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
it, to the reviewer who is already looking at that diff, before the platform
auto-merge that lane arms can land it unattended.

**A gate that BLOCKS the advance was considered and is deliberately not
required.** Divergence is a lawful state — the pin file has carried it, with
reasons, through four cycles — and a check that refused every advance leaving the
aggregation behind would refuse the ordinary case the estate designed for. The
obligation is to REPORT a declaration the measurement contradicts, not to forbid
the state it reports.

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
with each surface named and its value quoted, concluding neither `converged` nor
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

**The realization adds a `pull_request`-triggered gate of its own**, on the
estate's existing pattern — `openspec-cli-pin-gate.yml` and
`openreposhape-pin-gate.yml` are each their own `pull_request` workflow and each
a required check. **`review-lane-repin.yml` deliberately does NOT gain a
`pull_request` trigger**: that workflow's whole shape is *propose an advance*,
and a pull-request trigger would fire the advance logic on every pull request in
the repository. § 5.1b makes that a TESTED negative control rather than a
convention — a test requires `pull_request` to be ABSENT from the advance lane's
triggers.

## D8 — each outcome carries a CONCLUSION, and only one of the four fails

Copilot's *previously missed* item on this round found that the requirement
defined an UNDETERMINED semantic state and never said what the CHECK concludes,
leaving an implementation free to fail the gate on an xFactory outage — which D4
rejects — or to pass without a visible neutral result. **Taken, and it forced the
missing half of D2.**

| outcome | conclusion | why |
| --- | --- | --- |
| declared state CONTRADICTED by the measurement | **FAIL**, naming both values | this repository's own contract file states something false about another repository; the remedy is one edit to the field |
| surfaces disagree with each other (INCONSISTENT) | **NEUTRAL**, visible | another repository's defect, and not this repository's claim to answer |
| aggregation unreadable (UNDETERMINED) | **NEUTRAL**, visible | another repository's availability, and D4's whole point |
| declared state agrees | pass | |

**A NEUTRAL conclusion is not a pass and silence does not stand in for it.** A
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

**And the asymmetry is deliberate.** The one outcome that fails is the only one
whose subject is THIS repository's own file. The two neutral ones are facts about
the aggregation; turning either into a red build here would make the check a
liability its owners would route around, which is how a governance check stops
being run.

## D9 — the outcomes are ORDERED, because two of them overlapped

Copilot `r4076152698` found that the stale-`converged` scenario's WHEN was true
*whenever at least one surface does not name the new commit* — **including when
the surfaces disagree with each other**, which the INCONSISTENT scenario then
requires to be NEUTRAL. **The same inputs demanded both FAIL and NEUTRAL.** That
is not a wording problem; it is a requirement no implementation could satisfy.

Fixed by stating the order in the body — UNREADABLE, then DISAGREEING, then the
comparison, then the declared state, each reached only where every earlier one
does not hold — and by qualifying both comparison scenarios' WHEN with *the
aggregation's surfaces agreeing with each other, and read*. Exactly one outcome
holds for any input, and no implementation has to arbitrate.

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
nothing at all for the aggregation. **So on today's credentials the check would
answer UNDETERMINED on every run** — and a check that never concludes looks
exactly like a check that is working, which is the failure this packet exists to
end rather than to reproduce in a new place.

Three things follow, and all three are now written down. The realization declares
a READ-ONLY binding for `opensoft/xFactory` in the same shape as the existing
grant, keeping the family's own rule (*"neither repository's lane may reach into
the other's"*) by carrying the same `never_grants:` set. The requirement forbids
UNDETERMINED as a STANDING state: where the check cannot read the aggregation on
every run, the defect is its own access and is reported as that, not as a
property of the measurement. And § 5.4's realization evidence is no longer *one
observation of the check running* but **one observation of it CONCLUDING** —
because an observation of UNDETERMINED proves the access is missing, not that the
check works.

## D11 — the neutral conclusion needs a representation, and the PR host needs its own reading

Two more from the same round, both about the gap between what the requirement
says and what a workflow can express.

**`r4076152473` — a step exits 0 or non-zero, which is a green pass or a red
failure and nothing else.** *"NEUTRAL, visible, not reported as a pass"* has no
expression by exit code. So the realization publishes through the check-run API
with conclusion `neutral` and the values in its output, and the test asserts the
PUBLISHED CONCLUSION for each outcome rather than the process exit code —
**because this contract degrades silently to a green pass if nobody checks which
of the two was published.**

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

🤖 Generated with [Claude Code](https://claude.com/claude-code)
