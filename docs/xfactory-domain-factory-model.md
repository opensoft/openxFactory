# xFactory Domain Factory Model

This document generalizes `openWorkflow` from a software development factory
into the reusable `xFactory` pattern.

`openWorkflow` is the canonical workflow contract for xFactory. It defines the
general piping layer: authority boundaries, job envelopes, approvals,
traceability, worker routing, admission gates, review gates, and final
enforcement handoffs.

Domain factories apply domain-specific Hermes and Omnigent overlays on top of
that general piping layer.

## Core Idea

```text
xFactory / openWorkflow
  generic workflow contracts, gates, routing, and traceability

Domain factory
  xFactory plus domain-specific Hermes and Omnigent overlays

Subject layer
  patient, client, company, project, matter, campaign, or other specific input
```

Examples:

```text
opencodexFactory
  = xFactory + Opensoft Hermes overlay + Opensoft Omnigent overlay

MedxFactory
  = xFactory + Medx Domain Hermes overlay + Medx Omnigent overlay

LedgerxFactory
  = xFactory + LedgerX Hermes overlay + LedgerX Omnigent overlay

AdxFactory
  = xFactory + Adx Hermes overlay + Adx Omnigent overlay
```

The domain factory should not fork the xFactory contract. It should provide
overlays, policy packs, expert teams, tool bundles, memory boundaries, review
standards, and domain-specific workflows that plug into the same base contract.

## Layer Model

```text
Subject
  patient, client, company, project, matter, campaign

Subject Hermes layer
  subject-specific control, private memory, consent, preferences, context

Domain Hermes layer
  domain governance, domain agent team, policy, routing, review standards

xFactory / openWorkflow layer
  general job envelope, gates, traceability, worker routing, artifact contracts

Domain Omnigent layer
  domain-tuned orchestration, expert selection, task decomposition, checks

Base Omnigent layer
  generic agent harness, sessions, workers, tools, sandboxes

Execution substrates
  repos, documents, APIs, records, systems, devices, external tools
```

## Base Hermes and Hermes Overlays

Hermes should be installed as a reusable base runtime.

The base Hermes install owns:

- runtime installation
- profile loading
- memory-provider wiring
- Teams, email, search, and tool bridge wiring
- secret reference names, not secret values
- group registry loading
- backup, restore, and operational procedures

Domain Hermes overlays tune that base runtime for a domain.

A domain Hermes overlay owns:

- domain identity
- domain agent roster
- domain profile metadata
- domain policy
- domain memory boundaries
- domain workflow catalog
- domain approval gates
- domain escalation rules
- domain review standards
- domain tool routing

Subject Hermes overlays tune the domain runtime for one subject.

A subject Hermes overlay owns:

- subject identity
- subject-specific private context
- consent, authorization, and data-sharing boundaries
- subject goals and preferences
- subject timeline
- subject-specific agent assignments
- subject-specific memory
- subject-specific status and follow-up

The same base Hermes install can support many domain overlays. The same domain
Hermes overlay can support many subject Hermes overlays.

## Dual Hermes Layers

The domain Hermes layer and the subject Hermes layer must remain distinct.

```text
Subject Hermes
  "What does this specific subject need, allow, prefer, and remember?"

Domain Hermes
  "What does this domain know, require, permit, route, and review?"
```

The subject Hermes layer is a private concierge and lifetime-control layer.

It is close to the subject. In a medical factory, the subject is a patient. In
an accounting factory, the subject may be a client, company, ledger, or tax
matter. In a code factory, the subject may be a project, repo, product, or
feature initiative.

The domain Hermes layer is the shared domain control tower.

It is close to the expert team. It manages reusable domain expertise, domain
workflows, policy, review quality, escalation, and domain-level memory.

### Subject Hermes Owns

- subject-specific identity and context
- consent and authorization
- private memory
- active subject state
- user-facing communication
- preferences and goals
- subject timeline
- subject-specific team assignment
- subject-specific data-sharing decisions

### Domain Hermes Owns

- domain policy
- domain agent groups
- domain routing
- domain playbooks
- domain quality gates
- domain review councils
- domain memory
- escalation and exception policy
- domain tool and data-source permissions

## Product Domain Stack Repositories

The sellable domain stacks should live in separate repositories under the
`opensoft` GitHub organization.

```text
opensoft/MedxFactory
  medical domain stack

opensoft/LedgerxFactory
  accounting, finance, and ledger domain stack

opensoft/AdxFactory
  marketing, advertising, growth, and campaign domain stack

opensoft/opencodexFactory
  software, code, repo, and engineering domain stack
```

