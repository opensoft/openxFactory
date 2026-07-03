# xFactory Domain Factory Model

This document generalizes `openxFactory` from a software development factory
into the reusable `xFactory` pattern.

`openxFactory` is the canonical stack and workflow contract for xFactory. It
defines the general composition and piping layer: required stack parts,
authority boundaries, job envelopes, approvals, traceability, worker routing,
admission gates, review gates, and final enforcement handoffs.

The xFactory layer has two jobs:

```text
stack composition
  define which layers/modules a DomainxFactory must have and what each owns

runtime governance
  define how approved work moves through gates, routing, execution, review,
  memory/source promotion, credentials, audit, and final handoff
```

Credential access is part of the same contract boundary. See
[xFactory Credential Access Model](credential-access-model.md) for how domain
stacks declare credential needs, clients bind them to secret providers, Hermes
approves use, and Omnigent workers receive short-lived scoped grants. See
[xFactory Domain Factory Starter Pack](domain-factory-starter-pack.md) for the
starter credentialing module each new domain should stub out.

Memory and knowledge provider access is also part of the xFactory contract
boundary. See
[xFactory Memory Gateway Architecture](customer-memory-gateway-architecture.md)
for how Customer Hermes memory providers and Omnigent expert memory or
knowledge DBs are routed through xFactory rails, bindings, migrations,
metering, and audit before any provider adapter is used. See
[Customer Memory Fill And Maintenance Taxonomy](customer-memory-fill-maintenance-taxonomy.md)
for the general fill and maintenance modes that each DomainxFactory must map to
its own source families, evidence types, reviewers, and adapters.

Hermes Mixture of Agents reasoning is part of the Hermes overlay surface, not a
replacement for xFactory. See
[Hermes Mixture Of Agents For xFactory](hermes-mixture-of-agents-for-xfactory.md)
for the standard mix profile shape, context-packet rules, evidence records, and
credential guardrails.

Domain factories apply domain-specific Hermes and Omnigent overlays on top of
that general piping layer.

Template selection must separate the factory's work type from the buyer's
industry. See [xFactory Taxonomy Model](factory-taxonomy-model.md).

```text
factory_type + factory_subtype
  selects the expert work and Omnigent layer

target_domain + target_domain_subtype
  selects the subject matter overlay

client_industry + client_type
  selects client-facing assumptions and deployment language
```

## Core Idea

```text
xFactory / openxFactory
  generic stack composition, workflow contracts, gates, routing, and traceability

Domain factory
  xFactory plus domain-specific Hermes, client Hermes, customer Hermes,
  and Omnigent overlays

Customer layer
  patient, buyer, prospect, project, matter, campaign, or other
  customer-specific operating subject
```

Examples:

```text
codexFactory
  = xFactory + Software Engineering Domain Hermes + Software Company Hermes
    + Project Hermes + Opensoft Omnigent overlay

MedxFactory
  = xFactory + Medical Domain Hermes + Clinic Hermes + Patient Hermes
    + Medx Omnigent overlay

OpsxFactory
  = xFactory + Operations Domain Hermes + IT Customer Hermes
    + Managed System Hermes + Opsx Omnigent overlay

LedgerxFactory
  = xFactory + Ledger Domain Hermes + Firm Hermes + Ledger/Client Hermes
    + LedgerX Omnigent overlay

AdxFactory
  = xFactory + Marketing Domain Hermes + Marketing Company Hermes
    + Buyer Hermes + Adx Omnigent overlay
```

The domain factory should not fork the xFactory contract. It should provide
overlays, policy packs, expert teams, tool bundles, memory boundaries, review
standards, and domain-specific workflows that plug into the same base contract.

## Layer Model

```text
Customer subject
  patient, buyer, prospect, project, matter, campaign

Customer Hermes layer
  customer-specific control, private memory, consent, preferences, context

Client Hermes layer
  Opensoft client/operator control, tenant memory, local policy, staff,
  integrations, and customer relationship context

Domain Hermes layer
  domain governance, domain agent team, policy, routing, review standards,
  product learning, and domain memory

xFactory / openxFactory layer
  required stack parts, three-Hermes-layer contract, general job envelope,
  gates, traceability, worker routing, artifact contracts

Domain Omnigent layer
  domain-tuned orchestration, expert selection, task decomposition, checks,
  and bounded expert context consumption

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

Every xFactory domain stack standardizes on three Hermes overlays above the
base runtime:

```text
Customer Hermes
  "What does this specific customer subject need, allow, prefer, remember,
  and currently have in flight?"

Client Hermes
  "What does this Opensoft client organization operate, permit, configure,
  staff, integrate with, and owe to its customers?"

