#!/usr/bin/env python3
"""Validate the client-identity-roster contract family (add-client-identity-roster).

The openxFactory-owned CANONICAL validator for the two kinds
`xfactory_client_identity_roster` and `xfactory_client_identity_drift_finding`
(`contracts/schemas/xfactory-client-identity-roster.schema.yaml`). Run from the
pinned openxFactory checkout against a target domain repository, and NEVER
copied into a domain repo — a copy inside a domain repo is itself a conformance
defect under the pack's no-copy rule:

    python3 scripts/validate-client-identity-roster.py TARGET_REPO

DETERMINISTIC AND NETWORK-FREE. Filesystem reads only: no network, no model
call, no subprocess to a provider tool, no clock. Every ordering is sorted, so
identical inputs produce byte-identical findings.

Two layers run.

1. PACKAGED CORPUS SELF-TEST (`examples/client-identity-roster/`). Every
   `*.example.yaml` must validate clean; every file under `negative/` must FAIL
   for its REGISTERED reason, declared in EXPECTED_NEGATIVE_FINDINGS below
   (keyed by filename, optionally pinned by a detail substring where the code
   alone is too coarse). FIVE failure modes are themselves errors: a registered
   probe with no file, a file with no registration, a negative that passes, a
   negative that fails for the WRONG code, and a negative whose code fires
   without the pinned detail.

2. REPO SCAN of the target, in TWO EXACTLY COMPLEMENTARY PASSES over one
   `*.y*ml` universe, so every kind-carrying file is either validated or
   reported and never neither:
   (a) WHOLE-REPO KIND SWEEP: any file carrying the roster kind that is not a
       DIRECT CHILD of `credentials/client-identity-roster/` is
       `misplaced-roster-instance`. The predicate is EXACT-PATH, never a
       directory prefix: under a prefix reading a nested instance at
       `credentials/client-identity-roster/<sub>/x.yaml` passes the sweep AND
       misses pass (b)'s flat glob, which is covered by nothing.
   (b) DECLARED-PLACEMENT VALIDATION: every fragment at the declared path — the
       FLAT glob, direct children only — is schema-validated and rule-checked,
       and the run prints a count of records checked.
   Plus the two rules a packaged file cannot express, because both read the
   TARGET tree: gate-obligation RESOLUTION against the target's `workflows/`
   records, and `consent_ref` RESOLUTION against the target's own
   consent-instrument records.

RECORD-INTERNAL RULES RUN EVEN WHEN THE SCHEMA ALREADY REFUSES THE DOCUMENT,
and each raises its own kebab code. This is structural, not cosmetic: most of
this corpus's negatives are schema-visible (a value outside a closed set, a
missing admission list, a destructive class), and a raw `jsonschema` message
names neither the closed vocabulary nor the extension route that the refusal
messages are required to name. A validator that returned at the first schema
failure would leave those named refusals existing nowhere and make their
expectations-table entries unregisterable. So the rule engine reads the loaded
mapping DEFENSIVELY — a missing or wrong-typed field is skipped by the rule
that would have read it, never crashed on — and runs to completion.

WHAT THIS VALIDATOR DELIBERATELY DOES NOT DO:

  * IT ENFORCES NO COMPLETENESS RULE. Neither the absence of a fragment nor the
    absence of an entry is a finding, and NO code path anywhere in this module
    derives an expected entry set — not from `credentials/requirements.yaml`,
    not from any other inventory. A target with no roster directory, or with
    the directory and no files, prints an explicit notice and exits 0. Absence
    being a finding would be a scope breach, not a strictness improvement.
  * IT RESOLVES NO `evidence_ref`. That is a DECLARED POINTER into another
    repository and its SHAPE is all this validator checks; resolution belongs
    to the cross-domain doc-health family, which assembles from pinned repos.
    The `consent_ref` and `gate_obligation` targets are the opposite posture —
    both are INTRA-repo — which is why those two do resolve here.
  * IT RESOLVES NO `ratified_by`. The ratified resolution clause attaches to
    the instrument citation alone and the ratified scenario for the capability
    is an absence test, so the capability check is presence plus
    domain-qualification. A recorded reading, not an oversight.
  * IT NEVER INFERS A PROVIDER FACT. It compares provider tokens for equality
    and never reads breadth, class, or meaning out of one, and it resolves no
    identifier against any provider catalogue. Every provider fact a rule needs
    is DECLARED in the record beside the token.
  * IT NEVER READS A CLOCK. Grant-window expiry is adjudicated against the
    attestation's own `attested_at`, so identical inputs yield identical
    findings.

Exit codes: 0 clean, 1 findings, 2 harness error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover - harness error
    print("ERROR jsonschema is not installed", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "contracts" / "schemas" / "xfactory-client-identity-roster.schema.yaml"
EXAMPLES_DIR = ROOT / "examples" / "client-identity-roster"

ROSTER_KIND = "xfactory_client_identity_roster"
DRIFT_KIND = "xfactory_client_identity_drift_finding"
CONSENT_KIND = "xfactory_consent_instrument"

# The DECLARED PLACEMENT (FR-020, FR-036), as path parts relative to the target.
PLACEMENT_PARTS = ("credentials", "client-identity-roster")
PLACEMENT_DISPLAY = "credentials/client-identity-roster/<client_ref>.yaml"

SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__", ".venv"}

# The consent family's own closed lifecycle, read for FR-014's in-force test.
# `withdrawn` is admitted here because this feature grows that enum; an ENDED
# instrument is `terminated` or `withdrawn`, and both are the expected state
# beside a RETIRED roster entry.
CONSENT_IN_FORCE = ("amended", "executed")
CONSENT_ENDED = ("terminated", "withdrawn")

# FR-010's name detector. A DETECTOR, NOT A GUARANTEE, and its blind spot is
# stated rather than discovered: a name using an observation word outside this
# list escapes it. The list is admissible only because the load-bearing rule
# beside it is closed-world at the representation level — the record-internal
# check that `authority_class_achieved` equals the maximum declared `achieves`,
# which no naming choice can evade. This list MUST NOT be grown into an
# open-ended reading of prose, and MUST NOT be relied on as the mechanism that
# catches an understated identity.
OBSERVATION_TOKENS = ("audit", "observe", "observer", "read", "readonly",
                      "reader", "viewer")

# `mutate` dominates `observe`; there is no third rank, by ratification.
CLASS_RANK = {"observe": 0, "mutate": 1}

# The five obligations FR-012 requires of a vendor-tenant-multi registration.
VENDOR_OBLIGATIONS = (
    "tenant_allow_list_enforced_at_token_validation",
    "per_client_authorization_state",
    "per_client_revocation_evidence",
    "cross_client_credential_span_statement",
    "per_client_consent_amendment",
)

# Layer-1 negative corpus: filename -> (expected finding code, optional detail
# substring). The detail pins a fixture whose CODE alone is too coarse to prove
# it failed for its own reason — a code reused across several fields, a rule
# with several failure shapes, or a requirement that demands the message NAME
# something. A registration with no file and a file with no registration are
# both errors.
#
# Every negative below is built by mutating ONE minimal conformant record in
# exactly the way its own header names, and every one of them raises its
# REGISTERED code and NO OTHER record-internal code. Where a violation is also
# visible to the schema, the generic `schema` code accompanies it — that is the
# rule engine deliberately running to completion rather than returning at the
# first schema failure, because a raw jsonschema message names neither the
# closed vocabulary nor the extension route the refusals are required to name.
EXPECTED_NEGATIVE_FINDINGS: dict[str, tuple[str, str | None]] = {
    # --- record-internal rules -------------------------------------------
    "consent-recorded-as-access.yaml":
        ("consent-recorded-as-access", "no admission act"),
    "unverified-act-counted-as-access.yaml":
        ("unverified-act-counted-as-access", "verified_at with NO evidence_ref"),
    "undeclared-reach.yaml":
        ("undeclared-reach", "reaches surface 'exchange'"),
    "achieved-exceeds-intended-undeclared.yaml":
        ("achieved-exceeds-intended-undeclared", None),
    "achieved-class-contradicted-by-permissions.yaml":
        ("achieved-class-contradicts-permissions",
         "the maximum class its granted_permissions DECLARE is 'mutate'"),
    "scope-exceeds-unit-undeclared.yaml":
        ("undeclared-scope-excess", "declares no declared_excess"),
    "undeclared-act-surface.yaml":
        ("undeclared-act-surface", "surface 'exchange'"),
    # FR-010 requires the refusal to NAME the token it matched.
    "name-understates-achieved-authority.yaml":
        ("name-understates-achieved-authority",
         "observation-suggesting token 'observer'"),
    "missing-enforcement-test.yaml":
        ("missing-enforcement-test", "no enforcement_test_ref"),
    # The two per-unit rules share a subject and must not be confusable.
    "provider-enforced-without-per-unit-principal.yaml":
        ("provider-enforced-without-per-unit-principal",
         "claims provider_enforced on surface 'business_central'"),
    "per-unit-principal-available-but-logical.yaml":
        ("per-unit-principal-available-but-logical",
         "every admission act there"),
    "per-unit-principal-undeclared.yaml":
        ("per-unit-principal-undeclared",
         "no answer for surface 'business_central'"),
    # Gate ruling G2: the finding must NAME `home_tenant`, so a record that
    # would pass the REJECTED containment reading cannot pass this one.
    "vendor-homed-declared-client-resident.yaml":
        ("vendor-homed-declared-client-resident",
         "home_tenant is '22222222-2222-2222-2222-222222222222'"),
    "vendor-tenant-multi-missing-obligations.yaml":
        ("vendor-tenant-multi-missing-obligations",
         "tenant_allow_list_enforced_at_token_validation"),
    "mutate-without-ratified-capability.yaml":
        ("mutate-without-ratified-capability", "not domain-qualified"),
    "entry-without-consent-instrument.yaml":
        ("entry-without-consent-instrument", "names no consent instrument"),
    # Three failure shapes share this code; pin the one this file encodes.
    "false-standing-credential-attestation.yaml":
        ("false-standing-credential-attestation", "The record contradicts itself"),
    # FR-006 requires the refusal to name EVERY element of the tuple.
    "full-tuple-duplicate.yaml":
        ("duplicate-identity-key",
         "domain='demoxfactory', admission_surface='business_central', "
         "authority_class_intended='observe', blast_radius_unit='unit_a', "
         "duty='observing'"),
    "alias-pair-observationally-identical.yaml":
        ("alias-pair-observationally-identical", "['blast_radius_unit']"),

    # --- closed vocabularies (SC-014), one per set ------------------------
    # Each pin names the SET, because the code alone would be satisfied by the
    # same rule firing on a different field.
    "admission-surface-out-of-vocabulary.yaml":
        ("admission-surface-out-of-vocabulary",
         "admission_surface is 'sharepoint', which is not a member of the "
         "closed admission_surface vocabulary"),
    "destructive-authority-class.yaml":
        ("destructive-authority-class",
         "authority_class_intended is 'destroy', which is not a member of the "
         "closed authority_class vocabulary"),
    "residency-model-out-of-vocabulary.yaml":
        ("residency-model-out-of-vocabulary", "closed residency_model vocabulary"),
    "enforcement-mode-out-of-vocabulary.yaml":
        ("enforcement-mode-out-of-vocabulary", "closed enforcement_mode vocabulary"),
    "lifecycle-state-out-of-vocabulary.yaml":
        ("lifecycle-state-out-of-vocabulary", "closed lifecycle_state vocabulary"),
    "identity-kind-out-of-vocabulary.yaml":
        ("identity-kind-out-of-vocabulary", "closed identity_kind vocabulary"),
    "drift-finding-status-out-of-vocabulary.yaml":
        ("drift-finding-status-out-of-vocabulary", "closed drift_status vocabulary"),

    # --- legend and the declared evidence pointer -------------------------
    "legend-token-missing.yaml":
        ("legend-token-missing", "duty token 'auditing'"),
    "legend-token-declared-twice.yaml":
        ("legend-token-declared-twice", "declared in BOTH"),
    "evidence-ref-malformed.yaml":
        ("evidence-ref-malformed", "is missing ['path']"),

    # --- the drift record --------------------------------------------------
    "drift-finding-without-roster-value.yaml":
        ("drift-finding-without-roster-value", None),
    "drift-finding-without-observed-value.yaml":
        ("drift-finding-without-observed-value", None),
}


# --------------------------- findings ---------------------------

class Findings:
    """`ERROR [kebab-code] message` — the consent validator's shape."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []
        self.codes: list[str] = []

    def error(self, code: str, msg: str) -> None:
        self.errors.append(f"ERROR [{code}] {msg}")
        self.codes.append(code)

    def warn(self, code: str, msg: str) -> None:
        self.warnings.append(f"WARN  [{code}] {msg}")

    def note(self, msg: str) -> None:
        line = f"note  {msg}"
        if line not in self.notes:  # notes are facts about the run, not events
            self.notes.append(line)


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# --------------------------- vocabularies, read FROM the schema ---------------------------

