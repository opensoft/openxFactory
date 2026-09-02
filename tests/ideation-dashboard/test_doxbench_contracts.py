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

# RE-PINNED at contract-v1.40 (add-doxbench-editing-phase-b §10.7), and the
# MIRROR IMAGE OF THE PREVIOUS REPIN, which was itself the mirror of v1.34's: at
# v1.38 the catalog digest moved and the chat-turn's did not; here the CHAT-TURN
# digest moves and the catalog's does not, because this release grows
# `$defs/success_v2` with the assembled context's posture.
#
# The REF carried the unresolved-until-published sentinel across the realization
# branch, on v1.34's and v1.38's own precedent — the policy publishes the
# annotated tag against the commit that LANDS, so until that commit existed
# there was nothing honest to name — and now names it: `contract-v1.40^{}` ==
# 671a6908, the squash-merge of PR #256, tag object 3c82f6b8, peeled FROM THE
# REMOTE. (v1.38's resolution was 58e4aecd: `contract-v1.38^{}` == 0f50b35, tag
# object 46cd169; v1.34's was 7c544c84.)
# RE-PINNED at contract-v1.45 (add-doxchat-model-intake 3.3/3.6): the
# chat-turn schema gained the optional `provider_retry` block, so its bytes
# moved and the consumer pin moved with them. The ref carries the
# realization SENTINEL until the tag is published against the commit that
# lands — the same posture the v1.40 cut carried across its own branch.
# RE-PINNED at contract-v2.2 (add-model-capability-vocabulary 4.2/4.4), and the
# MIRROR of v1.45: there the chat-turn digest moved and the catalog's did not,
# here the CATALOG digest moves and the chat-turn's does not, because this
# release grows `$defs/model_entry` with the optional closed `modalities`
# declaration.
#
# The REF carried the unresolved-until-published sentinel across the realization
# branch, on v1.34's, v1.38's and v1.40's precedent — the policy publishes the
# annotated tag against the commit that LANDS, so until that commit existed
# there was nothing honest to name — and now names it: `contract-v2.2^{}` ==
# 8ccfb67b, the squash-merge of PR #498, tag object f86f2212, peeled FROM THE
# REMOTE. The v1.45 sentinel it replaced was never resolved to a commit
# (that repin's own task 4.2 went undischarged); it was superseded rather than
# repaired, since these bytes no longer belong to that bundle.
#
# RE-PINNED at contract-v3.0 (retire-doxbench-chat-turn-v1 6.1, taken at the
# cut): the chat-turn schema's bytes moved since v2.2 — PR #564 removed the
# three v1 `$defs`, their `oneOf` refs and the `deprecated_envelopes` block —
# so the digest below is the post-removal file's and the catalog's is unmoved.
# The file's own `contract_schema_version` deliberately did NOT move (see
# `test_the_widened_family_is_the_only_one_the_file_declares` below, which
# carries the reasoning), so the cut re-LABELS this pin without re-deriving the
# digest. #564 moved the module's digest and knowingly left the LABEL at
# contract-v2.2, so between that merge and the cut the pin named a release
# these bytes do not belong to; the cut closes that.
#
# The REF carries the unresolved-until-published SENTINEL again, on v1.34's,
# v1.38's, v1.40's, v1.45's and v2.2's precedent: the policy publishes the
# annotated tag against the commit that LANDS, so until that commit exists
# there is nothing honest to name. The value is spelled so a consumer comparing
# against it REFUSES rather than matching by accident — and the mechanism is
# the PIN VALIDATOR rather than YAML: a repository can write the string, but
# `scripts/validate-domain-openxfactory-pins.py` requires a 40-character
# lowercase SHA for `contract_ref_type: commit`, so a stack carrying the
# sentinel fails its own pin check and one carrying anything else fails the
# equality check in `doxbench_contracts.verify_stack_pin`. Resolving it to
# `contract-v3.0^{}` is owed immediately after the tag is published — the v1.45
# residue is what that obligation exists to avoid repeating.
#
# RESOLVED 2026-09-02, the day of publication rather than three days after it.
# `contract-v3.0^{}` == ff9ed81541ab3eb2ebeb2e79676e5a875dd58064, the
# squash-merge of PR #573, from annotated tag object
# 59f4f51f2e0ac7c833cdaee9f385e9e83777650e, peeled FROM THE REMOTE in a second
# clone that never saw the tagging clone's tree. `verify-commit` at that commit
# and `verify-tag --remote origin --tag contract-v3.0` both pass with zero
# findings, and `verify-promotion` was taken green on the promoted squash BEFORE
# the tag existed (§ Bundle Realization Order step 4 — the step whose omission
# left `contract-v2.6` unpublishable). Evidence: PR #573 comment 5506503494.
#
# THE LITERAL IS SPELLED HERE rather than imported from the module, which is the
# same discipline `test_declared_wire_kinds_are_every_doxbench_instance_kind`
# states for the kind names: this file asserts WHAT THE PIN IS, not merely that
# the module agrees with itself. A resolution that edited only the module would
# turn this assertion red, and that is the assertion working.
RELEASED_REF = "ff9ed81541ab3eb2ebeb2e79676e5a875dd58064"
RELEASED_TAG = "contract-v3.0"
RELEASED_DIGESTS = {
    CATALOG_SCHEMA_FILE:
        "e563cc9fc6ede03dfd62537935d0ae0842617d7de46702aee6ad9026aa021635",
    CHAT_TURN_SCHEMA_FILE:
        "350bfedc02696e7281a42c0bdc9a25059bf7af14d16d89d9f07018d3e691dc1d",
}

# ---------------------------------------------------------------------------
# hermetic fixture world
#
# The fake schemas mirror the released files' STRUCTURE (a whole-document
# catalog; one chat-turn file holding the surviving THREE envelopes under
# `$defs`, selected by a `oneOf`), because the structure is what the loader's
# per-kind mapping and the registry-backed `$ref` resolution have to cope with.
# It read SIX until contract-v3.0 -- the three v1 envelopes and the three
# contract-v1.34 added beside them -- and the count moved with the removal
# (retire-doxbench-chat-turn-v1; Copilot review of the realization). Keeping the
# old count would have invited the next fixture edit to be written against a
# structure the release cannot produce, which is the same class of stale
# statement this whole retirement exists to correct.
# They deliberately do NOT
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

