---
code_surface: codexFactory (the derive-possibles worker + versioned prompt contract, the nightly workflow lane, and the next-run merge into the openxFactory-hosted possibles_register), openxFactory (the additive possibles-register kernel delta — origin + derivation $defs — plus the packaged example and the delegated register validator), xFactory aggregation (nightly child dispatch + submodule commit-back), omnigent-install (one bounded read-only derive-possibles worker profile)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
---

# Proposal: add-possibles-derivation-lane

## Why

The landed cross-reference index (`add-ideation-cross-reference-readiness`)
carries `possibles_register` deliberately ABSENT at bootstrap, so the
dashboard funnel's possibles column is empty and the WHEEL can only show
synthesized, demo-marked placeholders. Brett's direction (ideation-dashboard
brainstorm, v5 candidate 1): "it must be that we have possibilities — that is
what we want our AI system to do, help think of possible connections." The
ratified v1 design named an AI-assist surface for exactly this and deferred
it; nothing yet fills it.

What is missing is a bounded generative lane: an AI worker that reads the
index (topic clusters, staged topics, member documents) and PROPOSES candidate
possibles — durable "this cluster could become X" backlog statements — for
humans to dispose. This is distinct from the readiness lane, which JUDGES
existing clusters with tier scores; derivation SYNTHESIZES new register
entries. Without it the possibles register stays empty and the realization
funnel has no left-hand supply.

## What Changes

- Add a bounded, read-only `derive-possibles` Omnigent lane — its own worker
  profile, prompt, and output schema, mirroring the document-cataloger and
  ideation-readiness lanes — that derives CANDIDATE possibles from the promoted
  `ideation-cross-reference` index and proposes `possibles_register` entries.
- Every derived entry carries `origin: ai-derived`, a `derivation` block naming
  the worker run (correlation id, worker profile, prompt-contract version), and
  machine `disposition: pending_review`, citing the source clusters and member
  documents it was derived from through the register's existing
  `claiming_clusters` and `supporting_evidence` fields.
- Add the small ADDITIVE `ideation-possibles-register` kernel delta this needs —
  optional `origin` and a `derivation` $def on `register_entry`, modelled
  one-for-one on the topic entry's `origin` + `human_seen` intake pair — with no
  `contract_schema_version` bump because it only adds optional fields and leaves
  human-authored possibles unchanged.
- Keep identity orchestration-authoritative: the tool-less worker NEVER
  computes or transcribes machine-precision values (register ids, hashes,
  counts); orchestration computes them and treats its own values as
  authoritative, carrying forward the document-cataloger contract that a
  mis-copied hash character voids the affected entries.
- Merge derived proposals into `ideation/cross-reference.yaml`'s
  `possibles_register` only through a later main run, under concurrency
  protection against stale overwrite; the one-way disposition lifecycle is
  respected, humans dispose on the gate console, and nothing auto-promotes.
- Contain failure like the cataloger lane: an offline/unauthorized/partial/
  invalid/failed worker cannot delay or suppress deterministic reporting; a
  watchdog reports and cancels a child queued beyond ten minutes or running
  beyond thirty minutes; immutable evidence commits under the factory identity.
- Report derived-but-undisposed possibles as their own section, excluded from
  any Ranked Plan; dashboard/WHEEL consumption renders them as a distinct
  non-`indexed` edge class (`inferred`/`synthesized`) until disposed, satisfying
  the WHEEL "possibles honesty rule" with real data instead of demo placeholders.

## Capabilities

### Modified Capabilities

- `ideation-cross-reference`: Adds the derived-possible register-entry contract
  (origin/derivation/pending_review provenance, the additive kernel delta), the
  orchestration-authoritative-identifier rule, the one-way gate-console
  disposition lifecycle, the bounded derivation worker with immutable evidence
  and concurrency-protected next-run merge, and the distinct-class consumption
  rule for the dashboard/WHEEL. No requirement of the readiness index is
  removed; every score, human-seen, and register invariant already promoted
  stands.
- `doc-health`: Adds the nightly possibles-derivation lane beside the semantic
  sweep, document-cataloger, and ideation-readiness lanes — report-only,
  skip-safe, recommendations at most `warning` with resolution class
  `contested`, derived possibles in their own report section excluded from the
  Ranked Plan; the lane adds no deterministic check family.

## Impact

- **openxFactory:** the additive `ideation-possibles-register` kernel delta
  (`origin` + `derivation` $def), a packaged derived-possible example, the
  delegated register validator (`validate-ideation-dashboard-contracts.py`)
  enforcing the new shape and one-way disposition, the index validator's
  delegation note, and additive ideation guidance. Contract registration in
  `contracts/manifest.yaml`/`CHANGELOG.md`/`README.md` at realization.
- **codexFactory:** the derive-possibles worker (versioned prompt, candidate
  derivation from clusters/topics/members, orchestration-computed identity, the
  register evidence contract, output validation), the next-run merge, and tests;
  realization follows the ideation-readiness two-repo split.
- **xFactory aggregation:** nightly child dispatch after the deterministic pass,
  the watchdog, immutable evidence commit, and report links; the openxFactory
  submodule commit-back and pin bump that persist the merged register.
- **omnigent-install:** one bounded read-only `derive-possibles` worker profile
  reusing the existing document-analysis host pattern; no new host class, no new
  Entra user or Cloud PC.
- **Compatibility:** the kernel delta is additive (no `contract_schema_version`
  bump); source documents are never edited, moved, or promoted; derived
  possibles only ever enter the existing human-disposed review flow, and nothing
  auto-promotes.
