# Client Hermes Product And Service Scaffold

Status: draft
Kind: template
Repository context: openxFactory
Purpose: define a reusable Client Hermes scaffold for organizations that sell,
deliver, support, or operate products, services, or hybrid offers.

## 1. Core Idea

Every Client Hermes layer represents an operating organization. Most operating
organizations offer one or more of these:

```text
product
service
productized service
subscription
managed service
marketplace offer
usage-based offer
project or engagement
outcome-based offer
```

Client Hermes should therefore model the client's business as an offer system:

```text
Client Hermes
  -> offer catalog
  -> customer roster
  -> staff and capability map
  -> operating policy
  -> integrations and credential bindings
  -> approval and escalation rules
  -> delivery, fulfillment, support, renewal, and outcome monitoring
```

The offer system is domain-neutral. MedxFactory may map offers to care programs,
visits, imaging services, pharmacy support, or patient communication workflows.
AdxFactory may map offers to campaigns, retainers, launches, or creative
packages. LedgerxFactory may map offers to bookkeeping, close, tax, audit, or
controller services. OpsxFactory may map offers to managed services, change
requests, backups, identity administration, or incident response.

Client installation may use the client's own document management system,
historical email, ticketing, CRM, calendars, and collaboration spaces to
discover real workflows. Those sources describe current state. They do not
become operational policy until gap review and Hermes approval. See
[Client Installation Discovery And Workflow Migration](client-installation-discovery-and-migration.md).

## 2. Product Versus Service Lens

The product/service distinction gives Client Hermes a practical scaffold.

| Offer shape | Client Hermes needs to model |
| --- | --- |
| Product | Catalog item, variant, entitlement, configuration, fulfillment, inventory or availability, warranty/return/support rules, activation state. |
| Service | Scope, intake criteria, assignment, schedule, capacity, deliverable, SLA, completion criteria, review, follow-up, renewal. |
| Productized service | Fixed service package with explicit inputs, outputs, pricing/budget guardrails, turnaround, and escalation path. |
| Subscription | Entitlement, term, renewal, usage, seats, plan limits, cancellation, expansion, support level. |
| Managed service | Standing authorization envelope, monitored assets, service windows, incident/change classes, escalation contacts, privileged credentials. |
| Marketplace offer | Supplier/provider, offer listing, eligibility, routing, dispute/return path, payout or settlement boundary. |
| Outcome-based offer | Target outcome, measurement method, intervention classes, risk boundaries, proof requirements, review cadence. |

This lens should not turn Client Hermes into a full ERP or CRM. It gives the
client layer enough structure to route work, enforce local policy, and explain
what the organization is allowed to do for a customer.

## 3. Client Layer Objects

Client Hermes should start with these domain-neutral objects.

```yaml
client_profile:
  client_id: string
  client_kind: string
  operating_model: product | service | hybrid | marketplace | managed_service
  staff_roles: []
  locations_or_operating_units: []
  default_timezone: string
  supported_customer_kinds: []

offer_catalog:
  products: []
  services: []
  subscriptions: []
  bundles: []
  managed_services: []

customer_roster:
  relationship_types: []
  onboarding_states: []
  offboarding_states: []
  active_entitlements: []

operating_policy:
  service_boundaries: []
  approval_rules: []
  escalation_rules: []
  communication_rules: []
  quality_rules: []

integration_map:
  systems: []
  credential_bindings: []
  tool_permissions: []
  source_workspaces: []
```

Domain factories can add domain-specific fields, but these objects should stay
recognizable across all client overlays.

## 4. Client Hermes Agent Scaffold

Client Hermes should have a stable operating team. Domains can rename these
agents, but the responsibilities should remain visible.

