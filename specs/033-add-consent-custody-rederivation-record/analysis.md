# Specification Analysis Report — 033-add-consent-custody-rederivation-record

**Run**: 2026-09-09, lane `opsXfactory-1`, after the no-arg checklist set closed
to zero. **Artifacts**: `spec.md`, `plan.md`, `tasks.md`, `research.md`,
`clarify-questions.md`, `.specify/memory/constitution.md` v1.0.0, and the
ratified packet at `openspec/changes/add-consent-custody-rederivation-record/`.

**Extension hooks**: `.specify/extensions.yml` registers `speckit.git.commit` on
both `before_analyze` and `after_analyze`, both `optional: true`. Neither was
auto-executed; the tree is committed by the lane's own explicit-pathspec commits.

## Findings

**ZERO.** No CRITICAL, HIGH, MEDIUM or LOW finding across the six detection
passes. This is a SECOND-pass result, not a first-pass one: the no-arg checklist
set ran first and found **46 defects across 431 items in ten checklists**, all
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
| Ratified delta scenarios | **22 / 22 in the matrix** — 16 realized here, 6 NOT-OWED with the C-7 reason (all six git-dependent) |
| Box accounting | **35 TICKED + 3 NOT-OWED-HERE + 8 NOT-OWED = 46** |
| Checklist items | **431 / 431 ticked, 0 open findings** across ten checklists |

## Constitution alignment

No violations. **One declared deviation**, recorded in `plan.md` rather than
silently taken:

> Principle V requires the affected validators green before any commit is
> pushed. Phase B deliberately leaves `contracts/manifest.yaml`'s
> `consent-instrument` digest stale until Phase G's candidate commit closes it
> (clarify Q5a, which ruled against splitting the manifest edit). The principle
> is satisfied **at the pushed head**, which is what CI evaluates; T017 makes
> the intermediate commit state the staleness and name the commit that closes
> it.

The principle's purpose is that pushed work be green, and pushed work is green.

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
- Checklist findings raised then closed: **46**

## Next actions

No CRITICAL or HIGH issue blocks implementation. The two gates before `T010` sit
outside this seat:

1. **Brett Heap's Q2 ruling is IN** — exit `3`, *"needs a human decision"* — so
   nothing in clarify round 1 is open.
2. **Phase F remains BLOCKED** on the lane's row-3 substrate note for the two
   sibling-row README sentences. Phase G must not wait on it; T055 carries the
   cadence and the terminal disposition.
