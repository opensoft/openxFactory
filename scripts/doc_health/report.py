"""Report generation and the regression diff.

The report schema is owned by the openxFactory `doc-health` contract:
dated Markdown, `Status: record` + `Kind: report`, canon-share headline,
per-stage counts, per-family sections, machine-parseable ranked plan.
This module renders findings into that schema; it defines no schema of
its own.
"""

from __future__ import annotations

import re
import sys
from datetime import date

from . import CRITICAL, ERROR, FAMILY_IDS, Finding, SEVERITY_RANK

# A free-text ranked-plan field: everything up to the closing `"`, with `\"`
# and `\\` admitted inside it. The naive `[^"]*` this replaces closed the field
# on the FIRST `"` and so could not read back a row it had itself emitted —
# any finding whose rule or action text contains a double quote. Such a row was
# emitted by `plan_line`, never matched by `PLAN_RE`, and silently dropped from
# every `--previous-report` comparison, which makes a persistent finding read as
# a new regression on the next run and hides a contested finding's disappearance
# from `uncited_resolutions`.
#
# THIS ALREADY FIRED IN PRODUCTION, and the family it fired for is NOT the one a
# reader would guess. The generator is `semantic.py`'s contradiction arm, which
# wraps a corpus excerpt in curly quotes —
# `rule = f"[id={pid}] confidence={confidence} “{excerpt}”"` — so a raw `"`
# inside the excerpt lands inside the field. `health/reports/2026-07-14.md:267`
# carries one: a `contested` `semantic-contradiction` finding on
# `openxFactory:docs/xfactory-domain-factory-model.md` whose excerpt quotes
# `"In this domain, customer Hermes is Managed System or Tenant Hermes."`. On
# 2026-07-15 that finding VANISHED — and the 18 uncited-resolution errors that
# run raised did not include it, because the 07-14 row had never parsed into the
# contested set. The citation requirement simply did not apply to it.
#
# The modified-block-currency arms are the OTHER exposure — `{title!r}` switches
# to DOUBLE quotes when a requirement title contains an apostrophe — but that is
# a latent one: that family has emitted no row at all in the 27 dated reports
# written to date. Named here so a reader does not go looking for the fired case
# there.
#
# THE REPAIR IS FORWARD-ONLY, and deliberately so. The 07-14 row carries a RAW
# `"` inside the field, and no parser can accept a raw `"` as field CONTENT
# while `"` is also the delimiter — the grammar would be ambiguous. So that row
# does not parse after this change either; what changes is that a row emitted
# from HERE ON carries `\"` and does parse. Both parsers, old and new, accept
# exactly the same 20,997 of the 20,999 historical rows and agree on the key of
# every one of them (measured across `health/reports/*.md`).
#
# THE OTHER HISTORICAL UNPARSED ROW IS A DIFFERENT DEFECT and is NOT fixed here:
# `health/reports/2026-07-09.md:188` writes `path=(lifecycle notebooks)`, and
# `path=(\S+)` cannot match a path containing a space. Same regex, unrelated
# cause, own repair — recorded so the next reader does not read this change as
# having cleared the whole class.
#
# Emit and parse are now symmetric (`escape_field` / `unescape_field`).
_FIELD = r'((?:[^"\\]|\\.)*)'

# THE RANKED-PLAN PATH FIELD, and the whole of its grammar. Unlike `rule=` and
# `action=` above, `path=` carries no delimiters: it starts after `path=` and
# ends at the space before `rule=`, so it is exactly "one or more
# non-whitespace characters" and can be nothing else.
#
# ISSUE #474, THE SIBLING OF THE QUOTING DEFECT ABOVE, AND IT ALSO FIRED. The
# notebook-projection-drift family wrote a SYNTHETIC LABEL into the path slot —
# `health/reports/2026-07-09.md:188` reads `path=(lifecycle notebooks)` — and
# that space makes the row match no parser, old or new. Emitted into the
# report, read back by nothing: absent from `regressions()` (so the finding
# reads as NEW on the next run) and absent from the contested set (so
# `uncited_resolutions` cannot notice it vanish). Harmless in that instance
# (a warning, not contested) and not harmless as a mechanism.
#
# THE REPAIR IS AT THE EMIT SIDE, NOT IN THE GRAMMAR. Quoting `path=` the way
# #472 quoted `rule=` would reshape all 20,999 ranked-plan rows written to date
# and buy nothing: no legitimate value for this field contains whitespace. A
# path is a repository-relative file path — every tracked file in every one of
# the twelve checkouts in the workspace is whitespace-free, measured — and a
# finding about something that is not one file names it with a slug. So
# `plan_line` REFUSES a path this pattern cannot read, and the one label that
# violated it became a real path (`families.fam_notebook_projection_drift`).
#
# ONE PATTERN, TWO USES, so the guard and the grammar cannot drift apart: the
# regex below interpolates it, and `plan_line`'s guard fullmatches it.
_PATH = r"\S+"
_PATH_RE = re.compile(_PATH)

PLAN_RE = re.compile(
    r"^- severity=(\w+) family=([\w-]+) repo=(\S+) path=(" + _PATH + r") "
    r'rule="' + _FIELD + r'" action="' + _FIELD + r'"'
    r'(?: class="([\w-]+)")?'
    r'(?: disposer="' + _FIELD + r'")?$')

