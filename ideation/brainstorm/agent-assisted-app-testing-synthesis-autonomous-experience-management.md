# Synthesis: Autonomous Experience Management — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A project UI constitution, proactive observatory, separated specialist team, experience council, and bounded autonomy policy let Subject Hermes manage routine UI improvement from discovery through admission without a human checkpoint on every change.
Topics: agent-assisted-app-testing, autonomous-experience-management, subject-hermes, proactive-testing, experience-admission, synthesis
Repository context: openxFactory; Project Hermes management loop with Omnigent UI execution and Merge Master enforcement
Captured: 2026-08-02

## Possible feats

- **Autonomous experience-management loop** — let Project Hermes observe, prioritize, commission, test, admit, merge, and learn from routine UI improvements under a versioned authority envelope.
- **Project UI health program** — combine scheduled campaigns, synthetic journeys, council evidence, and decision memory into a durable improvement backlog and outcome history.

## Members and their joints

Atomic members: [Project UI Constitution and Experience Memory](agent-assisted-app-testing-ui-constitution.md), [Autonomous UI Observatory](agent-assisted-app-testing-autonomous-ui-observatory.md), [UI Specialist Team and Separation of Duties](agent-assisted-app-testing-ui-specialist-separation.md), [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md), and [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md).

```text
user annotation ───────────────┐
Hermes observatory finding ────┤
regression / approved telemetry┤
                               ▼
                    Project/Subject Hermes
              constitution + PO + PM + memory
                               │
                               ▼
                  separated UI specialist team
                               │
                               ▼
                  implementation + test evidence
                               │
                               ▼
                  Experience Admission Council
                               │
                               ▼
                    UI autonomy-envelope check
                       │                 │
                 inside envelope   outside envelope
                       │                 │
                       ▼                 ▼
               Merge Council/Master   route/block/park
                       │
                       ▼
                merge + monitor + memory
```

### Intent joins reactive and proactive work

The observatory creates evidence-backed observations, while annotations preserve direct user input. Both become common intents with explicit origin, objective, risk, and autonomy metadata. This prevents Hermes-generated work from bypassing the same specs, tests, lineage, and admission controls used for a requested repair.

### Constitution grounds suggestion and judgment

The UI constitution tells the observatory what journeys and qualities to inspect and tells specialists what “better” means for the project. Runtime baselines still establish approved pixels; the constitution supplies design intent. Experience memory links decisions and outcomes without allowing repeated model preference to become policy automatically.

### Subject Hermes manages; Omnigent executes

Project/Subject Hermes owns purpose, Project Owner acceptance, Project Manager sequencing, active priorities, and the final in-envelope decision. UI/UX, coding, browser, and analysis agents remain bounded Omnigent workers. Hermes can therefore “run its own tests” as the controlling authority while tool-bearing workers execute reproducible campaigns under ordinary grants and audit.

### Separation makes agent approval credible

The specialist roster prevents one agent from proposing, implementing, reviewing, and approving its own change. The Experience Council preserves unlike findings rather than reducing them to a simple vote. The Project Manager coordinates fixes and capacity; the Project Owner owns user-visible acceptance; the Merge Council and Merge Master retain engineering readiness and enforcement roles.

### The envelope removes routine human management

The autonomy envelope is the bridge between safety and speed. Regression repairs and bounded experience improvements may proceed entirely through agent authorities when every condition passes. Protected surfaces, policy changes, unresolved product meaning, authority conflicts, and out-of-envelope enforcement park at their existing gates. Humans configure and ratify the boundary; they do not manage each ordinary iteration.

### Feedback improves memory without self-ratifying policy

Post-merge audits and approved telemetry can show whether a change resolved the original observation or introduced new friction. Hermes stores that evidence and may suggest constitution, roster, or policy changes through a separate path. It must not use its own admission history to silently relax thresholds or broaden autonomy.

## Emergent behavior

Together, these mechanisms turn the browser tooling from an annotation-driven repair assistant into a continuously operating project experience function. Subject Hermes can discover design debt, choose useful work, commission qualified agents, demand independent evidence, approve routine outcomes, and maintain project-specific experience memory without waiting for a human manager at each step.

## Tensions to hold

- More proactive testing finds more opportunities but can create design churn and model-generated busywork.
- Rich project memory improves consistency but can entrench old decisions unless the constitution has an explicit challenge path.
- Strong specialist separation improves trust but increases cost and latency for small changes.
- Synthetic journeys are reproducible but may not represent real user needs without carefully governed telemetry or periodic product review.
- A broad autonomy envelope accelerates improvement but increases the consequence of stale intent, tests, or reviewer calibration.

## Recombination opportunities

- Combine with [Synthesis: Execution and Evidence](agent-assisted-app-testing-synthesis-execution-evidence.md) to reuse route plans, render manifests, raw diffs, and evidence lineage.
- Combine with [Synthesis: Hermes Autonomy and Human Exception Control](agent-assisted-app-testing-synthesis-human-control-and-safety.md) to route out-of-envelope conditions into the existing safety and merge authority braid.
- Reuse the constitution, observatory, specialist, and admission concepts for Flutter widget, golden, emulator, device, and accessibility adapters.
- Connect approved usage telemetry later without making production observation a prerequisite for v1.

## Open questions

- Which two or three proactive campaigns prove value without producing an unmanageable finding backlog?
- What is the minimum independent council for a bounded improvement in v1?
- How is an agent Project Owner grounded strongly enough to decide user-visible product value?
- Which UI constitution changes can be approved by Project Hermes and which require ratification outside the autonomous lane?
- What evidence proves that autonomous UI changes improve outcomes rather than merely creating visually consistent churn?
