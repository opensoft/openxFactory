"""Per-document doxBench session threads — the sidecar FORMAT, its compaction,
its ONE write route, and the postures it declares
(add-doxbench-editing-phase-b, design §4 / §3.4, tasks §9).

The spelling is the point of this file. `design.md` §4.1 is a SKETCH and says so
("the realization pins the exact spelling"), so the golden render below IS the
format: the frontmatter keys and their order, the six commitment classes, the
turn line that names the model and the bound buffer, and the header sitting
ABOVE the transcript. Every scenario of the delta's thread requirement has a
test here, and the negative space — no automatic promotion, no second decision
store, no write route but the gate's — is asserted against this module's own
source, because an absence nobody checks is an absence that grows a helper.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)
from session_fixtures import GATE_RECORDS_PREFIX  # noqa: E402

from ideation_dashboard import doxbench_threads as dt  # noqa: E402
from ideation_dashboard import doxbench_turns as dtu  # noqa: E402
from ideation_dashboard import gate_routes as gr  # noqa: E402
from ideation_dashboard.boundary import (  # noqa: E402
    OUTSIDE_ALLOWLIST, BoundaryViolation, HumanGate,
)

THREADS_PY = (REPO_ROOT / "scripts" / "ideation_dashboard"
              / "doxbench_threads.py")

DOCUMENT = "ideation/staging/demo-topic/README.md"
SCOPE = dt.ThreadScope(repository="openxFactory", tile_kind="staged",
                       tile_id="demo-topic")

FACT_WITH_EVIDENCE = dt.AcceptedFact(
    "The topic declares three claims.",
    evidence="ideation/staging/demo-topic/README.md")
FACT_WITHOUT_EVIDENCE = dt.AcceptedFact("No delta type is declared yet.")
DECISION = dt.ThreadDecision("Keep the fragment staged",
                             "the claims are not yet mapped")
QUESTION = "Which capability owns the delta?"
EVIDENCE_REF = "openspec/specs/document-lifecycle/spec.md"
PENDING = "Draft the delta-type line."
GOAL = "Decide whether the topic exits to a change or stays staged."

TURN_ONE = dt.ThreadTurn(
    turn_id="t1", model="claude-opus-5", bound_buffer_key=DOCUMENT,
    human="What is missing from this fragment?",
    assistant="It declares claims but no delta type.\nThat blocks the exit path.")
TURN_TWO = dt.ThreadTurn(
    turn_id="t2", model="claude-sonnet-4",
    bound_buffer_key=dtu.OUTLINE_BUFFER_KEY,
    human="Add the delta-type line.", assistant="Proposed one.")


def _state() -> dt.ThreadState:
    return dt.ThreadState(
        active_goal=GOAL,
        accepted_facts=(FACT_WITH_EVIDENCE, FACT_WITHOUT_EVIDENCE),
        open_questions=(QUESTION,),
        decisions=(DECISION,),
        evidence_refs=(EVIDENCE_REF,),
        pending_actions=(PENDING,),
    )


def _thread(**over) -> dt.DocumentThread:
    fields = {"document": DOCUMENT, "scope": SCOPE, "state": _state(),
              "turns": (TURN_ONE, TURN_TWO)}
    fields.update(over)
    return dt.DocumentThread(**fields)


# The GOLDEN render. Byte for byte what a thread sidecar is.
GOLDEN = """\
---
schema_version: 1
kind: doxbench-document-thread
document: ideation/staging/demo-topic/README.md
scope: { repository: openxFactory, tile_kind: staged, tile_id: demo-topic }
authority: non_authoritative
regenerable_from: transcript
---

## Thread state

Active goal: Decide whether the topic exits to a change or stays staged.
Accepted facts:
  - The topic declares three claims. [evidence: ideation/staging/demo-topic/README.md]
  - No delta type is declared yet.
Open questions:
  - Which capability owns the delta?
Decisions in thread:
  - Keep the fragment staged — the claims are not yet mapped
Evidence refs:
  - openspec/specs/document-lifecycle/spec.md
Pending actions:
  - Draft the delta-type line.

## Transcript

### turn t1 · claude-opus-5 · bound: ideation/staging/demo-topic/README.md
human: What is missing from this fragment?
assistant: It declares claims but no delta type.
That blocks the exit path.

### turn t2 · claude-sonnet-4 · bound: outline
human: Add the delta-type line.
assistant: Proposed one.
"""


# ==========================================================================
# THE FILE FORMAT (task 9.1, design §4.1)
# ==========================================================================

def test_the_rendered_sidecar_is_exactly_the_declared_format():
    """The pin the rest of the feature reads: design §4.1's sketch, spelled."""
    assert dt.render_thread(_thread()) == GOLDEN