| Agent | Purpose |
| --- | --- |
| Client Profile Steward | Maintains client identity, deployment profile, tenant boundaries, locations, operating units, and supported customer kinds. |
| Offer Catalog Steward | Models products, services, subscriptions, bundles, eligibility, scope, deliverables, and entitlement rules. |
| Customer Relationship Steward | Maintains customer roster, relationship status, onboarding/offboarding, entitlement state, and account context. |
| Intake And Triage Agent | Converts staff/customer requests into the right offer, workflow, risk class, and required context. |
| Configure Quote Scope Agent | Helps scope a product, service, plan, engagement, or workflow package before approval or delivery. |
| Fulfillment Or Delivery Coordinator | Tracks assignment, schedule, capacity, deliverables, status, and completion criteria. |
| Policy And Approval Gatekeeper | Applies client policy, local approval rules, service boundaries, and stricter-than-domain gates. |
| Integration And Credential Steward | Tracks systems, credential bindings, tool permissions, grant readiness, and integration health. |
| Staff Capability And Routing Agent | Maps staff roles, licenses, permissions, availability, and escalation contacts to allowed work. |
| Communication And Handoff Agent | Drafts customer-facing updates, internal handoffs, escalation notes, and next-step explanations. |
| Quality And Outcome Monitor | Tracks SLA, quality, exceptions, outcome measures, complaint signals, and follow-up triggers. |
| Renewal Expansion Retention Agent | Monitors renewals, lifecycle events, expansion opportunities, cancellations, and service continuity. |
| Exception And Dispute Agent | Handles blocked work, disputes, returns, failed service delivery, policy conflicts, and complaint escalation. |
| Client Memory Steward | Decides what becomes client-level memory, what remains customer-private, and what may be promoted to domain learning. |
| Source Inventory Agent | Catalogs approved document, email, ticket, CRM, calendar, and collaboration sources for installation discovery. |
| Practice Gap Auditor | Compares observed current practice with domain standards, client policy, security rules, and customer-facing expectations. |
| Migration Planner Agent | Produces containment, dual-run, cutover, retirement, and drift-monitoring plans for bad or weak current practice. |

This team is not a set of always-running autonomous workers. It is a role
scaffold. Agents may be implemented as prompts, tools, workflow roles, review
councils, deterministic services, or human-assisted queues.

## 5. Skill Scaffold

Client Hermes skills should be grouped by the work of operating an offer.

```text
offer_modeling
  define products, services, bundles, subscriptions, plans, and managed services

eligibility_and_fit
  decide which customers, contexts, staff, systems, or assets qualify

intake_and_scope
  gather inputs, constraints, desired outcome, urgency, and missing context

configuration_and_entitlement
  select options, variants, plan limits, coverage, access, or service level

routing_and_assignment
  select staff, queue, workflow, domain profile, or escalation path

approval_packet_preparation
  summarize request, risk, evidence, policy fit, and approval options

delivery_coordination
  track schedule, capacity, status, deliverables, and dependencies

customer_communication
  draft updates, confirmations, explanations, reminders, and handoff messages

integration_readiness
  verify systems, credentials, permissions, source workspaces, and grant paths

quality_and_outcome_monitoring
  watch SLA, customer satisfaction, accuracy, safety, errors, and follow-up need

exception_handling
  triage blocked workflows, complaints, disputes, returns, incident paths, and repairs

renewal_and_lifecycle
  manage renewal, expansion, downgrade, cancellation, offboarding, and continuity

source_inventory
  inventory approved installation sources, owners, scopes, and retention rules

workflow_trace_reconstruction
  reconstruct current-state workflows from cited documents, email, tickets, and records

practice_gap_analysis
  compare current practice with target domain and client standards

migration_plan_design
  design containment, dual-run, cutover, retirement, and monitoring steps
```

Each skill should declare:

- allowed inputs
- prohibited inputs
- required tools
- required approvals
- evidence produced
- handoff target
- memory promotion rule
- UI surfaces where the skill appears

## 6. User Interaction Scaffold

Client Hermes should expose a hybrid UI: avatar-assisted where guidance matters,
conventional where density and repeatability matter.

### Operator Avatar

Use an avatar for:

- "What is this customer asking for?"
- "Which product or service does this map to?"
- "What is missing before we can start?"
- "Why is this blocked?"
- "What approval is needed?"
- "Who should handle this?"
- "What should we tell the customer?"
- "What changed since last time?"

The avatar should be able to walk a staff member through setup, intake, scope,
approval, exception handling, and handoff.

### Conventional Operator Console

Use conventional UI for:

- customer roster
- offer catalog
- queue and status board
- approval queue
- staff/capability matrix
- schedule/capacity view
- integration and credential binding status
- SLA and outcome dashboard
- exception/dispute queue
- audit and transcript search
- policy and escalation configuration

The console should be dense, filterable, and built for repeated operational
use.

### Guided Setup Wizard

The client-layer setup wizard should ask:

