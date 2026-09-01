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
this repository (`scripts/doc_health/`, adopted from codexFactory by
`adopt-neutral-tooling-home`); the nightly runner is hosted by the xFactory
aggregation repo; this document and the `doc-health` spec own the contract.

## Check Families

Every run executes twenty-three families over every family repo the aggregation
repo pins, after running each repo's own validators as a preflight. A
family that cannot run is reported as skipped, never silently omitted.

**The table below is knowingly incomplete.** It carries the original twelve
plus the eighteenth, `promotion-fidelity`, whose spec delta is one of the
deltas that raised the count above. Families 13 through 17, and the
nineteenth through twenty-third (`release-inventory-drift`,
`duplicate-packet`, `family-enumeration`, `modified-block-currency`,
`release-tag-publication`), each
reached the `doc-health` spec by delta and never reached this table — which
is also why the two paragraphs after it still describe families 13 and 14,
and the notes further below describe families 20 through 23, by the
changes that added them rather than by a table row. Repairing that backlog
belongs to a change that owns those families; it is a named standing gap,
recorded in the archived `add-promotion-fidelity-check` §5.2, not an
oversight here.

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
| 18 | Promotion fidelity | Every archived spec delta reached the promoted spec it was ratified to reach — the requirement title and every scenario stated under it, and a ratified removal actually removed. The most recent archived delta is the authority; only a packet whose own `proposal.md` declares `draft` or a lower standing is exempt. Findings are `error`, classified `contested`, and reported against the archived delta's own path |