def test_the_file_declares_its_own_non_authority_and_regenerability():
    """design §4.1: `authority` and `regenerable_from` are WRITTEN INTO the file
    so nothing downstream has to infer that a summary is not truth."""
    rendered = dt.render_thread(_thread())
    assert "authority: non_authoritative\n" in rendered
    assert "regenerable_from: transcript\n" in rendered
    # and the header a packet carries alone carries them too
    header = dt.render_state_header(_thread())
    assert "authority: non_authoritative\n" in header
    assert "regenerable_from: transcript\n" in header


def test_a_thread_claiming_authority_cannot_be_constructed():
    """The refusal lands where the claim is made rather than at write time: a
    summary does not become truth by declaring itself one."""
    with pytest.raises(dt.ThreadFormatRefused) as raised:
        dt.DocumentThread(document=DOCUMENT, scope=SCOPE, authority="governed")
    assert "non_authoritative" in str(raised.value)

    with pytest.raises(dt.ThreadFormatRefused):
        dt.DocumentThread(document=DOCUMENT, scope=SCOPE,
                          regenerable_from="the ratified record")


def test_the_state_header_declares_all_six_commitment_classes():
    header = dt.render_state_header(_thread())
    for label in (dt.ACTIVE_GOAL_LABEL, *dt.LIST_LABEL_ORDER):
        assert f"\n{label}" in f"\n{header}", label
    # the six classes are the header's whole vocabulary
    assert len((dt.ACTIVE_GOAL_LABEL, *dt.LIST_LABEL_ORDER)) == 6
    assert len(dt.COMMITMENT_CLASSES) == 6


def test_an_empty_thread_still_declares_every_class():
    """A thread that has established nothing SAYS so: the labels render either
    way, so a reader can tell "nothing accepted yet" from "class missing"."""
    empty = dt.DocumentThread(document=DOCUMENT, scope=SCOPE)
    rendered = dt.render_thread(empty)
    assert f"\n{dt.ACTIVE_GOAL_LABEL}\n" in rendered
    for label in dt.LIST_LABEL_ORDER:
        assert f"\n{label}\n" in rendered
    assert rendered.endswith(f"{dt.TRANSCRIPT_SECTION}\n")
    assert dt.parse_thread(rendered) == empty


def test_the_header_sits_above_the_transcript_and_carries_no_transcript_text():
    """design §4.1: a reader gets the commitments without reading the
    conversation, and a packet can carry OTHER threads' headers without their
    transcripts."""
    thread = _thread()
    header = dt.render_state_header(thread)
    rendered = dt.render_thread(thread)

    # the header is a literal PREFIX of the whole file — one composition, not two
    assert rendered.startswith(header)
    assert dt.TRANSCRIPT_SECTION not in header
    for needle in (dt.TURN_HEADER_PREFIX, dt.HUMAN_LABEL, dt.ASSISTANT_LABEL,
                   TURN_ONE.human, TURN_ONE.assistant, TURN_TWO.human,
                   TURN_TWO.assistant, TURN_ONE.model):
        assert needle not in header, needle
    # what it DOES carry is every commitment
    for needle in (GOAL, QUESTION, EVIDENCE_REF, PENDING, DECISION.decision,
                   FACT_WITH_EVIDENCE.text):
        assert needle in header, needle


def test_the_turn_line_names_the_model_and_the_bound_buffer():
    """design §4.1: the turn line's model + bound-buffer pair is the SAME pair
    the released envelope carries, so the sidecar and the wire agree by
    construction rather than by two independent conventions."""
    line = TURN_ONE.render().split("\n")[0]
    assert line == (f"### turn t1 · claude-opus-5 · bound: {DOCUMENT}")
    assert line.startswith(dt.TURN_HEADER_PREFIX)
    assert line.count(dt.TURN_FIELD_SEPARATOR) == 2
    assert f"{dt.TURN_BOUND_PREFIX}{DOCUMENT}" in line


def test_the_bound_buffer_key_is_the_turn_contracts_own_buffer_key():
    """The agreement, asserted against `doxbench_turns` rather than described: a
    document buffer's key IS its path, and the reserved outline key is the
    outline's. A thread that spelled either differently would name a buffer the
    envelope does not have."""
    document_buffer = dtu.TurnBuffer(
        kind="document", repository="openxFactory", path=DOCUMENT,
        base_ref="refs/heads/main", base_revision="0" * 40, base_hash="a" * 64,
        content_hash="b" * 64, content="# demo\n", dirty=True)
    assert TURN_ONE.bound_buffer_key == dtu.buffer_key_for(document_buffer)
    assert TURN_TWO.bound_buffer_key == dtu.OUTLINE_BUFFER_KEY


