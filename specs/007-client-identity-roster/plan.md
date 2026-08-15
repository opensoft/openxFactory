# Implementation Plan: client identity roster neutral contracts and conformance wiring

**Feature**: `007-client-identity-roster` | **Branch**:
`007-client-identity-roster` | **Date**: 2026-08-14

**Governing change**: `openspec/changes/add-client-identity-roster/` — ratified
2026-08-14 by Brett Heap, AMENDED the same day (Decisions A and B,
`review/amendment-record-2026-08-14.md`).

**Spec**: [spec.md](spec.md) · **Rulings**:
[clarify-rulings-2026-08-14.md](clarify-rulings-2026-08-14.md) ·
**Decisions and derivations**: [research.md](research.md)

**Plan-gate rulings applied**:
[plan-gate-rulings-2026-08-14.md](plan-gate-rulings-2026-08-14.md) — the
architect's rulings on the cross-model adversarial review of this plan and
research.md at `913c3ca` (17 decisions: 11 upheld, 5 amended, 1 broken; 4 new
issues). Every ruling in that file is encoded below: R-N1 (uniqueness key
element 3 = `authority_class_intended`, Cluster A), A-2 (Cluster A), A-3a/A-3b
(Cluster H), A-5/A-6/A-7 (Cluster I), A-9 (Cluster G), A-11 (Cluster C,
including the re-counted FR-016 coverage table), A-16 (Cluster D precondition),
A-N2 (Cluster F residual), A-N3 (ratified-constraint row 7), A-N4 (verification
story, SC-006). R-N1's verification obligation was discharged before encoding:
the sweep of every ratified mention of the uniqueness key — spec.md constraint
6 / FR-006 / FR-035 / Key Entities, the roster delta's uniqueness requirement
and its four scenarios, design.md Decision 2, the proposal's item 2, the
decision-review record, and the seed handoff's killed-flaw block — found NO
text implying the ACHIEVED authority class participates in uniqueness. Every
one spells the third element "authority class" unqualified.

## Summary

Realize the ratified identity layer as neutral contracts and wire it three
ways. One new schema file owning two record kinds (the per-(client, domain)
roster fragment and its drift finding); one canonical validator with a
two-layer corpus that carries a negative confirmation per rule AND the
killed-flaw regression positives; packaged examples spanning two fragments for
a two-domain client; registration at `contract-v1.32`. Then the four MODIFIED
capabilities: the conformance pack grows to four checks so intra-repo
conformance BLOCKS, doc-health grows a sixteenth family so cross-domain
composition REPORTS, `credential-contracts` gains a closed
`issuance_preconditions` vocabulary so the drift refusal has a neutral home,
and `consent-instrument` grows `withdrawn` plus a governed-identity dependent
kind so withdrawal reaches the identity and not merely its credentials.

No client-tenant act, no credential minting, no live provider call, no network
access, no domain-repository edit.

## Constitution Check

*GATE: passed before Phase 0 research; re-checked after the design below.*

| Principle | Disposition |
|---|---|
| I. Contract-first, domain-neutral core | PASS, and on the exact posture rather than a rounded one. The schema constrains shape; `blast_radius_unit` and `duty` are domain-declared tokens bound to provider-native identifiers in a per-fragment legend. Provider-native values ride VERBATIM and are never INTERPRETED by the neutral layer: a permission's identifier stays in `granted_permissions[].id` and a scope token stays in `achieved_scope`. Where a check needs a fact ABOUT one of those values, the fact is DECLARED by the domain that owns it — `achieves` and `reaches[]` beside the permission id (FR-004, FR-009), `exceeds_governed_unit` beside the scope token (FR-002) — never inferred from spelling and never resolved against a provider catalogue. That is what keeps the core neutral while leaving the rules checkable; the rounded claim "these fields are opaque" would hide the three declarations an architect reviewing this principle should look at. `admission_surface` and `identity_kind` are provider-named but closed BY RATIFICATION (FR-007) and extended only by the change that governs a new member. Domain fragments are explicitly not deliverables (FR-030). |
| II. OpenSpec before implementation | PASS. `add-client-identity-roster` is ratified and amended; this is its Speckit realization. Nothing here extends the packet's scope — the two amendments were ratified BEFORE planning, and the plan adds no fifth modified capability. |
| III. Document lifecycle | PASS. New docs (`examples/client-identity-roster/README.md`) carry `Status: ratified` naming the change. `Status: record` review files are never edited or appended; any amendment lands as a sibling record file (research.md, last section). |
| IV. Schema and artifact discipline | PASS. Every new YAML carries `schema_version` + `kind`; `.example.yaml` files are instantiation stubs, never live configuration; validator root is `Path(__file__).resolve().parents[1]` so no host-absolute path is committed; no credential, provider payload, or tenant secret enters the tree — the packaged BC case records app/object/sp identifiers and permission names only, and its source record already states `credentials: none`. New docs are linked into `README.md`'s index and `contracts/README.md`'s registration table. |
| V. Validation gates | PASS. The green bar is enumerated below and is the SC-010 list verbatim. Behaviour is proven by fixtures and a discrimination measurement (genuine pairs pass, alias pair refused), not by assertion. |
| VI. Versioned, content-addressed releases | PASS. `contract-v1.32` allocated at realization: manifest bundle version, per-file `sha256`, CHANGELOG entry, regenerated release digest inventory, atomic commit. `contract_schema_version` bumps on the two consent schemas; the record envelope's `schema_version` const does NOT change (research.md, "A registration gap FR-021 assumes away"). Additive-minor is the claim, and `docs/contract-versioning-policy.md:130-132` is the test it is held to. |
| VII. Fail-closed authority boundaries | PASS. SEVEN closed vocabularies refuse unrecognized values — FR-034's six entry-side sets plus the drift record's `status` (SC-014, as re-scoped by the checklist pass) — and each has its own refusal probe; the two open tokens are pattern-bound and legend-bound. The drift record refuses grant issuance while `open` — a fail-closed lever that mutates nothing. No model call anywhere; the cross-domain family is a deterministic recompute. |

**Complexity Tracking**: no entries. Nothing here requires a constitutional
exception.

## Ratified-constraint check

The spec's ten binding constraints are the harder gate. Each is dispositioned
against the design below; encoding them is the work.

