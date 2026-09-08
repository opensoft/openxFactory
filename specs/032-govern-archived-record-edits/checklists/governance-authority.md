# Checklist: Governance Authority — Govern Archived-Record Edits

**State**: written 2026-09-08, NOT YET RUN — this file is the gate instrument for the architect's refutation panel. The findings its authoring raised were resolved in the analyze loop and are recorded in [`../analysis.md`](../analysis.md).

Authority-domain requirements-quality gate for feature `032-govern-archived-record-edits`:
who may perform which act, what stands as authority for an act, and where an
agent's pen stops. Every item asks whether the WRITTEN RULE is precise enough
that a faithful implementer could not follow it to the letter and still leave
an authority question open. Audience: the release-gate reviewer and Brett Heap,
who holds the three named veto points. No-argument invocation — maximum
coverage, no item cap.

## Authority & Actor Boundaries

- [ ] CHK001 Is the boundary between what an AGENT may do (author prose, tick act-done boxes, run gates) and what only Brett Heap (the OPERATOR) may do stated as an explicit rule, or must it be inferred by cross-reading FR-006, FR-015 and Architect rulings? [Clarity, Spec FR-006/FR-015]
- [ ] CHK002 Is the boundary between this feature's acts and "the lane's" acts (claim, open the PR, post LANDING/LANDED, discharge issue #630, archive) enumerated completely, or could "claim" and "post LANDING/LANDED" fall outside FR-015's prohibition list, leaving silence readable as permission? [Completeness, Spec Assumptions/FR-015]
- [ ] CHK003 Is it stated as plainly in requirement text as in Clarifications narrative that an AGENT (not Brett Heap) authors the § 1 `[OPERATOR]` box ticks — given the rejected option was "leave the `[OPERATOR]` boxes for Brett Heap to tick himself"? [Clarity, Spec FR-006/Clarifications Q1]
- [ ] CHK004 Is the domain-twin actor (OpsxFactory, "a sibling orchestrator", PR #279) distinguished precisely enough from this feature's actor that a reader cannot mistake a twin box for one this feature may tick? [Clarity, Spec FR-007/Out of scope]
- [ ] CHK005 Is lane identity (`opsXfactory-1`) itself a checked precondition anywhere for continuing this feature, or only asserted through the trailer requirement (FR-014) with no gate on WHO may resume the work? [Gap, Spec FR-014]

## Ratified Packet as Sole Authority

- [ ] CHK006 Does "THE RATIFIED PACKET IS THE AUTHORITY, NOT THIS FILE" carry an operational consequence stated as a requirement an implementer is directed to follow on conflict, or is it asserted once in prose with no corresponding FR? [Gap, Spec Preamble]
- [ ] CHK007 Is the ratification record — GitHub review `5141756427`, APPROVED `2026-09-08T12:38:36Z`, PR #788, merge `3504287a` — cited identically everywhere it recurs (header, FR-006, research M1), or does any one citation drop a field the others carry? [Consistency, Spec Header/FR-006/Research M1]
- [ ] CHK008 Is the ratified packet's scope ("1 MODIFIED and two ADDED requirements, 18 scenarios") precise enough for an implementer to verify this feature's requirements do not exceed it, or must the count be taken on faith with no pointer to the promoted spec file? [Traceability, Spec Key Entities]
- [ ] CHK009 Is there a named escalation or correction procedure for the case where a requirement in this spec appears to WIDEN or NARROW a ratified block, or only the bare statement that the file would then be "the defect"? [Gap, Spec Preamble]

## Operator-Box Ticking Discipline

- [ ] CHK010 Is "ACT-DONE, not actor-class" (FR-006) defined as a general, mechanically applicable procedure, or does it rely entirely on analogy to the two cited precedents with no rule extracted from them for a box neither precedent resembles? [Ambiguity, Spec FR-006]
- [ ] CHK011 Is it specified what evidence is sufficient to call EACH of boxes 1.1–1.5 "verifiably DONE" individually, or does FR-006 give one evidentiary standard for all five without addressing whether each needs distinct evidence? [Clarity, Spec FR-006/Tasks T021]
- [ ] CHK012 Is there a requirement preventing an agent from ticking an `[OPERATOR]` box whose underlying act has NO independent record (unlike review `5141756427`), so the act-done test cannot be satisfied by the agent's own assertion alone? [Completeness, Spec FR-006]
- [ ] CHK013 Does the spec state whether the act-done test is durable beyond this feature's own 28 boxes — for a FUTURE `[OPERATOR]` box lacking a precedent as clean as the two cited, is the rule still applicable, or scoped narrowly to this feature? [Gap, Spec FR-006]

## Non-Fabrication of Ratification Quotes

- [ ] CHK014 Is "the approval body is EMPTY and no verbatim word exists... MUST NOT quote a word" (FR-006) paired with an explicit prohibition on quotation marks around a near-verbatim PARAPHRASE, closing the gap a literal reading of "quote" might leave open? [Precision, Spec FR-006]
- [ ] CHK015 Is the citation triple required for a § 1 note — review id, timestamp, record path — stated as a MINIMUM (all three required) or a menu (any one suffices), and is that reading unambiguous from FR-006's wording alone? [Ambiguity, Spec FR-006]
- [ ] CHK016 Is a bright-line test given for whether a drafted phrase "counts as quoting a word" from the empty approval body, or only the negative instruction "MUST NOT quote" with no test for the boundary case? [Ambiguity, Spec FR-006]
- [ ] CHK017 Does the spec state the CONSEQUENCE of a note that does invent a quotation — a blocking defect, a gate failure, or reliance on reviewer vigilance alone — or is that left unstated? [Gap, Spec FR-006]

## Amendment-of-Ratified-Text Discipline

- [ ] CHK018 Are the THREE sentences FR-017 targets identified precisely enough (exact wording and location: preamble, § 0.1, § 1) that an implementer could not mistake a fourth similar sentence for one of the three, or amend a wrong one? [Precision, Spec FR-017]
- [ ] CHK019 Is "each amendment NAMING the superseded sentence and the reason" (FR-017) specified with a required FORM the way FR-001's note is byte-exact, or is the amendment's own wording left free-form, risking three inconsistently shaped amendments? [Clarity, Spec FR-017]
- [ ] CHK020 Is precedent commit `3b530009` accompanied by enough excerpted text in this spec that an implementer without shell access could reproduce its shape, or does satisfying FR-017 require looking up an external commit with nothing quoted here? [Gap, Spec FR-017]
- [ ] CHK021 Is "the SAME COMMIT" in FR-017 defined precisely enough to rule out a separate fixup/amend commit as satisfying it? [Precision, Spec FR-017]
- [ ] CHK022 Is the ratification record's own "28 boxes, NONE ticked" baseline sentence (which FR-017 says MUST NOT be touched) located precisely enough that an implementer amending the three nearby "stays unticked" sentences will not touch it by accident? [Completeness, Spec FR-017]

## Frozen Set Integrity

- [ ] CHK023 Is the frozen set enumerated IDENTICALLY everywhere it appears (spec.md FR-009/FR-010/Out of scope, Plan Project Structure, Tasks T003), or does one list include an item another omits, leaving an implementer to guess which is authoritative? [Consistency, Spec FR-010/Plan Project Structure/Tasks T003]
- [ ] CHK024 Is "no ratified requirement text may be reworded" (FR-009) scoped precisely enough to be distinguished from FR-017's permitted amendment of `tasks.md` sentences, so FR-009 cannot be read as forbidding FR-017's own action? [Conflict, Spec FR-009/FR-017]
- [ ] CHK025 Is the freeze on `design.md`, `.openspec.yaml` and the spec delta stated as a CONTINUOUS constraint (re-checked at every commit, per Tasks T003's "not a one-time act") in spec.md itself, or only in tasks.md with spec.md asserting it once? [Traceability, Tasks T003]
- [ ] CHK026 Is "everything under `openspec/changes/archive/`" bounded to cover a file added to that tree AFTER branch cut (another lane's archive act landing on `main` mid-flight), or does the freeze contemplate only the archive tree as it stood at branch cut? [Edge Case, Spec FR-009]
- [ ] CHK027 Is a verification method for the frozen-set freeze named as a REQUIREMENT (not just Tasks T003/T030), so an implementer reading only the Functional Requirements would know how it is checked? [Gap, Spec FR-009/Tasks T030]

## Veto Points (Brett Heap)

- [ ] CHK028 Are all three architect rulings flagged for veto (the `proposal.md` note, ticking § 1 `[OPERATOR]` boxes, the two explanatory sentences) each traced to the exact FR(s) that would need to be UNDONE on veto, so the blast radius is knowable without re-deriving it? [Traceability, Spec Architect rulings]
- [ ] CHK029 Is the MECHANISM for exercising the veto specified (a comment, a ruling record, a named channel), or does the spec only say the rulings "proceed unless Brett Heap says otherwise" with no stated form for "otherwise"? [Gap, Spec Architect rulings]
- [ ] CHK030 Is a deadline or gating point stated by which the veto must be exercised — before the PR opens, before archive, or open indefinitely including after landing? [Ambiguity, Spec Architect rulings]
- [ ] CHK031 If Brett Heap exercises the veto on ruling 2 (ticking § 1's `[OPERATOR]` boxes) AFTER the branch already ticked them, is a rollback or correction procedure specified, or does the spec describe only the pre-veto consequence with no post-hoc path? [Recovery, Spec Architect rulings]

## Prohibited Acts (PR / Comment / Merge / Archive)

- [ ] CHK032 Does FR-015's prohibition list (`openspec archive`, open a PR, post a comment, merge) cover every lane act named in Assumptions ("claim, opens the PR, posts LANDING/LANDED, discharges the claims on issue #630, and performs the archive act"), or do "claim" and "post LANDING/LANDED" fall outside FR-015's enumerated verbs? [Completeness, Spec FR-015/Assumptions]
- [ ] CHK033 Is "post a GitHub comment" (FR-015) scoped to comments on this packet/PR, or could it be read to also forbid comments on unrelated issues — and is that ambiguity resolved? [Ambiguity, Spec FR-015]
- [ ] CHK034 Is the STOP condition ("STOP (B) → architect report") defined precisely enough — what "(B)" designates, what the report must contain — that reaching it cannot be mistaken for authorization to continue into a prohibited act? [Precision, Tasks T032/Plan Implementation sequence]
- [ ] CHK035 Is `gh` (the GitHub CLI) named explicitly as prohibited anywhere in spec.md's Functional Requirements, or does that prohibition exist only in the task-runner's operating constraints outside the spec, risking a reader of spec.md alone missing it? [Gap, Spec FR-015]

## Commit Trailer & Lane Discipline

- [ ] CHK036 Is the full required trailer set — `Lane: opsXfactory-1`, `Co-Authored-By`, the session link (FR-014) — specified with exact trailer key spellings and format, or could a differently formatted line satisfy "MUST carry... the session link" while missing T031's verification grep? [Precision, Spec FR-014/Tasks T031]
- [ ] CHK037 Is "MUST stage explicit paths" (FR-014) precise enough to distinguish a compliant multi-path `git add` from a non-compliant `git add -A`/`git add .`? [Clarity, Spec FR-014]
- [ ] CHK038 Is the verification method for FR-014 (Tasks T031's trailer grep) named as part of the requirement itself, so a reader of spec.md alone knows how conformance is checked, or does spec.md stay silent on verification? [Traceability, Spec FR-014/Tasks T031]
- [ ] CHK039 Does FR-014 or any other requirement state whether a forward-merge commit from `main` (Assumptions) must ALSO carry the three trailers, or is it exempt — and is that exemption, or the lack of one, stated anywhere? [Gap, Spec FR-014/Assumptions]

## Precision Sufficiency (residual)

- [ ] CHK040 Taking FR-006, FR-007, FR-012 and FR-017 together as the full ticking/amendment rule, could a careful implementer follow every sentence literally and still leave one of the 28 boxes without an actor-identifying note? [Gap, Spec FR-006/FR-007/FR-012/FR-017]
- [ ] CHK041 Could an implementer satisfy FR-015's letter (stop, no PR, no comment, no merge, no archive) while performing a functionally equivalent adjacent act (e.g., pushing the branch and separately instructing the lane out-of-band to open the PR)? [Ambiguity, Spec FR-015]
- [ ] CHK042 Is every authority-relevant term this feature relies on ("the lane", "the archive act", "the twin", "a sibling orchestrator") defined in spec.md's own Key Entities, or does any of them force an implementer to import meaning from the wider repository CLAUDE.md rather than from this feature's governing document? [Completeness, Spec Key Entities]
