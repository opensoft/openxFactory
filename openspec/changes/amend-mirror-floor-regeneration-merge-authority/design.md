# Design: amend-mirror-floor-regeneration-merge-authority

Status: ratified
Ratified by: amend-mirror-floor-regeneration-merge-authority — 2026-09-08, Brett Heap,
verbatim "merge 292 when green, then ratify 807" (openxFactory #745 comment
5586895152; record `review/ratification-2026-09-08.md`)
Kind: design

Seven decisions, **M-A through M-G**, mirroring the seven — D-1 through D-7 —
that codexFactory's `amend-floor-regeneration-merge-authority` was ratified
under at main `93f0f0d71ed00dbb384101be779d62233f6367f5`. **Each carries a
RECOMMENDATION, and each is put for Brett Heap's veto.** None is taken by this
lane; ratifying the proposal without vetoing any of them adopts every
recommendation as written, which is the same shape `mirror-floor-regeneration-automation`'s
M-1..M-7 and `extend-merge-master-envelope-to-floor-bot-lanes`'s N-1..N-5 were
ratified in.

**They are NOT transcriptions.** Three of the seven reach a different answer
from their codexFactory counterpart, and each difference is driven by a
measurement of THIS repository rather than by preference: **M-B** picks a merge
method where codexFactory had only one available; **M-C** adds a driver-side
control codexFactory already had; **M-D** finds four refusals where codexFactory
found one, recommends NO bypass actor anywhere (D-4 (i) was WITHDRAWN on
2026-09-08, and its ground binds harder here), and leaves the COMPLETION PATH
open for a word where D-4 recommended a single owner's click.

## 1. The two sentences, and the sweep that enforces one of them

| sentence | where | ratified |
|---|---|---|
| the lane *"MUST propose the advance as a pull request and MUST NOT dispose of it: it SHALL NOT merge, SHALL NOT approve, SHALL NOT push to this repository's default branch …"* | `mirror-floor-regeneration-automation/specs/review-lane-floor-mirror/spec.md:5` | 2026-09-06, PR #708 |
| the codexFactory twin, NARROWED: *"MUST NOT dispose of it by its own act: it SHALL NOT merge by its own act and SHALL NOT approve; it MAY arm the platform's auto-merge …"* | codexFactory `openspec/changes/amend-floor-regeneration-merge-authority/specs/repository-gate-floor/spec.md` | 2026-09-08, `93f0f0d7` |

The bar in this repository is swept in code, over the shell the runner executes
(not the file's prose — `_active()` strips whole-line comments precisely because
`review-lane-repin.yml` argues its own case at length in its header):

`tests/review_lane_pin/test_repin_lane.py::AnAutomatedPinAdvanceOnlyEverProposes::test_the_lane_opens_a_pull_request_and_stops_there`
requires `gh pr create` to be present and asserts the ABSENCE of ten terms —
`gh pr merge`, `gh pr review`, `gh pr close`, `--auto`, `--admin`,
`enable-auto-merge`, `--method PUT`, `-X PUT`, `/reviews`,
`enablePullRequestAutoMerge` — plus `assertNotRegex(shell, r"gh api[^\n]*pulls/[^\n]*/merge")`.
**Flipping exactly two of those ten, for the one target the sweep reads, is the
whole of this packet's own code surface.**

## 2. What the narrowing is, and what it is not

**It moves the boundary from "the lane may not cause a merge" to "the lane may
not BE the merge",** in the same words its twin uses. The lane's last act keeps
the shape it has today: it resolves codexFactory's default branch, writes and
re-reads five sites, opens or updates ONE pull request on `bot/review-lane-repin`,
and stops. What it may additionally do is record, with the platform, a standing
instruction that the PLATFORM — not the lane — completes the merge if and when
every rule this repository declares is satisfied.

Two properties make that a small step, and both are measured rather than argued:

1. **"SHALL NOT hold any authority over the pin that the equivalent hand act does
   not already have" survives untouched, and it is satisfied.** A human code
   owner advancing the pin by hand may merge their own pull request. The lane,
   after this narrowing, still may not — it may only ask the platform to merge
   when SOMEONE ELSE has approved. The automated path stays strictly weaker than
   the hand path it replaces.
