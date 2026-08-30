#!/usr/bin/env python3
"""Validate a domain repo's credential contracts against the neutral schema.

Canonical validator for the credential-contracts capability
(promote-credential-contracts change; DTN-004). Run from the pinned
openxFactory checkout, never copied into domain repos:

    python3 scripts/validate-credential-contracts.py <domain-repo-path>

Files under credentials/*.yaml|yml whose kind is one of the five contract
kinds validate against contracts/schemas/xfactory-credential-contracts.schema.yaml;
files with other kinds (e.g. domain policy records) are skipped with notice;
files with no kind envelope are errors.

TWO SEVERITIES, SINCE add-binding-consumer-identity. This validator printed
`ERROR` and counted errors and nothing else, so the deprecation posture the
versioning policy requires before any narrowing — "at least one full minor
release where the old shape produced deprecation warnings" — was not merely
unimplemented here, it was INEXPRESSIBLE. The warning channel below follows
`scripts/validate-client-identity-roster.py`'s `WARN  [code] message` shape
rather than inventing a fourth. A warning never reddens the verdict; the
EIGHT `consumer-*` codes it carries are the deprecation the next major's
refusals depend on, and every one of them is registered against a packaged
probe in `examples/credential-contracts/warning/`.
"""
from __future__ import annotations

import re
import sys
from itertools import combinations
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

SCHEMA = Path(__file__).resolve().parents[1] / "contracts/schemas/xfactory-credential-contracts.schema.yaml"
KINDS = {
    "xfactory_credential_requirements",
    "xfactory_runtime_capability_grant_template",
    "xfactory_credential_binding_template",
    "xfactory_credential_broker_contract",
    "xfactory_credential_audit_policy",
}

# Semantic checks for add-dispatch-credential-contract: the dispatch-only
# least-privilege + serving-tier-separation and reference-delivery invariants
# the shape schema cannot express. Neutral — they read the record, not the
# domain's meaning of a scope, beyond the trigger-scope allowlist.
EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples/credential-contracts"
DISPATCH_SCOPES = {"actions:write", "actions:read", "metadata:read"}
RAW_SECRET_MARKERS = ("-----BEGIN", "ghp_", "github_pat_", "gho_", "ghs_", "AKIA")
_B64ISH = re.compile(r"[A-Za-z0-9+/=]{40,}")
# openxFactory#506: three secret families the marker list and the base64 screen
# both miss, expanded here BECAUSE add-binding-consumer-identity §2.6 widens
# this screen's SCOPE to two new free-string members. Widening the scope of a
# leaky screen without fixing the screen would ship the gap wider.
#   (a) credential-bearing URIs   postgresql://user:password@host/db
#   (b) key=value assignments     password=hunter2, client_secret=…, token=…
#   (c) structured bearer tokens  a dotted JWT
_CONNECTION_STRING = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://[^\s/:@]+:[^\s/@]+@")
_KEYED_SECRET = re.compile(
    r"(?:^|[\s;,&])(?:password|passwd|pwd|secret|client_secret|token|api[_-]?key"
    r"|access[_-]?key|private[_-]?key|accountkey|sharedaccesskey)\s*=\s*\S",
    re.IGNORECASE,
)
# A JWT's first segment is base64url of `{"…`, so it always begins `eyJ`. The
# prefix is REQUIRED rather than matching any three dotted segments, because a
# dotted identifier (`xf.sync.lane`) is a legitimate holder reference and a
# screen that refused it would be worse than the gap it closes.
_DOTTED_JWT = re.compile(r"^eyJ[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]{4,}\.[A-Za-z0-9_-]*$")
# KNOWN LIMIT, recorded rather than papered over (add-binding-consumer-identity
# §2.6): `_B64ISH` requires 40 characters, so a 38-character alphanumeric secret
# passes this screen even after the expansion above. The screen catches SHAPES
# it recognises; it is not a secret detector and must not be described as one.

# each packaged negative must raise a finding whose code starts with this
NEGATIVE_EXPECTATIONS = {
    "dispatch-reuses-content-secret.yaml": "shared-secret-identity",
    "dispatch-grants-contents.yaml": "dispatch-scope-ceiling",
    "baked-secret-in-binding.yaml": "baked-secret",
    "issuance-precondition-out-of-vocabulary.yaml": "issuance-precondition-unknown",
    "issuance-precondition-valued-false.yaml": "issuance-precondition-unknown",
    "dispatch-content-pair-declares-sharing.yaml": "shared-secret-identity",
    "consumer-shared-holder-reference.yaml": "shared-secret-identity",
    "consumer-one-sided-acknowledgment.yaml": "shared-secret-identity",
    "consumer-acknowledgment-valued-false.yaml": "shared-secret-identity",
    "consumer-requirement-ref-unresolvable.yaml": "shared-secret-identity",
    "consumer-requirement-ref-ambiguous.yaml": "shared-secret-identity",
    "consumer-requirement-ref-escapes-tree.yaml": "shared-secret-identity",
    "consumer-shared-authority-identity.yaml": "shared-authority-identity",
    "three-bindings-two-share-authority.yaml": "shared-authority-identity",
    "consumer-holder-ref-raw-secret.yaml": "baked-secret",
    "consumer-fetch-identity-raw-secret.yaml": "baked-secret",
}

# add-client-identity-roster (Decision B): the CLOSED issuance-precondition
# vocabulary. The schema declares it too, and this mirror is STRUCTURALLY
# REQUIRED rather than decorative — the self-test above adjudicates registered
# negatives against `_semantic_findings` ONLY, so a schema-only implementation
# would make its own negatives unregisterable and leave the refusal with no
# probe at all.
ISSUANCE_PRECONDITIONS = ("accepted_request_required", "registered_active_subject",
                          "roster_drift_clear_required")

