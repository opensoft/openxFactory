# Client Layer Content — policy-overrides, memory-boundaries, integration-boundaries — Brainstorm

Status: brainstorm
Kind: template
Summary: Fills the three client content files behind the house team: the client
policy overrides (the client's stored *delta* — always stricter-than-domain,
never weaker), the memory boundaries (the four per-tenant buckets and what may
promote to the domain), and the integration boundaries (allowed integration
classes, credential-reference-only policy, external-call clearance). Each has a
domain-suggested default (codexFactory `hermes/client/`) and a client-tuned
instance (wizard → `config/clients/<client>/`). Applies the store-the-delta
principle: the client stores its specific choices, not generic policy. Parent:
`client-layer-scaffold.md`; wizard: `client-policy-wizard.md`.
Topics: client-hermes, company-policy, policy-overrides, memory-boundaries,
integration-boundaries, auto-clear-envelope, store-the-delta, per-tenant-memory,
credential-references, client-layer
Repository context: openxFactory (targets codexFactory hermes/client/ defaults + hermes-install config/clients/<client>/)
Captured: 2026-07-21

## Possible feats

- **`hermes/client/policy-overrides.yaml`** (domain defaults) + per-client
  `operating-policy.yaml` / `approval-matrix.yaml` (wizard).
- **`hermes/client/memory-boundaries.yaml`** extending the existing org block.
- **`hermes/client/integration-boundaries.yaml`**.
- **The stricter-than-domain invariant** as an enforced check.

## policy-overrides.yaml — the client's stored delta

The client layer's job is "is this allowed *here*?", so its policy is the
organization's specific choices on top of the domain. The load-bearing
invariant: **client policy may only be stricter than the domain, never weaker** —
a client can add a gate or tighten a threshold, never dial a domain gate down
(the `policy_approval_gatekeeper`'s "stricter-than-domain gates"). Two layers,
same shape:

```yaml
schema_version: 1
kind: client_policy_overrides
relation_to_domain: stricter_only        # enforced: never weakens a domain gate
policy:
  repo_boundaries:
    may_touch: [<repo/path allowlist>]
    never_touch: [<denylist — e.g. infra, secrets, other tenants>]
  realization:
    mode: pr_only                        # no direct pushes to protected branches
  credential_posture:
    allowed_families: [repo_read, branch_write, pr_write]
    never_standing: [production, deploy, package_publish]
  spend_ceilings:
    runner_minutes_per_day: <n>
    hosted_compute: <cap>
  security_posture:
    new_external_call: requires_csc_clearance
    new_foreign_input_trigger: requires_csc_clearance
  approvers:                             # → approval_matrix
    change_approver: <named authority>
    security_approver: <named authority>
  escalation_path: [<ordered contacts>]
  auto_clear_envelope:                   # the "likely yes" middle for the clearance pipeline
    conjunctive:
      - practice_maturity: ">= standard"
      - risk_class: low
      - new_credentials: none
      - realization: pr_only
      - subject_class: non_production
      - domain: trusted_first_party
```

Domain default (codexFactory `hermes/client/policy-overrides.yaml`) ships
conservative starting values; the wizard writes the client's real values into
`config/clients/<client>/operating-policy.yaml` + `approval-matrix.yaml`.
Everything outside the envelope parks for the human liaison.

## memory-boundaries.yaml — four per-tenant buckets

Extends the existing org block in `hermes/client/template.yaml` (already:
`scope: per_tenant`, `retains: [team_roster, reviewer_groups, repo_access_policy,
ci_conventions, integration_inventory]`, `promotion_requires_domain_review:
true`). Maps the four neutral buckets to access + promotion rules, expressed in
the ratified memory gateway's vocabulary:

```yaml
schema_version: 1
kind: client_memory_boundaries
buckets:
  client_private_memory:
    scope: per_tenant
    retains: [team_roster, reviewer_groups, repo_access_policy, ci_conventions, integration_inventory]
    shared_with_domain: false
    cross_client: never                  # tenant isolation invariant
  customer_relationship_memory:
    scope: per_customer
    retains: [account_context, entitlement_state, relationship_status]
    visibility: client_private
  domain_learning_candidates:
    scope: promotable
    promotion_requires_domain_review: true    # de-identified, gateway promotion-candidate
  current_state_evidence:
    scope: installation_discovery
    retention: bounded
consent: gateway_consent_profile         # ratified memory gateway
invariant: tenant_isolated               # one client never sees another's memory
```

The invariant that matters: client memory is **tenant-isolated**; only
de-identified `domain_learning_candidates` cross upward, and only through the
domain-review promotion gate.

*How these buckets get populated* — federating over the org's real systems,
structure-before-embed, governed retrieval — is designed in
`hermes-knowledge-base-architecture.md` (the Cerebras pattern inside the gateway
rails); the client layer is its star case.

## integration-boundaries.yaml — allowed classes, references only

```yaml
schema_version: 1
kind: client_integration_boundaries
allowed_classes: [version_control, ci, ticketing, chat, calendar, crm]
credential_binding:
  form: reference_only                   # vaultref://… — never a secret in any record
  standing_forbidden: [production, deploy, package_publish]
external_calls:
  new_endpoint: requires_csc_clearance   # Client Security & Compliance Officer
  foreign_input_trigger: requires_csc_clearance
grant_readiness:
  requires: [named_binding, approval_authority, out_of_band_recovery_path]
```

## Why these are stored (store-the-delta)

All three are the client's *specific choices* — its repo allowlist, its
approvers, its spend caps, its tenant memory scope, its permitted integrations —
none of which a model could know or should improvise, and each of which a gate
enforces. The generic "handle credentials safely" knowledge is the model's; the
*specific families this client permits* is stored. Same line as the domain
policy model, drawn for the client.

## Open questions

- **Stricter-only enforcement** — is `relation_to_domain: stricter_only` checked
  mechanically (diff the client gate against the domain gate) or by review?
- **Default aggressiveness** — how conservative are the domain-shipped defaults
  before they become friction (everything parking) vs. risk (auto-clearing too much)?
- **Envelope authorship** — is the auto-clear envelope fully wizard-generated, or
  does it always require a human ratification of the conjunctive conditions?
- **Customer memory vs. Customer layer** — `customer_relationship_memory` here vs.
  the Customer/Project layer's own memory — confirm the boundary (client holds
  the *operator's* view of the customer; the customer layer holds the subject's).
- **Validator coverage** — the new per-client shapes (`operating-policy`,
  `approval-matrix`, `integration-map`) have no validator yet;
  `validate-client-infrastructure.py` covers only the infrastructure records.
  Each new kind needs a schema + check before the wizard's output can be trusted.
