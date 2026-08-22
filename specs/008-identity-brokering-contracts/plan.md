# Implementation Plan: identity-brokering neutral contracts

**Feature**: `008-identity-brokering-contracts`
**Governing change**: `add-identity-brokering` (ratified 2026-08-21, Brett Heap)
**Spec**: [spec.md](spec.md) · **Decisions**: [research.md](research.md)

## Summary

Realize one ratified capability as a neutral contract family: six JSON Schema
kinds under `contracts/identity-brokering/`, one canonical validator under
`scripts/`, and a fixture corpus carrying a negative confirmation per
requirement. No broker, no realm, no organization, no credential, no persona,
and no change to how any surface authenticates today.

## Constitution Check

| Principle | Disposition |
|---|---|
| I. Contract-first, domain-neutral core | PASS. Keycloak appears in no schema, enumeration or requirement — only in the family README's context line and in fixture prose naming the realization being adopted. Domain-shaped artifacts (the workbench, the gate console, HealthLinc's patient population) appear only as fixtures demonstrating the neutral shape. |
| II. OpenSpec before implementation | PASS. `add-identity-brokering` was ratified 2026-08-21 and authorizes exactly one Speckit realization feature. This is that feature; it implements nothing the change's tasks file does not name, and the two settlements it makes were assigned to it by change task 2.3. |
| III. Document lifecycle | PASS. The family README carries `Status: ratified` naming the approving change; the promoted staged fragment carries `Status: draft` naming this change. No document claims `standard`. |
| IV. Schema and artifact discipline | PASS. Every YAML carries `schema_version` and `kind`. No host-absolute paths (`ROOT = Path(__file__).resolve().parents[1]`). No credentials — and by construction no credential VALUE, which is this feature's subject matter twice over: the shapes close every object, and the validator scans names, values and reassembled chunks. |
| V. Validation gates | PASS. `scripts/validate-identity-brokering.py . --strict` reports 0 errors and 0 warnings; `openspec validate --all --strict` green; doc-health carries no new finding. Behaviour is proven by fixtures and a red-proof harness rather than asserted. |
| VI. Versioned, content-addressed releases | PASS by hand-off. Registration in `contracts/manifest.yaml` with per-file digests, the `contracts/CHANGELOG.md` entry and the README index rows are the change's task 1.11, executed at the next additive bundle cut. This feature authors the artifacts those rows will pin. |
| VII. Fail-closed authority boundaries | PASS. Every property set is a closed allow-list at every depth; every enumeration is closed; the never-mirror rule, the transport assertions, the pre-broker `presented_as_persona` claim and the surface's `human_accounts_held_by_surface` claim are required constants rather than optional booleans, so the conformant answer is the only representable one. |

No Complexity Tracking entries: nothing here requires a constitutional
exception.

## Technical context

- **Language**: Python 3 for the validator; YAML for contracts and fixtures.
- **Dependencies**: `pyyaml`, `jsonschema>=4.18` with `rfc3339-validator` for
  `format: date` / `format: date-time` — all already pinned in
  `requirements/hermes-runtime-contracts.in` and already required by every
  other canonical validator in the repository. No new dependency.
- **Schema dialect**: JSON Schema Draft 2020-12 written in YAML, matching the
  `contracts/openxwallet/` and `contracts/worker-enrollment/` family shape.
- **Runtime dependencies of the validator, both deliberate**: it reads the
  canonical layer ids and reserved layer terms out of
  `contracts/policies/layer-vocabulary.yaml`, and the admissible link bases and
  authorization resolution point out of the family's own schemas. Restating
  either would create the second vocabulary the requirements exist to prevent —
  the same technique `validate-openxwallet.py` uses for the job envelope's
  approval-policy terms.

## Structure

```
contracts/identity-brokering/
  README.md
  persona-assertion.schema.yaml            # kind: persona_assertion
  broker-organization.schema.yaml          # kind: broker_organization
  actor-subject-reference.schema.yaml      # kind: actor_subject_reference
  identity-link-record.schema.yaml         # kind: identity_link_record
  broker-client-declaration.schema.yaml    # kind: broker_client_declaration
  surface-adoption.schema.yaml             # kind: broker_surface_adoption
  examples/*.example.yaml                  # 14 positives
  examples/negative/*.yaml                 # 27 intended-invalid

scripts/validate-identity-brokering.py     # the canonical validator
specs/008-identity-brokering-contracts/
  evidence/red-proof.py                    # every finding code load-bearing
  evidence/red-proof-output.txt
```

