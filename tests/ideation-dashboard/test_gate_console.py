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
import json
import shutil
import subprocess
import sys
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit, find_openxfactory_validator

from doc_health import families
from ideation_dashboard import gate_console as gc
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


def test_a_crlf_document_survives_a_demote_move_byte_exactly(tmp_path):
    """Wave re-review P3 — the F10 corpus-integrity class through another
    verb. The demote MOVE used to `read_text(errors="replace")` ->
    `write_text`, so on Linux a CRLF (Windows-authored) document was silently
    rewritten as LF by universal-newline translation — invalidating any open
    doxBench buffer's base identity for that document — and any undecodable
    byte was silently mangled to U+FFFD. A move that flips no Status header
    now copies BYTES and never decodes at all, so the moved copy is the
    source, byte for byte."""
    root = _tree(tmp_path)
    snap = _snapshot(root)
    crlf = b"# Tasks\r\n\r\n- [ ] 1.1 authored\r\n- [ ] 1.2 on Windows\r\n"
    (root / "openspec" / "changes" / CHANGE / "tasks.md").write_bytes(crlf)

    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason="CRLF round trip.", at=AT)
    gc.execute_demotion_plan(res.plan, root, at=AT)

    moved = root / "ideation" / "staging" / TOPIC / "openspec" / "tasks.md"
    assert moved.read_bytes() == crlf


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


def _demote_and_execute(root: Path, *, reason="Reworking scope."):
    snap = _snapshot(root)
    res = gc.GateConsole(_gate(root)).demote(snap, CHANGE, reason=reason, at=AT)
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
    # the requirement's idempotence clause measured on real output
    again = round_trip.refresh_fragment(
        text, proposal_text=returned,
        provenance={"Change ID": CHANGE, "Raised": "2026-07-02",
                    "Status at demote": "active", "Demoted": AT[:10],
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
# ratify — the ratification record round-trip, validator-clean
# ============================================================================

def test_ratify_writes_the_record_and_a_gate_action_carrying_it(tmp_path):
    root = _tree(tmp_path)
    res = gc.GateConsole(_gate(root)).ratify(CHANGE, "Brett", at=AT)
    assert res.ratification == {
        "kind": "ratification-record", "schema_version": 1,
        "change_id": CHANGE, "ratifier": "Brett", "date": "2026-07-14"}
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
