from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import pytest

from scripts.hermes_runtime_validation import content
from scripts.intent_compliance import authority_repository as authority


@pytest.mark.parametrize("reader", ["source", "family"])
@pytest.mark.parametrize("size", [8, 9])
def test_authority_blob_budget_precedes_content_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, reader: str, size: int
) -> None:
    payload = b"x" * size
    target = tmp_path / "authority.yaml"
    target.write_bytes(payload)
    for arguments in [
        ["init", "--quiet"],
        ["add", "authority.yaml"],
        [
            "-c",
            "user.name=Budget Test",
            "-c",
            "user.email=budget@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "authority",
        ],
    ]:
        subprocess.run(["git", *arguments], cwd=tmp_path, check=True)
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True
    ).strip()
    original_git = content._git
    blob_reads: list[tuple[str, ...]] = []

    def tracked_git(repository: Path, *arguments: str, binary: bool = False):
        if arguments[:2] == ("cat-file", "blob"):
            blob_reads.append(arguments)
        return original_git(repository, *arguments, binary=binary)

    monkeypatch.setattr(content, "_git", tracked_git)
    monkeypatch.setattr(authority, "MAX_INPUT_BYTES", 8)

    def read() -> bytes:
        if reader == "family":
            snapshot = authority.TrustedSnapshot(tmp_path, "example/factory", commit)
            return authority.read_trusted_family_blob(snapshot, "authority.yaml")
        source = authority.SourceCoordinates(
            commit, "authority.yaml", "sha256:" + hashlib.sha256(payload).hexdigest()
        )
        data, findings = authority.read_git_blob(tmp_path, source, "test source")
        assert not findings
        assert data is not None
        return data

    if size > 8:
        with pytest.raises(authority.TrustedSnapshotError):
            read()
        assert blob_reads == []
    else:
        assert read() == payload
        assert len(blob_reads) == 1
