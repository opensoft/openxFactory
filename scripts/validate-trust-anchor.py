#!/usr/bin/env python3
"""Validate the neutral trust-anchor contract family (add-trust-anchor).

The openxFactory-owned canonical validator for the eight kinds under
`contracts/trust-anchor/`. Run from the pinned openxFactory checkout, never
copied into a domain repo:

    python3 scripts/validate-trust-anchor.py [REPO_PATH] [--strict]

Two layers run:

1. Packaged reference corpus (`contracts/trust-anchor/examples/`): the canonical
   chain-custody registry and every `*.example.yaml` must pass schema
   conformance AND every cross-record rule; every file under `negative/` must
   FAIL for its INTENDED reason, declared in its own first lines as
   `# expected_failure: <code>` with an optional
   `# expected_failure_detail: <substring>` pin and a required
   `# requirement: <REQ-ID>` attribution. The detail pin matters because
   several cases would otherwise collapse into a generic `schema` finding and
   stop testing the invariant they are named for — this family expresses many
   of its guarantees IN THE SHAPE, so `schema` is a common outcome and a
   fixture pinned only to it proves very little.

   Coverage is closed in both directions: every requirement in REQUIREMENTS must
   carry at least one negative confirmation, and every requirement id a fixture
   claims must exist. A requirement cannot quietly lose its probe.

2. Optional real artifacts under REPO_PATH: every `*.y*ml` whose `kind` is one
   of the family kinds is validated. Other kinds are skipped and counted; the
   packaged corpus is excluded so a whole-repo sweep does not re-adjudicate the
   negatives as though they were live records, and cross-record references
   resolve against the scanned repo's OWN records plus the canonical registries,
   never against the packaged examples — a teaching fixture must not resolve a
   live reference.

The rules the shapes cannot express:

  (a) NO KEY MATERIAL, AT ANY DEPTH, INCLUDING REVERSIBLY ENCODED. An anchor is
      a key REFERENCE. The schemas close every object so no key-shaped PROPERTY
      can be added, and the only key-adjacent value the shapes admit is a
      pattern-restricted DIGEST — but a conformant shape can still carry a PEM
      block inside a string field that legitimately exists, so this walks names
      AND values, and then decodes base64 and hex runs and walks those too. A
      committed authority key is a compromised authority key, and the ratified
      text admits no exception for test, demonstration or QA material — which
      is exactly the context in which "it's only QA" gets said (R1, R7).

      THE SCAN IS ARMOR-INDEPENDENT. An earlier form of this rule matched only
      the PEM ARMOR — `-----BEGIN … PRIVATE KEY-----` — after decoding, so an
      adversarial review walked five keys past it: unarmored PKCS#8 DER as
      base64, the same DER as hex, a double-base64 wrapper, an armor label split
      across two fields, and a DER blob labelled "QA only". The armor is a
      LABEL, and a label is exactly what an evader drops. So the decoded BYTES
      are tested for DER private-key STRUCTURE (a SEQUENCE, a version INTEGER,
      the PKCS#8 prologue, the rsaEncryption / id-ecPublicKey / Ed25519
      algorithm OIDs), one further decode layer is reversed, the base64 run
      class includes the URL-safe alphabet, and the document's strings are
      joined before armor matching so a label torn across two fields still
      matches. The recovery recipe a reviewer can write down must have no green
      document to run against.

  (b) CUSTODY `evidences` IS DERIVED, NEVER ASSERTED. evidences = named_holder
      iff the key is NOT readable by the using host AND each use requires an
      authorization that host cannot supply; using_host otherwise. A member
      readable by the host that uses it and claiming to evidence the NAMED
      HOLDER is refused. This is the enumeration failure openxWallet's ruling of
      2026-08-07 exists to prevent, carried into chain custody (R3).

  (c) THE TOP ASSURANCE LEVEL MUST BE EARNED. Only custody evidencing the named
      holder may reach the top of the declared ladder — the level where nothing
      stands between the certificate and the effect. Keyed on RANK, not on the
      level's name: a registry that renamed its top level would otherwise slip
      a host-evidencing model into it and validate cleanly, which is this
      rule's own failure mode (R3).

  (d) NO CUSTODY COLLAPSE. Every member evidencing only the using host must rank
      STRICTLY BELOW every member evidencing the named holder. Without it the
      host-readable case could claim the isolated case's authority while the two
      stayed distinct in NAME (R3).

  (e) ONE CUSTODY AXIS. `evidences` derives from exactly two booleans, so two
      members declaring the SAME pair differ only in something this axis cannot
      express — a second axis smuggled in (operator escrow is the live example,
      ruled a relationship on the credential record and NOT a tier) or a rename.
      Refused, so the second axis cannot ride along invisibly (R3, OQ2).

  (f) THE openxWALLET MAPPING RESOLVES AND AGREES, READ AT RUN TIME from
      `openXwallet/contracts/openxwallet/openxwallet-custody.registry.yaml`
      rather than restated here. Each chain-custody member names its openxWallet
      counterpart; a member whose declared booleans or derived evidences
      disagree with the member it claims to be is refused. Restating the parent
      set here would recreate the second custody model the ratified text
      forbids (R3).

      THE PARENT SET IS CONSUMED AT A PIN, NOT OWNED HERE. openxFactory pins
      `opensoft/openXwallet` as a nested submodule declared by
      `contracts/openxwallet-pin.yaml`, so this rule now reads ACROSS A GITLINK,
      and `main()` refuses before any of it is trusted unless
      `scripts/verify-openxwallet-pin.py` agrees that the recorded gitlink, the
      checked-out revision and the eight digests are the pinned ones. Composing
      against whatever bytes happen to sit at that path was sufficient while the
      family was owned here; across a gitlink it is not, because a submodule
      moved off the pinned commit would move this set's answers without moving
      the pin — the mapping would still RESOLVE, and resolve against a parent set
      nobody ratified.

  (g) THE FLOOR IS A WEAKEST MEMBER. `undeclared_custody_resolves_to` must name
      a member that evidences the using host, sits at the ladder's minimum
      ceiling rank, and whose key is readable by the using host. Otherwise
      absence of a declaration would buy authority (R3). Resolved in the
      DOCUMENT'S OWN members: resolving it in the canonical registry made this
      rule report `custody-floor-unknown` for a registry that renamed its
      members and never reach the weakest-member comparison at all — a check
      failing OPEN on exactly the registry it was written to adjudicate.

  (h) A DECLARED CUSTODY MODEL IS IN THE CLOSED SET, on anchors and on
      certificates. Checking custody only where a binding compares a ceiling
      would leave the DECLARATION unchecked, so a record could name a model no
      registry contains and every ceiling derived from it resolve to nothing —
      the cap failing open at the one point it is supposed to bind (R3).

  (i) A CERTIFICATE'S `evidences` AND CEILING ARE DERIVED. Recomputed from the
      declared member, or from the registry's floor where none is declared. A
      record asserting a stronger `evidences` than its custody supplies is
      refused, and an undeclared record may not carry a ceiling above the
      floor's (R3).

  (j) A READABLE KEY LIVES IN A CREDENTIAL RECORD. Where the declared member's
      key is readable by the using host, the record must name the
      `credential-contracts` record and the vault binding that hold it — keyed
      on the registry's own boolean, never on a member's name (R7).

  (k) ANCHOR CUSTODY IS THE STRICTEST TIER, OR THE SHORTFALL IS DECLARED.
      Authority key material sits at the strictest custody tier the family
      operates; an anchor below it is conformant only where the realization
      declares that shortfall, which is the honest case for an authority the
      family does not operate and the dishonest one for an authority it does
      (R7, R8). The second half of that sentence is now MECHANISM rather than
      commentary — see rule (ff).

  (l) THE CHAIN IS COHERENT AND BOUNDS ITS SUBORDINATES. Anchors resolve, a
      subordinate sits exactly one below its parent, a certificate may not
      outlive its anchor, and an evaluation may not be `trusted` where the chain
      terminates in no held anchor or where the anchor is withdrawn, revoked or
      past its window. A refusal for a chain terminating nowhere NAMES the
      missing anchor (R1).

  (m) ISSUANCE HAPPENS UNDER AN ADMITTED AUTHORITY, AND VALIDITY DOES NOT
      RATIFY IT. `authorization_state` is derived from the anchor's admitted
      set, never asserted; an issuance citing an unadmitted authority is
      `unauthorized`, and a certificate whose evidence is unauthorized may not
      be recorded as trusted (R2).

  (n) A SHORTFALL IS DECLARED, BY THE SAME REALIZATION, AND IN TIME. A record
      that does not establish provenance must name an obligation entry that
      actually declares the shortfall — one recorded `satisfied` does not cover
      it, one belonging to another realization does not either, and one declared
      AFTER the record's own moment does not validate the claim made while the
      realization was silent (R2, R8).

  (o) AN UNEXPLAINED CERTIFICATE IS A CANDIDATE, NOT AN APPROVAL. A certificate
      with no issuance evidence answers "should this exist?" as UNANSWERED and
      may not be recorded as trusted (R2).

  (p) THE REBIND SET IS THE CERTIFICATE'S SET. A renewal's enumerated
      dependents must be exactly the set the certificate record enumerates: a
      renewal cannot reach `complete` by enumerating fewer dependents than
      exist (R4, R5).

  (q) A RENEWAL IS NOT COMPLETE WITH AN UNEVIDENCED DEPENDENT. The schema
      already forbids the recorded form; this closes the case the schema cannot
      see — an enumerated dependent with no entry in the rebind list at all
      (R4).

  (r) A RENEWAL PLANNED AGAINST AN INCOMPLETE RECORD IS REFUSED, and the
      declared enumeration state must match the certificate's, so a renewal
      cannot proceed by misdeclaring it (R5).

  (s) KEY GENERATIONS AGREE ACROSS RECORDS. A renewal's new generation is the
      certificate's current one and its superseded generation is what that
      supersedes; a binding recorded `current` or `rebound` points at the
      current generation and one recorded `rebind_required` does not. A binding
      claiming it was re-bound while still naming the superseded generation is
      the silent failure this family exists to make loud (R4, R5).

  (t) A FAILED RENEWAL NAMES THE UNBOUND DEPENDENTS, exactly those without
      succeeded evidence. Attribution is a constant in the shape; naming the
      wrong set would be the same evasion with the field filled in (R4).

  (u) EVERY BINDING IS ENUMERATED, AND AN OUTAGE-DISCOVERED ONE IS A RECORD
      DEFECT. A binding the certificate's enumeration does not name is refused;
      one discovered by an authentication failure obliges a defect entry on the
      certificate record; and a defect is closed only by naming the binding
      ADDED to the enumeration — never by the re-bind alone (R5).

  (v) THE DERIVED CEILING CAPS A BINDING. A binding requiring more assurance
      than the certificate's custody supplies must be refused WITH THE CEILING
      NAMED — the refusal names custody, not the certificate's contents (R3).

  (w) A DECLARED GAP IS NOT PERMISSION TO ASSERT THE EVIDENCE. A binding
      requiring an obligation the realization declares it CANNOT satisfy may not
      be recorded as admitted (R8). Scope, because the ratified wording draws
      the line at what the declaration CANNOT support: `cannot` is an ERROR, and
      a binding requiring an obligation declared `partial` is a WARNING — R8
      permits the admission (a partial obligation is partly met) and the warning
      is the point-of-use cost being made visible rather than assumed.

  (x) STANDING IS CHECKED AT USE. A certificate whose own state is revoked, or
      whose standing check returned revoked or was not performed at use, may not
      be recorded as trusted. Issuance-time validity is not evidence of current
      standing (R6).

  (y) THE WINDOW IS ARITHMETIC, AND A CLOSED UNEVIDENCED WINDOW IS AN OPEN
      EXPOSURE. `closes_at` is recomputed from `opens_at` + `bounded_seconds`
      rather than trusted, and where the record's own `assessed_at` is past the
      close with any authority unevidenced, the record must be
      `incomplete_open_exposure` with the escalation recorded (R6).

  (z) REVOCATION IS TRANSITIVE FOR BOTH TARGET KINDS. For an ANCHOR the closure
      is computed over the anchor chain from the corpus: a certificate chaining
      to the revoked anchor, or to any anchor beneath it, that the record does
      not name is a propagation gap. For a CERTIFICATE the closure is its own
      enumerated dependent bindings: every authority an ADMITTED binding
      supported must be named among the downstream authorities. The ratified
      requirement names certificates AND anchors — "revoking a certificate or an
      anchor revoke[s] the authority that certificate or anchor supported" — and
      an anchor-only closure left the certificate half, which is the ordinary
      case, checked by nothing (R6).

  (aa) THE DECLARATION IS CLOSED OVER THE EIGHT OBLIGATIONS, each exactly once,
      with a reason. An obligation with no entry is an UNDECLARED shortfall,
      which the ratified text treats as non-conformance even where the identical
      shortfall, declared, would be conformant (R8).

  (bb) CHAIN CUSTODY CAPS WHAT IS BENEATH A READABLE ANCHOR KEY. A certificate
      may not carry an assurance ceiling above the ceiling of any anchor in its
      chain whose private key is READABLE BY THE USING HOST, and neither may a
      subordinate anchor. Where a CA key sits in a readable file, anyone who ever
      had read access can mint a certificate for any subject, anywhere, forever
      — so nothing beneath that anchor can attribute an act to a NAMED HOLDER,
      whatever the leaf's own custody is. Keyed on READABILITY rather than on
      rank alone: an isolated anchor key confines minting to a compromised host
      while it is compromised, which is the bound a realization accepts when it
      declares the R7 shortfall for an authority the family does not operate,
      and capping that case as well would make a DECLARED shortfall a bar to
      conformance — the failure mode D6 exists to prevent (R3, R7).

  (cc) THE REGISTRY POINTER A RECORD CARRIES IS THE REGISTRY IT IS ADJUDICATED
      AGAINST. `registry_id` (and `registry_version` where present) must be the
      canonical registry's, and a SECOND registry document claiming the
      canonical `registry_id` with different content is refused. A pointer
      nobody reads is an invitation to ship a diverging closed set beside the
      records that cite it and have both validate (R3).

  (dd) VALIDITY IS CHECKED AT USE, LIKE STANDING. A certificate whose own state
      is `expired`, or whose evaluation moment lies past its own `not_after`,
      may not be recorded as trusted — the refusal vocabulary already reserves
      `certificate_outside_validity` for exactly this. Timed against the
      record's own fields, never the wall clock, so the record stays a stable
      statement about a moment (R6).

  (ee) A BINDING'S GENERATION AGREES WITH THE CERTIFICATE, WITHOUT A RENEWAL
      RECORD. Rule (s) compared generations only through a renewal, so a
      dependent left behind by a renewal that was never recorded — or recorded
      as key-preserving — was compared against nothing. A binding recorded
      `current` or `rebound` must name the certificate's CURRENT generation and
      one recorded `rebind_required` must not; and a renewal recording
      `changed: false` over a certificate that declares a superseded generation
      the renewal does not account for is refused (R4, R5).

  (ff) THE DECLARATION PERIMETER IS ENFORCED, NOT MERELY REQUIRED. Three fields
      the schemas require were read by nothing, so the rulings they carry were
      unrealized: `authority_operated_by_family` (a realization that OPERATES
      the authority cannot excuse its own authority key material by declaring an
      R7 shortfall — nothing prevents a credential record), `operated_by_family`
      on an issuance record (OQ1's refused middle option: the declared floor
      exists for an authority the family does not operate, so a family-operated
      one may not stop there), and `achieved_establishment_level` (a record may
      not assert a stronger establishment level than the realization declares it
      achieves). A required-but-unread field is a ruling that exists only in
      prose (R2, R7, R8; OQ1).

  (gg) A SHORTFALL CITATION HAS A MOMENT, AND EVIDENCE HAS ONE TOO. The lateness
      guard compared the entry's `declared_at` against the citing record's own
      moment and SKIPPED when either was absent, so omitting two optional
      timestamps disabled it; a citation with no resolvable moment is now
      refused. On the same principle, propagation evidence performed AFTER the
      declared window closed does not evidence propagation within it (R6, R8).

  (hh) A DECLARED `cannot` COSTS SOMETHING AT POINT OF USE. `required_obligations`
      is required and non-empty on every dependent binding, so a realization
      cannot declare every obligation `cannot` and meet no refusal anywhere; and
      a declaration recording more than one obligation `cannot` is reported, so
      breadth is visible rather than discovered (R8).

WHAT THIS VALIDATOR DELIBERATELY DOES NOT DO

It does not contact a certificate authority, parse a certificate, verify a
signature, check a revocation list, or confirm that a DECLARED custody model or
a DECLARED conformance state is the REAL one. Declaration is what keeps this
contract honest, and it works only if realizations declare truthfully; a
validator can check that a declaration exists, that nothing claims more than it
supports, and that the records agree with each other. It creates no authority,
anchor, certificate, key, credential or runtime.

Exit codes: 0 ok, 1 findings, 2 harness error.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import importlib.util
import re
import sys
from datetime import datetime, timedelta, timezone
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
FAMILY_DIR = ROOT / "contracts" / "trust-anchor"
CUSTODY_REGISTRY_PATH = FAMILY_DIR / "trust-anchor-chain-custody.registry.yaml"
# Rebased onto the pin's `submodule_path` (`contracts/openxwallet-pin.yaml`) as a
# PURE STRING JOIN, with no I/O and no read of the pin. The directory name is a
# literal here ON PURPOSE, and the duplication is the cheaper of two costs:
# `tests/trust-anchor/test_negative_corpus.py` and `test_declaration_perimeter.py`
# resolve this constant while standing their contexts up, so any resolution that
# CAN FAIL — an absent pin, a malformed one, an uninitialized submodule — stops
# being one gate's refusal and becomes a collection error that takes every
# trust-anchor test with it, and a suite that cannot collect proves nothing about
# the family. Reading `submodule_path` here would be exactly that: I/O at import.
# A string join cannot fail. The pin is read, and its identity checked, inside
# `main()` — see `refuse_unless_openxwallet_pinned` — and the literal's agreement
# with `submodule_path` is held by
# `tests/trust-anchor/test_openxwallet_pin_refusal.py`.
OPENXWALLET_REGISTRY_PATH = (
    ROOT / "openXwallet" / "contracts" / "openxwallet"
    / "openxwallet-custody.registry.yaml")

# Path only, for the same reason: constructing it is free, loading it is not.
OPENXWALLET_PIN_PATH = ROOT / "contracts" / "openxwallet-pin.yaml"
OPENXWALLET_VERIFIER_PATH = ROOT / "scripts" / "verify-openxwallet-pin.py"

KIND_TO_SCHEMA = {
    "xfactory_trust_anchor_chain_custody_registry":
        "chain-custody-registry.schema.yaml",
    "xfactory_trust_anchor": "trust-anchor.schema.yaml",
    "xfactory_certificate_record": "certificate-record.schema.yaml",
    "xfactory_certificate_issuance_evidence": "issuance-evidence.schema.yaml",
    "xfactory_certificate_dependent_binding": "dependent-binding.schema.yaml",
    "xfactory_certificate_renewal_record": "renewal-record.schema.yaml",
    "xfactory_certificate_revocation_propagation":
        "revocation-propagation.schema.yaml",
    "xfactory_trust_anchor_conformance_declaration":
        "conformance-declaration.schema.yaml",
}

# The identity field per indexed kind. A duplicated id is refused on every copy:
# index tables are last-write-wins, so a duplicate could swap the anchor a
# certificate resolves to, the custody a ceiling derives from, or the obligation
# entry a shortfall claims to be covered by.
_ID_FIELDS = {
    "xfactory_trust_anchor": "anchor_id",
    "xfactory_certificate_record": "certificate_id",
    "xfactory_certificate_issuance_evidence": "issuance_evidence_id",
    "xfactory_certificate_dependent_binding": "binding_id",
    "xfactory_certificate_renewal_record": "renewal_id",
    "xfactory_certificate_revocation_propagation": "propagation_id",
}

# The closed requirement list the ratified spec delta defines. Every one MUST
# carry at least one negative confirmation; that closure is what makes the
# corpus a negative confirmation PER REQUIREMENT rather than a pile of
# negatives.
REQUIREMENTS: dict[str, str] = {
    "TA-R1": "Systems trust anchors, never individual certificates",
    "TA-R2": "A certificate issues only under recorded authority",
    "TA-R3": "Declared chain custody bounds what a certificate evidences",
    "TA-R4": "Renewal that changes key material is a rebind obligation",
    "TA-R5": "Dependent bindings are recorded against the certificate",
    "TA-R6": "Revocation propagates to the authority the certificate supported",
    "TA-R7": "Authority material and issuance credentials are credential "
             "records, never committed",
    "TA-R8": "A realization declares the obligations it cannot meet",
}

# openxWallet asks its two questions of the holder's execution context; this
# family asks them of the using host. The hazard, and therefore the mapping, is
# the same one.
OPENXWALLET_EVIDENCES = {"environment": "using_host", "holder": "named_holder"}
OPENXWALLET_BOOLEANS = {
    "key_readable_by_using_host": "key_readable_by_holder_execution_context",
    "use_requires_authorization_outside_using_host":
        "use_requires_authorization_outside_holder_execution_context",
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

# Rule (ff). OQ1's two establishment levels, ordered: a record may not assert a
# level stronger than the realization declares it ACHIEVES.
ESTABLISHMENT_RANK = {
    "per_policy_attestation_with_authority_log": 0,
    "per_certificate_record": 1,
}

# Rule (a). Property names that could only be carrying key material, and value
# shapes that are key material whatever the property is called.
_KEY_NAME_TOKENS = (
    "private", "secret", "mnemonic", "passphrase", "pkcs8", "key_material",
    "keymaterial", "privkey", "seed_phrase", "pem",
)
_KEY_NAME_ALLOW = {
    "public_key_fingerprint", "key_identifier_ref", "key_generation_ref",
    "bound_key_reference", "new_key_generation_ref",
    "superseded_key_generation_ref", "supersedes_generation_ref",
}
# Armor labels vary (`RSA`, `EC`, `OPENSSH`, `PGP … BLOCK`), and matching only
# the bare `PRIVATE KEY-----` form lets a PGP block through the same field.
_KEY_VALUE_RE = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY(?: BLOCK)?-----", re.I)
# A serialized JWK: `d` is the private exponent. The letter alone is far too
# generic to blocklist, but alongside `kty` it is unambiguous.
_JWK_PRIVATE_RE = re.compile(
    r'"kty"\s*:.*"d"\s*:\s*"|"d"\s*:\s*".*"kty"\s*:', re.S)
# Reversible encodings. The ratified text refuses "any encoding a reader can
# reverse", so the scan reverses the encodings a repository actually receives and
# re-runs the value patterns AND the DER structure test over the result. The run
# class includes the URL-safe alphabet (`-` and `_`), because base64url is one
# `translate` away from base64 and a scan that misses it teaches which encoding
# to use.
_BASE64_RUN_RE = re.compile(r"[A-Za-z0-9+/=_\-\s]{48,}")
_HEX_RUN_RE = re.compile(r"(?:[0-9a-fA-F]{2}[\s:]?){48,}")
# How many decode layers to reverse. One layer catches base64-of-PEM; a second
# catches base64-of-base64, which an adversarial review used to walk a key past
# the single-layer form.
_DECODE_DEPTH = 2

# Rule (a), the structural half. A private key is a DER structure long before it
# is an armored label, and the label is what an evader drops. These are the
# algorithm OIDs a private-key structure carries, DER-encoded with their tag and
# length so the match cannot fire on a coincidental byte run.
_DER_KEY_OIDS = {
    b"\x06\x09\x2a\x86\x48\x86\xf7\x0d\x01\x01\x01": "rsaEncryption",
    b"\x06\x07\x2a\x86\x48\xce\x3d\x02\x01": "id-ecPublicKey",
    b"\x06\x03\x2b\x65\x70": "Ed25519",
    b"\x06\x03\x2b\x65\x71": "Ed448",
    b"\x06\x03\x2b\x65\x6e": "X25519",
    b"\x06\x03\x2b\x65\x6f": "X448",
}

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
    return {path.name: load_yaml(path)
            for path in sorted(FAMILY_DIR.glob("*.schema.yaml"))}


def validator_for(kind: str, docs: dict[str, dict]) -> Draft202012Validator:
    return Draft202012Validator(
        docs[KIND_TO_SCHEMA[kind]], format_checker=FORMAT_CHECKER)


def parse_time(value: Any) -> datetime | None:
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
    documents the schema has refused (findings accumulate; validation does not
    stop), so every block read must tolerate a non-mapping without crashing the
    run and discarding every other file's findings."""
    return value if isinstance(value, dict) else {}


