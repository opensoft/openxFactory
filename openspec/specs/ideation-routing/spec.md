# ideation-routing Specification

## Purpose

Establish capture-first, route-later ideation across the factory family: an
idea is captured where it lands — the owning DomainxFactory's brainstorm area,
openxFactory's when it is already neutral or cross-domain, and openxFactory's
unclassified inbox as an independently routable item when the owner is
genuinely unknown — while the xFactory aggregation repository hosts no
ideation backlog at all. Give every unclassified, mixed, cross-domain or
claim-split idea exactly one canonical routing record in openxFactory:
centrally allocated `XFI-` Idea IDs and per-claim Claim IDs, controlled scope
and routing-status vocabularies with append-only transitions, and structured
repository, path and revision references that resolve through the
aggregation's `.gitmodules` gitlinks. Route claim by claim so reusable
neutral contracts, domain policy, installer and runtime implementation, and
release assembly keep distinct owners and provenance, and let a record reach
`routed` only when every claim carries its accepted owner, destination and
acceptance evidence. Routing coordinates without transferring authority: the
non-mutating ideation organizer and the document-catalog signals it may
consume are recommendations pending an authorized human disposition, domain
origin material stays domain-authoritative, and adoption still runs the
lifecycle's own promotion gates.
## Requirements
### Requirement: Capture-first repository routing
Factory-family ideation SHALL permit capture before final ownership is known.
A known-domain idea SHALL enter that DomainxFactory's
`ideation/brainstorm/`; a clearly neutral or already cross-domain idea SHALL
enter `openxFactory/ideation/brainstorm/`; and a genuinely unknown-owner idea
SHALL enter its own
`openxFactory/ideation/brainstorm/inbox/<idea-id>/` directory. The xFactory
aggregation repository MUST NOT host a general ideation backlog, and a
monolithic tagged inbox MUST NOT substitute for independently routable items.

#### Scenario: Unknown-owner idea is captured
- **WHEN** an author cannot yet identify the owning repository
- **THEN** the idea MUST be captured as an independent item in the openxFactory unclassified inbox
- **AND** capture MUST NOT require a guessed owner

#### Scenario: Known-domain idea is captured
- **WHEN** the idea is already known to be domain-owned
- **THEN** it MUST remain in that DomainxFactory's brainstorm area rather than being centralized

#### Scenario: Clearly neutral idea is captured
- **WHEN** an idea is already known to define reusable neutral behavior or spans domains at capture
- **THEN** it MUST enter openxFactory's brainstorm area

#### Scenario: Aggregation backlog is created
- **WHEN** general ideation or an unclassified inbox is placed in the xFactory aggregation repository
- **THEN** routing validation MUST reject that placement

### Requirement: Canonical routing identity and record
Every unclassified, mixed, cross-domain, or claim-split idea SHALL have exactly
one canonical routing record in
openxFactory. Idea IDs SHALL use `XFI-<year>-<three-digit-sequence>` and be
allocated from the central openxFactory
`ideation/routing-index.yaml` in the same reviewed change that creates the
routing record. Claim IDs SHALL use
`<idea-id>-C<two-digit-sequence>`. The record SHALL declare its Idea ID,
controlled scope and routing status, all sources, domains and candidate owners,
claims, transition history, successors, and any deduplication rationale.

Allowed scopes SHALL be `unclassified`, `domain`, `cross_domain`,
`neutral_candidate`, and `mixed`. Allowed routing statuses SHALL be `intake`,
`triaging`, `split`, `routed`, `deferred`, and `rejected`. Routing metadata
MUST NOT replace the canonical document `Status:` taxonomy. Ordinary documents
and known-owner brainstorms not entered into routing SHALL remain valid without
a routing sidecar.

#### Scenario: Routing begins
- **WHEN** an idea becomes unclassified, mixed, cross-domain, or claim-split
- **THEN** one central Idea ID and exactly one canonical routing record MUST be created
- **AND** the human-readable source and routing record MUST agree on the Idea ID

#### Scenario: Concurrent allocation collides
- **WHEN** two proposed changes allocate the same Idea ID
- **THEN** validation MUST reject the duplicate and the later change MUST rebase and allocate a new sequence

