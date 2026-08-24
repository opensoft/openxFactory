#!/usr/bin/env python3
"""Validate the openxWallet contract families (add-openxwallet).

The openxFactory-owned canonical validator for the seven kinds across the
holder-agnostic core (`contracts/openxwallet/`, six kinds) and its first
profile (`contracts/openxwallet-agent-profile/`, one). Run from the pinned
openxFactory checkout, never copied into a domain repo:

    python3 scripts/validate-openxwallet.py [REPO_PATH] [--strict]

Two layers run:

1. Packaged reference corpus (`contracts/openxwallet*/examples/`): the
   canonical custody registry and every `*.example.yaml` must pass schema
   conformance AND every cross-shape rule; every file under `negative/` must
   FAIL for its INTENDED reason, declared in its own first lines as
   `# expected_failure: <code>` with an optional
   `# expected_failure_detail: <substring>` pin and a required
   `# requirement: <REQ-ID>` attribution. The detail pin matters because
   several cases would otherwise collapse into a generic `schema` finding and
   stop testing the invariant they are named for.

   Coverage is closed in both directions: every requirement in REQUIREMENTS
   must carry at least one negative confirmation, and every requirement id a
   fixture claims must exist. A requirement cannot quietly lose its probe.

2. Optional real artifacts under REPO_PATH: every `*.y*ml` whose `kind` is one
   of the family kinds is validated. Other kinds are skipped and counted; the
   packaged corpus is excluded so a whole-repo sweep does not re-adjudicate
   the negatives as though they were live records, and cross-record
   references resolve against the scanned repo's OWN records plus the
   canonical custody registry, never against the packaged examples — a
   teaching fixture must not resolve a live reference, nor collide with a
   consumer's DID-scoped key_ids.

The rules the shapes cannot express:

  (a) NO KEY MATERIAL, AT ANY DEPTH. A wallet is a key REFERENCE. The schemas
      close every object so no key-shaped PROPERTY can be added, but a
      conformant shape can still carry a PEM block inside a string field that
      legitimately exists — so this walks names AND values. A raw key can be
      neither expired nor revoked and a shared key destroys attribution, which
      is why this is unrepresentable rather than discouraged (core R1).

  (b) CUSTODY `evidences` IS DERIVED, NEVER ASSERTED. evidences = holder iff
      the key is NOT readable by the holder's execution context AND each use
      requires an authorization that context cannot supply; environment
      otherwise. A member readable by its own execution context that claims to
      evidence the HOLDER is refused. This is the enumeration failure the
      ruling of 2026-08-07 exists to prevent, and it must not be able to
      validate cleanly (core R4).

  (c) THE HIGHEST TIER MUST BE EARNED. Only custody evidencing the HOLDER may
      reach the top of the declared ladder — the tier where nothing stands
      between the holder and an irreversible effect. Keyed on RANK, not on the
      tier's name: a registry that renamed `act_unsupervised` would otherwise
      slip an environment-evidencing model into the top tier and validate
      cleanly, which is this rule's own failure mode (core R4).

  (d) NO CUSTODY COLLAPSE. Every member readable by the holder's execution
      context must rank STRICTLY BELOW every member evidencing the holder.
      This is the handoff's failure mode stated as a check: without it the
      readable case could claim the isolated case's authority (core R4).

  (e) CUSTODY CAPS AUTHORITY. A grant's tier may not exceed the ceiling of the
      custody its audience wallet declares; raising authority is a custody
      question, not a trust assertion (core R4).

  (f) ATTENUATION IS MONOTONIC. A derived grant's acts and objects are subsets
      of its parent's, its tier is at or below the parent's, and its expiry is
      at or before the parent's. Widening any dimension is refused (core R2).

  (g) ONE AUTHORITY VOCABULARY. A grant scope's `approval_posture` draws its
      keys from the neutral job envelope's `approval_policy` properties, READ
      OUT OF `contracts/schemas/hermes-job-envelope.schema.yaml` AT RUN TIME
      rather than restated here — restating them would recreate the second
      vocabulary the requirement forbids. A key outside that set is a parallel
      authority vocabulary (profile R3).

  (h) POSTURE AND TIER AGREE. `hermes_approval_required_before_apply: false`
      requires tier `act_unsupervised`; `authority_agents_may_approve: true`
      requires tier `act` or above. The two are one vocabulary, so they cannot
      be allowed to disagree (profile R3).

  (i) PROOF OF POSSESSION, NOT PRESENTATION. An exercise without a presented
      proof may not be permitted, and its refusal must name the MISSING PROOF
      rather than a missing grant — the grant was supplied and is not what was
      lacking (core R3).

  (j) A VERIFICATION FAILURE IS NOT AN ABSENCE. `event_class` must match what
      the proof block actually records. A presented-but-unverified signature
      recorded as an unauthenticated request destroys the distinction that
      makes a stolen grant visible (core R3).

  (k) ATTRIBUTION IS NOT LAUNDERED. A key-attributed exercise names its
      presenting key; an exercise with no establishable wallet key is
      `unattributed` and names no holder; a shared credential is recorded as
      transport and never as the actor (core R5).

  (l) REVOCATION IS CHECKED AT USE. The check must be performed at exercise,
      and an exercise against a revoked grant — or one derived from a revoked
      ancestor, or held by a wallet whose standing was revoked — may not be
      permitted. Issuance-time validity is not evidence of current validity
      (core R6).

  (m) DISTINCT-HOLDER CONSTRAINTS BIND WHERE DECLARED. An evaluation naming
      the same holder for both acts is unsatisfied, and an unsatisfied
      evaluation may not be permitted. Available, never implied: an exercise
      declaring no evaluation is subject to none (core R7).

  (n) NEVER AN IDENTITY SUBSTRATE. A subject attestation resolves through the
      subject's own identifier and declares itself reconstructable without a
      wallet. A wallet identifier that becomes a subject identifier breaks two
      RATIFIED MedxFactory constraints (core R8).

  (o) A COMPOSITION HASH NAMES WHAT IT COVERS. The component set is required
      and non-empty, and each component's binding mode carries the evidence
      that mode needs: `content` a digest, `reference` a corpus ref AND the
      digest of the configuration governing how it is consulted (profile R1).

  (p) A DECLARED CHANGE REVOKES IMMEDIATELY. An attested hash differing from
      the declared hash may not be recorded alongside live grants. No
      threshold, score, or tolerance band is consulted (profile R2).

  (q) COMPOSITION BELONGS TO THE AGENT PROFILE ONLY. A composition record must
      resolve to a wallet whose holder class is `agent` — a wallet that does
      not resolve is refused rather than passed over, because an unresolvable
      wallet is a class check that never runs; the core imposes composition on
      no class (profile R1).

  (r) AN EXERCISE BINDS TO ITS GRANT. The grant must resolve; the act must be
      one the grant confers; the presenting wallet must be the grant's
      audience; and the custody recorded in force must be the custody that
      wallet declares. The presenting wallet is DERIVED from the presenting
      key through the corpus's wallet records, never read from the record's
      own attribution block alone — a self-declared ref could be omitted
      (skipping the binding) or could name the audience while another
      wallet's key was presented (passing the binding on a lie). The binding
      key is the VERIFIED proof block's key when one is recorded: an
      attribution key contradicting it is laundering, a verified presented
      key on an act recorded 'unattributed' is laundering, a presenting key
      no wallet declares is refused rather than passed over, and a key
      declared by more than one wallet (key_id is DID-scoped) is refused as
      ambiguous rather than resolved by file order.
      Without these an exercise can cite a grant that does not exist, perform
      an act never conferred, be presented by a wallet the grant does not
      address, or claim evidence its own custody cannot supply — and every
      rule downstream then adjudicates a fiction (core R3, R5).

  (s) A WALLET'S DECLARED CUSTODY IS IN THE CLOSED SET. Checking custody only
      where an exercise reports a model in force left the DECLARATION
      unchecked, so a wallet could name a model no registry contains and every
      ceiling derived from it resolved to nothing — the cap failing open at the
      one point it is supposed to bind (core R4).

  (t) THE ISSUER IS RECORDED AND ROOTS ARE ANCHORED. A REVIEW-class grant —
      membership decided by scope content alone: the canonical review act
      token appearing in scope.acts — names issued_by, and a ROOT such grant
      (no parent_grant_ref) names no issuer but the responsible operator,
      exact-match, no normalization. A root issuer's authority to issue cannot
      be conferred by the register the grant writes into; it is standing under
      the Human Escalation Contract, which the anchor constant cites rather
      than restates. Machine-named issuers are refused with their own wording,
      and the legacy org string every pre-S2 example carries does NOT
      grandfather into the anchor (review-authority intake).

WHAT THIS VALIDATOR DELIBERATELY DOES NOT DO

It does not verify signatures, resolve DIDs, contact a key store, or check
that a DECLARED custody model is the REAL one. Custody declaration is what
keeps this contract honest, and it works only if consumers declare truthfully;
a validator can check that a model is declared and that authority does not
exceed it, and cannot check that the declaration is true. It creates no key,
credential, wallet, runtime, or issuance service.

Exit codes: 0 ok, 1 findings, 2 harness error.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover
    print("ERROR jsonschema>=4.18 is required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "contracts" / "openxwallet"
PROFILE_DIR = ROOT / "contracts" / "openxwallet-agent-profile"
FAMILY_DIRS = (CORE_DIR, PROFILE_DIR)
CUSTODY_REGISTRY_PATH = CORE_DIR / "openxwallet-custody.registry.yaml"
ENVELOPE_SCHEMA_PATH = ROOT / "contracts" / "schemas" / "hermes-job-envelope.schema.yaml"

# Rule (t). The review-authority intake composes this capability rather than
# extending it, so its two restrictions live HERE as named constants instead of
# in any schema. The class marker is the canonical review act token from
# review-authority-intake requirement 1 ("scope.acts names the review act");
# membership in a grant's scope.acts is what makes the grant REVIEW-class, and
# nothing else can trigger the class. The anchor token is the responsible
# operator's identity, ruled exact-match by the convener (2026-08-23); its
# AUTHORITY is not asserted here but cited — the operator's standing to issue
# root review-authority grants is recorded under the Human Escalation
# Contract, and this code points at that standing record rather than
# duplicating or re-deriving it.
# Contract note: the anchor token is the operator's email address. The grant
# schema's original identifier grammar could not carry one (no `@`), which the
# anchored-root self-test assertion caught before merge; the convener
# re-ruled 2026-08-24: token = Brett.Heap@opensoft.one AND a schema widening
# (issuer_identifier def) authorized for exactly this field. The initial
# display-name ruling `Brett Heap` is superseded.
REVIEW_ACT_TOKEN = "review"
ROOT_ISSUER_OPERATOR_TOKEN = "Brett.Heap@opensoft.one"
ISSUER_ANCHOR_AUTHORITY = "docs/roles-and-authority.md:103-140"
# Detail-pin classification ONLY: a machine-shaped issuer value gets the
# machine-named refusal wording. This regex never weakens the rule — every
# non-exact value is refused regardless of shape — it only says WHY the value
# cannot be the anchor. A bare prefix followed by a long hex blob is how the
# subject ids and key handles in this ecosystem name machines; a human name
# does not look like this, and the legacy org string does not either.
_MACHINE_ISSUER_RE = re.compile(r"^[a-z][a-z0-9]*-[0-9a-f]{8,}$", re.IGNORECASE)
_LEGACY_ORG_ISSUER = "opensoft"

KIND_TO_SCHEMA = {
    "xfactory_wallet_record": "openxwallet-record.schema.yaml",
    "xfactory_wallet_custody_registry": "openxwallet-custody-registry.schema.yaml",
    "xfactory_wallet_grant": "openxwallet-grant.schema.yaml",
    "xfactory_wallet_grant_exercise": "openxwallet-grant-exercise.schema.yaml",
    "xfactory_wallet_distinct_holder_constraint":
        "openxwallet-distinct-holder-constraint.schema.yaml",
    "xfactory_wallet_subject_attestation":
        "openxwallet-subject-attestation.schema.yaml",
    "xfactory_wallet_agent_composition":
        "openxwallet-agent-composition.schema.yaml",
}

# The identity field per indexed kind. A duplicated id is refused on every
# copy (rule backing: index tables are last-write-wins, so a duplicate could
# swap the wallet key, grant scope, or constraint a reference resolves to).
_ID_FIELDS = {
    "xfactory_wallet_record": "wallet_id",
    "xfactory_wallet_grant": "grant_id",
    "xfactory_wallet_distinct_holder_constraint": "constraint_id",
}

# The closed requirement list both capabilities' spec deltas define. Every one
# of these MUST carry at least one negative confirmation in the packaged
# corpus; that closure is what makes this a negative confirmation PER
# REQUIREMENT rather than a pile of negatives.
REQUIREMENTS: dict[str, str] = {
    "OXW-R1": "A wallet is a key, never a record of a key",
    "OXW-R2": "Authority travels as attenuated grants, never as keys",
    "OXW-R3": "Use requires proof of possession, not presentation",
    "OXW-R4": "Custody is declared and bounds what a signature evidences",
    "OXW-R5": "Every exercise is key-attributed",
    "OXW-R6": "Revocation propagates through the chain",
    "OXW-R7": "Distinct-holder constraints are expressible",
    "OXW-R8": "The capability is an authority control, never an identity substrate",
    "OXWA-R1": "An agent holder declares its composition",
    "OXWA-R2": "A composition change revokes the agent's grants immediately",
    "OXWA-R3": "Agent authority is grant scope, not a parallel vocabulary",
    # The review-authority intake family (rule (t)). Same pattern as the
    # profile prefix above: one capability, one prefix, one row per
    # independently probed invariant.
    "OXWR-R1": "Every review-authority grant names its issuer",
    "OXWR-R2": ("A root review-authority grant's issuer is anchored outside "
                "the register"),
}

SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__", ".venv"}

FORMAT_CHECKER = FormatChecker()
if not {"date", "date-time"} <= set(FORMAT_CHECKER.checkers):  # pragma: no cover
    print(
        "ERROR jsonschema is missing its date/date-time format checkers; "
        "install rfc3339-validator (see "
        "requirements/hermes-runtime-contracts.in) so `format: date` and "
        "`format: date-time` are enforced",
        file=sys.stderr,
    )
    sys.exit(2)

# Rule (a). Property names that could only be carrying key material, and value
# shapes that are key material whatever the property is called.
_KEY_NAME_TOKENS = (
    "private", "secret", "mnemonic", "passphrase", "pkcs8", "key_material",
    "keymaterial", "privkey", "seed_phrase",
)
_KEY_NAME_ALLOW = {
    "key_id", "key_ref", "wallet_ref", "presenting_key_ref",
    "public_key_multibase", "signature_algorithm",
}
# Armor labels vary (`RSA`, `EC`, `OPENSSH`, `PGP … BLOCK`), and matching only
# the bare `PRIVATE KEY-----` form let a PGP block through in the same field
# the shipped fixture uses. Digits appear in some labels, so allow them too.
_KEY_VALUE_RE = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY(?: BLOCK)?-----", re.I)
# A serialized JWK: `d` is the private exponent. The letter alone is far too
# generic to blocklist, but alongside `kty` it is unambiguous.
_JWK_PRIVATE_RE = re.compile(
    r'"kty"\s*:.*"d"\s*:\s*"|"d"\s*:\s*".*"kty"\s*:', re.S)

_EXPECTED_RE = re.compile(r"^#\s*expected_failure:\s*(\S+)\s*$")
_DETAIL_RE = re.compile(r"^#\s*expected_failure_detail:\s*(.+?)\s*$")
_REQUIREMENT_RE = re.compile(r"^#\s*requirement:\s*(\S+)\s*$")


# --------------------------- findings ---------------------------

class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"ERROR [{code}] {msg}")

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"WARN  [{code}] {msg}")

    def note(self, msg: str) -> None:
        line = f"note  {msg}"
        if line not in self.notes:  # notes are facts about the run, not events
            self.notes.append(line)


def codes_of(findings: list[str]) -> set[str]:
    out = set()
    for line in findings:
        m = re.match(r"ERROR \[([^]]+)]", line)
        if m:
            out.add(m.group(1))
    return out


def lines_for(findings: list[str], code: str) -> list[str]:
    return [x for x in findings if x.startswith(f"ERROR [{code}]")]


# --------------------------- loading ---------------------------

def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_schemas() -> dict[str, dict]:
    docs: dict[str, dict] = {}
    for family in FAMILY_DIRS:
        for path in sorted(family.glob("*.schema.yaml")):
            docs[path.name] = load_yaml(path)
    return docs


def validator_for(kind: str, docs: dict[str, dict]) -> Draft202012Validator:
    return Draft202012Validator(
        docs[KIND_TO_SCHEMA[kind]], format_checker=FORMAT_CHECKER)


def approval_policy_vocabulary() -> dict[str, str]:
    """Rule (g): the legal approval-scope terms, READ from the canonical job
    envelope rather than restated. Restating them here would recreate the
    parallel vocabulary the requirement exists to forbid."""
    doc = load_yaml(ENVELOPE_SCHEMA_PATH)
    node = doc["properties"]["job"]["properties"]["approval_policy"]["properties"]
    return {name: (spec or {}).get("type", "") for name, spec in node.items()}


def parse_time(value: str) -> datetime | None:
    """Parse an ISO timestamp, ALWAYS returning an aware datetime.

    A naive value compared against an aware one raises TypeError, and a
    TypeError here would abort the whole run as a harness error — discarding
    every finding from every other file and reporting 'harness failure' where
    CI needed 'findings'. A value with no offset is read as UTC; the schema's
    `format: date-time` is what refuses the malformed value itself.
    """
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _mapping(value: Any) -> dict:
    """A dict, or {} for anything else. Cross-record rules run even on
    documents the schema has refused (findings accumulate; validation does
    not stop), so every block read must tolerate a non-mapping without
    crashing the run and discarding every other file's findings."""
    return value if isinstance(value, dict) else {}


