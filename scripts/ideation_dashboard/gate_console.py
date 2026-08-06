"""Human gate console: demote / edit-apply / ratify + gate-action records
(plan "gate_console.py"; change task 3.12; US9 T033/T034).

The authority-bearing crown of the surface. Every action here is a HUMAN GATE
action (D16) — the ONE place a lifecycle transition is legal — so every entry
point demands a `boundary.HumanGate` (constructed with an identified human
actor). Machinery and agents hold no `HumanGate`; an `OutputBoundary` (the
machinery/agent chokepoint, which has no gate method BY CONSTRUCTION) handed to
a gate action is rejected AND reported on its own refusal ledger, exactly the
foundation's structural posture — a gate side effect from a non-human caller is
impossible by construction, not gated by an `is_human` boolean.

Each action produces the SAME governed artifacts as the equivalent manual path
PLUS one schema-valid gate-action record (`gate-action-record.schema.yaml`,
validated by the pinned openxFactory validator):

  demote(change_id, reason)   the mechanized REVERSE transition (D16), exactly
      the 2026-07-13 manual demotion tooled. This module PLANS the reverse
      transition — the file moves (change proposal docs -> the staging topic's
      `openspec/` draft workspace with draft headers; supporting docs -> the
      topic root with Status flips) plus the README/INDEX and register edits —
      and emits it as EXECUTABLE artifacts (a transition manifest + an ordered
      plan) alongside a register-update note and the gate-action record. The
      actual move against the real openxFactory corpus is a SEPARATE, explicit
      step a human runs (`execute_demotion_plan`, exposed by `cli.py gate
      demote --execute`, and exercised in-test against a fixture change tree) —
      the console never silently rewrites the live corpus. `reason` is REQUIRED
      (schema + entrypoint): the durable "why" a change went back to staging.

  ratify(change_id, ratifier)   writes the ratification record (ratifier, date)
      + register-update artifacts; the gate-action record carries the
      ratification-record artifact reference (the schema's contains-rule).

  edit_apply(change_id, document, redline)   applies a HUMAN-approved redline
      (a replacement-block or full-text artifact) to a change document through
      the gate — the AI-drafting of redlines is OUT of scope (a follow-on
      delta): the console APPLIES exactly what a human supplies and nothing
      else, and the record carries the redline artifact.

  kickoff(change_id)   the post-ratification realization dispatch (D17) lives in
      `kickoff.py`; `GateConsole.kickoff` delegates to it. It REFUSES without a
      recorded ratification and, on success, emits a workflow-job dispatch
      descriptor.

Gate/demotion/ratification/redline/job records land under a caller-DECLARED
records directory (the `HumanGate`'s output allowlist), never baked in here —
the same path-agnostic discipline as the snapshot's run-local output path. The
records are LIVE AUDIT entries (wall-clock stamped, not the deterministic
snapshot projection).
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import yaml

from doc_health import corpus

from .boundary import (
    GATE_SIDE_EFFECT,
    BoundaryViolation,
    HumanGate,
    Refusal,
)

HEADER_SCAN_LINES = corpus.STATUS_SCAN_LINES

# The gate-action record contract literals (mirror gate-action-record.schema.yaml
# — the READ-ONLY truth; transcribed, never invented).
RECORD_KIND = "gate-action-record"
RECORD_SCHEMA_VERSION = 1
ACTION_DEMOTE = "demote"
ACTION_EDIT_APPLY = "edit-apply"
ACTION_RATIFY = "ratify"
ACTION_KICKOFF = "kickoff"
ACTION_DISPOSE_POSSIBLE = "dispose-possible"
ACTION_PROPOSE = "propose"
# add-workbench-bullseye-and-create: the human-only create of a NEW ideation
# document through the tested authoring scaffold. Targets `document` (the schema
# requires it for this action) — no change_id, no possible_id, no topic_id.
ACTION_CREATE_DOCUMENT = "create-document"
# add-workbench-branch-sessions (chg 1.1): the three branch-session verbs.
# ADDITIVE, same posture as every growth above — no prior record is invalidated.
#
#   edit-document    the SESSION-ONLY rewrite of an existing document inside the
#       session worktree. Deliberately NOT `edit-apply`: that verb is the
#       main-resident redline path and stays behaviourally untouched (FR-017).
#       `edit-document` requires no redline artifact and produces none; it rides
#       ONE commit with its own record (FR-006, FR-015).
#   open-pr          push the session branch and open (or update) the pull
#       request into the EXISTING Merge-Master ritual. The record is
#       MAIN-RESIDENT and carries the pull request as an artifact; the verb
#       merges, approves, reviews, and bypasses NOTHING (FR-029, FR-030).
#   abandon-session  end a session without saving, carrying the REQUIRED reason.
#       Also MAIN-RESIDENT, because FR-028's human cleanup deletes the branch and
#       a branch-resident reason-record would be destroyed with it (FR-022).
ACTION_EDIT_DOCUMENT = "edit-document"
ACTION_OPEN_PR = "open-pr"
ACTION_ABANDON_SESSION = "abandon-session"
# add-wheel-action-verbs (011): the three GENERATIVE verbs the wheel's action
# row commissions. Each is a recorded dispatch — a `workflow-job` descriptor
# plus a gate-action record — and performs none of the work it commissions.
# ADDITIVE, same posture as every growth above; `demote` needs no constant
# because it is already enumerated with its `change_id` target.
ACTION_PROMOTE_TO_STAGING = "promote-to-staging"
ACTION_DERIVE_POSSIBLES = "derive-possibles"
ACTION_RESEARCH_BRIEF = "research-brief"
# add-project-scoped-selection: the create-project commission — the same
# recorded-dispatch mechanic one register over. The target `project_id` is
# slugged from the proposed name at commission time; the aggregation-owned
# project register is edited only by the commission's fulfilment.
ACTION_CREATE_PROJECT = "create-project"

# Artifact kinds the schema recognises.
ART_TRANSITION_MANIFEST = "transition-manifest"
ART_RATIFICATION_RECORD = "ratification-record"
ART_REDLINE = "redline"
ART_WORKFLOW_JOB = "workflow-job"
ART_REGISTER_UPDATE = "register-update"
# add-workbench-bullseye-and-create, Brett's 2026-07-25 ruling on that change's
# open question 4: an ideation/corpus document an action brought into existence,
# referenced by repository-relative path. A FIRST-CLASS kind rather than the
# `other` the first realization pass used — the schema now REQUIRES this kind on
# a `create-document` record, so an audit consumer can filter document-producing
# actions from the artifact vocabulary and not only from `action`.
ART_DOCUMENT = "document"
# add-workbench-branch-sessions (chg 1.1): the two session artifact kinds.
#
#   commit         the session commit an action rode. Its `reference` is the
#       record's OWN action stamp, never a sha: a commit cannot contain its own
#       sha, so resolution is DEFINED as the commit that INTRODUCED the record
#       file on the branch (`git log --diff-filter=A -- <record-path>`), which
#       immediately after the action is the branch tip (FR-006).
#   pull-request   the pull request an `open-pr` action opened or updated,
#       referenced by URL (FR-029).
ART_COMMIT = "commit"
ART_PULL_REQUEST = "pull-request"
ART_OTHER = "other"

# Default records prefix. A CALLER-DECLARED output path (the HumanGate allowlist);
# the aggregation lane wires the committed location (section 4). Not baked into
# any write here — only a default the CLI/tests may override.
DEFAULT_RECORDS_DIR = "ideation/dashboard/gate-records/"

DRAFT_STATUS = "draft"


class GateRefused(Exception):
    """A gate action refused on an engine-side PRECONDITION (a demote with no
    reason; a kickoff on an unratified change). Distinct from a boundary
    refusal: this is an authority/precondition rule the console enforces before
    any record is written. Raised, never silent."""


# --------------------------------------------------------------------------
# GATEWAY PROVENANCE (add-workbench-branch-sessions design D23; Brett's
# 2026-07-27 ruling, item 3 — "tag the event with the actual facts we know")
#
# The human/agent boundary on this console is a CONSOLE-PRESENCE control —
# anti-CSRF / same-origin — and NOT authentication. A process running as the
# identified human, on the human's own machine, can read the per-serve console
# token from `/capabilities` or set `XF_HUMAN_CONSOLE=1` and act as the human.
# Brett ACCEPTED that residual (item 1: distinguishing the two needs the
# xForge-host identity work deferred under D22) and required the record to carry
# the facts we DO know instead: WHICH DOOR the action came through, and HOW
# console presence was shown. An accepted-but-invisible residual becomes an
# AUDITABLE one.
#
# The vocabulary mirrors `gate-action-record.schema.yaml`'s `provenance` block —
# the READ-ONLY truth, transcribed and never invented. `provenance` is OPTIONAL
# schema-side and required by NO conditional, because pre-growth records exist
# and a conditional would invalidate the evidence retroactively; the obligation
# is a ROUTE obligation, which is what this module and its callers discharge.
SURFACE_HTTP = "http"
SURFACE_CLI = "cli"
SURFACES = (SURFACE_HTTP, SURFACE_CLI)
# HOW console presence was shown. There is deliberately NO value meaning "not
# shown": an invocation that cannot demonstrate presence is refused before a
# record exists, so no record can honestly carry one. `declared` is the WEAKEST
# and is its own value so an audit consumer can filter for it.
PRESENCE_CONSOLE_TOKEN = "console-token"
PRESENCE_TTY = "tty"
PRESENCE_DECLARED = "declared"
CONSOLE_PRESENCES = (PRESENCE_CONSOLE_TOKEN, PRESENCE_TTY, PRESENCE_DECLARED)


@dataclass(frozen=True)
class Provenance:
    """The gateway facts about ONE invocation: the surface it arrived on and how
    its console presence was shown.

    A TYPE, not a mapping, and that is the security-relevant part: the only way a
    record can carry provenance is for a caller to hand `build_gate_action_record`
    one of these, and the only places that construct one are the two GATEWAYS
    that observe the fact themselves — `serve.py`'s handler (which has already run
    the console-token check) and `cli.py` (which has already run the tty /
    declaration check). A request body is a mapping, so a body-supplied
    `provenance` cannot reach a record even by accident: it is not this type, and
    no route reads that key. A self-declared surface would be worthless.

    Validated at construction, so an invalid pair can never be written — the
    schema requires BOTH fields inside the block, and a half-filled provenance
    tags nothing."""

    surface: str
    console_presence: str

    def __post_init__(self) -> None:
        if self.surface not in SURFACES:
            raise GateRefused(
                f"unknown gateway surface {self.surface!r} — the record's "
                f"provenance names one of {', '.join(SURFACES)} (D23)")
        if self.console_presence not in CONSOLE_PRESENCES:
            raise GateRefused(
                f"unknown console-presence proof {self.console_presence!r} — the "
                f"record's provenance names one of "
                f"{', '.join(CONSOLE_PRESENCES)} (D23). There is deliberately no "
                "value meaning 'presence was not shown'")

    def as_record(self) -> dict:
        """The record block, in the schema's own field order."""
        return {"surface": self.surface, "console_presence": self.console_presence}


