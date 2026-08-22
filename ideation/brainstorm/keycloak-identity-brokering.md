# Keycloak Identity Brokering and the Single Persona — Brainstorm

Status: staged
Kind: architecture
Summary: Proposes self-hosted Keycloak as the family's identity broker — users log in with whatever upstream IdP their organization chooses (GitHub, Google, Entra ID, any OIDC/SAML), federated identities link/merge into ONE persistent persona per human, and organization membership (a user working at multiple companies or repo orgs) is modeled on the persona rather than fragmenting it — replacing the dashboard's htpasswd Basic Auth first and satisfying the gate console's authenticated-principal hardening prerequisite.
Topics: identity-brokering, keycloak, user-management, single-persona, sso, ideation-dashboard, roles-authority-model, credential-contracts
Repository context: openxFactory (contract-level, cross-factory; deployment mechanics land in Omnigent-Install; identity operations ownership likely OpsxFactory)
Captured: 2026-07-14
Origin: Brett, 2026-07-14, after the ideation-dashboard deployment shipped
with single-user htpasswd Basic Auth and the question "how do we manage
users?" — and the final review's accepted risks named authenticated actor
identity as the prerequisite for any write-enabled host phase.
Organized: 2026-08-21 into the
[identity-brokering-plane staged topic](../staging/identity-brokering-plane/identity-brokering-plane.md)
and the sibling
[pki-trust-anchor-plane staged topic](../staging/pki-trust-anchor-plane/pki-trust-anchor-plane.md)
(both staged); kept as design history. See "Exit executed" below.

Brainstorm — contradiction and half-formed options are legal here.

## The problem

Three surfaces are converging on the same missing thing:

1. **The ideation dashboard** is live behind one shared htpasswd user —
   no per-user identity, no self-service, no revocation story beyond
   rotating the one password.
2. **The gate console's** future server-side phase is explicitly blocked
   on authenticated principals (accepted risks: forgeable ratification
   records, unauthenticated `--actor`) — a gate action must bind to a
   proven human identity.
3. **The AI spec-doc editor product** (decisions D1/D2 of that
   workstream) needs realm logins anyway — Google and Microsoft OAuth
   for the drive connectors — and, as an Opensoft product deployed per
   client, each client will demand *their* IdP.

And the human reality cutting across all three: **one person works at
multiple companies and multiple repo orgs** (Brett himself operates
several org profiles). Identity-per-surface or identity-per-tenant
fragments that person into unlinkable accounts. We want the opposite: one
durable persona per human, with organizations as memberships ON the
persona.

## The proposal

Self-hosted **Keycloak** as the family identity broker:

- **Bring-your-own IdP**: Keycloak identity brokering federates GitHub,
  Google, Entra ID, and any OIDC/SAML upstream. The client organization
  chooses; the family's surfaces only ever speak OIDC to Keycloak.
- **Single persona = one Keycloak user with N linked federated
  identities.** Keycloak's account linking supports exactly this: the
  same human logs in via GitHub today and Entra tomorrow, both resolve to
  the one persona. Merging existing duplicates is an admin/first-login
  flow, not a data migration.
- **Organizations on the persona**: Keycloak's Organizations feature
  (multi-tenant orgs within one realm, each org with its own IdPs and
  domain-routed login) models "works at multiple companies" natively —
  one realm, one persona, N org memberships, per-org IdP choice. This is
  the single-persona argument AGAINST realm-per-tenant.
- **Self-hosted on the xForge plane** (Postgres-backed, same AKS pattern
  as the dashboard route) — consistent with the family's
  self-hosted-system-of-record constraint and the editor product's hard
  requirement.

## Integration path (roughly in order)

1. **Dashboard auth swap**: oauth2-proxy (or nginx external-auth) in
   front of `ideation-dashboard.xforge.us` → Keycloak realm. Replaces
   Basic Auth; usernames arrive in trusted headers; the htpasswd secret
   retires. Smallest first step with immediate user-management payoff.
2. **Gate console principals**: the gate-action record's `actor` binds to
   the Keycloak subject (`sub` claim + display name) — closing the two
   identity-shaped accepted risks and unblocking the server-side console
   phase. Likely an additive gate-action-record schema field
   (`actor_subject`).