Each domain stack repo defines one productized domain factory. It may contain
multiple deployment profiles, such as clinic, group practice, hospital,
pharmacy, agency, bookkeeping firm, or software team.

The deployment profile should not become a separate repo unless it has a
separate product lifecycle, release process, compliance boundary, or sales
motion.

Tenant deployments are instantiated from a domain stack repo. A tenant may be a
clinic, hospital, pharmacy, marketing agency, accounting firm, or software
team. The tenant owns customer-specific configuration and isolation, while the
domain stack repo owns the reusable product definition.

```text
opensoft/MedxFactory
  -> clinic profile
    -> tenant deployment for Clinic A
      -> Patient Hermes for Patient 001
      -> Patient Hermes for Patient 002

  -> hospital profile
    -> tenant deployment for Hospital B
      -> Patient Hermes for Patient 900
```

Recommended shape:

```text
<Domain>Factory/
  README.md
  stack.yaml

  profiles/
    <deployment-profile>.yaml

  workflows/
    <workflow>.yaml

  hermes/
    domain/
      overlay.yaml
      roles/
      policies/
      review-councils/
      memory-boundaries.yaml
      escalation-rules.yaml

    subject/
      template.yaml
      memory-boundaries.yaml
      consent-model.yaml

  omnigent/
    domain-overlay.yaml
    expert-routing/
    validation-checks/
    output-templates/

  tenants/
    README.md
    examples/
```

For MedxFactory, the subject Hermes layer should be named Patient Hermes in
files and manifests because it spans the lifetime of the patient, not a single
case, referral, visit, or claim.

Recommended MedxFactory shape:

```text
MedxFactory/
  README.md
  stack.yaml

  profiles/
    clinic.yaml
    group-practice.yaml
    hospital.yaml
    pharmacy.yaml
    imaging-center.yaml
    idtf.yaml

  workflows/
    intake.yaml
    referral-management.yaml
    diagnostic-review.yaml
    prior-auth.yaml
    patient-follow-up.yaml
    pharmacy-reconciliation.yaml

  hermes/
    domain/
      overlay.yaml
      roles/
      policies/
      review-councils/
      memory-boundaries.yaml
      escalation-rules.yaml

    patient/
      template.yaml
      consent-model.yaml
      memory-boundaries.yaml
      lifetime-timeline.yaml
      data-sharing-rules.yaml

  omnigent/
    domain-overlay.yaml
    expert-routing/
    validation-checks/
    output-templates/

  tenants/
    README.md
    examples/
      clinic.yaml
      hospital.yaml
      pharmacy.yaml
```

## MedxFactory Example

```text
Patient
  -> Patient Hermes
  -> Medx Domain Hermes
  -> xFactory / openWorkflow
  -> Medx Omnigent
  -> Base Omnigent
  -> medical records, diagnostics, documents, scheduling, devices, tools
```

Patient Hermes answers:

- Who is this patient?
- What has the patient consented to?
- What is the current patient context?
- What does this patient need next?
- Which information may be shared with the domain layer?
- Which domain workflow should be requested?

Medx Domain Hermes answers:

- Which medical workflow applies?
- Which medical experts should participate?
- Which policy gates are required?
- Which review or escalation path applies?
- Which clinical, diagnostic, administrative, or IDTF standards apply?
- Is this safe to route directly to execution?

Medx Omnigent answers:

- How should the approved work be decomposed?
- Which medical expert agents should be invoked?
- Which tools, records, checks, and evidence are needed?
- Which outputs must be produced?
- Which domain checks or reviewers must validate the result?

## Routing Modes

The two Hermes layers support three routing modes.

### Direct Subject-to-Factory Route

```text
Subject Hermes
  -> xFactory / openWorkflow
  -> Domain Omnigent
```

Use this when the workflow is already approved, bounded, repeatable, and low
risk.

Example:

```text
Patient Hermes requests a standard follow-up packet that already matches an
approved Medx workflow template.
```

### Domain-Mediated Route

```text
Subject Hermes
  -> Domain Hermes
  -> xFactory / openWorkflow
  -> Domain Omnigent
```

Use this when domain judgment, triage, policy selection, specialty selection,
or approval is needed before execution.

Example:

```text
Patient Hermes asks for evaluation of a new symptom cluster. Medx Domain Hermes
selects the correct medical workflow, agents, gates, and escalation path before
creating the xFactory job.
```

### Escalated Domain Route

```text
Subject Hermes
  -> Domain Hermes
  -> domain review or human approval
  -> xFactory / openWorkflow
  -> Domain Omnigent
```

Use this when the request is high-risk, ambiguous, regulated, externally
visible, or outside a standing approval envelope.

Example:

```text
Patient Hermes requests an action that may affect care decisions. Medx Domain Hermes
requires domain review and explicit approval before execution.
```

