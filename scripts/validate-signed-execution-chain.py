#!/usr/bin/env python3
"""Validate the signed-execution-chain contract family, and WALK THE SHORT CHAIN.

The openxFactory-owned canonical validator for the four kinds
`xfactory_signed_execution_chain_inception`,
`xfactory_signed_execution_chain_traveling_contract`,
`xfactory_signed_execution_chain_log_leaf` and
`xfactory_signed_execution_chain_conformance_declaration`
(`contracts/signed-execution-chain/*.schema.yaml`). Run from the pinned
openxFactory checkout, never copied into a domain repo:

    python3 scripts/validate-signed-execution-chain.py [REPO_PATH] [--strict] \\
        [--require-pinned-wallet-vocabulary]

THIS FILE IS THE NAMED READER. The capability's own ninth requirement is that it
confers and refuses NOTHING until a named validator that reads its records runs
as a REQUIRED check on the repository that holds them — so this validator is not
a description of a control, it IS the control. IN THIS REPOSITORY IT IS NOW THAT
CHECK: `signed-execution-chain-gate` has been REQUIRED on `main` since 2026-08-31
(opensoft org ruleset 21957695), and a deliberately broken chain was seen failing
a real pull request before the packaged declaration was allowed to say so (canary
#549). The rule this file enforces is unchanged and still applies to every OTHER
realization: a declaration recording the reader unrequired gets the standing
`reader-not-required` warning on every run, and may not record SEC-R9 satisfied.

Two layers run:

1. Packaged reference corpus (`contracts/signed-execution-chain/examples/`):
   every `*.example.yaml` must pass schema conformance AND every chain rule; every
   file under `negative/` must FAIL for its INTENDED reason, declared in its own
   `# expected_failure:` header and optionally pinned further by an
   `# expected_failure_detail:` substring, because a finding CODE alone is too
   coarse an anchor for some rules. THE NEGATIVES ARE EVALUATED IN THE POSITIVE
   CORPUS'S SCOPE, with the fixture added to it: a refusal of a CHAIN is a
   property of a SET of records — a missing link, a reused per-act value, a leaf
   that commits to another chain — and a fixture adjudicated alone could not
   express one. A negative fixture that introduces a chain of its own therefore
   also draws the completeness findings its own incompleteness earns; that is the
   rules working, and the expected code is what the self-test pins.
2. Optional real artifacts under REPO_PATH: every `*.y*ml` whose top-level `kind`
   is one of the ELEVEN family kinds — or one of the THREE CONSUMED
   `add-trust-anchor` kinds a tier-2 issuance composes, which the sweep collects
   into the scope exactly as the packaged corpora load them — is validated, and
   the whole set is walked as chains. Other kinds are skipped and counted. BOTH
   families' packaged `examples/` trees are excluded, this one's and
   trust-anchor's, because the negatives there are deliberately invalid and each
   family's layer 1 already asserts exactly how; the SAME BYTES at a live path
   are adjudicated, which is the difference the exclusion draws.
   ZERO REAL ARTIFACTS IS THE EXPECTED STATE UNTIL
   THE FIRST RATIFICATION IS INCEPTED UNDER THIS CAPABILITY — inception is a
   human act with a wallet-held key, and this realization mints no chain.

THE EIGHT ORDERED CHECKS the gate walks over links 1-3, in the delta's own order,
each one reported under a CLOSED refusal code:

  1. the ratification's signature VERIFIES (ed25519, over the canonical bytes of
     `signed_ratification`);
  2. the digest of the SIGNED RATIFICATION, RECOMPUTED under the one construction
     in force, EQUALS the carried chain identity — over the signed bytes, never
     over the ratified subject;
  3. the exercise that proved link 1 carries an `object_ref` equal to the
     ratification's CONTENT digest, taken over the subject ratified — a DIFFERENT
     comparison over a DIFFERENT subject, which is the replay check and not the
     identity check;
  4. the inception leaf commits to that same chain identity;
  5. the traveling contract's carried chain identity and carried leaf digest EQUAL
     the values established above;
  6. the ACTOR the chain records is bound to the wallet that signed;
  7. the exercise's PROOF OF POSSESSION was supplied AND verified, and its outcome
     is the authenticated one;
  8. the STANDING of the authority was current AT EXERCISE, and the HOLDER CLASS
     is one this capability admits for a RATIFYING act — a named human, never an
     agent, runner, lane or workflow identity.

CHECKS 2 AND 3 ARE NEVER COLLAPSED. Equating the content digest with the chain
identity rejects every conforming chain, because the signed bytes are a strict
superset of the ratified subject; it is unbuildable in the other direction too,
since an exercise's `object_ref` would have to commit to a signature not yet made.
A record that equates them is refused by name.

FOUR RULES THE GATE DOES NOT WALK, because a gate sees only chains that were
incepted and only the chain in front of it. They are enforced over the SCOPE, and
they are named here so their absence from the eight is decided rather than
overlooked:

  (i)   ATOMICITY — a ratification leaf whose act was never inscribed is a
        ratified-but-uninscribed half-state, and no partial state may be retained
        that a later reader could mistake for a ratification.
  (ii)  PER-RATIFICATION UNIQUENESS — an inception whose per-act value is already
        consumed by an existing chain is refused. The value is NAMED, not minted:
        it is the identifier of the grant exercise that proved link 1. The pinned
        schema constrains no reuse, so this capability enforces it.
  (iii) THE LOG'S APPEND-ONLY PROPERTY — leaf indices, tree sizes and the hash
        link between consecutive leaves are a STORE obligation over the whole log,
        not a per-chain check.
  (iv)  THE REALIZATION CONFORMANCE DECLARATION — closed over the capability's
        nine obligations in both directions, with the two residuals this tranche
        cannot close refused the word `satisfied`.

WHAT THIS VALIDATOR DOES NOT DO. It creates no chain, mints no identity, holds no
key, and reaches no network. It defines no anchor, witness, commitment or receipt
— those are the named tranche-three successor — and no attestation identity,
which is tranche two. It verifies `ed25519` and refuses `ecdsa-p256` and
`ecdsa-secp256k1` as UNEVALUABLE rather than accepting a signature it did not
check.

Exit codes: 0 ok, 1 findings, 2 harness error.
"""
from __future__ import annotations

import argparse
import base64
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
except ImportError:  # pragma: no cover
    print("ERROR jsonschema>=4.18 and referencing are required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.signed_execution_chain import canonical  # noqa: E402
from scripts.signed_execution_chain import ed25519  # noqa: E402
from scripts.signed_execution_chain import attestation  # noqa: E402

CONTRACT_DIR = ROOT / "contracts" / "signed-execution-chain"
EXAMPLES_DIR = CONTRACT_DIR / "examples"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"
ACTOR_SUBJECT_SCHEMA = (
    ROOT / "contracts" / "identity-brokering" / "actor-subject-reference.schema.yaml")
PINNED_WALLET_DIR = ROOT / "openXwallet" / "contracts" / "openxwallet"

SCHEMA_FILENAMES = [
    "digest-construction.schema.yaml",
    "chain-inception.schema.yaml",
    "traveling-contract.schema.yaml",
    "transparency-log-leaf.schema.yaml",
    "conformance-declaration.schema.yaml",
    # --- tranche two (`add-chain-attestation`) ---
    "attestation-common.schema.yaml",
    "setup-attestation.schema.yaml",
    "commitment-extension.schema.yaml",
    "signed-chain-binding.schema.yaml",
    "runner-attestation.schema.yaml",
    "pr-open-decision.schema.yaml",
    "closure-record.schema.yaml",
    "remediation-declaration.schema.yaml",
]

KIND_TO_SCHEMA = {
    "xfactory_signed_execution_chain_inception": "chain-inception.schema.yaml",
    "xfactory_signed_execution_chain_traveling_contract": "traveling-contract.schema.yaml",
    "xfactory_signed_execution_chain_log_leaf": "transparency-log-leaf.schema.yaml",
    "xfactory_signed_execution_chain_conformance_declaration":
        "conformance-declaration.schema.yaml",
    # --- tranche two's SEVEN record kinds ---
    "xfactory_signed_execution_chain_setup_attestation":
        "setup-attestation.schema.yaml",
    "xfactory_signed_execution_chain_commitment_extension":
        "commitment-extension.schema.yaml",
    "xfactory_signed_execution_chain_chain_binding":
        "signed-chain-binding.schema.yaml",
    "xfactory_signed_execution_chain_runner_attestation":
        "runner-attestation.schema.yaml",
    "xfactory_signed_execution_chain_pr_open_decision":
        "pr-open-decision.schema.yaml",
    "xfactory_signed_execution_chain_closure_record":
        "closure-record.schema.yaml",
    "xfactory_signed_execution_chain_remediation_declaration":
        "remediation-declaration.schema.yaml",
}

# THE CONSUMED `add-trust-anchor` VOCABULARY, admitted into the scope and NEVER
# REDEFINED HERE. Tranche two's tier-2 issuance COMPOSES three records — the
# canonical certificate record for the public-key fingerprint and the validity
# bounds, the canonical issuance evidence for the issuance act, and this
# capability's own signed chain binding — so a reader that could not see the first
# two could not run the composition at all. They are validated against
# `contracts/trust-anchor/`'s own schemas, exactly as carried wallet blocks are
# validated against the pinned openXwallet shapes.
CONSUMED_KIND_TO_SCHEMA = {
    "xfactory_certificate_record": "certificate-record.schema.yaml",
    "xfactory_certificate_issuance_evidence": "issuance-evidence.schema.yaml",
    "xfactory_trust_anchor": "trust-anchor.schema.yaml",
}
TRUST_ANCHOR_DIR = ROOT / "contracts" / "trust-anchor"
CUSTODY_REGISTRY = TRUST_ANCHOR_DIR / "trust-anchor-chain-custody.registry.yaml"

# The pinned openXwallet schemas the carried blocks are validated against when the
# `openXwallet/` gitlink is present. NEVER vendored: the pin
# (`contracts/openxwallet-pin.yaml`) is the consumption contract, and a second
# copy of a pinned schema is the drift the pin exists to prevent.
PINNED_WALLET_SCHEMAS = {
    "exercise": "openxwallet-grant-exercise.schema.yaml",
    "wallet": "openxwallet-record.schema.yaml",
    "attestation": "openxwallet-subject-attestation.schema.yaml",
}

# THE CLOSED REFUSAL ENUMERATION, held here as the set the packaged corpus must
# probe. It is the same enumeration the transparency-log leaf's
# `verdict.refusal.code` declares; the self-test refuses a code with no probe, so
# a refusal this validator can emit and no fixture ever provokes cannot ship.
REFUSAL_CODES = frozenset({
    "missing_proof_of_possession",
    "proof_verification_failed",
    "exercise_object_ref_absent",
    "exercise_replayed",
    "presentation_signed_over_not_request_digest",
    "authority_revoked_at_exercise",
    "actor_wallet_mismatch",
    "actor_resolved_through_wallet",
    "ratified_but_uninscribed",
    "orphan_chain_identity",
    "per_act_value_reused",
    "inception_not_out_of_pipeline",
    "digest_construction_mismatch",
    "content_digest_equated_with_chain_identity",
    "traveling_contract_digest_mismatch",
    "continuity_broken",
    "missing_link",
    "act_unproven",
    "leaf_hash_link_broken",
    "leaf_signature_invalid",
    "residual_not_declared",
    "chain_unevaluable",
    "machine_holder_as_ratifying_authority",
    "ratification_signature_invalid",
}) | attestation.REFUSAL_CODES

# The capability's obligations, in the delta's order. NINE at tranche one;
# SEC-R10..SEC-R18 are tranche two's nine, held in the module that enforces them.
TRANCHE_ONE_OBLIGATIONS = ["SEC-R1", "SEC-R2", "SEC-R3", "SEC-R4", "SEC-R5",
                           "SEC-R6", "SEC-R7", "SEC-R8", "SEC-R9"]
OBLIGATIONS = TRANCHE_ONE_OBLIGATIONS + attestation.OBLIGATIONS
# The two whose residual is STRUCTURAL at this tranche: the pinned exercise record
# carries no field holding the SIGNED digest value (SEC-R1), and suffix truncation
# no party has yet observed is invisible to a log with no external witness
# (SEC-R6). Neither may be recorded `satisfied`.
STRUCTURAL_RESIDUALS = {"SEC-R1", "SEC-R6"}

# Requirement 8, as Brett Heap's Narrowing A ruling of 2026-08-29 settled it: tier
# 1 is RATIFYING authority, held by a NAMED HUMAN. `agent` is the machine holder
# the ruling refuses for a ratifying act — agent-held REVIEW wallets stay lawful,
# and this validator never sees one, because reviewing is not incepting a chain.
# `organisation` is refused for the other half of the same sentence: a body is not
# a named human either.
HUMAN_HOLDER_CLASSES = frozenset({"person", "practitioner"})

# The only algorithm this realization VERIFIES. The other two members of the
# shipped enumeration are refused as unevaluable rather than accepted unchecked.
VERIFIABLE_ALGORITHM = "ed25519"

LEAF_TYPES = ("wallet_presented_ratification", "chain_inception",
              "traveling_contract_issued", "gate_verdict",
              # Tranche two: one leaf type per record kind it defines, written
              # into the SAME log — the walk is over the records the log holds
              # in the order it holds them.
              "setup_attestation", "commitment_extension",
              "signed_chain_binding", "runner_attestation",
              "pr_open_decision", "closure_record",
              "remediation_declaration")

CHECK_NAMES = (
    "ratification_signature_verifies",
    "chain_identity_recomputes",
    "exercise_object_ref_is_content_digest",
    "inception_leaf_commits_to_chain_identity",
    "traveling_contract_carries_established_values",
    "actor_bound_to_signing_wallet",
    "proof_of_possession_supplied_and_verified",
    "standing_and_holder_class_at_exercise",
)

# date/date-time enforced, not merely annotated. jsonschema registers the
# date-time checker only when rfc3339-validator is importable, so a bare
# environment would silently accept malformed timestamps — fail closed instead of
# validating vacuously.
FORMAT_CHECKER = FormatChecker()
if not {"date", "date-time"} <= set(FORMAT_CHECKER.checkers):  # pragma: no cover
    print(
        "ERROR jsonschema is missing its date/date-time format checkers; install "
        "rfc3339-validator (see requirements/hermes-runtime-contracts.in) so "
        "`format: date` and `format: date-time` are enforced",
        file=sys.stderr,
    )
    sys.exit(2)

BASE64URL_RX = re.compile(r"^[A-Za-z0-9_-]+$")


# --------------------------- findings ---------------------------

@dataclass
class Findings:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"ERROR [{code}] {msg}")

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"WARN  [{code}] {msg}")

    def note(self, msg: str) -> None:
        line = f"note  {msg}"
        if line not in self.notes:  # notes are facts about the run, not events
            self.notes.append(line)


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_records(path: Path) -> list[Any]:
    """A fixture may carry MORE THAN ONE record, `---`-separated.

    Not a convenience: several of this capability's refusals are properties of a
    SET rather than of a document — link 3 absent, a per-act value already
    consumed, a leaf that commits to another chain — and a probe for "an inception
    whose act was recorded in a leaf but that carries no traveling contract"
    cannot be written at all if a fixture is one record. Single-document files
    load unchanged."""
    with path.open(encoding="utf-8") as handle:
        return [doc for doc in yaml.safe_load_all(handle) if doc is not None]


