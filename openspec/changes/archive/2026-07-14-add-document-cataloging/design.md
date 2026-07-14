## Context

The deterministic document-health pass already emits an inventory keyed by
repository, path, status, and content hash. It does not retain a controlled,
queryable catalog or classification history. The earlier combined routing
proposal proved that cataloging is useful on its own: ordinary known-owner
documents need discovery metadata even when they never enter ideation routing.

This change therefore owns catalog coverage, taxonomy, classification,
snapshots, and the cataloger worker. It does not own Idea IDs, Claim IDs,
routing records, organizer recommendations, or lifecycle movement. A later
ideation-routing change may consume current catalog entries as optional signals
without making those entries authoritative.

The active `add-doc-health-semantic-sweep` change is still awaiting Cloud PC
realization. Catalog implementation starts after that change archives, reusing
its bounded worker and artifact-transfer pattern without editing its scope.

Stakeholders are document authors, corpus users, Domain Hermes authorities,
openxFactory ratify authority, codexFactory document-engineering workers, and
operators reviewing catalog recommendations.

## Goals / Non-Goals

**Goals:**

- Give every governed v1 document one deterministic external catalog entry.
- Maintain immutable, reproducible catalog snapshots outside source repos.
- Classify documents through controlled, evidence-backed discovery facets.
- Preserve owner authority over reviewed values and overrides.
- Detect catalog coverage, freshness, taxonomy, provenance, and aging defects
  deterministically.
- Keep semantic classification bounded, asynchronous, and non-blocking.
- Prevent source handling policy or inferred protected metadata from leaking
  through catalog processing.
- Preserve stable classifications across unrelated repository commits.

**Non-Goals:**

- Adding inferred YAML or frontmatter to source Markdown.
- Assigning document ownership or lifecycle status.
- Creating routing records, Idea IDs, Claim IDs, or `xspec:` markers.
- Scanning install/runtime repos, tests, generated health records, archives, or
  non-Markdown files in v1.
- Reclassifying the full corpus semantically every night.
- Defining generic Cloud PC administration, readiness-result, or outage policy.
- Making semantic recommendations merge-blocking in v1.

## Decisions

### 1. Catalog the governed Markdown corpus plus promoted specs

Version 1 uses the existing doc-health roots in openxFactory and pinned
DomainxFactories (`contracts/`, `docs/`, `examples/`, `ideation/`, and
`templates/`) and adds promoted `openspec/specs/*/spec.md` documents. Generated
catalog output, reports, tests, archives, vendored content, non-Markdown files,
and install/runtime repositories remain excluded.

This keeps coverage aligned with the governed corpus and avoids turning a
document-governance change into an enterprise file index.

### 2. Store full immutable snapshots in the aggregation repository

Each main run writes a complete per-repository snapshot under:

```text
health/document-catalog/runs/YYYY-MM-DD/<run-id>/
```

The aggregation repository is the reporting projection because it already pins
the participating repositories. A snapshot records source authority; it does
not transfer that authority. Closed snapshots and reports are never edited.

Alternative: write current catalogs into each submodule. Rejected because the
aggregation runner would need to mutate source repositories it does not own.

### 3. Mechanical identity is separate from semantic classification

The deterministic inventory supplies repository ID, POSIX path or authorized
opaque locator, repository revision, content hash, artifact type, source
headers, and snapshot ID. Semantic output cannot rewrite those fields.

Every inferred facet records taxonomy, classifier, model and prompt versions,
confidence, evidence reference, source method, state, and `state_since`.
Malformed source headers remain doc-health findings rather than being repaired
inside the catalog.

### 4. Controlled facets are descriptive, not authoritative

The v1 facets are `factory_scope`, `domain_contexts`, structured
`capability_refs`, namespaced `topic_tags`, `document_role`, and the one-way
`sensitivity_signal`. The last may raise caution to `potentially_sensitive` but
can never lower source policy or declare content safe.

Model output begins as `suggested`. Only an authorized disposition can produce
`reviewed` or `overridden`. Catalog values do not assign ownership, approve
handling, change lifecycle state, or create executable authority.

### 5. Taxonomy registries remain owner-scoped

openxFactory owns neutral namespaces. Each DomainxFactory owns its registered
domain namespaces and publishes its registry in the owning repository. The
effective taxonomy is the deterministic merge of pinned registries.

Its digest uses ordered registry repository, path, content hash, and registry
version. Repository revisions remain provenance but are excluded from the
digest so unrelated commits do not invalidate every classification.

### 6. Owner overrides live with the owning repository

Domain Hermes reviews domain classifications; openxFactory ratify authority
reviews neutral or cross-repository classifications. Overrides record actor,
time, rationale, and evidence in the owning repository. Aggregation-side edits
without owner evidence have no standing.

### 7. Baseline is sharded, resumable, and explicitly gated

The first full-corpus baseline is split by repository and bounded input size.
Progress is durable and merges deterministically. Complete-coverage enforcement
is disabled until the baseline proves exactly one mechanical entry per governed
document.

