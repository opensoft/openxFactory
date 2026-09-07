"""The GATE CONSOLE's command line: every `gate` verb and the whole `gate`
subparser tree (`split-opendox-two-layer-product` § 2.4, PR 4 of 4).

THIS IS THE ONE THAT TRAVELS. Design § D2 puts "gate console and verbs" in the
openXdox column — the layer above the document surface, the one that holds the
governed loop — so this cluster is the CLI's half of what the carve moves, and
it is the first thing to reach the command line through the SUBCOMMAND
EXTENSION POINT rather than through a line in `build_parser`. `GateSubcommands`
at the bottom of this file is that contribution: one `register` method,
structurally conforming to `subcommand_extension.SubcommandExtension` without
importing it, which is the whole reason that interface is a `Protocol`
(`corpus_adapter.CorpusAdapter`, same argument, same precedent).

WHAT DID NOT MOVE, AND WHY IT MATTERS. The AUTHENTICATION RAIL stays in `cli.py`
— `_gate_actor`, `_human_gate`, `_lens_gate`, `_session_identity_gate`,
`console_presence`, `cli_provenance` — together with the session spine
(`_session_registry`, `_session_repository_key`, `_notebook_port`,
`_pull_request_port`, `_unwind_cli_session`) and `_gate_snapshot`. That is not
tidiness: those are the shared controls every verb on this command line passes
through, core and contributed alike, and a contributed verb that carried its own
copy of them could drift into a second, weaker spelling of the same gate. It is
the command line's analogue of the route point's "no privileged route" — one
authentication path, reached by every verb, and this module cannot reach a gate
any other way because it does not define one.

HOW THAT SPINE IS REACHED: through `_core()`, resolved at CALL time and
RELATIVE to this module's own package. Never a module-level
`from ideation_dashboard.cli import _notebook_port` — a frozen reference would
still work and would silently stop honouring the thirteen module-level patch
sites the existing tests use to inject fakes (`cli_mod._notebook_port`,
`cli_mod._pull_request_port`, `cli_mod._session_registry`,
`cli_mod._session_identity_gate`, `cli_mod.generate_snapshot` behind
`_gate_snapshot`). That is the failure mode this refactor has to avoid above all
others, because it is GREEN: no test fails, and the fakes stop being reached.
The accessor also makes the import order between the two modules irrelevant.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ideation_dashboard import actor_identity as actor_mod
from ideation_dashboard import authoring as authoring_mod
from ideation_dashboard import branch_session as branch_session_mod
from ideation_dashboard import gate_console as gate_mod
from ideation_dashboard import gate_routes as gate_routes_mod
from ideation_dashboard import human_seen as human_seen_mod
from ideation_dashboard import kickoff as kickoff_mod
from ideation_dashboard import session_git as session_git_mod
from ideation_dashboard import session_pr as session_pr_mod
from ideation_dashboard import workbench as workbench_mod
from ideation_dashboard.boundary import BoundaryViolation, HumanGate


def _core():
    """The core CLI module OF THIS MODULE'S OWN PACKAGE, resolved when a verb RUNS.

    Deliberately a function and not a module-level import: see the header. Every
    reference this module makes into the shared spine goes through it, so a
    `monkeypatch.setattr(cli_mod, ...)` reaches this module's call sites and the
    two modules stay importable in either order.

    Deliberately RELATIVE, too. `scripts/__init__.py` exists, so the tree is
    importable both as `ideation_dashboard.x` and as `scripts.ideation_dashboard.x`,
    and each spelling is a module object of its own with its own
    `RepoRootRefused`/`GeneratedAtRefused`. Naming the core absolutely would bind
    every verb in this column to ONE of those cores no matter which one imported
    it: a refusal raised here would then be an instance of a class the running
    `main`'s `except` clauses do not name, and it would escape as a traceback.
    `from . import cli` resolves against the package this module was imported
    under, so the column always reaches the very core that is running it."""
    from . import cli

    return cli


def cmd_gate_demote(args: argparse.Namespace) -> int:
    """Reject / move a proposal back to staging — the mechanized reverse
    transition. Records the transition manifest, the executable plan, the
    register-update note, and the gate-action record; with `--execute` it also
    applies the moves to this checkout (the human-driven transition)."""
    repo_root, snapshot = _core()._gate_snapshot(args)
    console = gate_mod.GateConsole(_core()._human_gate(repo_root, args), records_dir=args.records_dir)
    res = console.demote(snapshot, args.change_id, reason=args.reason,
                         staging_topic=args.staging_topic,
                         provenance=_core().cli_provenance())
    print(f"demote {args.change_id} → staging topic {res.plan.staging_topic!r} (by {args.actor})")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    print(f"  transition manifest: {res.manifest_path.relative_to(repo_root)}")
    print(f"  executable plan:     {res.plan_path.relative_to(repo_root)}")
    print(f"  register-update:     {res.register_update_path.relative_to(repo_root)}")
    print(f"  planned moves: {len(res.plan.moves)}; withdrawn picks: {list(res.plan.withdrawn_picks)}")
    if args.execute:
        executed_at = gate_mod._utcnow()
        try:
            ex = gate_mod.execute_demotion_plan(
                res.plan, repo_root, at=executed_at)
        except (gate_mod.GateRefused, OSError, UnicodeError) as exc:
            print(
                "  DEMOTION EXECUTION FAILED; no executed receipt was written. "
                f"Inspect the planned destinations for partial filesystem work: {exc}",
                file=sys.stderr)
            return 1
        try:
            receipt_path = gate_mod.write_demotion_execution_receipt(
                _core()._human_gate(repo_root, args), res, ex, at=executed_at,
                records_dir=args.records_dir)
        except (gate_mod.GateRefused, BoundaryViolation, OSError) as exc:
            print(
                "  DEMOTION EXECUTED BUT RECEIPT NOT WRITTEN. Returned material "
                "has already moved; repair the receipt failure before treating "
                f"this demotion as cleanup evidence: {exc}", file=sys.stderr)
            print(f"  moved: {ex.moved}", file=sys.stderr)
            print(f"  change folder removed: {ex.removed_change_folder}",
                  file=sys.stderr)
            return 1
        # Not every move lands in openspec/ — supporting-docs restores and the
        # outline restore (below) can land in the topic ROOT instead, so the
        # summary counts both rather than naming a single destination
        # (Copilot review, PR #215).
        into_ws = sum(1 for _, to in ex.moved
                      if to.startswith(res.plan.openspec_workspace + "/"))
        into_root = len(ex.moved) - into_ws
        print(f"  EXECUTED: {len(ex.moved)} file(s) moved back into {res.plan.topic_path}/ "
              f"({into_ws} into openspec/, {into_root} into the topic root); "
              f"README+INDEX updated; change folder removed={ex.removed_change_folder}")
        print(f"  execution receipt: {receipt_path.relative_to(repo_root)}")
        # THE OUTLINE'S OWN SENTENCE (align-demote-to-round-trip-rule). "We did not
        # overwrite your work" is exactly the sentence a human needs to be able to
        # check, and a disposition recorded only in a returned dataclass is a
        # disposition nobody reads. It goes to the operator who ran the verb.
        if ex.outline_path is not None:
            print(f"  outline: {ex.outline_path.relative_to(repo_root)} "
                  f"(snapshot {ex.snapshot_disposition})")
            if ex.preserved_snapshot_path is not None:
                print(f"    your fragment already existed and differed, so it was "
                      f"REFRESHED IN PLACE — the change folder's snapshot was "
                      f"preserved as "
                      f"{ex.preserved_snapshot_path.relative_to(repo_root)}, "
                      f"not applied over your work")
            if ex.outline_refusal:
                print(f"    REFRESH WITHHELD: {ex.outline_refusal}")
    else:
        print("  (plan only — rerun with --execute to apply the moves to this checkout)")
    return 0


def cmd_gate_ratify(args: argparse.Namespace) -> int:
    """Approve a proposal: write the ratification record (ratifier, date) + a
    register-update note; the gate-action record carries the ratification-record
    reference (schema contains-rule)."""
    repo_root = Path(args.repo_root).resolve()
    console = gate_mod.GateConsole(_core()._human_gate(repo_root, args), records_dir=args.records_dir)
    res = console.ratify(args.change_id, args.ratifier or args.actor, date=args.date,
                         provenance=_core().cli_provenance())
    print(f"ratify {args.change_id} (ratifier {res.ratification['ratifier']}, {res.ratification['date']})")
    print(f"  gate-action record:  {res.record_path.relative_to(repo_root)}")
    print(f"  ratification record: {res.ratification_path.relative_to(repo_root)}")
    print(f"  register-update:     {res.register_update_path.relative_to(repo_root)}")
    return 0


def cmd_gate_promote_to_staging(args: argparse.Namespace) -> int:
    """Commission the organization of an ACCEPTED possible into a staging
    fragment. Refuses (exit 1) an absent register id, a possible that is not
    promotable, and a duplicate undelivered commission. Writes NOTHING to the
    possibles register: the pick edge lands when the fragment is delivered."""
    return _core()._commission_cli("promote-to-staging", args, args.possible_id,
                                   topic=args.topic)


def cmd_gate_research_brief(args: argparse.Namespace) -> int:
    """Commission a pre-verdict evidence brief for a possible. Legal while the
    possible is undisposed AND after — the engine carries no state guard
    (FR-018a); it never disposes the possible or edits its entry."""
    return _core()._commission_cli("research-brief", args, args.possible_id)


def cmd_gate_derive_possibles(args: argparse.Namespace) -> int:
    """Commission a cluster-scoped run of the ratified derivation lane. The
    cluster is validated against the SNAPSHOT (hence the snapshot args); the
    console derives nothing and creates no register entry."""
    repo_root, snapshot = _core()._gate_snapshot(args)
    args.repo_root = str(repo_root)
    return _core()._commission_cli("derive-possibles", args, args.cluster_id,
                                   snapshot=snapshot)


def cmd_gate_create_project(args: argparse.Namespace) -> int:
    """Commission a project-register edit creating one project
    (add-project-scoped-selection). The register is aggregation-owned: this
    records the edit (descriptor + gate-action record) and never performs it.
    The target project id is slugged from the name; refusals (exit 1) cover
    an unreachable register, an id collision, a member outside the register's
    repository universe, and a duplicate undelivered commission. A member
    already in another project is legal — membership is multi-parent
    (Brett's 2026-08-06 ruling)."""
    repo_root = Path(args.repo_root).resolve()
    console = gate_mod.GateConsole(_core()._human_gate(repo_root, args),
                                   records_dir=args.records_dir)
    try:
        res = console.create_project(
            args.name, repositories=args.repo,
            register_source=args.project_register,
            outline=args.outline, workflow=args.workflow, note=args.note)
    except (gate_mod.GateRefused, BoundaryViolation) as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1
    print(f"create-project {res.job['project_id']} ({args.name}) commissioned "
          f"(by {res.gate_action_record['actor']})")
    print(f"  members: {', '.join(res.job['repositories'])}")
    print(f"  workflow-job descriptor: {res.job_path.relative_to(repo_root)}")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    return 0


def cmd_gate_edit_project(args: argparse.Namespace) -> int:
    """Commission a membership edit of one existing project
    (add-opendox-project-header). Records the edit (descriptor with the
    add/remove lists + gate-action record) and never performs it."""
    repo_root = Path(args.repo_root).resolve()
    console = gate_mod.GateConsole(_core()._human_gate(repo_root, args),
                                   records_dir=args.records_dir)
    try:
        res = console.edit_project(
            args.project_id, add=args.add or [], remove=args.remove or [],
            register_source=args.project_register,
            outline=args.outline, workflow=args.workflow, note=args.note)
    except (gate_mod.GateRefused, BoundaryViolation) as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1
    print(f"edit-project {args.project_id} commissioned "
          f"(by {res.gate_action_record['actor']})")
    if res.job["add"]:
        print(f"  add: {', '.join(res.job['add'])}")
    if res.job["remove"]:
        print(f"  remove: {', '.join(res.job['remove'])}")
    print(f"  workflow-job descriptor: {res.job_path.relative_to(repo_root)}")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    return 0


def cmd_gate_dispose_possible(args: argparse.Namespace) -> int:
    """Dispose a pending_review ai-derived possible: the ONE human verdict the
    derivation lane's whole contract funnels toward. Writes the updated index
    (validated by the pinned validator BEFORE persistence), its `.md`
    projection, and the gate-action record. `--repo-root` is the pinned
    openxFactory checkout (where `ideation/cross-reference.yaml` lives)."""
    from doc_health import derive_possibles as dp
    repo_root = Path(args.repo_root).resolve()
    gate = HumanGate(
        repo_root,
        [args.records_dir, dp.INDEX_REL, dp.INDEX_MD_REL],
        human_actor=_core()._gate_actor(repo_root, args))
    console = gate_mod.GateConsole(gate, records_dir=args.records_dir)
    res = console.dispose_possible(
        args.possible_id, args.outcome, reason=args.reason,
        citation=args.citation, note=args.note, provenance=_core().cli_provenance())
    entry = res.entry
    print(f"dispose-possible {res.possible_id} -> {res.outcome} "
          f"(state {entry.get('state')}, origin {entry.get('origin')})")
    print(f"  index:              {res.index_path.relative_to(repo_root)}")
    if res.index_md_path:
        print(f"  index projection:   {res.index_md_path.relative_to(repo_root)}")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    print("  (commit + push the openxFactory checkout to publish; the next")
    print("   snapshot regeneration folds the disposition into the dashboard)")
    return 0


def cmd_gate_edit_apply(args: argparse.Namespace) -> int:
    """Apply a HUMAN-approved redline to a change document. The redline is read
    from files (never re-authored here) so the console applies exactly what the
    human supplies."""
    repo_root = Path(args.repo_root).resolve()
    if args.full_text_file:
        redline = gate_mod.Redline(
            full_text=Path(args.full_text_file).read_text(encoding="utf-8"), concept=args.concept)
    elif args.old_file and args.new_file:
        redline = gate_mod.Redline(
            old_text=Path(args.old_file).read_text(encoding="utf-8"),
            new_text=Path(args.new_file).read_text(encoding="utf-8"), concept=args.concept)
    else:
        print("edit-apply requires either --full-text-file or both --old-file and --new-file", file=sys.stderr)
        return 2
    console = gate_mod.GateConsole(_core()._human_gate(repo_root, args), records_dir=args.records_dir)
    try:
        res = console.edit_apply(args.change_id, args.document, redline,
                                 tree_root=repo_root, provenance=_core().cli_provenance())
    except BoundaryViolation as exc:
        # The confinement refusal (a `--document` that escapes the permitted
        # root) reaches the human as a REFUSAL and a non-zero exit, not a
        # traceback — and never as a silently corrected path.
        print(f"edit-apply refused: {exc.refusal.report()}", file=sys.stderr)
        return 1
    print(f"edit-apply {args.document} ({redline.form()}) by {args.actor}")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    print(f"  redline artifact:   {res.redline_path.relative_to(repo_root)}")
    return 0


def cmd_gate_propose(args: argparse.Namespace) -> int:
    """Commission proposal authoring for a staging topic (add-propose-verb):
    the recorded workflow-job dispatch + gate-action record. Refuses (exit 1)
    a missing topic, a duplicate undelivered commission, a topic that is not
    `ready`, and — 007-workbench-branch-sessions T054, FR-023 — a tile whose BRANCH
    SESSION is still live. The authoring runs externally and lands as an ordinary
    OpenSpec change.

    The session refusal needs a registry, and a CLI verb is a FRESH PROCESS whose
    registry starts empty, so this re-derives it through `_session_registry`
    (T033a) before asking: without that, a CLI `propose` would proceed over
    unmerged drafts, which is the exact hazard D15 exists to prevent."""
    repo_root = Path(args.repo_root).resolve()
    console = gate_mod.GateConsole(_core()._human_gate(repo_root, args), records_dir=args.records_dir)
    # The registry key's repository half, through the SAME derivation the session
    # verbs use (`_session_repository_key`) — this verb only READS liveness, but it
    # has to read it under the key the session was opened with or FR-023's refusal
    # simply does not fire.
    repository = _core()._session_repository_key(repo_root, args)
    try:
        res = console.propose(
            args.topic_id, outline=args.outline, workflow=args.workflow,
            note=args.note,
            session_precondition=gate_routes_mod.session_precondition_for(
                _core()._session_registry(repo_root, repository), repository=repository,
                topic_id=args.topic_id,
                tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root)),
            provenance=_core().cli_provenance())
    except branch_session_mod.SessionRefused as exc:   # a live branch session
        print(f"propose refused: {exc.report()}", file=sys.stderr)
        return 1
    except gate_mod.GateRefused as exc:
        print(f"propose refused: {exc}", file=sys.stderr)
        return 1
    print(f"propose {args.topic_id} → workflow {res.job['workflow']!r} "
          f"(status {res.job['status']}, by {args.actor})")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    print(f"  workflow-job:       {res.job_path.relative_to(repo_root)}")
    return 0


