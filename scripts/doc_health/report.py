"""Report generation and the regression diff.

The report schema is owned by the openxFactory `doc-health` contract:
dated Markdown, `Status: record` + `Kind: report`, canon-share headline,
per-stage counts, per-family sections, machine-parseable ranked plan.
This module renders findings into that schema; it defines no schema of
its own.
"""

from __future__ import annotations

import re
from datetime import date

from . import CRITICAL, ERROR, FAMILY_IDS, Finding, SEVERITY_RANK

# A free-text ranked-plan field: everything up to the closing `"`, with `\"`
# and `\\` admitted inside it. The naive `[^"]*` this replaces closed the field
# on the FIRST `"` and so could not read back a row it had itself emitted —
# any finding whose rule or action text contains a double quote. The live
# case is a modified-block-currency arm: it writes the requirement title as
# `{title!r}`, and `repr()` switches to DOUBLE quotes when the title contains
# an apostrophe (`"Brett's ruling"`), so the row was emitted by `plan_line`,
# never matched by `PLAN_RE`, and silently dropped from every
# `--previous-report` comparison — making a persistent finding read as a new
# regression on the next run, and hiding a contested finding's disappearance
# from `uncited_resolutions`. Emit and parse are now symmetric
# (`escape_field` / `unescape_field`).
_FIELD = r'((?:[^"\\]|\\.)*)'

PLAN_RE = re.compile(
    r"^- severity=(\w+) family=([\w-]+) repo=(\S+) path=(\S+) "
    r'rule="' + _FIELD + r'" action="' + _FIELD + r'"'
    r'(?: class="([\w-]+)")?'
    r'(?: disposer="' + _FIELD + r'")?$')


def escape_field(value: str) -> str:
    """Make `value` safe between the `"` delimiters of a ranked-plan field.

    BYTE-IDENTICAL for any value containing neither `"` nor `\\` — which is
    every row of every report written to date — so the escape is invisible in
    the nightly report diff and old reports keep parsing unchanged.
    """
    return value.replace("\\", "\\\\").replace('"', '\\"')


def unescape_field(value: str) -> str:
    """Inverse of `escape_field` over a `_FIELD` capture."""
    return re.sub(r"\\(.)", r"\1", value)


def plan_line(f: Finding) -> str:
    line = (f"- severity={f.severity} family={f.family} repo={f.repo} "
            f"path={f.path} rule=\"{escape_field(f.rule)}\" "
            f"action=\"{escape_field(f.action)}\" "
            f"class=\"{f.resolution}\"")
    if f.disposer:
        line += f" disposer=\"{escape_field(f.disposer)}\""
    return line


def parse_previous(text: str):
    """(error_keys, contested_keys) from a prior report's ranked plan.
    Reports predating resolution classes yield an empty contested set."""
    keys, contested = set(), set()
    for line in text.splitlines():
        m = PLAN_RE.match(line)
        if not m:
            continue
        key = (m.group(2), m.group(3), m.group(4))
        if m.group(1) in (CRITICAL, ERROR):
            keys.add(key)
        if m.group(7) == "contested":
            contested.add(key)
    return keys, contested


def uncited_resolutions(findings: list[Finding], previous_contested,
                        dispositions,
                        unavailable_families: set[str] | None = None
                        ) -> list[Finding]:
    """Contested findings from the previous report that vanished without a
    recorded disposition become new error findings (doc-health contract:
    contested resolutions require a cited change or human disposition)."""
    current = {f.match_key() for f in findings}
    out = []
    for family, repo, path in sorted(previous_contested or ()):
        if family in (unavailable_families or set()):
            continue
        if (family, repo, path) in current:
            continue
        if (family, repo, path) in dispositions:
            continue
        out.append(Finding(
            ERROR, "uncited-resolution", repo, path,
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
           family_notes: dict | None = None) -> str:
    findings = sorted(findings, key=Finding.sort_key)
    share, canon, total, by_stage = canon_stats(docs, spec_words)
    out = []
    out.append(f"# Doc-Health Report — {run_date.isoformat()}")
    out.append("")
    out.append("Status: record")
    out.append("Kind: report")
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
