# Intake Subtype Second-Pass Gap Report

Status: generated simulation report
Repository context: openxFactory

## Meaning

This is pass 2. It simulates the state after the generic runbook-created
factory scaffold, profile, workflow, credential, adapter, and Hermes mix
artifacts exist. The remaining gaps are the pieces that cannot be safely
invented by templates and must come from a customer, operator, domain
expert, provider, or live runtime.

## Summary

- Subtypes checked: 100
- All subtypes can reach: `installable_candidate` after generic scaffold fixes.
- No subtype can reach: `runtime_ready`, `workflow_ready`, or `live_ready` without runtime binding.

Machine-readable detail: [pass2.yaml](../examples/intake-runtime-simulations/pass2.yaml).

## Remaining Gap Families

- domain SME confirmation
- workflow semantics confirmation
- credential scope confirmation
- adapter implementation or package selection
- deployment target
- Hermes runtime
- Omnigent runtime
- secret provider and credential bindings
- adapter endpoints
- approvers
- runtime validation
- dry-run evidence
- live approval

## Per-Subtype Remaining Runtime Focus

### medical -> MedxFactory

| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |
| --- | --- | --- | --- |
| `clinical_operations.clinic` | `ehr_patient_read`, `scheduling_write`, `patient_messaging_send` | `ehr`, `practice_management`, `scheduling`, `patient_messaging` | `ehr_connectivity`, `scheduling_access`, `patient_messaging_approval`, `audit_store` |
| `clinical_operations.group_practice` | `ehr_patient_read`, `care_team_roster_read`, `scheduling_write` | `ehr`, `provider_directory`, `scheduling`, `document_repository` | `provider_roster`, `ehr_access`, `referral_sources`, `care_team_approvers` |
| `clinical_operations.hospital` | `ehr_patient_read`, `care_team_roster_read`, `scheduling_write` | `ehr`, `care_team_roster`, `scheduling`, `document_repository` | `ehr_connectivity`, `care_team_roster`, `discharge_sources`, `hospital_audit` |
| `clinical_operations.pharmacy` | `pharmacy_system_read`, `patient_messaging_send`, `payer_portal_read` | `pharmacy_system`, `payer_portal`, `patient_messaging`, `document_repository` | `pharmacy_system_access`, `payer_portal_access`, `patient_consent`, `pharmacist_review` |
| `clinical_operations.imaging_center` | `imaging_system_read`, `referral_document_read`, `provider_messaging_send` | `imaging_system`, `referral_document_store`, `provider_messaging`, `scheduling` | `imaging_system_access`, `referral_sources`, `provider_messaging`, `audit_store` |
| `clinical_operations.telehealth` | `ehr_patient_read`, `scheduling_write`, `patient_messaging_send` | `ehr`, `telehealth_platform`, `scheduling`, `patient_messaging` | `telehealth_platform`, `ehr_access`, `patient_messaging`, `clinical_escalation` |
| `clinical_operations.lab` | `lab_system_read`, `referral_document_read`, `provider_messaging_send` | `lis`, `ehr`, `provider_messaging`, `document_repository` | `lis_access`, `result_sources`, `provider_messaging`, `audit_store` |
| `clinical_operations.behavioral_health` | `ehr_patient_read`, `scheduling_write`, `patient_messaging_send` | `ehr`, `scheduling`, `patient_messaging`, `document_repository` | `ehr_access`, `sensitive_record_controls`, `crisis_escalation`, `messaging_approval` |
| `clinical_operations.dental` | `practice_management_read`, `scheduling_write`, `patient_messaging_send` | `dental_practice_management`, `scheduling`, `payer_portal`, `patient_messaging` | `practice_management_access`, `scheduling`, `payer_portals`, `patient_messaging` |
| `clinical_operations.home_health` | `ehr_patient_read`, `scheduling_write`, `payer_portal_read` | `ehr`, `scheduling`, `payer_portal`, `document_repository` | `ehr_access`, `scheduling_access`, `payer_portals`, `care_team_approvals` |

### operations -> OpsxFactory

| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |
| --- | --- | --- | --- |
| `identity_admin.m365` | `microsoft_365_admin`, `exchange_admin`, `entra_directory_admin` | `microsoft_365`, `entra_id`, `exchange_online` | `admin_consent`, `delegated_oauth`, `tenant_id`, `audit_log` |
| `exchange.mailbox_migration` | `exchange_admin`, `microsoft_365_admin`, `document_repository_read` | `exchange_online`, `microsoft_365`, `migration_tool` | `exchange_admin_consent`, `migration_endpoint`, `maintenance_window`, `audit_log` |
| `endpoint.intune` | `intune_admin`, `entra_directory_admin`, `microsoft_365_admin` | `intune`, `entra_id`, `endpoint_management` | `intune_consent`, `device_groups`, `rollout_rings`, `emergency_stop` |
| `cloud_ops.azure` | `azure_read`, `azure_operator`, `backup_operator` | `azure`, `backup_platform`, `observability` | `workload_identity`, `subscription_access`, `backup_access`, `audit_log` |
| `cloud_ops.aws` | `aws_read`, `aws_operator`, `backup_operator` | `aws`, `backup_platform`, `observability` | `iam_role`, `account_access`, `cloudtrail`, `backup_access` |
| `dns.domain_ops` | `dns_admin`, `certificate_authority_access`, `document_repository_read` | `dns_provider`, `certificate_authority`, `monitoring` | `dns_api_access`, `zone_refs`, `certificate_refs`, `monitoring` |
| `backup.dr` | `backup_operator`, `cloud_read`, `document_repository_read` | `backup_platform`, `cloud_provider`, `document_repository` | `backup_platform_access`, `restore_test_env`, `audit_log`, `approval_path` |
| `network.firewall` | `network_device_admin`, `monitoring_read`, `document_repository_read` | `firewall`, `network_device`, `monitoring`, `ticketing` | `device_access`, `monitoring_access`, `change_window`, `rollback_path` |
| `devops.github_org` | `github_org_admin`, `repo_read`, `branch_write` | `github`, `ci_cd`, `ticketing` | `github_app_install`, `org_permissions`, `repo_list`, `audit_log` |
| `security.incident_response` | `siem_read`, `endpoint_read`, `cloud_read` | `siem`, `edr`, `cloud_provider`, `ticketing` | `siem_access`, `edr_access`, `incident_channel`, `evidence_store` |

### accounting -> LedgerxFactory

| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |
| --- | --- | --- | --- |
| `bookkeeping.small_business` | `accounting_system_read`, `bank_feed_read`, `document_store_read` | `quickbooks`, `xero`, `bank_feed`, `document_store` | `accounting_system_access`, `bank_feed_access`, `client_approvers`, `audit_trail` |
| `bookkeeping.property_management` | `property_management_system_read`, `bank_feed_read`, `document_store_read` | `property_management_system`, `accounting_system`, `bank_feed` | `property_system_access`, `accounting_access`, `owner_approvers`, `audit_trail` |
| `tax.individual` | `tax_portal_access`, `document_store_read`, `accounting_system_read` | `tax_portal`, `document_store`, `tax_software` | `tax_portal_access`, `document_store`, `preparer_approver`, `audit_trail` |
| `tax.business` | `tax_portal_access`, `document_store_read`, `accounting_system_read` | `tax_portal`, `document_store`, `accounting_system`, `tax_software` | `tax_portal_access`, `accounting_access`, `signer_approval`, `audit_trail` |
| `audit.support` | `document_store_read`, `accounting_system_read`, `erp_read` | `document_store`, `accounting_system`, `erp`, `audit_platform` | `evidence_repository`, `erp_access`, `audit_approvers`, `retention_rules` |
| `month_end.close` | `accounting_system_read`, `erp_read`, `document_store_read` | `erp`, `accounting_system`, `document_store`, `spreadsheet` | `erp_access`, `close_calendar`, `controller_approver`, `audit_trail` |
| `payroll.ops` | `payroll_system_read`, `document_store_read`, `tax_portal_access` | `payroll_system`, `document_store`, `tax_portal` | `payroll_system_access`, `employee_data_controls`, `approver_roles`, `audit_trail` |
| `accounts_payable.ops` | `ap_system_read`, `document_store_read`, `vendor_master_read` | `ap_system`, `erp`, `document_store`, `payment_platform` | `ap_system_access`, `approval_matrix`, `vendor_master`, `audit_trail` |
| `accounts_receivable.ops` | `ar_system_read`, `document_store_read`, `customer_messaging_send` | `ar_system`, `erp`, `document_store`, `customer_messaging` | `ar_system_access`, `messaging_access`, `finance_approvers`, `audit_trail` |
| `controller.finance_ops` | `erp_read`, `accounting_system_read`, `document_store_read` | `erp`, `accounting_system`, `bi_platform`, `document_store` | `erp_access`, `reporting_sources`, `controller_approver`, `retention_rules` |

