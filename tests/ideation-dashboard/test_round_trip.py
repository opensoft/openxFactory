"""The pure fragment refresh (`align-demote-to-round-trip-rule`, tasks 1.x/4.1-4.2).

No tree, no plan, no I/O — `round_trip.py` is text in, text out, which is why the
risky half of this change can be pinned exhaustively here and the driven
end-to-end proof in test_gate_console.py can stay about the WIRING.

Three properties carry the change and each is asserted from both sides:

* FENCE-AWARENESS — the canonical template ships as a ```markdown skeleton
  containing the provenance heading and every slot, so a fragment that merely
  QUOTES it must not have its example rewritten.
* BYTE PRESERVATION — everything outside the slots and the marked bodies survives
  exactly, each line keeping its own ending; only created lines take the
  document's flavor.
* IDEMPOTENCE — both operations are addressed, not appending.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory

import pytest

from conftest import REPO_ROOT

from doc_health import families
from ideation_dashboard import round_trip as rt

OUTLINE_MODEL_JS = (
    REPO_ROOT / "scripts/ideation_dashboard/web/views/outline-model.js")
NODE = shutil.which("node")


PROVENANCE = {
    "Change ID": "add-worked-example",
    "Raised": "2026-07-02",
    "Status at demote": "active",
    "Demoted": "2026-08-19",
    "Demote reason": "Reworking scope.",
}

CONFORMING = """# Staged: a topic

Status: staged
Summary: a line the refresh must never touch.

## Last proposal attempt (round-trip provenance)

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Why

<!-- xspec:candidate target=ideation-dashboard -->
The aspirational pre-proposal guess.
<!-- /xspec:candidate -->

## Conflicts

- Nothing yet.
"""

PROPOSAL = """---
code_surface: none
---

# Proposal: add-worked-example

## Why

The REAL reason, learned while the change was in flight.
It runs to two lines on purpose.

## What Changes

A section the fragment does not mark.
"""


# ---- the row model: the identity everything else rests on ---------------------


@pytest.mark.parametrize("text", [
    "",
    "one line, no ending",
    "lf\nlf\n",
    "crlf\r\ncrlf\r\n",
    "cr\rcr\r",
    "mixed\r\nlf\ncr\rtail",
    "\n\n\n",
    "trailing\nno newline",
])
def test_split_and_join_are_exactly_inverse(text):
    """`join_rows(split_keepends(t)) == t` for every ending shape. Every other
    guarantee in this module is stated in terms of "these bytes survive", and that
    sentence is only meaningful if the split/join pair is lossless."""
    assert rt.join_rows(rt.split_keepends(text)) == text


def test_the_split_does_not_break_on_exotic_line_boundaries():
    """`str.splitlines(keepends=True)` also breaks on \\x0c, \\x85, U+2028 and
    friends. A governance document containing one would be re-split and rejoined
    into different bytes, so this module uses its own three-ending split."""
    text = "a\x0cb\x85c d\n"
    assert len(text.splitlines(keepends=True)) > 1      # the stdlib would split
    assert [body for body, _ in rt.split_keepends(text)] == ["a\x0cb\x85c d"]
    assert rt.join_rows(rt.split_keepends(text)) == text


@pytest.mark.parametrize("text,expected", [
    ("crlf\r\nthen lf\n", "\r\n"),
    ("lf\nthen crlf\r\n", "\n"),
    ("cr\rrest", "\r"),
    ("no ending at all", "\n"),
])
def test_new_lines_take_the_documents_first_ending(text, expected):
    """The FIRST-break rule, not a majority vote — the same rule
    `doxbench-editor.js`'s `eolFlavorOf` applies to these same documents, so a
    fragment edited in the outline tab and one refreshed by a demote agree about
    its flavor."""
    assert rt.document_eol(rt.split_keepends(text)) == expected


# ---- the provenance slots ----------------------------------------------------


def test_existing_slots_are_rewritten_and_nothing_else_moves():
    out = rt.fill_provenance_slots(CONFORMING, PROVENANCE)
    for name, value in PROVENANCE.items():
        assert f"{name}: {value}" in out
    assert "none yet" not in out and "n/a" not in out
    # every line outside the slot block survives byte for byte
    assert "Summary: a line the refresh must never touch." in out
    assert "The aspirational pre-proposal guess." in out
    assert "- Nothing yet." in out
    # …and the slot block keeps the skeleton's order
    order = [line.split(":")[0] for line in out.splitlines()
             if re.match(r"^(Change ID|Raised|Status at demote|Demoted|Demote reason):", line)]
    assert order == list(rt.SLOT_ORDER)


def test_a_rewritten_slot_keeps_its_own_line_ending():
    """The `_flip_status` precedent generalized: flipping a CRLF line must not be
    the one line that comes out LF, because a single stray ending is invisible in
    review and shows up as a whole-file diff later."""
    crlf = CONFORMING.replace("\n", "\r\n")
    out = rt.fill_provenance_slots(crlf, PROVENANCE)
    assert "\r\n" in out
    lone = [line for line in re.split(r"\r\n", out) if "\n" in line or "\r" in line]
    assert lone == [], f"lines with a foreign ending survived: {lone!r}"
    assert f"Change ID: {PROVENANCE['Change ID']}\r\n" in out


def test_a_missing_slot_is_added_to_a_partial_block():
    partial = CONFORMING.replace("Status at demote: n/a\n", "")
    out = rt.fill_provenance_slots(partial, PROVENANCE)
    assert "Status at demote: active" in out
    assert out.count("Status at demote:") == 1


def test_a_fragment_with_no_provenance_section_gains_one_in_canonical_position():
    """Most of the corpus, since template conformance is opt-in. The section lands
    ahead of the first `## ` section, which is where the skeleton puts it."""
    pre_template = "# Staged: old\n\nStatus: staged\n\n## Claims\n\n- A claim.\n"
    out = rt.fill_provenance_slots(pre_template, PROVENANCE)
    headings = [line for line in out.splitlines() if line.startswith("## ")]
    assert headings == [rt.PROVENANCE_HEADING, "## Claims"]
    assert "Change ID: add-worked-example" in out
    assert "- A claim." in out
    assert out.endswith("\n")
    assert "\n\n\n" not in out


def test_a_fragment_that_quotes_the_skeleton_keeps_its_example_intact():
    """THE FENCE LANDMINE. The slots inside a ```markdown example belong to
    somebody's copy-paste block; rewriting them would edit an illustration. The
    real section is added instead."""
    quoting = (
        "# Staged: x\n\nStatus: staged\n\nCopy this:\n\n"
        "```markdown\n## Last proposal attempt (round-trip provenance)\n\n"
        "Change ID: none yet\nRaised: n/a\n```\n\n## Claims\n\n- A claim.\n")
    out = rt.fill_provenance_slots(quoting, PROVENANCE)
    # the fenced example is untouched, verbatim
    assert "```markdown\n## Last proposal attempt (round-trip provenance)\n\n" \
        "Change ID: none yet\nRaised: n/a\n```" in out
    # …and a REAL section was inserted outside it
    assert "Change ID: add-worked-example" in out
    assert out.count("Change ID:") == 2