# --------------------------------------------------------------------------
# add-binding-consumer-identity — the consumer block, DECLARED at this minor
# and CONSTRAINED at the major.
# --------------------------------------------------------------------------
# The release every deprecation below names. It is a STRING in one place so a
# message cannot drift from the policy entry that governs it.
MAJOR_RELEASE = "contract-v3.0"

# The block's declared member set. Mirrored from the schema's description for
# the same structural reason ISSUANCE_PRECONDITIONS is mirrored: at this minor
# the schema CONSTRAINS nothing about the block, so the member set has no
# enforceable home there and the warnings would have no vocabulary to check
# against. `tests/credential_contracts/` gates the mirror against the schema.
CONSUMER_MEMBERS = ("holder_ref", "fetch_identity", "requirement_ref",
                    "shared_credential_acknowledged", "instantiation_stub")
CONSUMER_IDENTIFIERS = ("holder_ref", "fetch_identity")
CONST_TRUE_TOKENS = ("shared_credential_acknowledged", "instantiation_stub")
REQUIREMENT_REF_MEMBERS = ("requirement_id", "requirements_document_ref")

# identity-brokering's own identifier grammar (`$defs/identifier`, shipped and
# digest-pinned since contract-v1.37): the vocabulary is REUSED, not re-coined.
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")
IDENTIFIER_MAX = 200
# Repository-relative, non-escaping, non-foreign, YAML. Verified by
# construction: `../x.yaml`, `/etc/x.yaml` and `OpsxFactory:credentials/r.yaml`
# are all refused (the ':' is outside the segment character set, a leading '/'
# cannot start the first segment, and the lookahead refuses any '..' segment).
DOCUMENT_REF = re.compile(
    r"^(?!.*(?:^|/)\.\.(?:/|$))[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*\.(?:yaml|yml)$")
DOCUMENT_REF_MAX = 300  # identity-brokering's own bound on this member

# The CLOSED access-mode vocabulary — declared in the schema's description at
# this minor, enforced by `enum` at the major. Initial members are the values
# already in the wild; adding one is its own additive act.
ACCESS_MODES = ("contents_write", "delegated_api", "dispatch_only", "workload_identity")

# THE DEPRECATION SET, ENUMERATED AGAINST THE REFUSALS RATHER THAN COUNTED.
# One code per shape the major refuses; a shape that no code names is a shape
# the deprecation does not serve. The self-test checks the packaged corpus
# carries one registered probe per member of this tuple, so the next code added
# cannot silently ship unprobed.
DEPRECATION_CODES = (
    "consumer-identity-undeclared",
    "consumer-block-incomplete",
    "consumer-block-unknown-member",
    "consumer-member-grammar",
    "consumer-token-not-true",
    "consumer-binding-key-grammar",
    "consumer-access-mode-vocabulary",
    "consumer-requirement-ref-grammar",
)

# each packaged warning fixture must raise a warning carrying this code
WARNING_EXPECTATIONS = {
    "consumer-identity-undeclared.yaml": "consumer-identity-undeclared",
    "live-values-in-stub-named-file.template.yaml": "consumer-identity-undeclared",
    "consumer-block-incomplete.yaml": "consumer-block-incomplete",
    "consumer-block-locally-shaped.yaml": "consumer-block-incomplete",
    "consumer-block-unknown-member.yaml": "consumer-block-unknown-member",
    "consumer-member-grammar.yaml": "consumer-member-grammar",
    "consumer-token-not-true.yaml": "consumer-token-not-true",
    "consumer-binding-key-grammar.yaml": "consumer-binding-key-grammar",
    "consumer-access-mode-vocabulary.yaml": "consumer-access-mode-vocabulary",
    "consumer-requirement-ref-grammar.yaml": "consumer-requirement-ref-grammar",
}


def _looks_like_raw_secret(value: str) -> bool:
    v = value.strip()
    return (any(m in v for m in RAW_SECRET_MARKERS)
            or bool(_B64ISH.fullmatch(v))
            or bool(_CONNECTION_STRING.search(v))
            or bool(_KEYED_SECRET.search(v))
            or bool(_DOTTED_JWT.fullmatch(v)))


def _is_identifier(value: object) -> bool:
    return (isinstance(value, str) and 1 <= len(value) <= IDENTIFIER_MAX
            and bool(IDENTIFIER.fullmatch(value)))


def _is_document_ref(value: object) -> bool:
    """The path grammar AND its length bound. The bound is checked HERE rather
    than only at the major because every planned narrowing owes its warning
    release: a 400-character reference that this minor accepted silently would
    meet a `maxLength` at the major with no deprecation behind it (PR #516,
    Codex P2)."""
    return (isinstance(value, str) and 1 <= len(value) <= DOCUMENT_REF_MAX
            and bool(DOCUMENT_REF.fullmatch(value)))


def _mapping(value: object) -> dict:
    """The value as a mapping, or an empty one. A SCHEMA-INVALID record reaches
    the semantic pass — the two passes run BESIDE each other, not one behind the
    other — so `credential_bindings: [a, b]` would otherwise reach `.items()`
    and raise AttributeError, aborting the whole repository scan. The crash
    class Codex found on sorted keys is the same class Copilot then found on
    assumed types; both are answered the same way: report, never raise."""
    return value if isinstance(value, dict) else {}


def _sequence(value: object) -> list:
    """The value as a list, or an empty one — `requirements: 7` iterated is a
    TypeError, and a scan that dies on one malformed record reports nothing
    about the rest of the tree."""
    return value if isinstance(value, list) else []


def _consumer(binding: object) -> object:
    """The raw `consumer:` value, whatever shape it is. The block is UNCONSTRAINED
    at this minor, so this deliberately returns scalars and lists too."""
    if not isinstance(binding, dict):
        return None
    return binding.get("consumer")


