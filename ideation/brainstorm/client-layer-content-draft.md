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
Topics: client, client-hermes, company-policy, policy-overrides, memory-boundaries,
integration-boundaries, auto-clear-envelope, store-the-delta, per-tenant-memory,
credential-references, client-layer
Repository context: openxFactory (targets codexFactory hermes/client/ defaults + hermes-install config/clients/<client>/)
Captured: 2026-07-21

Updated: 2026-07-22 (stricter-only mechanics + envelope ratification + memory-seam decisions; cost wiring; validator package)

## Decided (2026-07-22)

- **Stricter-only: mechanical + review fallback.** Fields with defined
  comparison semantics (§Comparability spec) are checked mechanically at seed
  time (pipeline step 4), fail-closed; fields with no natural partial order
  **park for review** — never a silent pass.
- **Envelope authorship: wizard drafts, human ratifies.** The wizard composes
  the conjunctive envelope from answers; the responsible operator explicitly
  ratifies it before anything auto-clears. The envelope is the single riskiest
  artifact the wizard writes — it never activates un-ratified.
- **Customer-memory seam confirmed.** The client's
  `customer_relationship_memory` holds the *operator's* view (account,
  entitlement, relationship); the Customer/Subject layer holds the *subject's
  own* view (its state, its consent). Two records, never merged storage;
  cross-referencing only through governed gateway reads.

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
  budget_envelopes:                      # FAO-owned (client-layer-roster-draft §11)
    runner_minutes_per_day: <n>
    hosted_compute: <cap>
    credits_per_project: <n>             # clock-in ledger rolls up against these
  tracking_granularity:                  # the contract the subject layer must honor
    level: per_task | per_job | per_worker_run   # cost-accountability-and-efficiency-model.md
    set_by: finance-accounting-officer
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

## Comparability spec (what "stricter" means, per field)

The mechanical half of the stricter-only decision — comparison semantics per
field class; anything not listed here parks for review:

| Field class | Stricter means | Check |
| --- | --- | --- |
| allowlists (`may_touch`, `allowed_families`, `allowed_classes`) | client set ⊆ domain set | subset |
| denylists (`never_touch`, `never_standing`, `standing_forbidden`) | client set ⊇ domain set | superset |
| numeric ceilings (`budget_envelopes.*`) | client value ≤ domain default | ≤ |
| numeric floors (coverage new-code threshold) | client value ≥ domain floor | ≥ |
| clearance requirements (`requires_csc_clearance`, approvers) | client may add required approvals, never remove | add-only |
| auto-clear envelope (`conjunctive`) | client may ADD conjuncts or tighten one, never remove or loosen | conjunctive-add-only |
| enums with a declared order (`realization: pr_only` > direct) | client at or above the domain's rung | ordered |
| free-text / structural fields (escalation_path ordering, …) | **no partial order — park for review** | review |

## Validator work package (the exit for the coverage gap)

One package, consumed twice: JSON-schemas for the new kinds
(`client_policy_overrides`, `client_memory_boundaries`,
`client_integration_boundaries`, plus the wizard outputs `operating-policy`,
`approval-matrix`, `integration-map`) and a `validate-client-content` check
implementing the §Comparability spec. The **wizard** runs it at write time and
the **seeder** runs the same check at step 4 — one implementation, two
enforcement points, so the wizard can never write what the seeder would
reject.

## Why these are stored (store-the-delta)

All three are the client's *specific choices* — its repo allowlist, its
approvers, its spend caps, its tenant memory scope, its permitted integrations —
none of which a model could know or should improvise, and each of which a gate
enforces. The generic "handle credentials safely" knowledge is the model's; the
*specific families this client permits* is stored. Same line as the domain
policy model, drawn for the client.

## Open questions

- ~~**Stricter-only enforcement**~~ — DECIDED 2026-07-22: mechanical + review
  fallback (§Decided; semantics in §Comparability spec).
- **Default aggressiveness** — how conservative are the domain-shipped defaults
  before they become friction (everything parking) vs. risk (auto-clearing too
  much)? The envelope-ratification decision softens the stakes: nothing
  auto-clears un-ratified regardless of defaults.
- ~~**Envelope authorship**~~ — DECIDED 2026-07-22: wizard drafts, human
  ratifies, always (§Decided).
- ~~**Customer memory vs. Customer layer**~~ — CONFIRMED 2026-07-22:
  operator's view vs. subject's view, never merged (§Decided).
- ~~**Validator coverage**~~ — scoped as the §Validator work package: one
  implementation, enforced at wizard write time and seeder step 4. Still
  open: which repo hosts the schemas (openxFactory contracts, as usual?).