# --------------------------- schema registry ---------------------------

def build_registry() -> tuple[Registry, dict[str, dict]]:
    """Offline registry over the family's schemas plus the in-tree
    `actor_subject_reference`, so the cross-file `$ref`s into
    `digest-construction.schema.yaml` and `chain-inception.schema.yaml` resolve.
    Each schema is registered under BOTH its absolute `$id` and its filename, so
    the bundle resolves identically here and in a consumer's stock validator."""
    resources: list[tuple[str, Resource]] = []
    docs: dict[str, dict] = {}
    for name in SCHEMA_FILENAMES:
        doc = load_yaml(CONTRACT_DIR / name)
        docs[name] = doc
        resource = Resource.from_contents(doc, default_specification=DRAFT202012)
        resources.append((name, resource))
        if doc.get("$id"):
            resources.append((doc["$id"], resource))
    return Registry().with_resources(resources), docs


def load_carried_schemas(f: Findings, required: bool) -> dict[str, dict]:
    """The vocabularies a carried block is validated against.

    `actor_subject_reference` lives in this repository and is always available.
    The three openxWallet schemas are reachable only through the `openXwallet/`
    gitlink; when it is absent this validator says so and falls back to the
    members it RESTRICTS, and `--require-pinned-wallet-vocabulary` turns that
    fallback into a refusal. The gate passes the flag: a check that silently
    validates less than it claims is the vacuous pass this family already refuses
    once, for the wallet intake register."""
    carried: dict[str, dict] = {}
    if ACTOR_SUBJECT_SCHEMA.is_file():
        carried["actor_subject_reference"] = load_yaml(ACTOR_SUBJECT_SCHEMA)
    else:  # pragma: no cover - the file is tracked in this repository
        f.error("carried-vocabulary",
                f"{ACTOR_SUBJECT_SCHEMA} not found; the actor reference cannot be "
                f"validated against the vocabulary that owns it")
    # The CONSUMED `add-trust-anchor` shapes live in THIS repository, so they are
    # loaded before the pinned-wallet fallback returns: tranche two's composed
    # issuance is unverifiable without them whatever the `openXwallet/` gitlink is
    # doing.
    for consumed_kind, consumed_name in CONSUMED_KIND_TO_SCHEMA.items():
        consumed_path = TRUST_ANCHOR_DIR / consumed_name
        if consumed_path.is_file():
            carried[consumed_kind] = load_yaml(consumed_path)
        else:  # pragma: no cover - the files are tracked in this repository
            f.error("carried-vocabulary",
                    f"{consumed_path} not found; tranche two's composed tier-2 "
                    f"issuance cannot be verified against the vocabulary that owns "
                    f"it")
    missing = [name for name in PINNED_WALLET_SCHEMAS.values()
               if not (PINNED_WALLET_DIR / name).is_file()]
    if missing:
        message = (
            f"the pinned openXwallet vocabulary is not present at "
            f"{PINNED_WALLET_DIR.relative_to(ROOT)} ({', '.join(sorted(missing))}); "
            f"carried wallet blocks are checked against the members this "
            f"capability RESTRICTS and not against the shipped shapes. Run "
            f"`git submodule update --init openXwallet`")
        if required:
            f.error("pinned-wallet-vocabulary-unavailable", message)
        else:
            f.note(message)
        return carried
    for key, name in PINNED_WALLET_SCHEMAS.items():
        carried[key] = load_yaml(PINNED_WALLET_DIR / name)
    f.note(f"pinned openXwallet vocabulary read from "
           f"{PINNED_WALLET_DIR.relative_to(ROOT)}: carried exercise, wallet and "
           f"subject-attestation blocks validated against the shipped schemas")
    return carried


def schema_errors(doc: Any, schema: dict, registry: Registry | None = None
                  ) -> list[str]:
    validator = Draft202012Validator(
        schema, registry=registry, format_checker=FORMAT_CHECKER) \
        if registry is not None else \
        Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
    return [f"{'/'.join(str(part) for part in err.path) or '<root>'}: {err.message}"
            for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path))]


# --------------------------- the scope ---------------------------

@dataclass
class Chain:
    """Everything in scope that claims one chain identity."""
    chain_id: str
    inception: tuple[str, dict] | None = None
    traveling: list[tuple[str, dict]] = field(default_factory=list)
    leaves: list[tuple[str, dict]] = field(default_factory=list)


@dataclass
class Scope:
    records: list[tuple[str, dict]]
    inceptions: list[tuple[str, dict]] = field(default_factory=list)
    travelings: list[tuple[str, dict]] = field(default_factory=list)
    leaves: list[tuple[str, dict]] = field(default_factory=list)
    declarations: list[tuple[str, dict]] = field(default_factory=list)
    consumed: list[tuple[str, dict]] = field(default_factory=list)
    chains: dict[str, Chain] = field(default_factory=dict)

    def chain(self, chain_id: str) -> Chain:
        return self.chains.setdefault(chain_id, Chain(chain_id))


def get(doc: Any, *path: str) -> Any:
    node = doc
    for key in path:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def digest_value(node: Any) -> Any:
    return node.get("value") if isinstance(node, dict) else None


def build_scope(records: Iterable[tuple[str, dict]]) -> Scope:
    scope = Scope(records=list(records))
    for label, doc in scope.records:
        kind = doc.get("kind")
        if kind == "xfactory_signed_execution_chain_inception":
            scope.inceptions.append((label, doc))
            chain_id = digest_value(doc.get("chain_identity"))
            if isinstance(chain_id, str):
                scope.chain(chain_id).inception = (label, doc)
        elif kind == "xfactory_signed_execution_chain_traveling_contract":
            scope.travelings.append((label, doc))
            chain_id = digest_value(doc.get("chain_identity"))
            if isinstance(chain_id, str):
                scope.chain(chain_id).traveling.append((label, doc))
        elif kind == "xfactory_signed_execution_chain_log_leaf":
            scope.leaves.append((label, doc))
            chain_id = doc.get("chain_ref")
            if isinstance(chain_id, str):
                scope.chain(chain_id).leaves.append((label, doc))
        elif kind == "xfactory_signed_execution_chain_conformance_declaration":
            scope.declarations.append((label, doc))
        elif kind in CONSUMED_KIND_TO_SCHEMA:
            # CONSUMED, NOT CLASSIFIED. These are `add-trust-anchor`'s records and
            # this scope holds them only so tranche two's composed issuance has its
            # other two parts to resolve against; no chain rule of this capability
            # reads them except through a binding that names them.
            scope.consumed.append((label, doc))
    return scope


# --------------------------- rule: shapes ---------------------------

def check_shapes(f: Findings, scope: Scope, registry: Registry,
                 docs: dict[str, dict], carried: dict[str, dict]) -> None:
    for label, doc in scope.records:
        kind = doc.get("kind") if isinstance(doc, dict) else None
        if kind in CONSUMED_KIND_TO_SCHEMA:
            # HELD TO THE SHAPE THAT OWNS THEM, never to a local restatement of it,
            # which would be the second vocabulary this capability exists not to
            # invent.
            owner = carried.get(kind)
            if owner is None:
                continue
            for message in schema_errors(doc, owner):
                f.error("carried-vocabulary",
                        f"{label}: does not conform to the `add-trust-anchor` "
                        f"vocabulary that owns it ({kind}): {message}")
            continue
        if kind not in KIND_TO_SCHEMA:
            # Only reachable from a hand-assembled scope: both entry points filter
            # on the family kinds. It is a finding rather than a KeyError so a
            # stray document in the packaged corpus reads as a finding rather than
            # as a crashed harness.
            f.error("schema",
                    f"{label}: {kind!r} is not a kind of this family "
                    f"({sorted(KIND_TO_SCHEMA)})")
            continue
        for message in schema_errors(doc, docs[KIND_TO_SCHEMA[kind]], registry):
            f.error("schema", f"{label}: {message}")
    for label, doc in scope.inceptions + scope.travelings:
        signed = doc.get("signed_ratification")
        if not isinstance(signed, dict):
            continue
        check_carried_vocabulary(f, label, signed, carried)


