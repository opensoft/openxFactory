# Document Catalog And Controlled Tagging Contract

Status: draft
Proposed by: add-document-cataloging
Kind: architecture
Repository context: openxFactory
Target capabilities: `document-cataloging` (ADDED) and `doc-health` (MODIFIED)

## Decision

The shared sweep will catalog every document in its governed catalog corpus,
but it will not insert YAML or inferred tags into each source document.
Cataloging, semantic tag recommendation, and ideation routing are separate
lanes that consume one deterministic inventory:

```text
deterministic document inventory
  -> one mechanical catalog entry for every governed document
  -> structural document-catalog validation

semantic document cataloger
  -> recommends controlled discovery tags for new or changed documents

semantic ideation organizer
  -> may consume current catalog tags as routing signals
  -> recommends routing only for eligible ideation

owning authority
  -> reviews catalog overrides and routing decisions
```

Catalog tags improve retrieval and help identify routing candidates. They do
not assign ownership, approve handling, change lifecycle state, or replace a
routing record.

## Governed Catalog Corpus

Version 1 covers:

- Markdown documents already included in the doc-health inventory under each
  pinned openxFactory or DomainxFactory's `contracts/`, `docs/`, `examples/`,
  `ideation/`, and `templates/` roots; and
- promoted `openspec/specs/*/spec.md` files, represented as
  `artifact_type: promoted_spec`.

The catalog does not expand the governed corpus to install/runtime
repositories, tests, vendored dependencies, generated catalog output, health
reports, archived OpenSpec changes, or non-Markdown files in version 1.
Install/runtime repositories remain resolvable routing destinations, not
catalog-scanning targets.

Every inventory document receives exactly one catalog entry with a canonical
locator: repository ID plus POSIX path when policy permits persistence, or
repository ID plus opaque document reference and path hash when it does not.
Each entry records the current repository revision and content SHA-256 from the
shared inventory snapshot.

## Storage And Immutability

Each main sweep writes full, immutable, per-repository snapshots below:

```text
health/document-catalog/runs/YYYY-MM-DD/<run-id>/
  manifest.yaml
  openxFactory.yaml
  xFactories/MedxFactory.yaml
  xFactories/OpsxFactory.yaml
  ...
```

Slash-separated repository IDs become directories below the run path. Every
snapshot and manifest declares `status: record`. A later run creates a new
snapshot; it never edits a closed snapshot or report.

Semantic cataloger output lands separately as immutable recommendation
evidence:

```text
health/document-catalog/recommendations/YYYY-MM-DD/<job-id>.yaml
```

The next main sweep validates and merges eligible recommendations into its new
full snapshot. The next report finalized after the merge links the snapshot
and recommendation evidence. Temporary workflow artifacts are not the record.

Central xFactory storage is a reporting and retrieval projection. It does not
transfer document authority from the source repository.

## Mechanical Catalog Fields

The deterministic inventory supplies fields that a semantic worker cannot
rewrite:

- canonical repository ID;
- POSIX repository-relative path, or an opaque reference and path hash when
  policy prohibits persisting the path;
- repository revision;
- content SHA-256;
- artifact type;
- `Status`, `Kind`, `Repository context`, and source-declared handling values
  when present; and
- inventory snapshot ID.

A missing or malformed source header remains a deterministic doc-health
finding. The cataloger cannot repair it by inventing a catalog value.

## Controlled Classification Facets

The semantic cataloger may recommend only these discovery facets:

| Facet | Shape | Rule |
|---|---|---|
| `factory_scope` | one of `neutral`, `domain`, `cross_domain`, `aggregation`, `install_runtime`, `unknown` | descriptive only; never ownership |
| `domain_contexts` | canonical repository or registered domain IDs | zero or more contexts mentioned or governed |
| `capability_refs` | repository plus promoted or active OpenSpec capability ID | unresolved capabilities remain unclassified |
| `topic_tags` | registered namespaced tag IDs | unknown values remain proposed, not effective |
| `document_role` | controlled role aligned with `Kind` | does not overwrite the source `Kind` header |
| `sensitivity_signal` | `unspecified` or `potentially_sensitive` | may raise caution only; never declares content safe or lowers source policy |