def _sequence(value: Any) -> list:
    """A list, or [] for anything else — the sequence twin of `_mapping`.
    `value or []` passes a truthy scalar straight to iteration, so a
    schema-invalid `constraint_evaluations: 1` crashed the run before its
    schema finding could be reported."""
    return value if isinstance(value, list) else []


def _hashable(value: Any) -> bool:
    """True when the value can be a dict key or set member. Enumerating
    unhashable TYPES undercounts — PyYAML's safe `!!set` tag yields a Python
    set, exactly as unhashable as a list — so ask the only authority there
    is: hash() itself."""
    try:
        hash(value)
    except TypeError:
        return False
    return True


def _hashable_set(values: Any) -> set:
    """The hashable members of a list, or an empty set. Set arithmetic over
    doc-supplied lists must not crash on an unhashable member; the schema
    finding on the malformed document is the report, not a harness error."""
    if not isinstance(values, list):
        return set()
    return {v for v in values if _hashable(v)}



# --------------------------- corpus context ---------------------------

class Context:
    """Everything a cross-record rule needs: the canonical custody registry,
    the approval vocabulary, and an index of records by id."""

    def __init__(self, registry: dict, vocabulary: dict[str, str]) -> None:
        self.registry = registry
        self.vocabulary = vocabulary
        self.tier_rank: dict[str, int] = {
            t["id"]: t["rank"] for t in registry.get("authority_tiers", [])
            if isinstance(t, dict) and "id" in t and "rank" in t
        }
        self.custody: dict[str, dict] = {
            m["id"]: m for m in registry.get("custody_models", [])
            if isinstance(m, dict) and "id" in m
        }
        self.wallets: dict[str, dict] = {}
        self.grants: dict[str, dict] = {}
        self.constraints: dict[str, dict] = {}
        # key_id -> [wallet_id, ...]. The audience binding derives the
        # presenting wallet FROM THE PRESENTING KEY through this index;
        # reading only the record's self-declared `attribution.wallet_ref`
        # let an exercise skip the binding by omitting one optional field.
        # A LIST, not a single id: `key_id` names a key within its DID
        # anchor, so two wallets may legally share one, and collapsing them
        # would resolve an exercise's bare key reference by file order.
        self.wallets_by_key: dict[str, list[str]] = {}
        # (kind, id) pairs declared by MORE THAN ONE record. Index tables are
        # last-write-wins, so without this a duplicated id silently swaps the
        # wallet key, grant scope, or constraint a reference resolves to —
        # the duplicate is refused on every copy instead.
        self.duplicate_ids: set[tuple[str, str]] = set()

    def index(self, doc: dict) -> None:
        """Type-guarded: repo scans index BEFORE schema validation, so a
        malformed document must surface as a schema finding on its own file,
        never as a harness crash that discards every other file's findings."""
        kind = doc.get("kind")
        if kind == "xfactory_wallet_record":
            wid = doc.get("wallet_id")
            if isinstance(wid, str) and wid:
                if wid in self.wallets:
                    self.duplicate_ids.add((kind, wid))
                self.wallets[wid] = doc
                key_ref = doc.get("key_reference")
                key_id = key_ref.get("key_id") if isinstance(key_ref, dict) else None
                if isinstance(key_id, str) and key_id:
                    holders = self.wallets_by_key.setdefault(key_id, [])
                    if wid not in holders:
                        holders.append(wid)
        elif kind == "xfactory_wallet_grant":
            gid = doc.get("grant_id")
            if isinstance(gid, str) and gid:
                if gid in self.grants:
                    self.duplicate_ids.add((kind, gid))
                self.grants[gid] = doc
        elif kind == "xfactory_wallet_distinct_holder_constraint":
            cid = doc.get("constraint_id")
            if isinstance(cid, str) and cid:
                if cid in self.constraints:
                    self.duplicate_ids.add((kind, cid))
                self.constraints[cid] = doc

    def rank(self, tier: str) -> int | None:
        return self.tier_rank.get(tier) if isinstance(tier, str) else None

    def ceiling_for_wallet(self, wallet_ref: str) -> tuple[str, str] | None:
        """(custody_model_id, ceiling_tier) for a wallet, or None."""
        if not isinstance(wallet_ref, str):
            return None
        wallet = self.wallets.get(wallet_ref)
        if not wallet:
            return None
        model = _mapping(wallet.get("custody")).get("model")
        member = self.custody.get(model) if isinstance(model, str) else None
        if not member:
            return None
        return model, member.get("authority_ceiling", "")