Domain Hermes
  "What does this domain know, require, permit, route, review, and improve?"
```

The three layers must remain distinct even when one deployment starts small.
Small deployments may run the layers in one physical Hermes installation, but
their manifests, memory boundaries, authorization scopes, and approval records
must still identify which layer owns each decision.

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

Client Hermes overlays tune the domain runtime for one Opensoft client
organization or tenant operator.

A client Hermes overlay owns:

- client organization identity
- deployment profile and tenant configuration
- client staff, roles, teams, and escalation contacts
- local operating policy and service boundaries
- client-specific integrations, systems, and tool permissions
- client-specific memory and operating history
- customer roster and relationship context
- local approval gates that are stricter than the domain default
- client-specific reporting, SLA, and communication preferences

Customer Hermes overlays tune the client runtime for one customer subject.

A customer Hermes overlay owns:

- customer subject identity
- customer-specific private context
- consent, authorization, and data-sharing boundaries
- customer goals and preferences
- customer timeline
- customer evidence graph and source claims
- customer current state snapshots
- customer-specific agent assignments
- customer-specific memory
- customer-specific status and follow-up
- customer-to-client or customer-to-domain promotion candidates
- customer-specific communication preferences

See [Customer Hermes Memory Model](customer-hermes-memory-model.md) for the
canonical identity, consent, preference, timeline, evidence graph, current
state, memory, workflow context, follow-up, and promotion objects shared across
DomainxFactories.

See [xFactory Memory Gateway Architecture](customer-memory-gateway-architecture.md)
for the product-neutral implementation pattern that routes Hermes memory access
and Omnigent expert memory or knowledge DB access through xFactory rails before
provider adapters such as GBrain, Honcho, AgentMemory, root-truth DBs, source
workspaces, graph stores, vector indexes, playbook stores, or evaluation memory.

The same base Hermes install can support many domain overlays. The same domain
Hermes overlay can support many client Hermes overlays. The same client Hermes
overlay can support many customer Hermes overlays.

## Hermes Mixture Of Agents

Any Hermes layer may use a Mixture of Agents preset as an internal reasoning
step.

```text
Hermes layer
  -> Hermes role or council
  -> optional Mixture of Agents preset
  -> acting Hermes role synthesizes recommendation
  -> Hermes gate decision
  -> openxFactory job envelope or state transition
```

Mixture of Agents does not add a fourth Hermes layer. It is a review pattern
inside the existing domain, client, or customer Hermes layer.

Reference agents are advisory. They receive only approved context packets and
must not receive raw secrets, unrestricted private records, runtime credential
grants, or tool access. The acting Hermes role may request tool use or runtime
capability grants only through the openxFactory gate and credential broker
contract.

Domain factory repos declare reusable mix profiles under `hermes/domain/`.
Client and customer overlays may specialize those profiles through templates
under `hermes/client/` and `hermes/customer/`.

```text
hermes/domain/agent-mixes.yaml
hermes/client/agent-mixes.template.yaml
hermes/customer/agent-mixes.template.yaml
```

Common mix uses include pre-run simulation, setup readiness review, gate review
packets, credential approval review, memory promotion review, high-risk action
planning, and domain expert panels.

The default native Hermes Mixture of Agents pattern is `panel_synthesis`:
independent reference outputs followed by acting Hermes synthesis. xFactory adds
two governed council modes on top of that primitive:

```text
scored_vote
  independent opinions -> explicit vote or score -> acting Hermes synthesis

deliberative_council
  independent opinions -> disagreement summary -> rebuttal
  -> revised opinions -> consensus or dissent record
  -> acting Hermes recommendation
```

Both modes produce recommendation evidence only. They do not approve work
without the owning Hermes gate, review council, accountable human, or external
enforcement system.

## Three Hermes Layers

The customer Hermes, client Hermes, and domain Hermes layers must remain
distinct.

```text
Customer Hermes
  Close to the customer subject.

Client Hermes
  Close to the Opensoft client/operator organization.

Domain Hermes
  Close to the reusable domain product and expert team.
