# Design: assert-review-lane-lockstep-against-aggregation

Status: draft
Kind: design

The authoring decisions beyond the finding this packet encodes. Each is declared
for a veto and each is one edit away.

## D1 — shape (b), the assertion, and NOT shape (a), the widened write

The pin file's own `reason:` paragraph names both and prefers (b) on a general
ground: *"(a) still leaves this file's truth depending on a lane remembering to
write it."* That ground is sound but it is not the decisive one. **The decisive
one is a measurement: the lane cannot write the field honestly, because it has no
reading of the aggregation to write from.**

    $ grep -nE "opensoft/xFactory|MIGRATION_PIN|council-convening" \
        scripts/review_lane_repin.py .github/workflows/review-lane-repin.yml
    (no output)

`MIGRATION_PIN` appears in NO file under `scripts/` or `.github/workflows/`. The
only places the aggregation's surfaces are named anywhere in this repository are
PROSE: the pin file's append-only `reason:` narrative and the guarding test's
docstring. **So under (a) the lane would have exactly one thing it could write —
`diverged`, on every advance — and it would be writing it by INFERENCE from the
rule "`MIGRATION_PIN` does not move on a routine advance", not by measurement.**

**And that inference is already falsified by this estate's own history.** At the
fourth re-point ceremony (`opensoft/xFactory` `#475`, merge `c88d1fdd`,
2026-09-21) the aggregation converged ONTO a commit this file had been pinned to
since 2026-09-18 — the two moves three days apart and not a pairing at all, which
the pin file records as the first time that had happened. An advance that lands
on the commit the aggregation already names leaves the pair CONVERGED, and a lane
writing `diverged` by rule would have made the field false in the other
direction. **(a) does not remove the false declaration; it changes which
direction it is false in.**

**The capability has already ruled on assertion-versus-measurement, one
requirement over.** *The automated pin advance moves every pinned site in one
commit or opens nothing* ends: *"what is added here is that an UNATTENDED author
must prove the lockstep by measurement rather than assert it."* Shape (a) would
install inside that same capability precisely what that sentence forbids. Shape
(b) extends its principle to the one lockstep it does not yet reach: the five pin
sites' internal lockstep is proved by re-reading every site after the write, and
the cross-repository lockstep by reading the other repository.

**And the capability is already built for (b).** The realization's declared split
— *"the workflow reads the two repositories with `gh` … and hands this module
PURE INPUTS … Every requirement's refusal is then a unit test with a fixture, not
a workflow that has to be fired to be believed"* — is exactly the split the
assertion needs: one more repository read where repository reads already happen,
one more pure comparison where judgments already happen. No new architecture.

**THE TWO ARE NOT EXCLUSIVE AND THIS PACKET DOES NOT FORBID (a).** If a later act
teaches the lane to read the aggregation, it may then write the field — and it
would be writing a measurement, at which point (a) becomes a special case of (b)
rather than an alternative to it. What the requirement forbids is the state the
corpus is in now: a declaration nothing compares to anything.

## D2 — the check runs at the advance, not on a schedule

A nightly or a scheduled sweep would find the stale value eventually, which is
what a human already does. The hazard is specifically that **a routine advance
falsifies the claim and nothing notices**, so the requirement puts the check at
least on every proposed advance of `core_commit` and on the pull request carrying
it. That way the contradiction is reported in the SAME pull request that creates
it, to the reviewer who is already looking at that diff. It does not by itself
stop the auto-merge that lane arms: the verdict is not a required check, and
requiring it is a ruleset act this packet does not take (`tasks.md` § 6.5).

**A gate that BLOCKS the advance was considered and is deliberately not
required.** Divergence is a lawful state — the pin file has carried it, with
reasons, through four cycles — and a check that refused every advance leaving the
aggregation behind would refuse the ordinary case the estate designed for. The
obligation is to REPORT a declaration the measurement contradicts, not to forbid
the state it reports.

**What the check observes is this repository's side of the pair** (Copilot
`r4078648320`). An aggregation that moves alone — `MIGRATION_PIN` re-pointed at a
ceremony — can falsify the declaration with no pull request here. The check
reports that at the next pull request that changes the pin, and the ceremony's
own pull request here is one: `#1136`, the fourth ceremony's lockstep flip,
changed `contracts/review-lane-pin.yaml` (author `brettheap`, merge `7c49825e`).
Observing the aggregation as it moves would take either a dispatch from the
aggregation, which is an act in `opensoft/xFactory` this packet does not propose,
or a schedule, which the paragraph above declines as the mechanism. The
requirement now says which side it observes rather than implying both, and the
gap is registered at `tasks.md` § 6.7.

## D3 — `## ADDED` and no `## MODIFIED`, which is a decision

Three active changes carry deltas on `review-lane-floor-mirror`:
`amend-mirror-floor-regeneration-merge-authority` (`## MODIFIED` on *An automated
pin advance only ever proposes*), `admit-review-lane-repin-to-merge-approval-envelope`
(four `## ADDED`) and `extend-merge-master-envelope-to-floor-bot-lanes` (three
`## ADDED`). None names the requirement added here and none is named by it, so
there is no collision and no pairing marker is owed.

**More than that: there is no promoted requirement to modify.** The hazard is not
a defect in anything this capability says; it is the GAP between the pin advance
this capability automates and a field of the pin file that no requirement has
ever obliged anyone to measure. A `## MODIFIED` block would have to pick a
requirement to hang the obligation off, and each candidate is about something
else — the five sites' internal lockstep, the snapshot witnesses, the lane's
triggers. **Adding the obligation collides with nothing and rewords nothing**,
which is also why the two blocks this packet's sibling carries are not the shape
here.

## D4 — an unreadable aggregation is UNDETERMINED, and never a pass

Two wrong answers were available. Reading an unreachable aggregation as
CONFIRMING the declared state makes the check worthless the first time the API
rate-limits. Reading it as CONTRADICTING the state turns another repository's
availability into this repository's red build.