2. **The disposal that was forbidden is still forbidden where it matters.** The
   DRIVER, `scripts/review_lane_repin.py`, gains nothing; the workflow gains one
   line, in one exact form; and M-C adds the control that measures the driver
   half, which this repository's sweep does not read today.

## 3. The decisions

### M-A — WHERE the arming happens, and why arming before an approval is safe

**RECOMMENDATION: arm immediately after the pull request is opened or updated,
inside the existing "Open or update the single automated advance" step
(`.github/workflows/review-lane-repin.yml`, step 6), on the same App token, as
`gh pr merge --auto --squash "${BOT_BRANCH}"` — idempotently, on BOTH the
`gh pr create` path and the `gh pr edit` path.**

*Why it is safe before any approval exists.* `--auto` performs no merge. It
records an intent GitHub executes only when every merge requirement this
repository declares holds at once: the approving review count (`1`, ruleset
`18962101`), `require_last_push_approval`, the code-owner review (`18834180`),
the required status checks `signed-execution-chain-gate`, `lane-line`,
`wallet-validation`, `pytest-suite` and `release-tag-gate` (rulesets `21957695`
and `21538893`), and mergeability itself. There is no window in which arming
merges something an approval has not released — the platform, not the lane, holds
the predicate.

*What a PARK, or the absence of any approver, does.* Nothing fires. The pull
request stays open exactly as it does today, and the lane's next firing finds it
and takes the update path (single-flight, the parent's trigger-and-idempotence
requirement). **Today that is not the edge case but the ONLY case** — see M-D —
which is precisely why the recommendation is safe to land ahead of the enrolment:
an inert arming is indistinguishable in outcome from today's behaviour, and
deleting the one line returns the lane to the human gate in a single
code-owner-reviewed edit.

*Why BOTH paths, and idempotently.* GitHub disables auto-merge when a pull request
becomes unmergeable, and this lane's update path exists precisely for the case
where the advance moved while a pull request was open. Re-arming on every delivery
costs one API call and removes a state where an armed intent was silently dropped.
`gh pr merge --auto` on an already-armed pull request is a no-op.

