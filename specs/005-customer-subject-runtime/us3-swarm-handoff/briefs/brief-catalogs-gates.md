# Lane D Integrator Brief — T064 catalog registration + T065 combined gate
Feature worktree: `/workspace/projects/xFactory/openxFactory-worktrees/005-customer-subject-runtime` (branch `005-customer-subject-runtime`). All four catalogs live under `contracts/hermes-runtime/`. Per tasks.md "Shared-File Ownership", **only you (the catalog integrator) edit these four files** in T014/T030/T050/T064/T077.

---

## 1. Record shapes of the four catalog files

### 1a. `contracts/hermes-runtime/contract-index.yaml`
Header: `schema_version: 1`, `kind: openxfactory-hermes-runtime-contract-index`, then a single `contracts:` list. Every entry has exactly: `contract_id`, `path` (relative to `contracts/hermes-runtime/`), `type` (observed values: `acceptance-map`, `contract-index`, `schema`, `evidence-register`, `documentation`, `fixture-index`, `sql`), `contract_schema_version` (1 for catalog/doc entries, 2 for schemas and the SQL), `consumers` (list), `semantic_member`, `release_member` (booleans; everything is `true`/`true` except the README which is `semantic_member: false`).

Template — the existing SQL entry (the direct model for registering `migrations/v1-to-v2.sql`):
```yaml
- contract_id: hermes-operational-postgres-v2
  path: hermes-operational-postgres-v2.sql
  type: sql
  contract_schema_version: 2
  consumers:
  - openxfactory-release-verifier
  - xfactory-hermes-install
  semantic_member: true
  release_member: true
```
Schema entries instead use `consumers: [openxfactory-validator, xfactory-hermes-install]` (see e.g. `customer-subject-reference-profile`).

**Ordering convention**: entries are appended in registration waves. Wave 1 (T014/T030: catalogs, README, US1 schemas) is path-sorted; wave 2 (T050: the 18 US2 schemas) is bytewise path-sorted (`approval-decision-policy` before `approval-decision` because `-` < `.`), with the SQL entry deliberately placed **last** in the file even though `h` would sort earlier. For T064: append a new US3 wave at the end — the two new schemas (`legacy-quarantine-record.schema.yaml`, `migrations/v1-to-v2-mapping.schema.yaml`) path-sorted, then `migrations/v1-to-v2.sql` last. The T051 checkpoint recorded **31 catalog members / 25 schemas**; your additions change these counts.

### 1b. `contracts/hermes-runtime/fixtures/index.yaml`
Header: `schema_version: 1`, `kind: openxfactory-hermes-runtime-fixture-index`, `feature: 005-customer-subject-runtime`, `governed_change: add-hermes-customer-subject-runtime-contract`, `fixture_root: contracts/hermes-runtime/fixtures`, `status: implemented`, then `cases:`.

Semantic-case template (block style, used by US1 entries):
```yaml
- case_id: overlay-manifest-digest-drift
  phase: semantic
  class: invalid
  requirement_ids: [HCS-004, HCS-006]
  scenario_ids: [HCS-004-S03, HCS-006-S03]
  inputs: [pins/overlay-manifest-digest-drift.yaml]
  depends_on: []
  evaluation_time: "2026-07-12T12:00:00Z"
  expected:
    outcome: fail
    primary_finding_code: HCS-OVERLAY-DIGEST
    allowed_secondary_codes: []
  evidence_id: EVIDENCE-FIXTURE-OVERLAY-MANIFEST-DIGEST-DRIFT
```
Style note: the US2 authority/isolation entries use compact flow style — `expected: {outcome: fail, primary_finding_code: HGR-GRANT-CYCLE}` — and omit `allowed_secondary_codes` when empty; they also use `evaluation_time: "2026-07-12T12:30:00Z"` vs 12:00 elsewhere. Both styles coexist. `evidence_id` is always `EVIDENCE-FIXTURE-<CASE-ID-UPPERCASED>`. `depends_on` names other case_ids (e.g. `artifact-digest-drift` depends on `artifact-valid`). `allowed_secondary_codes` may list extra tolerated codes (see `topology-retired-identity-reuse`, `topology-lifecycle-fork`).

