"""THE REPORT SECTION: what a reader of `### modified-block-currency` is told.

`add-modified-block-currency-check`, Speckit feature
`022-modified-block-currency-reporting` (packet § 5.1–5.3). F1
(`019-…-family`) built the family and its four finding classes; F2
(`020-…-fixtures`) built the regression catalogue; F3 (`021-…-self-gate`)
asserted the verdict over this repository. **F4 is where the split the delta
drew reaches the reader**, and where two boundaries that hold by accident start
holding on purpose.

THE PROBLEM § 5.1 NAMES. The family's arms are already distinct FINDINGS with
distinct severities — the delta requires that ("SHALL report them as distinct
finding classes so that a precise signal is never buried in an editorial one").
The report does not carry the distinction: the section is a flat list of nine
long rows, and learning "one scenario was dropped, eight blocks diverge
editorially" means reading all nine and tallying. § 5.1 asks for the split to be
visible WITHOUT COUNTING.

WHAT THIS FILE ASSERTS, in the three groups the packet splits:

  1. **§ 5.1 — the tally.** The class map partitions every finding the family
     can emit; the summary states each class's count with its severity band;
     the block renders when the family RAN and never when it was skipped; and a
     finding the map cannot place is counted in a named residual row rather
     than dropped.
  2. **§ 5.2 — the action line.** Already landed with F1 as `_ACTION`, verbatim
     § 5.2's wording, which makes § 5.2 a PIN rather than an addition
     (`specs/022-…/research.md` R7). Pinned here on the finding AND on the
     rendered `action="…"`; and the marker class's own distinct action pinned
     beside it, because § 5.2 says "the action line" and the family has two.
  3. **§ 5.3 — the workflow boundary.** No per-family option reaches this
     family, and none exists to reach it. A NEW assertion of this family's own,
     as § 5.3 asks: `test_workflow_contract.py` pins that boundary for
     `promotion-fidelity` in a shape written for that family. **The workflow
     file is READ here and edited nowhere.**

THREE SPELLINGS OF ONE CLASSIFICATION, AND THAT IS DELIBERATE. F2's
`CLASSIFIERS` dict is a test-side classifier over five keys; this feature's
`modified_block_currency.CLASSES` is the production map over FOUR classes (the
delta names three arms and one non-arm class, and "title resolution and
ordering" is ONE arm with two shapes); and `test_every_finding_over_the_fixture_
corpus_lands_in_exactly_one_class` below recomputes the partition
independently. F2's own docstring argues for the redundancy — "an arm's wording
drifting in EITHER file fails loudly instead of silently reclassifying" — and
this file adds a third witness rather than collapsing the other two.

WHY THE PRODUCTION MAP IS ANCHORED WHERE F2's IS NOT. F2's keys are substring
probes over the whole rule text, which is right for a fixture corpus whose
titles it wrote. The production map reads CORPUS-SUPPLIED titles, so a
requirement titled `'X omits 1 of the 2 scenarios Y'` would make a
carriage-ledger finding match the titles probe too. Every production pattern is
therefore anchored at the start of the rule AND past the closing quote of the
title's `repr` — measured against exactly that constructed case in
`test_a_title_that_embeds_another_class_s_phrase_does_not_misfile_the_finding`.
"""

from __future__ import annotations

import inspect
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from doc_health import INFO, WARNING, Finding, Skip
from doc_health import modified_block_currency as mbc
from doc_health import report, runner

from conftest import AS_OF, FIXTURES, REPO_ROOT, make_ctx

WORKFLOW = REPO_ROOT / ".github" / "workflows" / "doc-health-reusable.yml"

# The fixture trees F2 built, by the state each one puts the family in. Named
# rather than globbed: this file asserts about STATES (ran-with-findings,
# ran-quiet, skipped) and each name below is a claim about which state its tree
# produces, checked by the tests that use it.
TREE_RICH = "modified-block-currency-two-writers"   # 9 ordering + 1 ledger
TREE_MARKERS = "modified-block-currency-markers"    # 1 marker + 3 ledger
TREE_RESOLUTION = "modified-block-currency-resolution"  # 2 resolution + 1 ledger
TREE_TITLES = "modified-block-currency-history-329"     # 1 titles + 1 ledger
TREE_QUIET = "modified-block-currency-quiet"        # ran, found nothing
TREE_NOSCOPE = "modified-block-currency-noscope"    # the family's own Skip

ALL_TREES = tuple(sorted(
    p.name for p in FIXTURES.iterdir()
    if p.is_dir() and p.name.startswith("modified-block-currency")))


def _real_ctx():
    """This repository, at the size the family reads — F3's stand-in.

    Two attributes, and `test_modified_block_currency_self_gate.py::
    test_the_family_reads_exactly_two_things_from_its_run_context` is what keeps
    that faithful. `agg_root=None` is the single-repo scope, in which no
    disposition can suppress anything.
    """
    class Ctx:
        repo_paths = {"openxFactory": REPO_ROOT}
        agg_root = None
    return Ctx()


def _fixture_findings(tree):
    out = mbc.fam_modified_block_currency(make_ctx(tree))
    return [] if isinstance(out, Skip) else out


# ============================================================================
# 1. THE CLASS MAP (§ 5.1, FR-005, FR-006 — foundational)
# ============================================================================

