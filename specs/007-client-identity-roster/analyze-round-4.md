# Analyze round 4 — 007-client-identity-roster

Date: 2026-08-14. Same scope and dimensions, run fresh against the
post-round-3 artifacts, with a cross-artifact identifier sweep
(`duty_separation_rationale`, `no_standing_credential`, fixture counts, probe
counts, `ratified_by`) confirming every new term appears in every artifact that
should carry it and nowhere it should not.

Four findings, two of them defects this loop's own earlier edits introduced.

## Findings

### F-031 — MEDIUM — round 1's member-spelling insertion split the `admission[]` paragraph

*Artifact*: plan.md Cluster A, the `admission[]` members block.

The "Member spellings are snake_case everywhere" paragraph (round 1's F-003
fix) was inserted between the `admission[]` member list and the sentences that
finish it, so the `evidence_ref` pointer rule and the effective-reach rule —
both about `admission[]` — now read as a continuation of a paragraph about
token spelling. The content is correct and complete; the placement makes the
`admission[]` definition look truncated and buries FR-037's derivation rule.

*Fix applied*: `admission[]`'s members, `evidence_ref` and effective reach
restored as one block; the member-spelling note moved after it as its own
paragraph.

### F-032 — LOW — "plus nothing except the legend's consequences" is no longer true of the entry table

*Artifact*: plan.md Cluster A, the sentence introducing the entry field table.

The table now also carries `duty_separation_rationale` (round 2's F-020 fix).
Both additions come from the same ruling (R7) and spec.md FR-001 records both,
but the plan's introduction still names only one.

*Fix applied*: the sentence now names both R7 consequences, matching FR-001.

### F-033 — MEDIUM — Phase 1's header contradicts Phase 0's checkpoint about 0.3

*Artifacts*: tasks.md Phase 1 header ("**Depends on**: nothing (0.x are
advisory except 0.1's gate on Phase 3)") against the Phase 0 checkpoint ("0.1
ruled, 0.2 clean, 0.3 captured → Phase 1 may begin").

One says the baseline is advisory, the other makes it a precondition of Phase 1.
Neither is quite right: 0.3 is a BEFORE-STATE, so it is not advisory at all —
it must precede the first edit to any of the four MODIFIED capabilities'
surfaces (Phases 5–8), which is what 8.6 and 10.4 diff against — while Phase 1
creates a new file and touches none of them. A reader following the header
could start Phase 8 with no baseline and make FR-030's "unmodified in
behaviour" unmeasurable; a reader following the checkpoint could block Phase 1
on a baseline it does not need.

*Fix applied*: both statements replaced by the precise rule — 0.3 gates the
first edit to any MODIFIED capability surface (Phases 5, 6, 7, 8) and does not
gate Phase 1's new-file work; 0.1 gates Phase 3; 0.2 gates 8.2. The dependency
section already carries this and is now consistent with both.

### F-034 — LOW — 0.2's estate sweep needs the tree 0.3 confirms

*Artifact*: tasks.md 0.2 (*Files*: "…and any `xFactories/*/` registry reachable
from the aggregation checkout"), marked `[P]` alongside 0.3.

0.2 cannot cover the domain registries unless the aggregation checkout is
reachable, which is precisely what 0.3 now establishes. As written, an
unreachable aggregation checkout silently narrows ruling A-7's sweep to the
openxFactory tree while the task still reports "clean".

*Fix applied*: 0.2 now records the sweep's REACH with its result, and a sweep
that could not see the domain registries is reported as such rather than as a
clean estate sweep.

### F-035 — LOW — one inserted block merged into the paragraph after it, plus four mis-wrapped lines

*Artifacts*: plan.md Cluster D (the round-2 BC reconciliation block ran
straight into the `evidence_ref` sentence that follows it, so a paragraph about
which SURFACE the acts belong to now reads as the preamble to a paragraph about
evidence pointers); spec.md FR-034, research.md Decision 7, tasks.md 5.1 and
6.7 (single lines left at 88–103 characters against these files' consistent
~78-character wrap).

Cosmetic in three of the five sites and structural in the first: an inserted
block that swallows the next paragraph changes what the reader takes the
paragraph to be about.

*Fix applied*: paragraph break restored in Cluster D; the four long lines
re-wrapped. No wording changed.

## Rounds 1–3 findings re-checked

All hold. The identifier sweep confirms: `duty_separation_rationale` in spec (2),
plan (3), tasks (3); `no_standing_credential` in plan (3), tasks (2); the
fixture corpus reads SIX repo fixtures in both plan and tasks with no "FIVE"
remnant; the probe count (32) appears once, in the plan, with its composition
corrected in round 3; `ratified_by` carries the presence-only reading in all
four artifacts.

## Escalations

None.