def _consts(node: Any) -> tuple[str, ...]:
    if isinstance(node, dict) and isinstance(node.get("oneOf"), list):
        return tuple(sorted(m["const"] for m in node["oneOf"]
                            if isinstance(m, dict) and "const" in m))
    return ()


class Vocabularies:
    """The closed sets, DERIVED from the schema rather than restated here.

    Restating them in Python would create two declarations of one closed set
    that can silently disagree — the failure this family refuses everywhere
    else. The schema is the single authority; this class only gives the refusal
    messages something to name.
    """

    def __init__(self, schema: dict) -> None:
        defs = schema.get("$defs", {})
        self.admission_surface = _consts(defs.get("admission_surface"))
        self.authority_class = _consts(defs.get("authority_class"))
        self.residency_model = _consts(defs.get("residency_model"))
        self.enforcement_mode = _consts(defs.get("enforcement_mode"))
        self.lifecycle_state = _consts(defs.get("lifecycle_state"))
        self.identity_kind = _consts(defs.get("identity_kind"))
        self.drift_status = _consts(
            defs.get("drift_finding", {}).get("properties", {}).get("status"))
        self.free_token = re.compile(
            defs.get("free_token", {}).get("pattern", "^[a-z0-9][a-z0-9_-]*$"))


# Extension routes, named in every closed-set refusal (FR-007, FR-031, FR-034).
EXTENSION_ROUTE = {
    "admission_surface":
        "a surface enters with the ratified change that governs it "
        "(endpoint MUTATION / Intune write, and Entra-directory MUTATION / "
        "user, group and application administration, arrive with theirs); "
        "non-Entra providers, including a client-org GitHub App installation, "
        "are a named successor routed by client-infrastructure-liaison",
    "authority_class":
        "a destructive class is deliberately unrepresentable — destructive "
        "capability rides the mutate entry's declared authority_class_achieved "
        "with its declared_excess and gate obligation, and earns its own member "
        "only where a provider demonstrably offers a delete-scoped permission "
        "distinct from write, declared with that demonstration",
    "residency_model":
        "a third model arrives with the change that governs it, carrying its "
        "own obligations; there is no class-dependent relaxation",
    "enforcement_mode": "a third mode arrives with the change that governs it",
    "lifecycle_state": "a fourth state arrives with the change that governs it",
    "identity_kind":
        "a new kind arrives with the change that governs the surface or "
        "provider needing it; an unratified kind vocabulary is never invented",
    "drift_status": "a fourth state arrives with the change that governs it",
}


