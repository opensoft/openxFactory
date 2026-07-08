# Domain Instantiation Setup Runbook

Status: draft
Kind: runbook
Repository context: openxFactory
Purpose: turn pre-run questionnaire answers into a domain factory implementation
or a client/tenant/customer-subject instantiation.

## 1. Inputs

Required inputs:

- completed pre-run questionnaire
- target domain repo
- target profile or client kind
- target customer-subject kind
- first read-only workflow
- first privileged or high-risk workflow
- credential requirement families
- human approval and escalation contacts as references, not secrets
- validation command

The completed questionnaire may come from the hosted website intake, TUI
self-install flow, or downloadable installer described in
[xFactory Intake And Installer Plan](intake-and-installer-plan.md).
For self-hosted deployments, runtime wiring follows
[Self-Hosted Runtime Binding Plan](self-hosted-runtime-binding-plan.md).

Forbidden inputs:

- raw credentials
- OAuth refresh tokens
- private keys
- production connection strings
- patient records, financial records, campaign data, source code secrets, or
  tenant-specific private data

## 2. Setup Flow

1. Mark answer quality as declared, inferred, simulated, confirmed, or approved.
2. Confirm the domain interpretation.
3. Normalize any legacy `subject_layer` vocabulary into domain Hermes, client
   Hermes, and customer Hermes.
4. Confirm the three Hermes layer names and authority boundaries.
5. Confirm client, tenant, and customer-subject isolation.
6. Declare any authorized installation discovery sources, including document
   management, email, ticketing, CRM, calendar, or collaboration records.
7. Mark discovered client workflows as current-state evidence, not target
   operational policy.
8. Convert discovered resources into workflow definition packets with states,
   transitions, roles, artifacts, systems, gates, completion criteria, and source
   traces.
9. Validate current-state workflow packets with the workflow owner or affected
   users before treating them as confirmed current state.
10. Create gap records and migration plans for current practices that differ from
   domain or client best practice.
11. Get workflow-change consent before replacing, constraining, automating, or
    retiring an existing user workflow.
12. Fill `stack.yaml`.
13. Fill profile files.
14. Fill model files.
15. Fill Hermes overlays.
16. Fill credential requirements and broker contract.
17. Fill Omnigent worker capabilities, command policy, and tool routing.
18. Add workflow specs.
19. Add schemas.
20. Add examples.
21. Run validation.
22. Produce the setup decision record.
23. Produce or request the runtime binding manifest.
24. Mark what remains domain implementation versus client instantiation versus
    runtime approval.

Runtime binding covers the customer-specific pieces that cannot be safely
collected during pre-run: deployment target, Hermes and Omnigent runtime
references, secret provider references, adapter endpoints, approval references,
validation results, and dry-run evidence.

## 2.5 Setup Modes

Use these modes to avoid treating starter output as operational truth:

| Mode | Meaning | Allowed Work |
| --- | --- | --- |
| `concept` | Domain language exists but implementation contracts are thin. | Add questionnaire answers, docs, missing scaffold, and inferred gaps. |
| `domain_implementation` | Domain repo is being made implementable. | Add workflows, schemas, overlays, credential requirements, examples, and validation. |
| `profile_setup` | A reusable deployment profile is being defined. | Add profile constraints, enabled workflows, client/customer kinds, and policy overrides. |
| `client_instantiation` | A real client or tenant is being configured. | Add non-secret client references, approver references, bindings, and isolation choices. |
| `customer_subject_instantiation` | A real patient, campaign, ledger, repo, or system is being configured. | Add runtime-only subject references through approved systems, not repo secrets. |

The starter may operate in `concept`, `domain_implementation`, and
`profile_setup` modes. Client and customer-subject instantiation require
authorized runtime decisions.

## 2.6 Stop Rules

Stop before applying changes when:

- raw secrets, private records, patient data, financial records, campaign data,
  source code secrets, or production connection strings are provided
