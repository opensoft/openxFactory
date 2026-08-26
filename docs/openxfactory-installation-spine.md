# openxFactory Installation Spine And Domain Overlays

Status: draft
Kind: architecture
Repository context: openxFactory
Purpose: define how installations use a domain-neutral openxFactory workflow
and optional DomainxFactory overlays such as MedxFactory or LedgerxFactory.

## 1. Decision

Use a hybrid installation model.

```text
openxFactory installation spine
  -> always runs the shared control plane

DomainxFactory installation overlay
  -> supplements, replaces, constrains, or vetoes declared stages
     while emitting the same openxFactory artifacts
```

The general workflow should not be replaced wholesale. It owns the invariant
installation controls. A domain workflow should specialize the places where
domain knowledge materially changes how a client xFactory is configured.

## 2. The Two Layers

### openxFactory Installation Spine

The spine is the general workflow for every installation, including clients
without a dedicated domain repo.

It owns:

- installation scope
- domain and profile resolution
- source access consent
- source inventory
- source traceability
- current-state workflow discovery
- user validation walkthrough
- current-state versus target-state separation
- workflow-change consent
- gap disposition vocabulary
- migration plan shape
- approval and audit records
- dry-run, cutover, rollback, and drift controls

The spine is domain-neutral. It can install a generic product or service
workflow when no domain repo exists.

### DomainxFactory Installation Overlay

The overlay is optional. It exists when a domain repo has reusable expertise,
domain workflows, policies, checks, roles, or best-practice migration paths.

It owns:

- domain ontology
- domain-specific source types
- domain workflow catalog
- domain best-practice standards
- domain roles and capability rules
- domain compliance checks
- domain migration playbooks
- domain validation examples
- domain-specific target workflow generation
- domain-specific cutover and drift rules

MedxFactory can specialize the spine for clinics, hospitals, pharmacies,
patients, eligibility, referrals, prior auth, clinical boundaries, and RCM.
LedgerxFactory can specialize it for bookkeeping, reconciliations, close,
tax, audit trails, approvals, and accounting controls.

## 3. Nonreplaceable Controls

Domain overlays may not replace these controls:

- source access must be scoped and consented
- raw credentials and unrestricted private exports are forbidden
- current-state evidence is not target operational policy
- AI-inferred workflows are hypotheses until source-backed and user validated
- every target workflow requires a definition packet
- every gap requires a disposition
- workflow changes require explicit consent before cutover
- high-risk migration requires containment or human approval
- artifacts must retain source references and authority levels
- customer-specific facts must stay in the customer or client boundary unless
  promotion is approved
- domain overlays must emit openxFactory-compatible records

These controls are part of the shared safety and audit model. A domain repo may
tighten them, but it may not weaken or remove them.

## 4. Overlay Operations

Domain repos declare their behavior per stage using these operations.

| Operation | Meaning | Example |
| --- | --- | --- |
| `supplement` | Add prompts, sources, roles, examples, policies, checks, or UI explanations while keeping the base stage behavior. | MedxFactory adds patient consent source types to source inventory. |
| `replace` | Substitute the stage implementation because domain expertise changes the logic. The replacement must emit the same openxFactory artifacts. | LedgerxFactory replaces generic best-practice comparison with close, reconciliation, tax, and approval controls. |
| `constrain` | Add stricter gates or block unsafe variants while preserving the base stage. | MedxFactory requires extra review for clinical or HIPAA-sensitive cutover. |
| `veto` | Stop the stage or installation when domain preconditions are missing. | A medical workflow cannot be configured without required licensed-role rules. |

Replacement should be narrow. If the stage is mostly about governance,
consent, audit, or source traceability, the domain should supplement or
constrain rather than replace.

## 5. Stage Ownership Matrix

