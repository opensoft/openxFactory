# Roles And Authority

Status: draft

This document is the canonical `openxFactory` role and authority model for the
AI software development factory. Install repositories may keep operational
implementation notes, but cross-factory responsibility, approval, escalation,
and routing policy starts here.

## Source Provenance

Reviewed sources:

- `/home/brett/projects/Agents/Omnigent-Install/docs/project-lead-agents.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/hermes-governance-agents.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/hermes-profiles-and-groups.md`
- `/home/brett/projects/Agents/Hermes-Install/README.md`

The install repo copies remain in place until a later migration feature marks
them as canonical links, legacy copies, or install-specific runbooks.

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
  The repo, service, package, module, data model, and local implementation
  architecture inside one approved project boundary.
  Owned by Omnigent LA.
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

## Omnigent Execution Roles

Omnigent roles execute inside a specific repo, service, project implementation,
or approved domain work unit.

| ID | Role | Owns | Decides |
|---|---|---|---|
| `LA` | Lead Architect | subsystem architecture, repo/service/module boundaries, local tech stack, internal interfaces, local data model implementation | how the repo is structured to satisfy PA and CA constraints, whether local implementation design is coherent |
| `LE` | Lead Engineer | engineering interpretation, feasibility, feature decomposition, stage-gate readiness | how approved software scope becomes executable engineering work inside `codexFactory`, which questions must be routed, whether a feature is ready for implementation |
| `LC` | Lead Coder / Coding Agent Manager | coder assignment, implementation strategy, code execution, local repair loop, implementation readiness | which coder agents do which tasks, how local failures are repaired, whether implementation evidence is ready |
| `LQ` | Lead Quality Engineer | test strategy, acceptance coverage, regression coverage, quality gates, test evidence | what evidence proves acceptance criteria, which tests are required, whether quality gates are satisfied |
| `LI` | Lead Integration Engineer | merge sequencing, dependency DAG validation, integration branch checks, conflict detection, cross-feature compatibility | safe merge order, dependency sequencing, integration readiness across branches |
| `LS` | Lead Security Engineer | threat model, authorization, tenant isolation, secrets handling, security acceptance criteria | required security controls, sufficiency of security evidence, whether security risk requires escalation |

Omnigent roles may recommend scope, risk, and merge decisions, but Hermes owns
approval and escalation. The engineering executor must not be the same
authority that approves its own merge path.

## Escalation Boundaries

Omnigent must escalate to Hermes when a repo-level decision changes product
meaning, project priority, system architecture, project architecture, canonical
contracts, data ownership, authorization, tenant isolation, merge risk, or
human-review requirements.

Common escalation routes:

| Question Type | Primary Authority | Consulted |
|---|---|---|
| Product meaning, visible behavior, scope | `PO` | `PM`, `LE` |
| Milestone, capacity, sequencing | `PM` | `PO`, `LI`, `LE` |
| Cross-project system architecture | `CA` | `PA`, `LA`, `LI` |
| Project architecture | `PA` | `CA`, `LA`, `LE` |
| Subsystem architecture | `LA` | `PA`, `LE`, `LC` |
| Security, tenant isolation, secrets | `LS` | `CA`, `PA`, `LQ` |
| Test evidence and quality gates | `LQ` | `LE`, `LC` |
| Integration and merge sequencing | `LI` | `PM`, `LE`, `LA` |
| Implementation feasibility | `LC` | `LE`, `LA`, `LQ` |
| Merge approval or escalation | `Merge Master` | `Merge Council`, `HR` when present |

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

The factory uses one Hermes install with many logical profiles and groups. The
groups are routing, permission, escalation, dashboard, and reviewer boundaries;
they are not separate Hermes installs.

```yaml
groups:
  opensoft/hermes-governance:
    purpose: Hermes-level governance, approvals, escalation, merge authority
    agents:
      - PO
      - PM
      - CA
      - PA
      - Merge Council
      - Merge Master

  opensoft/hermes-architecture:
    purpose: CA and PA reviews, system architecture, and project architecture
    agents:
      - CA
      - PA
      - LA

  opensoft/hermes-security:
    purpose: high-risk security and tenant isolation escalations
    agents:
      - LS
      - CA
      - PA
      - Merge Master

  opensoft/omnigent-engineering:
    purpose: repo execution leads
    agents:
      - LA
      - LE
      - LC
      - LQ
      - LI
      - LS
```

A profile can belong to more than one group. Each profile has one `home_group`
for primary ownership and a `member_of` list for routing, review, escalation,
and dashboard visibility.

Example:

```yaml
profiles:
  CA1:
    role: CA
    home_group: opensoft/hermes-governance
    member_of:
      - opensoft/hermes-governance
      - opensoft/hermes-architecture
      - opensoft/hermes-security

  A1:
    role: LA
    home_group: opensoft/omnigent-engineering
    member_of:
      - opensoft/omnigent-engineering
      - opensoft/hermes-architecture
```

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
LA answers: how should this repo or subsystem be designed?
LE answers: how does approved intent become executable engineering work?
LC answers: how do coder agents implement and repair it?
LQ answers: how do we prove it works?
LI answers: how do we integrate and merge safely?
LS answers: how do we keep it secure?
Merge Council answers: is the PR ready based on evidence?
Merge Master answers: approve, request human review, or block?
```