def _closed(f: Findings, label: str, code: str, vocab_name: str,
            allowed: Iterable[str], value: Any, where: str) -> bool:
    """Refuse a value outside a closed set, NAMING the set and the route."""
    allowed = tuple(allowed)
    if value is None or value in allowed:
        return True
    f.error(code,
            f"{label}: {where} is {value!r}, which is not a member of the "
            f"closed {vocab_name} vocabulary (allowed: {list(allowed)}). "
            f"Extension route: {EXTENSION_ROUTE[vocab_name]}.")
    return False


# --------------------------- small readers (defensive by contract) ---------------------------

def _d(node: Any) -> dict:
    return node if isinstance(node, dict) else {}


def _l(node: Any) -> list:
    return node if isinstance(node, list) else []


def _s(node: Any) -> str | None:
    return node if isinstance(node, str) and node else None


def entry_label(fragment_label: str, index: int, entry: dict) -> str:
    ref = _s(entry.get("identity_ref")) or f"<entry {index}>"
    return f"{fragment_label}: entry {ref!r}"


# --------------------------- rules, group 1: closed vocabularies and shapes (2.3) ---------------------------

def check_vocabularies(f: Findings, label: str, entry: dict, v: Vocabularies) -> None:
    _closed(f, label, "identity-kind-out-of-vocabulary", "identity_kind",
            v.identity_kind, entry.get("identity_kind"), "identity_kind")
    _closed(f, label, "admission-surface-out-of-vocabulary", "admission_surface",
            v.admission_surface, entry.get("admission_surface"), "admission_surface")
    _closed(f, label, "residency-model-out-of-vocabulary", "residency_model",
            v.residency_model, entry.get("residency_model"), "residency_model")
    _closed(f, label, "lifecycle-state-out-of-vocabulary", "lifecycle_state",
            v.lifecycle_state, entry.get("lifecycle_state"), "lifecycle_state")
    for field in ("authority_class_intended", "authority_class_achieved"):
        _closed(f, label, "destructive-authority-class", "authority_class",
                v.authority_class, entry.get(field), field)
    for perm in _l(entry.get("granted_permissions")):
        pid = _s(_d(perm).get("id")) or "<unnamed>"
        _closed(f, label, "destructive-authority-class", "authority_class",
                v.authority_class, _d(perm).get("achieves"),
                f"granted_permissions[{pid}].achieves")
        for reach in _l(_d(perm).get("reaches")):
            _closed(f, label, "admission-surface-out-of-vocabulary",
                    "admission_surface", v.admission_surface, reach,
                    f"granted_permissions[{pid}].reaches member")
    for act in _l(entry.get("admission")):
        act_name = _s(_d(act).get("act")) or "<unnamed act>"
        _closed(f, label, "admission-surface-out-of-vocabulary", "admission_surface",
                v.admission_surface, _d(act).get("surface"),
                f"admission[{act_name}].surface")
        _closed(f, label, "enforcement-mode-out-of-vocabulary", "enforcement_mode",
                v.enforcement_mode, _d(act).get("enforcement_mode"),
                f"admission[{act_name}].enforcement_mode")
        check_evidence_ref(f, label, _d(act).get("evidence_ref"),
                           f"admission[{act_name}].evidence_ref")
    for surface in sorted(_d(entry.get("per_unit_principal_available"))):
        _closed(f, label, "admission-surface-out-of-vocabulary", "admission_surface",
                v.admission_surface, surface,
                "per_unit_principal_available key")
    for surface in _l(_d(entry.get("declared_excess")).get("spanned_surfaces")):
        _closed(f, label, "admission-surface-out-of-vocabulary", "admission_surface",
                v.admission_surface, surface,
                "declared_excess.spanned_surfaces member")
    check_evidence_ref(f, label,
                       _d(entry.get("standing_credential_attestation")).get("evidence_ref"),
                       "standing_credential_attestation.evidence_ref")
    for field in ("blast_radius_unit", "duty"):
        token = entry.get(field)
        if isinstance(token, str) and not v.free_token.match(token):
            f.error("free-token-malformed",
                    f"{label}: {field} is {token!r}, which does not match the "
                    f"free-token pattern {v.free_token.pattern}. "
                    f"blast_radius_unit and duty are domain-declared tokens, "
                    f"bound to their provider-native identifiers by the "
                    f"fragment legend — provider fidelity lives in the legend, "
                    f"never in the token spelling.")


def check_evidence_ref(f: Findings, label: str, ref: Any, where: str) -> None:
    """FR-037: SHAPE only. Nothing here opens the referenced tree."""
    if ref is None:
        return
    if not isinstance(ref, dict):
        f.error("evidence-ref-malformed",
                f"{label}: {where} must be a declared pointer object "
                f"{{repo, path, sha?}}, not {type(ref).__name__}. The "
                f"canonical validator checks its shape and never resolves its "
                f"target — it is network-free and reads one repository.")
        return
    missing = [k for k in ("repo", "path") if not _s(ref.get(k))]
    if missing:
        f.error("evidence-ref-malformed",
                f"{label}: {where} is missing {missing} — a declared pointer "
                f"carries repo and path (and optionally sha). Its target is "
                f"never resolved here; resolution belongs to the cross-domain "
                f"doc-health family, which assembles from pinned repos.")
    extra = sorted(set(ref) - {"repo", "path", "sha"})
    if extra:
        f.error("evidence-ref-malformed",
                f"{label}: {where} carries unknown key(s) {extra}; a declared "
                f"pointer is exactly {{repo, path, sha?}}.")