# ==========================================================================
# ROUND TRIP AND REFUSALS
# ==========================================================================

def test_render_parse_render_is_byte_identical():
    thread = _thread()
    rendered = dt.render_thread(thread)
    parsed = dt.parse_thread(rendered)
    assert parsed == thread
    assert dt.render_thread(parsed) == rendered


def test_a_multi_line_body_survives_the_round_trip_unchanged():
    parsed = dt.parse_thread(dt.render_thread(_thread()))
    assert parsed.turns[0].assistant == TURN_ONE.assistant
    assert "\n" in parsed.turns[0].assistant


def test_a_fact_keeps_its_evidence_ref_through_the_round_trip():
    """Evidence is a FIELD of the fact, not a neighbouring list entry, so a fact
    cannot come back without what backs it."""
    parsed = dt.parse_thread(dt.render_thread(_thread()))
    assert parsed.state.accepted_facts[0] == FACT_WITH_EVIDENCE
    assert parsed.state.accepted_facts[1].evidence is None


def test_a_wrong_kind_is_refused():
    text = dt.render_thread(_thread()).replace(
        f"kind: {dt.THREAD_KIND}", "kind: gate-action-record")
    with pytest.raises(dt.ThreadKindRefused) as raised:
        dt.parse_thread(text)
    assert dt.THREAD_KIND in str(raised.value)


def test_an_unsupported_schema_version_is_refused():
    text = dt.render_thread(_thread()).replace("schema_version: 1",
                                               "schema_version: 2")
    with pytest.raises(dt.ThreadVersionRefused) as raised:
        dt.parse_thread(text)
    assert "refuses rather than reading a format it does not know" in str(raised.value)


def test_a_missing_state_section_is_refused():
    text = dt.render_thread(_thread()).replace(f"{dt.STATE_SECTION}\n\n", "")
    with pytest.raises(dt.ThreadFormatRefused) as raised:
        dt.parse_thread(text)
    assert dt.STATE_SECTION in str(raised.value)


def test_a_state_header_alone_is_not_a_thread():
    """`render_state_header`'s output is the packet unit, and it deliberately
    does NOT parse as a thread: a header with no transcript has nothing to be
    regenerable FROM."""
    with pytest.raises(dt.ThreadFormatRefused) as raised:
        dt.parse_thread(dt.render_state_header(_thread()))
    assert dt.TRANSCRIPT_SECTION in str(raised.value)


def test_a_missing_commitment_class_is_refused():
    text = dt.render_thread(_thread()).replace(
        f"{dt.OPEN_QUESTIONS_LABEL}\n{dt.ITEM_PREFIX}{QUESTION}\n", "")
    with pytest.raises(dt.ThreadFormatRefused) as raised:
        dt.parse_thread(text)
    assert dt.OPEN_QUESTIONS_LABEL in str(raised.value)


def test_a_misordered_state_header_is_refused():
    """Order is part of the format, so a reader knows what is MISSING rather
    than guessing."""
    text = dt.render_thread(_thread()).replace(
        f"{dt.OPEN_QUESTIONS_LABEL}\n{dt.ITEM_PREFIX}{QUESTION}\n"
        f"{dt.DECISIONS_LABEL}\n{dt.ITEM_PREFIX}{DECISION.render()}\n",
        f"{dt.DECISIONS_LABEL}\n{dt.ITEM_PREFIX}{DECISION.render()}\n"
        f"{dt.OPEN_QUESTIONS_LABEL}\n{dt.ITEM_PREFIX}{QUESTION}\n")
    with pytest.raises(dt.ThreadFormatRefused):
        dt.parse_thread(text)


def test_an_unknown_or_duplicated_frontmatter_key_is_refused():
    base = dt.render_thread(_thread())
    with pytest.raises(dt.ThreadFormatRefused) as unknown:
        dt.parse_thread(base.replace("authority:", "provenance: gateway\nauthority:"))
    assert "unknown=" in str(unknown.value)

    with pytest.raises(dt.ThreadFormatRefused) as duplicate:
        dt.parse_thread(base.replace(f"document: {DOCUMENT}\n",
                                     f"document: {DOCUMENT}\ndocument: other.md\n"))
    assert "twice" in str(duplicate.value)


