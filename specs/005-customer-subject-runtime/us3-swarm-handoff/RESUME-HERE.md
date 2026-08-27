# Fable Swarm Handoff: Gate G0 US3 — RESUME AFTER SESSION-LIMIT INTERRUPT

Status: record

## 0. What this is

The US3 swarm (T052–T065 of `add-hermes-customer-subject-runtime-contract`)
was launched, ran ~29 minutes across three parallel lanes, and was killed
mid-flight when the account hit its session token limit (all three lane agents
errored with `You've hit your session limit · resets 11:20pm UTC`). This
document is the authoritative resume point for a fresh session — on this
machine or a different one.

This directory (`specs/005-customer-subject-runtime/us3-swarm-handoff/`) is
self-contained and travels with the repository. It supersedes the /tmp
scratchpad the original session used (that scratchpad is session-local and
must NOT be relied on). It contains:

- `RESUME-HERE.md` — this file (current state + resume plan + procedures)
- `shared-interface-contract.md` — the frozen cross-lane interface (the "SIC"):
  every table/function signature, byte format, file-ownership rule, and output
  contract. **This is the single most important reference — read it in full.**
- `integration-decisions.md` — nine coordinator decisions (D1–D9) resolving
  ambiguities the SIC surfaced (canonical-JSON profile split, schema
  placement, catalog topology, evidence regeneration order, gate list).
- `briefs/` — five deep-read briefs of the existing code surface (v1 DDL,
  v2 SQL conventions, test harness, validator/schema dialect, catalog shapes).
  Regenerable by re-reading the repo, but provided so you don't have to.
- `us3-wip.patch` — a git patch capturing ALL uncommitted work-in-progress
  (see §3). This is the ONLY carrier of the partial lane output if you transfer
  via a fresh git clone.

## 1. TL;DR

- The 5-hour limit **has reset** (reset was 23:20 UTC; interrupt assessed at
  23:47 UTC). You may re-run the swarm immediately.
- Roughly **30% of the implementation landed** before the kill: 2 of Lane A's
  5 deliverables, 1 of Lane B's 4, **0 of Lane C's** (the entire production-SQL
  surface — the largest lane — is untouched).
- Everything that landed **compiles**, but **none of it is verified** (the
  agents died before self-verification). Treat all three landed files as
  *starting drafts to review against the SIC*, not as done.
- The branch itself is unchanged at the original handoff commit; all partial
  work is uncommitted working-tree state.

## 2. Authoritative locations

- OpenSpec change: `openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/`
- Speckit feature: `specs/005-customer-subject-runtime/`
- Executable tasks: `specs/005-customer-subject-runtime/tasks.md`
- Original US3 mission + stop conditions:
  `specs/005-customer-subject-runtime/fable-swarm-handoff-us3.md`
- Host worktree (original session):
  `/home/brett/projects/xFactory/openxFactory-worktrees/005-customer-subject-runtime`
- `py-bench` worktree (original session):
  `/workspace/projects/xFactory/openxFactory-worktrees/005-customer-subject-runtime`

On a different system, "the worktree root" is wherever you check out branch
`005-customer-subject-runtime`. Any absolute path in the SIC/briefs/decisions
should be read relative to that root. Run all repository commands from the
`py-bench`-equivalent checkout. Do not write absolute paths into committed
repository content other than these record docs.

## 3. Exact current state

Branch: `005-customer-subject-runtime`
HEAD: `06a98aaeac54942af4f862efffd66cbd87030692` ("Document Fable swarm US3 handoff")
(unchanged — nothing was committed by the swarm)

Uncommitted working-tree changes (all captured in `us3-wip.patch`):

| File | Origin | State |
|---|---|---|
| `tests/hermes_runtime_contracts/postgres/conftest.py` | Coordinator | **Trusted.** Adds fixtures `postgres_empty_database`, `postgres_v1_database`, `private_postgres_cluster` and constants `CANONICAL_DDL_V1`, `MIGRATION_SQL`, `MIGRATION_FIXTURE_ROOT`, `MIGRATION_ASSERTION_ROOT`. black-clean; collection verified. |
| `tests/hermes_runtime_contracts/postgres/fixtures/isolation/00-cluster-roles.sql` | Coordinator | **Trusted.** Adds `hcs_migrator` login (member of `xfactory_v2_migrator`). |
| `scripts/hermes_runtime_validation/migration.py` | Lane A | **UNVERIFIED, 1474 lines.** Full SIC §8 public API is present (dataset_stream, dataset_digest, mapping/authority/logical-boundary digests, catalog_digest, table_frame_digest, validate_*, build_staging_document, loaders, MigrationContractError). Compiles. NOT checked for byte-correctness against the ratified framing, NOT run against golden vectors (none exist yet), NOT black-checked. |
| `scripts/hermes-runtime-dataset-digest.py` | Lane A | **UNVERIFIED, 153 lines.** CLI wrapper; compiles; has `__main__`. |
| `scripts/validate-hermes-runtime-postgres.py` | Lane B | **UNVERIFIED, 1454 lines.** Fingerprint/readiness validator; compiles; has `__main__`. NOT run against a live database. |

