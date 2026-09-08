#!/usr/bin/env python3
"""Validate the identity-brokering contract family (add-identity-brokering).

The openxFactory-owned canonical validator for the six kinds of
`contracts/identity-brokering/`. Run from the pinned openxFactory checkout,
never copied into a domain repo:

    python3 scripts/validate-identity-brokering.py [REPO_PATH] [--strict]

Two layers run:

1. Packaged reference corpus (`contracts/identity-brokering/examples/`): every
   `*.example.yaml` must pass schema conformance AND every cross-shape rule;
   every file under `negative/` must FAIL for its INTENDED reason, declared in
   its own first lines as `# expected_failure: <code>` with an optional
   `# expected_failure_detail: <substring>` pin and a required
   `# requirement: <REQ-ID>` attribution. The detail pin matters because
   several cases would otherwise collapse into a generic `schema` finding and
   stop testing the invariant they are named for.

   Coverage is closed in both directions: every requirement in REQUIREMENTS
   must carry at least one negative confirmation, and every requirement id a
   fixture claims must exist. A requirement cannot quietly lose its probe.

2. Optional real artifacts under REPO_PATH: every `*.y*ml` whose `kind` is one
   of the family kinds is validated. Other kinds are skipped and counted; the
   packaged corpus is excluded so a whole-repo sweep does not re-adjudicate the
   negatives as though they were live records, and cross-record references
   resolve against the scanned repo's OWN records — a teaching fixture must not
   resolve a live reference.

The rules the shapes cannot express:

  (a) THE PROPERTY SET IS A CLOSED ALLOW-LIST, AT EVERY DEPTH, DERIVED FROM
      THE SCHEMA. Every property path in a document is checked against the
      names its schema declares — an ALLOW-LIST computed from the contract,
      never a denylist of forbidden names, because a denylist admits every
      field nobody thought to forbid (design D2's named risk). On
      `persona_assertion` and `broker_organization` — the two shapes the
      never-mirror rule governs — an unrecognized property is additionally
      reported as `never-mirror-property`: those are the records where a
      role, group, grant, project, stack, layer or tenancy projection would
      arrive, and the mirror grows one convenient field at a time (spec R3).

  (b) ONE PERSONA PER HUMAN PER BROKER INSTANCE. Two personas in one instance
      sharing a federated upstream identity are the same human twice, which
      is the outcome the whole capability exists to prevent. The federated
      identity is the only evidence of sameness the broker actually has, so it
      is what this keys on — NORMALIZED (NFKC, stripped, case folded) on all
      three components, because sameness a trailing space or a case change
      defeats is not sameness (spec R1).

  (c) A LINK OR MERGE NAMES WHO ACTED, AND A MERGE KEEPS EVERY PRIOR SUBJECT
      RESOLVABLE. A record naming neither an initiating human nor an approving
      administrator is not an established link; a merge that drops a prior
      subject identifier silently orphans every record already written against
      it; a self link is initiated FROM the persona it adds to AND BY that
      persona (the two initiator fields cannot disagree); a merge is NOT
      APPROVED BY ONE OF ITS OWN PARTIES; and the legal bases are READ OUT OF
      THE SCHEMA at run time rather than restated here, so an attribute-match
      basis is refused by the contract rather than by a second list that could
      drift from it (spec R4, design D4).

  (d) THE IDENTIFIER POSITION HOLDS AN OPAQUE SUBJECT AND NOTHING ELSE. No
      display name — compared on the ALPHANUMERIC SKELETON, so removing the
      spaces and the punctuation does not make a name an opaque subject — no
      email address, no upstream account name. Provenance is never
      `broker_asserted` for a bare username: a username the corpus records as
      PRE-BROKER, presented as a broker-asserted persona, is the exact
      substitution the requirement refuses. And a MAPPING RESOLVES TO A
      BROKER-ISSUED SUBJECT: a mapping whose target is its own
      `mapped_from_username`, or any bare username the corpus records as
      pre-broker, has resolved nothing and only made the substitution look
      adjudicated — history is marked at the boundary date and mapped on
      demand, never asserted (spec R5, OQ-1/OQ-3).

  (e) NOTHING SECRET-SHAPED, BY CLASS, ANYWHERE. The schemas close every
      object so no secret-shaped PROPERTY can be added, but a conformant shape
      can still carry a pasted secret inside a string field that legitimately
      exists — a configuration export dropped into a free-text reason, for
      instance. This walks names AND values, REASSEMBLES ADJACENT CHUNKS (a
      value split across array items or sibling fields is joined and re-tested)
      and tests each string WITH ITS WHITESPACE COLLAPSED (a wrapped or
      deliberately spaced-out export splits the secret inside ONE value, which
      neither a per-value regex nor cross-field reassembly spans), so a secret
      cannot be smuggled through in pieces. A configuration export used as
      reviewed state is credential-free by construction, never by redaction
      after the fact (spec R7).

  (f) A WRITE ACTION REQUIRES A RESOLVED AUTHORIZATION DECISION. A surface
      offering a governed write action declares `resolved_authorization` AND
      names its governed decision point; the decision resolves in the governed
      layer, never in broker membership. NAMING a write action IS offering one,
      so a populated `actions` list beside `offered: false` is refused — that
      combination is the quiet transition already half-made. And because
      `resolves_in` is a closed enumeration while the refs beside it are free
      text, the DECISION-POINT LOCATOR is walked by shape too: a record
      declaring `governed_layer` and then naming the broker's own
      administration API is the same substitution the enumeration refuses,
      moved one field to the left. The quiet failure this closes is a surface
      shipping read-only under "any authenticated persona" and then gaining a
      write action before per-action authorization exists (spec R9, design D9).

  (g) AN ADOPTION RETIRES THE SECRET IT REPLACES. Naming a replaced shared
      credential and leaving it live means the adoption added an
      authentication path instead of removing one, and the credential
      inventory grew by the adoption it was supposed to shrink (spec R7).

  (h) ONE POINTER, NEVER A PROJECTION. An organization carries AT MOST ONE
      reference to the governed record it corresponds to, and that reference
      resolves in the governed layer. The bound is in the schema; this reports
      a second reference under its own code so the refusal names the rule
      rather than an array length (spec R2, R3, design D2).

  (i) WORKLOADS ARE NOT PERSONAS. A declared broker service client may not
      appear as a persona subject, nor as the actor of a governed record, nor
      hold an organization membership as authority. Non-human authority stays
      on `credential-contracts` grants and `openxwallet` holders — the wallet
      family is CONSUMED at `contracts/openxwallet-pin.yaml` from
      `contract-v2.0` and published by `opensoft/openXwallet`, so the ratified
      rule is unchanged and only its publisher moved — which are
      strictly stronger than a user row; a second, weaker vocabulary next to
      them would win by convenience (spec R6, design D5).

  (j) ISOLATION ESCALATES BY INSTANCE, AND THE CO-RESIDENCE ANSWER IS RECORDED
      EITHER WAY. A restricted population is served by a DEDICATED instance; an
      adoption declaring the restriction while naming a shared instance is
      partitioning personas inside a shared deployment, which pays the full
      fragmentation cost for weaker isolation. BOTH answers carry a
      `restriction_ref`: the commitment that imposes the restriction, or the
      written finding that there is none — an unrecorded negative is
      indistinguishable from an unasked question, which is the OQ-5 finding's
      own rule applied to its own output. The contract stays silent on instance
      count, so a dedicated instance with no restriction at all is conformant
      and is refused by nothing (spec R8, design D3).

  (k) MEMBERSHIP IS ASSOCIATION, AND COMPANY ROLES ARE THE RATIFIED LAYER
      SPELLING. The canonical layer ids and the RESERVED layer terms are read
      out of `contracts/policies/layer-vocabulary.yaml` at run time; this
      family's bridge (`tenant` -> `tenant`, `served` -> `subject`) is checked
      against them, so a renamed canonical layer fails loudly here instead of
      drifting into a second spelling of the layer model (spec R2).

  (l) PERSONAS DO NOT SPAN INSTANCES. Every subject in a link record that
      resolves to a persona must resolve to one in the record's own instance.
      A merged-away subject legitimately resolves to nothing, which is why
      this fires on the resolved ones (spec R8).

  (m) NO SURFACE HOLDS HUMAN ACCOUNTS OF ITS OWN. An account the broker cannot
      resolve to a persona is an identity the governed layer cannot name
      (spec R1).

  (n) A MEMBERSHIP NAMES A DECLARED ORGANIZATION. The membership id was the
      one field on a persona assertion that points at another record and was
      never resolved, which made it the mirror's remaining doorway: a role, a
      grant, a project or a tenancy path carried as though it were a company.
      The schema pattern now refuses ':' and '/' in this position; this
      resolves what is left against the `broker_organization` records the scan
      actually sees. CORPUS-COUPLED, like (b), (i) and (l) — skipped entirely
      when a scan declares no organizations (spec R2, R3, R6).

WHAT THIS VALIDATOR DELIBERATELY DOES NOT DO

It creates no broker, realm, organization, credential, persona or deployment.
It cannot check that a declared authorization posture is actually resolved at
run time — a validator can check that a posture is declared and that a surface
with write actions declares the stronger one, and cannot check that the
resolution happens. That is the same honesty limit `openxwallet`'s declared
custody accepts (that family is consumed at `contracts/openxwallet-pin.yaml`
since `contract-v2.0`; the limit is the family's, not this repository's), and it is accepted here for the same reason: a declaration a
reader can audit beats an unstated assumption. Nor can it prove a free-text
field carries no secret; the value scan is a blocklist over the classes it
knows, so keeping secrets out of free text stays an obligation on consumers.

Rule (f)'s locator walk carries the same class of residue and by the same
argument: an OPAQUE decision-point ref (an internal id, a shortened URL, a
name that means nothing outside one team) that in fact resolves to broker
membership cannot be caught by shape at all. The blocklist catches the honest
mistake and the lazy shortcut; it does not catch a determined one. Rules (b),
(i), (l) and (n) are CORPUS-COUPLED: they resolve only against records in the
same scan, so a repository that splits its personas from its organizations
gets a weaker check than one that keeps them together. Every one of these is
recorded in the family README rather than left for a later reader to discover.

Exit codes: 0 ok, 1 findings, 2 harness error.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
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
FAMILY_DIR = ROOT / "contracts" / "identity-brokering"
EXAMPLES_DIR = FAMILY_DIR / "examples"
NEGATIVE_DIR = EXAMPLES_DIR / "negative"
LAYER_VOCABULARY_PATH = ROOT / "contracts" / "policies" / "layer-vocabulary.yaml"

KIND_TO_SCHEMA = {
    "persona_assertion": "persona-assertion.schema.yaml",
    "broker_organization": "broker-organization.schema.yaml",
    "actor_subject_reference": "actor-subject-reference.schema.yaml",
    "identity_link_record": "identity-link-record.schema.yaml",
    "broker_client_declaration": "broker-client-declaration.schema.yaml",
    "broker_surface_adoption": "surface-adoption.schema.yaml",
}

# The two shapes the never-mirror rule governs. An unrecognized property here
# is where a tenancy projection arrives, so it earns its own finding code.
NEVER_MIRROR_KINDS = {"persona_assertion", "broker_organization"}

# The identity field per indexed kind. A duplicated id is refused on every copy:
# index tables are last-write-wins, so a duplicate could swap the persona, the
# organization or the client a reference resolves to.
_ID_FIELDS = {
    "persona_assertion": "assertion_id",
    "broker_organization": "organization_id",
    "actor_subject_reference": "reference_id",
    "identity_link_record": "link_record_id",
    "broker_client_declaration": "client_id",
    "broker_surface_adoption": "adoption_id",
}

# This family's bridge from a COMPANY ROLE to a canonical Hermes LAYER. The
# layer ids and the reserved terms are read from the policy file at run time
# (rule k); only the bridge itself is contract content, and its targets are
# checked against the policy so a renamed layer fails loudly.
COMPANY_ROLE_TO_LAYER = {"tenant": "tenant", "served": "subject"}

# The closed requirement list the spec delta defines. Every one of these MUST
# carry at least one negative confirmation in the packaged corpus; that closure
# is what makes this a negative confirmation PER REQUIREMENT rather than a pile
# of negatives.
REQUIREMENTS: dict[str, str] = {
    "IDB-R1": "One persona per human within a broker instance",
    "IDB-R2": "Organizations realize company boundaries, on the persona",
    "IDB-R3": "The broker asserts identity and membership only",
    "IDB-R4": "Identities link explicitly or merge by decision, never silently",
    "IDB-R5": "A governed record binds its actor to a stable opaque subject",
    "IDB-R6": "Workloads are not personas",
    "IDB-R7": "Broker credentials are credential-contract records",
    "IDB-R8": "Isolation escalates by instance, never by fragmenting personas",
    "IDB-R9": "A surface declares its authorization posture",
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

# --------------------------------------------------------------------------
# Rule (e). Property names that could only be carrying a credential value, and
# value shapes that are credential material whatever the property is called.
# --------------------------------------------------------------------------
_SECRET_NAME_TOKENS = (
    "secret", "password", "passwd", "htpasswd", "passphrase", "private",
    "mnemonic", "api_key", "apikey", "bearer", "token",
)
# Legal property names that contain a secret-shaped token and are NOT secrets.
# An allow-list of CONTRACT PROPERTY NAMES, so the scan can stay blunt about
# tokens without punishing the shapes this family actually declares.
_SECRET_NAME_ALLOW = {"oidc_token_reason"}
_PEM_PRIVATE_RE = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY(?: BLOCK)?-----", re.I)
_JWK_PRIVATE_RE = re.compile(
    r'"kty"\s*:.*"d"\s*:\s*"|"d"\s*:\s*".*"kty"\s*:', re.S)
# `client_secret=hV3...`, `password: hunter2`, `KEYCLOAK_ADMIN_PASSWORD=...` —
# the shape a configuration export takes when it is pasted into a free-text
# field, which is the specific artifact spec R7 names.
_ASSIGNED_SECRET_RE = re.compile(
    r"(?:client[_-]?secret|admin[_-]?password|password|passwd|secret|"
    r"api[_-]?key)\s*[:=]\s*\S{6,}", re.I)
# A stored password verifier: htpasswd/bcrypt/apr1/SSHA/SHA-crypt.
_HASHED_SECRET_RE = re.compile(r"\$(?:2[aby]|apr1|5|6)\$|\{SSHA\}")
# A serialized bearer token: three base64url segments, the first a JWT header.
_JWT_RE = re.compile(
    r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")

_VALUE_CLASSES: tuple[tuple[re.Pattern[str], str], ...] = (
    (_PEM_PRIVATE_RE, "a PEM private key block"),
    (_JWK_PRIVATE_RE, "a serialized JWK carrying its private exponent"),
    (_ASSIGNED_SECRET_RE, "an assigned secret value"),
    (_HASHED_SECRET_RE, "a stored password verifier"),
    (_JWT_RE, "a bearer-token-shaped value"),
)

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")

# --------------------------------------------------------------------------
# Rule (f), value half. `resolves_in` has one legal value, so the ENUMERATION
# closes the declaration — and the ref beside it is free text, which is where
# the broker came back in. A record can say `resolves_in: governed_layer` and
# then name the broker's own administration API as the decision point, which
# is the same "membership is authority" substitution the enumeration refuses,
# expressed one field to the left. This walks the VALUE the way rule (e) walks
# credential values, and like rule (e) it is a blocklist over the classes it
# knows: an opaque ref that resolves to broker membership cannot be caught
# here at all, and that residue is recorded in the family README.
# --------------------------------------------------------------------------
# A broker-product / broker-administration URI scheme. `hermes://` and
# `openxfactory:` are governed-layer locators and are deliberately absent.
_BROKER_SCHEME_RE = re.compile(r"^\s*(?:keycloak|broker)://", re.I)
# Broker administration paths: a realm admin surface, or the membership
# collection of an organization — the exact endpoint the shortcut reads from.
_BROKER_ADMIN_PATH_RE = re.compile(
    r"/admin/realms\b|/auth/admin\b|"
    r"/realms/[^/\s]+/(?:users|roles|groups|clients)\b|"
    r"/organizations/[^/\s]+/members\b", re.I)

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


def _mapping(value: Any) -> dict:
    """A dict, or {} for anything else. Cross-record rules run even on
    documents the schema has refused (findings accumulate; validation does not
    stop), so every block read must tolerate a non-mapping without crashing the
    run and discarding every other file's findings."""
    return value if isinstance(value, dict) else {}


