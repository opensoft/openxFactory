# Proposal Ratification: register-gate-rules-council-seats

Status: ratified

Decision date: 2026-09-06

Ratifier: Brett Heap (repository owner) — in-session, lane
`hermes-wallet-exercise`, on the recorded word.

Ratified: 2026-09-06 by Brett Heap (repository owner) — in-session at
2026-09-06T14:13:46Z, verbatim: **"lets take them in your recommended order
all approved"** — given against the lane's board, whose item 3 read *"Ratify
openxFactory #717 with rulings on Q-GRC-1 to Q-GRC-5."* Each question carried
one recommendation; each is ruled as recommended.

Ratified baseline: head `169f84ef8e4bf342bc6a7f8cbf2232e1a2632501` —
"Declare the packet's origin: the OQ-C ruling queued it by name" —
`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, and
`specs/review-authority-intake/spec.md` (**SEVEN ADDED requirements, 21
scenarios**; one `## ADDED Requirements` heading, no `## MODIFIED` and no
`## REMOVED` block) as they stood at that commit. Measured rather than
asserted: `git diff 169f84ef -- openspec/changes/register-gate-rules-council-seats/specs/
openspec/changes/register-gate-rules-council-seats/design.md
openspec/changes/register-gate-rules-council-seats/tasks.md
openspec/changes/register-gate-rules-council-seats/.openspec.yaml` is EMPTY at
the recording commit — a catch-up merge of `origin/main` (four commits, none
touching this packet's own directory) rides in the same act, and it moves no
line of this change's own content.

Recorded at:
<https://github.com/opensoft/openxFactory/pull/717#issuecomment-5559795182>
(posted 2026-09-06T14:13:48Z, stating its own ruling time as
2026-09-06T14:13:46Z).

Lane: `hermes-wallet-exercise`

## Decision

**RATIFY**, at head `169f84ef`, the **SEVEN ADDED requirements** this change
adds to the new capability `review-authority-intake` — as written, unamended.
**FIVE OPEN QUESTIONS ARE RULED IN THE SAME WORD**, each as its own
recommendation, and none is reopened.

**The word carries two further acts, and this record carries all three that
land here.** It (1) ratifies the packet, (2) rules Q-GRC-1 through Q-GRC-5, and
(3) approves the eventual merge of PR #717 in the same sentence — *"Merge is
approved in the same word"* (Rule 6). **This record performs only the first
two.** The merge itself is a separate act, executed by whichever session takes
the Lane Collision Protocol Rule 6 landing window (a `LANDING` post on this PR
and in `LANES.md`, then `LANDED` at the merge sha) — it is not performed by
these recording acts, per this task's explicit instruction.

## What is ratified

`register-gate-rules-council-seats` is the **S5 register-act family** change
that codexFactory PR #165's OQ-C ruling (Brett Heap, 2026-09-05T17:15Z,
<https://github.com/opensoft/codexFactory/pull/165#issuecomment-5553459343>)
QUEUED by name: *"operator ratification now, seats later … Registering
gate-rules seats … is QUEUED as its own S5-family openxFactory change so later
convenings are signed."* It adds **SEVEN ADDED requirements** to
`review-authority-intake` (no `## MODIFIED`, no `## REMOVED`): a second
commissioned body enters the register as its own authority row; seat identity
is the pair (`council_id`, `seat_id`); an uncomposed body is not issued review
authority; a symbolic seat and a persona with no seat identifier are not
registered until the council seats them by identifier; the rule-setting body
never clears a candidate touching the register or the artifacts conferring its
own authority; a register act the pinned reader cannot represent is sequenced
behind the reader and never worked around; and one staleness bound governs the
whole register.

**This packet performs nothing.** No key is minted, no wallet, grant,
attestation or register row is written, no pin is advanced, no workflow
assertion is moved. `governance/review-authority/` carries no diff at the
recording commit (measured: `git diff 169f84ef -- governance/review-authority/`
is empty).

## The five rulings

Each question carried one recommendation on record in `proposal.md`; the word
rules each as recommended, verbatim from the ruling comment:

- **Q-GRC-1 RULED — (i):** mint the four private halves into codexFactory's
  `worker-credentials` now, `holder_readable`; the custody attestation names
  the OWED job (codexFactory task 5.9a) as the holder execution context and
  states plainly that it does not exist yet.
- **Q-GRC-2 RULED — pin the composition exactly, from the same enrolled
  roster** (Q8(d) of 2026-08-26 stands; not reopened). The two-body coupling is
  accepted openly: a roster pin flip revokes both bodies' grants and parks
  both; re-issuance is a scheduled two-body ceremony with one walk record per
  body.
- **Q-GRC-3 RULED — `expires_at: 2027-06-30T00:00:00Z`**, the same date as
  `grant-mrc-0002`, so one re-issuance ceremony covers both bodies.
- **Q-GRC-4 RULED — register neither deferred seat now; delete neither.**
  `intent_owner_role_slot` and `client-security-compliance-officer` are
  recorded as owed registrations that trigger on a codexFactory roster act,
  which must register the key in the same governed act.
- **Q-GRC-5 RULED (as this change's recorded ask of openXwallet) — replace the
  scalar cap with the invariants it stood in for**: every row resolves end to
  end; every seat entry attaches to a row that commissions its body;
  (`council_id`, `seat_id`) is unique. openXwallet decides in its own change.

**Nothing in the packet's own text moves as a result.** Every ruling above
adopts the recommendation `proposal.md` already carried; no edit is owed to the
open-questions section, `design.md`'s D1–D7, or the spec delta.

## What this ratification authorizes

**The realization sequence, and it performs none of it.** `proposal.md`'s own
§ "Sequencing, restated as a single order" stands as this ratification's
authorized order, unedited:

1. **openXwallet** — the reader widening, red-first (tasks §2), its own
   OpenSpec change and bundle tag.
2. **openxFactory** — the pin advance (`commit:`, `contract_bundle_tag:`) plus
   the consumer gate's literal assertions, one pull request, human-landed by
   construction (both paths are never-clearable floor members).
3. **codexFactory** — the `gate_rules_council` composition source map and
   agent-mix profile (Q-GRC-2), before the grant is issued.
4. **Brett's walk** — mint, attest, grant, row, in that order, one walk record
   (tasks §3), on the permanently human-only surface.
5. **hermes-install / operator** — the projection refresh (`seat_count` 4 → 8;
   `councils` gains `gate_rules_council`).
6. **codexFactory** — the caller that convenes gate-rules and returns signed
   seat returns (task 5.9a) — the first signed convening.

Steps 1–2 have no valid interleaving with step 4, per the packet's own
measured finding (a second row cannot land while the pinned reader still
carries `REGISTER_MVP_SINGLE_ROW = 1` and a global seat-name duplicate check).

## What this ratification does not do

**Not approved by this word** — quoted directly from the ruling: *"any mint,
wallet, grant, attestation or register row — those are Brett Heap's operator
acts in the walk, on the human-only surface."* In addition:

- **It does not merge PR #717.** The word approves the merge, but performing
  it is a separate act under Lane Collision Protocol Rule 6, not one of these
  recording acts.
- **It does not advance `contracts/openxwallet-pin.yaml`** or move the
  consumer gate's literal assertions — that is tasks §2, gated on the
  openXwallet reader widening landing first.
- **It does not author the `gate_rules_council` composition source map** or
  `review_council_profiles` entry in codexFactory — that is task 3.1,
  prerequisite to the grant.
- **It does not register `intent_owner_role_slot` or
  `client-security-compliance-officer`.** Q-GRC-4 rules that neither is
  registered now and neither is deleted; both remain owed, triggered on a
  codexFactory roster act.
- **It does not reopen Q8(d)** (2026-08-26, exact model versions only) — Q-GRC-2
  says so explicitly.
- **It does not close the floor-reachability gap** the proposal names at
  `split-openxwallet-repo` §8.3 — the proposal states plainly it is not
  declared closed, and this ratification does not change that.

## Review history

No adversarial round was run on this packet by this lane; the ruling was given
directly against the recommendations already on record in `proposal.md`. Bot
state at the ruling: **Sourcery** commented that the private repository lacks
Sourcery access (no review performed); **Copilot** (`copilot-pull-request-reviewer`)
posted two suppressed (non-blocking) comments — `target_release: none` reads as
out-of-vocabulary against `release-realization`'s `implemented`/named-release
pair, and the mint runbook's `tee` pipeline could mask a validator's exit code
without `pipefail`. **Neither was fixed here.** The ruling did not ask for
either change, and this record's brief is explicit: change nothing in
`proposal.md` beyond `Status:` and `Ratified:` — the ratified text is the
record. Both remain open observations for a future edit, not blocking
findings.

## Check state at the ratified head

**All nine checks green at `169f84ef`** (re-read via `gh pr checks 717`):
`clearing-dispatch-gate`, `lane-line`, `merge-master-approval`,
`openreposhape-pin`, `openspec-cli-pin`, `pytest-suite` (23m27s),
`release-tag-gate`, `signed-execution-chain-gate`, `wallet-validation`.
`reviewDecision` was `REVIEW_REQUIRED` and `mergeStateStatus` `BLOCKED` on the
code-owner gate only (`mergeable: MERGEABLE`).

The `pytest-suite` check run (`createdAt` 2026-09-06T10:01:20Z) predates
`main`'s most recent commit at the time of this ratification
(2026-09-06T11:52:08Z UTC), so a catch-up merge of `origin/main`
(four commits — `73c4ac46`, `31cc52b3`, `e2b8f620`, `310fd64f`; none touching
this packet's own directory, `README.md`'s conflicting hunk resolved by a clean
auto-merge in an unrelated section) rides in the same recording act, ahead of
the ratification commit, so CI is not stale at the pushed head.

## Verification (at the recording head, over the ratified baseline)

- `OPENSPEC_TELEMETRY=0 openspec validate register-gate-rules-council-seats
  --strict`: valid, zero issues.
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: **96 passed, 1
  failed (97 items)** — the one failure is `change/disposition-codexfactory-declared-renames`,
  pre-existing on `main` and unrelated to this packet.
- `python3 scripts/proposal-support.py . verify`: ok.
- `python3 -m pytest tests/sequenced_after -q`: **162 passed.**

## Next

1. **The recording acts of this ratification** — this record, `Status:
   ratified` and the `Ratified:` line on `proposal.md`, the Phase 1 ruling rows
   ticked in `tasks.md`, and the README `OpenSpec Records` entry moved to
   `Status: ratified` — land on top of the ratified head plus the catch-up
   merge, as one commit.
2. **Merge of `opensoft/openxFactory#717`** is approved by this word but
   awaits the Lane Collision Protocol Rule 6 landing window; it is not
   performed here.
3. **Realization** per the sequencing above, as owed acts in four repositories
   (openXwallet, openxFactory, codexFactory, hermes-install/operator), after
   the merge.
4. **Archive** per `release-realization`: `code_surface` is NOT `none`, so
   archive is gated on merged-plus-green realization evidence across the
   surfaces the proposal's front-matter names.
