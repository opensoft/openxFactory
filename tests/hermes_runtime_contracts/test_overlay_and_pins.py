"""RED contracts for exact assembly pins and closed overlay inventories."""

from __future__ import annotations

import hashlib
import importlib
import os
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from scripts.hermes_runtime_validation.content import resolve_git_object
from tests.hermes_runtime_contracts.support import commit_files, init_git_repo, run_command


CANONICAL_REPOSITORY = "opensoft/example-domain"


def _digest(body: bytes) -> str:
    return f"sha256:{hashlib.sha256(body).hexdigest()}"


def _overlays() -> ModuleType:
    try:
        return importlib.import_module(
            "scripts.hermes_runtime_validation.semantics.overlays"
        )
    except ModuleNotFoundError as exc:
        pytest.fail(f"planned overlay semantics are missing: {exc}")


def _codes(findings: list[Any]) -> list[str]:
    return [
        str(finding["code"] if isinstance(finding, dict) else finding.code)
        for finding in findings
    ]


@pytest.fixture
def overlay_repo(tmp_path: Path) -> tuple[Path, str, dict[str, bytes]]:
    repo = init_git_repo(tmp_path / "domain")
    files = {
        "overlay/A.yaml": b"name: upper\n",
        "overlay/a.yaml": b"name: lower\n",
        "overlay/nested/z.txt": b"recursive\x00bytes\n",
        "overlay/nested/.gitkeep": b"",
        "overlay/.generated-digests.yaml": b"generated: true\n",
        "templates/customer.yaml": b"kind: CustomerTemplate\n",
    }
    commit = commit_files(repo, files)
    run_command(["git", "branch", "-M", "main"], cwd=repo, check=True)
    run_command(["git", "tag", "v1.0.0", commit], cwd=repo, check=True)
    return repo, commit, files


def _single_file_pin(commit: str, body: bytes) -> dict[str, object]:
    return {
        "repository": CANONICAL_REPOSITORY,
        "commit": commit,
        "path": "templates/customer.yaml",
        "schema_id": "https://xforge.us/schemas/example/customer-template",
        "schema_version": 1,
        "digest": _digest(body),
    }


def _manifest(files: dict[str, bytes]) -> dict[str, object]:
    inventoried = [
        path
        for path in files
        if path.startswith("overlay/")
        and not path.endswith("/.gitkeep")
        and path != "overlay/.generated-digests.yaml"
    ]
    inventoried.sort(key=lambda path: path.encode("utf-8"))
    return {
        "schema_version": 1,
        "kind": "HermesRuntimeOverlayManifest",
        "overlay_root": "overlay",
        "files": [
            {"path": path, "digest": _digest(files[path])} for path in inventoried
        ],
        "exclusions": [
            {"kind": "gitkeep", "path": "overlay/nested/.gitkeep"},
            {
                "kind": "generated_digest_inventory",
                "path": "overlay/.generated-digests.yaml",
            },
        ],
    }


def test_exact_single_file_pin_uses_commit_bytes_not_worktree(
    overlay_repo: tuple[Path, str, dict[str, bytes]],
) -> None:
    repo, commit, files = overlay_repo
    (repo / "templates/customer.yaml").write_bytes(b"dirty worktree\n")
    findings = _overlays().validate_single_file_pin(
        _single_file_pin(commit, files["templates/customer.yaml"]),
        checkout=repo,
        expected_repository=CANONICAL_REPOSITORY,
        resolver=resolve_git_object,
    )
    assert findings == []


