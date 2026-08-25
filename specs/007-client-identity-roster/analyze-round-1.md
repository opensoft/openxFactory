# Analyze round 1 — 007-client-identity-roster

Date: 2026-08-14. Scope: `spec.md`, `plan.md`, `research.md`, `tasks.md`
against each other, against `clarify-rulings-2026-08-14.md`,
`plan-gate-rulings-2026-08-14.md`, the amended packet
(`openspec/changes/add-client-identity-roster/`: proposal + five deltas +
design + both `review/` records) and the seed handoff.

Dimensions: (1) requirement coverage, (2) terminology and identifier
consistency, (3) constraint fidelity, (4) dependency soundness, (5) ambiguity
residue, (6) adversarial re-examination of the nine tasks-phase decisions.
No `.specify/templates/` analyze template exists; these are the dimensions the
analyze charter names.

**Line numbers are as-read before this round's fixes.**

Tree facts were re-verified rather than trusted: manifest at `contract-v1.31`;
`families.py:1` docstring, its ownership note at 7-11, the import at :25, the
15-key `FAMILIES` dict at 674-690; `FAMILY_IDS` (14 ids, `proposal-origin`
absent); `conftest.py:66` `make_ctx(..., agg_root=None, ...)`;
`validate-credential-contracts.py:108` adjudicating negatives against
`_semantic_findings` only; the credential schema's single
`additionalProperties` at :98 and its absence from `contracts/manifest.yaml`;
consent schema `:194`, `:209`, `:239`, `:244`, `:248`, `:253-255`, `:256-259`,
`contract_schema_version` at `:9` / class-registry `:7`; consent validator
`:129-130`, `:133`, `:149-155`, `:167-182`, `:348`, `:494-505`, `:687`, `:699`;
`test_suite.py:15-19`; 15 conformance-gate tests and the "Locks the three
checks" docstring; 23 doc-health test modules; README `:264-272`, `:488`,
`:226`; `docs/contract-versioning-policy.md:130-132`; v1.30 and v1.31 digest
inventories at 190 entries each; `openspec validate --all --strict` = 58/58.
All of these claims in plan.md and research.md are ACCURATE as written.

## Findings

### F-001 — HIGH — the whole-repo kind sweep collides with this feature's own doc-health fixture corpus

*Artifacts*: plan.md:362-368 (Cluster B, pass 1); plan.md:892-894 (decision 12);
research.md:790-795 (Decision 7 corollary); tasks.md:286-299 (task 2.9).

The sweep excludes `.git`, `node_modules`, `__pycache__`, `.venv`, and — when
the target IS this checkout — `examples/client-identity-roster/` only. But
task 6.5 creates REAL on-disk roster fragments at
`tests/doc-health/fixtures/client-identity-composition/<repo>/credentials/client-identity-roster/*.yaml`.
Those paths are not the openxFactory checkout's own
`credentials/client-identity-roster/`, so every one of them is reported as
`misplaced-roster-instance` the moment the validator is pointed at this
checkout — which is exactly task 2.9's own verification ("running the validator
against this checkout must NOT report its own packaged corpus as misplaced")
and is implied by task 6.7 living in the same tree. The tree already carries
the governing principle and enforces it for the sibling scanner:
`tests/doc-health/test_suite.py:23-27` asserts "fixture corpora must never
enter a real scan".

This is an EXTENSION of an accommodation already ruled and already recorded
(plan decision 12 carves out `examples/client-identity-roster/` for the same
self-scan reason), not a narrowing of FR-036 or ruling R1: both govern the
sweep over a TARGET DOMAIN repo, where no such fixture tree exists.

*Fix applied*: the self-scan exclusion is stated as the feature's own fixture
corpora — `examples/client-identity-roster/` AND `tests/` — in plan.md Cluster
B, plan decision 12, research.md Decision 7, and tasks.md 2.9, each naming the
`test_suite.py` precedent.

### F-002 — MEDIUM — "task 3.1/3.2/3.3/3.4" is ambiguous: OpenSpec packet ids collide with this feature's Speckit ids

*Artifacts*: spec.md:22-28 (governing-change block); spec.md:100-119
(Clarifications, R2/R4 bullets carry the same numbers by reference);
plan.md:76 (ratified-constraint row 4).

The archive-blocker list cites "task 3.2" (consent cascade), "task 3.4"
(doc-health family), "task 3.1" (pack), "task 3.3" (neutral refusal fixture) —
the GOVERNING CHANGE's task numbers. In tasks.md, 3.1-3.6 are the packaged
example tasks (README, BC worked case, multi-surface reader, `planned` entry,
the ledgerx fragment, the drift example). A reader holding both files reads the
archive blockers as example authoring.

*Fix applied*: every such citation qualified as "OpenSpec task N", with one
explicit note in spec.md that these are the governing change's numbers and do
not correspond to this feature's Speckit task ids.

