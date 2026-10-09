"""Shared paths and helpers for the `council-convening` family's tests.

A PACKAGE conftest (`council_convening.conftest`; see `__init__.py`), so it
needs no `claim_conftest_slot`. It imports nothing from the implementation
under test: a test module whose implementation is absent then fails at its
own import, and the rest of the suite still collects. That is the red state
the tasks' tests-first rule records.

The repository root is APPENDED to `sys.path`, never prepended, so that
`scripts.council_convening` resolves without shadowing any name another
subtree already resolves.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

FAMILY_REL = Path("contracts") / "council-convening"
DIGEST_CONSTRUCTION_REL = (
    Path("contracts") / "signed-execution-chain" / "digest-construction.schema.yaml")

FAMILY = REPO_ROOT / FAMILY_REL
CONFORMANCE = FAMILY / "conformance"
VECTORS = CONFORMANCE / "vectors"
INDEX = CONFORMANCE / "index.json"
SHARED_DEFINITIONS = FAMILY / "shared-definitions.schema.yaml"
PROTOCOL_REGISTRY_SCHEMA = FAMILY / "protocol-registry.schema.yaml"
PROTOCOL_REGISTRY = FAMILY / "protocol.registry.yaml"
DIGEST_CONSTRUCTION = REPO_ROOT / DIGEST_CONSTRUCTION_REL
VALIDATOR = REPO_ROOT / "scripts" / "validate-council-convening.py"
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "council-convening-gate.yml"

REPLACEMENT = "xfc-resolved-council-1"
LEGACY = "xfactory-council-seat-return/v1"


def run_validator(*args: str, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess:
    """The canonical validator as CI runs it: a separate process, from the
    repository root unless a test says otherwise."""
    return subprocess.run(
        [sys.executable, str(VALIDATOR), *args],
        cwd=str(cwd), capture_output=True, text=True, timeout=300)


def load_validator():
    """The validator module, imported in process.

    Its filename carries dashes, so it is loaded by path, and registered in
    `sys.modules` before `exec_module`, as `tests/clearing/conftest.py` does.
    """
    name = "validate_council_convening"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def copy_family(root: Path) -> Path:
    """Copy the family and the digest-construction file it `$ref`s under `root`,
    in their repository layout, so a test can mutate a tree without touching
    the real one. Returns `root`."""
    shutil.copytree(FAMILY, root / FAMILY_REL)
    target = root / DIGEST_CONSTRUCTION_REL
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DIGEST_CONSTRUCTION, target)
    return root


@pytest.fixture
def family_tree(tmp_path: Path) -> Path:
    """A writable copy of the family, rooted at a temporary repository root."""
    return copy_family(tmp_path / "repo")