def check_drift_record(f: Findings, label: str, doc: dict, v: Vocabularies) -> None:
    _closed(f, label, "drift-finding-status-out-of-vocabulary", "drift_status",
            v.drift_status, doc.get("status"), "status")
    for field in ("roster_value", "observed_value"):
        if doc.get(field) in (None, "", [], {}):
            f.error(f"drift-finding-without-{field.replace('_', '-')}",
                    f"{label}: a drift finding must record BOTH the roster "
                    f"value and the observed value; {field} is absent. The "
                    f"record exists to state what was declared and what was "
                    f"seen, and it mutates nothing else.")
    if doc.get("status") == "disposed" and not _s(doc.get("disposition_ref")):
        f.error("disposed-finding-without-disposition",
                f"{label}: status is 'disposed' with no disposition_ref — a "
                f"disposal with no citation is exactly the unfalsifiable "
                f"disposal this record exists to prevent.")
    key = _d(doc.get("identity_ref"))
    if key and "authority_class_achieved" in key:
        f.error("drift-finding-key-uses-achieved-class",
                f"{label}: identity_ref carries authority_class_achieved. The "
                f"key's third element is authority_class_INTENDED, because a "
                f"key must be declarative and stable: an achieved-keyed "
                f"reference would name a tuple that no longer matches the "
                f"entry the finding is about, failing the join exactly when it "
                f"is needed.")


# --------------------------- rules, group 2: uniqueness and the alias rule (2.4) ---------------------------

KEY_FIELDS = ("domain", "admission_surface", "authority_class_intended",
              "blast_radius_unit", "duty")
FREE_TOKEN_FIELDS = ("blast_radius_unit", "duty")


def identity_key(domain: str | None, entry: dict) -> tuple:
    return (domain, entry.get("admission_surface"),
            entry.get("authority_class_intended"),
            entry.get("blast_radius_unit"), entry.get("duty"))


def permission_set(entry: dict) -> frozenset:
    """Normalized member tuples `(id, achieves, sorted(reaches))` — the shape
    the alias rule compares now that members are objects."""
    out = set()
    for perm in _l(entry.get("granted_permissions")):
        p = _d(perm)
        reaches = tuple(sorted(str(r) for r in _l(p.get("reaches"))))
        out.add((_s(p.get("id")), p.get("achieves"), reaches))
    return frozenset(out)


def admission_set(entry: dict) -> frozenset:
    """EXACTLY the four ratified elements. `exceeds_governed_unit` is
    deliberately NOT among them: it is a statement ABOUT a scope, not part of
    observational identity."""
    out = set()
    for act in _l(entry.get("admission")):
        a = _d(act)
        out.add((a.get("surface"), a.get("act"), a.get("achieved_scope"),
                 a.get("enforcement_mode")))
    return frozenset(out)


def _comparable(entry: dict) -> dict:
    """Every entry field EXCEPT the two free tokens and the rationale, which
    the alias rule's other two conjuncts own."""
    return {k: v for k, v in entry.items()
            if k not in FREE_TOKEN_FIELDS and k != "duty_separation_rationale"}


def check_uniqueness_and_alias(f: Findings, label: str, domain: str | None,
                               entries: list) -> None:
    """FR-006 and FR-038, BOTH SCOPED WITHIN ONE FRAGMENT.

    Never across fragments: the tuple carries no client_ref and the legend
    binds free tokens PER FRAGMENT, so `sandbox1` in two clients' fragments
    names two different provider objects. Pooling a repo's fragments would
    report a domain's two clients' per-environment identities as ONE duplicate
    — the per-blast-radius-unit flaw re-killed from the other direction.
    """
    seen: dict[tuple, int] = {}
    for i, raw in enumerate(entries):
        entry = _d(raw)
        key = identity_key(domain, entry)
        if None in key:
            continue  # an incomplete key is another rule's finding, not a duplicate
        if key in seen:
            named = ", ".join(f"{name}={value!r}"
                              for name, value in zip(KEY_FIELDS, key))
            f.error("duplicate-identity-key",
                    f"{label}: entries {seen[key]} and {i} share the WHOLE "
                    f"uniqueness tuple ({named}). Entries differing in ANY "
                    f"element validate clean — a per-blast-radius-unit or "
                    f"duty-separated identity is permitted and is never an "
                    f"overlap.")
        else:
            seen[key] = i

    # The alias rule (FR-038): a THREE-predicate conjunction and no broader.
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            a, b = _d(entries[i]), _d(entries[j])
            # (1) differ in free tokens ONLY — read as "in free tokens ONLY",
            # so a pair differing in BOTH is in scope: a domain able to evade
            # the rule by inventing two spellings instead of one would leave it
            # bounding nothing, and the wider reading cannot touch a genuine
            # pair, which differs in achieved_scope or in permissions.
            if _comparable(a) != _comparable(b):
                continue
            differing = [t for t in FREE_TOKEN_FIELDS if a.get(t) != b.get(t)]
            if not differing:
                continue
            # (2) observationally identical — stated separately from (1), so a
            # later narrowing of (1) cannot silently drop it.
            if permission_set(a) != permission_set(b):
                continue
            if admission_set(a) != admission_set(b):
                continue
            # (3) neither declares a duty-separation rationale. This predicate
            # reads THAT FIELD AND NOTHING ELSE.
            if _s(a.get("duty_separation_rationale")) or \
                    _s(b.get("duty_separation_rationale")):
                continue
            f.error("alias-pair-observationally-identical",
                    f"{label}: entries {i} and {j} differ only in "
                    f"{differing} while being observationally identical (the "
                    f"same granted_permissions set and the same admission acts "
                    f"by surface/act/achieved_scope/enforcement_mode) and "
                    f"declaring no duty_separation_rationale. A genuine "
                    f"per-unit pair differs in achieved_scope; a genuine duty "
                    f"pair differs in permissions or declares the rationale.")


# --------------------------- rules, group 3: admission, reach, scope excess (2.5) ---------------------------

def act_is_verified(act: dict) -> bool:
    """VERIFIED BY DERIVATION, never by an asserted flag. There is deliberately
    no `verified: false` property an author could set against the evidence."""
    return bool(_d(act.get("evidence_ref"))) and bool(_s(act.get("verified_at")))