def test_an_unresolved_value_is_recorded_as_unavailable_never_blank():
    """The requirement forbids both fabricating a value and leaving the slot
    reading as an unused placeholder."""
    out = rt.fill_provenance_slots(CONFORMING, {**PROVENANCE, "Raised": ""})
    assert f"Raised: {rt.UNAVAILABLE}" in out
    out_missing = rt.fill_provenance_slots(CONFORMING, {})
    for name in rt.SLOT_ORDER:
        assert f"{name}: {rt.UNAVAILABLE}" in out_missing


def test_filling_the_slots_twice_changes_nothing_the_second_time():
    once = rt.fill_provenance_slots(CONFORMING, PROVENANCE)
    assert rt.fill_provenance_slots(once, PROVENANCE) == once
    pre_template = "# Staged: old\n\nStatus: staged\n\n## Claims\n\n- A claim.\n"
    inserted = rt.fill_provenance_slots(pre_template, PROVENANCE)
    assert rt.fill_provenance_slots(inserted, PROVENANCE) == inserted


# ---- the marked proposal-element sections ------------------------------------


def test_a_marked_section_carries_the_returned_proposals_real_text():
    out = rt.refresh_marked_sections(CONFORMING, PROPOSAL)
    assert "The REAL reason, learned while the change was in flight." in out
    assert "It runs to two lines on purpose." in out
    assert "The aspirational pre-proposal guess." not in out


def test_the_marker_comments_are_never_rewritten():
    """They are the addressing key. Rewriting an addressing key mid-operation is
    how two sides stop agreeing about what they are addressing."""
    out = rt.refresh_marked_sections(CONFORMING, PROPOSAL)
    assert out.count("<!-- xspec:candidate target=ideation-dashboard -->") == 1
    assert out.count("<!-- /xspec:candidate -->") == 1


def test_a_section_only_the_proposal_carries_is_not_invented():
    out = rt.refresh_marked_sections(CONFORMING, PROPOSAL)
    assert "## What Changes" not in out
    assert "A section the fragment does not mark." not in out


