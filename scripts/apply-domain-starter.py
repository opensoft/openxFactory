#!/usr/bin/env python3
"""Apply the openxFactory domain starter pack to a domain factory repo.

The runner is intentionally conservative. It creates missing starter files,
adds a rerun report, validates YAML parsing for generated surfaces, and skips
existing files unless they are the rerun report itself.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - friendly CLI failure
    yaml = None


STARTER_VERSION = 6
STARTER_NAME = "openxFactory/domain-factory-starter-pack"


@dataclass(frozen=True)
class DomainContext:
    domain_id: str
    product_name: str
    display_name: str
    category: str
    domain_layer_name: str
    client_layer_name: str
    customer_layer_name: str
    orchestrator_profile: str


@dataclass
class RunLog:
    created: list[tuple[str, str]]
    updated: list[tuple[str, str]]
    skipped: list[tuple[str, str]]
    conflicts: list[tuple[str, str, str]]
    validation: list[str]


def slug_from_product(product_name: str) -> str:
    cleaned = re.sub(r"Factory$", "", product_name, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", cleaned).strip("_")
    return cleaned.lower() or "example"


def read_stack(target: Path) -> dict[str, Any]:
    stack_path = target / "stack.yaml"
    if not stack_path.exists() or yaml is None:
        return {}
    with stack_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data if isinstance(data, dict) else {}


def infer_context(target: Path, args: argparse.Namespace) -> DomainContext:
    stack = read_stack(target)
    product_name = args.product_name or stack.get("domain", {}).get("product_name") or target.name
    domain_id = args.domain_id or stack.get("domain", {}).get("id") or slug_from_product(product_name)
    display_name = args.display_name or stack.get("domain", {}).get("display_name") or product_name
    category = args.category or stack.get("domain", {}).get("category") or domain_id
    hermes = stack.get("hermes", {}) if isinstance(stack.get("hermes", {}), dict) else {}
    omnigent = stack.get("omnigent", {}) if isinstance(stack.get("omnigent", {}), dict) else {}
    return DomainContext(
        domain_id=domain_id,
        product_name=product_name,
        display_name=display_name,
        category=category,
        domain_layer_name=args.domain_layer_name or hermes.get("domain_layer_name") or f"{display_name} Domain Hermes",
        client_layer_name=args.client_layer_name or hermes.get("client_layer_name") or f"{display_name} Client Hermes",
        customer_layer_name=args.customer_layer_name or hermes.get("customer_layer_name") or f"{display_name} Customer Hermes",
        orchestrator_profile=args.orchestrator_profile or omnigent.get("orchestrator_profile") or domain_id,
    )


def yaml_header(ctx: DomainContext, managed_mode: str = "scaffold") -> str:
    return (
        "starter_metadata:\n"
        f"  source: {STARTER_NAME}\n"
        f"  starter_version: {STARTER_VERSION}\n"
        f"  domain_id: {ctx.domain_id}\n"
        "  generated_at: null\n"
        f"  managed_mode: {managed_mode}\n\n"
    )


def md_header(ctx: DomainContext) -> str:
    return (
        "<!--\n"
        f"starter_source: {STARTER_NAME}\n"
        f"starter_version: {STARTER_VERSION}\n"
        f"domain_id: {ctx.domain_id}\n"
        "managed_mode: scaffold\n"
        "-->\n\n"
    )


def templates(ctx: DomainContext) -> dict[str, str]:
    return {
        "README.md": f"""# {ctx.product_name}

{ctx.product_name} is an xFactory domain stack for {ctx.category}.

It implements the openxFactory/xFactory contract with:

- {ctx.domain_layer_name}
- {ctx.client_layer_name}
- {ctx.customer_layer_name}
- {ctx.display_name} Omnigent overlay

## Implementation

- [Implementation Runbook](docs/implementation-runbook.md)
- [Implementation Guide](docs/implementation-guide.md)
- [Pre-Run Questionnaire](docs/pre-run-questionnaire.md)
- [Setup Runbook](docs/setup-runbook.md)
- [Domain Overview](docs/domain-overview.md)
- [Workflow Gates](docs/workflow-gates.md)
- [Customer Hermes Model](docs/customer-hermes-model.md)
- [Omnigent Constitution](docs/omnigent-constitution.md)
- [Hermes Agent Mixes](docs/hermes-agent-mixes.md)
- [Credentialing](docs/credentialing.md)
- [Boundary](docs/boundary.md)
""",
        "Makefile": """PYTHON ?= python3

.PHONY: validate
validate:
\t$(PYTHON) scripts/validate-domain-factory.py
""",
        "stack.yaml": f"""schema_version: 1
kind: xfactory_domain_stack

domain:
  id: {ctx.domain_id}
  product_name: {ctx.product_name}
  display_name: {ctx.display_name}
  category: {ctx.category}

models:
  action_classes: models/action-classes.yaml
  risk_levels: models/risk-levels.yaml
  command_classes: models/command-classes.yaml
  evidence_types: models/evidence-types.yaml

xfactory:
  contract_repo: github.com/opensoft/openxFactory
  contract_name: openxFactory

hermes:
  domain_layer_name: {ctx.domain_layer_name}
  domain_overlay: hermes/domain
  domain_agent_mixes: hermes/domain/agent-mixes.yaml
  client_layer_name: {ctx.client_layer_name}
  client_overlay: hermes/client
  client_agent_mixes_template: hermes/client/agent-mixes.template.yaml
  customer_layer_name: {ctx.customer_layer_name}
  customer_overlay: hermes/customer
  customer_agent_mixes_template: hermes/customer/agent-mixes.template.yaml

omnigent:
  domain_overlay: omnigent
  orchestrator_profile: {ctx.orchestrator_profile}

credentials:
  requirements: credentials/requirements.yaml
  broker_contract: credentials/broker-contract.yaml
  binding_template: credentials/bindings.template.yaml
  grant_template: credentials/grants.template.yaml
  audit_policy: credentials/audit.yaml

tenancy:
  client_kinds: []
  customer_kinds: []
  isolation:
    memory: per_client
    records: per_client
    secrets: per_client
    customer_context: per_customer
""",
        "docs/boundary.md": md_header(ctx) + f"""# {ctx.product_name} Boundary

{ctx.product_name} owns domain behavior for {ctx.category}. openxFactory owns
the neutral workflow rail.

## openxFactory Owns

- workflow contracts
- gates
- traceability
- routing
- admission states
- audit expectations
- handoff boundaries

## {ctx.domain_layer_name} Owns

- domain policy
- workflow standards
- domain review gates
- escalation rules
- reusable domain memory and playbooks

## {ctx.client_layer_name} Owns

- client organization identity
- local operating policy
- staff and escalation contacts
- integration inventory
- credential binding references

## {ctx.customer_layer_name} Owns

- customer subject identity
- current state
- timeline
- subject-specific evidence
- subject-specific memory
""",
        "docs/implementation-guide.md": md_header(ctx) + """# Implementation Guide

For the phased implementation plan, see
[Implementation Runbook](implementation-runbook.md).

## Create a Client

1. Select a profile from `profiles/`.
2. Create a client record from `tenants/examples/`.
3. Bind credential requirements using `credentials/bindings.template.yaml`.
4. Confirm client isolation and audit policy.

## Run a Starter Workflow

1. Customer or client Hermes requests the workflow.
2. Client Hermes checks policy and binding availability.
3. Domain Hermes checks risk and approval requirements.
4. openxFactory creates the job envelope.
5. Domain Omnigent receives scoped grant references and executes bounded work.
6. Hermes records evidence, audit, and outcome.
""",
        "docs/implementation-runbook.md": md_header(ctx) + f"""# {ctx.product_name} Implementation Runbook

