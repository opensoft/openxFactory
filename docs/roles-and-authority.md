# Roles And Authority

Status: draft
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
| `Merge Master` | Merge authority agent | final risk interpretation and external enforcement action policy | approve low-risk ready actions, request human review, or block |

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
contracts, data ownership, authorization, tenant isolation, merge risk, or
human-review requirements.

Role-keyed escalation routing lives with each domain's role instantiation
(engineering: `codexFactory/docs/engineering-roles-and-authority.md`).

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

- approve low-risk enforcement actions when policy allows;
- request human or team review for medium/high-risk actions;
- block an enforcement action with a documented reason.

Human review is required for risky reviews. Hermes should act as a real review
authority for low-risk work once the domain enforcement system accepts the Merge
Master identity, but it must route human review for risk that exceeds its
authority.

For `codexFactory`, the external enforcement system is GitHub: pull requests,
checks, branch protection, reviews, merge queues, and merge commits.

## Role Rule Of Thumb

```text
PO answers: what should the user or business get?
PM answers: when, in what order, and with what coordination?
CA answers: how must the overall system behave and integrate?
PA answers: how should this project fit that system architecture?
Merge Council answers: is the work product ready based on evidence?
Merge Master answers: approve, request human review, or block?
```
