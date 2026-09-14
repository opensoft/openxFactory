# Proposal Ratification: mirror-floor-regeneration-automation

Status: record

Decision date: 2026-09-06

Ratifier: Brett Heap (openxFactory repository owner) — in session, lane
`openXfactory-2`, session `de9d8fd4`, recorded on PR #708
(`https://github.com/opensoft/openxFactory/pull/708#issuecomment-5556025824`,
the comment beginning "RULING — RATIFIED", posted 2026-09-06T01:18:15Z and
stating its own ruling time as 2026-09-06T01:18Z).

Ratified verbatim: **"ratify both when green, then land them"** — Brett Heap,
2026-09-06T01:18Z, in session. **It is a PAIR WORD**: it ratifies this companion
and its parent `codexFactory: add-floor-regeneration-automation` (codexFactory
PR #235, head `c551e281`, record
`openspec/changes/add-floor-regeneration-automation/review/ratification-2026-09-06.md`)
in one act, and each repository records it separately in its own review
directory.

**THE WORD WAS CONDITIONAL AND THE CONDITION WAS MET, WHICH IS RECORDED RATHER
THAN ASSUMED.** The ruling comment applies the word to head `e4ef8ade` "once
`pytest-suite` passes (all other eight checks green at 2026-09-06T01:18Z); if
that suite is red the ratifying commit is HELD and the red reported."
`pytest-suite` was polled at 60-second intervals on that head until it left
`pending`, and it PASSED. The ratifying commit was authored only after that.

Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
`tests/sequenced_after/corpus-ledger.yaml`'s row, this record, and the spec
delta `specs/review-lane-floor-mirror/spec.md` carrying EIGHT `## ADDED
Requirements` and 24 scenarios (measured by grep against the delta at this
commit: `grep -c '^### Requirement:'` → 8, `grep -c '^#### Scenario:'` → 24),
with exactly ONE `## ADDED Requirements` heading and no `## MODIFIED
Requirements` or `## REMOVED Requirements` block anywhere in the delta.

**NOTHING IN THE SPEC DELTA CHANGES BETWEEN THE HEAD THE RULING WAS GIVEN OVER
(`e4ef8ade`) AND THIS COMMIT**, and that is stated first rather than left to a
diff. Verified mechanically rather than asserted: `git diff e4ef8ade --
openspec/changes/mirror-floor-regeneration-automation/specs/
openspec/changes/mirror-floor-regeneration-automation/design.md
openspec/changes/mirror-floor-regeneration-automation/tasks.md` is EMPTY at this
commit — no requirement, no scenario, no design line and no task line moves in
the ratifying commit. What DOES change here is `proposal.md` (the `Status:` /
`Ratified:` headers and the two dated notes), `README.md` (the OpenSpec Records
entry's standing), `.openspec.yaml` (the kept-and-answered `approved_by`
statement), and this new record. **This differs by one file from the archived
`mirror-floor-addition-grace` precedent, which took its `.openspec.yaml`
statement in a separate later commit; the difference is named here rather than
papered over with a sentence that would not be true of this commit.**

The catch-up merge of `origin/main` (`0adb5c6b`) is carried in the same act. It
brought no conflict — main's two commits touched
`openspec/changes/implement-omniworker-install-repo/` and
`openspec/changes/split-opendox-two-layer-product/` only, and added no change
directory — so **the per-change sweep ledger needed no re-seeding**:
`python3 scripts/validate-sequenced-after.py . --ledger-diff` reports "per-change
sweep ledger consistent with the corpus (176 rows)" after the merge, with this
change's row intact at `moved_by: "#708"`, `moved_on: "2026-09-06"`, `depth: 1`.
`python3 -m pytest tests/sequenced_after -q` reports **162 passed** after the
merge.