def _sequence(value: Any) -> list:
    """A list, or [] for anything else — the sequence twin of `_mapping`.
    `value or []` passes a truthy scalar straight to iteration, so a
    schema-invalid `dependent_rebinds: 1` would crash the run before its schema
    finding could be reported."""
    return value if isinstance(value, list) else []


def _hashable(value: Any) -> bool:
    """True when the value can be a dict key or set member. Enumerating
    unhashable TYPES undercounts — PyYAML's safe `!!set` tag yields a Python
    set, exactly as unhashable as a list — so ask the only authority there is:
    hash() itself."""
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


def _text(value: Any) -> str:
    return value if isinstance(value, str) else ""


# --------------------------- corpus context ---------------------------

class Context:
    """Everything a cross-record rule needs: the canonical chain-custody
    registry, the openxWallet registry it composes with, and an index of records
    by id."""

    def __init__(self, registry: dict, openxwallet_registry: dict,
                 canonical_registry: dict | None = None) -> None:
        self.registry = registry
        # Rule (cc). The CANONICAL registry, carried separately from whichever
        # registry document this context resolves against: a registry FIXTURE is
        # adjudicated in a context built from itself, so `registry` is not a
        # reliable answer to "which registry is the canonical one" — and a check
        # keyed on object identity would then skip exactly the document that
        # claims to be canonical and is not.
        self.canonical_registry = _mapping(
            registry if canonical_registry is None else canonical_registry)
        self.canonical_registry_id = self.canonical_registry.get("registry_id")
        self.canonical_registry_version = self.canonical_registry.get(
            "registry_version")
        self.openxwallet = {
            m["id"]: m for m in _sequence(
                openxwallet_registry.get("custody_models"))
            if isinstance(m, dict) and isinstance(m.get("id"), str)
        }
        self.assurance_rank: dict[str, int] = {
            level["id"]: level["rank"]
            for level in _sequence(registry.get("assurance_levels"))
            if isinstance(level, dict) and _hashable(level.get("id"))
            and isinstance(level.get("rank"), int)
        }
        self.custody: dict[str, dict] = {
            m["id"]: m for m in _sequence(registry.get("custody_models"))
            if isinstance(m, dict) and isinstance(m.get("id"), str)
        }
        self.floor_model = registry.get("undeclared_custody_resolves_to")
        self.anchors: dict[str, dict] = {}
        self.certificates: dict[str, dict] = {}
        self.issuances: dict[str, dict] = {}
        self.issuance_by_certificate: dict[str, list[str]] = {}
        self.bindings: dict[str, dict] = {}
        self.renewals: dict[str, dict] = {}
        self.propagations: dict[str, dict] = {}
        self.declarations: dict[str, dict] = {}
        self.obligation_entries: dict[str, tuple[str, dict]] = {}
        self.duplicate_ids: set[tuple[str, str]] = set()
        # Kept apart from `duplicate_ids`, whose members are (kind, RECORD id).
        # An obligation entry's duplicate was recorded there under the
        # declaration's kind and then looked up by REALIZATION id, so it could
        # never match and a duplicated `entry_id` — the address a shortfall
        # citation resolves through — was reported by nothing.
        self.duplicate_entry_ids: set[str] = set()

    # -- indexing -------------------------------------------------------
    def index(self, doc: dict) -> None:
        """Type-guarded: repo scans index BEFORE schema validation, so a
        malformed document must surface as a schema finding on its own file,
        never as a harness crash that discards every other file's findings."""
        kind = doc.get("kind")
        table = {
            "xfactory_trust_anchor": self.anchors,
            "xfactory_certificate_record": self.certificates,
            "xfactory_certificate_issuance_evidence": self.issuances,
            "xfactory_certificate_dependent_binding": self.bindings,
            "xfactory_certificate_renewal_record": self.renewals,
            "xfactory_certificate_revocation_propagation": self.propagations,
        }.get(kind)
        if table is not None:
            rid = doc.get(_ID_FIELDS[kind])
            if isinstance(rid, str) and rid:
                if rid in table:
                    self.duplicate_ids.add((kind, rid))
                table[rid] = doc
                if kind == "xfactory_certificate_issuance_evidence":
                    cert = doc.get("certificate_ref")
                    if isinstance(cert, str):
                        self.issuance_by_certificate.setdefault(
                            cert, []).append(rid)
        elif kind == "xfactory_trust_anchor_conformance_declaration":
            realization = _mapping(doc.get("realization")).get("realization_id")
            if isinstance(realization, str) and realization:
                if realization in self.declarations:
                    self.duplicate_ids.add((kind, realization))
                self.declarations[realization] = doc
                for entry in _sequence(doc.get("obligations")):
                    if not isinstance(entry, dict):
                        continue
                    entry_id = entry.get("entry_id")
                    if isinstance(entry_id, str) and entry_id:
                        if entry_id in self.obligation_entries:
                            self.duplicate_entry_ids.add(entry_id)
                        self.obligation_entries[entry_id] = (realization, entry)

    def copy_index_from(self, other: "Context") -> None:
        self.anchors = dict(other.anchors)
        self.certificates = dict(other.certificates)
        self.issuances = dict(other.issuances)
        self.issuance_by_certificate = {
            k: list(v) for k, v in other.issuance_by_certificate.items()}
        self.bindings = dict(other.bindings)
        self.renewals = dict(other.renewals)
        self.propagations = dict(other.propagations)
        self.declarations = dict(other.declarations)
        self.obligation_entries = dict(other.obligation_entries)
        self.duplicate_ids = set(other.duplicate_ids)
        self.duplicate_entry_ids = set(other.duplicate_entry_ids)

    # -- derived lookups ------------------------------------------------
    def rank(self, level: Any) -> int | None:
        return self.assurance_rank.get(level) if _hashable(level) else None

    @property
    def top_rank(self) -> int | None:
        ranks = [r for r in self.assurance_rank.values() if isinstance(r, int)]
        return max(ranks) if ranks else None

    def custody_for(self, block: Any) -> tuple[str | None, dict | None, bool]:
        """(model_id, member, resolved_from_floor) for a declared custody block.

        A record with no declaration resolves to the registry's declared FLOOR,
        which is the ratified rule: an undeclared certificate evidences the
        weakest member of the set and may hold no authority above it.
        """
        declared = _mapping(block).get("custody_model")
        if declared is None:
            floor = self.floor_model if isinstance(self.floor_model, str) else None
            return floor, self.custody.get(floor) if floor else None, True
        member = self.custody.get(declared) if _hashable(declared) else None
        return declared, member, False

    def obligation(self, entry_ref: Any) -> tuple[str, dict] | None:
        return (self.obligation_entries.get(entry_ref)
                if _hashable(entry_ref) else None)

    def declaration_for(self, realization: Any) -> dict | None:
        return (self.declarations.get(realization)
                if _hashable(realization) else None)

    def obligations_declared(self, realization: Any,
                             *satisfaction: str) -> set[str]:
        """The obligations this realization records with one of the given
        satisfaction values. `cannot` is a refusal at point of use; `partial` is
        a warning — see rule (w)."""
        declaration = self.declaration_for(realization)
        if declaration is None:
            return set()
        return {entry.get("obligation")
                for entry in _sequence(declaration.get("obligations"))
                if isinstance(entry, dict)
                and entry.get("satisfaction") in satisfaction
                and _hashable(entry.get("obligation"))}

    def cannot_obligations(self, realization: Any) -> set[str]:
        return self.obligations_declared(realization, "cannot")

    def operated_by_family(self, realization: Any) -> bool | None:
        """Rule (ff). Whether the realization OPERATES the authority — the fact
        the whole honest-shortfall arrangement turns on. None where no
        declaration resolves, so a caller can tell "not declared" from "false"
        rather than reading silence as the permissive answer."""
        declaration = self.declaration_for(realization)
        if declaration is None:
            return None
        value = _mapping(declaration.get("realization")).get(
            "authority_operated_by_family")
        return value if isinstance(value, bool) else None

    def achieved_establishment_level(self, realization: Any) -> Any:
        """Rule (ff). The issuance-evidence form the realization DECLARES it
        achieves, read off the TA-R2 entry where the schema requires it."""
        declaration = self.declaration_for(realization)
        if declaration is None:
            return None
        for entry in _sequence(declaration.get("obligations")):
            if isinstance(entry, dict) and entry.get("obligation") == "TA-R2":
                return entry.get("achieved_establishment_level")
        return None

    def supersession_accounted(self, certificate_ref: Any, current: Any,
                              superseded: Any) -> bool:
        """Rule (ee). Whether some renewal record OWNS the key change the
        certificate's `supersedes_generation_ref` records.

        The escape matters: a certificate whose current generation supersedes an
        earlier one may be renewed again with the key PRESERVED, and that later
        renewal is conformant. What is not conformant is a supersession no
        renewal accounts for at all — the rebind obligation then exists and no
        record carries it.
        """
        for renewal in self.renewals.values():
            if renewal.get("certificate_ref") != certificate_ref:
                continue
            change = _mapping(renewal.get("key_change"))
            if change.get("changed") is True \
                    and change.get("new_key_generation_ref") == current \
                    and change.get("superseded_key_generation_ref") == superseded:
                return True
        return False

    def anchor_custody_cap(self, anchor_id: Any) -> tuple[int, str, str] | None:
        """Rule (bb). The tightest cap the anchor CHAIN imposes, as
        (rank, anchor_id, custody_model), or None where no anchor in the chain
        has a key readable by its using host.

        Walks parent references upward with a visited set: a malformed corpus
        must report findings rather than spin, and a cycle here would hang the
        whole run rather than fail one document.
        """
        cap: tuple[int, str, str] | None = None
        seen: set[str] = set()
        current = anchor_id
        while _hashable(current) and current not in seen:
            seen.add(current)
            anchor = self.anchors.get(current)
            if anchor is None:
                break
            model_id, member, _floor = self.custody_for(
                anchor.get("declared_chain_custody"))
            if isinstance(member, dict) and \
                    member.get("key_readable_by_using_host") is True:
                rank = self.rank(member.get("assurance_ceiling"))
                if rank is not None and (cap is None or rank < cap[0]):
                    cap = (rank, str(current), str(model_id))
            current = _mapping(anchor.get("chain_position")).get(
                "parent_anchor_ref")
        return cap

    def anchor_lineage(self, anchor_id: str) -> set[str]:
        """The anchor and every anchor beneath it, for the transitive-revocation
        closure. Cycle-guarded: a malformed corpus must report findings, not
        spin."""
        reached = {anchor_id}
        changed = True
        while changed:
            changed = False
            for aid, anchor in self.anchors.items():
                parent = _mapping(anchor.get("chain_position")).get(
                    "parent_anchor_ref")
                if aid not in reached and parent in reached:
                    reached.add(aid)
                    changed = True
        return reached


