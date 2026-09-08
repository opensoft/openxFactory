---
code_surface: openxFactory (`scripts/doc_health/family_enumeration.py` — a new module owning the twenty-first deterministic family: the requirement-prose reader, the enumeration splitter, the prose-name-to-registry-id normalization and its declared alias set, the number-word table, the three numeral checks, the canon/active-delta source selection, and the reporting-list direction check; `scripts/doc_health/families.py` — one import, one registration line in `FAMILIES`, one note recording why the family is deliberately absent from `FAMILY_RESOLUTION`, and the module docstring's owner list; `scripts/doc_health/__init__.py` — one entry in `FAMILY_IDS` so the family gets its own report section; `tests/doc-health/test_family_enumeration.py` plus `tests/doc-health/fixtures/family-enumeration*/` — one fixture per divergence class, the thin-delta prevention case, the pending-promotion negative, the alias-minimality pin, the self-gate assertion against this repository's own tree, and the structural pins on the advisory launch; `tests/doc-health/test_lifecycle_scan_set.py` — the twenty-first family classified as a non-reader of the lifecycle scan set, which is the loud failure that test was built to produce. NO change to the governed corpus, the lifecycle scan set, any existing family's behaviour or measurement basis, the report schema, the regression-diff rule, or any threshold.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, following `add-duplicate-packet-check` and `govern-openspec-corpus-membership` exactly: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount this proposal predicts — which here is by nothing at all. The change therefore ships ACTIVE and archives only after the merge.
Status: ratified
Ratified: 2026-08-25 by Brett — in-session commissioning, verbatim: "commission the §5.5 enumeration check". The citation covers the DECISION TO BUILD THIS CHECK and nothing else; the four design decisions in § Orchestrator Decisions below were taken by the orchestrating session under standing patterns, are NOT covered by this citation, and are flagged there for veto. No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for that case, clearing its three-way floor on two axes rather than the one it needs: approver (`by Brett`) and date (`2026-08-25`).
Proposed: 2026-08-25
Origin: `openspec/changes/archive/2026-08-25-add-duplicate-packet-check/tasks.md` § 5.5, recorded-not-fixed at that packet's archive — "a requirement whose text every new family must restate is a requirement every new family can truncate — and the fix is to stop restating it: derive the enumeration and the counts from `FAMILIES` rather than re-typing them into canon".
---

# Proposal: add-family-enumeration-check

## Why

**`doc-health`'s own "Deterministic check families" requirement names every
check family and counts them three times in prose, and every new family has to
restate the whole requirement to add itself to the list.** Nothing checked that
the restatement was complete, or that the numerals still described the families
that actually exist.

**It broke three times in three days, and a human caught it every time.**
`add-release-inventory-drift-check`, `add-promotion-fidelity-check` and
`add-duplicate-packet-check` each wrote a `MODIFIED` block restating ONE of that
requirement's EIGHT scenarios. Two were caught at their own archive gates, one
by a parallel lane. Because `MODIFIED` replaces a requirement wholesale, each
would have destroyed seven scenarios on promotion — and the file-level scenario
count would not have moved, because the seven lost exactly offset the seven the
change's own ADDED requirement brought.

The enumeration half had already drifted before that, and more quietly:
`staged-topic-template` registered on 2026-08-15 and stayed uncounted until
2026-08-23. `families.py`'s own docstring records the lesson in one line — "a
number that only a human re-reads is a number that drifts."

`add-duplicate-packet-check` § 5.5 recorded the structural reading rather than
fixing it, and this change is the fix it named:

> The class is structural — a requirement whose text every new family must
> restate is a requirement every new family can truncate — and the fix is to
> stop restating it: derive the enumeration and the counts from `FAMILIES`
> rather than re-typing them into canon.

## What Changes

- **`doc-health` gains the twenty-first check family.** One MODIFIED
  requirement (the count chain reaches twenty-one; the family reads a promoted
  spec and a Python dict, neither of them a governed-corpus document, so no
  census, word count, canon-share figure, inventory entry or catalog record
  moves) and one ADDED requirement defining the check: the two halves, the
  pending-promotion rule, the name-resolution rule, and the advisory launch.
- **The implementation lands in this change**, on the precedent its three
  sibling families set: `scripts/doc_health/family_enumeration.py`, its three
  registrations, and 20 tests over seven fixtures.
- **No obligation is added to `document-lifecycle`.** The obligation being
  checked is `doc-health`'s own requirement about itself, not a lifecycle rule
  about documents in general — which is why this change carries a single
  capability delta where the three sibling families each carried two.

## Impact

- **Affected specs**: `doc-health` (MODIFIED + ADDED).
- **Affected code**: `scripts/doc_health/` (one new module, three one-line
  registrations), `tests/doc-health/`.
- **Measured effect on this repository's own health run**: **nothing moves.**
  The single-repo report on this branch is byte-identical to the same run on
  main except the new family's own empty report section. The headline is
  unchanged.
- **Measured effect on the real corpus, both halves**: canon's enumeration
  currently names twenty families and the registry registers twenty — **0
  findings on the canon half at the branch point.** With this change's own
  delta present, the delta half reads its restatement of twenty-one against a
  registry of twenty-one — **0 findings.** Both measured through the family
  itself, not by inspection.

## Orchestrator Decisions — FLAGGED FOR VETO

The commissioning ruling covers the decision to build this check. It does not
cover the four decisions below, which the orchestrating session took under
standing patterns.

**D1 — The canon half: name-set AND every numeral.** The promoted requirement's
enumeration must name exactly the registered families, each once, and its three
numerals must be arithmetically true of that set — the stated total, the
subset-of-total in "Four of the twenty", and the remainder in "the other
sixteen". Any divergence fires, naming precisely what diverged: which family
was omitted, which numeral was stale and what it should read, or which name
resolved to nothing. The three numerals are checked as a system rather than
individually, so a stale total does not also report as a broken remainder — the
fixture proves the classes separate.

**The scan-set reader count (`Four`) is canon's own claim and is NOT derived
here.** There is no runtime registry of which families read the lifecycle scan
set; that boundary is already pinned structurally by
`test_lifecycle_scan_set.py`, which asserts `_lifecycle_scope` appears in the
source of exactly the four declared readers. This family verifies the
arithmetic around that number rather than inventing a second authority for it.

**D2 — The active-delta half is the real prevention.** Any ACTIVE change whose
delta restates the requirement must carry the complete enumeration, consistent
with the registry in its own tree. A change that registers family N+1 also
states family N+1 in its delta, so the comparison is self-consistent, and the
truncation is reported **at authoring time** instead of at an archive gate.
Where two or more active deltas restate the requirement — precisely the
situation that produced the three truncations — each is checked independently,
because whichever archives last is the one canon keeps.

**Canon is exempt from the count comparison while an active delta restates
it**, and that is the load-bearing half of D2 rather than a loophole. A change
adding family N+1 leaves canon stating N until it archives; canon is PENDING
there, not divergent. Without this rule the family would fire on every
legitimate in-flight family branch, which is the fastest way to make a check
hated and then disabled. A fixture pins the pending case quiet.

**D3 — Advisory at launch, and BOTH halves of that.** Every finding is
`warning`, and the family is deliberately absent from `FAMILY_RESOLUTION` so a
resolved finding cannot become an `error` through the uncited-resolution rule.
Kept **even though the corpus measures clean** — two of the three sibling
families have since flipped to enforcing, and the flip is cheap; sequencing it
behind a measured population is the house rule rather than an obstacle, and
this family has one branch's worth of measurement rather than a population.
The flip is a recorded task box.

**D4 — Acceptance in both directions, and the self-gate is one of them.** Each
divergence class fires on its own fixture and is asserted on its rule text, not
on a count; the lawful patterns stay quiet, including the pending case. And the
REAL corpus reads zero on both halves — asserted by a test, against this
repository's own tree, through the family itself.

## The irony is deliberate, and it is the acceptance test

Adding this check as the twenty-first family forces **exactly the enumeration
restatement it polices**. That is not an awkwardness to apologize for; it is the
strongest acceptance evidence available, and it was run as a two-step
demonstration:

1. With the family registered and no delta written, the check reported **three
   findings against canon** — the omitted `'family-enumeration'`, the stale
   total (`'twenty'`, expected `'twenty-one'`), and the stale subset total.
2. With this change's delta written, the same call reports **zero**.

So this change's own restatement was verified by this change's own check,
before it could be committed. A wrong restatement here could not have landed,
because the thing it would have corrupted was standing at the gate. Two tests
pin it: one asserts the zero, and one asserts that the delta half actually READ
this change's delta, so the first cannot pass vacuously.

**The archive lesson was heeded too.** The MODIFIED block restates all EIGHT of
the requirement's scenarios; verified scenario-by-scenario against canon, seven
byte-identical and the eighth differing by exactly one `AND` bullet — this
change's own.

## What this proposal does NOT claim

It does not claim to fix the scenario-completeness half of the same class. This
check derives the ENUMERATION and the COUNTS, which is what § 5.5 commissioned;
a `MODIFIED` block that restates the enumeration perfectly and still drops
scenarios would pass it. That is the adjacent half, it is what actually
destroyed text three times, and it is recorded as an open box in `tasks.md`
§ 5.3 with a measurement rather than folded in here.

It does not repair `FAMILY_IDS`. That reporting list is missing two entries
(`proposal-origin`, a defect that capability already records, and
`staged-topic-template`), so two families run and report findings with no report
section of their own. This family checks only the other direction — that no
section is promised for a family that does not run. Repairing another
capability's registration inside this change would put unrelated report output
on this feature's evidence; the measurement is in `tasks.md` § 4 and the box is
§ 5.2.

And it does not claim the enumeration can never drift again by other means: a
family renamed in the registry and in canon at once would satisfy this check
while changing what the requirement means. The check verifies AGREEMENT between
two statements, not that either one is wise.