```

The customer Hermes layer is a private concierge and lifetime-control layer.

It is close to the specific customer subject. In a medical factory, the
customer subject is a patient. In a marketing factory, it is a buyer, prospect,
audience member, or account. In a code factory, it is a project, repo, product,
or feature initiative.

The client Hermes layer is the operating layer for the Opensoft client.

It is close to the organization using the factory. In a medical factory, the
client is a clinic, group practice, hospital, pharmacy, imaging center, or IDTF.
In a marketing factory, the client is the marketing company or agency. In a code
factory, the client is the software company or engineering organization.

The domain Hermes layer is the shared domain control tower.

It is close to the expert team. It manages reusable domain expertise, domain
workflows, policy, review quality, escalation, and domain-level memory.

## Hermes Monitoring and Self-Initiation

Hermes layers are active control teams, not passive configuration records. Each
layer may monitor its owned state, notice changes, start allowed workflows,
request approval, escalate risks, and create xFactory jobs inside its authority
boundary.

Self-initiation must always be traceable to one of these sources:

- standing approval envelope
- customer request or observed customer need
- client operating requirement
- domain policy requirement
- scheduled review or follow-up
- risk, exception, or compliance trigger
- human instruction
- downstream system event

Self-initiation does not mean a layer may bypass approvals. It means the layer
may recognize that work is needed and create the next governed action.

Allowed self-initiated actions:

- observe and record a state change
- update private memory inside the owning layer
- create a recommendation
- create an approval request
- route a question to another Hermes layer
- start a low-risk workflow inside a standing approval envelope
- create an xFactory job with the required references and gates
- escalate to human or domain review

Disallowed self-initiated actions:

- weaken a domain, client, or customer gate
- promote private customer data into client or domain memory without approval
- execute regulated or high-risk work outside an approval envelope
- decide a domain outcome when the domain requires expert or human review
- assume authority from another xFactory domain stack

### Customer Hermes Teams

There should be one customer Hermes instance or logical team per customer
subject.

Each customer Hermes team has a small core roster:

- identity and context steward
- consent, authorization, and privacy steward
- customer-item relationship steward
- journey state and follow-up steward
- communication steward
- memory and timeline steward

The customer team may dynamically add or remove agents based on:

- active focal items
- journey state
- customer risk level
- consent boundaries
- current workflow
- client policy
- domain policy
- required expertise
- language, accessibility, or communication needs

Dynamic agents are assigned to the customer's current need. They do not become
permanent owners of customer truth unless the customer Hermes layer records that
assignment. When the need ends, customer Hermes should close or retire the
temporary assignment and preserve only the approved trace.

Examples:

```text
MedxFactory
  Patient Hermes starts with core patient context, consent, timeline, and
  follow-up agents. A cardiology-focused agent may join while the patient has an
  active cardiac focal item.

AdxFactory
  Buyer Hermes starts with identity, consent, journey, and communication agents.
  A pricing-objection agent may join while the buyer is in late consideration
  for a specific offer.

codexFactory
  Project Hermes starts with scope, repo, traceability, and delivery agents. A
  security-review agent may join while the project touches sensitive auth code.
```

### Client Hermes Monitoring

Client Hermes monitors the domain-specific operating needs of the Opensoft
client organization. It should not try to become the client's entire business
operating system unless the domain stack is specifically a corporate business
factory.

Client Hermes owns monitoring for:

- tenant configuration and enabled workflows
- client staff, roles, licenses, privileges, and domain capability assignments
- domain-specific compliance obligations
- client-specific policy overrides within domain limits
- customer roster and customer relationship state
- client integrations needed for the domain
- domain-specific credentials, coverage, payer, vendor, or facility constraints
- local approvals, escalations, review queues, and operating exceptions
- client-level outcome reporting for the domain

Client Hermes does not own general business operations by default:

- payroll
- employee tax withholding
- general HR benefits
- general corporate accounting
- general corporate legal
- office rent and facilities unrelated to domain service delivery
- generic procurement unrelated to domain workflows

Those belong in a corporate business, finance, HR, legal, or operations domain
stack unless they directly gate the domain workflow.

### Client Hermes Product And Service Model

Client Hermes should model the client organization's domain-specific offers.
Most clients sell, deliver, support, or operate one or more of:

- products
- services
- productized services
- subscriptions
- managed services
- marketplace offers
- projects or engagements
- outcome-based offers

This gives the client layer a reusable operating grammar:

```text
offer catalog
  -> what the client provides

customer roster
  -> who receives value and under what relationship

staff and capability map
  -> who may perform or approve work

integration and credential map
  -> which systems and scoped grants are needed

approval and escalation rules
  -> what can proceed, what is blocked, and who decides

delivery and outcome model
  -> how fulfillment, service delivery, support, quality, renewal, and
     completion are tracked
