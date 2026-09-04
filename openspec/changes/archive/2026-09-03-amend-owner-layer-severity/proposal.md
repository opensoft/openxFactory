---
code_surface: none — this change's whole diff is governance text: two spec deltas restating already-promoted requirements, this proposal, its design, its tasks, its origin declaration, its ratification record, the promotion of both deltas into `openspec/specs/workflow-gate-contract/spec.md` and `openspec/specs/release-surface-integrity/spec.md`, and one README record row. **NOT ONE LINE OF `scripts/validate-domain-factory.py` MOVES**, and that is the whole point of the change rather than an omission from it: canon comes to the validator, which has reported this condition as an error since `493fb33d` (2026-07-03). No script, workflow, schema, contract or runtime artifact moves, in this repository or any other. Nothing under `contracts/` changes, so no bundle is cut and no digest set moves. TWO LIVE CORPUS PINS MOVE AS BOOKKEEPING RATHER THAN AS A CODE SURFACE, named here rather than left to a diff: `tests/doc-health/test_modified_block_currency_self_gate.py`'s carriage-ledger population and `tests/sequenced_after/test_sweep.py`'s live sweep. Both COUNT THE CORPUS, so both move whenever any change is AUTHORED — a fact about this packet's existence, not about its subject — and each is moved in this change's own commit with a dated note, which is those pins' own stated protocol.
target_release: promotion-only — the corrected text reaching canon IS the release; archives on landing (`code_surface: none`), per `release-realization`'s doc-only default rather than the merge-plus-green gate.
Status: ratified
Ratified: 2026-09-03 by Brett Heap (repository owner) — in-session, verbatim: "implement your recommendations on all these", given over the lane's written recommendations for issues #561 and #339 among others, and recorded VERBATIM as the latest comment on both issues. Record: `review/ratification-2026-09-03.md`.
Proposed: 2026-09-03
Origin: openxFactory issue #561 (the canon/validator severity divergence, commissioned by `retire-hermes-flat-keys-and-openworkflow-tokens` tasks § 6.1) and openxFactory issue #339 (three retro-published bundles left standing in the present tense), the second folded into this packet by the same ruling.
---

# Proposal: amend-owner-layer-severity

## Why

**Promoted canon and the shipped validator disagree about a severity, and they
have disagreed since before the requirement was promoted.**
`workflow-gate-contract`'s *"Owner layer constraint"* says an `owner_layer`
matching neither a canonical role nor a declared layer id *"SHALL be reported
as a validator warning"*. It was promoted at `a1a2802b` on 2026-07-09.
`scripts/validate-domain-factory.py`'s `check_workflows` has reported that same
condition with `rpt.error` since `493fb33d` on 2026-07-03 — **six days BEFORE**
the requirement that names it a warning existed. This is not a regression
against canon; canon was written after the code and did not match it on the day
it landed.

