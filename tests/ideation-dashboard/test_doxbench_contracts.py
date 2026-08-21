"""Released-schema loading, digest verification, and delegated semantics (T014).

Two rungs, deliberately separated.

THE HERMETIC RUNG builds its own pinned checkout in `tmp_path` and monkeypatches
`SCHEMA_DIGESTS` to the digests of those fake bytes. That is not a weakening of
the digest check — it is the only way to test the check itself. A hermetic test
cannot author bytes that hash to the RELEASED digests (that is the entire point
of a digest), so testing "correct digest loads / one flipped byte refuses" needs
a pin the test controls. The released pin's own literal values are asserted
separately, against the constants and against `stack.yaml`, so a repin cannot
slip through unnoticed.

THE INTEGRATION RUNG reads the REAL released bytes: real digests, the packaged
workbench positives, and the delegated openxFactory validator. It runs by DEFAULT
from a publisher checkout — this suite is hosted inside openxFactory, so the
released bytes are simply present — and `OPENXFACTORY_ROOT` still selects a
different checkout when one is wanted:

    OPENXFACTORY_ROOT=/workspace/projects/xFactory/openxFactory-worktrees/contract-v1.34

It skips loudly only when neither is available. Making this rung default-on is
what turns a pin the serve would refuse on back into a test failure instead of a
runtime 500 (`align-doxbench-contract-pin-to-publisher`, 2026-08-10) — while it
was env-gated, the publisher-mode break sat green in CI for a week.

Every rule the shape cannot express belongs to the openxFactory validator, so
this suite never restates one: it asserts DELEGATION happened (the pinned script
was launched, its exit code was returned) and nothing about how it decides.
"""

from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path

import pytest
import yaml

from ideation_dashboard import doxbench_contracts as contracts

CATALOG_SCHEMA_FILE = "xfactory-workbench-model-catalog.schema.yaml"
CHAT_TURN_SCHEMA_FILE = "xfactory-workbench-chat-turn.schema.yaml"

# RE-PINNED at contract-v1.38 (add-doxbench-editing-phase-b §11.7). The MIRROR
# IMAGE of the v1.34 repin: there the chat-turn digest moved and the catalog's
# did not, because that release widened the chat-turn file; here the CATALOG
# digest moves and the chat-turn's does not, because this release grows the
# catalog entry with the routing-rule declaration.
#
# The REF is the unresolved-until-published sentinel again, on v1.34's own
# precedent — the policy publishes the annotated tag against the commit that
# LANDS, so across a realization branch there is no release commit to name and
# the sentinel is spelled as a value no `stack.yaml` can declare, so a consumer
# comparing against it refuses rather than matching by accident. A follow-up
# commit resolves it, as 7c544c84 did for v1.34 (`contract-v1.34^{}` == 5daa173,
# tag object 439d76b).
RELEASED_REF = "unpublished:contract-v1.38"
RELEASED_TAG = "contract-v1.38"
RELEASED_DIGESTS = {
    CATALOG_SCHEMA_FILE:
        "692dad330c5958720d9ba6ef8f6ce1a19dec715547a087e0b08ccd30a9aaa26d",
    CHAT_TURN_SCHEMA_FILE:
        "2eb2a834d4cd50a15838e0e7197b6ddaa6f33aee7d24ff8075e0df8deab0b7e5",
}

# ---------------------------------------------------------------------------
# hermetic fixture world
#
# The fake schemas mirror the released files' STRUCTURE (a whole-document
# catalog; one chat-turn file holding SIX envelopes under `$defs` -- the three v1
# ones and the three contract-v1.34 added beside them -- selected by a `oneOf`),
# because the structure is what the loader's per-kind mapping and the
# registry-backed `$ref` resolution have to cope with. They deliberately do NOT
# mirror the released files' rules — restating a contract rule in a fixture is
# the forking of contract authority this whole module exists to avoid.
# ---------------------------------------------------------------------------

FAKE_CATALOG_SCHEMA = """\
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "xfactory-workbench-model-catalog.schema.yaml"
type: object
additionalProperties: false
required: [schema_version, kind, models]
properties:
  schema_version: { const: 1 }
  kind: { const: workbench-model-catalog }
  models:
    type: array
    items:
      type: object
      additionalProperties: false
      required: [model_id, label]
      properties:
        model_id: { type: string, minLength: 1 }
        label: { type: string, minLength: 1 }
"""

FAKE_CHAT_TURN_SCHEMA = """\
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "xfactory-workbench-chat-turn.schema.yaml"
oneOf:
  - $ref: "#/$defs/request"
  - $ref: "#/$defs/success"
  - $ref: "#/$defs/failure"
  - $ref: "#/$defs/request_v2"
  - $ref: "#/$defs/success_v2"
  - $ref: "#/$defs/failure_v2"
$defs:
  request:
    type: object
    additionalProperties: false
    required: [schema_version, kind, message]
    properties:
      schema_version: { const: 1 }
      kind: { const: workbench-chat-turn }
      message: { type: string, minLength: 1 }
  success:
    type: object
    additionalProperties: false
    required: [schema_version, kind, assistant_prose]
    properties:
      schema_version: { const: 1 }
      kind: { const: workbench-chat-turn-success }
      assistant_prose: { type: string }
  failure:
    type: object
    additionalProperties: false
    required: [schema_version, kind, error]
    properties:
      schema_version: { const: 1 }
      kind: { const: workbench-chat-turn-failure }
      error: { type: string, minLength: 1 }
  request_v2:
    type: object
    additionalProperties: false
    required: [schema_version, kind, message]
    properties:
      schema_version: { const: 1 }
      kind: { const: workbench-chat-turn-v2 }
      message: { type: string, minLength: 1 }
  success_v2:
    type: object
    additionalProperties: false
    required: [schema_version, kind, assistant_prose]
    properties:
      schema_version: { const: 1 }
      kind: { const: workbench-chat-turn-v2-success }
      assistant_prose: { type: string }
  failure_v2:
    type: object
    additionalProperties: false
    required: [schema_version, kind, error]
    properties:
      schema_version: { const: 1 }
      kind: { const: workbench-chat-turn-v2-failure }
      error: { type: string, minLength: 1 }
"""