# A line that CLAIMS to be a ranked-plan row. `parse_previous` judges a line by
# this prefix before it reports the line as unreadable, so the report's prose,
# its per-family bullets, and its tables are never mistaken for broken grammar.
PLAN_ROW_PREFIX = "- severity="

# Fixed, greppable, on stderr — the convention `ideation_readiness`'s
# ROOT_FALLBACK_MARKER already sets for a diagnostic a run must be searchable
# for after the fact.
#
# THE SUMMARY MARKER IS NOT A SUPERSTRING OF THE ROW MARKER, deliberately. The
# first spelling of it was `[ranked-plan] unparsed rows: N`, which contains
# `[ranked-plan] unparsed row` — so `grep -c` for the row marker counted N+1
# and the diagnostic lied about its own subject. `test_the_two_unparsed_markers
# _are_countable_apart` pins the disjointness.
UNPARSED_PLAN_ROW_MARKER = "[ranked-plan] unparsed row"
UNPARSED_PLAN_ROW_TOTAL_MARKER = "[ranked-plan] unparsed-row total"

# A path `plan_line` had to repair to keep the row readable (see `plan_line`).
SANITIZED_PATH_MARKER = "[ranked-plan] sanitized path"

# ISSUE #342: the repo identity a report was PRODUCED under, stamped in the
# header beside `Status:`/`Kind:` so a `--previous-report` comparison can
# refuse a baseline built under a different one.
#
# THE MECHANISM THIS CLOSES. Finding identity is `(family, repo, path)`
# (`Finding.match_key`), and `repo` for a `--single-repo <path>` run is the
# directory BASENAME (`runner.build_context`) — nothing a written report ever
# recorded and nothing a read-back ever checked. Point `--previous-report` at
# a baseline built in a worktree named `base-wt` and diff it against a run
# named `openxFactory`: every key misses, so `regressions()` reads every
# current critical/error finding as new and `uncited_resolutions()` reads
# every baseline contested finding as vanished-without-citation — 36 phantom
# "regressions" and 23 phantom `uncited-resolution` errors in the issue's own
# reproduction, with exit code 0 throughout. A benign operator path slip
# reported in the vocabulary of the family's most serious findings.
#
# THE STAMP IS THE REPO-SLUG SET THE RUN COVERED, not a single name — an
# aggregation run covers many. One line, `key: value` like `Status:`/`Kind:`
# immediately above it in `render()`, sorted so the line is deterministic and
# comma-separated so it reads like the "scope limited to single repo X"
# deviation line already beside it. `(none)` is the explicit empty-set
# spelling — never an absent line, which is reserved for "not stamped at
# all" (see `parse_repo_identity`).
REPO_IDENTITY_PREFIX = "Repo-Identity: "
REPO_IDENTITY_NONE = "(none)"
REPO_IDENTITY_RE = re.compile(
    r"^" + re.escape(REPO_IDENTITY_PREFIX) + r"(.*)$", re.MULTILINE)

# What a whitespace run in a path becomes, and what an empty path becomes.
_WHITESPACE_RUN = re.compile(r"\s+")
EMPTY_PATH_PLACEHOLDER = "(empty-path)"


def sanitize_path(path: object) -> str:
    """A ranked-plan path that `PLAN_RE` can read, from one that it cannot.

    DETERMINISTIC, so the repaired key is STABLE across runs: the same bad
    path sanitizes to the same string every night, which is what lets the
    finding participate in the regression comparison at all instead of
    flickering. Each whitespace RUN collapses to a single `_` (so
    `docs/Meeting  Notes.md` and `docs/Meeting\tNotes.md` agree), and only a
    genuinely EMPTY path — which has no run to collapse — becomes
    `EMPTY_PATH_PLACEHOLDER`, rather than an empty field the parser would also
    reject. One rule and one exception; an all-whitespace path is one run and
    collapses to `_` like any other.
    """
    text = path if isinstance(path, str) else str(path)
    return _WHITESPACE_RUN.sub("_", text) or EMPTY_PATH_PLACEHOLDER


def escape_field(value: str) -> str:
    """Make `value` safe between the `"` delimiters of a ranked-plan field.

    BYTE-IDENTICAL for any value containing neither `"` nor `\\`, so the escape
    is invisible in the nightly report diff.

    THE ONE ACCEPTED REGRESSION IN READING OLD REPORTS, stated because it is
    unavoidable rather than overlooked: a row written by the PRE-ESCAPE emitter
    whose rule, action, or disposer text ENDS with a literal `\\` now parses as
    an escaped closing quote and the row is silently dropped. `PLAN_RE` cannot
    tell that row from a new-emitter row, and no reading of the old grammar
    distinguishes them, so no parser can be compatible with both. Measured
    before accepting it: ZERO such rows exist across the 20,999 ranked-plan rows
    in `health/reports/`, and none of those rows contains a backslash at all.
    """
    return value.replace("\\", "\\\\").replace('"', '\\"')


def unescape_field(value: str) -> str:
    """Inverse of `escape_field` over a `_FIELD` capture.

    NEW-EMITTER OUTPUT ONLY. It strips EVERY backslash it does not find doubled,
    so over a field captured from a pre-escape report it corrupts rather than
    round-trips: a legacy `C:\\temp\\x` reads back as `C:tempx`. That is
    inconsequential today — no production caller unescapes a field at all
    (`parse_previous` reads only severity, family, repo, path, and class) — and
    it is the reason this is a separate function instead of something
    `parse_previous` applies on everyone's behalf. A future caller that must
    read field TEXT out of an archived report needs a version-aware reader, not
    this one.
    """
    return re.sub(r"\\(.)", r"\1", value)


