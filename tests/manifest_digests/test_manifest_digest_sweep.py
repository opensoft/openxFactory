"""THE ESTATE-WIDE SWEEPER GETS A LANE (issue #512, second half).

`scripts/validate-manifest-digests.py` recomputes the sha256 of every file
`contracts/manifest.yaml` records a digest for. Its own docstring names the
failure mode it exists to close: a stale entry riding through bundle cuts
undetected (`content-manifest.schema.yaml`, stale since 403c2b5). Issue #512's
FIRST half was that exact failure recurring on a second row
(`ideation-dashboard-snapshot.schema.yaml`) and was repaired 2026-08-29 in
`88729102` — `python3 scripts/validate-manifest-digests.py` now prints
`OK contracts/manifest.yaml: 163 per-file digest(s) verify`. The SECOND half,
closed by this file, is that the checker was invoked by no workflow and no
test: it caught drift only when a human remembered to run it, which is the
same failure mode it was written to close, one level up. Both
`tests/credential_contracts/test_manifest_row_digest.py` and
`tests/signed_execution_chain/test_manifest_row_digests.py` say so in their
own docstrings, because each scopes itself to the handful of rows its own
capability owns and leans on the estate-wide sweep for every row it does not
— a dependency neither file could discharge for itself.

WHY A NEW MODULE RATHER THAN EXTENDING A FAMILY TEST. Scoping either sibling
file to run the whole sweep would make its result turn on rows that family
does not own, exactly the coupling both files' own "WHY NOT THE WHOLE
MANIFEST" paragraphs refuse. The estate-wide sweep needs a lane owned by
nobody's capability but the manifest itself, which is this file.

THE POSITIVE test runs the real checker as a subprocess, from the repository
root, exactly the way its own docstring's `Run:` line and a developer both
would — not the imported function, which would prove only that the code
executes, not that invoking the script the documented way succeeds and prints
what a reader of its output depends on. This is the assertion that actually
closes the issue: a checker that merely CAN be run is not one that IS run; a
checker `pytest tests/ -q -m "not postgres"` invokes on every required-suite
pass is.

THE NEGATIVE test proves the lane can go RED, not only that it stays green
today. A positive-only test would pass identically whether the checker still
recomputes anything or had been reduced to `sys.exit(0)` — indistinguishable
from the defect this whole issue is about. So the module is loaded by path
(it is `validate-manifest-digests.py`, hyphenated and therefore unimportable,
the reason `tests/openxwallet_pin/test_verify_pin.py` and
`tests/avatar_client_validator/test_f0_archive_fallback.py` load their own
subjects the same way) and its module-level `MANIFEST`/`ROOT` are
monkeypatched onto a throwaway manifest naming one real, committed file —
copied byte for byte, so the mismatch is manufactured only in the RECORDED
digest and never in the bytes read back — under a deliberately wrong
`sha256`. `main()` must still report the mismatch and return 1.

Hermetic: no network, and no `nlm`/`gh`/`omp` (`tests/hermeticity.py`'s
guarded set) — the subprocess in the positive test is `sys.executable` plus a
script path, the same shape already used by
`tests/credential_contracts/test_scaffolded_repo_conformance.py` and
`tests/credential_contracts/test_requirement_ref_resolution.py`. The negative
test touches only `tmp_path`.
"""

from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "validate-manifest-digests.py"


def _load_checker() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "validate_manifest_digests_under_test", CHECKER)
    assert spec and spec.loader, f"cannot load checker at {CHECKER}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_real_manifest_verifies_run_the_documented_way() -> None:
    """The command this lane actually gives CI: the checker as a subprocess,
    over the committed `contracts/manifest.yaml`, from the repository root —
    the `Run:` line in the checker's own docstring, unmodified."""
    result = subprocess.run(
        [sys.executable, str(CHECKER)],
        cwd=str(REPO_ROOT), capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK contracts/manifest.yaml:" in result.stdout, result.stdout
    assert "per-file digest(s) verify" in result.stdout, result.stdout


def test_a_stale_row_is_reported_and_fails_closed(
        tmp_path, monkeypatch, capsys) -> None:
    """The lane can go RED, not only stay green today. `pytest.ini` is copied
    byte for byte into the scratch tree — a real, committed file, chosen
    because it is small and stable — so the mismatch below lives only in the
    manifest's recorded digest, never in the file the checker reads back."""
    module = _load_checker()
    real_file = REPO_ROOT / "pytest.ini"
    copy = tmp_path / "pytest.ini"
    copy.write_bytes(real_file.read_bytes())
    wrong_digest = "0" * 64
    # Engineered, not assumed: prove the digest really is wrong before relying
    # on the checker to say so.
    assert hashlib.sha256(copy.read_bytes()).hexdigest() != wrong_digest
    manifest = tmp_path / "manifest.yaml"
    row = {"id": "scratch-row", "path": "pytest.ini", "sha256": wrong_digest}
    manifest.write_text(
        yaml.safe_dump({"contracts": [row]}), encoding="utf-8")
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "MANIFEST", manifest)

    exit_code = module.main()

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "FAIL pytest.ini: manifest records" in captured.out, captured.out
    assert "FAIL 1/1 manifest digest(s) do not verify" in captured.out, (
        captured.out)
