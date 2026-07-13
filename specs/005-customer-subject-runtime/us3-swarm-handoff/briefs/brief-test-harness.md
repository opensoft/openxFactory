# Hermes Runtime PostgreSQL Test Harness — Engineering Brief

Worktree root: `/workspace/projects/xFactory/openxFactory-worktrees/005-customer-subject-runtime/` (all paths below relative to it).
Harness dir: `tests/hermes_runtime_contracts/postgres/`. Runner: `scripts/run-hermes-runtime-postgres-tests.sh`. Identity logic: `scripts/hermes_runtime_validation/fixtures.py`.

## 1. Connection model, container lifecycle, DDL application

**There is no Python database driver.** The module docstring of `postgres/conftest.py` says so explicitly: everything goes through the Docker/Compose subprocess boundary. All SQL runs as `docker compose exec -T postgres sh -ceu '...psql...'` with SQL piped on **stdin**.

Key constants in `postgres/conftest.py`:
- `REPOSITORY_ROOT = Path(__file__).resolve().parents[3]`, `POSTGRES_ROOT`, `COMPOSE_FILE`, `IMAGE_LOCK_FILE`
- `CANONICAL_DDL = REPOSITORY_ROOT / "contracts/hermes-runtime/hermes-operational-postgres-v2.sql"`
- `ISOLATION_FIXTURE_ROOT = POSTGRES_ROOT / "fixtures/isolation"`, `ISOLATION_ASSERTION_ROOT = POSTGRES_ROOT / "assertions/isolation"`
- `BASE_DATABASE = "hermes_runtime_contracts"`, `BOOTSTRAP_USER = "hermes_runtime"`

**Major selection:** `_selected_postgres_majors()` reads env `HERMES_RUNTIME_POSTGRES_MAJOR`; empty → `("15","16")` (both majors run as session params); must be exactly `15` or `16` else `pytest.UsageError`. The runner sets this per major.

**Session-scoped cluster:** `@pytest.fixture(scope="session", params=_selected_postgres_majors()) def postgres_cluster(request, run_postgres_subprocess) -> Iterator[PostgresCluster]`:
1. Asserts `CANONICAL_DDL.is_file()` (RED boundary).
2. Loads `images.lock.yaml`, takes `lock["images"][major]["resolved_image"]`, asserts it matches `postgres@sha256:[0-9a-f]{64}` (digest-pinned; lock currently pins postgres:15 and :16, linux/amd64).
3. Generates `EphemeralCredential("POSTGRES_PASSWORD", secrets.token_urlsafe(36))` and project name `f"hcs-us2-{major}-{os.getpid()}-{secrets.token_hex(4)}"`.
4. `docker image inspect <image>` must succeed — **tests fail hard, they do not skip, if the image isn't already pulled**.
5. `cluster.compose("up", "--detach", "--wait", "postgres", timeout=90)`, then a TCP-readiness poll: up to 30× `cluster.psql(BASE_DATABASE, "SELECT 1;")` with `time.sleep(0.2)` (Compose healthcheck probes the Unix socket; the harness proves the TCP path).
6. Applies the **entire v2 DDL once** into `BASE_DATABASE` via `cluster.psql(BASE_DATABASE, CANONICAL_DDL.read_text(...), timeout=90)`.
7. Applies `fixtures/isolation/00-cluster-roles.sql` (cluster-wide login roles) once.
8. Teardown (finally): `cluster.compose("down", "--volumes", "--remove-orphans", timeout=90)` and asserts it succeeded.

**Per-test database:** function-scoped `postgres_database(request, postgres_cluster) -> Iterator[PostgresDatabase]`:
- Name: `f"hcs_{major}_{sha256(request.node.nodeid)[:12]}"`.
- Runs against database `postgres`: `pg_terminate_backend` for stragglers, `DROP DATABASE IF EXISTS`, then `CREATE DATABASE "<name>" TEMPLATE "hermes_runtime_contracts"` — i.e. the v2 schema is cloned, not re-applied, per test.
- Then seeds, per test, in order: `10-two-customer-topology.sql`, `20-authority.sql`, `30-governed-evidence.sql` from `fixtures/isolation/`.
- Teardown: terminate backends + `DROP DATABASE IF EXISTS` (asserted).