#### Scenario: Several sources are deduplicated
- **WHEN** several source documents contribute to one canonical idea
- **THEN** the record MUST list every source and the deduplication rationale

#### Scenario: Ordinary document has no routing metadata
- **WHEN** a document has not entered unclassified, mixed, cross-domain, or claim-split routing
- **THEN** it MUST remain valid without an Idea ID or routing sidecar

### Requirement: Routing and claim transition integrity
Routing transitions SHALL be append-only and limited to: `null` to `intake`;
`intake` to `triaging`, `deferred`, or `rejected`; `triaging` to `split`,
`routed`, `deferred`, or `rejected`; `split` to `triaging`, `routed`,
`deferred`, or `rejected`; and `routed`, `deferred`, or `rejected` to
`triaging` as a reviewed reopen.

Claim disposition SHALL be one of `unresolved`, `proposed`, `routed`,
`deferred`, or `rejected`. Normal progression SHALL be `unresolved` to
`proposed` to `routed`; `unresolved` or `proposed` MAY exit to `deferred` or
`rejected`; and a terminal claim MAY return to `unresolved` only through a
reviewed reopen. An unresolved claim SHALL name a blocker or blocking question.
A routed claim SHALL name its accepted owner, target capability, structured
destination, acceptance actor, acceptance time, and acceptance evidence. A
record SHALL reach `routed` only when no active claim remains `unresolved` or
`proposed`.

#### Scenario: Destination accepts a claim
- **WHEN** the destination authority accepts a proposed claim and its complete destination
- **THEN** the claim MAY transition to `routed` with acceptance evidence

#### Scenario: Proposed owner has not accepted
- **WHEN** a claim names a proposed owner but has no destination-owner acceptance
- **THEN** the claim MUST NOT be marked `routed`

#### Scenario: Ownership remains disputed
- **WHEN** no authorized owner accepts a claim
- **THEN** the claim MUST remain `unresolved` with an explicit blocker or blocking question

#### Scenario: Routing record closes prematurely
- **WHEN** any active claim remains `unresolved` or `proposed`
- **THEN** the routing record MUST NOT transition to `routed`

#### Scenario: Terminal claim is reconsidered
- **WHEN** a routed, deferred, or rejected claim needs reconsideration
- **THEN** a reviewed transition MUST reopen it as `unresolved` before another disposition is chosen

### Requirement: Claim-level classification and ownership boundaries
Each independently routable claim SHALL record its summary, stable source
evidence, proposed and accepted owners, target capability, structured
destination, dependencies, domain-local exclusions, disposition, and
rationale. Classification SHALL assign reusable lifecycle, schema, authority,
template, and workflow claims to openxFactory; professional, regulatory,
domain-evidence, terminology, threshold, and approval claims to the owning
DomainxFactory; domain specializations to thin domain overlays; privileged IT
execution to OpsxFactory; software-engineering execution to codexFactory;
installer or host/runtime behavior to its implementation repository; and only
composition, pinning, or release assembly to xFactory. Tags, candidate owners,
and organizer confidence MUST NOT confer ownership or authority.

#### Scenario: Mixed idea is split
- **WHEN** one idea contains neutral, domain, installer, and aggregation concerns
- **THEN** each independently routable claim MUST receive its own Claim ID and appropriate destination class

#### Scenario: Neutral skeleton has a domain overlay
- **WHEN** a reusable hook and domain-specific meaning coexist
- **THEN** the reusable skeleton MUST route to openxFactory and the specialization MUST route to a thin DomainxFactory overlay

#### Scenario: Runtime behavior is classified
- **WHEN** a claim changes installer, host, or runtime implementation
- **THEN** it MUST route to the implementation repository rather than becoming neutral policy

#### Scenario: Domain tag conflicts with ownership
- **WHEN** a domain tag names a repository that does not own the claim shape
- **THEN** the tag MUST NOT override classification or acceptance authority

### Requirement: Structured repository references and resolvable provenance
Every source, routing-record, and destination reference SHALL be a structured
object containing a canonical repository ID, a POSIX repository-relative path,
and a full commit revision. Repository IDs SHALL resolve through the xFactory
aggregation repository: reserved ID `xFactory` denotes its root and every other
ID SHALL equal an aggregation-relative `.gitmodules` path and resolve through
that path's gitlink. Absolute paths, path traversal, unknown repositories, and
revisions that do not belong to the named repository SHALL be invalid.
`pending_capture` MAY appear only on a source while its record is in `intake`;
every organize or proposal transition SHALL use committed, resolvable
revisions.

