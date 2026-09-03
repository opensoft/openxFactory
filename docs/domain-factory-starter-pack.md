# xFactory Domain Factory Starter Pack

Status: draft
Kind: template
Repository context: openxFactory
Purpose: provide starter instructions for stubbing out a new xFactory domain
repo, including the credentialing module every domain must specialize.

## 1. Scope

Use this starter pack when creating a domain repo such as:

- `MedxFactory`
- `OpsxFactory`
- `LedgerxFactory`
- `AdxFactory`
- `codexFactory`

A domain factory repo does not fork xFactory. It implements the
openxFactory/xFactory contract for one domain.

## 1.5. Implementation Agent Contract

An implementation agent using this starter pack must treat the starter as an
idempotent scaffold operation, not a one-time code dump.

The agent must:

1. Read this starter pack.
2. Inspect the target domain repo before writing.
3. Create missing starter files and directories.
4. Preserve domain-specific content that already exists.
5. Patch starter-owned placeholder sections only when safe.
6. Never overwrite a filled-in domain artifact without an explicit migration
   note and user approval.
7. Never write raw credentials, tokens, private keys, connection strings, or
   live tenant data.
8. Emit a rerun report that lists created files, updated files, skipped files,
   conflicts, and recommended next work.

The agent should operate in this order:

```text
1. Discover repo state.
2. Load stack.yaml if present.
3. Infer domain ID, product name, and Hermes layer names.
4. Compare repo state to the starter surface.
5. Create missing files from templates.
6. Update indexes such as README.md only with additive links.
7. Run validation.
8. Write or print a rerun report.
```

The agent must not assume it is omnipotent. It may scaffold, validate, and
recommend. Real credentials, client bindings, tenant approvals, provider
consent, and live workflow execution must come from authorized runtime or
client instantiation steps.

## 1.6. Idempotent Rerun Rules

The starter pack must be safe to run multiple times.

Rerun behavior:

```text
missing file
  create it from the current starter template

existing placeholder file
  update it when the file still has placeholder markers or no domain content

existing starter-owned validator
  update it when it matches a recognized old starter scaffold fingerprint

existing domain-filled file
  preserve it and report that it was skipped

existing file with conflicting old starter content
  write a migration recommendation, do not overwrite automatically

empty expected directory
  add a README.md placeholder

missing link in README or docs index
  add link without reordering unrelated content
```

A file is considered domain-filled when it contains domain-specific workflow
IDs, provider scopes, approval rules, client kinds, customer kinds, adapter
contracts, or hand-written explanations that are not starter placeholders.

Starter-generated files should include a small metadata block when practical:

```yaml
starter_metadata:
  source: openxFactory/domain-factory-starter-pack
  starter_version: 6
  domain_id: example
  generated_at: <timestamp-or-null>
  managed_mode: scaffold
```

`managed_mode: scaffold` means future reruns may update placeholder sections.
`managed_mode: domain_owned` means future reruns must preserve the file unless
the user explicitly requests migration.

The starter pack should aim for idempotence, not omnipotence. It cannot safely
infer real provider scopes, live client bindings, staff approvers, tenant vault
names, production maintenance windows, or domain-specific legal and compliance
requirements.

## 1.7. Starter Runner

The starter pack has a reference runner:

```text
scripts/apply-domain-starter.py
```

Use dry-run first:

```bash
scripts/apply-domain-starter.py --dry-run /path/to/<Domain>Factory
```

Apply for real:

```bash
scripts/apply-domain-starter.py /path/to/<Domain>Factory
```

The runner:

- infers domain metadata from `stack.yaml` when present
- creates missing starter files
- preserves existing files
- adds missing README implementation links
- parses YAML files
- runs the target repo validator when applying for real and the validator
  exists
- creates a pre-run questionnaire, setup runbook, and example pre-run answers
- creates Hermes Mixture of Agents docs, profiles, templates, and schema hooks
- creates the avatar-first UI profile and validation hooks
- creates product/service Tenant Hermes scaffold templates for offer catalog,
  client agents, skills, and user interactions