def _declares_stub(consumer: object) -> bool:
    """A STUB IS A RECORD THAT DECLARES THE TOKEN AND NAMES NOBODY.

    The token alone is not the test, and reading it as the test was a real hole
    (PR #516, Codex P1): an instantiator that filled in `holder_ref` and left
    the token behind kept the exemption, so the missing `fetch_identity` went
    unwarned through the whole minor and the requiredness it should have been
    served by arrived at the major unannounced. The ratified scenario is
    explicit on both halves — *"a record that is an instantiation stub carries
    the const-true stub token AND NO IDENTIFIERS"*, and *"a record carrying LIVE
    values MUST NOT declare the token"* — so the exemption is withheld the
    moment either identifier appears, and the ordinary warnings resume.

    A block declaring the token beside BOTH identifiers is a different matter
    and is deliberately left to the REQUIREMENT rather than claimed by this
    check: nothing in such a record's shape distinguishes a mislabelled stub
    from a complete declaration, it is accepted at both releases, and inventing
    a refusal for it at the major that no deprecation code warns about now would
    be the unphased narrowing this whole packet exists to prevent.
    """
    if not isinstance(consumer, dict) or consumer.get("instantiation_stub") is not True:
        return False
    return not any(member in consumer for member in CONSUMER_IDENTIFIERS)


def _issuance_precondition_findings(rid: str, req: dict) -> list[str]:
    """The closed issuance-precondition vocabulary, on BOTH failure shapes.

    An out-of-vocabulary member and a member valued `false` are the same
    defect wearing two faces: a record that reads as governance while binding
    the mint surface to nothing. Both raise the same code, and the message
    NAMES the closed set so a domain refused here knows where to go.
    """
    preconditions = req.get("issuance_preconditions")
    if not isinstance(preconditions, dict):
        return []
    out: list[str] = []
    # `key=repr` — THE SWEEP, not the one instance a bot round happened to land
    # on. The crash class Codex found on `requirement_ref` is a property of
    # sorting record-controlled keys, and this validator sorts them in three
    # places; a settled fact is chased to the whole file rather than to the line
    # that was pointed at. A non-string key here is already a SCHEMA error
    # (`issuance_preconditions` is closed), but the semantic pass runs beside
    # the schema pass rather than behind it, so the crash was reachable.
    for name in sorted(preconditions, key=repr):
        if name not in ISSUANCE_PRECONDITIONS:
            out.append(f"issuance-precondition-unknown: requirement {rid!r} declares issuance "
                       f"precondition {name!r}, which is outside the closed vocabulary "
                       f"{sorted(ISSUANCE_PRECONDITIONS)}; grow the vocabulary through the "
                       f"credential-contracts capability rather than declaring a local token "
                       f"the mint surface cannot adjudicate")
        elif preconditions[name] is not True:
            out.append(f"issuance-precondition-unknown: requirement {rid!r} declares issuance "
                       f"precondition {name!r} valued {preconditions[name]!r}; every member of "
                       f"{sorted(ISSUANCE_PRECONDITIONS)} is declared TRUE or not declared at "
                       f"all — a false-valued precondition reads as governance while asserting "
                       f"nothing, so omit it instead")
    return out


# --------------------------- requirement resolution ---------------------------

def requirements_index(documents: dict[str, dict]) -> dict[str, list[dict]]:
    """`{repository-relative path: [requirement records]}` for the tree scanned.

    ONLY records this validator itself discovered AND schema-checked go in, and
    the resolver NEVER OPENS A PATH TAKEN FROM A RECORD: a reference is matched
    against this index by string, so a record cannot steer the validator at a
    file of its choosing.
    """
    index: dict[str, list[dict]] = {}
    for rel, doc in documents.items():
        if not isinstance(doc, dict) or doc.get("kind") != "xfactory_credential_requirements":
            continue
        reqs = [r for r in _sequence(doc.get("requirements")) if isinstance(r, dict)]
        index[rel] = reqs
    return index


def resolve_requirement(ref: object, index: dict[str, list[dict]]) -> tuple[str, dict | None]:
    """Resolve a QUALIFIED requirement reference. Returns `(status, record)`.

    Statuses: `ok`, `malformed` (not the two-member object), `ungrammatical`
    (the document reference fails the path grammar), `not-found` (zero matches),
    `ambiguous` (more than one). ZERO and MORE-THAN-ONE both report and withhold
    — never pass silently, never disambiguate by picking one: requirement ids
    carry no repository-wide uniqueness, two matches may differ in `access_mode`,
    and a rule whose outcome depends on traversal order is not a rule.
    """
    if not isinstance(ref, dict) or set(ref) != set(REQUIREMENT_REF_MEMBERS):
        # AN EXTRA MEMBER IS MALFORMED, not a decorated success (PR #516,
        # Copilot). The docstring promised "the two-member object" while the
        # code checked only that the two were present, so a reference carrying
        # a third key could still resolve and satisfy the lift — accepting a
        # shape the major's closed block refuses. Refusing to RESOLVE it is not
        # a new refusal of any record: it withholds an exemption, and the
        # default shared-secret refusal it leaves standing is the one that
        # already stands today.
        #
        # COMPARED AS SETS, NEVER SORTED (PR #516, Codex round 2). The block is
        # UNCONSTRAINED at this minor, so a record may hold a mapping whose keys
        # are not all strings — YAML writes `1: extra` as an int key — and
        # `sorted()` over mixed types raises TypeError. That would abort the
        # whole repository scan on a record this release promises stays VALID
        # and warned. A crash is not a verdict.
        return "malformed", None
    rid = ref.get("requirement_id")
    doc_ref = ref.get("requirements_document_ref")
    if not isinstance(rid, str):
        return "malformed", None
    if not _is_document_ref(doc_ref):
        return "ungrammatical", None
    matches = [r for r in index.get(doc_ref, []) if r.get("id") == rid]
    if not matches:
        return "not-found", None
    if len(matches) > 1:
        return "ambiguous", None
    return "ok", matches[0]


