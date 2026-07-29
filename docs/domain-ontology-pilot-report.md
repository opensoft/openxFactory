# Domain-Ontology Pilot Report — MedxFactory / codexFactory

Status: record
Kind: report
Ratified by: [add-domain-ontology-layer](../openspec/changes/add-domain-ontology-layer/proposal.md) (tasks 7.1–7.4)
Repository context: openxFactory
Purpose: the recorded evidence of the two contrasting domain pilots run on
2026-07-29 — generation, conflict precedence, stewardship, releases across
every compatibility class, readiness, and worker-scoped context compilation
— and the kernel-minimization findings they produced. The pilot packages
are retained verbatim as validator-covered fixtures under
[`contracts/domain-ontology/examples/pilots/`](../contracts/domain-ontology/examples/pilots/).

## What ran

Both pilots used approved domain answer sets ("two equivalently contrasting
approved domain fixtures" per task 7.2): MedxFactory's drawn from the
clinical journey model (patient subject; treatment/care-plan/condition focal
items; intake→diagnosis→treatment-planning→active-treatment→monitoring
journey states) and codexFactory's from the engineering domain model
(project subject; repository/feature focal items; execution/review lanes,
admission journey). Every step below is reproducible from the pinned tools
in this repository; the pilot packages import kernel `xf/core` 0.1.0 at
digest `46e45f6c…d898b7`.

## Evidence log

```text
7.1 dry-run: exit 0, files written besides answers: 0
medx generate: exit 0            (19 concepts seeded across 8 kernel parents)
medx ingest (colliding + clean): exit 1 (conflict recorded: True)
medx readiness with unresolved conflict: blocked (domain_scaffold_required)
medx conflict dispositioned: rejected by medx-ontology-steward
medx first publication 0.1.0 -> 1.0.0 additive: exit 0
medx breaking 1.0.0 -> 2.0.0 (reparent, migration shipped): exit 0, line xf/medx@2
medx maintenance no-drift check recorded: exit 0
medx readiness: ontology_ready
medx worker contexts (verify, generate): compiled, closed subsets
medx canonical validation over pilot repo: exit 0
codex generate: exit 0           (18 concepts seeded)
codex first publication 0.1.0 -> 1.0.0 additive: exit 0
codex retiring 1.0.0 -> 1.1.0 (term retired, migration shipped): exit 0, line xf/codex@2
codex readiness: ontology_ready
codex worker context (verify): compiled, closed subset
codex canonical validation over pilot repo: exit 0
```

## Findings

1. **Structured imports take precedence and conflicts block review (7.3).**
   The model-extraction batch re-proposing `xf/medx/care_plan` was
   auto-recorded as a CONFLICTING candidate against the structured import,
   and readiness stayed `domain_scaffold_required` until the accountable
   steward dispositioned it (rejected). The clean proposal in the same
   batch (`xf/medx/care_gap`) entered the register normally.
2. **Every compatibility class exercised with history intact (7.4).**
   Additive first publications on both domains; a breaking reparent
   (`xf/medx/treatment` gains `xf/core/intervention`) shipping its
   migration map and opening line `xf/medx@2`; a retiring release
   (`xf/codex/decomposition` retired with its migration disposition)
   opening `xf/codex@2`. Superseded versions are retained byte-identically
   under `retained/<version>/` in both pilot fixtures — the two-pin
   coexistence and rollback story is structural: every historical release
   record and retained manifest keeps its original digest, so re-pinning
   the prior version is a pointer change with no rewrite anywhere.
3. **Kernel minimization (7.2): no domain leakage; adoption evidenced.**
   All 37 pilot concepts landed in `xf/medx`/`xf/codex` namespaces; no
   pilot needed a new kernel term, no kernel term went unused as a
   specialization parent or reference across the pair, and the two domains
   share the core without importing each other's vocabulary. The kernel's
   per-term adoption evidence was recorded (two resolvable adopters per
   term from the semantic-decisions inventory, plus the two pilot packages
   at package level); the kernel remains DRAFT — publication is the
   governed bundle-cut decision, now unblocked.
4. **The Omnigent seam works end-to-end (design decision 13).** Worker
   profiles (`verify`, `generate`, `assemble_for_admission`) compiled to
   closed, digest-pinned per-worker contexts on both domains — a verify
   worker's context carries its classification terms and their kernel
   ancestors, nothing else, and no authority-named field at any depth.
5. **7.1 dry-run migration path.** The starter's `--dry-run` against a
   repo produced the full report and wrote nothing — the explicit
   migration/report path for existing DomainxFactory repositories.

## Residual observations for the domain adoptions

- The medx quality gate passed at 15/16 intake coverage; the breaking and
  retiring releases used recorded reviewed exceptions
  (`review://medx/exception-break`, `review://codex/exception-retire`) —
  live domains should prefer fresh quality reports over exceptions.
- Pilot stewards are named placeholders for the real Domain Hermes rosters;
  the Medx roster composition is an open decision round
  (`medxfactory-domain-hermes-content`).