*WHAT AN UPDATE DOES TO AN ALREADY-ARMED PULL REQUEST — MEASURED, because
Codex's review of this packet (2026-09-08, P1) was right that the requirement as
first drafted forbade the very update the parent obliges.* The parent's
*The automated advance lane is triggered by the pinned core's own movement and
every firing is idempotent* requires a firing that finds an open advance to
UPDATE it rather than open a second, so an armed pull request must remain
updatable; the spec delta now says so in terms, and the prohibition it carries is
on a second ROUTE TO THE MERGE rather than on the lane's own delivery. What
happens to the armed state on that update is the platform's answer, and it is
documented: *"Auto-merge is disabled if someone without write permissions pushes
new changes to the head branch or switches the base branch"*
(`github/docs@main`, `content/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request.md:23`;
the same page states *"People with write permissions to a repository can enable
auto-merge for a pull request"*). **The condition is the pusher's permission, and
this lane's pusher HOLDS write**: `.github/workflows/review-lane-repin.yml` mints
its installation token with `permission-contents: write` and
`permission-pull-requests: write` (lines 219-220), so an update pushed by the
lane is not a push by an actor without write permission and does not disable the
arming. **The recommendation does not rest on that**: re-arming happens on BOTH
paths unconditionally, so the outcome is identical whether the platform kept the
intent (the call is a no-op) or dropped it (the call restores it), and the lane
never has to reason about which. The one thing an update genuinely does lose is
the APPROVAL, by the two rules named in the next paragraph — which is the
intended behaviour and the scenario that states it.

*The head-movement consequence, and how it differs from codexFactory's.* This
repository's required-check rulesets both declare
`strict_required_status_checks_policy: false`, so — unlike codexFactory, whose
D-1 records a mandatory up-to-date push as the head-mover — nothing here forces
a bot pull request to be brought up to date before merging. The head still moves
whenever the lane takes its own update path (a two-parent `commit-tree` push, no
force), and ruleset `18834180`'s `dismiss_stale_reviews_on_push: true` plus
`18962101`'s `require_last_push_approval: true` dismiss the approval when it does.
So the scenario *A head that moves after an approval is not merged on that
approval* is enforced BY PLATFORM RULE here as it is there, by a different route,
and it is a latency cost rather than a correctness one.

*One reported risk to the arming itself, stated rather than discovered.*
Community discussion
[#190610](https://github.com/orgs/community/discussions/190610) reports that
since 2026-03-25 enabling auto-merge fails with **HTTP 422 until all merge
requirements are already met**, with a GitHub staff acknowledgement the same
week. If that is still live, `gh pr merge --auto` at open time — the very thing
"arming before an approval is safe" relies on — ERRORS rather than recording an
intent, and the realization must decide whether the arming step is
`continue-on-error` with a named witness or a hard failure. **Unverified here; no
arming was attempted.** It is measured by M-D's precondition (1) on the same
throwaway pull request, and until it is, § 3.1 must not be written as if the call
always succeeds.

**Alternatives put and not recommended:** arm in a separate step gated on the
envelope's verdict (it makes the lane read another lane's decision, and it would
arm nothing on the very cycle the approval arrives); arm from the merge-master
lane instead (that lane APPROVES; giving the approver the merge collapses two
identities into one and is exactly what *"an autonomous approval is not a merge"*
refuses); arm only once the enrolment successor lands (defensible, and it is the
honest alternative to landing an inert line — but it splits one narrowing across
two realizations and leaves the flipped sweep with nothing to measure, so the
recommendation is to land the arming inert and say so).

### M-B — The merge method, and the lane line

**RECOMMENDATION: `--squash`, and leave the squash commit's message at the
platform default.**

**This is a real choice here and was not one in codexFactory.** Measured
2026-09-08: `opensoft/openxFactory` has `allow_merge_commit: true`,
`allow_squash_merge: true`, `allow_rebase_merge: true`, and both `pull_request`
rules allow all three; `opensoft/codexFactory` has only `allow_merge_commit`, so
its D-2 recommendation of `--merge` was the single available method rather than a
preference.

Squash is recommended on the lane's own measured precedent and on one structural
ground. The precedent: openxFactory PR **#732**, the only `bot/review-lane-repin`
pull request ever merged, merged as `9ffc6252` with **one parent** and a title
ending `(#732)` — a squash, chosen by the human who merged it. The structural
ground: the lane advances an open pull request with a **two-parent `commit-tree`**
whose first parent is the remote tip (that is how it avoids ever force-pushing).
A `--merge` would carry those synthetic bookkeeping commits onto `main`; a squash
lands the advance as the one commit the pull request is, which is what every
hand-merged advance in the pin file's history looks like. `--rebase` is refused:
it rewrites the bot's commits and would fight the no-force delivery idiom.

On the lane line: `.github/workflows/lane-line.yml:15` exempts Bot authors by
`github.event.pull_request.user.type != 'Bot'`, and the lane's own COMMITS
already carry `Lane: review-lane-repin-bot` (written into `MSG` in the delivery
step). Nothing evaluates a squash commit's message, so no trailer is owed there
and inventing one would assert a check that does not exist.

### M-C — What remains forbidden, and how the tests say so

**RECOMMENDATION: narrow exactly TWO of the ten swept terms, for the ONE target
the sweep reads, assert the admitted form by EQUALITY, and ADD the driver-side
control this repository does not have.**

Forbidden, unchanged, and each named in the requirement itself: approving under
any identity; dismissing or soliciting a review; closing the pull request;
`--admin` or any other administrative override; a direct call to a merge endpoint
(`gh api … pulls/*/merge`, `--method PUT`, `-X PUT`, `enablePullRequestAutoMerge`);
a merge queue this repository has not declared; editing a ruleset or a bypass
list; and merging a head the envelope's approval does not name.

*How the envelope binds the head.* The merge-master App submits `event=APPROVE`
against a named `commit_id`, and this repository's rulesets carry
`dismiss_stale_reviews_on_push: true` (`18834180`) and
`require_last_push_approval: true` (`18962101`). A moved head therefore
invalidates the approval BY PLATFORM RULE, not by the lane's good behaviour —
which is what makes the head-binding scenario enforceable rather than
aspirational.

*The flipped test, precisely.* In
`test_the_lane_opens_a_pull_request_and_stops_there`: `gh pr merge` and `--auto`
are admitted **only in the exact arming form, asserted by equality** — the arming
command appears exactly twice (once on each delivery path) in the form
`gh pr merge --auto --squash`, and no `gh pr merge` occurrence in the workflow
lacks `--auto`. The other eight terms and the raw-API regex stay refused.

*Three negative controls that MEASURE* — the `mirror-floor-addition-grace` lesson
(`ca9fafe6`: *"controls must MEASURE the same inputs as the shipped assertion"*,
learned in THIS repository when two controls hard-coded empty sets and so could
never have failed): one asserting the lane still names no approval verb under any
identity, varying the same input the shipped sweep reads; one that reds if a THIRD
`gh pr merge` occurrence appears in the workflow; and — **the addition
codexFactory did not need** — one that sweeps `scripts/review_lane_repin.py` for
all ten disposal terms, because `_shell_text()` reads only the workflow's `run:`
blocks and the driver has never been measured. codexFactory's D-3 could call its
driver's untouched sweep the blast-radius bound; here that bound must be created
before it can be claimed.

*One more thing the realization must not miss.*
`tests/review_lane_pin/test_repin_lane.py::EveryRatifiedScenarioHasATest` reads
the scenario titles out of `RATIFIED_DELTA` and asserts a literal count
(`24` today, over the parent's delta). The amendment adds a second ratified delta
for the same capability. **The mapping must be RE-READ, not re-pinned** — the
test says so in its own failure message — and the realization owes a test
docstring for each new scenario.

### M-D — The realization gate: four refusals, and NO bypass is recommended anywhere

**RECOMMENDATION, in three parts: (1) name an enrolment SUCCESSOR PACKET and do
not author it here; (2) recommend NO bypass actor on any ruleset, in this
repository or the org — the shape codexFactory's D-4 (i) recommended was
WITHDRAWN on 2026-09-08 and the withdrawal binds here more strongly than it does
there; and (3) leave the COMPLETION PATH open for Brett Heap's word, with the
shapes enumerated below and a precondition measured first.**

**This is where the mirror stops being a transcription.** codexFactory's D-4 had
ONE blocker with what it believed was a one-click remedy. Here there are four,
and the third one's remedy has since been withdrawn on evidence that applies to
this repository with greater force.

#### The four refusals

1. **No candidate class admits `bot/review-lane-repin`.**
   `.github/merge-approval-envelope.yml` enrols exactly one candidate,
   `intent-rolling-custody` (`expected_head_ref: intents/rolling`, allowlist
   `ideation/dashboard/intents/**` + `ideation/dashboard/gate-records/**`). The
   lane's branch and its four writable paths are none of those.
2. **The never-clearable floor is composed OVER the envelope.**
   `.github/workflows/merge-master-approval.yml:1504` parks any candidate whose
   `FLOOR_MATCHED != 0` *"whatever the envelope says"*, and
   `contracts/review-lane-pin.yaml` — which every advance writes — is a floor
   member whose stated ground is that a clearable pin *"would let a pull request
   choose its own judge"*. Clearing it needs the **N-1b (ii)** carve, authored in
   codexFactory's decision core and consumed here at a re-pin.
3. **Code-owner review is required on `main`, and no bypass grant is recommended
   to lift it.** See the measurement below; this is the refusal whose remedy
   changed.
4. **A promoted requirement forbids the approval outright.** codexFactory
   `openspec/specs/merge-master-approval/spec.md` § *Bounded autonomous surface*
   forbids autonomously approving any CODEOWNERS-scoped path.
   `extend-merge-master-envelope-to-floor-bot-lanes`'s ratified **N-1** narrowed
   it for the codexFactory REGENERATION lane ONLY; this lane was expressly left
   on a human merge word.

#### Refusal 3, measured on THIS repository on 2026-09-08

| fact | measured value |
|---|---|
| rulesets binding `openxFactory` `main` | **FIVE, and ALL FIVE are ORGANIZATION rulesets** (`source_type: "Organization"`, `source: "opensoft"`): `8981805` Copilot auto-review, `18834180` Require Code Owner Review, `21957695` chain-gate, `21538893` wallet-gate, `18962101` xFactory Tier-1 main protection |
| repository-level rulesets on `openxFactory` | **NONE.** `GET /repos/opensoft/openxFactory/rulesets` returns only the five above, each sourced from the organization |
| `18834180` conditions | `repository_name: {include: ["~ALL"]}`, `ref_name: {include: ["~DEFAULT_BRANCH"]}` — **org-wide, every repository's default branch** |
| `18834180` rules | `pull_request` (`require_code_owner_review: true`, count `0`, `dismiss_stale_reviews_on_push: true`), plus `deletion` and `non_fast_forward` |
| `18834180` bypass actors | `OrganizationAdmin`, mode `always` — and nothing else |
| where openxFactory's code-owner gate comes from | **`18834180` and only it.** `18962101` (count `1`, `require_last_push_approval: true`, scoped to seven named repositories including this one) has `require_code_owner_review: false`; `21957695` and `21538893` carry required-status-check rules only |
| classic branch protection on `main` | **ABSENT** — `GET /repos/opensoft/openxFactory/branches/main/protection` → `404 "Branch not protected"`. Protection here is **rulesets-only** |
| pull requests ever auto-merged here | **ZERO** of the last 60 closed pull requests carry a non-null `auto_merge`. The mechanism this packet admits has never once fired in this repository |
| CODEOWNERS coverage of the four sites the lane writes | **ALL FOUR MATCH.** `.github/CODEOWNERS:2` `.github/workflows/ @brettheap` covers `merge-master-approval.yml` AND `pytest-suite.yml`; `:20` covers `/contracts/review-lane-pin.yaml`; `:27` covers `/contracts/review-lane-floor-snapshot.yaml` |

**Why no bypass is recommended, and why the reason is stronger here than in
codexFactory.** D-4 (i) — add the merge-master App as a bypass actor on
`18834180` — was withdrawn on 2026-09-08 (codexFactory #232, comment
`5585989018`) for three reasons, all of which reach this repository:

* **The bypass would be exercised by nobody.** Bypass is per-ACTOR and is
  exercised by the actor taking the restricted action. The merge-master App
  neither pushes nor merges — it submits a review — and a GitHub App bot identity
  cannot be named in CODEOWNERS either, so the grant neither satisfies the rule
  nor bypasses it.
* **The async completion path is reported not to honour bypass at all.**
  Community discussion
  [#162623](https://github.com/orgs/community/discussions/162623) carries a
  repro on exactly this configuration — `require_code_owner_review: true` plus a
  required approving count, a GitHub App in `bypass_actors`, `gh pr merge --auto`
  — in which auto-merge never completed while the same App merged instantly
  through the synchronous merge endpoint.
* **The grant is not narrow, and here it is self-defeating.** `18834180` is
  `~ALL` repositories, so an entry on it is a grant over **every default branch
  in `opensoft`** — and over that ruleset's `deletion` and `non_fast_forward`
  rules too, because bypass is per RULESET and not per rule. **In this
  repository it would also remove the very gate the lane's own governance rests
  on**: `contracts/review-lane-pin.yaml` and
  `contracts/review-lane-floor-snapshot.yaml` are code-owner routed precisely
  because they decide which core judges this repository, and `18834180` is what
  makes that routing binding.

**And the escape codexFactory's shape 1 offers does not exist here.** There, the
regeneration lane's bot pull request writes ONE file, so relocating it off every
CODEOWNERS-matched prefix satisfies the code-owner rule vacuously with no bypass
at all. Here the lane writes FOUR files and **two of them are workflow files** —
`.github/workflows/merge-master-approval.yml` and
`.github/workflows/pytest-suite.yml` — which cannot be relocated off
`.github/workflows/` because that is where a workflow must live. Un-routing that
prefix is refused on its face: it is the 2026-08-23 convener ruling's routing for
assembly-class gate surfaces. **So there is no relocation shape for this lane,
and that is a measurement rather than a preference.**

#### The completion path, put OPEN for Brett Heap's word

Each shape one line, with what it costs. **None is taken by this lane, and the
recommendation is at the end.**

* **(1) Measure first — does auto-merge fire at all on a rulesets-only `main`?**
  #162623 reports it does not, with an empty classic branch-protection rule as
  the community workaround; this repository is exactly that configuration and has
  never auto-merged anything. **A precondition for every other shape**, and cheap:
  one throwaway pull request, armed, observed.
* **(2) A third merger identity, merging SYNCHRONOUSLY.** A separate App, holding
  the bypass, that calls the merge endpoint only after independently verifying a
  standing merge-master `APPROVE` bound to the exact head plus every required
  check green. Keeps approver ≠ merger and uses the path the evidence says does
  honour bypass — but it makes an automated identity BE the merge, which is a
  LARGER narrowing than this packet's *"the lane may not BE the merge"* and needs
  its own requirement and its own word.
* **(3) Approver-merges, synchronously.** Simplest, and refused: it collapses
  approver and merger, which openxFactory's ratified *"An autonomous approval is
  not a merge"* forbids by name.
* **(4) Relocate the moved files off CODEOWNERS-matched prefixes.**
  **UNAVAILABLE here** — two of the four are workflow files. Recorded so the
  reader knows it was measured and not overlooked.
* **(5) Name a human code owner who is not Brett Heap for these paths.** Keeps a
  person in the loop, so it does not buy the unattended landing the packet is for.
* **(6) Any bypass actor on `18834180`.** **NOT RECOMMENDED** for the three
  reasons above, and worse here than in codexFactory because this repository's own
  code-owner gate is that ruleset.
* **(7) Status quo.** Brett Heap continues to merge the re-pin pull request by
  hand. Costs one click per cycle, which is exactly what the whole exercise buys
  back.

**RECOMMENDATION on the completion path: take (1) as a measurement now, and hold
the rest for a word.** If auto-merge does not fire on a rulesets-only `main`, no
completion shape is worth designing until that is settled and every discussion of
(2)..(7) is premature. If it does fire, the honest ranking is (2) over (7) over
everything else, and (2) needs a requirement this packet does not carry.
**Nothing about that ordering changes what this packet asks for**: the narrowing
is canon text, it costs nothing while inert, and it is what stops the two
repositories' twin sentences from diverging.

### M-E — Observability: what the run says

**RECOMMENDATION: one notice and one summary line on arming, and one line on the
next firing saying what became of it.**

On arming:
`::notice title=review-lane-repin::auto-merge ARMED on #<N> at <head sha> — the
platform merges when the merge-master envelope approval for that head stands and
every required check has succeeded; this lane neither merges nor approves. NO
CANDIDATE CLASS ADMITS THIS LANE TODAY, so the arming is inert.` The trailing
clause is dropped by the enrolment successor and not before; while it is true it
must be said, because an armed proposal that will never complete is exactly the
thing a reader would otherwise mistake for progress.

The lane's existing delivery lines — `"Opened by the review-lane-repin lane; a
human word merges it."` in the commit message, and the DRY-RUN summary — are
CORRECTED in the same act where the narrowing makes them untrue as written,
rather than left standing beside a contradicting requirement.

On the following firing: the lane already computes its action from the open-branch
set, so it already knows whether the previous pull request is still open.
**Recommendation: say which, in the witness-line style the clean no-op already
uses** — a firing that finds no open advance where the last one armed states the
merge commit it resolved, so a reader learns the outcome from the run log rather
than from the platform. Every value stated is one another party can recompute; the
lane states no claim only it can make.

### M-F — Scope: what this packet touches, and what it must not

**RECOMMENDATION: ONE `## MODIFIED` block, over ONE requirement, in ONE
capability, and no second delta of any kind.**

`review-lane-floor-mirror` currently carries requirement text in THREE places: the
seven promoted requirements in `openspec/specs/review-lane-floor-mirror/spec.md`
(from the archived `mirror-floor-addition-grace`), the parent's seven `## ADDED`
requirements, and `extend-merge-master-envelope-to-floor-bot-lanes`'s three
`## ADDED` requirements. **This packet's block reaches exactly one of the
parent's seven**, and the other sixteen requirements across the three sources are
untouched. In particular it does NOT touch *Each floor bot lane's admission
conditions are measured, not asserted* or *A re-pin is approved only against the
source repository's default-branch head* — those are the ENROLMENT's rules and
belong to the successor.

The reciprocal is worth stating because the twin packet made the same promise in
the other direction: **this packet authors no codexFactory byte.** Its amendment
is read at `93f0f0d7` and cited; the N-1b carve, the *Bounded autonomous surface*
text and the regeneration lane are codexFactory's.

**One DISCLOSED consequence of amending a still-active parent, expected and not a
defect:** strict validation may emit an INFO line to the effect that an archive
would refuse the delta, because the requirement being modified still lives in the
parent's `## ADDED Requirements` rather than in
`openspec/specs/review-lane-floor-mirror/`. `sequenced_after:` declares the
parent first for exactly that reason — the parent promotes the requirement, this
packet replaces it — and `tasks.md` § 5 fixes the archive order.

### M-G — The live proof

**RECOMMENDATION: the realization evidence is SPLIT, and the second half is not
this packet's to produce.**

codexFactory's D-7 could name one observation that discharges everything. Here the
honest split is:

* **Half one, produceable now:** the arming line landed with
  `python3 -m pytest tests/review_lane_pin -q` green, the flipped sweep passing,
  the three new controls passing (including the one that would red if the driver
  gained a disposal verb), and the scenario mapping re-read. **This ticks § 3.**
* **Half two, NOT produceable until BOTH the enrolment successor lands AND the
  completion path has a word** (M-D — an enrolment with no completion mechanism
  is an approval that lands nothing, which is the exact gap openxFactory's own
  promoted *"An autonomous approval is not a merge"* obliges a packet to record
  rather than discover): ONE real `bot/review-lane-repin` pull request observed
  ARMED, autonomously APPROVED and MERGED with no human act — recorded as (a) the run id and the head armed at,
  (b) the pull request number and the merge commit, (c) the actor GitHub reports
  for the merge, and (d) a reviews-API measurement that the only approving review
  is the merge-master identity's. **This ticks § 4.1, and § 4.1 is what
  `target_release:` makes the archive wait on.**

**An armed auto-merge never observed to complete proves nothing.** The first
unattended cycle taught that three times over — codexFactory #252, #260 and
openxFactory #726 were all found by running, not by reading — and this repository
learned it once more at `mirror-floor-addition-grace`'s archive, where the live
test exposed two negative controls that could never have failed. A DELIBERATE PARK
observed not to merge while armed is the cheaper half of the same proof and is
recorded as § 4.2.

## 4. Where the amendment lands

`mirror-floor-regeneration-automation` is ratified and realized but NOT archived —
its `target_release:` waits on a complete unattended cycle — so its requirement 1
lives in an ACTIVE change's `## ADDED Requirements` and not yet in
`openspec/specs/review-lane-floor-mirror/`.

**This packet does not rewrite that packet's delta and does not restate its
history.** It carries a `## MODIFIED Requirements` block against the same
capability and declares
`sequenced_after: [mirror-floor-regeneration-automation, extend-merge-master-envelope-to-floor-bot-lanes, codexFactory:amend-floor-regeneration-merge-authority]`,
so the changes archive in order: the parent promotes the requirement, this packet
replaces it. The third entry is a QUALIFIED FOREIGN reference — the neutral
validator checks foreign entries for well-formedness only, because it *"cannot
read another repository's corpus and MUST NOT pretend to"* — and it names the
codexFactory amendment this one is the lockstep of, landed at
`93f0f0d71ed00dbb384101be779d62233f6367f5`. It is the third foreign entry in this
corpus; the first was `mirror-floor-addition-grace`'s and the second the parent's.
