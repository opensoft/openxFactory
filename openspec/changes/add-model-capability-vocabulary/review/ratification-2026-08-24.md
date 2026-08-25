# Proposal Ratification: add-model-capability-vocabulary

Status: ratified
Decision date: 2026-08-24
Ratifier: Brett Heap (repository owner) — in-session via question prompts
Ratified: 2026-08-24 by Brett Heap (repository owner) — in-session via question prompts
Ratified baseline: this change as committed in the ratification commit carrying
this record (proposal.md, design.md, tasks.md, .openspec.yaml,
specs/ideation-dashboard/spec.md — 2 ADDED requirements), validated `--strict`
and `--all --strict`.

## Decision

Two rulings in the one read, recorded separately because they are not the same
act:

1. **RATIFY.** The requirement set stands: one optional, closed `modalities`
   declaration on `$defs/model_entry` — exactly `text` and `image`, extended
   only by the change that governs a new member — plus the rule that the
   catalog type enforces the bounds its released schema declares.
2. **THE PARITY SCOPE IS ALL FIVE.** Every string bound the released schema
   declares gets type-side enforcement in THIS release. No residue, no named
   follow-up.

Ruling 2 overrode the proposal's own recommendation, and the override is the
better call. The proposal had closed two bounds and recorded three more as a
follow-up, reasoning that the topic's batching obligation named exactly two and
that quietly growing two into five was the opposite of deciding each one. That
reasoning protected a process boundary at the cost of shipping a capability
whose parity requirement was true only in part. Brett widened the scope
instead, which makes the requirement checkable rather than aspirational.

The change carries `target_release: implementation_pending`. Realization runs
post-ratification and CUTS A CONTRACT BUNDLE — schema bytes move — so this
record authorizes that realization; it does not perform it, and no bundle
number is allocated by it.

## The five bounds, reproduced before the ruling was encoded

Each was probed against the real type at the ratification commit, one character
past the released bound:

| Field | Released bound | Probe | Type-side before |
| --- | --- | --- | --- |
| `model_id` | `maxLength: 128` | 129 chars | ACCEPTS — gap |
| `model_id` | pattern | `'has space'` | ACCEPTS — gap |
| `label` | `maxLength: 200` | 201 chars | ACCEPTS — gap |
| `provider_class` | `maxLength: 64` | 65 chars | ACCEPTS — gap |
| `data_handling` | `maxLength: 500` | 501 chars | ACCEPTS — gap |
| `resolved_model_id` | `maxLength: 128` + pattern | 129 chars, `'has space'` | already refuses |
| `models` (catalog) | `maxItems: 64` | 65 entries | ACCEPTS — gap |

`resolved_model_id` is the fifth string-bounded field and is ALREADY enforced,
through `_require_model_reference`. That is the evidence the widening is cheap:
the pattern exists, works, and is reused rather than respelled.

## Pre-ratification review

A bot round ran on PR #298 before this read. Three findings, all verified
against the repository and all taken (commit `f5738746`).

- **The parity requirement over-promised.** It claimed the type refuses every
  catalog the released schema would refuse while the tasks closed only two
  bounds. Verified: `label`, `provider_class` and `data_handling` all accept
  over-length values. Taken by narrowing the requirement and naming the
  residue — and then SUPERSEDED by ruling 2 above, which removes the residue
  instead. The finding is what surfaced the scope question that Brett then
  ruled.
- **The schema would have accepted `modalities: [image]`.** `minItems` plus an
  item enum does not encode required `text` membership, so a schema-only
  consumer would have treated as conformant an instance the type and the
  standalone validator both refuse — the wire gate weaker than the type gate,
  in a change whose second requirement is about that divergence pointing the
  other way. Task 1.1 now requires `text` membership in the schema itself.
- **The declaration would never have reached the wire.**
  `ModelCatalogEntry.as_public_dict()` emits an explicit key list rather than
  serializing the dataclass, so a declared `modalities` would have been
  validated in process and silently dropped by `GET /workbench/model-catalog`
  — leaving consumers and the routing successor with nothing to read, which is
  the entire purpose of the field. Task 2.1b projects it, following the
  present-only-when-declared idiom the routing fields already use so an
  undeclared entry's bytes stay byte-identical across the release boundary.

## Conscious-acceptance notes (Brett, at ratification)

1. **Construction failures that did not exist before will exist after.** Every
   bound closed here refuses a value that constructs today. All were already
   unservable over the wire, so what changes is WHERE they fail, not whether —
   but the realization must check the existing corpus and fixtures before
   landing rather than discovering it in a gate.
2. **The vocabulary is two members, and that is deliberate.** `image` has a
   named near-term consumer and nothing else does. Audio, video, tool-calling,
   structured output, latency and cost class enter only with a change that
   governs a consumer, on the roster's admission-surface rule.
3. **The bundle number is not allocated by this ratification.** It is
   `contract-v1.41` only if the pending Unreleased block has not folded first,
   and it is fresh-counted at realization — this repository renumbered
   mid-flight three times last sprint.
4. **This is exit (a) of three.** Fit-aware routing (b) and compress-to-fit
   disclosure (c) are named successors. (b) inherits a constraint recorded in
   the topic's Q1 disposition — request bytes are bounded before assembly
   against the selected entry — and must be sequenced against the
   ratified-but-unbuilt intake lane, which (a) deliberately avoids.

## Next

Realization per tasks §1–§5, directly, carrying the full contract-release
ritual: fresh-counted allocation, manifest row and digest, bundle bump,
inventory rebuilt after the bump, verify-commit, the catalog digest repinned
everywhere it is mirrored, and no tag until the landing squash.
