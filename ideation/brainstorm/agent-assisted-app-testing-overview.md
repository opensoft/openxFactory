# Agent-Assisted App Testing Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Establish a platform-neutral, Project Hermes-governed experience loop that turns user annotations, autonomous UI observations, and regressions into specialist design work, layered evidence, agent admission, approved per-profile baselines, and bounded merge enforcement, beginning with browser apps and extending later to Flutter.
Topics: agent-assisted-app-testing, app-development, browser-testing, flutter, subject-hermes, autonomous-experience-management, verification, experience-admission, sdlc-session, chromium-render-manifest, approved-ui-source, os-baselines, visual-diff
Repository context: openxFactory; cross-factory workflow concept with a browser-app realization first and Flutter as a later adapter
Captured: 2026-08-02

## Possible feats

- **Hermes-governed app experience capability** — connect user annotations and proactive UI audits to Project Hermes management, specialist design/implementation, adaptive tests, experience admission, and bounded merge enforcement.

## Motivation

Fast app development loses time at the boundary between someone seeing a problem in a rendered app and an agent changing the code. An annotation can lack the route, component identity, interaction scope, browser, operating system, and viewport needed to reproduce the observation. An agent may choose an overly broad or overly narrow test surface, and a Linux screenshot can disagree with what the engineer saw on Windows or macOS. Automated checks can pass while the user's intended result is still wrong.

Human annotation alone also limits improvement to defects a person notices and has time to manage. The proposed workflow gives Project/Subject Hermes a second intake lane: run bounded UI audits and synthetic journeys, originate evidence-backed improvements, coordinate qualified specialists, and approve routine outcomes inside a versioned autonomy policy. Humans remain available for direct feedback, policy ratification, protected/regulated decisions, and out-of-envelope exceptions rather than every proposal and merge.

## Goals

- Preserve a user observation, Hermes finding, or regression as a durable intent with explicit origin and authority.
- Let Project Hermes proactively inspect approved states and journeys and suggest its own improvements.
- Select the smallest test surface that can reproduce the behavior honestly.
- Separate functional assertions, deterministic visual baselines, and OS/browser parity evidence.
- Detect likely spec and workflow violations before the agent edits code.
- Ground UI suggestions and acceptance in a versioned project UI constitution and experience memory.
- Separate visual, interaction, design-system, accessibility, content, quality, implementation, and approval responsibilities.
- Let the Project Owner admit user-visible behavior while the Project Manager prioritizes, sequences, and manages iteration.
- Give Project Hermes a reachable preview for final synthetic review and users an optional feedback/reopen surface.
- Provide only the v1 SDLC communication needed for observation, proposal, iteration, verification, experience admission, preview, and merge decisions.
- Make canonical visual evidence reproducible through a pinned Chromium render manifest.
- Keep approved runtime snapshots in the repository as the visual reference for named OS/browser profiles, with explicit migration history.
- Preserve raw pixel-diff evidence while independent specialists classify differences and prepare candidate baseline updates for Project Hermes admission.
- Allow routine UI changes to complete through agent authorities inside a conjunctive autonomy envelope, with humans reserved for exceptions.
- Keep Figma optional as design-intent context or a projection target rather than a runtime pixel dependency.
- Keep the intent, evidence, authority, and lifecycle concepts reusable for Flutter later.

## Non-goals

- Guarantee pixel-identical screenshots across operating systems, browsers, fonts, and devices.
- Automatically merge every machine-verified change without Project Hermes admission, Merge Master authority, and external enforcement.
- Treat an LLM vision judgment or a screenshot diff as a replacement for functional tests.
- Let the ordinary UI lane modify its own constitution, protected-surface list, thresholds, masks, reviewer qualifications, or autonomy policy.
- Remove humans or accountable professionals from ratification, protected/regulated decisions, and structurally human-gated enforcement.
- Define the complete annotation client, MCP, Storybook, Playwright, Loki, deployment, or Flutter implementation contract in this brainstorm.
- Certify healthcare, regulatory, accessibility, or legal compliance solely through a component spec.
- Design the Flutter adapter now; this packet only reserves the common seams needed to add it later.

## What the system delivers

The intended browser workflow delivers:

1. A common intent containing origin, objective, autonomy/risk class, target identity, route, interaction type, scope hint, backend/auth needs, browser/OS/viewport metadata, and supporting evidence.
2. A Project UI constitution containing personas, critical journeys, design and interaction principles, protected surfaces, and decision memory.
3. An autonomous UI observatory that runs bounded Storybook, Playwright, accessibility, visual, responsive, and performance campaigns and produces evidence-backed findings.
4. A logged scope decision selecting a component story, composite story, synthetic journey, or end-to-end flow, with confidence and fallback conditions.
5. A pre-edit spec verdict that blocks, routes, or parks unsafe or unknown changes and records any authority-bound exception.
6. A risk-routed specialist team with explicit separation among proposer, implementer, reviewers, Project Owner, Project Manager, and Merge Master.
7. A verification bundle containing functional results, Loki/container baseline evidence identified by a render-manifest hash, optional matching-environment captures, and structural parity findings.
8. An Experience Council packet containing independent visual, interaction, accessibility, design-system, and browser-quality findings plus the Project Owner verdict and Project Manager disposition.
9. A narrow bidirectional SDLC session stream for observations, proposals, progress, tests, experience admission, preview, iteration, and merge decisions.
10. An isolated preview tied to the exact revision where Hermes can run final synthetic journeys and policy-selected users can inspect, reject, or annotate the result.
11. An approved UI baseline registry containing per-profile snapshots, state/fixture identity, raw diff evidence, and candidate migration history.
12. A UI autonomy decision proving why the change may proceed through agent authorities or must route, block, or park.

The system should distinguish these outcomes:

```text
observed ≠ admitted for work ≠ machine verified ≠ experience admitted ≠ merge admitted ≠ merged
```

## System model

```text
[User annotation] ───────────────┐
[Hermes UI observatory] ─────────┤
[Regression/approved telemetry] ─┤
                                 ▼
                 [Intent envelope / session bridge]
                                 │
                 [Project/Subject Hermes]
          UI constitution + PO + PM + experience memory
          │
          ├── [Scope router]
          │       ├── component/panel → [Storybook reproduction + play]
          │       └── journey/flow/backend/auth → [Playwright]
          │
          ├── [Spec admission]
          │       └── violation/unknown → [route, block, or park]
          │
          └── [Separated UI/UX specialists + implementation]
                          │
                          ▼
              [Functional/a11y/journey verification]
                          │
                          ▼
              [Chromium render manifest]
                          │
                          ▼
              [Loki deterministic baseline]
                          │
                          ├── optional [reachable engineer-environment capture]
                          │                    └── structural comparison
                          ▼
                  [Raw diff + review derivatives]
                          │
                          ▼
             [Experience Admission Council]
            specialist findings + PO verdict + PM disposition
                          ▼
                [UI autonomy-envelope check]
                    │                 │
              inside envelope   outside envelope
                    │                 └── route/block/park
                    ▼
           [Merge Council + Merge Master]
                          │
                          ▼
                 [Git/CI enforcement]
                          │
                          ▼
              [Post-merge audit + experience memory]
```

The exact ordering between scope routing, design admission, spec admission, implementation, and preview may change as the design becomes concrete. The authority boundary should not: Project/Subject Hermes owns project purpose, Project Owner acceptance, and Project Manager coordination; Omnigent specialists execute and review; Merge Council/Merge Master own readiness and enforcement; humans or professionals hold only the exception gates declared by policy.

## Cluster map

- [Synthesis: Execution and Evidence](agent-assisted-app-testing-synthesis-execution-evidence.md) — joins annotation identity, scope routing, and layered verification into a replayable evidence path.
- [Synthesis: Hermes Autonomy and Human Exception Control](agent-assisted-app-testing-synthesis-human-control-and-safety.md) — joins pre-edit constraints, Project Hermes admission, protected exceptions, and Merge Master enforcement.
- [Synthesis: Autonomous Experience Management](agent-assisted-app-testing-synthesis-autonomous-experience-management.md) — joins the project UI constitution, proactive observatory, separated specialists, Experience Council, and autonomy envelope.

## How it fits

This is a neutral xFactory workflow concept rather than a change to a single factory's app. An in-house annotation client and MCP/session bridge are proposed input and lifecycle adapters. Storybook, Playwright, Loki, accessibility/performance tools, and preview providers are browser-specific execution adapters. Repository snapshots are the proposed runtime visual authority; the Project UI constitution, component specs, and tokens carry experience intent and constraints; Figma is optional context or projection.

The three Hermes layers compose the policy: Domain Hermes supplies reusable UI/UX practice and reviewer qualifications, Tenant Hermes supplies local brand/provider/privacy constraints, and Project/Subject Hermes owns project personas, journeys, priorities, decision memory, and in-envelope product admission. Omnigent specialists and browser workers execute bounded work. The intent, evidence, and authority model should remain independent of browser tooling so Flutter can later provide widget, golden, device, and build-preview adapters.