- creates Tenant Hermes installation discovery and workflow migration templates
  for document/email evidence, gap review, containment, cutover, and drift
  monitoring
- creates memory gateway placeholders that point at the canonical openxFactory
  contract without selecting a required memory provider
- marks pre-run answer quality as starter placeholder, declared, inferred,
  simulated, confirmed, or approved
- records legacy `subject_layer` normalization and implementation gaps
- writes `docs/starter-rerun-report.md`

The runner does not:

- overwrite domain-filled files
- infer real provider scopes
- create live credentials
- bind real client vaults
- perform OAuth consent
- execute live workflows

When creating a new empty repo, pass metadata explicitly if no `stack.yaml`
exists:

```bash
scripts/apply-domain-starter.py /path/to/NewFactory \
  --domain-id new \
  --product-name NewFactory \
  --display-name "New Factory" \
  --category new_domain \
  --domain-layer-name "New Domain Hermes" \
  --client-layer-name "New Tenant Hermes" \
  --customer-layer-name "New Subject Hermes"
```

The v13 starter is ontology-aware: it seeds a draft
`hermes/domain/ontology/` package deterministically from the `ontology:`
section of the pre-run answers (`--answers <file>`, defaulting to
`<target>/instantiation-answers.yaml`, then the generated example),
declares `domain_ontology` in `hermes/domain/content-manifest.yaml`, and
records the ontology-aware starter version in
`hermes/domain/ontology/STARTER.yaml`. Model-assisted extraction enters
only through `--ingest-candidates <batch.yaml>` — approved registered
sources plus an extraction-run identity, appending to the candidate
register without ever touching the active package or an existing
candidate's disposition. Reruns never overwrite domain-owned ontology
content: differences surface in the rerun report's Conflicts table, and
missing semantic inputs in its Unresolved Semantic Inputs table. Validate
a generated tree with `python3 scripts/validate-domain-ontology.py
<target>` and exercise the pipeline with
`python3 scripts/test-domain-starter-ontology.py`.

## 2. Required Repo Shape

Every new domain factory repo should start with this shape:

```text
<Domain>Factory/
  README.md
  Makefile
  stack.yaml

  docs/
    boundary.md
    domain-overview.md
    customer-hermes-model.md
    memory-gateway.md
    client-layer.md
    client-installation-discovery.md
    workflow-gates.md
    omnigent-constitution.md
    pre-run-questionnaire.md
    setup-runbook.md
    implementation-runbook.md
    implementation-guide.md
    credentialing.md
    hermes-agent-mixes.md
    avatar-first-ui.md

  models/
    action-classes.yaml
    risk-levels.yaml
    command-classes.yaml
    customer-kinds.yaml
    client-kinds.yaml
    evidence-types.yaml

  profiles/
    README.md

  ui/
    README.md
    avatar-first.yaml

  workflows/
    README.md
    example-readonly.yaml
    example-privileged.yaml

  hermes/
    domain/
      overlay.yaml
      agent-mixes.yaml
      policies/
      review-councils/
      memory-boundaries.yaml
      escalation-rules.yaml

    client/
      template.yaml
      offering-catalog.template.yaml
      agent-teams.template.yaml
      skills.template.yaml
      user-interactions.template.yaml
      installation-discovery.template.yaml
      agent-mixes.template.yaml
      memory-boundaries.yaml
      policy-overrides.yaml
      integration-boundaries.yaml

    customer/
      template.yaml
      agent-mixes.template.yaml
      memory-boundaries.yaml
      consent-model.yaml

  omnigent/
    domain-overlay.yaml
    worker-capabilities.yaml
    command-policy.yaml
    tool-routing.yaml
    expert-routing/
    validation-checks/
    output-templates/

  adapters/
    README.md

  memory-gateway/
    README.md
    provider-placeholders.yaml

  credentials/
    README.md
    requirements.yaml
    broker-contract.yaml
    bindings.template.yaml
    grants.template.yaml
    audit.yaml
    policies/
      approval-policy.yaml
      rotation-policy.yaml
      revocation-policy.yaml

  tenants/
    README.md
    examples/

  schemas/
    README.md
    stack.schema.yaml
    workflow.schema.yaml
    credential-requirements.schema.yaml
    agent-mixes.schema.yaml
    avatar-first-ui.schema.yaml
    instantiation-questionnaire.schema.yaml

  examples/
    README.md
    instantiation-answers.example.yaml
    golden-path/
      README.md

  scripts/
    validate-domain-factory.py
```

