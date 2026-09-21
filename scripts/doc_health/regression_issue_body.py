"""Render the doc-health nightly's regression-issue body under GitHub's
issue-body limit, plus the full, unabridged findings list for the report
artifact.

Fixes opensoft/openxFactory#1118: the "Open regression issue" step in
`.github/workflows/doc-health-reusable.yml` wrote one bullet per new
critical/error finding straight into the issue body with no size cap. Once
the regression list grew past GitHub's 65536-CHARACTER `createIssue` limit,
every `gh issue create` call failed and reddened the nightly's `finalize`
job (last successful open: opensoft/xFactory#236, 2026-09-04).

This module is extracted out of that step's inline `python3 - <<'PY'` rather
than kept there, because the fix needs the SAME rendering in TWO places in
one job run: "Open regression issue" sits near the end of a long `finalize`
job and only runs when there are new findings
(`if: steps.run.outputs.new_count != '0'`), but "Upload report artifact"
already ran, uploading only the capped report, LONG before that step is
reached. So the full findings list has to be written (as `new-findings.md`)
right after `new-findings.json` is produced -- earlier in the job, ahead of
"Upload report artifact" -- and `render()` is what both call sites share.
"""

from __future__ import annotations

#: GitHub's issue-body limit (GraphQL `createIssue`) is 65536 CHARACTERS.
#: This caps on UTF-8 BYTES instead: bytes >= characters for any UTF-8
#: string (the bullet text below contains an em dash, a multi-byte
#: character), so a body capped at 60000 bytes is always under the
#: 65536-character limit no matter how many multi-byte characters it
#: contains. The ~5.5KB margin is headroom for the header, count line and
#: omitted-count line that always accompany the bullets.
DEFAULT_CAP_BYTES = 60000


def _bullet(finding: dict) -> str:
    return (f"- [{finding['severity']}] {finding['family']} "
            f"{finding['repo']}:{finding['path']} — {finding['rule']}")


def _header(run_date: str) -> str:
    return (
        "New critical/error findings versus the previous report\n"
        "(matched by family + path). Full report:\n"
        f"health/reports/{run_date}.md"
    )


def render(findings: list[dict], run_date: str,
           cap_bytes: int = DEFAULT_CAP_BYTES) -> tuple[str, str]:
    """Return ``(issue_body, full_list_md)``.

    ``issue_body`` is the header, a count line ("<N> new critical/error
    findings (the first <K> are listed here; the full list is in the report
    artifact and in health/reports/<run_date>.md)"), as many bullets as fit
    under ``cap_bytes`` (UTF-8 encoded), and a final line naming how many
    were omitted. Its UTF-8 encoding is always <= ``cap_bytes``.

    ``full_list_md`` is every finding rendered as a bullet, unabridged --
    nothing is ever lost even when the issue body itself is capped, because
    the caller writes this to ``new-findings.md`` beside ``new-findings.json``
    for the report artifact.
    """
    total = len(findings)
    bullets = [_bullet(f) for f in findings]

    full_list_md = "\n".join(bullets)
    if full_list_md:
        full_list_md += "\n"

    header = _header(run_date)
    pointer = f"health/reports/{run_date}.md"

    def count_line(k: int) -> str:
        return (f"{total} new critical/error findings (the first {k} are "
                 f"listed here; the full list is in the report artifact "
                 f"and in {pointer})")

    def omitted_line(m: int) -> str:
        return (f"{m} finding(s) omitted from this issue body; see the "
                 f"full list in the report artifact (new-findings.md) and "
                 f"in {pointer}.")

    def assemble(included: list[str], k: int, m: int) -> str:
        # UNIFORM shape regardless of whether `included` is empty (the
        # blank-line separator before the bullets block is always present,
        # even with zero bullets in it) -- so there is exactly ONE join
        # structure to reason about, not a k==0-vs-k>0 special case that the
        # byte budget below would otherwise have to track separately.
        parts = [header, "", count_line(k), "", *included, "", omitted_line(m)]
        return "\n".join(parts) + "\n"

    # k (bullets included) and m (bullets omitted) are both bounded above by
    # `total`, so MEASURING assemble() with k=total, m=total for the count/
    # omitted-line slots upper-bounds their real digit width (0 <= k,m <=
    # total) and therefore their real encoded length. Measuring the actual
    # assemble() output -- rather than hand-deriving the separator byte
    # count separately -- is what keeps this reservation from silently
    # drifting out of sync with assemble()'s real join structure.
    skeleton_bytes = len(assemble([], total, total).encode("utf-8"))
    budget = cap_bytes - skeleton_bytes

    included: list[str] = []
    used = 0
    for bullet in bullets:
        cost = len(bullet.encode("utf-8")) + 1  # + its own "\n" join
        if used + cost > budget:
            break
        included.append(bullet)
        used += cost

    k = len(included)
    m = total - k

    issue_body = assemble(included, k, m)
    encoded_len = len(issue_body.encode("utf-8"))
    assert encoded_len <= cap_bytes, (
        f"render() produced a body over its own cap ({encoded_len} > "
        f"{cap_bytes} bytes) -- cap_bytes is too small to hold even the "
        f"header/count/omitted-line skeleton ({skeleton_bytes} bytes) for "
        f"{total} finding(s); this is a genuinely unsatisfiable cap_bytes, "
        f"not a reservation bug"
    )
    return issue_body, full_list_md
