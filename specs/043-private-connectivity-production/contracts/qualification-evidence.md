# Planned production qualification evidence interface

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](../spec.md)

This is a feature-local design for a future commissioned verifier and evidence workflow. No serialized schema, new published record kind, executable verifier or approval is created here. Exact formats and command interfaces require accepted C-01/C-08 scope.

## Evidence classes and scope

Keep source/unit evidence, exact-revision CI, supported release publication, target execution/readback, staging observations, production observations and human/commercial decisions distinguishable. A source or lab record cannot satisfy an unobserved deployed control.

Each record retains run/attempt identity, Q gate, candidate/profile revision/content identity, customer/site/network/domain/environment/target/region scope, current authority/request/channel/grant or reviewed-merge reference, policy baseline, expected case registry, actual command/probe, expected and observed outcomes, timestamps/event anchors, monitoring coverage, approved limits, incident/repair links and fresh sign-offs.

References are immutable and secret-free. Sensitive inputs remain in protected custody under references. Case output is retained with command identity, tested revision, exit/result and immutable output content; a copied pass string is not an observation.

## Planned verifier behavior

The proposed specs/043-private-connectivity-production/verify-evidence.py and feature tests are candidate implementation paths, not existing commands. The verifier must:

- Freeze required cases/subchecks, scope comparisons, owner commands and prerequisite-gate relationships in the reviewed implementation.
- Reject missing, duplicate, unknown, substituted or wrong-scope cases; mismatched command/revision/output; missing or failed owner checks; stale/expired authority; and mixed run/candidate/profile/customer/environment evidence.
- Require immutable dependency references/content checks, correct expected/observed outcomes and the accepted current candidate/limit/authority decisions.
- Require successful legitimate controls before denials count, real actual-application/network observations, approved direct/relay and applicable disconnected-peer checks, and separate authorized-neighbor proof.
- Compare finite, field-valid measured values against approved numeric limits with stated units/event anchors. Reject negative/invalid values, excessive sampling gaps and omitted observation intervals. Missing monitoring time does not count as healthy acceptance time.
- Preserve failed/blocked attempts, reviewed remediation and clean rerun/resume links. A waiver cannot manufacture an observation.
- Validate records without executing owner commands, collecting live state, granting authority or promoting a caller-written verdict.
- Import T001–T009 only through the closed authenticated bootstrap bridge; reject nonexistent-receipt requirements, fabricated replacement outputs and attempts to infer an approving authority from the verifier itself.
- Validate each Q3–Q5 child against its frozen approved instance manifest and same-scope predecessors. Aggregate completion requires all commissioned children; a missing unrelated aggregate cannot substitute for, or erase, a genuinely accepted child. A wave requires admission of its corresponding offer.

Independent owners/reviewers confirm that immutable outputs, actual tested targets/revisions and current authority support the records. A successful structural verification alone is not a human gate decision.

## Gate prerequisites

Q0 verifies commissioned scopes and consumed C-02 decisions; T049 freezes final C-05 consumer/harness compatibility before target preparation. Q1 verifies supported candidates, C-03–C-08 and current entry conditions. Q2 requires the same intended-platform candidate/run across four offering paths and required lifecycle/drill coverage. Q3 requires accepted Q2 plus current C-09 bounds and target authority. Q4 requires the approved actual observed window, results, incident closure and fresh C-10 acceptance. Q5 requires C-11 for an offer and C-12 for its individual wave, exact eligibility and accepted Q4. C-13 governs any resume after reviewed remediation and reruns. See the [task evidence contract](task-evidence.md) for bootstrap, child-DAG and final candidate closure rules.

Do not hard-code the 040 task inventory, its synthetic customers, old timing limits or five-role sign-off list as production defaults. Required roles derive from the accepted actual scope.

## Pin registration and custody

The proposed feature register-evidence-pins.py and tests may generate/check an exact 043 inventory only after their scope is accepted. Default writing and read-only checking must be distinguishable. Evidence references and local/foreign repository reachability remain checked under their proper ownership classes.

Existing shared registration covers only specs/040-private-connectivity/evidence/*.json. It does not admit this feature. Any change to scripts/doc_health/pin_class.py, its pin-reachability regressions, measured census or required CI needs a narrow owning OpenSpec authorization before implementation. No prefix exception or old register is widened by this design.

C-08 names protected immutable evidence storage, retention/access, backup and secret-safe publication policy. Verification must fail when required evidence/custody/reachability is absent rather than inventing a pass.
