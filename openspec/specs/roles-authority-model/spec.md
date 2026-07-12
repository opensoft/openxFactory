# roles-authority-model Specification

## Purpose

Define neutral ownership of the cross-factory authority model and the
requirement that each DomainxFactory instantiate its execution lead roles
as a declared specialization.
## Requirements
### Requirement: Neutral authority model ownership
`openxFactory` SHALL own the cross-factory authority model: the authority
layers, Hermes-level governance roles (project ownership, sequencing,
system and project architecture, merge readiness and merge authority),
escalation principles, and external enforcement concepts — expressed
without any single domain's execution roles, group names, or tooling.

#### Scenario: The neutral roles doc is revised
- **WHEN** `docs/roles-and-authority.md` changes
- **THEN** it MUST NOT define domain execution lead roles, domain-specific escalation routes, or deployment group names — those belong to the owning DomainxFactory

### Requirement: Domain execution role instantiation
Each DomainxFactory SHALL instantiate its execution lead roles — the
domain-side counterparts that decompose, implement, verify, integrate, and
secure approved work — in its own documentation, declared as a
specialization of the neutral model.

#### Scenario: Engineering roles are defined
- **WHEN** software engineering execution roles are defined or revised
- **THEN** the canonical text lives in `codexFactory/docs/engineering-roles-and-authority.md`
- **AND** codexFactory's stack.yaml declares `specializes` for the roles model

#### Scenario: Another domain instantiates roles
- **WHEN** a non-engineering DomainxFactory defines its execution roles
- **THEN** it follows the same pattern in its own repository and MUST NOT edit the neutral model to add its roles

### Requirement: Human-attention escalation ladder
The neutral authority model SHALL define a three-rung escalation ladder — route, park, interrupt — and every situation requiring a decision MUST be resolved at the first rung able to hold it: routed to an agent authority when one is competent to decide; parked in the `blocked` state with a decision packet queued at the owning gate when only a human may decide but the situation is stable; interrupting a human only when parking is unsafe.

#### Scenario: Decidable within agent authority
- **WHEN** a decision falls within a declared agent authority per the escalation tables
- **THEN** it is routed and decided there
- **AND** no human is notified outside their normal gate visits

#### Scenario: Human-authority decision that can wait
- **WHEN** a decision requires human authority (ratification, privileged grant, above-envelope merge approval, contested-finding disposition, exhausted authority deadlock) and the situation does not deteriorate while waiting
- **THEN** the workflow parks in `blocked` with a decision-ready packet queued at the gate that human already owns
- **AND** no interrupt is issued

#### Scenario: Ladder precedence is binding
- **WHEN** an agent considers interrupting a human
- **THEN** it must first establish that neither routing nor parking can hold the situation

### Requirement: Interrupt legality
A human interrupt SHALL be legal only on containment failure — the situation actively deteriorates while parked AND no agent can contain it within its declared permissions — and MUST cite one of the enumerated interrupt classes: suspected live secret or credential exposure beyond agent revocation authority; evidence of active unauthorized access to governed systems; an irreversible external action already in flight that must be halted and that no agent holds authority to halt.

#### Scenario: Containment failure test is conjunctive
- **WHEN** a situation deteriorates but an agent can contain it within its own permissions (revert, block, disable a workflow)
- **THEN** the agent contains it and the decision parks
- **AND** no interrupt is issued

#### Scenario: Uncited interrupt is a violation
- **WHEN** a human interrupt is issued without citing an enumerated interrupt class in its audit record
- **THEN** the interrupt itself is recorded as a policy violation

#### Scenario: Class list grows only by proposal
- **WHEN** a genuine containment failure does not match an enumerated class
- **THEN** the interrupt is legal under the conjunctive test and its audit record MUST propose the missing class through the change process

### Requirement: Non-interrupting conditions
The model SHALL explicitly name as non-interrupting — parked or routed, never interrupted: failed checks, merge conflicts, authority deadlocks, contested findings, merge decisions outside the low-risk envelope, ambiguity of any routed class, and schedule or deadline pressure.

