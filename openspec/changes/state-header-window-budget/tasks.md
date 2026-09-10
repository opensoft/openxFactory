# Tasks: state-header-window-budget

**House rule: OpenSpec ratifies, Speckit builds — never `opsx:apply`.**
`code_surface: none`, so there is no Group 2/3 realization gate the way a
code-surface change owes one: this packet's only obligations are authoring,
the standing validation gates, and — once ratified — an archive that is a
SEPARATE act this packet does not perform. **Group 0 is the ratification
gate, and putting the wording in front of Brett Heap for a ruling is the
only task here that needs his own hand.** (Group 3.1's archive also needs
Brett Heap's ratifying WORD, but — unlike Group 0 — is carried out
afterward by whichever lane holds that word, not performed by Brett
himself; the two are both human-gated, only one is human-performed.)

## Group 0 — RATIFICATION GATE (human; OPEN)

- [ ] 0.1 **Convener read of `design.md` § 0** (the four-line brief) and of
  `proposal.md` § Origin, which quotes both PR #906 comments in full.
- [ ] 0.2 **Rule on the added paragraph and scenario as drafted, or amend
  the wording.** The FACT is not in question — `design.md` D1 records an
  empirical re-verification on this branch, independent of the docstring's
  own word — so this box is a wording ratification and not a fact-finding
  one. `design.md` D2 records why the addition is a new paragraph rather
  than a reworded sentence, and D3 why the new scenario sits where it does.
- [ ] 0.3 On ratification: `Status: ratified` + a `Ratified:` line land in
  `proposal.md`, and the README "OpenSpec Records" entry moves from DRAFT to
  RATIFIED.

## Group 1 — openxFactory doctrine authoring (THIS change)

- [x] 1.1 Author `.openspec.yaml` — `kind: ad_hoc`, id
  `openxFactory:adhoc:2026-09-10-state-header-window-budget`, both PR #906
  comments cited by URL, the "fan out wide" resume ruling recorded as
  authorization-to-author and explicitly disclaimed as not a content
  ratification, the checked reason `kind: staged` is NOT taken
  (`ideation/staging/` listed and `INDEX.md` read 2026-09-10; the only
  "fence" hits are the unrelated staging-document markup fence), and three
  `related:` entries.
- [x] 1.2 Author `proposal.md`, quoting the Copilot finding and Brett Heap's
  reply on PR #906 in full rather than paraphrasing either, declaring this
  change's own `sequenced_after: [accept-sequenced-after-header-line]`, and
  recording the empirical re-verification (real line 19 behind a four-line
  fence refused; real line 15 behind the same fence read).
- [x] 1.3 Author the `release-realization` spec delta as a `## MODIFIED`
  block: one paragraph added, one scenario added, every existing sentence,
  bullet and scenario of the requirement carried verbatim (machine-diffed
  against the promoted spec after stripping the two additions — clean, task
  2.1 below), no `Removed from canon` or `Merged into` marker (nothing
  removed).
- [x] 1.4 Author `design.md` — § 0 convener brief, context, decisions D1–D4,
  risks, no open questions.
