# subject-establishment Specification

## Purpose

Define the one neutral pipeline every DomainxFactory instantiates for the
start-of-life motion of a newly admitted subject, and the two artifact kinds
that motion carries: the neutral subject design, which says what the
subject's setup means in domain terms, and the platform realization, which
maps that design into one named external system of record. Keep the split
load-bearing, because it is what buys portability across a change of system
of record, a review in which the domain's expert weighs judgment rather than
vendor trivia, and second-platform support as a second mapping instead of a
second design. Bound the motion around it so the split survives contact with
a real subject: facts carry provenance grades, versioned archetypes
accelerate and measure but never override an approved design, a deviating
design parks at the domain's named expert authority through the ratified
escalation ladder, a realization crossing to a different applying factory
rides the ratified deployment handoff rather than a new record kind,
establishing and migrating are distinct authority classes that never share a
grant, and no apply is conformant until it is read back from the system it
changed. Fix ownership of these artifacts on the canonical Subject / Tenant
/ Domain layering while leaving their storage to the realizing repository.
## Requirements
### Requirement: Subject establishment is one neutral pipeline over two artifact kinds
Every DomainxFactory's start-of-life motion for a newly admitted subject SHALL
be expressible as one ordered neutral pipeline — assemble the subject fact set,
author the neutral subject design, select the system of record, author the
platform realization, review under conformance tiering, apply, and verify by
read-back — and a domain SHALL instantiate that pipeline rather than re-derive
it. The pipeline SHALL carry exactly two artifact kinds: the NEUTRAL SUBJECT
DESIGN (what this subject should be, in domain terms) and the PLATFORM
REALIZATION (how that design maps into one named external system). A domain's
nouns, its design content, and its supported platforms are domain-local; the
ordering, the two artifact kinds, and the obligations stated in the
requirements below are not.

#### Scenario: A domain instantiates the pipeline for its own subject kind
- **WHEN** a DomainxFactory establishes a new subject — a client company, a patient, an engineering project, a managed estate, a campaign subject
- **THEN** its motion resolves onto this pipeline's steps in this order, with domain nouns substituted for the neutral ones
- **AND** the domain contributes design content and platform mappings, never a second ordering

#### Scenario: A domain proposes a step the pipeline does not have
- **WHEN** a domain's establishment motion needs a step outside the ordered pipeline
- **THEN** the step is a candidate amendment to this capability rather than a domain-local extension, because a divergent ordering makes the design/realization split unportable

#### Scenario: The two artifact kinds are collapsed into one
- **WHEN** a domain records the subject's intended setup and the platform objects that realize it as a single artifact
- **THEN** it does not conform, because the split is what carries portability, reviewability and second-platform support, and a collapsed artifact silently loses all three

### Requirement: Every fact in the subject fact set carries a provenance grade
The subject fact set SHALL record, for every fact, the source it came from and
a PROVENANCE GRADE distinguishing at least authoritative-registry facts,
subject self-report, and factory observation. A fact recorded without a grade
SHALL NOT be treated as established. Grades SHALL be re-evaluable: a fact whose
grade improves or degrades on re-verification SHALL carry the new grade with
the superseded one legible. This obligation is the neutral case of
`governed-derived-model`'s full-provenance requirement — every fact tagged with
an evidence trace or a declared assumption — applied to the establishment fact
set, and domains that already declare the assumptions-forbidden form SHALL
satisfy it by that form rather than by a second register.

#### Scenario: A registry fact and a wizard-typed fact sit side by side
- **WHEN** one fact arrives from an authoritative external registry and another is typed into an intake form by the subject
- **THEN** both are recorded, and each carries a grade that says which it is
- **AND** no consumer may read them as the same evidence

#### Scenario: A design element depends on an ungraded fact
- **WHEN** a neutral subject design element cites a fact carrying no provenance grade
- **THEN** the design is not review-ready, because the reviewer cannot weigh a judgment whose inputs have unknown standing

