# Domain Instantiation Pre-Run Questionnaire

Status: draft
Kind: template
Repository context: openxFactory
Purpose: define the questions that must be answered before a domain factory is
implemented for a new domain, profile, client, tenant, or customer-subject.

## 1. When To Use This

Use this questionnaire before:

- creating a new domain factory repo
- expanding a concept domain into an implementable stack
- creating a new client or tenant inside an existing domain factory
- running a workflow against a real customer, patient, campaign, ledger,
  project, managed system, or equivalent subject

The questionnaire is intentionally pre-run. It does not collect live
credentials, private records, patient data, financial records, campaign data,
source code secrets, or tenant secrets. It collects decisions and references
needed to configure the stack safely.

This questionnaire can be collected through a hosted website form, a terminal
UI self-install flow, or a downloadable installer. See
[xFactory Intake And Installer Plan](intake-and-installer-plan.md) for the
shared intake surfaces, generated artifacts, and readiness levels.
Template selection should follow
[xFactory Taxonomy Model](factory-taxonomy-model.md), which separates factory
type, factory subtype, target domain, client industry, and customer-subject
type.

## 2. Why This Exists

The existing xFactory domains use the same general pattern but interpret the
layers differently:

| Domain | Subject Hermes | Tenant Hermes | Domain Hermes | Main Subject | Main Risk |
| --- | --- | --- | --- | --- | --- |
| `MedxFactory` | Patient Hermes | Clinic, practice, hospital, pharmacy, imaging center, or IDTF Hermes | Medical Domain Hermes | Patient and care context | Care-affecting action, patient privacy, clinical authority |
| `OpsxFactory` | Managed System Hermes | IT Subject Hermes | Operations Domain Hermes | Tenant, system, service, subscription, DNS zone, backup vault | Privileged admin action, outage, destructive change |
| `codexFactory` | Project, repo, product, or feature Hermes | Software Company Hermes | Software Engineering Domain Hermes | Feature, repo, PR, release, incident | Merge, deploy, data exposure, production impact |
| `AdxFactory` | Buyer, audience, account, or campaign Hermes | Agency, brand, growth team, or marketing operator Hermes | Marketing Domain Hermes | Campaign, audience, offer, channel, account | Brand risk, external send, paid spend, privacy, attribution |
| `LedgerxFactory` | Ledger, company, client, tax matter, or engagement Hermes | Firm, controller org, bookkeeping team, or finance team Hermes | Ledger Domain Hermes | Ledger, filing, report, transaction, obligation | Money movement, filing accuracy, audit, compliance |

The implementation should not continue until these interpretations are made
explicit for the target stack.

## 3. Required Answers

### 3.0 Answer Quality

- Is this answer set for a domain, profile, client, tenant, or
  customer-subject?
- Is the answer set `declared`, `inferred`, `simulated`, `confirmed`, or
  `approved_for_instantiation`?
- Which repo files or stakeholder decisions support the answers?
- Which answers are still assumptions?
- Which answers must be confirmed before implementation?
- Which answers must be confirmed before live client or customer-subject
  instantiation?

### 3.1 Domain Identity

- What is the domain factory repo name?
- What is the public product name?
- What is the domain category?
- What factory type describes the work being performed?
- What factory subtype describes the specialized service area?
- What target domain is the work about?
- What target domain subtype is in scope?
- What industry is the client or operator in?
- What client type is operating or buying the stack?
- What customer-subject type sits at the top of the stack?
- What work does this domain own?
- What work does this domain explicitly not own?
- Which existing domain is the closest analogy?
- Which existing domain is the worst analogy and why?
- Is this a new domain, a domain profile, a client deployment, or a
  customer-subject deployment?

### 3.2 Three Hermes Layers

- What is the domain Hermes called?
- What reusable domain policy, standards, review councils, and memory does it
  own?
- What is the Tenant Hermes called?
- What organization, operating policy, staff roster, integrations, and local
  approval rules does it own?
- What is the Subject Hermes called?
- What customer-subject, timeline, current state, consent, and subject-specific
  memory does it own?
- Can one physical Hermes install host multiple logical layers?
- Which layer may initiate work without a new human request?
- Which layer can stop work?
- Which layer can approve read-only work?
- Which layer can approve write, publish, send, deploy, care-affecting,
  money-moving, or privileged work?
- Does the current repo use an older `subject_layer` or two-Hermes vocabulary?
- If yes, what is the normalized mapping to domain Hermes, Tenant Hermes, and
  Subject Hermes?