# --------------------------- rule (a): key material ---------------------------

def _der_length_offset(data: bytes) -> int | None:
    """Where a DER value's contents begin, or None if the length header is not
    well formed. Needed because the version INTEGER that identifies a private
    key sits AFTER a length header whose own size varies with the key."""
    if len(data) < 2:
        return None
    first = data[1]
    if first < 0x80:
        return 2
    count = first & 0x7F
    if count == 0 or count > 4 or len(data) < 2 + count:
        return None
    return 2 + count


def _der_private_key_reason(data: bytes) -> str | None:
    """Why these BYTES are a private key, or None.

    Structure, not armor. Every serialization a repository actually receives
    starts with a SEQUENCE and then says which private key it is:

      * PKCS#8 `PrivateKeyInfo` — version INTEGER 0, then an AlgorithmIdentifier
        SEQUENCE carrying the algorithm OID.
      * PKCS#1 `RSAPrivateKey` — version INTEGER 0, then the modulus INTEGER.
      * SEC1 `ECPrivateKey` — version INTEGER 1, then the private-key OCTET
        STRING.

    Each test requires the SEQUENCE, a well-formed length header AND the version
    prologue, so it cannot fire on a coincidental byte run — which matters
    because this test runs over every decoded candidate in every document.
    """
    # 24 bytes is enough for the prologue that identifies the structure, and the
    # test below is specific enough to carry the floor: SEQUENCE, a well-formed
    # length header, the version INTEGER, and then either an AlgorithmIdentifier
    # or a big modulus. A TRUNCATED key is still a key's prologue, and a fixture
    # that carries only the first line of a PEM is the form key material actually
    # arrives in a repository.
    if len(data) < 24 or data[0] != 0x30:
        return None
    start = _der_length_offset(data)
    if start is None:
        return None
    body = data[start:]
    if body[:3] == b"\x02\x01\x00":  # version 0
        rest = body[3:]
        if rest[:1] == b"\x30":  # AlgorithmIdentifier => PKCS#8 PrivateKeyInfo
            for oid, name in _DER_KEY_OIDS.items():
                if oid in rest[:64]:
                    return f"a PKCS#8 PrivateKeyInfo for {name}"
            return "a PKCS#8 PrivateKeyInfo prologue"
        if rest[:1] == b"\x02" and len(rest) > 4 and rest[1] in (0x81, 0x82):
            return "a PKCS#1 RSAPrivateKey"
    if body[:3] == b"\x02\x01\x01" and b"\x04" in body[3:5]:
        return "a SEC1 ECPrivateKey"
    return None


def _decoded_candidates(value: str,
                        depth: int = _DECODE_DEPTH) -> list[tuple[str, bytes]]:
    """(label, decoded-bytes) pairs for the reversible encodings a repository
    actually receives, reversed up to `depth` layers.

    Failures are silent by design: most long strings are not encoded material,
    and the point is to catch the ones that are. Bytes rather than text, because
    the structural test (`_der_private_key_reason`) reads bytes and decoding to
    text with `errors="replace"` destroys exactly the bytes it reads.
    """
    out: list[tuple[str, bytes]] = []
    if depth <= 0:
        return out
    for match in _BASE64_RUN_RE.findall(value):
        cleaned = re.sub(r"\s+", "", match)
        if len(cleaned) < 48:
            continue
        # Two readings of the same run, because a run is rarely just the payload:
        #
        #  * the WHOLE run with the URL-safe alphabet translated in, since
        #    base64url is one `translate` away and a scan that reverses only the
        #    standard alphabet teaches which alphabet to use; and
        #  * each maximal STANDARD-ALPHABET segment, because the run class has to
        #    admit `-` for base64url and that makes it swallow the armor lines
        #    and the prose around a payload — which shifts the decode and hides
        #    a key that was sitting in plain sight. Segments recover the payload
        #    from "TE KEY-----<body>-----END …" and from a sentence wrapped
        #    around a blob.
        candidates = [cleaned.replace("-", "+").replace("_", "/")]
        candidates += [seg for seg in re.findall(r"[A-Za-z0-9+/]{32,}", cleaned)
                       if seg not in candidates]
        for blob in candidates:
            try:
                decoded = base64.b64decode(blob + "=" * (-len(blob) % 4),
                                           validate=False)
            except (binascii.Error, ValueError):
                continue
            out.append(("base64", decoded))
    for match in _HEX_RUN_RE.findall(value):
        blob = re.sub(r"[\s:]+", "", match)
        if len(blob) % 2:
            blob = blob[:-1]
        try:
            decoded = bytes.fromhex(blob)
        except ValueError:
            continue
        out.append(("hex", decoded))
    # One further layer: base64-of-base64 walked past the single-layer form.
    for encoding, decoded in list(out):
        text = decoded.decode("utf-8", errors="ignore")
        if not text:
            continue
        for inner_encoding, inner in _decoded_candidates(text, depth - 1):
            out.append((f"{encoding}-then-{inner_encoding}", inner))
    return out


def _encoded_key_reason(value: str) -> tuple[str, str] | None:
    """(encoding, why) for the first decoded candidate that is key material, by
    ARMOR or by DER STRUCTURE. The structural half is what makes the scan
    armor-independent: an unarmored DER blob is a key with the label removed."""
    for encoding, decoded in _decoded_candidates(value):
        reason = _der_private_key_reason(decoded)
        if reason:
            return encoding, reason
        text = decoded.decode("utf-8", errors="replace")
        if _KEY_VALUE_RE.search(text):
            return encoding, "an armored private key block"
        if _JWK_PRIVATE_RE.search(text):
            return encoding, "a serialized JWK carrying its private exponent"
    return None


def check_no_key_material(f: Findings, label: str, node: Any,
                          path: str = "") -> None:
    """Rule (a), in two passes.

    Pass one walks names and values. Pass two joins the document's strings IN
    DOCUMENT ORDER and re-runs the armor match over the concatenation, because a
    label torn across two fields ("…BEGIN EC PRIVA" / "TE KEY-----") is
    conformant in every field and a key in the document. The joined pass is
    skipped when pass one already reported a key, so an ordinary
    single-field key is reported once.
    """
    strings: list[str] = []
    reported = _walk_key_material(f, label, node, path, strings)
    if reported or not strings:
        return
    joined = "".join(strings)
    if _KEY_VALUE_RE.search(joined) or _JWK_PRIVATE_RE.search(joined):
        f.error("key-material-embedded",
                f"{label}: the document's field values, read in order, contain "
                f"a private key block whose armor label is SPLIT ACROSS FIELDS; "
                f"each field is conformant on its own and the document is a "
                f"committed authority key, which is a compromised one")
        return
    reason = _encoded_key_reason(joined)
    if reason is not None:
        encoding, why = reason
        f.error("key-material-reversibly-encoded",
                f"{label}: the document's field values, read in order, decode "
                f"({encoding}) to {why}; splitting the blob across fields is "
                f"still an encoding a reader can reverse")


def _walk_key_material(f: Findings, label: str, node: Any, path: str,
                       strings: list[str]) -> bool:
    """The walking half of rule (a). Returns True where a finding already fired,
    which is what tells the joined pass it has nothing to add."""
    reported = False
    if isinstance(node, dict):
        # A JWK carries its private exponent under the single letter `d`, which
        # is far too generic a property name to blocklist on its own — but
        # alongside `kty` it is unambiguous, and it is how a key most plausibly
        # arrives as structured data rather than as armored text.
        if "kty" in node and "d" in node:
            f.error("key-material-embedded",
                    f"{label}: object at {path or '<root>'!r} is a JWK carrying "
                    f"its private exponent 'd'; an anchor references key "
                    f"material and never carries it")
            reported = True
        for name, value in node.items():
            here = f"{path}.{name}" if path else str(name)
            lname = str(name).lower()
            if lname not in _KEY_NAME_ALLOW and any(
                    tok in lname for tok in _KEY_NAME_TOKENS):
                f.error("key-material-embedded",
                        f"{label}: property {here!r} is key-material-shaped; "
                        f"authority key material exists only as a "
                        f"credential-contracts record with a vault binding, "
                        f"never in a repository")
            reported |= _walk_key_material(f, label, value, here, strings)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            reported |= _walk_key_material(f, label, item, f"{path}[{i}]",
                                          strings)
    elif isinstance(node, str):
        strings.append(node)
        if _KEY_VALUE_RE.search(node):
            f.error("key-material-embedded",
                    f"{label}: value at {path!r} contains a private key block; "
                    f"the property is conformant but the VALUE is key material, "
                    f"and a committed authority key is a compromised one")
            reported = True
        elif _JWK_PRIVATE_RE.search(node):
            f.error("key-material-embedded",
                    f"{label}: value at {path!r} is a serialized JWK carrying "
                    f"its private exponent 'd'; every object in this family is "
                    f"closed, so a JWK can only arrive as a STRING — which is "
                    f"exactly why the value scan has to look for one")
            reported = True
        else:
            reason = _encoded_key_reason(node)
            if reason is not None:
                encoding, why = reason
                f.error("key-material-reversibly-encoded",
                        f"{label}: value at {path!r} is {encoding}-encoded key "
                        f"material ({why}); the ratified text refuses ANY "
                        f"encoding a reader "
                        f"can reverse — armored or not, since the armor is a "
                        f"LABEL and the key is a STRUCTURE — and admits no "
                        f"exception for test, demonstration or QA material: a "
                        f"non-production authority's key is still an authority "
                        f"key")
                reported = True
    return reported


# --------------------- rules (b)-(g), (cc): the custody registry ---------------------