# --------------------------- rule (a): key material ---------------------------

def check_no_key_material(f: Findings, label: str, node: Any,
                          path: str = "") -> None:
    if isinstance(node, dict):
        # A JWK carries its private exponent under the single letter `d`, which
        # is far too generic a property name to blocklist on its own — but
        # alongside `kty` it is unambiguous, and it is how a key most plausibly
        # arrives as structured data rather than as armored text.
        if "kty" in node and "d" in node:
            f.error("key-material-embedded",
                    f"{label}: object at {path or '<root>'!r} is a JWK carrying "
                    f"its private exponent 'd'; a wallet references a key and "
                    f"never carries one")
        for name, value in node.items():
            here = f"{path}.{name}" if path else str(name)
            lname = str(name).lower()
            if lname not in _KEY_NAME_ALLOW and any(
                    tok in lname for tok in _KEY_NAME_TOKENS):
                f.error("key-material-embedded",
                        f"{label}: property {here!r} is key-material-shaped; a "
                        f"wallet record references a key and never carries one")
            check_no_key_material(f, label, value, here)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            check_no_key_material(f, label, item, f"{path}[{i}]")
    elif isinstance(node, str):
        if _KEY_VALUE_RE.search(node):
            f.error("key-material-embedded",
                    f"{label}: value at {path!r} contains a private key block; "
                    f"the property is conformant but the VALUE is key material")
        elif _JWK_PRIVATE_RE.search(node):
            f.error("key-material-embedded",
                    f"{label}: value at {path!r} is a serialized JWK carrying "
                    f"its private exponent 'd'; every object in this family is "
                    f"closed, so a JWK can only arrive as a STRING — which is "
                    f"exactly why the value scan has to look for one")


# --------------------------- rules (b)-(d): the custody registry ---------------------------

def check_custody_registry(f: Findings, label: str, doc: dict) -> None:
    models = _sequence(doc.get("custody_models"))
    # Ranks restricted to ints: a malformed rank would otherwise reach the
    # collapse comparison and crash the run instead of reporting the
    # registry's own schema finding. A tier dropped here makes ceilings
    # naming it 'unknown', which fails closed alongside that finding.
    tiers = {t.get("id"): t.get("rank") for t in _sequence(doc.get("authority_tiers"))
             if isinstance(t, dict) and _hashable(t.get("id"))
             and isinstance(t.get("rank"), int)}
    # Rule (c) keys on the TOP RANK rather than on the id `act_unsupervised`.
    # Naming the tier would make the rule depend on a string a registry is free
    # to choose, so renaming the top tier would silently disable the check —
    # the same "it all validates cleanly" failure this family exists to refuse.
    top_rank = max((r for r in tiers.values() if isinstance(r, int)), default=None)

    seen_ids: set[str] = set()
    for member in models:
        if not isinstance(member, dict):
            continue
        mid = member.get("id") if isinstance(member.get("id"), str) else "<unnamed>"
        if mid in seen_ids:
            f.error("custody-duplicate-member",
                    f"{label}: custody model {mid!r} declared twice")
        seen_ids.add(mid)

        readable = member.get("key_readable_by_holder_execution_context")
        per_use = member.get(
            "use_requires_authorization_outside_holder_execution_context")
        declared = member.get("evidences")

        # (b) the derivation, enforced rather than trusted.
        derived = "holder" if (readable is False and per_use is True) else "environment"
        if declared != derived:
            f.error("custody-evidences-derivation",
                    f"{label}: custody model {mid!r} declares evidences="
                    f"{declared!r} but its properties derive {derived!r} "
                    f"(readable={readable!r}, per_use_authorization={per_use!r}). "
                    f"`evidences` is derived, never asserted: a key readable by "
                    f"the holder's own execution context evidences the "
                    f"ENVIRONMENT, and only isolation WITH an authorization that "
                    f"context cannot supply evidences the HOLDER")

        # (c) the top tier must be earned.
        ceiling = member.get("authority_ceiling")
        if not isinstance(ceiling, str) or ceiling not in tiers:
            f.error("custody-ceiling-unknown",
                    f"{label}: custody model {mid!r} caps at {ceiling!r}, which "
                    f"is not a declared authority tier")
        elif (top_rank is not None and tiers.get(ceiling) == top_rank
                and declared != "holder"):
            f.error("custody-ceiling-unearned",
                    f"{label}: custody model {mid!r} caps at {ceiling!r}, the "
                    f"HIGHEST tier this ladder declares, while evidencing "
                    f"{declared!r}; unsupervised irreversible action requires "
                    f"evidence that the HOLDER acted")

    # (d) the collapse check, stated directly.
    #
    # Keyed on WHAT A MODEL EVIDENCES, not on whether its key is readable.
    # Readability is only one way to end up evidencing the environment: a key
    # isolated from the holder's context but signable by it WITHOUT LIMIT
    # evidences the environment too. An earlier form of this check tested
    # `key_readable_... is True`, so that middle case sat in neither list and
    # could outrank the holder-evidencing models untouched — the collapse this
    # rule exists to refuse, escaping through the gap between the two lists.
    holder_members = [m for m in models if isinstance(m, dict)
                      and m.get("evidences") == "holder"]
    environment_members = [m for m in models if isinstance(m, dict)
                           and m.get("evidences") == "environment"]
    for env_member in environment_members:
        e_rank = tiers.get(env_member.get("authority_ceiling")) \
            if _hashable(env_member.get("authority_ceiling")) else None
        for holder_member in holder_members:
            if env_member is holder_member:
                continue  # a self-comparison carries no information
            h_rank = tiers.get(holder_member.get("authority_ceiling")) \
                if _hashable(holder_member.get("authority_ceiling")) else None
            if e_rank is None or h_rank is None:
                continue
            if e_rank >= h_rank:
                f.error("custody-collapse",
                        f"{label}: custody model {env_member.get('id')!r} "
                        f"evidences only the ENVIRONMENT yet caps at or above "
                        f"{holder_member.get('id')!r}, which evidences the "
                        f"HOLDER; the weaker case can claim the stronger "
                        f"case's authority and the distinction the ruling drew "
                        f"is lost")

    if not holder_members:
        f.error("custody-holder-tier-absent",
                f"{label}: no custody model evidences the HOLDER; the "
                f"enumeration must be able to express the case it exists to "
                f"distinguish")
    if not environment_members:
        f.error("custody-environment-tier-absent",
                f"{label}: no custody model evidences only the ENVIRONMENT; "
                f"the enumeration must name the case it exists to refuse "
                f"authority to")


# --------------------------- the wallet record ---------------------------

