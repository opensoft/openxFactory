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
- Bound the analysis worker: read-only, credential-less, output at L1
  authority; keep orchestration deterministic under the existing factory
  identity.
- Make sweep scope Hermes-owned policy with a deterministic resolution rule.

**Non-Goals:**

- Merge blocking in v1 (promotion is a future OpenSpec delta gated on
  measured precision).
- Auto-fixing anything the sweep finds — semantic findings are always
  `contested` by construction.
- Replacing or altering any deterministic check family.
- A Hermes policy runtime — scope resolution reads overlay files directly.

## Decisions

1. **Two-part execution split.** Orchestration (inventory consumption,
   scope resolution, worker invocation, findings merge, report commit) is
   deterministic runner code in the existing reusable workflow, under the
   factory identity — the short-lived installation token minted from the
   openxFactory GitHub App, exactly as the deterministic pass runs today.
   Analysis (the model-driven judgment step) is the only part bounded as an
   Omnigent-profile worker. Alternative considered: run the whole sweep as
   one Omnigent job — rejected: orchestration is xFactory-layer plumbing
   (gates, state, audit), the deterministic pass sets the precedent that
   plumbing is runner code, and the split isolates model-runtime failures
   from report commits.
2. **Credential-less analysis worker with a job envelope.** The worker
   receives a local read-only checkout prepared by orchestration and holds
   no repository credentials or factory identity token — nothing to leak.
   Its sole write is the findings artifact. The invocation carries a job
   envelope conforming to the neutral job-envelope contract, and the report
   records the envelope reference alongside the pinned model id and
   prompt-contract version — full audit linkage without moving CI plumbing
   into Omnigent. In v1 the worker is a headless Claude Code invocation
   (`claude -p`) conforming to the profile; migrating it onto the
   AgentTower runtime later changes hosting, not the contract.
3. **Sweep scope is Hermes-owned policy, deepest declaration wins.** Each
   Hermes layer overlay (customer, client, domain) MAY declare
   `doc_health.sweep_scope` from the ordered set `incremental` <
   `full-weekly` < `full-nightly`; orchestration resolves the effective
   scope as the maximum across declarations, defaulting to `incremental`
   (nightly changed-docs + weekly full). Rationale: the layer model assigns
   policy to Hermes — a workflow knob would quietly park policy in the
   xFactory layer; Client Hermes already owns "CI conventions and required
   check profiles", Domain Hermes owns admission policy, and a project
   (Customer Hermes) may demand deeper review than the org default.
   Deepest-wins is monotone: any layer can raise scrutiny, none can lower
   another's. Resolution is deterministic — read up to three YAML overlays,
   take the max — so it lives in orchestration and needs no Hermes runtime.
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
6. **Disposition authority follows content ownership.** Findings on a
   domain factory's own docs are disposed by that factory's authority (its
   Domain Hermes); findings implicating a neutral openxFactory artifact or
   spanning repos go to the neutral ratify gate. Client and Customer Hermes
   have no disposition standing in v1 — their lever is the scope
   declaration. Ranked-plan items name their disposer, and a disposition
   recorded by any other authority is an uncited resolution under the
   existing contested-finding rule.
7. **False-positive budget before any promotion to blocking:** a future
   delta may promote contradiction findings to PR-blocking only with
   evidence of ≥70% confirmed-valid rate across ≥20 dispositioned semantic
   findings within a rolling 30-day window. The dispositions file is the
   measurement source, so the gate is auditable.

## Risks / Trade-offs

- [Model nondeterminism makes reports noisy across runs] → findings carry a
  stable id (doc path + passage hash); recurring findings dedupe against
  the previous report the same way deterministic findings do.
- [Sweep cost grows with corpus] → `incremental` default; a deeper scope is
  a deliberate Hermes declaration, so cost increases are attributable to a
  layer's explicit policy, never drift.
- [Model outage breaks the nightly run] → the analysis step is non-fatal:
  on failure the report records the sweep as skipped, deterministic results
  land regardless.
- [Prompt drift silently changes finding quality] → the prompt contract is
  a versioned file in codexFactory; the report records the prompt version
  alongside the model id and envelope reference.
- [Overlay declarations diverge across domain repos] → resolution reads the
  pinned submodule state, so a declaration takes effect only through the
  normal pin-sync gate.

## Migration Plan

1. Land the spec delta (this change) — no runtime effect.
2. codexFactory: implement inventory emission, scope resolution from Hermes
   overlays, the analysis worker invocation and prompt contract, and tests;
   merge through normal gates.
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
- Whether `doc_health.sweep_scope` belongs in a general Hermes policy
  vocabulary once more policies want layered deepest-wins resolution
  (candidate for a future neutral capability; out of scope here).
