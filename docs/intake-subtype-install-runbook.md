# Intake Subtype Install Runbook

Status: generated runbook
Repository context: openxFactory

## Purpose

Use this runbook to turn each subtype from intake-template data into an
installable xFactory candidate. It fixes generic scaffold and domain-artifact
gaps. It does not invent customer-specific runtime bindings, credentials,
adapter endpoints, approvals, validation evidence, or live execution approval.

## Standard Fix Flow

1. Create the factory repo if it is missing.
2. Apply the openxFactory domain starter.
3. Generate one profile file for the subtype.
4. Generate workflow specs for the subtype starter workflows.
5. Generate credential requirement stubs for every credential family.
6. Generate adapter contract stubs for every adapter family.
7. Generate or extend Hermes agent mix profiles.
8. Generate a runtime binding manifest template.
9. Run static validation.
10. Hand off to runtime binding for deployment target, vault refs, adapter endpoints, approvers, validation, and dry-run.

## Per-Subtype Fix Matrix

### medical -> MedxFactory

| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |
| --- | --- | --- | --- | --- |
| `clinical_operations.clinic` | `profiles/clinical_operations.clinic.yaml` | `intake_summary`, `referral_management`, `patient_follow_up` | `ehr_patient_read`, `scheduling_write`, `patient_messaging_send` | `ehr`, `practice_management`, `scheduling`, `patient_messaging` |
| `clinical_operations.group_practice` | `profiles/clinical_operations.group_practice.yaml` | `care_gap_review`, `referral_management`, `provider_panel_follow_up` | `ehr_patient_read`, `care_team_roster_read`, `scheduling_write` | `ehr`, `provider_directory`, `scheduling`, `document_repository` |
| `clinical_operations.hospital` | `profiles/clinical_operations.hospital.yaml` | `discharge_follow_up`, `care_transition_review`, `referral_management` | `ehr_patient_read`, `care_team_roster_read`, `scheduling_write` | `ehr`, `care_team_roster`, `scheduling`, `document_repository` |
| `clinical_operations.pharmacy` | `profiles/clinical_operations.pharmacy.yaml` | `pharmacy_reconciliation`, `refill_follow_up`, `medication_access_review` | `pharmacy_system_read`, `patient_messaging_send`, `payer_portal_read` | `pharmacy_system`, `payer_portal`, `patient_messaging`, `document_repository` |
| `clinical_operations.imaging_center` | `profiles/clinical_operations.imaging_center.yaml` | `order_intake`, `diagnostic_result_packet`, `referring_provider_follow_up` | `imaging_system_read`, `referral_document_read`, `provider_messaging_send` | `imaging_system`, `referral_document_store`, `provider_messaging`, `scheduling` |
| `clinical_operations.telehealth` | `profiles/clinical_operations.telehealth.yaml` | `visit_intake`, `follow_up_packet`, `escalation_review` | `ehr_patient_read`, `scheduling_write`, `patient_messaging_send` | `ehr`, `telehealth_platform`, `scheduling`, `patient_messaging` |
| `clinical_operations.lab` | `profiles/clinical_operations.lab.yaml` | `lab_order_intake`, `abnormal_result_packet`, `provider_follow_up` | `lab_system_read`, `referral_document_read`, `provider_messaging_send` | `lis`, `ehr`, `provider_messaging`, `document_repository` |
| `clinical_operations.behavioral_health` | `profiles/clinical_operations.behavioral_health.yaml` | `intake_summary`, `follow_up_packet`, `risk_escalation_review` | `ehr_patient_read`, `scheduling_write`, `patient_messaging_send` | `ehr`, `scheduling`, `patient_messaging`, `document_repository` |
| `clinical_operations.dental` | `profiles/clinical_operations.dental.yaml` | `patient_intake`, `treatment_plan_packet`, `insurance_follow_up` | `practice_management_read`, `scheduling_write`, `patient_messaging_send` | `dental_practice_management`, `scheduling`, `payer_portal`, `patient_messaging` |
| `clinical_operations.home_health` | `profiles/clinical_operations.home_health.yaml` | `care_visit_review`, `authorization_follow_up`, `care_plan_update_packet` | `ehr_patient_read`, `scheduling_write`, `payer_portal_read` | `ehr`, `scheduling`, `payer_portal`, `document_repository` |

### operations -> OpsxFactory

| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |
| --- | --- | --- | --- | --- |
| `identity_admin.m365` | `profiles/identity_admin.m365.yaml` | `user_lifecycle`, `mailbox_migration`, `conditional_access_review` | `microsoft_365_admin` | `microsoft_365`, `entra_id`, `exchange_online` |
| `exchange.mailbox_migration` | `profiles/exchange.mailbox_migration.yaml` | `mailbox_inventory`, `migration_batch_plan`, `migration_status_review` | `microsoft_365_admin`, `document_repository_read` | `exchange_online`, `microsoft_365`, `migration_tool` |
| `endpoint.intune` | `profiles/endpoint.intune.yaml` | `device_inventory_review`, `compliance_policy_review`, `app_deployment_plan` | `intune_admin`, `microsoft_365_admin` | `intune`, `entra_id`, `endpoint_management` |
| `cloud_ops.azure` | `profiles/cloud_ops.azure.yaml` | `subscription_review`, `infrastructure_change`, `backup_restore` | `azure_read`, `azure_operator` | `azure`, `backup_platform`, `observability` |
| `cloud_ops.aws` | `profiles/cloud_ops.aws.yaml` | `account_review`, `infrastructure_change`, `incident_packet` | `aws_read`, `aws_operator` | `aws`, `backup_platform`, `observability` |
| `dns.domain_ops` | `profiles/dns.domain_ops.yaml` | `dns_record_update`, `domain_cutover`, `certificate_renewal` | `certificate_authority_access`, `document_repository_read` | `dns_provider`, `certificate_authority`, `monitoring` |
| `backup.dr` | `profiles/backup.dr.yaml` | `backup_inventory`, `restore_test_plan`, `recovery_readiness_review` | `cloud_read`, `document_repository_read` | `backup_platform`, `cloud_provider`, `document_repository` |
| `network.firewall` | `profiles/network.firewall.yaml` | `rule_review`, `change_plan`, `post_change_validation` | `network_device_admin`, `monitoring_read`, `document_repository_read` | `firewall`, `network_device`, `monitoring`, `ticketing` |
| `devops.github_org` | `profiles/devops.github_org.yaml` | `org_access_review`, `branch_protection_review`, `repo_settings_update` | `repo_read`, `branch_write` | `github`, `ci_cd`, `ticketing` |
| `security.incident_response` | `profiles/security.incident_response.yaml` | `incident_intake`, `containment_plan`, `post_incident_review` | `siem_read`, `endpoint_read`, `cloud_read` | `siem`, `edr`, `cloud_provider`, `ticketing` |

### accounting -> LedgerxFactory

| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |
| --- | --- | --- | --- | --- |
| `bookkeeping.small_business` | `profiles/bookkeeping.small_business.yaml` | `client_intake`, `bank_feed_review`, `reconciliation` | `accounting_system_read`, `bank_feed_read`, `document_store_read` | `quickbooks`, `xero`, `bank_feed`, `document_store` |
| `bookkeeping.property_management` | `profiles/bookkeeping.property_management.yaml` | `rent_roll_review`, `owner_statement_packet`, `reconciliation` | `property_management_system_read`, `bank_feed_read`, `document_store_read` | `property_management_system`, `accounting_system`, `bank_feed` |
| `tax.individual` | `profiles/tax.individual.yaml` | `tax_document_intake`, `organizer_review`, `filing_packet` | `tax_portal_access`, `document_store_read`, `accounting_system_read` | `tax_portal`, `document_store`, `tax_software` |
| `tax.business` | `profiles/tax.business.yaml` | `tax_packet_preparation`, `filing_review`, `notice_response_packet` | `tax_portal_access`, `document_store_read`, `accounting_system_read` | `tax_portal`, `document_store`, `accounting_system`, `tax_software` |
| `audit.support` | `profiles/audit.support.yaml` | `audit_evidence_request`, `control_evidence_packet`, `exception_response` | `document_store_read`, `accounting_system_read`, `erp_read` | `document_store`, `accounting_system`, `erp`, `audit_platform` |
| `month_end.close` | `profiles/month_end.close.yaml` | `close_checklist_review`, `accrual_packet`, `variance_review` | `accounting_system_read`, `erp_read`, `document_store_read` | `erp`, `accounting_system`, `document_store`, `spreadsheet` |
| `payroll.ops` | `profiles/payroll.ops.yaml` | `payroll_precheck`, `exception_review`, `payroll_approval_packet` | `payroll_system_read`, `document_store_read`, `tax_portal_access` | `payroll_system`, `document_store`, `tax_portal` |
| `accounts_payable.ops` | `profiles/accounts_payable.ops.yaml` | `invoice_intake`, `approval_match_review`, `payment_packet` | `ap_system_read`, `document_store_read`, `vendor_master_read` | `ap_system`, `erp`, `document_store`, `payment_platform` |
| `accounts_receivable.ops` | `profiles/accounts_receivable.ops.yaml` | `ar_aging_review`, `collection_follow_up_packet`, `cash_application_review` | `ar_system_read`, `document_store_read`, `customer_messaging_send` | `ar_system`, `erp`, `document_store`, `customer_messaging` |
| `controller.finance_ops` | `profiles/controller.finance_ops.yaml` | `management_report_packet`, `budget_variance_review`, `board_packet_support` | `erp_read`, `accounting_system_read`, `document_store_read` | `erp`, `accounting_system`, `bi_platform`, `document_store` |

