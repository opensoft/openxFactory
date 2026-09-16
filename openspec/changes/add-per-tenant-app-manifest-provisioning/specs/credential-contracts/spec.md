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

## MODIFIED Requirements

### Requirement: Dispatch-only credential least privilege and serving-tier separation
A dispatch-only credential — one that exists to TRIGGER execution (a workflow dispatch or job kickoff) — SHALL be scoped to exactly the minimal permission required to trigger its one named target and nothing more (for a GitHub-hosted factory, `actions: write` on the single repository that owns the workflow), carrying no repository-contents authority. It SHALL be a DISTINCT binding from any content-write credential the same capability uses, and a zero-write-authority serving surface holding a dispatch-only credential MUST NOT hold — nor hold key material capable of minting — a content-write credential.

**WHERE THE SEPARATED PAIR IS PROVISIONED FOR A TENANT, EACH CREDENTIAL'S
IDENTITY SHALL BE CREATED IN THE TENANT'S OWN ORGANIZATION THROUGH A DECLARED
PROVISIONING MANIFEST, AND NEVER BY AN OPERATOR IDENTITY ACTING INSIDE IT.** A
provisioning manifest is a committed, credential-free record that pre-fills the
identity's requested permissions, its subscribed events and its callback, and the
provider creates the identity only after the tenant's own seat names and confirms
it. The manifest SHALL declare, per identity, exactly the scope the requirement
above already fixes — dispatch on the one named target, content-write on the
declared document repositories — and a manifest requesting more is refused for the
same reason the binding would be. No path in which an operator's own identity
creates, owns or holds the tenant's identity satisfies this clause, and neither
does one identity creating the other: an identity that can mint the pair is an
identity capable of minting a content-write credential, which the requirement
above already forbids the serving tier to hold.

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

**CREDENTIAL CAPTURE IS THE TENANT'S, IS TIME-BOUND, AND LEAVES THE INSTALLER NOT
A CUSTODIAN.** Where the provider returns the created identity's secrets ONCE and
within a bounded exchange window, the provisioning record SHALL declare that
window and the custody the secrets land in — the tenant's own vault, by reference,
under the reference-delivered rule this capability already carries — and the
installer SHALL NOT retain them after the hand-off. A provisioning manifest,
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

#### Scenario: An operator identity creates the tenant's credential identities
- **WHEN** a provisioning path has an operator-owned identity create, own or hold the tenant's dispatch or content identity, or has one provisioned identity create the other
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