Checks at `e4ef8ade`, the head the ruling was given over — all NINE green:
`pytest-suite`, `merge-master-approval`, `lane-line`, `openspec-cli-pin`,
`openreposhape-pin`, `wallet-validation`, `signed-execution-chain-gate`,
`clearing-dispatch-gate` and `release-tag-gate`. `OPENSPEC_TELEMETRY=0 openspec
validate mirror-floor-regeneration-automation --type change --strict` reports
**valid** at this commit, and `--all --strict` reports **94 passed, 2 failed (96
items)** — the two failures being `add-chain-attestation` and
`add-composed-view-authoring`, both pre-existing on `main`. The failure set is
unchanged from `main`; this branch adds one passing item.

Bot state at the ruling: **Copilot round 1, one thread, real, taken in
`e4ef8ade`, resolved before the ruling** — the ledger row's `moved_on` read
`2026-09-05` while the README entry, the proposal front-matter (`Proposed:
2026-09-06`) and `.openspec.yaml` (`created: 2026-09-06`) all said 2026-09-06.
Root cause recorded on the thread: the seeder defaults `--moved-on` to
`datetime.date.today()` (`scripts/validate-sequenced-after.py:265`), the LOCAL
date, and both pull requests were opened after 00:00Z on 2026-09-06. The fix was
made through the sanctioned writer — the row reset to `origin/main` and rewritten
with `--seed-ledger --moved-by '#708' --moved-on 2026-09-06` — rather than by
hand-editing the artifact. No Codex verdict was sought or obtained on this pull
request.

## Decision

**RATIFY, BY DIRECT RULING OF THE REPOSITORY OWNER**, the EIGHT `## ADDED
Requirements` and 24 scenarios this change adds to the existing capability
`review-lane-floor-mirror` — **as written**, unamended.

**Because the word was a pair word given over a finished head, AUTHORING
DECISIONS M-1 THROUGH M-7 STAND AS RECOMMENDED and none is separately ruled.**
No veto was exercised. This record does not elevate any one of them above the
others, and each remains ONE EDIT AWAY.

| | Decision | Alternative it beat | Disposition |
|---|---|---|---|
| **M-1** | The trigger is the codexFactory floor document MOVING, watched from here, plus a scheduled sweep — the SWEEP is the mechanism. | Have the codexFactory regeneration lane dispatch into this repository when its own pull request merges. | **STANDS AS RECOMMENDED** — a re-pin is owed whenever the floor document moves, INCLUDING by a hand act that sends no dispatch (and a removal can only ever be a hand act), so a dispatch-only design would silently not re-pin. The dispatch leg remains a legitimate accelerator a reviewer may add. |
| **M-2** | ALL FIVE SITES OR NOTHING, enforced by a post-write RE-READ. | Trust that the five edits succeeded. | **STANDS AS RECOMMENDED** — the archived companion's own task 1.2 verified all five "by reading it back rather than by trusting the edit"; this makes that discipline the lane's rather than the operator's, which is the only way it survives the operator being a machine. |
| **M-3** | The snapshot is re-copied and its `sha256`/`entry_count` recomputed from the WRITTEN BYTES. | Carry the digest and count forward from the codexFactory pull request's body. | **STANDS AS RECOMMENDED** — a witness restated from the party being witnessed is not a witness. |
| **M-4** | The bot's pull request is judged by the EXISTING freshness checks with NO exemption. | A bot-lane exemption — a skip, an allowlist, or an assertion relaxed for the lane's branch. | **STANDS AS RECOMMENDED** — an exemption keyed on the author would be the CSC-F16 silent-false-green shape granted on purpose, inside the guard against CSC-F16. |
| **M-5** | Merge authority UNCHANGED: a human word merges. | Extend the merge-master low-risk envelope, live today only for the doc-health nightly lane. | **STANDS AS RECOMMENDED** — `contracts/review-lane-pin.yaml` is itself a never-clearable floor entry whose stated ground is that a clearable pin "would let a pull request choose its own judge"; a lane that could both propose and land a change to it would be exactly that. Put as a separate later ruling in `tasks.md` § 6.3. |
| **M-6** | One identity, template-only, REFUSING rather than falling back. | A `\|\| github.token` fallback, the pattern `pytest-suite.yml:400` uses. | **STANDS AS RECOMMENDED** — there the fallback degrades a `continue-on-error` step whose absence is caught by a named-testcase watch; here it would degrade to an identity that cannot read codexFactory at all, and the lane would report "nothing to move" and exit green. |
| **M-7** | The pull request moves the pin and NOTHING else — no comment-history paragraph. | Let the lane append the templated narrative paragraph every hand advance has written. | **STANDS AS RECOMMENDED, WITH ITS COST ON THE RECORD** — eight advances of narrative in `contracts/review-lane-pin.yaml` stop accruing and the record of WHY an advance happened moves to the pull-request body. That is a real loss of a real practice, put for veto rather than smuggled. |