def check_wallet_record(f: Findings, label: str, doc: dict, ctx: Context) -> None:
    """The custody model a wallet DECLARES is where the closed set actually
    binds. Checking it only where an exercise reports a model in force left
    the declaration itself unchecked, so a wallet could name a custody model
    that does not exist and every ceiling computed from it would resolve to
    nothing — the cap failing open at its source."""
    model = _mapping(doc.get("custody")).get("model")
    if model and (not isinstance(model, str) or model not in ctx.custody):
        f.error("custody-model-unknown",
                f"{label}: declares custody model {model!r}, which is not a "
                f"member of the closed registry "
                f"({sorted(ctx.custody)}); custody is declared FROM A CLOSED "
                f"SET, and an unrecognised model is refused rather than "
                f"treated as uncapped")


# --------------------------- rules (e)-(h): grants ---------------------------

def check_grant(f: Findings, label: str, doc: dict, ctx: Context) -> None:
    scope = _mapping(doc.get("scope"))
    tier = scope.get("authority_tier")
    tier_rank = ctx.rank(tier)
    if tier_rank is None:
        f.error("authority-tier-unknown",
                f"{label}: scope names authority tier {tier!r}, which the "
                f"custody registry does not declare")

    # (t) the issuer is recorded, and roots are anchored. Class membership is
    # a scope-content fact and nothing else: the token's PRESENCE in acts
    # makes the grant review-class by design, so an unrelated grant must not
    # borrow the token casually. Absent issuer and unanchored root are
    # sequential, not nested: an absent value cannot be compared against an
    # anchor, so it reports its own code and stops there. The exact-match
    # comparison is deliberately un-normalized — identity strings do not get
    # fuzzy, so ` brett heap` is as refused as `opensoft`.
    if REVIEW_ACT_TOKEN in _hashable_set(scope.get("acts")):
        issued_by = doc.get("issued_by")
        if not issued_by:
            f.error("issuer-unrecorded",
                    f"{label}: REVIEW-class grant (scope acts include "
                    f"{REVIEW_ACT_TOKEN!r}) records no issued_by; every "
                    f"review-authority grant names its issuer")
        elif not doc.get("parent_grant_ref"):
            if issued_by != ROOT_ISSUER_OPERATOR_TOKEN:
                # Schema-invalid values still reach the rules (findings
                # accumulate; validation never stops), so every read here
                # must tolerate a non-string issued_by: a list or mapping is
                # unhashable, and `in` against a dict keyset would crash the
                # whole run as a harness error instead of reporting the
                # refusal. Non-strings simply take the generic branch — the
                # schema finding is the precise report, this one refuses the
                # anchor either way.
                machine_named = (
                    isinstance(issued_by, str)
                    and (issued_by in ctx.wallets
                         or bool(_MACHINE_ISSUER_RE.match(issued_by))))
                if machine_named:
                    why = (f"{issued_by!r}, a MACHINE-named issuer; a root "
                           f"issuer cannot be an agent holder")
                elif issued_by == _LEGACY_ORG_ISSUER:
                    why = (f"{issued_by!r}, the LEGACY org-level string; "
                           f"pre-anchor issuance values do not grandfather "
                           f"into the operator anchor")
                else:
                    why = (f"{issued_by!r}, which is not the anchored "
                           f"responsible operator")
                f.error("root-issuer-unanchored",
                        f"{label}: root REVIEW-class grant names its issuer "
                        f"as {why}. A root issuer's authority to issue is "
                        f"not conferred by the register the grant writes "
                        f"into; it is standing under the Human Escalation "
                        f"Contract ({ISSUER_ANCHOR_AUTHORITY}), and the only "
                        f"accepted root-issuer value here is "
                        f"{ROOT_ISSUER_OPERATOR_TOKEN!r}")

    # (e) custody caps authority.
    wallet_ref = _mapping(doc.get("audience")).get("wallet_ref")
    resolved = ctx.ceiling_for_wallet(wallet_ref) if wallet_ref else None
    if wallet_ref and resolved is None:
        # Failing silently here would make the custody ceiling optional in
        # practice: name a wallet nobody can resolve and the cap never runs.
        # The attenuation rule already refuses an unresolvable parent; this is
        # the same asymmetry closed. UNCONDITIONALLY: an `and ctx.wallets`
        # guard here was dead code while every context held the packaged
        # positives, then failed open the moment repo scans got their own
        # context — a consumer repo declaring no wallets at all skipped
        # every resolution this rule exists to force.
        f.error("custody-ceiling-unresolved",
                f"{label}: audience wallet {wallet_ref!r} does not resolve to a "
                f"wallet with a known custody model, so the ceiling that bounds "
                f"this grant cannot be checked")
    if resolved and tier_rank is not None:
        model, ceiling = resolved
        ceiling_rank = ctx.rank(ceiling)
        if ceiling_rank is not None and tier_rank > ceiling_rank:
            f.error("custody-ceiling-exceeded",
                    f"{label}: grant claims authority tier {tier!r} but its "
                    f"audience wallet {wallet_ref!r} declares custody {model!r}, "
                    f"whose ceiling is {ceiling!r}. Raising authority requires "
                    f"changing custody, not asserting trust")

    # (f) attenuation is monotonic.
    parent_ref = doc.get("parent_grant_ref")
    if parent_ref:
        parent = ctx.grants.get(parent_ref) if isinstance(parent_ref, str) else None
        if parent is None:
            f.error("attenuation-parent-unresolved",
                    f"{label}: parent_grant_ref {parent_ref!r} does not resolve "
                    f"in the corpus, so attenuation cannot be checked")
        else:
            pscope = _mapping(parent.get("scope"))
            child_acts = _hashable_set(scope.get("acts"))
            parent_acts = _hashable_set(pscope.get("acts"))
            widened = sorted(child_acts - parent_acts, key=repr)
            if widened:
                f.error("attenuation-widened",
                        f"{label}: derived grant adds acts {widened} its parent "
                        f"{parent_ref!r} does not confer; derivation may narrow "
                        f"and may never widen")
            parent_objects = pscope.get("objects")
            child_objects = scope.get("objects")
            if parent_objects is not None:
                if child_objects is None:
                    f.error("attenuation-widened",
                            f"{label}: parent {parent_ref!r} narrows to objects "
                            f"{sorted(parent_objects)} and the derived grant "
                            f"drops the narrowing entirely")
                else:
                    extra = sorted(_hashable_set(child_objects)
                                   - _hashable_set(parent_objects), key=repr)
                    if extra:
                        f.error("attenuation-widened",
                                f"{label}: derived grant adds objects {extra} "
                                f"outside its parent {parent_ref!r}")
            parent_rank = ctx.rank(pscope.get("authority_tier"))
            if tier_rank is not None and parent_rank is not None and tier_rank > parent_rank:
                f.error("attenuation-widened",
                        f"{label}: derived grant raises authority tier to "
                        f"{tier!r} above its parent {parent_ref!r} at "
                        f"{pscope.get('authority_tier')!r}")
            child_exp = parse_time(doc.get("expires_at"))
            parent_exp = parse_time(parent.get("expires_at"))
            if child_exp and parent_exp and child_exp > parent_exp:
                f.error("attenuation-widened",
                        f"{label}: derived grant expires {doc.get('expires_at')} "
                        f"after its parent {parent_ref!r} at "
                        f"{parent.get('expires_at')}; lifetime may only shorten")
            # Posture is part of scope, so attenuation must cover it. Rule (h)
            # declares posture and tier ONE vocabulary; attenuating only the
            # tier would let a derivation keep its parent's tier and quietly
            # waive the approval that made that tier survivable.
            pposture = _mapping(pscope.get("approval_posture"))
            cposture = _mapping(scope.get("approval_posture"))
            if (pposture.get("hermes_approval_required_before_apply") is True
                    and cposture.get("hermes_approval_required_before_apply") is False):
                f.error("attenuation-widened",
                        f"{label}: derived grant waives approval before apply "
                        f"where its parent {parent_ref!r} requires it")
            if (pposture.get("authority_agents_may_approve") is False
                    and cposture.get("authority_agents_may_approve") is True):
                f.error("attenuation-widened",
                        f"{label}: derived grant permits agent approval where "
                        f"its parent {parent_ref!r} withholds it")
            dropped = sorted(_hashable_set(pposture.get("human_escalation_required_for"))
                             - _hashable_set(cposture.get("human_escalation_required_for")), key=repr)
            if dropped:
                f.error("attenuation-widened",
                        f"{label}: derived grant drops escalation triggers "
                        f"{dropped} its parent {parent_ref!r} requires; removing "
                        f"an escalation widens authority")
            lost = sorted(_hashable_set(parent.get("distinct_holder_constraint_refs"))
                          - _hashable_set(doc.get("distinct_holder_constraint_refs")), key=repr)
            if lost:
                f.error("attenuation-widened",
                        f"{label}: derived grant drops distinct-holder "
                        f"constraints {lost} its parent {parent_ref!r} carries")

    # (g) one authority vocabulary, read from the canonical envelope.
    posture = scope.get("approval_posture")
    if isinstance(posture, dict):
        for key in sorted(posture, key=repr):
            if key not in ctx.vocabulary:
                f.error("authority-vocabulary-parallel",
                        f"{label}: approval_posture names {key!r}, which is not "
                        f"an `approval_policy` property of the neutral job "
                        f"envelope (legal terms: {sorted(ctx.vocabulary)}). An "
                        f"agent's authority and a job's approval posture are one "
                        f"vocabulary, not two kept in agreement")

        # (h) posture and tier agree.
        if posture.get("hermes_approval_required_before_apply") is False \
                and tier != "act_unsupervised":
            f.error("posture-tier-incoherent",
                    f"{label}: posture waives approval before apply while the "
                    f"authority tier is {tier!r}; acting with no approval before "
                    f"apply is the 'act_unsupervised' tier")
        if posture.get("authority_agents_may_approve") is True:
            act_rank = ctx.rank("act")
            if tier_rank is not None and act_rank is not None and tier_rank < act_rank:
                f.error("posture-tier-incoherent",
                        f"{label}: posture permits agent approval while the "
                        f"authority tier is {tier!r}; approving is an effecting "
                        f"act and requires tier 'act' or above")

    if doc.get("state") == "revoked" and not doc.get("revocation"):
        f.error("revocation-unrecorded",
                f"{label}: state is 'revoked' with no revocation block "
                f"recording when and why")