The idea also fits the existing xFactory ideation lifecycle: it is deliberately non-normative material in `ideation/brainstorm/`. If repeated use proves the workflow valuable, selected fragments can be organized into staging and then promoted through an OpenSpec proposal; this packet does not ratify a contract or authorize implementation.

## Key decisions and open questions

The load-bearing design direction is to preserve origin, ground decisions in project intent, route by scope, separate specialists and authorities, verify in layers, let Project Hermes admit routine work, and reserve humans for exceptions. The largest unresolved choices are:

- the canonical in-house annotation, observatory finding, intent, and evidence schemas;
- how stable target identity is maintained across local, branch, preview, and Flutter surfaces;
- whether annotation cleanup happens at automated verification, Project Hermes admission, or merge;
- how a matching OS/browser environment is provisioned and governed;
- which structural parity checks are trustworthy enough to block versus advise;
- how specs are discovered, owned, versioned, and overridden;
- the first approved Chromium version, container digest, font set, and baseline migration process;
- which OS/browser profiles are supported and blocking, and how their approved snapshots are stored and kept current;
- which raw-diff thresholds, dynamic masks, and reviewer derivatives are acceptable without hiding regressions;
- the minimum independent specialist roster and council evidence for each UI change class;
- which bounded improvements enter the first Project Hermes autonomy envelope;
- how the agent Project Owner is grounded strongly enough to decide user-visible product value;
- which constitution, reviewer, threshold, mask, profile, and autonomy changes remain outside the ordinary UI lane;
- which human/professional and Git/CI gates remain structurally enforced;
- whether Figma MCP adds enough design context to justify an optional integration;
- the v1 session transport and merge-authority integration;
- the first Flutter mapping for component, panel, flow, visual, and preview scopes.

## Document map

### Atomic mechanisms

- [Annotation-Centered Test Intent](agent-assisted-app-testing-intent.md) — user/Hermes origin provenance and the cross-platform intent envelope.
- [Adaptive Test Scope Routing](agent-assisted-app-testing-scope-routing.md) — Storybook/Playwright triage and future adapter routing.
- [Cross-Environment Verification and Parity](agent-assisted-app-testing-verification-parity.md) — functional, deterministic visual, and environment-aware evidence.
- [Spec-Aware Change Safety](agent-assisted-app-testing-spec-safety.md) — pre-edit constraint checks and explicit overrides.
- [Preview Verification and Feedback Loop](agent-assisted-app-testing-preview-approval.md) — integrated synthetic verification and optional user feedback before merge.
- [V1 SDLC Session Protocol](agent-assisted-app-testing-v1-sdlc-session.md) — minimum bidirectional lifecycle messages for observe, propose, iterate, test, admit, preview, and merge.
- [Chromium Render Manifest](agent-assisted-app-testing-chromium-render-manifest.md) — immutable-by-identity canonical Chromium/Loki rendering environment.
- [Approved UI Source of Truth](agent-assisted-app-testing-approved-ui-source.md) — repo-first authority split for runtime pixels, project experience intent, specialist interpretation, and admission.
- [OS Baseline Lifecycle](agent-assisted-app-testing-os-baseline-lifecycle.md) — per-OS/profile snapshot identity, migration triggers, and candidate update flow.
- [Visual Diff Review](agent-assisted-app-testing-visual-diff-review.md) — raw deterministic comparison and declared reviewer derivatives.
- [Hermes Designer Visual Review](agent-assisted-app-testing-hermes-visual-review.md) — independent visual-specialist classification and candidate baseline findings.
- [Project UI Constitution and Experience Memory](agent-assisted-app-testing-ui-constitution.md) — project personas, journeys, principles, protected surfaces, and decision history.
- [Autonomous UI Observatory](agent-assisted-app-testing-autonomous-ui-observatory.md) — proactive browser campaigns and Hermes-originated improvement intents.
- [UI Specialist Team and Separation of Duties](agent-assisted-app-testing-ui-specialist-separation.md) — risk-routed expert roles and independence rules.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) — specialist findings, Project Owner verdict, and Project Manager disposition.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) — conjunctive policy for agent-only management and protected exception routing.

### Relationship syntheses

- [Synthesis: Execution and Evidence](agent-assisted-app-testing-synthesis-execution-evidence.md) — how intent becomes reproducible evidence.
- [Synthesis: Hermes Autonomy and Human Exception Control](agent-assisted-app-testing-synthesis-human-control-and-safety.md) — how constraints, Project Hermes admission, Merge Master, and protected gates bound autonomy.
- [Synthesis: Autonomous Experience Management](agent-assisted-app-testing-synthesis-autonomous-experience-management.md) — how proactive observation, project intent, specialists, council review, and auto-clear form a durable loop.
