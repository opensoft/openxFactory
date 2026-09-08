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
from typing import Any, Mapping, Sequence

import yaml

from doc_health import corpus

from . import record_binding
from . import round_trip
from .boundary import (
    DOCUMENT_ESCAPE,
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
ACTION_CLEANUP_ABANDONED_BRANCH = "cleanup-abandoned-branch"
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
# add-opendox-project-header (D15): the membership edit of an EXISTING
# project — same mechanic, the descriptor carrying add/remove member lists.
ACTION_EDIT_PROJECT = "edit-project"
# add-doxbench-editing-phase-b §12 (contract-v1.36): the doxBench workbench
# SHARE verb. It commits the session's dirty thread sidecars and PUSHES the
# session branch so a colleague can resume the session — and does nothing else.
# STRICTLY LESS than `open-pr`: it reuses that verb's existing remote-write path
# and opens no pull request, requests no review, and holds no approval or merge
# authority. ADDITIVE, same posture as every growth above.
ACTION_SHARE_SESSION = "share-session"

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

DEMOTION_EXECUTION_KIND = "demotion-execution-receipt"

# Default records prefix. A CALLER-DECLARED output path (the HumanGate allowlist);
# the aggregation lane wires the committed location (section 4). Not baked into
# any write here — only a default the CLI/tests may override.
DEFAULT_RECORDS_DIR = "ideation/dashboard/gate-records/"

DRAFT_STATUS = "draft"
# The status a returning PRIMARY FRAGMENT carries. Set positively rather than by
# omitting the flip, so a snapshot whose own header had drifted is normalized
# instead of returned as-is (align-demote-to-round-trip-rule).
STAGED_STATUS = "staged"


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
SURFACE_INTENT = "intent-plane"
SURFACES = (SURFACE_HTTP, SURFACE_CLI, SURFACE_INTENT)
# HOW console presence was shown. There is deliberately NO value meaning "not
# shown": an invocation that cannot demonstrate presence is refused before a
# record exists, so no record can honestly carry one. `declared` is the WEAKEST
# and is its own value so an audit consumer can filter for it.
PRESENCE_CONSOLE_TOKEN = "console-token"
PRESENCE_TTY = "tty"
PRESENCE_DECLARED = "declared"
PRESENCE_INGRESS = "ingress-auth"
CONSOLE_PRESENCES = (PRESENCE_CONSOLE_TOKEN, PRESENCE_TTY, PRESENCE_DECLARED,
                     PRESENCE_INGRESS)


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
# The intent plane (add-ideation-intent-plane task 4.3): the apply lane is the
# gateway, and the presence fact it observed is that the inbox stamped the
# actor from the ingress-authenticated identity. The lane constructs this pair
# itself — an intent body can no more claim provenance than an HTTP body can.
INTENT_INGRESS = Provenance(SURFACE_INTENT, PRESENCE_INGRESS)


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
    a `.openspec.yaml`).

    LINES ARE THE THREE REAL LINE ENDINGS AND NOTHING ELSE. This used
    `str.splitlines(keepends=True)`, which also breaks on `\\x0b`, `\\x0c`,
    `\\x1c`-`\\x1e`, `\\x85`, U+2028 and U+2029 — and `align-demote-to-round-trip-
    rule` newly routes a topic's PRIMARY FRAGMENT through here, which made two
    real damages reachable:

    * `Status: draft\\x0crest of the line` was seen as TWO pseudo-lines, so the
      first was replaced with no ending and the remainder was GLUED onto the new
      value: `Status: stagedrest of the line`. A line boundary the file does not
      contain was invented, and text moved across it.
    * A header carrying U+2028s inflates the pseudo-line count past the 15-line
      window, so a real `Status:` inside the header is never found and the flip
      silently does nothing — which failed the ratified "the restored fragment MUST
      carry `Status: staged`" scenario on input you get by pasting from a web page.

    Both are fixed by sharing `round_trip`'s split, and the fix is not confined to
    the fragment: every `openspec/`-bound document this verb flips to `draft` was
    exposed to the same two damages before.
    """
    rows = round_trip.split_keepends(text)
    index = _status_row(rows)
    if index is None:
        return text
    body, ending = rows[index]
    # The rewritten line keeps the ending it HAD (wave re-review P3): a CRLF
    # header must not be the one line that comes out LF.
    rows[index] = (f"Status: {new_status}", ending)
    return round_trip.join_rows(rows)


_STATUS_BODY_RE = re.compile(r"Status:\s*(\S+)\s*")


def _status_row(rows: list[tuple[str, str]]) -> int | None:
    """Index of the document's `Status:` header row, or None. The ONE scan
    `_flip_status` and `_add_status_header` share, so the question "does this
    document carry a header" gets the same answer from the side that rewrites one
    and the side that adds one.

    THE SAME GRAMMAR AS THE FORWARD GATE (`proposal-support._status_row`), and
    that alignment is the point rather than a tidy-up: this side decides whether a
    returned document needs a header ADDED, the forward gate decides whether it
    REFUSES the document, and where the two readers disagreed the demote left a
    topic one-way while believing it had not. Measured over the corpus, the old
    reader disagreed with the gate on 11 of 1148 documents, in both directions:

    * STRICT, not `startswith`. `Status: record (in progress — …)` satisfies a
      prefix test and fails the gate's `\\S+` grammar, so seven archived-change
      artifacts were judged headed here and refused there. It also means
      `_flip_status` no longer overwrites such a line — the parenthetical is a
      human's annotation, and rewriting it to a bare `Status: draft` was silent
      data loss dressed up as a status flip.
    * FENCE-AWARE. A `Status:` line inside a ``` block is an EXAMPLE. Reading it
      as the document's header flipped the example and left the real header alone.
    * NO 15-ROW WINDOW. A real header below row 15 was invisible here and visible
      to the gate, so `_add_status_header` inserted a SECOND one.

    `HEADER_SCAN_LINES` still bounds the INSERTION point search in
    `_add_status_header`, which is a different question — where a header belongs,
    not whether one is present."""
    flags = round_trip._fenced_flags(rows)
    for index, (body, _ending) in enumerate(rows):
        if flags[index]:
            continue
        if _STATUS_BODY_RE.fullmatch(body):
            return index
    return None


def _add_status_header(text: str, new_status: str) -> tuple[str, bool]:
    """(text carrying a lifecycle status header, whether one was ADDED).

    THE ROUND-TRIP OBLIGATION, realized on returned material (Brett's ruling,
    2026-08-19). Every artifact the reverse transition writes into a staging
    topic has to satisfy the same governed-document rules the forward transition
    enforces there — and OpenSpec change artifacts do not carry lifecycle headers
    by convention. Measured at 8426dbc by the forward gate's own reader (a
    `Status:` line outside every fence): 93 of 94 `tasks.md`, 154 of 158 spec
    deltas, 65 of 68 `design.md` and 49 of 94 `proposal.md` carry NONE. The
    counts move with the corpus; the shape does not. Returned unheadered, every
    one of them made the next whole-folder transition of that topic refuse, so
    the demote left the cycle one-way for the topic it was applied to.

    `draft` is the status, for design Decision 2's reason: the returned material
    is a draft proposal continuing as a draft idea in the topic's workspace.

    WHERE IT GOES follows the corpus rather than an invention. A document opening
    with a `---` front-matter block gets the header INSIDE that block, which is
    where `ideation/staging/tier2-council-clearance-pattern/openspec/proposal.md`
    — the one real returned topic a human already fixed by hand — carries it;
    putting it above the block would push the front matter off position 0 and
    stop it being front matter at all. Otherwise it goes under the leading `# `
    title, which is where every other governed document in this corpus carries
    it.

    A document that already has a header is returned UNCHANGED and reports False:
    the flip arm owns those, and this must never become a second writer of the
    same line.
    """
    rows = round_trip.split_keepends(text)
    if _status_row(rows) is not None:
        return text, False
    eol = round_trip.document_eol(rows)
    if not rows:
        return f"Status: {new_status}{eol}", True

    if rows[0][0].strip() == "---":
        for i in range(1, min(len(rows), HEADER_SCAN_LINES)):
            if rows[i][0].strip() == "---":
                rows.insert(i, (f"Status: {new_status}", eol))
                return round_trip.join_rows(rows), True

    at = 0
    if rows[0][0].startswith("# "):
        at = 2 if len(rows) > 1 and not rows[1][0].strip() else 1
    block = [(f"Status: {new_status}", eol), ("", eol)]
    if at > 0 and rows[at - 1][0].strip():
        block.insert(0, ("", eol))
    if at >= len(rows):
        # Appending past the end: the last row may carry no ending at all (a file
        # with no trailing newline), and the new header must not be glued onto it.
        if rows and not rows[-1][1]:
            rows[-1] = (rows[-1][0], eol)
        block = block[:-1]
    rows[at:at] = block
    return round_trip.join_rows(rows), True


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
    cleanup: Mapping[str, Any] | None = None,
    model_declaration: str | None = None,
    model_approval: Mapping[str, Any] | None = None,
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
    if model_declaration and str(model_declaration).strip():
        target["model_declaration"] = str(model_declaration).strip()
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
    if cleanup is not None:
        record["cleanup"] = dict(cleanup)
    if model_approval is not None:
        # Placed where the schema places it — after `cleanup`, before the
        # narrative fields — so the rendered record reads in the schema's own
        # property order. Copied rather than referenced: a caller that kept a
        # handle on the mapping must not be able to mutate a record after it was
        # built and validated.
        record["model_approval"] = dict(model_approval)
    if reason:
        record["reason"] = reason
    if citation:
        record["citation"] = citation
    if notes:
        record["notes"] = notes
    return record


def _validate_contract_document(
    document: Mapping[str, Any], *, schema_filename: str, label: str,
) -> None:
    """Validate one document against a repository-pinned released schema."""
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:  # pragma: no cover - release dependency guard
        raise GateRefused(
            f"jsonschema is required to validate {label}") from exc
    schema_path = (Path(__file__).resolve().parents[2] / "contracts" / "schemas"
                   / schema_filename)
    try:
        schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise GateRefused(
            f"the {label} schema could not be loaded from {schema_path}: "
            f"{exc}") from exc
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(
            dict(document)),
        key=lambda error: tuple(str(part) for part in error.absolute_path))
    if errors:
        detail = "; ".join(
            f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: "
            f"{error.message}" for error in errors[:5])
        raise GateRefused(
            f"the {label} failed schema validation: {detail}")


def validate_gate_action_record(record: Mapping[str, Any]) -> None:
    """Validate one record against the repository-pinned released schema."""
    _validate_contract_document(
        record, schema_filename="gate-action-record.schema.yaml",
        label="gate-action record")
    if record.get("action") != ACTION_CLEANUP_ABANDONED_BRANCH:
        return
    target = record.get("target")
    cleanup = record.get("cleanup")
    release = cleanup.get("retention_release") if isinstance(
        cleanup, Mapping) else None
    if not isinstance(target, Mapping) or not isinstance(release, Mapping):
        raise GateRefused("cleanup record is missing target/release evidence")
    scope_fields = {
        "staged-topic": "topic_id", "cluster": "cluster_id",
        "possible": "possible_id",
    }
    scope_kind = str(release.get("scope_kind") or "")
    scope_field = scope_fields.get(scope_kind)
    populated = [
        field for field in scope_fields.values()
        if str(target.get(field) or "").strip()
    ]
    if scope_field is None or populated != [scope_field] or str(
            target.get(scope_field) or "") != str(release.get("scope_id") or ""):
        raise GateRefused(
            "cleanup target scope must exactly match retention-release "
            "scope_kind/scope_id")
    kind = str(release.get("kind") or "")
    references = release.get("references")
    if kind != "explicit-human-release":
        if not str(release.get("change_id") or "").strip():
            raise GateRefused(
                "machine cleanup evidence requires the preserving change_id")
        if not isinstance(references, list) or not references:
            raise GateRefused(
                "machine cleanup evidence requires at least one reference")
        if not str(release.get("recorded_at") or "").strip():
            raise GateRefused(
                "machine cleanup evidence requires its durable recording time")
    else:
        reason = str(record.get("reason") or "").strip()
        if reason != str(release.get("reason") or "").strip():
            raise GateRefused(
                "explicit cleanup reason must exactly match the release evidence")


def validate_demotion_execution_receipt(receipt: Mapping[str, Any]) -> None:
    _validate_contract_document(
        receipt, schema_filename="demotion-execution-receipt.schema.yaml",
        label="demotion execution receipt")
    destination = receipt.get("destination")
    if not isinstance(destination, Mapping) or str(destination.get("path") or "") \
            != f"ideation/staging/{destination.get('id')}":
        raise GateRefused(
            "demotion receipt destination.path must exactly match destination.id")
    path_values = [str(receipt.get("transition_manifest") or "")]
    path_values.extend(str(path) for path in receipt.get("returned_artifacts") or [])
    for move in receipt.get("returned_moves") or []:
        if isinstance(move, Mapping):
            path_values.extend((str(move.get("from") or ""),
                                str(move.get("to") or "")))
    for reference in path_values:
        parts = Path(reference).parts
        if (not reference or "\\" in reference
                or Path(reference).is_absolute() or ".." in parts
                or "." in parts):
            raise GateRefused(
                f"demotion receipt path {reference!r} must be a contained "
                "repository-relative reference")


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


def _gate_action_target_id(record: Mapping[str, Any]) -> str:
    target = record["target"]
    if (record.get("action") == ACTION_CLEANUP_ABANDONED_BRANCH
            and target.get("ref")):
        return ref_target_id(target["ref"])
    target_id = (target.get("change_id") or target.get("possible_id")
                 or target.get("topic_id") or target.get("cluster_id")
                 or target.get("project_id")
                 # add-doxchat-model-intake §3: an `approve-model` record has
                 # none of the five above and files under the declaration it
                 # approved. It is placed IN this chain rather than after
                 # `document`/`ref` because an approval record names neither, so
                 # no pre-existing verb's filename can move by its presence.
                 or target.get("model_declaration"))
    if not target_id and target.get("document"):
        target_id = document_target_id(target["document"])
    if not target_id and target.get("ref"):
        target_id = ref_target_id(target["ref"])
    if not target_id:
        raise GateRefused(
            "a gate-action record must name what it acted on "
            "(change_id, possible_id, topic_id, cluster_id, project_id, "
            "model_declaration, document, or a session ref)")
    return str(target_id)


def write_gate_action_record(
    gate: HumanGate, records_dir: str, record: dict, *, exclusive: bool = False,
) -> Path:
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
    target_id = _gate_action_target_id(record)
    rel = gate_action_record_relpath(records_dir, record["action"], target_id, record["at"])
    rendered = _render_yaml(record, _RECORD_BANNER)
    try:
        return (gate.create_gate_artifact(rel, rendered) if exclusive
                else gate.write_gate_artifact(rel, rendered))
    except FileExistsError as exc:
        raise GateRefused(
            f"gate-action record {rel} already exists; a concurrent or repeated "
            "attempt may not overwrite it") from exc


def replace_gate_action_record(
    gate: HumanGate, records_dir: str, record: dict,
) -> Path:
    """Atomically replace the exact action record created by this transaction."""
    target_id = _gate_action_target_id(record)
    rel = gate_action_record_relpath(
        records_dir, record["action"], target_id, record["at"])
    return gate.replace_gate_artifact(
        rel, _render_yaml(record, _RECORD_BANNER))


# ==========================================================================
# DEMOTE — the mechanized reverse transition (T033)
# ==========================================================================

@dataclass(frozen=True)
class FileMove:
    """One reverse-transition file move: a change artifact returning to the
    staging topic. `status_flip` (when set) rewrites the moved copy's `Status:`
    header — proposal documents CONTINUE AS DRAFT IDEAS in the topic's openspec/
    workspace (the draft-proposal convention).

    `outline` marks the ONE move whose destination is the topic's declared primary
    fragment (align-demote-to-round-trip-rule, design Decision 1). It is decided in
    the PURE PLAN and published, so `demote-<stamp>.plan.yaml` states which file
    will be treated as the topic's outline BEFORE anything is written — a human
    reviewing the plan should not have to infer that from a basename. An outline
    move carries `status_flip = "staged"`, not `"draft"`: the same selection rule
    still calls that file the staged topic's outline."""
    from_path: str          # repo-relative source (inside the change folder)
    to_path: str            # repo-relative destination (inside the staging topic)
    role: str               # proposal-draft | design-draft | spec-delta | tasks | supporting-doc | openspec-config | other
    status_flip: str | None
    outline: bool = False


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
    # The change's status the moment it was demoted, carried from the snapshot the
    # plan was derived from because `execute_demotion_plan` never sees one. It fills
    # the `Status at demote` provenance slot.
    status_at_demote: str = ""
    # The change's task progress at the same moment, carried the same way and for
    # the same reason (the executor never sees a snapshot). The status alone is a
    # CONSTANT — `plan_demotion` refuses any change that is not active, so a
    # status-only slot cannot tell one demote from another — and the progress is
    # the informative fact the snapshot already holds beside it. `None` where the
    # change records no tasks, which the slot renders as the status alone rather
    # than as a fabricated count.
    task_progress: dict[str, int] | None = None


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
        # Preserve nested provenance paths. Flattening every supporting document
        # to its basename makes `supporting-docs/README.md` collide with
        # `supporting-docs/source-snapshots/README.md` and silently overwrites
        # one during execution.
        supporting_rel = rel_within_change.split("supporting-docs/", 1)[1]
        return "supporting-doc", supporting_rel, flip
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
    # THE PRECEDENCE ORDER, and its first rung is here because this is where a
    # human's argument arrives: an explicitly supplied topic ALWAYS wins, because
    # naming the destination is the most direct statement of intent available. The
    # remaining two rungs — the change's own recorded staged origin, then a
    # possibles pick edge — are resolved into `origin_staging_id` by the generator,
    # which is the only side that reads the tree.
    topic = staging_topic or change.get("origin_staging_id")
    if not topic:
        raise GateRefused(
            f"change {change_id!r} has no recorded origin staging topic; pass "
            "staging_topic (`--staging-topic` on the CLI) explicitly to target "
            "the reverse transition")

    folder = change.get("folder") or f"openspec/changes/{change_id}"
    topic_path = f"ideation/staging/{topic}"
    openspec_ws = f"{topic_path}/openspec"

    # THE OUTLINE DESTINATION, decided PATH-ONLY and here in the pure plan
    # (align-demote-to-round-trip-rule, design Decision 1). `primaryFragmentPath`
    # has two arms — the exact `<topic>.md`, ELSE the shallowest markdown file — and
    # only the first is decidable from a path without reading the tree. That arm is
    # what `proposal-support.py transition` produces and what both real
    # staged-origin manifests carry, so it is the covered case; the
    # shallowest-markdown arm is a KNOWN BOUND, deliberately not half-handled, and
    # needs its own ruling rather than a guess here.
    outline_dest = f"{topic_path}/{topic}.md"

    moves: list[FileMove] = []
    for path in change.get("files") or []:
        if not path.startswith(folder + "/"):
            continue
        rel_within = path[len(folder) + 1:]
        role, dest_rel, flip = classify_change_file(rel_within)
        to_path = f"{topic_path}/{dest_rel}"
        is_outline = to_path == outline_dest
        moves.append(FileMove(
            from_path=path, to_path=to_path, role=role,
            # A staged topic's outline is STAGED. The `draft` flip stays exactly
            # as it was for the proposal documents bound for `openspec/`.
            status_flip=STAGED_STATUS if is_outline else flip,
            outline=is_outline))

    withdrawn = tuple(sorted(
        p["id"] for p in snapshot.get("possibles") or []
        if isinstance(p, dict) and (p.get("pick") or {}).get("change_id") == change_id and p.get("id")
    ))

    # Snapshot-derived, like the status beside it. The generator emits the key
    # only when the change records tasks, so an absent key is "no tasks", not
    # "lookup failed" — a distinction the slot's rendering depends on.
    raw_progress = change.get("task_progress")
    progress = dict(raw_progress) if isinstance(raw_progress, dict) else None

    return DemotionPlan(
        change_id=change_id, staging_topic=topic, change_folder=folder,
        topic_path=topic_path, openspec_workspace=openspec_ws, reason=reason.strip(),
        moves=tuple(moves), withdrawn_picks=withdrawn,
        status_at_demote=str(change.get("status") or ""),
        task_progress=progress)