MINIMAL_CATALOG = {
    "schema_version": 1,
    "kind": "workbench-model-catalog",
    "models": [{"model_id": "local-authoring-1", "label": "Approved model"}],
}


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_manifest(root: Path, digests: dict[str, str]) -> Path:
    """The released checkout's self-description, in the shape the real
    `contracts/manifest.yaml` uses: a `contracts` list whose entries carry the
    repository-relative `path` and the per-file `sha256`."""
    manifest = {
        "schema_version": 1,
        "contract_bundle_version": RELEASED_TAG,
        "contracts": [
            {
                "id": Path(name).stem,
                "path": f"contracts/schemas/{name}",
                "type": "schema",
                "sha256": digest,
            }
            for name, digest in sorted(digests.items())
        ],
    }
    path = root / "contracts" / "manifest.yaml"
    path.write_text(yaml.safe_dump(manifest, sort_keys=True), encoding="utf-8")
    return path


@pytest.fixture
def fake_root(tmp_path, monkeypatch):
    """A self-consistent fake pinned checkout: two schema files, a manifest that
    agrees with their bytes, and `SCHEMA_DIGESTS` pinned to those same bytes."""
    root = tmp_path / "openxFactory"
    schemas = root / "contracts" / "schemas"
    schemas.mkdir(parents=True)
    (schemas / CATALOG_SCHEMA_FILE).write_text(FAKE_CATALOG_SCHEMA, encoding="utf-8")
    (schemas / CHAT_TURN_SCHEMA_FILE).write_text(FAKE_CHAT_TURN_SCHEMA, encoding="utf-8")
    digests = {
        CATALOG_SCHEMA_FILE: _sha256_file(schemas / CATALOG_SCHEMA_FILE),
        CHAT_TURN_SCHEMA_FILE: _sha256_file(schemas / CHAT_TURN_SCHEMA_FILE),
    }
    _write_manifest(root, digests)
    monkeypatch.setattr(contracts, "SCHEMA_DIGESTS", dict(digests))
    return root


@pytest.fixture
def pinned_repo(tmp_path):
    """A repo root whose `stack.yaml` declares the pinned contract_ref."""
    return _repo_with_ref(tmp_path / "repo", RELEASED_REF)


def _repo_with_ref(root: Path, ref: str | None) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    xfactory: dict[str, object] = {"contract_ref_type": "commit"}
    if ref is not None:
        xfactory["contract_ref"] = ref
    (root / "stack.yaml").write_text(
        yaml.safe_dump({"xfactory": xfactory}, sort_keys=True), encoding="utf-8")
    return root


# ---------------------------------------------------------------------------
# the pin itself
# ---------------------------------------------------------------------------

def test_module_pins_the_immutable_released_contract():
    """The release is immutable (R13): these literals name content that exists,
    and the pin moves only through the normal xFactory workflow (T006)."""
    assert contracts.CONTRACT_REF == RELEASED_REF
    assert contracts.CONTRACT_TAG == RELEASED_TAG
    assert contracts.SCHEMA_DIGESTS == RELEASED_DIGESTS


# `test_repository_stack_pin_matches_the_module_pin` stayed with codexFactory's
# committed `stack.yaml` (adopt-neutral-tooling-home tranche B, 2026-08-03):
# `verify_stack_pin` checks the HOSTING repo's declared consumption pin, and
# openxFactory is the contract PUBLISHER — it has no stack.yaml and must not
# grow one. The release identity is still fully anchored here by the module's
# hard-pinned digests plus the checkout manifest (`_verified_document`, tested
# below).
#
# That tranche's OPEN ITEM — from a publisher checkout the stack-pin step raised,
# so serve's two doxbench model routes failed CLOSED — is RESOLVED by
# `align-doxbench-contract-pin-to-publisher` (2026-08-10). The ruled disposition
# is publisher mode: a hosting repo that IS a release consumes `CONTRACT_REF` by
# construction and reads no declaration. See the `publisher mode` section below,
# which pins both halves — that it passes without a stack.yaml, and that it
# exempts no byte.


def test_declared_wire_kinds_are_every_doxbench_instance_kind():
    """RE-PINNED at contract-v1.34 (add-doxbench-editing-phase-b §13): the
    co-resident widened family adds three kinds beside the three v1 ones, which
    stay DECLARED because they are deprecated, not withdrawn."""
    assert set(contracts.WIRE_KINDS) == {
        "workbench-model-catalog",
        "workbench-chat-turn",
        "workbench-chat-turn-success",
        "workbench-chat-turn-failure",
        "workbench-chat-turn-v2",
        "workbench-chat-turn-v2-success",
        "workbench-chat-turn-v2-failure",
    }


