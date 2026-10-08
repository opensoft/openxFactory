# Analysis: Neutral resolved council protocol

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md) · **Tasks**: [tasks.md](tasks.md) · **Date**: 2026-10-08

This is the `speckit-analyze` record for feature 035 and the disposition of every finding. The constitution says analyze "MUST report no critical findings before implementation begins", and that findings are "dispositioned, not ignored".

Each round was run by an independent, read-only reviewer that edited nothing. The fixes were made by the plan writer, in the feature files and in this feature's own README lines only. Nothing under `openspec/changes/renew-resolved-council-protocol/` was edited.

## Round 1

**Scope.** All ten feature files at the content of `4eeb708c`, the constitution, the governing packet and its ratification record. The reviewer also compared them with codexFactory 049 at `origin/main` `3d5c2c38` (tasks, interfaces and the commission, packet, signing and seat-resolution sources) and with the Hermes H1–H4 design, the 025 spec and the Hermes sources.

**Verdict.** 3 CRITICAL, 13 HIGH, 18 MEDIUM and 6 LOW. Implementation may not begin.

**Dispositions.** Each finding is one of the following:

- **FIXED**: changed in the feature files;
- **RESOLVED**: settled by Brett Heap's rulings of 2026-10-08;
- **SATISFIED**: the precondition now holds;
- **RECORDED**: accepted as stated, with its follow-up named.

Each finding's text describes the artifacts as that round saw them, including their task numbers at the time. Each disposition cites the current task numbering.

### Critical

