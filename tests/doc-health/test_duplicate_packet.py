"""The nineteenth family: one ruling discharged by two archived packets.

`add-duplicate-packet-check`. Five things are under test, and they fail in
different directions:

1. **The near-miss fires, and fires ONCE.** `fixtures/duplicate-packet/`
   reconstructs the shape openxFactory came twenty minutes from landing on
   2026-08-25 — one original ruling and TWO byte-faithful remedials, each
   naming the original and neither naming the other. Three restatement pairs;
   two of them are recorded lineage; exactly one is a duplicate discharge.
   Asserting the COUNT is the point: a build that fired on all three would
   report the lawful remedy as a defect and be useless.

2. **The lawful patterns stay quiet**, and each one is a false positive this
   corpus really contains or really wants to: the codexFactory PR #85 shape
   (an original and one naming remedial), successive MODIFIEDs that revise a
   requirement rather than restate it, and two pre-ratification packets that
   discharged nothing to duplicate.

3. **The token boundary in the lineage test is load-bearing**, proven the way
   the eighteenth family proved its tie-break: by running the SAME fixture
   twice, once with the real matcher and once with the substring test a first
   draft would reach for, and asserting the two DISAGREE.

4. **The advisory launch is pinned structurally** — WARNING severity AND
   absence from `FAMILY_RESOLUTION` — because enforcement can arrive through
   either half.

5. **The reuse is real reuse.** The module owns no delta grammar, no status
   reader and no disposition reader of its own; it borrows the eighteenth
   family's, and a test asserts that rather than trusting the import list.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import FIXTURES, FakeGit, make_ctx

from doc_health import Skip, WARNING
from doc_health import duplicate_packet, promotion_fidelity
from doc_health.families import FAMILIES, FAMILY_NOTES, FAMILY_RESOLUTION
from doc_health.duplicate_packet import FAMILY

REPO = "alphaFactory"

ORIGINAL = "2026-08-01-add-branch-sessions"
REMEDIAL_ONE = "2026-08-25-apply-branch-sessions-deltas"
REMEDIAL_TWO = "2026-08-25-promote-branch-sessions-delta"


def _ctx(agg_root=None):
    return make_ctx("duplicate-packet", git=FakeGit(), agg_root=agg_root)


def _run(ctx=None):
    return FAMILIES[FAMILY](ctx if ctx is not None else _ctx())


def _on(findings, needle):
    return [f for f in findings if needle in f.rule]


def _tree():
    return promotion_fidelity.WorkingTree(FIXTURES / "duplicate-packet" / REPO)


# --------------------------------------------- 1. the near miss fires, exactly once


def test_the_near_miss_fires_on_the_remedial_pair():
    """Tonight's shape: the pair the record gives no account of.

    Asserted on the finding's OWN text rather than on something having fired
    against that path — "a finding exists here" would pass over a build that
    reported the original against a remedial, which is the failure that would
    make this family unusable.
    """
    hits = _on(_run(), "'Branch-session notebooks'")
    assert len(hits) == 1
    finding = hits[0]
    assert finding.path == (
        f"openspec/changes/archive/{REMEDIAL_TWO}/specs/"
        "notebook-projection/spec.md")
    assert "`promote-branch-sessions-delta` restates" in finding.rule
    assert "from `apply-branch-sessions-deltas`" in finding.rule
    assert "one ruling discharged twice" in finding.rule
    assert finding.action == (
        "name the packet this one restates in its proposal, or withdraw "
        "the duplicate discharge")


def test_the_original_is_never_the_finding():
    """The ORIGINAL packet ratified the ruling; it discharged nothing twice.

    Both of its pairs are exempt, so its delta path must carry no finding at
    all — and the check is on the path rather than on the count, because a
    build that swapped earlier for later would keep the count and move the
    remedy onto the wrong document.
    """
    original_delta = (f"openspec/changes/archive/{ORIGINAL}/specs/"
                      "notebook-projection/spec.md")
    assert [f for f in _run() if f.path == original_delta] == []


def test_three_restatements_are_three_pairs_and_one_finding():
    """The arithmetic the lineage rule performs, stated as a test.

    Two remedials of one original produce THREE pairs. Two carry a recorded
    lineage. One does not, and one finding is what the corpus should see.
    """
    groups = duplicate_packet.collect_statements(_tree())
    key = [k for k in groups
           if k[1] == "branch-session notebooks"]
    assert len(key) == 1, "the three packets must share ONE identity group"
    assert sorted(s.change for s in groups[key[0]]) == [
        ORIGINAL, REMEDIAL_ONE, REMEDIAL_TWO]
    assert len(_on(_run(), "'Branch-session notebooks'")) == 1


# ------------------------------------------------- 2. the lawful patterns stay quiet


def test_the_pr_85_shape_stays_quiet():
    """An original and ONE remedial that names it: the lawful remedy for a
    promotion gap, and the pattern the eighteenth family's action line tells
    a reader to perform. A family that reported it would be telling readers
    not to fix the thing it reports."""
    assert _on(_run(), "Tier-2 ships inactive") == []


def test_a_revision_with_different_content_stays_quiet():
    """Successive writers of one requirement are the ORDINARY case — 59
    (capability, requirement) pairs in openxFactory have more than one
    archived writer. They differ in content, so byte-identity never fires on
    them, and no lineage naming is owed for a revision."""
    assert _on(_run(), "'Ontology scaffold'") == []


def test_two_pre_ratification_packets_stay_quiet():
    """C5's class, twice over: byte-identical blocks, no lineage between
    them, and still quiet. A packet that never claimed ratification
    discharged no ruling, so there is no second discharge to report."""
    assert _on(_run(), "'Live runtime'") == []


def test_the_pre_ratification_exemption_is_the_eighteenth_familys():
    """One reader of one header. Monkeypatching the eighteenth family's own
    exemption must move this family too — if it does not, there are two
    readers of `Status:` in the package and they will one day disagree."""
    ctx = _ctx()
    before = len(_run(ctx))
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(promotion_fidelity, "_is_exempt_from_promotion",
                   lambda tree, change: False)
        after = _run(ctx)
    assert len(_on(after, "'Live runtime'")) == 1
    assert len(after) == before + 1


# --------------------------------------- 3. the lineage matcher's boundary is real


def test_a_prefix_id_does_not_buy_an_exemption():
    """`add-session-telemetry` is a strict prefix of
    `add-session-telemetry-extended`, whose proposal names only ITSELF. The
    pair must fire."""
    hits = _on(_run(), "'Session telemetry'")
    assert len(hits) == 1
    assert hits[0].path == (
        "openspec/changes/archive/2026-08-26-add-session-telemetry-extended/"
        "specs/telemetry/spec.md")


def test_a_substring_lineage_test_would_silence_the_prefix_pair():
    """The two runs that DISAGREE, which is what makes the boundary a rule
    rather than a comment.

    Swapping the token matcher for the plain substring test a first draft
    reaches for makes the prefix pair vanish — silence bought by a
    coincidence of naming, on a corpus whose change ids really do nest
    (`add-workbench-branch-sessions` inside
    `2026-08-01-add-workbench-branch-sessions`). Measuring the cost of the
    wrong rule beats asserting the right one is harmless.
    """
    import re

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(duplicate_packet, "_mention",
                   lambda identifier: re.compile(re.escape(identifier)))
        loose = _run()
    assert _on(loose, "'Session telemetry'") == []
    # and the near-miss pair is untouched: neither remedial's id is a
    # fragment of the other's, so the loose rule agrees there
    assert len(_on(loose, "'Branch-session notebooks'")) == 1


def test_both_lineage_spellings_are_accepted():
    """A proposal names its original as a bare change id or as the archived
    folder that carries it, and the corpus uses both — often in one
    paragraph, which is exactly what
    `2026-08-25-apply-branch-sessions-deltas` does on main."""
    proposals = duplicate_packet._Proposals(_tree())
    assert proposals.names_change(REMEDIAL_ONE, ORIGINAL)
    assert proposals.names_change(REMEDIAL_TWO, ORIGINAL)
    # the two remedials have no account of each other, which is the finding
    assert not proposals.names_change(REMEDIAL_ONE, REMEDIAL_TWO)
    assert not proposals.names_change(REMEDIAL_TWO, REMEDIAL_ONE)


def test_the_bare_id_is_read_out_of_the_archive_folder_name():
    assert duplicate_packet.change_id(ORIGINAL) == "add-branch-sessions"
    # an undated folder is its own id, never a slice of one
    assert duplicate_packet.change_id("legacy-packet") == "legacy-packet"


# ------------------------------------------------ 4. the content rule, at its edges


def test_trailing_whitespace_is_the_only_normalization():
    """The boundary the decision drew, asserted from both sides."""
    body = ["The rule SHALL hold.", "", "- **WHEN** x", "- **THEN** y"]
    assert duplicate_packet.fingerprint(body) == duplicate_packet.fingerprint(
        ["The rule SHALL hold.   ", "   ", "- **WHEN** x", "- **THEN** y  ",
         "", "  "])
    # a one-word edit to normative text is a DIFFERENT statement
    assert duplicate_packet.fingerprint(body) != duplicate_packet.fingerprint(
        ["The rule SHALL not hold.", "", "- **WHEN** x", "- **THEN** y"])
    # so is a reordering: this family compares bytes, never sets
    assert duplicate_packet.fingerprint(body) != duplicate_packet.fingerprint(
        ["The rule SHALL hold.", "", "- **THEN** y", "- **WHEN** x"])


def test_the_requirement_header_is_not_part_of_the_body():
    """Two packets spelling one title with different spacing state the same
    requirement — `norm` already says so — so folding the header line into
    the bytes would make the title's whitespace decide the content rule."""
    requirements, _ = promotion_fidelity.parse_delta(
        "## ADDED Requirements\n\n"
        "### Requirement:   Spaced   Title\n"
        "The rule SHALL hold.\n\n"
        "#### Scenario: It holds\n"
        "- **WHEN** x\n- **THEN** y\n")
    assert len(requirements) == 1
    assert "Requirement:" not in "\n".join(requirements[0].body)
    assert requirements[0].body[0] == "The rule SHALL hold."
    assert "#### Scenario: It holds" in requirements[0].body


