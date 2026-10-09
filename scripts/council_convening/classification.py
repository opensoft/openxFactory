"""Protocol classification and the selection-dependent effects (data-model E1).

T018, written from the data model's rules and nothing else. Every boundary over
a protocol-carrying record begins here, before any replacement shape check runs,
so a legacy record is never called malformed.

CLASSIFICATION, in its written order:

1. A record whose `protocol` is the replacement's `protocol_id` is a
   REPLACEMENT record, whatever else it carries. Root-authorization members on
   it are refused later, as `root_authorization_refused`; they never make it
   legacy (analysis I3).
2. A record whose `protocol` is the legacy `protocol_id` is a LEGACY record.
   Any other `protocol` value is `protocol_unknown`.
3. A record with no `protocol` member is LEGACY when one of the legacy entry's
   recognition rules matches, and `protocol_unknown` otherwise.

THE EFFECTS depend on the side's SELECTED protocol, never on payload shape alone
(D5). Phase 1 lands these rows of the effects table:

* under a replacement selection, at any status: a legacy record is refused
  `legacy_protocol_refused`, and a replacement record proceeds to the
  replacement rules;
* under a legacy selection while the legacy status is `in_use`: a legacy record
  is ROUTED, and a replacement record is refused `protocol_not_selected`;
* offline, with no selection: a legacy record is ROUTED, and a replacement
  record proceeds to the offline replacement rules.

A ROUTE IS NEVER A PASS. It carries the finding `legacy_protocol_routed`, and the
legacy verifier remains the only verifier of legacy bytes. The rows for the
legacy statuses `deprecated` and `historical_only` land in Phase 6 with their
finding code. Until then this module raises `EffectNotLanded` rather than guess
them.

THE REGISTRY IS CLOSED HERE, as landed. `LANDED_PROTOCOLS` is the set at this
commit, and `registry_findings` refuses an instance that adds, removes, renames
or reorders an entry, or rewrites a signing context or a recognition rule.
Statuses and tags are the lifecycle data the release cuts move, so they are
checked by the schema and not pinned here.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from . import records

REGISTRY_REL = records.FAMILY_REL / "protocol.registry.yaml"
REGISTRY_SCHEMA_ID = records.ID_BASE + "protocol-registry.schema.yaml"
REGISTRY_KIND = "xfactory_council_protocol_registry"

#: The kinds that carry a `protocol` member and are classified first (E2, E4–E8).
PROTOCOL_CARRYING_KINDS = frozenset({
    "xfactory_council_convening",
    "xfactory_council_convening_snapshot",
    "xfactory_council_seat_assignment",
    "xfactory_council_registration_challenge",
    "xfactory_council_seat_key_registration",
    "xfactory_council_seat_return",
})

#: The kinds judged by kind alone and never classified (E1, E3, E10–E12; N7).
JUDGED_BY_KIND_KINDS = frozenset({
    REGISTRY_KIND,
    "xfactory_council_predicate_registry",
    "xfactory_council_producer_binding",
    "xfactory_council_protocol_selection",
    "xfactory_council_activation_evidence",
})

FAMILY_RECORD_KINDS = PROTOCOL_CARRYING_KINDS | JUDGED_BY_KIND_KINDS

ROUTE_FINDING = "legacy_protocol_routed"

#: The statuses each role may hold, as the registry schema's `allOf` says.
ROLE_STATUSES = {
    "replacement": ("available", "admission_eligible"),
    "legacy": ("in_use", "deprecated", "historical_only"),
}

#: The registry as landed at this commit, in its landed order. Moving it is a
#: governed contract change; `tests/council_convening/test_protocol_registry.py`
#: holds an independent copy.
LANDED_PROTOCOLS: dict[str, dict[str, Any]] = {
    "xfc-resolved-council-1": {
        "role": "replacement",
        "signing_contexts": [
            "xfc-resolved-council-1/seat-key-registration",
            "xfc-resolved-council-1/seat-return",
        ],
    },
    "xfactory-council-seat-return/v1": {
        "role": "legacy",
        "signing_contexts": [
            "xfactory-council-seat-return/v1",
            "xfactory-council-seat-key-authorization/v1",
        ],
        "recognition": [
            {"rule": "convening_block_without_roster",
             "block_member": "council_convening",
             "roster_member": "required_seats"},
            {"rule": "legacy_signing_context",
             "member_paths": [["signature", "protocol"]]},
            {"rule": "root_authorization_member",
             "members": ["root_key_fingerprint", "root_signature", "authorization"]},
        ],
    },
}


class EffectNotLanded(LookupError):
    """An effects-table row whose rules land in a later phase. Raised rather
    than guessed, so a vector that needs it cannot be adjudicated yet."""


# --------------------------------------------------------------------------
# The registry.
# --------------------------------------------------------------------------

def load_registry_doc(root: Path | None = None) -> Any:
    """The registry instance under `root`, parsed strictly and not yet judged."""
    root = Path(root) if root is not None else records.REPO_ROOT
    path = root / REGISTRY_REL
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise records.SchemaLoadError(
            f"{REGISTRY_REL.as_posix()}: unreadable ({type(exc).__name__})") from exc
    try:
        return records.strict_yaml(raw, REGISTRY_REL.as_posix())
    except ValueError as exc:
        raise records.SchemaLoadError(
            f"{REGISTRY_REL.as_posix()}: does not parse as strict YAML") from exc


class RegistryNotClosed(ValueError):
    """The registry instance in this checkout fails its schema or its closure.
    Nothing is classified against it; `findings` holds `(code, message)`."""

    def __init__(self, findings: list[tuple[str, str]]):
        self.findings = findings
        super().__init__("the protocol registry is not closed: "
                         + "; ".join(message for _code, message in findings))


def load_closed_registry(root: Path | None, schemas: records.SchemaSet) -> "Registry":
    """The registry under `root`, ONLY once its schema and closure findings are
    empty. Every entry point that classifies (`check`, `corpus`, the generator,
    the self-test) goes through this, so none classifies against an instance
    that added, removed, renamed or rewrote an entry."""
    document = load_registry_doc(root)
    findings = registry_findings(schemas, document)
    if findings:
        raise RegistryNotClosed(findings)
    return Registry(document)


class Registry:
    """A protocol registry instance, read by role."""

    def __init__(self, document: Mapping[str, Any]):
        self.document = document
        entries = document.get("protocols") if isinstance(document, Mapping) else None
        if not isinstance(entries, list) or not all(isinstance(e, Mapping) for e in entries):
            raise ValueError("the registry has no list of protocol entries")
        self.entries = {entry.get("protocol_id"): entry for entry in entries}
        by_role: dict[str, list[str]] = {}
        for entry in entries:
            by_role.setdefault(entry.get("role"), []).append(entry.get("protocol_id"))
        if len(by_role.get("replacement", [])) != 1 or len(by_role.get("legacy", [])) != 1:
            raise ValueError("the registry must hold exactly one replacement and one legacy entry")
        self.replacement_id: str = by_role["replacement"][0]
        self.legacy_id: str = by_role["legacy"][0]

    def entry(self, protocol_id: str) -> Mapping[str, Any]:
        if not isinstance(protocol_id, str) or protocol_id not in self.entries:
            raise KeyError(protocol_id)
        return self.entries[protocol_id]

    def status(self, protocol_id: str, overrides: Mapping[str, str] | None = None) -> str:
        """`protocol_id`'s status, from a vector's override where it names one."""
        if overrides and protocol_id in overrides:
            return overrides[protocol_id]
        return self.entry(protocol_id)["status"]


def load_registry(root: Path | None = None) -> Registry:
    return Registry(load_registry_doc(root))


def registry_findings(schemas: records.SchemaSet, document: Any) -> list[tuple[str, str]]:
    """Schema and closure findings for a registry instance, as `(code, message)`."""
    findings: list[tuple[str, str]] = []
    for error in schemas.errors(REGISTRY_SCHEMA_ID, document):
        where = "/".join(map(str, error.absolute_path)) or "(root)"
        findings.append(("council-convening-schema",
                         f"protocol registry: fails `{error.validator}` at {where}"))
    entries = document.get("protocols") if isinstance(document, Mapping) else None
    if not isinstance(entries, list):
        return findings
    ids = [entry.get("protocol_id") if isinstance(entry, Mapping) else None
           for entry in entries]
    landed = list(LANDED_PROTOCOLS)
    added = [pid for pid in ids if pid not in LANDED_PROTOCOLS]
    removed = [pid for pid in landed if pid not in ids]
    if added:
        findings.append(("council-convening-registry-closure",
                         f"protocol registry: {len(added)} entry(ies) not in the set as "
                         f"landed at this commit; adding a protocol is a governed "
                         f"contract change"))
    if removed:
        findings.append(("council-convening-registry-closure",
                         f"protocol registry: landed entry(ies) absent: {', '.join(removed)}"))
    if len(ids) != len(set(map(str, ids))):
        findings.append(("council-convening-registry-closure",
                         "protocol registry: a protocol_id is repeated"))
    if not added and not removed and ids != landed:
        findings.append(("council-convening-registry-closure",
                         "protocol registry: the entries are not in their landed order"))
    for entry in entries:
        if not isinstance(entry, Mapping) or entry.get("protocol_id") not in LANDED_PROTOCOLS:
            continue
        pid = entry["protocol_id"]
        want = LANDED_PROTOCOLS[pid]
        for member in ("role", "signing_contexts", "recognition"):
            if entry.get(member) != want.get(member):
                findings.append(("council-convening-registry-closure",
                                 f"protocol registry: {pid} `{member}` differs from "
                                 f"the entry as landed"))
    return findings


# --------------------------------------------------------------------------
# Classification and the effects.
# --------------------------------------------------------------------------

def _at(record: Mapping[str, Any], path: list[str]) -> Any:
    value: Any = record
    for member in path:
        if not isinstance(value, Mapping) or member not in value:
            return None
        value = value[member]
    return value


def _recognized(record: Mapping[str, Any], legacy: Mapping[str, Any]) -> bool:
    contexts = set(legacy["signing_contexts"])
    for rule in legacy["recognition"]:
        kind = rule["rule"]
        if kind == "convening_block_without_roster":
            block = record.get(rule["block_member"])
            if isinstance(block, Mapping) and rule["roster_member"] not in block:
                return True
        elif kind == "legacy_signing_context":
            for path in rule["member_paths"]:
                value = _at(record, path)
                if isinstance(value, str) and value in contexts:
                    return True
        elif kind == "root_authorization_member":
            if any(member in record for member in rule["members"]):
                return True
        else:  # pragma: no cover - the schema and closure admit only the three
            raise ValueError(f"unknown recognition rule {kind!r}")
    return False


def carries_protocol_shape(document: Any, registry: Registry) -> bool:
    """Whether `document` carries a `protocol` member or matches a legacy
    recognition rule: a shape that is classified, wherever it appears."""
    if not isinstance(document, Mapping):
        return False
    return "protocol" in document or _recognized(document, registry.entry(registry.legacy_id))


def classify(record: Any, registry: Registry) -> str:
    """`"replacement"` or `"legacy"`, or `Refused("protocol_unknown")`."""
    if not isinstance(record, Mapping):
        raise records.Refused("protocol_unknown")
    if "protocol" in record:
        protocol = record["protocol"]
        if isinstance(protocol, str) and protocol == registry.replacement_id:
            return "replacement"
        if isinstance(protocol, str) and protocol == registry.legacy_id:
            return "legacy"
        raise records.Refused("protocol_unknown", member="protocol")
    if _recognized(record, registry.entry(registry.legacy_id)):
        return "legacy"
    raise records.Refused("protocol_unknown")


def classify_and_select(record: Any, selected_protocol: str | None, registry: Registry,
                        statuses: Mapping[str, str] | None = None) -> records.Outcome:
    """Classification, then the effect of the side's selected protocol.

    `selected_protocol` is a registry `protocol_id`, or `None` offline. One that
    names no entry is a `KeyError`: a harness error, not a refusal.
    """
    if selected_protocol is not None:
        registry.entry(selected_protocol)
    try:
        classification = classify(record, registry)
    except records.Refused as refused:
        return records.Outcome("refuse", refused.code)

    legacy = classification == "legacy"
    accept = records.Outcome("accept", derived={"classification": "replacement"})
    if selected_protocol is None:
        if legacy:
            return records.Outcome("route", None, (ROUTE_FINDING,),
                                   {"classification": "legacy"})
        return accept
    if selected_protocol == registry.replacement_id:
        return records.Outcome("refuse", "legacy_protocol_refused") if legacy else accept

    status = registry.status(registry.legacy_id, statuses)
    if status != "in_use":
        raise EffectNotLanded(
            f"the effects under a legacy selection with legacy status {status!r} "
            f"land in Phase 6")
    if legacy:
        return records.Outcome("route", None, (ROUTE_FINDING,),
                               {"classification": "legacy"}, status_read=True)
    return records.Outcome("refuse", "protocol_not_selected", status_read=True)
