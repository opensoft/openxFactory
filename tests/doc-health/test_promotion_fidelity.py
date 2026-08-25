"""The eighteenth family: promotion fidelity of archived spec deltas.

`add-promotion-fidelity-check`. Four things are under test, and they fail in
different directions:

1. **The historical true positive fires.** `fixtures/promotion-fidelity/`
   reconstructs the SHAPE of codexFactory's real pre-PR-#85 gap — the
   archived `2026-08-08-activate-nightly-sweep-council-clearance` ratified
   six scenarios, canon carried two — plus openxFactory's own live gap, a
   whole ADDED requirement that never reached its promoted spec. The fixture
   is a reconstruction and says so: this repository cannot depend on the
   codex checkout, so the SHAPE is frozen here and the real instance is
   recorded in `docs/archive-record-discrepancies.md` under FU-DOM-CODEX.

2. **The known negatives stay quiet**, and each one is a false positive this
   corpus really contains: C5's deliberately-unpromoted deltas, a
   requirement rewritten by a LATER archived change, and a requirement
   RENAMED by a later archived change.

3. **The ENFORCING state is pinned structurally** (`test_enforcement_*`),
   not left to the severity that happens to be written on a finding. These
   tests pinned the ADVISORY launch until 2026-08-24 — WARNING severity AND
   absence from `FAMILY_RESOLUTION` — and they now pin its opposite, because
   Brett ruled the flip ("ENFORCING, SEQUENCED", task 4.1, PR #315) and it
   was taken in one commit after the standing population was discharged
   (§4.2/§4.3). The assertions are still BOTH halves, and still for the same
   reason: enforcement can arrive through either, so a half-flip in either
   direction has to fail here by name.

4. **The tie-break is load-bearing**, proven by running the SAME fixture
   twice: once with archive-commit order available and once without. The
   two runs disagree, which is what makes the ordering rule a rule rather
   than a comment.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import AS_OF, FIXTURES, FakeGit, make_ctx

from doc_health import CONTESTED, ERROR, Skip, TAXONOMY, WARNING
from doc_health import corpus, promotion_fidelity, runner
from doc_health.families import FAMILIES, FAMILY_NOTES, FAMILY_RESOLUTION
from doc_health.promotion_fidelity import FAMILY

REPO = "alphaFactory"
GAMMA = "gammaFactory"          # the presumption fixture's repo
LIVE = promotion_fidelity.LIVE_REF
LIVE_SHA = "1274b9bf014516f52673c0592f40e868c041dd29"

# The two packets of the same-date tie group, with archive-commit stamps that
# DISAGREE with folder-name order: `zeta-earlier` sorts last by name and was
# archived first. Canon carries `alpha-later`'s text.
TIE_STAMPS = {
    (REPO, "openspec/changes/archive/2026-07-20-alpha-later"): 1_753_000_200,
    (REPO, "openspec/changes/archive/2026-07-20-zeta-earlier"): 1_753_000_100,
}


def _ctx(stamps=TIE_STAMPS, agg_root=None):
    return make_ctx("promotion-fidelity",
                    git=FakeGit(first_stamps=dict(stamps)),
                    agg_root=agg_root)


def _run(ctx=None):
    return FAMILIES[FAMILY](ctx if ctx is not None else _ctx())


def _rules(findings):
    return sorted(f.rule for f in findings)


def _on(findings, needle):
    return [f for f in findings if needle in f.rule]


# ------------------------------------------------- 1. the true positives fire


def test_the_codex_regression_shape_fires():
    """The commissioned regression: a ratified MODIFIED delta of six
    scenarios, four of which never reached canon.

    Asserted on the COUNTS and on a named missing scenario, not on the
    finding merely existing — "some finding fired on that path" would pass
    over a build that reported the wrong four.
    """
    hits = _on(_run(), "Tier-2 ships inactive")
    assert len(hits) == 1
    finding = hits[0]
    assert finding.path == (
        "openspec/changes/archive/"
        "2026-08-08-activate-nightly-sweep-council-clearance/"
        "specs/merge-master-approval/spec.md")
    assert "without 4 of its 6 ratified scenarios" in finding.rule
    assert "Activation requires a freshly accepted record" in finding.rule
    assert "openspec/specs/merge-master-approval/spec.md" in finding.rule


def test_a_whole_added_requirement_that_never_arrived_fires():
    """openxFactory's OWN live instance, in fixture form: an ADDED
    requirement absent from canon by title."""
    hits = _on(_run(), "'Branch-session notebooks'")
    assert len(hits) == 1
    assert hits[0].rule == (
        "ratified ADDED requirement 'Branch-session notebooks' is absent "
        "from openspec/specs/notebook-projection/spec.md")


def test_one_missing_scenario_on_an_arrived_requirement_fires():
    """The quieter half of the same real gap: the requirement landed, one of
    its four ratified scenarios did not."""
    hits = _on(_run(), "'Corpus scan scope'")
    assert len(hits) == 1
    assert "without 1 of its 4 ratified scenarios" in hits[0].rule
    assert "A canon book is offered a branch session's drafts" in hits[0].rule


def test_a_removed_requirement_still_in_canon_fires():
    """REMOVED deltas check for ABSENCE, which is the direction a
    title-presence check gets backwards if nobody writes it down."""
    hits = _on(_run(), "REMOVED requirement")
    assert len(hits) == 1
    assert hits[0].rule == (
        "ratified REMOVED requirement 'Obsolete rule' is still present in "
        "openspec/specs/removed-capability/spec.md")


def test_the_fixture_fires_exactly_four_times():
    """The whole-population assertion. Every other test here names ONE
    finding; this one says there are no others — which is the assertion that
    fails when a negative starts firing."""
    findings = _run()
    assert len(findings) == 4, _rules(findings)
    assert {f.family for f in findings} == {FAMILY}
    assert {f.repo for f in findings} == {REPO}


# --------------------------------------------------- 2. the negatives stay quiet


def test_the_c5_class_stays_quiet():
    """A packet whose own proposal reads `Status: draft` never claimed the
    ratification that would have obliged promotion.

    This is the C5 exemption: `2026-06-26-enable-live-openxfactory` was
    archived with `--skip-specs`, keeping four spec deltas as archived
    design evidence, and the 2026-08-23 supersession addendum backfilled
    `Status: draft` onto it to say exactly that in the corpus's own
    vocabulary. The fixture packet declares four requirements across a
    capability that has NO promoted spec at all — the loudest possible
    shape — and the family says nothing about any of them.
    """
    assert _on(_run(), "live-runtime") == []
    assert _on(_run(), "Live factory pilot flow") == []


def test_the_c5_exemption_is_the_only_thing_keeping_it_quiet(tmp_path):
    """Mutation guard. Flip the packet's header to `ratified` and the two
    requirements MUST start firing — otherwise the exemption is untested and
    something else is doing the silencing.

    Mutated in a COPY under `tmp_path`, never in the shared fixture tree: a
    test that edits a fixture in place and restores it in a `finally` leaves
    the working tree dirty on any crash between the two, and this suite's
    fixtures are read by other modules in the same session.
    """
    copy = tmp_path / REPO
    shutil.copytree(FIXTURES / "promotion-fidelity" / REPO, copy)
    proposal = (copy / "openspec" / "changes" / "archive" /
                "2026-06-26-enable-live-legacy" / "proposal.md")
    proposal.write_text(
        proposal.read_text(encoding="utf-8").replace(
            "Status: draft", "Status: ratified"), encoding="utf-8")

    ctx = _ctx()
    ctx.repo_paths = {REPO: copy}
    loud = FAMILIES[FAMILY](ctx)
    assert len(_on(loud, "live-runtime")) == 2, _rules(loud)


def test_a_requirement_rewritten_by_a_later_change_stays_quiet():
    """Latest writer wins. The 2026-07-01 packet ratified a scenario canon
    does not carry; the 2026-07-30 packet rewrote the requirement without
    it. Canon is right and the earlier delta is superseded text."""
    assert _on(_run(), "Ontology scaffold") == []


def test_a_requirement_renamed_by_a_later_change_stays_quiet():
    """`openspec archive` applies RENAMED before MODIFIED, so a later rename
    legitimately removes an earlier delta's title from canon."""
    assert _on(_run(), "Staging workbench scoped view") == []
    assert _on(_run(), "doxBench scoped view") == []