def test_scenario_lines_are_part_of_the_body():
    """The body is the WHOLE block. A build that recorded only prose would
    call two packets identical while their scenarios differed — the exact
    gap the eighteenth family's own true positive lived in."""
    one, _ = promotion_fidelity.parse_delta(
        "## ADDED Requirements\n\n### Requirement: R\nProse.\n\n"
        "#### Scenario: A\n- **WHEN** x\n- **THEN** y\n")
    two, _ = promotion_fidelity.parse_delta(
        "## ADDED Requirements\n\n### Requirement: R\nProse.\n\n"
        "#### Scenario: B\n- **WHEN** x\n- **THEN** y\n")
    assert (duplicate_packet.fingerprint(one[0].body)
            != duplicate_packet.fingerprint(two[0].body))


def test_a_renamed_block_states_no_body_and_pairs_with_nothing():
    """RENAMED carries a FROM/TO pair, not a requirement block. It is not a
    discharge of normative content and cannot be a duplicate one."""
    groups = duplicate_packet.collect_statements(_tree())
    assert all(s.op in promotion_fidelity.CHECKED_OPS
               for statements in groups.values() for s in statements)


# ------------------------------------------------- 5. the advisory launch, pinned


def test_launch_is_advisory_by_severity():
    """First half. Every finding is WARNING, so `--fail-on error` and
    `--fail-on critical` cannot red on this family."""
    findings = _run()
    assert findings, "the advisory claim is vacuous over an empty run"
    assert {f.severity for f in findings} == {WARNING}
    assert duplicate_packet._LAUNCH_SEVERITY == WARNING


