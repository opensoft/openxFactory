code_surface: openxFactory, codexFactory, xFactory, DomainxFactories, omnigent-install, cloudpc-install
target_release: implemented
Status: ratified
Ratified: 2026-07-14 — record: the archive act, commit `20c76cd` "Realize and archive add-document-cataloging (contract-v1.11)", which applied this change's spec delta into `openspec/specs/doc-health/spec.md`, `openspec/specs/document-cataloging/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The commit body records the promotion in words: "Spec deltas folded into openspec/specs/document-cataloging and doc-health". Corroborated, not relied on, by this change's own tasks.md 8.7, which records a Brett gate the same day for a different artifact ("`docs/document-catalog-adoption.md` ratified (Brett's gate 2026-07-14)"). Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The shared document-health inventory identifies governed documents but does not
maintain a durable, controlled discovery catalog. Search, review, and later
routing therefore lack consistent domain, capability, topic, role, and caution
signals, while writing inferred YAML into every source document would confuse
classification with lifecycle and ownership authority.

## What Changes

- Add an external document catalog covering every document in the governed v1
  corpus, with deterministic identity and source metadata plus controlled
  semantic classification facets.
- Add immutable full catalog snapshots, a one-time sharded and resumable
  baseline, and nightly mechanical refresh for additions, edits, deletions,
  renames, and stale classifications.
- Add a deterministic `document-catalog` doc-health family for coverage,
  unique keys, revision/hash freshness, taxonomy, provenance, override
  standing, pending aging, and immutable snapshot validation.
- Add a separate, non-mutating `document-cataloger` Omni lane that returns
  evidence-backed recommendations with confidence, taxonomy digest, and review
  state through a bounded artifact-in/artifact-out contract.
- Keep model output non-authoritative: catalog tags cannot create ownership,
  routing state, `xspec:` markers, sensitivity approval, or lifecycle changes.
- Apply source handling policy and workload-specific host authorization before
  dispatch; prohibited inputs and inferred metadata remain suppressed or
  opaque, and unavailable semantic processing leaves mechanical entries visibly
  pending.
- Publish reusable tag registries and owner-side override conventions for every
  DomainxFactory without adding inferred frontmatter to source documents.
- Reuse the neutral infrastructure-readiness result when that staged contract
  is promoted; this change defines only the cataloger-specific profile and
  capability assertions, not generic Cloud PC administration or outage policy.
- Keep `add-doc-health-semantic-sweep` unchanged and implement this change only
  after that change realizes and archives.

## Capabilities

### New Capabilities

- `document-cataloging`: Defines complete governed-document catalog coverage,
  immutable snapshots, controlled classification facets, semantic tag
  recommendations, owner-reviewed overrides, incremental refresh, protected
  evidence handling, and non-authoritative downstream discovery signals.

### Modified Capabilities

- `doc-health`: Adds deterministic document-catalog validation as the
  thirteenth deterministic check family after the semantic-sweep change
  archives. Semantic cataloging remains a separate worker lane, not another
  semantic finding family.

## Impact

- **openxFactory:** document-catalog and taxonomy contracts, schemas,
  templates, examples, domain guidance, and doc-health requirements.
- **codexFactory:** shared inventory extensions, catalog snapshot and diff
  implementation, deterministic checks, bounded classifier selection,
  validation, tests, and reporting.
- **xFactory aggregation:** nightly mechanical snapshots, asynchronous
  cataloger dispatch, immutable recommendation evidence, and report links.
- **DomainxFactories:** tag-registry and override ownership plus catalog-review
  guidance; existing source documents remain unchanged.
- **omnigent-install and cloudpc-install:** one bounded `document-cataloger`
  profile and workload-specific readiness assertions on the existing document
  analysis host; no additional Entra user or Cloud PC.
- **Compatibility:** the first baseline describes current state without
  fabricating historical tags, and later ideation-routing work may consume only
  current, authorized catalog signals as optional review inputs.