NOT written (session died first) — the resume workload:

**Lane A remainder** (T056, T058, T057-partial):
- `contracts/hermes-runtime/migrations/v1-to-v2-mapping.schema.yaml`
- `contracts/hermes-runtime/legacy-quarantine-record.schema.yaml`
- `tests/hermes_runtime_contracts/postgres/fixtures/digest-golden-vectors.yaml`
  (the hand-derived byte-exact vectors — the crux of proving migration.py)
- `tests/hermes_runtime_contracts/postgres/test_migration.py` (T053)

**Lane B remainder** (T061-partial, T052):
- `scripts/apply-hermes-runtime-postgres-v2.py`
- `tests/hermes_runtime_contracts/postgres/test_clean_apply.py` (T052)
- `tests/hermes_runtime_contracts/postgres/test_ddl_drift.py` (T052)

**Lane C — ENTIRELY UNSTARTED** (T054, T055, T059, T060, T062):
- `contracts/hermes-runtime/hermes-operational-postgres-v2.sql` — **not touched**;
  the migration ledger/legacy/quarantine DDL, functions, freeze, and dependency
  guard must be appended (SIC §5).
- `contracts/hermes-runtime/migrations/v1-to-v2.sql` (new)
- `scripts/run-hermes-v1-to-v2-migration.sh` (new)
- `tests/hermes_runtime_contracts/postgres/test_migration_recovery.py` (T054)
- `tests/hermes_runtime_contracts/postgres/test_quarantine.py` (T055)
- `tests/hermes_runtime_contracts/postgres/fixtures/migration/*` (T062)
- `tests/hermes_runtime_contracts/postgres/assertions/migration/*` (T062)

**Lane D — not started** (T064): register everything in the four catalogs;
see `integration-decisions.md` D3–D5 and `briefs/brief-catalogs-gates.md`.

Task checkboxes: T001–T051 `[x]`; T052–T065 all still `[ ]`.

## 3.1 State after the SECOND interrupt (2026-07-13)

The resume swarm launched from WIP baseline `f78d1c1` was also killed
mid-flight. §3 above is now STALE; this section supersedes it. All of the
following landed as uncommitted work on top of `f78d1c1` (committed as the
second WIP baseline immediately after this addendum; nothing pushed):

- **Lane A — all deliverables present, none verified**: reworked
  `scripts/hermes_runtime_validation/migration.py` (+195 lines over the
  audited draft), `scripts/hermes-runtime-dataset-digest.py`, both schemas
  (`migrations/v1-to-v2-mapping.schema.yaml`,
  `legacy-quarantine-record.schema.yaml`),
  `tests/…/postgres/fixtures/digest-golden-vectors.yaml` (411 lines),
  `tests/…/postgres/test_migration.py` (1222 lines), plus
  `tests/hermes_runtime_contracts/test_migration_contracts.py` (758 lines,
  non-postgres schema/contract tests). Compiles; golden-vector independence
  (hand-derived, not generated) NOT yet audited; tests never run.
- **Lane B — all deliverables present, none verified**:
  `scripts/validate-hermes-runtime-postgres.py` (updated),
  `scripts/apply-hermes-runtime-postgres-v2.py` (336 lines),
  `tests/…/postgres/test_clean_apply.py`, `tests/…/postgres/test_ddl_drift.py`.
  Compiles; never run against a live database.
- **Lane C — roughly half**: `hermes-operational-postgres-v2.sql` extended
  +2593 lines and `contracts/hermes-runtime/migrations/v1-to-v2.sql`
  (864 lines) written. MISSING: `scripts/run-hermes-v1-to-v2-migration.sh`,
  `tests/…/postgres/test_migration_recovery.py` (T054),
  `tests/…/postgres/test_quarantine.py` (T055), and the entire
  `tests/…/postgres/fixtures/migration/` + `assertions/migration/` trees
  (T062).
