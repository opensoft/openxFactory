"""The wallet YAML syntax gate's own proof: drive it against scratch trees.

Matches the repo's validator-gating pattern (`tests/trust-anchor/
test_validator_gate.py`): run the script the way CI runs it — as a subprocess,
not an in-process import, so the exit codes the workflow will act on are the
ones under test — and point it at `tmp_path` roots built per case.

The four cases pin both sides of R7's ruled hole. A broken file that carries a
family kind string must FAIL (the exact fail-open the validator's layer 2
still shows: unparseable YAML skipped as "another kind"); a broken file
without one must PASS (this gate is not a whole-tree YAML linter; unrelated
broken YAML is nobody's business here); and the two valid cases prove the
gate adds no false failures of its own on either family-shaped or unrelated
YAML. The valid family case is deliberately NOT schema-conformant-complete:
syntax is all this gate measures.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GATE = REPO_ROOT / "scripts" / "wallet-yaml-syntax-gate.py"

# Unterminated flow sequence: parses for no reader. Carrying
# `xfactory_wallet_grant` makes it this gate's business.
BROKEN_WITH_KIND = (
    "kind: xfactory_wallet_grant\n"
    "scope:\n"
    "  acts: [\n"
)


def _run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(GATE), str(root)],
                          capture_output=True, text=True, cwd=REPO_ROOT)


def test_broken_yaml_carrying_a_family_kind_fails_and_names_the_file(
        tmp_path: Path) -> None:
    (tmp_path / "broken.yaml").write_text(BROKEN_WITH_KIND, encoding="utf-8")
    result = _run(tmp_path)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "ERROR" in result.stdout
    assert "broken.yaml" in result.stdout


def test_broken_yaml_without_a_family_kind_passes(tmp_path: Path) -> None:
    # Same syntax defect, no kind string: skipped silently, exactly as the
    # prefilter promises, so unrelated trees stay out of the gate's blast.
    (tmp_path / "unrelated-broken.yaml").write_text("foo: [bar\n",
                                                    encoding="utf-8")
    result = _run(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ERROR" not in result.stdout


def test_valid_family_document_passes(tmp_path: Path) -> None:
    (tmp_path / "wallet.yaml").write_text(
        "kind: xfactory_wallet_record\n"
        "wallet_id: wallet-example\n"
        "key_reference:\n"
        "  key_id: key-1\n",
        encoding="utf-8")
    result = _run(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ERROR" not in result.stdout


def test_valid_unrelated_yaml_passes(tmp_path: Path) -> None:
    (tmp_path / "notes.yaml").write_text(
        "title: meeting notes\n"
        "tags:\n"
        "  - a\n"
        "  - b\n",
        encoding="utf-8")
    result = _run(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ERROR" not in result.stdout
