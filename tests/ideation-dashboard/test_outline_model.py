"""The staged-topic outline model (add-staged-topic-outline-template task 3.1).

Pure module, so it runs under node with no DOM stub at all — the model touches
nothing but strings. Skipped when node is absent, matching the bullseye rig.

What these pin is the pair of properties the tab's honesty rests on: section
identity comes from the fragment's OWN headings and `xspec:` fences and is never
fabricated, and a fragment that merely QUOTES the canonical fenced skeleton has
not adopted it.
"""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
MODEL_JS = REPO_ROOT / "scripts/ideation_dashboard/web/views/outline-model.js"
NODE = shutil.which("node")

pytestmark = pytest.mark.skipif(NODE is None, reason="node is not installed")


def run_model(text: str) -> dict:
    """Evaluate `outlineModel(text)` under node and return its JSON."""
    with TemporaryDirectory() as tmp:
        script = Path(tmp) / "run.mjs"
        payload = Path(tmp) / "input.md"
        payload.write_text(text, encoding="utf-8")
        script.write_text(
            "import { readFileSync } from 'node:fs';\n"
            f"import {{ outlineModel }} from {json.dumps(str(MODEL_JS))};\n"
            f"const text = readFileSync({json.dumps(str(payload))}, 'utf8');\n"
            "console.log(JSON.stringify(outlineModel(text)));\n",
            encoding="utf-8")
        out = subprocess.run([NODE, str(script)], capture_output=True, text=True)
        assert out.returncode == 0, out.stderr
        return json.loads(out.stdout)


def run_insert(text: str, **options) -> dict:
    """Evaluate `insertSection(text, options)` under node and return its JSON."""
    with TemporaryDirectory() as tmp:
        script = Path(tmp) / "run.mjs"
        payload = Path(tmp) / "input.md"
        payload.write_text(text, encoding="utf-8")
        script.write_text(
            "import { readFileSync } from 'node:fs';\n"
            f"import {{ insertSection }} from {json.dumps(str(MODEL_JS))};\n"
            f"const text = readFileSync({json.dumps(str(payload))}, 'utf8');\n"
            f"const options = {json.dumps(options)};\n"
            "console.log(JSON.stringify(insertSection(text, options)));\n",
            encoding="utf-8")
        out = subprocess.run([NODE, str(script)], capture_output=True, text=True)
        assert out.returncode == 0, out.stderr
        return json.loads(out.stdout)


def headings(text: str) -> list[str]:
    """Every `## ` heading, in file order — read WITHOUT the model, on purpose:
    an ordering assertion that consulted the thing under test could not fail.
    Fence-blind, so it is only ever used on fence-free fixtures; the fenced case
    is asserted through the model, which is where fence-awareness lives."""
    return [line[3:].strip() for line in text.splitlines()
            if line.startswith("## ")]


CONFORMING = """# Staged: a topic

Status: staged

## Idea notes (pre-document, non-documented)

Half-formed.

## Conflicts

None known.

## Open questions

### Q1. Does it hold?

Context: unclear.
Recommended answer: yes.
Explanation: because of X.
Disposition status: open
"""


def test_a_conforming_fragment_reports_no_gaps():
    model = run_model(CONFORMING)
    assert model["conforming"] is True
    assert model["state"] == "conforming"
    assert model["gaps"] == []
    roles = {s["title"]: s["role"] for s in model["sections"]}
    assert all(r == "required" for r in roles.values()), roles


def test_sections_come_from_real_headings_and_are_never_fabricated():
    model = run_model(CONFORMING)
    titles = [s["title"] for s in model["sections"]]
    assert titles == [
        "Idea notes (pre-document, non-documented)", "Conflicts", "Open questions"]
    # nothing invented: every reported section is a line in the source
    for section in model["sections"]:
        assert CONFORMING.splitlines()[section["line"] - 1].startswith("## ")


def test_quoting_the_skeleton_is_not_adopting_it():
    """The canonical template ships as a copy-pasteable ```markdown fence whose
    body carries every required heading. A fragment that pastes the fence as an
    EXAMPLE has adopted nothing, and a fence-blind scanner would call it fully
    conforming."""
    quoting = (
        "# Staged: x\n\nStatus: staged\n\nCopy this:\n\n"
        "```markdown\n## Idea notes (pre-document, non-documented)\n\n"
        "## Conflicts\n\n## Open questions\n```\n")
    model = run_model(quoting)
    assert model["sections"] == []
    assert model["conforming"] is False
    assert {g["label"] for g in model["gaps"]} == {
        "pre-document idea notes", "conflicts", "open questions"}


