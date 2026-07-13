# US3 Integration Decisions (coordinator log — supplements the SIC)

Recorded 2026-07-12 during Lane A/B/C execution. Binding for Lane D and the
integration pass. Numbered for citation in fix-agent prompts.

## D1. Mapping schema placement and self-containment

The ratified design pins the path `contracts/hermes-runtime/migrations/v1-to-v2-mapping.schema.yaml`.
`schema_registry._validate_reference_shape` forbids `..` and out-of-directory
relative `$ref`s, so this schema CANNOT `$ref` root-level
`shared-definitions.schema.yaml`. Resolution: keep the ratified path and make
the schema fully SELF-CONTAINED (duplicate needed primitives under its own
`$defs`). If Lane A landed it at family root instead, move it back at
integration (path, `$id`, catalog entry all `migrations/...`).

## D2. Canonical JSON — two profiles, deliberately

- Existing `xfactory_runtime_v2.canonical_json` (SQL) and
  `semantics/authority.py::canonical_record_digest` (Python `json.dumps`)
  agree byte-for-byte with each other (verified: PG `escape_json` and Python
  both short-escape \b\f\n\r\t, lowercase-\u00xx other controls, raw
  non-ASCII, code-point==C-collation key sort, minimal integers). They deviate
  from the ratified prose ONLY on the five short-escaped control characters.
- US3 staging/record digests (mapping payload, authority envelope, logical
  boundary, catalog, reconciliation): use the SHIPPED family profile (SQL
  `canonical_json` semantics) so SQL recomputation agrees with Python. To make
  the prose deviation unreachable, `validate_mapping_payload` /
  `validate_authority_envelope` and the SQL staging path REJECT control
  characters U+0000–U+001F in every string field (stable code
  `HGR-MIGRATION-CONTROL-CHARACTER`).
- Dataset stream tag-36 JSON values (and only those): ratified rules exactly,
  via DEDICATED serializers on both sides — Python in migration.py, SQL
  `xfactory_runtime_v2.migration_canonical_json_value(jsonb) returns text`
  (escapes ALL controls as lowercase \u00xx, no short escapes). Golden vectors
  must include a control-character case proving `
` (not `\n`).

## D3. Fixture-index case topology

Extend the single existing database-phase case
`postgres-us2-governed-isolation-matrix` (the runner and evidence pipeline
require exactly one database case per major): append US3 files to
`source_paths` (both new schemas, migrations/v1-to-v2.sql, updated v2 SQL is
already listed, migration.py, hermes-runtime-dataset-digest.py,
apply-hermes-runtime-postgres-v2.py, validate-hermes-runtime-postgres.py,
run-hermes-v1-to-v2-migration.sh, digest-golden-vectors.yaml, v1 DDL
contracts/schemas/hermes-operational-postgres.sql), the five new modules to
`test_modules`, migration seeds to `seed_scripts`, migration assertions to
`assertion_scripts`; add HGR-008 to `requirement_ids` and HGR-008-S01..S08 to
`scenario_ids`. Do NOT rename the case. Do NOT add a second database case.

## D4. Contract-side semantic fixtures for the two new schemas

Add valid/invalid fixture pairs under `contracts/hermes-runtime/fixtures/migration/`
(mapping-payload-valid, mapping-payload-invalid → stable code from the schema
suite, quarantine-record-valid, quarantine-record-invalid), registered as
semantic cases with quoted `evaluation_time` and `evidence_id`. Update the
pinned count test `test_fixture_index.py::test_current_fixture_index_preserves_75_cases`
(75 → 75+N). 17 requirements / 85 scenarios DO NOT change — no ratified spec
edits in US3.

## D5. Evidence register / acceptance map

Flip HGR-008-S01..S08 entries IN PLACE to `status: bound` with
`fixture_case_ids: [postgres-us2-governed-isolation-matrix]` (+ semantic case
ids where apt), real collected per-major `test_node_ids`, and the two bare
evidence-JSON `result_refs` paths. `expected_*` counts unchanged. Leave
`us1_binding_status`/`us2_binding_status` headers untouched; do not invent
`us3_binding_status` (T077 owns final status flips). acceptance-map
`openspec_parity` for HGR-008 already exists — verify, don't duplicate.

## D6. Evidence regeneration ordering (handoff mandate)

Only after production SQL, runner, fingerprints, fixtures, and the source-path
inventory are FROZEN: run `./scripts/run-hermes-runtime-postgres-tests.sh`
(both majors) to regenerate `evidence/postgres-15.json` / `postgres-16.json`.
Never hand-edit those files. The T051 digests are expected to change.

## D7. T065 gate list (quickstart §3–4 + T051-parity hygiene)

