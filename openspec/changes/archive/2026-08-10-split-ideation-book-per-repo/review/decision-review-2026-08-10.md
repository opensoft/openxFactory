# Cross-model decision review: split-ideation-book-per-repo

Status: record
Date: 2026-08-10
Protocol: standing cross-model review of architect rulings (reviewer model ≠
deciding model). Deciding seat: architect (Fable 5). Reviewer: Opus, blind
worktree at the pre-commit authoring state, one pass, positions forced per
decision.

## Decisions under review

- D1 split shape: one Ideation book per governed repository
- D2 alias scheme `xf-ideation-<repo-slug>`; legacy alias retired, never repointed
- D3 lazy creation on first ideation membership
- D4 capacity-guard semantics
- D5 Working Drafts / Canon stay single; guard names the owed delta
- D6 migration via normal reconciliation sync, then legacy retirement

## Verdicts

All six: `agree_insufficient` (no `agree`, no `disagree`) — direction
affirmed, first-draft wording would not have achieved its goals. Per the
asymmetric-signal rule, the absence of `disagree` is weak evidence; the
specific insufficiencies were verified against the tree and are strong.
Severities: D3, D4, D6 high; D2 medium-high; D1, D5 medium.

## Confirmed failures and dispositions (all fix_now, folded into this authoring commit)

1. D1/D5 — measured post-split load was absent (openxFactory ideation ≈ 212
   docs > the 188 the capped book held; its book opens ≈ 216/300), and the
   owed-remedy rule was a two-name denylist. → Proposal states the honest
   sizing; the guard's owed-delta naming is closed-world over any book
   without a defined successor split.
2. D2 — `nlm` aliases are machine-local CLI state; alias-addressed sync dies
   on any other host/CI. Tags were never applied by any code path; created
   books would silently leave `nlm cross query --tags` scope. Retirement
   breaks suites binding the legacy key/alias (notebooklm sync tests;
   ideation-dashboard set-removal conformance). → Title-based resolution
   with idempotent non-fatal alias re-registration; tags + framing seeded at
   creation; binding suites and possible companion delta named in tasks.
3. D3 — the create scenario ignored dry-run-by-default (create-on-preview
   vs. die-on-missing-alias, both wrong); "membership" would have counted
   grounding seeds, creating books for repos with zero ideation docs;
   `nlm notebook create` has known CLI drift solved once in the workbench
   adapter; a refused create aborted the whole run. → Apply-gated creation
   with dry-run reporting; membership excludes seeds; centralized adapter
   reuse; refused-create contained per book.
4. D4 — "projected membership" missed the charter (the off-by-one that
   reproduces the incident at exactly 300) and deliberately-preserved
   unmanaged sources; the excess set was undefined (path-sort churn); the
   cap had no named operand. → Occupancy = managed + charter + observed
   unmanaged; deterministic in-cap prefix with exact excess; cap as a named
   constant recorded in the doc; headroom warning restated as ≤ 30 sources
   (scale-independent lead time) instead of a percentage.
5. D6 — the migration (roughly 345 source operations at ~2s each) exceeds
   the ~20-minute nlm session; the manifest wrote once at end-of-run, so a
   dead run resumed as delete+re-add of everything; the legacy book stayed
   a sync target during migration while over-cap, making a green run
   unachievable by construction; count-parity was weak evidence. →
   Sequenced per-book migration with fresh auth, per-book manifest flush,
   legacy book leaves the book set at implementation, parity by title-set
   equality reconciled against the corpus scan.
6. Outside D1–D6, adopted: `external_source_workspace` records written at
   creation and retired with the legacy book; manifest re-keying with the
   stale `ideation` key dropped; dynamic `--book`; grounding fan-out cost
   acknowledged in the proposal.

## Declined (judgment, recorded for the ratifier)

The reviewer offered two remedies for the warn-to-ratified-split gap:
fixed-headroom warning OR pre-authorizing the mechanical split of a warned
book in this delta. The headroom warning was adopted; pre-authorization was
DECLINED — it would move a book-identity decision (contract surface under
"Projection implementation ownership") out of the ratify gate. Brett may
overrule at ratification; the tension is real on the openxFactory ideation
book, which opens at ≈ 216/300.
