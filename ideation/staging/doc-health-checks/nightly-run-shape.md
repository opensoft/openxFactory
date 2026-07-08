# Staged: Nightly Doc-Health Run Shape

Status: staged
Kind: architecture
Repository context: openxFactory
Source: [doc-health-pipeline brainstorm](../../brainstorm/doc-health-pipeline.md)
Target capability: new `doc-health` capability (delta: ADDED) — contract in
openxFactory, implementation in codexFactory, nightly runner hosted by the
`xFactory` aggregation repo (the only repo pinning all submodules).

Companion fragment: [status-check-rules.md](status-check-rules.md) — the
deterministic checks the run MUST implement.

## Claims

1. Scheduled GitHub Action in the aggregation repo, `--recurse-submodules`
   checkout, nightly cron plus manual dispatch.
2. Deterministic pass only for v1: per-repo validators, the status-check
   rules, tag hygiene (once prose-tagging ratifies), submodule pin drift vs
   remote mains, contract-copy drift, NotebookLM projection dry-run drift.
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

- Aging thresholds for staged/draft items (days before a health smell).
- Report visualization: plain markdown v1; dashboard artifact later.

## Exit

Two OpenSpec changes: `add-doc-health-contract` (openxFactory, the capability
and report schema) and the codexFactory implementation change with the
workflow + scripts.