This runbook turns the current {ctx.product_name} scaffold into an
implementable domain stack.

## Phases

1. Fill canonical domain model.
2. Define workflows.
3. Define credential broker contract.
4. Define provider adapter contracts.
5. Define Hermes approval packets.
6. Define Omnigent worker and command policy.
7. Define validation and output templates.
8. Define client instantiation shape.
9. Add schemas and validation scripts.
10. Run first dry-run client workflow.

## Starter Pack Versus Instantiation

Starter pack provides scaffold, placeholders, examples, and validation hooks.
Domain implementation provides domain-specific workflows, provider scopes,
adapter contracts, and validation checks. Client instantiation provides real
client identity, vault references, approvers, maintenance windows, and SLAs.
Runtime produces grants, transcripts, evidence, audit, and revocation records.
""",
        "docs/pre-run-questionnaire.md": md_header(ctx) + f"""# {ctx.product_name} Pre-Run Questionnaire

Complete this before implementing a new profile, client, tenant, or
customer-subject instantiation.

## Answer Quality

- Answer status: <declared|inferred|simulated|confirmed|approved_for_instantiation>
- Answer scope: <domain|profile|client|tenant|customer_subject>
- Source files or stakeholder decisions supporting the answers:
- Assumptions:
- Must confirm before implementation:
- Must confirm before live instantiation:

## Domain Identity

- Domain repo: {ctx.product_name}
- Product name: {ctx.product_name}
- Domain category: {ctx.category}
- Closest existing xFactory analogy:
- Worst existing xFactory analogy and why:
- Work this domain owns:
- Work this domain does not own:
- Is this a new domain, profile, client deployment, or customer-subject deployment?

## Hermes Layers

- Domain Hermes: {ctx.domain_layer_name}
- Client Hermes: {ctx.client_layer_name}
- Customer Hermes: {ctx.customer_layer_name}
- Does this repo use legacy `subject_layer` or two-Hermes vocabulary?
- Legacy subject layer name, if any:
- Normalized client layer name:
- Normalized customer layer name:
- Which layer may initiate read-only work?
- Which layer may initiate privileged work?
- Which layer can stop work?
- Which layer can approve read-only work?
- Which layer can approve write, publish, send, deploy, money-moving,
  care-affecting, destructive, or privileged work?
- Which layer names are repo-declared?
- Which layer names are inferred?

## Hermes Mixture Of Agents

- Which workflows or gates require Mixture of Agents review?
- Which Hermes layer owns each mix?
- Which mode does each mix use: `panel_synthesis`, `scored_vote`, or
  `deliberative_council`?
- Which Hermes role is the acting role for each mix?
- Which reference roles are advisory for each mix?
- Which context classes may reference agents receive?
- Which context classes are prohibited from reference agents?
- What redaction level is required before invoking reference agents?
- May reference agents use tools?
- May reference agents receive runtime credential grants?
- May the acting Hermes role request tools or runtime grants?
- For `scored_vote`, what are the vote values, scoring criteria, approval
  threshold, unanimous requirements, abstain rules, and tie-break behavior?
- For `deliberative_council`, what rounds are required, which disagreement
  summaries are shared, are revised positions required, and what unresolved
  dissent escalates?
- What evidence must a mix produce?
- Must dissenting reference-agent opinions be preserved?
- Can the mix output approve work directly, or is it recommendation-only?
- Which mix profiles are repo-declared?
- Which mix profiles are inferred from workflows or risk?

## Client And Customer Shape

- Client kinds:
- Customer-subject kinds:
- Hosted by Opensoft, client, or hybrid:
- Runtime operator:
- Secret provider owner:
- Production incident response owner:
- Isolation required per client:
- Isolation required per customer-subject:
- Data or memory shared across clients:
- Data or memory shared across customer-subjects:
- Identifiers allowed in repo examples:
- Identifiers allowed only in runtime or tenant config:

## Workflows

- First read-only workflow:
- First privileged or high-risk workflow:
- Highest risk level:
- Required gates:
- Required evidence:
- Blocking conditions:
- Final enforcement or handoff system:
- Rollback, repair, or correction path:

## Omnigent

- Domain Omnigent overlay:
- Repo-declared worker or expert classes:
- Inferred worker or expert classes:
- Allowed read actions:
- Allowed write actions:
- Recommendation-only actions:
- Stop conditions:
- Ambiguity routing:
- Required audit outputs:

## Credentials

- External systems:
- Repo-declared credential requirements:
- Inferred credential requirements:
- Blocked credential decisions:
- Read-only requirements:
- Write/admin/publish/send/deploy/care-affecting/money-moving/destructive
  requirements:
- Domain Hermes approval requirements:
- Client Hermes approval requirements:
- Customer Hermes consent or authorization requirements:
- Human approval requirements:
- Allowed secret providers:
- Rotation owner:
- Maximum runtime grant duration:
- Revocation triggers:
- Mandatory audit fields:

## Source Authority

- Source workspace providers:
- Domain knowledge sources:
- Client-specific sources:
- Customer-subject sources:
- Claims that can rely on synthesis:
- Claims that require ground-source verification:
- Citation and trace requirements:

## Examples And Validation

- Golden-path example:
- Blocked-path example:
- Repair or exception example:
- Required schemas:
- Local validation command:
- Tenant-ready definition:
- Starter placeholders remaining:
- Domain files required before next run:
- Client instantiation decisions still required:
""",
        "docs/setup-runbook.md": md_header(ctx) + f"""# {ctx.product_name} Setup Runbook

Use this runbook after completing [Pre-Run Questionnaire](pre-run-questionnaire.md).

## Setup Steps

1. Mark answer quality as declared, inferred, simulated, confirmed, or approved.
2. Confirm the domain interpretation.
3. Normalize any legacy `subject_layer` vocabulary into domain Hermes, client
   Hermes, and customer Hermes.
4. Confirm the three Hermes layer names and authority boundaries.
5. Confirm client and customer-subject isolation.
6. Fill `stack.yaml`.
7. Fill profile files.
8. Fill model files.
9. Fill Hermes overlays.
10. Fill Hermes Mixture of Agents profiles.
11. Fill credential requirements and broker contract.
12. Fill Omnigent worker capabilities, command policy, and tool routing.
13. Add workflow specs.
14. Add schemas.
15. Add examples.
16. Run local validation.
17. Produce a setup decision record.
18. Mark what remains domain implementation, client instantiation, and runtime
    approval.

## Setup Modes

| Mode | Meaning | Allowed Work |
| --- | --- | --- |
| `concept` | Domain language exists but implementation contracts are thin. | Add questionnaire answers, docs, missing scaffold, and inferred gaps. |
| `domain_implementation` | Domain repo is being made implementable. | Add workflows, schemas, overlays, credential requirements, examples, and validation. |
| `profile_setup` | A reusable deployment profile is being defined. | Add profile constraints, enabled workflows, client/customer kinds, and policy overrides. |
| `client_instantiation` | A real client or tenant is being configured. | Add non-secret client references, approver references, bindings, and isolation choices. |
| `customer_subject_instantiation` | A real customer-subject is being configured. | Add runtime-only subject references through approved systems, not repo secrets. |

The starter may operate in `concept`, `domain_implementation`, and
`profile_setup` modes. Client and customer-subject instantiation require
authorized runtime decisions.

## Stop Rules

Stop before applying changes when:

- raw secrets or private runtime records are provided
- the three Hermes layer mapping is unresolved
- a privileged workflow lacks credential requirements
- live client approvers or vault references are needed but unavailable
- a domain-specific law, professional authority, or customer-facing risk is
  unresolved
- an inferred answer would be promoted to an approved answer without
  stakeholder confirmation

## Required Pre-Run Outputs