The estate's own doctrine already answers it, in the sibling capability this
lane's other work sits in: *"A reader over a corpus it does not own FAILS CLOSED
on an unresolvable corpus — an unanswerable question is never an implicit pass"*,
and *"An empty corpus and an unreadable corpus SHALL be DISTINCT answers."* So
the check reports UNDETERMINED, names each surface it could not read, and
concludes neither state. The declared value is neither confirmed nor
contradicted, because it was not measured.

## D6 — the surfaces are read as a SET, and disagreement is its own outcome

Copilot `r4075976905` found that the first draft said *"the commit the
aggregation's judging surfaces name"* while D5 had the implementation reading
THREE values, and never said what happens if they differ or which one is
authoritative. **An implementation could pick one surface and claim compliance,
so the measurement was not deterministic.** Taken.

The requirement now reads the surfaces AS A SET, requires them to agree before
either state is concluded, and gives disagreement its own outcome — INCONSISTENT,
with each surface named and its value digested (D20), concluding neither `converged` nor
`diverged`. **A check permitted to pick one surface is choosing its own answer**,
which is the same defect in miniature as the declaration this packet exists to
stop trusting.

**Naming the set rather than a count.** The text says *"the pin's own
`converged_with:` members and the aggregation's constant that holds them
identical"* rather than "three", because `converged_with:` is a list the pin
owner may extend and a requirement that hardcoded the cardinality would go stale
the day it did. D5's decision not to promote the constant to a converged-with
member is unchanged: it is READ, and it is not a member.

**And the outcome is worth having for its own sake.** The aggregation's constant
exists to hold its two judging workflows identical to each other; if it ever
disagreed with them, that is a fact about that repository which nothing today is
positioned to notice, because nothing today reads all three at once. This check
will be the first thing that does.

## D7 — the pull-request side is a SECOND workflow, and the advance lane keeps its triggers

Copilot `r4075976980` found that § 5.1 assigned the read to
`.github/workflows/review-lane-repin.yml`, whose `on:` keys are measured exactly
`['schedule', 'repository_dispatch', 'workflow_dispatch']` — **no
`pull_request`** — so the requirement's *"and the pull request that carries it"*
clause had nowhere to run and an advance could open a pull request with no check
on it. (The only `pull_request` string in that file is a comment at `:672`, which
is why a line-oriented grep for it answers misleadingly; the measurement above is
the parsed `on:` mapping.) Taken.

**The realization adds a gate of its own**, on the estate's existing pattern of a
pin gate that is its own workflow — `openspec-cli-pin-gate.yml` and
`openreposhape-pin-gate.yml` — **but not on their trigger.** Those two run on
`pull_request` because neither holds a secret (zero `secrets.` references in
either); this gate holds a credential that reads a private repository, so D14
puts it on `pull_request_target` and it never runs on `pull_request`. (This
paragraph first said *"a `pull_request`-triggered gate"*, written before D14
reversed the trigger; Copilot `r4076845460` and `r4076990021` found the phrase
still standing elsewhere, and it stood here too.) **`review-lane-repin.yml` deliberately does NOT gain a
`pull_request` trigger**: that workflow's whole shape is *propose an advance*,
and a pull-request trigger would fire the advance logic on every pull request in
the repository. § 5.1b makes that a TESTED negative control rather than a
convention — a test requires `pull_request` to be ABSENT from the advance lane's
triggers.

## D8 — each outcome carries a CONCLUSION, and three of the six fail

Copilot's *previously missed* item in review `5283291040` found that the requirement
defined an UNDETERMINED semantic state and never said what the CHECK concludes,
leaving an implementation free to fail the gate on an xFactory outage — which D4
rejects — or to pass without a visible neutral result. **Taken, and it forced the
missing half of D2.**