From the worktree root:
1. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`
2. `.venv/bin/python scripts/validate-hermes-runtime-contracts.py --strict`
   (DOMAIN_REPO_ROOT not required pre-US4 — the T051 baseline ran without it)
3. `.venv/bin/python -m pytest tests/hermes_runtime_contracts -m 'not postgres' -q`
4. `./scripts/run-hermes-runtime-postgres-tests.sh` (both majors, digest-pinned;
   NO --update-image-lock)
5. Hygiene: `black --check` over changed .py; `python -m compileall -q` over
   changed .py; `sh -n` + `shellcheck` over changed/new .sh;
   `git diff --check` (after staging).

## D8. tasks.md checkboxes

Flip T052–T065 `[ ]`→`[x]` as each completes; Lane D flips T052–T062 with
registration, coordinator flips T063–T065 after the green matrix + gates.

## D9. Checkpoint commit (coordinator)

Single commit on `005-customer-subject-runtime` after everything is green +
adversarial review: explicit-path staging only (`git add` each file; NEVER
`git add -A`), message style matching `6418fde` ("Implement …"), body listing
strict-validator counts, per-major matrix counts, source-identity and matrix
digests, hygiene gates, and any remaining P1/P2 findings (per the handoff's
closing paragraph). Then STOP — no US4, no tag, no push unless asked.

## D10. v1-cutover profile derivation includes the migration surface (2026-07-13)

The SIC §9 v1-cutover derivation recipe is amended to
`v2 + v1 + contracts/hermes-runtime/migrations/v1-to-v2.sql +
select xfactory_runtime_v2.install_v1_freeze('profile-derivation')`, in that
order, inside the existing single rolled-back scratch transaction.

Why: a live probe (integration phase 1) proved the original recipe reports
15 findings (3x XFV2-FUNCTION-EXTRA for the migrations-file helpers, 12x
XFV2-ACL-ALTERED for the superuser grants to `xfactory_v2_owner`) against a
database the production runner had just migrated to terminal success — i.e.
every legitimately cut-over database failed readiness, making the ratified
postflight clause ("postflight SHALL prove the selected fresh-v2 or
v1-cutover profile before success") unsatisfiable for databases produced by
the ratified protocol. The migration surface is ratified published contract
(spec.md:180) and the durable freeze exists only via that surface
(spec.md:190), so its helpers/grants are canonical post-cutover state, not
drift. Self-cleaning (option b) contradicts the idempotent-retry pins;
descoping migrated databases (option c) contradicts design.md Decision 7.
The patched recipe was probe-verified: `ready`, zero findings, against the
same migrated database. Lane B's related P1 ("install_v1_freeze cannot run
through the production cutover path") is REFUTED as stated — the probe that
produced it omitted `migrations/v1-to-v2.sql`, without which the claimed
call chain (`migration_attach_v1_freeze`) does not even exist.

Rework: Lane B validator (`CANONICAL_MIGRATION_DDL`, scratch-script append
before the freeze select, docstring), the two `test_clean_apply.py` and one
`test_ddl_drift.py` setups that build v1-cutover baselines via direct
`install_v1_freeze`, plus one new end-to-end guard test asserting a
runner-migrated database reports v1-cutover `ready`. No Lane C, ratified-spec,
or evidence edits.

## D11. F-P1 lock-before-snapshot protocol + ratified migrator UPDATE grant (2026-07-13)

Brett ratified (this session, post-checkpoint) the F-P1 fix from
`us3-review-findings.md`, including the grant widening it requires:

1. The cutover caller (the runner, and every direct test call site) acquires
   the twelve `LOCK TABLE public.hermes_* IN SHARE ROW EXCLUSIVE MODE` locks
   as TOP-LEVEL utility statements in bytewise order, immediately after
   `BEGIN ISOLATION LEVEL SERIALIZABLE;` and before
   `select execute_v1_cutover(...)`, so the transaction snapshot is pinned
   only after all locks are held (a LOCK wrapped in `select fn()` re-breaks
   the ordering — the SELECT snapshots first).
2. `execute_v1_cutover` replaces its lock-ACQUIRE loop with a lock-VERIFY
   loop: raise `HGR-MIGRATION-V1-LOCKS-NOT-PREHELD` (fail closed) unless the
   session already holds `ShareRowExclusiveLock`+ on each of the twelve.
3. `migrations/v1-to-v2.sql` adds
   `GRANT UPDATE ON public.hermes_<each of the 12> TO xfactory_v2_migrator;`
   — RATIFIED grant widening (a non-owner needs UPDATE to take that lock;
   MAINTAIN/SELECT are insufficient, empirically on PG15+16). Mitigants
   recorded in us3-review-findings.md F-P1. The migrations file is already
   part of the D10-derived v1-cutover profile, so the fingerprint follows
   automatically.
4. A regression test replays the race (writer commits during the lock wait →
   cutover aborts on boundary mismatch; no stranded row; no SUCCEEDED).

Fixed in the same session: F-1 (add `migrator` to
`shared-definitions.schema.yaml` `database_role_class` enum), F-2
(record-content assertions in the executed-migration tests), F-3 (behavioral
legacy_* RLS test via a customer login). Evidence regenerated (D6) and the
T065 gate re-run afterward; findings doc updated with resolutions.
