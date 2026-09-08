# Checklist: Archive Integrity and Pinned-Target Requirement Quality

**State**: written 2026-09-08, NOT YET RUN — this file is the gate instrument for the architect's refutation panel. The findings its authoring raised were resolved in the analyze loop and are recorded in [`../analysis.md`](../analysis.md).

**Purpose**: "Unit tests for English" over the requirements governing
immutability of `openspec/changes/archive/` and the pinned-target
re-derivation obligation this feature measures against but does not trigger.
Every item interrogates whether the WRITTEN requirements are complete, clear,
consistent, measurable, and cover the bookkeeping-vs-assertion and
report-then-refuse mechanics the two ratified requirements define — never
whether the archive tree was in fact left untouched (that is the gate report's
job).
**Created**: 2026-09-08
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Reviewer / release governance

## Requirement Completeness

- [x] CHK001 Does FR-009 ("no file under `openspec/changes/archive/` may be edited by this feature") state its verification method (a path-prefix check over the branch diff) precisely enough to catch a RENAME or a symlink INTO the archive tree, and not only a byte-content edit of an existing archived path? [Completeness, Spec FR-009, SC-007]
- [x] CHK002 Is the frozen-file set plan.md's Project Structure names ("design.md, .openspec.yaml, specs/document-lifecycle/spec.md, everything under openspec/changes/archive/, tests/sequenced_after/corpus-ledger.yaml, README.md, contracts/**") the SAME set FR-009, FR-010 and SC-007 individually enumerate, or does each artifact state a different subset such that a reader consulting only one would miss a frozen path the others name? [Consistency, Completeness, Plan Project Structure, Spec FR-009, FR-010, SC-007]
- [x] CHK003 Does the spec state, for the bookkeeping-vs-assertion test the ratified ADDED requirement defines by EFFECT ("THE TEST IS WHETHER THE EDIT CHANGES WHAT THE ARCHIVED RECORD ASSERTS"), whether this feature's own edits to the ACTIVE packet's `tasks.md` and `proposal.md` — neither of which is under `openspec/changes/archive/` because the packet has not yet archived — are stated to fall OUTSIDE that requirement's reach entirely, rather than merely happening to pass its bookkeeping test? [Completeness, Gap, Ratified ADDED Requirement, Spec FR-006, FR-017, FR-018]
- [x] CHK004 Given the ratified requirement explicitly lists "a task record or its tick state" as NOT bookkeeping when the edited file IS archived, is it stated anywhere that FR-017's amendment of three ratified sentences and FR-006's ticking of 20+ boxes are safe PRECISELY BECAUSE the packet has not yet archived — and that the SAME edits, performed after the archive act, would need the archived-record route instead? [Gap, Ambiguity, Spec FR-006, FR-017, Ratified ADDED Requirement]
- [x] CHK005 Is the exact scope word "IN-REPO" in FR-008 ("no IN-REPO `sha256` pin names `docs/document-lifecycle.md`") defined with the same precision the ratified requirement uses for task 1.2a's scope ("every in-repo `sha256` pointer to an in-repo target"), or could a reader take "in-repo" to mean "anywhere under this git tree including vendored or example content" rather than "a live pin, as opposed to the illustrative fixtures under `examples/document-cataloging/`" that research.md M2 separately excludes? [Completeness, Ambiguity, Spec FR-008, Research M2]
- [x] CHK006 Is the pinned-target measurement's method — a grep across `*.yaml|*.yml|*.json` for `sha256` co-occurring with the path, PLUS a parse of `contracts/manifest.yaml` for zero `docs/`-prefixed values — stated precisely enough to be re-run by a reader who has only FR-008, or does FR-008 state only the CONCLUSION and leave the METHOD to research.md, which spec.md's own framing treats as non-authoritative supporting material? [Measurability, Completeness, Spec FR-008, Research M2]
- [x] CHK007 Is the report-then-refuse transition the ratified requirement describes ("A family that declares no re-derivation rule has not earned a pin... It becomes a REFUSAL for that family on the day that family declares") named anywhere in this feature's own artifacts as a fact ABOUT this feature — that no family anywhere in the estate has declared a rule yet, per the ratified requirement's own "measured at this packet's authoring" note — or is that state assumed to still hold at THIS feature's base without a fresh measurement? [Completeness, Gap, Ratified ADDED Requirement]

