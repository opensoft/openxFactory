# Staged: Identity Brokering Plane — one persona, organizations as memberships

Status: staged
Kind: architecture
Summary: Adopts a self-hosted identity broker (Keycloak) as the family's
authentication plane: humans log in through whatever upstream IdP their
organization chose, federated logins link into ONE durable persona per human,
and company boundaries are modelled as Keycloak Organizations on that persona
rather than as separate realms. openxFactory owns the neutral persona/claims
contract (what a surface may demand of a broker, what a governed record may
store about an actor); OpsxFactory owns the `keycloak-administration` workflow;
a new `xFactory-Keycloak-Install` repo owns the deployable runtime and its
per-client instantiation. Ruled 2026-08-21: single realm per environment plus
Organizations, explicit account linking with an admin-approved merge queue,
workloads stay out of the realm, isolation escalates by broker INSTANCE and
never by realm split.
Topics: identity-brokering, keycloak, single-persona, keycloak-organizations, sso, account-linking, actor-identity, ideation-dashboard, gate-console, roles-authority-model, credential-contracts, openxwallet, install-repo-boundary
Repository context: openxFactory owns the neutral identity/persona contract (product-agnostic: persona, claims, org membership assertion, the never-mirror-the-tenancy-graph rule); OpsxFactory owns the governed administration workflow (`keycloak-administration`, sibling of `exchange-administration` / `aks-administration-workflow` / `github-administration-workflow` / `business-central-administration`, staged as `OpsxFactory:staging:identity-pki-administration`); a new install repo `opensoft/xFactory-Keycloak-Install` (aggregation path `installs/keycloak-install`) owns the deployable runtime and per-client instantiation
Staging ID: openxFactory:staging:identity-brokering-plane
Source: the 2026-07-14 brainstorm [keycloak-identity-brokering.md](../../brainstorm/keycloak-identity-brokering.md) (captured after the ideation dashboard shipped behind one shared htpasswd user), organized 2026-08-21 on Brett Heap's rulings in the xFactory family session — the brainstorm's exit clause named merge safety, realm topology, and the ownership split as the three blockers, and all three were ruled that day
Target capabilities: ADDED neutral `identity-brokering` (openxFactory); new OpsxFactory-owned `keycloak-administration` workflow capability; MODIFIED `repo-boundary-governance` (two new install repositories in scope)

Three surfaces have been converging on the same missing thing for a month, and
the brainstorm that named it has now been ruled. The point of this topic is the
part that survives the product choice: a **persona contract**. Keycloak is the
realization we are adopting; the contract openxFactory owns must describe what
any broker has to assert and what a governed record may store, so that a
domain deploying a different broker — or no broker at all — is still
conformant.

## The problem, condensed

1. **The ideation dashboard** (`ideation-dashboard.xforge.us`, now the openDox
   workbench) is live behind a single shared htpasswd user. There is no
   per-user identity, no self-service, and no revocation story beyond rotating
   the one password.
2. **The gate console** carries two accepted risks that are both identity
   shaped: a ratification record's actor is forgeable, and `--actor` is
   unauthenticated. Any write-enabled server-side phase is explicitly blocked
   on a proven principal. A gate action is a governance act; it must bind to a
   human the system can name.
3. **The editor product** needs realm logins regardless — Google and Microsoft
   OAuth for the drive connectors — and, deployed per client, each client will
   insist on *their* IdP.
4. **The human reality cutting across all three**: one person works at several
   companies and several repo orgs. Identity-per-surface or
   identity-per-tenant fragments that person into unlinkable accounts, which
   is precisely the outcome to avoid. We want one durable persona with
   organizations as memberships **on** it.

## Rulings — 2026-08-21 (Brett Heap, xFactory family session)

### R1 — Install repos own the deployable runtime

Two new install repositories, following the `xFactory-Hermes-Install`
naming and pattern:

| Repository | Aggregation path |
| --- | --- |
| `opensoft/xFactory-Keycloak-Install` | `installs/keycloak-install` |
| `opensoft/xFactory-OpenXPKI-Install` | `installs/openxpki-install` |

Per-client instantiation lives **inside** each install repo as
`config/clients/<tenant>/runtime-manifest.yaml`, the hermes-install precedent
(`config/clients/opensoft/runtime-manifest.yaml` — generated, never
hand-edited, digest-pinned by its consumers). Reasoning: the family already
proved this shape once. A stack-identity manifest that lives with the runtime
it describes can be regenerated and read back as evidence; a manifest that
lives in a factory repo drifts from the thing it claims to describe. Repo
creation is not a free action — it rides the promoted
`repo-boundary-governance` capability through an OpenSpec change, because that
capability's "Install repository scope" requirement currently enumerates
`Hermes-Install` and `Omnigent-Install` by name and must be amended to admit
the two new scopes (a MODIFIED delta naming that requirement, restating all
its scenarios).

