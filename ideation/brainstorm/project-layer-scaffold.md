# Project/Customer (Subject) Layer Scaffold: the subject, its deciders, and provisioning from a type — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Scaffolds the Customer/Project ("the subject") Hermes layer. It is
subject-centric — it owns the project's identity, scope and feature initiatives,
acceptance criteria, consent, private memory, and journey state — so its Plane-1
roster is small (Product Owner + Project Manager) and most of its substance is
the *subject content* plus the **project-type template** it is provisioned from.
Third distinct composition pattern: domain is authored-once, client is
per-client wizard-tuned, project is **per-project instantiated from an archetype**
(the type-template library, filled in `project-type-template-library-draft.md`).
The documentation help/manual writer lands here as a Plane-2 worker. Parent:
`hermes-layer-content-seeding.md`.
Topics: project-hermes, customer-hermes, subject, project-layer, product-owner,
project-manager, project-type-template, provisioning, consent, journey-state,
manual-writer, plane-1
Repository context: openxFactory (targets codexFactory hermes/subject|customer/ + hermes-install provision-project)
Captured: 2026-07-21

## Possible feats

- **Subject content model** filled (`identity, scope, acceptance, consent,
  memory, journey`).
- **Plane-1 project roster** (Product Owner + Project Manager).
- **Project-type template library** (separate doc).
- **`provision-project` archetype selection** + project-specific tuning.

## Subject-centric, not authority-heavy

The README defines this layer as *the subject*: for codex, a software project /
repository / product / feature initiative. It owns identity, consent, private
memory, and journey state, plus (from codex's client `must_not_own`) project
scope, feature initiatives, and acceptance criteria. So unlike the domain
(expert authority) and the client (operating policy), the project layer is
mostly *about a thing*, and needs only a small decider roster over rich subject
content.

## Composition (third pattern)

- **Neutral subject shape** — codex `hermes/subject/template.yaml`
  (`subject_kinds: [project, repository, product, feature_initiative]`,
  required subject fields). Naming skew flagged: prescribed shape says
  `hermes/customer/`; codex ships `hermes/subject/` — reconcile.
- **Domain specialization** — the subject template + a project-type library.
- **Project-type template (archetype)** — the big distinctive piece: a
  microservice, library, CLI, app, infra, or spike each want different default
  policy, practices, workflows, and consent (`project-type-template-library-draft.md`).
- **Project instance** — `provision-project` picks an archetype, materializes a
  Customer layer, then tunes it to *this* project (the repo, its branch-protection
  state, its team). opensoft already has `project-alfa` / `project-bravo` as
  Customer-layer instances.

## The plane split for the project layer

- **Plane 1 — project deciders (small): Product Owner + Project Manager** (below).
- **Plane 2 — project workers (Omnigent):** including the **documentation
  help/manual writer** (produces the project's user-facing manuals/help —
  distinct from the domain's `documentation_agent`, which verifies doc/traceability
  changes), plus project-specialized workers the archetype pulls in.
- **Plane 3 — advisory:** rare at project scope.

## Subject content model

```yaml
subject:
  identity: {kind: repository|product|feature_initiative, ref, display_name}
  scope: {feature_initiatives: [...], out_of_scope: [...]}      # PO owns
  acceptance_criteria: [...]                                     # PO owns; definition of done
  consent_model: {...}                                          # gateway consent; per-query recall path in subject-recall-and-consent-path.md
  private_memory: {scope: subject_private, promotes_via: domain_learning_candidates}
  journey_state: intent_received | ... | merge_ready | blocked  # the domain workflow sequence
```

## Plane-1 roster — domain-specific, NOT neutral

Unlike the client house team (neutral — operating orgs are alike), the
subject-layer roster is **domain-specific**, because the subject itself is what
most distinguishes domains: it ranges from a **person with rights** (a Medx
patient) to an **inert artifact** (a codex repo), and the roles a subject needs
depend on what *kind* of thing it is. So Product Owner / Project Manager are
**codex fillings**, not neutral roles — a MedxFactory subject would be served by
a Patient Advocate + Care Coordinator, which do not map cleanly onto PO/PM.

At most there is a *loose* neutral **functional skeleton** each domain fills
natively, and even the prominence of each slot varies:

| Neutral function | codex | Medx |
| --- | --- | --- |
| intent/value owner (what the subject is for; acceptance) | Product Owner | care-goal owner (care team) |
| journey coordinator (its progression/lifecycle) | Project Manager | Care Coordinator |
| rights & consent advocate (its interests) | *light — repo owner* | **Patient Advocate** (central) |

The rights/consent-advocate slot is near-empty in codex (a repo has no interests
to advocate for) and central in Medx (a patient does) — which is exactly why the
subject layer resists neutralization. Cast-coherence is a per-domain call;
codex's PO/PM are drafted independent.

### Product Owner — `PO` *(flagship, prose)*

```yaml
persona:
  id: product-owner
  role_code: PO
  layer: customer_project
  authority:
    owns: [scope, feature_initiatives, acceptance_criteria, priorities]
    decides: [what_and_why, done_ness]
    escalates: [{trigger: scope_vs_capacity_conflict, to: project-manager}]
  disposition: {rigor: moderate, risk_posture: neutral, bias: balanced, autonomy: high}
  voice: {warmth: moderate, verbosity: moderate, formality: low_moderate, proactivity: high}
```

**Character frame.** You own the *why* — the value this project is meant to
deliver and what "done" means for it. You translate customer need into crisp
acceptance criteria and you guard the scope line hard: you say no to gold-plating
and yes to the smallest thing that delivers the value. You never let the domain's
"how" pull the "what" around, and you never let acceptance be implied — if it
isn't written, it isn't done.

### Project Manager — `PM` *(flagship, prose)*

```yaml
persona:
  id: project-manager
  role_code: PM
  layer: customer_project
  authority:
    owns: [project_schedule, coordination, blocker_tracking]
    decides: [sequencing, commitment_dates]
    escalates: [{trigger: delivery_risk, to: client:delivery-sla-lead}]   # cross-layer to client
  disposition: {rigor: moderate, risk_posture: averse, bias: balanced, autonomy: moderate}
  voice: {warmth: moderate_high, verbosity: terse, formality: low, proactivity: high}
```

**Character frame.** You keep *this* project moving — the plan, the sequence, the
blockers surfaced early rather than explained late. You coordinate across the
domain deciders and the project team, but you own delivery for one project, not
the operating org's SLAs. Terse and reliable; a risk you see is a risk you raise.

**Three-layer coordination boundary (worth stating):** the domain **Scrum
Coordinator** owns process/cadence in general; the project **Project Manager**
owns this project's plan and delivery; the client **Delivery & SLA Lead** owns
capacity/SLA across the whole operating org. PM escalates delivery risk *up* to
the client's Delivery & SLA Lead.

## Provisioning flow

`provision-project <ref> --type <archetype>` → materialize a Customer layer from
the archetype → tune to the project (repo, branch-protection state, team) →
register into the stack. Today's `*.params.yaml` project entry (`layer_id`,
`display_name`, `project_ref`, `policy_namespace`, `overlay`) is the structural
half; the archetype is the content half.

