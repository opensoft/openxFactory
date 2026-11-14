# Specification Quality Checklist: Private connectivity production qualification

Status: draft

**Purpose**: Validate specification completeness and quality before implementation planning.
**Created**: 2026-11-13
**Feature**: [Specification](../spec.md)

## Content Quality

- [x] No implementation stack, source algorithm, API design or deployment recipe is prescribed.
- [x] Focused on customer value, independent offerings and evidence-based acceptance.
- [x] Written for rollout, customer, component and domain stakeholders.
- [x] All mandatory template sections are completed.

## Requirement Completeness

- [x] No NEEDS CLARIFICATION markers remain; unselected operating values are explicitly gated decision inputs, not invented defaults.
- [x] Requirements are testable and unambiguous.
- [x] Success criteria are measurable.
- [x] Success criteria describe outcomes independently of implementation technologies.
- [x] All acceptance scenarios are defined.
- [x] Edge cases are identified.
- [x] Scope is clearly bounded.
- [x] Dependencies and assumptions are identified.

## Feature Readiness

- [x] All functional requirements have acceptance coverage.
- [x] User scenarios cover all three tracks and four offering paths.
- [x] Defined success criteria cover the required outcomes; no live outcome is claimed achieved.
- [x] Ownership names the existing product boundaries without prescribing unapproved runtime paths.

## Notes

Reviewed against the ratified production policy and its 18 requirements / 39 scenarios. [Policy coverage](../policy-coverage.md) maps the complete governing corpus to this feature's requirements and planned acceptance.

The specification, plan and task list have completed [Speckit analysis and remediation](../analysis.md). This checklist records artifact quality, not Q0 commissioning or Q1–Q5 acceptance. Missing owner/runtime scopes, platform/domain decisions, numeric objectives and target/customer approvals remain explicitly blocked at the gates in [commissioning](../commissioning.md).

The [implementation plan](../plan.md) and [single task list](../tasks.md) are drafted. No runtime edit, staging run, production canary or commercial release is recorded as complete by creating specification/plan/tasks artifacts.

## Local validation

- Feature resolution selects branch 043-private-connectivity-production and its matching specification directory.
- Content review confirms seven independently testable user stories, 30 functional requirements, eight measurable success criteria and 18 track acceptance cases. The coverage index includes every one of the 18 governing requirements and 39 scenarios.
- At the analysis checkpoint all 126 packet-relative Markdown links resolved and all 20 feature documents were linked directly from the repository README. The expanded bootstrap packet is checked below; no template placeholders or host-specific paths remain.
- The pinned OpenSpec 1.12.0 strict check passes for the governing change. Whole-corpus strict validation exits 0 with its one existing accepted add-chain-attestation finding; this is not a clean whole-corpus result or a new waiver.
- Code-surface, target-release, status-validity and duplicate-packet checks pass. At the planning checkpoint the generated 248-row sequencing ledger was consistent without an edit; the two new bootstrap rows are recorded below.
- Staged whitespace checks pass. Feature 040, runtime code, published contracts, pins and required-check definitions are unchanged.
- The optional after-specify commit hook was disabled at the specification checkpoint; those artifacts remained local then. Subsequent explicit draft publication is recorded under T001–T005 below.

## Planning validation

- Planning artifacts resolve under the same 043 feature: plan, research, logical data model, quickstart, three draft interface documents and the validation matrix.
- Research decisions R-01–R-10 are resolved at the coordinating-design level. Required execution inputs C-01–C-13 remain explicit owner decisions, never lab defaults or passed gates.
- The validation matrix has 13 proof groups covering all 30 feature requirements and retaining the complete 18-requirement / 39-scenario governing coverage.
- Constitution checks pass before research and after design for planning scope. Q0 acceptance and Q1–Q5 execution remain unclaimed.
- The managed SPECKIT agent-context block points to the plan. Other agent instructions, feature 040, runtime code, published contracts, pins, workflows and tests are unchanged.
- Local governance/strict validation outcomes retain the existing whole-corpus accepted finding; owner commands were inspected rather than run, and no live qualification is claimed.
- The generated tasks.md is the sole executable list. Speckit analysis precedes implementation, which remains gated by accepted owner scope and consumed decisions.

