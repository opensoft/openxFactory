# Synthesis: Execution and Evidence — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Combining origin-aware intent, adaptive routing, and layered verification creates a traceable path from a user annotation, Hermes observation, or regression to evidence about the implemented change.
Topics: agent-assisted-app-testing, execution-evidence, intent-routing, verification, synthesis
Repository context: openxFactory; cross-platform workflow synthesis with browser tooling as the first concrete realization
Captured: 2026-08-02

## Possible feats

- **Intent-to-evidence execution contract** — connect annotation identity, route decisions, runner invocations, and verification artifacts into one replayable lineage.
- **Runner adapter manifest** — advertise which component, panel, flow, visual, and parity checks each app platform can honestly execute.

## Members and their joints

Atomic members: [Annotation-Centered Test Intent](agent-assisted-app-testing-intent.md), [Adaptive Test Scope Routing](agent-assisted-app-testing-scope-routing.md), [Cross-Environment Verification and Parity](agent-assisted-app-testing-verification-parity.md), [V1 SDLC Session Protocol](agent-assisted-app-testing-v1-sdlc-session.md), [Chromium Render Manifest](agent-assisted-app-testing-chromium-render-manifest.md), [OS Baseline Lifecycle](agent-assisted-app-testing-os-baseline-lifecycle.md), and [Visual Diff Review](agent-assisted-app-testing-visual-diff-review.md).

```text
user annotation | Hermes observation | regression
      │ normalized intent + origin + provenance
      ▼
scope/routing decision ── rationale + confidence
      │
      ▼
reproduction + functional checks
      │
      ▼
deterministic baseline ── optional matching-environment evidence
      │
      ▼
evidence bundle tied to intent and revision
```

### Identity joins the steps

The intent ID, source revision, origin, target identity, and environment metadata must survive each handoff. Without that shared identity, a screenshot from a later preview or a failed flow can be mistaken for evidence about the original observation, and a Hermes suggestion can be misrepresented as a user request. The intent document provides the durable origin; the verifier adds evidence rather than rewriting it.

### Routing controls execution cost and honesty

The routing decision is a control point between a cheap isolated reproduction and an expensive full flow. It should use the intent's scope hint as a signal, repository evidence as a check, and a logged rationale as an audit surface. If the selected runner cannot represent the required backend, auth, or navigation honestly, the route should escalate instead of producing a green mock.

### Verification layers make different claims

Storybook or Playwright functional assertions establish behavior in the selected state. Loki-style deterministic capture establishes rendering drift against a pinned baseline. A matching engineer environment can add evidence about OS/browser-specific rendering, but structural comparison is a different claim from exact pixel identity. The evidence bundle should retain the distinction.

### The session protocol closes the execution loop

The [V1 SDLC Session Protocol](agent-assisted-app-testing-v1-sdlc-session.md) turns the evidence path into a usable development loop: the agent can present a proposal, report implementation and verification status, publish a preview, receive iteration feedback, and request a merge without inventing an implicit conversational state. The [Chromium Render Manifest](agent-assisted-app-testing-chromium-render-manifest.md) gives visual evidence a stable environment identity.

### Baselines join evidence without becoming mutable test output

The [OS Baseline Lifecycle](agent-assisted-app-testing-os-baseline-lifecycle.md) adds a second identity to the evidence path: not only which application revision was tested, but which OS/browser profile made the pixels meaningful. A canonical Loki profile can provide a deterministic Linux gate while supported OS profiles carry their own approved references when native rendering is part of acceptance.

The [Visual Diff Review](agent-assisted-app-testing-visual-diff-review.md) keeps the raw comparison authoritative and treats preprocessing as a declared derivative for explanation. This lets a reviewer or agent inspect heatmaps, crops, geometry, and semantic summaries without allowing a resized or enhanced image to replace the reproducible pixel arithmetic.

## Emergent behavior

Together, these mechanisms allow an agent to move from “a user pointed at this rendered thing” or “Hermes found this experience gap” to “this exact revision was reproduced in the smallest honest test surface and checked with named evidence.” The same lineage can later route a Flutter widget or flow to a different adapter without changing the common intent, evidence, and admission vocabulary.

## Tensions to hold

- More metadata improves routing and parity but increases capture complexity and privacy exposure.
- Automatic routing reduces latency but may hide an incorrect scope classification unless rationale and confidence are visible.
- Exact baselines are useful for CI but can overreact to platform rendering; structural comparison is tolerant but less deterministic.
- Per-OS approved references improve user-visible fidelity but multiply capture, migration, and review work.
- A clean annotation UI conflicts with retaining enough unresolved history for audit and iteration.

## Recombination opportunities

- Join with [Preview Verification and Feedback Loop](agent-assisted-app-testing-preview-approval.md) to make automated evidence a handoff to integrated synthetic missions and optional user testing rather than the end of the workflow.
- Join with [Spec-Aware Change Safety](agent-assisted-app-testing-spec-safety.md) to place constraint admission before the route and implementation steps.
- Reuse the intent and evidence contract for Flutter, native desktop, or other rendered app adapters.
- Use the [V1 SDLC Session Protocol](agent-assisted-app-testing-v1-sdlc-session.md) as the browser-facing control surface while keeping repository and runner mechanics behind adapters.
- Combine with [Synthesis: Autonomous Experience Management](agent-assisted-app-testing-synthesis-autonomous-experience-management.md) so proactive audits consume the same route plans and evidence contracts as annotated repairs.

## Open questions

- Which artifacts are authoritative when functional, pixel, and structural checks disagree?
- Is the route plan part of the durable product record or only an execution trace?
- What minimum evidence is required before an agent may publish a preview?
- How can flaky or unavailable environments be separated from genuine product failures?