```

Product-like offers need catalog, variant, entitlement, configuration,
fulfillment, activation, warranty/return, and support rules.

Service-like offers need intake criteria, scope, assignment, schedule, capacity,
deliverables, SLA, completion criteria, review, follow-up, and renewal rules.

Hybrid offers should be modeled as bundles with product components, service
components, standing approval envelopes, shared customer entitlements, delivery
milestones, support boundaries, and renewal or expansion logic.

See [Client Hermes Product And Service Scaffold](client-hermes-product-service-scaffold.md).

### Installation Spine And Domain Overlays

Client installation uses a two-layer model. The openxFactory installation spine
always runs the shared control plane: scope, consent, source inventory,
current-state inference, validation, gap disposition, migration planning,
workflow-change consent, target generation, cutover, rollback, and drift
monitoring.

Domain repos such as MedxFactory or LedgerxFactory may overlay that spine. They
should supplement stages where they add domain vocabulary, source types,
examples, or stricter gates. They should replace only the stages where domain
expertise changes the implementation, usually best-practice comparison,
migration playbooks, target workflow generation, and domain cutover checks.

See [openxFactory Installation Spine And Domain Overlays](openxfactory-installation-spine.md).

### Client Installation Discovery And Migration

Client Hermes may use the installing company's document management system,
historical email, ticketing systems, CRM notes, calendars, and collaboration
spaces to discover how the client actually works today.

Those sources are evidence of current state, not automatic policy for the new
xFactory installation. A discovered workflow must pass through source tracing,
current-state mapping, workflow definition, user validation, best-practice
comparison, gap classification, migration planning, workflow-change consent, and
Hermes approval before it becomes a target workflow.

Use this rule:

```text
observed current practice
  -> source trace
  -> current workflow map
  -> workflow definition packet
  -> user validation
  -> best-practice gap review
  -> migration plan
  -> workflow-change consent
  -> approved target workflow
```

Bad or weak current practice should be dispositioned as `adopt_as_is`,
`configure_variant`, `migrate_to_best_practice`, `contain_temporarily`,
`quarantine`, or `reject`.

See [Client Installation Discovery And Workflow Migration](client-installation-discovery-and-migration.md).

### Domain-Specific Business Boundary

Some business-looking concerns are still domain concerns because they determine
whether domain work may legally, safely, or contractually happen.

Use this rule:

```text
If the fact gates whether a domain workflow may be performed, routed, billed,
reviewed, or trusted, it belongs in the domain factory boundary.

If the fact is a general company operation that would exist the same way in any
business, it belongs outside the domain factory unless another domain workflow
explicitly depends on it.
```

Clinic examples:

| Concern | Owner | Reason |
| --- | --- | --- |
| Employee tax withholding | Corporate business or payroll stack | General employer obligation, not clinic-domain work authorization |
| Practitioner malpractice or required professional coverage | MedxFactory client Hermes, with domain policy from Medical Domain Hermes | It may gate whether a practitioner may perform covered clinical work |
| LVN, NP, MD license and scope for a procedure | Medical Domain Hermes defines the general rule; Clinic Hermes applies it to local staff, state, facility, and current credential state | Determines whether a clinical workflow may be assigned or performed |
| Clinic-local policy that is stricter than law | Clinic Hermes | Client-specific operating constraint inside the domain |
| State regulation for who may perform an advanced procedure | Medical Domain Hermes | Reusable domain law and scope-of-practice rule |
| Patient consent for that procedure | Patient Hermes | Customer-specific authorization boundary |

The domain Hermes layer owns the reusable rules: laws, standards, role
capabilities, domain policy, evidence requirements, and review gates.

The client Hermes layer owns the local application of those rules: which staff,
locations, facilities, payers, credentials, policies, and current documents make
the work allowed for this client now.

The customer Hermes layer owns customer-specific permission and need: consent,
preferences, condition, journey state, and whether the customer should be routed
into that workflow.

When a concern crosses stacks, the current layer should route or request a
decision rather than absorb the other stack's responsibilities.

Examples:

```text
Clinic Hermes sees an NP credential expiring.
  -> This is in MedxFactory because it gates clinical assignment.

Clinic Hermes sees payroll tax filing is due.
  -> This belongs to a corporate business or payroll factory.

Clinic Hermes sees payroll failure could remove all nurses from next week's
schedule.
  -> Clinic Hermes may raise a domain operating risk and route the payroll issue
     to the corporate stack, but it does not become payroll owner.
