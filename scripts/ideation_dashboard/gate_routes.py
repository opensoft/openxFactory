"""Loopback-only executing gate routes — the LOCAL action center's engine
seam (openxFactory `add-ideation-intent-plane`, change tasks 3.1/3.2; design
D5 local-first).

serve.py dispatches `POST /actions/gate/<verb>` here. Each handler wraps the
EXISTING gate-console engine (`gate_console.py`) — the only executor of gate
verbs — constructing the `HumanGate` with the server's resolved local actor
and the verb's declared write allowlist. Nothing new gains write authority:
this module is transport, the console is the law.

RESPONSE DISCIPLINE (deliberate deviation from the notebook route's
fixed-catalog rule, documented here): gate refusals ARE the product — the
console's precondition messages ("a rejection requires a reason AND a
citation", "already disposed") must reach the human's refusal panel, so
refused responses carry `message: str(exception)`. This is acceptable ONLY
because these routes are loopback-only (the operator talking to their own
working tree) and the client renders every dynamic value via textContent
(the house DOM-safety posture). Unexpected exceptions still return a fixed
message — tracebacks never cross the wire.

Verb coverage this slice: `dispose-possible`, `ratify`, `propose`, the two
keyword-lens verbs `lens-save-recipe` / `lens-add-as-cluster`
(add-lens-gate-verbs), and `create-document`
(add-workbench-bullseye-and-create) — the staging workbench's ONE write, which
brings a NEW ideation document into existence through the tested authoring
scaffold and is create-only (an existing target refuses as SOURCE_EDIT, 409,
and is never overwritten; this verb carries NO edit or delete authority).
The lens verbs are thin glue: the route re-evaluates the
posted recipe server-side (via `lens.py`'s PURE recipe evaluation against the
served snapshot — never trusting a browser-assembled member list), then drives
the ALREADY-TESTED engines (`workbench.py` manifest save, `human_seen.py`
pending_review submission) with NO engine change; every refusal the engines
define surfaces verbatim and persists nothing. demote / edit-apply / kickoff
remain descriptor-only in the gate bar (multi-step plan/redline flows) and join
in a later slice.

BRANCH SESSIONS (007-workbench-branch-sessions, T023/T023a/T025): `create-document`
became session-aware without becoming a second verb. When the body carries the
tile's scope (`scope_kind` + `scope_id`, which did not exist anywhere in the
transport before this feature) AND the caller declared a session registry, the
route resolves the tile's branch session, roots the `HumanGate` at the session
WORKTREE, and commits the document together with its gate-action record as that
action's ONE commit (FR-006). With no scope, or no declared registry, the path is
byte-identical to the pre-session one and touches git not at all (FR-018).

`edit-document` (T042) is the first verb that is session-ONLY: it rewrites an
EXISTING document in the worktree through the boundary's narrow, construction-time
rewrite allowance, rides the same one-commit path, and requires NO redline
artifact — `edit-apply`, the MAIN-RESIDENT redline path, is untouched (FR-017).
With no live session it refuses and names `edit-apply`, because that is the verb
the human was reaching for; it never opens a session to satisfy itself.

The resolution is EXPLICIT, and that is the point: `serve.py` hands this module the
SERVED checkout root (research R1's gap), so the route cannot infer the session
from "the active entry" — the active entry is whatever the human is looking at.
`resolve_session` derives it from the tile instead, and refuses rather than guesses
on a cross-tile collision (G12), a live proposal (FR-024), a surviving abandoned
branch (FR-025), stale residue (FR-008), or an externally-dispatching verb (FR-007).
"""

from __future__ import annotations

import contextlib
import dataclasses

import yaml

from pathlib import Path

from . import branch_session, doxbench_threads, gate_console, generator
from . import session_git as session_git_mod
from . import session_pr
from .boundary import (
    GATE_SIDE_EFFECT, SOURCE_EDIT, BoundaryViolation, HumanGate,
)

# Verbs this slice executes. The gate bar keeps descriptors for the rest.
EXECUTING_VERBS = ("dispose-possible", "ratify", "propose",
                   "lens-save-recipe", "lens-add-as-cluster", "create-document",
                   "edit-document", "open-pr", "abandon-session",
                   "cleanup-abandoned-branch",
                   # add-wheel-action-verbs (011): `demote` graduates from
                   # descriptor-only to executing (it PLANS and RECORDS; the
                   # corpus moves stay a separate human-run step), and the three
                   # commission verbs join as ordinary recorded dispatches.
                   "demote", "promote-to-staging", "derive-possibles",
                   "research-brief",
                   # add-project-scoped-selection: the create-project
                   # commission — recorded dispatch of a project-register-edit;
                   # the aggregation-owned register is never written here.
                   # add-opendox-project-header: edit-project is that mechanic
                   # for an existing project's membership.
                   "create-project", "edit-project",
                   # T104 F10: the doxBench governed Save joined the if-chain
                   # (and SESSION_BEARING_VERBS) when it landed; the declaration
                   # here lagged, so the roster disagreed with what the route
                   # actually executes.
                   "first-edit",
                   # add-doxbench-editing-phase-b §12: the doxBench SHARE verb.
                   # It EXECUTES (it commits and it pushes), so it belongs here
                   # rather than in the descriptor-only remainder — and it is
                   # session-bearing below, which is what subjects it to the
                   # console-presence refusal every remote-writing verb carries.
                   "share-session")

# The verbs that can OPEN, WRITE INTO, or END a branch session. They are the
# verbs whose write lands in a per-repository worktree, so they are the verbs
# whose repository identity has to be CARRIED rather than inferred (PR #49 review
# finding 8, leg a).
SESSION_BEARING_VERBS = ("create-document", "edit-document", "open-pr",
                         "abandon-session", "cleanup-abandoned-branch",
                         "first-edit",
                         # §12.4: share-session writes into the session worktree
                         # AND performs a remote write with the engineer's own
                         # credential — the two properties this tuple exists to
                         # carry repository identity for, and the membership
                         # that makes FR-019's console-presence clause ENFORCED
                         # for it rather than merely observed.
                         "share-session")

# Action names recorded on the gate-action record for the two lens verbs. The
# names mirror the verb (honest audit), beside the enumerated console actions.
ACTION_LENS_SAVE_RECIPE = "lens-save-recipe"
ACTION_LENS_ADD_AS_CLUSTER = "lens-add-as-cluster"

_OUTCOMES = ("accepted", "rejected", "deferred")


def _str_or_none(value):
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _refused(message: str, status: int = 409) -> tuple[int, dict]:
    return status, {"ok": False, "error": "gate_refused", "message": message}


def _invalid(message: str) -> tuple[int, dict]:
    return 400, {"ok": False, "error": "invalid_body", "message": message}


def reachable_repositories(registry) -> tuple[str, ...]:
    """Every repository this plane can resolve a read to, from the registry's own
    key space (`(repository, ref)`). Duck-typed and tolerant: a registry-shaped
    double that cannot be enumerated contributes nothing, because this feeds a
    REFUSAL and a guess would be worse than the pre-existing behaviour."""
    entries = getattr(registry, "entries", None)
    if not callable(entries):
        return ()
    try:
        rows = entries()
    except Exception:  # noqa: BLE001 - a roster that cannot be read names nothing
        return ()
    names = {_str_or_none(getattr(row, "repository", None)) for row in rows}
    return tuple(sorted(name for name in names if name))


def refuse_foreign_repository(body: dict, repository: str | None, *,
                              reachable=()):
    """Refuse a session action whose repository is not the one this surface writes
    to, or cannot be established at all (PR #49 review finding 8, leg a; the
    second half added in wave 2). None means "carry on".

    The dashboard's repository SELECTOR is client-side: `_serve_snapshot`
    resolves `?repository=` without moving `registry.active`, so the page can be
    reading repoB while the server's session key is repoA and its `checkout_root`
    is repoA's tree. The route had no repository input at all, so a create issued
    from the repoB page opened a branch, a worktree, a document and a registry
    row in repoA — silently, keyed to the wrong repository, and invisible to the
    page that asked for it (reproduced during the adjudication).

    The identity is therefore CARRIED: both request shapes now send the
    repository the human is looking at, and a value this surface cannot honour is
    REFUSED rather than substituted. Fail-closed in both directions — a named
    repository with no server-side repository to compare against refuses too,
    because "cannot verify" is not "matches".

    REQUIRED-OR-DERIVED, not optional-and-ambient (wave 2). Wave 1 left a body
    that names NOTHING on the pre-existing path, described as compatibility; the
    replay pass then re-ran the review's ORIGINAL reproduction — the same body,
    with no `repository` key — and it still returned 200 and created a branch, a
    worktree, a document and a registry row in repoA for a tile that exists only
    in repoB. Compatibility for the caller is not confinement for the checkout, so
    the missing field is now DERIVED, and only where the derivation is the ONLY
    one available:

      * the plane reaches ONE repository (or none it can enumerate) — then the
        served repository is not a default, it is the only possible answer, and
        the action carries on exactly as it always did. This is every CLI-parity
        call site, every single-repository serve, and every test double.
      * the plane reaches MORE THAN ONE — then there is a real question, the
        server has no way to answer it, and substituting its own active entry is
        precisely how the cross-repository write happened. The action is REFUSED
        and names what to do.

    So a cross-repository write is now unreachable rather than unlikely: either
    the body names the repository and it is verified, or no other repository is
    reachable to write into by mistake.

    The refusals name only SERVED configuration — the served repository and, for
    the unresolved case, the roster the local plane already publishes at
    `/snapshot-index.json`. The rejected value is request data and never reaches
    the wire."""
    named = _str_or_none(body.get("repository"))
    served = _str_or_none(repository)
    if named is not None:
        if served is not None and named == served:
            return None
        return 409, {
            "ok": False, "error": "repository_mismatch",
            "message": (
                "this dashboard serves "
                + (f"{served!r}" if served else "no repository")
                + ", and a session action is confined to the repository it is "
                  "served from — reopen the dashboard on the repository you meant "
                  "to write to"),
        }
    candidates = sorted({name for name in
                         (served, *(_str_or_none(x) for x in reachable)) if name})
    if len(candidates) <= 1:
        return None
    return 409, {
        "ok": False, "error": "repository_unresolved",
        "message": (
            "this dashboard reaches " + str(len(candidates)) + " repositories ("
            + ", ".join(repr(name) for name in candidates) + ") and this action "
            "named none, so which checkout it belongs to cannot be established. "
            "The served repository is NOT a safe default here: the selector "
            "resolves another repository without moving the active entry, so a "
            "write substituted from it lands in a tree the page was not reading "
            "(PR #49 review finding 8). Send the repository the action is for — "
            "the workbench transports do — or serve one repository. Nothing was "
            "written."),
    }


def run_gate_action(verb: str, body: dict, *, checkout_root: Path,
                    actor: str, records_dir: str | None = None,
                    index_validator: Path | None = None,
                    snapshot_path: Path | None = None,
                    manifest_validator: Path | None = None,
                    xref_validator: Path | None = None,
                    session_registry=None,
                    project_register: Path | None = None,
                    repository: str | None = None,
                    tile_inventory=None,
                    session_notebook=None,
                    session_pull_requests=None,
                    provenance=None) -> tuple[int, dict]:
    """Execute one gate verb for the local action center. Returns
    ``(http_status, json_body)``; every refusal path returns a structured
    body and persists nothing (the console's own guarantee).

    The two lens verbs additionally need the served snapshot (to re-evaluate
    the recipe server-side) and the pinned manifest/cross-reference validators
    (``manifest_validator`` / ``xref_validator``); each defaults to walking up
    from the checkout when the caller passes None.

    ``checkout_root`` is and stays the SERVED checkout — the tree the dashboard
    projects, which no session operation may move (FR-004). The session's own
    root is NOT this argument: research R1 found that `serve.py` passes the
    served root here and not the active registry entry's `source_root`, so
    session-awareness cannot be had by "the active entry is the session". The
    route layer therefore resolves the session EXPLICITLY, from the three
    arguments below (007-workbench-branch-sessions T023/T025):

      * ``session_registry`` — where session LIVENESS lives (FR-008). Sessions
        are only available when a caller declares one, because a registry is the
        only place liveness can be keyed; `serve.py` passes its snapshot registry
        and every CLI-parity verb builds one for its own process. With none
        declared, `create-document` takes its pre-session path unchanged, even if
        the body carries a scope.
      * ``repository`` — the registry key's first half; two repositories can
        carry the same tile id, so a branch alone is not a session key.
      * ``tile_inventory`` — the LIVE tile inventory FR-026's scans are checked
        against (the staging folders plus the cluster / possible registers). It
        is passed IN rather than discovered, so the collision guard's inputs are
        declared by the caller and `branch_session` stays I/O-free.
      * ``session_notebook`` — the INJECTED notebook adapter (FR-036, FR-021,
        D16): `create-document` creates the session's `xf-session-*` notebook when
        it OPENS one, and both endings RETIRE it. None means this plane declares
        none, and an ending then reports honestly that there was no session
        notebook to retire rather than claiming one. `serve.py` declares one
        whenever its `notebook` capability is TRUE — a loopback bind, a real
        checkout, and `nlm` reachable (T074) — so a hosted plane never touches
        `nlm` and a full quota only DEGRADES the open (FR-042, D19).
      * ``session_pull_requests`` — the INJECTED `PullRequestPort` (FR-029's
        "injectable seam", `session_pr.py`). None means this plane declares no
        remote-write identity, and `open-pr` REFUSES rather than inventing one: the
        identity is ruled to be the invoking engineer's own `gh` auth (FR-034, D22)
        and a plane that cannot name a human cannot borrow one. `serve.py` DOES
        declare one — `_session_pull_requests()` returns a real
        `GhPullRequests(checkout_root)` whenever its `session` capability is true,
        and passes it into every gate dispatch (this sentence used to say "declares
        none yet — Phase 9's T082/T083 own that decision"; Phase 9 answered it, and
        the stale prose was the primary in-code description of the D22 confinement,
        PR #49 second-review tail B9). What keeps a personal credential off the
        hosted plane is therefore NOT the absence of a port here: it is the
        capability itself. `session: false` — a non-loopback bind, no real checkout,
        or no resolved actor — yields no port, no session verb and no session
        surface, so the only plane that ever speaks `gh` is a human's own loopback
        serve in their own checkout, which is exactly the D22 identity. The port
        also declares no merge/approve/review/bypass operation at all (FR-030), so
        even that plane cannot land its own pull request. Every test injects
        `FakePullRequests`.

    ``provenance`` (D23; Brett's 2026-07-27 ruling) is the GATEWAY fact the CALLER
    observed: a `gate_console.Provenance` naming the surface the invocation arrived
    on and how console presence was shown. It is passed IN, never derived here —
    this layer serves both gateways and cannot see either one's presence test, and
    a value it guessed would tag the wrong door. It is read from NO request body
    for the same reason: a caller-declared surface tags nothing. `None` (a caller
    that declares no gateway) writes a record with no `provenance` block, which is
    the pre-growth shape the grown schema still accepts.
    """
    records_dir = records_dir or gate_console.DEFAULT_RECORDS_DIR
    if not isinstance(body, dict):
        return _invalid("request body must be a JSON object")
    if verb in SESSION_BEARING_VERBS:
        # The roster comes from the DECLARED registry — the same object that
        # answers `?repository=` — so "how many repositories could this action
        # have meant" is asked of the thing that would serve them (wave 2).
        refusal = refuse_foreign_repository(
            body, repository, reachable=reachable_repositories(session_registry))
        if refusal is not None:
            return refusal
    if verb == "dispose-possible":
        return _dispose_possible(body, checkout_root, actor, records_dir,
                                 index_validator, provenance=provenance)
    if verb == "ratify":
        return _ratify(body, checkout_root, actor, records_dir,
                       provenance=provenance)
    if verb == "propose":
        return _propose(body, checkout_root, actor, records_dir,
                        session_registry=session_registry,
                        repository=repository, tile_inventory=tile_inventory,
                        provenance=provenance)
    if verb == "demote":
        return _demote(body, checkout_root, actor, records_dir,
                       snapshot_path, provenance=provenance)
    if verb == "promote-to-staging":
        return _promote_to_staging(body, checkout_root, actor, records_dir,
                                   provenance=provenance)
    if verb == "derive-possibles":
        return _derive_possibles(body, checkout_root, actor, records_dir,
                                 snapshot_path, provenance=provenance)
    if verb == "research-brief":
        return _research_brief(body, checkout_root, actor, records_dir,
                               provenance=provenance)
    if verb == "create-project":
        return _create_project(body, checkout_root, actor, records_dir,
                               session_registry=session_registry,
                               project_register=project_register,
                               provenance=provenance)
    if verb == "edit-project":
        return _edit_project(body, checkout_root, actor, records_dir,
                             session_registry=session_registry,
                             project_register=project_register,
                             provenance=provenance)
    if verb == "lens-save-recipe":
        return _lens_save_recipe(body, checkout_root, actor, records_dir,
                                 snapshot_path, manifest_validator,
                                 provenance=provenance)
    if verb == "lens-add-as-cluster":
        return _lens_add_as_cluster(body, checkout_root, actor, records_dir,
                                    snapshot_path, manifest_validator,
                                    xref_validator, provenance=provenance)
    if verb == "create-document":
        return _create_document(body, checkout_root, actor, records_dir,
                                snapshot_path, session_registry=session_registry,
                                repository=repository,
                                tile_inventory=tile_inventory,
                                session_notebook=session_notebook,
                                provenance=provenance)
    if verb == "edit-document":
        return _edit_document(body, checkout_root, actor, records_dir,
                              snapshot_path, session_registry=session_registry,
                              repository=repository,
                              tile_inventory=tile_inventory,
                              provenance=provenance)
    if verb == "open-pr":
        return _open_pr(body, checkout_root, actor, records_dir,
                        snapshot_path, session_registry=session_registry,
                        repository=repository, tile_inventory=tile_inventory,
                        session_notebook=session_notebook,
                        pull_requests=session_pull_requests,
                        provenance=provenance)
    if verb == "share-session":
        # The SAME `session_pull_requests` port `open-pr` is handed, because
        # §12's requirement is that the verb reuse the existing remote-write
        # path rather than introduce a second one. No `session_notebook`: a
        # share creates and retires nothing.
        return _share_session(body, checkout_root, actor, records_dir,
                              snapshot_path, session_registry=session_registry,
                              repository=repository,
                              tile_inventory=tile_inventory,
                              pull_requests=session_pull_requests,
                              provenance=provenance)
    if verb == "abandon-session":
        return _abandon_session(body, checkout_root, actor, records_dir,
                                snapshot_path, session_registry=session_registry,
                                repository=repository,
                                tile_inventory=tile_inventory,
                                session_notebook=session_notebook,
                                provenance=provenance)
    if verb == "cleanup-abandoned-branch":
        return _cleanup_abandoned_branch(
            body, checkout_root, actor, records_dir, snapshot_path,
            session_registry=session_registry, repository=repository,
            tile_inventory=tile_inventory, provenance=provenance)
    if verb == "first-edit":
        return _first_edit(body, checkout_root, actor, records_dir,
                           snapshot_path, session_registry=session_registry,
                           repository=repository,
                           tile_inventory=tile_inventory,
                           provenance=provenance)
    return 404, {"ok": False, "error": "unknown_verb",
                 "message": f"no executing route for verb {verb!r}"}


def _dispose_possible(body: dict, root: Path, actor: str, records_dir: str,
                      index_validator, *, provenance=None) -> tuple[int, dict]:
    from doc_health import derive_possibles as dp  # lazy: sibling package

    possible_id = _str_or_none(body.get("possible_id"))
    outcome = _str_or_none(body.get("outcome"))
    if not possible_id or outcome not in _OUTCOMES:
        return _invalid("dispose-possible requires possible_id and outcome "
                        "in {accepted, rejected, deferred}")
    gate = HumanGate(
        root, [records_dir, dp.INDEX_REL, dp.INDEX_MD_REL],
        human_actor=actor)
    try:
        res = gate_console.dispose_possible(
            gate, possible_id, outcome,
            reason=_str_or_none(body.get("reason")),
            citation=_str_or_none(body.get("citation")),
            note=_str_or_none(body.get("note")),
            records_dir=records_dir, index_validator=index_validator,
            provenance=provenance)
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    return 200, {
        "ok": True,
        "verb": "dispose-possible",
        "possible_id": res.possible_id,
        "outcome": res.outcome,
        "state": res.entry.get("state"),
        "record": str(res.record_path.relative_to(root)),
        "hint": "regenerate the snapshot to fold the disposition into the views",
    }