def check_admission(f: Findings, label: str, entry: dict) -> None:
    acts = _l(entry.get("admission"))
    if not acts:
        f.error("consent-recorded-as-access",
                f"{label}: no admission act. Provider CONSENT is not provider "
                f"ADMISSION and is never recordable as access — the measured "
                f"finding this contract exists for is four admin-consented "
                f"permissions held for six days that still returned 401 until "
                f"the admission act landed.")
        return

    for act in acts:
        a = _d(act)
        name = _s(a.get("act")) or "<unnamed act>"
        if _s(a.get("verified_at")) and not _d(a.get("evidence_ref")):
            f.error("unverified-act-counted-as-access",
                    f"{label}: admission act {name!r} declares verified_at with "
                    f"NO evidence_ref — the record claiming a verification it "
                    f"cannot evidence. The two travel as a pair: both present "
                    f"is a verified act, both absent is the unverified state, "
                    f"and an unverified act is excluded from effective reach "
                    f"rather than counted as access.")

    # EFFECTIVE REACH IS COMPUTED, NEVER DECLARED, and reported (FR-003).
    verified = [_d(a) for a in acts if act_is_verified(_d(a))]
    reach = sorted({(str(a.get("surface")), str(a.get("achieved_scope")))
                    for a in verified})
    exceeds = any(a.get("exceeds_governed_unit") is True for a in verified)
    unverified = len(acts) - len(verified)
    f.note(f"{label}: effective reach (VERIFIED acts only) = {reach}; "
           f"exceeds_governed_unit = {exceeds} (the OR over verified acts — "
           f"the union, NOT the narrower act); {unverified} unverified act(s) "
           f"excluded")

    # The scope-excess rule (FR-002, FR-010): the change's own motivating
    # measurement, made checkable rather than merely expressible.
    excess = _d(entry.get("declared_excess"))
    unit = entry.get("blast_radius_unit")
    for a in verified:
        if a.get("exceeds_governed_unit") is not True:
            continue
        if excess:
            continue
        f.error("undeclared-scope-excess",
                f"{label}: verified admission act "
                f"{_s(a.get('act')) or '<unnamed act>'!r} declares "
                f"exceeds_governed_unit with achieved_scope "
                f"{a.get('achieved_scope')!r}, reaching beyond the governed "
                f"blast_radius_unit {unit!r}, and the entry declares no "
                f"declared_excess. A structural bound the provider enforced has "
                f"been converted into one only gate logic enforces, and that "
                f"must be a declared, checkable, tested fact.")


# --------------------------- rules, group 4: authority and structural scoping (2.6) ---------------------------

def touched_surfaces(entry: dict) -> list[str]:
    own = entry.get("admission_surface")
    spanned = _l(_d(entry.get("declared_excess")).get("spanned_surfaces"))
    out = {s for s in [own] if isinstance(s, str)}
    out |= {s for s in spanned if isinstance(s, str)}
    return sorted(out)


def check_authority(f: Findings, label: str, entry: dict) -> None:
    perms = [_d(p) for p in _l(entry.get("granted_permissions"))]
    achieved = entry.get("authority_class_achieved")
    intended = entry.get("authority_class_intended")
    excess = _d(entry.get("declared_excess"))
    declared = [p.get("achieves") for p in perms if p.get("achieves") in CLASS_RANK]

    # FR-004: RECORD-INTERNAL. Never a provider catalogue, never an inference
    # from how an identifier is spelled.
    if declared and achieved in CLASS_RANK:
        maximum = max(declared, key=lambda c: CLASS_RANK[c])
        if achieved != maximum:
            names = sorted({_s(p.get("id")) or "<unnamed>" for p in perms
                            if p.get("achieves") == maximum})
            f.error("achieved-class-contradicts-permissions",
                    f"{label}: authority_class_achieved is {achieved!r} while "
                    f"the maximum class its granted_permissions DECLARE is "
                    f"{maximum!r} (declared by {names}). The record cannot "
                    f"assert an achieved class its own permissions contradict.")

    # FR-010: achieved above intended must be DECLARED.
    if achieved in CLASS_RANK and intended in CLASS_RANK \
            and CLASS_RANK[achieved] > CLASS_RANK[intended] and not excess:
        f.error("achieved-exceeds-intended-undeclared",
                f"{label}: authority_class_achieved {achieved!r} exceeds "
                f"authority_class_intended {intended!r} with no "
                f"declared_excess. Provider-forced breadth is CONFORMANT when "
                f"declared with its provider reason, bounding mechanism, gate "
                f"obligation and enforcement test — and a finding when not.")

    # FR-010's name check: THREE conjuncts, not two. The third is the CURE the
    # ratified acceptance scenario mandates ("passes only once the excess, its
    # provider reason, and its bounding mechanism are declared"); without it
    # this rule fires on the mandated Business Central positive, which three
    # artifacts require to validate with ZERO findings.
    ref = _s(entry.get("identity_ref"))
    if ref and achieved == "mutate" and not excess:
        matched = [t for t in OBSERVATION_TOKENS
                   if re.search(rf"\b{re.escape(t)}\b", ref, re.IGNORECASE)]
        if matched:
            f.error("name-understates-achieved-authority",
                    f"{label}: identity_ref {ref!r} contains the "
                    f"observation-suggesting token {matched[0]!r} while "
                    f"authority_class_achieved is 'mutate' and no "
                    f"declared_excess is present. An entry's name must not "
                    f"describe narrower authority than it achieves. Where "
                    f"intended equals achieved there is no excess to declare "
                    f"and therefore no cure: the only remedy is to rename the "
                    f"identity.")

    # FR-009, permission side: undeclared reach names the SURFACE and the
    # PERMISSION that reaches it.
    allowed = set(touched_surfaces(entry))
    for perm in perms:
        pid = _s(perm.get("id")) or "<unnamed>"
        for reach in sorted({str(r) for r in _l(perm.get("reaches"))}):
            if reach not in allowed:
                f.error("undeclared-reach",
                        f"{label}: granted permission {pid!r} reaches surface "
                        f"{reach!r}, which is neither the entry's own "
                        f"admission_surface {entry.get('admission_surface')!r} "
                        f"nor a declared declared_excess.spanned_surfaces "
                        f"member. Declare the spanned surface with its provider "
                        f"reason and gate obligation, and it is conformant.")

    # FR-009, ACT side. The permission-side rule cannot see an act performed on
    # a surface no permission declares — yet an admission act IS the second key
    # that makes a surface reachable, which is this change's own measured
    # finding. Without this the BLOCKING check would be weaker than the
    # REPORTING one on identical evidence.
    for act in _l(entry.get("admission")):
        a = _d(act)
        surface = a.get("surface")
        if isinstance(surface, str) and surface not in allowed:
            f.error("undeclared-act-surface",
                    f"{label}: admission act "
                    f"{_s(a.get('act')) or '<unnamed act>'!r} is performed on "
                    f"surface {surface!r}, which the entry neither owns nor "
                    f"declares as spanned. An admission act is the second key "
                    f"that makes a surface reachable, so this is reach the "
                    f"record hides.")

    # FR-008, structural before logical — and the coverage rule that makes an
    # absent answer distinguishable from a `false` one.
    mapping = _d(entry.get("per_unit_principal_available"))
    for surface in touched_surfaces(entry):
        if surface not in mapping:
            f.error("per-unit-principal-undeclared",
                    f"{label}: per_unit_principal_available carries no answer "
                    f"for surface {surface!r}, which this entry touches. An "
                    f"absent key and a declared `false` are otherwise "
                    f"indistinguishable and the structural-before-logical rule "
                    f"has nothing to read. A key for a surface the entry does "
                    f"NOT touch is not a finding — the key space is already "
                    f"closed by the vocabulary.")
    # A FALSE CLAIM is per-ACT: an act claiming provider_enforced where the
    # entry declares no per-unit principal at that surface is that act lying,
    # whatever its siblings do.
    for act in _l(entry.get("admission")):
        a = _d(act)
        surface = a.get("surface")
        if not isinstance(surface, str) or surface not in mapping:
            continue
        name = _s(a.get("act")) or "<unnamed act>"
        if a.get("enforcement_mode") == "provider_enforced" \
                and mapping.get(surface) is False:
            f.error("provider-enforced-without-per-unit-principal",
                    f"{label}: admission act {name!r} claims "
                    f"provider_enforced on surface {surface!r} where the entry "
                    f"declares NO principal scoped to the governed "
                    f"blast_radius_unit. A bound may be recorded as "
                    f"logic-enforced where no such principal exists, with the "
                    f"provider reason recorded — but it may not be claimed as "
                    f"provider-enforced.")

    # "LEFT UNUSED" IS PER-SURFACE, NOT PER-ACT, and the distinction is
    # load-bearing. The ratified scenario is "a surface that DOES offer such a
    # principal while the entry declares logical enforcement INSTEAD" — instead
    # of USING it. A per-act reading fires on the mandated Business Central
    # positive, whose per-environment application user USES the principal while
    # its admin-center act cannot, having no scope selector at all; and that
    # entry is required to validate with ZERO findings. So the finding is: the
    # principal is available at this surface and NO act here uses it.
    for surface in touched_surfaces(entry):
        if mapping.get(surface) is not True:
            continue
        here = [_d(a) for a in _l(entry.get("admission"))
                if _d(a).get("surface") == surface]
        if not here:
            continue
        if any(a.get("enforcement_mode") == "provider_enforced" for a in here):
            continue  # the available principal IS used at this surface
        names = sorted({_s(a.get("act")) or "<unnamed act>" for a in here})
        f.error("per-unit-principal-available-but-logical",
                f"{label}: a per-unit principal IS available at surface "
                f"{surface!r}, yet every admission act there ({names}) declares "
                f"logic_enforced — the available principal is left unused. "
                f"Structure before logic: use the principal the provider itself "
                f"enforces. An act that CANNOT use it (one with no scope "
                f"selector) is conformant beside a sibling act that does.")

    # FR-011's record-internal half. (Its RESOLUTION half is repo-context.)
    if excess and not _s(excess.get("enforcement_test_ref")):
        f.error("missing-enforcement-test",
                f"{label}: declared_excess names no enforcement_test_ref. A "
                f"gate obligation without a test proving the gate REFUSES an "
                f"out-of-unit target documents the degradation it exists to "
                f"prevent.")


