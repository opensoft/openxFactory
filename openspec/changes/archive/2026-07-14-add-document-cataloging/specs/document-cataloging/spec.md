# document-cataloging Specification

## ADDED Requirements

### Requirement: Governed document catalog coverage
Every document in the governed catalog corpus SHALL have exactly one entry in
each complete catalog snapshot for its repository. The v1 corpus SHALL contain
the Markdown documents from the shared doc-health inventory under
`contracts/`, `docs/`, `examples/`, `ideation/`, and `templates/` in
openxFactory and every pinned DomainxFactory, plus promoted
`openspec/specs/*/spec.md` files. Catalog output, health reports, archived
OpenSpec changes, tests, install/runtime repositories, vendored content,
non-Markdown files, and generated records outside that inventory SHALL remain
outside v1 semantic cataloging.

Each entry SHALL carry a canonical document locator: repository ID plus POSIX
repository-relative path when policy permits persistence, or repository ID plus
an opaque document reference and path SHA-256 when policy prohibits storing the
path. It SHALL also carry current repository revision, content SHA-256,
artifact type, and inventory snapshot. Each main run SHALL write full,
immutable, per-repository snapshots under
`health/document-catalog/runs/YYYY-MM-DD/<run-id>/`, with slash-separated
repository IDs represented as subdirectories and every snapshot declaring
`status: record`.

#### Scenario: Complete inventory is cataloged
- **WHEN** a main sweep emits its governed inventory
- **THEN** the corresponding run snapshot MUST contain exactly one entry for every inventory document and promoted spec

#### Scenario: Catalog entry is missing or duplicated
- **WHEN** a canonical or policy-opaque document locator is absent or appears more than once in a complete snapshot
- **THEN** deterministic document-catalog validation MUST emit a coverage finding

#### Scenario: Catalog entry is stale
- **WHEN** an entry's repository revision, canonical/opaque locator, or content hash does not match its source inventory entry
- **THEN** deterministic validation MUST reject it as current catalog evidence

#### Scenario: Path persistence is prohibited
- **WHEN** source policy forbids storing a repository-relative path in the aggregation catalog
- **THEN** the entry MUST use one authorized opaque document reference and path SHA-256 and MUST omit the path

#### Scenario: Locator is ambiguous
- **WHEN** an entry supplies both a persisted path and an opaque reference, or supplies neither
- **THEN** deterministic validation MUST reject the locator

#### Scenario: Document is deleted or renamed
- **WHEN** a later inventory omits a prior path or represents a rename as a new path
- **THEN** the new full snapshot MUST omit the deleted key and add the new key
- **AND** prior immutable snapshots MUST remain unchanged
- **AND** a rename MUST be treated as delete plus add unless reviewed lineage evidence links the paths

#### Scenario: Generated catalog is encountered
- **WHEN** corpus discovery reaches catalog snapshots or recommendation evidence
- **THEN** those generated records MUST be excluded so the catalog cannot recursively catalog itself

### Requirement: Controlled classification facets and provenance
Catalog classification SHALL use only the controlled facets
`factory_scope`, `domain_contexts`, `capability_refs`, `topic_tags`,
`document_role`, and `sensitivity_signal`. `factory_scope` SHALL be one of
`neutral`, `domain`, `cross_domain`, `aggregation`, `install_runtime`, or
`unknown`; capability references SHALL name a canonical repository and a
promoted or active OpenSpec capability; topic tags SHALL resolve through a
versioned namespaced registry; document roles SHALL be `policy`, `contract`,
`architecture`, `process`, `runbook`, `template`, `example`, `evidence`,
`register`, `idea`, `specification`, or `other`; and sensitivity signals SHALL
be only `unspecified` or `potentially_sensitive`.