# The three pairs the two gateways can actually observe, named once so no caller
# re-derives them. (`http` + `tty`/`declared` is not among them: the HTTP door's
# presence test IS the token.)
HTTP_CONSOLE_TOKEN = Provenance(SURFACE_HTTP, PRESENCE_CONSOLE_TOKEN)
CLI_TTY = Provenance(SURFACE_CLI, PRESENCE_TTY)
CLI_DECLARED = Provenance(SURFACE_CLI, PRESENCE_DECLARED)


# --------------------------------------------------------------------------
# the structural human-only guard (same pattern as boundary.HumanGate)
# --------------------------------------------------------------------------

def require_human_gate(gate: Any) -> HumanGate:
    """Every gate-action entrypoint calls this FIRST. A `HumanGate` passes
    through; anything else (an `OutputBoundary` = the machinery/agent chokepoint,
    or any other object) is REJECTED and REPORTED — appended to the offending
    object's own refusal ledger when it has one, then raised as a
    `BoundaryViolation` carrying the structured `Refusal`. So an agent path can
    neither reach a gate side effect nor do so silently."""
    if isinstance(gate, HumanGate):
        return gate
    actor = (getattr(gate, "actor", None)
             or getattr(gate, "human_actor", None) or "non-human")
    refusal = Refusal(
        GATE_SIDE_EFFECT, str(actor), "<gate-console>",
        "a gate-console action requires a HumanGate constructed with an "
        "identified human actor; an OutputBoundary / agent path cannot invoke a "
        "gate action (gate authority is human-only by construction, D16)")
    ledger = getattr(gate, "refusals", None)
    if isinstance(ledger, list):
        ledger.append(refusal)
    raise BoundaryViolation(refusal)


# --------------------------------------------------------------------------
# shared helpers
# --------------------------------------------------------------------------