Every directory shown in the starter shape should contain at least one tracked
placeholder file, usually `README.md`, when the generator does not yet have
domain-specific content for that directory. Git does not track empty
directories, so placeholder files preserve the expected scaffold in the first
commit.

Domains may add clearer aliases when useful, but the logical mapping to domain,
client, and Subject Hermes must remain explicit in `stack.yaml`.

Subject Hermes implementations should preserve the canonical object vocabulary
from [Subject Hermes Memory Model](customer-hermes-memory-model.md): identity
profile, consent profile, preference profile, timeline, evidence graph, source
claim, current state snapshot, memory item, active workflow context, follow-up
obligation, and promotion candidate.

Examples:

```text
MedxFactory/hermes/customer/   -> Patient Hermes
MedxFactory/hermes/client/     -> Clinic, hospital, pharmacy, imaging center, or IDTF Hermes
MedxFactory/hermes/domain/     -> Medical Domain Hermes

OpsxFactory/hermes/customer/   -> Managed tenant or system Hermes
OpsxFactory/hermes/client/     -> IT Subject Hermes
OpsxFactory/hermes/domain/     -> Operations Domain Hermes
```

## 3. First Decisions

Before adding detailed workflows, decide:

1. Domain name and product name.
2. Domain Hermes layer name.
3. Tenant Hermes layer name.
4. Subject Hermes layer name.
5. Factory type and factory subtype.
6. Target domain and target domain subtype.
7. Client industry and client type.
8. Client or tenant kinds.
9. Customer subject kinds.
10. Deployment profiles.
11. Initial workflow catalog.
12. Credential requirement families.
13. Required approval gates.
14. Mixture of Agents review presets.
15. Audit and retention rules.

## 4. `stack.yaml`

Start every domain with a machine-readable stack descriptor.

```yaml
schema_version: 1
kind: xfactory_domain_stack

domain:
  id: example
  product_name: ExampleFactory
  display_name: Example Factory
  category: example_domain
  factory_type: example_work_type
  factory_subtype: example_service_area
  target_domain: example_target_domain
  target_domain_subtype: example_target_domain_subtype
  default_client_industry: example_client_industry
  default_client_type: example_client_type
  default_customer_subject_type: example_customer_subject

models:
  action_classes: models/action-classes.yaml
  risk_levels: models/risk-levels.yaml
  command_classes: models/command-classes.yaml
  evidence_types: models/evidence-types.yaml

xfactory:
  contract_repo: github.com/opensoft/openxFactory
  contract_name: openxFactory
  contract_ref_type: commit
  contract_ref: "0000000000000000000000000000000000000000"
  contract_schema_version: 1
  contract_declared_at: null
  contract_source: starter_placeholder

memory_gateway:
  canonical_contract: openxFactory/contracts/memory-gateway
  conformance_tier: M0
  placeholder: true
  customer_memory_gateway:
    customer_layer_name: Example Subject Hermes
    customer_subject_kinds: []
    required_operations:
      - xfactory.memory.context_packet
      - xfactory.memory.query
    direct_provider_policy:
      worker_credentials_allowed: false
      diagnostics_only: true
      diagnostic_namespace: shadow/non-production
  omnigent_expert_memory_gateway:
    consumer_layer: domain_omnigent
    expert_profiles: []
    allowed_knowledge_scopes: []
    source_authority_minimum: source_backed
    audit_required: true
  providers: []
  bindings: []
  break_glass_workflows: []

hermes:
  domain_layer_name: Example Domain Hermes
  domain_overlay: hermes/domain
  client_layer_name: Example Tenant Hermes
  client_overlay: hermes/client
  customer_layer_name: Example Subject Hermes
  customer_overlay: hermes/customer

omnigent:
  domain_overlay: omnigent
  orchestrator_profile: example

credentials:
  requirements: credentials/requirements.yaml
  broker_contract: credentials/broker-contract.yaml
  binding_template: credentials/bindings.template.yaml
  grant_template: credentials/grants.template.yaml
  audit_policy: credentials/audit.yaml

tenancy:
  client_kinds:
    - starter_client
  customer_kinds:
    - starter_customer
  isolation:
    memory: per_client
    records: per_client
    secrets: per_client
    customer_context: per_customer
```

