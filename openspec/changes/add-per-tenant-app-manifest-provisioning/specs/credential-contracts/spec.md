# credential-contracts Specification

ONE MODIFIED requirement. **NO ACTIVE CHANGE CARRIES A DELTA ON THIS
REQUIREMENT** — checked over all 46 active change directories at `origin/main`
`4cef77af`, 2026-09-16. Two active changes DO carry a `credential-contracts`
delta: `add-credential-escrow-checkout` (MODIFIED *Canonical credential record
shapes*, plus nine ADDED) and `add-requirement-ref-resolution-integrity` (two
ADDED). Neither writes *Dispatch-only credential least privilege and serving-tier
separation*, so the block below is written over CANON, restated as canon states
it today, and **no `Modified over` marker is owed**.

**Why this requirement has to grow, and why nothing existing covers it.** The
promoted requirement already states the dispatch/content separation as an
invariant of a credential that EXISTS — it is a rule about scope, bindings and
what a serving tier may hold. It says nothing about where the two credentials
COME FROM, and until now nothing had to: `opensoft`'s QA install created both
Apps by hand, in `opensoft`'s own organization, twice. RULING Q3
(`opensoft/openxFactory` issue #656, 2026-09-04T15:32Z) makes that a per-tenant
act — *"one instance and one database per tenant, always … No cross-tenant data
ever shares a store"* — so the pair is provisioned once per tenant, N times, in N
organizations this estate does not own. Provisioning is where the invariant is
easiest to lose: the cheapest way to stand up two Apps in somebody else's
organization is for an operator identity to create them, or to create one App and
widen it, and both defeat the separation the requirement already protects. The
growth below therefore says how the pair is CREATED, and it says it as a shape
rather than as a runbook, because the runbook is the installer's and lives in
`Omnigent-Install`.

**What is deliberately NOT modified here.** The other eleven requirements of this
capability are untouched, including *A credential binding declares the consuming
system that holds it and the identity it fetches with* and the six-condition
shared-`secret_ref` lift — a provisioned pair is two DISTINCT bindings on two
distinct secrets and reaches none of that machinery. No schema file moves, no
validator arm is authored, and no contract bundle number is reserved: this packet
is the SHAPE, and `tasks.md` § 3 carries the realization as a separate act.

**WHAT THIS BLOCK DOES NOT REPEAL, MEASURED RATHER THAN ASSUMED.** Canon keeps
BOTH operating models legitimate and says so in terms — *The credential vault
operator is an execution binding, never contract content* reads *"Both cases
SHALL remain legitimate. Self-hosted operation by an individual or a client is
not a degraded form of operator-hosted operation"*
(`openspec/specs/credential-contracts/spec.md:141`) — and the ratified runbook
`docs/openxdox-dispatch-credential-binding.md:31-37` records a LIVE
operator-hosted Case A in which the operator creates the dispatch App and holds
its key in the OPERATOR's vault. The clauses below are therefore scoped to the
shape they introduce rather than written over every provisioning that exists:
they bind provisioning THROUGH A PROVISIONING MANIFEST, they fix WHERE the
created identity lives and HOW its material is reached, and they leave WHO
OPERATES the install exactly where canon already puts it — a per-install
execution binding. Nothing below refuses a pair already in service that was
created by hand, and nothing below names a custody party: naming one in a
contract artifact is precisely what *An operated identity's credential is held in
governed custody and reached only by reference* forbids (`:216` — *"the neutral
obligation lives in the contract, the concrete estate fact lives in the
binding"*). Whether and when Case A migrates to the manifest shape is the
installer's act and the staged topic's unruled managed-flow question, and this
packet decides neither. Two of the added scenarios assert this reconciliation
rather than leaving it to the preamble.

## MODIFIED Requirements

### Requirement: Dispatch-only credential least privilege and serving-tier separation
A dispatch-only credential — one that exists to TRIGGER execution (a workflow dispatch or job kickoff) — SHALL be scoped to exactly the minimal permission required to trigger its one named target and nothing more (for a GitHub-hosted factory, `actions: write` on the single repository that owns the workflow), carrying no repository-contents authority. It SHALL be a DISTINCT binding from any content-write credential the same capability uses, and a zero-write-authority serving surface holding a dispatch-only credential MUST NOT hold — nor hold key material capable of minting — a content-write credential.

**WHERE THE SEPARATED PAIR IS PROVISIONED FOR A TENANT THROUGH A PROVISIONING
MANIFEST, EACH CREDENTIAL'S IDENTITY SHALL BE CREATED IN THE TENANT'S OWN
ORGANIZATION, AND SHALL NOT BE AN OPERATOR-OWNED IDENTITY INSTALLED INTO IT.** A
provisioning manifest is a committed, credential-free record that pre-fills the
identity's requested permissions, its subscribed events and its callback, and the
provider creates the identity only after a seat that administers the tenant's own
organization names and confirms it. The manifest SHALL pre-fill, per identity, NO
MORE THAN THE SCOPE THAT IDENTITY'S BINDING MAY HOLD — for the dispatch identity
that is the scope the paragraph above already fixes, its one named target and no
repository-contents authority; for the content-write identity it is the scope
that identity's own binding declares, which this clause READS rather than widens
and does not newly define — and a manifest pre-filling more than the binding may
hold is refused for the same reason the binding would be. No path in which the
identity created is an OPERATOR'S OWN — one the operator rather than the tenant
owns and can re-point — satisfies this clause, and neither does one provisioned
identity creating the other: an identity that can mint the pair is an identity
capable of minting a content-write credential, which the requirement above
already forbids the serving tier to hold.

**THIS BINDS WHERE THE IDENTITY LIVES, NOT WHO DRIVES THE FLOW AND NOT WHO HOLDS
ITS MATERIAL.** Who operates the install remains a per-install execution binding
under the vault-operator requirement this capability already carries; an
operator-executed install MAY drive the manifest flow on the tenant's behalf, the
identity it obtains being the tenant's either way; and a pair already in service
that was created without a manifest is NOT retroactively refused by this clause.

**THE PAIR IS PROVISIONED ONCE PER TENANT AND SHALL NOT BE SHARED ACROSS
TENANTS.** One tenant's pair SHALL NOT be reused, copied, or re-scoped to reach
another tenant's repositories, because a shared identity makes the separation
per-estate rather than per-tenant and puts one tenant's dispatch surface one
misconfiguration away from another tenant's contents. Where the provider's naming
space is GLOBAL, the provisioning manifest SHALL carry a DECLARED NAMING
CONVENTION that is unique per tenant and discoverable by pattern — the form
`<product> — <tenant>` — so that the identities belonging to one tenant can be
enumerated without reading that tenant's organization, and so that two tenants
never contend for one name.

**THE DISPATCH IDENTITY'S REACH IS THE ONE REPOSITORY THAT OWNS THE APPLY
WORKFLOW, AND THAT REPOSITORY IS PART OF THE PROVISIONING.** Provisioning SHALL
name the single repository the dispatch identity may trigger and SHALL NOT place
that workflow in a repository holding governed content, because a dispatch
identity scoped to a content-bearing repository is scoped to more than its one
named target however narrow its permission set reads.

**CREDENTIAL CAPTURE IS TIME-BOUND AND LEAVES WHOEVER DRIVES THE FLOW NOT AN
UNDECLARED CUSTODIAN.** Where the provider returns the created identity's secrets
ONCE and within a bounded exchange window, the provisioning record SHALL declare
that window and the DECLARED CUSTODY the material lands in — reached by reference
under the reference-delivered rule this capability already carries, its operator
the per-install execution binding this capability already fixes rather than a
party this contract names — and whoever drives the flow SHALL NOT retain the
material after the hand-off unless it IS that declared custodian. A provisioning manifest,
record or template SHALL carry NO secret value, private key or installation
token; it carries the SHAPE of the grant and the reference to where the material
will live, and a record carrying the material itself is refused.

#### Scenario: A dispatch credential requests contents authority
- **WHEN** a dispatch-only credential requirement or binding grants repository-contents write, or any scope beyond triggering its one named target
- **THEN** the validator MUST report an error

#### Scenario: A dispatch credential reuses the content credential's identity
- **WHEN** a dispatch binding names the same App or key identity as a content-write binding
- **THEN** it MUST be rejected, because the serving tier would then hold key material capable of minting a content-write token

#### Scenario: A correctly separated dispatch credential
- **WHEN** a dispatch-only credential is scoped to trigger exactly one named workflow on one repository, held as a binding distinct from the content-write credential
- **THEN** it is valid

#### Scenario: An install provisions the pair inside the tenant's organization
- **WHEN** a per-tenant install provisions the dispatch and content identities from committed provisioning manifests, each confirmed by the tenant's own seat, each created in the tenant's organization under a name unique to that tenant
- **THEN** the provisioning is valid, and the separation the pair already owes is preserved by construction rather than by configuration

#### Scenario: A manifest-provisioned identity turns out to be the operator's own
- **WHEN** a manifest-provisioned path yields a dispatch or content identity that the operator rather than the tenant owns and can re-point, or has one provisioned identity create the other
- **THEN** it is refused, because an identity that can mint the pair is key material capable of minting a content-write credential

#### Scenario: A provisioning manifest requests more than the binding may hold
- **WHEN** a provisioning manifest pre-fills a permission set wider than the scope the separated binding is allowed
- **THEN** it MUST be reported, on the same ground the binding itself would be

#### Scenario: One tenant's provisioned pair is pointed at another tenant
- **WHEN** a provisioned identity is reused, copied or re-scoped to reach a second tenant's repositories
- **THEN** it is refused, because the separation would become per-estate rather than per-tenant
- **AND** a naming convention that does not distinguish the two tenants is itself a finding, because it makes the reuse unreadable

#### Scenario: The apply workflow is placed in a repository holding governed content
- **WHEN** provisioning names a content-bearing repository as the dispatch identity's one named target
- **THEN** it is refused, because the dispatch identity would reach more than its one named target whatever its permission set reads

#### Scenario: A provisioning record carries the captured material
- **WHEN** a provisioning manifest, record or template carries a secret value, a private key or an installation token rather than a reference to the custody it lands in
- **THEN** it MUST be rejected, and the record is remediated rather than redacted in place

#### Scenario: An operator-executed install drives the manifest flow
- **WHEN** an install whose execution binding is operator-executed drives the provisioning manifest flow on the tenant's behalf, the identity still being created in the tenant's own organization and its material landing in the custody that install's binding declares
- **THEN** it conforms, because this requirement fixes where the identity lives and how its material is reached and leaves who operates the install a per-install execution binding

#### Scenario: A pair already in service was created without a manifest
- **WHEN** a dispatch and content pair in service predates this shape and was created by hand rather than from a provisioning manifest
- **THEN** the provisioning clauses do not retroactively refuse it, and whether it migrates to the manifest shape is that install's own act rather than this requirement's finding
