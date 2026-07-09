# Add Doc-Health Semantic Sweep

code_surface: codexFactory, xFactory
target_release: implemented

## Why

The deterministic doc-health pass is running nightly with a committed
baseline, but twelve grep-shaped check families cannot find the two defect
classes the corpus review flagged as highest-risk: untagged normative prose
("must", "owns", "never" asserted outside promoted specs) and semantic
contradictions between prose and the requirements it should follow. The
staged topic (`ideation/staging/semantic-health-sweep/`) gated this pass on
the deterministic run operating long enough to provide a doc inventory and
baseline — that exit condition is now met.

## What Changes

- Add an agentic semantic sweep as a second doc-health pass: an LLM worker
  reads the governance corpus and reports untagged normative prose and
  prose-vs-spec contradictions.
- Findings are proposals, never verdicts: each names the doc, the passage,
  the suspected conflicting requirement, and a confidence note; disposition
  stays with a human or a gate. The sweep never blocks merges in v1.
- The sweep runs under a bounded read-only Omnigent worker profile with no
  credential grants; its output carries L1 authority.
- Sequencing: the sweep runs after the deterministic pass and consumes its
  inventory, so both passes report against the same corpus snapshot.
- Re-scope the deterministic pass's exclusion sentence: "semantic sweeps are
  out of scope" becomes "the deterministic pass makes no model calls; the
  semantic sweep is the separate agentic pass" — the capability now owns
  both passes with distinct mechanisms and failure modes.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `doc-health`: ADDED requirements for the agentic semantic sweep (scope,
  finding contract, execution profile, sequencing, cadence, and the
  report-only-to-blocking promotion gate); MODIFIED "Deterministic check
  families" to re-scope its semantic-sweep exclusion to the deterministic
  pass only.

## Impact

- openxFactory: `doc-health` spec delta; staged topic
  `ideation/staging/semantic-health-sweep/` closes when this change
  archives.
- codexFactory: sweep implementation (prompt contract, runner integration
  under `scripts/doc_health/`, tests) — implementation owner per the
  existing ownership split.
- xFactory aggregation repo: nightly workflow gains the sweep step after
  the deterministic run; sweep findings section lands in the dated report.
- Realization gate: non-none code surface — this change archives only after
  the sweep implementation merges and a green run of the sweep surface
  exists.
