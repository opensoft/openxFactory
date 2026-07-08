# Design: Doc-Health Contract

## Decision 1: Aging thresholds — concrete contract defaults

The fragments left aging thresholds open ("how long may an item sit
untouched before it counts against health?"). Leaving them to the
implementation would make reports incomparable across runs and versions, so
the defaults are contract surface. Values:

| What ages | Threshold | Severity on breach |
| --- | --- | --- |
| Staged topic (`ideation/staging/<topic>/` fragment) untouched | 30 days | `warning`; escalates to `error` at 90 days |
| `xspec:candidate` block untouched | 30 days | `warning`; escalates to `error` at 90 days |
| `xspec:supersedes` marker without a `change=` attribute | 14 days | `warning`; escalates to `error` at 45 days |
| `draft`-status document without a lifecycle transition | always reported (`info` age distribution) | `warning` at 60 days |

Rationale:

- The observed cadence of the lifecycle stack itself (capture to ratified
  within days, per the change history of `add-document-lifecycle-vocabulary`
  and `concretize-prose-tagging-syntax`) says healthy items move in
  well under a month; 30 days is a generous multiple, not a deadline.
- The supersedes threshold is tighter (14 days) because an unmarked-change
  supersedes marker is live divergence from promoted policy — the marker
  exists precisely to bridge the short gap until a change id exists
  (`document-lifecycle` aging scenario). Divergence is costlier than idle
  staging.
- Drafts never expire — `draft` is a legitimate long-lived state — so
  drafts get age *reporting* always and a `warning` only at 60 days,
  feeding the ranked plan rather than demanding action.
- Escalation (warning, then error) makes aging regression-visible: crossing
  the escalation boundary is a new `error` finding, which opens an issue
  under the regression rule.
- Thresholds are contract defaults: the implementation MAY make them
  configurable, but a report produced with non-default thresholds MUST say
  so, or cross-run comparisons silently lie.

## Decision 2: Report format — plain Markdown v1, committed

The fragments' second open question: report visualization. **Decision:
plain Markdown, committed at `health/reports/YYYY-MM-DD.md` in the xFactory
aggregation repo. Dashboard artifact later.**

- Committed Markdown needs zero new infrastructure, is diffable (yesterday
  vs today is `git diff`), greppable, and readable in every surface the
  family already uses — including the NotebookLM projection.
- The report is generated evidence, so per the `document-lifecycle`
  taxonomy each report file carries `Status: record` + `Kind: report` and
  is excluded from conversion and contradiction checks. The health pipeline
  producing docs that violate the doc taxonomy would be self-refuting.
- The aggregation repo is the right home: it is the only repo that pins all
  submodules, so whole-family health is aggregation-repo work product, and
  reports sit next to the workflow that produces them.
- A dashboard (or Hermes surface) is deferred, not rejected: the ranked
  plan section is deliberately machine-parseable (one finding per list
  item with severity, repo, path, and suggested action) so a later
  visualization consumes the same files without a schema break.

## Decision 3: Severity model and the regression rule

Four levels, keyed to what the reader must do:

- `critical` — governance integrity broken: unbacked `standard` claim,
  dangling `Ratified by:` provenance, `record` mutation. Fix is not
  optional.
- `error` — contract violation: malformed or unresolved `xspec:` marker,
  free-form status value, register-lifecycle inconsistency, aging past
  escalation.
- `warning` — drift and aging within escalation: pin drift, contract-copy
  drift, projection drift, first-stage aging.
- `info` — inventory and metrics: canon share, per-stage counts, age
  distributions.

Regression = any finding at `error` or above that was not in the previous
report (matched by check family + path). Regression opens one issue per run
in the aggregation repo listing the new findings; unchanged findings do not
re-open issues (no alert fatigue). The headline metric declining is not
itself a regression — it trends in the report — because canon share moves
for legitimate reasons (new brainstorm capture lowers it).

## Decision 4: Tag hygiene by reference, not restatement

The tag-hygiene family enforces the canonical `xspec:` grammar exactly as
`document-lifecycle` defines it (Prose Tagging Markers section of
`docs/document-lifecycle.md`; grammar concretized by
`concretize-prose-tagging-syntax`). This capability deliberately does not
restate the grammar: restating it would create a second normative copy that
could drift — the exact accidental-restatement defect the explicit-delta
rule (and this pipeline) exists to catch. The contract doc and spec name
the check obligations (well-formedness, target resolution, fence structure,
code-fence/inline-code exclusion, doc-level candidacy ban, supersedes
aging) and point at the grammar's owner for every syntactic detail.

## Decision 5: Scope — deterministic pass only

This capability covers only the deterministic pass: same inputs, same
findings, no model calls. The agentic/semantic sweep (untagged normative
prose, prose-vs-spec contradiction) stays in
`ideation/staging/semantic-health-sweep/` for its own future change. The
split keeps this contract testable and keeps the first implementation
change small. The notebook projection drift check is deterministic (the
sync script's dry-run reports add/update/delete counts; nonzero = drift)
and therefore belongs here even though it touches an external service.

## Context noted, not policy

`ideation/brainstorm/openspec-speckit-release-flow.md` (Status: brainstorm)
sketches a two-axis release-flow model in which changes with a code surface
archive on code realization rather than doc landing. It is cited only to
mark the follow-on implementation change as that model's pilot case; no
requirement in this change depends on it, and this change itself is
doc-only and archives on doc landing under current practice.