def plan_line(f: Finding, *, strict: bool = False) -> str:
    r"""Render one ranked-plan row, REPAIRING a path the grammar cannot read.

    ISSUE #474. A path carrying whitespace produces a row `PLAN_RE` cannot read
    back, and the old behaviour was to write it anyway: the report looked
    complete, and the row quietly took no part in any `--previous-report`
    comparison from then on. It took a year and an adversarial review to notice
    the one instance.

    NORMALIZE AND CONTINUE, WHICH IS WHAT THE PRECEDENT ACTUALLY DOES. An
    earlier draft of this raised unconditionally and cited `recorded_rel` for
    it; that citation was wrong, and the review of PR #477 caught it —
    `recorded_rel` REPAIRS the spelling of a recorded path and carries on
    precisely so a reader is never stopped by an alphabet. The stakes here make
    that the right shape rather than merely the consistent one: the path slot
    is fed from `corpus.iter_doc_paths`, which rglobs every `.md` in the
    checkout, so a governance file named `docs/Meeting Notes 2026.md` is enough
    to reach this code. Raising would abort `render()` BEFORE `--report-out` is
    written — the nightly's `Run doc-health suite` step has no
    `continue-on-error`, so there would be no report and no artifact at all
    until somebody renamed the file, and the run after that would baseline
    against a stale report. A repaired row that participates beats a whole
    report that does not exist.

    SO THE DEFAULT SANITIZES AND SAYS SO: each whitespace run becomes `_`, the
    row is written, and ONE line goes to stderr behind `SANITIZED_PATH_MARKER`
    naming the family, the repo, and both spellings. The repair is
    deterministic, so the key is stable run to run and the finding is
    comparable rather than dropped.

    `strict=True` RAISES INSTEAD, and is how the tests assert the rule. Nothing
    in production passes it: the authoring-time net is
    `test_no_family_writes_a_whitespace_bearing_path_literal` (static, in the
    pull request that would introduce the defect) plus the runtime value pin in
    `test_notebook_projection_drift`. Those catch a FAMILY that spells a bad
    path; the sanitizer catches DATA that carries one, which no test can
    forbid because the corpus is not ours to name.

    NOT GUARDED HERE: `repo=`, which shares the `\S+` shape. It is a checkout
    directory name and has never been anything but `[A-Za-z]+`, and the
    general net for a defect in ANY field is the other half of this change —
    `parse_previous` now REPORTS the rows it cannot read, so the next one
    surfaces on the first run rather than the hundredth.
    """
    path = f.path
    if not isinstance(path, str) or not _PATH_RE.fullmatch(path):
        if strict:
            raise ValueError(
                f"doc-health family {f.family!r} (repo {f.repo!r}) built a "
                f"finding whose ranked-plan path the report grammar cannot "
                f"read back: {f.path!r}. The `path=` field is unquoted and "
                f"ends at the space before `rule=`, so it must be one or more "
                f"NON-WHITESPACE characters. Name a real repository-relative "
                f"path, or — if the finding is not about one file — a "
                f"whitespace-free slug. A prose label in the path slot is "
                f"emitted into the report and read back by nothing (issue "
                f"#474; the live case was `path=(lifecycle notebooks)`).")
        path = sanitize_path(path)
        print(f"{SANITIZED_PATH_MARKER}: {f.family} {f.repo} {f.path!r} -> "
              f"{path!r}", file=sys.stderr)
    line = (f"- severity={f.severity} family={f.family} repo={f.repo} "
            f"path={path} rule=\"{escape_field(f.rule)}\" "
            f"action=\"{escape_field(f.action)}\" "
            f"class=\"{f.resolution}\"")
    if f.disposer:
        line += f" disposer=\"{escape_field(f.disposer)}\""
    return line


def unparsed_plan_rows(text: str) -> list[tuple[int, str]]:
    """`(line number, line)` for every ranked-plan row the grammar rejects.

    A line counts as a ranked-plan row when it starts with `PLAN_ROW_PREFIX`,
    so nothing else in the report can be reported as broken grammar. Over
    `health/reports/` today this returns exactly two rows across 27 reports:
    the raw-`"` row #472 recorded as unfixable, and the `(lifecycle notebooks)`
    row #474 fixes at its source.
    """
    return [(n, line) for n, line in enumerate(text.splitlines(), 1)
            if line.startswith(PLAN_ROW_PREFIX) and not PLAN_RE.match(line)]


def _announce_unparsed_plan_rows(rows: list[tuple[int, str]]) -> None:
    """Say which rows of the previous report took no part in the comparison.

    stderr, not the rendered report: this is a fact about READING a prior
    artifact, not a finding about the corpus, and the run that discovers it is
    not the run that can fix it.
    """
    for lineno, line in rows:
        print(f"{UNPARSED_PLAN_ROW_MARKER}: line {lineno}: {line}",
              file=sys.stderr)
    print(f"{UNPARSED_PLAN_ROW_TOTAL_MARKER}: {len(rows)} ranked-plan row(s) "
          f"in the previous report matched no parser and therefore took no "
          f"part in the regression or uncited-resolution comparison",
          file=sys.stderr)


