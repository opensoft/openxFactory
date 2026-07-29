# Keycloak Identity Brokering and the Single Persona — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Proposes self-hosted Keycloak as the family's identity broker — users log in with whatever upstream IdP their organization chooses (GitHub, Google, Entra ID, any OIDC/SAML), federated identities link/merge into ONE persistent persona per human, and organization membership (a user working at multiple companies or repo orgs) is modeled on the persona rather than fragmenting it — replacing the dashboard's htpasswd Basic Auth first and satisfying the gate console's authenticated-principal hardening prerequisite.
Topics: identity-custody, identity-brokering, keycloak, user-management, single-persona, sso, ideation-dashboard, roles-authority-model, credential-contracts
Repository context: openxFactory (contract-level, cross-factory; deployment mechanics land in Omnigent-Install; identity operations ownership likely OpsxFactory)
Captured: 2026-07-14

Origin: Brett, 2026-07-14, after the ideation-dashboard deployment shipped
with single-user htpasswd Basic Auth and the question "how do we manage
users?" — and the final review's accepted risks named authenticated actor
identity as the prerequisite for any write-enabled host phase.

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