def test_the_class_registry_is_closed_ordered_and_states_a_band_per_class():
    """FOUR CLASSES, and the module's own docstring already says so: "THREE
    ARMS, FOUR FINDING CLASSES, AND THE NUMBERS DIFFER ON PURPOSE".

    Ordered, because the rendered block's order is part of its contract — the
    gate-bearing arm reads first, for the same reason the family sorts its own
    findings severity-first. Closed, because an unrecognized finding must reach
    the residual row rather than a neighbouring class (constitution VII).

    THE BANDS ARE READ FROM THE MODULE'S OWN CONSTANTS, never re-spelled: a
    literal `"warning"` here would keep passing through § 7.2's flip of
    `_LAUNCH_SEVERITY` to `error` and would then describe the report wrongly.
    """
    ids = [c.id for c in mbc.CLASSES]
    assert ids == ["scenario-titles", "carriage-ledger",
                   "title-resolution", "marker-defects"]
    bands = {c.id: c.band for c in mbc.CLASSES}
    assert bands == {
        "scenario-titles": mbc._LAUNCH_SEVERITY,
        "carriage-ledger": mbc._LEDGER_SEVERITY,
        "title-resolution": mbc._RESOLUTION_SEVERITY,
        "marker-defects": mbc._LEDGER_SEVERITY,
    }
    actions = {c.id: c.action for c in mbc.CLASSES}
    assert actions == {
        "scenario-titles": mbc._ACTION,
        "carriage-ledger": mbc._ACTION,
        "title-resolution": mbc._ACTION,
        "marker-defects": mbc._MARKER_ACTION,
    }
    # every class carries a rendered label, and no two share one
    labels = [c.label for c in mbc.CLASSES]
    assert len(set(labels)) == 4, labels


def test_each_of_the_five_rule_shapes_classifies_into_its_own_class():
    """FIVE SHAPES, FOUR CLASSES. The delta's third arm is "Title resolution and
    ordering" — one arm, two shapes (a block resolving to nothing, and an
    ordering no declaration settles). They share a severity and an action and
    the delta names them together, so splitting them in the report would claim a
    fifth class the delta does not define.

    Driven by F2's fixture trees rather than by hand-written rule text: a
    hand-copied rule text in this file could drift from the arms and the test
    would keep passing on its own copy.
    """
    def classes_over(tree):
        return {mbc.classify(f) for f in _fixture_findings(tree)}

    assert classes_over(TREE_TITLES) == {"scenario-titles", "carriage-ledger"}
    assert classes_over(TREE_MARKERS) == {"marker-defects", "carriage-ledger"}
    assert classes_over(TREE_RESOLUTION) == {"title-resolution",
                                             "carriage-ledger"}
    assert classes_over(TREE_RICH) == {"title-resolution", "carriage-ledger"}
    # ...and the two shapes of the third arm really are two shapes, not one
    # fixture reached twice: their rule texts differ in their opening phrase.
    opens = {f.rule.split(" for ")[0] if " for " in f.rule else f.rule
             for tree in (TREE_RESOLUTION, TREE_RICH)
             for f in _fixture_findings(tree)
             if mbc.classify(f) == "title-resolution"}
    assert opens == {"active MODIFIED block", "the ordering of MODIFIED blocks"}


def test_every_finding_over_the_fixture_corpus_lands_in_exactly_one_class():
    """THE PARTITION, recomputed independently of F2's `CLASSIFIERS`.

    Over all thirteen trees, every finding matches exactly one production
    pattern. A rule text edited without the map reds here — and, on the
    artifact, becomes an `unclassified` row, which is the same defect seen from
    the reader's side.
    """
    seen = 0
    for tree in ALL_TREES:
        for f in _fixture_findings(tree):
            seen += 1
            hits = [c.id for c in mbc.CLASSES
                    if mbc.classify(f) == c.id]
            assert len(hits) == 1, (tree, hits, f.rule[:140])
            assert mbc.classify(f) != mbc.UNCLASSIFIED, (tree, f.rule[:140])
    assert seen >= 25, (
        f"only {seen} findings over {len(ALL_TREES)} fixture trees — discovery "
        f"is broken, not clean, and a partition over nothing proves nothing")


def test_every_finding_over_the_real_tree_lands_in_exactly_one_class():
    """The same property over the corpus a steward's report is computed from.

    Fixtures prove the map against text this packet wrote; this proves it
    against text it did not. The count is a FLOOR, never an equality: this
    assertion must not fall due every time the corpus moves (F3's § 4.1
    reasoning, and the reason its own count assertions are named-subject).
    """
    findings = mbc.fam_modified_block_currency(_real_ctx())
    assert not isinstance(findings, Skip)
    assert len(findings) >= 1, (
        "the family reports nothing over this checkout, so the partition below "
        "is vacuous — check the resolver before the map")
    for f in findings:
        assert mbc.classify(f) != mbc.UNCLASSIFIED, f.rule[:200]


