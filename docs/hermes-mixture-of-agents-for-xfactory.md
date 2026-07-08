# Hermes Mixture Of Agents For xFactory

Status: draft
Kind: architecture
Repository context: openxFactory
Purpose: define how Hermes Mixture of Agents reasoning should be used inside
xFactory without weakening the domain, client, customer, credential, and
workflow authority boundaries.

## 1. Source Interpretation

The Hermes Agent Mixture of Agents feature combines multiple AI model responses
into a stronger final response. In the Hermes Agent documentation, a mix has:

- reference models that independently respond to the conversation
- one acting model that synthesizes the final answer

The important implementation boundary is that reference models receive the
conversation text but do not receive system prompts or tool responses, and they
cannot call tools. Tool use is handled by the acting model.

Source: [Hermes Agent Mixture of Agents documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/mixture-of-agents)

For xFactory, treat Mixture of Agents as a Hermes reasoning pattern, not as a
new execution authority.

```text
Mixture of Agents advises.
Hermes roles decide.
openxFactory enforces the workflow rail.
Omnigent workers execute bounded domain work.
External systems enforce final state where applicable.
```

## 1.5 Native MoA Versus xFactory Councils

Native Hermes Mixture of Agents is closest to `panel_synthesis`.

```text
reference models produce independent responses
  -> acting model receives those responses
  -> acting model synthesizes the final response
```

That is not a vote by default. It is also not a deliberative council by
default. Reference models do not automatically see each other's answers, argue,
revise, or come to consensus.

xFactory therefore defines three council modes:

| Mode | Flow | Implemented By |
| --- | --- | --- |
| `panel_synthesis` | independent opinions -> acting Hermes synthesis | native Hermes MoA-compatible config |
| `scored_vote` | independent opinions -> explicit vote or score -> acting Hermes synthesis | xFactory council orchestration on top of Hermes |
| `deliberative_council` | independent opinions -> disagreement summary -> rebuttal -> revised opinions -> consensus or dissent record -> acting Hermes recommendation | xFactory council orchestration on top of Hermes |

Use native Hermes MoA as the primitive. Use xFactory council orchestration when
the domain needs voting, rebuttal, consensus, dissent capture, or audit-grade
deliberation.

## 2. xFactory Placement

xFactory keeps the standard stack:

```text
Customer subject
  patient, managed system, campaign, ledger, project, account, matter

Customer Hermes layer
  subject-specific context, consent, preferences, memory, active work

Client Hermes layer
  organization policy, staff, integrations, tenant configuration, approvals

Domain Hermes layer
  reusable domain policy, expert review standards, domain memory, routing

openxFactory layer
  contracts, job envelopes, gates, traceability, state transitions, audit

Domain Omnigent layer
  domain-tuned workers, tools, validation checks, output templates
```

A Hermes layer may use a Mixture of Agents preset before it reaches a decision,
but the decision is still owned by a named Hermes role or council.

```text
Hermes layer
  -> Hermes role or council
  -> optional Mixture of Agents preset
  -> acting Hermes role synthesizes recommendation
  -> Hermes gate decision
  -> openxFactory job envelope or state transition
```

## 3. Authority Rules

Every xFactory domain must preserve these rules:

- Reference agents are advisory only.
- Reference agents must not receive raw secrets, credential values, unrestricted
  private records, or unredacted regulated data.
- Reference agents must not call tools.
- The acting Hermes role is the only participant in a mix that may request tool
  use, and only through the normal openxFactory job envelope, gate, credential,
  and audit contract.
- A Mixture of Agents output is evidence, not approval.
- Approval remains with the owning Hermes role, review council, accountable
  human, or external enforcement system.
- Dissent must be preserved when a mix is used for high-risk work.

The safest default is to give reference agents a redacted context packet and
give the acting Hermes role the governed tool pathway.

## 4. Standard Files

Domain factories should declare Mixture of Agents presets in the Hermes overlay
surface:

```text
hermes/
  domain/
    agent-mixes.yaml
  client/
    agent-mixes.template.yaml
  customer/
    agent-mixes.template.yaml
```

Recommended documentation file in each domain repo:

```text
docs/hermes-agent-mixes.md
```

Domain Hermes presets describe reusable domain review patterns. Client Hermes
templates describe how a client can strengthen or specialize those patterns.
Customer Hermes templates describe customer-subject level reasoning that must
stay private to the customer subject unless explicitly promoted.

## 5. Mix Profile Shape

Use this profile shape as the domain-neutral starter:

```yaml
schema_version: 1
kind: hermes_agent_mix_profiles

mix_profiles:
  - id: setup_readiness_panel_synthesis
    layer: domain_hermes
    mode: panel_synthesis
    purpose: collect independent setup readiness opinions and synthesize a recommendation
    native_hermes_moa_compatible: true
    acting_role: hermes_setup_reviewer
    reference_roles:
      - workflow_architect
      - credentialing_reviewer
      - compliance_reviewer
      - implementation_planner
    allowed_context:
      - approved_intent_summary
      - workflow_state
      - redacted_customer_context
      - policy_references
      - credential_requirement_ids
    prohibited_context:
      - raw_credentials
      - unrestricted_private_records
      - tool_outputs_with_secret_values
      - unredacted_regulated_data_without_authorization
    tool_policy:
      reference_agents_have_tools: false
      acting_agent_tool_access: gated
    credential_policy:
      reference_agents_receive_runtime_grants: false
      acting_agent_may_request_grant: true
      grant_source: openxFactory_credential_broker
    evidence_required:
      - reference_agent_summaries
      - acting_agent_synthesis
      - dissent_summary
      - risk_classification
      - approval_basis
      - redaction_level
    escalation_rules:
      escalate_on_dissent: true
      escalate_on_missing_evidence: true
      escalate_on_policy_conflict: true
```

Domain repos may add domain-specific fields, but they should not remove the
authority, context, tool, credential, evidence, or escalation sections.

### Scored Vote Extension

Use `scored_vote` when the council needs explicit vote or score evidence before
the acting Hermes role synthesizes a recommendation.

```yaml
  - id: privileged_action_scored_vote
    layer: domain_hermes
    mode: scored_vote
    purpose: score a privileged action before recommendation
    native_hermes_moa_compatible: false
    acting_role: hermes_approval_controller
    reference_roles:
      - domain_policy_reviewer
      - security_reviewer
      - credential_risk_reviewer
      - workflow_gate_reviewer
    scoring_criteria:
      - policy_fit
      - evidence_completeness
      - credential_scope_fit
      - rollback_readiness
      - customer_or_client_risk
    voting_policy:
      vote_values:
        - approve
        - approve_with_conditions
        - reject
        - abstain
      approval_threshold: majority
      require_unanimous_for:
        - destructive_action
      abstain_requires_reason: true
      tie_breaker: escalate_to_human
    evidence_required:
      - reference_agent_summaries
      - vote_record
      - score_summary
      - acting_agent_synthesis
      - dissent_summary
      - risk_classification
      - approval_basis
      - redaction_level
```

The vote does not approve the work. It is evidence for the owning Hermes gate.

### Deliberative Council Extension

Use `deliberative_council` when disagreement matters and the domain needs an
argument, rebuttal, revised-position, consensus, and dissent record.

```yaml
  - id: high_risk_action_deliberative_council
    layer: domain_hermes
    mode: deliberative_council
    purpose: run disagreement and rebuttal before high-risk recommendation
    native_hermes_moa_compatible: false
    acting_role: hermes_approval_controller
    reference_roles:
      - domain_policy_reviewer
      - security_reviewer
      - credential_risk_reviewer
      - workflow_gate_reviewer
    deliberation_policy:
      rounds:
        - independent_positions
        - disagreement_summary
        - rebuttal
        - revised_positions
        - final_recommendation
      share_between_reference_agents:
        - disagreement_summary
        - redacted_peer_positions
      require_revised_positions: true
      preserve_unresolved_dissent: true
      consensus_target: consensus_or_explicit_dissent
    evidence_required:
      - reference_agent_summaries
      - disagreement_summary
      - rebuttal_record
      - revised_positions
      - consensus_summary
      - unresolved_dissent
      - dissent_summary
      - acting_agent_synthesis
      - risk_classification
      - approval_basis
      - redaction_level
    escalation_rules:
      escalate_on_dissent: true
      escalate_on_unresolved_dissent: true
      escalate_on_missing_evidence: true
      escalate_on_policy_conflict: true
```

The deliberative council does not approve the work. It produces an
audit-quality recommendation package for the owning Hermes role or gate.

## 6. Context Packets

Before invoking a mix, Hermes should create a context packet. The packet is the
only material sent to reference agents.

Context packet requirements:

- identify the owning Hermes layer
- identify the acting role
- identify the workflow, gate, and approved intent
- state the redaction level
- include only allowed context classes
- include source and evidence references where possible
- exclude raw secrets and prohibited data classes
- preserve enough facts for independent review

Example:

```yaml
schema_version: 1
kind: hermes_agent_mix_context_packet

packet:
  id: <packet-id>
  mix_profile_id: high_risk_action_deliberative_council
  owning_layer: domain_hermes
  acting_role: hermes_approval_controller
  workflow_ref: <workflow-ref>
  gate_ref: <gate-ref>
  approved_intent_ref: <intent-ref>
  redaction_level: customer_redacted
  includes:
    - approved_intent_summary
    - workflow_state
    - policy_references
    - credential_requirement_ids
  excludes:
    - raw_credentials
    - unrestricted_private_records
  source_refs:
    - <source-ref>
```

## 7. Evidence Record

A Mixture of Agents run should emit evidence that can be attached to a gate,
approval packet, memory promotion request, or credential approval request.

