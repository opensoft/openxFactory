"""Suite-level guarantees: determinism, fixture isolation, report schema,
regression matching, and threshold deviation reporting."""

from __future__ import annotations

import shutil
from datetime import date

from conftest import AS_OF, FIXTURES, REPO_ROOT, FakeGit, make_ctx

from doc_health import CRITICAL, ERROR, WARNING, DEFAULT_THRESHOLDS, Finding
from doc_health import catalog_dispatch, corpus, report, runner
from doc_health.families import FAMILIES


def test_determinism_identical_runs():
    a = FAMILIES["tag-hygiene"](make_ctx("tag-hygiene"))
    b = FAMILIES["tag-hygiene"](make_ctx("tag-hygiene"))
    assert [f.__dict__ for f in sorted(a, key=Finding.sort_key)] == \
           [f.__dict__ for f in sorted(b, key=Finding.sort_key)]


def test_real_repo_scan_excludes_fixtures():
    paths = corpus.iter_doc_paths(REPO_ROOT)
    assert paths, "governed corpus should not be empty"
    assert not [p for p in paths if p.as_posix().startswith("tests/")], \
        "fixture corpora must never enter a real scan"


def test_report_conforms_to_contract_schema():
    findings = [Finding(ERROR, "status-validity", "alpha", "docs/x.md",
                        "missing status header", "add a Status: header")]
    docs = make_ctx("status-validity").docs
    text = report.render(date(2026, 7, 9), findings, [], [], docs, 100, [], [])
    assert text.startswith("# Doc-Health Report — 2026-07-09")
    for element in ("Status: record", "Kind: report", "Canon share by words",
                    "## Per-Stage Counts", "## Findings By Family",
                    "## Ranked Plan"):
        assert element in text, element
    # Ranked-plan items are machine-parseable (severity, repo, path, action).
    lines = [l for l in text.splitlines() if l.startswith("- severity=")]
    assert len(lines) == 1
    m = report.PLAN_RE.match(lines[0])
    assert m and m.group(1) == ERROR and m.group(3) == "alpha"


def test_regression_matching_by_family_and_path():
    prev = report.render(
        date(2026, 7, 8),
        [Finding(ERROR, "tag-hygiene", "alpha", "docs/old.md", "r", "a")],
        [], [], [], 0, [], [])
    keys, contested = report.parse_previous(prev)
    now = [
        Finding(ERROR, "tag-hygiene", "alpha", "docs/old.md", "r", "a"),
        Finding(CRITICAL, "standard-backing", "alpha", "docs/new.md", "r", "a"),
        Finding(WARNING, "submodule-pin-drift", "x", "sub", "r", "a"),
    ]
    new = report.regressions(now, keys)
    assert [f.path for f in new] == ["docs/new.md"]  # persistent + warning excluded


def test_no_previous_report_is_baseline():
    findings = [Finding(CRITICAL, "standard-backing", "a", "p", "r", "a")]
    assert report.regressions(findings, None) == []


def test_threshold_override_is_reported_as_deviation():
    thresholds = dict(DEFAULT_THRESHOLDS, draft_warning_days=10)
    git = FakeGit(last_dates={("alpha", "docs/good.md"): date(2026, 6, 20)})
    ctx = make_ctx("status-validity", git=git, thresholds=thresholds)
    got = FAMILIES["staged-candidate-aging"](ctx)
    assert any(f.severity == WARNING and "draft without transition" in f.rule
               for f in got)  # 19 days >= overridden 10
    text = report.render(date(2026, 7, 9), got, [], [], ctx.docs, 0,
                         ["threshold draft_warning_days=10 (default 60)"], [])
    assert "Non-default configuration" in text
    assert "draft_warning_days=10" in text


def test_uncited_contested_resolution_becomes_finding():
    prev = report.render(
        date(2026, 7, 8),
        [Finding(ERROR, "location-conformance", "alpha", "docs/reg.md",
                 "r", "a", resolution="contested")],
        [], [], [], 0, [], [])
    keys, contested = report.parse_previous(prev)
    assert contested == {("location-conformance", "alpha", "docs/reg.md")}
    # vanished without disposition -> new error finding
    got = report.uncited_resolutions([], contested, dispositions=set())
    assert [(f.family, f.path) for f in got] == [
        ("uncited-resolution", "docs/reg.md")]
    # vanished WITH disposition -> clean
    assert report.uncited_resolutions(
        [], contested,
        dispositions={("location-conformance", "alpha", "docs/reg.md")}) == []