Initial document roles are `policy`, `contract`, `architecture`, `process`,
`runbook`, `template`, `example`, `evidence`, `register`, `idea`,
`specification`, and `other`.

Topic tags use a versioned registry. Neutral namespaces are owned by
openxFactory in `contracts/document-tag-registry.yaml`; DomainxFactories own
their registered namespaces and publish their tags in
`catalog/document-tag-registry.yaml`. The effective taxonomy is the
deterministic merge of pinned registries. Each snapshot records its effective
taxonomy SHA-256 computed from ordered repository/path/content-hash/version
inputs. Current pinned repository revision and the registry file's
last-modifying revision are retained as provenance but excluded from the digest,
so an unrelated repository commit does not invalidate every classification. A
classifier may propose a new tag, but the tag cannot become effective until the
owning registry accepts it and any namespace, ID, or alias collision is
resolved.

Every inferred facet carries:

- effective taxonomy digest;
- classifier implementation, model, and prompt-contract versions;
- confidence from 0 through 1;
- source method (`classifier`, `declared`, or `override`);
- section reference and passage hash, without requiring raw passage storage;
- `state_since` and state-transition evidence; and
- classification state: `pending`, `suggested`, `reviewed`, `overridden`,
  `unclassified`, or `policy_blocked`.

Model output is never labeled approved. `reviewed` and `overridden` require an
authorized disposition record.

## Application Model

Source Markdown keeps its existing lifecycle headers. No document receives
catalog frontmatter merely because it was inventoried or classified. Catalog
snapshots are external projections keyed to the source revision and content
hash.

Owning Domain Hermes reviews classifications for domain-owned documents.
openxFactory's ratify authority reviews neutral or cross-repository
classifications. An authorized override at
`catalog/document-tag-overrides.yaml` records actor, timestamp, rationale, and
evidence. Overrides are stored in the owning repository and consumed from the
pinned revision; an unauthorized aggregation-side edit has no standing.

An unchanged document may carry forward a reviewed classification when its
locator, content hash, effective taxonomy digest, and prompt compatibility
remain current. The mechanical repository revision updates independently, so
an unrelated commit does not reclassify the whole repository. A changed content
hash re-enters semantic selection and marks prior reviewed results as needing
review rather than silently treating them as current.

## Baseline And Incremental Operation

Before catalog coverage becomes enforceable, one explicit full-corpus backfill
creates the first complete snapshot. The backfill is sharded by repository and
bounded input size, is resumable, and merges deterministically. It must not be
sent as one unbounded model prompt.

After baseline:

1. the nightly deterministic pass emits the shared inventory;
2. a full mechanical snapshot is created for every document;
3. classifications carry forward when locator, content hash, effective
   taxonomy digest, and prompt compatibility remain current, while the
   mechanical repository revision updates independently;
4. new, changed, missing, or stale entries are marked `pending` and selected
   for the semantic cataloger;
5. deleted documents disappear from the new full snapshot while prior
   snapshots remain immutable; a rename is delete plus add unless reviewed
   lineage evidence links it; and
6. validated child recommendations are merged by the next main run.

A weekly deterministic reconciliation checks coverage, deletions, duplicate
keys, taxonomy drift, and stale recommendations. Full semantic
reclassification is manual or required by a breaking taxonomy/prompt change;
it is not an automatic weekly model expense.

Each facet carries `state_since` while its state and semantic identity remain
unchanged. Every validated state transition, including classifier
`pending -> suggested`, resets it. Content/taxonomy/prompt invalidation resets
the facet to pending; if already pending, a recorded `pending -> pending`
invalidation event resets the timestamp for the new semantic input. Pending
semantic classification is a warning at 30 days and an error at 90 days from
that timestamp. The deterministic base entry and report still land if the
cataloger is unavailable.