# --------------------------- rules, group 5: residency, lifecycle, attestation (2.7) ---------------------------

def check_residency(f: Findings, label: str, entry: dict,
                    client_tenant: str | None) -> None:
    model = entry.get("residency_model")
    if model == "client_tenant_single":
        # The predicate is EQUALITY against the fragment's DECLARED comparand,
        # never a containment reading (`home_tenant in principal_locations`),
        # which passes an identity homed in the WRONG client's tenant — the
        # exact case the ratified refusal exists to catch.
        if client_tenant is None:
            return
        home = entry.get("home_tenant")
        offenders = [p for p in _l(entry.get("principal_locations"))
                     if p != client_tenant]
        if home != client_tenant or offenders:
            f.error("vendor-homed-declared-client-resident",
                    f"{label}: residency_model is 'client_tenant_single' but "
                    f"home_tenant is {home!r} against the fragment's declared "
                    f"client_tenant {client_tenant!r}"
                    + (f" (and principal_locations {offenders} sit elsewhere)"
                       if offenders else "")
                    + ". A registration homed outside the client tenant cannot "
                      "be declared client-resident on the grounds that its "
                      "principal appears in the client tenant.")
    elif model == "vendor_tenant_multi":
        obligations = _d(entry.get("vendor_tenant_multi_obligations"))
        missing = [o for o in VENDOR_OBLIGATIONS if not _s(obligations.get(o))]
        if missing:
            f.error("vendor-tenant-multi-missing-obligations",
                    f"{label}: residency_model is 'vendor_tenant_multi' and the "
                    f"governed model's obligations are incomplete — missing "
                    f"{missing}. Client-resident single-tenant is the default "
                    f"for EVERY authority class; the multi-tenant model is "
                    f"admissible only with its full obligations.")


def check_attestation(f: Findings, label: str, entry: dict) -> None:
    """RECORD-INTERNAL ONLY. No credential store, grant record or provider is
    consulted, and no clock is read: window expiry is adjudicated against the
    attestation's own `attested_at`."""
    att = _d(entry.get("standing_credential_attestation"))
    if not att:
        return
    claim = att.get("no_standing_credential")
    held = _s(att.get("held_credential_ref"))
    window = _s(att.get("grant_window_ref"))
    expires = _s(att.get("grant_window_expires_at"))
    attested = _s(att.get("attested_at"))
    if claim is True and held:
        f.error("false-standing-credential-attestation",
                f"{label}: standing_credential_attestation claims "
                f"no_standing_credential while declaring held_credential_ref "
                f"{held!r}. The record contradicts itself.")
        return
    if held and not window:
        f.error("false-standing-credential-attestation",
                f"{label}: a held credential ({held!r}) is declared against no "
                f"approved grant window. A credential held outside an approved "
                f"grant window makes the attestation false.")
        return
    if held and expires and attested and expires < attested:
        f.error("false-standing-credential-attestation",
                f"{label}: the grant window {window!r} closed at {expires}, "
                f"BEFORE the attestation was made at {attested}, while "
                f"held_credential_ref {held!r} is declared. The credential is "
                f"held outside an approved grant window.")


# --------------------------- rules, group 6: the two roots and the legend (2.8) ---------------------------

def _domain_qualified(value: str) -> bool:
    for sep in (":", "/"):
        if sep in value:
            left, _, right = value.partition(sep)
            if left.strip() and right.strip():
                return True
    return False


def check_roots(f: Findings, label: str, entry: dict) -> None:
    if not _s(entry.get("consent_ref")):
        f.error("entry-without-consent-instrument",
                f"{label}: names no consent instrument. CONSENT — not our own "
                f"ratification — is what authorizes standing in another "
                f"party's tenant, so an entry citing a capability and no "
                f"instrument is invalid.")
    is_mutate = "mutate" in (entry.get("authority_class_intended"),
                             entry.get("authority_class_achieved"))
    ratified = _s(entry.get("ratified_by"))
    if is_mutate and (not ratified or not _domain_qualified(ratified)):
        detail = ("names no ratified capability" if not ratified
                  else f"names {ratified!r}, which is not domain-qualified")
        f.error("mutate-without-ratified-capability",
                f"{label}: a mutate entry {detail}. This is an ERROR that "
                f"fails the owning domain's gate, not a report-only finding.")