def test_a_delta_that_actually_arrived_stays_quiet():
    assert _on(_run(), "clean-capability") == []
    assert _on(_run(), "A promoted requirement") == []


def test_latest_writer_wins_is_load_bearing():
    """Mutation guard for the ordering rule itself.

    Checking EVERY writer instead of the latest is measurably noisier: on
    this fixture it turns two quiet supersessions into findings. The
    assertion is on that DELTA, so a build that silently reverted to
    per-writer checking fails here even though the fixture still fires its
    four true positives.
    """
    ctx = _ctx()
    findings = FAMILIES[FAMILY](ctx)

    per_writer = []
    repo_path = Path(ctx.repo_paths[REPO])
    writers = promotion_fidelity._collect_writers(
        promotion_fidelity.WorkingTree(repo_path))
    for key, group in sorted(writers.items()):
        for writer in group:
            if writer.op != "ADDED":
                continue
            spec = repo_path / "openspec" / "specs" / key[0] / "spec.md"
            canon = promotion_fidelity.parse_promoted(
                spec.read_text(encoding="utf-8")) if spec.is_file() else None
            if canon is None or key[1] not in canon:
                per_writer.append((writer.change, writer.title))
            elif [s for s in writer.scenarios
                  if promotion_fidelity.norm(s) not in canon[key[1]]]:
                per_writer.append((writer.change, writer.title))

    superseded = {("2026-07-01-add-ontology-layer", "Ontology scaffold"),
                  ("2026-07-02-add-workbench-view",
                   "Staging workbench scoped view")}
    assert superseded <= set(per_writer), per_writer
    assert not any(title in f.rule for _, title in superseded
                   for f in findings)


# ------------------------------------------------ 3. the enforcing state, pinned
#
# THESE THREE TESTS CHANGED MEANING on 2026-08-24, and that is a design fact
# rather than a weakened assertion. Through the advisory launch they pinned
# WARNING severity and ABSENCE from `FAMILY_RESOLUTION`; they now pin ERROR
# and a `contested` entry. The flip is Brett's ruling (task 4.1's
# four-question round, PR #315, verbatim "ENFORCING, SEQUENCED"), realized in
# §4.2 after §4.3's discharge. What did NOT change is why there are two of
# them: enforcement can arrive through severity or through the resolution
# class, so each half is pinned separately and a half-flip fails by name.


def test_enforcement_by_severity():
    """The flip's first half. Every finding is ERROR, so `--fail-on error`
    (gate `{CRITICAL, ERROR}`) reds on a ratified delta that never reached
    canon. Was WARNING for the advisory launch."""
    findings = _run()
    assert findings, "the severity claim is vacuous over an empty run"
    assert {f.severity for f in findings} == {ERROR}
    assert promotion_fidelity._LAUNCH_SEVERITY == ERROR
    assert promotion_fidelity._LAUNCH_SEVERITY != WARNING


