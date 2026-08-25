# Adaptive Test Scope Routing — Brainstorm

Status: brainstorm
Kind: process
Summary: Route a user- or Hermes-originated app-change intent to an isolated component, composite story, synthetic journey, or end-to-end flow using explicit signals, logged rationale, and an ambiguity fallback.
Topics: agent-assisted-app-testing, scope-routing, storybook, playwright, test-adapters, routing, flutter
Repository context: openxFactory; browser routing is the first adapter and Flutter widget/golden/integration routing is a later extension
Captured: 2026-08-02

## Possible feats

- **Scope routing decision record** — emit the selected runner, target, setup requirements, confidence, rationale, and fallback path for every intent.
- **Runner adapter registry** — describe browser and future Flutter runners through one routing interface while keeping their mechanics separate.

## Focus

A user annotation can describe a single control, a panel composed of several components, or a workflow that crosses routes and backend boundaries. Sending every annotation to a full end-to-end suite is slow and noisy; forcing every annotation into Storybook can produce a misleading mock.

This document isolates the triage decision that selects the smallest verification surface capable of reproducing the intent honestly.

## Proposed model

The router reads the normalized intent, its origin and objective, repository topology, available stories or test targets, project journey inventory, and environment requirements. It produces a routing record rather than an opaque tool call:

```text
intent → scope classification → runner + target + setup → rationale + confidence
                                      └──────────────→ fallback or escalation
```

An initial browser decision table could use these signals:

| Route | Strong signals | Candidate verification surface |
| --- | --- | --- |
| Component | `scope_hint=component`, leaf target, no backend or auth, visual/click interaction | Storybook story and `play` function, then component visual capture |
| Panel | `scope_hint=panel`, bounded composite, state mockable without backend | Composite Storybook story with args, decorators, and mocked state |
| Flow | `scope_hint=flow`, backend or auth required, route transition, or multi-step interaction | Playwright end-to-end scenario against a controlled environment |
| Synthetic journey | Hermes audit objective names a persona, critical journey, or cross-state quality question | Playwright mission using pinned persona, fixture, success criteria, and budget |
| Ambiguous | Conflicting hints, missing target, or setup that cannot be represented honestly | Ask for a targeted clarification or run a lower-confidence discovery lane before implementation |

The router can use deterministic rules for admission and an LLM for interpretation and rationale. A model-generated rationale should cite the signals that led to the decision, for example:

```text
Intent #123
  scope_hint: component
  interaction_type: visual
  requires_backend: false
  decision: Storybook / Button.stories.tsx
  rationale: leaf control, no route or API dependency
  confidence: high
```

The proposed heuristic of escalating when mock wiring becomes disproportionately large, such as more than roughly 30 lines, is useful as an exploration signal but should not become a hidden correctness rule. The eventual router should detect missing behavior and dishonest mocks, not just count lines.

The core scope vocabulary can map to future Flutter adapters. `component` may select a widget test or golden test, `panel` a composed widget test, and `flow` an integration or device test. The mapping is intentionally deferred; the common contract is the scope and evidence shape, not the tool names.

## Interfaces and boundaries

The router consumes the intent envelope and repository/test inventory. It emits a versioned route plan containing:

- selected adapter and runner;
- source target, story, route, or test entrypoint;
- required mocks, fixtures, backend, and authentication;
- environment and viewport/device requirements;
- rationale, confidence, and unresolved assumptions;
- fallback or escalation conditions.

It does not implement the fix, certify visual parity, or authorize a merge. Project/Subject Hermes may override the route inside its authority envelope, but the override should carry a reason and remain visible in the evidence chain. An out-of-envelope override follows the configured park or escalation path rather than defaulting to a user interruption.

## Alternatives and tensions

- **Storybook first versus Playwright first:** Storybook is fast and isolated; Playwright is more honest when routing, auth, or real integration matters.
- **Deterministic rules versus LLM classification:** rules are auditable but incomplete; an LLM understands prose and topology but can be inconsistent. A hybrid can let rules constrain model choices.
- **Automatic ambiguity fallback versus authority clarification:** automatic discovery keeps momentum but can waste time; Subject Hermes can resolve project intent when its constitution is sufficient, while genuinely missing product authority must park.
- **One universal scope taxonomy versus platform-specific taxonomies:** a common vocabulary improves recombination, while platform adapters need room for widget, device, browser, and native-system distinctions.

## Open questions

- Which signals are mandatory before the router is allowed to select Storybook or a full flow?
- How is a component mapped to its story when names, selectors, or repository boundaries are inconsistent?
- What is the honest fallback when backend behavior is needed but no stable test fixture exists?
- Should the router be allowed to change scope after a failed reproduction, or must Project Hermes admit a revised route plan?
- Which Flutter test surfaces will be the first equivalents for component, panel, and flow?

## Relationships

- [Annotation-Centered Test Intent](agent-assisted-app-testing-intent.md) supplies the routing signals and provenance.
- [Cross-Environment Verification and Parity](agent-assisted-app-testing-verification-parity.md) executes the selected lane and records its evidence.
- [Synthesis: Execution and Evidence](agent-assisted-app-testing-synthesis-execution-evidence.md) describes how routing joins capture and verification.
- [Autonomous UI Observatory](agent-assisted-app-testing-autonomous-ui-observatory.md) supplies synthetic-journey and proactive audit route requests.