def test_a_title_that_embeds_another_class_s_phrase_does_not_misfile_the_finding():
    """WHY THE PRODUCTION PATTERNS ARE ANCHORED PAST THE TITLE'S `repr`.

    Requirement titles come from the corpus, so a title may contain any phrase —
    including another class's. A carriage-ledger finding for a requirement
    titled `'X omits 1 of the 2 scenarios Y'` matches an UNANCHORED titles probe
    as well as the ledger one, and a first-match-wins classifier files it under
    the gate-bearing arm: a `warning` count inflated by an `info` row, on the
    one line § 5.1 exists so a reader can trust without counting.

    F2's test-side `CLASSIFIERS` are unanchored and correct for what they read —
    a fixture corpus whose titles F2 wrote. This is the production map's own
    obligation, and the case is constructed because the corpus has no such title
    today, which is exactly when a rule is worth pinning.
    """
    evil_title = "X omits 1 of the 2 scenarios Y"
    ledger = Finding(
        INFO, mbc.FAMILY, "openxFactory", "openspec/changes/c/specs/a/spec.md",
        f"active MODIFIED block for {evil_title!r} does not carry 1 of the 3 "
        f"body units and scenario bullets openspec/specs/a/spec.md currently "
        f"states for it — a divergence this arm CANNOT distinguish from a "
        f"deliberate rewording, and does not claim to: [body] 'z'",
        mbc._ACTION)
    assert mbc.classify(ledger) == "carriage-ledger"
    # and the unanchored reading really would have misfiled it, so the anchor is
    # load-bearing rather than defensive
    assert re.search(r"omits \d+ of the \d+ scenarios", ledger.rule)


def test_a_title_carrying_a_quote_still_classifies():
    """`{title!r}` switches to double quotes when the title contains a single
    one, so the pattern admits both quotings. A title neither quoting handles
    cleanly would fall to the residual row, which is the fail-closed direction.
    """
    titled = Finding(
        WARNING, mbc.FAMILY, "openxFactory", "openspec/changes/c/specs/a/spec.md",
        'active MODIFIED block for "It\'s a requirement" omits 2 of the 4 '
        "scenarios openspec/specs/a/spec.md currently states for it: 'A', 'B'",
        mbc._ACTION)
    assert mbc.classify(titled) == "scenario-titles"


# ============================================================================
# 2. THE TALLY AND ITS RENDERED LINES (§ 5.1, FR-001..FR-003, FR-006, FR-007)
# ============================================================================

_LEAD = ("Finding classes, counted apart so the gate-bearing arm is never read "
         "as one of the editorial rows:")


def test_the_summary_states_every_class_with_its_count_and_band():
    """The contract of `contracts/report-section.md` § 1, over a real fixture
    tree so the counts are measured rather than asserted about themselves."""
    findings = _fixture_findings(TREE_MARKERS)
    lines = mbc.class_summary(findings)
    assert lines[0] == _LEAD
    assert lines[1:] == [
        "- scenario-title completeness: 0 (`warning` — the arm carrying this "
        "family's gate)",
        "- carriage ledger: 3 (`info` — editorial, and the arm says so in "
        "every finding)",
        "- title resolution and ordering: 0 (`warning`)",
        "- marker defects: 1 (`info`)",
    ]


def test_the_summary_counts_sum_to_the_findings_it_was_handed():
    """INVARIANT I1 — the tally can never omit a row. Asserted over every
    fixture tree AND the real tree, by reading the counts back out of the
    rendered lines rather than out of the function's internals: a tally that
    agreed with itself and disagreed with the text would pass any other
    formulation of this test."""
    def counts_in(lines):
        return sum(int(m.group(1)) for line in lines
                   for m in [re.search(r": (\d+) \(`", line)] if m)

    for tree in ALL_TREES:
        findings = _fixture_findings(tree)
        assert counts_in(mbc.class_summary(findings)) == len(findings), tree
    real = mbc.fam_modified_block_currency(_real_ctx())
    assert counts_in(mbc.class_summary(real)) == len(real)


def test_a_finding_the_map_cannot_place_is_counted_and_named():
    """THE RESIDUAL ROW, and it renders only when it is nonzero.

    A tally that can silently omit rows is worse than no tally: a reader who
    trusts `1 / 8 / 0 / 0` on a report where two rows went uncounted has been
    told something false by the one line whose whole purpose is to be trusted
    without counting. Loud in the artifact, and NOT an exception — a
    presentational defect must not be able to abort a nightly report.
    """
    orphan = Finding(INFO, mbc.FAMILY, "openxFactory", "openspec/changes/c/specs/a/spec.md",
                     "a rule text no pattern of this family's map recognizes",
                     mbc._ACTION)
    assert mbc.classify(orphan) == mbc.UNCLASSIFIED

    lines = mbc.class_summary([orphan])
    assert any(line.startswith("- unclassified: 1 —") for line in lines), lines
    assert "the map has drifted from the arms" in lines[-1]

    # ...and it is absent from a fully classified set
    clean = mbc.class_summary(_fixture_findings(TREE_TITLES))
    assert not any("unclassified" in line for line in clean), clean


def test_the_summary_reads_the_findings_and_nothing_else():
    """FR-007, STRUCTURALLY (analyze finding A1).

    "It only reads the findings" is not a guarantee if the only evidence is that
    someone read the function once. The signature admits one argument, and the
    source names no context, no path and no reader — so there is nothing for a
    corpus read or a second family run to arrive through. This is F1's
    `test_the_promoted_reader_cannot_reach_a_measurement_basis` in the shape it
    established.
    """
    assert list(inspect.signature(mbc.class_summary).parameters) == ["findings"]
    assert list(inspect.signature(mbc.classify).parameters) == ["finding"]
    for fn in (mbc.class_summary, mbc.classify):
        src = inspect.getsource(fn)
        # MATCHED ON USE, NOT ON MENTION — the lesson this family's tests have
        # learned three times: a docstring that NAMES what it refuses to use
        # must not fail a probe on the refusal.
        body = re.sub(r'"""(?:.|\n)*?"""', "", src)
        for pattern in (r"\bctx\b", r"\bPath\s*\(", r"\bopen\s*\(",
                        r"\.read_text\s*\(", r"\.glob\s*\(",
                        r"fam_modified_block_currency\s*\("):
            assert not re.search(pattern, body), (fn.__name__, pattern)


