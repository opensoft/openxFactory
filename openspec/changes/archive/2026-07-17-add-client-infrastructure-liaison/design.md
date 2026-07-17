# Design: add-client-infrastructure-liaison

## Context

Source material: the six staged fragments in `supporting-docs/` (moved from
`ideation/staging/client-infrastructure-liaison` at the proposal gate; design
decisions there are LOCKED per the impact map). Precedents consumed:
`roles-authority-model` promoted spec + the archived
`add-github-app-identity-tiers` delta pattern (openxFactory); the promoted
`opsx-service-subject-model` (typed request-role projection, subject
taxonomy) + archived `add-github-administration-workflow` (OpsxFactory);
document-cataloging and credential-contracts as the two contract-family
shapes; `hermes-runtime/layer-lifecycle-event` as the lifecycle-in-YAML
precedent. The fragments' proposal sequence required the OpsxFactory
service-subject refinement FIRST — that archived 2026-07-10, so this change
is unblocked.

## Goals / Non-Goals

**Goals:**
- Land the neutral liaison role + request contract so client-tenant
  infrastructure dependencies are coordinated with full traceability and
  zero authority leakage to domain agents.
- Make completion evidence-gated (fresh readiness result), transitions
  actor-authorized, and secrets structurally impossible in the record.
- Close the github-administration-plane client-tenant carve-out.

**Non-Goals:**
- No per-domain adoption (successor changes per the impact map's sequence).
- No OpsxFactory-side implementation (execution binding, readiness producer,
  privileged-gate mapping stay OpsxFactory-owned).
- No new always-running agent, no new secret store, no job-envelope change.

## Decisions

**D1 — `execution_binding` reconciliation (the one fragment divergence).**
The primary fragment uses `execution_binding.type:
client_sysadmin|opsxfactory|managed_host_provider` with string profiles; the
request-contract fragment uses `execution_binding.mode` with object profiles
plus idempotency/correlation/digest fields. Ruled: the request-contract
fragment is authoritative (it is the fuller, later shape and carries the
invariants). Field is `execution_binding.mode` with closed enum
`client_managed | managed_host | opsxfactory_executed`, mapping the primary
fragment's tokens (`client_sysadmin`→`client_managed`,
`managed_host_provider`→`managed_host`, `opsxfactory`→
`opsxfactory_executed`) and the upstream prose vocabulary (customer-managed /
managed-host / full OpsxFactory). `managed_host` is SHOULD-support per the
primary fragment; the other two are MUST. Fragments stay unedited; this
ruling governs.

**D2 — Contract-family shape: document-cataloging registration,
credential-contracts residency.** openxFactory owns schemas + governing doc
+ examples + validator, registered in `contracts/manifest.yaml` at
realization (schemas as `type: schema` entries with sha256; validator as
`type: tool`, invoked from the pinned checkout, never copied). Instance
records (`client_infrastructure_request`, readiness results, handoff
records) live in client installs/domain repos — like credential grants,
openxFactory ships the shape, never the instances.

**D3 — Two schemas, not three.**
`xfactory-client-infrastructure-request.schema.yaml` carries the request
kind with `$defs` for the six identity-reference classes, execution binding,
approval, communication, package refs, conditions, and the embedded
`handoff` acceptance record (the handoff is a facet of the request's
correlation story, same lifecycle).
`xfactory-infrastructure-readiness-result.schema.yaml` is separate: produced
by trusted validators, different producer/lifecycle/trust policy, statuses
`ready|degraded|not_ready|unknown|maintenance`, `valid_until` freshness.
Draft 2020-12, `contract_schema_version: 1`, `additionalProperties: false`,
per-kind files (house preferred style).

