## 1. Contracts

- [x] 1.1 Add the record schemas under `contracts/schemas/`
      (`crystallized-capability-registry` record, `dispatch-record`,
      `adjudication-record`, `sentinel-policy`,
      `capability-health-report`, `savings-entry` + `calibration-score`),
      each with `schema_version` + `kind`, the status spine and fallback-
      cause vocabularies, and shape-only posture (policy in the canonical
      validator).
- [x] 1.2 Add positive and negative examples per kind — negatives MUST
      include: a registry record embedding episode payloads, an illegal
      status transition (candidate → active skipping proofs), a served
      dispatch record with unevaluated post-conditions, a fallback without
      a cause, a `compensable` capability admitted by the junction, a
      dispatch record without provenance, an active capability with
      sentinel ε at zero, a savings entry claiming `verified` without a
      fresh sentinel anchor, and a promotion without its demotion trigger
      bundle.
- [x] 1.3 Complete the MVP fixture corpus: the packet-capture capability's
      registry record in `shadow`, three dispatch records (served,
      fence-miss fallback, sentinel dual-run), the ε=0.20-no-decay
      sentinel policy, one bidirectional adjudication, a health report
      with one auto and one contested finding, and a sentinel-anchored
      savings entry.
- [x] 1.4 Register per the "Contracts Pending Realization" policy:
      contracts/README rows now; manifest + CHANGELOG + version allocation
      at the archive bundle cut (contract-v1.21 expected). — Rows added
      2026-07-29; manifest + CHANGELOG + version at archive.

## 2. Validator

- [x] 2.1 Implement `scripts/validate-capability-steward.py`
      (jsonschema-based, self-testing positives + intended-reason
      negatives): digests-only rule, status-transition legality (spine
      order; proofs before authority), pins-vs-live-authority shape (D10),
      effect-class admission (D11), fallback-cause taxonomy,
      post-conditions-evaluated rule, provenance-required rule,
      sentinel-floor rule (ε > 0 while authoritative), savings-anchor
      rule (verified requires a fresh anchor ref), demotion-bundle rule
      (no `active` without triggers armed), adjudication verdict/
      consequence pairing.
- [x] 2.2 Validator fixtures/tests wired into the `validate-*.py`
      discipline.

## 3. Documentation

- [ ] 3.1 OpenSpec Records entry at raise; doc-index links land with the
      promoted specs at archive.
- [x] 3.2 Update the staging INDEX row/detail on partial promotion (the
      `steward-contracts.md` fragment moves to `supporting-docs/`; the
      dials register remains staged as the topic's living remainder).
- [ ] 3.3 Close the topic's exit-path record: all three waves archived;
      note the cross-tenant fragment as the deliberate brainstorm
      remainder for a later wave.

## 4. Validation and realization evidence

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate add-capability-steward
      --strict` and `--all --strict` green — verified at raise, ratify, and
      realization (2026-07-29).
- [x] 4.2 Declare staged origin (`openxFactory:staging:recurrence-crystallization`)
      in `.openspec.yaml`; verify the supporting-docs manifest and hashes.
- [x] 4.3 Obtain ratification approval and stamp the proposal front matter
      (`Status: ratified`, `Ratified by:`) — ratified by Brett 2026-07-29.
- [ ] 4.4 Realization evidence per `release-realization`: schemas +
      validator merged and green; contract version allocated at the
      archive bundle cut with its annotated tag and release digest
      inventory; archive follows evidence, never precedes it.
