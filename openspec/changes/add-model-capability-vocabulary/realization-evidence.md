# Realization evidence — add-model-capability-vocabulary

**REALIZED 2026-08-29 as `contract-v2.2`.** This file is task 2.4's record: the
two behaviour changes stated as behaviour changes, the corpus check they oblige
before landing, and the reproduction table each fix was decided from. The
CHANGELOG entry for `contract-v2.2` is the published version of the same facts;
this file is the working record, including the things a CHANGELOG entry has no
place for.

The change does NOT archive with the cut. It carries a code surface, so the
archive gate (`docs/release-realization-flow.md`) wants the merge and a green
run first; §6.1 stays open until then.

## The bundle number, fresh-counted

`contract-v1.41` — the number §4.1 speculated about and then told the realizer
not to trust — was gone long before this ran. Counted at the branch base
(`3ffd6a8f`) and again before the landing squash:

* `contracts/CHANGELOG.md` top entry: `contract-v2.1`, 2026-08-28.
* `contracts/releases/`: v1.32–v1.47, v2.0, v2.1 all present.
* `git tag`: every one of those published, `contract-v2.1` included.
* No Unreleased block pending (`grep -i unreleased` finds only historical
  prose in older entries).

So the next available additive number is **`contract-v2.2`**, and this cut takes
it. The packet's own warning was well earned: the speculated number was seven
releases and one major stale.

## The six gaps, REPRODUCED before they were closed

Probed against the real type at the branch base, one value past each released
bound, before a line of the fix existed:

| field | released bound | probe | at `3ffd6a8f` | after |
| --- | --- | --- | --- | --- |
| `model_id` | `maxLength: 128` | 129 chars | ACCEPTS | refused |
| `model_id` | pattern | `'has space'` | ACCEPTS | refused |
| `label` | `maxLength: 200` | 201 chars | ACCEPTS | refused |
| `provider_class` | `maxLength: 64` | 65 chars | ACCEPTS | refused |
| `data_handling` | `maxLength: 500` | 501 chars | ACCEPTS | refused |
| `models` (catalog) | `maxItems: 64` | 65 entries | ACCEPTS | refused |
| `resolved_model_id` | `maxLength: 128` + pattern | 129 chars | already refused | unchanged |

That last row is why the widening was cheap: `_require_model_reference` already
existed, already worked, and is REUSED for `model_id` rather than respelled.

## §2.4 — the corpus check, run before landing

The two behaviour changes refuse constructions that succeeded before. Both were
already unservable over the wire, so what moves is WHERE they fail — but the
ratification's first conscious-acceptance note obliges checking the existing
corpus and fixtures rather than discovering it in a gate.

Every `kind: workbench-model-catalog` instance in the repository was parsed and
each entry measured against all five string bounds, the `model_id` pattern and
the catalog entry count:

```text
catalog instances scanned: 22
violations: NONE
```

The suites are the second half of that check, since the fixtures construct
through the real type rather than through YAML. NO FIXTURE NEEDED A VALUE
CHANGED. Three assertions did move, and each is a pin advancing with a release
rather than a fixture being made to fit:

* the packaged-positive COUNT, 14 → 15, for the new declaring example;
* two projection assertions that read `DECLARABLE_ENTRY_FIELDS` where they meant
  "the base seven then the routing three" — true while there was exactly one
  optional group, and false the moment there were two. The entry declaring BOTH
  groups now carries the `DECLARABLE_ENTRY_FIELDS` assertion, so nothing is
  lost.

## §1.1 — why the schema, not only the type, requires `text`

`minItems: 1` plus an item enum accepts `modalities: [image]`. The type and the
standalone validator both refuse that instance, so a schema-only consumer would
have treated as conformant a catalog every other gate rejects — the WIRE GATE
THE WEAKEST ONE, in the release whose second requirement is about that
divergence pointing the other way. `contains: {const: text}` is what closes it,
and `negative/workbench-model-catalog-modality-image-only.negative.yaml` is the
packaged proof that the shape itself refuses it.

## §2.1b — the wire projection, proved at the route

`as_public_dict` emits an explicit key list, so nothing about projecting a new
field is automatic. The claim that a declared set REACHES THE WIRE is therefore
proved by a real request through the real route and the real released-schema
validation, not only at the projection:
`tests/ideation-dashboard/test_doxbench_routes.py::test_a_declared_modality_set_REACHES_THE_WIRE_and_silence_does_not`.
The same test asserts the other half — an entry that declares nothing serves
exactly the seven base fields, byte-identical across the boundary.

## §3.3 — the revert-tests, both directions

Run against the candidate, one reverted edit at a time, each restored afterwards
and `__pycache__` purged between runs. The suite under each is
`test_doxbench_model.py` + `test_doxbench_contracts.py` (330 passing when
whole), plus `test_doxbench_routes.py` where the route is the thing being
proved. MEASURED, not predicted:

| # | reverted | measured |
| --- | --- | --- |
| R1 | the entry-count cap removed from `ModelCatalog.__post_init__` | **3 failed**, 327 passed |
| R2 | `_require_model_reference("model_id", …)` → `_require_non_blank_str` | **9 failed**, 321 passed |
| R3 | the three `_require_bounded_str` calls → `_require_non_blank_str` | **4 failed**, 326 passed |
| R4 | `MAX_CATALOG_ENTRIES = 64` → `65` (constant drifts from the schema) | **2 failed**, 328 passed |
| R5 | `LABEL_MAX_LENGTH = 200` → `201` | **2 failed**, 328 passed |
| R6 | `modalities` dropped from `as_public_dict` | **4 failed**, 494 passed (with the route suite) |
| R7 | `contains: {const: text}` removed from the schema, all three digest sites re-synced so the revert is isolated | **1 failed**, 106 passed, AND the packaged validator went to `1 error(s)` |

Restored: **330 passed**, working tree clean apart from this file and the ticked
`tasks.md`.

BOTH DIRECTIONS, which is the whole point of the pins. R1–R3 and R6 weaken the
TYPE and the behaviour proofs catch them. R4 and R5 leave every behaviour proof
GREEN — a type enforcing 65 refuses nothing a test asks it to refuse — and are
caught only by the released-bytes pin. Neither direction would have caught the
other, which is why the `MAX_ROUTING_TARGETS` precedent carries both and why
this release copies it rather than settling for behaviour tests.

R7 is the same idea one level out: the schema's own clause is what refuses
`modalities: [image]`, so removing it has to fail the vocabulary pin AND the
packaged negative — and it does both, the second as a validator error rather
than a test failure, which is where a schema-only consumer would have been
misled.

## What is NOT here

Reading `modalities` to choose a destination — exit (b). No route, selector or
browser file changed in this cut, which is what let this exit land without
touching the ratified-but-unbuilt intake lane.