## Task-generation validation

- At the task-generation checkpoint the sole [task list](../tasks.md) contained 68 sequential unique tasks, all unchecked: 14 US1, eight US2, eight US3, seven US4, seven US5, seven US6, eight US7 and nine shared setup/foundation/handoff tasks. Current bootstrap completion is recorded below.
- Every task has an owner, dependencies, gate/evidence class, required cases, relative file scope, one verification command and a build tier. After analysis elevated T005, there are 67 O and one S tasks; no governed task is H. Shell syntax and inline Python verification snippets compile without running future implementation commands.
- Every dependency refers to an existing lower task ID; the graph is acyclic. Local source readiness does not depend on hosted/domain commissioning or the full Q0 join. Standalone source readiness does not require actual domain selection. Q1 joins the full commissioned/source/release set, and Q2 joins every required offering path and operational proof before Q3–Q5 decisions.
- The 68-row [acceptance registry](../contracts/task-evidence.md) exactly matches task IDs, owners, dependencies, evidence classes and required-case IDs. The future verifier is available before its consumers, while T001–T006 use existing tools. Actual named-owner acceptance precedes helper implementation; structural metadata cannot supply it.
- All 30 feature requirements map to tasks; all 13 validation groups, 18 governing requirements / 39 scenarios and six acceptance cases per delivery track remain represented. Per-offering canary observations and named offer/wave decisions remain separate, current and bounded.
- The 13 P-marked tasks have disjoint candidate write sets. Exact C-01 file-list intersections and consumed decisions still control concurrency; shared proposal/index/ledger writes are serialized. Changed owner layouts require task refinement before editing.
- At the task-generation/analysis checkpoint, governing handoff task 2.1 was complete as an artifact handoff, task 2.2 and Q0–Q5 remained open and zero implementation tasks were complete. Subsequent bounded bootstrap progress and the T006 stop are recorded below.
- Task generation changes feature/handoff documentation only. No owner runtime, workflow, published contract, pin, test or feature 040 file is modified. Repository configuration disables before/after-tasks auto-commit; subsequent explicit publication follows T003/T004 rather than those hooks.

## Analysis and remediation validation

- The [analysis report](../analysis.md) records six repaired findings: per-scope owner commissioning, authenticated bootstrap dependency evidence, independent canary/offer child DAGs, final consumer/harness compatibility closure, T005's contract/design tier and explicit success-criterion/task coverage.
- The revised packet maps all 30 functional requirements and eight buildable success criteria to tasks; range expansion leaves no unmapped task. The 68-row evidence registry matches the actual task metadata. Zero critical, high, medium or low artifact findings remain.
- T049 now depends on the full commissioning and final source/release set before T050/Q1. Local and standalone source work still lack unrelated domain/program prerequisites. The approved child-instance model preserves full Q2 and exact scoped canary/offer/wave dependencies without requiring an unrelated parent aggregate to pass.
- Local syntax/coverage/DAG/tier/parallel-write/link checks and affected governance validators are rerun against the revised packet. The existing accepted whole-corpus finding remains disclosed. These checks do not run future helpers or owner source/live commands.
- The optional before/after-analyze commit hooks were disabled; the packet was local at that analysis checkpoint. Explicit draft publication follows below. Runtime, workflow, contract/pin, test and historical 040 files remain unchanged.

## T001–T005 bootstrap implementation