**Database-phase case** — the one existing example, `postgres-us2-governed-isolation-matrix`, is the last entry and the template for the US3 matrix case. Its distinct shape: `phase: database`, `class: valid`, `requirement_ids` = all seven HGR-001..007, `scenario_ids` = 26 explicit scenario IDs (block list), `inputs: []`, `depends_on: []`, **no `evaluation_time`**, `expected: {outcome: pass, allowed_secondary_codes: []}` (block form), `evidence_id: EVIDENCE-FIXTURE-POSTGRES-US2-GOVERNED-ISOLATION-MATRIX`, and then a `database:` block:
```yaml
  database:
    engine: postgresql
    supported_majors: [15, 16]
    source_paths:        # 33 repo-relative paths: all 25 schema yamls + the v2 SQL +
    - contracts/hermes-runtime/approval-decision-policy.schema.yaml
    # … + scripts/hermes_runtime_validation/{fixtures,loader,semantics/authority,semantics/evidence}.py
    # … + scripts/run-hermes-runtime-postgres-tests.sh
    # … + tests/hermes_runtime_contracts/postgres/{compose.yaml,conftest.py,images.lock.yaml}
    test_modules:        # 6 pytest files under tests/hermes_runtime_contracts/postgres/
    - tests/hermes_runtime_contracts/postgres/test_topology_lifecycle.py
    # … test_roles_and_rls, test_scope_pooling, test_governed_evidence,
    #   test_authorization_races, test_contract_alignment
    seed_scripts:        # numbered SQL under postgres/fixtures/isolation/ (00-,10-,20-,30-)
    assertion_scripts:   # SQL under postgres/assertions/isolation/ (alphabetical)
    row_expectations:
      active_customer_layers: 2
      successful_projection_target_artifacts: 1
      successful_projection_operation_authorizations: 1
      successful_projection_trace_edges: 1
      failed_projection_authoritative_rows: 0
    digest_expectations:
      artifact_body_reverified_at_admission: true
      artifact_body_reverified_at_authorization: true
      operation_and_trace_endpoints_digest_bound: true
    authoritative_deltas:      # prose strings
    - successful projection atomically appends one target artifact, one operation authorization, and one trace edge
    - rejected or rolled-back projection appends no authoritative row
    - committed revocation prevents every later governed use
    result_refs:
    - major: 15
      path: tests/hermes_runtime_contracts/postgres/evidence/postgres-15.json
      expected_outcome: pass
    - major: 16
      path: tests/hermes_runtime_contracts/postgres/evidence/postgres-16.json
      expected_outcome: pass
```
**Grouping/ordering convention**: cases grouped by fixture directory in wave order — references (8), pins (8), topology (20), authority (12, alphabetical by case_id), isolation (3), artifacts (6, alphabetical), approvals (14, alphabetical), traceability (4, alphabetical), then database-phase case(s) **at the very end**. For T064: register the migration/recovery/quarantine/image-lock/drift coverage as a US3 database-phase case (e.g. mapping HGR-008-S01..S08) appended after the US2 matrix, with `source_paths` covering the frozen US3 surface (`migrations/v1-to-v2-mapping.schema.yaml`, `legacy-quarantine-record.schema.yaml`, `migrations/v1-to-v2.sql`, the updated `hermes-operational-postgres-v2.sql`, `scripts/hermes_runtime_validation/migration.py`, `scripts/hermes-runtime-dataset-digest.py`, `scripts/apply-hermes-runtime-postgres-v2.py`, `scripts/validate-hermes-runtime-postgres.py`, `scripts/run-hermes-v1-to-v2-migration.sh`, `images.lock.yaml`, compose/conftest), `test_modules` = `test_clean_apply.py`, `test_ddl_drift.py`, `test_migration.py`, `test_migration_recovery.py`, `test_quarantine.py`, and seed/assertion scripts from `postgres/fixtures/migration/` and `postgres/assertions/migration/` (T062). Any semantic golden-vector fixture (`postgres/fixtures/digest-golden-vectors.yaml` is test-side, likely not indexed here — confirm against how T057 lands).

### 1c. `contracts/hermes-runtime/acceptance-map.yaml`
Header: `schema_version: 1`, `kind: openxfactory-hermes-runtime-acceptance-map`, `feature`, `governed_change`, `fixture_index: fixtures/index.yaml`, `evidence_register: evidence-register.yaml`, `us1_binding_status: partial`, `us2_binding_status: partial`, `expected_openspec_requirement_count: 17`, `expected_openspec_scenario_count: 85`. Then three sections: `openspec_parity` (17 requirement entries), `stories` (US1–US4), `gates` (G0-PROVIDER, G0-CONSUMER).

