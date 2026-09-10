---
code_surface: openxFactory — a NEW `.github/workflows/` lane that moves the FIVE sites naming the pinned decision core and opens the re-pin pull request, plus a declared credential binding template and the `tests/review_lane_pin/` assertions that pin the lane's shape. The five sites are the ones the pin file and the ratified `review-lane-floor-mirror` requirement "The mirror is inert until the pin carries the rule, and the pin moves as one act" already enumerate: `contracts/review-lane-pin.yaml` `core_commit`; `.github/workflows/merge-master-approval.yml`'s `PINNED_CORE_COMMIT`; that workflow's core checkout `ref:`; `.github/workflows/pytest-suite.yml`'s core checkout `ref:`; and `contracts/review-lane-floor-snapshot.yaml` re-copied at the new core commit with `floor_snapshot.sha256` and `floor_snapshot.entry_count` recomputed. NOT THIS CHANGE'S SURFACE, each for a stated reason: the codexFactory generator, its floor document, its tolerance line and the regeneration lane that runs it are AUTHORED THERE and read here (this packet edits no codexFactory file and claims no authority over one); the existing LQ-A7 coverage assertion and the byte-identity freshness verifier are NOT modified — they are the JUDGE of the bot's pull request and are left exactly as they are; and no floor regeneration is performed by this packet at all.
target_release: a code surface, so per `release-realization` it archives only on merged + green realization evidence. The evidence is: the re-pin lane landed with `tests/review_lane_pin/` green; the codexFactory regeneration lane landed; and ONE COMPLETE CYCLE OBSERVED UNATTENDED — a real `openspec/specs/**` promotion here, followed by a bot-opened codexFactory regeneration pull request and a bot-opened re-pin pull request in this repository, both carrying their witnesses, both merged on a human word, with no operator running a generator or copying a digest anywhere in the chain. No contract bundle is involved — this packet adds no registered contract row, moves no digest set, spends no `contract_bundle_version` and owes no release tag.
sequenced_after: [codexFactory:add-floor-regeneration-automation, mirror-floor-addition-grace]
---

# Proposal: mirror-floor-regeneration-automation