def _canonical_text(value: Any) -> str:
    """A stable, order-insensitive rendering for comparison. `safe_dump` can
    refuse a value a malformed document supplies, and a RepresenterError here
    would abort the whole run as a harness error — discarding every other file's
    findings — so the fallback is `repr`, which compares just as well."""
    try:
        return yaml.safe_dump(value, sort_keys=True)
    except yaml.YAMLError:
        return repr(value)


def _registry_content(doc: dict) -> Any:
    """The parts of a registry document that ARE the closed set. Two documents
    claiming one `registry_id` may be the same set shipped twice (a domain repo
    vendoring the pinned openxFactory bundle is the ordinary case) but they may
    not be two different sets."""
    return (
        doc.get("registry_version"),
        _canonical_text(doc.get("assurance_levels")),
        _canonical_text(doc.get("custody_models")),
        _canonical_text(doc.get("undeclared_custody_resolves_to")),
    )


def check_custody_registry(f: Findings, label: str, doc: dict,
                           ctx: Context) -> None:
    # (cc) a second document claiming the canonical registry_id. An identical
    # copy is the vendoring path and is fine; a DIFFERENT set under the same id
    # is a second closed set that records can cite and readers can believe,
    # which is the whole failure this family's `evidences` derivation exists to
    # refuse, one level up.
    if doc.get("registry_id") == ctx.canonical_registry_id \
            and _registry_content(doc) != _registry_content(
                ctx.canonical_registry):
        f.error("custody-registry-duplicate-claim",
                f"{label}: claims registry_id "
                f"{ctx.canonical_registry_id!r} while declaring a DIFFERENT "
                f"closed set from the canonical registry. Two documents may "
                f"carry one registry id only as the same set; a diverging copy "
                f"beside the records that cite it is how a renamed ladder or a "
                f"promoted member gets adjudicated as though it were ratified")

    models = _sequence(doc.get("custody_models"))
    levels = {level.get("id"): level.get("rank")
              for level in _sequence(doc.get("assurance_levels"))
              if isinstance(level, dict) and _hashable(level.get("id"))
              and isinstance(level.get("rank"), int)}
    # Rule (c) keys on the TOP RANK rather than on a level's id. Naming the
    # level would make the rule depend on a string a registry is free to choose,
    # so renaming the top level would silently disable the check — the same "it
    # all validates cleanly" failure this family exists to refuse.
    top_rank = max((r for r in levels.values() if isinstance(r, int)),
                   default=None)

    seen_ids: set[str] = set()
    discriminators: dict[tuple[Any, Any], str] = {}
    for member in models:
        if not isinstance(member, dict):
            continue
        mid = member.get("id") if isinstance(member.get("id"), str) else "<unnamed>"
        if mid in seen_ids:
            f.error("custody-duplicate-member",
                    f"{label}: custody model {mid!r} declared twice")
        seen_ids.add(mid)

        readable = member.get("key_readable_by_using_host")
        per_use = member.get("use_requires_authorization_outside_using_host")
        declared = member.get("evidences")

        # (b) the derivation, enforced rather than trusted.
        derived = ("named_holder" if (readable is False and per_use is True)
                   else "using_host")
        if declared != derived:
            f.error("custody-evidences-derivation",
                    f"{label}: custody model {mid!r} declares evidences="
                    f"{declared!r} but its properties derive {derived!r} "
                    f"(readable={readable!r}, per_use_authorization={per_use!r}). "
                    f"`evidences` is derived, never asserted: a key readable by "
                    f"the host that uses it evidences the USING HOST, and only "
                    f"isolation WITH an authorization that host cannot supply "
                    f"evidences the NAMED HOLDER")

        # (c) the top assurance level must be earned.
        ceiling = member.get("assurance_ceiling")
        if not isinstance(ceiling, str) or ceiling not in levels:
            f.error("custody-ceiling-unknown",
                    f"{label}: custody model {mid!r} caps at {ceiling!r}, which "
                    f"is not a declared assurance level")
        elif (top_rank is not None and levels.get(ceiling) == top_rank
                and declared != "named_holder"):
            f.error("custody-ceiling-unearned",
                    f"{label}: custody model {mid!r} caps at {ceiling!r}, the "
                    f"HIGHEST level this ladder declares, while evidencing "
                    f"{declared!r}; an act with nothing standing between the "
                    f"certificate and the effect requires evidence that the "
                    f"NAMED HOLDER acted")

        # (e) one custody axis. `evidences` derives from exactly two booleans,
        # so two members declaring the same pair differ only in something this
        # axis cannot express — operator escrow (ruled a relationship on the
        # credential record, not a tier) is the live example, and a rename is
        # the other.
        if _hashable(readable) and _hashable(per_use):
            pair = (readable, per_use)
            if pair in discriminators:
                f.error("custody-discriminator-duplicated",
                        f"{label}: custody model {mid!r} declares the same "
                        f"discriminator pair as {discriminators[pair]!r} "
                        f"(readable={readable!r}, per_use={per_use!r}); the two "
                        f"differ only in a fact this axis cannot express, which "
                        f"is either a second axis smuggled in — escrow is a "
                        f"relationship on the credential record, not a custody "
                        f"tier — or a rename that would let one member claim "
                        f"the other's authority")
            else:
                discriminators[pair] = mid

        # (f) the openxWallet mapping resolves and agrees, read at run time.
        mapped_id = member.get("openxwallet_custody_model")
        mapped = (ctx.openxwallet.get(mapped_id)
                  if _hashable(mapped_id) else None)
        if mapped_id is None:
            f.error("custody-openxwallet-mapping-missing",
                    f"{label}: custody model {mid!r} names no openxWallet "
                    f"counterpart; this set COMPOSES with that ratified rule "
                    f"rather than restating a second custody model, and an "
                    f"unmapped member is the beginning of the second model")
        elif mapped is None:
            f.error("custody-openxwallet-mapping-unresolved",
                    f"{label}: custody model {mid!r} maps to openxWallet member "
                    f"{mapped_id!r}, which the canonical openxWallet registry "
                    f"({sorted(ctx.openxwallet)}) does not declare")
        else:
            for here, there in OPENXWALLET_BOOLEANS.items():
                if member.get(here) != mapped.get(there):
                    f.error("custody-openxwallet-mapping-mismatch",
                            f"{label}: custody model {mid!r} declares "
                            f"{here}={member.get(here)!r} while the openxWallet "
                            f"member it claims to be ({mapped_id!r}) declares "
                            f"{there}={mapped.get(there)!r}; the two registries "
                            f"cannot disagree about the same question, or they "
                            f"are two custody models rather than one")
            expected = OPENXWALLET_EVIDENCES.get(mapped.get("evidences"))
            if expected is not None and declared != expected:
                f.error("custody-openxwallet-mapping-mismatch",
                        f"{label}: custody model {mid!r} evidences {declared!r} "
                        f"while openxWallet member {mapped_id!r} evidences "
                        f"{mapped.get('evidences')!r} (which corresponds to "
                        f"{expected!r})")

    # (d) the collapse check, keyed on WHAT A MODEL EVIDENCES rather than on
    # readability. Readability is only one route to evidencing the host: a key
    # isolated from the using host but presentable by it WITHOUT LIMIT evidences
    # the host too, and keying on readability would leave that middle case in
    # neither list and free to outrank the holder-evidencing member.
    holder_members = [m for m in models if isinstance(m, dict)
                      and m.get("evidences") == "named_holder"]
    host_members = [m for m in models if isinstance(m, dict)
                    and m.get("evidences") == "using_host"]
    for host_member in host_members:
        h_rank = levels.get(host_member.get("assurance_ceiling")) \
            if _hashable(host_member.get("assurance_ceiling")) else None
        for holder_member in holder_members:
            if host_member is holder_member:
                continue  # a self-comparison carries no information
            k_rank = levels.get(holder_member.get("assurance_ceiling")) \
                if _hashable(holder_member.get("assurance_ceiling")) else None
            if h_rank is None or k_rank is None:
                continue
            if h_rank >= k_rank:
                f.error("custody-collapse",
                        f"{label}: custody model {host_member.get('id')!r} "
                        f"evidences only the USING HOST yet caps at or above "
                        f"{holder_member.get('id')!r}, which evidences the "
                        f"NAMED HOLDER; the weaker case can claim the stronger "
                        f"case's assurance and the distinction the ruling drew "
                        f"is lost")

    if not holder_members:
        f.error("custody-holder-tier-absent",
                f"{label}: no custody model evidences the NAMED HOLDER; the "
                f"enumeration must be able to express the case it exists to "
                f"distinguish")
    if not host_members:
        f.error("custody-host-tier-absent",
                f"{label}: no custody model evidences only the USING HOST; the "
                f"enumeration must name the case it exists to refuse assurance "
                f"to")

    # (g) the floor is a weakest member — resolved in THIS DOCUMENT'S members.
    # Resolving it in the canonical registry made the rule report
    # `custody-floor-unknown` for any registry that renamed its members, so the
    # weakest-member comparison was never reached: the check failed OPEN on
    # exactly the document it exists to adjudicate.
    own_members = {m["id"]: m for m in models
                   if isinstance(m, dict) and isinstance(m.get("id"), str)}
    floor_id = doc.get("undeclared_custody_resolves_to")
    floor = own_members.get(floor_id) if _hashable(floor_id) else None
    if floor is None:
        f.error("custody-floor-unknown",
                f"{label}: undeclared_custody_resolves_to names {floor_id!r}, "
                f"which is not a member of this registry")
    else:
        # The weakest member of the DEFINED SET, which is the minimum ceiling any
        # member reaches — not the ladder's lowest level. A ladder may declare a
        # level no member caps at (channel authentication is one), and keying the
        # floor on the ladder would then demand a member nothing declares.
        member_ranks = [levels.get(m.get("assurance_ceiling"))
                        for m in models if isinstance(m, dict)
                        and _hashable(m.get("assurance_ceiling"))]
        min_rank = min((r for r in member_ranks if isinstance(r, int)),
                       default=None)
        floor_rank = levels.get(floor.get("assurance_ceiling")) \
            if _hashable(floor.get("assurance_ceiling")) else None
        if (floor.get("evidences") != "using_host"
                or floor.get("key_readable_by_using_host") is not True
                or (min_rank is not None and floor_rank != min_rank)):
            f.error("custody-floor-not-weakest",
                    f"{label}: the declared floor {floor_id!r} is not a weakest "
                    f"member (evidences={floor.get('evidences')!r}, "
                    f"readable={floor.get('key_readable_by_using_host')!r}, "
                    f"ceiling rank={floor_rank!r} against the weakest "
                    f"member's {min_rank!r}); "
                    f"an undeclared certificate resolves here, so a floor above "
                    f"the weakest member means absence of a declaration BUYS "
                    f"authority")


# --------------------------- shared helpers ---------------------------

def _shortfall_ok(f: Findings, label: str, ctx: Context, ref: Any,
                  obligation: str, realization: Any, claim_moment: Any,
                  what: str) -> None:
    """Rule (n): a declared gap is only a gap where the DECLARATION says so —
    by the same realization, for this obligation, and in time."""
    resolved = ctx.obligation(ref)
    if resolved is None:
        f.error("obligation-undeclared",
                f"{label}: {what} names declared shortfall {ref!r}, which "
                f"resolves to no obligation entry; an undeclared shortfall is "
                f"non-conformance even where the identical shortfall, declared, "
                f"would be conformant")
        return
    owner, entry = resolved
    if realization is not None and owner != realization:
        f.error("obligation-undeclared",
                f"{label}: {what} names shortfall entry {ref!r}, which belongs "
                f"to realization {owner!r} rather than {realization!r}; another "
                f"realization's declaration covers nothing here")
    if entry.get("obligation") != obligation:
        f.error("obligation-undeclared",
                f"{label}: {what} names shortfall entry {ref!r}, which declares "
                f"{entry.get('obligation')!r} rather than {obligation}")
    elif entry.get("satisfaction") not in ("partial", "cannot"):
        f.error("obligation-undeclared",
                f"{label}: {what} names shortfall entry {ref!r}, which records "
                f"{obligation} as {entry.get('satisfaction')!r}; a shortfall "
                f"covered by an obligation declared SATISFIED is an undeclared "
                f"shortfall, and asserting the evidence instead is what the "
                f"ratified text refuses")
    # Rule (ff). The R7 shortfall is the honest position for an authority the
    # family does NOT operate, and the dishonest one for an authority it does —
    # the ratified sentence says both halves, and only the first was mechanism.
    # An operator that can produce a credential record and declares that it
    # cannot is excusing itself with a field, which is exactly the loophole the
    # declared-obligation rule is otherwise designed to close.
    if obligation == "TA-R7" and ctx.operated_by_family(realization) is True:
        f.error("family-operated-shortfall-claimed",
                f"{label}: {what} cites shortfall entry {ref!r} while "
                f"realization {realization!r} declares "
                f"authority_operated_by_family: true. A realization that "
                f"OPERATES the authority can produce a credential record with a "
                f"vault binding for its key material, so there is no shortfall "
                f"to declare — the declared-shortfall shape is for an authority "
                f"the family does not run, and using it here excuses the record "
                f"from the obligation by asserting a fact about someone else")

    # Rule (gg). The lateness guard used to SKIP when either moment was absent,
    # so omitting two optional timestamps disabled it entirely — a guard that
    # fails open on the record that wants it to. A citation with no moment cannot
    # be shown to be timely, and unshowable is refused rather than assumed.
    declared_at = parse_time(entry.get("declared_at"))
    claimed_at = parse_time(claim_moment)
    if claimed_at is None:
        f.error("shortfall-claim-moment-missing",
                f"{label}: {what} cites shortfall entry {ref!r} while carrying "
                f"no moment of its own ({claim_moment!r}), so whether the gap "
                f"was declared BEFORE the claim cannot be established. "
                f"Declaring a gap afterwards does not validate the claims made "
                f"while the realization was silent, and a record with no moment "
                f"is indistinguishable from a backdated one")
    elif declared_at is None:
        f.error("shortfall-claim-moment-missing",
                f"{label}: {what} cites shortfall entry {ref!r}, which carries "
                f"no declared_at, so the lateness guard has nothing to compare "
                f"against")
    elif declared_at > claimed_at:
        f.error("shortfall-declared-after-the-claim",
                f"{label}: {what} was recorded at {claim_moment} while the "
                f"shortfall entry {ref!r} was declared at "
                f"{entry.get('declared_at')}; declaring a gap afterwards does "
                f"not validate the claims made while the realization was "
                f"silent")