def cmd_gate_kickoff(args: argparse.Namespace) -> int:
    """Dispatch a ratified change's next step as a recorded, gated workflow job.
    Refuses (exit 1) a change with no recorded ratification (D17). The workflow
    itself runs externally; this records the dispatch descriptor only."""
    repo_root, snapshot = _core()._gate_snapshot(args)
    console = gate_mod.GateConsole(_core()._human_gate(repo_root, args), records_dir=args.records_dir)
    try:
        res = console.kickoff(args.change_id, snapshot=snapshot,
                              outline=args.outline, workflow=args.workflow,
                              provenance=_core().cli_provenance())
    except gate_mod.GateRefused as exc:
        print(f"kickoff refused: {exc}", file=sys.stderr)
        return 1
    print(f"kickoff {args.change_id} → workflow {res.job['workflow']!r} "
          f"(status {res.job['status']}, by {args.actor})")
    print(f"  gate-action record: {res.record_path.relative_to(repo_root)}")
    print(f"  workflow-job:       {res.job_path.relative_to(repo_root)}")
    return 0


def cmd_gate_lens_save_recipe(args: argparse.Namespace) -> int:
    """Save a keyword-lens recipe as a gitignored workbench manifest through the
    gate — the same recorded dispatch the dashboard's execute button posts. The
    recipe is re-evaluated against the freshly generated snapshot; the reasoned-
    override guard, duplicate-name refusal, and schema validation all fire in
    the engine and surface here (exit 1)."""
    repo_root, snapshot = _core()._gate_snapshot(args)
    try:
        result = gate_routes_mod.execute_lens_save_recipe(
            _core()._lens_gate(repo_root, args),
            repository=args.repository, name=args.name,
            checked=list(args.checked), pinned=list(args.pinned or []),
            snapshot=snapshot,
            includes=_core()._parse_pairs(args.include, "--include"),
            excludes=_core()._parse_pairs(args.exclude, "--exclude"),
            records_dir=args.records_dir, provenance=_core().cli_provenance())
    except (workbench_mod.WorkbenchError, workbench_mod.ManifestInvalid) as exc:
        print(f"lens-save-recipe refused: {exc}", file=sys.stderr)
        return 1
    print(f"lens-save-recipe {args.name!r} → {result['members']} member(s) (by {args.actor})")
    print(f"  manifest:           {result['manifest']}")
    print(f"  gate-action record: {result['record']}")
    return 0