def test_a_pre_template_fragment_degrades_rather_than_breaking():
    """Opt-in migration means most topics carry none of this. The tab must
    render them as what they are, not report them as broken."""
    model = run_model("# Staged: old\n\nStatus: staged\n\n## Claims\n\nA claim.\n")
    assert model["state"] == "pre-template"
    assert [s["title"] for s in model["sections"]] == ["Claims"]
    assert [s["role"] for s in model["sections"]] == ["added"]


def test_a_partly_migrated_fragment_is_partial_not_pre_template():
    model = run_model("# Staged: x\n\nStatus: staged\n\n## Conflicts\n\nOne.\n")
    assert model["state"] == "partial"
    assert {g["label"] for g in model["gaps"]} == {
        "pre-document idea notes", "open questions"}


def test_a_question_missing_sub_fields_is_reported_by_name():
    model = run_model(CONFORMING.replace("Explanation: because of X.\n", ""))
    gaps = [g for g in model["gaps"] if g["kind"] == "incomplete-question"]
    assert len(gaps) == 1
    assert gaps[0]["missing"] == ["Explanation"]
    assert "Q1" in gaps[0]["label"]


# ---- task 4.1's named case, on the SURFACE side of the same contract ----------
#
# The checker half is pinned in tests/doc-health/test_families.py. Both are here
# because the model and the family MUST mean the same thing by conformance — the
# modules say so in their own comments ("change both together or neither") — and a
# rule proven on only one side can drift on the other while both keep passing.


def test_a_bare_question_is_non_conforming_and_reports_all_four_fields():
    """"A question is never recorded bare." A heading with nothing under it must
    report every field it owes, in the contract's order, so the tab tells the
    human what to write rather than only that something is wrong."""
    bare = CONFORMING.split("### Q1.")[0] + "### Q1. Does it hold?\n"
    model = run_model(bare)
    gaps = [g for g in model["gaps"] if g["kind"] == "incomplete-question"]
    assert len(gaps) == 1
    assert gaps[0]["missing"] == [
        "Context", "Recommended answer", "Explanation", "Disposition status"]
    assert model["conforming"] is False
    # the three required SECTIONS are all present, so the question is the only gap
    assert [g["kind"] for g in model["gaps"]] == ["incomplete-question"]


def test_a_question_with_a_disposition_but_no_recommendation_is_non_conforming():
    """The contract's own emphasis, and the case task 4.1 names: the disposition
    may stay `open`, but a recommendation and its reasoning are still owed. This
    is what makes an undecided question something a reader can disagree with
    instead of a prompt to re-derive."""
    model = run_model(CONFORMING.replace(
        "Recommended answer: yes.\nExplanation: because of X.\n", ""))
    gaps = [g for g in model["gaps"] if g["kind"] == "incomplete-question"]
    assert len(gaps) == 1
    assert gaps[0]["missing"] == ["Recommended answer", "Explanation"]


def test_a_sub_heading_outside_open_questions_is_not_an_open_question():
    """The four sub-fields are owed by open questions, not by every `### ` a
    fragment carries. A model that scored all of them would report a gap on a
    conforming fragment, and the tab would show a fault where there is none."""
    model = run_model(CONFORMING.replace(
        "## Conflicts\n\nNone known.\n",
        "## Conflicts\n\n### With the promoted spec\n\nStated, not resolved.\n"))
    assert [g for g in model["gaps"] if g["kind"] == "incomplete-question"] == []
    assert model["conforming"] is True


def test_added_sections_carry_their_provenance():
    model = run_model(CONFORMING + "\n## Prior art\n\nAdded-by: claude-opus-5 · 2026-08-15\n\nNotes.\n")
    extra = [s for s in model["sections"] if s["title"] == "Prior art"][0]
    assert extra["role"] == "added"
    assert extra["addedBy"] == "claude-opus-5 · 2026-08-15"