The governed document corpus SHALL remain openxFactory plus DomainxFactories.
References to xFactory or pinned install/runtime repositories SHALL be resolved
without treating those entire repositories as governance corpora. Nightly
validation MAY report an unavailable external path check as skipped, but
strict organize and proposal validation SHALL materialize each referenced
pinned repository and resolve its path and revision.

#### Scenario: Cross-repository source is pinned
- **WHEN** a domain-origin claim crosses the organize gate
- **THEN** its source repository, path, and full committed revision MUST resolve

#### Scenario: Intake has not yet been committed
- **WHEN** a newly captured intake record uses `pending_capture`
- **THEN** capture MAY proceed
- **AND** the record MUST acquire a committed revision before leaving `intake`

#### Scenario: External runtime target is referenced
- **WHEN** a claim targets a pinned install or runtime repository
- **THEN** strict gate validation MUST resolve the repository gitlink, revision, and path without adding that repository to the governance corpus

#### Scenario: Reference escapes a repository
- **WHEN** a reference uses an absolute path or path traversal
- **THEN** validation MUST reject it

### Requirement: Organize gate and lightweight destination provenance
At the organize gate, routing SHALL deduplicate claims, assign Claim IDs,
classify ownership and targets, create or update destination staging artifacts,
record lightweight provenance in every destination, record extraction targets
in each source, and retain unresolved claims in the canonical routing record.
Source brainstorms SHALL use one `Idea ID:` header. A destination derived from
one or more ideas SHALL use `Source Idea IDs:`, `Claim IDs:`, and `Routing
records:` pointers. The full routing YAML MUST NOT be copied into destination
documents, and cited source brainstorms MUST be retained while referenced. The
`Routing records:` header SHALL encode a canonical compact JSON array of the
same structured repository/path/revision objects this capability defines; it
MUST NOT introduce a separate string-reference grammar.

#### Scenario: Claims progress independently
- **WHEN** only some claims are ready for staging
- **THEN** those claims MAY enter their destination staging areas while unresolved claims remain in the routing record

#### Scenario: Destination consolidates ideas
- **WHEN** a destination intentionally combines claims from several ideas
- **THEN** it MUST list every Source Idea ID, Claim ID, and routing-record pointer
- **AND** it MUST NOT declare a misleading singular `Idea ID:`

#### Scenario: Destination serializes a routing pointer
- **WHEN** a Markdown destination uses the `Routing records:` header
- **THEN** its value MUST parse as the canonical compact JSON array of structured repository, path, and full-revision references

#### Scenario: Destination copies a routing record
- **WHEN** a destination contains a full routing-record schema rather than lightweight pointers
- **THEN** deterministic validation MUST report a drift defect

#### Scenario: Source is cited after extraction
- **WHEN** a routed destination cites a source brainstorm
- **THEN** the source MUST be retained and updated with its extraction destinations

### Requirement: Routing coordinates but does not transfer authority
Routing SHALL coordinate proposed ownership without replacing content
authority. Domain-origin material SHALL remain authoritative for domain-local
meaning until the existing `document-lifecycle` promotion and adoption gates
complete. The routing record, organizer recommendations, domain tags, and
candidate-owner fields MUST NOT replace the domain-neutral candidate register,
OpenSpec ratification, destination-owner acceptance, or Domain Hermes review.

#### Scenario: Domain-origin idea expands
- **WHEN** a domain brainstorm later yields neutral and other-domain claims
- **THEN** the original domain source MUST remain in place
- **AND** openxFactory MUST host the cross-domain routing hub without acquiring the source's domain authority

#### Scenario: Neutral candidate is routed
- **WHEN** a claim is accepted for neutral proposal work
- **THEN** it MUST still complete OpenSpec ratification, promotion, consumer re-pin, and overlay replacement before adoption

#### Scenario: Organizer recommends an owner
- **WHEN** the semantic organizer recommends a destination
- **THEN** the recommendation MUST remain pending until an authorized destination accepts it