# THREE envelopes, not six: the v1 `request`/`success`/`failure` blocks left
# this fake with the release that removed them (contract-v3.0,
# retire-doxbench-chat-turn-v1). They are not merely unused here — `load_release`
# resolves one `$ref` per `CHAT_TURN_DEFS` entry INTO this file, so a fake still
# carrying kinds the module no longer declares would let the hermetic rung go on
# proving a dispatch shape the release cannot produce.
FAKE_CHAT_TURN_SCHEMA = """\
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "xfactory-workbench-chat-turn.schema.yaml"
oneOf:
  - $ref: "#/$defs/request_v2"
  - $ref: "#/$defs/success_v2"
  - $ref: "#/$defs/failure_v2"
$defs:
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
    """RE-PINNED at contract-v3.0 (retire-doxbench-chat-turn-v1): four kinds,
    the catalog plus the ONE surviving turn family.

    It was four at contract-v1.31, seven at contract-v1.34 when the widened
    family arrived beside the deprecated one, and four again now. The set is
    asserted EXACTLY, which is what makes this the test a reintroduced v1 kind
    fails — and the LITERALS are spelled here rather than read from the module,
    so this asserts what the wire is called and not merely that the module
    agrees with itself."""
    assert set(contracts.WIRE_KINDS) == {
        "workbench-model-catalog",
        "workbench-chat-turn-v2",
        "workbench-chat-turn-v2-success",
        "workbench-chat-turn-v2-failure",
    }


def test_no_deprecated_kind_register_survives_the_removal():
    """`test_the_v1_family_is_declared_deprecated_and_still_dispatchable` stood
    here and pinned the other half of contract-v1.34's bargain: the three v1
    kinds were in `DEPRECATED_CHAT_TURN_KINDS`, and every one of them still
    resolved to its own envelope, because the versioning policy's breaking path
    requires the old shape to keep working for at least one full published
    release. It was deleted with the family at contract-v3.0
    (retire-doxbench-chat-turn-v1), and this is what took its place.

    `DEPRECATED_CHAT_TURN_KINDS` is REMOVED rather than emptied, and this asserts
    that: an empty tuple would be a claim that nothing in this family is
    deprecated, which is a statement the consumer module has no business making
    on the release's behalf. The schema's own `deprecated_envelopes` block is the
    authority on what is deprecated, and it is read rather than restated."""
    assert not hasattr(contracts, "DEPRECATED_CHAT_TURN_KINDS")
    for retired in ("workbench-chat-turn", "workbench-chat-turn-success",
                    "workbench-chat-turn-failure"):
        assert retired not in contracts.WIRE_KINDS
        assert retired not in contracts.CHAT_TURN_DEFS


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
        ("workbench-chat-turn-v2", "request_v2"),
        ("workbench-chat-turn-v2-success", "success_v2"),
        ("workbench-chat-turn-v2-failure", "failure_v2"),
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
    success body is checked against `success_v2` and NOT against `request_v2`."""
    success = {
        "schema_version": 1,
        "kind": "workbench-chat-turn-v2-success",
        "assistant_prose": "considered the outline",
    }
    assert contracts.validate_instance(success, fake_root,
                                       repo_root=pinned_repo) == []

    mislabelled = dict(success, kind="workbench-chat-turn-v2")
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
    assert schemas["workbench-chat-turn-v2-failure"]["$ref"].startswith(
        CHAT_TURN_SCHEMA_FILE)


def test_packaged_positives_validate_structurally(released_root):
    positives = _packaged_positives(released_root)
    # 6 -> 7 at contract-v1.28: the release ADDS
    # workbench-chat-turn-outline-only.example.yaml, the instance proving a
    # null active_document_path is legal (G-1). 7 -> 9 at contract-v1.34, which
    # adds the widened family's loaded-set request and its record. 9 -> 10 at
    # contract-v1.38, which adds the `auto` ROUTING RULE instance — and 10 -> 11
    # within that release, for the rule-5' instance Brett's ruling made lawful
    # (a rule wider than a NON-resolved member). 11 -> 13 at contract-v1.40,
    # which adds the two CONTEXT POSTURE records: one reduced-with-its-reason
    # and one explicitly full. (The pre-release record that states NO posture is
    # the unchanged `workbench-chat-turn-v2-success` instance already counted
    # here — its continued validity is the additive claim, so the release adds
    # two files rather than three.) 14 -> 15 at contract-v2.2, which adds the
    # entry DECLARING `[text, image]`. The ABSENCE case needs no file of its
    # own: `workbench-model-catalog-local.example.yaml` is already counted here
    # and its continued validity IS the additive claim, exactly as the
    # no-posture record was at contract-v1.40. The exact count IS the pin, so it
    # advances with the release rather than being loosened to an inequality.
    #
    # 15 -> 11 at contract-v3.0 (retire-doxbench-chat-turn-v1), the first time
    # this count has gone DOWN. Four packaged v1 instances leave with the family
    # they demonstrate — `workbench-chat-turn-both-proposals`,
    # `-outline-only`, `-prose-only` and `-unsaved-edits`. There is nothing to
    # migrate them to: each was a positive for an envelope the release no longer
    # defines, and the surviving family's own claims (the loaded set, the record,
    # both context postures, the retry) are demonstrated by instances already
    # counted here. A kept v1 example would not merely be stale — the delegated
    # validator below would refuse it, because its kind resolves to no envelope.
    assert len(positives) == 11, [p.name for p in positives]

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