def _utcnow() -> str:
    """Wall-clock UTC (date-time). Gate records are LIVE audit entries, not the
    deterministic snapshot, so ordinary wall-clock is correct here."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stamp(at: str) -> str:
    """A filesystem-safe slug for an ISO timestamp (drops separators)."""
    return re.sub(r"[^0-9A-Za-z]", "", at) or "unstamped"


def _prefix(records_dir: str) -> str:
    return records_dir if records_dir.endswith("/") else records_dir + "/"


def _render_yaml(doc: Any, banner: str) -> str:
    body = yaml.safe_dump(doc, sort_keys=False, default_flow_style=False,
                          allow_unicode=True)
    return banner + body


def find_change(snapshot: dict, change_id: str) -> dict | None:
    for c in snapshot.get("changes") or []:
        if isinstance(c, dict) and c.get("id") == change_id:
            return c
    return None


def _flip_status(text: str, new_status: str) -> str:
    """Rewrite the first `Status:` header value in the doc's header window.
    A no-op when the document carries no `Status:` header (e.g. tasks.md,
    a `.openspec.yaml`)."""
    lines = text.splitlines(keepends=True)
    limit = min(len(lines), HEADER_SCAN_LINES)
    for i in range(limit):
        if lines[i].startswith("Status:"):
            nl = "\n" if lines[i].endswith("\n") else ""
            lines[i] = f"Status: {new_status}{nl}"
            return "".join(lines)
    return text


# --------------------------------------------------------------------------
# gate-action record (pure builder)
# --------------------------------------------------------------------------

def build_gate_action_record(
    *, actor: str, action: str, at: str,
    artifacts: Sequence[dict], change_id: str | None = None,
    possible_id: str | None = None, outcome: str | None = None,
    topic_id: str | None = None, cluster_id: str | None = None,
    project_id: str | None = None,
    reason: str | None = None, citation: str | None = None,
    document: str | None = None, notes: str | None = None,
    ref: str | None = None, provenance: "Provenance | None" = None,
) -> dict:
    """A schema-valid `gate-action-record` (validated by the pinned validator).
    `artifacts` are `{kind, reference}` entries; the per-action companion
    requirements (demote->reason, ratify->ratification-record,
    kickoff->workflow-job, dispose-possible->register-update + possible_id/
    outcome + rejected->reason+citation, propose->workflow-job + topic_id)
    are the callers' responsibility and are asserted by the validator. The
    four change-lifecycle actions target a `change_id`; `dispose-possible`
    targets a `possible_id` + `outcome`; `propose` targets a staging
    `topic_id` (add-propose-verb).

    `ref` (add-workbench-branch-sessions, chg 1.1) names the SESSION BRANCH a
    branch-session action acted on. It stays OPTIONAL in the schema and is
    recorded only when given — so every pre-existing verb's record is byte
    identical — but inside a session the ROUTE always populates it, because a
    session record that does not name its branch audits nothing (D13,
    data-model record shapes).

    `provenance` (D23; Brett's 2026-07-27 ruling) is the GATEWAY fact: which door
    the invocation arrived on and how console presence was shown. It is a
    `Provenance` INSTANCE and nothing else — a mapping is refused — because the
    only honest source is the gateway that observed the fact, and a value that
    could be spelled by a request body would be worthless. It is NOT re-derived
    here: this builder has no way to know which surface called it, and guessing
    would be exactly the invisible-residual problem the ruling closes. Absent
    (`None`) it is omitted, and the record is byte-identical to a pre-growth one —
    which is what keeps every committed record valid, the schema's own reason for
    requiring `provenance` in no conditional."""
    target: dict[str, Any] = {}
    if change_id:
        target["change_id"] = change_id
    if possible_id:
        target["possible_id"] = possible_id
    if topic_id:
        target["topic_id"] = topic_id
    if cluster_id:
        target["cluster_id"] = cluster_id
    if project_id:
        target["project_id"] = project_id
    if outcome:
        target["outcome"] = outcome
    if document:
        target["document"] = document
    if ref and str(ref).strip():
        target["ref"] = str(ref).strip()
    record: dict[str, Any] = {
        "schema_version": RECORD_SCHEMA_VERSION,
        "kind": RECORD_KIND,
        "actor": actor,
        "action": action,
        "target": target,
    }
    if provenance is not None:
        if not isinstance(provenance, Provenance):
            raise GateRefused(
                "gateway provenance is an OBSERVED fact, not a supplied value: it "
                "must be a `Provenance` the gateway constructed after running its "
                "own console-presence test. A mapping — which is what a request "
                "body could carry — is refused, because a self-declared surface "
                "tags nothing (D23)")
        # placed between `target` and `at`, the schema's own property order
        record["provenance"] = provenance.as_record()
    record["at"] = at
    record["artifacts"] = [dict(a) for a in artifacts]
    if reason:
        record["reason"] = reason
    if citation:
        record["citation"] = citation
    if notes:
        record["notes"] = notes
    return record


def gate_action_record_relpath(records_dir: str, action: str, target_id: str, at: str) -> str:
    return f"{_prefix(records_dir)}{target_id}/{action}-{_stamp(at)}.gate-action.yaml"


# AMENDED 2026-07-27 (design D23; Brett's ruling, item 2). This banner used to say
# "Agents structurally cannot author one (the console rejects any non-human caller
# before a record is ever written)" — a claim the console's control cannot keep. The
# boundary is a CONSOLE-PRESENCE test (anti-CSRF / same-origin), not authentication:
# a process running as the identified human can read this serve's own console token
# or declare presence on the CLI. Brett accepted that residual (item 1) and required
# the record to name the door instead (item 3, the `provenance` block below the
# target). A banner promising more than the gate enforces is the same defect class
# the ruling corrected in the ratified scenarios, so it is corrected here too.
_RECORD_BANNER = (
    "# gate-action record — a HUMAN-gate console action audit entry\n"
    "# (gate-action-record.schema.yaml). A session verb is reachable only from the\n"
    "# human console: a caller that cannot show it originates there is rejected and\n"
    "# reported before any record is written. That is a console-PRESENCE control,\n"
    "# not authentication (design D23) — `provenance`, where present, names the\n"
    "# door this action came through and how presence was shown.\n"
)


def document_target_id(document: str) -> str:
    """The record-path segment for a DOCUMENT-only target
    (add-workbench-bullseye-and-create, design D10 consequence b): the
    repo-relative path, extension dropped and slugged, so
    `ideation/brainstorm/lens-launch.md` files its records under
    `ideation-brainstorm-lens-launch/`. Slugged for the same reason every other
    path segment here is — a hostile value can never traverse the records tree."""
    from .workbench import slug
    stem = str(document or "").rsplit(".", 1)[0]
    return slug(stem.replace("/", "-"))


def ref_target_id(ref: str) -> str:
    """The record-path segment for a SESSION-REF-only target
    (add-workbench-branch-sessions, plan Constraint 10): the session branch,
    slugged, so `cluster/cl-a` files its records under `cluster-cl-a/`. Slugged
    for the same reason every other path segment here is — a hostile value can
    never traverse the records tree."""
    from .workbench import slug
    return slug(str(ref or "").replace("/", "-"))


def write_gate_action_record(gate: HumanGate, records_dir: str, record: dict) -> Path:
    """Write the record under `<records_dir>/<target_id>/<action>-<stamp>...`.

    The `target_id` derivation accepts, in order, the change/possible/topic
    identifiers the pre-existing verbs target, then — additively — a
    DOCUMENT-only target (`create-document`, which has none of the other
    three and used to `KeyError` here), then — additively again — a SESSION
    `ref` (add-workbench-branch-sessions, plan Constraint 10), so an `open-pr`
    or `abandon-session` record on a cluster or possible tile still has a target
    id. The `ref` fallback comes AFTER `document` deliberately: an
    `edit-document` record names both, and it must keep filing under its
    document exactly where `create-document` already files. Existing verbs'
    filenames are unchanged: they still resolve on the first three keys exactly
    as before."""
    target = record["target"]
    # `cluster_id` joins the first-class keys additively (add-wheel-action-verbs
    # 011): `derive-possibles` is the first verb whose target is a cluster, and
    # without it a cluster-targeted record has no filename to file under.
    # Appended AFTER the existing three so every pre-existing verb's filename is
    # byte-identical. `project_id` joins the same way
    # (add-project-scoped-selection): `create-project` is the first verb whose
    # target is a register project.
    target_id = (target.get("change_id") or target.get("possible_id")
                 or target.get("topic_id") or target.get("cluster_id")
                 or target.get("project_id"))
    if not target_id and target.get("document"):
        target_id = document_target_id(target["document"])
    if not target_id and target.get("ref"):
        target_id = ref_target_id(target["ref"])
    if not target_id:
        raise GateRefused(
            "a gate-action record must name what it acted on "
            "(change_id, possible_id, topic_id, cluster_id, project_id, "
            "document, or a session ref)")
    rel = gate_action_record_relpath(records_dir, record["action"], target_id, record["at"])
    return gate.write_gate_artifact(rel, _render_yaml(record, _RECORD_BANNER))


# ==========================================================================
# DEMOTE — the mechanized reverse transition (T033)
# ==========================================================================

@dataclass(frozen=True)
class FileMove:
    """One reverse-transition file move: a change artifact returning to the
    staging topic. `status_flip` (when set) rewrites the moved copy's `Status:`
    header — proposal documents CONTINUE AS DRAFT IDEAS in the topic's openspec/
    workspace (the draft-proposal convention)."""
    from_path: str          # repo-relative source (inside the change folder)
    to_path: str            # repo-relative destination (inside the staging topic)
    role: str               # proposal-draft | design-draft | spec-delta | tasks | supporting-doc | openspec-config | other
    status_flip: str | None


@dataclass(frozen=True)
class DemotionPlan:
    change_id: str
    staging_topic: str
    change_folder: str
    topic_path: str          # ideation/staging/<topic>
    openspec_workspace: str  # ideation/staging/<topic>/openspec
    reason: str
    moves: tuple[FileMove, ...]
    withdrawn_picks: tuple[str, ...]   # register pick edges (change_id inheritance) to withdraw


def classify_change_file(rel_within_change: str) -> tuple[str, str, str | None]:
    """(role, dest_rel_within_topic, status_flip) for one change file, purely
    from its change-relative path. The reverse of the OpenSpec change-folder
    convention (mirrors explorer.js `classifyChangeFile`): proposal/design/spec
    deltas/tasks/openspec-config land in the topic's `openspec/` draft workspace;
    supporting-docs return to the topic root. Markdown drafts flip to
    `Status: draft`; non-markdown carry no Status header (flip is a no-op)."""
    base = rel_within_change.split("/")[-1]
    flip = DRAFT_STATUS if base.endswith(".md") else None
    if base == "proposal.md":
        return "proposal-draft", f"openspec/{rel_within_change}", flip
    if base == "design.md":
        return "design-draft", f"openspec/{rel_within_change}", flip
    if base == "tasks.md":
        return "tasks", f"openspec/{rel_within_change}", None
    if base == ".openspec.yaml":
        return "openspec-config", f"openspec/{rel_within_change}", None
    if re.search(r"(^|/)specs/", rel_within_change):
        return "spec-delta", f"openspec/{rel_within_change}", flip
    if re.search(r"(^|/)supporting-docs/", rel_within_change):
        return "supporting-doc", base, flip
    return "other", f"openspec/{rel_within_change}", flip


def plan_demotion(
    snapshot: dict, change_id: str, *, reason: str, staging_topic: str | None = None,
) -> DemotionPlan:
    """PURE: derive the reverse-transition plan for `change_id` from the snapshot
    (no I/O, no writes). Refuses (GateRefused) an empty reason, an unknown or
    non-active change, or a change with no resolvable origin staging topic."""
    if not (reason and reason.strip()):
        raise GateRefused(
            "a demotion REQUIRES a recorded reason — the durable 'why' a change "
            "went back to staging (gate-action-record demote allOf)")
    change = find_change(snapshot, change_id)
    if change is None:
        raise GateRefused(f"unknown change {change_id!r} (not in the snapshot)")
    if change.get("status") != "active":
        raise GateRefused(
            f"change {change_id!r} is {change.get('status')!r}; only an active "
            "proposal is demoted back to staging")
    topic = staging_topic or change.get("origin_staging_id")
    if not topic:
        raise GateRefused(
            f"change {change_id!r} has no recorded origin staging topic; pass "
            "staging_topic explicitly to target the reverse transition")

    folder = change.get("folder") or f"openspec/changes/{change_id}"
    topic_path = f"ideation/staging/{topic}"
    openspec_ws = f"{topic_path}/openspec"

    moves: list[FileMove] = []
    for path in change.get("files") or []:
        if not path.startswith(folder + "/"):
            continue
        rel_within = path[len(folder) + 1:]
        role, dest_rel, flip = classify_change_file(rel_within)
        moves.append(FileMove(
            from_path=path, to_path=f"{topic_path}/{dest_rel}", role=role, status_flip=flip))

    withdrawn = tuple(sorted(
        p["id"] for p in snapshot.get("possibles") or []
        if isinstance(p, dict) and (p.get("pick") or {}).get("change_id") == change_id and p.get("id")
    ))

    return DemotionPlan(
        change_id=change_id, staging_topic=topic, change_folder=folder,
        topic_path=topic_path, openspec_workspace=openspec_ws, reason=reason.strip(),
        moves=tuple(moves), withdrawn_picks=withdrawn)


def transition_manifest(plan: DemotionPlan, *, actor: str, at: str,
                        source_revision: str | None = None) -> dict:
    """The reverse-transition manifest (the demotion record): a structured,
    human-readable statement of the transition, shaped after the change's own
    `first-transition.manifest.yaml` promotion manifest but REVERSED — the
    change's artifacts return to the staging topic."""
    return {
        "format_version": 1,
        "transition": "demote",
        "change_id": plan.change_id,
        "destination": {
            "kind": "staged",
            "id": plan.staging_topic,
            "path": plan.topic_path,
            "openspec_workspace": plan.openspec_workspace,
        },
        "origin": {"kind": "change", "path": plan.change_folder},
        "actor": actor,
        "reason": plan.reason,
        "transitioned_at": at,
        "source_revision": source_revision,
        "files": [
            {"from": m.from_path, "to": m.to_path, "role": m.role,
             "status_flip": m.status_flip}
            for m in plan.moves
        ],
        "register_edits": {
            "withdraw_pick_edges": list(plan.withdrawn_picks),
            "note": "each listed possible's pick edge (change_id inheritance) is "
                    "withdrawn — the returning idea keeps its id (it was never "
                    "terminal, so no resurrection is required).",
        },
        "readme_index_update": (
            f"{plan.topic_path}/README.md gains a 'Returned drafts' record and "
            f"{plan.openspec_workspace}/INDEX.md lists the returned draft proposals."),
    }


def executable_plan(plan: DemotionPlan, *, actor: str, at: str) -> dict:
    """The ordered, executable step list — what `execute_demotion_plan` (or a
    human running the plan by hand) performs, one operation per step."""
    steps: list[dict[str, Any]] = []
    for m in plan.moves:
        step: dict[str, Any] = {"op": "move", "from": m.from_path, "to": m.to_path}
        if m.status_flip:
            step["set_status"] = m.status_flip
        steps.append(step)
    steps.append({"op": "update-readme", "path": f"{plan.topic_path}/README.md",
                  "record": f"demoted {plan.change_id} ({at})"})
    steps.append({"op": "write-index", "path": f"{plan.openspec_workspace}/INDEX.md"})
    if plan.withdrawn_picks:
        steps.append({"op": "withdraw-picks", "register": "possibles",
                      "ids": list(plan.withdrawn_picks)})
    steps.append({"op": "remove-empty", "path": plan.change_folder})
    return {
        "format_version": 1,
        "plan": "demote",
        "change_id": plan.change_id,
        "staging_topic": plan.staging_topic,
        "actor": actor,
        "at": at,
        "steps": steps,
    }


def register_update_note(plan: DemotionPlan, *, at: str) -> str:
    """The register-update artifact body: a human-runnable note describing the
    possibles-register edit the demotion implies."""
    if plan.withdrawn_picks:
        ids = "\n".join(f"- {pid}" for pid in plan.withdrawn_picks)
    else:
        ids = "- (none — no picked possible inherited this change id)"
    return (
        f"# Register update — demote {plan.change_id} ({at})\n\n"
        "Withdraw the pick edge (change_id inheritance) for the following "
        "possibles-register entries; each returns toward the staging backlog and "
        "KEEPS its id (it was never terminal, so no resurrection is required):\n\n"
        f"{ids}\n\n"
        "> A human applies this edit to the consolidated possibles register; the "
        "> console emits the note but enters nothing into the register itself.\n")


@dataclass
class DemoteResult:
    plan: DemotionPlan
    gate_action_record: dict
    record_path: Path
    manifest_path: Path
    plan_path: Path
    register_update_path: Path


def demote(
    gate: Any, snapshot: dict, change_id: str, *, reason: str,
    staging_topic: str | None = None, at: str | None = None,
    records_dir: str = DEFAULT_RECORDS_DIR, source_revision: str | None = None,
    provenance: Provenance | None = None,
) -> DemoteResult:
    """Plan + RECORD the reverse transition (the console action). Writes the
    transition manifest, the executable plan, the register-update note, and the
    gate-action record through the HumanGate; it does NOT touch the live corpus
    (execution is `execute_demotion_plan`, a separate human-driven step). Every
    entrypoint demands a HumanGate."""
    human = require_human_gate(gate)
    at = at or _utcnow()
    plan = plan_demotion(snapshot, change_id, reason=reason, staging_topic=staging_topic)
    rev = source_revision or (snapshot.get("generation") or {}).get("source_revision")

    base = f"{_prefix(records_dir)}{change_id}"
    stamp = _stamp(at)
    manifest = transition_manifest(plan, actor=human.human_actor, at=at, source_revision=rev)
    manifest_path = human.write_gate_artifact(
        f"{base}/demote-{stamp}.transition-manifest.yaml",
        _render_yaml(manifest, "# reverse-transition (demotion) manifest — the demotion record.\n"))
    plan_doc = executable_plan(plan, actor=human.human_actor, at=at)
    plan_path = human.write_gate_artifact(
        f"{base}/demote-{stamp}.plan.yaml",
        _render_yaml(plan_doc, "# executable demotion plan — run with `cli.py gate demote --execute` or by hand.\n"))
    reg_path = human.write_gate_artifact(
        f"{base}/demote-{stamp}.register-update.md", register_update_note(plan, at=at))

    record = build_gate_action_record(
        actor=human.human_actor, action=ACTION_DEMOTE, change_id=change_id, at=at,
        reason=plan.reason, provenance=provenance,
        artifacts=[
            {"kind": ART_TRANSITION_MANIFEST, "reference": _rel_to_records(manifest_path, human)},
            {"kind": ART_OTHER, "reference": _rel_to_records(plan_path, human)},
            {"kind": ART_REGISTER_UPDATE, "reference": _rel_to_records(reg_path, human)},
        ])
    record_path = write_gate_action_record(human, records_dir, record)
    return DemoteResult(plan, record, record_path, manifest_path, plan_path, reg_path)


# --------------------------------------------------------------------------
# PROMOTABILITY — the `promote-to-staging` precondition (add-wheel-action-verbs
# design D3; 011 FR-010/FR-011)
#
# Promotion is the organize-gate act, so what is promotable is fixed by the
# register kernel rather than by new policy: `latent` + (human-authored |
# accepted human disposition). READ FROM THE REGISTER in the pinned checkout —
# never from the snapshot, which trails it between bakes.
#
# THREE PROHIBITED SHORTCUTS. Each looks right and is wrong:
#
#   1. `derivation.disposition` is NOT the signal. The kernel pins it to the
#      CONSTANT `pending_review` for the life of a derived entry, including
#      after a human accepts (`dispose_possible` above preserves it verbatim,
#      and its test asserts so). A guard reading it never opens.
#   2. `doc_health.derive_possibles._is_undisposed` is NOT this predicate. It
#      answers the derivation lane's cluster-skip question — "has a human
#      looked at this yet" — so it treats a `deferred` verdict as DISPOSED and
#      says nothing about accepted vs rejected. Reusing it would silently make
#      deferred possibles promotable.
#   3. The snapshot's `possible` projection is a stale VIEW. The wheel computes
#      an approximation from it to decide what to OFFER; this function is what
#      decides what is ALLOWED, and it re-reads the checkout.
#
# A `deferred` verdict is therefore NOT an acceptance: it leaves the possible
# awaiting a real ruling.
# --------------------------------------------------------------------------

_PROMOTABLE_STATE = "latent"
_ORIGIN_AI_DERIVED = "ai-derived"
_ORIGIN_HUMAN = "human-authored"
_ACCEPTED = "accepted"


def promotability_refusal(entry: Any) -> str | None:
    """The reason `entry` may NOT be promoted to staging, or None when it may.

    Fail-closed: anything that is not a well-formed, promotable register entry
    yields a reason rather than being admitted by omission.
    """
    if not isinstance(entry, dict):
        return "no such possible in the pinned checkout's register"
    state = entry.get("state")
    if state != _PROMOTABLE_STATE:
        if state in ("rejected", "superseded"):
            return (f"possible is {state!r} — a terminal state; a revived "
                    "candidate is a NEW register entry with a new id")
        if state == "picked":
            return ("possible is 'picked' — it already carries its own pick "
                    "edge, so promoting it again would duplicate it")
        return (f"possible has state {state!r}, and only a 'latent' possible "
                "is promotable")
    origin = entry.get("origin")
    if origin in (None, _ORIGIN_HUMAN):
        return None                     # human-authored: accepted by construction
    if origin != _ORIGIN_AI_DERIVED:
        return f"possible has an unrecognised origin {origin!r}"
    # ai-derived: promotion presupposes an ACCEPTED human verdict. The machine
    # `derivation.disposition` is deliberately not consulted (shortcut 1).
    derivation = entry.get("derivation")
    verdict = (derivation or {}).get("human_disposition") \
        if isinstance(derivation, dict) else None
    outcome = (verdict or {}).get("outcome") if isinstance(verdict, dict) else None
    if outcome == _ACCEPTED:
        return None
    if outcome == "deferred":
        return ("derived possible carries a 'deferred' human disposition, "
                "which is not an acceptance — rule on it before promoting")
    if outcome is None:
        return ("derived possible has no human disposition yet — dispose it "
                "on the gate console before promoting")
    return (f"derived possible's human disposition is {outcome!r}, "
            "not 'accepted'")


def is_promotable(entry: Any) -> bool:
    """True when `entry` may be commissioned into staging (FR-010)."""
    return promotability_refusal(entry) is None


def load_possibles_register(root: Path | str) -> list[dict]:
    """The possibles register from the PINNED CHECKOUT's cross-reference index.

    READ-ONLY, and deliberately tolerant: an absent or unreadable index yields
    an empty register, so the callers' "no such possible" refusal fires rather
    than an exception escaping the gate. The register is never written here —
    the commission verbs are non-mutating by contract (FR-008).
    """
    from doc_health import derive_possibles as dp   # lazy: sibling package cycle

    path = Path(root) / dp.INDEX_REL
    try:
        index = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return []
    if not isinstance(index, dict):
        return []
    register = index.get(dp.REGISTER_KEY)
    return [e for e in register if isinstance(e, dict)] if isinstance(register, list) else []


def find_possible(root: Path | str, possible_id: str) -> dict | None:
    """The register entry for `possible_id` in the pinned checkout, or None."""
    for entry in load_possibles_register(root):
        if entry.get("id") == possible_id:
            return entry
    return None


def _rel_to_records(path: Path, human: HumanGate) -> str:
    """A record's artifact reference, repo-relative to the gate's output root."""
    try:
        return path.relative_to(human.output.root).as_posix()
    except ValueError:
        return path.as_posix()


# --------------------------------------------------------------------------
# demote EXECUTION — the file moves (separate, human-driven; tested vs a fixture)
# --------------------------------------------------------------------------

@dataclass
class DemotionExecution:
    moved: list[tuple[str, str]] = field(default_factory=list)
    readme_path: Path | None = None
    index_path: Path | None = None
    removed_change_folder: bool = False


def execute_demotion_plan(plan: DemotionPlan, tree_root: Path | str, *, at: str | None = None) -> DemotionExecution:
    """APPLY the reverse transition to a real tree — the legitimate way material
    (re-)enters `ideation/staging/` is exactly this human gate action. v1
    exercises it against an in-test FIXTURE change tree; `cli.py gate demote
    --execute` runs it against a real checkout a human drives. Moves each file
    (flipping Status where the plan says), records the return in the topic
    README, writes the openspec-workspace INDEX, and removes the emptied change
    folder."""
    root = Path(tree_root).resolve()
    at = at or _utcnow()
    result = DemotionExecution()

    for m in plan.moves:
        src = root / m.from_path
        dst = root / m.to_path
        if not src.is_file():
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        if m.status_flip:
            text = _flip_status(text, m.status_flip)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
        src.unlink()
        result.moved.append((m.from_path, m.to_path))

    # README record (append; create if absent).
    readme = root / plan.topic_path / "README.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    returned = [m.to_path for m in plan.moves]
    note = (f"\n## Returned drafts (demoted {plan.change_id}, {at[:10]})\n\n"
            f"Reason: {plan.reason}\n\n"
            + "\n".join(f"- {r}" for r in returned) + "\n")
    if readme.is_file():
        readme.write_text(readme.read_text(encoding="utf-8") + note, encoding="utf-8")
    else:
        readme.write_text(f"# {plan.staging_topic}\n\nStatus: staged\n" + note, encoding="utf-8")
    result.readme_path = readme

    # openspec/ workspace INDEX of the returned draft proposals.
    index = root / plan.openspec_workspace / "INDEX.md"
    index.parent.mkdir(parents=True, exist_ok=True)
    ws_files = [m.to_path for m in plan.moves if m.to_path.startswith(plan.openspec_workspace + "/")]
    index.write_text(
        f"# openspec/ draft workspace — {plan.staging_topic}\n\n"
        f"Draft proposals returned from demoted change {plan.change_id} "
        f"({at[:10]}). These continue as draft ideas per the draft-proposal "
        f"convention:\n\n" + ("\n".join(f"- {p}" for p in ws_files) or "- (none)") + "\n",
        encoding="utf-8")
    result.index_path = index

    # Remove the now-empty change folder (best effort).
    change_dir = root / plan.change_folder
    if change_dir.is_dir():
        shutil.rmtree(change_dir, ignore_errors=True)
        result.removed_change_folder = not change_dir.exists()

    return result


# ==========================================================================
# RATIFY — approve; write the ratification record + register update (T034)
# ==========================================================================

def build_ratification_record(change_id: str, ratifier: str, *, date: str) -> dict:
    """The ratification record artifact (ratifier + date) — the same content a
    manual ratification records on the proposal (`Ratified by:` + the ratify
    date the generator reads back into `changes[].ratification`)."""
    return {
        "kind": ART_RATIFICATION_RECORD,
        "schema_version": 1,
        "change_id": change_id,
        "ratifier": ratifier,
        "date": date,
    }


@dataclass
class RatifyResult:
    ratification: dict
    gate_action_record: dict
    record_path: Path
    ratification_path: Path
    register_update_path: Path


def ratify(
    gate: Any, change_id: str, ratifier: str, *, at: str | None = None,
    date: str | None = None, records_dir: str = DEFAULT_RECORDS_DIR,
    provenance: Provenance | None = None,
) -> RatifyResult:
    """Approve a proposal: write the ratification record (ratifier, date) and a
    register-update note, and emit a gate-action record that CARRIES the
    ratification-record artifact reference (the schema's ratify contains-rule).
    Human-only; every entrypoint demands a HumanGate."""
    human = require_human_gate(gate)
    at = at or _utcnow()
    date = date or at[:10]
    base = f"{_prefix(records_dir)}{change_id}"
    stamp = _stamp(at)

    ratification = build_ratification_record(change_id, ratifier, date=date)
    rat_path = human.write_gate_artifact(
        f"{base}/ratify-{stamp}.ratification-record.yaml",
        _render_yaml(ratification, "# ratification record — ratifier + date recorded on approval.\n"))
    reg_note = (
        f"# Register update — ratify {change_id} ({date})\n\n"
        f"Ratifier: {ratifier}. Record the ratification on the change "
        f"(`Ratified by: {ratifier}`) and update the registers to reflect the "
        f"ratified state.\n\n"
        "> The console writes this note; a human applies the register edit and "
        "> the `Ratified by:` header. Identical artifacts to a manual ratification.\n")
    reg_path = human.write_gate_artifact(f"{base}/ratify-{stamp}.register-update.md", reg_note)

    record = build_gate_action_record(
        actor=human.human_actor, action=ACTION_RATIFY, change_id=change_id, at=at,
        provenance=provenance,
        artifacts=[
            {"kind": ART_RATIFICATION_RECORD, "reference": _rel_to_records(rat_path, human)},
            {"kind": ART_REGISTER_UPDATE, "reference": _rel_to_records(reg_path, human)},
        ])
    record_path = write_gate_action_record(human, records_dir, record)
    return RatifyResult(ratification, record, record_path, rat_path, reg_path)


# ==========================================================================
# EDIT-APPLY — apply a HUMAN-approved redline (T034); AI drafting is OUT
# ==========================================================================

@dataclass(frozen=True)
class Redline:
    """A HUMAN-approved revision the console applies verbatim. Two forms:
    REPLACEMENT-BLOCK (`old_text` -> `new_text`, exact and unique) or FULL-TEXT
    (`full_text` replaces the whole document). `concept` optionally names the
    listed concept the revision addresses. The AI-drafting of redlines is a
    follow-on delta — this console never authors one; it applies what a human
    supplies."""
    old_text: str | None = None
    new_text: str | None = None
    full_text: str | None = None
    concept: str | None = None

    def form(self) -> str:
        if self.full_text is not None:
            return "full-text"
        if self.old_text is not None and self.new_text is not None:
            return "replacement-block"
        raise ValueError(
            "a redline is either a replacement-block (old_text + new_text) or a "
            "full-text replacement (full_text)")


def apply_redline(text: str, redline: Redline) -> str:
    """PURE: apply the redline to `text`, changing EXACTLY the redline and
    nothing else. A replacement-block MUST match its `old_text` exactly once
    (an ambiguous or absent block is refused, so the console never silently
    edits the wrong span)."""
    form = redline.form()
    if form == "full-text":
        return redline.full_text  # type: ignore[return-value]
    count = text.count(redline.old_text)  # type: ignore[arg-type]
    if count != 1:
        raise ValueError(
            f"replacement-block old_text matches {count} time(s) in the document "
            "(a redline must match exactly once — a human applies a precise span)")
    return text.replace(redline.old_text, redline.new_text, 1)  # type: ignore[arg-type]


def redline_artifact(document: str, redline: Redline) -> dict:
    """The redline the record carries — exactly what the human approved."""
    out: dict[str, Any] = {"kind": ART_REDLINE, "document": document, "form": redline.form()}
    if redline.concept:
        out["concept"] = redline.concept
    if redline.full_text is not None:
        out["full_text"] = redline.full_text
    else:
        out["old_text"] = redline.old_text
        out["new_text"] = redline.new_text
    return out


# Concept-list extraction: the console "lists the artifact's main concepts"
# (requirements, decisions, section headings) so a human can pick one to revise.
# Extraction only — AI drafting of the revision is OUT of scope (follow-on delta).
_HEADING_RE = re.compile(r"(?m)^(#{2,4})\s+(.*\S)\s*$")


def list_concepts(text: str) -> list[str]:
    """The document's main concepts: its `##`/`###`/`####` section headings
    (including `### Requirement:` / `### Decision:` blocks) in document order."""
    return [m.group(2).strip() for m in _HEADING_RE.finditer(text)]


@dataclass
class EditApplyResult:
    document: str
    applied_path: Path
    before: str
    after: str
    redline: dict
    gate_action_record: dict
    record_path: Path
    redline_path: Path


def edit_apply(
    gate: Any, change_id: str, document: str, redline: Redline, *,
    at: str | None = None, records_dir: str = DEFAULT_RECORDS_DIR,
    tree_root: Path | str | None = None, provenance: Provenance | None = None,
) -> EditApplyResult:
    """Apply a human-approved redline to a change `document` through the gate:
    the source changes only here, when a human runs this action (the gate
    authority). Writes the redline artifact and a gate-action record carrying
    it. Human-only; every entrypoint demands a HumanGate."""
    human = require_human_gate(gate)
    at = at or _utcnow()
    root = Path(tree_root).resolve() if tree_root is not None else human.output.root
    target = (root / document).resolve()
    before = target.read_text(encoding="utf-8")
    after = apply_redline(before, redline)
    target.write_text(after, encoding="utf-8")

    art = redline_artifact(document, redline)
    base = f"{_prefix(records_dir)}{change_id}"
    stamp = _stamp(at)
    redline_path = human.write_gate_artifact(
        f"{base}/edit-apply-{stamp}.redline.yaml",
        _render_yaml(art, "# redline — the HUMAN-approved revision the console applied verbatim.\n"))
    record = build_gate_action_record(
        actor=human.human_actor, action=ACTION_EDIT_APPLY, change_id=change_id, at=at,
        document=document, provenance=provenance,
        artifacts=[{"kind": ART_REDLINE, "reference": _rel_to_records(redline_path, human)}])
    record_path = write_gate_action_record(human, records_dir, record)
    return EditApplyResult(document, target, before, after, art, record, record_path, redline_path)


# ==========================================================================
# GateConsole — the human-only facade (every action demands a HumanGate)
# ==========================================================================

# ==========================================================================
# DISPOSE-POSSIBLE — the human verdict on a pending_review ai-derived
# possible (add-possibles-derivation-lane, "One-way derived-possible
# disposition on the gate console"). The register-side lifecycle rules live
# in `doc_health.derive_possibles.apply_disposition` (accept -> first-class
# `latent` retaining `origin: ai-derived`; reject -> `rejected` with the
# REQUIRED reason + citation; defer -> re-disposable; one-way otherwise;
# the machine `derivation.disposition` stays `pending_review` forever).
# This console action wraps that primitive in the house gate discipline:
# HumanGate-only, validate-before-persist against the pinned openxFactory
# index validator, and a schema-valid gate-action record beside the write.
# ==========================================================================

@dataclass
class DisposePossibleResult:
    possible_id: str
    outcome: str
    entry: dict
    index_path: Path
    index_md_path: Path | None
    record_path: Path


def dispose_possible(gate: Any, possible_id: str, outcome: str, *,
                     reason: str | None = None, citation: str | None = None,
                     note: str | None = None, at: str | None = None,
                     records_dir: str = DEFAULT_RECORDS_DIR,
                     index_validator: Path | None = None,
                     provenance: Provenance | None = None) -> DisposePossibleResult:
    """Dispose ONE pending_review derived possible in the checkout's
    `ideation/cross-reference.yaml`. The checkout root is the HumanGate's own
    root (the pinned openxFactory checkout the CLI was pointed at). Raises
    `GateRefused` on any precondition the register machinery rejects (unknown
    id, not ai-derived, already disposed, uncited rejection) or when the
    pinned validator rejects the updated index — nothing is persisted on any
    refusal path."""
    from doc_health import derive_possibles as dp  # lazy: sibling package

    human = require_human_gate(gate)
    root = human.output.root
    at = at or _utcnow()
    index_path = root / dp.INDEX_REL
    try:
        index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise GateRefused(f"cross-reference index unreadable at "
                          f"{index_path}: {exc}") from exc
    if not isinstance(index, dict):
        raise GateRefused(f"cross-reference index at {index_path} is not a "
                          "mapping")

    try:
        updated = dp.apply_disposition(
            index, possible_id, outcome=outcome,
            authority=human.human_actor, at=at[:10], note=note,
            reason=reason, citation=citation)
    except dp.DispositionError as exc:
        raise GateRefused(str(exc)) from exc

    # validate BEFORE persistence (OS temp dir, never the repo tree — the
    # derive lane's own staging pattern); a rejected index persists nothing.
    import tempfile
    tmp_dir = tempfile.mkdtemp(prefix="dispose-possible-")
    candidate = Path(tmp_dir) / "candidate.yaml"
    try:
        candidate.write_text(dp.render_index_yaml(updated), encoding="utf-8")
        ok, detail = dp.validate_index(candidate, validator=index_validator,
                                       repo=root, strict=True)
    finally:
        candidate.unlink(missing_ok=True)
        try:
            Path(tmp_dir).rmdir()
        except OSError:
            pass
    if ok is not True:
        raise GateRefused(
            "updated index rejected by the pinned validator"
            if ok is False else "index validator unreachable"
            + f": {detail}")

    human.write_gate_artifact(dp.INDEX_REL, dp.render_index_yaml(updated))
    index_md_path = None
    from doc_health import ideation_readiness as ir  # lazy: shared renderer
    md = ir._render_markdown(updated)
    if md is not None:
        index_md_path = human.write_gate_artifact(dp.INDEX_MD_REL, md)

    record = build_gate_action_record(
        actor=human.human_actor, action=ACTION_DISPOSE_POSSIBLE, at=at,
        possible_id=possible_id, outcome=outcome, provenance=provenance,
        reason=reason, citation=citation, notes=note,
        artifacts=[{"kind": ART_REGISTER_UPDATE,
                    "reference": f"{dp.INDEX_REL}#possibles_register"}])
    record_path = write_gate_action_record(human, records_dir, record)

    entry = next(e for e in updated.get(dp.REGISTER_KEY) or []
                 if isinstance(e, dict) and e.get("id") == possible_id)
    return DisposePossibleResult(
        possible_id=possible_id, outcome=outcome, entry=entry,
        index_path=root / dp.INDEX_REL, index_md_path=index_md_path,
        record_path=record_path)



class GateConsole:
    """Convenience facade binding one identified human's `HumanGate` to the four
    gate actions. Construction itself demands a HumanGate — an OutputBoundary /
    agent path is rejected and reported here, so no action is reachable without
    human authority."""

    def __init__(self, gate: Any, *, records_dir: str = DEFAULT_RECORDS_DIR) -> None:
        self.gate = require_human_gate(gate)
        self.actor = self.gate.human_actor
        self.records_dir = records_dir

    def demote(self, snapshot: dict, change_id: str, *, reason: str,
               staging_topic: str | None = None, at: str | None = None,
               source_revision: str | None = None,
               provenance: Provenance | None = None) -> DemoteResult:
        return demote(self.gate, snapshot, change_id, reason=reason,
                      staging_topic=staging_topic, at=at, records_dir=self.records_dir,
                      source_revision=source_revision, provenance=provenance)

    def ratify(self, change_id: str, ratifier: str, *, at: str | None = None,
               date: str | None = None,
               provenance: Provenance | None = None) -> RatifyResult:
        return ratify(self.gate, change_id, ratifier, at=at, date=date,
                      records_dir=self.records_dir, provenance=provenance)

    def dispose_possible(self, possible_id: str, outcome: str, *,
                         reason: str | None = None, citation: str | None = None,
                         note: str | None = None, at: str | None = None,
                         index_validator: Path | None = None,
                         provenance: Provenance | None = None) -> DisposePossibleResult:
        return dispose_possible(self.gate, possible_id, outcome,
                                reason=reason, citation=citation, note=note,
                                at=at, records_dir=self.records_dir,
                                index_validator=index_validator,
                                provenance=provenance)

    def edit_apply(self, change_id: str, document: str, redline: Redline, *,
                   at: str | None = None, tree_root: Path | str | None = None,
                   provenance: Provenance | None = None) -> EditApplyResult:
        return edit_apply(self.gate, change_id, document, redline, at=at,
                          records_dir=self.records_dir, tree_root=tree_root,
                          provenance=provenance)

    def kickoff(self, change_id: str, *, snapshot: dict | None = None,
                outline: str | None = None, workflow: str | None = None,
                at: str | None = None, provenance: Provenance | None = None):
        # Lazy import: kickoff.py imports this module for the shared record
        # helpers, so importing it at module top would be a cycle.
        from . import kickoff as kickoff_mod
        extra = {} if workflow is None else {"workflow": workflow}
        return kickoff_mod.kickoff(self.gate, change_id, snapshot=snapshot,
                                   outline=outline, at=at, records_dir=self.records_dir,
                                   provenance=provenance, **extra)

    def propose(self, topic_id: str, *, outline: str | None = None,
                workflow: str | None = None, note: str | None = None,
                at: str | None = None, session_precondition: Any = None,
                provenance: Provenance | None = None):
        from . import kickoff as kickoff_mod  # same cycle note as kickoff
        extra = {} if workflow is None else {"workflow": workflow}
        # `session_precondition` is the caller's FR-023 branch-session refusal
        # (007-workbench-branch-sessions T054); passed straight through, because
        # WHERE the engine evaluates it is the requirement — see `kickoff.propose`.
        return kickoff_mod.propose(self.gate, topic_id, outline=outline,
                                   note=note, at=at, records_dir=self.records_dir,
                                   session_precondition=session_precondition,
                                   provenance=provenance, **extra)

    # ---- the wheel action-row commissions (add-wheel-action-verbs; 011) ----
    # Same delegate shape as `propose`: bind this human's gate, pass the verb's
    # own optional arguments straight through, and let the engine own every
    # guard. `workflow` is omitted rather than passed as None so each engine's
    # own default applies.

    def promote_to_staging(self, possible_id: str, *, topic: str | None = None,
                           outline: str | None = None, workflow: str | None = None,
                           note: str | None = None, at: str | None = None,
                           provenance: Provenance | None = None):
        from . import kickoff as kickoff_mod   # same cycle note as kickoff
        extra = {} if workflow is None else {"workflow": workflow}
        return kickoff_mod.promote_to_staging(
            self.gate, possible_id, topic=topic, outline=outline, note=note,
            at=at, records_dir=self.records_dir, provenance=provenance, **extra)

    def derive_possibles(self, cluster_id: str, *, snapshot: dict | None = None,
                         outline: str | None = None, workflow: str | None = None,
                         note: str | None = None, at: str | None = None,
                         provenance: Provenance | None = None):
        from . import kickoff as kickoff_mod
        extra = {} if workflow is None else {"workflow": workflow}
        return kickoff_mod.derive_possibles(
            self.gate, cluster_id, snapshot=snapshot, outline=outline, note=note,
            at=at, records_dir=self.records_dir, provenance=provenance, **extra)

    def research_brief(self, possible_id: str, *, outline: str | None = None,
                       workflow: str | None = None, note: str | None = None,
                       at: str | None = None,
                       provenance: Provenance | None = None):
        from . import kickoff as kickoff_mod
        extra = {} if workflow is None else {"workflow": workflow}
        return kickoff_mod.research_brief(
            self.gate, possible_id, outline=outline, note=note, at=at,
            records_dir=self.records_dir, provenance=provenance, **extra)

    def create_project(self, name: str, *, repositories, roster=None,
                       register_source=None, outline: str | None = None,
                       workflow: str | None = None, note: str | None = None,
                       at: str | None = None,
                       provenance: Provenance | None = None):
        from . import kickoff as kickoff_mod
        extra = {} if workflow is None else {"workflow": workflow}
        return kickoff_mod.create_project(
            self.gate, name, repositories=repositories, roster=roster,
            register_source=register_source, outline=outline, note=note,
            at=at, records_dir=self.records_dir, provenance=provenance, **extra)