def _readable_access_mode(record: dict) -> str | None:
    """The access mode, or None where it is UNREADABLE — absent, non-string, or
    outside the closed vocabulary. Unreadable means UNAVAILABLE and never
    "equal, and not dispatch-only": an entry that cannot answer the question is
    not a matching entry, which is the fail-open rule this estate already
    learned from a drift check that skipped the byte comparison on an absent
    field."""
    mode = record.get("access_mode")
    if not isinstance(mode, str) or mode not in ACCESS_MODES:
        return None
    return mode


# The lift's conditions, named so a mutation round can address them one at a
# time and so a refusal message can say WHICH condition stood.
LIFT_CONDITIONS = ("c1-consumer-declared", "c2-holders-differ", "c3-fetch-identities-differ",
                   "c4-both-acknowledge", "c5-requirement-resolves", "c6-reference-names-its-key")


def _lift_refusal_detail(first: tuple[str, dict], second: tuple[str, dict],
                         index: dict[str, list[dict]]) -> tuple[str | None, str | None]:
    """The SIX-condition lift over ONE pair. Returns `(None, None)` when the pair
    lifts, otherwise `(condition, reason)` for the FIRST condition that stood.

    EVERY CONDITION FAILS CLOSED, and the sixth — the reference names its own
    binding — is what makes the other five mean anything: a precondition an
    author can satisfy by choosing where to point is not a precondition. A
    security seat proved that by execution, granting the lift to this
    capability's only red proof of serving-tier separation with its shared
    secret byte-untouched and four declarations added.
    """
    (name_a, binding_a), (name_b, binding_b) = first, second
    con_a, con_b = _consumer(binding_a), _consumer(binding_b)

    # 1. both declare a consumer block
    for name, con in ((name_a, con_a), (name_b, con_b)):
        if not isinstance(con, dict):
            return "c1-consumer-declared", f"binding {name!r} declares no consumer block"

    # 2. holder references differ — AND ARE IDENTITIES AT ALL.
    #
    # THE GRAMMAR GUARD IS A LIFT CONDITION, NOT A TIDINESS (PR #516, Codex P1).
    # A pair carrying `<holder-a>`/`<holder-b>` and `<fetch-a>`/`<fetch-b>` is
    # DISTINCT as strings while naming nobody, and with the acknowledgment and
    # two resolvable non-dispatch requirements it took the lift — REMOVING a
    # `shared-secret-identity` error that stands today. This change tightens
    # before it lifts, and nothing that is refused today may become accepted by
    # silence; a placeholder is exactly the "grammar-passing sentinel" the
    # packet calls worse than omission, arriving through the exemption door.
    # Withholding the lift is safe in the phasing direction too: the record it
    # refuses is one the current major already refuses.
    holder_a, holder_b = con_a.get("holder_ref"), con_b.get("holder_ref")
    for name, holder in ((name_a, holder_a), (name_b, holder_b)):
        if not _is_identifier(holder):
            return ("c2-holders-differ",
                    f"binding {name!r}'s holder_ref is {holder!r}, which is not an identifier "
                    f"({IDENTIFIER.pattern}) — a value that names nobody establishes no consumer, "
                    f"however distinct it is from the other one")
    if holder_a == holder_b:
        return ("c2-holders-differ",
                f"both bindings declare holder_ref {holder_a!r} — one system wearing two hats")

    # 3. fetch identities differ, and are identities
    fetch_a, fetch_b = con_a.get("fetch_identity"), con_b.get("fetch_identity")
    for name, fetch in ((name_a, fetch_a), (name_b, fetch_b)):
        if not _is_identifier(fetch):
            return ("c3-fetch-identities-differ",
                    f"binding {name!r}'s fetch_identity is {fetch!r}, which is not an identifier "
                    f"({IDENTIFIER.pattern}), so the per-system authority is unproven")
    if fetch_a == fetch_b:
        return ("c3-fetch-identities-differ",
                f"both bindings fetch with {fetch_a!r} — one identity MAY be shared, "
                f"one AUTHORITY SHALL NOT")

    # 4. both acknowledge the sharing
    for name, con in ((name_a, con_a), (name_b, con_b)):
        if con.get("shared_credential_acknowledged") is not True:
            return ("c4-both-acknowledge",
                    f"binding {name!r} does not declare shared_credential_acknowledged: true — "
                    f"a one-sided declaration exempts a pair on one party's word")

    # 5/6. the qualified reference resolves to exactly one readable requirement,
    #      and it names the binding it sits on
    modes: list[str] = []
    for name, con in ((name_a, con_a), (name_b, con_b)):
        ref = con.get("requirement_ref")
        status, record = resolve_requirement(ref, index)
        if status != "ok":
            detail = {
                "malformed": "is not a qualified reference (requirement_id + "
                             "requirements_document_ref)",
                "ungrammatical": "names a document reference that is absolute, escaping, or "
                                 "foreign-repository",
                "not-found": "resolves to no requirement in the repository under validation",
                "ambiguous": "resolves to MORE THAN ONE requirement, which may differ in "
                             "access_mode",
            }[status]
            return "c5-requirement-resolves", f"binding {name!r}'s requirement_ref {detail}"
        if ref.get("requirement_id") != name:
            return ("c6-reference-names-its-key",
                    f"binding {name!r}'s requirement_ref names "
                    f"{ref.get('requirement_id')!r}, not its own map key — a condition the "
                    f"author satisfies by choosing where to point is no condition at all")
        mode = _readable_access_mode(record)
        if mode is None:
            return ("c5-requirement-resolves",
                    f"binding {name!r}'s resolved requirement carries an access_mode that is "
                    f"absent, non-string, or outside {list(ACCESS_MODES)} — unreadable makes "
                    f"the lift UNAVAILABLE, never satisfied")
        modes.append(mode)

    if modes[0] != modes[1]:
        return ("c5-requirement-resolves",
                f"the resolved access modes differ ({modes[0]!r} vs {modes[1]!r}) — a dispatch "
                f"and a content credential do not become one credential by declaration")
    if modes[0] == "dispatch_only":
        return ("c5-requirement-resolves",
                "both resolved requirements are dispatch_only — the serving tier would hold key "
                "material capable of minting a content-write token, and no acknowledgment makes "
                "that intentional")
    return None, None