def _sequence(value: Any) -> list:
    """A list, or [] for anything else — the sequence twin of `_mapping`.
    `value or []` passes a truthy scalar straight to iteration, so a
    schema-invalid `subjects: 1` would crash the run before its schema finding
    could be reported."""
    return value if isinstance(value, list) else []


def _text(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _key(value: Any) -> str:
    """The normalized form used for IDENTITY KEYS ONLY (rule b). Unicode
    normalized (NFKC), whitespace stripped and case folded, so a trailing
    space, a full-width character or a case change cannot mint a SECOND
    PERSONA for one human.

    Keying on the byte-exact triple was the original implementation and it was
    wrong for the one thing this rule exists to do: the broker's own upstream
    subject, provider id and instance id all arrive through configuration and
    through federation metadata, where a trailing space survives a round trip
    and a case change is routine. `sameness` that a stray space defeats is not
    sameness. Normalized ONLY here — a subject is never rewritten for
    comparison outside an identity key, because two genuinely different
    subjects that fold together must stay different everywhere else."""
    return unicodedata.normalize("NFKC", _text(value)).strip().casefold()


def _skeleton(value: str) -> str:
    """The alphanumeric skeleton of a string, case folded (rule d). A display
    name and an identifier that differ only in spaces, dots, hyphens or
    capitals are THE SAME NAME in the identifier position: `Brett Heap` was
    refused byte-exactly while `BrettHeapOpensoft`, `Brett.Heap.Opensoft` and a
    trailing full stop all walked through, which left the check testing
    punctuation rather than the substitution."""
    return re.sub(r"[^a-z0-9]", "", value.casefold())


# --------------------------- runtime vocabularies ---------------------------

def layer_vocabulary() -> tuple[set[str], set[str]]:
    """Rule (k): the canonical layer ids and the RESERVED layer terms, READ
    from `contracts/policies/layer-vocabulary.yaml` rather than restated.
    Restating them here would create the second spelling of the layer model
    that policy exists to prevent."""
    doc = load_yaml(LAYER_VOCABULARY_PATH)
    canonical = {
        _text(layer.get("id"))
        for layer in _sequence(_mapping(doc).get("canonical_layers"))
        if isinstance(layer, dict) and _text(layer.get("id"))
    }
    reserved = {
        _text(term)
        for term in _sequence(_mapping(doc).get("reserved_layer_terms"))
        if _text(term)
    }
    return canonical, reserved


def schema_enum(docs: dict[str, dict], schema_name: str, *path: str) -> list[str]:
    """An enumeration READ OUT OF THE CONTRACT at run time. Used for the link
    bases (rule c) and the authorization resolution point (rule f): a check
    that restated them could drift from the shape it is supposed to enforce."""
    node: Any = docs[schema_name]
    for step in path:
        node = _mapping(node).get(step)
    values = _sequence(_mapping(node).get("enum"))
    return [v for v in values if isinstance(v, str)]


# --------------------------- rule (a): the closed allow-list ---------------------------

def _resolve(node: Any, root: dict) -> dict:
    """Follow a local `$ref` to its `$defs` target. Only local refs exist in
    this family; a foreign one resolves to {} and its subtree is simply not
    walked, which fails OPEN by design — the schema validator has already
    refused a document the shape cannot describe."""
    seen = 0
    current = _mapping(node)
    while "$ref" in current and seen < 10:
        seen += 1
        ref = _text(current.get("$ref"))
        if not ref.startswith("#/"):
            return {}
        target: Any = root
        for step in ref[2:].split("/"):
            target = _mapping(target).get(step)
        current = _mapping(target)
    return current


def _object_properties(node: Any, root: dict) -> dict[str, Any]:
    """The property schemas an object node declares, UNIONED across every
    branch a document could satisfy (`allOf`, `anyOf`, `oneOf`, `if`, `then`,
    `else`). The union is what makes this an allow-list of the CONTRACT rather
    than of one branch of it: `actor_subject_reference` declares `pre_broker`
    only inside a conditional, and a branch-blind walk would report a
    conformant document's own property as unknown."""
    resolved = _resolve(node, root)
    out: dict[str, Any] = {}
    for name, spec in _mapping(resolved.get("properties")).items():
        out[str(name)] = spec
    for keyword in ("allOf", "anyOf", "oneOf"):
        for branch in _sequence(resolved.get(keyword)):
            for name, spec in _object_properties(branch, root).items():
                out.setdefault(name, spec)
    # `if` / `then` / `else` declare properties a conformant document MAY
    # carry. `not` is deliberately EXCLUDED: a property appearing only inside a
    # `not` branch is one the contract refuses, and unioning it in would widen
    # the allow-list with the very names the schema exists to exclude.
    for keyword in ("if", "then", "else"):
        if keyword in resolved:
            for name, spec in _object_properties(resolved[keyword], root).items():
                out.setdefault(name, spec)
    return out


def _items_schema(node: Any, root: dict) -> Any:
    resolved = _resolve(node, root)
    if "items" in resolved:
        return resolved["items"]
    for keyword in ("allOf", "anyOf", "oneOf"):
        for branch in _sequence(resolved.get(keyword)):
            found = _items_schema(branch, root)
            if found is not None:
                return found
    return None


def check_closed_world(f: Findings, label: str, kind: str, doc: Any,
                       node: Any, root: dict, path: str = "") -> None:
    """Rule (a). Every property path in the document, against the names the
    SCHEMA declares. An allow-list derived from the contract, never a denylist
    of forbidden names."""
    if isinstance(doc, dict):
        allowed = _object_properties(node, root)
        for name in doc:
            here = f"{path}.{name}" if path else str(name)
            if str(name) not in allowed:
                f.error("closed-world-property",
                        f"{label}: property {here!r} is not declared by "
                        f"{KIND_TO_SCHEMA.get(kind, '<unknown schema>')}; this "
                        f"family's shapes are CLOSED ALLOW-LISTS at every "
                        f"depth, so an unrecognised property is refused rather "
                        f"than carried")
                if kind in NEVER_MIRROR_KINDS:
                    f.error("never-mirror-property",
                            f"{label}: {here!r} is an undeclared property on a "
                            f"{kind}; the broker asserts identity and "
                            f"membership only, and the tenancy graph — stacks, "
                            f"layers, domains, projects, subjects, roles, "
                            f"groups, grants — is not broker state. One graph, "
                            f"one authority: a second copy will disagree with "
                            f"the first, and the disagreement is discovered by "
                            f"an authorization decision going the wrong way")
                continue
            check_closed_world(f, label, kind, doc[name], allowed[str(name)],
                               root, here)
    elif isinstance(doc, list):
        items = _items_schema(node, root)
        if items is None:
            return
        for index, entry in enumerate(doc):
            check_closed_world(f, label, kind, entry, items, root,
                               f"{path}[{index}]")


# --------------------------- rule (e): credential values ---------------------------

def _report_value(f: Findings, label: str, where: str, value: str,
                  reassembled: bool = False) -> None:
    # A wrapped, column-truncated or deliberately spaced-out export splits a
    # secret with WHITESPACE INSIDE ONE STRING, which no per-value regex spans:
    # `client_secret: hV3x K9pQ 2mZr 7Lw4` defeated the assigned-secret class
    # while a reader sees the secret plainly. Chunk reassembly joined values
    # ACROSS fields and array items and still missed this, because the split is
    # inside a single value. Test the collapsed form as well as the literal one.
    candidates = (value, re.sub(r"\s+", "", value))
    for pattern, description in _VALUE_CLASSES:
        if any(pattern.search(candidate) for candidate in candidates):
            how = ("a value REASSEMBLED from adjacent chunks at "
                   if reassembled else "the value at ")
            f.error("credential-value-embedded",
                    f"{label}: {how}{where!r} is {description}; every "
                    f"credential this family touches is a "
                    f"`credential-contracts` record with declared custody and "
                    f"a named holder, referenced and never carried — and a "
                    f"configuration export used as reviewed state is "
                    f"credential-free by construction, not by redaction")
            return


def check_no_credential_material(f: Findings, label: str, node: Any,
                                 path: str = "") -> None:
    """Rule (e). Names AND values, with adjacent chunks reassembled."""
    if isinstance(node, dict):
        for name, value in node.items():
            here = f"{path}.{name}" if path else str(name)
            lname = str(name).lower()
            if lname not in _SECRET_NAME_ALLOW and any(
                    token in lname for token in _SECRET_NAME_TOKENS):
                f.error("credential-value-embedded",
                        f"{label}: property {here!r} is credential-shaped; a "
                        f"broker credential is a `credential-contracts` record "
                        f"referenced by requirement id, holder and custody "
                        f"declaration — never a value carried here")
            check_no_credential_material(f, label, value, here)
        # Chunk reassembly across SIBLING string values: a secret split over
        # two fields defeats a per-value scan, and joining what a reader would
        # read together is the cheapest way to close that.
        joined = "".join(v for v in node.values() if isinstance(v, str))
        if len(joined) > 12:
            _report_value(f, label, f"{path or '<root>'}(joined siblings)",
                          joined, reassembled=True)
    elif isinstance(node, list):
        for index, entry in enumerate(node):
            check_no_credential_material(f, label, entry, f"{path}[{index}]")
        # Chunk reassembly across ARRAY ITEMS, the obvious smuggling route: a
        # PEM block or an export line in three innocuous-looking items.
        joined = "".join(v for v in node if isinstance(v, str))
        if len(joined) > 12:
            _report_value(f, label, f"{path or '<root>'}(joined items)",
                          joined, reassembled=True)
    elif isinstance(node, str):
        _report_value(f, label, path or "<root>", node)


# --------------------------- corpus context ---------------------------

class Context:
    """Everything a cross-record rule needs: the corpus's personas indexed by
    subject and by federated identity, its organizations, its declared service
    clients, and the bare usernames it records as PRE-BROKER."""

    def __init__(self, canonical_layers: set[str], reserved_terms: set[str],
                 link_bases: list[str], resolution_points: list[str],
                 pointer_resolution_points: list[str] | None = None) -> None:
        self.canonical_layers = canonical_layers
        self.reserved_terms = reserved_terms
        self.link_bases = link_bases
        self.resolution_points = resolution_points
        # Where an organization's governed-record POINTER resolves, read from
        # the organization schema rather than restated — the same rule as the
        # surface adoption's decision point, and for the same reason.
        self.pointer_resolution_points = pointer_resolution_points or []
        # subject -> persona assertion
        self.personas: dict[str, dict] = {}
        # (instance, provider, upstream subject) -> [subject, ...], each
        # component NORMALIZED through `_key` (NFKC, stripped, case folded). A
        # LIST, because the collision IS the finding: one federated identity
        # resolving to two personas in one instance is the same human twice.
        # Normalized because a byte-exact key is defeated by a trailing space
        # or a case change, and minting a second persona is exactly the outcome
        # this table exists to catch.
        self.federated: dict[tuple[str, str, str], list[str]] = {}
        self.organizations: dict[str, dict] = {}
        # Every subject a declared service client owns — its client id and its
        # service-account subject alike, because either could be offered as a
        # persona or as an actor.
        self.client_subjects: dict[str, str] = {}
        # Bare usernames the corpus records as PRE-BROKER, and the upstream
        # account names it records. Both are refused in the opaque-subject
        # position (rule d).
        self.pre_broker_usernames: set[str] = set()
        self.upstream_accounts: set[str] = set()
        self.seen_ids: set[tuple[str, str]] = set()
        self.duplicate_ids: set[tuple[str, str]] = set()

    def index(self, doc: Any) -> None:
        """Type-guarded: repo scans index BEFORE schema validation, so a
        malformed document must surface as a schema finding on its own file,
        never as a harness crash that discards every other file's findings."""
        doc = _mapping(doc)
        kind = _text(doc.get("kind"))
        id_field = _ID_FIELDS.get(kind)
        rid = _text(doc.get(id_field)) if id_field else ""
        if id_field and rid:
            if (kind, rid) in self.seen_ids:
                self.duplicate_ids.add((kind, rid))
            self.seen_ids.add((kind, rid))
        if kind == "persona_assertion":
            subject = _text(doc.get("subject"))
            instance = _text(_mapping(doc.get("broker_instance")).get("instance_id"))
            if subject:
                self.personas[subject] = doc
            for identity in _sequence(doc.get("linked_identities")):
                identity = _mapping(identity)
                provider = _text(identity.get("provider_id"))
                upstream = _text(identity.get("upstream_subject"))
                if upstream:
                    self.upstream_accounts.add(upstream)
                if instance and provider and upstream and subject:
                    holders = self.federated.setdefault(
                        (_key(instance), _key(provider), _key(upstream)), [])
                    if subject not in holders:
                        holders.append(subject)
        elif kind == "broker_organization":
            if rid:
                self.organizations[rid] = doc
        elif kind == "broker_client_declaration":
            client_id = _text(doc.get("client_id"))
            service_subject = _text(doc.get("service_account_subject"))
            for value in (client_id, service_subject):
                if value:
                    self.client_subjects[value] = client_id
        elif kind == "actor_subject_reference":
            pre = _mapping(doc.get("pre_broker"))
            username = _text(pre.get("username"))
            if username:
                self.pre_broker_usernames.add(username)
            mapping = _mapping(doc.get("mapping"))
            mapped_from = _text(mapping.get("mapped_from_username"))
            if mapped_from:
                self.pre_broker_usernames.add(mapped_from)

    def persona_instance(self, subject: str) -> str:
        persona = self.personas.get(subject)
        if persona is None:
            return ""
        return _text(_mapping(persona.get("broker_instance")).get("instance_id"))


# --------------------------- rules (b), (i), (k): personas ---------------------------

def check_persona_assertion(f: Findings, label: str, doc: dict,
                            ctx: Context) -> None:
    subject = _text(doc.get("subject"))
    instance = _text(_mapping(doc.get("broker_instance")).get("instance_id"))

    # (b) one persona per human per broker instance.
    for identity in _sequence(doc.get("linked_identities")):
        identity = _mapping(identity)
        provider = _text(identity.get("provider_id"))
        upstream = _text(identity.get("upstream_subject"))
        if not (instance and provider and upstream):
            continue
        holders = [s for s in ctx.federated.get(
            (_key(instance), _key(provider), _key(upstream)), []) if s]
        others = sorted(s for s in holders if s and s != subject)
        if others:
            f.error("second-persona-in-instance",
                    f"{label}: federated identity {provider}/{upstream} in "
                    f"broker instance {instance!r} resolves to persona "
                    f"{subject!r} AND to {others}; a human resolves to exactly "
                    f"ONE persona within an instance, and every upstream "
                    f"identity attaches to that persona rather than standing "
                    f"up a second one. The federated identity is the only "
                    f"evidence of sameness the broker has")

    # (i) workloads are not personas.
    if subject and subject in ctx.client_subjects:
        f.error("workload-as-persona",
                # `openxwallet` here is the WIRE LABEL of the pinned family
                # (consumed at contracts/openxwallet-pin.yaml since
                # contract-v2.0). The label is deliberately not renamed with the
                # brand, and this message's bytes are not edited by the split:
                # a finding string is machine-visible surface (R2).
                f"{label}: subject {subject!r} is declared by broker service "
                f"client {ctx.client_subjects[subject]!r}; a workload, agent, "
                f"job or service is not a persona. Its authority comes from "
                f"`credential-contracts` grants and `openxwallet` holders, "
                f"which are stronger than a user row — attenuated grants, "
                f"proof of possession, key-attributed audit, revocation that "
                f"propagates")
    for identity in _sequence(doc.get("linked_identities")):
        upstream = _text(_mapping(identity).get("upstream_subject"))
        if upstream and upstream in ctx.client_subjects:
            f.error("workload-as-persona",
                    f"{label}: linked upstream identity {upstream!r} is "
                    f"declared by broker service client "
                    f"{ctx.client_subjects[upstream]!r}; a service client is "
                    f"TRANSPORT and never a persona's identity")

    # (n) A MEMBERSHIP NAMES A DECLARED ORGANIZATION. Without this the
    # organization_id was an unresolved free identifier, and a role, a grant, a
    # project or a tenancy path could ride in as a "membership" — the mirror,
    # arriving through the one field on this shape that points at another
    # record. The schema pattern now refuses ':' and '/' in this position, so
    # `role:platform-admin` and `stack/opensoft/qa/layer/tenant` are
    # unrepresentable; this closes the rest, where the smuggled value looks
    # like an ordinary company name.
    #
    # CORPUS-COUPLED, like rules (b), (i) and (l): it can only resolve against
    # the organizations the scan actually sees, so it is skipped when a scan
    # contains no broker_organization at all rather than failing every
    # membership in a repository that declares its organizations elsewhere.
    # R6's enforcement scope, stated: within one scanned corpus.
    if ctx.organizations:
        for index, membership in enumerate(
                _sequence(doc.get("organization_memberships"))):
            org = _text(_mapping(membership).get("organization_id"))
            if org and org not in ctx.organizations:
                f.error("never-mirror-property",
                        f"{label}: organization_memberships[{index}] names "
                        f"{org!r}, which no broker_organization in this corpus "
                        f"declares; a membership names a COMPANY BOUNDARY, and "
                        f"an unresolved membership id is where a role, a "
                        f"grant, a project or a tenancy path is carried as "
                        f"though it were a company")

    # (d, first half) The subject is opaque: never a display name, never an
    # address. The schema's pattern already refuses '@' and whitespace; this
    # catches the remaining substitutions the pattern cannot see.
    check_opaque_subject(f, label, "subject", subject,
                         _text(doc.get("display_name")), ctx)


def check_opaque_subject(f: Findings, label: str, where: str, subject: str,
                         display_name: str, ctx: Context) -> None:
    if not subject:
        return
    if _EMAIL_RE.match(subject):
        f.error("actor-identifier-not-opaque",
                f"{label}: {where} {subject!r} is an email address; addresses "
                f"are reassigned and an upstream provider may assert one it "
                f"never verified, so an address is never the identifier")
    # Compared on the ALPHANUMERIC SKELETON, not byte-exactly: `Brett Heap`
    # was caught and `BrettHeapOpensoft`, `Brett.Heap.Opensoft` and a trailing
    # full stop were not, which made the check a test of punctuation rather
    # than of the substitution it is named for.
    if display_name and _skeleton(subject) == _skeleton(display_name):
        f.error("actor-identifier-not-opaque",
                f"{label}: {where} {subject!r} is the display name "
                f"{display_name!r} with its spaces and punctuation removed; "
                f"display names change and the identifier may not, which is "
                f"the whole reason the opaque subject exists — and stripping "
                f"the spaces does not make a name an opaque subject")
    if subject in ctx.upstream_accounts:
        f.error("actor-identifier-not-opaque",
                f"{label}: {where} {subject!r} is an UPSTREAM ACCOUNT name "
                f"this corpus records; upstream accounts are created, retired, "
                f"renamed and reassigned by organisations the family does not "
                f"control, so nothing durable is built on one")


# --------------------------- rules (h), (k): organizations ---------------------------

def check_broker_organization(f: Findings, label: str, doc: dict,
                              ctx: Context) -> None:
    role = _text(doc.get("company_role"))

    # (k) the ratified layer spelling, checked against the policy at run time.
    if role and role in ctx.reserved_terms:
        f.error("reserved-layer-term",
                f"{label}: company_role {role!r} is a RESERVED layer term in "
                f"`contracts/policies/layer-vocabulary.yaml`; the ratified "
                f"spellings of the two company boundaries are "
                f"{sorted(COMPANY_ROLE_TO_LAYER)} (resolving to canonical "
                f"layers {sorted(set(COMPANY_ROLE_TO_LAYER.values()))})")
    elif role and role not in COMPANY_ROLE_TO_LAYER:
        f.error("company-role-unknown",
                f"{label}: company_role {role!r} is not one of "
                f"{sorted(COMPANY_ROLE_TO_LAYER)}; a company boundary is the "
                f"tenant/operator company or the served company, and there is "
                f"no third kind")

    refs = _sequence(doc.get("governed_record_refs"))
    # (h) one pointer, never a projection.
    if len(refs) > 1:
        f.error("organization-multiple-graph-refs",
                f"{label}: {len(refs)} governed-record references; an "
                f"organization carries AT MOST ONE. The failure mode is "
                f"incremental — a second reference for convenience, then a "
                f"third, until broker state is a partial copy of the tenancy "
                f"graph that disagrees with it")
    for index, ref in enumerate(refs):
        ref = _mapping(ref)
        record_kind = _text(ref.get("record_kind"))
        if record_kind and record_kind not in ctx.canonical_layers:
            f.error("layer-vocabulary-unknown",
                    f"{label}: governed_record_refs[{index}].record_kind "
                    f"{record_kind!r} is not a canonical layer in "
                    f"`contracts/policies/layer-vocabulary.yaml` "
                    f"({sorted(ctx.canonical_layers)})")
        where = ref.get("resolves_in")
        if where is not None and where not in ctx.pointer_resolution_points:
            f.error("membership-as-authority",
                    f"{label}: governed_record_refs[{index}] resolves in "
                    f"{where!r}; the pointer resolves in the GOVERNED LAYER "
                    f"(legal values: {sorted(ctx.pointer_resolution_points)}), "
                    f"and resolving it inside the broker is the mirror this "
                    f"requirement refuses")


# --------------------------- rules (c), (l): link records ---------------------------

def check_identity_link_record(f: Findings, label: str, doc: dict,
                               ctx: Context) -> None:
    mode = _text(doc.get("mode"))
    basis = _text(doc.get("basis"))
    initiated = _mapping(doc.get("initiated_by"))
    approved = _mapping(doc.get("approved_by"))
    surviving = _text(doc.get("surviving_subject"))
    subjects = [_text(s) for s in _sequence(doc.get("subjects"))]
    instance = _text(doc.get("broker_instance_ref"))

    # (c) the record names who acted.
    if not initiated and not approved:
        f.error("link-actor-unnamed",
                f"{label}: the record names neither an initiating human nor an "
                f"approving administrator, so the link is not established. "
                f"Without a named actor 'explicit' is unfalsifiable — and an "
                f"identity merge that cannot be undone from the audit record "
                f"is the failure this requirement exists to prevent")

    # (c) the basis is one the CONTRACT admits, read from the schema at run
    # time. `attribute_match` — an email address above all — is not a member,
    # and that omission is the requirement.
    if basis and basis not in ctx.link_bases:
        f.error("silent-auto-link",
                f"{label}: basis {basis!r} is not one of the bases this "
                f"contract admits ({sorted(ctx.link_bases)}). A federated "
                f"identity joins a persona by an EXPLICIT link the human "
                f"initiated or an ADMINISTRATIVE MERGE that was approved and "
                f"recorded — never on an attribute match, however convenient: "
                f"an upstream provider may assert an address it never "
                f"verified, and addresses are reassigned, so attribute-match "
                f"auto-linking is an account-takeover primitive")
    if mode == "self_link" and basis and basis != "explicit_user_action":
        f.error("link-basis-incoherent",
                f"{label}: mode 'self_link' with basis {basis!r}; a self link "
                f"IS the explicit user action, and the two cannot disagree")
    if mode == "admin_merge" and basis and basis != "governed_administration_approval":
        f.error("link-basis-incoherent",
                f"{label}: mode 'admin_merge' with basis {basis!r}; a merge is "
                f"an administrative act approved through the governed "
                f"workflow, and the two cannot disagree")

    # (c) a self link is initiated FROM the persona it adds to.
    if mode == "self_link" and initiated:
        held = _text(initiated.get("session_holds_subject"))
        actor = _text(initiated.get("subject"))
        # A self link is initiated BY the persona whose session it is. Checking
        # only `session_holds_subject` against the survivor left the two
        # initiator fields free to disagree: an attacker naming themselves as
        # the initiating subject while claiming the VICTIM's session produced a
        # record that read as the victim's own explicit act.
        if actor and held and actor != held:
            f.error("self-link-outside-persona-session",
                    f"{label}: the initiating subject is {actor!r} while the "
                    f"session held {held!r}; a self link is initiated BY the "
                    f"persona whose session it is, and the two cannot "
                    f"disagree — a record whose initiator is not the session "
                    f"holder is somebody else's act wearing the paperwork of "
                    f"an explicit one")
        if held and surviving and held != surviving:
            f.error("self-link-outside-persona-session",
                    f"{label}: the initiating session holds {held!r} while the "
                    f"link adds to {surviving!r}; an explicit link is "
                    f"initiated from a session ALREADY HOLDING that persona, "
                    f"which is what makes 'explicit' checkable rather than a "
                    f"claim")

    # (c) a self link joins ONE persona. A self link naming other subjects is a
    # merge wearing the paperwork of a link — no approver, no pre-merge
    # entries, and every record written against the extra subjects silently
    # orphaned. The mode determines which obligations apply, so the mode has to
    # match what the record actually does.
    if mode == "self_link":
        extra = sorted({s for s in subjects if s and s != surviving})
        if extra:
            f.error("link-subjects-inconsistent",
                    f"{label}: a self link names subject(s) {extra} besides "
                    f"the persona it adds to ({surviving!r}); joining two "
                    f"personas is an ADMIN MERGE, which requires an approver "
                    f"and carries every pre-merge subject")

    # (c, approver half) A MERGE IS NOT APPROVED BY ONE OF ITS OWN PARTIES.
    # Post-ratification disposition, recorded in research.md: the ratified text
    # says a merge is approved through GOVERNED ADMINISTRATION and does not
    # spell out "not by a party". This slice adopts the refusal as the faithful
    # reading, because a party approving its own absorption of another identity
    # is precisely the account takeover the requirement exists to refuse, and a
    # governed administration approval given by the beneficiary is not a
    # governed approval at all.
    if mode == "admin_merge":
        approver = _text(approved.get("administrator_subject"))
        if approver and approver in [s for s in subjects if s] + [surviving]:
            f.error("merge-approved-by-a-party",
                    f"{label}: the approving administrator {approver!r} is one "
                    f"of the personas being merged; a merge is an "
                    f"administrative act approved through the governed "
                    f"workflow, and a party approving its own absorption of "
                    f"another identity is the account takeover this "
                    f"requirement exists to refuse")

    # (c) every prior subject stays resolvable to the survivor.
    if mode == "admin_merge":
        resolvable = {
            _text(_mapping(entry).get("subject")):
                _text(_mapping(entry).get("remains_resolvable_to"))
            for entry in _sequence(doc.get("pre_merge_subjects"))
        }
        for subject in subjects:
            if not subject:
                continue
            if subject not in resolvable:
                f.error("pre-merge-subject-unresolvable",
                        f"{label}: subject {subject!r} took part in this merge "
                        f"and no pre-merge entry keeps it resolvable; the merge "
                        f"silently orphans every record already written against "
                        f"it, re-creating at merge time the attribution loss "
                        f"this capability exists to prevent")
            elif surviving and resolvable[subject] != surviving:
                f.error("pre-merge-subject-unresolvable",
                        f"{label}: pre-merge subject {subject!r} resolves to "
                        f"{resolvable[subject]!r} rather than to the surviving "
                        f"persona {surviving!r}")
    if surviving and subjects and surviving not in subjects:
        f.error("pre-merge-subject-unresolvable",
                f"{label}: surviving subject {surviving!r} is not among the "
                f"subjects this record names ({subjects}); the survivor is one "
                f"of the parties, not a third identity introduced by the merge")

    # (l) personas do not span instances.
    for subject in [*subjects, surviving]:
        if not subject:
            continue
        resolved_instance = ctx.persona_instance(subject)
        if resolved_instance and instance and resolved_instance != instance:
            f.error("persona-spans-instances",
                    f"{label}: subject {subject!r} is a persona of broker "
                    f"instance {resolved_instance!r} while this record is "
                    f"declared in {instance!r}; personas do not span "
                    f"instances, and a human holding a persona in two "
                    f"instances holds two single personas that no capability "
                    f"requires to be linked")


# --------------------------- rules (d), (i): actor references ---------------------------

def check_actor_subject_reference(f: Findings, label: str, doc: dict,
                                  ctx: Context) -> None:
    provenance = _text(doc.get("provenance"))
    subject = _text(doc.get("subject"))
    display = _text(doc.get("display_name_at_record"))

    check_opaque_subject(f, label, "actor subject", subject, display, ctx)

    # (d) provenance is never `broker_asserted` for a bare username.
    if provenance == "broker_asserted" and subject in ctx.pre_broker_usernames:
        f.error("bare-username-as-persona",
                f"{label}: subject {subject!r} is a bare username this corpus "
                f"records as PRE-BROKER, presented as a broker-asserted "
                f"persona. A record written before the broker is resolved "
                f"through an explicitly recorded mapping "
                f"(`mapped_historical_actor`) or MARKED as predating the "
                f"persona boundary (`pre_broker_username`) — never asserted as "
                f"a persona, because a blanket resolution asserts an identity "
                f"nobody verified")
    if provenance == "pre_broker_username":
        pre = _mapping(doc.get("pre_broker"))
        if pre.get("presented_as_persona") is not False:
            f.error("bare-username-as-persona",
                    f"{label}: a pre-broker actor record declares "
                    f"presented_as_persona="
                    f"{pre.get('presented_as_persona')!r}; such a record stays "
                    f"readable and is never presented as a broker-asserted "
                    f"persona")

    # (d, mapping half) A MAPPING RESOLVES A BARE USERNAME TO A BROKER-ISSUED
    # SUBJECT, or it has resolved nothing. A `mapped_historical_actor` whose
    # subject IS its own `mapped_from_username` — or is any bare username this
    # corpus records as pre-broker — is the blanket backfill OQ-1 refuses,
    # wearing the paperwork of a mapping: the durable identifier in the actor
    # position is still the username, and the mapping block only makes it look
    # adjudicated.
    if provenance == "mapped_historical_actor":
        mapped_from = _text(_mapping(doc.get("mapping")).get(
            "mapped_from_username"))
        if subject and mapped_from and subject == mapped_from:
            f.error("bare-username-as-persona",
                    f"{label}: the mapping resolves {mapped_from!r} to "
                    f"ITSELF, so the durable identifier is still the bare "
                    f"username; a mapping resolves a pre-broker username to a "
                    f"BROKER-ISSUED subject or it has resolved nothing")
        elif subject and subject in ctx.pre_broker_usernames:
            f.error("bare-username-as-persona",
                    f"{label}: the mapping resolves to {subject!r}, which this "
                    f"corpus records as a PRE-BROKER username; a mapping whose "
                    f"target is itself a bare username has moved the "
                    f"substitution one field along rather than resolving it")

    # (i) a service client never appears as the actor of a governed act.
    if subject and subject in ctx.client_subjects:
        f.error("workload-as-actor",
                f"{label}: the actor is broker service client "
                f"{ctx.client_subjects[subject]!r}; a service client is "
                f"TRANSPORT and never the actor of a governed act. The act is "
                f"recorded as unattributed unless a persona can be "
                f"established")


# --------------------------- rule (i): client declarations ---------------------------

def check_broker_client_declaration(f: Findings, label: str, doc: dict,
                                    ctx: Context) -> None:
    transport = _mapping(doc.get("transport"))
    if transport.get("is_transport") is not True:
        f.error("transport-not-declared",
                f"{label}: the client does not declare itself TRANSPORT; a "
                f"broker service client exists only where a surface genuinely "
                f"needs OIDC tokens, and it is transport by definition")
    if transport.get("actor_of_governed_acts") is not False:
        f.error("workload-as-actor",
                f"{label}: the client declares actor_of_governed_acts="
                f"{transport.get('actor_of_governed_acts')!r}; a service "
                f"client never appears as the actor of a governed act")
    if transport.get("organization_membership_as_authority") is not False:
        f.error("membership-as-authority",
                f"{label}: the client declares "
                f"organization_membership_as_authority="
                f"{transport.get('organization_membership_as_authority')!r}; a "
                f"membership records ASSOCIATION and is an input to a decision "
                f"taken in the governed layer, never authority to act — and a "
                f"transport client holds no membership as authority at all")
    if not _text(doc.get("oidc_token_reason")):
        f.error("token-need-unstated",
                f"{label}: no reason is stated for requiring OIDC tokens; a "
                f"client may be provisioned only where a surface genuinely "
                f"needs them, and the stated purpose is what makes that "
                f"visible")


# --------------------------- rules (f), (g), (j), (m): surface adoptions ---------------------------

def check_governed_decision_locator(f: Findings, label: str, field: str,
                                    ref: str, instance_id: str) -> None:
    """Rule (f), value half. A governed decision point is named by a
    GOVERNED-LAYER locator. Three classes are refused:

    1. a broker-product administration scheme (`keycloak://`, `broker://`);
    2. a broker administration path (a realm admin surface, a realm's user,
       role, group or client collection, an organization's member collection);
    3. a scheme-less ref whose FIRST SEGMENT is the record's own broker
       instance — a decision point named as a bare path under the broker is
       resolved inside the broker by construction.

    A ref that merely CONTAINS the instance id is NOT refused, and the reason
    is a ratified positive: the gate console's governed decision point is
    `hermes://broker-opensoft-shared/authorization/gate-console`, where the
    instance id is a legitimate scoping token on a governed-layer endpoint.
    Containment cannot discriminate the two, so this keys on the locator's
    SHAPE and says so rather than turning a conformant example red."""
    if not ref:
        return
    reasons: list[str] = []
    if _BROKER_SCHEME_RE.search(ref):
        reasons.append("a broker-administration URI scheme")
    if _BROKER_ADMIN_PATH_RE.search(ref):
        reasons.append("a broker administration path")
    if "://" not in ref and instance_id and (
            ref.split("/", 1)[0].strip() == instance_id):
        reasons.append("a bare path under this record's own broker instance")
    if not reasons:
        return
    f.error("membership-as-authority",
            f"{label}: resolved_authorization.{field} {ref!r} is "
            f"{' and '.join(reasons)}; the record declares that authorization "
            f"resolves in the GOVERNED LAYER and then names the broker's own "
            f"administration surface as the place it resolves. That is "
            f"organization membership offered as authority with the "
            f"enumeration satisfied — a decision taken by reading who is in a "
            f"group, which is an INPUT to the governed decision and never the "
            f"decision itself")


def check_surface_adoption(f: Findings, label: str, doc: dict,
                           ctx: Context) -> None:
    posture = _text(doc.get("authorization_posture"))
    writes = _mapping(doc.get("governed_write_actions"))
    resolved = _mapping(doc.get("resolved_authorization"))
    isolation = _mapping(doc.get("isolation"))
    instance = _mapping(doc.get("broker_instance"))

    # (f) a write action requires a resolved authorization decision.
    if writes.get("offered") is True:
        if posture != "resolved_authorization":
            f.error("write-action-without-resolved-authorization",
                    f"{label}: the surface offers governed write actions "
                    f"{_sequence(writes.get('actions')) or '<unnamed>'} while "
                    f"its declared posture is {posture!r}; a governed write "
                    f"action requires a RESOLVED AUTHORIZATION DECISION rather "
                    f"than authentication alone. This is the quiet failure: a "
                    f"surface ships read-only under 'any authenticated "
                    f"persona', then gains a write action, and the login is "
                    f"silently doing work it was never designed to do")
        if not _text(resolved.get("decision_point_ref")):
            f.error("write-action-without-resolved-authorization",
                    f"{label}: the surface offers governed write actions and "
                    f"names NO GOVERNED DECISION POINT; declaring the stronger "
                    f"posture without naming where the decision resolves is "
                    f"the declaration satisfying itself")
    # (f) NAMING A WRITE ACTION IS OFFERING ONE. `offered: false` beside a
    # populated `actions` list is the quiet transition already half-made: the
    # actions are written down, the posture is not, and the schema's
    # write-action conditional keys on `offered` so it never fired. The bound
    # is now in the schema too; this reports it under its own code so the
    # refusal names the rule rather than an if/then failure (the same reason
    # rule (h) reports a second pointer rather than an array length).
    if writes.get("offered") is not True and _sequence(writes.get("actions")):
        f.error("write-action-without-resolved-authorization",
                f"{label}: the record NAMES governed write actions "
                f"{_sequence(writes.get('actions'))} while declaring "
                f"offered={writes.get('offered')!r}; a surface that names a "
                f"governed write action offers one, and offering one requires "
                f"the stronger posture and a resolved authorization decision")
    if posture == "resolved_authorization" and not resolved:
        f.error("write-action-without-resolved-authorization",
                f"{label}: posture 'resolved_authorization' with no "
                f"resolved_authorization block; the posture names where the "
                f"decision is taken or it says nothing")
    if resolved:
        where = resolved.get("resolves_in")
        if where is not None and where not in ctx.resolution_points:
            f.error("membership-as-authority",
                    f"{label}: authorization resolves in {where!r}; the "
                    f"decision resolves in the governed layer against the "
                    f"governed tenancy graph and the grants recorded there "
                    f"(legal values: {sorted(ctx.resolution_points)}). "
                    f"Organization membership is an INPUT to that decision, "
                    f"never the decision itself")
        # (f, value half) The enumeration is closed; the REFS beside it are
        # free text. A record declaring `governed_layer` and then naming the
        # broker's own administration API is the same substitution the
        # enumeration refuses, moved one field to the left.
        for field in ("decision_point_ref", "grants_ref"):
            check_governed_decision_locator(
                f, label, field, _text(resolved.get(field)),
                _text(instance.get("instance_id")))

    # (m) no surface holds human accounts of its own.
    if doc.get("human_accounts_held_by_surface") is not False:
        f.error("surface-holds-human-accounts",
                f"{label}: the surface declares "
                f"human_accounts_held_by_surface="
                f"{doc.get('human_accounts_held_by_surface')!r}; human "
                f"identity resolves at the broker, and an account the broker "
                f"cannot resolve to a persona is an identity the governed "
                f"layer cannot name")

    # (g) the adoption retires the secret it replaces.
    replaced = _mapping(doc.get("replaced_credential"))
    if replaced:
        requirement = _text(_mapping(replaced.get("credential_requirement"))
                            .get("requirement_id"))
        if replaced.get("retired") is not True:
            f.error("shared-secret-not-retired",
                    f"{label}: adoption replaces shared credential "
                    f"{requirement or '<unnamed>'!r} and records retired="
                    f"{replaced.get('retired')!r}; the shared credential is "
                    f"RETIRED as part of the adoption, so the inventory "
                    f"records one fewer shared secret rather than one more and "
                    f"two authentication paths are not left live")
        elif not _text(replaced.get("retired_at")):
            f.error("shared-secret-not-retired",
                    f"{label}: shared credential {requirement or '<unnamed>'!r} "
                    f"is recorded retired with no retirement time; a "
                    f"retirement nobody dated is not evidence of one")

    # (j) isolation escalates by instance, never by partitioning personas.
    restriction = _text(isolation.get("co_residence_restriction"))
    deployment = _text(instance.get("deployment"))

    # (j, negative half) THE UNRESTRICTED CLAIM IS ALSO A FINDING THAT WAS
    # MADE. `co_residence_restriction: none` was previously the one answer that
    # needed no evidence, so the co-residence question could be answered
    # "no restriction" without anybody having asked it — and an unrecorded
    # negative is indistinguishable from an unasked question, which is the
    # OQ-5 finding's own rule applied to its own output. BOTH enum values now
    # require the reference: for `population_restricted` the commitment that
    # imposes the restriction, for `none` the written finding that there is
    # none.
    if restriction and not _text(isolation.get("restriction_ref")):
        f.error("isolation-restriction-unrecorded",
                f"{label}: co_residence_restriction {restriction!r} is "
                f"declared with nothing referenced; the co-residence question "
                f"is answered by a RECORDED FINDING in either direction — an "
                f"unrecorded negative is indistinguishable from an unasked "
                f"question, and 'none' is the answer a surface reaches by "
                f"default rather than by inquiry")

    if restriction == "population_restricted":
        if deployment and deployment != "dedicated":
            f.error("isolation-by-partition",
                    f"{label}: population "
                    f"{_text(isolation.get('restricted_population')) or '<unnamed>'!r} "
                    f"must not co-reside, and the adoption names a "
                    f"{deployment!r} broker instance "
                    f"{_text(instance.get('instance_id'))!r}. Isolation "
                    f"escalates to a DEDICATED INSTANCE — its own deployment, "
                    f"datastore and administrative plane — and is not met by "
                    f"partitioning personas inside a shared one, which pays "
                    f"the full persona-fragmentation cost for weaker "
                    f"isolation: the administrative plane, the datastore and "
                    f"the blast radius stay shared")


# --------------------------- per-record validation ---------------------------

def validate_record(f: Findings, label: str, doc: Any, docs: dict[str, dict],
                    ctx: Context) -> None:
    if not isinstance(doc, dict):
        f.error("schema", f"{label}: document is not a mapping")
        return
    kind = doc.get("kind")
    if kind not in KIND_TO_SCHEMA:
        f.error("unknown-kind",
                f"{label}: kind {kind!r} is not an identity-brokering kind")
        return

    schema_doc = docs[KIND_TO_SCHEMA[kind]]
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
                f"last-write-wins, so a duplicate could swap the persona, "
                f"organization or client a reference resolves to — refused on "
                f"every copy rather than resolved by file order")

    check_closed_world(f, label, kind, doc, schema_doc, schema_doc)
    check_no_credential_material(f, label, doc)

    if kind == "persona_assertion":
        check_persona_assertion(f, label, doc, ctx)
    elif kind == "broker_organization":
        check_broker_organization(f, label, doc, ctx)
    elif kind == "actor_subject_reference":
        check_actor_subject_reference(f, label, doc, ctx)
    elif kind == "identity_link_record":
        check_identity_link_record(f, label, doc, ctx)
    elif kind == "broker_client_declaration":
        check_broker_client_declaration(f, label, doc, ctx)
    elif kind == "broker_surface_adoption":
        check_surface_adoption(f, label, doc, ctx)


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
        # Blank lines are allowed INSIDE the header block: stopping at the
        # first non-comment line would silently drop a detail pin separated by
        # a blank line, and a dropped pin fails OPEN — the fixture keeps a
        # green self-test with its invariant pin gone.
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
    return sorted(EXAMPLES_DIR.glob("*.example.yaml"))