`openspec_parity` entry template (HGR entries have no `feature_requirement_ids`; HCS entries do):
```yaml
- id: HGR-008
  capability: hermes-governed-record-integrity
  title: v2 persistence coexists with v1 and migrates atomically
  scenario_ids:
  - HGR-008-S01
  - HGR-008-S02
  - HGR-008-S03
  - HGR-008-S04
  - HGR-008-S05
  - HGR-008-S06
  - HGR-008-S07
  - HGR-008-S08
  scenario_titles:
  - Clean v2 database is initialized twice
  - Same-named database object or security authority has drifted
  - Two-subject v1 database is migrated
  - Migration mapping is ambiguous
  - Source changes during cutover
  - Migration is retried with another map
  - Legacy approval lacks target digest
  - Quarantined evidence is referenced
```
The US3 story block already exists too:
```yaml
- story_id: US3
  title: Upgrade legacy operational evidence safely
  requirements: [FR-026, FR-027, FR-028, FR-029, FR-030, FR-041]   # (block-list in file)
  outcomes: [SC-006, SC-007, SC-008, SC-014, SC-016]
  contract_groups: [postgres-v2, migration, quarantine, dataset-digest]
```
**Implication for T064**: HGR-008 parity and the US3 story are already registered; the expected counts (17/85) must NOT change. Your acceptance-map edits are likely limited to binding-status headers (see open question) — the T011/T012 parity tests will fail if you add/duplicate/dangle scenario IDs. Ordering: parity entries by requirement ID (HCS-001..006, HGR-001..009, NJE-004, SCO-002). YAML comments are permitted (there's one inside US1's requirements list).

### 1d. `contracts/hermes-runtime/evidence-register.yaml`
Header: `schema_version: 1`, `kind: openxfactory-hermes-runtime-evidence-register`, `feature`, `governed_change`, `authorization_effect: none`, `us1_binding_status: partial`, `us2_binding_status: partial`, `expected_scenario_count: 85`. Then `entries:` — exactly one entry per scenario, ordered by scenario ID (HCS-001-S01 … SCO-002-S07). Fields: `scenario_id`, `requirement_id`, `scenario_title`, `status` (`bound` | `planned`), `authorizes: false` (always), `evidence_id` (`EVIDENCE-<scenario-id>`), `planned_owner_task`, `fixture_case_ids`, `test_node_ids`, `result_refs`.

Template — a bound, postgres-backed entry (your model for HGR-008 entries):
```yaml
- scenario_id: HGR-002-S02
  requirement_id: HGR-002
  scenario_title: Subject A attempts a write into Subject B
  status: bound
  authorizes: false
  evidence_id: EVIDENCE-HGR-002-S02
  planned_owner_task: T050
  fixture_case_ids:
  - postgres-us2-governed-isolation-matrix
  test_node_ids:
  - tests/hermes_runtime_contracts/postgres/test_roles_and_rls.py::test_customer_a_cannot_write_or_delete_customer_b[15-insert]
  - tests/hermes_runtime_contracts/postgres/test_roles_and_rls.py::test_customer_a_cannot_write_or_delete_customer_b[15-update]
  - tests/hermes_runtime_contracts/postgres/test_roles_and_rls.py::test_customer_a_cannot_write_or_delete_customer_b[15-delete]
  - tests/hermes_runtime_contracts/postgres/test_roles_and_rls.py::test_customer_a_cannot_write_or_delete_customer_b[16-insert]
  - tests/hermes_runtime_contracts/postgres/test_roles_and_rls.py::test_customer_a_cannot_write_or_delete_customer_b[16-update]
  - tests/hermes_runtime_contracts/postgres/test_roles_and_rls.py::test_customer_a_cannot_write_or_delete_customer_b[16-delete]
  result_refs:
  - tests/hermes_runtime_contracts/postgres/evidence/postgres-15.json
  - tests/hermes_runtime_contracts/postgres/evidence/postgres-16.json
```
The 8 entries **you own at T064** are HGR-008-S01 … HGR-008-S08 — all currently `status: planned`, `planned_owner_task: T064`, with empty `fixture_case_ids`/`test_node_ids`/`result_refs`. Edit them **in place** (do not append). Note carefully: HCS-005-S03, HGR-001-S01, HGR-001-S02, all HGR-009, NJE-004, and SCO-002 entries are `planned` with `planned_owner_task: T077` — those belong to the US4 integrator, not you.