# --- Ranked-plan field quoting round-trip ------------------------------------
#
# `plan_line` EMITS a row and `PLAN_RE`/`parse_previous` READ one back; a
# finding whose rule or action text contains the field delimiter itself must
# survive that round trip, or `--previous-report` silently forgets it. It was
# not surviving: `PLAN_RE` closed the field on the FIRST `"`, so a row like
# `rule="active MODIFIED block for "Brett's ruling" omits ..."` — the shape
# every modified-block-currency arm writes when the requirement title it
# quotes with `{title!r}` contains an apostrophe, because `repr()` then
# switches to double quotes — was emitted and never parsed back. The finding
# read as absent from the previous report on the NEXT run, which makes a
# persistent finding look like a fresh regression and makes a contested
# finding's disappearance invisible to `uncited_resolutions`.
#
# The rule text below is a real arm's, verbatim in shape.
_QUOTED_TITLE_RULE = (
    "active MODIFIED block for \"Brett's ruling\" omits 1 of the 2 "
    "scenarios in the promoted requirement")


def test_a_rule_containing_a_double_quote_round_trips_through_the_plan():
    f = Finding(ERROR, "modified-block-currency", "openxFactory",
                "openspec/changes/c/specs/doc-health/spec.md",
                _QUOTED_TITLE_RULE, "carry the missing scenario")
    text = report.render(date(2026, 8, 28), [f], [], [], [], 0, [], [])
    keys, _ = report.parse_previous(text)
    assert f.match_key() in keys, "the emitted row did not parse back"
    # ... and the next run therefore does NOT report it as a new regression.
    assert report.regressions([f], keys) == []


def test_an_action_containing_a_double_quote_round_trips_through_the_plan():
    f = Finding(ERROR, "tag-hygiene", "alpha", "docs/x.md",
                "marker missing a change= attribute",
                'add change="add-thing" to the marker')
    text = report.render(date(2026, 8, 28), [f], [], [], [], 0, [], [])
    keys, _ = report.parse_previous(text)
    assert f.match_key() in keys
    assert report.regressions([f], keys) == []


def test_a_contested_quoted_rule_round_trips_into_the_contested_set():
    f = Finding(ERROR, "modified-block-currency", "openxFactory",
                "openspec/changes/c/specs/doc-health/spec.md",
                _QUOTED_TITLE_RULE, "carry the missing scenario",
                resolution="contested", disposer='the "gate" convener')
    text = report.render(date(2026, 8, 28), [f], [], [], [], 0, [], [])
    keys, contested = report.parse_previous(text)
    assert contested == {f.match_key()}
    # vanished with no disposition -> the uncited-resolution error is raised
    assert [g.family for g in report.uncited_resolutions(
        [], contested, dispositions=set())] == ["uncited-resolution"]


def test_quote_heavy_and_backslash_bearing_fields_round_trip():
    for rule, action in (
            ('"""', 'a'),
            ('a \\ b', 'c \\ d'),
            ('ends with a backslash \\', 'starts "quoted"'),
            ('\\"', '"\\'),
            ('every "word" is "quoted" here', 'and "so" is the action')):
        f = Finding(ERROR, "tag-hygiene", "alpha", "docs/x.md", rule, action)
        line = report.plan_line(f)
        m = report.PLAN_RE.match(line)
        assert m, f"unparsed: {line!r}"
        assert report.unescape_field(m.group(5)) == rule
        assert report.unescape_field(m.group(6)) == action
        keys, _ = report.parse_previous(line)
        assert f.match_key() in keys


def test_plan_line_is_byte_identical_for_fields_with_no_quote_or_backslash():
    """The escape is invisible to every row that needs none — the whole
    corpus of existing reports. Pinned against the pre-escape format
    literally, so a future escaping scheme that reshapes ordinary rows
    (percent-encoding, `repr()` quoting) reds here rather than silently
    rewriting the diff of every nightly report."""
    f = Finding(ERROR, "tag-hygiene", "alpha", "docs/x.md",
                "missing status header", "add a Status: header",
                resolution="contested", disposer="alpha authority")
    assert report.plan_line(f) == (
        f"- severity={f.severity} family={f.family} repo={f.repo} "
        f"path={f.path} rule=\"{f.rule}\" action=\"{f.action}\" "
        f"class=\"{f.resolution}\" disposer=\"{f.disposer}\"")


def test_parse_previous_still_reads_rows_from_the_pre_escape_emitter():
    """Backward compatibility: yesterday's report was written by the old
    emitter, and tonight's run diffs against it."""
    old = ("- severity=error family=tag-hygiene repo=alpha path=docs/x.md "
           'rule="missing status header" action="add a Status: header" '
           'class="contested" disposer="alpha authority"')
    keys, contested = report.parse_previous(old)
    assert keys == {("tag-hygiene", "alpha", "docs/x.md")}
    assert contested == {("tag-hygiene", "alpha", "docs/x.md")}