def test_launch_is_advisory_by_resolution_class():
    """Second half, and the one that is easy to lose. A CONTESTED entry
    would route a resolved finding into `report.uncited_resolutions` as an
    ERROR — enforcement through the back door on the first duplicate anyone
    withdrew. The flip raises severity and adds this entry TOGETHER."""
    assert FAMILY not in FAMILY_RESOLUTION
    assert {f.resolution for f in _run()} == {"auto-fixable"}


def test_the_family_is_registered_for_reporting():
    from doc_health import FAMILY_IDS
    assert FAMILY in FAMILIES
    assert FAMILY in FAMILY_IDS


def test_the_family_declares_no_measurement_basis_note():
    """The live-`main` basis was ruled for the promotion-fidelity family AND
    THAT FAMILY ALONE (task 4.1, PR #315), and `basis_notes` tells every
    reader that every other family measures the checkout. A `FAMILY_NOTES`
    entry here would be this family quietly joining a ruling it was not
    given — so the absence is asserted, not left to be noticed."""
    assert FAMILY not in FAMILY_NOTES
    assert "promotion_fidelity_basis" not in Path(
        duplicate_packet.__file__).read_text(encoding="utf-8")


# ------------------------------------------------------------- dispositions


def _dispositions(tmp_path, body: str):
    health = tmp_path / "health"
    health.mkdir(parents=True, exist_ok=True)
    (health / "dispositions.yaml").write_text(body, encoding="utf-8")
    return tmp_path