## 2. Evidence-register ↔ postgres evidence JSON binding, and what US3 adds

- Binding mechanism: a scenario is bound to database evidence by (a) listing the database-phase fixture case in `fixture_case_ids`, (b) listing per-major parametrized pytest node IDs (`…[15]`/`…[16]` suffixes) in `test_node_ids`, and (c) `result_refs` as **plain repo-relative paths** to `tests/hermes_runtime_contracts/postgres/evidence/postgres-15.json` and `postgres-16.json`. The register itself pins **no digests and no test counts** — it is pure path/ID indirection. (The fixture index's `result_refs` add `major` + `expected_outcome: pass` per file; the register's are bare paths.)
- The evidence JSONs are self-describing. Current `postgres-15.json` shape: `{"image": "postgres@sha256:…", "kind": "HermesRuntimePostgresEvidence", "major": 15, "matrix": {"case_id": "postgres-us2-governed-isolation-matrix", "digest": "sha256:ca8674…", "profile": "xfactory-postgres-matrix-v1"}, "outcome": "pass", "schema_version": 1, "source_identity": {"digest": "sha256:867015…", "identity_kind": "canonical_content", "member_count": 53, "profile": "xfactory-postgres-source-inputs-v1"}, "suite": {"id": "hermes-runtime-postgres", "test_count": 61}}` — i.e., the **matrix digest, source-identity digest/member_count, image digest, and test count live in the JSON**, computed over the source-path inventory declared in the fixture index's `database:` block.
- Therefore US3 must: (1) flip HGR-008-S01..S08 to `bound` with fixture cases / node IDs / the two result_ref paths; (2) add the US3 database case (and any US3 files appended to source-path inventories) to `fixtures/index.yaml`; (3) **regenerate both evidence JSONs only after the US3 SQL, runner, fingerprints, fixtures, and source-path inventory are frozen** (explicit Lane D instruction in `fable-swarm-handoff-us3.md`: "US3 changes the production SQL and test inventory, so these evidence records must be regenerated only after the US3 source surface is frozen" and "Regenerates both PostgreSQL evidence records only after production SQL, runner, fingerprints, fixtures, and the source-path inventory are frozen"). The T051 baseline digests (source `sha256:867015c4…`, matrix `sha256:ca867466…`, 61 tests per major) **will change**; the new values belong in the regenerated JSONs and the US3 checkpoint record, not in the register. Also confirm whether the runner emits one matrix block or per-case blocks once two database cases exist (see open questions).

## 3. Gate commands documented in `specs/005-customer-subject-runtime/quickstart.md` (in file order)

Run everything from the feature worktree root **inside py-bench**; never host Python; never commit container-absolute paths.

§1 Confirm checkout:
```bash
cd "$(git rev-parse --show-toplevel)"
git status -sb
git branch --show-current        # expect 005-customer-subject-runtime
```
§2 Environment:
```bash
uv venv .venv
uv pip sync --python .venv/bin/python requirements/hermes-runtime-contracts.lock
: "${DOMAIN_REPO_ROOT:?set DOMAIN_REPO_ROOT to the prepared canonical mirror root}"
```
§3 Governance + static gates (this plus §4 is the T065 "combined US1/US2/US3 strict gate"):
```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
.venv/bin/python scripts/validate-hermes-runtime-contracts.py \
  --strict \
  --domain-repo-root "$DOMAIN_REPO_ROOT"
.venv/bin/python -m pytest tests/hermes_runtime_contracts -m 'not postgres' -q
```
§4 PostgreSQL 15/16 conformance — image-lock refresh is only for pre-candidate-freeze review; normal runs are digest-pinned:
```bash
./scripts/run-hermes-runtime-postgres-tests.sh --update-image-lock   # only before candidate freeze
./scripts/run-hermes-runtime-postgres-tests.sh                       # normal/release run
```
Docker/image unavailability is a **failed required gate, not a skip**.
§5 Single-case inspection (diagnostic, not a gate):
```bash
.venv/bin/python scripts/validate-hermes-runtime-contracts.py --case topology-operational-two-customers --json
.venv/bin/python scripts/validate-hermes-runtime-contracts.py --case topology-operational-zero-customers --json
```
§6–§9 are **US4-only** (release candidate build `validate-contract-release.py build/verify-commit/verify-promotion/verify-tag`, `--require-candidate`/`--require-realization` validator modes, G0 handoff receipt validation). Lane D stop conditions forbid touching these: do not start US4, allocate a bundle version, publish/tag, edit Hermes-Install, or mark Gate G0/OpenSpec acceptance complete.

