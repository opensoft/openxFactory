---
code_surface: openxFactory (scripts/validate-client-infrastructure.py + the two contract schemas, packaged examples, and the client-layer scaffold template; domain-repo adoptions are successor changes per the impact map)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
Status: ratified
Ratified: 2026-07-16 by Brett — record: this change's own tasks.md 4.1, under its "## 4. Ratification gate" heading — "[GATE] Product-owner sign-off on D1 ... and D5 ... recorded here before the specs are treated as settled. — SIGNED OFF by Brett, 2026-07-16, item-by-item", ticked, and closing with the decisive clause the same line records: "Governing doc flipped to `Status: ratified` + `Ratified by: add-client-infrastructure-liaison` at this gate" — `docs/client-infrastructure-liaison.md` carries exactly that header today, verified against the live file; the archive act followed on 2026-07-17 in `3a66fc5`, "Archive add-client-infrastructure-liaison (5.2); promote capabilities", which promoted `openspec/specs/client-infrastructure-liaison/spec.md` and `openspec/specs/client-infrastructure-request/spec.md` and updated `openspec/specs/roles-authority-model/spec.md`. The date recorded is the sign-off's, which is one day before the archive folder's. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".
---

# Proposal: add-client-infrastructure-liaison

## Why

Every DomainxFactory install depends on infrastructure someone else controls
— a customer's own tenant, a contracted managed host, or a purchased
OpsxFactory instance — and today there is no neutral way to coordinate such a
dependency without either granting domain agents tenant-administration
authority (forbidden) or losing the dependency in untracked email/tickets.
The github-administration-plane work (ratified 2026-07-14/15) deliberately
scoped itself to Opensoft's own vendor org and named this topic as the route
for all client-tenant execution; its prerequisite
(`refine-opsx-service-subject-model`, archived 2026-07-10) is satisfied. The
staging topic is marked Ready to propose with its design decisions locked.

## What Changes

- **Adds the Client Infrastructure Liaison** — a neutral Client Hermes
  coordination profile (one accountable owner, composed from existing Client
  Hermes roles, present in every Client Hermes scaffold, domain display
  aliases resolving to the same neutral contract). Coordination only: the
  liaison never holds tenant-administration authority, never executes
  privileged change, never stores secrets, and never bypasses client
  approval or an OpsxFactory gate.
- **Adds the `client_infrastructure_request` contract** — a durable
  coordination record (distinct from the neutral job envelope) with six
  distinct identity-reference classes, three execution bindings
  (client-managed / managed-host / full-OpsxFactory), a closed lifecycle
  with an authorized-actor transition matrix, orthogonal conditions (never
  states), an OpsxFactory handoff/acceptance record, and completion gated on
  a fresh passing `infrastructure_readiness_result`.
- **Ships the contract family** (document-cataloging shape): two JSON-Schema
  files under `contracts/schemas/`, a governing invariants doc under
  `docs/`, valid + one-violation-each negative examples under `examples/`,
  and `scripts/validate-client-infrastructure.py` enforcing what schema
  cannot (transition legality, embedded-secret rejection, actor/authority
  separation, completed-requires-fresh-readiness). Instance records live in
  client installs (credential-contracts residency model); manifest
  registration happens at realization.
- **MODIFIED `roles-authority-model`**: the "GitHub App identity tiers"
  requirement's client-tenant exclusion is closed by routing it here —
  additive amendment plus one appended scenario; all existing text and
  scenarios preserved verbatim.
- **Wires the liaison into the base Client Hermes scaffold**
  (`templates/client-layer/product-service-scaffold.yaml`):
  configured-but-inactive by default, activation-blocking when a declared
  component needs an external operator, with the activation gate (owner,
  authorities, out-of-band path, validation profiles, one exercised
  failure-and-recovery scenario) declared.

## Capabilities

### New Capabilities
- `client-infrastructure-liaison`: the coordination role — ownership,
  composition, authority boundary, the three operating models, the
  activation gate, and bootstrap/out-of-band recovery independence.
- `client-infrastructure-request`: the request artifact — record shape and
  identity classes, lifecycle + transition legality, OpsxFactory handoff
  correlation, readiness-result gating, and deterministic validation.

### Modified Capabilities
- `roles-authority-model`: the "GitHub App identity tiers" requirement —
  its final exclusion sentence is extended so client-tenant infrastructure
  execution routes through the liaison model (additive; one new scenario).

## Impact

- **openxFactory**: +2 schemas (`contracts/schemas/`), +1 governing doc
  (`docs/`), examples (valid + negatives), +1 validator (`scripts/`),
  `templates/client-layer/product-service-scaffold.yaml` extended,
  `contracts/README.md` "Contracts Pending Realization" row now,
  `contracts/manifest.yaml` + CHANGELOG + release digests at realization.
- **Consumes, never renames** OpsxFactory vocabulary: the typed
  actor/capability/authority projection, subject kinds, and the
  `github_administration` workflow/credential names stay OpsxFactory-owned;
  the neutral request maps onto them at the handoff boundary.
- **Successor changes (not here)**: per-domain adoption (OpsxFactory
  execution-binding + readiness producer; Medx "Care Infrastructure
  Liaison" alias + protected-data fallback; Ledger/Ad/codex aliases and
  profiles), per the impact map's sequence.
- **Unblocks**: client-tenant GitHub administration routing (the
  github-administration-plane carve-out), Southside-class operating models
  (customer-managed / managed-host / OpsxFactory-bound), and
  activation-readiness gating for installs that declare external operators.