**Ratification authorizes promotion of the spec delta and performs no
realization.** No code lands by this act.

## What ratification does NOT authorize

1. **No code lands here.** Not one line of `.github/workflows/`, not one test in
   `tests/review_lane_pin/`, not one credential binding. Every box in `tasks.md`
   remains unticked, group 1 included. The realization is a LATER WORD.
2. **No pin moves.** `contracts/review-lane-pin.yaml` `core_commit`,
   `merge-master-approval.yml`'s `PINNED_CORE_COMMIT` and its checkout `ref:`,
   `pytest-suite.yml`'s checkout `ref:`, and
   `contracts/review-lane-floor-snapshot.yaml` with its `sha256` and
   `entry_count: 68` are all byte-unchanged by this act. The floor total stays
   68 and the generated block's pin stays `b5eddaa3…` at `entry_count: 60`.
3. **The JUDGE is not touched, and ratification does not license touching it.**
   LQ-A7, its two negative controls, the byte-identity freshness verifier, its
   named-testcase watch and `EXPECT_SKIPPED` are outside this packet's declared
   `code_surface:` and stay there through realization.
4. **The merge-authority extension stays a SEPARATE LATER RULING** (`tasks.md`
   § 6.3). The default until it is ruled is a human merge word.
5. **No D-3 tolerance value is set, endorsed or read-and-rewritten here.** `3`
   lives in codexFactory's CODEOWNERS-routed floor document, ruled 2026-09-05
   and recorded by codexFactory PR #231 (`8a406b10`); this repository reads the
   field through the pinned core and declares no value of its own.
6. **This record does not merge PR #708**, and this change does not land before
   its parent. It declares `codexFactory:add-floor-regeneration-automation` in
   `sequenced_after:`, so codexFactory #235 lands FIRST; merge here is the
   orchestrator's act on the owner's word ("...then land them"), under the Rule
   6 landing window.
7. **The ratified `review-lane-floor-mirror` requirements promoted by
   `mirror-floor-addition-grace` are not reopened, extended or re-argued.** Every
   requirement in this delta is ADDED and names in its own body which promoted
   requirement it composes with.

## Record links