def test_enforcement_by_resolution_class():
    """The flip's second half, and the one that is easy to lose.

    `report.uncited_resolutions` turns a CONTESTED finding that vanishes
    between reports into an ERROR under the `uncited-resolution` family.
    Under the advisory launch that was a back door — the nightly would have
    gone red the first time anyone actually promoted a delta this family
    reported. Under enforcement it is the discipline the ruling wanted: the
    remedy is a governance act, so a finding that disappears owes a citation.

    Asserted at BOTH ends. The table entry is the declaration; `runner.main`
    is the only thing that applies it, so a `FAMILY_RESOLUTION` row that some
    future refactor stopped reading would pass the first assertion and fail
    the second.
    """
    assert FAMILY_RESOLUTION.get(FAMILY) == CONTESTED
    # The family function itself still labels findings `auto-fixable`; the
    # table is applied in `runner.main`, which is what the next assertion
    # exercises end to end.
    assert {f.resolution for f in _run()} == {"auto-fixable"}


def test_both_halves_reach_the_emitted_findings(tmp_path):
    """END TO END for the flip: run the CLI over the fixture and read both
    halves off the REPORT rather than off the constants.

    `runner.main` is the only thing that applies `FAMILY_RESOLUTION`, so a
    table entry some future refactor stopped reading would still satisfy the
    declaration test above and fail here.
    """
    out = tmp_path / "report.md"
    repo = tmp_path / REPO
    shutil.copytree(FIXTURES / "promotion-fidelity" / REPO, repo)
    assert runner.main([
        "--single-repo", str(repo),
        "--family", FAMILY, "--as-of", AS_OF.isoformat(),
        "--report-out", str(out)]) == 0
    emitted = [ln for ln in out.read_text(encoding="utf-8").splitlines()
               if f"family={FAMILY}" in ln]
    assert emitted
    assert all("severity=error" in ln for ln in emitted), emitted
    assert all('class="contested"' in ln for ln in emitted), emitted


def test_an_enforcing_run_reds_a_fail_on_error_gate(tmp_path):
    """The point of the flip, measured rather than asserted: the SAME fixture
    that returned 0 under `--fail-on error` for the whole advisory launch now
    returns non-zero. `--fail-on critical` still passes — the flip raised the
    family to ERROR, not to CRITICAL."""
    repo = tmp_path / REPO
    shutil.copytree(FIXTURES / "promotion-fidelity" / REPO, repo)

    def run(fail_on):
        return runner.main([
            "--single-repo", str(repo), "--family", FAMILY,
            "--as-of", AS_OF.isoformat(),
            "--report-out", str(tmp_path / f"{fail_on}.md"),
            "--fail-on", fail_on])

    assert run("error") != 0
    assert run("critical") == 0


def test_the_family_is_registered_for_reporting():
    from doc_health import FAMILY_IDS
    assert FAMILY in FAMILIES
    assert FAMILY in FAMILY_IDS


# ----------------------------------------------------- 4. the tie-break is real


def test_a_same_date_tie_is_broken_by_archive_commit_order():
    """Two packets archived on one date, canon carrying the LATER one's
    text. With archive-commit order available the family is quiet."""
    assert _on(_run(_ctx()), "Contested on one date") == []


def test_the_name_order_fallback_disagrees_and_is_therefore_load_bearing():
    """The same fixture with git unable to answer.

    Folder-name order picks `zeta-earlier` — it sorts last — and fires. The
    two runs disagreeing is the whole point: it proves archive-commit order
    is doing work, and it measures the cost of the documented fallback
    rather than asserting the fallback is harmless. Measured against
    openxFactory's real archive, folder-name order disagrees with
    archive-commit order on six of nineteen tie groups.
    """
    quiet = _on(_run(_ctx(stamps={})), "Contested on one date")
    assert len(quiet) == 1
    assert "The earlier statement holds" in quiet[0].rule


# ------------------------------------------------------------- dispositions


def _dispositions(tmp_path, body: str):
    health = tmp_path / "health"
    health.mkdir(parents=True, exist_ok=True)
    (health / "dispositions.yaml").write_text(body, encoding="utf-8")
    return tmp_path


def test_a_cited_disposition_suppresses_one_requirement(tmp_path):
    """The existing `health/dispositions.yaml` vocabulary, narrowed by the
    optional `requirement:` key — the same shape the neutrality lane's
    `content_sha256` extension already set."""
    agg = _dispositions(tmp_path, f"""
- family: {FAMILY}
  repo: {REPO}
  path: openspec/changes/archive/2026-08-01-add-branch-sessions/specs/notebook-projection/spec.md
  requirement: Branch-session notebooks
  cite: add-promotion-fidelity-check
""")
    findings = _run(_ctx(agg_root=agg))
    assert _on(findings, "'Branch-session notebooks'") == []
    # its file-mate is NOT suppressed: the entry names one requirement
    assert len(_on(findings, "'Corpus scan scope'")) == 1


def test_an_entry_without_a_requirement_suppresses_the_whole_path(tmp_path):
    agg = _dispositions(tmp_path, f"""
- family: {FAMILY}
  repo: {REPO}
  path: openspec/changes/archive/2026-08-01-add-branch-sessions/specs/notebook-projection/spec.md
  cite: add-promotion-fidelity-check
""")
    findings = _run(_ctx(agg_root=agg))
    assert _on(findings, "notebook-projection") == []
    assert len(findings) == 2, _rules(findings)


def test_an_uncited_entry_disposes_nothing(tmp_path):
    """An entry without a `cite` records no decision — the rule every other
    reader of this file already applies."""
    agg = _dispositions(tmp_path, f"""
- family: {FAMILY}
  repo: {REPO}
  path: openspec/changes/archive/2026-08-01-add-branch-sessions/specs/notebook-projection/spec.md
""")
    assert len(_run(_ctx(agg_root=agg))) == 4


