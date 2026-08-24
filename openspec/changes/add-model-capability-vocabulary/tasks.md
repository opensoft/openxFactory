# Tasks: add-model-capability-vocabulary

Status: draft

NOTHING BELOW RUNS BEFORE RATIFICATION. This change's own diff is the spec
delta and these records. Realization cuts a contract bundle; the number is
allocated at §4, not here.

## 1. The schema

- [ ] 1.1 Add an OPTIONAL `modalities` property to `$defs/model_entry` in
  `contracts/schemas/xfactory-workbench-model-catalog.schema.yaml`: an array,
  `uniqueItems: true`, `minItems: 1`, items constrained to the closed set
  `text` and `image`. Not added to `required` — absence must stay valid.
- [ ] 1.2 State in the schema's own prose why the set is closed and how it
  extends (the change that governs a new member), mirroring how
  `admission_surface` states its extension route.
- [ ] 1.3 State that absence is not a claim — the producer predates the field —
  reusing the chat-turn family's wording for the same idiom.

## 2. The type and the two batched fixes

- [ ] 2.1 `doxbench_model.py`: read and validate `modalities` on
  `ModelCatalogEntry`. Refuse a member outside the closed set, an empty set,
  and a set omitting `text`.
- [ ] 2.2 TAKEN follow-up 1 — enforce the released entry-count cap on the
  catalog type. Reproduced: a 65-entry catalog constructs today while the
  released schema caps `models` at 64. Restate the bound with a comment naming
  the released cap it mirrors, as `MAX_ROUTING_TARGETS` already does.
- [ ] 2.3 TAKEN follow-up 2 (review N7) — hold `model_id` to the released
  length and pattern bounds, the same bounds `_require_model_reference` already
  applies to `routes_to` members and `resolved_model_id`. Reproduced: a
  200-character id and an id containing a space both construct today. Remove
  the deferral note, which says the fix "belongs to no release" — this is that
  release.
- [ ] 2.4 Both fixes are BEHAVIOUR CHANGES that tighten construction toward the
  released schema. Record them in the change's own realization notes, and
  check the existing corpus and fixtures for values that would now be refused
  before landing.

## 3. Validator, examples and tests

- [ ] 3.1 `scripts/validate-ideation-dashboard-contracts.py`: cover the new
  refusals, including a packaged NEGATIVE for an out-of-vocabulary modality and
  one for an image-only set.
- [ ] 3.2 A packaged POSITIVE example declaring `[text, image]`, and one
  declaring nothing, so absence is exercised as a valid shape.
- [ ] 3.3 Tests under `tests/ideation-dashboard/` for each refusal and for the
  absence default; revert-test the two bound fixes so a weakened gate fails.

## 4. The contract release

- [ ] 4.1 ALLOCATE THE BUNDLE NUMBER FRESH at this point — `contract-v1.41`
  only if the pending Unreleased block has not folded first. Re-count at the
  tip AND again at the landing squash; this repository has renumbered
  mid-flight more than once.
- [ ] 4.2 CHANGELOG entry, `contracts/manifest.yaml` row and digest,
  `contract_bundle_version` bump, inventory rebuilt AFTER the bump, then the
  verify-commit. Per `docs/contract-versioning-policy.md`.
- [ ] 4.3 NO TAG until the landing squash.
- [ ] 4.4 Note the consumer re-pin: codexFactory pins this schema by digest.
  Additive, so a consumer may ignore the field, but the pin moves.

## 5. Validate green

- [ ] 5.1 Gates: `pytest tests/ideation-dashboard`, `pytest
  tests/ideation_dashboard`, `pytest tests/doc-health`;
  `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`; doc-health zero-new
  against a fresh same-clock `origin/main` baseline;
  `scripts/validate-ideation-dashboard-contracts.py` at its baseline.
- [ ] 5.2 Contract-release verification per the policy, including that the
  inventory was rebuilt after the version bump rather than before.

## 6. Bookkeeping

- [ ] 6.1 README OpenSpec Records: move this change from active to archived
  when it archives.
- [ ] 6.2 The staged topic keeps its row: this is exit (a) of three, and the
  topic exits only when (b) and (c) have landed too.

## 7. NOT part of this change

- Reading `modalities` to choose a destination. That is exit (b), which also
  inherits the pre-assembly request-bound constraint recorded in the topic's Q1
  disposition, and which must be sequenced against the ratified-but-unbuilt
  intake lane.
- Any further capability dimension. Audio, video, tool-calling, structured
  output, latency and cost enter only with a change that governs a consumer.
- Compression, disclosure, and the `reduced_reason` constant — exit (c).
