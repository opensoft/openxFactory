# Domain Pre-Run Simulation Report

Status: simulated pre-run review
Repository context: openxFactory
Date: 2026-06-30
Purpose: answer the pre-run questionnaire for the currently implemented
xFactory domain repos using only non-secret repo information.

## 1. Scope

This report simulates the pre-run questionnaire for:

- `AdxFactory`
- `LedgerxFactory`
- `MedxFactory`
- `codexFactory`
- `OpsxFactory`

The simulation is not a live instantiation. It does not create client records,
tenant bindings, patient records, campaign data, ledgers, source code secrets,
or runtime credential grants.

Structured simulated answer records are in
`examples/pre-run-simulations/`.

Each structured record now marks answer quality:

- `declared` means the answer is directly represented in the repo.
- `simulated` means the answer was generated from repo evidence but still needs
  stakeholder confirmation before real instantiation.
- `inferred` values may guide scaffolding, but they must not become approved
  client, tenant, or customer-subject decisions without confirmation.

## 2. Cross-Domain Findings

### Q: What pattern is common across all domains?

A: Each domain uses xFactory as the neutral rail, Hermes as the policy and
memory authority, and Omnigent as bounded domain execution. Every domain needs
three logical Hermes authorities even when older repos call one of them a
`subject_layer`.

### Q: What differs across domains?

A: The meaning of the customer-subject changes:

| Domain | Customer-subject |
| --- | --- |
| `AdxFactory` | campaign, audience, offer, channel, account, buyer segment |
| `LedgerxFactory` | company, ledger, engagement, tax matter, filing, report |
| `MedxFactory` | patient, case, decision candidate, care plan, diagnostic pathway |
| `codexFactory` | project, repo, feature, PR, release, incident |
| `OpsxFactory` | tenant, subscription, service, DNS zone, backup vault, endpoint fleet |

### Q: What is the biggest implementation risk found in simulation?

A: The older concept repos have strong domain language but do not yet carry the
new starter v3 implementation surfaces: explicit client/customer Hermes
overlays, credential modules, pre-run answer artifacts, and local validators.

### Q: Which repo is closest to the current starter v3 shape?

A: `OpsxFactory`. It now has explicit domain/client/customer Hermes names, a
credential module, workflow specs, starter validation, and pre-run artifacts.

## 3. AdxFactory Simulation

Structured record: `examples/pre-run-simulations/adx.yaml`

### Q: What does this domain own?

A: `AdxFactory` owns the marketing interpretation of the xFactory rail:
campaign planning, brand governance, creative review, launch readiness,
audience/privacy review, performance reverification, and bounded marketing
agent execution.

### Q: How do the three Hermes layers map?

A:

- Domain Hermes: Adx Domain Hermes
- Client Hermes: Brand Hermes or Marketing Operator Hermes
- Customer Hermes: Campaign Hermes

The existing repo explicitly names Campaign Hermes and Brand Hermes. The
simulation maps Brand Hermes to the client layer for most tenant setups, but a
real implementation should confirm whether the client is an agency, brand,
growth team, or in-house marketing team.

### Q: What client and customer-subject kinds are implied?

A:

- Client kinds: agency, in-house marketing team, growth team, brand program
- Customer-subject kinds: campaign, audience, offer, channel, account, buyer
  segment

### Q: What are the first workflow seeds?

A:

- Read-only workflow: campaign performance review
- Privileged workflow: campaign launch
- Gates: brief readiness, audience and privacy review, brand and claims review,
  creative approval, launch readiness, performance reverification

### Q: What can Omnigent do?

A: Adx Omnigent may draft briefs, creative concepts, campaign plans, audience
hypotheses, measurement plans, and performance reviews. It may not launch
campaigns, spend budget, make unsupported claims, or override tenant approval
policy.

### Q: What credentials are needed?

A: The repo does not yet declare a credential module. The simulation infers:
analytics read, ad account read, ad account write, CRM read, email send, and
social publish. Runtime grants should be required for all external systems.

### Q: What needs confirmation before real instantiation?

A:

- Whether the customer Hermes subject is a campaign, audience, account, buyer
  segment, or another marketing subject
- Whether Brand Hermes or Marketing Operator Hermes is the canonical client
  layer name
- Credential provider choices and approval rules
- First concrete workflow specs and examples
- Local validation command

## 4. LedgerxFactory Simulation

Structured record: `examples/pre-run-simulations/ledgerx.yaml`

### Q: What does this domain own?