def _lift_refusal(first: tuple[str, dict], second: tuple[str, dict],
                  index: dict[str, list[dict]]) -> str | None:
    """The reason the default refusal stands for this pair, or None if it lifts."""
    return _lift_refusal_detail(first, second, index)[1]


def _binding_findings(doc: dict, index: dict[str, list[dict]]) -> list[str]:
    """Errors over one binding template: the baked-secret screen, the every-pair
    shared-secret refusal with its six-condition lift, and the distinct
    shared-authority finding."""
    out: list[str] = []
    bindings = [(n, b) for n, b in _mapping(doc.get("credential_bindings")).items()
                if isinstance(b, dict)]

    # THE SCREEN, over THREE sinks rather than one. `secret_ref` was the only
    # free string read before add-binding-consumer-identity; the block adds two
    # more on the one record kind whose invariant is "never bake a secret".
    for name, binding in bindings:
        consumer = _consumer(binding)
        sinks = [("secret_ref", binding.get("secret_ref"))]
        if isinstance(consumer, dict):
            sinks += [(f"consumer.{m}", consumer.get(m)) for m in CONSUMER_IDENTIFIERS]
        for field, value in sinks:
            if isinstance(value, str) and _looks_like_raw_secret(value):
                out.append(f"baked-secret: binding {name!r} {field} is a raw secret value, not a "
                           f"vault reference; credentials are delivered by reference, never baked")

    # THE DISTINCT FAULT, and it is NOT scoped to a shared secret_ref: two
    # different holders declaring one fetch identity is the authority collapse
    # whatever their secret references, and scoping the finding to the proxy
    # would leave it unreported when two spellings name one secret. One holder
    # reusing its OWN fetch identity across its OWN bindings is not the fault.
    #
    # IT COMPARES ONLY VALUES THAT PASS THE IDENTIFIER GRAMMAR, and that guard
    # is load-bearing rather than tidy (PR #516, Codex P1). This is the one arm
    # of this change that can raise a NEW error on a record carrying no shared
    # secret, so it is also the one place a malformed value could turn a
    # deprecation into a refusal: two bindings whose consumers both carry
    # `fetch_identity: ""` validate today, and reading them as "the same
    # identity" would refuse in a minor a shape the current major accepts —
    # exactly the narrowing the whole packet phases. A malformed identity is
    # WARNED by `consumer-member-grammar` for the whole of this minor and
    # refused at the major, at which point the record is gone anyway.
    authority_pairs: set[tuple[str, str]] = set()
    for (name_a, binding_a), (name_b, binding_b) in combinations(bindings, 2):
        con_a, con_b = _consumer(binding_a), _consumer(binding_b)
        if not (isinstance(con_a, dict) and isinstance(con_b, dict)):
            continue
        holder_a, holder_b = con_a.get("holder_ref"), con_b.get("holder_ref")
        fetch_a, fetch_b = con_a.get("fetch_identity"), con_b.get("fetch_identity")
        if not all(_is_identifier(v) for v in (holder_a, holder_b, fetch_a, fetch_b)):
            continue
        if holder_a != holder_b and fetch_a == fetch_b:
            authority_pairs.add((name_a, name_b))
            out.append(f"shared-authority-identity: bindings {name_a!r} ({holder_a!r}) and "
                       f"{name_b!r} ({holder_b!r}) are two systems authenticating as "
                       f"{fetch_a!r}; one identity MAY be shared, one AUTHORITY SHALL NOT — "
                       f"give each consuming system its own fetch identity, its own grant and "
                       f"its own audit trail")

    # THE DEFAULT REFUSAL, over EVERY PAIR sharing a secret reference. The
    # inherited shape kept the FIRST binding per secret and compared later ones
    # against it, so with three bindings the pair (b, c) was never examined and
    # a record where those two shared a fetch identity shipped the authority
    # collapse and was accepted. That shape is REPLACED, not extended.
    by_secret: dict[str, list[tuple[str, dict]]] = {}
    for name, binding in bindings:
        ref = binding.get("secret_ref")
        if isinstance(ref, str):
            by_secret.setdefault(ref, []).append((name, binding))
    for ref, sharers in by_secret.items():
        if len(sharers) < 2:
            continue
        for first, second in combinations(sharers, 2):
            if (first[0], second[0]) in authority_pairs:
                continue  # one fault, one finding: the named fault replaces the default
            reason = _lift_refusal(first, second, index)
            if reason is None:
                continue
            out.append(f"shared-secret-identity: bindings {first[0]!r} and {second[0]!r} share "
                       f"secret_ref {ref!r}; dispatch and content credentials must be distinct "
                       f"bindings so the serving tier holds no content-write key material. The "
                       f"two-consumer lift is UNAVAILABLE here: {reason}")
    return out


