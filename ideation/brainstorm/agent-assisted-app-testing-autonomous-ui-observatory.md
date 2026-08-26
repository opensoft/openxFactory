# Autonomous UI Observatory — Brainstorm

Status: brainstorm
Kind: process
Summary: Let Project/Subject Hermes originate evidence-backed UI improvement intents through bounded browser audits, synthetic journeys, regression triggers, and approved telemetry rather than waiting only for human annotations.
Topics: agent-assisted-app-testing, autonomous-ui-observatory, subject-hermes, synthetic-journeys, proactive-testing, improvement-generation
Repository context: openxFactory; Hermes-controlled browser observation with Omnigent test execution and a later Flutter/device adapter
Captured: 2026-08-02

## Possible feats

- **Autonomous UI audit campaign** — schedule or trigger bounded Storybook, Playwright, accessibility, visual, responsive, and performance inspections from Project Hermes.
- **Hermes-originated improvement intent** — turn an observed experience gap into the same traceable intent and evidence lifecycle used by a user annotation.

## Focus

The current annotation workflow is reactive: a person must notice and mark a problem. To remove the human from routine management, Hermes needs a second intake lane that actively evaluates the project against its approved UI constitution, supported state inventory, and quality policy.

The observatory is a control capability of Project/Subject Hermes. Hermes chooses the purpose, campaign, budget, and stop conditions. Browser and analysis workers execute the tests through Omnigent or CI and return evidence; this preserves the existing Hermes control and execution boundary.

## Proposed model

```text
scheduled trigger | post-change trigger | regression | approved telemetry
                              │
                              ▼
                Project Hermes audit mandate
                    purpose + scope + budget
                              │
                              ▼
                 bounded test campaign plan
                              │
            ┌─────────────────┼──────────────────┐
            ▼                 ▼                  ▼
      Storybook states   Playwright journeys   visual/a11y/perf tools
            │                 │                  │
            └─────────────────┼──────────────────┘
                              ▼
                    observation records
                              │
                              ▼
               prioritize, dismiss, or create
                  Hermes-originated intent
```

Candidate campaigns include:

- story and component-state inventory, including missing loading, empty, error, disabled, and overflow states;
- synthetic user journeys tied to project personas and explicit success criteria;
- responsive layout checks at supported breakpoints and long-text/localization stress states;
- keyboard navigation, focus order, focus visibility, accessible names, roles, and automated accessibility checks;
- canonical Loki comparison and supported OS/browser parity checks;
- design-token, spacing, typography, component-usage, and interaction-pattern consistency;
- console errors, failed requests, broken links, layout shifts, and recovery from interrupted or invalid states;
- approved performance and interaction-latency budgets;
- task-friction signals such as dead ends, unnecessary steps, unclear action hierarchy, and failed recovery paths.

### Observation and intent identity

An observatory finding is evidence, not automatically a work order. A candidate record should include:

```yaml
observation:
  id: uiobs-01J...
  origin: hermes-ui-audit
  trigger: post-merge
  project_ref: project-alfa
  constitution_version: 3
  campaign_ref: responsive-critical-journeys-v1
  surface: checkout/payment
  finding_kind: focus-loss-after-validation
  evidence_refs: [artifact://trace.zip, artifact://a11y.json]
  affected_personas: [keyboard-user]
  severity: high
  confidence: 0.92
  suggested_action: create-improvement-intent
```

When admitted for consideration, the observation creates an ordinary intent with `origin: hermes_ui_audit`, the triggering evidence, a proposed objective, autonomy/risk classification, and lineage back to the campaign. User annotations, regressions, and Hermes observations then share one implementation and verification path.

### Prioritization and batching

The Project Manager should rank admitted observations using declared factors such as user impact, journey criticality, accessibility severity, recurrence, confidence, reach, estimated effort, regression risk, and current project capacity. Related observations should be batched when one coherent design change can resolve them without hiding separate evidence.

The observatory should have route, state, time, spend, model-call, and finding-volume limits. An audit that encounters unbounded navigation, unstable data, or an unknown protected surface should stop or narrow rather than crawl indefinitely.

## Interfaces and boundaries

The observatory consumes the UI constitution, route/story inventory, supported render profiles, test fixtures, current revision, autonomy policy, and approved telemetry. It emits campaign records, test evidence, observations, and candidate intents.

It does not approve a design, mutate code, update baselines, change policy, or merge. It may dismiss clear duplicates or known approved variances under policy, but the dismissal remains traceable to the evidence and rule used.

Production crawling and telemetry are optional inputs with separate authorization, privacy, retention, and credential requirements. V1 can operate entirely on controlled stories, fixtures, previews, and synthetic journeys.

## Alternatives and tensions

- **Scheduled sweeps:** find drift without waiting for code changes, but consume steady resources and can repeat known noise.
- **Post-change audits:** are efficient and causally clear, but miss longstanding design debt.
- **Synthetic journeys:** are reproducible, but may optimize for scripted behavior rather than actual users.
- **Telemetry-driven suggestions:** reflect real usage, but introduce privacy, representativeness, and causal-inference concerns.
- **Automatic implementation of every finding:** maximizes activity, but creates churn; Hermes should first decide whether the observation deserves work.

## Open questions

- Which campaigns run on every change, nightly, weekly, or only by Project Manager request?
- What observation score is sufficient to create an intent automatically?
- How should duplicate findings across states, routes, and OS profiles be clustered without losing provenance?
- Which task-friction metrics are stable enough to compare across releases?
- What is the first Flutter observatory surface: widget-state inventory, golden sweeps, emulator journeys, or device telemetry?

## Relationships

- [Hermes Control and Execution Boundary](hermes-recursive-subject-establishment-hermes-control-and-execution-boundary.md) supplies the pattern in which Subject Hermes owns purpose and bounded workers execute tool-bearing tests.
- [Project UI Constitution and Experience Memory](agent-assisted-app-testing-ui-constitution.md) supplies personas, journeys, and quality objectives.
- [Annotation-Centered Test Intent](agent-assisted-app-testing-intent.md) normalizes observatory findings into the common work lifecycle.
- [Adaptive Test Scope Routing](agent-assisted-app-testing-scope-routing.md) selects honest execution surfaces for audit and repair.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) determines which findings may progress without human management.
- [Synthesis: Autonomous Experience Management](agent-assisted-app-testing-synthesis-autonomous-experience-management.md) connects observation to design, review, admission, and learning.
