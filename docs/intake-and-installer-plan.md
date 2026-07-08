# xFactory Intake And Installer Plan

Status: draft
Kind: plan
Repository context: openxFactory
Purpose: define how xFactory collects pre-run answers through a hosted website,
a terminal UI, and a downloadable installer, then turns those answers into an
installable candidate package.

## 1. Core Idea

xFactory should have one shared intake contract and multiple intake surfaces.

```text
factory type and subtype template
  -> intake answers
  -> AI bridge and gap fill
  -> user confirmation
  -> instantiation packet
  -> starter application
  -> validation
  -> install or runtime gap report
```

The website, TUI, and downloadable installer must produce the same structured
answer artifact. They may look different, but they should not ask incompatible
questions or generate incompatible files.

## 2. Intake Surfaces

### 2.1 Hosted Website Intake

Use the website intake when Opensoft is hosting, selling, scoping, or onboarding
a client.

Primary users:

- prospective customer
- Opensoft sales or implementation lead
- client operations lead
- domain implementation lead

Best for:

- guided qualification
- industry-specific branching
- saved drafts
- team review
- Opensoft-hosted install request
- handoff to implementation staff

Website outputs:

- pre-run answer packet
- implementation gap report
- recommended domain stack
- recommended profile
- installability score
- quote or scope inputs when needed
- downloadable instantiation package

### 2.2 Terminal UI Self-Install

Use the TUI when the user wants a full self-install from a terminal, SSH
session, server console, or developer workstation.

Primary users:

- technical customer
- Opensoft engineer
- managed service operator
- self-hosting administrator
- domain repo maintainer

Best for:

- offline or local-first setup
- server installation
- repeatable domain factory scaffolding
- CI-friendly validation
- users who do not want a browser-based onboarding flow

Recommended commands:

```bash
xfactory intake
xfactory intake --industry medical
xfactory intake --answers examples/instantiation-answers.generated.yaml
xfactory install --answers examples/instantiation-answers.generated.yaml
xfactory validate
```

TUI outputs should match the website outputs, with an additional local install
log and validation transcript.

### 2.3 Downloadable Flutter Installer

Use the Flutter installer when the user wants a packaged guided installer that
runs on common desktop platforms and can later share UI code with mobile or web
surfaces.

Primary users:

- non-technical customer
- client administrator
- Opensoft implementation partner
- technical user who wants a visual local installer

Best for:

- guided local setup
- cross-platform downloads
- offline draft creation
- packaging an instantiation bundle
- local validation before sending data to Opensoft

The Flutter installer should be a UI shell over the same intake schema and
template engine used by the website and TUI. It should not invent a separate
configuration language.

Flutter installer outputs:

- local instantiation bundle
- optional zip export
- local validation report
- install log
- next-step checklist
- optional handoff package for Opensoft-hosted deployment

## 3. Shared Intake Engine

All three surfaces should use the same intake engine.

The shared engine owns:

- factory template loading
- factory taxonomy mapping
- question schema
- branching rules
- answer quality labels
- AI bridge prompts and guardrails
- generated artifact shape
- validation rules
- readiness classification

Recommended package boundaries:

```text
intake-schema/
  question schema, answer schema, validation rules

factory-templates/
  medical, law, ops, software, marketing, accounting, custom

intake-engine/
  load template, merge answers, classify gaps, generate artifacts

intake-ai-bridge/
  infer missing fields, label assumptions, produce gap suggestions

website-intake/
  hosted web form

tui-intake/
  terminal wizard

flutter-installer/
  downloadable visual installer
```

The first implementation can live inside a domain-neutral xFactory tool repo,
but the contract belongs in openxFactory.

## 4. Factory Templates

The intake starts by separating the work being performed from the industry of
the company using the factory. See
[xFactory Taxonomy Model](factory-taxonomy-model.md).

Starter templates live in [templates/intake](../templates/intake/README.md).
The template index is [templates/intake/index.yaml](../templates/intake/index.yaml).
The subtype catalog is
[templates/intake/subtypes/catalog.yaml](../templates/intake/subtypes/catalog.yaml).

The current install-readiness loop for every factory type and subtype is
documented in:

- [Intake Subtype Install Readiness Report](intake-subtype-install-readiness-report.md)
- [Intake Subtype Install Runbook](intake-subtype-install-runbook.md)
- [Intake Subtype Second-Pass Gap Report](intake-subtype-second-pass-gap-report.md)

Primary template selection uses:

```text
factory_type + factory_subtype
```

Target-domain overlays use:

```text
target_domain + target_domain_subtype
```