def check_carried_vocabulary(f: Findings, label: str, signed: dict,
                             carried: dict[str, dict]) -> None:
    """The carried blocks are the SHIPPED records, so they are held to the shipped
    shapes wherever those shapes are reachable — never to a local restatement of
    them, which would be the second vocabulary this capability exists not to
    invent."""
    blocks = [
        ("presentation/exercise", get(signed, "presentation", "exercise"), "exercise"),
        ("presentation/wallet", get(signed, "presentation", "wallet"), "wallet"),
        ("actor/wallet_attestation",
         get(signed, "actor", "wallet_attestation"), "attestation"),
        ("actor/subject_reference",
         get(signed, "actor", "subject_reference"), "actor_subject_reference"),
    ]
    for where, block, key in blocks:
        schema = carried.get(key)
        if schema is None or block is None:
            continue
        for message in schema_errors(block, schema):
            f.error("carried-vocabulary",
                    f"{label}: {where} does not conform to the vocabulary that "
                    f"owns it ({key}): {message}")


# --------------------------- rule: digests ---------------------------

def recompute(f: Findings, label: str, subject: str, carried: Any, value: Any,
              where: str) -> bool:
    """Recompute a carried digest under the one construction in force. A
    disagreement is reported as a CONSTRUCTION MISMATCH rather than as a broken
    chain: two readers serializing the same record differently derive different
    digests, and calling that a break would blame the chain for the reader."""
    if not isinstance(value, str):
        return False
    if not canonical.is_tagged(value):
        f.error("digest_construction_mismatch",
                f"{label}: {where} carries an untagged digest {value!r}; an "
                f"untagged digest cannot be migrated without silently changing "
                f"meaning")
        return False
    try:
        derived = canonical.digest(carried)
    except canonical.ConstructionError as exc:
        f.error("digest_construction_mismatch",
                f"{label}: {where} cannot be serialized under "
                f"{canonical.CONSTRUCTION}: {exc}")
        return False
    if derived != value:
        f.error("digest_construction_mismatch",
                f"{label}: {where} carries {value} but the digest of the "
                f"{subject} recomputed under {canonical.CONSTRUCTION} is "
                f"{derived}")
        return False
    return True


def leaf_content(doc: dict) -> dict:
    """The leaf content is the leaf record with its own digest and signature
    removed. A digest cannot cover itself, and a signature cannot cover the digest
    of the bytes it is part of."""
    return {key: value for key, value in doc.items()
            if key not in ("leaf_digest", "leaf_signature")}


def check_digests(f: Findings, scope: Scope) -> None:
    for label, doc in scope.inceptions:
        signed = doc.get("signed_ratification")
        chain_id = digest_value(doc.get("chain_identity"))
        content = digest_value(get(signed, "ratified_subject", "subject_digest"))
        if isinstance(chain_id, str) and chain_id == content:
            # Reported BEFORE the recomputation, and the recomputation is then
            # suppressed for this record: the equation is the defect, and a second
            # finding saying the digest also fails to recompute would bury it.
            f.error("content_digest_equated_with_chain_identity",
                    f"{label}: the chain identity and the ratification's content "
                    f"digest carry the same value {chain_id}. They are taken over "
                    f"DIFFERENT subjects — the SIGNED ratification and the subject "
                    f"ratified — and the signed bytes are a strict superset, so the "
                    f"two can never be equal for a conforming record")
        elif signed is not None:
            recompute(f, label, "signed ratification", signed, chain_id,
                      "chain_identity")
    for label, doc in scope.travelings:
        signed = doc.get("signed_ratification")
        if signed is not None:
            recompute(f, label, "signed ratification", signed,
                      digest_value(doc.get("chain_identity")), "chain_identity")
    for label, doc in scope.leaves:
        recompute(f, label, "leaf content", leaf_content(doc),
                  digest_value(doc.get("leaf_digest")), "leaf_digest")
        check_leaf_payload_digest(f, label, doc, scope)


def check_leaf_payload_digest(f: Findings, label: str, doc: dict,
                              scope: Scope) -> None:
    """A leaf commits to WHAT IT RECORDS, and the subject it names has to be the
    one that act's digest is taken over. A leaf whose payload digest names the
    wrong subject is a leaf whose commitment cannot be checked, which is the same
    as no commitment at all."""
    leaf_type = doc.get("leaf_type")
    payload = doc.get("payload_digest")
    subject = payload.get("subject") if isinstance(payload, dict) else None
    expected = {
        "wallet_presented_ratification": "ratified_subject",
        "chain_inception": "signed_ratification",
        "traveling_contract_issued": "traveling_contract",
        "gate_verdict": "gate_verdict",
    }.get(leaf_type)
    if expected is None or subject is None:
        return
    if subject != expected:
        f.error("digest_construction_mismatch",
                f"{label}: a {leaf_type} leaf commits to a digest over "
                f"{subject!r}; the act it records is digested over {expected!r}, "
                f"and readers that agree on how to hash can still disagree on what "
                f"was hashed")
        return
    if leaf_type == "gate_verdict":
        verdict = doc.get("verdict")
        if verdict is not None:
            recompute(f, label, "verdict", verdict, digest_value(payload),
                      "payload_digest")
        return
    if leaf_type == "traveling_contract_issued":
        # A LEAF BELONGS TO THE CHAIN IT NAMES, so the lookup is CHAIN-SCOPED.
        # Found by Codex as a P1 on `eb1241fc`, and it is round two's shape one
        # level up: the leaf's `chain_ref` and the payload it names could
        # disagree. A scope-wide lookup by identifier matched chain B's traveling
        # contract from a leaf filed under chain A, the digest recomputed cleanly,
        # and the missing-leaf rule — which collected recorded ids GLOBALLY — then
        # treated chain A's leaf as discharging chain B's obligation. Chain B
        # passed with its primary custody record silent about an act the contract
        # requires to be recorded, which is exactly the hole that rule had just
        # been added to close.
        chain = scope.chains.get(doc.get("chain_ref"))
        matches = [(other_label, other) for other_label, other
                   in (chain.traveling if chain else [])
                   if other.get("traveling_contract_id") == doc.get("payload_ref")]
        if not matches:
            f.error("continuity_broken",
                    f"{label}: this leaf records the issuance of traveling "
                    f"contract {doc.get('payload_ref')!r} and no traveling "
                    f"contract of chain {doc.get('chain_ref')} carries that "
                    f"identifier. An issuance is discharged only by a leaf on the "
                    f"ISSUING chain")
            return
        if len(matches) > 1:
            f.error("continuity_broken",
                    f"{label}: {len(matches)} traveling contracts of this chain "
                    f"carry the identifier {doc.get('payload_ref')!r}, so which "
                    f"issuance this leaf records cannot be established")
            return
        other_label, other = matches[0]
        recompute(f, label, "traveling contract", other, digest_value(payload),
                  f"payload_digest (over {other_label})")
        return
    if leaf_type == "wallet_presented_ratification":
        # THE CONTENT DIGEST IS IN SCOPE, SO IT IS COMPARED. Checking only that
        # the SUBJECT is named `ratified_subject` and never comparing the value
        # would be a check of exactly the shape round one's four findings had:
        # it reads as though the leaf's commitment were verified while nothing is
        # compared. The subject ratified is external and cannot be recomputed
        # here, but the digest the ratification DECLARES over it can be, and a
        # ratification leaf committing to some other subject's digest records the
        # presentation of a ratification that is not this one.
        chain = scope.chains.get(doc.get("chain_ref"))
        if chain is None or chain.inception is None:
            return
        declared = digest_value(get(chain.inception[1], "signed_ratification",
                                    "ratified_subject", "subject_digest"))
        if declared is not None and digest_value(payload) != declared:
            f.error("digest_construction_mismatch",
                    f"{label}: the ratification leaf commits to "
                    f"{digest_value(payload)} and this chain's ratification "
                    f"declares the content digest {declared}. The leaf records a "
                    f"presentation for a different subject than the one this "
                    f"chain ratified")
        # AND THE `payload_ref` NAMES THE PRESENTATION, not merely something. A
        # leaf whose digest is right and whose reference points elsewhere records
        # the right commitment against the wrong act.
        presentation = get(chain.inception[1], "signed_ratification",
                           "presentation", "exercise_ref")
        if presentation is not None and doc.get("payload_ref") != presentation:
            f.error("continuity_broken",
                    f"{label}: the ratification leaf records payload "
                    f"{doc.get('payload_ref')!r} and this chain's ratification was "
                    f"proved by exercise {presentation!r}")


# --------------------------- rule: the log ---------------------------

def check_log(f: Findings, scope: Scope) -> None:
    """THE LOG'S APPEND-ONLY PROPERTY IS A STORE OBLIGATION over the whole log,
    not a per-chain check: leaves from every chain share one sequence, and the
    hash link is what makes an alteration inside an observed prefix detectable."""
    if not scope.leaves:
        return
    ordered = sorted(scope.leaves, key=lambda item: item[1].get("leaf_index", 0))
    seen: dict[int, str] = {}
    for label, doc in ordered:
        index = doc.get("leaf_index")
        if not isinstance(index, int):
            continue
        if index in seen:
            f.error("leaf_hash_link_broken",
                    f"{label}: leaf index {index} is already held by {seen[index]}; "
                    f"an append-only log has one leaf per position, and two is how "
                    f"a replacement presents itself as an append")
        seen[index] = label
        if doc.get("tree_size") != index + 1:
            f.error("leaf_hash_link_broken",
                    f"{label}: leaf_index {index} completes a tree of size "
                    f"{index + 1}, and the leaf declares {doc.get('tree_size')!r}. "
                    f"The head is the newest leaf, and a head that misstates its "
                    f"own size is how a truncation presents itself as a complete "
                    f"log")
    # THE RETAINED SET MUST BEGIN AT ITS GENESIS LEAF AND RUN CONSECUTIVELY, and
    # this is checked BEFORE any predecessor digest, because a link chain walked
    # over a set with a hole in it verifies the links that remain and says
    # nothing about the ones that do not.
    #
    # Found by Codex as a P1 on `0d0f277d`. The first version walked consecutive
    # PAIRS: the lowest retained leaf had no predecessor in scope, so its carried
    # digest went unchecked, and a store that deleted a prefix presented a set in
    # which every surviving pair linked correctly and every `tree_size` still
    # agreed with its own index. LEAVES ARE APPENDED AND NEVER REMOVED is the
    # contract's sentence; a check that cannot see a removal is not checking it.
    present = sorted(index for index in seen)
    if present and present[0] != 0:
        f.error("leaf_hash_link_broken",
                f"the retained log begins at leaf {present[0]} ({seen[present[0]]}) "
                f"and not at its genesis leaf, so leaves 0-{present[0] - 1} have "
                f"been removed from an append-only log. The surviving leaves link "
                f"to one another correctly, which is exactly what a deleted prefix "
                f"looks like")
    expected_indices = list(range(present[0], present[-1] + 1)) if present else []
    missing = [index for index in expected_indices if index not in seen]
    if missing:
        f.error("leaf_hash_link_broken",
                f"the retained log skips leaf position(s) {missing} between "
                f"{present[0]} and {present[-1]}; an append-only log has no holes, "
                f"and a hole is a removal that the links either side of it cannot "
                f"detect")

    previous: tuple[str, dict] | None = None
    for label, doc in ordered:
        index = doc.get("leaf_index")
        carried = digest_value(doc.get("previous_leaf_digest"))
        if index == 0:
            if carried is not None:
                f.error("leaf_hash_link_broken",
                        f"{label}: the genesis leaf carries a predecessor digest "
                        f"{carried}; there is nothing before position 0")
        elif carried is None:
            f.error("leaf_hash_link_broken",
                    f"{label}: leaf {index} carries no predecessor digest, so the "
                    f"link chain stops here and every alteration before it becomes "
                    f"undetectable")
        elif previous is None or previous[1].get("leaf_index") != index - 1:
            # No predecessor IN SCOPE to compare against. The prefix and gap
            # rules above have already named why, and reporting the comparison as
            # a pass here is what let a truncated prefix through.
            f.error("leaf_hash_link_broken",
                    f"{label}: leaf {index} carries predecessor digest {carried} "
                    f"and leaf {index - 1} is not in scope, so the carried digest "
                    f"is compared against nothing. An unverifiable link is not a "
                    f"verified one")
        else:
            expected = digest_value(previous[1].get("leaf_digest"))
            if expected is not None and carried != expected:
                f.error("leaf_hash_link_broken",
                        f"{label}: the predecessor digest {carried} does not match "
                        f"{previous[0]}'s own digest {expected}. A consistency "
                        f"proof against an observed head fails here, and the "
                        f"alteration is a fraud signal rather than a corrupted file")
        previous = (label, doc)