**D4 — Lifecycle: closed state enum in schema, legality in the validator.**
States and the transition matrix land normatively in the capability spec and
governing doc; the schema closes the `status` enum; transition legality,
authorized-actor classes, and guards are deterministic `check_*` functions
in `validate-client-infrastructure.py` (hermes-runtime precedent: schema
shapes records, validator enforces what JSON Schema cannot). Conditions
(`overdue`, `escalated`, `maintenance_hold`, `awaiting_external_response`)
are an orthogonal array with type/active/observed_at/policy_ref — never
status values. Terminals: `declined`, `cancelled`, `completed`; reopening
completed work requires a new request with `supersedes_request_ref`.

**D5 — roles-authority-model delta: narrow and additive.** MODIFY only
"GitHub App identity tiers": extend its final exclusion sentence to route
client-tenant infrastructure through this change's model, and append one
scenario ("Client-tenant execution routes through the liaison"). Full
existing body + all three scenarios reproduced verbatim (tiers-change
pattern; OpenSpec replaces whole requirements). "Structural parking in
external enforcement" is NOT touched — its authority-separation principle
is already enforcement-system-neutral and binds the liaison as-is.

**D6 — Validator scope (deterministic checks mandated by the fragments).**
`scripts/validate-client-infrastructure.py`: kind-keyed, skip-with-notice
for foreign kinds, self-tests packaged examples. Checks beyond schema:
(a) embedded-secret rejection (value-shaped fields; denylist patterns —
reuse `contracts/avatar-client/redaction/` pattern of bounded sentinels);
(b) transition legality incl. terminal immutability and
completed-requires-fresh-readiness (freshness = `valid_until` not passed at
transition time, result status `ready`, all mandatory checks passed);
(c) identity-class separation (`execution_binding.actor_ref` ≠
`approval.authority_ref`; subject ids never in actor/capability/authority
fields — mirrors the OpsxFactory projection rule);
(d) idempotency/supersedes integrity (duplicate idempotency_key must
reference the same open request; `supersedes_request_ref` only from a
terminal predecessor).

**D7 — Scaffold wiring.** The liaison joins
`templates/client-layer/product-service-scaffold.yaml` as a named
coordination profile: default `configured_but_inactive` with a declared
responsible operator + escalation path; `activation_blocking: true` when any
declared component requires an external operator. The activation gate
(operating model selected; owner + execution/approval authorities assigned;
primary + out-of-band paths; validation profiles + trusted validators named;
response/restoration/escalation targets; one exercised failure-and-recovery
scenario) is spec-level, template carries the fields.

## Risks / Trade-offs

- [Vocabulary collision with OpsxFactory] → consume-don't-rename rule: the
  neutral change adopts `client_infrastructure_request` + the three binding
  names already coined upstream; OpsxFactory workflow/credential/subject
  tokens are referenced, never redefined; checked in the verify panel.
- [Scope creep into domain adoption] → hard Non-Goal; successor changes per
  the impact map; the only cross-repo text here is the handoff *shape*.
- [Fragment divergence resurfacing] → D1 ruling recorded; fragments kept
  verbatim as provenance with the README note; validator enforces the ruled
  shape.
- [Liaison becoming a shadow admin] → the request record structurally
  separates actor/authority refs; the roles delta keeps authority-separation
  binding; grants are referenced opaquely (`credential_grant_ref`), never
  carried.
- [Readiness freshness gamed by stale results] → `valid_until` + trust
  policy are schema-required; the completed-transition check is
  deterministic and negative-tested.

## Migration Plan

Additive only. Order: schemas + examples + validator (self-test green) →
governing doc + README doc-index + contracts/README pending-realization row
→ specs deltas → scaffold template wiring → strict validation + verify panel
→ land. Realization (successor step, this change's final task): manifest +
CHANGELOG + release digests + tag at the next bundle cut, then archive.
Domain adoptions follow as their own changes.

## Open Questions

- None blocking: the fragments' decisions are locked; the one divergence is
  ruled (D1). Product-owner veto points: D1's enum tokens and D5's scenario
  wording — flag at proposal review before the specs are treated as settled.