**Why it was filed rather than fixed at the time.**
`retire-hermes-flat-keys-and-openworkflow-tokens` (ratified 2026-09-01, PR
#551) met the divergence while retiring the `openworkflow`-prefixed token
branch that used to shadow the general rule, recorded it as its **D4**, and
deliberately declined to resolve it: resolving it moves every unresolvable
`owner_layer` token in every domain repository at whatever severity is ruled,
which is a strictly larger subject than a four-line retirement and one that
packet had no measurement to support. Its `tasks.md` § 6.1 commissioned issue
#561 so the record would survive that packet's fate, and the requirement it
added names the fall-through's severity as *"whatever the general rule
carries"* precisely so this change can move it without reopening that row.

**The measurement was taken before the ruling, and it makes either direction
free.** Ran at `96b2b968` against the five supported DomainxFactory consumers:
**zero gates carry an `owner_layer` that resolves to nothing** — codexFactory,
MedxFactory, LedgerxFactory, OpsxFactory and AdxFactory alike. No consumer is
refused whichever text moves, and no deprecation phasing is owed. The full
table is in `design.md` § *The measurement*.

**The ruling.** Brett Heap, 2026-09-03, in-session over the lane's written
recommendation — "implement your recommendations on all these", recorded
verbatim on issue #561: **canon moves to ERROR.** It matches the behaviour
every consumer has conformed to since 2026-07-03, keeps the stricter gate, and
costs a doc-only change. Relaxing the validator to `warning` would loosen a
conformance gate nobody asked to loosen.

**And the same ruling folded in issue #339**, which had been queued for
whichever change next opened a delta against `release-surface-integrity`. That
capability's requirement *"The declared bundle describes the release surface"*
justifies its tag-free reference point with a live example — `contract-v1.33`,
`contract-v1.35` and `contract-v1.39` *"are recorded in the changelog and the
manifest with no published tag"* — and all three were retro-published on
2026-08-25 by PR #333. The present tense has been false since. **The rule the
sentence illustrates is untouched and still exactly right**: a declared bundle
need not have a tag, so the inventory FILE at the commit is the reference. Only
the illustration went stale, and PR #333 already settled the treatment for the
identical claim in `scripts/doc_health/release_inventory.py`'s docstring — it
DATED the examples rather than deleting them, keeping the rule's provenance.
The same treatment is applied here.

## What Changes

- **`workflow-gate-contract` — "Owner layer constraint" says ERROR.** The body
  clause becomes "any other value SHALL be reported as a validator error", and
  the one scenario's `**THEN**` bullet becomes "the validator MUST report an
  error identifying the gate and the unknown layer". **Those two words are the
  entire diff against canon** — proven by word-diff in `tasks.md` § 2, not
  asserted. The canonical role list, the `stack.yaml` layer-id clause and the
  scenario's `**WHEN**` bullet are restated byte-for-byte.
- **`release-surface-integrity` — the retro-published bundles are past-tensed and
  DATED.** One paragraph of the requirement body: the three bundles "were each
  recorded in the changelog and the manifest with no published tag for weeks —
  the state this rule was written against — so a rule anchored on a tag would
  have been unevaluable for them; they were retro-published on 2026-08-25 (PR
  #333), and the rule stands on the general fact rather than on those three."
  The sentence that carries the rule — the inventory FILE at the commit is the
  reference, present whenever the bundle is declared — survives with only the
  tense-driven rewrap. Every other paragraph and all four scenarios are
  restated byte-for-byte.
- **No severity, threshold, vocabulary or check anywhere else moves**, and no
  requirement is added, removed or renamed.

## What does NOT change, stated because a reader will assume otherwise

- **The validator.** `scripts/validate-domain-factory.py` is not opened by this
  change. Its `rpt.error` fall-through is the behaviour canon is being brought
  to, and editing it would perform the OPPOSITE of the ruling.
- **The `openworkflow`-prefixed compatibility branch**, which is retired by
  #551's realization at `contract-v3.0` and is not reopened here. That packet's
  Executed row states the fall-through's severity as "whatever the general rule
  carries" so that this change could move it without touching that row, and
  this change does not touch it.
- **Any consumer's contracts.** Zero gates are refused by this amendment
  because zero gates carry an unresolvable token; the change moves text, not
  state.
- **The `contract-v1.33` / `v1.35` / `v1.39` records themselves.**
  `contracts/CHANGELOG.md`, `contracts/manifest.yaml` and the
  `contracts/releases/` inventories are untouched: they are the record of what
  was declared, and the illustration is corrected where the illustration lives.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `workflow-gate-contract`: *"Owner layer constraint"* reports an unresolvable
  `owner_layer` at ERROR, the severity the canonical domain-factory conformance
  validator has applied since 2026-07-03.
- `release-surface-integrity`: *"The declared bundle describes the release
  surface"* states its untagged-bundle illustration in the past tense with the
  2026-08-25 retro-publication dated, keeping the rule it justifies intact.

## Impact

- openxFactory: one clause and one scenario bullet in
  `openspec/specs/workflow-gate-contract/spec.md`; one body paragraph in
  `openspec/specs/release-surface-integrity/spec.md`; one README record row;
  this packet.
- Behaviour: **none.** Every supported consumer has conformed to the error
  severity since 2026-07-03, and the three bundles have carried published tags
  since 2026-08-25. Both deltas move text to where the world already is.
- Promotion fidelity: this change becomes the latest archived writer of both
  requirements the moment it archives, so that family measures IT against canon
  from then on. It must read — and does read — zero findings for openxFactory.
- Realization gate: promotion-only; `code_surface: none`, so this change
  archives on landing with no separate realization evidence.