def check_traveling_contracts_alone(f: Findings, scope: Scope) -> None:
    """THE POINT-OF-USE CHECK, PERFORMED THE WAY A POINT-OF-USE CHECKER WOULD.

    Requirement 5's whole claim is that a traveling contract is a SELF-CONTAINED
    artifact: a checker that can resolve no registry and no live service can
    still establish its internal consistency. This function is that claim
    executed — it reads ONE traveling contract and nothing else, recovers the
    signing key from the wallet the artifact carries, and verifies the carried
    signature over the canonical bytes of the carried `signed_ratification`.

    Without it the reader would establish the signature only through the
    INCEPTION record, and the artifact's self-containment would be a property
    nothing ever exercised — which is the described-control failure this
    capability exists to end, one level down.

    It establishes CONSISTENCY ONLY. Whether the chain this artifact names was
    ever incepted, whether its leaf is in the log, and whether the log's prefix
    is intact are questions that require the store, and the chain walk still
    refuses them when it cannot reach it."""
    for label, doc in scope.travelings:
        signed = doc.get("signed_ratification")
        signature = doc.get("ratification_signature") or {}
        if not isinstance(signed, dict):
            continue
        key_ref = signature.get("presenting_key_ref")
        entry = declared_keys(get(signed, "presentation", "wallet")).get(key_ref)
        raw = decode_signature(signature.get("signature"))
        if entry is AMBIGUOUS_KEY:
            entry = None
        if signature.get("algorithm") != VERIFIABLE_ALGORITHM or entry is None:
            f.error("chain_unevaluable",
                    f"{label}: the carried signature declares "
                    f"{signature.get('algorithm')!r} by key {key_ref!r}, which "
                    f"this reader cannot evaluate from the artifact alone. A "
                    f"traveling contract a point-of-use checker cannot check is "
                    f"not a traveling contract")
            continue
        try:
            public = ed25519.public_key_from_did(entry.get("did"))
            message = canonical.serialize(signed).encode("utf-8")
        except (ed25519.KeyRecoveryError, canonical.ConstructionError) as exc:
            f.error("chain_unevaluable", f"{label}: {exc}")
            continue
        if raw is None or not ed25519.verify(public, message, raw):
            f.error("ratification_signature_invalid",
                    f"{label}: the signature the traveling contract CARRIES does "
                    f"not verify against key {key_ref!r} over the canonical bytes "
                    f"of the ratification it carries, so the artifact establishes "
                    f"nothing on its own")


def check_leaf_signatures(f: Findings, scope: Scope) -> None:
    """EVERY LEAF IS SIGNED, and this reader verifies the ones whose key it can
    resolve.

    A leaf's `key_ref` is resolved against the keys DECLARED by the wallets this
    scope carries. Where it resolves, the signature is verified over the canonical
    bytes of the leaf content and a failure is a refusal. Where it does not — a
    store signing identity established by an operator, which this tranche defines
    no custody for and no record of — the reader says the signature is UNVERIFIED
    rather than treating an unresolvable key as a pass. That bound is what the
    realization declares under SEC-R6, and it is stated here as well because a
    limit recorded only in a declaration is a limit nobody reads at the moment it
    applies. Detection at this tranche rests on the HASH LINK and on the traveling
    contract's carried leaf digest, which is exactly the strength the requirement
    claims."""
    keys: dict[str, Any] = {}
    for _, doc in scope.inceptions + scope.travelings:
        merge_declared_keys(keys, get(doc, "signed_ratification", "presentation",
                                      "wallet"))
    for label, doc in scope.leaves:
        signature = doc.get("leaf_signature") or {}
        key_ref = signature.get("key_ref")
        entry = keys.get(key_ref)
        if entry is AMBIGUOUS_KEY:
            f.error("chain_unevaluable",
                    f"{label}: the leaf signature names key {key_ref!r}, which "
                    f"more than one carried wallet declares for DIFFERENT public "
                    f"halves. An ambiguous key is not a resolved one, and "
                    f"verifying against whichever declaration was read last is a "
                    f"result decided by iteration order")
            continue
        if entry is None:
            f.warn("leaf-signature-unverified",
                   f"{label}: the leaf signature names key {key_ref!r}, which no "
                   f"wallet carried in this scope declares, so it is recorded and "
                   f"NOT verified here")
            continue
        raw = decode_signature(signature.get("signature"))
        if signature.get("algorithm") != VERIFIABLE_ALGORITHM or raw is None:
            f.warn("leaf-signature-unverified",
                   f"{label}: the leaf signature declares "
                   f"{signature.get('algorithm')!r}; this reader verifies "
                   f"{VERIFIABLE_ALGORITHM!r} and records the rest unverified")
            continue
        try:
            public = ed25519.public_key_from_did(entry.get("did"))
            message = canonical.serialize(leaf_content(doc)).encode("utf-8")
        except (ed25519.KeyRecoveryError, canonical.ConstructionError) as exc:
            f.warn("leaf-signature-unverified", f"{label}: {exc}")
            continue
        if not ed25519.verify(public, message, raw):
            f.error("leaf_signature_invalid",
                    f"{label}: the leaf signature does not verify against key "
                    f"{key_ref!r} over the canonical bytes of the leaf content. A "
                    f"leaf whose signature does not verify is not a leaf of this "
                    f"log")


def check_atomicity(f: Findings, scope: Scope) -> None:
    """RULE (i) — ratification and inception are ONE signed act. Either both stand
    or neither does, so a ratification leaf whose act was never inscribed is a
    half-state, and it is refused rather than read as a record awaiting
    completion.

    AND EVERY ACT THIS CAPABILITY GOVERNS WRITES A LEAF, checked in BOTH
    directions. The first version checked only that a ratification leaf had an
    inception leaf beside it; a chain whose inception existed with NO ratification
    leaf, and a traveling contract whose ISSUANCE no leaf recorded, both passed.
    That is round one's defect class — a check that reads as though it covered an
    obligation while covering one half of it — caught here by the pass D7.8 says
    is owed after a finding rather than by a fifth finding."""
    for chain_id, chain in sorted(scope.chains.items()):
        types = {doc.get("leaf_type") for _, doc in chain.leaves}
        if "wallet_presented_ratification" in types and "chain_inception" not in types:
            labels = ", ".join(label for label, _ in chain.leaves)
            f.error("ratified_but_uninscribed",
                    f"chain {chain_id}: the log records a wallet-presented "
                    f"ratification and no chain inception ({labels}). An inception "
                    f"that fails leaves no standing ratification, and no partial "
                    f"state may be retained that a later reader could mistake for "
                    f"one")
        if chain.inception is not None and \
                "wallet_presented_ratification" not in types:
            f.error("act_unproven",
                    f"chain {chain_id}: the ratification this chain was incepted "
                    f"from is recorded in no leaf ({chain.inception[0]}). The "
                    f"wallet-presented ratification is one of the four acts this "
                    f"capability governs, and an act with no signed leaf is "
                    f"UNPROVEN however completely the rest of the chain verifies")
        if chain.inception is not None and "gate_verdict" not in types:
            # THE FOURTH GOVERNED LEAF TYPE, and the omission was fresh evidence
            # of the same class one round after the missing-act fix (Codex, P1 on
            # `eb1241fc`): that fix required the ratification and traveling-contract
            # leaves and still never required this one, so a chain could pass with
            # its own adjudication absent from the primary custody record.
            #
            # IT IS NOT A CHICKEN-AND-EGG, and the packaged corpus is the proof: a
            # producer WRITES the verdict leaf it expects, and this reader holds it
            # to the reader's own walk — a leaf claiming `permitted` over a chain
            # the walk refuses is itself a refusal. So requiring the leaf demands
            # no trust in the producer and deadlocks no first landing.
            f.error("act_unproven",
                    f"chain {chain_id}: no gate-verdict leaf records this chain's "
                    f"adjudication ({chain.inception[0]}). Every verdict the gate "
                    f"returns is one of the four acts this capability governs, and "
                    f"a chain whose own verdict is absent from the log has a "
                    f"custody record silent about whether it was ever permitted")
    # KEYED ON THE PAIR, not on the identifier alone (Codex, P1 on `eb1241fc`).
    # A global set of recorded identifiers let a leaf filed under ANOTHER chain
    # discharge this chain's obligation, so the chain a leaf names is part of what
    # it records.
    recorded = {(doc.get("chain_ref"), doc.get("payload_ref"))
                for _, doc in scope.leaves
                if doc.get("leaf_type") == "traveling_contract_issued"}
    for label, doc in scope.travelings:
        pair = (digest_value(doc.get("chain_identity")),
                doc.get("traveling_contract_id"))
        if pair not in recorded:
            f.error("act_unproven",
                    f"{label}: the issuance of this traveling contract is recorded "
                    f"in no leaf OF ITS OWN CHAIN. Issuing one is an act this "
                    f"capability governs, and work travels on an artifact whose "
                    f"issuance nothing proves")


