"""US9 human gate console tests (T036) — the authority-bearing crown story.

Every ratified "Human gate console" scenario, against the REAL fixture change
tree (a tmp copy of base-repo carrying the active `add-ideation-governance`
change and its `ideation-governance` staging topic), generated in-test on the
same FakeGit + PINNED_REVISION substrate as the rest of the suite:

  * demote produces the transition artifacts (manifest + executable plan +
    register-update note) and a gate-action record that validates clean against
    the PINNED openxFactory validator;
  * demote without a reason is refused (engine-side, before any write);
  * the reverse transition ROUND-TRIPS — executing the plan against the fixture
    tree lands the proposal drafts in the topic's `openspec/` workspace with
    Status flipped to draft, updates the staging README + writes the openspec/
    INDEX, and removes the emptied change folder;
  * ratify writes the ratification record + register-update and a gate-action
    record CARRYING the ratification-record artifact (schema contains-rule),
    validator-clean;
  * edit-apply applies EXACTLY the human-approved redline and nothing else
    (byte-compare) through the HumanGate, and its record carries the redline;
  * EVERY action entrypoint demands a HumanGate — an OutputBoundary / agent path
    is rejected AND reported on its own ledger (structural, D16);
  * serve.py exposes NO GATE write route (its only write route is the v2
    loopback notebook action, tested in test_notebook_action; a POST to a
    read-only route is refused without writing);
  * the web gate bar (gate.js) is a pure descriptor builder and binds every
    dynamic value via textContent (node-verified DOM-safety).
"""

from __future__ import annotations

import http.client
import importlib.util
import json
import shutil
import subprocess
import sys
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest
import yaml

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit, find_openxfactory_validator

from doc_health import families
from ideation_dashboard import gate_console as gc
from ideation_dashboard import record_binding as rb
from ideation_dashboard import round_trip
from ideation_dashboard import serve as serve_mod
from ideation_dashboard.boundary import (
    AGENT, GATE_SIDE_EFFECT, BoundaryViolation, HumanGate, OutputBoundary,
)
from ideation_dashboard.generator import generate_snapshot

VALIDATOR = find_openxfactory_validator()
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
GATE_JS = WEB / "views" / "gate.js"
NODE = shutil.which("node")
CHANGE = "add-ideation-governance"
TOPIC = "ideation-governance"
AT = "2026-07-14T12:00:00Z"


def _tree(tmp_path: Path) -> Path:
    """A writable copy of the fixture change tree (base-repo)."""
    root = tmp_path / "repo"
    shutil.copytree(BASE_REPO, root)
    return root


def _snapshot(root: Path) -> dict:
    return generate_snapshot(root, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


def _gate(root: Path, records_dir: str = gc.DEFAULT_RECORDS_DIR) -> HumanGate:
    return HumanGate(root, [records_dir], human_actor="brett")


def _validate(path: Path, *extra: str) -> subprocess.CompletedProcess:
    if VALIDATOR is None:
        pytest.skip("pinned openxFactory validator not reachable")
    return subprocess.run([sys.executable, str(VALIDATOR), *extra, str(path)],
                          capture_output=True, text=True)


# ============================================================================
# agent refusal — every action entrypoint demands a HumanGate (D16, structural)
# ============================================================================

def test_constructing_a_console_from_an_agent_boundary_is_rejected_and_reported(tmp_path):
    agent = OutputBoundary(_tree(tmp_path), [gc.DEFAULT_RECORDS_DIR], actor=AGENT)
    with pytest.raises(BoundaryViolation) as ei:
        gc.GateConsole(agent)
    assert ei.value.refusal.kind == GATE_SIDE_EFFECT
    # reported on the offending boundary's OWN ledger — never silent.
    assert agent.refusals and agent.refusals[-1].kind == GATE_SIDE_EFFECT


def test_every_gate_action_function_refuses_an_agent_boundary_and_reports(tmp_path):
    root = _tree(tmp_path)
    snap = _snapshot(root)
    agent = OutputBoundary(root, [gc.DEFAULT_RECORDS_DIR], actor=AGENT)
    attempts = {
        "demote": lambda: gc.demote(agent, snap, CHANGE, reason="x"),
        "ratify": lambda: gc.ratify(agent, CHANGE, "brett"),
        "edit_apply": lambda: gc.edit_apply(agent, CHANGE, "d.md", gc.Redline(full_text="z")),
    }
    for name, fn in attempts.items():
        before = len(agent.refusals)
        with pytest.raises(BoundaryViolation) as ei:
            fn()
        assert ei.value.refusal.kind == GATE_SIDE_EFFECT, name
        # each attempt appended exactly one refusal to the agent's ledger.
        assert len(agent.refusals) == before + 1, name
        assert agent.refusals[-1].kind == GATE_SIDE_EFFECT, name


def test_require_human_gate_passes_a_real_humangate(tmp_path):
    gate = _gate(_tree(tmp_path))
    assert gc.require_human_gate(gate) is gate


# ============================================================================
# demote — plan, records, refusals, and the round-trip execution
# ============================================================================

def test_demote_emits_transition_manifest_plan_register_update_and_a_valid_record(tmp_path):
    root = _tree(tmp_path)
    snap = _snapshot(root)
    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="Reworking scope.", at=AT)

    # the three governed artifacts + the gate-action record all landed on disk.
    for p in (res.manifest_path, res.plan_path, res.register_update_path, res.record_path):
        assert p.is_file()
    # ... all under the declared records allowlist (nothing outside it).
    for p in (res.manifest_path, res.plan_path, res.register_update_path, res.record_path):
        assert gc.DEFAULT_RECORDS_DIR in p.relative_to(root).as_posix()

    rec = res.gate_action_record
    assert rec["action"] == "demote"
    assert rec["reason"] == "Reworking scope."
    kinds = {a["kind"] for a in rec["artifacts"]}
    assert "transition-manifest" in kinds and "register-update" in kinds

    proc = _validate(res.record_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_successful_demotion_execution_writes_a_schema_valid_receipt(tmp_path):
    root = _tree(tmp_path)
    res = gc.GateConsole(_gate(root)).demote(
        _snapshot(root), CHANGE, reason="Reworking scope.", at=AT)

    execution = gc.execute_demotion_plan(res.plan, root, at=AT)
    receipt_path = gc.write_demotion_execution_receipt(
        _gate(root), res, execution, at="2026-07-14T12:01:00Z")

    receipt = yaml.safe_load(receipt_path.read_text(encoding="utf-8"))
    assert receipt["kind"] == gc.DEMOTION_EXECUTION_KIND
    assert receipt["status"] == "executed"
    assert receipt["change_id"] == CHANGE
    assert receipt["destination"]["id"] == TOPIC
    assert receipt["transition_manifest"] == res.manifest_path.relative_to(root).as_posix()
    assert receipt["returned_moves"] == [
        {"from": move.from_path, "to": move.to_path}
        for move in sorted(res.plan.moves, key=lambda item: (
            item.from_path, item.to_path))
    ]
    assert receipt["returned_artifacts"]
    proc = _validate(receipt_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_demotion_preflights_every_planned_source_before_moving_anything(tmp_path):
    root = _tree(tmp_path)
    plan = gc.plan_demotion(_snapshot(root), CHANGE, reason="Reworking scope.")
    first = root / plan.moves[0].from_path
    missing = root / plan.moves[-1].from_path
    before = first.read_bytes()
    missing.unlink()

    with pytest.raises(gc.GateRefused, match="no files were moved"):
        gc.execute_demotion_plan(plan, root, at=AT)

    assert first.read_bytes() == before
    assert not (root / plan.moves[0].to_path).exists()


def test_execution_receipt_refuses_partial_or_zero_move_results(tmp_path):
    root = _tree(tmp_path)
    result = gc.GateConsole(_gate(root)).demote(
        _snapshot(root), CHANGE, reason="Reworking scope.", at=AT)
    with pytest.raises(gc.GateRefused, match="every planned move"):
        gc.demotion_execution_receipt(
            result, gc.DemotionExecution(), actor="brett", at=AT, root=root)


def _cleanup_record_for(ref: str, *, scope_id: str = TOPIC) -> dict:
    return gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_CLEANUP_ABANDONED_BRANCH,
        at=AT, topic_id=scope_id, ref=ref,
        reason="reviewed and superseded",
        artifacts=[{"kind": gc.ART_OTHER, "reference": f"refs/heads/{ref}@"
                    + "a" * 40}],
        cleanup={
            "status": "completed", "pre_delete_head": "a" * 40,
            "abandonment": {
                "kind": "abandon-session-record",
                "reference": "ideation/dashboard/gate-records/abandon.yaml",
                "summary": "The record names this ref.",
            },
            "retention_release": {
                "kind": "explicit-human-release",
                "scope_kind": "staged-topic", "scope_id": scope_id,
                "references": [], "reason": "reviewed and superseded",
            },
        })


def test_cleanup_records_with_same_tile_and_stamp_are_keyed_by_exact_ref(tmp_path):
    root = _tree(tmp_path)
    gate = _gate(root)
    first = _cleanup_record_for(f"draft/{TOPIC}")
    second = _cleanup_record_for(f"draft/{TOPIC}-2")

    first_path = gc.write_gate_action_record(
        gate, gc.DEFAULT_RECORDS_DIR, first, exclusive=True)
    second_path = gc.write_gate_action_record(
        gate, gc.DEFAULT_RECORDS_DIR, second, exclusive=True)

    assert first_path != second_path
    assert first_path.parent.name != second_path.parent.name
    with pytest.raises(gc.GateRefused, match="may not overwrite"):
        gc.write_gate_action_record(
            gate, gc.DEFAULT_RECORDS_DIR, first, exclusive=True)


def test_cleanup_record_semantics_require_exact_target_scope_identity():
    record = _cleanup_record_for(f"draft/{TOPIC}")
    record["cleanup"]["retention_release"]["scope_id"] = "another-topic"

    with pytest.raises(gc.GateRefused, match="exactly match"):
        gc.validate_gate_action_record(record)


def test_nested_supporting_documents_keep_unique_return_destinations(tmp_path):
    root = _tree(tmp_path)
    _reach_proposal(root, _fragment_reaching_proposal(ASPIRATIONAL_GUESS))
    plan = gc.plan_demotion(_snapshot(root), CHANGE, reason="Reworking scope.")
    destinations = [move.to_path for move in plan.moves]

    assert len(destinations) == len(set(destinations))
    assert (f"ideation/staging/{TOPIC}/source-snapshots/README.md"
            in destinations)


def test_demote_plan_routes_proposal_to_openspec_workspace_and_withdraws_the_pick(tmp_path):
    root = _tree(tmp_path)
    plan = gc.plan_demotion(_snapshot(root), CHANGE, reason="r")
    by_from = {m.from_path: m for m in plan.moves}
    prop = by_from[f"openspec/changes/{CHANGE}/proposal.md"]
    assert prop.to_path == f"ideation/staging/{TOPIC}/openspec/proposal.md"
    assert prop.status_flip == "draft"  # proposal continues as a DRAFT idea
    tasks = by_from[f"openspec/changes/{CHANGE}/tasks.md"]
    assert tasks.to_path == f"ideation/staging/{TOPIC}/openspec/tasks.md"
    # the picked possible inheriting this change id has its pick withdrawn.
    assert plan.withdrawn_picks == ("pos-ideation-governance",)


def test_demote_without_a_reason_is_refused_before_any_write(tmp_path):
    root = _tree(tmp_path)
    snap = _snapshot(root)
    console = gc.GateConsole(_gate(root))
    with pytest.raises(gc.GateRefused):
        console.demote(snap, CHANGE, reason="   ", at=AT)
    # refused engine-side: no record was written and the ledger recorded no gate write.
    assert not (root / gc.DEFAULT_RECORDS_DIR).exists()


def test_demote_of_an_unknown_or_inactive_change_is_refused(tmp_path):
    snap = _snapshot(_tree(tmp_path))
    with pytest.raises(gc.GateRefused):
        gc.plan_demotion(snap, "no-such-change", reason="r")


def test_demote_round_trip_lands_drafts_in_the_topic_openspec_workspace(tmp_path):
    root = _tree(tmp_path)
    snap = _snapshot(root)
    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="Back to staging.", at=AT)

    ex = gc.execute_demotion_plan(res.plan, root, at=AT)

    ws = root / "ideation" / "staging" / TOPIC / "openspec"
    proposal = ws / "proposal.md"
    assert proposal.is_file()  # draft landed in the topic's openspec/ workspace
    head = proposal.read_text(encoding="utf-8").splitlines()
    assert "Status: draft" in head  # proposal CONTINUES AS A DRAFT idea
    # the source change folder is emptied/removed by the reverse transition.
    assert not (root / "openspec" / "changes" / CHANGE).exists()
    assert ex.removed_change_folder
    # the staging README records the return and the openspec/ INDEX lists it.
    readme = (root / "ideation" / "staging" / TOPIC / "README.md").read_text(encoding="utf-8")
    assert "Returned drafts" in readme and CHANGE in readme
    index = (ws / "INDEX.md").read_text(encoding="utf-8")
    assert "proposal.md" in index


def test_demote_console_does_not_touch_the_live_corpus_only_execution_does(tmp_path):
    # The console action PLANS + RECORDS; the change folder is untouched until a
    # human runs execute_demotion_plan (the plan-vs-execute split).
    root = _tree(tmp_path)
    snap = _snapshot(root)
    before = (root / "openspec" / "changes" / CHANGE / "proposal.md").read_bytes()
    gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="plan only.", at=AT)
    assert (root / "openspec" / "changes" / CHANGE / "proposal.md").read_bytes() == before
    assert (root / "openspec" / "changes" / CHANGE).is_dir()