| ID | Finding | Disposition |
|---|---|---|
| C1 | Principle IV, "New documents MUST be linked into the README document index", was deferred to T054 and T062. The runbook was linked twice, and no planning document was linked. | **FIXED.** `README.md` now has a document-index entry for 035 that links every planning document, including this one and `clarify-questions.md`. This feature's own sentence in the OpenSpec Records block is updated, and nothing else in that shared block is touched. Every later document is linked in the PR that creates it: `evidence.md` at T001; the family README at T004, also in the `contracts/README.md` native index as pending; the runbook once, at T062. The cut (T072) only changes the family's rows from pending to registered. See plan Constitution Check row IV. |
| C2 | The constitution says "material ambiguities MUST be resolved before planning", yet four questions were left open, and spec.md:95 said "The scope contains no new unresolved policy decision". | **RESOLVED.** Five questions, OPEN-1 to OPEN-5, were put to Brett Heap on 2026-10-08, and he ruled all five that day, first-hand, choosing the recommended option of each. The record is brett-wip `lanes/log/codeXfactory-2.md`, RULED at 19:24:21Z and 19:24:59Z. The rulings are recorded in [clarify-questions.md](clarify-questions.md) and encoded in [spec.md § Clarifications](spec.md#clarifications), with a dated note on the Assumptions sentence. Research R5, R7, R12, R13 and R15 and the plan state each as decided. The deviation is recorded as closed in plan § Complexity Tracking. No implementation began before the rulings. |
| C3 | Principle VII: legacy `in_use` and historical records passed bytes this family never verified, and recognition rule (a) matched almost any kind-less object. | **FIXED.** Classification now runs first at every boundary, from Phase 1 (data-model E1; R10). A legacy record under a replacement selection is refused (`legacy_protocol_refused`). Under a legacy selection, offline, or in `--historical` mode, it is routed to the legacy verifier: the validator exits 3, which is never a pass, with the finding `legacy_protocol_routed`. Recognition rule (a) now requires a `council_convening` block, and the rules apply only to records with no `protocol`. Vectors: T009; tests: T006, T010, T057 and T059. |

### High

| ID | Finding | Disposition |
|---|---|---|
| I1 | The gate-rules council's candidate and its `rule_facts`, read from the rule packet at `subject_pin`, were not expressible. | **FIXED.** `candidate` gains an optional `subject_path`, and a fact source `candidate_subject` reads `rule_facts` from it at `candidate.head_sha`. R6 maps the gate-rules candidate onto D1's shape: its pull number is the dispatch's `candidate_pull_number`, which 049 T011b already reads. The change is recorded as a consumer impact, and T025 and T026 carry gate-rules positives. |
| U1 | The class-binding inputs (repository and head ref) were absent, so the consumer could not reproduce class selection. | **FIXED.** The provenance carries `class_inputs`. The projection carries an ordered `class_selector`, with the governed envelope's glob grammar restated in data-model E3. A declared class that was not selected is `class_mismatch`. Tests and vectors: T025 and T026. |
| U2 | One `governed_rule` pinned one file, while 049 builds the projection from four governed inputs. `blob_sha256` was a raw-byte digest under a git-blob name. | **FIXED.** `governed.sources` lists every file (with `sha256`) and directory listing (with `tree_id`) at one revision. Authority, digest and currency checks apply to each source, in path order (data-model E2 step 5; R7). |
| A1 | No normative check order, so "a different refusal is a disagreement" could not be met. Several codes were reachable only through the schema, and some refusals were written with "or". | **FIXED.** Each boundary has one evaluation order, and the first failing check wins (data-model E2, E4, E7, E8, E10 and E11; R21). Schemas do not check a condition that has a named semantic code. `opaque_conclusion` and `completion_set_mismatch` are redefined so that each can fire. No expected outcome names two codes. Multi-defect vectors pin the order (T025, T042). |
| I2 | E7 and E8 carried no presented context, so the three cross-context codes could not be told apart. | **FIXED.** Both records carry the presented `context`. The verifier rebuilds the expected context from frozen state and compares it member by member before verifying the signature. Each differing member names one code. |
| I3 | Root-authorization members made a record legacy under recognition rule (c), contradicting `root_authorization_refused` and the spec delta. | **FIXED.** Classification step 1: a record carrying `protocol: xfc-resolved-council-1` is a replacement record whatever else it carries, and root-authorization members on it are `root_authorization_refused`. Vectors: T006 and T009. |
| I4 | The legacy status effects applied to any legacy-classified record, whatever the side selected, contrary to D5. | **FIXED.** The data-model E1 effects table is keyed by the side's selected protocol. A legacy record under a replacement selection is always refused. |
| G1 | Coverage, notes and the vocabulary were not phase-scoped. Phase 1 had no boundary or handler, and no task after the first extended `refusal_code`. | **FIXED.** Coverage is checked against the vocabulary as landed at the commit: refusal codes, finding codes and the index's `coverage_floor` (R16). Phase 1 has the `definition` and `classification` boundaries, with handlers in T019. T028, T038, T046, T053 and T060 extend the enumerations. The predicate-registry note joins the gate's assertion in Phase 2 (T032). |
| G2 | Phase 7 flipped the registry with no failing test first. | **FIXED.** T067 updates `test_protocol_registry.py` to the minor before T069 flips the registry. |
| I5 | #1267 had to land before PR-1. | **SATISFIED and FIXED.** #1267 landed as `80f47483` on 2026-10-08, which is an ancestor of `origin/main`. This branch merged `origin/main` with no rebase. The tasks and plan record the precondition as satisfied, and add a second one: #1268, which carries the 2026-10-03 allocation notes under `openspec/changes/`, lands in its own Rule 6 window before PR-1 opens. Each phase is then its own branch from `origin/main`. |
| I6 | E10's subject rules refused GitHub's documented subject customization, and the issuer constant refused an enterprise issuer. | **FIXED.** E10 carries `subject_claim_keys` and parses the template against them. A customized template, including the `job_workflow_ref` key, is legal. Conflation is judged by meaning: a bare workflow reference as the template, or permitted workflows matched against `sub`. The enterprise issuer form is accepted. Tests: T050. |
| A2 | The plan settled the predicate-identifier tension with the Goals itself, instead of asking. | **RESOLVED** by OPEN-5, "Keep the existing names (Recommended)" (R5; plan row I). |
| I7 | The vocabulary was claimed to map one-to-one onto 049's refusals, but it maps many-to-one. | **FIXED.** The data model states that the mapping is many-to-one and that 049 refines its refusals at T010 and T020. The change is listed in provider-interface § Consumer impacts. |

### Medium

| ID | Finding | Disposition |
|---|---|---|
| I8 | `relative_path` was stricter than 049, `changed_paths` had no item bound, and `packet_refs` "as today" was not today's rule. | **FIXED.** `relative_path` now follows 049's rules exactly, so `\` and C1 characters are legal. The one tightening, 4096 bytes, is disclosed with its producer impact. `changed_paths` is bounded at 6000 and the counts at 3000. `packet_refs` says it is not the legacy rule. |
| I9 | The challenge had no `key_fingerprint`, as H3 requires. | **FIXED** (data-model E6). |
| A3 | The `governed` oracle encoded only one OPEN-3 option. | **RESOLVED and FIXED.** The ruled option is encoded: a `governed_history` oracle for first-parent membership, tip values per source, and the closed `workflow_revision_rule` value `equals_governed_revision`. |
| U3 | Unruled ceilings would have landed unbounded. | **RESOLVED.** The ceilings are ruled: 21600 seconds for an assignment and 600 seconds for a challenge. Vectors sit at the ceiling, one second above it, at zero and at a negative lifetime (T035, T036, T042, T044). |
| I10 | A warn code sat in the refusal coverage rule. | **FIXED.** `finding_code` is a separate closed enumeration with its own coverage rule. Outcomes are `accept`, `refuse`, `warn` and `route`. |
| I11 | E5 used `cross_convening_context`, a Phase 4 code. | **FIXED.** An assignment whose convening members differ from the snapshot's is `assignment_set_mismatch` (Phase 3). |
| U4 | Only legacy vectors carried a `registry_status` override. | **FIXED.** Every vector whose outcome reads a status must carry one, and the validator enforces it (`council-convening-vector-registry-status-missing`; T008). |
| G3 | Phase 8 refreshed no manifest rows, and per-file `contract_schema_version` was undecided. | **FIXED.** T082 refreshes every changed row, as Phase 8's last edit. Per-file `contract_schema_version` stays `1`, because no schema's shape changes; the policy's own ideation-dashboard precedent is cited (R19; plan row VI). T078 asserts it. |
| U5 | E12 had no per-act rules. Broker capability was required even for rollback, a rehearsal did not have to pass before activation, and a dormant rehearsal needed `paused_at`. | **FIXED.** E12 lists seven acts with per-act required members. Activation and resume need a passing matched rehearsal and verified broker capability. A rollback needs neither. A dormant rehearsal needs no `intake`. |
| U6 | No member said what a rehearsal is. | **FIXED.** E11 carries `mode: rehearsal \| active`. |
| U7 | The principal kind was named two ways, with no derivation and no registry file. | **FIXED.** One closed `principal_kind` enumeration lives in the shared definitions (`github_oidc_job`, `governed_broker_job`). The holder's references are issued by the trusted dispatcher or the broker (D3), and this family binds and checks them. Plan row VII says "closed enumerations". |
| U8 | The expected and resolved candidates had no input. | **FIXED.** `inputs.expected_candidate` (commission) and `environment.resolved_candidate` (admission). |
| I12 | The spec said the work was outside a lane, and no task returned change task 2.2's evidence. | **FIXED** for the feature files: spec.md carries a dated note, and T002 records 2.2's evidence on the change in its own governance commit. The packet-side part is open; see N10. |
| G4 | The foundation vectors came after implementation, and no phase after Phase 1 had a failing CLI test. | **FIXED.** T009 precedes the implementation. CLI test tasks: T010, T027, T037, T045, T052 and T059. |
| U9 | R11 did not pick a representation, or note the cost floor and the entry digest. | **FIXED.** The payload is the whole checked entry, and non-integer quantities are `decimal_string`. Integer minor units are rejected, with the reason. The cost-floor impact is recorded. |
| G5 | Phase 1 widened `SUBJECTS` but did not name the two validators that consume it. | **FIXED.** T014 and quickstart step 4 run `validate-signed-execution-chain.py` and `validate-clearing-dispatch.py`. |
| I13 | The secret floor missed four patterns 049 detects, and 049 missed one of the floor's. | **RECORDED.** Both gaps are stated in R9. 049 adds the assignment detector (a consumer impact). Widening the floor changes every domain-factory scan, so it is not done in passing: T033 measures it and files it as its own follow-up. |
| U10 | The seed check caught every digest, the path check had no base, and the gate had no push trigger. | **FIXED.** The seed check is keyed by member name (T043). The scope check runs against the PR's own merge base (quickstart step 5). The gate runs on push to `main` too (R17; T011). |

### Low

| ID | Finding | Disposition |
|---|---|---|
| I14 | R19 said two entries target `contract-v5.0`; the policy lists three. | **FIXED.** R19 and T080 name all three. |
| I15 | "T032–T034" and "T033 and T034" disagreed, and "T066 done" named an owner box that stays unticked. | **FIXED.** Both now read "a prerequisite of T033 and T034" (049's ids), and the dependency is "T075's dated evidence recorded". |
| U11 | Empty area directories would need placeholder files. | **FIXED.** Each area directory is created with its first vector. |
| A4 | "Frozen ratified set" overstated what was ratified. | **FIXED.** The closure check is "against the set as landed at this commit". The family README cites the five rulings (T004). |
| U12 | The known answers came from the code that adjudicates them. | **FIXED.** `derived_origin: hand` marks hand-authored answers, and T007 pins one RFC 8785 known answer. |
| I16 | Plan row VI did not record the manifest-row precedent. | **FIXED.** Row VI cites it. |

## Round 2

**Scope.** The same files after the round-1 fixes and the encoding of Brett Heap's five rulings, plus `clarify-questions.md`. Read at openxFactory `origin/main` `80f47483`, codexFactory `origin/main` `2ce8544e`, xFactory `origin/main` `651dd5c9`, and the brett-wip register clone. The reviewer checked the five ruling labels against the RULED lines word for word.

**Verdict.** 0 CRITICAL, 2 HIGH, 9 MEDIUM and 13 LOW. The constitution's analyze gate is met. Of the 40 round-1 findings, 34 were verified as fixed, 5 as partly fixed (I1, A1, I10, G3, I12) and 1 as not fixed (U1). Each partial is closed by the round-2 finding named beside it below.

| ID | Sev | Finding | Disposition |
|---|---|---|---|
| N1 | HIGH | `class_inputs.head_ref` was never authenticated, so a producer could still cite a head ref that selects a lighter class (U1 not fixed). | **FIXED.** E2 step 4 requires `class_inputs.head_ref` to equal the head ref read by the trusted gather at commission and by the consumer at admission (`environment.head_refs`); otherwise `candidate_mismatch`. Test and vector: T025, T026. |
| N2 | HIGH | The workflow-revision rule compared the governed repository with the caller, which refuses the estate's own pattern: xFactory's `council-convening-lane.yml` calls codexFactory's `council-lane-reusable.yml`. | **FIXED.** The rule compares the governed repository with the repository named in the verified `job_workflow_ref`, whose commit `job_workflow_sha` is (data-model E10; R7). The caller pattern is accepted (T050). The remaining refusal, of a permitted workflow outside the governed repository, is a case the ruling does not address, so it is flagged for confirmation below rather than claimed as adding nothing. |
| N3 | MED | A `tree` source's id changes on any code edit in the rule directory, so admission would refuse on unrelated changes. Applying OPEN-3 to every source went beyond the ruling's words. | **FIXED, and confirmation requested.** A directory is now a `listing` of the files with named suffixes directly inside it, each also a `file` source, which is exactly what 049's `read_directory` reads. The every-source reading stays, as the fail-closed default, and is flagged below. |
| N4 | MED | The gate-rules council has no class, but E2 required one (I1 partial). | **FIXED.** The projection declares each council classed or unclassed. `class_inputs` and `matched_class` are present exactly for a classed council; anything else is `class_mismatch`. Gate-rules vectors: T025, T026. |
| N5 | MED | Several codes had no step or input role: `assignment_malformed`, `challenge_malformed`, `convening_conflict` and the E12 codes (A1 partial). | **FIXED.** `assignment_malformed` is E4 step 3; `challenge_malformed` is in E7 step 6, over `environment.issued.challenges`; `convening_conflict` is E2 step 14; E12 has an activation order with a new `activation_evidence_malformed`. |
| N6 | MED | A route carried two findings in a single `finding` member, and `warn` could never occur (I10 partial). | **FIXED.** `expected.findings` is an ordered list, and the corpus has no `warn` outcome. |
| N7 | MED | Classifying every record made `check` refuse registries and evidence as `protocol_unknown`. | **FIXED.** Classification applies to the protocol-carrying kinds (E2, E4–E8) and to records with no family `kind`. Other kinds are judged by kind (data-model conventions; validator-cli `check`; T010). |
| N8 | MED | Binding read an E2 record before it was classified or shape-checked, and R21 said every order begins with classification. | **FIXED.** At admission, binding runs between E2 steps 2 and 3. R21 now says which orders begin with classification. |
| N9 | MED | Phase 4 generated signing vectors before the generator could sign, and the generator was checked only against itself. | **FIXED.** Signing lives in the T020 generator, and T048 no longer adds it. T042 and T044 add hand-authored signed-bytes answers for one registration and one return context. |
| N10 | MED | #1268 carries three edits under `openspec/changes/renew-resolved-council-protocol/` (`implementation-handoff.md`, `proposal.md` and `tasks.md`). They are 2026-10-03 allocation notes from the specifying session, including a `Status: draft` to `Status: record` flip, and they now read as stale. The round-1 disposition of I12 wrongly said they were left untouched. | **OPEN, for the coordinator.** The plan writer neither authored nor changed them, and its brief forbids editing that directory. The choice is to restore `main`'s bytes for the three files or to add dated corrections, and either needs an edit there. T002 now says the change's owner lane is this lane. |
| N11 | MED | `repository_identity_unknown` could not be decided, because the identity file has one row. | **FIXED.** A spelling the file does not list is taken as current. The code becomes `repository_identity_mismatch`: a verified `repository` or `repository_id` claim that differs from the binding. |
| N12 | LOW | Exit 3 was called this family's addition. | **FIXED.** validator-cli cites `validate-consent-instruments.py`'s `EXIT_NEEDS_DECISION = 3` (ruled 2026-09-09). It says exit 3 comes from `check` only, and that the self-test exits 0 on correctly adjudicated route vectors. |
| N13 | LOW | Phase 8 refreshed a manifest row the regression inventory does not have, before the file was rewritten. | **FIXED.** T082 is Phase 8's last edit, and it says the inventory has no row. |
| N14 | LOW | "Closed at every depth" contradicted the open `payload`, which was unbounded. | **FIXED.** `payload` is named as the one open object and bounded at 1 MiB of canonical bytes. The bound is a plan choice made for H1's "bounded inputs". |
| N15 | LOW | The "verification step" conflation case could not be probed by data, the code for an unparseable template was missing, and the claim-key list was unverified. | **FIXED.** The data-probeable form is a vector whose `sub` contains a permitted reference while `job_workflow_ref` does not (`workflow_not_permitted`). An unparseable template is `subject_template_mismatch`. The key set is enumerated at T053 from GitHub's OIDC reference. |
| N16 | LOW | E8 named no code for a differing context `key_fingerprint`. | **FIXED:** `return_key_mismatch`. |
| N17 | LOW | E1 and E11 disagreed on whether a `historical_only` legacy selection is refused only when active. | **FIXED.** It is refused in either mode. |
| N18 | LOW | The spec delta's "key transport MUST refuse" had no vector. | **FIXED.** Registration and return refuse private-key members and PEM private-key blocks (E7 and E8 step 3 and step 2; T042). |
| N19 | LOW | `selection_sha256` could never match across sides, and `rehearsal_ref` had no lookup. | **FIXED.** Each side carries its E11 record, and the two are compared on the five matched values. `rehearsal_ref` resolves through `inputs.rehearsal`. |
| N20 | LOW | Task ranges disagreed across files, and round-1 numbering was unmarked. | **FIXED.** The plan lists the exact tasks, and this record says which numbering each column uses. |
| N21 | LOW | R7 quoted the RULED line's description as Brett Heap's words, and the checklist was stale. | **FIXED.** R7 and spec.md attribute the description to the RULED line. The checklist carries a dated note. |
| N22 | LOW | "Admitted governed source for that council" had no council in the oracle key. | **FIXED.** `rule_unauthorized` means not an admitted governed source of an allowlisted governed repository. Council admission is step 6's `council_unknown`. |
| N23 | LOW | The challenge-ceiling vectors would bind 049, whose pre-check allows 3600 seconds. | **FIXED.** They carry `applies_to: [consumer]`, because the consumer issues challenges (R12; T044). |
| N24 | LOW | "Run red" could put red commits on a pushed branch. | **FIXED.** Red runs stay local; each phase pushes tests and implementation together. |

## Round 3

**Scope.** A verification pass over the round-2 dispositions and the edits they made, at the same refs. The reviewer re-checked the ruling labels against the RULED lines, every link and anchor (0 broken), every cited task id, and every cited evaluation-order step.

**Verdict.** 0 CRITICAL, 2 HIGH, 6 MEDIUM and 9 LOW new findings. The constitution's analyze gate holds. Of N1–N24, 20 were verified, 3 were partly fixed (N8, N15, N19), and N10 remained open, with its disposition judged accurate. The two confirmations were judged honestly framed: each is a fail-closed default awaiting Brett Heap, and neither is presented as his ruling. Every finding below is fixed in this revision.

| ID | Sev | Finding | Disposition |
|---|---|---|---|
| R3-H1 | HIGH | `subject_workflow_conflation` could never fire, because a bare workflow reference fails the parse check, which ran first (introduced by the N15 fix). | **FIXED.** In E10, conflation (step 5) now runs before the parse check (step 6). A bare workflow reference is defined by grammar: the `<owner>/<repo>/.github/workflows/<file>@<ref>` shape with no `key:` element. |
| R3-H2 | HIGH | Nothing compared the verified `iss`, `aud` and `sub` with the binding, or checked the token's validity window, contrary to D3's "the consumer verifies signed issuer/audience/expiry". Registration had the same gap. | **FIXED.** E10 has an offline half (steps 1–6) and a claim half (steps 7–15), with new codes `claims_expired` and `audience_mismatch`. E7 step 5 applies the claim half to a seat job against its holder's binding. Tests: T050, T042. |
| R3-M1 | MED | The step-4 head-ref check depended on whether a council is classed, which is known only at step 6. A record with only one of `class_inputs` and `matched_class` had no step. | **FIXED.** Step 4 checks `class_inputs` whenever the record carries it; a half-present pair is `convening_malformed` at step 2; step 6 judges presence against the projection. |
| R3-M2 | MED | `rehearsal_ref` hashed "the bytes" of an object embedded in a vector, which has no defined bytes. | **FIXED.** `inputs.rehearsal` carries the record's exact UTF-8 text as a JSON string, and the hash is over those bytes. |
| R3-M3 | MED | Phase 5 could land before Phase 4 but used `claims_unverified`, a Phase 4 code. | **FIXED** in the other direction. Registration now uses the binding's claim checks, so Phase 4 depends on Phase 5. The landing order is 1, 2, 3, 5, 4, 6, and the claim codes are introduced in Phase 5 (plan; tasks; data-model § Refusal vocabulary). |
| R3-M4 | MED | No task wired binding into admission or updated the Phase 2 admission vectors when it arrived. | **FIXED.** T051 re-authors those vectors with a passing binding and adds combined-defect vectors. T055 runs binding inside the admission handler. |
| R3-M5 | MED | Full equality with `inputs.expected_candidate` could not hold, because the merge-readiness trigger names only `repository` and `pull_number`. | **FIXED.** The candidate must agree with the expected candidate on the members the trigger names. |
| R3-M6 | MED | `historical_reinterpretation_refused` had no data trigger. | **FIXED.** A rollback carries `new_records_protocol`, which must be the replacement; `new_records_retained: false` is `activation_evidence_incomplete`. |
| R3-L1 | LOW | Two leftover order statements contradicted binding-inside-admission and the secrets step. | **FIXED** (provider-interface; data-model E2 step 3). |
| R3-L2 | LOW | T002 told the lane to tick 2.2 under `openspec/changes/`, against "No task edits" that directory. | **FIXED.** T002 reports the evidence; ticking is the lane's governance act outside the feature's tasks, as T086's is. |
| R3-L3 | LOW | The every-source reading was stated without its pending-confirmation flag in four places. | **FIXED** (plan; provider-interface; conformance-corpus; data-model E2 step 5). |
| R3-L4 | LOW | Confirmation 1 left out its cost, and R7's "never refuses on unrelated movement of main" was too strong. | **FIXED.** The governed sources include `hermes/domain/agent-mixes.yaml`. 57 codexFactory commits touched those YAML sources between 2026-09-01 and 2026-10-08, measured by `git log` on its `origin/main`. R7 and the confirmation state the trade-off. |
| R3-L5 | LOW | Confirmation 2 did not name the reading it rests on. | **FIXED** (below; data-model E10). |
| R3-L6 | LOW | Several schema types would catch conditions that have their own named codes. | **FIXED.** The data-model conventions name each one and the step that checks it. |
| R3-L7 | LOW | The payload size check ran before canonicalizability, though size is measured in canonical bytes. | **FIXED.** E8 step 2 checks canonicalizability first. |
| R3-L8 | LOW | A listing entry that is not also a `file` source had no code. | **FIXED:** `convening_malformed` at E2 step 2. |
| R3-L9 | LOW | The former-spelling check missed the one transferred repository, which appears in `job_workflow_ref` and `governed.repository`. | **FIXED.** E10 step 4 checks every permitted `job_workflow_ref` repository. A former spelling of `governed.repository` is not allowlisted, so it refuses as `rule_unauthorized`. |

## Round 4

**Scope.** A verification pass over the round-3 fixes at the committed head `d330d4b5c`, with codexFactory read at `origin/main` `0fa88fb0` and `2ce8544e` and xFactory at `651dd5c9`.

**Verdict.** 0 CRITICAL, 3 HIGH, 6 MEDIUM and 4 LOW new findings. The analyze gate holds. Of the 17 round-3 fixes, 13 were verified and 4 were partly fixed (R3-H2, R3-M4, R3-L6, R3-L9). Each partial is closed by the round-4 finding named beside it below. Every finding below is fixed in this revision.

| ID | Sev | Finding | Disposition |
|---|---|---|---|
| R4-H1 | HIGH | E7 step 5 reused E10 steps 7 to 13 only, so the seat job's workflow commit was never checked at registration, though D3 requires "permitted reusable workflow/ref/sha". Applying the commission rule as written would refuse 049's seat worker whenever `main` moved. | **FIXED, and confirmation requested.** E7 step 5 now runs E10 steps 7 to 15 with operation `seat_execution`. The closed `workflow_revision_rule` gains a second value, `on_governed_history_since_revision`: the seat commit must be on the governed first-parent history, at or after the frozen revision. That applies the ruling's "history" half to seats, and is confirmation 3 below. |
| R4-H2 | HIGH | Binding step 14 read the record's `governed` member before E2 step 5 had checked it, so a former spelling or a mutable revision refused under the wrong code. | **FIXED.** Admission interleaves the boundaries: E2 steps 1–2, E10 steps 1–13 and 15, E2 steps 3–5, E10 step 14, then E2 steps 6–14 (data-model E2; R21). |
| R4-H3 | HIGH | Nothing checked the listed governed sources against the set the projection was built from, so an omitted source escaped the currency test. | **FIXED.** E2 step 5 adds `governed_sources_mismatch` (Phase 2). The `rules` oracle returns the source set, and each adapter reports the set it read. Vectors: T025, T026. |
| R4-M1 | MED | Phase 3's admission vectors land before Phase 5 inserts binding into admission. | **FIXED.** Phase 5 lands after Phases 2 and 3, and T051 re-authors every admission vector at that commit. |
| R4-M2 | MED | Shared admission vectors carrying a binding would force 049 to implement the consumer's OIDC checks. | **FIXED.** Shared resolution vectors use boundary `commission`; admission vectors are `applies_to: [consumer]` (T026). |
| R4-M3 | MED | `holder.binding_ref` resolved against nothing, the holder's binding was never shape-checked, and a broker holder had no binding shape. | **FIXED.** E10 gains `binding_id`; `inputs.bindings` holds the instances; `binding_unresolved` is new (Phase 5); E7 step 5 runs E10 steps 1–6 on the resolved binding; a `governed_broker_job` holder is `broker_capability_insufficient` until a broker shape exists. |
| R4-M4 | MED | Verified claims and broker capability each had two homes, and step 15 was misdescribed. | **FIXED.** Claims live only in `environment.identity`, and broker capability only in the binding's `broker` member. The binding's input roles are named, and steps 1–6 and 15 are its offline half. |
| R4-M5 | MED | Nothing tied the passing rehearsal to the activation it backs. | **FIXED.** E12 step 2 requires the rehearsal's provider and five matched values to equal the activation's (T057). |
| R4-M6 | MED | "No task waits on an open question", yet two confirmations gated PR-2 and PR-5 with no task. | **FIXED.** tasks.md names the three confirmations and the tasks that record them: T034, T049 and T056. |
| R4-L1 | LOW | The list of binding codes reused in Phase 4 was incomplete, and the boundary column too narrow. | **FIXED** (data-model § Refusal vocabulary). |
| R4-L2 | LOW | The schema-type convention left out several members, and E12 step 2 did not name `new_records_retained: false`. | **FIXED.** |
| R4-L3 | LOW | Out-of-order or repeated sources, unsorted listing entries and a repeated `fact_sources` contract had no code. | **FIXED:** `convening_malformed` at E2 step 2. |
| R4-L4 | LOW | The churn figure, 57 commits, counted all history, while only first-parent movement supersedes a source. | **FIXED.** The first-parent count is 34, about 0.9 a day, measured with `git log --first-parent --since=2026-09-01 --until=2026-10-08T00:00:00 2ce8544e -- hermes/domain/agent-mixes.yaml 'scripts/merge_master/*.yaml' 'scripts/merge_master/*.yml' .github/merge-approval-envelope.yml` in codexFactory. The round-3 row above keeps its original figure as history. |

### Confirmations requested

Three applications of the OPEN-3 ruling go beyond its words. Each is the plan's fail-closed default, and each is flagged for Brett Heap's one-line confirmation before the phases that implement it land. None is presented as his ruling.

1. **The currency test covers every governed source, not only the rule file** (R7; data-model E2 step 5).
   - **The sources.** For 049 they are the council profile `hermes/domain/agent-mixes.yaml`, the council document, the rule directory's YAML files and their listing, and the envelope configuration. Each contributes to the projection, so a changed council document or envelope configuration at the tip would otherwise seat an outdated roster.
   - **The cost.** Admission refuses whenever any of those sources moved on the governed branch's first-parent line between commission and admission. 34 first-parent codexFactory commits touched them between 2026-09-01 and 2026-10-08, about 0.9 a day, against a window of minutes. A refused convening is convened again.
   - **Affects** Phase 2: record the answer at T034, before PR-2 lands. If he prefers the narrower reading, Phase 2 checks currency on the governing rule file alone.
2. **A permitted workflow whose repository is not the governed repository is refused** (data-model E10).
   - **The reading it rests on.** The ruling's "producer repository" is read as the repository of the producer's code, which the verified `job_workflow_ref` names. E10's own `producer_repository` member is the calling repository. For the estate's pattern (xFactory's lane calling codexFactory's `council-lane-reusable.yml`), this reading applies the ruled sha check to codexFactory's commit. The other reading would apply no check at all, because the caller is never the rule repository.
   - **The refusal.** The ruling constrains only the case where the workflow's repository is the governed repository. No consumer uses the other case today, so the binding refuses it rather than inventing a rule.
   - **Affects** Phase 5: record the answer at T056, before PR-5 lands.
3. **A seat job's workflow commit must be on the governed history at or after the frozen revision, not equal to it** (data-model E10, `on_governed_history_since_revision`; E7 step 5).
   - **Why not equality.** A seat job runs after admission, and 049's seat worker checks its tooling out from the default branch. So equality would refuse every seat job that ran after `main` moved.
   - **Why the history test.** It still refuses a seat commit that is off the governed history or older than the commission's revision. It applies the ruling's "history" half.
   - **The alternative** is strict equality, which would require every caller to pin the reusable workflow to the commission's commit.
   - **Affects** Phases 5 and 4: record the answer at T056, before PR-5 and PR-4 land.