def test_a_decision_with_no_basis_is_refused():
    text = dt.render_thread(_thread()).replace(DECISION.render(),
                                               DECISION.decision)
    with pytest.raises(dt.ThreadFormatRefused) as raised:
        dt.parse_thread(text)
    assert "states no basis" in str(raised.value)
    with pytest.raises(dt.ThreadFormatRefused):
        dt.ThreadDecision("a decision", "")


def test_a_thread_file_is_lf_only_and_ends_with_a_newline():
    rendered = dt.render_thread(_thread())
    with pytest.raises(dt.ThreadFormatRefused):
        dt.parse_thread(rendered.replace("\n", "\r\n"))
    with pytest.raises(dt.ThreadFormatRefused):
        dt.parse_thread(rendered.rstrip("\n"))


def test_a_body_line_that_opens_with_a_sentinel_is_refused_not_escaped():
    """A body that could parse back as a different thread is refused at
    construction; escaping it would make the sidecar unreadable to the human it
    is written for."""
    for sentinel in dt.BODY_FORBIDDEN_LINE_PREFIXES:
        with pytest.raises(dt.ThreadFormatRefused):
            dt.ThreadTurn(turn_id="t9", model="m", bound_buffer_key="outline",
                          human="fine", assistant=f"ok\n{sentinel} smuggled")


def test_a_blank_or_whitespace_padded_value_is_refused_not_coerced():
    with pytest.raises(dt.ThreadFormatRefused):
        dt.ThreadState(open_questions=("  padded ",))
    with pytest.raises(dt.ThreadFormatRefused):
        dt.ThreadState(pending_actions=("",))
    with pytest.raises(dt.ThreadFormatRefused):
        dt.ThreadTurn(turn_id="t9", model="m", bound_buffer_key="outline",
                      human="", assistant="ok")


def test_a_repeated_turn_id_is_refused():
    """A turn id identifies a turn, so a repeat means one of them was lost."""
    with pytest.raises(dt.ThreadFormatRefused) as raised:
        _thread(turns=(TURN_ONE, TURN_ONE))
    assert "twice" in str(raised.value)


# ==========================================================================
# THE SIDECAR PATH RULE (task 9.1)
# ==========================================================================

def test_the_sidecar_path_is_always_inside_the_declared_prefix():
    for document in (DOCUMENT, "docs/a.md", "openspec/specs/x/spec.md"):
        path = dt.thread_path_for(document)
        assert path.startswith(dt.THREAD_PREFIX)
        assert path.endswith(dt.THREAD_SUFFIX)


def test_the_prefix_says_session_working_memory_and_is_not_corpus():
    """Threads are working memory, so they live in the dashboard's own artifact
    tree beside the gate records — never under the corpus folders a lifecycle
    `Status:` header would be expected in."""
    assert dt.THREAD_PREFIX == "ideation/dashboard/session-threads/"
    for corpus in ("ideation/staging/", "ideation/brainstorm/", "docs/",
                   "openspec/"):
        assert not dt.THREAD_PREFIX.startswith(corpus)


def test_two_documents_with_the_same_basename_get_different_thread_paths():
    """The failure a basename-keyed rule would cause is two conversations merged
    into one, which is the worst thing this format could do."""
    first = dt.thread_path_for("ideation/staging/alpha/README.md")
    second = dt.thread_path_for("ideation/staging/beta/README.md")
    assert first != second
    assert dt.thread_document_for(first) == "ideation/staging/alpha/README.md"
    assert dt.thread_document_for(second) == "ideation/staging/beta/README.md"


def test_appending_to_one_documents_thread_leaves_the_others_unchanged(tmp_path):
    """The delta scenario "The selected document changes", at the layer this
    module owns: each loaded document has its OWN sidecar, so appending a turn to
    one cannot touch another's. Which thread the chat SHOWS is the selector's
    job; that two threads exist and stay separate is this file's."""
    worktree = tmp_path / "wt"
    worktree.mkdir()
    gate = HumanGate(worktree, [dt.THREAD_PREFIX], human_actor="brett",
                     session_root=worktree)
    first = dt.DocumentThread(document="ideation/staging/demo-topic/alpha.md",
                              scope=SCOPE, turns=(TURN_ONE,))
    second = dt.DocumentThread(document="ideation/staging/demo-topic/beta.md",
                               scope=SCOPE, turns=(TURN_ONE,))
    dt.write_thread(gate, first)
    dt.write_thread(gate, second)
    before = (worktree / dt.thread_path_for(second.document)).read_text(
        encoding="utf-8")

    dt.write_thread(gate, dt.mirror_turn(first, TURN_TWO))

    assert len(dt.parse_thread(
        (worktree / dt.thread_path_for(first.document)).read_text(
            encoding="utf-8")).turns) == 2
    assert (worktree / dt.thread_path_for(second.document)).read_text(
        encoding="utf-8") == before