def test_the_types_target_cap_is_pinned_to_the_RELEASED_schemas_maxItems(
        released_root):
    """`MAX_ROUTING_TARGETS` is a literal in a module that imports only
    `dataclasses` and `typing` and so cannot read the schema. This is what makes
    it authoritative anyway: the bound is read out of the RELEASED BYTES here
    and pinned equal, so the two cannot drift into two caps (the hazard §12.2
    recorded for its own duplicated list, and the reason Codex's P2 asked for
    the bound by reference rather than a second literal)."""
    from ideation_dashboard.doxbench_model import (
        MAX_ROUTING_TARGETS, MODEL_REFERENCE_MAX_LENGTH, MODEL_REFERENCE_PATTERN)
    entry = _model_entry_subschema(released_root)
    routes_to = entry["properties"]["routes_to"]
    assert routes_to["maxItems"] == MAX_ROUTING_TARGETS
    # …and every other bound the type enforces on the same field, so a schema
    # change to any of them fails here rather than only in production.
    assert routes_to["minItems"] == 1
    assert routes_to["uniqueItems"] is True
    # THE ITEM BOUNDS (review N7). `routes_to`'s items and `resolved_model_id`
    # carry the same maxLength/pattern, and the type now enforces both; the
    # constants are pinned to the released bytes here rather than eyeballed.
    resolved = entry["properties"]["resolved_model_id"]
    for shape in (routes_to["items"], resolved):
        assert shape["maxLength"] == MODEL_REFERENCE_MAX_LENGTH
        assert shape["pattern"] == MODEL_REFERENCE_PATTERN
    # `model_id`'s bounds are IDENTICAL and the type ENFORCES them since
    # contract-v2.2 (review N7, closed by Brett's ALL-FIVE ruling). Pinned so
    # the sameness is a fact on the record rather than an assumption, and so
    # the one spelling `_require_model_reference` applies to all three stays
    # correct for all three.
    model_id = entry["properties"]["model_id"]
    assert model_id["maxLength"] == MODEL_REFERENCE_MAX_LENGTH
    assert model_id["pattern"] == MODEL_REFERENCE_PATTERN


def test_the_types_catalog_cap_is_pinned_to_the_RELEASED_schemas_maxItems(
        released_root):
    """`MAX_CATALOG_ENTRIES` mirrors `models.maxItems`, restated for the same
    reason `MAX_ROUTING_TARGETS` is and pinned the same way (contract-v2.2)."""
    from ideation_dashboard.doxbench_model import MAX_CATALOG_ENTRIES
    schema = yaml.safe_load(
        (released_root / "contracts" / "schemas" / CATALOG_SCHEMA_FILE)
        .read_text(encoding="utf-8"))
    assert schema["properties"]["models"]["maxItems"] == MAX_CATALOG_ENTRIES


def test_the_types_descriptive_string_bounds_are_pinned_to_the_RELEASED_schema(
        released_root):
    """The three bounds Brett's ALL-FIVE ruling added (contract-v2.2).

    Each is a literal in a module that cannot open the schema, so each is read
    out of the RELEASED BYTES here and pinned equal — the same discipline
    `MAX_ROUTING_TARGETS` got, applied to the three fields that carried a
    `maxLength` in the schema and a blankness check in the type."""
    from ideation_dashboard.doxbench_model import (
        DATA_HANDLING_MAX_LENGTH, LABEL_MAX_LENGTH, PROVIDER_CLASS_MAX_LENGTH)
    properties = _model_entry_subschema(released_root)["properties"]
    assert properties["label"]["maxLength"] == LABEL_MAX_LENGTH
    assert properties["provider_class"]["maxLength"] == PROVIDER_CLASS_MAX_LENGTH
    assert properties["data_handling"]["maxLength"] == DATA_HANDLING_MAX_LENGTH


def test_the_closed_modality_vocabulary_is_pinned_to_the_RELEASED_schema(
        released_root):
    """The contract-v2.2 vocabulary, read from the released bytes.

    `contains: {const: text}` is asserted here as well as the enum, because it
    is the clause that keeps the WIRE GATE from being the weakest one: without
    it the shape accepts `modalities: [image]`, which the catalog TYPE refuses.

    NOT "which the type and the validator both refuse" — the delegated validator
    restates no modality rule, so it refuses that instance by applying these
    very bytes. This clause is the whole file-side refusal, which is why it is
    pinned rather than assumed."""
    from ideation_dashboard.doxbench_model import (
        CATALOG_MODALITIES, REQUIRED_MODALITY)
    modalities = _model_entry_subschema(released_root)["properties"]["modalities"]
    assert tuple(modalities["items"]["enum"]) == CATALOG_MODALITIES
    assert modalities["contains"]["const"] == REQUIRED_MODALITY
    assert modalities["minItems"] == 1
    assert modalities["uniqueItems"] is True
    # OPTIONAL, and that is the additive property: absence must stay valid.
    entry = _model_entry_subschema(released_root)
    assert "modalities" not in entry["required"]


def test_EVERY_string_bound_the_released_schema_declares_is_enforced_at_construction(
        released_root):
    """THE NO-RESIDUE PROOF (contract-v2.2), driven from the released bytes
    rather than from a list of field names.

    The ratified requirement's last scenario says a field the schema bounds but
    the type does not is A DEFECT IN THE REQUIREMENT, not an accepted residue.
    A test that enumerated the four names could not detect a FIFTH bound added
    later, so this one walks `$defs/model_entry`, finds every string-valued
    property carrying a `maxLength` or a `pattern`, and drives one violating
    value through the real construction gate for each. A future release that
    bounds a new string field in the schema and forgets the type fails HERE.

    SCOPE, stated so the docstring does not claim more than the code drives:
    this walks the TOP-LEVEL string properties of `$defs/model_entry`. A bound
    added later under an array's `items` — the shape `routes_to` already has —
    or inside a nested object would not be reached. What IS airtight is the hard
    `assert set(bounded) == {…}` below: a new top-level bounded string cannot be
    added to the schema without failing here, which is the case this proof
    exists for. (`routes_to`'s own members ARE enforced, at
    `_validate_routing_declaration`; they are simply not driven by this test.)

    `resolved_model_id` is id-bearing and only constructible on a routing rule,
    so it is driven through one; every other bounded string is driven on a plain
    entry. Its refusal is raised BEFORE the `resolved_model_id not in
    routes_to` membership check, so this drives the bound and not that rule."""
    from ideation_dashboard.doxbench_model import (
        InvalidCatalogEntryError, ModelCatalogEntry)

    entry_schema = _model_entry_subschema(released_root)
    bounded = {
        name: shape for name, shape in entry_schema["properties"].items()
        if shape.get("type") == "string"
        and ("maxLength" in shape or "pattern" in shape)
    }
    # The four base-entry strings plus the id-bearing `resolved_model_id`.
    assert set(bounded) == {"model_id", "label", "provider_class",
                            "data_handling", "resolved_model_id"}, bounded

    def _construct(field, value):
        if field == "resolved_model_id":
            return ModelCatalogEntry(**{
                **_PLAIN_ENTRY, "model_id": "auto", "routing_rule": True,
                "routes_to": ["target-a"], "resolved_model_id": value})
        return ModelCatalogEntry(**{**_PLAIN_ENTRY, field: value})

    for field, shape in sorted(bounded.items()):
        if "maxLength" in shape:
            over = "a" * (shape["maxLength"] + 1)
            with pytest.raises(InvalidCatalogEntryError) as caught:
                _construct(field, over)
            # The refusal NAMES the measured length and the released maximum,
            # which is what the ratified scenario asks of it.
            assert str(shape["maxLength"]) in str(caught.value)
            assert str(len(over)) in str(caught.value)
        if "pattern" in shape:
            with pytest.raises(InvalidCatalogEntryError):
                _construct(field, "has space")

    # …and the ARRAY bound one level up, which the same requirement names.
    _assert_the_entry_count_cap_is_enforced(released_root)


