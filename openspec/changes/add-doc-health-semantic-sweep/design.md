# Design: Doc-Health Semantic Sweep

## Context

The deterministic doc-health pass (twelve check families, codexFactory
implementation, nightly xFactory runner) is live with a committed report
baseline. The staged topic `ideation/staging/semantic-health-sweep/` defines
a second pass that only a model can perform: reading prose the way a
reviewer would. The two passes deliberately stay in one capability but with
distinct mechanisms — grep-shaped determinism vs LLM judgment — and this
design keeps their failure modes separated so the deterministic gate never
depends on model availability.

## Goals / Non-Goals

**Goals:**

- Surface untagged normative prose and prose-vs-spec contradiction
  candidates across the whole pinned corpus.
- Keep every semantic finding a disposable proposal that feeds the existing
  ranked plan and disposition machinery unchanged.
- Bound the worker: read-only, no credential grants, output at L1 authority.

**Non-Goals:**

- Merge blocking in v1 (promotion is a future OpenSpec delta gated on
  measured precision).
- Auto-fixing anything the sweep finds — semantic findings are always
  `contested` by construction.
- Replacing or altering any deterministic check family.

## Decisions

1. **Runtime: headless agent step in the existing nightly runner.** The
   sweep executes as a headless Claude Code invocation (`claude -p`) added
   to the aggregation repo's nightly workflow after the deterministic pass,
   with a pinned model id recorded in the workflow. Alternative considered:
   a standalone service — rejected as premature; the runner already owns
   scheduling, checkout, and report commit rights.
2. **Worker profile: bounded read-only Omnigent worker.** The invocation
   conforms to the neutral job-envelope contract: read-only repository
   checkout, no credential grants beyond model API access, and no write
   path except its findings file, which the (deterministic) runner merges
   into the report. Output authority is L1 — same rank as notebook
   synthesis.
3. **Cadence: weekly full sweep, nightly changed-docs-only.** Nightly runs
   sweep only docs whose content changed since the previous report
   (computed from the inventory diff); a weekly run sweeps the full corpus.
   Alternative (nightly full) rejected on cost; alternative (weekly only)
   rejected because contradictions are most cheaply fixed the day they
   land. Every report states which scope ran.
4. **Snapshot coupling via the inventory artifact.** The deterministic pass
   emits its doc inventory (paths, statuses, content hashes) as a
   machine-readable artifact; the sweep consumes exactly that inventory.
   Both passes therefore describe the same corpus snapshot, and the
   changed-docs set is derived by hash diff against the previous inventory
   rather than by a second git walk.
5. **Findings map onto the existing severity/resolution contract.**
   Semantic findings are always resolution-class `contested` and severity
   at most `warning`. Because the regression-issue rule fires only on
   `critical`/`error`, the sweep can never open issues or block anything in
   v1 without any special-case carve-out.
6. **False-positive budget before any promotion to blocking:** a future
   delta may promote contradiction findings to PR-blocking only with
   evidence of ≥70% confirmed-valid rate across ≥20 dispositioned semantic
   findings within a rolling 30-day window. The dispositions file is the
   measurement source, so the gate is auditable.

## Risks / Trade-offs

- [Model nondeterminism makes reports noisy across runs] → findings carry a
  stable id (doc path + passage hash); recurring findings dedupe against
  the previous report the same way deterministic findings do.
- [Sweep cost grows with corpus] → changed-docs-only nightly default;
  weekly full sweep is the cost ceiling and is a single workflow knob.
- [Model outage breaks the nightly run] → the sweep step is non-fatal: on
  failure the report records the sweep as skipped, deterministic results
  land regardless.
- [Prompt drift silently changes finding quality] → the prompt contract is
  a versioned file in codexFactory; the report records the prompt version
  alongside the model id.

## Migration Plan

1. Land the spec delta (this change) — no runtime effect.
2. codexFactory: implement inventory emission, the sweep runner and prompt
   contract, and tests; merge through normal gates.
3. xFactory: add the sweep step to the nightly workflow (non-fatal).
4. First green nightly with the sweep section in the report is the
   realization evidence; the change archives on it.

Rollback: remove the workflow step; the deterministic pass is untouched.

## Open Questions

- Which pinned model tier balances cost vs judgment quality (start:
  the mid-tier model; revisit after the first weekly full sweep's token
  bill).
- Whether untagged-normative-prose findings should eventually become a
  deterministic family once the prose-tagging vocabulary stabilizes
  (tracked in `ideation/staging/prose-tagging/`, not here).
