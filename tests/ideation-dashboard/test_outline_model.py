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