# The family `uncited_resolutions` itself emits. Not a member of `FAMILY_IDS`
# / `families.FAMILIES` — doc-health.md's "Check Families" table runs exactly
# twenty-three named families over the corpus, and this is not one of them. It
# is the ENFORCEMENT of the contested-finding rule (doc-health spec
# "Requirement: Finding severity and regression handling", scenario "A
# contested finding is resolved") for THOSE families, stamped
# `resolution="contested"` below because the two-value taxonomy has no third
# option and an uncited-resolution finding plainly is not a mechanical
# `auto-fixable` defect.
#
# ISSUE #515: that `contested` stamp must NOT make `parse_previous` fold a
# vanished uncited-resolution LINE into `previous_contested`, or the finding
# audits its own disappearance forever. The ORIGINAL finding's key (e.g.
# `(location-conformance, alpha, docs/reg.md)`) already carries the citation
# obligation under its own family's line — that is what this rule exists to
# police. The DERIVED echo's key
# (`(uncited-resolution, alpha, docs/reg.md)`) names no corpus state a human
# ever deliberately set; it exists only to demand a citation for the
# original's disappearance, and once emitted it has done its job — there is
# no second citation to give for an accountability marker resolving itself.
# Treating it as its own contested subject produced exactly the loop the
# nightly of 2026-08-30 observed: 25 of 41 `uncited-resolution` errors were
# the 25 `uncited-resolution` findings of the 2026-08-26 baseline, echoing
# themselves, with no document behind any of them.
UNCITED_RESOLUTION_FAMILY = "uncited-resolution"


def parse_repo_identity(text: str) -> frozenset[str] | None:
    """The repo-slug set a report was stamped with (issue #342), read back
    from the FIRST `Repo-Identity:` header line.

    `None` means UNSTAMPED — a report written before this change, including
    every report in `health/reports/*.md` as of 2026-08-31 — and is the one
    return value a caller MUST treat as "identity unknown", never as "empty
    set". An empty but STAMPED set (a run that covered zero repos) reads back
    as `frozenset()`, which is falsy but not `None`; callers comparing
    against this MUST use `is None`, never bare truthiness, or the two
    collapse into the same branch.

    Deliberately NOT folded into `parse_previous`: that function's
    `(keys, contested)` pair is unpacked by ~30 call sites across this
    package's tests, and widening it to a triple would touch every one of
    them for a concern most of those callers do not have. A caller that wants
    both calls this and `parse_previous` separately, over the same text.
    """
    m = REPO_IDENTITY_RE.search(text)
    if not m:
        return None
    value = m.group(1).strip()
    if value == REPO_IDENTITY_NONE:
        return frozenset()
    return frozenset(s.strip() for s in value.split(",") if s.strip())


def parse_previous(text: str, *, announce=_announce_unparsed_plan_rows):
    """(error_keys, contested_keys) from a prior report's ranked plan.
    Reports predating resolution classes yield an empty contested set.

    UNREADABLE ROWS ARE REPORTED, NOT DROPPED (issue #474). This used to
    `continue` past any line `PLAN_RE` rejected, which is right for the 200-odd
    prose lines of a report and catastrophic for a ranked-plan row: a grammar
    defect cost the comparison a finding and said nothing, so both instances
    found so far were found by reading the regex, not by running it. Rows that
    DO parse are unaffected — the returned key sets are byte-for-byte what they
    always were — and `announce=None` silences the diagnostic for a caller that
    wants the sets alone.

    A `uncited-resolution` LINE NEVER JOINS `contested` (issue #515), even
    though it is written with `class="contested"`. See `UNCITED_RESOLUTION_
    FAMILY` above for why: it is the enforcement of the rule for OTHER
    families, not a subject of the rule itself, and folding it in here is
    the entire mechanism of the infinite echo. It still joins `keys` like any
    other `error`/`critical` row, so a genuinely persisting uncited-resolution
    finding is recognized as persisting rather than misread as a fresh
    regression.
    """
    keys, contested = set(), set()
    for line in text.splitlines():
        m = PLAN_RE.match(line)
        if not m:
            continue
        key = (m.group(2), m.group(3), m.group(4))
        if m.group(1) in (CRITICAL, ERROR):
            keys.add(key)
        if m.group(7) == "contested" and m.group(2) != UNCITED_RESOLUTION_FAMILY:
            contested.add(key)
    # ONE SOURCE FOR "WHICH ROWS ARE UNREADABLE": `unparsed_plan_rows`, not a
    # second copy of its predicate inlined in the loop above. The inlined copy
    # was the first draft and is exactly the drift this whole change is about —
    # two readers of one grammar that can disagree.
    unparsed = unparsed_plan_rows(text)
    if unparsed and announce is not None:
        announce(unparsed)
    return keys, contested