Status: ratified
Proposed: 2026-09-06
Origin: codexFactory issue
[#232](https://github.com/opensoft/codexFactory/issues/232) — the governing
issue for the option (b) PROPOSAL, which carries lane `openxfactory-2`'s Rule-1
claim — over codexFactory issue
[#203](https://github.com/opensoft/codexFactory/issues/203), which enumerated
option (b) and left it unruled. The codexFactory packet
`add-floor-regeneration-automation` names this repository's half as the
COMPANION CHANGE `openxFactory: mirror-floor-regeneration-automation` and
deliberately does not author it. **No separate openxFactory governing issue was
filed**: the orchestrating lane's instruction was to file none and to cite #232
in both repositories, and this line is that citation rather than an omission.

Ratified: 2026-09-06, Brett Heap (openxFactory repository owner), in session,
verbatim **"ratify both when green, then land them"** — a PAIR word given over
this companion and its parent codexFactory #235 together, recorded
2026-09-06T01:18Z on PR #708 (comment beginning "RULING — RATIFIED") and applied
at head `e4ef8ade` on the condition that `pytest-suite` pass, which it did;
record `review/ratification-2026-09-06.md`. **AUTHORING DECISIONS M-1 THROUGH
M-7 STAND AS RECOMMENDED** under that word and none is separately ruled; the
owner may veto any of them by follow-up. **NOTHING IS REALIZED BY THE
RATIFICATION** — it ratifies the PROPOSAL, and realization is a later word.

Authored: 2026-09-06, lane `openxfactory-2` (display `openXfactory-2`), on Brett
Heap's word in session, verbatim **"merge 231 when green, then propose option
(b)"** (2026-09-05 ~23:5xZ). **THE WORD AUTHORIZED THE PROPOSING, NOT THE
CONTENT. RATIFICATION IS OWED AND IS BRETT HEAP'S ACT**; nothing below is
ratified by being authored, no requirement here may be cited as approved until
he rules on this packet itself, and NOTHING IS REALIZED — this packet adds no
workflow file, no test, moves no pin, and ticks no box. Every judgment this
authoring session took is listed under § Authoring decisions rather than
presented as settled.
**Ratified 2026-09-06 — see `Ratified:` above; the paragraph above is kept as
the record of the packet's state at authoring.**

## Why

**This repository pays the second half of every floor repair, and the half it
pays is the half where a human retypes a digest.**

The addition grace landed and is in force: a promotion of a new
`openspec/specs/**` path is reported `pending_floor_extension` instead of
refusing the pull request that creates it. **The deferral has a ruled bound.**
codexFactory's floor document declares
`pending_floor_extension_tolerance: 3` — ruled by Brett Heap 2026-09-05T23:39Z,
recorded by codexFactory PR #231 (merge commit `8a406b10`) — so the FOURTH
un-regenerated addition escalates back to `floor_incomplete` and the REQUIRED
`pytest-suite` (org ruleset `21538893`) refuses again.

Discharging the deferral is two pull requests across two repositories, and the
second one is this repository's. **Measured on the only two cycles that have
been run, both by hand on 2026-09-05, every figure read back from the GitHub
API rather than remembered:**

| cycle | codexFactory regeneration | opened → merged | openxFactory re-pin | opened → merged | wall time |
|---|---|---|---|---|---|
| 1 | #212 (`67a6ffc9`) | 17:44:05Z → 18:08:23Z | **#689** (`b6804991`) | 18:17:20Z → 18:39:13Z | **55 min** |
| 2 | #226 (`ad15a898`) | 21:32:29Z → 21:52:00Z | **#702** (`7eedc7ac`) | 22:08:16Z → 22:50:05Z | **77 min** |

**The re-pin half is not judgment. It is a lockstep transcription of one commit
id into four places and a digest into a fifth**, and the pin file says as much
about itself: its `refresh:` instruction is to re-copy the document at the new
`core_commit`, recompute `sha256` and update `entry_count`, and **never** to
hand-edit the copy (`contracts/review-lane-pin.yaml:675-678`). The five sites
today all read `ad15a8988490bf19c659254a92354987ec3a4028` —
`contracts/review-lane-pin.yaml:60`,
`.github/workflows/merge-master-approval.yml:410` and `:525`, and
`.github/workflows/pytest-suite.yml:397` — with the fifth being
`contracts/review-lane-floor-snapshot.yaml` and its declared witnesses
(`contracts/review-lane-pin.yaml:627-632`: `sha256`, `entry_count: 68`).

**A human is a poor transcription device and an excellent reviewer.** The
transcription is exactly the part a machine does without error and the part a
reviewer cannot check by reading — they would have to recompute the digest
themselves to know it is right. The judgment — *is this the core commit we mean
to be judged by?* — is exactly the part that must stay human, and it stays human
in this packet: the lane PROPOSES and a human word merges.

**And the freshness checks that judge such an advance already exist and already
work.** `tests/review_lane_pin/` compares the vendored snapshot byte for byte
against the pinned core and asserts LQ-A7's coverage over it; the byte-identity
verifier is watched BY NAME in the JUnit report so it cannot silently skip
(`.github/workflows/pytest-suite.yml:359-380`). **This packet adds no exemption
for a bot-authored pull request and asks for none.** The bot's pull request is
judged by the same assertions, at the same strictness, or it stays red.

## What Changes

- **A re-pin lane in openxFactory that PROPOSES and never disposes.** On a
  codexFactory `main` push touching the floor document, it resolves the
  codexFactory commit, moves the five sites in ONE commit, and opens a pull
  request. It never merges, never approves and never pushes to `main`.
- **The lockstep is a refusal, not an intention.** The lane moves all five sites
  or it opens nothing. A partial advance is exactly the disagreement the ratified
  requirement *"The mirror is inert until the pin carries the rule, and the pin
  moves as one act"* already refuses, and the lane must not be able to author it.
- **The vendored snapshot is RE-COPIED, never edited, and its witnesses are
  recomputed from the bytes actually written** — not carried forward from a
  report, not copied from the codexFactory pull-request body. An edited witness
  proves nothing.
- **A landed-core refusal, mirroring the landed-pin rule from the consuming
  side.** The lane refuses a codexFactory commit that codexFactory's default
  branch does not carry: a pin at a pull-request head becomes unresolvable when
  that branch is deleted, and this repository has already measured that defect —
  three of the last five declared `generated_at` pins were not ancestors of
  `main` (`contracts/review-lane-pin.yaml:375-382` records the finding, and `:575`
  and `:593` record its retirement).
- **Witnesses in the pull-request body**: the codexFactory commit and how it was
  resolved, `core_commit` before → after, the snapshot's `sha256` and
  `entry_count` before → after, the floor total, the block's `generated_at`
  before → after, and the run URL — the same arithmetic the pin file's own
  comment history keeps for each of its eight advances.
- **Trigger and idempotence**: the codexFactory floor document moving is the
  signal; a scheduled sweep is the backstop; at most one open re-pin pull request
  at a time; nothing to move is a clean, named no-op.
- **Identity**: the App already installed in both repositories, declared as a
  binding TEMPLATE with no live value under `credential-contracts`. The lane
  refuses when the binding does not resolve rather than falling back.
- **What does NOT change**: the pin's `kind: pinned_workflow` grammar; the
  snapshot's status as a byte witness; LQ-A7 and the two negative controls; the
  byte-identity freshness verifier and its named-testcase watch; `EXPECT_SKIPPED`;
  who authors the floor; and the D-3 tolerance, which is codexFactory's
  CODEOWNERS-routed line and is read here, never written.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `review-lane-floor-mirror`: gains the automated re-pin lane's obligations —
  proposal-only authority, the landed-core refusal, the all-five-or-nothing
  lockstep restated for an unattended author, snapshot re-copy and witness
  recomputation, judgment by the existing freshness checks without exemption, the
  witness set, trigger and idempotence, and the credential discipline.
  **The delta is `## ADDED Requirements` only.** No existing requirement is
  modified or removed.

## How this composes, and why nothing is MODIFIED

The seven requirements promoted into
`openspec/specs/review-lane-floor-mirror/spec.md` by the archive of
`mirror-floor-addition-grace` are the base this packet reasons against — in
particular *"The mirror is inert until the pin carries the rule, and the pin
moves as one act"*, which enumerates the five sites and refuses a partial
advance, and *"The grace changes what the lanes report and nothing they
witness"*, which fixes the snapshot as a byte witness. **Every requirement below
is ADDED and names in its own body which promoted requirement it composes with.**
None restates one and none may be read as re-ratifying one.

A `## MODIFIED` delta would be wrong twice: the promoted requirements say WHAT
the lanes must do, and these say WHO may perform the advance and under what
confinement; and a MODIFIED block replaces the whole requirement, so it would put
ratified text back in play to add an automation that changes none of it.

`sequenced_after:` declares two parents. `codexFactory:add-floor-regeneration-automation`
is a QUALIFIED FOREIGN entry, checked for well-formedness only — the neutral
validator *"cannot read another repository's corpus and MUST NOT pretend to"* —
and it is the second foreign entry in this corpus; the first was
`mirror-floor-addition-grace`'s. `mirror-floor-addition-grace` is BARE and
resolves locally at
`openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/`, the archived
anchor the grammar accepts as one of exactly two locations. Both were checked
in the clone rather than assumed.

## What this deliberately does not do

- **It authors no codexFactory file** and claims no authority over one. The
  generator, the floor document, the tolerance line and the regeneration lane
  are codexFactory's.
- **It does not modify LQ-A7, its two negative controls, or the byte-identity
  freshness verifier.** Those are the JUDGE. A packet that automated the author
  and adjusted the judge in the same act would be marking its own homework.
- **It grants a bot-authored pull request no exemption of any kind** — no skip,
  no allowlist, no relaxed assertion, no `EXPECT_SKIPPED` movement.
- **It does not ask for merge-master approval.** The doc-health nightly lane is
  the estate's one bot-authored pull request an App may approve
  (`.github/workflows/doc-health-reusable.yml:2898-2910`); extending that
  envelope here is a SEPARATE later ruling, put in `tasks.md` § 6 and NOT taken.
- **It does not set or read-and-rewrite the D-3 tolerance.** `3` is ruled in
  codexFactory's own CODEOWNERS-routed document.
- **It performs nothing now.** No workflow file, no test, no pin movement. Every
  box in `tasks.md` is unticked.

## Authoring decisions — put for veto, not presented as settled

**2026-09-06 — under the ratification word "ratify both when green, then land
them", decisions M-1 through M-7 below STAND AS RECOMMENDED; none is separately
ruled and no veto was exercised. Each remains one edit away.** This note answers
the section's own heading; it rewrites no decision below.

Brett Heap's word settled WHICH option to propose. It settled none of these.
Each is stated with the alternative it beat, so a veto has something to veto.
Grounds are in `design.md`.

- **M-1 — the lane's trigger is the codexFactory floor document MOVING, watched
  from this repository, plus a scheduled sweep. Recommended.** The alternative is
  for the codexFactory regeneration lane to dispatch into this repository when
  its own pull request merges. Rejected as the DEFAULT because it couples the two
  automations: a failure in one silently disables the other, and the re-pin is
  owed whether or not the regeneration was automated (a human regeneration must
  produce the same re-pin). A sweep that reads codexFactory `main` is true
  regardless of how the floor document got there. The dispatch leg is recorded as
  a legitimate accelerator a reviewer may prefer to add on top.
- **M-2 — ALL FIVE SITES OR NOTHING, enforced by a post-write re-read rather
  than by the edit succeeding. Recommended.** The lane re-reads each of the five
  sites after writing and requires all five to equal the new core commit before
  it commits anything. The alternative — trusting the five edits — is what the
  hand path already does and is precisely the step that a reviewer cannot check
  by reading. The archived companion's own task 1.2 verified all five "by reading
  it back rather than by trusting the edit"; this makes that discipline the
  lane's, not the operator's.
- **M-3 — the snapshot is re-copied from the codexFactory checkout and its
  `sha256`/`entry_count` recomputed from the written bytes. Recommended.** The
  alternative — carrying the digest and count forward from the codexFactory pull
  request's body — is refused: it would make this repository's witness a
  RESTATEMENT of a claim made in the repository being witnessed, which is not a
  witness at all.
- **M-4 — the bot's pull request is judged by the EXISTING freshness checks with
  no exemption. Recommended, and the alternative is named so the refusal is
  visible.** The alternative would be a bot-lane exemption (a skip, an allowlist,
  or a relaxed assertion for pull requests from the lane's branch). Refused
  outright: the freshness checks are the only thing that makes the vendored
  snapshot trustworthy, and an exemption keyed on the author would be the
  CSC-F16 silent-false-green shape, granted deliberately.
- **M-5 — merge authority is UNCHANGED: a human word merges. Recommended.** See
  the codexFactory packet's E-4. The App-approval question is put separately.
- **M-6 — one identity, template-only, refusing rather than falling back.
  Recommended.** The App already installed here and in codexFactory
  (`secrets.OPENXFACTORY_APP_ID` / `_PRIVATE_KEY`, minted at
  `.github/workflows/pytest-suite.yml:318-324`), needing `contents: read` on
  codexFactory and `contents: write` + `pull-requests: write` here — the workflow
  `permissions:` spelling; the App installation permission of the same capability
  is `pull_requests` in the App/API vocabulary. Declared as a
  binding template under `credential-contracts`, no live value. The alternative —
  `|| github.token` fallback, the pattern `pytest-suite.yml:400` uses — is
  refused for THIS lane: there the fallback degrades a `continue-on-error` step
  whose absence is caught by a named-testcase assertion, whereas here it would
  degrade to an identity that cannot read codexFactory at all and the lane would
  report "nothing to move" and exit green.
- **M-7 — the pull request moves the pin and NOTHING else. Recommended.** No
  README line, no dashboard, no ideation note, no unrelated formatting. The
  alternative — letting the lane also append the pin file's comment-history
  paragraph, which every hand advance has written — is REFUSED and the cost is
  stated: eight advances of narrative history stop accruing, and the record of
  WHY an advance happened moves to the pull-request body and the codexFactory
  regeneration it names. That is a real loss of a real practice, and it is put
  for veto rather than smuggled: a reviewer may prefer a lane that appends a
  templated paragraph, at the cost of a machine writing prose into a governance
  document.

## Impact

- **The floor does not move.** No entry is added, removed or reordered by this
  packet or by the lane it proposes; a graced path never becomes an entry; the
  enumeration stays exact and codexFactory stays its sole author.
- **The witnesses keep their meaning.** `floor_snapshot.sha256` and
  `entry_count` continue to read the floor's DECLARED ENTRIES and continue to be
  recomputed from the copied bytes; the byte-for-byte comparison against the
  pinned core is untouched; `EXPECT_SKIPPED` does not move.
- **The required lane's strictness is unchanged**, for everybody including the
  bot.
- **It is inert until it is realized, and half-inert until the codexFactory lane
  lands** — with the re-pin automated and the regeneration still a hand act, the
  cycle is halved, not closed. Stated without hedging, in the same terms the
  codexFactory packet uses about itself.
- **It discharges nothing else.** CSC-C6's required-check home, LA-C1's ordering
  condition, `add-substantive-review-lane` task 5.1's ruleset half and the
  `add-wallet-carried-review-authority` residue are untouched and must not be
  cited as affected.
