# Proposal Ratification: add-target-release-deferred-allocation

Status: ratified
Kind: report
Decision date: 2026-09-13
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-09-13T01:0xZ by Brett Heap (openxFactory repository owner),
verbatim: *"accept all A on 1022"* — given as a MULTIPLE-CHOICE ruling over all
ten decisions `proposal.md` § Open questions and `design.md` D1 through D10 put
for the owner, given in session directly to lane `hermes-wallet-exercise`
(window `hermes-wallet-exercise`, session `codeXfactory-2`, workstation Eagle)
and recorded in full here.
**THE WORD TAKES THE RECOMMENDATION ON EVERY ONE OF THE TEN: OQ-1 = (a),
OQ-2 = (a), OQ-3 = (a), OQ-4 = (a), OQ-5 = (a), OQ-6 = (a), OQ-7 = (a),
OQ-8 = (a), OQ-9 = (a), OQ-10 = (a).** Each is the option the packet already
encoded, so **THE DELTA'S WORDING STANDS UNCHANGED AND NOTHING WAS SUBSTITUTED,
RESTORED OR DELETED.**

## 1. The word, and what it reaches

**"accept all A on 1022" IS A SINGLE MULTIPLE-CHOICE RULING OVER TEN DECISIONS,
NOT TEN SEPARATE WORDS.** It was given at 2026-09-13T01:0xZ and is recorded
verbatim, with that instant, on every document this ratification touches —
`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`
(`approved_by`/`approved_on`, added beside the unmoved `proposed_by`/
`proposed_on` pair the `add-drafted-proposal-origin` (issue #318) shape
defined), the README OpenSpec Records entry, and this record.

**THE INSTANT IS RECORDED TO THE PRECISION IT WAS TAKEN AT AND NO FINER.** The
minute is written `01:0xZ` rather than invented, which is this packet's own
house form: its filing provenance records the commissioning word of the same
night as *"2026-09-13 at approximately 00:5xZ"*. `tasks.md` § 1.2 required the
UTC instant "as GIVEN (never invented)"; writing a false `:MMZ` to make the
stamp look machine-produced would be inventing evidence, and this record
declines to.

**THE RATIFICATION IS APPLIED BY LEAVING THE TEXT ALONE, AND THAT IS VERIFIED BY
DIFF RATHER THAN ASSERTED.** `git diff --stat -- openspec/changes/add-target-release-deferred-allocation/specs/`
across the ratification commit is **empty (0 files)** — the two `## MODIFIED`
requirements over `release-realization` are ratified exactly as authored and as
PR #1022's review was drafted against.

## 2. The ten decisions, as put and as ruled

| OQ | `design.md` | Put | Ruled | Considered, not adopted |
| --- | --- | --- | --- | --- |
| **OQ-1** | D1 | The token's spelling | **(a) — `deferred-allocation`**, the register's own ratified class word, so vocabulary and register name one thing and retirement is mechanical (`class: deferred-allocation` ↔ `target_release: deferred-allocation`) | (b) `deferred` — reads as a work STATE and invites the four registered `implementation_pending` carriers to "correct" into a token that does not describe them; (c) `contract-deferred` — a second name for a class the register already names |
| **OQ-2** | D2 | Where the widening is written | **(a) — BOTH promoted requirements, `## MODIFIED`**, paying `sequenced_after: [add-structured-scope-substrate]` and a pre-text written from that change's outcome | (b) the gate requirement only — canon would enumerate two values in one place and three in the other; (c) an `## ADDED` novel title — both promoted enumerations go stale and the vocabulary is written in three places |
| **OQ-3** | D3 | May a `deferred-allocation` change archive? | **(a) — NO**; the archiving act first resolves the token to the literal the cut allocated, or to `implemented` where no bundle was cut | (b) archive with the token standing — a permanently unresolvable frozen record; (c) archive with a disposition — makes the ordinary case a contested act |
| **OQ-4** | D4 | How that archive rule is enforced | **(a) — canon-enforced AT THE ARCHIVING ACT**; the validator REPORTS an archived-unresolved count and refuses nothing there | (b) refuse an archived carrier — contradicts the promoted *"SHALL refuse nothing there"* and creates a standing finding with no remedy on a frozen record; (c) silent — nobody learns the rule was broken |
| **OQ-5** | D5 | Must the resolving edit cite the cut? | **(a) — YES**; it names the bundle version and the release surface carrying it, so the number is OBSERVED, mirroring § Bundle Realization Order steps 4–5 | (b) a bare token swap — indistinguishable from the reservation the versioning policy forbids; (c) cite only for a cut in another repository — a seam for no reason |
| **OQ-6** | D6 | Who may declare it | **(a) — only a change whose `code_surface:` is non-empty AND whose realization lands in a contract bundle** | (b) any change — a second `none`, re-opening the defect the gate was built to close; (c) any non-empty code surface — admits the four `realization-state` carriers this packet does not reach |
| **OQ-7** | D7 | The twelve standing register entries | **(a) — NOT swept here**; each retires when its owning packet corrects its own declaration, the entry deleted in that same pull request, which the exit-2 stale refusal already forces. Only the class NOTE is amended | (b) sweep all twelve — twelve other lanes' `proposal.md` files, twelve entry deletions and a baseline move inside a vocabulary packet; (c) sweep only the quiescent lanes' — an arbitrary line nobody can re-derive later |
| **OQ-8** | D8 | This packet's own `target_release:` | **(a) — `implemented`**; its surface is a validator, a register note and a test, it cuts no bundle, so `deferred-allocation` would be FALSE under its own new sentence | (b) `deferred-allocation` — false, and circular; (c) omit it — but `code_surface:` is non-empty, so the doc-only default would misdescribe it |
| **OQ-9** | D9 | openxFactory #1017 | **(a) — NOT edited here**; its own lane makes the one-line correction after this lands, and `merge 1017 when green` then applies unchanged | (b) edit its front matter in this pull request — two lanes writing one packet; (c) hold #1017 until its bundle is cut — blocks a ratified change on an unscheduled event |
| **OQ-10** | D10 | Where the realization lands | **(a) — THIS pull request**, mirroring `gate-realization-axis-vocabulary` exactly: validator, register note and tests beside the ratification, archiving later on merged-plus-green | (b) a follow-up realization PR — leaves canon admitting a value no validator accepts, so #1017 stays blocked after ratification |

**EVERY RULING IS THE RECOMMENDED OPTION.** No requirement text was rewritten,
no delta directory was renamed, and no `sequenced_after:` entry moved.

## 3. What this word admits, and what it does not

**ADMITTED.** The two `## MODIFIED` requirements on `release-realization`
exactly as authored on PR #1022: *Realization axis declaration* and
*Realization axis vocabulary is gated*, each widened from the two-value
enumeration to three by the single token `deferred-allocation` (OQ-1), written
into BOTH rather than one (OQ-2); plus the four rules the new value needs and
canon did not have — it is available only where a bundle is cut (OQ-6); it MUST
be resolved to a literal release before the packet archives (OQ-3); the
resolving pull request MUST name the cut it observed (OQ-5); and an archived
record still carrying it unresolved is COUNTED AND REPORTED and judged never
(OQ-4), the promoted *"SHALL refuse nothing there"* admitting no exception for
this value.

**NOT ADMITTED, AND NOT BY THIS WORD.**

- **Nothing reaches `openspec/specs/`.** This ratification edits no promoted
  file. Promotion happens at archive, and `tasks.md` § 5 holds that behind
  merged-plus-green realization evidence, its own word, and the § 5.2 ordering
  re-read against `add-structured-scope-substrate`.
- **`CLOSED_REGISTER` does not move and no register ENTRY is added.** This act
  admits a VALUE, which is the distinction the promoted requirement draws:
  *"admitting a NEW value to the vocabulary SHALL be a change to this
  specification rather than an addition to the register."*
- **The twelve standing `deferred-allocation` carriers are not swept** (OQ-7).
  None of them spells the token `deferred-allocation` today — they carry `THE`,
  `next`, `the` and `contract-v<next` — so admitting the value retires no entry
  by itself, and only the class NOTE moves.
- **openxFactory #1017 is not touched** (OQ-9). Its one-line correction —
  `target_release:` token to `deferred-allocation`, the prose gloss preserved
  verbatim — is its own lane's act after this lands, under the separate word
  `merge 1017 when green` already given.
- **No other estate repository is reached**, no contract byte moves, no schema
  member is added, no workflow changes, and nothing under `contracts/` or
  `governance/` is edited.
- **`code_surface:` is still not gated** (openxFactory #1013) and the
  "aggregation repository" wording is still unrepaired (`tasks.md` § 6.2) —
  both named and deliberately left.

## 4. What is owed after this word

- **§ 2 (realize) rides in THIS pull request** per OQ-10 and is already
  carried by it: `scripts/target_release.py`, `scripts/validate-target-release.py`,
  `scripts/target-release-register.yaml`'s class note and ten new tests in
  `tests/target_release/test_target_release_gate.py`. Its evidence is this pull
  request's green `pytest-suite` at the tree the merge carries.
- **§ 2.5 (re-measure both rows of `proposal.md` § The measurement on the tree
  this packet lands on) STAYS OPEN, and this record says why it must be
  re-taken rather than trusted.** The figures in `proposal.md` § The measurement
  and in `design.md` D0 were taken off `origin/main` `a1429885`. This branch has
  since been re-levelled onto `origin/main` `3cf8b0bb` (PR #1015's archive of
  `report-stale-grandfather-dispositions` and PR #1011), which moved the corpus
  counts under them. They are the honest record of the measurement as taken and
  are not edited by this ratification; the re-measure is § 2.5's act.
- **§ 5 (archive) stays entirely open**, held behind merged-plus-green
  realization evidence, a separate word, and the § 5.2 ordering re-read.
- **Merge is a separate word.** This ratification takes PR #1022 out of DRAFT
  (marked READY) but does not merge it; Rule 6 (the landing-window protocol for
  a PR touching `openspec/changes/` and the README OpenSpec Records block)
  applies at landing.

## 5. The gate this ratification unblocks

`scripts/target_release.py` is a RATCHET: its register is the corpus as it stood
on 2026-09-12, so a proposal authored after it, obeying
`docs/contract-versioning-policy.md` § Bundle Realization Order exactly as the
twelve registered carriers do, has no entry and no lawful spelling and reds the
required `pytest-suite`. openxFactory #1017
(`encode-wallet-authority-rulings-r6-r12`) is RATIFIED and READY with its merge
word given and is blocked on precisely that. This word admits the spelling that
packet needs; the correction itself is its lane's, not this one's (OQ-9).

## 6. Provenance of this record

Written in the ratification commit itself, in the worktree
`~/projects/xFactory/openxFactory-worktrees/target-release-deferred`, by lane
`hermes-wallet-exercise`. It carries `Status: ratified` because
`document-lifecycle`'s *A review record records a ratification* governs a
`review/ratification-*` file. Every path in this file is repo-relative.