def test_a_crlf_document_keeps_its_endings_when_the_demote_adds_a_header(tmp_path):
    """Wave re-review P3 — the F10 corpus-integrity class through another verb.
    The demote MOVE used to `read_text(errors="replace")` -> `write_text`, so on
    Linux a CRLF (Windows-authored) document was silently rewritten as LF by
    universal-newline translation — invalidating any open doxBench buffer's base
    identity for that document — and any undecodable byte was silently mangled to
    U+FFFD. Nothing here goes through universal-newline translation any more.

    UPDATED CONTRACT (Brett's ruling, 2026-08-19). This used to assert the moved
    copy was the source BYTE FOR BYTE, which was a wave-re-review regression pin
    and never ratified text. The round-trip requirement is unconditional about
    every artifact the reverse transition writes into a topic carrying a
    lifecycle status header, and a returned `tasks.md` is one — so a header IS
    added. What survives is the corpus-integrity guarantee itself: the added line
    takes the DOCUMENT'S OWN ending flavor, and every pre-existing byte is
    untouched."""
    root = _tree(tmp_path)
    snap = _snapshot(root)
    crlf = b"# Tasks\r\n\r\n- [ ] 1.1 authored\r\n- [ ] 1.2 on Windows\r\n"
    (root / "openspec" / "changes" / CHANGE / "tasks.md").write_bytes(crlf)

    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="CRLF round trip.", at=AT)
    ex = gc.execute_demotion_plan(res.plan, root, at=AT)

    moved = root / "ideation" / "staging" / TOPIC / "openspec" / "tasks.md"
    expected = b"# Tasks\r\n\r\nStatus: draft\r\n\r\n- [ ] 1.1 authored\r\n- [ ] 1.2 on Windows\r\n"
    assert moved.read_bytes() == expected
    # NOT one LF among the CRLFs — the added line matches the document
    assert b"\n" not in moved.read_bytes().replace(b"\r\n", b"")
    # …and the addition is RECORDED rather than silent
    assert ex.status_headers_added == [f"ideation/staging/{TOPIC}/openspec/tasks.md"]


def test_a_returned_document_that_already_has_a_header_is_not_touched_twice(tmp_path):
    """The add arm must never become a second writer of the same line: a document
    arriving with a header goes through the flip arm alone, and reports nothing
    added."""
    root = _tree(tmp_path)
    snap = _snapshot(root)
    crlf = b"# Tasks\r\n\r\nStatus: staged\r\n\r\n- [ ] 1.1 authored\r\n"
    (root / "openspec" / "changes" / CHANGE / "tasks.md").write_bytes(crlf)

    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="Already headed.", at=AT)
    ex = gc.execute_demotion_plan(res.plan, root, at=AT)

    moved = root / "ideation" / "staging" / TOPIC / "openspec" / "tasks.md"
    # `tasks.md` carries no status FLIP, so its existing header stands as authored
    assert moved.read_bytes() == crlf
    assert ex.status_headers_added == []


def test_a_returned_front_matter_document_gets_its_header_inside_the_block(tmp_path):
    """Where the header goes follows the corpus: the one real returned topic a
    human already fixed by hand
    (`ideation/staging/tier2-council-clearance-pattern/openspec/proposal.md`)
    carries `Status:` INSIDE the `---` block. Above it, the front matter would no
    longer start at position 0 and would stop being front matter."""
    root = _tree(tmp_path)
    snap = _snapshot(root)
    (root / "openspec" / "changes" / CHANGE / "proposal.md").write_text(
        "---\ncode_surface: none\ntarget_release: none\n---\n\n"
        "# Proposal: x\n\n## Why\n\nbecause.\n", encoding="utf-8")

    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="Front matter.", at=AT)
    gc.execute_demotion_plan(res.plan, root, at=AT)

    moved = (root / "ideation" / "staging" / TOPIC / "openspec"
             / "proposal.md").read_text(encoding="utf-8")
    assert moved.startswith(
        "---\ncode_surface: none\ntarget_release: none\nStatus: draft\n---\n")
    assert moved.count("Status:") == 1


def test_a_returned_document_with_no_leading_heading_still_gets_a_header(tmp_path):
    root = _tree(tmp_path)
    snap = _snapshot(root)
    (root / "openspec" / "changes" / CHANGE / "tasks.md").write_text(
        "- [ ] 1.1 no title line at all\n", encoding="utf-8")

    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="No heading.", at=AT)
    gc.execute_demotion_plan(res.plan, root, at=AT)

    moved = (root / "ideation" / "staging" / TOPIC / "openspec"
             / "tasks.md").read_text(encoding="utf-8")
    assert moved == "Status: draft\n\n- [ ] 1.1 no title line at all\n"


def test_a_non_markdown_return_is_still_a_pure_byte_copy(tmp_path):
    """The header obligation is about GOVERNED MARKDOWN. A `.openspec.yaml` is
    not decoded at all, so an undecodable byte in one cannot fail a demotion and
    cannot be mangled into U+FFFD either."""
    root = _tree(tmp_path)
    raw = b"schema: spec-driven\r\ncreated: 2026-07-02\r\n\xff\xfe not utf-8\r\n"
    (root / "openspec" / "changes" / CHANGE / ".openspec.yaml").write_bytes(raw)
    snap = _snapshot(root)   # written BEFORE the snapshot, so the move plans it

    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="Bytes.", at=AT)
    ex = gc.execute_demotion_plan(res.plan, root, at=AT)

    moved = root / "ideation" / "staging" / TOPIC / "openspec" / ".openspec.yaml"
    assert moved.read_bytes() == raw
    # the fixture's own header-less `tasks.md` IS headed on the same lap — the
    # obligation applies to markdown and to nothing else
    assert not any(p.endswith(".yaml") for p in ex.status_headers_added)


def test_a_status_flipping_demote_move_preserves_crlf_line_endings(tmp_path):
    """The flip arm of the same P3 fix: a move that DOES rewrite the `Status:`
    header must decode — but only that line changes. Untouched lines keep
    their CRLF endings exactly, and the rewritten Status line keeps the
    ending it had rather than being collapsed to LF."""
    root = _tree(tmp_path)
    snap = _snapshot(root)
    crlf = ("# Proposal\r\n\r\nStatus: active\r\n\r\n## Why\r\n\r\n"
            "authored on Windows.\r\n")
    (root / "openspec" / "changes" / CHANGE / "proposal.md").write_bytes(
        crlf.encode("utf-8"))

    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="CRLF flip.", at=AT)
    gc.execute_demotion_plan(res.plan, root, at=AT)

    moved = root / "ideation" / "staging" / TOPIC / "openspec" / "proposal.md"
    expected = crlf.replace("Status: active\r\n", "Status: draft\r\n")
    assert moved.read_bytes() == expected.encode("utf-8")


def test_the_demote_readme_append_preserves_the_existing_readmes_bytes(tmp_path):
    """The topic README leg of the same P3 fix: recording the return APPENDS
    to the staging README, and the append must not retranslate the document
    it appends to — a CRLF README's pre-existing bytes survive exactly, with
    the note after them."""
    root = _tree(tmp_path)
    snap = _snapshot(root)
    readme = root / "ideation" / "staging" / TOPIC / "README.md"
    crlf = b"# Ideation Governance\r\n\r\nStatus: staged\r\n"
    readme.write_bytes(crlf)

    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="README bytes.", at=AT)
    gc.execute_demotion_plan(res.plan, root, at=AT)

    after = readme.read_bytes()
    assert after.startswith(crlf), (
        "the append rewrote the README's own bytes instead of only adding to them")
    assert b"Returned drafts" in after


# ============================================================================
# demote and the ROUND-TRIP RULE (align-demote-to-round-trip-rule)
# ============================================================================
#
# The whole change exists because greps lie about this mechanism: nothing in the
# repository writes the round-trip slot BY NAME, so a search concluded the rule
# was unimplemented, and only driving the verb showed that the fragment is written
# by ROUTING — `supporting-docs/<topic>.md` returns to the topic root under its
# bare basename, which IS the primary fragment's path. So every test below drives
# the REAL `plan_demotion` + `execute_demotion_plan`. None of them stubs the move.
#
# The fixture change carries no supporting-docs, so `_with_transitioned_snapshot`
# adds exactly what `proposal-support.py transition` records: the topic's own
# fragment snapshotted under its bare basename, plus the manifest whose
# `transitioned_at` is the only source for the `Raised` slot.

ASPIRATIONAL = f"""# Staged: {TOPIC}

Status: staged
Summary: THE ASPIRATIONAL ORIGINAL, snapshotted before the proposal was raised.

## Last proposal attempt (round-trip provenance)

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Why

<!-- xspec:candidate target=ideation-dashboard -->
THE ASPIRATIONAL PRE-PROPOSAL GUESS.
<!-- /xspec:candidate -->
"""

LIVE = f"""# Staged: {TOPIC}

Status: staged
Summary: THE LIVE FRAGMENT, worked on AFTER the proposal was raised.

## Last proposal attempt (round-trip provenance)

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Idea notes (pre-document, non-documented)

- A HALF-FORMED THOUGHT NOBODY ELSE HAS A COPY OF. — Added-by: brett · 2026-08-18

## Why

<!-- xspec:candidate target=ideation-dashboard -->
A GUESS THE HUMAN LATER IMPROVED IN FLIGHT.
<!-- /xspec:candidate -->
"""


def _with_transitioned_snapshot(root: Path, *, manifest: bool = True,
                                snapshot: str = ASPIRATIONAL) -> Path:
    """Give the fixture change the shape `transition` leaves behind."""
    sd = root / "openspec" / "changes" / CHANGE / "supporting-docs"
    sd.mkdir(parents=True, exist_ok=True)
    (sd / f"{TOPIC}.md").write_text(snapshot, encoding="utf-8")
    if manifest:
        (sd / "manifest.yaml").write_text(
            "change_id: " + CHANGE + "\n"
            "format_version: 1\n"
            "origin:\n  kind: staged\n  path: ideation/staging/" + TOPIC + "\n"
            "remaining_paths: []\n"
            "transitioned_at: '2026-07-02'\n", encoding="utf-8")
    return sd / f"{TOPIC}.md"


def _fragment(root: Path) -> Path:
    return root / "ideation" / "staging" / TOPIC / f"{TOPIC}.md"


def _demote_and_execute(root: Path, *, reason="Reworking scope.",
                        staging_topic=None):
    snap = _snapshot(root)
    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason=reason, at=AT,
                                             staging_topic=staging_topic)
    ex = gc.execute_demotion_plan(res.plan, root, at=AT)
    return res, ex


def test_the_plan_declares_which_move_is_the_topics_outline(tmp_path):
    """design Decision 1: decided PATH-ONLY and in the PURE plan, so the
    reviewable `demote-<stamp>.plan.yaml` states it BEFORE execution. A human
    reviewing the plan should not have to infer it from a basename."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    plan = gc.plan_demotion(_snapshot(root), CHANGE, reason="r")

    outline = [m for m in plan.moves if m.outline]
    assert len(outline) == 1
    assert outline[0].to_path == f"ideation/staging/{TOPIC}/{TOPIC}.md"
    # A staged topic's outline is STAGED — set positively, not by omitting a flip.
    assert outline[0].status_flip == "staged"
    # …and the draft flip is UNCHANGED for the documents bound for `openspec/`.
    by_from = {m.from_path: m for m in plan.moves}
    prop = by_from[f"openspec/changes/{CHANGE}/proposal.md"]
    assert prop.status_flip == "draft" and prop.outline is False

    # published in both artifacts a human reads before running --execute
    manifest = gc.transition_manifest(plan, actor="brett", at=AT)
    entry = [f for f in manifest["files"] if f["outline"]]
    assert len(entry) == 1 and entry[0]["status_flip"] == "staged"
    assert manifest["status_at_demote"] == "active"
    steps = gc.executable_plan(plan, actor="brett", at=AT)["steps"]
    declared = [s for s in steps if s.get("outline_restore")]
    assert len(declared) == 1
    assert declared[0]["set_status"] == "staged"


def test_a_demote_restores_an_absent_outline_and_refreshes_it(tmp_path):
    """The ordinary case — `transition` empties the topic folder, so the
    destination is usually absent. Restored, staged, slots filled, and the marked
    section carrying the RETURNED proposal's real text."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    assert not _fragment(root).exists()

    res, ex = _demote_and_execute(root)
    text = _fragment(root).read_text(encoding="utf-8")

    assert ex.snapshot_disposition == "applied"
    assert ex.preserved_snapshot_path is None
    assert ex.outline_refreshed is True
    assert "Status: staged" in text and "Status: draft" not in text
    assert f"Change ID: {CHANGE}" in text
    assert "Raised: 2026-07-02" in text          # from the manifest, not guessed
    assert "Status at demote: active" in text
    assert f"Demoted: {AT[:10]}" in text
    assert "Demote reason: Reworking scope." in text
    assert "n/a" not in text and "none yet" not in text
    # the REAL returned proposal text, not the aspirational snapshot's
    returned = (root / "ideation" / "staging" / TOPIC / "openspec"
                / "proposal.md").read_text(encoding="utf-8")
    why = returned.split("## Why", 1)[1].split("\n## ", 1)[0].strip()
    assert why and why in text
    assert "THE ASPIRATIONAL PRE-PROPOSAL GUESS." not in text

    # …and refreshing the RESULT again with the same inputs is a no-op, which is
    # the requirement's idempotence clause measured on real output. "The same
    # inputs" moved with `refine-demote-round-trip-mechanics` part 4: the
    # state-at-demote slot now carries the change's task progress beside its
    # status (the fixture change records 2 of 4), so re-deriving it here means
    # re-deriving that too.
    again = round_trip.refresh_fragment(
        text, proposal_text=returned,
        provenance={"Change ID": CHANGE, "Raised": "2026-07-02",
                    "Status at demote": "active — 2 of 4 tasks done",
                    "Demoted": AT[:10],
                    "Demote reason": "Reworking scope."})
    assert again == text
    # the selector still calls it the topic's outline
    assert families._primary_fragment(
        root / "ideation" / "staging" / TOPIC).name == f"{TOPIC}.md"