| outcome | conclusion | why |
| --- | --- | --- |
| declaration ABSENT or outside its vocabulary — a foreign declared state, a `core_commit` that is not a commit, an unparseable candidate, or a `converged_with:` other than the read plan's workflow members (D16, D17, D19) | **FAIL**, naming the value found | added at round 6; see D14a. Checked FIRST, before the aggregation is read |
| declared state CONTRADICTED by the measurement | **FAIL**, naming `core_commit` and the agreed commit's digest | this repository's own contract file states something false about another repository; the remedy is one edit to the field |
| the check's own ACCESS fails — binding, mint, or the aggregation refusing its token | **FAIL**, naming the failure | this repository's own configuration; the per-run form of the standing-state rule (review `5286349291`'s *previously missed* item) |
| surfaces disagree with each other (INCONSISTENT) | **NEUTRAL**, visible | another repository's defect, and not this repository's claim to answer |
| aggregation unreadable (UNDETERMINED) | **NEUTRAL**, visible | another repository's availability, and D4's whole point |
| declared state agrees | pass | |

**A NEUTRAL conclusion is not a pass and silence does not stand in for it.**
(The table gained its fifth row and its second FAIL at round 6, when D14a
closed the absent-or-foreign declared state, and its sixth row and third FAIL
when review `5286349291` found that the standing-state rule had no conclusion;
the heading is counted here rather than left to drift again.) A
state a check computes and does not publish is a state nobody acts on, which is
the same defect as a declaration nobody measures — this packet would be an odd
place to reintroduce it.

**THIS DOES NOT CONTRADICT D2, AND THE DISTINCTION IS WORTH STATING.** D2 refuses
a gate that BLOCKS AN ADVANCE for leaving the aggregation behind: divergence is a
lawful state the pin file has carried, with reasons, through four cycles, and a
check that refused every such advance would refuse the ordinary case the estate
designed for. What fails here is not the divergence but **the false declaration
about it** — a field asserting `converged` while the measurement says otherwise.
The advance stays lawful; only the sentence claiming something untrue is refused,
and fixing it is one edit rather than an act in another repository.

**And the asymmetry is deliberate.** The two outcomes that fail are the only two
whose subject is THIS repository's own file — a declared state outside its
vocabulary, and one the measurement contradicts. The two neutral ones are facts
about the aggregation; turning either into a red build here would make the check a
liability its owners would route around, which is how a governance check stops
being run.

## D9 — the outcomes are ORDERED, because two of them overlapped

Copilot `r4076152698` found that the stale-`converged` scenario's WHEN was true
*whenever at least one surface does not name the new commit* — **including when
the surfaces disagree with each other**, which the INCONSISTENT scenario then
requires to be NEUTRAL. **The same inputs demanded both FAIL and NEUTRAL.** That
is not a wording problem; it is a requirement no implementation could satisfy.

Fixed by stating the order in the body, each outcome reached only where every
earlier one does not hold, and by qualifying both comparison scenarios' WHEN with
*the aggregation's surfaces read, and agreeing with each other on one commit of forty lowercase hexadecimal characters* — the commit clause added by review
`5286144492`'s *previously missed* item, so that surfaces agreeing on a value that
is not a commit cannot satisfy a comparison scenario's own WHEN (D16). Exactly one
outcome holds for any input, and no implementation has to arbitrate. **THE ORDER
AS IT NOW STANDS**, after D14b moved the vocabulary check to the front, D16
folded a non-commit surface into UNREADABLE and a non-commit `core_commit` into
the first, D19 folded a foreign `converged_with:` into the first too, and the
standing-state rule gained its own outcome: the declaration OUTSIDE ITS
VOCABULARY; then the check's own ACCESS FAILING; then the aggregation UNREADABLE; then its surfaces DISAGREEING; then
the comparison of the agreed commit against `core_commit`, and the declared state
against that comparison. This paragraph first recorded the order this section
fixed — UNREADABLE, DISAGREEING, comparison, declared state — and it stood after
D14b had superseded it (review `5284046970`'s *previously missed* item, then
Copilot `r4076845591`), which would have let an implementation read the other
repository before rejecting a malformed local declaration.

**The defect was introduced by my own D8 fix**, which gave each outcome a
conclusion without noticing that two outcomes could be reached by one input. A
requirement gains a contradiction the moment its cases stop being disjoint, and
adding conclusions is exactly when that happens.

## D10 — the access path, and why its absence would have made the packet inert

Copilot `r4076152594` asked where the second cross-repository read gets its
credentials. **Measured, and it is the most consequential finding on this
packet:**

    $ gh api repos/opensoft/xFactory --jq .visibility
    private
    $ curl -s -o /dev/null -w "%{http_code}" https://raw.githubusercontent.com/opensoft/xFactory/main/tests/test_merge_master_workflows.py
    404

and `contracts/review-lane-repin-binding.template.yaml` declares
`source_repository: codeXfactory/codexFactory` with `grants: [contents:read]` and
nothing at all for the aggregation. **So on today's credentials the check could
never conclude** — it answered UNDETERMINED on every run as the requirement then
stood, and since review `5286349291` it would end every run in its ACCESS FAIL
instead — and a check that never concludes looks exactly like a check that is
working, which is the failure this packet exists to
end rather than to reproduce in a new place.

Three things follow, and all three are now written down. The realization declares
a READ-ONLY binding for `opensoft/xFactory` in the same shape as the existing
grant, keeping the family's own rule (*"neither repository's lane may reach into
the other's"*) by carrying the same `never_grants:` set. The requirement forbids
UNDETERMINED as a STANDING state: the check's own access failing is reported as
that, not as a property of the measurement — and, since review `5286349291`'s
*previously missed* item, it has a per-run conclusion of its own, FAIL, so it
cannot stand as a permanent NEUTRAL (D8). And § 5.4's realization evidence is no longer *one
observation of the check running* but **one observation of it CONCLUDING** —
because an observation of UNDETERMINED proves the access is missing, not that the
check works.

## D11 — the neutral conclusion needs a representation, and the PR host needs its own reading

Two more from the same round, both about the gap between what the requirement
says and what a workflow can express.

**`r4076152473` — a step exits 0 or non-zero, which is a green pass or a red
failure and nothing else.** *"NEUTRAL, visible, not reported as a pass"* has no
expression by exit code. So the realization publishes through the check-run API,
and every outcome is mapped rather than only the neutral ones (Copilot
`r4078058050`): `failure` for the three FAIL outcomes, `neutral` for INCONSISTENT
and UNDETERMINED, `success` for agreement, and no conclusion outside those (D17) —
the values read in its output each
time, a surface's only as its classification, its relation to `core_commit` and a
digest (D20). The test asserts the PUBLISHED CONCLUSION for each outcome against that
mapping rather than the process exit code —
**because this contract degrades silently to a green pass if nobody checks which
of the two was published.**

**`r4076254027` — and the same separateness reaches the CREDENTIALS.** A binding
written for the repin identity alone would leave the pull-request gate failing
on its own access on every run — D10's defect, reappearing one workflow over, because
a separate run cannot reuse a minted App token any more than it can reuse step
outputs, and the ambient `GITHUB_TOKEN` cannot read a private repository at all.
The gate mints its own token from the SAME App under a binding of its OWN (D13),
and a test asserts the PULL-REQUEST SIDE's read succeeds rather than only the
advance side's. **The two runs share an App identity and nothing else — no
token, no outputs, no privilege set** — D7's split restated where it costs
something.

**`r4076152645` — the pull-request host is a separate workflow run** and cannot
consume the scheduled run's step outputs, so § 5.1a takes its own reading and
passes it to the same pure comparison. Two reads of one fact by two runs is the
cost of the split in D7, and it is cheaper than a shared artifact whose staleness
would need a rule of its own — which would be this packet's own subject,
recursively.

**`r4076152544` — a read failure must be an INPUT, never a fatal step.** The
advance workflow treats a non-404 API failure as step-fatal, so an auth error, a
rate limit or a transport failure would abort before the comparison ran, and the
UNDETERMINED scenario would be unreachable by the only route that reaches it. The
realization makes every read outcome, failures included, an input naming what
could not be read.

**`r4078594297` — and so is every other outcome.** A validation step that FAILED
by exiting non-zero would stop the job before the publisher, and the `failure`
the requirement asks for would never be created. So validation, the access
check, the reads and the comparison each RETURN an outcome, and one publisher
runs last and always. The job's own exit code then reports only whether that
publisher did what its input required: publish the verdict, or, for a head that
moved (D14c), publish nothing. Publication failing is the one thing that turns
the job red, so a missing verdict is itself visible.

**`r4076902144` and `r4077054569` — and the published run is the gate's ONLY
identity, hung on the CANDIDATE.** Publishing a check run does not change the
job's own. GitHub names a job's check-run after its job id, which this repository
already treats as load-bearing (`merge-master-approval.yml`:457, *"JOB ID IS
LOAD-BEARING"*), and a `pull_request_target` run's job check lands on the pull
request's HEAD. Measured on this packet's own pull request: run `35788224200`
(`merge-master-approval`, event `pull_request_target`) carries `head_sha`
`918e30e3`, the head and not the base `2e222d98`, and its job check-run concluded
`success` on that commit. **So a gate job that exits 0 after publishing `neutral`
leaves a GREEN check on the very commit it judged.** Two rules close it. The
verdict check-run carries a declared name, `review-lane-lockstep-verdict` (D18),
that matches NO job id in any workflow here, and that name, never a job id, is the
gate's identity wherever a check is required or read. And the run is created with `head_sha` set to the VERIFIED candidate
`head.sha` of D14c, never `github.sha` — which in a `pull_request_target` run is
the BASE branch's last commit, and would hang the verdict on a commit the advance
does not propose.

**`r4077837539` — and so the advance side publishes nothing.** It records the
measured values, in the form the gate publishes them (D20), and the outcome in
the pull-request body the lane already writes, and the conclusion for that advance is the gate's, on the same head: the
lane's App-token push starts the gate's `pull_request_target` run (measured on
`#1138`). A second check run for one fact on one commit would be the second
identity the paragraph above forbids. **The body's record is HISTORICAL, and says
so** (Copilot `r4078594266`). The two runs read mutable aggregation state at
different times, so a re-point landing between them can give them different
resolved commits and different outcomes. The body therefore records the lane's
reading as a reading AT the commit it resolved, and names the gate's verdict on
the head as the only authoritative conclusion. Where the two differ, each names
the commit it read, so the difference reads as the aggregation having moved, not
as a contradiction.

## D12 — the surfaces are read at ONE resolved commit, or the check measures read timing

Copilot's *previously missed* item on round 5: reading the three files
independently from `main` is not a snapshot. **A re-point commit landing between
two API calls returns a MIXED set, which the check would report as INCONSISTENT —
a state that never existed in the repository it was reading.** Taken into the
REQUIREMENT rather than the task list, because it is about what is measured
rather than how.

The check resolves the aggregation's branch to a single commit FIRST, reads every
surface at that commit, and names the commit with its verdict. **And WHICH branch
is not the caller's to say** (Copilot `r4078009970`): it is the repository's own
DEFAULT BRANCH, resolved at run time the way this lane already resolves its
source (`review-lane-repin.yml`:433-459, under the capability's rule that the
verification *"SHALL NOT be inferred from an event payload, a pull-request head,
a tag, or any reference supplied by a caller"*). A snapshot of the wrong branch
is internally consistent and still measures the wrong aggregation. **A measurement
taken across a moving ref measures read timing, not the aggregation** — and for
this packet that failure would be particularly cruel: the one outcome it would
manufacture, INCONSISTENT, is the outcome nobody can check against anything,
because it says the other repository disagrees with itself.

## D13 — the gate's credential is a binding of its OWN, and the never-passed statement is HONOURED rather than amended

Copilot `r4076368784` measured what round 4's fix had waved at:
`contracts/review-lane-repin-binding.template.yaml` is structurally
single-consumer — `consumer.holder_ref: "openxfactory:workflow:review-lane-repin"`
(`:100`), `resolution.resolved_by: review_lane_repin_workflow_only` (`:167`), and
a statement that the minted token is *"never passed to a second workflow"*
(`:190`). *"Names both consumers"* without saying HOW would let an implementation
add the privilege under a contract that still denies it.

**The first answer here was a SECOND CONSUMER ENTRY under that binding, and it was
wrong one level down** (Copilot `r4076990082`). The template's `privileges:`
(`:109`) and `resolution.scoped_to` (`:180`) sit at the BINDING's top level, not
under a consumer, and its `floored_repository` entry grants `contents:write`,
`pull-requests:write` and `workflows:write` (`:154`) — so a gate seated as a
second consumer would mint with the advance lane's write authority over this
repository, in a job that exists only to READ another repository and publish a
check.

**So the gate gets a binding of its own, in the same template shape**:
`privileges:` naming only the aggregation, `grants: [contents:read]` with the
family's `never_grants:`; `resolution.scoped_to: [xFactory]`; `resolved_by`
naming the gate's workflow alone (D18 names the binding, the workflow and the
consumer); and ONE mint requesting exactly
`owner: opensoft`, `repositories: xFactory` and `permission-contents: read`. That
is the estate's own per-mint down-scoping — `review-lane-repin.yml`:276-284
already mints its codexFactory read that way, beside a separate write mint for
its own repository — held by a test in the shape of
`test_the_token_is_scoped_to_the_bindings_two_repositories`. The never-passed
statement is **carried unchanged on both, because nothing is passed**: each
workflow mints its own token under its own binding. The existing sentence is not
an obstacle the design works around; it is the design.

## D14 — `pull_request_target`, and THIS DECISION REVERSES ITSELF ON THE ESTATE'S OWN RUNNING TEST

**The first version of this decision refused `pull_request_target` by name and
scoped a plain `pull_request` gate to same-repository events. It was wrong, and
the evidence against it is a test this repository already runs.**

Copilot `r4076368722` raised fork events (no secrets → UNDETERMINED on every fork
run), and the fix was a `head.repo.full_name` condition. `r4076474882` then
measured what that condition does not reach:
`tests/review_lane_pin/test_review_lane_caller.py`'s
`test_the_head_executing_trigger_is_absent`, verbatim —

> *"a plain `pull_request` trigger would run the head's copy of this file with
> the App credential that reads a private repository in scope — the exfiltration
> shape the base-branch rule prevents"*

— with `EXPECTED_TRIGGERS = {"pull_request_target", "workflow_dispatch"}` beside
it. **A same-repository condition cannot fix that, because under `pull_request`
the head's copy of the WORKFLOW runs and can delete the condition.** Any
same-repository pull request author could have read a private repository's
contents through this gate.

So the gate takes the estate's worked shape rather than one reasoned out here:
**`pull_request_target`**, so the BASE's copy of the workflow runs and a head
cannot rewrite it; **no checkout of `github.event.pull_request.head`**, mirroring
`test_no_checkout_takes_the_pull_request_head` (*"rules must come from the base
branch"*) — and that costs nothing here, because the check reads two repositories
over the API and needs no candidate code at all, which is exactly the "safe
base-code/API design" the first finding asked for; plus an **allowlist** — a head
ref here (`bot/review-lane-repin`), refined at D14d to the author / head-ref /
base-ref triple — and the same-repository condition as defence in depth, with
fork events and non-allowlisted heads reported OUT OF SCOPE. **Both the allowlist
and the scope are REMOVED at D17**, because this capability forbids exactly that
exemption to every check that judges a pin advance; this paragraph is kept as the
record of what D17 reverses.

**The lesson is the one this packet keeps relearning about itself.** I refused
`pull_request_target` by reasoning from its general hazard without checking
whether this estate had already solved it — and it had, in the workflow this very
capability governs, with the reason written into a test's failure message. **A
first-principles refusal that contradicts a running test is a finding about the
reasoner.**

## D14a — the declared state is a closed vocabulary, or the ordering has an input it does not reach

Copilot's *previously missed* item on round 6: D8's table and D9's ordering
between them claim exactly one outcome holds for any input, **and neither has a
case for a declared status that is absent or outside the two words.** With
agreeing surfaces, a value such as `pending` is neither `converged` nor
`diverged` and the comparison reaches no defined outcome. The live pin test
checks only the current literal, so nothing closes that domain.

The requirement now does: the declared state SHALL be one of the two words, and
an absent or foreign value FAILS naming what was found, **in the same class as a
contradicted declaration** — because both are this repository's own file failing
to say something true, and the remedy for both is one edit to the field. It gets
its own scenario, and the ordering is total.

## D14b — the new outcome had to go FIRST in the order, and four inventories had to move with it

Copilot round 7 raised five findings and four were one defect: **adding a
scenario left four statements of the count behind** — `tasks.md` § 2.1 and § 5.3,
the `target_release` archive-evidence clause, and the README row. The sibling
packet on this lane spent four review rounds on exactly that class, so this one
was swept the way that one ended up being swept: case-insensitively, across
`.md`, `.yaml` and `.py`, over every number-word adjacent to a counted noun. Every
inventory now also NAMES the six rather than only counting them, which is the
durable half of the fix. (Seven since review `5286349291` added the check's own
access failing. The four inventories moved again, and the `target_release`
clause was again the one left behind, until Copilot `r4078648354`.)

**The fifth finding was real and structural.** `r4076557241`: the ordering in D9
put the comparison before the declared state, while D14a's scenario requires an
absent or foreign value to FAIL **without falling through to a comparison**. For
readable, agreeing surfaces and `status: pending`, the two texts disagreed about
which outcome held — the exact defect D9 exists to prevent, reintroduced by the
fix that closed D14a's gap.

**The vocabulary check now comes FIRST**, before the aggregation is read at all:

> the DECLARED STATE OUTSIDE ITS VOCABULARY first — this repository's own file,
> readable without touching anything else, and a defect that makes every later
> question moot; then the aggregation UNREADABLE; then its surfaces DISAGREEING;
> then the comparison.

(That was the spec's text at this round. D16 and D19 later widened the first
outcome to the whole DECLARATION, so a `core_commit` that is not a commit and a
`converged_with:` other than the read plan's workflow members are in it too; D9
carries the order as it now stands.)

That is both the ordering the scenarios require and the honest engineering order:
**a check does not go asking another repository a question in order to report a
defect in its own file.**

## D14c — `pull_request_target` made the gate read the WRONG PIN, and that is the cost of D14 paid in full

The round-8 *previously missed* item is the one that would have made this packet
decorative. **Under `pull_request_target` the workflow runs from the BASE**, so a
gate that parses the checked-out `contracts/review-lane-pin.yaml` reads the
commit ALREADY IN PLACE rather than the one being proposed. Measured against the
live reproduction this packet cites throughout: for `#1138` that is base
`b21f0100` compared to the aggregation's `b21f0100` — **a pass, while the advance
proposes `491fc54d` and is never seen.**

**The gate would have been green on exactly the act it exists to judge.**

This is D14's cost, and it is worth naming as such rather than as an oversight:
choosing the safe trigger moved the workflow's own code to the base, and the pin
came with it. The remedy keeps the safety and pays the cost explicitly — the gate
**fetches the candidate pin as INERT BYTES at the verified `head.sha`** (a file
read over the API, not a checkout and not an execution), **parses it with base
code**, and **re-reads `head.sha` after the fetch** so a force-push between the
two is refused rather than reported.

**And the parse is STRICT** (Copilot `r4078835237`). The bytes are the fork's to
choose, so "parses it with base code" is not a parser. The gate applies a byte
ceiling fixed in its own code before parsing — 1 MiB, against the pin's measured
70,039 bytes — and then accepts exactly ONE YAML document with no duplicate key,
alias, merge key or tag. A duplicate `core_commit` is the case that matters most:
a reader taking the last value and a reviewer reading the first would see
different pins in the same bytes. Each refusal is the candidate that cannot be
parsed (D17): ABSENT, and FAILING, with nothing read in the aggregation.

**The distinction that makes `pull_request_target` usable rather than merely
safe** is exactly this one: head CODE is never run, head DATA may be read as
bytes. The estate's own rule says the first half — *"rules must come from the
base branch"* — and this packet needed the second half stated to be correct at
all.

**And head data is JUDGED, never FOLLOWED** (Copilot `r4077898334`). The
candidate's `converged_with:` is head-controlled; if it chose the paths the gate
reads in the private aggregation, a candidate could turn the xFactory token on
any file there, and D16's rule of naming a non-commit surface by its value would
print that file's contents into the verdict. So the read plan is the base's —
the base's `converged_with:` and the gate's own fixed location for the
aggregation's constant — and the candidate supplies only the values under
judgment, `core_commit` and the declared state. (**Superseded in part by D19**:
the base's pin file is data too, so the plan is now fixed in the gate's own code
and `converged_with:` is judged against its workflow members rather than followed.) The value named for a surface is
the field extracted from its fixed location, never the file around it.

## D14d — the allowlist is a TRIPLE, because a head ref is a predicate its author controls

**SUPERSEDED BY D17**, which removes the allowlist this section refines; kept as
the record of the reasoning D17 reverses.

Copilot `r4076740158`, the last refinement of D14's chain. A head-ref allowlist
is satisfied by anyone who can create or update that branch — so **the same
writer could open a different pull request under the allowlisted name and run the
base workflow with the aggregation token**; and an unfiltered base would expose
the same path on any branch, not only `main`.

**The estate already states the shape and this packet simply adopts it.**
`.github/merge-approval-envelope.yml`:70-74 requires `expected_author`,
`expected_head_ref` AND `expected_base_ref` together, held by
`tests/review_lane_pin/test_review_lane_caller.py`:780-789 — whose own words call
the exact head ref *"half of the fork defence"*. **Half.** The gate's condition is
the same triple, each an exact value and none a pattern, with a test per predicate
driving a pull request that satisfies the other two and fails this one. **The
SHAPE is the envelope's and the VALUES are this lane's** (Copilot
`r4078098160`): author `openxfactory[bot]`, head ref `bot/review-lane-repin`
(`BOT_BRANCH`, `scripts/review_lane_repin.py`:553), base `main`. The envelope's
own `expected_head_ref` is `intents/rolling`, another lane's, and copying it
would open the gate to the wrong pull request.

**That is the fourth time on this packet that the estate had already worked out
what I was deriving** — after the trigger, the no-head-checkout rule and the
never-passed token statement. The pattern is now the packet's own advice to its
realizer: before reasoning about a governance mechanism here, read what this
repository's tests already refuse.

## D15 — the neutral conclusion needs a WRITE path, and it is a different token from the read

Copilot's second *previously missed* item: § 5.1e publishes through the check-run
API while § 5.1c's binding grants `contents:read` only, and **no workflow in this
repository grants `checks: write` today** (`merge-master-approval.yml`:453 grants
`checks: read`). The publish would 403, and INCONSISTENT/UNDETERMINED could never
be visible as `neutral` — the contract would degrade to exactly the silent green
pass D11 was written to prevent, by a different route.

The gate's own job declares exactly the three `GITHUB_TOKEN` scopes its steps
use — `contents: read`, `pull-requests: read` and `checks: write` — because a
declared `permissions:` block sets every undeclared scope to `none`
(`merge-master-approval.yml`:448-449). The first draft of this decision granted
`checks: write` alone, which would have left the gate unable to fetch the
candidate pin or re-read its head (Copilot `r4077837498`). **The aggregation
read token stays read-only and gains nothing**: the
thing being written is a check run in THIS repository and the thing being read is
ANOTHER repository, and keeping those two privileges in different places is the
same separation the binding's `never_grants:` set exists to state.

## D16 — a surface is read only as a commit, or agreement on garbage passes

Copilot `r4076989950` found the input the ordering still did not reach: a
READABLE aggregation whose surfaces all AGREE on a value that names no commit.
That is neither UNREADABLE nor INCONSISTENT, so it reached the comparison — and a
declared `diverged` would then PASS, merely because `core_commit` differs from the
string the surfaces agreed on. The realistic form is not a typo in the
aggregation; it is an EMPTY STRING, which is exactly what a reader that failed
quietly returns for all three at once.

**Each surface is now read only as a commit** — forty lowercase hexadecimal
characters, the grammar `core_commit` already obeys (`SHA40_RE`,
`scripts/review_lane_repin.py`:114) — and a surface outside it counts as
UNREADABLE, named by the CLASSIFICATION of what its fixed location in the gate's
read plan held — absent, empty or not a commit — and never by that value or the
file around it (D14c, D19, D20). The input lands in an outcome that
already exists, NEUTRAL, so no outcome is added and the order stays as D9
states it.

**`core_commit` is validated too, REVERSING this section's first answer** (Copilot
`r4078528147`). This section first left the candidate's `core_commit` to
`tests/review_lane_pin/test_review_lane_caller.py`:180 and :296, which refuse a
pin that does not declare exactly one readable 40-hex `core_commit`, in the suite
that runs on the pull request. That keeps a malformed commit from LANDING, but not
this gate from publishing a false `success` first: a `core_commit` that is not a
commit, declared `diverged`, differs from any commit the surfaces agree on, so an
inequality reports agreement. The verdict is the gate's own claim, so the gate
validates its own input: a candidate `core_commit` outside the grammar FAILS in
the first outcome, with nothing read in the aggregation. The two rules are not
one rule stated twice: the suite's refuses a pin that cannot land, and this one
refuses a verdict that would be false.

## D17 — the allowlist is REMOVED, because the capability already forbids it

Copilot `r4078145229`, and review `5285808064`'s *previously missed* item, from
two sides. The requirement runs the check on EVERY proposed advance and the pull
request that carries it, while D14 and D14d scoped the gate to the bot's pull
requests alone — and this capability's promoted *An automated pin advance is
judged by the freshness checks that already exist, with no exemption*
(`openspec/specs/review-lane-floor-mirror/spec.md`:314-328) forbids exactly that:
*"none of them branches on the pull request's author, branch name or automated
origin … an exemption of that shape is a defect rather than a policy"*. A
hand-authored advance leaves `lockstep.status` as false as an automated one —
`#1123`, the 2026-09-18 repair, was itself a hand-authored pull request changing
this very file (author `brettheap`, head `chore/review-lane-lockstep-residue-b21f0100`)
— and it would have drawn no verdict.

**Scoping the requirement to the automated lane instead would breach the same
rule from the other side**, which asks for the automated advance to be judged
*"at exactly the strictness they judge a hand-authored one"*. So the gate judges
every pull request that changes the pin, keyed on WHAT it changes — a `paths:`
filter — and never on who opened it.

**The allowlist was defence in depth, and the depth now sits where it holds for
anyone — which had to be checked rather than assumed, because removing it admits
pull requests from forks.** This repository is public and both repositories the
gate reads about are private (measured: `private: true` for `opensoft/xFactory`
and for `codeXfactory/codexFactory`), so anyone who can open a pull request here
may now start a run that holds the aggregation token. What that run can do does
not depend on who started it: base code runs; no head is checked out; the event
supplies only the pull request's number and `head.sha`, and nothing derived from
the event or the candidate — a step output, a parsed field, a parse error —
reaches a script except through `env:` or a file, never through a `${{ }}`
expression (Copilot `r4078835258`); the candidate is fetched from THIS repository
at that `head.sha` — a fork's head commit is readable here through its pull
request, as every pull request's head is published here as `refs/pull/<n>/head`
— and never from the head repository the event names, then parsed as inert data
and judged, never followed (D14c); the read plan is fixed in the gate's own code
(D19), so no pull request chooses what is read; the aggregation token is read-only and scoped to one
repository; and every value the verdict names comes from a grammar or a
vocabulary. A CANDIDATE value outside them, which is public already, is named only
as an inert, length-bounded code span whose line breaks and backticks are
replaced, so it cannot end the span; a SURFACE value, which is private, is never
named at all, only classified, related to `core_commit` and digested (D20).
**What such a run publishes is what the bot's own pull requests publish**: the
aggregation's default branch, its resolved commit and each surface's
classification, relation and digest, on this public repository, beside a
pin file that already publishes a private repository's commit as `core_commit`.
An outside author chooses when it is published, and nothing about what is read.

**The race with an automated approver is real, but not yet present** (Copilot
`r4078145216`). No approver admits a pin-changing pull request today — the
envelope's one candidate, `intent-rolling-custody`, admits only
`ideation/dashboard/intents/**` and `ideation/dashboard/gate-records/**` — and the
two active changes that would admit this lane inherit the obligation to wait for
the verdict, registered at `tasks.md` § 6.5.

**This is the second time on this packet that a defence I added was the defect.**
D14's same-repository condition would have run the head's copy of a
secret-bearing workflow, and D14d's triple would have exempted every
hand-authored advance. Both times the estate had already written the rule: once
as a test, once as a requirement in this very capability.

**And the `paths:` filter is EXACTLY `contracts/review-lane-pin.yaml`** (Copilot
`r4078252960`). With the allowlist gone, the filter is the only boundary between
the aggregation token and every other pull request; a broader one would mint the
token and publish the aggregation's commits on pull requests that do not touch
the pin. The one gap an exact filter leaves is the platform's own, a diff of more
than 3,000 files, and it is registered at `tasks.md` § 6.6.

**And every admitted pull request is judged, its declaration FIRST** (Copilot
`r4078425707`, `r4078883755`). The candidate's declaration is validated before
anything else: a declared state outside its two words, a `core_commit` that is
not a commit (D16), a `converged_with:` other than the read plan's workflow
members (D19), or a candidate that cannot be parsed at all (Copilot
`r4078425733`) FAILS before anything is minted or read. Every valid candidate is
then judged through the remaining outcomes, a `reason:`-only edit included.

**A skip was tried and is withdrawn.** Copilot `r4078308120` asked that the token
not be minted for an edit that moves no judged value, and a `skipped` conclusion
answered it. `r4078883755` then found that the requirement's outcomes are
ordered, with exactly one holding for any input, so a `skipped` beside them was a
bypass the requirement does not authorize. The exposure the first finding named
is now closed where it lives rather than by skipping: a run reads only the plan
fixed in its code (D19) and publishes no aggregation value as it is (D20). The
first finding had also proposed `core_commit` alone as its condition, which would
have skipped the pull requests that move only the declaration, half of what this
check judges; `#1123` was one, moving `status: converged` to `status: diverged`
and leaving `core_commit` where it was.

## D18 — the gate's identity is chosen ONCE, and every part of the packet uses it

Review `5285930613`'s *previously missed* item: the binding's `resolved_by`, the
mint, the trigger tests, the publisher and § 6.5's lookup all address the gate,
and nothing named it. An implementation could have built a gate those parts did
not agree on. So the packet names it here, once:

| part | name |
| --- | --- |
| workflow | `.github/workflows/review-lane-lockstep-gate.yml` |
| its one job id, and so its own check-run's name | `review-lane-lockstep-gate` |
| the verdict check-run, the gate's identity wherever a check is required or read | `review-lane-lockstep-verdict` |
| binding template | `contracts/review-lane-lockstep-gate-binding.template.yaml` |
| `consumer.holder_ref` | `"openxfactory:workflow:review-lane-lockstep-gate"` |
| `consumer.fetch_identity` | `"github-actions:openxfactory:review-lane-lockstep-gate"` |
| `resolution.resolved_by` | `review_lane_lockstep_gate_workflow_only` |

Each follows the advance lane's own naming — `review-lane-repin.yml`, job
`review-lane-repin`, `holder_ref: "openxfactory:workflow:review-lane-repin"`
(`contracts/review-lane-repin-binding.template.yaml`:100), `resolved_by:
review_lane_repin_workflow_only` (`:167`) — and none collides with anything that
exists. Measured: no file under `.github/workflows/` or `contracts/` carries
`lockstep` in its name, no job declares a `name:`, so each job's check run is named
after its id, and none of the fifteen job ids across the fourteen workflows is
either name above.

**The verdict's name matches no job id in ANY workflow, not only its own, and no
job's `name:` either.** A job elsewhere with the verdict's name would publish a
check run under it — a declared `name:` is what a job's check run carries when
one is set — and a required check or § 6.5's approver would then read that job
instead of the verdict. § 5.1e's test asserts the wider rule, and § 5.1f's test holds the
binding, the workflow and the names together.

## D19 — the read plan is FIXED IN CODE, because the base is data too

Copilot `r4078365046`. D14c took the read plan from the base so that no candidate
could choose what the xFactory token reads, but the base's pin file is only the
candidate an earlier pull request proposed. The pin's own test checks nothing of
`converged_with:` but its length
(`tests/review_lane_pin/test_review_lane_caller.py`:648-649), and D17's skip rule,
since withdrawn, would have let a pull request that changed only `converged_with:` land unjudged.
That pull request could have installed any `opensoft/xFactory` path for every
later run to read with the private token.

**So the plan is the gate's CODE, not the pin file's data.** It has two WORKFLOW
MEMBERS, the judging workflows `converged_with:` names today —
`opensoft/xFactory .github/workflows/merge-master-approval.yml` and
`opensoft/xFactory .github/workflows/council-convening-lane.yml`
(`contracts/review-lane-pin.yaml`:1019-1020) — each read at the `ref:` of its step
that checks out `codeXfactory/codexFactory`; and one ADDITIONAL fixed read, the
`MIGRATION_PIN` assignment in `tests/test_merge_master_workflows.py`, which is not
and never becomes a `converged_with:` member (`tasks.md` § 6.2; Copilot
`r4078528181`). The candidate's `converged_with:` is JUDGED against the plan's
workflow members and never followed. Where it names any other set, the
check FAILS naming both, before anything is read, in the class of a declared
state outside its vocabulary, so no outcome is added. The base is not judged
separately: a candidate inherits the base's list unless it changes it, so a
base's defect FAILS every candidate that carries it, and a candidate that repairs
it is judged on what it proposes rather than failed for what it replaces.

**A pull request that moves the plan and `converged_with:` together fails its own
gate**, because the base's code judges it. That is the base-code rule's ordinary
cost. The verdict names both sets, so a reviewer sees exactly what moved, and the
next run, from the new base, agrees.

## D20 — a value read from the private aggregation is published as a commit or not at all

Copilot `r4078468841`. The fixed plan (D19) stops a pull request choosing WHAT is
read, but not what is PUBLISHED. The requirement named a non-commit surface by its
value, and this gate runs on a public repository, for any pull request, with a
verdict and a run log that are both public. A selector changed or compromised in
the private aggregation could carry a credential, and bounding its length or
replacing its delimiters would still publish it.

**So no surface's value is published as it is** — not even one with a commit's
grammar, because forty lowercase hexadecimal characters prove the shape and not
a commit (Copilot `r4078835190`): a legacy personal access token, for one, was
forty hexadecimal characters. A surface outside the grammar is published only as
its CLASSIFICATION: absent, empty, or not a commit. A surface inside it is
published as its relation to `core_commit` — equal or not — and a digest, the
first twelve hexadecimal characters of the SHA-256 of its value. Where it equals
`core_commit` the relation says so, and nothing is disclosed that this
repository does not publish itself. The one aggregation value named as it is, is
the commit the check resolves the default branch to, which the API returns as a
commit rather than as a field that merely looks like one. Verifying that a
surface's value is a real commit would need a read of `codeXfactory/codexFactory`,
a second repository the gate's one mint deliberately does not reach (D13). A
reviewer with access to the aggregation reproduces every value with the same call
the run made, and its digest with one hash. **The candidate's own values are
different**: the candidate is the pull request's own public content, so a
candidate value outside its grammar is still named, inert and length-bounded, as
§ 5.1g says.

**And overlapping runs are serialized** (Copilot `r4078468867`). One pull request
can start several runs — `opened`, `synchronize`, `reopened`, a re-run — and each
reads mutable aggregation state, so an older run finishing late could publish the
latest verdict under the declared name. The gate takes the answer
`merge-master-approval.yml`:427-434 gives for its own verdict, a per-pull-request
`concurrency:` group with `cancel-in-progress: true`, *"a superseded run's verdict
is stale by definition"*. It also re-reads `head.sha` once more immediately before
publishing. Neither is atomic with the check-run creation (Copilot
`r4078883704`), so the guarantee is the one that holds without atomicity: the
verdict is attached to the one commit it verified and binds nothing else, and
every consumer reads it only on the pull request's current head (`tasks.md`
§ 6.5).

## D5 — what the check compares, and why it is values rather than authorship

The comparison is `core_commit` against the commit the aggregation's JUDGING
surfaces name, and nothing else. It does not ask which act last wrote the field,
whether the last mover was a lane or a hand, or whether a ceremony was recorded.
Those are questions about provenance and the pin file already records them at
length; the check answers one question — **are the two commits the same** — and
reports the declaration against it.

**The `converged_with:` list is the check's own subject list and it names TWO
surfaces**, the places a core is actually checked out and run, while
`MIGRATION_PIN` is the aggregation's test constant holding those two identical to
each other. This packet does not promote the constant to a converged-with member
— that is the pin owner's call and the field has been through three cycles
without it — but the check reads all three, because a constant that disagreed
with the two workflows it guards is a fact worth reporting even though it is the
aggregation's own to repair.

**Each of the three is read at a named selector, not found by a pattern** (review
`5285753827`'s *previously missed* item): the `ref:` of each workflow's step
that checks out the pin's own `repository:`, parsed as YAML, and the
`MIGRATION_PIN` assignment in `tests/test_merge_master_workflows.py`. Measured on
`opensoft/xFactory` `main` `6e52e98e`, each file carries exactly one 40-hex
literal today, at `:152`, `:308` and `:72` — so a file-wide match would happen to
work, and would stop working silently the day a comment carried a second.