- Which layer name is repo-declared, and which layer name is inferred?

### 3.2.5 Hermes Mixture Of Agents

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

### 3.3 Client Or Tenant Shape

- What client kinds exist?
- What customer-subject kinds exist?
- What profiles should the repo ship first?
- Is this Opensoft-hosted, client-hosted, or hybrid?
- Who operates the runtime?
- Who owns the vault or secret provider?
- Who owns production incident response?
- What must be isolated per client?
- What must be isolated per customer-subject?
- What can be shared across clients?
- What can be shared across customer-subjects?
- What identifiers are allowed in repo examples?
- What identifiers must only exist in runtime or tenant configuration?
- Which client document management, mailbox, ticketing, CRM, calendar, or
  collaboration sources may be used for installation discovery?
- Which sources are official policy, which are working documents, and which are
  merely historical evidence?
- Which known current practices should not be treated as target practice?
- Who approves migration from current practice to target practice?
- Which user groups are affected by each workflow change?
- Which workflow changes require direct user consent, manager approval,
  representative approval, customer consent, or only notice?
- What training, acknowledgement, or change notice is required before cutover?

### 3.4 Customer-Subject Model

- What is the thing at the top of the stack?
- Is it a person, organization, account, project, ledger, campaign, tenant,
  system, asset, matter, case, or something else?
- Does the customer-subject span multiple cases or workflow runs?
- What is the lifecycle or journey state model?
- What events update the customer-subject timeline?
- Which memories can be promoted to domain memory?
- Which memories must never be promoted?
- What de-identification, aggregation, or review is required before learning?

### 3.4.5 Ontology Intake

Machine-readable answers land in the `ontology:` section of the pre-run
answer file (`xfactory_instantiation_prerun_answers`); the ontology-aware
starter (v13+) seeds `hermes/domain/ontology/` deterministically from them
per the `add-domain-ontology-layer` generation pipeline. Placeholder values
in angle brackets are never seeded — each becomes an unresolved input in
the starter rerun report and the coverage-gap report, and the draft package
stays non-publishable until Domain Hermes review resolves it.

- Which subject kinds does this domain serve? (each seeds a draft
  specialization of `xf/core/subject`)
- Which focal item kinds? (`xf/core/focal_item`)
- Which primary workflows, activities, journey states, outcomes, and
  interventions? (each list seeds its kernel specialization)
- Which evidence types? (`xf/core/evidence`)
- Which external terminologies or code systems, with license class and
  permitted use? (registered by reference in the source inventory; content
  is never mirrored)
- Which governed internal sources feed the ontology?
- What are the domain boundaries and prohibited interpretations?
- Who is the accountable ontology steward, and which review council and
  required reviewers gate high-impact semantic change? (a worker or agent
  identity cannot publish)
- Which semantic assumptions remain unresolved?

### 3.5 Workflows And Gates

- What are the first three workflows?
- Which workflow is read-only?
- Which workflow is privileged, externally visible, destructive, regulated, or
  otherwise high risk?
- What are the required gates for each workflow?
- What evidence is required at each gate?
- What does pass, fail, pending, and not applicable mean?
- What blocks the workflow?
- What is the final handoff or enforcement system?
- What is the rollback, correction, or repair path?

### 3.6 Omnigent Layer

- What is the domain Omnigent overlay called?
- Which expert or worker classes are needed?
- What can workers read?
- What can workers write?
- What can workers recommend but not execute?
- What stop conditions must workers obey?
- What ambiguity must route back to Hermes?
- What outputs must workers produce for audit and validation?
- Which worker classes already exist in the repo?
- Which worker classes are inferred from workflows but not yet declared?

### 3.7 Credentials

- Which external systems will the domain touch?
- Which access requirements are read-only?
- Which are write, admin, publish, send, deploy, care-affecting, money-moving,
  or destructive?
- Which credential requirements need domain Hermes approval?
- Which need Tenant Hermes approval?
- Which need Subject Hermes consent or authorization?
- Which need human approval?
- What secret providers are allowed?
- Who owns rotation?
- What is the maximum runtime grant duration?
- What revokes a runtime grant?
- What audit fields are mandatory?
- Which requirements are repo-declared?
- Which requirements are inferred from workflows or docs?
- Which requirements are blocked until provider choice or client approval?

### 3.8 Source Authority And Evidence