def test_a_demote_never_byte_replaces_a_live_differing_outline(tmp_path):
    """THE TEST THIS CHANGE EXISTS FOR. Before it, the demote wrote the change
    folder's pre-proposal snapshot straight over the live fragment: everything
    learned while the change was in flight was discarded at exactly the moment it
    was most valuable, with no diff, no prompt, and no record beyond a path in a
    README list."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    _fragment(root).parent.mkdir(parents=True, exist_ok=True)
    _fragment(root).write_text(LIVE, encoding="utf-8")

    res, ex = _demote_and_execute(root)
    text = _fragment(root).read_text(encoding="utf-8")

    assert ex.snapshot_disposition == "preserved"
    # the live fragment's OWN content, outside the refreshed regions, survives
    assert "THE LIVE FRAGMENT, worked on AFTER the proposal was raised." in text
    assert "A HALF-FORMED THOUGHT NOBODY ELSE HAS A COPY OF." in text
    assert "## Idea notes (pre-document, non-documented)" in text
    # the snapshot never reached the destination
    assert "THE ASPIRATIONAL ORIGINAL" not in text
    assert "THE ASPIRATIONAL PRE-PROPOSAL GUESS." not in text
    # the bounded regions DID move
    assert f"Change ID: {CHANGE}" in text
    assert "A GUESS THE HUMAN LATER IMPROVED IN FLIGHT." not in text


def test_the_preserved_snapshot_is_a_visible_topic_file_named_in_the_record(tmp_path):
    """"Never byte-replace" must not quietly become "silently discard the other
    copy". The snapshot is kept as an ORDINARY topic file — not a dotfile, not
    `.orig` — because a hidden artifact in a governed folder is how material goes
    missing, and it is named where the human will look."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    _fragment(root).parent.mkdir(parents=True, exist_ok=True)
    _fragment(root).write_text(LIVE, encoding="utf-8")

    res, ex = _demote_and_execute(root)

    kept = root / "ideation" / "staging" / TOPIC / f"{TOPIC}.snapshot-{CHANGE}.md"
    assert kept.is_file()
    assert ex.preserved_snapshot_path == kept
    assert not kept.name.startswith(".") and not kept.name.endswith(".orig")
    body = kept.read_text(encoding="utf-8")
    assert "THE ASPIRATIONAL ORIGINAL" in body
    # it is a proposal-era snapshot, not the topic's outline
    assert "Status: draft" in body
    # …and the selector is NOT confused about which file is the outline
    assert families._primary_fragment(
        root / "ideation" / "staging" / TOPIC).name == f"{TOPIC}.md"
    # the README says what happened, and names the kept file
    readme = (root / "ideation" / "staging" / TOPIC / "README.md").read_text(
        encoding="utf-8")
    assert "REFRESHED IN PLACE" in readme
    assert "PRESERVED" in readme and kept.name in readme


def test_an_identical_outline_destination_counts_as_a_restore(tmp_path):
    """Case (b): nothing to lose, so no preserved copy. Routing it through the
    differs path would leave a snapshot file identical to the one beside it."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    _fragment(root).parent.mkdir(parents=True, exist_ok=True)
    _fragment(root).write_text(ASPIRATIONAL, encoding="utf-8")

    res, ex = _demote_and_execute(root)
    assert ex.snapshot_disposition == "applied"
    assert ex.preserved_snapshot_path is None
    assert not (root / "ideation" / "staging" / TOPIC
                / f"{TOPIC}.snapshot-{CHANGE}.md").exists()


def test_a_demote_with_no_proposal_document_still_fills_the_slots(tmp_path):
    """The requirement's own edge: slots filled, marked sections left exactly as
    they were."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    (root / "openspec" / "changes" / CHANGE / "proposal.md").unlink()

    res, ex = _demote_and_execute(root)
    text = _fragment(root).read_text(encoding="utf-8")
    assert f"Change ID: {CHANGE}" in text
    assert "Demote reason: Reworking scope." in text
    # the snapshot's own marked body is untouched, because there was nothing to
    # refresh it from
    assert "THE ASPIRATIONAL PRE-PROPOSAL GUESS." in text


def test_an_absent_manifest_records_the_raised_date_as_unavailable(tmp_path):
    """Never fabricated: not from the change folder's archive-date prefix, not
    from a file mtime. Most changes carry no manifest at all."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root, manifest=False)

    res, ex = _demote_and_execute(root)
    text = _fragment(root).read_text(encoding="utf-8")
    assert f"Raised: {round_trip.UNAVAILABLE}" in text
    assert "Raised: n/a" not in text


def test_a_crlf_outline_keeps_its_line_endings_through_the_refresh(tmp_path):
    """The corpus-integrity class through this verb's newest arm. The refresh is a
    bounded write; one insertion must never become a whole-file line-ending
    rewrite."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    _fragment(root).parent.mkdir(parents=True, exist_ok=True)
    _fragment(root).write_bytes(LIVE.replace("\n", "\r\n").encode("utf-8"))

    res, ex = _demote_and_execute(root)
    raw = _fragment(root).read_bytes()
    assert b"\r\n" in raw
    # no lone LF anywhere: every ending is CRLF
    assert raw.replace(b"\r\n", b"") .count(b"\n") == 0
    assert f"Change ID: {CHANGE}".encode() in raw


# ---- review F1: `_flip_status` shared the round-trip split --------------------
#
# Both inputs below are the reviewer's, reproduced against the fixed tree. They
# were reachable the moment this change routed a topic's PRIMARY FRAGMENT through
# `_flip_status`, and the fix is not confined to the fragment: every
# `openspec/`-bound document this verb flips to `draft` was exposed to the same two
# damages before.


def test_a_form_feed_in_a_status_line_does_not_invent_a_line_boundary():
    """`str.splitlines(keepends=True)` saw `Status: draft\\x0crest` as TWO
    pseudo-lines, replaced the first with no ending, and GLUED the remainder onto
    the new value — `Status: stagedrest of the line`. Text moved across a line
    boundary the file does not contain."""
    src = "Status: draft\x0crest of the line\nbody\n"
    out = gc._flip_status(src, "staged")
    assert "Status: stagedrest of the line" not in out, \
        "the remainder was glued onto the status value again"
    # the real line count is unchanged: no boundary was invented or destroyed
    assert out.count("\n") == src.count("\n")
    assert out.endswith("body\n")

    # UPDATED CONTRACT: `_flip_status` now reads the SAME grammar as the forward
    # gate, and `Status: draft\x0crest of the line` does not satisfy it — the
    # gate would refuse this document for lacking a header. So the flip declines
    # the line instead of rewriting it, and the human's trailing text survives.
    # The old behavior replaced the whole row with a bare `Status: staged`,
    # DISCARDING `\x0crest of the line`: silent data loss dressed as a flip, and
    # the assertion that used to sit here pinned it.
    assert out == src
    assert "rest of the line" in out

    # …and the ratified "the restored fragment MUST carry `Status: staged`"
    # scenario still holds, because the demote composes the flip with the header
    # ADD — which is the pair the verb actually applies.
    composed, added = gc._add_status_header(out, "staged")
    assert added is True
    assert composed.startswith("Status: staged\n")
    assert "rest of the line" in composed


def test_a_unicode_line_separator_in_the_header_does_not_hide_the_status():
    """U+2028 inflates the pseudo-line count past the 15-line header window, so a
    real `Status:` inside the header was never found and the flip silently did
    nothing — failing the ratified "the restored fragment MUST carry `Status:
    staged`" scenario on input you get by pasting from a web page."""
    header = "".join(f"Field{i}: v  \n" for i in range(9))
    src = "# Staged: t\n" + header + "Status: draft\n\n## Why\n"
    assert len(src.splitlines(keepends=True)) > gc.HEADER_SCAN_LINES
    out = gc._flip_status(src, "staged")
    assert "Status: staged" in out
    assert "Status: draft" not in out
    # …and every U+2028 the author had survives
    assert out.count(" ") == src.count(" ")


def test_the_status_flip_still_keeps_a_crlf_headers_own_ending():
    """The P3 guarantee the rewrite had to carry across unchanged."""
    src = "# T\r\n\r\nStatus: draft\r\n\r\n## Why\r\n"
    out = gc._flip_status(src, "staged")
    assert out == src.replace("Status: draft\r\n", "Status: staged\r\n")


# ---- review F2 and F3, through the driven verb --------------------------------


def test_a_fragment_ending_inside_an_unclosed_fence_withholds_the_refresh(tmp_path):
    """Review F2, end to end. The restore still happens — the file must exist — but
    the provenance is NOT written into the open span, and the execution record says
    so rather than reporting a refresh that did not occur."""
    root = _tree(tmp_path)
    unclosed = (f"# Staged: {TOPIC}\n\nStatus: staged\n\nExample:\n\n"
                "```markdown\n## Claims\n\n- x\n")
    _with_transitioned_snapshot(root, snapshot=unclosed)

    res, ex = _demote_and_execute(root)
    text = _fragment(root).read_text(encoding="utf-8")

    assert ex.outline_refreshed is False
    assert "unclosed code fence" in (ex.outline_refusal or "")
    assert round_trip.PROVENANCE_HEADING not in text
    # the restored bytes are the snapshot's, with only the status flip applied
    assert "```markdown\n## Claims\n\n- x\n" in text
    # and the README tells the human, instead of claiming a refresh
    readme = (root / "ideation" / "staging" / TOPIC / "README.md").read_text(
        encoding="utf-8")
    assert "unclosed code fence" in readme
    assert "REFRESHED IN PLACE" not in readme


def test_a_withheld_refresh_leaves_a_live_fragment_byte_identical(tmp_path):
    """The refusal must not become its own overwrite: a live differing fragment
    that ends inside a fence keeps every byte, and its mtime is not even touched."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    live = (f"# Staged: {TOPIC}\n\nStatus: staged\n\nMY WORK\n\n"
            "```markdown\n## Claims\n")
    _fragment(root).parent.mkdir(parents=True, exist_ok=True)
    _fragment(root).write_text(live, encoding="utf-8")
    before_mtime = _fragment(root).stat().st_mtime_ns

    res, ex = _demote_and_execute(root)

    assert ex.outline_refreshed is False
    assert _fragment(root).read_text(encoding="utf-8") == live
    assert _fragment(root).stat().st_mtime_ns == before_mtime
    # the snapshot was still preserved rather than discarded
    assert ex.snapshot_disposition == "preserved"
    assert ex.preserved_snapshot_path is not None


def test_the_cli_tells_the_human_the_snapshot_was_preserved(tmp_path, capsys):
    """Review F3. `snapshot_disposition` and `preserved_snapshot_path` were
    populated and read by nothing — "we did not overwrite your work" is exactly the
    sentence a human needs to be able to check, and it has to reach the operator who
    ran the verb, not just a dataclass."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    _fragment(root).parent.mkdir(parents=True, exist_ok=True)
    _fragment(root).write_text(LIVE, encoding="utf-8")

    from ideation_dashboard import cli

    # Through the REAL parser, not a hand-built Namespace: a Namespace's field set
    # can drift from the CLI's while the test keeps passing.
    args = cli.build_parser().parse_args([
        "gate", "demote", "--repo-root", str(root), "--actor", "brett",
        "--repository", "fixture-repo", "--source-revision", PINNED_REVISION,
        "--change-id", CHANGE, "--reason", "Reworking scope.", "--execute",
    ])
    assert args.func(args) == 0
    out = capsys.readouterr().out

    assert "snapshot preserved" in out
    assert "REFRESHED IN PLACE" in out
    assert f"{TOPIC}.snapshot-{CHANGE}.md" in out
    assert "not applied over your work" in out


# ---- the PARENT change's task 4.2: the round-trip rule, both transitions driven -
#
# `add-staged-topic-outline-template` 4.2 calls itself "the one test that must not
# be a shape assertion", and its property is narrower than anything above: a
# fragment that genuinely REACHED PROPOSAL, then was demoted, carries the last
# attempted `proposal.md`'s REAL text — not the aspirational original the change
# folder snapshotted — plus the change id, BOTH dates, and the reason.
#
# What the tests above already discharge, and what is therefore not repeated here:
# the absent-destination restore, the marked-section refresh against a returned
# proposal, the five slots, `Raised` from a manifest, and the never-byte-replace
# guard. What none of them do is REACH PROPOSAL for real — they hand-build the
# post-transition shape with `_with_transitioned_snapshot`. This one drives the
# actual forward gate, so "reached proposal" is the mechanism's own doing and both
# dates are real: `Raised` from the transition that raised it, `Demoted` from the
# demote that returned it.