- named domain, client, and customer Hermes layers
- answer quality marker
- legacy subject-layer normalization when present
- client kinds
- customer-subject kinds
- first read-only workflow
- first privileged or high-risk workflow
- credential requirement families
- Hermes Mixture of Agents profile requirements
- allowed secret providers
- human approval rules
- source authority rules
- golden-path example plan
- blocked-path example plan
- local validation command
- implementation gap list

## Implementation Agent Rules

The implementation agent may scaffold, validate, and recommend. It must not
invent live provider scopes, customer consent, raw credentials, client vault
names, staff approvals, professional authority, or production maintenance
windows.
""",
        "docs/credentialing.md": md_header(ctx) + f"""# {ctx.product_name} Credentialing

This domain must not store raw credentials. Credentials live in approved secret
providers. Workers receive only short-lived scoped runtime capability grants.

## Credential Families

Fill domain-specific credential families in `credentials/requirements.yaml`.
""",
        "docs/domain-overview.md": md_header(ctx) + f"""# {ctx.product_name} Domain Overview

{ctx.product_name} is the {ctx.category} implementation of the domain-neutral
openxFactory rail.

```text
openxFactory
  -> neutral contracts, gates, traceability, routing, state transitions, and audit

{ctx.product_name}
  -> domain agents, domain Hermes overlays, domain workflows, provider
     adapters, validation checks, and domain-specific evidence
```

The boundary is simple: openxFactory defines how governed work moves, while
{ctx.product_name} defines what {ctx.category} work means inside that rail.
""",
        "docs/customer-hermes-model.md": md_header(ctx) + f"""# {ctx.customer_layer_name} Model

{ctx.customer_layer_name} carries customer-scoped context for this domain.

It should preserve:

- customer subject identity
- current customer-subject state
- customer-specific memory
- consent, authorization, or operating permission boundaries
- active workflow context
- evidence and follow-up state

{ctx.customer_layer_name} should not become the global source of domain truth.
Those authorities remain with {ctx.client_layer_name}, {ctx.domain_layer_name},
domain policy, and required human review.
""",
        "docs/workflow-gates.md": md_header(ctx) + f"""# {ctx.product_name} Workflow Gates

Every domain workflow should expose gate records that name:

- gate ID
- owning Hermes or execution layer
- required evidence
- required credential grants
- unresolved risks
- next allowed transition
- blocking behavior

Default starter gates:

- request readiness
- client policy review
- customer context review
- credential grant review
- execution readiness
- validation evidence review
- final outcome audit
""",
        "docs/omnigent-constitution.md": md_header(ctx) + f"""# {ctx.display_name} Omnigent Constitution

{ctx.display_name} Omnigent runs domain agents inside Hermes policy and
openxFactory gates.

Agents may prepare plans, evidence packets, drafts, analyses, validation
reports, and recommendations. They may not override Hermes approval, bypass
credential policy, execute outside an approved workflow, or make final
authority decisions reserved for humans or external enforcement systems.

Every privileged, externally visible, regulated, or destructive action must
pass through the required workflow gates.
""",
        "docs/hermes-agent-mixes.md": md_header(ctx) + f"""# {ctx.product_name} Hermes Agent Mixes

Hermes Mixture of Agents profiles are advisory reasoning presets used inside
{ctx.domain_layer_name}, {ctx.client_layer_name}, or {ctx.customer_layer_name}.

They do not create a new authority layer. Reference agents provide independent
review, optional vote or deliberation rounds add structure, the acting Hermes
role synthesizes the recommendation, and the owning Hermes gate or review
council decides whether work may proceed.

## Council Modes

| Mode | Use |
| --- | --- |
| `panel_synthesis` | Independent opinions followed by acting Hermes synthesis. This is the closest fit to native Hermes Mixture of Agents. |
| `scored_vote` | Independent opinions plus explicit votes or scores before acting Hermes synthesis. |
| `deliberative_council` | Independent opinions, disagreement summary, rebuttal, revised positions, consensus or dissent record, then acting Hermes recommendation. |

## Required Rules

- Reference agents are advisory only.
- Reference agents do not receive tool access.
- Reference agents do not receive runtime credential grants.
- Reference agents receive only approved and redacted context packets.
- Acting Hermes roles may request tools only through openxFactory gates.
- Mix output is recommendation evidence, not approval.
- Dissent must be preserved for high-risk work.

## Starter Profiles

- `hermes/domain/agent-mixes.yaml`
- `hermes/client/agent-mixes.template.yaml`
- `hermes/customer/agent-mixes.template.yaml`

Replace the starter profiles with domain-owned profiles before live
instantiation.
""",
        "models/action-classes.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_action_classes

action_classes:
  - id: read
    description: Read approved state, metadata, or records.
    default_risk: low
  - id: write
    description: Create or update approved state.
    default_risk: moderate
  - id: admin
    description: Perform privileged administration.
    default_risk: privileged
  - id: destructive
    description: Delete, disable, purge, revoke, overwrite, or remove access.
    default_risk: high
""",
        "models/risk-levels.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_risk_levels

risk_levels:
  - id: low
    requires_human_approval: false
  - id: moderate
    requires_human_approval: true
  - id: high
    requires_human_approval: true
    requires_rollback_plan: true
  - id: privileged
    requires_human_approval: true
""",
        "models/command-classes.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_command_classes

command_classes:
  - id: readonly
    action_classes:
      - read
  - id: privileged
    action_classes:
      - read
      - write
      - admin
""",
        "models/customer-kinds.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_customer_kinds

customer_kinds: []
""",
        "models/client-kinds.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_client_kinds

client_kinds: []
""",
        "models/evidence-types.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_evidence_types

evidence_types:
  - id: approval_packet
  - id: runtime_capability_grant
  - id: preflight_report
  - id: operation_plan
  - id: validation_report
  - id: credential_audit_summary
  - id: revocation_record
  - id: agent_mix_evidence
""",
        "profiles/README.md": md_header(ctx) + "# Profiles\n\nProfiles define deployable shapes for this domain.\n",
        "workflows/README.md": md_header(ctx) + "# Workflows\n\nWorkflow specs belong in this folder.\n",
        "workflows/example-readonly.yaml": yaml_header(ctx) + f"""schema_version: 1
kind: xfactory_workflow

workflow:
  id: example_readonly
  display_name: Example Read-Only Workflow
  risk_level: low
  credential_requirements:
    - example_system_read
  allowed_actions:
    - read_customer_context
  required_approvals:
    domain_hermes: false
    client_hermes: true
    customer_hermes: true
    human: false