def check_per_act_uniqueness(f: Findings, scope: Scope) -> None:
    """RULE (ii) — the per-act value is NAMED, not minted, and the pinned schema
    constrains no reuse, so this capability enforces it. Without it, re-ratifying
    an unchanged subject reproduces identical bytes, an identical digest and — under
    a deterministic signature scheme — an identical signature, and the collision
    returns by the back door."""
    seen: dict[str, tuple[str, str]] = {}
    for label, doc in scope.inceptions:
        # KEYED ON THE CARRIED IDENTIFIER, falling back to the outer reference
        # only when no record is carried. The outer reference is replaceable
        # without touching the exercise it names, so keying on it alone let a
        # consumed exercise through under a fresh label (Codex, P1). The gate's
        # own binding requires the two to agree; this key does not DEPEND on that
        # check having run, because a rule that relies on another rule to be sound
        # is a rule with a second failure mode.
        value = get(doc, "signed_ratification", "presentation", "exercise",
                    "exercise_id") or \
            get(doc, "signed_ratification", "presentation", "exercise_ref")
        chain_id = digest_value(doc.get("chain_identity"))
        if not isinstance(value, str) or not isinstance(chain_id, str):
            continue
        if value in seen and seen[value][1] != chain_id:
            f.error("per_act_value_reused",
                    f"{label}: the per-act value {value!r} is already consumed by "
                    f"chain {seen[value][1]} ({seen[value][0]}). One exercise is "
                    f"one act; reusing it while re-ratifying an unchanged subject "
                    f"reproduces the identical signed bytes")
        else:
            seen[value] = (label, chain_id)


# --------------------------- rule: the eight checks ---------------------------

def decode_signature(value: Any) -> bytes | None:
    """A signature's TEXT is canonical unpadded base64url, or it is refused.

    Found by Codex as a P2 on `eb1241fc`. For 64 bytes the final base64url
    character carries only two data bits, and `urlsafe_b64decode` IGNORES the
    remaining four: sixteen different textual signatures decode to the same bytes,
    verify identically, and all match the schema pattern. The contract says
    canonical unpadded base64url, so the reader re-encodes the decoded bytes and
    requires an exact match — one signature, one spelling. Measured before the
    repair: an altered final character on a packaged example verified cleanly.
    """
    if not isinstance(value, str) or not BASE64URL_RX.match(value):
        return None
    padding = "=" * (-len(value) % 4)
    try:
        raw = base64.urlsafe_b64decode(value + padding)
    except (ValueError, TypeError):
        return None
    if len(raw) != ed25519.SIGNATURE_BYTES:
        return None
    if base64.urlsafe_b64encode(raw).decode().rstrip("=") != value:
        return None
    return raw


#: An identifier claimed by two key declarations with DIFFERENT public halves.
#: Held as a value in the key map rather than dropped, because "ambiguous" and
#: "absent" are different answers and only one of them is a reader's own fault.
AMBIGUOUS_KEY = object()


def _merge_key(keys: dict[str, Any], entry: dict) -> None:
    key_id = entry.get("key_id")
    if not isinstance(key_id, str):
        return
    held = keys.get(key_id)
    if held is None:
        keys[key_id] = entry
    elif held is AMBIGUOUS_KEY:
        return
    elif held.get("did") != entry.get("did"):
        keys[key_id] = AMBIGUOUS_KEY


def declared_keys(wallet: Any) -> dict[str, Any]:
    """Every key the carried wallet DECLARES, by `key_id`. A presenting key no
    wallet declares is unresolvable, which is an unevaluable chain and never a
    failed signature — the two are different events.

    AND AN IDENTIFIER TWO DECLARATIONS CLAIM FOR DIFFERENT PUBLIC HALVES IS
    `AMBIGUOUS_KEY`, NOT THE LAST ONE SEEN. Found by Codex as a P1 on `aedfd8ce`:
    the first version merged declarations with `dict.update`, so whichever wallet
    was encountered last silently won. Valid leaves of the other chain would then
    fail, and leaves signed by the colliding wallet's key would be ACCEPTED for a
    chain that never authorized it — a verification result decided by iteration
    order. Verifying against a guess is worse than declining to verify, so an
    ambiguous identifier makes every signature naming it unevaluable, which is a
    refusal. Two declarations of the same id with the SAME `did` are a harmless
    restatement and stay resolved."""
    keys: dict[str, Any] = {}
    if not isinstance(wallet, dict):
        return keys
    reference = wallet.get("key_reference")
    if isinstance(reference, dict):
        _merge_key(keys, reference)
    for entry in wallet.get("keys") or []:
        if isinstance(entry, dict):
            _merge_key(keys, entry)
    return keys


def merge_declared_keys(target: dict[str, Any], wallet: Any) -> None:
    """Fold one carried wallet's declarations into a scope-wide map, carrying the
    ambiguity FORWARD rather than overwriting or dropping it.

    An id already ambiguous inside one wallet stays ambiguous in the scope: a
    reader that discarded it here would resolve, from a second wallet, an
    identifier the first wallet had already made unanswerable."""
    for key_id, entry in declared_keys(wallet).items():
        if entry is AMBIGUOUS_KEY:
            target[key_id] = AMBIGUOUS_KEY
        else:
            _merge_key(target, entry)