Client-specific language and deployment assumptions use:

```text
client_industry + client_type
```

Initial templates:

```text
medical
  MedxFactory

ops
  OpsxFactory

software
  codexFactory

marketing
  AdxFactory

accounting
  LedgerxFactory

law
  LegalxFactory
  profiles:
    compliance.medical.pharmacy
    compliance.medical.clinic
    contract_review.saas.vendor

custom
  new xFactory domain
```

Each template should define:

- default domain factory repo
- domain Hermes name
- client Hermes aliases
- customer Hermes aliases
- client or organization types
- customer-subject types
- common workflows
- common credential families
- default risk classes
- default Hermes council modes
- default source authority rules
- compliance prompts
- required golden-path and blocked-path examples

Templates provide defaults, not approval. Any default that is not confirmed by
the user or responsible stakeholder remains `template_default` or `inferred`.

Example:

```yaml
factory_type: law
factory_subtype: compliance
target_domain: medical
target_domain_subtype: pharmacy
client_industry: legal_services
client_type: law_firm
recommended_factory: LegalxFactory
recommended_profile: compliance.medical.pharmacy
```

This selects a legal/compliance expert stack about pharmacy rules. It should
not select the clinical `MedxFactory` stack unless the work is clinical medical
operations.

## 5. Intake Form Families

### 5.1 Short Website Lead Form

This form qualifies the request and selects the template.

Minimum fields:

- factory type
- factory subtype
- target domain
- target domain subtype
- client industry
- organization type
- hosted by Opensoft, client, or hybrid
- target domain stack, if known
- first workflow desired
- systems likely touched
- whether the workflow reads, writes, sends, publishes, administers, deletes,
  affects care, moves money, or changes production
- contact and organization references

Output:

```text
lead_qualified
template_selected
requires_full_pre_run
```

### 5.2 Full Pre-Run Intake Form

This is the canonical form for generating an instantiation packet.

Sections:

- answer quality
- domain identity
- three Hermes layers
- Hermes Mixture of Agents and council modes
- client or tenant shape
- customer-subject model
- workflows and gates
- Omnigent layer
- credential requirement families
- source authority and evidence
- compliance and human authority
- examples and validation

Output:

```text
pre_run_complete
instantiation_answers.generated.yaml
pre_run_gap_report.md
```

### 5.3 Advanced Install Form

This form is for self-install and technical onboarding.

Additional fields:

- target repo path
- target branch
- domain starter version
- Hermes install path or remote
- Omnigent install path or remote
- secret provider type
- non-secret vault reference names
- adapter packages to enable
- local validation command
- deployment profile
- environment name
- runtime operator

Output:

```text
installable_candidate
install_manifest.generated.yaml
setup_runbook.generated.md
```

### 5.4 Runtime Binding Wizard

This is not part of the pre-run questionnaire. It happens later when an
authorized operator is ready to wire real runtime references.

Allowed:

- secret provider names
- vault reference names
- OAuth app registration references
- workload identity references
- approver group references
- environment references

Forbidden:

- raw passwords
- API keys
- OAuth refresh tokens
- private keys
- production connection strings
- private patient, customer, financial, campaign, source code, or tenant data

Output:

```text
runtime_binding_candidate
runtime_gap_report.md
```

## 6. AI Bridge

The AI bridge helps move from a premade factory template and target-domain
overlay to a useful
instantiation packet.

It may:

- infer likely Hermes aliases from industry and organization type
- suggest workflows
- suggest credential families
- suggest risk gates
- suggest Hermes council modes
- suggest Omnigent worker classes
- generate golden-path and blocked-path examples
- produce a gap report
- explain what must be confirmed

It must not:

- mark inferred answers as approved
- invent live credentials
- collect secrets
- approve live execution
- replace professional, client, human, or external authority

Answer quality labels:

```text
declared
  user answered directly

template_default
  supplied by the factory template or target-domain overlay

inferred
  AI inferred from provided answers and template context

simulated
  AI generated as an example

confirmed
  user or stakeholder confirmed

approved_for_instantiation
  responsible authority approved for generating install artifacts
```

## 7. Generated Artifacts

The intake should generate non-secret artifacts only.

Recommended outputs:

```text
examples/instantiation-answers.generated.yaml
docs/pre-run-gap-report.md
docs/setup-runbook.generated.md
stack.generated.yaml
credentials/requirements.generated.yaml
hermes/domain/agent-mixes.generated.yaml
workflows/workflow-seeds.generated.yaml
install_manifest.generated.yaml
validation_report.md
```