def _assert_the_entry_count_cap_is_enforced(released_root):
    from ideation_dashboard.doxbench_model import (
        CatalogEntryCountError, ModelCatalog, ModelCatalogEntry)
    schema = yaml.safe_load(
        (released_root / "contracts" / "schemas" / CATALOG_SCHEMA_FILE)
        .read_text(encoding="utf-8"))
    cap = schema["properties"]["models"]["maxItems"]
    entries = tuple(
        ModelCatalogEntry(**{**_PLAIN_ENTRY, "model_id": f"m{i}"})
        for i in range(cap + 1))
    with pytest.raises(CatalogEntryCountError) as caught:
        ModelCatalog(entries)
    assert str(cap) in str(caught.value)
    assert str(cap + 1) in str(caught.value)
    # …and exactly at the cap it still constructs.
    assert len(ModelCatalog(entries[:cap]).entries) == cap


def _model_entry_subschema(released_root):
    schema = yaml.safe_load(
        (released_root / "contracts" / "schemas" / CATALOG_SCHEMA_FILE)
        .read_text(encoding="utf-8"))
    return schema["$defs"]["model_entry"]


def _entry_with_targets(n):
    """One ENTRY declaring `n` routable targets. Nothing else — the catalog-level
    caps are not this shape's business, which is the point."""
    return {**_PLAIN_ENTRY, "model_id": "auto", "routing_rule": True,
            "routes_to": [f"t{i}" for i in range(n)], "resolved_model_id": "t0"}


@pytest.mark.parametrize("count, valid", [(1, True), (63, True), (64, True),
                                          (65, False), (200, False)])
def test_the_routes_to_cap_boundary_holds_at_the_ENTRY_SUBSCHEMA(
        released_root, count, valid):
    """`routes_to.maxItems: 64` is a bound on ONE ENTRY, and this is the level at
    which the 64/65 boundary is actually true (review N6).

    It cannot be shown on a whole catalog: `models.maxItems` is also 64 and the
    rule occupies a slot, so a conformant catalog tops out at 63 targets. Testing
    the boundary against a full envelope would either fail for the wrong reason
    or quietly assert something weaker. So the entry subschema is validated
    directly — no `$ref`s inside it, so no registry is needed."""
    from jsonschema import Draft202012Validator
    validator = Draft202012Validator(_model_entry_subschema(released_root),
                                     format_checker=contracts.FORMAT_CHECKER)
    errors = list(validator.iter_errors(_entry_with_targets(count)))
    assert (errors == []) is valid, (count, [e.message for e in errors][:1])


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
# THE BYTE-IDENTITY BASELINE IS RETIRED (contract-v3.0,
# retire-doxbench-chat-turn-v1 task 5.1), AND THIS SAYS WHAT IT WAS FOR
#
# `test_the_v1_envelope_bytes_are_unchanged_by_the_release` stood here, with
# `V1_ENVELOPE_BASELINE`, `_v1_ref_closure`, `_local_refs` and `_defs_order`
# feeding it, and `tests/ideation-dashboard/fixtures/chat-turn-v1-envelopes.baseline.yaml`
# holding the bytes. It asserted that the three v1 `$defs` AND every shared
# definition they `$ref`-ed were byte-identical to their contract-v1.31 bytes.
#
# WHAT IT EXISTED TO DO. contract-v1.34 added the widened family BESIDE the v1
# one rather than mutating a closed envelope, and "byte-identical" was the
# promise the CHANGELOG made to every consumer pinned to the older shape. The
# guard asserted that promise against COMMITTED bytes rather than by
# re-validating an instance -- which would still have passed after a widened
# `maxItems` or a relaxed enum quietly changed what the old shape MEANT. Its F1
# hardening (adversarial review of the §13 slice) extended it from the three
# envelope blocks to their whole `$ref` CLOSURE, after a guard over the blocks
# alone went green while `buffer_state.kind`'s and `typed_proposal.target`'s
# enums were both mutated.
#
# WHY IT ENDS, AND WHY THAT IS NOT THE SAME AS BECOMING INCONVENIENT. The
# assertion protects a shape consumers are PINNED to. At contract-v3.0 that
# shape leaves the published surface, so the assertion has no subject: there are
# no v1 `$defs` left to compare, and `_v1_ref_closure` would raise a `KeyError`
# on its own seed rather than fail an assertion. A consumer pinned below
# contract-v3.0 keeps the promise it was given, and keeps it by the
# IMMUTABILITY OF THE BYTES ITS PIN NAMES rather than by their continued
# presence here -- compatibility flows from the consumer, and no new release
# reaches backwards into an old pin.
#
# Deleting it as an incidental casualty of a schema edit would have been
# indistinguishable from deleting it because it had become inconvenient, which
# is why the removal is stated here and named again in the CHANGELOG entry the
# cut writes (task 6.3). What replaces it, in kind, is
# `test_the_widened_family_is_the_only_one_the_file_declares` below: a v1
# envelope left behind by an incomplete removal fails THERE.
#
# `_defs_blocks` SURVIVES the retirement and is used by that test.
# ---------------------------------------------------------------------------

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