def _check_registry_pointer(f: Findings, label: str, ctx: Context, block: Any,
                            what: str) -> None:
    """Rule (cc). The pointer a record carries names the closed set it is
    adjudicated against, so it has to BE that set.

    A decorative pointer is worse than none: it invites a diverging registry to
    ship beside the records that cite it, with the records validating against the
    canonical set and a reader believing the shipped one.
    """
    block = _mapping(block)
    if not block:
        return
    declared_id = block.get("registry_id")
    if declared_id is not None and declared_id != ctx.canonical_registry_id:
        f.error("custody-registry-pointer-mismatch",
                f"{label}: {what} cites registry {declared_id!r} while custody "
                f"in this family is declared from {ctx.canonical_registry_id!r} "
                f"— which is the registry this record's `evidences` and ceiling "
                f"were actually derived from. A record cannot be adjudicated "
                f"against one closed set while naming another")
    declared_version = block.get("registry_version")
    if declared_version is not None and \
            declared_version != ctx.canonical_registry_version:
        f.error("custody-registry-pointer-mismatch",
                f"{label}: {what} cites registry version {declared_version!r} "
                f"while the canonical registry is version "
                f"{ctx.canonical_registry_version!r}; a version nobody resolves "
                f"is a version a diverging copy can claim")


# ------------- rules (h)-(k), (bb), (cc), (ff), (gg): the anchor record -------------

def check_anchor(f: Findings, label: str, doc: dict, ctx: Context) -> None:
    block = _mapping(doc.get("declared_chain_custody"))
    _check_registry_pointer(f, label, ctx, block, "anchor custody")
    model_id, member, _floor = ctx.custody_for(block)
    if member is None:
        # (h) the closed set binds where a record DECLARES, not only where a
        # ceiling is compared. An unrecognised model would otherwise make every
        # ceiling derived from it resolve to nothing.
        f.error("custody-model-unknown",
                f"{label}: declares custody model {model_id!r}, which is not a "
                f"member of the closed registry ({sorted(ctx.custody)}); "
                f"custody is declared FROM A CLOSED SET, and an unrecognised "
                f"model is refused rather than treated as uncapped")
    else:
        # (k) authority material at the strictest tier, or a declared shortfall.
        ceiling_rank = ctx.rank(member.get("assurance_ceiling"))
        if (ctx.top_rank is not None and ceiling_rank is not None
                and ceiling_rank < ctx.top_rank):
            ref = block.get("declared_shortfall_ref")
            if ref is None:
                f.error("anchor-custody-below-strictest-tier",
                        f"{label}: anchor key custody {model_id!r} caps at "
                        f"{member.get('assurance_ceiling')!r}, below the "
                        f"strictest member the closed set declares, and no "
                        f"shortfall is declared. Authority key material sits at "
                        f"the strictest custody tier the family operates; where "
                        f"it cannot, the realization DECLARES that rather than "
                        f"leaving a reader to assume the strongest case")
            else:
                _shortfall_ok(f, label, ctx, ref, "TA-R7",
                              doc.get("realization_ref"),
                              block.get("declared_at") or doc.get("created_at"),
                              "anchor custody below the strictest tier")
    # (k, second half) the key lives in a credential record with a vault
    # binding, or the realization has declared that neither can be produced. The
    # schema admits only those two shapes; this is where the declared one is
    # held to being a real declaration rather than a reference to anything.
    if not (block.get("credential_record_ref") and block.get("vault_binding_ref")):
        ref = block.get("declared_shortfall_ref")
        if ref is not None:
            _shortfall_ok(f, label, ctx, ref, "TA-R7",
                          doc.get("realization_ref"),
                          block.get("declared_at") or doc.get("created_at"),
                          "an anchor whose key material has no credential "
                          "record")

    # (l) the chain resolves and is coherent.
    position = _mapping(doc.get("chain_position"))
    parent_ref = position.get("parent_anchor_ref")
    if position.get("role") == "subordinate":
        parent = ctx.anchors.get(parent_ref) if _hashable(parent_ref) else None
        if parent is None:
            f.error("chain-parent-unresolved",
                    f"{label}: parent anchor {parent_ref!r} does not resolve, "
                    f"so this subordinate's chain terminates in no held anchor; "
                    f"an unresolvable parent is refused rather than passed over")
        else:
            p_depth = _mapping(parent.get("chain_position")).get("path_depth")
            depth = position.get("path_depth")
            if isinstance(p_depth, int) and isinstance(depth, int) \
                    and depth != p_depth + 1:
                f.error("chain-depth-incoherent",
                        f"{label}: declares path depth {depth} under parent "
                        f"{parent_ref!r} at depth {p_depth}; a subordinate sits "
                        f"exactly one below its parent, or the chain a consumer "
                        f"walks is not the chain the records describe")
            p_valid = _mapping(parent.get("validity"))
            own_end = parse_time(_mapping(doc.get("validity")).get("not_after"))
            parent_end = parse_time(p_valid.get("not_after"))
            if own_end and parent_end and own_end > parent_end:
                f.error("certificate-outlives-anchor",
                        f"{label}: subordinate anchor validity ends "
                        f"{_mapping(doc.get('validity')).get('not_after')}, "
                        f"after its parent {parent_ref!r} ends "
                        f"{p_valid.get('not_after')}; an anchor's window bounds "
                        f"everything beneath it, and remaining validity of its "
                        f"own does not extend the parent's")
            # (bb) a subordinate cannot out-claim a readable parent key.
            cap = ctx.anchor_custody_cap(parent_ref)
            own_rank = ctx.rank(member.get("assurance_ceiling")) \
                if isinstance(member, dict) else None
            if cap is not None and own_rank is not None and own_rank > cap[0]:
                f.error("chain-custody-not-monotone",
                        f"{label}: declares custody {model_id!r} capping at "
                        f"{member.get('assurance_ceiling')!r} beneath anchor "
                        f"{cap[1]!r}, whose own custody {cap[2]!r} leaves its "
                        f"private key READABLE BY THE USING HOST. Anything with "
                        f"read access to that host can issue under this chain, "
                        f"anywhere, indefinitely — so no record beneath it can "
                        f"carry more assurance than that anchor does, whatever "
                        f"its own custody is")

    if doc.get("state") == "revoked" and not _mapping(doc.get("revocation")).get(
            "propagation_ref"):
        f.warn("revocation-propagation-unnamed",
               f"{label}: anchor is revoked and its revocation names no "
               f"propagation record; the transitive revocation it owes is then "
               f"untraceable from the anchor")


# --------- rules (h)-(x), (bb)-(ee): the certificate record ---------

def check_certificate(f: Findings, label: str, doc: dict, ctx: Context) -> None:
    block = doc.get("declared_chain_custody")
    _check_registry_pointer(f, label, ctx, block, "certificate custody")
    model_id, member, from_floor = ctx.custody_for(block)
    if member is None:
        f.error("custody-model-unknown",
                f"{label}: resolves custody model {model_id!r}, which is not a "
                f"member of the closed registry ({sorted(ctx.custody)}); "
                f"custody is declared FROM A CLOSED SET, and an unrecognised "
                f"model is refused rather than treated as uncapped — otherwise "
                f"every ceiling derived from it resolves to nothing")
    else:
        # (i) evidences and ceiling are DERIVED, including from the floor.
        expected = member.get("evidences")
        if doc.get("evidences") != expected:
            f.error("certificate-evidences-derivation",
                    f"{label}: records evidences={doc.get('evidences')!r} while "
                    f"custody {model_id!r}"
                    f"{' (the registry floor, no custody declared)' if from_floor else ''}"
                    f" derives {expected!r}; what a certificate evidences comes "
                    f"from the declared custody, never from the certificate's "
                    f"own contents or its record's assertion")
        expected_ceiling = member.get("assurance_ceiling")
        if doc.get("assurance_ceiling") != expected_ceiling:
            f.error("certificate-ceiling-derivation",
                    f"{label}: records assurance_ceiling="
                    f"{doc.get('assurance_ceiling')!r} while custody "
                    f"{model_id!r}"
                    f"{' (the registry floor, no custody declared)' if from_floor else ''}"
                    f" caps at {expected_ceiling!r}; raising assurance is a "
                    f"custody change, not a claim")
        if (not from_floor and member.get("key_readable_by_using_host") is True
                and not (_mapping(block).get("credential_record_ref")
                         and _mapping(block).get("vault_binding_ref"))):
            f.error("custody-credential-record-missing",
                    f"{label}: custody {model_id!r} is readable by the using "
                    f"host, so this record must name the credential-contracts "
                    f"record and vault binding that hold the material")

    # (l) the anchor resolves, bounds this certificate, and is held.
    anchor_ref = doc.get("anchor_ref")
    anchor = ctx.anchors.get(anchor_ref) if _hashable(anchor_ref) else None
    evaluation = _mapping(doc.get("trust_evaluation"))
    outcome = evaluation.get("outcome")
    refusal = _mapping(evaluation.get("refusal"))
    if anchor is None:
        if outcome == "trusted":
            f.error("trusted-without-held-anchor",
                    f"{label}: recorded as trusted while its anchor "
                    f"{anchor_ref!r} resolves to no held anchor record. A "
                    f"certificate is trusted only through an anchor the "
                    f"evaluating system already holds; a certificate accepted "
                    f"on its own strength is an untrusted certificate however "
                    f"well-formed it is")
        elif refusal.get("code") == "missing_anchor":
            if refusal.get("missing_anchor_ref") != anchor_ref:
                f.error("refusal-names-the-wrong-absence",
                        f"{label}: refused for a missing anchor but names "
                        f"{refusal.get('missing_anchor_ref')!r} rather than the "
                        f"anchor that is missing ({anchor_ref!r})")
        else:
            f.warn("anchor-unresolved",
                   f"{label}: anchor {anchor_ref!r} does not resolve in this "
                   f"corpus; the chain rules that bound this certificate cannot "
                   f"be checked")
    else:
        own_end = parse_time(_mapping(doc.get("validity")).get("not_after"))
        anchor_end = parse_time(_mapping(anchor.get("validity")).get("not_after"))
        if own_end and anchor_end and own_end > anchor_end:
            f.error("certificate-outlives-anchor",
                    f"{label}: validity ends "
                    f"{_mapping(doc.get('validity')).get('not_after')} while its "
                    f"anchor {anchor_ref!r} ends "
                    f"{_mapping(anchor.get('validity')).get('not_after')}; "
                    f"certificates chaining to an anchor stop being trusted "
                    f"when its window closes, and a certificate's own remaining "
                    f"validity does not extend the anchor's")
        if outcome == "trusted":
            if anchor.get("state") != "held":
                f.error("trusted-under-closed-anchor",
                        f"{label}: recorded as trusted while anchor "
                        f"{anchor_ref!r} is {anchor.get('state')!r}; a withdrawn "
                        f"or revoked anchor stops trusting its subordinates from "
                        f"that moment")
            evaluated = parse_time(evaluation.get("evaluated_at"))
            if evaluated and anchor_end and evaluated > anchor_end:
                f.error("trusted-under-closed-anchor",
                        f"{label}: evaluated {evaluation.get('evaluated_at')}, "
                        f"after anchor {anchor_ref!r} left its validity window "
                        f"at {_mapping(anchor.get('validity')).get('not_after')}")
        # (bb) the chain caps what this certificate may claim.
        cap = ctx.anchor_custody_cap(anchor_ref)
        own_rank = ctx.rank(doc.get("assurance_ceiling"))
        if cap is not None and own_rank is not None and own_rank > cap[0]:
            f.error("chain-custody-not-monotone",
                    f"{label}: carries assurance ceiling "
                    f"{doc.get('assurance_ceiling')!r} while anchor {cap[1]!r} "
                    f"in its chain declares custody {cap[2]!r}, whose private "
                    f"key is READABLE BY THE USING HOST. A certificate cannot "
                    f"evidence that the NAMED HOLDER acted when anything with "
                    f"read access to the authority's host could have obtained "
                    f"the same certificate for the same subject; the leaf's own "
                    f"custody bounds it from below, and the chain bounds it "
                    f"from above")

    # (dd) validity is checked at use, on the same principle as standing. The
    # refusal vocabulary already reserves `certificate_outside_validity`; before
    # this, nothing produced it.
    not_after = parse_time(_mapping(doc.get("validity")).get("not_after"))
    if outcome == "trusted":
        if doc.get("state") == "expired":
            f.error("certificate-outside-validity-trusted",
                    f"{label}: recorded as trusted while the certificate's own "
                    f"state is 'expired'; validity is checked at USE, and the "
                    f"refusal this record owes is "
                    f"certificate_outside_validity")
        moments = {
            "trust_evaluation.evaluated_at": evaluation.get("evaluated_at"),
            "revocation_standing_check.checked_at":
                _mapping(evaluation.get("revocation_standing_check")).get(
                    "checked_at"),
        }
        for where, value in moments.items():
            moment = parse_time(value)
            if moment and not_after and moment > not_after:
                f.error("certificate-outside-validity-trusted",
                        f"{label}: recorded as trusted with {where} at {value}, "
                        f"after this certificate's own validity ended "
                        f"{_mapping(doc.get('validity')).get('not_after')}. "
                        f"Compared against the record's OWN moments rather than "
                        f"the wall clock, so the record stays a stable "
                        f"statement about a moment instead of a claim that "
                        f"decays")
                break

    # (x) standing is checked at use.
    if outcome == "trusted" and doc.get("state") == "revoked":
        f.error("revoked-certificate-trusted",
                f"{label}: recorded as trusted while the certificate's own "
                f"state is 'revoked'; standing is checked at USE, and validity "
                f"at issuance is not evidence of current standing")
    standing = _mapping(evaluation.get("revocation_standing_check"))
    if outcome == "trusted" and standing.get("performed_at_use") is not True:
        f.error("standing-not-checked-at-use",
                f"{label}: recorded as trusted with no standing check performed "
                f"at use")

    # (m)/(o) issuance evidence: admitted authority, and the honest absence.
    issuance = _mapping(doc.get("issuance_evidence"))
    if issuance.get("present") is True:
        ref = issuance.get("evidence_ref")
        evidence = ctx.issuances.get(ref) if _hashable(ref) else None
        if evidence is None:
            f.error("issuance-evidence-unresolved",
                    f"{label}: names issuance evidence {ref!r}, which does not "
                    f"resolve; an unresolvable evidence record is the same "
                    f"epistemic position as no record, and is refused rather "
                    f"than read as one")
        else:
            if evidence.get("authorization_state") == "unauthorized" \
                    and outcome == "trusted":
                f.error("issuance-unauthorized-trusted",
                        f"{label}: recorded as trusted while its issuance "
                        f"evidence {ref!r} is 'unauthorized'; the certificate's "
                        f"validity does not ratify an unauthorized issuance "
                        f"retroactively")
            if evidence.get("certificate_ref") != doc.get("certificate_id"):
                f.error("issuance-evidence-unresolved",
                        f"{label}: names issuance evidence {ref!r}, which is "
                        f"recorded against certificate "
                        f"{evidence.get('certificate_ref')!r}")
            issued = parse_time(evidence.get("issued_at"))
            not_before = parse_time(_mapping(doc.get("validity")).get("not_before"))
            not_after = parse_time(_mapping(doc.get("validity")).get("not_after"))
            if issued and not_after and issued > not_after:
                f.error("issuance-time-outside-validity",
                        f"{label}: issuance evidence records issuance at "
                        f"{evidence.get('issued_at')}, after this certificate's "
                        f"validity ends")
            if issued and not_before and issued < not_before - timedelta(days=1):
                f.warn("issuance-time-outside-validity",
                       f"{label}: issuance evidence records issuance at "
                       f"{evidence.get('issued_at')}, more than a day before "
                       f"the certificate's validity begins")
    elif issuance.get("present") is False and outcome == "trusted":
        f.error("issuance-evidence-absent-trusted",
                f"{label}: recorded as trusted while carrying no issuance "
                f"evidence. The question 'should this exist?' is answered "
                f"UNANSWERED, not yes, and the certificate is a revocation "
                f"candidate until the record is produced")

    # (ee, from the certificate's side) a supersession no renewal accounts for.
    # The renewal record being ABSENT is the same defect as a renewal declaring
    # `changed: false`, and it is the shape an adversarial probe reached for
    # second: the certificate says the key changed, no record owns the rebind
    # obligation that follows, and every dependent binding still points wherever
    # it pointed.
    generation = _mapping(doc.get("key_generation"))
    superseded_ref = generation.get("supersedes_generation_ref")
    if superseded_ref is not None and not ctx.supersession_accounted(
            doc.get("certificate_id"), generation.get("generation_ref"),
            superseded_ref):
        f.error("renewal-key-change-understated",
                f"{label}: declares generation "
                f"{generation.get('generation_ref')!r} superseding "
                f"{superseded_ref!r} while no renewal record in this corpus "
                f"accounts for that key change. A key change with no renewal "
                f"record is a rebind obligation with no owner, which is exactly "
                f"the silent failure this family exists to make loud")

    # (u) a record defect is closed by correcting the RECORD.
    enumeration = _mapping(doc.get("dependent_binding_enumeration"))
    enumerated = _hashable_set(enumeration.get("binding_refs"))
    for defect in _sequence(doc.get("record_defects")):
        if not isinstance(defect, dict):
            continue
        added = defect.get("added_binding_ref")
        if defect.get("resolution") == "record_corrected" and added not in enumerated:
            f.error("record-defect-not-closed-by-record-correction",
                    f"{label}: defect {defect.get('defect_id')!r} is resolved as "
                    f"'record_corrected' while the binding it names ({added!r}) "
                    f"is absent from the dependent enumeration; the incident is "
                    f"not closed by re-binding alone — the correction of THIS "
                    f"RECORD is what closes it")