def _ratify(body: dict, root: Path, actor: str, records_dir: str, *,
            provenance=None) -> tuple[int, dict]:
    change_id = _str_or_none(body.get("change_id"))
    if not change_id:
        return _invalid("ratify requires change_id")
    gate = HumanGate(root, [records_dir], human_actor=actor)
    try:
        res = gate_console.ratify(
            gate, change_id, _str_or_none(body.get("ratifier")) or actor,
            date=_str_or_none(body.get("date")), records_dir=records_dir,
            provenance=provenance)
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    return 200, {
        "ok": True,
        "verb": "ratify",
        "change_id": change_id,
        "ratifier": res.ratification["ratifier"],
        "date": res.ratification["date"],
        "record": str(res.record_path.relative_to(root)),
    }


def session_precondition_for(registry, *, repository: str | None, topic_id: str,
                             tile_inventory=None):
    """The FR-023 precondition `propose` evaluates, as a callable (T054).

    A CALLABLE rather than a check inlined here, because WHERE it runs is the
    requirement: it must fire AFTER `propose`'s own missing-topic and
    duplicate-dispatch refusals — a tile that does not exist, or that already
    carries an undelivered commission, has a more specific problem than "a session
    holds it" — and BEFORE the first write. Only `kickoff.propose` knows that
    point, and `kickoff` must not learn what a snapshot registry is, so the route
    hands it this closure and the engine calls it.

    Returns None when no registry is declared: with nowhere for liveness to live
    there is no session to refuse over (FR-008), which is also what keeps every
    pre-existing `propose` caller byte-identical."""
    if registry is None:
        return None
    tile = branch_session.Tile(branch_session.STAGED_TOPIC, topic_id)

    def precondition() -> None:
        branch_session.assert_no_live_session(
            registry, repository or "", tile, inventory=tile_inventory,
            verb="propose")

    return precondition


def _propose(body: dict, root: Path, actor: str, records_dir: str, *,
             session_registry=None, repository: str | None = None,
             tile_inventory=None, provenance=None) -> tuple[int, dict]:
    from . import kickoff as kickoff_mod  # lazy: mirrors gate_console's cycle note

    topic_id = _str_or_none(body.get("topic_id"))
    if not topic_id:
        return _invalid("propose requires topic_id")
    gate = HumanGate(root, [records_dir], human_actor=actor)
    try:
        if tile_inventory is None and session_registry is not None:
            tile_inventory = discover_tile_inventory(root)
        res = gate_console.GateConsole(gate, records_dir=records_dir).propose(
            topic_id,
            outline=_str_or_none(body.get("outline")),
            workflow=_str_or_none(body.get("workflow")),
            note=_str_or_none(body.get("note")),
            # FR-023: refused while a live session holds the tile, keyed on the
            # registry ENTRY and never on branch existence — a branch surviving an
            # abandon does not block (D15, G2).
            session_precondition=session_precondition_for(
                session_registry, repository=repository, topic_id=topic_id,
                tile_inventory=tile_inventory),
            provenance=provenance)
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except branch_session.SessionRefused as exc:   # the live-session precondition
        return _refused(exc.report())
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    except OSError as exc:                         # unreadable staging tree
        return _refused(f"propose could not be evaluated: {exc}")
    return 200, {
        "ok": True,
        "verb": "propose",
        "topic_id": topic_id,
        "workflow": res.job["workflow"],
        "record": str(res.record_path.relative_to(root)),
        "job": str(res.job_path.relative_to(root)),
        "hint": "proposal authoring commissioned — the change lands via the "
                "authoring lane for review and ratification",
    }


# ==========================================================================
# THE WHEEL ACTION-ROW VERBS (add-wheel-action-verbs; 011)
#
# Four handlers, one discipline. Each is THIN GLUE: it validates only the body
# shape, hands everything else to the engine, and reports the engine's own
# reason verbatim on refusal. Every guard — human-only, target existence,
# promotability, duplicate — lives in the engine, so the CLI and the route
# cannot drift apart.
#
# `demote` is SNAPSHOT-DRIVEN: the demotion planner resolves the change, its
# status, its files and its origin staging topic from the served snapshot, so
# the handler needs `snapshot_path`. The two possibles verbs re-read the pinned
# checkout's register instead, and `derive-possibles` validates its cluster
# against the snapshot's cluster set. That asymmetry is deliberate (FR-023).
# ==========================================================================


def _demote(body: dict, root: Path, actor: str, records_dir: str,
            snapshot_path, *, provenance=None) -> tuple[int, dict]:
    """PLAN + RECORD a reverse transition. It does NOT execute the plan and
    exposes no switch that could: the corpus file moves stay the separate,
    deliberately human-run step the engine already implements (design D1,
    FR-004, NG-005). Any `execute`-shaped field in the body is ignored, because
    the handler never reads one.
    """
    change_id = _str_or_none(body.get("change_id"))
    if not change_id:
        return _invalid("demote requires change_id")
    # `reason` is deliberately NOT pre-validated here: the demotion planner
    # owns that rule and refuses an empty reason with its own message, so the
    # engine stays the single choke point and the route cannot drift from it
    # (contract: a missing reason is a 409 engine refusal, not a 400).
    reason = _str_or_none(body.get("reason")) or ""
    snapshot = _load_snapshot(snapshot_path)
    if not isinstance(snapshot, dict):
        return _refused(
            "demote refused: the served snapshot could not be read, so the "
            "target change cannot be resolved — nothing was planned or recorded.")
    gate = HumanGate(root, [records_dir], human_actor=actor)
    try:
        res = gate_console.GateConsole(gate, records_dir=records_dir).demote(
            snapshot, change_id, reason=reason,
            staging_topic=_str_or_none(body.get("staging_topic")),
            provenance=provenance)
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    except OSError as exc:
        return _refused(f"demote could not be evaluated: {exc}")
    return 200, {
        "ok": True,
        "verb": "demote",
        "change_id": change_id,
        "plan": str(res.plan_path.relative_to(root)),
        "record": str(res.record_path.relative_to(root)),
        "hint": "planned + recorded — run the recorded plan deliberately to "
                "move the files; the dashboard never moves them",
    }


def _commission_route(verb: str, target_field: str, body: dict, root: Path,
                      actor: str, records_dir: str, *, engine_kwargs=None,
                      provenance=None, hint: str) -> tuple[int, dict]:
    """The shared half of the three commission routes."""
    target = _str_or_none(body.get(target_field))
    if not target:
        return _invalid(f"{verb} requires {target_field}")
    gate = HumanGate(root, [records_dir], human_actor=actor)
    console = gate_console.GateConsole(gate, records_dir=records_dir)
    call = getattr(console, verb.replace("-", "_"))
    try:
        res = call(target,
                   note=_str_or_none(body.get("note")),
                   outline=_str_or_none(body.get("outline")),
                   workflow=_str_or_none(body.get("workflow")),
                   provenance=provenance, **(engine_kwargs or {}))
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    except OSError as exc:
        return _refused(f"{verb} could not be evaluated: {exc}")
    return 200, {
        "ok": True,
        "verb": verb,
        target_field: target,
        "workflow": res.job["workflow"],
        "record": str(res.record_path.relative_to(root)),
        "job": str(res.job_path.relative_to(root)),
        "hint": hint,
    }


def _promote_to_staging(body: dict, root: Path, actor: str, records_dir: str, *,
                        provenance=None) -> tuple[int, dict]:
    """Commission the organization of an ACCEPTED possible into a staging
    fragment. The possibles register is never mutated by this call."""
    return _commission_route(
        "promote-to-staging", "possible_id", body, root, actor, records_dir,
        engine_kwargs={"topic": _str_or_none(body.get("topic"))},
        provenance=provenance,
        hint="staging-fragment authoring commissioned — the fragment lands for "
             "review, and the pick edge is recorded only when it is delivered")


def _derive_possibles(body: dict, root: Path, actor: str, records_dir: str,
                      snapshot_path, *, provenance=None) -> tuple[int, dict]:
    """Commission a cluster-scoped run of the ratified derivation lane. The
    cluster is validated against the SNAPSHOT's cluster set."""
    return _commission_route(
        "derive-possibles", "cluster_id", body, root, actor, records_dir,
        engine_kwargs={"snapshot": _load_snapshot(snapshot_path)},
        provenance=provenance,
        hint="cluster-scoped derivation commissioned — candidates arrive "
             "pending_review and still require a human verdict")


def _research_brief(body: dict, root: Path, actor: str, records_dir: str, *,
                    provenance=None) -> tuple[int, dict]:
    """Commission a pre-verdict evidence brief. NO register-state guard: a
    disposed possible is accepted here by design (FR-018a) — the wheel hides
    the verb, the engine stays permissive."""
    return _commission_route(
        "research-brief", "possible_id", body, root, actor, records_dir,
        provenance=provenance,
        hint="research brief commissioned — it informs the verdict and never "
             "makes it")


def _create_project(body: dict, root: Path, actor: str, records_dir: str, *,
                    session_registry=None, project_register: Path | None = None,
                    provenance=None) -> tuple[int, dict]:
    """Commission a project-register edit (add-project-scoped-selection).

    Unlike the other commissions, the TARGET id is not in the body — the
    engine slugs it from the proposed name (design D-a) — so this handler
    does not ride `_commission_route`. The member roster is the registry's
    own reachable set (the same object that answers `?repository=`), which
    WIDENS the register-derived universe to whatever this serve can read;
    the register itself is discovered by the engine from the checkout
    (aggregation-owned, one or more levels up)."""
    name = _str_or_none(body.get("name"))
    if not name:
        return _invalid("create-project requires name")
    repositories = body.get("repositories", [])
    if not isinstance(repositories, list):
        return _invalid("create-project repositories must be a list")
    # an EMPTY list is legal (Brett's 2026-08-06 ruling): the project is
    # created first and gains members later through edit-project
    gate = HumanGate(root, [records_dir], human_actor=actor)
    console = gate_console.GateConsole(gate, records_dir=records_dir)
    try:
        res = console.create_project(
            name, repositories=repositories,
            roster=reachable_repositories(session_registry),
            register_source=project_register,
            note=_str_or_none(body.get("note")),
            outline=_str_or_none(body.get("outline")),
            workflow=_str_or_none(body.get("workflow")),
            provenance=provenance)
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    except OSError as exc:
        return _refused(f"create-project could not be evaluated: {exc}")
    return 200, {
        "ok": True,
        "verb": "create-project",
        "project_id": res.job["project_id"],
        "workflow": res.job["workflow"],
        "record": str(res.record_path.relative_to(root)),
        "job": str(res.job_path.relative_to(root)),
        "hint": "project-register edit commissioned — the register is "
                "aggregation-owned; the fulfilment applies and validates the "
                "edit, and the project appears on the next publication",
    }


def _edit_project(body: dict, root: Path, actor: str, records_dir: str, *,
                  session_registry=None, project_register: Path | None = None,
                  provenance=None) -> tuple[int, dict]:
    """Commission a membership edit of one existing project
    (add-opendox-project-header D15). Same posture as create-project: the
    register is never written here; the roster is the registry's own
    reachable set."""
    project_id = _str_or_none(body.get("project_id"))
    if not project_id:
        return _invalid("edit-project requires project_id")
    add = body.get("add")
    remove = body.get("remove")
    if add is not None and not isinstance(add, list):
        return _invalid("edit-project add must be a list")
    if remove is not None and not isinstance(remove, list):
        return _invalid("edit-project remove must be a list")
    gate = HumanGate(root, [records_dir], human_actor=actor)
    console = gate_console.GateConsole(gate, records_dir=records_dir)
    try:
        res = console.edit_project(
            project_id, add=add, remove=remove,
            roster=reachable_repositories(session_registry),
            register_source=project_register,
            note=_str_or_none(body.get("note")),
            outline=_str_or_none(body.get("outline")),
            workflow=_str_or_none(body.get("workflow")),
            provenance=provenance)
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    except OSError as exc:
        return _refused(f"edit-project could not be evaluated: {exc}")
    return 200, {
        "ok": True,
        "verb": "edit-project",
        "project_id": project_id,
        "add": res.job["add"],
        "remove": res.job["remove"],
        "workflow": res.job["workflow"],
        "record": str(res.record_path.relative_to(root)),
        "job": str(res.job_path.relative_to(root)),
        "hint": "membership edit commissioned — pending until the fulfilment "
                "lands the register edit",
    }


# ==========================================================================
# LENS VERBS — save-recipe / add-as-cluster (add-lens-gate-verbs)
#
# The keyword lens builds a recipe (checked/pinned keywords) + reasoned
# overrides and, on a read-only surface, stops at a PLAN. These verbs execute
# that plan through the tested engines as recorded human dispatches. THIN GLUE:
# the route re-evaluates the recipe server-side against the served snapshot
# (`lens.build_workbench_from_recipe`, which drives `workbench.py`'s reasoned-
# override guard), NEVER trusting a browser-assembled member list; then it
# saves the manifest (schema-validated at write) and, for add-as-cluster, the
# `pending_review` human-seen submission (evidence contract enforced BEFORE
# persistence). No engine is modified.
# ==========================================================================


