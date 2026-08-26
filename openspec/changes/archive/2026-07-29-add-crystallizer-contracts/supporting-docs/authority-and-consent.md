# Authority Conservation and Consent Tiers

Status: staged
Kind: architecture
Summary: Declares the MODIFIED `omnigent-domain-overlay` delta (a
crystallized-executor profile class inside the existing generalized
permission matrix with the constitutional falses intact, plus per-category
rung-ceiling declarations) and the ADDED `crystallization-consent` contract
(three separately-grantable, default-deny tiers: episode use, automation,
pooling), together with the runtime obligations — mechanical
authority-conservation validation, path-invariant audit shape,
young-capability throttles, and the three-layer approval braid.
Topics: authority-conservation, crystallization-consent, omnigent-domain-overlay,
permission-matrix, credential-contracts, audit-continuity, blast-radius,
rung-ceiling, layer-vocabulary
Repository context: openxFactory (the permission matrix and consent schemas
are neutral; ceilings are domain overlay content)
Staging ID: `openxFactory:staging:recurrence-crystallization`
Source: brainstorm doc
[authority and consent](../../../../../ideation/brainstorm/crystallization-authority-and-consent.md)
(AU-C1..C5, AU-Q1..Q5); braid framing from the
[Crystallizer synthesis](../../../../../ideation/brainstorm/crystallization-synthesis-crystallizer.md);
ruling D11 (effect classes) interacts via the dispatch fragment.
Target capabilities: `omnigent-domain-overlay` (MODIFIED),
`crystallization-consent` (ADDED)

## The MODIFIED delta: omnigent-domain-overlay

- **Crystallized-executor profile class.** Capabilities enter the existing
  generalized permission matrix as a bounded executor class — not a novel
  privilege domain. The constitutional falses (`execute_final_action`,
  `access_secrets`) persist at every rung including L6 (AU-C1).
- **Authority conservation is mechanical.** A capability's permission
  binding MUST be a subset of the effective permissions of the AI
  configuration whose work it absorbs, checked by a validator, not by
  judgment. Widening scope happens only via ordinary role-change governance
  on the *replaced configuration* — never as a side effect of
  crystallizing.
- **Rung-ceiling declarations.** Domain overlays declare `rung_ceiling`
  per task category with reasons (AU-C5) — the regulatory posture (e.g.
  Medx SaMD-adjacent caution) lives in the overlay, never in neutral
  defaults.
- Credentials ride `credential-contracts` unchanged (grant/binding
  templates, short-lived grants); generated code holds no secrets, exactly
  like workers. External enforcement remains the final backstop.

## The ADDED contract: crystallization-consent

Three tiers, separately grantable, default deny (AU-C2):

| Tier | Grants | Scope |
| --- | --- | --- |
| T1 episode use | mining this tenant's solved runs into families, forecasts, corpora | per tenant |
| T2 automation | serving a family category without fresh AI judgment | per family category |
| T3 pooling | de-identified evidence aggregating cross-tenant | per tenant; **defined now, unused this wave** |

Where the work is subject-affecting, provenance is subject-visible and the
subject consent path applies. A T2 grant MAY carry a human-spot-check
condition (AU-Q4, carried as a design option for the OpenSpec round).

## Runtime obligations

- **Audit-shape parity** (AU-C3): run records have the same shape on
  either path; provenance is the only difference an auditor sees, and the
  lineage chain run → capability → spec → corpus → episodes → original runs
  resolves without a seam.
- **Correlated-failure throttles** (AU-C4): deterministic bugs fail at
  scale, so young capabilities carry rate/output/spend caps that relax
  only with tenure and proof freshness (schedule in the dials register);
  an incident auto-demotes and files the counterexample into the corpus.
- **The approval braid** (SYB-C3): Domain approves fitness (spec,
  corpus adequacy, ceiling), Tenant approves money and policy (budget,
  T1/T2/T3, clearance), Subject sees provenance and consents where
  affected. No single layer can push a capability into authority alone.

## Open questions carried

Binding signature mapping onto `roles-authority-model` — domain Lead
proposes, tenant authority countersigns? (AU-Q2); one executor class or one
per rung band, since playbooks and programs have different failure physics
(AU-Q3); the automated-decision legal review per domain and jurisdiction,
Medx first (AU-Q1); throttle schedule ownership — neutral table vs wholly
domain policy (AU-Q5, staged default in the dials register).