`memory_gateway.placeholder: true` means the starter has not selected a memory
or expert knowledge provider yet. A domain-ready stack should replace the empty
`providers` and `bindings` lists with concrete provider profiles, gateway-only
grant scopes, source-authority policy, and any declared break-glass workflows.

## 4.5. Hermes Mixture Of Agents Module

Every domain factory should include a small Mixture of Agents module from day
one. The module does not make the domain more autonomous by itself. It defines
where Hermes may use independent reference-agent reasoning before a named
Hermes role, review council, human approver, or enforcement system decides.

Starter files:

```text
docs/hermes-agent-mixes.md
hermes/domain/agent-mixes.yaml
hermes/client/agent-mixes.template.yaml
hermes/customer/agent-mixes.template.yaml
schemas/agent-mixes.schema.yaml
```

Default rules:

- reference agents are advisory only
- reference agents do not receive tools
- reference agents do not receive runtime credential grants
- reference agents receive only approved context packets
- acting Hermes roles may request tools only through xFactory gates
- mix output is recommendation evidence, not approval
- dissent must be preserved for high-risk work

Council modes:

| Mode | Flow | Owner |
| --- | --- | --- |
| `panel_synthesis` | independent opinions -> acting Hermes synthesis | native Hermes MoA-compatible config |
| `scored_vote` | independent opinions -> explicit vote or score -> acting Hermes synthesis | xFactory council orchestration |
| `deliberative_council` | independent opinions -> disagreement summary -> rebuttal -> revised opinions -> consensus or dissent record -> acting Hermes recommendation | xFactory council orchestration |

Starter profiles:

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
```

See [Hermes Mixture Of Agents For xFactory](hermes-mixture-of-agents-for-xfactory.md)
for the canonical design guidance.

## 5. Credentialing Module

Every domain factory should include a credentialing module from day one.

The module owns:

- domain credential requirement declarations
- client or tenant binding templates
- runtime grant templates
- credential approval policy
- rotation policy
- revocation policy
- audit requirements

It does not own:

- passwords
- API keys
- OAuth refresh tokens
- private keys
- service principal secrets
- patient or customer records
- raw tenant secrets

## 6. Credentialing Folder Shape

```text
credentials/
  README.md
  requirements.yaml
  broker-contract.yaml
  bindings.template.yaml
  grants.template.yaml
  audit.yaml
  policies/
    approval-policy.yaml
    rotation-policy.yaml
    revocation-policy.yaml
```

The starter should include a broker contract placeholder because every
credential-aware domain eventually needs to describe how Hermes approval turns
client bindings into short-lived runtime grants.

## 7. `credentials/README.md`

```markdown
# <Domain>Factory Credentials

This folder declares credential requirements for <Domain>Factory.

It contains requirements, binding templates, runtime grant templates, approval
policy, rotation policy, revocation policy, and audit policy.

This folder must not contain raw secrets.

Raw secrets must live in approved secret providers such as Azure Key Vault,
AWS Secrets Manager, GCP Secret Manager, 1Password, Bitwarden, customer-owned
vaults, Opensoft-hosted vaults, OAuth delegated consent stores, or workload
identity providers.
```

## 8. `credentials/requirements.yaml`

```yaml
schema_version: 1
kind: xfactory_credential_requirements

domain:
  id: example
  product_name: ExampleFactory

