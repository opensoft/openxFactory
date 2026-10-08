# Clarify questions: Neutral resolved council protocol

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md) · **Research**: [research.md](research.md)

**State: all five answered.** Brett Heap ruled each one first-hand on 2026-10-08, choosing the recommended option. The record is brett-wip `lanes/log/codeXfactory-2.md`: RULED at 2026-10-08T19:24:21Z for Q1 to Q4, and at 2026-10-08T19:24:59Z for Q5. The answers are encoded in [spec.md § Clarifications](spec.md#clarifications).

These questions surfaced while planning against the two consumers, codexFactory feature 049 and Hermes feature 025. The ratified text did not decide them. The lane coordinator put each to Brett Heap as multiple choice with a recommended option, as the RULED lines record. The options below are the ones this plan recorded, and each answer quotes the label he chose.

## Q1 (OPEN-1): lifetime ceilings

D3 requires a "short lifetime" for assignments, and FR-007 requires "bounded one-use challenges", but neither fixes a number. What are the contract ceilings?

- **(a) Recommended:** a challenge lives at most 600 seconds, and an assignment at most 6 hours. These are contract maximums; the consumer configures any tighter value. A challenge is consumed within seconds of issue, and an assignment must outlive runner queueing plus the seat job's 30-minute timeout.
- (b) Other values.

**Answer:** "600 s challenge, 6 h assignment (Recommended)". Encoded in [R12](research.md#r12--lifetime-ceilings).

## Q2 (OPEN-2): where the producer-binding instance lives

The provider defines the binding's shape. Where does the concrete instance, with its live audience and subject template, live?

- **(a) Recommended:** in the consumer's governed runtime configuration. The operator writes it at the provisioning act (049 T031; 025 H3), and it is validated with this family's validator at the consumer's pin. The provider ships only the schema, a `.template.yaml` stub, the derivation from `repository-identity.yaml`, and the corpus.
- (b) Provider-published under `contracts/council-convening/`. That makes the neutral repository the holder of one domain's authority configuration, and turns every audience or subject-template change into a provider contract cut.

**Answer:** "Consumer's runtime config (Recommended)". Encoded in [R13](research.md#r13--producer-workflow-binding-and-its-placement).

## Q3 (OPEN-3): revision currency

D1 and D4 require an "admitted governed rule" at "the governed ref and immutable code revision", but not how current that revision must be when the consumer admits. `main` can move between commission and admission.

- (a) Any revision on the governed branch's first-parent history. A superseded rule could seat an outdated roster.
- (b) Exactly the governed tip at admission. Spurious refusals whenever the branch advances, even for unrelated files.
- **(c) Recommended:** first-parent history, plus the rule file at that revision equal to the rule file at the governed tip when admission runs; otherwise `rule_superseded`. Where the rule repository is the producer repository, the producer's verified `job_workflow_sha` must also equal the cited rule revision.

**Answer:** "History + unchanged rule file (Recommended)". Encoded in [R7](research.md#r7--governed-sources-rule-authority-and-revision-currency), which applies the test to every governed source the projection is built from.

## Q4 (OPEN-4): release-inventory membership

Does `contracts/council-convening/`, with its validator, package and tests, join the release digest inventory?

- **(a) Recommended:** join, behind `COUNCIL_CONVENING_RELEASE_FLOOR` set at the Phase 7 cut, following the clearing precedent (#722, ruled for clearing in #745).
- (b) Do not join: identity travels by manifest-row SHA-256 only, as `signed-execution-chain` does.

**Answer:** "Join behind a version floor (Recommended)". Encoded in [R15](research.md#r15--release-surface-membership).

## Q5 (OPEN-5): predicate identifiers

The design's Goals say "Domain predicates remain domain-owned", while D1 makes the closed predicate registry a shared specification. Which identifiers does the neutral registry use?

- **(a) Recommended:** keep the identifiers the governed rule files already declare, `changed_paths_intersect` over `pr_facts` and `rule_touches_security_posture` over `rule_facts`, with no mapping layer. The domain owns which seats a rule conditions on and with which parameters; the evaluation mechanism is neutral.
- (b) Neutral identifiers, with each side's adapter mapping its domain's declared names.

**Answer:** "Keep the existing names (Recommended)". Adding or renaming a predicate is a governed contract change. Encoded in [R5](research.md#r5--the-closed-predicate-registry-and-input-contracts).