**Core classes (copy these signatures):**
- `@dataclass PostgresCluster(major, image, project_name, credential: EphemeralCredential, run_subprocess)` with:
  - `environment` property → `{"COMPOSE_PROJECT_NAME", "POSTGRES_IMAGE", "POSTGRES_PASSWORD"}`.
  - `compose(*arguments: str, timeout: float = 90)` → `docker compose --file COMPOSE_FILE --project-name <p> <arguments>` from `REPOSITORY_ROOT`.
  - `psql(database: str, sql: str, *, user: str = BOOTSTRAP_USER, timeout: float = 30)` → in-container `psql -X -q -A -t -v ON_ERROR_STOP=1 -v hcs_test_password="$POSTGRES_PASSWORD" -h 127.0.0.1 -U <user> -d <database>` with SQL on stdin; password expanded only inside the container (never in host argv/evidence). Note `-A -t`: unaligned, tuples-only output.
  - `psql_file(database, path: Path, *, user, timeout)` — asserts `path.is_file()` then reads text and delegates to `psql`.
- `@dataclass(frozen=True) PostgresDatabase(cluster, name)` with `major` property and:
  - `sql(statement, *, user=BOOTSTRAP_USER, timeout=30)` → CompletedProcess
  - `file(path, *, user=..., timeout=...)`
  - `scalar(statement, *, user=...) -> str` — asserts returncode 0 and exactly one non-blank stdout line, returns it stripped.
  - `race(calls: Sequence[tuple[str, str]], *, timeout=45) -> list[CompletedProcess]` — `(user, sql)` pairs run concurrently in a `ThreadPoolExecutor(max_workers=len(calls))`; results returned in call order.
- `EphemeralCredential(environment_key, value)` with `fingerprint` (sha256 hex) property.
- `CleanupStack` — LIFO registry; `register(callback, /, *args, **kwargs)`; `close()` runs all, aggregates failures into `ExceptionGroup`. Available as function-scoped fixture `cleanup_stack`.
- Function-scoped fixtures also available but unused by current tests: `compose_project_name` (nodeid-slug + `secrets.token_hex(5)`, `hcs-` prefix, ≤38-char slug) and `ephemeral_postgres_credential` (monkeypatched `HERMES_RUNTIME_POSTGRES_PASSWORD`). These are the intended building blocks for tests needing a **private cluster**.
- Session-scoped `run_postgres_subprocess` — shell-free `subprocess.run` wrapper with deterministic env (`LC_ALL/LANG=C.UTF-8`, `TZ=UTC`, `PYTHONHASHSEED=0`), signature `run(argv, *, cwd: Path, env=None, timeout=30, input_text=None)`.

**compose.yaml:** two services on an `internal: true` network, no host ports. `postgres` service: `POSTGRES_DB=hermes_runtime_contracts`, `POSTGRES_USER=hermes_runtime`, `POSTGRES_PASSWORD` from env (required), `pg_isready` healthcheck (1s interval, 30 retries), named volume `postgres-data:/var/lib/postgresql/data`, repo mounted read-only at `/workspace`. `psql-client` service: one-shot `psql ... -c "SELECT 1"` preflight used by the runner. `test_compose_is_internal_has_no_host_port_and_uses_throwaway_storage` in `test_runner_contract.py` enforces: no `ports`, at least one healthcheck, named volumes present, all networks internal, at least one `:ro` mount — keep any compose edits within those invariants.

## 2. Fixture-loading conventions