def _semantic_findings(doc: dict, index: dict[str, list[dict]] | None = None) -> list[str]:
    """Dispatch-credential invariants the shape schema cannot express, plus the
    closed issuance-precondition vocabulary and the consumer-identity refusals.
    Returns `code: message` strings (empty when the record conforms)."""
    kind = doc.get("kind")
    out: list[str] = []
    if kind == "xfactory_credential_requirements":
        for req in _sequence(doc.get("requirements")):
            if not isinstance(req, dict):
                continue
            rid = req.get("id", "<?>")
            out.extend(_issuance_precondition_findings(rid, req))
            if req.get("access_mode") != "dispatch_only":
                continue
            bad = [s for s in _sequence(req.get("minimum_scopes")) if s not in DISPATCH_SCOPES]
            if bad:
                out.append(f"dispatch-scope-ceiling: requirement {rid!r} is dispatch_only but "
                           f"requests non-trigger scope(s) {bad}; a dispatch credential carries no "
                           f"contents authority (allowed: {sorted(DISPATCH_SCOPES)})")
            if len(_sequence(req.get("allowed_workflows"))) > 1:
                out.append(f"dispatch-one-workflow: requirement {rid!r} is dispatch_only but names "
                           f">1 allowed_workflow; a dispatch credential triggers exactly one")
    elif kind == "xfactory_credential_binding_template":
        out.extend(_binding_findings(doc, index or {}))
    return out


# --------------------------- the deprecation channel ---------------------------

def _consumer_block_warnings(name: str, binding: dict) -> list[tuple[str, str]]:
    """The block's own five codes, over ONE binding. Every one names a shape the
    major REFUSES and this minor accepts, which is the only test for whether an
    act phases — not where the refusal happens to be written."""
    out: list[tuple[str, str]] = []
    consumer = _consumer(binding)
    stub = _declares_stub(consumer)

    if consumer is None:
        return [("consumer-identity-undeclared",
                 f"binding {name!r} declares no consumer block, so which system holds it and "
                 f"what it fetches with are asserted by the estate's wiring rather than read "
                 f"from the record; declare `consumer: {{holder_ref, fetch_identity}}` — or "
                 f"`instantiation_stub: true` if this record is a stub. ERROR at "
                 f"{MAJOR_RELEASE}")]

    if not isinstance(consumer, dict):
        return [("consumer-block-incomplete",
                 f"binding {name!r} carries a consumer value that is not an object "
                 f"({type(consumer).__name__}); it stays VALID at this minor because the schema "
                 f"constrains nothing about the block, and is an ERROR at {MAJOR_RELEASE}")]

    if not stub:
        missing = [m for m in CONSUMER_IDENTIFIERS if m not in consumer]
        if missing:
            out.append(("consumer-block-incomplete",
                        f"binding {name!r} declares a consumer block that omits "
                        f"{', '.join(missing)}; a block present but incomplete matches neither "
                        f"the no-block nor the unknown-member finding, and would otherwise cross "
                        f"the whole minor unwarned. ERROR at {MAJOR_RELEASE}"))

    # `key=repr` for the same reason the reference is compared as a set: an
    # unconstrained block may carry non-string member keys, and a bare
    # `sorted()` over mixed types raises rather than reports.
    unknown = [m for m in consumer if m not in CONSUMER_MEMBERS]
    if unknown:
        out.append(("consumer-block-unknown-member",
                    f"binding {name!r}'s consumer block declares "
                    f"{sorted(unknown, key=repr)}, outside the "
                    f"declared member set {list(CONSUMER_MEMBERS)}; the block is closed at "
                    f"{MAJOR_RELEASE}, where this is an ERROR"))

    for member in CONSUMER_IDENTIFIERS:
        if member in consumer and not _is_identifier(consumer[member]):
            out.append(("consumer-member-grammar",
                        f"binding {name!r}'s consumer.{member} is {consumer[member]!r}, outside "
                        f"the identifier grammar {IDENTIFIER.pattern} (1–{IDENTIFIER_MAX} "
                        f"characters). A grammar-passing SENTINEL is not the repair — it reads "
                        f"as an authority declaration while naming nothing; a stub declares "
                        f"`instantiation_stub: true` instead. ERROR at {MAJOR_RELEASE}"))

    # MEMBERSHIP, NOT TRUTHINESS (PR #516, Codex P2). `requirement_ref: null` is
    # a DECLARED member whose value is not an object, and the major refuses it;
    # `.get()` made it indistinguishable from an absent optional member, so the
    # shape crossed the deprecation release in silence. The test is whether the
    # key is there.
    if "requirement_ref" in consumer:
        ref = consumer["requirement_ref"]
        if not isinstance(ref, dict) or set(ref) != set(REQUIREMENT_REF_MEMBERS):
            out.append(("consumer-member-grammar",
                        f"binding {name!r}'s consumer.requirement_ref is not a QUALIFIED "
                        f"reference — an object of exactly {list(REQUIREMENT_REF_MEMBERS)}. A "
                        f"bare id resolves ambiguously, because a requirement id carries no "
                        f"repository-wide uniqueness in the tree this validator scans. ERROR at "
                        f"{MAJOR_RELEASE}"))
        else:
            if not _is_identifier(ref.get("requirement_id")):
                out.append(("consumer-member-grammar",
                            f"binding {name!r}'s consumer.requirement_ref.requirement_id is "
                            f"{ref.get('requirement_id')!r}, outside the identifier grammar "
                            f"{IDENTIFIER.pattern}. ERROR at {MAJOR_RELEASE}"))
            doc_ref = ref.get("requirements_document_ref")
            if not _is_document_ref(doc_ref):
                out.append(("consumer-requirement-ref-grammar",
                            f"binding {name!r}'s consumer.requirement_ref."
                            f"requirements_document_ref is {doc_ref!r}, which is not a "
                            f"repository-relative YAML path of at most {DOCUMENT_REF_MAX} "
                            f"characters: no leading '/', no '..' segment, no "
                            f"foreign-repository prefix, and a .yaml/.yml suffix. It is inherited "
                            f"as an unconstrained string that nothing resolved; promoting it to a "
                            f"resolution input feeding a security precondition without a grammar "
                            f"would rest that precondition on an unenforced convention. ERROR at "
                            f"{MAJOR_RELEASE}"))

    for token in CONST_TRUE_TOKENS:
        if token in consumer and consumer[token] is not True:
            out.append(("consumer-token-not-true",
                        f"binding {name!r}'s consumer.{token} is {consumer[token]!r}; the token "
                        f"is DECLARED or ABSENT and `false` is not a second meaning — it reads "
                        f"as governance while asserting nothing. It stays VALID at this minor "
                        f"because such a record validates on the current major, and is an ERROR "
                        f"at {MAJOR_RELEASE}. The two-consumer lift is withheld from a "
                        f"false-valued acknowledgment at BOTH releases: declining an exemption "
                        f"is not refusing a record"))
    return out


