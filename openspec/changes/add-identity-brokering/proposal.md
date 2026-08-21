---
code_surface: openxFactory (a NEW `contracts/identity-brokering/` family — persona assertion, broker organization, actor-subject reference, identity link/merge record, broker service-client declaration, and surface adoption/posture schemas — plus a family README, packaged positive/negative examples, and the canonical `scripts/validate-identity-brokering.py`; registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` + the README contract index at the next additive bundle cut). The broker RUNTIME and its per-client instantiation (`xFactory-Keycloak-Install`), the OpsxFactory `keycloak-administration` workflow with its service-subject registration, the dashboard oauth2-proxy swap, and the gate-action `actor_subject` field are successor realization changes named in the impact map, not this change's surface.
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
Status: ratified
Ratified by: Brett Heap, 2026-08-21 — "ratify both proposals"; all design decisions adopted as written, OQ-1 through OQ-4 recommendations adopted as the working recommendations at the settlement points their tasks name, and the OQ-5 pre-ratification gate discharged by review/co-residence-finding-2026-08-21.md (one population found: HealthLinc patients, pre-declared the first dedicated-instance client under D3)
---

# Proposal: add-identity-brokering

## Why

Three surfaces spent a month converging on the same missing thing, and the
brainstorm that named it has now been ruled.

1. **The ideation dashboard / openDox workbench** is live behind a single
   shared htpasswd user. There is no per-user identity, no self-service,
   and no revocation story beyond rotating the one password — so the
   answer to "who read this?" is "somebody with the password".
2. **The gate console** carries two accepted risks that are both identity
   shaped: a ratification record's actor is forgeable, and `--actor` is
   unauthenticated. Any write-enabled server-side phase is explicitly
   blocked on a proven principal, because a gate action is a governance
   act and must bind to a human the system can name.
3. **The editor product** needs realm logins regardless — Google and
   Microsoft OAuth for the drive connectors — and, deployed per client,
   each client will insist on *their* identity provider.
4. **The human reality cutting across all three**: one person works at
   several companies and several repository orgs. Identity-per-surface or
   identity-per-tenant fragments that person into unlinkable accounts,
   which is precisely the outcome to avoid. One durable persona, with
   organizations as memberships **on** it.

The product choice is settled and is not what this change is about.
Keycloak is the realization the family is adopting; what openxFactory owns
is the part that survives it — a persona contract stating what any broker
must assert, what a governed record may store about an actor, and what the
broker must never become. A domain deploying a different broker, or none,
stays conformant.

Ratifying that contract first is the sequencing the family already proved
with `github-administration`: the administration workflow's desired state
is expressed in the neutral contract's vocabulary, so the vocabulary has
to exist before the workflow or the runtime is built against it.

## What Changes

- **ADD the neutral `identity-brokering` capability** — nine requirements,
  product-agnostic throughout:

  - **One persona per human within a broker instance.** Federated upstream
    identities attach to that persona; no surface holds a human account
    the broker cannot resolve.
  - **Organizations realize company boundaries** — the tenant/operator
    company and the subject/served company alike — as memberships on the
    persona, many-to-many, each organization free to federate its own
    upstream provider with domain-routed login. Membership records
    association, never authority.
  - **The broker asserts identity and membership only.** It MUST NOT
    represent stacks, layers, domains, projects, subjects, roles, or
    grants. Authorization resolves in the governed layer against the
    tenancy graph and the grants already recorded there. An organization
    may carry one resolvable pointer to its governed record — a pointer,
    not a projection.
  - **Identities link explicitly or merge by decision, never silently.**
    Explicit user-initiated linking, or an administrative merge approved
    through the governed workflow and recorded; never an attribute match,
    email above all. Pre-merge subject identifiers stay resolvable so
    existing records stay attributable.
  - **Governed records bind their actor to a stable opaque subject** plus
    the display name in force, never to a display name, address, or
    upstream account name as the identifier — with the exact field shape
    a named open design point rather than a guess ratified early.
  - **Workloads are not personas.** Non-human authority stays on
    `credential-contracts` grants and `openxwallet` holders; broker
    service clients exist only where a surface genuinely needs OIDC
    tokens, and such a client is transport, never an actor.
  - **Broker credentials are credential-contract records** with declared
    custody — client secrets, upstream provider credentials, datastore
    credentials — never committed and never carried in a configuration
    export. Adopting persona login on a surface running a shared static
    secret RETIRES that secret.
  - **Isolation escalates by dedicated instance**, never by fragmenting
    personas inside a shared one; the capability stays deliberately
    silent on instance count so a single-organization deployment is
    conformant.
  - **A surface declares its authorization posture**, and a governed write
    action requires a resolved authorization decision rather than
    authentication alone.

- **ADD one requirement to `repo-boundary-governance`** — "Keycloak
  install repository boundary", on the avatar-client template: the repo,
  its named creating successor change, the aggregation path, ownership of
  the deployment topology and the per-client
  `config/clients/<tenant>/runtime-manifest.yaml`, the contract pin, the
  explicit MUST NOTs (no credentials, no key material, no credential-
  bearing configuration export, no neutral contract restatement, no
  administration workflow), and aggregation admission as a separate
  reviewed act.

- **Schemas, examples, and a validator (this change's code surface).** No
  broker, no realm, no deployment, no credential, no user store, and no
  change to any surface's authentication today.

## Capabilities

### New Capabilities

- `identity-brokering`: the neutral persona and claims contract — the
  single-persona rule, organizations as company boundaries on the persona,
  the never-mirror-the-governed-graph rule, merge and linking safety, the
  durable actor subject in governed records, the workloads-are-not-personas
  rule, broker credential custody by composition, isolation by instance,
  and the declared authorization posture.

### Modified Capabilities

- `repo-boundary-governance`: one ADDED requirement admitting the
  `xFactory-Keycloak-Install` boundary. No existing requirement is
  modified or restated.

## Impact

- **New code (this change)**: six schemas, a family README, packaged
  positive and negative examples, one canonical validator, and bundle
  registration. No runtime behavior changes; nothing needs un-building.
- **Successor realization changes**, each consuming this contract's
  vocabulary and pinning the released bundle:
  1. **OpsxFactory `keycloak-administration`** — the governed
     administration workflow as a sibling of `exchange-administration`,
     `aks-administration-workflow`, `github-administration-workflow` and
     `business-central-administration`, plus the new service-subject kind
     registered in lockstep (`customer-kinds` + the Hermes template +
     `stack.yaml`, with grant ceilings in `credentials/requirements.yaml`).
     Developed in `OpsxFactory:staging:identity-pki-administration`, which
     covers both administration workflows because they share the
     service-subject registration work.
  2. **`implement-keycloak-install-repo`** — creates
     `opensoft/xFactory-Keycloak-Install` under the requirement this
     change adds, lands the first `config/clients/opensoft/`
     runtime-manifest, and hands aggregation admission to its own
     separate reviewed change.
  3. **Dashboard oauth2-proxy swap** — oauth2-proxy (or nginx
     external-auth) in front of the workbench route, pointed at the
     broker; the htpasswd secret retires with it. Smallest step, immediate
     payoff, and it proves the broker in production against a surface
     whose worst failure is "nobody can read the dashboard".
  4. **Gate-console `actor_subject` binding** — the gate-action record
     binds its actor to the broker-issued subject plus display name,
     closing both identity-shaped accepted risks and unblocking the
     server-side console phase. Its exact field shape is open design point
     OQ-3 here, and that change settles it.
  5. **Editor-product login**, then the later deltas each on their own:
     the `hermes-readiness` bearer token, avatar-surface persona login,
     and persona-scoped workbench filtering (organization membership
     crossed with the project register).
- **Sibling proposal**: `add-trust-anchor` (from
  `openxFactory:staging:pki-trust-anchor-plane`) carries the PKI half of
  the same 2026-08-21 session. Rulings R1 (install repos own the runtime)
  and R7 (the ownership split) were made once for both topics, so the two
  proposals each add their own per-repo `repo-boundary-governance`
  requirement — `openxpki-install` there, `keycloak-install` here — rather
  than contending over one shared enumeration. Neither depends on the
  other's content.
- **Relies on ratified work**: `credential-contracts` (requirement,
  binding, grant and custody shapes), `openxwallet` and
  `openxwallet-agent-profile` (the non-human half of the same picture),
  `roles-authority-model` (a persona's authority still comes from grants),
  `repo-boundary-governance` (the avatar-client template for admitting an
  install repository), `layer-vocabulary` (tenant and subject naming), and
  `document-lifecycle` (staged-topic promotion into `supporting-docs/`).
- **Provenance**: staged topic
  `openxFactory:staging:identity-brokering-plane` (its exit 1), which
  records Brett Heap's rulings R1, R3, R4, R5 and R7 of 2026-08-21; origin
  brainstorm `ideation/brainstorm/keycloak-identity-brokering.md`
  (2026-07-14), whose three exit blockers were all ruled that day.
- **Not ratified**: one pre-ratification GATE is outstanding — the
  co-residence check (design OQ-5). See design.md.

## Ratification

Ratified by Brett Heap, 2026-08-21 (session instruction: "ratify both
proposals"). All design decisions adopted as written. The carried open
questions keep their recommendations and their named settlement points
(OQ-1/OQ-3 before schema authoring, in the realization feature's research;
OQ-2 as its own later delta; OQ-4 with the readiness surface's owner). The
OQ-5 gate is discharged by the written finding at
`review/co-residence-finding-2026-08-21.md`: one population was found —
HealthLinc patients (`healthlinc-argentina` in HealthLinc's recorded
architecture) — and it is pre-declared the FIRST dedicated-instance client
under design D3, binding realization to exclude clinical-patient
populations from the shared instance by rule. Ratification authorizes
exactly one Speckit realization feature for phase 1 and creates no broker,
realm, organization, credential, or persona.