def uncited_resolutions(findings: list[Finding], previous_contested,
                        dispositions,
                        unavailable_families: set[str] | None = None,
                        unavailable_repos: set[str] | None = None
                        ) -> list[Finding]:
    """Contested findings from the previous report that vanished without a
    recorded disposition become new error findings (doc-health contract:
    contested resolutions require a cited change or human disposition).

    `previous_contested` never carries a `uncited-resolution` key — see
    `UNCITED_RESOLUTION_FAMILY` and `parse_previous` — so this can iterate it
    with no self-exclusion of its own and still never re-audit its own prior
    output (issue #515).

    `unavailable_repos` (issue #342 fix shape item 3) is the same exclusion
    as `unavailable_families`, one axis over: a repo the baseline covered but
    THIS run's scope does not never got a chance to re-confirm or refute that
    repo's contested findings, so their absence from `findings` must never
    read as "resolved". This is the residual gap a `--previous-report` whose
    stamped identity is a proper SUPERSET of the current run's still carries
    even after the identity refusal in `runner.main` (which requires the
    current scope to be a SUBSET of the baseline's, not equal to it) — e.g. a
    `--single-repo` self-gate diffed against last night's full aggregation
    baseline. Callers that cannot determine the baseline's identity (an
    unstamped, pre-#342 report) MUST pass `None` or an empty set here rather
    than guess one, preserving exactly today's behaviour for that case.
    """
    current = {f.match_key() for f in findings}
    out = []
    for family, repo, path in sorted(previous_contested or ()):
        if family in (unavailable_families or set()):
            continue
        if repo in (unavailable_repos or set()):
            continue
        if (family, repo, path) in current:
            continue
        if (family, repo, path) in dispositions:
            continue
        out.append(Finding(
            ERROR, UNCITED_RESOLUTION_FAMILY, repo, path,
            f"contested {family} finding resolved without citation",
            "record a disposition (health/dispositions.yaml) citing the "
            "OpenSpec change or human decision, or restore the prior state",
            resolution="contested"))
    return out


def regressions(findings: list[Finding],
                previous_keys: set | None) -> list[Finding]:
    """New critical/error findings vs the previous report (family + path
    match, per the contract). No previous report = baseline, no regressions."""
    if previous_keys is None:
        return []
    return [f for f in findings
            if f.severity in (CRITICAL, ERROR)
            and f.match_key() not in previous_keys]


def canon_stats(docs, spec_words: int):
    by_stage: dict[str, tuple[int, int]] = {}
    total_words = spec_words
    canon_words = spec_words
    for doc in docs:
        stage = doc.status or "(none)"
        n, w = by_stage.get(stage, (0, 0))
        by_stage[stage] = (n + 1, w + doc.words)
        total_words += doc.words
        if doc.status in ("ratified", "standard"):
            canon_words += doc.words
    share = (100.0 * canon_words / total_words) if total_words else 0.0
    return share, canon_words, total_words, by_stage