def _fixture_catalog_meta(**overrides):
    fields = {
        "snapshot_refs": [
            "health/document-catalog/runs/2026-07-09/abc/alpha.yaml"],
        "total_docs": 10, "cataloged": 6,
        "state_counts": {"pending": 2, "suggested": 3, "reviewed": 1,
                        "overridden": 0, "unclassified": 0,
                        "policy_blocked": 0},
        "new_count": 2, "changed_count": 1, "deleted_count": 1,
        "stale_count": 1,
        "rejected_count": 1, "inventory_version": "inv-abc123",
        "taxonomy_digest": "deadbeef",
        "classifier_version": "document-cataloger/1",
        "prompt_version": 1, "model": "claude-sonnet-5",
        "recommendation_refs": [
            "health/document-catalog/recommendations/2026-07-09/CATJOB-1.yaml"],
        "skipped_reason": "child_timeout",
        "baseline_progress": {"cataloged": 9, "total": 15,
                              "repos_complete": 1, "repos_total": 2,
                              "percent": 60.0, "complete": False},
        "pending_aging": {"warning": 2, "error": 1},
        "deviations": ["catalog shard budget=10 (default 25)"],
    }
    fields.update(overrides)
    return catalog_dispatch.CatalogMeta(**fields)


def test_catalog_meta_report_section_renders_the_full_field_table():
    # T020/T022: every data-model.md CatalogMeta field renders somewhere in
    # the "## Document Catalog" section, positioned before Findings By
    # Family (mirrors "## Semantic Sweep"'s existing placement/style).
    meta = _fixture_catalog_meta()
    text = report.render(date(2026, 7, 9), [], [], [], [], 0, [], [],
                         catalog_meta=meta)
    assert "## Document Catalog" in text
    assert "Skipped: child_timeout" in text
    assert ("snapshots: health/document-catalog/runs/2026-07-09/abc/"
           "alpha.yaml") in text
    assert "coverage: 6 of 10 docs cataloged" in text
    assert ("facet states: pending=2, suggested=3, reviewed=1, "
           "overridden=0, unclassified=0, policy_blocked=0") in text
    assert ("changes: 2 new, 1 changed, 1 deleted, 1 stale, "
           "1 rejected") in text
    assert "inventory: inv-abc123, taxonomy digest deadbeef" in text
    assert ("classifier: document-cataloger/1, prompt contract v1, "
           "model claude-sonnet-5") in text
    assert ("recommendation evidence: health/document-catalog/"
           "recommendations/2026-07-09/CATJOB-1.yaml") in text
    assert ("baseline progress: 9/15 entries (60.0%) across "
           "1/2 repositories") in text
    assert "pending-aging: warning=2, error=1" in text
    assert ("non-default configuration: catalog shard budget=10 "
           "(default 25)") in text
    assert text.index("## Document Catalog") < \
        text.index("## Findings By Family")


def test_catalog_meta_omits_optional_sections_when_absent():
    meta = _fixture_catalog_meta(skipped_reason=None, baseline_progress=None,
                                 deviations=[], recommendation_refs=[])
    text = report.render(date(2026, 7, 9), [], [], [], [], 0, [], [],
                         catalog_meta=meta)
    assert "Skipped:" not in text
    assert "baseline progress:" not in text
    assert "non-default configuration:" not in text
    assert "recommendation evidence: (none)" in text


def test_catalog_meta_never_leaks_into_the_ranked_plan():
    # FR-012 hard invariant: CatalogMeta is read-only render input -- no
    # recommendation-derived content (job/recommendation refs, skip reason,
    # model id) ever becomes a Ranked Plan line, even when real Findings
    # from an UNRELATED family are also present in the same report.
    meta = _fixture_catalog_meta()
    findings = [Finding(ERROR, "tag-hygiene", "alpha", "docs/x.md",
                        "missing status header", "add a Status: header")]
    text = report.render(date(2026, 7, 9), findings, [], [], [], 0, [], [],
                         catalog_meta=meta)
    assert "## Document Catalog" in text  # the section itself did render
    plan_lines = [l for l in text.splitlines() if l.startswith("- severity=")]
    assert len(plan_lines) == 1  # only the one real Finding
    m = report.PLAN_RE.match(plan_lines[0])
    assert m and m.group(2) == "tag-hygiene" and m.group(3) == "alpha"
    for field in (meta.model, meta.skipped_reason, *meta.recommendation_refs,
                 *meta.snapshot_refs, meta.inventory_version,
                 meta.taxonomy_digest):
        assert not any(field in l for l in plan_lines)