The OpenXPKI half of R1 is developed in the sibling topic
[pki-trust-anchor-plane](../pki-trust-anchor-plane/pki-trust-anchor-plane.md);
it is recorded here because the ruling was made once, for both.

### R3 — Realm topology: one realm, Organizations for companies

The brainstorm's hardest open question ("one realm vs many") is **ruled**:

- **Default: a single realm per environment**, with **Keycloak Organizations**
  representing companies — both **tenant** companies (the operator layer) and
  **subject / served** companies (the served layer). Each Organization may
  federate its own IdP, with domain-routed login, so a client's users reach
  their own IdP from the shared login page.
- **The broker MUST NOT mirror the tenancy graph.** Keycloak asserts two
  things only: *who this persona is* and *which organizations it belongs to*.
  It does not encode stacks, layers, domains, projects, or grants.
  Authorization resolves in the governed layer, against the Hermes graph and
  the grants that already exist there. Reasoning: a second copy of the tenancy
  graph inside an off-the-shelf IdP is a copy that will disagree with the
  first one, and the disagreement will be discovered by an authorization
  decision going the wrong way. One graph, one authority.
- **Isolation escalates by INSTANCE, never by realm split.** When a client's
  contract or a population's sensitivity forbids co-residence, the answer is a
  **dedicated broker instance** — its own per-client install under
  `config/clients/<tenant>/` — not a second realm inside the shared broker.
  Reasoning: realm-splitting inside one broker buys weaker isolation than a
  separate instance (shared admin plane, shared database, shared blast radius)
  while paying the full persona-fragmentation cost. If we are going to
  fragment personas, we should at least get real isolation for it.
- **The neutral contract is therefore written as**: *a single persona within a
  broker instance; organizations realize company boundaries* — and it stays
  **silent on instance count**. Reasoning: silence is load-bearing here. A
  non-tenanted MedxFactory-style deployment (one clinic, its own stack, no
  operator above it) can run its own broker and still be conformant; a
  contract that mandated one shared broker would make that deployment
  non-conformant for no governance benefit.

### R4 — Merge safety: explicit linking, admin-approved merges