def test_a_disposition_for_another_family_disposes_nothing(tmp_path):
    agg = _dispositions(tmp_path, f"""
- family: neutrality-drift
  repo: {REPO}
  path: openspec/changes/archive/2026-08-01-add-branch-sessions/specs/notebook-projection/spec.md
  cite: some-change
""")
    assert len(_run(_ctx(agg_root=agg))) == 4


# ---------------------------------------------------------------- skip with notice


def test_a_scope_without_an_archive_skips_with_notice():
    """Never silently omitted — the contract's own rule for a family that
    cannot run."""
    ctx = make_ctx("promotion-fidelity-no-archive", git=FakeGit())
    out = FAMILIES[FAMILY](ctx)
    assert isinstance(out, Skip)
    assert out.family == FAMILY
    assert "archive" in out.reason


# ------------------------------------------------------------------ determinism


def test_two_runs_agree_byte_for_byte():
    a, b = _run(_ctx()), _run(_ctx())
    assert [f.__dict__ for f in a] == [f.__dict__ for f in b]


# ------------------------------------------------------------------- the parsers


def test_the_delta_parser_reads_ops_titles_scenarios_and_renames():
    text = (FIXTURES / "promotion-fidelity" / REPO / "openspec" / "changes" /
            "archive" / "2026-08-02-rename-workbench-view" / "specs" /
            "ontology" / "spec.md").read_text(encoding="utf-8")
    requirements, renames = promotion_fidelity.parse_delta(text)
    assert renames == [("Staging workbench scoped view",
                        "doxBench scoped view")]
    assert [(r.op, r.title) for r in requirements] == [
        ("MODIFIED", "doxBench scoped view")]
    assert requirements[0].scenarios == ["A scope is chosen"]


def test_normalization_collapses_whitespace_and_case_and_nothing_else():
    """The disclosed narrowing. Casefold and whitespace, never punctuation:
    the codex gap carried a `tier-2`-to-`tier 2` change INSIDE a scenario
    body, and a rule loose enough to forgive punctuation in a title is one
    that would have forgiven that too."""
    assert promotion_fidelity.norm("  Tier-2   Ships\tInactive ") == \
        "tier-2 ships inactive"
    assert promotion_fidelity.norm("Tier-2 ships") != \
        promotion_fidelity.norm("Tier 2 ships")
    assert promotion_fidelity.norm("A rule.") != promotion_fidelity.norm("A rule")


def test_a_scenario_before_any_requirement_belongs_to_nothing():
    requirements, renames = promotion_fidelity.parse_delta(
        "## ADDED Requirements\n\n#### Scenario: Orphan\n\n"
        "### Requirement: Real\n\n#### Scenario: Owned\n")
    assert renames == []
    assert [(r.title, r.scenarios) for r in requirements] == [
        ("Real", ["Owned"])]


def test_headings_outside_a_declared_operation_are_not_delta_statements():
    """A delta file's prose preamble can carry `###` headings. Only headings
    under a declared `## <OP> Requirements` section are statements."""
    requirements, _ = promotion_fidelity.parse_delta(
        "# Delta\n\n### Requirement: Not a statement\n\n"
        "## ADDED Requirements\n\n### Requirement: A statement\n")
    assert [r.title for r in requirements] == ["A statement"]


def test_an_undated_archive_folder_never_outranks_a_dated_one():
    assert promotion_fidelity._archive_date("legacy-bootstrap") == ""
    assert promotion_fidelity._archive_date("2026-08-24-x") == "2026-08-24"
    assert "" < "2026-08-24"


# ============================================================================
# 5. THE PRESUMPTION (ruled 2026-08-24, task 4.1, PR #315)
#
# The exemption was `status == "ratified"`; it is now "explicitly draft or a
# lower taxonomy standing", with archiving itself presumed to be ratification.
# The two shapes that made the old spelling a false-negative channel are
# fixtures here, taken from the real packets the ruling's measurement named:
# an ANNOTATED ratification (hermes-install, 23 requirements unexamined) and a
# HEADERLESS archive (medx-roottruth-install + hermes-install, 31 more).
#
# The alphaFactory fixture above is deliberately NOT extended with them. Its
# `test_the_fixture_fires_exactly_four_times` is the regression evidence that
# the relaxation moved NOTHING for packets that read exactly `ratified` or
# exactly `draft` — the same result openxFactory's own archive measured (2
# findings before, 2 after, across 89 delta-carrying packets).
# ============================================================================


def _beta_ctx(agg_root=None):
    return make_ctx("promotion-fidelity-presumption", git=FakeGit(),
                    agg_root=agg_root)


def _beta():
    return FAMILIES[FAMILY](_beta_ctx())


def test_an_annotated_ratification_is_examined():
    """`Status: ratified (approved at commit 5ace969). Amendment A1 ...`

    `corpus.STATUS_RE` captures the whole rest of the line, so this value was
    never the string `ratified` and the packet was silently exempt. It is the
    shape hermes-install's archived three-layer-runtime packet carries, and it
    took 23 requirements out of examination with it.
    """
    hits = _on(_beta(), "'Layer seeding'")
    assert len(hits) == 1
    assert hits[0].path == (
        "openspec/changes/archive/2026-07-10-annotated-ratification/"
        "specs/runtime-foundation/spec.md")
    assert "absent from openspec/specs/runtime-foundation/spec.md" \
        in hits[0].rule


