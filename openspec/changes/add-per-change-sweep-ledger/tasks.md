# Tasks: add-per-change-sweep-ledger

`code_surface: openxFactory`. Realizes the ADDED requirement "A pinned corpus
measurement is carried per subject, never as a shared total"
(`release-realization`).

## Group 0 — Convener gate

- [ ] 0.1 **RATIFICATION.** `Status: draft` until the convener ratifies. The
  2026-09-03 ruling admitted the packet and settled its shape; it did not
  ratify this text. The reading most worth a veto is `design.md` D1: that this
  delta is honestly ALL-ADDED rather than a `## MODIFIED` restatement of
  `add-sequenced-after-substrate`'s measured-bound requirement.

## Group 1 — The per-change derivation (Speckit feature `per-change-sweep-ledger`)

- [x] 1.1 Add `Reading` and `classify_corpus(repo_root)` to
  `scripts/sequenced_after.py`: change id → the per-change reading (`state`,
  `class`, `declares`, `depth`, `prose`), over the ACTIVE and ARCHIVED corpora
  both, making the same allowances `corpus_sweep` makes (an unreadable proposal
  declares nothing; a refused declaration reads as absence, a measurement not
  being a gate).
- [x] 1.2 Add `sweep_from_readings(readings) -> Sweep` folding the rows into
  EVERY field of the existing fifteen-field `Sweep`, with the sweep's own
  deepest-chain tie-break (strictly greater, ids in sorted order).
- [x] 1.3 **LEAVE `corpus_sweep` UNTOUCHED.** The derivation is independent so
  that their equality is a cross-check rather than a tautology (`design.md` D3).
- [x] 1.4 Add `sweep_mismatches(derived, measured)` naming the field and both
  values on a disagreement.

## Group 2 — The ledger file and its reader

- [x] 2.1 Define the ledger at `tests/sequenced_after/corpus-ledger.yaml`:
  `schema_version` + `kind`, a header comment carrying the row grammar, the
  re-seeding command and the record-citation rule, `seeded_from`, and `rows:`
  with ONE LINE per change id, sorted.
- [x] 2.2 `load_ledger` reads it through the strict loader's `StrictLoader`, so
  a DUPLICATE change id is refused by construction rather than resolved
  last-wins. The front-matter byte ceiling is deliberately not applied
  (`design.md` D5).
- [x] 2.3 `ledger_problems(readings, ledger)` reports, each NAMING the change
  id: a missing row, an extra row, a stale value (with the key, the ledger's
  value and the live one), an unsorted file, a malformed schema header, a
  malformed `moved_by`/`moved_on`, and an unknown key.
- [x] 2.4 `readings_from_ledger` converts the rows back into per-change
  readings, REFUSING a row too malformed to read rather than defaulting it — a
  defaulted row is an invented reading, and the ledger is what every later
  author reads. This is what makes "the totals are DERIVED from the rows"
  literal: the asserted totals are folded from THESE readings, not from a
  second classification of the corpus.
- [x] 2.5 `render_ledger` rewrites the whole file and PRESERVES the
  `moved_by`/`moved_on` of every row whose derived keys are unchanged, so a
  re-seed stamps only the rows that actually moved.

## Group 3 — The CLI

- [x] 3.1 `validate-sequenced-after.py --ledger-diff`: print the derived reading
  and every finding by name; exit 1 when stale. Unlike `--sweep` this IS a gate,
  a stale ledger being a stale pin rather than a measurement.
- [x] 3.2 `validate-sequenced-after.py --seed-ledger --moved-by '#PR'
  [--moved-on] [--seeded-from]`: rewrite from the live corpus. Kept as a
  permanent authoring tool, not deleted after seeding (`design.md` D6).
- [x] 3.3 `--sweep`'s output is unchanged, byte for byte.

## Group 4 — The test rewrite

- [x] 4.1 Replace the five live scalar assertions (and the four other scalar
  readings) with: the derived-vs-measured field-by-field equality; exactly-one
  row per corpus change id and no orphan rows, ids named; each row's keys equal
  the live reading, id + key + both values named; sorted order; and
  well-formed provenance on every row.
