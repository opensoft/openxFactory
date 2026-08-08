# Implementation Plan: openxWallet neutral contracts

**Feature**: `006-openxwallet-contracts`
**Governing change**: `add-openxwallet` (ratified 2026-08-07, Brett Heap)
**Spec**: [spec.md](spec.md) · **Decisions**: [research.md](research.md)

## Summary

Realize two ratified capabilities as neutral contracts: a holder-agnostic
`openxwallet` core and its first profile `openxwallet-agent-profile`. Three
artifacts, no more: JSON Schema families under `contracts/`, one validator
under `scripts/`, and a fixture corpus carrying a negative confirmation per
requirement. No runtime, no key material, no existing capability touched.

## Constitution Check

| Principle | Disposition |
|---|---|
| I. Contract-first, domain-neutral core | PASS. Both families are domain-neutral. The one domain-shaped artifact — the LedgerxFactory posting constraint — appears only as a fixture demonstrating the neutral shape, with the domain named in `declared_by` rather than encoded in the schema. |
| II. OpenSpec before implementation | PASS. `add-openxwallet` was ratified 2026-08-07 and authorizes exactly one Speckit feature. This is that feature; it implements nothing the change's tasks file does not name. |
| III. Document lifecycle | PASS. Both family READMEs carry `Status: ratified` naming the approving change. No document claims `standard`. |
| IV. Schema and artifact discipline | PASS. Every YAML carries `schema_version` and `kind`. No host-absolute paths (`ROOT = Path(__file__).resolve().parents[1]`). No credentials — and by construction no key material, which is this feature's subject matter. New docs linked into the README index. |
| V. Validation gates | PASS. `scripts/validate-openxwallet.py` self-tests; `openspec validate --all --strict` green; doc-health carries no new finding. Behaviour is proven by fixtures and a red-proof harness rather than asserted. |
| VI. Versioned, content-addressed releases | PASS. Schemas registered in `contracts/manifest.yaml` with per-file digests, a `contracts/CHANGELOG.md` entry, and a bundle version allocated at realization. |
| VII. Fail-closed authority boundaries | PASS. The custody set, authority ladder, holder classes, refusal codes and event classes are all closed enumerations; unrecognized values are refused. The capability is an authority control that fails closed and never degrades open. |

No Complexity Tracking entries: nothing here requires a constitutional
exception.

## Technical context

- **Language**: Python 3 for the validator; YAML for contracts and fixtures.
- **Dependencies**: `pyyaml`, `jsonschema>=4.18` with `rfc3339-validator` for
  `format: date-time` — all already pinned in
  `requirements/hermes-runtime-contracts.in`. No new dependency.
- **Schema dialect**: JSON Schema Draft 2020-12 written in YAML, matching the
  `contracts/worker-enrollment/` family shape.
- **Runtime dependency**: the validator READS the legal approval-scope
  vocabulary out of `contracts/schemas/hermes-job-envelope.schema.yaml` at run
  time. This is deliberate and is the point of profile requirement 3 — one
  vocabulary rather than two kept in agreement.

## Structure

```
contracts/openxwallet/                     # the holder-agnostic core
  README.md
  openxwallet-record.schema.yaml
  openxwallet-custody-registry.schema.yaml
  openxwallet-custody.registry.yaml        # THE closed set
  openxwallet-grant.schema.yaml
  openxwallet-grant-exercise.schema.yaml
  openxwallet-distinct-holder-constraint.schema.yaml
  openxwallet-subject-attestation.schema.yaml
  examples/*.example.yaml
  examples/negative/*.yaml

contracts/openxwallet-agent-profile/       # the first profile, a sibling
  README.md                                #   family: a NEW capability over
  openxwallet-agent-composition.schema.yaml#   the core, not a modification
  examples/*.example.yaml
  examples/negative/*.yaml

scripts/validate-openxwallet.py            # one validator, both families
```

The two directories mirror the two capabilities. That is the structural
expression of the core/profile seam the change calls its substance: a patient
or practitioner profile arrives as a third directory, never as an edit to the
first.

## Design decisions this plan rests on

Both are recorded in full in [research.md](research.md); summarized here
because they shape the artifacts.

1. **Custody is a three-member closed set with `evidences` DERIVED** from two
   declared booleans, and three enforced invariants make the collapse the
   handoff warns about structurally impossible rather than discouraged.
2. **Composition components declare a binding mode** (`content` or
   `reference`), which dissolves the include-or-exclude-the-corpus binary: a
   corpus is bound by identity and governing configuration, not by contents.

## Approach to the negative corpus

The repository's dominant dialect is a first-line `# expected_failure:` header
with an optional `# expected_failure_detail:` substring pin. Both are used.
The detail pin is not optional in practice here: several probes would
otherwise satisfy themselves with a generic `schema` finding and stop testing
the invariant they are named for.

Two additions on top of the dialect:

- **`# requirement:` attribution and closed coverage.** The validator carries
  the eleven ratified requirements as a closed list and fails when any has no
  probe, or when a fixture claims one that does not exist. That is what makes
  this a negative confirmation PER REQUIREMENT.
- **A red-proof harness** (`evidence/red-proof.py`). A green self-test proves
  the negatives fail; it does not prove they fail for the reason they name.
  The harness suppresses each finding code in turn and asserts the corpus goes
  red. All twenty codes are load-bearing.

## Out of scope, by ratification

No runtime, wallet infrastructure, key storage, issuance service, or signing
implementation. No patient or practitioner profile — each is a NEW profile
capability over the same core, gated on its own consumer. No certification
batteries, measured drift, or qualification tiers. No modification to any
existing capability. Creating a key, credential, or wallet is out of scope.
