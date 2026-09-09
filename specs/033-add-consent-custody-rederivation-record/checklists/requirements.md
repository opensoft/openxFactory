# Checklist: Requirements Quality — 033-add-consent-custody-rederivation-record

**Purpose**: Release-gate requirements-quality gate over `spec.md`'s 32 written
Functional Requirements (FR-001..FR-047, numbering has intentional per-section
gaps — verified below), 10 Success Criteria, four user stories and twelve
ruled clarifications (plus A1/A2). Every item interrogates the WRITTEN
REQUIREMENTS themselves — never whether the schema or validator code has
actually been changed (it has not: see `research.md` R8, R5). No-argument
invocation — maximum coverage, no item cap.

**Artifacts under review**: `specs/033-add-consent-custody-rederivation-record/spec.md`
(primary), cross-checked against `clarify-questions.md`, `research.md`,
`openspec/changes/add-consent-custody-rederivation-record/tasks.md` (the
ratified 46-box list) and
`openspec/changes/add-consent-custody-rederivation-record/specs/consent-instrument/spec.md`
(the ratified delta, 1 MODIFIED + 1 ADDED requirement, 22 scenarios).

**Date**: 2026-09-09. **State**: run the same day it was written.

## Requirement Completeness

- [x] CHK001 Is a requirement defined for every one of the 35 in-scope packet boxes (§2.1–2.5, §3.1–3.5 incl. 3.4b/3.4c, §4.1–4.9 incl. sub-lettered fixtures, §5.2–5.4), or only for a subset the FR blocks happen to name? [Completeness, Spec FR-001–005/010–016/020–024/030–036, OpenSpec tasks.md §2–5]
- [x] CHK002 Are the four already-performed boxes (§0.1, §1.1–1.3) covered by a stated requirement (FR-040's general "verifiably DONE" rule), rather than left with no FR at all because no FR-006..FR-009 slot exists for them? [Completeness, Spec FR-040, OpenSpec tasks.md §0–1]
- [x] CHK003 Is a requirement defined for the THREE `contracts/README.md` amendment sites (Q8), including the fifth site the cross-model review found (`README.md:2993`), or does spec.md name only the two the packet's own task 4.9/A1 would suggest? [Completeness, Spec FR-046, Clarifications Q8]
- [ ] CHK004 Does every one of FR-001 through FR-047 carry an explicit cross-reference (a box number, a Q-number, or a ruling id) a reviewer can follow to its origin, or do most FRs (FR-001–005, FR-010–016, FR-020–023, FR-030–035, FR-040–045) assert their MUST with no inline tag at all, leaving only FR-024, FR-036, FR-046 and FR-047 self-citing? [Traceability, Spec Functional Requirements] — **FINDING:** of the 32 written FRs, only four (FR-024, FR-036, FR-046, FR-047) carry an explicit parenthetical citation; the other 28 — including every schema (FR-001–005) and validator (FR-010–016) requirement — state their MUST with no inline box/Q/ruling tag, so the FR↔box mapping exists only in the separate executable `tasks.md` (T010–T028), not in spec.md itself.
- [x] CHK005 Is a requirement defined for what happens when a box's evidence and its tick land in different commits (the FR-041 violation case), beyond stating the same-commit rule itself — i.e. is there a stated remediation, or is the rule stated with no recovery path? [Gap, Spec FR-041]
- [x] CHK006 Is the corpus-count correction at `contracts/README.md:102` (FR-024) stated as an ADDITIONAL act distinct from the ratified task list's own numbering, so a reader cannot mistake it for a renumbering of task 4.9? [Completeness, Spec FR-024]

## Requirement Clarity & Precision

- [x] CHK007 Is "more generally any state in which the pin has been advanced to a value the chain itself records as observed" (FR-011) given any bound tighter than "any state", or does the requirement leave the residual clause exactly as open as the ratified task 3.2 text it copies verbatim? [Clarity, Spec FR-011, OpenSpec tasks.md 3.2]
- [ ] CHK008 Is "DISTINCT finding codes per leg" (FR-010) precise enough to determine, without reading the User Story 2 Acceptance Scenarios, that the ANCHOR leg shares ONE code across both its digest and locator halves while the LINKAGE leg splits into TWO codes (one per half) — an asymmetry the ratified packet's task 3.1 also carries but FR-010's prose does not surface? [Ambiguity, Spec FR-010, US2 Acceptance 1–2] — **FINDING:** FR-010 says only "anchor in BOTH halves... linkage in BOTH halves... with DISTINCT finding codes per leg", which reads as though anchor and linkage are symmetric; a reader must go to User Story 2's Acceptance Scenarios 1–2 (lines ~130–134) to learn that the anchor's two halves share `custody-chain-unanchored` while linkage's two halves are `custody-chain-broken-link` vs `custody-chain-locator-gap` — two different codes. FR-010 itself never names any of the four codes.
- [ ] CHK009 Is "what it checked and what it did not" (FR-013) given the same itemized content the ratified delta's own scenario "The neutral pass is not a currency claim" specifies (anchoring, linkage in digest AND locator, order, enumerations, entry closure, the unmoved pin, `path_only` digest equality, any withheld outcome, and nothing about the target's bytes), or is FR-013 a strictly weaker paraphrase that an implementer could satisfy with a vaguer line? [Completeness, Spec FR-013, Ratified delta line 280–284] — **FINDING:** FR-013 states only "the validator's report line... MUST state what it checked and what it did not"; it does not restate the ratified scenario's eight-item enumeration, so a report line naming only two or three of the eight checked facts would satisfy FR-013's text as written while falling short of the ratified scenario it realizes.
- [x] CHK010 Is "byte-identical" (FR-003) defined by an objective, reproducible check (`git diff` showing zero changed lines inside the `custody` object), rather than left as an unquantified adjective? [Clarity, Spec FR-003, SC-003]
- [x] CHK011 Is "the file's existing naming style" (FR-010) illustrated with the two named precedent codes (`custody-sha256-malformed`, `embedded-original-content`) anywhere in spec.md, or does a reader need to open `scripts/validate-consent-instruments.py` to know what "existing style" means? [Clarity, Spec FR-010] — checked against `scripts/validate-consent-instruments.py:400,393` where both precedent codes actually appear; spec.md itself never names them, but Key Entities and FR-016 both reuse `embedded-original-content` by name, so the style is demonstrated by example elsewhere in the same document. Passes on that basis.
- [x] CHK012 Is "the orchestrator" (FR-030: "the orchestrator re-measures at every merge-from-main and reports") a role defined anywhere in spec.md's Key Entities or elsewhere, distinct from "the LANE" that FR-030's next sentence names as the one who claims the number? [Ambiguity, Spec FR-030, Key Entities] — **FINDING:** "the orchestrator" appears in FR-030 and in `plan.md`'s Landing Contract point 2, naming an actor distinct from "the LANE", but spec.md's Key Entities section defines only `custody_rederivations` entry, the chain, WITHHELD and the candidate commit — no entity or role glossary distinguishes "the orchestrator" from "the LANE" for a reader of spec.md alone.
- [x] CHK013 Is "PROVISIONAL" candidate version naming (FR-030, "the PR body names `contract-v3.5` as an explicitly PROVISIONAL measured candidate") distinguished clearly enough from a reservation that a reader cannot construe the Measured-baseline table's own `contract-v3.5` figure as a claim already staked? [Clarity, Spec Measured baseline, FR-030, Edge Cases]

