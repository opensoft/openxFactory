#!/usr/bin/env python3
"""Validate the consent-instrument contract family (add-consent-instrument).

The openxFactory-owned canonical validator for the three kinds
`xfactory_consent_instrument`, `xfactory_consent_instrument_class_registry`,
and `xfactory_consent_purpose_model` (`contracts/schemas/
consent-instrument.schema.yaml`, `consent-instrument-class-registry.schema.yaml`,
`consent-purpose-model.schema.yaml`). STANDALONE by ruling D8 — hostable where
no credential-contracts broker lives (the Medx constraint). Run from the pinned
openxFactory checkout, never copied into a domain repo:

    python3 scripts/validate-consent-instruments.py [REPO_PATH] [--strict]
        [--purpose PURPOSE]

Two layers run:

1. Packaged reference examples (`examples/consent-instrument/`): every
   `*.example.yaml` must pass schema conformance AND every cross-shape rule;
   every file under `negative/` must FAIL for its INTENDED finding, declared in
   the EXPECTED_NEGATIVE_FINDINGS table below (keyed by filename, optionally
   pinned by a detail substring — a finding CODE alone is too coarse where
   `schema` would be satisfied by any schema error at all). The self-test fails
   closed if a positive fails, a negative stops failing for its declared
   reason, or a negative on disk is missing from the table (and vice versa).
   Two purpose-resolution probes also run: one requested purpose that RESOLVES
   through the packaged purpose model and one that REFUSES.
2. Optional real artifacts under REPO_PATH: every `*.y*ml` whose `kind` is one
   of the three family kinds is validated; other kinds are skipped and counted.
   The packaged `examples/` tree is excluded — the negatives there are
   deliberately invalid and layer 1 already asserts exactly how. A registry or
   purpose model found in scope is the adjudication context for the
   instruments found beside it, matched by `domain`.

The rules the shapes cannot express:

  (a) CLASS MEMBERSHIP AND EVIDENCE DECLARATIONS (spec R3, ruling D2). An
      instrument's `instrument_class` must exist in its domain's CLOSED
      registry, and the class must declare BOTH `custody_anchor_kind` and
      `execution_evidence_kind`. The neutral contract never constrains WHICH
      classes a domain may have — only what a class declares. With no registry
      in scope for the instrument's domain, the check is skipped with a note
      (the registry is domain-owned and may live in the domain repo).
  (b) DECLARED-SKIP LIFECYCLE DISCIPLINE (spec R4, ruling D3). Under a class
      declaring `signature_phase: true`, an instrument at `executed` or beyond
      must show `pending_signatures` in its `status_history` — a class may
      skip the signature phase only when its class declaration says so
      (`portal_acceptance`), never silently.
  (c) ALIAS DISCIPLINE (spec R4, ruling D3). A registry `status_aliases` entry
      maps a DOMAIN spelling onto the closed neutral enum (Ledgerx `active`
      -> `executed`); an alias whose key is itself a neutral spelling remaps
      the enum and is refused, as is an alias targeting a non-neutral value.
  (d) CUSTODY IS A POINTER, NOT A PAYLOAD (spec R9, ruling D9). Custody
      carries `locator` + `sha256` and nothing else: any other custody
      property, a malformed sha256, or a blob-shaped custody value (a long
      base64 run, a data: URI, PDF magic, an embedded multi-line body) is the
      signed original entering a product repo.
  (e) PURPOSE RESOLUTION (spec R7, ruling D4). Every `scope.purposes` entry
      must resolve in the domain's declared purpose model — direct membership
      or a `resolves_to` chain — and the finding names the missing link. The
      `--purpose` flag additionally checks ONE requested purpose against each
      instrument in the scanned scope: covered when it appears in (or resolves
      through) the record's purposes under the model.
  (f) TERMINATION CASCADE EVIDENCE (spec R8, ruling D5). A `terminated`
      instrument must carry `cascade_evidence` on EVERY declared dependent
      reference — the evidence obligation under the record's revocation SLA.
      Cascade MECHANICS stay in the owning contract families.
  (g) DATA-CONSENT MAPPING COHERENCE (spec R10, ruling D1). `mapping:
      consent_profile` requires the derived profile to be declared as a
      consent_profile dependent reference (the Medx derivation pattern);
      `mapping: none` must not coexist with one.

WHAT THIS VALIDATOR DELIBERATELY DOES NOT DO (ruling D4; spec R7 scenario
"One enforcement truth per concern"): it NEVER inspects the technical access
shape inside a delegation clause. Permission strings, constraints, read-only
limits, and verification evidence are credential-contracts enforcement — a
clause's `access` block is carried free-shape and passed over untouched, so a
disagreement between a clause and a credential grant is a credential-contracts
finding, not a consent-instrument finding.

Exit codes: 0 ok, 1 findings, 2 dependency/harness error.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Iterator

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
SCHEMA_DIR = ROOT / "contracts" / "schemas"
EXAMPLES_DIR = ROOT / "examples" / "consent-instrument"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"

KIND_TO_SCHEMA = {
    "xfactory_consent_instrument": "consent-instrument.schema.yaml",
    "xfactory_consent_instrument_class_registry":
        "consent-instrument-class-registry.schema.yaml",
    "xfactory_consent_purpose_model": "consent-purpose-model.schema.yaml",
}

# date/date-time enforced, not merely annotated. jsonschema only registers the
# date-time checker when rfc3339-validator is importable, so a bare
# environment would silently accept malformed timestamps — fail closed
# instead of validating vacuously.
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

NEUTRAL_STATUSES = ("draft", "pending_signatures", "executed", "amended",
                    "terminated", "withdrawn")
# States that lie past the signature phase: an instrument here under a
# signature_phase-true class must show pending_signatures in its trace.
# `withdrawn` belongs here because an instrument can only be withdrawn AFTER
# execution, so the lifecycle-skip discipline must reach it.
PAST_SIGNATURE_STATUSES = {"executed", "amended", "terminated", "withdrawn"}
# The two TERMINAL states. Both raise the cascade obligation, because
# withdrawal by the consenting party and termination are distinct events with
# the same consequence for everything the instrument authorized.
ENDED_STATUSES = ("terminated", "withdrawn")
EVIDENCE_KIND_FIELDS = ("custody_anchor_kind", "execution_evidence_kind")

ALLOWED_CUSTODY_KEYS = {"locator", "sha256"}
SHA256_RX = re.compile(r"^[0-9a-f]{64}$")
# Rule (d), value side: shapes an embedded signed original takes. A long
# base64 run is a document body; `data:` is an inline payload URI; JVBERi/
# %PDF- are the PDF magic in and out of base64. An opaque LOCATOR is short
# and single-line by nature, so none of these fire on conformant custody.
BASE64_BLOB_RX = re.compile(r"[A-Za-z0-9+/=]{200,}")
PDF_MAGIC_RX = re.compile(r"JVBERi|%PDF-")

# Layer-1 negative corpus: filename -> (expected finding code, optional
# detail substring). The detail pins fixtures whose code alone is too coarse:
# `schema` is satisfied by ANY schema error, so amendment-as-child-instrument
# must fail on `parent_ref` specifically or it no longer tests ruling D7.
EXPECTED_NEGATIVE_FINDINGS: dict[str, tuple[str, str | None]] = {
    "embedded-original-content.yaml": ("embedded-original-content", None),
    "undeclared-lifecycle-skip.yaml": ("undeclared-lifecycle-skip", None),
    "class-without-evidence-kind.yaml": ("class-without-evidence-kind", None),
    "amendment-as-child-instrument.yaml": ("schema", "parent_ref"),
    "purpose-unresolvable.yaml": ("purpose-unresolvable", "crypto-custody"),
    # add-client-identity-roster: the same half-cascade on BOTH terminal
    # events. The detail pins the EVENT, because the code alone cannot tell
    # the pair apart and the pair is the whole point — an obligation that
    # fired only on termination would leave withdrawal unguarded.
    "identity-cascade-incomplete-on-terminated.yaml":
        ("identity-cascade-incomplete", "a terminated instrument"),
    "identity-cascade-incomplete-on-withdrawn.yaml":
        ("identity-cascade-incomplete", "a withdrawn instrument"),
}

# Self-test purpose probes (spec R7 scenario "Purpose resolution passes and
# fails mechanically"): (instrument example, requested purpose, must_resolve).
PURPOSE_PROBES = [
    ("consent-instrument-engagement-letter.example.yaml",
     "reconcile-bank-feeds", True),
    ("consent-instrument-engagement-letter.example.yaml",
     "payroll-support", False),
]


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


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# --------------------------- schema loading ---------------------------

def load_schemas() -> dict[str, dict]:
    """One schema document per family kind. No cross-file `$ref`s exist in
    this family, so plain per-document validators suffice — a consumer's
    stock Draft 2020-12 validator resolves each schema identically."""
    docs: dict[str, dict] = {}
    for name in set(KIND_TO_SCHEMA.values()):
        docs[name] = load_yaml(SCHEMA_DIR / name)
    return docs


def validator_for(kind: str, docs: dict[str, dict]) -> Draft202012Validator:
    return Draft202012Validator(
        docs[KIND_TO_SCHEMA[kind]], format_checker=FORMAT_CHECKER)


# --------------------------- adjudication context ---------------------------

# Sentinel distinguishing "several documents claim this domain" from "none in
# scope" — both skip the domain-owned checks, but the operator remedy differs
# (dedupe the registries/models vs scan them alongside the instruments).
AMBIGUOUS: dict = {}


class Context:
    """The domain-owned adjudication documents in scope: class registries and
    purpose models, keyed by `domain`. An instrument is checked against ITS
    domain's documents only; a domain with several registries (or models) in
    one scope is ambiguous, so those checks fall back to a note."""

    def __init__(self) -> None:
        self.registries: dict[str, dict | None] = {}
        self.purpose_models: dict[str, dict | None] = {}

    @staticmethod
    def _add(store: dict[str, dict | None], domain: Any, doc: dict) -> None:
        if not isinstance(domain, str):
            return
        store[domain] = AMBIGUOUS if domain in store else doc

    def add(self, doc: dict) -> None:
        if doc.get("kind") == "xfactory_consent_instrument_class_registry":
            self._add(self.registries, doc.get("domain"), doc)
        elif doc.get("kind") == "xfactory_consent_purpose_model":
            self._add(self.purpose_models, doc.get("domain"), doc)


def model_map(model: dict) -> dict[str, str | None]:
    """purpose name -> resolves_to (or None for a root purpose). A non-string
    resolves_to is stored as None so a schema-invalid model surfaces as its
    schema finding instead of a TypeError inside resolve_purpose()."""
    out: dict[str, str | None] = {}
    for entry in model.get("purposes") or []:
        if isinstance(entry, dict) and isinstance(entry.get("purpose"), str):
            target = entry.get("resolves_to")
            out[entry["purpose"]] = target if isinstance(target, str) else None
    return out


def resolve_purpose(requested: str, record_purposes: set[str],
                    links: dict[str, str | None]) -> bool:
    """Spec R7: the requested purpose appears in (or resolves through) the
    record's purposes under the domain purpose model. Walk the resolves_to
    chain with a visited set so a cyclic model cannot hang the check."""
    seen: set[str] = set()
    cur: str | None = requested
    while cur is not None and cur not in seen:
        if cur in record_purposes:
            return True
        seen.add(cur)
        cur = links.get(cur)
    return False


# --------------------------- rule (a)/(b): class + declared skip ---------------------------

def check_class(f: Findings, label: str, doc: dict, registry: dict | None) -> None:
    domain = doc.get("domain")
    cls_name = doc.get("instrument_class")
    if registry is AMBIGUOUS:
        f.note(f"several instrument-class registries claim domain {domain!r} "
               f"in this scope: class-membership and declared-skip checks "
               f"skipped — deduplicate the registries so exactly one owns "
               f"the domain (D2)")
        return
    if registry is None:
        f.note(f"no instrument-class registry in scope for domain {domain!r}: "
               f"class-membership and declared-skip checks skipped — the "
               f"registry is domain-owned (D2) and may live in the domain "
               f"repo; scan it alongside the instruments to check declared "
               f"facts")
        return
    classes = {c.get("name"): c for c in registry.get("classes") or []
               if isinstance(c, dict)}
    cls = classes.get(cls_name)
    if cls is None:
        f.error("unknown-instrument-class",
                f"{label}: instrument_class {cls_name!r} is not in the "
                f"{domain!r} registry's CLOSED class list "
                f"({sorted(k for k in classes if isinstance(k, str))}) — the "
                f"domain owns the vocabulary, and the registry is closed over "
                f"it (spec R3, D2)")
        return
    missing = [k for k in EVIDENCE_KIND_FIELDS if not cls.get(k)]
    if missing:
        f.error("class-without-evidence-kind",
                f"{label}: instrument_class {cls_name!r} declares no "
                f"{' or '.join(missing)} in the {domain!r} registry — a class "
                f"without both evidence declarations is refused (spec R3)")
    if cls.get("signature_phase") is True and \
            doc.get("status") in PAST_SIGNATURE_STATUSES:
        history = [e.get("status") for e in doc.get("status_history") or []
                   if isinstance(e, dict)]
        if "pending_signatures" not in history:
            f.error("undeclared-lifecycle-skip",
                    f"{label}: status {doc.get('status')!r} under class "
                    f"{cls_name!r}, which declares signature_phase true, with "
                    f"no pending_signatures in status_history — a class may "
                    f"skip the signature phase only when its class declaration "
                    f"says so; skipping is class-appropriate, never silent "
                    f"(spec R4, D3)")


# --------------------------- rule (c): registry discipline ---------------------------

def check_registry(f: Findings, label: str, doc: dict) -> None:
    """Runs on the registry REGARDLESS of schema outcome, so a registry
    negative fails for the invariant it is named for, not merely for the
    first required-property slip."""
    seen: set[str] = set()
    for i, cls in enumerate(doc.get("classes") or []):
        if not isinstance(cls, dict):
            continue
        name = cls.get("name") if isinstance(cls.get("name"), str) \
            else f"classes[{i}]"
        if name in seen:
            f.error("duplicate-class",
                    f"{label}: class {name!r} appears more than once — the "
                    f"registry is the domain's single CLOSED vocabulary "
                    f"(spec R3, D2)")
        seen.add(name)
        missing = [k for k in EVIDENCE_KIND_FIELDS if not cls.get(k)]
        if missing:
            f.error("class-without-evidence-kind",
                    f"{label}: class {name!r} omits {' and '.join(missing)} — "
                    f"every class declares BOTH its custody-anchor kind and "
                    f"its execution-evidence kind (spec R3 scenario 'A class "
                    f"without evidence declaration is refused')")
        if "signature_phase" not in cls:
            f.error("signature-phase-undeclared",
                    f"{label}: class {name!r} does not declare "
                    f"signature_phase — the D3 lifecycle skip is "
                    f"class-DECLARED, never implicit (spec R4)")
        aliases = cls.get("status_aliases")
        if isinstance(aliases, dict):
            for key, value in aliases.items():
                if key in NEUTRAL_STATUSES:
                    f.error("alias-remaps-neutral-status",
                            f"{label}: class {name!r} aliases neutral status "
                            f"{key!r} — aliases map DOMAIN spellings onto the "
                            f"closed enum, never remap the enum itself "
                            f"(spec R4, D3)")
                if value not in NEUTRAL_STATUSES:
                    f.error("alias-target-not-neutral",
                            f"{label}: class {name!r} alias {key!r} -> "
                            f"{value!r} does not target the closed six-state "
                            f"enum (spec R4, D3)")


# --------------------------- rule (d): custody ---------------------------

def walk_strings(node: Any, path: str) -> Iterator[tuple[str, str]]:
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


def check_custody(f: Findings, label: str, doc: dict) -> None:
    custody = doc.get("custody")
    if not isinstance(custody, dict):
        return  # shape failure; the schema layer reports it
    for key in custody:
        if key not in ALLOWED_CUSTODY_KEYS:
            f.error("embedded-original-content",
                    f"{label}: custody.{key}: custody carries {key!r} beyond "
                    f"locator + sha256 — the signed original is referenced by "
                    f"opaque locator + sha256 and NEVER embedded; there is no "
                    f"property its content may occupy (spec R9, D9)")
    sha = custody.get("sha256")
    if isinstance(sha, str) and not SHA256_RX.fullmatch(sha):
        f.error("custody-sha256-malformed",
                f"{label}: custody.sha256 {sha!r} is not 64 lowercase hex "
                f"characters — the digest is the half of the custody pair "
                f"that proves the pointed-at original (spec R9)")
    for loc, value in walk_strings(custody, "custody"):
        if loc == "custody.sha256":
            continue  # a digest is the one long opaque value custody DOES carry
        blob = []
        if BASE64_BLOB_RX.search(value):
            blob.append("a base64-alphabet run of 200+ characters")
        if value.startswith("data:"):
            blob.append("a data: payload URI")
        if PDF_MAGIC_RX.search(value):
            blob.append("PDF magic (raw or base64)")
        if "\n" in value:
            blob.append("an embedded multi-line body")
        if blob:
            f.error("embedded-original-content",
                    f"{label}: {loc}: value carries {', '.join(blob)} — "
                    f"custody is a pointer, not a payload; original content "
                    f"in a product repo is nonconformant wherever it hides "
                    f"(spec R9, D9)")


# --------------------------- rule (e): purpose resolution ---------------------------

def check_purposes(f: Findings, label: str, doc: dict, model: dict | None) -> None:
    domain = doc.get("domain")
    purposes = (doc.get("scope") or {}).get("purposes") \
        if isinstance(doc.get("scope"), dict) else None
    if not isinstance(purposes, list):
        return  # shape failure; the schema layer reports it
    if model is AMBIGUOUS:
        f.note(f"several consent purpose models claim domain {domain!r} in "
               f"this scope: purpose-resolution checks skipped — deduplicate "
               f"the models so exactly one owns the domain (D4)")
        return
    if model is None:
        f.note(f"no consent purpose model in scope for domain {domain!r}: "
               f"purpose-resolution checks skipped — the model is "
               f"domain-declared (D4) and may live in the domain repo; scan "
               f"it alongside the instruments to check resolution")
        return
    links = model_map(model)
    for purpose in purposes:
        if isinstance(purpose, str) and purpose not in links:
            f.error("purpose-unresolvable",
                    f"{label}: scope.purposes entry {purpose!r} is absent "
                    f"from the {domain!r} purpose model and resolves through "
                    f"no chain — the missing link is {purpose!r} (spec R7, "
                    f"D4)")


def check_requested_purpose(f: Findings, label: str, doc: dict,
                            model: dict | None, requested: str) -> None:
    purposes = (doc.get("scope") or {}).get("purposes") \
        if isinstance(doc.get("scope"), dict) else None
    if not isinstance(purposes, list):
        return
    if model is None or model is AMBIGUOUS:
        why = ("several purpose models claim" if model is AMBIGUOUS
               else "no purpose model in scope for")
        f.error("purpose-not-covered",
                f"{label}: requested purpose {requested!r} cannot be "
                f"adjudicated — {why} domain "
                f"{doc.get('domain')!r} (spec R7)")
        return
    record_purposes = {p for p in purposes if isinstance(p, str)}
    if resolve_purpose(requested, record_purposes, model_map(model)):
        f.note(f"{label}: requested purpose {requested!r} resolves into the "
               f"record's purposes under the {doc.get('domain')!r} model")
    else:
        f.error("purpose-not-covered",
                f"{label}: requested purpose {requested!r} neither appears in "
                f"nor resolves through the record's purposes "
                f"({sorted(record_purposes)}) under the "
                f"{doc.get('domain')!r} purpose model (spec R7, D4)")


def check_purpose_model(f: Findings, label: str, doc: dict) -> None:
    names = [e.get("purpose") for e in doc.get("purposes") or []
             if isinstance(e, dict)]
    seen: set[str] = set()
    for name in names:
        if isinstance(name, str):
            if name in seen:
                f.error("duplicate-purpose",
                        f"{label}: purpose {name!r} is declared more than "
                        f"once — the model is a single declared vocabulary "
                        f"(spec R7)")
            seen.add(name)
    for entry in doc.get("purposes") or []:
        if not isinstance(entry, dict):
            continue
        target = entry.get("resolves_to")
        if target is None:
            continue
        if target == entry.get("purpose") or target not in seen:
            f.error("purpose-model-dangling-link",
                    f"{label}: purpose {entry.get('purpose')!r} resolves_to "
                    f"{target!r}, which is "
                    f"{'itself' if target == entry.get('purpose') else 'not a purpose in this model'}"
                    f" — every chain link must land on a declared purpose "
                    f"(spec R7, D4)")


# --------------------------- rule (f): termination cascade ---------------------------

IDENTITY_CASCADE_EVIDENCE = ("identity_removal_evidence",
                             "admission_withdrawal_evidence")


def check_termination_cascade(f: Findings, label: str, doc: dict) -> None:
    """The cascade obligation, on BOTH terminal events.

    `termination-without-cascade-evidence` keeps its CODE SPELLING for
    continuity, but its REACH is wider than it was: it now fires on a withdrawn
    instrument as well as a terminated one. That is a change in meaning, stated
    rather than glossed — withdrawal by the consenting party and termination
    are distinct events, and the ratified cascade runs from either.
    """
    status = doc.get("status")
    if status not in ENDED_STATUSES:
        return
    for i, ref in enumerate(doc.get("dependent_refs") or []):
        if not isinstance(ref, dict):
            continue
        if not ref.get("cascade_evidence"):
            f.error("termination-without-cascade-evidence",
                    f"{label}: dependent_refs[{i}] ({ref.get('kind')} "
                    f"{ref.get('ref')!r}) carries no cascade_evidence on a "
                    f"{status} instrument — every declared dependent "
                    f"reference falls due under the record's revocation SLA "
                    f"with an evidence obligation; the mechanics stay in the "
                    f"owning families (spec R8, D5)")
        if ref.get("kind") != "governed_identity":
            continue
        # A STANDING IDENTITY in another party's tenant is held by two keys,
        # so its cascade needs two pieces of evidence. Revoking the credential
        # and stopping there leaves the identity in place with its admission
        # intact — the half-cascade this obligation exists to refuse. The
        # finding lands against the INSTRUMENT, which is the record that
        # carries the obligation; the identity is named, never blamed.
        absent = [k for k in IDENTITY_CASCADE_EVIDENCE if not ref.get(k)]
        if absent:
            f.error("identity-cascade-incomplete",
                    f"{label}: dependent_refs[{i}] is a governed_identity "
                    f"({ref.get('ref')!r}) on a {status} instrument and "
                    f"declares no {' or '.join(absent)}. A governed identity "
                    f"falls due on withdrawal exactly as on termination, and "
                    f"its cascade is complete only when BOTH the identity's "
                    f"removal and the withdrawal of its admission act are "
                    f"evidenced — credential revocation alone leaves standing "
                    f"access in the client's tenant (spec R8, D5)")


# --------------------------- rule (g): data-consent coherence ---------------------------

def check_data_consent(f: Findings, label: str, doc: dict) -> None:
    dc = doc.get("data_consent")
    if not isinstance(dc, dict):
        f.error("data-consent-undeclared",
                f"{label}: no data_consent block — an instrument declares its "
                f"consent-profile mapping or declares `mapping: none` "
                f"explicitly; silent omission is nonconformant (spec R10, D1)")
        return
    profile_refs = [r.get("ref") for r in doc.get("dependent_refs") or []
                    if isinstance(r, dict) and r.get("kind") == "consent_profile"]
    mapping = dc.get("mapping")
    if mapping == "consent_profile":
        if dc.get("profile_ref") not in profile_refs:
            f.error("data-consent-mapping-incoherent",
                    f"{label}: data_consent maps to profile "
                    f"{dc.get('profile_ref')!r} but the derived profile is "
                    f"not declared as a consent_profile dependent reference — "
                    f"the instrument declares the derived profile as a "
                    f"dependent reference with its derivation basis (spec R10 "
                    f"scenario 'The Medx derivation is the reference', D1/D5)")
    elif mapping == "none" and profile_refs:
        f.error("data-consent-mapping-incoherent",
                f"{label}: data_consent declares `mapping: none` yet "
                f"consent_profile dependent reference(s) "
                f"{sorted(r for r in profile_refs if isinstance(r, str))} are "
                f"declared — an instrument with no data-consent implication "
                f"carries no derived profile (spec R10)")


# --------------------------- per-record validation ---------------------------

def validate_record(f: Findings, label: str, doc: Any,
                    docs: dict[str, dict], ctx: Context) -> None:
    if not isinstance(doc, dict):
        f.error("shape", f"{label}: document is not a mapping")
        return
    kind = doc.get("kind")
    if kind not in KIND_TO_SCHEMA:
        f.error("unknown-kind",
                f"{label}: kind {kind!r} is not a consent-instrument family kind")
        return
    for err in sorted(validator_for(kind, docs).iter_errors(doc),
                      key=lambda e: list(e.absolute_path)):
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        f.error("schema", f"{label}: {loc}: {err.message}")
    # The cross-shape rules run REGARDLESS of schema outcome: a negative
    # fixture must fail for the rule it names, not merely for the first
    # schema slip.
    domain = doc.get("domain") if isinstance(doc.get("domain"), str) else None
    if kind == "xfactory_consent_instrument":
        check_class(f, label, doc, ctx.registries.get(domain))
        check_custody(f, label, doc)
        check_purposes(f, label, doc, ctx.purpose_models.get(domain))
        check_termination_cascade(f, label, doc)
        check_data_consent(f, label, doc)
    elif kind == "xfactory_consent_instrument_class_registry":
        check_registry(f, label, doc)
    elif kind == "xfactory_consent_purpose_model":
        check_purpose_model(f, label, doc)


# --------------------------- layer 1: packaged examples ---------------------------

def codes_of(findings: list[str]) -> set[str]:
    return {m.group(1) for m in
            (re.match(r"ERROR \[([^]]+)]", line) for line in findings) if m}


def lines_for(findings: list[str], code: str) -> list[str]:
    return [line for line in findings if line.startswith(f"ERROR [{code}]")]


def packaged_context(f: Findings) -> Context:
    """The packaged registry and purpose model are the adjudication context
    for the whole self-test — rules (a), (b), and (e) check declared facts,
    never a naming heuristic."""
    ctx = Context()
    for name in ("consent-instrument-class-registry.example.yaml",
                 "consent-purpose-model.example.yaml"):
        path = EXAMPLES_DIR / name
        if path.is_file():
            doc = load_yaml(path)
            if isinstance(doc, dict):
                ctx.add(doc)
        else:
            f.error("examples-missing",
                    f"no packaged {name}: the self-test cannot exercise its "
                    f"registry/purpose cross-checks")
    return ctx


def self_test(f: Findings, docs: dict[str, dict]) -> None:
    if not EXAMPLES_DIR.is_dir():
        f.error("examples-missing", f"{EXAMPLES_DIR} not found")
        return
    ctx = packaged_context(f)

    valid_ok = 0
    for path in sorted(EXAMPLES_DIR.glob("*.example.yaml")):
        local = Findings()
        validate_record(local, f"examples/{path.name}", load_yaml(path),
                        docs, ctx)
        if local.errors:
            f.errors.extend(f"{line} [expected a valid example]"
                            for line in local.errors)
        else:
            valid_ok += 1
        f.warnings.extend(local.warnings)

    neg_ok = 0
    if not NEGATIVE_DIR.is_dir():
        f.error("examples-missing", f"{NEGATIVE_DIR} not found")
    else:
        on_disk = {p.name for p in NEGATIVE_DIR.glob("*.yaml")}
        for name in sorted(EXPECTED_NEGATIVE_FINDINGS.keys() - on_disk):
            f.error("negative-missing",
                    f"negative/{name} is declared in "
                    f"EXPECTED_NEGATIVE_FINDINGS but absent on disk")
        for path in sorted(NEGATIVE_DIR.glob("*.yaml")):
            expected = EXPECTED_NEGATIVE_FINDINGS.get(path.name)
            if expected is None:
                f.error("negative-unregistered",
                        f"negative/{path.name} has no entry in "
                        f"EXPECTED_NEGATIVE_FINDINGS — every negative "
                        f"declares the finding it exists to provoke")
                continue
            code, detail = expected
            local = Findings()
            validate_record(local, f"examples/negative/{path.name}",
                            load_yaml(path), docs, ctx)
            if not local.errors:
                f.error("negative-should-fail",
                        f"negative/{path.name}: expected invalid, validated "
                        f"cleanly")
            elif code not in codes_of(local.errors):
                f.error("negative-wrong-reason",
                        f"negative/{path.name}: expected finding {code!r}, "
                        f"got {sorted(codes_of(local.errors))}")
            elif detail and not any(detail in line
                                    for line in lines_for(local.errors, code)):
                f.error("negative-wrong-reason",
                        f"negative/{path.name}: finding {code!r} fired but "
                        f"not for {detail!r} — the fixture no longer tests "
                        f"the invariant it is named for: "
                        f"{lines_for(local.errors, code)}")
            else:
                neg_ok += 1

    probe_ok = 0
    for example, requested, must_resolve in PURPOSE_PROBES:
        path = EXAMPLES_DIR / example
        if not path.is_file():
            f.error("examples-missing", f"purpose probe target {example} not found")
            continue
        doc = load_yaml(path)
        local = Findings()
        check_requested_purpose(local, f"examples/{example}", doc,
                                ctx.purpose_models.get(doc.get("domain")),
                                requested)
        resolved = not local.errors
        if resolved == must_resolve:
            probe_ok += 1
        else:
            f.error("purpose-probe",
                    f"examples/{example}: requested purpose {requested!r} "
                    f"was expected to "
                    f"{'resolve' if must_resolve else 'refuse'} but did not — "
                    f"the mechanical purpose check has drifted (spec R7)")
    f.note(f"self-test: {valid_ok} valid example(s) confirmed valid, "
           f"{neg_ok} negative example(s) confirmed invalid for their "
           f"intended finding (detail-pinned where the code alone is too "
           f"coarse), {probe_ok} purpose probe(s) confirmed (one resolution, "
           f"one refusal)")


# --------------------------- layer 2: real artifacts ---------------------------

SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__", ".venv"}


def repo_scan(f: Findings, target: Path, docs: dict[str, dict],
              requested_purpose: str | None) -> None:
    sweep = target.is_dir()
    files = sorted(set(target.rglob("*.yaml")) | set(target.rglob("*.yml"))) \
        if sweep else [target]
    records: list[tuple[str, dict]] = []
    checked = skipped = 0
    for path in files:
        parts = set(path.parts)
        if parts & SKIP_DIR_NAMES or EXAMPLES_DIR in path.parents:
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
        checked += 1
        records.append(
            (str(path.relative_to(target) if target.is_dir() else path), doc))
    # Registries and purpose models found in the tree are the adjudication
    # context for the instruments found beside them, matched by domain.
    ctx = Context()
    for _, doc in records:
        ctx.add(doc)
    for domain, doc in sorted(ctx.registries.items()):
        if doc is None:
            f.note(f"several class registries in scope for domain {domain!r}; "
                   f"class checks cannot choose between them and are skipped")
    for domain, doc in sorted(ctx.purpose_models.items()):
        if doc is None:
            f.note(f"several purpose models in scope for domain {domain!r}; "
                   f"purpose checks cannot choose between them and are skipped")
    for label, doc in records:
        validate_record(f, label, doc, docs, ctx)
        if requested_purpose and doc.get("kind") == "xfactory_consent_instrument":
            check_requested_purpose(
                f, label, doc,
                ctx.purpose_models.get(doc.get("domain")), requested_purpose)
    f.note(f"repo scan ({target}): {checked} artifact(s) checked, {skipped} "
           f"skipped (not a consent-instrument kind); packaged examples/ "
           f"excluded (layer 1 owns them). Zero real artifacts is normal in "
           f"this checkout — instances live in the domain repos (Ledgerx "
           f"tenant tree, Medx governed store) per declared placement policy "
           f"(D9)")


# --------------------------- orchestration ---------------------------

def report(f: Findings, strict: bool) -> int:
    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)
    print(f"\nvalidate-consent-instruments: {len(f.errors)} error(s), "
          f"{len(f.warnings)} warning(s)")
    return 1 if f.errors or (strict and f.warnings) else 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=None,
                    help="repo checkout (or single file) to scan for real "
                         "consent-instrument artifacts; omit to self-test only")
    ap.add_argument("--strict", action="store_true",
                    help="treat warnings as errors")
    ap.add_argument("--purpose", default=None, metavar="PURPOSE",
                    help="also check that this ONE requested purpose resolves "
                         "into every scanned instrument's purposes under its "
                         "domain purpose model (spec R7); requires a path")
    args = ap.parse_args()

    if args.purpose is not None and args.path is None:
        print("ERROR --purpose adjudicates scanned instruments; give a path "
              "(the packaged examples are probed by the self-test instead)",
              file=sys.stderr)
        return 2
    if not SCHEMA_DIR.is_dir():
        print(f"ERROR {SCHEMA_DIR} not found", file=sys.stderr)
        return 2
    try:
        docs = load_schemas()
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
                    f"{name}: every schema in this family declares its "
                    f"dialect ($schema) and an $id, so a consumer's stock "
                    f"validator resolves it the same way this one does")

    try:
        self_test(f, docs)
        if args.path is not None:
            target = Path(args.path).resolve()
            if not target.exists():
                print(f"ERROR path {target} not found", file=sys.stderr)
                return 2
            repo_scan(f, target, docs, args.purpose)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR harness failure: {exc}", file=sys.stderr)
        return 2
    return report(f, args.strict)


if __name__ == "__main__":
    sys.exit(main())