**Important discrepancy**: quickstart.md does **NOT** document Black, compileall, shell-syntax, ShellCheck, or `git diff --check` commands. Those five appear only in `specs/005-customer-subject-runtime/fable-swarm-handoff-us3.md` (lines 55–56) as gates recorded "passed" at the T051 checkpoint — "Strict OpenSpec validation, Black, compileall, POSIX shell syntax, ShellCheck, and `git diff --check`: passed" — with no exact invocations written down anywhere in the worktree. T065's checkbox only requires the quickstart-documented gates; to match the prior checkpoint's evidence bar you should also run those hygiene checks over the changed Python/shell surface and record them, but you'll have to pick the invocations (see open questions).

## 4. tasks.md — US3 checkpoint, dependencies, parallel guidance, checkbox lines

**Phase 5 header block (verbatim)**:
> ## Phase 5: User Story 3 — Upgrade Legacy Operational Evidence Safely (Priority: P2)
> **Goal**: Clean v2 initialization and v1 migration are deterministic, drift-aware, atomic, recoverable, and incapable of promoting unverifiable legacy evidence.
> **Independent Test**: PostgreSQL 15 and 16 clean apply/reapply, one/two-subject migration, concurrent write, crash/retry, identical concurrent runner, changed input, reconciliation, security drift, and quarantine matrices all yield the specified exact outcomes.

**US3 checkpoint line (verbatim, follows T065)**:
> **Checkpoint**: Fresh and legacy installations have deterministic, fail-closed PostgreSQL realization evidence.

**Phase-dependency note (verbatim)**:
> **US3 (T052–T065)**: depends on the US2 v2 PostgreSQL base; test, mapping, digest, quarantine, and fixture lanes may start in parallel.

**Within-story dependencies (verbatim)**:
> **US3**: T052–T055 precede implementation; T059 depends on T056–T057 and the US2 SQL base; T060 follows T059; T061 depends on the realized base/migration security surface; T063 depends on T056–T062; T064 follows passing evidence; T065 follows T064.

**Parallel Execution Example — User Story 3 (verbatim)**:
```text
Security drift lane: T052 then T061
Mapping/digest lane: T053, T056, T057
Recovery lane: T054, T059
Quarantine lane: T055, T058, T060
Fixture/assertion lane: T062
```

**Shared-file ownership (verbatim, the two bullets that bind you)**:
> - The **catalog integrator** alone edits `contracts/hermes-runtime/contract-index.yaml`, `contracts/hermes-runtime/fixtures/index.yaml`, `contracts/hermes-runtime/acceptance-map.yaml`, and `contracts/hermes-runtime/evidence-register.yaml` in T014/T030/T050/T064/T077.
> - The single **PostgreSQL/migration owner** alone edits `contracts/hermes-runtime/hermes-operational-postgres-v2.sql` in T048→T049 and T059, `contracts/hermes-runtime/migrations/v1-to-v2.sql` in T059→T060, and the dedicated migration runner in T059; no parallel lane edits either production SQL file.

**Notes section (verbatim)**:
> - `[P]` means safe file ownership, not permission to ignore dependencies.
> - Tests must fail for the intended missing behavior before implementation and must pass without weakening the fixture expectation.
> - Docker/image or required Git-object unavailability is a failed gate, never a skip.
> - Version allocation, release metadata, `origin/main` promotion, and tagging are serialized realization work only.
> - Gate G0 remains open until T084; completion of US1 alone does not authorize codexFactory multi-Project implementation.