def check_legend(f: Findings, label: str, fragment: dict) -> None:
    """EXACTLY the two findings the requirement names, and no third rule.

    An unused legend entry is NOT a finding: no requirement makes it one, it
    would fire on a conformant fragment whose entry is `retired` or `planned`,
    and a rule with no negative confirmation is itself a defect.
    """
    legend = _d(fragment.get("legend"))
    units = _d(legend.get("blast_radius_units"))
    duties = _d(legend.get("duties"))
    for token in sorted(set(units) & set(duties)):
        f.error("legend-token-declared-twice",
                f"{label}: legend token {token!r} is declared in BOTH "
                f"blast_radius_units and duties. A token binds to one "
                f"provider-native identifier on one axis; declaring it twice "
                f"makes the binding ambiguous.")
    for i, raw in enumerate(_l(fragment.get("entries"))):
        entry = _d(raw)
        label_i = entry_label(label, i, entry)
        for field, bound in (("blast_radius_unit", units), ("duty", duties)):
            token = entry.get(field)
            if isinstance(token, str) and token not in bound:
                f.error("legend-token-missing",
                        f"{label_i}: {field} token {token!r} has no entry in "
                        f"the fragment legend. Every free token used in a "
                        f"fragment is bound there to its provider-native "
                        f"identifier — that binding is where provider fidelity "
                        f"lives for the values the neutral layer leaves open.")


# --------------------------- the record-internal rule engine ---------------------------

def check_record(f: Findings, label: str, doc: Any, v: Vocabularies) -> None:
    """Runs to completion whether or not the schema already refused the
    document, reading the mapping defensively throughout."""
    if not isinstance(doc, dict):
        return
    kind = doc.get("kind")
    if kind == DRIFT_KIND:
        check_drift_record(f, label, doc, v)
        return
    if kind != ROSTER_KIND:
        return
    check_legend(f, label, doc)
    domain = _s(doc.get("domain"))
    client_tenant = _s(doc.get("client_tenant"))
    entries = _l(doc.get("entries"))
    check_uniqueness_and_alias(f, label, domain, entries)
    for i, raw in enumerate(entries):
        entry = _d(raw)
        el = entry_label(label, i, entry)
        check_vocabularies(f, el, entry, v)
        check_admission(f, el, entry)
        check_authority(f, el, entry)
        check_residency(f, el, entry, client_tenant)
        check_attestation(f, el, entry)
        check_roots(f, el, entry)


def schema_findings(validator: Draft202012Validator, doc: Any) -> list[str]:
    """Schema messages with the `oneOf` kind-mismatch noise filtered out, so
    the reported message is the branch-specific one."""
    out: list[str] = []
    for err in sorted(validator.iter_errors(doc),
                      key=lambda e: (list(e.absolute_path), e.message)):
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        if err.validator == "oneOf" and err.context:
            msgs = sorted({e.message for e in err.context
                           if "const" not in e.message})
            for m in msgs[:3] or [err.message]:
                out.append(f"{loc}: {m}")
            continue
        out.append(f"{loc}: {err.message}")
    return out


def validate_document(f: Findings, label: str, doc: Any,
                      validator: Draft202012Validator, v: Vocabularies) -> None:
    for msg in schema_findings(validator, doc):
        f.error("schema", f"{label}: {msg}")
    check_record(f, label, doc, v)


# --------------------------- layer 1: the packaged corpus self-test (2.2) ---------------------------

def record_findings(doc: Any, validator: Draft202012Validator,
                    v: Vocabularies) -> tuple[list[str], list[str]]:
    """(codes, lines) for ONE document, in isolation from the run's findings."""
    probe = Findings()
    validate_document(probe, "probe", doc, validator, v)
    return probe.codes, probe.errors


def self_test(f: Findings, validator: Draft202012Validator, v: Vocabularies) -> None:
    if not EXAMPLES_DIR.is_dir():
        f.note(f"self-test: {EXAMPLES_DIR.relative_to(ROOT)} does not exist "
               f"yet, so layer 1 is inert. It becomes a hard gate the moment "
               f"the packaged family directory lands.")
        if EXPECTED_NEGATIVE_FINDINGS:
            f.error("negative-corpus-missing",
                    f"self-test: {len(EXPECTED_NEGATIVE_FINDINGS)} negative "
                    f"probe(s) are registered but the packaged corpus does not "
                    f"exist — a registered probe with no file is one of the "
                    f"five failure modes.")
        return

    positives = sorted(EXAMPLES_DIR.glob("*.example.yaml"))
    for path in positives:
        codes, lines = record_findings(load_yaml(path), validator, v)
        if codes:
            f.error("positive-should-pass",
                    f"self-test: positive {path.name} is not clean: {lines}")

    neg_dir = EXAMPLES_DIR / "negative"
    negatives = sorted(neg_dir.glob("*.yaml")) if neg_dir.is_dir() else []
    on_disk = {p.name for p in negatives}

    for name in sorted(set(EXPECTED_NEGATIVE_FINDINGS) - on_disk):
        f.error("negative-missing",
                f"self-test: negative {name} is registered in the "
                f"expectations table but is not on disk.")

    for path in negatives:
        want = EXPECTED_NEGATIVE_FINDINGS.get(path.name)
        codes, lines = record_findings(load_yaml(path), validator, v)
        if want is None:
            f.error("negative-unregistered",
                    f"self-test: negative {path.name} is on disk with no entry "
                    f"in the expectations table — a file with no probe.")
            continue
        code, detail = want
        if not codes:
            f.error("negative-should-fail",
                    f"self-test: negative {path.name} validated CLEAN; it must "
                    f"be refused for {code!r}.")
            continue
        if code not in codes:
            f.error("negative-wrong-reason",
                    f"self-test: negative {path.name} must be refused for "
                    f"{code!r} but raised {sorted(set(codes))} — a negative "
                    f"that fails for the wrong reason proves nothing.")
            continue
        if detail is not None:
            hits = [ln for ln in lines if f"[{code}]" in ln and detail in ln]
            if not hits:
                f.error("negative-detail-mismatch",
                        f"self-test: negative {path.name} raised {code!r} but "
                        f"without the pinned detail {detail!r}; the code alone "
                        f"is too coarse to prove it failed for its own reason.")

    if not any(e.startswith("ERROR [negative-") or
               e.startswith("ERROR [positive-") for e in f.errors):
        f.note(f"self-test: {len(positives)} positive example(s) confirmed "
               f"clean, {len(negatives)} negative example(s) confirmed refused "
               f"for their registered reason (detail-pinned where the code "
               f"alone is too coarse)")


# --------------------------- layer 2: the repo scan (2.9, 2.10) ---------------------------

def is_self_checkout(target: Path) -> bool:
    """True when the target IS this neutral checkout (or a clone of it).

    Its own fixture corpora are then excluded from the sweep: the packaged
    `examples/` tree, and `tests/` — the latter is LOAD-BEARING, not tidiness,
    because the cross-domain family's fixtures put REAL roster fragments at
    each FIXTURE repo's declared placement, which is not THIS checkout's, so
    without the exclusion a self-scan reports every one as misplaced. Neither
    exclusion narrows the sweep over a TARGET DOMAIN repo, which carries no
    such trees.
    """
    return (target / "contracts" / "schemas" /
            "xfactory-client-identity-roster.schema.yaml").is_file()


def sweep_files(target: Path) -> list[Path]:
    excluded: list[Path] = []
    if is_self_checkout(target):
        excluded = [target / "examples" / "client-identity-roster",
                    target / "tests"]
    out = []
    for path in sorted(set(target.rglob("*.yaml")) | set(target.rglob("*.yml"))):
        if set(path.parts) & SKIP_DIR_NAMES:
            continue
        if any(ex in path.parents for ex in excluded):
            continue
        out.append(path)
    return out