def test_the_widened_family_is_the_only_one_the_file_declares(released_root):
    """RE-EXPRESSED at contract-v3.0 (retire-doxbench-chat-turn-v1).

    It read `..._is_present_beside_the_unchanged_one` and was the other half of
    contract-v1.34's additive claim: a test that only checked the v1 bytes would
    pass on a file that never gained a widened envelope at all. There is nothing
    beside the widened family any more, so the claim it can still make is the
    stronger one — the `oneOf` is EXACTLY these three, in this order, so a v1
    envelope left behind by an incomplete removal fails here.

    The v1 envelopes' own bytes are a separate question with a separate test,
    which is where the retirement of the byte guard belongs."""
    schema = (released_root / "contracts" / "schemas"
              / CHAT_TURN_SCHEMA_FILE).read_text(encoding="utf-8")
    blocks = _defs_blocks(schema)
    for envelope in ("request_v2", "success_v2", "failure_v2"):
        assert envelope in blocks, envelope
    for retired in ("request", "success", "failure"):
        assert retired not in blocks, retired
    document = yaml.safe_load(schema)
    # The file's own version does NOT move. It did not move at contract-v1.34
    # because nothing previously valid became invalid (D16); it does not move
    # here for the opposite reason — the envelopes this file no longer defines
    # cannot be validated against it AT ALL, so there is no shape left for a
    # bumped `contract_schema_version` to describe. What changed is which
    # release a consumer pins, which is the major's own job.
    assert document["contract_schema_version"] == 1
    assert [ref["$ref"] for ref in document["oneOf"]] == [
        "#/$defs/request_v2", "#/$defs/success_v2", "#/$defs/failure_v2"]


def test_no_deprecation_record_outlives_the_envelopes_it_named(released_root):
    """`test_the_deprecation_records_its_removal_target` stood here and pinned
    contract-v1.34's task 13.2: a top-level `deprecated_envelopes` block naming
    each v1 kind, its successor, `deprecated_in: contract-v1.34` and a removal
    target. It is DELETED at contract-v3.0 (retire-doxbench-chat-turn-v1) because
    its whole subject was that block, and the block leaves with the kinds — a
    declaration that three envelopes this file no longer defines are deprecated
    names nothing.

    This is the negative that replaces it, and it is worth a test rather than a
    comment for one reason: a removal that took the envelopes and LEFT the block
    would still parse, still load, and still validate every surviving instance,
    so nothing else in this suite would notice. The consumer-side reader of the
    block is kept deliberately (`validate_ideation_dashboard_contracts`) — the
    next family to be deprecated will declare one, and a reader deleted with its
    only current input is a reader somebody re-derives from scratch."""
    document = yaml.safe_load(
        (released_root / "contracts" / "schemas"
         / CHAT_TURN_SCHEMA_FILE).read_text(encoding="utf-8"))
    assert "deprecated_envelopes" not in document


# ---------------------------------------------------------------------------
# THE FILE GATE AND THE TYPE GATE AGREE (contract-v1.38; adversarial review
# round 1 F2)
#
# The claim "the same rules are enforced at catalog construction" was in a
# docstring and was FALSE: `resolved_model_id ∈ routes_to` and the
# self-reference refusal existed only on the type, so the file gate was strictly
# weaker and the reviewer walked a catalog past it. It is now asserted over the
# packaged corpus, in both directions, so a rule added to one gate and forgotten
# in the other fails here instead of passing twice.
# ---------------------------------------------------------------------------

_ROUTING_NEGATIVE_GLOB = "workbench-model-catalog-routing-*.negative.yaml"


def _type_gate_refuses(doc) -> bool:
    """Construct the catalog through the real type. True when it refuses."""
    from ideation_dashboard.doxbench_model import (
        ModelCatalog, ModelCatalogEntry, ModelCatalogError,
    )
    try:
        ModelCatalog.from_entries(
            [ModelCatalogEntry(**entry) for entry in doc["models"]])
    except (ModelCatalogError, TypeError):
        return True
    return False


def _file_gate_errors(root: Path, path: Path) -> list:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "vidc_gate_parity", root / "scripts"
        / "validate-ideation-dashboard-contracts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    registry, docs = module.build_registry()
    findings = module.Findings()
    module.validate_instance(findings, path.name, module.load_yaml(path),
                             registry, docs, set(), model_ctx={})
    return findings.errors


def test_every_packaged_routing_negative_is_refused_by_BOTH_gates(released_root):
    negatives = sorted((released_root / "examples" / "ideation-dashboard"
                        / "negative").glob(_ROUTING_NEGATIVE_GLOB))
    # The exact count IS the pin, so it advances with the corpus rather than
    # being loosened to an inequality. TEN at contract-v1.38: the five rules'
    # own negatives (badge-gap, dangling-target, chained, unavailable-resolution,
    # wider-than-its-resolution), the FOUR the adversarial review contributed
    # (inverted-substring, incidental-word, resolved-outside-routes-to,
    # self-reference), and the separator-collision case the segment grammar
    # brought with it.
    assert len(negatives) == 10, [p.name for p in negatives]
    for path in negatives:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert _file_gate_errors(released_root, path) != [], (
            f"{path.name}: the FILE gate accepted it")
        assert _type_gate_refuses(doc), (
            f"{path.name}: the TYPE gate accepted it")


# Each packaged routing negative fails for ITS OWN NAMED reason in the file
# gate. This is the guard for the two arms revert-testing proved are DIAGNOSTIC
# rather than independent — the separator collision (the covering check would
# refuse it anyway, with a message that misdirects) and the self-reference (the
# chained-rule arm would refuse it anyway, calling it something else). Asserting
# the CODE is what keeps those arms honest; asserting mere refusal would not.
_EXPECTED_FINDING_CODE = {
    "workbench-model-catalog-routing-badge-gap": "routing-badge",
    "workbench-model-catalog-routing-badge-holds-the-separator": "routing-badge",
    "workbench-model-catalog-routing-badge-incidental-word": "routing-badge",
    "workbench-model-catalog-routing-badge-inverted-substring": "routing-badge",
    "workbench-model-catalog-routing-dangling-target": "routing-target",
    "workbench-model-catalog-routing-resolved-outside-routes-to": "routing-resolution",
    "workbench-model-catalog-routing-rule-chained": "routing-target",
    "workbench-model-catalog-routing-rule-unavailable-resolution": "routing-availability",
    "workbench-model-catalog-routing-rule-wider-than-its-resolution": "routing-limit",
    "workbench-model-catalog-routing-self-reference": "routing-self-reference",
}


