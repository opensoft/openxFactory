# Project UI Constitution and Experience Memory — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Give Project/Subject Hermes a versioned UI constitution and decision memory that explain what the experience should optimize for, beyond merely preserving previously approved screenshots.
Topics: agent-assisted-app-testing, project-ui-constitution, subject-hermes, experience-memory, design-intent
Repository context: openxFactory; project-specific browser experience intent with tenant/domain constraints and a later Flutter realization
Captured: 2026-08-02

## Possible feats

- **Project UI constitution** — describe approved personas, journeys, design principles, interaction rules, protected surfaces, and quality objectives in a versioned repository artifact.
- **Experience decision memory** — retain accepted and rejected proposals, rationales, known platform variances, and observed outcomes for future Subject Hermes decisions.

## Focus

An approved screenshot says what the application looked like in one state and rendering profile. It does not say whether that state is easy to use, consistent with the product's goals, accessible, or worth preserving. Autonomous improvement needs an intent authority that can answer what “better” means for this project.

The proposed UI constitution is the project-specific design and experience context owned through Project/Subject Hermes. It is constrained by Domain Hermes practice and Tenant Hermes policy, but remains distinct from runtime snapshots, component specifications, and the personal taste of any one design agent.

## Proposed model

The three Hermes layers contribute different parts of the effective constitution:

| Layer | Proposed ownership |
|---|---|
| Domain Hermes | Reusable UI/UX methods, accessibility practice, evidence requirements, reviewer qualifications, and domain-protected interaction rules |
| Tenant Hermes | Brand and house style, approved model/provider policy, local accessibility commitments, cost limits, and stricter review or data-handling rules |
| Project/Subject Hermes | Personas, journeys, product objectives, accepted component patterns, local exceptions, baseline lineage, current improvement priorities, and decision history |

An illustrative project record could contain:

```yaml
ui_constitution:
  version: 3
  project_ref: project-alfa
  personas:
    - id: clinic-scheduler
      primary_goals: [find_patient, schedule_visit, recover_from_conflict]
  critical_journeys:
    - id: schedule-visit
      success_criteria: [completed_without_dead_end, keyboard_operable]
  experience_principles:
    - preserve_clear_primary_action
    - explain_irreversible_actions_before_commit
    - prefer_progressive_disclosure_over_dense_forms
  design_system_ref: repo://design-system/manifest.yaml
  content_rules_ref: repo://content/tone-and-terminology.yaml
  accessibility_profile: wcag-project-profile-v1
  supported_viewports: [mobile, tablet, desktop]
  protected_surfaces: [authentication, consent, payment, clinical-decision]
  known_platform_variances_ref: repo://ui-baselines/platform-variances.yaml
  autonomy_policy_ref: repo://policy/ui-change-autonomy.yaml
```

The exact shape is open. The load-bearing distinction is between:

- **experience intent:** constitution, personas, journeys, and acceptance objectives;
- **runtime truth:** approved snapshots and functional evidence;
- **implementation constraints:** component specs, tokens, architecture, and safety rules;
- **decision history:** why prior proposals were accepted, rejected, narrowed, or escalated.

### Experience memory

Subject Hermes should retain structured references to:

- annotations and Hermes-generated observations;
- selected and rejected design variants;
- council findings and Project Owner decisions;
- Project Manager priority and batching decisions;
- baseline migrations and platform-specific exceptions;
- recurring usability failures and repaired regressions;
- measured post-merge outcomes when approved telemetry is available.

The memory should distinguish observed evidence from inferred preference. Repetition may justify a new suggestion, but it must not silently rewrite the constitution or widen the autonomy envelope.

## Interfaces and boundaries

The constitution is consumed by the autonomous observatory, design specialists, experience council, scope router, spec checker, and Project Owner admission decision. It emits pinned references and project-specific evaluation criteria.

It does not replace component specifications, baseline images, accessibility tooling, domain policy, or a ratified authority rule. An ordinary UI change may cite the constitution but must not modify the constitution as a side effect. Proposed changes to the judging rules, protected surfaces, thresholds, or autonomy policy travel through a separate governed policy path.

Figma may project or supplement selected visual intent, but the versioned repository record remains the inspectable project reference for automated decisions.

## Alternatives and tensions

- **Snapshots alone:** are concrete and testable, but preserve defects as readily as good design.
- **Figma as constitution:** gives designers a familiar surface, but mixes hosted design state with runtime and policy authority.
- **Free-form project memory:** captures nuance, but is hard to validate and can drift into implicit policy.
- **Highly structured constitution:** improves repeatability, but may overconstrain useful design exploration.
- **Automatic preference learning:** can adapt quickly, but risks turning model self-consistency into product intent without an accountable decision.

## Open questions

- Which constitution fields are mandatory before Hermes may originate improvements?
- Does the Project Owner own every constitution update, or can designated low-risk sections be maintained by a Project Hermes experience steward?
- Which project telemetry may be retained as experience evidence, and under what privacy policy?
- How are contradictions among Domain, Tenant, and Project layers surfaced and resolved?
- Which parts of the constitution should later map directly to Flutter themes, semantics, and golden-test states?

## Relationships

- [xFactory Domain Factory Model](../../docs/xfactory-domain-factory-model.md) supplies the Domain, Tenant, Subject Hermes, and Omnigent layer boundaries this constitution composes.
- [Project/Customer (Subject) Layer Scaffold](project-layer-scaffold.md) supplies the Project Owner and Project Manager roster and project-specific content model.
- [Approved UI Source of Truth](agent-assisted-app-testing-approved-ui-source.md) supplies runtime pixel truth while this document supplies experience intent.
- [Autonomous UI Observatory](agent-assisted-app-testing-autonomous-ui-observatory.md) uses personas, journeys, and quality objectives to decide what to inspect.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) evaluates proposals against the pinned constitution.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) references protected surfaces and project-specific limits.
- [Synthesis: Autonomous Experience Management](agent-assisted-app-testing-synthesis-autonomous-experience-management.md) joins the constitution to proactive testing and agent admission.