The neutral registry at
`openxFactory/contracts/document-tag-registry.yaml` SHALL register namespace
owners and neutral tags. A DomainxFactory MAY define tags only in its owned
namespace at `catalog/document-tag-registry.yaml`. The effective registry SHALL
be the deterministic merge of pinned registries; duplicate IDs, aliases, or
namespace ownership claims SHALL be invalid. Every snapshot SHALL record an
effective taxonomy SHA-256 computed from the ordered canonical repository,
path, registry content hash, and registry-version inputs. Each input SHALL also
record the current pinned repository revision and the registry file's
last-modifying revision as provenance, but neither revision SHALL alter the
digest when registry content and version are unchanged.

Source-derived `Status`, `Kind`, `Repository context`, and any declared
handling classification SHALL remain mechanical inventory fields and MUST NOT
be semantically rewritten. Every inferred facet SHALL record the effective
taxonomy digest, classifier implementation, model, and prompt versions;
confidence from 0 through 1; source method; section and passage-hash evidence;
`state_since`; state transitions; and one state from `pending`, `suggested`,
`reviewed`, `overridden`, `unclassified`, or `policy_blocked`. Model output
SHALL be `suggested`, never approved.

#### Scenario: Controlled tags are recommended
- **WHEN** the classifier emits a catalog recommendation
- **THEN** every facet value MUST satisfy its controlled vocabulary and carry versioned provenance, confidence, evidence, and `suggested` state

#### Scenario: Topic tag is unknown
- **WHEN** a recommendation names a topic absent from the applicable namespace registry
- **THEN** it MUST remain a proposed tag and MUST NOT enter the effective catalog until the owning registry accepts it

#### Scenario: Namespace ownership collides
- **WHEN** two registries claim the same namespace, tag ID, or alias without one canonical owner
- **THEN** deterministic taxonomy validation MUST reject the effective registry

#### Scenario: Taxonomy inputs are incomplete
- **WHEN** a snapshot lacks the effective taxonomy digest or an ordered pinned-registry input
- **THEN** deterministic validation MUST reject its taxonomy provenance

#### Scenario: Registry repository changes elsewhere
- **WHEN** a repository's pinned revision changes but the registry file content hash and registry version do not
- **THEN** the taxonomy provenance MUST record the new pinned revision while the effective digest remains unchanged
- **AND** catalog entries MUST NOT be reclassified for that unrelated commit

#### Scenario: Capability cannot resolve
- **WHEN** a recommendation names no promoted or active capability in the referenced repository
- **THEN** that facet MUST remain `unclassified` rather than inventing a capability

#### Scenario: Classifier disagrees with a source header
- **WHEN** inferred role or context conflicts with source `Kind` or `Repository context`
- **THEN** the source value MUST remain unchanged and the semantic disagreement MAY be recorded as a suggestion for review

#### Scenario: Sensitivity inference lowers caution
- **WHEN** a classifier attempts to mark content safe, public, or less restricted than source policy
- **THEN** the output MUST be rejected because semantic classification may only raise `potentially_sensitive` caution

### Requirement: External catalog application and disposition authority
Catalog tags SHALL live in aggregation-hosted catalog snapshots rather than
source-document YAML or frontmatter. Suggested tags SHALL be descriptive
retrieval metadata only and MUST NOT assign document ownership, destination
acceptance, lifecycle status, promotion, access, handling policy, approval, or
routing state.

Domain Hermes SHALL review classifications for domain-owned documents;
openxFactory ratify authority SHALL review neutral or cross-repository
classifications. Authorized overrides SHALL be committed in the owning
repository at `catalog/document-tag-overrides.yaml` with document path, source
hash, actor, timestamp, rationale, and evidence. Aggregation-side edits or
actors without standing MUST NOT create `reviewed` or `overridden` state. A
content-hash change SHALL mark a prior reviewed result stale until renewed or
replaced.

#### Scenario: Ordinary document is cataloged
- **WHEN** an ordinary governance document enters the inventory
- **THEN** it MUST receive an external catalog entry without any source-document edit