**Explicit account linking** (the broker's logged-in link-account flow) plus
an **admin-approved merge queue** for pre-existing duplicates. **Never silent
auto-link on email match.** Reasoning: email-match auto-linking is an account
takeover primitive wherever an upstream IdP will assert an unverified or
reassignable address — Entra guest addresses and self-service directories both
qualify. The convenience is real and the failure is an identity merge that
cannot be undone from the audit record. A merge is an administrative act with
a record; it goes through a governed queue like every other administrative
act.

### R5 — Services and workloads are not realm users

Workload identity does **not** flow through the broker's user store. It flows
through the promoted `credential-contracts` (grants distributed by reference
into ephemeral job scope, custody as an execution binding) and `openxwallet`
(**grants as the authority primitive**, custody **declared** and bounding what
a signature evidences). Keycloak clients / service accounts are provisioned
**only** where something genuinely needs an OIDC token — a confidential client
for a web surface, for instance. Reasoning: the family already ratified an
authority model for non-human actors, and it is stronger than a realm user
row: attenuated grants, proof of possession, key-attributed audit, revocation
that propagates. Putting workloads in the realm would create a second, weaker
authority vocabulary next to it, and the weaker one would win by convenience.

### R7 — Ownership split, on the github-administration precedent

The same three-way split the family already executed for GitHub
(`github-administration-plane`, both exits archived 2026-07-14/15):

- **openxFactory owns the neutral contract.** For identity: the
  persona/claims contract — what a surface may demand of a broker, what
  claims a governed record may store about an actor, the single-persona rule,
  the organizations-realize-companies rule, and the never-mirror-the-tenancy-
  graph rule. Product-agnostic: no Keycloak-specific vocabulary in the
  requirement text.
- **OpsxFactory owns the governed administration workflow.**
  `keycloak-administration` as a **sibling** of the existing
  `exchange-administration`, `aks-administration-workflow`,
  `github-administration-workflow`, and `business-central-administration`
  capabilities — not a profile of one of them. The broker is a managed
  platform under the promoted `opsx-service-subject-model`, administered the
  same way every other managed platform is: plan / apply / verify / recover
  against reviewed desired state.
- **New service-subject kinds are registered in lockstep.** An identity
  broker (and, in the sibling topic, a certificate authority) is a new
  service-subject kind: it lands in `customer-kinds` **and** the Hermes
  template **and** `stack.yaml` in the same change, with grant ceilings in
  `credentials/requirements.yaml`. Reasoning: these three files are a single
  registry wearing three filenames; a kind present in one and absent from
  another is a validation failure at best and an ungoverned subject at worst.
- **The install repos own the runtime**, per R1.

## Integration path

Ordered so that each step pays for itself before the next one starts.

1. **Dashboard auth swap.** oauth2-proxy (or nginx external-auth) in front of
   the workbench route, pointed at the broker. Basic Auth retires with the
   htpasswd secret; usernames arrive in trusted headers. Smallest step,
   immediate user-management payoff, and it proves the broker in production
   against a surface whose failure mode is "nobody can read the dashboard".
2. **Gate `actor_subject` binding.** The gate-action record binds its actor to
   the broker's subject identifier plus a display name, closing the two
   identity-shaped accepted risks and unblocking the server-side console
   phase. Likely an additive record field; the exact shape is an open question
   below.
3. **Editor-product login.** The editor authenticates through the same broker;
   the drive grants (Google / Microsoft OAuth tokens under
   `credential-contracts`) attach to the persona. One human, one persona,
   their drives, their organizations.
4. **Later, each on its own delta**: the `hermes-readiness` bearer token moves
   to broker-issued tokens; avatar surfaces adopt persona login; the workbench
   filters by persona (organization membership crossed with the project
   register) so a persona sees the projects its organizations actually own.

## Composition with promoted capabilities

- `roles-authority-model` — the persona is the human end of the authority
  model the App identity tiers already sit in; a persona's authority still
  comes from grants, not from realm group membership.
- `credential-contracts` — broker DB credentials, IdP client secrets, and the
  confidential-client secrets are all credential records with declared
  custody. Nothing is committed. The htpasswd retirement **removes** today's
  one shared secret rather than adding to the inventory.
- `openxwallet` / `openxwallet-agent-profile` — the non-human half of the same
  picture (R5). A persona in the broker and a wallet holder are different
  holder classes; neither is a substrate for the other.

## Open questions (carried, not resolved)

1. **The durable subject in governed records.** Store the broker's `sub` UUID
   (stable, opaque) with a denormalized display name? And what happens to
   records written before the broker existed, which carry bare usernames — a
   mapping table, a one-time backfill, or leave history as-is and mark the
   boundary date?
2. **Login-only vs authorization gating at v1.** Leaning **login-only first**
   (any persona in an organization may read), with authorization as its own
   later delta consuming Organizations plus the project register. The risk to
   watch is a surface shipping read-only, then gaining a write action before
   the authorization delta lands.
3. **The exact `actor_subject` field shape** on the gate-action record —
   single opaque identifier, or a small structured object (issuer + subject +
   display name)? The second is more honest across a future broker migration
   and costs a schema major if we guess wrong.
4. **`hermes-readiness` bearer-token adoption** — worth folding into the first
   wave, or does the token-gated readiness surface stay as-is until the
   worker-enrollment broker's own auth modes settle?
5. **Co-residence check before ratification.** Verify whether any current
   commitment implies a user population that must **not** co-reside in the
   shared realm — the Medx clinical surfaces and the Business Central /
   DaVinciSite tenant work are the two candidates. If one exists, it becomes
   the first dedicated-instance client under R3, and the neutral contract's
   silence on instance count is exercised immediately rather than
   theoretically.

## Exit

Three planned OpenSpec changes, in dependency order:

1. **openxFactory** — a neutral `identity-brokering` capability: persona and
   claims, the single-persona rule ("a single persona within a broker
   instance"), organizations-realize-company-boundaries, the
   never-mirror-the-tenancy-graph rule, what a governed record may store about
   an actor, and the merge-safety obligation (explicit linking; administrative
   merge with a record). Product-neutral requirement text — Keycloak appears
   in the design discussion, never in a requirement.
2. **OpsxFactory** — a `keycloak-administration` workflow capability, sibling
   to the four existing administration capabilities, plus the new
   service-subject kind registered in lockstep (`customer-kinds` + Hermes
   template + `stack.yaml`, grant ceilings in
   `credentials/requirements.yaml`). Developed in the sibling staged topic
   `OpsxFactory:staging:identity-pki-administration`
   (`xFactories/OpsxFactory/ideation/staging/identity-pki-administration/`),
   which covers both administration workflows because they share the
   service-subject registration work.
3. **Aggregation + install** — create `opensoft/xFactory-Keycloak-Install`
   under `repo-boundary-governance` (a MODIFIED delta to its "Install
   repository scope" requirement), add the `installs/keycloak-install`
   submodule pin, and land the first `config/clients/opensoft/`
   runtime-manifest. Sequenced after exit 1 so the runtime is built against a
   ratified contract rather than the other way round.

Sequencing note: exit 1 and exit 2 can be authored in parallel (the
github-administration precedent did exactly that, one day apart), but the
neutral contract must ratify first — the administration workflow's desired
state is expressed in the neutral contract's vocabulary. Engagement-shape
questions raised by per-client broker instances are developed in the other
OpsxFactory sibling topic, `OpsxFactory:staging:engagement-shapes`.
