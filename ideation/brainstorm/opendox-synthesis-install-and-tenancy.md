# openDox Install and Tenancy — Synthesis — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Synthesis across the packet: the per-tenant descendant install Brett
described ("If I install MedxFacotry, then I get a medXdox install running in
the installed tenand with its own db") is the requirement that forces every
other choice — it makes the app-with-a-database non-optional, it makes the
two-layer split load-bearing rather than tidy, it lands squarely on the ratified
`domain-descendant-boundary` pattern, and it inherits a proven in-house runtime
shape from the Hermes install; what it does NOT settle is whether a descendant
instance is always its own instance, and whether the descendant pins openXdox or
openDox.
Topics: opendox, openxdox, medxdox, codexdox, tenant-install,
per-tenant-database, domain-descendant-boundary, neutral-product-pin,
hermes-install, runtime-shape, openxdox-install-app-provisioning,
install-provisioning, feat-request
Repository context: synthesizes across openxFactory (the contracts and the
corpus), the DomainxFactories (the descendants), Omnigent-Install and
OpsxFactory (the install and workload plane), and xFactory-Hermes-Install (the
runtime precedent)
Captured: 2026-09-04

## Possible feats

- **The openDox install repository** — `openDox-Install`, or install machinery
  inside openDox itself; the Hermes install's shape is the decision to copy or
  reject.
- **Descendant provisioning inside a DomainxFactory install** — the install
  flow that stands up one descendant instance with its own database in the
  tenant it just created.
- **Per-tenant database lifecycle** — ordered migrations, a lifecycle CLI,
  backup and restore, and the tenant-sovereignty rule that opensoft never holds
  a key on the tenant's data.
- **Descendant pin-and-profile for a runtime** — `domain-descendant-boundary`
  was ratified over CONTRACT products; a descendant of a running application
  with a schema is a new case the standard has never been applied to.
- **Fold the App-provisioning topic in** — `openxdox-install-app-provisioning`
  designed the two-App manifest bootstrap for the intent plane; a per-tenant
  app install needs it and adds a database to it.

## The requirement that forces everything else

> "If I install MedxFacotry, then I get a medXdox install running in the
> installed tenand with its own db."

Read that as a specification and four things fall out immediately:

1. **There is a runtime.** Not a static site published from a checkout — a
   service with a lifecycle that an installer starts. The current hosted
   dashboard is a credential-free pod serving a snapshot thawed from git by a
   nightly lane; that is not installable per tenant in any meaningful sense.
2. **There is a database, per tenant.** Which means schema, migrations, backup,
   and a tenancy boundary that is physical rather than a row filter. Brett said
   "its own db", not "its own schema" or "its own rows".
3. **There is a descendant, per domain.** `MedxDox` for MedxFactory, `codexDox`
   for codexFactory. So the neutral product must be consumable by a descendant,
   which means a release identity, a pin, and a profile surface.
4. **The install is driven by the DomainxFactory install.** Installing
   MedxFactory installs MedxDox. That is a composition, and it is the same
   composition Omnigent-Install already performs for the intent plane.

None of the four is available today. All four are ordinary for the Hermes
install.

## The runtime shape is already in the house

`opensoft/xFactory-Hermes-Install` is the in-house precedent and it is
LIVE-REALIZED on AKS. Its shape, transcribed:

```text
src/hermes_install/          the runtime: config, api, domain, repositories,
                             persistence, authz, artifacts, health, audit,
                             lifecycle
migrations/                  ordered SQL (0001 = pinned canonical schema,
                             0002+ additive)
config/clients/<client>/     per-client instance trees, validated by
                             openxFactory's own validator from a pinned checkout
deploy/compose/              canonical single-node package (image + Compose)
deploy/kubernetes/           AKS adapter (kustomize base + per-env overlay)
scripts/hermes-lifecycle     the single lifecycle CLI (20 verbs)
tests/                       unit, pg, api, compose, adapter suites
```

FastAPI plus Postgres, ordered migrations, a per-client instance tree, one
lifecycle CLI, a Compose package for single-node and a kustomize adapter for
AKS, and layer contracts owned by openxFactory rather than by the installer. It
serves two live hosts. Whatever openDox's runtime turns out to be, this is the
pattern with the fewest unknowns, and the strongest argument for it is not
elegance — it is that the same operators already run it.

Two properties worth copying explicitly:

- **The installer installs and configures; it does not own contracts.** Hermes
  install's README says layer contracts and schemas are owned by openxFactory
  and "this repo only installs and configures the runtime that implements
  them." The same discipline keeps openDox from quietly becoming a second home
  for governance vocabulary.
- **The committed stack-identity manifest is regenerated, never hand-edited.**
  A per-tenant openDox install will want the same: a generated manifest that
  downstream repos digest-pin.

## Where the descendant pattern fits, and where it strains

`domain-descendant-boundary` is promoted (5 requirements) and says, in the
ruling's own shape: a domain consumes a neutral product through a
`<Domainx><Product>` descendant repository; the descendant pins the product by
commit TWICE (submodule gitlink plus `contracts/<product>-pin.yaml`, both in the
same commit); it carries only profile — overlays, branding, deploy config,
domain validators — and never a fork; it is placed at a ratified placement; and
it is created on its first profile, not before.

`MedxDox` and `codexDox` land on that pattern cleanly at the naming and pinning
level. Where it strains is that every existing descendant profiles a CONTRACT
family — openChart → MedxChart, openPractice → MedxPractice, openAvatar →
MedxAvatar / LedgerxAvatar, openXwallet → LedgerxWallet. A descendant of a
running application with a database schema has to profile things the standard
has never had to express:

- **Schema.** Does a domain add tables? If MedxDox needs a clinical field on a
  document, is that a profile (a JSONB extension the neutral schema reserves) or
  a fork (a migration the neutral product does not know about)? "Pin and
  profile, never fork" is easy to honour in YAML and hard to honour in DDL.
- **Deploy config.** Already permitted by the standard, and here it is the bulk
  of the descendant: namespace, image digests, ingress host, secrets bindings,
  database sizing.
- **Migrations.** If the neutral product ships ordered SQL and the descendant
  pins it by commit, then an upgrade is a migration run inside the tenant, and
  the pin bump is a scheduled operation rather than a file edit. Nothing in
  `neutral-product-pin` contemplates a pin whose consumption has downtime.

And one question the ruling leaves genuinely open: **does the descendant pin
openXdox, or openDox?** The ruling says descendants pin openXdox, and for the
DomainxFactories that is right — they need the governance layer. But a domain
that wants the app without the governance interpretation (a clinic wanting a
document workbench, not an OpenSpec funnel) would want to pin openDox. If both
are possible the descendant standard grows a "which layer" declaration; if only
openXdox is possible, then openDox has exactly one consumer and its
independence is nominal.

## The install flow, and the topic it folds

`openxdox-install-app-provisioning` (staged 2026-08-14, five open questions,
exit unraised, and its own gate MET on the evidence) already designed the hard
part of a tenant install: GitHub has no app-creates-app API, so the installer
drives the **GitHub App Manifest flow** — a shipped manifest with permissions
pre-filled, the tenant name-and-confirms, GitHub creates the App in THEIR org
and returns credentials the installer captures within the hour. Two Apps stay
two (content-write in CI, dispatch-only for the exposed inbox) because that
separation is the security invariant. App names are globally unique, so the
convention is `openXdox — <tenant>`. The apply workflow lives in a small
dedicated repo the install creates, and the tenant's one real decision is which
repos the content App may write.

All of that survives into the per-tenant app install. What it gains is
everything the database brings: a Postgres instance to provision, credentials
for it that the tenant owns, ordered migrations to run at install and at
upgrade, and a backup posture. What it may lose is its subject: the topic was
scoped to the INTENT PLANE's credentials, and if the app writes to its own
database instead of dispatching an apply workflow into a repository, the
dispatch App may not be needed at all. That is not a reason to drop the topic —
the content App is still needed the moment git is a publication target — but it
means the topic's Q1 (contract home) should be answered inside the two-layer
change rather than on its own.

Measured state of the current runtime, so the install story is not written
against an imagined baseline: the public host `openxdox.opensoft.dev` is live
and auth-gated (HTTP 401); the QA intent plane passed 6/6 readiness on
2026-08-15 and both readiness results are expired and twenty days stale; the
apply lane `intent-apply.yml` has been dispatched exactly once, ever; the
nightly image-refresh lane has three runs and no successes; the OpsxFactory
workload set declares four workloads in namespace `dox` (`dox-auth`,
`dox-dashboard`, `dox-intent-inbox`, `dox-token-minter`); the DNS record exists
on the live zone but is ungoverned.

## Shared instance or always its own — the question this document cannot answer

Brett said "its own db". That reads as a per-tenant database, and every
sovereignty argument in the house supports it: the Hermes install is per-client,
the App-provisioning topic's whole design exists so that no opensoft identity
holds a key on tenant assets, and the readiness contract's serving-tier
separation is a physical boundary.

But "its own db" is compatible with at least three deployment shapes, and they
have very different costs:

1. **One instance, one database, per tenant.** Maximum isolation, maximum
   operational surface — N instances to upgrade, N migration runs, N backup
   policies. The Hermes install's actual shape.
2. **One shared instance, one database per tenant.** Isolation of DATA with
   shared runtime; upgrades are one deployment and N migration runs. Satisfies
   "its own db" literally while breaking sovereignty on the runtime.
3. **One instance and database per DOMAIN, tenants as rows.** Cheapest,
   contradicts the ruling as spoken, and is worth naming only so that nobody
   arrives at it by accident under cost pressure.

The choice interacts with the descendant pattern: a descendant repository per
domain suggests shape 1 or 2 (the descendant IS the deployment unit), whereas
shape 3 would make the descendant a tenant-agnostic distribution and put
tenancy entirely inside the app.

## Synthesis: what has to be true, in order

1. **Break the import cycle.** `doc_health` ↔ `ideation_dashboard` is two lazy
   imports of one class in one 377-line module in one direction and 23 imports
   in the other. Fix the cheap direction first. Nothing else can start.
2. **Name the corpus adapter.** One interface — enumerate, read/write,
   classify, assess, act — replaces a third of the package's knowledge of
   openxFactory's tree layout.
3. **Rule the authority boundary.** Database versus git, per object class. D5
   already fired for projects; the other six object classes need the same
   declaration before code is written, because an unstated split forks.
4. **Choose the runtime.** Adopt the Hermes install pattern or state why not.
5. **Then carve.** Two repositories, non-byte-identical, on the
   `split-openxwallet-repo` shape with the byte-identity floor replaced by
   something honest — a conformance corpus and a behavioural equivalence suite
   rather than eight matching digests.
6. **Then a descendant.** Lazily, on the first domain that stands one up —
   which is also the precedent's own trigger, and the trigger the 2026-09-04
   read-only review recommended waiting for.

Step 6 is where this ruling and that recommendation meet. The review's advice
was "not now, gate the split on the first real consumer"; the ruling is a
consumer being commissioned rather than waited for. Both can hold: steps 1
through 3 are worth doing whether or not the carve ever happens, because they
are the debts that make the current code hard to change.