#### Scenario: Deadline pressure does not interrupt
- **WHEN** a parked decision approaches a milestone or external deadline
- **THEN** the deadline consequence is recorded in the decision packet
- **AND** the decision remains parked until the human's gate visit

#### Scenario: Deadlock parks after routing is exhausted
- **WHEN** primary and consulted authorities cannot converge after the routed escalation path is exhausted
- **THEN** the question parks as a decision packet at the appropriate governance gate

### Requirement: Low-risk enforcement envelope
The model SHALL define Merge Master's autonomous approval envelope conjunctively — every required deterministic check passes, any policy-required governed review verdict is ADMIT with no undispositioned conditions, ordinary revert suffices as rollback, the action is within approved scope, and no security findings are open — and any enforcement action failing any condition SHALL park at the merge gate rather than interrupt.

#### Scenario: Inside the envelope
- **WHEN** an enforcement action satisfies every envelope condition and deployment policy allows autonomous action
- **THEN** Merge Master may approve it without human involvement

#### Scenario: Outside the envelope
- **WHEN** any envelope condition fails
- **THEN** the action parks at the merge gate with a decision-ready packet
- **AND** no interrupt is issued on risk grounds alone

### Requirement: Parked-decision delivery
Every parked decision SHALL be delivered as a decision-ready packet — situation summary, at most three options with exactly one recommendation, evidence references, the consequence of each option and of deciding nothing — deduplicated by root cause, and governed by fail-closed silence: no response leaves the workflow blocked, and a timeout MUST NOT escalate autonomy, auto-proceed, or convert the parked decision into an interrupt.

#### Scenario: Packet is decision-ready
- **WHEN** a human opens a parked decision at a gate
- **THEN** the packet presents situation, options, one recommendation, evidence references, and consequences without requiring the human to assemble context from raw logs

#### Scenario: Duplicate root cause
- **WHEN** a new instance of an already-parked root cause arises
- **THEN** its evidence is appended to the existing packet
- **AND** no additional packet or notification is created

#### Scenario: Silence stays blocked
- **WHEN** a parked decision receives no response for any period
- **THEN** the workflow remains blocked and nothing proceeds by default

### Requirement: Structural parking in external enforcement
Where a domain's external enforcement system supports required human review, parked human-decision gates SHALL be encoded there as enforcement rules — named or counted required reviewers scoped to the surfaces that demand them — so that parking is fail-closed against agent misbehavior and the enforcement configuration is the machine-readable declaration of where a human gate exists.

#### Scenario: Engineering merge gate is structural
- **WHEN** codexFactory encodes its human merge gates
- **THEN** branch protection or rulesets require the named human review (via code-owner path scoping for human-gated surfaces), and the pull request cannot merge while that gate is pending

#### Scenario: Privileged deployment gate is structural
- **WHEN** a deploy or production action is policy-gated on explicit human approval
- **THEN** the enforcement system's deployment-approval mechanism (e.g. environment required reviewers) holds the action until the approval act occurs

#### Scenario: Pending structural gate is a park
- **WHEN** a required human review is pending in the enforcement system
- **THEN** the workflow is parked at that gate with its decision-ready packet attached to the work item
- **AND** no interrupt is issued for the pending review itself

#### Scenario: Autonomous lane coexists
- **WHEN** an enforcement action is inside the low-risk envelope on surfaces not scoped to a human gate
- **THEN** the Merge Master identity may satisfy the enforcement system's review requirement without human involvement, where deployment policy allows

### Requirement: Domain instantiation of the ladder
Each DomainxFactory SHALL map the interrupt classes and parked-decision gates to domain terms in its role instantiation documentation, and MUST NOT consult undefined role identifiers in its escalation routing.

#### Scenario: Engineering instantiation
- **WHEN** codexFactory revises its engineering escalation table
- **THEN** the merge approval row references the escalation ladder instead of the undefined `HR` identifier
- **AND** engineering examples of the interrupt classes are documented in GitHub terms

#### Scenario: Dangling consultation identifiers
- **WHEN** a domain role doc consults a role identifier
- **THEN** the identifier is defined in the neutral model or the domain's own instantiation

