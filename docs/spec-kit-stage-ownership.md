# Spec Kit Stage Ownership

This document is the canonical `openWorkflow` policy for Spec Kit stage
ownership, clarification routing, and answer approval. Omnigent/Polly executes
Spec Kit. Hermes owns approval, audit, and authority routing policy.

## Source Provenance

Reviewed sources:

- `/home/brett/projects/Agents/Omnigent-Install/docs/hermes-integration-plan.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/project-lead-agents.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/runbooks/project-alfa-structured-clarify-test.md`
- `/home/brett/projects/Agents/Omnigent-Install/docs/hermes-structured-event-contract.md`
- `docs/roles-and-authority.md`

The install repo source docs remain in place until a later migration feature
marks them as canonical links, legacy copies, or implementation runbooks.

## Boundary

Spec Kit may run only after Hermes approves the feature and Omnigent accepts
the feature as ready for implementation flow.

```text
Hermes-approved feature
  -> Omnigent pre-Spec-Kit acceptance
  -> /speckit.specify
  -> /speckit.clarify
  -> Hermes approval for clarification answers
  -> /speckit.plan
  -> /speckit.tasks
  -> /speckit.analyze
  -> /speckit.implement
  -> local checks and branch review
```

Hermes may read every Spec Kit artifact for traceability, approval, dashboard,
and merge readiness. Hermes does not run the implementation commands.

## Stage Ownership

```yaml
speckit_ownership:
  specify:
    command: /speckit.specify
    owner: LE
    consulted:
      - PO
      - PM
      - PA
    output:
      - feature_spec
      - acceptance_criteria
      - scope_boundaries
    hermes_gate:
      before: feature_must_be_approved_for_speckit
      after: record_spec_artifact_reference

  clarify:
    command: /speckit.clarify
    owner: LE
    question_router: Omnigent
    answer_packet_approver: Hermes
    output:
      - clarification_questions
      - authority_answers
      - clarification_answer_packet
    hermes_gate:
      before: feature_must_be_approved_for_speckit
      after: answers_must_be_approved_before_application

  plan:
    command: /speckit.plan
    owner: LE
    consulted:
      - PA
      - LC
      - LQ
      - LI
      - LS
    output:
      - implementation_plan
      - technical_context
      - risk_notes
    hermes_gate:
      before: clarification_answers_must_be_approved_when_present
      after: record_plan_artifact_reference

  tasks:
    command: /speckit.tasks
    owner: LC
    reviewed_by:
      - LE
      - LQ
    output:
      - task_breakdown
      - coder_assignments
      - validation_tasks
    hermes_gate:
      before: plan_must_exist
      after: record_tasks_artifact_reference

  analyze:
    command: /speckit.analyze
    owner: LE
    reviewed_by:
      - PA
      - LQ
      - LS
    output:
      - ambiguity_findings
      - consistency_findings
      - risk_findings
    hermes_gate:
      before: spec_plan_and_tasks_must_exist
      after: blockers_must_be_resolved_or_approved

  implement:
    command: /speckit.implement
    owner: LC
    executor: coder_agents
    reviewed_by:
      - LE
      - LQ
    output:
      - implementation_diff
      - test_evidence
      - local_check_results
    hermes_gate:
      before: implementation_must_be_allowed_by_policy
      after: pr_admission_required_before_github_pr
```

## Clarification Routing

When the LE returns clarification questions, Omnigent must route each question
to the authority map. Omnigent may classify, dispatch, collect, and assemble.
It must not invent authority answers or apply them before Hermes approval.

```yaml
clarification_routing:
  product_scope:
    primary: PO
    fallback: PM
  user_visible_behavior:
    primary: PO
    fallback: PM
  priority:
    primary: PM
    fallback: PO
  milestone:
    primary: PM
    fallback: PO
  architecture_data_contracts:
    primary: PA
    escalate_to: CA
  project_architecture:
    primary: PA
    escalate_to: CA
  cross_project_architecture:
    primary: CA
    consulted:
      - PA
      - LA
  canonical_data_ownership:
    primary: CA
    consulted:
      - PA
  product_wide_contract:
    primary: CA
    consulted:
      - PA
  subsystem_architecture:
    primary: LA
    consulted:
      - PA
  local_data_model:
    primary: LA
    consulted:
      - PA
  local_tech_stack:
    primary: LA
    consulted:
      - PA
  security:
    primary: LS
    escalate_to: hermes-security
  tenant_isolation:
    primary: LS
    escalate_to: hermes-security
  test_strategy:
    primary: LQ
  test_evidence:
    primary: LQ
  integration:
    primary: LI
  merge_sequencing:
    primary: LI
    consulted:
      - PM
  implementation_feasibility:
    primary: LC
    consulted:
      - LE
  coding_approach:
    primary: LC
    consulted:
      - LA
```

If classification is ambiguous, Omnigent routes to LE for triage. If the answer
could change product scope, architecture ownership, security posture, or merge
risk, Hermes must record an approval request before the answer becomes project
truth.

## Elicitation Flow

The operational prompt that drives routing is:

```text
When LE returns clarification questions:
1. Read the project Spec Kit routing map.
2. Classify each question.
3. Dispatch the question to the mapped lead agent.
4. Collect answers.
5. Send the answer packet back to LE.
6. Submit the answer packet to Hermes.
7. Do not apply answers until Hermes approval.
```

This is an Omnigent execution rule governed by Hermes policy. In v1, Hermes
owns the router service contract and Omnigent emits structured events or
markers. AgentTower is not part of v1.

## Event And Artifact Requirements

Omnigent must emit durable evidence for Spec Kit stages. The preferred contract
is structured events, with text markers only as an early compatibility path.

Required stage events:

- `stage_started`
- `stage_completed`
- `subagent_dispatched`
- `subagent_result_collected`
- `artifact_recorded`
- `approval_requested`

Required durable IDs where applicable:

- `stage_id`
- `subagent_session_id`
- `question_id`
- `agent_id`
- `artifact_id`
- `approval_request_id`
- `bridge_key`

Clarification sequence:

```text
stage_started                 speckit_clarify
subagent_dispatched           LE clarify preparation
subagent_result_collected     clarification questions
subagent_dispatched           routed authority answers
subagent_result_collected     authority answers
subagent_dispatched           LE answer packet assembly
artifact_recorded             clarification answer packet
approval_requested            apply clarification answers
stage_completed               speckit_clarify
```

## Approval Rules

Hermes approval is required before:

- a feature enters Spec Kit;
- clarification answers are applied;
- implementation begins when policy or risk requires a gate;
- a branch opens a GitHub PR.

Authority agents may approve within their assigned authority. Hermes records
the approval, applies policy, and escalates when risk or scope exceeds that
authority.

## Failure Conditions

The stage must stop when:

- a coder is asked to decide product, architecture, security, or test policy;
- Omnigent answers clarification questions itself instead of routing them;
- E1/LE guesses answers without authority evidence;
- answers are applied before Hermes approval;
- implementation starts before required gates pass;
- a live elicitation disappears into a stalled CLI session;
- Spec Kit artifacts drift outside the approved feature scope.

## Pass Criteria

- Every Spec Kit artifact traces back to an approved feature.
- Clarification questions route to named authority agents.
- Each answer records `question_id`, `answered_by`, decision, rationale, and
  confidence or equivalent evidence.
- The final answer packet remains `awaiting_hermes_approval` or equivalent
  until approved.
- No unapproved clarification becomes project truth.