- Governing issue: codexFactory [#232](https://github.com/opensoft/codexFactory/issues/232) — carries lane `openxfactory-2`'s Rule-1 claim; no separate openxFactory issue was filed, by instruction.
- Origin issue: codexFactory [#203](https://github.com/opensoft/codexFactory/issues/203) — enumerated option (b) and left it unruled.
- D-3 tolerance ruled at `3`: codexFactory [#231](https://github.com/opensoft/codexFactory/pull/231), merge commit `8a406b10`.
- The ruling comment: [PR #708, comment 5556025824](https://github.com/opensoft/openxFactory/pull/708#issuecomment-5556025824); its codexFactory twin is [PR #235, comment 5556025715](https://github.com/opensoft/codexFactory/pull/235#issuecomment-5556025715).
- The parent: codexFactory [#235](https://github.com/opensoft/codexFactory/pull/235), head `c551e281` at the ruling.
- The local parent this packet is also sequenced after: `openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/`.

## Addendum — 2026-09-06: narrative corrections taken at a later head, on the same word

**Three corrections were taken in one commit AFTER this record was first
written, under the SAME ratification word.** They are the openxFactory half of a
sweep whose codexFactory half was Copilot's round 2 on PR #235 (six threads,
four of them factual errors in that packet's E-8 corpus narrative). Copilot has
not reviewed this head; the defects below were found by carrying that review's
findings across rather than by waiting to be told twice.

**NO REQUIREMENT TEXT MOVED, AND NO PIN MOVED.**
`specs/review-lane-floor-mirror/spec.md` is byte-unchanged: still EIGHT `##
ADDED Requirements` and 24 scenarios, one `## ADDED Requirements` heading, no `##
MODIFIED` and no `## REMOVED` block; zero ticked boxes. The corrections touched
`design.md`, `tasks.md`, `.openspec.yaml` and this record only. The precedent for
correcting a ratified packet's narrative in place is openxFactory PR #701 (five
reality-check corrections to `split-opendox-two-layer-product`).

1. **`.openspec.yaml`'s `approved_by` contradicted itself** — it asserted "the
   packet remains Status: draft … a separate act **that has not happened**" and
   then, in the same field, that the packet has since been ratified. This is the
   same defect openxFactory PR #676 fixed in `98edcb45`, and it is fixed the same
   way: the approval-to-author sentence is now in the PAST tense and scoped to
   the moment the field was written, so the field reads as one continuous record
   — authorization to file, then ratification.
2. **`tasks.md` § 6.1 still described the packet as `Status: draft`.** It now
   carries a dated 2026-09-06 note recording the ratification, and § 6.2 a dated
   note recording that M-1 through M-7 stood. **Both boxes stay UNTICKED**:
   ticking an owner's-act box is a claim an agent may not make about the owner,
   and a dated note is how the act is recorded instead.
3. **`design.md` § 8's "second cross-repository entry" was CHECKED and HELD, and
   is now backed by the number rather than by memory.** Measured at this head:
   `corpus_sweep('.')` reports `declaring=5` over `change_ids=176`, and of those
   five declaring changes exactly TWO carry a qualified foreign entry —
   `mirror-floor-addition-grace` (`codexFactory:add-floor-addition-grace`) and
   this one. The claim was true; only its evidence was missing.

**What was checked here and needed NO correction**: this packet carries no
"fenced front matter" claim of any kind (`grep -rn 'fenced'` over the packet and
the README entry returns nothing), so the four false absolutes corrected on
codexFactory #235 are not mirrored in this repository.

**This addendum changes no disposition.** M-1 through M-7 still stand as
recommended, no veto was exercised, and nothing in § "What ratification does NOT
authorize" is relaxed.

### Round-3 corrections — 2026-09-06, same word, same discipline

A further Copilot round on the corrected head raised the workflow-permission
spelling, and it was right: **the workflow `permissions:` key is
`pull-requests`, hyphenated** — the only spelling any workflow in either
repository uses (`pull-requests: read` ×3, `pull-requests: write` ×3 across the
two `.github/workflows/` trees; zero underscore forms), and
`actions/create-github-app-token`'s own input is `permission-pull-requests`. The
underscore `pull_requests` is the App INSTALLATION permission's spelling in the
App/API vocabulary, which both repositories' READMEs already use for App grants.
Both sites here described what the LANE'S WORKFLOW needs, so they now carry the
hyphen form with the App-side spelling named beside it, so neither reader nor a
later realization can copy the wrong one into YAML.

The same round found `tasks.md`'s header asserting "NOTHING BELOW IS STARTED BY
THE AUTHORING OF THIS PACKET" above a group 1 that lists the packet's own
authoring acts. The absolute was wrong and the header now scopes itself: no
REALIZATION is started (groups 2–5), group 1 is the proposal's own acts with its
boxes still unticked for the stated reason, and group 6 is the owner's, recorded
by dated note rather than by an agent ticking it.

**Still no requirement text, and still no ticked box**: EIGHT `## ADDED
Requirements`, 24 scenarios, one `## ADDED Requirements` heading, no `##
MODIFIED` and no `## REMOVED` block, `grep -c '- [x]'` → 0. The companion
codexFactory #235 took the identical corrections in the same sweep.