### Requirement: Non-mutating semantic ideation organizer
The ideation-routing capability SHALL provide a semantic organizer that reviews
new or materially changed `unclassified` or `mixed` ideas, manual requests,
new cross-domain links, aged routing items, and pre-organize or pre-proposal
gates. It MAY recommend scope, owners, claim splits, neutral skeletons, domain
exclusions, dependencies, related ideas, destinations, and blocking questions.
Each recommendation SHALL identify the committed source revision, passage hash
and section reference, rationale, numeric confidence from 0 through 1,
alternatives, exclusions, ambiguity, and `pending_review` disposition.

The organizer MUST NOT move, delete, supersede, promote, or approve content;
assign repository or approval authority; resolve disputed claims; create
normative staging content without review; copy protected domain content into a
neutral record; treat inference as domain truth; or mutate the canonical
routing record. Organizer recommendations are proposals, not doc-health
findings or verdicts.

#### Scenario: Changed mixed idea is selected
- **WHEN** a materially changed mixed brainstorm meets organizer selection rules
- **THEN** it MUST be eligible for a bounded semantic review

#### Scenario: Organizer emits recommendations
- **WHEN** organizer analysis succeeds
- **THEN** every recommendation MUST carry stable evidence, rationale, confidence, alternatives, ambiguity, and pending disposition

#### Scenario: Organizer attempts a mutation
- **WHEN** organizer output requests or performs a lifecycle or repository mutation
- **THEN** the output MUST be rejected and the source MUST remain unchanged

#### Scenario: Recommendation is reviewed
- **WHEN** an authorized owner accepts, edits, or rejects a recommendation
- **THEN** lifecycle tooling MAY update the canonical routing record with the decision and evidence reference

### Requirement: Document catalog signals are routing recommendations only
The ideation organizer SHALL treat current document-catalog classifications as
optional selection and evidence inputs and enforce the currentness and
non-authority rules owned by `document-cataloging` by reference. A catalog
signal MUST match the current repository, path or authorized opaque resolver,
content hash, inventory snapshot, and effective taxonomy digest before use.
Policy-blocked signals MUST NOT be used. No catalog state, topic, domain
context, capability reference, confidence, or review status SHALL count as
routing ownership, destination acceptance, or lifecycle authority.

#### Scenario: Current mixed-context tag is observed
- **WHEN** a current catalog entry suggests unknown or several domain contexts
- **THEN** the organizer MAY recommend opening routing review
- **AND** it MUST NOT allocate an Idea ID or create a routing record

#### Scenario: Catalog entry is stale
- **WHEN** a catalog entry does not match the current inventory hash or effective taxonomy digest
- **THEN** the organizer MUST ignore its tags as routing evidence

#### Scenario: Catalog override names a domain
- **WHEN** an authorized catalog override classifies a document with a domain context
- **THEN** that classification MUST NOT substitute for destination-owner acceptance under this capability

#### Scenario: Human authorizes routing from a catalog signal
- **WHEN** an authorized reviewer accepts a routing recommendation supported by catalog evidence
- **THEN** the normal central ID allocation and routing-record workflow MAY begin with the snapshot cited as evidence

### Requirement: Organizer execution, persistence, and readiness isolation
openxFactory SHALL own the organizer contract and schemas, and SHALL also own
selection, orchestration adapters, validation, and report integration;
xFactory SHALL host dispatch and durable reporting; a dedicated
`ideation-organizer` Omnigent worker profile SHALL perform bounded read-only
analysis on the existing document-analysis host; and owning Domain Hermes,
neutral authority, or an authorized human SHALL dispose recommendations.

