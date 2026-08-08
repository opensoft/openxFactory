# Staged: Hermes Stack Topology per Client (company Hermes, domain stacks, and where requests enter)

Status: staged
Kind: architecture
Summary: Settle how many Hermes installations a company actually has and what
each one is for — one single-layer company/business Hermes per company, plus
one three-layer stack per (company x licensed DomainxFactory) — and decide
whether request intake/admission is realized at the existing Tenant Hermes
(cheap, contract-aligned) or waits on standing up a second domain stack.
Carries the verified cardinality constraints, the Omnigent multiplication
rule, and the one fixture that contradicts the per-client-stack reading.
Topics: hermes-topology, company-hermes, domain-stack, per-client-instantiation,
omnigent-instantiation, request-intake, admission-gate, licensing, opsxfactory-install
Repository context: openxFactory (neutral topology + intake contract) +
installs/hermes-install (runtime) + xFactories/OpsxFactory (consumer) +
codexFactory (consumer)
Staging ID: openxFactory:staging:hermes-stack-topology-per-client
Source: 2026-08-08 session — the council-clearance canary exposed that the
ratified "Client Hermes is the source of truth for outcome and client
communication" has no realization; scoping OpsxFactory's installability then
surfaced the cardinality constraints below.

## Verified facts (checked against contracts and the live stack, not recalled)

1. **A stack holds exactly one Tenant(client) + exactly one Domain + one or more
   Subject(customer) layers.** `three-layer-hermes-runtime` rejects a manifest
   declaring more than one Client or Domain layer *before any state is mutated*.
2. **Therefore one stack cannot serve two client companies, and cannot serve two
   domains.** Two companies = two stacks. Two DomainxFactories for one company =
   two stacks. This is the structural basis for "one 3-layer Hermes per
   (company x licensed domain)".
3. **A stack is pinned to one domain factory**: `stack_registration.domain_id`
   plus `domain_stack_pin.repository/commit/digest`. Layer content arrives as
   digest-pinned `overlay_manifest_pin`s read from that repo — so the domain
   definition is SINGULAR (one repo) and its INSTANCES are per-stack.
4. **Omnigent multiplies with the stack, not with the definition.** The neutral
   contract states the split verbatim: "core omnigent + per-domain overlay +
   per-tenant instantiation", and `omnigent-install-manifest` pins the Hermes
   runtime manifest as "the single stack identity, exactly one domain overlay
   (one tenant / one domain / N subject workloads)".
5. **The xFactory Hermes runtime cannot express a single-layer Hermes.** A
   manifest without a Domain layer or without at least one Subject layer fails
   validation. A company/business Hermes is therefore NOT an xFactory stack — it
   is the separate single-layer product (`FarHeap/Hermes-Install`), which the
   aggregation README already marks as deliberately distinct and never to be
   repointed.
6. **The live opensoft QA stack is three-layer, not single-layer**: Tenant
   `opensoft-company-policy`, Domain `codexfactory-software-engineering`,
   Subjects `project-alfa` + `project-bravo`. It already IS "codexFactory
   instantiated for the opensoft tenant".
7. **No licensing model exists in the contracts.** Searching openxFactory finds
   licence references only in ontology source metadata. "Licensed client" is a
   commercial concept with no contract, no record kind, and no gate today.

## The contradiction to resolve first

`contracts/hermes-runtime/fixtures/topology/ledgerx-client-company-hermes.yaml`
registers a **customer-role** layer whose display name is **"Client Company
Hermes"** — i.e. it models client companies as SUBJECT layers inside one domain
stack, not as one stack each. That is the opposite of the reading in fact 2.

Both readings satisfy the cardinality rule; they differ in what a Subject layer
MEANS per domain (codexFactory subjects are projects; Ledgerx subjects are
engagements per the ratified fix; this fixture's subjects are client companies).
Until this is settled, "one stack per licensed client" is an inference, not a
ratified rule — and it is the single highest-leverage question here, because it
decides whether onboarding a client is a stack install or a layer provision.

## The (a)/(b) decision this topic exists to make

**(a) Realize intake + admission at the existing Tenant Hermes.** The promoted
`client-infrastructure-request` capability already says "Client Hermes remains
the source of truth for outcome and client communication; the execution system
becomes the source of truth for privileged execution only after it returns an
accepted work-item reference." Today that is unrealized: the `cir-` request is a
YAML file, its approval is a git commit, and the Client Hermes role was played
by an agent in a chat window. (a) means: an intake route, an admission gate that
kills or admits, a pending-request discovery surface, and a notifier — at the
Tenant layer that already exists. Cheap, contract-aligned, and it unblocks the
"all requests enter Hermes first" goal immediately.

**(b) Additionally stand up an OpsxFactory domain stack.** Per facts 2-4 this is
a second installation: its own control plane, Postgres, ingress, Entra
registrations, federated credentials, principal rows, plus a per-tenant Omnigent
instantiation. OpsxFactory's repo side is largely ready — domain implementation,
4 profiles, 13 tenant records, and a validator that went green 2026-08-08 — but
it has no runtime binding manifest and its broker reports
`production_authority not_realized, service not_deployed`.

**(a) does not preclude (b), and (b) does not deliver (a).** Routing belongs to
the xFactory layer per the ratified layer model, so Hermes deciding *whether*
and the xFactory layer deciding *where* works with or without an Opsx stack.

## Open questions

- Does a client company get its own stack, or a Subject layer in the domain's
  stack? (The fixture contradiction above. Decides onboarding cost per client.)
- Is the company/business Hermes in openxFactory's scope at all, or does it stay
  FarHeap's single-layer product with a defined seam between them?
- Where do client stacks run — the opensoft tenant, or the client's own
  infrastructure? Nothing models hosting today.
- Should "licensed for domain X" become a modelled record (entitlement) or stay
  commercial/out-of-band?
- Opsx layer naming: the instantiation runbook recommends "Operations Domain
  Hermes / IT Subject Hermes / Managed System Hermes"; OpsxFactory's ratified
  `opsx-hermes-layer-model` names "Domain Hermes / Organization IT Hermes / IT
  Service Subject Hermes". The ratified spec wins; the runbook example is stale.

## Exit path

Target capability: a new neutral `request-intake-and-admission` capability
(Tenant-layer intake, admission gate, discovery, notification) plus an amendment
to the topology contract making the per-client stack-vs-layer rule explicit.
Delta type: additive contract + runtime realization in installs/hermes-install;
OpsxFactory and codexFactory conform as consumers. Proposal should not start
until the fixture contradiction and the (a)/(b) decision are settled.
