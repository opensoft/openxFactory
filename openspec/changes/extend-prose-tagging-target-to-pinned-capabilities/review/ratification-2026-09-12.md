# Proposal Ratification: extend-prose-tagging-target-to-pinned-capabilities

Status: ratified
Kind: report
Decision date: 2026-09-12
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-09-12 at approximately 23:20Z by Brett Heap (openxFactory
repository owner) — FOUR SELECTIONS, not typed sentences, made via the
lane's interactive multi-choice — one question per `tasks.md` § 1 task: the
options "Ratify 1.1 as filed (Recommended) / Ratify 1.2 as filed / Ratify
1.3 as filed (Recommended) / Confirm 1.4 as filed (Recommended)" —
first-hand, in session, lane `openxfactory-2` (display `openXfactory-2`),
recorded on openxFactory #992 (comment
https://github.com/opensoft/openxFactory/issues/992#issuecomment-5649359053).
Confirmed: the SAME word and the SAME act, recorded a second time, verbatim,
for the lane's status thread — one act, two records, and not a second
decision, recorded on openxFactory #745 (comment
https://github.com/opensoft/openxFactory/issues/745#issuecomment-5649359201).

## Decision

RATIFIED AS FILED, by Brett Heap.

## The word, and exactly what it ratifies

Brett Heap's instruction was FOUR SELECTIONS:

> **"Ratify 1.1 as filed (Recommended) / Ratify 1.2 as filed / Ratify 1.3 as filed (Recommended) / Confirm 1.4 as filed (Recommended)"**

