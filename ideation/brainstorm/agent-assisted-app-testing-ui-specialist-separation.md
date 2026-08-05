# UI Specialist Team and Separation of Duties — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Compose distinct visual, interaction, design-system, accessibility, content, browser-quality, and implementation agents while preventing the same agent from being the sole proposer, executor, reviewer, and approver of a UI change.
Topics: agent-assisted-app-testing, ui-specialist-team, separation-of-duties, omnigent, ui-ux, agent-roster
Repository context: openxFactory; project-specialized UI/UX workers under Subject Hermes control and Domain/Tenant policy
Captured: 2026-08-02

## Possible feats

- **Project UI specialist roster** — bind qualified design, experience, accessibility, content, test, and implementation roles to a project and risk profile.
- **UI change duty-separation check** — reject admission when proposer, implementer, reviewer, or authority identities collapse beyond the configured envelope.

## Focus

“UI/UX expert agent” hides several different competencies. A visually polished screen can still have a poor journey, inaccessible interaction, inconsistent component usage, misleading copy, or fragile implementation. Autonomous management needs specialist perspectives and explicit independence between creating a change and approving it.

The specialist team belongs to the Project Omnigent execution plane. Project/Subject Hermes commissions, prioritizes, and decides; Domain Hermes supplies reusable practice and qualifications; Tenant Hermes applies local provider, brand, privacy, and risk policy.

## Proposed model

Candidate specialist roles are:

| Role | Primary responsibility | Typical evidence |
|---|---|---|
| Visual/graphic designer | hierarchy, typography, color, spacing, composition, brand expression | variants, token references, visual rationale |
| Interaction/UX designer | journey, information architecture, affordances, error recovery, task friction | journey maps, interaction states, synthetic-task findings |
| Design-system specialist | component reuse, token conformance, pattern consistency, controlled exceptions | component/spec references, token and usage diffs |
| Accessibility specialist | semantics, keyboard behavior, focus, contrast, assistive-technology implications | automated findings, semantic-tree and manual-reasoning review |
| Content/microcopy specialist | labels, instructions, error messages, tone, terminology, comprehension | copy alternatives, terminology and reading-level evidence |
| Browser quality engineer | state coverage, functional tests, visual evidence, OS profiles, flake analysis | Storybook, Playwright, Loki, trace, and parity reports |
| UI implementation agent | component, style, state, and test changes inside the approved design proposal | code revision and implementation evidence |

A single model may temporarily fill more than one role in a small deployment, but each role invocation should still have a declared context, output contract, model/config identity, and authority ceiling. Identity reuse must not turn one model response into independent corroboration.

### Separation rules

- The implementation agent must not be the sole reviewer of its own change.
- A design proposer may explain and revise its proposal but may not issue the final experience-admission decision.
- The browser-quality role owns deterministic evidence and flake classification, not product desirability.
- Specialist reviewers emit findings and recommendations; Project/Subject Hermes owns the product decision.
- The Project Manager coordinates sequence, budget, and required participants; the Project Owner owns user-visible acceptance.
- The Merge Council and Merge Master remain separate from the implementation team and enforce the final readiness path.
- Changes to reviewer qualifications, duty-separation policy, or the autonomy envelope cannot be approved through the ordinary UI change they govern.

### Assignment record

Each change should retain an assignment and independence record:

```yaml
ui_team:
  proposal:
    visual_design: {agent: vd-03, model_config: sha256:...}
    interaction_design: {agent: ux-02, model_config: sha256:...}
  implementation:
    ui_coder: {agent: code-11, model_config: sha256:...}
  review:
    experience: {agent: ux-07, independent_of: [ux-02, code-11]}
    accessibility: {agent: a11y-02, independent_of: [code-11]}
    quality: {agent: lq-04, independent_of: [code-11]}
  authority:
    project_owner: po-project-alfa
    project_manager: pm-project-alfa
```

Model diversity may reduce correlated blind spots, but role separation, deterministic evidence, and authority separation are the first-order controls. A multi-model council should not be treated as independent merely because provider names differ.

## Interfaces and boundaries

The roster consumes project type, change class, surface risk, specialist qualification records, privacy/provider policy, and available worker capacity. It emits assignments, required artifacts, reviewer independence evidence, and escalation conditions.

It does not grant merge authority or allow specialists to rewrite project intent. A specialist may identify that the constitution or component spec is inadequate, but changing that authority surface requires a separate proposal.

## Alternatives and tensions

- **One generalist agent:** is fast and coherent, but concentrates blind spots and makes self-review difficult to distinguish from confidence.
- **Specialist council on every change:** improves coverage, but can be expensive for trivial repairs.
- **Risk-routed roster:** keeps routine work small and expands expertise for consequential changes, but requires trustworthy classification.
- **Same model, separate prompts:** preserves operational simplicity, but does not provide strong independence.
- **Different models/providers:** can diversify judgment, but adds cost, disclosure, and data-handling complexity.

## Open questions

- Which roles are mandatory for regression repairs, bounded improvements, and protected-surface changes?
- What qualification evidence is required before a specialist may issue a blocking finding?
- When is same-model role reuse acceptable, and how must it be disclosed?
- Should a design-system specialist live at Project, Tenant, or Domain scope for shared components?
- Which roles map cleanly to Flutter, and which need native-platform specialists?

## Relationships

- [Roles and Authority](../../docs/roles-and-authority.md) supplies the Project Owner, Project Manager, Merge Council, and Merge Master decision boundaries.
- [Hermes Designer Visual Review](agent-assisted-app-testing-hermes-visual-review.md) supplies one specialist review rather than the whole authority chain.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) convenes independent specialist findings into a decision-ready packet.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) selects the minimum roster and separation rules by change class.
- [Project UI Constitution and Experience Memory](agent-assisted-app-testing-ui-constitution.md) supplies the project intent against which specialists reason.
- [Synthesis: Autonomous Experience Management](agent-assisted-app-testing-synthesis-autonomous-experience-management.md) places the roster in the proactive design and admission loop.