def _deprecation_warnings(doc: dict) -> list[tuple[str, str]]:
    """The EIGHT `consumer-*` codes, over one document. Warnings never redden a
    verdict; they are the deprecation release the major's refusals depend on,
    and the set is derived from the list of things the major refuses — a shape
    that no code names is a shape the deprecation does not serve."""
    kind = doc.get("kind")
    out: list[tuple[str, str]] = []
    if kind == "xfactory_credential_requirements":
        for req in _sequence(doc.get("requirements")):
            if not isinstance(req, dict):
                continue
            mode = req.get("access_mode")
            if not isinstance(mode, str) or mode not in ACCESS_MODES:
                out.append(("consumer-access-mode-vocabulary",
                            f"requirement {req.get('id', '<?>')!r} declares access_mode "
                            f"{mode!r}, outside the declared vocabulary {list(ACCESS_MODES)}. "
                            f"The field is an unconstrained string on this major and one line of "
                            f"code compares it to one exact spelling, so a variant spelling "
                            f"compares equal to itself; the two-consumer lift already treats an "
                            f"unreadable mode as UNAVAILABLE, and the `enum` lands at "
                            f"{MAJOR_RELEASE}"))
    elif kind == "xfactory_credential_binding_template":
        for name, binding in _mapping(doc.get("credential_bindings")).items():
            if not _is_identifier(name):
                out.append(("consumer-binding-key-grammar",
                            f"credential_bindings key {name!r} is outside the identifier grammar "
                            f"{IDENTIFIER.pattern} (1–{IDENTIFIER_MAX} characters). The map "
                            f"accepts arbitrary keys on this major, so the grammar is a "
                            f"narrowing like any other and is not exempt for sitting outside the "
                            f"block; the lift's binding-link condition still holds here because "
                            f"it compares the reference's id to the key as a STRING. ERROR at "
                            f"{MAJOR_RELEASE}"))
            if isinstance(binding, dict):
                out.extend(_consumer_block_warnings(name, binding))
    return out


# --------------------------- the packaged corpus ---------------------------

def _corpus_documents() -> dict[str, list[Path]]:
    """The four channels of `examples/credential-contracts/`. `warning/` and
    `support/` are add-binding-consumer-identity's: a warning fixture placed
    among the positives failed the self-test as "unexpectedly invalid" and one
    placed in `negative/` failed it as "has no registered expectation", so a
    deprecation the major depends on had no place to hold its proof. `support/`
    holds records the validator INDEXES for reference resolution and adjudicates
    for nothing — a reference needs something to resolve AT."""
    return {
        "positive": sorted(EXAMPLES_DIR.glob("*.example.yaml")),
        "negative": sorted((EXAMPLES_DIR / "negative").glob("*.yaml"))
        if (EXAMPLES_DIR / "negative").is_dir() else [],
        "warning": sorted((EXAMPLES_DIR / "warning").glob("*.yaml"))
        if (EXAMPLES_DIR / "warning").is_dir() else [],
        "support": sorted((EXAMPLES_DIR / "support").glob("*.yaml"))
        if (EXAMPLES_DIR / "support").is_dir() else [],
    }


