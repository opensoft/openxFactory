# Specification Analysis Report — 033-add-consent-custody-rederivation-record

**Run**: 2026-09-09, lane `opsXfactory-1`, after the no-arg checklist set closed
to zero. **Artifacts**: `spec.md`, `plan.md`, `tasks.md`, `research.md`,
`clarify-questions.md`, `.specify/memory/constitution.md` v1.0.0, and the
ratified packet at `openspec/changes/add-consent-custody-rederivation-record/`.

**Extension hooks**: `.specify/extensions.yml` registers `speckit.git.commit` on
both `before_analyze` and `after_analyze`, both `optional: true`. Neither was
auto-executed; the tree is committed by the lane's own explicit-pathspec commits.

## Findings

**THIS SECTION'S VERDICT WAS SUPERSEDED, AND IS LEFT STANDING WITH THE
CORRECTION RATHER THAN REWRITTEN TO LOOK PRESCIENT.** It recorded ZERO findings
at commit `489be604`. A **consistency panel** then ran on that same commit and
returned **PROCEED AFTER FIXES** with TEN findings — including two HIGH defects
this pass did not catch (the cut-coupled tests the cut reds, and the
manifest-edit split), one HIGH unimplementable assertion (the naive no-git ban),
and a MAJOR miscount of the scenario taxonomy in this feature's own favour.
**A zero-finding analyze pass is not a clean bill of health.** The figures in
this report are the POST-FIX ones. The six passes read: This is a SECOND-pass result, not a first-pass one: the no-arg checklist
set ran first and found **46 defects across 430 items in ten checklists** (430 MEASURED — panel F8 corrected 431), all
fixed and re-verified before this analysis ran. The analyze pass confirms a tree
that has already been attacked — which is the only reading under which a
zero-finding report carries information.

| Pass | Result |
| --- | --- |
| **A. Duplication** | No near-duplicate requirements. 39 FRs, no duplicate ids, no two FRs asserting the same MUST. |
| **B. Ambiguity** | No placeholders (`TODO`, `TKTK`, `???`, `FIXME`, `[NEEDS…]`) in any artifact. The three vague-adjective matches are all `non-fast-forward`, a git term of art rather than an unmeasured quality claim. Every numeric claim in `spec.md` and `research.md` carries the command that produced it. |
| **C. Underspecification** | Every FR names an object and a measurable outcome. Every task names the file it writes. No task references a component absent from `spec.md`/`plan.md`. |
| **D. Constitution alignment** | Principle-by-principle table in `plan.md` against all seven principles, the Repository Constraints and the Development Workflow gates. **One deviation DECLARED rather than hidden** (below). No MUST violated. |
| **E. Coverage gaps** | 100% both ways — see the coverage summary. |
| **F. Inconsistency** | Phase letters now agree byte-for-byte between `plan.md`'s sequence table (A–H) and `tasks.md`'s `## Phase` headers (A–H). No terminology drift: `WITHHELD`, `candidate commit`, `NOT-OWED` vs `NOT-OWED-HERE`, and the seven finding codes are each used in exactly one sense. No task-ordering contradiction. |

## Coverage summary

| Dimension | Result |
| --- | --- |
| Functional requirements | **39** (FR-001…FR-047 with sub-letters), ascending order, **every one carrying an inline origin tag** |
| FRs with ≥ 1 task | **39 / 39 = 100%** — verified by diffing the FR ids in `spec.md` against the traceability table: IDENTICAL |
| Success criteria | **10** (SC-001…SC-010), each mapped to a gate task |
| Tasks | **75** (`T001`–`T083`, no duplicate ids), each naming the box, clarify answer, ruling or checklist finding it discharges |
| Unmapped tasks | **NONE** |
| Packet boxes §§ 0–5 | **38 / 38 covered** — verified by diff against the packet's own list: IDENTICAL |
| Ratified delta scenarios | **22 / 22 in the matrix** — **13 realized here, 9 NOT-OWED**, all nine git-dependent. The earlier 16/6 was WRONG, and wrong in this feature's favour; corrected by panel F4 |
| Box accounting | **35 TICKED + 3 NOT-OWED-HERE + 8 NOT-OWED = 46** |
| Checklist items | **430 / 430 ticked, 0 open findings** across ten checklists (MEASURED, panel F8) |

## Constitution alignment

No violations, **and no deviation** — the one this report previously declared is
WITHDRAWN by panel F2. The `consent-instrument` per-file digest is integrity
bookkeeping for the edited file rather than a release surface, so it is
re-derived in the § 2 commit that moves the schema. `validate-manifest-digests.py`
is green at EVERY commit on the branch, not only at the pushed head, and
Principle V is satisfied without qualification.

## Recorded, deliberately not closed

**A `path_only` entry whose two locators are IDENTICAL is refused by nothing.**
`path_only` means *"only the locator changed"*, so such an entry records an event
that did not occur. The contradiction is derivable from the record's own bytes,
so by design C-7's placement test the refusing leg WOULD be neutral and would
belong here. **No ratified task names it**, so this feature does not add it.
Surfaced for the architect; not taken on this seat's authority.

## Metrics

- Total requirements: **39 FR + 10 SC = 49**
- Total tasks: **75**
- Requirement coverage: **100%**
- Ambiguity count: **0**
- Duplication count: **0**
- Critical issues: **0**
- Checklist findings raised then closed: **46** (over 430 items)
- Consistency-panel findings raised then closed: **10** (2 HIGH scope/sequencing, 1 HIGH implementability, 2 MAJOR, 3 MEDIUM, 2 LOW)

## Next actions

The consistency panel's verdict is **PROCEED AFTER FIXES**, and the fixes are
applied. Nothing blocks implementation:

1. **Brett Heap's Q2 ruling is IN** — exit `3`, *"needs a human decision"*, with
   exit 2 keeping its ratified *"dependency/harness error"* wording.
2. **Phase F is DISCHARGED**, not blocked — the lane's row-3 substrate note is
   posted at [#630 comment 5603344475](https://github.com/opensoft/openxFactory/issues/630#issuecomment-5603344475),
   and it covers all four sibling sentences, which sit in ONE README row
   (`README.md:2854–3101`).
3. **Phases F and G are independent**; G never waits on F.