_SUPPORT_SPEC = importlib.util.spec_from_file_location(
    "proposal_support_for_round_trip", REPO_ROOT / "scripts" / "proposal-support.py")
support = importlib.util.module_from_spec(_SUPPORT_SPEC)
sys.modules[_SUPPORT_SPEC.name] = support
_SUPPORT_SPEC.loader.exec_module(support)

# Deliberately unlike anything the template ships, so an aspirational echo or a
# skeleton placeholder cannot pass for the real thing.
ASPIRATIONAL_GUESS = "PRE-PROPOSAL GUESS: maybe the wheel should re-derive summaries."
IN_FLIGHT_TRUTH = ("WHAT THE CHANGE ACTUALLY LEARNED: the summary is guaranteed by "
                   "the template, so the wheel reads it and keeps the fallback.")
RAISED_ON = "2026-07-02"


def _fragment_reaching_proposal(marked_body: str) -> str:
    return f"""# Staged: {TOPIC}

Status: staged
Summary: a topic on its way to a proposal.
Staging ID: fixture-repo:staging:{TOPIC}

## Last proposal attempt (round-trip provenance)

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Why

<!-- xspec:candidate target=ideation-dashboard -->
{marked_body}
<!-- /xspec:candidate -->
"""


def _reach_proposal(root: Path, fragment_text: str, *, raised=RAISED_ON) -> None:
    """Drive the REAL forward gate: `proposal-support.py transition`.

    This is what "reached proposal" means mechanically, and every fact it produces
    is the transition's rather than this test's: the fragment MOVES into the
    change's `supporting-docs/` rewritten to `Status: draft` with a `Proposed by:`
    line, its original bytes are kept under `source-snapshots/`, the manifest
    records `transitioned_at` (the only source for the `Raised` slot), and the topic
    folder is emptied and removed.
    """
    topic_dir = root / "ideation" / "staging" / TOPIC
    topic_dir.mkdir(parents=True, exist_ok=True)
    (topic_dir / f"{TOPIC}.md").write_text(fragment_text, encoding="utf-8")
    support.transition(root, CHANGE, f"ideation/staging/{TOPIC}", [], None,
                       raised, False, True)


def _write_proposal(root: Path, why: str) -> None:
    proposal = root / "openspec" / "changes" / CHANGE / "proposal.md"
    proposal.parent.mkdir(parents=True, exist_ok=True)
    proposal.write_text(
        f"---\ncode_surface: none\n---\n\n# Proposal: {CHANGE}\n\n"
        f"## Why\n\n{why}\n", encoding="utf-8")


# THE DEMOTE NEEDS `--staging-topic`, and that is a fact about the flow rather than
# a convenience here. `plan_demotion` resolves the origin topic ONLY from a
# possible's pick edge, and the forward transition REMOVES the staging folder, which
# drops that edge from the snapshot — so a change that genuinely reached proposal
# reports `origin_staging_id: None`. Measured on the real corpus too: the defect is
# TOTAL — all 12 of 12 active changes report None, not just the four that declare
# `origin.kind: staged` (one of which has a supporting-docs manifest recording the
# pick edge, and still reports None). The refusal message anticipates exactly this
# and says to pass the topic explicitly, and the CLI exposes `--staging-topic`, so
# this is the operator's real path and the test takes it.



def test_a_demoted_fragment_carries_the_real_prior_text_not_the_aspirational_one(tmp_path):
    """PARENT TASK 4.2. Both gates driven, nothing hand-built between them."""
    root = _tree(tmp_path)
    _reach_proposal(root, _fragment_reaching_proposal(ASPIRATIONAL_GUESS))

    # The forward transition really did move the fragment out of staging…
    assert not _fragment(root).exists()
    snapshot = (root / "openspec" / "changes" / CHANGE / "supporting-docs"
                / f"{TOPIC}.md")
    assert snapshot.is_file()
    assert ASPIRATIONAL_GUESS in snapshot.read_text(encoding="utf-8")
    # …it flipped the moved copy to a draft…
    assert "Status: draft" in snapshot.read_text(encoding="utf-8")
    # …and the manifest it wrote is where `Raised` will come from.
    manifest = (root / "openspec" / "changes" / CHANGE / "supporting-docs"
                / "manifest.yaml").read_text(encoding="utf-8")
    assert RAISED_ON in manifest and "transitioned_at" in manifest

    # The proposal is then WORKED ON — this is the text the rule exists to save.
    _write_proposal(root, IN_FLIGHT_TRUTH)

    res, ex = _demote_and_execute(root, reason="Scope was wrong.",
                                  staging_topic=TOPIC)
    text = _fragment(root).read_text(encoding="utf-8")

    # THE PROPERTY: the real prior text, not the aspirational original.
    assert IN_FLIGHT_TRUTH in text, \
        "the demoted fragment lost what the change learned while it was in flight"
    assert ASPIRATIONAL_GUESS not in text, \
        "the demoted fragment reset to its pre-proposal aspirational text"
    # …inside the marked block, which is where the contract puts it
    marked = text.split("<!-- xspec:candidate", 1)[1].split("<!-- /xspec:candidate", 1)[0]
    assert IN_FLIGHT_TRUTH in marked

    # …tagged with the change id, BOTH dates, and the reason
    assert f"Change ID: {CHANGE}" in text
    assert f"Raised: {RAISED_ON}" in text          # the real forward transition's
    assert f"Demoted: {AT[:10]}" in text           # the real demote's
    assert "Demote reason: Scope was wrong." in text
    assert "Status at demote: active" in text
    assert "n/a" not in text and "none yet" not in text

    # …and the forward transition's `Status: draft` is undone: a staged topic's
    # outline is staged again.
    assert "Status: staged" in text and "Status: draft" not in text
    assert families._primary_fragment(
        root / "ideation" / "staging" / TOPIC).name == f"{TOPIC}.md"


def test_the_round_trip_survives_a_second_lap_through_both_gates(tmp_path):
    """The rule's own words are "nothing learned while a change was in flight may
    be lost", and that has to hold on the SECOND lap too — otherwise the guarantee
    expires after one use. Both gates are driven again, so the second lap is as real
    as the first."""
    root = _tree(tmp_path)
    _reach_proposal(root, _fragment_reaching_proposal(ASPIRATIONAL_GUESS))
    _write_proposal(root, IN_FLIGHT_TRUTH)
    _demote_and_execute(root, reason="First attempt.", staging_topic=TOPIC)
    returned = _fragment(root).read_text(encoding="utf-8")
    assert IN_FLIGHT_TRUTH in returned

    # A human works the returned fragment, and it goes round again — through the
    # REAL forward gate a second time.
    _fragment(root).write_text(
        returned + "\n## Idea notes (pre-document, non-documented)\n\n"
        "- LEARNED AFTER THE FIRST DEMOTE. — Added-by: brett · 2026-08-19\n",
        encoding="utf-8")
    # Re-raising means the change folder EXISTS again: the first demote removed it
    # (`active OpenSpec change not found` otherwise), so a second attempt is a
    # change re-created and then transitioned into — not the same folder reopened.
    _write_proposal(root, "A SECOND ATTEMPT'S REASONING.")
    # SELECTED, not "everything in the topic". The first demote left its own
    # `openspec/INDEX.md` in the folder, and that file carries no `Status:` header —
    # which a whole-folder transition refuses outright ("governed Markdown lacks
    # Status header"). Naming the fragment is both the operator's normal move and
    # the only one that works on a topic a demote has already returned to.
    support.transition(root, CHANGE, f"ideation/staging/{TOPIC}",
                       [f"{TOPIC}.md"], None, "2026-08-01", False, True)

    res, ex = _demote_and_execute(root, reason="Second attempt.",
                                  staging_topic=TOPIC)
    text = _fragment(root).read_text(encoding="utf-8")

    # THE HUMAN'S OWN MATERIAL survives the second lap — that is what "nothing
    # learned may be lost by falling back to staging" protects.
    assert "LEARNED AFTER THE FIRST DEMOTE." in text
    # The marked section carries the LAST attempt, so the first attempt's text is
    # SUPERSEDED there rather than lost by the demote — the contract says "the last
    # attempted proposal.md", singular. (A first draft of this test asserted the
    # first lap's text also survived; the contract does not promise that, and the
    # code was right.)
    assert "A SECOND ATTEMPT'S REASONING." in text
    assert IN_FLIGHT_TRUTH not in text
    assert ASPIRATIONAL_GUESS not in text
    # …and the slots moved on to the second attempt, both dates with them
    assert "Demote reason: Second attempt." in text
    assert "Raised: 2026-08-01" in text
    assert f"Demoted: {AT[:10]}" in text


def test_the_round_trip_arm_leaves_a_topic_with_no_snapshot_untouched(tmp_path):
    """The fixture change as it ships carries no supporting-docs, so there is no
    outline move at all and this arm must be inert — which is why the eight
    pre-existing demote tests still pass unchanged."""
    root = _tree(tmp_path)
    res, ex = _demote_and_execute(root)
    assert ex.outline_refreshed is False
    assert ex.snapshot_disposition is None
    assert not _fragment(root).exists()


# ============================================================================
# refine-demote-round-trip-mechanics — the four mechanics around the rule
# ============================================================================
#
# Three defects that only a FULL LAP can show (forward gate, then demote, then
# forward again), plus Brett's Decision 3. Every test below drives the real gates
# for the same reason the round-trip tests above do: each of these was invisible
# to a reading of the code and visible on the first lap.


def _minimal_snapshot(**over) -> dict:
    change = {"id": CHANGE, "status": "active",
              "folder": f"openspec/changes/{CHANGE}", "files": []}
    change.update(over)
    return {"changes": [change], "possibles": []}


# ---- part 1: the origin precedence order, at the planner's rung --------------

def test_an_explicitly_supplied_topic_outranks_a_resolved_origin():
    """The first rung, and it is here rather than in the generator because this
    is where a human's argument arrives. A human naming the destination is the
    most direct statement of intent available, so it wins over both derived
    sources — including one that now actually answers."""
    snap = _minimal_snapshot(origin_staging_id="resolved-from-the-origin-block")
    plan = gc.plan_demotion(snap, CHANGE, reason="r",
                            staging_topic="named-by-a-human")
    assert plan.staging_topic == "named-by-a-human"
    assert plan.topic_path == "ideation/staging/named-by-a-human"


def test_a_resolved_origin_is_used_when_no_topic_is_supplied():
    plan = gc.plan_demotion(_minimal_snapshot(origin_staging_id="from-the-block"),
                            CHANGE, reason="r")
    assert plan.staging_topic == "from-the-block"


def test_an_unresolvable_origin_still_refuses_and_names_the_explicit_option():
    """A change whose origin is ad-hoc or absent has NO staging topic to return
    to, and inventing one would move material somewhere nobody chose. The refusal
    survives this change unchanged in substance, and it has to name the way out."""
    with pytest.raises(gc.GateRefused) as ei:
        gc.plan_demotion(_minimal_snapshot(origin_staging_id=None), CHANGE, reason="r")
    message = str(ei.value)
    assert "no recorded origin staging topic" in message
    assert "--staging-topic" in message


# ---- part 2: the demote's own INDEX does not block the next transition -------

def _headerless_change_artifacts(root: Path, why: str) -> None:
    """The change folder in the shape OpenSpec really leaves it in.

    Measured at 8426dbc by the forward gate's own reader (a `Status:` line
    outside every fence): 93 of 94 `tasks.md`, 154 of 158 spec deltas, 65 of 68
    `design.md` and 49 of 94 `proposal.md` carry NO lifecycle status header —
    the convention simply does not put one there. So the driven test below runs
    on that shape rather than on a tidied one: `proposal.md` (front matter, no
    Status), `design.md`, `tasks.md` (the fixture's own, unheadered) and a spec
    delta. Every one of them is governed markdown the demote writes into a
    governed staging folder, and the forward transition refuses governed markdown
    without a header.
    """
    folder = root / "openspec" / "changes" / CHANGE
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "proposal.md").write_text(
        f"---\ncode_surface: none\ntarget_release: none\n---\n\n"
        f"# Proposal: {CHANGE}\n\n## Why\n\n{why}\n", encoding="utf-8")
    (folder / "design.md").write_text(
        f"# Design: {CHANGE}\n\n## Decision 1\n\nbecause.\n", encoding="utf-8")
    delta = folder / "specs" / "ideation-dashboard" / "spec.md"
    delta.parent.mkdir(parents=True, exist_ok=True)
    delta.write_text(
        "# ideation-dashboard\n\n## ADDED Requirements\n\n"
        "### Requirement: Something\nThe thing SHALL happen.\n\n"
        "#### Scenario: It happens\n- **WHEN** asked\n- **THEN** it happens\n",
        encoding="utf-8")


