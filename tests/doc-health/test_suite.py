"""Suite-level guarantees: determinism, fixture isolation, report schema,
regression matching, and threshold deviation reporting."""

from __future__ import annotations

import ast
import re
import shutil
from datetime import date

import pytest

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
# not surviving: `PLAN_RE` closed the field on the FIRST `"`, so such a row was
# emitted and never parsed back. The finding read as absent from the previous
# report on the NEXT run, which makes a persistent finding look like a fresh
# regression and makes a contested finding's disappearance invisible to
# `uncited_resolutions`.
#
# THE FIRED CASE IS `semantic.py`'s CONTRADICTION ARM, not the shape exercised
# below: `health/reports/2026-07-14.md:267` carries a contested
# semantic-contradiction row whose corpus excerpt embeds a raw `"`, it vanished
# on 07-15, and that run's 18 uncited-resolution errors did not include it. The
# full account is the comment over `_FIELD` in `report.py`.
#
# The shape exercised below is the modified-block-currency arms' — `{title!r}`
# switches to double quotes when a requirement title contains an apostrophe —
# which is a LATENT exposure (that family has emitted no row in 27 reports). It
# is used here because it is the narrowest reproduction of the emit/parse
# asymmetry; the round trip it pins is generator-independent.
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


# --- Ranked-plan path: whitespace-free at emit, unparsed rows reported -------
#
# The sibling of the quoting defect above, and the same shape: `plan_line`
# EMITS `path=<value>` unquoted and `PLAN_RE` READS it back as `(\S+)`, so a
# path carrying a space is emitted into the report and matched by no parser.
# The row is then silently absent from `--previous-report`, which makes a
# persistent finding read as a new regression and hides a contested finding's
# disappearance from `uncited_resolutions`.
#
# THE LIVE INSTANCE is `health/reports/2026-07-09.md:188` — the
# notebook-projection-drift family wrote the SYNTHETIC LABEL
# `path=(lifecycle notebooks)` into the path slot. Reproduced verbatim below,
# because a hand-written approximation of a defect is not the defect.
_LIVE_UNPARSABLE_ROW = (
    "- severity=warning family=notebook-projection-drift repo=xFactory "
    "path=(lifecycle notebooks) "
    'rule="projection dry-run reports 44 pending operations" '
    'action="run the lifecycle notebook sync with --apply"')


def test_the_live_2026_07_09_row_is_the_defect_this_pins():
    """The row really does match no parser — the premise of everything below.
    If a future grammar change made it parse, these tests would be pinning
    nothing and this one says so."""
    assert report.PLAN_RE.match(_LIVE_UNPARSABLE_ROW) is None


def test_plan_line_refuses_a_path_containing_whitespace():
    """Loud at emit, not silent at parse a year later. The finding names the
    family so the fix lands at the construction site, not here."""
    f = Finding(WARNING, "notebook-projection-drift", "xFactory",
                "(lifecycle notebooks)", "44 pending operations", "sync")
    with pytest.raises(ValueError) as excinfo:
        report.plan_line(f)
    message = str(excinfo.value)
    assert "notebook-projection-drift" in message
    assert "(lifecycle notebooks)" in message


def test_plan_line_refuses_a_tab_or_newline_in_the_path():
    r"""`(\S+)` is broken by every whitespace character, not just the space
    that happened to fire."""
    for bad in ("docs/a\tb.md", "docs/a\nb.md", "docs/a b.md"):
        f = Finding(ERROR, "tag-hygiene", "alpha", bad, "r", "a")
        with pytest.raises(ValueError):
            report.plan_line(f)


def test_plan_line_refuses_an_empty_path():
    r"""`(\S+)` needs at least one character; an empty path is unreadable for
    the same reason a spaced one is."""
    f = Finding(ERROR, "tag-hygiene", "alpha", "", "r", "a")
    with pytest.raises(ValueError):
        report.plan_line(f)


def test_the_emit_guard_admits_exactly_what_the_parser_reads_back():
    """Guard and grammar are one rule. Every path the guard accepts must
    round-trip, or the guard is passing rows the parser still drops."""
    for path in ("docs/x.md", "(drafts)", "installs/agenttower",
                 "openspec/changes/c/specs/doc-health/spec.md",
                 "openxFactory/docs/lifecycle-notebook-projection.md",
                 'a"quoted".md', "a\\backslash.md", "—em-dash.md"):
        f = Finding(ERROR, "tag-hygiene", "alpha", path, "r", "a")
        line = report.plan_line(f)
        m = report.PLAN_RE.match(line)
        assert m, f"guard admitted a path the parser drops: {path!r}"
        assert m.group(4) == path


def test_plan_line_is_byte_identical_for_a_whitespace_free_path():
    """The guard adds no bytes. Pinned against the pre-guard format literally
    so a future path-quoting scheme reds here instead of silently rewriting
    the diff of every nightly report."""
    f = Finding(ERROR, "tag-hygiene", "alpha", "docs/x.md",
                "missing status header", "add a Status: header")
    assert report.plan_line(f) == (
        f"- severity={f.severity} family={f.family} repo={f.repo} "
        f"path={f.path} rule=\"{f.rule}\" action=\"{f.action}\" "
        f"class=\"{f.resolution}\"")