- T001: feature resolution selects the existing 043 linked worktree and spec/plan/tasks; the 16-item prerequisite checklist passes. Existing Python/environment/credential and Docker ignore rules cover this documentation-only bootstrap. No new package, container, runtime or ignore-policy change is needed.
- T001: the pre-existing staged planning packet is preserved. Historical feature 040, runtime files, workflows, published contracts, pins, tests and nonmanaged agent instructions remain unchanged. Before/after-implement automatic commit hooks are disabled; explicit draft publication under T003/T004 is a separate authorized action.
- T002: the historical baseline records the current T021 content digest and original pass verdict; authorizes_production is false. It preserves the source and approved lab acceptance record without carrying forward lab limits, sign-offs or runtime authority.
- Bootstrap command outputs are retained locally pending the actual E custody/authentication decision at T006. They are not represented as accepted protected C-08 evidence by creating this record.

- T003: draft commission-private-connectivity-production-evidence is published in [PR #1310](https://github.com/opensoft/openXfactory/pull/1310), indexed and strict-valid; its generated corpus row carries that actual PR number. It proposes exact E files/commands, bootstrap/instance controls, pin registration and required CI, without owner acceptance.
- T004: draft publish-private-connectivity-production-contract is published in the same PR, indexed and strict-valid; its independently generated row also carries #1310. It reserves no version and grants no neutral scope, release cut or consumer-pin change.
- T005: the [review freeze](../contracts/task-evidence.md#t005-review-freeze) binds all 68 normalized task lines, 68 registry rows and 16 acceptance-input digests. Independent recomputation matches the recorded SHA-256; the listed T005 command passes with completed bootstrap checkboxes. All 30 FR, eight SC, 18 governing requirements / 39 scenarios and 13 proof groups remain covered.
- At the bootstrap stop, T001–T005 were complete and T006–T068 unchecked. Both proposals were draft with no origin approval metadata or ratification record; actual E acceptance and its consumed C-08 choices were still required. The subsequent T006 owner decision is recorded below. No helper, shared reader, required workflow, neutral contract or owner runtime implementation was performed.
- Current ledger: 250 rows; only the two successor rows are added by the sanctioned generator with #1310. The original 248 rows retain their provenance. Whole-corpus OpenSpec retains its accepted add-chain-attestation exception. The proposal-origin family retains two pre-existing unrelated findings in add-workload-factory-binding and honor-conditional-lane-attribution; neither successor adds one.
- Final bootstrap audit: 28 Markdown feature/successor documents and 152 relative links resolve and are indexed; all T001–T005 verification commands pass. The source/registry DAG, tier/file/command format, parallel envelopes, 38 FR/SC task mappings, historical T021 bytes, exact two-row ledger addition and review-freeze digest are independently checked. T006–T068 remain unchecked and the planned helpers/published contract directory remain absent.
- Focused regression validation: python3 -m pytest tests/sequenced_after tests/doc-health/test_pin_reachability.py tests/doc-health/test_sentinel_vocabulary.py -q reports 418 passed. Strict validation of both successor changes and the governing policy reports three passed; whole-corpus strict reports 125 passed plus its one existing accepted finding, with zero undispositioned failures. Sequencing, code-surface, target-release, status-validity, duplicate-packet and whitespace checks pass for the bootstrap packet.

## Local Codex PR review

- Reviewed PR #1310 here with the nine standard expert roles, a CI/release specialist and the coordinator. Two P2 findings were confirmed and corrected: the governing handoff now records completed analysis/T001–T005 and the T006 stop; the neutral publication scope is described as proposed until its own T016 acceptance.
- The task-generation all-unchecked statement is explicitly historical. The T005 review freeze is refreshed for the corrected evidence-contract wording. Independent QA and maintainability re-review reproduced all 16 input hashes and the new canonical digest; all 68 task definitions and registry rows are unchanged, with five tasks complete and 63 pending.
- A possible direct release-inventory membership issue was investigated and rejected using the existing manifest-registration/exact-commit publication precedent in contracts/README.md. No publication, catalog or builder scope was added.
- After the corrections, the two affected digest/census regressions pass; strict validation of both successors and the governing policy, whole-corpus strict validation with its existing accepted finding, sequencing ledger, code-surface, target-release, status-validity, duplicate-packet and whitespace checks pass. Existing unrelated proposal-origin findings remain outside this repair.
- At the local PR review checkpoint both proposals remained draft and T006 was unchecked, with no origin approval metadata or ratification record. The subsequent T006 owner decision is recorded below; all other owner scopes and full program Q0–Q5 remain pending. Hosted CI and Sonar are verified separately at the published head; hosted Codex review availability does not substitute for this local review or owner acceptance.

## T006 owner acceptance

- Brett Heap approved the reviewed E owner scope and then explicitly selected the prepared source-only Git custody policy. The owner/custody note and ratification record preserve both session decisions, the accepted nine surfaces/commands and the reviewed definition identity.
- Source-only C-08 values: Brett is custodian; reviewed/redacted evidence and approval references use exact Git commit/content identities in opensoft/openXfactory, retained for project lifetime under existing repository permissions, with SHA-256, actual GitHub run/job/output identities and owner review. Private provider/customer/live custody remains a later decision; actual bootstrap ingestion/authentication is still required at its consumer.
- T006 verification passes. T001–T006 are complete; T007–T068 remain unchecked and this pass stops before T007. The E proposal is ratified with actual origin approval metadata. Neutral publication stays draft and T016 unaccepted. Full program Q0 is unaccepted and Q1–Q5 are unentered; no helper, shared reader, workflow, contract publication or owner runtime is implemented.
- The acceptance-state freeze records supplied decisions in four input documents and preserves all 68 task/registry definitions. Its digest is independently recomputed before publication; the ratification record retains the earlier reviewed definition/source identity.
- T006 validation: 112 focused ratification/provenance/digest/pin-census regressions pass; all three scoped strict packets pass. Whole-corpus strict retains its existing accepted finding with zero undispositioned failures. The ledger remains 250 rows with zero moved rows; code-surface, target-release, status-validity, duplicate-packet and whitespace checks pass. This E packet has no provenance/origin finding; the existing 33/2 broader baseline findings remain outside it.

## T007 read-only evidence verifier

- T007's two accepted source/test paths are implemented. Its five initial closed-case/subcheck regressions fail for missing rejection behavior, then the completed exact-source suite reports 183 passed. All 68 tasks and required cases are exercised; fixtures are synthetic source tests, not rollout evidence.
- Verification requires an independently reviewed manifest anchor, immutable actual outputs and current owner decisions. Missing trust fails closed. Original bootstrap artifacts, source/receipt revision separation, scoped dependencies, child/aggregate progress, service eligibility, offer-before-wave, finite limits, monitoring omissions, managed carriers, incidents and fresh resume are covered. Actual Git-object and CLI tests verify read-only behavior.
- T001–T007 are complete. T008 inventory, T009 registration and T010 required feature CI remain pending. No real bootstrap import or production manifest is created. The unchanged 16-input/68-task acceptance freeze is reproduced by the verifier. Full program Q0 and Q1–Q5 remain unaccepted/unentered; PR #1310 stays draft.
- Affected validation: 418 existing sequencing/pin regressions pass, followed by both tracked-file pin reachability/census assertions after staging the new files. All three scoped OpenSpec packets pass; whole-corpus strict retains only the accepted add-chain-attestation finding with zero undispositioned failures. The 250-row ledger, code-surface, target-release, scoped status-validity/duplicate-packet and whitespace checks pass. Actual published-head CI and hosted Codex review are tracked separately from these source checks.

## T008–T009 continuation

- The aggregate/inventory integration repair passes T007's now-184 tests. T008's 27 tests pass, including real local/foreign Git reachability, exact ownership, explicit modes, scoped new-draft generation, immutable/tracked evidence refusal, links and byte-preserving checks.
- T009's new T010 coverage regression first fails because the registration is absent. After registration, 39 new scope/reachability cases pass and the complete affected pin/sentinel suites pass 172 tests, including the new FUTURE-population assertion. Local orphan detection, foreign proof, unknown-path refusal and feature 040 behavior remain intact. The actual standing census is unchanged at 701 sites/31 members; no production evidence is fabricated to populate it.
- T001–T009 are complete; T010–T068 remain pending. The draft bootstrap-custody proposal makes the exact durable-source/first-pin gap concrete for owner review. Its two additional records, contained-reference format and T010 file refinement remain proposed. No frozen definition/input changes are made before approval; no workflow or new evidence record is implemented here.
- The new proposal's strict check and the three existing scoped packets pass. Sequencing reports 251 consistent rows, with only the new proposal row stamped by sanctioned generation using PR #1310. Code-surface, target-release, status-validity and duplicate-packet checks pass. Required CI and hosted Codex review remain separate published-head results; PR #1310 stays draft and full Q0/Q1–Q5 gates remain pending.

## Owner-proposal and historical-authority preparation

- T007 now passes 213 source regressions and T008 passes 28; combined validation reports 241 passed. Completed execution needs an independently reviewed current evidence admission bound to original authority/output/scope, while revoked grants need exact post-run completion closure. No new operation may borrow that historical authority; new inventory generation retains current authority. The source fixes stay in their respective two-file E scopes.
- All five coordinating owner proposals and both matching D/O native packets pass pinned strict OpenSpec validation. The whole coordinating corpus reports 131 passed plus its one existing accepted add-chain-attestation finding; zero undispositioned failures. The sanctioned 256-row ledger is consistent and moves only the five new rows under actual PR #1310.
- The affected pin/sentinel suites report 172 passed, sequencing reports 286 passed, and coordinating code-surface, target-release, status-validity and duplicate-packet checks pass. Proposal-origin still reports its two pre-existing unrelated errors (add-workload-factory-binding and honor-conditional-lane-attribution); none concerns these drafts. Relative links in the 28 new proposal Markdown files resolve.
- The [production approval preparation register](../review/production-approval-register.md) separates prepared source decisions from unaccepted operating choices and actual result-dependent sign-offs. Full Q0 and Q1–Q5 remain pending; no source approval, provider effect, credential grant, customer enrollment, commercial release or new resource spend is inferred. Published-head required CI and actual hosted Codex review are tracked separately.

## T010 source-suite collection checkpoint

- The already approved workflow path now explicitly runs both feature suites at the exact source head in a separate worktree, preserving the root check and all existing floors/skips/named verdicts.
- The measured per-module JUnit guard requires 213 verifier and 28 inventory cases, zero skips/failures/errors, unique identities and the exact two modules. The actual committed step passes 241 source cases; missing cases, unknown modules, a skipped testcase, duplicate identity and a suite error each fail the guard. The affected workflow/floor/CLI-pin suites pass 185 cases.
- T010 is still incomplete and unchecked. Required published-head CI and the actual bootstrap scope/format/authentication decisions remain pending. No new evidence record or frozen task/input change is claimed.

## Source-permission and live-phase follow-up

- The measured combined source run passes 270 cases: 241 verifier and 29 inventory tests, with no skips, failures or errors. Source permissions, source policies and source evidence admissions may remain until superseded; revocation still refuses use. Execution channels and live permissions retain finite limits and actual chronology.
- Source-phase decision overrides are rejected for staging/production C-03 and C-08–C-13 consumption. New regressions first exposed the source-lifetime and live-phase gaps; the repaired source passes them. Real Git-object inventory generation/checking succeeds with current source consent and fails after withdrawal without changing record bytes.
- Exact T007 and T008 commands pass at their separate clean, unchanged source commits. A repeatable T006 structural rerun also passes at the original ratified source; it does not replace or renew the original human decision. Local provenance observations still await actual custodian authentication.
- The new count pins belong to a separate T010 workflow-only commit. No new bootstrap format/record, accepted owner scope, frozen-definition change, deployment or live-gate acceptance is created. All three current PRs stay draft.