def test_a_marked_section_the_proposal_omits_is_left_exactly_alone():
    fragment = CONFORMING.replace(
        "## Conflicts\n\n- Nothing yet.\n",
        "## Impact\n\n<!-- xspec:candidate target=x -->\nOnly the fragment has this.\n"
        "<!-- /xspec:candidate -->\n")
    out = rt.refresh_marked_sections(fragment, PROPOSAL)
    assert "Only the fragment has this." in out
    assert "## Impact" in out


def test_an_unmarked_fragment_section_is_not_refreshed():
    """The fragment's MARKED set is the human's declaration of which proposal
    elements this topic carries. A demote is not the moment to widen it."""
    unmarked = CONFORMING.replace(
        "<!-- xspec:candidate target=ideation-dashboard -->\n", "").replace(
        "<!-- /xspec:candidate -->\n", "")
    out = rt.refresh_marked_sections(unmarked, PROPOSAL)
    assert "The aspirational pre-proposal guess." in out
    assert "The REAL reason" not in out


def test_an_unterminated_marker_leaves_the_section_untouched():
    """Guessing where an unclosed block ends would be a rewrite over an unknown
    span. Refusing is the only safe answer, and it is the same
    refuse-rather-than-repair posture the outline tab takes on an unclosed fence."""
    broken = CONFORMING.replace("<!-- /xspec:candidate -->\n", "")
    out = rt.refresh_marked_sections(broken, PROPOSAL)
    assert "The aspirational pre-proposal guess." in out
    assert "The REAL reason" not in out


def test_a_fenced_xspec_example_is_not_refreshed():
    quoting = (
        "# Staged: x\n\nStatus: staged\n\nCopy this:\n\n"
        "```markdown\n## Why\n\n<!-- xspec:candidate target=x -->\n"
        "an example body\n<!-- /xspec:candidate -->\n```\n")
    out = rt.refresh_marked_sections(quoting, PROPOSAL)
    assert "an example body" in out
    assert "The REAL reason" not in out


def test_the_refresh_writes_the_destinations_endings_not_the_proposals():
    """A CRLF fragment refreshed from an LF proposal must not sprout LF lines in
    the middle of it — the mixed-ending outcome the byte-preserving rule exists to
    prevent."""
    crlf = CONFORMING.replace("\n", "\r\n")
    out = rt.refresh_marked_sections(crlf, PROPOSAL)
    assert "The REAL reason, learned while the change was in flight.\r\n" in out
    stray = [line for line in re.split(r"\r\n", out) if "\n" in line or "\r" in line]
    assert stray == [], f"foreign endings survived: {stray!r}"


def test_no_proposal_text_leaves_the_sections_exactly_as_they_were():
    assert rt.refresh_marked_sections(CONFORMING, "") == CONFORMING
    assert rt.refresh_marked_sections(CONFORMING, "# no sections here\n") == CONFORMING


def test_refreshing_the_sections_twice_changes_nothing_the_second_time():
    once = rt.refresh_marked_sections(CONFORMING, PROPOSAL)
    assert rt.refresh_marked_sections(once, PROPOSAL) == once


# ---- the combined refresh ----------------------------------------------------


def test_the_whole_refresh_is_idempotent():
    once = rt.refresh_fragment(
        CONFORMING, proposal_text=PROPOSAL, provenance=PROVENANCE)
    twice = rt.refresh_fragment(
        once, proposal_text=PROPOSAL, provenance=PROVENANCE)
    assert twice == once


def test_the_whole_refresh_fills_slots_even_with_no_proposal():
    """The no-`proposal.md` edge the requirement names: slots filled, sections
    untouched."""
    out = rt.refresh_fragment(
        CONFORMING, proposal_text=None, provenance=PROVENANCE)
    assert "Change ID: add-worked-example" in out
    assert "The aspirational pre-proposal guess." in out
    assert "The REAL reason" not in out


def test_the_whole_refresh_touches_only_the_slots_and_the_marked_body():
    """The boundedness claim, measured line by line rather than asserted: every
    changed line is either a provenance slot or inside the marked block."""
    out = rt.refresh_fragment(
        CONFORMING, proposal_text=PROPOSAL, provenance=PROVENANCE)
    before = CONFORMING.splitlines()
    after = out.splitlines()
    changed_before = [line for line in before if line not in after]
    slot_names = tuple(f"{name}:" for name in rt.SLOT_ORDER)
    for line in changed_before:
        assert line.startswith(slot_names) or line == "The aspirational pre-proposal guess.", \
            f"an unrelated line changed: {line!r}"


