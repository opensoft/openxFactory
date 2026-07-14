# Roles And Authority

Status: ratified
Ratified by: define-human-escalation-contract; amended by add-github-app-identity-tiers
Kind: architecture

This document is the canonical `openxFactory` cross-factory role and
authority model. Domain execution roles are instantiated per DomainxFactory
(split-roles-authority change, DTN-013) — for software engineering, see
`codexFactory/docs/engineering-roles-and-authority.md`. Install repositories
may keep operational implementation notes (see `opensoft/Omnigent-Install`
docs), but cross-factory responsibility, approval, escalation, and routing
policy starts here.

## Authority Layers

Hermes and Omnigent have different authority layers.

```text
Hermes
  Portfolio, product, project, system architecture, policy, memory,
  approvals, risk, escalation, merge authority, and dashboard truth.

Domain Omnigent / execution layer
  Domain-specific orchestration inside Hermes-approved boundaries.

Domain execution framework
  Domain-specific workflow mechanism selected by the owning DomainxFactory.

External enforcement system
  Domain-specific final-state enforcement after review and admission.
```

Hermes decides what is approved to pursue and whether a work product may enter
the next admission path. Domain Omnigent decides how approved domain work is
decomposed, assigned, checked, and prepared for admission. The external
enforcement system applies final state where the domain workflow requires it.

## Architecture Language

Use these terms deliberately:

```text
system architecture
  The overall way the product, portfolio, and projects behave and integrate.
  Owned by Hermes CA, with PA participation for project-level impact.

project architecture
  The architecture model for one project as a product/system inside Hermes.
  Owned by Hermes PA, constrained by CA decisions.

subsystem architecture
  The local implementation architecture inside one approved project
  boundary (for engineering: repos, services, packages, modules, data
  models). Owned by the domain execution architect — engineering: Omnigent
  LA, per codexFactory's role instantiation.
```

This split keeps the source of truth for whole-system behavior in Hermes while
still giving Omnigent strong local architecture authority for execution.

## Hermes-Level Roles

Hermes-level roles own portfolio, product, project, policy, memory, approval,
and escalation truth across repos.

| ID | Role | Owns | Decides |
|---|---|---|---|
| `PO` | Project Owner | business outcome, product vision, release value, user-visible behavior, acceptance intent | what problem the feature solves, what is in or out of scope, whether behavior preserves product value |
| `PM` | Project Manager | sequencing, milestones, dependency coordination, capacity, delivery process, stakeholder coordination | when work happens, how features are sequenced, who must be consulted or escalated |
| `CA` | Chief Architect | system architecture, cross-project boundaries, canonical data ownership, product-wide contracts, long-lived architecture memory | which system owns a capability, how projects integrate, which contracts are canonical, whether repo design violates the system model |
| `PA` | Project Architect | project architecture, project-level technical direction, project integration shape, project architecture decisions | how one project should satisfy CA constraints, where project boundaries sit, whether project architecture remains coherent |
| `Merge Council` | Merge readiness body | multi-lane readiness evidence and blocking findings | whether a domain work product is ready, not ready, or needs fixes before enforcement |
| `Merge Master` | Merge authority agent | final risk interpretation and external enforcement action policy | approve actions inside the low-risk envelope, park out-of-envelope actions for the human gate, or block |

Hermes roles do not own day-to-day code structure, coder assignment, local test
mechanics, or repository repair loops unless a local decision affects product
meaning, project sequencing, system architecture, security, or merge risk.

## Domain Execution Roles

Each DomainxFactory instantiates the execution lead roles that decompose,
implement, verify, integrate, and secure its approved work, declared as a
specialization of this model in its own repository. Execution roles may
recommend scope, risk, and admission decisions, but Hermes owns approval and
escalation, and a domain executor must not be the authority that approves
its own admission path.

Engineering instantiation (LA, LE, LC, LQ, LI, LS):
`codexFactory/docs/engineering-roles-and-authority.md`.

## Escalation Boundaries

Omnigent must escalate to Hermes when a repo-level decision changes product
meaning, project priority, system architecture, project architecture, canonical
contracts, data ownership, authorization, tenant isolation, or merge risk.
Whether the escalation reaches a human — and how — is decided by the Human
Escalation Contract below, never ad hoc.

Role-keyed escalation routing lives with each domain's role instantiation
(engineering: `codexFactory/docs/engineering-roles-and-authority.md`).

## Human Escalation Contract

Human attention is the scarcest resource in the factory. Every situation
requiring a decision resolves at the first rung of this ladder able to hold
it:

```text
1. Route      an agent authority is competent to decide
              -> decide there, per the escalation tables. No human.

2. Park       only a human may decide, and the situation is stable
              -> workflow enters `blocked`; a decision-ready packet queues
                 at the gate that human already owns. The human decides on
                 their own schedule. This is the default and near-universal
                 human path.

3. Interrupt  parking is unsafe
              -> claim human attention now. Legal only on containment
                 failure, defined below.
```

### Parked decisions

Decisions that require human authority park; they never interrupt:
ratification acts, privileged capability grants (deployment, production),
enforcement actions outside the low-risk envelope, contested-finding
dispositions, and authority deadlocks after the routed escalation path is
exhausted.

Every parked decision is delivered as a decision-ready packet: situation
summary, at most three options with exactly one recommendation, evidence
references, and the consequence of each option and of deciding nothing.
Packets deduplicate by root cause — a new instance of a parked root cause
appends evidence to the existing packet and never re-notifies. Silence is
fail-closed: no response leaves the workflow blocked; a timeout must never
escalate autonomy, auto-proceed, or convert a parked decision into an
interrupt.

### Interrupts