def test_a_headerless_archived_packet_is_examined():
    """A packet with no `Status:` header anywhere in the window.

    Three real packets carry this shape (medx-roottruth-install's two and
    hermes-install's seed-layer one) and between them 31 requirements were
    unexamined — a silence bought by an omission rather than by a decision.
    The missing header itself is `fam_status_validity`'s finding to report,
    over the lifecycle scan set; it is not this family's job to double as it.
    """
    hits = _on(_beta(), "'Tiered ingestion'")
    assert len(hits) == 1
    assert "2026-07-11-headerless-archive" in hits[0].path


def test_a_packet_with_no_proposal_at_all_is_examined():
    """The floor of the same presumption: no `proposal.md` in the packet."""
    hits = _on(_beta(), "'Probe endpoint'")
    assert len(hits) == 1
    assert "2026-07-14-no-proposal-at-all" in hits[0].path


def test_an_explicit_draft_stays_exempt():
    """C5's own shape, and the reason the relaxation cost nothing: a packet
    that explicitly declares pre-ratification standing still declares it."""
    assert _on(_beta(), "'Never ratified rule'") == []


def test_an_annotated_draft_stays_exempt():
    """The symmetry the leading-token reader buys. `Status: draft — archived
    with --skip-specs; never ratified` declares `draft` for exactly the reason
    an annotated `ratified` declares `ratified`."""
    assert _on(_beta(), "'Annotated draft rule'") == []


def test_the_presumption_fixture_fires_exactly_three_times():
    """The whole-population assertion for this fixture: three examined
    packets, two exempt ones, and nothing else."""
    findings = _beta()
    assert len(findings) == 3, _rules(findings)
    assert {f.repo for f in findings} == {GAMMA}
    assert {f.severity for f in findings} == {ERROR}


def test_inverting_the_presumption_loses_every_one_of_them(monkeypatch):
    """MUTATION GUARD, first direction: restore the ORIGINAL spelling — exempt
    unless the status reads exactly `ratified` — and all three findings must
    disappear. Measured on the mutant rather than asserted about it, so a
    build that quietly reverted the ruling fails here by name.
    """
    def original_spelling(tree, change):
        text = tree.read(f"openspec/changes/archive/{change}/proposal.md")
        if text is None:
            return True
        return corpus.parse_status(text) != "ratified"

    monkeypatch.setattr(promotion_fidelity, "_is_exempt_from_promotion",
                        original_spelling)
    reverted = _beta()
    assert reverted == [], _rules(reverted)


def test_dropping_the_explicit_draft_check_starts_firing(monkeypatch):
    """MUTATION GUARD, second direction: a presumption with NO explicit-draft
    check at all — everything archived is examined — and both draft packets
    start firing. So the exemption, not the absence of a finding, is what
    keeps C5's class quiet.
    """
    monkeypatch.setattr(promotion_fidelity, "_is_exempt_from_promotion",
                        lambda tree, change: False)
    loud = _beta()
    assert len(_on(loud, "'Never ratified rule'")) == 1, _rules(loud)
    assert len(_on(loud, "'Annotated draft rule'")) == 1, _rules(loud)
    assert len(loud) == 5


def test_declared_standing_reads_the_leading_token_in_both_directions():
    read = promotion_fidelity.declared_standing
    assert read("ratified") == "ratified"
    assert read("ratified (approved at commit 5ace969). Amendment A1") == \
        "ratified"
    assert read("draft") == "draft"
    assert read("draft — archived with `--skip-specs`; never ratified") == \
        "draft"
    assert read("`ratified`") == "ratified"
    assert read("Ratified") == "ratified"
    # an unrecognized word is NOT a standing, so it can never be mistaken for
    # one — it falls through to the presumption like any other archived packet
    assert read("approved") is None
    assert read(None) is None
    assert read("") is None


def test_the_two_standing_sets_exhaust_the_taxonomy():
    """A ninth standing added to `doc_health.TAXONOMY` and forgotten here
    would land in the presumed-ratified bucket in silence, which is the class
    of silence this ruling closed. This test is how it cannot."""
    pre = promotion_fidelity.PRE_RATIFICATION
    beyond = promotion_fidelity.RATIFIED_OR_BEYOND
    assert pre | beyond == TAXONOMY
    assert not (pre & beyond)
    assert "draft" in pre and "ratified" in beyond


# ============================================================================
# 6. THE MEASUREMENT BASIS (ruled 2026-08-24, task 4.1, PR #315)
#
# The nightly measures LIVE MAINS for this family and the pinned checkout for
# every other. The tests below prove the basis is real (a live run reads a
# tree the checkout does not carry), that it degrades LOUDLY rather than
# silently, that it says which basis it used, and that no other family can
# reach the option even by accident.
# ============================================================================


def _tree_of(repo_path: Path, overrides=None) -> dict:
    """The fixture tree as `{path: body}` — one source of truth for both
    halves of the FakeGit ref shim, so its listing and its bodies cannot
    disagree about what `origin/main` contains."""
    tree = {p.relative_to(repo_path).as_posix(): p.read_text(encoding="utf-8")
            for p in sorted(repo_path.rglob("*")) if p.is_file()}
    tree.update(overrides or {})
    return tree


def _live_ctx(overrides=None, resolvable=True, head_stamps=False):
    """A live-main run over the alphaFactory fixture.

    The tie stamps are declared under the REF by default and under HEAD when
    `head_stamps` — which is not a convenience: a fall-back run reads the
    checkout, so its ties belong to HEAD's history, and a shim that answered
    ref-keyed stamps to a checkout-basis run would be pretending the two trees
    are one.
    """
    fixture = FIXTURES / "promotion-fidelity" / REPO
    stamps = (dict(TIE_STAMPS) if head_stamps else
              {(REPO, LIVE, path): stamp
               for (_repo, path), stamp in TIE_STAMPS.items()})
    git = FakeGit(
        refs={(REPO, LIVE): LIVE_SHA} if resolvable else {},
        ref_trees={(REPO, LIVE): _tree_of(fixture, overrides)},
        first_stamps=stamps)
    ctx = make_ctx("promotion-fidelity", git=git)
    ctx.promotion_fidelity_basis = promotion_fidelity.BASIS_LIVE_MAIN
    return ctx