## Requirement Consistency

- [ ] CHK014 Do FR-004 ("`contract_schema_version` MUST move `2` → `3`... the record envelope's `schema_version` stays `const: 1`") and Clarifications Q4's ruling ("Confirmed. Only `contract_schema_version` moves... `$id` frozen... the `contracts/manifest.yaml` row's `schema_version: 1` frozen") describe the SAME set of frozen identity fields, or does FR-004 encode only two of Q4's four named facts? [Consistency, Spec FR-004, Clarifications Q4] — **FINDING:** Q4's ruling names FOUR frozen facts (`$id`, record-envelope `const: 1`, the manifest row's own `schema_version: 1` field, and — by omission — nothing else moves); FR-004 encodes only two of them (`contract_schema_version` 2→3, and the envelope's `const: 1`). Neither `$id` nor the manifest row's `schema_version: 1` field appears in any FR (confirmed absent from spec.md by search); they are named only in `tasks.md` T016 and in the clarify answer itself, so a reader of the Functional Requirements alone would not know these two facts are also frozen and gate-checked.
- [ ] CHK015 Do FR-021's fixture list and FR-010/FR-011/FR-014/FR-015's validator-behavior requirements name the SAME seven finding codes Clarifications Q10 rules "adopted... verbatim", or do three of the seven (`custody-chain-broken-link`, `custody-chain-out-of-order`, `custody-path-class-digests-differ`) never appear as literal strings anywhere in spec.md? [Consistency, Spec FR-010/011/014/015/021, Clarifications Q10] — **FINDING:** searched spec.md for all seven code strings; only four appear literally (`custody-chain-unanchored`, `custody-chain-locator-gap`, `custody-pin-rewritten` — all three only in User Story 2's Acceptance Scenarios, not in the FR text — and `custody-content-class-withheld` in FR-014). `custody-chain-broken-link`, `custody-chain-out-of-order` and `custody-path-class-digests-differ` do not occur anywhere in the file, even though Q10 rules all seven adopted verbatim and FR-021 requires negative fixtures for the refusals they name.
- [x] CHK016 Does FR-030's "re-measured at every merge-from-main" reconcile with plan.md's Landing Contract point 6 ("If `main` advanced under `contracts/` between integration and merge, the lane REPEATS the integration") without requiring the reader to open `plan.md` to learn WHAT repeating the integration entails? [Consistency, Spec FR-030, Plan Landing Contract]
- [x] CHK017 Is FR-036's "landing is a MERGE COMMIT" consistent with FR-034's "every gate MUST run against the exact unchanged candidate", given a merge commit is by FR-036's own text "a different commit" from the pre-merge candidate — does spec.md state, without deferring entirely to `plan.md`, that the FR-034 gate run must be REPEATED against the merge commit? [Consistency, Spec FR-034/036]
- [x] CHK018 Does the Measured-baseline table's box-class arithmetic (35 TICKED + 3 NOT-OWED-HERE + 8 NOT-OWED = 46) agree with SC-002's identical arithmetic and with `tasks.md`'s (feature-level) Box Accounting table, so all three documents assert the same 46-box partition? [Consistency, Spec Measured baseline/SC-002, Tasks Box Accounting]

## No Invented Requirements

- [x] CHK019 Does FR-024 — self-declared "NOT named by any ratified task" — trace to a specific ruling (clarify A1) rather than standing as an undisclosed addition to the ratified scope? [Traceability, Spec FR-024, Clarifications A1]
- [x] CHK020 Does FR-047 — self-declared "state it, do not act on it" — stop short of building, scheduling or ticking anything for A2's cross-repo consequence, matching A2's ruling exactly, rather than quietly widening this feature's scope to include F.2's gate? [Non-invention, Spec FR-047, Clarifications A2]
- [x] CHK021 Does FR-016's walk scope ("the whole entry minus the two digest fields") match Clarifications Q12's ruling exactly, rather than reverting to the narrower four-field scope task 3.5 originally proposed, without spec.md disclosing that the ratified task text and the realized requirement differ? [Non-invention, Spec FR-016, Clarifications Q12, OpenSpec tasks.md 3.5]
- [x] CHK022 Is FR-045 (the two-report doc-health comparison) traceable to the reused F.3 architect ruling the Assumptions section cites, rather than appearing as a bare new obligation with no stated basis? [Traceability, Spec FR-045, Assumptions]

## Ratified Delta Scenario Traceability (22 scenarios)

- [x] CHK023 "Custody is a pointer, not a payload" (delta line 54) — traceable via FR-003's byte-identity requirement, which is what preserves this unmodified behavior? [Traceability]
- [x] CHK024 "A re-derivation is recorded beside custody, never inside it" (line 62) — traceable via FR-001 (the sibling property) and FR-003 (custody untouched)? [Traceability]
- [ ] CHK025 "A re-derivation does not amend the instrument" (line 68) — traceable to any FR in spec.md's Functional Requirements? [Traceability] — **FINDING:** no FR states that a `custody_rederivations` entry requires no `amendments` entry or status transition. The only place this rule appears in the feature's own documents is OpenSpec packet task 1.3 (an `[OPERATOR]` ratification point, C-10) and `research.md`; spec.md's Functional Requirements section is silent on it, so this ratified scenario has no FR-level landing point.
- [x] CHK026 "The executed pin is never rewritten to match the moved target" (line 74) — traceable via FR-011 (refuse a rewritten pin)? [Traceability]
- [x] CHK027 "An unattributed or uncited acceptance is refused" (line 80) — traceable via FR-001's required-field list naming `ruling_ref` and `recorded_by`? [Traceability]
- [x] CHK028 "An unknown class or reason is refused at the contract" (line 86) — traceable via FR-002's closed enums plus FR-021's negative fixtures for each? [Traceability]
- [x] CHK029 "An instrument that declares no re-derivations is unaffected" (line 92) — traceable via FR-004's ADDITIVE statement and US1 Acceptance Scenario 2? [Traceability]
- [x] CHK030 "A direct pin verifies with no chain" (line 196) — correctly requires no new FR, since this is pre-existing, unmodified validator behavior the feature does not touch? [Traceability]
- [x] CHK031 "An unbroken chain is admitted, link by link" (line 202) — traceable via FR-010? [Traceability]
- [x] CHK032 "A path move is re-derived at both paths" (line 208) — correctly disclaimed as a consumer-side (git-based) act via FR-012's "MUST NOT open a repository" boundary and Out of scope §6's "operated custody-digest check", rather than silently unaddressed? [Traceability, Out of scope §6]
- [x] CHK033 "A path_only entry whose digests differ is refused" (line 214) — traceable via FR-015? [Traceability]
- [x] CHK034 "A header_only claim contradicted by the diff is refused" (line 220) — correctly disclaimed as consumer-side (requires measuring the actual diff) via the same FR-012/Out-of-scope §6 boundary as CHK032, rather than silently unaddressed? [Traceability, Out of scope §6]
- [x] CHK035 "A locator pair that resolves at neither path is refused" (line 226) — correctly disclaimed as consumer-side (locator resolution needs the declared custody store mapping, which lives in the consuming repository) via the same boundary? [Traceability, Out of scope §6]
- [x] CHK036 "A content-class divergence withholds the verdict" (line 232) — traceable via FR-014? [Traceability]
- [x] CHK037 "A consumer gate propagates a withheld verdict and never upgrades it" (line 238) — correctly disclaimed as consumer-side (§6.2b's "operate the custody-digest check")? [Traceability, Out of scope §6]
- [x] CHK038 "A broken link is refused, not repaired" (line 244) — traceable via FR-010, though the specific code name `custody-chain-broken-link` is absent from spec.md (see CHK015)? [Traceability]
- [x] CHK039 "A chain that does not anchor to the pin is refused" (line 250) — traceable via FR-010? [Traceability]
- [x] CHK040 "A chain on a commit that is not an ancestor of HEAD is refused" (line 256) — correctly disclaimed as consumer-side (git ancestry is unavailable to a validator FR-012 forbids from opening a repository)? [Traceability, Out of scope §6]
- [x] CHK041 "A HEAD digest matching no terminus is refused" (line 262) — correctly disclaimed as consumer-side for the same reason? [Traceability, Out of scope §6]
- [x] CHK042 "Entries out of recorded-time order are refused" (line 268) — traceable via FR-010? [Traceability]
- [x] CHK043 "A chain that cannot be re-derived is refused, never admitted" (line 274) — correctly disclaimed as consumer-side (F.2's gate, § 7.1)? [Traceability, Out of scope §7]
- [x] CHK044 "The neutral pass is not a currency claim" (line 280) — traceable via FR-013, subject to the completeness gap already recorded at CHK009? [Traceability]

## Clarify Q-Answer Fidelity

- [x] CHK045 Is Q1(a)'s "ONE pull request carrying §§ 2–5" encoded as a MUST in FR-030, rather than left as a plan-only decision with no FR backing it? [Fidelity, Spec FR-030, Clarifications Q1]
- [ ] CHK046 Is Q4's full four-fact ruling ($id frozen, envelope const:1 frozen, manifest row schema_version:1 frozen, only contract_schema_version moves) encoded completely in FR-004, or only half of it (see CHK014)? [Fidelity, Spec FR-004, Clarifications Q4] — **FINDING:** duplicate of CHK014; recorded here under its Q-answer-fidelity aspect because the gap is a ruling not fully carried into a requirement, not merely an internal inconsistency.
- [x] CHK047 Is Q5's "NO SPLIT... § 2's commit leaves the digest stale on purpose" encoded in FR-031, including the instruction that the commit message must say so? [Fidelity, Spec FR-031, Clarifications Q5]
- [x] CHK048 Is Q6's "attributes ALL of the above by originating change/PR" and "Change class: ADDITIVE (minor)" encoded in FR-032? [Fidelity, Spec FR-032, Clarifications Q6]
- [x] CHK049 Is Q7's three-part answer (directory name, BOTH self-test-fixture-and-pytest for the walk, BOTH source-level-and-runtime-patch for no-git, over all three buckets) fully encoded across FR-012 and FR-016? [Fidelity, Spec FR-012/016, Clarifications Q7]
- [x] CHK050 Is Q8's ruling — which of the (now five) README sentences take the `3b530009` form vs. which are left true-when-written, and the BLOCKED substrate-note precondition — encoded in FR-046 and Phase F of `tasks.md`? [Fidelity, Spec FR-046, Clarifications Q8]
- [x] CHK051 Is Q9's "nine new bullets, third table column" encoded precisely (not merely "grows") in FR-023? [Fidelity, Spec FR-023, Clarifications Q9]
- [x] CHK052 Is Q11's "ticked on the local run... the workflow's own green is the lane's PR-open observation, not this feature's tick condition" encoded in a way that FR-034 alone does not contradict (i.e., FR-034 does not imply the workflow run itself is required)? [Fidelity, Spec FR-034, Clarifications Q11]

## Success Criteria Measurability

- [x] CHK053 Is SC-001's "0 errors and 0 warnings" paired with an exact invocation (`--strict`, no path argument) so two readers would run the identical command? [Measurability, Spec SC-001]
- [x] CHK054 Is SC-002's box-class arithmetic independently reproducible from `tasks.md`'s own note-count without re-deriving the 46-box partition from the packet? [Measurability, Spec SC-002]
- [x] CHK055 Is SC-006's "zero UNDISPOSITIONED failures" defined anywhere in spec.md, or does a reader need `contracts/openspec-cli-pin.yaml`'s disposition ledger (per the 032 precedent's own resolution of the identical ambiguity) to know what "undispositioned" excludes? [Ambiguity, Spec SC-006]
- [x] CHK056 Is SC-010's exit-status assertion checkable independent of Brett Heap's still-PARKED ruling on the exact number (FR-014), i.e. does SC-010 test "a distinguishable non-zero status" rather than hard-coding the provisional `3`? [Measurability, Spec SC-010, FR-014]
- [ ] CHK057 Does SC-010 appear in its correct numeric position among SC-001..SC-009, or is it placed between SC-007 and SC-008 in the document body, out of sequence? [Clarity, Spec Success Criteria] — **FINDING:** SC-010 is written between SC-007 and SC-008 (spec.md lines 510–519: SC-001..SC-007, then SC-010, then SC-008, SC-009) rather than after SC-009 in numeric order. Cosmetic, but a reader scanning for "SC-008" or "SC-009" must read past SC-010 first.

## Acceptance Criteria Quality

- [x] CHK058 Is User Story 2 Acceptance Scenario 4's "exits in the status class that means 'needs a human decision'" checkable without first reading FR-014's constant name, or does the scenario stand alone as a testable assertion? [Measurability, Spec US2 Acceptance 4]
- [x] CHK059 Is User Story 4 Acceptance Scenario 4's "every gate reruns against the landed commit" cross-checked against FR-036's identical requirement so the two do not silently diverge under a future edit to either? [Consistency, Spec US4 Acceptance 4, FR-036]
- [x] CHK060 Is User Story 3's Independent Test ("removing any one fixture reddens it") a claim a reviewer can verify mechanically (delete one file, re-run, observe a nonzero exit) rather than one requiring trust in the self-test's internal wiring? [Measurability, Spec US3 Independent Test]

## Ambiguities & Conflicts

- [x] CHK061 Does "the packet governs and this file is the defect" (spec.md's own stated resolution rule, near the top) foreclose the reading that a spec.md FR narrower than the ratified delta (e.g. FR-013's weaker report-line text, CHK009) is itself a defect requiring correction before this branch is handed off? [Ambiguity, Spec header framing]
- [x] CHK062 Is "verifiably DONE" (FR-040) given a general test applicable to boxes outside §0–1 (e.g., a future §2 box ticked mid-branch), or illustrated only by the four already-performed boxes research.md documents? [Clarity, Spec FR-040]
- [x] CHK063 Does FR-043's list of permitted edits ("`tasks.md`, the evidence file, and ONE additive dated realization note") reconcile with FR-046's THREE separate `README.md` amendment sites and FR-078-equivalent (tasks.md T078) note in the packet's own `tasks.md`, without a reader construing FR-043 as forbidding those additional writes? [Consistency, Spec FR-043/046]

## Structural / Numbering Hygiene

- [x] CHK064 Does the FR numbering scheme (FR-00x for §2, FR-01x for §3, FR-02x for §4, FR-03x for §5, FR-04x for bookkeeping) hold without exception across all 32 written FRs, making the block-of-ten gaps (FR-006–009, FR-017–019, FR-025–029, FR-037–039) a deliberate section-aligned convention rather than an unexplained numbering hole? [Clarity, Spec Functional Requirements]
- [x] CHK065 Is the feature's own title's claim realized precisely — does spec.md realize §§ 0–5 ONLY, with §§ 6–7 explicitly and consistently excluded in the Out of scope section, the Measured-baseline table and the Assumptions section, with no internal contradiction about the boundary? [Consistency, Spec title/Out of scope/Measured baseline]

---

## Evaluation — 2026-09-09

**Tally**: 57 passed / 8 unticked / 0 dispositioned (total 65).

### Findings (unticked items)

1. **CHK004** — 28 of 32 FRs carry no inline traceability tag (box/Q/ruling); only FR-024, FR-036, FR-046, FR-047 self-cite.
2. **CHK008** — FR-010 does not surface the anchor-vs-linkage code asymmetry (one code for anchor's two halves, two codes for linkage's two halves); only the User Story 2 Acceptance Scenarios do.
3. **CHK009** — FR-013's "what it checked and what it did not" is strictly weaker than the ratified delta's eight-item enumeration for the same scenario.
4. **CHK014** — Q4's ruling on `$id` and the manifest row's `schema_version: 1` field is not encoded in any FR; only `contract_schema_version` and the record envelope's `const: 1` are.
5. **CHK015** — three of the seven Q10-ratified finding codes (`custody-chain-broken-link`, `custody-chain-out-of-order`, `custody-path-class-digests-differ`) never appear as literal strings anywhere in spec.md.
6. **CHK025** — the ratified delta's "A re-derivation does not amend the instrument" scenario has no landing FR anywhere in spec.md's Functional Requirements.
7. **CHK046** — same underlying defect as CHK014, recorded separately under the Q-answer-fidelity section per this checklist's own cross-referencing requirement.
8. **CHK057** — SC-010 is placed out of numeric sequence, between SC-007 and SC-008.

Six distinct defects (CHK014 and CHK046 are the same defect viewed from two
required angles — internal consistency and Q-answer fidelity — as is
CHK008/CHK015's shared code-naming root, tracked separately because they cite
different requirements and different failure modes).