```

## Standard Layer Mapping

| Domain stack | Customer Hermes | Client Hermes | Domain Hermes |
| --- | --- | --- | --- |
| MedxFactory | Patient Hermes | Clinic, practice, hospital, pharmacy, imaging center, or IDTF Hermes | Medical Domain Hermes |
| AdxFactory | Buyer Hermes for a buyer, prospect, audience member, or account | Marketing Company Hermes for the agency or marketing operator | Marketing Domain Hermes |
| codexFactory | Project Hermes for a project, repo, product, or feature initiative | Software Company Hermes for the engineering organization | Software Engineering Domain Hermes |
| LedgerxFactory | Ledger/Client Hermes for a company, ledger, tax matter, or engagement | Firm Hermes for the accounting or finance operator | Ledger Domain Hermes |

## Customer-Item Interaction Model

Every domain factory should model a customer subject in relation to one or more
focal items. The focal item is the thing the customer is considering, using,
experiencing, affected by, trying to change, or trying to resolve.

The base xFactory contract uses neutral terms:

```text
Customer
  the person, organization, account, project, or other subject being modeled

Focal item
  the product, service, condition, treatment, project, matter, campaign, or
  other thing the customer is interacting with

Interaction
  an observed or planned contact between the customer and the focal item,
  client organization, domain process, content, tool, or human team

Journey state
  the customer's current position in a domain-specific lifecycle

Outcome
  a target, predicted, observed, or reviewed result of the interaction over time

Intervention
  an approved action intended to change the journey state or outcome
```

The point of the model is to make each domain able to ask the same general
questions:

- Who or what is the customer subject?
- What focal item is currently important?
- What is the customer's current state relative to that item?
- What interactions have already happened?
- What outcome are we trying to predict, improve, prevent, or personalize?
- Which intervention is allowed, useful, and appropriately reviewed?
- What evidence would prove the prediction or intervention was right or wrong?

Domain stacks specialize the neutral model:

| Domain stack | Customer | Focal item | Journey state | Outcome |
| --- | --- | --- | --- | --- |
| AdxFactory | Buyer, prospect, account, advertiser audience member, or marketing client customer | Product, service, offer, brand, campaign, subscription, or purchase decision | Awareness, interest, consideration, conversion, onboarding, retention, expansion, churn risk | Conversion, retention, lifetime value, satisfaction, campaign response, next-best action |
| MedxFactory | Patient | Disease, symptom cluster, treatment, diagnostic pathway, medication, device, care plan, or referral | Risk, suspicion, diagnosis, treatment planning, active treatment, monitoring, remission, recurrence, follow-up | Clinical outcome, diagnostic confidence, adherence, side effects, progression, recovery, readmission risk |
| codexFactory | Project, repo, product, feature initiative, or engineering customer | Feature, bug, architecture decision, service, dependency, release, or technical debt item | Discovery, specification, planning, implementation, review, release, operation, incident response | Delivery confidence, defect risk, maintainability, release readiness, user impact |
| LedgerxFactory | Company, client, ledger, tax matter, or engagement | Transaction, account, filing, report, obligation, forecast, audit issue, or financial decision | Intake, reconciliation, review, filing, close, audit, advisory, exception handling | Accuracy, compliance risk, cash position, tax exposure, audit readiness, decision confidence |

### Model Records

The generic model should be represented by linked records rather than a single
large blob:

```text
customer_profile
  stable customer identity, permissions, preferences, private context refs

focal_item
  stable item identity, domain type, owner, lifecycle state, source refs

customer_item_relationship
  why this item matters to this customer, current state, goals, constraints

interaction_event
  timestamped customer/client/domain touchpoint with evidence refs

journey_state_snapshot
  current inferred state, confidence, inputs, and review status

prediction
  expected next state, outcome, risk, or opportunity with confidence and horizon

intervention_plan
  approved action, owner, constraints, intended effect, and rollback/escalation

outcome_observation
  measured result, evidence, comparison to prediction, and learning decision
```

These records form a loop:

```text
observe interaction
  -> update customer-item relationship
  -> infer journey state
  -> predict likely outcome or next need
  -> propose intervention
  -> route through client and domain approval gates
  -> execute through xFactory / Omnigent
  -> observe outcome
  -> update customer, client, and domain memory according to promotion rules