# canon at `origin/main` carrying the requirement the CHECKOUT's canon lacks —
# the shape a lagging pin produces, and the one the ruling was taken over.
_PROMOTED_ON_MAIN = {
    "openspec/specs/notebook-projection/spec.md": (
        (FIXTURES / "promotion-fidelity" / REPO / "openspec" / "specs" /
         "notebook-projection" / "spec.md").read_text(encoding="utf-8")
        + "\n### Requirement: Branch-session notebooks\n"
          "A branch session SHALL project into its own notebook.\n\n"
          "#### Scenario: A session notebook is created and synced\n"
          "- **WHEN** a branch session opens\n"
          "- **THEN** a session notebook MUST be created\n\n"
          "#### Scenario: A session ends\n"
          "- **WHEN** a branch session ends\n"
          "- **THEN** its notebook MUST be retired\n")}


def test_the_default_basis_is_the_pinned_checkout():
    """Every existing caller, and every other family's tree. A Context built
    without the option behaves exactly as it did before the option existed."""
    ctx = _ctx()
    assert promotion_fidelity.requested_basis(ctx) == \
        promotion_fidelity.BASIS_PINNED
    assert [t.basis for _r, _p, t in promotion_fidelity.repo_trees(ctx)] == \
        [promotion_fidelity.BASIS_PINNED]
    assert promotion_fidelity.basis_notes(ctx) == [
        "Basis: the pinned checkout — the same tree every other family "
        "measures."]


def test_the_live_basis_reads_the_ref_and_not_the_checkout():
    """THE LOAD-BEARING ASSERTION. `origin/main` carries a promoted spec the
    checkout does not, so the live run is quiet exactly where the pinned run
    fires. Two runs of one fixture that DISAGREE is what makes the basis a
    basis rather than a label."""
    pinned = _run()
    live = FAMILIES[FAMILY](_live_ctx(overrides=_PROMOTED_ON_MAIN))
    assert len(_on(pinned, "'Branch-session notebooks'")) == 1
    assert _on(live, "'Branch-session notebooks'") == []
    assert len(pinned) == 4 and len(live) == 3, (_rules(pinned), _rules(live))


def test_the_live_basis_names_the_ref_and_sha_it_measured():
    notes = promotion_fidelity.basis_notes(_live_ctx())
    assert notes[0].startswith("Basis: each repository's live `origin/main`")
    assert "RULED for this family alone" in notes[0]
    assert "every other family in this report measures the pinned checkout" \
        in notes[0]
    assert notes[1] == f"- {REPO}: origin/main {LIVE_SHA[:12]}"


def test_an_unfetched_live_main_falls_back_loudly_never_silently():
    """A checkout with no local `origin/main` still gets measured — from its
    own tree — and the note SAYS the repository fell back. Silence would be
    the failure mode this ruling exists to close; an unlabelled fall-back
    would be that failure mode wearing the ruling's name."""
    ctx = _live_ctx(resolvable=False, head_stamps=True)
    assert _rules(FAMILIES[FAMILY](ctx)) == _rules(_run())
    notes = promotion_fidelity.basis_notes(ctx)
    assert notes[0].startswith("Basis: each repository's live `origin/main`")
    assert notes[1] == (f"- {REPO}: FELL BACK to the pinned checkout — "
                        f"origin/main is not present locally")


def test_an_unreadable_live_main_falls_back_loudly_too():
    """`rev-parse` answers but `ls-tree` does not — a shallow or corrupted
    fetch. Same direction, and the note names the sha it could not read."""
    git = FakeGit(refs={(REPO, LIVE): LIVE_SHA})  # no ref_trees entry
    ctx = make_ctx("promotion-fidelity", git=git)
    ctx.promotion_fidelity_basis = promotion_fidelity.BASIS_LIVE_MAIN
    notes = promotion_fidelity.basis_notes(ctx)
    assert notes[1] == (f"- {REPO}: FELL BACK to the pinned checkout — "
                        f"origin/main {LIVE_SHA[:12]} is unreadable")


def test_a_git_shim_that_cannot_read_refs_falls_back_loudly():
    """The oldest FakeGit in this suite, and any Context built by a caller
    that predates the option: the family degrades instead of raising."""
    class NoRefs:
        def first_commit_timestamp(self, repo, relpath, ref=None):
            return TIE_STAMPS.get((repo.name, relpath))

    ctx = make_ctx("promotion-fidelity", git=NoRefs())
    ctx.promotion_fidelity_basis = promotion_fidelity.BASIS_LIVE_MAIN
    assert _rules(FAMILIES[FAMILY](ctx)) == _rules(_run())
    assert promotion_fidelity.basis_notes(ctx)[1] == (
        f"- {REPO}: FELL BACK to the pinned checkout — this run cannot read "
        f"git refs")


def test_an_unknown_basis_value_fails_loudly_instead_of_silently_coercing():
    """Copilot's PR #320 note: `requested_basis` used to coerce any
    unrecognized value BACK to pinned, silently, while `runner.build_context`
    treated the very same raw value as live-main for the headline deviation
    line — so a typo'd or programmatically-built basis could make the report
    CLAIM live-main while the family measured pinned. `normalize_basis` is
    now the one choke point both sides read through, and an unrecognized
    value fails loudly there instead of letting either side guess."""
    ctx = _ctx()
    ctx.promotion_fidelity_basis = "whatever-someone-typed"
    with pytest.raises(ValueError, match="whatever-someone-typed"):
        promotion_fidelity.requested_basis(ctx)


