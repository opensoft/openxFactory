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
    result = run_insert(PARTLY_MIGRATED, title="pre-document idea notes",
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
    result = run_insert(PARTLY_MIGRATED, title="pre-document idea notes",
                        addedBy="brett", date="2026-08-18")
    assert result["heading"] == "Idea notes (pre-document, non-documented)"
    assert "## Idea notes (pre-document, non-documented)" in result["text"]


def test_an_added_section_carries_its_provenance():
    """Either a human or an AI may add one, so the document must stay
    attributable. The required trio carry the stamp the way the skeleton shows
    it — on the note the human is about to write."""
    required = run_insert(PARTLY_MIGRATED, title="pre-document idea notes",
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
                        title="open questions",
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
                        title="pre-document idea notes",
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