A: `LedgerxFactory` owns the accounting and finance interpretation of the
xFactory rail: client intake, ledger workflows, reconciliations, close
readiness, tax boundaries, evidence requirements, compliance review, and bounded
accounting agent execution.

### Q: How do the three Hermes layers map?

A:

- Domain Hermes: Ledgerx Domain Hermes
- Client Hermes: Firm Hermes
- Customer Hermes: Client Hermes

The repo currently calls the subject layer `Client Hermes`. For the general
three-layer model, the simulation treats Firm Hermes as the client organization
layer and Client Hermes as the customer-subject layer. In real rollout, this
customer layer should be narrowed to company, ledger, engagement, tax matter,
filing, or report.

### Q: What client and customer-subject kinds are implied?

A:

- Client kinds: accounting firm, bookkeeping firm, finance team, controller
  organization
- Customer-subject kinds: company, ledger, tax matter, engagement, filing,
  report

### Q: What are the first workflow seeds?

A:

- Read-only workflow: client intake readiness
- Privileged workflow: filing review
- Gates: client intake readiness, document completeness, reconciliation review,
  close readiness, tax boundary review, final approval

### Q: What can Omnigent do?

A: Ledgerx Omnigent may draft reconciliations, exception lists, workpaper
summaries, document requests, close packets, and reporting support. It may not
file returns, issue final professional advice, override accounting policy, or
approve financial statements without required human authority.

### Q: What credentials are needed?

A: The repo does not yet declare a credential module. The simulation infers:
accounting system read, bank feed read, ledger write, document store read,
filing portal access, and payment approval.

### Q: What needs confirmation before real instantiation?

A:

- Canonical customer-subject name for each deployment
- Explicit three-layer Hermes overlays
- Credential module and grant rules
- Workflow specs beyond narrative gates
- Local validation command

## 5. MedxFactory Simulation

Structured record: `examples/pre-run-simulations/medx.yaml`

### Q: What does this domain own?

A: `MedxFactory` owns the medical interpretation of the xFactory rail:
patient truth, care-organization policy, medical-domain governance, Root Truth
DB governance, diagnostic and treatment reasoning support, decision foundation
loops, safety gates, and bounded medical expert orchestration.

### Q: How do the three Hermes layers map?

A:

- Domain Hermes: Medx Domain Hermes
- Client Hermes: Care Organization Hermes
- Customer Hermes: Patient Hermes

This repo already models the three logical authorities clearly. Patient Hermes
owns patient-specific truth, consent, preferences, memory, and patient-scoped
evidence. Care Organization Hermes owns clinic/practice/hospital/pharmacy/IDTF
operations, staff roles, standing orders, and local patient-care relationships.
Medx Domain Hermes owns medical-domain governance, Root Truth DB policy,
taxonomies, safety rules, validation rules, and review requirements.

### Q: What client and customer-subject kinds are implied?

A:

- Client kinds: clinic, group practice, hospital, pharmacy, imaging center,
  IDTF
- Customer-subject kinds: patient, patient case, decision candidate, care plan,
  diagnostic pathway

### Q: What are the first workflow seeds?

A:

- Read-only workflow: patient foundation review
- Privileged workflow: decision foundation loop
- Gates: decision scope gate, dependency mapping gate, reliability assessment
  gate, risk-of-wrong gate, clinician review routing gate

The `decision_foundation_loop` is event-driven around Decision Candidates and
is meant to validate foundational patient data before clinician-facing use.

### Q: What can Omnigent do?

A: Medx Omnigent may run bounded medical reasoning, dependency mapping,
reliability assessment support, simulation branching, specialist pod work, and
draft clinician review packages. It may not make clinical decisions, authorize
orders, silently rewrite patient facts, override deterministic safety gates, or
replace clinicians.

### Q: What credentials are needed?

A: The repo does not yet declare the starter credential module. The simulation
infers EHR patient read, scheduling write, patient messaging send, imaging
result read, and pharmacy reconciliation. Patient consent, care-organization
authorization, medical-domain policy, and human clinical review must gate
care-affecting use.

### Q: What needs confirmation before real instantiation?

A:

- Credential requirements and broker contract
- Patient consent model for each workflow
- Care-organization approver references
- Human clinical review requirements by workflow type
- Blocked-path and repair examples

## 6. codexFactory Simulation

Structured record: `examples/pre-run-simulations/codex.yaml`

### Q: What does this domain own?