# ----------------- rules (m)-(n), (ff), (gg): issuance evidence -----------------

def check_issuance_evidence(f: Findings, label: str, doc: dict,
                            ctx: Context) -> None:
    anchor_ref = doc.get("anchor_ref")
    anchor = ctx.anchors.get(anchor_ref) if _hashable(anchor_ref) else None
    authority = _mapping(doc.get("authority"))
    authority_ref = authority.get("authority_ref")
    if anchor is None:
        f.error("issuance-anchor-unresolved",
                f"{label}: anchor {anchor_ref!r} does not resolve, so whether "
                f"the anchor ADMITS the authority this issuance cites cannot be "
                f"checked; an issuance under an unknown anchor is refused rather "
                f"than passed over")
    else:
        admitted = {
            entry.get("authority_ref")
            for entry in _sequence(anchor.get("admitted_issuance_authorities"))
            if isinstance(entry, dict) and _hashable(entry.get("authority_ref"))
        }
        if authority_ref not in admitted:
            if doc.get("authorization_state") != "unauthorized":
                f.error("issuance-authority-not-admitted",
                        f"{label}: cites authority {authority_ref!r}, which "
                        f"anchor {anchor_ref!r} does not admit "
                        f"({sorted(admitted, key=repr)}), yet records "
                        f"authorization_state="
                        f"{doc.get('authorization_state')!r}. Authorization is "
                        f"DERIVED from the anchor's admitted set: an issuance "
                        f"with no admitted authority is recorded as "
                        f"unauthorized")
        elif doc.get("authorization_state") == "unauthorized":
            f.warn("issuance-authorization-understated",
                   f"{label}: records 'unauthorized' although anchor "
                   f"{anchor_ref!r} admits authority {authority_ref!r}; if the "
                   f"issuance was unauthorized for another reason, the record "
                   f"should say which")

    # (ff) OQ1's refused middle option, made mechanism. The ruling is explicit
    # that the declared floor exists for an authority the family does not
    # operate: "Reject the tempting middle option of writing the weaker form
    # into the requirement itself: that would let the self-hosted authority,
    # which can do better, stop at the floor." An issuance record that declares
    # the floor while recording the authority as family-operated IS that middle
    # option, arriving one record at a time.
    level = doc.get("establishment_level")
    if level == "per_policy_attestation_with_authority_log" and \
            _mapping(doc.get("issuing_authority")).get(
                "operated_by_family") is True:
        f.error("issuance-floor-under-a-family-operated-authority",
                f"{label}: records the DECLARED FLOOR (per-policy attestation "
                f"plus the authority's own log) while declaring "
                f"issuing_authority.operated_by_family: true. The floor is the "
                f"honest form for an authority whose internals the family "
                f"cannot read; an authority the family OPERATES can expose "
                f"per-certificate request provenance, and stopping at the floor "
                f"is the middle option the ratification refused")

    # (ff) a record may not assert a stronger level than the realization
    # declares it ACHIEVES. `achieved_establishment_level` is where a consumer
    # reads which form to expect, and a record above it makes the declaration a
    # decoration rather than a constraint.
    achieved = ctx.achieved_establishment_level(doc.get("realization_ref"))
    record_rank = ESTABLISHMENT_RANK.get(level)
    achieved_rank = ESTABLISHMENT_RANK.get(achieved)
    if record_rank is not None and achieved_rank is not None \
            and record_rank > achieved_rank:
        f.error("issuance-level-above-the-declared-achievement",
                f"{label}: records establishment level {level!r} while "
                f"realization {doc.get('realization_ref')!r} declares it "
                f"achieves {achieved!r}. A consumer reads the achieved level "
                f"from the declaration; a record claiming more than the "
                f"declaration supports is the gap being closed by the "
                f"realization asserting the evidence instead")

    # (n) the shortfall behind a floor-level record is declared, by this
    # realization, for this obligation, and in time.
    provenance = _mapping(doc.get("request_provenance"))
    if provenance.get("establishment") == "not_established":
        _shortfall_ok(f, label, ctx, provenance.get("declared_shortfall_ref"),
                      "TA-R2", doc.get("realization_ref"), doc.get("issued_at"),
                      "issuance evidence that does not establish provenance")
        if doc.get("establishment_level") == "per_certificate_record":
            f.error("provenance-asserted-unestablished",
                    f"{label}: declares the per-certificate establishment level "
                    f"while recording provenance as not established; the level "
                    f"IS the claim that the authority exposes per-certificate "
                    f"provenance")
    elif provenance.get("establishment") == "established" and \
            doc.get("establishment_level") == \
            "per_policy_attestation_with_authority_log":
        f.error("provenance-asserted-unestablished",
                f"{label}: declares the floor level — per-policy attestation "
                f"plus the authority's own log — while asserting per-certificate "
                f"request provenance. An asserted-but-unestablished record is "
                f"worse than a declared gap, which is why the floor level "
                f"cannot carry the claim it exists to replace")


# ------------------- rules (p)-(t), (ee): renewals -------------------

def check_renewal(f: Findings, label: str, doc: dict, ctx: Context) -> None:
    cert_ref = doc.get("certificate_ref")
    certificate = ctx.certificates.get(cert_ref) if _hashable(cert_ref) else None
    enumerated = _hashable_set(doc.get("enumerated_dependents"))
    rebinds = {entry.get("binding_ref"): entry
               for entry in _sequence(doc.get("dependent_rebinds"))
               if isinstance(entry, dict) and _hashable(entry.get("binding_ref"))}
    key_change = _mapping(doc.get("key_change"))

    if certificate is None:
        f.error("renewal-certificate-unresolved",
                f"{label}: certificate {cert_ref!r} does not resolve, so neither "
                f"the rebind set nor the key generations can be checked; a "
                f"renewal of an unknown certificate is refused rather than "
                f"passed over")
    else:
        enumeration = _mapping(certificate.get("dependent_binding_enumeration"))
        # (p) the rebind set is the CERTIFICATE's set.
        declared = _hashable_set(enumeration.get("binding_refs"))
        missing = sorted(declared - enumerated, key=repr)
        extra = sorted(enumerated - declared, key=repr)
        if missing:
            f.error("rebind-set-understated",
                    f"{label}: the certificate record enumerates dependents "
                    f"{missing} that this renewal does not, so the obligation is "
                    f"reported over a smaller set than exists. A renewal cannot "
                    f"reach 'complete' by enumerating fewer dependents than the "
                    f"record names")
        if extra:
            f.error("rebind-set-understated",
                    f"{label}: enumerates dependents {extra} the certificate "
                    f"record does not, so one of the two records is wrong about "
                    f"what depends on this key")
        # (r) planning against an incomplete record.
        planning = _mapping(doc.get("planning"))
        actual_state = enumeration.get("state")
        if _hashable(actual_state) and \
                planning.get("certificate_enumeration_state") != actual_state:
            f.error("renewal-planned-on-incomplete-record",
                    f"{label}: declares the certificate's dependent enumeration "
                    f"as {planning.get('certificate_enumeration_state')!r} while "
                    f"the record itself declares {actual_state!r}; a renewal "
                    f"planned against a record known to be incomplete is "
                    f"refused, and it cannot proceed by misdeclaring the state")
        # (s) key generations agree across records.
        generation = _mapping(certificate.get("key_generation"))
        current = generation.get("generation_ref")
        if key_change.get("changed") is True:
            if key_change.get("new_key_generation_ref") != current:
                f.error("renewal-generation-mismatch",
                        f"{label}: records new key generation "
                        f"{key_change.get('new_key_generation_ref')!r} while the "
                        f"certificate's current generation is {current!r}; the "
                        f"rebind comparison every dependent is held to reads the "
                        f"certificate's generation, so the two cannot disagree")
            superseded = generation.get("supersedes_generation_ref")
            if superseded is not None and \
                    key_change.get("superseded_key_generation_ref") != superseded:
                f.error("renewal-generation-mismatch",
                        f"{label}: records superseded generation "
                        f"{key_change.get('superseded_key_generation_ref')!r} "
                        f"while the certificate records {superseded!r}")
        # (ee) `changed` was a self-assertion nothing read. The schema binds
        # `arises` to it and forbids the generation fields when it is false — a
        # sound implication over an UNVERIFIED premise, so a renewal that did
        # change the key could declare it did not and owe no rebinds at all. The
        # certificate's own record is the witness: a superseded generation NO
        # renewal accounts for is a key change nobody recorded.
        superseded_ref = generation.get("supersedes_generation_ref")
        if key_change.get("changed") is False and superseded_ref is not None \
                and not ctx.supersession_accounted(cert_ref, current,
                                                   superseded_ref):
            f.error("renewal-key-change-understated",
                    f"{label}: records key_change.changed: false while "
                    f"certificate {cert_ref!r} declares generation {current!r} "
                    f"superseding {superseded_ref!r}, and no renewal record in "
                    f"this corpus accounts for that supersession. "
                    f"`changed: false` is what removes the rebind obligation "
                    f"entirely — the schema then FORBIDS the generation fields "
                    f"and forces the rebind list empty — so it is the one field "
                    f"a renewal has the strongest incentive to get wrong, and "
                    f"until now nothing read it")

    # (q) complete with an enumerated dependent that has no entry at all. The
    # schema already refuses an entry whose evidence is missing or failed; this
    # closes the case the schema cannot see.
    #
    # Guarded on the obligation ARISING, because a key-preserving renewal owes no
    # rebinds at all: the ratified text says the record states that explicitly and
    # that the absence of rebind evidence is not read as an omission. An unguarded
    # rule would read it as exactly that.
    arises = _mapping(doc.get("rebind_obligation")).get("arises") is True
    if arises and doc.get("completion_state") == "complete":
        for ref in sorted(enumerated, key=repr):
            entry = rebinds.get(ref)
            evidence = _mapping((entry or {}).get("rebind_evidence"))
            if entry is None or evidence.get("result") != "succeeded":
                f.error("renewal-complete-with-unevidenced-dependent",
                        f"{label}: reported complete while dependent {ref!r} "
                        f"carries no succeeded rebind evidence. A renewal that "
                        f"succeeds at the authority while a dependent still "
                        f"points at superseded material is a FAILURE OF THE "
                        f"ISSUING WORKFLOW, and silence is not evidence")

    # (t) a failed renewal names exactly the unbound dependents. Same guard: with
    # no obligation there are no rebinds to be unbound, and the schema already
    # forces the rebind list empty.
    if arises and doc.get("completion_state") == "failed":
        failure = _mapping(doc.get("failure"))
        named = _hashable_set(failure.get("unbound_dependents"))
        actual = {ref for ref in enumerated
                  if _mapping((rebinds.get(ref) or {}).get(
                      "rebind_evidence")).get("result") != "succeeded"}
        if named != actual:
            f.error("renewal-failure-misnames-dependents",
                    f"{label}: records unbound dependents "
                    f"{sorted(named, key=repr)} while the dependents lacking "
                    f"succeeded evidence are {sorted(actual, key=repr)}; "
                    f"attribution to the issuing workflow is only useful if the "
                    f"named set is the real one")

    # (s, second half) the dependent bindings' own rebind states must agree with
    # what this renewal reports about them.
    if key_change.get("changed") is True and certificate is not None:
        new_generation = key_change.get("new_key_generation_ref")
        for ref in sorted(enumerated, key=repr):
            binding = ctx.bindings.get(ref) if _hashable(ref) else None
            if binding is None:
                f.error("dependent-binding-unresolved",
                        f"{label}: enumerated dependent {ref!r} resolves to no "
                        f"binding record, so its rebind cannot be evidenced "
                        f"against anything")
                continue
            evidence = _mapping((rebinds.get(ref) or {}).get("rebind_evidence"))
            evidenced = evidence.get("result") == "succeeded"
            state = _mapping(binding.get("rebind_status")).get("state")
            bound = _mapping(binding.get("bound_key_reference")).get(
                "key_generation_ref")
            if evidenced and state != "rebound":
                f.error("dependent-rebind-state-contradicts-renewal",
                        f"{label}: reports dependent {ref!r} re-bound with "
                        f"evidence while the binding records state {state!r}")
            if evidenced and bound != new_generation:
                f.error("dependent-rebind-state-contradicts-renewal",
                        f"{label}: reports dependent {ref!r} re-bound while the "
                        f"binding still names generation {bound!r} rather than "
                        f"the new {new_generation!r}; a binding recorded as "
                        f"re-bound while pointing at superseded material is the "
                        f"silent failure this contract exists to make loud")
            if not evidenced and state == "rebound":
                f.error("dependent-rebind-state-contradicts-renewal",
                        f"{label}: dependent {ref!r} claims state 'rebound' "
                        f"while this renewal carries no succeeded evidence for "
                        f"it")


# -------------- rules (u)-(w), (ee): dependent bindings --------------

