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

3. **The advisory launch is pinned structurally** (`test_launch_is_advisory`
   and its siblings), not left to the severity that happens to be written on
   a finding. Decision 3 of the change is "report-only at launch", and both
   halves of it — WARNING severity AND absence from `FAMILY_RESOLUTION` —
   are asserted, because enforcement can arrive through either.

4. **The tie-break is load-bearing**, proven by running the SAME fixture
   twice: once with archive-commit order available and once without. The
   two runs disagree, which is what makes the ordering rule a rule rather
   than a comment.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from conftest import FIXTURES, FakeGit, make_ctx

from doc_health import Skip, WARNING
from doc_health import promotion_fidelity
from doc_health.families import FAMILIES, FAMILY_RESOLUTION
from doc_health.promotion_fidelity import FAMILY

REPO = "alphaFactory"

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
    writers = promotion_fidelity._collect_writers(repo_path)
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


# ------------------------------------------------- 3. the advisory launch, pinned


def test_launch_is_advisory_by_severity():
    """Decision 3, first half. Every finding is WARNING, so `--fail-on
    error` and `--fail-on critical` (whose gates are `{CRITICAL, ERROR}` and
    `{CRITICAL}`) cannot red on this family."""
    findings = _run()
    assert findings, "the advisory claim is vacuous over an empty run"
    assert {f.severity for f in findings} == {WARNING}
    assert promotion_fidelity._LAUNCH_SEVERITY == WARNING


def test_launch_is_advisory_by_resolution_class():
    """Decision 3, second half, and the one that is easy to lose.

    `report.uncited_resolutions` turns a CONTESTED finding that vanishes
    between reports into an ERROR under the `uncited-resolution` family. A
    `contested` entry here would therefore red the nightly the first time
    anyone actually promoted a delta this family had reported — enforcement
    arriving through the back door on the run that proves the advisory
    launch worked. The flip raises severity and adds this entry TOGETHER.
    """
    assert FAMILY not in FAMILY_RESOLUTION
    assert {f.resolution for f in _run()} == {"auto-fixable"}


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