def negative_paths() -> list[Path]:
    return sorted(NEGATIVE_DIR.glob("*.yaml"))


def _clone(ctx: Context) -> Context:
    fresh = Context(ctx.canonical_layers, ctx.reserved_terms, ctx.link_bases,
                    ctx.resolution_points, ctx.pointer_resolution_points)
    fresh.personas = dict(ctx.personas)
    fresh.federated = {k: list(v) for k, v in ctx.federated.items()}
    fresh.organizations = dict(ctx.organizations)
    fresh.client_subjects = dict(ctx.client_subjects)
    fresh.pre_broker_usernames = set(ctx.pre_broker_usernames)
    fresh.upstream_accounts = set(ctx.upstream_accounts)
    fresh.seen_ids = set(ctx.seen_ids)
    fresh.duplicate_ids = set(ctx.duplicate_ids)
    return fresh


def self_test(f: Findings, docs: dict[str, dict], ctx: Context) -> None:
    positives = positive_paths()
    negatives = negative_paths()
    if not positives:
        f.error("examples-missing", "no packaged positive examples found")
    if not negatives:
        f.error("examples-missing", "no packaged negative fixtures found")

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
        local_ctx = _clone(ctx)
        doc = load_yaml(path)
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
    scanned = skipped = excluded = 0
    found: list[tuple[Path, dict]] = []
    for path in files:
        if set(path.parts) & SKIP_DIR_NAMES:
            continue
        # Exclude ANY packaged corpus, not only this checkout's: domain repos
        # pin and vendor openxFactory, so the normal consumption path scans a
        # COPY, and matching on this checkout's absolute paths would
        # re-adjudicate every vendored negative fixture as a live record.
        #
        # DURING A SWEEP ONLY, and COUNTED. Applying the rule to an explicitly
        # named file made `validate-identity-brokering.py <family-example>`
        # silently validate nothing — the one command an author reaches for
        # when checking a single record, answering "0 errors" for a file it
        # never opened. And the exclusion was uncounted, so a sweep that
        # dropped 41 documents said so nowhere: a consumer whose own records
        # happened to sit under an `examples/identity-brokering/` path would
        # read a clean, silent, empty scan as a pass.
        if sweep and "examples" in path.parts and (
                "identity-brokering" in path.parts):
            excluded += 1
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
        found.append((path, doc))

    # INDEX FIRST, then validate — into a context of the SCANNED REPO'S OWN
    # records. Without this the cross-record rules (one persona per instance,
    # the workload/persona collisions, cross-instance linking) would resolve
    # only against the packaged corpus and be inert on every real artifact,
    # while a consumer's legitimate records reported spurious findings against
    # teaching fixtures.
    repo_ctx = Context(ctx.canonical_layers, ctx.reserved_terms, ctx.link_bases,
                       ctx.resolution_points, ctx.pointer_resolution_points)
    for _, doc in found:
        repo_ctx.index(doc)
    for path, doc in found:
        scanned += 1
        validate_record(f, str(path), doc, docs, repo_ctx)
    f.note(f"repo scan: {scanned} identity-brokering artifact(s) validated, "
           f"{skipped} document(s) skipped as another kind, {excluded} "
           f"excluded as a packaged/vendored teaching corpus")


