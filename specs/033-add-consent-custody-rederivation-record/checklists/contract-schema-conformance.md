# Checklist: Contract Schema Conformance — § 2, the schema growth

**Purpose**: Release-gate check that `spec.md`'s FR-001–FR-005 (the § 2 schema
requirements) state the ten-field entry shape, entry closure, the two closed
enumerations, the additive posture, `custody`'s byte-identity, the
`contract_schema_version` 2→3 bump, the frozen `$id`/`const: 1`/manifest
`schema_version` trio, the three mandated in-file comments and the D9 sibling
argument PRECISELY AND COMPLETELY enough to implement without returning to the
ratified packet. Every item is checked against the WRITTEN REQUIREMENT text,
cross-referenced against the ratified delta, the ratified packet's `tasks.md`
§ 2, and the CURRENT (pre-realization) state of the schema file itself, since
`contract_schema_version` is measured at `2` today with no `custody_rederivations`
property (`research.md` R5, R8; Measured baseline table) — nothing in § 2 has
been built yet, so this checklist interrogates what the requirement TEXT
commits an implementer to, not running code.

**Artifacts under review**: `specs/033-add-consent-custody-rederivation-record/spec.md`
FR-001–FR-005 (and, where cited, FR-016 for the boundary with the walk
extension); `contracts/schemas/consent-instrument.schema.yaml` (current state,
354 lines); `openspec/changes/add-consent-custody-rederivation-record/tasks.md`
§ 2 (tasks 2.1–2.5); `openspec/changes/add-consent-custody-rederivation-record/specs/consent-instrument/spec.md`
(the ratified MODIFIED requirement); `clarify-questions.md` Q4, Q5, Q12.

**Date**: 2026-09-09. **State**: run the same day it was written.

## The Ten Required Fields, In Order

