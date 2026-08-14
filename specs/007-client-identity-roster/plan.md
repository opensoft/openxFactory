# Implementation Plan: client identity roster neutral contracts and conformance wiring

**Feature**: `007-client-identity-roster` | **Branch**:
`007-client-identity-roster` | **Date**: 2026-08-14

**Governing change**: `openspec/changes/add-client-identity-roster/` — ratified
2026-08-14 by Brett Heap, AMENDED the same day (Decisions A and B,
`review/amendment-record-2026-08-14.md`).

**Spec**: [spec.md](spec.md) · **Rulings**:
[clarify-rulings-2026-08-14.md](clarify-rulings-2026-08-14.md) ·
**Decisions and derivations**: [research.md](research.md)

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
| I. Contract-first, domain-neutral core | PASS. The schema constrains shape; `blast_radius_unit` and `duty` are domain-declared tokens bound to provider-native identifiers in a per-fragment legend, and `granted_permissions[]` / `achieved_scope` stay provider-native and opaque to the neutral layer. `admission_surface` and `identity_kind` are provider-named but closed BY RATIFICATION (FR-007) and extended only by the change that governs a new member. Domain fragments are explicitly not deliverables (FR-030). |
| II. OpenSpec before implementation | PASS. `add-client-identity-roster` is ratified and amended; this is its Speckit realization. Nothing here extends the packet's scope — the two amendments were ratified BEFORE planning, and the plan adds no fifth modified capability. |
| III. Document lifecycle | PASS. New docs (`examples/client-identity-roster/README.md`) carry `Status: ratified` naming the change. `Status: record` review files are never edited or appended; any amendment lands as a sibling record file (research.md, last section). |
| IV. Schema and artifact discipline | PASS. Every new YAML carries `schema_version` + `kind`; `.example.yaml` files are instantiation stubs, never live configuration; validator root is `Path(__file__).resolve().parents[1]` so no host-absolute path is committed; no credential, provider payload, or tenant secret enters the tree — the packaged BC case records app/object/sp identifiers and permission names only, and its source record already states `credentials: none`. New docs are linked into `README.md`'s index and `contracts/README.md`'s registration table. |
| V. Validation gates | PASS. The green bar is enumerated below and is the SC-010 list verbatim. Behaviour is proven by fixtures and a discrimination measurement (genuine pairs pass, alias pair refused), not by assertion. |
| VI. Versioned, content-addressed releases | PASS. `contract-v1.32` allocated at realization: manifest bundle version, per-file `sha256`, CHANGELOG entry, regenerated release digest inventory, atomic commit. `contract_schema_version` bumps on the two consent schemas; the record envelope's `schema_version` const does NOT change (research.md, "A registration gap FR-021 assumes away"). Additive-minor is the claim, and `docs/contract-versioning-policy.md:130-132` is the test it is held to. |
| VII. Fail-closed authority boundaries | PASS. Six closed vocabularies refuse unrecognized values; the two open tokens are pattern-bound and legend-bound. The drift record refuses grant issuance while `open` — a fail-closed lever that mutates nothing. No model call anywhere; the cross-domain family is a deterministic recompute. |

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
| 4 | Done means records AND consent cascade AND doc-health family | All three are archive-blocking clusters, plus 3.1/3.3 per the amendments. Only domain fragments are exempt. |
| 5 | `admission_surface` CLOSED to two members | Cluster A enum + one negative (SC-014). |
| 6 | Five-element tuple; classes `observe\|mutate` only | Cluster A `$defs.identity_key`; Cluster C carries a GENUINE per-unit pair and a GENUINE duty pair as ZERO-finding positives alongside the alias-pair negative — the discrimination is the measurement (SC-002). |
| 7 | `granted_permissions[]` and `admission[]` (a LIST) survive | Both required on every entry; `admission` is `type: array, minItems: 1`; a single-act expression is unrepresentable. |
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
  doc-health family module, ~30 packaged fixture files, four modified
  capabilities' surfaces, one bundle cut.

## Project structure

### Documentation (this feature)

