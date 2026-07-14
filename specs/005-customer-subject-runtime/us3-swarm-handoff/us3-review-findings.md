# US3 Adversarial Review — Findings & Dispositions

Status: record

Adversarial multi-lens review of the complete US3 implementation
(commit range 06a98aa..US3-checkpoint) run 2026-07-13. Eight lens finders
produced 11 findings; the three-vote verification phase was destroyed by a
session-limit interrupt, so the coordinator verified the load-bearing findings
inline (live PG-16/PG-15 probes + static reads). This record is the
authoritative disposition. NONE of these are fixed in the checkpoint commit —
they are the documented backlog the handoff's pause condition calls for
("a list of any remaining P1/P2 finding"). Rationale for document-not-fix:
every source change invalidates the frozen green PG 15/16 evidence and forces
a full both-majors matrix regeneration (D6), the P1 fix widens a ratified
security grant (Brett's ratify call), and the checkpoint is a WIP pause with
Gate G0 still open.

## Confirmed — must fix before Gate G0 close

### F-P1 — Cutover snapshot predates the v1 table locks (data stranding)
Severity: P1 (spec-conformance / data integrity). Verified: CONFIRMED by live
PG-16 probe (`scratchpad/probe_snapshot_race.py`).
File: `contracts/hermes-runtime/hermes-operational-postgres-v2.sql`
(`execute_v1_cutover`, ~6672) and `scripts/run-hermes-v1-to-v2-migration.sh`.

Defect: the runner does `BEGIN ISOLATION LEVEL SERIALIZABLE; SELECT
execute_v1_cutover(...)`, so the transaction snapshot is taken at that SELECT,
and the `LOCK TABLE ... IN SHARE ROW EXCLUSIVE MODE` loop runs *inside* the
function (after the snapshot). A concurrent writer that holds an uncommitted
v1 row when the SELECT starts and COMMITs while the cutover blocks on the lock
is invisible to the (already-taken) snapshot yet committed to the base table.
`migration_observe_source` never sees it, reconciliation reports
`input_count=3`, the freeze is installed, and the row is stranded in the
frozen table, absent from a SUCCEEDED ledger. Probe output:
`cutover_succeeded=1, v1_hermes_jobs_rows=4, job_racer_present=1,
ledger_jobs_rows=3, ledger_job_racer_present=0, freeze_installed=1`. Violates
the ratified "Source changes during cutover" scenario (spec.md:208-211: "no
successful ledger entry may omit the row") and the before-read lock clause
(spec.md:182-184).

Exact fix (fully de-risked):
1. Acquire the twelve `LOCK TABLE public.hermes_* IN SHARE ROW EXCLUSIVE MODE`
   as a **top-level utility statement** in the runner, immediately after
   `BEGIN ISOLATION LEVEL SERIALIZABLE;` and BEFORE the `SELECT
   execute_v1_cutover(...)`. A top-level LOCK does NOT take the transaction
   snapshot; the subsequent SELECT then snapshots after all locks are held, so
   a racing writer either committed-before-lock (visible → counted, or
   boundary-mismatch abort) or is blocked-until-freeze (rejected). A LOCK
   wrapped in `SELECT fn()` does NOT work — the SELECT snapshots first.
2. Replace the in-function lock-acquire loop with a lock-VERIFY loop: raise
   `HGR-MIGRATION-V1-LOCKS-NOT-PREHELD` if the session does not already hold
   `ShareRowExclusiveLock`+ on each of the twelve tables (fail closed against
   direct misuse).
3. Grant the migrator the privilege to take that lock. **Empirically confirmed
   on both PG15 and PG16** (`scratchpad/probe_lock_priv.py`): a non-owner needs
   `UPDATE` on the table — `MAINTAIN` and `SELECT` are insufficient. So
   `GRANT UPDATE ON public.hermes_<12> TO xfactory_v2_migrator;` in
   `migrations/v1-to-v2.sql` (where both surfaces exist; already part of the
   D10 v1-cutover derived profile, so the fingerprint stays consistent). This
   WIDENS the migrator's grant surface on v1 — a ratified-contract change
   needing Brett's ratify. Mitigants: post-cutover the freeze blocks the
   migrator too; the migration protocol never issues UPDATE; the ratified
   operational model quiesces v1 in a maintenance window (research Decision 8).
4. Add the LOCK to the four direct `execute_v1_cutover` call sites in
   `test_migration_recovery.py` (~574, 729, 807, 874) and add a regression
   test replaying the probe (writer commits during the lock wait → cutover
   aborts with boundary-mismatch, no stranded row, no SUCCEEDED).
5. Regenerate both PG evidence records (D6) and re-run the full matrix.

Practical severity note: the ratified model quiesces v1 during migration, so
this is primarily a defense-in-depth gap in the automated concurrency guard
rather than a routine loss path — but strict spec conformance requires the
abort, so it is P1.

## Confirmed — contract drift, low blast radius

### F-1 — `role_class` vocabulary drift (`migrator` not in registered enum)
Severity: P2. Verified: CONFIRMED (static). SQL CHECK on
`database_principal_bindings.role_class` is `('runtime','control','audit',
'migrator')` but `shared-definitions.schema.yaml $defs.database_role_class.enum`
is `[runtime, control, audit]`, which `database-principal-binding.schema.yaml`
$refs. A governed migrator binding document (mandatory before a production
migration, and created by fixture `30-migration-authority.sql`) fails schema
validation. Fix: add `migrator` to the `database_role_class` enum (additive,
safe). Forces evidence regen (shared-definitions is a source_path).

## Confirmed — evidence/coverage gaps (behavior correct today)

- **F-2 (P2)** — quarantine/history record CONTENT never verified by the
  executed-migration tests (`test_migration.py:1041-1077`): only per-table
  counts + reason codes, and quarantine `source_pk` is not checked at all,
  though T053 promised twelve-table row-ID preservation. A transform
  regression corrupting preserved `source_row`/`source_pk`/`source_row_digest`
  would pass green. Fix: assert content, not just counts.
- **F-3 (P2)** — no behavioral RLS test on the eight `legacy_*` history tables
  via an `hcs_customer_*` login; the sole read expects `count==0`, which a
  deny-all policy also satisfies, and a cross-layer leak is exercised by
  nothing. Policy is correct today (v2.sql:~6893). Fix: add a customer-scope
  read asserting only own-layer legacy rows are visible.
- **F-4 (P3, downgraded from P2)** — no full two-runner end-to-end concurrency
  test. PARTIALLY REFUTED: lock-exclusivity is tested (`test_migration_
  recovery.py:435`) and the lock-not-held guard is tested (:432); the finder's
  own probe confirmed correct behavior. Residual: no test drives two whole
  runner processes asserting one `succeeded` + one `lock-unavailable`.
- **F-5 (P3)** — six T052 drift directions untested (constraint-extra,
  index-altered, policy-extra, trigger-extra, role-membership-missing,
  ACL-revocation). The validator's `_diff_dimension` is symmetric (verified),
  so these are likely handled; only the mutate-then-detect tests are missing.
- **F-6 (P3)** — the migration semantic fixtures (`migration/mapping-payload-*`,
  `quarantine-record-*`) are header-verified only; unlike every sibling family
  they are not content-walked by a portable-matrix test, so a malformed body
  could pass. Fix: extend the portable-fixture test to glob `migration/`.
- **F-7 (P3)** — ratified canonical-JSON DECIMAL number rules exercised by zero
  fixtures; the SQL number branch (e.g. a `hermes_jobs.envelope` with a float)
  is outside the 152-test matrix and inexpressible in the YAML corpus. Probe
  confirmed the branch is currently correct.

## Confirmed — edge / minor, contained

- **F-8 (P3)** — BC-era `timestamptz` aliases to its AD rendering in
  `migration_value_frame` (RFC 3339 cannot express BC), so the frozen-source
  digest is non-injective on BC dates instead of failing closed. Out of the
  ratified value domain; effectively impossible in v1 Hermes job data.
- **F-9 (P3)** — `migration_dataset_stream_from` accepts profile-invalid
  datasets and duplicate framed primary keys yield an order-unstable (thus
  nondeterministic) SQL digest where Python fails closed. Contained: the
  function is only used for golden-vector parity in tests; real tables have
  unique PKs.
- **F-10 (P3)** — `legacy_*`/quarantine `source_row` stores integer/bool
  columns as JSON number/boolean, not the pinned §7 text form, so a consumer
  reconstructing dataset cells from `source_row` fails migration.py's own
  `_validate_cell`. Internal inconsistency only; `source_row` is a preservation
  copy, not the digest input. DISPOSITIONED 2026-07-13: Brett approved the
  current behavior AS-IS (see Resolutions) — closed, no code change.

## Pre-disposed (fenced from re-report; unchanged)

- P3: re-migration under a NEW migration id on an already-frozen database
  succeeds by design.
- P2 design limit: a rogue pre-existing `xfactory_v2_%` cluster role is
  invisible to the scratch-diff fingerprint.
- P2 design limit: extra objects in non-`xfactory` schemas tolerated on reapply.
- D10 resolved the v1-cutover profile scope (migration SQL is part of the
  derived profile); refuted Lane B's "freeze cannot run" P1.

## Recommended follow-up

One dedicated session (not racing a limit) to: implement F-P1 (with Brett's
ratify on the migrator UPDATE grant) and F-1 together, add the F-2/F-3
behavioral assertions, then regenerate both PG evidence records and re-run the
full matrix + T065 gate. F-5..F-10 are optional hardening.

## Resolutions (2026-07-13, post-checkpoint hardening session)

Fixed and verified in the updated checkpoint commit. Brett RATIFIED the F-P1
grant widening (recorded as D11 in integration-decisions.md).

- **F-P1 FIXED.** Lock-before-snapshot protocol per D11: the runner takes the
  twelve top-level `SHARE ROW EXCLUSIVE` locks (bytewise order) before the
  cutover SELECT; `execute_v1_cutover` VERIFIES rather than acquires, raising
  `HGR-MIGRATION-V1-LOCKS-NOT-PREHELD` fail-closed;
  `migrations/v1-to-v2.sql` grants the migrator UPDATE on the twelve v1
  tables (minimal lock privilege, proven on both majors). Two independent
  implementations converged on the same fix; the original probe now prints
  NOT REPRODUCED. Regression test replays the race (writer commits during the
  lock wait → boundary-mismatch abort, no stranded row, no SUCCEEDED; a
  re-staged retry counts the racer row) plus a direct-misuse guard test.
- **F-1 FIXED.** `migrator` added to the `database_role_class` enum; a
  migrator binding validates through the offline registry; enum stays closed.
- **F-2 FIXED.** Executed-migration tests assert full content round-trip:
  every row of all twelve tables cell-for-cell against the YAML mirrors and
  every stored `source_row_digest` against an independently recomputed
  row-frame digest; quarantine `source_pk`/digest included.
- **F-3 FIXED.** Behavioral RLS test: real `hcs_customer_a/b` logins see
  exactly their own layer's rows across all eight `legacy_*` tables
  (superuser-derived ground truth; non-zero own-layer, zero foreign-layer).
- **F-5 FIXED.** All six missing drift directions now mutate-then-detect in
  `test_ddl_drift.py` (38 tests/major). Semantic note:
  `XFV2-ROLE-MEMBERSHIP-MISSING` is structurally unreachable by target
  mutation while the canonical DDL creates no role-to-role memberships; the
  direction is proven via a re-rooted byte-copy of the validator over the
  canonical DDL plus one appended grant (no repo/target/cluster mutation).
  `_membership_findings` symmetry is now proven in both directions.
- **F-6 FIXED.** The portable-fixture matrix content-walk
  (`test_artifact_approval_trace.py`) now globs the migration family: schema
  + semantic validation of all four bodies, exact primary finding codes on
  the invalid cases, reason-specific rejection proven corrupt-then-detect.

F-4 and F-7..F-9 FIXED (2026-07-14, Opus isolated-copy agents, folded in
with a fresh both-majors evidence cycle):
- **F-4 FIXED.** Deterministic two-whole-runner e2e test (blocker-transaction
  sequencing over pg_locks, no sleeps): exactly one `succeeded` winner and
  one clean `lock-unavailable` loser, single STARTED/SUCCEEDED, exactly-once
  reconciliation, loser leaves zero v2 state.
- **F-8 FIXED.** `migration_value_frame` now enforces the full AD
  proleptic-Gregorian RFC-3339 domain via immutable `make_timestamp`
  validation (rejects month-13, 30-Feb, 24:00, minute-60, leap-second forms
  the regex alone accepted), and `migration_live_cells_expression` tags BC
  instants so they fail closed with HGR-MIGRATION-DATASET-VALUE instead of
  aliasing to their AD rendering. Python cannot represent BC at all (RFC-3339
  strings only), so SQL-side fail-closed is the correct resolution.
- **F-9 FIXED.** `migration_dataset_stream_from` fails closed on duplicate
  framed primary keys (HGR-MIGRATION-DATASET-ORDER, deterministic
  count-vs-distinct detection) and duplicate column names
  (HGR-MIGRATION-DATASET-COLUMN), mirroring migration.py; golden vectors
  unchanged byte-for-byte.
- **F-7 FIXED.** Nine new SQL-side tests drive the live canonical/digest
  functions over the ratified DECIMAL edge cases with Python byte-parity
  plus the F-8/F-9 fail-closed branches. (The exponent-form guard is
  unreachable from jsonb input — PostgreSQL numeric expands exponents —
  so parity is proven over the reachable domain.)

F-10 is CLOSED as-designed — Brett approved the current `source_row`
preservation form as-is (2026-07-13): preserved records keep native JSON
scalar types; the pinned §7 text form governs the digest stream only, not
the preservation copy. Pre-disposed design limits above unchanged. All
eleven findings are now resolved or dispositioned; post-fix gate results
are recorded in the hardening commit message.