```

### Layer Ownership

Customer Hermes owns the private customer-item relationship from the customer's
point of view. It records preferences, constraints, consent, history, and what
the customer appears to need next.

Client Hermes owns the operating relationship from the client organization's
point of view. It records what the client is allowed to do, which customer
relationship exists, which systems can be used, and which interventions fit the
client's service model.

Domain Hermes owns the reusable lifecycle model. It defines allowed focal item
types, journey states, outcome measures, prediction standards, intervention
classes, evidence requirements, and review gates.

xFactory / openxFactory owns the contract shape that connects these records to
jobs, gates, traceability, reviews, predictions, interventions, and observed
outcomes.

Domain Omnigent executes approved modeling and intervention work. It may infer,
simulate, recommend, generate, test, or package outputs, and it may request
bounded expert context through xFactory. It does not own the customer truth,
client authority, reusable domain truth, domain policy, expert DB mutation, or
final outcome claim.

### Customer Hermes Owns

- customer-specific identity and context
- consent and authorization
- private memory
- active customer state
- customer-item relationships
- interaction history
- journey state snapshots
- customer-level predictions and outcome observations
- user-facing communication
- preferences and goals
- customer timeline
- customer-specific team assignment
- customer-specific data-sharing decisions

### Client Hermes Owns

- client organization identity and profile
- tenant configuration and isolation
- staff, teams, locations, and operating hours
- client-specific integrations and credentials references
- client policy overrides within domain limits
- client customer roster and relationship metadata
- client-side interaction history
- approved intervention catalog and operating constraints
- client-level outcome reporting
- client-specific memory and operating history
- local approvals, escalations, and communication preferences
- customer onboarding and offboarding rules

### Domain Hermes Owns

- domain policy
- domain agent groups
- domain routing
- domain playbooks
- domain quality gates
- focal item types and lifecycle states
- journey models and outcome taxonomies
- prediction and intervention standards
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
  https://github.com/opensoft/MedxFactory

opensoft/OpsxFactory
  IT operations, sysops, devops, identity, infrastructure, and tenant administration domain stack
  https://github.com/opensoft/OpsxFactory

opensoft/LedgerxFactory
  accounting, finance, and ledger domain stack
  https://github.com/opensoft/LedgerxFactory

opensoft/AdxFactory
  marketing, advertising, growth, and campaign domain stack
  https://github.com/opensoft/AdxFactory

opensoft/codexFactory
  software, code, repo, and engineering domain stack
  https://github.com/opensoft/codexFactory
```

Each domain stack repo defines one productized domain factory. It may contain
multiple deployment profiles, such as clinic, group practice, hospital,
pharmacy, agency, bookkeeping firm, or software team.

The deployment profile should not become a separate repo unless it has a
separate product lifecycle, release process, compliance boundary, or sales
motion.

Tenant deployments are instantiated from a domain stack repo. A tenant may be a
clinic, hospital, pharmacy, marketing agency, accounting firm, or software
team. The tenant is represented by the client Hermes layer. It owns
client-specific configuration and isolation, while the domain stack repo owns
the reusable product definition.

```text
opensoft/MedxFactory
  -> clinic profile
    -> tenant deployment for Clinic A
      -> Clinic Hermes for Clinic A
      -> Patient Hermes for Patient 001
      -> Patient Hermes for Patient 002

  -> hospital profile
    -> tenant deployment for Hospital B
      -> Hospital Hermes for Hospital B
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

    client/
      template.yaml
      memory-boundaries.yaml
      policy-overrides.yaml
      integration-boundaries.yaml

    customer/
      template.yaml
      memory-boundaries.yaml
      consent-model.yaml

  omnigent/
    domain-overlay.yaml
    expert-routing/
    validation-checks/
    output-templates/

  credentials/
    README.md
    requirements.yaml
    bindings.template.yaml
    grants.template.yaml
    audit.yaml
    policies/
      approval-policy.yaml
      rotation-policy.yaml
      revocation-policy.yaml

  tenants/
    README.md
    examples/
```

For MedxFactory, the customer Hermes layer should be named Patient Hermes in
files and manifests because it spans the lifetime of the patient, not a single
case, referral, visit, or claim. The client Hermes layer should be named for the
operator profile, such as Clinic Hermes, Hospital Hermes, Pharmacy Hermes, or
IDTF Hermes.

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

    clinic/
      template.yaml
      memory-boundaries.yaml
      policy-overrides.yaml
      integration-boundaries.yaml

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
  -> Clinic Hermes
  -> Medx Domain Hermes
  -> xFactory / openxFactory
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

Clinic Hermes answers:

- Which clinic, tenant, staff, and operating profile applies?
- Which local systems and integrations may be used?
- Which clinic-specific policies, schedules, forms, and communication rules apply?
- Which patients belong to this clinic context?
- Which local approval or escalation path applies?
- Which information may be shared beyond the clinic boundary?

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

The three Hermes layers support three routing modes.

### Standing Client-Approved Route

```text
Customer Hermes
  -> Client Hermes
  -> xFactory / openxFactory
  -> Domain Omnigent
```

Use this when the workflow is already approved, bounded, repeatable, and low
risk under both domain policy and the client's standing approval envelope.

Example:

```text
Patient Hermes requests a standard follow-up packet for Clinic A. Clinic Hermes
confirms the patient relationship, communication policy, and standing approval
before the request enters xFactory.
```

