"""THE REPORT SECTION: what a reader of `### modified-block-currency` is told.

`add-modified-block-currency-check`, Speckit feature
`022-modified-block-currency-reporting` (packet § 5.1–5.3). F1
(`019-…-family`) built the family and its first four finding classes; F2
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
`modified_block_currency.CLASSES` is the production map over FIVE classes (the
delta names three arms and one non-arm class, "title resolution and ordering" is
ONE arm with two shapes, and `add-unclassified-finding-class` later added a
fifth non-arm class that reads the map's own verdict); and
`test_every_finding_over_the_fixture_corpus_lands_in_exactly_one_class` below
recomputes the partition independently. F2's own docstring argues for the redundancy — "an arm's wording
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

from doc_health import ERROR, INFO, WARNING, Finding, Skip
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
# F5 (`026-unplaced-finding-drift`): 1 titles + 3 ledger, ALL PLACED over the
# unmodified map. It becomes the fifth class's exercise only under an induced
# drift — see `_drifted` below.
#
# TWO CHANGE DIRECTORIES, AND THAT IS THE POINT OF THE SECOND. The arms emit by
# (capability, normalized title) — Alpha, Beta, Gamma, Zeta — while the family's
# own report order is severity, then repo, then PATH. `add-a-drift-case/` sorts
# before `add-drift-cases/`, so Zeta's ledger finding is FIRST in report order
# and THIRD in emission order. The two orders disagree, which is the only way
# "the first of that shape in report order" can be asserted at all: over a tree
# where they agree, grouping before the sort and grouping after it name the same
# finding and the pin passes either way. A mutation round proved that — the
# earlier one-directory tree let "emit before the first sort" survive.
TREE_UNPLACED = "modified-block-currency-unplaced"
# `govern-sibling-added-modified-deltas`: one tree per new class.
# `-pairing` carries every reported state of the pairing class AND both silent
# ones; `-collision` carries the unsafe archive order in both basis forms plus
# the lawful-rename negative control.
TREE_PAIRING = "modified-block-currency-pairing"
TREE_COLLISION = "modified-block-currency-collision"

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
    """SEVEN CLASSES, and the module's own docstring already says so: "THREE
    ARMS, SEVEN FINDING CLASSES, AND THE NUMBERS DIFFER ON PURPOSE". The fifth,
    `unplaced`, is `add-unclassified-finding-class`'s: not an arm, and not a
    comparison between documents — it reads this map's own verdict.

    **MOVED BY `govern-sibling-added-modified-deltas`, 2026-09-01: FIVE ->
    SEVEN, AND THE TWO NEW ROWS ARE INSERTED RATHER THAN APPENDED.**
    `sibling-pairing` and `added-over-canon` sit BEFORE `unplaced` so that BOTH
    standing ordering claims below stay true — the gate-bearing arm reads FIRST,
    and the drift class, which reads this map's verdict on everything above it,
    reads LAST. Appending them after it would have left the drift row rendering
    in the middle of the block it is about.

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
                   "title-resolution", "marker-defects",
                   "sibling-pairing", "added-over-canon", "unplaced"]
    bands = {c.id: c.band for c in mbc.CLASSES}
    assert bands == {
        "scenario-titles": mbc._LAUNCH_SEVERITY,
        "carriage-ledger": mbc._LEDGER_SEVERITY,
        "title-resolution": mbc._RESOLUTION_SEVERITY,
        "marker-defects": mbc._LEDGER_SEVERITY,
        # THEIR OWN CONSTANTS, not `_LAUNCH_SEVERITY` and not each other's, on
        # the module's own stated reason: § 7.2's flip moved `_LAUNCH_SEVERITY`
        # ALONE at `7f656980`, which is the demonstration that separately
        # assignable constants are what keep a later flip from dragging a class
        # no ruling named.
        "sibling-pairing": mbc._PAIRING_SEVERITY,
        "added-over-canon": mbc._COLLISION_SEVERITY,
        # ITS OWN CONSTANT, not `_LAUNCH_SEVERITY`. They were value-identical
        # before the § 7.2 flip (2026-08-31, issue #357), so this line alone
        # could not tell them apart pre-flip — that is what
        # `test_modified_block_currency.py::
        # test_the_realized_flip_of_the_launch_severity_did_not_drag_the_drift_class`
        # is for. This line's job is that the band is read from the MODULE and
        # never re-spelled as a literal.
        "unplaced": mbc._DRIFT_SEVERITY,
    }
    actions = {c.id: c.action for c in mbc.CLASSES}
    assert actions == {
        "scenario-titles": mbc._ACTION,
        "carriage-ledger": mbc._ACTION,
        "title-resolution": mbc._ACTION,
        "marker-defects": mbc._MARKER_ACTION,
        # A FRESH LITERAL, TYPED INDEPENDENTLY OF `mbc._DRIFT_ACTION` — the
        # same tautology `_MARKER_ACTION` had here until #448's review caught
        # it (see `_MARKER_ACTION_TEXT` below): comparing a finding's action
        # to the constant it was BUILT from passes whatever that constant had
        # been mutated to, because `mbc.CLASSES` reads `_DRIFT_ACTION` at
        # import time too — both sides move together. Issue #485.
        "unplaced": ("extend the class map in "
                     "`scripts/doc_health/modified_block_currency.py`, or "
                     "fix the drifted rule text the finding names"),
        # FRESH LITERALS, TYPED INDEPENDENTLY of `mbc._PAIRING_ACTION` and
        # `mbc._COLLISION_ACTION`, on the same rule the `unplaced` row above
        # states: comparing a class's action to the constant it was BUILT from
        # passes whatever that constant was mutated to.
        "sibling-pairing": (
            "declare the basis with ONE `Modified over` marker and no more "
            "than one, name the change carrying the block as that marker's "
            "`by` identifier, give the marker the ` — <reason>` tail its form "
            "requires, disclose in that reason clause where the basis is not "
            "ratified, and hold the archive until the declared change "
            "promotes"),
        "added-over-canon": (
            "promote nothing further until the collision is resolved, and — "
            "where the requirement genuinely already exists — convert the "
            "addition to a modification declared against canon, or withdraw "
            "or re-target the rename whose `TO:` title canon already carries"),
    }
    # every class carries a rendered label, and no two share one
    labels = [c.label for c in mbc.CLASSES]
    assert len(set(labels)) == 7, labels
    # NEITHER THE FIFTH ID NOR ITS LABEL MAY CONTAIN `unclassified`:
    # `test_a_finding_the_map_cannot_place_is_counted_and_named` asserts that
    # string's absence from a fully-classified summary, and a class label
    # renders even at a count of zero.
    assert "unclassified" not in mbc.CLASS_DRIFT
    assert "unclassified" not in dict(
        (c.id, c.label) for c in mbc.CLASSES)[mbc.CLASS_DRIFT]
    # ...and the fifth carries NO gloss, on the module's own stated rule
    assert dict((c.id, c.gloss) for c in mbc.CLASSES)[mbc.CLASS_DRIFT] == ""
    # ...and neither do the two `govern-sibling-added-modified-deltas` inserts,
    # on that same rule: the labels already say what they are, and the block's
    # whole value is being short enough to read at a glance.
    glosses = dict((c.id, c.gloss) for c in mbc.CLASSES)
    assert glosses[mbc.CLASS_PAIRING] == ""
    assert glosses[mbc.CLASS_COLLISION] == ""
    assert "unclassified" not in mbc.CLASS_PAIRING
    assert "unclassified" not in mbc.CLASS_COLLISION