""",
        "workflows/example-privileged.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_workflow

workflow:
  id: example_privileged
  display_name: Example Privileged Workflow
  risk_level: high
  required_mix_profiles:
    - high_risk_action_deliberative_council
  credential_requirements:
    - example_system_write
  allowed_actions:
    - update_customer_context
  required_approvals:
    domain_hermes: true
    client_hermes: true
    customer_hermes: true
    human: true
""",
        "hermes/domain/overlay.yaml": yaml_header(ctx) + f"""schema_version: 1
kind: hermes_domain_overlay

domain:
  id: {ctx.domain_id}
  display_name: {ctx.domain_layer_name}
""",
        "hermes/domain/agent-mixes.yaml": yaml_header(ctx) + """schema_version: 1
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

  - id: privileged_action_scored_vote
    layer: domain_hermes
    mode: scored_vote
    purpose: score a privileged action before the acting Hermes role synthesizes a recommendation
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
    tool_policy:
      reference_agents_have_tools: false
      acting_agent_tool_access: gated
    credential_policy:
      reference_agents_receive_runtime_grants: false
      acting_agent_may_request_grant: true
      grant_source: openxFactory_credential_broker
    evidence_required:
      - reference_agent_summaries
      - vote_record
      - score_summary
      - acting_agent_synthesis
      - dissent_summary
      - risk_classification
      - approval_basis
      - redaction_level
    escalation_rules:
      escalate_on_dissent: true
      escalate_on_missing_evidence: true
      escalate_on_policy_conflict: true
      escalate_on_tie: true

  - id: high_risk_action_deliberative_council
    layer: domain_hermes
    mode: deliberative_council
    purpose: run a disagreement and rebuttal council before high-risk action recommendation
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
    tool_policy:
      reference_agents_have_tools: false
      acting_agent_tool_access: gated
    credential_policy:
      reference_agents_receive_runtime_grants: false
      acting_agent_may_request_grant: true
      grant_source: openxFactory_credential_broker
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
""",
        "hermes/domain/memory-boundaries.yaml": yaml_header(ctx) + """schema_version: 1
kind: hermes_memory_boundaries

domain_memory:
  shared: true
  excludes_raw_credentials: true
  requires_review_before_update: true
""",
        "hermes/domain/escalation-rules.yaml": yaml_header(ctx) + """schema_version: 1
kind: hermes_escalation_rules

requires_domain_review: []
""",
        "hermes/domain/policies/README.md": md_header(ctx) + "# Domain Policies\n\nDomain Hermes policies belong here.\n",
        "hermes/domain/review-councils/README.md": md_header(ctx) + "# Review Councils\n\nDomain review council definitions belong here.\n",
        "hermes/client/template.yaml": yaml_header(ctx) + f"""schema_version: 1
kind: client_hermes_template

client_hermes:
  layer_name: {ctx.client_layer_name}
  owns:
    - client organization identity
    - local operating policy
    - staff and escalation contacts
    - credential binding references
""",
        "hermes/client/agent-mixes.template.yaml": yaml_header(ctx) + """schema_version: 1
kind: hermes_client_agent_mix_template

client_agent_mix_overrides:
  may_strengthen_domain_profiles: true
  may_weaken_domain_profiles: false
  default_decision_status: recommendation_only
  reference_agents_have_tools: false
  reference_agents_receive_runtime_grants: false
  override_examples:
    - profile_id: high_risk_action_deliberative_council
      additional_reference_roles:
        - client_policy_reviewer
        - client_integration_owner
      additional_evidence_required:
        - client_policy_basis
        - client_approver_reference
""",
        "hermes/client/memory-boundaries.yaml": yaml_header(ctx) + """schema_version: 1
kind: client_memory_boundaries

client_memory:
  client_scoped: true
  excludes_raw_credentials: true
  domain_shared_by_default: false
""",
        "hermes/client/policy-overrides.yaml": yaml_header(ctx) + """schema_version: 1
kind: client_policy_overrides

policy_overrides:
  may_strengthen_domain_gates: true
  may_weaken_domain_gates: false
""",
        "hermes/client/integration-boundaries.yaml": yaml_header(ctx) + """schema_version: 1
kind: client_integration_boundaries

integrations:
  store_references_only: true
  raw_credentials_allowed: false
  client_binding_required: true
""",
        "hermes/customer/template.yaml": yaml_header(ctx) + f"""schema_version: 1
kind: customer_hermes_template

customer_hermes:
  layer_name: {ctx.customer_layer_name}
  customer_kinds: []
""",
        "hermes/customer/agent-mixes.template.yaml": yaml_header(ctx) + """schema_version: 1
kind: hermes_customer_agent_mix_template

customer_agent_mix_rules:
  default_decision_status: recommendation_only
  reference_agents_have_tools: false
  reference_agents_receive_runtime_grants: false
  customer_context_requires_redaction: true
  customer_private_memory_shared_by_default: false
  allowed_uses:
    - customer_context_review
    - consent_or_authorization_review
    - follow_up_readiness_review
  prohibited_uses:
    - direct_privileged_action_approval
    - raw_secret_review
    - unrestricted_private_record_review
""",
        "hermes/customer/memory-boundaries.yaml": yaml_header(ctx) + """schema_version: 1
kind: customer_memory_boundaries

customer_memory:
  customer_scoped: true
  excludes_raw_credentials: true
  domain_shared_by_default: false
""",
        "hermes/customer/consent-model.yaml": yaml_header(ctx) + """schema_version: 1
kind: customer_authorization_model

authorization:
  approval_required_for_privileged_actions: true
""",
        "omnigent/domain-overlay.yaml": yaml_header(ctx) + f"""schema_version: 1
kind: omnigent_domain_overlay

domain:
  id: {ctx.domain_id}
  orchestrator_profile: {ctx.orchestrator_profile}
""",
        "omnigent/worker-capabilities.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_worker_capabilities

worker_capabilities:
  - id: readonly
    command_classes:
      - readonly
  - id: privileged
    command_classes:
      - privileged
""",
        "omnigent/command-policy.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_command_policy

command_policy:
  require_human_approval_for:
    - admin
    - destructive
  evidence_required:
    - runtime_capability_grant
    - credential_audit_summary
    - revocation_record
""",
        "omnigent/tool-routing.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_tool_routing

tool_routing:
  - workflow: example_readonly
    adapter: adapters/README.md
    required_worker_capability: readonly
""",
        "omnigent/expert-routing/README.md": md_header(ctx) + "# Expert Routing\n\nDomain expert routing rules belong here.\n",
        "omnigent/validation-checks/README.md": md_header(ctx) + "# Validation Checks\n\nValidation check definitions belong here.\n",
        "omnigent/output-templates/README.md": md_header(ctx) + "# Output Templates\n\nOutput templates belong here.\n",
        "adapters/README.md": md_header(ctx) + "# Adapters\n\nProvider adapter contracts belong here. Adapters must not store secrets.\n",
        "credentials/README.md": md_header(ctx) + f"""# {ctx.product_name} Credentials

This folder declares credential requirements for {ctx.product_name}.

This folder must not contain raw secrets.
""",
        "credentials/requirements.yaml": yaml_header(ctx) + f"""schema_version: 1
kind: xfactory_credential_requirements

domain:
  id: {ctx.domain_id}
  product_name: {ctx.product_name}

requirements:
  - id: example_system_read
    purpose: read approved customer context from an external system
    access_mode: delegated_api
    allowed_workflows:
      - example_readonly
    customer_scope: customer
    minimum_scopes:
      - read
    requires_domain_approval: true
    requires_customer_consent: false
    requires_human_approval: false
    max_grant_minutes: 30
    audit_required: true

  - id: example_system_write
    purpose: update approved customer context in an external system
    access_mode: delegated_api
    allowed_workflows:
      - example_privileged
    customer_scope: customer
    minimum_scopes:
      - write
    requires_domain_approval: true
    requires_customer_consent: true
    requires_human_approval: true
    max_grant_minutes: 15
    audit_required: true
""",
        "credentials/broker-contract.yaml": yaml_header(ctx) + f"""schema_version: 1
kind: xfactory_credential_broker_contract

broker:
  id: {ctx.domain_id}-credential-broker
  resolves:
    - credential_requirements
    - client_bindings
    - approval_packets
  issues:
    - runtime_capability_grant
  must:
    - verify_approval
    - verify_binding
    - enforce_scope
    - enforce_expiration
    - write_audit_record
    - support_revocation
  must_not:
    - expose_raw_secret_to_worker
    - write_secret_to_logs
    - write_secret_to_repo