- **Lane D (T064), T063 matrix, T065 gate — untouched.** Task checkboxes
  T052–T065 all still `[ ]`.

Resume shape for the NEXT session: Lanes A and B become audit+verify lanes
(hostile SIC audit, then actually run their tests against live databases);
Lane C audits its landed SQL then finishes its five missing surfaces. The
§6 plan then continues unchanged from step 5 (Lane D → matrix → gate →
review → single squashed checkpoint commit; both WIP baselines get squashed
away per D9).

## 3.2 State after the resume swarm completed (2026-07-13, later)

The three-lane resume swarm (run `wf_98c9905d-857`) COMPLETED. All lanes
report complete-verified: Lane A 18/18 (test_migration.py) on PG15+16 with
golden vectors independently re-derived byte-for-byte; Lane B 44/44
(clean-apply + drift) on both majors; Lane C 28/28 (recovery + quarantine)
on both majors plus a full live end-to-end cutover and SQL/Python digest
byte-parity proofs. US2 regression smoke clean. Committed as the third WIP
baseline immediately after this addendum.

Remaining integration work: (1) resolve Lane B's v1-cutover profile-scope
finding (runner-migrated databases carry migration helper functions/grants
absent from the derived profile expectation — needs a live probe + coordinator
disposition; Lane B's related "P1 freeze cannot run" claim is refuted by
Lanes A/C full-path runs — their probe omitted migrations/v1-to-v2.sql);
(2) Lane D T064 catalog registration (exact entries pinned in both lanes'
cross_lane_requests, in the workflow journal); (3) T063 both-majors matrix
with evidence regeneration after source freeze; (4) T065 combined gate;
(5) adversarial P1/P2 review; (6) single squashed checkpoint commit per D9.
Parked for the stop-gate findings list: Lane C's P3 (re-migration under a
new migration id on an already-frozen database succeeds by design) and Lane
B's two documented P2 design limits (rogue xfactory_v2_% cluster role
invisible to scratch-diff; unscoped-schema extras tolerated on reapply).

## 3.3 Checkpoint landed (2026-07-13)

Endgame executed: leaked adv-review container reaped; T063/T065 checkboxes
flipped; T065 combined gate re-run GREEN (OpenSpec 24/24; strict validator
34/27/79/17/85 + 637 collected; non-PG pytest 337 passed; PG matrix 152/major
pass on 15+16 with matching digests; black/compileall/shellcheck/git-diff
clean). Adversarial review completed: finders produced 11 findings; the
verification phase was killed by the session limit, so findings were verified
inline (live PG probes + static). Dispositions are in
[us3-review-findings.md](us3-review-findings.md) — 1 P1 (cutover snapshot
predates locks; probe-confirmed data-stranding), 1 P2 contract drift (migrator
role_class), plus coverage/edge P2/P3s. NONE fixed in the checkpoint: every
source change invalidates the frozen green evidence, and the P1 fix widens a
ratified security grant — Brett's ratify call. The four WIP baselines
(f78d1c1, 44a249f, d0b9ae9, 0bfda0a) were squashed into the single US3
checkpoint commit `11c25d9` per D9. Then the F-P1 (data-stranding) and F-1
(role_class) fixes were RATIFIED and implementation began (§3.4).
Superseded by §3.4.

## 3.4 STOP-AND-REGROUP: ratified F-P1/F-1 fix in flight (2026-07-13)

Committed as WIP baseline on top of `11c25d9` (nothing pushed). The eight
ratified changes are implemented and the P1 is PROBE-VERIFIED fixed, but the
evidence is NOT yet valid — one clean matrix re-run from a frozen source is
required before this can fold into the checkpoint.

