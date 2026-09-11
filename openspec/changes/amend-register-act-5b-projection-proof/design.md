# Design: amend-register-act-5b-projection-proof

Status: ratified
Ratified by: Brett Heap, 2026-09-11T13:09:12Z — verbatim "accept all A on 960" (record `review/ratification-2026-09-11.md`)
Kind: design
Lane: hermes-wallet-exercise

**Seven decisions, D-1 through D-7, one per open question in `proposal.md`.**
Each carries the alternative it rejects and the measurement it rests on. Each
is put for Brett Heap's ruling as multiple choice, and the RECOMMENDED option
is the one the delta already encodes — so ratifying without vetoing adopts
every recommendation and moves no byte.

## Context — what was walked, and where it stopped

On 2026-09-10/11 this lane coordinated the governed re-issuance of
`gate_rules_council`'s holder end to end. The procedure it walked is
`docs/governed-reissuance-runbook.md`, pointed at by codexFactory
`clarify-gate-rules-decline-position` `tasks.md` §3 and summarized in that
packet's `design.md` § D4 as steps 1 → 5 → 5b.

Step 5 landed: openxFactory PR #941 →
`f0eea7ed1af5a3b7cc247adc8316e04e4b610dc0` (**T2**, 2026-09-11T02:29:10Z)
revoked `grant-grc-0001`, minted `grant-grc-0002` and repointed `row-grc-0001`.

Step 5b did not. The walker read the runbook's exit condition — §5.2 step 3,
*"VERIFY ONE CONVENING ADMITS"* — traced it into shipped code, and found the
route does not reach the artifact it is supposed to prove. The reasoning is at
the walk record §13.2 and is not re-derived here; it is summarized in
`proposal.md` § Why and cited to the landed record rather than to this design.

**THE STOP WAS THE RIGHT MOVE AND IT IS WHY THIS PACKET IS NARROW.** Had the
walker dispatched, the runtime would have answered 201, the record would have
read the admission as the projection proof, and the re-issuance would have
closed on a projection that still carried the revoked grant. The packet's whole
subject is that one exit condition; everything else about the re-issuance
worked.

## D-1 — The exit condition becomes an observation of the projection — RULED A, 2026-09-11T13:09:12Z

**RECOMMENDED: option A.** The projection step exits on a direct observation of
the published register projection's declared source revision, at or after the
register act's landed commit.

**Why, in one measurement.** The register projection is read at VERDICT
CONSUMPTION and nowhere in the admission path; a lane that convenes no seat
never reaches verdict consumption; therefore the admission of a convening is
independent of grant state in both directions. The 2026-09-11 record carries
both directions as observations rather than as argument: run `34561266626` was
refused for a reason that has nothing to do with the register
(`council.self_review_refused`, §14.3) and run `34586762846` was admitted
against a projection whose source revision the lane had ALREADY observed
separately (§15.2). Neither outcome moved with the register.

**Alternative rejected — B, a reachable gate-side check.** It is the right
long-run answer and it does not exist. Nothing in this repository can see
cluster state: no commit, no required check and no artifact carries the
projection's content, which is the same fact §13.2 states as *"there is no
GitHub-visible artifact of the register projection's live content."* Adopting B
today leaves step 5b unexitable until phase 6 is gated, which is the outcome
the disposition was raised to end. **B is named as the successor** rather than
refused on its merits.

**Alternative rejected — C, drop the exit condition.** The runbook's own §4
says *"The only exit is step 5 and step 5b together."* Downgrading 5b to record
evidence contradicts that sentence and leaves a re-issuance able to close with
the runtime still refusing on a stale projection — which the runbook's §5.2
calls *"the commonest way to think this runbook is finished when it is not."*

**Alternative rejected — D, keep the wording and defer.** It preserves the
manufactured-clearance hazard for as long as phase 6 stays ungated, and the
hazard is not hypothetical: the walk record's §13.2 computed the exact green
the deferred wording would have produced.

## D-2 — The observation proves by SOURCE REVISION, and names what it did not read — RULED A, 2026-09-11T13:09:12Z

**RECOMMENDED: option A.** The declared source revision alone is the exit test;
the row-level confirmations are named as OWED with an owner.

**Why.** It is what was proved. §14.1's own stated limit reads: *"This read
establishes 5b BY SOURCE REVISION … those three fields were NOT separately
read … it is recorded as owed rather than quietly treated as covered."*
Requiring more than the precedent did would make the landed walk retroactively
non-conformant with the requirement written from it, which is a shape this
estate has refused before.

**Alternative rejected — B, mandate the row-level fields.** Strictly stronger
and defensible; the cost is that it needs an explicit sentence preserving the
2026-09-11 precedent, and it raises the cluster-read surface from one
annotation to the projected rows, which is a wider read for a marginal gain
while the refresher's fidelity to its input is itself gated elsewhere.

**Alternative rejected — C, observer's discretion.** A bar the observer chooses
is not a bar, and the fourth requirement (*states the limit of what it
establishes*) already carries the honest-reporting half without making the
depth optional.

## D-3 — Neutral in the requirement, concrete in the runbook — RULED A, 2026-09-11T13:09:12Z

**RECOMMENDED: option A.** The requirement says *"the published register
projection's declared source revision"*; the runbook says ConfigMap
`hermes-register-projection`, annotation `hermes.opensoft.one/source-revision`.

**Why.** Working rule 1: openxFactory owns domain-neutral contracts, and the
projection's deployment shape belongs to hermes-install, which moved it as
recently as the 2026-09-10 refresher-installation split. A requirement pinned
to a ConfigMap name is a requirement that a deploy change can falsify.