def test_each_of_the_eight_rule_shapes_classifies_into_its_own_class(monkeypatch):
    """EIGHT SHAPES, SEVEN CLASSES. The delta's third arm is "Title resolution
    and ordering" — one arm, two shapes (a block resolving to nothing, and an
    ordering no declaration settles). They share a severity and an action and
    the delta names them together, so splitting them in the report would claim a
    class the delta does not define.

    RENAMED FROM `..._five_rule_shapes_...` BY `026-unplaced-finding-drift`. The
    sixth shape is the fifth class's own finding: the arms build five fixed
    prefixes and the drift emit builds a sixth. A count in a FUNCTION NAME that
    the code contradicts is the same defect the numeral sweep exists to remove
    from the prose, so the name moved with the numbers.

    **RENAMED AGAIN BY `govern-sibling-added-modified-deltas`, 2026-09-01:
    `..._six_rule_shapes_...` -> `..._eight_...`.** Two classes, two templates,
    two shapes — and the pairing class's FOUR reported states are ONE of them,
    which is the assertion the `-resolution` line below carries: they differ
    only in an interpolated clause, so a second shape among them would mean a
    state had been given fixed prose the mask cannot strip.

    Driven by fixture trees rather than by hand-written rule text: a hand-copied
    rule text in this file could drift from the arms and the test would keep
    passing on its own copy. The sixth shape is reached the only honest way, by
    inducing the drift — see the honesty note in section 6.
    """
    def classes_over(tree):
        return {mbc.classify(f) for f in _fixture_findings(tree)}

    assert classes_over(TREE_TITLES) == {"scenario-titles", "carriage-ledger"}
    assert classes_over(TREE_MARKERS) == {"marker-defects", "carriage-ledger"}
    # MOVED 2026-09-01: the `-resolution` tree's `add-pending-title` block
    # carries the corpus's oldest pending pair and no marker, so it is now the
    # UNDECLARED state rather than a silence. That is the whole change this
    # class makes to an existing fixture, and it is a change of REPORTING and
    # not of comparison — the three arms still do not run against it.
    assert classes_over(TREE_RESOLUTION) == {"title-resolution",
                                             "carriage-ledger",
                                             "sibling-pairing"}
    # MOVED 2026-09-01 for the same reason `-resolution` moved, and this tree's
    # pairing row says something the other's does not: `add-mo-modifier` DOES
    # name `add-mo-adder` in its own proposal, and it is still UNDECLARED. The
    # proposal cross-reference is a fact about two CHANGES; the marker is a fact
    # about two BLOCKS, and neither substitutes for the other.
    assert classes_over(TREE_RICH) == {"title-resolution", "carriage-ledger",
                                       "sibling-pairing"}
    # ...and the two `govern-sibling-added-modified-deltas` adds, each reached
    # from the tree written for it. The pairing tree's `carriage-ledger` row is
    # NOT incidental: it is the own-rename carve's, and it is what proves the
    # three comparison arms RAN against a rename-and-amend block under the OLD
    # name rather than that the pairing check merely stayed quiet about it.
    assert classes_over(TREE_PAIRING) == {"sibling-pairing", "carriage-ledger"}
    assert classes_over(TREE_COLLISION) == {"added-over-canon"}
    # ...and the pairing class's FOUR reported states are ONE shape: over the
    # tree that carries all four, every finding lands in that one class and
    # matches exactly one template.
    pairing = [f for f in _fixture_findings(TREE_PAIRING)
               if mbc.classify(f) == mbc.CLASS_PAIRING]
    assert {mbc._shape(f.rule) for f in pairing} == {"template:sibling-pairing"}
    assert {f.rule.split(" and the pairing is ")[1].split(":")[0]
            for f in pairing} == {"undeclared", "misdeclared",
                                  "self-referential", "undisclosed"}, (
        [f.rule[:160] for f in pairing])
    # ...and the two shapes of the third arm really are two shapes, not one
    # fixture reached twice: their rule texts differ in their opening phrase.
    opens = {f.rule.split(" for ")[0] if " for " in f.rule else f.rule
             for tree in (TREE_RESOLUTION, TREE_RICH)
             for f in _fixture_findings(tree)
             if mbc.classify(f) == "title-resolution"}
    assert opens == {"active MODIFIED block", "the ordering of MODIFIED blocks"}

    # ...and the SIXTH shape, which no corpus can supply: the fifth class's own
    # finding, reached by removing one entry from the map.
    drifted, _ = _drifted(monkeypatch, mbc.CLASS_LEDGER)
    assert {mbc.classify(f) for f in drifted} == {
        "scenario-titles", mbc.UNCLASSIFIED, mbc.CLASS_DRIFT}


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
            # ITERATE THE PATTERNS, NOT THE CLASSES. The first cut compared
            # `mbc.classify(f)` with each class id in turn, which can never
            # exceed one hit however many patterns match — so it asserted
            # "classify returns something in CLASSES", not "exactly one pattern
            # matches", and a second pattern matching the same rule was
            # invisible to it. Caught by the combined review of 2026-08-27,
            # which measured the true property: ZERO multi-matches over 37
            # findings across thirteen fixture trees and the real corpus.
            hits = [class_id for class_id, pattern in mbc._CLASS_PATTERNS
                    if pattern.match(f.rule)]
            assert len(hits) == 1, (tree, hits, f.rule[:140])
            assert mbc.classify(f) == hits[0], (tree, f.rule[:140])
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
        # the same pattern-level partition as over the fixtures, for the same
        # reason: a class-level comparison cannot see two patterns matching one
        # rule (combined review, 2026-08-27).
        hits = [class_id for class_id, pattern in mbc._CLASS_PATTERNS
                if pattern.match(f.rule)]
        assert len(hits) == 1, (hits, f.rule[:200])
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
    tree so the counts are measured rather than asserted about themselves.

    The scenario-title band FLIPPED to `error` 2026-08-31 (issue #357);
    `FindingClass.band` reads `_LAUNCH_SEVERITY` directly, so the rendered
    caption moved with it, per `_LAUNCH_SEVERITY`'s own comment. Every other
    band is unmoved (O8).

    **TWO ROWS ADDED 2026-09-01 BY `govern-sibling-added-modified-deltas`**, in
    the position the registry puts them — before the drift row, so the row that
    ENDS this block is still the one that reads this map's verdict on the rows
    above it. Both read 0 over this tree, which is the point of rendering a
    class at zero: a reader can tell a quiet corpus from a class that was never
    measured."""
    findings = _fixture_findings(TREE_MARKERS)
    lines = mbc.class_summary(findings)
    assert lines[0] == _LEAD
    assert lines[1:] == [
        "- scenario-title completeness: 0 (`error` — the arm carrying this "
        "family's gate)",
        "- carriage ledger: 3 (`info` — editorial, and the arm says so in "
        "every finding)",
        "- title resolution and ordering: 0 (`warning`)",
        "- marker defects: 1 (`info`)",
        "- sibling-pairing declaration: 0 (`warning`)",
        "- added-over-canon collision: 0 (`warning`)",
        "- unplaced-finding drift: 0 (`warning`)",
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
    # as the first of the rows. BOTH assertions moved to the fifth class when
    # `add-unclassified-finding-class` appended it LAST — the row that ends the
    # block is the row this test is about, and it is no longer `marker defects`.
    assert "- unplaced-finding drift: 0 (`warning`)" in section
    assert "- unplaced-finding drift: 0 (`warning`)\n\n- [" in section


def test_the_block_renders_on_a_run_that_found_nothing():
    """A clean run is exactly where an unstated split misleads: "No findings."
    reads as a verdict, and a reader who does not know WHICH classes were
    measured cannot tell a quiet corpus from an arm that stopped firing. All
    five counts read 0 and the block still renders — the same argument
    `test_the_report_states_the_basis_on_a_family_with_no_findings` makes for the
    basis note."""
    result = _suite(TREE_QUIET)
    assert result.findings == [] and result.skips == []
    section = _section(_render(result))
    assert _LEAD in section
    # `error` since the 2026-08-31 flip (issue #357); `warning` at launch.
    assert "- scenario-title completeness: 0 (`error`" in section
    assert "No findings." in section
    assert section.index(_LEAD) < section.index("No findings.")


def test_a_family_skipped_by_run_configuration_carries_no_block():
    """A SKIP IS THE ABSENCE OF A MEASUREMENT, and `0 · 0 · 0 · 0 · 0` beside one
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

# A FRESH LITERAL, TYPED INDEPENDENTLY OF `mbc._MARKER_ACTION` — the same
# argument `_ARMS_ACTION` makes above, applied to the family's SECOND action
# string. Comparing a finding's action to `mbc._MARKER_ACTION` itself (as
# `test_the_marker_class_keeps_its_own_action_and_not_the_arms_one` already
# did, below) is tautological: it passes whatever `_MARKER_ACTION` had been
# mutated to. A reviewer proved this on 2026-08-28 by mutating "does not
# restate" to "does not carry" in `_MARKER_ACTION` and finding the whole
# suite — this file included — stayed green. This constant is § 5.2's
# marker-class wording, spelled out here once, so the comparison below is
# against WORDS rather than against the module's own (possibly mutated) copy
# of them.
_MARKER_ACTION_TEXT = (
    "name a unit the block does not restate, or drop the "
    "declaration — a marker that does not describe the block "
    "declares nothing")


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

    def check(findings, induced=()):
        for f in findings:
            class_id = mbc.classify(f)
            # NEVER INDEX `by_id` WITH `UNCLASSIFIED`. It is deliberately not a
            # class id — that is the whole point of the residual — so an
            # induced-unplaced finding would raise `KeyError` here, and a pin
            # that CRASHES is not the assertion this pin exists to make. The
            # induced ones are asserted directly instead: the drift emit does
            # not rewrite them, so each still carries the band and action of the
            # arm that produced it.
            if class_id == mbc.UNCLASSIFIED:
                assert f in induced, f.rule[:120]
                assert f.severity in (WARNING, INFO), f.rule[:120]
                assert f.action in (mbc._ACTION, mbc._MARKER_ACTION), f.rule[:120]
                continue
            klass = by_id[class_id]
            checked[klass.id] += 1
            assert f.severity == klass.band, (klass.id, f.severity, f.rule[:120])
            assert f.action == klass.action, (klass.id, f.rule[:120])

    check([f for tree in ALL_TREES for f in _fixture_findings(tree)])
    check(list(mbc.fam_modified_block_currency(_real_ctx())))

    # THE FIFTH CLASS'S PASS, AND IT IS WHY THIS PIN IS NOT VACUOUS FOR IT.
    # `unplaced` reads 0 over every tree above and over this repository, so
    # `all(checked.values())` would fail on it — the map places everything, and
    # the tree's mere PRESENCE in `ALL_TREES` does not exercise the class. So
    # this pass induces the drift the class exists to report (one entry removed
    # from `_CLASS_PATTERNS`; see the honesty note in section 6) and drives the
    # finding through `fam_modified_block_currency`, `classify` and this same
    # comparison — a MEASURED row rather than a constructed `Finding`.
    with pytest.MonkeyPatch.context() as patch:
        drifted, induced = _drifted(patch, mbc.CLASS_LEDGER)
        assert induced, "no drift was induced, so the pass below proves nothing"
        check(drifted, induced=induced)

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
    # THE BEHAVIOURAL PIN, against the independent literal above — this is
    # the assertion the two lines above cannot be, because they compare the
    # finding to `mbc._MARKER_ACTION` rather than to typed-out words.
    assert marker_findings[0].action == _MARKER_ACTION_TEXT


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
    # MOVED 2026-09-01 by `govern-sibling-added-modified-deltas`: the lead plus
    # SEVEN class rows, the two new classes rendering at zero like every other.
    assert len(block) == 8, block          # the lead plus seven class rows
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


def _scopes(value):
    """EVERY SCOPE A WORKFLOW CAN SET `env` OR `with` IN, not only the steps.

    ADDED BY THE COMBINED REVIEW OF 2026-08-27, which proved the first cut
    green against a job-level `env` (mutant M5b). GitHub Actions resolves `env`
    at three levels — workflow, job, step — and a variable set at ANY of them is
    visible to every `run` beneath it. Both jobs in this workflow ALREADY carry a
    job-level `env` block (`HAS_APP_KEY`, `HAS_ANTHROPIC_KEY`), so the shape the
    step-only probe missed is not hypothetical: it is one line away from an
    existing block.

    `with` is walked at job level too, for a job that calls a reusable workflow
    (`jobs.<id>.uses`) and passes inputs down.
    """
    yield "workflow", "env", value.get("env") or {}
    for job_name, job in (value.get("jobs") or {}).items():
        for field in ("env", "with"):
            yield f"job {job_name}", field, job.get(field) or {}
    for job_name, step in _steps(value):
        for field in ("env", "with"):
            yield (f"{job_name}/{step.get('name')}", field,
                   step.get(field) or {})


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

    AND THEY ARE WALKED AT ALL THREE LEVELS — workflow, job, step (`_scopes`).
    The first cut walked steps only and the combined review killed it with a
    JOB-level `env` (M5b): Actions resolves `env` down the tree, so a variable
    set on the job is visible to every `run` in it, and both jobs here already
    carry a job-level `env` block. A probe that reads one of three scopes is a
    probe with two blind spots.

    KEY AND VALUE BOTH, CASE-INSENSITIVELY. An env key is conventionally
    UPPER_SNAKE, so `MODIFIED_BLOCK_CURRENCY_BASIS: live-main` names this family
    in a spelling only a case-insensitive read of the KEY catches. With `run`
    that makes FOUR shapes a per-family option can arrive in: the flag written
    straight into `run`; an env/with key named for the family; an env/with value
    carrying the flag text for `run` to expand; and any of the last three set at
    a scope above the step.
    """
    found = []
    for job_name, step in _steps(value):
        text = (step.get("run") or "").lower()
        if any(spelling in text for spelling in _SPELLINGS):
            found.append(f"{job_name}/{step.get('name')}: run")
    for where, field, mapping in _scopes(value):
        for key, val in mapping.items():
            lowered = f"{key} {val}".lower()
            for spelling in _SPELLINGS:
                if spelling in lowered:
                    found.append(f"{where}: {field}.{key}")
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
    # `any`, not `all`: each injection asserts that ITS shape is found, never
    # that no other shape is. `all` was the first spelling and it fails for the
    # wrong reason the moment the base file carries a mention of another shape —
    # which is exactly the state the M5b mutation puts it in.
    assert found and any(f.endswith(": run") for f in found), found

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

    # THE JOB-LEVEL AND WORKFLOW-LEVEL SHAPES (mutant M5b, added by the combined
    # review, which proved the step-only probe green against the first of them).
    # Both jobs already carry a job-level `env:` block, so this is one line from
    # an existing one — and `env` resolves DOWN, so a job-level variable reaches
    # every `run` in the job.
    job_anchor = "    env:\n      HAS_APP_KEY:"
    assert job_anchor in text, "the job-level env block this mutant needs is gone"
    scratch.write_text(
        text.replace(job_anchor,
                     "    env:\n      MODIFIED_BLOCK_CURRENCY_BASIS: live-main\n"
                     "      HAS_APP_KEY:", 1),
        encoding="utf-8")
    found = _family_mentions(_load_workflow(scratch))
    assert found and any(f.startswith("job ") for f in found), found

    scratch.write_text(
        "env:\n  MODIFIED_BLOCK_CURRENCY_BASIS: live-main\n" + text,
        encoding="utf-8")
    found = _family_mentions(_load_workflow(scratch))
    assert found and any(f.startswith("workflow:") for f in found), found

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


# ============================================================================
# 6. THE FIFTH CLASS — unplaced-finding drift
#    (`add-unclassified-finding-class`, Speckit feature
#     `026-unplaced-finding-drift`; delta scenarios 1–6)
# ============================================================================
#
# WHAT THE DELTA ADDS. The family already detects that its own class map has
# drifted — `classify` is fail-closed and `class_summary` renders a named
# residual row — and then tells nobody who can act on it: the row is prose, so
# it has no severity, no `--fail-on` reach and no ranked-plan reach. The fifth
# class makes a nonzero residual emit ONE `warning` per DISTINCT unplaced rule
# SHAPE per run, and places that warning by the map so it is never counted by
# the residual it reports.
#
# ####################################################################
# THE LIVE-TRIGGER HONESTY NOTE, AND IT APPLIES TO EVERY TEST BELOW.
#
# NO CRAFTED FIXTURE TITLE CAN EXERCISE THIS CLASS. Every rule text this family
# constructs is one of FIVE fixed prefixes plus `{title!r}`, and `_TITLE_REPR`
# admits both `repr` quotings and the `\\.` escape, so no corpus-supplied title
# can fall outside the map. Fuzzed at packet review (`add-unclassified-finding-class`
# tasks.md § 3.5): 13 adversarial titles (empty, both quote kinds together,
# trailing backslash, tab, `\x7f`, and titles that themselves read
# `omits 1 of the 2 scenarios` and `carries a 'removed' marker by`) plus 4000
# random titles over an alphabet of quotes, backslashes, control characters and
# class phrases, times the five rule shapes = **20,065 rule texts, 0
# unplaceable**.
#
# SO THE TRIGGER IS THE DRIFT ITSELF. `_drifted` removes ONE entry from
# `_CLASS_PATTERNS`, which is precisely the live condition the class exists to
# report — "the map has drifted behind the arms". The family, the classifier,
# the summary and the renderer all run UNMODIFIED underneath it. The seam is a
# recorded decision of `026-unplaced-finding-drift` (plan § O2), reversible, and
# a one-test change if a reviewer prefers a different one.
# ####################################################################


def _drifted(monkeypatch, *dropped, tree=TREE_UNPLACED):
    """The family's findings over `tree` with `dropped` classes removed from the
    class map — the map having drifted behind the arms by exactly that much.

    Returns `(findings, unplaced)`: everything the family emitted, and the
    subset the map no longer places. See the honesty note above.
    """
    monkeypatch.setattr(mbc, "_CLASS_PATTERNS", tuple(
        entry for entry in mbc._CLASS_PATTERNS if entry[0] not in dropped))
    findings = _fixture_findings(tree)
    unplaced = [f for f in findings if mbc.classify(f) == mbc.UNCLASSIFIED]
    return findings, unplaced


def _drift_findings(findings):
    """The findings the FIFTH class places, read off the class map rather than
    off a hand-copied rule text."""
    return [f for f in findings if mbc.classify(f) == mbc.CLASS_DRIFT]


def test_a_run_the_map_places_entirely_emits_no_additional_finding():
    """DELTA SCENARIO 1 — the state this requirement exists to LEAVE ALONE.

    The map and the arms agreeing is the normal state and the state of this
    repository, so the expensive half of this feature is the half that must do
    nothing. Over every fixture tree AND the real tree: no drift finding, and
    the counts still sum to the findings they were handed.

    POSITIVE CONTROL FIRST. "No finding is in the fifth class" is vacuously true
    of a registry that has no fifth class, which is exactly how an "absent from"
    assertion lies (F1's mutation round, three times over).
    """
    assert mbc.CLASS_DRIFT in {klass.id for klass in mbc.CLASSES}, (
        "there is no fifth class, so the absence below would be vacuous")

    def counts_in(lines):
        return sum(int(m.group(1)) for line in lines
                   for m in [re.search(r": (\d+) \(`", line)] if m)

    for tree in ALL_TREES:
        findings = _fixture_findings(tree)
        assert _drift_findings(findings) == [], tree
        assert counts_in(mbc.class_summary(findings)) == len(findings), tree

    real = list(mbc.fam_modified_block_currency(_real_ctx()))
    assert _drift_findings(real) == []
    assert counts_in(mbc.class_summary(real)) == len(real)


def test_a_rule_text_the_map_does_not_place_emits_one_warning_naming_it(
        monkeypatch):
    """DELTA SCENARIO 2 — the emit, measured through the family rather than
    constructed.

    One `warning` for the shape, naming HOW MANY of the run's findings carry it
    and quoting, VERBATIM, the rule text of the FIRST of them in the family's
    own report order, and carrying that first finding's repository and delta
    path. See the honesty note above for why the drift is induced.
    """
    findings, unplaced = _drifted(monkeypatch, mbc.CLASS_LEDGER)
    assert len(unplaced) == 3, [f.rule[:80] for f in unplaced]

    drift = _drift_findings(findings)
    assert len(drift) == 1, [f.rule[:120] for f in drift]
    one = drift[0]

    assert one.severity == mbc._DRIFT_SEVERITY == WARNING
    assert one.family == mbc.FAMILY
    assert one.action == mbc._DRIFT_ACTION
    # the count of that shape, stated
    assert "3 findings" in one.rule, one.rule[:200]
    # VERBATIM, and that word is load-bearing: a `repr`-wrapped quotation would
    # escape the rule's own quotes and this suffix comparison would be false.
    assert one.rule.endswith(unplaced[0].rule), one.rule[-200:]
    # ...carrying the FIRST instance's repo and delta path
    assert (one.repo, one.path) == (unplaced[0].repo, unplaced[0].path)


def test_the_drift_warning_is_worked_from_the_ranked_plan(monkeypatch):
    """DELTA SCENARIO 5 — the whole point. The residual row could never become
    work; this finding is work.

    Rendered, not asserted about a `Finding` object: the ranked plan is what a
    session reads, and a field nothing prints is not a work item. The residual
    row MUST still render in the family's own block beside it — the two are two
    readings of one fact rather than alternatives.
    """
    monkeypatch.setattr(mbc, "_CLASS_PATTERNS", tuple(
        entry for entry in mbc._CLASS_PATTERNS
        if entry[0] != mbc.CLASS_LEDGER))
    text = _render(_suite(TREE_UNPLACED))

    plan = text[text.index("## Ranked Plan"):]
    rows = [line for line in plan.splitlines()
            if f"family={mbc.FAMILY}" in line
            and f'action="{mbc._DRIFT_ACTION}"' in line]
    assert len(rows) == 1, plan
    assert "severity=warning" in rows[0]
    assert "repo=driftFactory" in rows[0]
    # the FIRST of the shape in report order, which is the other change dir
    assert "path=openspec/changes/add-a-drift-case/" in rows[0]

    section = _section(text)
    assert "- unplaced-finding drift: 1 (`warning`)" in section
    # ...and the residual row is NOT replaced by the finding
    assert "- unclassified: 3 —" in section


def test_the_drift_finding_is_placed_by_the_map_and_never_by_the_residual(
        monkeypatch):
    """DELTA SCENARIO 2's third clause, and decision D2's whole argument.

    A drift finding the map could not place would be counted by the residual it
    reports: the count would name itself, the next run would report a drift the
    map had just been extended to describe, and the tally still would not sum.
    Rejected as incoherent in the packet; asserted here as behaviour.
    """
    findings, unplaced = _drifted(monkeypatch, mbc.CLASS_LEDGER)
    drift = _drift_findings(findings)
    assert len(drift) == 1

    assert mbc.classify(drift[0]) == mbc.CLASS_DRIFT
    assert mbc.classify(drift[0]) != mbc.UNCLASSIFIED
    assert drift[0] not in unplaced

    counts = mbc.class_counts(findings)
    assert counts[mbc.CLASS_DRIFT] == 1
    assert counts[mbc.UNCLASSIFIED] == 3      # the ARMS' unplaced findings only
    assert sum(counts.values()) == len(findings)

    # and the rendered lines say the same thing, which is what a reader has
    lines = mbc.class_summary(findings)
    assert "- unplaced-finding drift: 1 (`warning`)" in lines
    assert any(line.startswith("- unclassified: 3 —") for line in lines), lines


def test_a_drift_finding_quoting_an_arm_shaped_rule_text_is_not_misfiled(
        monkeypatch):
    """DELTA SCENARIO 4 — WHY THE MAP IS ANCHORED, from the new class's side.

    This finding QUOTES an unrecognized rule text, and that quotation may itself
    begin in the shape of an arm's. Here it does: the scenario-titles pattern is
    the one removed, so the quoted text opens
    `active MODIFIED block for '…' omits 1 of the 2 scenarios …`. An unanchored
    or substring probe files the drift finding under `scenario-titles` — a
    `warning` counted under the gate-bearing arm, on the one line § 5.1 exists
    so a reader can trust without counting.
    """
    findings, unplaced = _drifted(monkeypatch, mbc.CLASS_TITLES)
    assert len(unplaced) == 1
    assert unplaced[0].rule.startswith("active MODIFIED block for ")
    assert "omits 1 of the 2 scenarios" in unplaced[0].rule

    drift = _drift_findings(findings)
    assert len(drift) == 1
    assert mbc.classify(drift[0]) == mbc.CLASS_DRIFT
    assert mbc.classify(drift[0]) != mbc.CLASS_TITLES

    # THE POSITIVE CONTROL, in F4's own idiom: the unanchored reading really
    # would have matched, so the anchor is load-bearing rather than defensive.
    assert re.search(r"omits \d+ of the \d+ scenarios ", drift[0].rule)

    # ...and the finding it names is STILL counted by the residual: the two are
    # counted apart.
    counts = mbc.class_counts(findings)
    assert counts[mbc.UNCLASSIFIED] == 1
    assert counts[mbc.CLASS_DRIFT] == 1


def test_a_title_that_embeds_the_drift_phrase_still_matches_exactly_one_pattern():
    """WHY THE FIFTH PATTERN IS ANCHORED, from the ARMS' side — and this is the
    half a reader is likeliest to think is decoration, because `classify` calls
    `re.match`, which already anchors at position 0.

    It is not decoration. Requirement titles come from the corpus, so a
    requirement may be TITLED with this class's own opening phrase. Its ledger
    finding's rule text then CONTAINS that phrase, and a pattern written as a
    substring probe (`.*`-prefixed, which `re.match` happily accepts) matches it
    as well as the ledger pattern does. Two hits reds
    `test_every_finding_over_the_fixture_corpus_lands_in_exactly_one_class`,
    which counts PATTERN matches rather than `classify`'s single return — the
    stronger property the combined review of 2026-08-27 installed for exactly
    this shape of defect.

    Constructed, because the corpus has no such title today, which is exactly
    when a rule is worth pinning (F4's own argument for its evil-title test).
    """
    assert mbc.CLASS_DRIFT in {class_id for class_id, _ in mbc._CLASS_PATTERNS}, (
        "the fifth pattern is not in the map, so the assertion below is vacuous")

    # THE TITLE MUST CARRY THE WHOLE PREFIX, and the mutation round is what
    # taught this file so. The first cut stopped at `… for 2 findings`, which
    # the pattern does not reach — it also requires `this run emitted, ` — so
    # the unanchored mutant matched nothing and SURVIVED. A near-miss adversary
    # is not an adversary.
    evil_title = ("this family's own class map has no pattern for 2 findings "
                  "this run emitted, and somebody should extend it")
    ledger = Finding(
        INFO, mbc.FAMILY, "openxFactory", "openspec/changes/c/specs/a/spec.md",
        f"active MODIFIED block for {evil_title!r} does not carry 1 of the 3 "
        f"body units and scenario bullets openspec/specs/a/spec.md currently "
        f"states for it — a divergence this arm CANNOT distinguish from a "
        f"deliberate rewording, and does not claim to: [body] 'z'",
        mbc._ACTION)

    hits = [class_id for class_id, pattern in mbc._CLASS_PATTERNS
            if pattern.match(ledger.rule)]
    assert hits == [mbc.CLASS_LEDGER], hits
    assert mbc.classify(ledger) == mbc.CLASS_LEDGER


def test_two_unplaced_findings_of_one_shape_are_one_remedy(monkeypatch):
    """DELTA SCENARIO 3, FIRST HALF — one drifted rule SHAPE is one remedy.

    The two ledger findings of this tree differ only in a quoted requirement
    title and a quoted body unit; every digit run is identical too. Masked, they
    are one shape, so they are ONE map entry to write and ONE finding to report.
    """
    findings, unplaced = _drifted(monkeypatch, mbc.CLASS_LEDGER)
    assert len(unplaced) == 3
    assert len({f.rule for f in unplaced}) == 3      # genuinely three findings
    assert len({mbc._shape(f.rule) for f in unplaced}) == 1

    drift = _drift_findings(findings)
    assert len(drift) == 1, [f.rule[:120] for f in drift]
    assert "3 findings" in drift[0].rule


def test_two_unplaced_shapes_are_two_remedies(monkeypatch):
    """DELTA SCENARIO 3, SECOND HALF — two SHAPES are two findings.

    Collapsing them would quote only one of the two drifted texts, which is the
    half of the delta this scenario protects.

    NOT "TWO REMEDIES", AND THE DIFFERENCE IS MEASURED. The grain is one finding
    per distinct arm text after masking, which is FINER than one per remedy —
    see `test_the_drift_grain_is_one_finding_per_masked_arm_text_not_one_per_remedy`
    for the real-tree figure and for why widening it is a delta amendment rather
    than a fix.
    """
    findings, unplaced = _drifted(monkeypatch, mbc.CLASS_LEDGER, mbc.CLASS_TITLES)
    assert len(unplaced) == 4

    shapes = {mbc._shape(f.rule) for f in unplaced}
    assert len(shapes) == 2, shapes

    drift = _drift_findings(findings)
    assert len(drift) == 2, [f.rule[:120] for f in drift]
    assert sorted("3 findings" in f.rule for f in drift) == [False, True]
    assert any("1 finding this run emitted" in f.rule for f in drift), (
        "the singular is not spelled, so a one-finding shape reads wrongly")


def test_the_drift_finding_names_the_first_instance_in_report_order_and_is_deterministic(
        monkeypatch):
    """"FIRST" IS IN THE FAMILY'S OWN REPORT ORDER, which is what makes the emit
    deterministic: sort, group, append, sort again.

    Both halves matter. Naming an arbitrary member of the shape would make the
    finding's identity churn between runs over an unchanged tree; and because
    the family's own sort is severity-then-repo-then-path-then-rule, "first" is
    a property of the report a reader can check by eye.
    """
    findings, unplaced = _drifted(monkeypatch, mbc.CLASS_LEDGER, mbc.CLASS_TITLES)
    drift = _drift_findings(findings)
    assert len(drift) == 2

    for one in drift:
        named = next(f for f in unplaced if one.rule.endswith(f.rule))
        same_shape = [f for f in unplaced
                      if mbc._shape(f.rule) == mbc._shape(named.rule)]
        # RE-SORTED HERE, not read off the family's output order, so this
        # compares against the RULE rather than against the implementation.
        assert named is min(same_shape, key=mbc._report_order), (
            named.rule[:120], min(same_shape, key=mbc._report_order).rule[:120])
        assert (one.repo, one.path) == (named.repo, named.path)

    # THE PIN ONLY BITES ON A TREE WHOSE TWO ORDERS DISAGREE, so the tree is
    # asserted to be such a tree. The arms EMIT by normalized requirement title
    # — Alpha, Beta, Gamma, Zeta — and report order sorts by PATH within a
    # severity, where `add-a-drift-case/` precedes `add-drift-cases/`. So the
    # ledger shape's report-order-first is ZETA and its emission-order-first is
    # ALPHA. Without this, grouping before the sort and grouping after it name
    # the same finding and the assertion above passes over a mutant. Measured:
    # the mutation round's "emit before the first sort" SURVIVED the earlier
    # single-directory tree.
    ledger_shape = [f for f in unplaced if "does not carry" in f.rule]
    assert len(ledger_shape) == 3
    first_by_report = min(ledger_shape, key=mbc._report_order)
    first_by_title = min(ledger_shape, key=lambda f: f.rule)
    assert "add-a-drift-case" in first_by_report.path
    assert "'Zeta boundary is declared'" in first_by_report.rule
    assert "'Alpha boundary is declared'" in first_by_title.rule
    assert first_by_report is not first_by_title, (
        "the two orders agree on this tree, so the assertion above cannot fail "
        "on a build that groups before it sorts")

    again = _fixture_findings(TREE_UNPLACED)
    assert [f.__dict__ for f in again] == [f.__dict__ for f in findings]


def test_extending_the_map_removes_both_the_finding_and_the_residual_row(
        monkeypatch):
    """DELTA SCENARIO 6 — the remedy works, and its success is not itself
    reported as a defect.

    This finding is DESIGNED to stop being emitted the moment somebody extends
    the map. `report.uncited_resolutions` turns a `contested` finding that
    VANISHES between reports into an `error` — through the advisory launch
    the family's deliberate absence from `FAMILY_RESOLUTION` is what prevented
    that. FLIPPED 2026-08-31 (issue #357): the family is CONTESTED now, this
    fixture's remedy included, so the drift finding vanishing here would owe a
    citation the same way every other class's does — the discipline the
    flip's second half exists to buy, asserted rather than assumed.
    """
    from doc_health import CONTESTED
    from doc_health.families import FAMILIES, FAMILY_RESOLUTION

    drifted, unplaced = _drifted(monkeypatch, mbc.CLASS_LEDGER)
    assert len(_drift_findings(drifted)) == 1
    assert unplaced

    monkeypatch.undo()                     # the map is extended to place them
    restored = _fixture_findings(TREE_UNPLACED)
    assert _drift_findings(restored) == []
    assert [f for f in restored if mbc.classify(f) == mbc.UNCLASSIFIED] == []
    assert not any("unclassified" in line
                   for line in mbc.class_summary(restored))

    assert mbc.FAMILY in FAMILIES, "the membership below means nothing otherwise"
    assert FAMILY_RESOLUTION.get(mbc.FAMILY) == CONTESTED


def test_the_new_fixture_tree_declares_its_provenance_and_the_other_classes_stay_advisory():
    """F2's convention, checked for a tree F2's own checker cannot reach.

    `test_every_fixture_tree_this_feature_adds_carries_a_provenance_note`
    iterates `NEW_TREES` and additionally requires each README to cite an F2
    AUDIT ROW and an `add-modified-block-currency-check § 3.x` section. This
    tree belongs to `026-unplaced-finding-drift` and to neither of those, so
    joining `NEW_TREES` would mean fabricating an audit-row citation to satisfy
    a checker — the false-documentation defect this whole family exists to
    catch. The convention is kept and pinned HERE instead (plan § O5).

    The band sweep rides along for the same reason: F2's
    `test_no_new_tree_reports_an_unexpected_error_or_a_critical_finding` also
    iterates `NEW_TREES`, so nothing else asserts about this tree's bands.

    THIS TREE CARRIES 1 titles + 3 ledger, so it is exactly where the flip
    (2026-08-31, issue #357) changes what "stays advisory" means: the ONE
    scenario-title finding is `error` now, by design — that arm is
    gate-bearing. What still "stays advisory" is everything else, checked
    apart from it the same way `test_no_new_tree_reports_an_unexpected_error_
    or_a_critical_finding` splits `NEW_TREES`.
    """
    note = FIXTURES / TREE_UNPLACED / "README.md"
    assert note.is_file()
    lines = note.read_text().splitlines()
    assert len(lines) >= 3
    assert re.search(r"\bSYNTHESIZED\b", lines[2]), lines[2]
    assert not re.search(r"\b[0-9a-f]{40}\b", lines[2]), lines[2]
    assert "add-unclassified-finding-class" in note.read_text()

    findings = _fixture_findings(TREE_UNPLACED)
    assert findings, "a vacuous pass is not a pass"
    titles = [f for f in findings if mbc.classify(f) == mbc.CLASS_TITLES]
    others = [f for f in findings if f not in titles]
    assert {f.severity for f in titles} == {ERROR}
    assert {f.severity for f in others} <= {WARNING, INFO}


# ============================================================================
# 6b. THE GRAIN, MEASURED — and it is FINER than "one finding per remedy"
# ============================================================================

def _independently_masked(rule):
    """A SECOND implementation of the repr-span mask, written here on purpose.

    `mbc._mask_repr_spans` is part of the subject below, so using it would
    compare the implementation with itself. This is the same rule read afresh: a
    quote opens a span only where a `repr` could have emitted one — at the start
    of the text, or after a non-alphanumeric — so the apostrophe inside
    `sibling's` is prose and never an opener.
    """
    out, index = [], 0
    while index < len(rule):
        char = rule[index]
        if char in "'\"" and (index == 0 or not rule[index - 1].isalnum()):
            span = re.compile(mbc._TITLE_REPR).match(rule, index)
            if span:
                out.append("\x01")
                index = span.end()
                continue
        out.append(char)
        index += 1
    return "".join(out)


# One DISCRIMINATING PHRASE per arm template, typed out here rather than read
# off `mbc._ARM_TEMPLATES`. That is what makes the grouping below an INDEPENDENT
# recomputation: the module's registry could be wrong in exactly the way this
# test exists to catch, and a test that asked the registry which template a rule
# came from would agree with it either way. Each phrase is a fragment of ONE
# template's fixed prose and of no other's — the same discipline F2's
# `CLASSIFIERS` are written under.
_TEMPLATE_PROBES = {
    "titles": " omits ",
    "ledger": " does not carry ",
    "markers": " marker by ",
    "unresolved": " resolves to no promoted requirement, ",
    "ordering": "the ordering of MODIFIED blocks for ",
    "drift": "this family's own class map has no pattern for ",
    # THE TWO `govern-sibling-added-modified-deltas` ADDS. The pairing probe is
    # deliberately the WHOLE clause and not "sibling's addition": that shorter
    # fragment appears in `TEMPLATE_UNRESOLVED`'s fixed prose too ("no active
    # sibling's addition:"), so it would match two templates and this
    # independent reading would assert against itself rather than against the
    # module.
    "pairing": " rests on an active sibling's addition rather than on canon, ",
    "collision": " writes a requirement title ",
}


def _independent_template_of(rule):
    """Which arm template a rule came from, decided without asking the module."""
    masked = _independently_masked(rule)
    hits = [name for name, probe in _TEMPLATE_PROBES.items() if probe in masked]
    assert len(hits) == 1, (hits, masked[:160])
    return hits[0]


def test_the_drift_grain_is_one_finding_per_arm_template():
    """THE GRAIN, MEASURED ON THE REAL TREE — and it is ONE PER REMEDY.

    **AMENDED 2026-08-28 ON BRETT'S RULING**, verbatim: "Amend: shape = arm
    template, all interpolations masked". Two rule texts are ONE SHAPE where
    they come from the SAME TEMPLATE, whatever their interpolated values. One
    shape is one template, one template is one map entry somebody has to write,
    so the count of drift findings is the count of REMEDIES.

    **THIS TEST IS THE FIGURE THAT MOVED.** Under the rule as first ratified —
    quoted spans and digit runs masked, and nothing else — every UNQUOTED
    interpolation was shape-bearing, so dropping ONE class pattern on this
    repository emitted **SIX** findings for SEVEN unplaced ones where one map
    entry would have placed all seven. Re-measured under the amendment, at the
    same drop on the same tree:

    | tree | pattern dropped | unplaced | shapes — was | now |
    |---|---|---|---|---|
    | this repository | `carriage-ledger` | 7 | 6 | **1** |
    | `-two-writers` | `title-resolution` | 9 | 4 | **1** |
    | `-markers` | `carriage-ledger` | 3 | 3 | **1** |
    | `-unplaced` | `carriage-ledger` | 3 | 1 | **1** |

    THE COLLAPSE IS ASSERTED AS A REAL ONE, not a vacuous one. The seven
    findings are first shown to be seven DIFFERENT texts differing in more than
    their quoted spans — they name several promoted specs — and only then
    required to be one shape. Without that, a mask that returned a constant
    would pass.
    """
    # EVERYTHING INSIDE THE DRIFTED MAP. `classify` reads `_CLASS_PATTERNS`, so
    # a measurement taken after the patch is undone reads zero unplaced findings
    # and passes on nothing — which this test did, once, before the guard below
    # caught it.
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(mbc, "_CLASS_PATTERNS", tuple(
            entry for entry in mbc._CLASS_PATTERNS
            if entry[0] != mbc.CLASS_LEDGER))
        findings = list(mbc.fam_modified_block_currency(_real_ctx()))
        unplaced = [f for f in findings
                    if mbc.classify(f) == mbc.UNCLASSIFIED]
        drift = _drift_findings(findings)

    assert len(unplaced) >= 2, (
        "fewer than two findings were unplaced, so the collapse below is "
        "vacuous — check the resolver before the mask")

    # they really are different findings, differing OUTSIDE their quoted spans
    assert len({f.rule for f in unplaced}) == len(unplaced)
    specs = {re.search(r"(openspec/specs/[\w./-]+)", f.rule).group(1)
             for f in unplaced}
    assert len(specs) >= 2, (
        f"every unplaced finding named the same promoted spec ({specs}), so the "
        f"collapse below would hold under the OLD rule too and this test no "
        f"longer measures the amendment")

    # ...and they are nonetheless ONE template, hence ONE remedy, hence ONE finding
    assert len({_independent_template_of(f.rule) for f in unplaced}) == 1
    assert len({mbc._shape(f.rule) for f in unplaced}) == 1
    assert len(drift) == 1, [f.rule[:120] for f in drift]


def test_every_finding_matches_exactly_one_arm_template():
    """THE PROPERTY THE MASK RESTS ON, over every tree and the real corpus.

    `_shape` matches templates FIRST MATCH WINS, so two templates claiming one
    rule would merge two remedies into one silently. Asserted at the TEMPLATE
    level rather than through `_shape`'s single return, for the same reason
    `test_every_finding_over_the_fixture_corpus_lands_in_exactly_one_class`
    counts pattern matches rather than `classify`'s: a class-level comparison
    can never exceed one hit however many templates match.

    AND THE MASKING ORDER IS WHY IT HOLDS. Requirement titles and quoted body
    units come from the corpus and may contain any phrase, including another
    arm's fixed prose — the same hazard `_BLOCK_HEAD` was measured into
    existence for. Matching templates against RAW text could file one arm's
    finding under another's; masked first, the only text left is the module's
    own prose.
    """
    findings = [f for tree in ALL_TREES for f in _fixture_findings(tree)]
    findings += list(mbc.fam_modified_block_currency(_real_ctx()))
    assert len(findings) >= 25, len(findings)

    for f in findings:
        masked = mbc._mask_repr_spans(f.rule)
        hits = [t.id for t in mbc._ARM_TEMPLATES if t.matches(masked)]
        assert len(hits) == 1, (hits, f.rule[:140])
        assert mbc._shape(f.rule) == hits[0], f.rule[:140]
        # ...and the independent reading agrees, so neither is checking itself
        assert hits[0].endswith(
            {"titles": "scenario-titles", "ledger": "carriage-ledger",
             "markers": "marker-defects", "unresolved": "title-resolution",
             "ordering": "ordering", "drift": "unplaced-drift",
             # MOVED BY `govern-sibling-added-modified-deltas`: two more
             # templates, two more rows, and the property is unchanged.
             "pairing": "sibling-pairing", "collision": "added-over-canon"}[
                 _independent_template_of(f.rule)]), f.rule[:140]

    # every registered template exercised at least once, or the sweep above
    # proves nothing about the ones it never met
    seen = {mbc._shape(f.rule) for f in findings}
    unseen = {t.id for t in mbc._ARM_TEMPLATES} - seen
    assert unseen == {"template:unplaced-drift"}, (
        f"expected only the drift template to be unexercised over a corpus "
        f"whose map places everything; unexercised: {sorted(unseen)}")

    # THE SIXTH TEMPLATE, REACHED — and this assertion is also what keeps
    # `_ArmTemplate.matches` ANCHORED. Its pattern carries `\Z` but no `^`: it
    # relies on `re.match`, so switching that one call to `re.search` finds the
    # ledger template's segments INSIDE the drift finding's quotation and files
    # a drift finding under `carriage-ledger` — the ledger template being
    # earlier in the registry. Nothing else in this suite can see that, because
    # the SHIPPING path never shapes a drift finding at all: `_drift_findings`
    # makes one pass over the arms' findings and its own output is never fed
    # back in. The registry entry is defensive, and this is the test that stops
    # it from being defensive AND untested.
    quoting_a_ledger = mbc.TEMPLATE_DRIFT.render(
        n=1, s="", rule=mbc.TEMPLATE_LEDGER.render(
            title="A requirement", missing=1, total=3,
            spec_rel="openspec/specs/alpha/spec.md", listed="[body] 'z'"))
    assert mbc._shape(quoting_a_ledger) == "template:unplaced-drift", (
        mbc._shape(quoting_a_ledger))


def test_a_title_that_embeds_another_arm_s_template_prose_matches_one_template():
    """WHY `_shape` MASKS BEFORE IT MATCHES, and this is the pin that makes the
    order load-bearing rather than merely sensible.

    Requirement titles come from the CORPUS, so a title may contain any text —
    including another arm's whole fixed prose. Here a SCENARIO-TITLES finding is
    built for a requirement titled with the carriage-ledger template's prose. On
    the RAW rule text both templates match: the ledger template's fixed segments
    all appear, in order, inside the quoted title. Two templates on one rule
    means two remedies collapsed into one, or one split into two, depending on
    which wins — the same misfiling `_BLOCK_HEAD` was measured into existence to
    prevent, one layer up.

    Masked first, the title is a single placeholder and only its own template
    matches. Added by the mutation round: the mutant that matches templates
    against raw text SURVIVED everything else, because no corpus title carries
    another arm's prose today — which is exactly when a rule is worth pinning.
    """
    # THE LEDGER FINDING IS THE ONE TO BUILD, not the titles finding, and the
    # direction is what makes this falsifiable. `_ARM_TEMPLATES` is ordered and
    # first match wins, with `scenario-titles` FIRST — so an unmasked ledger
    # finding whose title embeds the TITLES prose resolves to the wrong
    # template, while an unmasked titles finding whose title embeds the LEDGER
    # prose still resolves to titles by luck of the ordering and proves nothing.
    evil_title = mbc.TEMPLATE_TITLES.render(
        title="Inner", missing=1, total=2,
        spec_rel="openspec/specs/inner/spec.md", named="'S'")
    ledger = Finding(
        INFO, mbc.FAMILY, "openxFactory", "openspec/changes/c/specs/a/spec.md",
        mbc.TEMPLATE_LEDGER.render(
            title=evil_title, missing=1, total=3,
            spec_rel="openspec/specs/a/spec.md", listed="[body] 'z'"),
        mbc._ACTION)

    # THE POSITIVE CONTROL FIRST: raw, this really is ambiguous, so the masking
    # step below is load-bearing rather than defensive.
    raw_hits = [t.id for t in mbc._ARM_TEMPLATES if t.matches(ledger.rule)]
    assert set(raw_hits) == {"template:scenario-titles",
                             "template:carriage-ledger"}, raw_hits
    assert raw_hits[0] == "template:scenario-titles", (
        "the ordering no longer puts the wrong template first, so this test "
        "would pass over an unmasked build and stops being a pin")

    # ...and masked, exactly one claims it, and it is the arm that emitted it.
    masked_hits = [t.id for t in mbc._ARM_TEMPLATES
                   if t.matches(mbc._mask_repr_spans(ledger.rule))]
    assert masked_hits == ["template:carriage-ledger"], masked_hits
    assert mbc._shape(ledger.rule) == "template:carriage-ledger"


def test_the_arm_templates_are_the_only_place_the_prose_lives():
    """NO ARM MAY BUILD A RULE TEXT ANY OTHER WAY.

    The mask is derived from the templates, so an arm that spelled its prose
    inline again would emit findings no template claims — and they would fall to
    the fail-closed lexical fallback and split into as many shapes as they have
    distinct interpolations, which is the defect the amendment removed.

    Asserted over the module's SOURCE, matched on the f-string prefixes the arms
    used to carry. Both openings are checked, because both were inline before.

    ITS REACH, STATED PLAINLY. This catches a REVERTED arm — one that goes back
    to the two openings this family has ever used. It does NOT catch a brand-new
    arm written inline with new prose and firing only on a state the corpus does
    not currently reach; nothing here can, short of enumerating arms, and
    `test_every_finding_matches_exactly_one_arm_template` only sees findings the
    corpus actually produces. What DOES cover the realistic case is measured:
    rebuilding the module with an arm's prose drifted from its template reds 24
    tests, because every rule-text pin in F1 and F2 reads the rendered bytes.
    """
    source = inspect.getsource(mbc)
    for opening in ('f"active MODIFIED block for ',
                    'f"the ordering of MODIFIED blocks for '):
        assert opening not in source, (
            f"an arm is building a rule text inline again ({opening!r}); it must "
            f"render through an `_ArmTemplate` or the shape mask cannot see it")
    # MOVED BY `govern-sibling-added-modified-deltas`, 2026-09-01: SIX -> EIGHT.
    # The packet registers `TEMPLATE_PAIRING` and `TEMPLATE_COLLISION`, and the
    # count moves with the registry rather than the registry being trimmed to
    # the count. The pairing class's FOUR reported states share ONE template on
    # purpose — one shape, one map entry, one remedy — so the two new classes
    # bring exactly two, and a third would mean a state had been given fixed
    # prose of its own.
    assert len(mbc._ARM_TEMPLATES) == 8
    assert len({t.id for t in mbc._ARM_TEMPLATES}) == 8


def test_two_findings_of_one_template_differing_in_an_unquoted_field_are_one_shape():
    """THE AMENDED DELTA'S SCENARIO 3, FIRST HALF: same template, different
    interpolations → ONE.

    The field varied here is the promoted spec's PATH, which is unquoted and was
    therefore shape-bearing under the rule as first ratified — this is the exact
    pair that made the real tree read six. Constructed so the difference is
    ONLY that field.
    """
    def ledger(spec_rel):
        return Finding(
            INFO, mbc.FAMILY, "openxFactory", "openspec/changes/c/specs/a/spec.md",
            mbc.TEMPLATE_LEDGER.render(
                title="A requirement", missing=1, total=3, spec_rel=spec_rel,
                listed="[body] 'z'"),
            mbc._ACTION)

    one = ledger("openspec/specs/alpha/spec.md")
    two = ledger("openspec/specs/omega/spec.md")
    assert one.rule != two.rule
    assert mbc._shape(one.rule) == mbc._shape(two.rule) == "template:carriage-ledger"

    # and the unit-KIND list, the other unquoted field the old rule split on
    three = Finding(
        INFO, mbc.FAMILY, "openxFactory", "openspec/changes/c/specs/a/spec.md",
        mbc.TEMPLATE_LEDGER.render(
            title="A requirement", missing=2, total=3,
            spec_rel="openspec/specs/alpha/spec.md",
            listed="[bullet] 'y'; [body] 'z'"),
        mbc._ACTION)
    assert mbc._shape(three.rule) == mbc._shape(one.rule)


def test_two_findings_of_different_templates_are_two_shapes():
    """THE AMENDED DELTA'S SCENARIO 3, SECOND HALF: different templates → TWO.

    Two templates are two map entries to write, so collapsing them would report
    one remedy where two are owed and quote only one of the two drifted texts.
    """
    ledger = Finding(
        INFO, mbc.FAMILY, "openxFactory", "openspec/changes/c/specs/a/spec.md",
        mbc.TEMPLATE_LEDGER.render(
            title="A requirement", missing=1, total=3,
            spec_rel="openspec/specs/alpha/spec.md", listed="[body] 'z'"),
        mbc._ACTION)
    titles = Finding(
        WARNING, mbc.FAMILY, "openxFactory", "openspec/changes/c/specs/a/spec.md",
        mbc.TEMPLATE_TITLES.render(
            title="A requirement", missing=1, total=3,
            spec_rel="openspec/specs/alpha/spec.md", named="'S'"),
        mbc._ACTION)
    assert mbc._shape(ledger.rule) != mbc._shape(titles.rule)
    assert {mbc._shape(ledger.rule), mbc._shape(titles.rule)} == {
        "template:carriage-ledger", "template:scenario-titles"}


def test_a_rule_text_no_template_claims_falls_back_and_is_never_merged():
    """FAIL-CLOSED (constitution VII), and the case is an arm's prose drifting
    from its own template.

    A text no template claims must NOT be absorbed into a neighbouring
    template's shape — that would merge a remedy nobody has written a template
    for into one somebody has. It falls back to the old lexical mask, where two
    such texts group only if they are lexically alike.
    """
    stray = "a rule text no template of this family emitted, naming 'x'"
    assert mbc._shape(stray) not in {t.id for t in mbc._ARM_TEMPLATES}
    assert mbc._shape(stray) == mbc._shape(
        "a rule text no template of this family emitted, naming 'y'")
    assert mbc._shape(stray) != mbc._shape(
        "a different stray text entirely, naming 'x'")


def test_two_unresolved_blocks_differing_only_in_capability_are_one_shape():
    """THE APOSTROPHE IN `sibling's`, AND WHY THE MASK IS A SCANNER.

    `_unresolved_finding`'s rule text is fixed prose interleaved with `repr`
    spans, and one of the fixed strings carries an apostrophe: "no active
    sibling's addition:". A GLOBAL substitution pairs that apostrophe with the
    opening quote of the NEXT `repr`, masks the prose between them, and leaves
    the capability name exposed — so two blocks that differ ONLY in an
    interpolated capability read as two shapes and the family reports two
    remedies for one.

    Constructed rather than fixtured, because the corpus resolves every block
    today; that is exactly when a rule is worth pinning. Both halves are
    asserted: the two collapse, AND the title `repr` is still masked, so the fix
    did not buy this by masking less.
    """
    def unresolved(title, capability):
        return Finding(
            WARNING, mbc.FAMILY, "openxFactory",
            "openspec/changes/c/specs/a/spec.md",
            f"active MODIFIED block for {title!r} resolves to no promoted "
            f"requirement, no rename of its own, and no active sibling's "
            f"addition: capability {capability!r} has no promoted spec at all",
            mbc._ACTION)

    a = unresolved("First block", "absent-a")
    b = unresolved("Second block", "absent-b")
    assert a.rule != b.rule
    assert mbc._shape(a.rule) == mbc._shape(b.rule) == "template:title-resolution"

    # ASSERTED AT THE MASKING LAYER TOO, because that is where the apostrophe
    # rule lives and where a regression would land. `_shape` now returns a
    # TEMPLATE ID, which would keep reading the same for both even if the mask
    # were broken in some other way — the template match would still succeed on
    # a differently-damaged text. This is the assertion that cannot.
    for rule in (a.rule, b.rule):
        masked = mbc._mask_repr_spans(rule)
        for leaked in ("absent-a", "absent-b", "First block", "Second block"):
            assert leaked not in masked, (leaked, masked)
        # ...and the prose apostrophe survives, because it is prose. The
        # template's own fixed segment carries it, so the match below depends on
        # it: a mask that ate it would take this finding to the fail-closed
        # fallback and split the two capabilities apart again.
        assert "sibling's addition" in masked, masked
    assert mbc._mask_repr_spans(a.rule) == mbc._mask_repr_spans(b.rule)


def test_dropping_either_new_class_s_pattern_makes_the_fifth_class_name_it(
        monkeypatch):
    """§ 2.8's NEGATIVE, VERIFIED FIRST AND THEN KEPT.

    A class whose pattern is registered can only be shown to be NEEDED by
    removing it: with the arm template registered and the `_CLASS_PATTERNS`
    entry absent, the fifth class must fire and QUOTE the new rule text. That is
    the fifth class working, and it is also the proof that the two new entries
    are load-bearing rather than decorative — an entry nothing would notice the
    absence of is an entry no test covers.

    ONE DRIFT FINDING PER CLASS, whatever the unplaced count: the grain is one
    per ARM TEMPLATE, which is one per REMEDY, and both new classes render
    through exactly one template each. Thirteen unplaced pairing findings and
    two unplaced collision ones each collapse to ONE — which is also what says
    the pairing class's four reported states are one shape.
    """
    for class_id, tree, phrase in (
        (mbc.CLASS_PAIRING, TREE_PAIRING,
         "rests on an active sibling's addition rather than on canon"),
        (mbc.CLASS_COLLISION, TREE_COLLISION,
         "writes a requirement title"),
    ):
        with pytest.MonkeyPatch.context() as patch:
            findings, unplaced = _drifted(patch, class_id, tree=tree)
            assert unplaced, class_id
            drift = _drift_findings(findings)
            assert len(drift) == 1, (class_id, [f.rule[:120] for f in drift])
            assert phrase in drift[0].rule, class_id
            assert f"no pattern for {len(unplaced)} findings" in drift[0].rule
            # ...and the residual row says so on the artifact too
            residual = [line for line in mbc.class_summary(findings)
                        if line.startswith("- unclassified: ")]
            assert residual == [
                f"- unclassified: {len(unplaced)} — findings this family "
                f"emitted that its own class map does not place; the map has "
                f"drifted from the arms and the counts above are short by this "
                f"many"], (class_id, residual)

    # ...and with BOTH patterns present the map places everything on both trees
    for tree in (TREE_PAIRING, TREE_COLLISION):
        findings = _fixture_findings(tree)
        assert [f for f in findings
                if mbc.classify(f) == mbc.UNCLASSIFIED] == [], tree
        assert _drift_findings(findings) == [], tree