requirements:
  - id: example_system_read
    purpose: read approved customer context from an external system
    access_mode: delegated_api
    allowed_workflows:
      - example_workflow
    customer_scope: customer
    minimum_scopes:
      - read
    requires_domain_approval: true
    requires_customer_consent: false
    requires_human_approval: false
    max_grant_minutes: 30
    audit_required: true
```

Guidance:

- Use stable requirement IDs.
- Prefer read-only requirements by default.
- Split read, write, admin, publish, send, and delete access.
- Scope requirements to workflows.
- Keep grant windows short.
- Require audit for all credential use.
- Require human approval for privileged or externally visible actions.

## 8.5. `credentials/broker-contract.yaml`

```yaml
schema_version: 1
kind: xfactory_credential_broker_contract

broker:
  id: example-credential-broker
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
```

## 9. `credentials/bindings.template.yaml`

```yaml
schema_version: 1
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
    consumer:
      instantiation_stub: true
```

Guidance:

- Bindings belong to client or tenant deployments, not the domain repo.
- Domain repos provide templates only.
- Use secret references, never raw values.
- `consumer:` declares WHO holds a binding and WHAT IDENTITY that system
  authenticates to the secret store with (`holder_ref` + `fetch_identity`). The
  scaffolded file is a stub written before any install exists, so it declares
  the const-true `instantiation_stub` token and nothing else; an instantiator
  REPLACES the token with the two identifiers when the consuming system exists,
  rather than keeping it beside live values; where the provider issues that
  identity out of a named directory, account or tenant, the instantiator also
  declares `identity_namespace`, which is optional and is what keeps two
  tenants' identically-named principals from reading as one authority. The exemption is the TOKEN and
  never the `*.template.yaml` filename — a filename is author-chosen and
  invisible in the bytes a pinned consumer validates — and a placeholder is not
  an alternative: it fails the identifier grammar, and a grammar-passing
  sentinel would read as an authority declaration while naming nothing.
- Prefer customer-owned vaults when customers require credential custody.
- Use Opensoft-hosted vaults when Opensoft operates the managed service.

## 10. `credentials/grants.template.yaml`

```yaml
schema_version: 1
kind: xfactory_runtime_capability_grant_template

runtime_capability_grant:
  id: <grant-id>
  job_id: <job-id>
  client_id: <client-id>
  domain: example
  requirement_id: example_system_read
  issued_by: hermes_credential_broker
  approved_by: domain_hermes
  customer_ref: <customer-ref>
  allowed_workflows:
    - example_workflow
  allowed_actions:
    - read_customer_context
  expires_at: <timestamp>
  audit_ref: <audit-ref>
```

Guidance:

- Workers should only receive runtime grants.
- Grants should be job-specific.
- Grants should be customer-specific when possible.
- Grants should expire quickly.
- Grants should be revocable.
- Grants should reference an audit record.

## 11. `credentials/audit.yaml`

```yaml
schema_version: 1
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
```

## 12. Credential Policies

`credentials/policies/approval-policy.yaml`:

```yaml
schema_version: 1
kind: xfactory_credential_approval_policy

approval_policy:
  default_requires_domain_hermes: true
  default_requires_human_approval: false

  always_require_human_approval:
    - admin_access
    - delete_access
    - external_send
    - money_movement
    - production_deployment
    - care_affecting_action

  deny_by_default_when:
    - workflow_not_approved
    - tenant_binding_missing
    - requested_scope_exceeds_requirement
    - customer_consent_missing
    - grant_duration_exceeds_policy
```

`credentials/policies/rotation-policy.yaml`:

```yaml
schema_version: 1
kind: xfactory_credential_rotation_policy

rotation_policy:
  default_owner: client
  supported_owners:
    - client
    - opensoft
    - provider

  require_rotation_on:
    - client_offboarding
    - suspected_exposure
    - provider_policy_change
    - privileged_scope_change
```

`credentials/policies/revocation-policy.yaml`:

```yaml
schema_version: 1
kind: xfactory_credential_revocation_policy

