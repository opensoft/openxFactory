# Design: Proposal Origin Contract

## Context

The promoted document lifecycle moves staged material into a change's
`supporting-docs/` with a manifest, and doc-health validates that support
record. But provenance is recorded from the staging side only: nothing in the
proposal packet itself declares where the proposal came from, and nothing
distinguishes "deliberately created ad hoc with approval" from "silently
bypassed the pipeline". The bootstrap `add-proposal-supporting-doc-lifecycle`
change is the worked example of the gap.

The active `add-cross-factory-ideation-routing` change extended the manifest
with `ideation_provenance` for routed claims and explicitly left "general
proposal-origin/archive-source-state policy to the staged
`proposal-origin-contract` topic". This change is that policy.

Delta sequencing follows the promoted ordered-deltas rule: the doc-health
"Deterministic check families" requirement is currently modified by the
semantic-sweep (wording), document-cataloging (thirteenth family), and
ideation-routing (fourteenth family) changes, in that declared order. This
change declares its enumeration delta relative to the ideation-routing
outcome and adds `proposal-origin` as the fifteenth family; its
document-lifecycle "Proposal-owned supporting documents" delta is likewise
declared relative to the routing outcome (which added `ideation_provenance`).

## Goals / Non-Goals

**Goals:**

- Make every proposal's origin machine-checkable at the proposal gate, the
  archive gate, and in the nightly deterministic pass.
- Keep ad-hoc creation possible but explicit, approved, and durable.
- Backfill history from recorded evidence without fabricating staging
  sources.
- Prove the contract by self-application: this change's own packet declares
  its staged origin.

**Non-Goals:**

- FDA/SaMD or other regulated-traceability compliance. The staged
  [FDA SaMD Traceability Rationale](../../../ideation/staging/proposal-origin-contract/fda-samd-traceability-rationale.md)
  records why origin provenance is necessary but not sufficient; the
  regulated-traceability profile is future work and deliberately remains
  staged.
- Routing-claim provenance (`ideation_provenance`) — owned by
  `add-cross-factory-ideation-routing`; this change only makes the two
  declarations consistent in one manifest.
- Retroactive re-litigation of archived decisions — migration classifies,
  it does not judge.

## Decisions

- **Origin lives in `.openspec.yaml`**, not the proposal prose: it must be
  machine-checkable, survive archive byte-for-byte, and stay outside the
  Markdown that authors edit freely.
- **Durable ids** (`<repo>:staging:<topic>` / `<repo>:adhoc:<date>-<slug>`)
  decouple provenance from filesystem state; a staged origin's path is the
  historical record of where the topic lived at transition, not a live link.
- **Fifteenth family, not a fold-in:** origin checks join the numbered
  deterministic-family convention (13th catalog, 14th routing) rather than
  overloading the existing supporting-document integrity requirement, keeping
  one family per owning contract area.
- **Fail-closed gates, report-only nightly:** the proposal and archive gates
  reject violations outright; the nightly family reports drift (e.g. a
  post-ratification mutation) as findings with `contested` resolution class,
  since undoing one is reversing a gate decision.