## Requirement Clarity

- [x] CHK008 Is "edited by this feature" (FR-009) defined precisely enough to cover a file the feature READS and derives a measurement from without changing it (e.g., `tests/sequenced_after/corpus-ledger.yaml`, read at T020) — is read-only reference to a frozen file clearly distinguished from edit, so T020's read of the ledger row is not itself ambiguous under FR-009's language? [Clarity, Spec FR-009, Tasks T020]
- [x] CHK009 Is a criterion given for telling a "live pin" apart from an "illustrative fixture" (research.md M2's characterization of `examples/document-cataloging/*.yaml`) other than the path sitting under `examples/` — e.g., a schema marker, a `Kind:` header, or an explicit statement that `examples/` content is never a consumed pin — so the distinction is checkable rather than asserted? [Ambiguity, Research M2, Gap]
- [x] CHK010 Is "no dependent pin exists" (the consequence of M2's negative result) clearly distinguished from "a family has declared no re-derivation rule" (the ratified requirement's REPORT-not-refuse condition) — given the two are different facts, one about whether a pin exists at all and the other about whether an EXISTING pin's family has a rule, that this feature's evidence could conflate if it states only the M2 result? [Clarity, Ambiguity, Ratified ADDED Requirement, Spec FR-008]

## Requirement Consistency

- [x] CHK011 Is T003's cross-reference — "This is a standing constraint re-checked at T028, not a one-time act" — internally consistent with tasks.md's own numbering, given T028 is the `proposal.md` additive-note task (FR-010) and NOT a verification task, while T030 ("Verify SC-007: `git diff main...HEAD --name-only`...") is the task that actually re-checks the frozen set and the no-archive-edit claim? [Conflict, Tasks T003, T028, T030]
- [x] CHK012 Is the "measured at base `68712924`" wording (FR-008, and repeated at T012 and T025) reconciled with the fact that T012 runs in Phase 4, AFTER Phase 3's T005–T010 have already committed the § 3.4 doc edit and advanced HEAD past `68712924` — does the spec make clear that "base" names the branch's cut-point rather than the commit HEAD was at when the measurement command actually ran, so a reader does not conclude the measurement is stale the moment any commit lands? [Consistency, Clarity, Spec FR-008, Tasks T012, T025]
- [x] CHK013 Is there a conflict between plan.md's Constitution Check row VI ("measured — no in-repo `sha256` pin names ANY FILE THIS FEATURE EDITS") and FR-008's narrower claim about ONE file (`docs/document-lifecycle.md`) alone — is the broader Constitution Check claim separately measured for `tasks.md`, `proposal.md` and the new `evidence/realization-2026-09-08.md` file, or does it rest entirely on the single M2 measurement of the doc file? [Conflict, Completeness, Plan Constitution Check, Spec FR-008]
- [x] CHK014 Is there a conflict between FR-016 ("this feature MUST... repair no broken pin") and the ratified requirement's "an edit that cannot re-derive its dependents may not land" — if a pin WERE later found broken by this edit, would FR-016's blanket "repair no broken pin" and the requirement's landing refusal pull in opposite directions (one forbidding the fix, the other forbidding landing without it), and is that tension resolved anywhere given M2's negative result is assumed to make it moot? [Conflict, Spec FR-016, Ratified ADDED Requirement]

## Measurability / Acceptance Criteria Quality

- [x] CHK015 Is SC-007's diff-path check ("`git diff main...HEAD --stat` shows changes ONLY under [5 paths]... and nothing under any `archive/` path") measurable as a SINGLE reproducible command, or does verifying "nothing under any `archive/` path" require a second command beyond the `--stat` diff that SC-007 does not separately name? [Measurability, Spec SC-007]
- [x] CHK016 Is "no pin names this file" stated together with the git ref or commit it was measured AT, everywhere the claim appears (T012's evidence entry, T025's `tasks.md` note, and any restatement at T029's final-head re-run), so a reader of any ONE of the three copies gets the same head rather than three copies that could silently diverge if only one is updated on a later re-run? [Consistency, Measurability, Tasks T012, T025, T029]
- [x] CHK017 Is the claim in spec.md's Measured baseline — "the ratification merge `3504287a` (PR #788) IS an ancestor of [base] `68712924`, measured with `git merge-base --is-ancestor`" — paired with a re-run instruction at the FINAL head (T029), so the ancestry claim does not silently go stale across the four subsequent commits this feature makes, the same way the pin claim is required to? [Measurability, Consistency, Spec Measured baseline, Tasks T029]

## Scenario Coverage (Primary / Alternate / Exception / Recovery / Non-Functional)

- [x] CHK018 Primary: Are requirements defined for the primary path — a reader of the evidence file alone reproducing BOTH the pinned-target measurement's negative result and the "no file under `archive/` is edited" claim by re-running the named commands at the recorded head, with the commands themselves (not just their conclusions) present in the evidence file per FR-013? [Coverage, Primary Flow, Spec FR-008, FR-013]
- [x] CHK019 Alternate: Are requirements defined for the alternate path where the archive act's own re-derivation check — performed by the LANE, not this feature — finds this feature's M2 measurement's base (`68712924`) has since been superseded by a later HEAD carrying a NEW pin, with that handoff named as the lane's own obligation (FR-015, Out of scope § 6) rather than left implicit? [Coverage, Alternate Flow, Spec FR-015, Out of scope]
- [x] CHK020 Exception: Do the requirements state what MUST happen if the pinned-target measurement, when re-run, comes back POSITIVE — a pin is found naming `docs/document-lifecycle.md` — given the ratified requirement's own "A pinned target's bytes change" scenario would then demand re-deriving every dependent pin IN THE SAME CHANGE, and this feature's task list contains no task encoding that contingency? [Coverage, Exception Flow, Gap, Ratified ADDED Requirement]
- [x] CHK021 Exception: Are requirements defined for the case where a dependent pin IS found and CANNOT be re-derived — the ratified requirement's "A dependent pin cannot be re-derived" scenario mandates a refusal naming the pin — or does this feature's design implicitly assume the negative M2 result makes this scenario permanently moot for this branch without saying so? [Coverage, Exception Flow, Ratified ADDED Requirement, Gap]
- [x] CHK022 Recovery: Are requirements defined for the recovery path when T002's re-measurement of M1 at the current head is NOT empty (the packet or promoted canon moved) — T002 says "STOP and report," but is there a requirement for what becomes of Phase 3/4/5's partially-committed work, or does "STOP and report" leave the branch's disposition unstated? [Coverage, Recovery, Tasks T002]
- [x] CHK023 Non-Functional: Is the requirement that gate evidence be reproducible (FR-011, "recorded verbatim") paired with a rule for WHICH head each recorded result is stamped against, given T029's final-head re-run is expected to supersede some but re-affirm other Phase-4 measurements, and the evidence file's own structure (per FR-013's header) is the only place that distinction could live? [Non-Functional, Measurability, Spec FR-011, FR-013, Tasks T029]

## Edge Case Coverage

- [x] CHK024 Is the edge case of `contracts/manifest.yaml` itself changing between the base measurement and the final head addressed — since `contracts/**` is in the frozen set (plan.md Project Structure), is it explicit that this specific input to the M2 measurement is guaranteed stable for the life of this branch, or do the freeze claim and T029's re-run requirement sit in unstated tension over whether re-parsing it is even necessary? [Edge Case, Consistency, Plan Project Structure, Research M2]
- [x] CHK025 Is the case where ANOTHER lane's concurrent change adds a NEW in-repo pin naming `docs/document-lifecycle.md` while this branch is open addressed — spec.md's own Edge Cases section names "another lane lands a substrate change first" for the README/ledger rows but not for a new pin appearing against the § 3.4 edit target? [Edge Case, Gap, Spec Edge Cases]
- [x] CHK026 Is a NOT-OWED-HERE note (FR-007) that names an `openspec/changes/archive/...` path inside the ACTIVE packet's own `tasks.md` clearly distinguished from an EDIT of that archived path itself — i.e., is it stated that adding a dated note ABOUT an archived location, inside a live file, is not the kind of act FR-009 forbids? [Ambiguity, Spec FR-007, FR-009]

## Dependencies & Assumptions

- [x] CHK027 Is it stated as an explicit assumption that `contracts/manifest.yaml`'s ZERO `docs/`-prefixed path values (M2) is parsed rather than grepped specifically BECAUSE a grep could miss a YAML anchor/alias or a differently-quoted path string, or is that assumption about grep's insufficiency left implicit in the choice of tool rather than named as a reason? [Assumption, Research M2]
- [x] CHK028 Is the assumption that `examples/document-cataloging/` is the COMPLETE set of non-live-pin occurrences (research.md M2: "the only occurrences... are illustrative fixtures") re-verified at the measurement's actual run time rather than carried forward from research.md's earlier read, consistent with the re-measurement discipline M1 states for itself? [Assumption, Consistency, Research M1, M2]
- [x] CHK029 Is it stated as an assumption that OpsxFactory's own `govern-archived-record-edits` domain twin (PR #279, cited in FR-007 as the landing vehicle) carries no in-repo pin of its own naming `docs/document-lifecycle.md` from OpsxFactory's side — or is the "IN-REPO" scope of FR-008 explicitly bounded to THIS repository alone, making a cross-repository pin structurally out of this measurement's reach regardless of what OpsxFactory holds? [Completeness, Assumption, Spec FR-008, FR-007]

## Notes

- **CHK011 is a verifiable defect, not a stylistic quibble**: `tasks.md`'s
  T003 explicitly names "T028" as the task that re-checks the frozen-set /
  no-archive-edit standing constraint, but T028 in the current `tasks.md` is
  the `proposal.md` additive-note task; the actual re-check is T030
  (SC-007 verification). If T003's cross-reference is trusted as written
  rather than cross-checked against the task list, the standing re-check
  this feature depends on could read as scheduled when the numbering
  actually points at unrelated work.
- **CHK003/CHK004 form the other load-bearing family**: the ratified ADDED
  requirement's bookkeeping-vs-assertion test is written for files UNDER
  `openspec/changes/archive/`. This feature ticks boxes and rewords sentences
  in the SAME packet's `tasks.md`, which is not yet archived — the individual
  FRs (006, 017, 018) are each defensible on their own terms, but none of them
  states outright that the archived-record rule does not YET reach this file,
  or that it will once § 6 (the archive act) runs.
## Evaluation — 2026-09-08 (round 3 re-evaluation)

**Round 3**: FR-009a (frozen set enumerated once), FR-008a (measurement names
its method, re-taken at T029), FR-008b (pointers vs obligations kept apart;
fixture criterion stated), FR-008c + T012b (contingency for a positive or
unresolvable pin finding), FR-013b, the reconciled FR-016, and plan.md's
narrowed Constitution Check VI were read against every item left open in round
2. This tally replaces the round-2 tally rather than appending to it.

**Tally**: 27 passed / 2 open / 0 dispositioned (total 29).

### Open items
- CHK004 — FR-022 (unchanged this round) still does not state that the SAME edits — ticking boxes, amending sentences — performed AFTER the archive act would instead need the archived-record bookkeeping route this packet itself defines; none of round 3's new FRs (FR-008a/b/c, FR-009a, FR-013b, FR-016, FR-032, FR-007b) touch this. → Add one sentence to FR-022 stating that identical edits to tasks.md/proposal.md made after archive would require the recorded-ruling-plus-bookkeeping-note route this packet itself defines.
- CHK019 — T029 now re-takes the pinned-target measurement and the ancestry check at this feature's OWN final head, and FR-008c stops the branch on a positive/unresolvable finding — closing the risk window up to STOP (B). What remains unnamed is the narrower gap AFTER this feature stops and BEFORE the archive act runs: Out of scope § 6 still says only "The archive act (§ 6)... — the lane's," without naming the pin re-check as part of that handoff. → Add one clause to Out of scope § 6 (or FR-015) naming the archive-time pinned-target re-check as the lane's obligation, the way FR-012 already hands off the MODIFIED-block currency re-check.

### Deferred items
- None — every item in this checklist interrogates the WRITTEN requirements' quality, never an execution result, so no item qualifies for deferral.

## Final closure — 2026-09-08 (orchestrator, after the amendment round)

Every item this file left OPEN after round 3 was closed by the amendments the
requirements now carry (FR-033..FR-040 and the targeted edits to FR-005b,
FR-008b, FR-012, FR-025, FR-028, SC-007, the Edge-Cases record obligation, and
tasks T010/T029/T030a/T033a). Items closed in this pass: CHK004, CHK019.

**Final tally: 29 passed / 0 dispositioned / 0 open.** A DISPOSITIONED
item is one that cannot be closed from inside this feature — it needs an act in a
frozen file, another repository's process, or a later act's own decision — and it
carries that reason inline.

