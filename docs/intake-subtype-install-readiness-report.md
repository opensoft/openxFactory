# Intake Subtype Install Readiness Report

Status: generated simulation report
Repository context: openxFactory

## Meaning

This is pass 1. It checks every intake subtype against the current local
catalog and local factory repo state. It does not assume any runtime
bindings, credentials, adapters, approvals, validation results, or dry-run
evidence have been collected.

## Summary

- Subtypes checked: 100
- Installable candidates in current local state: 0
- Require domain scaffold or artifact work: 50
- Template catalog only because factory repo is missing locally: 50
- Subtypes blocked by missing local factory repo: 50

## Gap Code Legend

- `repo`: factory repo is missing locally.
- `workflows:N`: subtype workflow specs are missing.
- `repo_credentials:N`: domain repo credential requirements are missing.
- `template_credentials:N`: subtype credential family details are not defined in the top-level intake template.
- `adapters:N`: adapter contract stubs are missing.
- `runtime`: deployment target, Hermes, Omnigent, vault refs, adapter endpoints, approvers, validation, dry-run, and live approval are not yet bound.

Machine-readable detail: [pass1.yaml](../examples/intake-runtime-simulations/pass1.yaml).

## Per-Subtype Results

### medical -> MedxFactory

| Subtype | Current readiness | Missing domain artifacts | Runtime missing |
| --- | --- | --- | --- |
| `clinical_operations.clinic` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `clinical_operations.group_practice` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `clinical_operations.hospital` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `clinical_operations.pharmacy` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `clinical_operations.imaging_center` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `clinical_operations.telehealth` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `clinical_operations.lab` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:1, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `clinical_operations.behavioral_health` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `clinical_operations.dental` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:1, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `clinical_operations.home_health` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |

### operations -> OpsxFactory

| Subtype | Current readiness | Missing domain artifacts | Runtime missing |
| --- | --- | --- | --- |
| `identity_admin.m365` | `domain_scaffold_required` | workflows:3, repo_credentials:1, adapters:3, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `exchange.mailbox_migration` | `domain_scaffold_required` | workflows:3, repo_credentials:2, template_credentials:1, adapters:3, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `endpoint.intune` | `domain_scaffold_required` | workflows:3, repo_credentials:2, template_credentials:1, adapters:3, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `cloud_ops.azure` | `domain_scaffold_required` | workflows:3, repo_credentials:2, template_credentials:2, adapters:3, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `cloud_ops.aws` | `domain_scaffold_required` | workflows:3, repo_credentials:2, template_credentials:2, adapters:3, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `dns.domain_ops` | `domain_scaffold_required` | workflows:3, repo_credentials:2, template_credentials:1, adapters:3, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `backup.dr` | `domain_scaffold_required` | workflows:3, repo_credentials:2, template_credentials:1, adapters:3, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `network.firewall` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:2, adapters:4, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `devops.github_org` | `domain_scaffold_required` | workflows:3, repo_credentials:2, template_credentials:3, adapters:3, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `security.incident_response` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:2, adapters:4, hermes_agent_mixes_missing, subtype_profile_missing | runtime |

### accounting -> LedgerxFactory

| Subtype | Current readiness | Missing domain artifacts | Runtime missing |
| --- | --- | --- | --- |
| `bookkeeping.small_business` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `bookkeeping.property_management` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:1, adapters:3, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `tax.individual` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:3, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `tax.business` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `audit.support` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `month_end.close` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `payroll.ops` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:1, adapters:3, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `accounts_payable.ops` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:2, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `accounts_receivable.ops` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:2, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `controller.finance_ops` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |

### marketing -> AdxFactory

| Subtype | Current readiness | Missing domain artifacts | Runtime missing |
| --- | --- | --- | --- |
| `campaign_ops.paid_media` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `lifecycle.email` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `brand.claims` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `content.seo` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:1, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `social.community` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:2, adapters:3, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `product_marketing.launch` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:1, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `analytics.attribution` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `ecommerce.growth` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:1, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `partner.channel` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:2, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `pr.communications` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:2, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |

### software -> codexFactory

| Subtype | Current readiness | Missing domain artifacts | Runtime missing |
| --- | --- | --- | --- |
| `product_engineering.repo_delivery` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `release_ops.cicd` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `incident_response.software` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `security.appsec` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:2, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `data_engineering.pipelines` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:2, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `mlops.model_delivery` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:1, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `platform_engineering.internal_tools` | `domain_scaffold_required` | workflows:3, repo_credentials:3, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `qa.test_automation` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:1, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `docs.developer_experience` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:1, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |
| `product_management.requirements` | `domain_scaffold_required` | workflows:3, repo_credentials:3, template_credentials:2, adapters:4, credential_requirements_file_missing, domain_validator_missing, hermes_agent_mixes_missing, subtype_profile_missing | runtime |

### law -> LegalxFactory

| Subtype | Current readiness | Missing domain artifacts | Runtime missing |
| --- | --- | --- | --- |
| `compliance.medical.pharmacy` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:4 | runtime |
| `compliance.medical.clinic` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:4 | runtime |
| `compliance.privacy.healthcare` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:4 | runtime |
| `compliance.employment.payroll` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:4 | runtime |
| `compliance.finance.broker_dealer` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:4 | runtime |
| `contract_review.saas.vendor` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `contract_review.healthcare.vendor` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `legal_ops.matter_management` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:4 | runtime |
| `litigation.discovery` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:3 | runtime |
| `policy.governance` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:3 | runtime |

### insurance -> InsurexFactory

| Subtype | Current readiness | Missing domain artifacts | Runtime missing |
| --- | --- | --- | --- |
| `claims.property_casualty` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `claims.health` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:4 | runtime |
| `claims.workers_comp` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:3 | runtime |
| `underwriting.commercial` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `underwriting.personal_lines` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `policy_ops.brokerage` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `actuarial.pricing` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:3 | runtime |
| `insurance.compliance` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:3, adapters:3 | runtime |
| `subrogation.recovery` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:3 | runtime |
| `risk_engineering.loss_control` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:3 | runtime |

### manufacturing -> MakexFactory

| Subtype | Current readiness | Missing domain artifacts | Runtime missing |
| --- | --- | --- | --- |
| `quality_ops.plant` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `maintenance.asset` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `safety.ehs` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `production_planning.scheduling` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:3 | runtime |
| `procurement.supplier_quality` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:3 | runtime |
| `inventory.materials` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:3 | runtime |
| `regulatory.gmp` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:3 | runtime |
| `engineering.change_control` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:3 | runtime |
| `field_service.equipment` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:3, adapters:3 | runtime |
| `energy.utilities_ops` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:3 | runtime |

### logistics -> FlowxFactory

| Subtype | Current readiness | Missing domain artifacts | Runtime missing |
| --- | --- | --- | --- |
| `freight_ops.carrier` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `warehouse_ops.inventory` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `supply_chain.procurement` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `transportation.fleet` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:4 | runtime |
| `cold_chain.compliance` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:3 | runtime |
| `customs.trade_compliance` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:3, adapters:3 | runtime |
| `last_mile.delivery` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:3 | runtime |
| `reverse_logistics.returns` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:4 | runtime |
| `logistics.customer_service` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:4 | runtime |
| `planning.demand_forecast` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:4 | runtime |

### retail -> CommerxFactory

| Subtype | Current readiness | Missing domain artifacts | Runtime missing |
| --- | --- | --- | --- |
| `ecommerce_ops.marketplace` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `customer_ops.returns` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `merchandising.pricing` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, adapters:3 | runtime |
| `inventory.replenishment` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:3 | runtime |
| `store_ops.physical` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:3 | runtime |
| `loyalty.crm` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:3, adapters:4 | runtime |
| `fraud.chargebacks` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:3 | runtime |
| `product_content.catalog` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:3 | runtime |
| `retail.analytics` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:1, adapters:4 | runtime |
| `subscription.commerce` | `template_catalog_ready` | repo, workflows:3, repo_credentials:3, template_credentials:2, adapters:4 | runtime |
