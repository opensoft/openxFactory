# Tasks: add-model-capability-vocabulary

Status: ratified
Ratified: 2026-08-24 — `review/ratification-2026-08-24.md`. These are AUTHORIZED, not performed, by the ratification.

NOTHING BELOW RUNS BEFORE RATIFICATION. This change's own diff is the spec
delta and these records. Realization cuts a contract bundle; the number is
allocated at §4, not here.

REALIZED 2026-08-29 as **`contract-v2.2`** — record: `realization-evidence.md`.
The number was fresh-counted at the branch base and again before the landing
squash, exactly as §4.1 demands: `contract-v1.41` had been taken seven releases
and one major earlier. §6.1 is the only task left open, and deliberately: a
code-surface change archives after the merge and a green run, never with the
cut.

## 1. The schema

- [x] 1.1 Add an OPTIONAL `modalities` property to `$defs/model_entry` in
  `contracts/schemas/xfactory-workbench-model-catalog.schema.yaml`: an array,
  `uniqueItems: true`, `minItems: 1`, items constrained to the closed set
  `text` and `image`. Not added to `required` — absence must stay valid.
  THE SCHEMA MUST ALSO REQUIRE `text` MEMBERSHIP where the property is present
  (`contains: {const: text}` or equivalent). Review found that `minItems` plus
  an item enum would accept `modalities: [image]`, which the requirement and
  its negative scenario refuse — and a schema-only consumer would then treat
  that instance as a conformant released catalog even though the type and the
  standalone validator reject it. The wire gate must not be the weakest one;
  that is the very divergence class §2 exists to close.
- [x] 1.2 State in the schema's own prose why the set is closed and how it
  extends (the change that governs a new member), mirroring how
  `admission_surface` states its extension route.
- [x] 1.3 State that absence is not a claim — the producer predates the field —
  reusing the chat-turn family's wording for the same idiom.

## 2. The type and the two batched fixes

- [x] 2.1 `doxbench_model.py`: read and validate `modalities` on
  `ModelCatalogEntry`. Refuse a member outside the closed set, an empty set,
  and a set omitting `text`.
- [x] 2.1b PROJECT IT ONTO THE WIRE, with a test. Review found the gap: the
  projection is not automatic — `ModelCatalogEntry.as_public_dict()` emits an
  EXPLICIT key list (`PUBLIC_ENTRY_FIELDS`, plus the routing fields when the
  entry is a rule), so a declared `modalities` would be validated in process
  and then silently dropped by `GET /workbench/model-catalog`, leaving
  consumers and the routing successor with nothing to read. Follow the
  PRESENT-ONLY-WHEN-DECLARED idiom the routing fields already use, and for the
  same stated reason: an undeclared entry's public dict must stay byte-identical
  across the release boundary.
- [x] 2.2 TAKEN follow-up 1 — enforce the released entry-count cap on the
  catalog type. Reproduced: a 65-entry catalog constructs today while the
  released schema caps `models` at 64. Restate the bound with a comment naming
  the released cap it mirrors, as `MAX_ROUTING_TARGETS` already does.
- [x] 2.3 TAKEN follow-up 2 (review N7) — hold `model_id` to the released
  length and pattern bounds, the same bounds `_require_model_reference` already
  applies to `routes_to` members and `resolved_model_id`. Reproduced: a
  200-character id and an id containing a space both construct today. Remove
  the deferral note, which says the fix "belongs to no release" — this is that
  release.
- [x] 2.4 These are BEHAVIOUR CHANGES that tighten construction toward the
  released schema. Record them in the change's own realization notes, and
  check the existing corpus and fixtures for values that would now be refused
  before landing.
- [x] 2.5 WIDENED BY BRETT'S RULING (2026-08-24): enforce the remaining
  schema-declared string bounds too — `label` (released `maxLength: 200`),
  `provider_class` (64) and `data_handling` (500), each checked type-side only
  for blankness today. The proposal had recorded these as a named follow-up
  because the batching obligation named two; Brett widened the scope to ALL
  FIVE string-bounded fields, so there is no residue. Reproduced 2026-08-24:
  201, 65 and 501 characters respectively all construct cleanly.
  `resolved_model_id` is the fifth and is ALREADY enforced through
  `_require_model_reference`, which is the proof the pattern works — reuse it
  rather than writing a fourth spelling.

## 3. Validator, examples and tests

- [x] 3.1 `scripts/validate-ideation-dashboard-contracts.py`: cover the new
  refusals, including a packaged NEGATIVE for an out-of-vocabulary modality and
  one for an image-only set — the latter must be refused by the SCHEMA as well
  as the validator, per §1.1.
- [x] 3.2 A packaged POSITIVE example declaring `[text, image]`, and one
  declaring nothing, so absence is exercised as a valid shape.
- [x] 3.3 Tests under `tests/ideation-dashboard/` for each refusal, for the
  absence default, and for the WIRE PROJECTION (a declared set reaches
  `GET /workbench/model-catalog`; an undeclared entry's bytes are unchanged);
  revert-test the two bound fixes so a weakened gate fails.

## 4. The contract release

- [x] 4.1 ALLOCATE THE BUNDLE NUMBER FRESH at this point — `contract-v1.41`
  only if the pending Unreleased block has not folded first. Re-count at the
  tip AND again at the landing squash; this repository has renumbered
  mid-flight more than once.
- [x] 4.2 CHANGELOG entry, `contracts/manifest.yaml` row and digest,
  `contract_bundle_version` bump, inventory rebuilt AFTER the bump, then the
  verify-commit. Per `docs/contract-versioning-policy.md`.
- [x] 4.3 NO TAG until the landing squash.
- [x] 4.4 Note the consumer re-pin: codexFactory pins this schema by digest.
  Additive, so a consumer may ignore the field, but the pin moves.

## 5. Validate green

- [x] 5.1 Gates: `pytest tests/ideation-dashboard`, `pytest
  tests/ideation_dashboard`, `pytest tests/doc-health`;
  `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`; doc-health zero-new
  against a fresh same-clock `origin/main` baseline;
  `scripts/validate-ideation-dashboard-contracts.py` at its baseline.
- [x] 5.2 Contract-release verification per the policy, including that the
  inventory was rebuilt after the version bump rather than before.

## 6. Bookkeeping

- [x] 6.1 README OpenSpec Records: move this change from active to archived
  when it archives. DONE 2026-08-29, in the archive commit itself: the row left
  the "Active changes:" list — where it still read "**NOT YET RATIFIED**
  (`Status: draft`)`", stale by five days and two rulings — and entered
  "Archived changes:" pointing at
  `openspec/changes/archive/2026-08-29-add-model-capability-vocabulary/`, with
  the realization recorded (PR #498, squash `8ccfb67b`, tag object `f86f2212`,
  sentinel resolved in `0b9e31c8`) and the promotion numbers stated. Evidence:
  `review/archive-verification-2026-08-29.md`.
- [x] 6.2 The staged topic keeps its row: this is exit (a) of three, and the
  topic exits only when (b) and (c) have landed too.

## 7. NOT part of this change

- Reading `modalities` to choose a destination. That is exit (b), which also
  inherits the pre-assembly request-bound constraint recorded in the topic's Q1
  disposition, and which must be sequenced against the ratified-but-unbuilt
  intake lane.
- Any further capability dimension. Audio, video, tool-calling, structured
  output, latency and cost enter only with a change that governs a consumer.
- Compression, disclosure, and the `reduced_reason` constant — exit (c).