def test_the_path_rule_is_deterministic_and_reversible():
    for document in (DOCUMENT, "docs/a.md", "a/b/c/d.md"):
        path = dt.thread_path_for(document)
        assert path == dt.thread_path_for(document)
        assert dt.thread_document_for(path) == document


@pytest.mark.parametrize("document", [
    "/etc/passwd",
    "../outside/notes.md",
    "ideation/staging/../../escape.md",
    "ideation\\staging\\demo\\README.md",
    "",
    "   ",
    "ideation/staging//demo.md",
])
def test_a_traversal_shaped_or_absolute_document_path_is_refused(document):
    with pytest.raises(dt.ThreadPathRefused):
        dt.thread_path_for(document)


def test_a_thread_of_a_thread_is_refused():
    with pytest.raises(dt.ThreadPathRefused):
        dt.thread_path_for(dt.thread_path_for(DOCUMENT))


def test_a_path_outside_the_prefix_is_not_a_thread_path():
    with pytest.raises(dt.ThreadPathRefused):
        dt.thread_document_for(f"ideation/staging/demo{dt.THREAD_SUFFIX}")
    with pytest.raises(dt.ThreadPathRefused):
        dt.thread_document_for(f"{dt.THREAD_PREFIX}notes.md")


def test_thread_paths_in_selects_only_sidecars_in_the_order_given():
    paths = [DOCUMENT, dt.thread_path_for(DOCUMENT), GATE_RECORDS_PREFIX + "r.yaml",
             dt.thread_path_for("docs/a.md")]
    assert dt.thread_paths_in(paths) == (dt.thread_path_for(DOCUMENT),
                                         dt.thread_path_for("docs/a.md"))


# ==========================================================================
# COMPACTION — LAYER TWO (task 9.3, delta scenario "A thread is compacted")
# ==========================================================================

def _state_fields(state: dt.ThreadState) -> dict:
    """The state's six classes as a dict, so a test can replace exactly one and
    assert the refusal names THAT class."""
    return {field: getattr(state, field)
            for field in ("active_goal", "accepted_facts", "open_questions",
                          "decisions", "evidence_refs", "pending_actions")}


def test_compaction_is_lossy_over_the_transcript_by_design():
    thread = _thread()
    compacted = dt.compact_thread(thread, keep_turns=1)
    assert compacted.turns == (TURN_TWO,)
    assert dt.compact_thread(thread, keep_turns=0).turns == ()
    # and the header is untouched by the mechanical part
    assert compacted.state == thread.state


def test_the_compacted_result_stays_non_authoritative_and_regenerable():
    compacted = dt.compact_thread(_thread(), keep_turns=0)
    assert compacted.authority == dt.NON_AUTHORITATIVE
    assert compacted.regenerable_from == dt.REGENERABLE_FROM_TRANSCRIPT
    rendered = dt.render_thread(compacted)
    assert "authority: non_authoritative\n" in rendered
    assert "regenerable_from: transcript\n" in rendered


def test_a_compaction_that_drops_an_accepted_fact_is_refused():
    thread = _thread()
    lost = dt.ThreadState(**{**_state_fields(thread.state),
                             "accepted_facts": (FACT_WITHOUT_EVIDENCE,)})
    with pytest.raises(dt.ThreadCompactionRefused) as raised:
        dt.compact_thread(thread, keep_turns=1, state=lost)
    assert "accepted fact" in str(raised.value)
    assert FACT_WITH_EVIDENCE.text in str(raised.value)


def test_a_compaction_that_drops_a_facts_evidence_ref_is_refused():
    """Keeping the sentence and losing what backs it is losing an evidence
    ref."""
    thread = _thread()
    stripped = dt.AcceptedFact(FACT_WITH_EVIDENCE.text)
    lost = dt.ThreadState(**{**_state_fields(thread.state),
                             "accepted_facts": (stripped, FACT_WITHOUT_EVIDENCE)})
    with pytest.raises(dt.ThreadCompactionRefused):
        dt.compact_thread(thread, keep_turns=1, state=lost)


def test_a_compaction_that_drops_an_open_question_is_refused():
    thread = _thread()
    lost = dt.ThreadState(**{**_state_fields(thread.state),
                             "open_questions": ()})
    with pytest.raises(dt.ThreadCompactionRefused) as raised:
        dt.compact_thread(thread, keep_turns=1, state=lost)
    assert "open question" in str(raised.value) and QUESTION in str(raised.value)