PG fixtures are **SQL files, not YAML** (YAML fixtures belong to the non-PG phases of the suite). Conventions:
- Location: `postgres/fixtures/<topic>/NN-name.sql`, numeric prefixes define apply order (`00-cluster-roles.sql`, `10-two-customer-topology.sql`, `20-authority.sql`, `30-governed-evidence.sql`).
- Every seed file starts with `\set ON_ERROR_STOP on`.
- Cluster-wide, run-once fixtures (roles) live at `00-` and are applied in the session fixture; role passwords use the psql var injected by `psql()`: `ALTER ROLE hcs_customer_a PASSWORD :'hcs_test_password';`. Roles are created idempotently (`IF NOT EXISTS` loop) as `LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT NOREPLICATION NOBYPASSRLS`, then granted `xfactory_v2_runtime` / `xfactory_v2_control` / `xfactory_v2_audit`. Existing login roles: `hcs_customer_a`, `hcs_customer_b`, `hcs_install_admin`, `hcs_control_plane`, `hcs_reviewer_a`, `hcs_reviewer_b`, `hcs_unbound`, `hcs_audit`.
- Per-test seeds use literal deterministic data (fixed IDs like `install-01`/`stack-01`/`customer-a`/`customer-b`, padded fake digests, fixed timestamps `2026-07-12T12:00:00Z`).
- **Index registration is mandatory:** the database case `postgres-us2-governed-isolation-matrix` in `contracts/hermes-runtime/fixtures/index.yaml` (phase `database`, ~line 910) carries `database.source_paths`, `database.test_modules`, `database.seed_scripts`, `database.assertion_scripts`, `database.supported_majors: [15, 16]`, and `row_expectations`. New test modules, seed scripts, and assertion scripts MUST be appended to the respective lists. `repository_source_identity()` raises on missing files, symlinks, or duplicate entries across the four lists, and any unregistered test file breaks the evidence `test_count` check (see §5). For a new topic add e.g. `fixtures/migration/` + `assertions/migration/` files and register every one. Note the index already lists `test_topology_lifecycle.py`, `test_roles_and_rls.py`, `test_scope_pooling.py`, `test_governed_evidence.py`, `test_authorization_races.py`, `test_contract_alignment.py` — `test_runner_contract.py` is deliberately NOT indexed (it is not `postgres`-marked).
- If you add a new fixture root, mirror the conftest constants: define e.g. `MIGRATION_FIXTURE_ROOT = POSTGRES_ROOT / "fixtures/migration"` and `MIGRATION_ASSERTION_ROOT = POSTGRES_ROOT / "assertions/migration"` in `postgres/conftest.py`.

## 3. Assertion-file conventions

`postgres/assertions/isolation/*.sql` fall into two shapes:
1. **Catalog assertions** (`role-catalog.sql`, `rls-catalog.sql`, `security-definer-catalog.sql`, `evidence-immutability-catalog.sql`, `topology-catalog.sql`): a single `SELECT` over `pg_catalog` built from a `WITH expected(...) AS (VALUES ...)` list, `LEFT JOIN`ed so missing objects surface, reduced with `count(*) = N AND bool_and(...)` to one boolean. Consumed as:
   ```python
   result = postgres_database.file(_assertion("rls-catalog.sql"))
   assert_sql_succeeds(result)
   assert result.stdout.strip() == "t"
   ```
   Each test module defines its own tiny helper `def _assertion(name: str) -> Path: return ISOLATION_ASSERTION_ROOT / name`.
2. **Race/action scripts** (`project-race.sql`, `revoke-binding-race.sql`, `revoke-grant-race.sql`): full transactions meant for `PostgresDatabase.race()`. Pattern: `SET lock_timeout = '15s'; SET statement_timeout = '30s'; BEGIN; SELECT xfactory_runtime_api_v2.assume_scope(...); SELECT xfactory_runtime_api_v2.<op>(...); COMMIT;`. Loaded as text via `_sql(name)` (`path.read_text`) because `race()` takes SQL strings, not paths.
3. **Invariant probes** (`race-operation-invariant.sql`): a single SELECT concatenating counts into a `"1:1:1"`-style string, compared exactly after the race.

## 4. Markers / skip logic / env vars

- `pytest_configure` in `postgres/conftest.py` registers marker `postgres` ("requires a digest-pinned real PostgreSQL 15 or 16 container"). Every real-DB test module sets `pytestmark = pytest.mark.postgres` at module top. **New test files must do the same.**
- **There is no docker-detection auto-skip.** Selection is opt-in: the runner invokes pytest with `-m postgres` against the `postgres/` directory. Without docker/images, marked tests FAIL at the session fixture (`docker image inspect` assert), not skip. `test_runner_contract.py` carries no marker, so it runs in ordinary suites and is excluded from `-m postgres` runs.
- The runner's JUnit gate **rejects skips**: `if tests < 1 or failures or errors or skipped: exit 1`. Do not write `pytest.skip`-based tests in this directory.
- Env the runner sets for pytest: `HERMES_RUNTIME_POSTGRES_MAJOR=<major>` (narrows the session param to one major), `PYTEST_ADDOPTS=''`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, `PYTHONPATH=$repo_root[:existing]`, plus flags `-p no:cacheprovider --color=no -q -m postgres --junitxml=<tmp>`.
- Env the runner exports for its own docker steps: `POSTGRES_IMAGE` (from lock), `POSTGRES_PASSWORD` (fresh `secrets.token_urlsafe(36)`), `COMPOSE_PROJECT_NAME` (`hcs-<major>-$$-<hex5>`). Note the pytest-side conftest generates its **own** credential/project name; the runner's compose stack (up + one-shot `psql-client`) is a preflight separate from the cluster pytest creates.
- `HERMES_RUNTIME_CANDIDATE_FROZEN=1` makes `--update-image-lock` exit 2.

