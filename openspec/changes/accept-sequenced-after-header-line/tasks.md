# Tasks: accept-sequenced-after-header-line

**House rule: OpenSpec ratifies, Speckit builds — never `opsx:apply`.** Group 1
is the authoring done BY this change. **Group 0 is the ratification gate and is
the only task here a human must perform.** Group 2 is the realization; it is
TICKED because this change's code surface is one reader whose proof is its own
suite, and holding a reader edit back from the packet that specifies it would
put the requirement and its only evidence in two different pull requests.
**NOTHING IS MERGED BY THIS CHANGE**, and nothing in codexFactory is touched:
its re-vendor and pin advance are Group 4, unticked, owned elsewhere.

## Group 0 — RATIFICATION GATE (human; OWED)

**OPEN. RATIFICATION IS OWED AND IS BRETT HEAP'S ACT.** Brett Heap's ruling of
2026-09-10 ~02:10Z, verbatim **"do door b"**, chose the DOOR between two named
alternatives on codexFactory #268. It did not ratify any text in this packet.

- [ ] 0.1 **Convener read of `design.md` § 0** (the ten-line brief).
- [ ] 0.2 **Rule the narrowing of the ratified sentence.**
  `add-sequenced-after-substrate`'s ADDED requirement says a "prose
  `Sequenced-after:` header … SHALL NOT constitute a machine-readable parent
  declaration". `proposal.md` § The ratified sentence this change narrows quotes
  it in full and answers its three reasons. **This is the packet's load-bearing
  ask: refuse it and nothing else here survives, and door (a) is the remaining
  door.**
- [ ] 0.3 **Rule OQ-H1 — the five carriers beyond the window** (codexFactory
  lines 20, 24, 33, 36, 38). Widen the window, or leave the bound?
  Recommendation: LEAVE THE BOUND.
- [ ] 0.4 **Confirm or veto OQ-H2** — `scope_globs:` stays untaught the
  header-line form. Recommendation: LEAVE IT OUT.
- [ ] 0.5 **Confirm or veto authoring decisions H-1 … H-7** (`design.md`
  § Decisions), including H-2's extension of the promoted real-lines rule's
  language-boundary escape clause to a VENDORING boundary.
- [ ] 0.6 On ratification: `Status: ratified` + a `Ratified by:` line + a
  `## Ratification record` section recording the dispositions land in
  `proposal.md`, and the README "OpenSpec Records" entry moves from DRAFT to
  RATIFIED.

## Group 1 — openxFactory doctrine authoring (THIS change)

- [x] 1.1 Author `.openspec.yaml` — `kind: ad_hoc`, id
  `openxFactory:adhoc:2026-09-10-accept-sequenced-after-header-line`, the ruling
  verbatim, the checked reason `kind: staged` is NOT taken
  (`ideation/staging/` listed and `INDEX.md` read 2026-09-10; no topic names
  declaration sites, unfenced front matter or header windows), the
  authorization-to-author disclaimer, and four `related:` entries.
- [x] 1.2 Author `proposal.md`, DECLARING this change's own
  `sequenced_after: [add-sequenced-after-substrate]` — the substrate's mechanism
  used by its first successor, on the substrate itself.
- [x] 1.3 Author the `release-realization` spec delta — **ALL-ADDED**, two
  requirements, seven scenarios.
- [x] 1.4 Author `design.md` — § 0 convener brief, context, decisions H-1 …
  H-7, risks, and open questions OQ-H1 / OQ-H2.
- [x] 1.5 **Check the vehicle rather than assume it.** Confirmed the substrate's
  requirements are NOT promoted (`grep -n "Machine-readable ordered-delta parent
  declaration" openspec/specs/release-realization/spec.md` → no output, exit 1),
  so a MODIFIED block over them is unavailable; confirmed both ADDED titles are
  NOVEL against the eight promoted `release-realization` requirements and every
  title in the five ACTIVE deltas on this capability, so no currency marker is
  owed and no sibling's archive-order hold is incurred.
- [x] 1.6 **Quote the ratified sentence this change narrows IN FULL**, with the
  three reasons it gives and what the admitted form does about each, rather than
  paraphrasing it into agreement.
- [x] 1.7 List the change in the openxFactory README "OpenSpec Records" ACTIVE
  block, marked **DRAFT — RATIFICATION OWED**.
- [x] 1.8 `openspec validate accept-sequenced-after-header-line --strict` and
  `--all --strict` pass under the repository's PINNED CLI.

## Group 2 — the reader (code_surface: openxFactory) — REALIZED IN THIS PULL REQUEST