### Domain-Mediated Route

```text
Customer Hermes
  -> Client Hermes
  -> Domain Hermes
  -> xFactory / openxFactory
  -> Domain Omnigent
```

Use this when domain judgment, triage, policy selection, specialty selection,
or approval is needed before execution.

Example:

```text
Patient Hermes asks for evaluation of a new symptom cluster. Clinic Hermes
confirms the clinic context and patient relationship. Medx Domain Hermes selects
the correct medical workflow, agents, gates, and escalation path before creating
the xFactory job.
```

### Escalated Domain Route

```text
Customer Hermes
  -> Client Hermes
  -> Domain Hermes
  -> client, domain, or human review
  -> xFactory / openxFactory
  -> Domain Omnigent
```

Use this when the request is high-risk, ambiguous, regulated, externally
visible, or outside a standing approval envelope.

Example:

```text
Patient Hermes requests an action that may affect care decisions. Clinic Hermes
requires local review, and Medx Domain Hermes requires domain review and
explicit approval before execution.
```

## Learning and Memory Boundaries

Customer-specific data must not automatically mutate client memory, domain
memory, or shared domain experts.

```text
Customer memory
  private, customer-specific, consent-bound

Client memory
  tenant-scoped, customer-aware, organization-specific

Domain memory
  shared, reviewed, de-identified when required, reusable across clients and
  customers

Base memory
  runtime and operational memory that is not domain expertise
```

Allowed promotion path:

```text
customer observation
  -> customer Hermes records private context
  -> client Hermes reviews tenant relevance and authorization
  -> domain Hermes reviews whether the lesson is reusable
  -> privacy, consent, and de-identification checks pass
  -> domain memory update is approved
  -> domain Hermes or domain Omnigent overlay is updated
```

Disallowed shortcut:

```text
patient data
  -> directly changes Clinic Hermes, Medx Domain Hermes, or shared Medx experts
```

Domain experts should get better in their domain, but not by silently absorbing
private customer data.

## External Source Workspaces

Domain factories may use external source workspaces such as NotebookLM to gather,
summarize, compare, and discuss source material. These workspaces are mediated
source surfaces, not ground truth by themselves.

The generic rule is:

```text
external source workspace output
  -> source trace
  -> ground source verification when required
  -> Hermes review
  -> memory, policy, workflow, or agent use
```

NotebookLM workspaces may attach to any Hermes layer or to an approved domain
agent task:

- Customer Hermes may use customer-scoped notebooks for private customer context.
- Client Hermes may use client-scoped notebooks for tenant policies, SOPs,
  integrations, staff credentials, coverage, and local operating sources.
- Domain Hermes may use domain-scoped notebooks for reusable research,
  regulations, standards, playbooks, and root truth corpus exploration.
- Domain agents may use task-scoped notebooks as job context under the owning
  Hermes layer's approval and source policy.

Every workspace-derived claim must carry a source authority level:

```text
L0 unverified_note
L1 notebook_synthesis
L2 notebook_cited_source
L3 ground_source_verified
L4 hermes_reviewed_truth
L5 operational_policy
```

NotebookLM output defaults to `L1`. Citations to notebook sources may support
`L2`. A claim reaches `L3` only when the original article, regulation, chart,
policy, document, or other ground source is recorded and checked. It reaches
`L4` or `L5` only after the relevant Hermes layer accepts it.

The required trace chain is:

```text
claim
  -> NotebookLM output or note
  -> notebook workspace
  -> notebook source
  -> original ground source
  -> cited passage, page, section, timestamp, or document-level citation
  -> verification record
  -> Hermes review decision
  -> consuming memory, policy, workflow, or agent artifact
```

If a notebook citation points only to an entire source, the trace must record
that document-level citation. If the consuming workflow requires precise
support, the verifier must add page, section, passage, timestamp, or equivalent
location metadata before the claim can be promoted.

See [NotebookLM Source Workspaces](notebooklm-source-workspaces.md).

## Domain Omnigent Overlays

Base Omnigent provides the general agent harness and execution substrate.

Domain Omnigent overlays tune that substrate for domain execution.

A domain Omnigent overlay owns:

- domain expert agent mappings
- domain task decomposition rules
- expert context packet requirements
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

Expert memory follows that same rule. Domain Omnigent can use external expert
memory and knowledge DBs only through xFactory-governed context packets or
approved gateway operations. xFactory maintains the expert provider bindings,
route tables, source-authority rails, usage events, migration manifests, and
audit records. Domain Hermes remains the owner of reusable expert truth and
review standards.

## Factory Contract Boundary