**US3 checkpoint commit contents** (from `fable-swarm-handoff-us3.md`, Lane D + closing paragraph): Lane D "Runs the combined US1/US2/US3 strict gate and creates the US3 checkpoint commit", and the swarm pauses "after T065 with a clean US3 checkpoint commit, exact PostgreSQL 15/16 evidence, strict OpenSpec/validator results, and a list of any remaining P1/P2 finding." The T051 precedent for "strict validator results" recorded: catalog-member/schema/fixture counts, collected test-node count, 17 requirements / 85 scenarios, per-major matrix pass counts, source-identity and matrix digests, plus the hygiene gate list.

**Exact checkbox lines T052–T065** (currently all unchecked; flip `[ ]` → `[x]` as completed):
```markdown
- [ ] T052 [P] [US3] Write failing preflight/apply/postflight clean-apply, verified-reapply-without-repair, fresh-v2/v1-cutover profile, and independent missing/extra/altered table, column, constraint, index, policy, function, trigger, role, membership, ownership, ACL, RLS, search-path, PUBLIC, trusted-schema, durable-v1-freeze, quarantine, and dependency-guard fingerprint tests in `tests/hermes_runtime_contracts/postgres/test_clean_apply.py` and `tests/hermes_runtime_contracts/postgres/test_ddl_drift.py`
- [ ] T053 [P] [US3] Write failing detached mapping-payload/authority-envelope schema and digest tests; exact binary framing golden vectors; forged/revoked/wrong-scope `run_migration` authority and inactive trust-chain tests; canonical-JSON staging handoff; logical-versus-physical boundary behavior; one/two-subject/default-map; all-twelve-table exactly-one compatibility-history/quarantine row and ID preservation; and PostgreSQL-major parity tests in `tests/hermes_runtime_contracts/postgres/test_migration.py`
- [ ] T054 [P] [US3] Write failing pre-lock/post-lock concurrent-v1-write and durable-freeze tests; installation-plus-migration-ID session-lock concurrency; crash/abandon/retry; committed-success-before-client-ack; changed payload/authority/logical-boundary; permitted changed physical snapshot after rollback; terminal success; and reconciliation tests in `tests/hermes_runtime_contracts/postgres/test_migration_recovery.py`
- [ ] T055 [P] [US3] Write failing quarantine read/reference/promotion and authoritative-FK/view boundary tests in `tests/hermes_runtime_contracts/postgres/test_quarantine.py`
- [ ] T056 [P] [US3] Implement the typed detached expected-content mapping payload, separately digest-bound `run_migration` authority envelope, source catalog/count/dataset expectations, subject and installation-admin mappings, target topology, single-default proof, and exact binary digest-profile contract in `contracts/hermes-runtime/migrations/v1-to-v2-mapping.schema.yaml`
- [ ] T057 [P] [US3] Implement canonical payload/authority-envelope normalization and digests; exact `xfactory-v1-dataset-binary-v1` magic/tag/u64-length framing with closed column type/nullability/primary-key-position metadata, bytewise table/framed-PK ordering, schema-ordinal typed values, exact timestamp/binary/arbitrary-precision-JSON rules; logical-boundary derivation; active approver-grant/policy/scope/anchor verification; and validated canonical-JSON staging handoff plus golden vectors in `scripts/hermes_runtime_validation/migration.py`, `scripts/hermes-runtime-dataset-digest.py`, and `tests/hermes_runtime_contracts/postgres/fixtures/digest-golden-vectors.yaml`
- [ ] T058 [P] [US3] Implement the closed non-authoritative legacy quarantine record contract in `contracts/hermes-runtime/legacy-quarantine-record.schema.yaml`
- [ ] T059 [US3] Implement the base v2 `legacy_jobs`, `legacy_job_runs`, `legacy_job_events`, `legacy_workers`, `legacy_groups`, `legacy_profiles`, `legacy_group_memberships`, `legacy_github_team_mappings`, migration staging/attempt/event/reconciliation, and quarantine security structures; validated-staging-only input; one session advisory lock on installation plus migration ID across attempt/authoritative/recovery transactions; SERIALIZABLE fixed-order locks over the exact twelve v1 tables; database-recomputed logical boundary and physical cutover envelope; scoped non-authorizing compatibility-history migration; all-row exactly-one reconciliation; durable successful v1 write freeze; exact retry convergence; and changed payload/authority/logical-boundary rejection in `contracts/hermes-runtime/hermes-operational-postgres-v2.sql`, `contracts/hermes-runtime/migrations/v1-to-v2.sql`, and `scripts/run-hermes-v1-to-v2-migration.sh`
- [ ] T060 [US3] Implement quarantine-only preservation for unverifiable legacy artifact/approval-request/approval/trace rows, immutable closed records, no runtime/control/audit direct access, no authoritative FK/view/materialized-view/function/gate dependency, DDL dependency rejection, no in-place promotion, and new-governed-record-only exit rules in `contracts/hermes-runtime/migrations/v1-to-v2.sql`
- [ ] T061 [US3] Implement the locked preflight/apply/postflight boundary plus deterministic fresh-v2 and v1-cutover PostgreSQL catalog fingerprinting and missing/extra/altered readiness for tables, columns, constraints, indexes, policies, functions, triggers, role attributes/memberships, owners/ACLs, RLS flags, security-definer/search-path configuration, PUBLIC privileges, trusted-schema writability, migration/compatibility-history/quarantine objects, durable v1 freeze, and quarantine grants/dependency guard in `scripts/apply-hermes-runtime-postgres-v2.py` and `scripts/validate-hermes-runtime-postgres.py`
- [ ] T062 [P] [US3] Add deterministic all-twelve-table v1 seeds, detached payload/authority envelopes, logical/physical boundary vectors, compatibility-history and quarantine classifications, session-lock concurrency barriers, before/after-lock writes, durable-freeze probes, crash/ack-loss points, drift mutations, quarantine dependency inputs, and expected SQL assertions under `tests/hermes_runtime_contracts/postgres/fixtures/migration/` and `tests/hermes_runtime_contracts/postgres/assertions/migration/`
- [ ] T063 [US3] Run and make green the complete clean-apply, drift, migration, recovery, and quarantine matrix on both digest-pinned PostgreSQL majors through `scripts/run-hermes-runtime-postgres-tests.sh`
- [ ] T064 [US3] Register migration mapping/quarantine schemas, migration SQL, lifecycle, recovery, image-lock, structural/security drift cases, and evidence in `contracts/hermes-runtime/contract-index.yaml`, `contracts/hermes-runtime/fixtures/index.yaml`, `contracts/hermes-runtime/acceptance-map.yaml`, and `contracts/hermes-runtime/evidence-register.yaml`
- [ ] T065 [US3] Run the combined US1/US2/US3 strict validator, non-PostgreSQL pytest, PostgreSQL 15/16 matrix, and OpenSpec gate documented in `specs/005-customer-subject-runtime/quickstart.md`
```
(T001–T051 are all `[x]`; T066–T084 are `[ ]` and out of scope for Lane D.)