def test_a_cited_disposition_suppresses_one_requirement(tmp_path):
    agg = _dispositions(tmp_path, f"""
- family: {FAMILY}
  repo: {REPO}
  path: openspec/changes/archive/{REMEDIAL_TWO}/specs/notebook-projection/spec.md
  requirement: Branch-session notebooks
  cite: add-duplicate-packet-check
""")
    findings = _run(_ctx(agg_root=agg))
    assert _on(findings, "'Branch-session notebooks'") == []
    assert len(_on(findings, "'Session telemetry'")) == 1


def test_an_uncited_entry_disposes_nothing(tmp_path):
    """An entry without a `cite` records no decision — the rule every other
    reader of this file already applies."""
    agg = _dispositions(tmp_path, f"""
- family: {FAMILY}
  repo: {REPO}
  path: openspec/changes/archive/{REMEDIAL_TWO}/specs/notebook-projection/spec.md
""")
    assert len(_run(_ctx(agg_root=agg))) == 2


def test_a_disposition_for_the_neighbouring_family_disposes_nothing(tmp_path):
    """The reason this is a SIBLING family rather than a finding kind inside
    the eighteenth: dispositions key on `(family, repo, path)`, and a
    promotion gap dispositioned on a delta must not also buy silence for a
    duplicate discharge on the same delta. Two governance decisions, two
    citations."""
    agg = _dispositions(tmp_path, f"""
- family: {promotion_fidelity.FAMILY}
  repo: {REPO}
  path: openspec/changes/archive/{REMEDIAL_TWO}/specs/notebook-projection/spec.md
  cite: add-promotion-fidelity-check
""")
    assert len(_run(_ctx(agg_root=agg))) == 2


# ---------------------------------------------------------------- skip with notice


def test_a_scope_without_an_archive_skips_with_notice():
    """Never silently omitted — the contract's own rule for a family that
    cannot run."""
    out = FAMILIES[FAMILY](make_ctx("duplicate-packet-no-archive",
                                    git=FakeGit()))
    assert isinstance(out, Skip)
    assert out.family == FAMILY
    assert "archive" in out.reason


# ------------------------------------------------------------------ determinism


def test_the_run_is_deterministic():
    """Identical inputs, identical findings in identical order — the suite's
    own contract, and the property the report's regression diff rests on."""
    first = [(f.severity, f.path, f.rule) for f in _run()]
    second = [(f.severity, f.path, f.rule) for f in _run()]
    assert first == second
    # and the order is DECLARED, not incidental: repositories sorted, then
    # identity groups sorted, then pairs walked earliest-first inside each.
    assert [path for _sev, path, _rule in first] == [
        f"openspec/changes/archive/{REMEDIAL_TWO}/specs/"
        "notebook-projection/spec.md",
        "openspec/changes/archive/2026-08-26-add-session-telemetry-extended/"
        "specs/telemetry/spec.md",
    ]


def test_the_pinned_basis_is_the_only_tree_this_family_reads():
    """Structural, not incidental. `_repo_trees` builds `WorkingTree` and
    nothing else, so no configuration can move this family onto the live-main
    basis without a visible edit here."""
    _, tree = duplicate_packet._repo_trees(_ctx())[0]
    assert isinstance(tree, promotion_fidelity.WorkingTree)
    assert tree.basis == promotion_fidelity.BASIS_PINNED
