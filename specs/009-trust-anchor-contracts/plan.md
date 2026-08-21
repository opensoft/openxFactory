# Implementation Plan: Trust-anchor neutral contracts

**Feature**: `009-trust-anchor-contracts`
**Governing change**: `add-trust-anchor` (ratified 2026-08-21, Brett Heap)
**Spec**: [spec.md](spec.md) · **Decisions**: [research.md](research.md)

## Summary

Realize one ratified capability as neutral contracts: a `trust-anchor` family
covering anchors, certificates, issuance evidence, dependent bindings, renewals,
revocation propagation, realization conformance, and the closed chain-custody
registry the whole thing derives from. Three artifact kinds and no more: JSON
Schema under `contracts/trust-anchor/`, one validator under `scripts/`, and a
fixture corpus carrying a negative confirmation per requirement plus the ten
violations the change names. No authority, no anchor, no key, no runtime, no
existing capability touched.

## Constitution Check

| Principle | Disposition |
|---|---|
| I. Contract-first, domain-neutral core | PASS. Every requirement is an obligation on a RECORD or a WORKFLOW, never on a mechanism, and no schema names a product, protocol or vendor object model. Realization identity appears only as opaque `realization_ref` values in examples (`realization:core-self-hosted-authority`, `realization:managed-cloud-authority-canary`), which is what the change's D1 asks for. |
| II. OpenSpec before implementation | PASS. `add-trust-anchor` was ratified 2026-08-21 and authorizes exactly one Speckit feature. This is that feature; it implements nothing the change's tasks file does not name, and it stops short of task 5.10. |
| III. Document lifecycle | PASS. The family README carries `Status: ratified` naming the approving change. The promoted staging fragment carries `Status: draft` and names this change. No document claims `standard`. |
| IV. Schema and artifact discipline | PASS. Every YAML carries `schema_version` and `kind`. No host-absolute paths (`ROOT = Path(__file__).resolve().parents[1]`). No credentials, and by construction no key material — which is this feature's subject matter, so it is enforced at names, values and reversible encodings. |
| V. Validation gates | PASS. `scripts/validate-trust-anchor.py` self-tests over 32 positives and 43 intended-invalid fixtures; `openspec validate --all --strict` green; doc-health carries no new finding. Behaviour is proven by fixtures and a red-proof harness rather than asserted. |
| VI. Versioned, content-addressed releases | PASS by handoff. Registration in `contracts/manifest.yaml` with per-file digests and a `contracts/CHANGELOG.md` entry is change task 5.10, executed at the next additive bundle cut; the README says so rather than claiming a version this feature did not allocate. |
| VII. Fail-closed authority boundaries | PASS. The custody set, assurance ladder, refusal codes, establishment levels, satisfaction values and completion states are closed enumerations; unresolvable references are refused rather than passed over; and the guarantees that could be expressed as constants are (trust basis, standing basis, failure attribution, escalation class, brokering, revocation mechanism). |

No Complexity Tracking entries: nothing here requires a constitutional
exception.

## Technical context

- **Language**: Python 3 for the validator; YAML for contracts and fixtures.
- **Dependencies**: `pyyaml`, `jsonschema>=4.18` with `rfc3339-validator` for
  `format: date-time` — all already pinned in
  `requirements/hermes-runtime-contracts.in`. No new dependency.
- **Schema dialect**: JSON Schema Draft 2020-12 written in YAML, matching the
  `contracts/openxwallet/` family shape.
- **Runtime dependency**: the validator READS
  `contracts/openxwallet/openxwallet-custody.registry.yaml` at run time and holds
  every chain-custody member to the openxWallet member it claims to be. This is
  deliberate and is how the ratified "composes with rather than restates" clause
  becomes structural; the validator refuses to run without it (exit 2).

## Structure

```
contracts/trust-anchor/
  README.md
  chain-custody-registry.schema.yaml        # the mechanism
  trust-anchor-chain-custody.registry.yaml  # THE closed set
  trust-anchor.schema.yaml
  certificate-record.schema.yaml
  issuance-evidence.schema.yaml
  dependent-binding.schema.yaml
  renewal-record.schema.yaml
  revocation-propagation.schema.yaml
  conformance-declaration.schema.yaml
  examples/*.example.yaml
  examples/negative/*.yaml

scripts/validate-trust-anchor.py            # the canonical validator
specs/009-trust-anchor-contracts/evidence/red-proof.py
```

One directory, one capability. The change's D9 settled that two realizations do
not justify a profile seam — the axis of variation is OBLIGATION SATISFACTION,
which the conformance declaration handles inside one capability — so a profile
split would arrive as a NEW capability directory over this core, never as an edit
to these files.

## Design decisions this plan rests on

All recorded in full in [research.md](research.md); summarized here because they
shape the artifacts.

1. **Chain custody is a three-member closed set with `evidences` DERIVED** from
   two declared booleans asked of the USING HOST, with four enforced invariants —
   the derivation, the earned top level (rank-keyed), the ordering, and
   single-axis discriminator uniqueness. The last is how the ratified escrow
   ruling becomes structural rather than editorial.
2. **The set COMPOSES with openxWallet's** by naming its counterpart per member
   and resolving that mapping against the canonical registry at run time. A
   mapping nobody checks is how a second custody model arrives anyway.
3. **The issuance-evidence floor is two levels**, with the per-certificate fields
   UNREPRESENTABLE at the floor level, and the achieved level carried on the
   conformance declaration.
4. **Obligation entries are addressable and dated**, which is what makes the two
   ratified guards on the degraded-obligation rule enforceable across records.
5. **Where a guarantee could be a constant or an `if/then`, it is.** A record
   that cannot be authored is stronger than one that is authored and refused, and
   a schema constraint cannot be neutered by editing a validator.

## Approach to the negative corpus

The repository's dominant dialect is a first-line `# expected_failure:` header
with an optional `# expected_failure_detail:` substring pin. Both are used, plus
two additions:

- **`# requirement:` attribution and closed coverage.** The validator carries the
  eight ratified requirements as a closed list and fails when any has no probe,
  or when a fixture claims one that does not exist. That is what makes this a
  negative confirmation PER REQUIREMENT.
- **A red-proof harness** (`evidence/red-proof.py`). A green self-test proves the
  negatives fail; it does not prove they fail for the reason they name. The
  harness suppresses each finding code in turn and asserts the corpus goes red.

The detail pin carries more weight here than in most families, because so much of
this contract is enforced in the shape: a probe pinned only to `schema` would be
satisfied by any schema error at all. Exactly one fixture pins `schema` — the one
whose guarantee IS a constant — and it pins the const message.

The positive corpus is a single coherent story rather than a pile of valid
documents: two realizations (one self-hosted, one managed and not operated by the
family), five anchors, seven certificates including the undeclared-custody and
unexplained cases, three renewals including a correctly-recorded failure, and two
revocation propagations including an honestly escalated open exposure. Every
cross-record rule is exercised by records that agree with each other, which is
what makes a fixture that disagrees a real probe.

## Out of scope, by ratification

No certificate authority, anchor, key, credential, issuance or revocation
service, deployment topology or runtime. No product profiles (D9). No escrow
contract — that is the `client-credential-escrow-registry` topic's, and this
feature's job was to stay compatible with its direction rather than pre-empt it
(recorded in `research.md`). No administration workflow — that is the OpsxFactory
`pki-administration` successor's, by R7. No modification to any existing
capability. Registration at the bundle cut (task 5.10), the staging INDEX row and
the README "OpenSpec Records" entry are the change's bookkeeping, not this
feature's.