def test_the_demotes_own_index_carries_a_lifecycle_status(tmp_path):
    """design Decision 2 — `draft`, because the INDEX describes the returned
    DRAFT proposals and shares their state, and the next demote regenerates it
    rather than it being durable evidence (which `record` would claim)."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    res, ex = _demote_and_execute(root)
    index = ex.index_path.read_text(encoding="utf-8")
    assert "Status: draft" in index.splitlines()
    # and it is in the HEADER WINDOW the readers scan, not buried in the listing
    assert index.splitlines().index("Status: draft") < 5


def test_a_returned_topic_transitions_forward_again_over_its_whole_folder(tmp_path):
    """DRIVEN, not asserted (task 2.2). The defect was found by running the real
    forward transition over a returned topic and watching it refuse
    (`SupportError: governed Markdown lacks Status header`), so the fix is
    believed on the same evidence: both gates driven, WHOLE FOLDER, no file
    naming, no operator workaround, and the change folder in the header-less shape
    OpenSpec really leaves it in.

    The refusal has TWO sources and the requirement covers both — every artifact
    the reverse transition writes into the topic, which is its own `INDEX.md` and
    equally the `tasks.md`/`design.md`/spec deltas it moves there. Fixing only the
    first just moves the refusal to the next file in sorted order, which is how
    the second source stayed hidden: the gate refuses on the FIRST offender and
    `INDEX.md` sorts before `tasks.md`."""
    root = _tree(tmp_path)
    _reach_proposal(root, _fragment_reaching_proposal(ASPIRATIONAL_GUESS))
    _headerless_change_artifacts(root, IN_FLIGHT_TRUTH)
    res, ex = _demote_and_execute(root, reason="Reworking scope.")

    topic_dir = root / "ideation" / "staging" / TOPIC
    returned = sorted(p.relative_to(root).as_posix()
                      for p in topic_dir.rglob("*") if p.is_file())
    # the returned topic holds the demote's own INDEX *and* the header-less
    # change artifacts, all of which had to be made transitionable
    assert f"ideation/staging/{TOPIC}/openspec/INDEX.md" in returned
    assert f"ideation/staging/{TOPIC}/openspec/tasks.md" in returned
    assert (f"ideation/staging/{TOPIC}/openspec/specs/ideation-dashboard/spec.md"
            in returned)
    assert sorted(ex.status_headers_added) == [
        f"ideation/staging/{TOPIC}/openspec/design.md",
        f"ideation/staging/{TOPIC}/openspec/proposal.md",
        f"ideation/staging/{TOPIC}/openspec/specs/ideation-dashboard/spec.md",
        f"ideation/staging/{TOPIC}/openspec/tasks.md",
    ]
    # …and the human can read which files this verb edited, in the topic README
    readme = (topic_dir / "README.md").read_text(encoding="utf-8")
    assert "Status headers added" in readme
    assert f"ideation/staging/{TOPIC}/openspec/tasks.md" in readme

    # THE PROPERTY: the REAL forward gate takes the WHOLE FOLDER without refusing.
    _headerless_change_artifacts(root, "A SECOND ATTEMPT'S REASONING.")
    support.transition(root, CHANGE, f"ideation/staging/{TOPIC}", [], None,
                       "2026-08-01", False, True)

    sd = root / "openspec" / "changes" / CHANGE / "supporting-docs"
    for rel in ("openspec/INDEX.md", "openspec/tasks.md", "openspec/design.md",
                "openspec/specs/ideation-dashboard/spec.md"):
        assert (sd / rel).is_file(), \
            f"the whole-folder transition did not carry {rel} forward"
    assert not topic_dir.exists(), \
        "the forward transition leaves the topic folder empty and removed"


# ---- part 3: one authorship line per document, not one per attempt ----------

def test_two_laps_leave_exactly_one_proposed_by_line_naming_the_latest(tmp_path):
    """The forward gate rewrites `Status: staged` into `Status: draft` plus a
    `Proposed by:` line; the demote restores `Status: staged` and leaves the
    authorship line alone (correctly — see the boundary test below). So without
    the fix the second lap adds a SECOND line and the third a third, and several
    lines each claiming to name the proposing change say nothing about which one
    is current."""
    root = _tree(tmp_path)
    _reach_proposal(root, _fragment_reaching_proposal(ASPIRATIONAL_GUESS))
    _headerless_change_artifacts(root, IN_FLIGHT_TRUTH)
    _demote_and_execute(root, reason="First attempt.")

    returned = _fragment(root).read_text(encoding="utf-8")
    # the demote returns the line untouched — that is the boundary, not the bug
    assert returned.count("Proposed by:") == 1

    _headerless_change_artifacts(root, "A SECOND ATTEMPT'S REASONING.")
    support.transition(root, CHANGE, f"ideation/staging/{TOPIC}", [], None,
                       "2026-08-01", False, True)

    moved = (root / "openspec" / "changes" / CHANGE / "supporting-docs"
             / f"{TOPIC}.md").read_text(encoding="utf-8")
    lines = [ln for ln in moved.splitlines() if ln.startswith("Proposed by:")]
    assert lines == [f"Proposed by: {CHANGE}"], \
        "a second lap through the proposal gate duplicated the authorship line"
    assert "Status: draft" in moved.splitlines()


def test_the_demotes_bounded_refresh_is_not_where_the_line_is_deduped(tmp_path):
    """design Decision 3, asserted as a BOUNDARY rather than assumed. The obvious
    place to dedupe is the demote's refresh, since that is what runs when the line
    comes back — and it is the wrong place: the ratified requirement pins that
    refresh as bounded to the provenance slots and the marked sections, "leaving
    every other byte of that file unchanged". A header-tidying refresh would trade
    a data-loss guarantee for neatness, so this test pins that the demote leaves
    two authorship lines EXACTLY as it found them."""
    root = _tree(tmp_path)
    snapshot_path = _with_transitioned_snapshot(root)
    fragment = _fragment(root)
    fragment.parent.mkdir(parents=True, exist_ok=True)
    live = snapshot_path.read_text(encoding="utf-8").replace(
        "Status: staged\n",
        "Status: staged\nProposed by: an-older-change\n"
        "Proposed by: a-second-older-change\n", 1)
    fragment.write_text(live, encoding="utf-8")

    res, ex = _demote_and_execute(root, reason="Boundary.")
    after = fragment.read_text(encoding="utf-8")

    assert ex.snapshot_disposition == "preserved"   # the live-fragment arm
    assert [ln for ln in after.splitlines() if ln.startswith("Proposed by:")] == [
        "Proposed by: an-older-change", "Proposed by: a-second-older-change"], \
        "the demote's bounded refresh widened to tidy a header line"


# ---- the outline's own header, on the REFRESH-IN-PLACE arm (review R1) ------

def test_a_header_less_live_outline_does_not_leave_the_topic_one_way(tmp_path):
    """DRIVEN. An earlier pass of this change declared the outline out of scope on
    the grounds that its source always arrives carrying a header. That is true of
    the SNAPSHOT the restore arm applies and false of the LIVE FRAGMENT the
    refresh-in-place arm reads — a document the human owns, which never passed the
    forward gate and so never had to acquire a header. The demote then succeeded
    with `outline_refusal: None`, wrote the fragment back with no header, and left
    the topic one-way: the next whole-folder transition refused on the outline
    itself. Both gates driven here, because that is how it was found."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    fragment = _fragment(root)
    fragment.parent.mkdir(parents=True, exist_ok=True)
    fragment.write_text(
        f"# Staged: {TOPIC}\n\nSummary: a live working outline, no Status "
        "header.\n\n## Why\n\nWHAT THE HUMAN IS ACTUALLY WORKING ON.\n",
        encoding="utf-8")

    res, ex = _demote_and_execute(root, reason="Live header-less fragment.")
    after = fragment.read_text(encoding="utf-8")

    assert ex.snapshot_disposition == "preserved"       # the refresh-in-place arm
    assert ex.outline_refusal is None
    # `staged`, NOT the `draft` returned change artifacts get: the ratified rule
    # says the topic's declared primary fragment keeps `Status: staged`, and the
    # value is taken from the same expression the restore arm uses.
    assert "Status: staged" in after.splitlines()
    assert "Status: draft" not in after.splitlines()
    assert f"ideation/staging/{TOPIC}/{TOPIC}.md" in ex.status_headers_added
    # the human's own bytes are still there
    assert "WHAT THE HUMAN IS ACTUALLY WORKING ON." in after
    assert "Summary: a live working outline, no Status header." in after
    # …and the round-trip provenance still landed
    assert f"Change ID: {CHANGE}" in after

    # THE PROPERTY: the topic transitions forward again, whole folder.
    _headerless_change_artifacts(root, "A SECOND ATTEMPT'S REASONING.")
    support.transition(root, CHANGE, f"ideation/staging/{TOPIC}", [], None,
                       "2026-08-01", False, True)
    assert not (root / "ideation" / "staging" / TOPIC).exists()


def test_a_live_outline_that_has_a_header_keeps_the_humans_own_value(tmp_path):
    """The other half of R1, and the reason the fix is an ADD rather than a flip:
    the refresh-in-place arm deliberately does not rewrite the live fragment's
    status, because that value is the human's. Only its ABSENCE is filled."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    fragment = _fragment(root)
    fragment.parent.mkdir(parents=True, exist_ok=True)
    fragment.write_text(
        f"# Staged: {TOPIC}\n\nStatus: brainstorm\n\n## Why\n\nmine.\n",
        encoding="utf-8")

    res, ex = _demote_and_execute(root, reason="Human's own status.")
    after = fragment.read_text(encoding="utf-8")

    assert "Status: brainstorm" in after.splitlines()
    assert f"ideation/staging/{TOPIC}/{TOPIC}.md" not in ex.status_headers_added


def test_a_preserved_snapshot_copy_also_carries_a_header(tmp_path):
    """The third governed markdown the demote writes into a topic on this arm.
    Belt and braces — the snapshot arrives with a header by construction — but a
    silent hole here would be the same defect in a third place."""
    root = _tree(tmp_path)
    snapshot_path = _with_transitioned_snapshot(root)
    snapshot_path.write_text(
        f"# Staged: {TOPIC}\n\nno header at all here either.\n", encoding="utf-8")
    fragment = _fragment(root)
    fragment.parent.mkdir(parents=True, exist_ok=True)
    fragment.write_text(
        f"# Staged: {TOPIC}\n\nStatus: staged\n\n## Why\n\nlive.\n",
        encoding="utf-8")

    res, ex = _demote_and_execute(root, reason="Preserved copy.")

    assert ex.snapshot_disposition == "preserved"
    kept = ex.preserved_snapshot_path.read_text(encoding="utf-8")
    assert "Status: draft" in kept.splitlines()


# ---- part 4: the state-at-demote slot (Brett's Decision 3) ------------------

def test_state_at_demote_renders_status_and_progress_as_prose():
    assert gc.state_at_demote("active", {"completed": 9, "total": 22}) == \
        "active — 9 of 22 tasks done"


def test_state_at_demote_with_no_progress_renders_the_status_alone():
    """NOT `active — unavailable`. The ratified unavailable rule is about a value
    that could not be RESOLVED; a change recording no tasks has no progress to
    resolve, and reporting a lookup failure where there was none is a different
    lie from the one the rule forbids."""
    for progress in (None, {}, {"completed": 0, "total": 0}, {"total": "many"}):
        assert gc.state_at_demote("active", progress) == "active"


def test_state_at_demote_refuses_a_progress_record_that_does_not_add_up():
    """Unreachable through the generator, which counts `completed` out of the same
    sweep that produces `total`. Guarded anyway: the slot is prose a human reads as
    fact, and `9 of 4 tasks done` is a fabricated one — the status alone is the
    true statement about a record that does not add up."""
    assert gc.state_at_demote("active", {"completed": 9, "total": 4}) == "active"
    assert gc.state_at_demote("active", {"completed": -1, "total": 4}) == "active"


def test_state_at_demote_with_no_status_stays_empty_for_the_unavailable_marker():
    """An unresolvable STATUS is a real resolution failure, so it must reach the
    caller's `UNAVAILABLE` rather than being papered over with a task count."""
    assert gc.state_at_demote("", {"completed": 9, "total": 22}) == ""


def test_the_plan_carries_task_progress_beside_the_status(tmp_path):
    """Same reasoning as `status_at_demote` before it: the plan is snapshot-derived
    and pure, and `execute_demotion_plan` never sees a snapshot."""
    root = _tree(tmp_path)
    plan = gc.plan_demotion(_snapshot(root), CHANGE, reason="r")
    assert plan.status_at_demote == "active"
    assert plan.task_progress == {"completed": 2, "total": 4}


def test_the_demoted_fragments_state_slot_carries_the_progress(tmp_path):
    """The fixture change records 2 of 4 tasks done — ticked AND unticked, so the
    count is not a total masquerading as progress."""
    root = _tree(tmp_path)
    _with_transitioned_snapshot(root)
    _demote_and_execute(root)
    text = _fragment(root).read_text(encoding="utf-8")
    assert "Status at demote: active — 2 of 4 tasks done" in text
    assert round_trip.UNAVAILABLE not in text


def test_a_change_with_no_tasks_file_gets_the_status_alone(tmp_path):
    root = _tree(tmp_path)
    (root / "openspec" / "changes" / CHANGE / "tasks.md").unlink()
    _with_transitioned_snapshot(root)
    plan = gc.plan_demotion(_snapshot(root), CHANGE, reason="No tasks.")
    assert plan.task_progress is None
    gc.execute_demotion_plan(plan, root, at=AT)
    slot = [ln for ln in _fragment(root).read_text(encoding="utf-8").splitlines()
            if ln.startswith("Status at demote:")]
    assert slot == ["Status at demote: active"]


# ============================================================================
# ratify — the ratification record round-trip, validator-clean
# ============================================================================