# ============================================================================
# 3. THE BLOCK REACHES THE REPORT (§ 5.1, US1 — FR-001..FR-004, FR-011)
# ============================================================================

def _render(result) -> str:
    """One in-process rendering of a `RunResult`, the shape
    `test_promotion_fidelity.py::test_the_report_states_the_basis_under_the_family_heading`
    established. No subprocess: every state this group asserts is reachable
    without spawning a checker run, and a test that spawns one pays for a
    hermeticity argument it does not need."""
    return report.render(AS_OF, result.findings, result.skips, [], [], 0, [],
                         [], family_notes=result.notes)


def _section(text: str, family: str = mbc.FAMILY) -> str:
    start = text.index(f"### {family}\n")
    rest = text[start:]
    end = rest.find("\n### ")
    return rest if end < 0 else rest[:end]


def _suite(tree: str, skip: bool = False):
    """The family, through the runner, over one fixture tree.

    `only_family` is set even when skipping, so the preflight pass — which
    shells out — never runs. The skip path under test is the `--skip-family`
    branch, and it is reached identically either way.
    """
    return runner.run_suite(make_ctx(tree), mbc.FAMILY,
                            {mbc.FAMILY} if skip else set())


def test_the_summary_registry_is_keyed_by_family_and_takes_findings():
    """TWO REGISTRIES, ASSERTED APART. `FAMILY_NOTES` is `(ctx) -> lines`, a
    fact about the RUN — which tree promotion fidelity measured. `FAMILY_SUMMARIES`
    is `(findings) -> lines`, a fact about the FINDINGS. Widening the first to
    carry the second would have put a findings-derived line behind a ctx-derived
    channel and changed `basis_notes`' contract for no gain
    (`specs/022-…/research.md` R1).

    Both memberships are asserted, so neither "absent from" claim can pass
    against a registry that has quietly emptied.
    """
    from doc_health.families import FAMILIES, FAMILY_NOTES, FAMILY_SUMMARIES

    assert mbc.FAMILY in FAMILIES, "the claims below mean nothing otherwise"
    assert set(FAMILY_SUMMARIES) == {mbc.FAMILY}
    assert FAMILY_SUMMARIES[mbc.FAMILY] is mbc.class_summary
    assert set(FAMILY_NOTES) == {"promotion-fidelity"}
    assert mbc.FAMILY not in FAMILY_NOTES


def test_the_block_renders_under_the_heading_before_the_first_row():
    """§ 5.1's whole point: the split is stated before the rows, so a reader has
    it before they start reading them."""
    section = _section(_render(_suite(TREE_MARKERS)))
    assert _LEAD in section
    assert "- marker defects: 1 (`info`)" in section
    assert section.index(_LEAD) < section.index("- [info] ")
    # the block is followed by a blank line, so it reads as a block rather than
    # as the first of the rows
    assert "- marker defects: 1 (`info`)\n\n- [" in section


def test_the_block_renders_on_a_run_that_found_nothing():
    """A clean run is exactly where an unstated split misleads: "No findings."
    reads as a verdict, and a reader who does not know WHICH classes were
    measured cannot tell a quiet corpus from an arm that stopped firing. All
    four counts read 0 and the block still renders — the same argument
    `test_the_report_states_the_basis_on_a_family_with_no_findings` makes for the
    basis note."""
    result = _suite(TREE_QUIET)
    assert result.findings == [] and result.skips == []
    section = _section(_render(result))
    assert _LEAD in section
    assert "- scenario-title completeness: 0 (`warning`" in section
    assert "No findings." in section
    assert section.index(_LEAD) < section.index("No findings.")


def test_a_family_skipped_by_run_configuration_carries_no_block():
    """A SKIP IS THE ABSENCE OF A MEASUREMENT, and `0 · 0 · 0 · 0` beside one
    would claim a measurement nobody took — precisely what canon's skip rule
    exists to prevent ("cannot run", not "found nothing").

    THIS IS THE OPPOSITE CALL FROM `FAMILY_NOTES`, deliberately, and the
    difference is asserted here rather than left to be rediscovered: a basis note
    answers "which tree WOULD this family have measured", which is still true of
    a skipped run, so promotion fidelity's note renders beside its skip line. A
    tally has no such reading.
    """
    result = _suite(TREE_MARKERS, skip=True)
    assert [s.family for s in result.skips] == [mbc.FAMILY]
    assert mbc.FAMILY not in result.notes
    section = _section(_render(result))
    assert "Skipped: skipped by run configuration" in section
    assert _LEAD not in section
    assert "scenario-title completeness" not in section
    # POSITIVE CONTROL, and without it this test passes on a tree where the
    # mechanism does not exist at all — which is how an "absent from" assertion
    # lies. The SAME tree, not skipped, must carry the block.
    assert _LEAD in _section(_render(_suite(TREE_MARKERS)))


def test_the_family_s_own_scope_skip_carries_no_block_either():
    """The SECOND skip shape, and it is a different code path with a different
    reason string: a scope carrying no `openspec/changes/` directory at all. Two
    tests because canon distinguishes them and because one guard covering both is
    a claim worth checking rather than assuming."""
    result = _suite(TREE_NOSCOPE)
    assert len(result.skips) == 1
    assert "openspec/changes/" in result.skips[0].reason
    section = _section(_render(result))
    assert "Skipped:" in section
    assert _LEAD not in section
    # POSITIVE CONTROL — same reason as the test above.
    assert _LEAD in _section(_render(_suite(TREE_MARKERS)))


