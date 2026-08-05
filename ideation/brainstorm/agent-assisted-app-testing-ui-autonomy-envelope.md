# UI Change Autonomy Envelope — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Define a conjunctive, project-scoped policy under which Subject Hermes may prioritize, approve, baseline, and send routine UI changes to merge without a human management step while parking protected or self-modifying decisions.
Topics: agent-assisted-app-testing, ui-autonomy-envelope, subject-hermes, auto-clear, human-escalation, merge-authority
Repository context: openxFactory; Project Hermes autonomy policy composed with Domain/Tenant constraints and external Git/CI enforcement
Captured: 2026-08-02

## Possible feats

- **UI autonomy policy** — classify UI changes and declare the evidence, role separation, rollback, budget, and protected-surface conditions required for agent-only admission.
- **UI auto-clear decision record** — prove why a proposal was inside or outside the active autonomy envelope at each approval boundary.

## Focus

The desired operating model removes humans from routine UI management, not from governance. Humans or accountable authorities establish product purpose, protected surfaces, legal/regulated constraints, and the autonomy policy. Subject Hermes then acts as a real manager and approval authority for changes that remain inside that policy.

The envelope must be conjunctive: one failed condition sends the work to another agent authority, blocks it, or parks it at an existing human/professional gate. Confidence alone cannot expand authority.

## Proposed model

Candidate change classes are:

| Change class | Example | Proposed default authority |
|---|---|---|
| Approved-state regression repair | Restore a component that drifted from its accepted story/baseline | Subject Hermes auto-admit after independent verification |
| Bounded experience improvement | Improve spacing, hierarchy, focus behavior, responsive layout, or an unambiguous label inside approved intent | Project Owner + Project Manager agent admission through the Experience Council |
| Project design-system change | Change a shared token, component contract, or pattern across many surfaces | Project Owner plus Project Architect/Domain design-system review |
| Product-meaning or workflow change | Add/remove steps, change navigation intent, alter business terminology or outcomes | Project Owner authority; park when the approved product record is insufficient |
| Protected-surface change | Authentication, authorization, consent, payment, clinical, regulated, destructive, or irreversible interaction | Existing human, professional, security, or domain gate |
| Governing-policy change | Relax a threshold, broaden a mask, modify protected surfaces, reviewer qualifications, or this envelope | Separate ratification path; never self-approved by the ordinary UI lane |

### Conjunctive auto-clear conditions

An agent-only decision is available only when all required conditions hold:

- the project, branch, target surfaces, and desired objective are inside approved scope;
- the active UI constitution, component specs, design tokens, and workflow constraints resolve without a violation or stale material unknown;
- the change does not alter permissions, data ownership, protected business rules, or a protected/regulated workflow;
- no threshold relaxation, mask expansion, fixture weakening, test deletion, or policy change is bundled with the implementation;
- every required functional, accessibility, visual, responsive, journey, performance, and OS-profile check passes or has a policy-approved nonblocking classification;
- proposer, implementer, required specialist reviewers, Project Owner, and Merge Master satisfy the configured separation rules;
- the Experience Council has no undispositioned blocking finding;
- the visual diff is localized, explainable, and tied to the intended revision and state;
- code, tests, snapshots, manifests, and approval records move together;
- ordinary revert is sufficient rollback and the preview or controlled environment remains reproducible;
- the work remains within time, spend, iteration, route/state, and model-provider limits;
- no live security finding, authority conflict, or external enforcement failure is open.

### Decision record

```yaml
ui_autonomy_decision:
  intent_id: intent-01J...
  project_ref: project-alfa
  change_class: bounded-experience-improvement
  policy_version: 2
  constitution_version: 3
  inside_envelope: true
  condition_results:
    scope: pass
    protected_surface: pass
    deterministic_checks: pass
    experience_council: admit
    separation_of_duties: pass
    rollback: pass
    budget: pass
  project_owner_decision_ref: approval://po/...
  project_manager_disposition_ref: approval://pm/...
  merge_readiness_ref: evidence://merge-council/...
```

The policy should name which failures route to another agent authority, which return to implementation, which block, and which park. A timeout never converts a park into permission.

## Interfaces and boundaries

The envelope consumes live Domain, Tenant, Project, security, architecture, review, and external-enforcement policy plus the complete change evidence. It emits an inside/outside decision, required route, approval refs, and unresolved conditions.

It does not grant standing production credentials, bypass branch protection, let one agent weaken its own tests, or make a policy change through precedent. The Merge Master still performs final risk interpretation and external enforcement only where Git/CI accepts that authority.

Human attention remains reserved for ratification, protected or regulated decisions, novel product meaning without adequate authority, contested findings that agent routing cannot resolve, and changes to the autonomy mechanism itself. These are exception gates, not routine management checkpoints.

## Alternatives and tensions

- **Human approval for every UI change:** is straightforward, but defeats autonomous project management and creates a queue for low-risk work.
- **Confidence-threshold autonomy:** is easy to implement, but mistakes model certainty for authority and evidence.
- **Allowlist-only repairs:** are very safe, but exclude valuable proactive usability improvements.
- **Conjunctive policy envelope:** supports meaningful autonomy, but requires disciplined specs, tests, roles, and evidence.
- **Self-adjusting thresholds:** may reduce noise, but lets the system redefine success from its own outcomes and should remain outside the ordinary lane.

## Open questions

- Which bounded experience changes are initially inside the v1 envelope?
- Is Project Owner admission sufficient for product-meaning changes when the PO is an agent, or must some categories remain human-ratified?
- Which protected surfaces apply globally versus by project archetype?
- What iteration, spend, and repeated-failure limit causes a change to park?
- Which external enforcement surfaces will accept the Merge Master agent identity without a human review rule?

## Relationships

- [Project UI Constitution and Experience Memory](agent-assisted-app-testing-ui-constitution.md) supplies project-specific objectives and protected surfaces.
- [Autonomous UI Observatory](agent-assisted-app-testing-autonomous-ui-observatory.md) uses the envelope to decide which findings can progress automatically.
- [UI Specialist Team and Separation of Duties](agent-assisted-app-testing-ui-specialist-separation.md) supplies independent roles and qualification evidence.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) emits the experience verdict consumed by the envelope.
- [Synthesis: Hermes Autonomy and Human Exception Control](agent-assisted-app-testing-synthesis-human-control-and-safety.md) places the envelope inside the broader safety and merge boundary.
- [Synthesis: Autonomous Experience Management](agent-assisted-app-testing-synthesis-autonomous-experience-management.md) joins auto-clear to the complete proactive loop.
