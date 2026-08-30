from __future__ import annotations

from collections import defaultdict

from .model import Finding, Record, as_records, as_strings
from .temporal import parse_timestamp

RevocationTarget = tuple[str, str, str]


def revocation_findings(
    records: list[Record], registries_by_id: dict[str, list[Record]]
) -> list[Finding]:
    approvals = {
        _target(item): item
        for item in records
        if item.get("kind") == "policy_allowance"
    }
    revocations = {
        str(item.get("revocation_digest")): item
        for item in records
        if item.get("kind") == "policy_allowance_revocation"
    }
    by_target: dict[RevocationTarget, list[Record]] = defaultdict(list)
    for revocation in revocations.values():
        by_target[_target(revocation)].append(revocation)
    findings = _registry_closure_findings(
        registries_by_id, revocations, by_target
    )
    for digest, revocation in revocations.items():
        target = _target(revocation)
        approval = approvals.get(target)
        if approval is None:
            findings.append(
                Finding(
                    "revocation-target",
                    digest,
                    "complete approval identity does not resolve",
                )
            )
        applicable = [
            revision
            for revision in registries_by_id.get(target[0], [])
            if parse_timestamp(revision.get("published_at"))
            <= parse_timestamp(revocation.get("revoked_at"))
        ]
        predecessors = {
            str(revision.get("predecessor_revision_digest"))
            for revision in applicable
            if revision.get("predecessor_revision_digest") is not None
        }
        heads = [
            revision
            for revision in applicable
            if str(revision.get("revision_digest")) not in predecessors
        ]
        if len(heads) != 1 or revocation.get(
            "predecessor_revision_digest"
        ) != heads[0].get("revision_digest"):
            findings.append(
                Finding(
                    "registry-chain",
                    digest,
                    "revocation predecessor is not the unique effective registry head",
                )
            )
        elif not any(
            str(entry.get("allowance_id")) == target[1]
            and str(entry.get("approval_digest")) == target[2]
            for entry in as_records(heads[0].get("allowances"))
        ):
            findings.append(
                Finding(
                    "registry-chain",
                    digest,
                    "revocation target is absent from its predecessor revision",
                )
            )
        if approval is not None and parse_timestamp(
            revocation.get("revoked_at")
        ) <= parse_timestamp(approval.get("approved_at")):
            findings.append(
                Finding(
                    "revocation-chain-time",
                    digest,
                    "revocation is not later than approval",
                )
            )
        predecessor = revocation.get("predecessor_event_digest")
        if predecessor is not None:
            previous = revocations.get(str(predecessor))
            if previous is None or _target(previous) != target:
                findings.append(
                    Finding(
                        "revocation-chain",
                        digest,
                        "event predecessor identity differs",
                    )
                )
    for target, events in by_target.items():
        findings.extend(_chain_findings(target, events))
    return findings


def _registry_closure_findings(
    registries_by_id: dict[str, list[Record]],
    revocations: dict[str, Record],
    by_target: dict[RevocationTarget, list[Record]],
) -> list[Finding]:
    findings: list[Finding] = []
    for registry_id, revisions in registries_by_id.items():
        for revision in revisions:
            for entry in as_records(revision.get("allowances")):
                target = (
                    registry_id,
                    str(entry.get("allowance_id")),
                    str(entry.get("approval_digest")),
                )
                listed = set(as_strings(entry.get("revocation_digests")))
                expected = {
                    str(event.get("revocation_digest"))
                    for event in by_target.get(target, [])
                    if parse_timestamp(event.get("revoked_at"))
                    <= parse_timestamp(revision.get("published_at"))
                }
                if listed != expected:
                    findings.append(
                        Finding(
                            "registry-revocation-closure",
                            f"{registry_id}/{revision.get('revision_id')}/{target[1]}",
                            "registry revocations are not the exact effective history",
                        )
                    )
                for digest in listed:
                    event = revocations.get(digest)
                    if event is None or _target(event) != target:
                        findings.append(
                            Finding(
                                "registry-revocation",
                                digest,
                                "listed revocation does not resolve to the allowance identity",
                            )
                        )
    return findings


def _chain_findings(
    target: RevocationTarget, events: list[Record]
) -> list[Finding]:
    by_digest = {str(event.get("revocation_digest")): event for event in events}
    roots = [event for event in events if event.get("predecessor_event_digest") is None]
    findings: list[Finding] = []
    subject = "/".join(target)
    if len(roots) != 1:
        findings.append(
            Finding(
                "revocation-chain-root",
                subject,
                "revocation history must have exactly one root",
            )
        )
    children: dict[str, int] = defaultdict(int)
    for event in events:
        predecessor = event.get("predecessor_event_digest")
        if predecessor is None:
            continue
        children[str(predecessor)] += 1
        prior = by_digest.get(str(predecessor))
        if prior is not None and parse_timestamp(event.get("revoked_at")) <= parse_timestamp(
            prior.get("revoked_at")
        ):
            findings.append(
                Finding(
                    "revocation-chain-time",
                    str(event.get("revocation_digest")),
                    "revocation is not later than its predecessor",
                )
            )
    if any(count > 1 for count in children.values()):
        findings.append(
            Finding("revocation-chain-fork", subject, "revocation history is not linear")
        )
    if _cycle_exists(events, by_digest):
        findings.append(
            Finding("revocation-chain-cycle", subject, "revocation event cycle detected")
        )
    return findings


def _cycle_exists(events: list[Record], by_digest: dict[str, Record]) -> bool:
    for event in events:
        visited: set[str] = set()
        current: Record | None = event
        while current is not None:
            digest = str(current.get("revocation_digest"))
            if digest in visited:
                return True
            visited.add(digest)
            predecessor = current.get("predecessor_event_digest")
            current = by_digest.get(str(predecessor)) if predecessor is not None else None
    return False


def _target(record: Record) -> RevocationTarget:
    return (
        str(record.get("registry_id")),
        str(record.get("allowance_id")),
        str(record.get("approval_digest")),
    )
