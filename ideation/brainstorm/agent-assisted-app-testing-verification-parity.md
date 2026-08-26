# Cross-Environment Verification and Parity — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Combine functional reproduction, deterministic visual baselines, and optional engineer-environment comparison so rendering differences inform review without pretending that every operating system produces identical pixels.
Topics: agent-assisted-app-testing, verification, visual-regression, loki, playwright, screenshot-parity, structural-comparison
Repository context: openxFactory; browser verification uses Storybook, Playwright, Loki, and reachable browser environments, with a future Flutter golden/device adapter
Captured: 2026-08-02

## Possible feats

- **Verification evidence bundle** — collect functional results, screenshots, runner versions, environment metadata, and diff classifications under one intent ID.
- **Structural parity comparator** — compare engineer and deterministic-runner captures by layout and semantic intent while keeping exact pixel baselines available for CI.

## Focus

The engineer may annotate on Windows Chrome while the agent verifies in a Linux container. Font rasterization, anti-aliasing, native controls, and browser versions can produce different pixels even when the implementation is correct.

This document isolates a layered verification model that distinguishes behavioral correctness, deterministic visual regression, and environment-specific rendering evidence.

## Proposed model

Verification can proceed in layers:

1. Reproduce the original state in the selected Storybook or Playwright lane.
2. Run functional assertions for the requested interaction or flow.
3. Capture a deterministic screenshot in a pinned Loki/container environment for CI baseline comparison.
4. When the annotation includes an engineer OS, browser, and viewport, run an optional secondary capture in a reachable matching environment.
5. Compare the captures structurally and route any meaningful disagreement to the Experience Council or configured authority policy.

The deterministic lane remains suitable for exact or thresholded baseline gating. The cross-environment lane should ask questions such as:

- Does the target exist and occupy the expected relationship to nearby content?
- Is its size, alignment, and spacing within an intended range?
- Does its semantic role, accessible name, enabled state, and interaction affordance remain correct?
- Is the visual treatment in the expected color, emphasis, and hierarchy family?

Those checks can combine DOM or accessibility-tree facts, geometry, token values, and vision-model judgments. A structural comparison is not a license to ignore a real functional failure, and an LLM vision result should not silently replace deterministic assertions.

The metadata describing `os`, browser channel, viewport, device scale factor, and app revision must travel with every capture. Metadata alone cannot launch a remote Windows or macOS browser; a matching environment must be available through a worker, remote Playwright endpoint, or other explicitly governed execution surface. If it is unavailable, the system should report that parity evidence is missing rather than imply that Linux is equivalent.

The eventual Flutter adapter can retain the same evidence concepts while selecting widget tests, golden tests, or device/integration captures. Platform-specific rendering baselines and device metadata should remain adapter-owned rather than forcing browser assumptions into the common contract.

## Interfaces and boundaries

The verifier consumes a route plan, the code revision under test, the original intent, and environment/toolchain declarations. It emits:

- functional pass/fail results;
- screenshot and baseline references;
- environment and runner versions;
- exact diff or structural comparison results;
- missing-environment, flaky, needs-authority, or protected-surface classifications.

It does not decide whether the requested or Hermes-suggested change is allowed by a component specification, and it does not imply Project Owner acceptance. The evidence should be append-only and tied to the intent and revision so a later preview cannot be confused with the original main-branch observation.

## Alternatives and tensions

- **One canonical Linux baseline versus per-OS baselines:** one baseline simplifies CI and catches code-level drift; per-OS baselines represent native rendering more faithfully but increase maintenance and review cost.
- **Pixel diff versus structural comparison:** pixel diff is precise and deterministic; structural comparison is more tolerant of rasterization but can miss subtle visual regressions or encode model bias.
- **Local matching environment versus remote worker:** local capture is closest to the engineer's observation; a managed remote endpoint is easier to audit and reproduce across teams.
- **Full viewport versus annotation crop:** a crop focuses on the requested target; a full viewport catches layout shifts and workflow regressions outside the annotation.

## Open questions

- Which visual changes are blocking, advisory, Experience Council reviewed, or protected by a human/professional gate?
- What structural representation should be compared first: DOM/accessibility tree, geometry, design tokens, or vision features?
- How are browser version, font set, device scale factor, and OS image pinned and reported?
- Is the matching-environment lane required for certain targets or merely optional evidence?
- What is the first Flutter parity surface: Linux golden tests, platform-specific goldens, or device screenshots?

## Relationships

- [Adaptive Test Scope Routing](agent-assisted-app-testing-scope-routing.md) selects the runner and reproduction surface.
- [Annotation-Centered Test Intent](agent-assisted-app-testing-intent.md) supplies the original environment and target provenance.
- [Preview Verification and Feedback Loop](agent-assisted-app-testing-preview-approval.md) separates automated evidence from Project Hermes experience admission and optional user feedback.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) consumes parity disagreements and retains specialist findings.
- [Autonomous UI Observatory](agent-assisted-app-testing-autonomous-ui-observatory.md) uses the same evidence lanes for proactive campaigns.
