# Staged: Doc-Health Implementation Handoff

Status: superseded
Superseded by: [doc-health contract](../../../docs/doc-health.md) and the
codexFactory change `implement-doc-health-checker` (archived 2026-07-09;
`doc-health-checker` capability promoted) — both declared exit changes
exist and are realized; this topic has left the staged work queue.
Kind: reference
Repository context: openxFactory
Source: [add-doc-health-contract](../../../openspec/changes/archive/2026-07-09-add-doc-health-contract/proposal.md)
(task 3.1) — the ratified contract this scopes an implementation of.
Target capability: the follow-on **codexFactory** implementation change
(the second of this topic's two declared exit changes). Contract surface
lives in [docs/doc-health.md](../../../docs/doc-health.md) and the
`doc-health` spec; this fragment lists what the implementation change MUST
include and the decisions it must make.

## The implementation change MUST include

1. **Checker scripts, one per check family** (twelve families per the
   contract), runnable individually and as a suite, deterministic (same
   inputs, same findings), invoking each repo's own validators as a
   preflight. Owned by codexFactory (`scripts/` + tests).
2. **Report generator** emitting the contract's report schema: dated
   Markdown at `health/reports/YYYY-MM-DD.md` with `Status: record` +
   `Kind: report`, headline canon-share metric, per-stage counts,
   per-family findings, and the machine-parseable ranked-plan item shape
   (severity, repo, path, suggested action).
3. **Reusable workflow in codexFactory** plus a **thin nightly caller in
   the xFactory aggregation repo** (`--recurse-submodules` checkout,
   nightly cron + manual dispatch) and the `health/reports/` home there.
   This will be the family's FIRST CI.
4. **Issue automation for the regression rule**: new critical/error
   findings vs the previous report (matched by family + path) open one
   aggregation-repo issue per run; persistent findings do not re-open.
5. **Notebook projection drift integration**: run the lifecycle notebook
   sync in dry-run mode and report nonzero operations as drift; family is
   skipped-with-notice when unauthenticated. **Open**: a CI auth strategy
   for nlm (~20-minute sessions; see the projection doc's limitations) —
   until solved, this family runs only in operator-triggered runs.
6. **Threshold configuration** honoring contract defaults, with any
   non-default run stating its deviation in the report.
7. **Fixture-based tests** for every family (a miniature corpus with known
   violations; the checker finds exactly those).

## Decisions the implementation change must make

- **Archive discipline (the release-flow pilot).** This change is the
  family's first with a real code surface. Whether it archives on
  doc-landing (current practice) or on code realization is deliberately
  undecided by the contract change; the proposal must decide it and say
  why. Context (non-normative):
  [openspec-speckit-release-flow brainstorm](../../brainstorm/openspec-speckit-release-flow.md).
- Language/runtime for the checkers (existing family validators are Python
  and shell; pick one and justify).
- Where per-family fixtures live in codexFactory.

## Boundaries already fixed by the contract (do not re-litigate)

- openxFactory owns contract + report schema; changes to families,
  severities, thresholds, or schema are OpenSpec deltas to `doc-health`.
- The pipeline reports and stages; it never approves or merges another
  factory's content.
- Deterministic pass only — no model calls. The semantic sweep is a
  separate future change (`../semantic-health-sweep/`).
- Tag hygiene enforces the `document-lifecycle` grammar by reference.