### marketing -> AdxFactory

| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |
| --- | --- | --- | --- |
| `campaign_ops.paid_media` | `ad_account_read`, `ad_account_write`, `analytics_read` | `google_ads`, `meta_ads`, `linkedin_ads`, `analytics` | `ad_account_connection`, `analytics_access`, `spend_approvers`, `brand_policy` |
| `lifecycle.email` | `crm_read`, `email_send`, `analytics_read` | `crm`, `email_platform`, `analytics`, `consent_platform` | `crm_access`, `email_platform_access`, `consent_source`, `send_approvers` |
| `brand.claims` | `creative_asset_read`, `cms_write`, `legal_source_read` | `creative_asset_store`, `cms`, `legal_source`, `document_repository` | `asset_store_access`, `cms_access`, `legal_sources`, `brand_approvers` |
| `content.seo` | `cms_write`, `analytics_read`, `search_console_read` | `cms`, `analytics`, `search_console`, `keyword_tool` | `cms_access`, `search_console_access`, `analytics_access`, `publish_approvers` |
| `social.community` | `social_read`, `social_publish`, `creative_asset_read` | `social_platform`, `community_platform`, `creative_asset_store` | `social_account_access`, `moderation_policy`, `publish_approvers`, `escalation_channel` |
| `product_marketing.launch` | `document_store_read`, `cms_write`, `analytics_read` | `document_store`, `cms`, `analytics`, `project_management` | `source_docs`, `cms_access`, `launch_approvers`, `analytics_access` |
| `analytics.attribution` | `analytics_read`, `ad_account_read`, `crm_read` | `analytics`, `ad_platform`, `crm`, `bi_platform` | `analytics_access`, `ad_account_access`, `crm_access`, `report_approvers` |
| `ecommerce.growth` | `ecommerce_platform_read`, `cms_write`, `analytics_read` | `ecommerce_platform`, `cms`, `analytics`, `email_platform` | `storefront_access`, `cms_access`, `analytics_access`, `promotion_approvers` |
| `partner.channel` | `partner_portal_read`, `document_store_read`, `cms_write` | `partner_portal`, `document_store`, `cms`, `crm` | `partner_portal_access`, `asset_store`, `approval_matrix`, `cms_access` |
| `pr.communications` | `document_store_read`, `cms_write`, `media_list_read` | `document_store`, `cms`, `media_database`, `pr_platform` | `source_docs`, `cms_access`, `legal_approvers`, `media_database` |

### software -> codexFactory

| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |
| --- | --- | --- | --- |
| `product_engineering.repo_delivery` | `repo_read`, `branch_write`, `pr_write` | `github`, `gitlab`, `ci_cd`, `issue_tracker` | `repo_access`, `branch_protection`, `ci_access`, `review_approvers` |
| `release_ops.cicd` | `ci_read`, `deployment_operator`, `cloud_read` | `ci_cd`, `cloud_provider`, `package_registry`, `observability` | `ci_access`, `deployment_identity`, `cloud_read`, `release_approvers` |
| `incident_response.software` | `observability_read`, `repo_read`, `deployment_operator` | `observability`, `github`, `ci_cd`, `incident_management` | `observability_access`, `incident_channel`, `repo_access`, `deployment_authority` |
| `security.appsec` | `repo_read`, `security_scanner_read`, `issue_tracker_write` | `github`, `security_scanner`, `issue_tracker`, `ci_cd` | `scanner_access`, `repo_access`, `issue_tracker_access`, `security_approvers` |
| `data_engineering.pipelines` | `repo_read`, `data_catalog_read`, `pipeline_operator` | `data_catalog`, `orchestrator`, `warehouse`, `repo` | `catalog_access`, `orchestrator_access`, `warehouse_read`, `data_approvers` |
| `mlops.model_delivery` | `model_registry_read`, `ci_read`, `deployment_operator` | `model_registry`, `ci_cd`, `observability`, `feature_store` | `model_registry_access`, `ci_access`, `monitoring_access`, `deployment_approvers` |
| `platform_engineering.internal_tools` | `repo_read`, `cloud_read`, `deployment_operator` | `github`, `cloud_provider`, `ci_cd`, `service_catalog` | `repo_access`, `service_catalog`, `cloud_read`, `rollout_approvers` |
| `qa.test_automation` | `repo_read`, `ci_read`, `issue_tracker_write` | `github`, `ci_cd`, `test_management`, `issue_tracker` | `repo_access`, `ci_access`, `test_results`, `qa_approvers` |
| `docs.developer_experience` | `repo_read`, `branch_write`, `cms_write` | `github`, `docs_site`, `cms`, `analytics` | `repo_access`, `docs_publish_access`, `review_approvers`, `analytics_access` |
| `product_management.requirements` | `issue_tracker_read`, `document_store_read`, `repo_read` | `issue_tracker`, `document_store`, `roadmap_tool`, `repo` | `issue_tracker_access`, `docs_access`, `stakeholder_approvers`, `repo_context` |