def _load_snapshot(snapshot_path):
    if snapshot_path is None:
        return None
    try:
        import json
        return json.loads(Path(snapshot_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _str_map(value):
    """A {document: reason} override map from an untrusted body, or None when
    the value is present but not an object of strings. An absent value is {}."""
    if value is None:
        return {}
    if not isinstance(value, dict):
        return None
    out: dict[str, str] = {}
    for key, val in value.items():
        if not isinstance(key, str) or not isinstance(val, str):
            return None
        out[key] = val
    return out


def _str_list(value):
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
        return None
    return list(value)


def _write_lens_record(human: HumanGate, records_dir: str, *, action: str,
                       set_slug: str, at: str, artifacts, notes=None,
                       provenance=None):
    """Write a schema-shaped gate-action record for a lens verb through the
    HumanGate — the same audit artifact dispose/ratify/propose emit, targeting
    the workbench SET (`target.set`). Returns (record_path, record_relpath).

    `provenance` (D23) is the GATEWAY fact the caller observed, stamped between
    `target` and `at` exactly where `gate_console.build_gate_action_record` puts
    it — this verb family builds its record inline because its `target.set` has no
    builder keyword, so the block is added here in the same position and under the
    same rule: a `Provenance` instance only, never a body value."""
    record: dict = {
        "schema_version": gate_console.RECORD_SCHEMA_VERSION,
        "kind": gate_console.RECORD_KIND,
        "actor": human.human_actor,
        "action": action,
        "target": {"set": set_slug},
    }
    if provenance is not None:
        if not isinstance(provenance, gate_console.Provenance):
            raise gate_console.GateRefused(
                "gateway provenance is an OBSERVED fact, not a supplied value "
                "(D23)")
        record["provenance"] = provenance.as_record()
    record["at"] = at
    record["artifacts"] = [dict(a) for a in artifacts]
    if notes:
        record["notes"] = notes
    rel = gate_console.gate_action_record_relpath(records_dir, action, set_slug, at)
    # AMENDED 2026-07-27 (D23, Brett's ruling item 2): this banner used to claim
    # "Agents structurally cannot author one". The control is console PRESENCE, not
    # authentication — see `gate_console._RECORD_BANNER` for the same correction.
    banner = (
        "# gate-action record — a HUMAN-gate lens dispatch audit entry\n"
        "# (gate-action-record.schema.yaml). The route rejects and reports a caller\n"
        "# that cannot show it originates from the human console; that is a\n"
        "# console-PRESENCE control, not authentication (design D23) —\n"
        "# `provenance`, where present, names the door and the proof shown.\n"
    )
    body = yaml.safe_dump(record, sort_keys=False, default_flow_style=False,
                          allow_unicode=True)
    path = human.write_gate_artifact(rel, banner + body)
    return path, str(path.relative_to(human.output.root))


def _refuse_duplicate_set(root: Path, name: str) -> None:
    """Refuse a set name whose manifest already exists — and NEVER crash asking.

    The `.exists()` was unguarded, and `wb.manifest_relpath` derived a path from
    the set name, which for `lens-save-recipe` is machine-derived from every
    checked keyword. Past the filesystem's 255-byte component limit the question
    itself raised `OSError: [Errno 36] File name too long`, so the verb blew up
    INSIDE ITS OWN DUPLICATE CHECK — before any write, and unable even to refuse
    (T092 acceptance sweep, defect 2). `wb.slug` is bounded now, which is the
    real fix; this is the belt-and-braces half, because a path is a question to
    the operating system and the answer can always be an error (an unreadable
    parent, a name the filesystem rejects for its own reasons) — and a gate verb
    answers with a refusal, never with a traceback."""
    from . import workbench as wb
    rel = wb.manifest_relpath(name)
    try:
        exists = (root / rel).exists()
    except OSError as exc:
        raise wb.WorkbenchError(
            f"the workbench manifest path for the set name {name!r} could not be "
            f"checked: {rel} — {exc.strerror or exc}. Nothing was written; choose "
            "a shorter or simpler set name") from exc
    if exists:
        raise wb.WorkbenchError(
            f"a workbench set named {name!r} already exists at {rel} — choose a "
            "different name; executing would overwrite existing session state")


def execute_lens_save_recipe(gate, *, repository: str, name: str,
                             checked, pinned, snapshot, includes, excludes,
                             records_dir: str, at: str | None = None,
                             manifest_validator: Path | None = None,
                             provenance=None) -> dict:
    """Drive the save-recipe plan through the tested engines under a HumanGate.
    Human-only: an OutputBoundary / agent path is rejected (BoundaryViolation)
    before anything is built or written — the same structural guard every gate
    action uses."""
    from . import lens, workbench as wb

    human = gate_console.require_human_gate(gate)   # agent path -> BoundaryViolation
    root = human.output.root
    at = at or gate_console._utcnow()
    _refuse_duplicate_set(root, name)               # duplicate set name -> refuse
    w = lens.build_workbench_from_recipe(           # reasoned-override guard fires here
        repository, name, checked, pinned, snapshot,
        includes=includes, excludes=excludes, now=at)
    manifest_path = wb.save(w, human.output, validate=True,   # schema-valid at write
                            validator=manifest_validator)
    manifest_rel = str(manifest_path.relative_to(root))
    _, record_rel = _write_lens_record(
        human, records_dir, action=ACTION_LENS_SAVE_RECIPE,
        set_slug=wb.slug(name), at=at, provenance=provenance,
        artifacts=[{"kind": gate_console.ART_OTHER, "reference": manifest_rel}])
    return {
        "ok": True,
        "verb": "lens-save-recipe",
        "set": name,
        "manifest": manifest_rel,
        "record": record_rel,
        "members": len(w.member_documents()),
        "hint": "recipe saved as a gitignored workbench manifest through the "
                "boundary; re-runnable as the corpus grows",
    }


def execute_lens_add_as_cluster(gate, *, repository: str, name: str,
                                checked, pinned, snapshot, includes, excludes,
                                submission, records_dir: str,
                                at: str | None = None,
                                manifest_validator: Path | None = None,
                                xref_validator: Path | None = None,
                                provenance=None) -> dict:
    """Drive the add-as-cluster plan: the recipe-seeded manifest PLUS the
    pending_review human-seen submission into the cross-reference queue. The
    evidence contract is enforced BEFORE any write (human_seen), and the
    generated cross-reference index is NEVER touched. Human-only."""
    from . import lens, workbench as wb

    human = gate_console.require_human_gate(gate)   # agent path -> BoundaryViolation
    root = human.output.root
    at = at or gate_console._utcnow()
    _refuse_duplicate_set(root, name)               # duplicate set name -> refuse
    w = lens.build_workbench_from_recipe(
        repository, name, checked, pinned, snapshot,
        includes=includes, excludes=excludes, now=at)
    repo_root = manifest_validator.resolve().parents[1] if manifest_validator else None
    res = lens.add_as_cluster(                       # evidence enforced before persistence
        w, human.output, snapshot, submission, now=at,
        validate=True, validator=manifest_validator,
        xref_validator=xref_validator, repo=repo_root)
    manifest_rel = str(res.manifest_path.relative_to(root))
    _, record_rel = _write_lens_record(
        human, records_dir, action=ACTION_LENS_ADD_AS_CLUSTER,
        set_slug=wb.slug(name), at=at, notes=res.note, provenance=provenance,
        artifacts=[
            {"kind": gate_console.ART_OTHER, "reference": manifest_rel},
            {"kind": gate_console.ART_OTHER, "reference": res.queue_relpath},
        ])
    return {
        "ok": True,
        "verb": "lens-add-as-cluster",
        "set": name,
        "manifest": manifest_rel,
        "pending_entry": res.queue_relpath,
        "cluster_id": res.cluster_id,
        "record": record_rel,
        "note": res.note,
        "hint": "workbench set created and the human-seen proposal queued "
                "(pending_review) — a disposing authority reviews it; the "
                "generated cross-reference index is untouched",
    }


def _lens_common(body: dict, snapshot):
    """Parse + validate the shared recipe fields of a lens verb body. Returns
    either (None, error_tuple) or (parsed_dict, None)."""
    name = _str_or_none(body.get("name"))
    if not name:
        return None, _invalid("a lens verb requires a non-empty set name")
    checked = _str_list(body.get("checked"))
    if checked is None:
        return None, _invalid("checked must be a list of keyword strings")
    if not checked:
        return None, _invalid("a lens recipe requires at least one checked keyword")
    pinned = _str_list(body.get("pinned"))
    if pinned is None:
        return None, _invalid("pinned must be a list of keyword strings")
    includes = _str_map(body.get("includes"))
    if includes is None:
        return None, _invalid("includes must be a {document: reason} object")
    excludes = _str_map(body.get("excludes"))
    if excludes is None:
        return None, _invalid("excludes must be a {document: reason} object")
    repository = (_str_or_none(body.get("repository"))
                  or (snapshot.get("repository") if isinstance(snapshot, dict) else None)
                  or "")
    return {"name": name, "checked": checked, "pinned": pinned,
            "includes": includes, "excludes": excludes,
            "repository": repository}, None


def _lens_save_recipe(body: dict, root: Path, actor: str, records_dir: str,
                      snapshot_path, manifest_validator, *,
                      provenance=None) -> tuple[int, dict]:
    from . import workbench as wb
    from .workbench import WorkbenchError, ManifestInvalid

    snapshot = _load_snapshot(snapshot_path)
    if not isinstance(snapshot, dict):
        return _invalid("the served snapshot is unavailable — cannot re-evaluate "
                        "the recipe server-side")
    parsed, err = _lens_common(body, snapshot)
    if err:
        return err
    gate = HumanGate(root, [records_dir, wb.WORKBENCH_DIR], human_actor=actor)
    try:
        result = execute_lens_save_recipe(
            gate, snapshot=snapshot, records_dir=records_dir,
            manifest_validator=manifest_validator, provenance=provenance,
            **parsed)
    except WorkbenchError as exc:            # reasonless override, dup name, W1
        return _refused(str(exc))
    except ManifestInvalid as exc:           # schema validation failed at write
        return _refused(str(exc))
    except BoundaryViolation as exc:         # agent path (structural)
        return _refused(exc.refusal.report(), status=403)
    return 200, result


def _lens_add_as_cluster(body: dict, root: Path, actor: str, records_dir: str,
                         snapshot_path, manifest_validator,
                         xref_validator, *, provenance=None) -> tuple[int, dict]:
    from . import workbench as wb, human_seen as hs
    from .workbench import WorkbenchError, ManifestInvalid

    snapshot = _load_snapshot(snapshot_path)
    if not isinstance(snapshot, dict):
        return _invalid("the served snapshot is unavailable — cannot re-evaluate "
                        "the recipe server-side")
    parsed, err = _lens_common(body, snapshot)
    if err:
        return err
    submission, err = _build_submission(body.get("evidence"), parsed["repository"],
                                        actor)
    if err:
        return err
    gate = HumanGate(root, [records_dir, wb.WORKBENCH_DIR], human_actor=actor)
    try:
        result = execute_lens_add_as_cluster(
            gate, snapshot=snapshot, submission=submission,
            records_dir=records_dir, manifest_validator=manifest_validator,
            xref_validator=xref_validator, provenance=provenance, **parsed)
    except hs.SubmissionRefused as exc:      # missing/malformed evidence contract
        return _refused(str(exc))
    except hs.SubmissionInvalid as exc:      # queue entry failed the xref validator
        return _refused(str(exc))
    except WorkbenchError as exc:            # reasonless override, dup name, W1
        return _refused(str(exc))
    except ManifestInvalid as exc:           # manifest schema validation failed
        return _refused(str(exc))
    except BoundaryViolation as exc:         # agent path (structural)
        return _refused(exc.refusal.report(), status=403)
    return 200, result


# ==========================================================================
# CREATE-DOCUMENT — the workbench's ONE write (add-workbench-bullseye-and-create)
#
# The human decides, in the scope that justifies it, that a document needs to
# exist. Everything the create needs was already implemented and tested:
# `authoring.create_scaffold` renders the controlled header block and writes it
# through `boundary.OutputBoundary.create_document`, which is CREATE-ONLY — an
# existing target refuses as SOURCE_EDIT and is never overwritten. This verb is
# the missing wire, nothing more: validate + normalize the body, construct the
# HumanGate with the server's resolved actor, drive the engine, record the
# dispatch, surface every engine refusal verbatim (design D10).
#
# Human-only by CONSTRUCTION (design D11): `require_human_gate` admits a
# `HumanGate` and rejects an `OutputBoundary` (the machinery/agent chokepoint)
# with a reported refusal. Document creation BY an agent is a different,
# already-specified surface (`authoring.agent_capture`, with its own header
# enforcement) — this verb neither widens nor replaces it.
#
# NOTE on the allowlist (design D10 consequence a): `create_document`
# deliberately does NOT consult the boundary's output allowlist — `area` is a
# SOURCE directory like `ideation/brainstorm/`, not a declared output path — so
# the create-only refusal is the whole protection, by design. The gate's
# allowlist still governs the gate-action record, which IS a declared output.
# ==========================================================================


def execute_create_document(gate, *, area: str, title: str, summary: str,
                            topics, repository_context: str,
                            kind: str | None = None, status: str | None = None,
                            possible_feats=(), source: str | None = None,
                            records_dir: str, at: str | None = None,
                            session=None, git=None, provenance=None) -> dict:
    """Drive `authoring.create_scaffold` through the gate as a recorded human
    dispatch. Human-only: an OutputBoundary / agent path is rejected
    (BoundaryViolation) before anything is written. Returns the response body
    the route and the CLI both report from.

    `session` (a `branch_session.SessionOpen`) + `git` (the `SessionGit` seam)
    switch this into the SESSION form (FR-006, FR-018,
    007-workbench-branch-sessions T023). Nothing about the create itself changes:
    the SAME `create_scaffold` runs, still create-only, so an existing target
    still refuses as `SOURCE_EDIT` and is never overwritten. Two things differ,
    and both come from the caller having rooted the `HumanGate` at the WORKTREE:

      * the document and its record land in the worktree, not the served
        checkout, and
      * they are COMMITTED TOGETHER as this action's single commit, with the
        record naming its own action stamp and the resulting sha reported in the
        response rather than written into the record (a commit cannot contain its
        own sha — data-model SessionCommit).

    Outside a session (`session is None`) the path is byte-identical to the
    pre-session one: one record written through the gate, no git write at all."""
    from . import authoring

    human = gate_console.require_human_gate(gate)   # agent path -> BoundaryViolation
    root = human.output.root
    at = at or gate_console._utcnow()
    if session is not None:
        if git is None:
            raise branch_session.SessionRefused(
                "a session create needs the git seam that commits it; a session "
                "write is never left uncommitted (FR-006)")
        if Path(session.worktree).resolve() != Path(root).resolve():
            raise branch_session.SessionRefused(
                f"the gate is rooted at {root} but the session's worktree is "
                f"{session.worktree}: a session create is written through a gate "
                "rooted at the WORKTREE, so its record rides the same commit as "
                "its document (FR-006, plan Constraint 10)")
    # `brainstorm` in EVERY area (Brett's 2026-07-25 ruling on open question 1):
    # the area places the document — which is the packet tie — and the status
    # says only what stage it is at, which for a fresh capture is `brainstorm`.
    resolved_status = status or authoring.DEFAULT_STATUS
    path = authoring.create_scaffold(                # create-only; existing -> SOURCE_EDIT
        human.output, area=area, title=title, summary=summary, topics=topics,
        repository_context=repository_context,
        kind=kind or authoring.DEFAULT_KIND, status=resolved_status,
        possible_feats=possible_feats, source=source, now=at)
    rel = str(path.relative_to(root))
    # the created document IS the artifact, as a first-class `document` kind
    # (design D12 / open question 4's RULING — the `other` of the first pass
    # is reversed, and the grown schema now REQUIRES this kind here)
    artifacts = [{"kind": gate_console.ART_DOCUMENT, "reference": rel}]
    if session is not None:
        artifacts.append(branch_session.commit_artifact(
            branch_session.action_stamp(at)))
    record = gate_console.build_gate_action_record(
        actor=human.human_actor, action=gate_console.ACTION_CREATE_DOCUMENT,
        at=at, document=rel, artifacts=artifacts, notes=source,
        # the GATEWAY fact the caller observed (D23) — the surface this create
        # arrived on and how console presence was shown. Passed in, never derived:
        # this engine serves both gateways and can see neither presence test.
        provenance=provenance,
        # `ref` stays OPTIONAL in the schema and is populated only in a session —
        # inside one the route ALWAYS populates it, because a session record that
        # does not name its branch audits nothing (D13)
        ref=session.branch if session is not None else None)
    if session is None:
        record_path = gate_console.write_gate_action_record(human, records_dir,
                                                           record)
        return {
            "ok": True,
            "verb": "create-document",
            "path": rel,
            "record": str(record_path.relative_to(root)),
            "status": resolved_status,
            "hint": "created through the tested authoring scaffold (create-only) — "
                    "open it and write; regenerate the snapshot to fold it into the views",
        }
    commit = branch_session.commit_gate_action(
        human, git, worktree=root, branch=session.branch, record=record,
        documents=[rel], records_dir=records_dir,
        summary=f"create-document: {rel}",
        # the session carries the registry its snapshot is keyed in, so this
        # action regenerates the session's projection as part of itself (FR-010)
        session=session)
    result = {
        "ok": True,
        "verb": "create-document",
        "path": rel,
        "record": commit.record_relpath,
        "status": resolved_status,
        "ref": session.branch,
        "commit": commit.sha,
        "joined": session.joined,
        "hint": "created on the session branch through the tested authoring "
                "scaffold (create-only) — this action is ONE commit carrying the "
                "document and its gate-action record; save the session with "
                "`open-pr` when it is ready for review",
    }
    # FR-042 / D19: a session whose notebook could not be created says so, in the
    # response the human is already reading. Present only when there is something
    # to say, so the ordinary success shape is unchanged. The notice comes off the
    # session AS OF THE COMMIT: the create is deferred to the first successful
    # commit (PR #49 finding 3), so the open itself has nothing to report yet.
    notice = getattr(commit.session, "notebook_notice", None) \
        or session.notebook_notice
    if notice:
        result["notebook_notice"] = notice
    return result


def _create_body(body: dict, snapshot):
    """Parse + validate a create-document body. Returns (parsed, None) or
    (None, error_tuple). `repository_context` defaults from the SERVED
    snapshot's repository (the same defaulting the lens verbs use), and the
    `Status:` default is `brainstorm` in EVERY area (open question 1's
    ruling — NOT area-derived; placement carries the packet tie)."""
    from . import authoring

    title = _str_or_none(body.get("title"))
    if not title:
        return None, _invalid("create-document requires a non-empty title")
    summary = _str_or_none(body.get("summary"))
    if not summary:
        return None, _invalid("create-document requires a non-empty summary "
                              "(one sentence — it is never generated for you)")
    topics = _str_list(body.get("topics"))
    if topics is None:
        return None, _invalid("topics must be a list of keyword strings")
    topics = [t.strip() for t in topics if t and t.strip()]
    if not topics:
        return None, _invalid("create-document requires at least one topic "
                              "(the header contract's Topics: field)")
    feats = _str_list(body.get("possible_feats"))
    if feats is None:
        return None, _invalid("possible_feats must be a list of strings")
    area = authoring.normalized_area(
        _str_or_none(body.get("area")) or authoring.DEFAULT_AREA)
    # The area is CONFINED, not merely non-escaping: `authoring.area_refusal`
    # enforces the whole sentence this refusal has always asserted — inside
    # `ideation/`, and never inside the gate-records prefix the served-checkout
    # fingerprint excludes (PR #49 wave-2 critic; see that function for what each
    # condition prevents).
    refusal = authoring.area_refusal(area)
    if refusal is not None:
        return None, _invalid(refusal)
    status = _str_or_none(body.get("status")) or authoring.DEFAULT_STATUS
    if status not in authoring.CREATABLE_STATUSES:
        return None, _invalid(
            "status must be one of "
            f"{', '.join(authoring.CREATABLE_STATUSES)} — a new document is "
            "never born ratified, standard, superseded, retired, or record")
    repository_context = (_str_or_none(body.get("repository_context"))
                          or (snapshot.get("repository")
                              if isinstance(snapshot, dict) else None)
                          or "")
    if not repository_context:
        return None, _invalid("create-document requires repository_context "
                              "(the served snapshot names no repository)")
    # The TILE's scope identity (007-workbench-branch-sessions T023a). BOTH
    # fields are OPTIONAL and BOTH are required together: `scope_kind` without
    # `scope_id` (or the reverse) names no tile, so it is a shaping error rather
    # than a silent no-scope create. Absent entirely -> the pre-session path,
    # byte-identical, which is what keeps every existing caller working (FR-018).
    scope_kind = _str_or_none(body.get("scope_kind"))
    scope_id = _str_or_none(body.get("scope_id"))
    if bool(scope_kind) != bool(scope_id):
        return None, _invalid(
            "scope_kind and scope_id are given together or not at all — one "
            "without the other names no tile, so no branch session can be "
            "resolved from it")
    if scope_kind and scope_kind not in branch_session.SCOPE_KINDS:
        return None, _invalid(
            "scope_kind must be one of "
            f"{', '.join(branch_session.SCOPE_KINDS)}")
    # The human's ANSWER to the FR-025 resume-or-new report (T056). Optional by
    # design: absent is what the FIRST write sends, and a surviving abandoned
    # branch then REPORTS the choice rather than having one made for it.
    continuation = _str_or_none(body.get("continuation"))
    try:
        continuation = branch_session.normalize_continuation(continuation)
    except branch_session.SessionRefused as exc:
        return None, _invalid(exc.report())
    return {
        "area": area, "title": title, "summary": summary, "topics": topics,
        "repository_context": repository_context,
        "kind": _str_or_none(body.get("kind")) or authoring.DEFAULT_KIND,
        "status": status, "possible_feats": feats,
        "source": _str_or_none(body.get("source")),
        # carried under a leading underscore so they are unmistakably NOT the
        # engine's own arguments; `_create_document` pops them before the splat.
        "_scope": (scope_kind, scope_id),
        "_continuation": continuation,
    }, None


def parse_create_document_body(body: dict, snapshot=None):
    """`_create_body`, as BOTH surfaces' one validation (FR-020).

    Returns `(parsed, None)` or `(None, message)`. The CLI had no equivalent at
    all, so `--area 'ideation/staging/../../escape/'` — which the HTTP route
    refuses with "area must be a repo-relative ideation directory" — created and
    COMMITTED a document outside `ideation/` on the session branch (found during
    the PR #49 adjudication, adjacent to finding 7's HTTP/CLI divergence family).
    Parity is a requirement, not a nicety: the two surfaces drive the SAME engine
    and must refuse the same inputs, so there is exactly one validator and both
    call it."""
    parsed, err = _create_body(body, snapshot)
    if err is None:
        return parsed, None
    _status, payload = err
    return None, str(payload.get("message") or payload)


def discover_tile_inventory(checkout_root: Path, snapshot=None):
    """The LIVE tile inventory FR-026's two scans are checked against.

    `branch_session` deliberately does no I/O — it takes the inventory as a
    declaration — so the discovery lives here, at the route layer that already
    holds the checkout and (sometimes) the served snapshot.

    Staged-topic ids come from the STAGING FOLDERS, which is the same source the
    generator projects `staged_topics[].staging_id` from and the id the branch is
    derived from (FR-002).

    Cluster and possible ids used to come from the served SNAPSHOT and from
    nowhere else, so the inventory's completeness depended on whether the caller
    happened to hold one — and every CLI session verb passed None (PR #49 review
    finding 7). The same checkout therefore yielded TWO DIFFERENT TILE UNIVERSES,
    and the narrower one silently disabled BOTH of G12's exclusions rather than
    refusing: reproduced, a gate write on tile `cl-foo` resolved onto tile
    `cl-foo-2`'s LIVE session branch (so one tile's documents and records
    committed onto another tile's session), and `assert_branch_cleanup_permitted`
    admitted `git branch -D cluster/cl-foo-2` on behalf of tile `cl-foo`. Both are
    refused on the HTTP inventory. FR-020's parity promise, broken in the
    destructive direction, with no realization note sanctioning the narrowing.

    So the ids are DERIVED from the checkout now — `generator.live_tile_scopes`,
    the same projection `generate_snapshot` uses, kept in the generator because it
    is the sole component that scans the repository — and a snapshot, when one is
    passed, is UNIONED in rather than replacing them. Union is the monotone
    direction: a stale snapshot naming a tile the corpus no longer has produces
    one more EXCLUSION, never one fewer, and neither surface can end up seeing
    less than the other."""
    root = Path(checkout_root)
    staging = root / "ideation" / "staging"
    topics = sorted(p.name for p in staging.iterdir() if p.is_dir()) \
        if staging.is_dir() else []
    clusters, possibles = generator.live_tile_scopes(root, repository=root.name)
    if isinstance(snapshot, dict):
        clusters = tuple(clusters) + tuple(
            str(c.get("id")) for c in (snapshot.get("clusters") or [])
            if isinstance(c, dict) and c.get("id"))
        possibles = tuple(possibles) + tuple(
            str(p.get("id")) for p in (snapshot.get("possibles") or [])
            if isinstance(p, dict) and p.get("id"))
    return branch_session.TileInventory.from_scopes(
        staged_topics=topics, clusters=sorted(set(clusters)),
        possibles=sorted(set(possibles)))


def resolve_session(body_scope, *, checkout_root: Path, registry,
                    repository: str | None, records_dir: str,
                    tile_inventory=None, verb: str | None = None,
                    git=None, require_live: bool = False,
                    remedy: str | None = None,
                    continuation: str | None = None,
                    notebook=None):
    """Resolve the branch session a gate write belongs to, or ``(None, None)``.

    This is the EXPLICIT resolution research R1 said the gate layer owes: the
    route is handed the SERVED checkout root, so the session must be derived from
    the tile's scope identity rather than assumed from the active registry entry.

    Returns ``(session, git)``. ``(None, None)`` — the pre-session path — when the
    body carries no scope, or when the caller declared no session registry and
    therefore no place liveness could live (FR-008). Every refusal on the way is
    raised, never swallowed: a cross-tile collision (G12), a live proposal
    (FR-024), a surviving abandoned branch (FR-025), stale residue (FR-008), or an
    externally-dispatching verb (FR-007).

    ``require_live`` is what a SESSION-ONLY verb passes: the tile's session is
    JOINED or the call raises `NoActiveSession`, and nothing is opened on its
    behalf (FR-016). ``remedy`` is the verb's own next-step sentence carried into
    that refusal — `edit-document` names `edit-apply`, because a human whose edit
    was refused needs the main-resident route, not just a failure.

    ``continuation`` is the human's answer to the FR-025 resume-or-new report
    (`resume` / `new`), carried from the body or the CLI flag. Absent — the normal
    case — a surviving abandoned branch REPORTS the choice instead of resolving it,
    which is the whole requirement (T056).

    ``notebook`` is the INJECTED notebook adapter (T074): an OPEN creates the
    session's `xf-session-*` notebook from the worktree, a JOIN creates nothing,
    and a create that cannot happen leaves the session open with an honest notice
    (FR-036, FR-042). A plane that declares none opens sessions without
    notebooks — which is a complete session, not a degraded one."""
    scope_kind, scope_id = body_scope or (None, None)
    if not scope_kind or not scope_id or registry is None:
        return None, None
    from .session_git import SessionGit

    root = Path(checkout_root)
    git = git or SessionGit(root)
    tile = branch_session.Tile(scope_kind, scope_id)
    session = branch_session.open_session(
        git, registry, repository=repository or "", tile=tile,
        inventory=tile_inventory, verb=verb, checkout_root=root,
        # FR-024, both halves (T055): the LANDED proposal comes from the register's
        # pick edge joined to the change status, the IN-FLIGHT one from the
        # dispatched `propose` jobs in the served checkout's records tree.
        proposal=branch_session.proposal_state_for(
            tile, records_root=root / records_dir, checkout_root=root),
        require_live=require_live, remedy=remedy, continuation=continuation,
        notebook=notebook)
    return session, git


def _refuse_blank_actor(verb: str, actor):
    """FR-019's actor clause, checked BEFORE any session is resolved.

    `HumanGate` refuses a blank or whitespace actor with a `ValueError`, and on
    this route the gate is constructed AFTER `resolve_session` — so a whitespace
    actor opened a branch, a worktree, a live registry entry and a snapshot and
    THEN died as an uncaught 500, leaving a phantom live session behind (PR #49
    review finding 3, the HTTP twin of the CLI traceback). Asked here, the answer
    costs nothing and persists nothing."""
    if actor is not None and str(actor).strip():
        return None
    return _refused(
        f"{verb} refused: a gate action requires an identified human actor — a "
        "blank one is structurally invalid (FR-019). Nothing was resolved and "
        "nothing was opened.", status=403)


def _create_document(body: dict, root: Path, actor: str, records_dir: str,
                     snapshot_path, *, session_registry=None,
                     repository: str | None = None,
                     tile_inventory=None,
                     session_notebook=None,
                     provenance=None) -> tuple[int, dict]:
    blank = _refuse_blank_actor("create-document", actor)
    if blank:
        return blank
    snapshot = _load_snapshot(snapshot_path)
    parsed, err = _create_body(body, snapshot)
    if err:
        return err
    scope = parsed.pop("_scope", (None, None))
    continuation = parsed.pop("_continuation", None)
    try:
        if tile_inventory is None and all(scope) and session_registry is not None:
            # discovered only when a session is actually being resolved, so a
            # scope-less create touches the filesystem exactly as it did before
            tile_inventory = discover_tile_inventory(root, snapshot)
        session, git = resolve_session(
            scope, checkout_root=root, registry=session_registry,
            repository=repository, records_dir=records_dir,
            tile_inventory=tile_inventory, verb="create-document",
            continuation=continuation,
            # create-document is the ONE verb that can OPEN a session, so it is
            # the one that carries the notebook adapter (T074, FR-036); the
            # session-only verbs JOIN, and a join creates no notebook
            notebook=session_notebook)
    except branch_session.SessionRefused as exc:
        # Every session refusal is a 409 carrying the engine's own reason: the
        # human is being told a precondition is unmet, which is the same shape as
        # every other gate refusal (`_refused`), and nothing was persisted.
        return _refused(exc.report())
    except session_git_mod.GitError as exc:
        return _refused(f"the session could not be opened: {exc}")
    except OSError as exc:                   # unreadable staging tree / container
        return _refused(f"the session could not be opened: {exc}")
    # In a session the gate is rooted at the WORKTREE, so the document AND the
    # gate-action record land there and are committed together (plan Constraint
    # 10). Outside one, root and behaviour are exactly what they were.
    gate_root = session.worktree if session is not None else root
    gate = HumanGate(gate_root, [records_dir], human_actor=actor)
    # THE OPEN IS INSIDE THE CREATE'S FAILURE DOMAIN from here (PR #49 review
    # finding 3): every refusal below arrives AFTER `resolve_session` may have
    # brought a branch, a worktree, a live registry entry and a snapshot into
    # existence, and each one used to return "nothing was persisted" over a
    # phantom live session. `_unwound` ends a session this call OPENED and leaves
    # a JOINED one untouched.
    try:
        result = execute_create_document(gate, records_dir=records_dir,
                                         session=session, git=git,
                                         provenance=provenance, **parsed)
    except BoundaryViolation as exc:
        # An EXISTING target is the engine's create-only refusal (SOURCE_EDIT):
        # a 409 conflict carrying the boundary's own report, with the existing
        # document byte-identical. Any other boundary refusal (the agent path,
        # an escape attempt) is a 403. UNCHANGED inside a session: the create
        # stays create-only there too (FR-018).
        status = 409 if exc.refusal.kind == SOURCE_EDIT else 403
        return _unwound(session, git, root, exc.refusal.report(), status=status)
    except gate_console.GateRefused as exc:
        return _unwound(session, git, root, str(exc))
    except branch_session.SessionRefused as exc:   # a split write, an escape
        return _unwound(session, git, root, exc.report())
    except session_git_mod.SessionGitRefused as exc:
        # a STRUCTURAL git refusal — a stage-everything spelling, a path escaping
        # the worktree, the served-checkout guard. A 409 carrying the module's own
        # reason, not a traceback (it reached the handler as a 500 before).
        return _unwound(session, git, root, str(exc))
    except session_git_mod.GitError as exc:        # git itself refused the write
        return _unwound(session, git, root, f"the session commit failed: {exc}")
    except OSError as exc:                   # unwritable area, bad path
        return _unwound(session, git, root,
                        f"the create could not be written: {exc}")
    return 200, result


def _unwound(session, git, root: Path, message: str, *, status: int = 409):
    """Refuse, having first undone a session THIS call opened (finding 3).

    The refusal text is the engine's own, with any residue the unwind could not
    remove appended — a human told "nothing was persisted" over a surviving
    worktree is worse off than one told exactly what is still there."""
    notes = ()
    if session is not None and git is not None:
        notes = branch_session.unwind_opened_session(git, session,
                                                     checkout_root=root)
    if notes:
        message = message + "\n\n" + "\n".join(notes)
    return _refused(message, status=status)


# ==========================================================================
# EDIT-DOCUMENT — the SESSION-ONLY rewrite (007-workbench-branch-sessions T042;
# FR-015, FR-016, FR-017)
#
# The one verb in this codebase that changes a document which already exists.
# Research R5 found there was no engine to reuse: `authoring.py` has no exec
# path, and `boundary.create_document` refuses an existing target as
# `SOURCE_EDIT` on purpose. Phase 3 (T026) answered that with a NARROW,
# construction-time allowance — `boundary.rewrite_session_document`, available
# only to a gate constructed with `session_root=<the worktree>` — so the
# create-only rule over the corpus is untouched and the ground the rewrite
# happens on is what changed: an UNMERGED branch, one pull request away from a
# reviewer.
#
# Consequences, all deliberate:
#
#   * NO redline artifact is required or produced (FR-017). `edit-apply`'s
#     redline is the ceremony that makes a MAIN-RESIDENT source edit reviewable;
#     on a session branch the pull request is that ceremony (D18). `edit-apply`
#     itself is untouched — two verbs, never one renamed.
#   * SESSION-ONLY, and the refusal names `edit-apply` rather than merely
#     failing: with no live session there is nothing to edit here, and the human
#     is trying to do something the other verb does.
#   * NO creation and NO deletion by any path (FR-015): an absent target refuses
#     (creation stays `create-document`), and a blank/absent replacement is
#     refused as a delete in disguise — both in the boundary, so neither can be
#     bypassed by a caller that skips this route.
# ==========================================================================


def _refuse_record_stamp_collision(root: Path, *, action: str, target_id: str,
                                   at: str, records_dir: str,
                                   subject: str, consequence: str) -> None:
    """Refuse a second record for the SAME action and target within the same
    SECOND, before anything is written.

    A gate-action record's filename carries its stamp at second resolution, so two
    records of one action on one target collide and the second OVERWRITES the first
    — destroying an audit entry. The verbs of this feature are the first that can
    do it (`edit-document` on one document, and the ref-keyed main-resident
    `abandon-session` / `open-pr` on one branch), so the check lives at the route,
    ahead of the action, where a refusal still persists nothing.

    It is false-NEGATIVE-only by design: it derives the prospective path the same
    way the write will, but a caller that reaches the write by another route is
    still caught by whatever guard sits downstream."""
    prospective = gate_console.gate_action_record_relpath(
        records_dir, action, target_id, at)
    if (Path(root) / prospective).exists():
        raise branch_session.SessionRefused(
            f"a gate-action record for {subject} already carries this action's "
            f"stamp ({branch_session.action_stamp(at)}): a second "
            f"{action} within the same second would overwrite that record"
            f"{consequence}. Nothing was written — retry.")


def _refuse_stamp_collision(root: Path, document: str, *, records_dir: str,
                            at: str) -> None:
    """Refuse a SECOND edit of the same document within the same SECOND, BEFORE
    anything is written (FR-006, FR-016).

    A gate-action record's filename carries its action stamp at second
    resolution, and `edit-document` is the first verb that can emit two records
    for the SAME target id: a re-submitted save (a double-clicked button) would
    overwrite the first record in place, and its commit would then no longer be
    the one that INTRODUCED that record file — which the commit path detects,
    but only AFTER the commit has landed, leaving a refusal behind a real commit.
    Checked here, ahead of the rewrite, so the refusal persists nothing at all
    and says what actually happened. The check is a false-NEGATIVE-only
    approximation (it slugs the requested path, not the boundary-resolved one):
    when it misses, the downstream introduced-by guard still fires."""
    _refuse_record_stamp_collision(
        root, action=gate_console.ACTION_EDIT_DOCUMENT,
        target_id=gate_console.document_target_id(document), at=at,
        records_dir=records_dir, subject=repr(document),
        consequence=", and its commit would no longer be the one that introduced "
                    "it (FR-006)")


def _rewritten_and_not_committed(exc: "branch_session.SessionRefused", *,
                                 root: Path, rel: str
                                 ) -> "branch_session.SessionRefused":
    """Say that the REPLACEMENT BYTES ARE ALREADY ON DISK (PR #49 review finding
    1's residual, wave 2).

    `rewrite_session_document` runs BEFORE `commit_gate_action` claims the action
    lock, so every refusal raised from inside the transaction — a rival writer
    holding the lock, a foreign path in the index, a post-stage set that is not the
    declared one — is returned over a worktree whose document is no longer
    byte-identical to the committed one. Nothing is staged, nothing is recorded and
    nothing is committed (the transaction unwinds itself), but the bytes stay.

    THAT IS DELIBERATE and it is not changed here: a TRACKED document's bytes are
    never reverted by a refusal, because the human's replacement is the only copy
    of what they just typed and git already holds the committed version
    (`test_session_transaction.py::test_a_tracked_document_is_left_exactly_as_the
    _action_found_it`). What was wrong is that the refusal did not SAY so, and the leftover
    then trips the merge ending's uncommitted-work refusal
    (`_refuse_reconciling_over_uncommitted_work`) with the human never told why
    their worktree is dirty. Widening the lock to cover the rewrite is the other
    direction and was rejected: the boundary owns the write, the engine owns the
    transaction, and one lock spanning both would put a file write inside a git
    transaction that must be able to unwind without it.

    The engine's own reason is kept VERBATIM as the first sentence — the mapping a
    caller reads (409 carrying the engine's refusal) is unchanged."""
    return branch_session.SessionRefused(
        f"{exc.report()} — and note that {rel!r} in the session worktree ALREADY "
        f"CARRIES YOUR REPLACEMENT: the rewrite happens before this action claims "
        f"the worktree's index, so the bytes are on disk while nothing was staged, "
        f"recorded or committed. Retry the action to commit them, or restore the "
        f"committed bytes with `git -C {root} checkout -- {rel}`. Until one of "
        f"those happens the session worktree is DIRTY, and a merge ending refuses "
        f"to reconcile over uncommitted work (FR-033)")


# --------------------------------------------------------------------------
# WHOSE MATERIAL IS THIS? — the ownership boundary on a session rewrite
# (T092 real-corpus acceptance sweep, defect 1)
# --------------------------------------------------------------------------
#
# The sweep drove `edit-document` from a staged tile's workbench and REPLACED
# ANOTHER TOPIC'S 1,460-word staged document with a five-line probe, twice, on
# two independent tiles — committed onto this tile's session branch with a
# gate-action record filed under the foreign document's target id, so the audit
# trail presented the overwrite as authorised. No refusal, no warning, no 4xx.
#
# The paths reached the route from the workbench's rewrite picker, which offered
# every resolved path in the tile's scope — including the CLUSTER NEIGHBOURHOOD
# and inherited sections the same panel labels "inferred via clusters, not the
# topic's own material". The picker is fixed too (staging-workbench-model.js
# `rewritableDocuments`), but the picker is UI: this is the boundary, and it is
# where the rule has to hold for the CLI parity verb, for a hand-shaped body, and
# for the next surface nobody has written yet.
#
# WHAT THE BOUNDARY ALREADY ENFORCED, and why it was not enough: the gate's
# construction-time rewrite allowance confines the target to the session
# WORKTREE. Every foreign document above passed that check — the worktree is a
# whole checkout of the corpus, so worktree containment is not topic ownership,
# and the route's own comment conflated the two.

def tile_owned_prefix(tile) -> str | None:
    """The repo-relative directory holding a tile's OWN material, or None for a
    tile that has no folder of its own.

    A STAGED-TOPIC tile owns its staging folder — the section the workbench calls
    "the topic's own material" and the same folder `discover_tile_inventory`
    derives the tile's id from. A CLUSTER or POSSIBLE tile owns no folder at all:
    a cluster's member documents and a possible's cited evidence live all over the
    corpus and belong to whoever authored them, which is exactly the conflation
    defect 1 exploited. Those tiles' sessions can still rewrite what they CREATE
    (below) — they simply inherit nothing."""
    kind = getattr(tile, "scope_kind", None)
    scope_id = str(getattr(tile, "scope_id", "") or "").strip()
    if kind == branch_session.STAGED_TOPIC and scope_id:
        return f"ideation/staging/{scope_id}/"
    return None


def repo_relative_document(root: Path | str, document: str) -> str | None:
    """`document` as a slash-spelled path relative to `root`, or None when it is
    not under `root` at all.

    PURE lexical normalization on a resolved path — it answers WHERE the target
    is, never whether the write is allowed. A path that escapes (or that cannot
    be resolved) returns None and is left to the boundary, whose `outside-root`
    refusal is the one that owns that answer and already reports it."""
    try:
        base = Path(root).resolve()
        candidate = Path(document)
        resolved = (candidate if candidate.is_absolute() else base / candidate).resolve()
        return resolved.relative_to(base).as_posix()
    except (OSError, ValueError):
        return None


def foreign_document_refusal(document: str, *, tile, worktree: Path | str,
                             checkout_root: Path | str | None) -> str | None:
    """Why this tile's session may NOT rewrite `document`, or None when it may.

    A session may rewrite exactly two things:

      * the tile's OWN material — the staging folder a staged-topic tile is named
        after (`tile_owned_prefix`); and
      * a document THIS SESSION brought into existence — a path the session
        worktree has and the SERVED CHECKOUT does not. The served checkout is the
        branch's base, never moved by any session operation (FR-004), so a path
        absent there and present here was introduced on this branch.

    Everything else — another topic's staged document, an `ideation/brainstorm/`
    capture, a cluster-neighbourhood or inherited row, an inbound document that
    merely DECLARES this topic as a destination — is READ-ONLY CONTEXT in the
    workbench and is refused here.

    `checkout_root=None` (a hand-built caller that names no base) is FAIL-CLOSED:
    the created-in-this-session allowance cannot be evaluated without a base, so
    only the tile's own material passes."""
    rel = repo_relative_document(worktree, document)
    if rel is None:
        return None                      # not under the worktree: the boundary's answer
    prefix = tile_owned_prefix(tile)
    if prefix and (rel == prefix.rstrip("/") or rel.startswith(prefix)):
        return None
    if checkout_root is not None:
        try:
            if not (Path(checkout_root) / rel).exists():
                return None              # this session created it
        except OSError:                  # an unreadable base is not a licence
            pass
    kind = str(getattr(tile, "scope_kind", "") or "?")
    scope_id = str(getattr(tile, "scope_id", "") or "?")
    own = (f"documents under {prefix} (the topic's own material)" if prefix
           else "no folder of its own — a cluster/possible tile inherits none")
    return (
        f"refusing to rewrite {rel!r}: it is NOT this tile's own material. The "
        f"session is open on tile {kind} {scope_id}, which owns {own}, plus any "
        f"document this session created. {rel!r} already exists in the served "
        f"checkout outside that material, so rewriting it here would commit "
        f"ANOTHER topic's document onto this tile's branch under a gate-action "
        f"record naming this session — an overwrite that reads as authorised and "
        f"is not (T092 sweep defect 1). The workbench shows inherited, "
        f"cluster-neighbourhood and inbound documents as READ-ONLY CONTEXT for "
        f"exactly this reason. Nothing was written. To edit that document, open "
        f"the workbench on ITS tile, or use `edit-apply`, the main-resident "
        f"redline path (FR-017)")


def execute_edit_document(gate, *, document: str, content, records_dir: str,
                          session, git, notes: str | None = None,
                          at: str | None = None, provenance=None,
                          checkout_root: Path | str | None = None) -> dict:
    """Rewrite ONE existing document inside the session worktree and commit it
    with its gate-action record as this action's single commit (FR-015, FR-006).

    Human-only: an `OutputBoundary` / agent path is rejected (BoundaryViolation)
    and REPORTED before the rewrite is attempted. `session` is mandatory — this
    verb has no main-resident form at all — and `git` is the seam that commits it,
    the same one `create-document` uses in a session, which is what gives this
    verb FR-010's regeneration for free.

    The rewrite goes through `HumanGate.rewrite_session_document`, so all four
    structural conditions are the BOUNDARY's and not this route's: a declared
    session worktree, confinement inside it, an existing target, and a non-blank
    replacement. Returns the response body the route and the CLI both report
    from; the commit sha is RETURNED, never written into the record.

    `checkout_root` is the SERVED checkout — the branch's base — and it is what
    makes the FIFTH condition answerable: the target is the tile's OWN material
    (`foreign_document_refusal`, T092 defect 1). It lives here rather than in
    either caller so the HTTP route and the CLI parity verb cannot diverge on it
    (FR-020); a caller that names no base gets the fail-closed reading."""
    human = gate_console.require_human_gate(gate)   # agent path -> BoundaryViolation
    root = human.output.root
    at = at or gate_console._utcnow()
    if session is None:
        raise branch_session.SessionRefused(
            "`edit-document` is valid ONLY inside an active branch session: it "
            "rewrites a document in the session WORKTREE and commits it on the "
            "session branch. Editing a document that lives on `main` stays "
            "`edit-apply`, the main-resident redline path (FR-015, FR-017)")
    if git is None:
        raise branch_session.SessionRefused(
            "a session rewrite needs the git seam that commits it; a session "
            "write is never left uncommitted (FR-006)")
    if Path(session.worktree).resolve() != Path(root).resolve() \
            or human.session_root is None \
            or Path(human.session_root).resolve() != Path(root).resolve():
        raise branch_session.SessionRefused(
            f"the gate is rooted at {root} (declared session worktree "
            f"{human.session_root}) but the session's worktree is "
            f"{session.worktree}: a session rewrite is written through a gate "
            "rooted at the WORKTREE and DECLARING it, so the rewrite allowance "
            "and the record's residence are the same tree (FR-015, T026)")
    # OWNERSHIP, before anything is read for a stamp and long before anything is
    # written (T092 defect 1): worktree containment is not topic ownership, and
    # the difference is another topic's committed document.
    foreign = foreign_document_refusal(document, tile=session.tile, worktree=root,
                                       checkout_root=checkout_root)
    if foreign is not None:
        raise branch_session.SessionRefused(foreign)
    _refuse_stamp_collision(root, document, records_dir=records_dir, at=at)
    target = human.rewrite_session_document(document, content)
    rel = str(target.relative_to(root))
    if rel not in set(git.dirty_paths(root)):
        # A byte-identical replacement. The split-write guard downstream would
        # report it as an already-committed document — true, and useless: there is
        # no commit for this action to ride, so it is refused in its own words and
        # nothing is persisted (the bytes on disk are the ones already committed).
        raise branch_session.SessionRefused(
            f"refusing {rel!r}: the replacement is byte-identical to the document "
            "already committed in the session worktree, so this action has no "
            "commit to ride and nothing to record (FR-006)")
    record = gate_console.build_gate_action_record(
        actor=human.human_actor, action=gate_console.ACTION_EDIT_DOCUMENT,
        at=at, document=rel, notes=notes,
        # the GATEWAY fact the caller observed (D23): `http` from the console
        # handler that already ran the token check, `cli` from the parity verb that
        # already ran the tty / declaration check. Never derived here.
        provenance=provenance,
        # ONE artifact: the commit, referenced by this action's own stamp. No
        # redline is required and none is produced (FR-017, data-model T014).
        artifacts=[branch_session.commit_artifact(branch_session.action_stamp(at))],
        # inside a session the route ALWAYS names the branch: a session record
        # that does not name its branch audits nothing (D13)
        ref=session.branch)
    try:
        commit = branch_session.commit_gate_action(
            human, git, worktree=root, branch=session.branch, record=record,
            documents=[rel], records_dir=records_dir,
            summary=f"edit-document: {rel}",
            # the session carries the registry its snapshot is keyed in, so this
            # action regenerates the session's projection as part of itself (FR-010)
            session=session)
    except branch_session.SessionRefused as exc:
        raise _rewritten_and_not_committed(exc, root=root, rel=rel) from exc
    return {
        "ok": True,
        "verb": "edit-document",
        "ref": session.branch,
        "commit": commit.sha,
        "document": rel,
        "record": commit.record_relpath,
        "hint": "rewritten on the session branch as ONE commit carrying the "
                "document and its gate-action record — no redline artifact is "
                "required here; the pull request is the review (`open-pr`)",
    }


# --------------------------------------------------------------------------
# THE FIRST SAVE — doxBench's governed write, through the SAME gate
# (T075; FR-031, FR-032, FR-034, FR-036)
# --------------------------------------------------------------------------
#
# doxBench's first-edit is an ORCHESTRATION entrypoint,
    # not new write authority: the persisted action remains
    # create-document/edit-document. An eligible first Save of a
# changed buffer is exactly one of the two EXISTING document actions — the
# create action for a path nothing has made yet, the edit action for one that
# exists — performed inside the tile's own branch session, with the difference
# that the session may not exist yet: the transaction creates it or joins it
# atomically and unwinds itself on any failure
# (`branch_session.commit_first_edit`, FR-032/FR-033).
#
# WHAT THIS EXPOSURE OWNS, and nothing else:
#
#   1. THE GATE. The write and its record go through a `HumanGate` rooted at
#      the SESSION WORKTREE and DECLARING it — the identical construction
#      `_edit_document` performs below — handed to the transaction as a
#      FACTORY, because the worktree only exists once the transaction has
#      opened or joined the session. Building the gate here rather than inside
#      `branch_session` keeps that module free of gate construction and keeps
#      the HTTP route, the CLI parity verb, and this Save on one shape.
#   2. THE OWNERSHIP INPUT. `tile_owned_prefix` stays the SINGLE source of
#      which folder a tile owns; it is INJECTED as `owned_prefix` so the
#      transaction answers FR-036 from the same rule
#      `foreign_document_refusal` answers `edit-document` from. This exposure
#      adds no ownership test of its own — a second copy of that rule is how
#      the two drift apart, which is the defect the rule exists to close.
#
# WHAT IT DELIBERATELY DOES NOT OWN: any refusal. Eligibility, the
# new-versus-existing action choice, base revalidation, the empty-Save
# (delete-shaped) refusal and every rollback are the TRANSACTION's, asserted at
# its own surface; the boundary's four structural conditions are the GATE's.
# Route-level enforcement of ownership, current full identity, and action choice
# is a later task and is not performed here. This function is a seam, and a seam
# that grew its own opinions would be a second boundary.
#
# THE LOCK IS THE TRANSACTION'S. `commit_first_edit` claims the
# per-worktree action lock itself, and that lock is NOT reentrant — so nothing
# here may claim it around the call.

# ===========================================================================
# SHARE-SESSION (add-doxbench-editing-phase-b tasks.md §12, contract-v1.36)
#
# The verb that hands a live workbench session to a colleague, and the reason
# threads are LOCAL until a human says otherwise. It is defined by what it is
# STRICTLY LESS THAN: `open-pr` pushes the branch AND opens a pull request into
# the Merge-Master ritual; share-session pushes the branch and stops. Same port,
# same credential rule, same console posture — one member instead of three.
#
# The whole verb is three steps: commit the session's DIRTY thread sidecars,
# push the branch, return and record the pushed ref.
# ===========================================================================

SHARE_SESSION_REMEDY = (
    "share-session publishes an ACTIVE branch session; open the tile and Save "
    "once to start one, then share it.")

# The port members this verb is FORBIDDEN to reach. Written down as DATA, not
# left as an absence, because "opens no pull request, requests no review, holds
# no approval or merge authority" is only checkable against a list somebody
# committed to — `session_pr.PORT_OPERATIONS` minus `push` is exactly it, and
# deriving it that way means a port that grows a fourth member fails this
# assertion instead of quietly widening the verb.
FORBIDDEN_SHARE_OPERATIONS: tuple[str, ...] = tuple(
    op for op in session_pr.PORT_OPERATIONS if op != "push")

# Sharing is NOT promotion (task 9.4). The verb pushes a branch; it promotes no
# finding, and the thread prefix stays excluded from session-PR promotion by
# default. Read from the threads module rather than restated, so the exclusion
# has ONE spelling on this surface too.
SHARE_IS_NOT_PROMOTION = (
    "shared, not promoted: this verb pushes the session branch and promotes "
    "nothing. Threads stay excluded from session pull-request promotion by "
    "default (" + ", ".join(doxbench_threads.promotion_excluded_prefixes())
    + "), and a finding becomes durable only by someone creating a new object "
    "through an existing lifecycle verb, with provenance.")


@dataclasses.dataclass(frozen=True)
class SharePlan:
    """What one share invocation has to do, decided by a SIDE-EFFECT-FREE read.

    Computed before the port is touched so the "nothing new" answer costs no
    remote write, and so the record's residency (below) is known before a gate
    is built at either root."""

    branch: str
    threads: tuple[str, ...]
    local_sha: str | None
    remote_sha: str | None

    @property
    def commits(self) -> bool:
        """Whether this share has sidecars to commit — which is also what
        decides where its record lives."""
        return bool(self.threads)

    @property
    def unpushed(self) -> bool:
        """Whether the branch holds commits the remote has not seen. This is the
        ORDINARY state after a run of Saves, not an edge case: nothing pushes
        implicitly, so every Save leaves a commit here."""
        return bool(self.local_sha) and self.local_sha != self.remote_sha

    @property
    def nothing_new(self) -> bool:
        return not self.commits and not self.unpushed

    def report(self) -> str:
        """The HONEST nothing-new sentence (task 12.3). It names both things it
        checked, because "nothing to share" with no reason reads as a failure."""
        return (
            f"nothing new to share: {self.branch!r} has no uncommitted thread "
            f"sidecars, and the remote already holds this branch at "
            f"{(self.remote_sha or '')[:12]}. Nothing was pushed.")


def plan_share(git, *, worktree, branch: str) -> SharePlan:
    """Read what a share WOULD do. No commit, no push, no remote write.

    `remote_sha` uses `git ls-remote`, which is side-effect-free and never
    fetches — the same read the merge observation already trusts."""

    dirty = git.dirty_paths(worktree)
    return SharePlan(
        branch=branch,
        threads=doxbench_threads.shareable_thread_paths(dirty),
        local_sha=git.head(worktree) or None,
        remote_sha=git.remote_sha(branch))


def share_session_gate_factory(actor: str, records_dir: str):
    """The gate builder for a share, at whichever root the plan needs.

    DELIBERATELY NARROWER THAN `first_edit_gate_factory`: the records tree and
    NOTHING else. That factory grants the thread-sidecar prefix because a Save
    WRITES a sidecar through its gate; a share never writes one. It commits
    sidecars that are already on disk, staged by explicit path through git, and
    the only thing it writes through the gate is its own record. Granting the
    thread prefix here would widen the allowlist for a write that does not
    exist, so it is not granted, and a companion test asserts the difference."""

    def build(root):
        return HumanGate(root, [records_dir], human_actor=actor,
                         session_root=root)
    return build


def execute_share_session(gate_factory, git, *, session, pull_requests,
                          records_dir: str, checkout_root: Path | str,
                          notes: str | None = None, at: str | None = None,
                          provenance=None) -> dict:
    """Commit the session's dirty threads, push the branch, record the share.

    Human-only: the agent path is rejected (BoundaryViolation) BEFORE the plan
    is read and long before anything is pushed, exactly as `execute_open_pr`
    rejects it before the port is touched.

    TWO RECORD RESIDENCIES, and the reason is structural rather than a taste
    call — the contract-v1.36 entry states the same thing schema-side:

      * WITH dirty sidecars, the record rides their commit onto the session
        branch (`commit_gate_action`, untouched), so one gate action is one
        commit and the record travels to the colleague who fetches the branch.
      * WITH nothing dirty and commits the remote has not seen, there is
        nothing to co-commit, and FR-006's own guard REFUSES an empty declared
        set. So the record is main-resident, exactly as `open-pr`'s is.

    The ordering differs with it, and the difference is reported rather than
    hidden: the branch-resident record is written INSIDE the commit and so
    precedes the push, while the main-resident one is written after it. A push
    that fails after a thread commit therefore leaves a recorded commit and an
    unshared branch — which the next invocation sees as `unpushed` and pushes,
    honestly, rather than reporting nothing to do."""

    # FIRST, before the plan and before the port: a gate at the SERVED checkout,
    # which is where a main-resident record would land and where the agent-path
    # refusal is identical either way.
    main_gate = gate_factory(Path(checkout_root))
    human = gate_console.require_human_gate(main_gate)
    root = Path(human.output.root)
    at = at or gate_console._utcnow()
    if session is None:
        raise branch_session.SessionRefused(
            "`share-session` publishes an ACTIVE branch session; there is none "
            "on this tile. " + SHARE_SESSION_REMEDY)
    if Path(checkout_root).resolve() != root.resolve():
        raise branch_session.SessionRefused(
            f"the gate is rooted at {root} but the served checkout is "
            f"{checkout_root}: a share's main-resident record is written into "
            "the SERVED checkout's gate-records tree")
    if pull_requests is None:
        raise branch_session.SessionRefused(
            "no pull-request port is declared on this plane, so `share-session` "
            "has no identity to push with. The remote write uses the INVOKING "
            "ENGINEER's own `gh` authentication (FR-034) — the same plane rule "
            "the session Save already carries, and the reason a hosted plane "
            "never holds one")

    worktree = Path(session.worktree)
    plan = plan_share(git, worktree=worktree, branch=session.branch)

    # TASK 12.3, decided BEFORE the port: nothing new is reported, never pushed
    # again. Costs one local status read and one `ls-remote`, and no write.
    if plan.nothing_new:
        return {"ok": True, "shared": False, "branch": plan.branch,
                "pushed_ref": None, "revision": plan.local_sha,
                "threads": [], "reason": plan.report(),
                "promotion": SHARE_IS_NOT_PROMOTION}

    commit = None
    if plan.commits:
        # THE P3-17 DISCHARGE. These sidecars belong to documents that were
        # DISCUSSED and, in the tail case that obligation named, never Saved
        # again — so no Save will ever carry them and they would not travel.
        # They ride the SHARE's own commit instead, which is the first verb with
        # a legitimate reason to commit a thread on its own.
        record = gate_console.build_gate_action_record(
            actor=human.human_actor, action=gate_console.ACTION_SHARE_SESSION,
            at=at, ref=plan.branch, notes=notes, provenance=provenance,
            artifacts=[branch_session.commit_artifact(
                branch_session.action_stamp(at))])
        commit = branch_session.commit_gate_action(
            gate_factory(worktree), git, worktree=worktree,
            branch=plan.branch, record=record, documents=plan.threads,
            records_dir=records_dir,
            summary=f"share-session: {len(plan.threads)} thread(s)",
            session=session)

    # THE ONLY REMOTE WRITE, and the port's EXISTING member. Everything above is
    # local; everything the colleague can see happens here.
    pull_requests.push(plan.branch)
    pushed_ref = f"refs/heads/{plan.branch}"
    revision = git.head(worktree) or plan.local_sha

    if commit is None:
        # Main-resident, and written AFTER the push, exactly as `open-pr`'s is:
        # the record attests to a share that has already happened.
        record = gate_console.build_gate_action_record(
            actor=human.human_actor, action=gate_console.ACTION_SHARE_SESSION,
            at=at, ref=plan.branch, notes=notes, provenance=provenance,
            artifacts=[{"kind": gate_console.ART_OTHER,
                        "reference": pushed_ref}])
        record_path = gate_console.write_gate_action_record(
            human, records_dir, record)
        # Relative to the SERVED checkout, the root a main-resident record is
        # read back from — `open-pr`'s response says the same thing the same way.
        record_rel = str(Path(record_path).relative_to(root))
    else:
        # Relative to the WORKTREE, because that is where it rode its commit.
        record_rel = commit.record_relpath

    return {"ok": True, "shared": True, "branch": plan.branch,
            "pushed_ref": pushed_ref, "revision": revision,
            "threads": list(plan.threads),
            "record": record_rel,
            "record_resident": "branch" if commit is not None else "main",
            "promotion": SHARE_IS_NOT_PROMOTION}


def first_edit_gate_factory(actor: str, records_dir: str):
    """The worktree-rooted gate builder `commit_first_edit` writes through.

    Called with the session worktree ONLY once the transaction has opened or
    joined the session, so the gate's root, its declared session root, and the
    tree the record lands in are the same directory by construction (FR-015).

    TWO declared allowances, and no third: the records tree, exactly as
    `_edit_document` grants it, and — since add-doxbench-editing-phase-b (task
    9.5, `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/tasks.md`) — the THREAD
    SIDECAR tree.

    THE WIDENING IS AS NARROW AS THE TASK ALLOWS, and this note is the record of
    why it is this wide and no wider (PR #207 review, F10). The allowance is ONE
    prefix, the threads module's own declared one, granted to ONE gate — the doxBench
    first-edit/Save gate — and to no other gate on this surface; a companion test
    asserts the prefix appears exactly once in this module. It is a PREFIX rather
    than a per-document path because the gate is constructed once per Save and the
    sidecar path is derived per document inside that Save
    (`doxbench_threads.thread_commit_paths`), so a path-exact allowance would have
    to be recomputed by this factory from state it does not hold. What keeps the
    prefix from being a hole is that nothing else can write under it: the module
    exposes exactly one write route (`write_thread`), the path rule refuses an
    absolute, traversal-shaped or already-a-sidecar document, and the boundary
    still resolves every write inside the session worktree. A thread commits WITH the document's Save on
    the one-commit-per-gate-action path (design §4.2), and it is written through
    this same gate's `write_gate_artifact`, so without the prefix DECLARED here
    the boundary refuses it as `outside-allowlist`. The narrow session-rewrite
    allowance is still unlocked by the DECLARATION rather than by a wider path
    list, and nothing else on this surface widens: only this gate gains the
    thread prefix."""
    def build(worktree):
        return HumanGate(worktree,
                         [records_dir, doxbench_threads.THREAD_PREFIX],
                         human_actor=actor, session_root=worktree)
    return build


def execute_first_edit(*, git, session_registry, repository: str, tile,
                       document: str, content, actor: str,
                       checkout_root: Path | str, records_dir: str,
                       base_hash: str | None = None, at: str | None = None,
                       notes: str | None = None, provenance=None,
                       tile_inventory=None,
                       base: str = branch_session.DEFAULT_BASE,
                       notebook=None, summary: str | None = None,
                       continuation: str | None = None,
                       proposal=None) -> dict:
    """Persist ONE changed doxBench buffer as its own existing governance action,
    creating or joining this tile's branch session as part of the same
    transaction (FR-031, FR-032, FR-034).

    Raises what the transaction raises — `branch_session.SessionRefused` for an
    ineligible buffer, a moved base, or a rollback report; `BoundaryViolation`
    for a structural gate refusal — so a caller reports the engine's own reason
    rather than a paraphrase of it. Returns the response body a route or a parity
    verb reports from, shaped like `execute_edit_document`'s and additionally
    naming WHICH existing action ran, the committed content identity, and whether
    this Save opened the session or joined one already open.

    `at` is the caller's observed instant, `provenance` the GATEWAY fact the
    caller already established (D23) — neither is derived here."""
    outcome = branch_session.commit_first_edit(
        git, session_registry, repository=repository, tile=tile,
        document=document, content=content,
        gate_factory=first_edit_gate_factory(actor, records_dir),
        checkout_root=checkout_root,
        # the SINGLE ownership source, injected — never re-decided here
        owned_prefix=tile_owned_prefix(tile),
        base_hash=base_hash, records_dir=records_dir, at=at, notes=notes,
        inventory=tile_inventory, base=base, notebook=notebook,
        provenance=provenance, summary=summary, continuation=continuation,
        proposal=proposal,
        # THREADS COMMIT WITH THE DOCUMENT'S SAVE (add-doxbench-editing-phase-b
        # task 9.2). The RULE is `doxbench_threads`', named here — the one place
        # doxBench's Save is assembled — and applied by the transaction to the
        # NORMALISED document path it settles on, because that is the path the
        # turn's own sidecar was written under. Passing the seam rather than a
        # computed list is what keeps those two paths the same file; computing
        # it here would derive it from the caller's spelling instead.
        thread_paths_for=doxbench_threads.thread_commit_paths)
    return {
        "ok": True,
        "verb": outcome.action,
        "ref": outcome.ref,
        "commit": outcome.revision,
        "document": outcome.document,
        "record": outcome.commit.record_relpath,
        "content_hash": outcome.content_hash,
        "session": "joined" if outcome.joined else "opened",
        "hint": "saved on the session branch as ONE commit carrying the document "
                "and its gate-action record, through the existing "
                f"`{outcome.action}` action — the pull request is still the "
                "review (`open-pr`)",
    }


def _edit_body(body: dict):
    """Parse + validate an edit-document body. Returns (parsed, None) or
    (None, error_tuple).

    The tile scope is REQUIRED here, unlike `create-document`'s optional pair:
    there is no main-resident form of this verb, so a body naming no tile names no
    session and is a shaping error rather than a fallthrough (FR-016).

    An ABSENT or blank `content` is deliberately NOT rejected here — it is the
    DELETE SHAPE, and the contract answers it with a 409 refusal from the
    boundary's own `SOURCE_DELETE` rather than a 400, because the caller shaped a
    request the verb holds no authority for rather than a malformed one."""
    scope_kind = _str_or_none(body.get("scope_kind"))
    scope_id = _str_or_none(body.get("scope_id"))
    if not scope_kind or not scope_id:
        return None, _invalid(
            "edit-document requires the tile scope (scope_kind + scope_id): the "
            "session it rewrites in is resolved from the tile, and this verb has "
            "no main-resident form")
    if scope_kind not in branch_session.SCOPE_KINDS:
        return None, _invalid(
            "scope_kind must be one of "
            f"{', '.join(branch_session.SCOPE_KINDS)}")
    document = _str_or_none(body.get("document"))
    if not document:
        return None, _invalid("edit-document requires the document it rewrites "
                              "(a path inside the session worktree)")
    content = body.get("content")
    if content is not None and not isinstance(content, str):
        return None, _invalid("content is the document's full replacement TEXT")
    return {"document": document, "content": content,
            "notes": _str_or_none(body.get("notes")),
            "_scope": (scope_kind, scope_id)}, None


# The `edit-document` refusal the human reads when no session is live. It names
# the main-resident route, because that is what they were reaching for.
EDIT_REMEDY = ("Editing a document that lives on `main` stays `edit-apply`, the "
               "main-resident redline path (FR-017); a session opens on the tile "
               "with `create-document`, and `edit-document` rewrites inside it.")


def _edit_document(body: dict, root: Path, actor: str, records_dir: str,
                   snapshot_path, *, session_registry=None,
                   repository: str | None = None,
                   tile_inventory=None, provenance=None) -> tuple[int, dict]:
    blank = _refuse_blank_actor("edit-document", actor)
    if blank:
        return blank
    parsed, err = _edit_body(body)
    if err:
        return err
    scope = parsed.pop("_scope")
    if session_registry is None:
        # No registry is no place for liveness to live (FR-008), so no session can
        # be live on this plane. `create-document` falls through to its
        # pre-session path here; this verb HAS no such path, so it refuses.
        return _refused(
            "no session registry is declared on this plane, so no branch session "
            "can be live here. " + EDIT_REMEDY)
    snapshot = _load_snapshot(snapshot_path)
    try:
        if tile_inventory is None:
            tile_inventory = discover_tile_inventory(root, snapshot)
        session, git = resolve_session(
            scope, checkout_root=root, registry=session_registry,
            repository=repository, records_dir=records_dir,
            tile_inventory=tile_inventory, verb="edit-document",
            require_live=True, remedy=EDIT_REMEDY)
    except branch_session.SessionRefused as exc:
        # No live session, a cross-tile collision, a live proposal: the engine's
        # own reason, as a 409, with nothing persisted.
        return _refused(exc.report())
    except session_git_mod.GitError as exc:
        return _refused(f"the session could not be resolved: {exc}")
    except OSError as exc:
        return _refused(f"the session could not be resolved: {exc}")
    # Rooted at the WORKTREE and DECLARING it: the root places the document and
    # its record (plan Constraint 10), the declaration is what unlocks the narrow
    # rewrite allowance at all (T026).
    gate = HumanGate(session.worktree, [records_dir], human_actor=actor,
                     session_root=session.worktree)
    try:
        result = execute_edit_document(gate, records_dir=records_dir,
                                       session=session, git=git,
                                       provenance=provenance,
                                       # the SERVED root, so the engine can tell
                                       # this session's own new document from
                                       # another tile's committed one (defect 1)
                                       checkout_root=root, **parsed)
    except BoundaryViolation as exc:
        # Every boundary refusal ABOUT THE DOCUMENT is a 409 conflict carrying the
        # boundary's own report: an escaping path (`outside-root`), a target
        # outside the declared worktree (`session-rewrite`), an absent target
        # (`source-edit` — creation stays `create-document`), and a blank
        # replacement (`source-delete` — no session verb grants delete authority).
        # The AUTHORITY refusal stays a 403: an agent path is not a conflict.
        status = 403 if exc.refusal.kind == GATE_SIDE_EFFECT else 409
        return _refused(exc.refusal.report(), status=status)
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except branch_session.SessionRefused as exc:   # a split write, a no-op rewrite
        return _refused(exc.report())
    except session_git_mod.SessionGitRefused as exc:   # a STRUCTURAL git refusal
        return _refused(str(exc))
    except session_git_mod.GitError as exc:        # git itself refused the write
        return _refused(f"the session commit failed: {exc}")
    except OSError as exc:                         # unreadable/unwritable target
        return _refused(f"the rewrite could not be written: {exc}")
    return 200, result


# ==========================================================================
# OPEN-PR — the SAVE (T065; FR-029-FR-034)
#
# The verb that closes the loop, and the only one in the dashboard that performs a
# REMOTE write. Six decisions are load-bearing here:
#
#   1. The push and pull-request mechanics are BEHIND A PORT (`session_pr.py`), so
#      every test runs against `FakePullRequests` and none reaches a network. The
#      port is INJECTED by the caller; a plane that declares none cannot save, and
#      says so, because the identity is ruled to be the invoking engineer's own
#      `gh` auth (FR-034, D22) and there is no credential to fall back to.
#   2. ORDER: push -> open-or-update -> write the record. The `find_open` READ runs
#      ahead of the push so the response can report `updated` honestly — what was
#      TRUE before this action, rather than an inference — and it persists nothing.
#   3. The record is MAIN-RESIDENT (plan Constraint 10, FR-029) and carries NO
#      `commit` artifact. A record committed onto the branch after the push would
#      never reach the pull request it names, and would then die with the branch
#      when the merge deletes it (FR-033). So: the SERVED checkout's gate-records
#      tree, one `pull-request` artifact, no commit on the branch at all.
#   4. NO readiness signal of either kind is consulted (FR-031, D21) — not the
#      blocking staged-to-proposal gate and not the advisory recommendation. D21's
#      deadlock is the reason: that gate evaluates the SERVED checkout, a session's
#      documents reach the served checkout only when the pull request merges, so a
#      gated save could never merge. A test asserts the blocking helper is NOT
#      REACHED, not merely that the verb succeeded.
#   5. NO approval authority (FR-030). The port exposes no merge/approve/review/
#      protection operation and the ABSENCE is the enforcement; the merge is the
#      Merge Master's action under the existing ritual.
#   6. A branch the base ALREADY CONTAINS is RECONCILED, not re-pushed. This verb
#      is the one surface that knows about the pull request, so it is where the
#      external merge is observed (FR-033); pushing merged work and opening a
#      second pull request for it would be the opposite of FR-032.
# ==========================================================================

# The `NoActiveSession` remedy for this verb: there is nothing to save, and the
# human reaching for it is trying to publish work that has to exist first.
OPEN_PR_REMEDY = ("There is nothing to save: `open-pr` pushes an ACTIVE branch "
                  "session's branch and opens its pull request. A session opens on "
                  "the tile with `create-document` and is written in with "
                  "`edit-document`; a branch whose session already ended is either "
                  "merged or abandoned, and neither is re-saved (FR-029).")

# The default pull-request body. It carries D18 forward to the reviewer, because
# nothing mechanically enforces it: squash and rebase are both still enabled on the
# repositories and no ruleset forbids them, so the protection is REVIEW-ONLY and
# changing a repository merge setting is out of scope here (FR-035, Constraint 7).
MERGE_COMMIT_NOTICE = (
    "Land this with a MERGE COMMIT, never a squash and never a rebase: every "
    "gate-action commit on this branch is one recorded human action, and the series "
    "is traceability evidence for medical FDA clearance (D18). Squashing would "
    "collapse that granularity and leave it only inside a forge artifact.")


def _open_pr_body(body: dict):
    """Parse + validate an open-pr body. The tile scope is REQUIRED (the session is
    resolved from the tile); `title` and `body` are both OPTIONAL, and a
    non-string value for either is a shaping error rather than something to
    coerce — a pull request titled `None` is nobody's intent."""
    scope_kind = _str_or_none(body.get("scope_kind"))
    scope_id = _str_or_none(body.get("scope_id"))
    if not scope_kind or not scope_id:
        return None, _invalid(
            "open-pr requires the tile scope (scope_kind + scope_id): the session "
            "whose branch it pushes is resolved from the tile")
    if scope_kind not in branch_session.SCOPE_KINDS:
        return None, _invalid(
            "scope_kind must be one of "
            f"{', '.join(branch_session.SCOPE_KINDS)}")
    for field in ("title", "body"):
        value = body.get(field)
        if value is not None and not isinstance(value, str):
            return None, _invalid(f"{field} is the pull request's {field} TEXT")
    return {"title": _str_or_none(body.get("title")),
            "body": _str_or_none(body.get("body")),
            "notes": _str_or_none(body.get("notes")),
            "_scope": (scope_kind, scope_id)}, None


def execute_open_pr(gate, git, *, session, pull_requests, records_dir: str,
                    checkout_root: Path | str,
                    base: str = branch_session.DEFAULT_BASE,
                    title: str | None = None, body: str | None = None,
                    notebook=None, notes: str | None = None,
                    at: str | None = None, provenance=None) -> dict:
    """Push the session branch, open or update its pull request, and record it
    (FR-029, FR-032) — or, if the base already contains the branch, END the
    session (FR-033).

    Human-only: an `OutputBoundary` / agent path is rejected (BoundaryViolation)
    and REPORTED before the port is touched and before anything is pushed. The
    record is written LAST and lands in the SERVED checkout, so it outlives the
    branch it names.

    Returns the response body the route and the CLI both report from. `updated`
    reports whether the branch ALREADY had an open pull request, read before the
    push, so a human who saved twice is told which of the two things happened."""
    human = gate_console.require_human_gate(gate)   # agent path -> BoundaryViolation
    root = Path(human.output.root)
    at = at or gate_console._utcnow()
    if session is None:
        raise branch_session.SessionRefused(
            "`open-pr` saves an ACTIVE branch session; there is none on this "
            "tile. " + OPEN_PR_REMEDY)
    if Path(checkout_root).resolve() != root.resolve():
        raise branch_session.SessionRefused(
            f"the gate is rooted at {root} but the served checkout is "
            f"{checkout_root}: an open-pr record is MAIN-RESIDENT — written into "
            "the SERVED checkout's gate-records tree, never onto the session "
            "branch, which the merge deletes (FR-029, FR-033, plan Constraint 10)")

    # The MERGE ending, observed rather than commanded (FR-033). Checked BEFORE the
    # port is reached: pushing a branch the base already contains would publish
    # merged work and open a second pull request for it.
    # The DISPATCH evidence this route owns, handed to the observation (PR #49
    # critic finding C2). Both signals live outside the git seam and both mean the
    # same thing: this branch has already been pushed, so a stale base really can
    # be hiding a merge of it. Without either — and with no remote head and no
    # remote-tracking ref — the branch has never left the checkout, and a lagging
    # local `main` (the steady state of a SHARED served checkout) must not refuse
    # the session's first save.
    dispatched = None
    if branch_session.read_dispatch_marker(checkout_root, session.branch):
        dispatched = (f"a pending-dispatch marker names {session.branch!r}, so its "
                      "pull request was already opened")
    elif dispatch_records_for(root, records_dir, session.branch):
        dispatched = (f"a main-resident `open-pr` record already names "
                      f"{session.branch!r}, so it has been pushed")
    merged = branch_session.merge_state(git, session.branch, base=base,
                                        dispatched=dispatched)
    if merged.base_stale:
        # The base the merge would have advanced is not the base this checkout can
        # see, so neither answer is available: pushing would resurrect a head branch
        # the merge may already have deleted, and reconciling would delete a branch
        # on a guess (FR-033; PR #49 review finding 9). Reached ONLY for a branch
        # that has already left this checkout (critic C2).
        raise branch_session.SessionRefused(merged.reason)
    if merged.merged:
        # FINALIZE an interrupted dispatch before the branch is destroyed (PR #49
        # review finding 4). If the record write failed on an earlier save, the
        # pull request is open, the record is missing, and the reconciliation is
        # about to delete the branch that is the only other trace — so the marker
        # left at `open_or_update` is turned into the FR-029 record now, while
        # there is still something to attest to.
        finalized = _finalize_pending_dispatch(
            human, git, session=session, records_dir=records_dir,
            checkout_root=checkout_root, at=at, provenance=provenance)
        torn = branch_session.reconcile_merged_session(
            git, session, checkout_root=checkout_root, base=base,
            notebook=notebook)
        return _merged_response(session, torn, root=root, records_dir=records_dir,
                                finalized=finalized)

    if pull_requests is None:
        raise branch_session.SessionRefused(
            "no pull-request port is declared on this plane, so `open-pr` has no "
            "identity to push with. The remote write uses the INVOKING ENGINEER's "
            "own `gh` authentication (FR-034) — run the parity command "
            "`cli.py gate open-pr` from a shell where `gh auth status` succeeds")
    _refuse_record_stamp_collision(
        root, action=gate_console.ACTION_OPEN_PR,
        target_id=gate_console.ref_target_id(session.branch), at=at,
        records_dir=records_dir, subject=f"branch {session.branch!r}",
        consequence=" — and the pull request the first save recorded would lose its "
                    "only durable trace, which the merge then deletes the branch "
                    "behind (FR-029, FR-033)")

    # A READ, ahead of the push and side-effect-free: it is what lets the response
    # say `updated` honestly instead of inferring it from a return value that looks
    # identical either way (FR-032).
    existing = pull_requests.find_open(session.branch)
    pull_requests.push(session.branch)
    # WHAT THIS SAVE MAY REWRITE (PR #49 second-review finding R2-13). The
    # generated title and notice are what a pull request is NAMED when it has to
    # be CREATED and the human named nothing — they are NOT what a later save
    # overwrites a human's text with. Substituting them on both paths made every
    # second save with the form left blank replace the reviewer-facing description
    # of a series whose per-action commits are traceability evidence (D18),
    # silently, while the UI copy said blank meant unchanged. Whitespace is not
    # authorship: a blank-looking field is "supplied nothing".
    supplied_title = (title or "").strip()
    supplied_body = body if (body or "").strip() else ""
    pull_request = pull_requests.open_or_update(
        session.branch, base=base,
        title=supplied_title, body=supplied_body,
        default_title=f"Session {session.branch}: {session.tile.scope_id}",
        default_body=MERGE_COMMIT_NOTICE)
    if not str(pull_request.url or "").strip():
        # The port coerces a missing url to '' at two sites (`find_open`'s JSON read
        # and `open_or_update`'s create fallback), and that '' flowed straight into
        # the record's `reference`, which the schema requires NON-EMPTY: a 200 was
        # reported to the human while an FR-029 audit record naming NOTHING landed
        # in the served corpus, where `validate-docs.sh` then fails on it (PR #49
        # tail finding B5, reproduced). Refused HERE — before the marker and before
        # the record — and honestly, because the push already happened.
        raise branch_session.SessionRefused(
            f"the branch {session.branch!r} WAS pushed, but the pull-request port's "
            f"`open_or_update` returned NO url for it, so there is nothing for the "
            f"FR-029 record to name — and a record whose `pull-request` reference is "
            f"empty is one the pinned gate-action-record schema rejects, reported to "
            f"you as a success. Nothing was recorded. Check the pull request by hand "
            f"(`gh pr list --head {session.branch}`): if it exists, run `open-pr` "
            f"again, which finds and updates the SAME one (FR-032); if it does not, "
            f"the port could not create it and its own error is upstream of this.")
    # The FR-029 order is push -> open-or-update -> record, so from here until the
    # record lands there is a window in which the REMOTE write has happened and
    # the durable audit has not. The marker makes that window recoverable rather
    # than invisible (PR #49 review finding 4): if the record write fails and the
    # branch then merges, the merge ending finalizes the record FROM this marker
    # instead of deleting the branch behind a dispatch nothing recorded.
    #
    # The marker is a RECOVERY AID, so a marker that cannot be written must never
    # be the reason a pull request the human already has cannot be recorded — this
    # is contained, and the record write below still runs. But it must not be
    # SILENT (finding 4, wave 2): the refusal text used to promise the marker
    # UNCONDITIONALLY, so when the write had failed the human was told the record
    # was recoverable while it was in fact permanently lost.
    dispatch_marker: Path | None = None
    dispatch_failure: branch_session.DispatchNotRecorded | None = None
    try:
        dispatch_marker = branch_session.write_dispatch_marker(
            checkout_root, session.branch, url=pull_request.url, at=at,
            actor=human.human_actor)
    except branch_session.DispatchNotRecorded as exc:
        dispatch_failure = exc

    record = gate_console.build_gate_action_record(
        actor=human.human_actor, action=gate_console.ACTION_OPEN_PR,
        at=at, ref=session.branch, notes=notes,
        # the GATEWAY fact the caller observed (D23)
        provenance=provenance,
        # ONE artifact: the pull request, by URL. NO `commit` artifact — this action
        # adds no commit to the branch, and a record naming one would name
        # something that does not exist (FR-029).
        artifacts=[{"kind": gate_console.ART_PULL_REQUEST,
                    "reference": pull_request.url}])
    try:
        record_path = gate_console.write_gate_action_record(human, records_dir,
                                                            record)
    except OSError as exc:
        # NOT "refused": the push happened and the pull request is open. Saying
        # "the open-pr record could not be written" over a 409 read as "nothing
        # happened", which is the opposite of the truth (PR #49 finding 4).
        #
        # And the marker sentence is CONDITIONAL on the marker (finding 4, wave 2).
        # Both writes failing is the correlated case — an unwritable tree is often
        # an unwritable filesystem — and it is exactly the case where the old text's
        # promise was false and the FR-029 record was lost with nothing on disk to
        # rebuild it from. So when there is no marker, this message says so, and
        # carries the record's whole content itself: it is the only copy.
        if dispatch_marker is not None:
            recovery = (
                f"A pending-dispatch marker ({dispatch_marker.name}) holds the URL "
                f"meanwhile, so if the pull request merges first the ending "
                f"finalizes the record from it (FR-029).")
        else:
            detail = (f" ({dispatch_failure.reason})" if dispatch_failure
                      else "")
            recovery = (
                f"NO pending-dispatch marker could be written either{detail}, so "
                f"NOTHING on disk holds this dispatch and the merge ending has "
                f"nothing to finalize the record from: if the pull request merges "
                f"before `open-pr` succeeds, the FR-029 record is LOST. This "
                f"message is the only copy — record it now: pull request "
                f"{pull_request.url}, ref {session.branch!r}, actor "
                f"{human.human_actor!r}, at {at}.")
        raise branch_session.SessionRefused(
            f"the branch {session.branch!r} WAS pushed and its pull request "
            f"{pull_request.url} IS open — only the main-resident gate-action "
            f"record could not be written ({exc}). The save is half done, not "
            f"undone: fix the records tree and run `open-pr` again, which updates "
            f"the SAME pull request (FR-032) and writes the record. "
            f"{recovery}") from exc
    branch_session.clear_dispatch_marker(checkout_root, session.branch)
    # What this save did to the reviewer-facing text, SAID (finding R2-13): the
    # response reported only `updated: true`, so a human could not tell a save that
    # renamed the pull request from one that left a description alone.
    notes: list[str] = []
    if existing is not None:
        changed = [name for name, value in (("title", supplied_title),
                                            ("body", supplied_body)) if value]
        notes.append(
            f"the pull request's {' and '.join(changed)} "
            f"{'were' if len(changed) > 1 else 'was'} updated to what this save "
            f"supplied"
            if changed else
            "the pull request's title and body are UNCHANGED: this save supplied "
            "neither, and a save never overwrites text a human wrote (the "
            "reviewer-facing description is evidence on this series — D18)")
    return {
        "ok": True,
        "verb": "open-pr",
        "ref": session.branch,
        "pull_request": pull_request.url,
        "updated": existing is not None,
        "merged": False,
        "record": str(record_path.relative_to(root)),
        "notes": notes,
        "hint": "the branch is pushed and its pull request is open in the existing "
                "Merge-Master ritual; this verb merges, approves, and reviews "
                "nothing (FR-030). The session ends when the pull request MERGES — "
                "as a merge commit, never a squash (D18)",
    }


def dispatch_records_for(root: Path, records_dir: str, ref: str) -> list[Path]:
    """Every main-resident `open-pr` gate-action record naming `ref`.

    The merged response used to ASSERT one existed ("Its `open-pr` record stays on
    `main` and outlives the branch") while deleting the branch that was the only
    other trace, and the assertion was reproducibly false whenever an earlier
    record write had failed (PR #49 review finding 4). Checked now, so the
    response reports what is there rather than what should be."""
    folder = (Path(root) / gate_console._prefix(records_dir)
              / gate_console.ref_target_id(ref))
    if not folder.is_dir():
        return []
    return sorted(folder.glob(
        f"{gate_console.ACTION_OPEN_PR}-*.gate-action.yaml"))


def _finalize_pending_dispatch(human, git, *, session, records_dir: str,
                               checkout_root, at: str,
                               provenance=None) -> str | None:
    """Write the FR-029 record an interrupted `open-pr` never wrote, from the
    pending-dispatch marker it left (PR #49 review finding 4).

    Reached only on the MERGE arm, and only when the marker says a pull request
    exists and no main-resident `open-pr` record for the branch does. The record
    is the ordinary one — same action, same MAIN residence, the same single
    `pull-request` artifact — carrying the marker's URL and its own `notes` saying
    it finalizes a dispatch whose record write had failed, because a record that
    quietly back-dated itself would be worse than the gap it fills.

    Returns the record's repo-relative path, or None when there was nothing to
    finalize. A failure here is REPORTED by the caller and never blocks the
    ending: the ending is the human's, and it must not be held hostage by the
    records tree twice."""
    root = Path(human.output.root)
    marker = branch_session.read_dispatch_marker(checkout_root, session.branch)
    if not marker or dispatch_records_for(root, records_dir, session.branch):
        return None
    record = gate_console.build_gate_action_record(
        actor=human.human_actor, action=gate_console.ACTION_OPEN_PR,
        at=at, ref=session.branch,
        # the gateway of the invocation FINALIZING the record — this ending's door,
        # not the interrupted dispatch's, which no marker recorded. The `notes`
        # below already say the record was written later than the action it names
        # (D23: name the facts we actually know, and no others).
        provenance=provenance,
        notes=(f"finalized at the merge ending: the pull request was opened at "
               f"{marker.get('at')} by {marker.get('actor')} and its record could "
               f"not be written then (FR-029; PR #49 finding 4)"),
        artifacts=[{"kind": gate_console.ART_PULL_REQUEST,
                    "reference": str(marker["url"])}])
    try:
        path = gate_console.write_gate_action_record(human, records_dir, record)
    except (OSError, gate_console.GateRefused):
        return None
    branch_session.clear_dispatch_marker(checkout_root, session.branch)
    return str(path.relative_to(root))


def _merged_response(session, torn, *, root: Path | None = None,
                     records_dir: str = gate_console.DEFAULT_RECORDS_DIR,
                     finalized: str | None = None) -> dict:
    """The response for the ending the merge triggered (FR-033). It reports what
    was torn down and that the branch is gone, and carries a `record` key only
    when this ending FINALIZED an interrupted dispatch: the reconciliation itself
    writes no gate-action record, because the schema has no such action and the
    durable audit is the MAIN-RESIDENT `open-pr` record, which names the branch
    and the pull request and OUTLIVES the branch.

    The hint VERIFIES that claim before making it (PR #49 review finding 4). It
    used to assert the record "stays on `main` and outlives the branch"
    unconditionally, while the same call deleted the branch — and the assertion
    was reproducibly false: an earlier record write that failed left the pull
    request open, no record anywhere, and this sentence over the top of it."""
    teardown = torn.teardown
    ended = ("this branch had already merged, so the SESSION ended instead of "
             "being saved again: worktree, registry entry, and notebook torn "
             "down, the branch deleted, the main view refreshed (FR-033). ")
    records = dispatch_records_for(Path(root), records_dir, session.branch) \
        if root is not None else []
    if finalized:
        trace = (f"its `open-pr` record was MISSING — the save that opened the "
                 f"pull request could not write it — and was finalized here from "
                 f"the pending-dispatch marker as {finalized}, so the dispatch "
                 f"outlives the branch after all (FR-029)")
    elif records:
        trace = ("its `open-pr` record stays on `main` and outlives the branch")
    else:
        trace = ("NO main-resident `open-pr` record for this branch exists, so "
                 "the branch just deleted was its only remaining trace: this "
                 "session's pull request was never recorded through `open-pr` "
                 "(FR-029)")
    return {
        "ok": True,
        "verb": "open-pr",
        "ref": session.branch,
        "merged": True,
        "torn_down": list(teardown.torn_down) if teardown else [],
        "branch_deleted": bool(teardown and teardown.branch_deleted),
        "main_view_refreshed": bool(teardown and teardown.main_view is not None),
        "record": finalized,
        "notes": list(teardown.notes) if teardown else [],
        "hint": ended + trace,
    }


def _open_pr(body: dict, root: Path, actor: str, records_dir: str,
             snapshot_path, *, session_registry=None,
             repository: str | None = None, tile_inventory=None,
             session_notebook=None, pull_requests=None,
             provenance=None) -> tuple[int, dict]:
    blank = _refuse_blank_actor("open-pr", actor)
    if blank:
        return blank
    parsed, err = _open_pr_body(body)
    if err:
        return err
    scope = parsed.pop("_scope")
    if session_registry is None:
        # No registry is no place for liveness to live (FR-008), so no session can
        # be live here and there is nothing to save.
        return _refused(
            "no session registry is declared on this plane, so no branch session "
            "can be live here. " + OPEN_PR_REMEDY)
    snapshot = _load_snapshot(snapshot_path)
    try:
        if tile_inventory is None:
            tile_inventory = discover_tile_inventory(root, snapshot)
        session, git = resolve_session(
            scope, checkout_root=root, registry=session_registry,
            repository=repository, records_dir=records_dir,
            tile_inventory=tile_inventory, verb="open-pr",
            require_live=True, remedy=OPEN_PR_REMEDY)
    except branch_session.SessionRefused as exc:
        return _refused(exc.report())
    except session_git_mod.GitError as exc:
        return _refused(f"the session could not be resolved: {exc}")
    except OSError as exc:
        return _refused(f"the session could not be resolved: {exc}")
    # Rooted at the SERVED checkout: the record is MAIN-RESIDENT (plan Constraint
    # 10), exactly as `abandon-session`'s is and unlike `edit-document`'s.
    gate = HumanGate(root, [records_dir], human_actor=actor)
    try:
        result = execute_open_pr(
            gate, git, session=session, pull_requests=pull_requests,
            records_dir=records_dir, checkout_root=root,
            notebook=session_notebook, provenance=provenance, **parsed)
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except branch_session.SessionRefused as exc:
        return _refused(exc.report())
    except session_pr.PullRequestRefused as exc:
        # The port's own reason, VERBATIM (contracts/gate-routes.md): a push that
        # was rejected, a pull request the forge refused, a `gh` auth that is not
        # there. Nothing was recorded — the record is written last.
        return _refused(str(exc))
    except session_git_mod.GitError as exc:
        return _refused(f"the session could not be saved: {exc}")
    except OSError as exc:
        return _refused(f"the open-pr record could not be written: {exc}")
    return 200, result


def _share_session(body: dict, root: Path, actor: str, records_dir: str,
                   snapshot_path, *, session_registry=None,
                   repository: str | None = None, tile_inventory=None,
                   pull_requests=None,
                   provenance=None) -> tuple[int, dict]:
    """The §12 SHARE verb's route arm — `_open_pr`'s refusal chain with the
    pull-request half removed, because that is precisely what the verb is.

    It takes NO `title` and NO `body`: those exist on `open-pr` to name a pull
    request, and a verb that opens none has nothing to name. `notes` stays,
    because the record carries one."""
    blank = _refuse_blank_actor("share-session", actor)
    if blank:
        return blank
    scope_kind = _str_or_none(body.get("scope_kind"))
    scope_id = _str_or_none(body.get("scope_id"))
    if not scope_kind or not scope_id:
        return _invalid(
            "share-session requires the tile scope (scope_kind + scope_id): the "
            "session whose branch it pushes is resolved from the tile")
    if scope_kind not in branch_session.SCOPE_KINDS:
        return _invalid("scope_kind must be one of "
                        f"{', '.join(branch_session.SCOPE_KINDS)}")
    if session_registry is None:
        return _refused(
            "no session registry is declared on this plane, so no branch session "
            "can be live here. " + SHARE_SESSION_REMEDY)
    snapshot = _load_snapshot(snapshot_path)
    try:
        if tile_inventory is None:
            tile_inventory = discover_tile_inventory(root, snapshot)
        session, git = resolve_session(
            (scope_kind, scope_id), checkout_root=root,
            registry=session_registry, repository=repository,
            records_dir=records_dir, tile_inventory=tile_inventory,
            verb="share-session", require_live=True,
            remedy=SHARE_SESSION_REMEDY)
    except branch_session.SessionRefused as exc:
        return _refused(exc.report())
    except session_git_mod.GitError as exc:
        return _refused(f"the session could not be resolved: {exc}")
    except OSError as exc:
        return _refused(f"the session could not be resolved: {exc}")
    try:
        result = execute_share_session(
            share_session_gate_factory(actor, records_dir), git,
            session=session, pull_requests=pull_requests,
            records_dir=records_dir, checkout_root=root,
            notes=_str_or_none(body.get("notes")), provenance=provenance)
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except branch_session.SessionRefused as exc:
        return _refused(exc.report())
    except session_pr.PullRequestRefused as exc:
        # The port's own reason, VERBATIM, exactly as `open-pr` reports it: a
        # rejected push, a `gh` auth that is not there. On the main-resident
        # path nothing was recorded, because that record is written last; on the
        # branch-resident path the thread commit stands and the NEXT invocation
        # sees it as unpushed and shares it, which is why this is safe to retry.
        return _refused(str(exc))
    except session_git_mod.GitError as exc:
        return _refused(f"the session could not be shared: {exc}")
    except OSError as exc:
        return _refused(f"the share-session record could not be written: {exc}")
    return 200, result


# ==========================================================================
# ABANDON-SESSION — the ending that saves nothing (T053; FR-021, FR-022)
#
# One of exactly TWO endings (FR-021). It ends the SESSION and nothing else: the
# worktree, the registry entry, and the session notebook go; the branch, its
# pushed history, and any open pull request STAY. The pull-request port is not
# even reachable from here — closing a PR on a human's behalf is not this verb's
# authority (FR-022, G9).
#
# "STAY" is not the same as "unaccounted for" (PR #49 critic finding C6). Because
# this ending cannot close the pull request, it must not be able to LOSE it either:
# a pending-dispatch marker means the pull request is open and its FR-029 record
# was never written, so this verb finalizes that record from the marker — the merge
# arm's own move — and names the open pull request in its response and notes.
#
# The record is MAIN-RESIDENT, and that is the load-bearing decision (plan
# Constraint 10): it is written into the SERVED checkout's gate-records tree
# through the same `write_gate_action_record` path `propose` / `demote` /
# `dispose` use, and NEVER as a commit on the session branch. A branch-resident
# reason-record would self-destruct — the branch never merges, and FR-028's human
# cleanup DELETES it, taking with it the very artifact D17's reconciliation reads.
# So: no `commit` artifact, and no commit on the branch at all.
#
# ORDER: RECORD, then tear down (PR #49 review finding 4). It used to be the
# other way round, on the rationale that "the record states what happened
# (`torn_down`, `branch_retained`), so writing it first would claim a teardown
# that had not occurred yet". That rationale does not survive reading the record:
# `torn_down` and `branch_retained` are fields of the RESPONSE, not of the record.
# The record carries actor, action, at, ref, reason and one `other` artifact — it
# attests that this human abandoned this session, for this reason, at this time,
# which is true the moment they invoke the verb.
#
# The old order was not merely arbitrary, it was lossy. `teardown_session` drops
# the registry entry FIRST and CONTAINS every later failure into `notes`, so the
# fallible step was strictly last and strictly uncompensated: a records tree that
# could not be written (a read-only mount, a full disk, permissions) returned a
# 409 "refused" over a session that had in fact ENDED, and the human's reason —
# the ONE artifact FR-022 exists to produce — was gone for good. Retry was
# structurally impossible, because liveness IS the registry entry (FR-008) and it
# was already dropped; and FR-028's cleanup did not require an abandon record at
# all, so the surviving branch was later deletable too, leaving zero durable trace.
# Reproduced end to end during the PR #49 adjudication. (That last clause is no
# longer true: the cleanup now REQUIRES proof of the abandon — second-review
# finding 3 — which makes this record load-bearing in a second way.)
#
# Record-first makes the fallible step the FIRST one: it fails before anything is
# torn down, the session is still live, and the identical retry works. The teardown
# is the contained half, and if it nonetheless raises, the record is removed again
# so it cannot attest to an ending that did not happen — one failure domain, both
# artifacts. The stamp-collision refusal still runs ahead of both, where it
# persists nothing.
# ==========================================================================

# The `NoActiveSession` remedy for this verb: there is nothing to abandon, and the
# human reaching for it wants to know what the tile's real state is.
ABANDON_REMEDY = ("There is nothing to abandon: a session ends ONCE, and its "
                  "registry entry is what makes it live (FR-008). A branch or a "
                  "worktree that survives is not a session — resume it or start a "
                  "new ordinal with the tile's next write (FR-025), and clean the "
                  "branch up once durable retention-release evidence exists "
                  "(FR-028).")


def execute_abandon_session(gate, git, *, session, reason: str, records_dir: str,
                            checkout_root: Path | str, notebook=None,
                            notes: str | None = None,
                            at: str | None = None, provenance=None) -> dict:
    """End a session without saving, and RECORD WHY (FR-021, FR-022).

    Human-only: an `OutputBoundary` / agent path is rejected (BoundaryViolation)
    and REPORTED before anything is torn down. The teardown itself is
    `branch_session.teardown_session` — the ONE mechanism both endings use — called
    here WITHOUT `delete_branch`, because an abandon deletes nothing: the surviving
    branch is the evidence FR-028's human-invoked cleanup later disposes of, and
    `branch_retained` is read back from git rather than asserted, so the response
    cannot claim a retention it did not verify.

    Returns the response body the route and the CLI both report from."""
    human = gate_console.require_human_gate(gate)   # agent path -> BoundaryViolation
    root = Path(human.output.root)
    at = at or gate_console._utcnow()
    if session is None:
        raise branch_session.SessionRefused(
            "`abandon-session` ends an ACTIVE branch session; there is none on "
            "this tile. " + ABANDON_REMEDY)
    why = str(reason or "").strip()
    if not why:                                     # the route refuses this as 400
        raise branch_session.SessionRefused(
            "an abandon REQUIRES a recorded reason — the durable 'why' this "
            "exploration stopped, exactly as a demotion does (FR-022)")
    if Path(checkout_root).resolve() != root.resolve():
        raise branch_session.SessionRefused(
            f"the gate is rooted at {root} but the served checkout is "
            f"{checkout_root}: an abandon record is MAIN-RESIDENT — written into "
            "the SERVED checkout's gate-records tree, never onto the session "
            "branch, which FR-028's cleanup deletes (FR-022, plan Constraint 10)")
    abandoned_head = git.branch_sha(session.branch)
    if not abandoned_head:
        raise branch_session.SessionRefused(
            f"cannot abandon {session.branch!r}: its exact branch head could not "
            "be resolved for the durable abandonment record")
    _refuse_record_stamp_collision(
        root, action=gate_console.ACTION_ABANDON_SESSION,
        target_id=gate_console.ref_target_id(session.branch), at=at,
        records_dir=records_dir, subject=f"branch {session.branch!r}",
        consequence=" — and the reason of the first abandon would be lost, which is "
                    "the one artifact this verb exists to leave behind (FR-022)")

    record = gate_console.build_gate_action_record(
        actor=human.human_actor, action=gate_console.ACTION_ABANDON_SESSION,
        at=at, ref=session.branch, reason=why, notes=notes,
        # the GATEWAY fact the caller observed (D23)
        provenance=provenance,
        # NO `commit` artifact: this action adds no commit to the branch, and a
        # record naming one would name something that does not exist (FR-022).
        # The branch itself is the artifact, referenced as `other` — the schema
        # requires at least one (`artifacts.minItems: 1`).
        artifacts=[{
            "kind": gate_console.ART_OTHER,
            "reference": f"refs/heads/{session.branch}@{abandoned_head}",
        }])
    # FIRST — see the ORDER note above. The reason is the one artifact this verb
    # exists to leave behind and the record write is the only irrecoverable step,
    # so it happens while the session is still LIVE and the retry still works.
    record_path = gate_console.write_gate_action_record(human, records_dir, record)
    # THE OTHER ENDING'S HALF OF THE CUSTODY GAP (PR #49 critic finding C6). An
    # `open-pr` whose record write failed leaves the pull request OPEN with a
    # pending-dispatch marker as the only trace; the MERGE arm finalizes that
    # record before it destroys the branch, and nothing followed the marker across
    # to THIS ending. So an abandon silently discarded a remote dispatch that no
    # gate-action record named anywhere — the precise gap FR-029's main-residence
    # rule exists to close — leaving a permanently orphaned open pull request on
    # the vendor org. The dispatch is finalized here for the same reason and from
    # the same marker; it is REPORTED either way, because this verb closes no pull
    # request (FR-022, G9) and the human has to know one is open.
    dispatch = branch_session.read_dispatch_marker(checkout_root, session.branch)
    finalized = None
    if dispatch:
        finalized = _finalize_pending_dispatch(
            human, git, session=session, records_dir=records_dir,
            checkout_root=checkout_root, at=at, provenance=provenance)
    try:
        torn = branch_session.teardown_session(
            git, session, checkout_root=checkout_root, notebook=notebook,
            # NEVER here: an abandon deletes no branch and no pushed history
            # (FR-022, G9). The merge ending is the only caller that passes True
            # (FR-033).
            delete_branch=False)
    except BaseException:
        # The ending did not happen, so its record must not survive claiming it
        # did: one failure domain, both artifacts. `teardown_session` contains
        # every step after the first, so reaching here means something structural
        # refused before anything was torn down.
        with contextlib.suppress(OSError):
            record_path.unlink()
        raise
    hint = ("the session ended and saved nothing; the branch is retained as "
            "evidence until active/archived proposal custody, executed demotion, "
            "or a separate explicit human retention release permits "
            "`cleanup-abandoned-branch` (FR-028)")
    if branch_session.TORN_NOTEBOOK not in torn.torn_down:
        hint += " — no session notebook was retired here (see `notes`)"
    notes = list(torn.notes)
    pull_request = str(dispatch.get("url")) if dispatch else None
    if dispatch and finalized:
        notes.append(
            f"the pull request {pull_request} was OPEN with no gate-action record "
            f"naming it — the save that opened it could not write one — so its "
            f"FR-029 `open-pr` record was finalized here from the pending-dispatch "
            f"marker as {finalized}. The pull request is NOT closed by this verb "
            f"(FR-022, G9): it stays open, on a branch this abandon retains, and "
            f"closing or landing it is yours")
        hint += (f" — and an interrupted dispatch was finalized: the pull request "
                 f"{pull_request} is OPEN and now has its FR-029 record")
    elif dispatch:
        # Either the record already existed (custody was never broken) or the
        # finalize could not write. Both are reported, because in neither case does
        # this verb touch the pull request.
        traced = dispatch_records_for(root, records_dir, session.branch)
        notes.append(
            f"the pull request {pull_request} for this branch is OPEN and this verb "
            f"does not close it (FR-022, G9); its FR-029 `open-pr` record "
            + (f"is on `main` ({traced[-1].name})" if traced else
               "could NOT be written or finalized, so the pending-dispatch marker "
               f"{branch_session.dispatch_marker_path(checkout_root, session.branch).name} "
               "is the only trace on disk — record the dispatch and fix the records "
               "tree"))
        hint += f" — the pull request {pull_request} is OPEN and stays open"
    return {
        "ok": True,
        "verb": "abandon-session",
        "ref": session.branch,
        "reason": why,
        "torn_down": list(torn.torn_down),
        "branch_retained": torn.branch_retained,
        "record": str(record_path.relative_to(root)),
        "pull_request": pull_request,
        "dispatch_record": finalized,
        "notes": notes,
        "hint": hint,
    }


def _abandon_body(body: dict):
    """Parse + validate an abandon-session body. The tile scope is REQUIRED (the
    session is resolved from the tile), and a missing or blank reason is a 400
    rather than a 409: the precondition that failed is the BODY's, not the
    session's (contracts/gate-routes.md)."""
    scope_kind = _str_or_none(body.get("scope_kind"))
    scope_id = _str_or_none(body.get("scope_id"))
    if not scope_kind or not scope_id:
        return None, _invalid(
            "abandon-session requires the tile scope (scope_kind + scope_id): the "
            "session it ends is resolved from the tile")
    if scope_kind not in branch_session.SCOPE_KINDS:
        return None, _invalid(
            "scope_kind must be one of "
            f"{', '.join(branch_session.SCOPE_KINDS)}")
    raw = body.get("reason")
    if raw is not None and not isinstance(raw, str):
        return None, _invalid("reason is the durable text of why this exploration "
                              "stopped")
    reason = _str_or_none(raw)
    if not reason:
        return None, _invalid(
            "abandon-session requires a non-blank reason — the durable 'why' this "
            "exploration stopped, exactly as a demotion does (FR-022)")
    return {"reason": reason, "notes": _str_or_none(body.get("notes")),
            "_scope": (scope_kind, scope_id)}, None


def _abandon_session(body: dict, root: Path, actor: str, records_dir: str,
                     snapshot_path, *, session_registry=None,
                     repository: str | None = None,
                     tile_inventory=None,
                     session_notebook=None,
                     provenance=None) -> tuple[int, dict]:
    blank = _refuse_blank_actor("abandon-session", actor)
    if blank:
        return blank
    parsed, err = _abandon_body(body)
    if err:
        return err
    scope = parsed.pop("_scope")
    if session_registry is None:
        # No registry is no place for liveness to live (FR-008), so no session can
        # be live here and there is nothing to end.
        return _refused(
            "no session registry is declared on this plane, so no branch session "
            "can be live here. " + ABANDON_REMEDY)
    snapshot = _load_snapshot(snapshot_path)
    try:
        if tile_inventory is None:
            tile_inventory = discover_tile_inventory(root, snapshot)
        session, git = resolve_session(
            scope, checkout_root=root, registry=session_registry,
            repository=repository, records_dir=records_dir,
            tile_inventory=tile_inventory, verb="abandon-session",
            require_live=True, remedy=ABANDON_REMEDY)
    except branch_session.SessionRefused as exc:
        return _refused(exc.report())
    except session_git_mod.GitError as exc:
        return _refused(f"the session could not be resolved: {exc}")
    except OSError as exc:
        return _refused(f"the session could not be resolved: {exc}")
    # Rooted at the SERVED checkout: the record is MAIN-RESIDENT (plan Constraint
    # 10), which is the opposite of `edit-document`'s worktree-rooted gate.
    gate = HumanGate(root, [records_dir], human_actor=actor)
    try:
        result = execute_abandon_session(
            gate, git, session=session, records_dir=records_dir,
            checkout_root=root, notebook=session_notebook,
            provenance=provenance, **parsed)
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except branch_session.SessionRefused as exc:
        return _refused(exc.report())
    except session_git_mod.GitError as exc:
        return _refused(f"the session could not be ended: {exc}")
    except OSError as exc:
        return _refused(f"the abandon record could not be written: {exc}")
    return 200, result


# ==========================================================================
# CLEANUP-ABANDONED-BRANCH — the abandoned branch's end of life (T056; FR-028)
#
# HUMAN-INVOKED, ALWAYS. It is never a consequence of a `propose` dispatch: a
# dispatch commissions authoring that may never deliver a proposal, and deleting
# the only surviving evidence of an exploration on the strength of a commission is
# exactly the failure FR-028 names. The window opens only when durable active,
# archived, or executed-demotion custody exists, or when a human separately
# releases a true orphan with a recorded reason.
#
# It validates and writes a MAIN-RESIDENT cleanup record containing the exact
# pre-delete head, abandon proof, and release evidence before performing a
# compare-and-swap local delete. A failed delete unwinds that new record.
# ==========================================================================


def execute_cleanup_abandoned_branch(gate, git, *, tile, ref: str, registry,
                                     repository: str | None,
                                     checkout_root: Path | str,
                                     records_dir: str, tile_inventory=None,
                                     proposal=None,
                                     retention_release_reason: str | None = None,
                                     superseding_references=(),
                                     provenance=None) -> dict:
    """Delete an ABANDONED session's surviving branch (FR-028). Human-only: an
    `OutputBoundary` / agent path is rejected and REPORTED before the branch is
    touched. Preconditions live with the state machine; the successful transaction
    adds one main-resident audit record and deletes only the local ref."""
    human = gate_console.require_human_gate(gate)   # agent path -> BoundaryViolation
    branch = str(ref or "").strip()
    root = Path(checkout_root).resolve()
    gate_root = Path(human.output.root).resolve()
    git_root = Path(git.served_root).resolve()
    if gate_root != root or git_root != root:
        raise branch_session.SessionRefused(
            "cleanup requires the human gate, Git service, and checkout_root to "
            f"name the same repository; got gate={gate_root}, git={git_root}, "
            f"checkout={root}")

    # The served checkout's git-dir lock serializes record creation, evidence
    # revalidation, and ref deletion across CLI and HTTP processes.
    with git.worktree_action_lock(
            root, action=f"cleanup abandoned branch {branch}"):
        candidates = branch_session.retention_release_candidates(
            root, tile, records_dir=records_dir)
        abandonment = branch_session.abandon_evidence(
            root, branch, records_dir=records_dir)
        head = git.branch_sha(branch)
        machine_retention = None
        correlation_error = None
        if candidates and abandonment is not None and head:
            # EVERY candidate is correlated, not just the first: a tile can carry
            # several exact-origin records, and one that predates the abandonment
            # disqualifies only itself (PR #336 review finding 2). The reported
            # error is the FIRST candidate's, so a refusal still names the
            # nearest-miss evidence rather than whichever was tried last.
            for candidate in candidates:
                failure = branch_session.machine_release_correlation_error(
                    candidate, abandonment, head)
                if not failure:
                    machine_retention = candidate
                    correlation_error = None
                    break
                if correlation_error is None:
                    correlation_error = failure
        elif candidates:
            # Nothing to correlate against — no abandonment proof, or no ref. The
            # preconditions below refuse on exactly those, and they refuse better
            # when the evidence they name is the tile's first candidate.
            machine_retention = candidates[0]

        state = proposal if proposal is not None else branch_session.proposal_state_for(
            tile, records_root=root / records_dir, checkout_root=root)
        if machine_retention is None and state.dispatch_in_flight:
            raise branch_session.SessionRefused(
                f"no cleanup of {branch!r}: a `propose` commission for tile "
                f"{tile.scope_id!r} was dispatched and the proposal has not landed "
                "yet. A dispatch is a commission, not retention-release evidence; "
                "finish or resolve that authoring before cleanup.")

        retention = machine_retention
        explicit_reason = str(retention_release_reason or "").strip()
        if retention is None and explicit_reason:
            retention = branch_session.explicit_retention_release(
                tile, explicit_reason, superseding_references)
        if retention is None and correlation_error:
            raise branch_session.SessionRefused(
                f"no cleanup of {branch!r} through machine evidence: "
                f"{correlation_error}. Record a fresh disposition after "
                "abandonment or provide a new explicit human retention-release "
                "reason for the current head.")

        proof = branch_session.assert_branch_cleanup_permitted(
            git, registry, repository=repository or "", tile=tile, branch=branch,
            retention=retention, checkout_root=root, inventory=tile_inventory,
            records_dir=records_dir)
        abandonment = branch_session.abandon_evidence(
            root, branch, records_dir=records_dir)
        if abandonment is None:
            raise branch_session.SessionRefused(
                f"no cleanup of {branch!r}: abandonment evidence disappeared "
                "while cleanup was being prepared")
        head = git.branch_sha(branch)
        if not head:
            raise branch_session.SessionRefused(
                f"no cleanup of {branch!r}: its exact pre-delete head could not "
                "be resolved")
        if retention.kind != branch_session.RETENTION_EXPLICIT_HUMAN:
            correlation_error = branch_session.machine_release_correlation_error(
                retention, abandonment, head)
            if correlation_error:
                raise branch_session.SessionRefused(
                    f"no cleanup of {branch!r}: {correlation_error}")

        evidence_references = list(retention.references)
        artifacts = [
            {"kind": gate_console.ART_OTHER,
             "reference": f"refs/heads/{branch}@{head}"},
            {"kind": gate_console.ART_OTHER,
             "reference": abandonment.reference},
        ]
        artifacts.extend(
            {"kind": gate_console.ART_OTHER, "reference": reference}
            for reference in evidence_references)
        at = gate_console._utcnow()
        target_args = {
            "topic_id": tile.scope_id if tile.scope_kind == branch_session.STAGED_TOPIC else None,
            "cluster_id": tile.scope_id if tile.scope_kind == branch_session.CLUSTER else None,
            "possible_id": tile.scope_id if tile.scope_kind == branch_session.POSSIBLE else None,
        }
        record = gate_console.build_gate_action_record(
            actor=human.human_actor,
            action=gate_console.ACTION_CLEANUP_ABANDONED_BRANCH,
            at=at, ref=branch, artifacts=artifacts,
            reason=retention.reason,
            provenance=provenance,
            cleanup={
                "status": "prepared",
                "pre_delete_head": head,
                "abandonment": {
                    "kind": abandonment.kind,
                    "reference": abandonment.reference,
                    "summary": abandonment.summary,
                },
                "retention_release": retention.as_record(),
            },
            **target_args)
        gate_console.validate_gate_action_record(record)
        record_path = gate_console.write_gate_action_record(
            human, records_dir, record, exclusive=True)
        try:
            # Local only. Atomic expected-old-value deletion preserves any ref
            # advanced after the observation above.
            git.delete_branch(branch, expect_sha=head)
        except BaseException:
            with contextlib.suppress(OSError):
                record_path.unlink()
            raise

        record["cleanup"]["status"] = "completed"
        gate_console.validate_gate_action_record(record)
        try:
            gate_console.replace_gate_action_record(human, records_dir, record)
        except BaseException as finalize_error:
            try:
                git.restore_branch_if_absent(branch, head)
            except BaseException as restore_error:
                raise branch_session.SessionRefused(
                    f"cleanup deleted {branch!r} at {head}, but could not "
                    "finalize its record or restore the ref. The surviving "
                    f"record is PREPARED and requires manual recovery: "
                    f"finalize={finalize_error}; restore={restore_error}") \
                    from finalize_error
            with contextlib.suppress(OSError):
                record_path.unlink()
            raise branch_session.SessionRefused(
                f"cleanup record finalization failed after deleting {branch!r}; "
                "the exact ref was restored and the prepared record removed, so "
                f"the operation is safely retryable: {finalize_error}") \
                from finalize_error

        return {
            "ok": True,
            "verb": "cleanup-abandoned-branch",
            "ref": branch,
            "deleted": True,
            "abandon_proof": proof,
            "pre_delete_head": head,
            "retention_release": retention.as_record(),
            "record": str(record_path.relative_to(root)),
            "hint": f"the abandoned session's branch is gone, and the abandon "
                    f"it ends was VERIFIED before the delete: {proof}; retention "
                    f"released by {retention.kind} (FR-022, FR-028)",
        }


def _cleanup_abandoned_branch(body: dict, root: Path, actor: str,
                              records_dir: str, snapshot_path, *,
                              session_registry=None,
                              repository: str | None = None,
                              tile_inventory=None,
                              provenance=None) -> tuple[int, dict]:
    blank = _refuse_blank_actor("cleanup-abandoned-branch", actor)
    if blank:
        return blank
    scope_kind = _str_or_none(body.get("scope_kind"))
    scope_id = _str_or_none(body.get("scope_id"))
    ref = _str_or_none(body.get("ref"))
    if not scope_kind or not scope_id:
        return _invalid(
            "cleanup-abandoned-branch requires the tile scope (scope_kind + "
            "scope_id): the branch is checked against the TILE that owns it")
    if scope_kind not in branch_session.SCOPE_KINDS:
        return _invalid("scope_kind must be one of "
                        f"{', '.join(branch_session.SCOPE_KINDS)}")
    if not ref:
        return _invalid("cleanup-abandoned-branch requires the ref (the abandoned "
                        "session branch to delete)")
    raw_reason = body.get("retention_release_reason", body.get("reason"))
    if raw_reason is not None and not isinstance(raw_reason, str):
        return _invalid("retention_release_reason must be the human's durable "
                        "text for releasing an orphaned branch")
    release_reason = _str_or_none(raw_reason)
    raw_references = body.get("superseding_references", [])
    if not isinstance(raw_references, list) or any(
            not isinstance(reference, str) or not reference.strip()
            for reference in raw_references):
        return _invalid("superseding_references must be a list of nonblank "
                        "reference strings")
    snapshot = _load_snapshot(snapshot_path)
    gate = HumanGate(root, [records_dir], human_actor=actor)
    try:
        if tile_inventory is None:
            tile_inventory = discover_tile_inventory(root, snapshot)
        result = execute_cleanup_abandoned_branch(
            gate, session_git_mod.SessionGit(root),
            tile=branch_session.Tile(scope_kind, scope_id), ref=ref,
            registry=session_registry, repository=repository,
            checkout_root=root, records_dir=records_dir,
            tile_inventory=tile_inventory,
            retention_release_reason=release_reason,
            superseding_references=tuple(
                reference.strip() for reference in raw_references),
            provenance=provenance)
    except BoundaryViolation as exc:
        return _refused(exc.refusal.report(), status=403)
    except branch_session.SessionRefused as exc:
        return _refused(exc.report())
    except gate_console.GateRefused as exc:
        return _refused(str(exc))
    except session_git_mod.SessionGitRefused as exc:
        return _refused(str(exc))
    except session_git_mod.GitError as exc:
        return _refused(f"the branch could not be deleted: {exc}")
    except OSError as exc:
        return _refused(f"the cleanup could not be evaluated: {exc}")
    return 200, result


def _build_submission(evidence, repository: str, actor: str):
    """Build the HumanSeenSubmission from the posted evidence block. The
    completeness/format refusal is the engine's (human_seen.require_complete_
    evidence), fired during execution — here we only shape the object, defaulting
    the proposer to the acting human and the repository to the recipe's."""
    from . import human_seen as hs

    ev = evidence if isinstance(evidence, dict) else {}
    alternatives = ev.get("alternatives")
    if alternatives is None:
        alternatives = []
    if not isinstance(alternatives, list):
        return None, _invalid("evidence.alternatives must be a list")
    extension_fit = ev.get("extension_fit")
    if extension_fit is not None and not isinstance(extension_fit, dict):
        return None, _invalid("evidence.extension_fit must be an object")
    submission = hs.HumanSeenSubmission(
        proposer=_str_or_none(ev.get("proposer")) or actor,
        repository=str(ev.get("repository") or repository or ""),
        path=str(ev.get("path") or ""),
        revision=str(ev.get("revision") or ""),
        section=str(ev.get("section") or ""),
        passage_sha256=str(ev.get("passage_sha256") or ""),
        rationale=str(ev.get("rationale") or ""),
        confidence=ev.get("confidence"),
        alternatives=alternatives,
        recipe_reference=_str_or_none(ev.get("recipe_reference")),
        extension_fit=extension_fit,
    )
    return submission, None


# The FIXED refusal for first-edit content that cannot be encoded as UTF-8
# (an unpaired surrogate). Module-level so the route test pins the exact
# sentence, and fixed so the refusal can never quote the buffer it refuses.
FIRST_EDIT_UNENCODABLE_CONTENT = (
    "first-edit content contains an unpaired surrogate, so no file can hold "
    "it as UTF-8; the Save is refused rather than re-encoded. Remove the "
    "malformed character and save again.")


def _first_edit(body: dict, root: Path, actor: str, records_dir: str,
                snapshot_path, *, session_registry=None,
                repository: str | None = None,
                tile_inventory=None, provenance=None) -> tuple[int, dict]:
    """THE FIRST SAVE as a console verb (T080 server-route slice, 2026-07-30).

    The same dispatch table, refusal vocabulary, and console discipline as
    every other session-bearing verb — the transaction is T074's and the
    ownership rule is T075's own injection, so this arm only parses, refuses
    early, and reports. Fail-closed: every missing precondition refuses
    before anything opens, and every transaction refusal arrives as the
    engine's own sentence with nothing persisted."""
    blank = _refuse_blank_actor("first-edit", actor)
    if blank:
        return blank
    parsed, err = _edit_body(body)
    if err:
        return err
    del parsed  # shape-validated above; this arm reads the body directly
    document = _str_or_none(body.get("document"))
    content = body.get("content")
    if not isinstance(content, str):
        # edit-document's absent-content DELETE SHAPE holds no authority here
        # either, and first-edit refuses it at the door rather than at the
        # boundary: a first Save persists the buffer it was handed, and this
        # body carries no buffer.
        return _invalid("first-edit requires the replacement content: a Save "
                        "with no buffer is not a Save")
    try:
        content.encode("utf-8")
    except UnicodeEncodeError:
        # Wave re-review P3: JSON's "\ud800" escape decodes to a str holding a
        # lone UTF-16 surrogate -- text NO file can hold, so the Save cannot
        # succeed and the only question is WHERE it fails. Nothing on this
        # path encoded `content` before the boundary write, so the
        # `UnicodeEncodeError` raised at `write_text` escaped the
        # transaction's unwind as a 500 with a stderr traceback -- after a
        # session had already been opened for a Save that could never land.
        # Encodability is a property of the BODY, so it is refused here at the
        # body/shape layer, before anything opens, with a fixed sentence that
        # names the condition and never the text (the same no-echo discipline
        # as every doxBench refusal).
        return _invalid(FIRST_EDIT_UNENCODABLE_CONTENT)
    if session_registry is None:
        return _refused(
            "no session registry is declared on this plane, so no branch "
            "session can be opened or joined here. " + EDIT_REMEDY)
    if not repository:
        return _refused("first-edit needs the plane's repository identity to "
                        "key the session registry, and none is declared")
    # The human's ANSWER to the FR-025 resume-or-new report, read exactly where
    # `_create_body` reads it for the other session-opening verb (T104 F3).
    # first-edit OPENS a session, so the refusal that instructs the human to
    # answer with `continuation='resume'` has to be answerable ON THIS ROUTE:
    # the field was declared by the transaction, forwarded by
    # `execute_first_edit`, and never read off the body here, so the answer was
    # dropped and the second attempt got the identical report.
    try:
        continuation = branch_session.normalize_continuation(
            _str_or_none(body.get("continuation")))
    except branch_session.SessionRefused as exc:
        return _invalid(exc.report())
    snapshot = _load_snapshot(snapshot_path)
    if tile_inventory is None:
        tile_inventory = discover_tile_inventory(root, snapshot)
    tile = branch_session.Tile(
        _str_or_none(body.get("scope_kind")),
        _str_or_none(body.get("scope_id")))
    try:
        payload = execute_first_edit(
            git=session_git_mod.SessionGit(Path(root)),
            session_registry=session_registry, repository=repository,
            tile=tile, document=document, content=content, actor=actor,
            checkout_root=root, records_dir=records_dir,
            base_hash=_str_or_none(body.get("base_hash")),
            tile_inventory=tile_inventory, provenance=provenance,
            continuation=continuation,
            # FR-024, both halves — the same derivation `resolve_session`
            # feeds the session verbs. The first edit OPENS (or joins) the
            # tile's session, so a proposed tile must refuse it here too;
            # this parameter existed through the whole chain and was unfed
            # at exactly this call site (T104 final queue Q-1, the F4
            # discarded-parameter class, ruled fix-first 2026-08-09).
            proposal=branch_session.proposal_state_for(
                tile, records_root=Path(root) / records_dir,
                checkout_root=root))
    except branch_session.SessionRefused as exc:
        return _refused(exc.report())
    return 200, payload