# --------------------------- rules (i)-(m): exercise ---------------------------

def attribution_wallet_ref(doc: dict) -> str | None:
    """The wallet that actually presented this exercise, if the record names
    one. An unattributed act names none, and is not held to the audience
    binding — there is no claimed identity to contradict."""
    attribution = _mapping(doc.get("attribution"))
    if attribution.get("mode") == "unattributed":
        return None
    return attribution.get("wallet_ref")


def _revoked_ancestor(ctx: Context, grant_ref: str) -> str | None:
    seen: set[str] = set()
    ref = grant_ref
    while isinstance(ref, str) and ref and ref not in seen:
        seen.add(ref)
        grant = ctx.grants.get(ref)
        if grant is None:
            return None
        if grant.get("state") == "revoked":
            return ref
        wallet_ref = _mapping(grant.get("audience")).get("wallet_ref")
        wallet = ctx.wallets.get(wallet_ref) if isinstance(wallet_ref, str) else None
        if wallet is not None and wallet.get("state") == "revoked":
            return wallet_ref
        ref = grant.get("parent_grant_ref")
    return None


def check_exercise(f: Findings, label: str, doc: dict, ctx: Context) -> None:
    proof = _mapping(doc.get("proof_of_possession"))
    presented = proof.get("presented")
    verified = proof.get("verified")
    event_class = doc.get("event_class")
    outcome = doc.get("outcome")
    refusal = _mapping(doc.get("refusal"))

    if outcome == "refused" and not refusal:
        f.error("refusal-unrecorded",
                f"{label}: outcome is 'refused' with no refusal block naming "
                f"what was lacking")

    # The exercise must actually BIND to the grant it names. Without these an
    # exercise can cite a grant that does not exist, perform an act the grant
    # never conferred, be presented by a wallet the grant does not address, or
    # claim a custody model stronger than its own wallet declares — each of
    # which makes every downstream rule adjudicate a fiction.
    grant = (ctx.grants.get(doc.get("grant_ref"))
             if isinstance(doc.get("grant_ref"), str) else None)
    if doc.get("grant_ref") and grant is None:
        f.error("grant-unresolved",
                f"{label}: grant_ref {doc.get('grant_ref')!r} does not resolve, "
                f"so neither its scope, its custody ceiling nor its revocation "
                f"state can be checked; an exercise against an unknown grant is "
                f"refused rather than passed over")
    elif grant is not None:
        gscope = _mapping(grant.get("scope"))
        if doc.get("act") and doc["act"] not in _sequence(gscope.get("acts")):
            f.error("act-outside-grant-scope",
                    f"{label}: act {doc['act']!r} is not among the acts grant "
                    f"{doc.get('grant_ref')!r} confers "
                    f"({sorted(_sequence(gscope.get('acts')), key=repr)})")
        audience_wallet = _mapping(grant.get("audience")).get("wallet_ref")
        exercising_wallet = attribution_wallet_ref(doc)
        # The presenting wallet is DERIVED from the presenting key, and the
        # binding key is the VERIFIED proof block's key when one is recorded.
        # `attribution.presenting_key_ref` is the same self-declared data as
        # `attribution.wallet_ref` — deriving from it alone would move the
        # lie one field over, not close it. A verified proof ESTABLISHES its
        # key (this corpus's own semantics: an unverified signature
        # establishes nothing, which is why a verification failure may be
        # recorded unattributed); the attribution block may narrate the same
        # fact, and may not contradict it.
        exercise_attribution = _mapping(doc.get("attribution"))
        attributed_key = (exercise_attribution.get("presenting_key_ref")
                          if exercise_attribution.get("mode") != "unattributed"
                          else None)
        if not isinstance(attributed_key, str):
            attributed_key = None
        verified_key = (proof.get("presenting_key_ref")
                        if verified is True else None)
        if not isinstance(verified_key, str):
            verified_key = None
        if verified is True and not verified_key:
            # No fallback to the attribution key here: a record could claim
            # a verified signature, omit the proof key, and put the
            # audience's key in attribution — the original laundering route,
            # one omission deeper.
            f.error("presenting-key-unresolved",
                    f"{label}: the proof block records a verified signature "
                    f"but names no presenting key, so the exercise cannot be "
                    f"bound to any wallet; a verification that does not "
                    f"record WHICH key verified is refused rather than "
                    f"trusted from the attribution block")
        presenting_key = verified_key if verified is True else attributed_key
        key_wallet = None
        if verified_key and exercise_attribution.get("mode") == "unattributed":
            f.error("attribution-laundered",
                    f"{label}: the proof block records a VERIFIED signature "
                    f"by {verified_key!r} while the act is recorded "
                    f"'unattributed'; a verified presented key is an "
                    f"establishable identity, and recording the act as "
                    f"nobody's launders it past the audience and "
                    f"distinct-holder bindings it would otherwise face")
        elif verified_key and attributed_key and attributed_key != verified_key:
            f.error("attribution-laundered",
                    f"{label}: attribution names presenting key "
                    f"{attributed_key!r} while the verified proof was "
                    f"presented by {verified_key!r}; attribution follows the "
                    f"key that actually signed")
        if presenting_key:
            owners = ctx.wallets_by_key.get(presenting_key) or []
            if not owners:
                f.error("presenting-key-unresolved",
                        f"{label}: presenting key {presenting_key!r} is no "
                        f"known wallet's key_reference, so the audience "
                        f"binding cannot be checked; an exercise presented by "
                        f"an unknown key is refused rather than passed over")
            elif len(owners) > 1:
                f.error("presenting-key-unresolved",
                        f"{label}: presenting key {presenting_key!r} is "
                        f"declared by more than one wallet "
                        f"({sorted(owners)}); `key_id` is scoped to its DID "
                        f"anchor, so a bare key reference cannot say which "
                        f"wallet presented — an ambiguous key is refused "
                        f"rather than resolved by file order")
            else:
                key_wallet = owners[0]
                if exercising_wallet and key_wallet != exercising_wallet:
                    f.error("attribution-laundered",
                            f"{label}: attribution names wallet "
                            f"{exercising_wallet!r} while the presenting key "
                            f"{presenting_key!r} is wallet {key_wallet!r}'s; "
                            f"an act is attributed to the wallet whose key "
                            f"was presented, never to a declared stand-in")
        presented_by = key_wallet or exercising_wallet
        if audience_wallet and presented_by and presented_by != audience_wallet:
            f.error("audience-mismatch",
                    f"{label}: presented by wallet {presented_by!r} but "
                    f"grant {doc.get('grant_ref')!r} addresses "
                    f"{audience_wallet!r}; a grant is exercisable only by its "
                    f"audience, or proof of possession secures nothing")
        wallet = (ctx.wallets.get(audience_wallet)
                  if isinstance(audience_wallet, str) else None)
        if wallet is not None:
            declared_model = _mapping(wallet.get("custody")).get("model")
            in_force = doc.get("custody_model_in_force")
            if declared_model and in_force and in_force != declared_model:
                f.error("custody-model-mismatch",
                        f"{label}: records custody {in_force!r} in force while "
                        f"wallet {audience_wallet!r} declares {declared_model!r}; "
                        f"an exercise cannot claim evidence its wallet's custody "
                        f"does not supply")
            if wallet.get("state") == "suspended" and outcome == "permitted":
                f.error("revoked-chain-exercised",
                        f"{label}: exercise permitted while wallet "
                        f"{audience_wallet!r} is suspended")
        if grant.get("state") == "expired" and outcome == "permitted":
            f.error("revoked-chain-exercised",
                    f"{label}: exercise permitted against grant "
                    f"{doc.get('grant_ref')!r}, whose state is 'expired'")
        # (m, second half) Constraints are declared on the GRANT. An exercise
        # that simply omits the evaluation would otherwise escape a constraint
        # its own grant carries.
        if outcome == "permitted":
            evaluated = {e.get("constraint_ref")
                         for e in _sequence(doc.get("constraint_evaluations"))
                         if isinstance(e, dict)
                         and _hashable(e.get("constraint_ref"))}
            for ref in _sequence(grant.get("distinct_holder_constraint_refs")):
                if not _hashable(ref):
                    continue  # unhashable member; the schema finding on the
                              # grant is the report, not a membership crash
                if ref not in evaluated:
                    f.error("distinct-holder-violated",
                            f"{label}: grant {doc.get('grant_ref')!r} declares "
                            f"constraint {ref!r} and this permitted exercise "
                            f"records no evaluation of it; a declared "
                            f"constraint is not escaped by silence")

    # (i) proof of possession, and a refusal that names the right absence.
    if presented is not True:
        if outcome == "permitted":
            f.error("proof-of-possession-missing",
                    f"{label}: exercise permitted with no proof of possession "
                    f"presented; possession of a grant confers nothing, and a "
                    f"stolen grant must be inert")
        elif refusal.get("code") not in (None, "missing_proof_of_possession"):
            f.error("proof-of-possession-missing",
                    f"{label}: refusal names {refusal.get('code')!r} while what "
                    f"was missing is the PROOF; the grant was supplied and is "
                    f"not what was lacking")
    elif verified is not True and outcome == "permitted":
        # `verified is not True` covers BOTH an explicit false and an ABSENT
        # verdict. Testing only for false would let a record permit an act on
        # a signature nobody ever checked — presentation accepted as proof,
        # which is exactly what this requirement forbids.
        f.error("proof-of-possession-missing",
                f"{label}: exercise permitted although the presented signature "
                f"is recorded verified={verified!r}; presentation is not proof, "
                f"and an unchecked signature is not a verified one")

    # (j) a verification failure is not an absence.
    if presented is True and verified is False:
        expected_class = "verification_failure"
    elif presented is True and verified is True:
        expected_class = "authenticated"
    elif presented is not True:
        expected_class = "unauthenticated_request"
    else:
        # presented with no verdict recorded: the record cannot say what event
        # this was, so say so rather than skipping the check silently.
        expected_class = None
        f.error("verification-failure-miscategorised",
                f"{label}: a signature was presented and no verification "
                f"verdict is recorded, so the record cannot distinguish an "
                f"authenticated act from a verification failure")
    if expected_class and event_class != expected_class:
        f.error("verification-failure-miscategorised",
                f"{label}: event_class is {event_class!r} but the proof block "
                f"records presented={presented!r}/verified={verified!r}, which "
                f"is a {expected_class!r}. A signature that fails to verify and "
                f"a request carrying no signature are different events and stay "
                f"distinguishable in the record")

    # (k) attribution is not laundered.
    attribution = _mapping(doc.get("attribution"))
    mode = attribution.get("mode")
    transport = _mapping(attribution.get("transport"))
    if mode == "key_attributed" and not attribution.get("presenting_key_ref"):
        f.error("attribution-laundered",
                f"{label}: attribution claims 'key_attributed' but names no "
                f"presenting key; attribution is cryptographic, not inferred")
    if mode == "unattributed" and (attribution.get("holder_ref")
                                   or attribution.get("presenting_key_ref")):
        f.error("attribution-laundered",
                f"{label}: attribution is 'unattributed' yet the record assigns "
                f"a holder or a key; an act that cannot be attributed says so "
                f"rather than being assigned on the strength of the credential "
                f"used")
    if transport and not attribution.get("presenting_key_ref") and mode != "unattributed":
        f.error("attribution-laundered",
                f"{label}: the only identity on this act is the shared "
                f"credential {transport.get('shared_credential_ref')!r}; a "
                f"shared credential is transport and never the actor, so this "
                f"act is 'unattributed'")

    # (l) revocation is checked at use.
    check = _mapping(doc.get("revocation_check"))
    if check.get("performed_at_exercise") is not True:
        f.error("revoked-chain-exercised",
                f"{label}: no revocation check was performed at exercise; "
                f"issuance-time validity is not evidence of current validity")
    grant_ref = doc.get("grant_ref")
    revoked_at_ancestor = _revoked_ancestor(ctx, grant_ref) if grant_ref else None
    if revoked_at_ancestor and outcome == "permitted":
        f.error("revoked-chain-exercised",
                f"{label}: exercise permitted although {revoked_at_ancestor!r} "
                f"in its chain is revoked; revoking a grant revokes everything "
                f"derived from it at the same moment")
    if revoked_at_ancestor and check.get("result") == "active":
        f.error("revoked-chain-exercised",
                f"{label}: revocation check reports 'active' although "
                f"{revoked_at_ancestor!r} in the chain is revoked")
    if check.get("result") == "revoked" and outcome == "permitted":
        f.error("revoked-chain-exercised",
                f"{label}: revocation check reports 'revoked' and the exercise "
                f"was permitted anyway")

    # (m) distinct-holder constraints bind where declared.
    for evaluation in _sequence(doc.get("constraint_evaluations")):
        if not isinstance(evaluation, dict):
            continue
        ref = evaluation.get("constraint_ref")
        same = evaluation.get("prior_act_holder_ref") == evaluation.get("this_holder_ref")
        if same and evaluation.get("satisfied") is True:
            f.error("distinct-holder-violated",
                    f"{label}: constraint {ref!r} is recorded satisfied while "
                    f"the same holder "
                    f"{evaluation.get('this_holder_ref')!r} is named for both "
                    f"acts; the prior act's recorded holder is the comparison "
                    f"basis")
        if evaluation.get("satisfied") is False and outcome == "permitted":
            f.error("distinct-holder-violated",
                    f"{label}: constraint {ref!r} is unsatisfied and the "
                    f"exercise was permitted anyway")
        if ref and (not isinstance(ref, str) or ref not in ctx.constraints):
            f.warn("constraint-unresolved",
                   f"{label}: constraint {ref!r} does not resolve in the corpus")

    # Custody in force must be a member of the closed set.
    model = doc.get("custody_model_in_force")
    if model and (not isinstance(model, str) or model not in ctx.custody):
        f.error("custody-model-unknown",
                f"{label}: custody_model_in_force {model!r} is not a member of "
                f"the closed custody registry")