### marketing -> AdxFactory

| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |
| --- | --- | --- | --- | --- |
| `campaign_ops.paid_media` | `profiles/campaign_ops.paid_media.yaml` | `campaign_intake`, `creative_review`, `budget_adjustment` | `ad_account_read`, `ad_account_write`, `analytics_read` | `google_ads`, `meta_ads`, `linkedin_ads`, `analytics` |
| `lifecycle.email` | `profiles/lifecycle.email.yaml` | `segment_review`, `email_send_review`, `attribution_review` | `crm_read`, `email_send`, `analytics_read` | `crm`, `email_platform`, `analytics`, `consent_platform` |
| `brand.claims` | `profiles/brand.claims.yaml` | `claim_review`, `landing_page_review`, `campaign_launch_readiness` | `creative_asset_read`, `cms_write`, `legal_source_read` | `creative_asset_store`, `cms`, `legal_source`, `document_repository` |
| `content.seo` | `profiles/content.seo.yaml` | `content_brief`, `seo_review`, `publish_readiness` | `cms_write`, `analytics_read`, `search_console_read` | `cms`, `analytics`, `search_console`, `keyword_tool` |
| `social.community` | `profiles/social.community.yaml` | `post_review`, `response_draft`, `escalation_packet` | `social_read`, `social_publish`, `creative_asset_read` | `social_platform`, `community_platform`, `creative_asset_store` |
| `product_marketing.launch` | `profiles/product_marketing.launch.yaml` | `launch_intake`, `positioning_review`, `launch_readiness` | `document_store_read`, `cms_write`, `analytics_read` | `document_store`, `cms`, `analytics`, `project_management` |
| `analytics.attribution` | `profiles/analytics.attribution.yaml` | `tracking_audit`, `attribution_review`, `performance_report` | `analytics_read`, `ad_account_read`, `crm_read` | `analytics`, `ad_platform`, `crm`, `bi_platform` |
| `ecommerce.growth` | `profiles/ecommerce.growth.yaml` | `offer_review`, `promo_launch_review`, `conversion_analysis` | `ecommerce_platform_read`, `cms_write`, `analytics_read` | `ecommerce_platform`, `cms`, `analytics`, `email_platform` |
| `partner.channel` | `profiles/partner.channel.yaml` | `partner_campaign_intake`, `co_marketing_review`, `enablement_packet` | `partner_portal_read`, `document_store_read`, `cms_write` | `partner_portal`, `document_store`, `cms`, `crm` |
| `pr.communications` | `profiles/pr.communications.yaml` | `message_intake`, `statement_review`, `media_response_packet` | `document_store_read`, `cms_write`, `media_list_read` | `document_store`, `cms`, `media_database`, `pr_platform` |

### software -> codexFactory

| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |
| --- | --- | --- | --- | --- |
| `product_engineering.repo_delivery` | `profiles/product_engineering.repo_delivery.yaml` | `approved_intent_intake`, `feature_decomposition`, `pr_admission` | `repo_read`, `branch_write`, `pr_write` | `github`, `gitlab`, `ci_cd`, `issue_tracker` |
| `release_ops.cicd` | `profiles/release_ops.cicd.yaml` | `release_readiness`, `deployment_review`, `rollback_plan_review` | `ci_read`, `deployment_operator`, `cloud_read` | `ci_cd`, `cloud_provider`, `package_registry`, `observability` |
| `incident_response.software` | `profiles/incident_response.software.yaml` | `incident_intake`, `root_cause_packet`, `remediation_review` | `observability_read`, `repo_read`, `deployment_operator` | `observability`, `github`, `ci_cd`, `incident_management` |
| `security.appsec` | `profiles/security.appsec.yaml` | `finding_triage`, `secure_fix_plan`, `security_review_packet` | `repo_read`, `security_scanner_read`, `issue_tracker_write` | `github`, `security_scanner`, `issue_tracker`, `ci_cd` |
| `data_engineering.pipelines` | `profiles/data_engineering.pipelines.yaml` | `pipeline_intake`, `data_quality_review`, `pipeline_change_packet` | `repo_read`, `data_catalog_read`, `pipeline_operator` | `data_catalog`, `orchestrator`, `warehouse`, `repo` |
| `mlops.model_delivery` | `profiles/mlops.model_delivery.yaml` | `model_eval_packet`, `deployment_readiness`, `monitoring_review` | `model_registry_read`, `ci_read`, `deployment_operator` | `model_registry`, `ci_cd`, `observability`, `feature_store` |
| `platform_engineering.internal_tools` | `profiles/platform_engineering.internal_tools.yaml` | `platform_request_intake`, `tool_change_review`, `rollout_readiness` | `repo_read`, `cloud_read`, `deployment_operator` | `github`, `cloud_provider`, `ci_cd`, `service_catalog` |
| `qa.test_automation` | `profiles/qa.test_automation.yaml` | `test_gap_review`, `test_plan_packet`, `release_quality_review` | `repo_read`, `ci_read`, `issue_tracker_write` | `github`, `ci_cd`, `test_management`, `issue_tracker` |
| `docs.developer_experience` | `profiles/docs.developer_experience.yaml` | `docs_gap_review`, `api_doc_update`, `onboarding_packet` | `repo_read`, `branch_write`, `cms_write` | `github`, `docs_site`, `cms`, `analytics` |
| `product_management.requirements` | `profiles/product_management.requirements.yaml` | `intent_intake`, `requirement_clarification`, `acceptance_criteria_packet` | `issue_tracker_read`, `document_store_read`, `repo_read` | `issue_tracker`, `document_store`, `roadmap_tool`, `repo` |

### law -> LegalxFactory

| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |
| --- | --- | --- | --- | --- |
| `compliance.medical.pharmacy` | `profiles/compliance.medical.pharmacy.yaml` | `compliance_intake`, `regulation_mapping`, `remediation_plan_review` | `regulation_source_read`, `policy_document_read`, `evidence_repository_read` | `legal_research`, `compliance_management_system`, `policy_repository`, `evidence_repository` |
| `compliance.medical.clinic` | `profiles/compliance.medical.clinic.yaml` | `policy_gap_review`, `evidence_request_packet`, `corrective_action_plan` | `policy_document_read`, `evidence_repository_read`, `compliance_system_read` | `legal_research`, `policy_repository`, `compliance_management_system`, `evidence_repository` |
| `compliance.privacy.healthcare` | `profiles/compliance.privacy.healthcare.yaml` | `privacy_assessment`, `incident_review_packet`, `policy_update_review` | `policy_document_read`, `evidence_repository_read`, `incident_record_read` | `legal_research`, `incident_management`, `policy_repository`, `evidence_repository` |
| `compliance.employment.payroll` | `profiles/compliance.employment.payroll.yaml` | `payroll_policy_review`, `wage_hour_gap_packet`, `remediation_plan_review` | `regulation_source_read`, `policy_document_read`, `payroll_record_read` | `legal_research`, `payroll_system`, `policy_repository`, `document_repository` |
| `compliance.finance.broker_dealer` | `profiles/compliance.finance.broker_dealer.yaml` | `rule_mapping`, `supervisory_policy_review`, `exam_response_packet` | `regulation_source_read`, `policy_document_read`, `evidence_repository_read` | `legal_research`, `compliance_management_system`, `policy_repository`, `evidence_repository` |
| `contract_review.saas.vendor` | `profiles/contract_review.saas.vendor.yaml` | `contract_intake`, `clause_review`, `redline_packet` | `document_store_read`, `contract_repository_read`, `redline_workspace_write` | `contract_lifecycle_management`, `document_repository`, `redline_workspace` |
| `contract_review.healthcare.vendor` | `profiles/contract_review.healthcare.vendor.yaml` | `contract_intake`, `compliance_clause_review`, `redline_packet` | `document_store_read`, `contract_repository_read`, `regulation_source_read` | `contract_lifecycle_management`, `legal_research`, `document_repository` |
| `legal_ops.matter_management` | `profiles/legal_ops.matter_management.yaml` | `matter_intake`, `deadline_review`, `status_packet` | `matter_management_read`, `document_store_read`, `calendar_read` | `matter_management`, `document_repository`, `calendar`, `email` |
| `litigation.discovery` | `profiles/litigation.discovery.yaml` | `discovery_request_intake`, `evidence_index_packet`, `privilege_review_packet` | `document_store_read`, `ediscovery_platform_read`, `privilege_log_write` | `ediscovery_platform`, `document_repository`, `matter_management` |
| `policy.governance` | `profiles/policy.governance.yaml` | `policy_intake`, `policy_gap_review`, `approval_packet` | `policy_document_read`, `evidence_repository_read`, `approval_system_write` | `policy_repository`, `compliance_management_system`, `approval_system` |