One directory, one capability. There is no profile seam here as there is in
`openxwallet`: the six kinds are one capability's vocabulary, and a second
broker product would consume these shapes rather than add a sibling family.

## Design decisions this plan rests on

All five are recorded in full in [research.md](research.md); summarized here
because they shape the artifacts.

1. **The `actor_subject` shape is the STRUCTURED REFERENCE** (change task 2.3,
   design OQ-3) — issuer, opaque subject, display name at record, plus a
   provenance discriminator.
2. **History is marked at the boundary and mapped on demand** (change task 2.3,
   design OQ-1) — realized as the three provenance classes, with the wrong
   combinations unrepresentable and `presented_as_persona` a required constant
   `false`.
3. **The closed allow-list is DERIVED FROM THE SCHEMA**, not written as a
   second list. The design's named risk is that the mapping seam becomes the
   mirror one convenient field at a time, and a denylist admits every field
   nobody thought to forbid.
4. **`served` bridges to the canonical `subject` layer**, with the bridge's
   targets and the reserved terms checked against the ratified policy at run
   time.
5. **Structural enforcement wherever a claim could be omitted**: required
   constants (`transport.is_transport: true`,
   `transport.actor_of_governed_acts: false`,
   `transport.organization_membership_as_authority: false`,
   `pre_broker.presented_as_persona: false`,
   `human_accounts_held_by_surface: false`), single-member enumerations
   (`resolves_in: governed_layer`, `satisfied_by: dedicated_broker_instance`),
   `maxItems: 1` on the governed-record pointer, and conditional requirements
   binding mode to actor and write actions to posture.

## Approach to the negative corpus

The repository's dominant dialect is a first-line `# expected_failure:` header
with an optional `# expected_failure_detail:` substring pin. Both are used. The
detail pin is not optional in practice here: many of these fixtures ALSO fail
schema validation (a closed enumeration, a required constant, a conditional
requirement), so without the pin a fixture could drift into satisfying itself
with a generic `schema` finding and stop testing the invariant it is named for.

Three additions on top of the dialect:

- **`# requirement:` attribution and closed coverage.** The validator carries
  the nine ratified requirements as a closed list and fails when any has no
  probe, or when a fixture claims one that does not exist. That is what makes
  this a negative confirmation PER REQUIREMENT.
- **A red-proof harness** (`evidence/red-proof.py`). A green self-test proves
  the negatives fail; it does not prove they fail for the reason they name. The
  harness suppresses each finding code in turn and asserts the corpus goes red.
  All nineteen codes are load-bearing.
- **Nine probes beyond the eighteen the change names**, each for a ratified
  clause that would otherwise go unproven: the surface holding local human
  accounts (R1's second clause), membership offered as authority and a reserved
  layer term (R2, which the named list left without a probe), the self link
  from a session not holding the persona (R4's "already holding that persona"),
  an email address in the identifier position (R5's named substitution), a
  bearer token at rest and a secret split across chunks (R7's
  by-construction and reassembly clauses), a merge spanning instances (R8's
  personas-do-not-span-instances clause), and a write-posture surface naming no
  decision point (R9's decision-point clause).

## Out of scope, by ratification

No broker, realm, organization, deployment, credential, persona or user store.
No authorization model — memberships are asserted and decisions stay in the
governed layer; the per-action authorization delta that OQ-2 defers is a named
successor. No change to how any surface authenticates today; the htpasswd
workbench keeps working until the oauth2-proxy successor lands. No modification
to any existing capability. No obligation on any domain to adopt a broker, and
no instance-count mandate in either direction.

Registration (`contracts/manifest.yaml`, `contracts/CHANGELOG.md`, the
`contracts/README.md` index, the root README conformance bullet) and the
staging-index bookkeeping (change tasks 3.3–3.6) are outside this feature's
authoring surface and are executed by the change's own landing sequence.