For an existing repo, the installer should prefer patch files or generated
artifacts over overwriting domain-owned files.

Recommended patch outputs:

```text
patches/stack.patch.yaml
patches/credential-requirements.patch.yaml
patches/hermes-agent-mixes.patch.yaml
patches/workflow-seeds.patch.yaml
```

## 8. Readiness Levels

The intake and installer should classify the result.

```text
lead_qualified
  enough to route the prospect or user to the right factory template and
  target-domain overlay

pre_run_complete
  questionnaire answers are complete enough to evaluate

approved_for_instantiation
  responsible authority approved answers for artifact generation

installable_candidate
  non-secret install artifacts can be generated

install_ready
  target repo, starter, local paths, and validation command are available

runtime_ready
  Hermes, Omnigent, adapters, secret references, and bindings are wired

workflow_ready
  at least one workflow can run through dry-run gates

live_ready
  live client or customer-subject execution is approved
```

Pre-run can usually reach `installable_candidate`. It should not claim
`runtime_ready`, `workflow_ready`, or `live_ready` without actual runtime
bindings, adapters, validation, approvals, and dry-run evidence.

For self-hosted deployments, the next stage is the runtime binding wizard. See
[Self-Hosted Runtime Binding Plan](self-hosted-runtime-binding-plan.md) for how
the installer collects deployment targets, Hermes and Omnigent runtime
references, secret provider references, adapter endpoints, approver references,
validation results, and dry-run evidence without storing raw secrets in repos or
support bundles.

## 9. Install Flow

Shared flow:

```text
1. Select intake surface.
2. Ask industry and organization type.
3. Load factory template and target-domain overlay.
4. Ask required template questions.
5. Run AI bridge for gaps.
6. Show inferred and template-default answers separately from declared answers.
7. Ask user to confirm or leave gaps.
8. Generate pre-run answer packet.
9. Generate gap report.
10. Generate installable candidate artifacts when allowed.
11. Apply starter or patch only after user confirmation.
12. Run local validation.
13. Produce final readiness classification and next-step checklist.
```

Website install request:

```text
website intake
  -> saved answer packet
  -> Opensoft review
  -> approved_for_instantiation
  -> managed install or handoff package
```

TUI self-install:

```text
xfactory intake
  -> local answer packet
  -> xfactory install
  -> apply starter or generated patches
  -> make validate
  -> readiness report
```

Flutter installer:

```text
guided local form
  -> local answer packet
  -> optional AI bridge
  -> local artifact generation
  -> local validation
  -> zip export or local install
```

Self-hosted runtime binding:

```text
installable candidate
  -> bind local runtime
  -> connect vault references
  -> connect adapters
  -> configure approvers
  -> validate runtime
  -> dry-run first workflow
  -> runtime_ready or gap report
```

## 10. Safety Rules

All intake surfaces must enforce:

- no raw secrets
- no private records in pre-run examples
- answer quality labels are mandatory
- inferred answers cannot become approved without confirmation
- privileged workflows require credential families and approval paths
- high-risk workflows require a Hermes council mode
- reference agents do not receive tools
- reference agents do not receive runtime grants
- generated artifacts are non-secret by default
- runtime binding is a separate stage

## 11. Implementation Phases

### Phase 1: Contract

- Define intake answer schema.
- Define factory template and target-domain overlay schema.
- Define generated artifact manifest.
- Define readiness classifier.
- Define validation rules.

### Phase 2: CLI And TUI

- Implement `xfactory intake`.
- Implement `xfactory validate-intake`.
- Implement `xfactory install --answers`.
- Use local files only.
- Generate non-secret artifacts and gap reports.

### Phase 3: Website Intake

- Build hosted form from the shared question schema.
- Add saved drafts.
- Add factory template and target-domain overlay selection.
- Add AI bridge review.
- Add handoff package download.
- Add Opensoft review queue.

### Phase 4: Flutter Installer

- Build a cross-platform guided installer over the same schema.
- Support offline draft mode.
- Support local validation.
- Support artifact export.
- Support optional handoff to Opensoft.

### Phase 5: Runtime Binding

- Add provider reference wizard.
- Add adapter checks.
- Add Hermes and Omnigent install checks.
- Add dry-run workflow checks.
- Add live readiness gate.

## 12. Open Decisions

- Which repo owns the shared intake engine implementation?
- Should the website and Flutter app call a hosted AI bridge, a local model, or
  both?
- Which platforms should the first Flutter installer target?
- Should the TUI use the same binary as the CLI installer?
- Should install bundles be signed before use?
- How should Opensoft-hosted review queues store non-secret answer packets?
