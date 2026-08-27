"""The twenty-first family: canon's family enumeration, derived-verified.

`add-family-enumeration-check`. Five things are under test, and they fail in
different directions:

1. **Each divergence class fires SEPARATELY and names what diverged** — a
   missing family name, a stale numeral, an unregistered name, an
   arithmetically impossible remainder. Asserting on the rule text rather than
   on "something fired" is the point: a build that reported the wrong sentence
   would pass a count-only assertion.

2. **A thin ACTIVE delta fires, which is the whole prevention.** Three changes
   in three days truncated this requirement and all three were caught by a
   human. The delta half reports the truncation at authoring time.

3. **A correct enumeration stays quiet**, and so does the PENDING case that
   would otherwise make this family fire on every legitimate in-flight
   family — canon at N while a complete active delta already states N+1.

4. **The alias set is minimal, by test.** One prose name does not normalize
   mechanically to its registry id; the alias for it must still be NEEDED, so
   a rename that makes it redundant fails here instead of leaving a private
   dictionary of forgiveness behind.

5. **The advisory launch is pinned structurally** — WARNING severity AND
   absence from `FAMILY_RESOLUTION` — because enforcement can arrive through
   either half.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import FIXTURES, FakeGit, make_ctx

from doc_health import Skip, WARNING
from doc_health import family_enumeration as fe
from doc_health.families import FAMILIES, FAMILY_RESOLUTION
from doc_health.family_enumeration import FAMILY

REPO = "alphaFactory"


def _run(fixture):
    return FAMILIES[FAMILY](make_ctx(fixture, git=FakeGit()))


def _rules(findings):
    return sorted(f.rule for f in findings)


def _on(findings, needle):
    return [f for f in findings if needle in f.rule]


# ------------------------------------------------------- 1. the divergences fire


def test_a_missing_family_name_fires_and_names_it():
    """The class that actually happened: `staged-topic-template` registered
    2026-08-15 and went uncounted for eight days."""
    hits = _on(_run("family-enumeration-missing-name"), "omits")
    assert len(hits) == 1
    assert "'family-enumeration'" in hits[0].rule
    assert "omits 1 of the 21 registered check families" in hits[0].rule
    assert hits[0].path == "openspec/specs/doc-health/spec.md"


def test_a_stale_numeral_fires_separately_from_the_names():
    """Names complete, numerals stale — the two halves are independent, and a
    build that only compared name-sets would call this healthy."""
    findings = _run("family-enumeration-stale-numeral")
    assert _on(findings, "omits") == []
    total = _on(findings, "check families, but")
    assert len(total) == 1
    assert "'twenty'" in total[0].rule and "21 are registered" in total[0].rule
    assert "expected 'twenty-one'" in total[0].rule
    # and the subset sentence carries its own stale total
    assert len(_on(findings, "of 'twenty', but 21 families")) == 1


def test_an_unregistered_name_is_reported_not_guessed_at():
    """A name resolving to nothing is a defect, not a puzzle for a fuzzier
    matcher — the whole reason the enumeration is DERIVED."""
    hits = _on(_run("family-enumeration-unknown-name"), "not a registered family")
    assert len(hits) == 1
    assert "'phantom check'" in hits[0].rule
    assert "'phantom-check'" in hits[0].rule


def test_an_impossible_remainder_fires_on_the_arithmetic():
    """`Four of the twenty-one … the other sixteen` does not add up. Asserted
    against a hand-built statement, because the fixture corpus deliberately
    keeps its numerals self-consistent."""
    st = fe.parse_statement("x.md", "canon", """### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twenty-one check families over