def test_build_context_rejects_an_unknown_basis_before_deciding_the_headline():
    """THE MUTATION CHECK for the choke point above, exercised through
    `runner.build_context` itself rather than through `promotion_fidelity`
    directly — so a regression that re-introduces `build_context`'s OWN
    independent `!= BASIS_PINNED` guess (instead of routing through
    `normalize_basis`) fails this test even though `requested_basis` alone
    would still look correct in isolation.

    Before the fix, this exact call silently built a Context whose headline
    would have claimed "measured against live main" while
    `promotion_fidelity.requested_basis` would separately coerce the same
    value back to pinned for the family's own measurement — the disagreement
    this choke point exists to make impossible. After the fix, `build_context`
    aborts before either side has decided anything.
    """
    from types import SimpleNamespace

    repo = FIXTURES / "promotion-fidelity" / REPO
    with pytest.raises(SystemExit, match="whatever-someone-typed"):
        runner.build_context(SimpleNamespace(
            single_repo=str(repo), repo_root=None, config=None, family=None,
            as_of=AS_OF.isoformat(), routing_strict=False,
            promotion_fidelity_basis="whatever-someone-typed"))


def test_the_tie_break_walks_the_same_ref_the_statements_came_from():
    """A tie decided from HEAD's history while the statements came from
    `origin/main` is two readers of two different trees agreeing by accident.
    Here the ref-keyed stamps are the ONLY ones the shim answers, and the run
    is quiet — which it can only be if the ranker asked for the ref."""
    quiet = FAMILIES[FAMILY](_live_ctx())
    assert _on(quiet, "Contested on one date") == []

    # the same run with the stamps recorded under HEAD instead: the ranker
    # asks for the ref, gets nothing, and falls back to folder-name order
    fixture = FIXTURES / "promotion-fidelity" / REPO
    git = FakeGit(refs={(REPO, LIVE): LIVE_SHA},
                  ref_trees={(REPO, LIVE): _tree_of(fixture)},
                  first_stamps=dict(TIE_STAMPS))
    ctx = make_ctx("promotion-fidelity", git=git)
    ctx.promotion_fidelity_basis = promotion_fidelity.BASIS_LIVE_MAIN
    assert len(_on(FAMILIES[FAMILY](ctx), "Contested on one date")) == 1


def test_the_live_basis_finds_an_archive_the_checkout_does_not_carry():
    """`has_archive` is answered from the TREE, not from the directory: a
    repository whose main carries an archive is in scope even where the
    checked-out pin predates it."""
    ctx = make_ctx("promotion-fidelity-no-archive", git=FakeGit())
    repo = next(iter(ctx.repo_paths))
    assert not (Path(ctx.repo_paths[repo]) / "openspec" / "changes"
                / "archive").is_dir()
    tree = _tree_of(FIXTURES / "promotion-fidelity" / REPO)
    ctx.git = FakeGit(refs={(repo, LIVE): LIVE_SHA},
                      ref_trees={(repo, LIVE): tree},
                      first_stamps={(repo, LIVE, path): stamp
                                    for (_r, path), stamp in
                                    TIE_STAMPS.items()})
    ctx.promotion_fidelity_basis = promotion_fidelity.BASIS_LIVE_MAIN
    out = FAMILIES[FAMILY](ctx)
    assert not isinstance(out, Skip)
    assert len(out) == 4, _rules(out)


def test_only_this_family_can_reach_the_basis_option():
    """STRUCTURAL, because the ruling's constraint is structural: no OTHER
    family's measurement moves. Nothing but this family's own module and the
    runner that plumbs the flag may mention the option at all — a family that
    cannot name it cannot read it.
    """
    package = Path(promotion_fidelity.__file__).parent
    mentions = sorted(p.name for p in package.glob("*.py")
                      if "promotion_fidelity_basis" in
                      p.read_text(encoding="utf-8"))
    assert mentions == ["promotion_fidelity.py", "runner.py"]


def test_the_family_publishes_its_basis_note_for_the_report():
    """The registry the report renders from. One entry, and it is this one."""
    assert list(FAMILY_NOTES) == [FAMILY]
    assert FAMILY_NOTES[FAMILY] is promotion_fidelity.basis_notes


def test_the_live_reader_never_shells_out_for_a_path_the_ref_does_not_carry():
    """The membership guard, pinned by CALL COUNT rather than by result.

    A capability with no promoted spec at all is one of this family's own
    findings, so the miss is the common case, not the exception; and both
    readers return None either way, which means the result can never hold this
    guard. What it costs is one `git show` per miss, per repository, per
    nightly — so the count is the only honest assertion available.
    """
    asked: list[str] = []

    class Counting(FakeGit):
        def show_blob(self, repo, ref, relpath):
            asked.append(relpath)
            return super().show_blob(repo, ref, relpath)

    present = "openspec/specs/present/spec.md"
    git = Counting(ref_trees={(REPO, LIVE): {present: "# present\n"}})
    tree = promotion_fidelity.GitRefTree(
        Path(REPO), git, LIVE, LIVE_SHA, [present])

    assert tree.read(present) == "# present\n"
    assert asked == [present]
    assert tree.read("openspec/specs/never-promoted/spec.md") is None
    assert asked == [present], asked


# ---------------------------------------------- the report says which basis


def _section(text: str, family: str = FAMILY) -> str:
    start = text.index(f"### {family}\n")
    rest = text[start:]
    end = rest.find("\n### ")
    return rest if end < 0 else rest[:end]


