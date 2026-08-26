"""Archive-aware F0 evidence resolution (issue #30, option C).

``_resolve_f0_dir`` follows the ``f0_evidence_pin.f0_change_path`` pin into
``openspec/changes/archive/<date>-<name>/`` once the owning change archives.
The fallback must be exactly as fail-closed as the path it replaces: it fires
only when the live directory is absent, and only on an unambiguous match —
zero or several dated archive copies resolve back to the absent pinned path so
the gate stays BLOCKED.

The validator is a hyphenated script, so it is loaded by file path with
``importlib``; each test monkeypatches the module-level ``ROOT`` to a tmp tree.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = REPOSITORY_ROOT / "scripts" / "validate-avatar-client.py"

CHANGE = "qualify-avatar-brokered-call-feasibility"
PIN = {"f0_change_path": f"openspec/changes/{CHANGE}"}


def _load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_avatar_client", ENTRYPOINT)
    assert spec and spec.loader, f"cannot load validator at {ENTRYPOINT}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _with_root(monkeypatch, module: ModuleType, root: Path) -> None:
    monkeypatch.setattr(module, "ROOT", root)


def test_live_change_dir_wins(tmp_path, monkeypatch):
    module = _load_validator()
    _with_root(monkeypatch, module, tmp_path)
    live = tmp_path / "openspec/changes" / CHANGE
    live.mkdir(parents=True)
    (tmp_path / "openspec/changes/archive" / f"2026-08-09-{CHANGE}").mkdir(parents=True)
    assert module._resolve_f0_dir(PIN) == live


def test_single_archive_match_resolves(tmp_path, monkeypatch):
    module = _load_validator()
    _with_root(monkeypatch, module, tmp_path)
    archived = tmp_path / "openspec/changes/archive" / f"2026-08-09-{CHANGE}"
    archived.mkdir(parents=True)
    assert module._resolve_f0_dir(PIN) == archived


def test_no_copy_anywhere_stays_on_absent_pin(tmp_path, monkeypatch):
    module = _load_validator()
    _with_root(monkeypatch, module, tmp_path)
    (tmp_path / "openspec/changes/archive").mkdir(parents=True)
    resolved = module._resolve_f0_dir(PIN)
    assert resolved == tmp_path / "openspec/changes" / CHANGE
    assert not resolved.exists()


def test_ambiguous_archive_matches_stay_closed(tmp_path, monkeypatch):
    module = _load_validator()
    _with_root(monkeypatch, module, tmp_path)
    for stamp in ("2026-08-09", "2026-08-10"):
        (tmp_path / "openspec/changes/archive" / f"{stamp}-{CHANGE}").mkdir(parents=True)
    resolved = module._resolve_f0_dir(PIN)
    assert resolved == tmp_path / "openspec/changes" / CHANGE
    assert not resolved.exists()


def test_empty_pin_resolves_to_root_without_globbing(tmp_path, monkeypatch):
    module = _load_validator()
    _with_root(monkeypatch, module, tmp_path)
    assert module._resolve_f0_dir({}) == tmp_path


def _write_bundle(directory: Path, members: dict[str, bytes]) -> None:
    import io
    import tarfile

    directory.mkdir(parents=True, exist_ok=True)
    with tarfile.open(directory / "supporting-docs.tar.gz", "w:gz") as tar:
        for name, data in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))


def test_member_bytes_prefers_the_loose_file(tmp_path):
    module = _load_validator()
    loose = tmp_path / "supporting-docs" / "f0-results.schema.yaml"
    loose.parent.mkdir(parents=True)
    loose.write_bytes(b"loose: true\n")
    _write_bundle(tmp_path, {"f0-results.schema.yaml": b"bundled: true\n"})
    assert module._f0_member_bytes(tmp_path, "supporting-docs/f0-results.schema.yaml") == b"loose: true\n"


def test_member_bytes_reads_the_packaged_bundle(tmp_path):
    module = _load_validator()
    _write_bundle(tmp_path, {"f0-results.schema.yaml": b"bundled: true\n"})
    assert module._f0_member_bytes(tmp_path, "supporting-docs/f0-results.schema.yaml") == b"bundled: true\n"


def test_member_bytes_missing_member_is_none(tmp_path):
    module = _load_validator()
    _write_bundle(tmp_path, {"other.yaml": b"x: 1\n"})
    assert module._f0_member_bytes(tmp_path, "supporting-docs/f0-results.schema.yaml") is None


def test_member_bytes_never_reads_bundle_for_non_support_paths(tmp_path):
    module = _load_validator()
    _write_bundle(tmp_path, {"f0-results.json": b"{}"})
    assert module._f0_member_bytes(tmp_path, "evidence/f0-results.json") is None


def test_member_bytes_empty_rel_is_none(tmp_path):
    module = _load_validator()
    assert module._f0_member_bytes(tmp_path, "") is None