A: `codexFactory` owns the engineering interpretation of the xFactory rail:
approved intent intake, feature decomposition, Spec Kit execution, coding-agent
implementation, deterministic validation, branch review, PR admission, merge
readiness, and repository-centered examples.

### Q: How do the three Hermes layers map?

A:

- Domain Hermes: Software Engineering Domain Hermes
- Client Hermes: Software Company Hermes
- Customer Hermes: Project Hermes

The repo currently names Project Hermes as the subject layer. The simulation
adds Software Company Hermes as the client layer needed for tenant rollout.

### Q: What client and customer-subject kinds are implied?

A:

- Client kinds: software team, product team, platform team, software agency
- Customer-subject kinds: project, repository, feature, pull request, release,
  incident

### Q: What are the first workflow seeds?

A:

- Read-only workflow: approved intent intake
- Privileged workflow: merge readiness
- Gates: feature decomposition, Spec Kit execution, deterministic validation,
  branch review, PR admission, merge readiness

### Q: What can Omnigent do?

A: Engineering workers may prepare branches, run coding-agent tasks, run tests,
linting, formatting, type checks, schema validation, secret scanning, branch
review, PR admission packets, and merge readiness summaries. They should not
store production secrets, long-lived credentials, patient data, medical runtime
state, or final governance authority.

### Q: What credentials are needed?

A: The repo does not yet declare the starter credential module. The simulation
infers repo read, branch write, PR write, package publish, deployment operator,
cloud read, and cloud deploy. Merge and deployment permissions must stay
behind workflow gates and external enforcement systems.

### Q: What needs confirmation before real instantiation?

A:

- Explicit Software Company Hermes layer
- Credential requirements and runtime grant model
- Tenant-specific check command mapping
- Human security review triggers
- Which external system enforces final merge/deploy

## 7. OpsxFactory Simulation

Structured record: `examples/pre-run-simulations/opsx.yaml`

### Q: What does this domain own?

A: `OpsxFactory` owns the IT operations interpretation of the xFactory rail:
sysops, devops, tenant administration, infrastructure operations, identity,
endpoint management, DNS, deployment operations, backup/restore, monitoring,
incident response, and bounded IT worker execution.

### Q: How do the three Hermes layers map?

A:

- Domain Hermes: Operations Domain Hermes
- Client Hermes: IT Customer Hermes
- Customer Hermes: Managed System Hermes

This repo already uses the explicit three-Hermes model. Managed System Hermes
owns the specific tenant, system, workload, service, DNS zone, backup vault, or
operational subject being worked.

### Q: What client and customer-subject kinds are implied?

A:

- Client kinds: managed IT customer, internal IT team, MSP customer, DevOps
  customer
- Customer-subject kinds: Microsoft 365 tenant, Azure subscription, GitHub
  organization, DNS zone, production service, backup vault, endpoint fleet

### Q: What are the first workflow seeds?

A:

- Read-only workflow: GitHub organization review
- Privileged workflow: DNS record update
- Highest-risk workflows: deployment and backup restore
- Evidence gates: approval packet, runtime capability grant, preflight report,
  operation plan, rollback plan, validation report, credential audit summary,
  revocation record

### Q: What can Omnigent do?

A: Opsx workers may execute bounded actions through declared worker
capabilities such as GitHub admin, DNS admin, Exchange migration, Entra admin,
Azure deploy, and backup restore. They must not receive standing global admin
credentials and must operate through scoped runtime grants.

### Q: What credentials are needed?

A: The repo declares Entra directory admin, Exchange admin, DNS admin, GitHub
organization admin, deployment operator, and backup operator. Grants require
approval, short maximum durations, audit, and revocation.

### Q: What needs confirmation before real instantiation?

A:

- Real provider adapter contracts
- Secret provider choice per client
- Real approver references
- Maintenance windows and rollback owners
- Complete golden-path, blocked-path, and repair examples

## 8. Recommended Next Work

1. Apply the starter v3 scaffold to `AdxFactory` and `LedgerxFactory` first;
   they are the lightest concept stacks and will stress-test the questionnaire.
2. Add credential modules to `MedxFactory`, `codexFactory`, `AdxFactory`,
   and `LedgerxFactory`.
3. Convert the simulated answer records into domain-owned
   `examples/instantiation-answers.example.yaml` files inside each domain repo.
4. Add blocked-path and repair examples for all domains.
5. Add local validators that check pre-run answer presence, workflow seeds,
   credential requirement references, and no raw secrets.