### What was done (all in the WIP baseline commit)
- **F-P1 (D11) — data stranding, probe-confirmed FIXED.** The runner
  (`scripts/run-hermes-v1-to-v2-migration.sh`) now issues the twelve
  `LOCK TABLE public.hermes_* IN SHARE ROW EXCLUSIVE MODE` as top-level
  utility statements (bytewise order) right after `BEGIN ISOLATION LEVEL
  SERIALIZABLE` and BEFORE the `SELECT execute_v1_cutover(...)`, so the
  snapshot is pinned only after all locks are held. `execute_v1_cutover`
  (in `hermes-operational-postgres-v2.sql`) now VERIFIES the locks are
  pre-held (raises `HGR-MIGRATION-V1-LOCKS-NOT-PREHELD`) instead of acquiring
  them late. `migrations/v1-to-v2.sql` grants `xfactory_v2_migrator` UPDATE on
  the twelve v1 tables (empirically the minimal privilege for a non-owner to
  take that lock on BOTH PG15 and PG16 — MAINTAIN/SELECT are insufficient;
  proved by `scratchpad/probe_lock_priv.py`). The four direct cutover call
  sites in `test_migration_recovery.py` pre-lock via the module `V1_LOCK_
  STATEMENT`, and a new regression test replays the exact race (writer commits
  during the lock wait → cutover aborts on boundary mismatch, no stranded row,
  no SUCCEEDED). Decision recorded as D11 in `integration-decisions.md`; the
  SIC §5 execute_v1_cutover pin was updated to the verify-not-acquire protocol.
  Re-running `scratchpad/probe_snapshot_race.py` now prints
  `PROBE-A VERDICT: NOT REPRODUCED — cutover aborted (boundary caught it)`.
- **F-1 — role_class drift FIXED.** `migrator` added to
  `shared-definitions.schema.yaml $defs.database_role_class.enum`.
- **F-2 / F-3 — coverage hardening.** `test_migration.py` now asserts
  quarantine `source_pk` preservation + a `source_row` content check, and a
  behavioral RLS read proving each customer scope sees exactly its own
  `legacy_jobs` rows (not zero, not the other layer's).
- Note: a concurrent actor/linter further refined some of these files
  (per-table LOCK reformatting; `RACER_JOB_CELLS` + `import copy` in
  test_migration_recovery.py to re-stage the post-race boundary; catalog
  assertions in v1-to-v2.sql). Those refinements are IN the WIP baseline and
  look correct — re-read them before extending.

### CRITICAL: evidence is inconsistent — re-run the matrix first
The T063 matrix run passed both majors (exit 0), but the source files were
edited DURING the run, so the two evidence records hashed different source
bytes: `postgres-15.json` source_identity `sha256:bc0ee61c…` vs
`postgres-16.json` `sha256:daf308b0…` (they MUST be identical — the source
inventory is major-independent). Both are 153 tests, matrix digest
`sha256:032f80fa…`. This split means the strict validator's
HGR-FIXTURE-DATABASE-RESULT-SOURCE / -SUITE checks will fail until a single
clean re-run. Do NOT trust or commit these evidence JSONs as-is.

### Resume steps (new session)
1. `git status -sb` (branch 005-customer-subject-runtime) and confirm NO source
   file has changed in the last few minutes — the surface must be FROZEN
   (`find contracts scripts tests -type f -mmin -5 -not -path '*/.git/*'`).
2. Fast sanity: `black --check` changed .py; `sh -n` + `shellcheck`
   `scripts/run-hermes-v1-to-v2-migration.sh`;
   `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
3. Re-run the full matrix ONCE from the frozen source:
   `./scripts/run-hermes-runtime-postgres-tests.sh` (both majors, ~10-15 min;
   regenerates both evidence JSONs). Expect 153 tests/major and IDENTICAL
   source_identity across the two files this time.
4. Re-run the fast gates: `scripts/validate-hermes-runtime-contracts.py
   --strict` (expect 34/27/79/17/85 + 639 collected — 637 + the new regression
   test + any F-2/F-3 node); `pytest tests/hermes_runtime_contracts
   -m 'not postgres' -q` (expect all green — the 4 test_validator_cli failures
   were only the stale-evidence guard and clear once evidence is consistent).
5. Hygiene: `git diff --check` (exclude the swarm-handoff dir).
6. Squash: `git reset --soft 11c25d9~1` is WRONG — instead squash the WIP
   baseline INTO `11c25d9` so there is still ONE US3 checkpoint commit
   (`git reset --soft 11c25d9~1` would drop the checkpoint; use
   `git reset --soft <11c25d9's parent = 06a98aa>` then re-commit once, OR
   `git commit --amend` after `git reset --soft 11c25d9`). Simplest:
   `git reset --soft 06a98aa`, stage the US3 paths explicitly (never `-A`),
   commit once with the D11 fix folded into the checkpoint message.
7. Update this doc's status and STOP per the handoff (no US4, no tag, no push).

### Verification probes (scratchpad, reusable)
- `scratchpad/probe_snapshot_race.py` — the F-P1 regression probe (expects
  NOT REPRODUCED / cutover aborted).
- `scratchpad/probe_lock_priv.py` — proves UPDATE is the minimal lock grant on
  both majors.