def test_the_rendered_counts_equal_the_rendered_rows():
    """SC-001, READ BACK OUT OF THE ARTIFACT.

    Both sides parsed from the SAME rendered section — the counts from the block,
    the rows from the lines beneath it — rather than one side taken from the
    finding list the block was computed from. A tally that agreed with its own
    input and disagreed with the text printed under it would pass any weaker
    formulation of this test, and the text is what the reader has.
    """
    for tree in (TREE_TITLES, TREE_MARKERS, TREE_RESOLUTION, TREE_RICH,
                 TREE_QUIET):
        section = _section(_render(_suite(tree)))
        stated = sum(int(m.group(1)) for line in section.splitlines()
                     for m in [re.search(r": (\d+) \(`", line)] if m)
        rows = len([line for line in section.splitlines()
                    if line.startswith("- [")])
        assert stated == rows, (tree, stated, rows, section)


# ============================================================================
# 4. THE ACTION LINE, AND NOTHING ELSE MOVES (§ 5.2, US2 — FR-008..FR-013)
# ============================================================================
#
# § 5.2 READS AS IF THE ACTION LINE WERE F4's TO ADD. It is not: F1 landed it as
# `_ACTION`, verbatim § 5.2's wording, and it has been rendering in the ranked
# plan since. Read as "add", § 5.2 is a no-op; read as "pin", it is a real
# deliverable, and the pin is what this group is (`specs/022-…/research.md` R7).
#
# THERE IS NO PER-FAMILY ACTION REGISTRY IN THIS SUITE. Each family constructs
# its findings with an `action=` argument and `report.plan_line` renders it as
# `action="…"`. So "where do per-family action lines live" resolves to: at each
# family's own finding construction — which is why the byte-identity assertion
# below is over the RENDERED plan rows of other families rather than over a
# table that does not exist.

_ARMS_ACTION = ("restate the requirement as canon currently states it, or "
                "declare the deletion with a `Removed from canon by` marker")


def test_the_arms_action_is_verbatim_what_the_packet_asks_for():
    """§ 5.2's text, spelled out here ONCE and compared with the module's own
    constant. Spelling it out is the point: a test that asserted
    `f.action == mbc._ACTION` would pass whatever `_ACTION` had been changed to,
    and § 5.2 is a requirement about the WORDS."""
    assert mbc._ACTION == _ARMS_ACTION
    assert mbc._MARKER_ACTION != mbc._ACTION


def test_every_finding_carries_its_class_s_band_and_action():
    """INVARIANT I4, over every fixture tree and the real tree.

    This is what ties the rendered `(warning)` / `(info)` caption to the rows
    beneath it: the caption is read from the class table, so a finding whose
    severity had drifted from its class's band would be described wrongly by a
    line nobody could check by eye. And it is the § 5.2 pin at finding level —
    each class's action, on every finding of that class.
    """
    by_id = {klass.id: klass for klass in mbc.CLASSES}
    checked = {klass.id: 0 for klass in mbc.CLASSES}
    findings = [f for tree in ALL_TREES for f in _fixture_findings(tree)]
    findings += list(mbc.fam_modified_block_currency(_real_ctx()))
    for f in findings:
        klass = by_id[mbc.classify(f)]
        checked[klass.id] += 1
        assert f.severity == klass.band, (klass.id, f.severity, f.rule[:120])
        assert f.action == klass.action, (klass.id, f.rule[:120])
    # every class actually exercised, or the loop above proves nothing about it
    assert all(checked.values()), checked


def test_the_action_renders_in_the_ranked_plan_for_every_one_of_our_rows():
    """The finding-level pin above says the action is SET. This says it is
    RENDERED — `report.plan_line`'s `action="…"` — because § 5.2 is a requirement
    about what the report carries, and a field nothing prints is not an action
    line."""
    text = _render(_suite(TREE_MARKERS))
    plan = text[text.index("## Ranked Plan"):]
    rows = [line for line in plan.splitlines()
            if f"family={mbc.FAMILY}" in line]
    assert rows, "no row of this family reached the ranked plan"
    for row in rows:
        assert (f'action="{_ARMS_ACTION}"' in row
                or f'action="{mbc._MARKER_ACTION}"' in row), row
    # both actions present on this tree, so the `or` above is not hiding one
    assert any(f'action="{_ARMS_ACTION}"' in r for r in rows)
    assert any(f'action="{mbc._MARKER_ACTION}"' in r for r in rows)


def test_the_marker_class_keeps_its_own_action_and_not_the_arms_one():
    """§ 5.2 SAYS "THE ACTION LINE" AND THE FAMILY HAS TWO. The split is correct
    and F1 argued it: the remedy for an uncarried unit is to restate it or
    declare it removed, and the remedy for a marker naming a unit the block still
    carries is to fix the marker. Recorded as an imprecision in § 5.2 rather than
    a defect in the code (`specs/022-…/research.md` R7).
    """
    marker_findings = [f for f in _fixture_findings(TREE_MARKERS)
                       if mbc.classify(f) == mbc.CLASS_MARKERS]
    assert len(marker_findings) == 1
    assert marker_findings[0].action == mbc._MARKER_ACTION
    assert _ARMS_ACTION not in marker_findings[0].action


