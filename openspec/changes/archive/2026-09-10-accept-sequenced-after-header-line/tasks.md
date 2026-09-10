# Tasks: accept-sequenced-after-header-line

**House rule: OpenSpec ratifies, Speckit builds — never `opsx:apply`.** Group 1
is the authoring done BY this change. **Group 0 is the ratification gate and is
the only task here a human must perform.** Group 2 is the realization; it is
TICKED because this change's code surface is one reader whose proof is its own
suite, and holding a reader edit back from the packet that specifies it would
put the requirement and its only evidence in two different pull requests.
**NOTHING IS MERGED BY THIS CHANGE**, and nothing in codexFactory is touched:
its re-vendor and pin advance are Group 4, unticked, owned elsewhere.

*(The paragraph above was TRUE AS AUTHORED AND AT RATIFICATION, and is kept as
the record of what this file claimed rather than rewritten: this change merged
as openxFactory PR #886 → `b91af6ea` on 2026-09-10T12:33:38Z, and Group 4's
successors have since landed in codexFactory. Read the paragraph below.)*

**AMENDED 2026-09-10, AT THE ARCHIVE — AND THIS IS THAT ACT.** Group 0 closed
at ratification; **0.4 and 0.5 close HERE** on the ruling already given, because
the archive gate refuses any `^- [ ]` box and the record's note-rather-than-tick
treatment cannot survive an archive (see each box for the citation, and that
neither closure invents a disposition). **Group 4 closes with THREE TICKS on
acts that landed in another repository** — codexFactory #333 → `8be1a855` (the
re-pin, 4.1), #268's disposition comment (4.2) and #331 → `36ecb9bc` (the four
pure moves, 4.3) — **ONE `- [~]` DEFERRED** with its owner named (4.4, other
consumers' re-pins) **and 4.5 ticked as this archive itself**. The realization
`release-realization` owes for a non-empty `code_surface` is recorded in
`evidence/realization-2026-09-10.md`, `Status: record`, with the decisive
byte-equality arm RE-RUN at this gate rather than quoted from #333.

## Group 0 — RATIFICATION GATE (human; CLOSED)

**CLOSED. RATIFIED 2026-09-10T11:31:31Z.** Brett Heap's earlier ruling of
2026-09-10 ~02:10Z, verbatim **"do door b"**, chose the DOOR between two named
alternatives on codexFactory #268 and did not ratify any text in this packet.
Ratification followed as a separate act: Brett Heap, repository owner,
first-hand, in session, to lane codexfactory-1, verbatim **"ratify 886, 0.2 as
narrowed, 0.3 pure moves"**, over head `f36d2bc2`. Record:
`review/ratification-2026-09-10.md`.

- [x] 0.1 **Convener read of `design.md` § 0** (the ten-line brief). DONE —
  evidenced by the ruling itself: 0.2, 0.3, 0.4 and 0.5 were all ruled at the
  same 2026-09-10T11:31:31Z sitting, which the § 0 read precedes. See
  `review/ratification-2026-09-10.md`.
- [x] 0.2 **Rule the narrowing of the ratified sentence.**
  `add-sequenced-after-substrate`'s ADDED requirement says a "prose
  `Sequenced-after:` header … SHALL NOT constitute a machine-readable parent
  declaration". `proposal.md` § The ratified sentence this change narrows quotes
  it in full and answers its three reasons. **This is the packet's load-bearing
  ask: refuse it and nothing else here survives, and door (a) is the remaining
  door.**
  **RULED 2026-09-10T11:31:31Z** — Brett Heap, first-hand, in session, to lane
  codexfactory-1, verbatim **"ratify 886, 0.2 as narrowed, 0.3 pure moves"**:
  AS NARROWED. The substrate's sentence stands, narrowed to the legacy prose
  `Sequenced-after:` spelling; the strict, schema-validated `sequenced_after:`
  header line inside the fifteen-line window DOES declare — exactly the
  reading this proposal admits. See `review/ratification-2026-09-10.md`.
- [x] 0.3 **Rule OQ-H1 — the five carriers beyond the window** (codexFactory
  lines 20, 24, 33, 36, 38). Widen the window, or leave the bound?
  Recommendation: LEAVE THE BOUND.
  **RULED 2026-09-10T11:31:31Z** — same word as 0.2, verbatim **"…0.3 pure
  moves"**: PURE LINE MOVES. The bound stands (the window is not widened); the
  five out-of-window carriers are resolved by pure line moves of their
  existing `sequenced_after:` line into the window (the codexFactory #323
  shape — pre-image and post-image are the same multiset of lines), no text
  change, no fencing. Successor: task 4.3, owner lane codeXfactory-1 in
  codexFactory, after the re-pin (task 4.1). See
  `review/ratification-2026-09-10.md`.
- [x] 0.4 **Confirm or veto OQ-H2** — `scope_globs:` stays untaught the
  header-line form. Recommendation: LEAVE IT OUT.
  **CONFIRMED AS THE PACKET STATES IT, ratified 2026-09-10T11:31:31Z by
  "ratify 886"; box CLOSED AT THE ARCHIVE 2026-09-10.** No separate word was
  given and none is invented: `review/ratification-2026-09-10.md` § "0.4 and 0.5
  — ratified as they stand, not separately ruled" records that *"ratify 886"
  ratifies the packet at head `f36d2bc2` as a whole, including the two open
  questions and seven decisions the packet itself already resolved with a stated
  recommendation and no dissent recorded against them*. The box asked for a
  CONFIRM-OR-VETO; the packet-level ratification is the confirmation, and no
  veto was entered. The recommendation is what shipped —
  `scripts/scope_globs.py` is untouched and the asymmetry is ASSERTED in the
  suite (task 2.6). The record says tasks.md marks this with a note "rather than
  a tick"; that treatment was right while the packet was active and cannot
  survive the archive, whose gate refuses any `^- [ ]` box with no bypass flag
  (`scripts/proposal-support.py … archive`). Closing it here changes no
  disposition and adds no ruling — it records the one already given.
- [x] 0.5 **Confirm or veto authoring decisions H-1 … H-7** (`design.md`
  § Decisions), including H-2's extension of the promoted real-lines rule's
  language-boundary escape clause to a VENDORING boundary.
  **CONFIRMED AS THE PACKET STATES THEM, ratified 2026-09-10T11:31:31Z by
  "ratify 886"; box CLOSED AT THE ARCHIVE 2026-09-10**, on the same record
  section and for the same reason as 0.4 immediately above. H-1 … H-7 stand as
  written in `design.md` § Decisions, no veto entered against any of them.
- [x] 0.6 On ratification: `Status: ratified` + a `Ratified by:` line + a
  `## Ratification record` section recording the dispositions land in
  `proposal.md`, and the README "OpenSpec Records" entry moves from DRAFT to
  RATIFIED.
  **DONE 2026-09-10T11:31:31Z.** `proposal.md` carries `Status: ratified` and a
  `Ratified:` line — not `Ratified by:`, because no approving OpenSpec change
  exists to name; the ratifier is a first-hand human ruling, the second of
  `document-lifecycle`'s two sanctioned citation spellings — citing this
  record in a separate file, `review/ratification-2026-09-10.md` (the
  `pin-openspec-cli-dependency-closure` shape), rather than an inline
  `## Ratification record` section. The README "OpenSpec Records" entry is
  moved DRAFT → RATIFIED.

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

## Group 4 — SUCCESSORS (NOT this change's code surface)

**CLOSED AT THE ARCHIVE, 2026-09-10, AND THE EVIDENCE IS RE-RUN RATHER THAN
INHERITED.** Three of these five boxes are ticked on acts that LANDED in another
repository, each cited by pull request and merge commit; one is `- [~]`
DEFERRED with its owner named; the last is this archive itself. The realization
this packet's `target_release` owes is recorded in
`evidence/realization-2026-09-10.md` (`Status: record`) — merged
(openxFactory #886 → `b91af6ea`), green (10 of 10 required checks), and READ BY
A CONSUMER (codexFactory #333 → `8be1a855`), with the decisive byte-equality arm
run here rather than quoted.

- [x] 4.1 **codexFactory re-vendor + pin advance — lane codeXfactory-1.** In ONE
  commit: re-copy openxFactory `scripts/frontmatter_strict.py` and
  `scripts/sequenced_after.py` into `scripts/merge_master/`, refresh their
  entries in `VENDORED_SHA256` / `VENDORED_SOURCE_PATHS`, and advance
  `stack.yaml`'s `contract_ref` to the openxFactory commit carrying this change.
  Advancing the pin without re-copying reds
  `test_the_vendored_bytes_equal_the_source_at_the_pinned_contract_version`
  BY DESIGN.
  **DONE 2026-09-10T16:09:02Z** — codexFactory
  [#333](https://github.com/codeXfactory/codexFactory/pull/333) →
  `8be1a855325e89b6b0ea943db130ba4724089580` on that repository's `main`.
  `stack.yaml` `xfactory.contract_ref` `724a2a4f` → `b91af6ea`,
  `contract_declared_at` `"2026-09-10"`, and **all four** vendored rows
  re-copied byte-for-byte in the same commit (one `source_contract_ref` covers
  all four captures, so a partial advance reds three rows by design). The arm
  this box warns about was RE-RUN AT THIS GATE with an openxFactory checkout
  supplied — `OPENXFACTORY_ROOT=… pytest tests/merge-master/test_vendored_sequenced_after.py
  tests/merge-master/test_vendored_scope_globs.py -q` → **84 passed, exit 0, 0
  skipped** — where the same file without that checkout reports `19 passed, 1
  skipped`, the skip being that very test. Evidence § 3.
- [x] 4.2 **The #268 disposition — lane codeXfactory-1**, posted AFTER 4.1: the
  three admitted carriers with their RETAINED retention readings, and the five
  beyond the window named with their line numbers and left to an explicit act.
  **DONE 2026-09-10T16:20Z** — posted on codexFactory
  [#268](https://github.com/codeXfactory/codexFactory/issues/268)
  ([comment 5621865823](https://github.com/codeXfactory/codexFactory/issues/268#issuecomment-5621865823)),
  after #333 merged. It carries the three carriers' RETAINED readings against
  their own ratified heads, all five beyond-window carriers with their real line
  numbers and what became of each (four moved, one reverted), and the one-corpus
  two-reader sweep. The issue itself closed **COMPLETED at
  2026-09-10T16:09:04Z** with #333's merge, two seconds after the merge commit —
  so the disposition was posted to a closed issue deliberately, because a
  closure is not a record of why.
- [x] 4.3 **The five beyond-window carriers — codexFactory, owner TBD at 0.3.**
  Only if OQ-H1 is ruled LEAVE THE BOUND. Moving a declaration INTO the window is
  a retention-gate mutation on a ratified packet and needs the same explicit
  recorded disposition door (a) would have needed; it is not a reformat.
  **DONE 2026-09-10T13:49:20Z, AND ITS CONDITION WAS MET** — OQ-H1 was ruled
  LEAVE THE BOUND with the remedy PURE LINE MOVES (task 0.3), so this box became
  live; owner resolved at that ruling to lane codeXfactory-1. codexFactory
  [#331](https://github.com/codeXfactory/codexFactory/pull/331) →
  `36ecb9bcca97c87e280a24ad5b8b57a1d7826c6f` moved **FOUR** of the five
  (`amend-floor-regeneration-merge-authority` 24→3,
  `relocate-review-authority-floor` 33→3,
  `admit-hosted-artifact-to-contract-manifest` 36→3,
  `add-mcp-transport-adapters` 38→3), each a pure move whose pre-image and
  post-image are the same multiset of lines — no text change, no fencing — under
  the explicit disposition this box demands, Brett Heap's *"0.3 pure moves"*.
  **THE FIFTH WAS RULED AND THEN REVERTED, and this box reports that rather than
  rounding to five**: `archive/2026-09-05-add-floor-addition-grace` (line 20) was
  restored byte-for-byte at `cd3eb14` on Brett Heap's word, first-hand, in
  session, 2026-09-10, verbatim **"merge 401, revert the archived line in 331"** —
  an archived packet is a record, and a parent proposal does not need to declare
  against one to stay valid. Net effect, measured: the sweep over codexFactory
  `main` `8be1a855` reads **8** declaring where the old pin read **0**
  (evidence § 4).
- [~] 4.4 **DEFERRED 2026-09-10, AT THE ARCHIVE — OPEN, OWNED ELSEWHERE, AND NOT
  CLAIMED.** *Other consumers' re-pins — their own lanes. Any repository
  vendoring either module advances its own pin; none is advanced from here.*
  **Owner: each consuming repository's own lane** (Medx / Ledgerx / Adx / Ops),
  on its own pin cadence. **Why deferral is honest and not a shortcut:** the
  requirement is realized once ANY consumer reads the site, and one does —
  codexFactory, at `b91af6ea`, proven in evidence § 3 and § 4; no other
  repository's clock is this packet's to advance, and none has been asked to.
  The marker says the box is OPEN and says who owns it; it does not say the work
  is done. It takes the reserved `- [~]` rather than `- [x]` because
  `scripts/proposal-support.py … archive` refuses any packet whose `tasks.md`
  still matches `^- [ ]` with no bypass flag, and buying that refusal off with a
  false tick is the one thing an archive must not do.
- [x] 4.5 **Archive this change — lane codeXfactory-1**, on merged + green
  realization evidence per `release-realization`, after Group 0 closes. The two
  ADDED requirements promote to `openspec/specs/release-realization/spec.md` at
  that archive and not before.
  **DONE 2026-09-10 — THIS ACT.** Group 0 closed at 2026-09-10T11:31:31Z; the
  realization gate's two arms are recorded in
  `evidence/realization-2026-09-10.md`. Performed through the house entrypoint
  `python3 scripts/proposal-support.py . archive accept-sequenced-after-header-line`
  (origin-retention arm, ratified-proposal arm and the pinned CLI, no bypass
  flag), moving the packet to
  `openspec/changes/archive/2026-09-10-accept-sequenced-after-header-line/` and
  writing BOTH ADDED requirements into
  `openspec/specs/release-realization/spec.md` — verified byte-identical to the
  archived delta by sha256 over each extracted block, with the promoted
  `## Purpose` untouched. README's "OpenSpec Records" row moves ACTIVE →
  ARCHIVED and the per-change sweep ledger row moves `state: active` →
  `archived`.