```text
What does this client sell or provide?
Is it a product, service, productized service, subscription, managed service,
marketplace, project, or hybrid offer?
Who receives value?
Who approves delivery?
Who performs delivery?
What systems are needed?
What credentials are needed?
What workflows are customer-facing?
What workflows are high-risk?
What can be done under standing approval?
What always requires human approval?
What does completion mean?
What should be measured?
Which document management, email, ticketing, CRM, calendar, or collaboration
sources may be analyzed for installation discovery?
Which observed current practices are known to be outdated, risky, or informal?
Which best-practice standards should override bad current practice?
What migration path is acceptable before cutover?
Which affected users, workflow owners, or client approvers must consent before
we replace, constrain, automate, or retire a current workflow?
```

## 7. Standard Client Workflows

Every client overlay should consider these starter workflows.

| Workflow | Purpose |
| --- | --- |
| Offer setup | Define product/service catalog, eligibility, scope, deliverables, and policy. |
| Customer onboarding | Establish customer relationship, permissions, preferences, entitlements, and starting state. |
| Request intake | Turn a request or observed need into a scoped workflow. |
| Eligibility and fit check | Verify that the offer, customer, staff, systems, and policy fit. |
| Scope and configuration | Choose product options, service scope, plan limits, or engagement terms. |
| Approval routing | Package risk, evidence, policy fit, and recommendation for the right approver. |
| Delivery or fulfillment | Assign, schedule, execute, track, and complete the offer. |
| Customer communication | Explain next steps, status, missing inputs, and outcomes. |
| Exception handling | Manage blocked work, complaints, disputes, failed delivery, or unsafe requests. |
| Outcome review | Measure quality, SLA, customer result, and follow-up need. |
| Renewal or lifecycle | Renew, expand, downgrade, offboard, retire, return, or close. |
| Installation discovery | Use authorized client documents and email to map current workflows with source traces. |
| Workflow migration | Move weak or bad current practice through containment, target design, dual-run, cutover, retirement, and drift monitoring. |

## 8. Product-Specific Patterns

Product-like clients need:

- product catalog and variant model
- inventory, availability, or entitlement state
- configuration and compatibility rules
- activation, warranty, return, replacement, or support policy
- purchase, fulfillment, delivery, or access workflow
- product content and documentation sources
- product lifecycle and deprecation rules

Useful agents:

- Product Catalog Steward
- Compatibility And Fit Agent
- Entitlement Agent
- Fulfillment Agent
- Warranty/Return Agent
- Product Content Steward

## 9. Service-Specific Patterns

Service-like clients need:

- service catalog
- intake requirements
- scope boundaries
- staff capability map
- assignment and scheduling
- capacity and SLA rules
- deliverable templates
- completion criteria
- renewal, follow-up, or continuity policy

Useful agents:

- Service Catalog Steward
- Intake And Scope Agent
- Capacity Scheduler
- Delivery Coordinator
- SLA Monitor
- Follow-Up Agent

## 10. Hybrid Offer Patterns

Many real clients sell hybrids.

Examples:

```text
software product + implementation service
medical device + monitoring service
bookkeeping subscription + monthly close service
managed IT service + hardware/product procurement
marketing retainer + campaign deliverables
training product + coaching service
```

Client Hermes should model hybrids as bundles with:

- product component
- service component
- standing approval envelope
- shared customer entitlement
- delivery milestones
- support boundary
- renewal or expansion logic

## 11. Memory And Learning

Client Hermes should separate memory into three buckets.

```text
client_private_memory
  client policy, staff preferences, operating history, integration lessons

customer_relationship_memory
  customer status, relationship context, entitlements, service history

domain_learning_candidates
  reusable patterns that may be promoted only after domain review
```

Client Hermes must not promote customer-private facts into domain memory unless
the customer and client policies allow it and the owning Hermes layer approves.

## 12. Starter Files

A domain starter should include these client-layer scaffold files:

```text
hermes/client/template.yaml
hermes/client/offering-catalog.template.yaml
hermes/client/agent-teams.template.yaml
hermes/client/skills.template.yaml
hermes/client/user-interactions.template.yaml
hermes/client/installation-discovery.template.yaml
hermes/client/memory-boundaries.yaml
hermes/client/policy-overrides.yaml
hermes/client/integration-boundaries.yaml
```

Those files should remain templates until a real client or tenant
instantiation supplies the operating model, offer catalog, approvers, systems,
credential bindings, and customer roster.
