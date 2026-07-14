code_surface: none
target_release: implemented

## Why

A single GitHub App (`openxfactory`) currently does both content work
(reports, review-record PRs, pin syncs) and holds org-wide `Contents: write`,
which also lets it bypass the branch protection/rulesets that the ratified
"Structural parking in external enforcement" requirement (`roles-authority-model`)
relies on to make human-review gates fail-closed against agent misbehavior. A
2026-07-10 review-lane live run exposed this: the content-only identity has
control-plane power it should never have, and nothing in the neutral
authority model currently forbids that. This change closes the gap at the
neutral layer by requiring that any external-enforcement identity capable of
modifying a structural human-review gate be authority-separated from any
identity that performs ordinary content/workflow actions on the same surface,
and by defining the resulting content-vs-administration App identity tiers
and their credential-custody obligations.

## What Changes

- Extend the "Structural parking in external enforcement" requirement (or add
  an adjacent requirement in the same spec) so that an identity able to
  modify a structural human-review gate MUST be authority-separated from any
  identity performing ordinary content/workflow actions on that same
  enforcement surface — closing the gap the requirement did not previously
  cover.
- Define, as a neutral authority-boundary concept, two GitHub App identity
  tiers: a **content identity** (does factory work — reports, review-record
  PRs, pin syncs — under the rules) and an **administration identity** (sets
  the rules — org/repo rulesets, branch protection — applied only via the
  governed review lane + ratify gate). Neither tier may escalate the other:
  the content identity cannot change the rules; the administration identity
  performs no content work.
- Require least-authority credential custody for any administration-tier
  identity: a vaulted private key, narrowed runtime grants (short-lived,
  workflow-scoped, human-approved), and audited actions — reusing the
  existing, already-promoted `credential-contracts` record shapes as-is (this
  change does not modify that spec).
- Scope this tiering explicitly to identities operating on Opensoft's own
  vendor build org. Per-client-tenant execution bindings are out of scope
  (see Impact).

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `roles-authority-model`: add the App-identity-tier separation requirement
  (content vs. administration, neither escalates the other) and the
  administration-tier credential-custody obligation, extending the existing
  "Structural parking in external enforcement" requirement's guarantee to
  cover who may configure the enforcement mechanism itself.

## Impact

- Affected docs: `docs/roles-and-authority.md` (neutral authority-model doc)
  and `openspec/specs/roles-authority-model/spec.md`.
- Does not modify `credential-contracts` (`contracts/schemas/xfactory-credential-contracts.schema.yaml`)
  — its five record kinds are reused unchanged as the shape for the
  administration identity's credential requirement/binding/grant/audit
  records.
- Enables, but does not itself implement, a sibling OpsxFactory-local
  OpenSpec change (`github-administration`) that instantiates this tiering
  as an actual second App, a dedicated write workflow, and concrete
  credential records for Opensoft's own vendor org.
- Out of scope: client-tenant GitHub administration (whether a client runs
  its own GitHub org or a customer repo hosted inside Opensoft's org, and who
  administers it) is a separate, not-yet-proposed concern that routes through
  the staged `client-infrastructure-liaison` topic's execution-binding model,
  not through this change.