### insurance -> InsurexFactory

| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |
| --- | --- | --- | --- | --- |
| `claims.property_casualty` | `profiles/claims.property_casualty.yaml` | `claim_intake`, `evidence_packet`, `coverage_review_packet` | `policy_admin_read`, `claims_system_read`, `document_repository_read` | `claims_system`, `policy_admin`, `document_repository` |
| `claims.health` | `profiles/claims.health.yaml` | `claim_intake`, `medical_necessity_packet`, `denial_review_packet` | `claims_system_read`, `policy_admin_read`, `provider_portal_read` | `claims_system`, `payer_system`, `provider_portal`, `document_repository` |
| `claims.workers_comp` | `profiles/claims.workers_comp.yaml` | `claim_intake`, `medical_record_packet`, `return_to_work_review` | `claims_system_read`, `document_repository_read`, `medical_record_read` | `claims_system`, `document_repository`, `medical_record_source` |
| `underwriting.commercial` | `profiles/underwriting.commercial.yaml` | `submission_intake`, `risk_evidence_review`, `quote_readiness_packet` | `underwriting_system_read`, `document_repository_read`, `rating_system_read` | `underwriting_system`, `rating_system`, `document_repository` |
| `underwriting.personal_lines` | `profiles/underwriting.personal_lines.yaml` | `application_intake`, `risk_factor_review`, `quote_readiness_packet` | `underwriting_system_read`, `rating_system_read`, `document_repository_read` | `underwriting_system`, `rating_system`, `document_repository` |
| `policy_ops.brokerage` | `profiles/policy_ops.brokerage.yaml` | `renewal_review`, `certificate_request`, `policy_change_packet` | `agency_management_read`, `carrier_portal_read`, `document_repository_read` | `agency_management`, `carrier_portal`, `document_repository` |
| `actuarial.pricing` | `profiles/actuarial.pricing.yaml` | `data_intake_review`, `assumption_packet`, `pricing_review_packet` | `data_warehouse_read`, `model_repository_read`, `document_repository_read` | `data_warehouse`, `model_repository`, `document_repository` |
| `insurance.compliance` | `profiles/insurance.compliance.yaml` | `rule_mapping`, `filing_readiness_packet`, `audit_response` | `regulation_source_read`, `policy_document_read`, `evidence_repository_read` | `legal_research`, `compliance_management_system`, `policy_repository` |
| `subrogation.recovery` | `profiles/subrogation.recovery.yaml` | `recovery_opportunity_review`, `demand_packet`, `follow_up_review` | `claims_system_read`, `document_repository_read`, `customer_messaging_send` | `claims_system`, `document_repository`, `messaging_platform` |
| `risk_engineering.loss_control` | `profiles/risk_engineering.loss_control.yaml` | `inspection_packet`, `recommendation_review`, `follow_up_packet` | `inspection_system_read`, `document_repository_read`, `customer_messaging_send` | `inspection_system`, `document_repository`, `customer_messaging` |

### manufacturing -> MakexFactory

| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |
| --- | --- | --- | --- | --- |
| `quality_ops.plant` | `profiles/quality_ops.plant.yaml` | `nonconformance_intake`, `root_cause_packet`, `corrective_action_review` | `qms_read`, `document_repository_read`, `erp_read` | `qms`, `erp`, `document_repository` |
| `maintenance.asset` | `profiles/maintenance.asset.yaml` | `work_order_triage`, `preventive_maintenance_review`, `downtime_root_cause_packet` | `cmms_read`, `sensor_data_read`, `work_order_write` | `cmms`, `historian`, `sensor_platform` |
| `safety.ehs` | `profiles/safety.ehs.yaml` | `safety_incident_packet`, `hazard_review`, `training_gap_review` | `ehs_system_read`, `policy_document_read`, `training_system_read` | `ehs_system`, `training_system`, `policy_repository` |
| `production_planning.scheduling` | `profiles/production_planning.scheduling.yaml` | `schedule_review`, `constraint_packet`, `change_impact_review` | `erp_read`, `mes_read`, `scheduling_write` | `erp`, `mes`, `planning_system` |
| `procurement.supplier_quality` | `profiles/procurement.supplier_quality.yaml` | `supplier_intake`, `supplier_quality_review`, `purchase_order_packet` | `erp_read`, `supplier_portal_read`, `qms_read` | `erp`, `supplier_portal`, `qms` |
| `inventory.materials` | `profiles/inventory.materials.yaml` | `inventory_exception_review`, `shortage_packet`, `replenishment_review` | `erp_read`, `inventory_write`, `warehouse_system_read` | `erp`, `wms`, `inventory_system` |
| `regulatory.gmp` | `profiles/regulatory.gmp.yaml` | `batch_record_review`, `deviation_packet`, `validation_readiness` | `qms_read`, `document_repository_read`, `mes_read` | `qms`, `mes`, `document_repository` |
| `engineering.change_control` | `profiles/engineering.change_control.yaml` | `change_intake`, `impact_review`, `approval_packet` | `plm_read`, `document_repository_read`, `erp_read` | `plm`, `document_repository`, `erp` |
| `field_service.equipment` | `profiles/field_service.equipment.yaml` | `service_case_intake`, `parts_review`, `service_follow_up_packet` | `field_service_system_read`, `inventory_read`, `customer_messaging_send` | `field_service_system`, `inventory_system`, `customer_messaging` |
| `energy.utilities_ops` | `profiles/energy.utilities_ops.yaml` | `asset_review`, `outage_packet`, `maintenance_plan_review` | `asset_system_read`, `sensor_data_read`, `work_order_write` | `asset_management`, `historian`, `cmms` |

### logistics -> FlowxFactory

| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |
| --- | --- | --- | --- | --- |
| `freight_ops.carrier` | `profiles/freight_ops.carrier.yaml` | `shipment_intake`, `carrier_exception_review`, `delivery_follow_up` | `tms_read`, `carrier_portal_read`, `customer_messaging_send` | `tms`, `carrier_portal`, `customer_messaging` |
| `warehouse_ops.inventory` | `profiles/warehouse_ops.inventory.yaml` | `inventory_exception_review`, `pick_pack_issue_packet`, `replenishment_review` | `wms_read`, `inventory_write`, `erp_read` | `wms`, `erp`, `inventory_system` |
| `supply_chain.procurement` | `profiles/supply_chain.procurement.yaml` | `supplier_intake`, `shortage_review`, `purchase_order_packet` | `erp_read`, `supplier_portal_read`, `procurement_system_write` | `erp`, `supplier_portal`, `procurement_system` |
| `transportation.fleet` | `profiles/transportation.fleet.yaml` | `fleet_issue_intake`, `route_exception_review`, `maintenance_follow_up` | `fleet_system_read`, `telematics_read`, `customer_messaging_send` | `fleet_system`, `telematics`, `tms`, `customer_messaging` |
| `cold_chain.compliance` | `profiles/cold_chain.compliance.yaml` | `temperature_exception_packet`, `lane_review`, `compliance_follow_up` | `tms_read`, `sensor_data_read`, `evidence_repository_read` | `tms`, `sensor_platform`, `evidence_repository` |
| `customs.trade_compliance` | `profiles/customs.trade_compliance.yaml` | `entry_intake`, `classification_review`, `documentation_packet` | `customs_system_read`, `document_repository_read`, `regulation_source_read` | `customs_system`, `document_repository`, `legal_research` |
| `last_mile.delivery` | `profiles/last_mile.delivery.yaml` | `delivery_exception_review`, `customer_update_packet`, `route_adjustment` | `delivery_platform_read`, `customer_messaging_send`, `order_system_read` | `delivery_platform`, `customer_messaging`, `order_system` |
| `reverse_logistics.returns` | `profiles/reverse_logistics.returns.yaml` | `return_intake`, `disposition_review`, `vendor_claim_packet` | `wms_read`, `order_system_read`, `customer_messaging_send` | `wms`, `order_system`, `customer_messaging`, `vendor_portal` |
| `logistics.customer_service` | `profiles/logistics.customer_service.yaml` | `case_intake`, `status_response_draft`, `escalation_packet` | `tms_read`, `customer_messaging_send`, `crm_read` | `tms`, `crm`, `customer_messaging`, `ticketing` |
| `planning.demand_forecast` | `profiles/planning.demand_forecast.yaml` | `forecast_intake`, `variance_review`, `demand_plan_packet` | `erp_read`, `inventory_read`, `analytics_read` | `erp`, `inventory_system`, `analytics`, `planning_system` |