#### Scenario: Domain classification is reviewed
- **WHEN** the owning Domain Hermes records an override against the matching path and content hash
- **THEN** the next snapshot MAY mark the affected classification `reviewed` or `overridden` and MUST cite the override

#### Scenario: Unauthorized override is supplied
- **WHEN** an aggregation actor or non-owning layer attempts to dispose a domain classification
- **THEN** the override MUST be ignored and the catalog MUST retain the prior state

#### Scenario: Source content changes after review
- **WHEN** a reviewed entry's source content hash changes
- **THEN** the new entry MUST re-enter classification and MUST NOT silently retain current reviewed standing

### Requirement: Full baseline and incremental refresh
Document cataloging SHALL begin with one explicit, sharded, resumable
full-corpus baseline before complete-coverage enforcement is enabled. During
baseline, the report SHALL state progress without opening one issue per legacy
document. After baseline, every nightly main run SHALL create a full mechanical
snapshot from the shared inventory and update each entry's current repository
revision. It SHALL carry classification forward when canonical repository ID,
path or opaque locator, content hash, effective taxonomy digest, and
prompt-contract compatibility remain unchanged; an unrelated repository commit
MUST NOT force reclassification. It SHALL select only new, content-changed,
missing, pending, or taxonomy/prompt-incompatible entries for semantic
classification.

Selection SHALL detect additions, modifications, and deletions by inventory
diff. A weekly deterministic reconciliation SHALL check coverage, duplicate
keys, deletion handling, taxonomy drift, and stale recommendations. Full
semantic reclassification SHALL occur only on explicit request or when a
breaking taxonomy or prompt change requires it. A missing current inventory
MUST skip classification rather than using a stale snapshot. Pending semantic
classification SHALL warn after 30 days and escalate to error after 90 days,
measured from the affected facet's `state_since`. That timestamp SHALL carry
forward only while both state and semantic identity remain unchanged. Every
validated state transition, including classifier `pending` to `suggested`,
SHALL reset it. Content/taxonomy/prompt invalidation SHALL move the facet to
`pending` and reset it; if the facet was already pending, the system SHALL
record a `pending` to `pending` invalidation event and reset the timestamp for
the new semantic input.

#### Scenario: First catalog run begins
- **WHEN** no complete baseline exists
- **THEN** all governed catalog documents MUST be selected in bounded, resumable shards
- **AND** coverage enforcement MUST remain in disclosed baseline mode until deterministic merge completes

#### Scenario: Unchanged incremental run executes
- **WHEN** document locator and hash, effective taxonomy digest, and prompt compatibility are unchanged even though an unrelated repository commit changed the repository revision
- **THEN** the run MUST carry forward compatible entries and select none of them for semantic reclassification

#### Scenario: One document changes
- **WHEN** one content hash differs from the previous inventory
- **THEN** only that entry and any entries invalidated by its references MUST become pending classification

#### Scenario: Taxonomy has a breaking change
- **WHEN** the taxonomy major version changes incompatibly
- **THEN** affected entries MUST become stale and be reclassified without silently mixing taxonomy versions

#### Scenario: Classifier is unavailable
- **WHEN** the semantic cataloger cannot run
- **THEN** the complete mechanical snapshot and deterministic report MUST still land
- **AND** selected entries MUST remain visibly pending

#### Scenario: Pending state crosses an aging boundary
- **WHEN** a facet remains pending across snapshots for 30 or 90 days without an invalidation or disposition transition
- **THEN** its preserved `state_since` MUST produce a warning at 30 days and an error at 90 days

#### Scenario: Pending input changes again
- **WHEN** content or taxonomy changes while a facet is already pending
- **THEN** the catalog MUST record a pending-to-pending invalidation event and reset `state_since` for the new semantic identity

#### Scenario: Classifier resolves pending state
- **WHEN** validated classifier output changes a facet from `pending` to `suggested`
- **THEN** the suggested state MUST receive a new `state_since` and transition evidence