- [x] 1.5 **Sibling search, checked rather than assumed — CORRECTED
  2026-09-10 after Copilot found the original `find` command's depth bug.**
  The first pass ran
  `find openspec/changes -maxdepth 3 -path "*/specs/release-realization/*" -not -path "*/archive/*"`
  and read its empty result as "no other active change"; that command
  cannot reach `openspec/changes/<id>/specs/release-realization/spec.md`
  (four segments deep) at `-maxdepth 3`, so the empty result proved nothing.
  Re-run at the correct depth AND, after a second Copilot pass found this
  depth-corrected command also matched this packet's OWN delta file when
  run against this packet's own worktree (three paths, not two — a `find`
  has no "before filing" moment to self-exclude with, so the exclusion is
  an explicit path term instead),
  `find openspec/changes -maxdepth 4 -path "*/specs/release-realization/spec.md" -not -path "*/archive/*" -not -path "*/state-header-window-budget/*"`
  → TWO other active changes DO carry a `release-realization` delta
  (`add-sequenced-after-substrate`, `add-structured-scope-substrate`), but a
  `grep -n "^### Requirement:"` over both shows neither declares "Equivalent
  declaration sites for the ordered-delta parent declaration" — the
  requirement key this change writes — so the relevant claim (no OTHER
  active change writes THIS requirement key) still holds; the broader claim
  the first pass made ("no other active change carries a
  `release-realization` delta at all") did not, and is retracted.
  `gh pr list -R opensoft/openxFactory --state open --json number,title,files --jq '.[] | select(.files[].path | test("release-realization|frontmatter_strict"))'`
  → empty, checked BEFORE this pull request was filed (this pull request
  itself necessarily touches `release-realization`, so "no OTHER open pull
  request" is the claim, not "no open pull request" read literally).
  **Corrected 2026-09-10:** the earlier "re-checked at head `5252c37b`,
  still empty" was wrong — that bare command has no term excluding this
  pull request's own number, so a re-check taken AFTER filing necessarily
  matches #921 itself. Reproduced at head `7e31b2df`: exactly one match,
  #921 itself; excluded BY NUMBER, zero OTHER open pull requests remain.
  No ACTIVE-change collision on the requirement key, so no `Modified over`
  marker is owed. Ledger row `class: co-modifier`, partnered with
  `accept-sequenced-after-header-line` (its own row flips `sole` →
  `co-modifier` in the same re-seed, task 1.7) — correct, since both write
  the same requirement key; this is the ledger's documented partner-flip
  mechanic, not an active-change collision.
- [x] 1.6 List the change in the openxFactory README "OpenSpec Records"
  ACTIVE block, marked **DRAFT — RATIFICATION OWED**.
- [x] 1.7 **DONE, PR #921.** Seeded this change's row in the per-change
  sweep ledger via the sanctioned tool
  (`python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#921'`
  → "wrote tests/sequenced_after/corpus-ledger.yaml (195 rows, 2
  moved by #921)"), taken AFTER the pull request existed, on
  `accept-sequenced-after-header-line` task 4.5's own precedent. TWO rows
  moved, both correctly: this change's own new row
  (`state: active, class: co-modifier, declares:
  [accept-sequenced-after-header-line], depth: 3`), and
  `accept-sequenced-after-header-line`'s row flipping `sole` →
  `co-modifier` in the same commit — the ledger's own documented
  partner-flip mechanic, because that archived change's `## ADDED
  Requirements` block wrote the same requirement key this change's
  `## MODIFIED` block now also writes.

## Group 2 — Gates

- [x] 2.1 Machine diff: this delta's two additions stripped from
  `specs/release-realization/spec.md` and diffed against the promoted
  requirement in `openspec/specs/release-realization/spec.md` — CLEAN (one
  harmless trailing-blank-line artifact of the extraction method, no
  content difference).
- [x] 2.2 `OPENSPEC_TELEMETRY=0 <pinned openspec> validate
  state-header-window-budget --strict` → "Change 'state-header-window-budget'
  is valid", exit 0.
- [x] 2.3 `OPENSPEC_TELEMETRY=0 <pinned openspec> validate --all --strict` →
  **99 passed, 2 failed (101 items)**, exit 1 — vs a clean `origin/main`
  worktree's **98 passed, 2 failed (100 items)**, exit 1: exactly +1 passed,
  same 2 pre-existing failures on both sides
  (`change/add-chain-attestation`, `change/add-composed-view-authoring` —
  the two known ERROR-level marker-blind findings `prepare-openspec-1-12-readiness`
  already named), zero new failures introduced. **THIS COUNT IS A SNAPSHOT AT
  THIS TASK'S OWN AUTHORING HEAD, NOT A PINNED NUMBER, AND DRIFTS AS
  `origin/main` GROWS** — exactly as task 2.6 documents for the ledger row
  count; the invariant that is the actual gate is the relationship (branch =
  main + 1 item, the same two pre-existing failures, zero new ones), checked
  by a JSON diff of the two failing-item sets and not by the totals matching
  some fixed pair of numbers. Re-measured at head `8088d01e` (after merging
  `origin/main` `52e42be9`): **100 passed, 2 failed (102 items)** vs main's
  **99 passed, 2 failed (101 items)**. Re-measured again after this
  verification pass's own merge of `origin/main` `6f95ff57` (merge commit
  `3a7b3757`): branch **100 passed, 2 failed (102 items)**, a fresh
  `origin/main` clone at `6f95ff57` **99 passed, 2 failed (101 items)** —
  the two failing-item sets, taken from `validate --all --strict --json` and
  diffed by item id rather than eyeballed, are byte-identical
  (`{add-chain-attestation, add-composed-view-authoring}`) on both sides
  every time: zero new failures, at every head this packet has carried.
- [x] 2.4 `python3 -m pytest tests -q -k "sequenced or frontmatter or
  release_realization"` → **278 passed, 0 failed**, identical total to a
  clean `origin/main` worktree's 278 passed. (Before 1.7's seed this read
  274 passed / 4 failed — the four ledger-consistency tests, because this
  change's row did not yet exist; expected and resolved by the seed.)
- [x] 2.5 `python3 scripts/doc-health.py --single-repo . --family
  status-validity`, `--family record-immutability`, `--family
  ratified-provenance` (run separately — `--family` takes one choice, not a
  list) — all three exit 0; zero findings name any path under
  `openspec/changes/state-header-window-budget/` (`grep -c
  state-header-window-budget` on each family's output → 0). Extended
  2026-09-10 during re-verification: added `--family modified-block-currency`
  (the family that actually parses an active `## MODIFIED` block's prose,
  `design.md` § Risks) — exit 0, zero findings naming this packet, all four
  families; and, separately, a full `python3 scripts/doc-health.py
  --single-repo .` with NO `--family` filter — every family in one run —
  exit 0, zero findings naming this packet there either.
- [x] 2.6 `python3 scripts/validate-sequenced-after.py . --ledger-diff` →
  "per-change sweep ledger consistent with the corpus", exit 0, at this
  task's own authoring head (`13a7ee64`: 195 rows). THE ROW COUNT IS NOT
  PINNED AND DRIFTS as other lanes add or archive changes corpus-wide,
  independent of this packet — the exit code and the word "consistent" are
  the gate, not the number. Re-measured 2026-09-10 after the `origin/main`
  merge to `d32509d3` (head `d3f73dde`): 197 rows, still exit 0, still
  consistent; re-measured again after two further `origin/main` merges
  (heads `3a7b3757` then `6e80b7aa`, main at `6f95ff57` then `0e76e789`):
  198 rows, still exit 0, still consistent; the PR's own re-verification
  comments carry the count as of whichever head they were taken at.
- [x] 2.6a **Movement log entry, added 2026-09-10 on a Copilot finding**
  (review comment on THIS pull request, not on #906). Seeding this change's
  ledger row (task 1.7) flips `accept-sequenced-after-header-line` from
  `sole` to `co-modifier` — a PARTNER'S row moving because of this change's
  own delta, the reason not legible from the two rows alone — which
  `tests/sequenced_after/test_sweep.py`'s own MOVEMENT LOG rule (restated
  2026-09-03, quoted in that file) says an entry is owed for. Appended one,
  matching the file's own established narrative style (the 2026-09-03
  "PARTNER FLIP" and 2026-09-04 "TEN ROWS MOVED" entries): named the shared
  requirement key and the exact arithmetic (`co_modified` 143 -> 145,
  `sole_modifiers` 54 -> 53, `change_ids` 197 -> 198, `active` 40 -> 41,
  `active_co_modified` 25 -> 26, `active_sole` holds at 15), measured on
  both `origin/main` at `0e76e789` and this branch via
  `python3 scripts/validate-sequenced-after.py . --sweep`, not adjusted by
  hand. A docstring addition inside an existing test function: asserts
  nothing and changes no test's outcome — `proposal.md` § Impact.

## Group 3 — Archive (NOT this change's act — owed on ratification)

- [ ] 3.1 **Archive — owner: whichever lane holds Brett Heap's ratifying
  word**, per `release-realization`'s doc-only rule ("its code_surface is
  `none` and it archives when its artifacts land, as before"). This pull
  request is deliberately left OPEN/DRAFT and UNMERGED by the authoring
  session; archiving is a separate act on a separate word, exactly as
  `amend-neutral-product-pin-interim-copy-vocabulary` task 4.1 records for
  its own comparable packet.
