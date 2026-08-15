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

**Status markers.** `[ ]` not started; `[x]` done AND its verification has
actually run; `[~]` **the work is AUTHORED and its own inline checks pass, but
the verification this task names lives in a later phase** (see "Verification
timing" below) — so it is not yet `[x]`, and it is not `[ ]` either, because
claiming it unstarted would send a later reader to rewrite finished work. A
`[~]` task is closed out by the phase that supplies its verification. `[~]` is
also used for a task RELOCATED elsewhere, which says so in its body and names
the task that now owns the work.

Every task below names its TARGET FILES and its VERIFICATION — the validator,
suite, or command whose result proves the task done. A task with no runnable
verification is not done, it is asserted.

**Verification timing.** A task's WORK and its VERIFICATION may land in
different phases: where a *Verification* line names an artifact a LATER task
creates (2.2's self-test needs Phase 3's and Phase 4's corpus; 1.5's field-list
assertion lives in the module created at 4.5), the work is authored in its own
phase and the task is not checked `[x]` until its verification has actually
run. This is not a dependency cycle — code precedes fixtures, verification
follows both — but it is the reason a phase header's "Depends on" line and a
task's verification can point in opposite directions.

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

- [x] 0.1 **[HARD GATE on Phase 3]** Verify the multi-surface reader's citable
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
      **EXECUTED 2026-08-15 — the precondition FAILED and the escalation is
      RULED. Phase 3 is unblocked by the ruling, not by a citation.** Both
      clauses were falsified: no permission or directory role reaching BOTH
      surfaces is citable anywhere in the estate (seven candidates refuted),
      Business Central offers NO read-only path at all
      (`OpsxFactory:openspec/specs/business-central-administration/spec.md:93-101`),
      and Exchange offers a surface-scoped read-only path that falsifies the
      second clause outright
      (`openspec/specs/exchange-administration/spec.md:46-56`, live-verified
      with an attempted-overreach proof). Disposition chain:
      `a16-escalation-ruling-2026-08-15.md` (architect) → its item-5 obligation
      fired on ratified packet task 2.3 → **Decision C (Brett, 2026-08-15):
      RELOCATE TO FIXTURE**, packet amended in place at task 2.3 with the
      sibling record
      `openspec/changes/add-client-identity-roster/review/amendment-record-2026-08-15b.md`.
      Full account: research.md Decision 8's dated sub-section. Consequence for
      this list: 3.3 is RELOCATED to Phase 4 as task 4.9, Phase 3 packages
      THREE cases, and no packaged example asserts an uncitable provider fact.
- [x] 0.2 [P] Re-confirm the ruling A-7 precondition: no consent class registry
      anywhere in the reachable estate aliases a key spelled `withdrawn`.
      *Files*: read-only sweep of every `status_aliases` block
      (`examples/consent-instrument/`, `contracts/schemas/`, and any
      `xFactories/*/` registry reachable from the aggregation checkout).
      *Verification*: `grep -rn "status_aliases" -A6` over the estate returns no
      `withdrawn` KEY; record the sweep date AND ITS REACH in `research.md`
      Decision 5 — the domain registries are visible only through the
      aggregation checkout 0.3 confirms, and a sweep that could not see them is
      recorded as a NARROWED sweep, never reported as a clean estate sweep.
      On a hit, STOP — growing `NEUTRAL_STATUSES` would change an existing
      registry's verdict and breach FR-030.
      **SWEPT 2026-08-15 — CLEAN, and FULL-ESTATE in reach, not narrowed.** The
      aggregation checkout resolved (0.3), so the domain registries were
      visible. Exactly four files in the whole estate declare `status_aliases`;
      the ONLY alias KEY declared anywhere is `active` (→ `executed`), in
      `xFactories/LedgerxFactory/conformance/consent-instrument-classes.yaml`
      and openxFactory's packaged example. No `withdrawn` key exists. Recorded
      with the per-file table in `research.md` Decision 5. 8.2 is clear.
- [x] 0.3 [P] Capture the green-before baseline for the four MODIFIED
      capabilities, so "unmodified in behaviour" (FR-030) is measured and not
      assumed. Record verdicts AND finding codes, not just exit codes.
      *Commands*: `python3 scripts/validate-consent-instruments.py` (5
      positives, 5 registered negatives, 2 purpose probes);
      `python3 scripts/validate-credential-contracts.py .` (2 positives, 3
      registered negatives); `pytest tests/credential_contracts/`;
      `pytest tests/doc-health/`; `pytest tests/conformance-gate/`.
      *Where the baseline is written*: OUTSIDE the tracked tree — the session
      scratchpad, path recorded in this task — NEVER inside
      `specs/007-client-identity-roster/`, because every commit in this lane
      stages that directory as a pathspec and an "uncommitted" note there is
      committed by the next commit. 8.6 and 10.4 diff against it.
      ALSO establish, in the same task, that the two EXTERNAL trees the later
      measurements need are reachable: an aggregation checkout (10.3's
      `doc-health.py --repo-root`, 10.6's `git status --porcelain` over
      `xFactories/`) and an OpsxFactory checkout (7.4's live-record
      regression, the one result that would falsify the additivity claim).
      On absence, STOP AND ESCALATE — those three measurements cannot be
      synthesized and must not be quietly skipped.
      *Verification*: the baseline file exists at the recorded scratch path and
      is re-compared at 10.4; both external checkouts resolve, or the
      escalation is ruled.
      **CAPTURED 2026-08-15, before any edit to any MODIFIED capability's
      surface. THE RECORDED PATH — 8.6 and 10.4 diff against this:**
      `/tmp/claude-1000/-home-brett-projects-xFactory-xFactories-OpsxFactory/af342a91-d20e-4518-ae91-43c3ec1e3ccd/scratchpad/007-baseline/BASELINE.md`
      (raw run transcripts are its siblings in that directory). All five
      commands exit 0 and EVERY finding-code register is empty — no validator
      emits any `ERROR [code]` or `WARN [code]` line at baseline. Composition:
      consent self-test 5 positives / 5 negatives / 2 purpose probes;
      credential-contracts self-test 2 positives + 3 negatives, `0 contract(s)
      checked, 0 skipped, 0 error(s) -> PASS`; `tests/credential_contracts/` 2
      passed; `tests/doc-health/` 621 passed + 7 skipped (628); and
      `tests/conformance-gate/` 13 passed + 2 skipped — **15 tests, the number
      5.1 must preserve unmodified**. BOTH external checkouts resolve: the
      aggregation checkout at `/home/brett/projects/xFactory` (HEAD `dac0a55`,
      every submodule populated) and the OpsxFactory checkout at
      `/home/brett/projects/xFactory/xFactories/OpsxFactory` (the two live
      `issuance_preconditions` records confirmed at
      `credentials/requirements.yaml:232-234,263-265`, both values `true`, so
      Decision 3's `const: true` narrowing breaks no live record). No
      escalation on this half. CAUTION for 10.3/10.6: the aggregation checkout
      is SHARED with other sessions, so its porcelain reading must account for
      foreign uncommitted work, and per gate ruling G8's rider the doc-health
      merge phase must never be run there.

**Checkpoint**, stated as what each precondition actually gates: 0.1 ruled
before **Phase 3** begins; 0.2 clean before **8.2**; 0.3 captured before the
FIRST edit to any of the four MODIFIED capabilities' surfaces (**Phases 5, 6, 7
and 8**), because it is the before-state 8.6 and 10.4 diff against and it
cannot be captured after the edit. None of the three gates Phase 1, which
creates a new file and touches no existing capability — but 0.3 is not
"advisory" either: skipping it makes FR-030's "unmodified in behaviour"
unmeasurable rather than merely unrecorded.

---

## Phase 1 — Cluster A: the roster schema family

**Blocks**: Phases 2, 3, 4, 6. **Depends on**: nothing — this phase creates a
new file and touches no existing capability, so no Phase 0 precondition gates
it (0.1 gates Phase 3, 0.2 gates 8.2, and 0.3 must precede the first edit in
Phases 5–8; see the Phase 0 checkpoint).

*Target file (all of Phase 1)*:
`contracts/schemas/xfactory-client-identity-roster.schema.yaml`.

- [x] 1.1 [US1] Schema skeleton: Draft 2020-12 with `$schema` and `$id`,
      `contract_schema_version: 1`, a top-level `oneOf` over the two kinds,
      `additionalProperties: false` on EVERY object at every depth. **Both
      kinds declare `schema_version: const: 1`** (ruling A-2) so the single
      manifest row is unambiguous.
      *Verification*: `python3 -c "import yaml,jsonschema;
      jsonschema.Draft202012Validator.check_schema(yaml.safe_load(open(...)))"`
      passes; a grep confirms no object lacks `additionalProperties: false`.
- [~] 1.2 [US1] The six CLOSED vocabularies as `$defs`, each enumerated
      explicitly and each carrying a `description` naming its extension route
      (FR-007, FR-031, FR-034). **Each `admission_surface` MEMBER's description
      additionally names the admission act and the scoping mechanism that make
      it a surface** — FR-007's second clause and packet task 2.2 verbatim; for
      `business_central` that is BOTH acts (the per-environment application
      user, scoped by environment; the admin-center Entra-app authorization,
      no scope selector), for `exchange` its own act and mechanism. A surface
      description may not assert a provider fact the builder cannot cite
      (research.md Decision 8): an uncitable `exchange` act or mechanism
      ESCALATES by 0.1's route, it is not invented. The `authority_class`
      description names FR-005's conformant expression (destructive capability
      rides the `mutate` entry's achieved class and gate obligation) so 2.3's
      refusal can cite the route. Vocabularies: `admission_surface`
      (`business_central`, `exchange`), `authority_class`
      (`observe`, `mutate` — destructive UNREPRESENTABLE, FR-005),
      `residency_model` (`client_tenant_single`, `vendor_tenant_multi`),
      `enforcement_mode` (`provider_enforced`, `logic_enforced`),
      `lifecycle_state` (`planned`, `enrolled`, `retired`), and `identity_kind`
      (`entra_app_registration`, ONE member, research.md Decision 1). Plus
      `$defs.free_token` — pattern `^[a-z0-9][a-z0-9_-]*$` — for
      `blast_radius_unit` and `duty`.
      *Verification*: ONE negative per closed set — the FIVE vocabulary
      negatives of 4.2 plus `destructive-authority-class.yaml` in 4.1 (the
      authority-class set's refusal, which sits in 4.1 because FR-016 names
      it), six in total — each refused (SC-014).
- [~] 1.3 [US1] `$defs.identity_key` — the five-element uniqueness tuple,
      **element 3 = `authority_class_intended`** (ruling R-N1), defined ONCE
      and referenced by both the uniqueness rule and the drift record. The
      `description` states the choice and its reason: a key must be declarative
      and stable, and the achieved class is observational and moves with
      provider state.
      *Files*: also the schema description of kind 2 (task 1.9).
      *Verification*: 2.4's uniqueness rule reads element 3 from
      `authority_class_intended`; 4.1's `full-tuple-duplicate.yaml` is refused
      naming all five elements (FR-006).
- [~] 1.4 [US1] Kind 1 `xfactory_client_identity_roster` top level:
      `schema_version`, `kind`, `client_ref`, **`client_tenant`**, `domain`,
      `legend`, `entries[]`
      (`minItems: 1`). **`client_tenant` (gate ruling G2)** is a REQUIRED
      string carrying the PROVIDER TENANT IDENTIFIER of the client this
      fragment covers, in the same dialect as `home_tenant` and the members of
      `principal_locations[]`; its `description` says so and says why it is
      declared rather than derived — `client_ref` is a governance slug, so
      without this field the `client_tenant_single` rule (2.7) has nothing to
      compare `home_tenant` against, and the inference alternative
      (`home_tenant ∈ principal_locations[]`) cannot catch an identity homed
      in the WRONG client's tenant. It sits on the FRAGMENT because a fragment
      is per (client, domain). `legend` is
      `{blast_radius_units: {<token>: <provider id>}, duties: {…}}` — a MAPPING,
      so "declared twice for the same key" is unrepresentable at the schema
      level and the checkable duplicate (FR-034) is a token in BOTH maps
      (2.8). A legend entry no entry uses is NOT a finding in this release —
      no requirement makes it one and it would fire on a conformant `retired`
      or `planned` entry's fragment.
      *Verification*: 3.2/3.5 fragments validate; 4.2's legend negatives refused.
- [~] 1.5 [US1] The entry object — the FR-001 field list UNREDUCED:
      `identity_ref` (string), `identity_kind`, `home_tenant`,
      `principal_locations[]`, `residency_model`, `admission_surface`, `duty`,
      `blast_radius_unit`, `authority_class_intended`,
      `authority_class_achieved`, `granted_permissions[]` (`minItems: 1`; each
      member an OBJECT — `id` the provider-native identifier VERBATIM,
      `achieves` (`observe|mutate`), `reaches[]` (admission-surface members) —
      because FR-004's "checkable against" and FR-009's "naming the surface and
      the permission that reaches it" are otherwise decidable only by a
      provider catalogue the validator may not call or by inferring provider
      semantics from a string, and spec.md's Assumptions block already puts the
      mapping IN THE RECORD), `admission[]`, `declared_excess` (optional),
      `per_unit_principal_available` (a MAPPING admission-surface member →
      boolean, covering the entry's surface and every `spanned_surfaces[]`
      member — FR-008 is per-surface and the multi-surface reader needs one
      answer per surface), `lifecycle_state`,
      `standing_credential_attestation`, `ratified_by` (domain-qualified),
      `consent_ref` — plus the OPTIONAL `duty_separation_rationale` (string),
      the declaration FR-038's alias rule reads and the second addition ruling
      R7 makes to the ratified list (the legend at 1.4 is the first). Without
      it 2.4 cannot implement its third predicate and 3.5 cannot author its
      genuine duty pair. **Plus the OPTIONAL `provider_object_ref` (string,
      gate ruling G4)** — the provider-native OBJECT identifier (an Entra
      `app_id`; the BC identity evidence record already carries one), which is
      the second disjunct of the cross-domain `shared-identity-material` rule
      (6.2). Its `description` states that it is an OBJECT identifier and NOT
      a tenant identifier, the distinction the whole rule turns on: read
      against `principal_locations[]` (tenants) the disjunct would intersect
      on the shared client tenant and refuse FR-024's ratified non-finding.
      *Verification* (the assertion's module is created at 4.5; see
      "Verification timing"): a field-list assertion in
      `tests/client-identity-roster/test_client_identity_roster.py` compares the
      entry's declared properties against FR-001's list — so a later refactor
      cannot quietly drop `granted_permissions[]` or `admission[]` (SC-004).
- [~] 1.6 [US1] `admission[]` — `type: array, minItems: 1` (**not 2**; a
      one-member array is a legal single-act expression, ruling A-N3), whose
      members carry `surface`, `act`, `achieved_scope` (provider-native),
      `enforcement_mode`, `evidence_ref`, `verified_at`, and
      **`exceeds_governed_unit`** (boolean, REQUIRED). `evidence_ref` is a
      DECLARED POINTER object `{repo, path, sha?}` (FR-037) with a description
      stating that no validator resolves it. **`evidence_ref` and `verified_at`
      are a PAIR, expressed as `dependentRequired` in BOTH directions**: both
      present is a VERIFIED act, both absent is the UNVERIFIED state FR-003
      requires to stay representable, and a `verified_at` with no
      `evidence_ref` is refused (2.5). `verified_at` carries NO maximum age
      (FR-033 — no decay in this release, and reworded by the checklist pass to
      "every VERIFIED act", because requiring it on every act made the
      unverified state unrepresentable); an act with
      no `evidence_ref` is unverified BY DERIVATION, never by an independent
      `verified: false` field an author could contradict (FR-003).
      `exceeds_governed_unit` declares whether the scope that act achieves
      reaches BEYOND the entry's `blast_radius_unit` — a DECLARED fact, not an
      inferred one, because `achieved_scope` is provider-native and opaque
      (ruling R7) so the neutral layer may compare scope tokens for equality
      but must never read breadth out of one. It is what makes the change's own
      motivating measurement checkable (2.5) instead of merely expressible;
      without it a tenant-wide no-selector act with no `declared_excess` passes
      every rule in the corpus. Its description says exactly that.
      *Verification*: 4.1's `unverified-act-counted-as-access.yaml`,
      `scope-exceeds-unit-undeclared.yaml` and `evidence-ref-malformed.yaml`
      refused; 3.2's two-act case validates with the excess declared.
- [~] 1.7 [US1] `declared_excess` (optional object: `spanned_surfaces[]`,
      `provider_reason`, `bound_mechanism`, `gate_obligation`,
      `enforcement_test_ref`), `per_unit_principal_available` (the per-surface
      MAPPING declared at 1.5 — admission-surface member → boolean, never a
      single boolean; the schema closes its KEY SPACE to the enum, while the
      COVERAGE rule — a key for the entry's surface and for every
      `spanned_surfaces[]` member — is 2.6's, because a key set that depends on
      another field's value is not expressible here),
      `standing_credential_attestation` — the claim
      (`no_standing_credential`, boolean), the approved GRANT-WINDOW REFERENCE
      the claim is made against, and the evidence pointer, so FR-013's
      falsification is a RECORD-INTERNAL contradiction the network-free
      validator can see (2.7) rather than an observation of a credential store
      it must never make (FR-029) — FR-008, FR-009, FR-010, FR-013.
      *Verification*: 4.1's `missing-enforcement-test.yaml`,
      `provider-enforced-without-per-unit-principal.yaml`,
      `per-unit-principal-available-but-logical.yaml`,
      `false-standing-credential-attestation.yaml` each refused for its own code.
- [~] 1.8 [US1] The `vendor_tenant_multi` obligations as an `if/then` on
      `residency_model` IN THE SCHEMA (not only in the validator), so a
      validator refactor cannot lose them: tenant allow-list enforced at token
      validation, per-client authorization state, per-client revocation
      evidence, the cross-client credential-span statement, the per-client
      consent amendment (FR-012). Residency branches on NOTHING else — in
      particular on no `authority_class_*` (ratified constraint 1).
      *Verification*: 4.1's `vendor-tenant-multi-missing-obligations.yaml`
      refused; a grep asserting no `authority_class` appears inside any
      residency branch (constraint 1's mechanized form).
- [~] 1.9 [US6] Kind 2 `xfactory_client_identity_drift_finding`:
      `schema_version`, `kind`, `identity_ref` (the `$defs.identity_key`
      OBJECT — deliberately a different shape from the entry's STRING
      `identity_ref`, FR-035, documented in the description), `fragment_ref`,
      `rule_id`, `roster_value` and `observed_value` (BOTH required — the
      ratified delta scenario), `observed_at`, `opened_at`, `status`
      (`open|resolved|disposed` — a CLOSED set, refused outside it like every
      other, whose negative is 4.3's third file), and `disposition_ref`
      (OPTIONAL, made REQUIRED by an `if status == disposed / then` branch: a
      disposed finding with no citation is the unfalsifiable disposal this
      record exists to prevent, and an `open` finding cannot have one).
      The description states:
      (a) why the two `identity_ref` shapes differ; (b) that the tuple's third
      element is the INTENDED class so the join survives drift (R-N1); (c) that
      the record claims no alignment with and no storage in any doc-health
      findings register, because none exists; (d) that recording a finding
      mutates nothing (FR-027).
      *Verification*: 3.6's example validates; 4.3's two negatives refused.
- [~] 1.10 [US2] Declare the PLACEMENT in the schema description:
      `credentials/client-identity-roster/<client_ref>.yaml`, one file per
      (client, domain), and note that
      `scripts/validate-credential-contracts.py`'s skip-with-notice over that
      path is EXPECTED and blessed (FR-020). The drift kind carries no
      placement rule in this release (research.md Decision 2's consequence).
      *Verification*: the manifest `consumption_rule` at 9.1 states the same two
      facts; 2.9's sweep enforces the placement.

**Checkpoint**: the schema validates as a schema and both kinds are
expressible → Phases 2, 3, 6 may begin.

**REACHED 2026-08-15.** `contracts/schemas/xfactory-client-identity-roster.schema.yaml`
passes `Draft202012Validator.check_schema`; 19 `$defs`; 11 objects closed with
`additionalProperties: false`, the 3 MAP-shaped properties closed via
`propertyNames` (the only closure a map admits), 0 objects left open, and the
ROOT closed with `unevaluatedProperties: false` — the Draft 2020-12 form that
accounts for the matched `oneOf` branch, since a root `additionalProperties:
false` beside a branching `oneOf` refuses every instance. **30/30 expressibility
probes behaved as expected**: both kinds validate; all SEVEN closed sets refuse
an out-of-vocabulary value; the `evidence_ref`/`verified_at` pair refuses a
claimed-but-unevidenced verification while leaving the unverified state
representable; a one-member `admission[]` validates (A-N3); `vendor_tenant_multi`
refuses without its five obligations and passes with them; a `disposed` drift
finding refuses without `disposition_ref` and an `open` one passes without it;
and the multi-surface spanned-surfaces shape 4.9 needs validates.
Constraint 1 is mechanized and green: no `authority_class` appears anywhere
inside the residency `if/then` branch. Tasks 1.2–1.10 are `[~]` rather than
`[x]` because each names a verification that lives in Phase 3 or 4 (a
registered negative, a packaged fragment, or 4.5's assertion module); the WORK
is authored and its inline checks pass.

---

## Phase 2 — Cluster B: the canonical validator

**Depends on**: Phase 1. **Blocks**: Phase 4's repo fixtures, Phase 5.
**Verification timing**: the CODE of this phase depends on Phase 1 only, but
2.2's verification reads the corpus Phases 3 and 4 author (see "Verification
timing" in Format) — 2.2 is authored here and checked `[x]` after 4.4.

*Target file (all of Phase 2)*: `scripts/validate-client-identity-roster.py`.

- [x] 2.1 Module skeleton following the sibling `validate-*.py` contract
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
- [~] 2.2 The self-test layer (FR-018): positives validate clean; each negative
      must raise its REGISTERED code, with an optional pinned detail substring
      where the code alone would be satisfied by a generic `schema` finding —
      the consent validator's two-part expectations table. FIVE failure modes
      are themselves errors: a registered probe with no file, a file with no
      registration, a negative that passes, a negative that fails for the WRONG
      code, and a negative whose code fires without the pinned detail.
      **Record-internal rules RUN even when the schema already refuses the
      document, and each raises its own kebab code** (checklist pass): most of
      this corpus's negatives are schema-visible, and a raw `jsonschema`
      message names neither the closed vocabulary nor the extension route that
      2.3, FR-007, FR-034 and SC-014 require, so a validator that returned at
      the first schema failure would leave those refusals existing nowhere and
      make their expectations-table entries unregisterable — the roster-side
      form of the `_semantic_findings`-only fact behind ruling A-3a. Rules read
      the loaded mapping defensively (a missing or wrong-typed field is skipped
      by the rule that would read it, never crashed on).
      *Verification* (runs after Phase 4 — this task's corpus is authored at
      3.2–3.6 and 4.1–4.4): temporarily break one negative each way and confirm
      five distinct self-test failures; SC-001. Plus one assertion that a
      schema-invalid negative still raises its NAMED code, not only a generic
      `schema` finding.
- [~] 2.3 Record-internal rules, group 1 — closed-vocabulary and shape
      refusals, each naming the closed set and the extension route in its
      message (FR-005, FR-007, FR-031, FR-034, SC-014).
      *Verification*: 4.2's five vocabulary negatives plus 4.1's
      `destructive-authority-class.yaml` — one per closed set, six in total.
- [~] 2.4 [US1] Uniqueness and the alias rule — the feature's sharpest pair.
      Uniqueness: entries sharing the whole `$defs.identity_key` tuple are a
      finding NAMING EVERY ELEMENT; entries differing in ANY element validate
      clean (FR-006). **Both rules compare entries WITHIN ONE FRAGMENT, never
      across fragments** (checklist pass): the tuple carries no `client_ref`
      and the legend binds free tokens per fragment, so pooling a repo's
      fragments would report a domain's two clients' `sandbox1` identities as
      one duplicate — the per-unit flaw re-killed from the other direction.
      4.5's fixture 1 measures the scope. The alias rule (FR-038) is a
      THREE-predicate conjunction
      and no broader: two entries differ SOLELY in free tokens — one or BOTH,
      since a domain that could evade the rule by inventing two spellings
      instead of one would leave it bounding nothing, and the wider reading
      cannot touch a genuine pair — AND are
      observationally identical (the same `granted_permissions[]` set, compared
      as normalized member tuples `(id, achieves, sorted(reaches))` now that
      members are objects, and the same admission acts by
      `(surface, act, achieved_scope, enforcement_mode)` — exactly the four
      ratified elements, with `exceeds_governed_unit` deliberately NOT among
      them),
      AND declare no `duty_separation_rationale` (the optional entry field
      declared at 1.5 — the predicate reads that field and nothing else). A
      pair differing in `achieved_scope`, in permissions, or carrying the
      rationale validates clean.
      *Verification*: 4.6's single-run discrimination — the genuine per-unit
      pair and genuine duty pair at ZERO findings while the alias pair is
      refused (SC-002). A rule broad enough to catch all three fails.
- [~] 2.5 [US1] Admission verification, effective reach, and the scope-excess
      rule (FR-002, FR-003, FR-010): an act with no `evidence_ref` is unverified
      and EXCLUDED from effective reach; **an act carrying `verified_at` with
      NO `evidence_ref` is REFUSED as `unverified-act-counted-as-access`,
      naming the act** — the record claiming a verification it cannot evidence,
      which is the refusal predicate that FR-016 negative lacked before the
      checklist pass (exclusion is a behaviour, not a refusal, so the fixture
      would have passed); provider consent with no admission act
      is refused stating that consent is not admission. Effective reach is
      COMPUTED, never declared, and CONCRETELY: the set of
      `(surface, achieved_scope)` pairs over VERIFIED acts only, plus the
      derived flag `exceeds_governed_unit = OR` over those acts — emitted as a
      per-entry NOTE, because FR-003 and US1 scenario 2 require the union to be
      REPORTED and a union of opaque tokens is otherwise an unimplemented word.
      That OR is the ratified "the union, NOT the narrower act". **The rule
      that fires**: a VERIFIED act declaring `exceeds_governed_unit: true`
      REQUIRES a `declared_excess` with its four fields; absent one,
      `undeclared-scope-excess` names the act, its `achieved_scope`, and the
      governed `blast_radius_unit`. This is the change's motivating measurement
      — a no-selector act silently converting a provider-enforced bound into a
      gate-logic one — and before this rule nothing in the corpus caught it
      (FR-009 checks surfaces, FR-010 checked class only, and FR-008's
      per-surface rule is satisfied by the OTHER act's use of the per-unit
      principal).
      *Verification*: 4.1's `consent-recorded-as-access.yaml`,
      `unverified-act-counted-as-access.yaml` and
      `scope-exceeds-unit-undeclared.yaml`; 3.2's union reach and its DECLARED
      excess are the discrimination partner of the last of those.
- [~] 2.6 [US1] Authority, all of it RECORD-INTERNAL against the declarations
      1.5 puts in `granted_permissions[]` — no provider catalogue, no inference
      from an identifier's spelling: `authority_class_achieved` must equal the
      MAXIMUM declared `achieves` (`mutate` dominates `observe`), and any other
      value is the contradiction 4.4's negative encodes (FR-004);
      achieved-above-intended with no `declared_excess` refused (FR-010); every
      member of a permission's `reaches[]` must be the entry's own
      `admission_surface` or a declared `spanned_surfaces[]` member, and
      anything else is undeclared reach refused NAMING the surface and the
      permission `id` that reaches it (FR-009); a NAME describing narrower
      authority than it achieves refused — the check reads `identity_ref` (the
      ratified record has no `purpose` field), fires only when an
      observation-suggesting token appears while `authority_class_achieved` is
      `mutate`, matches a SMALL CLOSED token list declared in the module
      (`observer`, `observe`, `reader`, `read`, `readonly`, `viewer`, `audit`,
      case-insensitive, word-boundary) and NAMES the token it matched (FR-010).
      **THREE conjuncts, not two (gate ruling G6): token AND
      `authority_class_achieved: mutate` AND NO `declared_excess` covering the
      class overshoot** — "covering" = PRESENT, since `declared_excess` is a
      single object (a future per-excess split re-keys this to the
      class-overshoot member). The third conjunct is the CURE US1 acceptance
      scenario 4 ratifies; without it this rule fires on 3.2's Business
      Central positive, which 3.2, 4.6 and 10.5 all require to be clean. The
      residual is deliberate: intended = achieved = `mutate` leaves no excess
      to declare, so the finding stands and the identity must be renamed.
      **ACT-SIDE reach** (checklist pass, FR-009): every `admission[].surface`
      must be the entry's own `admission_surface` or a declared
      `spanned_surfaces[]` member, and anything else is `undeclared-act-surface`
      naming the act and the surface — the permission-side rule cannot see an
      act performed on a surface no permission declares, yet an admission act
      IS the second key that makes a surface reachable (this change's own
      measured finding), and the cross-domain family already reads acts this
      way (6.3), so without it the BLOCKING check is weaker than the REPORTING
      one on identical evidence.
      Structural scoping:
      provider-enforced claimed where no per-unit principal exists is a
      finding; an available per-unit principal left unused while logical
      enforcement is declared is a finding NAMING the available principal; and
      **"LEFT UNUSED" IS PER-SURFACE, NOT PER-ACT — measured 2026-08-15, and
      the distinction is load-bearing.** A per-ACT reading (any
      `logic_enforced` act at a surface whose mapping says `true`) FIRES ON
      3.2's mandated Business Central positive, which 3.2, 4.6 and 10.5 all
      require to validate with ZERO findings: that entry's per-environment
      application user USES the available principal, while its admin-center act
      CANNOT, having no scope selector at all. The ratified scenario is "a
      surface that DOES offer such a principal while the entry declares logical
      enforcement INSTEAD" — instead of USING it. So the predicate is: at a
      surface whose mapping declares `true`, NO act on that surface is
      `provider_enforced`. An act that cannot use the principal is conformant
      beside a sibling act that does. The FALSE-CLAIM rule
      (`provider-enforced-without-per-unit-principal`) stays PER-ACT, because
      an act claiming an enforcement its surface cannot supply is that act
      lying whatever its siblings do. 4.1's
      `per-unit-principal-available-but-logical.yaml` must therefore declare
      logical enforcement on EVERY act at the surface, or it will not fire.
      **a surface the entry touches with NO key in
      `per_unit_principal_available` is `per-unit-principal-undeclared` naming
      that surface** (checklist pass — 1.7 states the coverage obligation and
      nothing fired on it; an absent key and a `false` answer are otherwise
      indistinguishable). A key for a surface the entry does NOT touch is not a
      finding: the key space is already closed by the enum (FR-008).
      The rules must NOT invalidate a deliberately narrow identity
      because the provider's granularity is coarser than the axis (FR-009).
      *Verification*: 4.1 and 4.4's negatives — including
      `undeclared-act-surface.yaml` and `per-unit-principal-undeclared.yaml`;
      4.9's multi-surface representability fixture
      validates clean, which is the "must not invalidate" half and the
      discrimination partner of both new negatives (its acts sit on declared
      surfaces and its mapping answers both). It is a FIXTURE rather than
      3.3's packaged entry by Decision C (2026-08-15); the discrimination it
      performs is unchanged.
- [~] 2.7 [US1] Residency (FR-012) and lifecycle/attestation (FR-013): a
      registration homed outside the client tenant may not declare
      client-resident — **the predicate, against 1.4's DECLARED comparand
      (gate ruling G2): under `residency_model: client_tenant_single`,
      `home_tenant == fragment.client_tenant` AND every
      `principal_locations[]` member `== fragment.client_tenant`, with the
      finding NAMING `home_tenant`. Never a containment reading
      (`home_tenant ∈ principal_locations[]`), which passes an identity homed
      in the WRONG client's tenant — the case the rule exists to refuse**;
      `vendor_tenant_multi` requires its five obligations; a
      `planned` entry validates and is NEVER reported as missing or incomplete;
      a retired entry retains its record; a credential held outside an approved
      grant window makes the attestation false and is reported against that
      entry — raised on the RECORD-INTERNAL contradiction 1.7 makes expressible
      (a `no_standing_credential` claim against a declared held credential, or
      against an expired or absent grant-window reference). NO credential
      store, grant record or provider is consulted (FR-029).
      *Verification*: 4.1's `vendor-homed-declared-client-resident.yaml`,
      `vendor-tenant-multi-missing-obligations.yaml`,
      `false-standing-credential-attestation.yaml`; 3.4's `planned` positive.
- [~] 2.8 [US1] Both roots and the legend — the RECORD-INTERNAL half (the
      resolution half is 2.9): an entry naming a capability and no consent
      instrument is invalid, stating that consent — not our own ratification —
      authorizes standing in another party's tenant; a `mutate` entry naming no
      ratified capability is an ERROR that fails the gate, not a report
      (FR-014). Legend: EXACTLY the two findings FR-034 names — a free
      token used with no legend entry, and a token declared twice (i.e.
      appearing in BOTH legend maps). No third legend rule: an unused legend
      entry is not a finding, because no requirement makes it one and a rule
      with no negative confirmation breaches FR-016.
      *Verification*: 4.1's `entry-without-consent-instrument.yaml`,
      `mutate-without-ratified-capability.yaml`; 4.2's two legend negatives.
- [~] 2.9 [US2] The repo-scan layer, two passes. (a) **Whole-repo kind sweep**
      (FR-036): `rglob` every `*.y*ml` skipping `.git`, `node_modules`,
      `__pycache__`, `.venv`, and — when the target IS this checkout — THIS
      FEATURE'S OWN FIXTURE CORPORA: `examples/client-identity-roster/` AND
      `tests/`. **The `tests/` exclusion is load-bearing, not tidiness**: 6.5
      puts real roster fragments at
      `tests/doc-health/fixtures/client-identity-composition/<repo>/credentials/client-identity-roster/*.yaml`,
      which are at each FIXTURE repo's declared placement but not at this
      checkout's, so without it a self-scan reports every one as misplaced and
      breaks this task's own verification and 6.7's. The tree already states
      and tests the rule for the sibling scanner
      (`tests/doc-health/test_suite.py:23-27`, "fixture corpora must never
      enter a real scan"); neither exclusion narrows FR-036 over a TARGET
      DOMAIN repo, which carries no such trees. Any file carrying
      `kind: xfactory_client_identity_roster` that is **not a DIRECT CHILD of**
      `credentials/client-identity-roster/` raises `misplaced-roster-instance`
      naming the offending path AND the declared placement. **The predicate is
      EXACT-PATH, never a directory prefix** (gate ruling G3, FR-036):
      `path.parent == <target>/credentials/client-identity-roster`, not
      `startswith`. Under a prefix reading a nested instance at
      `credentials/client-identity-roster/<sub>/x.yaml` is tolerated by this
      pass AND missed by (b)'s flat glob — covered by nothing, the hole SC-005
      forbids. (b) **Declared-placement validation**: every fragment at the
      declared path — the FLAT `*.y*ml` glob, direct children only — is
      schema-validated and rule-checked, and the run prints a COUNT of records
      checked. (a) and (b) MUST be exact complements over one `*.y*ml`
      universe: every kind-carrying file is validated or reported, never
      neither. Plus the repo-context rules the packaged corpus cannot express:
      (i) gate-obligation RESOLUTION against the target's `workflows/<name>.yaml`
      gates, with an unresolvable obligation a finding (FR-011); and (ii)
      **`consent_ref` RESOLUTION** against the target repo's own
      consent-instrument records (FR-014's second clause — presence is 2.8's
      half, and a citation that resolves to nothing is the failure the change's
      central claim depends on catching). The MECHANISM, since the consent
      family declares no placement to cite: sweep the target for
      `kind: xfactory_consent_instrument` under the same `SKIP_DIR_NAMES` —
      what `validate-consent-instruments.py`'s own `repo_scan` does — and match
      `consent_ref` against each record's `instrument_id`, reading that
      record's `status` for "in force". Resolution is INTRA-REPO, the same
      posture as the gate obligation and deliberately NOT `evidence_ref`'s
      (FR-037), which points into another repo; "in force" is `executed` or
      `amended`, never `draft`, `pending_signatures`, `terminated` or
      `withdrawn`. **The in-force test is LIFECYCLE-SCOPED (gate ruling G1,
      FR-014): RESOLUTION binds every entry, but an entry whose
      `lifecycle_state` is `retired` is exempt from the in-force test — an
      ended instrument is the EXPECTED state beside a retired entry, since the
      ratified cascade runs withdrawal or termination through to retirement
      while FR-013 keeps the record. `planned` and `enrolled` entries take the
      in-force test unchanged, and a NON-retired entry citing an ended
      instrument raises its own code (distinct from the unresolvable-citation
      code — this citation resolves) naming the entry, the instrument and its
      status.** `ratified_by` is NOT resolved — the ratified clause attaches
      resolution to the instrument citation alone and the capability scenario is
      an absence test (2.8's half, with repo fixture 2 proving the gate exit).
      *Verification*: 4.5's repo fixtures 2, 4, 5, 6, 7 and 8; running the
      validator against this checkout must NOT report its own packaged corpus
      OR 6.5's fixture repos as misplaced (exit 0 with the absence notice,
      since openxFactory publishes no fragment of its own) — the `tests/`
      exclusion is what holds this true, and it is unaffected by the
      exact-path predicate, since 6.5's fragments are direct children of their
      OWN fixture repos' declared placement.
- [~] 2.10 [US2] Absence, and the negative guarantee (FR-022, FR-032, SC-013):
      a target with no `credentials/client-identity-roster/` directory, or the
      directory with no files, prints an EXPLICIT NOTICE naming the absence and
      exits 0. NO code path in the module derives an expected entry set — not
      from `credentials/requirements.yaml`, not from any other inventory.
      *Verification*: 4.5's repo fixture 3; 4.7's source-level assertion.

**Checkpoint**: the validator runs, self-tests, and scans → Phases 4 and 5 may
begin.

**REACHED 2026-08-15.** `scripts/validate-client-identity-roster.py`: 30 rules
across the six groups, all record-internal ones running to completion whether
or not the schema already refused the document, each raising its own kebab
code. No argument exits 2 and prints usage; a self-scan of this checkout exits
0 with the absence notice and reports NO misplacement of its own corpus.
**46/46 inline rule probes behaved as expected**, over repos built in
`tmp_path` — every named negative fires for its OWN code, every discrimination
partner stays clean, both misplacement arms fire (including the NESTED one the
exact-path predicate exists for), the retired/enrolled consent pair
discriminates, and identical inputs produce byte-identical findings. The
throwaway harness that ran them is in the session scratchpad
(`probe_phase2.py`); the PERMANENT module is 4.5's, which is why 2.2–2.10 stay
`[~]`: each names a Phase-4 fixture as its verification.

**One rule was CORRECTED by its own discrimination partner during this phase**
— the per-unit "left unused" predicate, which as first written fired on the
mandated Business Central positive. Recorded in 2.6 above, with the consequence
for 4.1's fixture. This is the discrimination doing exactly what SC-002 keeps
it for.

**FR-030 re-measured after Phases 1–2**: the four MODIFIED capabilities'
suites are byte-identical to 0.3's baseline — consent `0 error(s), 0
warning(s)`, credential-contracts `0 error(s) -> PASS`, and 645 tests
(636 passed + 9 skipped) against the baseline's 645. Neither phase touches a
MODIFIED capability's surface, and the measurement confirms it.

---

## Phase 3 — Cluster D: packaged examples

**Depends on**: **0.1 (HARD)** and Phase 1. **Blocks**: Phase 4's positives and
2.2's self-test corpus.

*Target directory*: `examples/client-identity-roster/`.

> Every task in this phase lists **0.1 as a hard dependency**. If 0.1 escalated
> and has not been ruled, this phase does not start.
>
> **0.1 escalated and IS ruled (2026-08-15).** The gate is satisfied by the
> ruling: **Decision C (Brett) — the packaged set is THREE cases**, the
> multi-surface reader having been relocated to the synthetic representability
> fixture now homed at task 4.9. Phase 3 proceeds on that basis, and no task
> here may reintroduce a packaged multi-surface reader.

- [x] 3.1 [US2] `examples/client-identity-roster/README.md` carrying
      `Status: ratified` plus a `Ratified by:` line naming
      `add-client-identity-roster` and the bundle it registers at — the
      `contracts/openxwallet/README.md` (006) header precedent, not the older
      siblings' `Status: draft` — with the sibling READMEs' layout block.
      *Depends on*: 0.1. *Verification*: doc-health's status-validity and
      tag-hygiene families report no finding (10.3).
- [x] 3.2 [US1] `client-identity-roster-farheap-opsx.example.yaml` — the
      Business Central worked case, transcribed from
      `OpsxFactory:tenants/farheap-bc-observer-identity-evidence-v1.yaml`: ONE
      entry with TWO admission acts (the provider-enforced Sandbox1 application
      user with no production application user; the admin-center Entra-app
      authorization with no scope selector, therefore tenant-wide), the UNION
      effective reach, and the declared excess with its provider reason, gate
      obligation and enforcement-test reference. The second act declares
      `exceeds_governed_unit: true` (it has no scope selector and the entry
      governs `sandbox1`) and is therefore covered by that `declared_excess` —
      which is exactly what 4.1's `scope-exceeds-unit-undeclared.yaml` omits,
      making this file its discrimination partner. **Two acts, ONE surface**: both
      acts sit under `admission_surface: business_central`, which packet task
      2.2 binds verbatim and answer 5's two-member vocabulary makes the only
      representable form — the delta's "each act is its own admission surface"
      scenario governs acts that admit INDEPENDENTLY, and these two do not (six
      days of admin-consented permissions still returned `401` until the
      admin-center act). Do not split the case into two surfaces and do not
      drop the second act (research.md Decision 1). `granted_permissions[]`
      carries the real four as member `id`s (`API.ReadWrite.All`,
      `Automation.ReadWrite.All`, `AdminCenter.ReadWrite.All`, `app_access`),
      each with its declared `achieves` and `reaches[]` (1.5), which is what
      makes this
      simultaneously the name/purpose-mismatch case
      (`opsx-farheap-bc-observer` achieving mutation) expressed through
      `declared_excess` rather than by renaming anything in a domain repo.
      `evidence_ref` pointers name `opensoft/OpsxFactory` and the real
      `tenants/farheap-bc-sandbox1-verify-probe-evidence-v*.yaml` paths — real
      pinned content, left UNRESOLVED by the validator (FR-037). Legend binds
      every free token used.
      *Depends on*: 0.1, 1.4–1.7. *Verification*: 2.2 self-test clean; SC-003
      and SC-004 are read off this file.
- [~] 3.3 **RELOCATED to task 4.9 by Decision C (Brett, 2026-08-15).** This
      task authored the provider-forced multi-surface reader as a PACKAGED
      entry carrying 0.1's citation verbatim. 0.1 established that no such
      citation exists, so the entry cannot be packaged without asserting an
      uncitable provider fact — and a packaged example is an instantiation
      template a domain copies. The case is NOT dropped: it becomes the
      SYNTHETIC representability fixture at **4.9**, with the same ZERO-findings
      obligation and the same discrimination role against 2.6's reach rules.
      Nothing is authored under this id; it is retained rather than deleted so
      the relocation is legible and the SC-002 positive can be traced from the
      case list to its new home.
- [x] 3.4 [US1] The `planned` entry, in the same fragment: `lifecycle_state:
      planned`, an identity not yet created, its kind declared as intent.
      *Depends on*: 0.1, 1.7. *Verification*: ZERO findings (FR-013, SC-002);
      and it is not reported as missing or incomplete (2.10, SC-013).
- [x] 3.5 [P] [US1] `client-identity-roster-farheap-ledgerx.example.yaml` — the
      SECOND fragment for the SAME client held by a SECOND domain (fragments
      are per (client, domain), which is why the three mandated PACKAGED cases
      span two
      files, ruling C3). Carries the GENUINE duty-separated pair (the
      `ledgerx-farheap-bc-poster` / `-provisioner` precedent, differing in
      granted permissions or declaring `duty_separation_rationale`, the
      optional field 1.5 declares) and the GENUINE per-unit pair (differing in
      `achieved_scope`). It also carries the **`retired` entry** (checklist
      pass): the third `lifecycle_state` member otherwise has no instance
      anywhere in the corpus, and FR-013's "a retired entry MUST retain its
      record" is a guarantee nothing exercises without one. **That entry's
      `consent_ref` names a `terminated` (or `withdrawn`) instrument** (gate
      ruling G1) — the cascade's own end state, which FR-014's lifecycle
      scoping admits for a `retired` entry and refuses for every other. It is
      authored here so the packaged corpus STATES the case; the RESOLUTION that
      makes it load-bearing is repo-context, and 4.5's fixtures 1 and 8 are
      where it is measured.
      **RETIRED ENTRY RELOCATED to its own fragment,
      `client-identity-roster-lxtest-ledgerx.example.yaml` (2026-08-15).** No
      retired identity exists for the (farheap, ledgerxfactory) pair — nor for
      (farheap, opsxfactory) — anywhere in the estate, and a fragment is per
      (client, domain), so packaging one here would synthesize a governed fact
      into an instantiation template, the exact move ruling A-16 and
      research.md Decision 8 forbid. The real one
      (`ledgerx-lxtest-ap-monitor`, torn down 2026-07-26 with per-step
      before/after evidence) belongs to (lxtest_opensoft, ledgerxfactory) and is
      packaged there. Full account in the Phase 3 checkpoint below. Everything
      else this task mandates — both genuine pairs — is in THIS fragment.
      *Depends on*: 0.1, 1.4–1.7. *Verification*: both pairs at ZERO findings in
      the same run that refuses 4.1's alias pair — the SC-002 discrimination
      asserted at 4.6; the `retired` entry likewise clean, and not reported as
      missing, incomplete or stale (FR-013, FR-033), nor reported for citing an
      ended instrument (FR-014).
- [x] 3.6 [P] [US6] `client-identity-drift-finding.example.yaml` — a complete
      finding: the `identity_key` OBJECT (element 3 = the entry's
      `authority_class_intended`), `fragment_ref` naming 3.2's fragment,
      `rule_id`, `roster_value`, `observed_value`, `observed_at`, `opened_at`,
      `status: open` — and therefore NO `disposition_ref`, which 1.9 makes
      conditional on `status: disposed` (an open finding has not been
      dispositioned; carrying a citation there was incoherent in the pre-
      checklist draft).
      *Depends on*: 0.1, 1.9. *Verification*: 2.2 self-test clean; 4.3's three
      negatives are its refusals.

**Checkpoint**: THREE mandated cases packaged across two fragments (Decision C
— the fourth is 4.9's fixture), drift example packaged → Phase 4 may assert
against them.

**REACHED 2026-08-15.** `examples/client-identity-roster/` carries FOUR
positives, all confirmed CLEAN by the validator's layer-1 self-test, which went
strict the moment the directory landed (`negative/` created in the same commit,
empty until 4.1). A self-scan of this checkout exits 0 and reports NO
misplacement of its own corpus. The three MANDATED packaged cases are where
3.2/3.4/3.5 put them; the drift example is 3.6's.

**THE ONE STRUCTURAL DEPARTURE — a THIRD positive fragment,
`client-identity-roster-lxtest-ledgerx.example.yaml`, and it is forced by the
same rule that forced Decision C.** 3.5 mandates the `retired` entry INSIDE the
farheap-ledgerx fragment. A fragment is per (client, domain), and an exhaustive
sweep of the estate establishes that NO retired identity exists for the
(farheap, ledgerxfactory) pair, nor for (farheap, opsxfactory): LedgerxFactory's
three FarHeap identities are all live and explicitly "retained", and
OpsxFactory's FarHeap observer is enrolled with Production pending. Authoring a
retired FarHeap identity would be synthesizing a governed fact into an
INSTANTIATION TEMPLATE — precisely what ruling A-16 and research.md Decision 8
forbid, and what Decision C chose relocation over. What DOES exist, with a full
evidence chain, is a retired identity for a DIFFERENT (client, domain) pair:
`ledgerx-lxtest-ap-monitor`, scoped `Mail.Read` bounded to one mailbox by an
Exchange application access policy, torn down 2026-07-26 in the recorded order
with before/after reads per step. It is therefore packaged as its own fragment,
which is what the per-(client, domain) rule requires. Two consequences worth
naming: the `exchange` member of the closed admission-surface vocabulary now has
a packaged POSITIVE instance, which it otherwise would not have anywhere in the
corpus; and G1's ENDED-INSTRUMENT arm stays where 3.5 already put its
measurement — repo fixtures 1 and 8 — because `consent_ref` resolution is
repo-context and this neutral repository publishes no consent-instrument record
for that engagement. The packaged entry cites the engagement's real consent
record and declares no status for it; the instrument record is the only
authority on that.

**No Phase 1–2 `[~]` task flips here.** Each of 1.2–1.10 and 2.2–2.10 names at
least one Phase-4 artifact in its verification line (a registered negative, a
repo fixture, or 4.5's assertion module), so none is closed out by this phase
even where its packaged half now passes — 1.4's fragments validate and 1.9's
drift example validates, but both also require Phase 4's negatives.

**Also landed in this commit, per the architect's Phase 0–2 review**: spec.md
FR-001's field enumeration now names the two Phase-1 additions it omitted —
`vendor_tenant_multi_obligations` (required only under `vendor_tenant_multi`;
FR-012's five obligations have no declaration site otherwise) and the
`standing_credential_attestation` subfields `attested_at`,
`grant_window_expires_at` and `held_credential_ref` (FR-013's falsification must
be record-internal, since FR-029 forbids observing a credential store, and
expiry must be read against `attested_at` rather than the clock or identical
inputs would yield different findings between runs, SC-011).

---

## Phase 4 — Cluster C: the fixture corpus

**Depends on**: Phases 1, 2, 3 — except **4.9, which depends on Phases 1 and 2
ONLY** (Decision C relocated it here from Phase 3, and it is authored in this
phase's own `tests/` tree rather than against a packaged fragment).
**Blocks**: Phase 5.

*Target directories*: `examples/client-identity-roster/negative/`,
`tests/client-identity-roster/` (including
`tests/client-identity-roster/fixtures/` for 4.9's synthetic fixture — a tree
2.9's `tests/` exclusion already keeps out of a self-scan).

Negatives take the CONSENT family's header dialect
(`# INVALID <record noun> — violates <requirement> (<rule>): <what is wrong>` /
`# … (finding <finding-code>)`), one violation per file, each registered by
filename in the validator's expectations table.

- [ ] 4.1 Author the NINETEEN record-internal packaged negatives — twelve of
      FR-016's named rules (the thirteenth packaged named rule,
      out-of-vocabulary admission surface, sits with its vocabulary siblings in
      4.2) plus SEVEN per-rule confirmations FR-016's "at minimum" list does not
      enumerate (FR-003, FR-008's second half, FR-010's name/purpose clause,
      FR-012, FR-002/FR-010's scope excess, and the two the checklist pass
      homed — FR-009's act side and FR-008's mapping coverage):
      `consent-recorded-as-access.yaml`,
      `unverified-act-counted-as-access.yaml` (an act carrying `verified_at`
      with NO `evidence_ref` — the predicate 2.5 gives this file, without which
      it would pass), `undeclared-reach.yaml`,
      `achieved-exceeds-intended-undeclared.yaml`,
      `name-understates-achieved-authority.yaml` (**sharpened by gate ruling
      G6** so it fails for its OWN reason: `authority_class_intended: mutate`
      AND `authority_class_achieved: mutate`, an observation-suggesting
      `identity_ref`, and NO `declared_excess` — with intended equal to
      achieved there is no excess to declare and therefore no cure, so the
      name code fires ALONE, unaccompanied by the achieved-above-intended
      finding that would otherwise mask it),
      `missing-enforcement-test.yaml`,
      `provider-enforced-without-per-unit-principal.yaml`,
      `per-unit-principal-available-but-logical.yaml`,
      **`per-unit-principal-undeclared.yaml`** (a mapping with no answer for a
      surface the entry touches — 2.6),
      **`undeclared-act-surface.yaml`** (an admission act on a surface the
      entry neither owns nor declares as spanned — 2.6),
      `vendor-homed-declared-client-resident.yaml` (**pinned to the G2 code**:
      the fragment declares `client_tenant`, the entry declares
      `residency_model: client_tenant_single` and a `home_tenant` that differs
      from it, and the expectations table pins the finding that NAMES
      `home_tenant` — so the file cannot pass by an inference the validator no
      longer makes),
      `vendor-tenant-multi-missing-obligations.yaml`,
      `mutate-without-ratified-capability.yaml` (the record-internal FINDING;
      repo fixture 2 proves the gate EXIT),
      `entry-without-consent-instrument.yaml` (absence; the unresolvable
      citation is repo fixture 6),
      `false-standing-credential-attestation.yaml`,
      `destructive-authority-class.yaml`, `full-tuple-duplicate.yaml`,
      `alias-pair-observationally-identical.yaml`, and
      **`scope-exceeds-unit-undeclared.yaml`** — a VERIFIED act declaring
      `exceeds_governed_unit: true` with NO `declared_excess`, whose
      discrimination partner is 3.2's worked case (the same shape with the
      excess declared, zero findings).
      *Verification*: each refused by its OWN registered code (2.2); SC-001.
- [ ] 4.2 [P] The closed-vocabulary and legend negatives (SC-014):
      `admission-surface-out-of-vocabulary.yaml`,
      `residency-model-out-of-vocabulary.yaml`,
      `enforcement-mode-out-of-vocabulary.yaml`,
      `lifecycle-state-out-of-vocabulary.yaml`,
      `identity-kind-out-of-vocabulary.yaml`, `legend-token-missing.yaml`,
      `legend-token-declared-twice.yaml`, `evidence-ref-malformed.yaml`.
      *Verification*: these FIVE vocabulary negatives plus 4.1's
      `destructive-authority-class.yaml` give ONE negative per ENTRY-side
      closed set (FR-034's six sets, six refusals), each refusal NAMING the
      closed vocabulary and the extension route; SC-014's SEVENTH set — the
      drift record's `status` — is homed at 4.3, so no closed vocabulary in the
      roster family ships without a refusal probe (the
      `issuance_preconditions` set is SC-008's, at 7.3); plus both legend cases
      (FR-034's two findings) and
      `evidence-ref-malformed.yaml`, which is FR-037's shape probe rather than a
      vocabulary or legend case.
- [ ] 4.3 [P] [US6] The THREE drift-record negatives:
      `drift-finding-without-roster-value.yaml`,
      `drift-finding-without-observed-value.yaml` (FR-035), and
      **`drift-finding-status-out-of-vocabulary.yaml`** (checklist pass) — the
      `status` set is closed and SC-014 covers EVERY closed vocabulary of this
      family, so its seventh set gets the refusal probe the other six have.
      *Verification*: refused by their own codes in the 2.2 self-test; the
      third names the closed `status` set the way 2.3's refusals name theirs.
- [ ] 4.4 [P] `achieved-class-contradicted-by-permissions.yaml` (**ruling
      A-11**) — an entry declaring `authority_class_achieved: observe` while a
      `granted_permissions[]` member DECLARES `achieves: mutate` (the
      contradiction is between two declarations in the record; the fixture must
      NOT be authored around a permission's name, because 2.6 reads the
      declared `achieves` and never the identifier's spelling).
      This homes FR-004's rule, which is distinct from
      `achieved-exceeds-intended-undeclared.yaml`'s (that one proves
      achieved-above-intended must be DECLARED; this one proves an achieved
      class cannot be ASSERTED against its own permissions). Neither
      substitutes for the other.
      *Verification*: refused by 2.6's FR-004 code, registered in the
      expectations table.
- [ ] 4.5 The EIGHT repo-shaped fixtures in `tests/client-identity-roster/
      test_client_identity_roster.py`, built in `tmp_path` from inline
      templates (the `tests/conformance-gate/test_conformance_checks.py`
      `make_repo` idiom): (1) conformant → exit 0, carrying TWO fragments for
      TWO clients whose entries share the WHOLE uniqueness tuple, which is how
      FR-006's fragment scope is measured (checklist pass: a cross-fragment
      comparison would report them as a duplicate and re-kill the per-unit
      flaw) — and, per gate ruling G1, ALSO a `retired` entry whose
      `consent_ref` resolves to a `terminated` instrument PRESENT in that
      repo's consent records, so FR-014's lifecycle exemption is measured
      clean rather than asserted; (2) nonconformant
      `mutate`-without-ratified-capability → nonzero — the ROSTER delta's own
      gate-exit scenario; its packaged sibling proves the FINDING
      record-internally and this repo proves the EXIT, which a packaged file
      cannot; (3) no-fragment → exit 0 + explicit notice;
      (4) **unresolvable gate obligation** (ruling A-11) — an entry whose
      `declared_excess.gate_obligation` names a gate ABSENT from that repo's
      `workflows/`, while the repo carries at least one REAL gate so the
      finding proves non-resolution rather than an empty tree → nonzero with
      FR-011's code; (5) misplacement — the roster kind at `tenants/stray.yaml`,
      outside `credentials/` entirely → nonzero with
      `misplaced-roster-instance` (SC-005); (6) **unresolvable consent
      citation** — an entry whose `consent_ref` names an instrument absent from
      that repo's consent records, while the repo carries at least one real
      `xfactory_consent_instrument` in force (so the finding proves
      non-resolution, not an empty tree) → nonzero with FR-014's resolution
      code; (7) **nested misplacement** (gate ruling G3) — a roster instance at
      `credentials/client-identity-roster/<sub>/x.yaml`, INSIDE the declared
      directory but not a DIRECT CHILD of it, so it is invisible to the flat
      validating glob → nonzero with `misplaced-roster-instance`. This is the
      arm the pre-gate prefix reading left covered by nothing, and it is the
      HARDER placement case: fixture 5 is outside `credentials/` entirely and
      any reading catches it. (8) **an ended instrument cited by a NON-retired
      entry** (gate ruling G1) — an `enrolled` entry whose `consent_ref`
      RESOLVES to the same `terminated` instrument fixture 1's `retired` entry
      cites → nonzero with FR-014's in-force code, which is NOT fixture 6's
      resolution code: the citation resolves, so the fixture can only fail for
      its own reason.
      *Verification*: `pytest tests/client-identity-roster/`; fixture 1 is the
      discrimination partner of fixtures 2, 4, 6 and 8 (it names a ratified
      capability, its gate obligation and its consent citation both DO resolve,
      and its `retired` entry's ended instrument is accepted), and fixture 7's
      partner is fixture 1's fragments at the declared placement.
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
      lacks a file. The count is unaffected by Decision C: it counts NEGATIVES,
      and 4.9 relocates a POSITIVE.
- [ ] 4.9 [US1] **The SYNTHETIC representability fixture — SC-002's fourth
      positive, relocated here from 3.3 by Decision C (Brett, 2026-08-15).**
      Author `tests/client-identity-roster/fixtures/multi-surface-reader-representability.yaml`:
      a fragment whose entry declares an `admission_surface` of
      `business_central`, a `declared_excess.spanned_surfaces[]` naming
      `exchange`, `granted_permissions[]` whose `reaches[]` cover both, an
      admission act on each surface, a `per_unit_principal_available` mapping
      answering BOTH surfaces, and the provider reason, bound mechanism, gate
      obligation and enforcement-test reference FR-010 requires.
      **The file MUST open with a DATED SYNTHETIC HEADER** — the ruling's item 1
      and FR-017's amended text — declaring in this order: that the record is
      SYNTHETIC and is NOT a packaged example and MUST NOT be instantiated from;
      that as of 2026-08-15 no in-vocabulary provider-forced multi-surface
      permission exists, citing BOTH halves of the falsification
      (`OpsxFactory:openspec/specs/business-central-administration/spec.md:93-101`
      — Business Central offers no read-only path at all; and
      `openspec/specs/exchange-administration/spec.md:46-56` — Exchange offers a
      surface-scoped read-only path, which is what falsifies "no single-surface
      read-only role exists"); that it exists to prove killed-flaw (a)
      REPRESENTABILITY — a spanned-surfaces entry with its forced breadth
      declared validates with ZERO findings — and to stand ready for vocabulary
      growth; and that it is authorized by Decision C, citing
      `openspec/changes/add-client-identity-roster/review/amendment-record-2026-08-15b.md`.
      The `provider_reason` field itself must be written as a REPRESENTABILITY
      PLACEHOLDER naming the header, never as an asserted provider fact — that
      distinction is the whole point of the relocation.
      *Depends on*: Phases 1 and 2 (it is validated by the Phase 2 validator);
      NOT on Phase 3. *Verification*: the fixture validates with ZERO findings,
      asserted in `tests/client-identity-roster/test_client_identity_roster.py`;
      and 2.6's undeclared-reach rule refuses the same record with
      `spanned_surfaces[]` removed — the discrimination that proves the fixture
      measures the rule rather than passing vacuously. This is SC-002's fourth
      positive and FR-017's multi-surface obligation, in full.

**Checkpoint**: every named rule has a refused negative and every killed-flaw
positive passes clean — three of the four SC-002 positives in the packaged
corpus, the fourth as 4.9's synthetic fixture.

---

## Phase 5 — Cluster F: pack membership (Decision A, archive blocker)

**Depends on**: Phases 2, 4. **Parallel with**: Phases 6, 7, 8.

- [ ] 5.1 [US3] Grow `tests/conformance-gate/test_conformance_checks.py` to
      load `validate-client-identity-roster` alongside the three `check-*`
      modules, exercising FOUR pack behaviours the deltas specify — three from
      the `domain-conformance-checks` delta (an entry nonconformance → nonzero;
      a conformant repo → 0; **no fragment → 0 with an explicit notice**) and
      one from the ROSTER delta's "A mutate identity has no ratified
      capability" scenario (→ ERROR not report) (FR-022). The three existing
      checks' 15 tests must pass UNMODIFIED — only new tests are added.
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
      the same identity MATERIAL. **EXACTLY TWO disjuncts (gate ruling G4):**
      (i) the same `identity_ref`; (ii) both entries declare
      `provider_object_ref` (1.5) AND the values are EQUAL. Disjunct (ii) does
      NOT fire when either entry omits the field — an absent declaration is
      not evidence of sharing. **It is NOT read against
      `principal_locations[]`**, which carries TENANT identifiers: that
      reading intersects on the shared client tenant and would refuse FR-024's
      ratified non-finding, since two domains holding separate identities in
      one client tenant necessarily share the tenant. Keyed on MATERIAL, never
      on (surface, class) collocation and never on collocation in a tenant.
      *Verification*: 6.6 asserts the FR-024 discrimination — two domains each
      holding their OWN separate identity on one surface and class is NOT a
      finding at any level — and 6.5's equal-`provider_object_ref` fixture
      proves disjunct (ii) fires on its own.
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
      *Verification*: `python3 openxFactory/scripts/doc-health.py --repo-root
      <aggregation checkout>` (the path from the aggregation root, plan green
      bar step 7) lists sixteen families and renders the new section; grep
      confirms the promoted spec and the ordinals are untouched.
- [ ] 6.5 [US5] Fixtures at
      `tests/doc-health/fixtures/client-identity-composition/` — at least THREE
      repo directories so the corpus proves both finding classes AND the FR-024
      non-finding: two domains sharing identity material for one client; two
      domains with separate identities on one surface and class; a
      single-fragment client for the skip case. **Plus the disjunct-(ii)
      fixture (gate ruling G4): two domains' entries for one client declaring
      EQUAL `provider_object_ref` under DIFFERENT `identity_ref` spellings →
      `shared-identity-material`.** It is the only probe of the second
      disjunct, and its discrimination partner is the FR-024 fixture, which
      must stay a NON-finding — separate identities in one client tenant, each
      with its own `provider_object_ref` (or none), sharing only the tenant. Include the fixture that
      produces a finding CONTRADICTING a ratified capability, which is what
      6.6's `CONTESTED` assertion measures. **Every fixture fragment MUST be
      intra-repo CONFORMANT** — closed vocabularies, legend, verified
      admission, both roots present with the consent citation RESOLVING to an
      `xfactory_consent_instrument` in force INSIDE that fixture repo (2.9),
      resolvable gate obligations — because
      6.7 runs the canonical roster validator over each of these repos and
      asserts exit 0, and that assertion is the whole point of ruling A-N4: the
      shared identity is intra-repo conformant, so the finding is genuinely
      composition-only. A minimal fixture missing `consent_ref` or a legend
      would fail 6.7 for reasons that measure nothing. This corpus is also
      where FR-016's "cross-domain shared identity" negative lives (research.md
      Decision 7).
      *Verification*: 6.6 and 6.7.
- [ ] 6.6 [US5] `tests/doc-health/test_client_identity_composition.py`.
      **Ruling A-9 — the trap this suite must not fall into**:
      `tests/doc-health/conftest.py` `make_ctx` defaults **`agg_root=None`**
      (line 66), and this family's FIRST branch is
      `ctx.agg_root is None → Skip`. **Every test MUST pass `agg_root`
      explicitly**, or it short-circuits into the skip and passes vacuously —
      green while measuring nothing. The single-repo-skip test passes
      `agg_root=None` EXPLICITLY so the omission can never be mistaken for
      intent. Tests: both finding classes; the FR-024 non-finding; both skips;
      no intra-repo code in the output; **the RESOLUTION CLASS — a finding that
      contradicts a ratified capability is `CONTESTED`, one that does not keeps
      the dataclass default** (FR-023, US5 acceptance scenario 5, otherwise
      authored at 6.3 and measured by nothing); and DETERMINISM — the family
      run twice over one fixture context with `__dict__`-equal sorted findings,
      the `tests/doc-health/test_suite.py:15-19` pattern (SC-011, which a
      vacuous skip would satisfy trivially).
      *Verification*: `pytest tests/doc-health/test_client_identity_composition.py`;
      plus `pytest tests/doc-health/` whole-suite, where the new family must add
      findings to NO existing family's fixtures.
- [ ] 6.7 [US5] **Ruling A-N4** — prove SC-006 across BOTH corpora: run
      `scripts/validate-client-identity-roster.py` over each doc-health
      cross-domain fixture repo and assert **exit 0** on each (which is why
      6.5 requires every fixture fragment to be intra-repo conformant). Without
      this the
      "leaves the domain gate exit unchanged" half of SC-006 is an assertion
      about a corpus nothing measured; with it, the shared identity is proven
      intra-repo CONFORMANT and the finding proven composition-only.
      *Files*: `tests/doc-health/test_client_identity_composition.py` — named,
      not left as a choice (the roster-side module is the rejected
      alternative: this test reads the fixture repos that live beside the
      doc-health module). A test, not a manual step.
      *Verification*: the test passes; paired with 5.1's nonzero-exit case it is
      SC-006's complete measurement.

---

## Phase 7 — Cluster H: `credential-contracts` (Decision B, archive blocker)

**Depends on**: no BUILD dependency in this feature; 7.1's member description
cites the drift kind NAME `xfactory_client_identity_drift_finding`, which is
fixed at 1.9, so if this phase runs first the spelling comes from 1.9's task
text and not from a fresh invention. **Parallel with**: Phases 5, 6, 8.
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
      **The COUNT-BEARING PROSE sweep ships with the enum growth — two sites,
      both saying "five" of a set that is becoming six** (gate ruling G5): the
      schema comment at `contracts/schemas/consent-instrument.schema.yaml:195`
      ("CLOSED five-state lifecycle") and the validator's
      `alias-target-not-neutral` message at
      `scripts/validate-consent-instruments.py:356` ("does not target the
      closed five-state enum", the site 8.2 edits). Both become
      **six-state**. This is the consent-side counterpart of FR-025's
      count-bearing prose rule for doc-health, and it is a COUNT, not an
      ordinal — no ordinal statement about an earlier state is touched.
      *Verification*: 8.6's regression; `withdrawn` is a DISTINCT member, never
      aliased onto `terminated`; a grep for "five-state" across the schemas and
      `scripts/` returns nothing.
- [ ] 8.2 [US4] `scripts/validate-consent-instruments.py`: `NEUTRAL_STATUSES`
      (`:129-130`) + `withdrawn` — the alias-target check adjudicates against
      this tuple, so omitting it would let a domain alias onto a status the
      schema accepts and the validator rejects; and `PAST_SIGNATURE_STATUSES`
      (`:133`) + `withdrawn` — an instrument can only be withdrawn after
      execution, so the lifecycle-skip discipline must reach it. The
      `alias-target-not-neutral` MESSAGE at `:356` is one of 8.1's two
      count-bearing prose sites: "closed five-state enum" → **six-state**,
      edited in the same pass that grows the tuple it describes.
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
- [ ] 9.4 [US2] **After 9.1, 9.2 AND 9.3 have landed** — `RELEASE_SURFACE_PATHS`
      (`scripts/hermes_runtime_validation/release.py:64-70`) covers
      `contracts/manifest.yaml`, `contracts/CHANGELOG.md` and
      `contracts/README.md`, so building the inventory before the changelog and
      README edits land bakes in digests this same commit invalidates
      (checklist pass; the [P] on 9.2/9.3 means "parallel with each other",
      never "concurrent with 9.4") — generate
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

- [ ] 10.1 Author `specs/007-client-identity-roster/traceability.yaml` in the
      006 file's ACTUAL shape (read
      `specs/006-openxwallet-contracts/traceability.yaml`, not only its task
      6.6): the record envelope — `schema_version: 1`, `kind:
      openxfactory_realization_traceability`, `feature`, `ratified_change`,
      `capabilities` (all five) — then `requirements:` keyed by id, each row
      carrying `statement`, `artifact` (the file that realizes it),
      **`enforced_by`** (validator rule / test / command — the 006 field name,
      not a renamed one), `negative_confirmation` (the probe that proves the
      check is load-bearing, or an explicit `n/a` with a reason for the
      positive-only criteria), and `red_proven` in 006's own sense:
      SUPPRESSING the rule's finding code turns the corpus red, which is what
      proves the probe fails FOR ITS OWN REASON rather than incidentally
      (FR-018's standard; 2.2's break-one-negative procedure is the
      reproduction, no new script needed). The envelope is not optional — every
      YAML in this tree carries `schema_version` + `kind`. Rows: FR-001 …
      FR-039 and SC-001 … SC-014; the SC rows EXTEND the 006 shape, which
      carries requirement rows only. The plan DEFERS this file to
      implementation precisely because `red_proven` needs RUNS — it cannot be
      authored at plan time. The FR-022/SC-006 rows carry the ruling A-N2
      residual note (task 5.3).
      *Verification*: a coverage check that every FR and SC id in spec.md has a
      row, and that no row's `red_proven` is left unset.
- [ ] 10.2 `OPENSPEC_TELEMETRY=0 openspec validate add-client-identity-roster
      --strict` **and** `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`,
      run from the `openxFactory/` root. 58/58 at `4de5bb2` — it must not
      regress.
      *Verification*: both exit 0; the `--all` count is ≥ 58.
- [ ] 10.3 The doc-health family green:
      `python3 openxFactory/scripts/doc-health.py --repo-root <aggregation
      checkout>` run FROM the aggregation root (the script lives inside the
      openxFactory repo, so the leading `openxFactory/` is required from there)
      — SIXTEEN families run, the new one REPORTS or SKIPS
      with an explicit reason, and NO new finding lands against this change or
      its documents (FR-025, SC-009), **excluding the `document-catalog`
      family's `coverage` and `stale-entry` classes against documents THIS
      change adds or edits** (gate ruling G8). Those three arms — coverage for
      the new `examples/client-identity-roster/README.md`, stale-entry for the
      `contracts/CHANGELOG.md` and `contracts/README.md` edits, and revision
      re-staling when the catalog merges — are LAGGING AGGREGATION-CATALOG
      STATE, not defects: the snapshot is aggregation-hosted and the nightly
      catalog lane's merge phase cures them in ONE cycle (precedent:
      `openxdox-naming.md`, whose identical coverage finding self-healed on
      the next nightly). Record the excluded findings verbatim in the run
      notes with that reason, so the exclusion is auditable rather than a
      silent pass. **Every other family, and every other `document-catalog`
      class, fails this task unqualified** — including a `coverage` or
      `stale-entry` finding against a document this change did NOT touch.
      A demonstration run of the merge phase is OPTIONAL and, if done, runs in
      a THROWAWAY aggregation checkout with
      `--catalog-unavailable-reason worker_unavailable` — **never in the
      shared `/home/brett/projects/xFactory` checkout**, which it would leave
      carrying uncommitted `runs/` and `.sequence/` state the porcelain guard
      (10.6) does not cover.
      Plus `pytest tests/doc-health/` whole suite green against 0.3's baseline.
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
      review killed have regressed and the work stops. The multi-surface reader
      is 4.9's SYNTHETIC fixture rather than a packaged entry (Decision C,
      2026-08-15); its ZERO-findings obligation in this measurement is
      unchanged, and the measurement must reach it — a run that covers only the
      packaged fragments would silently drop SC-002's fourth positive, which is
      the outcome the relocation was ruled to avoid, not to cause.
      *Verification*: `pytest tests/client-identity-roster/ -k discrimination`
      plus the self-test's zero-finding verdict on both packaged fragments AND
      on 4.9's fixture.
- [ ] 10.6 The boundary measurements: `git status --porcelain` over the
      AGGREGATION checkout shows no change under `xFactories/` (SC-012, FR-030);
      a confirmation that no credential was minted and no provider call made
      anywhere in the feature or its tests (FR-029); **the FR-027 no-mutation
      confirmation — a source-level check that no module in this feature
      writes to a roster fragment, a permission set or an admission record,
      and that the drift path reads and records only** (US6's Independent Test
      asks for exactly this, and a schema description is not a verification);
      and the suite-wide hermeticity guard (`tests/hermeticity.py`) confirmed
      active, which makes a network reach a test FAILURE rather than a silent
      success (SC-011).
      *Verification*: clean porcelain under `xFactories/`; `pytest tests/`
      green with the guard registered.
- [ ] 10.7 **The pre-archive delta-fidelity assertion** (gate ruling G7;
      precedent
      `openspec/changes/archive/2026-08-04-add-ideation-cross-reference-readiness/tasks.md:5`,
      which records exactly this rebase for the same requirement). BEFORE the
      archive step runs, verify that the `doc-health` delta's MODIFIED
      "Deterministic check families" block is REBASED onto the promoted
      requirement as it then stands: every promoted scenario restated verbatim
      (seven at the time of writing — "A run executes the check families" with
      all of its THEN/AND bullets, "Lifecycle conformance checks fire", "A
      register carries staged status", "Drift checks fire", "Catalog
      conformance checks fire", "Routing conformance checks fire", "Origin
      conformance checks fire"), plus THIS change's additions and nothing else.
      The archive rewrites a requirement WHOLESALE from the delta's text, per
      requirement and not per capability, so any promoted scenario the delta
      omits is DELETED on landing. Apply the same check to the
      `consent-instrument` delta's restated lifecycle requirement. If the
      promoted text has moved since (another lane landing first), rebase again
      — the assertion is against the promoted file at archive time, never
      against this file's snapshot of it.
      *Verification*: diff the delta block against
      `openspec/specs/doc-health/spec.md`'s promoted requirement — every
      promoted scenario present; then `openspec validate
      add-client-identity-roster --strict` and `--all --strict` (10.2). The
      2026-08-15 rebase is recorded in
      `openspec/changes/add-client-identity-roster/review/amendment-record-2026-08-15.md`.

---

## Requirement → task coverage

Every FR and SC in spec.md maps to at least one task. `traceability.yaml`
(10.1) is the machine-readable form; this table is the authoring check that
nothing was orphaned.

| Requirement | Tasks |
|---|---|
| FR-001 | 1.4 (fragment, incl. `client_tenant`), 1.5 (entry, incl. `provider_object_ref`) |
| FR-002 | 1.6, 2.5, 4.1 (`scope-exceeds-unit-undeclared.yaml`) |
| FR-003 | 1.6, 2.5, 4.1 |
| FR-004 | 2.6, 4.4 |
| FR-005 | 1.2, 4.1 |
| FR-006 | 1.3, 2.4, 4.1, 4.5 (fixture 1: the fragment scope) |
| FR-007 | 1.2, 2.3, 4.2 |
| FR-008 | 1.7, 2.6, 4.1 |
| FR-009 | 1.7, 2.6, 3.3, 4.1 |
| FR-010 | 1.7, 2.5 (scope excess), 2.6, 3.2, 4.1 |
| FR-011 | 1.7, 2.9, 4.1 (missing enforcement test), 4.5 (fixture 4: unresolvable obligation) |
| FR-012 | 1.4 (`client_tenant`, ruling G2), 1.8, 2.7, 4.1 |
| FR-013 | 1.7, 2.7, 3.4, 3.5 (the `retired` entry), 4.1 |
| FR-014 | 2.8 (presence), 2.9 (resolution + the lifecycle-scoped in-force test), 3.5 (the `retired` entry's ended instrument), 4.1, 4.5 (fixtures 2, 6, and 8 — the non-retired entry citing an ended instrument) |
| FR-015 | 2.1 (shape, argument, exit codes) + 2.3–2.10 ("enforce every intra-repo rule") |
| FR-016 | 4.1, 4.2, 4.3, 4.4, 4.5, 4.8, 6.5 |
| FR-017 | 3.2, 3.3, 3.4, 3.5, 4.6 |
| FR-018 | 2.2 |
| FR-019 | 3.1–3.6 |
| FR-020 | 1.10, 2.9, 9.1 |
| FR-021 | 9.1–9.6 |
| FR-022 | 2.10, 5.1, 5.2, 5.3 |
| FR-023 | 6.1, 6.2 (both disjuncts, ruling G4), 6.3, 6.4, 6.5, 6.6 |
| FR-024 | 6.2, 6.5, 6.6 |
| FR-025 | 6.4, 10.3 |
| FR-026 | 8.3, 8.4, 8.5 |
| FR-027 | 1.9, 10.6 |
| FR-028 | 7.1, 7.2, 7.3 |
| FR-029 | 2.1, 0.1, 10.6 |
| FR-030 | 0.3, 5.1, 7.4, 8.6, 10.4, 10.6 |
| FR-031 | 1.2, 2.3 |
| FR-032 | 2.10, 4.7 |
| FR-033 | 1.6 |
| FR-034 | 1.2, 1.4, 2.3, 2.8, 4.2 |
| FR-035 | 1.9, 3.6, 4.3 |
| FR-036 | 2.9 (exact-path predicate), 4.5 (fixtures 5 and 7 — outside `credentials/`, and nested inside the declared directory) |
| FR-037 | 1.6, 2.9, 4.2 (`evidence-ref-malformed.yaml`), 8.3 |
| FR-038 | 2.4, 3.5 (both genuine pairs), 4.1 (alias-pair negative), 4.6 |
| FR-039 | 8.1, 8.2, 8.5 |
| SC-001 | 4.1–4.4, 2.2, 10.4 |
| SC-002 | 3.3, 3.4, 3.5, 4.6, 10.5 |
| SC-003 | 3.2 |
| SC-004 | 1.5, 3.2 |
| SC-005 | 2.9, 4.5 (fixtures 5 and 7) |
| SC-006 | 5.1, 6.7, 5.3 (residual) |
| SC-007 | 8.5, 8.6 |
| SC-008 | 7.1, 7.2, 7.3 |
| SC-009 | 6.4, 6.6, 10.3 |
| SC-010 | 10.2, 10.3, 10.4, 9.6 |
| SC-011 | 2.1, 6.6, 10.6 |
| SC-012 | 7.4, 10.6 |
| SC-013 | 2.10, 4.7, 3.4 |
| SC-014 | 1.2, 1.9, 4.2, 4.3 |

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
- Within Phase 9, 9.2 and 9.3 are `[P]` **with each other only**; the
  sequence is 9.1, 9.2, 9.3 → 9.4 → 9.6, because all three of the files 9.1–9.3
  edit are release-surface members whose digests 9.4 records.

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
