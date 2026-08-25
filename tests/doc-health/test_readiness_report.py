"""Ideation-readiness report integration (`report.insert_readiness_section`;
openxFactory add-ideation-cross-reference-readiness, change task 4.3).

Pure string-transform tests: no lane, no worker, no filesystem — a minimal
stand-in for `readiness_dispatch.ReadinessLaneMeta` and a minimal
already-rendered report fragment carrying the same '## Findings By Family' /
'## Ranked Plan' markers `report.render()` always emits.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)

from doc_health import CONTESTED, WARNING, Finding
from doc_health import report


@dataclass
class FakeMeta:
    run_id: str = "run-1"
    model: str = "claude-sonnet-5"
    total_clusters: int = 2
    scored_clusters: int = 0
    skipped_clusters: list = field(default_factory=list)
    index_path: str | None = "openxFactory/ideation/cross-reference.yaml"
    index_md_path: str | None = "openxFactory/ideation/cross-reference.md"
    evidence_path: str | None = None
    prompt_version: int | None = 1
    source_revision: str | None = "a" * 40
    validated: bool | None = None
    rejection_detail: str | None = None
    skipped_reason: str | None = None
    findings: list = field(default_factory=list)


def sample_report(ranked_plan_body="No findings — nothing to stage.\n"):
    return (
        "# Doc-Health Report — 2026-07-14\n\n"
        "Status: record\nKind: report\n\n"
        "## Headline\n\nsomething\n\n"
        "## Findings By Family\n\n"
        "### status-validity\n\nNo findings.\n\n"
        "## Ranked Plan\n\n" + ranked_plan_body)


def a_finding(path="cl-alpha") -> Finding:
    return Finding(WARNING, "ideation-readiness", "openxFactory", path,
                  f"topic {path!r} flagged propose-for-authorization",
                  "human authority disposes this pending_review "
                  "recommendation", resolution=CONTESTED,
                  disposer="openxFactory ratify gate")


# --- build_readiness_section -------------------------------------------

def test_section_reports_ok_with_links_and_counts():
    meta = FakeMeta(scored_clusters=2, evidence_path=
                    "openxFactory/health/ideation-readiness/2026-07-14/run-1.yaml")
    lines = report.build_readiness_section(meta)
    text = "\n".join(lines)
    assert "## Ideation Readiness" in text
    assert "Skipped" not in text
    assert "2 scored of 2 total" in text
    assert meta.index_path in text
    assert meta.index_md_path in text
    assert meta.evidence_path in text
    assert "prompt contract v1" in text
    assert meta.source_revision in text


def test_section_reports_skip_reason_and_unscored_clusters():
    meta = FakeMeta(scored_clusters=0, skipped_reason="worker_unavailable",
                    skipped_clusters=[("cl-alpha", "worker failed: boom")])
    text = "\n".join(report.build_readiness_section(meta))
    assert "Skipped: worker_unavailable" in text
    assert "0 scored of 2 total" in text
    assert "cl-alpha unscored: worker failed: boom" in text


def test_section_with_no_index_yet_says_so():
    meta = FakeMeta(index_path=None, index_md_path=None,
                    skipped_reason="openxFactory checkout not found")
    text = "\n".join(report.build_readiness_section(meta))
    assert "(none persisted yet)" in text
    assert "(none this run)" in text


# --- insert_readiness_section --------------------------------------------

def test_insert_replaces_no_findings_placeholder_when_findings_present():
    meta = FakeMeta(scored_clusters=2, findings=[a_finding("cl-alpha"),
                                                 a_finding("cl-beta")])
    updated = report.insert_readiness_section(sample_report(), meta)
    assert "## Ideation Readiness" in updated
    assert updated.index("## Ideation Readiness") < \
        updated.index("## Findings By Family")
    assert "No findings — nothing to stage." not in updated
    assert "severity=warning family=ideation-readiness repo=openxFactory " \
          "path=cl-alpha" in updated
    assert "class=\"contested\"" in updated
    # both findings present, sorted by Finding.sort_key (severity, family,
    # repo, path, rule) -- cl-alpha before cl-beta.
    assert updated.index("path=cl-alpha") < updated.index("path=cl-beta")


def test_insert_appends_after_existing_ranked_plan_lines():
    existing_line = ("- severity=error family=status-validity "
                     "repo=openxFactory path=docs/x.md rule=\"r\" "
                     "action=\"a\" class=\"auto-fixable\"")
    body = existing_line + "\n"
    meta = FakeMeta(scored_clusters=1, findings=[a_finding("cl-alpha")])
    updated = report.insert_readiness_section(sample_report(body), meta)
    assert existing_line in updated
    assert "family=ideation-readiness" in updated
    # the pre-existing deterministic line is untouched, and the new line
    # follows it (append, not replace).
    assert updated.index(existing_line) < \
        updated.index("family=ideation-readiness")


def test_insert_with_no_findings_leaves_ranked_plan_untouched():
    meta = FakeMeta(scored_clusters=0, skipped_reason="worker_unavailable",
                    findings=[])
    updated = report.insert_readiness_section(sample_report(), meta)
    assert "## Ideation Readiness" in updated
    assert "Skipped: worker_unavailable" in updated
    # no findings -> the Ranked Plan placeholder is untouched.
    assert "No findings — nothing to stage." in updated


def test_insert_is_idempotent_in_position_across_a_realistic_report():
    """Sanity: inserting into a report that already has BOTH deterministic
    findings and an existing '## Ideation Readiness'-shaped neighbor section
    (Document Catalog) still lands the section immediately before
    'Findings By Family' and appends plan lines after the existing ones."""
    report_text = (
        "# Doc-Health Report — 2026-07-14\n\n"
        "## Document Catalog\n\n- snapshots: (none)\n\n"
        "## Findings By Family\n\n### status-validity\n\nNo findings.\n\n"
        "## Ranked Plan\n\n"
        "- severity=warning family=tag-hygiene repo=openxFactory "
        "path=docs/y.md rule=\"r\" action=\"a\" class=\"auto-fixable\"\n")
    meta = FakeMeta(scored_clusters=1, findings=[a_finding("cl-alpha")])
    updated = report.insert_readiness_section(report_text, meta)
    assert updated.index("## Document Catalog") < \
        updated.index("## Ideation Readiness") < \
        updated.index("## Findings By Family")
    assert updated.rstrip("\n").endswith(
        "family=ideation-readiness repo=openxFactory path=cl-alpha "
        "rule=\"topic 'cl-alpha' flagged propose-for-authorization\" "
        "action=\"human authority disposes this pending_review "
        "recommendation\" class=\"contested\" "
        "disposer=\"openxFactory ratify gate\"")