# --------------------------- rule (n): non-substrate ---------------------------

def check_subject_attestation(f: Findings, label: str, doc: dict) -> None:
    resolution = _mapping(doc.get("resolution"))
    if resolution.get("resolved_by") != "subject_ref":
        f.error("wallet-ref-as-subject-identifier",
                f"{label}: resolution keys on "
                f"{resolution.get('resolved_by')!r}; a wallet reference is "
                f"attestation, never the identifier, and resolution treating it "
                f"as one is a validation failure")
    if resolution.get("reconstructable_without_wallet") is False:
        f.error("wallet-ref-as-subject-identifier",
                f"{label}: the record declares it is not reconstructable "
                f"without a wallet; a wallet may not become a prerequisite for "
                f"reconstructing a record or resolving a subject")


# --------------------------- rules (o)-(q): the agent profile ---------------------------

def check_agent_composition(f: Findings, label: str, doc: dict,
                            ctx: Context) -> None:
    composition = _mapping(doc.get("composition"))
    component_set = composition.get("component_set")

    # (o) a hash names what it covers.
    if composition.get("declared_hash") and not component_set:
        f.error("composition-set-missing",
                f"{label}: a composition hash is declared with no component "
                f"set; the set is part of the declaration so a reader can tell "
                f"what a matching hash was actually asserting")
    for component in _sequence(component_set):
        if not isinstance(component, dict):
            continue
        name = component.get("component")
        mode = component.get("binding_mode")
        if mode == "content" and not component.get("content_digest"):
            f.error("composition-binding-incomplete",
                    f"{label}: component {name!r} is bound by content and "
                    f"carries no digest, so the hash covers nothing for it")
        if mode == "reference":
            reference = _mapping(component.get("reference"))
            if not reference.get("ref") or not reference.get(
                    "governing_configuration_digest"):
                f.error("composition-binding-incomplete",
                        f"{label}: component {name!r} is bound by reference and "
                        f"must carry both the corpus ref and the digest of the "
                        f"configuration governing how it is consulted; without "
                        f"the latter an agent could change what it may retrieve "
                        f"without changing its identity")

    # (p) a declared change revokes immediately.
    attestation = _mapping(doc.get("attestation"))
    attested = attestation.get("attested_hash")
    declared = composition.get("declared_hash")
    if attested and declared and attested != declared:
        if doc.get("grants_state") != "revoked_on_composition_change":
            f.error("declared-change-not-revoked",
                    f"{label}: the attested composition differs from the "
                    f"declared composition and grants_state is "
                    f"{doc.get('grants_state')!r}; a changed agent is a "
                    f"different agent and its outstanding grants are revoked at "
                    f"that moment, with no tolerance band and no grace period")

    # (q) composition belongs to the agent profile only. The wallet must
    # RESOLVE before its holder class can be checked — firing only on a
    # resolved non-agent wallet made resolution optional in practice: name a
    # wallet nobody can resolve and the class check never runs. Same
    # asymmetry the custody-ceiling and grant bindings already close.
    wallet_ref = doc.get("wallet_ref")
    wallet = ctx.wallets.get(wallet_ref) if isinstance(wallet_ref, str) else None
    if wallet_ref and wallet is None:
        f.error("composition-wallet-unresolved",
                f"{label}: composition declared for wallet {wallet_ref!r}, "
                f"which does not resolve, so its holder class cannot be "
                f"checked; a composition for an unknown wallet is refused "
                f"rather than passed over")
    if wallet is not None:
        holder_class = _mapping(wallet.get("holder")).get("holder_class")
        if holder_class != "agent":
            f.error("composition-on-non-agent",
                    f"{label}: composition declared for wallet {wallet_ref!r} "
                    f"whose holder class is {holder_class!r}; composition is "
                    f"meaningful for an agent and meaningless for a patient, "
                    f"and the core imposes none on any class")


# --------------------------- per-record validation ---------------------------

