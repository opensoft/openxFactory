## 1. Contracts

- [ ] 1.1 Add the four record schemas under `contracts/schemas/`
      (`crystallization-decision`, `crystallization-spec`,
      `crystallization-build`, `crystallization-consent`), each with
      `schema_version` + `kind`, the frozen `automation_rung` L0–L6
      vocabulary, the `effect_class` vocabulary, and shape-only posture
      (policy lives in the canonical validator).
- [ ] 1.2 Add the additive `omnigent-domain-overlay` schema fields:
      the crystallized worker-class marker block (`crystallized`,
      `capability_ref`, `automation_rung`, `replaces_configuration`,
      `throttle`) and the per-category `rung_ceilings` list — no change to
      the archetype vocabulary or the six-boolean matrix.
- [ ] 1.3 Add positive and negative examples per kind — negatives MUST
      include: decision funding above the ceiling, decision without an
      open candidate ref, spend fields on a `not_yet` outcome, spec with
      zero counterexamples, byte-equality golden posing as an equivalence
      predicate, missing effect class, binding whose permissions exceed
      the replaced configuration, crystallized class inventing a sixth
      archetype, EV-rung decision without calibration evidence.
- [ ] 1.4 Continue the MVP fixture corpus: a `crystallization_decision`
      (funded, L3, rungs-1–2 ladder), `crystallization_spec` (mined from
      the three packet-capture episodes, incl. the staging-variant branch
      and ≥1 counterexample), scope fence, and the crystallized-executor
      binding for the packet-capture family the ledger already nominates.
- [ ] 1.5 Register per the "Contracts Pending Realization" policy:
      contracts/README rows now; manifest + CHANGELOG + version allocation
      at the archive bundle cut.

## 2. Validators

- [ ] 2.1 Implement `scripts/validate-crystallizer-contracts.py`
      (derived-models/pattern-ledger style: dependency-free, self-testing
      positives + intended-reason negatives): decision evaluation-order
      rule (ceiling present, valuation rows only ≤ ceiling, funded rung ∈
      valuation), only-path-to-spend shape rules, not-yet completeness,
      braid completeness (domain + tenant + consent refs), spec
      counterexample floor, corpus digest pinning, fence presence, effect
      class enum, decision-ladder maturity rule.
- [ ] 2.2 Extend `scripts/validate-omnigent-contracts.py`: crystallized
      binding rules (existing archetype only, subset-of-replaced
      permissions and credential families, throttle present, constitutional
      falses untouched) and rung-ceiling shape (category uniqueness,
      L3 default documented).
- [ ] 2.3 Validator fixtures/tests wired into the `validate-*.py`
      discipline for both scripts.

## 3. Documentation

- [ ] 3.1 OpenSpec Records entry at raise; doc-index links land with the
      promoted specs at archive.
- [x] 3.2 Update the staging INDEX row/detail on partial promotion (the
      `crystallizer-contracts.md` and `authority-and-consent.md` fragments
      move to `supporting-docs/`).
- [ ] 3.3 Record the artifact-residence lean (design doc table) in the
      build contract's guidance section — declared residence required,
      realization per domain.

## 4. Validation and realization evidence

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate add-crystallizer-contracts
      --strict` and `--all --strict` green.
- [x] 4.2 Declare staged origin (`openxFactory:staging:recurrence-crystallization`)
      in `.openspec.yaml`; verify the supporting-docs manifest and hashes.
- [ ] 4.3 Obtain ratification approval and stamp the proposal front matter
      (`Status: ratified`, `Ratified by:`).
- [ ] 4.4 Realization evidence per `release-realization`: schemas +
      validators merged and green; contract version allocated at the
      archive bundle cut with its annotated tag and release digest
      inventory; archive follows evidence, never precedes it.