## The scaffold, listed

```text
PROJECT/CUSTOMER (SUBJECT) LAYER
├── Composition
│   ├── neutral subject shape (codex hermes/subject/template.yaml)
│   ├── project-type template (archetype)      → project-type-template-library-draft.md
│   └── project instance (provision-project + tuning; opensoft alfa/bravo)
├── Plane 1 — project deciders
│   ├── Product Owner (what/why, acceptance)
│   └── Project Manager (schedule, delivery)
├── Plane 2 — project workers (Omnigent)
│   ├── documentation help/manual writer
│   └── archetype-pulled workers
├── Subject content
│   ├── identity · scope · acceptance_criteria
│   ├── consent_model
│   ├── private_memory (subject-private; promotes via domain_learning_candidates)
│   └── journey_state (domain workflow sequence)
└── File shape (reconcile subject/ vs customer/)
    └── hermes/customer/{template, memory-boundaries, consent-model} + templates/<type>.yaml
```

## Open questions

- **subject/ vs customer/ naming** — reconcile codex `hermes/subject/` with the
  prescribed `hermes/customer/` (the §A1 layer-name hazard).
- **Project cast coherence** — do PO + PM form a coherent pair or stay
  independent? (Only two, so low stakes; left independent.)
- **Consent granularity** — what exactly does a software project *consent* to,
  and how does it differ from a MedxFactory patient's consent (same layer, very
  different subject)?
- **Journey-state ownership** — is journey_state owned by the project layer or a
  projection of the domain workflow engine's state?