### Requirement: Bounded cataloger execution and protected evidence
Semantic classification SHALL execute as a distinct, bounded, read-only
`document-cataloger` Omnigent job on the existing Cloud PC document-analysis
host, using a dedicated profile, prompt, output schema, and artifact lane. The
worker SHALL receive self-contained bounded shards only after orchestration
evaluates each document's declared handling and source-domain policy against
the target host's attested tenant/data boundary and handling authorizations.
It SHALL receive no repository credentials and no write authority. It SHALL
NOT be a third doc-health semantic finding family and SHALL NOT require another
Entra user or Cloud PC.

The main deterministic run SHALL finish before an asynchronous cataloger child
is dispatched. The hosted preflight SHALL consume the current neutral
infrastructure-readiness result when that contract is promoted and SHALL
require cataloger-specific assertions for an eligible runner, fresh worker
heartbeat, matching profile and version, tenant/data boundary, handling
authorization, and absence of repository credentials. Until that neutral
contract is promoted, the existing semantic-sweep runner/heartbeat preflight
SHALL be the compatibility bridge and MUST NOT be generalized into a competing
readiness-result schema. The watchdog SHALL
report and cancel a child queued longer than ten minutes or running longer than
thirty minutes. Validated recommendation evidence SHALL be immutable at
`health/document-catalog/recommendations/YYYY-MM-DD/<job-id>.yaml` with
`status: record` and SHALL merge only through a later main run.

When the host is not authorized for a document's handling class, orchestration
MUST NOT dispatch its content or identifying metadata and SHALL mark its facets
`policy_blocked` with an opaque blocker reference. Redacted dispatch MAY occur
only when source policy explicitly authorizes the redacted derived view.

Before persistence, an output-policy filter SHALL apply the same handling rules
to paths, topic/domain/capability values, sensitivity signals, and evidence.
It MAY replace a path with an opaque document reference plus path hash and MAY
suppress sensitive facet values. Raw protected passages or revealing metadata
MUST NOT be copied centrally when source-domain policy forbids them.

#### Scenario: Cataloger shard executes
- **WHEN** readiness succeeds, source policy permits the work, and the host attests the required tenant/data boundary and handling authorization
- **THEN** the worker MUST have no repository credentials or source write path
- **AND** it MUST return only its validated recommendation artifact

#### Scenario: Cataloger is offline
- **WHEN** trusted readiness evidence or a required cataloger-specific assertion is absent, stale, or failed
- **THEN** the main run MUST record a skip and leave selected entries pending without waiting for the Cloud PC

#### Scenario: Recommendation arrives asynchronously
- **WHEN** a cataloger child returns after the dispatching report is closed
- **THEN** its immutable evidence MUST be merged by a later main run
- **AND** the closed report and catalog snapshot MUST NOT be edited

#### Scenario: Protected source is classified
- **WHEN** source policy permits classification but prohibits storing a path, passage, or revealing inferred tag centrally
- **THEN** the output-policy filter MUST use an opaque source reference and hashes and suppress the prohibited values

#### Scenario: Host is not authorized for protected content
- **WHEN** the Cloud PC host lacks the required handling authorization or tenant/data-boundary attestation
- **THEN** orchestration MUST NOT dispatch the document or its identifying metadata
- **AND** the catalog MUST record `policy_blocked` with an opaque blocker reference rather than silently treating it as classified

#### Scenario: Redaction is not authorized
- **WHEN** source policy does not explicitly authorize a redacted derived view
- **THEN** orchestration MUST skip dispatch rather than assuming redaction makes processing permissible

### Requirement: Lifecycle and xspec marker exclusion
The document cataloger MUST NOT add, remove, edit, or recommend source
`Status`, `Kind`, or `Repository context` headers; `xspec:candidate` or
`xspec:supersedes` markers; Idea IDs, Claim IDs, routing sidecars, or routing
transitions; promotion or adoption state; access policy; or source-document
content of any kind. Catalog tags SHALL remain distinct from the human/gate
selection expressed by `xspec:` markers.

