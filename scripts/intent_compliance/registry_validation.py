from __future__ import annotations

from collections import defaultdict

from .model import Finding, Record, as_records, as_strings
from .revocation_validation import revocation_findings
from .temporal import parse_timestamp


def registry_chain_findings(records: list[Record]) -> list[Finding]:
    approvals = {
        (
            str(record.get("registry_id")),
            str(record.get("allowance_id")),
            str(record.get("approval_digest")),
        )
        for record in records
        if record.get("kind") == "policy_allowance"
    }
    registries_by_id: dict[str, list[Record]] = defaultdict(list)
    for record in records:
        if record.get("kind") == "policy_allowance_registry":
            registries_by_id[str(record.get("registry_id"))].append(record)
    findings: list[Finding] = []
    for registry_id, revisions in registries_by_id.items():
        by_digest = {str(item.get("revision_digest")): item for item in revisions}
        children: dict[str, list[Record]] = defaultdict(list)
        roots = 0
        bindings: dict[str, str] = {}
        for revision in revisions:
            predecessor = revision.get("predecessor_revision_digest")
            if predecessor is None:
                roots += 1
            elif predecessor not in by_digest:
                findings.append(
                    Finding("registry-chain", registry_id, "missing same-registry predecessor")
                )
            else:
                children[str(predecessor)].append(revision)
                findings.extend(_child_revision_findings(by_digest[str(predecessor)], revision))
            entries = as_records(revision.get("allowances"))
            allowance_ids = [str(entry.get("allowance_id")) for entry in entries]
            for allowance_id in set(allowance_ids):
                if allowance_ids.count(allowance_id) > 1:
                    findings.append(
                        Finding(
                            "registry-duplicate-allowance",
                            f"{registry_id}/{revision.get('revision_id')}/{allowance_id}",
                            "allowance identity occurs more than once in one revision",
                        )
                    )
            for entry in entries:
                allowance_id = str(entry.get("allowance_id"))
                approval_digest = str(entry.get("approval_digest"))
                if (registry_id, allowance_id, approval_digest) not in approvals:
                    findings.append(
                        Finding(
                            "registry-approval",
                            f"{registry_id}/{allowance_id}",
                            "registry entry has no matching approval record",
                        )
                    )
                prior = bindings.get(allowance_id)
                if prior is not None and prior != approval_digest:
                    findings.append(
                        Finding("allowance-id-reused", allowance_id, "approval digest changed")
                    )
                bindings[allowance_id] = approval_digest
        if roots != 1:
            findings.append(
                Finding("registry-chain-fork", registry_id, "registry must have one root")
            )
        for predecessor, child_revisions in children.items():
            if len(child_revisions) > 1:
                findings.append(
                    Finding("registry-chain-fork", registry_id, f"fork after {predecessor}")
                )
        if _has_cycle(revisions, by_digest):
            findings.append(
                Finding("registry-chain-cycle", registry_id, "predecessor cycle detected")
            )
    findings.extend(revocation_findings(records, registries_by_id))
    return findings


def _child_revision_findings(parent: Record, child: Record) -> list[Finding]:
    findings: list[Finding] = []
    if parse_timestamp(child.get("published_at")) <= parse_timestamp(
        parent.get("published_at")
    ):
        findings.append(
            Finding(
                "registry-chain-time",
                str(child.get("revision_id")),
                "child publication is not later",
            )
        )
    parent_entries = {
        str(item.get("allowance_id")): item
        for item in as_records(parent.get("allowances"))
    }
    child_entries = {
        str(item.get("allowance_id")): item
        for item in as_records(child.get("allowances"))
    }
    for allowance_id, parent_entry in parent_entries.items():
        child_entry = child_entries.get(allowance_id)
        if child_entry is None or child_entry.get("approval_digest") != parent_entry.get(
            "approval_digest"
        ):
            findings.append(
                Finding(
                    "registry-append-only",
                    allowance_id,
                    "approval disappeared or changed",
                )
            )
            continue
        if not set(as_strings(parent_entry.get("revocation_digests"))) <= set(
            as_strings(child_entry.get("revocation_digests"))
        ):
            findings.append(
                Finding("registry-append-only", allowance_id, "revocation disappeared")
            )
    return findings


def _has_cycle(revisions: list[Record], by_digest: dict[str, Record]) -> bool:
    for revision in revisions:
        visited: set[str] = set()
        current: Record | None = revision
        while current is not None:
            digest = str(current.get("revision_digest"))
            if digest in visited:
                return True
            visited.add(digest)
            predecessor = current.get("predecessor_revision_digest")
            current = by_digest.get(str(predecessor)) if predecessor is not None else None
    return False