revocation_policy:
  revoke_runtime_grant_when:
    - job_completes
    - grant_expires
    - client_revokes_authorization
    - customer_consent_withdrawn
    - worker_session_terminates
    - workflow_leaves_approved_scope
    - suspicious_behavior_detected
    - human_approver_cancels_job
```

## 13. MedxFactory Credentialing Starter

MedxFactory should map the customer layer to Patient Hermes.

Credential families should start with:

```yaml
requirements:
  - id: ehr_patient_read
    purpose: read patient chart context for approved workflow
    access_mode: delegated_api
    allowed_workflows:
      - intake_summary
      - diagnostic_review_packet
      - patient_follow_up_packet
    customer_scope: patient
    requires_patient_consent: true
    requires_domain_approval: true
    requires_human_approval: false
    max_grant_minutes: 30
    audit_required: true

  - id: patient_messaging_send
    purpose: send approved patient communication
    access_mode: delegated_api
    allowed_workflows:
      - patient_follow_up
      - appointment_instruction
    customer_scope: patient
    requires_patient_consent: true
    requires_domain_approval: true
    requires_human_approval: true
    max_grant_minutes: 15
    audit_required: true

  - id: scheduling_write
    purpose: create or update approved scheduling records
    access_mode: delegated_api
    allowed_workflows:
      - appointment_scheduling
      - referral_coordination
    customer_scope: patient
    requires_patient_consent: true
    requires_domain_approval: true
    requires_human_approval: true
    max_grant_minutes: 15
    audit_required: true
```

MedxFactory-specific rules:

1. Patient Hermes does not own clinic-wide credentials.
2. Patient Hermes may request patient-specific access.
3. Clinic or Tenant Hermes owns local integration bindings.
4. Medical Domain Hermes approves medical policy and risk.
5. Patient data access requires consent and audit.
6. Care-affecting, diagnosis-related, or external patient communication
   workflows require domain approval and usually human review.
7. Patient-derived lessons must not update domain memory without review,
   de-identification when required, and approval.

## 14. OpsxFactory Credentialing Starter

OpsxFactory should treat credentials as privileged administrative capability.

Credential families should start with:

```yaml
requirements:
  - id: entra_directory_admin
    purpose: Entra ID administration
    access_mode: delegated_oauth
    allowed_workflows:
      - user_lifecycle
      - security_group_management
      - conditional_access_review
    requires_domain_approval: true
    requires_human_approval: true
    max_grant_minutes: 45
    audit_required: true

  - id: exchange_admin
    purpose: Exchange Online administration
    access_mode: delegated_oauth
    allowed_workflows:
      - mailbox_migration
      - mailbox_permission_review
      - transport_rule_review
    requires_domain_approval: true
    requires_human_approval: true
    max_grant_minutes: 60
    audit_required: true

  - id: dns_admin
    purpose: DNS administration
    access_mode: delegated_api
    allowed_workflows:
      - dns_record_update
      - domain_cutover
    requires_domain_approval: true
    requires_human_approval: true
    max_grant_minutes: 30
    audit_required: true