def check_one(f: Findings, label: str, doc: dict, scope: Scope) -> dict[str, str]:
    """The eight ordered checks over one chain, returning each check's outcome so a
    recorded gate verdict can be held to the same walk."""
    outcomes = {name: "pass" for name in CHECK_NAMES}
    # THE CODES THIS WALK ACTUALLY EMITTED, collected so a recorded verdict can be
    # held to the REASON as well as to the outcome (Codex, P2 on `eb1241fc`).
    emitted: set[str] = set()

    def fail(name: str, code: str, message: str) -> None:
        outcomes[name] = "fail"
        emitted.add(code)
        f.error(code, f"{label}: {message}")

    def unevaluable(name: str, message: str) -> None:
        outcomes[name] = "not_evaluable"
        emitted.add("chain_unevaluable")
        f.error("chain_unevaluable", f"{label}: {message}")

    signed = doc.get("signed_ratification") or {}
    signature = doc.get("ratification_signature") or {}
    presentation = signed.get("presentation") or {}
    exercise = presentation.get("exercise") or {}
    wallet = presentation.get("wallet") or {}
    actor = signed.get("actor") or {}
    chain_id = digest_value(doc.get("chain_identity"))

    # ---- check 1: the ratification's signature verifies -------------------
    algorithm = signature.get("algorithm")
    key_ref = signature.get("presenting_key_ref")
    keys = declared_keys(wallet)
    if algorithm != VERIFIABLE_ALGORITHM:
        unevaluable(CHECK_NAMES[0],
                    f"the ratifying signature declares {algorithm!r}; this "
                    f"realization verifies {VERIFIABLE_ALGORITHM!r} and refuses the "
                    f"rest as unevaluable rather than accepting a signature it did "
                    f"not check")
    elif keys.get(key_ref) is AMBIGUOUS_KEY:
        unevaluable(CHECK_NAMES[0],
                    f"wallet {wallet.get('wallet_id')!r} declares the presenting "
                    f"key {key_ref!r} more than once for DIFFERENT public halves, "
                    f"so which half signed cannot be established")
    elif key_ref not in keys:
        unevaluable(CHECK_NAMES[0],
                    f"the presenting key {key_ref!r} is declared by no key of "
                    f"wallet {wallet.get('wallet_id')!r} "
                    f"({sorted(keys) or 'none declared'}); an unresolvable key is "
                    f"an unevaluable chain, never a failed signature")
    else:
        entry = keys[key_ref]
        raw_signature = decode_signature(signature.get("signature"))
        try:
            public = ed25519.public_key_from_did(entry.get("did"))
            multibase = entry.get("public_key_multibase")
            if isinstance(multibase, str) and \
                    ed25519.public_key_from_multibase(multibase) != public:
                raise ed25519.KeyRecoveryError(
                    "the key's `did` and `public_key_multibase` encode different "
                    "public halves, so which one signed cannot be established")
        except ed25519.KeyRecoveryError as exc:
            public = None
            unevaluable(CHECK_NAMES[0], f"key {key_ref!r}: {exc}")
        if public is not None:
            if raw_signature is None:
                fail(CHECK_NAMES[0], "ratification_signature_invalid",
                     "the ratifying signature is not 64 bytes of canonical "
                     "unpadded base64url")
            else:
                try:
                    message = canonical.serialize(signed).encode("utf-8")
                except canonical.ConstructionError as exc:
                    message = None
                    unevaluable(CHECK_NAMES[0],
                                f"the signed ratification cannot be serialized "
                                f"under {canonical.CONSTRUCTION}: {exc}")
                if message is not None and not ed25519.verify(
                        public, message, raw_signature):
                    fail(CHECK_NAMES[0], "ratification_signature_invalid",
                         f"the ratifying signature does not verify against key "
                         f"{key_ref!r} over the canonical bytes of "
                         f"`signed_ratification`")
    if key_ref is not None and presentation.get("presenting_key_ref") != key_ref:
        fail(CHECK_NAMES[0], "continuity_broken",
             f"the signature names presenting key {key_ref!r} and the presentation "
             f"names {presentation.get('presenting_key_ref')!r}; artifacts from "
             f"different acts do not assemble into one chain")

    # ---- check 2: the chain identity recomputes ---------------------------
    # The recomputation itself is `check_digests`'; this reads its outcome so the
    # verdict a gate records can be held to the same walk. Reporting it twice
    # would say one thing in two places.
    content = digest_value(get(signed, "ratified_subject", "subject_digest"))
    try:
        derived = canonical.digest(signed)
    except canonical.ConstructionError:
        derived = None
    if derived is None or derived != chain_id:
        outcomes[CHECK_NAMES[1]] = "fail"

    # ---- the presentation reference NAMES the record it carries ------------
    # Found by Codex as a P1 on `aedfd8ce`, and it was the sharpest finding of
    # this bench. Without this, a producer carries the ALREADY-CONSUMED exercise
    # VERBATIM and replaces only the OUTER `exercise_ref` with a fresh value: the
    # signed bytes change, the chain identity changes, and the per-act uniqueness
    # map — keyed on that outer reference — sees a value it has never seen. The
    # consumed exercise was replayable despite a rule written to prevent exactly
    # that. ONE EXERCISE IS ONE ACT, so the reference and the record it names must
    # agree, and uniqueness is keyed on the CARRIED identifier as well.
    carried_id = exercise.get("exercise_id")
    if carried_id is not None and presentation.get("exercise_ref") != carried_id:
        fail(CHECK_NAMES[2], "continuity_broken",
             f"the presentation names exercise "
             f"{presentation.get('exercise_ref')!r} and the carried exercise "
             f"record is {carried_id!r}. A reference that does not name the record "
             f"beside it names nothing, and moving the two independently is how a "
             f"consumed exercise is replayed past the uniqueness rule")

    # THE REST OF THE SAME SHAPE, swept for rather than waited for. Round two's
    # two findings were both a REFERENCE and its REFERENT able to move
    # independently — two facts that look like one fact. A capability whose whole
    # subject is binding one record to another should expect it everywhere, so
    # every remaining pair of that shape is compared here. These paths are covered
    # by `tests/signed_execution_chain/test_chain_reader.py` rather than by three
    # more packaged fixtures: the closed refusal code they report is already
    # red-proven, and what needs pinning is that each COMPARISON runs.
    for outer, inner, what in (
        (presentation.get("grant_ref"), exercise.get("grant_ref"), "grant"),
        (wallet.get("wallet_id"), get(exercise, "attribution", "wallet_ref"),
         "attributed wallet"),
        (get(wallet, "holder", "holder_id"),
         get(exercise, "attribution", "holder_ref"), "attributed holder"),
        (get(wallet, "custody", "model"), exercise.get("custody_model_in_force"),
         "custody model in force"),
    ):
        if outer is not None and inner is not None and outer != inner:
            fail(CHECK_NAMES[2], "continuity_broken",
                 f"the chain's {what} is {outer!r} and the carried exercise "
                 f"records {inner!r}. The two are one fact, and a disagreement "
                 f"means the exercise beside this ratification is not the exercise "
                 f"this ratification was proved by")
    # CUSTODY IS THE ONE OF THOSE FOUR THAT IS LOAD-BEARING RATHER THAN TIDY.
    # `add-trust-anchor`'s ratified rule is that DECLARED CUSTODY BOUNDS WHAT A
    # SIGNATURE EVIDENCES — a key readable by the host that uses it evidences that
    # the HOST acted, which is precisely what a ratification may not stand on. So
    # an exercise recording a stronger custody model than the wallet it was made
    # with declares would let a `holder_readable` key evidence a human act, and
    # requirement 8's whole narrowing rests on that not being possible.

    # ---- check 3: object_ref is the CONTENT digest (the replay check) ------
    object_ref = exercise.get("object_ref")
    if object_ref is None:
        fail(CHECK_NAMES[2], "exercise_object_ref_absent",
             "the exercise carries no `object_ref`. The pinned schema leaves it "
             "optional; this capability requires it, because an identifier alone "
             "would let a previously successful exercise be replayed as the proof "
             "for a different ratification")
    elif not canonical.is_tagged(object_ref):
        fail(CHECK_NAMES[2], "exercise_replayed",
             f"the exercise's `object_ref` {object_ref!r} is not a tagged digest, "
             f"so it is nominal rather than recomputable and binds nothing")
    elif content is None or object_ref != content:
        fail(CHECK_NAMES[2], "exercise_replayed",
             f"the exercise's `object_ref` {object_ref} is not this ratification's "
             f"content digest {content}. The exercise is REFUSED AS A REPLAY, and "
             f"its own validity is not a defence")

    # ---- check 4: the inception leaf commits to this chain identity -------
    chain = scope.chains.get(chain_id) if isinstance(chain_id, str) else None
    inception_leaves = [(leaf_label, leaf) for leaf_label, leaf in
                        (chain.leaves if chain else [])
                        if leaf.get("leaf_type") == "chain_inception"]
    if not inception_leaves:
        fail(CHECK_NAMES[3], "act_unproven",
             "no chain-inception leaf records this act. An act this capability "
             "governs that writes no signed leaf is UNPROVEN, and its own success "
             "is not evidence that it was permitted")
    else:
        for leaf_label, leaf in inception_leaves:
            committed = digest_value(leaf.get("payload_digest"))
            if committed != chain_id:
                fail(CHECK_NAMES[3], "continuity_broken",
                     f"{leaf_label} records this inception and commits to "
                     f"{committed}, not to the chain identity {chain_id}")
            if leaf.get("payload_ref") != doc.get("inception_id"):
                fail(CHECK_NAMES[3], "continuity_broken",
                     f"{leaf_label} records payload {leaf.get('payload_ref')!r} "
                     f"while this inception is {doc.get('inception_id')!r}")
        if doc.get("inception_leaf_ref") not in {leaf.get("leaf_id")
                                                 for _, leaf in inception_leaves}:
            fail(CHECK_NAMES[3], "continuity_broken",
                 f"the inception names leaf {doc.get('inception_leaf_ref')!r}, "
                 f"which is not among the chain-inception leaves recorded for this "
                 f"chain")

    # ---- check 5: the traveling contract carries the established values ---
    travelings = chain.traveling if chain else []
    if not travelings:
        fail(CHECK_NAMES[4], "missing_link",
             "link 3 is absent: no traveling contract carries this chain. Work "
             "arriving with no traveling contract is UNPERMITTED at the point of "
             "use, and a missing link is a fraud signal rather than a warning")
    for travel_label, travel in travelings:
        if travel.get("presentation_ref") != presentation.get("exercise_ref"):
            fail(CHECK_NAMES[4], "continuity_broken",
                 f"{travel_label} names presentation "
                 f"{travel.get('presentation_ref')!r} while this chain's "
                 f"ratification was proved by "
                 f"{presentation.get('exercise_ref')!r}; individually valid "
                 f"artifacts drawn from different executions do not assemble into "
                 f"a chain")
        carried_leaf = digest_value(travel.get("inception_leaf_digest"))
        known = {digest_value(leaf.get("leaf_digest"))
                 for _, leaf in inception_leaves}
        if inception_leaves and carried_leaf not in known:
            fail(CHECK_NAMES[4], "traveling_contract_digest_mismatch",
                 f"{travel_label} carries inception-leaf digest {carried_leaf}, "
                 f"which is not the digest of any leaf that recorded this "
                 f"inception ({sorted(value for value in known if value)}). The "
                 f"mismatch is never resolved in favour of the carried copy")
        if travel.get("signed_ratification") != signed:
            fail(CHECK_NAMES[4], "continuity_broken",
                 f"{travel_label} carries a signed ratification that is not this "
                 f"chain's; the carried form of the signed ratification is the "
                 f"signed ratification, not a summary of it")

    # ---- check 6: the actor is bound to the wallet that signed ------------
    attestation = actor.get("wallet_attestation") or {}
    reference = actor.get("subject_reference") or {}
    resolved_by = get(attestation, "resolution", "resolved_by")
    if resolved_by != "subject_ref":
        fail(CHECK_NAMES[5], "actor_resolved_through_wallet",
             f"the actor's wallet attestation declares `resolution.resolved_by` "
             f"{resolved_by!r}. The pinned `openxwallet-subject-attestation` "
             f"closes it to `subject_ref` precisely so a record cannot declare it "
             f"resolves a subject THROUGH a wallet; the wallet reference is "
             f"checked as an ATTESTATION and never used to resolve identity")
    if attestation.get("wallet_ref") != wallet.get("wallet_id"):
        fail(CHECK_NAMES[5], "actor_wallet_mismatch",
             f"the recorded actor attests wallet "
             f"{attestation.get('wallet_ref')!r} and the exercise was made by a "
             f"key of {wallet.get('wallet_id')!r}. The exercise proves who SIGNED "
             f"and not whom the act is recorded as, so its validity does not admit "
             f"the link")
    if attestation.get("subject_ref") != reference.get("subject"):
        fail(CHECK_NAMES[5], "actor_wallet_mismatch",
             f"the wallet attestation attests subject "
             f"{attestation.get('subject_ref')!r} while the actor reference names "
             f"{reference.get('subject')!r}; the binding joins nothing")

    # ---- check 7: proof of possession supplied AND verified ---------------
    proof = exercise.get("proof_of_possession") or {}
    event_class = exercise.get("event_class")
    if event_class == "unauthenticated_request" or proof.get("presented") is False:
        fail(CHECK_NAMES[6], "missing_proof_of_possession",
             "the exercise records no proof of possession. The refusal names the "
             "MISSING PROOF and never the missing grant — the grant was supplied "
             "and is not what was lacking")
    elif event_class == "verification_failure" or proof.get("verified") is False:
        fail(CHECK_NAMES[6], "proof_verification_failed",
             "the exercise records a presented proof that did NOT verify. A failed "
             "proof is a stronger signal than a missing one, never a weaker one")
    elif event_class != "authenticated":
        fail(CHECK_NAMES[6], "proof_verification_failed",
             f"the exercise's event class is {event_class!r}; the presence of an "
             f"exercise record is never accepted in place of a verified proof")
    if proof.get("signed_over") != "request_digest":
        fail(CHECK_NAMES[6], "presentation_signed_over_not_request_digest",
             f"the exercise records `proof_of_possession.signed_over` "
             f"{proof.get('signed_over')!r}. This capability restricts the shipped "
             f"selector to `request_digest` — a scope restriction by the consuming "
             f"capability, not a schema change")
    if proof.get("presenting_key_ref") not in (None, key_ref):
        fail(CHECK_NAMES[6], "continuity_broken",
             f"the exercise was presented by key "
             f"{proof.get('presenting_key_ref')!r} and the ratification is signed "
             f"by {key_ref!r}")

    # ---- check 8: standing at exercise, and holder class ------------------
    revocation = exercise.get("revocation_check") or {}
    if revocation.get("performed_at_exercise") is not True:
        fail(CHECK_NAMES[7], "authority_revoked_at_exercise",
             "the exercise records no revocation check performed at exercise, so "
             "standing at presentation is not established. Validity recorded at "
             "issuance is not evidence of validity at presentation")
    elif revocation.get("result") != "active":
        fail(CHECK_NAMES[7], "authority_revoked_at_exercise",
             f"the exercise's revocation check returns "
             f"{revocation.get('result')!r}. A valid signature is not current "
             f"authority, and revocation does not invalidate a signature")
    elif revocation.get("revoked_ancestor_ref") is not None:
        fail(CHECK_NAMES[7], "authority_revoked_at_exercise",
             f"the exercise names revoked ancestor "
             f"{revocation.get('revoked_ancestor_ref')!r}; standing must be current "
             f"for the grant, for every ancestor of it, and for the holder")
    if wallet.get("state") != "active":
        fail(CHECK_NAMES[7], "authority_revoked_at_exercise",
             f"the signing wallet's standing is {wallet.get('state')!r}")
    holder_class = get(wallet, "holder", "holder_class")
    if holder_class not in HUMAN_HOLDER_CLASSES:
        fail(CHECK_NAMES[7], "machine_holder_as_ratifying_authority",
             f"the ratifying wallet's holder class is {holder_class!r}. Ratifying "
             f"authority is HUMAN-HELD: correct attribution is never accepted as "
             f"evidence that the attributed holder was eligible to ratify, and the "
             f"refusal names the holder class rather than the missing signature")
    if exercise.get("outcome") != "permitted":
        fail(CHECK_NAMES[7], "authority_revoked_at_exercise",
             f"the exercise's own outcome is {exercise.get('outcome')!r}; a refused "
             f"exercise proves nothing was permitted")

    # ---- the out-of-pipeline ground, cited rather than asserted -----------
    ground = signed.get("out_of_pipeline") or {}
    if ground.get("performed_out_of_pipeline") is not True or \
            not ground.get("ground_ref"):
        f.error("inception_not_out_of_pipeline",
                f"{label}: the inception does not declare an out-of-pipeline act "
                f"citing its ground. Routing inception through the clearance "
                f"envelope describes a control that provably cannot run, and a "
                f"pipeline that CLEARS candidates cannot also be what CONFERS the "
                f"authority those candidates are cleared against")
        emitted.add("inception_not_out_of_pipeline")
    return outcomes, emitted


def check_chains(f: Findings, scope: Scope) -> None:
    verdicts: dict[str, tuple[dict[str, str], set[str]]] = {}
    for label, doc in scope.inceptions:
        chain_id = digest_value(doc.get("chain_identity"))
        outcomes, emitted = check_one(f, label, doc, scope)
        if isinstance(chain_id, str):
            verdicts[chain_id] = (outcomes, emitted)
    for chain_id, chain in sorted(scope.chains.items()):
        if chain.inception is None:
            holders = ", ".join(label for label, _ in chain.traveling + chain.leaves)
            f.error("orphan_chain_identity",
                    f"chain {chain_id} resolves to no signed ratification "
                    f"({holders}). It is refused as a fraud signal and never "
                    f"treated as an incomplete record awaiting completion")
    check_recorded_verdicts(f, scope, verdicts)