the whole factory family's governance corpus: alpha.
Four of the twenty-one — a, b, c, and d — SHALL additionally read the scan set;
the other sixteen families SHALL not.
""")
    findings = fe._check(st, ["alpha"] * 0 + [f"f{i}" for i in range(21)], REPO)
    hits = _on(findings, "does not add up")
    assert len(hits) == 1
    assert "expected 'seventeen'" in hits[0].rule


def test_a_thin_active_delta_fires_on_its_own_path():
    """THE PREVENTION. The delta restates the requirement with two names of
    twenty-one; the finding lands on the delta, not on canon."""
    findings = _run("family-enumeration-thin-delta")
    hits = _on(findings, "omits")
    assert len(hits) == 1
    assert hits[0].path == (
        "openspec/changes/add-something/specs/doc-health/spec.md")
    assert "this active delta's restatement" in hits[0].rule
    assert "omits 19 of the 21 registered check families" in hits[0].rule
    # canon is complete in this fixture and is NOT reported: the delta half is
    # what carries the obligation while a restatement is in flight
    assert all(f.path.startswith("openspec/changes/") for f in findings)


# ------------------------------------------------------ 2. the quiet directions


def test_a_correct_enumeration_is_quiet():
    assert _run("family-enumeration-clean") == []


def test_canon_pending_behind_a_complete_delta_is_quiet():
    """The case that would otherwise make this family fire on EVERY new
    family's branch: canon states twenty because it has not moved yet, and a
    complete active delta already states twenty-one. Canon is pending, not
    divergent."""
    assert _run("family-enumeration-pending") == []


def test_a_scope_without_a_doc_health_spec_skips_with_notice():
    out = _run("family-enumeration-no-spec")
    assert isinstance(out, Skip)
    assert out.family == FAMILY
    assert "doc-health" in out.reason


# ------------------------------------------- 3. the real corpus, both halves


def test_the_real_corpus_reads_zero_on_both_halves():
    """The acceptance measurement, run through the family itself against this
    repository's own tree — canon, and this change's own delta.

    THIS IS THE SELF-GATE. This change registers the twenty-first family, so
    it had to restate the very requirement it polices; the assertion below is
    the check verifying its own restatement. Before the delta was written the
    same call reported three findings — the omitted name and two stale
    numerals — and that is what makes this a test rather than a tautology.

    **AFTER THE ARCHIVE ACT (2026-08-27) THIS READS CANON ALONE.** The
    paragraph above is the historical claim and is kept as written; the block
    it describes was promoted, so "both halves" is now canon plus an empty
    active-delta set. Twenty-one families, `twenty-one` in canon, zero
    findings.
    """
    from conftest import REPO_ROOT

    class Ctx:
        repo_paths = {"openxFactory": Path(REPO_ROOT)}

    assert fe.fam_family_enumeration(Ctx()) == []


def test_canon_is_the_statement_under_test():
    """The test above is only meaningful if the family actually READ a
    statement. Asserted, so a refactor that stopped discovering statements
    could not leave it passing vacuously.

    **RE-AIMED BY THE ARCHIVE ACT (2026-08-27), NOT DELETED.** As written this
    was `test_this_changes_own_delta_is_the_statement_under_test` and it read
    the DELTA half, because while `add-family-enumeration-check` was active its
    own delta was the statement carrying the twenty-one enumeration — the
    self-gate the packet's §4.1 recorded. The archive act promoted that block,
    so the enumeration now lives in CANON and no active change restates the
    requirement: `_delta_statements` legitimately returns nothing, and the
    guard has to sit where the statement went. The three assertions are the
    same three, moved one document over. The delta half's own discovery stays
    covered by the fixture tests in §1.
    """
    from conftest import REPO_ROOT

    canon = fe._canon_statement(Path(REPO_ROOT))
    assert canon is not None
    assert canon.total_word == "twenty-one"
    assert len(canon.names) == len(FAMILIES)


# --------------------------------------------------- 4. the alias set is minimal


def test_every_alias_is_load_bearing():
    """An alias that is no longer needed is a private dictionary of
    forgiveness. Each entry must still fail to normalize mechanically."""
    import re

    for prose_slug, ident in fe.ALIASES.items():
        mechanical = re.sub(r"-{2,}", "-",
                            re.sub(r"[\s/]+", "-", prose_slug.lower())).strip("-")
        assert mechanical != ident, (
            f"alias {prose_slug!r} -> {ident!r} is redundant: the mechanical "
            f"normalization already produces {mechanical!r}")
        assert ident in FAMILIES, (
            f"alias {prose_slug!r} points at {ident!r}, which is not a "
            f"registered family")


def test_the_mechanical_normalization_covers_everything_else():
    """Only the declared aliases may need help. A second name drifting out of
    mechanical reach must fail HERE, by name, rather than being absorbed by a
    looser matcher later."""
    from conftest import REPO_ROOT

    canon = fe._canon_statement(Path(REPO_ROOT))
    aliased = 0
    for prose in canon.names:
        slug = fe.normalize_family_name(prose)
        assert slug in FAMILIES or slug in fe.ALIASES.values(), prose
        if slug in fe.ALIASES.values() and slug != prose.replace(" ", "-"):
            aliased += 1
    assert aliased == len(fe.ALIASES) == 1


def test_number_words_round_trip_over_the_range_the_corpus_uses():
    for n in range(1, 30):
        word = fe.WORD_FOR[n]
        assert fe.word_to_int(word) == n
    assert fe.word_to_int("umpteen") is None


def test_an_unreadable_numeral_is_reported_rather_than_treated_as_zero():
    st = fe.parse_statement("x.md", "canon", """### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement umpteen check families over