def _self_test(validator: Draft202012Validator) -> int:
    """Packaged examples: positives are schema-valid with no semantic finding AND
    no deprecation warning; each negative raises its intended semantic code; each
    warning fixture raises its intended deprecation code and NO error. Returns
    the error count."""
    if not EXAMPLES_DIR.is_dir():
        print(f"ERROR self-test: {EXAMPLES_DIR} not found")
        return 1
    errs = 0
    channels = _corpus_documents()
    docs: dict[str, dict] = {}
    for paths in channels.values():
        for path in paths:
            loaded = yaml.safe_load(path.read_text())
            if isinstance(loaded, dict):
                docs[str(path.relative_to(EXAMPLES_DIR))] = loaded
    # In the self-test the corpus directory stands in for the repository root,
    # so a fixture's `requirements_document_ref` is relative to it.
    index = requirements_index({rel: doc for rel, doc in docs.items()
                                if not list(validator.iter_errors(doc))})

    for path in channels["positive"]:
        doc = docs[str(path.relative_to(EXAMPLES_DIR))]
        problems = ([e.message for e in validator.iter_errors(doc)]
                    + _semantic_findings(doc, index)
                    + [f"WARN [{c}] {m}" for c, m in _deprecation_warnings(doc)])
        if problems:
            print(f"ERROR self-test: positive {path.name} unexpectedly invalid: {problems}")
            errs += 1

    for path in channels["negative"]:
        want = NEGATIVE_EXPECTATIONS.get(path.name)
        findings = _semantic_findings(docs[str(path.relative_to(EXAMPLES_DIR))], index)
        if not want:
            print(f"ERROR self-test: negative {path.name} has no registered expectation")
            errs += 1
        elif not any(f.startswith(want) for f in findings):
            print(f"ERROR self-test: negative {path.name} did not raise {want!r} (got {findings})")
            errs += 1

    for path in channels["warning"]:
        rel = str(path.relative_to(EXAMPLES_DIR))
        want = WARNING_EXPECTATIONS.get(path.name)
        doc = docs[rel]
        codes = [c for c, _ in _deprecation_warnings(doc)]
        errors = _semantic_findings(doc, index)
        if not want:
            print(f"ERROR self-test: warning {path.name} has no registered expectation")
            errs += 1
        elif want not in codes:
            print(f"ERROR self-test: warning {path.name} did not warn {want!r} (got {codes})")
            errs += 1
        if errors:
            print(f"ERROR self-test: warning {path.name} raised an ERROR ({errors}); a fixture "
                  f"that is refused belongs in negative/, not warning/")
            errs += 1
        if list(validator.iter_errors(doc)):
            print(f"ERROR self-test: warning {path.name} is schema-INVALID; every shape this "
                  f"channel probes stays VALID at this minor, which is the whole point of the "
                  f"phasing")
            errs += 1

    for path in channels["support"]:
        doc = docs[str(path.relative_to(EXAMPLES_DIR))]
        schema_errs = [e.message for e in validator.iter_errors(doc)]
        if schema_errs:
            print(f"ERROR self-test: support {path.name} is schema-INVALID: {schema_errs}; a "
                  f"record the resolver indexes must be one the resolver would have accepted")
            errs += 1

    # ONE REGISTERED PROBE PER WARNING CODE, CHECKED BY COUNT AGAINST THE CODE
    # LIST ITSELF — so the next code added cannot silently ship unprobed. A
    # corpus that probes SOME of the codes is worse than one that probes none,
    # because the major's preconditions then LOOK evidenced.
    probed = set(WARNING_EXPECTATIONS.values())
    unprobed = [c for c in DEPRECATION_CODES if c not in probed]
    if unprobed:
        print(f"ERROR self-test: deprecation code(s) {unprobed} carry no packaged probe; a "
              f"deprecation the major depends on cannot be evidenced by a corpus with no place "
              f"to hold its proof")
        errs += 1
    stray = [c for c in probed if c not in DEPRECATION_CODES]
    if stray:
        print(f"ERROR self-test: warning expectation(s) {sorted(stray)} name no declared "
              f"deprecation code")
        errs += 1

    if errs == 0:
        print(f"self-test: {len(channels['positive'])} positive + "
              f"{len(channels['negative'])} negative + {len(channels['warning'])} warning "
              f"example(s) confirmed, {len(DEPRECATION_CODES)} deprecation code(s) probed")
    return errs


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    repo = Path(sys.argv[1]).resolve()
    validator = Draft202012Validator(yaml.safe_load(SCHEMA.read_text()))
    errors = _self_test(validator)
    warnings: list[str] = []
    skipped = checked = 0

    cred = repo / "credentials"
    files = sorted(cred.rglob("*.y*ml")) if cred.is_dir() else []

    # PASS ONE: parse, envelope-check, and index the requirement records this
    # validator itself discovered and schema-checked. A qualified reference
    # resolves against THIS index and nothing else; the validator never opens a
    # path a record supplies.
    parsed: list[tuple[str, dict]] = []
    for f in files:
        rel = str(f.relative_to(repo))
        try:
            doc = yaml.safe_load(f.read_text())
        except yaml.YAMLError as exc:
            print(f"ERROR {rel}: YAML parse failure: {exc}")
            errors += 1
            continue
        if not isinstance(doc, dict):
            continue
        kind = doc.get("kind")
        if kind is None:
            print(f"ERROR {rel}: missing schema_version/kind envelope")
            errors += 1
            continue
        if kind not in KINDS:
            print(f"skip  {rel}: kind {kind!r} is not a credential contract (out of scope)")
            skipped += 1
            continue
        parsed.append((rel, doc))
    index = requirements_index({rel: doc for rel, doc in parsed
                                if not list(validator.iter_errors(doc))})

    # PASS TWO: adjudicate.
    for rel, doc in parsed:
        checked += 1
        # `repr` per path element: a record with non-string mapping keys
        # (`1: foo`) produces error paths that mix ints and strings at one
        # position, and a bare sort over those raises — turning a SCHEMA
        # ERROR into a crash (PR #516, Copilot).
        for err in sorted(validator.iter_errors(doc),
                          key=lambda e: [repr(p) for p in e.absolute_path]):
            loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
            # oneOf noise: report the sub-errors that are not kind mismatches
            if err.validator == "oneOf":
                msgs = sorted({e.message for e in err.context
                               if "const" not in e.message})
                for m in msgs[:3] or [err.message]:
                    print(f"ERROR {rel}: {loc}: {m}")
                    errors += 1
                continue
            print(f"ERROR {rel}: {loc}: {err.message}")
            errors += 1
        for code, msg in _deprecation_warnings(doc):
            warnings.append(f"WARN  [{code}] {rel}: {msg}")
        for msg in _semantic_findings(doc, index):
            print(f"ERROR {rel}: {msg}")
            errors += 1

    for line in warnings:
        print(line)

    verdict = "PASS" if errors == 0 else "FAIL"
    print(f"\n{repo.name}: {checked} contract(s) checked, {skipped} skipped, "
          f"{len(warnings)} warning(s), {errors} error(s) -> {verdict}")
    raise SystemExit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()