def cmd_gate_lens_add_as_cluster(args: argparse.Namespace) -> int:
    """Add a keyword-lens set as a cluster: the recipe-seeded manifest PLUS the
    pending_review human-seen submission into the cross-reference queue. The
    evidence contract is enforced BEFORE persistence; the generated index is
    never written (acceptance stays a governed human edit)."""
    repo_root, snapshot = _core()._gate_snapshot(args)
    submission = human_seen_mod.HumanSeenSubmission(
        proposer=args.proposer or args.actor,
        repository=args.evidence_repository or args.repository,
        path=args.evidence_path or "",
        revision=args.revision or "",
        section=args.section or "",
        passage_sha256=args.passage_sha256 or "",
        rationale=args.rationale or "",
        confidence=args.confidence,
        alternatives=list(args.alternative or []),
        recipe_reference=args.recipe_reference)
    try:
        result = gate_routes_mod.execute_lens_add_as_cluster(
            _core()._lens_gate(repo_root, args),
            repository=args.repository, name=args.name,
            checked=list(args.checked), pinned=list(args.pinned or []),
            snapshot=snapshot,
            includes=_core()._parse_pairs(args.include, "--include"),
            excludes=_core()._parse_pairs(args.exclude, "--exclude"),
            submission=submission, records_dir=args.records_dir,
            provenance=_core().cli_provenance())
    except (human_seen_mod.SubmissionRefused, human_seen_mod.SubmissionInvalid,
            workbench_mod.WorkbenchError, workbench_mod.ManifestInvalid) as exc:
        print(f"lens-add-as-cluster refused: {exc}", file=sys.stderr)
        return 1
    print(f"lens-add-as-cluster {args.name!r} → cluster {result['cluster_id']} (by {args.actor})")
    print(f"  manifest:           {result['manifest']}")
    print(f"  pending entry:      {result['pending_entry']}")
    print(f"  gate-action record: {result['record']}")
    return 0


def cmd_gate_create_document(args: argparse.Namespace) -> int:
    """Create a NEW header-compliant ideation document through the GATE
    (add-workbench-bullseye-and-create) — the same recorded human dispatch the
    workbench's create dialog posts, driving the same tested authoring scaffold
    and writing the same gate-action record. Distinct from the non-gated
    `create` subcommand, which scaffolds + opens an editor and records nothing.
    Create-only: an existing target refuses (exit 1) and is never overwritten.

    With `--scope-kind` / `--scope-id` (007-workbench-branch-sessions T023a) the
    create resolves the tile's BRANCH SESSION first: the document and its record
    land in the session worktree and are committed together as that action's ONE
    commit, and the resulting sha is printed rather than written into the record.
    Without them, the behaviour is exactly what it was.

    FR-019 is a PER-VERB obligation here, and this verb is where it was missing:
    `create-document` was the ONE session subcommand that skipped
    `_session_identity_gate`, so a blank `--actor` reached `HumanGate` inside the
    try and died with an UNCAUGHT `ValueError` traceback — after the session had
    already been opened (PR #49 review finding 3). The gate now runs FIRST, ahead
    of the registry bootstrap and ahead of any resolution, exactly as every other
    session verb's does.

    The BODY is validated by the route's own `parse_create_document_body`, not by
    a second CLI-shaped approximation: the two surfaces drive the same engine, so
    an `--area` the HTTP route refuses must not be committable here."""
    repo_root = Path(args.repo_root).resolve()
    refused = _core()._session_identity_gate("create-document", repo_root, args)
    if refused is not None:
        return refused
    scope_kind = getattr(args, "scope_kind", None)
    scope_id = getattr(args, "scope_id", None)
    if bool(scope_kind) != bool(scope_id):
        print("create-document refused: --scope-kind and --scope-id are given "
              "together or not at all — one without the other names no tile, so "
              "no branch session can be resolved from it", file=sys.stderr)
        return 1
    parsed, message = gate_routes_mod.parse_create_document_body({
        "area": args.area, "title": args.title, "summary": args.summary,
        "topics": [t.strip() for t in (args.topics or "").split(",") if t.strip()],
        "repository_context": args.repository_context, "kind": args.kind,
        "status": args.status, "source": args.source,
        "possible_feats": list(args.possible_feat or []),
        "scope_kind": scope_kind, "scope_id": scope_id,
        "continuation": getattr(args, "continuation", None),
    })
    if message is not None:
        print(f"create-document refused: {message}", file=sys.stderr)
        return 1
    parsed.pop("_scope", None)
    continuation = parsed.pop("_continuation", None)
    session = git = None
    # The registry/notebook key, through the ONE derivation every session verb
    # uses (`_session_repository_key`). It is NOT `--repository-context`, which is
    # a document header field: keying the open off a header value made
    # `create-document` disagree with the verbs that end the session it opened (PR
    # #49 review finding 8, leg b).
    repository = _core()._session_repository_key(repo_root, args)
    try:
        session, git = gate_routes_mod.resolve_session(
            (scope_kind, scope_id), checkout_root=repo_root,
            registry=(_core()._session_registry(repo_root, repository)
                      if scope_kind else None),
            repository=repository,
            records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root),
            verb="create-document",
            # the human's answer to the FR-025 resume-or-new report, when they have
            # been shown it (T056); absent, a surviving abandoned branch reports the
            # choice instead of having one made for it
            continuation=continuation,
            # the ONE verb that can open a session carries the notebook adapter
            # (T074, FR-036) — the notebook itself is created by the first
            # SUCCESSFUL commit, never by the open (finding 3)
            notebook=_core()._notebook_port(repo_root) if scope_kind else None)
        gate_root = session.worktree if session is not None else repo_root
        result = gate_routes_mod.execute_create_document(
            HumanGate(gate_root, [args.records_dir], human_actor=args.actor),
            records_dir=args.records_dir, session=session, git=git,
            # THE GATEWAY FACT (D23): surface `cli`, and the proof
            # `_session_identity_gate` above already required — a tty, or an
            # explicit `XF_HUMAN_CONSOLE` declaration. Observed HERE, where it is
            # known, and never re-derived by the engine.
            provenance=_core().cli_provenance(), **parsed)
    # THE OPEN IS INSIDE THE CREATE'S FAILURE DOMAIN (finding 3): every refusal
    # below can arrive after `resolve_session` opened a branch, a worktree, a live
    # registry entry and a snapshot. `_unwind_cli_session` ends a session THIS
    # invocation opened and leaves a JOINED one exactly as it was.
    except BoundaryViolation as exc:          # existing target (create-only), etc.
        return _core()._unwind_cli_session("create-document", session, git, repo_root,
                                           exc.refusal.report())
    except gate_mod.GateRefused as exc:
        return _core()._unwind_cli_session("create-document", session, git, repo_root,
                                           str(exc))
    except branch_session_mod.SessionRefused as exc:   # collision, live proposal
        return _core()._unwind_cli_session("create-document", session, git, repo_root,
                                           exc.report())
    except session_git_mod.SessionGitRefused as exc:   # a STRUCTURAL git refusal
        return _core()._unwind_cli_session("create-document", session, git, repo_root,
                                           str(exc))
    except session_git_mod.GitError as exc:            # git's own reason, verbatim
        return _core()._unwind_cli_session("create-document", session, git, repo_root,
                                           str(exc))
    except OSError as exc:                    # unwritable area, bad path
        return _core()._unwind_cli_session("create-document", session, git, repo_root,
                                           f"the create could not be written: {exc}")
    print(f"create-document {result['path']} "
          f"(status {result['status']}, by {args.actor})")
    print(f"  document:           {result['path']}")
    print(f"  gate-action record: {result['record']}")
    if result.get("ref"):
        print(f"  session branch:     {result['ref']}"
              f"{' (joined)' if result.get('joined') else ''}")
        print(f"  commit:             {result['commit']}")
    if result.get("notebook_notice"):
        # FR-042: a NOTIFICATION, not a failure — stderr so it cannot be mistaken
        # for part of the created document's report, exit code still 0
        print(f"  session note:       {result['notebook_notice']}", file=sys.stderr)
    return 0