def _other_family_findings():
    """One finding for each of four other families, with their own actions.

    Hand-built rather than run: the subject under test is whether THIS family's
    rendering perturbs another family's LINES, and hand-built findings make the
    before/after comparison exact and corpus-independent.
    """
    return [
        Finding("critical", "ratified-provenance", "openxFactory", "docs/a.md",
                "Ratified by: missing", "name the approving change"),
        Finding("error", "promotion-fidelity", "openxFactory",
                "openspec/changes/archive/x/specs/a/spec.md",
                "archived delta not promoted",
                "apply the ratified delta, or record the non-promotion"),
        Finding(WARNING, "duplicate-packet", "openxFactory",
                "openspec/changes/archive/y/proposal.md",
                "one ruling discharged twice",
                "name the packet you restate, or withdraw the duplicate"),
        Finding(INFO, "release-inventory-drift", "openxFactory",
                "contracts/manifest.yaml", "inventory lags the cut",
                "cut the release"),
    ]


def test_no_other_family_s_section_or_action_line_moves(monkeypatch):
    """BYTE IDENTITY, PROVED IN PROCESS AND CORPUS-FREE.

    Two renders of ONE finding set, differing only by whether the summary
    registry carries this family. Every line outside `### modified-block-currency`
    must be identical — every other family's section, every other family's
    ranked-plan row, every `action="…"` in them, the headline, the per-stage
    table, the preflight block.

    WHY THIS AND NOT ONLY F3's SUBPROCESS GATE. F3's
    `test_the_report_moves_only_in_this_family_s_lines` proves the same property
    over the real corpus and is not duplicated here. It cannot fail on a
    mechanism defect that the corpus happens not to exercise, and it cannot
    isolate the RENDERER from the FAMILY. This one can: the finding set is fixed,
    so any difference is the renderer's.
    """
    from doc_health import families

    findings = _other_family_findings() + list(_fixture_findings(TREE_MARKERS))
    result = runner.RunResult(findings=list(findings))

    with_summary = _render(result)
    monkeypatch.setattr(families, "FAMILY_SUMMARIES", {})
    without = _render(result)

    ours = f"### {mbc.FAMILY}"
    assert _LEAD in with_summary and _LEAD not in without, (
        "the two renders are the same, so this comparison is vacuous")

    def outside_our_section(text):
        keep, inside = [], False
        for line in text.splitlines():
            if line.startswith("### "):
                inside = line.strip() == ours
            if not inside:
                keep.append(line)
        return keep

    assert outside_our_section(with_summary) == outside_our_section(without), (
        "the report moved OUTSIDE this family's section. The render branch must "
        "emit NOTHING for a family with no summary entry — a stray blank line "
        "for every family fails exactly here, which is what this test is for.")

    # and the sections of the four other families are byte-identical by name,
    # so the sweep above cannot have passed by dropping them all
    for family in ("ratified-provenance", "promotion-fidelity",
                   "duplicate-packet", "release-inventory-drift"):
        assert _section(with_summary, family) == _section(without, family), family

    # ------------------------------------------------------------------
    # ADDED BY THE MUTATION ROUND (M4), WHICH THIS TEST SURVIVED.
    #
    # Everything above compares registry-ON with registry-OFF, and that
    # comparison is BLIND to any change the render branch makes for EVERY
    # family — a mutant appending one unconditional blank line per section
    # perturbed all twenty-two of them and passed twenty-six green tests,
    # because it perturbed both sides of the comparison identically.
    #
    # So the before-state has to be stated, not differenced: for a family with
    # neither a note nor a summary entry, the section is its heading, ONE blank
    # line, and then its rows — which is what `report.render` emitted before
    # this feature existed. Exact text, deliberately: this is the one assertion
    # in the file whose whole value is that it cannot be satisfied by a
    # relative comparison.
    assert _section(with_summary, "ratified-provenance") == (
        "### ratified-provenance\n"
        "\n"
        "- [critical] openxFactory:docs/a.md — Ratified by: missing\n")
    assert _section(with_summary, "tag-hygiene") == (
        "### tag-hygiene\n"
        "\n"
        "No findings.\n")

    # THE ACTION LINES OF OTHER FAMILIES, ABSOLUTELY. Same argument, applied to
    # the ranked plan: every other family's row is stated in full, `action="…"`
    # included, so a render that rewrote or re-quoted an action for all families
    # fails here rather than passing a differential comparison.
    #
    # WHAT THIS CANNOT REACH, said plainly because the mutation round measured
    # it (M2): changing another family's action CONSTANT at its own construction
    # site reds nothing here and nothing anywhere else in `tests/doc-health` —
    # `promotion_fidelity._ACTION` was mutated and 85 tests stayed green. That is
    # a gap in that family's own suite, not something this file can close: the
    # only way to close it from here is to snapshot twenty-one other families'
    # action texts in F4's test file, which would red on their PRs for their own
    # legitimate edits. § 5.2's "no other family's action line changed" is
    # therefore realized as "F4's change cannot alter them", which is what the
    # assertions above prove.
    plan = with_summary[with_summary.index("## Ranked Plan"):]
    for expected in (
        '- severity=critical family=ratified-provenance repo=openxFactory '
        'path=docs/a.md rule="Ratified by: missing" '
        'action="name the approving change" class="auto-fixable"',
        '- severity=info family=release-inventory-drift repo=openxFactory '
        'path=contracts/manifest.yaml rule="inventory lags the cut" '
        'action="cut the release" class="auto-fixable"',
    ):
        assert expected in plan, expected
        assert expected in without[without.index("## Ranked Plan"):]


