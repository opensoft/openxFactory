# Party Ladder

Status: draft
Kind: reference
Summary: The neutral four-rung party model every DomainxFactory
instantiates — product author/operator, tenant, subject, modeled third
parties — with the frozen-machine-word reading rules (including the
two-meaning `client` token), the subject-policy rung, the
rung-attachment rule for third parties, and the self-client pattern.
Restates ratified vocabulary and constraints with citations; introduces
no new normative requirements.
Topics: party-ladder, terminology, subject-tenant-domain,
layer-vocabulary, counterparty, persona, self-client,
governed-derived-model
Repository context: openxFactory

Every xFactory install serves a chain of parties. The chain is the same
in every domain; only the rung names change. Getting the rungs confused
is the single most common vocabulary failure in this product family
(the review §A1 "Client Hermes" collision was a rung confusion), so
this document is the one place the ladder is stated neutrally. The
binding vocabulary is the ratified Subject/Tenant/Domain trio
(`adopt-subject-tenant-domain-vocabulary`; machine mapping at
[`contracts/policies/layer-vocabulary.yaml`](../contracts/policies/layer-vocabulary.yaml)).

## The four rungs

| Rung | Neutral name | What it is | Hermes layer | Frozen machine words |
| --- | --- | --- | --- | --- |
| 0 | **Product author / operator** | Authors and ships the factory (Opensoft; openxFactory contracts + the DomainxFactory product). Optionally also the managing operator, per install profile (`client_managed` / `managed_host` / `opsxfactory_executed`). | not a Hermes layer — present as the pinned contract source and, when managing, through the client-infrastructure liaison | (none — repo/product identity) |
| 1 | **Tenant** | The organization that purchased and operates the factory: the firm, the agency, the clinic, the IT operator, the engineering org. Owns staff, service catalog, review routing, operating procedure. | the tenant layer (e.g. Firm Hermes) | role key `client` |
| 2 | **Subject** | The served party whose truth and policy bind the work: the firm's client company, the advertiser, the patient, the managed service subject, the project. | the subject layer (e.g. Engagement Hermes) | role key `customer`; domain subject kinds (e.g. `client_entity`, `advertiser`) |
| 3 | **Modeled third parties** | Parties the subject cares about but who hold no authority in the stack: the subject's customers and vendors (counterparties), the advertiser's consumers (personas), synthetic cases (dream objects). | never a layer — governed objects inside a declared scope | domain subject kinds (e.g. `counterparty`, `persona`) |

Rungs are **roles, not identities** — one organization can occupy more
than one rung (see the self-client pattern below).

## Reading rules for the frozen machine words

Machine identifiers are frozen until the next major contract bundle;
all meaning lives in prose. Three rules keep reading safe:

1. **Role key `client` = tenant.** In `stack.yaml`
   `hermes.layers[].role`, `client` always means the tenant-operator
   (rung 1).
2. **Isolation scope `per_client` = per subject.** In
   `tenancy.isolation`, `per_client` means per client-of-the-tenant —
   rung 2 scope. The same frozen token means *tenant* as a role key and
   *per-subject* as an isolation scope. Never interpret the token by
   intuition; interpret it by which field it sits in, via the
   layer-vocabulary mapping.
3. **Prose never says "client" or "customer" unqualified.** Say
   *tenant*, *subject*, *counterparty*, or the domain display word
   (firm, client company, advertiser, patient). "Customer company" is
   banned — it collides with the frozen `customer` role key. Domains
   that had subject kinds literally named `client` renamed them via
   registry alias while zero instances existed (`client → advertiser`
   in AdxFactory, `client → client_entity` in LedgerxFactory).

## Subject policy: rung 2 carries its own rulebook

The subject is not just a data scope — it is a policy source. The
subject's own operating policy (a client company's accounting policy
and chart of accounts, an advertiser's brand truth and restricted
claims, a patient's consent profile) binds all work done for that
subject, composed **stricter-rule-wins** with domain standards and
tenant procedure (the composition rule the omnigent contract fixes).
Domain policy says what the profession requires, tenant policy says how
this operator works, subject policy says how this subject's work must
be done — the tightest rule governs.

## The rung-attachment rule for third parties

Every modeled third party belongs to exactly one scope — a counterparty
of *subject X*, a persona of *advertiser Y* — and never floats between
rungs or subjects. This restates, vertically, the walls the ratified
capabilities already enforce horizontally:

- no cross-subject edges or intelligence sharing without domain-layer
  review with attribution severed (AdxFactory cross-advertiser wall,
  LedgerxFactory cross-client wall);
- third parties hold no authority: edges never carry authority-class
  fields, and derived models of third parties are non-authoritative by
  construction with a declared scope dial
  ([Governed Derived Model](governed-derived-model.md)).

Practical consequence: an intake pipeline's trust gates resolve an
inbound party against exactly one subject's registry. A sender that
resolves against no registry is either a new-third-party onboarding
case *for a specific subject* or not that pipeline's business — it is
never handled "generally".

## The self-client pattern

Because rungs are roles, the tenant may register itself as a subject of
its own tenancy — the firm keeping its own books, the agency marketing
itself, Opensoft running a self-client install of its own factory (the
precedent: the opensoft self-client QA install). The tenant-as-subject
gets an ordinary rung-2 scope: its own policy, its own third-party
registry, the same pipelines with zero special cases. Rung-0 parties
appear naturally this way too: Opensoft invoicing a tenant for the
factory license is just a counterparty (`vendor_of`) of the
tenant-as-subject.

## Per-domain instantiation

| Rung | codexFactory | MedxFactory | OpsxFactory | LedgerxFactory | AdxFactory |
| --- | --- | --- | --- | --- | --- |
| 1 Tenant | Engineering Organization Hermes | Care Organization Hermes | Organization IT Hermes | Firm Hermes | Marketing Organization Hermes |
| 2 Subject | Project Hermes | Patient Hermes | IT Service Subject Hermes | Engagement Hermes (`client_entity`) | Advertiser Hermes (`advertiser`) |
| 3 Third parties | (unmodeled today — upstream dependencies/services are candidates) | dream objects + simulation scenarios (synthetic; dream objects are **domain-scoped**, showing rung-3 scope is a declared dial, not always per-subject) | (unmodeled today — external providers of the managed estate are candidates) | counterparties (`customer_of`/`vendor_of`) + health profiles/scenarios | personas + campaign simulations |

## See also

- [Terminology And Repository Topology](terminology-and-repo-topology.md) —
  the repo/stack/layer ownership model (this doc is its runtime-party
  companion).
- [`contracts/policies/layer-vocabulary.yaml`](../contracts/policies/layer-vocabulary.yaml) —
  the binding machine mapping.
- [Governed Derived Model](governed-derived-model.md) — the ratified
  contract for rung-3 derived models (tiers, dials, validator).
- [Subject Hermes Memory Model](customer-hermes-memory-model.md) and
  [Tenant Hermes Product And Service Scaffold](client-hermes-product-service-scaffold.md) —
  the rung-2 and rung-1 layer content models.
- [xFactory Domain Factory Model](xfactory-domain-factory-model.md) —
  the full stack model this ladder threads through.
