# Staged: Semantic Health Sweep (Agentic Pass)

Status: staged
Kind: architecture
Repository context: openxFactory
Source: [doc-health-pipeline brainstorm](../../brainstorm/doc-health-pipeline.md)
Target capability: extends the planned `doc-health` capability (delta: ADDED
requirements for the agentic pass) — deliberately a SEPARATE change from the
deterministic run: different mechanism (LLM vs grep), different failure modes,
different governance questions.

## Claims

1. An agent sweep finds what grep cannot: untagged normative prose ("must",
   "owns", "never" outside specs) and semantic contradictions between prose
   and promoted spec requirements.
2. Findings are proposals, not verdicts: each is a candidate work item with
   the doc, the passage, the suspected conflicting requirement, and a
   confidence note — a human (or a gate) disposes of it.
3. The sweep runs under a bounded Omnigent worker profile with read-only
   repo access and no credential grants; its output is L1-equivalent and
   never blocks merges directly in v1.
4. Runs after the deterministic pass and consumes its inventory (docs, their
   statuses) so the two passes report against the same snapshot.

## Open questions

- Which model/runtime executes the sweep, and under which worker profile.
- Cost/cadence: nightly full sweep vs weekly full + nightly changed-docs-only.
- False-positive budget before findings move from report-only to PR-blocking.

## Exit

One OpenSpec change after the deterministic run has operated for long enough
to provide the doc inventory and a baseline (do not ratify both passes
together; sequencing is the risk control).

Exiting via: `add-doc-health-semantic-sweep` (ratified 2026-07-09; open
questions resolved in its design.md — headless worker under an Omnigent
profile, Hermes-layer scope resolution defaulting to weekly full + nightly
changed-docs, 70%/20-disposition precision gate). This topic closes when
that change archives on realization evidence.