```text
specs/007-client-identity-roster/
├── spec.md                              # ratified requirements (exists)
├── clarify-rulings-2026-08-14.md        # the ruling record (exists)
├── plan.md                              # this file
├── research.md                          # decisions and derivations
├── traceability.yaml                    # authored at implementation:
│                                        #   one row per ratified requirement →
│                                        #   artifact, enforcing check, negative
│                                        #   confirmation (the 006 shape)
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
│                                                            #   per-unit pair
├── client-identity-drift-finding.example.yaml
└── negative/                                                # one file per rule
    ├── consent-recorded-as-access.yaml
    ├── unverified-act-counted-as-access.yaml
    ├── undeclared-reach.yaml
    ├── achieved-exceeds-intended-undeclared.yaml
    ├── name-understates-achieved-authority.yaml
    ├── missing-enforcement-test.yaml
    ├── provider-enforced-without-per-unit-principal.yaml
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
    └── drift-finding-without-observed-value.yaml

tests/client-identity-roster/test_client_identity_roster.py  # repo-context rules
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
tests/doc-health/test_suite.py                               # determinism assertion
examples/credential-contracts/                               # + 1 positive, + 1 negative
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

**Kind 1 — `xfactory_client_identity_roster`** (the fragment): `schema_version`,
`kind`, `client_ref`, `domain`, `legend`, `entries[]` (`minItems: 1`).

`legend` binds every free token used in the fragment to its provider-native
identifier: `{blast_radius_units: {<token>: <provider identifier>}, duties:
{<token>: <provider identifier>}}`. A YAML mapping makes "declared twice"
unrepresentable at the schema level for the same key; the DUPLICATE case
FR-034 requires as a finding is a token appearing in BOTH maps, or a legend
entry whose key is never used — both checked in the validator, both with
their own negatives.

Each entry carries the ratified field list of FR-001, unreduced, plus nothing
except the legend's consequences:

| Field | Shape |
|---|---|
| `identity_ref` | string — the identity's own provider-facing name |
| `identity_kind` | closed enum, ONE member (research.md Decision 1) |
| `home_tenant` | string — the tenant the REGISTRATION is homed in |
| `principal_locations[]` | array of tenant identifiers |
| `residency_model` | closed enum: client-tenant-single, vendor-tenant-multi |
| `admission_surface` | closed enum: `business_central`, `exchange` |
| `duty`, `blast_radius_unit` | pattern `^[a-z0-9][a-z0-9_-]*$`, legend-bound |
| `authority_class_intended` / `_achieved` | closed enum `observe\|mutate` |
| `granted_permissions[]` | provider-native strings, `minItems: 1` |
| `admission[]` | LIST, `minItems: 1` — see below |
| `declared_excess` | optional object: `spanned_surfaces[]`, `provider_reason`, `bound_mechanism`, `gate_obligation`, `enforcement_test_ref` |
| `per_unit_principal_available` | boolean, per surface |
| `lifecycle_state` | closed enum `planned\|enrolled\|retired` |
| `standing_credential_attestation` | object: the claim plus its evidence pointer |
| `ratified_by` | domain-qualified capability id |
| `consent_ref` | instrument citation |

`admission[]` members: `surface`, `act`, `achieved_scope` (provider-native),
`enforcement_mode` (closed: provider-enforced, logic-enforced), `evidence_ref`,
`verified_at`. `evidence_ref` is a DECLARED POINTER — `{repo, path, sha?}`
(FR-037) — and an act with no `evidence_ref` is `verified: false` by
derivation, never by independent assertion, so an unverified act cannot claim
verification. Effective reach is the union of verified acts, computed, never
declared.

`vendor_tenant_multi` obligations (tenant allow-list enforced at token
validation, per-client authorization state, per-client revocation evidence,
the cross-client credential-span statement, the per-client consent amendment)
are required by an `if/then` on `residency_model` — expressible in schema and
therefore expressed there, so the obligation cannot be lost in a validator
refactor.

**Kind 2 — `xfactory_client_identity_drift_finding`**: `schema_version`,
`kind`, `identity_ref` (the five-element tuple OBJECT from `$defs.identity_key`
— deliberately a different shape from the entry's string `identity_ref`, per
FR-035's wording, documented in the schema description), `fragment_ref`,
`rule_id`, `roster_value`, `observed_value` (both REQUIRED — the ratified
delta scenario), `observed_at`, `opened_at`, `status` (`open|resolved|disposed`),
`disposition_ref`. Field names borrow doc-health's where they apply; the
schema description states explicitly that the record claims no alignment with
and no storage in any doc-health findings register, because none exists.

`$defs.identity_key` is the five-element tuple, defined once and referenced by
the uniqueness rule and by the drift record — the single-file decision's whole
payoff.

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

**Layer 2 — repo scan of the target.** Two passes:

1. **Whole-repo kind sweep** (FR-036): `rglob` every `*.y*ml`, skipping
   `.git`, `node_modules`, `__pycache__`, `.venv`, and — when the target IS
   this checkout — `examples/client-identity-roster/`. Any file carrying
   `kind: xfactory_client_identity_roster` outside
   `credentials/client-identity-roster/` is `misplaced-roster-instance`,
   naming the offending path AND the declared placement.
2. **Declared-placement validation**: every fragment at
   `credentials/client-identity-roster/*.y*ml` is schema-validated and
   rule-checked; the run prints a count of records checked.

Rules split by what they can see (research.md Decision 7). Record-internal
rules run in both layers. Repo-context rules run only in layer 2:
gate-obligation RESOLUTION against the target's `workflows/<name>.yaml`
gates (FR-011 — the intra-repo target FR-037 leaves unchanged), and the
absence notice.

**Absence** (FR-022, FR-032, SC-013): a target with no
`credentials/client-identity-roster/` directory, or with the directory and no
files, prints an explicit notice naming the absence and exits 0. There is no
expected-entry-set derivation anywhere in the module — the checklist item and
the analyze pass should both look for one and find nothing.

**The alias rule** (FR-038) is implemented exactly as stated, as a
three-predicate conjunction, and no more: two entries differ SOLELY in a free
token, AND are observationally identical (same `granted_permissions[]` SET and
same admission acts by the tuple `(surface, act, achieved_scope,
enforcement_mode)`), AND declare no duty-separation rationale. A pair
differing in `achieved_scope`, in permissions, or carrying the rationale
validates clean. This is the one place the plan asks the implementer to write
the condition and then write the two positive fixtures that would fail under
any broader form.

### Cluster C — the fixture corpus

- **Positives** (FR-017, SC-002): a genuine per-unit pair (differing in
  `achieved_scope`), a genuine duty pair (differing in permissions OR
  declaring the rationale), a provider-forced multi-surface reader with its
  declaration, and a `planned` entry — each with ZERO findings, living inside
  the two packaged fragments.
- **Negatives**: the 26 files listed in the structure above. FR-016's list is
  covered, with two routed elsewhere by nature (research.md Decision 7):
  cross-domain shared identity → the doc-health fixtures; the misplacement
  case → a repo-shaped fixture, because a packaged file cannot express a path
  rule about itself.
- **Repo-shaped fixtures** (`tests/client-identity-roster/`): built in
  `tmp_path` from inline templates, the idiom
  `tests/conformance-gate/test_conformance_checks.py` already uses. Three
  repos: conformant (exit 0), nonconformant `mutate`-without-capability
  (nonzero), and no-fragment (exit 0 + notice); plus a repo carrying the
  roster kind at `tenants/stray.yaml` for the misplacement measurement
  SC-005 demands ("placed outside `credentials/` entirely").

### Cluster D — packaged examples

`examples/client-identity-roster/` with `README.md` (`Status: ratified`,
naming the change, following the sibling READMEs' layout block), two positive
fragments for ONE client held by TWO domains (fragments are per (client,
domain), which is why the four mandated cases span two files, ruling C3), and
the drift-finding example.

The BC worked case is transcribed from
`OpsxFactory:tenants/farheap-bc-observer-identity-evidence-v1.yaml` — two
admission acts (the provider-enforced Sandbox1 application user; the
tenant-wide admin-center Entra-app authorization with no scope selector), the
union effective reach, the declared excess with its provider reason, gate
obligation and enforcement test. `evidence_ref` pointers name
`opensoft/OpsxFactory` and the real `tenants/farheap-bc-sandbox1-verify-probe-evidence-v*.yaml`
paths, which are on `origin/main` (verified) — and remain unresolved by the
validator (FR-037).

The multi-surface reader carries the constraint of research.md Decision 8: its
`provider_reason` must cite provider documentation or a record in the evidence
chain; an uncitable provider claim is escalated, never invented.

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
   (research.md, "Registration mechanics").
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

Count-bearing prose: `scripts/doc_health/families.py:1` ("The fifteen contract
check families.") → sixteen, and the ownership note at lines 7-11 grows to
name the sixteenth module. Ordinals elsewhere are left alone (FR-025).
`openspec/specs/doc-health/spec.md` is NOT edited.

### Cluster H — `credential-contracts` (Decision B, archive blocker)

`issuance_preconditions` on the `xfactory_credential_requirements` requirement
item, declared as an OBJECT whose property names are the closed vocabulary and
whose values are booleans — the shape the live precedent already uses, so the
growth is additive in EFFECT and not merely in form (research.md Decision 3,
which is the plan's most consequential finding). Members:
`roster_drift_clear_required` (ratified here), plus
`accepted_request_required` and `registered_active_subject`, the two tokens
the vocabulary is chartered to regularize rather than replace in place.

`scripts/validate-credential-contracts.py` gains one `_semantic_findings`
branch emitting `issuance-precondition-unknown` naming the closed vocabulary,
because `propertyNames` alone refuses without naming (research.md Decision 4).
Fixtures: one positive requirement record declaring the roster-drift member,
one negative declaring an out-of-vocabulary token registered in
`NEGATIVE_EXPECTATIONS`, and the existing positives which declare nothing and
must stay valid — that trio is SC-008's whole neutral criterion, stated as
fixture-proven because no producer of live drift findings exists in the family
at archive time.

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
  rejects;
- `PAST_SIGNATURE_STATUSES` (`:133`) + `withdrawn` — an instrument can only be
  withdrawn after execution, so the lifecycle-skip discipline must reach it;
- `dependent_refs[].kind` enum (`:244`) + `governed_identity` — a named member,
  never the `other` escape;
- two new OPTIONAL properties on the dependent-ref item,
  `identity_removal_evidence` and `admission_withdrawal_evidence`;
- `check_termination_cascade` (`:494-505`): the gate widens to
  `status not in ("terminated", "withdrawn")`; the existing
  `termination-without-cascade-evidence` code is unchanged in meaning; a new
  `identity-cascade-incomplete` fires when a `governed_identity` dependent on
  a terminated OR withdrawn instrument lacks either evidence field;
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
3. `pytest tests/conformance-gate tests/doc-health tests/credential_contracts`.
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
  check's exit stays 0 over the same fixture corpus.
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

1. **`identity_kind` = `[entra_app_registration]`, one member** — derived
   (research.md Decision 1). The SET is not ambiguous; the SPELLING is a
   choice.
2. **The drift record is a second `kind` in the roster schema file**, not a
   second file (research.md Decision 2).
3. **`issuance_preconditions` is an OBJECT with closed property names and
   boolean values, with three members** — the roster-drift token plus the two
   precedent tokens it regularizes. The alternative (an array, or a
   single-member set) breaks a live OpsxFactory record and contradicts the
   tree's own definition of an additive-minor bump. **This is the decision
   most worth the architect's time** (research.md Decision 3).
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
    consequent routing of two FR-016 negatives (cross-domain shared identity →
    doc-health fixtures; misplacement → repo fixture, because a packaged file
    cannot express a path rule about itself) (research.md Decision 7).
12. **The repo scan excludes this checkout's own
    `examples/client-identity-roster/`**, or pointing the validator at
    openxFactory reports its own corpus as misplaced.
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
