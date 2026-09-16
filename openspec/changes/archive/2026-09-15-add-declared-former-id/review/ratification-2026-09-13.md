# Proposal Ratification: add-declared-former-id

Status: ratified
Kind: report
Decision date: 2026-09-13
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-09-13T22:48Z by Brett Heap (openxFactory repository owner),
verbatim: *"ratify 1028 as encoded"* — a MULTIPLE-CHOICE ruling over all five
decisions `design.md` D1 through D5 put for the owner, given first-hand in lane
`openxfactory-1`'s window, recorded on PR #1028 at 2026-09-13T22:48:34Z
([issuecomment-5656710037](https://github.com/opensoft/openxFactory/pull/1028#issuecomment-5656710037)),
mirrored on issue #1003 at 2026-09-13T22:48:36Z
([issuecomment-5656710187](https://github.com/opensoft/openxFactory/issues/1003#issuecomment-5656710187)),
and recorded in full here.

**THE WORD TAKES THE RECOMMENDATION ON EVERY ONE OF THE FIVE: D1 = (a),
D2 = (a), D3 = (a), D4 = (a), D5 = (a).** Each is the option the packet already
encoded, so **THE DELTA'S WORDING STANDS UNCHANGED AND NOTHING WAS SUBSTITUTED,
RESTORED OR DELETED.**

## 1. The word, and what it reaches

**"ratify 1028 as encoded" IS A SINGLE MULTIPLE-CHOICE RULING OVER FIVE
DECISIONS, NOT FIVE SEPARATE WORDS.** It was given at 2026-09-13T22:48Z in
answer to the standing question this pull request had put — ratify-as-encoded,
land-as-draft, or a per-decision veto — and it is recorded verbatim, with that
instant, on every document this ratification touches: `proposal.md`,
`design.md`, `tasks.md`, `.openspec.yaml` (`approved_by`/`approved_on`, ADDED
BESIDE the unmoved `proposed_by`/`proposed_on` pair the
`add-drafted-proposal-origin` (issue #318) shape defined), the README OpenSpec
Records entry, and this record.

**THE RATIFIED TEXT IS THE TEXT FROZEN AT `1e57643d`.** The word names that
head — *"the packet `add-declared-former-id` as FROZEN at head `1e57643d` is
ratified with EVERY design.md decision at its RECOMMENDED option […] The
ratified wording is the wording at `1e57643d`; nothing is re-authored."* That
head is the one the lane FROZE at 2026-09-13T07:04:25Z
([issuecomment-5651836101](https://github.com/opensoft/openxFactory/pull/1028#issuecomment-5651836101)),
with sixteen review threads and zero unresolved.

**THE INSTANT IS RECORDED TO THE PRECISION IT WAS TAKEN AT AND NO FINER.** The
word is stamped `2026-09-13T22:48Z`; the RECORDING of it on the pull request
carries the second (`22:48:34Z`) and is cited as the recording time, which is a
different fact from the instant the word was given. `tasks.md` § 1.2 required
the instant "as GIVEN (never invented)", and writing a false `:SSZ` onto the
word itself to make the stamp look machine-produced would be inventing
evidence.

**THE RATIFICATION IS APPLIED BY LEAVING THE TEXT ALONE, AND THAT IS VERIFIED
BY DIFF RATHER THAN ASSERTED.**
`git diff --stat -- openspec/changes/add-declared-former-id/specs/` across the
ratification commit is **empty (0 files)** — the one `## MODIFIED` block and
the three `## ADDED` requirements over `release-realization`, thirty-one
scenarios in all (7 + 8 + 10 + 6), are ratified exactly as authored and exactly
as the bench reviewed them.

## 2. The five decisions, as put and as ruled

| D | `design.md` | Put | Ruled | Considered, not adopted |
| --- | --- | --- | --- | --- |
| **D1** | D1 | Where the declaration lives | **(a) — a top-level `former_ids:` key in the packet's own `.openspec.yaml`, a SIBLING of `origin:` and never a member of it.** It is the file the archive gate already reads at both ends; it is the packet's identity record beside `origin:`'s ideation record; and the sibling position is a REQUIREMENT, not a preference — M3 measures that `origin_block_lines` returns the identical block with the key present, so a lawful move is never a mutation of the frozen origin declaration | (b) a field inside `origin:` — every lawful move becomes a mutation of a frozen declaration needing its own disposition, a mechanism whose ordinary use requires an exception; (c) an estate-level register in the shape of `contracts/policies/repository-identity.yaml` — a repository transfer is an ESTATE-WIDE event, a packet move is LOCAL, and its record must travel with the packet through the archive relocation into the directory the gate reads |
| **D2** | D2 | What the declaration names | **(a) — CHANGE IDS, with the path DERIVED**, ordered oldest first and APPENDED TO, never rewritten. Read from how this estate already addresses a packet: `ratifying_commit` takes an id and derives the path, `proposal_path_at_ref` resolves an id to whichever path it occupied at a ref, `doc_health.corpus.change_ids` unions active and archived ids | (b) declare former PATHS — would restate the archive-directory convention in every packet that ever moved and would have to be RE-declared when the packet archives, which is not an identity change at all, so the list would record a non-event and stop meaning "the identities this packet has had" |
| **D3** | D3 | Who takes the fail-closed refusal | **(a) — a NEW house validator run as a required check AT THE LANDING**, in the shape `gate-realization-axis-vocabulary` established: `former-id-undeclared` exit 1 naming the commit, the source path, the destination path and the one repair; `former-id-arrival-unreadable` exit 2 CANNOT RUN; the pairing arm primary and the `ls-tree` tree arm fail-closed; the archive relocation excepted by id; **no bypass flag** (#690) | (b) put the refusal in the archive gate — the corpus would carry a laundered rename until the packet archived, and the author who could repair it cheaply would be long gone; (c) a `doc-health` finding — `doc-health` REPORTS and does not refuse, and the commissioning ruling's word is "refused" |
| **D4** | D4 | Does the swept-in citation half owe a `doc-health` delta | **(a) — NO `doc-health` delta in this packet.** What the mechanism repairs is a RESOLUTION RULE, and it belongs with the identity it resolves: M4 measures that the rule alone repairs 58 of the 94 dangling references, every one of them broken by the archive relocation. REPORTING the remainder is a second governed surface with its own numeral, recorded as a successor at `tasks.md` § 6.1 with the figures so it need not re-derive them | (b) add the twenty-fourth family here — a `## MODIFIED Requirements` block over a promoted enumeration reading *"twenty-three check families"*, plus a registry edit, a numeral, and a second set of severity decisions this packet has no ruling for; (c) put the reporting sweep in the `cited_to` gate — that gate (`validate-pin-registrations.py`'s `check_citations`, M5) already resolves every citation and refuses exit 1 on an absent path, so it needs the RESOLUTION RULE and not a reporting arm, and its deliberately cross-repository dispositions belong to its own design |
| **D5** | D5 | *Origin retention at archive* — MODIFIED or left alone | **(a) — MODIFY it.** The promoted requirement names the baseline as *"the declaration present at ratification"* and the whole defect is that after a move the walk compares against a commit that is NOT the ratification; leaving it untouched and adding a separate requirement would put two rules over one gate with the older one still saying the baseline is found where it cannot be found. The block carries every promoted sentence and all three promoted scenarios VERBATIM and only adds, so the modified-block-currency carriage arm has nothing to report and this packet opens no ledger row | (b) three ADDED requirements only — cheaper (an ADDED block costs no carriage argument) and the shape `gate-code-surface-declarations` took for a neighbouring sentence, but that packet was ADDING a constraint the promoted sentence did not speak to, while this one CHANGES where the promoted sentence's own baseline is found |

**EVERY RULING IS THE RECOMMENDED OPTION.** No requirement text was rewritten,
no scenario was added or removed, no delta directory was renamed, and no
`sequenced_after:` entry moved. `sequenced_after: []` stands corroborated by M6
rather than asserted.

## 3. The measurements this ratification rests on (D0, restated)

The figures were taken in the authoring session on a clone of `main` at
`9378eca5`, and they are restated here because a ratification that cites a
design must be readable without it.

- **M1 — the two silences git answers with the same value.** On a
  `git clone --filter=blob:none --no-checkout` of a fixture carrying the #1003
  chain with the promisor remote made unreachable (git 2.43.0):
  `git ls-tree --name-only <rev> -- <path>` prints **the row at exit 0** for a
  path present with an unavailable blob and **nothing at exit 0** for a path
  genuinely absent, while `git cat-file -e` and `git show` **exit 128 for
  both**. `ls-tree` separates ABSENT from UNREADABLE; the two reads this
  estate's packet-at-a-ref lookups are built on
  (`proposal-support.git_show_text`, `sequenced_after._blob_exists_at_ref`) do
  not.
- **M2 — the substrate loses exactly the hop that matters.** At the hop that
  renames AND un-ratifies in one commit, the full clone pairs
  `R075 <source> <destination>` and the partial clone reports **no record at
  all**. Rename pairing below an exact match is computed from content, and an
  un-ratifying rename is a rename that also EDITS, so the checkout that cannot
  read content loses the dangerous hop and keeps the harmless ones. On that
  same checkout the TREE still names the predecessor. **A declaration is read
  from the tree.**
- **M3 — a sibling key does not enter the frozen origin comparison.**
  `proposal-support.origin_block_lines`, loaded from the shipped script, returns
  the IDENTICAL block with and without a top-level `former_ids:` list appended,
  because it starts at the `origin:` line and stops at the first line that is
  neither blank nor indented. Nothing in the repository refuses an unknown
  top-level key in `.openspec.yaml`.
- **M4 — the dangling-citation population.** Over every tracked file except
  `openspec/changes/archive/` (frozen record), `tests/` and `specs/` (fixtures
  and Spec Kit feats): **94** distinct `openspec/changes/<id>/…` references
  resolve to nothing, **58** of them resolve BY ID against the archive. The one
  #833 named is among the 58.
- **M5 — one thing checks a citation's destination, and it checks the RAW
  PATH.** `validate-pin-registrations.py`'s `check_citations`, landed for this
  exact defect (issue #840), resolves every `dispositions[].cited_to` referent
  and makes an absent path "a named finding and exit 1". **Six of its live
  in-tree referents point into four ACTIVE packets**, so the next of those
  archives turns a lawful act into an exit-1 refusal of a gate nobody touched.
  This measurement was taken twice — the first reading said nothing checks, and
  the bench's third round found the consumer it missed; the correction is
  recorded rather than smoothed, because the corrected fact is stronger than
  the claim it replaces.
- **M6 — the delta is unsequenced.** No active change holds a `## MODIFIED`
  block over *Origin retention at archive*; the only other occurrence of that
  title under `openspec/changes/*/specs/` is one line of prose in
  `add-structured-scope-substrate`'s delta.

## 4. The bench, on the head this word ratifies

The ratified head `1e57643d` is a BENCHED head, and this record states its
dispositions rather than leaving them in comment scrollback. **Four rounds,
sixteen threads, sixteen disposed: fifteen TAKEN in three content commits, one
REFUSED with a measurement. Zero unresolved, counted through GraphQL and never
by eye.**

| round | on | threads | disposition |
| --- | --- | --- | --- |
| 1 | `75ff1043` | **9** (3 Codex P1, 6 Copilot) — the refusal reached a LAWFUL DRAFT RENAME, contradicting this packet's own scenario and the promoted record; a standing packet could append an identity it never had; append-only was stated and unenforceable; one identity could resolve to a SET; `proposal_path_at_ref`'s boolean probes contradicted this packet's own fail-closed clause | ALL NINE TAKEN in `94a0e6cd` |
| 2 | `94a0e6cd` | **3** — round one's qualification could be SHED BY MOVING TWICE (X ratified → X→Y declared and un-ratified → Y→Z undeclared); the reference rule resolved the packet and never the FILE; the README row's own count was stale by one | ALL THREE TAKEN in `f887fd78` |
| 3 | `f887fd78` | **3** — the fail-closed arm covered the pairing read and not the RATIFICATION LOOKUP; `design.md` D0 M5 was WRONG about there being no citation consumer; the description carried round zero's count | ALL THREE TAKEN in `1e57643d` |
| 4 | `1e57643d` | **1** — a re-flag of the item round 3 had already taken ("20 scenarios (6 + 5 + 5 + 4)", "29 task boxes") | **REFUSED**, measured: the description's `lastEditedAt` reads 2026-09-13T06:39:37Z through GraphQL, seven minutes BEFORE that review was submitted at 06:46:47Z against the snapshot taken at the push; read live, neither quoted phrase is present; answered on the thread and disposed at [issuecomment-5651753014](https://github.com/opensoft/openxFactory/pull/1028#issuecomment-5651753014) |

Two of round two's findings and one of round three's are defects the previous
round's own fixes created or left half-closed, which is why each round was
benched rather than assumed clean. `design.md` D9, D10 and D11 carry the three
content rounds thread by thread. **Codex** reviewed once, at
2026-09-13T05:28:25Z, and its three P1 threads are the first three of round
one; it posted nothing after. The FREEZE of 2026-09-13T07:04:25Z recorded six
of six required checks PASS on `1e57643d` — `pytest-suite`
([run 34743252884](https://github.com/opensoft/openxFactory/actions/runs/34743252884),
selected=7336 passed=7330 skipped=6 failures=0 errors=0), `lane-line`,
`openspec-cli-pin`, `release-tag-gate`, `signed-execution-chain-gate`,
`wallet-validation` — and `closingIssuesReferences = []`.

## 5. What this word admits, and what it does not

**ADMITTED.** The one `## MODIFIED` block and three `## ADDED` requirements on
`release-realization` exactly as frozen at `1e57643d`:

- *Origin retention at archive* (MODIFIED) — the baseline is resolved across
  the current identity and every declared former identity together, taking the
  EARLIEST commit at which any of them declares `Status: ratified`; the
  resolution is by identity and never by rename detection; the comparison
  itself does not move, so a rename is not a way to acquire a later baseline
  and therefore not a way to launder a mutation; and every read behind the
  baseline fails closed with ABSENT distinguished from UNREADABLE.
- *A moved packet declares the identity it was ratified under* (ADDED) — the
  top-level `former_ids:` list, a sibling of `origin:`, naming change ids,
  oldest first, APPEND-ONLY ACROSS COMMITS, each entry added only by the commit
  that performs the move it records, exactly one owner per former identity, the
  archive relocation never declared, and a declared former id that still stands
  as a live directory refused.
- *An undeclared rename arrival is refused at its landing* (ADDED) — one commit
  read and never a chain, qualified to a move whose source identity has EVER
  declared `Status: ratified` over its whole DECLARED LINEAGE, the arriving list
  being the source's list with the source id appended, both historical reads
  failing closed, the archive relocation excepted by id, no bypass flag.
- *A packet reference resolves by identity, not by path* (ADDED) — resolution
  by change id against the location the id occupies now and against any packet
  declaring it as a former id; BOTH HALVES of a packet-relative citation
  resolve; resolution is to exactly one packet or to nothing and an id that
  would resolve twice is reported AMBIGUOUS, never settled by sort order.

**NOT ADMITTED, AND NOT BY THIS WORD.**

- **Nothing reaches `openspec/specs/`.** This ratification edits no promoted
  file. Promotion happens at ARCHIVE, and `tasks.md` § 7.1 holds it in a
  SEPARATE pull request on a separate word.
- **Nothing is realized.** No script, validator, reader, register, workflow or
  test is added or edited by this act; `tasks.md` §§ 2, 3, 4 and 5 stay
  entirely open and unticked.
- **No `doc-health` delta exists and none is owed here** (D4). The reporting
  sweep for the unresolvable remainder is a successor, filed with a sibling
  search at the realization and not before, and `tasks.md` § 6.1 carries its
  figures.
- **Nothing anyone else authored is edited.**
  `disposition-codexfactory-declared-renames`, which carries the live dangling
  citation M4 found, keeps its ratified prose exactly as it stands: the repair
  is a resolution rule applied by the READER.
- **No other estate repository is reached**, no contract byte moves, no schema
  member is added, and nothing under `contracts/` or `governance/` is edited.
- **The interim docstring-and-fixture pin is still a separate pull request**
  (`fix/1003-interim-pin-multi-hop-gap`, `tasks.md` § 6.2), and the three
  further residues § 6.3 to § 6.5 are named and taken nowhere.
- **openxFactory #1003 stays OPEN.** Whether and when it closes is Brett Heap's
  word; this packet carries no closing keyword against it in any body, commit
  message or reply, and `closingIssuesReferences` reads `[]`.

## 6. What is owed after this word

- **§ 2 through § 5 (realization) are owed and are NOT in this pull request.**
  `code_surface:` is NON-EMPTY — `scripts/proposal-support.py`'s
  `ratifying_commit` and its `origin_retention_errors`, a new reader and
  validator CLI for the landing refusal, a new reader for the
  reference-resolution rule, `tests/proposal-support/test_proposal_support.py`
  and a new test module, and `docs/document-lifecycle.md`'s blocked-rename
  sentence — and no byte of it moves here.
- **THE ARCHIVE IS GATED ON REALIZATION EVIDENCE, BY PROMOTED CANON AND BY
  THIS PACKET'S OWN TERMS.** `release-realization`'s *Realization archive gate*
  reads: *"A change with a non-empty code surface SHALL NOT archive until
  realization evidence exists: its code merged on the implemented target
  through the owning domain's engineering gates, and — where the surface is
  runnable — a green run of that surface […] Until then the change remains
  active as approved-but-unrealized intent."* `tasks.md` § 7.1 states the same
  obligation in this packet's own words: it *"does not archive on landing and
  does not archive on ratification: it archives when the realization slices of
  § 2 through § 5 are merged on the implemented target and `pytest-suite` has
  run green at the tree that merge carries. **Neither this pull request nor the
  ratification pull request may perform it.**"* `target_release: implemented`
  (the openxFactory main line) — no contract bundle is cut, so no release tag
  is owed and `deferred-allocation` is deliberately not declared.
- **The promotion of the one MODIFIED and three ADDED requirements into canon
  is the archive pull request's act**, byte-for-byte, on a further word
  (§ 7.1).
- **openxFactory #1003 closes at the archive pull request and nowhere else, and
  only on Brett Heap's word** (§ 7.2).
- **Merge is a separate word.** This ratification does not land PR #1028; Rule 6
  (the landing-window protocol for a pull request touching `openspec/changes/`
  and the README OpenSpec Records block) applies at landing, and the landing is
  the lane's act on this same word.

## 7. Provenance of this record

Written in the ratification commit itself, in the clone
`scratchpad/wave-22Z/encode-prep` of `opensoft/openxFactory`, by lane
`openxfactory-1` (display `openXfactory-1`), session `ea50c958`. It carries
`Status: ratified` because `document-lifecycle`'s *A review record records a
ratification* governs a `review/ratification-*` file, and the single
`Ratified:` line in its header is the one sanctioned citation the
`ratified-provenance` family counts — `Ratifier:` and `Decision date:`
accompany it and never stand in place of it. Every repository path in this file
is repo-relative.

## Addendum — the realization, and the separate archive word (2026-09-15)

Appended at the archive, AFTER everything above and editing none of it. Nothing
above this line was true only until now; it was written at the ratification and
it is kept as it stood.

**REALIZED ON `main`, FOUR PULL REQUESTS, EACH BY NUMBER AND MERGE SHA.**
`code_surface: openxFactory` is non-empty, so under `release-realization`'s
*Realization archive gate* this packet archives on merged-plus-green
realization evidence and never on landing or on ratification:

| slice | PR | merge sha | merged (UTC) |
| --- | --- | --- | --- |
| 1–3 — the declaration, its reader, the identity baseline, the fail-closed reads | [#1038](https://github.com/opensoft/openxFactory/pull/1038) | `701c8fded24963a855d7f34155821cd4ec70c100` | 2026-09-14T21:09:32Z |
| 5 — the reference resolver and its named consumer | [#1037](https://github.com/opensoft/openxFactory/pull/1037) | `8f3937584da8c4ba734ec087c9d613552a9cb217` | 2026-09-15T19:02:27Z |
| 4 — the landing validator `former-id-arrival-gate` | [#1039](https://github.com/opensoft/openxFactory/pull/1039) | `92d519b0c9e700f288c7d8e19cdf0b8312353f60` | 2026-09-15T19:15:02Z |
| 6 — the documents and the ticks | [#1041](https://github.com/opensoft/openxFactory/pull/1041) | `79ac94b74ec6418b9fb149f9ba70767ac2635773` | 2026-09-15T21:24:28Z |

**THE GREEN RUN, AND THE THREE MERGES THAT HAVE NO DECIDED RUN OF THEIR OWN —
SAID EXACTLY, NOT GLOSSED.** `pytest-suite` triggers on `push: main` as well as
on `pull_request`, so each merge commit starts its own run; but the workflow's
concurrency group is `pytest-suite-${{ github.ref }}` with
`cancel-in-progress: true` (`.github/workflows/pytest-suite.yml:287-289`), and
on `main` that ref is the same string for every push, so each landing CANCELS
the previous main run. Measured from
`GET /repos/opensoft/openxFactory/commits/<sha>/check-runs?check_name=pytest-suite`:

| merge | main's own run on it | verdict | what covers it |
| --- | --- | --- | --- |
| `701c8fde` | [34897189477](https://github.com/opensoft/openxFactory/actions/runs/34897189477) | **completed / SUCCESS**, `selected=7626 passed=7620 skipped=6 failures=0 errors=0` | itself — no fallback needed |
| `8f393758` | [35011209877](https://github.com/opensoft/openxFactory/actions/runs/35011209877) | completed / **CANCELLED** by the push of `92d519b0` | the pull request's own green run on `refs/pull/1037/merge`, TREE-EQUAL to this merge |
| `92d519b0` | [35012492979](https://github.com/opensoft/openxFactory/actions/runs/35012492979) | completed / **CANCELLED** by the push of `8944758c` | **NO tree-equal green run exists.** `main`'s own next decided run, and its newest — see below |
| `79ac94b7` | [35025437085](https://github.com/opensoft/openxFactory/actions/runs/35025437085) | completed / **CANCELLED** by the push of `b3a75537` | the pull request's own green run on `refs/pull/1041/merge`, TREE-EQUAL to this merge |

**THE TREE-EQUALITY HALF, READ RATHER THAN ASSERTED.** Each pull-request run
checked out `refs/pull/<n>/merge`, whose sha and parents its own log names, and
those objects are still fetchable by sha:

* **#1037**, run [34905703945](https://github.com/opensoft/openxFactory/actions/runs/34905703945)
  (job `104182031635`, SUCCESS, `selected=7745 passed=7739 skipped=6
  failures=0 errors=0`) — log: *"HEAD is now at 34ab52f3 Merge
  `c48b91ae…` into `74348374…`"*.
  `git rev-parse 34ab52f3…^{tree}` = `1ee37ec026163f225f95fd7fb7f4aeb49e10a422`
  = `git rev-parse 8f393758^{tree}`. **EQUAL**, and the same two parents.
* **#1041**, run [35023330889](https://github.com/opensoft/openxFactory/actions/runs/35023330889)
  (job `104564236583`, SUCCESS, `selected=7809 passed=7803 skipped=6
  failures=0 errors=0`) — log: *"HEAD is now at 018aa2ed Merge
  `f7fda10e…` into `8944758c…`"*.
  `git rev-parse 018aa2ed…^{tree}` = `cce4586019aefe3a266cb730c2df0b4329af028f`
  = `git rev-parse 79ac94b7^{tree}`. **EQUAL**, and the same two parents.
* **#1039 IS THE ONE THAT DOES NOT CLOSE THIS WAY, AND IT IS NAMED RATHER THAN
  STRETCHED.** Its run [34909231418](https://github.com/opensoft/openxFactory/actions/runs/34909231418)
  (job `104192844791`, SUCCESS, `selected=7773 passed=7767 skipped=6
  failures=0 errors=0`) checked out `a7fc93e9` — *"Merge `24cd42a1…` into
  `74348374…`"* — but the merge commit `92d519b0` is `merge(8f393758,
  24cd42a1)`, #1037 having landed in between. `git rev-parse a7fc93e9…^{tree}`
  = `bd318880cda3206da49f0b9f6f2a9637fa0caab3`, `git rev-parse
  92d519b0^{tree}` = `8857c32dc42a30daaf3d4ef39f2be3779543b3ee`: **DIFFERENT**.
  So the pull-request run is NOT evidence at the tree this merge carries, and
  it is not offered as such.

**WHAT COVERS `92d519b0`, AND WHAT COVERS ALL FOUR TOGETHER.** No `pytest-suite`
run in this repository is decided green at a commit whose tree equals
`8857c32d`; `92d519b0` is the only commit carrying that tree and its own run was
cancelled. Two decided green runs on `main` stand behind it instead, both cited
as what they are — runs at DESCENDANT commits, not at this tree:

1. **`main`'s next decided run, [35014513335](https://github.com/opensoft/openxFactory/actions/runs/35014513335)** at
   `8944758c739e6658d2ef7a9be03549e33b415db2`, `event: push`,
   `conclusion: success`, 2026-09-15T19:35:14Z→19:49:15Z,
   `selected=7809 passed=7803 skipped=6 failures=0 errors=0`. `git rev-parse
   8944758c^1` is `92d519b0` — it is the merge's own first-parent child — and
   `git diff --stat 92d519b0 8944758c` is the `extend-prose-tagging…` archive
   and nothing else, with slice 4's entire surface
   (`scripts/former_id_arrival.py`, `scripts/validate-former-id-arrival.py`,
   `tests/former_id_arrival/`, `.github/workflows/former-id-arrival-gate.yml`)
   BYTE-IDENTICAL between the two trees (empty diff).
2. **`main`'s newest decided run, [35026939157](https://github.com/opensoft/openxFactory/actions/runs/35026939157)** at
   `b3a755374…`, `event: push`, `conclusion: success`,
   2026-09-15T21:40:28Z→22:00:07Z,
   `selected=7814 passed=7808 skipped=6 failures=0 errors=0`.
   `git merge-base --is-ancestor <merge> b3a75537` exits 0 for **all four**
   merges, so this one run is green over a tree that contains every one of
   them, and slice 4's surface is again byte-identical to `92d519b0`'s.
   (`main`'s runs at `96be520a` and later were themselves cancelled or still
   running when this was read, 2026-09-15T23:3xZ; `b3a75537` is the newest
   DECIDED one.)

**THE OPERATOR HALF, IN ITS HONEST DEGRADED CASE.** § 4.5 —
registering `former-id-arrival-gate` as a required check — is **NOT PERFORMED**.
Re-read live at 2026-09-15T23:35:31Z, `GET
/repos/opensoft/openxFactory/rules/branches/main` returns three
`required_status_checks` rules (21957695, 22551797, 21538893) and that context
is in none of them. Brett Heap ruled the packet may archive anyway —
2026-09-15T19:00Z, verbatim ***"Yes, with disposition + carry-forward
issue"***, [issuecomment-5686436893](https://github.com/opensoft/openxFactory/issues/1003#issuecomment-5686436893)
— so `tasks.md` § 4.5 is ticked WITH ITS DISPOSITION and the obligation is
carried forward at openxFactory#1061, the shape
`add-signed-execution-chain` established at issue #534. The packet reaches
canon MEETING ITS OWN DEGRADED CASE: an unrequired arrival gate runs on every
pull request and refuses no landing.

**THE ARCHIVE WORD.** Brett Heap, 2026-09-16 (~12:4xZ, in session to lane `openxfactory-1`, display `openXfactory-1`), verbatim
***"archive it, open the PR"***, recorded at [#1003](https://github.com/opensoft/openxFactory/issues/1003#issuecomment-5697795401) — a SEPARATE
word from the ratification of 2026-09-13T22:48Z and from every realization
merge, exactly as § 7.1 requires. The archive was performed with
`python3 scripts/proposal-support.py . archive add-declared-former-id --yes`
and never a bare `openspec archive`.

**AND THE GOVERNING ISSUE HAD ALREADY CLOSED.** openxFactory #1003 was closed
2026-09-15T21:24:38Z, eleven seconds after slice 6's merge, on Brett Heap's
word *"Close when #1041 lands"* — earlier than `tasks.md` § 7.2's own first
sentence put it, which that box now records rather than reconciles.
