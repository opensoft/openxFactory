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
  EVERY field of the existing fourteen-field `Sweep`, with the sweep's own
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
- [x] 4.3 Turn the deepest-chain pin into a FLOOR (`>= 1`), and record why in
  `design.md` D4. THE EXACT DEPTH IS STILL PINNED — by the declaring change's
  own LEDGER ROW in the row-agreement test (`depth: 9` on that row fails it,
  naming row, key and both values), not by the deepest-chain test, whose second
  assertion reads `classify_corpus` and never opens the ledger and is therefore
  a self-consistency check on the fold rather than a ledger check. Labelled as
  such in that test's docstring.
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
  historical and are NOT rewritten (`design.md` D8). **`<sha>` IS THE HEAD
  `--ledger-diff` LAST RAN CLEAN ON, NOT `seeded_from`** — that field is the
  commit the file was FIRST seeded from, is preserved across re-seeds, and the
  ledger is provably inconsistent with the corpus at it (eleven findings at
  `995c0ad5`). Documented as history in the header's FILE KEYS block, and the
  ADDED requirement says the cited commit must be one at which the check was
  actually run and passed.
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

- [x] 6.1 **BOT ROUND 2 (Copilot), both findings TAKEN.** (a) `--seed-ledger`
  called `load_ledger` unconditionally when the file existed, so a MALFORMED
  ledger made the only tool that can rewrite it unusable on the only file that
  needed rewriting — it now says on stderr what it could not read and re-seeds
  from the corpus, stamping EVERY row (none of the old provenance was readable,
  so none can be preserved) and dropping `seeded_from` unless `--seeded-from` is
  given. (b) The usage text bracketed `--moved-by` as optional while the code
  refused without it — the usage line, the flag's help and the refusal now agree,
  and a fixture asserts the help text itself. Fixtures:
  `test_the_SEEDER_REPAIRS_a_ledger_too_malformed_to_READ`,
  `test_the_SEED_LEDGER_help_does_not_call_moved_by_OPTIONAL`. **Codex ABSENT
  again**: a second usage-limit refusal on the same request.

- [x] 6.2 **BOT ROUND 3 (Copilot), finding TAKEN ON ITS REAL CAUSE.** The
  finding named an uncaught `SequencedAfterError` from `--seed-ledger` on an
  unreadable existing ledger — that path was already repaired in round 2 and is
  clean (measured: it exits 0 with the stderr notice). But the SYMPTOM was real
  on two paths the finding did not name and this packet had not checked: a
  `--moved-by` or `--moved-on` the row grammar refuses reached
  `render_ledger`'s own validation and surfaced as a TRACEBACK. Argument shape
  is now refused by argparse at the boundary in its own voice, and
  `_seed_ledger` catches `SequencedAfterError` as a backstop, returning 2 with a
  message. Fixture:
  `test_the_SEEDER_REFUSES_a_bad_provenance_WITHOUT_a_traceback` asserts three
  bad inputs refuse with no `Traceback` in stderr.

- [x] 6.3 **BOT ROUND 4 (Copilot, 21:30:47Z), both findings TAKEN.** Both were
  posted as SUPPRESSED "previously missed" comments in the review body rather
  than as inline comments, so they are transcribed here. (a) The
  `test_sweep.py` docstring said the ledger pin was **"Ratified by
  `add-per-change-sweep-ledger`"** while the packet is `Status: draft`
  everywhere else — a ratification claimed in running code is worse than one
  claimed in prose, because it is what the next author copies. Now "Proposed by
  … admitted on the convener's ruling … `Status: draft` until ratified." (b)
  `--ledger-diff`'s usage text promised "the ledger-derived totals BESIDE the
  measured ones"; `_ledger_diff` prints one OR the other, never both. Text
  corrected to what it does.
- [x] 6.4 **BOT ROUND 5 (Copilot, 21:35:16Z), both findings TAKEN, and one was
  a real defect in the repair tool.** Likewise suppressed-body findings. (a)
  `_render_row` wrote `declares` entries UNQUOTED. A shape-refused declaration
  is still recorded as a declaration (only a strict-LOADER refusal reads as
  absence), so an entry can carry a comma or a bracket: `["a, b"]` read back as
  TWO entries and `["a] b: {c"]` did not parse at all — meaning `--seed-ledger`,
  **the documented repair tool**, could print "wrote" for a file `--ledger-diff`
  then called unparseable. Fixed twice over: `_render_entry` quotes any entry
  that is not a safe YAML plain scalar in a flow sequence (bare and
  repository-qualified ids stay plain, so the ordinary file is unchanged), AND
  `render_ledger` now ROUND-TRIPS its own output through `load_ledger` +
  `ledger_problems` before returning, so the renderer can never emit a file it
  cannot read back. (b) `--ratified-ref` was accepted in every mode and silently
  ignored outside `--archive-gate` — the same defect the mutually exclusive
  modes were introduced to remove. Every mode-scoped flag
  (`--ratified-ref`; `--moved-by`/`--moved-on`/`--seeded-from`) is now refused
  outside its mode with exit 2. Fixtures:
  `test_an_UNSAFE_declares_entry_is_QUOTED_and_reads_back`,
  `test_a_WELL_FORMED_entry_is_NOT_quoted_for_show`,
  `test_the_RENDERER_REFUSES_output_that_does_not_READ_BACK`,
  `test_a_FLAG_OUTSIDE_ITS_MODE_is_REFUSED_not_ignored`. **Codex ABSENT for a
  third request.**

- [x] 6.5 **BOT ROUND 6 (Copilot, 22:17:16Z), finding TAKEN.** `seeded_from` was
  interpolated into the header with HAND-ROLLED double quotes while
  `_render_entry` already had a safe strategy for exactly this. It is
  caller-supplied and — unlike `moved_by`/`moved_on` — NOT pattern-validated, so
  a value carrying a quote, a backslash or a newline produced a header the new
  round-trip then refused: a refusal caused by the RENDERER rather than by the
  input. Every scalar the renderer writes now goes through `json.dumps` (a JSON
  string is a valid YAML double-quoted scalar), including the pattern-validated
  pair — "safe because something upstream checked" is the reasoning that made
  `declares` unsafe, and one quoting strategy is easier to keep right than
  three. **The output is byte-identical for every valid value**: re-seeding the
  live ledger after the change rewrites it with no diff. Fixture:
  `test_a_SEEDED_FROM_carrying_YAML_metacharacters_still_reads_back`.

## Group 6b — Gates

- [x] 6b.1 `OPENSPEC_TELEMETRY=0 openspec validate add-per-change-sweep-ledger
  --strict` and `--all --strict`.
- [x] 6b.2 `python3 scripts/validate-sequenced-after.py .` (no flag) passes, and
  `--ledger-diff` exits 0 on the branch tip.
- [x] 6b.3 `python3 scripts/validate-sequenced-after.py . --sweep` output is
  unchanged from `main`'s, byte for byte, apart from the readings this
  packet's own directory and declaration move.
- [x] 6b.4 `python3 scripts/doc-health.py --single-repo .` stays clean of any
  new finding.
- [x] 6b.5 `python3 -m pytest tests/ -q -m "not postgres"` green.

## Group 7 — Archive preflight (after ratification)

- [ ] 7.1 Under `release-realization`'s realization archive gate, this packet
  archives on MERGED-PLUS-GREEN, measured after landing and never assumed.
- [ ] 7.2 Archiving moves this change's own ledger row `state: active` →
  `archived` — the row diff states it, so NO MOVEMENT LOG entry is owed for it,
  which is this change's own rule applied to itself.
