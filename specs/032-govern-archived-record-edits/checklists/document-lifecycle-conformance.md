# Checklist: Document-Lifecycle Conformance of the § 3.4 Adoption

**State**: written 2026-09-08, NOT YET RUN — this file is the gate instrument for the architect's refutation panel. The findings its authoring raised were resolved in the analyze loop and are recorded in [`../analysis.md`](../analysis.md).

**Purpose**: "Unit tests for English" over the requirements governing the one
top-level bullet this feature adds to `docs/document-lifecycle.md` § *Status
Claim Rules*. Every item below interrogates the QUALITY of the written
requirement — completeness, clarity, consistency, measurability, and coverage
of the lifecycle machinery (the 15-real-line header window, the two sanctioned
ratification-citation spellings, the Explicit Delta Rule, the `evidence/`
scan-exclusion) the feature claims to conform to. No item asks whether the
edit was performed correctly; that is the gate report's job, not this one.
**Created**: 2026-09-08
**Feature**: [spec.md](../spec.md)
**Depth**: Formal release gate | **Audience**: Reviewer / release governance

## Requirement Completeness

- [x] CHK001 Is the exact 15-real-line boundary of the lifecycle-header scan window (`STATUS_SCAN_LINES = 15`, `scripts/doc_health/corpus.py:111`) named anywhere in FR-002 or FR-004 as the test for "the edited file's own lifecycle-header block," or is the placement left to inference from a sibling precedent bullet? [Completeness, Spec FR-002, FR-004]
- [x] CHK002 Are the three "real line" endings (CR, LF, CRLF) that the header-window count is defined over — as opposed to the wider set of Unicode line separators `str.splitlines()` treats as breaks — named as the counting rule FR-002's placement claim relies on? [Completeness, Gap]
- [x] CHK003 Does the spec name which of the document's two sanctioned ratification-citation spellings — the header-level `Ratified by: <change>` (colon, for a document's own `Status: ratified` claim) or the inline precedent form `Ratified by \`<change>\` (<date>)` (no colon, the sibling `govern-openspec-corpus-membership` bullet's form) — FR-003's citation is drawn from, given the two differ by more than punctuation? [Completeness, Ambiguity, Spec FR-003, docs/document-lifecycle.md §Status Claim Rules]
- [x] CHK004 Does FR-013 distinguish the `evidence/` exclusion (no lifecycle header owed) from the `review/` inclusion ("a `review/` record would owe one") with enough precision that a reader knows which of the packet's OTHER working directories (`supporting-docs/`, `source-snapshots/`) share the same exclusion, given `EVIDENCE_PARTS` covers three segments but FR-013 names only one? [Completeness, Gap, Spec FR-013]
- [x] CHK005 Is the `evidence/` path-segment exclusion (FR-013, `EVIDENCE_PARTS` at `scripts/doc_health/corpus.py:107`) stated with the SAME segment-matching rule the code applies (a directory-PART match anywhere in the path, not a suffix or filename match), so a reader cannot mistake it for a narrower "the file is literally named evidence.md" rule? [Completeness, Spec FR-013]
- [x] CHK006 Does FR-005 fully enumerate the content the two explanatory sentences must and must not carry (ruling recorded before the edit; note records WHAT not THAT IT MAY) precisely enough to reject a drafted sentence that says something adjacent but not identical — e.g., "the note documents the change" without the before/after ordering claim? [Completeness, Measurability, Spec FR-005]

## Requirement Clarity

- [x] CHK007 Is the phrase "the edited file's own lifecycle-header block" in FR-002 clearly scoped to the FUTURE archived file the adopted rule will apply to, and not to `docs/document-lifecycle.md`'s own header — given the new bullet sits in a body section (§ *Status Claim Rules*) far below this document's own 15-line header window, and a careless reader could conflate the two? [Clarity, Ambiguity, Spec FR-002, FR-004]
- [x] CHK008 Is "the requirement text being the packet's and reaching canon at archive" (FR-005) precise enough to tell a future reader WHICH sentences in the finished bullet are the two permitted explanatory sentences and which is the quoted requirement text, absent any typographic or structural marker distinguishing them? [Clarity, Spec FR-005]
- [x] CHK009 Is a rule given for how a reader — or doc-health's Explicit Delta Rule tooling — distinguishes the bullet's "explanation" prose (FR-005, exactly two sentences) from "requirement text" by anything other than trusting the author's intent, given neither FR-004 nor FR-005 requires a marker separating them? [Ambiguity, Spec FR-004, FR-005]
- [x] CHK010 Is "minimal" in FR-005's "the prose MUST stay minimal" given any measurable bound (a sentence count, a word count, or a comparison document), or is it left as an unquantified adjective a reviewer must judge unaided? [Ambiguity, Spec FR-005]
- [x] CHK011 Is the placement instruction precise enough that an implementer following task T005's literal wording ("after the byte-exact-evidence bullet") alone, without cross-checking FR-004, could not produce a bullet nested one indentation level too deep? [Clarity, Tasks T005]

## Requirement Consistency

- [x] CHK012 Is FR-004's instruction that the new content be "a new TOP-LEVEL BULLET... in the shape the `govern-openspec-corpus-membership` bullet already uses" consistent with task T005's instruction to place it "after the byte-exact-evidence bullet" — given that bullet is itself a SUB-bullet nested under the `govern-openspec-corpus-membership` bullet, so "after" it could mean either a further nested sub-bullet or a new top-level bullet following the whole parent block, and only the second reading satisfies FR-004? [Consistency, Ambiguity, Spec FR-004, Tasks T005]
- [x] CHK013 Is the requirement that the new passage "MUST NOT claim `standard` authority the corpus does not back" (FR-005, citing `docs/document-lifecycle.md` line 57) reconciled with the fact that the passage's own backing citation (FR-003) names a RATIFIED change that reaches promoted canon only "at the archive act" — is it specified how a `standard`-status document may add content backed by a not-yet-promoted ratification without breaching line 57's "backed by a promoted OpenSpec spec or canonical contract" test? [Conflict, Spec FR-003, FR-005, docs/document-lifecycle.md:57]
- [x] CHK014 Is the Explicit Delta Rule's "restatement of promoted policy in different words is a defect" test reconciled with FR-001's demand to quote the note form "byte-exact from the ratified requirement" — given the source requirement is RATIFIED, not yet PROMOTED, so the Explicit Delta Rule's literal trigger ("restates promoted policy") does not yet apply, and is that non-application stated as a reason rather than left to be assumed? [Consistency, Ambiguity, Spec FR-001, docs/document-lifecycle.md §The Explicit Delta Rule]
- [x] CHK015 Is there a conflict between FR-009 ("no ratified requirement text may be reworded") and FR-001's demand to quote "byte-exact... including the em dash and the placeholder spellings" — does byte-exact quotation of a SUBSTRING of the ratified requirement (the note form alone, stripped of its surrounding "THE NOTE HAS A NEUTRAL MINIMUM..." framing) count as quotation or as a form of rewording-by-omission, and is that line drawn anywhere? [Conflict, Spec FR-001, FR-009]
- [x] CHK016 Is there a conflict between the corpus norm that a ratification citation sits within a document's own 15-line header window and FR-003's placement of a ratification citation deep in body prose — or is it established, per research.md M8, that inline body citations of a POLICY BULLET (as opposed to the whole document) are a separate, already-precedented class the header-window rule was never meant to reach? [Conflict, Ambiguity, docs/document-lifecycle.md §Status Claim Rules, Research M8]

## Measurability / Acceptance Criteria Quality

- [x] CHK017 Is SC-001's acceptance test — "the string `Edited (bookkeeping):` appears in that document at least once" — precise enough to guard against a bullet that contains the string inside prose ABOUT the note (e.g., quoting it merely as an example) rather than as the sanctioned byte-exact form with its placeholders, or does the criterion need the FULL line form rather than substring presence? [Measurability, Spec SC-001]
- [x] CHK018 Is the doc-health finding-set diff criterion (SC-003 / gate 4.4) specified precisely enough to say WHICH finding fields must match (rule id + path + line, or rule id + path only), so a line-number shift caused by inserting the new bullet cannot silently produce a spurious non-empty diff that the criterion would then wrongly treat as a blocker? [Measurability, Spec SC-003]
- [x] CHK019 Can FR-006's "the test is ACT-DONE, not actor-class" be objectively measured for a § 1 `[OPERATOR]` box, given the two precedents it cites (`create-medxchart-overlay-boundary` § 5.3, `add-release-tag-gate` § 4.1) are ticked on a READ-BACK console artifact, while this feature's own § 1 boxes are ticked against a GitHub review id and timestamp with an EXPLICITLY EMPTY approval body — is the evidentiary bar for "done" the same in both cases, or narrower here precisely because there is no word to quote? [Measurability, Spec FR-006]

## Scenario Coverage (Primary / Alternate / Exception / Recovery / Non-Functional)

- [x] CHK020 Primary: Are requirements defined for a reader who has never seen the OpenSpec packet recovering the note's exact form, its placement, and its ratifying change from `docs/document-lifecycle.md` alone (SC-001, US1 Acceptance Scenario 1) — including the case where FR-003's citation is the reader's ONLY route to the ratifying change id, so a garbled or dropped citation breaks the primary path entirely? [Coverage, Primary Flow, Spec SC-001, FR-003]
- [x] CHK021 Alternate: Are requirements defined for a reviewer reading ONLY `docs/document-lifecycle.md` (the Independent Test's stated condition) reaching a DIFFERENT note form than the ratified requirement's, because the two explanatory sentences (FR-005) are worded ambiguously enough to be read as narrowing or widening the neutral minimum? [Coverage, Alternate Flow, Spec US1 Independent Test]
- [x] CHK022 Exception: Are requirements defined for the byte-exact quotation (T006) being transcribed with a drifted character — an en dash substituted for the required em dash, or a straight quote for the ratified requirement's own punctuation — with a verification step distinct from T009's general "states no rule the ratified requirement does not carry" check that would catch a punctuation-level transcription defect specifically? [Coverage, Exception Flow, Tasks T006, T009]
- [x] CHK023 Recovery: Are requirements defined for the recovery path when doc-health's finding set DOES move (Edge Cases: "doc-health's finding set moves for a reason unrelated to this diff") — does the spec state a concrete recovery (rework the edit vs. an explained exception) rather than only naming the two options in the abstract? [Coverage, Recovery, Spec Edge Cases]
- [x] CHK024 Non-Functional: Is the requirement that "no rule the ratified requirement does not carry" be introduced (FR-005) paired with any repeatable check other than human re-reading — e.g., a word-diff against the ratified requirement's own text — so the constraint is enforceable at scale rather than only at first-author diligence? [Non-Functional, Measurability, Spec FR-005]

## Edge Case Coverage

- [x] CHK025 Is the case where ANOTHER lane or change adds a further top-level bullet to § *Status Claim Rules* before this feature's commit lands addressed — FR-004's "at the end of" placement is relative, and would silently become inaccurate (no longer last) under a race the spec does not name? [Edge Case, Gap, Spec FR-004]
- [x] CHK026 Is the case addressed where the archive act (which the ratified requirement's promotion depends on) lands BEFORE this branch, changing "reaches promoted canon at the archive act" (FR-003) from a future-tense claim to a past one — does the passage's wording need to change post-archive, or is "at the archive act" phrased so it reads correctly in both states? [Edge Case, Ambiguity, Spec FR-003]

## Ambiguities & Conflicts

- [ ] CHK027 Is there a stated rule for what happens to the § 3.4 bullet's conformance status on the day the archive act promotes the underlying requirement — does it then become subject to the Explicit Delta Rule as a restatement of NOW-promoted policy, and if so is a marker (`xspec:supersedes` or equivalent) anticipated anywhere, or does the byte-exact quotation implicitly substitute for one without that substitution being stated? [Gap, Spec FR-001, FR-003] **— DISPOSITIONED:** this decides what happens to the § 3.4 bullet's conformance status AFTER the archive act promotes the underlying requirement (whether the Explicit Delta Rule then applies, whether a supersedes marker is owed) — an act this feature's own FR-015 explicitly stops before, and the Glossary now names "the archive act" as "the later, separate act." That decision belongs to whoever performs or reviews the archive act at that later time, not to this realization branch.
- [x] CHK028 Is the state BETWEEN this feature's landing and the archive act — during which `docs/document-lifecycle.md` carries `Status: standard` prose backed by a ratified-but-not-yet-promoted requirement — named anywhere as an intentional, self-healing interval rather than left to read as a residual line-57 defect a reader must resolve unaided? [Gap, Spec FR-003, FR-005]

## Dependencies & Assumptions

- [x] CHK029 Is the assumption that the `govern-openspec-corpus-membership` bullet's shape (research.md M8) is still an accurate, unedited precedent at this feature's base commit stated as a RE-CHECKED measurement rather than a one-time citation, given research.md's own M1 discipline of re-measuring rather than trusting an earlier read? [Assumption, Research M8, M1]
- [x] CHK030 Is it documented as an assumption that the `govern-openspec-corpus-membership` bullet (M8's precedent, cited to justify FR-003's citation form) is itself the ONLY prior instance of this inline-citation convention in the document, so that FR-003's "the precedent form" resolves to one unambiguous shape rather than to a choice among several unstated variants elsewhere in the corpus? [Assumption, Research M8]

## Notes

- **CHK007 and CHK012 are the sharpest cross-artifact findings**: FR-002's
  "edited file's own lifecycle-header block" governs where a FUTURE bookkeeping
  note goes on some OTHER file, not where THIS bullet sits in
  `docs/document-lifecycle.md` — but nothing in the spec states that
  disambiguation explicitly, and task T005's "after the byte-exact-evidence
  bullet" wording is one misread away from nesting the new content one level
  too deep under `govern-openspec-corpus-membership` instead of beside it.
- **CHK013/CHK014/CHK027/CHK028 form one family**: the feature adopts language
  from a requirement that is ratified but not yet promoted, inside a document
  whose own rules (line 57, the Explicit Delta Rule) are written in terms of
  PROMOTED canon. The spec's individual FRs are each locally correct; none of
  them states the transition rule for the interval between this landing and
  the archive act, or for the day after.

## Evaluation — 2026-09-08 (consolidated, round 3)

**Tally**: 23 passed / 6 open / 1 dispositioned / 0 deferred (total 30).

History: round 1 = 13 passed / 17 open; round 2 (after amendment) closed CHK017,
CHK020, CHK022, CHK025 → 17 passed / 13 open; round 3 (this one) closed CHK001,
CHK009, CHK013, CHK028, CHK029, CHK030, and moved CHK027 to dispositioned →
23 passed / 6 open / 1 dispositioned.

### Open items
- CHK002 — no stated line-ending convention for the header-window count (FR-002 gained `STATUS_SCAN_LINES = 15` but not this) → name the `corpus.py`-matching counting rule in research.md or FR-002.
- CHK014 — FR-005b reconciles line 57 but the Explicit Delta Rule's separate "restates promoted policy" trigger is not itself addressed by name → extend FR-005b's reasoning to the Explicit Delta Rule explicitly.
- CHK015 — no rule distinguishing byte-exact substring quotation from rewording-by-omission under FR-009 → add a clause to FR-001 or FR-009.
- CHK018 — the identity-safe recipe (FR-028) fixes repo-identity normalization but not the finding-key match-field question (line number included or not) → add the matching rule to T016/FR-011.
- CHK024 — FR-005's "no added rule" constraint still has no repeatable non-human check (T030a covers only the note form) → add a word-diff verification task for the two explanatory sentences.
- CHK026 — no statement that FR-003's "at the archive act" phrasing reads correctly before and after that act → add a clarifying sentence to FR-003.

### Dispositioned items
- CHK027 — decides the § 3.4 bullet's conformance status AFTER the archive act promotes the underlying requirement (Explicit Delta Rule applicability, a possible supersedes marker). This feature's own FR-015 stops before the archive act, and the Glossary names it "the later, separate act" — that decision belongs to whoever performs or reviews the archive act, not to this realization branch.

### Deferred items
- None.

## Final closure — 2026-09-08 (orchestrator, after the amendment round)

Every item this file left OPEN after round 3 was closed by the amendments the
requirements now carry (FR-033..FR-040 and the targeted edits to FR-005b,
FR-008b, FR-012, FR-025, FR-028, SC-007, the Edge-Cases record obligation, and
tasks T010/T029/T030a/T033a). Items closed in this pass: CHK002, CHK014, CHK015, CHK018, CHK024, CHK026.

**Final tally: 29 passed / 1 dispositioned / 0 open.** A DISPOSITIONED
item is one that cannot be closed from inside this feature — it needs an act in a
frozen file, another repository's process, or a later act's own decision — and it
carries that reason inline.