- `scratchpad/review-findings.json` — the 11 verified review findings.
Note: scratchpad is session-local; these will not survive to a new machine,
but the fixes and D11 fully specify the intent.

## 3.5 FINAL: ratified fixes + backlog hardening folded in (2026-07-13)

Supersedes §3.4; the §3.4 resume steps were executed to completion.
- WIP `82253f4` carried the merged two-session implementation of
  F-P1/F-1/F-2 (+ the recovery regression tests); the full eight-table F-3
  behavioral RLS test and a black reflow were its uncommitted remainder.
- Backlog findings F-5 (six drift-direction tests, 38/module/major) and F-6
  (migration-family fixture content-walk) were developed in isolated copies
  and folded in.
- One clean matrix run from the frozen source regenerated both evidence
  records — identical source_identity `sha256:b2ef44a9…` (78 members) across
  majors this time, 161 tests per major, both pass.
- Full T065 gate re-ran green: OpenSpec strict 24/24; strict validator zero
  findings (34/27/79/17/85, 655 collected); non-PG pytest 337 passed;
  black/compileall/shellcheck/sh -n/git diff --check clean.
- Resolutions recorded in [us3-review-findings.md](us3-review-findings.md);
  remaining backlog F-4, F-7..F-10 (all P3). All five WIP baselines squashed
  into the single US3 checkpoint per §3.4 step 6 / D9.
STOPPED per the handoff: no US4, no tag, no push.

## 4. How to move this to a different system

The branch carries everything through T051 plus the original handoff and THIS
handoff directory once you commit it. The partial lane work (§3) is ONLY in
the working tree and inside `us3-wip.patch` — it is not committed anywhere.
Pick one:

**A. Via git (recommended for a different machine).** On this system:
```sh
cd <worktree-root>
git add specs/005-customer-subject-runtime/us3-swarm-handoff   # carry the handoff
git commit -m "US3 swarm resume handoff (session-limit interrupt)"   # optional WIP commit
git push origin 005-customer-subject-runtime                   # OUTWARD — confirm first
```
Then on the new system: clone/fetch the branch. The handoff dir arrives via
git; recreate the partial lane work by applying the embedded patch:
```sh
cd <worktree-root>
git apply --3way specs/005-customer-subject-runtime/us3-swarm-handoff/us3-wip.patch
```
(The patch recreates all five files in §3, including the two coordinator edits.
If you WIP-committed those separately, apply only the parts you still need.)

**B. Via file copy.** Copy the entire worktree directory. The partial files are
already in place; `us3-wip.patch` is redundant but harmless.

Verify the patch applies before relying on it:
```sh
git apply --check specs/005-customer-subject-runtime/us3-swarm-handoff/us3-wip.patch
```

## 5. First commands on the resuming system

```sh
cd <worktree-root>
git status -sb                      # expect branch 005-customer-subject-runtime
git rev-parse HEAD                  # expect 06a98aa… unless you added a WIP commit
date -u                             # confirm you are past any limit reset
docker info >/dev/null && docker images | grep -i postgres   # both 15 & 16 digests present
ls .venv/bin/pytest && .venv/bin/python --version            # 3.12; pytest 9
# Confirm the partial work is present (or apply the patch per §4):
git status --short
.venv/bin/python -m py_compile scripts/hermes_runtime_validation/migration.py \
  scripts/hermes-runtime-dataset-digest.py scripts/validate-hermes-runtime-postgres.py
# Read the frozen interface and decisions before touching anything:
sed -n '1,80p' specs/005-customer-subject-runtime/us3-swarm-handoff/shared-interface-contract.md
```

Environment facts (original system; reconfirm on a new one): Docker 29.4.3
running, both PostgreSQL 15/16 images present at the digests in
`tests/hermes_runtime_contracts/postgres/images.lock.yaml`; `.venv` has
Python 3.12 + pytest 9 + PyYAML + jsonschema; `black` and `shellcheck` on PATH.
Baseline strict validator before US3: `pass (31 contracts, 25 schemas,
75 fixtures, 17 requirements, 85 scenarios, 407 tests collected)`.

## 6. Resume plan

Read `shared-interface-contract.md` (all of it) and `integration-decisions.md`
(D1–D9) first — they pin every cross-lane name/byte and are unchanged. Then:

1. **Audit the three landed files against the SIC** before extending them.
   Priority: `migration.py` — confirm the frame tags are the HEX bytes of
   SIC §4.1, the canonical-JSON handling follows decision **D2** (staging
   digests use the shipped `canonical_json` profile with control chars
   rejected; the dataset tag-`0x36` stream uses the dedicated ratified-exact
   serializer), and derived identities (§4.3) match. If it diverges, fix it —
   it is the dependency of everything else.