### F-003 — MEDIUM — token-form drift: `residency_model` and `enforcement_mode` members spelled hyphenated at the declaration sites

*Artifacts*: spec.md:810-812 (FR-034); plan.md:252, plan.md:255-256,
plan.md:265-267 (Cluster A field table and `admission[]` members).

tasks.md 1.2 fixes the members as `client_tenant_single` / `vendor_tenant_multi`
and `provider_enforced` / `logic_enforced` (snake_case, the tree's member
dialect and the form every other member in this feature uses:
`business_central`, `entra_app_registration`, `roster_drift_clear_required`).
spec.md FR-034 and plan.md's Cluster A table spell them
`client-tenant-single` / `vendor-tenant-multi` and `provider-enforced` /
`logic-enforced` at the ENUMERATION sites — the sites a builder copies from.
spec.md is already internally split: constraint 1, FR-012 and US1 scenario 7
all use `vendor_tenant_multi`.

Per the analyze charter the tasks' snake_case choice is the normalization
target. The ratified delta's prose ("A client-tenant-single model … A
vendor-tenant-multi model") is English prose naming models, not a token
declaration, so normalizing the token form contradicts no ratified text.

*Fix applied*: declaration sites normalized to snake_case in spec.md FR-034 and
plan.md Cluster A, each recording that the ratified delta's hyphenated prose
names the same two models and that prose elsewhere in these documents keeps the
English hyphenated forms deliberately.

### F-004 — MEDIUM — "six vocabulary negatives in 4.2" is false; 4.2 carries five