# ---- the THIRD implementation of one fence rule -------------------------------
#
# design Decision 2 named this hazard when it chose a new module: `round_trip.py`,
# `doc_health.families` and `web/views/outline-model.js` now each carry the same
# naive ``` toggle, in the same corpus, over the same documents. Sharing the code
# is not available — one of the three is JavaScript in the browser bundle — so the
# mitigation is this test.
#
# It compares what each module DOES with fences rather than a private helper's
# signature: for a fixture whose lines are headings and fences, the set of headings
# each one treats as REAL is its answer to "where are the fences", and all three
# answers must be identical. That also exercises the real consumer path in each
# module instead of a shape nobody calls.

FENCE_FIXTURES = {
    "plain": "## one\n```\n## fenced\n```\n## two\n",
    "language_tag": "## one\n```markdown\n## fenced\n```\n## two\n",
    "indented_fence": "## one\n   ```\n## fenced\n   ```\n## two\n",
    # `~~~` is a real CommonMark fence and NONE of the three treats it as one.
    # Recorded deliberately: the shared rule is ``` only, so this heading is REAL
    # in all three, and a future "improvement" to any one of them breaks here.
    "tilde_is_not_a_fence": "## one\n~~~\n## still real\n~~~\n## two\n",
    "unclosed": "## one\n```\n## fenced\n## also fenced\n",
    "four_backticks": "## one\n````\n## fenced\n````\n## two\n",
    "fence_with_trailing_space": "## one\n``` \n## fenced\n``` \n## two\n",
    "nested_looking": "## one\n````\n```\n## fenced\n```\n````\n## two\n",
    "empty": "",
    "no_fences": "## one\n\ntext\n\n## two\n",
}

_JS_PROBE = """
import { readFileSync } from 'node:fs';
import { outlineSections } from %(model)s;
const cases = JSON.parse(readFileSync(%(cases)s, 'utf8'));
const out = {};
for (const [name, text] of Object.entries(cases)) {
  out[name] = outlineSections(text).map((s) => [s.line, s.title]);
}
console.log(JSON.stringify(out));
"""


def _js_real_headings() -> dict:
    with TemporaryDirectory() as tmp:
        cases = Path(tmp) / "cases.json"
        cases.write_text(json.dumps(FENCE_FIXTURES), encoding="utf-8")
        script = Path(tmp) / "probe.mjs"
        script.write_text(_JS_PROBE % {
            "model": json.dumps(str(OUTLINE_MODEL_JS)),
            "cases": json.dumps(str(cases)),
        }, encoding="utf-8")
        done = subprocess.run([NODE, str(script)], capture_output=True, text=True)
        assert done.returncode == 0, done.stderr
        return json.loads(done.stdout)


def _round_trip_real_headings(text: str) -> list[list]:
    rows = rt.split_keepends(text)
    return [[index + 1, title] for index, title, _end in rt._section_bounds(rows)]


def _families_real_headings(text: str) -> list[list]:
    return [[lineno, line[3:].strip()]
            for lineno, line, fenced in families._scan_lines(text)
            if not fenced and line.startswith("## ")]


@pytest.mark.parametrize("name", sorted(FENCE_FIXTURES))
def test_round_trip_and_doc_health_agree_about_every_fence(name):
    text = FENCE_FIXTURES[name]
    assert _round_trip_real_headings(text) == _families_real_headings(text), name


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_all_three_fence_implementations_agree():
    """The whole mitigation in one assertion. If this fails, one of the three moved
    and the other two did not — and the fix is to move all three or none, never to
    relax the test."""
    js = _js_real_headings()
    for name, text in sorted(FENCE_FIXTURES.items()):
        mine = _round_trip_real_headings(text)
        theirs = [[line, title] for line, title in js[name]]
        assert mine == theirs, (
            f"{name}: round_trip.py says {mine}, outline-model.js says {theirs}")
        assert mine == _families_real_headings(text), name


def test_the_shared_predicate_is_spelled_the_same_in_all_three():
    """The algorithm, not just its outcome on these fixtures: all three lstrip (or
    trimStart) and then test the literal three backticks. A fixture set can only
    ever sample the input space; this pins the rule itself."""
    mine = (REPO_ROOT / "scripts/ideation_dashboard/round_trip.py").read_text(
        encoding="utf-8")
    fam = (REPO_ROOT / "scripts/doc_health/families.py").read_text(encoding="utf-8")
    js = OUTLINE_MODEL_JS.read_text(encoding="utf-8")
    assert 'return line.lstrip().startswith("```")' in mine
    assert 'if line.lstrip().startswith("```")' in fam
    assert 'return String(line).trimStart().startsWith("```")' in js