def test_unavailable_semantic_family_does_not_fake_a_resolution():
    contested = {
        ("semantic-normative-prose", "alpha", "docs/a.md"),
        ("location-conformance", "alpha", "docs/reg.md"),
    }
    got = report.uncited_resolutions(
        [], contested, dispositions=set(),
        unavailable_families={"semantic-normative-prose",
                              "semantic-contradiction"})
    assert [(finding.family, finding.path) for finding in got] == [
        ("uncited-resolution", "docs/reg.md")]


# ---------------------------------------------------------- run-configuration
#
# PR #325 review (add-promotion-fidelity-check task 4.2): `unavailable_families`
# was populated from semantic/readiness/neutrality availability only, never
# from run CONFIGURATION — a `--skip-family` entry, or a `--family` run's
# implicit omission of every other family. `report.uncited_resolutions`
# treats a family absent from `unavailable_families` as having genuinely run
# and found nothing, so a run that skipped a CONTESTED family manufactured a
# spurious `uncited-resolution` ERROR for every one of that family's prior
# contested findings. `promotion-fidelity`'s CONTESTED flip (this branch)
# widened the exposure, but it predates the flip — the same hazard applied
# to `record-immutability`, `location-conformance`, etc. on any run that
# skipped one of them.
#
# `location-conformance`'s existing fixture (a "brainstorm" doc outside
# ideation/brainstorm/) is reused for all three tests below via `runner.main`
# end to end, because the fix lives in `runner.main`'s CLI wiring, not in
# `report.uncited_resolutions` itself (already covered above).

def _previous_report_with_contested_finding():
    finding = Finding(
        ERROR, "location-conformance", "alpha", "docs/stray.md",
        "brainstorm document outside ideation/brainstorm/",
        "move it under ideation/brainstorm/ or change its status",
        resolution="contested")
    return report.render(date(2026, 7, 8), [finding], [], [], [], 0, [], [])


def test_skip_family_run_never_manufactures_an_uncited_resolution(tmp_path):
    repo = tmp_path / "alpha"
    shutil.copytree(FIXTURES / "location-conformance" / "alpha", repo)
    prev = tmp_path / "previous.md"
    prev.write_text(_previous_report_with_contested_finding(),
                    encoding="utf-8")

    out = tmp_path / "report.md"
    rc = runner.main([
        "--single-repo", str(repo),
        "--skip-family", "location-conformance",
        "--as-of", AS_OF.isoformat(),
        "--previous-report", str(prev),
        "--report-out", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    # The violation is still sitting right there in the repo — skipping the
    # family must suppress the manufactured resolution regardless of what
    # the corpus actually contains, because a skipped family never looked.
    assert "family=uncited-resolution" not in text


def test_single_family_run_never_manufactures_an_uncited_resolution(tmp_path):
    """A `--family` run executes ONLY the named family (`run_suite`'s
    `only_family` branch silently `continue`s past every other one), so it
    must suppress exactly like `--skip-family` for every family it did not
    run — proven here by selecting an unrelated family."""
    repo = tmp_path / "alpha"
    shutil.copytree(FIXTURES / "location-conformance" / "alpha", repo)
    prev = tmp_path / "previous.md"
    prev.write_text(_previous_report_with_contested_finding(),
                    encoding="utf-8")

    out = tmp_path / "report.md"
    rc = runner.main([
        "--single-repo", str(repo), "--family", "tag-hygiene",
        "--as-of", AS_OF.isoformat(),
        "--previous-report", str(prev),
        "--report-out", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "family=uncited-resolution" not in text


def test_full_run_still_fires_uncited_resolution_when_genuinely_resolved(
        tmp_path):
    """The mechanism the fix must NOT break: a family that actually RAN and
    found nothing for a path previously contested still owes a citation."""
    repo = tmp_path / "alpha"
    shutil.copytree(FIXTURES / "location-conformance" / "alpha", repo)
    (repo / "docs" / "stray.md").unlink()  # the violation is genuinely gone
    prev = tmp_path / "previous.md"
    prev.write_text(_previous_report_with_contested_finding(),
                    encoding="utf-8")

    out = tmp_path / "report.md"
    rc = runner.main([
        "--single-repo", str(repo),
        "--as-of", AS_OF.isoformat(),
        "--previous-report", str(prev),
        "--report-out", str(out)])
    assert rc == 0
    text = out.read_text(encoding="utf-8")
    assert "family=uncited-resolution" in text