def test_a_compaction_that_drops_a_decision_is_refused():
    thread = _thread()
    lost = dt.ThreadState(**{**_state_fields(thread.state), "decisions": ()})
    with pytest.raises(dt.ThreadCompactionRefused) as raised:
        dt.compact_thread(thread, keep_turns=1, state=lost)
    assert "decision" in str(raised.value)


def test_a_compaction_that_drops_an_evidence_ref_is_refused():
    thread = _thread()
    lost = dt.ThreadState(**{**_state_fields(thread.state),
                             "evidence_refs": ()})
    with pytest.raises(dt.ThreadCompactionRefused) as raised:
        dt.compact_thread(thread, keep_turns=1, state=lost)
    assert "evidence ref" in str(raised.value) and EVIDENCE_REF in str(raised.value)


def test_a_compaction_that_drops_a_pending_action_is_refused():
    thread = _thread()
    lost = dt.ThreadState(**{**_state_fields(thread.state),
                             "pending_actions": ()})
    with pytest.raises(dt.ThreadCompactionRefused) as raised:
        dt.compact_thread(thread, keep_turns=1, state=lost)
    assert "pending action" in str(raised.value) and PENDING in str(raised.value)


def test_a_compaction_that_drops_or_rewords_the_active_goal_is_refused():
    """The goal is the header's sixth commitment class. The delta enumerates the
    five list classes; losing the goal is the same class of defect, and
    REWORDING it is a human's decision through a lifecycle verb rather than
    something a compaction may do."""
    thread = _thread()
    for goal in ("", "Something else entirely."):
        lost = dt.ThreadState(**{**_state_fields(thread.state),
                                 "active_goal": goal})
        with pytest.raises(dt.ThreadCompactionRefused) as raised:
            dt.compact_thread(thread, keep_turns=1, state=lost)
        assert "active goal" in str(raised.value)


def test_a_compaction_that_only_drops_narrative_is_permitted():
    """"Dropping prose that merely restates them is the point" — a compacted
    header that ADDS nothing and loses nothing passes."""
    thread = _thread()
    same = dt.ThreadState(**_state_fields(thread.state))
    compacted = dt.compact_thread(thread, keep_turns=1, state=same)
    assert compacted.state == thread.state
    assert compacted.turns == (TURN_TWO,)


def test_a_compaction_bound_must_be_a_non_negative_integer():
    thread = _thread()
    for bad in (-1, True, "1", 1.0):
        with pytest.raises(dt.ThreadFormatRefused):
            dt.compact_thread(thread, keep_turns=bad)


# ==========================================================================
# THE PERSISTENCE SEAM (task 9.2) — one commit, one write route
# ==========================================================================

def test_the_commit_paths_are_the_documents_own_sidecar():
    """These are the paths a Save adds to the DECLARED set
    `branch_session.commit_gate_action` commits as exactly ONE commit, so a
    thread and the document text it discusses cannot land through separate
    commits."""
    assert dt.thread_commit_paths(DOCUMENT) == (dt.thread_path_for(DOCUMENT),)
    assert isinstance(dt.thread_commit_paths(DOCUMENT), tuple)


def test_a_thread_is_written_through_the_gate_inside_the_session_worktree(tmp_path):
    worktree = tmp_path / "wt"
    worktree.mkdir()
    gate = HumanGate(worktree, [GATE_RECORDS_PREFIX, dt.THREAD_PREFIX],
                     human_actor="brett", session_root=worktree)

    written = dt.write_thread(gate, _thread())

    assert written == (worktree / dt.thread_path_for(DOCUMENT)).resolve()
    assert written.read_text(encoding="utf-8") == GOLDEN
    # the SERVED checkout (this test's tmp root, outside the worktree) is untouched
    assert not (tmp_path / dt.THREAD_PREFIX).exists()


def test_a_gate_with_no_declared_session_worktree_refuses_the_write(tmp_path):
    """Threads live only on a session branch, so a gate that declares no session
    worktree has nowhere to put one — and the served checkout is not an
    alternative."""
    gate = HumanGate(tmp_path, [dt.THREAD_PREFIX], human_actor="brett")
    with pytest.raises(dt.ThreadCapabilityAbsent) as raised:
        dt.write_thread(gate, _thread())
    assert "session worktree" in str(raised.value)


def test_a_gate_whose_allowlist_omits_the_prefix_refuses_the_write(tmp_path):
    """Why task 9.5 exists: the sidecar is written through the gate's
    allowlist-governed artifact write, so a gate that does not DECLARE the thread
    prefix refuses it as `outside-allowlist` rather than writing it anyway."""
    worktree = tmp_path / "wt"
    worktree.mkdir()
    gate = HumanGate(worktree, [GATE_RECORDS_PREFIX], human_actor="brett",
                     session_root=worktree)
    with pytest.raises(BoundaryViolation) as raised:
        dt.write_thread(gate, _thread())
    assert raised.value.refusal.kind == OUTSIDE_ALLOWLIST