def test_each_routing_negative_is_refused_for_its_OWN_named_reason(released_root):
    negatives = sorted((released_root / "examples" / "ideation-dashboard"
                        / "negative").glob(_ROUTING_NEGATIVE_GLOB))
    assert {p.name.replace(".negative.yaml", "") for p in negatives} == set(
        _EXPECTED_FINDING_CODE)
    for path in negatives:
        errors = _file_gate_errors(released_root, path)
        codes = {e.split("[", 1)[1].split("]", 1)[0] for e in errors}
        expected = _EXPECTED_FINDING_CODE[path.name.replace(".negative.yaml", "")]
        assert expected in codes, (path.name, sorted(codes))


def test_the_separator_collision_and_self_reference_name_their_real_cause(
        released_root):
    """The two diagnostic arms, pinned on their MESSAGES. Without these the
    arms could be deleted and every other test would stay green, because the
    covering rule and the chained-rule rule respectively refuse the same
    catalogs under different names."""
    base = released_root / "examples" / "ideation-dashboard" / "negative"
    separator = _file_gate_errors(
        released_root,
        base / "workbench-model-catalog-routing-badge-holds-the-separator.negative.yaml")
    assert any("segment separator" in e for e in separator), separator
    self_ref = _file_gate_errors(
        released_root,
        base / "workbench-model-catalog-routing-self-reference.negative.yaml")
    assert any("names ITSELF in routes_to" in e for e in self_ref), self_ref


# BOTH packaged routing positives, not just the first (review re-verify N4).
# The rule-5' instance was bound to the file gate by the example self-test and
# to the schema by the positives count, but nothing held it against the TYPE
# gate — and rule 5' is enforced in both places, so an accept that held on one
# side only would have gone unnoticed.
_ROUTING_POSITIVES = (
    "workbench-model-catalog-routing-rule.example.yaml",
    "workbench-model-catalog-routing-rule-wider-than-a-non-resolved-member.example.yaml",
)


@pytest.mark.parametrize("filename", _ROUTING_POSITIVES)
def test_the_packaged_routing_positives_are_accepted_by_BOTH_gates(
        released_root, filename):
    path = released_root / "examples" / "ideation-dashboard" / filename
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert contracts.validate_instance(doc, released_root) == []
    assert _file_gate_errors(released_root, path) == []
    assert not _type_gate_refuses(doc)


def test_every_packaged_routing_positive_is_covered_by_that_pin(released_root):
    """The table above is a list, so a positive added later could miss it. The
    corpus is the authority: every packaged `workbench-model-catalog-routing-*`
    positive must appear in `_ROUTING_POSITIVES`."""
    on_disk = {p.name for p in (released_root / "examples" / "ideation-dashboard")
               .glob("workbench-model-catalog-routing-*.example.yaml")}
    assert on_disk == set(_ROUTING_POSITIVES)


# ---------------------------------------------------------------------------
# THE CONTEXT-POSTURE GROWTH IS ADDITIVE (contract-v1.40,
# add-doxbench-editing-phase-b task 10.7)
#
# Asserted against the REAL released bytes, through the same loader a serve
# uses, for the reason the v1.38 block records: the class claim ("nothing
# previously valid becomes invalid") is a claim about those bytes and not about
# a fixture. Each case below is one clause of the released `$defs/context_packet`
# and of the optional property that references it.
# ---------------------------------------------------------------------------

_HASH_A = "74d2e440df9974e0c1d82412165e497bb95611142b3ed1235c0bd74b3c2277ba"
_HASH_B = "9859eb7d779f1dee12579980045bb94ecbc2cc487d8160aa239bc1bfe3416825"
_REASON = (
    "the staged-set knowledge service is unavailable, so this packet carries "
    "the selected thread and the loaded buffers only, with NO corpus evidence; "
    "no unbounded context was substituted and no rail was bypassed to reach a "
    "provider")


def _v2_record(**overrides):
    """The pre-release widened record — no `context_packet` at all."""
    record = {
        "schema_version": 1,
        "kind": "workbench-chat-turn-v2-success",
        "client_turn_id": "turn-v2-9001",
        "assistant_turn_id": "srv-v2-9001",
        "model_id": "local-authoring-1",
        "selected_model": {
            "requested_model_id": "local-authoring-1",
            "routing_rule": False,
            "data_handling": "Local process only; no content leaves this machine.",
        },
        "bound_buffer": "outline",
        "observed_hashes": {"outline": _HASH_A, "document": _HASH_B},
        "assistant_prose": "An answer.",
        "proposals": [],
    }
    record.update(overrides)
    return record


def test_the_pre_release_v2_record_is_still_valid(released_root):
    """THE ADDITIVE TEST ITSELF: the record every existing producer emits, with
    no posture at all, validates against the grown schema. Its ABSENCE is legal
    and says nothing about the posture — which is the sentence the manifest's
    consumption rule and the schema comment both carry, executed here."""
    assert contracts.validate_instance(_v2_record(), released_root) == []


@pytest.mark.parametrize("packet, why", [
    ({"posture": "full"}, "an explicitly full turn"),
    ({"posture": "reduced", "reduced_reason": _REASON}, "a reduced turn"),
    ({"posture": "reduced", "reduced_reason": "x"},
     "the shortest legal reason"),
    ({"posture": "reduced", "reduced_reason": "y" * 500},
     "the reason at its exact ceiling"),
])
def test_the_released_bytes_accept_a_conformant_posture(
        released_root, packet, why):
    assert contracts.validate_instance(
        _v2_record(context_packet=packet), released_root) == [], why


@pytest.mark.parametrize("packet, why", [
    ({"posture": "reduced"},
     "a reduction with no reason — the silent degradation, refused"),
    ({"posture": "full", "reduced_reason": _REASON},
     "a full posture carrying a reason — two facts, one record"),
    ({"posture": "degraded"}, "a posture outside the released vocabulary"),
    ({"posture": "Full"}, "the right posture in the wrong case"),
    ({}, "a posture object that states no posture"),
    ({"reduced_reason": _REASON}, "a reason with no posture"),
    ({"posture": "reduced", "reduced_reason": ""},
     "an empty reason, which is a reason nobody can read"),
    ({"posture": "reduced", "reduced_reason": "y" * 501},
     "a reason one byte past the released ceiling"),
    # PRESENCE, NOT TRUTHINESS, on the full arm — the boundary three of the
    # family's four gates accepted (Copilot review of PR #256, finding 1). The
    # shape refuses the KEY on a full posture, whatever it holds.
    ({"posture": "full", "reduced_reason": ""},
     "a full posture carrying a BLANK reason — the key is still present"),
    ({"posture": "full", "reduced_reason": None},
     "a full posture carrying a NULL reason — the key is still present"),
    ({"posture": "reduced", "reduced_reason": _REASON,
      "provider_id": "vertex-hosted"},
     "a fourth fact on a closed object"),
    ("reduced", "a bare string where the object belongs"),
    (None, "an explicit null, which is not an absent key"),
])
def test_the_released_bytes_refuse_a_malformed_posture(
        released_root, packet, why):
    assert contracts.validate_instance(
        _v2_record(context_packet=packet), released_root) != [], why