""",
        "credentials/bindings.template.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_credential_binding_template

client:
  id: <client-id>
  display_name: <client-display-name>

credential_bindings:
  example_system_read:
    provider: azure_key_vault
    vault: <client-vault-name>
    secret_ref: <secret-reference-name>
    owner: <client-or-opensoft>
    rotation_policy: client_managed
""",
        "credentials/grants.template.yaml": yaml_header(ctx) + f"""schema_version: 1
kind: xfactory_runtime_capability_grant_template

runtime_capability_grant:
  id: <grant-id>
  job_id: <job-id>
  client_id: <client-id>
  domain: {ctx.domain_id}
  requirement_id: example_system_read
  issued_by: hermes_credential_broker
  approved_by: domain_hermes
  customer_ref: <customer-ref>
  allowed_workflows:
    - example_readonly
  allowed_actions:
    - read_customer_context
  expires_at: <timestamp>
  audit_ref: <audit-ref>
""",
        "credentials/audit.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_credential_audit_policy

audit:
  required: true
  minimum_fields:
    - grant_id
    - job_id
    - domain
    - client_id
    - customer_ref
    - requirement_id
    - binding_ref
    - requested_by
    - approved_by
    - issued_by
    - worker_id
    - allowed_actions
    - issued_at
    - expires_at
    - revoked_at
    - outcome
    - evidence_refs
""",
        "credentials/policies/approval-policy.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_credential_approval_policy

approval_policy:
  default_requires_domain_hermes: true
  default_requires_human_approval: false
  always_require_human_approval:
    - admin_access
    - delete_access
    - external_send
    - production_deployment
  deny_by_default_when:
    - workflow_not_approved
    - client_binding_missing
    - requested_scope_exceeds_requirement
    - customer_consent_missing
    - grant_duration_exceeds_policy
""",
        "credentials/policies/rotation-policy.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_credential_rotation_policy

rotation_policy:
  default_owner: client
  supported_owners:
    - client
    - opensoft
    - provider
""",
        "credentials/policies/revocation-policy.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_credential_revocation_policy

revocation_policy:
  revoke_runtime_grant_when:
    - job_completes
    - grant_expires
    - client_revokes_authorization
    - customer_consent_withdrawn
    - worker_session_terminates
    - workflow_leaves_approved_scope
""",
        "tenants/README.md": md_header(ctx) + "# Tenants\n\nClient or tenant examples belong here. Do not store raw secrets.\n",
        "tenants/examples/example-client.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_client_example

client:
  id: example_client
  display_name: Example Client
""",
        "schemas/README.md": md_header(ctx) + "# Schemas\n\nSchema files belong here.\n",
        "schemas/stack.schema.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_schema

schema:
  id: stack
  applies_to_kind: xfactory_domain_stack
  required_paths:
    - domain.id
    - domain.product_name
    - xfactory.contract_repo
    - hermes.domain_overlay
    - hermes.domain_agent_mixes
    - hermes.client_overlay
    - hermes.client_agent_mixes_template
    - hermes.customer_overlay
    - hermes.customer_agent_mixes_template
    - omnigent.domain_overlay
    - credentials.requirements
    - credentials.broker_contract
    - tenancy.isolation.memory
""",
        "schemas/workflow.schema.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_schema

schema:
  id: workflow
  applies_to_kind: xfactory_workflow
  required_paths:
    - workflow.id
    - workflow.display_name
    - workflow.risk_level
    - workflow.credential_requirements
    - workflow.allowed_actions
    - workflow.required_approvals
""",
        "schemas/credential-requirements.schema.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_schema

schema:
  id: credential_requirements
  applies_to_kind: xfactory_credential_requirements
  required_paths:
    - domain.id
    - domain.product_name
    - requirements
""",
        "schemas/agent-mixes.schema.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_schema

schema:
  id: agent_mixes
  applies_to_kind: hermes_agent_mix_profiles
  allowed_modes:
    - panel_synthesis
    - scored_vote
    - deliberative_council
  required_paths:
    - mix_profiles
""",
        "schemas/instantiation-questionnaire.schema.yaml": yaml_header(ctx) + """schema_version: 1
kind: xfactory_schema

schema:
  id: instantiation_questionnaire
  applies_to_kind: xfactory_instantiation_prerun_answers
  required_paths:
    - answer_metadata.status
    - answer_metadata.scope
    - domain.repo
    - domain.category
    - hermes_layers.domain_hermes
    - hermes_layers.client_hermes
    - hermes_layers.customer_hermes
    - hermes_mixture.enabled
    - hermes_mixture.default_decision_status
    - hermes_mixture.reference_agents_have_tools
    - hermes_mixture.reference_agents_receive_runtime_grants
    - hermes_mixture.profile_modes
    - legacy_normalization.uses_legacy_subject_layer
    - instantiation.level
    - workflow_seed.readonly_workflow
    - workflow_seed.privileged_workflow
    - credentials.raw_secrets_in_repo_allowed
    - validation.local_command
    - implementation_gaps.starter_placeholders_remaining
""",
        "examples/README.md": md_header(ctx) + "# Examples\n\nExample packets and dry-run artifacts belong here.\n",
        "examples/instantiation-answers.example.yaml": yaml_header(ctx) + f"""schema_version: 1
kind: xfactory_instantiation_prerun_answers

answer_metadata:
  status: starter_placeholder
  scope: domain
  generated_from:
    - stack.yaml
    - openxFactory starter
  assumptions:
    - Replace placeholder values before implementation.
  must_confirm_before_instantiation:
    - client kind
    - customer-subject kind
    - secret provider
    - approver references

domain:
  repo: {ctx.product_name}
  category: {ctx.category}
  closest_existing_domain: <MedxFactory|OpsxFactory|codexFactory|AdxFactory|LedgerxFactory>

hermes_layers:
  domain_hermes: {ctx.domain_layer_name}
  client_hermes: {ctx.client_layer_name}
  customer_hermes: {ctx.customer_layer_name}

hermes_mixture:
  enabled: true
  default_decision_status: recommendation_only
  reference_agents_have_tools: false
  reference_agents_receive_runtime_grants: false
  required_profiles:
    - high_risk_action_deliberative_council
  repo_declared_profiles:
    - setup_readiness_panel_synthesis
    - privileged_action_scored_vote
    - high_risk_action_deliberative_council
  inferred_profiles:
    - privileged_action_scored_vote
  profile_modes:
    setup_readiness_panel_synthesis: panel_synthesis
    privileged_action_scored_vote: scored_vote
    high_risk_action_deliberative_council: deliberative_council
  context_rules:
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
    default_redaction_level: customer_redacted
  acting_roles:
    setup_readiness_panel_synthesis: hermes_setup_reviewer
    privileged_action_scored_vote: hermes_approval_controller
    high_risk_action_deliberative_council: hermes_approval_controller
  scored_vote:
    privileged_action_scored_vote:
      vote_values:
        - approve
        - approve_with_conditions
        - reject
        - abstain
      scoring_criteria:
        - policy_fit
        - evidence_completeness
        - credential_scope_fit
      approval_threshold: majority
      tie_breaker: escalate_to_human
  deliberative_council:
    high_risk_action_deliberative_council:
      rounds:
        - independent_positions
        - disagreement_summary
        - rebuttal
        - revised_positions
        - final_recommendation
      preserve_unresolved_dissent: true
      escalation_for_unresolved_dissent: escalate_to_human
  evidence_required:
    - reference_agent_summaries
    - vote_record
    - score_summary
    - disagreement_summary
    - rebuttal_record
    - revised_positions
    - consensus_summary
    - unresolved_dissent
    - acting_agent_synthesis
    - dissent_summary

legacy_normalization:
  uses_legacy_subject_layer: false
  legacy_subject_layer_name: null
  normalized_client_layer_name: {ctx.client_layer_name}
  normalized_customer_layer_name: {ctx.customer_layer_name}

instantiation:
  level: <domain|profile|client|tenant|customer_subject>
  hosted_by: <opensoft|client|hybrid>
  client_kind: <client-kind>
  customer_subject_kind: <customer-subject-kind>

workflow_seed:
  readonly_workflow: example_readonly
  privileged_workflow: example_privileged
  highest_risk_level: high

