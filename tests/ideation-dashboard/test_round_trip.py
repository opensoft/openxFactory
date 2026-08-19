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


# ---- the fence rule: ONE shared line-split + two independent fence toggles ---
#
# design Decision 2 named this hazard when it chose a new module: `round_trip.py`,
# `doc_health.families` and `web/views/outline-model.js` each carry the same
# naive ``` PREDICATE (`line.lstrip().startswith("```")` / `String(line)
# .trimStart().startsWith("```")`), independently spelled three times and pinned
# textually by `test_the_shared_predicate_is_spelled_the_same_in_all_three` below.
# Sharing THAT code is not available — one of the three is JavaScript in the
# browser bundle — so the mitigation for the predicate itself stays this pair of
# agreement tests.
#
# The LINE-SPLIT underneath the predicate is a narrower story, and it changed
# under `align-status-reader-to-real-lines`'s wide ruling (2026-08-19,
# adversarial-review finding C3): `round_trip.py`'s `_section_bounds` and
# `doc_health.families._scan_lines` now BOTH split through the same
# `doc_health.lines.split_keepends` (real lines: CR/LF/CRLF only), so on any
# input the two Python call sites cannot diverge on WHERE a line is — only on a
# bug in one's own fence-toggle loop, which is what the agreement test below
# still exists to catch.
#
# `outline-model.js`'s OWN split is not one rule, corrected (finding F1, a
# focused re-verify): `outlineSections` (the function this test's JS probe
# calls) splits with `text.split("\n")` at outline-model.js:46 — LF ONLY —
# while `endsInsideFence`/`insertSection` split with the real-line regex
# `text.split(/\r\n|\r|\n/)` at outline-model.js:273/:319. The two disagree
# on their own, INSIDE the JS file, on a CR-only document (demonstrated:
# `outlineSections` folds two `##` lines into one section, `endsInsideFence`
# reads them as two). That pre-existing JS-internal inconsistency is out of
# scope for this Python-side change — the fixtures below carry no bare-CR
# input, so it is held by NEITHER test here, and fixing the JS is not
# attempted. What `outlineSections` does share with the Python side, on
# every fixture this test actually exercises (LF-only markdown), is the
# outcome, not the rule: no fixture here distinguishes LF-only splitting
# from real-line splitting, because none contains a lone CR or an exotic
# separator adjacent to a `##`/```` ``` ```` boundary.
#
# What `test_all_three_fence_implementations_agree` compares is therefore two
# implementations of the full heading-detection behavior on THESE
# fixtures — ONE Python (unified line-split, two independent fence loops)
# and ONE JS — not three independently-splitting ones on these inputs, even
# though it is still useful to run the comparison against both Python call
# sites explicitly (a regression in either one's fence-toggle loop alone
# would still be caught).
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


# ---- review F2: ends-inside-fence, the FOURTH agreed behavior -----------------


UNCLOSED = ("# Staged: t\n\nStatus: staged\n\nExample:\n\n"
            "```markdown\n## Claims\n\n- x\n")


def test_an_unclosed_fence_refuses_the_insert_rather_than_writing_into_it():
    """Review F2. The insert would land INSIDE the open fence, where
    `find_provenance_section` cannot see it — so the next pass inserts again, and
    the ratified idempotence clause (which carries no qualifier) is broken: 1 -> 2
    -> 3 sections. `outline-model.js` already refuses this exact input on the JS
    side; the rule is now the same on both."""
    assert rt.ends_inside_fence(UNCLOSED) is True
    once = rt.fill_provenance_slots(UNCLOSED, PROVENANCE)
    assert once == UNCLOSED, "nothing may be written into an open fence span"
    assert once.count(rt.PROVENANCE_HEADING) == 0


def test_the_unclosed_fence_refusal_is_idempotent_to_any_depth():
    """The property the defect broke, asserted past the point it used to fail."""
    text = UNCLOSED
    for _ in range(4):
        text = rt.refresh_fragment(
            text, proposal_text=PROPOSAL, provenance=PROVENANCE)
        assert text == UNCLOSED


def test_closing_the_fence_restores_the_insert_and_stays_idempotent():
    """The refusal is about the fence and nothing else — the remedy it names
    actually works."""
    closed = UNCLOSED + "```\n"
    assert rt.ends_inside_fence(closed) is False
    once = rt.fill_provenance_slots(closed, PROVENANCE)
    assert once.count(rt.PROVENANCE_HEADING) == 1
    assert rt.fill_provenance_slots(once, PROVENANCE) == once