- [x] 2.1 `scripts/frontmatter_strict.py`: `split_real_lines` (CR/LF/CRLF only),
  `fence_span`, `HEADER_WINDOW_LINES = 15`, `read_header_line`, and the
  `NO_HEADER_LINE` sentinel — distinct from `None`, which is a header line with
  no value (present-but-null), because presence is decided by the KEY on both
  reading paths.
- [x] 2.2 Convert `fenced_lines` to the shared real-line rule so the fence span
  and the header window agree about where a document's lines are, and MEASURE
  the conversion first: 372 `proposal.md` files across both clones (241 real
  corpus + 131 fixtures), zero differing fenced blocks.
- [x] 2.3 One fence rule for both readers: `fenced_lines` takes the lines INSIDE
  the span and the header-line scan starts AFTER it, so a field declared in the
  fence is read once and never counted a second time as a header line. Fence
  lines still COUNT toward the window — one window rule, the document's own.
- [x] 2.4 Refuse the block-sequence attempt BY NAME (a valueless `field:` line
  followed by an indented continuation), naming the two forms that work; refuse
  two header lines for one field as the duplicate key they are, by handing both
  matched lines to `strict_load` together so the message is the loader's own.
- [x] 2.5 `scripts/sequenced_after.py`: `read_header_line`, and
  `read_declaration` reading BOTH sites — equal under `_canonical` is ONE
  declaration, different is REFUSED with both values named, and absence from
  both is still `ABSENT`.
- [x] 2.6 Leave `scripts/scope_globs.py` UNTOUCHED (H-4) and ASSERT the
  asymmetry in the suite rather than leaving it to trust.
- [x] 2.7 `tests/sequenced_after/test_header_line.py`: the header-line form
  declares, resolves, validates and walks; beyond the window it is prose; the
  legacy `Sequenced-after:` still declares nothing; both-sites equal / different
  / root-contradicted; the loader's refusals reach the new path; the freeze
  cases; the two agreement tests; the `scope_globs` asymmetry; and a corpus test
  asserting openxFactory gains and loses no declaration.
- [x] 2.8 Prove the gates: `python3 scripts/validate-sequenced-after.py` → exit
  0 ("39 active changes, 9 declaring the field"); the targeted suite green with
  the pre-existing `trust-anchor` failures shown IDENTICAL on a clean
  `origin/main` worktree.

## Group 3 — the measurement (this change's own evidence)

- [x] 3.1 BEFORE/AFTER `corpus_sweep` over codexFactory main `2ade133` with the
  `origin/main` reader and this branch's reader: `declaring` 0 → 3, deepest
  chain 0 → 2 hops. Recorded in `proposal.md` § The measurement.
- [x] 3.2 Enumerate ALL EIGHT carriers with their real line numbers and state
  plainly which three the window admits and which five it does not — reported,
  not quietly dropped.
- [x] 3.3 Run `retention_at_archive` through the new reader against each
  admitted carrier's own ratified head: all three RETAINED, none contested —
  door (b)'s central claim, asserted as a measurement.
- [x] 3.4 **Correct #268's own "two late-added carriers" reading** with that
  measurement: it was taken through the fence-only reader, which returns ABSENT
  on both sides.

## Group 4 — SUCCESSORS (NOT this change's code surface; unticked with owners)

- [ ] 4.1 **codexFactory re-vendor + pin advance — lane codeXfactory-1.** In ONE
  commit: re-copy openxFactory `scripts/frontmatter_strict.py` and
  `scripts/sequenced_after.py` into `scripts/merge_master/`, refresh their
  entries in `VENDORED_SHA256` / `VENDORED_SOURCE_PATHS`, and advance
  `stack.yaml`'s `contract_ref` to the openxFactory commit carrying this change.
  Advancing the pin without re-copying reds
  `test_the_vendored_bytes_equal_the_source_at_the_pinned_contract_version`
  BY DESIGN.
- [ ] 4.2 **The #268 disposition — lane codeXfactory-1**, posted AFTER 4.1: the
  three admitted carriers with their RETAINED retention readings, and the five
  beyond the window named with their line numbers and left to an explicit act.
- [ ] 4.3 **The five beyond-window carriers — codexFactory, owner TBD at 0.3.**
  Only if OQ-H1 is ruled LEAVE THE BOUND. Moving a declaration INTO the window is
  a retention-gate mutation on a ratified packet and needs the same explicit
  recorded disposition door (a) would have needed; it is not a reformat.
- [ ] 4.4 **Other consumers' re-pins — their own lanes.** Any repository
  vendoring either module advances its own pin; none is advanced from here.
- [ ] 4.5 **Archive this change — lane codeXfactory-1**, on merged + green
  realization evidence per `release-realization`, after Group 0 closes. The two
  ADDED requirements promote to `openspec/specs/release-realization/spec.md` at
  that archive and not before.
