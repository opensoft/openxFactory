# Staged: Nightly Doc-Health Run Shape

Status: superseded
Superseded by: [doc-health contract](../../../docs/doc-health.md) and the
codexFactory change `implement-doc-health-checker` (archived 2026-07-09) —
both declared exit changes exist and are realized.
Kind: architecture
Repository context: openxFactory
Source: [doc-health-pipeline brainstorm](../../brainstorm/doc-health-pipeline.md)
Target capability: new `doc-health` capability (delta: ADDED) — contract in
openxFactory, implementation in codexFactory, nightly runner hosted by the
`xFactory` aggregation repo (the only repo pinning all submodules).
Proposed by: [add-doc-health-contract](../../../openspec/changes/archive/2026-07-09-add-doc-health-contract/proposal.md)
— the first of this topic's two declared exit changes (the contract); the
codexFactory implementation change follows after it ratifies, scoped by
[implementation-handoff.md](implementation-handoff.md).

Companion fragments: [status-check-rules.md](status-check-rules.md) and
[tag-hygiene-rules.md](tag-hygiene-rules.md) — the deterministic checks the
run MUST implement, now carried by the contract change.

## Claims

1. Scheduled GitHub Action in the aggregation repo, `--recurse-submodules`
   checkout, nightly cron plus manual dispatch.
2. Deterministic pass only for v1: per-repo validators, the status-check
   rules, tag hygiene (per the ratified prose-tagging grammar), submodule
   pin drift vs remote mains, contract-copy drift, NotebookLM projection
   dry-run drift.
3. Output is a dated report PLUS a ranked plan: every finding is a
   ready-to-stage work item, so report output feeds the ideation pipeline.
   Location: `health/reports/YYYY-MM-DD.md` in the aggregation repo; open an
   issue on regression.
4. Headline metric: canon share by words (ratified+standard+specs vs total),
   with per-stage counts and staged-item aging.
5. codexFactory owns the reusable workflow + scripts; the aggregation repo
   workflow only invokes them (keeps implementation in the engineering
   domain).

## Open questions

Both resolved at the proposal gate — see
[design.md](../../../openspec/changes/archive/2026-07-09-add-doc-health-contract/design.md)
of the proposing change:

- Aging thresholds → **contract defaults**: staged topics and candidate
  blocks warning at 30 days / error at 90; supersedes-without-`change=`
  warning at 14 / error at 45; drafts age-reported always, warning at 60.
- Report visualization → **plain Markdown v1** committed in
  `health/reports/` (reports carry `Status: record`); dashboard artifact
  later, plan-item shape kept machine-parseable for it.

## Exit

Two OpenSpec changes:
[add-doc-health-contract](../../../openspec/changes/archive/2026-07-09-add-doc-health-contract/proposal.md)
(openxFactory, the capability and report schema — created 2026-07-09) and
the codexFactory implementation change with the workflow + scripts, scoped
by [implementation-handoff.md](implementation-handoff.md).