# --------------------------- orchestration ---------------------------

def report(f: Findings, strict: bool) -> int:
    for line in f.notes:
        print(line)
    for line in f.warnings:
        print(line)
    for line in f.errors:
        print(line)
    print(f"\nvalidate-identity-brokering: {len(f.errors)} error(s), "
          f"{len(f.warnings)} warning(s)")
    return 1 if f.errors or (strict and f.warnings) else 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=None,
                    help="repo checkout (or single file) to scan for real "
                         "identity-brokering artifacts; omit to self-test only")
    ap.add_argument("--strict", action="store_true",
                    help="treat warnings as errors")
    args = ap.parse_args()

    if not FAMILY_DIR.is_dir():
        print(f"ERROR {FAMILY_DIR} not found", file=sys.stderr)
        return 2
    if not LAYER_VOCABULARY_PATH.is_file():
        print(f"ERROR {LAYER_VOCABULARY_PATH} not found; the canonical layer "
              f"ids and reserved layer terms are read from the ratified policy",
              file=sys.stderr)
        return 2

    try:
        docs = load_schemas()
        canonical_layers, reserved_terms = layer_vocabulary()
        link_bases = schema_enum(docs, "identity-link-record.schema.yaml",
                                 "properties", "basis")
        resolution_points = schema_enum(
            docs, "surface-adoption.schema.yaml", "properties",
            "resolved_authorization", "properties", "resolves_in")
        pointer_resolution_points = schema_enum(
            docs, "broker-organization.schema.yaml", "properties",
            "governed_record_refs", "items", "properties", "resolves_in")
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR schema load failure: {exc}", file=sys.stderr)
        return 2

    f = Findings()
    missing = sorted(set(KIND_TO_SCHEMA.values()) - set(docs))
    if missing:
        f.error("schema-file-missing",
                f"the family is missing schema file(s) {missing}")
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
        if doc.get("schema_version") != 1 or not doc.get("kind"):
            f.error("schema-identity-missing",
                    f"{name}: every contract YAML carries `schema_version` and "
                    f"`kind`")

    # (k) the bridge's targets must exist in the ratified policy. A renamed
    # canonical layer fails LOUDLY here rather than leaving this family
    # speaking a second spelling of the layer model.
    for role, layer in sorted(COMPANY_ROLE_TO_LAYER.items()):
        if layer not in canonical_layers:
            f.error("layer-vocabulary-drift",
                    f"company role {role!r} maps to canonical layer {layer!r}, "
                    f"which `contracts/policies/layer-vocabulary.yaml` no "
                    f"longer declares ({sorted(canonical_layers)})")
    if not link_bases:
        f.error("schema-enum-missing",
                "identity-link-record.schema.yaml declares no `basis` "
                "enumeration, so the admissible linking acts cannot be read "
                "from the contract")
    if not resolution_points:
        f.error("schema-enum-missing",
                "surface-adoption.schema.yaml declares no "
                "`resolved_authorization.resolves_in` enumeration, so the "
                "governed decision point cannot be read from the contract")
    if not pointer_resolution_points:
        f.error("schema-enum-missing",
                "broker-organization.schema.yaml declares no "
                "`governed_record_refs[].resolves_in` enumeration, so where "
                "the governed-record pointer resolves cannot be read from the "
                "contract")

    ctx = Context(canonical_layers, reserved_terms, link_bases,
                  resolution_points, pointer_resolution_points)
    for path in positive_paths():
        ctx.index(load_yaml(path))
    f.note(f"layer vocabulary read from "
           f"{LAYER_VOCABULARY_PATH.relative_to(ROOT)}: canonical "
           f"{sorted(canonical_layers)}, reserved {sorted(reserved_terms)}")
    f.note(f"linking bases read from the contract: {sorted(link_bases)}; "
           f"authorization resolves in {sorted(resolution_points)}")

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