## Open questions
- Exact invocations for the Black / compileall / POSIX shell-syntax / ShellCheck / `git diff --check` hygiene gates are not documented anywhere in the worktree — fable-swarm-handoff-us3.md only records them as 'passed' at the T051 checkpoint. Lane D must choose invocations (e.g. `.venv/bin/python -m black --check` over changed Python, `python -m compileall`, `bash -n` / `shellcheck` over the three new/changed shell scripts) or recover them from the T051 commit/session evidence.
- Whether T064 should extend the existing `postgres-us2-governed-isolation-matrix` database case's source_paths/test_modules or add a separate `postgres-us3-*` database-phase case for HGR-008; the fixture-index shape supports either, and no convention is written down. Related: whether the runner's evidence JSON schema (single `matrix` object with one `case_id`) supports two matrix cases per major, or whether the US2 case must absorb the US3 surface.
- Whether T064 adds a `us3_binding_status` header field to acceptance-map.yaml and evidence-register.yaml, or updates the existing `us1_binding_status`/`us2_binding_status: partial` values — no rule is documented for either action.
- quickstart.md §3 passes `--domain-repo-root "$DOMAIN_REPO_ROOT"` referencing `fixtures/domain-regression-inventory.yaml`, but that inventory is a US4 deliverable (T072). Confirm whether the strict validator at the US3 gate still requires DOMAIN_REPO_ROOT (T051 evidence suggests the strict run already worked, so mirrors were presumably prepared; verify before running).
- Whether test-side fixtures created by US3 lanes (e.g. `tests/hermes_runtime_contracts/postgres/fixtures/digest-golden-vectors.yaml` from T057) belong in fixtures/index.yaml or only in the database case's source_paths — the US2 precedent indexes only contracts/hermes-runtime/fixtures/** as cases and lists test-side files under database.source_paths.