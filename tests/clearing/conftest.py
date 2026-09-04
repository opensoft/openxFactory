"""Shared fixtures for the `clearing` contract family's tests.

THE VALIDATOR IS LOADED BY IMPORT, NOT RUN AS A SUBPROCESS. Its filename carries
dashes, so it is loaded through `importlib.util.spec_from_file_location` and
REGISTERED IN `sys.modules` BEFORE `exec_module` — the dataclass in it resolves
its annotations through `sys.modules[cls.__module__]`, and a module that is not
registered raises at class-creation time rather than at use.

`claim_conftest_slot` is called for the same reason the other four conftests in
this tree call it: `conftest` is an ambient top-level module name with a single
`sys.modules` entry, so a subtree that does not re-claim it can hijack another
subtree's import when both are collected in one run.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tests"))

from hermeticity import (  # noqa: E402,F401  (autouse fixture registration)
    claim_conftest_slot,
    hermetic_binary_path,
    hermetic_external_runners,
)

claim_conftest_slot(globals())

VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate-clearing-dispatch.py"
FAMILY_DIR = REPO_ROOT / "contracts" / "clearing"
EXAMPLES = FAMILY_DIR / "examples"
NEGATIVES = EXAMPLES / "negative"
REGISTRY_INSTANCE = FAMILY_DIR / "permitted-operations.registry.yaml"


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_clearing_dispatch", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = _load_validator()


@pytest.fixture(scope="session")
def reader():
    """The canonical validator, imported once per session."""
    return validator


@pytest.fixture(scope="session")
def registry_and_docs(reader):
    return reader.build_registry()


@pytest.fixture(scope="session")
def pinned(reader):
    """The PINNED openXwallet decoders.

    This does NOT degrade to a skip when the gitlink is absent, and that is
    deliberate: `.github/workflows/pytest-suite.yml` initializes `openXwallet`
    before the suite and pins the skipped count EXACTLY, so a directory that
    quietly turned into skips is the condition that pin exists to catch. An
    uninitialized gitlink must fail here, loudly, the way
    `tests/trust-anchor/` treats its own unavailable parent set.
    """
    return reader.load_pinned_reader()


@pytest.fixture(scope="session")
def entries(reader, registry_and_docs):
    """The register's entries, indexed by operation id."""
    doc = reader.load_yaml(REGISTRY_INSTANCE)
    findings = reader.Findings()
    resolved = reader.check_register(findings, doc, "permitted-operations.registry.yaml")
    assert findings.errors == [], findings.errors
    return resolved


@pytest.fixture(scope="session")
def fixture_origins(reader, pinned):
    findings = reader.Findings()
    return reader.read_origin_register(findings, reader.FIXTURE_IDENTITY, pinned)


@pytest.fixture(scope="session")
def live_origins(reader, pinned):
    findings = reader.Findings()
    return reader.read_origin_register(findings, reader.LIVE_IDENTITY, pinned)


def adjudicate(reader, registry_and_docs, entries, origins, doc, where="probe"):
    """Validate ONE record and return the findings it earned."""
    registry, docs = registry_and_docs
    findings = reader.Findings()
    reader.validate_record(findings, doc, where, registry, docs, entries, origins,
                           reader.NOW_SENTINEL)
    return findings