def test_the_block_is_not_a_finding_and_cannot_become_one(monkeypatch):
    """FR-012. The block is a rendering of findings; it must not re-enter the
    machinery that reads findings back.

    ASSERTED THROUGH `parse_previous`, WHICH IS THE ACTUAL DOOR (analyze finding
    A2). `report.parse_previous` is what a next run reads a prior report with,
    and its output feeds `previous_keys` -> `regressions()` and
    `previous_contested` -> `uncited_resolutions()`. Asserting only that
    `PLAN_RE` misses the lines proves it one inference short; asserting the two
    parses are EQUAL proves it directly. The shape is
    `test_promotion_fidelity.py::test_the_basis_lines_can_never_be_read_back_as_findings`.
    """
    from doc_health import families

    findings = _other_family_findings() + list(_fixture_findings(TREE_MARKERS))
    result = runner.RunResult(findings=list(findings))
    with_summary = _render(result)
    monkeypatch.setattr(families, "FAMILY_SUMMARIES", {})
    without = _render(result)

    assert report.parse_previous(with_summary) == report.parse_previous(without)

    section = _section(with_summary)
    block = [line for line in section.splitlines()
             if line == _LEAD or (line.startswith("- ")
                                  and not line.startswith("- ["))]
    assert len(block) == 5, block
    for line in block:
        assert report.PLAN_RE.match(line) is None, line
    plan = with_summary[with_summary.index("## Ranked Plan"):]
    for line in block:
        assert line not in plan, line

    # the headline severity counts are identical with the registry on and off
    def headline(text):
        return next(line for line in text.splitlines()
                    if line.startswith("Findings: "))
    assert headline(with_summary) == headline(without)


# ============================================================================
# 5. THE WORKFLOW BOUNDARY (§ 5.3, US3 — FR-014..FR-018)
# ============================================================================
#
# § 5.3: "NO workflow change is expected. `.github/workflows/doc-health-reusable.yml`
# passes no per-family option to this family and must not: the live-`main` basis
# belongs to `promotion-fidelity` alone, and this family measures the checkout by
# contract. Pin the boundary by a NEW test of this family's own."
#
# THE WORKFLOW FILE IS READ HERE AND EDITED NOWHERE. The mechanical proof that
# nothing edited it is `git diff --stat <merge-base> -- .github/ openspec/`,
# recorded in `specs/022-…/evidence/f4-gates.md`.
#
# CITED, NOT DUPLICATED — the three pins that already exist and that this group
# deliberately does not restate:
#
#   * `test_modified_block_currency.py::test_the_promoted_reader_cannot_reach_a_measurement_basis`
#     (F1) — the family's readers take a root and a capability, so there is no
#     parameter a basis could arrive through, and the module names no git-ref
#     reader at all.
#   * `test_modified_block_currency.py::test_the_advisory_launch_is_pinned_in_both_halves`
#     (F1) — the severities, and the deliberate absence from `FAMILY_RESOLUTION`.
#   * `test_workflow_contract.py::test_only_the_reporting_run_declares_the_live_main_basis`
#     — that the ONE per-family option the workflow carries belongs to the
#     reporting run alone. Written in `promotion-fidelity`'s shape, which is why
#     § 5.3 asks for a new assertion rather than a reuse of it.
#
# What is left for THIS family to assert is the pair those three do not touch:
# what the WORKFLOW passes, and what the CLI ACCEPTS.

_SPELLINGS = ("modified-block-currency", "modified_block_currency")
_LIVE_MAIN_FLAG = "--promotion-fidelity-basis live-main"


def _load_workflow(path: Path = WORKFLOW):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _steps(value):
    for job_name, job in (value.get("jobs") or {}).items():
        for step in job.get("steps") or []:
            yield job_name, step


def _family_mentions(value) -> list[str]:
    """Every place a parsed workflow names this family — `run`, `env` value or
    `with` value, in either spelling.

    A PROBE, NOT AN ASSERTION, so the same code can be pointed at a scratch copy
    and shown to FIND one. An "absent from" test whose probe is never
    demonstrated finding anything is the shape of assertion that lies, and this
    family's own suite has caught that three times.

    `env` and `with` are walked as well as `run` because this workflow's
    untrusted-input idiom deliberately passes values through `env:` rather than
    interpolating them into bash (`test_workflow_contract.py::test_untrusted_
    workflow_inputs_are_not_interpolated_into_bash`). A `run`-only probe would
    miss the shape the workflow actually uses to hand a value to the checker.
    """
    found = []
    for job_name, step in _steps(value):
        where = {"run": step.get("run") or ""}
        for field in ("env", "with"):
            for key, val in (step.get(field) or {}).items():
                # KEY AND VALUE BOTH. An env key is conventionally UPPER_SNAKE,
                # so `MODIFIED_BLOCK_CURRENCY_BASIS: live-main` names this family
                # in a spelling only a case-insensitive read of the KEY catches —
                # and it is one of the three shapes a per-family option can
                # arrive in (the others are the flag written straight into `run`,
                # and an env VALUE carrying the flag text for `run` to expand).
                where[f"{field}.{key}"] = f"{key} {val}"
        for label, text in where.items():
            lowered = text.lower()
            for spelling in _SPELLINGS:
                if spelling in lowered:
                    found.append(f"{job_name}/{step.get('name')}: {label}")
    return found