## Learning and Memory Boundaries

Subject-specific data must not automatically mutate shared domain experts.

```text
Subject memory
  private, subject-specific, consent-bound

Domain memory
  shared, reviewed, de-identified when required, reusable across subjects

Base memory
  runtime and operational memory that is not domain expertise
```

Allowed promotion path:

```text
subject observation
  -> subject Hermes records private context
  -> domain Hermes reviews whether the lesson is reusable
  -> privacy, consent, and de-identification checks pass
  -> domain memory update is approved
  -> domain Hermes or domain Omnigent overlay is updated
```

Disallowed shortcut:

```text
patient data
  -> directly changes shared Medx experts
```

Domain experts should get better in their domain, but not by silently absorbing
private subject data.

## Domain Omnigent Overlays

Base Omnigent provides the general agent harness and execution substrate.

Domain Omnigent overlays tune that substrate for domain execution.

A domain Omnigent overlay owns:

- domain expert agent mappings
- domain task decomposition rules
- domain validation checks
- domain tool packs
- domain worker capabilities
- domain review packet shapes
- domain acceptance evidence rules
- domain output templates
- domain escalation hooks back to Hermes

In the current software factory, Polly is the engineering orchestrator inside
Omnigent. In other domains, the domain factory may use a different named
orchestrator, or it may use Polly with a domain-specific operating mode.

The generic rule remains:

```text
Hermes approves what should be done.
Omnigent decides how approved work is decomposed and executed.
xFactory defines the contract between them.
```

## Factory Contract Boundary

xFactory / openWorkflow owns general contract fields such as:

- job identity
- subject reference
- domain reference
- requesting Hermes layer
- approving Hermes layer
- allowed phase
- required outputs
- gates
- traceability chain
- worker requirements
- review requirements
- admission state
- final enforcement handoff

Domain factories own domain-specific fields such as:

- specialty routing
- domain policy references
- domain review council membership
- domain evidence requirements
- domain tool permissions
- domain data-source permissions
- domain-specific risk labels
- domain-specific output formats

Subject overlays own subject-specific fields such as:

- subject identifier
- consent references
- private context references
- subject timeline references
- subject team assignments
- subject-specific communication preferences

## Suggested Job Envelope Extension

The generic Hermes job envelope should support factory, domain, and subject
metadata without making xFactory domain-specific.

Example:

```yaml
factory:
  schema_version: 1
  factory_kind: MedxFactory
  xfactory_contract: openWorkflow
  xfactory_contract_version: "2026-06-27"

domain:
  id: medx
  stack_repo: github.com/opensoft/MedxFactory
  hermes_overlay: hermes/domain
  omnigent_overlay: omnigent
  policy_refs:
    - medx/policies/diagnostic-review.yaml
  review_profile: medx_standard_review

subject:
  subject_kind: patient
  subject_ref: patient-hermes://patients/<patient-id>
  patient_hermes_ref: hermes://patients/<patient-id>
  consent_refs:
    - patient-hermes://patients/<patient-id>/consents/current
  private_context_refs:
    - patient-hermes://patients/<patient-id>/timeline/current

routing:
  requested_by: patient_hermes
  approved_by: domain_hermes
  route_mode: domain_mediated
```

The xFactory layer validates that these fields exist and are internally
consistent. The domain factory validates whether the referenced policies,
consents, tools, and experts are appropriate for the requested work.

## Repository Ownership

Recommended ownership:

```text
openWorkflow
  canonical xFactory contracts and general workflow policy

Hermes-Install
  reusable Hermes installation, restore, runtime wiring, and profile loading

Agents/<Domain>
  domain Hermes roster, identity references, profile metadata, and overlays

omnigent
  base Omnigent runtime and harness

opensoft/<Domain>Factory
  productized domain stack with Hermes and Omnigent overlays

subject registries
  private subject Hermes overlays and subject-specific memory references
```

The domain stack repo may reference existing agent registries, such as
`Agents/Medx`, `Agents/LedgerX`, or `Agents/Opensoft`, but the sellable stack
definition belongs in the domain factory repo.

## Design Rules

1. xFactory is domain-neutral.
2. Domain factories are overlays, not forks.
3. Subject Hermes and domain Hermes are separate authority layers.
4. Subject data remains subject-bound unless explicitly promoted.
5. Domain learning requires review, approval, and privacy checks.
6. Hermes approves intent and policy.
7. Omnigent executes approved work.
8. openWorkflow defines the handoff contract.
9. Domain overlays may add gates, but must not bypass base xFactory gates.
10. Direct subject-to-factory routing is allowed only inside a standing domain approval envelope.