#### Scenario: A self-reported fact is later confirmed by a registry
- **WHEN** re-verification raises a fact from self-report to authoritative-registry
- **THEN** the fact carries the new grade and the superseded grade remains legible, so a design approved under the weaker evidence can be found

### Requirement: The neutral subject design names semantic roles and no vendor object
The neutral subject design SHALL express every element as a SEMANTIC ROLE in
domain terms and SHALL NOT name any external product, its objects, its
identifiers, or its field names. The design SHALL be authoritative for what the
subject's setup means; it SHALL survive a change of system of record unchanged
except where the domain's judgment itself changed. Vendor material belongs to
the platform realization, and a design carrying it has pre-committed to one
platform.

#### Scenario: A design element names a platform object
- **WHEN** a design element is expressed as a general-ledger account number, a repository ruleset identifier, a chart-section code, or any other system-specific object
- **THEN** the design does not conform, and the element belongs in the platform realization under the semantic role it was standing in for

#### Scenario: The system of record changes
- **WHEN** a subject migrates from one external system to another
- **THEN** the neutral subject design is unchanged and a second platform realization is authored against it

#### Scenario: A reviewer reads the design
- **WHEN** the domain's expert authority reviews an established subject's design
- **THEN** every element under review is domain judgment, because no vendor trivia is present to review

### Requirement: The platform realization is a separate artifact, one per system of record
A platform realization SHALL be a separate artifact from the design it
realizes, SHALL name exactly ONE system of record, and SHALL map every element
of that design to concrete objects in that system. Every realization element
SHALL trace to the design element it realizes, and every design element SHALL
be either mapped or explicitly recorded as unrealizable in that system with a
reason. A second supported platform SHALL be a second realization of the same
design, never a second design. The realization SHALL be authored by the
authority competent in that platform, which may not be the authority that
authored the design.

#### Scenario: A second platform is supported
- **WHEN** a domain adds support for a second external system for the same subject kind
- **THEN** it authors a second realization against the existing design and the design is untouched

#### Scenario: A design element has no object in the target system
- **WHEN** the target platform cannot express a design element
- **THEN** the realization records it as unrealizable with a reason rather than dropping it, so the gap is reviewable and does not read as conformance

#### Scenario: A realization element traces to nothing
- **WHEN** a realization names a platform object that no design element asked for
- **THEN** it is realization drift and is a finding, because an object nobody designed is an object nobody reviewed

#### Scenario: One realization names two systems of record
- **WHEN** a single realization artifact maps design elements into more than one external system
- **THEN** it does not conform, because the per-platform overlay is what makes the mapping reviewable by that platform's specialist and replaceable at migration

### Requirement: The reference archetype accelerates and measures but never overrides
A domain SHALL keep VERSIONED reference archetypes — archetype-level neutral
designs that per-subject research starts from and that serve as the conformance
yardstick. The per-subject design SHALL remain authoritative: an archetype
SHALL NOT override, silently amend, or retroactively invalidate an already
approved subject design. Resolutions of subject-level deviations SHALL be
harvestable back into the archetype, and a harvest SHALL produce a new
archetype VERSION rather than mutate the version existing subjects were
measured against.

#### Scenario: Research starts from an archetype
- **WHEN** a domain begins establishing a subject matching a known archetype
- **THEN** the archetype's design is the starting point and the per-subject research amends it

#### Scenario: A deviation resolution is harvested
- **WHEN** an expert resolves a subject-level deviation in a way the domain wants as standard
- **THEN** the resolution produces a NEW archetype version, and the auto-approving share of future subjects grows

#### Scenario: An archetype version is superseded
- **WHEN** a new archetype version lands
- **THEN** subjects established against the prior version remain conformant to the version they were measured against, and any re-alignment is proposed as its own act rather than appearing as a new non-conformance