- the three Hermes layer mapping is unresolved
- a privileged workflow lacks credential requirements
- live client approvers or vault references are needed but not available
- a domain-specific law, professional authority, or customer-facing risk is
  unresolved
- the requested change would turn an inferred answer into an approved answer
  without stakeholder confirmation
- document or email mining would promote observed current practice into target
  workflow policy without gap review and Hermes approval
- a current-state workflow packet has not been validated by the workflow owner
  or affected users
- a high-risk bad-practice finding has no containment, migration, or cutover
  plan
- a workflow change would affect user work without the consent, notice,
  acknowledgement, or representative approval required by client policy

## 3. Domain Interpretation Examples

### 3.1 MedxFactory

Recommended interpretation:

- Domain Hermes: Medical Domain Hermes
- Client Hermes: Clinic, practice, hospital, pharmacy, imaging center, or IDTF
  Hermes
- Customer Hermes: Patient Hermes
- Customer-subject: patient across the life of the patient, not only one case
- Example profiles: clinic, group practice, hospital, pharmacy, imaging center,
  IDTF
- Example workflows: intake, referral management, diagnostic review, prior
  authorization, patient follow-up, pharmacy reconciliation
- Credential families: EHR read, scheduling write, patient messaging send,
  imaging result read, pharmacy reconciliation
- Highest-risk boundary: care-affecting action, diagnosis-related output,
  patient-facing communication, patient privacy

Setup emphasis:

- Patient Hermes owns patient-specific context, consent, timeline, and current
  state.
- Clinic or care-organization Hermes owns local operating policy, staff roles,
  integration bindings, and escalation contacts.
- Medical Domain Hermes owns medical policy, reusable review standards, domain
  memory promotion, and clinical risk gates.
- Omnigent may prepare evidence and recommendations, but clinical authority
  stays with the accountable medical layer and human review where required.

### 3.2 OpsxFactory

Recommended interpretation:

- Domain Hermes: Operations Domain Hermes
- Client Hermes: IT Customer Hermes
- Customer Hermes: Managed System Hermes
- Customer-subject: tenant, subscription, service, DNS zone, backup vault,
  endpoint fleet, or production workload
- Example profiles: managed IT customer, DevOps customer, internal IT team
- Example workflows: GitHub organization review, DNS record update, mailbox
  migration, user lifecycle, deployment, backup restore
- Credential families: Microsoft 365 admin, Exchange admin, DNS admin, GitHub
  org admin, deployment operator, backup operator
- Highest-risk boundary: privileged admin action, outage, destructive change,
  production impact

Setup emphasis:

- Managed System Hermes owns the operational subject and current state.
- IT Customer Hermes owns tenant policy, maintenance windows, staff approvers,
  integration inventory, and credential bindings.
- Operations Domain Hermes owns reusable operations policy, risk classes,
  escalation rules, and command standards.
- Workers receive runtime grants only, never standing global administrator
  credentials.

### 3.3 codexFactory

Recommended interpretation:

- Domain Hermes: Software Engineering Domain Hermes
- Client Hermes: Software Company Hermes
- Customer Hermes: Project, repo, product, feature, or release Hermes
- Customer-subject: project, repository, feature initiative, bug, PR, release,
  incident, dependency, or technical debt item
- Example profile: software team
- Example workflows: approved intent intake, feature decomposition, Spec Kit
  execution, deterministic validation, branch review, PR admission, merge
  readiness
- Credential families: repo read, branch write, PR write, package publish,
  deployment, cloud read, cloud deploy
- Highest-risk boundary: merge, deploy, package publish, production impact,
  data exposure

Setup emphasis:

- Project Hermes owns project/repo/feature context and traceability.
- Software Company Hermes owns engineering policy, repo ownership, release
  policy, CI/CD authority, and staff approvals.
- Software Engineering Domain Hermes owns engineering standards, review gates,
  reusable validation policy, and worker boundaries.
- Omnigent may implement, validate, and draft PR artifacts under admission and
  merge-readiness gates.

### 3.4 AdxFactory

Recommended interpretation:

- Domain Hermes: Marketing Domain Hermes
- Client Hermes: Agency, brand, growth team, or marketing operator Hermes
- Customer Hermes: Buyer, prospect, audience, account, or campaign Hermes
- Customer-subject: campaign, audience, offer, channel, brand, account,
  product, subscription, or purchase decision
- Example profiles: agency, brand program, growth team, in-house marketing team
- Example workflows: campaign intake, audience segmentation, creative review,
  campaign launch, budget adjustment, attribution review
- Credential families: analytics read, ad account read, ad account write,
  creative asset access, CRM read, email send, social publish
- Highest-risk boundary: brand risk, regulated claims, external send, paid
  spend, privacy, targeting, attribution

Setup emphasis:

- Customer Hermes should clarify whether the subject is a buyer, audience,
  account, or campaign because each has different memory and consent semantics.
- Client Hermes owns brand policy, campaign approvals, budget boundaries,
  channel integrations, and local review rules.
- Marketing Domain Hermes owns reusable marketing standards, claim review,
  segmentation policy, experimentation rules, and campaign gates.
- Omnigent can draft, analyze, segment, and recommend, but publishing and spend
  changes require explicit gates.

### 3.5 LedgerxFactory

Recommended interpretation:

- Domain Hermes: Ledger Domain Hermes
- Client Hermes: Accounting firm, bookkeeping firm, controller organization, or
  finance team Hermes
- Customer Hermes: Ledger, company, client, tax matter, engagement, or report
  Hermes
- Customer-subject: company, ledger, transaction set, account, filing, report,
  tax matter, audit issue, obligation, or financial decision
- Example profiles: accounting firm, bookkeeping firm, finance team, controller
  organization
- Example workflows: client intake, bank feed review, reconciliation,
  month-end close, tax packet preparation, filing review, audit support
- Credential families: accounting system read, bank feed read, ledger write,
  document store read, filing portal access, payment approval
- Highest-risk boundary: money movement, filing, compliance representation,
  audit evidence, tax advice, financial reporting

Setup emphasis:

- Customer Hermes must disambiguate whether the subject is the company, ledger,
  tax matter, engagement, or filing.
- Client Hermes owns firm policy, staff roles, client authorizations,
  integration bindings, and professional review.
- Ledger Domain Hermes owns accounting standards, evidence requirements,
  close/reconciliation gates, and compliance-sensitive workflow policy.
- Omnigent may prepare reconciliations, packets, drafts, and exceptions, but
  filings, money movement, and professional representations require explicit
  authority.

## 4. Pre-Run Output Checklist

Before implementation or client instantiation continues, confirm:

- [ ] Three Hermes layers are named.
- [ ] Answer quality is marked.
- [ ] Legacy subject-layer mappings are normalized when present.
- [ ] Layer ownership and stop authority are documented.
- [ ] Client kinds and customer-subject kinds are listed.
- [ ] First read-only workflow is selected.
- [ ] First privileged or high-risk workflow is selected.
- [ ] Credential requirement families are listed.
- [ ] Credential broker expectations are documented.
- [ ] Human approval requirements are documented.
- [ ] Runtime grant duration limits are set.
- [ ] Source authority and evidence rules are documented.
- [ ] At least one golden-path example is planned.
- [ ] At least one blocked-path example is planned.
- [ ] Local validation command is known.
- [ ] Implementation gaps are listed.
- [ ] No raw secrets or private runtime records are present.

## 5. Implementation Agent Instruction

An implementation agent should:

1. Read the pre-run answers.
2. Refuse to proceed if raw secrets are provided.
3. Map domain-specific names back to the neutral xFactory layer names.
4. Mark inferred answers as inferred.
5. Refuse to promote inferred answers to approved answers without confirmation.
6. Update starter-owned placeholder files only when safe.
7. Preserve existing domain-owned files.
8. Create missing examples and schemas.
9. Run local validation.
10. Emit a setup report naming what remains unresolved.

The agent should not infer customer consent, client authorization, live
credential access, provider scopes, or professional authority from repo
structure alone.
