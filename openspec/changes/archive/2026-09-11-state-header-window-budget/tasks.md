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

## Group 0 — RATIFICATION GATE (human; CLOSED)

**CLOSED 2026-09-11T01:44Z.** Brett Heap (openxFactory operator authority;
sole operator), first-hand, in session, to lane `codexfactory-1` (window
`codeXfactory-1`), verbatim **"ratify 921"**, over verified head
`29f2211437b9f5e0fd9960f45e83f8ca8de91bb7`. Recorded on PR #921
([comment 5628429288](https://github.com/opensoft/openxFactory/pull/921#issuecomment-5628429288));
record `review/ratification-2026-09-11.md`.

**WHY TWO BOXES BELOW STAY UNTICKED THOUGH THE GATE IS CLOSED.** 0.1 and 0.2
are Brett Heap's OWN acts — the preamble above says so in as many words
("putting the wording in front of Brett Heap for a ruling is the only task
here that needs his own hand"). **No agent ticks an owner's box**, so neither
is ticked here; each carries a dated note recording what the word discharged,
which is evidence and not a substitute for his hand. 0.3 is different in
kind: it describes files changing, is performed by this lane, and is ticked
below — the same split `accept-sequenced-after-header-line` made at its own
ratification (`208f88d4`, box 0.6, identically worded).

**AND WHY BOTH ARE TICKED HERE, AT THE ARCHIVE — DISCHARGED BY THE WORD, NOT
PERFORMED BY AN AGENT.** The paragraph above is kept byte-unmoved because it
was true of the act it describes, the ratification encode, which correctly
left an owner's boxes alone. It was never the whole story, and § 3.1 below
said so before this act began: `scripts/proposal-support.py` `archive_change`
refuses on the FIRST `^- [ ]` anywhere in this file, so an archive either
closes these two or does not happen. **The distinction the paragraph draws
survives the tick intact**, because what each tick records is BRETT HEAP'S
OWN ACT — his ruling of 2026-09-11T01:44Z, verbatim *"ratify 921"* — and not
the archiving lane's. Nothing is invented and no disposition is minted here:
each box already carried, from the ratifying commit `8d5fb17e`, the dated
note naming exactly what that word discharged; this act adds the tick and
the citation to a disposition already written, on § 3.1's own standing
instruction. **NO OTHER BOX IS TOUCHED.** Three boxes were unticked at the
landed head `7099fbdd` — 0.1, 0.2 and 3.1 — and they are exactly the three
§ 3.1 names; no fourth box exists whose completion would have to be invented,
and none is marked `[~]` because nothing is being deferred.

- [x] 0.1 **Convener read of `design.md` § 0** (the four-line brief) and of
  `proposal.md` § Origin, which quotes both PR #906 comments in full.
  *(Discharged 2026-09-11T01:44Z by the word itself — "ratify 921" is a
  ruling on this packet, which the § 0 read precedes. Brett Heap's box; left
  unticked for him.)*
  **CLOSED AT THE ARCHIVE, 2026-09-11, AS DISCHARGED-BY-WORD.** The note
  above IS the disposition; this tick carries it and asserts nothing beyond
  it — in particular it does not claim that any agent performed a convener's
  read. The discharging act is Brett Heap's (openxFactory operator
  authority; sole operator), first-hand, in session, to lane
  `codexfactory-1` (window `codeXfactory-1`), **2026-09-11T01:44Z**,
  verbatim **"ratify 921"**, given over verified head `29f22114`; recorded
  on openxFactory PR #921 at
  [comment 5628429288](https://github.com/opensoft/openxFactory/pull/921#issuecomment-5628429288)
  (posted 2026-09-11T02:14:24Z) and durably at
  `review/ratification-2026-09-11.md`, and encoded in ratifying commit
  `8d5fb17e`. **The trailing clause *"left unticked for him"* described the
  state at that ratifying commit and is superseded HERE, at the archive, by
  § 3.1's own standing instruction — it is kept rather than edited so the
  ratification's posture stays legible to a later reader.**
- [x] 0.2 **Rule on the added paragraph and scenario as drafted, or amend
  the wording.** The FACT is not in question — `design.md` D1 records an
  empirical re-verification on this branch, independent of the docstring's
  own word — so this box is a wording ratification and not a fact-finding
  one. `design.md` D2 records why the addition is a new paragraph rather
  than a reworded sentence, and D3 why the new scenario sits where it does.
  **RULED 2026-09-11T01:44Z — AS DRAFTED, NOT AMENDED.** The word was the
  bare **"ratify 921"**: it names no wording to change, so the paragraph and
  the scenario are ratified exactly as the bench reviewed them. Verified by
  diff rather than asserted — `git diff 5dfa1831 HEAD --
  openspec/changes/state-header-window-budget/specs/` is EMPTY at the
  ratifying commit, so no byte of the delta moved between review and
  ratification. D1–D4 were carried beside it and none was vetoed.
  *(Brett Heap's box; left unticked for him.)*
  **CLOSED AT THE ARCHIVE, 2026-09-11, AS DISCHARGED-BY-WORD — same word,
  same citation as 0.1**, and for this box the word is not merely evidence of
  a read but the ruling itself: *"ratify 921"* IS the disposition this box
  asks for, and because it was BARE it ruled AS DRAFTED, amending no wording.
  That is verified by diff rather than asserted, twice over: the delta is
  byte-identical between the reviewed head and the ratifying commit (the
  clause above), and it is byte-identical again between the ratifying commit
  and the copy this archive promotes — `git diff 8d5fb17e HEAD --
  openspec/changes/state-header-window-budget/specs/` is EMPTY, so the words
  ratified are the words promoted. As with 0.1, the *"left unticked for him"*
  clause is kept unedited and is superseded here.

  **ONE DISCREPANCY IN THE RECORD, DISCLOSED RATHER THAN RECONCILED, BECAUSE
  AN ARCHIVE MAY NOT LAUNDER ONE.** Every artifact this repository carries
  stamps the word at **2026-09-11T01:44Z** — `proposal.md`'s `Ratified:`
  line, `.openspec.yaml` `origin.approved_by`, `review/ratification-2026-09-11.md`,
  the README record, and ratifying commit `8d5fb17e`'s own message. The
  authoring lane's contemporaneous handoff
  (`session-handoff-2026-09-05-lane-codeXfactory-1.md`, xFactory aggregation
  repo) carries **BOTH** stamps: its § 32 `WORD —` line reads
  `2026-09-11T02:02:14Z`, and its § 33 snapshot taken at 02:07:42Z reads
  *"ratify 921" 01:44Z standing*. The two differ by eighteen minutes. **The
  verbatim word, the authority, the recipient lane and the head it was given
  over (`29f22114`) are identical in every source; only the minute differs**,
  and no fact of the ratification turns on it. **NOTHING IS EDITED TO
  RESOLVE IT**: the four artifacts carrying `01:44Z` are a ratified proposal,
  a frozen origin declaration, a `Status: ratified` record and a landed
  commit message — `.openspec.yaml` is the origin-retention gate's own
  baseline and an edit there is a refusal, and the record is governed by
  `govern-archived-record-edits`. The archived text therefore stands at
  `01:44Z` and this note is the disclosure. A correction, if one is wanted,
  is a separate act on a separate word.
- [x] 0.3 On ratification: `Status: ratified` + a `Ratified:` line land in
  `proposal.md`, and the README "OpenSpec Records" entry moves from DRAFT to
  RATIFIED.
  **DONE 2026-09-11, in the ratifying commit.** `proposal.md` carries
  `Status: ratified` and EXACTLY ONE citation line, spelled `Ratified:` —
  the record-citing alternative, the legal spelling here because no
  approving OpenSpec change exists to name (`document-lifecycle` § Status
  Claim Rules) — naming an approver in the recognized `by <Name>` form, a
  date, the verbatim word, its UTC instant, the head it was given over, the
  PR comment and the record path. **THE CITATION SITS AT LINE 10, INSIDE THE
  FIFTEEN-LINE WINDOW COUNTED FROM LINE 1 WITH THE FRONT-MATTER FENCE'S FIVE
  LINES INCLUDED — this packet's own rule, applied to the packet that states
  it** — and the whole lifecycle header (fence, title, `Status:`, citation,
  `Authored:`) still closes inside that budget. Two further things the
  written rule requires land in this SAME commit: the ratification is ADDED
  to `.openspec.yaml` `origin.approved_by` beside the authorization-to-author
  provenance, which is byte-unmoved along with `kind`, `id`, `reason` and
  `approved_on` (`document-lifecycle` § *Proposal origin declaration* —
  "APPROVAL IS AN ADDITION, NEVER A REWRITE", "APPROVAL SHALL APPEAR WHEN A
  STATUS CLAIMS IT"; the archive gate reads this file's blob at the ratifying
  commit as its permanent baseline, so an addition made anywhere else is a
  mutation), and the durable record `review/ratification-2026-09-11.md` is
  captured beside the packet, carrying its own in-window citation. The README
  "OpenSpec Records" row moved DRAFT → RATIFIED.

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

- [x] 3.1 **Archive — owner: whichever lane holds Brett Heap's ratifying
  word**, per `release-realization`'s doc-only rule ("its code_surface is
  `none` and it archives when its artifacts land, as before"). This pull
  request is deliberately left OPEN/DRAFT and UNMERGED by the authoring
  session; archiving is a separate act on a separate word, exactly as
  `amend-neutral-product-pin-interim-copy-vocabulary` task 4.1 records for
  its own comparable packet.
  **READ THIS BEFORE RUNNING THE ARCHIVE — a trap found by Copilot review on
  2026-09-11 and verified in the code rather than taken on its word.** The
  house archive entrypoint REFUSES this packet in its present state:
  `scripts/proposal-support.py` `archive_change` runs
  `re.search(r"^- \[ \]", tasks.read_text(), re.M)` immediately after the
  origin arms and raises `SupportError("change has incomplete tasks")` on the
  FIRST unticked box anywhere in this file. Three boxes are unticked — **0.1**
  and **0.2**, Brett Heap's own acts, and **this 3.1**. That is the correct
  state *now*, and it is not a defect of the ratification: the ratifying lane
  deliberately did not tick 0.1/0.2, because no agent ticks an owner's box,
  and 3.1 is the archive act itself, which has not happened. **It becomes the
  archiving lane's first task**, on the archive word, before invoking the
  entrypoint: close 0.1 and 0.2 as discharged by the ratifying word of
  2026-09-11T01:44Z (each already carries the dated note recording what that
  word discharged), and tick 3.1 as the act being performed. Deferred work
  that is genuinely NOT being done at archive takes `[~]`, not `[x]` and not
  `[ ]` — the shape the prior archived packet used. **Do not discover this at
  the entrypoint.**

  **DONE — THIS ACT, 2026-09-11, lane `codexfactory-1` (window
  `codeXfactory-1`), archive pull request
  [#953](https://github.com/opensoft/openxFactory/pull/953), pre-staged as a
  DRAFT.** The trap
  above was read BEFORE the entrypoint ran and not discovered at it: 0.1 and
  0.2 were closed as discharged-by-word first, each on the dated note it
  already carried from `8d5fb17e`, and this box was ticked as the act being
  performed. **No box is marked `[~]`, because nothing is deferred** — the
  three unticked boxes at the landed head `7099fbdd` were exactly the three
  this note names, and no fourth existed.

  **THE ARCHIVE CONDITION, CITED RATHER THAN ASSERTED.** `proposal.md`
  declares **`code_surface: none`**, so under `release-realization`'s
  doc-only rule this packet archives **ON LANDING** — not on
  merged-plus-green realization evidence, which is the other arm and is the
  one the precedent PR #906 had to satisfy. The landing:

  | arm | evidence | value |
  | --- | --- | --- |
  | **RATIFIED** | Brett Heap, first-hand, in session, verbatim *"ratify 921"*, over head `29f22114`; encoded at `8d5fb17e`, recorded at `review/ratification-2026-09-11.md` and on PR [#921](https://github.com/opensoft/openxFactory/pull/921#issuecomment-5628429288) | 2026-09-11T01:44Z |
  | **MERGE WORD** | Brett Heap, first-hand, in session, verbatim *"merge 921"*, recorded in the lane handoff's § 32 `WORD —` line and acted on with the Rule 6 `LANDING` post on PR #921 ([comment 5629118605](https://github.com/opensoft/openxFactory/pull/921#issuecomment-5629118605)) | 2026-09-11T03:00:53Z |
  | **MERGED** | PR [#921](https://github.com/opensoft/openxFactory/pull/921) → `3ccfd6c3957bd49ef28e70ef984f13c3dc9d2c03` on `main`; `LANDED` posted at [comment 5629341902](https://github.com/opensoft/openxFactory/pull/921#issuecomment-5629341902) | 2026-09-11T04:11:24Z |
  | **ORIGIN RETAINED** | `origin_errors(strict=True)` → `[]` and `origin_retention_errors` → `[]`, printing *"ORIGIN RETAINED state-header-window-budget (declaration unchanged since the ratifying commit `8d5fb17e0eee`)"* — run on the landed packet BEFORE the move and again on the archived copy AFTER it | both clean |
  | **ARCHIVE WORD** | **GIVEN.** Brett Heap, first-hand, in session, to lane `codexfactory-1` (window `codeXfactory-1`), verbatim ***"archive 921"***. PR [#953](https://github.com/opensoft/openxFactory/pull/953) is the archiving act and lands on it. | **2026-09-11T10:21:39Z** |

  **THAT LAST ROW WAS BLANK WHEN THIS ACT WAS PREPARED, AND THE PREPARATION
  IS THE POINT.** The archive was performed, proved and frozen in a DRAFT
  pull request that did not flip READY, did not merge itself and posted no
  Rule 6 `LANDING`, because none of those was authorized yet. **The third
  word has since been given** — 2026-09-11T10:21:39Z, verbatim *"archive
  921"* — so this pull request now flips READY and lands on it, exactly as
  the ratification landed on *"ratify 921"* and the merge on *"merge 921"*.
  **Three acts, three separate words, each recorded before the act it
  authorizes rather than after it.** Nothing about the archive's content
  changed when the word arrived: the wrapper had already run, the promotion
  was already byte-proved, and the word authorized the LANDING and nothing
  else.

  **THE README RECORDS COLLISION OF 2026-09-11T03:43Z DID NOT REACH THIS
  PACKET'S BYTES, and is named here only so a reader need not re-derive it.**
  PR [#937](https://github.com/opensoft/openxFactory/pull/937)
  (`amend-repo-boundary-governance-scope-first-line`) merged at
  2026-09-11T03:43:30Z, thirteen seconds after this packet's own `LANDING`
  post, and the two collided in the README "OpenSpec Records" active list.
  It was resolved as a union — **both entries kept** — in merge commit
  `54e14d07`, whose own message says so. Measured rather than asserted:
  `git diff --stat 54e14d07^1 54e14d07 -- openspec/changes/state-header-window-budget/`
  is EMPTY. No byte of this packet moved in that resolution, so nothing
  about it is this archive's business beyond the README row it now moves.

  **PERFORMED THROUGH THE HOUSE ENTRYPOINT, NOT A BARE `openspec archive`.**
  `TZ=UTC python3 scripts/proposal-support.py . archive
  state-header-window-budget --date 2026-09-11 --yes`, which resolves the
  content-addressed pinned `@fission-ai/openspec@1.12.0` artifact, runs the
  origin shape and retention arms before it moves anything, validates the
  change `--strict` through the pin, and fixes the archive directory's date
  to UTC. **Its stdout, verbatim:**

  ```
  ORIGIN RETAINED state-header-window-budget (declaration unchanged since the ratifying commit 8d5fb17e0eee)
  proposal-support: @fission-ai/openspec@1.12.0 from the pinned artifact (…/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified, over the pinned dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages, lockfile_integrity sha512-aw5lIN45tQq2WZll…, installed with `npm ci --ignore-scripts`)
  openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (…/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
  openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
  -> …/node_modules/.bin/openspec validate state-header-window-budget --strict --json  (in …/openx-arch921)
  Totals: 1 passed, 0 failed (1 items)

  Proposal warnings in proposal.md (non-blocking):
    ⚠ Why section should not exceed 1000 characters
  Task status: ✓ Complete

  Specs to update:
    release-realization: update
  Applying changes to openspec/specs/release-realization/spec.md:
    ~ 1 modified
  Totals: + 0, ~ 1, - 0, → 0
  Specs updated successfully.
  Change 'state-header-window-budget' archived as '2026-09-11-state-header-window-budget'.
  OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
  NO SUPPORTING DOCS …/openspec/changes/state-header-window-budget (origin retained, nothing to package)
  ```

  **`~ 1 modified`, NOT `+ 1 added`, AND THAT IS THE WHOLE SHAPE OF THIS
  PACKET.** `release-realization` holds at **10 requirements** across the
  act; a `## MODIFIED` block rewrites one in place, where the predecessor
  `accept-sequenced-after-header-line`'s `## ADDED` block took the capability
  8 → 10. The write-back is **`18 added, 0 removed`** — measured, not
  asserted — in exactly two hunks: the 13-line paragraph (12 lines plus its
  separating blank) at the promoted file's line 446, and the 5-line scenario
  at line 488. **`git diff -w --numstat` EQUALS `git diff --numstat` at
  18/0**, so ZERO lines changed by whitespace alone: the pinned 1.12
  serializer's whole-file normalization did not recur here either.

  **THE PROMOTED REQUIREMENT IS BYTE-IDENTICAL TO THE ARCHIVED DELTA'S
  `## MODIFIED` BLOCK**, both extracted programmatically and hashed rather
  than eyeballed — **5,786 bytes, sha256
  `98e8280252ca4112ee130399bddc4f2b6dc1d25979f9f798e9625cae37db6e58`, on both
  sides.** (Raw extraction differs by ONE byte, a single trailing blank line
  that exists in canon because a further requirement follows the block and
  does not exist in the delta file because the block ends it; the figure
  above normalizes that one trailing newline on both sides. This is the same
  harmless extraction artifact task 2.1 recorded when it ran the inverse
  comparison at authoring time.) Before the act canon's copy of this
  requirement was **4,315 bytes**; the delta is a pure addition, so the
  growth is the paragraph and the scenario and nothing else.

  **AND WHAT WAS NOT TOUCHED IS MEASURED TOO.** The sibling requirement this
  same capability carries from the same predecessor packet, "One parent
  declaration across both sites, and its retention", hashes **2,720 bytes,
  sha256 `6e6f2225b5f700da8e314d4d7e47409aa8058b2bd596af1852903e8eb154bf11`**
  — identical on `origin/main` before the act and in canon after it. The
  requirement this packet amends goes from **four scenarios to five**; no
  scenario is renamed, reordered or dropped, which is why the delta carries
  neither a `Removed from canon` nor a `Merged into` marker. The spec-file
  COUNT under `openspec/specs/` is unchanged (no file added or removed), so
  no codexFactory review-authority-floor advance is owed by this act.

  **ALL SIX PACKET FILES MOVE AS PURE RENAMES.** `.openspec.yaml`,
  `proposal.md`, `design.md`, `tasks.md`, `specs/release-realization/spec.md`
  and `review/ratification-2026-09-11.md` go to
  `openspec/changes/archive/2026-09-11-state-header-window-budget/` at 100%
  similarity with ZERO changed lines — **except `tasks.md`, which changes
  here and only here, to record this act**. The ratification record is
  `Status: ratified` and is MOVED BY THIS ARCHIVE AND NOT EDITED BY IT; the
  origin declaration is frozen at ratification (openxFactory #709) and is not
  altered, which the retention arm re-confirms on the archived copy.

  **THE ORIGIN ARMS, RUN TWICE — ONCE ON THE LANDED PACKET BEFORE THE MOVE
  AND ONCE ON THE ARCHIVED COPY AFTER IT**, because the gate that matters at
  an archive is the one taken against the path the archive produces:
  `origin_errors(root, packet, strict=True)` → `[]` and
  `origin_retention_errors(root, packet)` → `[]`, printing **`ORIGIN RETAINED
  state-header-window-budget (declaration unchanged since the ratifying
  commit 8d5fb17e0eee)`** both times. The wrapper runs the same two arms
  itself, in that order, before it moves anything — its first stdout line
  above is that run.

  **THE ARCHIVE DIRECTORY'S DATE IS TODAY IN UTC, AND THE WRAPPER ENFORCED
  IT.** `--date 2026-09-11` was passed and the child ran under `TZ=UTC`, so
  `2026-09-11-state-header-window-budget` names the day the archive actually
  happened rather than the local day of whatever clock the pinned CLI reads
  (issue #790). **A merge on a later UTC day would make the directory name
  false and the archive would have to be re-dated instead** — so this pull
  request's landing, whenever the word comes, either falls on 2026-09-11 UTC
  or takes a re-dated directory.

  **THE PER-CHANGE SWEEP LEDGER IS RE-SEEDED IN THE FOLLOW-UP COMMIT, WITH
  THE SANCTIONED TOOL AND AFTER THE PULL REQUEST EXISTED**, because
  `moved_by` must name the pull request that moves the row and the real
  number does not exist until the pull request does — the two-commit shape
  the precedents PR #926 (`a0176d21`) and PR #906 (`fb5a9141`) used.
  `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
  '#953'` → *"wrote tests/sequenced_after/corpus-ledger.yaml (199 rows, 1
  moved by #953)"*. **ONE row moves and the diff is 1/1, measured:**
  `state: active → archived`, `moved_by: "#921" → "#953"`, `moved_on:
  "2026-09-10" → "2026-09-11"`. **`class: co-modifier` is HELD and NO
  PARTNER FLIPS, so no MOVEMENT LOG entry is owed** — this change's partner
  on the shared requirement key is `accept-sequenced-after-header-line`,
  already `archived` and already `co-modifier` since its own archive, so
  nothing about it moves; task 2.6a's entry covered the flip that DID happen,
  at the seed on PR #921, and this act repeats none of it. `--ledger-diff`
  before the seed: **STALE, 4 findings** — this row's `state` (ledger
  `active` vs live `archived`) plus the three derived totals it feeds
  (`active` 40 ≠ 39, `archived` 159 ≠ 160, `active_co_modified` 25 ≠ 24).
  After: **exit 0, *"per-change sweep ledger consistent with the corpus (199
  rows)"***. The row count is not pinned and drifts as other lanes land; the
  exit code and the word "consistent" are the gate.