def test_an_xspec_marked_section_is_a_proposal_element():
    model = run_model(
        CONFORMING + "\n## Why\n\n<!-- xspec:candidate id=why -->\n\nBecause.\n")
    why = [s for s in model["sections"] if s["title"] == "Why"][0]
    assert why["role"] == "proposal-element"
    assert why["marked"] is True


# ---- the add-section half (task 3.2, asserted here as pure rules) -------------
#
# The affordance in staging-workbench.js computes the whole next text through
# `insertSection` and hands it to the canvas. Everything that decides WHAT lands
# and WHERE is therefore testable without a DOM, a buffer, or a server, which is
# why it lives here; the wiring half (buffer, provenance actor, `edit-document`)
# is driven through the real composition in test_outline_tab.py.

PARTLY_MIGRATED = """# Staged: a topic

Status: staged

## Claims

- A settled fact.

## Conflicts

None known.

## Exit

Every open question carries a disposition.
"""


def test_a_missing_required_section_lands_in_its_canonical_place():
    """The skeleton's order is Claims -> … -> Idea notes -> Conflicts -> Exit, so
    an added Idea notes section belongs BETWEEN Claims and Conflicts. Appending it
    would be easier and wrong: the fragment would read out of template order for
    no reason a human could see."""
    result = run_insert(PARTLY_MIGRATED, title="pre-document idea notes", required=True,
                        addedBy="claude-opus-5", date="2026-08-18")
    assert result["ok"] is True
    assert headings(result["text"]) == [
        "Claims", "Idea notes (pre-document, non-documented)", "Conflicts", "Exit"]
    # …and the patch STATES the section it was scoped by, which is the addressing
    # key the contract calls for
    assert result["target"] == "Claims"
    assert result["mode"] == "after"


def test_a_required_section_lands_under_its_canonical_heading():
    """The caller asks by the gap's LABEL ("pre-document idea notes"); what is
    written is the skeleton's own heading. A surface reporting the request instead
    of the result would name a heading the file does not contain."""
    result = run_insert(PARTLY_MIGRATED, title="pre-document idea notes", required=True,
                        addedBy="brett", date="2026-08-18")
    assert result["heading"] == "Idea notes (pre-document, non-documented)"
    assert "## Idea notes (pre-document, non-documented)" in result["text"]


def test_an_added_section_carries_its_provenance():
    """Either a human or an AI may add one, so the document must stay
    attributable. The required trio carry the stamp the way the skeleton shows
    it — on the note the human is about to write."""
    required = run_insert(PARTLY_MIGRATED, title="pre-document idea notes", required=True,
                          addedBy="claude-opus-5", date="2026-08-18")
    assert "- <idea note text> — Added-by: claude-opus-5 · 2026-08-18" \
        in required["text"]
    # …and a section BEYOND the required set carries the section-level line the
    # contract makes attributable, which the model then reports back
    extra = run_insert(PARTLY_MIGRATED, title="Prior art",
                       addedBy="claude-opus-5", date="2026-08-18")
    section = [s for s in run_model(extra["text"])["sections"]
               if s["title"] == "Prior art"][0]
    assert section["role"] == "added"
    assert section["addedBy"] == "claude-opus-5 · 2026-08-18"