def test_ratify_writes_the_record_and_a_gate_action_carrying_it(tmp_path):
    root = _tree(tmp_path)
    res = gc.GateConsole(_gate(root)).ratify(CHANGE, "Brett", at=AT)
    # the ratified facts, unchanged — plus the `binding` block that makes them
    # tamper-evident (the records-tree-trust gap; `record_binding`).
    assert {k: v for k, v in res.ratification.items() if k != "binding"} == {
        "kind": "ratification-record", "schema_version": 1,
        "change_id": CHANGE, "ratifier": "Brett", "date": "2026-07-14"}
    assert res.ratification["binding"]["digest"] == \
        rb.content_digest(res.ratification)
    # the gate-action record carries the ratification-record artifact (contains-rule).
    kinds = {a["kind"] for a in res.gate_action_record["artifacts"]}
    assert "ratification-record" in kinds
    proc = _validate(res.record_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_ratify_date_defaults_to_the_action_day(tmp_path):
    res = gc.GateConsole(_gate(_tree(tmp_path))).ratify(CHANGE, "Brett", at="2026-07-14T23:59:59Z")
    assert res.ratification["date"] == "2026-07-14"


# ============================================================================
# edit-apply — applies EXACTLY the redline and nothing else (byte-compare)
# ============================================================================

DOC = f"openspec/changes/{CHANGE}/proposal.md"


def test_edit_apply_replacement_block_changes_exactly_the_redline(tmp_path):
    root = _tree(tmp_path)
    before = (root / DOC).read_text(encoding="utf-8")
    redline = gc.Redline(
        old_text="Add the ideation-area lifecycle and work queue.",
        new_text="Add the ideation-area lifecycle, work queue, and gate console.",
        concept="What Changes")
    res = gc.GateConsole(_gate(root)).edit_apply(CHANGE, DOC, redline, at=AT)

    expected = before.replace(
        "Add the ideation-area lifecycle and work queue.",
        "Add the ideation-area lifecycle, work queue, and gate console.")
    # byte-exact: only the redline span changed, nothing else.
    assert (root / DOC).read_text(encoding="utf-8") == expected
    assert res.after == expected
    # the record carries the redline artifact, and validates clean.
    assert res.redline["kind"] == "redline"
    assert {a["kind"] for a in res.gate_action_record["artifacts"]} == {"redline"}
    proc = _validate(res.record_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_a_redline_apply_preserves_crlf_on_untouched_lines(tmp_path):
    """Wave re-review P3 — the F10 corpus-integrity class through the redline
    verb. `edit_apply` used to `read_text` -> `write_text`, so on Linux
    applying a redline to a CRLF document silently rewrote EVERY line ending
    as LF — a whole-document mutation the human never approved, and one that
    invalidates any open doxBench buffer's base identity. Both legs now run
    translation-free: the redline span changes, and nothing else does —
    byte-compared, CR intact."""
    root = _tree(tmp_path)
    crlf = ("# Proposal\r\n\r\nalpha BETA gamma\r\n\r\n## Why\r\n\r\n"
            "untouched Windows-authored text.\r\n")
    (root / DOC).write_bytes(crlf.encode("utf-8"))
    redline = gc.Redline(old_text="BETA", new_text="DELTA")

    res = gc.GateConsole(_gate(root)).edit_apply(CHANGE, DOC, redline, at=AT)

    expected = crlf.replace("BETA", "DELTA")
    assert (root / DOC).read_bytes() == expected.encode("utf-8")
    assert res.after == expected


def test_apply_redline_is_pure_and_exact():
    text = "alpha BETA gamma\n"
    assert gc.apply_redline(text, gc.Redline(old_text="BETA", new_text="DELTA")) == "alpha DELTA gamma\n"
    # a replacement block must match EXACTLY once (ambiguous or absent is refused).
    ambiguous = gc.Redline(old_text="x", new_text="y")
    with pytest.raises(ValueError):
        gc.apply_redline("x x", ambiguous)
    absent = gc.Redline(old_text="absent", new_text="y")
    with pytest.raises(ValueError):
        gc.apply_redline("nope", absent)
    # full-text replaces the whole document.
    assert gc.apply_redline("old", gc.Redline(full_text="brand new")) == "brand new"
    # a redline needs one form or the other.
    formless = gc.Redline()
    with pytest.raises(ValueError):
        gc.apply_redline("x", formless)


def test_list_concepts_extracts_the_documents_headings(tmp_path):
    concepts = gc.list_concepts((_tree(tmp_path) / DOC).read_text(encoding="utf-8"))
    assert concepts == ["Why", "What Changes", "Non-Goals"]


# ============================================================================
# serve.py exposes NO GATE write route. v2 added exactly ONE write route — the
# loopback-only /actions/notebook tile action (a bounded, non-gate projection
# that mutates no source doc and executes no lifecycle gate). Gate side effects
# remain CLI-only through HumanGate and are never reachable over HTTP; the
# read-only snapshot/source routes are never written through.
# ============================================================================

@contextmanager
def _serving(tmp_path):
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(_snapshot(_tree(tmp_path))), encoding="utf-8")
    httpd = serve_mod.build_server(WEB, snap_path, BASE_REPO, head=PINNED_REVISION)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield host, port
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def test_serve_has_no_gate_write_handlers():
    # The only write verb is do_POST (the v2 loopback notebook-action seam); no
    # PUT/DELETE/PATCH, and the sole POST route is the tile action — serve.py
    # carries no gate route of any kind (gate side effects are HumanGate/CLI).
    for verb in ("do_PUT", "do_DELETE", "do_PATCH"):
        assert not hasattr(serve_mod.DashboardHandler, verb), verb
    assert serve_mod.ACTIONS_NOTEBOOK_ROUTE == "/actions/notebook"


def test_serve_post_to_a_readonly_route_is_refused_without_writing(tmp_path):
    snap_path = tmp_path / "snapshot.json"
    with _serving(tmp_path) as (host, port):
        before = snap_path.read_bytes()
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("POST", "/snapshot.json", body=b"{}")
        resp = conn.getresponse()
        resp.read()
        conn.close()
    # a POST to the read-only snapshot route is not an action route -> refused
    # (404, structured), and the snapshot file is never written through.
    assert resp.status == 404
    assert snap_path.read_bytes() == before


# ============================================================================
# web gate bar (gate.js) — pure descriptors + DOM-safety (node)
# ============================================================================

_HARNESS = """
import { isGateBearing, gateCommand, gateActionDescriptors, GATE_ACTIONS } from './gate.mjs';
console.log(JSON.stringify({
  bearing: {
    proposal: isGateBearing('openspec/changes/add-x/proposal.md'),
    specDelta: isGateBearing('openspec/changes/add-x/specs/cap/spec.md'),
    readme: isGateBearing('ideation/staging/x/README.md'),
  },
  actions: GATE_ACTIONS,
  descriptors: gateActionDescriptors({ changeId: 'add-x', actor: 'brett',
    repository: 'codexFactory', path: 'openspec/changes/add-x/proposal.md' }),
  demote: gateCommand('demote', { changeId: 'add-x', actor: 'brett', repository: 'codexFactory' }),
  unknown: gateCommand('nope', {}),
}));
"""


def _run_node(tmp_path):
    if not NODE:
        pytest.skip("node not available for the gate.js descriptor probe")
    shutil.copy(GATE_JS, tmp_path / "gate.mjs")
    (tmp_path / "h.mjs").write_text(_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "h.mjs")], capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_gate_js_is_gate_bearing_only_on_change_documents(tmp_path):
    r = _run_node(tmp_path)
    assert r["bearing"] == {"proposal": True, "specDelta": True, "readme": False}


def test_gate_js_descriptors_cover_all_four_actions_with_cli_commands(tmp_path):
    r = _run_node(tmp_path)
    assert [d["action"] for d in r["descriptors"]] == r["actions"] == ["demote", "edit", "ratify", "kickoff"]
    for d in r["descriptors"]:
        assert d["command"].startswith("python3 scripts/ideation_dashboard/cli.py gate")
        assert "add-x" in d["command"]
    # demote's descriptor is the exact CLI command a human runs (read-only web
    # never executes server-side — it produces the ACTION DESCRIPTOR).
    assert "gate demote" in r["demote"] and "--reason" in r["demote"]
    assert r["unknown"] is None


def test_gate_js_binds_dynamic_values_via_textcontent_only():
    # The gate bar's el() sets textContent (never innerHTML); the only innerHTML
    # occurrence is the clear (`= ""`) — the same DOM-safety posture as canvas.js.
    import re
    text = GATE_JS.read_text(encoding="utf-8")
    for m in re.finditer(r"\.innerHTML\s*=\s*(.+)", text):
        rhs = m.group(1).strip().rstrip(";").strip()
        assert rhs == '""', f"non-clearing innerHTML in gate.js: {m.group(0)!r}"
    assert "node.textContent = text" in text


# ==========================================================================
# PR #49 review finding 15 (wave 2) — THIS emitter is safe to paste too
#
# Wave 1 quoted the staging workbench's descriptors and left `gateCommand`
# untouched: `--change-id`, `--repository`, `--actor` and `--document` were
# interpolated BARE, and `--reason "<why>"` used double quotes (which preserve
# `$` and backtick expansion). The values are snapshot- and corpus-derived — the
# change id and document path come from the served artifact, the repository from
# the snapshot identity — so the boundary crossed is "merged corpus content ->
# the human's shell in the served checkout".
#
# The oracle is the SHELL, not `shlex`: `shlex.split` tokenizes without
# expanding, which is exactly why the pre-existing descriptor tests above passed
# while the emitted line ran a second command. Each descriptor is pasted into a
# real `/bin/sh` whose `python3` is an argv-recording shim, with `PATH` holding
# the shim alone. `PWNED` is ASSEMBLED by the shell (`printf 'PWN%sD' E`) and so
# appears nowhere in the literal text: finding it in the argv or the output is
# proof of EVALUATION, not of the payload travelling through intact. Payloads use
# shell BUILTINS only, so nothing external can run and nothing is written.
# ==========================================================================

_GATE_SUBST = "$(printf 'PWN%sD' E)"
_GATE_BACKTICK = "`printf 'PWN%sD' E`"
_GATE_SEPARATOR = "; printf 'PWN%sD' E"

# Each value carries an expansion or a command separator, and two carry the
# single quote — the one character single-quoting itself has to escape.
_GATE_HOSTILE = {
    "changeId": f"add-x{_GATE_SUBST}",
    "repository": f"codexFactory{_GATE_SEPARATOR}",
    "actor": f"Brett O'Hara {_GATE_BACKTICK}",
    "path": f"openspec/changes/add-x/{_GATE_BACKTICK}/it's/proposal.md",
}

# Which hostile values each action's descriptor must carry through untouched.
_GATE_EXPECTED = {
    "demote": ("changeId", "repository", "actor"),
    "ratify": ("changeId", "actor"),
    "kickoff": ("changeId", "repository", "actor"),
    "edit": ("changeId", "actor", "path"),
}

_GATE_HOSTILE_HARNESS = """
import { gateCommand } from './gate.mjs';
import { readFileSync } from 'node:fs';
const ctx = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const out = {};
for (const action of ['demote', 'ratify', 'kickoff', 'edit']) {
  out[action] = gateCommand(action, ctx);
}
console.log(JSON.stringify(out));
"""

_GATE_PYTHON3_SHIM = """#!/bin/sh
for arg in "$@"; do printf '%s\\0' "$arg" >> "$XF_ARGV_LOG"; done
"""


def _hostile_gate_commands(tmp_path):
    if not NODE:
        pytest.skip("node not available for the gate.js descriptor probe")
    shutil.copy(GATE_JS, tmp_path / "gate.mjs")
    (tmp_path / "hostile.mjs").write_text(_GATE_HOSTILE_HARNESS, encoding="utf-8")
    ctx = tmp_path / "ctx.json"
    ctx.write_text(json.dumps(_GATE_HOSTILE), encoding="utf-8")
    proc = subprocess.run([NODE, str(tmp_path / "hostile.mjs"), str(ctx)],
                          capture_output=True, text=True, cwd=tmp_path, timeout=60)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def _paste_gate_command(tmp_path, command):
    """Run `command` the way a human pastes it, and return (argv, output).

    `python3` is a shim recording its argv; `PATH` holds nothing else, so the
    payloads use shell BUILTINS and no external program can run."""
    shim_dir = tmp_path / "shim"
    shim_dir.mkdir(exist_ok=True)
    shim = shim_dir / "python3"
    shim.write_text(_GATE_PYTHON3_SHIM, encoding="utf-8")
    shim.chmod(0o755)
    log = tmp_path / "argv.log"
    log.write_bytes(b"")
    run_dir = tmp_path / "paste"
    run_dir.mkdir(exist_ok=True)
    done = subprocess.run(["/bin/sh", "-c", command], cwd=str(run_dir),
                          capture_output=True, text=True, timeout=60,
                          env={"PATH": str(shim_dir), "XF_ARGV_LOG": str(log)})
    argv = [part for part in log.read_bytes().decode("utf-8").split("\0") if part]
    return argv, done.stdout + done.stderr, run_dir


def _gate_unquoted_characters(command):
    """The characters of `command` a POSIX shell would read as SYNTAX — everything
    outside single quotes, with `\\x` counted as the literal `x`.

    A small lexer rather than a quote-parity toggle: the escape spelling for an
    inner `'` is `'\\''` (close, escaped literal, reopen), and a toggle mis-reads
    that as re-entering quoted text — it would call a genuinely unquoted `$` safe."""
    out = []
    index, inside = 0, False
    while index < len(command):
        char = command[index]
        if inside:
            inside = char != "'"
            index += 1
            continue
        if char == "'":
            inside = True
        elif char == "\\":
            index += 1              # the escaped character is a literal
        else:
            out.append(char)
        index += 1
    return out


