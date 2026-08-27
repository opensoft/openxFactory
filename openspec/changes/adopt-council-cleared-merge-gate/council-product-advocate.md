# Council — product-advocate seat

Status: draft
Round: council, 2026-08-27
Subject: `adopt-council-cleared-merge-gate`, post-alignment draft
**SEAT VERDICT: APPROVE WITH CONDITIONS** — five conditions, all accepted.

This seat was asked to judge value, scope, and whether the change is worth doing
at all — and to be an honest advocate rather than a friendly one. It measured
instead of arguing, and the measurement is the most consequential single artifact
the council produced.

## The measurement

Every file of the last 140 merged pull requests on `opensoft/openxFactory`,
classified against the four allowlist entries, counting a pull request only if
**all** its files fall inside:

| Window | Merged PRs | Entirely inside the allowlists |
| --- | --- | --- |
| Most recent 40 (2026-08-26 → 08-27) | 40 | **0** |
| Next 100 back (2026-08-24 → 08-26) | 100 | **13** (9.3% of 140) |
| The derived class, all history | ~400 | **0** |

**The 13 are one finished campaign, not a rate.** Nine are single-file appends to
*one* file, `docs/archive-record-discrepancies.md` (#286, #288, #297, #300, #301,
#302, #303, #307, #309, #311); two are `ideation/staging/` pairs (#294, #296);
one is a runbook typo fix (#398). Twelve of thirteen landed on 2026-08-24/25.
That register work is done and the trailing 40 pull requests contain **zero
successors**.

The derived class is worse than thin — it is empty. Its two trees have been
touched by **three pull requests ever** (#38, #64, #381), and #381 also carried
`ideation/cross-reference.yaml`, so even it would not have cleared. The floor's
own comment explains it: "no class uses them today (Phase 2 is held)."

**Measured expected benefit: ~0 pull requests per week today; ~3/week at the peak
of an ended campaign.** The seat's judgement: "That is not worth seven gates on
its own merits."

## Where the traffic actually is

The near-miss list found it. **Four of the recent 40 merged pull requests are
single-file diffs whose only file is `openspec/changes/**/tasks.md`** (#410,
#413, #436, #441) — checkbox ticks, 10% of recent traffic, higher than the
clearable class at its historical peak. Adding one-file-off cases (#430, a
`review/` record) the pattern is unmistakable: **openxFactory's bypass ritual is
bookkeeping under `openspec/`, not prose.**

The proposal is right that doctrine floors it and right that
`regular-pr-council-clearance/spec.md:55` forbids narrowing a floor to reach it.
The seat's objection is that the packet left this **unsaid**, so "a reader
currently closes this packet believing the narrow slice is all there could ever
be, when in fact the high-value class exists and is merely locked behind a
doctrine amendment nobody has proposed."

## What the seat defended

**The sequencing — and it called this the strongest part of the packet.** Value
here is option-closing, not throughput, and it is already realized: the packet
killed the convener's sketch on both doctrine and mechanics, found G4b, and
converted "most openxFactory PRs qualify" from an assumption into a measured
falsehood. "Premature governance is governance that constrains a mechanism whose
shape is unknown; this constrains a mechanism whose shape is *already committed*
in codexFactory's `council_clearance.py`. It will not be re-litigated by the
arrival of G1/G2, because G1/G2 land signature verification, not
classification."

It also declined to call the gates creep: G5 and G4b are load-bearing and G7 "is
the single most important line in the document."

## The canary was unsatisfiable — the hard blocker

N=6 split ≥3 per class. Prose fills in ~1 day at campaign rate and **never** at
current rate. Derived: 3 qualifying pull requests in ~400 is 0.086/day
optimistically, so ≥3 needs **~35 days at best and is unbounded in practice**,
because Phase 2 is held and no lane writes those trees.

G7 requires the canary complete. **Therefore, as written, the flip to `clearable`
could never open, and the packet would have ratified a boundary that is
structurally unexercisable.** In the seat's words: "That is not caution, it is a
null."

## Dispositions

1. **PA-C1 — APPLIED.** The measured numbers are now in the proposal body under
   "The value this delivers, MEASURED — and it is very small": 0 of the last 40,
   13 of 140, 12 of those 13 from one closed campaign on one file, 0 of ~400 in
   the derived class. "A steady stream" is explicitly withdrawn, and the section
   states that the measurement is the strongest argument against ratifying on
   throughput grounds, published rather than buried.
2. **PA-C2 — APPLIED.** The canary is **prose-only, N=3**, zero disagreements;
   each enrolled class carries its own canary in the change that enrolls it. The
   ≥3-per-class split is removed. This preserves the class-boundary-error
   detection the alignment round asked for without conditioning adoption on
   nonexistent traffic.
3. **PA-C3 — APPLIED.** `openxfactory-derived-health-artifact` is **demoted to a
   successor change**, gated on a wired producer existing and the Phase-2 hold
   being lifted. (The adversary and systems-architect seats required the same
   removal on independent security and structural grounds, so this was the
   council's one unanimous act.)
4. **PA-C4 — APPLIED.** A proposal subsection, "The high-value class this change
   cannot reach, named so it is not invisible", records the
   `openspec/changes/**/tasks.md` measurement and the `GATE_INTEGRITY_FLOOR` /
   `spec.md:55` blocker, and raises **Q7**: does the convener want a doctrine
   amendment defining a checkbox-only class by **diff shape** rather than path —
   the objection to `openspec/changes/**` being that it holds the change records,
   which a checkbox tick does not alter — or should the pilot move to
   `opensoft/xFactory`, which has real traffic to canary against? A task records
   it too.
5. **PA-C5 — APPLIED as Q8** rather than as a unilateral rule, since binding
   future proposals is the convener's call: should every clearance proposal in
   this family state a falsifiable expected-benefit figure measured against
   merged-pull-request history? Recorded with the admission that **this proposal
   would have failed that test at authoring**, four days before the council
   caught it.

## The seat's closing recommendation, carried to the convener unaltered

> Enroll a third candidate class and make it the pilot's real subject —
> `openspec/changes/**/tasks.md`-only bookkeeping diffs — declared advisory, and
> name the doctrine amendment it requires as an explicit gate rather than an
> unasked question. That is the traffic. Everything else is a rounding error.

This packet does **not** do that: it cannot, without a floor narrowing that
ratified doctrine forbids. It carries the recommendation as Q7 for the convener
to rule on, which is the only disposition available to a change that may not
narrow a floor.
