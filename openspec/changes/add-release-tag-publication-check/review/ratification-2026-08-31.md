# Proposal Ratification: add-release-tag-publication-check

Status: ratified
Decision date: 2026-08-31
Ratifier: Brett Heap (repository owner) — in-session, in TWO ACTS
Ratified: 2026-08-31 by Brett Heap (repository owner) — in session; record: this
file.
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `tasks.md`, `.openspec.yaml`, the spec delta
`specs/doc-health/spec.md`, and the README's active-changes entry. **The delta's
`## MODIFIED Requirements` block is BYTE-UNCHANGED from the canon text it
restates except for the five enumeration edits the packet exists to make**: the
total (twenty-two → twenty-three), the family list (gaining `release-tag
publication`, last), the scan-set split ("Four of the twenty-two" →
"twenty-three"), the remainder ("the other eighteen" → "nineteen"), and one added
sentence describing the new family's document-list behaviour in the pattern the
block already uses for every family that takes neither document list. All eight
scenarios are carried unchanged. The ratification act adds D4's disposition, the
threshold's ruled value, and the sites that assert the packet's own standing.
Gates at the ratification commit, which are the COMMIT'S gates and not
`tasks.md` § 5's archive gate: `openspec validate --strict` valid and
`--all --strict` **82 passed / 0 failed**; `pytest tests/doc-health`
**1364 passed / 0 failed**; doc-health `--single-repo` against the merge-base
`8f986c394`, measured in a clean worktree so the base tree genuinely lacks this
packet — base **5 critical, 4 error, 28 warning, 12 info**, head **5 critical,
4 error, 28 warning, 13 info**, a movement of **+1 `info` and nothing else**.

**THE SEQUENCE CHANGED AFTER THE RULING, ON EVIDENCE, AND BRETT RULED THE
CHANGE.** This record first cited a proposal-only baseline and a movement of
+3 `warning` / +1 `info`. Running the suite showed those three warnings were not
a report movement to tolerate but a RED GATE: `family-enumeration`'s self-gate
asserts the real corpus reads ZERO on both halves, and a delta declaring
twenty-three against a registry holding twenty-two cannot satisfy it. The
precedent settles why — `add-family-enumeration-check`, which wrote that gate,
landed its delta, its module and its tests in ONE commit (`bc779dcc`), because a
family addition is one landing. Put to Brett with three options, he ruled: land
realization together on this branch. So the ratified baseline INCLUDES the
realization, `tasks.md` § 2 is discharged rather than deferred, and the
"ratification authorizes realization and performs none of it" sequencing is
COMPRESSED HERE BY RULING rather than by drift.

## Decision

**RATIFY, BY DIRECT RULING OF THE REPOSITORY OWNER.** The requirement set stands
as drafted. **All five orchestrator decisions flagged for veto in `proposal.md`
§ Orchestrator Decisions are ACCEPTED AS DRAFTED**, and D3's open number is ruled.

**The two acts, and why the sequence is recorded rather than collapsed.**

**Act one**, verbatim: *"accept D1, D2, D5; threshold N=5"*. That disposed four of
the five flagged decisions and settled the one number the authoring session had
declined to pick. **D4 was not named.** It was therefore carried as OWED — task
1.4 was opened for it, `Status:` stayed `draft`, and the packet recorded that
reading silence as acceptance would be narrowing a ruling by omission.

**Act two**, verbatim: *"accept D4, and yes that's the ratification"*, given after
D4 was put back to him as outstanding.

The sequence is kept because the alternative was available and wrong. D4 decides
what this family PROVES about a tag's target, and the packet's answer carries a
disclosed residue: it asserts the cheap conjunct — the tag must peel to a commit
that DECLARES the bundle — and does NOT prove the target is the EARLIEST such
declaring commit, so a tag on a later declaring commit passes this family and
remains a defect under `docs/contract-versioning-policy.md`. **That residue is now
accepted WITH its disclosure intact, rather than accepted by silence.** A packet
that had folded D4 in with the other four would have obtained the same words from
a ruler who had not been asked the question.

## The threshold

**N = 5 first-parent landings**, ruled in act one and stated in the delta as the
ruled default rather than a placeholder. The calibration it answers to, recorded
so a later reader can re-derive rather than trust: `contract-v2.3` sat untagged
across **six** first-parent landings on published `main` before a human noticed
it, so any threshold above five would have stayed silent through the exact
recurrence this family exists to catch.

## What this ratification does NOT do

**REALIZATION IS PERFORMED HERE, BY THE RULING OF 2026-08-31 RECORDED ABOVE**,
and this is a departure from the usual sequencing rather than the usual case.
`tasks.md` § 2 is discharged: the module exists, the family is registered as the
twenty-third, the count sites have moved, and the family runs and reports ZERO
over this tree — a genuine answer, not a skip. The departure is not a
convenience: canon, the code registry and the pins that measure them cannot
disagree across a merge boundary without reddening the gate that exists to
notice exactly that.

It does not fix **#338**, which D5 routes around rather than waits on. It does not
close **#528**, which closes when the check exists and runs. It does not touch
`Release-inventory drift`'s behaviour, severities, or resolution class (D1). And
it cuts no contract bundle, so — with the irony noted rather than risked — **no
release tag is owed by the change that checks release tags**.