The deterministic run SHALL complete without waiting for organizer execution.
A hosted preflight SHALL consume the current neutral infrastructure-readiness
result when that contract is promoted and SHALL require organizer-specific
assertions for an eligible runner, fresh worker heartbeat, matching profile and
version, tenant/data boundary, handling authorization, and absence of
repository credentials. Until that neutral contract is promoted, the existing
semantic-sweep runner/heartbeat preflight SHALL be the compatibility bridge and
MUST NOT be generalized into a competing readiness-result schema. Before
dispatch, orchestration SHALL evaluate each source's declared handling and
source-domain policy against the host's attested tenant/data boundary and
organizer handling authorizations.
Missing readiness or authorization SHALL record a fail-closed skip without
sending source content or identifying metadata. Redacted dispatch MAY occur
only when source policy explicitly permits the derived view. A watchdog SHALL
report and cancel a child queued longer than ten minutes or running longer than
thirty minutes without blocking deterministic results; non-default readiness
or watchdog thresholds SHALL be reported.
Validated organizer output SHALL be committed by orchestration as immutable
evidence at
`health/ideation-organizer/YYYY-MM-DD/<idea-id>-<run-id>.yaml` with
`status: record`, and the dated
health report finalized after that evidence lands SHALL link its summary;
already finalized `Status: record` reports MUST NOT be edited. Accepted,
modified, and rejected decisions SHALL remain preserved through evidence
references in the routing record. Before persistence, an output-policy filter
SHALL apply source handling rules to paths, proposed tags/owners/destinations,
summaries, and evidence. Prohibited values SHALL be suppressed or replaced by
opaque references and hashes; raw protected source passages or revealing
metadata MUST NOT be copied into aggregation evidence.

#### Scenario: Worker is ready
- **WHEN** the hosted preflight observes current trusted readiness evidence plus the required organizer profile, tenant/data-boundary, handling, and no-repository-credential assertions
- **THEN** it MAY asynchronously dispatch the organizer child workflow
- **AND** deterministic report finalization MUST remain independent

#### Scenario: Worker is unavailable
- **WHEN** trusted readiness evidence or a required organizer-specific assertion is absent, stale, or failed
- **THEN** the organizer MUST be recorded as skipped without suppressing deterministic findings
- **AND** source content and identifying metadata MUST NOT be dispatched

#### Scenario: Organizer evidence is produced
- **WHEN** validated organizer output returns
- **THEN** orchestration MUST persist an immutable evidence record declaring `status: record` and link it from reporting
- **AND** a temporary workflow artifact alone MUST NOT satisfy persistence

#### Scenario: Organizer evidence lands after report finalization
- **WHEN** a child organizer run finishes after the dispatching dated report is closed
- **THEN** the evidence MUST remain in its immutable organizer path and be summarized by the next report
- **AND** the closed report MUST NOT be edited

#### Scenario: Organizer child becomes stale
- **WHEN** a child remains queued beyond ten minutes or running beyond thirty minutes
- **THEN** the watchdog MUST report and cancel it without blocking deterministic reporting

#### Scenario: Domain evidence is protected
- **WHEN** source-domain policy permits organizer analysis but prohibits persisting a passage, path, proposed tag, owner, destination, or summary centrally
- **THEN** output filtering MUST suppress the prohibited value or retain only an authorized opaque reference and hash

#### Scenario: Organizer host is unauthorized
- **WHEN** the Cloud PC host is not attested for the source tenant/data boundary or handling class
- **THEN** orchestration MUST fail closed and MUST NOT dispatch the source or its identifying metadata

#### Scenario: Organizer redaction is not authorized
- **WHEN** source policy does not explicitly permit a redacted derived view
- **THEN** orchestration MUST skip the source rather than assuming redaction makes dispatch permissible

### Requirement: Prospective compatibility and migration
Existing brainstorms SHALL remain valid without fabricated historical Idea IDs,
claims, or transitions. Routing metadata SHALL become required only when an
existing item is materially changed into an unclassified, mixed,
cross-domain, or claim-split state, or when an authorized migration records
current evidence. Future DomainxFactories SHALL receive the capture and routing
convention from the shared domain starter.

#### Scenario: Legacy brainstorm is unchanged
- **WHEN** an existing brainstorm has not been materially changed or entered into routing
- **THEN** it MUST remain valid without retroactive routing metadata

#### Scenario: Legacy brainstorm enters routing
- **WHEN** an existing brainstorm is deliberately routed
- **THEN** the new record MUST cite the current committed source revision
- **AND** it MUST NOT fabricate earlier transitions

#### Scenario: A new DomainxFactory is scaffolded
- **WHEN** the shared domain starter creates a new factory
- **THEN** its ideation guide MUST include the promoted capture and routing convention