After baseline, every nightly run creates a full mechanical snapshot while the
semantic selector sends only new, content-changed, missing, pending, or
taxonomy/prompt-incompatible entries to the cataloger.

### 8. Diffs include deletion and rename-as-delete-plus-add

Inventory comparison detects additions, edits, deletions, and renames. A rename
is deletion plus addition unless reviewed lineage evidence links it. Prior
snapshots remain immutable and retain historical locations.

Classification carry-forward depends on locator, content hash, effective
taxonomy digest, and prompt compatibility—not on an unrelated repository HEAD
change.

### 9. Pending aging is tracked per facet

Each facet preserves `state_since` while its semantic identity and state remain
unchanged. A validated state transition resets it. Content, taxonomy, or prompt
invalidation also resets it; an already-pending facet records a
`pending -> pending` invalidation event for the new input.

Pending classification is a warning after 30 days and an error after 90 days.
The mechanical entry and report still land while semantic work is unavailable.

### 10. The cataloger is a distinct bounded worker lane

The `document-cataloger` profile has its own prompt, schema, job type, artifact
lane, timeouts, concurrency, and capability advertisement. It receives a
self-contained bounded shard and no repository or factory credentials. Output
is schema-validated before orchestration persists immutable recommendation
evidence under:

```text
health/document-catalog/recommendations/YYYY-MM-DD/<job-id>.yaml
```

The next main run validates and merges eligible recommendations into a new
snapshot. Temporary workflow artifacts are not records.

### 11. Generic readiness is consumed, not redefined

The staged Client Infrastructure Liaison contract owns the neutral
`infrastructure_readiness_result`, trusted validators, expiry, and remediation
handoff. This change adds only cataloger-specific mandatory assertions:
eligible runner state, current worker heartbeat, matching profile/version,
tenant/data boundary, handling authorization, and absence of repository
credentials.

Until the neutral readiness contract is promoted, implementation may use the
existing semantic-sweep preflight shape but must not introduce a competing
generic readiness schema.

### 12. Handling policy gates both input and output

Orchestration compares source handling and source-domain policy to the target
host's workload-specific authorization before uploading content or identifying
metadata. Redacted input is used only when source policy explicitly permits the
derived view. Otherwise the entry remains `policy_blocked` with an authorized
opaque blocker reference.

Output filtering covers paths, inferred tags, summaries, and evidence because
metadata may itself disclose protected facts.

### 13. Semantic work is asynchronous and failure-isolated

The main run finishes the deterministic catalog family, mechanical snapshot,
and report before dispatching an independent cataloger child. Offline,
unauthorized, partial, stale, timed-out, or invalid child work leaves selected
entries pending and cannot delay deterministic finalization.

A watchdog reports and cancels a child queued beyond ten minutes or running
beyond thirty minutes. Non-default thresholds are reported.

### 14. Downstream routing signals are optional and read-only

A later routing capability may consume a catalog signal only when its locator
or authorized resolver, content hash, inventory snapshot, and taxonomy digest
are current and the entry is not policy-blocked. The catalog itself never
allocates routing identifiers, chooses an owner or destination, or moves source
content.

## Risks / Trade-offs

- **Large first baseline** → shard by repository and size, checkpoint progress,
  and enable coverage enforcement only after deterministic merge verification.
- **Taxonomy churn invalidates excessive work** → use a content-based taxonomy
  digest and require explicit breaking-change classification.
- **Central projection appears authoritative** → retain source revision,
  owning authority, and override standing in every entry and guide.
- **Inferred metadata leaks protected context** → gate before dispatch and
  filter locators, tags, summaries, and evidence on return.
- **Worker outage creates a growing pending queue** → keep mechanical coverage
  complete, report per-facet aging, and expose readiness/remediation evidence.
- **Two changes modify doc-health family enumeration** → archive the semantic
  sweep first, catalog as family thirteen, then let ideation routing add family
  fourteen against the promoted catalog wording.

## Migration Plan

1. Finish and archive `add-doc-health-semantic-sweep`.
2. Promote catalog contracts, schemas, registry templates, and validators.
3. Extend the shared inventory and prove deterministic add/edit/delete diffs.
4. Run the sharded baseline without enforcing complete coverage.
5. Verify one mechanical entry per governed v1 document and enable the
   `document-catalog` family.
6. Enable incremental cataloger dispatch only after workload readiness and
   handling-policy checks pass.
7. Publish DomainxFactory registry and override guidance, then re-pin consumers.

Rollback disables semantic dispatch and complete-coverage enforcement while
retaining immutable snapshots as records. Source documents require no rollback
because the catalog never mutates them.

## Open Questions

- Whether the first production taxonomy needs additional neutral namespaces is
  decided through reviewed registry additions, not by expanding this proposal.
- Catalog-to-routing signal integration remains optional until the separate
  ideation-routing change defines its exact consumer gate.