- [x] 4.2 KEEP every synthetic-corpus test that proves the counting method,
  unchanged.
- [x] 4.3 Turn the deepest-chain pin into a FLOOR (`>= 1`) plus agreement with
  the ledger's own deepest row, and record why in `design.md` D4.
- [x] 4.4 Fixtures for every failure shape, in the existing `tmp_path`
  synthetic-corpus style: row missing, extra row, stale `state`, stale `class`,
  a PARTNER flip naming both ids, unsorted ledger, malformed provenance,
  unknown key, duplicate row id refused by the loader, and derived totals ≠
  measured totals.
- [x] 4.5 The MOVEMENT LOG: every existing entry retained VERBATIM, the new
  rule stated at its head, and the dated seeding entry added naming the commit
  seeded from and this pull request.

## Group 5 — Seeding, docs and bookkeeping

- [x] 5.1 Seed the ledger mechanically from the live corpus at this branch's
  base commit, via `--seed-ledger`. This change's own directory is itself a
  corpus member, so its own row appears.
- [x] 5.2 State the record-citation rule (cite the row and
  "ledger ⇔ corpus consistent at `<sha>`", never a total) in `proposal.md`, the
  requirement, and the ledger's header comment. Records already written are
  historical and are NOT rewritten (`design.md` D8).
- [x] 5.3 Add the change's row to the README "OpenSpec Records" block (Active),
  and repoint the README's own scalar-pin prose at the ledger.
- [x] 5.4 `docs/sequenced-after-trust-root-floor.md` § The measured bound: name
  the ledger as where the per-change reading now lives, leaving the DATED
  2026-09-01 first-post-adoption table exactly as it stands — that section is
  explicitly a dated measurement and not a currency obligation.

## Group 6 — Review rounds

- [x] 6.0 **BOT ROUND 1 (Copilot), both findings TAKEN.** (a) The `--seed-ledger`
  summary counted rows whose `moved_by` already equalled the given pull request,
  so it reported UNMOVED rows as moved — fixed by extracting `moved_rows()`, the
  one place that decides whether a row moved, and having the renderer stamp by it
  and the CLI report from it, so the two cannot disagree. (b) The mode flags were
  combinable and the dispatch order silently picked one — `--archive-gate`,
  `--sweep`, `--ledger-diff` and `--seed-ledger` are now an argparse mutually
  exclusive group. Both carry fixtures
  (`test_MOVED_ROWS_names_exactly_the_rows_a_re_seed_moves`,
  `test_the_SEED_summary_counts_ONLY_the_rows_it_MOVED`,
  `test_the_CLI_MODES_are_MUTUALLY_EXCLUSIVE`). **Codex was ABSENT, not
  clearing**: it answered the review request with a usage-limit refusal.

## Group 6b — Gates

- [x] 6.1 `OPENSPEC_TELEMETRY=0 openspec validate add-per-change-sweep-ledger
  --strict` and `--all --strict`.
- [x] 6.2 `python3 scripts/validate-sequenced-after.py .` (no flag) passes, and
  `--ledger-diff` exits 0 on the branch tip.
- [x] 6.3 `python3 scripts/validate-sequenced-after.py . --sweep` output is
  unchanged from `main`'s, byte for byte, apart from the readings this
  packet's own directory and declaration move.
- [x] 6.4 `python3 scripts/doc-health.py --single-repo .` stays clean of any
  new finding.
- [x] 6.5 `python3 -m pytest tests/ -q -m "not postgres"` green.

## Group 7 — Archive preflight (after ratification)

- [ ] 7.1 Under `release-realization`'s realization archive gate, this packet
  archives on MERGED-PLUS-GREEN, measured after landing and never assumed.
- [ ] 7.2 Archiving moves this change's own ledger row `state: active` →
  `archived` — the row diff states it, so NO MOVEMENT LOG entry is owed for it,
  which is this change's own rule applied to itself.