def test_an_unparsable_plan_row_is_reported_not_silently_skipped(capsys):
    """`parse_previous` used to `continue` past a row it could not read, so
    the NEXT grammar defect would also take a year and an adversarial review
    to notice. The 2026-07-09 row is now named, with its line number."""
    text = "# Doc-Health Report\n\n## Ranked Plan\n\n" + _LIVE_UNPARSABLE_ROW
    assert report.unparsed_plan_rows(text) == [(5, _LIVE_UNPARSABLE_ROW)]
    report.parse_previous(text)
    err = capsys.readouterr().err
    assert report.UNPARSED_PLAN_ROW_MARKER in err
    assert "line 5" in err
    assert "(lifecycle notebooks)" in err


def test_reporting_an_unparsable_row_does_not_disturb_the_rows_that_parse():
    """The returned key sets are the contract; the report is diagnostic
    beside them, never instead of them."""
    good = ("- severity=error family=tag-hygiene repo=alpha path=docs/x.md "
            'rule="r" action="a" class="contested"')
    text = "\n".join([good, _LIVE_UNPARSABLE_ROW, good])
    keys, contested = report.parse_previous(text)
    assert keys == {("tag-hygiene", "alpha", "docs/x.md")}
    assert contested == {("tag-hygiene", "alpha", "docs/x.md")}
    assert report.unparsed_plan_rows(text) == [(2, _LIVE_UNPARSABLE_ROW)]


def test_a_clean_report_reports_no_unparsed_rows_and_says_nothing(capsys):
    """Silence on the healthy path: the nightly's stderr must not grow a line
    per run, or the signal is worthless when it does fire."""
    f = Finding(ERROR, "tag-hygiene", "alpha", "docs/x.md", "r", "a")
    text = report.render(date(2026, 8, 28), [f], [], [], [], 0, [], [])
    assert report.unparsed_plan_rows(text) == []
    report.parse_previous(text)
    assert capsys.readouterr().err == ""


def test_prose_lines_are_not_mistaken_for_unparsable_plan_rows():
    """Only a line that CLAIMS to be a ranked-plan row is judged as one — the
    per-family bullets and the headline share the report and must not be
    reported as broken grammar."""
    f = Finding(WARNING, "tag-hygiene", "alpha", "docs/x.md", "r", "a")
    text = report.render(date(2026, 8, 28), [f], [], [], [], 0, [], [])
    assert "- [warning] alpha:docs/x.md" in text  # a per-family bullet exists
    assert report.unparsed_plan_rows(text) == []


def _finding_path_literals(source):
    r"""Every statically-known string that reaches the `path` slot of a
    `Finding(...)` in one module, as `(lineno, text)`.

    THREE SPELLINGS, because a rule that only reads one of them is a rule a
    refactor walks straight through: the literal in the call, an f-string's
    literal parts, and a module-level `NAME = "..."` constant named in the
    slot — which is exactly how the notebook-projection path is spelled after
    this change, so the narrow version of this check would have gone green on
    a reverted label. Anything computed at run time is out of reach here and
    is `plan_line`'s guard to catch.
    """
    tree = ast.parse(source.read_text(encoding="utf-8"))
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(
                node.value, ast.Constant) and isinstance(
                    node.value.value, str):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    constants[target.id] = node.value.value
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        called = getattr(node.func, "id", None) or getattr(
            node.func, "attr", None)
        if called != "Finding":
            continue
        arg = node.args[3] if len(node.args) >= 4 else next(
            (k.value for k in node.keywords if k.arg == "path"), None)
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            out.append((node.lineno, arg.value))
        elif isinstance(arg, ast.JoinedStr):
            out += [(node.lineno, v.value) for v in arg.values
                    if isinstance(v, ast.Constant) and isinstance(v.value, str)]
        elif isinstance(arg, ast.Name) and arg.id in constants:
            out.append((node.lineno, constants[arg.id]))
    return out


def test_no_family_writes_a_whitespace_bearing_path_literal():
    """The durable form of the grep this change was found by: a path that a
    family spells out in its own source may not carry whitespace.

    STATIC, because the family that DID violate it cannot be caught any other
    way: notebook-projection-drift only emits when `nlm` is authenticated and
    an aggregation checkout is in scope, so it renders no row in any fixture
    run, in the self-gate, or in CI. `plan_line`'s guard is the run-time net;
    this is the one that fires in the pull request that introduces the defect.
    """
    offenders = []
    for source in sorted(
            (REPO_ROOT / "scripts" / "doc_health").rglob("*.py")):
        for lineno, literal in _finding_path_literals(source):
            if re.search(r"\s", literal):
                offenders.append(f"{source.name}:{lineno}: {literal!r}")
    assert offenders == []


def test_the_whitespace_literal_check_reads_a_constant_in_the_path_slot(
        tmp_path):
    """The check above is only worth its line count if it sees the spelling
    the tree actually uses — a module constant, not an inline literal. Written
    against a module that DOES offend, so a reader can see the check catch
    something rather than take an empty list on faith."""
    module = tmp_path / "family.py"
    module.write_text(
        'LABEL = "(lifecycle notebooks)"\n'
        'REAL = "docs/real.md"\n'
        'a = Finding(WARNING, "fam", "repo", LABEL, "r", "a")\n'
        'b = Finding(WARNING, "fam", "repo", REAL, "r", "a")\n'
        'c = Finding(WARNING, "fam", "repo", "docs/inline.md", "r", "a")\n'
        'd = Finding(WARNING, "fam", "repo", f"docs/{x}/a b.md", "r", "a")\n',
        encoding="utf-8")
    found = [text for _, text in _finding_path_literals(module)]
    assert found == ["(lifecycle notebooks)", "docs/real.md",
                     "docs/inline.md", "docs/", "/a b.md"]
    assert [t for t in found if re.search(r"\s", t)] == [
        "(lifecycle notebooks)", "/a b.md"]


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