### law -> LegalxFactory

| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |
| --- | --- | --- | --- |
| `compliance.medical.pharmacy` | `regulation_source_read`, `policy_document_read`, `evidence_repository_read` | `legal_research`, `compliance_management_system`, `policy_repository`, `evidence_repository` | `legal_sources`, `policy_docs`, `evidence_repository`, `professional_approvers` |
| `compliance.medical.clinic` | `policy_document_read`, `evidence_repository_read`, `compliance_system_read` | `legal_research`, `policy_repository`, `compliance_management_system`, `evidence_repository` | `policy_docs`, `evidence_repository`, `compliance_system`, `attorney_or_consultant_approvers` |
| `compliance.privacy.healthcare` | `policy_document_read`, `evidence_repository_read`, `incident_record_read` | `legal_research`, `incident_management`, `policy_repository`, `evidence_repository` | `incident_records`, `policy_docs`, `evidence_store`, `counsel_approvers` |
| `compliance.employment.payroll` | `regulation_source_read`, `policy_document_read`, `payroll_record_read` | `legal_research`, `payroll_system`, `policy_repository`, `document_repository` | `legal_sources`, `payroll_record_refs`, `policy_docs`, `counsel_approvers` |
| `compliance.finance.broker_dealer` | `regulation_source_read`, `policy_document_read`, `evidence_repository_read` | `legal_research`, `compliance_management_system`, `policy_repository`, `evidence_repository` | `regulatory_sources`, `policy_docs`, `evidence_repository`, `compliance_approvers` |
| `contract_review.saas.vendor` | `document_store_read`, `contract_repository_read`, `redline_workspace_write` | `contract_lifecycle_management`, `document_repository`, `redline_workspace` | `contract_repository`, `playbook_docs`, `redline_workspace`, `attorney_approvers` |
| `contract_review.healthcare.vendor` | `document_store_read`, `contract_repository_read`, `regulation_source_read` | `contract_lifecycle_management`, `legal_research`, `document_repository` | `contract_repository`, `regulatory_sources`, `privacy_playbook`, `attorney_approvers` |
| `legal_ops.matter_management` | `matter_management_read`, `document_store_read`, `calendar_read` | `matter_management`, `document_repository`, `calendar`, `email` | `matter_system_access`, `calendar_access`, `document_store`, `privilege_boundaries` |
| `litigation.discovery` | `document_store_read`, `ediscovery_platform_read`, `privilege_log_write` | `ediscovery_platform`, `document_repository`, `matter_management` | `ediscovery_access`, `document_store`, `privilege_reviewers`, `deadline_calendar` |
| `policy.governance` | `policy_document_read`, `evidence_repository_read`, `approval_system_write` | `policy_repository`, `compliance_management_system`, `approval_system` | `policy_repository`, `approval_system`, `control_sources`, `governance_approvers` |

### insurance -> InsurexFactory

| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |
| --- | --- | --- | --- |
| `claims.property_casualty` | `policy_admin_read`, `claims_system_read`, `document_repository_read` | `claims_system`, `policy_admin`, `document_repository` | `claims_access`, `policy_admin_access`, `evidence_repository`, `claim_approvers` |
| `claims.health` | `claims_system_read`, `policy_admin_read`, `provider_portal_read` | `claims_system`, `payer_system`, `provider_portal`, `document_repository` | `claims_access`, `member_privacy_controls`, `provider_sources`, `reviewer_approvers` |
| `claims.workers_comp` | `claims_system_read`, `document_repository_read`, `medical_record_read` | `claims_system`, `document_repository`, `medical_record_source` | `claims_access`, `medical_record_sources`, `jurisdiction_rules`, `adjuster_approvers` |
| `underwriting.commercial` | `underwriting_system_read`, `document_repository_read`, `rating_system_read` | `underwriting_system`, `rating_system`, `document_repository` | `underwriting_system_access`, `rating_system`, `guideline_sources`, `underwriter_approvers` |
| `underwriting.personal_lines` | `underwriting_system_read`, `rating_system_read`, `document_repository_read` | `underwriting_system`, `rating_system`, `document_repository` | `underwriting_access`, `rating_access`, `eligibility_rules`, `approval_roles` |
| `policy_ops.brokerage` | `agency_management_read`, `carrier_portal_read`, `document_repository_read` | `agency_management`, `carrier_portal`, `document_repository` | `agency_management_access`, `carrier_portals`, `producer_approvers`, `document_store` |
| `actuarial.pricing` | `data_warehouse_read`, `model_repository_read`, `document_repository_read` | `data_warehouse`, `model_repository`, `document_repository` | `data_access`, `model_repository`, `actuarial_reviewers`, `audit_trail` |
| `insurance.compliance` | `regulation_source_read`, `policy_document_read`, `evidence_repository_read` | `legal_research`, `compliance_management_system`, `policy_repository` | `regulatory_sources`, `policy_docs`, `evidence_repository`, `compliance_approvers` |
| `subrogation.recovery` | `claims_system_read`, `document_repository_read`, `customer_messaging_send` | `claims_system`, `document_repository`, `messaging_platform` | `claims_access`, `document_store`, `messaging_approval`, `counsel_approvers` |
| `risk_engineering.loss_control` | `inspection_system_read`, `document_repository_read`, `customer_messaging_send` | `inspection_system`, `document_repository`, `customer_messaging` | `inspection_system`, `document_store`, `insured_messaging`, `underwriter_approvers` |

### manufacturing -> MakexFactory

| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |
| --- | --- | --- | --- |
| `quality_ops.plant` | `qms_read`, `document_repository_read`, `erp_read` | `qms`, `erp`, `document_repository` | `qms_access`, `erp_access`, `quality_approvers`, `audit_trail` |
| `maintenance.asset` | `cmms_read`, `sensor_data_read`, `work_order_write` | `cmms`, `historian`, `sensor_platform` | `cmms_access`, `sensor_sources`, `work_order_permissions`, `maintenance_approvers` |
| `safety.ehs` | `ehs_system_read`, `policy_document_read`, `training_system_read` | `ehs_system`, `training_system`, `policy_repository` | `ehs_access`, `training_access`, `safety_approvers`, `regulatory_sources` |
| `production_planning.scheduling` | `erp_read`, `mes_read`, `scheduling_write` | `erp`, `mes`, `planning_system` | `erp_access`, `mes_access`, `schedule_write_permissions`, `planner_approvers` |
| `procurement.supplier_quality` | `erp_read`, `supplier_portal_read`, `qms_read` | `erp`, `supplier_portal`, `qms` | `erp_access`, `supplier_portal`, `qms_access`, `procurement_approvers` |
| `inventory.materials` | `erp_read`, `inventory_write`, `warehouse_system_read` | `erp`, `wms`, `inventory_system` | `inventory_access`, `erp_access`, `adjustment_approvers`, `audit_trail` |
| `regulatory.gmp` | `qms_read`, `document_repository_read`, `mes_read` | `qms`, `mes`, `document_repository` | `qms_access`, `batch_records`, `qa_approvers`, `audit_trail` |
| `engineering.change_control` | `plm_read`, `document_repository_read`, `erp_read` | `plm`, `document_repository`, `erp` | `plm_access`, `document_store`, `approval_matrix`, `audit_trail` |
| `field_service.equipment` | `field_service_system_read`, `inventory_read`, `customer_messaging_send` | `field_service_system`, `inventory_system`, `customer_messaging` | `field_service_access`, `inventory_access`, `messaging_access`, `service_approvers` |
| `energy.utilities_ops` | `asset_system_read`, `sensor_data_read`, `work_order_write` | `asset_management`, `historian`, `cmms` | `asset_system_access`, `historian_access`, `work_order_permissions`, `operator_approvers` |

### logistics -> FlowxFactory

| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |
| --- | --- | --- | --- |
| `freight_ops.carrier` | `tms_read`, `carrier_portal_read`, `customer_messaging_send` | `tms`, `carrier_portal`, `customer_messaging` | `tms_access`, `carrier_portals`, `messaging_approval`, `audit_trail` |
| `warehouse_ops.inventory` | `wms_read`, `inventory_write`, `erp_read` | `wms`, `erp`, `inventory_system` | `wms_access`, `inventory_write_permissions`, `erp_access`, `warehouse_approvers` |
| `supply_chain.procurement` | `erp_read`, `supplier_portal_read`, `procurement_system_write` | `erp`, `supplier_portal`, `procurement_system` | `erp_access`, `supplier_portal`, `procurement_system`, `approval_matrix` |
| `transportation.fleet` | `fleet_system_read`, `telematics_read`, `customer_messaging_send` | `fleet_system`, `telematics`, `tms`, `customer_messaging` | `fleet_access`, `telematics_access`, `dispatch_approvers`, `messaging_approval` |
| `cold_chain.compliance` | `tms_read`, `sensor_data_read`, `evidence_repository_read` | `tms`, `sensor_platform`, `evidence_repository` | `sensor_access`, `tms_access`, `quality_approvers`, `evidence_store` |
| `customs.trade_compliance` | `customs_system_read`, `document_repository_read`, `regulation_source_read` | `customs_system`, `document_repository`, `legal_research` | `customs_system_access`, `regulation_sources`, `broker_approvers`, `document_store` |
| `last_mile.delivery` | `delivery_platform_read`, `customer_messaging_send`, `order_system_read` | `delivery_platform`, `customer_messaging`, `order_system` | `delivery_platform_access`, `order_system`, `messaging_access`, `dispatcher_approvers` |
| `reverse_logistics.returns` | `wms_read`, `order_system_read`, `customer_messaging_send` | `wms`, `order_system`, `customer_messaging`, `vendor_portal` | `wms_access`, `order_system`, `messaging_access`, `approval_matrix` |
| `logistics.customer_service` | `tms_read`, `customer_messaging_send`, `crm_read` | `tms`, `crm`, `customer_messaging`, `ticketing` | `crm_access`, `tms_access`, `messaging_approval`, `escalation_channel` |
| `planning.demand_forecast` | `erp_read`, `inventory_read`, `analytics_read` | `erp`, `inventory_system`, `analytics`, `planning_system` | `planning_system_access`, `erp_access`, `inventory_access`, `planner_approvers` |

### retail -> CommerxFactory

| Subtype | Credential bindings to collect | Adapter endpoints to collect | Runtime focus |
| --- | --- | --- | --- |
| `ecommerce_ops.marketplace` | `ecommerce_platform_read`, `marketplace_read`, `support_system_write` | `ecommerce_platform`, `marketplace`, `support_system` | `marketplace_access`, `ecommerce_access`, `support_system`, `approval_matrix` |
| `customer_ops.returns` | `order_system_read`, `support_system_write`, `payment_system_read` | `order_system`, `support_system`, `payment_system` | `order_system_access`, `payment_read_access`, `support_write_access`, `refund_approvers` |
| `merchandising.pricing` | `product_catalog_read`, `pricing_write`, `inventory_read` | `product_catalog`, `pricing_system`, `inventory_system` | `catalog_access`, `pricing_write_permissions`, `inventory_access`, `merchant_approvers` |
| `inventory.replenishment` | `inventory_read`, `erp_read`, `supplier_portal_read` | `inventory_system`, `erp`, `supplier_portal` | `inventory_access`, `erp_access`, `supplier_portal`, `replenishment_approvers` |
| `store_ops.physical` | `store_system_read`, `workforce_system_read`, `support_system_write` | `store_system`, `workforce_system`, `ticketing` | `store_system_access`, `workforce_access`, `escalation_channel`, `store_approvers` |
| `loyalty.crm` | `crm_read`, `customer_messaging_send`, `analytics_read` | `crm`, `loyalty_platform`, `customer_messaging`, `analytics` | `crm_access`, `consent_source`, `messaging_access`, `offer_approvers` |
| `fraud.chargebacks` | `payment_system_read`, `order_system_read`, `document_repository_read` | `payment_system`, `order_system`, `document_repository` | `payment_access`, `order_access`, `evidence_store`, `dispute_approvers` |
| `product_content.catalog` | `product_catalog_read`, `cms_write`, `creative_asset_read` | `product_catalog`, `cms`, `creative_asset_store` | `catalog_access`, `cms_access`, `asset_store`, `publish_approvers` |
| `retail.analytics` | `analytics_read`, `ecommerce_platform_read`, `inventory_read` | `analytics`, `ecommerce_platform`, `inventory_system`, `bi_platform` | `analytics_access`, `commerce_access`, `inventory_access`, `report_approvers` |
| `subscription.commerce` | `subscription_platform_read`, `payment_system_read`, `customer_messaging_send` | `subscription_platform`, `payment_system`, `customer_messaging`, `crm` | `subscription_access`, `payment_read_access`, `messaging_access`, `billing_approvers` |