3. **Editor product login**: the AI-doc-editor authenticates via the same
   broker; the realm-integration drive grants (Google/Microsoft OAuth
   tokens under credential-contracts) attach to the persona — one human,
   one persona, their drives and their orgs.
4. Later candidates: hermes-readiness's bearer token, avatar surfaces,
   per-persona dashboard filtering (org membership × the D10 project
   register could scope which repos/projects a persona's dashboard
   shows).

## Open questions / contradictions (legal here)

- **Merge safety**: auto-link by matching email is convenient and
  dangerous (unverified emails, Entra guest addresses). Options:
  verified-email auto-link only; explicit link-account flow from a logged-
  in session (Keycloak's builtin); admin-approved merge queue for existing
  duplicates. Leaning: explicit linking + admin merge, never silent.
- **The durable subject**: what do family records (gate actions, doc
  authorship, review records) store as the persona id — Keycloak `sub`
  UUID (stable, opaque) with display name denormalized? Records written
  before Keycloak carry bare usernames; mapping table or leave historic?
- **One realm vs many**: single realm + Organizations preserves the
  single persona (leaning); realm-per-client isolates tenants harder but
  fragments personas — the exact failure Brett wants to avoid. Is there a
  client-contractual case that FORCES realm isolation, and if so does a
  persona-linking layer above realms exist worth the complexity?
- **Ownership**: identity infrastructure smells like OpsxFactory's domain
  (it already owns Entra/Intune administration in the family model);
  openxFactory owns the neutral contract (what surfaces may demand of the
  broker, what claims records may store). Same split as
  github-administration.
- **Authorization vs authentication**: v1 dashboard is read-only and
  same-for-everyone — is login-only (any persona in the org) enough, or
  do we gate by org/group from day one? Leaning: login-only first,
  authorization as its own later delta consuming Organizations + the
  project register.
- **Credential custody**: Keycloak client secrets, IdP client
  credentials, and the broker's DB creds all flow through
  credential-contracts (grant/binding templates, Key Vault custody) —
  never committed. The htpasswd retirement removes today's one shared
  secret.

## Possible feats

- Keycloak deployment on the xForge AKS plane (Omnigent-Install route +
  Postgres; mirrors the dashboard-route pattern).
- Dashboard oauth2-proxy swap (retire htpasswd Basic Auth).
- Account-linking + admin merge flow (single persona across GitHub /
  Google / Entra logins).
- Organizations model: per-client org with client-chosen IdP,
  domain-routed login.
- Gate-action authenticated principal (additive `actor_subject` field +
  console binding) — unblocks the server-side gate phase.
- Editor-product login via the broker, with drive grants attached to the
  persona (ties to the realm-integration staged topic).
- Persona-scoped dashboard filtering (org membership × D10 project
  register).

## Exit

When direction settles (merge safety, realm topology, ownership split),
split into staged topics — likely: broker deployment + dashboard swap
first (smallest, immediate payoff), persona/linking contract second
(neutral, openxFactory-owned), gate-principal binding third. Coordinate
with the OpsxFactory identity ownership question and the
realm-integration topic in codexFactory staging.

## Exit executed — 2026-08-21

All three blockers this exit clause named were ruled by Brett Heap in the
xFactory family session on 2026-08-21, so the split was executed the same
day:

- **Realm topology** → single realm per environment plus Keycloak
  Organizations for companies (both tenant and subject/served), each able
  to federate its own IdP with domain-routed login. The broker MUST NOT
  mirror the tenancy graph — it asserts persona plus organization
  memberships only, and authorization resolves in the governed layer
  against the Hermes graph and grants. Isolation escalates by broker
  INSTANCE (a per-client install) and never by realm split; the neutral
  contract stays silent on instance count.
- **Merge safety** → explicit account linking plus an admin-approved merge
  queue. Never silent email-match auto-link. (This was the brainstorm's
  own leaning; it is now the ruling.)
- **Ownership split** → the github-administration precedent: openxFactory
  owns the neutral contracts, OpsxFactory owns the administration
  workflows as siblings of `exchange-administration` /
  `aks-administration-workflow` / `github-administration-workflow` /
  `business-central-administration`, and new install repos own the
  deployable runtime (`opensoft/Keycloak-Install` at
  `installs/keycloak-install`, `opensoft/OpenXPKI-Install` at
  `installs/openxpki-install`, per-client instantiation as
  `config/clients/<tenant>/runtime-manifest.yaml` on the hermes-install
  precedent).

Also ruled, beyond what this brainstorm asked: services and workloads are
**not** realm users — workload identity stays on `credential-contracts`
plus `openxwallet` grants, with broker clients provisioned only where
something genuinely needs an OIDC token.

The successors:

- [identity-brokering-plane](../staging/identity-brokering-plane/identity-brokering-plane.md)
  (`openxFactory:staging:identity-brokering-plane`) — the persona/claims
  side, carrying the rulings above and the integration path (dashboard
  oauth2-proxy swap, gate `actor_subject` binding, editor login, then the
  later candidates this doc listed).
- [pki-trust-anchor-plane](../staging/pki-trust-anchor-plane/pki-trust-anchor-plane.md)
  (`openxFactory:staging:pki-trust-anchor-plane`) — the PKI side, which
  this brainstorm did not anticipate: two realizations (a live Intune
  Cloud PKI canary and OpenXPKI for the production core) force one
  product-agnostic trust-anchor contract.
- `OpsxFactory:staging:identity-pki-administration` — the governed
  administration workflows for both planes, plus the new service-subject
  kinds registered in lockstep.
- `OpsxFactory:staging:engagement-shapes` — the engagement questions
  raised by per-client broker and CA instances.

The open questions this doc left unresolved were carried forward rather
than answered: the durable subject id stored in governed records, the
exact `actor_subject` field shape, login-only versus authorization gating
at v1, `hermes-readiness` bearer-token adoption, and a pre-ratification
check for any user population that must not co-reside in the shared
realm. Credential custody (the last bullet above) is settled by
composition rather than by ruling — broker DB credentials, IdP client
secrets, and CA material are all `credential-contracts` records with
declared custody, never committed.

### Realization landed — 2026-08-21

Exit 1 of the persona/claims side is **realized**, the same day it was
proposed and ratified: the neutral `identity-brokering` capability landed as
`add-identity-brokering`, realized by Speckit feature
`008-identity-brokering-contracts` and **registered at `contract-v1.37`** in
[contracts/manifest.yaml](../../contracts/manifest.yaml) and
[contracts/CHANGELOG.md](../../contracts/CHANGELOG.md). The family is
[contracts/identity-brokering/](../../contracts/identity-brokering/README.md)
— six schemas, a canonical validator, and 14 positive plus 41
intended-invalid fixtures at 9/9 requirement coverage — and every ruling
recorded above survived into it unchanged, including the two this brainstorm
argued hardest for: the broker asserts persona plus organization memberships
ONLY (now a closed property allow-list at every depth, so the tenancy graph
cannot be mirrored even by accident), and merging is explicit or
admin-approved with attribute-match auto-linking unrepresentable rather than
merely discouraged.

Three of the open questions this doc carried forward are now settled in the
realization's research record: the durable subject id and the `actor_subject`
field shape (the STRUCTURED reference — issuer, opaque subject, display name
as it stood, provenance class), pre-broker history (mark the boundary date and
map on demand, never blanket-backfill), and the co-residence check, which
found one population (HealthLinc patients) and pre-declared it the first
dedicated-instance client. Login-only versus authorization gating and
`hermes-readiness` bearer tokens remain deferred to later deltas.

The PKI side this brainstorm did not anticipate was realized the same day as
the sibling `add-trust-anchor` (feature `009-trust-anchor-contracts`, the same
`contract-v1.37` cut). Both staged fragments have completed full promotion and
now live with their proposals:
[identity-brokering-plane.md](../../openspec/changes/add-identity-brokering/supporting-docs/identity-brokering-plane.md)
and
[pki-trust-anchor-plane.md](../../openspec/changes/add-trust-anchor/supporting-docs/pki-trust-anchor-plane.md).
The `../staging/` links above are kept as design history and are no longer
live paths.

Still open here: exits 2 and 3 on both planes — the OpsxFactory
administration workflows and the two install-repository creations — tracked as
named successors on the two changes, not in this brainstorm.