def render(run_date: date, findings: list[Finding], skips, preflight_log,
           docs, spec_words: int, deviations: list[str],
           new_regressions: list[Finding], semantic_meta=None,
           catalog_meta=None, organizer_meta=None,
           family_notes: dict | None = None,
           repo_slugs: frozenset[str] | set[str] | None = None) -> str:
    findings = sorted(findings, key=Finding.sort_key)
    share, canon, total, by_stage = canon_stats(docs, spec_words)
    out = []
    out.append(f"# Doc-Health Report — {run_date.isoformat()}")
    out.append("")
    out.append("Status: record")
    out.append("Kind: report")
    # ISSUE #342. `repo_slugs=None` renders NO line — byte-identical output
    # for every caller that has not adopted the stamp (this package's own
    # unit tests included, most of which build a report to exercise one
    # unrelated field and pass no repo scope at all). `runner.main` is the
    # one production caller and always passes the run's real scope, even
    # when it is a single repo, so every report it writes from here on is
    # stamped — `frozenset()` (a run somehow covering zero repos) still
    # renders the explicit `(none)` line rather than being mistaken for "not
    # stamped" on read-back (see `parse_repo_identity`).
    if repo_slugs is not None:
        stamp = (", ".join(sorted(repo_slugs))
                 if repo_slugs else REPO_IDENTITY_NONE)
        out.append(f"{REPO_IDENTITY_PREFIX}{stamp}")
    out.append("")
    out.append("## Headline")
    out.append("")
    out.append(f"Canon share by words: {share:.1f}% "
               f"({canon} canon words / {total} governance words, "
               f"promoted specs included).")
    counts = {s: 0 for s in SEVERITY_RANK}
    for f in findings:
        counts[f.severity] += 1
    out.append(f"Findings: {counts['critical']} critical, "
               f"{counts['error']} error, {counts['warning']} warning, "
               f"{counts['info']} info. "
               f"New regressions vs previous report: {len(new_regressions)}.")
    if deviations:
        out.append("")
        out.append("Non-default configuration (cross-run comparisons must "
                   "account for this):")
        for d in deviations:
            out.append(f"- {d}")
    if skips:
        out.append("")
        out.append("Skipped families (never silently omitted):")
        for s in sorted(skips, key=lambda s: s.family):
            out.append(f"- `{s.family}` — {s.reason}")
    out.append("")
    out.append("## Per-Stage Counts")
    out.append("")
    out.append("| Status | Docs | Words |")
    out.append("| --- | --- | --- |")
    for stage in sorted(by_stage):
        n, w = by_stage[stage]
        out.append(f"| {stage} | {n} | {w} |")
    out.append(f"| (promoted specs) | — | {spec_words} |")
    out.append("")
    out.append("## Preflight")
    out.append("")
    for repo, cmd, ok, tail in preflight_log:
        mark = "ok" if ok else "FAIL"
        out.append(f"- {mark}: {repo} `{cmd}` — {tail}")
    if semantic_meta is not None:
        out.append("")
        out.append("## Semantic Sweep")
        out.append("")
        if semantic_meta.skipped_reason:
            out.append(f"Skipped: {semantic_meta.skipped_reason}")
        declared = (f"declared by {semantic_meta.declared_by}"
                    if semantic_meta.declared_by else "contract default")
        out.append(f"- scope: {semantic_meta.scope} ({declared})")
        out.append(f"- corpus: {semantic_meta.corpus_size} of "
                   f"{semantic_meta.total_docs} docs")
        out.append(f"- model: {semantic_meta.model}, prompt contract "
                   f"v{semantic_meta.prompt_version}")
        out.append(f"- job envelope: {semantic_meta.envelope_ref}")
        for d in semantic_meta.dropped:
            out.append(f"- dropped malformed finding: {d}")
    if catalog_meta is not None:
        # "Document Catalog" section (feature task T020; data-model.md
        # CatalogMeta field table) — every field renders as a plain bullet
        # line, same style as "## Semantic Sweep" above. Read-only render
        # input: nothing here is ever wrapped in a Finding or appended to
        # `findings`/the Ranked Plan (FR-012 / Constitution Check).
        from .catalog_dispatch import FACET_STATE_KEYS
        out.append("")
        out.append("## Document Catalog")
        out.append("")
        if catalog_meta.skipped_reason:
            out.append(f"Skipped: {catalog_meta.skipped_reason}")
        out.append(f"- snapshots: "
                   f"{', '.join(catalog_meta.snapshot_refs) or '(none)'}")
        out.append(f"- coverage: {catalog_meta.cataloged} of "
                   f"{catalog_meta.total_docs} docs cataloged")
        sc = catalog_meta.state_counts
        out.append("- facet states: " + ", ".join(
            f"{k}={sc.get(k, 0)}" for k in FACET_STATE_KEYS))
        out.append(f"- changes: {catalog_meta.new_count} new, "
                   f"{catalog_meta.changed_count} changed, "
                   f"{catalog_meta.deleted_count} deleted, "
                   f"{catalog_meta.stale_count} stale, "
                   f"{catalog_meta.rejected_count} rejected")
        out.append(f"- inventory: {catalog_meta.inventory_version}, "
                   f"taxonomy digest {catalog_meta.taxonomy_digest}")
        out.append(f"- classifier: {catalog_meta.classifier_version}, "
                   f"prompt contract v{catalog_meta.prompt_version}, "
                   f"model {catalog_meta.model or '(none)'}")
        out.append(f"- recommendation evidence: "
                   f"{', '.join(catalog_meta.recommendation_refs) or '(none)'}")
        if catalog_meta.baseline_progress is not None:
            bp = catalog_meta.baseline_progress
            out.append(
                f"- baseline progress: {bp['cataloged']}/{bp['total']} "
                f"entries ({bp['percent']:.1f}%) across "
                f"{bp['repos_complete']}/{bp['repos_total']} repositories")
        pa = catalog_meta.pending_aging
        out.append("- pending-aging: " + ", ".join(
            f"{k}={pa.get(k, 0)}" for k in ("warning", "error")))
        if catalog_meta.deviations:
            out.append("- non-default configuration: " +
                       "; ".join(catalog_meta.deviations))
    if organizer_meta is not None:
        # "Ideation Organizer" section (task 7.3): organizer selection,
        # readiness, authorization, skip, queue, run, and recommendation
        # counts, following the "## Document Catalog" section's bullet shape.
        # Read-only render input: nothing here is ever wrapped in a Finding or
        # appended to `findings`/the Ranked Plan — organizer recommendations are
        # proposals, not doc-health findings or verdicts (spec "Non-mutating
        # semantic ideation organizer"), and are kept out of the critical/error
        # regression issue entirely (task 7.3).
        om = organizer_meta
        out.append("")
        out.append("## Ideation Organizer")
        out.append("")
        if om.skipped_reason:
            out.append(f"Skipped: {om.skipped_reason}")
        reasons = ", ".join(f"{k}={om.by_reason[k]}"
                            for k in sorted(om.by_reason)) or "none"
        out.append(f"- selection: {om.selected} selected, "
                   f"{om.dispatchable} dispatchable ({reasons})")
        ready = "n/a" if om.ready is None else str(om.ready).lower()
        out.append(f"- readiness: ready={ready} "
                   f"({om.readiness_reason or 'not evaluated'})")
        out.append(f"- authorization: {om.authorized} authorized, "
                   f"{om.authorization_denied} denied")
        out.append(f"- watchdog: {om.queue_timeouts} queue timeout(s), "
                   f"{om.run_timeouts} run timeout(s), {om.runs} run(s)")
        out.append(f"- recommendations: {om.recommendation_count} "
                   f"(dispatched idea {om.dispatched_idea or '(none)'}, "
                   f"rejected {om.rejected})")
        out.append(f"- organizer: prompt contract v{om.prompt_version}, "
                   f"model {om.model or '(none)'}")
        out.append(f"- evidence (this run): "
                   f"{', '.join(om.evidence_refs) or '(none)'}")
        linked = (": " + ", ".join(om.linked_evidence_refs[:5])
                  if om.linked_evidence_refs else "")
        out.append(f"- linked evidence: {len(om.linked_evidence_refs)} "
                   f"record(s) under health/ideation-organizer/{linked}")
        if om.deviations:
            out.append("- non-default configuration: " +
                       "; ".join(om.deviations))
    out.append("")
    out.append("## Findings By Family")
    from .families import FAMILY_SUMMARIES
    from .semantic import SEMANTIC_FAMILY_IDS
    for family in FAMILY_IDS + SEMANTIC_FAMILY_IDS + ["preflight"]:
        fam_findings = [f for f in findings if f.family == family]
        skipped = next((s for s in skips if s.family == family), None)
        out.append("")
        out.append(f"### {family}")
        out.append("")
        # A family's own notes come BEFORE its findings and are rendered even
        # when there are none — a family whose measurement basis varies must
        # state the basis on a clean run too, or "No findings." reads as a
        # verdict about a tree nobody named (`families.FAMILY_NOTES`).
        #
        # SINCE add-modified-block-currency-check § 5.1 there is a SECOND kind of
        # line in this position: a per-class tally of the family's own findings,
        # from `families.FAMILY_SUMMARIES`. The two are kept apart because they
        # answer different questions — a note is a fact about the RUN (which tree
        # was measured), a summary is a fact about the FINDINGS (how they split
        # across the family's classes) — and they differ on the skip: a skipped
        # family still HAS a basis, and has no tally, because zeros beside a skip
        # line would claim a measurement nobody took.
        #
        # ADDITIVE, AND BYTE-IDENTICAL FOR EVERY FAMILY WITH NO ENTRY: `notes`
        # is empty for those, so the emit-and-blank-line condition below is the
        # same one this code already applied to `family_notes` alone.
        notes = list((family_notes or {}).get(family, ()))
        if not skipped and family in FAMILY_SUMMARIES:
            notes += FAMILY_SUMMARIES[family](fam_findings)
        for note in notes:
            out.append(note)
        if notes:
            out.append("")
        if skipped:
            out.append(f"Skipped: {skipped.reason}")
        elif not fam_findings:
            out.append("No findings.")
        else:
            for f in fam_findings:
                out.append(f"- [{f.severity}] {f.repo}:{f.path} — {f.rule}")
    out.append("")
    out.append("## Ranked Plan")
    out.append("")
    if not findings:
        out.append("No findings — nothing to stage.")
    for f in findings:
        out.append(plan_line(f))
    out.append("")
    return "\n".join(out)


