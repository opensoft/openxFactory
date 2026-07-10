code_surface: openxFactory, codexFactory, xFactory, DomainxFactories, omnigent-install, cloudpc-install
target_release: implemented

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
