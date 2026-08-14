# Tasks: client identity roster neutral contracts and conformance wiring

**Feature**: `007-client-identity-roster` · **Change**: `add-client-identity-roster`

**Inputs**: [plan.md](plan.md) (as amended by
[plan-gate-rulings-2026-08-14.md](plan-gate-rulings-2026-08-14.md)),
[research.md](research.md), [spec.md](spec.md),
[clarify-rulings-2026-08-14.md](clarify-rulings-2026-08-14.md).

The governing change's own `tasks.md` stays governance-level and is NOT
duplicated here — the protocol forbids two task lists for one body of work, and
Speckit owns this one. Where the packet's sketch and this list differ on
packaging (its single `examples/client-identity-roster.example.yaml` versus
FR-019's directory), the spec's Assumptions block already dispositions it: the
sketch is superseded on packaging convention.

## Format

`[ID] [P?] [Story] Description` — IDs are `<phase>.<n>`, the 006 precedent's
scheme, so a task ID sorts into its phase. `[P]` marks a task that touches only
files no concurrent task touches and whose dependencies have landed. `[Story]`
maps the task to spec.md's user stories (US1–US6); tasks serving the whole
feature carry no story label.

Every task below names its TARGET FILES and its VERIFICATION — the validator,
suite, or command whose result proves the task done. A task with no runnable
verification is not done, it is asserted.

## Phase order and its one deliberate departure

Phases follow the plan's clusters, in dependency order rather than in the
plan's alphabetical order. The one departure: **Cluster D (packaged examples)
is Phase 3 and Cluster C (the fixture corpus) is Phase 4**, because Cluster C's
killed-flaw POSITIVES live inside Cluster D's two packaged fragments (plan.md,
Cluster C). Authoring C before D would mean authoring assertions about files
that do not exist. No task is dropped or moved between clusters.

---

## Phase 0 — Preconditions and baselines

**Purpose**: establish the facts later phases assume, before those phases can
spend work on them. Two of these are ruling-mandated gates; one is the
before-state FR-030 is measured against.

- [ ] 0.1 **[HARD GATE on Phase 3]** Verify the multi-surface reader's citable
      provider fact (ruling A-16). Establish that ONE provider-native
      permission or directory role, in its narrowest available form, reaches
      BOTH the `business_central` and the `exchange` read surfaces, and that no
      read-only role scoped to just one of the two exists. The evidence must be
      a citation to the provider's own documentation or to a record in the
      OpsxFactory evidence chain — searched offline against the pinned
      checkout and the builder's own reference material (FR-029 forbids a live
      provider call). Record the citation in `research.md` under Decision 8 as
      a dated sub-section.
      **On failure: STOP AND ESCALATE to the architect.** Report the candidate
      permissions/roles examined and why each failed. Do NOT synthesize a
      provider fact, and do NOT soften the case into a single-surface reader —
      either under-delivers FR-019 and silently drops SC-002's fourth positive.
      *Verification*: the citation exists in `research.md` and names a
      resolvable source; Phase 3 does not begin until this task is `[x]` or the
      escalation is ruled.
- [ ] 0.2 [P] Re-confirm the ruling A-7 precondition: no consent class registry
      anywhere in the reachable estate aliases a key spelled `withdrawn`.
      *Files*: read-only sweep of every `status_aliases` block
      (`examples/consent-instrument/`, `contracts/schemas/`, and any
      `xFactories/*/` registry reachable from the aggregation checkout).
      *Verification*: `grep -rn "status_aliases" -A6` over the estate returns no
      `withdrawn` KEY; record the sweep date in `research.md` Decision 5.
      On a hit, STOP — growing `NEUTRAL_STATUSES` would change an existing
      registry's verdict and breach FR-030.
- [ ] 0.3 [P] Capture the green-before baseline for the four MODIFIED
      capabilities, so "unmodified in behaviour" (FR-030) is measured and not
      assumed. Record verdicts AND finding codes, not just exit codes.
      *Commands*: `python3 scripts/validate-consent-instruments.py` (5
      positives, 5 registered negatives, 2 purpose probes);
      `python3 scripts/validate-credential-contracts.py .` (2 positives, 3
      registered negatives); `pytest tests/credential_contracts/`;
      `pytest tests/doc-health/`; `pytest tests/conformance-gate/`.
      *Verification*: the captured output is stored in the feature directory as
      a scratch note (not committed) and re-compared at 10.4.

**Checkpoint**: 0.1 ruled, 0.2 clean, 0.3 captured → Phase 1 may begin.

---

## Phase 1 — Cluster A: the roster schema family