- What source workspaces may be used?
- Which sources are allowed for domain knowledge?
- Which sources are allowed for client-specific knowledge?
- Which sources are allowed for customer-subject context?
- Which claims may rely on workspace synthesis?
- Which claims require ground-source verification?
- What citation or trace is required?
- Which outputs are advisory only?
- Which outputs can affect external state only after review?
- Which current-state claims may be inferred from documents or email?
- Which current-state claims require ground-source verification?
- Which bad-practice findings require containment before automation?
- What migration record is required before a discovered current workflow becomes
  a target workflow?
- What workflow definition packet is required before best-practice migration?
- What current-to-target delta must be shown to users before consent?
- What consent record is required before target workflow cutover?

### 3.9 Compliance And Human Authority

- What laws, regulations, contracts, professional standards, or internal policies
  are in scope?
- Which decisions are reserved for licensed professionals, accountable staff,
  client approvers, or external systems?
- What must be reviewed before customer-facing output?
- What must be reviewed before external execution?
- What is the incident, appeal, correction, or escalation path?

### 3.10 Examples And Validation

- What is the first golden-path example?
- What is the first blocked-path example?
- What is the first repair or exception example?
- What schemas are required before implementation?
- What local validation command must pass?
- What live checks are forbidden in local validation?
- What does tenant-ready mean for this domain?
- Which starter files are still placeholders?
- Which domain-owned files must be created before the next run?
- Which answers should become machine-readable YAML?

## 4. Pre-Run Decision Record

Every implementation should produce a decision record before writing real
tenant/client/customer configuration:

```yaml
schema_version: 1
kind: xfactory_instantiation_prerun_answers

answer_metadata:
  status: <declared|inferred|simulated|confirmed|approved_for_instantiation>
  scope: <domain|profile|client|tenant|customer_subject>
  generated_from:
    - <repo-file-or-decision-ref>
  assumptions:
    - <assumption>
  must_confirm_before_instantiation:
    - <decision>

domain:
  repo: <Domain>Factory
  category: <domain-category>
  closest_existing_domain: <MedxFactory|OpsxFactory|codexFactory|AdxFactory|LedgerxFactory>
  factory_type: <medical|law|accounting|marketing|operations|software|custom>
  factory_subtype: <subtype>
  target_domain: <domain-being-worked-on>
  target_domain_subtype: <narrower-domain-context>
  client_industry: <industry-of-buyer-or-operator>
  client_type: <client-type>
  customer_subject_type: <customer-subject-type>

hermes_layers:
  domain_hermes: <name>
  client_hermes: <name>
  customer_hermes: <name>

hermes_mixture:
  enabled: true
  default_decision_status: recommendation_only
  reference_agents_have_tools: false
  reference_agents_receive_runtime_grants: false
  required_profiles:
    - <mix-profile-id>
  repo_declared_profiles:
    - <mix-profile-id>
  inferred_profiles:
    - <mix-profile-id>
  profile_modes:
    <mix-profile-id>: <panel_synthesis|scored_vote|deliberative_council>
  context_rules:
    allowed_context:
      - <context-class>
    prohibited_context:
      - raw_credentials
      - unrestricted_private_records
      - tool_outputs_with_secret_values
    default_redaction_level: <redaction-level>
  acting_roles:
    <mix-profile-id>: <acting-role>
  scored_vote:
    <mix-profile-id>:
      vote_values:
        - approve
        - approve_with_conditions
        - reject
        - abstain
      scoring_criteria:
        - <criterion>
      approval_threshold: <threshold>
      tie_breaker: <escalation-rule>
  deliberative_council:
    <mix-profile-id>:
      rounds:
        - independent_positions
        - disagreement_summary
        - rebuttal
        - revised_positions
        - final_recommendation
      preserve_unresolved_dissent: true
      escalation_for_unresolved_dissent: <escalation-rule>
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
  uses_legacy_subject_layer: <true|false>
  legacy_subject_layer_name: <name-or-null>
  normalized_client_layer_name: <name>
  normalized_customer_layer_name: <name>

instantiation:
  level: <domain|profile|client|tenant|customer_subject>
  hosted_by: <opensoft|client|hybrid>
  client_kind: <kind>
  customer_subject_kind: <kind>

workflow_seed:
  readonly_workflow: <workflow-id>
  privileged_workflow: <workflow-id>
  highest_risk_level: <risk-level>

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
    - <file-or-area>
  domain_files_required:
    - <file-or-area>
  client_instantiation_required:
    - <decision-or-reference>
```

The answers should be stored as a non-secret artifact, usually under
`examples/instantiation-answers.example.yaml` for examples or under tenant
configuration for a real client.
