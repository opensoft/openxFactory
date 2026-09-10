# Tasks: state-header-window-budget

**House rule: OpenSpec ratifies, Speckit builds — never `opsx:apply`.**
`code_surface: none`, so there is no Group 2/3 realization gate the way a
code-surface change owes one: this packet's only obligations are authoring,
the standing validation gates, and — once ratified — an archive that is a
SEPARATE act this packet does not perform. **Group 0 is the ratification
gate and is the only task here a human must perform.**

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
- [x] 1.5 **Sibling search, checked rather than assumed.**
  `find openspec/changes -maxdepth 3 -path "*/specs/release-realization/*"
  -not -path "*/archive/*"` → no other active change. `gh pr list -R
  opensoft/openxFactory --state open --json number,title,files --jq '.[] |
  select(.files[].path | test("release-realization|frontmatter_strict"))'`
  → empty. Ledger row `class: sole`.
- [x] 1.6 List the change in the openxFactory README "OpenSpec Records"
  ACTIVE block, marked **DRAFT — RATIFICATION OWED**.
- [ ] 1.7 Seed this change's row in the per-change sweep ledger
  (`tests/sequenced_after/corpus-ledger.yaml`) via the sanctioned tool
  (`python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
  '#<this PR>'`), never hand-authored. **Deferred until the pull request
  exists**, on `accept-sequenced-after-header-line` task 4.5's own
  precedent: "taken AFTER the pull request existed, because the real number
  does not exist until it does."

## Group 2 — Gates

- [ ] 2.1 Machine diff: strip this delta's two additions from
  `specs/release-realization/spec.md` and diff the remainder against the
  promoted requirement in `openspec/specs/release-realization/spec.md` —
  MUST be clean (verified once already during authoring; re-run at the
  ratified head before archive).
- [ ] 2.2 `OPENSPEC_TELEMETRY=0 <pinned openspec> validate
  state-header-window-budget --strict` — exit 0.
- [ ] 2.3 `OPENSPEC_TELEMETRY=0 <pinned openspec> validate --all --strict` —
  totals compared against a clean `origin/main` worktree, no new failure.
- [ ] 2.4 `python3 -m pytest tests -q -k "sequenced or frontmatter or
  release_realization"` — exit 0, identical to a clean `origin/main`
  worktree (this packet changes no code any of those tests exercise).
- [ ] 2.5 `python3 scripts/doc-health.py --single-repo . --family
  status-validity,record-immutability,ratified-provenance` — 0 findings on
  this packet.
- [ ] 2.6 `python3 scripts/validate-sequenced-after.py . --ledger-diff` —
  clean after 1.7's seed.

## Group 3 — Archive (NOT this change's act — owed on ratification)

- [ ] 3.1 **Archive — owner: whichever lane holds Brett Heap's ratifying
  word**, per `release-realization`'s doc-only rule ("its code_surface is
  `none` and it archives when its artifacts land, as before"). This pull
  request is deliberately left OPEN/DRAFT and UNMERGED by the authoring
  session; archiving is a separate act on a separate word, exactly as
  `amend-neutral-product-pin-interim-copy-vocabulary` task 4.1 records for
  its own comparable packet.