The archived `add-document-cataloging` change added a thirteenth
deterministic family, `document-catalog`, plus a separate, non-deterministic
`document-cataloger` worker lane that never participates in this pass; see
its
[doc-health spec delta](../openspec/changes/archive/2026-07-14-add-document-cataloging/specs/doc-health/spec.md)
for the owned check scope. Its table registration never landed — see the
disclosure paragraph above — and any catalog classification stays
descriptive discovery metadata — never lifecycle, ownership, or approval
authority (see
[Document Lifecycle](document-lifecycle.md#catalog-tags-are-not-lifecycle-state)).

A second archived change, `add-cross-factory-ideation-routing`, added a
fourteenth deterministic family, `ideation-routing` (sequenced after
`add-document-cataloging`, per that change's own tasks), covering routing
schema and controlled-vocabulary conformance, central Idea-ID and Claim-ID
allocation and uniqueness, legal routing/claim transitions, destination-owner
acceptance, structured repository/path/revision reference resolution, and
routing aging; see its
[doc-health spec delta](../openspec/changes/archive/2026-08-06-add-cross-factory-ideation-routing/specs/doc-health/spec.md)
for the owned check scope. Its table registration never landed either, and
routing metadata stays descriptive coordination — never lifecycle,
ownership, or approval authority (see
[Document Lifecycle](document-lifecycle.md#cross-factory-ideation-routing)).

The archived
[`2026-08-25-add-duplicate-packet-check`](../openspec/changes/archive/2026-08-25-add-duplicate-packet-check/specs/doc-health/spec.md)
change added a twentieth deterministic family, `duplicate-packet`, comparing
every repository's archived spec deltas against each other for the same
ruling recorded twice, per the canon `Requirement: One ruling, one discharge,
across archived packets` in
[`openspec/specs/doc-health/spec.md`](../openspec/specs/doc-health/spec.md).

The archived
[`2026-08-27-add-family-enumeration-check`](../openspec/changes/archive/2026-08-27-add-family-enumeration-check/specs/doc-health/spec.md)
change added a twenty-first deterministic family, `family-enumeration`,
verifying this very section's family count and roster against the code
registry rather than trusting either on prose alone, per the canon
`Requirement: The family enumeration is derived, not restated on trust` in
[`openspec/specs/doc-health/spec.md`](../openspec/specs/doc-health/spec.md).

The archived
[`2026-08-27-add-modified-block-currency-check`](../openspec/changes/archive/2026-08-27-add-modified-block-currency-check/specs/doc-health/spec.md)
change added a twenty-second deterministic family, `modified-block-currency`
(launched ADVISORY; the gate-bearing scenario-title arm flipped to `error`
and the family joined `FAMILY_RESOLUTION` on 2026-08-31, issue #357, once the
measured population read zero), comparing an active change's `MODIFIED
Requirements` blocks against the promoted requirements they replace across
three arms plus a marker-defect class, per the canon `Requirement: Currency
of an active change's MODIFIED requirement blocks` in
[`openspec/specs/doc-health/spec.md`](../openspec/specs/doc-health/spec.md);
the archived
[`2026-08-28-add-unclassified-finding-class`](../openspec/changes/archive/2026-08-28-add-unclassified-finding-class/specs/doc-health/spec.md)
change then added a fifth `unplaced` class for findings its own arms/
marker-defect map cannot place, per the canon `Requirement: A
modified-block-currency finding its own class map cannot place is itself a
finding`. The ratified
[`govern-sibling-added-modified-deltas`](../openspec/changes/govern-sibling-added-modified-deltas/proposal.md)
change adds a SIXTH and a SEVENTH class, both `warning` at launch and both
inserted BEFORE `unplaced` so that the gate-bearing arm still reads first and
the drift class still reads last: `sibling-pairing`, which evaluates the
PAIRING — never the carriage — of a MODIFIED block whose title only an active
sibling's `ADDED` (or a rename's `TO:` half) supplies, in four reported states
(self-referential, undeclared, misdeclared, undisclosed) and silent on a
correctly declared pair, per the canon `Requirement: A MODIFIED block over an
active sibling's addition is evaluated for its pairing, not for its carriage`;
and `added-over-canon`, the archive-ordering backstop, which reports an active
`## ADDED Requirements` block — or an active rename's `TO:` title — naming a
requirement the promoted specification ALREADY carries, per the canon
`Requirement: An active block writing a title the promoted specification
already carries is reported`. The three comparison arms still do NOT run
against a pending block: the pairing class reads a delta's own markers and the
set of active additions, and compares no requirement text at all. The declaring
marker is `document-lifecycle`'s third reserved form,
``**Modified over `<basis change-id>`'s addition by <change-id>
(<YYYY-MM-DD>):**`` followed by ` — <reason>`, which names no units and is
therefore never a suppression, never a marker defect and never a carriage unit.

[`add-release-tag-publication-check`](../openspec/changes/add-release-tag-publication-check/proposal.md)
added a twenty-third deterministic family, `release-tag-publication`, per the
canon `Requirement: Release-tag publication`. It asks the one question
`docs/contract-versioning-policy.md` states absolutely and nothing checked —
"a bundle is not published until its tag exists" — for every repository in
scope declaring a bundle at or above the `contract-v1.7` enforcement line:
does that bundle have a PUBLISHED ANNOTATED tag, and does it peel to a commit
that declares the bundle? It is DISTANCE-GRADED in first-parent landings on
published `main` (silent while the declaring commit is still the tip, since
the owner's tag act legitimately follows the cut; `warning` after that;
`error` past **five**, ruled 2026-08-31), and it splits an ABSENT tag from a
MISPLACED one — a tag on a non-declaring commit satisfies every check that
asks only whether a tag exists, and is what consumers pin. Its action line:
*publish the annotated tag at the commit the versioning policy's rule
identifies — the earliest first-parent commit on published main that declares
the bundle and at which verify-commit passes — never edit the manifest, the
changelog or the inventory to match the absence*. The gap it closes reached
`contract-v1.33`/`v1.35`/`v1.39` in August and recurred on `contract-v2.3`
and `contract-v2.4`; a human found it both times (issue #528).

## Finding Severities

| Severity | Meaning | Examples |
| --- | --- | --- |
| `critical` | Governance integrity broken | Unbacked `standard` claim; dangling provenance; `record` mutation |
| `error` | Contract violation | Malformed/unresolved marker; free-form status; aging past escalation; a ratified spec delta that never reached its promoted spec |
| `warning` | Drift or first-stage aging | Pin drift; copy drift; projection drift; 30-day staged item |
| `info` | Inventory and metrics | Canon share; per-stage counts; age distributions |

**Regression rule:** any `critical` or `error` finding not present in the
previous report (matched by family + path) opens one issue per run in the
aggregation repo listing all new findings. Persistent findings do not
re-open issues. A headline-metric decline is trend data, not a regression.

**Identity check (issue #342):** a report is stamped with the repo(s) the
run covered (`Repo-Identity:` header line); `--previous-report` REFUSES a
stamped baseline whose identity does not cover this run's scope, with a
nonzero exit — otherwise every finding key misses by construction and a
benign path/scope slip reports as mass regressions and uncited-resolution
errors. A baseline written before this stamp existed is still accepted
(with a warning), so the check phases in without breaking an in-flight
nightly.

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
`Kind: report`, plus a `Repo-Identity:` line naming the repo(s) the run
covered (generated evidence, per the lifecycle taxonomy; see "Identity
check" above). Contents:

- **Headline metric** — canon share by words: ratified + standard +
  promoted spec words over total governance words.
- **Per-stage counts** and age distributions.
- **Per-family finding sections** for every family the run executed.
- **The promotion fidelity measurement basis**, stated in that family's own
  section on every run and whether or not it found anything: the pinned
  checkout by default — the same tree every other family measures — or each
  repository's own live `main` where the run is configured for it, naming
  any repository whose live `main` could not be read and was measured from
  its checkout instead.
- **Ranked plan** — every finding as a ready-to-stage work item stating
  severity, repo, path, and suggested action, so report output feeds the
  ideation pipeline's input.

Plain Markdown is v1 by decision (diffable, greppable, zero infrastructure,
flows into the notebook projection); the plan-item shape is
machine-parseable so a later dashboard consumes the same files.

## Ownership

```text
openxFactory      owns the CONTRACT (this document, the doc-health spec,
                  the report schema) AND the IMPLEMENTATION: checker
                  scripts, report generator, reusable workflow
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

## Neutrality-Drift Lane

Ratified by `add-neutrality-drift-lane` (2026-08-04) as a MODIFIED
`doc-health` requirement: a nightly, incremental, model-driven lane beside
the deterministic families — the standing scout for domain-factory content
that belongs in openxFactory. Families/lanes overview row:

| Lane | Scope | Stage 1 (deterministic) | Stage 2 (model) | Output |
| --- | --- | --- | --- | --- |
| `neutrality-drift` | pinned `xFactories/*` domain repos only (never openxFactory, openAvatar, or installs in v1) | near-duplicate of a neutral artifact (token-set similarity, `contract-copy-drift` generalized), zero domain-lexicon hits in a schema/script (lexicon from the repo's own identity + ontology), cross-repo consumers, stack.yaml-uninventoried `scripts/` tooling | bounded batch of new/changed survivors judged under `scripts/doc_health/neutrality-prompt.md` ("would another domain need this essentially unchanged?") | drafted DTN-register seed (row + detail section, the register's own format) + ranked-plan items |

**Approval flow** (nothing moves automatically — ever): candidates land in
the rolling health PR as drafted register-seed text (persisted under
`health/neutrality-drift/seeds/` in this repo) plus contested WARNING
ranked-plan items. Brett's approval of a seed is his merge of the register
addition; movement then follows the
[Domain-To-Neutral Promotion Process](domain-to-neutral-promotion-process.md)
(staged topic → OpenSpec change → tranche moves), never the nightly. The
lane's write surface is exactly its own `health/neutrality-drift/` tree
(state, baseline markers, drafted seeds) plus the dated report — it never
edits a domain repo, the register, or any contract.

**Dispositions keying**: a rejected candidate gets an entry in the
aggregation repo's existing `health/dispositions.yaml` — the same
vocabulary every contested resolution uses, extended for this lane with a
content digest — keyed `family: neutrality-drift`, `repo`, `path`,
`content_sha256`, plus the required `cite`. Suppression holds while the
content is unchanged; a changed digest re-files the candidate.

**Incremental state**: `health/neutrality-drift/state.yaml` records each
repo's last-run commit and judged content digests;
`health/neutrality-drift/baseline/<repo>.yaml` is the recorded baseline
marker for a completed full sweep (codexFactory's cites the 2026-08-03
manual sweep). The reusable nightly exposes `neutrality-drift` (opt-out,
default on) and `neutrality-baseline` (manual full-sweep repo) inputs; with
no omnigent worker host the lane records a skip note and stage-1 counts
only, never an error.

## Related Documents

- [Document Lifecycle](document-lifecycle.md) — states, taxonomy, marker
  grammar.
- [Lifecycle Notebook Projection](lifecycle-notebook-projection.md) —
  drift-check target and report distribution surface.
- [Domain Neutralization Candidate Register](domain-neutralization-candidate-register.md)
  — register the consistency family checks.
- Implementation history is retained with the archived doc-health OpenSpec
  changes and their supporting-document manifests.