## 5. Runner script mechanics (`scripts/run-hermes-runtime-postgres-tests.sh`, POSIX sh, `set -eu`)

CLI: `[--major 15|16] [--json]` or `--update-image-lock` (mutually exclusive with run options; both combined → exit 2). Invalid major → exit 2 before any docker call. No `--major` → `run_one 15` then `run_one 16`.

**Evidence invalidation first:** before dependency/docker checks, it `rm -f`s `tests/hermes_runtime_contracts/postgres/evidence/postgres-<major>.json` (selected major) or both `postgres-15.json` and `postgres-16.json` (unscoped). A prior pass never survives a new attempt (contract-tested in `test_every_attempt_invalidates_selected_prior_pass_before_dependencies` and `test_unscoped_attempt_invalidates_both_prior_major_results`).

**`run_one <major>` sequence:** lookup `resolved_image` from `images.lock.yaml` via an awk `lookup_field` (glob-validated `postgres@sha256:<64 chars>`; bad pin → exit 2) → generate password + project name → `trap cleanup EXIT HUP INT TERM` (cleanup always runs `docker compose ... down --volumes --remove-orphans`, removes temp files, unsets env) → `docker image inspect` (fail → 2) → `compose up --detach --wait postgres` (fail → 1) → `compose run --rm psql-client` preflight (fail → 1) → pytest (prefers `$repo_root/.venv/bin/pytest`, else PATH; missing → 2) with the env/flags in §4 → parse JUnit XML with inline python: computes tests/failures/errors/skipped, **fails unless tests ≥ 1 and failures=errors=skipped=0**, prints the test count. All raw logs pass through `redact_log` which replaces the exact `$POSTGRES_PASSWORD` with `<redacted>`.

**Evidence JSON:** built by inline python importing `scripts.hermes_runtime_validation.fixtures`. It selects from `contracts/hermes-runtime/fixtures/index.yaml` the unique case with `phase == "database"` and `major in database.supported_majors` (must be exactly one) and emits, compact-JSON (`sort_keys=True, separators=(",",":")`):
```json
{"schema_version":1, "kind":"HermesRuntimePostgresEvidence", "major":15,
 "outcome":"pass", "image":"postgres@sha256:...",
 "source_identity": repository_source_identity(repo, case),
 "suite": {"id":"hermes-runtime-postgres", "test_count": <junit count>},
 "matrix": database_matrix_identity(case)}
```
Written atomically: `mktemp "$evidence_dir/.postgres-$major.XXXXXX"` then `mv -f` to `evidence/postgres-<major>.json`. `--json` also prints the payload to stdout.

**Matrix digest** — `database_matrix_identity(case)` in `fixtures.py`: takes `{"case_id", "requirement_ids", "scenario_ids", "database": <database mapping minus result_refs>}`, canonical-JSON-encodes (`ensure_ascii=False, sort_keys=True, separators=(",",":")`), sha256 → returns `{"profile": "xfactory-postgres-matrix-v1", "case_id": "postgres-us2-governed-isolation-matrix", "digest": "sha256:<hex>"}`.

**Source identity digest** — `repository_source_identity(repository_root, case)`: iterates the four lists **`database.source_paths`, `database.test_modules`, `database.seed_scripts`, `database.assertion_scripts`** (each must be a non-empty list; paths must be normalized relative POSIX, no `..`/`.`, no duplicates across lists, must exist as non-symlink files). For each file: `{"path": p, "digest": "sha256:" + sha256(file bytes)}`. Members sorted by UTF-8 path bytes. Payload `{"profile": "xfactory-postgres-source-inputs-v1", "matrix": database_matrix_identity(case), "members": [...]}` → canonical digest. Returns `{"identity_kind": "canonical_content", "profile": "xfactory-postgres-source-inputs-v1", "member_count": N, "digest": "sha256:..."}`. Deliberately git-independent. Current `source_paths` include all `contracts/hermes-runtime/*.schema.yaml`, the v2 SQL, `scripts/hermes_runtime_validation/{fixtures,loader}.py`, `semantics/{authority,evidence}.py`, the runner script itself, and `postgres/{compose.yaml,conftest.py,images.lock.yaml}`.