### Requirement: Conformance tiering routes review through the ratified escalation ladder
Review of a neutral subject design SHALL be tiered on its conformance to the
governing archetype version, and the tiering SHALL be the ratified
`roles-authority-model` escalation ladder applied rather than a second
mechanism: an archetype-conforming design is ROUTED and decided within the
declared agent authority under the domain's standing envelope; a DEVIATING
design PARKS with a decision-ready packet at the gate the domain's named expert
authority already owns, and SHALL NOT interrupt on deviation alone. The
deviating element and its rationale SHALL be the packet's subject. Which seat
holds that expert authority is domain-local; that a deviating design reaches
one before it may be applied is not.

#### Scenario: A conforming design is reviewed
- **WHEN** a subject design matches its archetype version within the domain's declared envelope
- **THEN** it is routed and approved within agent authority, and no human is notified outside their normal gate visits

#### Scenario: A deviating design is reviewed
- **WHEN** a subject design departs from its archetype version
- **THEN** it parks with a decision-ready packet naming the deviating element and its rationale at the domain's expert-authority gate

#### Scenario: A deviating design is applied without its ruling
- **WHEN** an apply is attempted for a design whose deviation is still parked
- **THEN** it is refused, because the tiering exists to put domain judgment in front of a human before external state moves

#### Scenario: A domain declares no expert seat
- **WHEN** a domain instantiates this capability without naming the authority a deviating design parks at
- **THEN** it does not conform, because an unnamed gate is an unreachable one and every design would route

### Requirement: A realization crossing to a different applying factory rides the ratified handoff
A platform realization SHALL reach its applier as a governed handoff under the
ratified `deployment-handoff-boundary`, and SHALL NOT invent a second crossing
mechanism, wherever the factory that AUTHORED the design is not the factory
that ADMINISTERS the target system of record. Which factory applies is decided by that
capability's managed-subject test; the crossing takes the shape its "handoff
crosses as a client infrastructure request" requirement fixes — a
`client_infrastructure_request` or a requirements-profile of it, with no new
record kind — carrying the realization as the requested intent. The design, the
handoff and the applied result SHALL share one correlation identifier, on the
same correlation the boundary's out-of-band-detectability requirement already
stamps. Where the designing and administering factory are the same, no handoff
exists and the apply is self-served.

#### Scenario: The designer and the applier are different factories
- **WHEN** a domain designs a subject whose system of record is administered by another factory
- **THEN** the realization crosses as a `client_infrastructure_request` under an approved execution binding and the designing factory holds no credential path to apply it directly

#### Scenario: The designer administers its own system of record
- **WHEN** the designing factory is also the administrator of the target system
- **THEN** no handoff record exists and the apply is self-served, exactly as the managed-subject test decides

#### Scenario: An applied change is audited back to its design
- **WHEN** the evidence-correlation audit joins observed changes on the target system against accepted requests
- **THEN** the applied change, the handoff request and the subject design resolve through one correlation identifier

#### Scenario: A second crossing mechanism is proposed
- **WHEN** a domain proposes a bespoke design-handoff record for this purpose
- **THEN** it does not conform, because the ratified boundary already states that a crossing does not get its own record kind

### Requirement: An apply is not conformant until it is verified by read-back
An apply against an external system of record SHALL be verified by READING THE
RESULTING STATE back from that system and diffing it against the platform
realization that was applied; an unverified apply SHALL NOT be recorded as
conformant, successful, or green. The read-back SHALL exercise the same
authorization path a real change traverses: a probe that a platform answers
before it authorizes proves nothing about what the platform will do, and SHALL
NOT be accepted as verification. A diff SHALL be resolved — by re-apply, by
amending the realization, or by recording the platform's behaviour as a mapping
defect — before the subject is established.

#### Scenario: The read-back matches the realization
- **WHEN** the applied state is read back and diffs clean against the realization
- **THEN** the apply is conformant and the subject reaches established

#### Scenario: The platform silently did something else
- **WHEN** the read-back diff shows the system holds state the realization did not ask for, or lacks state it did
- **THEN** the apply is not conformant and the diff is resolved before the subject is established

