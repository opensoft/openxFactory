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