— 2026-09-12 at approximately 23:20Z, first-hand, in session, lane `openxfactory-2` (display
`openXfactory-2`), recorded on openxFactory
[#992](https://github.com/opensoft/openxFactory/issues/992) (comment
https://github.com/opensoft/openxFactory/issues/992#issuecomment-5649359053).

**AS FILED, WITH NO AMENDMENT AND NO VETO. The word carries no condition on
any later act and reopens no decision.**

**THE HEAD THIS RATIFIES.** The commit `dafe8877e4c8f2d3a52cbe94307904b639b7bece` (2026-09-12T23:16:13Z),
openxFactory pull request
[#994](https://github.com/opensoft/openxFactory/pull/994) — this
packet's text at the head the word was given over, with every fix round
encoded. No text this packet carries at that head is excepted from the
ratification: `proposal.md`'s account of the four `tag-hygiene` findings and
why no edit clears them honestly, `design.md`'s decisions, the two `## MODIFIED`
spec deltas against `document-lifecycle` and `doc-health`, and every scenario
and task the packet states.

## What is ratified

The proposal as written at `dafe8877e4c8f2d3a52cbe94307904b639b7bece`, and the decisions `design.md`
carries:

- **D-1 — the FORM.** An `xspec:candidate` marker's `target=` may be
  `pinned:<pin-id>/<capability>`, where `<pin-id>` is the stem of a
  `contracts/<pin-id>-pin.yaml` record, the value is EXACTLY TWO
  `[a-z0-9]+(-[a-z0-9]+)*` components separated by EXACTLY ONE `/`, and a value
  that fails that grammar is refused BEFORE any path is built or any file is
  read. D-1.1: the `xspec:supersedes` marker's `spec=` attribute is OUT OF
  SCOPE and CLOSED — a `spec=` value carrying the reserved `pinned:` prefix is
  refused.
- **D-2 — the RESOLUTION RULE.** The pin id must resolve to a
  neutral-product pin record this repository carries, of
  `kind: pinned_contract_manifest` (`kind: pinned_workflow` is EXCLUDED —
  five of the six pin records qualify today), COMPLETE for its RECORD SHAPE
  against that shape's SHAPE-GUARD-REQUIRED SET — the top-level members its
  in-tree verifier refuses-when-absent in its pure, source-free guards,
  pinned to those guards by a two-leg equivalence test and NECESSARY, by
  design, without being SUFFICIENT for the record's full verifier — rather
  than a member list this grammar writes down, judged through a CODE-FIXED
  route (one shared, pure, non-executing adapter) that never executes,
  imports or opens a path a pin record selects — `verify_pin:` is
  data that route may compare, never a resolution prerequisite — and
  resolved under the same root precedence the in-tree arm already uses,
  whose `contracts` directory must itself be a real, non-redirecting
  directory before any candidate path is read. The
  capability segment is checked for shape and resolved further ONLY where
  the pin record enumerates capabilities, through the ONE reserved member
  `capabilities:` — reserved by this change and ADDED TO NO RECORD AND NO
  SCHEMA BY IT. This is the packet's one live constitutional question
  (Principle VII) and `design.md` states the tension in full.
- **D-3 — the STALE-TARGET RULE.** When a target capability exits the corpus
  the marker either takes the pinned form or the block is unfenced — never
  silently retargeted, never silently deleted.
- **D-5 — the REALIZATION SPLIT.** ONE later pull request carries the resolver
  arm, its tests, the four retargeted markers, the `docs/document-lifecycle.md`
  section and the stale `ideation/staging/INDEX.md` line together, rather than
  four separate ones.

**BOXES TICKED BY THIS RATIFICATION: 1.1, 1.2, 1.3, 1.4.** Boxes none in
`tasks.md` § 1 stay OPEN and are not ticked by this record — a box ticks on the
word that answers it and on nothing else.

## What this ratification does NOT do

- **NO REALIZATION.** No byte of `scripts/doc_health/families.py` moves, no
  module is added under `scripts/doc_health/`, and no byte of
  `scripts/validate-pin-registrations.py` or of any per-product pin
  verifier moves. No marker is retargeted or deleted.
  `docs/document-lifecycle.md` is not touched. `ideation/staging/INDEX.md`
  is not touched. No pin record gains a `capabilities:` member and no
  schema admits one. The four `error`-band `tag-hygiene` findings stand at
  FOUR, unchanged. Realization is a LATER pull request in this same
  repository, on a separate word.
- **NO ARCHIVE.** `code_surface` is non-empty (`scripts/doc_health/families.py`
  and its tests), so under `release-realization` this packet archives only on
  merged-plus-green realization evidence — not on this ratifying commit. Every
  box in `tasks.md` § 3 and § 4 stays unticked.
- **NO TICK OF ITEM (7) OF THE `split-openxwallet-repo` ARCHIVED-LEDGER ENTRY.**
  That owed successor discharges on ARCHIVE, not on ratification. The archived
  packet is not edited at all, under the archived-record rule.
- **NO MERGE.** This record ratifies text at one head. Landing the pull request
  that carries this ratifying commit is a SEPARATE act under this repository's
  Rule 6 landing-window protocol, because this change touches
  `openspec/changes/`.

## Records

- Governing issue, and the finding this packet answers: openxFactory
  [#992](https://github.com/opensoft/openxFactory/issues/992),
  § 4 "The ask" — the ratifying word's comment (https://github.com/opensoft/openxFactory/issues/992#issuecomment-5649359053).
- The lane's status thread: openxFactory [#745](https://github.com/opensoft/openxFactory/issues/745) — where the same word, in the same act, was recorded a second time,
  verbatim (https://github.com/opensoft/openxFactory/issues/745#issuecomment-5649359201).
- The packet this ratifies: openxFactory pull request
  [#994](https://github.com/opensoft/openxFactory/pull/994), landed
  `dafe8877e4c8f2d3a52cbe94307904b639b7bece`, 2026-09-12T23:16:13Z.
- The cause: `openspec/changes/archive/2026-08-28-split-openxwallet-repo/` —
  its `tasks.md` measured the four findings, rejected both mechanical fixes and
  named this grammar extension as the honest one; its README archived-ledger
  entry carries the owed successor as numbered item (7), UNTICKED by this act.
