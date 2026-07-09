## ADDED Requirements

### Requirement: Canonical document lifecycle states
Governance documents across `openxFactory` and every DomainxFactory SHALL move
through one canonical lifecycle: `captured`, `organized`, `proposed`,
`ratified`, `implemented`, `promoted`, `adopted`, with `superseded` and
`retired` as terminal transitions and `rejected` or `deferred` as exits from
any pre-promoted state. Every transition SHALL be a deliberate, reviewable
step, never an implicit copy or a silent status edit.

#### Scenario: New governance thinking is recorded
- **WHEN** free-form design thinking, discussion output, or exploratory prose is added to a repository
- **THEN** it MUST enter the lifecycle at `captured` inside that repository's `ideation/brainstorm/` area
- **AND** it MUST NOT be treated as policy by any consumer

#### Scenario: A document changes lifecycle state
- **WHEN** a document moves between lifecycle states
- **THEN** the transition MUST be visible in review history (a commit moving it through an ideation gate, or an OpenSpec change)
- **AND** the document's status header MUST be updated in the same change

#### Scenario: A concept is rejected or deferred
- **WHEN** a captured, organized, or proposed concept is decided against or parked
- **THEN** its status MUST record `rejected` or `deferred` with the reason
- **AND** the artifact MUST be retained (not deleted) while any other document references it

### Requirement: Controlled document status taxonomy
Every governance document SHALL carry a `Status:` header drawn from the
controlled taxonomy: `brainstorm`, `staged`, `draft`, `ratified`, `standard`,
`superseded`, `retired`, `record`. Document genre SHALL NOT be encoded in the
status value; an optional `Kind:` header carries genre.

#### Scenario: A document claims standard authority
- **WHEN** a document's header declares `standard` status or its prose claims to be a shared xFactory standard
- **THEN** a promoted OpenSpec spec or canonical contract MUST back the claim
- **AND** absent such backing the document MUST carry `draft` or lower status

#### Scenario: A generated artifact is stored
- **WHEN** a simulation report, generated runbook, audit output, or other evidence artifact is committed
- **THEN** it MUST carry `record` status
- **AND** it MUST be excluded from prose-to-spec conversion and contradiction checks

#### Scenario: A document is superseded
- **WHEN** a later artifact replaces a document's content
- **THEN** the replaced document MUST move to `superseded` status naming its successor, or be deleted with the successor recording provenance

### Requirement: Ideation work area convention
Each repository that authors governance documents SHALL host its pre-proposal
pipeline in `ideation/brainstorm/` (non-normative capture) and
`ideation/staging/` (organized fragments). Content in `ideation/brainstorm/`
MAY contradict promoted specs; that area is the only place where
contradiction is sanctioned.

#### Scenario: Brainstorm content is organized
- **WHEN** brainstorm material is selected for progression
- **THEN** it MUST be organized into `ideation/staging/` or a candidate register with identified targets and deduplicated claims
- **AND** the brainstorm source MUST be marked `staged` (or note what was extracted) rather than silently duplicated

#### Scenario: Staged content becomes a proposal
- **WHEN** a staged topic is ready for ratification
- **THEN** an OpenSpec change MUST be created carrying the spec deltas
- **AND** the staged material MUST reference that change

#### Scenario: Cross-factory topic is captured
- **WHEN** ideation concerns the neutral layer or multiple DomainxFactories
- **THEN** it MUST be captured in `openxFactory`'s ideation area rather than a single domain repository

### Requirement: Explicit delta rule
Documents SHALL express any change to, contradiction of, or restatement of
promoted policy outside `ideation/brainstorm/` as an explicit change from
current state: an OpenSpec change proposal, or prose carrying an explicit
supersedes marker naming the affected spec requirement. Accidental
restatement of promoted policy in differing words SHALL be treated as a
defect.

#### Scenario: Prose contradicts a promoted spec
- **WHEN** a document outside `ideation/brainstorm/` asserts behavior that conflicts with a promoted spec requirement
- **THEN** the document MUST either carry an explicit supersedes marker naming that requirement and an associated OpenSpec change, or be corrected
- **AND** health tooling MUST report unmarked contradictions as findings

#### Scenario: Prose is tagged for conversion
- **WHEN** an author designates prose as needing conversion to a spec or contract
- **THEN** the designation MUST use an explicit machine-readable tag rather than implication
- **AND** only tagged prose is queued for conversion

### Requirement: Promotion process binding
Domain-to-neutral concept promotion and neutral-to-domain devolution SHALL
follow the documented promotion process, including candidate registration
with evidence, classification and scoring, OpenSpec ratification, and the
adoption steps (consumer re-pin, overlay replacement, local-copy retirement).
Register statuses SHALL be defined in terms of the canonical lifecycle
states.

#### Scenario: A promotion is implemented
- **WHEN** a promoted neutral artifact merges into `openxFactory`
- **THEN** the promotion is not complete until each consuming DomainxFactory re-pins, replaces its local copy with a reference plus thin overlay, and the register entry reaches `adopted`
- **AND** a surviving domain-local near-duplicate MUST be reported as a health finding

#### Scenario: A neutral artifact proves domain-specific
- **WHEN** a neutral artifact is found to encode single-domain authority or vocabulary
- **THEN** a devolution MUST run the same lifecycle in reverse through an OpenSpec change, with the owning DomainxFactory adopting the content