def test_the_doxbench_save_gate_declares_the_thread_prefix(tmp_path):
    """Task 9.5, pinned against the REAL gate the doxBench Save is written
    through (`gate_routes.first_edit_gate_factory`), not a stand-in."""
    worktree = tmp_path / "wt"
    worktree.mkdir()
    gate = gr.first_edit_gate_factory("brett", GATE_RECORDS_PREFIX)(worktree)

    assert dt.THREAD_PREFIX in gate.output.allowlist
    # and the records tree is still declared — the allowance was ADDED, not swapped
    assert GATE_RECORDS_PREFIX in gate.output.allowlist
    assert len(gate.output.allowlist) == 2

    written = dt.write_thread(gate, _thread())
    assert written.is_file()
    assert Path(gate.session_root).resolve() == worktree.resolve()


def test_no_other_gate_on_this_surface_gained_the_thread_prefix(tmp_path):
    """"Do not widen any other gate": the `edit-document` gate — the other
    worktree-rooted session gate — still declares the records tree alone."""
    source = (REPO_ROOT / "scripts" / "ideation_dashboard"
              / "gate_routes.py").read_text(encoding="utf-8")
    assert source.count("doxbench_threads.THREAD_PREFIX") == 1


# ==========================================================================
# PROMOTION EXCLUSION (task 9.4, design §4.2)
# ==========================================================================

def test_threads_are_excluded_from_promotion_by_default():
    assert dt.promotion_excluded_prefixes() == (dt.THREAD_PREFIX,)
    reason = dt.PROMOTION_EXCLUSION_REASON
    assert "does NOT promote them by default" in reason
    assert "explicit human opt-in" in reason
    assert "existing lifecycle verb" in reason


_FORBIDDEN_MODULE_NEEDLES = [
    # the ONE write route: the injected gate's artifact write, and nothing else
    ("open(", "a direct file open"),
    ("write_text", "a direct text write"),
    ("write_bytes", "a direct byte write"),
    ("mkdir", "a directory creation"),
    ("shutil", "a filesystem utility"),
    ("subprocess", "a subprocess invocation"),
    ("import os", "an os import"),
    ("Path(", "a runtime filesystem path construction"),
    # nothing leaves the machine, ever, from here (design §4.3 D13)
    ("urllib", "a network client"),
    ("socket", "a network socket"),
    ("push", "a remote-write verb"),
    ("open_or_update", "the pull-request port's write verb"),
    ("session_pr", "the pull-request adapter"),
    # no parallel decision store — a finding leaves a thread only through an
    # existing lifecycle verb, so there is nowhere else for one to be kept
    ("sqlite3", "a second decision store"),
    ("pickle", "an opaque store"),
    ("shelve", "an opaque store"),
    ("json.dump", "a second serialization of the same commitments"),
    # and no automatic promotion path, nor a commit of its own
    ("def promote_", "a promotion path"),
    ("commit_gate_action(", "a commit this module must not perform itself"),
]


@pytest.mark.parametrize("needle,label", _FORBIDDEN_MODULE_NEEDLES,
                         ids=[needle for needle, _ in _FORBIDDEN_MODULE_NEEDLES])
def test_the_thread_module_contains_no_forbidden_spelling(needle, label):
    source = THREADS_PY.read_text(encoding="utf-8")
    assert needle not in source, (
        f"doxbench_threads.py must not contain {label}: {needle!r}")


def test_the_module_exposes_no_promotion_or_publish_callable():
    """The negative asserted against the module's public surface, not only its
    text: a finding leaves a thread through an existing lifecycle verb."""
    public = {name for name in vars(dt) if not name.startswith("_")}
    for name in public:
        assert not name.startswith("promote"), name
        assert "publish" not in name, name
    assert "promotion_excluded_prefixes" in public


# ==========================================================================
# THE MIRRORING INTERFACE THE GATED §11 SLICE CONSUMES
# ==========================================================================

class RecordingMirror:
    """A stand-in for the §11 harness bridge — the ONLY thing this slice knows
    about a harness."""

    def __init__(self, *, fail: str | None = None) -> None:
        self.calls: list[tuple] = []
        self._fail = fail

    def mirror_turn(self, thread, turn) -> None:
        self.calls.append((thread, turn))
        if self._fail:
            raise RuntimeError(self._fail)


