# Second approval act — add-credential-escrow-checkout, 2026-08-28

Status: record
Kind: report
Captured: 2026-09-05, in lane `openxfactory-1` (session `5e783e4d`), on branch
`fix/restore-origin-add-credential-escrow-checkout`. Refs #709.

**This file is the home of text that was written into a ratified origin
declaration and has been moved out of it.** It records the SECOND approval act
of 2026-08-28 — the act that closed this packet's veto window — verbatim as it
was written, with its date, its author, and the commit it came from. Nothing is
summarised and nothing is dropped: the origin declaration is restored to its
ratifying bytes and the act it later acquired lives here instead.

## Why the text moved

`openspec/specs/release-realization/spec.md` § "Origin retention at archive":
*"Mutation of an origin declaration after ratification SHALL be rejected at the
archive gate."* An origin declaration is fixed at ratification; it records the
act that ADMITTED the packet, and it is not a running log of later acts.

- **Ratifying commit:** `0e2de331` (2026-08-28, *"A ratified boundary left three
  blanks; the checkout packet fills them"*) — the first commit whose
  `openspec/changes/add-credential-escrow-checkout/proposal.md` carries
  `Status: ratified`, resolved by `scripts/proposal-support.py`
  `ratifying_commit()`.
- **Mutating commit:** `f5e53364` (2026-08-28 21:25:37 -0400, brettheap,
  *"The veto sent the schema back, so the packet's delta names six record kinds
  and its own record says who moved it"*) — the only commit after ratification
  that changed this file's bytes. In `origin.reason` it made two insertions
  of 20 and 4 lines (24 lines total); in `origin.approved_by` it rewrote 2
  lines into 9. Net growth of the whole `origin:` block is 31 lines (33
  added, 2 removed) — `git diff -U0 03244fad f5e53364 --
  openspec/changes/add-credential-escrow-checkout/.openspec.yaml`.

## The act itself

**Who:** Brett Heap (repository owner), by four multi-choice selections put to
him by the orchestrating session over openxFactory pull request **#479** and
relayed the same day.
**When:** 2026-08-28 — later the same day as the first act, which is the one the
ratified `origin.approved_by` describes.
**What it did:** closed the veto window opened by the first act, and MOVED DELTA
TEXT — ruling A's escrow relationship block and the escrow-entry record kind
came into this packet rather than its successor.

## The moved text, verbatim

### 1. Added to `origin.reason` after the line "THE FOUR RULINGS, as selected." (`f5e53364`)

> A SECOND ACT THE SAME DAY, ON THE SAME MECHANISM, CLOSED THE VETO WINDOW
> AND CHANGED THE PACKET. The orchestrating session put a further four-question
> multi-choice to Brett over pull request #479 and relayed it the same day.
> OD-2 was VETOED — ruling A's escrow relationship block and escrow-entry
> record kind come into THIS packet on A's literal shape, and Brett accepted
> the stated consequence that realization now owes the additive contract cut at
> the NEXT ADDITIVE MINOR, whose number is allocated at realization by merge
> order and is deliberately not spent here. OD-4 was APPROVED as authored. OD-1, OD-3,
> OD-5, OD-6 and OD-7 were CLEARED as authored, with OD-3's deferral of ruling
> C — the registry home, the grandfathered openxpki exception and the three
> escalation tests — expressly STANDING: only the SCHEMA HALF moved here. All
> five open questions were ruled, four of them on this packet's own
> recommendations and ONE AGAINST IT (the drill must also prove a live refusal,
> where the packet had recommended proving refusals by fixture only) — recorded
> as a reversal rather than smoothed into agreement. Merge on green was
> approved, to be performed by the orchestrating session; realization stays a
> later commission because the drill needs Brett's hands on real material.
> THE TWO ACTS ARE KEPT DISTINCT because they authorized different things: the
> first ADMITTED the packet and ratified the four rulings below; the second
> CLOSED the veto window and MOVED DELTA TEXT.

### 2. Added to `origin.reason` after ruling A's citation of `contracts/manifest.yaml` (`f5e53364`)

> AS AUTHORED THIS PACKET CARRIED NONE OF A, on OD-2, deferring both halves to
> the successor; the OD-2 VETO of the same day reversed that, and A is realized
> here in full as a MODIFIED block (the schema owns six kinds, not five) plus
> two ADDED requirements.

### 3. Added to `origin.approved_by` (`f5e53364`)

> THAT VETO WINDOW IS NOW CLOSED, by the second act recorded in the reason
> above. All seven orchestrator decisions are ruled and all five open questions
> answered: the policy-window numbers were APPROVED as authored and the
> no-schema decision was VETOED. The paragraph above is kept in its original
> tense because it records what the FIRST citation covered, which is what a
> later reader needs from it; what the SECOND act covered is stated separately
> so the two are never read as one approval.

### 4. The two ratified lines `f5e53364` rewrote, and their restoration

`f5e53364` also re-tensed the closing sentence of `origin.approved_by`. The
RATIFIED wording, restored by the commit carrying this record, is:

> the authoring session and stays FLAGGED FOR VETO there, as do the open
> questions, each of which carries a recommendation and no decision.

The wording `f5e53364` put in its place, removed by that restoration and kept
here so no version of the sentence is lost, is:

> the authoring session and WAS FLAGGED FOR VETO there, as were the open
> questions, each of which carried a recommendation and no decision.

The present-tense ratified sentence is true OF THE FIRST CITATION, which is
what the origin declaration records. That the window has since closed is the
subject of this file.

## What did NOT move, and why

`f5e53364` also rewrote the trailing comment on the first `related:` entry
(`add-credential-escrow-registry`) to say that the escrow relationship block and
the escrow-entry record kind are NO LONGER the successor's. `related:` is
outside the `origin:` mapping — the retention rule and the gate both read the
origin declaration — and that comment is a live cross-reference that is now
correct and would be FALSE if reverted, because this packet's own delta carries
both halves. It is kept as it stands.

## Where this act is also recorded

The act was never confined to the origin declaration, so restoring the
declaration removes no unique copy of it:

- `proposal.md:5` — the `Ratified:` header block, from **"A SECOND ACT LATER THE
  SAME DAY CLOSED THE VETO WINDOW AND CHANGED THIS PACKET'S SHAPE."**
- `proposal.md` § Orchestrator decisions — the per-decision rulings.
- `tasks.md` header — *"THIS FILE CHANGED SHAPE ON 2026-08-28"* — and § 1.1,
  § 2.5 and § 3.1, which name the veto as the mover (§ 1.5 and § 1.7 do not:
  neither names the veto or OD-2 — `grep -n 'veto\|OD-2'
  openspec/changes/add-credential-escrow-checkout/tasks.md`).

## Disposition

Restoring a post-ratification origin mutation is a contested-class act requiring
an explicit disposition (`release-realization` § "Origin retention at archive";
the gate has no bypass flag). The disposition is **Brett Heap, 2026-09-05:
*"restore all four, land them when green"*** — recorded on openxFactory issue
**#709**, over the four packets that #695's active-corpus sweep read as REFUSED.

Verification on the tree carrying this record:

```console
$ diff <(git show 0e2de331:openspec/changes/add-credential-escrow-checkout/.openspec.yaml) \
       openspec/changes/add-credential-escrow-checkout/.openspec.yaml
97c97
<   - openxFactory:change:add-credential-escrow-registry      # ... the escrow relationship block, the escrow-entry record kind, ...
---
>   - openxFactory:change:add-credential-escrow-registry      # ... NO LONGER the escrow relationship block or the escrow-entry record kind ...
```

The `related:` line above is the one deliberate difference, stated in § What did
NOT move. The `origin:` mapping is byte-identical, which is what the gate reads:

```console
$ ORIGIN RETAINED add-credential-escrow-checkout (declaration unchanged since the ratifying commit 0e2de3313e0c)
```
