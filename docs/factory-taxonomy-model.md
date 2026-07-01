# xFactory Taxonomy Model

Status: shared xFactory standard
Repository context: openxFactory
Purpose: separate the kind of work an xFactory performs from the industry of
the company using it and the regulated or operational domain the work is about.

## 1. Why This Exists

The first instinct is to ask, "What industry is this company in?" That is
useful, but it is not enough to choose the right xFactory template.

A hospital using xFactory for patient care is not the same as a law firm using
xFactory for medical compliance. Both involve healthcare, but they require
different expert teams, workflows, risk models, credentials, review standards,
and authority boundaries.

The template selection question must therefore separate:

```text
Who is using the factory?
What kind of work does the factory perform?
What domain is the work about?
What narrower regulated or operational context is in scope?
```

## 2. Taxonomy Axes

Use these axes for intake, templates, and domain repo design.

```yaml
factory_type: <professional-work-type>
factory_subtype: <specialized-service-area>
target_domain: <domain-being-worked-on>
target_domain_subtype: <narrower-domain-context>
client_industry: <industry-of-the-buyer-or-operator>
client_type: <kind-of-organization-operating-the-stack>
customer_subject_type: <thing-at-the-top-of-the-stack>
```

### Factory Type

`factory_type` describes the kind of expert work the xFactory performs.

Examples:

- medical
- law
- accounting
- marketing
- operations
- software
- insurance
- manufacturing
- logistics
- retail

### Factory Subtype

`factory_subtype` narrows the professional service area.

Examples:

- clinical_operations under `medical`
- compliance under `law`
- contract_review under `law`
- tax under `accounting`
- bookkeeping under `accounting`
- paid_media under `marketing`
- identity_admin under `operations`
- devops under `operations`

### Target Domain

`target_domain` describes the domain the work is about.

Examples:

- medical
- pharmacy
- insurance
- employment
- privacy
- finance
- retail
- construction
- education

### Target Domain Subtype

`target_domain_subtype` narrows the subject matter.

Examples:

- pharmacy under medical
- imaging_center under medical
- hospital under medical
- HIPAA under privacy or medical
- payroll under employment
- bank_feed under finance
- M365 under operations

### Client Industry

`client_industry` describes the industry of the company buying or operating the
factory.

Examples:

- healthcare
- legal_services
- accounting_services
- marketing_agency
- managed_service_provider
- manufacturing
- ecommerce
- insurance

### Client Type

`client_type` describes the organization shape.

Examples:

- clinic
- hospital
- pharmacy
- law_firm
- compliance_consultant
- accounting_firm
- agency
- managed_service_provider
- software_company

### Customer Subject Type

`customer_subject_type` describes the thing at the top of the xFactory stack.

Examples:

- patient
- matter
- compliance_engagement
- ledger
- campaign
- managed_system
- repo
- claim
- shipment

## 3. Template Selection Rule

The primary template is selected by `factory_type` and `factory_subtype`, not
by `client_industry` alone.

```text
factory_type + factory_subtype
  selects the expert team, workflows, authority model, and Omnigent overlay

target_domain + target_domain_subtype
  selects the subject matter overlays, source authorities, and domain rules

client_industry + client_type
  selects client Hermes aliases, integrations, deployment assumptions, and
  sales/onboarding language
```

This prevents healthcare, law, compliance, and consulting scenarios from
collapsing into one overloaded medical template.

## 4. Medical Clinical Versus Medical Compliance

Medical clinical work:

```yaml
factory_type: medical
factory_subtype: clinical_operations
target_domain: medical
target_domain_subtype: clinic
client_industry: healthcare
client_type: clinic
customer_subject_type: patient
recommended_factory: MedxFactory
```

This stack helps medical operators perform medical workflows. Its Omnigent
layer is tuned toward clinical, patient, care, referral, diagnostic, intake, and
follow-up workflows under medical authority.

Medical compliance work:

```yaml
factory_type: law
factory_subtype: compliance
target_domain: medical
target_domain_subtype: pharmacy
client_industry: legal_services
client_type: law_firm
customer_subject_type: compliance_engagement
recommended_factory: LegalxFactory
recommended_profile: compliance.medical.pharmacy
```

This stack helps legal or compliance professionals perform compliance work
about medical/pharmacy rules. Its Omnigent layer is tuned toward law,
regulation, policy, audit, evidence, risk, and compliance review. It may use
medical source material, but it is not a clinical care stack.

## 5. Legal And Compliance Nesting

Compliance can be modeled as a subtype under law when the factory performs
legal, regulatory, policy, audit, or compliance advisory work.

```text
LegalxFactory
  compliance
    medical
      pharmacy
    medical
      clinic
    privacy
      healthcare
    employment
      payroll
    finance
      broker_dealer
```

Store this nesting as structured data rather than an infinitely deep folder
tree.

```yaml
factory_type: law
factory_subtype: compliance
target_domain: medical
target_domain_subtype: pharmacy
```

The repo may provide profiles for common combinations:

```text
profiles/
  compliance.medical.pharmacy.yaml
  compliance.medical.clinic.yaml
  compliance.privacy.healthcare.yaml
  compliance.employment.payroll.yaml
```

## 6. Omnigent Expert Boundary

The Omnigent layer follows the factory type, not just the target domain.

Medical clinical stack:

```text
MedxFactory Omnigent
  clinical workflow experts
  medical reasoning reviewers
  patient-care documentation workers
  referral and care coordination workers
```

Medical compliance legal stack:

```text
LegalxFactory compliance Omnigent
  compliance law experts
  regulatory research workers
  policy mapping workers
  audit evidence reviewers
  risk and remediation planners
```

The legal compliance stack may include medical subject matter references and
medical-domain source authorities, but its authority is legal/compliance
analysis, not diagnosis, treatment, or clinical action.

## 7. Intake Questions

The intake flow should ask these separately:

1. What kind of work should the factory perform?
2. What subtype of that work is needed?
3. What industry is your organization in?
4. What kind of organization are you?
5. What domain is the work about?
6. What narrower domain subtype is in scope?
7. What is the customer subject at the top of the stack?

Example:

```text
What kind of work should the factory perform?
  law

What subtype?
  compliance

What is the work about?
  medical

What narrower context?
  pharmacy

Who is operating it?
  law firm

Recommended template:
  LegalxFactory / compliance.medical.pharmacy
```

## 8. Template Metadata

Every template should declare these fields:

```yaml
schema_version: 1
kind: xfactory_template_metadata

template:
  id: compliance.medical.pharmacy
  factory_type: law
  factory_subtype: compliance
  target_domain: medical
  target_domain_subtype: pharmacy
  supported_client_industries:
    - legal_services
    - compliance_consulting
    - healthcare
  supported_client_types:
    - law_firm
    - compliance_consultant
    - pharmacy_operator
  default_customer_subject_type: compliance_engagement
  recommended_factory: LegalxFactory
```

This metadata should drive website intake, TUI self-install, downloadable
installer branching, and AI bridge gap filling.

## 9. Naming Guidance

Top-level repos should represent stable factory types:

```text
MedxFactory
LegalxFactory
LedgerxFactory
AdxFactory
OpsxFactory
codexFactory
```

Profiles should represent subtypes and target domains:

```text
LegalxFactory profile: compliance.medical.pharmacy
LegalxFactory profile: contract_review.saas.vendor
MedxFactory profile: clinical_operations.clinic
OpsxFactory profile: identity_admin.m365
LedgerxFactory profile: tax.small_business
```

Do not create a new top-level repo for every target-domain combination unless
the work type, authority model, Omnigent expert team, and reusable workflow
surface are genuinely different.
