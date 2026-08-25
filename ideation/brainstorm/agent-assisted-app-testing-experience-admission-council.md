# Experience Admission Council — Brainstorm

Status: brainstorm
Kind: process
Summary: Convene independent UI/UX, accessibility, design-system, and browser-quality findings into a Subject Hermes decision packet so the Project Owner can admit user-visible behavior while the Project Manager manages the loop.
Topics: agent-assisted-app-testing, experience-admission-council, subject-hermes, governed-review, ui-ux, merge-readiness
Repository context: openxFactory; Project Hermes experience review before Merge Council and external Git/CI enforcement
Captured: 2026-08-02

## Possible feats

- **Experience admission record** — bind proposal intent, independent specialist findings, deterministic evidence, Project Owner verdict, Project Manager coordination state, and conditions to one revision.
- **Risk-routed experience council** — select the minimum qualified review roster and escalation path from the UI change class and protected-surface policy.

## Focus

Removing the human from routine UI management requires a real agent authority, not merely a vision model that approves its own aesthetics. The Experience Admission Council is a Hermes-convened readiness body for user-visible behavior. It assembles specialist evidence and findings; the Project Owner owns the acceptance verdict, while the Project Manager owns sequence, coordination, budget, and disposition of required fixes.

The council is distinct from the Merge Council. Experience admission asks whether the implemented UI preserves or improves product value under the project constitution. Merge readiness asks whether the complete engineering work product may enter external enforcement.

## Proposed model

```text
design intent + implemented revision + complete evidence packet
                              │
                              ▼
                  Experience Admission Council
        ┌──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
   visual review   UX/journey     accessibility   browser quality
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                              ▼
                 findings + disagreements + risks
                              │
                    Project Manager disposition
                              │
                              ▼
                    Project Owner decision
                   ADMIT | FIX | PARK | REJECT
                              │
                              ▼
                 Merge Council readiness evidence
```

### Council inputs

- the originating annotation, Hermes observation, or regression intent;
- project UI constitution and accepted design/spec references;
- proposal and variant-selection rationale;
- implementation revision and affected-surface inventory;
- Storybook, Playwright, accessibility, visual, responsive, performance, and OS-profile evidence required by policy;
- baseline changes and render-manifest lineage;
- specialist assignment and independence record;
- autonomy/risk classification and any unresolved assumption.

### Findings and verdicts

Each specialist should return structured findings with severity, affected region or journey, evidence refs, rationale, confidence, and a proposed disposition. The council packet retains disagreement rather than flattening it into a vote count.

The proposed Project Owner verdict vocabulary is:

- `ADMIT` — user-visible behavior satisfies the constitution and all required conditions;
- `FIX` — the direction remains valid but blocking findings require another implementation/review iteration;
- `PARK` — authority, evidence, policy, or specialist competency is insufficient for an agent decision;
- `REJECT` — the proposal conflicts with project intent or would make the experience worse;
- `ADMIT_WITH_CONDITIONS` — only when policy allows explicit, time-bounded follow-up conditions that do not conceal a blocking defect.

The Project Manager records scheduling, capacity, dependency, and iteration disposition. The PM does not overrule a product-acceptance finding or invent missing user intent. The Project Owner does not waive deterministic quality, security, or protected-surface gates merely by preferring the design.

### Pre- and post-implementation review

Nontrivial changes may use two council checkpoints:

1. **Design admission:** select or narrow a proposed variant before code is changed.
2. **Experience admission:** verify that the implemented revision realizes the selected design and remains acceptable in tested journeys and profiles.

Regression repairs that return exactly to an approved state may skip design admission when the autonomy policy allows it, but still require independent verification and a recorded experience verdict.

## Interfaces and boundaries

The council consumes a decision-ready experience packet and emits specialist findings, disagreements, required fixes, the Project Owner verdict, and Project Manager disposition. The record is tied to the exact revision and baseline candidate.

It does not merge code, alter baselines outside the approved revision, modify the autonomy policy, grant credentials, override protected workflow constraints, or substitute for security/architecture review. The Merge Council and Merge Master consume its result under the broader engineering authority model.

## Alternatives and tensions

- **Simple majority vote:** is easy to automate, but treats unlike competencies and finding severities as interchangeable.
- **Single judge synthesis:** creates a coherent decision, but can hide minority blocking evidence unless the packet preserves it.
- **Project Owner only:** respects product authority, but lacks independent domain evidence.
- **Council on every cosmetic repair:** maximizes process, but may cost more than the change; the autonomy envelope should select the smallest honest roster.
- **Human design owner by default:** provides familiar accountability, but keeps humans in routine management and prevents the intended autonomous factory loop.

## Open questions

- Which finding classes are always blocking regardless of Project Owner preference?
- May `ADMIT_WITH_CONDITIONS` enter merge, or should every condition be resolved first in v1?
- What minimum independence and reviewer qualification evidence must accompany an `ADMIT` verdict?
- When does a cross-project design-system change require Domain Hermes or Project Architect participation?
- How should council disagreement be presented to the Merge Council without duplicating review?

## Relationships

- [Roles and Authority](../../docs/roles-and-authority.md) supplies the canonical Project Owner, Project Manager, Merge Council, and Merge Master authority split.
- [UI Specialist Team and Separation of Duties](agent-assisted-app-testing-ui-specialist-separation.md) supplies the council roster and independence evidence.
- [Project UI Constitution and Experience Memory](agent-assisted-app-testing-ui-constitution.md) supplies product-specific evaluation criteria.
- [Hermes Designer Visual Review](agent-assisted-app-testing-hermes-visual-review.md) contributes a visual specialist finding.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) determines when the council may resolve the change without human management.
- [Synthesis: Autonomous Experience Management](agent-assisted-app-testing-synthesis-autonomous-experience-management.md) joins the council to proactive observation and merge admission.
