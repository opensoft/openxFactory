# Annotation-Centered Test Intent — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Treat a user annotation, Hermes UI observation, or detected regression as an environment-aware test intent that can be prioritized, routed, verified, admitted, and traced through merge.
Topics: agent-assisted-app-testing, annotation-intent, autonomous-ui-observatory, test-provenance, mcp, cross-platform-ui
Repository context: openxFactory; neutral intent and evidence vocabulary with an in-house browser annotation adapter first and a future Flutter adapter
Captured: 2026-08-02

## Possible feats

- **Annotation intent envelope** — define a versioned record for user intent, target identity, observed environment, and supporting evidence.
- **In-house annotation intake adapter** — expose annotation read, lifecycle, resolution, and bidirectional session operations without making the annotation store the test runner; optionally translate legacy VibeA records during migration.
- **Hermes-originated UI intent** — normalize proactive audit findings and regressions into the same lifecycle without presenting them as user-authored requests.

## Focus

The first handoff into implementation is not a test command; it is an observation made against a particular rendered app or controlled test surface. The observation may come from a person, a Hermes audit campaign, a regression detector, or approved telemetry. This document isolates the contract that preserves enough context for another environment and another tool to act on it without confusing the observation's origin or authority.

The useful unit is therefore a test intent, not merely a screenshot or a free-form bug report. It should say what the person saw, what they want changed, where it happened, and how the original observation was rendered.

## Proposed model

An in-house annotation or Hermes observation could be normalized into an intent envelope with fields such as:

```json
{
  "id": "intent-123",
  "origin": "user_annotation",
  "trigger": "browser_annotation",
  "note": "make this button more prominent",
  "objective": "increase primary-action hierarchy without changing checkout behavior",
  "selector": "div.checkout-panel button.primary",
  "component_name": "CheckoutPanel",
  "route": "/checkout",
  "interaction_type": "visual",
  "scope_hint": "component",
  "autonomy_class": "bounded_experience_improvement",
  "risk_class": "low",
  "requires_backend": false,
  "requires_auth": false,
  "environment": {
    "browser": "chrome",
    "os": "win32",
    "viewport": "1920x1080"
  },
  "annotation": {
    "coordinates": { "x": 742, "y": 418 },
    "target_identity": "semantic-or-selector-reference"
  }
}
```

The exact schema is open. The important separation is between:

- the observation origin and the original human statement or Hermes finding;
- the proposed objective, which remains a candidate interpretation until admitted;
- observed facts such as route, target, screenshot, and viewport;
- routing hints such as component versus flow;
- autonomy and risk classifications, with the policy version that produced them;
- provenance such as app revision, timestamp, browser, and operating system;
- evidence references that later runs can add without rewriting the original observation.

`scope_hint` and selectors are useful signals, but neither should be treated as authoritative when the repository or rendered app contradicts them. A normalized record should preserve the original values and let triage record any corrected identity.

The lifecycle may include `observed`, `captured`, `triaged`, `proposal_ready`, `admitted_for_work`, `reproduced`, `implementing`, `verified`, `experience_review`, `preview`, `accepted`, `rejected`, and `iterating`. A `delete_annotation` operation should be understood as a projection or cleanup action over this lifecycle, not as proof that the requested change was accepted. A Hermes-originated intent has no annotation badge to delete, but follows the same evidence and admission rules.

The contract should be platform-neutral at its core. Browser records can carry DOM selectors, routes, and browser metadata. A future Flutter adapter can carry widget keys, semantic labels, route names, device/OS metadata, and screenshot or golden-test references while preserving the same intent, evidence, and lifecycle concepts.

## Interfaces and boundaries

The intent layer consumes a user annotation, Hermes observatory finding, regression signal, or approved telemetry event plus the current app context and available screenshot or DOM/semantics evidence. It emits a normalized intent record, immutable provenance for the original observation, and append-only links to later proposal, admission, reproduction, and verification evidence.

It does not choose Storybook versus Playwright, interpret component specifications, implement code, or decide that a preview or change is accepted. Those responsibilities belong to the neighboring routing, safety, verification, Experience Council, and Subject Hermes authority mechanisms.

The record may contain sensitive user or application data. Redaction, access control, retention, and preview-data isolation must be part of the eventual implementation contract, especially when the browser surface can contain healthcare or other regulated information.

## Alternatives and tensions

- **Coordinates versus semantic identity:** coordinates preserve what the person pointed at, while selectors, component names, DOM roles, widget keys, or semantics labels are more durable. The record may need both, with confidence and revision metadata.
- **Screenshot-only versus structured context:** a screenshot is easy to capture but weak for routing and reproducibility; structured context is stronger but can be unavailable or stale.
- **Annotation deletion timing:** deleting the badge after automated verification gives a clean UI, but retaining a resolved or pending badge until Project Hermes admission or merge preserves the feedback trail. Direct user feedback and technical resolution should remain distinguishable.
- **Agent-read metadata versus user-authored metadata:** inferred fields can accelerate triage, but they should be marked as inferred and never overwrite the user's original note.
- **Human versus Hermes origin:** one lifecycle simplifies execution, but the UI must never imply that a Hermes-generated objective was requested or approved by a person.

## Open questions

- What is the authoritative in-house annotation schema, and which legacy VibeA fields require a migration adapter?
- Can the annotation system capture a stable semantic identity in addition to a CSS selector and coordinates?
- How are annotations correlated across the original app, a feature branch, and a preview URL?
- Which evidence must be redacted before an annotation is sent through MCP or attached to a branch?
- What is the common core of the browser and Flutter intent envelopes, and which fields are adapter-specific?
- Which observatory findings may create an intent automatically, and which remain suggestions in the Project Manager backlog?

## Relationships

- [Adaptive Test Scope Routing](agent-assisted-app-testing-scope-routing.md) consumes the intent envelope to choose a verification lane.
- [Cross-Environment Verification and Parity](agent-assisted-app-testing-verification-parity.md) extends the envelope with reproduction and rendering evidence.
- [Preview Verification and Feedback Loop](agent-assisted-app-testing-preview-approval.md) carries the intent into an integrated synthetic and optional user-review surface.
- [Autonomous UI Observatory](agent-assisted-app-testing-autonomous-ui-observatory.md) supplies proactive observations with explicit non-human provenance.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) consumes the intent's change and risk classifications.
