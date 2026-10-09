# Clarify questions: Neutral resolved council protocol

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md) · **Research**: [research.md](research.md)

**State: all answered.** Brett Heap ruled each question first-hand on 2026-10-08, choosing the recommended option. The record is brett-wip `lanes/log/codeXfactory-2.md`: RULED at 2026-10-08T19:24:21Z for Q1 to Q4, at 2026-10-08T19:24:59Z for Q5, and at 2026-10-08T23:03:35Z for the three follow-ups to Q3 and for N10. The answers are encoded in [spec.md § Clarifications](spec.md#clarifications); N10 is a packet question, encoded in the packet files and [tasks.md](tasks.md) T002.

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

## Follow-ups to Q3 (OPEN-3)

Applying the Q3 answer raised three questions the label alone did not settle. The lane coordinator put each to Brett Heap as multiple choice with a recommended option. The RULED lines record the label he chose and what it means, quoted below; they do not record the other options.

### Follow-up 1: which sources the currency test covers

The answer names "the rule file". The projection is also built from the council profile, the council document, the rule directory's listing and the envelope configuration, and a change to any of them changes the roster.

**Answer:** "Every governed source (Recommended)": every governed source a convening cites must be unchanged at the governed tip at admission, not only the rule file. Encoded in [R7](research.md#r7--governed-sources-rule-authority-and-revision-currency) and data-model E2 step 5.

### Follow-up 2: which repository is the "producer repository"

In the estate's calling pattern the token's `repository` claim is the caller, while the workflow, its commit and the rules are another repository's.

**Answer:** "job_workflow_ref's repo (Recommended)": "producer repository" is the repository named in `job_workflow_ref`, and a permitted producer workflow outside the governed repository is refused, failing closed. Encoded in R7, R13 and data-model E10; the binding names the calling repository `caller_repository` so the two are not confused.

### Follow-up 3: the seat job's workflow commit

A seat runs after admission, when `main` may have moved, so equality with the frozen revision would refuse every seat whose `main` moved.

**Answer:** "At or after the frozen rev (Recommended)": a seat job's workflow commit must be on the governed history at or after the frozen revision, not equal to it. Encoded as `on_governed_history_since_revision` in data-model E10, with the seat's checkout held to its verified `job_workflow_sha`.

## N10: the packet's stale allocation notes

Not a specification question. #1268 carried 2026-10-03 allocation notes under `openspec/changes/renew-resolved-council-protocol/` that no longer described the owner, and the packet's task 2.2 was unticked.

**Answer:** "Dated correction + tick 2.2 (Recommended)": #1268 replaces its stale 2026-10-03 allocation notes under the packet directory with a dated allocation record (owner codeXfactory-2, feature 035, claimed 2026-10-07, builder ruled 2026-10-08) and ticks the packet's task 2.2; #1268 lands in a Rule 6 window.