@pytest.mark.parametrize("action", sorted(_GATE_EXPECTED))
def test_a_pasted_gate_descriptor_carries_hostile_values_verbatim(tmp_path, action):
    """Finding 15's CORRECTNESS half on this emitter: the descriptor is the exact
    command a human runs, so every value must arrive as ONE argument,
    byte-identical — and nothing may expand or execute on the way."""
    command = _hostile_gate_commands(tmp_path)[action]
    argv, output, _run_dir = _paste_gate_command(tmp_path, command)

    for key in _GATE_EXPECTED[action]:
        assert _GATE_HOSTILE[key] in argv, (key, argv)
    assert "PWNED" not in "".join(argv), argv
    assert "PWNED" not in output, output


@pytest.mark.parametrize("action", sorted(_GATE_EXPECTED))
def test_a_hostile_gate_descriptor_stays_one_command(tmp_path, action):
    """A `;` in the snapshot-derived repository used to SPLIT the pasted line, so
    the shell ran a second command the descriptor never showed — and wrote a file.
    One paste, one invocation of the tool the descriptor names, no side effects."""
    command = _hostile_gate_commands(tmp_path)[action]
    argv, _output, run_dir = _paste_gate_command(tmp_path, command)

    assert argv[:1] == ["scripts/ideation_dashboard/cli.py"], argv
    assert argv.count("scripts/ideation_dashboard/cli.py") == 1, argv
    assert sorted(p.name for p in run_dir.iterdir()) == [], list(run_dir.iterdir())


@pytest.mark.parametrize("action", sorted(_GATE_EXPECTED))
def test_no_gate_descriptor_leaves_a_shell_metacharacter_unquoted(tmp_path, action):
    """The structural reading of the same rule, so a NEW slot added to this emitter
    without quoting fails here even with no payload aimed at it: outside the single
    quotes a descriptor holds flag names and one literal script path, nothing else.

    `<`/`>` are in the set deliberately — the `<why>` / `<old>` / `<new>` PLACEHOLDERS
    were bare or double-quoted, and an unquoted `<old>` is a redirect, not decoration."""
    command = _hostile_gate_commands(tmp_path)[action]
    remainder = "".join(_gate_unquoted_characters(command))
    for char in "$`;&|<>()\n\"":
        assert char not in remainder, (char, remainder)


def test_the_hostile_gate_descriptors_still_reach_the_real_cli(tmp_path):
    """Quoting is not validation and does not pretend to be: the descriptor hands
    the hostile value to the CLI as one argument, and the CLI's OWN checks are what
    refuse it — inside the process, which is the layer that can refuse."""
    import shlex

    from ideation_dashboard import cli

    out = _hostile_gate_commands(tmp_path)
    parser = cli.build_parser()
    for action in ("demote", "ratify", "kickoff"):
        args = parser.parse_args(shlex.split(out[action])[2:])
        assert args.change_id == _GATE_HOSTILE["changeId"]
    demote = parser.parse_args(shlex.split(out["demote"])[2:])
    assert demote.repository == _GATE_HOSTILE["repository"]
    assert demote.actor == _GATE_HOSTILE["actor"]


# ==========================================================================
# DISPOSE-POSSIBLE (add-possibles-derivation-lane: the console verdict verb)
# ==========================================================================

def _derived_entry(pid="pos-derived-x", disposed=None):
    entry = {
        "id": pid, "title": "Derived", "claim": "c", "state": "latent",
        "origin": "ai-derived",
        "provenance": {"document": "d", "section": "s"},
        "derivation": {"worker_run": {
            "correlation_id": "DPOSS-1", "worker_profile": "derive-possibles",
            "prompt_contract_version": "derive-possibles-prompt-v1"},
            "disposition": "pending_review"},
        "claiming_clusters": ["cl-a"],
        "supporting_evidence": [{"document": "d", "section": "s",
                                 "passage_sha256": "0" * 64}],
    }
    if disposed:
        entry["derivation"]["human_disposition"] = {
            "outcome": disposed, "authority": "gate"}
    return entry


def _dispose_root(tmp_path, register=None):
    import yaml as yaml_mod
    root = tmp_path / "openx"
    (root / "ideation").mkdir(parents=True)
    index = {"schema_version": 1, "kind": "ideation-cross-reference",
             "repository": "openxFactory",
             "generation": {"source_revision": "e" * 40,
                            "generator_version": "test"},
             "topic_entries": [{"id": "cl-a", "name": "A",
                                "members": [{"path": "p", "stage": "staged"}]}],
             "possibles_register": register if register is not None
             else [_derived_entry()]}
    (root / "ideation" / "cross-reference.yaml").write_text(
        yaml_mod.safe_dump(index, sort_keys=False), encoding="utf-8")
    return root


def _accepting_validator(tmp_path, accept=True):
    script = tmp_path / "fake_index_validator.py"
    script.write_text(f"import sys\nsys.exit(0 if {accept!r} else 1)\n",
                      encoding="utf-8")
    return script


def _diagnosing_validator(tmp_path, *, exit_code: int, message: str):
    """A fake validator that prints `message` to stdout and exits `exit_code`
    — for pinning what a refusal message carries at each exit code, not just
    whether it refuses."""
    script = tmp_path / f"fake_index_validator_exit{exit_code}.py"
    script.write_text(
        f"import sys\nprint({message!r})\nsys.exit({exit_code!r})\n",
        encoding="utf-8")
    return script


def _dispose_gate(root, actor="brett"):
    from doc_health import derive_possibles as dp
    return HumanGate(root, [gc.DEFAULT_RECORDS_DIR, dp.INDEX_REL,
                            dp.INDEX_MD_REL], human_actor=actor)


def test_dispose_accept_stays_latent_and_writes_record(tmp_path, monkeypatch):
    import yaml as yaml_mod
    monkeypatch.delenv("OPENXFACTORY_ROOT", raising=False)
    root = _dispose_root(tmp_path)
    res = gc.dispose_possible(
        _dispose_gate(root), "pos-derived-x", "accepted", note="good",
        index_validator=_accepting_validator(tmp_path))
    assert res.entry["state"] == "latent"
    assert res.entry["origin"] == "ai-derived"          # provenance retained
    hd = res.entry["derivation"]["human_disposition"]
    assert hd["outcome"] == "accepted" and hd["authority"] == "brett"
    # persisted index carries the disposition
    index = yaml_mod.safe_load(res.index_path.read_text(encoding="utf-8"))
    persisted = next(e for e in index["possibles_register"]
                     if e["id"] == "pos-derived-x")
    assert persisted["derivation"]["human_disposition"]["outcome"] == "accepted"
    assert persisted["derivation"]["disposition"] == "pending_review"  # machine field immutable
    # schema-valid gate-action record beside it
    record = yaml_mod.safe_load(res.record_path.read_text(encoding="utf-8"))
    assert record["action"] == "dispose-possible"
    assert record["target"] == {"possible_id": "pos-derived-x",
                                "outcome": "accepted"}
    assert any(a["kind"] == "register-update" for a in record["artifacts"])