**Alternative rejected — B, concrete in the requirement.** More useful to a
walker and more brittle to a deploy; the runbook is the right place for the
useful-and-brittle half, because it is the document the walker has open.

**Alternative rejected — C, neutral everywhere.** Leaves the walker to identify
"the declared source revision" unaided, which is how a step gets satisfied by
the wrong field.

## D-4 — The precondition is an EVENT, not a clock — RULED A, 2026-09-11T13:09:12Z

**RECOMMENDED: option A.** A refresh cycle that COMPLETED after the act landed,
evidenced by the refresher's own success record; and §5.2 step 2's stale
sentence corrected in the same edit.

**Why, and it is the sharpest thing in the packet.** Currency is not content.
The declared bound (`revocation_staleness_bound`, today `P7D`) governs how long
a revocation may go unhonoured. It says nothing about whether a particular act
is in the projection. §13.2's computation is the worked example: the live
projection at 02:5xZ was about 45 minutes old, *"nowhere near"* the bound, and
derived from a revision at which `grant-grc-0001` was still active. **A
projection can be perfectly current and completely wrong about the act you just
landed.** So the precondition is a completed cycle, and the evidence is the
refresher's own record of it — Job `hermes-register-projection-refresher-29818320`,
created 2026-09-11T04:00:00Z, `succeeded=1`.

**The stale sentence rides with it.** §5.2 step 2 reads *"it is loose on
purpose because nothing refreshes the projection automatically."* Measured
2026-09-11: `hermes-register-projection-refresher` runs `0 */2 * * *` and its
04:00Z cycle is what the walk waited on. Leaving that sentence beside a new
precondition that depends on the refresher existing would put the runbook in
contradiction with itself in adjacent paragraphs.

**Alternative rejected — B, name the cadence.** `0 */2` is hermes-install's to
change and has changed; a requirement that names it goes stale silently.

**Alternative rejected — C, silence.** Reproduces 2026-09-11T02:5xZ exactly.

## D-5 — A named operator's word naming a named lane, read-only, recorded — RULED A, 2026-09-11T13:09:12Z

**RECOMMENDED: option A.**

**Why.** The observation crosses a boundary the rest of the procedure does not:
out of the governed tree, into a running system. The 2026-09-11 read is
auditable precisely because both halves were named — the word (*"Operator word:
hermes-wallet-exercise reads it"*, 03:01:28Z) and the lane
(`hermes-wallet-exercise`) — and because every verb was a `get`. Requiring the
record to carry the commands and the values is what makes a later reader able
to disagree with it.

**Alternative rejected — B, a standing ceremony word.** Convenient, and it
dissolves the named act into a class of acts; the audit value was in the
naming.

**Alternative rejected — C, the operator personally.** Correct and
unavailable — it is the bottleneck the named-lane shape exists to relieve, and
the operator's word is already the authority under A.

## D-6 — `## ADDED`, and the archive does not overtake the parents — RULED A, 2026-09-11T13:09:12Z

**RECOMMENDED: option A.** The delta is `## ADDED` because there is no promoted
`review-authority-intake` specification to modify; `sequenced_after:` declares
both parents and `tasks.md` §5 holds the archive behind
`add-wallet-carried-review-authority`.

**Why the class is forced.** Measured 2026-09-11 on `main` `78d2c6f5`:
`openspec/specs/` has no `review-authority-intake` directory; the capability is
authored by two ACTIVE changes, `add-wallet-carried-review-authority` (19
requirements between them) and `register-gate-rules-council-seats`. A
`## MODIFIED` block would have no base block, and the archive would have
nothing to replace.

**Why the ordering is put at all.** If this packet archived first it would
CREATE `openspec/specs/review-authority-intake/spec.md` containing four
requirements about a projection step and none of the capability's substance — a
promoted file that misrepresents its own capability until its parents land.

**Alternative rejected — B, archive whenever ready.** Cheaper and produces that
misleading intermediate state.

**Alternative rejected — C, hold the packet.** Leaves the defective runbook
sentence in force for as long as the parents take, and the parents are gated on
operator acts and an openXwallet reader widening.

## D-7 — `review-authority-intake`, in openxFactory — RULED A, 2026-09-11T13:09:12Z

**RECOMMENDED: option A.**

**Why.** The capability already owns the register (*"The intake register is a
permanently human-only surface"*), the bound (*"One revocation staleness bound
governs the whole register"*, *"Revocation is re-checked at verdict consumption
against a declared staleness bound"*) and the event (*"A reviewing holder's
composition is pinned, and a composition roll is a governed re-issuance"*).
Step 5b is the last unowned step of that same act.

**Alternative rejected — B, `roles-authority-model`.** It owns route/park/
interrupt, and the park is the CONSEQUENCE of a stale projection rather than
its subject. Nothing in that capability names a register or a projection.

**Alternative rejected — C, codexFactory `domain-hermes-content`.** A domain
repository would be authoring a neutral contract, against working rule 1; and
the sentence being amended is not codexFactory's.

## What this design does not decide

* **Whether the gate-side check of D-1 option B should be built.** It is named
  as the successor and left unproposed; no owner is assigned here.
* **Whether the refresher is faithful to its input.** D-2's owed fields are the
  only place that question touches this packet, and it is recorded rather than
  answered.
* **Anything about the 2026-09-11 walk record's content.** It is `Status:
  record` and this packet cites it; it does not edit it.