An interrupt is legal only on containment failure — both conditions must
hold:

1. the situation actively deteriorates while parked, and
2. no agent can contain it within its declared permissions.

The interrupt classes are a closed set:

- suspected live secret or credential exposure beyond agent revocation
  authority;
- evidence of active unauthorized access to governed systems;
- an irreversible external action already in flight that must be halted and
  that no agent holds authority to halt.

Every interrupt must cite its class in the audit record; an uncited
interrupt is itself a policy violation. A genuine containment failure
outside the class list is legal under the two-condition test, and its audit
record must propose the missing class through the change process. Tenant
policy may add classes for its deployment; the neutral set stays minimal.

Explicitly non-interrupting — parked or routed, never interrupted: failed
checks, merge conflicts, authority deadlocks, contested findings,
enforcement decisions outside the low-risk envelope, ambiguity of any
routed class, and schedule or deadline pressure. Deadline consequences
belong in the decision packet, not in a notification.

### Structural parking

Where a domain's external enforcement system supports required human
review, the parked human gates are encoded there as enforcement rules —
named or counted required reviewers scoped to the surfaces that demand
them, and deployment-approval reviewers for privileged actions. Parking
then holds even against a misbehaving agent, a pending required review is a
park by construction (the enforcement system holds the door without
paging), and the enforcement configuration is the machine-readable
declaration of where a human gate exists. For engineering the mechanisms
are GitHub branch protection/rulesets, code-owner path scoping, and
environment required reviewers; each domain names its equivalents in its
role instantiation.

### External enforcement identity separation

Structural parking only holds if the identity that can reconfigure the
enforcement mechanism itself is separate from the identity doing ordinary
content or workflow work on the same surface — otherwise a routine-work
identity could quietly weaken or remove the gate it is meant to be subject
to. Any identity capable of modifying a structural human-review gate MUST be
authority-separated from any identity performing ordinary content/workflow
actions on that surface.

For GitHub, this splits into two tiers. A **content-tier** identity performs
ordinary factory work — reports, review-record pull requests, pin-sync
commits — under the existing rules, and holds no permission capable of
changing rulesets or branch protection. An **administration-tier** identity
holds the permission to change those rules, applies only rules-as-code
configuration that has passed the governed review lane and ratify gate, and
performs no content work. Neither tier escalates the other. This tiering
governs identities operating on Opensoft's own vendor build org; a client
tenant's own GitHub identities are out of scope here.

An administration-tier identity's credentials are held under the canonical
credential-contracts shapes (see `docs/credential-access-model.md`) with
least-authority defaults: a vaulted key, short-lived and workflow-scoped
runtime grants, human and domain approval before grant issuance, and an
audit record — with an evidence reference to the reviewed configuration
change that authorized it — for every action.

## Domain Execution Ownership

`openxFactory` owns cross-factory authority, escalation, and neutral workflow
gates. It does not own every domain's execution mechanics.

```text
openxFactory
  owns approved intent, decomposition gate, execution gate, validation gate,
  review gate, admission gate, external enforcement handoff, traceability, and
  escalation policy.

DomainxFactory repos
  own domain-specific execution roles, stage mechanics, artifact formats,
  validators, and worker routing.
```

For software engineering, `codexFactory` owns Spec Kit stage ownership,
engineering clarification routing, branch review, PR admission packet format,
and merge readiness packet format. The current engineering policy lives in:

```text
opensoft/codexFactory/docs/spec-kit-engineering-flow.md
opensoft/codexFactory/docs/feature-decomposition-traceability.md
opensoft/codexFactory/docs/pr-admission-merge-readiness.md
```

Other DomainxFactories use the same neutral gates but specialize them with their
own domain artifacts and review roles.

## Hermes Profiles And Groups

The factory uses one Hermes install with many logical profiles and groups —
routing, permission, escalation, dashboard, and reviewer boundaries, not
separate installs. A profile can belong to more than one group, with one
`home_group` for primary ownership. Concrete group and profile definitions
are deployment instantiation and live with the owning domain (engineering:
`codexFactory/docs/engineering-roles-and-authority.md`).

## External Enforcement Authority

The Merge Council is a Hermes-convened readiness body. It reviews evidence and
emits blocking findings, warnings, and required fixes. It does not merge code
and does not bypass the external enforcement system.

The Merge Master is a Hermes governance agent. It reads Merge Council output,
external enforcement checks, admission state, traceability, and risk policy. It
may:

- approve enforcement actions inside the low-risk envelope when deployment
  policy allows;
- park any action outside the envelope at the owning gate as a
  decision-ready packet (per the Human Escalation Contract);
- block an enforcement action with a documented reason.

The low-risk envelope is conjunctive — an action is inside it only when ALL
hold:

- every required deterministic check passes;
- any policy-required governed review verdict is ADMIT with no
  undispositioned conditions;
- ordinary revert suffices as rollback;
- the action is within approved scope;
- no security findings are open.

An action failing any condition parks at the merge gate; risk grounds alone
never produce an interrupt. Hermes should act as a real review authority
for in-envelope work once the domain enforcement system accepts the Merge
Master identity on surfaces not scoped to a human gate; human-gated
surfaces always require the human act.

For `codexFactory`, the external enforcement system is GitHub: pull requests,
checks, branch protection, reviews, merge queues, and merge commits.

## Role Rule Of Thumb

```text
PO answers: what should the user or business get?
PM answers: when, in what order, and with what coordination?
CA answers: how must the overall system behave and integrate?
PA answers: how should this project fit that system architecture?
Merge Council answers: is the work product ready based on evidence?
Merge Master answers: in-envelope approve, park for the human gate, or block?
```