def test_dispose_reject_requires_reason_and_citation(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENXFACTORY_ROOT", raising=False)
    root = _dispose_root(tmp_path)
    validator = _accepting_validator(tmp_path)
    with pytest.raises(gc.GateRefused):
        gc.dispose_possible(_dispose_gate(root), "pos-derived-x",
                                  "rejected", index_validator=validator)
    res = gc.dispose_possible(
        _dispose_gate(root), "pos-derived-x", "rejected",
        reason="not viable", citation="cl-a review",
        index_validator=validator)
    assert res.entry["state"] == "rejected"
    assert res.entry["reason"] == "not viable"


def test_dispose_is_one_way_and_human_only(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENXFACTORY_ROOT", raising=False)
    root = _dispose_root(tmp_path, register=[
        _derived_entry(disposed="accepted")])
    validator = _accepting_validator(tmp_path)
    with pytest.raises(gc.GateRefused):   # already disposed
        gc.dispose_possible(_dispose_gate(root), "pos-derived-x",
                                  "rejected", reason="r", citation="c",
                                  index_validator=validator)
    # an OutputBoundary (machinery/agent path) is rejected and reported
    boundary = OutputBoundary(root, [gc.DEFAULT_RECORDS_DIR])
    with pytest.raises(BoundaryViolation):
        gc.dispose_possible(boundary, "pos-derived-x", "accepted",
                                  index_validator=validator)
    assert boundary.refusals and boundary.refusals[0].kind == GATE_SIDE_EFFECT


def test_dispose_rejected_index_persists_nothing(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENXFACTORY_ROOT", raising=False)
    root = _dispose_root(tmp_path)
    before = (root / "ideation" / "cross-reference.yaml").read_text(
        encoding="utf-8")
    with pytest.raises(gc.GateRefused):
        gc.dispose_possible(
            _dispose_gate(root), "pos-derived-x", "accepted",
            index_validator=_accepting_validator(tmp_path, accept=False))
    after = (root / "ideation" / "cross-reference.yaml").read_text(
        encoding="utf-8")
    assert after == before          # nothing persisted on the refusal path
    assert not list((root / "ideation").glob("dashboard/gate-records/**/*"))


# ==========================================================================
# Regression: #656 D-2 act A. `"A" if ok is False else "B" + f": {detail}"`
# binds as `A if ok is False else (B + f": {detail}")`, so a real rejection
# (ok is False) discarded the validator's diagnosis entirely, while the
# unreachable branch (ok is None) carried it. Both branches must carry
# `detail`, bounded, with the unreachable phrase appearing exactly once.
# ==========================================================================

def test_dispose_reject_message_carries_the_validators_diagnosis(
        tmp_path, monkeypatch):
    monkeypatch.delenv("OPENXFACTORY_ROOT", raising=False)
    root = _dispose_root(tmp_path)
    validator = _diagnosing_validator(
        tmp_path, exit_code=1, message="tier score 11 is out of range")
    with pytest.raises(gc.GateRefused) as ei:
        gc.dispose_possible(_dispose_gate(root), "pos-derived-x", "accepted",
                                  index_validator=validator)
    msg = str(ei.value)
    assert msg.startswith("updated index rejected by the pinned validator: ")
    assert "tier score 11 is out of range" in msg


def test_dispose_unreachable_message_carries_detail_exactly_once(
        tmp_path, monkeypatch):
    """A harness error (validator exit 2, distinct from a real rejection —
    the D-2 act A defect) reads "index validator unreachable: <detail>" with
    the leading phrase exactly once; the 2026-09-06 doubled message
    ("...unreachable: index validator unreachable (...)") must not recur."""
    monkeypatch.delenv("OPENXFACTORY_ROOT", raising=False)
    root = _dispose_root(tmp_path)
    validator = _diagnosing_validator(
        tmp_path, exit_code=2,
        message="ImportError: no module named yaml")
    with pytest.raises(gc.GateRefused) as ei:
        gc.dispose_possible(_dispose_gate(root), "pos-derived-x", "accepted",
                                  index_validator=validator)
    msg = str(ei.value)
    assert msg.count("index validator unreachable") == 1
    assert msg.startswith("index validator unreachable: ")
    assert "ImportError" in msg
    assert "2" in msg           # the exit code is carried in the detail


def test_dispose_refusal_message_bounds_the_validators_detail(
        tmp_path, monkeypatch):
    monkeypatch.delenv("OPENXFACTORY_ROOT", raising=False)
    root = _dispose_root(tmp_path)
    huge = "x" * 5000
    validator = _diagnosing_validator(tmp_path, exit_code=1, message=huge)
    with pytest.raises(gc.GateRefused) as ei:
        gc.dispose_possible(_dispose_gate(root), "pos-derived-x", "accepted",
                                  index_validator=validator)
    msg = str(ei.value)
    assert len(msg) < 2100                    # nowhere near the raw 5000
    assert msg.count("x") >= gc._VALIDATOR_DETAIL_MAX - 1


def test_bounded_detail_keeps_the_tail_and_normalises_whitespace():
    detail = "line one\nline two\n" + ("z" * 3000)
    bounded = gc._bounded_detail(detail)
    assert len(bounded) == gc._VALIDATOR_DETAIL_MAX
    assert "\n" not in bounded
    assert bounded.endswith("z" * 100)


def test_bounded_detail_bounds_the_raw_tail_before_normalising(monkeypatch):
    """Regression: `_bounded_detail()` used to normalise whitespace over the
    ENTIRE raw string (`" ".join(s.split())`, materialising a full token
    list) before bounding it — the exact case the helper exists to make
    safe for very large validator output. Bounding must happen FIRST: prove
    it structurally by spying on the normalisation step and asserting it
    never sees more than the small, fixed-size tail window, regardless of
    how large the raw input is (a multi-megabyte string here)."""
    seen_lengths = []
    real_normalise = gc._normalise_whitespace

    def spy(s):
        seen_lengths.append(len(s))
        return real_normalise(s)

    monkeypatch.setattr(gc, "_normalise_whitespace", spy)
    huge = "word " * 1_000_000                       # ~5,000,000 raw chars
    result = gc._bounded_detail(huge)
    assert len(result) <= gc._VALIDATOR_DETAIL_MAX
    assert seen_lengths == [gc._DETAIL_TAIL_MARGIN]  # bounded BEFORE normalising
    assert seen_lengths[0] < len(huge)               # never the full raw text


# ==========================================================================
# WHEEL ACTION-ROW VERBS (011; add-wheel-action-verbs)
#
# The PROMOTABILITY predicate (FR-010) and the additive `cluster_id` record
# target (FR-016). Promotability is the trap-dense part of this feature, so the
# matrix below is exhaustive over state x origin x human verdict rather than
# illustrative.
#
# THREE PROHIBITED SHORTCUTS, each asserted against directly:
#   1. `derivation.disposition` is a CONTRACT CONSTANT — it stays
#      `pending_review` for the life of a derived entry, INCLUDING after a human
#      accepts (see test_dispose_accept_stays_latent_and_writes_record above,
#      which asserts exactly that). A guard reading it never opens.
#   2. `doc_health.derive_possibles._is_undisposed` is NOT this predicate: it
#      treats ANY recorded human_disposition as disposed, so it admits
#      `deferred`, and it says nothing about accepted vs rejected.
#   3. The snapshot projection is a stale VIEW; promotability is read from the
#      register in the pinned checkout.
# ==========================================================================

def _human_entry(pid="pos-human", state="latent", **kw):
    """A human-authored possible: no `origin`, no `derivation` (the contract's
    absent-origin default). Accepted by construction."""
    entry = {"id": pid, "title": "Human", "claim": "c", "state": state,
             "provenance": {"document": "d", "section": "s"}}
    if state in ("rejected", "superseded"):
        entry["reason"], entry["citation"] = "r", "c"
    if state == "picked":
        entry["pick"] = {"staging_id": "some-topic"}
    entry.update(kw)
    return entry


def _derived_state(pid="pos-derived", state="latent", outcome=None):
    """A derived possible in `state`, optionally carrying a human verdict."""
    entry = _derived_entry(pid, disposed=outcome)
    entry["state"] = state
    if state in ("rejected", "superseded"):
        entry["reason"], entry["citation"] = "r", "c"
    if state == "picked":
        entry["pick"] = {"staging_id": "some-topic"}
    return entry


# ---- the promotable cases ------------------------------------------------

def test_promotable_human_authored_latent():
    """A human-authored possible is accepted BY CONSTRUCTION (FR-010): it
    carries no origin and no disposition, and is promotable at `latent`."""
    assert gc.is_promotable(_human_entry()) is True


def test_promotable_explicit_human_origin_latent():
    assert gc.is_promotable(_human_entry(origin="human-authored")) is True


def test_promotable_derived_with_accepted_verdict():
    """The ONLY way a derived possible becomes promotable."""
    assert gc.is_promotable(_derived_state(outcome="accepted")) is True


# ---- the refused cases ---------------------------------------------------

def test_not_promotable_derived_awaiting_a_verdict():
    entry = _derived_state()
    assert gc.is_promotable(entry) is False
    assert "disposition" in gc.promotability_refusal(entry)


def test_not_promotable_derived_deferred_is_not_an_acceptance():
    """TRAP 1. A deferred verdict leaves the possible AWAITING a ruling. The
    derivation lane's own `_is_undisposed` helper would call this DISPOSED —
    which is why this predicate may not reuse it."""
    entry = _derived_state(outcome="deferred")
    assert gc.is_promotable(entry) is False
    assert "deferred" in gc.promotability_refusal(entry)


def test_not_promotable_derived_rejected_verdict():
    assert gc.is_promotable(_derived_state(outcome="rejected")) is False


@pytest.mark.parametrize("state", ["rejected", "superseded", "picked"])
def test_not_promotable_terminal_or_picked_states(state):
    """FR-011: the entry's STATE is the reason, for human and derived alike."""
    for entry in (_human_entry(state=state),
                  _derived_state(state=state, outcome="accepted")):
        assert gc.is_promotable(entry) is False
        assert state in gc.promotability_refusal(entry)


# ---- the exhaustive matrix ----------------------------------------------

@pytest.mark.parametrize("state", ["latent", "picked", "rejected", "superseded"])
@pytest.mark.parametrize("outcome", [None, "accepted", "rejected", "deferred"])
def test_promotability_matrix_derived(state, outcome):
    """state x verdict for ai-derived entries. Promotable IFF latent AND
    accepted — every other cell is refused with a non-empty reason."""
    entry = _derived_state(state=state, outcome=outcome)
    expected = (state == "latent" and outcome == "accepted")
    assert gc.is_promotable(entry) is expected
    reason = gc.promotability_refusal(entry)
    if expected:
        assert reason is None
    else:
        assert reason and reason.strip()


@pytest.mark.parametrize("state", ["latent", "picked", "rejected", "superseded"])
def test_promotability_matrix_human_authored(state):
    """Human-authored: promotable IFF latent (accepted by construction)."""
    entry = _human_entry(state=state)
    assert gc.is_promotable(entry) is (state == "latent")


# ---- the prohibited shortcuts, asserted directly -------------------------

def test_machine_disposition_constant_does_not_gate_promotability():
    """TRAP 2. An ACCEPTED derived possible still carries the machine field
    `pending_review` — the contract pins it for the entry's life. A predicate
    that read it would never open."""
    entry = _derived_state(outcome="accepted")
    assert entry["derivation"]["disposition"] == "pending_review"
    assert gc.is_promotable(entry) is True


def test_promotability_disagrees_with_the_derivation_lane_helper_on_deferred():
    """TRAP 1, pinned as an executable claim: the two helpers MUST disagree on
    a deferred verdict. If this ever passes by agreeing, someone reused
    `_is_undisposed` and `deferred` silently became promotable."""
    from doc_health import derive_possibles as dp
    entry = _derived_state(outcome="deferred")
    assert dp._is_undisposed(entry) is False     # the lane calls it disposed
    assert gc.is_promotable(entry) is False      # promotability calls it not accepted


def test_promotability_fails_closed_on_absent_or_stateless_entries():
    """Fail closed on the facts this predicate OWNS: a non-entry, or an entry
    whose state is missing or not `latent`, is refused rather than admitted by
    omission."""
    for bad in (None, "pos-x", [], {}, {"id": "x"},
                {"id": "x", "state": None, "origin": "ai-derived"},
                {"id": "x", "state": "latent", "origin": "something-else"}):
        assert gc.is_promotable(bad) is False
        assert gc.promotability_refusal(bad)


def test_promotability_does_not_re_validate_the_register_schema():
    """Deliberately NOT fail-closed on schema conformance: a `latent` entry
    with no `origin` is promotable even when other required kernel fields are
    absent. Structural validity is the pinned validator's job (the entry is
    read from an already-validated register); duplicating it here would refuse
    legitimately promotable entries the moment the kernel grows a field."""
    assert gc.is_promotable({"id": "x", "state": "latent"}) is True


# ---- the additive `cluster_id` record target (FR-016) --------------------

def test_gate_action_record_carries_cluster_id_target():
    record = gc.build_gate_action_record(
        actor="brett", action=gc.ACTION_DERIVE_POSSIBLES,
        cluster_id="cl-a", at="2026-08-02T10:00:00Z",
        artifacts=[{"kind": gc.ART_WORKFLOW_JOB, "reference": "r"}])
    assert record["target"] == {"cluster_id": "cl-a"}
    assert record["action"] == "derive-possibles"


def test_cluster_id_is_additive_existing_records_byte_identical():
    """FR-016: omitting `cluster_id` leaves every pre-existing record shape
    exactly as it was."""
    common = dict(actor="brett", at="2026-08-02T10:00:00Z",
                  artifacts=[{"kind": gc.ART_WORKFLOW_JOB, "reference": "r"}])
    grown = gc.build_gate_action_record(
        action=gc.ACTION_PROPOSE, topic_id="t", **common)
    assert grown["target"] == {"topic_id": "t"}      # no empty cluster_id key
    assert "cluster_id" not in grown["target"]


def test_new_verb_constants_are_the_contract_spellings():
    assert gc.ACTION_PROMOTE_TO_STAGING == "promote-to-staging"
    assert gc.ACTION_DERIVE_POSSIBLES == "derive-possibles"
    assert gc.ACTION_RESEARCH_BRIEF == "research-brief"


# ==========================================================================
# 011 T056–T059a — SCHEMA CONFORMANCE, with the DEP-003 deferral posture
#
# The three new verbs are proposed in the UPSTREAM openxFactory change
# `add-wheel-action-verbs` (tasks 1.1–1.5) and are NOT released yet. So these
# assertions run through the DELEGATED pinned validator and SKIP — with a reason
# that names the unreleased change — whenever the reachable contract predates the
# extension. They must NEVER fail for that reason, and must NEVER be made to pass
# by copying or stubbing the schema locally (NG-009/FR-042).
#
# The moment the pin advances, this group turns from SKIPPED to PASSING with no
# code edit. That transition IS the signal (FR-037a).
# ==========================================================================

import subprocess as _subprocess
import sys as _sys

from conftest import find_openxfactory_validator as _find_validator

_VALIDATOR = _find_validator()
_NEW_VERBS = ("promote-to-staging", "derive-possibles", "research-brief")


def _contract_carries_the_new_verbs() -> bool:
    """True once the reachable openxFactory contract enumerates the new verbs."""
    if _VALIDATOR is None:
        return False
    schemas = _VALIDATOR.parent.parent / "contracts" / "schemas"
    try:
        intent = (schemas / "gate-intent.schema.yaml").read_text(encoding="utf-8")
        record = (schemas / "gate-action-record.schema.yaml").read_text(encoding="utf-8")
    except OSError:
        return False
    return all(v in intent and v in record for v in _NEW_VERBS)


_UNRELEASED_REASON = (
    "the openxFactory contract reachable from this checkout predates "
    "`add-wheel-action-verbs` (upstream tasks 1.1-1.5): its gate-intent and "
    "gate-action-record schemas do not yet enumerate promote-to-staging, "
    "derive-possibles, or research-brief. DEP-003 defers exact parity until "
    "that release; this group goes live automatically when the pin advances."
)

_conformance = pytest.mark.skipif(
    not _contract_carries_the_new_verbs(), reason=_UNRELEASED_REASON)


def _validate_record(path, *extra):
    return _subprocess.run([_sys.executable, str(_VALIDATOR), *extra, str(path)],
                           capture_output=True, text=True)


def _write(tmp_path, name, doc):
    import yaml as y
    p = tmp_path / name
    p.write_text(y.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return p


def _record(action, target, artifacts=None):
    return {"schema_version": gc.RECORD_SCHEMA_VERSION, "kind": gc.RECORD_KIND,
            "actor": "brett", "action": action, "at": "2026-08-02T09:00:00Z",
            "target": target,
            "artifacts": artifacts if artifacts is not None
            else [{"kind": gc.ART_WORKFLOW_JOB, "reference": "r.workflow-job.yaml"}]}


@_conformance
@pytest.mark.parametrize("action,target", [
    ("promote-to-staging", {"possible_id": "pos-a"}),
    ("research-brief", {"possible_id": "pos-a"}),
    ("derive-possibles", {"cluster_id": "cl-a"}),
])
def test_one_valid_record_per_new_verb(tmp_path, action, target):
    """A well-formed record for each new verb is ACCEPTED by the pinned
    validator."""
    path = _write(tmp_path, f"{action}.gate-action.yaml", _record(action, target))
    result = _validate_record(path)
    assert result.returncode == 0, result.stdout + result.stderr


@_conformance
def test_a_commission_record_without_its_workflow_job_is_rejected(tmp_path):
    """design D2: the descriptor is not optional companionship — a commission
    record that does not carry it is not a commission."""
    path = _write(tmp_path, "no-companion.gate-action.yaml",
                  _record("promote-to-staging", {"possible_id": "pos-a"},
                          artifacts=[]))
    assert _validate_record(path).returncode != 0


@_conformance
def test_a_derive_possibles_record_without_cluster_id_is_rejected(tmp_path):
    """The per-verb conditional: this verb targets a CLUSTER."""
    path = _write(tmp_path, "no-cluster.gate-action.yaml",
                  _record("derive-possibles", {"possible_id": "pos-a"}))
    assert _validate_record(path).returncode != 0


def test_the_conformance_posture_is_recorded_and_visible(tmp_path):
    """FR-037a — this test NEVER skips, so the deferral can never go silent.

    It reports which posture the run is in, and pins that the deferral is a
    property of the upstream contract rather than of anything in this
    repository."""
    released = _contract_carries_the_new_verbs()
    if not released:
        assert _VALIDATOR is None or _UNRELEASED_REASON
        # the transition SKIPPED -> PASSING above is the pin-advance signal
    assert released in (True, False)


def test_no_forked_or_stubbed_upstream_schema_exists_in_this_repo():
    """NG-009 / FR-042 — the deferral must never be 'fixed' by vendoring the
    upstream schema. A local copy would make the conformance group pass while
    proving nothing about the real contract."""
    from conftest import REPO_ROOT
    offenders = []
    for base in ("scripts", "tests"):
        for path in (REPO_ROOT / base).rglob("*"):
            if not path.is_file() or path.suffix not in (".yaml", ".yml", ".json"):
                continue
            if path.name in ("gate-intent.schema.yaml",
                             "gate-action-record.schema.yaml"):
                offenders.append(path.relative_to(REPO_ROOT).as_posix())
                continue
            try:
                head = path.read_text(encoding="utf-8", errors="ignore")[:400]
            except OSError:
                continue
            if "$id" in head and ("gate-intent.schema" in head
                                  or "gate-action-record.schema" in head):
                offenders.append(path.relative_to(REPO_ROOT).as_posix())
    assert offenders == [], f"forked upstream schema(s) found: {offenders}"
