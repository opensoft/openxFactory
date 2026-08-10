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

THE INTEGRATION RUNG is env-gated on `OPENXFACTORY_ROOT` and skips loudly when no
released checkout is provided. It is the only place the REAL contract-v1.28 bytes
are read: real digests, the six packaged workbench positives, and the delegated
openxFactory validator. Run it with

    OPENXFACTORY_ROOT=/workspace/projects/xFactory/openxFactory-worktrees/contract-v1.28

Every rule the shape cannot express belongs to the openxFactory validator, so
this suite never restates one: it asserts DELEGATION happened (the pinned script
was launched, its exit code was returned) and nothing about how it decides.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest
import yaml

from ideation_dashboard import doxbench_contracts as contracts

CATALOG_SCHEMA_FILE = "xfactory-workbench-model-catalog.schema.yaml"
CHAT_TURN_SCHEMA_FILE = "xfactory-workbench-chat-turn.schema.yaml"

RELEASED_REF = "ff64e81a967b75f92b3f5af9204aeb54c59a15d3"
RELEASED_TAG = "contract-v1.28"
RELEASED_DIGESTS = {
    CATALOG_SCHEMA_FILE:
        "0e6e7e946268b220918a426c6df399a9e01d064ee5dcbe22f8381dbf39aef1e0",
    CHAT_TURN_SCHEMA_FILE:
        "8386566ef881661659d38f6d6c27c723a7ddaf5dd3b8e18ead854c40a2a876bb",
}

# ---------------------------------------------------------------------------
# hermetic fixture world
#
# The fake schemas mirror the released files' STRUCTURE (a whole-document
# catalog; one chat-turn file holding three envelopes under `$defs`, selected by
# a `oneOf`), because the structure is what the loader's per-kind mapping and the
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
# below). OPEN ITEM (flagged in the change's task ledger): from a publisher
# checkout `load_release`'s stack-pin step raises, so serve's two doxbench
# model routes fail CLOSED until a ruled disposition for the publisher-side
# declaration lands.


def test_declared_wire_kinds_are_the_four_doxbench_instance_kinds():
    assert set(contracts.WIRE_KINDS) == {
        "workbench-model-catalog",
        "workbench-chat-turn",
        "workbench-chat-turn-success",
        "workbench-chat-turn-failure",
    }


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
    declared = os.environ.get("OPENXFACTORY_ROOT")
    if not declared:
        pytest.skip("released checkout not provided (set OPENXFACTORY_ROOT)")
    root = Path(declared)
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
    # null active_document_path is legal (G-1). The exact count IS the pin, so
    # it advances with the release rather than being loosened to an inequality.
    assert len(positives) == 7, [p.name for p in positives]

    for path in positives:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert contracts.validate_instance(doc, released_root) == [], path.name


def test_delegated_semantics_accept_the_packaged_positives(released_root):
    positives = _packaged_positives(released_root)
    returncode, output = contracts.delegated_semantic_validation(positives,
                                                                 released_root)
    assert returncode == 0, output