def test_the_v1_family_is_declared_deprecated_and_still_dispatchable():
    """contract-v1.34 deprecates the v1 family with a removal target of
    contract-v2.0. Deprecated is NOT withdrawn: every deprecated kind still
    resolves to its own envelope, because the policy's breaking path requires
    the old shape to keep working for at least one full published release."""
    assert set(contracts.DEPRECATED_CHAT_TURN_KINDS) == {
        "workbench-chat-turn",
        "workbench-chat-turn-success",
        "workbench-chat-turn-failure",
    }
    for kind in contracts.DEPRECATED_CHAT_TURN_KINDS:
        assert kind in contracts.WIRE_KINDS
        assert kind in contracts.CHAT_TURN_DEFS


# ---------------------------------------------------------------------------
# loading (hermetic)
# ---------------------------------------------------------------------------

def test_load_returns_one_schema_per_wire_kind(fake_root, pinned_repo):
    schemas = contracts.load_released_schemas(fake_root, repo_root=pinned_repo)

    assert set(schemas) == set(contracts.WIRE_KINDS)
    # The catalog kind gets the whole-document schema.
    assert schemas["workbench-model-catalog"]["properties"]["kind"]["const"] == \
        "workbench-model-catalog"
    # The three turn kinds get a `$ref` INTO the one chat-turn file, so the
    # oneOf's three envelopes stay individually addressable by kind.
    for kind, definition in (
        ("workbench-chat-turn", "request"),
        ("workbench-chat-turn-success", "success"),
        ("workbench-chat-turn-failure", "failure"),
    ):
        assert schemas[kind] == {
            "$ref": f"{CHAT_TURN_SCHEMA_FILE}#/$defs/{definition}"}


def test_openxfactory_root_env_selects_the_checkout(fake_root, pinned_repo,
                                                    monkeypatch):
    monkeypatch.setenv("OPENXFACTORY_ROOT", str(fake_root))
    schemas = contracts.load_released_schemas(repo_root=pinned_repo)
    assert set(schemas) == set(contracts.WIRE_KINDS)


def test_explicit_root_wins_over_the_env_override(fake_root, pinned_repo,
                                                  tmp_path, monkeypatch):
    monkeypatch.setenv("OPENXFACTORY_ROOT", str(tmp_path / "nowhere"))
    schemas = contracts.load_released_schemas(fake_root, repo_root=pinned_repo)
    assert set(schemas) == set(contracts.WIRE_KINDS)


def test_absent_schema_file_fails_closed(fake_root, pinned_repo):
    (fake_root / "contracts" / "schemas" / CHAT_TURN_SCHEMA_FILE).unlink()

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.load_released_schemas(fake_root, repo_root=pinned_repo)
    assert CHAT_TURN_SCHEMA_FILE in str(excinfo.value)


def test_unreachable_checkout_fails_closed(tmp_path, pinned_repo):
    with pytest.raises(contracts.ContractPinError):
        contracts.load_released_schemas(tmp_path / "no-checkout",
                                        repo_root=pinned_repo)


def test_one_flipped_byte_fails_closed(fake_root, pinned_repo):
    """A digest mismatch is a REFUSAL, never a warning: a schema copy that is not
    the released bytes is not the contract, whatever else it looks like."""
    target = fake_root / "contracts" / "schemas" / CATALOG_SCHEMA_FILE
    original = target.read_text(encoding="utf-8")
    target.write_text(original.replace("const: 1", "const: 2", 1), encoding="utf-8")

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.load_released_schemas(fake_root, repo_root=pinned_repo)
    message = str(excinfo.value)
    assert CATALOG_SCHEMA_FILE in message
    assert contracts.SCHEMA_DIGESTS[CATALOG_SCHEMA_FILE] in message


def test_trailing_newline_change_fails_closed(fake_root, pinned_repo):
    """Byte identity, not YAML equivalence: the same document with one extra
    byte is a different artifact."""
    target = fake_root / "contracts" / "schemas" / CHAT_TURN_SCHEMA_FILE
    target.write_bytes(target.read_bytes() + b"\n")

    with pytest.raises(contracts.ContractPinError):
        contracts.load_released_schemas(fake_root, repo_root=pinned_repo)


def test_manifest_disagreeing_with_the_bytes_fails_closed(fake_root, pinned_repo):
    """Manifest parity: the release's own self-description must match the bytes
    on disk. If they disagree, the checkout is not a coherent release."""
    _write_manifest(fake_root, {
        CATALOG_SCHEMA_FILE: contracts.SCHEMA_DIGESTS[CATALOG_SCHEMA_FILE],
        CHAT_TURN_SCHEMA_FILE: "0" * 64,
    })

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.load_released_schemas(fake_root, repo_root=pinned_repo)
    message = str(excinfo.value)
    assert "manifest" in message
    assert CHAT_TURN_SCHEMA_FILE in message


def test_manifest_without_an_entry_for_a_pinned_schema_fails_closed(fake_root,
                                                                    pinned_repo):
    _write_manifest(fake_root, {
        CATALOG_SCHEMA_FILE: contracts.SCHEMA_DIGESTS[CATALOG_SCHEMA_FILE],
    })

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.load_released_schemas(fake_root, repo_root=pinned_repo)
    assert CHAT_TURN_SCHEMA_FILE in str(excinfo.value)


def test_absent_manifest_fails_closed(fake_root, pinned_repo):
    (fake_root / "contracts" / "manifest.yaml").unlink()

    with pytest.raises(contracts.ContractPinError):
        contracts.load_released_schemas(fake_root, repo_root=pinned_repo)


# ---------------------------------------------------------------------------
# stack.yaml pin drift
# ---------------------------------------------------------------------------

def test_drifted_stack_pin_fails_closed(fake_root, tmp_path):
    drifted = _repo_with_ref(tmp_path / "drifted", "c782d6d" + "0" * 33)

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.load_released_schemas(fake_root, repo_root=drifted)
    message = str(excinfo.value)
    assert "stack.yaml" in message
    assert contracts.CONTRACT_REF in message