credentials:
  raw_secrets_in_repo_allowed: false
  secret_provider: <provider-or-tbd>
  runtime_grants_required: true

validation:
  local_command: make validate
  golden_path_required: true
  blocked_path_required: true

implementation_gaps:
  starter_placeholders_remaining:
    - examples/golden-path
  domain_files_required:
    - domain workflow specs
    - provider adapter contracts
  client_instantiation_required:
    - approver references
    - vault or secret provider references
""",
        "examples/golden-path/README.md": md_header(ctx) + f"""# Golden Path

This folder should hold the first complete dry-run path for {ctx.product_name}.

Recommended artifacts:

1. Client example
2. Customer subject example
3. Workflow request
4. Approval packet
5. Agent mix evidence
6. Runtime capability grant
7. Operation plan
8. Validation report
9. Audit summary
10. Revocation record
""",
        "scripts/validate-domain-factory.py": validate_script(),
    }


def validate_script() -> str:
    return '''#!/usr/bin/env python3
"""Lightweight validation for an xFactory domain starter scaffold."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "Makefile",
    "stack.yaml",
    "docs/domain-overview.md",
    "docs/workflow-gates.md",
    "docs/customer-hermes-model.md",
    "docs/omnigent-constitution.md",
    "docs/hermes-agent-mixes.md",
    "docs/pre-run-questionnaire.md",
    "docs/setup-runbook.md",
    "hermes/domain/agent-mixes.yaml",
    "hermes/client/agent-mixes.template.yaml",
    "hermes/customer/agent-mixes.template.yaml",
    "credentials/requirements.yaml",
    "credentials/broker-contract.yaml",
    "credentials/bindings.template.yaml",
    "credentials/grants.template.yaml",
    "credentials/audit.yaml",
    "models/action-classes.yaml",
    "models/risk-levels.yaml",
    "models/command-classes.yaml",
    "omnigent/worker-capabilities.yaml",
    "omnigent/command-policy.yaml",
    "omnigent/tool-routing.yaml",
    "workflows/example-readonly.yaml",
    "workflows/example-privileged.yaml",
    "schemas/stack.schema.yaml",
    "schemas/workflow.schema.yaml",
    "schemas/credential-requirements.schema.yaml",
    "schemas/agent-mixes.schema.yaml",
    "schemas/instantiation-questionnaire.schema.yaml",
    "examples/instantiation-answers.example.yaml",
    "examples/golden-path/README.md",
]

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?i)(client_secret|password|api_key)\\s*=\\s*['\\"]?[A-Za-z0-9_./+=-]{12,}"),
    re.compile(r"\\bsk-[A-Za-z0-9]{20,}\\b"),
]


def load_yaml(rel: str) -> dict:
    data = yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def ids_from(items: object) -> set[str]:
    if not isinstance(items, list):
        return set()
    return {str(item.get("id")) for item in items if isinstance(item, dict) and item.get("id")}


def value_at(data: dict, dotted_path: str) -> object:
    current: object = data
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def validate_required_paths(data: dict, required_paths: list[str], label: str, errors: list[str]) -> None:
    for dotted_path in required_paths:
        value = value_at(data, dotted_path)
        if value in (None, "", []):
            errors.append(f"{label} missing required path: {dotted_path}")


def validate_pre_run_answers(errors: list[str]) -> None:
    rel = "examples/instantiation-answers.example.yaml"
    answers = load_yaml(rel)
    validate_required_paths(
        answers,
        [
            "answer_metadata.status",
            "answer_metadata.scope",
            "domain.repo",
            "domain.category",
            "hermes_layers.domain_hermes",
            "hermes_layers.client_hermes",
            "hermes_layers.customer_hermes",
            "hermes_mixture.enabled",
            "hermes_mixture.default_decision_status",
            "hermes_mixture.reference_agents_have_tools",
            "hermes_mixture.reference_agents_receive_runtime_grants",
            "hermes_mixture.profile_modes",
            "legacy_normalization.uses_legacy_subject_layer",
            "instantiation.level",
            "workflow_seed.readonly_workflow",
            "workflow_seed.privileged_workflow",
            "credentials.raw_secrets_in_repo_allowed",
            "validation.local_command",
            "implementation_gaps.starter_placeholders_remaining",
        ],
        rel,
        errors,
    )
    allowed_statuses = {
        "starter_placeholder",
        "declared",
        "inferred",
        "simulated",
        "confirmed",
        "approved_for_instantiation",
    }
    status = value_at(answers, "answer_metadata.status")
    if status and status not in allowed_statuses:
        errors.append(f"{rel} has unknown answer_metadata.status: {status}")
    if value_at(answers, "credentials.raw_secrets_in_repo_allowed") is not False:
        errors.append(f"{rel} must set credentials.raw_secrets_in_repo_allowed: false")
    if value_at(answers, "hermes_mixture.reference_agents_have_tools") is not False:
        errors.append(f"{rel} must set hermes_mixture.reference_agents_have_tools: false")
    if value_at(answers, "hermes_mixture.reference_agents_receive_runtime_grants") is not False:
        errors.append(f"{rel} must set hermes_mixture.reference_agents_receive_runtime_grants: false")
    if value_at(answers, "hermes_mixture.default_decision_status") not in (None, "recommendation_only"):
        errors.append(f"{rel} hermes_mixture.default_decision_status must be recommendation_only")
    profile_modes = value_at(answers, "hermes_mixture.profile_modes")
    if isinstance(profile_modes, dict):
        allowed_modes = {"panel_synthesis", "scored_vote", "deliberative_council"}
        for profile_id, mode in profile_modes.items():
            if mode not in allowed_modes:
                errors.append(f"{rel} hermes_mixture.profile_modes.{profile_id} has unknown mode: {mode}")
    legacy = value_at(answers, "legacy_normalization.uses_legacy_subject_layer")
    if legacy is True:
        validate_required_paths(
            answers,
            [
                "legacy_normalization.legacy_subject_layer_name",
                "legacy_normalization.normalized_client_layer_name",
                "legacy_normalization.normalized_customer_layer_name",
            ],
            rel,
            errors,
        )


def validate_pre_run_workflow_seed(workflow_ids: set[str], risks: set[str], errors: list[str]) -> None:
    rel = "examples/instantiation-answers.example.yaml"
    answers = load_yaml(rel)
    for dotted_path in ["workflow_seed.readonly_workflow", "workflow_seed.privileged_workflow"]:
        workflow_id = value_at(answers, dotted_path)
        if isinstance(workflow_id, str) and workflow_id.startswith("<"):
            continue
        if workflow_id and workflow_id not in workflow_ids:
            errors.append(f"{rel} {dotted_path} references unknown workflow: {workflow_id}")
    risk = value_at(answers, "workflow_seed.highest_risk_level")
    if isinstance(risk, str) and risk.startswith("<"):
        return
    if risk and risk not in risks:
        errors.append(f"{rel} workflow_seed.highest_risk_level references unknown risk level: {risk}")