def test_a_seeded_open_questions_section_is_conforming_on_arrival():
    """A bare question is non-conforming by the contract's own rule, so seeding
    one would be adding a defect. The seed carries all four sub-fields."""
    result = run_insert(PARTLY_MIGRATED + "\n## Idea notes (pre-document)\n\n- x\n",
                        title="open questions", required=True,
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is True
    model = run_model(result["text"])
    assert [g for g in model["gaps"] if g["kind"] == "incomplete-question"] == []
    assert model["conforming"] is True


def test_a_section_the_outline_already_carries_is_refused_not_duplicated():
    """The add buttons are offered from what the STORED fragment lacks while the
    insert is computed against what the BUFFER holds, and those differ by exactly
    the human's unsaved work — so "already there" is a real state and must be a
    stated refusal rather than a second copy."""
    result = run_insert(PARTLY_MIGRATED, title="conflicts",
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is False
    assert "already carries" in result["reason"]
    assert "Conflicts" in result["reason"]
    assert "text" not in result


def test_the_gap_route_refuses_a_required_section_present_under_another_spelling():
    """The gap button asks by the contract's LABEL, and the section it would add
    may already be present under the skeleton's longer heading. On THAT route the
    rank match is doing necessary work — it is what stops a second idea-notes
    section from landing beside `## Idea notes (pre-document, non-documented)`."""
    already = PARTLY_MIGRATED.replace(
        "## Claims", "## Idea notes (pre-document, non-documented)\n\n- one.\n\n## Claims")
    result = run_insert(already, title="pre-document idea notes", required=True,
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is False
    assert result["reason"] == (
        'this outline already carries the section '
        '"Idea notes (pre-document, non-documented)"')


# ---- review finding F2: the free-form route is EXACT, not rank-wide ------------
#
# The contract grants that "either a human or an AI may add a section beyond the
# required set", and the free-form control is the only route to it. A rank-wide
# duplicate rule made every one of the headings below unaddable on a FULLY
# TEMPLATED fragment — refused, and refused while naming a section the human never
# asked for. Verified against the pre-fix module: all seven refused, and an
# explicit `after=` target did not get round it because the refusal fired before
# the anchor was read.
#
# The fixture has to be the WHOLE skeleton for that to be true, which is the point:
# the more conformant a topic becomes, the more headings the old rule locked out.

FULLY_TEMPLATED = """# Staged: a fully templated topic

Status: staged

## Last proposal attempt (round-trip provenance)

Change ID: none yet

## Claims

- A settled fact.

## Why

<!-- xspec:candidate target=ideation-dashboard -->
Because of a reason.
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=ideation-dashboard -->
This shape.
<!-- /xspec:candidate -->

## Impact

<!-- xspec:candidate target=ideation-dashboard -->
- Affected specs: `ideation-dashboard`
<!-- /xspec:candidate -->

## Idea notes (pre-document, non-documented)

- A half-formed thought. — Added-by: brett · 2026-08-16

## Conflicts

- Contradicts nothing yet. — Added-by: brett · 2026-08-16

## Open questions

### Q1. Does it hold?

Context: unclear.
Recommended answer: yes.
Explanation: because of X.
Disposition status: open

## Exit

Every open question carries a disposition other than open.
"""

TEMPLATED_HEADINGS = [
    "Last proposal attempt (round-trip provenance)", "Claims", "Why",
    "What changes", "Impact", "Idea notes (pre-document, non-documented)",
    "Conflicts", "Open questions", "Exit",
]

# Each of these was refused pre-fix, against the section named beside it.
F2_HEADINGS = [
    ("Exit criteria", "Exit"),
    ("Why we deferred", "Why"),
    ("Impact analysis", "Impact"),
    ("Claims log", "Claims"),
    ("Prior art on why", "Why"),
    ("Conflicts with promoted specs", "Conflicts"),
    ("Open questions for Brett", "Open questions"),
]


def test_the_fixture_really_is_fully_templated():
    """The finding only exists on a conformant fragment, so this is load-bearing:
    if the fixture drifts out of conformance the seven cases below stop testing
    anything."""
    model = run_model(FULLY_TEMPLATED)
    assert model["conforming"] is True
    assert [s["title"] for s in model["sections"]] == TEMPLATED_HEADINGS


@pytest.mark.parametrize("title,resembled", F2_HEADINGS)
def test_a_free_form_heading_that_merely_resembles_a_template_one_still_lands(
        title, resembled):
    result = run_insert(FULLY_TEMPLATED, title=title,
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is True, result.get("reason")
    # VERBATIM — the human's heading, not the section it resembles
    assert result["heading"] == title
    assert "## " + title in result["text"]
    # nothing already written moved, and the resembled section is still single
    assert headings(result["text"])[:len(TEMPLATED_HEADINGS)] == TEMPLATED_HEADINGS
    assert headings(result["text"]).count(resembled) == 1


@pytest.mark.parametrize("title,resembled", F2_HEADINGS)
def test_an_explicit_target_also_works_for_those_headings(title, resembled):
    """The pre-fix refusal fired before the anchor was even read, so naming a
    target could not get round it."""
    result = run_insert(FULLY_TEMPLATED, title=title, after="Conflicts",
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is True, result.get("reason")
    assert result["target"] == "Conflicts"
    at = headings(result["text"]).index(title)
    assert headings(result["text"])[at - 1] == "Conflicts"
    assert headings(result["text"]).count(resembled) == 1


# The canonicalization symptom needs a fragment LACKING the resembled section:
# with no clash to refuse on, the loose match reached the skeleton instead and
# rewrote the human's heading. Pre-fix this produced `## Conflicts` seeded with
# `- <conflict text>`, and the typed heading was simply gone.
SPARSE = """# Staged: x

Status: staged

## Claims

- one.

## Exit

Done.
"""


def test_a_free_form_heading_is_never_canonicalized_into_a_required_one():
    result = run_insert(SPARSE, title="Notes on conflicts",
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is True
    assert result["heading"] == "Notes on conflicts"
    # the GENERIC skeleton, never the required section's seed
    assert result["section"] == (
        "## Notes on conflicts\n\nAdded-by: brett · 2026-08-18\n\n- <fill this in>")
    assert "<conflict text>" not in result["text"]
    assert "## Conflicts" not in result["text"]
    assert headings(result["text"]) == ["Claims", "Exit", "Notes on conflicts"]


def test_the_free_form_route_still_refuses_an_exact_duplicate():
    """Exact-title equality is the free-form duplicate rule — narrower than rank,
    and still a real guard."""
    result = run_insert(FULLY_TEMPLATED, title="conflicts",
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is False
    assert result["reason"] == 'this outline already carries the section "Conflicts"'


def test_typing_a_canonical_heading_exactly_still_gets_its_seed():
    """The exact rule cuts both ways: a human who types the required heading
    letter for letter means that section, and gets the skeleton's own seed."""
    result = run_insert(PARTLY_MIGRATED, title="Open questions",
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is True
    assert result["heading"] == "Open questions"
    assert "Disposition status: open" in result["section"]
    # …in its canonical place, which is behind Conflicts and ahead of Exit
    assert headings(result["text"]) == [
        "Claims", "Conflicts", "Open questions", "Exit"]


def test_the_required_route_refuses_a_label_it_does_not_recognise():
    result = run_insert(PARTLY_MIGRATED, title="Prior art", required=True,
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is False
    assert "not one of the three required sections" in result["reason"]


# ---- review finding F4: the unclosed fence -------------------------------------


UNCLOSED_FENCE = """# Staged: x

Status: staged

## Claims

- A settled fact.

Here is the shape I want, and I forgot to close it:

```markdown
## Conflicts

- <conflict text>
"""


def test_an_unclosed_fence_is_refused_rather_than_appended_into():
    """The duplicate guard fails exactly when it is needed. Inside an unclosed
    fence the append lands INSIDE the fence, the model then sees no sections at
    all, so "already carries" can never fire and repeated presses pile up copies
    — each one reporting success."""
    result = run_insert(UNCLOSED_FENCE, title="conflicts",
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is False
    assert "unclosed code fence" in result["reason"]
    assert "text" not in result


def test_the_blindness_the_fence_refusal_protects_is_real():
    """Why the refusal and not a repair: the guard's own input is gone. Everything
    after the open fence — including `## Claims`, which really is a section — is
    invisible to the model, so nothing downstream could have noticed a duplicate.
    Repairing the fence would rewrite a fragment nobody asked us to change, which
    task 3.3 forbids outright."""
    model = run_model(UNCLOSED_FENCE)
    assert [s["title"] for s in model["sections"]] == ["Claims"]
    # `## Conflicts` sits inside the unclosed fence and is correctly not reported
    assert "Conflicts" not in [s["title"] for s in model["sections"]]
    assert "## Conflicts" in UNCLOSED_FENCE


def test_a_second_press_cannot_duplicate_because_the_first_never_landed():
    """The pile-up, closed at its source: two presses on the same unclosed-fence
    fragment both refuse, so there is no first copy for a second to duplicate."""
    first = run_insert(UNCLOSED_FENCE, title="conflicts",
                       addedBy="brett", date="2026-08-18")
    second = run_insert(UNCLOSED_FENCE, title="conflicts",
                        addedBy="brett", date="2026-08-18")
    assert first["ok"] is False and second["ok"] is False
    assert first["reason"] == second["reason"]


def test_closing_the_fence_restores_the_add_and_the_duplicate_guard():
    """The refusal is about the fence and nothing else — the remedy it names
    actually works, and the guard comes back with it."""
    closed = UNCLOSED_FENCE + "```\n"
    added = run_insert(closed, title="conflicts",
                       addedBy="brett", date="2026-08-18")
    assert added["ok"] is True
    again = run_insert(added["text"], title="conflicts",
                       addedBy="brett", date="2026-08-18")
    assert again["ok"] is False
    assert "already carries" in again["reason"]


def test_a_quoted_skeleton_does_not_block_a_real_add():
    """The fence-blindness defect, on the WRITE side. A fragment that pastes the
    canonical skeleton as an example carries `## Conflicts` inside a fence and has
    adopted nothing — a fence-blind duplicate check would refuse to add the real
    section, leaving the topic permanently unable to migrate."""
    quoting = ("# Staged: x\n\nStatus: staged\n\nCopy this:\n\n"
               "```markdown\n## Conflicts\n\n- <conflict text>\n```\n")
    result = run_insert(quoting, title="conflicts",
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is True
    # the real section is now identified, and the fenced example still is not
    model = run_model(result["text"])
    assert [s["title"] for s in model["sections"]] == ["Conflicts"]
    assert "```markdown\n## Conflicts" in result["text"]


def test_the_insert_is_scoped_by_an_explicitly_named_target():
    """A heading with no canonical place is anchored by the human, and that
    anchor IS the patch's addressing key."""
    result = run_insert(PARTLY_MIGRATED, title="Prior art", after="Claims",
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is True
    assert result["target"] == "Claims"
    assert headings(result["text"]) == ["Claims", "Prior art", "Conflicts", "Exit"]


def test_an_unnamed_target_appends_and_reorders_nothing():
    result = run_insert(PARTLY_MIGRATED, title="Prior art",
                        addedBy="brett", date="2026-08-18")
    assert result["mode"] == "end"
    assert result["target"] is None
    assert headings(result["text"]) == ["Claims", "Conflicts", "Exit", "Prior art"]
    # every original line survives, in its original order
    assert result["text"].startswith(PARTLY_MIGRATED.rstrip("\n"))


def test_a_target_the_outline_does_not_carry_is_refused():
    result = run_insert(PARTLY_MIGRATED, title="Prior art", after="Nowhere",
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is False
    assert "no \"Nowhere\" section" in result["reason"]
    assert "text" not in result


def test_a_section_needs_a_heading():
    result = run_insert(PARTLY_MIGRATED, title="   ",
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is False
    assert "text" not in result


def test_the_insert_is_eol_blind_and_answers_in_one_flavor():
    """A CRLF fragment must not come back with doubled CRs or mixed endings: the
    model answers in LF and the canvas re-applies the document's own flavor at the
    swap. Applying LF verbatim to a CRLF document is how one reviewed insertion
    becomes a whole-file line-ending rewrite."""
    result = run_insert(PARTLY_MIGRATED.replace("\n", "\r\n"),
                        title="pre-document idea notes", required=True,
                        addedBy="brett", date="2026-08-18")
    assert result["ok"] is True
    assert "\r" not in result["text"]
    assert headings(result["text"]) == [
        "Claims", "Idea notes (pre-document, non-documented)", "Conflicts", "Exit"]


def test_exactly_one_blank_line_separates_the_inserted_block():
    """Whatever the surrounding whitespace was: a heading pressed against the
    previous paragraph is not the markdown the fragment's other sections are
    written in."""
    cramped = "# Staged: x\n\nStatus: staged\n## Claims\n- one\n"
    result = run_insert(cramped, title="Prior art",
                        addedBy="brett", date="2026-08-18")
    lines = result["text"].splitlines()
    at = lines.index("## Prior art")
    assert lines[at - 1] == ""
    assert lines[at - 2] == "- one"
    assert result["text"].endswith("\n")
    assert "\n\n\n" not in result["text"]


def test_the_model_and_the_doc_health_family_agree_on_the_contract():
    """The surface and the checker must mean the same thing by conformance."""
    import sys
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from doc_health import families

    js = MODEL_JS.read_text(encoding="utf-8")
    for _needle, label in families._TEMPLATE_SECTIONS:
        assert f'label: "{label}"' in js, f"model omits required section {label}"
    for field in families._QUESTION_SUBFIELDS:
        assert f'"{field}"' in js, f"model omits sub-field {field}"