2. **Finish Lane A**: author the two schemas (heed **D1** — the mapping schema
   stays at `migrations/…` and must be self-contained because `..` refs are
   rejected; see `briefs/brief-validation-tooling.md`), hand-derive the golden
   vectors (byte-by-byte from the spec, NOT generated by migration.py), verify
   migration.py reproduces every vector, then write `test_migration.py`.
3. **Finish Lane B**: `apply-hermes-runtime-postgres-v2.py` (locked
   preflight/apply/postflight, SIC §9), `test_clean_apply.py`,
   `test_ddl_drift.py` (one stable finding code per drift dimension).
4. **Do Lane C from scratch** (largest): extend
   `hermes-operational-postgres-v2.sql` with the base migration surface
   (SIC §5), write `migrations/v1-to-v2.sql`, the session-locked
   `run-hermes-v1-to-v2-migration.sh`, the recovery/quarantine tests, and the
   deterministic migration fixtures/assertions (whose YAML mirrors must equal
   the SQL seeds value-for-value). Lane C is the sole editor of both
   production SQL files.
5. **Lane D** (T064): register per `integration-decisions.md` D3–D5 and
   `briefs/brief-catalogs-gates.md` — extend the single existing database case,
   flip HGR-008-S01..S08 evidence entries in place, update the pinned
   `test_current_fixture_index_preserves_75_cases` count. No ratified-spec
   edits (17/85 unchanged).
6. **Green the matrix** (T063): `./scripts/run-hermes-runtime-postgres-tests.sh`
   both majors. This regenerates `evidence/postgres-15.json` / `-16.json` —
   only after the SQL/runner/fingerprints/fixtures/source-path inventory are
   frozen (D6). The T051 baseline digests WILL change.
7. **Combined gate** (T065): run §7 below; fix to zero findings.
8. **Adversarial review** for P1/P2 findings, then the single US3 checkpoint
   commit (D9), then STOP.

Whether to re-run as a fresh Workflow swarm or drive the lanes inline is your
call. If re-swarming, the lane prompts are reconstructable from the SIC + the
task text; keep the same file-ownership partition (A/B/C/D). Consider running
Lane C first or alone (it is the critical path and the only production-SQL
owner) and reusing the audited Lane A/B output rather than regenerating it.

## 7. T065 combined gate (from `integration-decisions.md` D7)

From the worktree root:
```sh
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
.venv/bin/python scripts/validate-hermes-runtime-contracts.py --strict
.venv/bin/python -m pytest tests/hermes_runtime_contracts -m 'not postgres' -q
./scripts/run-hermes-runtime-postgres-tests.sh          # both majors, digest-pinned
# Hygiene (match the T051 evidence bar):
black --check <changed .py>
.venv/bin/python -m compileall -q <changed .py>
sh -n <new .sh> && shellcheck <new .sh>
git diff --check
```
`DOMAIN_REPO_ROOT` is NOT required pre-US4 (the T051 baseline ran without it).
Docker/image unavailability is a failed gate, never a skip.

## 8. Stop conditions (unchanged from the original handoff)

Do NOT: start US4 or allocate a bundle version; publish or tag openxFactory;
edit `opensoft/xFactory-Hermes-Install`; mark OpenSpec acceptance or Gate G0
complete; treat compatibility-history rows as executable jobs or authorizing
evidence; regenerate final PostgreSQL evidence while its declared source paths
are still changing; hand-edit the evidence JSONs. Pause after T065 with a clean
US3 checkpoint commit, exact PostgreSQL 15/16 evidence, strict OpenSpec/validator
results, and a list of any remaining P1/P2 findings.

## 9. Checkpoint commit procedure (coordinator, after all green + review)

Single commit on `005-customer-subject-runtime`, explicit-path staging only
(`git add <each file>`; NEVER `git add -A` — the shared checkout carries other
sessions' work). Message style matching `6418fde` ("Implement …"). Body records
the strict-validator counts, per-major matrix counts, source-identity and
matrix digests, hygiene-gate results, and any remaining P1/P2 findings.
**Delete this `us3-swarm-handoff/` directory (or exclude it) before that clean
checkpoint commit** unless you deliberately want the swarm record retained —
if retained, keep `Status: record` and expect the strict/doc-health gates to
scan it. Then STOP: no US4, no tag, no push unless explicitly asked.
