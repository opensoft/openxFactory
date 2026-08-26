# Spec-Aware Change Safety — Brainstorm

Status: brainstorm
Kind: process
Summary: Check an intended app change against versioned component and workflow constraints before implementation, blocking violations unless a scoped override is issued by the authority named in the active policy.
Topics: agent-assisted-app-testing, spec-validation, change-safety, accessibility, workflow-constraints, override-consent
Repository context: openxFactory; neutral safety pattern for browser components first and future Flutter widgets or flows later
Captured: 2026-08-02

## Possible feats

- **Component specification schema** — describe required props, accessibility guarantees, workflow constraints, and design-token bounds in a versioned, discoverable form.
- **Pre-implementation constraint check** — produce a machine-readable verdict and block or escalate a proposed change when a constraint is violated or unknown.
- **Scoped override record** — preserve the authorizing role, reason, affected intent, constraint, and expiry when policy permits an exception.

## Focus

Fast implementation is unsafe when the agent treats the annotation as the only authority. A request that appears visual can remove a required action, weaken accessibility, or break a workflow. The agent needs a pre-edit safety check that is close enough to the target component or flow to be useful and explicit enough to be audited.

## Proposed model

A component or workflow specification could be co-located with a story, component, or route and might include:

```yaml
component: Button
version: 1.2.0
required_props:
  - label: string
  - onClick: function
optional_props:
  - variant: [primary, secondary, danger]
  - disabled: boolean
workflow_constraints:
  - "Must have a visible accessible label"
  - "onClick must trigger navigation or an allowed action"
  - "Cannot remove Cancel in modal contexts"
design_tokens:
  min_height: 44px
  font_family: var(--font-primary)
```

Before editing, the agent would:

1. resolve the most relevant spec and its version;
2. translate the annotation into a proposed change plan;
3. check required props, accessibility rules, workflow constraints, and token bounds;
4. record `pass`, `violation`, `unknown`, or `stale-spec` with citations to the relevant constraint and code/story context;
5. block implementation or request a decision from the authority named for that constraint when a violation or material unknown exists.

For example, “remove the cancel button” should not be treated as an ordinary visual change when the target is a modal with a `Cannot remove Cancel` constraint. A permitted override should name the constraint, scope, reason, authorizing Hermes or human/professional role, policy reference, and expiration or re-review condition. The override is an exception to the constraint, not a rewrite of the specification.

The UI autonomy envelope should fail closed on a spec violation, stale spec, or material unknown. Routine Project Hermes admission may resolve only constraints whose policy explicitly delegates that authority. Protected workflow, accessibility, security, regulatory, or governing-policy exceptions remain at their existing gates.

The safety layer should distinguish product constraints, accessibility requirements, and domain or regulatory obligations. A component spec can expose evidence and checks, but it cannot by itself certify legal or clinical compliance.

The same pattern can later protect Flutter widgets and flows. The adapter may resolve widget keys, semantics labels, route/state models, and golden/accessibility constraints while keeping the pre-edit verdict and override shape common.

## Interfaces and boundaries

The checker consumes the intent, proposed plan, target spec, source/story context, and optionally existing test evidence. It emits a verdict, constraint references, missing-evidence warnings, and—only when explicitly authorized—an override record.

It owns admission to the implementation step, not code generation, test execution, preview deployment, or merge approval. A missing spec should not be reported as “safe”; it should be visible as an unguarded or unknown condition with a configured route, block, or park policy.

## Alternatives and tensions

- **Hard constraints versus advisories:** hard blocking protects important invariants but can slow iteration; advisories preserve speed but risk being ignored for high-consequence workflows.
- **Co-located specs versus central registry:** co-location improves discovery and change locality; a registry supports cross-component policy but can drift from source.
- **Schema checks versus LLM interpretation:** schemas give stable validation; an LLM is useful for mapping prose and code to constraints but should not be the sole authority.
- **Automatic spec updates versus explicit maintenance:** generating spec changes from implementation can reduce drift, but silently weakening a constraint is an unsafe side effect.

## Open questions

- Which constraints are always blocking, and which may be advisory?
- How does the checker resolve contextual rules such as “Cancel is required in modal contexts”?
- Who owns and reviews component specifications, especially when a shared component spans factories?
- How should stale, missing, or conflicting specs affect an otherwise fast fix?
- What evidence and authorization are required for a project, domain, accessibility, security, or regulatory override?

## Relationships

- [Annotation-Centered Test Intent](agent-assisted-app-testing-intent.md) supplies the desired change and target context.
- [Preview Verification and Feedback Loop](agent-assisted-app-testing-preview-approval.md) returns integrated evidence to Project Hermes and optional user feedback.
- [Synthesis: Hermes Autonomy and Human Exception Control](agent-assisted-app-testing-synthesis-human-control-and-safety.md) places this check in the full authority chain.
- [Project UI Constitution and Experience Memory](agent-assisted-app-testing-ui-constitution.md) supplies project-specific interaction and protected-surface intent.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) consumes the verdict and prevents ordinary UI work from weakening its own constraints.