def test_the_workflow_parses_and_carries_the_one_per_family_option_that_exists():
    """W1 + W2 — THE NON-VACUITY CLAUSE for everything below.

    "This family is not named in the workflow" is worth nothing over a file that
    names no family at all, or that failed to parse. So: the file parses, it has
    jobs, and it carries `--promotion-fidelity-basis live-main` in exactly one
    step — the one per-family option that exists, ruled for that family alone on
    2026-08-24. The absence asserted next is measured against a real population
    of one.
    """
    value = _load_workflow()
    assert value.get("jobs"), "the workflow parsed to no jobs"
    carriers = [f"{job}/{step.get('name')}" for job, step in _steps(value)
                if _LIVE_MAIN_FLAG in (step.get("run") or "")]
    assert len(carriers) == 1, carriers


def test_the_workflow_passes_no_per_family_option_to_this_family():
    """W3 + W4 — the pin § 5.3 asks for.

    Nothing in the nightly may hand this family a basis, a scope or any other
    per-family switch. The reason is in the family's own requirement: an active
    change lives on a BRANCH, so a family reading `main` would measure a delta
    `main` does not carry against canon the branch may have moved. The
    live-`main` basis is `promotion-fidelity`'s by ruling and would be actively
    wrong here.
    """
    assert _family_mentions(_load_workflow()) == []


def test_the_probe_finds_a_per_family_option_when_one_is_present(tmp_path):
    """THE POSITIVE CONTROL, KEPT AS A TEST rather than performed once in a
    mutation round.

    A scratch copy of the workflow — never the tracked file — with
    `--modified-block-currency-basis live-main` inserted into the reporting run.
    The probe must find it, in the same shape it would find a real one. Without
    this, `test_the_workflow_passes_no_per_family_option_to_this_family` passes
    just as happily against a probe that reads the wrong field, the wrong job, or
    nothing at all.

    The `env` half is controlled too, because that is the shape this workflow
    actually uses to pass a value in and the shape a `run`-only probe would miss.
    """
    text = WORKFLOW.read_text(encoding="utf-8")
    assert _LIVE_MAIN_FLAG in text
    scratch = tmp_path / "scratch-workflow.yml"

    scratch.write_text(
        text.replace(_LIVE_MAIN_FLAG,
                     _LIVE_MAIN_FLAG + " \\\n            "
                     "--modified-block-currency-basis live-main"),
        encoding="utf-8")
    found = _family_mentions(_load_workflow(scratch))
    assert found and all("run" in f for f in found), found

    anchor = "          FAIL_ON_INPUT: ${{ inputs.fail-on }}"
    assert anchor in text
    for injected in (
            # the env KEY shape — UPPER_SNAKE, caught only case-insensitively
            "          MODIFIED_BLOCK_CURRENCY_BASIS: live-main",
            # the env VALUE shape — the flag text handed to `run` to expand
            '          EXTRA_FLAGS: "--modified-block-currency-basis live-main"',
    ):
        scratch.write_text(text.replace(anchor, anchor + "\n" + injected),
                           encoding="utf-8")
        found = _family_mentions(_load_workflow(scratch))
        assert found and any("env." in f for f in found), (injected, found)

    # and the tracked file is untouched by all of the above
    assert WORKFLOW.read_text(encoding="utf-8") == text


def test_the_checker_exposes_no_option_named_after_this_family():
    """W5 + W6 — the other half of the boundary: not only does the workflow pass
    no per-family option, there is none to pass.

    READ OFF THE OPTION STRINGS, NOT OFF THE HELP TEXT, and the distinction is
    the whole test. This family's id appears FOUR times in `--help` output — as a
    choice of `--family` and of `--skip-family`, in the usage line and in the
    option list. Those are GENERIC options that take every family's id, and a
    pin that could not tell them from a per-family option would be satisfied only
    by a family nothing can run.
    """
    proc = subprocess.run(
        [sys.executable, "scripts/doc-health.py", "--help"],
        cwd=str(REPO_ROOT), capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr[-2000:]
    help_text = proc.stdout

    options = set(re.findall(r"--[a-z][a-z0-9-]*", help_text))
    assert "--promotion-fidelity-basis" in options, (
        "the one per-family option is gone from the CLI, so the absence below "
        "is measured against nothing")
    named = sorted(opt for opt in options
                   if any(s in opt for s in _SPELLINGS))
    assert named == [], named

    # W6 — the generic options still accept this family's id, and accepting it
    # is not the same as being named after it.
    assert "--family" in options and "--skip-family" in options
    for spelling in ("modified-block-currency",):
        assert spelling in help_text, (
            "this family is not among the generic options' choices, so it "
            "cannot be run or skipped at all")
    # ACCEPTANCE PROVED BY RUNNING, not by reading the choices list — argparse
    # is where a rejected value surfaces. Pointed at F2's smallest fixture tree
    # rather than at this repository: what is under test is that the two GENERIC
    # options take this family's id, and a full single-repo run over the real
    # corpus would pay seconds per invocation to assert the same thing while
    # making the result depend on the corpus.
    scope = FIXTURES / TREE_QUIET / "quietFactory"
    for flag in ("--family", "--skip-family"):
        proc = subprocess.run(
            [sys.executable, "scripts/doc-health.py", "--single-repo",
             str(scope), flag, mbc.FAMILY, "--report-out", "/dev/null"],
            cwd=str(REPO_ROOT), capture_output=True, text=True)
        assert proc.returncode == 0, (flag, proc.stderr[-2000:])