def check_recorded_verdicts(
        f: Findings, scope: Scope,
        verdicts: dict[str, tuple[dict[str, str], set[str]]]) -> None:
    """A gate that records a verdict is held to the walk this validator performs.
    A recorded PERMIT over a chain the walk refuses is the described-control defect
    written into the record itself; a recorded refusal this walk did not reach is
    a record stricter than its reader, which is a warning and not a fraud signal."""
    for label, doc in scope.leaves:
        if doc.get("leaf_type") != "gate_verdict":
            continue
        verdict = doc.get("verdict")
        if not isinstance(verdict, dict):
            f.error("act_unproven",
                    f"{label}: a gate-verdict leaf carries no verdict, so the "
                    f"verdict it exists to record is nowhere")
            continue
        resolved = verdicts.get(doc.get("chain_ref"))
        if resolved is None:
            continue
        computed, emitted = resolved
        walked_refusal = any(value != "pass" for value in computed.values())
        outcome = verdict.get("outcome")
        if outcome == "permitted" and walked_refusal:
            failing = sorted(name for name, value in computed.items()
                             if value != "pass")
            f.error("continuity_broken",
                    f"{label}: the leaf records `permitted` while this reader's "
                    f"walk refuses the chain at {failing}. A verdict is not "
                    f"evidence of the walk that produced it")
        elif outcome != "permitted" and not walked_refusal:
            f.warn("recorded-verdict-stricter",
                   f"{label}: the leaf records {outcome!r} over a chain this "
                   f"reader's walk finds whole; a record stricter than its reader "
                   f"is not a fraud signal, but the two should not disagree")
        recorded = {entry.get("check"): entry.get("outcome")
                    for entry in verdict.get("checks") or []
                    if isinstance(entry, dict)}
        for name in CHECK_NAMES:
            if name in recorded and recorded[name] != computed.get(name):
                f.error("continuity_broken",
                        f"{label}: the leaf records check {name} as "
                        f"{recorded[name]!r} and this reader's walk finds "
                        f"{computed.get(name)!r}")
        if outcome == "permitted" and "refusal" in verdict:
            f.error("continuity_broken",
                    f"{label}: a permitted verdict carries a refusal")
        if outcome != "permitted" and "refusal" not in verdict:
            f.error("continuity_broken",
                    f"{label}: a {outcome!r} verdict names no refusal, so it does "
                    f"not say what was lacking")
        # AND THE CODE MUST NAME THE REASON THE WALK ACTUALLY FOUND (Codex, P2 on
        # `eb1241fc`). The closed enumeration exists so a refusal names WHAT WAS
        # LACKING; a verdict free to record any enum-valid code while the walk
        # failed for another reason turns that enumeration into decoration, and
        # the false reason is what an operator would act on. Checking that a
        # `refusal` object merely EXISTS was the whole of the previous rule.
        recorded_code = get(verdict, "refusal", "code")
        if recorded_code is not None and emitted and recorded_code not in emitted:
            f.error("continuity_broken",
                    f"{label}: the leaf records the refusal "
                    f"{recorded_code!r} and this reader's walk refused for "
                    f"{sorted(emitted)}. A refusal that names the wrong reason is "
                    f"a record an operator would act on wrongly")


# --------------------------- rule: the declaration ---------------------------

def check_declarations(f: Findings, scope: Scope) -> None:
    """RULE (iv). Closed over the nine obligations IN BOTH DIRECTIONS: an
    obligation with no entry is refused, and so is an entry naming an obligation
    this capability does not have. An undeclared shortfall is non-conformance even
    where the identical shortfall, declared, would be conformant."""
    for label, doc in scope.declarations:
        entries = doc.get("obligations") or []
        named = [entry.get("obligation") for entry in entries
                 if isinstance(entry, dict)]
        # WHICH SET IS OWED IS DERIVED FROM THE DECLARATION AND NOT FROM A FLAG. A
        # declaration naming ANY tranche-two obligation is closed over all
        # EIGHTEEN; one naming none is closed over tranche one's NINE, exactly as
        # it was before this tranche existed. A realization cannot claim tranche
        # two and declare against nine, and a tranche-one declaration is not made
        # non-conformant by a capability that grew after it was written — which is
        # the BREAKING change `docs/contract-versioning-policy.md` reserves for a
        # major bump behind a full minor of deprecation warnings.
        owed = OBLIGATIONS if any(name in attestation.OBLIGATIONS for name in named) \
            else TRANCHE_ONE_OBLIGATIONS
        for obligation in owed:
            if named.count(obligation) != 1:
                f.error("residual_not_declared",
                        f"{label}: obligation {obligation} is declared "
                        f"{named.count(obligation)} times; this declaration is "
                        f"closed over the {len(owed)} obligations of the tranches it "
                        f"covers, because one that can quietly omit an obligation is "
                        f"how a silent gap gets recorded as conformance")
        for obligation in named:
            if obligation not in OBLIGATIONS:
                f.error("residual_not_declared",
                        f"{label}: {obligation!r} is not an obligation of this "
                        f"capability")
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            obligation = entry.get("obligation")
            satisfaction = entry.get("satisfaction")
            residual = entry.get("declared_residual")
            if satisfaction == "satisfied" and residual is not None:
                f.error("residual_not_declared",
                        f"{label}: {obligation} is recorded `satisfied` and also "
                        f"declares a residual; a satisfied obligation with a "
                        f"residual is a contradiction, not a nuance")
            if satisfaction != "satisfied" and residual is None:
                f.error("residual_not_declared",
                        f"{label}: {obligation} is recorded {satisfaction!r} and "
                        f"declares no residual. A gap recorded without saying what "
                        f"it is, and what closes it, is a gap that is implied "
                        f"rather than visible")
            if obligation in attestation.STRUCTURAL_RESIDUALS \
                    and satisfaction == "satisfied":
                f.error("residual_not_declared",
                        f"{label}: {obligation} cannot be recorded `satisfied` at "
                        f"this tranche. SEC-R17's residuals are structural — link "
                        f"7's per-seat signatures are outside this tranche's gate "
                        f"scope, and a file-based intake register cannot serve "
                        f"revocation-at-exercise — and SEC-R18 is UNMET rather than "
                        f"partially met until A RUNNING LAYER REFUSES a step whose "
                        f"inbound chain does not verify")
            if obligation in STRUCTURAL_RESIDUALS and satisfaction == "satisfied":
                f.error("residual_not_declared",
                        f"{label}: {obligation} cannot be recorded `satisfied` at "
                        f"this tranche. Its residual is structural — the pinned "
                        f"exercise record holds no signed digest value (SEC-R1), "
                        f"and suffix truncation no party has observed is invisible "
                        f"to a log with no external witness (SEC-R6) — and the "
                        f"realization DECLARES it rather than claiming coverage")
        reader = get(doc, "realization", "reader_required_check")
        if isinstance(reader, dict) and reader.get("is_required_in_ruleset") is not True:
            f.warn("reader-not-required",
                   f"{label}: the named reader "
                   f"{reader.get('check_name')!r} is NOT required in the branch "
                   f"ruleset, so this capability confers and refuses NOTHING and "
                   f"its records are documentation that governs nothing. A merged "
                   f"workflow file is not evidence that a check is required; the "
                   f"live ruleset state is")
            for entry in entries:
                if isinstance(entry, dict) and entry.get("obligation") == "SEC-R9" \
                        and entry.get("satisfaction") == "satisfied":
                    f.error("residual_not_declared",
                            f"{label}: SEC-R9 is recorded `satisfied` while the "
                            f"named reader is not required in the ruleset. Where no "
                            f"such check exists the requirement is UNMET, not "
                            f"partially met")


# --------------------------- orchestration of the rules ---------------------------

def validate_scope(f: Findings, records: list[tuple[str, dict]], registry: Registry,
                   docs: dict[str, dict], carried: dict[str, dict]) -> Scope:
    scope = build_scope(records)
    check_shapes(f, scope, registry, docs, carried)
    check_digests(f, scope)
    check_log(f, scope)
    check_leaf_signatures(f, scope)
    check_traveling_contracts_alone(f, scope)
    check_atomicity(f, scope)
    check_per_act_uniqueness(f, scope)
    check_chains(f, scope)
    check_declarations(f, scope)
    # TRANCHE TWO RUNS LAST, so a chain that fails at link 2 is not also told about
    # link 6: the tranche-one walk reports first, and the extended legs are part of
    # the SAME ONE WALK rather than a second gate reporting in parallel.
    attestation.check_tranche_two(f, scope.records, custody_models())
    return scope


_CUSTODY_MODELS: dict[str, dict] | None = None


def custody_models() -> dict[str, dict]:
    """The RATIFIED, CLOSED custody registry `add-trust-anchor` put in force at
    `contract-v1.37`, read rather than restated.

    Tranche two's evidence classes are a DIFFERENT AXIS from that registry's — it
    classes WHOSE ACT a signature evidences, they class WHERE A FACT INSIDE THE
    SIGNED PAYLOAD CAME FROM — and they compose in a declared ORDER: the signing
    certificate's custody ceiling BOUNDS what any fact under it evidences. Reading
    the members from the file is what keeps the two sets from drifting into two
    custody models."""
    global _CUSTODY_MODELS
    if _CUSTODY_MODELS is None:
        models: dict[str, dict] = {}
        if CUSTODY_REGISTRY.is_file():
            registry = load_yaml(CUSTODY_REGISTRY)
            for entry in (registry or {}).get("custody_models") or []:
                if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                    models[entry["id"]] = entry
        _CUSTODY_MODELS = models
    return _CUSTODY_MODELS


# --------------------------- layer 1: packaged corpus ---------------------------

def expected_failure(path: Path) -> tuple[str, str | None]:
    """A negative fixture declares the finding CODE it exists to provoke and MAY
    pin it further with a substring. The detail matters: `schema` is satisfied by
    any schema error whatsoever, so without it a fixture can be mutated into
    testing nothing while its self-test stays green."""
    code = detail = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# expected_failure:"):
            code = line.split(":", 1)[1].strip()
        elif line.startswith("# expected_failure_detail:"):
            detail = line.split(":", 1)[1].strip()
    if code is None:
        raise SystemExit(f"negative fixture missing '# expected_failure:' header: {path}")
    return code, detail


def codes_of(findings: list[str]) -> set[str]:
    return {match.group(1) for match in
            (re.match(r"ERROR \[([^]]+)]", line) for line in findings) if match}


def lines_for(findings: list[str], code: str) -> list[str]:
    return [line for line in findings if line.startswith(f"ERROR [{code}]")]


def labelled(prefix: str, path: Path) -> list[tuple[str, dict]]:
    records = load_records(path)
    if len(records) == 1:
        return [(f"{prefix}/{path.name}", records[0])]
    return [(f"{prefix}/{path.name}#{index}", doc)
            for index, doc in enumerate(records)]


def positive_records(directory: Path = None, prefix: str = "examples") -> list[tuple[str, dict]]:
    """Defaults to the tranche-one reference corpus, which is the signature the
    family's pytest wiring consumes; the self-test passes each corpus explicitly."""
    if directory is None:
        directory = EXAMPLES_DIR
    out: list[tuple[str, dict]] = []
    for path in sorted(directory.glob("*.example.yaml")):
        out.extend(labelled(prefix, path))
    return out