def test_each_conditional_guards_a_case_THE_OTHER_ONE_DOES_NOT(released_root):
    """THE S1-vs-S3 LESSON, read on this shape. contract-v1.38's growth carried
    a `dependentRequired` block AND two `if`-conditionals, and its review found
    they guard different paths — so a test that exercises one and assumes the
    other is covered proves nothing about the second.

    This release's two conditionals are the pairing's two halves, and they are
    NOT each other's inverse. Deleting `posture == reduced -> required
    [reduced_reason]` leaves the reason-on-full case still refused, and deleting
    `posture == full -> not required [reduced_reason]` leaves
    reduced-without-reason still refused: each case must therefore be shown
    against BOTH clauses present and each clause revert-tested on its own. The
    third case is the one NEITHER conditional touches — both require `posture`
    to equal a named constant, so an unknown posture matches neither `if` and is
    refused by the `enum` underneath them. A conditional guard cannot stand in
    for the value constraint it sits on top of."""
    schema = yaml.safe_load(
        (released_root / "contracts" / "schemas" / CHAT_TURN_SCHEMA_FILE)
        .read_text(encoding="utf-8"))
    definition = schema["$defs"]["context_packet"]
    # The two conditionals exist, and each names its own posture.
    postures = [clause["if"]["properties"]["posture"]["const"]
                for clause in definition["allOf"]]
    assert postures == ["reduced", "full"]
    # BOTH require `posture` to be PRESENT, which is what makes an object
    # missing it fall through to `required` rather than to a silently-passing
    # conditional.
    for clause in definition["allOf"]:
        assert clause["if"]["required"] == ["posture"]
    # …and the enum underneath them is the whole vocabulary, so the unknown
    # posture above is refused by a rule neither conditional can express.
    assert definition["properties"]["posture"]["enum"] == ["full", "reduced"]
    assert definition["additionalProperties"] is False
    assert definition["required"] == ["posture"]


def test_no_other_envelope_in_the_family_grows_a_posture(released_root):
    """THE BLAST RADIUS, pinned. Exactly ONE envelope gains the key. Every
    other envelope in this file is closed and refuses it, which is what makes
    "one optional property on one shape" a checkable claim rather than a
    description of intent.

    The DEPRECATED v1 success envelope was the third instance here until
    contract-v3.0 (retire-doxbench-chat-turn-v1): its refusal was what kept
    contract-v1.34's byte-identity promise checkable from this angle too. It is
    replaced by the surviving REQUEST, not dropped — the claim is about every
    other envelope in the family, and with three left the two that are not
    `success_v2` are exactly these two."""
    packet = {"posture": "reduced", "reduced_reason": _REASON}
    v2_request = {
        "schema_version": 1,
        "kind": "workbench-chat-turn-v2",
        "client_turn_id": "turn-9001",
        "scope": {"repository": "openxFactory", "ref": "main",
                  "tile_kind": "staged", "tile_id": "ideation-governance"},
        "bound_buffer": "outline",
        "working_subject": "the acceptance boundary",
        "message": "Which open question should we close next?",
        "model_id": "local-authoring-1",
        "last_assistant_turn_id": None,
        "transcript": [],
        "buffers": [],
        "context_packet": packet,
    }
    assert contracts.validate_instance(v2_request, released_root) != []
    v2_failure = {
        "schema_version": 1,
        "kind": "workbench-chat-turn-v2-failure",
        "client_turn_id": "turn-v2-9001",
        "error": "model_failed",
        "message": "The model could not answer this turn.",
        "context_packet": packet,
    }
    assert contracts.validate_instance(v2_failure, released_root) != []


_POSTURE_NEGATIVE_GLOB = "workbench-chat-turn-v2-context-*.negative.yaml"

# Each packaged posture negative fails for ITS OWN reason AT THE GATE THAT OWNS
# IT, and the table records WHICH gate rather than settling for "something
# refused it". The distribution is the release's design, stated:
#
#   * the two PAIRING violations are refused by BOTH the shape and the delegated
#     validator, with the `context-packet` finding code — that overlap is
#     deliberate and is what keeps the restatement honest (see
#     check_context_packet's docstring on why a file gate restates a rule the
#     shape can express);
#   * the unknown posture and the extra field are the SHAPE's alone, also
#     deliberately: the delegated validator restates neither an enum nor a
#     closure, because those are exactly what a schema is for;
#   * and the credential leak is the DELEGATED validator's alone, because the
#     shape cannot express it — `reduced_reason` is free prose and the leaking
#     instance is structurally perfect. It is the one negative in THIS TABLE
#     the shape must NOT catch; if it ever did, the rule would have stopped
#     being the shape's blind spot and this table would be lying about why the
#     rule exists.
#     CORRECTED (issue #263): this used to read "the one rule this release
#     delegates", which stopped being true when the NON-BLANK rule landed. That
#     rule is also undelegatable to the shape — `minLength: 1` counts
#     CHARACTERS and every blank class is one character — so the family now
#     delegates TWO. It has no packaged negative here because adding one would
#     touch the released example surface; it is asserted instead, across all
#     four gates and both runtimes, in test_doxbench_blank_reason.py.
#
# (shape refuses, expected file-gate finding code or None)
_POSTURE_NEGATIVE_GATES = {
    "workbench-chat-turn-v2-context-reduced-without-reason":
        (True, "context-packet"),
    "workbench-chat-turn-v2-context-reason-on-full":
        (True, "context-packet"),
    "workbench-chat-turn-v2-context-unknown-posture": (True, None),
    "workbench-chat-turn-v2-context-extra-field": (True, None),
    "workbench-chat-turn-v2-context-reason-leaks-a-credential":
        (False, "credential"),
    # The blank and the null on a FULL posture (Copilot review of PR #256,
    # finding 1). Both are refused by the shape for the KEY's presence, and both
    # are now refused by the delegated validator too — the blank always was, the
    # null was not, because that gate read the value where the shape reads the
    # key.
    "workbench-chat-turn-v2-context-empty-reason-on-full":
        (True, "context-packet"),
    "workbench-chat-turn-v2-context-null-reason-on-full":
        (True, "context-packet"),
}


