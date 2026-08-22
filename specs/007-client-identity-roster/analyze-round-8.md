# Analyze round 8 — 007-client-identity-roster

Date: 2026-08-14. Final round of the continuation (cap: rounds 6–8). Fresh
full-dimension pass over the post-round-7 artifacts, followed by a documented
POST-FIX RE-SWEEP whose result is the evidence for zero.

## Findings

### F-048 — LOW — FR-001's exhaustiveness claim and FR-002's act-level addition read as a contradiction

*Artifacts*: spec.md FR-001 ("the legend and the duty-separation rationale are
the only additions the 2026-08-14 rulings make to it") against FR-002's
`exceeds_governed_unit` (added by round 6).

Both statements are true — FR-001 governs the ENTRY's field list and FR-002 the
ADMISSION ACT's, which are different lists — but nothing said so, and a reader
checking whether the record had grown beyond its ratified shape would find an
"only additions" claim in one requirement and a third addition two requirements
later.

*Fix applied*: FR-001 now scopes its claim to the entry list explicitly and
names the act-level addition, its home (FR-002), and the ratified obligation
that justifies it — so the exhaustiveness claim stays checkable instead of
becoming a thing a reader has to reconcile alone.

### F-049 — LOW — four wrap defects from the rounds 5–7 edits

*Artifacts*: spec.md FR-008 (twice, the second introduced by the first fix),
research.md Decision 7, tasks.md 2.6.

Same class as F-035: paragraph re-flow left single lines at 86–99 characters in
files that wrap at ~78. Three were normalized before this round's sweep under
F-035's standing remediation; the fourth was introduced BY that normalization
and caught in the re-sweep below — which is the reason the re-sweep exists.

*Fix applied*: all four re-flowed; no wording changed. The only lines now over
82 characters in the four artifacts are three pre-existing ones carrying long
inline paths (`research.md:1000`, `research.md:1075`, `tasks.md:3`), none
authored by this loop.

## Post-fix re-sweep (the evidence for zero)

Run after the two fixes above, across every dimension, mechanically where
mechanically checkable:

| Dimension | Check | Result |
|---|---|---|
| Requirement coverage | every `**FR-xxx**:` / `**SC-xxx**:` in spec.md against the coverage table's rows, computed both directions | **53 ids, 53 rows, exact bijection** — none unmapped, none orphaned |
| Coverage integrity | every `<phase>.<n>` referenced anywhere in tasks.md against the tasks actually defined | **69 tasks defined, zero dangling references** |
| Fixture counts | plan's negative tree vs its prose claims vs task 4.1's filename list | 28 files in the tree, "28 packaged" claimed, 17 filenames in 4.1 which says SEVENTEEN, "31 rule-homes", "33 refusing probes" — all reconcile |
| Terminology | `exceeds_governed_unit`, `duty_separation_rationale`, `no_standing_credential`, `achieves` across all four artifacts | present in every artifact that spells the rule they serve; no hyphen/snake drift; no new closed vocabulary |
| Constraint fidelity | residual-pattern sweep for every superseded formulation this loop replaced (unused-legend rule, "or its roster sibling", unqualified "(task 3.x)", "FIVE tmp_path", "six vocabulary negatives", `enforcing_check`, pre-F-037 permission phrasing) | **zero hits** |
| Dependency soundness | Phase 0 gates (0.1→Phase 3, 0.2→8.2, 0.3→first edit in Phases 5–8), field→rule→positive→negative ordering for every field added in rounds 5–7 | consistent; no ordering claim contradicts another |
| Ambiguity residue | every rule added in rounds 5–7 has a named mechanism, a schema task, a validator task, a fixture and a coverage row | complete for all seven (`duty_separation_rationale`, object-form `granted_permissions[]`, the `per_unit_principal_available` map, the attestation shape, `exceeds_governed_unit`, `consent_ref` resolution, the FR-010 name-check token list) |
| Line hygiene | non-table, non-path lines over 82 characters | three, all pre-existing |

**Result: zero.** No finding remains open and none was deferred.

## Honest note on the loop's shape

The zero above is a post-fix re-sweep INSIDE round 8, not a separately numbered
round 9 — the continuation's cap is rounds 6–8 and it was respected. What that
means precisely: round 8's ANALYSIS produced two LOW findings (both wording
hygiene; every substantive dimension was already clean when the round opened),
both were fixed, and the re-sweep above then found nothing. A ninth round would
be re-running the table above against unchanged artifacts.

The rounds are visibly converging in severity: HIGH findings in rounds 1, 2, 5
and 6 (structural gaps and unimplementable rules), MEDIUM in 3, 4 and 7
(composition failures across summary surfaces), LOW only in 8.

## Escalations

None — in this round or in any of the eight.