| Stage | openxFactory owns | Domain overlay behavior |
| --- | --- | --- |
| `install_scope` | Define client, product/service scope, tenant boundary, and requested outcome. | Supplement with domain-specific profiles and excluded workflows. |
| `domain_resolution` | Decide whether a dedicated domain repo applies or the generic installer should run. | Supplement with profile matching and domain capability declarations. |
| `source_access_consent` | Collect scoped consent to inspect documents, email, tickets, CRM, calendars, and related systems. | Supplement or constrain with domain-specific privacy, compliance, or delegated-consent language. |
| `source_inventory` | Catalog approved sources, owners, date windows, access modes, retention rules, and source families. | Supplement with domain systems and domain source taxonomy. |
| `current_state_inference` | Build evidence graph, event ledger, candidate process graph, and current workflow hypotheses. | Supplement with domain ontology, entity resolution, activity classes, and evidence interpretation. |
| `domain_ontology_seeding` | Validate and seed the declared `domain_ontology` package (content manifest → `contracts/domain-ontology/` validation: manifest, exact kernel import, inventory, digests) before any semantic classification consumes it; fail closed on drift. | The domain's published package pin; readiness stays `domain_scaffold_required` until Domain Hermes publishes. |
| `workflow_definition_packet` | Emit common states, transitions, roles, gates, artifacts, systems, messages, exceptions, and source refs. | Supplement with domain fields and required domain packet sections. |
| `user_validation_walkthrough` | Walk users through inferred current state, source evidence, conflicts, risks, and questions. | Supplement with domain visuals, examples, and role-specific explanations. |
| `best_practice_comparison` | Provide generic comparison frame, gap records, and disposition vocabulary. | Usually replace with domain best-practice standards, then emit openxFactory gap records. |
| `migration_plan` | Require current-to-target delta, containment, dual-run/cutover, rollback, training, and monitoring. | Often replace migration tactics with domain playbooks while preserving plan shape. |
| `workflow_change_consent` | Require explicit consent before changing enforced workflow behavior. | Supplement or constrain with domain consent language and approver rules. |
| `target_workflow_generation` | Generate target workflow artifact using approved packet, gaps, consent, and approvals. | Supplement or replace target generation using domain workflow templates. |
| `dry_run_cutover` | Require dry-run, cutover criteria, rollback or repair path, and approval refs. | Supplement, replace checks, constrain cutover, or veto if domain preconditions fail. |
| `drift_monitoring` | Watch for return to retired practices or new side channels. | Supplement with domain-specific drift signals and quality metrics. |

## 6. Generic Fallback

When no domain repo exists, openxFactory still installs a useful client
xFactory by using the generic product/service model:

```text
offer catalog
  -> customer subject model
  -> current workflow discovery
  -> generic best-practice gap review
  -> migration plan
  -> approved target workflow
  -> dry-run and drift monitoring
```

The fallback is intentionally conservative. It should configure obvious
product, service, subscription, support, approval, fulfillment, and renewal
workflows. It should not pretend to know regulated or professional standards
that belong in a domain repo.

## 7. Artifact Contract

Every installation, generic or domain-specific, emits these openxFactory
artifact families:

- `installation_scope`
- `domain_overlay_binding`
- `source_access_consent`
- `installation_source_inventory`
- `workflow_evidence_claim`
- `current_workflow_map`
- `workflow_definition_packet`
- `user_validation_record`
- `practice_gap`
- `workflow_migration_plan`
- `workflow_change_consent`
- `target_workflow_package`
- `dry_run_cutover_record`
- `drift_monitoring_plan`

Domain artifacts may be attached, but the shared artifacts remain the
cross-factory audit surface.

## 8. Implementation Surface

The openxFactory portion is machine-readable in:

- [openxFactory installation spine template](../templates/installation/openxfactory-installation-spine.yaml)
- [domain installation overlay schema](../contracts/schemas/domain-installation-overlay.schema.yaml)
- [domain overlay examples](../examples/installation/domain-overlay-examples.yaml)

Domain repos should publish an overlay manifest that references the
openxFactory spine version they implement, declares stage operations, and lists
the openxFactory artifact families they emit.

## 9. Installation Rule

Use this rule during implementation:

```text
Run the openxFactory spine every time.
Apply a domain overlay only where it declares a compatible stage operation.
If the domain overlay replaces a stage, require the same openxFactory outputs.
If there is a conflict, the stricter safety, consent, privacy, or audit rule wins.
```