# --- Ideation readiness lane report integration ------------------------------
#
# doc-health "Ideation readiness lane" (openxFactory
# add-ideation-cross-reference-readiness, change task 4.3). Unlike the
# Semantic Sweep / Document Catalog sections above (rendered by `render()`
# itself, from data available at deterministic-pass time), the readiness
# lane's own ADDED requirement binds it to run AFTER the deterministic pass —
# so its section and ranked-plan lines are folded into an ALREADY-RENDERED
# report in place, by `insert_readiness_section`, called from
# `readiness_dispatch.main`'s merge phase. `build_readiness_section` is a
# read-only render (mirrors the "Document Catalog" section: never wrapped in
# a Finding itself); `meta.findings` are the ONE part of this lane that DOES
# reach the Ranked Plan (the ADDED requirement's own scenario), via the SAME
# `plan_line()` every other family already uses.

FINDINGS_BY_FAMILY_HEADING = "\n## Findings By Family\n"
NO_FINDINGS_LINE = "No findings — nothing to stage.\n"


def build_readiness_section(meta) -> list[str]:
    """Render the "## Ideation Readiness" section lines: lane outcome, links
    to the index/evidence artifacts, and per-cluster counts."""
    lines = ["", "## Ideation Readiness", ""]
    if meta.skipped_reason:
        lines.append(f"Skipped: {meta.skipped_reason}")
    lines.append(f"- clusters: {meta.scored_clusters} scored of "
                f"{meta.total_clusters} total")
    lines.append(f"- index: {meta.index_path or '(none persisted yet)'}")
    if meta.index_md_path:
        lines.append(f"- index (markdown projection): {meta.index_md_path}")
    lines.append(f"- evidence: {meta.evidence_path or '(none this run)'}")
    prompt_version = (meta.prompt_version if meta.prompt_version is not None
                      else "(n/a)")
    lines.append(f"- model: {meta.model}, prompt contract v{prompt_version}")
    lines.append(f"- source revision: {meta.source_revision or '(n/a)'}")
    for cluster_id, reason in meta.skipped_clusters:
        lines.append(f"- cluster {cluster_id} unscored: {reason}")
    return lines


def insert_readiness_section(report_text: str, meta) -> str:
    """Insert the Ideation Readiness section before '## Findings By Family'
    and fold `meta.findings` into the existing '## Ranked Plan' section of an
    ALREADY-RENDERED report — both idempotent-in-position against exactly one
    `render()` output per dated report (the lane runs once, after the
    deterministic pass, before the nightly's "Commit report" step)."""
    idx = report_text.index(FINDINGS_BY_FAMILY_HEADING)
    section = "\n".join(build_readiness_section(meta)) + "\n"
    report_text = report_text[:idx] + section + report_text[idx:]

    if meta.findings:
        plan_lines = "\n".join(
            plan_line(f) for f in sorted(meta.findings, key=Finding.sort_key))
        if NO_FINDINGS_LINE in report_text:
            report_text = report_text.replace(
                NO_FINDINGS_LINE, plan_lines + "\n", 1)
        else:
            report_text = report_text.rstrip("\n") + "\n" + plan_lines + "\n"
    return report_text