#### Scenario: Cataloger encounters normative prose
- **WHEN** a document contains prose that might be an `xspec:candidate`
- **THEN** the cataloger MAY classify its topic or capability but MUST NOT add or recommend an `xspec:` marker

#### Scenario: Cataloger output requests a header edit
- **WHEN** classifier output attempts to change lifecycle or repository-context metadata
- **THEN** validation MUST reject the output and leave the source unchanged

#### Scenario: Cataloger attempts routing mutation
- **WHEN** classifier output creates an Idea ID, claim, owner, destination, or routing transition
- **THEN** validation MUST reject the output as outside catalog authority

### Requirement: Catalog-to-routing signal handoff
Current catalog classifications SHALL serve only as optional evidence for a
future or promoted ideation-organizer recommendation. An `unknown` scope,
several domain contexts, or a classification conflict MAY enqueue routing
review only when the catalog
entry's repository, path or authorized opaque resolver, content hash, inventory
snapshot, and effective taxonomy digest match current inputs. Stale, unknown,
policy-blocked, or superseded tags MUST be ignored.

Catalog tags MUST NOT allocate Idea or Claim IDs, create a routing record, set
routing `Scope` or `Routing status`, split a claim, choose or accept an owner or
destination, move content, or create proposal material. If an
`ideation-routing` capability is promoted, authorized routing transitions SHALL
continue through it; otherwise the catalog SHALL only retain the review signal.

#### Scenario: Multi-domain classification is current
- **WHEN** a current catalog entry suggests several domain contexts
- **THEN** the system MAY enqueue an ideation-organizer review
- **AND** it MUST NOT create routing state

#### Scenario: Known-owner document is tagged
- **WHEN** an ordinary domain document has a current known-owner classification
- **THEN** it MUST remain cataloged without being routed merely because it has tags

#### Scenario: Stale classification suggests routing
- **WHEN** a tag's content hash or effective taxonomy digest differs from current inventory/taxonomy inputs
- **THEN** any routing consumer MUST ignore it until a current catalog entry exists

#### Scenario: Routing review is accepted
- **WHEN** an authorized reviewer decides a catalog signal should enter a promoted routing process
- **THEN** that routing process MAY allocate an Idea ID and record the catalog snapshot as evidence

### Requirement: Catalog reporting and immutable history
Each dated doc-health report SHALL link the current immutable per-repository
catalog snapshots and report cataloged versus total documents; counts by
`pending`, `suggested`, `reviewed`, `overridden`, `unclassified`, and
`policy_blocked`; new, changed, deleted, stale, and rejected-output counts;
inventory, taxonomy,
classifier, prompt, and model versions; merged recommendation evidence; skips;
and non-default configuration. Closed reports, snapshots, and recommendation
records MUST remain immutable.

Catalog recommendations SHALL appear in the catalog summary, not the
doc-health Ranked Plan, and MUST NOT directly open critical/error regression
issues. Deterministic coverage, schema, hash, taxonomy, provenance, or override
violations SHALL remain doc-health findings under the `document-catalog`
family.

#### Scenario: Catalog run is reported
- **WHEN** a main sweep completes
- **THEN** its report MUST link the immutable snapshot and state coverage, classification states, versions, changes, and skips

#### Scenario: Semantic recommendation exists
- **WHEN** cataloger output is pending or merged
- **THEN** it MUST be summarized as catalog state rather than emitted as a doc-health finding verdict

#### Scenario: Structural catalog defect exists
- **WHEN** deterministic validation finds missing coverage, stale hashes, invalid taxonomy, or unauthorized override evidence
- **THEN** it MUST emit a `document-catalog` finding under normal severity and regression rules

#### Scenario: Historical record is closed
- **WHEN** a later run changes inventory or classification
- **THEN** it MUST create new snapshots and report references rather than modifying any closed record