def validate_agent_mixes(errors: list[str]) -> set[str]:
    rel = "hermes/domain/agent-mixes.yaml"
    data = load_yaml(rel)
    profiles = data.get("mix_profiles")
    if not isinstance(profiles, list) or not profiles:
        errors.append(f"{rel} must define at least one mix_profiles entry")
        return set()

    profile_ids: set[str] = set()
    allowed_modes = {"panel_synthesis", "scored_vote", "deliberative_council"}
    for profile in profiles:
        if not isinstance(profile, dict):
            errors.append(f"{rel} mix_profiles entries must be mappings")
            continue
        profile_id = profile.get("id")
        if not profile_id:
            errors.append(f"{rel} mix profile missing id")
            continue
        profile_ids.add(str(profile_id))
        mode = profile.get("mode")
        if mode not in allowed_modes:
            errors.append(f"{rel} {profile_id} must set mode to one of: {', '.join(sorted(allowed_modes))}")
        if value_at(profile, "tool_policy.reference_agents_have_tools") is not False:
            errors.append(f"{rel} {profile_id} must set tool_policy.reference_agents_have_tools: false")
        if value_at(profile, "credential_policy.reference_agents_receive_runtime_grants") is not False:
            errors.append(
                f"{rel} {profile_id} must set credential_policy.reference_agents_receive_runtime_grants: false"
            )
        prohibited = profile.get("prohibited_context")
        if not isinstance(prohibited, list) or "raw_credentials" not in prohibited:
            errors.append(f"{rel} {profile_id} must prohibit raw_credentials")
        evidence = profile.get("evidence_required")
        if not isinstance(evidence, list) or "dissent_summary" not in evidence:
            errors.append(f"{rel} {profile_id} must require dissent_summary evidence")
        if mode == "scored_vote":
            scoring = profile.get("scoring_criteria")
            if not isinstance(scoring, list) or not scoring:
                errors.append(f"{rel} {profile_id} scored_vote must define scoring_criteria")
            if not isinstance(profile.get("voting_policy"), dict):
                errors.append(f"{rel} {profile_id} scored_vote must define voting_policy")
            for required_evidence in ["vote_record", "score_summary"]:
                if not isinstance(evidence, list) or required_evidence not in evidence:
                    errors.append(f"{rel} {profile_id} scored_vote must require {required_evidence} evidence")
        if mode == "deliberative_council":
            deliberation_policy = profile.get("deliberation_policy")
            if not isinstance(deliberation_policy, dict):
                errors.append(f"{rel} {profile_id} deliberative_council must define deliberation_policy")
                rounds = []
            else:
                rounds = deliberation_policy.get("rounds")
            required_rounds = [
                "independent_positions",
                "disagreement_summary",
                "rebuttal",
                "revised_positions",
                "final_recommendation",
            ]
            if not isinstance(rounds, list) or any(required_round not in rounds for required_round in required_rounds):
                errors.append(f"{rel} {profile_id} deliberative_council must define all required rounds")
            for required_evidence in [
                "disagreement_summary",
                "rebuttal_record",
                "revised_positions",
                "consensus_summary",
                "unresolved_dissent",
            ]:
                if not isinstance(evidence, list) or required_evidence not in evidence:
                    errors.append(
                        f"{rel} {profile_id} deliberative_council must require {required_evidence} evidence"
                    )
            if value_at(profile, "escalation_rules.escalate_on_unresolved_dissent") is not True:
                errors.append(
                    f"{rel} {profile_id} deliberative_council must escalate_on_unresolved_dissent"
                )

    for rel in ["hermes/client/agent-mixes.template.yaml", "hermes/customer/agent-mixes.template.yaml"]:
        data = load_yaml(rel)
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "reference_agents_have_tools: false" not in text:
            errors.append(f"{rel} must keep reference_agents_have_tools: false")
        if "reference_agents_receive_runtime_grants: false" not in text:
            errors.append(f"{rel} must keep reference_agents_receive_runtime_grants: false")

    return profile_ids


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing required file: {rel}")
            continue
        if path.suffix in {".yaml", ".yml"}:
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                errors.append(f"invalid yaml: {rel}: {exc}")

    if not errors:
        stack = load_yaml("stack.yaml")
        for rel in [
            stack.get("hermes", {}).get("domain_overlay"),
            stack.get("hermes", {}).get("domain_agent_mixes"),
            stack.get("hermes", {}).get("client_overlay"),
            stack.get("hermes", {}).get("client_agent_mixes_template"),
            stack.get("hermes", {}).get("customer_overlay"),
            stack.get("hermes", {}).get("customer_agent_mixes_template"),
            stack.get("omnigent", {}).get("domain_overlay"),
            stack.get("credentials", {}).get("requirements"),
            stack.get("credentials", {}).get("broker_contract"),
        ]:
            if rel and not (ROOT / rel).exists():
                errors.append(f"stack.yaml references missing path: {rel}")

        requirements = load_yaml("credentials/requirements.yaml")
        requirement_ids = ids_from(requirements.get("requirements"))
        risks = ids_from(load_yaml("models/risk-levels.yaml").get("risk_levels"))
        capabilities = ids_from(load_yaml("omnigent/worker-capabilities.yaml").get("worker_capabilities"))
        mix_profile_ids = validate_agent_mixes(errors)
        validate_pre_run_answers(errors)
        workflow_ids: set[str] = set()
        for workflow_path in sorted((ROOT / "workflows").glob("*.yaml")):
            workflow_doc = yaml.safe_load(workflow_path.read_text(encoding="utf-8")) or {}
            workflow = workflow_doc.get("workflow", {})
            workflow_id = workflow.get("id")
            if workflow_id:
                workflow_ids.add(str(workflow_id))
            for req in workflow.get("credential_requirements", []) or []:
                if req not in requirement_ids:
                    errors.append(f"{workflow_path.relative_to(ROOT)} references unknown credential requirement: {req}")
            risk = workflow.get("risk_level")
            if risk and risk not in risks:
                errors.append(f"{workflow_path.relative_to(ROOT)} references unknown risk level: {risk}")
            for mix_profile_id in workflow.get("required_mix_profiles", []) or []:
                if mix_profile_id not in mix_profile_ids:
                    errors.append(
                        f"{workflow_path.relative_to(ROOT)} references unknown mix profile: {mix_profile_id}"
                    )

        for route in load_yaml("omnigent/tool-routing.yaml").get("tool_routing", []) or []:
            if not isinstance(route, dict):
                continue
            workflow = route.get("workflow")
            if workflow and workflow not in workflow_ids:
                errors.append(f"omnigent/tool-routing.yaml references unknown workflow: {workflow}")
            capability = route.get("required_worker_capability")
            if capability and capability not in capabilities:
                errors.append(f"omnigent/tool-routing.yaml references unknown worker capability: {capability}")
        validate_pre_run_workflow_seed(workflow_ids, risks, errors)

    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirnames:
            dirnames.remove(".git")
        for filename in filenames:
            path = Path(dirpath) / filename
            rel_path = path.relative_to(ROOT)
            if rel_path == Path("scripts/validate-domain-factory.py"):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"possible secret pattern {pattern.pattern!r} in {rel_path}")

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("OK xFactory domain starter scaffold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def starter_owned_upgrade_reason(rel: str, existing: str) -> str | None:
    if (
        rel == "scripts/validate-domain-factory.py"
        and "starter scaffold" in existing
        and (
            "validate_pre_run_workflow_seed" not in existing
            or "validate_agent_mixes" not in existing
            or "deliberative_council" not in existing
        )
    ):
        return "upgraded starter-owned validator to current starter surface"
    if (
        rel == "docs/pre-run-questionnaire.md"
        and "starter_source: openxFactory/domain-factory-starter-pack" in existing
        and (
            "## Answer Quality" not in existing
            or "## Hermes Mixture Of Agents" not in existing
            or "deliberative_council" not in existing
        )
    ):
        return "upgraded starter-owned pre-run questionnaire to current starter model"
    if (
        rel == "docs/hermes-agent-mixes.md"
        and "starter_source: openxFactory/domain-factory-starter-pack" in existing
        and "deliberative_council" not in existing
    ):
        return "upgraded starter-owned Hermes agent mixes doc to current council-mode model"
    if (
        rel == "hermes/domain/agent-mixes.yaml"
        and "source: openxFactory/domain-factory-starter-pack" in existing
        and "deliberative_council" not in existing
    ):
        return "upgraded starter-owned Hermes agent mix profiles to current council-mode model"
    if (
        rel == "docs/setup-runbook.md"
        and "starter_source: openxFactory/domain-factory-starter-pack" in existing
        and ("## Setup Modes" not in existing or "Mixture of Agents" not in existing)
    ):
        return "upgraded starter-owned setup runbook to current starter model"
    if (
        rel == "examples/instantiation-answers.example.yaml"
        and "source: openxFactory/domain-factory-starter-pack" in existing
        and (
            "answer_metadata:" not in existing
            or "hermes_mixture:" not in existing
            or "deliberative_council" not in existing
        )
    ):
        return "upgraded starter-owned pre-run answer example to current starter model"
    if (
        rel == "schemas/instantiation-questionnaire.schema.yaml"
        and "source: openxFactory/domain-factory-starter-pack" in existing
        and (
            "answer_metadata.status" not in existing
            or "hermes_mixture.enabled" not in existing
            or "hermes_mixture.profile_modes" not in existing
        )
    ):
        return "upgraded starter-owned pre-run answer schema"
    if (
        rel == "schemas/agent-mixes.schema.yaml"
        and "source: openxFactory/domain-factory-starter-pack" in existing
        and "deliberative_council" not in existing
    ):
        return "upgraded starter-owned agent mixes schema"
    return None


def maybe_create(target: Path, path: Path, content: str, log: RunLog, dry_run: bool) -> None:
    rel = str(path.relative_to(target))
    if path.exists():
        try:
            existing = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            existing = ""
        upgrade_reason = starter_owned_upgrade_reason(rel, existing)
        if upgrade_reason:
            if not dry_run:
                path.write_text(content, encoding="utf-8")
                if path.name.endswith(".py"):
                    path.chmod(0o755)
            log.updated.append((rel, upgrade_reason))
            return
        log.skipped.append((rel, "exists; preserved"))
        return
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if path.name.endswith(".py"):
            path.chmod(0o755)
    log.created.append((rel, "missing starter file"))


def add_readme_links(target: Path, log: RunLog, dry_run: bool) -> None:
    readme = target / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    links = [
        "- [Implementation Runbook](docs/implementation-runbook.md)",
        "- [Implementation Guide](docs/implementation-guide.md)",
        "- [Pre-Run Questionnaire](docs/pre-run-questionnaire.md)",
        "- [Setup Runbook](docs/setup-runbook.md)",
        "- [Domain Overview](docs/domain-overview.md)",
        "- [Workflow Gates](docs/workflow-gates.md)",
        "- [Customer Hermes Model](docs/customer-hermes-model.md)",
        "- [Omnigent Constitution](docs/omnigent-constitution.md)",
        "- [Hermes Agent Mixes](docs/hermes-agent-mixes.md)",
        "- [Credentialing](docs/credentialing.md)",
        "- [Boundary](docs/boundary.md)",
    ]
    missing = [link for link in links if link not in text]
    if not missing:
        log.skipped.append(("README.md", "starter links already present"))
        return
    implementation_heading = re.search(r"(?m)^## Implementation\s*$", text)
    if not dry_run:
        if implementation_heading:
            section_start = implementation_heading.end()
            next_heading = re.search(r"(?m)^##\s+", text[section_start:])
            section_end = section_start + next_heading.start() if next_heading else len(text)
            updated = text[:section_end].rstrip() + "\n" + "\n".join(missing) + "\n" + text[section_end:]
        else:
            addition = "\n\n## Implementation\n\n" + "\n".join(missing) + "\n"
            updated = text.rstrip() + addition
        readme.write_text(updated, encoding="utf-8")
    log.updated.append(("README.md", "added missing implementation links"))


def validate_yaml(target: Path, log: RunLog) -> None:
    if yaml is None:
        log.validation.append("SKIP PyYAML is not available")
        return
    errors = []
    for path in target.rglob("*.yaml"):
        if ".git" in path.parts:
            continue
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.relative_to(target)}: {exc}")
    if errors:
        log.validation.extend(f"ERROR invalid yaml: {err}" for err in errors)
    else:
        log.validation.append("OK YAML files parse")