def test_the_report_states_the_basis_under_the_family_heading():
    from doc_health import report
    result = runner.run_suite(_ctx(), FAMILY, set())
    text = report.render(AS_OF, result.findings, result.skips, [], [], 0, [],
                         [], family_notes=result.notes)
    section = _section(text)
    assert "Basis: the pinned checkout" in section
    # BEFORE the findings, so the tree is named before anything is read as a
    # verdict about it
    assert section.index("Basis:") < section.index("- [error]")


def test_the_report_states_the_basis_on_a_family_with_no_findings():
    """A clean run is exactly where an unnamed basis misleads: "No findings."
    reads as a verdict, and a reader who does not know which tree produced it
    cannot tell health from a lagging pin."""
    from doc_health import report
    ctx = make_ctx("promotion-fidelity-no-archive", git=FakeGit())
    result = runner.run_suite(ctx, FAMILY, set())
    text = report.render(AS_OF, result.findings, result.skips, [], [], 0, [],
                         [], family_notes=result.notes)
    section = _section(text)
    assert "Basis: the pinned checkout" in section
    assert "Skipped:" in section


def test_a_skipped_family_carries_no_note():
    """`--skip-family` means the family did not run, so there is no basis to
    report — a note about a measurement nobody took is worse than none."""
    result = runner.run_suite(_ctx(), None, {FAMILY})
    assert FAMILY not in result.notes
    assert [s.family for s in result.skips if s.family == FAMILY] == [FAMILY]


def test_the_basis_lines_can_never_be_read_back_as_findings():
    """`report.parse_previous` scans a prior report for ranked-plan lines, and
    a note line that parsed as one would become a phantom finding in the next
    run's regression diff. The bullet shape is close enough to be worth
    pinning rather than assuming."""
    from doc_health import report
    for note in promotion_fidelity.basis_notes(_live_ctx()):
        assert report.PLAN_RE.match(note) is None, note
    keys, contested = report.parse_previous(
        "\n".join(promotion_fidelity.basis_notes(_live_ctx())))
    assert keys == set() and contested == set()


def test_the_cli_flag_reaches_the_family_and_the_headline(tmp_path):
    """END TO END through `runner.main`, because a flag that parses and never
    arrives is the failure this wiring is most likely to have.

    The fixture is not a git repository, so `origin/main` cannot resolve and
    the run takes the documented loud fall-back — which is itself the
    assertion: the report must say so rather than quietly measuring the
    checkout under a live-main banner.
    """
    # copied OUT of this repository's own checkout: run in place, the fixture
    # sits inside a real git repository whose `origin/main` resolves, and the
    # test would measure openxFactory's archive instead of the fixture's
    out = tmp_path / "report.md"
    repo = tmp_path / REPO
    shutil.copytree(FIXTURES / "promotion-fidelity" / REPO, repo)
    rc = runner.main([
        "--single-repo", str(repo),
        "--family", FAMILY,
        "--promotion-fidelity-basis", promotion_fidelity.BASIS_LIVE_MAIN,
        "--as-of", AS_OF.isoformat(),
        "--report-out", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert ("promotion-fidelity measured against each repository's live "
            "origin/main (every OTHER family measures the pinned checkout)"
            in text)
    section = _section(text)
    assert "Basis: each repository's live `origin/main`" in section
    assert f"- {REPO}: FELL BACK to the pinned checkout" in section


def test_the_default_run_says_pinned_and_adds_no_deviation(tmp_path):
    out = tmp_path / "report.md"
    repo = tmp_path / REPO
    shutil.copytree(FIXTURES / "promotion-fidelity" / REPO, repo)
    assert runner.main([
        "--single-repo", str(repo),
        "--family", FAMILY, "--as-of", AS_OF.isoformat(),
        "--report-out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "promotion-fidelity measured against" not in text
    assert "Basis: the pinned checkout" in _section(text)


def test_the_ref_reader_lists_and_reads_the_same_tree_from_a_subdirectory(
        tmp_path):
    """A LISTING AND A READ OF ONE NAME MUST MEAN ONE FILE.

    `git ls-tree` resolves its pathspec against the current prefix and prints
    relative to it; `git show <ref>:<path>` always reads from the tree ROOT.
    Pointed at a subdirectory of a checkout, the untuned pair lists one
    subtree and reads another — and it does so silently, with output that
    looks right. Caught live: the fixture repositories sit inside THIS
    repository, so the first cut of the CLI test listed the fixture's
    `openspec/` and read openxFactory's, and reported a clean run for it.
    """
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "openspec" / "specs" / "root-cap").mkdir(parents=True)
    (tmp_path / "openspec" / "specs" / "root-cap" / "spec.md").write_text(
        "# root capability\n", encoding="utf-8")
    nested = tmp_path / "nested" / "openspec" / "specs" / "nested-cap"
    nested.mkdir(parents=True)
    (nested / "spec.md").write_text("# nested capability\n", encoding="utf-8")
    for args in (["add", "-A"],
                 ["-c", "user.email=t@t", "-c", "user.name=t",
                  "commit", "-qm", "fixture"],
                 ["update-ref", "refs/remotes/origin/main", "HEAD"]):
        subprocess.run(["git", "-C", str(tmp_path), *args], check=True)

    git = corpus.RealGit()
    paths = git.ls_tree_paths(tmp_path / "nested", LIVE, "openspec")
    assert "openspec/specs/root-cap/spec.md" in paths
    assert "nested/openspec/specs/nested-cap/spec.md" not in paths
    for path in paths:
        assert git.show_blob(tmp_path / "nested", LIVE, path) is not None