- [x] CHK001 Does FR-001 name all TEN required fields, in the same order as ratified task 2.1's list (`at, commit, previous_locator, observed_locator, previous_sha256, observed_sha256, diff_class, reason, ruling_ref, recorded_by`)? [Conformance, Spec FR-001, OpenSpec tasks.md 2.1]
- [x] CHK002 Does FR-001 state the entry's `required` array names EXACTLY these ten — no fewer, no eleventh — matching the ratified delta's "Each entry SHALL be closed... and SHALL carry all of" the ten named facts (delta lines 22–30)? [Conformance, Spec FR-001, Ratified delta lines 22–30]
- [x] CHK003 Is the entry-closure test for an ELEVENTH property (FR-021's fixture, task 4.7) consistent with FR-001 requiring exactly ten — i.e., does spec.md's own text explain why a "ninth" fixture (task 4.7's own parenthetical) would not test closure, given the field count moved from nine to ten under C-6a? [Consistency, Spec FR-021, OpenSpec tasks.md 4.7]

## Field Shape Precision

- [x] CHK004 Does FR-002 pin `at` to `type: string, format: date-time` — the same format keyword already used for `status_history[].at` in the current schema (`consent-instrument.schema.yaml:220–222`) — rather than a looser `type: string` with no format? [Conformance, Spec FR-002, Schema line 220–222]
- [x] CHK005 Does FR-002 pin `commit` to `pattern: "^[0-9a-f]{40}$"` (a 40-hex git SHA-1), matching exactly the ratified task 2.1 text with no widened or narrowed character class? [Conformance, Spec FR-002, OpenSpec tasks.md 2.1]
- [x] CHK006 Does FR-002 pin both digest fields to `pattern: "^[0-9a-f]{64}$"` — the IDENTICAL pattern the current schema already uses for `custody.sha256` (`consent-instrument.schema.yaml:196`) — so the new digests are held to the same precision as the existing pin, not a looser one? [Conformance, Spec FR-002, Schema line 196]
- [x] CHK007 Does FR-002 state both locator fields as `type: string, minLength: 1` with "NO path grammar imposed", matching the existing `custody.locator` shape (`consent-instrument.schema.yaml:189–191`, also `type: string, minLength: 1` with no pattern) precedent exactly, rather than introducing a new constraint (e.g., a URI pattern) the existing locator does not carry? [Conformance, Spec FR-002, Schema line 189–191]
- [x] CHK008 Does FR-002 state `ruling_ref` and `recorded_by` as `type: string, minLength: 1` with no further shape constraint, matching the ratified task 2.1 text exactly? [Conformance, Spec FR-002, OpenSpec tasks.md 2.1]

## Entry Closure

- [x] CHK009 Does FR-001 require `additionalProperties: false` on the entry object itself (not merely on the array), so an eleventh property is refused at the entry level rather than only at the array level? [Conformance, Spec FR-001]
- [x] CHK010 Is the entry-object closure pattern (`type: object`, `additionalProperties: false`, an explicit `required` list) the SAME pattern the current schema already uses for every other closed sub-object (`custody`, `revocation`, `data_consent`, `parties[]` items, `amendments[]` items — `consent-instrument.schema.yaml:96–97, 168–169, 187, 232, 311`), so FR-001 introduces no new closure idiom? [Consistency, Spec FR-001, Schema multiple lines]

## The Two Three-Member Enums

- [x] CHK011 Does FR-002 close `diff_class` to exactly `[path_only, header_only, content]` — three members, matching the ratified delta's "minimally `path_only`, `header_only` and `content`" (delta line 33)? [Conformance, Spec FR-002, Ratified delta line 33]
- [x] CHK012 Does FR-002 close `reason` to exactly `[lifecycle_header_edit, archive_move, other_ruled_edit]` — three members, matching the ratified delta line 34? [Conformance, Spec FR-002, Ratified delta line 34]
- [ ] CHK013 Does any FR (FR-001–005) state that a FUTURE new `diff_class` or `reason` member requires a contract change (a further `contract_schema_version` bump) rather than a silent widening — the ratified delta's own words are "a novel class arrives as a contract question rather than as a silently admitted string" (delta line 35–36) — or is that governance consequence left unstated in spec.md's Functional Requirements, recoverable only from the ratified delta text itself? [Gap, Spec FR-002, Ratified delta lines 35–36] — **FINDING:** FR-002 states the two enums' closed membership but does not carry forward the ratified delta's explicit governance consequence (a new member is a contract change, never author-coined) into the FR text; a reader of FR-002 alone would know the enum is closed today but not that widening it is itself a governed act requiring a future schema growth, only that FR-021 tests refusal of an unknown member today.
- [x] CHK014 Does spec.md's FR text (or Key Entities) explain WHY `path_only` is a distinct third member rather than folding into `content` — i.e., is the ratified delta's rationale ("a pure relocation changes ZERO bytes... calling it `content` would withhold the verdict forever on a target nobody edited", task 2.1's own parenthetical) reachable from spec.md, even if only via a cross-reference to the ratified task rather than restated? [Traceability, OpenSpec tasks.md 2.1]

## Additive Posture

- [ ] CHK015 Does FR-001 state, alongside the entry shape it prescribes, that `custody_rederivations` MUST NOT be added to the schema's own TOP-LEVEL `required` array (`consent-instrument.schema.yaml:50–62`), or is the additive posture left to be inferred solely from FR-004's "ADDITIVE" adjective and US1 Acceptance Scenario 2? [Completeness, Spec FR-001/FR-004, Schema lines 50–62] — **FINDING:** FR-001 fully specifies the new property's own internal shape (array/items/required/pattern) but never states the complementary fact that the property itself is OPTIONAL at the top level — i.e., not added to the document's existing twelve-member `required:` list. An implementer reading FR-001 in isolation could add `custody_rederivations` to the top-level `required` array without violating FR-001's literal text, which would break every existing instrument and contradict FR-004's "ADDITIVE" claim and US1 Acceptance Scenario 2 ("an existing instrument declares no array... it validates unchanged").
- [x] CHK016 Does FR-004's "ADDITIVE" claim match the ratified delta's own additive statement ("The growth is ADDITIVE: an instrument that declares no re-derivations remains valid unchanged, and the record envelope's `schema_version` does not move", delta lines 51–52) word-for-word in substance? [Conformance, Spec FR-004, Ratified delta lines 51–52]
- [x] CHK017 Is the additive posture independently testable via US1 Acceptance Scenario 2 and FR-020's task-4.2-derived fixture (an unchanged existing example re-validated), giving the additive claim a concrete fixture-level test rather than resting on the adjective alone? [Measurability, Spec US1 Acceptance 2, FR-020]

## `custody` Byte-Identity

- [x] CHK018 Does FR-003 name all FOUR things that must stay byte-identical — the two properties (`locator`, `sha256`), the `required` array, `additionalProperties: false`, and the comment block — matching what is actually present in the current schema's `custody` object (`consent-instrument.schema.yaml:180–196`, confirmed: two properties, `required: [locator, sha256]`, `additionalProperties: false`, and comment lines 183–186 plus the two per-field comments)? [Conformance, Spec FR-003, Schema lines 180–196]
- [x] CHK019 Is FR-003's test ("A diff touching `custody` fails this requirement") stated as an objective, mechanically checkable predicate (`git diff` over the file showing zero changed lines inside the object's span), matching SC-003 exactly? [Measurability, Spec FR-003, SC-003]
- [x] CHK020 Does FR-003's byte-identity requirement correctly distinguish `custody` (frozen) from `custody_rederivations` (the new sibling FR-001 grows), so a reader cannot conflate the two objects when checking the diff? [Clarity, Spec FR-001/FR-003]

## Version Identity — `contract_schema_version` 2→3 and the Frozen Trio

- [x] CHK021 Does FR-004 require `contract_schema_version` to move from the MEASURED current value `2` (`consent-instrument.schema.yaml:14`) to `3`, matching the Measured-baseline table's own figure? [Conformance, Spec FR-004, Schema line 14, Measured baseline]
- [x] CHK022 Does FR-004 require the record envelope's `schema_version` to remain `const: 1` (`consent-instrument.schema.yaml:64–65`), matching Clarifications Q4's ruling on that one fact? [Conformance, Spec FR-004, Schema lines 64–65]
- [ ] CHK023 Does any FR require the schema's `$id: "consent-instrument.schema.yaml"` (`consent-instrument.schema.yaml:7`) to stay frozen, matching Q4's ruling ("`$id` unchanged")? [Gap, Spec FR-004, Schema line 7, Clarifications Q4] — **FINDING:** no FR mentions `$id` at all. Q4's ruling explicitly confirms `$id` frozen and task T016 (feature `tasks.md`) checks it by diff, but the requirement is absent from spec.md's Functional Requirements — the gate exists only at the task level, not the requirement level.
- [ ] CHK024 Does any FR require `contracts/manifest.yaml`'s `consent-instrument` row's own `schema_version: 1` field (`contracts/manifest.yaml:2041`, confirmed present and distinct from both the schema's `contract_schema_version` and the record envelope's `const: 1`) to stay frozen, matching Q4's ruling on that third fact? [Gap, Spec FR-004/FR-031, Manifest line 2041, Clarifications Q4] — **FINDING:** three DIFFERENT fields all named "schema_version"-adjacent exist across this family (`contract_schema_version` in the schema file, the record envelope's `schema_version: const: 1`, and the manifest row's own `schema_version: 1` field) and Q4 rules all frozen except the first; FR-004 addresses only the first two. The manifest row's `schema_version: 1` is untouched by FR-031 (which only names `contract_bundle_version`, the row's `sha256`, and `consumption_rule` as the three things that move) — so its frozen status is correct by omission from FR-031, but is never affirmatively STATED anywhere in the Functional Requirements the way Q4's ruling states it.
- [x] CHK025 Does FR-031 correctly enumerate ONLY the three manifest-row fields that DO move (`contract_bundle_version`, the row's `sha256`, and the appended `consumption_rule` paragraph), implicitly confirming by omission that the row's `schema_version: 1` field is not among them? [Conformance, Spec FR-031, Manifest lines 2038–2054]

## The Three Mandated In-File Comments

- [x] CHK026 Does FR-004 require the new version-bump comment to follow "the style of the existing `1 -> 2` note" — and does that existing note (`consent-instrument.schema.yaml:9–13`) in fact contain the three elements FR-004 requires (what grew, that it is ADDITIVE, that the envelope's `schema_version` stays `const: 1`), confirming FR-004's precedent citation is accurate? [Conformance, Spec FR-004, Schema lines 9–13]
- [x] CHK027 Does FR-005(a) require the sibling comment to record "why the array is a SIBLING (ruling D9's closure argument)", matching ratified task 2.4's citation of "ruling D9's closure argument"? [Conformance, Spec FR-005, OpenSpec tasks.md 2.4]
- [ ] CHK028 Does FR-005(a) preserve BOTH citations task 2.4 gives for the sibling comment — "ruling D9's closure argument, design C-1" — or does it drop the "design C-1" citation, naming only ruling D9? [Fidelity, Spec FR-005, OpenSpec tasks.md 2.4] — **FINDING:** FR-005(a) reads "why the array is a SIBLING (ruling D9's closure argument)" — it cites only ruling D9, dropping task 2.4's second citation "design C-1". The substantive content (custody's closure forces the sibling) survives, but the FR text is a strictly narrower citation than the ratified task's own.
- [x] CHK029 Does FR-005(b) require the comment to record that `ruling_ref` is "a DECLARED POINTER the validator does not resolve", matching ratified task 2.4's identical language and the schema's own existing precedent for declared-pointer fields (`dependent_refs[].ref`, `consent-instrument.schema.yaml:262–274`, "A DECLARED POINTER, never resolved by this validator")? [Conformance, Spec FR-005, Schema lines 262–274]
- [x] CHK030 Does FR-005(c) require the comment to name the MEASUREMENT ("every OpsxFactory locator carries an `opsx:opensoft/` scheme prefix; three of four targets resolve at no ref under their literal path"), matching ratified task 2.5's identical measurement, rather than leaving the comment's factual content unspecified? [Conformance, Spec FR-005, OpenSpec tasks.md 2.5]
- [x] CHK031 Does FR-005(c) require the comment to state all FOUR facts task 2.5 names — locator is opaque/not a path, resolution runs through the declared custody store mapping, the two legs are evaluated on opposite sides of the commit, and an archive move is unadmittable without the pair — or does it drop any of the four? [Completeness, Spec FR-005, OpenSpec tasks.md 2.5]

## The D9 Sibling Argument

- [x] CHK032 Is "ruling D9's closure argument" (FR-005a) traceable to an ACTUAL existing comment in the schema file — the "CUSTODY IS A POINTER" block (`consent-instrument.schema.yaml:32–35`, citing "ruling D9") — confirming FR-005 does not invent a new ruling label with no textual anchor? [Traceability, Spec FR-005, Schema lines 32–35]
- [x] CHK033 Does the ratified delta's own text supply the closure argument FR-005(a) must summarize — that `custody` "whose closure exists so that no property can hold the signed original's content" (delta lines 21–22) is exactly why the new record must live in a sibling rather than inside `custody` — so FR-005(a)'s one-line citation has a traceable, substantive origin rather than being a bare label? [Traceability, Ratified delta lines 18–22]
- [x] CHK034 Is the "sibling, never inside `custody`" placement rule stated as a MUST for the SCHEMA's shape (FR-001: a top-level property, not a `custody` sub-property) consistently with the ratified delta's own MUST ("the instrument SHALL record that fact in a SIBLING of `custody`... and never inside `custody` itself", delta lines 18–20)? [Consistency, Spec FR-001, Ratified delta lines 18–20]

## Boundary With § 3/§ 4 (no schema-requirement leakage or gap)

- [x] CHK035 Does FR-001–005 stop at the SCHEMA layer and leave the chain-linkage, rewritten-pin and WITHHELD checks to § 3 (FR-010–016), so no § 2 FR duplicates or contradicts a § 3 FR's validator-level obligation? [Consistency, Spec FR-001–005 vs FR-010–016]
- [x] CHK036 Does FR-016 (the `walk_strings` extension, a § 3 validator requirement) correctly depend on the ENTRY SHAPE FR-001/FR-002 define — walking "the whole entry minus the two digest fields" presupposes exactly the ten named fields FR-001 requires, with no field FR-016 references left undefined by FR-001/002? [Consistency, Spec FR-001/002/016]

---

## Evaluation — 2026-09-09

**Tally**: 31 passed / 5 unticked / 0 dispositioned (total 36).

### Findings (unticked items)

1. **CHK013** — no FR carries forward the ratified delta's governance consequence that a new `diff_class`/`reason` member is itself a contract change, not an author-coined string.
2. **CHK015** — FR-001 never states that `custody_rederivations` must NOT be added to the schema's own top-level `required:` array; the additive posture rests entirely on FR-004's adjective and an Acceptance Scenario.
3. **CHK023** — `$id` frozen (ruled at Q4) has no landing FR; gated only at the task level (T016).
4. **CHK024** — the manifest row's own `schema_version: 1` field (`contracts/manifest.yaml:2041`, distinct from `contract_schema_version` and the record envelope's `const: 1`) frozen (ruled at Q4) has no landing FR; correct by omission from FR-031 but never affirmatively stated.
5. **CHK028** — FR-005(a) drops task 2.4's second citation ("design C-1"), naming only ruling D9.

CHK023 and CHK024 are the schema-specific restatement of requirements.md's
CHK014/CHK046 finding, viewed here against the actual current byte locations
of the three schema-version-adjacent fields rather than against the
Functional-Requirements text alone.