```yaml
schema_version: 1
kind: hermes_agent_mix_evidence

evidence:
  id: <evidence-id>
  mix_profile_id: high_risk_action_deliberative_council
  context_packet_ref: <packet-id>
  owning_layer: domain_hermes
  acting_role: hermes_approval_controller
  reference_roles:
    - domain_policy_reviewer
    - security_reviewer
    - credential_risk_reviewer
  redaction_level: customer_redacted
  recommendation: approve_with_conditions
  dissent_present: true
  dissent_summary: <summary>
  vote_record_ref: <vote-record-or-null>
  rebuttal_record_ref: <rebuttal-record-or-null>
  consensus_summary: <summary-or-null>
  unresolved_dissent: <summary-or-null>
  required_conditions:
    - <condition>
  decision_owner: domain_hermes
  decision_status: recommendation_only
  created_at: <timestamp>
```

The evidence record must be explicit that the mix produced a recommendation
unless and until a separate Hermes gate decision approves the next transition.

## 8. Where To Use MoA

Use Mixture of Agents when independent reasoning materially improves safety,
quality, or auditability.

Strong use cases:

- pre-run questionnaire simulation
- setup readiness review
- gate review packets
- credential approval review
- high-risk workflow planning
- memory promotion review
- domain expert panel review
- incident, exception, rollback, or repair review
- customer-facing output review

Weak use cases:

- simple deterministic validation
- low-risk formatting
- schema parsing
- routine file generation
- work where a single tool result is the source of truth

## 9. Domain Examples

MedxFactory:

```text
Medical safety reviewer
Clinical workflow reviewer
Privacy and consent reviewer
Payer or referral reviewer
Acting role: Medical Domain Hermes Approval Controller
```

OpsxFactory:

```text
Change-risk reviewer
Security reviewer
Rollback reviewer
Credential-risk reviewer
Acting role: Operations Domain Hermes Approval Controller
```

LedgerxFactory:

```text
Reconciliation reviewer
Tax or filing reviewer
Audit evidence reviewer
Fraud-risk reviewer
Acting role: Ledger Domain Hermes Approval Controller
```

AdxFactory:

```text
Brand reviewer
Privacy reviewer
Claims reviewer
Spend-risk reviewer
Acting role: Marketing Domain Hermes Approval Controller
```

codexFactory:

```text
Architecture reviewer
Security reviewer
Test reviewer
Release reviewer
Acting role: Software Engineering Domain Hermes Approval Controller
```

## 10. Credentialing Rule

Credentialing must stay asymmetric:

```text
Reference agents
  receive redacted context only
  do not receive runtime grants
  do not call tools
  do not see raw credentials

Acting Hermes role
  may request a runtime grant only when the workflow gate allows it
  uses the credential broker
  records evidence and audit
  cannot bypass approval policy

Omnigent worker
  receives only short-lived scoped runtime capability grants
  never receives raw credentials from the mix
```

This preserves the xFactory credential model while still allowing richer
reasoning before a grant is approved.

## 11. Memory Promotion

Mixture of Agents can improve memory quality, but it must not promote memory by
itself.

Recommended memory promotion flow:

```text
Customer or workflow event
  -> candidate learning
  -> redacted context packet
  -> reference review
  -> acting Hermes synthesis
  -> Hermes Memory Curator decision
  -> memory update in the correct layer
```

The review must decide whether a learning is:

- customer-specific and private
- client-specific and tenant-scoped
- domain-level and reusable
- too sensitive to promote
- allowed only after de-identification or aggregation

## 12. Starter Requirements

The openxFactory starter should create:

- `docs/hermes-agent-mixes.md`
- `hermes/domain/agent-mixes.yaml`
- `hermes/client/agent-mixes.template.yaml`
- `hermes/customer/agent-mixes.template.yaml`
- `schemas/agent-mixes.schema.yaml`

The pre-run questionnaire should ask:

- Which workflows require Mixture of Agents review?
- Which Hermes layer owns each mix?
- Which council mode is required: `panel_synthesis`, `scored_vote`, or
  `deliberative_council`?
- Which Hermes role is the acting role?
- Which reference roles are advisory?
- Which context classes are allowed?
- Which context classes are prohibited?
- What redaction level is required?
- For `scored_vote`, what are the scoring criteria, vote values, threshold, and
  tie-break behavior?
- For `deliberative_council`, what rounds are required, what disagreement is
  shared, and what unresolved dissent escalates?
- What evidence and dissent must be preserved?
- Can a mix result approve work, or is it recommendation-only?

Default answer: recommendation-only.

## 13. Validation Expectations

Validation should fail or warn when:

- a mix omits `mode`
- a mix uses a mode other than `panel_synthesis`, `scored_vote`, or
  `deliberative_council`
- a mix gives tools to reference agents
- a mix allows reference agents to receive runtime grants
- a mix omits prohibited context classes
- a `scored_vote` mix has no scoring criteria, voting policy, vote record, or
  score summary
- a `deliberative_council` mix has no disagreement summary, rebuttal round,
  revised positions, consensus summary, unresolved dissent record, or unresolved
  dissent escalation
- a high-risk workflow requires a mix but has no evidence requirement
- a mix says it can approve privileged work directly
- a credential approval mix has no credential policy
- a memory promotion mix has no memory owner

The starter validator can begin with structural checks. Domain validators should
add domain-specific checks as workflows mature.