def test_recursive_overlay_inventory_byte_order_and_closed_exclusions_pass(
    overlay_repo: tuple[Path, str, dict[str, bytes]],
) -> None:
    repo, commit, files = overlay_repo
    findings = _overlays().validate_overlay_manifest(
        _manifest(files),
        checkout=repo,
        commit=commit,
        expected_repository=CANONICAL_REPOSITORY,
        resolver=resolve_git_object,
    )
    assert findings == []


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("missing", "HCS-OVERLAY-MISSING-MEMBER"),
        ("extra", "HCS-OVERLAY-EXTRA-MEMBER"),
        ("order", "HCS-OVERLAY-BYTE-ORDER"),
        ("exclusion", "HCS-OVERLAY-EXCLUSION"),
    ],
)
def test_overlay_membership_order_and_exclusions_fail_for_exact_reason(
    overlay_repo: tuple[Path, str, dict[str, bytes]],
    mutation: str,
    expected_code: str,
) -> None:
    repo, commit, files = overlay_repo
    manifest = _manifest(files)
    entries = manifest["files"]
    assert isinstance(entries, list)
    if mutation == "missing":
        entries.pop()
    elif mutation == "extra":
        entries.append(
            {"path": "overlay/not-in-tree.yaml", "digest": _digest(b"absent\n")}
        )
    elif mutation == "order":
        entries[0], entries[1] = entries[1], entries[0]
    else:
        manifest["exclusions"] = [
            {"kind": "temporary", "path": "overlay/a.yaml"}
        ]

    findings = _overlays().validate_overlay_manifest(
        manifest,
        checkout=repo,
        commit=commit,
        expected_repository=CANONICAL_REPOSITORY,
        resolver=resolve_git_object,
    )
    assert expected_code in _codes(findings)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("overlay_root", "../outside"),
        ("overlay_root", "/absolute/overlay"),
        ("file_path", "overlay/../outside.yaml"),
    ],
)
def test_overlay_traversal_and_absolute_paths_fail_closed(
    overlay_repo: tuple[Path, str, dict[str, bytes]], field: str, value: str
) -> None:
    repo, commit, files = overlay_repo
    manifest = _manifest(files)
    if field == "file_path":
        manifest["files"][0]["path"] = value  # type: ignore[index]
    else:
        manifest[field] = value
    findings = _overlays().validate_overlay_manifest(
        manifest,
        checkout=repo,
        commit=commit,
        expected_repository=CANONICAL_REPOSITORY,
        resolver=resolve_git_object,
    )
    assert "HCS-OVERLAY-PATH" in _codes(findings)


@pytest.mark.parametrize("entry_kind", ["symlink", "submodule"])
def test_overlay_rejects_symlink_and_submodule_tree_entries(
    overlay_repo: tuple[Path, str, dict[str, bytes]], entry_kind: str
) -> None:
    repo, commit, files = overlay_repo
    if entry_kind == "symlink":
        os.symlink("A.yaml", repo / "overlay/link.yaml")
        run_command(["git", "add", "overlay/link.yaml"], cwd=repo, check=True)
    else:
        run_command(
            [
                "git",
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{commit},overlay/vendor",
            ],
            cwd=repo,
            check=True,
        )
    run_command(["git", "commit", "--quiet", "-m", f"add {entry_kind}"], cwd=repo, check=True)
    tree_commit = run_command(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True
    ).stdout.strip()
    findings = _overlays().validate_overlay_manifest(
        _manifest(files),
        checkout=repo,
        commit=tree_commit,
        expected_repository=CANONICAL_REPOSITORY,
        resolver=resolve_git_object,
    )
    assert "HCS-OVERLAY-NONREGULAR" in _codes(findings)


@pytest.mark.parametrize("movable_ref", ["main", "v1.0.0"])
def test_branch_or_tag_without_exact_commit_is_rejected(
    overlay_repo: tuple[Path, str, dict[str, bytes]], movable_ref: str
) -> None:
    repo, _, files = overlay_repo
    findings = _overlays().validate_single_file_pin(
        _single_file_pin(movable_ref, files["templates/customer.yaml"]),
        checkout=repo,
        expected_repository=CANONICAL_REPOSITORY,
        resolver=resolve_git_object,
    )
    assert "HCS-PIN-EXACT-COMMIT" in _codes(findings)


def test_single_file_and_overlay_digest_drift_are_distinct_findings(
    overlay_repo: tuple[Path, str, dict[str, bytes]],
) -> None:
    repo, commit, files = overlay_repo
    pin = _single_file_pin(commit, files["templates/customer.yaml"])
    pin["digest"] = _digest(b"different template\n")
    pin_findings = _overlays().validate_single_file_pin(
        pin,
        checkout=repo,
        expected_repository=CANONICAL_REPOSITORY,
        resolver=resolve_git_object,
    )
    assert "HCS-PIN-DIGEST" in _codes(pin_findings)

    manifest = _manifest(files)
    manifest["files"][0]["digest"] = _digest(b"different overlay\n")  # type: ignore[index]
    overlay_findings = _overlays().validate_overlay_manifest(
        manifest,
        checkout=repo,
        commit=commit,
        expected_repository=CANONICAL_REPOSITORY,
        resolver=resolve_git_object,
    )
    assert "HCS-OVERLAY-DIGEST" in _codes(overlay_findings)