*Artifacts*: tasks.md:114 (task 1.2 verification); tasks.md:232 (task 2.3
verification); against tasks.md:415-423 (task 4.2's file list).

Six closed vocabularies are declared (FR-034: `admission_surface`, authority
class, `residency_model`, `enforcement_mode`, `lifecycle_state`,
`identity_kind`), but 4.2 lists FIVE vocabulary negatives — the authority-class
refusal is `destructive-authority-class.yaml`, which sits in 4.1 because
FR-016 names it. plan.md gets this right ("SC-014's four remaining
closed-vocabulary refusals", i.e. the four beyond FR-016's two named ones);
only the two task verification lines miscount.

*Fix applied*: both verification lines corrected to "the five vocabulary
negatives in 4.2 plus `destructive-authority-class.yaml` in 4.1 — one per
closed set, six in total (SC-014)".

### F-005 — MEDIUM — plan.md lists a MODIFIED file no task touches and no evidence requires

*Artifacts*: plan.md:190 (`tests/doc-health/test_suite.py  # determinism
assertion`) against research.md:641-644 and tasks.md 6.6.

research.md Decision 6 establishes that `test_suite.py`'s determinism test is
family-specific (`tag-hygiene`) and that "the new family needs its own
equivalent assertion", which tasks.md places in 6.6
(`test_client_identity_composition.py`). Verified: `test_suite.py` references
`FAMILIES` only for `tag-hygiene` (:16-17) and `staged-candidate-aging` (:70) —
it carries no all-families iteration and no `FAMILY_IDS` assertion, so
registering a sixteenth family requires no edit to it. The plan's MODIFIED list
therefore over-declares the blast radius of a change to a MODIFIED capability's
existing suite — the one thing FR-030 forbids touching.

*Fix applied*: the entry moved out of MODIFIED and recorded under NOT EDITED
with the measured reason.

### F-006 — MEDIUM — an invented legend rule with no requirement behind it and no negative fixture

*Artifacts*: plan.md:238-242 (Cluster A legend paragraph); tasks.md:281-283
(task 2.8) against FR-034 (spec.md:822-827) and the 27-file negative list
(plan.md:142-169, tasks.md 4.1-4.4).

FR-034 names exactly two legend findings: a token used with no legend entry,
and a token declared twice. plan.md and tasks.md add a third — "a legend entry
never used" — which (a) is not required by any FR, (b) can fire on a conformant
fragment (a legend documenting a unit whose entry is `retired`, or the
enrollment axis's `planned` case), cutting against ratified answer 3 and
SC-013's "absence is never a finding", and (c) has NO negative fixture: the
corpus carries `legend-token-missing.yaml` and `legend-token-declared-twice.yaml`
and nothing else, so it breaches FR-016's "one negative confirmation per rule".
plan.md compounds it by claiming "both checked in the validator, both with
their own negatives", which its own file list contradicts.

Fixing by ADDING a 28th fixture would ratify an invented rule and cascade
through every count in the plan and tasks; fixing by DROPPING it restores
exactly FR-034's two findings and their two negatives.

*Fix applied*: the unused-legend-entry rule dropped from plan.md Cluster A and
tasks.md 1.4/2.8, with an explicit statement that an unused legend entry is not
a finding in this release and why.

### F-007 — MEDIUM — research.md Decision 3 still carries its pre-A-3a wording

*Artifact*: research.md:358-360 ("an OBJECT whose PROPERTY NAMES are the closed
vocabulary and whose values are **booleans**").

Ruling A-3a narrows the values to `const: true`, and the same section says so
three paragraphs later (research.md:386-394), as do plan.md Cluster H and
tasks.md 7.1. The lead-in sentence is the pre-gate text and now contradicts the
ruling it introduces — an implementer reading top-down writes `type: boolean`.

*Fix applied*: lead-in restated as `const: true` values, naming ruling A-3a at
the point of first statement.

### F-008 — MEDIUM — A-N4's test has no named home

*Artifacts*: plan.md:817-818 ("This is a test in
`tests/doc-health/test_client_identity_composition.py` or its roster sibling");
tasks.md:583-584 (task 6.7 *Files*, same disjunction).

An unnamed file path in a task's *Files* line is exactly the ambiguity residue
the analyze pass exists to remove: two implementers land the same assertion in
two modules, or neither writes it. The fixture repos the test reads live under
`tests/doc-health/fixtures/client-identity-composition/`, so the doc-health
module is the home that keeps the test beside its data.

*Fix applied*: pinned to `tests/doc-health/test_client_identity_composition.py`
in both artifacts, with the rejected alternative recorded rather than left open.

### F-009 — MEDIUM — four coverage-table rows understate their real task mapping

*Artifact*: tasks.md:842-896 (Requirement → task coverage).

Spot-verified row by row against the task bodies. Four rows are materially
incomplete — each omits the task that actually homes half the requirement:

- **FR-011** → `2.9, 4.5 (fixture 4)`. FR-011 has TWO findings; the second
  ("a missing enforcement test") is schema-borne at 1.7 and confirmed by
  `missing-enforcement-test.yaml` at 4.1, neither of which is listed.
- **FR-015** → `2.1`. FR-015 requires the validator to "enforce every
  intra-repo rule above"; those are 2.3-2.10.
- **FR-037** → `1.6, 2.9, 8.3`. The `evidence_ref` SHAPE refusal is confirmed
  by `evidence-ref-malformed.yaml`, authored at 4.2.
- **FR-038** → `2.4, 4.6`. FR-038's fixture obligation is explicitly
  "threefold and inseparable": the genuine pairs (3.5) and the alias-pair
  negative (4.1) are both unlisted.

Three further rows are thin rather than wrong (FR-022 omits 5.2, FR-039 omits
8.5, SC-008 omits 7.1).

*Fix applied*: all seven rows corrected.

### F-010 — MEDIUM — task 0.3 parks an uncommitted baseline inside the exact path the feature commits wholesale

*Artifact*: tasks.md:80-81 ("the captured output is stored in the feature
directory as a scratch note (not committed)").

Every commit in this lane stages `specs/007-client-identity-roster` as a
pathspec (the shared-checkout discipline this repo family mandates), so a file
written into that directory is committed by the next commit whether or not the
task says "not committed" — and FR-030's before-state would land in the
governance tree as an untracked-turned-tracked artifact.

*Fix applied*: 0.3 now writes the baseline outside the tracked tree (the
session scratchpad), with the path recorded in the task so 8.6 and 10.4 can
find it.

### F-011 — LOW/MEDIUM — Phase 2's verifications consume Phase 3/4 artifacts while the phase header claims Phase 1 is its only dependency

*Artifacts*: tasks.md:205 (Phase 2 header), tasks.md:221-229 (task 2.2),
tasks.md:143-145 (task 1.5 verification).

2.2 authors the self-test layer whose corpus does not exist until Phases 3-4;
1.5's field-list assertion lives in a test module created at 4.5. Neither is a
true cycle — code precedes fixtures, verification follows both — but the
tasks state the dependency in only one direction (Phase 3 "Blocks … 2.2's
self-test corpus") and the Phase 2 header contradicts it.

*Fix applied*: a "verification timing" rule added to the Format section (a
task's *Verification* may be discharged after a later phase where it names that
phase's artifacts, and the task is not `[x]` until it is), plus a pointer in
the Phase 2 header and in 2.2 and 1.5.

### F-012 — LOW — the "30 negative confirmations" total omits a repo-shaped negative

*Artifact*: plan.md:470-472 ("27 packaged + 2 repo-shaped + 1 doc-health =
**30**").

The "2 repo-shaped" is the count of FR-016 RULES with no packaged home (rule 5,
the unresolvable gate obligation; rule 15, misplacement). The repo corpus
carries a THIRD refusing fixture — repo fixture 2, the nonconformant `mutate`
repo, which the coverage table itself cites for rule 9. As a count of probes
the number is 31; as a count of rule-homes it is 30.

*Fix applied*: the sentence now states both counts and what each measures.

### F-013 — LOW — Phase 7 declares no dependency while 7.1 names an artifact fixed in Phase 1

*Artifact*: tasks.md:592 ("**Depends on**: nothing in this feature").

7.1's `roster_drift_clear_required` description names
`xfactory_client_identity_drift_finding`, the kind string fixed at task 1.9. It
is a textual dependency, not a build one — but "nothing" is the wrong word for
it and would let 7.1 mint a divergent spelling if run first.

*Fix applied*: header amended to "no build dependency; 7.1's member description
cites the drift kind NAME fixed at 1.9 (textual)".

### F-014 — LOW — three tasks require checkouts no Phase 0 task establishes

*Artifacts*: tasks.md:628-637 (7.4, an OpsxFactory checkout), tasks.md:797-804
(10.3, an aggregation checkout), tasks.md:825-832 (10.6, `git status` over the
aggregation checkout).

Phase 0 baselines only in-repo suites. The feature's decisive regression (7.4,
"the one result that would falsify the additivity claim") and two of its green
bar measurements need trees outside this clone, and nothing establishes their
reachability before the work that depends on them is done.

*Fix applied*: 0.3 extended to confirm reachability of the aggregation
checkout and the OpsxFactory checkout, with a STOP-and-escalate on absence
(those measurements cannot be synthesized and must not be quietly skipped).

### F-015 — LOW — research.md cites a README that does not exist

*Artifact*: research.md:929-931 ("the shape of `examples/consent-instrument/`
and `examples/credential-contracts/`").

Verified: `examples/credential-contracts/` holds two positives and a
`negative/` directory and NO `README.md`. The convention claim stands on
`examples/consent-instrument/` alone (which does carry one, `Status: draft`),
plus the 006 header precedent the same paragraph already cites.

*Fix applied*: the citation corrected and the measured asymmetry recorded.

## Verdicts on the nine tasks-phase decisions

| # | Decision | Verdict |
|---|---|---|
| 1 | Phase reorder (Cluster D as Phase 3, Cluster C as Phase 4) | UPHELD. Cluster C's killed-flaw positives live inside Cluster D's two fragments, so C-before-D would assert against files that do not exist. The residual — Phase 2's verifications depending on 3/4 — is F-011, fixed as a stated rule, not by re-ordering. |
| 2 | The 0.3 baseline task | UPHELD in substance (FR-030's "unmodified in behaviour" is unmeasurable without a before-state), FIXED in placement (F-010) and extended to the external checkouts 7.4/10.3/10.6 need (F-014). |
| 3 | A-N2 residual carried as task 5.3 | UPHELD. Ruling A-N2 asks for plan.md; 5.3 additionally echoes it into `traceability.yaml`'s FR-022/SC-006 rows, which is where the follow-up's author looks. No over-claim: 5.3's own verification bounds the claim to SC-006. |
| 4 | Traceability rows covering SCs as well as FRs | UPHELD. `red_proven` genuinely needs runs, so deferring the file to 10.1 is right; covering SC-001…SC-014 is what makes SC-008's and SC-006's fixture-only proofs auditable. |
| 5 | A-N4 test location | FIXED (F-008): "or its roster sibling" pinned to `tests/doc-health/test_client_identity_composition.py`. |
| 6 | The 2.3-2.10 validator-rule split | UPHELD. Every intra-repo FR maps into exactly one task (2.3 vocabularies, 2.4 uniqueness+alias, 2.5 admission, 2.6 authority, 2.7 residency+lifecycle, 2.8 roots+legend, 2.9 repo context, 2.10 absence) with no rule in two places and none unhomed — after F-006 removes the one rule that had no requirement behind it and F-001 fixes 2.9's sweep. |
| 7 | The second credential-contracts negative in 7.3 (false-valued member) | UPHELD, and structurally required: `validate-credential-contracts.py:108` adjudicates negatives against `_semantic_findings` ONLY (verified), so a `const: true` narrowing with no semantic branch would have no registrable probe at all. |
| 8 | The 4.1/4.2 fixture split | UPHELD on the numbers, verified independently: FR-016 names 16 rules; 12 named + 4 unnamed = 4.1's sixteen files; the thirteenth packaged named rule (out-of-vocabulary admission surface) sits with its vocabulary siblings in 4.2; 4.1+4.2+4.3+4.4 = 16+8+2+1 = 27 = the plan's packaged list exactly. The only defect was the miscounted verification lines (F-004). |
| 9 | snake_case member spellings | UPHELD as the normalization target; spec.md FR-034 and plan.md Cluster A normalized to it (F-003). |

## Escalations

None. No finding required changing a ruling, a ratified constraint, Brett's
Decisions A or B, or any packet text. Every fix lands in the four Speckit
artifacts.