def test_every_packaged_posture_negative_is_covered_by_that_pin(released_root):
    """The table above is a list, so a negative added later could miss it."""
    on_disk = {p.stem.replace(".negative", "") for p in
               (released_root / "examples" / "ideation-dashboard" / "negative")
               .glob(_POSTURE_NEGATIVE_GLOB)}
    assert on_disk == set(_POSTURE_NEGATIVE_GATES)


@pytest.mark.parametrize("stem, shape_refuses, code", sorted(
    (stem, shape, code)
    for stem, (shape, code) in _POSTURE_NEGATIVE_GATES.items()))
def test_each_packaged_posture_negative_is_refused_where_it_should_be(
        released_root, stem, shape_refuses, code):
    path = (released_root / "examples" / "ideation-dashboard" / "negative"
            / f"{stem}.negative.yaml")
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert bool(contracts.validate_instance(doc, released_root)) is shape_refuses, (
        f"{stem}: SHAPE expectation {shape_refuses!r}")
    errors = _file_gate_errors(released_root, path)
    if code is None:
        # The delegated validator stays out of it — but SOMETHING must refuse,
        # and that something is the schema check the file gate also runs.
        assert not [e for e in errors if "[context-packet]" in e], stem
        assert errors, f"{stem}: nothing refused it at all"
    else:
        assert [e for e in errors if f"[{code}]" in e], (
            f"{stem}: no {code!r} finding, got {errors}")


# The TYPE-GATE instance for each packaged pairing negative — one per stem,
# spelled out (review N-2). This used to be a two-branch conditional
# (`reduced-without-reason` or else `(FULL, _REASON)`), so the two negatives the
# bot round added both collapsed onto the SAME instance as the pre-existing
# one: four parameterisations constructing two distinct packets, reporting
# per-stem coverage it did not provide. The blank stem in particular — the exact
# instance the type used to accept — was never actually constructed here.
#
# `refuses=False` is not a gap being waved through, it is a REPRESENTATIONAL
# LIMIT stated: a Python attribute has no key/value distinction, so
# `reduced_reason=None` IS absence and there is no way to hand this constructor
# "the key, present, holding null". The instance the WIRE can express has no
# counterpart here, so the honest thing is to assert what the type really does
# with the nearest expressible input rather than to pretend otherwise.
_TYPE_GATE_INSTANCE = {
    # FULL stem -> (posture, reduced_reason, refuses). Keyed on the whole stem,
    # not a suffix: `-reason-on-full` is a suffix of `-empty-reason-on-full` and
    # of `-null-reason-on-full`, so suffix matching is ambiguous here — which
    # the companion test below caught on its first run, having been written to
    # catch exactly that.
    "workbench-chat-turn-v2-context-reduced-without-reason":
        ("reduced", None, True),
    "workbench-chat-turn-v2-context-reason-on-full":
        ("full", _REASON, True),
    "workbench-chat-turn-v2-context-empty-reason-on-full":
        ("full", "", True),
    "workbench-chat-turn-v2-context-null-reason-on-full":
        ("full", None, False),
}


@pytest.mark.parametrize("stem", sorted(
    s for s, (_shape, code) in _POSTURE_NEGATIVE_GATES.items()
    if code == "context-packet"))
def test_the_pairing_negatives_are_refused_by_the_PACKET_TYPE_TOO(stem):
    """THE THIRD GATE. `ContextPacket.__post_init__` refuses the pairing
    violations at construction, which is why no shipped path can produce one —
    and asserting it HERE, beside the shape and the file gate, is what makes
    "three gates, one rule" evidence rather than a claim in a docstring. It is
    the same parity discipline contract-v1.38's review had to add after finding
    its file gate strictly weaker than its type gate.

    ONE STEM IS ASSERTED AS ACCEPTED, and that is the honest reading rather than
    a hole: `-null-reason-on-full` names an instance only a WIRE format can
    express (a key that is present and holds null), and a Python attribute
    cannot hold it — `reduced_reason=None` is absence. The shape and the
    delegated validator refuse that instance and are pinned doing so above; what
    the type owns is the PRESENCE rule over the inputs it can actually receive,
    and `test_the_construction_gate_and_the_derivation_agree_on_PRESENCE` is the
    faithful pin for it."""
    from ideation_dashboard import doxbench_packet as pk
    from ideation_dashboard.doxbench_scope import ScopeKey

    posture, reason, refuses = _TYPE_GATE_INSTANCE[stem]
    scope = ScopeKey(repository="fixture-repo", ref="main",
                     tile_kind="staged", tile_id="t")

    def _construct():
        return pk.ContextPacket(
            purpose=pk.PACKET_PURPOSE_CHAT_TURN, scope=scope, posture=posture,
            sources=(), issued_at=0.0, expires_at=1.0, reduced_reason=reason)

    if refuses:
        with pytest.raises(pk.PacketError):
            _construct()
    else:
        assert _construct().posture == posture


def test_every_pairing_negative_has_its_OWN_type_gate_instance():
    """The table above is a map, so a stem added later could fall through it —
    and the silent fallthrough is exactly the defect N-2 found. Every stem the
    parametrization drives must match exactly one entry, and no two stems may
    share an instance."""
    stems = [s for s, (_shape, code) in _POSTURE_NEGATIVE_GATES.items()
             if code == "context-packet"]
    assert set(stems) == set(_TYPE_GATE_INSTANCE), (
        f"table and corpus disagree: {set(stems) ^ set(_TYPE_GATE_INSTANCE)}")
    instances = [_TYPE_GATE_INSTANCE[stem] for stem in stems]
    assert len(set(instances)) == len(stems), (
        f"two stems share one instance: {dict(zip(stems, instances))}")