#### Scenario: Verification is attempted with a pre-authorization probe
- **WHEN** the only evidence of success is a platform response produced before the authorization layer was reached
- **THEN** it is not verification, because the platform may validate before it authorizes and the probe never reached the layer that decides

#### Scenario: No read-back is performed
- **WHEN** an apply completes with no read-back recorded
- **THEN** the subject is not established, regardless of the applier reporting success

### Requirement: Establishing and migrating are different authority classes and never share a grant
Two authority classes SHALL be distinct and SHALL NOT be reachable through the
same grant: ESTABLISHING a new subject in an empty environment, and MIGRATING
an established subject that already carries history.
The establishment class MAY carry a lighter
approval because a wrong result is discarded by re-provisioning and no existing
state is damaged. The migration class SHALL be proposal, then approval, then
apply, then read-back verification, in that order, in every domain. A grant
issued for the establishment class SHALL be refused against a subject that
already holds state.

#### Scenario: A new subject is established in an empty environment
- **WHEN** the target holds no prior subject state
- **THEN** the establishment class applies and its lighter approval is legitimate, because the remedy for a wrong result is to discard and re-provision

#### Scenario: An establishment grant reaches an established subject
- **WHEN** an establishment-class grant is presented against a subject that already carries history
- **THEN** it is refused, and the act is a migration requiring the migration class

#### Scenario: A migration is applied without approval
- **WHEN** a change to an established subject's configuration is applied with no approved proposal
- **THEN** it is a boundary violation, not a fast path

### Requirement: The audit mirror lifts existing configuration into the neutral design
Reading an already-configured subject SHALL be expressible as the inverse of
realization: read the external system's actual state, LIFT it into the neutral
subject design vocabulary using the same mapping the platform realization
declares, diff the lifted design against the design the domain's research would
produce today, and propose the difference as a migration. The proposed
migration SHALL be a migration-class act under the authority-class requirement
above. Where the lift and the realization mapping disagree about the same
object, the disagreement SHALL be a defect in the mapping rather than a
judgment call at lift time, because one mapping read in two directions is what
makes the mirror trustworthy.

#### Scenario: An existing subject is audited
- **WHEN** a domain audits a subject it did not establish
- **THEN** the system's state is lifted into a neutral design, diffed against the design research would produce, and the difference is proposed as a migration

#### Scenario: The lift and the realization disagree
- **WHEN** lifting an object produces a different semantic role than the realization mapping assigns to it
- **THEN** the mapping is defective and is corrected, rather than the lift choosing a role

#### Scenario: An audit's proposed migration is applied
- **WHEN** an audit-proposed migration is approved and applied
- **THEN** it travels the migration authority class and is verified by read-back like any other apply

### Requirement: Layer ownership of establishment artifacts is fixed, their storage is not
The canonical Subject / Tenant / Domain layering SHALL own the establishment
artifacts as follows: the SUBJECT layer holds the subject fact set and that
subject's design; the TENANT layer holds the reference-archetype library, the
domain standard, and the system-of-record selection for that subject; the
DOMAIN layer holds the correctness criteria and commissions the research. The
applied realization's identity SHALL be reachable from the act that applied it.
Which STORE any layer uses SHALL remain a realizing repository's choice; this
capability fixes ownership, not persistence.

#### Scenario: A domain instantiates the layering
- **WHEN** a DomainxFactory instantiates this capability
- **THEN** its fact set and subject designs sit at the subject layer, its archetypes and standard at the tenant layer, and its correctness criteria at the domain layer

#### Scenario: A tenant decides the system of record
- **WHEN** the external system a subject will live in is selected
- **THEN** the decision is the tenant layer's, because the same domain serves subjects across estates and instances

#### Scenario: A realizing repository picks a store
- **WHEN** a realizing repository holds subject designs in a memory store, a governed configuration tree, or a domain database
- **THEN** it conforms, provided the layer ownership above is unchanged