**test_count cross-check:** the acceptance validator (and `test_runner_contract.py`) recomputes `collect_database_test_count(repository_root, database, major)` — a `pytest --collect-only -q -m postgres <indexed test_modules...>` counting unique `tests/...::...` node lines — and requires equality with the evidence `suite.test_count`, which the runner derived from JUnit over the **whole postgres directory**. Consequence: **a new test file left out of `database.test_modules` makes real runs' JUnit count exceed the collected count and invalidates evidence.** Register every new module.

**`--update-image-lock`:** refuses under candidate freeze; validates `source_tag == postgres:<major>`; `docker pull --platform linux/amd64`; reads `RepoDigests[0]` via `docker image inspect --format`; rewrites `images.lock.yaml` atomically with fresh `update_evidence` for both majors.

## 6. Conventions worth copying from existing tests

- Module docstring style: `"""RED real-PostgreSQL contracts for <topic>."""`; `from __future__ import annotations`; relative import `from .conftest import (ISOLATION_ASSERTION_ROOT, PostgresDatabase, assert_sql_fails, assert_sql_succeeds)`; `pytestmark = pytest.mark.postgres`.
- Long descriptive snake_case test names stating the invariant (`test_failed_cross_layer_operation_rolls_back_every_authoritative_effect`).
- `@pytest.mark.parametrize` with explicit `ids=[...]` when the params are SQL blobs (see the immutability test: ids `["artifact", "approval-request", "decision-policy", "trace-edge"]`).
- **One psql call = one connection = one script.** Read-only probes wrap in `BEGIN; ... ROLLBACK;`; mutating flows use `BEGIN; SELECT xfactory_runtime_api_v2.assume_scope('install-01','stack-01','<layer>','<grant>'); <ops>; COMMIT;`. Scope is per-connection, so `assume_scope` must be re-run in every script.
- Result reading: `result.stdout.splitlines()[-1].strip()` for the last tuple (with `-A -t` output), or `database.scalar(...)` for single-value follow-up checks as bootstrap user.
- Failure assertions: `assert_sql_fails(result, *fragments)` — passes if ANY fragment appears case-insensitively in combined stdout+stderr; list several plausible server wordings (`"immutable", "append-only", "denied", "forbidden"`). Tolerant dual-outcome helper pattern: `_assert_zero_rows_or_denied` in `test_roles_and_rls.py` (returncode 0 with `"0"` rows OR denial fragments). RLS write tests accept "hidden row, zero-row command" for UPDATE/DELETE but then verify victim rows unchanged via `scalar`.
- Role switching is done by connecting **as** the role (`user="hcs_customer_a"` kwarg), not `SET ROLE`; `SET ROLE` appears only as an attack probe (`test_runtime_login_cannot_assume_owner_or_migrator` asserts `SET ROLE xfactory_v2_owner` fails).
- Concurrency: `postgres_database.race([(user, sql), ...])`; race scripts set `lock_timeout`/`statement_timeout` explicitly; after the race, assert **no** "deadlock"/"lock timeout" text and check an all-or-nothing invariant string (`"1:1:1"` vs `"0:0:0"`) via an invariant SQL file.
- Multi-step flows use module-private helpers taking keyword-only args (`_record_decision(database, *, user, scope_grant, decision_id, decision, reviewer_grant)`, `_approval_authorizes(database) -> str`).
- Deterministic expected values are precomputed literals (exact sha256 digests, storage keys) — no runtime hashing in assertions where a literal will do.

## 7. Shared-file edits needed for the new test topics

Minimal extension points that already exist: `PostgresCluster.compose()` (arbitrary compose subcommands → kill/stop/restart possible), `PostgresCluster.psql(database=...)` (any database name — nothing pins you to the v2 clone), `PostgresDatabase.race()` (N concurrent connections), function-scoped `compose_project_name` + `ephemeral_postgres_credential` + `cleanup_stack` + session `run_postgres_subprocess` (all the parts to assemble a **private per-test cluster**).