def test_stack_without_a_contract_ref_fails_closed(fake_root, tmp_path):
    refless = _repo_with_ref(tmp_path / "refless", None)

    with pytest.raises(contracts.ContractPinError):
        contracts.load_released_schemas(fake_root, repo_root=refless)


def test_absent_stack_fails_closed(fake_root, tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()

    with pytest.raises(contracts.ContractPinError):
        contracts.load_released_schemas(fake_root, repo_root=empty)


# ---------------------------------------------------------------------------
# publisher mode
#
# The ruled disposition for adopt-neutral-tooling-home's tranche-D open item
# (align-doxbench-contract-pin-to-publisher, 2026-08-10). Two halves, and the
# second is the one that matters: publisher mode must drop the vacuous question
# WITHOUT becoming a way past the byte chain.
# ---------------------------------------------------------------------------

def _make_publisher(root: Path) -> Path:
    """Complete a fake checkout into a publisher release. `fake_root` already
    carries the manifest and the schemas, so only the family validator is
    missing."""
    validator = root / contracts.VALIDATOR_IN_CHECKOUT
    validator.parent.mkdir(parents=True, exist_ok=True)
    validator.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    return root


def test_a_publisher_checkout_needs_no_declared_pin(fake_root):
    """The publisher declares no consumption pin on itself; refusing for want of
    one is a question with no honest answer."""
    publisher = _make_publisher(fake_root)
    assert contracts.is_publisher_checkout(publisher)
    assert not (publisher / contracts.STACK_FILE).exists()

    assert contracts.verify_stack_pin(publisher) == contracts.CONTRACT_REF
    schemas = contracts.load_released_schemas(publisher, repo_root=publisher)
    assert set(schemas) == set(contracts.WIRE_KINDS)


@pytest.mark.parametrize("missing", contracts.PUBLISHER_MARKERS,
                         ids=lambda marker: str(marker))
def test_an_incomplete_publisher_still_needs_its_declared_pin(fake_root, missing):
    """All three markers TOGETHER: any one alone is satisfied by a tree that
    merely contains a similarly named file, which is exactly the confusion
    manifest parity exists to prevent for a single schema."""
    publisher = _make_publisher(fake_root)
    target = publisher / missing
    shutil.rmtree(target) if target.is_dir() else target.unlink()

    assert not contracts.is_publisher_checkout(publisher)
    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.verify_stack_pin(publisher)
    assert contracts.STACK_FILE in str(excinfo.value)


def test_publisher_mode_does_not_exempt_a_drifted_digest(fake_root):
    """The whole safety argument. Publisher mode drops ONE vacuous question and
    keeps every substantive one — `_verified_bytes` is untouched by it."""
    publisher = _make_publisher(fake_root)
    target = publisher / "contracts" / "schemas" / CATALOG_SCHEMA_FILE
    target.write_text(target.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.load_released_schemas(publisher, repo_root=publisher)
    assert "sha256" in str(excinfo.value)


def test_publisher_mode_does_not_exempt_a_disagreeing_manifest(fake_root):
    publisher = _make_publisher(fake_root)
    _write_manifest(publisher, {name: "0" * 64 for name in contracts.SCHEMA_DIGESTS})

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.load_released_schemas(publisher, repo_root=publisher)
    assert "manifest.yaml" in str(excinfo.value)


def test_a_consumer_repo_keeps_every_declared_pin_refusal(fake_root, tmp_path):
    """Nothing about consumer pinning moved: a domain repo still declares the
    release it consumes and still refuses on drift."""
    drifted = _repo_with_ref(tmp_path / "drifted", "c782d6d" + "0" * 33)
    assert not contracts.is_publisher_checkout(drifted)

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.load_released_schemas(fake_root, repo_root=drifted)
    assert contracts.CONTRACT_REF in str(excinfo.value)


# ---------------------------------------------------------------------------
# checkout resolution
# ---------------------------------------------------------------------------

def _publisher_tree(root: Path) -> Path:
    """A minimally publisher-shaped directory — markers only, no real bytes.
    Resolution is a STRUCTURAL question and must not need a loadable release."""
    (root / contracts.SCHEMAS_RELPATH).mkdir(parents=True, exist_ok=True)
    (root / contracts.MANIFEST_RELPATH).write_text("", encoding="utf-8")
    validator = root / contracts.VALIDATOR_IN_CHECKOUT
    validator.parent.mkdir(parents=True, exist_ok=True)
    validator.write_text("", encoding="utf-8")
    return root


def test_resolution_prefers_the_hosting_repo_over_a_reachable_sibling(
        tmp_path, monkeypatch):
    """THE DEFECT THIS REPLACES. `VALIDATOR_RELPATH` carries the `openxFactory/`
    prefix, so from inside the publisher the walk searched one level BELOW where
    it stood: it went past itself every time and landed on the aggregation's
    submodule — a shared tree sessions move between branches. A serve in a
    worktree was verifying its wire shapes against another session's checkout."""
    monkeypatch.delenv(contracts.OPENXFACTORY_ROOT_ENV, raising=False)
    aggregation = tmp_path / "aggregation"
    sibling = _publisher_tree(aggregation / "openxFactory")
    hosting = _publisher_tree(aggregation / "openxFactory-worktrees" / "feature")

    # The walk-up genuinely WOULD find the sibling from here — this is the real
    # layout, not a contrived one.
    assert (aggregation / contracts.VALIDATOR_RELPATH).is_file()

    assert contracts.resolve_root(start=hosting) == hosting.resolve()
    assert contracts.resolve_root(start=hosting) != sibling.resolve()


def test_a_consumer_hosting_repo_still_walks_up(tmp_path, monkeypatch):
    """The rung above is additive: a tree that is not a publisher reaches the
    existing aggregation-relative walk exactly as before."""
    monkeypatch.delenv(contracts.OPENXFACTORY_ROOT_ENV, raising=False)
    aggregation = tmp_path / "aggregation"
    sibling = _publisher_tree(aggregation / "openxFactory")
    consumer = aggregation / "xFactories" / "codexFactory"
    consumer.mkdir(parents=True)

    assert not contracts.is_publisher_checkout(consumer)
    assert contracts.resolve_root(start=consumer) == sibling


def test_explicit_root_and_env_outrank_the_publisher_rung(tmp_path, monkeypatch):
    hosting = _publisher_tree(tmp_path / "hosting")
    elsewhere = tmp_path / "elsewhere"

    monkeypatch.setenv(contracts.OPENXFACTORY_ROOT_ENV, str(elsewhere))
    assert contracts.resolve_root(start=hosting) == elsewhere
    assert contracts.resolve_root(tmp_path / "explicit", start=hosting) == \
        tmp_path / "explicit"


def test_resolution_still_fails_closed_with_no_checkout_anywhere(tmp_path,
                                                                 monkeypatch):
    monkeypatch.delenv(contracts.OPENXFACTORY_ROOT_ENV, raising=False)
    nowhere = tmp_path / "nowhere"
    nowhere.mkdir()

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.resolve_root(start=nowhere)
    message = str(excinfo.value)
    assert contracts.OPENXFACTORY_ROOT_ENV in message
    assert contracts.CONTRACT_TAG in message


# ---------------------------------------------------------------------------
# structural validation (hermetic)
# ---------------------------------------------------------------------------

def test_validators_are_draft202012_per_kind(fake_root, pinned_repo):
    from jsonschema import Draft202012Validator

    built = contracts.validators(fake_root, repo_root=pinned_repo)
    assert set(built) == set(contracts.WIRE_KINDS)
    assert all(isinstance(v, Draft202012Validator) for v in built.values())


def test_validators_are_cached_on_the_verified_digests(fake_root, pinned_repo):
    """T104 final queue Q-2 (ruled 2026-08-09): the 100 ms pre-dispatch p95
    target STANDS, so the COMPILED validators are reused across calls whose
    verified bytes are identical — the yaml parse, registry build, and
    jsonschema compilation stop being per-request. The key derives FROM the
    digests the per-call verification just proved, never from time or
    trust; the companion test below is the fail-closed half."""
    first = contracts.validators(fake_root, repo_root=pinned_repo)
    second = contracts.validators(fake_root, repo_root=pinned_repo)
    assert set(first) == set(second)
    for kind, validator in first.items():
        assert second[kind] is validator, kind


def test_the_cache_never_shortcuts_the_byte_verification(fake_root, pinned_repo):
    """The load-bearing half of the Q-2 ruling: a byte that drifts AFTER a
    cached resolution refuses on the very next call. The digests are
    re-verified against the released bytes on EVERY call; only compilation
    is amortized — a cache hit is possible only for bytes that just proved
    themselves."""
    contracts.validators(fake_root, repo_root=pinned_repo)   # warm the cache
    target = fake_root / "contracts" / "schemas" / CATALOG_SCHEMA_FILE
    target.write_bytes(target.read_bytes() + b"\n# drifted after caching\n")

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.validators(fake_root, repo_root=pinned_repo)
    assert CATALOG_SCHEMA_FILE in str(excinfo.value)


def test_the_manifest_parse_memo_never_serves_drifted_bytes(fake_root,
                                                            pinned_repo):
    """The memo's other input: the manifest's PARSE is reused only for bytes
    that hash identically. A manifest rewritten after a cached resolution is
    a NEW key — its disagreement with the schema bytes refuses on the very
    next call, exactly as it would have cold."""
    contracts.validators(fake_root, repo_root=pinned_repo)   # warm every memo
    manifest = fake_root / "contracts" / "manifest.yaml"
    drifted = manifest.read_text(encoding="utf-8").replace(
        contracts.SCHEMA_DIGESTS[CATALOG_SCHEMA_FILE], "0" * 64)
    manifest.write_text(drifted, encoding="utf-8")

    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.validators(fake_root, repo_root=pinned_repo)
    assert "manifest" in str(excinfo.value)


def test_valid_catalog_instance_validates(fake_root, pinned_repo):
    assert contracts.validate_instance(MINIMAL_CATALOG, fake_root,
                                       repo_root=pinned_repo) == []


def test_broken_catalog_instance_returns_schema_errors(fake_root, pinned_repo):
    broken = {
        "schema_version": 1,
        "kind": "workbench-model-catalog",
        "models": [{"model_id": "", "label": "Approved model"}],
        "api_key": "sk-not-a-public-field",
    }

    errors = contracts.validate_instance(broken, fake_root, repo_root=pinned_repo)
    assert errors
    assert all(isinstance(error, str) for error in errors)
    assert any("api_key" in error for error in errors)


def test_turn_kinds_select_their_own_envelope(fake_root, pinned_repo):
    """The chat-turn file's three envelopes are discriminated by kind, so a
    success body is checked against `success` and NOT against `request`."""
    success = {
        "schema_version": 1,
        "kind": "workbench-chat-turn-success",
        "assistant_prose": "considered the outline",
    }
    assert contracts.validate_instance(success, fake_root,
                                       repo_root=pinned_repo) == []

    mislabelled = dict(success, kind="workbench-chat-turn")
    assert contracts.validate_instance(mislabelled, fake_root,
                                       repo_root=pinned_repo)


def test_unknown_kind_fails_closed(fake_root, pinned_repo):
    with pytest.raises(contracts.ContractPinError) as excinfo:
        contracts.validate_instance({"kind": "workbench-chat-turn-partial"},
                                    fake_root, repo_root=pinned_repo)
    assert "workbench-chat-turn-partial" in str(excinfo.value)


def test_missing_kind_fails_closed(fake_root, pinned_repo):
    with pytest.raises(contracts.ContractPinError):
        contracts.validate_instance({"schema_version": 1}, fake_root,
                                    repo_root=pinned_repo)


def test_non_mapping_instance_fails_closed(fake_root, pinned_repo):
    with pytest.raises(contracts.ContractPinError):
        contracts.validate_instance(["workbench-model-catalog"], fake_root,
                                    repo_root=pinned_repo)


# ---------------------------------------------------------------------------
# delegated semantic validation (hermetic: a stub in the pinned checkout's slot)
# ---------------------------------------------------------------------------

STUB_VALIDATOR = """\
import sys
print("stub validated " + " ".join(sys.argv[1:]))
sys.exit({code})
"""


def _install_stub_validator(root: Path, code: int = 0) -> Path:
    scripts = root / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    path = scripts / "validate-ideation-dashboard-contracts.py"
    path.write_text(STUB_VALIDATOR.format(code=code), encoding="utf-8")
    return path


def test_delegation_runs_the_pinned_validator(fake_root, tmp_path):
    _install_stub_validator(fake_root)
    instance = tmp_path / "catalog.yaml"
    instance.write_text(yaml.safe_dump(MINIMAL_CATALOG), encoding="utf-8")

    returncode, output = contracts.delegated_semantic_validation([instance],
                                                                 fake_root)
    assert returncode == 0
    assert "stub validated" in output
    assert str(instance) in output


def test_delegation_returns_the_validators_findings_exit(fake_root, tmp_path):
    """The verdict is the pinned validator's, not ours — its exit code is
    reported, never re-derived here."""
    _install_stub_validator(fake_root, code=1)
    instance = tmp_path / "catalog.yaml"
    instance.write_text(yaml.safe_dump(MINIMAL_CATALOG), encoding="utf-8")

    returncode, _ = contracts.delegated_semantic_validation([instance], fake_root)
    assert returncode == 1


def test_delegation_without_the_pinned_validator_fails_closed(fake_root, tmp_path):
    instance = tmp_path / "catalog.yaml"
    instance.write_text(yaml.safe_dump(MINIMAL_CATALOG), encoding="utf-8")

    with pytest.raises(contracts.ContractPinError):
        contracts.delegated_semantic_validation([instance], fake_root)


# ---------------------------------------------------------------------------
# integration rung — the REAL released checkout, env-gated
# ---------------------------------------------------------------------------

@pytest.fixture
def released_root() -> Path:
    """The released checkout to read: `OPENXFACTORY_ROOT` when one is named,
    otherwise the hosting repository when it IS a release.

    The fallback is the point. This suite is hosted inside the publisher, so the
    released bytes are simply present and this rung has no reason to be opt-in —
    while it was, the publisher-mode refusal that killed both model routes sat
    green in CI (align-doxbench-contract-pin-to-publisher, 2026-08-10)."""
    declared = os.environ.get(contracts.OPENXFACTORY_ROOT_ENV)
    if declared:
        root = Path(declared)
    elif contracts.is_publisher_checkout(contracts.REPO_ROOT):
        root = contracts.REPO_ROOT
    else:
        pytest.skip("no released checkout: set OPENXFACTORY_ROOT, or run from a "
                    "publisher checkout")
    if not (root / "contracts" / "schemas").is_dir():
        pytest.skip(f"released checkout not provided (no contracts/schemas under {root})")
    return root


def _packaged_positives(root: Path) -> list[Path]:
    return sorted((root / "examples" / "ideation-dashboard")
                  .glob("workbench-*.example.yaml"))


def test_released_bytes_match_the_pinned_digests(released_root):
    for name, digest in contracts.SCHEMA_DIGESTS.items():
        path = released_root / "contracts" / "schemas" / name
        assert _sha256_file(path) == digest, name


def test_released_schemas_load_against_the_real_pin(released_root):
    schemas = contracts.load_released_schemas(released_root)
    assert set(schemas) == set(contracts.WIRE_KINDS)
    assert schemas["workbench-model-catalog"]["$id"] == CATALOG_SCHEMA_FILE
    assert schemas["workbench-chat-turn-failure"]["$ref"].startswith(
        CHAT_TURN_SCHEMA_FILE)


def test_packaged_positives_validate_structurally(released_root):
    positives = _packaged_positives(released_root)
    # 6 -> 7 at contract-v1.28: the release ADDS
    # workbench-chat-turn-outline-only.example.yaml, the instance proving a
    # null active_document_path is legal (G-1). 7 -> 9 at contract-v1.34, which
    # adds the widened family's loaded-set request and its record. 9 -> 10 at
    # contract-v1.38, which adds the `auto` ROUTING RULE instance. The exact
    # count IS the pin, so it advances with the release rather than being
    # loosened to an inequality.
    assert len(positives) == 10, [p.name for p in positives]

    for path in positives:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert contracts.validate_instance(doc, released_root) == [], path.name


def test_delegated_semantics_accept_the_packaged_positives(released_root):
    positives = _packaged_positives(released_root)
    returncode, output = contracts.delegated_semantic_validation(positives,
                                                                 released_root)
    assert returncode == 0, output


# ---------------------------------------------------------------------------
# THE ROUTING-RULE GROWTH IS ADDITIVE (contract-v1.38,
# add-doxbench-editing-phase-b task 11.7)
#
# Asserted against the REAL released bytes, through the same loader a serve
# uses, because the class claim ("nothing previously valid becomes invalid") is
# a claim about those bytes and not about a fixture. Each case below is one
# clause of the released `$defs/model_entry`: the two `if`s both require
# `routing_rule` to be PRESENT, and `dependentRequired` binds the three fields
# to each other.
# ---------------------------------------------------------------------------

_PLAIN_ENTRY = {
    "model_id": "plain-1",
    "label": "Approved authoring model",
    "provider_class": "on-tenant",
    "available": True,
    "input_limit_bytes": 2048,
    "output_limit_bytes": 8192,
    "data_handling": "Processed in the approved tenant boundary; no retention.",
}


def _catalog_instance(*models):
    return {"schema_version": 1, "kind": "workbench-model-catalog",
            "models": list(models)}


def _entry_with(**overrides):
    return {**_PLAIN_ENTRY, **overrides}


def test_the_pre_release_entry_shape_is_still_valid(released_root):
    """THE ADDITIVE TEST ITSELF: the entry every existing producer emits, with
    none of the three new fields, validates against the grown schema."""
    assert contracts.validate_instance(
        _catalog_instance(_PLAIN_ENTRY), released_root) == []


def test_a_routing_rule_entry_is_valid_against_the_released_bytes(released_root):
    rule = _entry_with(model_id="auto", routing_rule=True,
                       routes_to=["plain-1"], resolved_model_id="plain-1")
    assert contracts.validate_instance(
        _catalog_instance(rule, _PLAIN_ENTRY), released_root) == []


def test_the_released_schema_tolerates_a_producer_that_states_false_explicitly(
        released_root):
    """Additive means the wire accepts BOTH producers. This repository's own
    projection OMITS the three fields on a plain entry, but a consumer of this
    contract may not assume omission — an explicit `routing_rule: false` with no
    siblings is valid, and a reader that choked on it would be wrong."""
    assert contracts.validate_instance(
        _catalog_instance(_entry_with(routing_rule=False)), released_root) == []


@pytest.mark.parametrize("models, why", [
    ([_entry_with(model_id="auto", routing_rule=True)],
     "a rule with neither sibling"),
    ([_entry_with(model_id="auto", routing_rule=True, routes_to=["plain-1"])],
     "a rule with no resolved model"),
    ([_entry_with(resolved_model_id="plain-1")],
     "a plain entry that resolves elsewhere"),
    ([_entry_with(routes_to=["plain-1"])],
     "a plain entry with a routable set"),
    ([_entry_with(model_id="auto", routing_rule=False, routes_to=["plain-1"],
                  resolved_model_id="plain-1")],
     "an explicit non-rule carrying routing fields"),
    ([_entry_with(model_id="auto", routing_rule=True,
                  routes_to=["plain-1", "plain-1"],
                  resolved_model_id="plain-1")],
     "a repeated routable target"),
    ([_entry_with(model_id="auto", routing_rule=True, routes_to=[],
                  resolved_model_id="plain-1")],
     "an empty routable set"),
    ([_entry_with(provider_id="local-proxy")],
     "a harness provider id smuggled onto the entry (task 11.6's ruling)"),
])
def test_the_released_schema_refuses_a_malformed_routing_declaration(
        released_root, models, why):
    assert contracts.validate_instance(
        _catalog_instance(*models), released_root) != [], why


# ---------------------------------------------------------------------------
# THE V1 ENVELOPES ARE BYTE-IDENTICAL (contract-v1.34,
# add-doxbench-editing-phase-b task 13.1)
#
# The release ADDS a family beside the existing one rather than mutating a closed
# envelope, and "byte-identical" is the promise the CHANGELOG makes to every
# consumer pinned to the older shape. That promise is asserted against a
# COMMITTED BASELINE of those bytes -- not by re-validating an instance, which
# would still pass after a widened `maxItems` or a relaxed enum quietly changed
# what the old shape means.
#
# F1 (adversarial review of the §13 slice): the baseline covers the `$ref`
# CLOSURE, not the three envelope blocks alone. A v1 envelope is only as closed
# as what it points at -- `buffer_state.kind`'s two-value enum and
# `typed_proposal.target`'s are shared `$defs`, and they are exactly the
# constraints D15 contemplates widening. A guard over the three blocks alone went
# green while both enums were mutated, which is a change to v1's MEANING wearing
# the appearance of byte identity. The closure is COMPUTED here rather than
# listed, so a v1 envelope that grows a `$ref` to some new shared definition
# widens the guard with it instead of quietly escaping it.
# ---------------------------------------------------------------------------

V1_ENVELOPE_BASELINE = (
    Path(__file__).resolve().parent / "fixtures"
    / "chat-turn-v1-envelopes.baseline.yaml")


def _defs_order(schema_text: str) -> list[str]:
    """The `$defs` member names in FILE order, which is the order the committed
    baseline concatenates them in."""
    return list(_defs_blocks(schema_text))


def _defs_blocks(schema_text: str) -> dict[str, str]:
    """Every `$defs` member's EXACT source text, keyed by name.

    Split on indent-2 keys, with an indent-2 comment run attaching to the block
    it introduces rather than to the one above it -- otherwise a comment written
    before a NEW definition would appear to change the bytes of the definition
    before it, which is the opposite of what this file measures."""
    lines = schema_text.splitlines(keepends=True)
    blocks: dict[str, str] = {}
    name: str | None = None
    body: list[str] = []
    pending: list[str] = []
    for line in lines[lines.index("$defs:\n") + 1:]:
        stripped = line.strip()
        if line.startswith("  #") and not line.startswith("   "):
            pending.append(line)
            continue
        if (line.startswith("  ") and not line.startswith("   ")
                and stripped.endswith(":") and stripped[:-1].isidentifier()):
            if name is not None:
                blocks[name] = "".join(body)
            name, body, pending = stripped[:-1], [*pending, line], []
            continue
        body.extend(pending)
        pending = []
        body.append(line)
    if name is not None:
        blocks[name] = "".join(body)
    return blocks


def _local_refs(node, found):
    """Every `#/$defs/<name>` this node points at, at any depth."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str) and value.startswith("#/$defs/"):
                found.add(value.split("/")[-1])
            else:
                _local_refs(value, found)
    elif isinstance(node, list):
        for item in node:
            _local_refs(item, found)
    return found


def _v1_ref_closure(document):
    """The three v1 envelopes plus every `$def` reachable from them.

    Computed, never listed: a v1 envelope that starts pointing at a new shared
    definition must pull that definition under the byte guard automatically,
    because the alternative is a guard that silently stops covering what the
    envelope actually means."""
    defs = document["$defs"]
    closure: set[str] = set()
    frontier = {"request", "success", "failure"}
    while frontier:
        closure |= frontier
        following: set[str] = set()
        for name in frontier:
            following |= _local_refs(defs[name], set())
        frontier = following - closure
    return closure


def test_the_v1_envelope_bytes_are_unchanged_by_the_release(released_root):
    schema = (released_root / "contracts" / "schemas"
              / CHAT_TURN_SCHEMA_FILE).read_text(encoding="utf-8")
    blocks = _defs_blocks(schema)
    document = yaml.safe_load(schema)
    closure = _v1_ref_closure(document)
    # The closure is what it is BECAUSE of the refs; these names are asserted so
    # a closure computation that silently returned nothing cannot pass.
    assert closure >= {
        "request", "success", "failure",
        "content_hash", "confined_path", "scope_key", "buffer_state",
        "transcript_turn", "typed_proposal",
    }, sorted(closure)
    # The widened family's own definitions are NOT in it: they are new bytes
    # this release adds, and the promise is about the old shape.
    assert not (closure & {"request_v2", "success_v2", "failure_v2",
                           "buffer_key", "keyed_observed_hashes",
                           "keyed_typed_proposal", "selected_model"})
    covered = [name for name in _defs_order(schema) if name in closure]
    observed = "".join(blocks[name] for name in covered)
    baseline = V1_ENVELOPE_BASELINE.read_text(encoding="utf-8")
    assert observed == baseline, (
        "the v1 envelopes and the shared definitions they $ref are not "
        "byte-identical to the committed contract-v1.31 baseline; the release is "
        "additive, so any change here is a change to a shape consumers are "
        "pinned to -- including a widened enum in a SHARED definition, which "
        "changes what the old envelope means without touching its own block")


def test_the_widened_family_is_present_beside_the_unchanged_one(released_root):
    """The other half of the same claim: the file really did grow. A test that
    only checked the v1 bytes would pass on a file that never gained a widened
    envelope at all."""
    schema = (released_root / "contracts" / "schemas"
              / CHAT_TURN_SCHEMA_FILE).read_text(encoding="utf-8")
    blocks = _defs_blocks(schema)
    for envelope in ("request_v2", "success_v2", "failure_v2"):
        assert envelope in blocks, envelope
    document = yaml.safe_load(schema)
    # The file's own version does NOT move: nothing previously valid becomes
    # invalid, which is what makes this additive rather than breaking (D16).
    assert document["contract_schema_version"] == 1
    assert [ref["$ref"] for ref in document["oneOf"]] == [
        "#/$defs/request", "#/$defs/success", "#/$defs/failure",
        "#/$defs/request_v2", "#/$defs/success_v2", "#/$defs/failure_v2"]


def test_the_deprecation_records_its_removal_target(released_root):
    """Task 13.2: the v1 family is deprecated IN THIS RELEASE with the removal
    target recorded. Recorded OUTSIDE the envelopes, because a deprecation is a
    statement about a shape and editing the shape to say so would break the byte
    identity asserted above."""
    document = yaml.safe_load(
        (released_root / "contracts" / "schemas"
         / CHAT_TURN_SCHEMA_FILE).read_text(encoding="utf-8"))
    declared = document.get("deprecated_envelopes")
    assert declared, (
        "contract-v1.34 deprecates the v1 family, and the record lives in the "
        "schema itself so a consumer reading the bytes learns it without "
        "reading a CHANGELOG")
    recorded = {entry["kind"]: entry for entry in declared}
    assert set(recorded) == set(contracts.DEPRECATED_CHAT_TURN_KINDS)
    for kind, entry in recorded.items():
        assert entry["deprecated_in"] == "contract-v1.34"
        # Removal of a released shape is BREAKING, so it can only land at a
        # major -- and only after the full minor release of deprecation the
        # versioning policy requires, which this release is.
        assert entry["removal_target"] == "contract-v2.0"
        assert entry["superseded_by"] in contracts.CHAT_TURN_DEFS
        assert entry["superseded_by"] not in contracts.DEPRECATED_CHAT_TURN_KINDS
        assert kind in contracts.CHAT_TURN_DEFS
