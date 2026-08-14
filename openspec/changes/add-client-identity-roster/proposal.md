---
code_surface: openxFactory
target_release: implementation_pending
---
# Proposal: add-client-identity-roster

Status: draft — proposed 2026-08-14; parked at the ratify gate.

## Why

xFactory governs credentials (`credential-contracts`: record shapes, grant
neutrality, SOPS patterns) and governs the authority chain's root
(`consent-instrument`). It does not govern the **identity layer** those
credentials belong to: which app registrations / service principals exist
inside a paying client's tenant, how many, on what axis, holding what reach,
and traceable to what ratified capability. That gap is now load-bearing for
three measured reasons.

**1. Provider consent is not provider admission — measured, not assumed.**
The OpsxFactory Business Central investigation (2026-08-08..14) held four
admin-consented Entra application permissions on the Business Central API
for six days and still received `401` from the admin-center API. Access
appeared only after a **separate provider-side authorization inside the
Business Central admin center** (evidence
`xFactories/OpsxFactory/tenants/farheap-bc-sandbox1-verify-probe-evidence-v3`
through `-v7`; Microsoft documents consent AND admin-center authorization as
jointly required). Every workload has such a second key, and each one is
different. An identity model that records only the Entra grant records a
fiction.

**2. Some second keys silently widen the blast radius.** The BC admin-center
authorization has **no scope selector**: it enables admin-center operations
across every environment in the tenant. Before it, "sandbox only" was
enforced *structurally* — the credential could not reach Production. After
it, that guarantee exists only in gate logic. A degradation of this kind
must be a declared, checkable fact, not a discovery.

**3. The identity axis is a product decision arriving now.** A client buying
OpsxFactory governance expects it to span Business Central, SharePoint,
Teams, Exchange and the D365/CRM family. The tempting simplification is one
broad app controlling all of them. That fails on a concrete mechanism, not
on taste: **the app is the unit of grant for every per-workload scoping
mechanism**, so one app forces the broadest variant of every permission —
SharePoint `Sites.Selected` (which grants nothing until per-site grants)
collapses to estate-wide site access; Exchange RBAC-for-Applications
mailbox scoping collapses to all mailboxes; a per-environment Dataverse
application user collapses to org-wide. It also destroys the client's own
provider-side attribution (one appId for every action across every
workload), makes revocation all-or-nothing, and turns consent into a
40-permission dialog no administrator can meaningfully approve. The family
has already paid for this lesson once: the 2026-07-10 incident behind
OpsxFactory's `add-github-installation-policy` was a too-broad content App
holding org-wide `Contents:write` and bypassing branch protection.

Two domain factories (OpsxFactory, LedgerxFactory — `ledgerx-farheap-bc-*`)
already place identities in the same client tenant, so this cannot be a
domain-local rule.

## What Changes

- **`client-identity-roster` (ADDED capability)** — the neutral contract for
  governed identities in a client tenant:
  1. **Roster axis.** One governed identity per **(workload × authority
     class)**, authority classes being `observe`, `mutate`, `destructive`.
     No identity spans workloads; no identity mixes authority classes. This
     generalizes the axis OpsxFactory already ratified in
     `credentials/requirements.yaml` (16 requirement classes, reads split
     from writes, destructive split from ordinary writes) and the App
     tiering the GitHub plane adopted.
  2. **Residency.** Governed identities are **single-tenant, resident in the
     client's own tenant**, making the client the blast-radius unit. A
     multi-tenant (Opensoft-resident, consented-per-client) identity
     requires its own ratified exception carrying a blast-radius analysis,
     because one registration means one credential set spanning every
     client.
  3. **Workload admission is declared, with its ACHIEVED scope.** Each
     roster entry declares the provider-side second key (what must be done
     in the workload's own console) and the scope that key actually
     achieves. Where achieved scope exceeds the governed blast-radius unit,
     the excess is declared and the narrower bound must be enforced by gate
     logic — never assumed from the credential.
  4. **Ratification traceability.** Every entry names the ratified
     capability that justifies it; an identity present in a client tenant
     with no such capability is drift. Mutation and destructive identities
     come into existence only when their capability ratifies, so the
     client's tenant footprint is a projection of what governance has
     actually ratified.
  5. **Drift detection is report-only.** Identity, permission and admission
     mutations remain human acts; a drift finding never triggers automated
     remediation. (Generalizes `add-github-installation-policy`'s
     rules-as-code + report-only check from Opensoft's own org to client
     tenants.)
  6. **Cross-domain composition.** The roster is per-client and spans domain
     factories; each domain declares its own entries against the neutral
     shape, and an identity claimed by two domains, or two identities with
     overlapping (workload, authority class), is a finding.

## Capabilities

### New Capabilities

- `client-identity-roster`: governed identity topology for client tenants —
  the (workload × authority class) axis, single-tenant residency, declared
  workload admission with achieved scope, ratification traceability,
  report-only drift, and cross-domain composition.

### Modified Capabilities

<!-- none: this ADDS the identity layer beneath credential-contracts and
     consent-instrument without changing either. Credential shapes, grant
     neutrality, JIT/zero-standing-credential discipline and the authority
     chain root are consumed unchanged. -->

## Impact

- New neutral records: a roster schema under `contracts/schemas/` and a
  roster instance shape per client; no secrets, no tenant identifiers beyond
  references (the existing credential-record discipline applies unchanged).
- Static conformance: a `doc-health` family checking roster records against
  ratified capabilities (entry without capability, capability without entry,
  overlapping entries, missing achieved-scope declaration).
- Live drift detection against a real client tenant is a DOMAIN realization
  (the pattern already exists in OpsxFactory's `add-github-installation-policy`);
  this change defines its obligations, not its implementation.
- Domain follow-ups (named, not performed here): OpsxFactory declares its
  entries — including the finding that its Business Central identity is
  named `opsx-farheap-bc-observer` while now holding tenant-wide
  admin-center authority, and carries an inert Microsoft Graph delegated
  scope its own identity record does not mention; LedgerxFactory declares
  its `ledgerx-farheap-bc-*` entries.
- No change to `credential-contracts`, `consent-instrument`, grant
  templates, or the JIT discipline. No client-tenant act is authorized by
  this change.

## Out of scope, deliberately

- Enrollment automation. Creating app registrations inside a client tenant
  would itself require a broadly-privileged identity in that tenant — the
  chicken-and-egg this change deliberately does not solve. Enrollment stays
  a consented human act per client.
- The per-workload admission procedures themselves (each is provider
  documentation plus a domain runbook).
- Any decision to grant, widen, or narrow a live client identity.