# TWO PACKAGED CORPORA, AND THE SPLIT IS FORCED BY THE LOG RATHER THAN CHOSEN.
# The transparency log's append-only property is a STORE obligation over the WHOLE
# log: one leaf per position, no holes, every leaf hash-linked to the one before.
# Tranche one's negatives append their probe leaf at position 4, the first free
# slot after its four-leaf reference log — so a tranche-two chain sharing that
# store would have taken position 4 and turned thirty-four shipped fixtures into
# index collisions, each then refusing for `leaf_hash_link_broken` instead of the
# invariant it is named for. Re-numbering them is not available either: their leaf
# signatures are over the leaf content, and the fixture key's private half exists
# nowhere in this repository, exactly as tranche one intended.
#
# SO TRANCHE TWO SHIPS ITS OWN STORE, and each corpus is adjudicated ALONE. Every
# rule runs over both — tranche one's eight checks walk the tranche-two chains'
# links 1-3 exactly as they walk their own — and the refusal-code coverage the
# self-test demands is the UNION, so no code goes unprobed because it lives in the
# other corpus.
CORPORA = [
    ("examples", EXAMPLES_DIR, NEGATIVE_DIR),
    ("examples/tranche-two", EXAMPLES_DIR / "tranche-two",
     EXAMPLES_DIR / "tranche-two" / "negative"),
]


def self_test(f: Findings, registry: Registry, docs: dict[str, dict],
              carried: dict[str, dict]) -> None:
    probed: set[str] = set()
    total_base = neg_ok = 0
    for prefix, positives_dir, negatives_dir in CORPORA:
        if not positives_dir.is_dir():
            f.error("examples-missing", f"{positives_dir} not found")
            continue
        base = positive_records(positives_dir, prefix)
        if not base:
            f.error("examples-missing",
                    f"no packaged positive examples found in {positives_dir}")
            continue
        total_base += len(base)
        local = Findings()
        validate_scope(local, base, registry, docs, carried)
        f.errors.extend(f"{line} [expected a valid corpus]" for line in local.errors)
        f.warnings.extend(local.warnings)

        if not negatives_dir.is_dir():
            f.error("examples-missing", f"{negatives_dir} not found")
            continue
        for path in sorted(negatives_dir.glob("*.yaml")):
            code, detail = expected_failure(path)
            probe = Findings()
            validate_scope(probe, base + labelled(f"{prefix}/negative", path),
                           registry, docs, carried)
            found = codes_of(probe.errors)
            if not probe.errors:
                f.error("negative-should-fail",
                        f"{prefix}/negative/{path.name}: expected invalid, "
                        f"validated cleanly")
            elif code not in found:
                f.error("negative-wrong-reason",
                        f"{prefix}/negative/{path.name}: expected finding {code!r}, "
                        f"got {sorted(found)}")
            elif detail and not any(detail in line for line in lines_for(probe.errors, code)):
                f.error("negative-wrong-reason",
                        f"{prefix}/negative/{path.name}: finding {code!r} fired but "
                        f"not for {detail!r} — the fixture no longer tests the "
                        f"invariant it is named for: {lines_for(probe.errors, code)}")
            else:
                neg_ok += 1
                probed.add(code)
    unprobed = sorted(REFUSAL_CODES - probed)
    if unprobed:
        f.error("refusal-code-without-probe",
                f"the closed refusal enumeration declares {unprobed} and no "
                f"packaged negative provokes them. A refusal this reader can emit "
                f"and no fixture ever exercises is a refusal nobody has seen work")
    f.note(f"self-test: {total_base} packaged record(s) validated across "
           f"{len(CORPORA)} coherent corpora, {neg_ok} negative fixture(s) "
           f"confirmed invalid for their intended reason, "
           f"{len(probed & REFUSAL_CODES)}/{len(REFUSAL_CODES)} "
           f"closed refusal codes red-proven "
           f"({len(probed - REFUSAL_CODES)} further finding code(s) probed, for the "
           f"obligations refused BY SHAPE, where unrepresentable is stronger "
           f"than refused)")


# --------------------------- layer 2: real artifacts ---------------------------

SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__", ".venv"}


#: The identifier each consumed record is RESOLVED THROUGH. `add-trust-anchor`
#: owns these fields; they are named here only to detect an ambiguous set, never
#: to restate the vocabulary.
CONSUMED_ID_FIELD = {
    "xfactory_certificate_record": "certificate_id",
    "xfactory_certificate_issuance_evidence": "issuance_evidence_id",
    "xfactory_trust_anchor": "anchor_id",
}


def check_consumed_identifiers_are_unambiguous(
        f: Findings, records: list[tuple[str, dict]]) -> None:
    """AN AMBIGUOUS CONSUMED SET IS REFUSED, NEVER RESOLVED BY FILE ORDER.

    The consumed records are resolved THROUGH THEIR IDENTIFIERS, and the view
    that resolves them keeps the last document it saw. In a curated corpus that
    is harmless; over an ARBITRARY CHECKOUT it means two certificates, issuance
    evidences or anchors sharing an id let lexicographic file order decide which
    fingerprint, which issuance act or which anchor a tier-2 signature verifies
    against — the substitution `add-trust-anchor`'s own reader refuses as
    `record-id-duplicate` on every copy, and the same substitution this reader
    already refuses one vocabulary over, where a key id two wallets claim
    differently is AMBIGUOUS rather than last-seen.

    It is checked at the SWEEP rather than in the shared scope builder because
    the sweep is where an uncurated set can arise: the packaged corpora are
    adjudicated by layer 1, which would report a duplicate there as the corpus
    defect it would be.
    """
    seen: dict[tuple[str, str], list[str]] = {}
    for label, doc in records:
        kind = doc.get("kind") if isinstance(doc, dict) else None
        field = CONSUMED_ID_FIELD.get(kind) if isinstance(kind, str) else None
        if field is None:
            continue
        identifier = doc.get(field)
        if isinstance(identifier, str) and identifier:
            seen.setdefault((kind, identifier), []).append(label)
    for (kind, identifier), labels in sorted(seen.items()):
        if len(labels) > 1:
            f.error("consumed-record-id-duplicate",
                    f"{', '.join(labels)}: {len(labels)} {kind} records in the "
                    f"scanned tree declare identity {identifier!r}. Resolution "
                    f"through an id is last-write-wins, so a duplicate could swap "
                    f"the certificate a fingerprint is compared against, the "
                    f"issuance act a composition is discharged by, or the anchor a "
                    f"certificate hangs from — refused on EVERY copy rather than "
                    f"resolved by file order, because an ambiguous identity is not "
                    f"a resolved one")


def repo_scan(f: Findings, target: Path, registry: Registry, docs: dict[str, dict],
              carried: dict[str, dict]) -> None:
    sweep = target.is_dir()
    files = sorted(list(target.rglob("*.yaml")) + list(target.rglob("*.yml"))) \
        if sweep else [target]
    records: list[tuple[str, dict]] = []
    checked = skipped = 0
    for path in files:
        if set(path.parts) & SKIP_DIR_NAMES:
            continue
        # Exclude ANY packaged corpus, not only this checkout's: a domain repo
        # that vendors openxFactory scans a COPY, and matching this checkout's
        # absolute paths would re-adjudicate every vendored negative as a live
        # record.
        if "examples" in path.parts and "signed-execution-chain" in path.parts:
            continue
        # And the same for the CONSUMED family's packaged corpus: trust-anchor's
        # examples/ carries deliberately-invalid negatives that ITS reader
        # adjudicates. Sweeping them here as live consumed records would
        # re-adjudicate another family's fixtures — the same mistake the
        # exclusion above prevents, one family over.
        if "examples" in path.parts and "trust-anchor" in path.parts:
            continue
        try:
            documents = load_records(path)
        except yaml.YAMLError as exc:
            # A whole-checkout sweep is not the place to adjudicate unrelated
            # YAML: a file that does not parse cannot carry a family kind. An
            # explicitly named file is a different matter.
            if sweep:
                skipped += 1
                continue
            f.error("yaml", f"{path}: parse failure: {exc}")
            continue
        name = str(path.relative_to(target) if sweep else path)
        for index, doc in enumerate(documents):
            # THE CONSUMED trust-anchor KINDS ARE COLLECTED TOO — found by the
            # 5.8 canary build, which is what a canary is for. A tier-2
            # identity's issuance COMPOSES the certificate record and the
            # issuance evidence, and a scan that dropped every kind outside the
            # family's own would refuse EVERY real chain as a forged identity:
            # the records that discharge the composition could never reach the
            # scope that resolves them. They are collected into scope exactly as
            # the packaged corpora already load them, and validated against the
            # same carried canonical schemas.
            # THE `kind` IS TYPE-GUARDED BEFORE IT IS LOOKED UP, because a sweep
            # reads ARBITRARY YAML and `{"a": 1} in some_dict` raises rather than
            # returning False. A document writing `kind: [a, b]` crashed the whole
            # scan and discarded every other file's findings — a required gate
            # felled by one unrelated file. Every key in both maps is a string, so
            # a non-string kind is a skip by construction.
            kind = doc.get("kind") if isinstance(doc, dict) else None
            if not isinstance(kind, str) or (
                    kind not in KIND_TO_SCHEMA
                    and kind not in CONSUMED_KIND_TO_SCHEMA):
                skipped += 1
                continue
            checked += 1
            records.append(
                (name if len(documents) == 1 else f"{name}#{index}", doc))
    check_consumed_identifiers_are_unambiguous(f, records)
    if records:
        validate_scope(f, records, registry, docs, carried)
    f.note(f"repo scan ({target}): {checked} artifact(s) checked, {skipped} skipped "
           f"(no kind this reader adjudicates — neither one of this family's own "
           f"nor one of the CONSUMED trust-anchor kinds a tier-2 issuance composes); "
           f"BOTH families' packaged examples/ excluded, this one's and "
           f"trust-anchor's (each family's layer 1 owns its own). ZERO real "
           f"artifacts is the expected state until "
           f"the first ratification is incepted under this capability — inception "
           f"is a human act with a wallet-held key, and this realization mints no "
           f"chain")


# --------------------------- orchestration ---------------------------

def report(f: Findings, strict: bool) -> int:
    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)
    print(f"\nvalidate-signed-execution-chain: {len(f.errors)} error(s), "
          f"{len(f.warnings)} warning(s)")
    return 1 if f.errors or (strict and f.warnings) else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", nargs="?", default=None,
                        help="repo checkout (or single file) to scan for real "
                             "signed-execution-chain artifacts; omit to self-test only")
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as errors")
    parser.add_argument("--require-pinned-wallet-vocabulary", action="store_true",
                        help="refuse when the pinned openXwallet schemas are not "
                             "reachable, instead of falling back to the members "
                             "this capability restricts")
    args = parser.parse_args()

    if not CONTRACT_DIR.is_dir():
        print(f"ERROR {CONTRACT_DIR} not found", file=sys.stderr)
        return 2
    try:
        registry, docs = build_registry()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR schema load failure: {exc}", file=sys.stderr)
        return 2

    f = Findings()
    for name, doc in docs.items():
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as exc:  # noqa: BLE001
            f.error("schema-meta-invalid", f"{name}: {exc}")
        if not doc.get("$schema") or not doc.get("$id"):
            f.error("schema-identity-missing",
                    f"{name}: every schema in this family declares its dialect "
                    f"($schema) and an absolute $id, so a consumer's stock "
                    f"validator resolves the bundle the same way this one does")
    carried = load_carried_schemas(f, args.require_pinned_wallet_vocabulary)

    try:
        self_test(f, registry, docs, carried)
        if args.path is not None:
            target = Path(args.path).resolve()
            if not target.exists():
                print(f"ERROR path {target} not found", file=sys.stderr)
                return 2
            repo_scan(f, target, registry, docs, carried)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2
    return report(f, args.strict)


if __name__ == "__main__":
    sys.exit(main())
