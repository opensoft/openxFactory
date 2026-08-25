# Project-Type Template Library — Draft Archetypes — Brainstorm

Status: brainstorm
Kind: template
Summary: Fills the project layer's distinctive piece — a library of project-type
archetypes a project is provisioned from. Each archetype is a content bundle:
default policy (stricter-than-client/domain only), expected practices (from the
domain catalog), workflow selection, memory/consent posture, and default agents
(including the documentation help/manual writer for the doc-heavy types). Six
archetypes drafted — service, library, cli, application, infra-iac, spike —
spanning from external-facing/high-gate to quarantined/relaxed. Ownership:
archetype *content* is codex-owned (`hermes/customer/templates/<type>.yaml`);
the archetype *schema* is neutral (openxFactory). Parent:
`project-layer-scaffold.md`; consumes the practice catalog
(`codexfactory-domain-memory-and-practices.md`).
Topics: project, project-hermes, project-type-template, archetype, template-library,
project-policy, expected-practices, manual-writer, spike, infra-iac,
provisioning, subject
Repository context: openxFactory (schema neutral; content codexFactory hermes/customer/templates/)
Captured: 2026-07-21

## Possible feats

- **Neutral archetype schema** (`xfactory_project_type_template` — a neutral
  schema needs a neutral `kind`; codex archetypes are *instances* of it).
- **The six archetype content files** under `hermes/customer/templates/`.
- **`provision-project --type`** selection wired to the library.

## The archetype shape

```yaml
schema_version: 1
kind: xfactory_project_type_template   # neutral kind (openxFactory schema); this file is a codex instance
project_type:
  id: <service|library|cli|application|infra_iac|spike>
  subject_kind: repository
  default_policy: {...}          # deltas ON TOP of client + domain — stricter only
  expected_practices: [...]      # from the domain practice catalog
  workflows: [...]               # from the domain workflow catalog
  memory_boundaries: {...}
  consent_model: {...}
  default_agents: [...]          # Plane-2 workers this type pulls in
  risk_class: <low|medium|high>
```

## The six archetypes at a glance

| Type | Distinguishing policy | Expected practices | Manual-writer? | Risk |
| --- | --- | --- | --- | --- |
| **service** | external-facing; deploy credential gated (never standing); integration tests + monitoring | conformance-gate, governed-review-lane, credential-contracts, doc-health-sweep | no | medium-high |
| **library** | semver + no breaking change without major bump; `package_publish` gated | conformance-gate, governed-review-lane, credential-contracts, doc-health-sweep | **yes** (API docs) | medium |
| **cli** | release binaries; cross-platform; user manual prominent | conformance-gate, governed-review-lane, doc-health-sweep | **yes** (user manual) | low-medium |
| **application** | UX + accessibility; end-user help; user-data consent | conformance-gate, governed-review-lane, doc-health-sweep | **yes** (user guide) | medium |
| **infra_iac** | production/deploy heavily gated (human ack); change-window; drift monitoring | conformance-gate, credential-contracts (strict), governed-review-lane | no | high |
| **spike** | explicitly **non-releasable**; time-boxed; repo_read only; cannot merge to protected without graduating type | minimal / none required | no | low (quarantined) |

## Three worked examples

```yaml
project_type:
  id: service
  subject_kind: repository
  default_policy:
    realization: pr_only
    credential_posture: {deploy: gated_never_standing}
    security_posture: {external_facing: true, new_endpoint: requires_csc_clearance}
    required_extras: [integration_tests, monitoring]
  expected_practices: [conformance-gate, governed-review-lane, credential-contracts, doc-health-sweep]
  workflows: [approved-intent-intake, feature-decomposition, spec-kit-execution, deterministic-validation, branch-review, pr-admission, merge-readiness]
  consent_model: {deploy_actions: explicit_consent}
  default_agents: []
  risk_class: medium_high
```

```yaml
project_type:
  id: cli
  subject_kind: repository
  default_policy:
    realization: pr_only
    release: {artifacts: cross_platform_binaries}
  expected_practices: [conformance-gate, governed-review-lane, doc-health-sweep]
  workflows: [approved-intent-intake, feature-decomposition, spec-kit-execution, deterministic-validation, branch-review, pr-admission, merge-readiness]
  default_agents: [documentation_help_manual_writer]   # the user manual is a first-class deliverable
  risk_class: low_medium
```

```yaml
project_type:
  id: spike
  subject_kind: repository
  default_policy:
    releasable: false                     # hard: a spike may not ship
    merge_to_protected: forbidden_until_type_graduated
    credential_posture: {allowed_families: [repo_read]}
    time_box: required
  expected_practices: []                  # relaxed — nothing required
  workflows: [approved-intent-intake, feature-decomposition, spec-kit-execution]
  default_agents: []
  risk_class: low_quarantined
```

The spike archetype shows the library is not only about *adding* gates — it can
safely *relax* them, but only within a quarantine (non-releasable, no
production credentials, cannot reach a protected branch until the project is
deliberately graduated to a shippable type).

## How an archetype composes with the layers above

An archetype's `default_policy` is a **project-type delta on top of** the client
policy (which is itself stricter-than-domain). The stricter-only invariant
chains all the way down: domain → client → project-type → project instance, each
layer able to tighten, never loosen (except the spike's *quarantine*, which
relaxes gates only by also removing the ability to ship). The
`expected_practices` are what the domain's suggestion pipeline will check a
project of this type against.

## The manual-writer, placed

The documentation help/manual writer (raised for the project layer) is a
Plane-2 worker pulled in by the doc-heavy archetypes (library → API docs, cli →
user manual, application → user guide). It produces the project's user-facing
documentation — distinct from the domain's `documentation_agent`, which verifies
doc/traceability changes on any change. Not pulled in by service/infra/spike by
default.

## Open questions

- **Archetype drift** — if an archetype changes after a project is provisioned,
  does the project re-seed or is the archetype a one-time stamp? (From the
  umbrella; leaning: pinned stamp + explicit re-provision, like a domain re-pin.)
- **Type graduation** — the mechanism to graduate a spike into a shippable type
  (a governed transition, presumably PO-owned).
- **Archetype count** — are six enough, or are there codex-specific types missing
  (e.g. github-action, data-pipeline, notebook)?
- **Multi-type repos** — a monorepo holding a service + a library: one archetype
  with path scoping, or composed archetypes?