```

OpsxFactory-specific rules:

1. Prefer delegated OAuth over stored passwords.
2. Prefer workload identity over long-lived client secrets.
3. Prefer just-in-time elevation over standing administrator access.
4. Never give workers standing global admin credentials.
5. Split read, write, admin, and destructive actions.
6. Require audit for all privileged access.
7. Revoke grants when the job completes or leaves scope.

## 15. Starter Checklist

```text
[ ] Create stack.yaml.
[ ] Create Makefile with local validation target.
[ ] Name Domain Hermes.
[ ] Name Tenant Hermes.
[ ] Name Subject Hermes.
[ ] Define client or tenant kinds.
[ ] Define customer subject kinds.
[ ] Add deployment profiles.
[ ] Add initial workflow catalog.
[ ] Complete pre-run questionnaire for this domain interpretation.
[ ] Mark which answers are declared, inferred, simulated, confirmed, or approved.
[ ] Normalize any legacy subject-layer vocabulary into domain, client, and Subject Hermes.
[ ] Add setup runbook for implementation and instantiation.
[ ] Add domain overview, Subject Hermes model, workflow gates, and Omnigent constitution docs.
[ ] Add hermes/domain overlay.
[ ] Add hermes/domain agent mix profiles.
[ ] Add hermes/client overlay.
[ ] Add hermes/client product/service offer scaffold.
[ ] Add hermes/client installation discovery and workflow migration scaffold.
[ ] Define how observed document/email workflows are reviewed before becoming target workflows.
[ ] Add hermes/client agent mix template.
[ ] Add hermes/customer overlay or domain-specific alias.
[ ] Add hermes/customer agent mix template.
[ ] Add omnigent/domain-overlay.yaml.
[ ] Add credentials/requirements.yaml.
[ ] Add credentials/bindings.template.yaml.
[ ] Add credentials/grants.template.yaml.
[ ] Add credential approval, rotation, revocation, and audit policies.
[ ] Add schema descriptors for stack, workflow, and credential requirements.
[ ] Add schema descriptor for Hermes Mixture of Agents profiles.
[ ] Add schema descriptor for pre-run instantiation answers.
[ ] Add examples/README.md and examples/golden-path/README.md.
[ ] Add examples/instantiation-answers.example.yaml.
[ ] Add README placeholders to generated directories that would otherwise be empty.
[ ] Confirm no raw secrets exist in the repo.
[ ] Link back to openxFactory docs.
[ ] Run local validation.
[ ] Produce a starter rerun report.
```

## 16. Starter Rerun Report

Every starter run should produce a report. The report may be printed in the
agent response, written to `docs/starter-rerun-report.md`, or both.

Template:

~~~markdown
# Starter Rerun Report

Domain: <Domain>Factory
Date: <date>
Starter: openxFactory/domain-factory-starter-pack

## Summary

- Created:
- Updated:
- Skipped:
- Conflicts:
- Validation:

## Created Files

| File | Reason |
|---|---|

## Updated Files

| File | Change |
|---|---|

## Skipped Files

| File | Reason |
|---|---|

## Conflicts

| File | Conflict | Recommended action |
|---|---|---|

## Validation

```text
<validation output>
```

## Next Work

1. Fill domain-specific workflows.
2. Fill provider-specific credential requirements.
3. Fill adapter contracts.
4. Fill client instantiation examples.
5. Replace placeholders with domain-owned content.
~~~

## 17. What The Starter Should Not Try To Solve

The starter pack should not attempt to generate:

- real secret values
- real client vault names
- live OAuth consent
- live customer or patient records
- production app registrations
- provider-specific legal or compliance determinations
- final clinical, financial, legal, or operational authority
- runtime credentials or refresh tokens
- customer-specific staff approval rosters
- production maintenance windows

Those belong to domain implementation, client instantiation, or live runtime
approval.

## 18. Improvements From Domain Repo Review

The starter pack should keep learning from real domain repos without becoming
domain-specific.

Current review lessons:

- `AdxFactory` and `LedgerxFactory` show that every domain needs narrative
  orientation docs, not only machine manifests. The starter therefore creates
  domain overview, Subject Hermes model, workflow gates, and Omnigent
  constitution docs.
- `MedxFactory` shows that schemas and local validation must arrive early. The
  starter therefore creates a Makefile, schema descriptors, and a validation
  script from day one.
- `codexFactory` shows that examples make the workflow contract concrete.
  The starter therefore creates an `examples/` area and a golden-path folder.
- `OpsxFactory` shows that credential-aware domains need a broker contract,
  runtime grant templates, policy files, and idempotent rerun reports before
  provider-specific implementation begins.
- The cross-domain comparison shows that every implementation should answer a
  pre-run questionnaire before a domain, profile, client, tenant, or
  customer-subject instantiation proceeds.
- The simulation reports show that inferred answers must be labeled. Starter
  setup should never treat repo-inferred layer names, credential requirements,
  or approval rules as client-approved instantiation decisions.

The starter runner should remain conservative: create missing generic
surfaces, preserve existing domain-owned files, and report the next specific
work rather than guessing domain truth.