**a) Throwaway v1 database** — edits confined to `postgres/conftest.py` + index:
- Add a `CANONICAL_DDL_V1` constant (wherever the v1 SQL lands, presumably `contracts/hermes-runtime/hermes-operational-postgres-v1.sql`) and a new function-scoped fixture, e.g. `postgres_v1_database(request, postgres_cluster)`, mirroring `postgres_database` but `CREATE DATABASE "<name>"` **without** `TEMPLATE "hermes_runtime_contracts"` (plain create from template1/template0), then apply the v1 DDL + `fixtures/migration/*.sql` seeds. Reuse the terminate/drop create/cleanup SQL verbatim. No changes needed to `PostgresCluster`/`PostgresDatabase` — they are database-name agnostic.
- Register the v1 DDL path in `database.source_paths` (conftest.py is already indexed, so the conftest edit itself re-keys the source identity automatically).
- No compose.yaml or runner changes.

**b) Multi-connection concurrency** — `PostgresDatabase.race(calls)` already provides N independent connections (each a separate `docker compose exec` psql). For ordered interleaving across connections you cannot hold a psql session open between calls; follow the existing pattern of encoding coordination inside the SQL scripts (timeouts + atomic-outcome assertions) or, if true step-interleaving is required, add a new method to `PostgresCluster` that starts a long-lived `docker compose exec -T` psql with a pipe — that would be the only conftest.py extension needed. compose.yaml/runner: no changes (PostgreSQL default max_connections=100 is ample).

**c) Crash / ack-loss simulation** — the session `postgres_cluster` is shared across all tests of a major, so **never kill/restart it from a test**. Build a private cluster instead: instantiate `PostgresCluster(major=..., image=..., project_name=compose_project_name, credential=..., run_subprocess=run_postgres_subprocess)` inside the test (or a new function-scoped fixture, e.g. `private_postgres_cluster`, added to `postgres/conftest.py`), register teardown (`compose("down","--volumes","--remove-orphans")`) on `cleanup_stack`, then simulate crashes with `cluster.compose("kill", "postgres")` / `compose("stop", ...)` followed by `compose("up","--detach","--wait","postgres")` — the named `postgres-data` volume persists across restarts within one compose project, so WAL recovery is observable. You need the major/image: either take `postgres_cluster` just to read `.major`/`.image` (wasteful but zero-edit) or, cleaner, add a small session fixture exposing the resolved image per major (refactor lines that read `images.lock.yaml` in `postgres_cluster` into a helper, e.g. `resolved_image(major) -> str`). For ack-loss (commit acknowledged vs not), drive it with `compose kill` between two psql calls; no compose.yaml edits required unless you want a second postgres service — the current file's runner-contract invariants (§1) permit adding services so long as no `ports`, internal network, `:ro` repo mount, named volumes.
- Runner script: **no changes** for any of the three topics unless new evidence artifacts are wanted; timing note — each new test costs one `CREATE DATABASE ... TEMPLATE` clone (fast) but a private cluster costs a full container start (~seconds); the runner has no per-test timeout, only per-psql-call timeouts you pass explicitly.
- Mandatory for all new files: add each new `test_*.py` to `database.test_modules`, each `fixtures/migration/*.sql` to `database.seed_scripts`, each `assertions/migration/*.sql` to `database.assertion_scripts` in `contracts/hermes-runtime/fixtures/index.yaml`; add any new v1 DDL/contract files to `source_paths`. Missing registration = evidence `test_count`/`source_identity` mismatch, not a silent pass.

## Open questions
- Where will the v1 DDL live? No hermes-operational-postgres-v1.sql exists yet under contracts/hermes-runtime/ — its path must be agreed before CANONICAL_DDL_V1 and index source_paths registration.
- Do the new migration tests need their own evidence record / fixture-index case (a second phase:database case would break the runner's 'exactly one database case per major' selection), or do they fold into postgres-us2-governed-isolation-matrix? The runner exits 1 if len(cases)!=1 for a major, so a new case must not overlap supported_majors.
- True step-interleaved multi-connection scenarios (open transaction on connection A while connection B acts) are not expressible with one-shot psql calls; confirm whether encoding coordination inside single SQL scripts (existing race pattern) is acceptable or whether a long-lived psql pipe method must be added to PostgresCluster.
- Crash tests restarting a private cluster will re-run the DDL/seed path themselves; confirm whether the seeded state must match the isolation fixtures exactly or migration-specific seeds replace them.
- matrix.digest covers requirement_ids/scenario_ids — new tests presumably map to new HGR scenario IDs; confirm which requirement/scenario IDs the five new modules should declare in the index case.