def test_the_mirror_declares_exactly_one_operation():
    assert dt.MIRROR_OPERATIONS == ("mirror_turn",)
    declared = {name for name in vars(dt.ThreadMirror)
                if not name.startswith("_")}
    assert declared == set(dt.MIRROR_OPERATIONS)
    assert isinstance(RecordingMirror(), dt.ThreadMirror)


def test_the_sidecar_append_is_fully_functional_with_no_mirror():
    """The default posture: a thread never depends on a harness existing
    (design §3.4's editor-only case)."""
    thread = _thread(turns=())
    appended = dt.mirror_turn(thread, TURN_ONE)
    assert appended.turns == (TURN_ONE,)
    assert dt.mirror_turn(appended, TURN_TWO).turns == (TURN_ONE, TURN_TWO)
    # the input is untouched — the shapes are frozen
    assert thread.turns == ()


def test_an_injected_mirror_is_handed_the_same_turn_the_sidecar_holds():
    mirror = RecordingMirror()
    appended = dt.mirror_turn(_thread(turns=()), TURN_ONE, mirror=mirror)
    assert len(mirror.calls) == 1
    seen_thread, seen_turn = mirror.calls[0]
    assert seen_turn is TURN_ONE
    # it is told what the RECORD says: the thread it sees already holds the turn
    assert seen_thread.turns == (TURN_ONE,) == appended.turns


def test_a_failing_mirror_does_not_cost_the_thread_its_turn():
    """The sidecar is the record, so a harness failure is reported WITH the
    appended thread rather than instead of it."""
    mirror = RecordingMirror(fail="the bridge died")
    with pytest.raises(dt.ThreadMirrorFailed) as raised:
        dt.mirror_turn(_thread(turns=()), TURN_ONE, mirror=mirror)
    assert raised.value.thread.turns == (TURN_ONE,)
    assert isinstance(raised.value.cause, RuntimeError)
    assert "the sidecar remains the record" in str(raised.value)


def test_an_object_that_is_not_a_mirror_is_refused():
    with pytest.raises(dt.ThreadFormatRefused) as raised:
        dt.mirror_turn(_thread(turns=()), TURN_ONE, mirror=object())
    assert "mirror_turn" in str(raised.value)


def test_the_split_brain_prohibition_and_the_gated_slice_are_stated_in_source():
    """The two statements the §11 slice is written against, kept in the module
    rather than only in the change: what that slice wires in, and that the
    harness's native memory MUST NOT hold the thread."""
    source = THREADS_PY.read_text(encoding="utf-8")
    assert "TODO(add-doxbench-editing-phase-b tasks.md §11)" in source
    assert "sidecar files are" in source and "THE RECORD" in source
    assert "MUST NOT hold the thread" in source
    assert "ranked LAST" in source


# ==========================================================================
# DEGRADED POSTURES (design §3.4) — threads exist only where sessions exist
# ==========================================================================

def test_threads_are_available_on_a_local_plane_with_the_gate_capability():
    assert dt.require_thread_capability(plane=dt.LOCAL_PLANE,
                                        gate_capability=True) is None
    assert dt.thread_capability_absence(plane=dt.LOCAL_PLANE,
                                        gate_capability=True) is None


def test_no_thread_exists_on_the_hosted_plane():
    with pytest.raises(dt.ThreadCapabilityAbsent) as raised:
        dt.require_thread_capability(plane=dt.HOSTED_PLANE, gate_capability=True)
    assert dt.THREAD_CAPABILITY_ABSENT_REASON in str(raised.value)
    assert raised.value.cause == dt.HOSTED_PLANE_CAUSE
    assert dt.thread_capability_absence(
        plane=dt.HOSTED_PLANE, gate_capability=True) == str(raised.value)


def test_no_thread_exists_without_the_gate_capability():
    with pytest.raises(dt.ThreadCapabilityAbsent) as raised:
        dt.require_thread_capability(plane=dt.LOCAL_PLANE, gate_capability=False)
    assert dt.THREAD_CAPABILITY_ABSENT_REASON in str(raised.value)
    assert raised.value.cause == dt.NO_GATE_CAPABILITY_CAUSE
    assert "copyable descriptor" in str(raised.value)


def test_an_undeclared_plane_or_capability_is_refused_not_guessed():
    with pytest.raises(dt.ThreadFormatRefused):
        dt.require_thread_capability(plane="qa", gate_capability=True)
    with pytest.raises(dt.ThreadFormatRefused):
        dt.require_thread_capability(plane=dt.LOCAL_PLANE, gate_capability="yes")