def test_slots_already_outside_the_fence_are_still_filled():
    """The refusal is narrow: it withholds the INSERT, not the whole refresh. A
    provenance section that is findable outside the open fence is safely
    rewritable, and refusing that too would punish a document for a defect
    somewhere below it."""
    findable = ("# Staged: t\n\nStatus: staged\n\n"
                + rt.PROVENANCE_HEADING + "\n\nChange ID: none yet\n"
                "Raised: n/a\nStatus at demote: n/a\nDemoted: n/a\n"
                "Demote reason: n/a\n\nExample:\n\n```markdown\n## Claims\n")
    assert rt.ends_inside_fence(findable) is True
    out = rt.fill_provenance_slots(findable, PROVENANCE)
    assert "Change ID: add-worked-example" in out
    assert out.count(rt.PROVENANCE_HEADING) == 1
    assert rt.fill_provenance_slots(out, PROVENANCE) == out


_ENDS_FENCE_PROBE = """
import { readFileSync } from 'node:fs';
import { endsInsideFence } from %(model)s;
const cases = JSON.parse(readFileSync(%(cases)s, 'utf8'));
const out = {};
for (const [name, text] of Object.entries(cases)) out[name] = endsInsideFence(text);
console.log(JSON.stringify(out));
"""

ENDS_FENCE_FIXTURES = {
    **FENCE_FIXTURES,
    "unclosed_markdown": UNCLOSED,
    "closed_after_unclosed": UNCLOSED + "```\n",
    "three_fences": "a\n```\nb\n```\nc\n```\nd\n",
    "fence_only": "```\n",
    # THE SCHEDULED FIXTURE, built (align-status-reader-to-real-lines, C6): an
    # exotic separator SHARING a real line with a fence marker, so the OLD
    # pseudo-line rule would split the marker onto its own pseudo-line (and
    # toggle on it) where the real-line rule does not, because the marker is
    # not at the START of the real line. Measured: before this change's
    # families.py conversion, `families._scan_lines`'s implied fence state
    # disagreed (True) with `round_trip.ends_inside_fence`/outline-model.js's
    # `endsInsideFence` (both False, correctly) on both of these. After the
    # conversion all three agree.
    "form_feed_fence": "## one\nbody\x0c```after\n## two\n",
    "u2028_fence": "## one\nbody" + chr(0x2028) + "```after\n## two\n",
}


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_ends_inside_fence_agrees_with_outline_model_js():
    """The FOURTH agreed behavior, and WHAT IT ACTUALLY PINS.

    It pins TWO implementations directly: `round_trip.ends_inside_fence` against
    `outline-model.js`'s `endsInsideFence`, over twelve fixtures (ten shared with
    `ENDS_FENCE_FIXTURES`'s ancestors plus the two exotic-separator fixtures
    below). `doc_health.families` has no `ends_inside_fence`-shaped predicate at
    all, so `implied` is not a third implementation's independent answer — it
    RETYPES the backtick test rather than consuming `_scan_lines`' own
    `in_fence` flag. It is kept as a cheap consistency check on the shared
    rule, not as a third pin, and saying so is the point: a test that
    overstates its reach is worse than a narrow one, because the gap it
    leaves is invisible.

    THE UPGRADE PATH IS NO LONGER BLOCKED (align-status-reader-to-real-lines,
    finding C6). This docstring used to say the real three-way pin this test
    wants — a fixture carrying an exotic separator (`\\x0c`, U+2028, …), the
    input where a pseudo-line rule and a real-line rule genuinely diverge —
    was blocked because building it would also expose the (then-unfixed)
    read/write divergence in `corpus.parse_status`. This change's wide ruling
    removed that blocker: `corpus.parse_status` was fixed first (its own
    commit), and `families._scan_lines`'s line-split converted alongside it.
    `form_feed_fence` and `u2028_fence` below are that fixture, built. The
    two REAL pins (`rt.ends_inside_fence` vs. `outline-model.js`'s
    `endsInsideFence`) already agreed on this exotic input even before the
    `families.py` conversion — both split real lines already — so it was
    `implied`, the families-based consistency check, that disagreed until
    `families._scan_lines` converted too; it agrees now.
    """
    with TemporaryDirectory() as tmp:
        cases = Path(tmp) / "cases.json"
        cases.write_text(json.dumps(ENDS_FENCE_FIXTURES), encoding="utf-8")
        script = Path(tmp) / "probe.mjs"
        script.write_text(_ENDS_FENCE_PROBE % {
            "model": json.dumps(str(OUTLINE_MODEL_JS)),
            "cases": json.dumps(str(cases)),
        }, encoding="utf-8")
        done = subprocess.run([NODE, str(script)], capture_output=True, text=True)
        assert done.returncode == 0, done.stderr
        js = json.loads(done.stdout)
    for name, text in sorted(ENDS_FENCE_FIXTURES.items()):
        mine = rt.ends_inside_fence(text)
        assert mine == js[name], f"{name}: round_trip={mine}, outline-model.js={js[name]}"
        # A consistency check on the shared RULE, not a third implementation's
        # answer: this retypes the backtick test because `_scan_lines` does not
        # report its final fence state. See the docstring.
        implied = sum(1 for _lineno, line, _f in families._scan_lines(text)
                      if line.lstrip().startswith("```")) % 2 == 1
        assert mine == implied, name


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
