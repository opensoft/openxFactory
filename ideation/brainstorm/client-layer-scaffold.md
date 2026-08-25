# Client (Company Policy) Layer Scaffold: structure, planes, and the per-client tuning path — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Scaffolds the Client ("Company Policy") Hermes layer and lists the
skeleton before filling it. Unlike the domain layer (authored once, identical
for every install), the client layer is **per-client and wizard-loaded**: a
neutral scaffold (`product-service-scaffold.yaml`, exists) is specialized by the
domain (`hermes/client/template.yaml`, exists) and then *tuned* by a policy
wizard into each client's tree (`config/clients/<client>/`). Applies the plane
model: the **house-team deciders** (Plane 1, the Company Policy authority) are
distinct from the **18 steward workers** (Plane 2, Omnigent), with a coherent
house style (the deliberate contrast to the domain's independent personas).
Parent: `hermes-layer-content-seeding.md`; roster filled in
`client-layer-roster-draft.md`.
Topics: client, client-hermes, company-policy, client-layer, scaffold, house-team,
per-client, policy-wizard, client-infrastructure-liaison, offer-shapes,
plane-1, plane-2, layer-content-seeding
Repository context: openxFactory (targets openxFactory client-layer template + codexFactory hermes/client/ + hermes-install config/clients/)
Captured: 2026-07-21

Updated: 2026-07-22 (roles/ + facts-rule + liaison decisions; seeding path synced; steward table + accounting gap)

## Decided (2026-07-22)

- **`roles/` is added to the client shape.** The house team gets a `roles/`
  dir by domain analogy; the prescribed model doc
  (`xfactory-domain-factory-model.md`) is updated to include it — the same
  reconciliation pass that renames `customer/` → `subject/` (umbrella
  §Decided).
- **The facts rule (domain-default vs. wizard-only).** A policy value may be a
  domain default iff it is justifiable for *any* engineering organization;
  anything naming a **client-specific fact** (a person, a system, a ceiling
  value) is wizard-only, always. Domain defaults are suggestions the wizard
  confirms — never pre-filled client facts.
- **The liaison is a convened capability, not a member.** It is composed from
  stewards, `configured_but_inactive`, never standing — the house team
  *activates* it through its gate; it holds no seat. Plane 1 is therefore
  **9 deciders + 1 convened capability**, not 10 members.
- **How client content seeds — decided with the mechanism doc:** the wizard's
  output is committed as a per-client overlay document that seeds through the
  SAME pipeline (pin → digest verify → validate → split). Still open there:
  where the wizard-written overlay's digest pin is recorded and who signs it.

## Possible feats

- **Client-layer file shape** filled (`hermes/client/{roles/, policy-overrides,
  memory-boundaries, integration-boundaries}`).
- **The policy wizard** that turns scaffold blanks into a client's tree.
- **Plane-1 house-team roster** (see roster draft).
- **Per-client tuning contract** — what the wizard writes and how it re-tunes.

## How the client layer is composed (three tiers)

The client layer is assembled by overlay, not authored once:

1. **Neutral scaffold** — `openxFactory/templates/client-layer/product-service-scaffold.yaml`
   (draft). Domain-neutral: offer shapes, client objects, 18 steward agents,
   skills, UI surfaces, starter workflows, memory buckets, the composed Client
   Infrastructure Liaison — **and the Plane-1 house-team roster itself** (added).
   The house-team functions (policy, approvals, legal, reputation, liability,
   security, integrations, delivery, customer) are universal to *any* operating
   organization, so the roster is neutral, not codex-specific. Structure and role
   *labels*, no policy *text*.
2. **Domain specialization** — `codexFactory/hermes/client/template.yaml`
   (`Engineering Organization Hermes`, exists). Sets what an engineering-org
   client owns (org identity, reviewer groups, repo-access policy, CI
   conventions, integration inventory, credential-binding refs) and must not own
   (project scope → Project Hermes; decomposition/admission → Domain Hermes;
   gates/audit → xFactory; final merge → repo).
3. **Client tuning (the wizard)** — turns the scaffold's governance-shaped blanks
   into *this* client's real policy set, written to `config/clients/<client>/`
   (opensoft already has this tree). This is where the client's actual repo
   boundaries, approvers, spend ceilings, security posture, and escalation path
   land — and where the auto-clear envelope for the clearance pipeline is defined.

**The key contrast with the domain:** domain content is install-invariant
(same for every codexFactory install); client content is **per-client**, and
most of its substance arrives at tuning time, not authoring time. An un-tuned
client is safe but fully manual (everything parks for the human liaison).

## The plane split for the client layer

Same discipline as the domain:

- **Plane 1 — house-team deciders (Company Policy authority).** The personas that
  decide "is this allowed *here*?" — filled in the roster draft. **Neutral
  scaffold roles** (every operating org), domain-*specialized* and client-*tuned*,
  sharing a coherent **house style** per the cast-coherence decision.
- **Plane 2 — steward workers.** The 18 `agent_scaffold` stewards
  (`client_profile_steward`, `policy_approval_gatekeeper`, …) — execution/steward
  agents that belong to the client's **Omnigent** plane, directed by the Plane-1
  house team. Not Hermes deciders; kept separate.
- **Plane 3 — advisory.** MoA mixes as needed (e.g. a policy panel for a
  contested clearance), same profile-in-Hermes / execution-in-Omnigent seam.

## The object model (from the neutral scaffold)

- **7 offer shapes**: product, service, productized_service, subscription,
  managed_service, marketplace_offer, outcome_based_offer.
- **11 client-layer objects**: client_profile, offer_catalog, customer_roster,
  operating_policy, integration_map, staff_capability_map, approval_matrix,
  escalation_map, communication_policy, outcome_dashboard,
  client_infrastructure_liaison.
- **4 memory buckets**: client_private_memory, customer_relationship_memory,
  domain_learning_candidates, current_state_evidence.
- **Client Infrastructure Liaison**: a *composed* coordination profile (from
  seven stewards), `configured_but_inactive` by default, with an activation gate
  — never a standing agent, never holds tenant authority, never stores secrets.

## Physical file shape

Prescribed client shape (`xfactory-domain-factory-model.md`) is `hermes/client/
{template.yaml, memory-boundaries.yaml, policy-overrides.yaml,
integration-boundaries.yaml}`. To hold the Plane-1 house team, this scaffold adds
a `roles/` dir by analogy to the domain (flag: the prescribed client shape omits
`roles/` — reconcile). Per-client instances live in the install, not the domain repo:

```text
openxFactory/templates/client-layer/    # NEUTRAL — every client, all domains
  product-service-scaffold.yaml   # exists — gains the house-team roster (roles/)
  roles/                          # NEW (neutral) — the house-team persona defaults + house_style

codexFactory/hermes/client/       # domain SPECIALIZATION only (overrides the neutral roster)
  template.yaml                   # exists — Engineering Organization Hermes
  role-overrides.yaml             # NEW — engineering-specific tuning of neutral roles
  policy-overrides.yaml           # NEW — domain-suggested client policy defaults
  memory-boundaries.yaml          # NEW — org memory scope (per_tenant)
  integration-boundaries.yaml     # NEW — allowed integration classes

hermes-install/config/clients/<client>/   # per-client, wizard-loaded (opensoft exists)
  client-profile.yaml             # exists
  operating-policy.yaml           # NEW (wizard) — the client's real policy set
  approval-matrix.yaml            # NEW (wizard) — approvers + auto-clear envelope
  integration-map.yaml            # NEW (wizard) — this client's systems + credential bindings
  ...                             # liaison, readiness, grants, etc. (exist)
```

## The policy wizard

Guided elicitation that fills the client tree from the scaffold blanks:
repo-boundary policy, credential posture, spend ceilings, security posture,
named approvers, escalation path — and the **auto-clear envelope** (the "likely
yes" middle for the clearance pipeline). Conservative defaults: until a policy
is set, everything parks for the human liaison, so an un-tuned client is safe.
Re-running the wizard is idempotent re-tuning; the liaison's accreted
dispositions are candidate inputs for the next pass.

**The facts rule (decided, §Decided) governs every wizard question:** if the
answer would be true for any engineering organization, it belongs in the
domain's `hermes/client/policy-overrides.yaml` as a default the wizard merely
confirms; the moment an answer names a client-specific fact — an approver, a
system, a spend number — it is wizard-only and lives exclusively in
`config/clients/<client>/`.

## Steward direction (Plane 1 → Plane 2) and the accounting gap

Count correction: the neutral scaffold defines **19** steward agents, not 18.
Draft direction map (mirrors the domain's worker-coverage table; the stewards
live in a **client Omnigent overlay — to be created**, with the same
bidirectional seed-checked references and the same clock-in duty from
`cost-accountability-and-efficiency-model.md`):

| House-team decider | Directs (stewards) |
| --- | --- |
| Company Policy Lead | policy_approval_gatekeeper, workflow_definition_agent, practice_gap_auditor, client_profile_steward |
| Change Approvals Authority | policy_approval_gatekeeper (approval-packet leg) |
| Legal & Compliance Counsel | consent_adoption_gatekeeper, client_memory_steward |
| Reputation & Brand Steward | — none; **undirected by design or a steward gap — verify** |
| Product Liability & Insurance Officer | exception_dispute_agent |
| Client Security & Compliance Officer | integration_credential_steward (posture leg) |
| Integrations & Credentials Steward | integration_credential_steward, source_inventory_agent, migration_planner_agent |
| Delivery & SLA Lead | fulfillment_delivery_coordinator, intake_and_triage_agent, configure_quote_scope_agent, staff_capability_routing_agent, quality_outcome_monitor, offer_catalog_steward? |
| Customer & Communications Lead | customer_relationship_steward, communication_handoff_agent, renewal_expansion_retention_agent |

**The accounting gap (finding, 2026-07-22):** the cost-accountability model
requires the tenant layer to run **reporting-to-accounting** (company-wide
cost tracking) and to **set the tracking granularity the subject layer must
honor** — and *no* house-team persona or steward owns that today. Candidates:
a new **Finance & Accounting Officer** persona (+ a `cost_reporting_steward`
worker), or growing Delivery & SLA Lead's scope. Carried to
`client-layer-roster-draft.md` as a roster-gap item.

## The scaffold, listed

```text
CLIENT (COMPANY POLICY) LAYER
├── Composition
│   ├── neutral scaffold (openxFactory, exists)
│   ├── domain specialization (codexFactory hermes/client/template.yaml, exists)
│   └── client tuning (wizard → config/clients/<client>/)
├── Plane 1 — house-team deciders (Hermes, 10)  → client-layer-roster-draft.md
│   ├── Policy core:    Company Policy Lead · Change Approvals Authority
│   ├── Risk & Assurance: Legal & Compliance Counsel · Reputation & Brand Steward · Product Liability & Insurance Officer
│   ├── Security:       Client Security & Compliance Officer
│   ├── Ops:            Integrations & Credentials Steward · Client Infrastructure Liaison (composed, inactive) · Delivery & SLA Lead
│   └── Customer:       Customer & Communications Lead
├── Plane 2 — 18 steward workers (Omnigent)
│   └── client_profile_steward … consent_adoption_gatekeeper
├── Objects
│   ├── 7 offer shapes
│   ├── 11 client-layer objects
│   └── 4 memory buckets
├── Content files (to fill)
│   ├── roles/                    (house team — filling now)
│   ├── policy-overrides.yaml     (domain defaults + wizard)
│   ├── memory-boundaries.yaml    (per_tenant org memory)
│   └── integration-boundaries.yaml
└── Per-client tree (wizard-loaded)
    └── config/clients/<client>/  (operating-policy, approval-matrix, integration-map, …)
```

## Open questions

- ~~**`roles/` vs. prescribed shape**~~ — DECIDED 2026-07-22: add `roles/`;
  update the prescribed model doc in the same pass as the `subject/` rename
  (§Decided).
- ~~**Domain-default vs. client-tuned split**~~ — DECIDED 2026-07-22: the
  facts rule (§Decided).
- **Steward-worker home** — the direction table assumes a **client Omnigent
  overlay** (like the domain workers); that overlay does not exist yet and is
  a prerequisite for the stewards being real. Also: scaffold count is 19, not
  18 — reconcile the label.
- ~~**Liaison as persona vs. profile**~~ — DECIDED 2026-07-22: convened
  capability, not a member; Plane 1 = 9 deciders + 1 capability (§Decided).
- ~~**How client content seeds**~~ — DECIDED 2026-07-22 with
  `hermes-layer-seeding-mechanism.md`: unified — the wizard commits a
  per-client overlay that seeds through the same pipeline (§Decided).
- ~~**The accounting gap**~~ — DECIDED 2026-07-22: a new **Finance &
  Accounting Officer** persona + `cost_reporting_steward` worker (drafted in
  `client-layer-roster-draft.md` §11); the steward must be added to the
  neutral scaffold's roster.
- **Reputation & Brand Steward's hands** — the only decider with no directed
  steward; confirm undirected-by-design or add a steward.
