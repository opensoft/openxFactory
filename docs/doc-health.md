# xFactory Doc-Health Contract

Status: standard
Kind: process
Repository context: openxFactory
Backed by: [openspec/specs/doc-health/spec.md](../openspec/specs/doc-health/spec.md) (promoted from the archived add-doc-health-contract change)
Purpose: define the deterministic health-check contract for the factory
family's governance corpus — the check families, the report and ranked-plan
schema, finding severities, aging thresholds, and the ownership split.

Companion contracts: [Document Lifecycle](document-lifecycle.md) (the states,
taxonomy, and `xspec:` marker grammar the checks enforce) and
[Lifecycle Notebook Projection](lifecycle-notebook-projection.md) (whose
sync dry-run is one of the drift checks).

## Scope

This contract covers the **deterministic pass only**: same inputs, same
findings, no model calls. The agentic/semantic sweep (untagged normative
prose, prose-vs-spec contradiction) is a separate active change
(`openspec/changes/add-doc-health-semantic-sweep/`). Implementation lives in
codexFactory; the nightly runner is hosted by the xFactory aggregation
repo; this document and the `doc-health` spec own the contract.

## Check Families

Every run executes twelve families over every family repo the aggregation
repo pins, after running each repo's own validators as a preflight. A
family that cannot run is reported as skipped, never silently omitted.

| # | Family | What it verifies |
| --- | --- | --- |
| 1 | Status validity | Every governance doc carries a `Status:` header from the controlled taxonomy |
| 2 | Standard backing | Every `standard` claim (header or prose) is backed by a promoted spec or canonical contract |
| 3 | Ratified provenance | Every `Ratified by:` resolves to an existing OpenSpec change |
| 4 | Succession integrity | `superseded` docs name successors; `retired` docs name reasons |
| 5 | Location conformance | Lifecycle locations, proposal-support manifests/statuses, archive bundle checksums, and no historical bundles under canonical specs |
| 6 | Record immutability | `record` docs unchanged after capture (link fixes excepted) |
| 7 | Staged/candidate aging | Staged topics, candidate blocks, unmarked supersedes refs, and draft ages against the thresholds below |
| 8 | Register-lifecycle consistency | Candidate register aliases map to lifecycle states; `adopted` entries have no surviving near-duplicates |
| 9 | Tag hygiene | Live `xspec:` markers obey the canonical grammar — as defined by [Document Lifecycle](document-lifecycle.md#prose-tagging-markers), which owns every syntactic detail; this contract never restates it |
| 10 | Submodule pin drift | Aggregation-repo pins vs each submodule's remote main |
| 11 | Contract-copy drift | Domain-local copies vs their canonical openxFactory sources |
| 12 | Notebook projection drift | The lifecycle notebook sync dry-run reports zero add/update/delete operations |

The active `add-document-cataloging` change proposes a thirteenth
deterministic family, `document-catalog`, plus a separate, non-deterministic
`document-cataloger` worker lane that never participates in this pass; see
its
[doc-health spec delta](../openspec/changes/add-document-cataloging/specs/doc-health/spec.md)
for the owned check scope. Until that change promotes, this contract remains
the twelve-family baseline above, and any catalog classification stays
descriptive discovery metadata — never lifecycle, ownership, or approval
authority (see
[Document Lifecycle](document-lifecycle.md#catalog-tags-are-not-lifecycle-state)).

A second active change, `add-cross-factory-ideation-routing`, proposes a
fourteenth deterministic family, `ideation-routing` (sequenced after
`add-document-cataloging`, per that change's own tasks), covering routing
schema and controlled-vocabulary conformance, central Idea-ID and Claim-ID
allocation and uniqueness, legal routing/claim transitions, destination-owner
acceptance, structured repository/path/revision reference resolution, and
routing aging; see its
[doc-health spec delta](../openspec/changes/add-cross-factory-ideation-routing/specs/doc-health/spec.md)
for the owned check scope. Until both changes promote, this contract remains
the twelve-family baseline above, and routing metadata stays descriptive
coordination — never lifecycle, ownership, or approval authority (see
[Document Lifecycle](document-lifecycle.md#cross-factory-ideation-routing)).

## Finding Severities

| Severity | Meaning | Examples |
| --- | --- | --- |
| `critical` | Governance integrity broken | Unbacked `standard` claim; dangling provenance; `record` mutation |
| `error` | Contract violation | Malformed/unresolved marker; free-form status; aging past escalation |
| `warning` | Drift or first-stage aging | Pin drift; copy drift; projection drift; 30-day staged item |
| `info` | Inventory and metrics | Canon share; per-stage counts; age distributions |

**Regression rule:** any `critical` or `error` finding not present in the
previous report (matched by family + path) opens one issue per run in the
aggregation repo listing all new findings. Persistent findings do not
re-open issues. A headline-metric decline is trend data, not a regression.

## Aging Threshold Defaults

| What ages | Warning | Error |
| --- | --- | --- |
| Staged topic untouched | 30 days | 90 days |
| `xspec:candidate` block untouched | 30 days | 90 days |
| `xspec:supersedes` without `change=` | 14 days | 45 days |
| `draft` doc without transition | 60 days | — (age always reported as `info`) |

Defaults are contract surface so reports stay comparable; a run using
non-default thresholds or scope must say so in its report.

## Report Contract

Each run commits a dated Markdown report at `health/reports/YYYY-MM-DD.md`
in the xFactory aggregation repo, carrying `Status: record` +
`Kind: report` (generated evidence, per the lifecycle taxonomy). Contents:

- **Headline metric** — canon share by words: ratified + standard +
  promoted spec words over total governance words.
- **Per-stage counts** and age distributions.
- **Per-family finding sections** for the twelve families.
- **Ranked plan** — every finding as a ready-to-stage work item stating
  severity, repo, path, and suggested action, so report output feeds the
  ideation pipeline's input.

Plain Markdown is v1 by decision (diffable, greppable, zero infrastructure,
flows into the notebook projection); the plan-item shape is
machine-parseable so a later dashboard consumes the same files.

## Ownership

```text
openxFactory      owns the CONTRACT: this document, the doc-health spec,
                  the report schema
codexFactory      owns the IMPLEMENTATION: checker scripts, report
                  generator, reusable workflow
xFactory (root)   HOSTS the nightly runner and health/reports/ (the only
                  repo pinning every submodule)
each domain repo  owns APPROVAL of its own content: the pipeline reports
                  and stages, it never approves or merges
```

Changes to check families, schema, severities, or thresholds are OpenSpec
deltas to the `doc-health` capability here; the implementation follows.

Proposal-support integrity is part of location conformance rather than a
thirteenth family. It reports staged documents that already cite a proposal,
active support folders without valid manifests, `staged` status below an
active proposal, unverifiable archived bundles, and bundles misplaced below
`openspec/specs/`.

## Related Documents

- [Document Lifecycle](document-lifecycle.md) — states, taxonomy, marker
  grammar.
- [Lifecycle Notebook Projection](lifecycle-notebook-projection.md) —
  drift-check target and report distribution surface.
- [Domain Neutralization Candidate Register](domain-neutralization-candidate-register.md)
  — register the consistency family checks.
- Implementation history is retained with the archived doc-health OpenSpec
  changes and their supporting-document manifests.