## Routing Handoff

Only current catalog entries whose repository, path or authorized opaque
resolver, content hash, inventory snapshot, and effective taxonomy digest match
current inputs may inform routing. Policy-blocked or stale tags are ignored.
Signals such as `factory_scope: unknown`, several domain contexts, or a
classification conflict may enqueue ideation-organizer review.

A catalog tag alone must not:

- allocate an Idea ID or Claim ID;
- create or change a routing record;
- set routing `Scope` or `Routing status`;
- select or accept an owner or destination;
- split a claim; or
- move content into staging or a proposal.

A known-owner ordinary document can be richly cataloged without entering
ideation routing.

## Lifecycle And xspec Safety

The cataloger must not add, remove, or recommend:

- `xspec:candidate` or `xspec:supersedes` markers;
- `Status`, `Kind`, or `Repository context` edits;
- Idea IDs, Claim IDs, routing sidecars, or routing transitions;
- promotion, adoption, approval, access, or sensitivity-policy changes; or
- source-document writes of any kind.

`xspec:` markers remain deliberate human/gate selections. Catalog tags are
descriptive retrieval metadata and are not another form of `xspec` tagging.

## Execution And Failure Isolation

The cataloger runs under a dedicated `document-cataloger` bounded read-only
Omnigent profile on the same Cloud PC document-analysis host used by the other
documentation workers. This does not require another Entra user or Cloud PC.
It uses a distinct job type, prompt, schema, artifact lane, and readiness-gated
asynchronous child workflow.

Before dispatch, orchestration compares source-declared handling and
source-domain policy with the target host's attested tenant/data boundary and
handling authorizations. The child receives a self-contained bounded shard only
when that check passes and receives no repository credentials. Redacted input
is permitted only when source policy explicitly authorizes that derived view.
Otherwise, no content or identifying metadata leaves the source boundary and
the facets become `policy_blocked` with an opaque blocker reference.

The main deterministic report and mechanical catalog snapshot complete before
child dispatch. Missing readiness, partial shard failure, invalid output, or an
offline worker records pending coverage and cannot block the deterministic run.

Before persistence, an output-policy filter applies the same restrictions to
paths, inferred tags, topic/domain/capability metadata, sensitivity signals,
and evidence. It replaces prohibited identifiers with opaque references and
hashes and suppresses prohibited values. Raw protected passages or revealing
metadata are not stored centrally when source-domain policy forbids them.

## Reporting

The dated report links the immutable catalog snapshot and states:

- cataloged documents versus inventory total;
- counts by `pending`, `suggested`, `reviewed`, `overridden`, `unclassified`,
  and `policy_blocked` state;
- new, changed, deleted, stale, and rejected-output counts;
- inventory snapshot, taxonomy, classifier, prompt, and model versions;
- recommendation evidence merged since the prior report; and
- skip reasons and non-default configuration.

Catalog recommendations do not enter the doc-health Ranked Plan as findings
and cannot directly open critical/error regression issues. Deterministic
coverage, schema, hash, or provenance violations remain ordinary doc-health
findings.

## Acceptance Tests

- the baseline creates exactly one entry for every governed catalog document;
- an unchanged second run selects no document for semantic classification;
- additions, edits, deletions, and renames produce deterministic diffs;
- an unknown topic or capability is not invented into the effective catalog;
- identical inventory and validated classifier output produce byte-identical
  snapshots;
- no classifier output mutates source documents or `xspec:` markers;
- sensitivity inference can raise caution but cannot declare content safe;
- worker failure leaves complete mechanical entries with pending semantic
  state and does not block the report;
- an unauthorized host receives neither protected content nor identifying
  metadata, and output filtering covers paths and inferred tags as well as raw
  passages;
- only current tags may enqueue routing review, and tags never create routing
  state; and
- a closed snapshot or report is never modified.