def validate_record(f: Findings, label: str, doc: Any, docs: dict[str, dict],
                    ctx: Context) -> None:
    if not isinstance(doc, dict):
        f.error("schema", f"{label}: document is not a mapping")
        return
    kind = doc.get("kind")
    if kind not in KIND_TO_SCHEMA:
        f.error("unknown-kind", f"{label}: kind {kind!r} is not an openxWallet kind")
        return

    for error in sorted(validator_for(kind, docs).iter_errors(doc),
                        key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "<root>"
        f.error("schema", f"{label}: {where}: {error.message}")

    id_field = _ID_FIELDS.get(kind)
    rid = doc.get(id_field) if id_field else None
    if isinstance(rid, str) and (kind, rid) in ctx.duplicate_ids:
        f.error("record-id-duplicate",
                f"{label}: {id_field} {rid!r} is declared by more than one "
                f"record in this corpus; resolution through an id is "
                f"last-write-wins, so a duplicate could swap the key, scope "
                f"or constraint a reference resolves to — refused on every "
                f"copy rather than resolved by file order")

    check_no_key_material(f, label, doc)

    if kind == "xfactory_wallet_record":
        check_wallet_record(f, label, doc, ctx)
    elif kind == "xfactory_wallet_custody_registry":
        check_custody_registry(f, label, doc)
    elif kind == "xfactory_wallet_grant":
        check_grant(f, label, doc, ctx)
    elif kind == "xfactory_wallet_grant_exercise":
        check_exercise(f, label, doc, ctx)
    elif kind == "xfactory_wallet_subject_attestation":
        check_subject_attestation(f, label, doc)
    elif kind == "xfactory_wallet_agent_composition":
        check_agent_composition(f, label, doc, ctx)


# --------------------------- negative fixture headers ---------------------------

def expected_failure(path: Path) -> tuple[str, str | None, str]:
    """A negative fixture declares the finding CODE it exists to provoke, MAY
    pin it further with a substring, and MUST attribute itself to a
    requirement. The detail matters: `schema` is satisfied by any schema error
    whatsoever, so without it a fixture can be mutated into testing nothing
    while its self-test stays green. The requirement is what makes the corpus a
    negative confirmation PER REQUIREMENT rather than a pile of negatives."""
    code = detail = requirement = None
    for line in path.read_text(encoding="utf-8").splitlines():
        # Blank lines are allowed INSIDE the header block. Stopping at the
        # first non-comment line meant a detail pin separated by a blank line
        # was silently dropped — and the detail pin fails OPEN (the fixture
        # keeps a green self-test with its invariant pin gone), which is the
        # precise drift the pin exists to prevent.
        if not line.strip():
            continue
        if not line.startswith("#"):
            break
        if (m := _EXPECTED_RE.match(line)):
            code = m.group(1)
        elif (m := _DETAIL_RE.match(line)):
            detail = m.group(1)
        elif (m := _REQUIREMENT_RE.match(line)):
            requirement = m.group(1)
    if code is None:
        raise SystemExit(
            f"negative fixture missing '# expected_failure:' header: {path}")
    if requirement is None:
        raise SystemExit(
            f"negative fixture missing '# requirement:' header: {path}")
    return code, detail, requirement


# --------------------------- layer 1: packaged corpus ---------------------------

def positive_paths() -> list[Path]:
    out: list[Path] = []
    for family in FAMILY_DIRS:
        out.extend(sorted((family / "examples").glob("*.example.yaml")))
    return out


def negative_paths() -> list[Path]:
    out: list[Path] = []
    for family in FAMILY_DIRS:
        out.extend(sorted((family / "examples" / "negative").glob("*.yaml")))
    return out


def self_test(f: Findings, docs: dict[str, dict], ctx: Context) -> None:
    positives = positive_paths()
    negatives = negative_paths()
    if not positives:
        f.error("examples-missing", "no packaged positive examples found")
    if not negatives:
        f.error("examples-missing", "no packaged negative fixtures found")

    # The canonical custody registry is validated as a positive: it is the
    # closed set every other record resolves against.
    registry_label = str(CUSTODY_REGISTRY_PATH.relative_to(ROOT))
    validate_record(f, registry_label, ctx.registry, docs, ctx)
    if f.errors:
        f.note("the canonical custody registry is validated first; downstream "
               "ceiling checks resolve against it")

    for path in positives:
        label = str(path.relative_to(ROOT))
        before = len(f.errors)
        validate_record(f, label, load_yaml(path), docs, ctx)
        for i in range(before, len(f.errors)):
            f.errors[i] = f"{f.errors[i]} [expected a valid example]"

    covered: dict[str, list[str]] = {}
    for path in negatives:
        code, detail, requirement = expected_failure(path)
        label = f"negative/{path.name}"
        if requirement not in REQUIREMENTS:
            f.error("negative-requirement-unknown",
                    f"{label}: declares requirement {requirement!r}, which is "
                    f"not one of the capability's requirements")
        else:
            covered.setdefault(requirement, []).append(path.name)

        local = Findings()
        local_ctx = Context(ctx.registry, ctx.vocabulary)
        local_ctx.wallets = dict(ctx.wallets)
        local_ctx.grants = dict(ctx.grants)
        local_ctx.constraints = dict(ctx.constraints)
        local_ctx.wallets_by_key = {k: list(v)
                                    for k, v in ctx.wallets_by_key.items()}
        local_ctx.duplicate_ids = set(ctx.duplicate_ids)
        doc = load_yaml(path)
        if isinstance(doc, dict):
            local_ctx.index(doc)
        validate_record(local, label, doc, docs, local_ctx)

        if not local.errors:
            f.error("negative-should-fail",
                    f"{label}: expected invalid, validated cleanly — the probe "
                    f"proves nothing")
        elif code not in codes_of(local.errors):
            f.error("negative-wrong-reason",
                    f"{label}: expected finding {code!r}, got "
                    f"{sorted(codes_of(local.errors))}")
        elif detail and not any(detail in line for line in lines_for(local.errors, code)):
            f.error("negative-wrong-reason",
                    f"{label}: finding {code!r} fired but not for {detail!r} — "
                    f"the fixture no longer tests the invariant it is named "
                    f"for: {lines_for(local.errors, code)}")

    # Boundary guard (US3): the widening must cost non-review grants nothing.
    # A schema-valid post_transaction-class ROOT grant with NO issued_by is
    # exactly what every packaged positive looked like before S2; validated
    # against the packaged context (audience resolves, ceiling admits its
    # tier), it must come back with ZERO findings. Any finding here means
    # class membership leaked past the scope-content test.
    boundary = {
        "schema_version": 1,
        "kind": "xfactory_wallet_grant",
        "grant_id": "grant-boundary-guard-non-review-0001",
        "audience": {"wallet_ref": "wal-agent-poster-0001",
                     "holder_ref": "agent:ledger-poster"},
        "scope": {
            "acts": ["create_transaction", "post_transaction"],
            "authority_tier": "act",
            "approval_posture": {
                "hermes_approval_required_before_apply": True,
                "authority_agents_may_approve": False,
                "human_escalation_required_for": [
                    "irreversible_external_effect"],
            },
        },
        "expires_at": "2027-12-31T23:59:59Z",
        "issued_at": "2026-08-24T00:00:00Z",
        "state": "active",
    }
    local = Findings()
    validate_record(local, "self-test/boundary-guard", boundary, docs, ctx)
    if local.errors:
        f.error("boundary-guard-failed",
                f"a non-review root grant without issued_by must validate "
                f"cleanly (US3); got {local.errors}")

    # S2 anchor assertions. The packaged specimens prove the corpus fails on
    # the violations; these synthetic probes pin the RULE's own edges so no
    # single edit or deleted fixture can silence an invariant while the
    # self-test stays green: the anchored-root positive, whitespace/case
    # drift refused without normalization, child grants exempt from the root
    # check, and both refusal wordings the detail pins name.
    def _anchor_probe(label, doc, expect_code=None, expect_sub=None):
        probe = Findings()
        validate_record(probe, label, doc, docs, ctx)
        errs = probe.errors
        if expect_code is None:
            if errs:
                f.error("anchor-assertion-failed",
                        f"{label}: expected clean, got {errs}")
            return
        if not any(expect_code in e for e in errs):
            f.error("anchor-assertion-failed",
                    f"{label}: expected {expect_code!r}, got "
                    f"{sorted(codes_of(errs))} {errs}")
        elif expect_sub and not any(
                expect_sub in e for e in errs if expect_code in e):
            f.error("anchor-assertion-failed",
                    f"{label}: {expect_code!r} fired but without the "
                    f"{expect_sub!r} wording")

    review_scope = {
        "acts": [REVIEW_ACT_TOKEN],
        "authority_tier": "act",
        "approval_posture": {
            "hermes_approval_required_before_apply": True,
            "authority_agents_may_approve": False,
            "human_escalation_required_for": ["irreversible_external_effect"],
        },
    }
    _anchor_probe("self-test/anchor-anchored-root", {
        "schema_version": 1, "kind": "xfactory_wallet_grant",
        "grant_id": "grant-anchor-assert-anchored-0001",
        "audience": {"wallet_ref": "wal-agent-poster-0001",
                     "holder_ref": "agent:ledger-poster"},
        "scope": dict(review_scope),
        "expires_at": "2027-12-31T23:59:59Z",
        "issued_at": "2026-08-24T00:00:00Z",
        "issued_by": ROOT_ISSUER_OPERATOR_TOKEN, "state": "active",
    })
    _anchor_probe("self-test/anchor-drift-not-normalized", {
        "schema_version": 1, "kind": "xfactory_wallet_grant",
        "grant_id": "grant-anchor-assert-drift-0001",
        "audience": {"wallet_ref": "wal-agent-poster-0001",
                     "holder_ref": "agent:ledger-poster"},
        "scope": dict(review_scope),
        "expires_at": "2027-12-31T23:59:59Z",
        "issued_at": "2026-08-24T00:00:00Z",
        "issued_by": " brett heap", "state": "active",
    }, expect_code="root-issuer-unanchored")
    _anchor_probe("self-test/anchor-machine-wording", {
        "schema_version": 1, "kind": "xfactory_wallet_grant",
        "grant_id": "grant-anchor-assert-machine-0001",
        "audience": {"wallet_ref": "wal-agent-poster-0001",
                     "holder_ref": "agent:ledger-poster"},
        "scope": dict(review_scope),
        "expires_at": "2027-12-31T23:59:59Z",
        "issued_at": "2026-08-24T00:00:00Z",
        "issued_by": "sub-deadbeefdeadbeef", "state": "active",
    }, expect_code="root-issuer-unanchored", expect_sub="MACHINE")
    _anchor_probe("self-test/anchor-legacy-wording", {
        "schema_version": 1, "kind": "xfactory_wallet_grant",
        "grant_id": "grant-anchor-assert-legacy-0001",
        "audience": {"wallet_ref": "wal-agent-poster-0001",
                     "holder_ref": "agent:ledger-poster"},
        "scope": dict(review_scope),
        "expires_at": "2027-12-31T23:59:59Z",
        "issued_at": "2026-08-24T00:00:00Z",
        "issued_by": _LEGACY_ORG_ISSUER, "state": "active",
    }, expect_code="root-issuer-unanchored", expect_sub="LEGACY")

    # Child exemption needs a RESOLVING parent, which the packaged corpus
    # cannot supply without tripping attenuation (no packaged parent confers
    # the review act), so the parent is synthesized into a copied context.
    family_ctx = Context(ctx.registry, ctx.vocabulary)
    family_ctx.wallets = dict(ctx.wallets)
    family_ctx.grants = dict(ctx.grants)
    family_ctx.constraints = dict(ctx.constraints)
    family_ctx.wallets_by_key = {k: list(v)
                                 for k, v in ctx.wallets_by_key.items()}
    family_ctx.duplicate_ids = set(ctx.duplicate_ids)
    family_ctx.index({
        "schema_version": 1, "kind": "xfactory_wallet_grant",
        "grant_id": "grant-anchor-assert-parent-0001",
        "audience": {"wallet_ref": "wal-agent-poster-0001",
                     "holder_ref": "agent:ledger-poster"},
        "scope": {
            "acts": ["create_transaction", "post_transaction"],
            "authority_tier": "act",
            "approval_posture": {
                "hermes_approval_required_before_apply": True,
                "authority_agents_may_approve": False,
                "human_escalation_required_for": [
                    "irreversible_external_effect"],
            },
        },
        "expires_at": "2027-12-31T23:59:59Z",
        "issued_at": "2026-08-24T00:00:00Z",
        "state": "active",
    })
    child_doc = {
        "schema_version": 1, "kind": "xfactory_wallet_grant",
        "grant_id": "grant-anchor-assert-child-0001",
        "parent_grant_ref": "grant-anchor-assert-parent-0001",
        "audience": {"wallet_ref": "wal-agent-poster-0001",
                     "holder_ref": "agent:ledger-poster"},
        "scope": {
            "acts": ["post_transaction"], "authority_tier": "act",
            "approval_posture": {
                "hermes_approval_required_before_apply": True,
                "authority_agents_may_approve": False,
                "human_escalation_required_for": [
                    "irreversible_external_effect"],
            },
        },
        "expires_at": "2027-06-30T23:59:59Z",
        "issued_at": "2026-08-24T00:00:00Z",
        "issued_by": "sub-0123456789abcdef", "state": "active",
    }
    child_probe = Findings()
    validate_record(child_probe, "self-test/anchor-child-exempt",
                    child_doc, docs, family_ctx)
    if child_probe.errors:
        f.error("anchor-assertion-failed",
                f"self-test/anchor-child-exempt: a review-class CHILD with "
                f"a machine-shaped issuer inherits attenuation semantics, "
                f"not the root check; expected clean, got "
                f"{child_probe.errors}")

    # The three S2 fixtures are named probes, not interchangeable coverage:
    # their absence or a stripped detail pin must be loud even though the
    # requirement rows would still look covered.
    by_name = {p.name: p for p in negatives}
    for name in ("grant-review-authority-omits-issued-by.yaml",
                 "grant-review-root-issuer-is-a-machine.yaml",
                 "grant-review-root-issuer-says-opensoft.yaml"):
        path = by_name.get(name)
        if path is None:
            f.error("examples-missing",
                    f"S2 named probe negative/{name} is absent from the "
                    f"packaged corpus; each branch of rule (t) keeps its own "
                    f"standing fixture")
            continue
        _, detail, _ = expected_failure(path)
        if name != "grant-review-authority-omits-issued-by.yaml" and not detail:
            f.error("negative-wrong-reason",
                    f"negative/{name}: S2 branch probes MUST carry an "
                    f"expected_failure_detail pin naming their branch; an "
                    f"unpinned probe can be mutated into testing nothing")

    # Coverage closure: a negative confirmation PER REQUIREMENT.
    for requirement, statement in REQUIREMENTS.items():
        if requirement not in covered:
            f.error("negative-requirement-uncovered",
                    f"requirement {requirement} ({statement}) carries no "
                    f"negative confirmation; every requirement must have a "
                    f"recorded probe proving its check fails on the violation "
                    f"it exists to catch")
    f.note(f"corpus: {len(positives)} positive example(s), "
           f"{len(negatives)} negative confirmation(s) across "
           f"{len(covered)}/{len(REQUIREMENTS)} requirements")


# --------------------------- layer 2: real artifacts ---------------------------

def repo_scan(f: Findings, target: Path, docs: dict[str, dict],
              ctx: Context) -> None:
    sweep = target.is_dir()
    files = sorted(target.rglob("*.y*ml")) if sweep else [target]
    scanned = skipped = 0
    found: list[tuple[Path, dict]] = []
    for path in files:
        if set(path.parts) & SKIP_DIR_NAMES:
            continue
        # Exclude ANY packaged corpus, not only this checkout's. Domain repos
        # pin and vendor openxFactory, so the normal consumption path scans a
        # COPY — and matching on this checkout's absolute paths meant every
        # vendored negative fixture was re-adjudicated as a live record.
        if "examples" in path.parts and any(
                part in ("openxwallet", "openxwallet-agent-profile")
                for part in path.parts):
            continue
        try:
            doc = load_yaml(path)
        except yaml.YAMLError as exc:
            # A whole-checkout sweep is not the place to adjudicate unrelated
            # YAML: a file that does not parse cannot carry a family kind. An
            # explicitly named file is a different matter.
            if sweep:
                skipped += 1
                continue
            f.error("yaml", f"{path}: parse failure: {exc}")
            continue
        if not isinstance(doc, dict) or doc.get("kind") not in KIND_TO_SCHEMA:
            skipped += 1
            continue
        if path.resolve() == CUSTODY_REGISTRY_PATH.resolve():
            continue
        found.append((path, doc))

    # INDEX FIRST, then validate. Without this the cross-record rules — the
    # custody ceiling, attenuation, revocation through the chain, the audience
    # binding — resolved only against the packaged corpus and were therefore
    # inert on every real artifact, while legitimate parent/child pairs inside
    # the scanned repo reported spurious unresolved-reference findings.
    #
    # Into a context of the SCANNED REPO'S OWN records (plus the canonical
    # registry and vocabulary), never the packaged positives: a teaching
    # fixture must not resolve a live record's reference, and a consumer
    # wallet legitimately reusing a DID-scoped key_id that an example also
    # uses must not be refused as ambiguous against it. A consumer corpus is
    # closed over itself.
    repo_ctx = Context(ctx.registry, ctx.vocabulary)
    for _, doc in found:
        repo_ctx.index(doc)
    for path, doc in found:
        scanned += 1
        validate_record(f, str(path), doc, docs, repo_ctx)
    f.note(f"repo scan: {scanned} openxWallet artifact(s) validated, "
           f"{skipped} document(s) skipped as another kind")


# --------------------------- orchestration ---------------------------

def report(f: Findings, strict: bool) -> int:
    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)
    print(f"\nvalidate-openxwallet: {len(f.errors)} error(s), "
          f"{len(f.warnings)} warning(s)")
    return 1 if f.errors or (strict and f.warnings) else 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=None,
                    help="repo checkout (or single file) to scan for real "
                         "openxWallet artifacts; omit to self-test only")
    ap.add_argument("--strict", action="store_true",
                    help="treat warnings as errors")
    args = ap.parse_args()

    for family in FAMILY_DIRS:
        if not family.is_dir():
            print(f"ERROR {family} not found", file=sys.stderr)
            return 2
    if not ENVELOPE_SCHEMA_PATH.is_file():
        print(f"ERROR {ENVELOPE_SCHEMA_PATH} not found; the approval-scope "
              f"vocabulary is read from the canonical job envelope",
              file=sys.stderr)
        return 2

    try:
        docs = load_schemas()
        registry = load_yaml(CUSTODY_REGISTRY_PATH)
        vocabulary = approval_policy_vocabulary()
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR schema load failure: {exc}", file=sys.stderr)
        return 2

    f = Findings()
    for name, doc in sorted(docs.items()):
        try:
            Draft202012Validator.check_schema(doc)
        except Exception as exc:  # noqa: BLE001
            f.error("schema-meta-invalid", f"{name}: {exc}")
        if not doc.get("$schema") or not doc.get("$id"):
            f.error("schema-identity-missing",
                    f"{name}: every schema in this family declares its dialect "
                    f"($schema) and an absolute $id, so a consumer's stock "
                    f"validator resolves the bundle the same way this one does")

    ctx = Context(registry, vocabulary)
    for path in positive_paths():
        doc = load_yaml(path)
        if isinstance(doc, dict):
            ctx.index(doc)
    f.note(f"approval-scope vocabulary read from "
           f"{ENVELOPE_SCHEMA_PATH.relative_to(ROOT)}: {sorted(vocabulary)}")

    try:
        self_test(f, docs, ctx)
        if args.path is not None:
            target = Path(args.path).resolve()
            if not target.exists():
                print(f"ERROR path {target} not found", file=sys.stderr)
                return 2
            repo_scan(f, target, docs, ctx)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2
    return report(f, args.strict)


if __name__ == "__main__":
    sys.exit(main())