| # | Constraint | Where the design encodes it |
|---|---|---|
| 1 | Residency is class-independent | `residency_model` is a top-level entry field with no branch on `authority_class_*` anywhere in schema, validator, examples or docs. Cluster A/B. |
| 2 | Blocking scope is all three | Pack membership (Cluster F), doc-health family (Cluster G), `issuance_preconditions` (Cluster H). |
| 3 | The enrollment axis stays permissive | No completeness predicate exists in any code path; `planned` is a first-class positive fixture; absence exits 0 with a notice (FR-032, SC-013). |
| 4 | Done means records AND consent cascade AND doc-health family | All three are archive-blocking clusters, plus OpenSpec tasks 3.1/3.3 per the amendments (governing-change numbering, not this feature's Speckit ids). Only domain fragments are exempt. |
| 5 | `admission_surface` CLOSED to two members | Cluster A enum + one negative (SC-014). |
| 6 | Five-element tuple; classes `observe\|mutate` only | Cluster A `$defs.identity_key`, whose third element is `authority_class_intended` by ruling R-N1 (see "The uniqueness key's third element" below); Cluster C carries a GENUINE per-unit pair and a GENUINE duty pair as ZERO-finding positives alongside the alias-pair negative — the discrimination is the measurement (SC-002). |
| 7 | `granted_permissions[]` and `admission[]` (a LIST) survive | Both required on every entry; `admission` is `type: array, minItems: 1`. A one-member `admission[]` array IS a legal single-act expression — an identity admitted through exactly one act is conformant and common. What FR-002 makes unrepresentable is the SCALAR form: an `admission` that is not a list at all. An implementer reading this row as "two acts required" and writing `minItems: 2` would break legitimate entries; `minItems: 1` is the correct and intended bound (ruling A-N3). |
| 8 | No client-tenant act, no minting, no live call | Every artifact is a schema, a fixture, a deterministic reader, or a document. The validator opens files; the doc-health family reads pinned checkouts; `tests/hermeticity.py` makes external binaries structurally unreachable for the suite. |
| 9 | Two ratified amendments | Clusters F and H are archive blockers, not successors. |
| 10 | No completeness rule ships | Same as 3; SC-013 measures it three ways, including "no code path derives an expected entry set". |

## Technical context

- **Language**: Python 3 for the validator and the doc-health family; YAML for
  contracts, examples and fixtures. No new dependency: `pyyaml` and
  `jsonschema>=4.18` (Draft 2020-12) are already pinned and already used by
  every sibling validator.
- **Schema dialect**: JSON Schema Draft 2020-12 written in YAML, with
  `$schema` and `$id` declared (the consent-instrument family's shape; the
  older `xfactory-credential-contracts.schema.yaml` predates that convention
  and is not retrofitted here).
- **Determinism / hermeticity**: filesystem reads only. No network, no model
  call, no subprocess to a provider tool. `tests/conftest.py` registers
  `tests/hermeticity.py` for every directory under `tests/`, which makes the
  ambient `nlm`/`gh` binaries refusals — the suite-wide guard SC-011 leans on.
- **Consumption shape**: canonical validators run FROM the pinned openxFactory
  checkout against a target repository handed as an explicit argument, and are
  never copied into a domain repo. Exit codes 0 clean / 1 findings / 2 harness
  error.
- **Scale**: one new schema file (2 kinds), one new validator, one new
  doc-health family module, ~35 packaged fixture files (31 negatives, two
  positive fragments, the drift example, a README), four modified
  capabilities' surfaces, one bundle cut.

## Project structure

### Documentation (this feature)

```text
specs/007-client-identity-roster/
├── spec.md                              # ratified requirements (exists)
├── clarify-rulings-2026-08-14.md        # the ruling record (exists)
├── plan.md                              # this file
├── research.md                          # decisions and derivations
├── traceability.yaml                    # authored at implementation, in the
│                                        #   006 file's ACTUAL shape: envelope
│                                        #   (schema_version, kind:
│                                        #   openxfactory_realization_traceability,
│                                        #   feature, ratified_change,
│                                        #   capabilities) + `requirements:`
│                                        #   rows carrying statement, artifact,
│                                        #   enforced_by, negative_confirmation,
│                                        #   red_proven
└── tasks.md                             # /speckit.tasks output, not this phase
```

### Repository (openxFactory only — no domain repo is touched)

```text
NEW
contracts/schemas/xfactory-client-identity-roster.schema.yaml
    kinds: xfactory_client_identity_roster
           xfactory_client_identity_drift_finding

scripts/validate-client-identity-roster.py
scripts/doc_health/client_identity_composition.py

examples/client-identity-roster/
├── README.md                                                # Status: ratified
├── client-identity-roster-farheap-opsx.example.yaml         # BC worked case (2 acts),
│                                                            #   multi-surface reader,
│                                                            #   planned entry
├── client-identity-roster-farheap-ledgerx.example.yaml      # duty-separated pair,
│                                                            #   per-unit pair,
│                                                            #   retired entry
├── client-identity-drift-finding.example.yaml
└── negative/                                                # one file per rule
    ├── consent-recorded-as-access.yaml
    ├── unverified-act-counted-as-access.yaml
    ├── undeclared-reach.yaml
    ├── achieved-exceeds-intended-undeclared.yaml
    ├── achieved-class-contradicted-by-permissions.yaml       # FR-004 (ruling A-11)
    ├── scope-exceeds-unit-undeclared.yaml                    # FR-002/FR-010 (analyze R6)
    ├── undeclared-act-surface.yaml                           # FR-009 act side (checklist)
    ├── name-understates-achieved-authority.yaml
    ├── missing-enforcement-test.yaml
    ├── provider-enforced-without-per-unit-principal.yaml
    ├── per-unit-principal-undeclared.yaml                    # FR-008 coverage (checklist)
    ├── per-unit-principal-available-but-logical.yaml
    ├── vendor-homed-declared-client-resident.yaml
    ├── vendor-tenant-multi-missing-obligations.yaml
    ├── mutate-without-ratified-capability.yaml
    ├── entry-without-consent-instrument.yaml
    ├── false-standing-credential-attestation.yaml
    ├── destructive-authority-class.yaml
    ├── admission-surface-out-of-vocabulary.yaml
    ├── residency-model-out-of-vocabulary.yaml
    ├── enforcement-mode-out-of-vocabulary.yaml
    ├── lifecycle-state-out-of-vocabulary.yaml
    ├── identity-kind-out-of-vocabulary.yaml
    ├── full-tuple-duplicate.yaml
    ├── alias-pair-observationally-identical.yaml
    ├── legend-token-missing.yaml
    ├── legend-token-declared-twice.yaml
    ├── evidence-ref-malformed.yaml
    ├── drift-finding-without-roster-value.yaml
    ├── drift-finding-without-observed-value.yaml
    └── drift-finding-status-out-of-vocabulary.yaml           # SC-014's 7th set (checklist)

tests/client-identity-roster/test_client_identity_roster.py  # repo-context rules,
                                                             #   SIX tmp_path repos
                                                             #   (see Cluster C)
tests/doc-health/test_client_identity_composition.py
tests/doc-health/fixtures/client-identity-composition/       # 2+ fixture repos

MODIFIED
contracts/schemas/xfactory-credential-contracts.schema.yaml  # + issuance_preconditions
contracts/schemas/consent-instrument.schema.yaml             # + withdrawn (x2),
                                                             #   + governed_identity,
                                                             #   + 2 evidence fields,
                                                             #   contract_schema_version 1→2
contracts/schemas/consent-instrument-class-registry.schema.yaml  # + withdrawn,
                                                             #   contract_schema_version 1→2
scripts/validate-credential-contracts.py                     # + semantic precondition check
scripts/validate-consent-instruments.py                      # + withdrawn, + cascade rule
scripts/doc_health/families.py                               # import, FAMILIES, docstring
scripts/doc_health/__init__.py                               # FAMILY_IDS
tests/conformance-gate/test_conformance_checks.py            # pack grows to four
examples/credential-contracts/                               # + 1 positive, + 2 negatives
                                                             #   (unknown token; false value)
examples/consent-instrument/                                 # + 1 positive, + 2 negatives
contracts/manifest.yaml                                      # bundle v1.32 + 4 rows
contracts/CHANGELOG.md                                       # v1.32 entry
contracts/README.md                                          # registration rows
contracts/releases/contract-v1.32.digests.yaml               # generated
README.md                                                    # doc index + OpenSpec Records

NOT EDITED (deliberately)
openspec/specs/doc-health/spec.md                    # FR-025; archive rewrites it
openspec/specs/domain-conformance-checks/spec.md     # same rule, same reason
openspec/specs/consent-instrument/spec.md            # same rule, same reason
openspec/changes/add-client-identity-roster/review/* # Status: record, immutable
tests/doc-health/test_suite.py                       # measured: its determinism
                                                     #   test is tag-hygiene-specific
                                                     #   (:15-19) and it carries no
                                                     #   all-families iteration, so a
                                                     #   sixteenth family needs no edit
                                                     #   here — the new family's own
                                                     #   determinism assertion lives in
                                                     #   test_client_identity_composition.py
xFactories/**                                        # FR-030, SC-012
```

**Structure decision**: `examples/<family>/` (ruling C3) because the schema
lives in `contracts/schemas/`; ONE schema file owning two kinds (research.md
Decision 2); the validator standalone with no shared helper module, matching
every sibling.

---

## Design by deliverable cluster

### Cluster A — the roster schema family

One file, `contracts/schemas/xfactory-client-identity-roster.schema.yaml`,
Draft 2020-12, `$schema` + `$id` + `contract_schema_version: 1`, a top-level
`oneOf` over the two kinds, `additionalProperties: false` on every object.

**Both kinds declare `schema_version: const: 1`** (ruling A-2). The record
envelope's `schema_version` is the value the manifest row mirrors, and this
family registers as ONE row for ONE file; declaring the same const on both
branches is what makes that single row unambiguous. Neither kind may carry a
different envelope version while they share a file, a digest and a
`consumption_rule`. (`contract_schema_version: 1` on the FILE is the separate,
schema-level number — the distinction research.md records under "A registration
gap FR-021 assumes away".)

**Kind 1 — `xfactory_client_identity_roster`** (the fragment): `schema_version`,
`kind`, `client_ref`, `domain`, `legend`, `entries[]` (`minItems: 1`).

`legend` binds every free token used in the fragment to its provider-native
identifier: `{blast_radius_units: {<token>: <provider identifier>}, duties:
{<token>: <provider identifier>}}`. A YAML mapping makes "declared twice"
unrepresentable at the schema level for the same key; the DUPLICATE case
FR-034 requires as a finding is therefore a token appearing in BOTH maps.
FR-034's two legend findings — a token used with no legend entry, and a token
declared twice — are the WHOLE legend rule set, each with its own negative
(`legend-token-missing.yaml`, `legend-token-declared-twice.yaml`). **A legend
entry that no entry uses is NOT a finding in this release**: no requirement
makes it one, it fires on a conformant fragment whose entry is `retired` or
`planned`, and inventing it would add a rule with no negative confirmation
(FR-016) on the permissive axis ratified answer 3 protects.

Each entry carries the ratified field list of FR-001, unreduced, plus nothing
except the two consequences of ruling R7 that FR-001 records — the fragment's
legend, and the entry's optional `duty_separation_rationale`:

| Field | Shape |
|---|---|
| `identity_ref` | string — the identity's own provider-facing name |
| `identity_kind` | closed enum, ONE member (research.md Decision 1) |
| `home_tenant` | string — the tenant the REGISTRATION is homed in |
| `principal_locations[]` | array of tenant identifiers |
| `residency_model` | closed enum: `client_tenant_single`, `vendor_tenant_multi` |
| `admission_surface` | closed enum: `business_central`, `exchange`; each MEMBER's `description` names the admission act and the scoping mechanism that make it a surface (below) |
| `duty`, `blast_radius_unit` | pattern `^[a-z0-9][a-z0-9_-]*$`, legend-bound |
| `duty_separation_rationale` | OPTIONAL string — the declaration FR-038's alias rule reads (below) |
| `authority_class_intended` / `_achieved` | closed enum `observe\|mutate` |
| `granted_permissions[]` | `minItems: 1`; each member an OBJECT — `id` (the provider-native identifier, verbatim), `achieves` (`observe\|mutate`), `reaches[]` (admission-surface members) — see below |
| `admission[]` | LIST, `minItems: 1` — see below |
| `declared_excess` | optional object: `spanned_surfaces[]`, `provider_reason`, `bound_mechanism`, `gate_obligation`, `enforcement_test_ref` |
| `per_unit_principal_available` | MAPPING `admission_surface` member → boolean; keys constrained to the enum by the schema, and REQUIRED to cover the entry's own surface plus every `spanned_surfaces[]` member — a coverage rule the validator enforces (Cluster B), because the schema cannot make a key set depend on another field's value. FR-008 is per-surface, and a missing key is indistinguishable from `false` unless it is named |
| `lifecycle_state` | closed enum `planned\|enrolled\|retired` |
| `standing_credential_attestation` | object: `no_standing_credential` (boolean claim), the approved grant-window reference, and the evidence pointer — see below |
| `ratified_by` | domain-qualified capability id |
| `consent_ref` | instrument citation |

`admission[]` members: `surface`, `act`, `achieved_scope` (provider-native),
`enforcement_mode` (closed: `provider_enforced`, `logic_enforced`),
`evidence_ref`, `verified_at`, `exceeds_governed_unit` (boolean, required —
below). `evidence_ref` is a DECLARED POINTER — `{repo, path, sha?}` (FR-037) —
and an act with no `evidence_ref` is `verified: false` by derivation, never by
independent assertion, so an unverified act cannot claim verification.

**`evidence_ref` and `verified_at` are a PAIR, expressed as
`dependentRequired` in BOTH directions** (checklist pass; FR-002, FR-003,
FR-033). Both optional, but each requires the other: present-present is a
VERIFIED act, absent-absent is the UNVERIFIED state FR-003 requires to stay
representable, and `verified_at` WITHOUT `evidence_ref` is refused as
`unverified-act-counted-as-access` — the record claiming a verification it
cannot evidence. Before this pairing the derivation had no firing rule: with
`verified_at` required on every act, an unverified act was unrepresentable;
with it merely optional, the negative FR-016 names by that very phrase had no
refusal predicate at all and would have passed. The pairing is what makes
"consent is never access" checkable at the ACT level, as the union rule makes
it computable at the ENTRY level.

**`exceeds_governed_unit` exists because `achieved_scope` is an OPAQUE TOKEN
and the change's own motivating measurement must be checkable.** Ruling R7
keeps `achieved_scope` provider-native, so the neutral layer may compare two
scope tokens for equality and MUST NOT read breadth out of one. Every rule that
touches `achieved_scope` is satisfied by that limit — the alias rule needs
equality, the genuine per-unit pair needs inequality, the drift record carries
the tokens verbatim — with ONE exception: the worked case's second act, the
admin-center authorization with NO SCOPE SELECTOR that reaches every environment
while the entry governs `sandbox1`. Knowing that act EXCEEDS the unit is
breadth, not equality; comparing its token to the legend's binding for the unit
would detect DIFFERENCE, not excess, and would fire on a legitimately narrower
act. So the fact is DECLARED, exactly as `granted_permissions[]` declares
`achieves` and `reaches[]` rather than having them inferred:
`exceeds_governed_unit: true` on an act whose achieved scope reaches beyond the
entry's `blast_radius_unit`.

Two things follow, and they are the whole reason for the field:

1. **The degradation rule fires** (Cluster B): a VERIFIED act declaring
   `exceeds_governed_unit: true` REQUIRES a `declared_excess` carrying its four
   fields; without one, `undeclared-scope-excess` names the act, its achieved
   scope and the governed unit. Before this, an entry could declare a
   tenant-wide no-selector act, omit `declared_excess` entirely, and pass every
   rule in the corpus — FR-009 checks SURFACES, FR-010 checks CLASS, and
   FR-008's per-surface rule is satisfied by act 1's use of the per-unit
   principal.
2. **Effective reach becomes computable**: the union of verified acts is the
   set of `(surface, achieved_scope)` pairs over VERIFIED acts only, plus the
   derived flag `exceeds_governed_unit = OR over those acts`, emitted as a
   per-entry note. That OR is the ratified "the effective reach is their union,
   NOT the narrower act": one verified no-selector act carries the whole
   entry's reach past the governed unit regardless of the narrower act.

The field changes no ratified spelling — `achieved_scope` stays provider-native
and verbatim — and the FR-038 alias tuple keeps EXACTLY its four ratified
elements `(surface, act, achieved_scope, enforcement_mode)`; the flag is a
statement about a scope, not part of observational identity.

**Member spellings are snake_case everywhere** — `client_tenant_single`,
`vendor_tenant_multi`, `provider_enforced`, `logic_enforced`, alongside
`business_central`, `entra_app_registration`, `planned|enrolled|retired`. The
hyphenated English forms used in prose here, in spec.md and in the ratified
delta ("a client-tenant-single model", "provider-enforced") name the same
members and are prose, never a second token spelling.

`vendor_tenant_multi` obligations (tenant allow-list enforced at token
validation, per-client authorization state, per-client revocation evidence,
the cross-client credential-span statement, the per-client consent amendment)
are required by an `if/then` on `residency_model` — expressible in schema and
therefore expressed there, so the obligation cannot be lost in a validator
refactor.

**Each `admission_surface` member DEFINES itself by its act** (FR-007's second
clause, and packet task 2.2 verbatim: "Each entry names its admission act and
scoping mechanism"). The member `description` carries both — for
`business_central`, BOTH acts of the worked case (the per-environment
application user, scoped by environment; the admin-center Entra-app
authorization, which has no scope selector); for `exchange`, its own act and
scoping mechanism. This is what makes the axis falsifiable: a member is a
surface because an act exists separately, not because a product is named.
research.md Decision 8's standing rule applies to these descriptions as it does
to packaged examples — a surface description may not assert a provider fact the
builder cannot cite, and an uncitable `exchange` act or mechanism ESCALATES by
the route ruling A-16 defines rather than being invented. The
`authority_class` member descriptions likewise name FR-005's conformant
expression (destructive capability rides the `mutate` entry's achieved class
and gate obligation), so the Cluster B refusal can cite the route and not only
the closed set.

**`granted_permissions[]` members are OBJECTS, because two ratified rules read
them.** FR-004 requires `authority_class_achieved` to be CHECKABLE against the
granted permissions and FR-009 requires undeclared reach to name "the surface
and the permission that reaches it" — neither is decidable from an opaque
provider string without a provider catalogue (forbidden: network-free) or an
invented inference about provider naming. spec.md's Assumptions block already
fixes the answer: "the mapping from a permission identifier to an achieved
authority class is DECLARED IN THE RECORD and checked for internal consistency,
not resolved against any provider catalogue." So each member carries:

- `id` — the provider-native identifier VERBATIM (`API.ReadWrite.All`), which is
  the fidelity ruling R7 protects;
- `achieves` — `observe` or `mutate`, the class that permission confers;
- `reaches[]` — the admission-surface members that permission reaches.

FR-004 then reads: `authority_class_achieved` equals the MAXIMUM declared
`achieves` (`mutate` dominates `observe`), and any other value is the
contradiction 4.4's negative encodes. FR-009 reads: every `reaches[]` member is
either the entry's own `admission_surface` or a declared
`declared_excess.spanned_surfaces[]` member, and anything else is undeclared
reach — reported naming both the surface and the `id` that reaches it, which is
the delta's own wording. Both are record-internal and deterministic. The alias
rule's "same `granted_permissions[]` SET" (FR-038) compares normalized member
tuples `(id, achieves, sorted(reaches))`.

**`duty_separation_rationale`** is an OPTIONAL entry string, and it exists
because FR-038's alias rule reads it: the third predicate is "declares no
duty-separation rationale", and a genuine duty pair may qualify EITHER by
differing in granted permissions OR by declaring the rationale (FR-017,
SC-002). It is the second addition ruling R7 makes to the ratified field list,
for the same reason as the legend — the ruling's rule cannot be evaluated
without it.

**`standing_credential_attestation` is checkable only as a record-internal
contradiction.** The validator is network-free and single-repo and observes no
credential store, so the object carries the claim (`no_standing_credential`),
the approved grant-window reference the claim is made against, and the evidence
pointer; FR-013's "a credential held outside an approved grant window makes the
attestation false" is raised when the record contradicts itself — a claim of
none against a declared held credential, or against an expired or absent window
reference. No grant record, credential store or provider is consulted, which is
FR-029's boundary and is what 4.1's negative encodes.

**Kind 2 — `xfactory_client_identity_drift_finding`**: `schema_version`,
`kind`, `identity_ref` (the five-element tuple OBJECT from `$defs.identity_key`
— deliberately a different shape from the entry's string `identity_ref`, per
FR-035's wording, documented in the schema description), `fragment_ref`,
`rule_id`, `roster_value`, `observed_value` (both REQUIRED — the ratified
delta scenario), `observed_at`, `opened_at`, `status` (`open|resolved|disposed` — a CLOSED set
with its own refusal probe, SC-014 as re-scoped by the checklist pass),
`disposition_ref` (OPTIONAL, and REQUIRED by an `if status == disposed / then`
branch: a disposed finding with no citation is exactly the unfalsifiable
disposal the record exists to prevent, while an `open` finding cannot carry
one — which is why the packaged example, an `open` finding, declares none).
Field names borrow doc-health's where they apply; the
schema description states explicitly that the record claims no alignment with
and no storage in any doc-health findings register, because none exists.

`$defs.identity_key` is the five-element tuple, defined once and referenced by
the uniqueness rule and by the drift record — the single-file decision's whole
payoff.

**The uniqueness key's third element is `authority_class_intended`** (ruling
R-N1). Every ratified statement of the key — spec constraint 6, FR-006, the
Key Entities "Roster entry", the roster delta's "Identity uniqueness is keyed
on surface, class, blast-radius unit and duty", design.md Decision 2, the
proposal's item 2, and the seed handoff's killed-flaw block — spells the third
element "authority class" unqualified, while the record carries TWO such
fields. The choice is therefore the plan's to make and is made here as:

```yaml
$defs:
  identity_key:
    type: object
    additionalProperties: false
    required: [domain, admission_surface, authority_class_intended,
               blast_radius_unit, duty]
    properties:
      domain: {type: string, minLength: 1}
      admission_surface: {$ref: "#/$defs/admission_surface"}
      authority_class_intended: {$ref: "#/$defs/authority_class"}
      blast_radius_unit: {$ref: "#/$defs/free_token"}
      duty: {$ref: "#/$defs/free_token"}
```

Rationale, stated so the choice is reviewable rather than incidental: **a key
must be declarative and stable.** `authority_class_intended` is a declaration
the domain makes and only a contract change moves.
`authority_class_achieved` is OBSERVATIONAL — it is derived from
`granted_permissions[]` and therefore moves with provider state. Keying on the
achieved class would make an identity's identity change the moment its
permissions drifted, which is incoherent on its face: drift is what FR-009 and
FR-010 REPORT ABOUT a stable identity, not what re-keys it. Worse, it would
make the drift record unjoinable — a drift finding is raised precisely when
observed authority departs from the record, so an achieved-keyed
`identity_ref` would name a tuple that no longer matches the entry the finding
is about.

The consequence for the drift record (kind 2) is stated in its schema
description: its `identity_ref` object carries the SAME `authority_class_intended`
value as the entry it cites — the stable join key — while the observed class
rides `roster_value` / `observed_value` like every other drifted field. A drift
finding about an authority-class change is therefore expressible without the
key moving underneath it.

The uniqueness rule and the alias rule both read element 3 from
`authority_class_intended`. Two entries sharing all five elements are the
FR-006 duplicate finding even where their achieved classes differ — that
difference is a separate finding (FR-004/FR-010), never a licence to duplicate.

**Both rules are scoped WITHIN one fragment** (checklist pass, FR-006). A
fragment is per (client, domain), the tuple carries no `client_ref`, and the
legend binds free tokens per fragment — so `sandbox1` in client A's fragment
and `sandbox1` in client B's name different provider objects. A validator that
pooled every fragment in a target repo before applying the uniqueness rule
would report a domain's two clients' per-environment identities as ONE
duplicate: the per-unit flaw re-killed from the other direction. The
comparison set is therefore the entries of one fragment. Repo fixture 1
(Cluster C) carries two fragments for two clients with an identical tuple and
exits 0, so the scope is measured rather than assumed.

### Cluster B — the canonical validator

`scripts/validate-client-identity-roster.py`, standalone, network-free,
`ROOT = Path(__file__).resolve().parents[1]`, one positional target-repo
argument, `Findings` class emitting `ERROR [kebab-code] message`, exit 0/1/2.

**Layer 1 — self-test over the packaged corpus.** Positives validate clean;
each negative must raise its REGISTERED code, and where the code alone would
be satisfied by a generic `schema` finding, a detail substring is pinned too
(the consent validator's two-part expectations table). Five failure modes are
themselves errors: a registered probe with no file, a file with no
registration, a negative that passes, a negative that fails for the wrong
code, and a negative whose code fires without the pinned detail (FR-018).

**Record-internal rules run on a document even when the SCHEMA already refuses
it, and each raises its own kebab code** (checklist pass). This is structural,
not cosmetic: most of this corpus's negatives are schema-visible (a value
outside a closed set, an entry with no `admission` list, a destructive class),
and a raw `jsonschema` message names neither the closed vocabulary nor the
extension route that FR-007, FR-034, SC-014 and this cluster's own message
requirements demand. If the validator returned at the first schema failure,
those negatives would adjudicate as a generic `schema` finding and the named
refusals would exist nowhere. The rule engine therefore reads the loaded
mapping defensively — a missing or wrong-typed field is skipped by the rule
that would have read it, never crashed on — and runs to completion; the schema
finding and the named finding both appear, and the expectations table pins the
NAMED one. This is the roster-side counterpart of the fact ruling A-3a records
for `validate-credential-contracts.py`, whose self-test reads
`_semantic_findings` ONLY (`:108`): a refusal the harness cannot read is a
refusal that does not exist.

**Layer 2 — repo scan of the target.** Two passes:

1. **Whole-repo kind sweep** (FR-036): `rglob` every `*.y*ml`, skipping
   `.git`, `node_modules`, `__pycache__`, `.venv`, and — when the target IS
   this checkout — THIS FEATURE'S OWN FIXTURE CORPORA:
   `examples/client-identity-roster/` AND `tests/`. Any file carrying
   `kind: xfactory_client_identity_roster` outside
   `credentials/client-identity-roster/` is `misplaced-roster-instance`,
   naming the offending path AND the declared placement.

   **Both exclusions are self-scan accommodations, and `tests/` is not
   optional.** Cluster G's fixture repos put REAL roster fragments at
   `tests/doc-health/fixtures/client-identity-composition/<repo>/credentials/client-identity-roster/*.yaml`
   — a legal placement inside each FIXTURE repo, and not the openxFactory
   checkout's own `credentials/client-identity-roster/`. Without the `tests/`
   exclusion, pointing the validator at this checkout reports every one of
   them as misplaced, which would break this cluster's own verification and
   task 6.7's. The tree already holds the rule and enforces it for the sibling
   scanner: `tests/doc-health/test_suite.py:23-27` asserts "fixture corpora
   must never enter a real scan". Neither exclusion narrows FR-036 or ruling
   R1 over a TARGET DOMAIN repo, which carries no such trees; when a fixture
   repo is itself the target (6.7), its fragments sit at ITS declared
   placement and are validated normally.
2. **Declared-placement validation**: every fragment at
   `credentials/client-identity-roster/*.y*ml` is schema-validated and
   rule-checked; the run prints a count of records checked.

Rules split by what they can see (research.md Decision 7). Record-internal
rules run in both layers. Repo-context rules run only in layer 2:
gate-obligation RESOLUTION against the target's `workflows/<name>.yaml`
gates (FR-011 — the intra-repo target FR-037 leaves unchanged); **`consent_ref`
RESOLUTION** against the target repo's own consent-instrument records (FR-014's
second clause, which presence-checking alone does not satisfy — a citation that
resolves to nothing is the failure mode the change's central claim depends on
catching); and the absence notice.

`consent_ref` resolution is intra-repo BY THE SAME ARGUMENT as the gate
obligation: a domain's consent instruments live in the domain repo (the BC
chain's own `tenants/farheap-bc-administration-consent.yaml`), so nothing
crosses a repository boundary and hermeticity is untouched — the opposite
posture from `evidence_ref` (FR-037), which points into ANOTHER repo and is
therefore shape-checked only.

**The mechanism, named** (the consent family declares no placement, so the
rule cannot cite a path the way FR-011 cites `workflows/`): sweep the target
repo for `kind: xfactory_consent_instrument`
(`contracts/schemas/consent-instrument.schema.yaml:62`) under the same
`SKIP_DIR_NAMES` the sweep already uses — the mechanism
`validate-consent-instruments.py`'s own `repo_scan` uses — and match
`consent_ref` against each record's `instrument_id` (`:63`). "In force" is
read from that record's `status`: `executed` or `amended`, never `draft`,
`pending_signatures`, `terminated` or `withdrawn` (a plan-phase reading,
listed for architect review below).

`ratified_by` is NOT resolved in this release: the ratified resolution clause
attaches to the instrument citation alone, and the delta's capability scenario
is an absence test ("names no ratified capability"). The check is presence plus
domain-qualification, and repo fixture 2 proves the GATE EXIT on absence.

**Absence** (FR-022, FR-032, SC-013): a target with no
`credentials/client-identity-roster/` directory, or with the directory and no
files, prints an explicit notice naming the absence and exits 0. There is no
expected-entry-set derivation anywhere in the module — the checklist item and
the analyze pass should both look for one and find nothing.

**The scope-excess rule** (FR-002, FR-010): a VERIFIED act declaring
`exceeds_governed_unit: true` requires a `declared_excess` with its four
fields; absent one, `undeclared-scope-excess` names the act, its
`achieved_scope` and the governed `blast_radius_unit`. The entry's effective
reach is emitted as a note — the `(surface, achieved_scope)` set over verified
acts plus the OR of their `exceeds_governed_unit` flags (Cluster A) — so
FR-003's union is reported, not merely asserted, and US1 scenario 2 has
something to read.

**Three rules the checklist pass added, each closing a stated obligation that
had no firing predicate** (none extends scope; each carries its own packaged
negative, Cluster C):

1. **The verification pair** (FR-002, FR-003): an act carrying `verified_at`
   with no `evidence_ref` raises `unverified-act-counted-as-access` naming the
   act. The schema's two-way `dependentRequired` refuses the same shape; the
   named code is what the expectations table reads.
2. **Act-surface reach** (FR-009): every `admission[].surface` must be the
   entry's own `admission_surface` or a declared
   `declared_excess.spanned_surfaces[]` member; anything else raises
   `undeclared-act-surface` naming the act and the surface. FR-009's
   permission-side rule reads `granted_permissions[].reaches[]` and cannot see
   an act performed on a surface no permission declares — yet an admission act
   IS the second key that makes a surface reachable, which is this change's own
   measured finding. The cross-domain family already reads acts this way
   (research.md Decision 6), so without this rule the intra-repo gate is
   strictly weaker than the reporting pass on the same evidence.
3. **Per-unit principal coverage** (FR-008): `per_unit_principal_available`
   must carry a key for the entry's surface and for every spanned surface;
   a missing key raises `per-unit-principal-undeclared` naming the surface. A
   key for a surface the entry does not touch is NOT a finding — the key space
   is closed by the enum, and inventing strictness there would penalise a
   fragment that answers more than it must.

**The alias rule** (FR-038) is implemented exactly as stated, as a
three-predicate conjunction, and no more: two entries differ SOLELY in a free
token, AND are observationally identical (the same `granted_permissions[]` set,
compared as normalized member tuples `(id, achieves, sorted(reaches))`, and the
same admission acts by the tuple `(surface, act, achieved_scope,
enforcement_mode)` — exactly the four ratified elements, with
`exceeds_governed_unit` deliberately NOT among them), AND declare no
duty-separation rationale. A pair
differing in `achieved_scope`, in permissions, or carrying the rationale
validates clean. This is the one place the plan asks the implementer to write
the condition and then write the two positive fixtures that would fail under
any broader form.

### Cluster C — the fixture corpus

- **Positives** (FR-017, SC-002): a genuine per-unit pair (differing in
  `achieved_scope`), a genuine duty pair (differing in permissions OR
  declaring the rationale), a provider-forced multi-surface reader with its
  declaration, and a `planned` entry — each with ZERO findings, living inside
  the two packaged fragments. The checklist pass adds a fifth positive for
  coverage rather than for a killed flaw: a `retired` entry, so the third
  member of the `lifecycle_state` set has an instance somewhere in the corpus
  and FR-013's "a retired entry MUST retain its record" is exercised instead
  of merely asserted.
- **Negatives**: the 31 packaged files listed in the structure above (26 as
  first planned; plus THREE added by the checklist pass —
  `undeclared-act-surface.yaml`, `per-unit-principal-undeclared.yaml` and
  `drift-finding-status-out-of-vocabulary.yaml`, each homing a rule this
  cluster's own requirements state and nothing fired on; plus
  `achieved-class-contradicted-by-permissions.yaml` added
  by ruling A-11 to home FR-004's rule — an entry declaring
  `authority_class_achieved: observe` while a `granted_permissions[]` member
  declares `achieves: mutate`, a contradiction between two DECLARATIONS rather
  than a reading of a permission's name; plus
  `scope-exceeds-unit-undeclared.yaml` added by the analyze pass to home the
  scope-excess rule — a verified act declaring `exceeds_governed_unit: true`
  with no `declared_excess`, which is the change's own motivating measurement
  made enforceable; and the earlier
  `achieved-exceeds-intended-undeclared.yaml` proves the DIFFERENT rule that
  achieved-above-intended must be declared, and neither substitutes for the
  other). THREE of FR-016's named rules are routed out of the packaged corpus
  by nature (research.md Decision 7), because a packaged single file cannot
  express a rule about its own repo context:
  - cross-domain shared identity → `tests/doc-health/fixtures/client-identity-composition/`;
  - a roster instance outside the declared placement → the stray-repo fixture;
  - an unresolvable gate obligation → the gate-obligation repo fixture added
    by ruling A-11 (below). FR-011's obligation RESOLUTION is a repo-context
    rule that reads the target's `workflows/`, so it has no packaged home
    either; the first fixture plan left it with no home at all, which is the
    defect A-11 fixes.
- **Repo-shaped fixtures** (`tests/client-identity-roster/`): built in
  `tmp_path` from inline templates, the idiom
  `tests/conformance-gate/test_conformance_checks.py` already uses (`make_repo`,
  `STACK`/`FLOW_MD`/`FLOW_YAML`). SIX repos:
  1. conformant (exit 0) — and it carries TWO fragments, for TWO clients,
     whose entries share the whole uniqueness tuple, so the fragment scope of
     FR-006 (Cluster A) is measured here rather than assumed; its gate
     obligation and its consent citation both resolve, which makes it the
     discrimination partner of fixtures 2, 4 and 6;
  2. nonconformant `mutate`-without-ratified-capability (nonzero) — the
     delta's own gate-exit scenario. Its packaged sibling
     `negative/mutate-without-ratified-capability.yaml` proves the FINDING
     record-internally; this repo proves the EXIT, which a packaged file cannot;
  3. no-fragment (exit 0 + explicit notice);
  4. **unresolvable gate obligation** (ruling A-11): a fragment at the
     declared placement whose entry's `declared_excess.gate_obligation` names
     a gate that is ABSENT from that fixture repo's `workflows/` records —
     the repo also carries a `workflows/` tree holding at least one real gate,
     so the finding proves non-resolution and not merely an empty directory.
     Exits nonzero with FR-011's own code. Its sibling measurement — the
     obligation that DOES resolve — is fixture 1, so the pair is a
     discrimination and not a bare refusal;
  5. misplacement: the roster kind at `tenants/stray.yaml`, the measurement
     SC-005 demands ("placed outside `credentials/` entirely");
  6. **unresolvable consent citation**: an entry whose `consent_ref` names an
     instrument absent from that repo's consent records — while the repo
     carries at least one real instrument, so the finding proves
     non-resolution and not an empty tree. Exits nonzero with FR-014's own
     code; its discrimination partner is fixture 1, whose citation resolves to
     an instrument in force.

  (Ruling A-11 calls the gate-obligation repo "a FOURTH repo-shaped fixture",
  counting the three behavioural repos the first plan enumerated; the stray
  repo, which that plan carried as a separate clause, made five. The analyze
  pass adds the sixth, because FR-014's resolution clause had no probe in any
  corpus. No fixture is dropped.)

**FR-016 per-rule negative coverage, re-counted after both A-11 additions.**
FR-016 names SIXTEEN rules as its minimum. All sixteen have a home:

| # | FR-016 named rule | Negative home |
|---|---|---|
| 1 | cross-domain shared identity | doc-health fixture corpus (`fixtures/client-identity-composition/`) |
| 2 | undeclared reach | `negative/undeclared-reach.yaml` |
| 3 | unverified admission act counted as access | `negative/unverified-act-counted-as-access.yaml` |
| 4 | achieved authority exceeding intended without a declared excess | `negative/achieved-exceeds-intended-undeclared.yaml` |
| 5 | an unresolvable gate obligation | repo fixture 4 (**A-11**) |
| 6 | a missing enforcement test | `negative/missing-enforcement-test.yaml` |
| 7 | provider-enforced claim with no per-unit principal | `negative/provider-enforced-without-per-unit-principal.yaml` |
| 8 | vendor-homed registration declared client-resident | `negative/vendor-homed-declared-client-resident.yaml` |
| 9 | `mutate` entry with no ratified capability | `negative/mutate-without-ratified-capability.yaml` (packaged — the finding) + repo fixture 2 (the gate exit) |
| 10 | false standing-credential attestation | `negative/false-standing-credential-attestation.yaml` |
| 11 | a proposed destructive class | `negative/destructive-authority-class.yaml` |
| 12 | out-of-vocabulary admission surface | `negative/admission-surface-out-of-vocabulary.yaml` |
| 13 | an entry with no consent instrument | `negative/entry-without-consent-instrument.yaml` |
| 14 | a genuine full-tuple duplicate | `negative/full-tuple-duplicate.yaml` |
| 15 | a roster instance outside the declared placement | repo fixture 5 |
| 16 | an alias pair | `negative/alias-pair-observationally-identical.yaml` |

**Count: 16 named rules, 16 homed, 0 unhomed** — 13 packaged, 2 repo-shaped,
1 in the doc-health corpus. Before ruling A-11 the count was 15 of 16 (rule 5
had no home in any corpus), which is the BROKEN verdict A-11 records.

FR-016's floor is "at minimum", and the phrase it opens with is "one NEGATIVE
CONFIRMATION per RULE", so the corpus also homes the rules the named list does
not enumerate: FR-004 (`achieved-class-contradicted-by-permissions.yaml`,
**A-11**), FR-002/FR-010's scope excess
(`scope-exceeds-unit-undeclared.yaml`, analyze R6), FR-003's
consent-recorded-as-access, FR-010's
name-understates-achieved-authority, FR-008's available-but-unused per-unit
principal, FR-012's vendor-tenant-multi missing obligations, SC-014's four
remaining closed-vocabulary refusals and its two legend negatives, FR-037's
`evidence_ref` shape, FR-035's two drift-record negatives, and the three the
checklist pass homed: FR-009's act-side reach (`undeclared-act-surface.yaml`),
FR-008's mapping coverage (`per-unit-principal-undeclared.yaml`), and SC-014's
seventh closed set (`drift-finding-status-out-of-vocabulary.yaml`). FR-002's
verification pair reuses the already-planned
`unverified-act-counted-as-access.yaml`, which the pairing rule gives a
refusal predicate it did not previously have.

Two counts, because they measure different things: **34 rule-homes** (31
packaged + the 2 FR-016 rules with no packaged home + 1 in the doc-health
corpus) and **36 refusing probes** — the repo corpus carries FOUR refusing
fixtures (2, 4, 5, 6) where only two of them are the rule-homes counted above:
fixture 2 additionally proves named rule 9's GATE EXIT, which its packaged
sibling cannot, and fixture 6 homes FR-014's resolution clause, which is not in
FR-016's named list and which no packaged file can express.

### Cluster D — packaged examples

`examples/client-identity-roster/` with `README.md` (`Status: ratified`,
naming the change, following the sibling READMEs' layout block), two positive
fragments for ONE client held by TWO domains (fragments are per (client,
domain), which is why the four mandated cases span two files, ruling C3), and
the drift-finding example.

The BC worked case is transcribed from
`OpsxFactory:tenants/farheap-bc-observer-identity-evidence-v1.yaml` — two
admission acts (the provider-enforced Sandbox1 application user, which does NOT
exceed the governed unit; the tenant-wide admin-center Entra-app authorization
with no scope selector, which declares `exceeds_governed_unit: true`), the
union effective reach, the declared excess with its provider reason, gate
obligation and enforcement test. That declaration is what satisfies Cluster B's
scope-excess rule, and it makes this file the discrimination partner of
`negative/scope-exceeds-unit-undeclared.yaml`: same shape, excess omitted.

**Two acts, ONE surface — and that is ratified, not a judgement call.** The
roster delta's scenario "One product name has two admission acts → each act is
its own admission surface" does NOT split Business Central here: packet task
2.2 binds both acts to the single `business_central` member verbatim ("BC: the
per-environment application user AND the admin-center Entra-app authorization,
which is the two-act worked case"), and answer 5 closes the vocabulary at two
members. The measured reason the acts are not INDEPENDENT admission acts in the
delta's sense is the investigation itself: four admin-consented permissions
held for six days still returned `401` until the admin-center act, so neither
act admits on its own — they are jointly required keys to one surface. The
delta's scenario governs acts that admit independently, in separate
administrative surfaces. Authoring the worked case as two entries on two
surfaces would be unrepresentable (FR-007) and would break SC-003.

`evidence_ref` pointers name `opensoft/OpsxFactory` and the real
`tenants/farheap-bc-sandbox1-verify-probe-evidence-v*.yaml` paths, which are on
`origin/main` (verified) — and remain unresolved by the validator (FR-037).

**PRECONDITION on this cluster (ruling A-16).** The multi-surface reader's
provider fact is verified BEFORE any Cluster D work begins, not discovered
inside it. The fact to be established: that a single provider-native permission
or directory role, in its narrowest available form, reaches BOTH the
`business_central` and the `exchange` read surfaces, and that no read-only role
scoped to just one of the two exists — evidenced by a citation to the
provider's own documentation or to a record in the OpsxFactory evidence chain.

- If a citable spanning permission IS found, Cluster D proceeds and the
  citation is transcribed into `declared_excess.provider_reason`.
- If NO in-vocabulary citation exists, the builder **STOPS and escalates to
  the architect**, listing the candidates examined and why each failed. The
  builder MUST NOT synthesize a provider fact, and MUST NOT soften the case
  into a single-surface reader — either would under-deliver FR-019 and
  SC-002's fourth positive.

Cluster D is therefore blocked on this precondition, and the fixture corpus of
Cluster C is blocked on Cluster D for the multi-surface positive specifically.
The escalation path exists and had not triggered as of the plan-gate ruling.

The constraint of research.md Decision 8 is the standing rule this precondition
mechanizes: a packaged example may not assert a provider fact the builder
cannot cite.

### Cluster E — registration at `contract-v1.32`

Atomic, in one commit (constitution VI):

1. `contracts/manifest.yaml`: `contract_bundle_version: contract-v1.32`; a NEW
   row for the roster schema (one row, one `sha256`, one `consumption_rule`
   stating BOTH the declared placement and that
   `validate-credential-contracts.py`'s skip-with-notice over that path is
   EXPECTED and blessed); refreshed rows for `consent-instrument` and
   `consent-instrument-class-registry`; and a FIRST row for
   `xfactory-credential-contracts`, which has none today (research.md, "A
   registration gap FR-021 assumes away").
2. `contracts/CHANGELOG.md`: a `## contract-v1.32` entry classed **additive**,
   folding in the pending `## Unreleased` openxwallet item, and stating the
   additivity argument explicitly: an OPTIONAL property and an ADDED enum
   member, so a domain repo on the same major version remains conformant
   without changes.
3. `contracts/README.md`: registration rows for the roster schema + validator
   + examples, and amended rows for the two consent schemas.
4. `contracts/releases/contract-v1.32.digests.yaml`: GENERATED by
   `python3 scripts/validate-contract-release.py build --tag contract-v1.32
   --output contracts/releases/contract-v1.32.digests.yaml`. Its membership is
   the Hermes-runtime release surface plus the manifest/CHANGELOG/README and
   versioning policy — roster paths do NOT enter it and must not be hand-added
   (research.md, "Registration mechanics"). **Generation is therefore LAST
   inside this cluster** (checklist pass): `RELEASE_SURFACE_PATHS`
   (`scripts/hermes_runtime_validation/release.py:64-70`) contains
   `contracts/manifest.yaml`, `contracts/CHANGELOG.md` AND
   `contracts/README.md`, so steps 1, 2 and 3 must all have landed before the
   inventory is built — generating it after step 1 alone bakes in stale
   digests for the two files steps 2 and 3 are still editing, and the release
   verifier then fails on a file this same commit touched.
5. `README.md`: the roster family in the document index, AND the correction
   the progress handoff owes — the OpenSpec Records block at ~line 264-272
   still says "MODIFIES consent-instrument … and doc-health (sixteenth
   family)". It now reads four Modified Capabilities, naming Decisions A and
   B. **This correction is scheduled into Cluster E**, the first slice that
   touches `README.md`, and is a completion condition of that slice.

Verification: `python3 scripts/validate-manifest-digests.py` (per-file
`sha256` recomputed and matched) — the check FR-021's "digest verification
passes" names.

### Cluster F — pack membership (Decision A, archive blocker)

There is no pack registry file; the pack IS the promoted spec's enumeration
plus its test. Enrollment therefore consists of:

- the `domain-conformance-checks` MODIFIED delta — already in the packet,
  nothing to author;
- the validator satisfying the pack's consumption rules unchanged: explicit
  target argument, run from the pinned checkout, never copied into a domain
  repo, nonzero exit fails the gate;
- `tests/conformance-gate/test_conformance_checks.py` growing to load
  `validate-client-identity-roster` alongside the three `check-*` modules and
  exercising the four pack scenarios of the delta: entry nonconformance →
  nonzero; `mutate` with no ratified capability → error not report;
  conformant repo → 0; **no fragment → 0 with an explicit notice**;
- its module docstring, which says "Locks the three checks", updated to four
  (the only pack COUNT site the feature owns);
- `openspec/specs/domain-conformance-checks/spec.md` left UNEDITED — promoted
  text the archive step rewrites, by the same rule FR-025 states for
  doc-health.

The naming asymmetry (three `check-*.py` members, one `validate-*.py`) is
ratified in the delta's own enumeration and is not corrected here.

**A residual this plan records honestly (ruling A-N2): pack blocking is
NOMINAL at archive.** Pack membership is the promoted mechanism that CONFERS
blocking status, and this feature confers it — but conferral and firing are
different facts, and the estate does not yet carry the second:

- codexFactory's conformance gate enumerates the pack's three members BY NAME,
  so a fourth member is not picked up by that gate until the gate is edited;
- OpsxFactory's gate invokes no canonical pack check at all.

A second, smaller residual belongs beside it (checklist pass): the pack's
NO-COPY rule — US3 acceptance scenario 3's second clause, and the promoted
delta's "A copied check is a conformance defect" — is a DECLARATION with no
mechanized probe anywhere in the estate. The existing conformance-gate suite's
fifteen tests cover inventory, parity and pin behaviour and none of them scans
a domain repo for a copied check. This feature inherits the rule with its
fourth member and does not build the missing detector, because a copy-detector
is a new check rather than a realization of FR-022. It is named here so the
clause is not read as measured.

So on the day this feature archives, a nonconformant roster entry fails the
pack check when the pack check is RUN, and the pack check is not yet run by
either domain's gate. Wiring the domain gates is a DOMAIN-REPOSITORY EDIT and
is therefore out of scope by FR-030 and SC-012 — it joins the named follow-ups
alongside the OpsxFactory and LedgerxFactory fragments and live drift
detection. The claim this feature is entitled to make is exactly SC-006's:
the check exits nonzero on intra-repo nonconformance and the pack's rules
apply to it unchanged. The plan states the residual so no reader mistakes
"blocking" for "already firing in a domain's CI", and so the follow-up is
carried rather than lost.

### Cluster G — the sixteenth doc-health family

`scripts/doc_health/client_identity_composition.py`, exposing
`fam_client_identity_composition(ctx) -> list[Finding] | Skip`, registered by
importing it at `families.py:25` and adding
`"client-identity-composition": client_identity_composition.fam_client_identity_composition`
to `FAMILIES` (families.py:674-690). Left out of `FAMILY_RESOLUTION`; each
`Finding` sets its own `resolution` (`CONTESTED` where the finding
contradicts a ratified capability, default otherwise) — the precedent of the
three other late families.

Assembly: iterate `sorted(ctx.repo_paths.items())`, read
`<repo>/credentials/client-identity-roster/*.y*ml`, group by `client_ref`.
Two skips, both explicit: `ctx.agg_root is None` → "single-repo run"; no
client held by two or more domains → "nothing to compose". Two finding classes
with the predicates fixed in research.md Decision 6, and NO intra-repo rule of
any kind — the family's test asserts that the intra-repo finding codes never
appear in its output.

`FAMILY_IDS` (`__init__.py:52-70`) also gains the id so the family renders a
report section. The pre-existing omission of `proposal-origin` from that list
is recorded in research.md and NOT fixed here.

**The fixture trap this family's tests must not fall into (ruling A-9).**
`tests/doc-health/conftest.py` `make_ctx(family, git=None, agg_root=None, …)`
defaults **`agg_root=None`** (line 66). This family's FIRST branch is
`ctx.agg_root is None → Skip("single-repo run")`. So any fixture test that
calls `make_ctx` without passing `agg_root` explicitly does not exercise the
family at all — it short-circuits into the skip and passes vacuously, looking
green while measuring nothing. **Every fixture test for this family MUST pass
`agg_root` explicitly**, pointed at the fixture aggregation root, and the
suite carries one test that asserts the single-repo skip DELIBERATELY (with
`agg_root=None` stated in the call, so the omission is never mistaken for the
default). The determinism test and both finding-class tests are the ones most
at risk, because a vacuous skip satisfies "identical findings across runs"
trivially.

Count-bearing prose: `scripts/doc_health/families.py:1` ("The fifteen contract
check families.") → sixteen, and the ownership note at lines 7-11 grows to
name the sixteenth module. Ordinals elsewhere are left alone (FR-025).
`openspec/specs/doc-health/spec.md` is NOT edited.

### Cluster H — `credential-contracts` (Decision B, archive blocker)

`issuance_preconditions` on the `xfactory_credential_requirements` requirement
item, declared as an OBJECT whose property names are the closed vocabulary and
**whose values are `const: true`** (ruling A-3a) — the shape the live
precedent already uses, so the growth is additive in EFFECT and not merely in
form (research.md Decision 3, which is the plan's most consequential finding).
Members: `roster_drift_clear_required` (ratified here), plus
`accepted_request_required` and `registered_active_subject`, the two tokens
the vocabulary is chartered to regularize rather than replace in place.

`const: true` rather than `type: boolean`: a precondition is a REQUIREMENT that
is declared or not declared. `false` is not a second meaning — it is a
declaration that reads as governance while asserting nothing, the exact
false-comfort shape a closed vocabulary exists to refuse. Both live OpsxFactory
records declare `true`, so the narrowing breaks nothing and keeps the additive
claim intact.

**Each of the three members carries a one-line schema `description` naming its
governed condition** (ruling A-3b), so the vocabulary is self-describing at the
point of use and a reader need not chase the change that ratified it:

- `roster_drift_clear_required` — "grant issuance is refused while an `open`
  `xfactory_client_identity_drift_finding` covers the roster entry for the
  identity this requirement names (`add-client-identity-roster`)";
- `accepted_request_required` — cites **`adopt-deployment-handoff-boundary`**;
- `registered_active_subject` — cites **`adopt-deployment-handoff-boundary`**.

Citing the governing change on the two precedent members is what makes
"regularizes rather than replaces in place" legible in the schema itself: they
are admitted because they are already governed elsewhere, not minted here.

`scripts/validate-credential-contracts.py` gains one `_semantic_findings`
branch emitting `issuance-precondition-unknown` naming the closed vocabulary,
because `propertyNames` alone refuses without naming (research.md Decision 4).
**That branch fires on BOTH failure shapes — an out-of-vocabulary member AND a
false-valued member** (ruling A-3a). The semantic mirror is not decorative and
not optional: it is STRUCTURALLY REQUIRED, because this validator's self-test
adjudicates its registered negatives against `_semantic_findings` ONLY
(`scripts/validate-credential-contracts.py:108` —
`findings = _semantic_findings(yaml.safe_load(path.read_text()))`, the verified
fact behind decision 4). A negative whose only defect is a schema violation
raises NO semantic finding and would be reported as `negative-should-fail` —
so a schema-only implementation of this vocabulary makes its own negatives
unregisterable. Every closed-vocabulary refusal this cluster ships must
therefore exist in both layers: the schema constrains, the semantic branch
names and is what the self-test reads.

Fixtures: one positive requirement record declaring the roster-drift member,
one negative declaring an out-of-vocabulary token registered in
`NEGATIVE_EXPECTATIONS`, one negative declaring a member with value `false`
(also registered, adjudicated against the same semantic code), and the
existing positives which declare nothing and must stay valid — that set is
SC-008's whole neutral criterion, stated as fixture-proven because no producer
of live drift findings exists in the family at archive time.

The neutral property governs the CREDENTIAL REQUIREMENT record only. The
workflow-record occurrence at `OpsxFactory:workflows/deployment.yaml:75` is a
different kind under a different validator and is explicitly out of this
vocabulary's reach.

### Cluster I — `consent-instrument` (archive blocker)

Additive growth across every declaration, per FR-039 (research.md Decision 5):

- `status` enum + `withdrawn` at `consent-instrument.schema.yaml:194` AND
  `:209` (two declarations in one file), and at
  `consent-instrument-class-registry.schema.yaml:77`;
- `NEUTRAL_STATUSES` (`validate-consent-instruments.py:129-130`) + `withdrawn`
  — the alias-target check adjudicates against this tuple, so omitting it
  would let a domain alias onto a status the schema accepts and the validator
  rejects. **Verified precondition (ruling A-7): no consent class registry
  anywhere in the estate aliases a key spelled `withdrawn`** (swept
  2026-08-14). The consequence matters in the other direction from the one an
  implementer might expect: growing `NEUTRAL_STATUSES` NARROWS what
  `alias-remaps-neutral-status` (`validate-consent-instruments.py:348`)
  refuses — a domain alias whose KEY is a neutral status is the thing that
  check rejects — and because no registry uses that spelling today, the
  narrowing fires nowhere and no existing instrument or registry changes
  verdict. The sweep is what converts "should be safe" into a measured fact,
  and it is the precondition to re-run if this cluster is rebased onto a
  materially later estate;
- `PAST_SIGNATURE_STATUSES` (`:133`) + `withdrawn` — an instrument can only be
  withdrawn after execution, so the lifecycle-skip discipline must reach it;
- `dependent_refs[].kind` enum (`:244`) + `governed_identity` — a named member,
  never the `other` escape;
- **the dependent-ref's `ref` for a `governed_identity`** names the roster
  FRAGMENT PATH plus the entry's `identity_ref`, and is UNRESOLVED by the
  consent validator (ruling A-5). The existing `ref` is a bare
  `{type: string, minLength: 1}` and stays so; what this change adds is a
  schema `description` stating the convention and the posture explicitly —
  the pointer names `credentials/client-identity-roster/<client_ref>.yaml`
  and the `identity_ref` within it, and the consent validator checks that a
  `governed_identity` dependent carries a non-empty `ref` and NOTHING more.
  It does not open the fragment, does not confirm the entry exists, and does
  not cross a repository boundary — the same FR-037 posture the roster
  validator takes toward `evidence_ref`, for the same reason: these
  validators are network-free and read one repository. Resolution, here as
  there, belongs to a pass that assembles pinned repos. Stating the posture in
  the schema is what stops a later reader from filing the non-resolution as a
  gap;
- two new OPTIONAL properties on the dependent-ref item,
  `identity_removal_evidence` and `admission_withdrawal_evidence`;
- `check_termination_cascade` (`:494-505`): the gate widens to
  `status not in ("terminated", "withdrawn")` — so the REACH of the existing
  `termination-without-cascade-evidence` code widens to `withdrawn`
  instruments, which is a behaviour change and is declared as one; the code
  SPELLING is retained for continuity with the corpus and the registered
  negatives (ruling A-6). A new `identity-cascade-incomplete` fires when a
  `governed_identity` dependent on a terminated OR withdrawn instrument lacks
  either evidence field;
- `contract_schema_version` 1 → 2 on both schema files. The RECORD envelope's
  `schema_version: const: 1` does NOT change — changing it would invalidate
  every existing instrument, which is the opposite of additive;
- fixtures: one positive (a withdrawn instrument with a `governed_identity`
  dependent carrying complete cascade evidence) and two negatives registered
  in `EXPECTED_NEGATIVE_FINDINGS` — credential-only evidence on `terminated`,
  and the same on `withdrawn` — proving the obligation fires identically on
  both events.

`openspec/specs/consent-instrument/spec.md:69-74` ("the closed five-state
lifecycle") is NOT edited: promoted text, rewritten by the archive step.

---

## Verification story

### Which suites prove FR-030's "existing suites unaffected"

FR-030 requires all FOUR modified capabilities' existing suites and fixtures
to stay green AND unmodified in behaviour. Measured against the tree, that
resolves to a specific, runnable list — and to one honest gap.

| Capability | The suite that proves it | Note |
|---|---|---|
| `consent-instrument` | `python3 scripts/validate-consent-instruments.py` (no argument = full self-test: 5 positives, 5 registered negatives, 2 purpose probes) | The family's ONLY consumer. There is no `tests/` directory for it — grep for `consent-instrument` under `tests/` returns nothing — so the validator's self-test IS the suite, and the plan says so rather than implying a pytest suite exists. The measurement of "unaffected" is that the 5 pre-existing positives and 5 pre-existing negatives keep their verdicts and their finding codes with the corpus grown, not merely that the run exits 0. |
| `credential-contracts` | `python3 scripts/validate-credential-contracts.py <repo>` self-test (2 positives, 3 registered negatives) **and** `pytest tests/credential_contracts/test_dispatch_credential_contract.py` | Plus the load-bearing extra measurement: run the validator against the OpsxFactory checkout and confirm the record carrying the live `issuance_preconditions` object still passes. That is the direct test of research.md Decision 3, and the one result that would falsify the additivity claim. |
| `doc-health` | `pytest tests/doc-health/` (23 test modules) | Specifically `test_families.py` (per-family fixture verdicts) and `test_suite.py` (suite-level guarantees). The new family must add findings to no existing family's fixtures. |
| `domain-conformance-checks` | `pytest tests/conformance-gate/test_conformance_checks.py` (15 tests over the three existing checks) | The three existing checks' tests must pass unmodified; only NEW tests are added for the fourth member. |

### The green bar (SC-010, verbatim as runnable steps)

1. `python3 scripts/validate-client-identity-roster.py <fixture repo>` — clean
   on the conformant fixture, nonzero on each negative repo.
2. Every repo-local validator the change touches, per the four rows above.
3. `pytest tests/conformance-gate tests/doc-health tests/credential_contracts
   tests/client-identity-roster`.
4. `OPENSPEC_TELEMETRY=0 openspec validate add-client-identity-roster --strict`
   and `--all --strict` (58/58 at `4de5bb2`; must not regress).
5. `python3 scripts/validate-manifest-digests.py` — every row's `sha256`
   verifies at `contract-v1.32`.
6. `python3 scripts/validate-contract-release.py build --tag contract-v1.32
   --output contracts/releases/contract-v1.32.digests.yaml`, then the
   release verifier over the realized commit.
7. `python3 openxFactory/scripts/doc-health.py --repo-root <aggregation
   checkout>` from the aggregation root — sixteen families run, the new one
   reports or skips with an explicit reason, and NO new finding lands against
   this change or its documents.

### How the harder success criteria are measured, not asserted

- **SC-002 (the discrimination)** — the genuine per-unit pair and the genuine
  duty pair are asserted to produce ZERO findings in the same run in which the
  alias pair is refused. A single run, three verdicts; a rule broad enough to
  catch the alias pair and the genuine pairs alike fails the test.
- **SC-005 (misplacement)** — a fixture repo with the roster kind at
  `tenants/stray.yaml`, outside `credentials/` entirely.
- **SC-006 (the blocking/reporting split)** — one measurement pair: an
  intra-repo nonconformance yields a nonzero exit from the pack check, and a
  cross-domain shared-identity case yields a doc-health finding while the pack
  check's exit stays 0 over the same fixture corpus. **The second half is
  proven across BOTH corpora (ruling A-N4): the canonical roster validator is
  also run over the doc-health cross-domain fixture repos
  (`tests/doc-health/fixtures/client-identity-composition/<repo>/`) and MUST
  exit 0 on each.** Without that run the "leaves the domain gate exit
  unchanged" half is an assertion about a corpus nothing measured — the
  cross-domain fixtures would only ever have been read by the doc-health
  family. Running the intra-repo validator over them is what proves the shared
  identity is intra-repo CONFORMANT and that the finding is genuinely
  composition-only, not a nonconformance visible from either side. It is a
  test in `tests/doc-health/test_client_identity_composition.py` — named, not
  left as a choice, so the assertion cannot land in two modules or in neither;
  the roster-side module was the rejected alternative, because the fixture
  repos this test reads live beside the doc-health module.
- **SC-011 (determinism)** — the family run twice over one fixture context
  with `__dict__`-equal sorted findings, the pattern of
  `tests/doc-health/test_suite.py:15-19`; plus the suite-wide hermeticity
  guard, which makes a network reach a test failure rather than a silent
  success.
- **SC-013 (absence is never a finding)** — three measurements as written,
  including the negative one: an assertion that no module in the feature
  reads `credentials/requirements.yaml` or any other inventory to derive an
  expected entry set.
- **SC-012 (no domain file modified)** — `git status --porcelain` over the
  aggregation checkout shows no change under `xFactories/`.

---

## Decisions this plan makes that the rulings did not fix

Every item below is a plan-phase choice, listed for architect review before
implementation. Nothing here contradicts a ruling; each is a gap the rulings
left open.

Seventeen items went to the plan gate; the rulings of
[plan-gate-rulings-2026-08-14.md](plan-gate-rulings-2026-08-14.md) upheld
eleven, amended five (2, 3, 5, 6, 7 → see A-2, A-3a/b, A-5, A-6, A-7 encoded
above), and found one BROKEN (11 → A-11, the missing FR-011 negative home).
The list below is the AMENDED state — it is what implementation follows. One
item is new since the gate: **R-N1, the uniqueness key's third element**, which
is a ruling rather than an open choice and is encoded in Cluster A above.

1. **`identity_kind` = `[entra_app_registration]`, one member** — derived
   (research.md Decision 1). The SET is not ambiguous; the SPELLING is a
   choice.
2. **The drift record is a second `kind` in the roster schema file**, not a
   second file (research.md Decision 2).
3. **`issuance_preconditions` is an OBJECT with closed property names and
   `const: true` values, with three members** — the roster-drift token plus
   the two precedent tokens it regularizes, each carrying a schema
   `description` naming its governed condition and the two precedent members
   citing `adopt-deployment-handoff-boundary`. The alternative (an array, or a
   single-member set) breaks a live OpsxFactory record and contradicts the
   tree's own definition of an additive-minor bump. **This was the decision
   most worth the architect's time**; it was UPHELD at the plan gate and
   amended twice — values narrowed from `type: boolean` to `const: true`, and
   the semantic mirror declared structurally required rather than
   presentational (rulings A-3a, A-3b; research.md Decision 3).
4. **Precondition token name**: `roster_drift_clear_required`, following the
   precedent's `<condition>_required` style.
5. **Consent dependent-kind token**: `governed_identity`.
6. **Cascade coverage is STRUCTURAL** — two new optional evidence properties
   plus a Python obligation, rather than a keyword scan of free text
   (research.md Decision 5).
7. **`PAST_SIGNATURE_STATUSES` grows by `withdrawn`** — not named by any
   ruling; omitting it opens a lifecycle-skip hole through the new member.
8. **The two cross-domain finding predicates** are fixed here
   (`shared-identity-material` keyed on identity MATERIAL never on
   (surface, class) collocation; `undeclared-cross-domain-reach` defined as
   reach into a surface the owning domain publishes no entry for while
   another domain declares it) — the ratified delta names them in prose only
   (research.md Decision 6).
9. **The corpus-level skip rule** for the doc-health family: `Skip` only when
   NO client has two or more fragments; a mixed corpus reports.
10. **`FAMILY_IDS` gains the new family** so it renders a report section; the
    pre-existing `proposal-origin` omission is recorded and NOT fixed here.
11. **The two-layer corpus split** — record-internal rules proven by packaged
    fixtures, repo-context rules by `tmp_path` repo fixtures — and the
    consequent routing of THREE FR-016 negatives (cross-domain shared identity
    → doc-health fixtures; misplacement → repo fixture, because a packaged
    file cannot express a path rule about itself; **unresolvable gate
    obligation → repo fixture, because FR-011 resolves against the target's
    `workflows/`**) (research.md Decision 7). The third routing is ruling
    A-11's fix: the pre-gate plan routed only two and left FR-011's negative
    with no home in any corpus, the single BROKEN verdict of the plan gate.
    The FR-016 coverage table in Cluster C is the re-count that closes it —
    16 named rules, 16 homed.
12. **The repo scan excludes this checkout's own fixture corpora —
    `examples/client-identity-roster/` AND `tests/` —** or pointing the
    validator at openxFactory reports its own packaged corpus and Cluster G's
    fixture repos as misplaced. The `tests/` half was missed by the pre-analyze
    plan and is the analyze pass's one HIGH finding; `test_suite.py:23-27`
    ("fixture corpora must never enter a real scan") is the tree's own
    statement of the rule.
13. **`credential-contracts` gets a FIRST manifest row**, not a refresh — it
    has none today, which FR-021's wording assumes it does.
14. **The `Unreleased` CHANGELOG block folds into the v1.32 entry** rather
    than surviving beside it.
15. **`openspec/specs/domain-conformance-checks/spec.md` and
    `openspec/specs/consent-instrument/spec.md` are left unedited**, extending
    FR-025's doc-health rule to the other promoted specs this change modifies
    — the archive step rewrites all three.
16. **The multi-surface reader example must CITE its provider fact**, and an
    uncitable claim escalates rather than being invented (research.md
    Decision 8).
17. **The drift record's `identity_ref` is an OBJECT** while the entry's
    `identity_ref` is a STRING — both names are ratified (FR-001, FR-035); the
    divergence is documented in the schema rather than renamed away.

Three further choices are added by the analyze pass, in the same reviewable
class — each closes a ratified clause that had no encoding, and none extends
scope:

18. **"In force" (FR-014) = `executed` or `amended`** — the consent family's own
    lifecycle states past signature and short of ending, never `draft`,
    `pending_signatures`, `terminated` or `withdrawn`. The alternative (accept
    any instrument that exists) would satisfy the word "resolve" while dropping
    "in force" entirely.
19. **`consent_ref` resolves INTRA-REPO**, against the target domain
    repository, which is what makes FR-014's resolution clause implementable at
    all inside a network-free single-repo validator — and the opposite posture
    from `evidence_ref` (FR-037), deliberately, because that pointer names
    another repo. **`ratified_by` is NOT resolved**: the ratified clause
    attaches resolution to the instrument citation alone and the capability
    scenario is an absence test, so extending resolution to it would invent a
    requirement (the analyze pass proposed it in round 2 and reverted it in
    round 3).
20. **`duty_separation_rationale` is an optional entry field** (ruling R7's
    alias predicate needs a declaration to read), and
    **`standing_credential_attestation` is falsified record-internally**
    (`no_standing_credential` against a declared held credential or an
    expired/absent window reference), never by consulting a credential store.
21. **`granted_permissions[]` members are objects** — `id` (provider-native,
    verbatim), `achieves`, `reaches[]` — because FR-004's "checkable against"
    and FR-009's "naming the surface and the permission that reaches it" are
    otherwise decidable only by a provider catalogue (forbidden) or an invented
    inference from identifier spelling. spec.md's Assumptions block already
    says the mapping is declared in the record; this is that declaration's
    shape.
22. **`per_unit_principal_available` is a mapping keyed by admission surface**,
    not a bare boolean — FR-008 is per-surface, and the mandated multi-surface
    reader is exactly the entry one boolean cannot describe.
23. **FR-010's name check reads `identity_ref`** (the ratified record has no
    `purpose` field), fires in ONE direction only — an observation-suggesting
    token in the name while `authority_class_achieved` is `mutate` — against a
    small CLOSED token list declared in the validator module
    (`observer`, `observe`, `reader`, `read`, `readonly`, `viewer`, `audit`),
    matched case-insensitively on word boundaries and NAMING the token it
    matched. And **`consent_ref` resolves by kind sweep** for
    `xfactory_consent_instrument`, matching `instrument_id`, reading `status`
    for "in force".
24. **Each admission act declares `exceeds_governed_unit`** (boolean), because
    `achieved_scope` is an opaque provider token and the ratified "declared,
    CHECKABLE, tested" degradation cannot otherwise be checked: comparing the
    token to the legend's binding would detect DIFFERENCE, not excess, and
    would fire on a legitimately narrower act. It carries the scope-excess rule
    and makes FR-003's union computable. The alternative — inferring breadth
    from a provider string — is the inference the neutral layer has no standing
    to make.

Six further choices are added by the **checklist pass**, in the same reviewable
class. Each closes a rule this feature's own requirements state but nothing
fired on, or an ambiguity whose wrong resolution would regress a killed flaw;
none extends scope, and each is homed by a probe:

25. **`evidence_ref` and `verified_at` are a two-way `dependentRequired`
    pair**, and `verified_at` without `evidence_ref` is the refusal predicate
    of `unverified-act-counted-as-access` — the FR-016 negative that, before
    this, had no predicate at all (exclusion from effective reach is a
    behaviour, not a refusal). FR-033 is reworded from "every admission act" to
    "every VERIFIED admission act", because requiring the timestamp everywhere
    made FR-003's unverified state unrepresentable.
26. **Uniqueness and the alias rule are scoped WITHIN one fragment.** The tuple
    carries no `client_ref` and the legend is per fragment, so pooling a
    repo's fragments would report two clients' per-environment identities as a
    duplicate — the per-unit flaw from the other side. Repo fixture 1 measures
    it.
27. **The alias rule's "solely in a free token" reads as "in free tokens
    only"** — a pair differing in BOTH tokens is in scope. The narrow reading
    leaves the rule evadable by inventing two spellings instead of one, and the
    wider reading cannot fire on a genuine pair (which differs in
    `achieved_scope`, in permissions, or declares the rationale).
28. **Three rules gain a firing predicate and a packaged negative**: act-side
    undeclared reach (`undeclared-act-surface`), `per_unit_principal_available`
    coverage (`per-unit-principal-undeclared`), and the drift record's closed
    `status` set. The first is the sharpest — the cross-domain family reads
    admission acts for reach while the intra-repo gate read only permissions,
    so the BLOCKING check was strictly weaker than the REPORTING one on the
    same evidence.
29. **`disposition_ref` is optional and required only when `status: disposed`**
    (an `open` finding cannot carry one), and **record-internal rules run to
    completion even when the schema already refuses the document**, so a
    schema-visible negative still raises the named code its refusal message
    and its expectations-table entry depend on.
30. **A `retired` entry joins the packaged corpus** so no member of a closed
    lifecycle set is left without an instance, and FR-013's retention
    guarantee is exercised rather than asserted.

## Contradictions found between spec.md, the rulings, and the amended packet

None. The three were read in full against each other at `4de5bb2`, including
all five deltas, `design.md`, and both `review/` records. Two things that
LOOK like contradictions and are not, recorded so a later reader does not
re-open them:

- The packet's `tasks.md` 2.3 names a single example file
  (`examples/client-identity-roster.example.yaml`) while FR-019 and ruling C3
  require a directory spanning at least two fragments. The spec's Assumptions
  block already dispositions this: the governed sketch is superseded on
  packaging convention, and Speckit owns the task list.
- The packet routes the refusal through "the existing `issuance_preconditions`
  mechanism" (proposal, item 12; design Decision 7) while the amendment record
  establishes that no such neutral mechanism existed. Decision B is the
  recorded cure; the proposal's older wording is history, not a live claim.

One item the plan flags as a wording assumption rather than a contradiction:
FR-021 says every other schema this feature edits must have its manifest row
"refreshed", but `xfactory-credential-contracts.schema.yaml` has no row to
refresh. The plan registers it for the first time and records the fact
(decision 13 above).

## Out of scope, by ratification

Domain fragments (OpsxFactory's and LedgerxFactory's), live client-tenant
drift detection, enrollment automation, drift remediation, per-surface
admission procedures, any decision to grant/widen/narrow a live client
identity, surfaces outside `business_central` and `exchange`, roster
completeness in any form, admission-freshness decay, and the LedgerxFactory
residency conflict — which touches live client consent instruments and is
Brett's decision, not this feature's.