### retail -> CommerxFactory

| Subtype | Profile file | Workflow specs | Credential requirements | Adapter contracts |
| --- | --- | --- | --- | --- |
| `ecommerce_ops.marketplace` | `profiles/ecommerce_ops.marketplace.yaml` | `order_exception_review`, `listing_quality_review`, `marketplace_case_packet` | `ecommerce_platform_read`, `marketplace_read`, `support_system_write` | `ecommerce_platform`, `marketplace`, `support_system` |
| `customer_ops.returns` | `profiles/customer_ops.returns.yaml` | `return_intake`, `refund_review`, `customer_response_draft` | `order_system_read`, `support_system_write`, `payment_system_read` | `order_system`, `support_system`, `payment_system` |
| `merchandising.pricing` | `profiles/merchandising.pricing.yaml` | `promotion_review`, `pricing_exception_packet`, `inventory_replenishment_review` | `product_catalog_read`, `pricing_write`, `inventory_read` | `product_catalog`, `pricing_system`, `inventory_system` |
| `inventory.replenishment` | `profiles/inventory.replenishment.yaml` | `stockout_review`, `replenishment_packet`, `vendor_follow_up` | `inventory_read`, `erp_read`, `supplier_portal_read` | `inventory_system`, `erp`, `supplier_portal` |
| `store_ops.physical` | `profiles/store_ops.physical.yaml` | `store_task_intake`, `incident_packet`, `staffing_gap_review` | `store_system_read`, `workforce_system_read`, `support_system_write` | `store_system`, `workforce_system`, `ticketing` |
| `loyalty.crm` | `profiles/loyalty.crm.yaml` | `segment_review`, `loyalty_offer_review`, `customer_message_packet` | `crm_read`, `customer_messaging_send`, `analytics_read` | `crm`, `loyalty_platform`, `customer_messaging`, `analytics` |
| `fraud.chargebacks` | `profiles/fraud.chargebacks.yaml` | `chargeback_intake`, `evidence_packet`, `dispute_response_review` | `payment_system_read`, `order_system_read`, `document_repository_read` | `payment_system`, `order_system`, `document_repository` |
| `product_content.catalog` | `profiles/product_content.catalog.yaml` | `catalog_gap_review`, `listing_update_packet`, `content_quality_review` | `product_catalog_read`, `cms_write`, `creative_asset_read` | `product_catalog`, `cms`, `creative_asset_store` |
| `retail.analytics` | `profiles/retail.analytics.yaml` | `data_quality_review`, `sales_report_packet`, `margin_analysis` | `analytics_read`, `ecommerce_platform_read`, `inventory_read` | `analytics`, `ecommerce_platform`, `inventory_system`, `bi_platform` |
| `subscription.commerce` | `profiles/subscription.commerce.yaml` | `subscription_exception_review`, `billing_issue_packet`, `retention_offer_review` | `subscription_platform_read`, `payment_system_read`, `customer_messaging_send` | `subscription_platform`, `payment_system`, `customer_messaging`, `crm` |

## Runtime Binding Hand-Off

After the generic fixes above, run the self-hosted runtime binding wizard.

Required runtime binding outputs:

- deployment target
- Hermes runtime references
- Omnigent runtime references
- secret provider and vault references
- credential binding references
- adapter endpoint references
- approver references
- runtime validation report
- first workflow dry-run evidence
- live approval decision when live execution is requested