def gate_ids(target: Path) -> set[str]:
    """Every gate id declared in the target's governed workflow records.

    Collected by walking for `gates` lists rather than by assuming one record
    shape, so a domain's own workflow dialect resolves as readily as the
    neutral `xfactory_workflow` one.
    """
    found: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            gates = node.get("gates")
            if isinstance(gates, list):
                for gate in gates:
                    if isinstance(gate, dict) and _s(gate.get("id")):
                        found.add(gate["id"])
                    elif isinstance(gate, str) and gate:
                        found.add(gate)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    workflows = target / "workflows"
    if not workflows.is_dir():
        return found
    for path in sorted(set(workflows.rglob("*.yaml")) | set(workflows.rglob("*.yml"))):
        try:
            walk(load_yaml(path))
        except yaml.YAMLError:
            continue
    return found


def consent_instruments(target: Path) -> dict[str, str | None]:
    """`instrument_id` -> `status`, by KIND SWEEP.

    The consent family declares no domain placement to cite the way the gate
    obligation cites `workflows/`, so resolution uses the mechanism that
    family's own validator uses. This is INTRA-repo and crosses no repository
    boundary — the opposite posture from `evidence_ref`.
    """
    out: dict[str, str | None] = {}
    for path in sweep_files(target):
        try:
            doc = load_yaml(path)
        except yaml.YAMLError:
            continue
        if not isinstance(doc, dict) or doc.get("kind") != CONSENT_KIND:
            continue
        iid = _s(doc.get("instrument_id"))
        if iid:
            out[iid] = doc.get("status")
    return out


def check_repo_context(f: Findings, label: str, doc: dict, gates: set[str],
                       instruments: dict[str, str | None]) -> None:
    for i, raw in enumerate(_l(doc.get("entries"))):
        entry = _d(raw)
        el = entry_label(label, i, entry)

        obligation = _s(_d(entry.get("declared_excess")).get("gate_obligation"))
        if obligation and obligation not in gates:
            f.error("unresolvable-gate-obligation",
                    f"{el}: declared_excess.gate_obligation {obligation!r} "
                    f"resolves to no gate in the target's workflows/ records "
                    f"(found: {sorted(gates)}). An unenforced obligation "
                    f"converts an undetected widening into a documented one.")

        ref = _s(entry.get("consent_ref"))
        if not ref:
            continue  # absence is check_roots's finding, not this one's
        if ref not in instruments:
            f.error("unresolvable-consent-citation",
                    f"{el}: consent_ref {ref!r} resolves to no "
                    f"xfactory_consent_instrument in the target repository. "
                    f"Presence of a citation is not resolution, and a citation "
                    f"resolving to nothing is exactly the failure the change's "
                    f"central claim depends on catching.")
            continue
        status = instruments[ref]
        # The in-force test is LIFECYCLE-SCOPED. A `retired` entry is EXEMPT:
        # the ratified cascade runs withdrawal or termination THROUGH to
        # retirement while the record is RETAINED, so an ended instrument is
        # the EXPECTED state beside it. An unscoped rule would turn the
        # cascade's own correct end state into a permanently red blocking gate
        # whose only cure is deleting a record required to be kept.
        if entry.get("lifecycle_state") == "retired":
            continue
        if status not in CONSENT_IN_FORCE:
            f.error("consent-instrument-not-in-force",
                    f"{el}: consent_ref {ref!r} RESOLVES, but that instrument's "
                    f"status is {status!r}, which is not in force (in force is "
                    f"{list(CONSENT_IN_FORCE)}). Only a `retired` entry may "
                    f"cite an ended instrument "
                    f"({list(CONSENT_ENDED)}); this entry is "
                    f"{entry.get('lifecycle_state')!r}.")


def repo_scan(f: Findings, target: Path, validator: Draft202012Validator,
              v: Vocabularies) -> int:
    placement = target.joinpath(*PLACEMENT_PARTS)

    # PASS (a): the whole-repo kind sweep. EXACT-PATH, never a prefix.
    for path in sweep_files(target):
        try:
            doc = load_yaml(path)
        except yaml.YAMLError:
            continue  # a file that does not parse cannot carry the kind
        if not isinstance(doc, dict) or doc.get("kind") != ROSTER_KIND:
            continue
        if path.parent == placement:
            continue
        f.error("misplaced-roster-instance",
                f"{path.relative_to(target)}: carries kind {ROSTER_KIND!r} "
                f"outside the declared placement. A domain's fragments live at "
                f"{PLACEMENT_DISPLAY}, ONE file per (client, domain) and a "
                f"DIRECT CHILD of that directory — a nested instance is "
                f"reached by no validating glob. Placement is a contract.")

    # PASS (b): declared-placement validation — the FLAT glob, direct children
    # only, so (a) and (b) are exact complements over one *.y*ml universe.
    if not placement.is_dir():
        f.note(f"absence: {target.name} publishes no "
               f"{'/'.join(PLACEMENT_PARTS)}/ directory, so there is no roster "
               f"fragment to check. This is NOT a finding: neither a missing "
               f"fragment nor a missing entry is a finding in this release, "
               f"and no expected entry set is derived from any inventory.")
        return 0

    fragments = sorted(set(placement.glob("*.yaml")) | set(placement.glob("*.yml")))
    if not fragments:
        f.note(f"absence: {'/'.join(PLACEMENT_PARTS)}/ exists in "
               f"{target.name} but publishes no fragment. This is NOT a "
               f"finding, for the same reason: absence is never a finding here.")
        return 0

    gates = gate_ids(target)
    instruments = consent_instruments(target)
    checked = 0
    for path in fragments:
        label = str(path.relative_to(target))
        try:
            doc = load_yaml(path)
        except yaml.YAMLError as exc:
            f.error("yaml", f"{label}: parse failure: {exc}")
            continue
        checked += 1
        validate_document(f, label, doc, validator, v)
        if isinstance(doc, dict) and doc.get("kind") == ROSTER_KIND:
            check_repo_context(f, label, doc, gates, instruments)
    return checked


# --------------------------- orchestration ---------------------------

def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    target = Path(sys.argv[1]).resolve()
    if not target.is_dir():
        print(f"ERROR {target} is not a directory", file=sys.stderr)
        raise SystemExit(2)
    if not SCHEMA_PATH.is_file():
        print(f"ERROR {SCHEMA_PATH} not found", file=sys.stderr)
        raise SystemExit(2)

    schema = load_yaml(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    vocab = Vocabularies(schema)

    f = Findings()
    self_test(f, validator, vocab)
    checked = repo_scan(f, target, validator, vocab)

    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)

    verdict = "PASS" if not f.errors else "FAIL"
    print(f"\n{target.name}: {checked} roster record(s) checked, "
          f"{len(f.errors)} error(s) -> {verdict}")
    raise SystemExit(0 if not f.errors else 1)


if __name__ == "__main__":
    main()