def check_dependent_binding(f: Findings, label: str, doc: dict,
                            ctx: Context) -> None:
    cert_ref = doc.get("certificate_ref")
    certificate = ctx.certificates.get(cert_ref) if _hashable(cert_ref) else None
    admission = _mapping(doc.get("admission"))
    refusal = _mapping(admission.get("refusal"))
    required = doc.get("required_assurance")
    if ctx.rank(required) is None:
        f.error("assurance-level-unknown",
                f"{label}: requires assurance {required!r}, which the registry's "
                f"ladder does not declare")

    if certificate is None:
        f.error("dependent-binding-certificate-unresolved",
                f"{label}: certificate {cert_ref!r} does not resolve, so neither "
                f"the ceiling that caps this binding nor the enumeration that "
                f"must name it can be checked")
        return

    # (ee) the generation this binding points at, compared against the
    # certificate's CURRENT generation — with no renewal record in the way. Rule
    # (s) made the same comparison only THROUGH a renewal, so a dependent left
    # behind by a renewal that was recorded as key-preserving, or never recorded
    # at all, was compared against nothing. `rebind_status` is the binding's own
    # claim about where it stands, and the certificate is the authority on where
    # "current" is.
    current_generation = _mapping(certificate.get("key_generation")).get(
        "generation_ref")
    bound_generation = _mapping(doc.get("bound_key_reference")).get(
        "key_generation_ref")
    rebind_state = _mapping(doc.get("rebind_status")).get("state")
    if current_generation is not None and bound_generation is not None:
        if rebind_state in ("current", "rebound") \
                and bound_generation != current_generation:
            f.error("dependent-binding-generation-mismatch",
                    f"{label}: records rebind_status {rebind_state!r} while "
                    f"binding generation {bound_generation!r}, which is not "
                    f"certificate {cert_ref!r}'s current generation "
                    f"({current_generation!r}). A binding claiming it is "
                    f"current or re-bound while naming superseded material is "
                    f"the silent failure this family exists to make loud — and "
                    f"it does not need a renewal record to be a contradiction")
        if rebind_state == "rebind_required" \
                and bound_generation == current_generation:
            f.error("dependent-binding-generation-mismatch",
                    f"{label}: records rebind_status 'rebind_required' while "
                    f"already bound to certificate {cert_ref!r}'s current "
                    f"generation ({current_generation!r}); an obligation that "
                    f"is already discharged reads as an open one, and the "
                    f"rebind set a renewal computes is then wrong in the other "
                    f"direction")

    # (u) every binding is enumerated against its certificate.
    enumeration = _mapping(certificate.get("dependent_binding_enumeration"))
    if doc.get("binding_id") not in _hashable_set(enumeration.get("binding_refs")):
        f.error("dependent-binding-unenumerated",
                f"{label}: certificate {cert_ref!r} does not enumerate this "
                f"binding. The rebind obligation is unenforceable against "
                f"bindings no record names, and the failure mode is silent "
                f"precisely because nothing was looking")

    # (u, second half) a dependent discovered by an outage is a record defect.
    if _mapping(doc.get("discovery")).get("discovered_by") == "authentication_failure":
        defects = [d for d in _sequence(certificate.get("record_defects"))
                   if isinstance(d, dict)
                   and d.get("added_binding_ref") == doc.get("binding_id")]
        if not defects:
            f.error("dependent-omission-unrecorded",
                    f"{label}: discovered by an authentication failure, and "
                    f"certificate {cert_ref!r} records no defect naming it. A "
                    f"dependent discovered only when it broke is a DEFECT OF "
                    f"THE CERTIFICATE RECORD, not merely an incident")

    # (v) the derived ceiling caps this binding, and the refusal names custody.
    ceiling = certificate.get("assurance_ceiling")
    ceiling_rank = ctx.rank(ceiling)
    required_rank = ctx.rank(required)
    if ceiling_rank is not None and required_rank is not None \
            and required_rank > ceiling_rank:
        if admission.get("state") != "refused":
            f.error("assurance-ceiling-exceeded",
                    f"{label}: requires assurance {required!r} while certificate "
                    f"{cert_ref!r} declares custody whose ceiling is "
                    f"{ceiling!r}, and the binding is recorded "
                    f"{admission.get('state')!r}. A certificate whose declared "
                    f"custody is host-held may not be presented for, or accepted "
                    f"for, an assurance requiring hardware-bound custody — and "
                    f"raising assurance is a custody change rather than a claim")
        elif refusal.get("ceiling_named") != ceiling:
            f.error("assurance-ceiling-exceeded",
                    f"{label}: refused for exceeding the ceiling but names "
                    f"{refusal.get('ceiling_named')!r} rather than the "
                    f"certificate's {ceiling!r}; the refusal names CUSTODY, and "
                    f"it has to name the right ceiling to do that")

    # (w) a declared gap is not permission to assert the evidence.
    realization = certificate.get("realization_ref")
    cannot = ctx.cannot_obligations(realization)
    blocked = sorted(_hashable_set(doc.get("required_obligations")) & cannot,
                     key=repr)
    if blocked:
        if admission.get("state") != "refused":
            f.error("declared-gap-claimed",
                    f"{label}: requires obligations {blocked} that realization "
                    f"{realization!r} declares it CANNOT satisfy, and the "
                    f"binding is recorded {admission.get('state')!r}. A consumer "
                    f"refuses the certificate for that use with the declared gap "
                    f"named; a declared gap is not permission to assert the "
                    f"missing evidence")
        else:
            resolved = ctx.obligation(refusal.get("gap_obligation_ref"))
            if resolved is None or resolved[1].get("obligation") not in blocked:
                f.error("declared-gap-claimed",
                        f"{label}: refused for a declared gap but names "
                        f"{refusal.get('gap_obligation_ref')!r}, which is not an "
                        f"entry declaring one of {blocked}")
    # (w, the partial case) A WARNING, not an error: R8's wording refuses what
    # the declaration "cannot support", and a partial obligation is partly
    # supported — the ratified consumer scenario is about the obligation the
    # realization declares it CANNOT satisfy. The report is the point-of-use cost
    # made visible, so a partial obligation is a fact a consumer weighed rather
    # than one it discovered later.
    partial = sorted(_hashable_set(doc.get("required_obligations"))
                     & ctx.obligations_declared(realization, "partial"),
                     key=repr)
    if partial and admission.get("state") != "refused":
        f.warn("declared-partial-required",
               f"{label}: requires obligations {partial} that realization "
               f"{realization!r} declares it satisfies only PARTIALLY, and the "
               f"binding is admitted. R8 permits this — partial is not cannot — "
               f"but the declaration's shortfall reaches this use, and a "
               f"consumer relying on the obligation should be relying on the "
               f"declaration's reason and compensating control rather than on "
               f"the obligation's name")
    if realization is not None and not _hashable(realization):
        return
    if realization is not None and realization not in ctx.declarations:
        f.error("realization-declaration-unresolved",
                f"{label}: certificate {cert_ref!r} names realization "
                f"{realization!r}, whose conformance declaration does not "
                f"resolve — so the obligations this binding depends on cannot be "
                f"read, and a consumer cannot refuse what it cannot read")


# ----------- rules (y)-(z), (gg): revocation propagation -----------

def check_revocation_propagation(f: Findings, label: str, doc: dict,
                                 ctx: Context) -> None:
    window = _mapping(doc.get("declared_window"))
    opens = parse_time(window.get("opens_at"))
    closes = parse_time(window.get("closes_at"))
    bounded = window.get("bounded_seconds")
    if opens and closes and isinstance(bounded, int):
        expected = opens + timedelta(seconds=bounded)
        if expected != closes:
            f.error("revocation-window-arithmetic",
                    f"{label}: declares a {bounded}s window opening "
                    f"{window.get('opens_at')} and closing "
                    f"{window.get('closes_at')}, which is not when it closes "
                    f"({expected.isoformat()}). The window is recomputed rather "
                    f"than trusted, on the same principle that makes `evidences` "
                    f"derived")

    authorities = _sequence(doc.get("downstream_authorities"))
    # (gg) evidence dated after the window closed does not evidence propagation
    # WITHIN it. The ratified obligation is "within a declared bounded window and
    # with the propagation evidenced" — a conjunction — and checking only that
    # evidence EXISTS let a record close the window on evidence gathered months
    # later and read `complete`.
    for authority in authorities:
        if not isinstance(authority, dict):
            continue
        evidence = _mapping(authority.get("propagation_evidence"))
        performed = parse_time(evidence.get("performed_at"))
        if performed and closes and performed > closes:
            f.error("propagation-evidenced-after-the-window",
                    f"{label}: authority {authority.get('authority_ref')!r} is "
                    f"recorded {authority.get('state')!r} on evidence performed "
                    f"{evidence.get('performed_at')}, after the declared window "
                    f"closed {window.get('closes_at')}. Evidence gathered after "
                    f"the window does not evidence propagation inside it; the "
                    f"honest record is an open exposure the window did not close")
    unevidenced = [a.get("authority_ref") for a in authorities
                   if isinstance(a, dict) and a.get("state") != "propagated"]
    assessed = parse_time(doc.get("assessed_at"))
    completion = _mapping(doc.get("completion"))
    if unevidenced and assessed and closes and assessed > closes:
        if completion.get("state") != "incomplete_open_exposure":
            f.error("revocation-window-closed-unevidenced",
                    f"{label}: the declared window closed {window.get('closes_at')} "
                    f"and at assessment {doc.get('assessed_at')} the authorities "
                    f"{sorted(unevidenced, key=repr)} carry no propagation "
                    f"evidence, yet completion is "
                    f"{completion.get('state')!r}. A revocation whose "
                    f"propagation cannot be evidenced within the declared window "
                    f"is escalated as an OPEN EXPOSURE rather than recorded as "
                    f"complete on the strength of the revocation request")

    revoked = _mapping(doc.get("revoked"))
    target_ref = revoked.get("target_ref")
    if revoked.get("target_kind") == "certificate":
        certificate = (ctx.certificates.get(target_ref)
                       if _hashable(target_ref) else None)
        if certificate is None:
            f.error("revocation-target-unresolved",
                    f"{label}: revokes certificate {target_ref!r}, which does "
                    f"not resolve; a propagation record over an unknown target "
                    f"cannot be checked against what that target supported")
        elif certificate.get("state") != "revoked":
            f.error("revocation-target-state-incoherent",
                    f"{label}: revokes certificate {target_ref!r} while that "
                    f"record's own state is {certificate.get('state')!r}")
        if certificate is not None:
            # (z, the certificate half) The closure for a CERTIFICATE target is
            # its own enumerated dependent bindings: those are, by construction,
            # the authorities this certificate supported. Computing the closure
            # only for anchor targets left the ORDINARY case — one certificate
            # revoked — resting on whatever the record chose to list, which is
            # the assertion this rule exists to replace. Refused bindings are
            # excluded: an authority that was never admitted was never
            # supported.
            reached = _hashable_set(
                [a.get("authority_ref") for a in authorities
                 if isinstance(a, dict)])
            owed: dict[str, str] = {}
            for ref in _hashable_set(
                    _mapping(certificate.get(
                        "dependent_binding_enumeration")).get("binding_refs")):
                binding = ctx.bindings.get(ref)
                if not isinstance(binding, dict):
                    continue
                if _mapping(binding.get("admission")).get("state") != "admitted":
                    continue
                authority_ref = _mapping(binding.get("binds")).get("authority_ref")
                if _hashable(authority_ref) and authority_ref is not None \
                        and authority_ref not in reached:
                    owed[str(authority_ref)] = str(ref)
            if owed:
                f.error("revocation-transitivity-incomplete",
                        f"{label}: revokes certificate {target_ref!r} without "
                        f"reaching "
                        f"{sorted(f'{a} (via {b})' for a, b in owed.items())}. "
                        f"Revoking a certificate revokes the authority THAT "
                        f"CERTIFICATE SUPPORTED, and the certificate's own "
                        f"dependent-binding enumeration is the record of what "
                        f"that was — an authority the propagation record does "
                        f"not name is a propagation gap, not a paperwork "
                        f"omission")
    elif revoked.get("target_kind") == "anchor":
        anchor = ctx.anchors.get(target_ref) if _hashable(target_ref) else None
        if anchor is None:
            f.error("revocation-target-unresolved",
                    f"{label}: revokes anchor {target_ref!r}, which does not "
                    f"resolve, so the transitive closure it owes cannot be "
                    f"computed")
        else:
            if anchor.get("state") != "revoked":
                f.error("revocation-target-state-incoherent",
                        f"{label}: revokes anchor {target_ref!r} while that "
                        f"record's own state is {anchor.get('state')!r}")
            # (z) revoking an anchor is transitive.
            lineage = ctx.anchor_lineage(target_ref)
            expected = {cid for cid, cert in ctx.certificates.items()
                        if cert.get("anchor_ref") in lineage}
            named = _hashable_set(doc.get("subordinate_certificates_reached"))
            missing = sorted(expected - named, key=repr)
            if missing:
                f.error("revocation-transitivity-incomplete",
                        f"{label}: revokes anchor {target_ref!r} without "
                        f"reaching {missing}, which chain to it or to an anchor "
                        f"beneath it. Revoking an anchor revokes transitively "
                        f"what its subordinate certificates supported; a "
                        f"certificate the record does not name is a propagation "
                        f"gap, not a paperwork omission")


# ------- rules (aa), (ff), (hh): the conformance declaration -------

def check_conformance_declaration(f: Findings, label: str, doc: dict) -> None:
    entries = _sequence(doc.get("obligations"))
    operated_by_family = _mapping(doc.get("realization")).get(
        "authority_operated_by_family")
    declared: dict[str, int] = {}
    cannot: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        obligation = entry.get("obligation")
        if not _hashable(obligation):
            continue
        declared[obligation] = declared.get(obligation, 0) + 1
        if entry.get("satisfaction") == "cannot":
            cannot.append(str(obligation))
        if obligation not in REQUIREMENTS:
            f.error("obligation-unknown",
                    f"{label}: declares obligation {obligation!r}, which is not "
                    f"one of this capability's obligations "
                    f"({sorted(REQUIREMENTS)})")
        # (ff) the same ruling as rule (n)'s citation check, at the place the
        # claim is MADE rather than where it is used. A realization that operates
        # the authority has nothing standing between it and a credential record
        # with a vault binding, so an R7 shortfall here is not a shortfall — it
        # is a declaration used as an exemption, which is the one thing the
        # declared-obligation rule must not become.
        if obligation == "TA-R7" and operated_by_family is True \
                and entry.get("satisfaction") in ("partial", "cannot"):
            f.error("family-operated-shortfall-claimed",
                    f"{label}: declares TA-R7 as "
                    f"{entry.get('satisfaction')!r} while recording "
                    f"authority_operated_by_family: true. Authority key "
                    f"material and issuance credentials sit at the strictest "
                    f"custody tier THE FAMILY OPERATES; where the family "
                    f"operates the authority, nothing prevents the credential "
                    f"record, so there is no shortfall to declare and the "
                    f"conformant answer is to produce it")
    for obligation, count in sorted(declared.items(), key=repr):
        if count > 1:
            f.error("obligation-declared-twice",
                    f"{label}: obligation {obligation!r} is declared {count} "
                    f"times; two entries for one obligation say nothing about "
                    f"which one a consumer is entitled to rely on")
    for obligation, statement in REQUIREMENTS.items():
        if obligation not in declared:
            f.error("obligation-coverage-incomplete",
                    f"{label}: obligation {obligation} ({statement}) carries no "
                    f"entry. An UNDECLARED shortfall is non-conformance even "
                    f"where the identical shortfall, declared, would be "
                    f"conformant, so the declaration is closed over all "
                    f"{len(REQUIREMENTS)} obligations")
    # (hh) the design's own named loophole risk: declare everything `cannot` and
    # stay conformant. The declaration is not refused for breadth — that is the
    # whole point of the honest-shortfall rule — but breadth is REPORTED, and it
    # meets a refusal at every point of use through rule (w) and the
    # now-mandatory `required_obligations` on every dependent binding.
    if len(cannot) > 1:
        f.warn("declaration-cannot-breadth",
               f"{label}: declares {len(cannot)} of {len(REQUIREMENTS)} "
               f"obligations as CANNOT ({sorted(cannot)}). Conformance by "
               f"declaration is the ratified arrangement and this is not "
               f"refused, but a realization declaring most of the capability "
               f"unmeetable is claiming very little, and every consuming "
               f"binding that requires one of these obligations must be "
               f"recorded as refused with the gap named")