the whole factory family's governance corpus: alpha.
""")
    findings = fe._check(st, ["alpha-check"], REPO)
    assert len(_on(findings, "a total this check cannot read")) == 1


# ------------------------------------------------- 5. the advisory launch, pinned


def test_launch_is_advisory_by_severity():
    findings = _run("family-enumeration-missing-name")
    assert findings, "the advisory claim is vacuous over an empty run"
    assert {f.severity for f in findings} == {WARNING}
    assert fe._LAUNCH_SEVERITY == WARNING


def test_launch_is_advisory_by_resolution_class():
    """The half that is easy to lose: a CONTESTED entry would route a resolved
    finding into `report.uncited_resolutions` as an ERROR — enforcement
    through the back door on the first enumeration anyone corrected."""
    assert FAMILY not in FAMILY_RESOLUTION
    assert {f.resolution
            for f in _run("family-enumeration-missing-name")} == {"auto-fixable"}


def test_the_family_is_registered_for_reporting():
    from doc_health import FAMILY_IDS
    assert FAMILY in FAMILIES
    assert FAMILY in FAMILY_IDS


def test_the_reporting_list_mirrors_the_registry_exactly():
    """THE INVARIANT, pinned so the DRIFT CLASS dies rather than the instance.

    `report.render` iterates `FAMILY_IDS` to emit "## Findings By Family"
    sections, so a registered family missing from this list reports findings
    that count in the headline and appear in the ranked plan while rendering
    under NO SECTION AT ALL. That is what happened: `staged-topic-template`
    (registered 2026-08-15) and `proposal-origin` were absent, between them
    carrying 61 findings — three of them ERRORS — with nowhere to show. It was
    recorded as a known omission three separate times and deferred each time on
    the "not in this change's evidence" rule, which was right about scope and
    wrong about the outcome: the deferral outlived its reason. RULED
    2026-08-25 (Brett, "fix the FAMILY_IDS drift").

    Pinning SET EQUALITY does not make `FAMILY_IDS` a second authority for
    which families exist — `families.FAMILIES` remains the sole one, as that
    module's own docstring says. It makes this list the COMPLETE PROJECTION of
    that authority onto the report. Both directions matter and fail for
    different reasons: an extra entry renders a heading nothing fills, and a
    missing one hides real findings.

    ORDER is deliberately NOT pinned. It is the order sections render in, so
    it is a layout choice someone may legitimately want to change; membership
    is not.
    """
    from doc_health import FAMILY_IDS

    missing = sorted(set(FAMILIES) - set(FAMILY_IDS))
    phantom = sorted(set(FAMILY_IDS) - set(FAMILIES))
    assert not missing, (
        f"registered families with no report section: {missing} — their "
        f"findings count in the headline and the ranked plan but render "
        f"under no heading")
    assert not phantom, (
        f"`FAMILY_IDS` promises a section for unregistered families: "
        f"{phantom}")
    assert set(FAMILY_IDS) == set(FAMILIES)
    # no duplicates either: a repeated id would render its section twice
    assert len(FAMILY_IDS) == len(set(FAMILY_IDS)) == len(FAMILIES)


def test_the_runtime_phantom_check_still_guards_its_direction():
    """The family's own runtime check covers the phantom direction, and the
    test above covers both. Kept because it is the direction a reader of a
    REPORT can act on, and asserted against a synthetic registry so it does
    not merely restate the invariant."""
    assert fe._check_reporting_list(REPO, list(FAMILIES)) == []
    assert len(fe._check_reporting_list(REPO, ["only-this-one"])) == 1


def test_every_registered_family_can_render_a_section():
    """The consequence, asserted end to end rather than inferred: every
    registered family is reachable by the renderer's own iteration."""
    from doc_health import FAMILY_IDS
    from doc_health.semantic import SEMANTIC_FAMILY_IDS

    rendered = FAMILY_IDS + SEMANTIC_FAMILY_IDS + ["preflight"]
    for family in FAMILIES:
        assert family in rendered, family


# --------------------------------------------------------------- determinism


def test_the_run_is_deterministic():
    first = [(f.severity, f.path, f.rule)
             for f in _run("family-enumeration-missing-name")]
    second = [(f.severity, f.path, f.rule)
              for f in _run("family-enumeration-missing-name")]
    assert first == second
