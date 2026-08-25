# Add Doc-Health Semantic Sweep

code_surface: codexFactory, xFactory
target_release: implemented
Status: ratified
Ratified: 2026-07-12 — record: the archive act, commit `f3d4000` "Realize and archive add-doc-health-semantic-sweep", which applied this change's spec delta into `openspec/specs/doc-health/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The commit body records the promotion in words: "Archived via proposal-support wrap (verify -> openspec archive -> bundle): doc-health delta promoted (+8 requirements, ~1 modified)". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The deterministic doc-health pass is running nightly with a committed
baseline, but twelve grep-shaped check families cannot find the two defect
classes the corpus review flagged as highest-risk: untagged normative prose
("must", "owns", "never" asserted outside promoted specs) and semantic
contradictions between prose and the requirements it should follow. The
proposal support (`supporting-docs/agentic-pass.md`) gated this pass on
the deterministic run operating long enough to provide a doc inventory and
baseline — that exit condition is now met.

## What Changes

- Add an agentic semantic sweep as a second doc-health pass: an LLM worker
  reads the governance corpus and reports untagged normative prose and
  prose-vs-spec contradictions.
- Findings are proposals, never verdicts: each names the doc, the passage,
  the suspected conflicting requirement, and a confidence note; disposition
  stays with a human or a gate. The sweep never blocks merges in v1.
- The sweep splits into two parts with distinct authorities: deterministic
  orchestration under the factory identity (the openxFactory GitHub App
  token, as the deterministic pass runs today), and a credential-less
  analysis worker bounded by an Omnigent worker profile with a job envelope
  the report cites; analysis output carries L1 authority.
- Sweep scope is Hermes-owned policy: each layer (customer, client, domain)
  may declare a `doc_health.sweep_scope`; the deepest declaration wins,
  defaulting to incremental (nightly changed-docs + weekly full).
- Disposition authority follows content ownership: the owning factory's
  Domain Hermes for its own docs, the neutral ratify gate for neutral or
  cross-repo findings; Client/Customer Hermes have no disposition standing
  in v1.
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

- `doc-health`: ADDED requirements for the agentic semantic sweep (the two
  semantic families, the orchestration/analysis execution split, the bounded
  analysis worker profile, findings-as-proposals, disposition authority,
  sequencing, Hermes-layer scope resolution, and the report-only-to-blocking
  promotion gate); MODIFIED "Deterministic check families" to re-scope its
  semantic-sweep exclusion to the deterministic pass only.

## Impact

- openxFactory: `doc-health` spec delta; proposal support is retained with
  this change and packaged when the change archives.
- codexFactory: sweep implementation (prompt contract, runner integration
  under `scripts/doc_health/`, tests) — implementation owner per the
  existing ownership split.
- xFactory aggregation repo: nightly workflow gains the sweep step after
  the deterministic run; sweep findings section lands in the dated report.
- Domain repos: Hermes layer overlays MAY declare `doc_health.sweep_scope`
  (optional; no immediate change — the default applies until a layer
  declares).
- Realization gate: non-none code surface — this change archives only after
  the sweep implementation merges and a green run of the sweep surface
  exists.