def cmd_gate_edit_document(args: argparse.Namespace) -> int:
    """Rewrite an EXISTING document inside the tile's branch session
    (007-workbench-branch-sessions T043, FR-015/FR-020) — the CLI parity surface
    of `POST /actions/gate/edit-document`, driving the SAME engine.

    Session-ONLY: with no live session on the tile this refuses and names
    `edit-apply`, the main-resident redline path, which is untouched by this
    feature (FR-017). The replacement arrives as `--content-file` rather than
    inline text so a shell cannot mangle a document, and the whole action is ONE
    commit on the session branch carrying the document and its gate-action record.

    FR-019 is a PER-VERB obligation here: a CLI verb is a FRESH PROCESS with no
    `serve.py` handler in front of it, so this function constructs the HumanGate
    and requires it ITSELF — before the content file is read and before any
    session is resolved — and re-derives the process's session registry through
    `_session_registry` (T033a), without which a CLI verb would see no session at
    all."""
    repo_root = Path(args.repo_root).resolve()
    # The IDENTITY gate, run first and purely to enforce FR-019 ahead of every
    # read and every resolution — through the SHARED `_session_identity_gate`, so
    # this verb cannot drift from its four siblings on any of the three clauses
    # (it used to construct its own gate inline and therefore missed the
    # agent/automation clause when that clause arrived; PR #49 finding 2). The
    # WRITING gate is a second one, rooted at (and declaring) the worktree once
    # the session is known — that declaration is what unlocks the narrow rewrite
    # allowance at all (T026).
    refused = _core()._session_identity_gate("edit-document", repo_root, args)
    if refused is not None:
        return refused
    try:
        content = Path(args.content_file).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"edit-document refused: the replacement could not be read: {exc}",
              file=sys.stderr)
        return 1
    # The registry key's repository half, DERIVED so the contract's flag surface
    # stays as short as it reads: the checkout directory name IS the repository
    # name by the same convention `branch_session.container_root` already relies
    # on (`<repo>` beside `<repo>-worktrees/`, FR-005/R7). The registry is
    # per-PROCESS, so all that is required is that the bootstrap below and the
    # resolution beside it agree — and `--repository` overrides both together for
    # a checkout whose directory is named something else.
    repository = _core()._session_repository_key(repo_root, args)
    try:
        session, git = gate_routes_mod.resolve_session(
            (args.scope_kind, args.scope_id), checkout_root=repo_root,
            registry=_core()._session_registry(repo_root, repository),
            repository=repository, records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root),
            verb="edit-document", require_live=True,
            remedy=gate_routes_mod.EDIT_REMEDY)
        result = gate_routes_mod.execute_edit_document(
            HumanGate(session.worktree, [args.records_dir],
                      human_actor=args.actor, session_root=session.worktree),
            document=args.document, content=content, notes=args.notes,
            records_dir=args.records_dir, session=session, git=git,
            # the SERVED checkout: the base this session branched from, and
            # therefore the engine's answer to "did THIS session create this
            # document, or does it belong to another tile" (T092 defect 1)
            checkout_root=repo_root,
            provenance=_core().cli_provenance())
    except branch_session_mod.SessionRefused as exc:   # no session, collision, …
        print(f"edit-document refused: {exc.report()}", file=sys.stderr)
        return 1
    except BoundaryViolation as exc:          # confinement, absent target, delete
        print(f"edit-document refused: {exc.refusal.report()}", file=sys.stderr)
        return 1
    except gate_mod.GateRefused as exc:
        print(f"edit-document refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.SessionGitRefused as exc:   # a STRUCTURAL git refusal
        print(f"edit-document refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.GitError as exc:   # git's own reason, verbatim
        print(f"edit-document refused: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:                    # unreadable staging tree / target
        print(f"edit-document refused: {exc}", file=sys.stderr)
        return 1
    print(f"edit-document {result['document']} (by {args.actor})")
    print(f"  session branch:     {result['ref']}")
    print(f"  commit:             {result['commit']}")
    print(f"  gate-action record: {result['record']}")
    return 0


def cmd_gate_open_pr(args: argparse.Namespace) -> int:
    """Push the tile's session branch and open (or update) its pull request
    (007-workbench-branch-sessions T065, FR-029/FR-032/FR-020) — the CLI parity
    surface of `POST /actions/gate/open-pr`, driving the SAME engine.

    The remote write uses the invoking engineer's own ambient `gh` authentication
    (FR-034, D22): a missing or invalid `gh` auth is reported VERBATIM as the
    engine's refusal, because a paraphrase of an auth failure cannot be acted on.

    NO readiness signal of either kind is consulted (FR-031, D21), the verb merges
    and approves nothing (FR-030), and the gate-action record is MAIN-RESIDENT so it
    outlives the branch the merge deletes (FR-029). If the branch has ALREADY
    merged, this ends the session instead of pushing it again (FR-033).

    FR-019 is a PER-VERB obligation here: a CLI verb is a FRESH PROCESS with no
    `serve.py` handler in front of it, so the identity gate runs FIRST — before the
    body file is read and before any session is resolved."""
    repo_root = Path(args.repo_root).resolve()
    refused = _core()._session_identity_gate("open-pr", repo_root, args)
    if refused is not None:
        return refused
    body = None
    if args.body_file:
        try:
            body = Path(args.body_file).read_text(encoding="utf-8")
        except OSError as exc:
            print(f"open-pr refused: the pull-request body could not be read: "
                  f"{exc}", file=sys.stderr)
            return 1
    repository = _core()._session_repository_key(repo_root, args)
    try:
        session, git = gate_routes_mod.resolve_session(
            (args.scope_kind, args.scope_id), checkout_root=repo_root,
            registry=_core()._session_registry(repo_root, repository),
            repository=repository, records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root),
            verb="open-pr", require_live=True,
            remedy=gate_routes_mod.OPEN_PR_REMEDY)
        result = gate_routes_mod.execute_open_pr(
            HumanGate(repo_root, [args.records_dir], human_actor=args.actor),
            git, session=session, pull_requests=_core()._pull_request_port(repo_root),
            records_dir=args.records_dir, checkout_root=repo_root,
            title=args.title, body=body, provenance=_core().cli_provenance(),
            # retire-at-teardown on the MERGE ending too (T074): before Phase 8
            # the CLI declared no adapter and reported honestly that there was no
            # notebook to retire — now both surfaces have one (FR-021, D16)
            notebook=_core()._notebook_port(repo_root))
    except branch_session_mod.SessionRefused as exc:   # no session, live proposal
        print(f"open-pr refused: {exc.report()}", file=sys.stderr)
        return 1
    except BoundaryViolation as exc:
        print(f"open-pr refused: {exc.refusal.report()}", file=sys.stderr)
        return 1
    except gate_mod.GateRefused as exc:
        print(f"open-pr refused: {exc}", file=sys.stderr)
        return 1
    except session_pr_mod.PullRequestRefused as exc:   # `gh`'s own words, verbatim
        print(f"open-pr refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.GitError as exc:            # git's own reason, verbatim
        print(f"open-pr refused: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"open-pr refused: {exc}", file=sys.stderr)
        return 1
    if result.get("merged"):
        print(f"open-pr {result['ref']} had already MERGED — the session ended "
              f"(by {args.actor})")
        print(f"  torn down:          {', '.join(result['torn_down']) or '(nothing)'}")
        print("  branch:             "
              f"{'DELETED' if result['branch_deleted'] else 'retained'} "
              f"({result['ref']})")
        for note in result.get("notes") or []:
            print(f"  session note:       {note}", file=sys.stderr)
        return 0
    print(f"open-pr {result['ref']} "
          f"({'updated' if result['updated'] else 'opened'}, by {args.actor})")
    print(f"  pull request:       {result['pull_request']}")
    print(f"  gate-action record: {result['record']}")
    # what this save did to the reviewer-facing TEXT (finding R2-13): "updated"
    # alone cannot distinguish a save that renamed the pull request from one that
    # left a human's description exactly as it was
    for note in result.get("notes") or []:
        print(f"  pull-request text:  {note}")
    return 0


def cmd_gate_share_session(args: argparse.Namespace) -> int:
    """Commit the session's dirty thread sidecars and PUSH the session branch, so
    a colleague can resume it (add-doxbench-editing-phase-b §12) — the CLI parity
    surface of `POST /actions/gate/share-session`, driving the SAME engine.

    It is `open-pr`'s sibling with the pull request removed, and it is the reason
    threads are local until a human says otherwise. It opens no pull request,
    requests no review, and holds no approval or merge authority.

    The remote write uses the invoking engineer's own ambient `gh` authentication
    (FR-034, D22) — the plane rule the Save already carries — so the port's own
    refusal is reported VERBATIM.

    FR-019 is a PER-VERB obligation here for the same reason it is on `open-pr`:
    a CLI verb is a fresh process with no `serve.py` handler in front of it."""
    repo_root = Path(args.repo_root).resolve()
    refused = _core()._session_identity_gate("share-session", repo_root, args)
    if refused is not None:
        return refused
    repository = _core()._session_repository_key(repo_root, args)
    try:
        session, git = gate_routes_mod.resolve_session(
            (args.scope_kind, args.scope_id), checkout_root=repo_root,
            registry=_core()._session_registry(repo_root, repository),
            repository=repository, records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root),
            verb="share-session", require_live=True,
            remedy=gate_routes_mod.SHARE_SESSION_REMEDY)
        result = gate_routes_mod.execute_share_session(
            gate_routes_mod.share_session_gate_factory(
                args.actor, args.records_dir),
            git, session=session, pull_requests=_core()._pull_request_port(repo_root),
            records_dir=args.records_dir, checkout_root=repo_root,
            notes=args.notes, provenance=_core().cli_provenance())
    except branch_session_mod.SessionRefused as exc:
        print(f"share-session refused: {exc.report()}", file=sys.stderr)
        return 1
    except BoundaryViolation as exc:
        print(f"share-session refused: {exc.refusal.report()}", file=sys.stderr)
        return 1
    except gate_mod.GateRefused as exc:
        print(f"share-session refused: {exc}", file=sys.stderr)
        return 1
    except session_pr_mod.PullRequestRefused as exc:   # `gh`'s own words, verbatim
        print(f"share-session refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.GitError as exc:
        print(f"share-session refused: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"share-session refused: {exc}", file=sys.stderr)
        return 1
    if not result.get("shared"):
        # Exit 0: "nothing new" is a correct answer, not a failure (§12.3).
        print(f"share-session {result['branch']}: {result['reason']}")
        return 0
    print(f"share-session {result['pushed_ref']} (by {args.actor})")
    print(f"  revision:           {result['revision']}")
    print(f"  threads committed:  "
          f"{', '.join(result['threads']) or '(none dirty)'}")
    print(f"  gate-action record: {result['record']} "
          f"({result['record_resident']}-resident)")
    print(f"  {result['promotion']}")
    return 0


def cmd_gate_abandon_session(args: argparse.Namespace) -> int:
    """End the tile's branch session WITHOUT saving, carrying the required reason
    (007-workbench-branch-sessions T053, FR-021/FR-022/FR-020) — the CLI parity
    surface of `POST /actions/gate/abandon-session`, driving the SAME engine.

    Tears down the worktree, the registry entry, and the session notebook, and
    deletes NOTHING: the branch, its pushed history, and any open pull request
    survive, and `branch_retained` is read back from git rather than assumed. The
    record is MAIN-RESIDENT — the served checkout's gate-records tree — because
    FR-028's cleanup deletes the branch and would take a branch-resident
    reason-record with it."""
    repo_root = Path(args.repo_root).resolve()
    refused = _core()._session_identity_gate("abandon-session", repo_root, args)
    if refused is not None:
        return refused
    repository = _core()._session_repository_key(repo_root, args)
    try:
        session, git = gate_routes_mod.resolve_session(
            (args.scope_kind, args.scope_id), checkout_root=repo_root,
            registry=_core()._session_registry(repo_root, repository),
            repository=repository, records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root),
            verb="abandon-session", require_live=True,
            remedy=gate_routes_mod.ABANDON_REMEDY)
        result = gate_routes_mod.execute_abandon_session(
            HumanGate(repo_root, [args.records_dir], human_actor=args.actor),
            git, session=session, reason=args.reason, notes=args.notes,
            records_dir=args.records_dir, checkout_root=repo_root,
            provenance=_core().cli_provenance(),
            # the session notebook is RETIRED at this ending too (T074, FR-021,
            # D16) — never re-pointed at `main`
            notebook=_core()._notebook_port(repo_root))
    except branch_session_mod.SessionRefused as exc:   # no session, live proposal
        print(f"abandon-session refused: {exc.report()}", file=sys.stderr)
        return 1
    except BoundaryViolation as exc:
        print(f"abandon-session refused: {exc.refusal.report()}", file=sys.stderr)
        return 1
    except gate_mod.GateRefused as exc:
        print(f"abandon-session refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.GitError as exc:            # git's own reason, verbatim
        print(f"abandon-session refused: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"abandon-session refused: {exc}", file=sys.stderr)
        return 1
    print(f"abandon-session {result['ref']} (by {args.actor})")
    print(f"  reason:             {result['reason']}")
    print(f"  torn down:          {', '.join(result['torn_down']) or '(nothing)'}")
    print("  branch:             "
          f"{'RETAINED' if result['branch_retained'] else 'gone'} "
          f"({result['ref']})")
    print(f"  gate-action record: {result['record']}")
    # An OPEN pull request this ending does not close (FR-022, G9) is named, and so
    # is the FR-029 record finalized for it — the custody gap critic finding C6
    # found was silent on both counts.
    if result.get("pull_request"):
        print(f"  pull request:       OPEN, {result['pull_request']} "
              "(this verb closes none)")
    if result.get("dispatch_record"):
        print(f"  dispatch record:    {result['dispatch_record']} "
              "(finalized from the pending-dispatch marker)")
    for note in result.get("notes") or []:
        print(f"  session note:       {note}", file=sys.stderr)
    return 0


def cmd_gate_cleanup_abandoned_branch(args: argparse.Namespace) -> int:
    """Delete an ABANDONED session's surviving branch after durable retention
    release (007-workbench-branch-sessions T056, FR-028/FR-020).

    HUMAN-INVOKED, always: nothing automatic ever calls this, and a `propose`
    DISPATCH is explicitly not enough — the commissioned authoring may never
    deliver a proposal, and the abandoned branch is the only surviving evidence of
    that exploration until it does."""
    repo_root = Path(args.repo_root).resolve()
    refused = _core()._session_identity_gate("cleanup-abandoned-branch", repo_root, args)
    if refused is not None:
        return refused
    repository = _core()._session_repository_key(repo_root, args)
    superseding_references = tuple(args.superseding_reference or ())
    if any(not str(reference).strip() for reference in superseding_references):
        print("cleanup-abandoned-branch refused: every --superseding-reference "
              "must be nonblank", file=sys.stderr)
        return 1
    try:
        result = gate_routes_mod.execute_cleanup_abandoned_branch(
            HumanGate(repo_root, [args.records_dir], human_actor=args.actor),
            session_git_mod.SessionGit(repo_root),
            tile=branch_session_mod.Tile(args.scope_kind, args.scope_id),
            ref=args.ref, registry=_core()._session_registry(repo_root, repository),
            repository=repository, checkout_root=repo_root,
            records_dir=args.records_dir,
            tile_inventory=gate_routes_mod.discover_tile_inventory(repo_root),
            retention_release_reason=args.retention_release_reason,
            superseding_references=tuple(
                str(reference).strip() for reference in superseding_references),
            provenance=_core().cli_provenance())
    except branch_session_mod.SessionRefused as exc:
        print(f"cleanup-abandoned-branch refused: {exc.report()}", file=sys.stderr)
        return 1
    except BoundaryViolation as exc:
        print(f"cleanup-abandoned-branch refused: {exc.refusal.report()}",
              file=sys.stderr)
        return 1
    except session_git_mod.SessionGitRefused as exc:
        print(f"cleanup-abandoned-branch refused: {exc}", file=sys.stderr)
        return 1
    except session_git_mod.GitError as exc:
        print(f"cleanup-abandoned-branch refused: {exc}", file=sys.stderr)
        return 1
    except gate_mod.GateRefused as exc:
        print(f"cleanup-abandoned-branch refused: {exc}", file=sys.stderr)
        return 1
    except (OSError, UnicodeError) as exc:
        print(f"cleanup-abandoned-branch refused: {exc}", file=sys.stderr)
        return 1
    print(f"cleanup-abandoned-branch {result['ref']} deleted (by {args.actor})")
    # What was VERIFIED, not what ought to exist: the line used to assert that "the
    # abandon record on `main` survives it" whether or not any abandon had ever
    # happened (PR #49 second-review finding 3).
    print(f"  the abandon this ends was verified first: {result['abandon_proof']}")
    print(f"  pre-delete head:     {result['pre_delete_head']}")
    print(f"  retention release:   {result['retention_release']['kind']}")
    print(f"  gate-action record:  {result['record']}")
    return 0


def _add_gate_identity_args(sub: argparse.ArgumentParser) -> None:
    """Identity + records location shared by EVERY gate action. `--actor` is the
    CLAIMED human identity and is AUTHENTICATED against the deployment's trusted
    principal before any record is written (`actor_identity`); an unverifiable
    claim is refused, never recorded."""
    sub.add_argument("--repo-root", required=True, help="the pinned checkout root")
    sub.add_argument("--actor", required=True,
                     help="the acting human's identity, checked against the "
                          "authenticated principal (gateway user, "
                          f"${actor_mod.PRINCIPAL_ENV}, ${actor_mod.ROSTER_ENV}/"
                          f"${actor_mod.ALLOWLIST_ENV}, or the checkout's git "
                          "identity) and recorded in the gate-action record")
    sub.add_argument("--records-dir", default=gate_mod.DEFAULT_RECORDS_DIR,
                     help=f"records output directory (default: {gate_mod.DEFAULT_RECORDS_DIR})")


def _add_gate_snapshot_args(sub: argparse.ArgumentParser) -> None:
    """Snapshot-generation args for the actions that plan against the snapshot
    (demote, kickoff)."""
    sub.add_argument("--repository", required=True, help="canonical repository id for the snapshot")
    sub.add_argument("--source-revision", default=None, help="pin the source_revision anchor (default: git HEAD)")
    sub.add_argument("--project-register", default=None, help="override the project-register source")
    sub.add_argument("--possibles", default=None, help="override the possibles-register source")


def _add_gate_subcommands(sub) -> None:
    gate = sub.add_parser("gate", help="human-only gate console actions (US9): demote / ratify / edit-apply / kickoff")
    gsub = gate.add_subparsers(dest="gate_command", required=True)

    demote = gsub.add_parser(
        "demote",
        help="reject a proposal back to staging (mechanized reverse transition); "
             "peer of the executing dashboard route POST /actions/gate/demote, which "
             "PLANS and RECORDS only \u2014 this command is the only surface that can "
             "also --execute the recorded plan")
    _add_gate_identity_args(demote)
    _add_gate_snapshot_args(demote)
    demote.add_argument("--change-id", required=True, help="the change to demote")
    demote.add_argument("--reason", required=True, help="the required reason a change went back to staging")
    demote.add_argument("--staging-topic", default=None,
                        help="target staging topic (default: the change's recorded origin staging id)")
    demote.add_argument("--execute", action="store_true",  # unreachable from the dashboard route by design (NG-005)
                        help="apply the moves to this checkout (default: emit the plan only)")
    demote.set_defaults(func=cmd_gate_demote)

    ratify = gsub.add_parser("ratify", help="approve a proposal (write the ratification record + register update)")
    _add_gate_identity_args(ratify)
    ratify.add_argument("--change-id", required=True, help="the change to ratify")
    ratify.add_argument("--ratifier", default=None, help="the ratifying authority (default: --actor)")
    ratify.add_argument("--date", default=None, help="ratification date YYYY-MM-DD (default: today)")
    ratify.set_defaults(func=cmd_gate_ratify)

    edit = gsub.add_parser("edit-apply", help="apply a HUMAN-approved redline to a change document")
    _add_gate_identity_args(edit)
    edit.add_argument("--change-id", required=True, help="the change owning the document")
    edit.add_argument("--document", required=True, help="repo-relative path of the change document to revise")
    edit.add_argument("--old-file", default=None, help="file holding the exact block to replace (replacement-block form)")
    edit.add_argument("--new-file", default=None, help="file holding the replacement block")
    edit.add_argument("--full-text-file", default=None, help="file whose contents replace the whole document (full-text form)")
    edit.add_argument("--concept", default=None, help="the listed concept this redline revises (optional)")
    edit.set_defaults(func=cmd_gate_edit_apply)

    dispose = gsub.add_parser(
        "dispose-possible",
        help="dispose a pending_review ai-derived possible (accept / reject / defer)")
    _add_gate_identity_args(dispose)
    dispose.add_argument("--possible-id", required=True,
                         help="the possibles-register entry id (pos-derived-...)")
    dispose.add_argument("--outcome", required=True,
                         choices=("accepted", "rejected", "deferred"),
                         help="the human verdict (one-way; only deferred may be re-disposed)")
    dispose.add_argument("--reason", default=None,
                         help="REQUIRED with --outcome rejected: the durable why")
    dispose.add_argument("--citation", default=None,
                         help="REQUIRED with --outcome rejected: what the rejection cites")
    dispose.add_argument("--note", default=None, help="optional free-text note on the disposition")
    dispose.set_defaults(func=cmd_gate_dispose_possible)

    kick = gsub.add_parser("kickoff", help="dispatch a ratified change's next step (refused without ratification)")
    _add_gate_identity_args(kick)
    _add_gate_snapshot_args(kick)
    kick.add_argument("--change-id", required=True, help="the ratified change to kick off")
    kick.add_argument("--outline", default=None, help="the realization outline (default: a Speckit realization descriptor)")
    kick.add_argument("--workflow", default=kickoff_mod.DEFAULT_WORKFLOW, help="workflow id (default: speckit-realization)")
    kick.set_defaults(func=cmd_gate_kickoff)

    prop = gsub.add_parser("propose", help="commission proposal authoring for a staging topic (add-propose-verb)")
    _add_gate_identity_args(prop)
    prop.add_argument("--topic-id", required=True, help="the staging topic to take toward proposal (ideation/staging/<topic-id>/)")
    prop.add_argument("--outline", default=None, help="the authoring outline (default: a standard OpenSpec-change commission)")
    prop.add_argument("--workflow", default=kickoff_mod.DEFAULT_PROPOSAL_WORKFLOW,
                      help="workflow id (default: proposal-authoring)")
    prop.add_argument("--note", default=None, help="optional free-text note recorded on the action")
    prop.set_defaults(func=cmd_gate_propose)

    # ---- the wheel action-row commissions (011 add-wheel-action-verbs) ----
    # REQUIRED FLAGS, not positionals (plan decision P6): no gate subcommand in
    # this CLI takes a positional target, and consistency wins over the task
    # prose's shorthand.
    promote = gsub.add_parser(
        "promote-to-staging",
        help="commission a staging fragment for an ACCEPTED possible (add-wheel-action-verbs)")
    _add_gate_identity_args(promote)
    promote.add_argument("--possible-id", required=True,
                         help="the possibles-register id to promote")
    promote.add_argument("--topic", default=None,
                         help="optional proposed destination topic slug (the fulfilling step chooses when omitted)")
    promote.add_argument("--outline", default=None, help="the commissioning outline (default: a standard organize commission)")
    promote.add_argument("--workflow", default=kickoff_mod.DEFAULT_STAGING_FRAGMENT_WORKFLOW,
                         help=f"workflow id (default: {kickoff_mod.DEFAULT_STAGING_FRAGMENT_WORKFLOW})")
    promote.add_argument("--note", default=None, help="optional free-text note recorded on the action")
    promote.set_defaults(func=cmd_gate_promote_to_staging)

    brief = gsub.add_parser(
        "research-brief",
        help="commission a PRE-VERDICT evidence brief for a possible (add-wheel-action-verbs)")
    _add_gate_identity_args(brief)
    brief.add_argument("--possible-id", required=True,
                       help="the possibles-register id to research")
    brief.add_argument("--outline", default=None, help="the commissioning outline (default: a standard research commission)")
    brief.add_argument("--workflow", default=kickoff_mod.DEFAULT_RESEARCH_BRIEF_WORKFLOW,
                       help=f"workflow id (default: {kickoff_mod.DEFAULT_RESEARCH_BRIEF_WORKFLOW})")
    brief.add_argument("--note", default=None, help="optional free-text note recorded on the action")
    brief.set_defaults(func=cmd_gate_research_brief)

    derive = gsub.add_parser(
        "derive-possibles",
        help="commission a CLUSTER-SCOPED run of the possibles-derivation lane (add-wheel-action-verbs)")
    _add_gate_identity_args(derive)
    _add_gate_snapshot_args(derive)   # the cluster is validated against the snapshot
    derive.add_argument("--cluster-id", required=True,
                        help="the topic cluster to scope the derivation run to")
    derive.add_argument("--outline", default=None, help="the commissioning outline (default: a standard derivation commission)")
    derive.add_argument("--workflow", default=kickoff_mod.DEFAULT_DERIVE_POSSIBLES_WORKFLOW,
                        help=f"workflow id (default: {kickoff_mod.DEFAULT_DERIVE_POSSIBLES_WORKFLOW})")
    derive.add_argument("--note", default=None, help="optional free-text note recorded on the action")
    derive.set_defaults(func=cmd_gate_derive_possibles)

    project = gsub.add_parser(
        "create-project",
        help="commission a project-register edit creating one project (add-project-scoped-selection)")
    _add_gate_identity_args(project)
    project.add_argument("name", help="the project display name (the id is slugged from it)")
    project.add_argument("--repo", action="append", default=None,
                         help="a member repository id (repeatable; OPTIONAL — an empty project gains members later via edit-project)")
    project.add_argument("--project-register", default=None,
                         help="explicit register path (default: discovered from the checkout upward)")
    project.add_argument("--outline", default=None, help="the commissioning outline (default: a standard register-edit commission)")
    project.add_argument("--workflow", default=kickoff_mod.DEFAULT_PROJECT_REGISTER_EDIT_WORKFLOW,
                         help=f"workflow id (default: {kickoff_mod.DEFAULT_PROJECT_REGISTER_EDIT_WORKFLOW})")
    project.add_argument("--note", default=None, help="optional free-text note recorded on the action")
    project.set_defaults(func=cmd_gate_create_project)

    edit_project = gsub.add_parser(
        "edit-project",
        help="commission a membership edit of an existing project (add-opendox-project-header)")
    _add_gate_identity_args(edit_project)
    edit_project.add_argument("project_id", help="the register project to edit")
    edit_project.add_argument("--add", action="append", default=None,
                              help="a repository id to add (repeatable)")
    edit_project.add_argument("--remove", action="append", default=None,
                              help="a repository id to remove (repeatable)")
    edit_project.add_argument("--project-register", default=None,
                              help="explicit register path (default: discovered from the checkout upward)")
    edit_project.add_argument("--outline", default=None, help="the commissioning outline (default: a standard register-edit commission)")
    edit_project.add_argument("--workflow", default=kickoff_mod.DEFAULT_PROJECT_REGISTER_EDIT_WORKFLOW,
                              help=f"workflow id (default: {kickoff_mod.DEFAULT_PROJECT_REGISTER_EDIT_WORKFLOW})")
    edit_project.add_argument("--note", default=None, help="optional free-text note recorded on the action")
    edit_project.set_defaults(func=cmd_gate_edit_project)

    _add_lens_gate_subcommands(gsub)
    _add_create_document_subcommand(gsub)
    _add_edit_document_subcommand(gsub)
    _add_open_pr_subcommand(gsub)
    _add_session_ending_subcommands(gsub)


def _add_create_document_subcommand(gsub) -> None:
    """`gate create-document` (add-workbench-bullseye-and-create task 4.5): the
    parity surface for the workbench's create affordance. The flag names mirror
    the non-gated `create` subcommand so the two read the same, and the gate-off
    CLI DESCRIPTOR the workbench renders is exactly this invocation."""
    doc = gsub.add_parser(
        "create-document",
        help="create a NEW header-compliant ideation document through the gate "
             "(create-only, recorded; add-workbench-bullseye-and-create)")
    _add_gate_identity_args(doc)
    # The TILE's scope identity (007-workbench-branch-sessions T023a, FR-018).
    # OPTIONAL and given TOGETHER: with both, the create opens or joins the tile's
    # branch session and lands on the branch as one commit with its record; with
    # neither, the create behaves exactly as it did before this feature. This is
    # the pair quickstart step 2 invokes.
    doc.add_argument("--scope-kind", default=None,
                     choices=list(branch_session_mod.SCOPE_KINDS),
                     help="the tile's scope kind — resolves the branch session "
                          "(requires --scope-id; omit both for a main-resident "
                          "create)")
    doc.add_argument("--scope-id", default=None,
                     help="the tile id: a staging FOLDER name, a cl-*, or a pos-* "
                          "(requires --scope-kind)")
    doc.add_argument("--area", default=authoring_mod.DEFAULT_AREA,
                     help=f"target ideation area (default: {authoring_mod.DEFAULT_AREA})")
    doc.add_argument("--title", required=True,
                     help="document title (H1, without the — Brainstorm suffix)")
    doc.add_argument("--summary", required=True, help="Summary: one sentence")
    doc.add_argument("--topics", required=True, help="comma-separated Topics: list")
    doc.add_argument("--repository-context", required=True,
                     help="Repository context: value — a DOCUMENT HEADER field "
                          "(the route defaults it from the served snapshot; the "
                          "CLI asks for it). It is not the registry key: see "
                          "--repository")
    # THE REGISTRY/NOTEBOOK KEY (PR #49 review finding 8, leg b). Every sibling
    # session verb has had this flag and derives the key as `--repository or the
    # checkout directory's name`; `create-document` — the ONE verb that OPENS a
    # session — had no such flag and used `--repository-context`, a document
    # HEADER value, instead. A create with `--repository-context "openxFactory
    # ideation"` therefore keyed its session and named its notebook one way while
    # every later verb keyed the same session another, so the abandon reported a
    # notebook torn down that it had never looked at. One derivation now, shared.
    doc.add_argument("--repository", default=None,
                     help="the registry key's repository half (default: the "
                          "checkout directory's name, the same convention the "
                          "worktree container is derived from)")
    doc.add_argument("--kind", default=authoring_mod.DEFAULT_KIND, help="Kind: value")
    doc.add_argument("--status", default=None,
                     choices=authoring_mod.CREATABLE_STATUSES,
                     help="Status: value (default: brainstorm, in EVERY area — "
                          "a created document's tie to a staging packet is its "
                          "placement in that folder, not its status header)")
    doc.add_argument("--source", default=None,
                     help="optional Source: provenance citation (the workbench "
                          "scope, or the keyword-lens recipe at a source_revision)")
    doc.add_argument("--possible-feat", action="append", default=[],
                     help="a ## Possible feats bullet (repeatable)")
    # The ANSWER to the FR-025 resume-or-new report (T056). Not in
    # contracts/cli.md's flag list, and added because FR-020 owes the choice a CLI
    # surface: the report is a REFUSAL naming both continuations, so without a way
    # to answer it a CLI-only human could never continue an abandoned tile at all.
    # Optional by design — the first write sends none and gets the report.
    doc.add_argument("--continuation", default=None,
                     choices=list(branch_session_mod.CONTINUATIONS),
                     help="answer the resume-or-new report on a tile whose "
                          "abandoned branch survives: `resume` keeps the existing "
                          "branch and its history, `new` opens the next ordinal "
                          "(FR-025; omit it to be SHOWN the choice)")
    doc.set_defaults(func=cmd_gate_create_document)


def _add_edit_document_subcommand(gsub) -> None:
    """`gate edit-document` (007-workbench-branch-sessions T043, FR-020): the
    parity surface for the session's rewrite affordance, and the copyable
    descriptor the gate-off workbench renders for it (FR-046).

    The flag surface is contracts/cli.md's, exactly: the tile scope that resolves
    the session, the document, `--content-file` (never inline text, so a shell
    cannot mangle a document), and optional notes. There is deliberately no
    `--dry-run` — a partial session write is worse than no affordance — and no
    flag that creates or deletes: this verb REWRITES, creation stays
    `create-document`, and no session verb grants delete authority."""
    doc = gsub.add_parser(
        "edit-document",
        help="rewrite an EXISTING document inside the tile's branch session "
             "(session-only, recorded, one commit; 007-workbench-branch-sessions)")
    _add_gate_identity_args(doc)
    doc.add_argument("--scope-kind", required=True,
                     choices=list(branch_session_mod.SCOPE_KINDS),
                     help="the tile's scope kind — resolves the branch session "
                          "this rewrite happens in")
    doc.add_argument("--scope-id", required=True,
                     help="the tile id: a staging FOLDER name, a cl-*, or a pos-*")
    doc.add_argument("--document", required=True,
                     help="the document to rewrite, as a path inside the session "
                          "worktree (a path outside it refuses)")
    doc.add_argument("--content-file", required=True,
                     help="file whose contents REPLACE the document (never inline "
                          "text; an empty file is refused as a delete in disguise)")
    doc.add_argument("--notes", default=None,
                     help="optional free-text note recorded on the action")
    doc.add_argument("--repository", default=None,
                     help="the registry key's repository half (default: the "
                          "checkout directory's name, the same convention the "
                          "worktree container is derived from)")
    doc.set_defaults(func=cmd_gate_edit_document)


def _add_open_pr_subcommand(gsub) -> None:
    """`gate open-pr` (007-workbench-branch-sessions T065, FR-020/FR-029): the
    parity surface for the session's SAVE affordance, and the copyable descriptor
    the gate-off workbench renders for it (FR-046).

    The flag surface is contracts/cli.md's, exactly: the tile scope that resolves
    the session, an optional `--title`, and `--body-file` rather than inline text so
    a shell cannot mangle a pull-request body. There is deliberately NO `--dry-run`
    (a partial session write is worse than no affordance), NO flag that merges,
    approves, or bypasses protection (FR-030 — the verb holds no such authority),
    and — the ruled one — NO token flag of any kind: the push identity is the
    INVOKING ENGINEER's own ambient `gh` authentication (FR-034, D22), so a
    credential argument would create a second, unruled identity path."""
    save = gsub.add_parser(
        "open-pr",
        help="push the tile's session branch and open (or update) its pull "
             "request into the existing Merge-Master ritual")
    _add_gate_identity_args(save)
    save.add_argument("--scope-kind", required=True,
                      choices=list(branch_session_mod.SCOPE_KINDS),
                      help="the tile's scope kind — resolves the session to save")
    save.add_argument("--scope-id", required=True,
                      help="the tile id: a staging FOLDER name, a cl-*, or a pos-*")
    save.add_argument("--title", default=None,
                      help="the pull request's title. Omitted: the FIRST save "
                           "names the session branch and its tile, a LATER save "
                           "leaves the existing title unchanged")
    save.add_argument("--body-file", default=None,
                      help="file whose contents become the pull request BODY "
                           "(never inline text). Omitted: the FIRST save carries "
                           "the merge-commit-never-squash notice (D18), a LATER "
                           "save leaves the existing body unchanged — a save never "
                           "overwrites reviewer-facing text a human wrote")
    save.add_argument("--repository", default=None,
                      help="the registry key's repository half (default: the "
                           "checkout directory's name)")
    save.set_defaults(func=cmd_gate_open_pr)

    # add-doxbench-editing-phase-b §12: the SHARE verb, the same flag surface with
    # the pull-request half removed. No `--title` and no `--body-file`, because
    # those name a pull request and this verb opens none; no token flag, for the
    # same ruled reason as above; and nothing that overrides the nothing-new
    # answer, because §12.3 says it is reported honestly rather than pushed past.
    share = gsub.add_parser(
        "share-session",
        help="commit the session's dirty thread sidecars and push the branch so "
             "a colleague can resume the session (opens NO pull request)")
    _add_gate_identity_args(share)
    share.add_argument("--scope-kind", required=True,
                       choices=list(branch_session_mod.SCOPE_KINDS),
                       help="the tile's scope kind — resolves the session to share")
    share.add_argument("--scope-id", required=True,
                       help="the tile id: a staging FOLDER name, a cl-*, or a pos-*")
    share.add_argument("--notes", default=None,
                       help="optional note recorded on the gate-action record — "
                            "why this session is being handed over")
    share.add_argument("--repository", default=None,
                       help="the registry key's repository half (default: the "
                            "checkout directory's name)")
    share.set_defaults(func=cmd_gate_share_session)


def _add_session_ending_subcommands(gsub) -> None:
    """`gate abandon-session` and `gate cleanup-abandoned-branch`
    (007-workbench-branch-sessions T053/T056, FR-020) — the CLI parity surfaces of
    the two FR-021/FR-028 routes, and the copyable descriptors the gate-off
    workbench renders for them (FR-046).

    The flag surface is contracts/cli.md's, exactly. There is deliberately no
    `--dry-run` (a partial session write is worse than no affordance), no flag that
    skips the record, and — on the abandon — nothing that deletes a branch: FR-022
    deletes nothing at abandon time, and the branch's end of life is the SEPARATE,
    human-invoked cleanup below, which is why they are two verbs."""
    end = gsub.add_parser(
        "abandon-session",
        help="end the tile's branch session without saving, with the required "
             "reason (recorded on `main`; the branch survives)")
    _add_gate_identity_args(end)
    end.add_argument("--scope-kind", required=True,
                     choices=list(branch_session_mod.SCOPE_KINDS),
                     help="the tile's scope kind — resolves the session to end")
    end.add_argument("--scope-id", required=True,
                     help="the tile id: a staging FOLDER name, a cl-*, or a pos-*")
    end.add_argument("--reason", required=True,
                     help="the durable why this exploration stopped (required, "
                          "exactly as a demotion's reason is)")
    end.add_argument("--notes", default=None,
                     help="optional free-text note recorded on the action")
    end.add_argument("--repository", default=None,
                     help="the registry key's repository half (default: the "
                          "checkout directory's name)")
    end.set_defaults(func=cmd_gate_abandon_session)

    clean = gsub.add_parser(
        "cleanup-abandoned-branch",
        help="delete an ABANDONED session's surviving local branch after durable "
             "retention release (human-invoked, never automatic)")
    _add_gate_identity_args(clean)
    clean.add_argument("--scope-kind", required=True,
                       choices=list(branch_session_mod.SCOPE_KINDS),
                       help="the tile's scope kind — the branch is checked against "
                            "the tile that OWNS it")
    clean.add_argument("--scope-id", required=True,
                       help="the tile id: a staging FOLDER name, a cl-*, or a pos-*")
    clean.add_argument("--ref", required=True,
                       help="the abandoned session branch to delete (must be this "
                            "tile's own branch or one of its ordinal forms)")
    clean.add_argument(
        "--retention-release-reason", default=None,
        help="explicit human release for a true orphan, duplicate, superseded, "
             "cluster, possible, or missing tile; machine-resolved proposal or "
             "demotion evidence does not require it")
    clean.add_argument(
        "--superseding-reference", action="append", default=[],
        help="optional durable reference supporting an explicit release; repeat "
             "for multiple references")
    clean.add_argument("--repository", default=None,
                       help="the registry key's repository half (default: the "
                            "checkout directory's name)")
    clean.set_defaults(func=cmd_gate_cleanup_abandoned_branch)


def _add_lens_recipe_args(sub: argparse.ArgumentParser) -> None:
    """Recipe + override args shared by the two lens verbs. Snapshot-generation
    args supply the corpus the recipe is re-evaluated against."""
    _add_gate_identity_args(sub)
    _add_gate_snapshot_args(sub)
    sub.add_argument("--name", required=True, help="the workbench set name (slugged for the manifest path)")
    sub.add_argument("--checked", action="append", required=True,
                     help="a checked keyword (stratify); repeatable — at least one required")
    sub.add_argument("--pinned", action="append", default=[],
                     help="a pinned keyword (require = hard filter); repeatable (MUST be a subset of --checked)")
    sub.add_argument("--include", action="append", default=[],
                     help="a manual-include override document=reason (near-miss pulled in; reason required); repeatable")
    sub.add_argument("--exclude", action="append", default=[],
                     help="an excluded override document=reason (recipe match removed; reason required); repeatable")


def _add_lens_gate_subcommands(gsub) -> None:
    save = gsub.add_parser("lens-save-recipe",
                           help="save a keyword-lens recipe as a workbench manifest (add-lens-gate-verbs)")
    _add_lens_recipe_args(save)
    save.set_defaults(func=cmd_gate_lens_save_recipe)

    cluster = gsub.add_parser("lens-add-as-cluster",
                              help="add a keyword-lens set as a pending_review human-seen cluster (add-lens-gate-verbs)")
    _add_lens_recipe_args(cluster)
    cluster.add_argument("--proposer", default=None, help="the proposing human (default: --actor)")
    cluster.add_argument("--evidence-repository", default=None,
                         help="the evidence source_ref repository (default: --repository)")
    cluster.add_argument("--evidence-path", default=None, help="the evidence source_ref repo-relative path")
    cluster.add_argument("--revision", default=None, help="the FULL committed revision the passage is pinned at (40/64-hex)")
    cluster.add_argument("--section", default=None, help="the evidence source_ref section")
    cluster.add_argument("--passage-sha256", default=None, help="the 64-hex sha256 of the pinned passage")
    cluster.add_argument("--rationale", default=None, help="the organizer rationale for the cluster")
    cluster.add_argument("--confidence", type=float, default=None, help="the organizer confidence in [0, 1]")
    cluster.add_argument("--alternative", action="append", default=[],
                         help="an alternative interpretation considered (repeatable; may be empty)")
    cluster.add_argument("--recipe-reference", default=None,
                         help="optional re-runnable recipe pointer (default: derived from the set name + keywords)")
    cluster.set_defaults(func=cmd_gate_lens_add_as_cluster)


class GateSubcommands:
    """This module's contribution to the command line, as the extension point
    takes it (`subcommand_extension.SubcommandExtension`).

    STRUCTURAL CONFORMANCE, ASSERTED BY ABSENCE: nothing here imports
    `subcommand_extension`, and that is the point of declaring the interface as
    a `runtime_checkable` `Protocol` — the contributing layer conforms by having
    the method, so after the carve an openXdox that never imports openDox's
    tooling still registers. `register_all` refuses a non-conformer where it is
    wired, which is the only check this shape needs.

    The class lives HERE, beside the verbs it contributes, rather than in the
    composition module: what a layer contributes is the layer's own statement,
    and which contributions an assembly uses is the composition point's
    (`profile_openxfactory.SUBCOMMAND_EXTENSIONS`). Same division the corpus
    adapter already draws between the adapter package and its selection.
    """

    def register(self, subparsers) -> None:
        """Attach the `gate` subcommand tree to the parser being built."""
        _add_gate_subcommands(subparsers)