**Blocks**: Phases 2, 3, 4, 6. **Depends on**: nothing (0.x are advisory except
0.1's gate on Phase 3).

*Target file (all of Phase 1)*:
`contracts/schemas/xfactory-client-identity-roster.schema.yaml`.

- [ ] 1.1 [US1] Schema skeleton: Draft 2020-12 with `$schema` and `$id`,
      `contract_schema_version: 1`, a top-level `oneOf` over the two kinds,
      `additionalProperties: false` on EVERY object at every depth. **Both
      kinds declare `schema_version: const: 1`** (ruling A-2) so the single
      manifest row is unambiguous.
      *Verification*: `python3 -c "import yaml,jsonschema;
      jsonschema.Draft202012Validator.check_schema(yaml.safe_load(open(...)))"`
      passes; a grep confirms no object lacks `additionalProperties: false`.
- [ ] 1.2 [US1] The six CLOSED vocabularies as `$defs`, each enumerated
      explicitly and each carrying a `description` naming its extension route
      (FR-007, FR-031, FR-034): `admission_surface`
      (`business_central`, `exchange`), `authority_class`
      (`observe`, `mutate` — destructive UNREPRESENTABLE, FR-005),
      `residency_model` (`client_tenant_single`, `vendor_tenant_multi`),
      `enforcement_mode` (`provider_enforced`, `logic_enforced`),
      `lifecycle_state` (`planned`, `enrolled`, `retired`), and `identity_kind`
      (`entra_app_registration`, ONE member, research.md Decision 1). Plus
      `$defs.free_token` — pattern `^[a-z0-9][a-z0-9_-]*$` — for
      `blast_radius_unit` and `duty`.
      *Verification*: six negatives in 4.2 each refused; SC-014.
- [ ] 1.3 [US1] `$defs.identity_key` — the five-element uniqueness tuple,
      **element 3 = `authority_class_intended`** (ruling R-N1), defined ONCE
      and referenced by both the uniqueness rule and the drift record. The
      `description` states the choice and its reason: a key must be declarative
      and stable, and the achieved class is observational and moves with
      provider state.
      *Files*: also the schema description of kind 2 (task 1.9).
      *Verification*: 2.4's uniqueness rule reads element 3 from
      `authority_class_intended`; 4.1's `full-tuple-duplicate.yaml` is refused
      naming all five elements (FR-006).
- [ ] 1.4 [US1] Kind 1 `xfactory_client_identity_roster` top level:
      `schema_version`, `kind`, `client_ref`, `domain`, `legend`, `entries[]`
      (`minItems: 1`). `legend` is
      `{blast_radius_units: {<token>: <provider id>}, duties: {…}}` — a MAPPING,
      so "declared twice for the same key" is unrepresentable at the schema
      level and the checkable duplicate (FR-034) is a token in BOTH maps or a
      legend entry never used (2.8).
      *Verification*: 3.2/3.5 fragments validate; 4.2's legend negatives refused.
- [ ] 1.5 [US1] The entry object — the FR-001 field list UNREDUCED:
      `identity_ref` (string), `identity_kind`, `home_tenant`,
      `principal_locations[]`, `residency_model`, `admission_surface`, `duty`,
      `blast_radius_unit`, `authority_class_intended`,
      `authority_class_achieved`, `granted_permissions[]` (`minItems: 1`,
      provider-native strings), `admission[]`, `declared_excess` (optional),
      `per_unit_principal_available`, `lifecycle_state`,
      `standing_credential_attestation`, `ratified_by` (domain-qualified),
      `consent_ref`.
      *Verification*: a field-list assertion in
      `tests/client-identity-roster/test_client_identity_roster.py` compares the
      entry's declared properties against FR-001's list — so a later refactor
      cannot quietly drop `granted_permissions[]` or `admission[]` (SC-004).
- [ ] 1.6 [US1] `admission[]` — `type: array, minItems: 1` (**not 2**; a
      one-member array is a legal single-act expression, ruling A-N3), whose
      members carry `surface`, `act`, `achieved_scope` (provider-native),
      `enforcement_mode`, `evidence_ref`, `verified_at`. `evidence_ref` is a
      DECLARED POINTER object `{repo, path, sha?}` (FR-037) with a description
      stating that no validator resolves it. `verified_at` is required and
      carries NO maximum age (FR-033 — no decay in this release); an act with
      no `evidence_ref` is unverified BY DERIVATION, never by an independent
      `verified: false` field an author could contradict (FR-003).
      *Verification*: 4.1's `unverified-act-counted-as-access.yaml` and
      `evidence-ref-malformed.yaml` refused; 3.2's two-act case validates.
- [ ] 1.7 [US1] `declared_excess` (optional object: `spanned_surfaces[]`,
      `provider_reason`, `bound_mechanism`, `gate_obligation`,
      `enforcement_test_ref`), `per_unit_principal_available` (boolean, per
      surface), `standing_credential_attestation` (the claim plus its evidence
      pointer) — FR-008, FR-009, FR-010, FR-013.
      *Verification*: 4.1's `missing-enforcement-test.yaml`,
      `provider-enforced-without-per-unit-principal.yaml`,
      `per-unit-principal-available-but-logical.yaml`,
      `false-standing-credential-attestation.yaml` each refused for its own code.
- [ ] 1.8 [US1] The `vendor_tenant_multi` obligations as an `if/then` on
      `residency_model` IN THE SCHEMA (not only in the validator), so a
      validator refactor cannot lose them: tenant allow-list enforced at token
      validation, per-client authorization state, per-client revocation
      evidence, the cross-client credential-span statement, the per-client
      consent amendment (FR-012). Residency branches on NOTHING else — in
      particular on no `authority_class_*` (ratified constraint 1).
      *Verification*: 4.1's `vendor-tenant-multi-missing-obligations.yaml`
      refused; a grep asserting no `authority_class` appears inside any
      residency branch (constraint 1's mechanized form).
- [ ] 1.9 [US6] Kind 2 `xfactory_client_identity_drift_finding`:
      `schema_version`, `kind`, `identity_ref` (the `$defs.identity_key`
      OBJECT — deliberately a different shape from the entry's STRING
      `identity_ref`, FR-035, documented in the description), `fragment_ref`,
      `rule_id`, `roster_value` and `observed_value` (BOTH required — the
      ratified delta scenario), `observed_at`, `opened_at`, `status`
      (`open|resolved|disposed`), `disposition_ref`. The description states:
      (a) why the two `identity_ref` shapes differ; (b) that the tuple's third
      element is the INTENDED class so the join survives drift (R-N1); (c) that
      the record claims no alignment with and no storage in any doc-health
      findings register, because none exists; (d) that recording a finding
      mutates nothing (FR-027).
      *Verification*: 3.6's example validates; 4.3's two negatives refused.
- [ ] 1.10 [US2] Declare the PLACEMENT in the schema description:
      `credentials/client-identity-roster/<client_ref>.yaml`, one file per
      (client, domain), and note that
      `scripts/validate-credential-contracts.py`'s skip-with-notice over that
      path is EXPECTED and blessed (FR-020). The drift kind carries no
      placement rule in this release (research.md Decision 2's consequence).
      *Verification*: the manifest `consumption_rule` at 9.1 states the same two
      facts; 2.9's sweep enforces the placement.

**Checkpoint**: the schema validates as a schema and both kinds are
expressible → Phases 2, 3, 6 may begin.

---

## Phase 2 — Cluster B: the canonical validator

**Depends on**: Phase 1. **Blocks**: Phase 4's repo fixtures, Phase 5.

*Target file (all of Phase 2)*: `scripts/validate-client-identity-roster.py`.

- [ ] 2.1 Module skeleton following the sibling `validate-*.py` contract
      (FR-015, FR-029): `ROOT = Path(__file__).resolve().parents[1]` (no
      host-absolute path), ONE positional target-repo argument, `print(__doc__)`
      + `SystemExit(2)` on wrong argc, a `Findings` class emitting
      `ERROR [kebab-code] message` (the consent validator's shape), a closing
      verdict line, exit `0` clean / `1` findings / `2` harness error.
      Filesystem reads only: no network, no model call, no subprocess to a
      provider tool.
      *Verification*: `python3 scripts/validate-client-identity-roster.py`
      with no argument exits 2 and prints usage; `pytest tests/` runs under the
      `tests/hermeticity.py` guard, which makes an outbound reach a test
      failure (SC-011).
- [ ] 2.2 The self-test layer (FR-018): positives validate clean; each negative
      must raise its REGISTERED code, with an optional pinned detail substring
      where the code alone would be satisfied by a generic `schema` finding —
      the consent validator's two-part expectations table. FIVE failure modes
      are themselves errors: a registered probe with no file, a file with no
      registration, a negative that passes, a negative that fails for the WRONG
      code, and a negative whose code fires without the pinned detail.
      *Verification*: temporarily break one negative each way and confirm five
      distinct self-test failures; SC-001.
- [ ] 2.3 Record-internal rules, group 1 — closed-vocabulary and shape
      refusals, each naming the closed set and the extension route in its
      message (FR-005, FR-007, FR-031, FR-034, SC-014).
      *Verification*: 4.2's six vocabulary negatives.
- [ ] 2.4 [US1] Uniqueness and the alias rule — the feature's sharpest pair.
      Uniqueness: entries sharing the whole `$defs.identity_key` tuple are a
      finding NAMING EVERY ELEMENT; entries differing in ANY element validate
      clean (FR-006). The alias rule (FR-038) is a THREE-predicate conjunction
      and no broader: two entries differ SOLELY in a free token, AND are
      observationally identical (same `granted_permissions[]` SET and same
      admission acts by `(surface, act, achieved_scope, enforcement_mode)`),
      AND declare no duty-separation rationale. A pair differing in
      `achieved_scope`, in permissions, or carrying the rationale validates
      clean.
      *Verification*: 4.6's single-run discrimination — the genuine per-unit
      pair and genuine duty pair at ZERO findings while the alias pair is
      refused (SC-002). A rule broad enough to catch all three fails.
- [ ] 2.5 [US1] Admission verification and effective reach (FR-002, FR-003):
      an act with no `evidence_ref` is unverified and EXCLUDED from effective
      reach; effective reach is COMPUTED as the union of verified acts, never
      declared; provider consent with no admission act is refused stating that
      consent is not admission.
      *Verification*: 4.1's `consent-recorded-as-access.yaml` and
      `unverified-act-counted-as-access.yaml`; 3.2's union reach.
- [ ] 2.6 [US1] Authority: `authority_class_achieved` checked against
      `granted_permissions[]` so an achieved class the permissions contradict
      is refused (FR-004); achieved-above-intended with no `declared_excess`
      refused (FR-010); undeclared reach refused NAMING the surface and the
      permission that reaches it (FR-009); a name or stated purpose describing
      narrower authority than it achieves refused (FR-010). Structural scoping:
      provider-enforced claimed where no per-unit principal exists is a
      finding, and an available per-unit principal left unused while logical
      enforcement is declared is a finding NAMING the available principal
      (FR-008). The rules must NOT invalidate a deliberately narrow identity
      because the provider's granularity is coarser than the axis (FR-009).
      *Verification*: 4.1 and 4.4's negatives; 3.3's multi-surface reader
      validates clean, which is the "must not invalidate" half.
- [ ] 2.7 [US1] Residency (FR-012) and lifecycle/attestation (FR-013): a
      registration homed outside the client tenant may not declare
      client-resident; `vendor_tenant_multi` requires its five obligations; a
      `planned` entry validates and is NEVER reported as missing or incomplete;
      a retired entry retains its record; a credential held outside an approved
      grant window makes the attestation false and is reported against that
      entry.
      *Verification*: 4.1's `vendor-homed-declared-client-resident.yaml`,
      `vendor-tenant-multi-missing-obligations.yaml`,
      `false-standing-credential-attestation.yaml`; 3.4's `planned` positive.
- [ ] 2.8 [US1] Both roots and the legend: an entry naming a capability and no
      consent instrument is invalid, stating that consent — not our own
      ratification — authorizes standing in another party's tenant; a `mutate`
      entry naming no ratified capability is an ERROR that fails the gate, not
      a report (FR-014). Legend: a free token used with no legend entry, a
      token appearing in BOTH legend maps, or a legend entry never used is a
      finding (FR-034).
      *Verification*: 4.1's `entry-without-consent-instrument.yaml`,
      `mutate-without-ratified-capability.yaml`; 4.2's two legend negatives.
- [ ] 2.9 [US2] The repo-scan layer, two passes. (a) **Whole-repo kind sweep**
      (FR-036): `rglob` every `*.y*ml` skipping `.git`, `node_modules`,
      `__pycache__`, `.venv`, and — when the target IS this checkout —
      `examples/client-identity-roster/`; any file carrying
      `kind: xfactory_client_identity_roster` outside
      `credentials/client-identity-roster/` raises `misplaced-roster-instance`
      naming the offending path AND the declared placement. (b)
      **Declared-placement validation**: every fragment at the declared path is
      schema-validated and rule-checked, and the run prints a COUNT of records
      checked. Plus the repo-context rule the packaged corpus cannot express:
      gate-obligation RESOLUTION against the target's `workflows/<name>.yaml`
      gates, with an unresolvable obligation a finding (FR-011).
      *Verification*: 4.5's repo fixtures 4 and 5; running the validator against
      this checkout must NOT report its own packaged corpus as misplaced.
- [ ] 2.10 [US2] Absence, and the negative guarantee (FR-022, FR-032, SC-013):
      a target with no `credentials/client-identity-roster/` directory, or the
      directory with no files, prints an EXPLICIT NOTICE naming the absence and
      exits 0. NO code path in the module derives an expected entry set — not
      from `credentials/requirements.yaml`, not from any other inventory.
      *Verification*: 4.5's repo fixture 3; 4.7's source-level assertion.

**Checkpoint**: the validator runs, self-tests, and scans → Phases 4 and 5 may
begin.

---

## Phase 3 — Cluster D: packaged examples

**Depends on**: **0.1 (HARD)** and Phase 1. **Blocks**: Phase 4's positives and
2.2's self-test corpus.

*Target directory*: `examples/client-identity-roster/`.

> Every task in this phase lists **0.1 as a hard dependency**. If 0.1 escalated
> and has not been ruled, this phase does not start.

- [ ] 3.1 [US2] `examples/client-identity-roster/README.md` carrying
      `Status: ratified` plus a `Ratified by:` line naming
      `add-client-identity-roster` and the bundle it registers at — the
      `contracts/openxwallet/README.md` (006) header precedent, not the older
      siblings' `Status: draft` — with the sibling READMEs' layout block.
      *Depends on*: 0.1. *Verification*: doc-health's status-validity and
      tag-hygiene families report no finding (10.3).
- [ ] 3.2 [US1] `client-identity-roster-farheap-opsx.example.yaml` — the
      Business Central worked case, transcribed from
      `OpsxFactory:tenants/farheap-bc-observer-identity-evidence-v1.yaml`: ONE
      entry with TWO admission acts (the provider-enforced Sandbox1 application
      user with no production application user; the admin-center Entra-app
      authorization with no scope selector, therefore tenant-wide), the UNION
      effective reach, and the declared excess with its provider reason, gate
      obligation and enforcement-test reference. `granted_permissions[]` are
      the real four (`API.ReadWrite.All`, `Automation.ReadWrite.All`,
      `AdminCenter.ReadWrite.All`, `app_access`), which is what makes this
      simultaneously the name/purpose-mismatch case
      (`opsx-farheap-bc-observer` achieving mutation) expressed through
      `declared_excess` rather than by renaming anything in a domain repo.
      `evidence_ref` pointers name `opensoft/OpsxFactory` and the real
      `tenants/farheap-bc-sandbox1-verify-probe-evidence-v*.yaml` paths — real
      pinned content, left UNRESOLVED by the validator (FR-037). Legend binds
      every free token used.
      *Depends on*: 0.1, 1.4–1.7. *Verification*: 2.2 self-test clean; SC-003
      and SC-004 are read off this file.
- [ ] 3.3 [US1] The provider-forced multi-surface reader entry, in the same
      fragment: `granted_permissions[]` in provider-native identifiers,
      `declared_excess.provider_reason` carrying **0.1's citation verbatim**,
      plus the gate obligation and enforcement-test reference FR-010 requires.
      *Depends on*: **0.1 (this task is the reason 0.1 is a gate)**.
      *Verification*: validates with ZERO findings (SC-002's fourth positive)
      while 2.6's undeclared-reach rule refuses the same entry with the
      declaration removed.
- [ ] 3.4 [US1] The `planned` entry, in the same fragment: `lifecycle_state:
      planned`, an identity not yet created, its kind declared as intent.
      *Depends on*: 0.1, 1.7. *Verification*: ZERO findings (FR-013, SC-002);
      and it is not reported as missing or incomplete (2.10, SC-013).
- [ ] 3.5 [P] [US1] `client-identity-roster-farheap-ledgerx.example.yaml` — the
      SECOND fragment for the SAME client held by a SECOND domain (fragments
      are per (client, domain), which is why the four mandated cases span two
      files, ruling C3). Carries the GENUINE duty-separated pair (the
      `ledgerx-farheap-bc-poster` / `-provisioner` precedent, differing in
      granted permissions or declaring the duty-separation rationale) and the
      GENUINE per-unit pair (differing in `achieved_scope`).
      *Depends on*: 0.1, 1.4–1.7. *Verification*: both pairs at ZERO findings in
      the same run that refuses 4.1's alias pair — the SC-002 discrimination
      asserted at 4.6.
- [ ] 3.6 [P] [US6] `client-identity-drift-finding.example.yaml` — a complete
      finding: the `identity_key` OBJECT (element 3 = the entry's
      `authority_class_intended`), `fragment_ref` naming 3.2's fragment,
      `rule_id`, `roster_value`, `observed_value`, `observed_at`, `opened_at`,
      `status: open`, `disposition_ref`.
      *Depends on*: 0.1, 1.9. *Verification*: 2.2 self-test clean; 4.3's two
      negatives are its refusals.

**Checkpoint**: four mandated cases packaged across two fragments, drift
example packaged → Phase 4 may assert against them.

---

## Phase 4 — Cluster C: the fixture corpus

**Depends on**: Phases 1, 2, 3. **Blocks**: Phase 5.

*Target directories*: `examples/client-identity-roster/negative/`,
`tests/client-identity-roster/`.

Negatives take the CONSENT family's header dialect
(`# INVALID <record noun> — violates <requirement> (<rule>): <what is wrong>` /
`# … (finding <finding-code>)`), one violation per file, each registered by
filename in the validator's expectations table.

- [ ] 4.1 Author the SIXTEEN record-internal packaged negatives — twelve of
      FR-016's named rules (the thirteenth packaged named rule,
      out-of-vocabulary admission surface, sits with its vocabulary siblings in
      4.2) plus four per-rule confirmations FR-016's "at minimum" list does not
      enumerate (FR-003, FR-008's second half, FR-010's name/purpose clause,
      FR-012): `consent-recorded-as-access.yaml`,
      `unverified-act-counted-as-access.yaml`, `undeclared-reach.yaml`,
      `achieved-exceeds-intended-undeclared.yaml`,
      `name-understates-achieved-authority.yaml`,
      `missing-enforcement-test.yaml`,
      `provider-enforced-without-per-unit-principal.yaml`,
      `per-unit-principal-available-but-logical.yaml`,
      `vendor-homed-declared-client-resident.yaml`,
      `vendor-tenant-multi-missing-obligations.yaml`,
      `mutate-without-ratified-capability.yaml`,
      `entry-without-consent-instrument.yaml`,
      `false-standing-credential-attestation.yaml`,
      `destructive-authority-class.yaml`, `full-tuple-duplicate.yaml`,
      `alias-pair-observationally-identical.yaml`.
      *Verification*: each refused by its OWN registered code (2.2); SC-001.
- [ ] 4.2 [P] The closed-vocabulary and legend negatives (SC-014):
      `admission-surface-out-of-vocabulary.yaml`,
      `residency-model-out-of-vocabulary.yaml`,
      `enforcement-mode-out-of-vocabulary.yaml`,
      `lifecycle-state-out-of-vocabulary.yaml`,
      `identity-kind-out-of-vocabulary.yaml`, `legend-token-missing.yaml`,
      `legend-token-declared-twice.yaml`, `evidence-ref-malformed.yaml`.
      *Verification*: one negative per closed set plus both legend cases, each
      refusal NAMING the closed vocabulary and the extension route.
- [ ] 4.3 [P] [US6] The drift-record negatives:
      `drift-finding-without-roster-value.yaml`,
      `drift-finding-without-observed-value.yaml` (FR-035).
      *Verification*: refused by their own codes in the 2.2 self-test.
- [ ] 4.4 [P] `achieved-class-contradicted-by-permissions.yaml` (**ruling
      A-11**) — an entry declaring `authority_class_achieved: observe` while
      its `granted_permissions[]` carry a write- or delete-capable permission.
      This homes FR-004's rule, which is distinct from
      `achieved-exceeds-intended-undeclared.yaml`'s (that one proves
      achieved-above-intended must be DECLARED; this one proves an achieved
      class cannot be ASSERTED against its own permissions). Neither
      substitutes for the other.
      *Verification*: refused by 2.6's FR-004 code, registered in the
      expectations table.
- [ ] 4.5 The FIVE repo-shaped fixtures in `tests/client-identity-roster/
      test_client_identity_roster.py`, built in `tmp_path` from inline
      templates (the `tests/conformance-gate/test_conformance_checks.py`
      idiom): (1) conformant → exit 0; (2) nonconformant
      `mutate`-without-ratified-capability → nonzero; (3) no-fragment → exit 0
      + explicit notice; (4) **unresolvable gate obligation** (ruling A-11) —
      an entry whose `declared_excess.gate_obligation` names a gate ABSENT from
      that repo's `workflows/`, while the repo carries at least one REAL gate
      so the finding proves non-resolution rather than an empty tree → nonzero
      with FR-011's code; (5) misplacement — the roster kind at
      `tenants/stray.yaml`, outside `credentials/` entirely → nonzero with
      `misplaced-roster-instance` (SC-005).
      *Verification*: `pytest tests/client-identity-roster/`; fixture 1 is
      fixture 4's discrimination partner (its obligation DOES resolve).
- [ ] 4.6 **The SC-002 discrimination assertion** — ONE run over the packaged
      corpus producing THREE verdicts: the genuine per-unit pair ZERO findings,
      the genuine duty pair ZERO findings, the alias pair REFUSED. Asserted in
      `tests/client-identity-roster/test_client_identity_roster.py` as a single
      test so a rule broad enough to catch all three cannot pass.
      *Verification*: `pytest tests/client-identity-roster/ -k discrimination`;
      this is the killed-flaw acceptance test named at 10.5.
- [ ] 4.7 [P] The SC-013 negative assertion: a source-level test that NO module
      in this feature reads `credentials/requirements.yaml` or any other
      inventory to derive an expected entry set — the checklist item and the
      analyze pass should both look for one and find nothing.
      *Verification*: `pytest tests/client-identity-roster/ -k no_completeness`.
- [ ] 4.8 Confirm the FR-016 coverage re-count holds against the built corpus:
      **16 named rules, 16 homed, 0 unhomed** (13 packaged, 2 repo-shaped, 1 in
      the doc-health corpus at 6.5) — plan.md's Cluster C table.
      *Verification*: walk the table against the files on disk; the 2.2
      registration check independently proves no file lacks a probe and no probe
      lacks a file.

**Checkpoint**: every named rule has a refused negative and every killed-flaw
positive passes clean.

---

## Phase 5 — Cluster F: pack membership (Decision A, archive blocker)

**Depends on**: Phases 2, 4. **Parallel with**: Phases 6, 7, 8.

- [ ] 5.1 [US3] Grow `tests/conformance-gate/test_conformance_checks.py` to
      load `validate-client-identity-roster` alongside the three `check-*`
      modules, exercising the delta's FOUR pack scenarios: an entry
      nonconformance → nonzero; a `mutate` entry with no ratified capability →
      ERROR not report; a conformant repo → 0; **no fragment → 0 with an
      explicit notice** (FR-022). The three existing checks' 15 tests must pass
      UNMODIFIED — only new tests are added.
      *Verification*: `pytest tests/conformance-gate/`; diff against 0.3's
      baseline shows no existing test changed.
- [ ] 5.2 [P] [US3] Update that module's docstring — "Locks the three checks" →
      four. This is the only pack COUNT site this feature owns.
      *Verification*: grep; `openspec/specs/domain-conformance-checks/spec.md`
      is confirmed UNEDITED (the archive step rewrites promoted text, the same
      rule FR-025 states for doc-health).
- [ ] 5.3 [P] Carry the ruling A-N2 residual so it is not silently dropped:
      pack blocking is NOMINAL at archive — codexFactory's gate enumerates the
      pack's three members by NAME and OpsxFactory's gate invokes no canonical
      check — so domain-gate wiring is a named FOLLOW-UP, out of scope by
      FR-030/SC-012 because it is a domain-repository edit. Recorded in
      plan.md (Cluster F) and echoed in the `traceability.yaml` note for
      FR-022/SC-006 at 10.1, so the reviewer of this feature and the author of
      the follow-up both see it.
      *Verification*: the residual appears in both places; the claim this
      feature makes is exactly SC-006's, no wider.

---

## Phase 6 — Cluster G: the sixteenth doc-health family

**Depends on**: Phase 1. **Parallel with**: Phases 5, 7, 8.

- [ ] 6.1 [US5] `scripts/doc_health/client_identity_composition.py` exposing
      `fam_client_identity_composition(ctx) -> list[Finding] | Skip`. Assembly:
      iterate `sorted(ctx.repo_paths.items())`, read
      `<repo>/credentials/client-identity-roster/*.y*ml`, group by
      `client_ref`. TWO explicit skips: `ctx.agg_root is None` → "single-repo
      run: no aggregation checkout"; no client held by two or more domains →
      "no client is held by two or more domains: nothing to compose". The skip
      is CORPUS-level, not per-client — a mixed corpus reports (FR-023).
      *Verification*: 6.6's skip tests.
- [ ] 6.2 [P] [US5] The `shared-identity-material` finding class: two fragments
      for one `client_ref` from DIFFERENT `domain` values whose entries name
      the same identity MATERIAL — the same `identity_ref`, or the same
      provider-native application identifier in `principal_locations[]`. Keyed
      on MATERIAL, never on (surface, class) collocation.
      *Verification*: 6.6 asserts the FR-024 discrimination — two domains each
      holding their OWN separate identity on one surface and class is NOT a
      finding at any level.
- [ ] 6.3 [P] [US5] The `undeclared-cross-domain-reach` finding class: an
      admission act or `declared_excess` in domain A's fragment achieves scope
      over an admission surface for which A publishes no entry, while another
      domain's fragment for the same client declares that surface. The
      intra-repo undeclared-reach rule (FR-009, task 2.6) is NOT duplicated
      here. Each `Finding` sets its own `resolution` — `CONTESTED` where it
      contradicts a ratified capability, the dataclass default otherwise (the
      three late families' precedent); the family stays OUT of
      `FAMILY_RESOLUTION`.
      *Verification*: 6.6 asserts no intra-repo finding code ever appears in
      this family's output (FR-023, SC-009).
- [ ] 6.4 [US5] Registration and the count-bearing prose this feature OWNS:
      import at `scripts/doc_health/families.py:25`; the
      `"client-identity-composition"` key in `FAMILIES` (`families.py:674-690`);
      the id added to `FAMILY_IDS` (`scripts/doc_health/__init__.py:52-70`) so
      the family renders a report section; `families.py:1` "The fifteen
      contract check families." → **sixteen**; the ownership note at
      `families.py:7-11` grown to name the sixteenth module. ORDINALS
      elsewhere are left alone and `openspec/specs/doc-health/spec.md` is NOT
      edited (FR-025). The pre-existing omission of `proposal-origin` from
      `FAMILY_IDS` is recorded in research.md and NOT fixed here.
      *Verification*: `python3 scripts/doc-health.py --repo-root <agg>` lists
      sixteen families and renders the new section; grep confirms the promoted
      spec and the ordinals are untouched.
- [ ] 6.5 [US5] Fixtures at
      `tests/doc-health/fixtures/client-identity-composition/` — at least THREE
      repo directories so the corpus proves both finding classes AND the FR-024
      non-finding: two domains sharing identity material for one client; two
      domains with separate identities on one surface and class; a
      single-fragment client for the skip case. This corpus is also where
      FR-016's "cross-domain shared identity" negative lives (research.md
      Decision 7).
      *Verification*: 6.6.
- [ ] 6.6 [US5] `tests/doc-health/test_client_identity_composition.py`.
      **Ruling A-9 — the trap this suite must not fall into**:
      `tests/doc-health/conftest.py` `make_ctx` defaults **`agg_root=None`**
      (line 66), and this family's FIRST branch is
      `ctx.agg_root is None → Skip`. **Every test MUST pass `agg_root`
      explicitly**, or it short-circuits into the skip and passes vacuously —
      green while measuring nothing. The single-repo-skip test passes
      `agg_root=None` EXPLICITLY so the omission can never be mistaken for
      intent. Tests: both finding classes; the FR-024 non-finding; both skips;
      no intra-repo code in the output; and DETERMINISM — the family run twice
      over one fixture context with `__dict__`-equal sorted findings, the
      `tests/doc-health/test_suite.py:15-19` pattern (SC-011, which a vacuous
      skip would satisfy trivially).
      *Verification*: `pytest tests/doc-health/test_client_identity_composition.py`;
      plus `pytest tests/doc-health/` whole-suite, where the new family must add
      findings to NO existing family's fixtures.
- [ ] 6.7 [US5] **Ruling A-N4** — prove SC-006 across BOTH corpora: run
      `scripts/validate-client-identity-roster.py` over each doc-health
      cross-domain fixture repo and assert **exit 0** on each. Without this the
      "leaves the domain gate exit unchanged" half of SC-006 is an assertion
      about a corpus nothing measured; with it, the shared identity is proven
      intra-repo CONFORMANT and the finding proven composition-only.
      *Files*: `tests/doc-health/test_client_identity_composition.py` (or its
      roster sibling) — a test, not a manual step.
      *Verification*: the test passes; paired with 5.1's nonzero-exit case it is
      SC-006's complete measurement.

---

## Phase 7 — Cluster H: `credential-contracts` (Decision B, archive blocker)

**Depends on**: nothing in this feature. **Parallel with**: Phases 5, 6, 8.
**Blocks**: Phase 9 (its file content must be final before digests).

- [ ] 7.1 [US6] `contracts/schemas/xfactory-credential-contracts.schema.yaml` —
      `issuance_preconditions` on the `xfactory_credential_requirements`
      requirement item as an OBJECT with `minProperties: 1`,
      `additionalProperties: false`, and THREE explicitly declared members
      whose values are **`const: true`** (ruling A-3a — a precondition is
      declared or not declared; `false` reads as governance while asserting
      nothing). Each member carries a one-line `description` naming its
      governed condition (ruling A-3b); `accepted_request_required` and
      `registered_active_subject` CITE `adopt-deployment-handoff-boundary`,
      which is what makes "regularizes rather than replaces in place" legible
      in the artifact. Declaring nothing must leave every existing requirement
      record valid.
      *Verification*: 7.4's live-record regression is the decisive one.
- [ ] 7.2 [US6] `scripts/validate-credential-contracts.py` — one new
      `_semantic_findings` branch emitting `issuance-precondition-unknown`
      NAMING the closed vocabulary, firing on BOTH failure shapes: an
      out-of-vocabulary member and a false-valued member (ruling A-3a). The
      semantic mirror is STRUCTURALLY REQUIRED, not decorative: this
      validator's self-test adjudicates registered negatives against
      `_semantic_findings` ONLY (`:108`), so a schema-only implementation makes
      its own negatives unregisterable and leaves SC-008 with no probe.
      *Verification*: 7.3's negatives are reported as expected, not as
      `negative-should-fail`.
- [ ] 7.3 [US6] Fixtures in `examples/credential-contracts/`: ONE positive
      requirement record declaring `roster_drift_clear_required: true`; TWO
      negatives under `negative/` (an out-of-vocabulary token; a member valued
      `false`), both registered in `NEGATIVE_EXPECTATIONS`, both keeping THAT
      directory's terser `# NEGATIVE (expect: <code>). …` dialect. The existing
      positives, which declare nothing, must stay valid.
      *Verification*: `python3 scripts/validate-credential-contracts.py .` —
      that trio plus the untouched positives IS SC-008's whole neutral
      criterion, fixture-proven because no producer of live drift findings
      exists at archive time. Live refuse-then-allow is NOT claimed here.
- [ ] 7.4 [US6] **The load-bearing regression**: run
      `python3 scripts/validate-credential-contracts.py <OpsxFactory checkout>`
      and confirm the LIVE records carrying `issuance_preconditions`
      (`credentials/requirements.yaml`, `aks_workload_administration` and
      `deployment_operator`) still PASS. This is the direct test of research.md
      Decision 3 and the one result that would falsify the additivity claim —
      an array-shaped or single-member vocabulary breaks them, which would
      breach FR-030, FR-028 and the tree's own additive-minor definition.
      *Verification*: exit 0 over the domain checkout, with NO file in it
      modified (SC-012). Also `pytest tests/credential_contracts/`.

---

## Phase 8 — Cluster I: `consent-instrument` (archive blocker)

**Depends on**: 0.2. **Parallel with**: Phases 5, 6, 7. **Blocks**: Phase 9.

- [ ] 8.1 [US4] Grow the closed status enum by `withdrawn` at EVERY normative
      declaration together (FR-039): `consent-instrument.schema.yaml:194` (the
      record's `status`) AND `:209` (the `status_history[].status`, a second
      declaration in the same file), and
      `consent-instrument-class-registry.schema.yaml:77` (the `status_aliases`
      value constraint). Bump `contract_schema_version` 1 → 2 on BOTH schema
      files. The RECORD envelope's `schema_version: const: 1` does NOT change —
      changing it would invalidate every existing instrument, the opposite of
      additive.
      *Verification*: 8.6's regression; `withdrawn` is a DISTINCT member, never
      aliased onto `terminated`.
- [ ] 8.2 [US4] `scripts/validate-consent-instruments.py`: `NEUTRAL_STATUSES`
      (`:129-130`) + `withdrawn` — the alias-target check adjudicates against
      this tuple, so omitting it would let a domain alias onto a status the
      schema accepts and the validator rejects; and `PAST_SIGNATURE_STATUSES`
      (`:133`) + `withdrawn` — an instrument can only be withdrawn after
      execution, so the lifecycle-skip discipline must reach it.
      *Depends on*: **0.2** — growing `NEUTRAL_STATUSES` NARROWS
      `alias-remaps-neutral-status` (`:348`), and 0.2 is what proves the
      narrowing fires nowhere.
      *Verification*: 8.6; the existing registries keep their verdicts.
- [ ] 8.3 [US4] `consent-instrument.schema.yaml` dependent-ref growth:
      `dependent_refs[].kind` enum (`:244`) + **`governed_identity`** as a
      NAMED member, never the `other` escape (FR-026); TWO new OPTIONAL sibling
      properties `identity_removal_evidence` and `admission_withdrawal_evidence`
      (`{type: string, minLength: 1}` each); and a `description` on `ref`
      stating the convention and the posture (**ruling A-5**) — for a
      `governed_identity` the `ref` names the roster FRAGMENT PATH plus the
      entry's `identity_ref`, and the validator does NOT resolve it: no
      fragment is opened, no entry existence is confirmed, no repository
      boundary is crossed. Same posture as FR-037's `evidence_ref`, same
      reason — these validators are network-free and read one repository.
      *Verification*: 8.5's positive declares a complete `ref`; a source-level
      check confirms no read of the fragment path.
- [ ] 8.4 [US4] `check_termination_cascade` (`:494-505`): the gate widens from
      `status != "terminated"` to `status not in ("terminated", "withdrawn")`.
      **State this as what it is — the REACH of
      `termination-without-cascade-evidence` widens to `withdrawn`
      instruments; the code SPELLING is retained for continuity** (ruling A-6;
      the claim that it is "unchanged in meaning" was false and is not
      restored). Add `identity-cascade-incomplete`, firing when a
      `governed_identity` dependent on a TERMINATED or WITHDRAWN instrument
      lacks either evidence field. The obligation lives in Python, not in a
      root-level `if/then` — the family's own precedent (the schema comment at
      `:256-259` already says the validator requires cascade evidence once
      terminated).
      *Verification*: 8.5's two negatives prove the obligation fires
      IDENTICALLY on both events.
- [ ] 8.5 [US4] Fixtures in `examples/consent-instrument/`: ONE positive (a
      `withdrawn` instrument with a `governed_identity` dependent carrying
      complete cascade evidence) and TWO negatives registered in
      `EXPECTED_NEGATIVE_FINDINGS` — credential-only evidence on `terminated`,
      and the same on `withdrawn`. US4 acceptance scenario 3's attribution rule
      (the finding lands against the INSTRUMENT, not the identity) is measured
      by the negative's finding naming the instrument path — it is the
      already-promoted attribution rule, not a new discovery mechanism, since
      this validator is standalone and reads one repo.
      *Verification*: `python3 scripts/validate-consent-instruments.py`
      self-test; SC-007.
- [ ] 8.6 [US4] The FR-030 regression for this family: the FIVE pre-existing
      positives and FIVE pre-existing negatives keep their VERDICTS and their
      FINDING CODES with the corpus grown — not merely that the run exits 0.
      This validator's self-test IS the suite; there is no `tests/` directory
      for the family, and the plan says so rather than implying a pytest suite
      exists.
      *Verification*: diff against 0.3's captured baseline, code by code
      (SC-007's "every existing instrument and fixture validates unchanged").

---

## Phase 9 — Cluster E: registration at `contract-v1.32`

**Depends on**: Phases 1, 3, 4, 7, 8 — every registered file's CONTENT must be
final before its `sha256` is computed. **Atomic**: one commit (constitution VI).

- [ ] 9.1 [US2] `contracts/manifest.yaml`: `contract_bundle_version:
      contract-v1.32`; a NEW row for the roster schema (ONE row, ONE `sha256`,
      ONE `consumption_rule` stating BOTH the declared placement AND that
      `validate-credential-contracts.py`'s skip-with-notice over that path is
      EXPECTED and blessed); REFRESHED rows for `consent-instrument` and
      `consent-instrument-class-registry` (new `sha256`, the
      `contract_schema_version` bump recorded in the `consumption_rule` prose);
      and a **FIRST** row for `xfactory-credential-contracts`, which has NO row
      today — FR-021's "refresh" is a first registration for that schema
      (research.md, "A registration gap FR-021 assumes away"). Rows follow the
      v1.31 (openxWallet) shape, closing sentence included. Note the trap: the
      per-row `schema_version` mirrors the RECORD envelope's const, not the
      schema file's `contract_schema_version`.
      *Verification*: 9.6.
- [ ] 9.2 [P] [US2] `contracts/CHANGELOG.md`: a `## contract-v1.32` entry
      classed **additive**, FOLDING IN the pending `## Unreleased` openxwallet
      item rather than leaving it beside, and stating the additivity argument
      explicitly — an OPTIONAL property and an ADDED enum member, so a domain
      repo on the same major version remains conformant without changes
      (`docs/contract-versioning-policy.md:130-132` is the test it is held to).
      *Verification*: the `## Unreleased` block is gone; doc-health reports no
      finding.
- [ ] 9.3 [P] [US2] `contracts/README.md`: registration rows for the roster
      schema, its validator and its examples; amended rows for the two consent
      schemas; a row for `xfactory-credential-contracts`.
      *Verification*: the registration table lists every file 9.1 registers.
- [ ] 9.4 [US2] Generate
      `contracts/releases/contract-v1.32.digests.yaml` with
      `python3 scripts/validate-contract-release.py build --tag contract-v1.32
      --output contracts/releases/contract-v1.32.digests.yaml`. Its membership
      is the Hermes-runtime release surface plus manifest/CHANGELOG/README and
      the versioning policy — **roster paths do NOT enter it and MUST NOT be
      hand-added**. It regenerates because the manifest and changelog digests
      change, not because roster files join (research.md, "Registration
      mechanics"; v1.30 and v1.31 have identical 190-entry membership).
      *Verification*: the release verifier over the realized commit; a diff
      showing only digest changes, no new paths.
- [ ] 9.5 **Root `README.md` — two edits, both completion conditions of this
      slice.** (a) The roster family added to the document index. (b) **The
      OpenSpec Records correction the progress handoff owes**: the block at
      `README.md:264-272` still reads "MODIFIES consent-instrument (cascade
      reaches identities) and doc-health (sixteenth family)" — it must name
      **FOUR** Modified Capabilities, adding `domain-conformance-checks`
      (Decision A, the pack grows to four checks) and `credential-contracts`
      (Decision B, the `issuance_preconditions` vocabulary), and naming
      Decisions A and B as the 2026-08-14 amendments that added them.
      *Verification*: the block enumerates four; doc-health reports no finding
      against README.
- [ ] 9.6 [US2] `python3 scripts/validate-manifest-digests.py` — every row's
      `sha256` recomputed against the file on disk and matched. This is the
      check FR-021's "digest verification passes" names, and it fails closed.
      *Verification*: exit 0 at `contract-v1.32`.

---

## Phase 10 — Traceability and the green bar

**Depends on**: all preceding phases.

- [ ] 10.1 Author `specs/007-client-identity-roster/traceability.yaml` — the
      006 shape (`specs/006-openxwallet-contracts` task 6.6), one row per
      RATIFIED REQUIREMENT and per SUCCESS CRITERION: `id`, `artifact` (the
      file that realizes it), `enforcing_check` (validator rule / test /
      command), `negative_confirmation` (the probe that proves the check is
      load-bearing, or an explicit `n/a` with a reason for the positive-only
      criteria), and `red_proven` (whether the check was observed to FAIL on
      its negative). The plan DEFERS this file to implementation precisely
      because `red_proven` needs RUNS — it cannot be authored at plan time.
      Rows: FR-001 … FR-039 and SC-001 … SC-014. The FR-022/SC-006 rows carry
      the ruling A-N2 residual note (task 5.3).
      *Verification*: a coverage check that every FR and SC id in spec.md has a
      row, and that no row's `red_proven` is left unset.
- [ ] 10.2 `OPENSPEC_TELEMETRY=0 openspec validate add-client-identity-roster
      --strict` **and** `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`,
      run from the `openxFactory/` root. 58/58 at `4de5bb2` — it must not
      regress.
      *Verification*: both exit 0; the `--all` count is ≥ 58.
- [ ] 10.3 The doc-health family green:
      `python3 scripts/doc-health.py --repo-root <aggregation checkout>` from
      the aggregation root — SIXTEEN families run, the new one REPORTS or SKIPS
      with an explicit reason, and NO new finding lands against this change or
      its documents (FR-025, SC-009). Plus `pytest tests/doc-health/` whole
      suite green against 0.3's baseline.
      *Verification*: the report renders a `client-identity-composition`
      section (which is why 6.4 adds the id to `FAMILY_IDS`).
- [ ] 10.4 **All validator self-tests green**, each compared against 0.3's
      captured baseline so "unaffected" is measured, not assumed:
      `python3 scripts/validate-client-identity-roster.py <fixture repo>`
      (clean on the conformant fixture, nonzero on each negative repo);
      `python3 scripts/validate-consent-instruments.py`;
      `python3 scripts/validate-credential-contracts.py .` and against the
      OpsxFactory checkout (7.4); `pytest tests/conformance-gate
      tests/doc-health tests/credential_contracts tests/client-identity-roster`;
      `python3 scripts/validate-manifest-digests.py`.
      *Verification*: every command exits 0; no pre-existing finding code
      changed or disappeared (FR-030, SC-010).
- [ ] 10.5 **The killed-flaw acceptance fixtures pass with ZERO findings** —
      the feature's own acceptance test, run as one measurement: the genuine
      per-unit pair, the genuine duty pair, the provider-forced multi-surface
      reader, and the `planned` entry, all clean, in the SAME run in which the
      alias-pair negative is refused (4.6, FR-017, FR-038, SC-002). If any
      finding lands against a genuine pair, the two flaws the cross-model
      review killed have regressed and the work stops.
      *Verification*: `pytest tests/client-identity-roster/ -k discrimination`
      plus the self-test's zero-finding verdict on both packaged fragments.
- [ ] 10.6 The boundary measurements: `git status --porcelain` over the
      AGGREGATION checkout shows no change under `xFactories/` (SC-012, FR-030);
      a confirmation that no credential was minted and no provider call made
      anywhere in the feature or its tests (FR-029); and the suite-wide
      hermeticity guard (`tests/hermeticity.py`) confirmed active, which makes
      a network reach a test FAILURE rather than a silent success (SC-011).
      *Verification*: clean porcelain under `xFactories/`; `pytest tests/`
      green with the guard registered.

---

## Requirement → task coverage

Every FR and SC in spec.md maps to at least one task. `traceability.yaml`
(10.1) is the machine-readable form; this table is the authoring check that
nothing was orphaned.

| Requirement | Tasks |
|---|---|
| FR-001 | 1.4, 1.5 |
| FR-002 | 1.6, 2.5 |
| FR-003 | 1.6, 2.5, 4.1 |
| FR-004 | 2.6, 4.4 |
| FR-005 | 1.2, 4.1 |
| FR-006 | 1.3, 2.4, 4.1 |
| FR-007 | 1.2, 2.3, 4.2 |
| FR-008 | 1.7, 2.6, 4.1 |
| FR-009 | 1.7, 2.6, 3.3, 4.1 |
| FR-010 | 1.7, 2.6, 4.1 |
| FR-011 | 2.9, 4.5 (fixture 4) |
| FR-012 | 1.8, 2.7, 4.1 |
| FR-013 | 1.7, 2.7, 3.4, 4.1 |
| FR-014 | 2.8, 4.1 |
| FR-015 | 2.1 |
| FR-016 | 4.1, 4.2, 4.3, 4.4, 4.5, 4.8, 6.5 |
| FR-017 | 3.2, 3.3, 3.4, 3.5, 4.6 |
| FR-018 | 2.2 |
| FR-019 | 3.1–3.6 |
| FR-020 | 1.10, 2.9, 9.1 |
| FR-021 | 9.1–9.6 |
| FR-022 | 2.10, 5.1, 5.3 |
| FR-023 | 6.1, 6.2, 6.3, 6.4, 6.6 |
| FR-024 | 6.2, 6.5, 6.6 |
| FR-025 | 6.4, 10.3 |
| FR-026 | 8.3, 8.4, 8.5 |
| FR-027 | 1.9 |
| FR-028 | 7.1, 7.2, 7.3 |
| FR-029 | 2.1, 0.1, 10.6 |
| FR-030 | 0.3, 5.1, 7.4, 8.6, 10.4, 10.6 |
| FR-031 | 1.2, 2.3 |
| FR-032 | 2.10, 4.7 |
| FR-033 | 1.6 |
| FR-034 | 1.2, 1.4, 2.3, 2.8, 4.2 |
| FR-035 | 1.9, 3.6, 4.3 |
| FR-036 | 2.9, 4.5 (fixture 5) |
| FR-037 | 1.6, 2.9, 8.3 |
| FR-038 | 2.4, 4.6 |
| FR-039 | 8.1, 8.2 |
| SC-001 | 4.1–4.4, 2.2, 10.4 |
| SC-002 | 3.3, 3.4, 3.5, 4.6, 10.5 |
| SC-003 | 3.2 |
| SC-004 | 1.5, 3.2 |
| SC-005 | 2.9, 4.5 (fixture 5) |
| SC-006 | 5.1, 6.7, 5.3 (residual) |
| SC-007 | 8.5, 8.6 |
| SC-008 | 7.2, 7.3 |
| SC-009 | 6.4, 6.6, 10.3 |
| SC-010 | 10.2, 10.3, 10.4, 9.6 |
| SC-011 | 2.1, 6.6, 10.6 |
| SC-012 | 7.4, 10.6 |
| SC-013 | 2.10, 4.7, 3.4 |
| SC-014 | 1.2, 4.2 |

---

## Dependencies and execution order

### Phase dependencies

- **Phase 0** — no dependencies. 0.1 HARD-GATES Phase 3; 0.2 gates 8.2;
  0.3 is the baseline 10.4 and 8.6 compare against.
- **Phase 1 (Cluster A)** — foundational. BLOCKS Phases 2, 3, 4, 6.
- **Phase 2 (Cluster B)** — depends on 1. Blocks 4's repo fixtures and Phase 5.
- **Phase 3 (Cluster D)** — depends on **0.1** and 1. Blocks 4's positives and
  2.2's self-test corpus.
- **Phase 4 (Cluster C)** — depends on 1, 2, 3. Blocks Phase 5.
- **Phase 5 (Cluster F)** — depends on 2, 4.
- **Phase 6 (Cluster G)** — depends on 1. Independent of 2–5.
- **Phase 7 (Cluster H)** — independent. Blocks Phase 9.
- **Phase 8 (Cluster I)** — depends on 0.2. Blocks Phase 9.
- **Phase 9 (Cluster E)** — depends on 1, 3, 4, 7, 8 (content final before
  digests). Atomic, one commit.
- **Phase 10** — depends on everything.

### Parallel opportunities

- 0.2 and 0.3 run alongside 0.1 (0.1 is the only gate).
- Once Phase 1 lands, **Phases 6, 7 and 8 can run in parallel with the
  2 → 3 → 4 → 5 chain** — they touch disjoint files (`scripts/doc_health/`,
  the credential family, the consent family) and no shared registry until
  Phase 9.
- Within Phase 3, 3.5 and 3.6 are `[P]` (different files from 3.2–3.4).
- Within Phase 4, 4.2, 4.3, 4.4 and 4.7 are `[P]` (different files).
- Within Phase 6, 6.2 and 6.3 are `[P]` (different finding classes, same module
  — parallel only if authored as separate functions first).
- Within Phase 9, 9.2 and 9.3 are `[P]`; 9.1 → 9.4 → 9.6 is sequential.

### The two STOP conditions

1. **0.1 finds no citable provider fact** → STOP AND ESCALATE. Phase 3 cannot
   start; 3.3 cannot be softened; the corpus cannot be built around a
   synthesized fact.
2. **10.5 finds ANY finding against a genuine per-unit or duty pair** → STOP.
   That is a regression of the two flaws the cross-model review killed, and it
   is the acceptance test the seed handoff states in those terms.

---

## Notes

- `[P]` = different files, no dependency between them.
- Commit after each phase or logical group, with EXPLICIT pathspecs — this is a
  shared checkout and a bare `git commit` takes whatever any session has staged.
- The four MODIFIED capabilities' EXISTING suites must stay green AND unmodified
  in behaviour (FR-030); 0.3's baseline is what makes that measurable rather
  than assertable.
- Promoted spec text is NOT edited by this feature —
  `openspec/specs/doc-health/spec.md`,
  `openspec/specs/domain-conformance-checks/spec.md` and
  `openspec/specs/consent-instrument/spec.md` are all rewritten by the OpenSpec
  archive step (FR-025 and its extension, plan decision 15).
- `Status: record` files under
  `openspec/changes/add-client-identity-roster/review/` are never edited or
  appended; any amendment lands as a sibling record file.