def state_at_demote(status: str, progress: dict[str, int] | None) -> str:
    """PURE: the `Status at demote` provenance slot's value — the change's state
    at the moment it was demoted, as the prose a human reads in the fragment.

    `active — 9 of 22 tasks done`. PROSE, not a code: the slot sits in a markdown
    document beside four other slots that are all plain prose, and a reader of
    that document is the audience.

    NO PROGRESS RENDERS THE STATUS ALONE, never `active — unavailable`. The
    ratified unavailable rule is about a value that could not be RESOLVED; a
    change that records no tasks has no progress to resolve, so writing
    `unavailable` there would report a lookup failure that did not happen. An
    empty status still yields "", which the caller turns into the real
    UNAVAILABLE marker — that one IS a resolution failure."""
    base = str(status or "").strip()
    if not base or not isinstance(progress, dict):
        return base
    completed, total = progress.get("completed"), progress.get("total")
    if not isinstance(completed, int) or not isinstance(total, int):
        return base
    if isinstance(completed, bool) or isinstance(total, bool) or total <= 0:
        return base
    if completed < 0 or completed > total:
        # Unreachable through the generator, which counts `completed` out of the
        # same regex sweep that produces `total`. Guarded anyway because the slot
        # is prose a human reads as fact, and `9 of 4 tasks done` is a fabricated
        # one — the status alone is the true statement about a record that does
        # not add up.
        return base
    return f"{base} — {completed} of {total} tasks done"


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
        "status_at_demote": plan.status_at_demote,
        "files": [
            {"from": m.from_path, "to": m.to_path, "role": m.role,
             "status_flip": m.status_flip, "outline": m.outline}
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
        if m.to_path.endswith(".md") and not m.outline:
            # DECLARED before execution, and decidable PATH-ONLY like everything
            # else in this plan: a returned governed markdown document that
            # arrives with no lifecycle status header is given `Status: draft`,
            # because the forward transition refuses governed markdown without
            # one. Whether any given file needs it is a fact about the tree, not
            # the path — so the plan states the RULE and the execution record
            # names the files it actually applied to.
            step["ensure_status"] = DRAFT_STATUS
        if m.outline:
            # DECLARED before execution: this destination is the topic's outline,
            # so it is refreshed rather than overwritten, and a pre-existing
            # differing fragment is never byte-replaced.
            step["outline_restore"] = True
            step["refresh"] = "provenance-slots + xspec:candidate sections"
            step["on_existing_differing_fragment"] = "refresh in place; preserve snapshot"
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
    # align-demote-to-round-trip-rule: what happened to the topic's OUTLINE.
    # `outline_path` is the fragment that now carries the round-trip provenance;
    # `snapshot_disposition` is "applied" when the change folder's snapshot became
    # that fragment (the destination was absent or identical) or "preserved" when a
    # live differing fragment was refreshed in place and the snapshot was kept
    # beside it instead; `preserved_snapshot_path` names that kept copy. The
    # distinction is recorded rather than inferred because "we did not overwrite
    # your work" is exactly the sentence a human needs to be able to check.
    outline_path: Path | None = None
    snapshot_disposition: str | None = None
    preserved_snapshot_path: Path | None = None
    outline_refreshed: bool = False
    # Why the refresh did NOT happen, when it did not. A refusal a caller cannot
    # read is a refusal that reads as success.
    outline_refusal: str | None = None
    # Returned markdown that arrived carrying no lifecycle status header and was
    # given `Status: draft` so the topic stays transitionable (Brett's ruling,
    # 2026-08-19). Recorded rather than silent: this verb edited bytes of a
    # human-visible document, and "which of my files did you touch, and how" is
    # exactly the question a gate record has to be able to answer.
    status_headers_added: list[str] = field(default_factory=list)


def _read_raised_date(root: Path, plan: DemotionPlan) -> str:
    """The date the topic transitioned INTO the change, from the change's own
    supporting-docs manifest.

    Read BEFORE the moves run, because that manifest is itself a returning
    supporting-doc and the change folder is removed at the end of execution.
    An absent or unreadable manifest yields the UNAVAILABLE marker: the
    requirement forbids fabricating the value, so it is never guessed from the
    change folder's archive-date prefix or from a file mtime.
    """
    manifest = root / plan.change_folder / "supporting-docs" / "manifest.yaml"
    if not manifest.is_file():
        return round_trip.UNAVAILABLE
    try:
        loaded = yaml.safe_load(manifest.read_bytes().decode("utf-8"))
    except Exception:
        return round_trip.UNAVAILABLE
    if not isinstance(loaded, dict):
        return round_trip.UNAVAILABLE
    raised = loaded.get("transitioned_at")
    return str(raised) if raised else round_trip.UNAVAILABLE


def _restore_outline(
    plan: DemotionPlan, root: Path, at: str, raised: str,
    result: DemotionExecution,
) -> None:
    """The outline move, which is a REFRESH and not a copy.

    Three cases, and the third is the reason this change exists:

    * destination ABSENT — restore the snapshot, then refresh it. The ordinary
      case, because `transition` empties the topic folder on the way out.
    * destination byte-IDENTICAL to the snapshot — the same, since there is
      nothing to lose; routing it through the third case would preserve a copy of
      a file identical to the one beside it.
    * destination PRESENT AND DIFFERING — the live fragment is the AUTHORITY. Its
      bytes are NOT replaced. The refresh applies into it, bounded to the
      provenance slots and the marked sections, and the snapshot is preserved
      beside it so that "never byte-replace" does not quietly become "silently
      discard the other copy".
    """
    outline = next((m for m in plan.moves if m.outline), None)
    if outline is None:
        return
    src = root / outline.from_path
    dst = root / outline.to_path
    if not src.is_file():
        return

    provenance = {
        "Change ID": plan.change_id,
        "Raised": raised,
        "Status at demote": (state_at_demote(plan.status_at_demote,
                                             plan.task_progress)
                             or round_trip.UNAVAILABLE),
        "Demoted": at[:10],
        "Demote reason": plan.reason,
    }
    # The RETURNED proposal, read from its destination: the durable artifact a
    # human can still open afterwards. A change with no proposal.md leaves the
    # marked sections untouched and still gets its slots filled.
    # `read_bytes().decode`, never `read_text`: Python 3.12's `Path.read_text` has
    # no `newline=` parameter and its universal-newline mode TRANSLATES CRLF to LF
    # on the way in. Reading the fragment that way collapsed a Windows-authored
    # outline to LF and the refresh then wrote the translation back — the same
    # corpus-integrity defect this verb's move arm was already fixed for once.
    returned_proposal = root / plan.openspec_workspace / "proposal.md"
    proposal_text = (
        returned_proposal.read_bytes().decode("utf-8")
        if returned_proposal.is_file() else None)

    snapshot_bytes = src.read_bytes()
    dst.parent.mkdir(parents=True, exist_ok=True)

    if dst.is_file() and dst.read_bytes() != snapshot_bytes:
        # CASE 3. The snapshot never reaches the destination. It is kept as a
        # VISIBLE ordinary topic file — not a dotfile and not `.orig` — because a
        # hidden artifact in a governed folder is how material goes missing, and
        # the corpus readers (doc-health, the wheel) should see it.
        kept = dst.parent / f"{plan.staging_topic}.snapshot-{plan.change_id}.md"
        kept_text, kept_added = _add_status_header(
            _flip_status(snapshot_bytes.decode("utf-8"), DRAFT_STATUS), DRAFT_STATUS)
        kept.write_bytes(kept_text.encode("utf-8"))
        if kept_added:
            result.status_headers_added.append(
                kept.relative_to(root).as_posix())
        result.preserved_snapshot_path = kept
        result.snapshot_disposition = "preserved"
        base = dst.read_bytes().decode("utf-8")   # never read_text (see above)
    else:
        # CASES 1 and 2. The snapshot becomes the fragment, with its Status set
        # positively to `staged` by the plan's own flip.
        base = _flip_status(snapshot_bytes.decode("utf-8"), outline.status_flip
                            or STAGED_STATUS)
        result.snapshot_disposition = "applied"

    # THE HEADER OBLIGATION REACHES THE OUTLINE TOO, and specifically the
    # REFRESH-IN-PLACE arm. A previous pass of this change declared the outline
    # out of scope on the grounds that its source always arrives carrying a
    # header — true of the snapshot the restore arm applies, and FALSE of the
    # live fragment case 3 reads, which is a document the human owns and which
    # never passed the forward gate to acquire one. Driven: a header-less working
    # outline demoted cleanly (`outline_refusal: None`) and left the topic
    # one-way, the next whole-folder transition refusing on the fragment itself.
    #
    # THE VALUE IS `staged`, NOT the `draft` used for returned change artifacts,
    # and it is taken from the same expression the restore arm uses so the two
    # cannot drift. The ratified rule is explicit: a returning file whose
    # destination is the topic's declared primary fragment SHALL keep
    # `Status: staged` and MUST NOT be flipped to draft, because the selection
    # rule still calls that file the staged topic's outline.
    #
    # `_add_status_header` DEFERS to an existing header, so the live fragment's
    # own status — whatever the human set it to — is still never rewritten here.
    # Only its absence is filled.
    base, outline_added = _add_status_header(
        base, outline.status_flip or STAGED_STATUS)
    if outline_added:
        result.status_headers_added.append(outline.to_path)

    # THE UNCLOSED-FENCE REFUSAL. Inside an open fence a written section is
    # invisible to the scanner that would find it next time, so it would be written
    # again on every pass — the ratified idempotence clause carries no qualifier.
    # The restore still happens (the file must exist); only the refresh is withheld,
    # and it says so.
    if round_trip.ends_inside_fence(base):
        result.outline_refusal = (
            "the fragment ends inside an unclosed code fence, so the round-trip "
            "provenance was NOT written — close the fence and re-run the demote's "
            "refresh")
        refreshed = base
    else:
        refreshed = round_trip.refresh_fragment(
            base, proposal_text=proposal_text, provenance=provenance)

    # Written only when the bytes actually move, so a refused refresh leaves the
    # destination's mtime alone as well as its content.
    new_bytes = refreshed.encode("utf-8")
    if not dst.is_file() or dst.read_bytes() != new_bytes:
        dst.write_bytes(new_bytes)
    src.unlink()
    result.moved.append((outline.from_path, outline.to_path))
    result.outline_path = dst
    result.outline_refreshed = result.outline_refusal is None


def _contained_tree_path(root: Path, reference: str, *, label: str) -> Path:
    candidate = Path(reference)
    if not reference or "\\" in reference or candidate.is_absolute():
        raise GateRefused(f"{label} must be a repository-relative path")
    resolved = (root / candidate).resolve()
    if not resolved.is_relative_to(root):
        raise GateRefused(f"{label} escapes the repository root: {reference!r}")
    return resolved


def execute_demotion_plan(plan: DemotionPlan, tree_root: Path | str, *, at: str | None = None) -> DemotionExecution:
    """APPLY the reverse transition to a real tree — the legitimate way material
    (re-)enters `ideation/staging/` is exactly this human gate action. v1
    exercises it against an in-test FIXTURE change tree; `cli.py gate demote
    --execute` runs it against a real checkout a human drives. Moves each file
    (flipping Status where the plan says), records the return in the topic
    README, writes the openspec-workspace INDEX, and removes the emptied change
    folder.

    THE OUTLINE MOVE IS DIFFERENT (align-demote-to-round-trip-rule). Every other
    move is a byte copy; the topic's primary fragment is REFRESHED, and a live
    fragment that differs from the change folder's snapshot of it is never
    byte-replaced — the snapshot is a fallback SOURCE, never the authority."""
    root = Path(tree_root).resolve()
    at = at or _utcnow()
    result = DemotionExecution()

    if not plan.moves:
        raise GateRefused(
            f"demotion plan for {plan.change_id!r} contains no proposal artifacts")
    planned_destinations: set[Path] = set()
    for move in plan.moves:
        source = _contained_tree_path(
            root, move.from_path, label="demotion source")
        destination = _contained_tree_path(
            root, move.to_path, label="demotion destination")
        if not source.is_file():
            raise GateRefused(
                f"demotion cannot start: planned source {move.from_path!r} "
                "is missing; no files were moved")
        if destination in planned_destinations:
            raise GateRefused(
                f"demotion plan targets destination {move.to_path!r} more than once")
        planned_destinations.add(destination)
    _contained_tree_path(root, plan.change_folder, label="change folder")

    # BEFORE the moves: the raised date lives in the change's supporting-docs
    # manifest, which is itself a returning supporting-doc, and the change folder
    # is removed at the end of this function.
    raised = _read_raised_date(root, plan)

    for m in plan.moves:
        src = _contained_tree_path(root, m.from_path, label="demotion source")
        dst = _contained_tree_path(root, m.to_path, label="demotion destination")
        if m.outline:
            # Deferred to its own pass below, after every ordinary move has landed:
            # the refresh reads the RETURNED `proposal.md` from its destination, so
            # it must run once that file is there.
            continue
        # Wave re-review P3 (the F10 corpus-integrity class through another
        # verb): this MOVE used to `read_text(errors="replace")` ->
        # `write_text`, which universal-newline-translated CRLF to LF on
        # Linux — silently rewriting a Windows-authored document and
        # invalidating any open doxBench buffer's base identity — and mangled
        # undecodable bytes to U+FFFD on the way. So NOTHING here goes through
        # universal-newline translation: a governed markdown document is decoded
        # STRICTLY, rewritten by row (each line keeping the ending it had), and
        # re-encoded only when its bytes actually changed. Strict is the same
        # refuse-to-fabricate asymmetry as the doxBench base revalidation (P3-5):
        # a non-UTF-8 markdown document fails the demotion loudly rather than
        # being silently re-encoded under a gate record naming the human.
        # Non-markdown never decodes at all — it is a byte copy.
        data = src.read_bytes()
        if m.to_path.endswith(".md"):
            decoded = data.decode("utf-8")
            updated = _flip_status(decoded, m.status_flip) if m.status_flip else decoded
            # THE ROUND-TRIP OBLIGATION on returned material (Brett's ruling,
            # 2026-08-19): a governed markdown artifact this verb writes into a
            # staging topic carries a lifecycle status header, because the
            # forward transition refuses governed markdown without one and an
            # unheadered returned artifact makes the cycle one-way for that
            # topic. `_flip_status` cannot do this — it is a no-op on a document
            # with no header, which is 93 of 94 `tasks.md` in this corpus.
            updated, added = _add_status_header(updated, m.status_flip or DRAFT_STATUS)
            if added:
                result.status_headers_added.append(m.to_path)
            if updated != decoded:
                data = updated.encode("utf-8")
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        src.unlink()
        result.moved.append((m.from_path, m.to_path))

    _restore_outline(plan, root, at, raised, result)

    # README record (append; create if absent).
    readme = root / plan.topic_path / "README.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    returned = [m.to_path for m in plan.moves]
    # THE OUTLINE'S OWN SENTENCE (align-demote-to-round-trip-rule). A human whose
    # live fragment was refreshed rather than overwritten has to be able to read
    # that here, and to find the snapshot that was kept instead of applied.
    outline_note = ""
    if result.outline_refusal and result.outline_path is not None:
        outline_note = (
            f"\nOutline: {result.outline_path.relative_to(root).as_posix()} — "
            f"{result.outline_refusal}.\n")
    elif result.outline_refreshed and result.outline_path is not None:
        rel = result.outline_path.relative_to(root).as_posix()
        if result.snapshot_disposition == "preserved" and result.preserved_snapshot_path:
            kept = result.preserved_snapshot_path.relative_to(root).as_posix()
            outline_note = (
                f"\nOutline: {rel} already existed and differed, so it was "
                f"REFRESHED IN PLACE (round-trip provenance slots and "
                f"`xspec:candidate` sections only). Its other bytes are "
                f"untouched. The change folder's snapshot was PRESERVED as "
                f"{kept} rather than applied over your work.\n")
        else:
            outline_note = (
                f"\nOutline: {rel} was restored from the change folder's snapshot "
                f"and refreshed with this demote's round-trip provenance.\n")
    # WHICH RETURNED FILES THIS VERB EDITED, named. The header additions are the
    # only place a demote changes bytes inside a file it is otherwise just moving,
    # so they are stated rather than left for a human to notice in a diff.
    header_note = ""
    if result.status_headers_added:
        header_note = (
            "\nStatus headers added (these arrived carrying none, and the "
            "forward transition refuses governed Markdown without one):\n"
            + "\n".join(f"- {p}" for p in result.status_headers_added) + "\n")
    note = (f"\n## Returned drafts (demoted {plan.change_id}, {at[:10]})\n\n"
            f"Reason: {plan.reason}\n"
            + outline_note + header_note + "\n"
            + "\n".join(f"- {r}" for r in returned) + "\n")
    if readme.is_file():
        # Translation-free on BOTH legs (wave re-review P3): `read_bytes().
        # decode` instead of `read_text` because Python 3.12's `Path.read_text`
        # has no `newline=` parameter and its universal-newline mode collapses
        # an existing CRLF README to LF; `newline=""` on the write so the
        # combined text lands exactly as composed. The NOTE itself uses "\n" —
        # appending it to a CRLF README yields mixed endings deliberately: the
        # pre-existing bytes surviving untouched is the guarantee, not the
        # note matching the document's style.
        readme.write_text(readme.read_bytes().decode("utf-8") + note,
                          encoding="utf-8", newline="")
    else:
        readme.write_text(f"# {plan.staging_topic}\n\nStatus: staged\n" + note,
                          encoding="utf-8", newline="")
    result.readme_path = readme

    # openspec/ workspace INDEX of the returned draft proposals.
    index = root / plan.openspec_workspace / "INDEX.md"
    index.parent.mkdir(parents=True, exist_ok=True)
    ws_files = [m.to_path for m in plan.moves if m.to_path.startswith(plan.openspec_workspace + "/")]
    # THE STATUS HEADER IS A ROUND-TRIP OBLIGATION, not a formatting preference.
    # This INDEX is a governed markdown document the reverse transition writes
    # into a governed folder, and the FORWARD transition refuses any governed
    # markdown without a `Status:` header — so an unheadered INDEX made the cycle
    # one-way for the topic it was applied to (`SupportError: governed Markdown
    # lacks Status header` on the next whole-folder transition of that topic).
    # `draft` is the status: the INDEX describes the returned DRAFT proposals and
    # shares their state, and the next demote regenerates it, so it is not the
    # immutable evidence `record` would claim (design Decision 2).
    index.write_text(
        f"# openspec/ draft workspace — {plan.staging_topic}\n\n"
        f"Status: {DRAFT_STATUS}\n\n"
        f"Draft proposals returned from demoted change {plan.change_id} "
        f"({at[:10]}). These continue as draft ideas per the draft-proposal "
        f"convention:\n\n" + ("\n".join(f"- {p}" for p in ws_files) or "- (none)") + "\n",
        encoding="utf-8")
    result.index_path = index

    # Remove the now-empty change folder (best effort).
    change_dir = _contained_tree_path(
        root, plan.change_folder, label="change folder")
    if change_dir.is_dir():
        shutil.rmtree(change_dir)
        result.removed_change_folder = not change_dir.exists()

    expected_moves = sorted((move.from_path, move.to_path) for move in plan.moves)
    if sorted(result.moved) != expected_moves:
        raise GateRefused(
            f"demotion execution was incomplete: planned {len(expected_moves)} "
            f"moves but completed {len(result.moved)}; no executed receipt will "
            "be written")
    missing_destinations = [
        destination for _source, destination in expected_moves
        if not _contained_tree_path(
            root, destination, label="returned artifact").is_file()
    ]
    if missing_destinations or not result.removed_change_folder:
        problems = []
        if missing_destinations:
            problems.append(f"missing destinations {missing_destinations}")
        if not result.removed_change_folder:
            problems.append("the source change folder was not removed")
        raise GateRefused(
            "demotion execution was incomplete: " + "; ".join(problems)
            + "; no executed receipt will be written")

    return result


def demotion_execution_receipt(
    result: DemoteResult, execution: DemotionExecution, *, actor: str, at: str,
    root: Path,
) -> dict[str, Any]:
    """The durable statement written only after a demotion execution returns."""
    expected_moves = sorted(
        (move.from_path, move.to_path) for move in result.plan.moves)
    if not expected_moves or sorted(execution.moved) != expected_moves:
        raise GateRefused(
            "an executed demotion receipt requires every planned move exactly once")
    if not execution.removed_change_folder or _contained_tree_path(
            root, result.plan.change_folder, label="change folder").exists():
        raise GateRefused(
            "an executed demotion receipt requires the source change folder to "
            "be removed")
    returned: list[str] = [to_path for _from_path, to_path in execution.moved]
    for path in (execution.readme_path, execution.index_path,
                 execution.preserved_snapshot_path):
        if path is not None:
            try:
                returned.append(path.relative_to(root).as_posix())
            except ValueError as exc:
                raise GateRefused(
                    f"returned artifact {path} escapes the repository root") from exc
    for reference in returned:
        if not _contained_tree_path(
                root, reference, label="returned artifact").is_file():
            raise GateRefused(
                f"returned artifact {reference!r} does not exist at receipt time")
    try:
        manifest_ref = result.manifest_path.resolve().relative_to(
            root.resolve()).as_posix()
    except ValueError as exc:
        raise GateRefused(
            "the transition manifest escapes the repository root") from exc
    if not (root / manifest_ref).is_file():
        raise GateRefused("the transition manifest is missing at receipt time")
    return {
        "schema_version": 1,
        "kind": DEMOTION_EXECUTION_KIND,
        "actor": actor,
        "change_id": result.plan.change_id,
        "status": "executed",
        "destination": {
            "kind": "staged",
            "id": result.plan.staging_topic,
            "path": result.plan.topic_path,
        },
        "executed_at": at,
        "transition_manifest": manifest_ref,
        "returned_moves": [
            {"from": source, "to": destination}
            for source, destination in expected_moves
        ],
        "returned_artifacts": sorted(set(returned)),
        "removed_change_folder": execution.removed_change_folder,
    }


def write_demotion_execution_receipt(
    gate: Any, result: DemoteResult, execution: DemotionExecution, *,
    at: str | None = None, records_dir: str = DEFAULT_RECORDS_DIR,
) -> Path:
    """Persist execution proof after, and only after, successful execution."""
    human = require_human_gate(gate)
    at = at or _utcnow()
    root = human.output.root
    receipt = demotion_execution_receipt(
        result, execution, actor=human.human_actor, at=at, root=root)
    validate_demotion_execution_receipt(receipt)
    rel = (f"{_prefix(records_dir)}{result.plan.change_id}/demote-"
           f"{_stamp(at)}.execution-receipt.yaml")
    try:
        return human.create_gate_artifact(
            rel, _render_yaml(
                receipt,
                "# demotion execution receipt — written only after the returned "
                "artifacts land.\n"))
    except FileExistsError as exc:
        raise GateRefused(
            f"demotion execution receipt {rel} already exists; refusing to "
            "overwrite another execution") from exc


# ==========================================================================
# RATIFY — approve; write the ratification record + register update (T034)
# ==========================================================================

def build_ratification_record(change_id: str, ratifier: str, *, date: str) -> dict:
    """The ratification record artifact (ratifier + date) — the same content a
    manual ratification records on the proposal (`Ratified by:` + the ratify
    date the generator reads back into `changes[].ratification`).

    PLUS its `binding` block (`record_binding`, the records-tree-trust gap). The
    record used to be believed because of WHERE IT SAT; the binding is the first
    half of a reason to believe it — a `sha256` over its own content, so the
    ratifier, the date, and the change it names cannot be edited in place
    afterwards. The second half is the git commit anchor, which only exists once
    a human commits the record and is verified at READ time (`kickoff`)."""
    return record_binding.with_binding({
        "kind": ART_RATIFICATION_RECORD,
        "schema_version": 1,
        "change_id": change_id,
        "ratifier": ratifier,
        "date": date,
    })


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
    # The ratify ACTION record carries a binding too, for the same reason its
    # artifact does: `kickoff` reads ratification from EITHER document, so a
    # binding on only one of them leaves the other believable on placement alone
    # (`record_binding`). ADDITIVE — the schema fixes no closed property set and
    # states that consumers MUST ignore unknown properties.
    record = record_binding.with_binding(record)
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


def confined_document_path(human: HumanGate, root: Path, document: str) -> Path:
    """Resolve a gate-console DOCUMENT target strictly INSIDE `root`, or REFUSE.

    THE GAP THIS CLOSES (`ideation/brainstorm/ideation-dashboard.md` item 25:
    "un-confined `edit_apply` document path"). `edit_apply` resolved its target
    as `(root / document).resolve()` and wrote to whatever came back. `document`
    is caller-supplied, `Path.__truediv__` DISCARDS the left operand when the
    right one is absolute, and `resolve()` happily walks `..` and symlinks out of
    the tree — so `--document ../../../../etc/hosts`, `--document /etc/hosts`, or
    a symlink planted inside the corpus all made a human gate action overwrite a
    file outside the repository entirely, with a governed record filed as if a
    change document had been revised.

    Five refusals, and every one of them is a REFUSAL rather than a clamp. A
    silently corrected path is worse than either extreme: the human is told their
    redline applied, the record names the document they asked for, and the bytes
    landed somewhere else.

      1. a blank / unusable target;
      2. an ABSOLUTE path (it names a tree, not a document in this one);
      3. any `..` segment (the traversal spelling, refused even when it would
         land back inside — a gate document is named, never navigated to);
      4. a target that RESOLVES outside the real root — which is the symlink
         case, because `resolve()` follows every link in the path and the
         comparison is against the resolved root;
      5. a target that is not an existing regular file — `edit_apply` REVISES a
         change document; creating one is the authoring path's job, and a
         directory or device node is not a document at all.

    Refusals go through the boundary's public hook, so each one lands on the
    gate's own refusal ledger AND raises — never silent (the module's posture)."""
    raw = str(document)
    if not raw.strip():
        raise human.output.refuse(
            DOCUMENT_ESCAPE, raw,
            "a gate document target must be a repo-relative path; blank was given")
    try:
        candidate = Path(raw)
    except (TypeError, ValueError) as exc:      # embedded NUL and friends
        raise human.output.refuse(
            DOCUMENT_ESCAPE, raw, f"unusable document path ({exc})") from exc
    if candidate.is_absolute() or candidate.drive or candidate.root:
        raise human.output.refuse(
            DOCUMENT_ESCAPE, raw,
            "an ABSOLUTE document path is refused: a gate document is named "
            "relative to the checkout the gate was constructed with, and an "
            "absolute path silently replaces that root entirely")
    if any(part == ".." for part in candidate.parts):
        raise human.output.refuse(
            DOCUMENT_ESCAPE, raw,
            "a `..` segment is refused: a gate document is NAMED, never "
            "navigated to, so traversal is a refusal and not a path to normalize")

    real_root = Path(root).resolve()
    try:
        resolved = (real_root / candidate).resolve()
    except (OSError, RuntimeError, ValueError) as exc:   # symlink loops, bad names
        raise human.output.refuse(
            DOCUMENT_ESCAPE, raw, f"document path could not be resolved ({exc})") from exc
    if resolved != real_root and not resolved.is_relative_to(real_root):
        raise human.output.refuse(
            DOCUMENT_ESCAPE, raw,
            f"document resolves to {resolved}, outside the permitted root "
            f"{real_root} — confinement is a REFUSAL, never a clamp back inside")
    # Belt AND braces: when a caller supplies its own `tree_root`, the target
    # must satisfy BOTH that root and the root the human's gate was constructed
    # over. The authority came from the gate; a second root parameter widens the
    # reach of an action, never the authority behind it.
    gate_root = Path(human.output.root).resolve()
    if real_root != gate_root and not (
            resolved == gate_root or resolved.is_relative_to(gate_root)):
        raise human.output.refuse(
            DOCUMENT_ESCAPE, raw,
            f"document resolves outside the gate's own root {gate_root}; a "
            "declared tree_root may narrow where a gate action reaches, never "
            "widen it")
    if not resolved.is_file():
        raise human.output.refuse(
            DOCUMENT_ESCAPE, raw,
            "no such document under the permitted root (this verb REVISES an "
            "existing change document; it never brings one into existence)")
    return resolved


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
    target = confined_document_path(human, root, document)
    # Translation-free on both legs (wave re-review P3, the F10 class through
    # this verb): `Path.read_text`'s universal-newline mode collapsed CRLF to
    # LF, so on Linux an edit-apply silently rewrote every line ending of a
    # CRLF document — a whole-document mutation the human never approved,
    # and one that invalidates any open doxBench buffer's base identity.
    # `read_bytes().decode` keeps CR/CRLF exactly (3.12's `read_text` has no
    # `newline=`), and `newline=""` pins the write side. `apply_redline` is a
    # pure count/replace over the string — no line splitting — so
    # \r\n-bearing text passes through it untouched.
    before = target.read_bytes().decode("utf-8")
    after = apply_redline(before, redline)
    target.write_text(after, encoding="utf-8", newline="")

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

_VALIDATOR_DETAIL_MAX = 2000


def _bounded_detail(detail: str) -> str:
    """The pinned validator's diagnosis (stdout+stderr, or an unreachable
    reason), whitespace-normalised and bounded to the last
    `_VALIDATOR_DETAIL_MAX` characters — so a refusal that carries it
    verbatim (`GateRefused` message, commit message, gate-action record)
    stays readable no matter how much the validator printed."""
    normalised = " ".join(str(detail or "").split())
    return normalised[-_VALIDATOR_DETAIL_MAX:]


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
            ("updated index rejected by the pinned validator"
             if ok is False else "index validator unreachable")
            + f": {_bounded_detail(detail)}")

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

    def edit_project(self, project_id: str, *, add=None, remove=None,
                     roster=None, register_source=None,
                     outline: str | None = None, workflow: str | None = None,
                     note: str | None = None, at: str | None = None,
                     provenance: Provenance | None = None):
        from . import kickoff as kickoff_mod
        extra = {} if workflow is None else {"workflow": workflow}
        return kickoff_mod.edit_project(
            self.gate, project_id, add=add, remove=remove, roster=roster,
            register_source=register_source, outline=outline, note=note,
            at=at, records_dir=self.records_dir, provenance=provenance, **extra)