# --------------------------- per-record validation ---------------------------

def validate_record(f: Findings, label: str, doc: Any, docs: dict[str, dict],
                    ctx: Context) -> None:
    if not isinstance(doc, dict):
        f.error("schema", f"{label}: document is not a mapping")
        return
    kind = doc.get("kind")
    if kind not in KIND_TO_SCHEMA:
        f.error("unknown-kind",
                f"{label}: kind {kind!r} is not a trust-anchor kind")
        return

    for error in sorted(validator_for(kind, docs).iter_errors(doc),
                        key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "<root>"
        f.error("schema", f"{label}: {where}: {error.message}")

    id_field = _ID_FIELDS.get(kind)
    rid = doc.get(id_field) if id_field else \
        _mapping(doc.get("realization")).get("realization_id")
    if isinstance(rid, str) and (kind, rid) in ctx.duplicate_ids:
        f.error("record-id-duplicate",
                f"{label}: identity {rid!r} is declared by more than one record "
                f"in this corpus; resolution through an id is last-write-wins, "
                f"so a duplicate could swap the anchor, custody or obligation "
                f"entry a reference resolves to — refused on every copy rather "
                f"than resolved by file order")

    # An obligation entry_id is the address a shortfall citation resolves
    # through, so it is an identity in exactly the same sense. The duplicates
    # were being recorded under the declaration's kind and looked up by
    # REALIZATION id, which cannot match — so two entries sharing an entry_id
    # went unreported, and a citation resolved to whichever the file order
    # happened to leave last.
    if kind == "xfactory_trust_anchor_conformance_declaration":
        shared = sorted(
            {entry.get("entry_id")
             for entry in _sequence(doc.get("obligations"))
             if isinstance(entry, dict)
             and _text(entry.get("entry_id")) in ctx.duplicate_entry_ids},
            key=repr)
        if shared:
            f.error("record-id-duplicate",
                    f"{label}: obligation entry id(s) {shared} are declared by "
                    f"more than one entry in this corpus. A citation names an "
                    f"entry_id, so a duplicate decides which shortfall a record "
                    f"is excused by through file order — and a record could "
                    f"then be covered by an entry recording `satisfied` while "
                    f"appearing to cite the one recording `cannot`")

    check_no_key_material(f, label, doc)

    if kind == "xfactory_trust_anchor_chain_custody_registry":
        check_custody_registry(f, label, doc, ctx)
    elif kind == "xfactory_trust_anchor":
        check_anchor(f, label, doc, ctx)
    elif kind == "xfactory_certificate_record":
        check_certificate(f, label, doc, ctx)
    elif kind == "xfactory_certificate_issuance_evidence":
        check_issuance_evidence(f, label, doc, ctx)
    elif kind == "xfactory_certificate_dependent_binding":
        check_dependent_binding(f, label, doc, ctx)
    elif kind == "xfactory_certificate_renewal_record":
        check_renewal(f, label, doc, ctx)
    elif kind == "xfactory_certificate_revocation_propagation":
        check_revocation_propagation(f, label, doc, ctx)
    elif kind == "xfactory_trust_anchor_conformance_declaration":
        check_conformance_declaration(f, label, doc)


# --------------------------- negative fixture headers ---------------------------

def expected_failure(path: Path) -> tuple[str, str | None, str]:
    """A negative fixture declares the finding CODE it exists to provoke, MAY
    pin it further with a substring, and MUST attribute itself to a requirement.

    The detail matters more here than in most families: many guarantees in this
    family are expressed IN THE SHAPE, so `schema` is satisfied by any schema
    error whatsoever and a fixture pinned only to it can be mutated into testing
    nothing while its self-test stays green. The requirement is what makes the
    corpus a negative confirmation PER REQUIREMENT rather than a pile of
    negatives.
    """
    code = detail = requirement = None
    for line in path.read_text(encoding="utf-8").splitlines():
        # Blank lines are allowed INSIDE the header block: a detail pin
        # separated by a blank line must not be silently dropped, because the
        # pin fails OPEN — the fixture keeps a green self-test with its
        # invariant pin gone, which is the precise drift the pin prevents.
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
    return sorted((FAMILY_DIR / "examples").glob("*.example.yaml"))


def negative_paths() -> list[Path]:
    return sorted((FAMILY_DIR / "examples" / "negative").glob("*.yaml"))


def self_test(f: Findings, docs: dict[str, dict], ctx: Context) -> None:
    positives = positive_paths()
    negatives = negative_paths()
    if not positives:
        f.error("examples-missing", "no packaged positive examples found")
    if not negatives:
        f.error("examples-missing", "no packaged negative fixtures found")

    # The canonical chain-custody registry is validated as a positive: it is the
    # closed set every other record resolves against.
    registry_label = str(CUSTODY_REGISTRY_PATH.relative_to(ROOT))
    validate_record(f, registry_label, ctx.registry, docs, ctx)
    if f.errors:
        f.note("the canonical chain-custody registry is validated first; every "
               "downstream ceiling and derivation resolves against it")

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
        canonical = ctx.canonical_registry
        local_ctx = Context(ctx.registry, {}, canonical)
        local_ctx.openxwallet = dict(ctx.openxwallet)
        local_ctx.copy_index_from(ctx)
        doc = load_yaml(path)
        if isinstance(doc, dict):
            local_ctx.index(doc)
        # A registry fixture replaces the closed set for its own adjudication;
        # otherwise a probe against the enumeration would be checked against the
        # canonical registry it is deliberately not. The CANONICAL identity is
        # carried across regardless, or rule (cc) would read the fixture as the
        # canonical registry and a probe against duplicate-id claims would have
        # nothing to fire on.
        if isinstance(doc, dict) and doc.get("kind") == \
                "xfactory_trust_anchor_chain_custody_registry":
            local_ctx = Context(doc, {}, canonical)
            local_ctx.openxwallet = dict(ctx.openxwallet)
            local_ctx.copy_index_from(ctx)
        validate_record(local, label, doc, docs, local_ctx)

        if not local.errors:
            f.error("negative-should-fail",
                    f"{label}: expected invalid, validated cleanly — the probe "
                    f"proves nothing")
        elif code not in codes_of(local.errors):
            f.error("negative-wrong-reason",
                    f"{label}: expected finding {code!r}, got "
                    f"{sorted(codes_of(local.errors))}")
        elif detail and not any(detail in line
                                for line in lines_for(local.errors, code)):
            f.error("negative-wrong-reason",
                    f"{label}: finding {code!r} fired but not for {detail!r} — "
                    f"the fixture no longer tests the invariant it is named "
                    f"for: {lines_for(local.errors, code)}")

    # Coverage closure: a negative confirmation PER REQUIREMENT.
    for requirement, statement in REQUIREMENTS.items():
        if requirement not in covered:
            f.error("negative-requirement-uncovered",
                    f"requirement {requirement} ({statement}) carries no "
                    f"negative confirmation; every requirement must have a "
                    f"recorded probe proving its check fails on the violation it "
                    f"exists to catch")
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
        # Exclude ANY packaged corpus, not only this checkout's: domain repos
        # pin and vendor openxFactory, so the normal consumption path scans a
        # COPY, and matching on this checkout's absolute paths would
        # re-adjudicate every vendored negative fixture as a live record.
        if "examples" in path.parts and "trust-anchor" in path.parts:
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

    # INDEX FIRST, then validate — otherwise every cross-record rule resolves
    # only against the packaged corpus and is inert on real artifacts, while
    # legitimate anchor/certificate pairs inside the scanned repo report
    # spurious unresolved-reference findings.
    #
    # Into a context of the SCANNED REPO'S OWN records plus the canonical
    # registries, never the packaged positives: a teaching fixture must not
    # resolve a live record's reference.
    repo_ctx = Context(ctx.registry, {}, ctx.canonical_registry)
    repo_ctx.openxwallet = dict(ctx.openxwallet)
    for _, doc in found:
        repo_ctx.index(doc)
    for path, doc in found:
        scanned += 1
        validate_record(f, str(path), doc, docs, repo_ctx)
    f.note(f"repo scan: {scanned} trust-anchor artifact(s) validated, "
           f"{skipped} document(s) skipped as another kind")


# --------------------------- orchestration ---------------------------

def report(f: Findings, strict: bool) -> int:
    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)
    print(f"\nvalidate-trust-anchor: {len(f.errors)} error(s), "
          f"{len(f.warnings)} warning(s)")
    return 1 if f.errors or (strict and f.warnings) else 0


# The ONE repetition of `verify-openxwallet-pin.REMEDIATION`, and it exists for
# the single case in which the canonical copy is unreachable: the verifier itself
# failed to load, so its constant cannot be read and an operator would otherwise
# get a refusal with no way out of it. Held byte-identical to the canonical
# string by `tests/trust-anchor/test_openxwallet_pin_refusal.py`, which is what
# keeps this from becoming the drifting third copy the design refused.
OPENXWALLET_REMEDIATION_FALLBACK = (
    "Remediation: run `git submodule update --init openXwallet` (NOT "
    "--recursive; this wave's init is deliberately scoped). If the pin itself "
    "is stale, follow `openXwallet/docs/pin-resync-runbook.md`.")


def load_openxwallet_pin_verifier():
    """Load `scripts/verify-openxwallet-pin.py` ON DEMAND, never at import.

    Lazy on purpose, and the laziness is the requirement rather than a
    style preference. This module is imported — not run — by
    `tests/trust-anchor/test_negative_corpus.py` and
    `test_declaration_perimeter.py`, and an import-scope load of the verifier
    would make every one of those tests uncollectable the moment the verifier
    were absent, unparseable, or raised while executing. The pin question belongs
    to the gate that asks it, so it is asked in `main()` and answered there.

    Loaded through `spec_from_file_location` because the verifier is a
    hyphenated script beside this one, not an importable module name — the same
    route this repo's own tests use to load these validators.
    """
    spec = importlib.util.spec_from_file_location(
        "verify_openxwallet_pin", OPENXWALLET_VERIFIER_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"{OPENXWALLET_VERIFIER_PATH} is not loadable as a "
                          f"module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def refuse_unless_openxwallet_pinned() -> str | None:
    """The refusal text if the openxWallet pin does not hold, else `None`.

    Replaces a bare `is_file()` on the custody registry, which asked only
    whether SOMETHING was at the path. Rule (f) composes this family's
    chain-custody set with the canonical openxWallet custody registry and checks
    against it at run time, which is why an unavailable parent set is fatal
    rather than skippable — and now that the parent set arrives across a gitlink,
    presence is no longer the whole question: an initialized submodule sitting on
    an unpinned commit is present, readable, and not the set anybody ratified.
    So the check is delegated to the verifier, which answers for the recorded
    gitlink, the checked-out revision and the eight digests, and refuses with a
    NAMED code.

    Every route out of here is closed: a verifier that will not load is a
    refusal, not a licence to fall back to "the file happens to be there". That
    fallback is precisely how a swapped submodule would validate green.
    """
    context = (
        f"ERROR the openxWallet pin does not hold, so rule (f) cannot run: this "
        f"family's chain-custody set COMPOSES with the canonical openxWallet "
        f"custody registry ({OPENXWALLET_REGISTRY_PATH.relative_to(ROOT)}) and "
        f"is checked against it at run time, so a parent set that is absent — or "
        f"present without being the one "
        f"{OPENXWALLET_PIN_PATH.relative_to(ROOT)} pins — is fatal rather than "
        f"skippable.")
    try:
        verifier = load_openxwallet_pin_verifier()
    except Exception as exc:  # noqa: BLE001
        return (f"{context}\nREFUSE openxwallet-pin-unverifiable: "
                f"{OPENXWALLET_VERIFIER_PATH.relative_to(ROOT)} could not be "
                f"loaded ({exc}), so the pin was never checked\n"
                f"{OPENXWALLET_REMEDIATION_FALLBACK}")
    try:
        verifier.verify(ROOT)
    except verifier.PinRefusal as exc:
        # `str(exc)` already renders `REFUSE <code>: <detail>` and the fixed
        # remediation trailer, so the context goes BEFORE it and the trailer
        # stays the last thing an operator reads.
        return f"{context}\n{exc}"
    except Exception as exc:  # noqa: BLE001
        return (f"{context}\nREFUSE openxwallet-pin-unverifiable: "
                f"{OPENXWALLET_VERIFIER_PATH.relative_to(ROOT)} failed while "
                f"checking the pin ({exc.__class__.__name__}: {exc})\n"
                f"{verifier.REMEDIATION}")
    return None


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=None,
                    help="repo checkout (or single file) to scan for real "
                         "trust-anchor artifacts; omit to self-test only")
    ap.add_argument("--strict", action="store_true",
                    help="treat warnings as errors")
    args = ap.parse_args()

    if not FAMILY_DIR.is_dir():
        print(f"ERROR {FAMILY_DIR} not found", file=sys.stderr)
        return 2
    refusal = refuse_unless_openxwallet_pinned()
    if refusal is not None:
        print(refusal, file=sys.stderr)
        return 2

    try:
        docs = load_schemas()
        registry = load_yaml(CUSTODY_REGISTRY_PATH)
        openxwallet_registry = load_yaml(OPENXWALLET_REGISTRY_PATH)
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

    ctx = Context(registry, openxwallet_registry)
    for path in positive_paths():
        doc = load_yaml(path)
        if isinstance(doc, dict):
            ctx.index(doc)
    f.note(f"chain custody composed with "
           f"{OPENXWALLET_REGISTRY_PATH.relative_to(ROOT)}: "
           f"{sorted(ctx.openxwallet)}")

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