def build_derive_possibles_section(meta) -> list[str]:
    """Render the "## Derived Possibles" section lines: lane outcome, links
    to the index/evidence artifacts, merged register ids, and per-cluster
    skip/void detail (add-possibles-derivation-lane tasks 4.1/4.4)."""
    lines = ["", "## Derived Possibles", ""]
    if meta.skipped_reason:
        lines.append(f"Skipped: {meta.skipped_reason}")
    lines.append(f"- possibles merged: {len(meta.merged_added)} "
                 f"(from {meta.eligible_clusters} eligible of "
                 f"{meta.total_clusters} cluster(s))")
    for pid in meta.merged_added:
        lines.append(f"  - `{pid}` (pending_review — dispose on the gate "
                     "console)")
    lines.append(f"- index: {meta.index_path or '(register unchanged)'}")
    lines.append(f"- evidence: {meta.evidence_path or '(none this run)'}")
    prompt_version = (meta.prompt_version if meta.prompt_version is not None
                      else "(n/a)")
    lines.append(f"- model: {meta.model}, prompt contract v{prompt_version}")
    lines.append(f"- source revision: {meta.source_revision or '(n/a)'}")
    for cluster_id, reason in meta.skipped_clusters:
        lines.append(f"- cluster {cluster_id} skipped: {reason}")
    for cluster_id, title, reason in meta.voided:
        lines.append(f"- cluster {cluster_id} voided {title!r}: {reason}")
    return lines


def insert_derive_possibles_section(report_text: str, meta) -> str:
    """Insert the Derived Possibles section before '## Findings By Family'
    (idempotent-in-position against exactly one `render()` output per dated
    report, like `insert_readiness_section`). Deliberately NEVER touches the
    Ranked Plan: undisposed derived possibles are excluded from ranked plans
    and human-picked totals by contract (the possibles-derivation delta's
    "A consumer counts possibles" scenario)."""
    idx = report_text.index(FINDINGS_BY_FAMILY_HEADING)
    section = "\n".join(build_derive_possibles_section(meta)) + "\n"
    return report_text[:idx] + section + report_text[idx:]


def build_neutrality_section(meta) -> list[str]:
    """Render the "## Neutrality Drift" section lines (openxFactory
    add-neutrality-drift-lane task 1.3): stage-1 signal counts per domain
    repo, the incremental selection outcome, and each drafted DTN-register
    seed with its evidence reference — the rolling-PR surface Brett
    approves seeds from (design D3)."""
    lines = ["", "## Neutrality Drift", ""]
    if meta.skipped_reason:
        lines.append(f"Skipped: {meta.skipped_reason}")
    per_repo = ", ".join(
        f"{repo}={meta.candidates.get(repo, 0)}"
        for repo in sorted(meta.scope)) or "none"
    total_files = sum(meta.scanned_files.values())
    lines.append(f"- stage 1: {sum(meta.candidates.values())} candidate(s) "
                 f"from {total_files} scanned file(s) ({per_repo})")
    totals: dict[str, int] = {}
    for counts in meta.signal_counts.values():
        for name, n in counts.items():
            totals[name] = totals.get(name, 0) + n
    lines.append("- signals: " + (", ".join(
        f"{name}={totals[name]}" for name in sorted(totals)) or "none"))
    register_cited = sum(meta.register_cited.values())
    lines.append(f"- selection: {meta.selected} new/changed survivor(s); "
                 f"{meta.dispatched} dispatched, {meta.carried_over} "
                 f"carried over; {meta.suppressed} disposition-suppressed, "
                 f"{meta.baseline_skipped} baseline-covered, "
                 f"{register_cited} already register-cited")
    if meta.seeds:
        lines.append(f"- drafted seeds ({len(meta.seeds)}; approval = "
                     "merging the register addition):")
        for dtn, repo, path, decision, seed_ref in meta.seeds:
            lines.append(f"  - {dtn} `{decision}` — {repo}:{path} "
                         f"(drafted seed: {seed_ref})")
    else:
        lines.append("- drafted seeds: none this run")
    for repo in sorted(meta.lexicon_notes):
        lines.append(f"- lexicon [{repo}]: {meta.lexicon_notes[repo]}")
    prompt_version = (meta.prompt_version
                      if meta.prompt_version is not None else "(n/a)")
    lines.append(f"- scout: prompt contract v{prompt_version}, model "
                 f"{meta.model or '(none)'}, run {meta.run_id or '(n/a)'}")
    if meta.baseline_recorded:
        lines.append(f"- baseline marker recorded: {meta.baseline_recorded}")
    if meta.deviations:
        lines.append("- non-default configuration: "
                     + "; ".join(meta.deviations))
    return lines


def insert_neutrality_section(report_text: str, meta) -> str:
    """Insert the Neutrality Drift section before '## Findings By Family'
    and fold `meta.findings` — the drafted seeds' ranked-plan items
    (WARNING/contested proposals, never regression-eligible) — into the
    existing '## Ranked Plan' section, exactly the
    `insert_readiness_section` mechanics."""
    idx = report_text.index(FINDINGS_BY_FAMILY_HEADING)
    section = "\n".join(build_neutrality_section(meta)) + "\n"
    report_text = report_text[:idx] + section + report_text[idx:]

    if meta.findings:
        plan_lines = "\n".join(
            plan_line(f) for f in sorted(meta.findings, key=Finding.sort_key))
        if NO_FINDINGS_LINE in report_text:
            report_text = report_text.replace(
                NO_FINDINGS_LINE, plan_lines + "\n", 1)
        else:
            report_text = report_text.rstrip("\n") + "\n" + plan_lines + "\n"
    return report_text