def validate_domain(target: Path, log: RunLog, dry_run: bool) -> None:
    validator = target / "scripts/validate-domain-factory.py"
    if dry_run:
        log.validation.append("SKIP domain validator not run during dry-run")
        return
    if not validator.exists():
        log.validation.append("SKIP domain validator not found")
        return
    result = subprocess.run(
        [sys.executable, str(validator)],
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
    )
    output = "\n".join(part.strip() for part in [result.stdout, result.stderr] if part.strip())
    if result.returncode == 0:
        log.validation.append(f"OK domain validator: {output or 'passed'}")
    else:
        log.validation.append(f"ERROR domain validator failed:\n{output or f'exit code {result.returncode}'}")


def write_report(target: Path, ctx: DomainContext, log: RunLog, dry_run: bool) -> None:
    report_path = target / "docs/starter-rerun-report.md"
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report_status = "would write starter rerun report" if dry_run else "wrote starter rerun report"
    log.updated.append((str(report_path.relative_to(target)), report_status))

    def table(rows: list[tuple[str, str]], headers: tuple[str, str]) -> str:
        if not rows:
            return "| None | |\n|---|---|\n"
        body = "\n".join(f"| `{a}` | {b} |" for a, b in rows)
        return f"| {headers[0]} | {headers[1]} |\n|---|---|\n{body}\n"

    conflict_body = (
        "| None | | |\n|---|---|---|\n"
        if not log.conflicts
        else "| File | Conflict | Recommended action |\n|---|---|---|\n"
        + "\n".join(f"| `{a}` | {b} | {c} |" for a, b, c in log.conflicts)
        + "\n"
    )

    report = f"""# Starter Rerun Report

Domain: {ctx.product_name}
Date: {now}
Starter: {STARTER_NAME}
Dry Run: {dry_run}

## Summary

- Created: {len(log.created)}
- Updated: {len(log.updated)}
- Skipped: {len(log.skipped)}
- Conflicts: {len(log.conflicts)}
- Validation: {'; '.join(log.validation) if log.validation else 'not run'}

## Created Files

{table(log.created, ('File', 'Reason'))}
## Updated Files

{table(log.updated, ('File', 'Change'))}
## Skipped Files

{table(log.skipped, ('File', 'Reason'))}
## Conflicts

{conflict_body}
## Validation

```text
{chr(10).join(log.validation) if log.validation else 'not run'}
```

## Next Work

1. Fill domain-specific workflows.
2. Fill provider-specific credential requirements.
3. Fill adapter contracts.
4. Fill client instantiation examples.
5. Replace placeholders with domain-owned content.
"""
    if not dry_run:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
    print(report)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Path to the target domain factory repo")
    parser.add_argument("--domain-id")
    parser.add_argument("--product-name")
    parser.add_argument("--display-name")
    parser.add_argument("--category")
    parser.add_argument("--domain-layer-name")
    parser.add_argument("--client-layer-name")
    parser.add_argument("--customer-layer-name")
    parser.add_argument("--orchestrator-profile")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = args.target.resolve()
    if not target.exists():
        target.mkdir(parents=True)
    if not target.is_dir():
        print(f"ERROR target is not a directory: {target}", file=sys.stderr)
        return 2

    ctx = infer_context(target, args)
    log = RunLog(created=[], updated=[], skipped=[], conflicts=[], validation=[])
    for rel, content in templates(ctx).items():
        maybe_create(target, target / rel, content, log, args.dry_run)
    add_readme_links(target, log, args.dry_run)
    validate_yaml(target, log)
    validate_domain(target, log, args.dry_run)
    write_report(target, ctx, log, args.dry_run)
    return 1 if any(item.startswith("ERROR") for item in log.validation) or log.conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
