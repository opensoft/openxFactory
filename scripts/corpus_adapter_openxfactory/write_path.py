"""This repository's DECLARED governed write path, and why it is unreachable
today.

RULING Q1 (`opensoft/openxFactory` issue #656, 2026-09-04T15:24Z) is that
specs, changes, ideation documents and contracts "stay in git, read from
repositories and written back only through the apply lane". So this corpus
DECLARES a governed write path, and the seam's third requirement makes that
declaration answerable at resolution time rather than at the first write.

AND THE DECLARED PATH CANNOT CARRY A DOCUMENT-BODY WRITE YET. The verb a
document write-back maps to is `edit-apply`, and
`ideation_dashboard.intent_apply_lane` lists it in `LANE_DEFERRED_VERBS` —
"kernel-transportable verbs the routes layer cannot yet execute — the dispatcher
has no branch for them (they remain local-console verbs)". The conformant answer
to that is not a fallback: it is exactly what `corpus-adapter-seam`'s third
requirement already writes for a declared-but-unreachable path — the write
refuses, names the path, and the document remains unsaved.

That is why `dispatch` defaults to None and why nothing here writes a file.
`split-opendox-two-layer-product` § 2.5 — "HARDEN THE APPLY LANE BEFORE IT
BECOMES THE ONLY WRITE PATH", a PRECONDITION of § 3 rather than a follow-up —
is the task that changes it, and when it does, it flips ONE construction
argument: `apply_lane_write_path(dispatch=...)` turns every refusal below into a
receipt without a line changing in the adapter. Making that visible in code
rather than only in the packet is the point of building the request artifact and
the correlation identifier now.

THIS MODULE AND `home.py` ARE THE TWO THE VOCABULARY SCAN EXEMPTS. Naming the
lane, the verb and the packet layout is this module's whole job; every other
module in the package receives them as data.

NO DISPATCH IS PERFORMED BY THIS CHANGE OR ITS TESTS. The default path refuses;
the tests that exercise construction inject a recording callable of their own and
invoke no workflow.
"""

from __future__ import annotations

import base64
import hashlib
import re
from datetime import datetime, timezone
from typing import Mapping

from .shape import WritePath, WriteProposal

#: The declared governed write path's NAME. It is the string a refusal names,
#: and it is deliberately the workflow's own file name so an operator reading a
#: refusal knows what to go and look at.
APPLY_LANE_NAME = "intent-apply.yml"

#: The verb a document-body write-back maps to.
EDIT_APPLY = "edit-apply"

#: Why the declared path is unreachable, named at the source of truth.
DEFERRED_REASON = (
    "the declared governed write path does not yet carry the edit-apply verb "
    "(ideation_dashboard.intent_apply_lane.LANE_DEFERRED_VERBS); "
    "split-opendox-two-layer-product § 2.5 is the task that changes this"
)

#: Where a change packet's documents live, as path segments.
_PACKET_ROOT = ("openspec", "changes")
#: An archived packet sits one level deeper, under this segment.
_ARCHIVE_SEGMENT = "archive"

#: The lane refuses a target id that is not ONE safe path segment (its own
#: `_SAFE_SEGMENT`, mirrored here so a request is never built that the lane
#: would reject on arrival).
_SAFE_SEGMENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def packet_target(document_key: str) -> str | None:
    """The change-packet id a document belongs to, or None where it has none.

    The apply lane's `edit-apply` verb targets a `change_id`, so a document
    outside a change packet has no target on this path at all. Answering None
    rather than inventing an id is what keeps the refusal honest.
    """
    parts = tuple(document_key.split("/"))
    if parts[:len(_PACKET_ROOT)] != _PACKET_ROOT:
        return None
    rest = parts[len(_PACKET_ROOT):]
    if rest and rest[0] == _ARCHIVE_SEGMENT:
        rest = rest[1:]
    if len(rest) < 2:            # an id AND a document under it
        return None
    return rest[0] if _SAFE_SEGMENT.match(rest[0]) else None


def build_gate_intent(proposal: WriteProposal) -> Mapping:
    """The corpus's own request artifact for one proposed document body.

    Built to the EXISTING `contracts/schemas/gate-intent.schema.yaml` — no new
    schema is authored by this change — and shape-checked against the lane's own
    `shape_error` before it is returned, so a request this repository builds can
    never be one the lane would reject on arrival. A failure here is a defect in
    this module, not a refusal of the caller's proposal, and it is raised as one.

    The body travels as text where it decodes and as base64 where it does not,
    with the digest always present: a request that carried only a digest would
    not be a proposal, and one that silently dropped undecodable bytes would be
    worse than either.
    """
    target = packet_target(proposal.document_key)
    if target is None:
        raise ValueError(
            f"{proposal.document_key} has no target on {APPLY_LANE_NAME}")
    args = {
        "document": proposal.document_key,
        "content_sha256": hashlib.sha256(proposal.content).hexdigest(),
    }
    try:
        args["content"] = proposal.content.decode("utf-8")
    except UnicodeDecodeError:
        args["content_base64"] = base64.b64encode(proposal.content).decode("ascii")
    if proposal.reason:
        args["reason"] = proposal.reason
    intent = {
        "schema_version": 1,
        "kind": "gate-intent",
        "actor": proposal.actor,
        "verb": EDIT_APPLY,
        "target": {"change_id": target},
        "args": args,
        "requested_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_rev_seen": proposal.basis_revision,
        "status": "pending",
    }
    # Lazy, function-local: the dashboard package is heavy and its destiny is
    # unsettled (design D3 files it in the column that splits by function),
    # while this package must import cleanly in a tree that does not carry it —
    # which is exactly the tree the neutral conformance corpus stands in for.
    from ideation_dashboard.intent_apply_lane import shape_error
    problem = shape_error(intent)
    if problem:
        raise ValueError(
            f"this module built a request the lane would refuse: {problem}")
    return intent


def request_correlation_id(intent: Mapping) -> str:
    """The request's stable identity, computed by the lane's OWN function.

    `intent_apply_lane.request_digest` is sha256 over the actor, the verb, the
    canonical target and the viewed revision — "a stable identity for ONE
    request, computed lane-side from the validated fields". That IS design D2's
    "correlation identifier", and the eventual durable record is reachable from
    it, so a second identity function invented here would be a second answer to
    a question already answered.
    """
    from ideation_dashboard.intent_apply_lane import request_digest  # lazy, as above
    return request_digest(dict(intent))


def apply_lane_write_path(*, dispatch=None) -> WritePath:
    """This corpus's declared write path. Unreachable unless a dispatcher is
    injected — see the module docstring, and § 2.5."""
    return WritePath(
        name=APPLY_LANE_NAME,
        build_request=build_gate_intent,
        correlation_id=request_correlation_id,
        routes=packet_target,
        dispatch=dispatch,
        unavailable_reason=DEFERRED_REASON,
    )