xFactory / openxFactory owns general contract fields such as:

- job identity
- customer reference
- client reference
- domain reference
- focal item references
- customer-item relationship references
- interaction event references
- journey state references
- prediction, intervention, and outcome references
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

- focal item type catalogs
- domain journey state machines
- outcome measure definitions
- specialty routing
- domain policy references
- domain review council membership
- domain evidence requirements
- domain tool permissions
- domain data-source permissions
- domain-specific risk labels
- domain-specific output formats

Client overlays own client-specific fields such as:

- client identifier
- tenant profile
- client Hermes reference
- customer roster references
- client policy references
- integration references
- staff or team routing references
- approved intervention references
- local approval references
- client memory references

Customer overlays own customer-specific fields such as:

- customer identifier
- focal item relationship references
- interaction history references
- journey state snapshot references
- prediction and outcome observation references
- consent references
- private context references
- customer timeline references
- customer team assignments
- customer-specific communication preferences

## Suggested Job Envelope Extension

The generic Hermes job envelope should support factory, domain, client, and
customer metadata without making xFactory domain-specific.

Example:

```yaml
factory:
  schema_version: 1
  factory_kind: MedxFactory
  xfactory_contract: openxFactory
  xfactory_contract_version: "2026-06-27"

domain:
  id: medx
  stack_repo: github.com/opensoft/MedxFactory
  hermes_overlay: hermes/domain
  omnigent_overlay: omnigent
  policy_refs:
    - medx/policies/diagnostic-review.yaml
  review_profile: medx_standard_review

client:
  client_kind: clinic
  client_ref: clinic-hermes://clinics/<clinic-id>
  client_hermes_ref: hermes://clinics/<clinic-id>
  tenant_profile: clinic
  policy_refs:
    - clinic-hermes://clinics/<clinic-id>/policies/current
  integration_refs:
    - clinic-hermes://clinics/<clinic-id>/integrations/ehr

customer:
  customer_kind: patient
  customer_ref: patient-hermes://patients/<patient-id>
  patient_hermes_ref: hermes://patients/<patient-id>
  consent_refs:
    - patient-hermes://patients/<patient-id>/consents/current
  private_context_refs:
    - patient-hermes://patients/<patient-id>/timeline/current

focus:
  focal_items:
    - item_kind: treatment_plan
      item_ref: medx://treatments/<treatment-plan-id>
      relationship_ref: patient-hermes://patients/<patient-id>/relationships/<relationship-id>
  journey_state_ref: patient-hermes://patients/<patient-id>/journey/current
  outcome_objectives:
    - reduce_readmission_risk
    - improve_treatment_adherence
  prediction_refs:
    - patient-hermes://patients/<patient-id>/predictions/<prediction-id>
  intervention_refs:
    - clinic-hermes://clinics/<clinic-id>/interventions/<intervention-id>

routing:
  requested_by: patient_hermes
  client_approved_by: clinic_hermes
  domain_approved_by: medx_domain_hermes
  route_mode: domain_mediated
```

The xFactory layer validates that these fields exist and are internally
consistent. The domain factory validates whether the referenced policies,
consents, tools, and experts are appropriate for the requested work.

## Repository Ownership

Recommended ownership:

```text
openxFactory
  canonical xFactory contracts and general workflow policy

Hermes-Install
  reusable Hermes installation, restore, runtime wiring, and profile loading

Agents/<Domain>
  domain Hermes roster, identity references, profile metadata, and overlays

omnigent
  base Omnigent runtime and harness

opensoft/<Domain>Factory
  productized domain stack with Hermes and Omnigent overlays

customer registries
  private customer Hermes overlays and customer-specific memory references
```

Recommended workstation layout:

```text
/home/brett/projects/xFactory/
  README.md
  MedxFactory/
  OpsxFactory/
  LedgerxFactory/
  AdxFactory/
  codexFactory/
```

The domain stack repo may reference existing agent registries, such as
`Agents/Medx`, `Agents/LedgerX`, or `Agents/Opensoft`, but the sellable stack
definition belongs in the domain factory repo.

## Design Rules

1. xFactory is domain-neutral.
2. Domain factories are overlays, not forks.
3. Customer Hermes, client Hermes, and domain Hermes are separate authority layers.
4. Customer data remains customer-bound unless explicitly promoted.
5. Domain learning requires review, approval, and privacy checks.
6. Hermes approves intent and policy.
7. Omnigent executes approved work.
8. openxFactory defines the handoff contract.
9. Domain overlays may add gates, but must not bypass base xFactory gates.
10. Direct customer-to-factory routing is allowed only inside standing client
    and domain approval envelopes.
