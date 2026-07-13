# US4 Shared Interface Contract (SIC)

Status: record

Frozen cross-lane interface for the US4 provider swarm (T066–T078). Every
name, path, constant, and signature here is pinned; lanes MUST NOT deviate
without a coordinator decision recorded in `integration-decisions.md`.
Companion to `RESUME-HERE.md` (mission/constraints) in this directory.

## §1 Lane partition and file ownership (exclusive; NEW files unless noted)

| Lane | Tasks | Owns (sole editor) |
|---|---|---|
| **J** (jobs) | T066, T070, T071 | `tests/hermes_runtime_contracts/test_v2_jobs.py`; `contracts/hermes-runtime/hermes-job-envelope-v2.schema.yaml`, `hermes-job-run-v2.schema.yaml`, `hermes-job-event-v2.schema.yaml`; `contracts/hermes-runtime/fixtures/jobs/*.yaml`; `scripts/hermes_runtime_validation/semantics/jobs.py` |
| **R** (release) | T068, T074 | `tests/hermes_runtime_contracts/test_release_inventory.py`; `contracts/releases/release-digest-inventory.schema.yaml`; `scripts/hermes_runtime_validation/release.py`; `scripts/validate-contract-release.py`; `contracts/hermes-runtime/fixtures/release/*.yaml` |
| **D** (domain regression) | T067, T072, T073 | `tests/hermes_runtime_contracts/test_domain_regression.py`; `contracts/hermes-runtime/domain-regression-inventory.schema.yaml`; `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`; `contracts/hermes-runtime/fixtures/regression/*.yaml`; `scripts/hermes_runtime_validation/domain_regression.py` |
| **H** (handoff) | T069, T075 | `tests/hermes_runtime_contracts/test_consumer_handoff.py`; `contracts/hermes-runtime/consumer-handoff-receipt.schema.yaml`; `contracts/hermes-runtime/fixtures/pins/consumer-receipt-wrong-repository.yaml` (+ any additional `fixtures/pins/handoff-*.yaml`); `scripts/hermes_runtime_validation/consumer_handoff.py` |
| **DOC** | T076 | `contracts/hermes-runtime/README.md` (edit), `docs/contract-versioning-policy.md` (edit), `docs/xfactory-domain-factory-model.md` (edit), `docs/terminology-and-repo-topology.md` (edit or create) |
| **Coordinator** | T077, T078 | `contracts/hermes-runtime/contract-index.yaml`, `fixtures/index.yaml`, `acceptance-map.yaml`, `evidence-register.yaml`; `scripts/validate-hermes-runtime-contracts.py`; `tests/hermes_runtime_contracts/test_validator_cli.py`; `tests/hermes_runtime_contracts/test_fixture_index.py`; `openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/provider-verification.yaml`; `specs/005-customer-subject-runtime/tasks.md` |

## §2 Forbidden for ALL lanes (coordinator-enforced)

1. The 78 PostgreSQL-evidence source-inventory members (RESUME-HERE.md §2) —
   notably `shared-definitions.schema.yaml` (reuse by `$ref`, never edit),
   `hermes-operational-postgres-v2.sql`, `migrations/*`, `scripts/hermes_runtime_validation/{fixtures,loader,migration}.py`,
   `semantics/{authority,evidence}.py` (import from them freely; never edit),
   everything under `tests/hermes_runtime_contracts/postgres/`.
2. The coordinator-owned files in §1 (lanes RETURN registration payloads
   instead of editing catalogs — §7).
3. Any existing test module (`test_artifact_approval_trace.py` etc.) — new
   families get NEW test modules with their own matrices.
4. `specs/005-customer-subject-runtime/us3-swarm-handoff/**` and the
   uncommitted `us3-review-findings.md` working-tree edit (concurrent session).
5. `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, `contracts/README.md`
   — release-metadata surfaces are T079 (parked for Brett).
6. No push, no tag, no version allocation, no network fetch.

## §3 Schema pins

Common (all hermes-runtime family members; enforced by `catalog.py`):
top-level `schema_version: 1`, `kind: openxfactory-hermes-runtime-contract-schema`,
`$schema: https://json-schema.org/draft/2020-12/schema`,
`$id: https://xforge.us/schemas/openxfactory/hermes-runtime/v2/<family-relative-path>`,
`contract_id` + `contract_schema_version` matching the catalog entry, `title`,
`description`. Closure via `additionalProperties: false` everywhere (never
`unevaluatedProperties`). Cross-file reuse ONLY as same-directory
`$ref: shared-definitions.schema.yaml#/$defs/<name>` (no `./`, no `..` — refs
with `.`/`..` segments are hard-rejected by `schema_registry.py`). Payload
identity asserted inside `properties` as `schema_version: {const: 1}` +
`kind: {const: <instance-kind>}`.

| File | contract_id | csv | instance `kind` const |
|---|---|---|---|
| `hermes-job-envelope-v2.schema.yaml` | `hermes-job-envelope-v2` | 2 | `openxfactory-hermes-runtime-job-envelope-v2` |
| `hermes-job-run-v2.schema.yaml` | `hermes-job-run-v2` | 2 | `openxfactory-hermes-runtime-job-run-v2` |
| `hermes-job-event-v2.schema.yaml` | `hermes-job-event-v2` | 2 | `openxfactory-hermes-runtime-job-event-v2` |
| `domain-regression-inventory.schema.yaml` | `domain-regression-inventory` | 1 | `openxfactory-hermes-runtime-domain-regression-inventory` |
| `consumer-handoff-receipt.schema.yaml` | `consumer-handoff-receipt` | 1 | `openxfactory-hermes-runtime-consumer-handoff-receipt` |

Content requirements (authoritative sources lanes MUST read: `specs/005-customer-subject-runtime/data-model.md` §§Job Lifecycle V2 / DomainRegressionEntry / HermesG0HandoffReceipt; the NJE-004 / SCO-002 / HGR-009 delta specs under `openspec/changes/add-hermes-customer-subject-runtime-contract/specs/`; `specs/005-customer-subject-runtime/contracts/{schema-inventory,release-and-consumer-pin}.md`):

- **v2 jobs**: every record requires the neutral scope tuple via
  `$ref shared-definitions.schema.yaml#/$defs/layer_scope`; reuse
  `canonical_id`, `principal_reference`, `content_resource_reference`,
  `sha256_digest`, `rfc3339_timestamp`, `extensions`, `customer_subject_ref`
  as needed. NO domain noun (project/patient/repository/feature) in any
  required property name or enum. Event: monotonic `sequence` (integer ≥ 0),
  actor `principal_reference`, `occurred_at`, schema-validated payload
  reference. `dependentRequired` couples run→job identifiers as in
  `artifact-record.schema.yaml`.
- **domain-regression-inventory**: doc fields `schema_version(const 1)`,
  `kind(const)`, `inventory_version` (int ≥1), `entries[]` (min 5) each
  `{repository (canonical_repository), commit (git_commit), stack_path
  (repository_relative_path), stack_digest (sha256_digest), domain_id
  (canonical_id), expected_contract_ref (git_commit),
  expected_contract_schema_version (int ≥1), expected_result (const "pass")}`,
  `exclusions[]` each `{repository, reason, evidence}` (min 1 for
  LegalxFactory). Bytewise-unique repositories.
- **consumer-handoff-receipt**: `consumer_repository` is
  `{const: opensoft/xFactory-Hermes-Install}`; `bundle_tag`;
  provider block (openxFactory repository/tag/peeled commit/manifest +
  inventory paths and digests); `consumer_commit` (git_commit);
  `closure_packet` `{path: const-prefixed evidence/gates/g0/<...>.yaml form,
  digest}`; recorded `compatibility_manifest`/`checker`/`runtime_binding`/
  `evidence` path+digest pairs; positive AND negative check results.
- **release-digest-inventory** (`contracts/releases/`, OUTSIDE the family
  root): **fully self-contained** (own local `$defs`; it cannot be a
  hermes-runtime catalog member and cannot `$ref` across directories). Own
  header `schema_version: 1`, `kind:
  openxfactory-contract-release-digest-inventory-schema`,
  `$id: https://xforge.us/schemas/openxfactory/releases/release-digest-inventory.schema.yaml`.
  Instance shape (planning-pinned): `schema_version: 1`, `kind:
  openxfactory-contract-release-digest-inventory`, `bundle_tag`,
  `repository: opensoft/openxFactory`, `digest_algorithm: sha256`,
  `digest_source: raw_git_blob`, `path_order: bytewise_utf8`, `entries[]`
  each `{artifact_id, path, type, git_mode ("100644"|"100755"),
  schema_id?, schema_version?, digest}`; entries unique + bytewise
  path-sorted; the inventory NEVER contains itself or any commit field.

## §4 Realized domain-regression inventory (Lane D; values verified 2026-07-13)

`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` pins the
ratified planning table EXACTLY (all commits/digests verified present in the
local checkouts; every pinned stack.yaml carries
`contract_ref: 3d51c3ed5854d112bcc049e1ef7f70863b993fa3`, schema version 1):

| repository | commit | stack_path | stack_digest |
|---|---|---|---|
| `opensoft/AdxFactory` | `d0e42622d1da51a3aa6475e2df076df4e55e7918` | `stack.yaml` | `sha256:b5ab723eac7395523a7988468076048e4d0426e03b556231dfb4c282bb8b3fc9` |
| `opensoft/LedgerxFactory` | `1b2ca4c1e66b5e90c9e983a7d0aad11c1ab5ae1c` | `stack.yaml` | `sha256:85d67c54a07f3d4e31943257cf43cb19e0fc400f39a0c719591ed30eeb140ab9` |
| `opensoft/MedxFactory` | `280fdbb5aee8cd83f5c75defd652c1a60039cd0e` | `stack.yaml` | `sha256:02e4b34528217870e982462dde4ff8624c29a7b9e61f3ab405f4710307ff6622` |
| `opensoft/OpsxFactory` | `beed3481fb7f500695bcc4394bb686fab125ad71` | `stack.yaml` | `sha256:3de89a6c7e8b9f112deb7074b8798dc17311425f819968f2f7e1c7e86c7e8fa0` |
| `opensoft/codexFactory` | `7bfa492f700de29cdeab31dc899420745546d982` | `stack.yaml` | `sha256:06f88e192bfd17d42ea6519072e472b9f6d028d88ab0985065640e37c9719722` |

Exclusion: `opensoft/LegalxFactory` — no canonical `stack.yaml` yet (reason
recorded verbatim from research Decision 12). Tests use SYNTHETIC git repos
(`support.init_git_repo`/`commit_files`); real-mirror resolution happens only
at the T078 gate via `--domain-repo-root`.

## §5 Module APIs (pinned signatures; findings = sorted `{code, severity,
case_id?, path, message}` dicts per existing semantics convention)

- `scripts/hermes_runtime_validation/semantics/jobs.py` (Lane J):
  - `validate_jobs_document(document, *, evaluation_time: str) -> list[dict]`
    — orchestrator dispatching on instance `kind`/`operation`; covers scope
    sharing, job/run/event correlation, monotonic event sequence,
    terminal-layer (retired/suspended) new-job denial, retained retired-layer
    artifact/approval/trace/audit evidence access, v1-noun exclusion.
  - May import `canonical_record_digest` from `semantics.authority` and
    lifecycle helpers from `semantics.topology` (imports only, no edits).
- `scripts/hermes_runtime_validation/domain_regression.py` (Lane D):
  - `class DomainRegressionDependencyError(RuntimeError)` with
    `exit_code = 2`, `code = "HGR-REGRESSION-DEPENDENCY"`.
  - `build_repository_resolver(mappings: Mapping[str, Path] | None, root: Path | None)`
    — canonical `owner/repo` resolves ONLY to `<root>/<owner>/<repo>` or
    `<root>/<owner>/<repo>.git`; ambiguity/missing → DependencyError.
  - `validate_domain_regression(inventory: Mapping, *, resolver) -> list[dict]`
    — exact `commit:path` blob reads via `content.resolve_git_object`, digest
    parity, expected-pin parity, per-entry stack validation, and the
    duplicate-Customer DERIVED negative (inject a second `role: customer`
    into the resolved bytes in memory; never modify domain repos).
- `scripts/hermes_runtime_validation/release.py` (Lane R):
  - `release_membership(repo_root: Path) -> list[Path]` — closed membership
    per research Decision 10 (hermes-runtime family + indexed fixtures +
    validators + `requirements/hermes-runtime-contracts.{in,lock}` +
    `tests/hermes_runtime_contracts/postgres/images.lock.yaml` + inventory
    schema + `contracts/{manifest.yaml,CHANGELOG.md,README.md}` + normative
    docs; excludes the inventory instance itself).
  - `build_release_inventory(repo_root: Path, *, bundle_tag: str) -> dict`
  - `verify_inventory_against_commit(repo_root, commit: str, inventory: Mapping) -> list[dict]`
  - `verify_promotion(repo_root, *, commit: str, remote: str, tag: str) -> list[dict]`
  - `verify_tag(repo_root, *, remote: str, tag: str) -> list[dict]`
  - `validate_candidate(repo_root, *, catalog) -> list[dict]` /
    `validate_realization(repo_root, *, catalog, remote: str = "origin") -> list[dict]`
    — the CLI-mode workhorses (coordinator wires them into the entrypoint).
- `scripts/hermes_runtime_validation/consumer_handoff.py` (Lane H):
  - `validate_handoff_receipt(receipt: Mapping, *, consumer_resolver) -> list[dict]`
    — `consumer_repository` equality check FIRST
    (`HGR-HANDOFF-CONSUMER-REPOSITORY`, before ANY object lookup), then exact
    `commit:path` reads of the closure packet and every recorded artifact.
  - `build_consumer_resolver(mappings, root)` — same deterministic-root rules
    as Lane D (share the shape, duplicate the small logic; do NOT create a
    shared module both lanes edit).
- `scripts/validate-contract-release.py` (Lane R): thin CLI over `release.py`.
  Subcommands exactly `build --tag <tag> --output <path>`,
  `verify-commit --commit <sha>`,
  `verify-promotion --commit <sha> --remote <name> --tag <tag>`,
  `verify-tag --remote <name> --tag <tag>`; `--json` on all. Exit codes:
  0 pass, 1 findings, 2 dependency/harness (mirrors
  `validate-hermes-runtime-contracts.py::classify_exit_code`).

## §6 Finding codes, fixture conventions

- Namespaces (pattern `^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$`): Lane J
  `HGR-JOB-*`; Lane R `HGR-RELEASE-*`; Lane D `HGR-REGRESSION-*`; Lane H
  `HGR-HANDOFF-*` (the wrong-product code is EXACTLY
  `HGR-HANDOFF-CONSUMER-REPOSITORY`). Harness/dependency reuse `HRC-*` only
  inside the CLI entrypoints.
- New portable fixtures: kind
  `openxfactory-hermes-runtime-portable-evidence-fixture` (jobs family may
  follow the migration precedent with a family kind ONLY if self-description
  demands it — default to the portable kind). `evaluation_time:
  "2026-07-13T12:00:00Z"` for ALL new semantic fixtures. Case-id prefixes:
  `jobs-`, `release-`, `regression-`, `handoff-`. Every fixture body repeats
  `case_id/phase/class/requirement_ids/scenario_ids/evaluation_time`
  consistently with its (future) index entry — self-description mismatch is a
  strict finding. `expected.outcome` `pass|fail`; `fail` requires
  `primary_finding_code` from the lane namespace and empty
  `allowed_secondary_codes`. Evidence IDs: `EVIDENCE-FIXTURE-<CASE-ID>`
  (match existing index style). Phases: `semantic` or `structural` ONLY —
  NEVER `phase: database` (that path would drag `fixtures.py` into scope).
- Mandatory named fixtures: Lane J `fixtures/jobs/retired-layer-new-job.yaml`
  (fail) + `fixtures/jobs/retired-layer-evidence-preserved.yaml` (pass);
  Lane H `fixtures/pins/consumer-receipt-wrong-repository.yaml` (fail,
  `HGR-HANDOFF-CONSUMER-REPOSITORY`).

## §7 Lane return payload (StructuredOutput; the ONLY channel into T077)

```json
{
  "lane": "J|R|D|H|DOC",
  "status": "complete-verified|complete-unverified|partial|failed",
  "files": ["<repo-relative paths written>"],
  "contract_index_entries": [{"contract_id":"…","path":"…","type":"schema",
    "contract_schema_version":2,"consumers":["openxfactory-validator"],
    "semantic_member":true,"release_member":true}],
  "fixture_cases": [{"case_id":"…","phase":"semantic","class":"…",
    "requirement_ids":["…"],"scenario_ids":["…"],"inputs":["jobs/…yaml"],
    "depends_on":[],"evaluation_time":"2026-07-13T12:00:00Z",
    "expected":{"outcome":"fail","primary_finding_code":"…",
    "allowed_secondary_codes":[]},"evidence_id":"EVIDENCE-FIXTURE-…"}],
  "evidence_bindings": [{"scenario_id":"NJE-004-S01",
    "fixture_case_ids":["…"],"test_node_ids":
    ["tests/hermes_runtime_contracts/test_v2_jobs.py::test_…"]}],
  "api": {"module":"…","functions":["…"]},
  "tests": {"command":"…","passed":0,"failed":0},
  "notes": "…"
}
```
`fixture_cases[].inputs` are fixture-root-relative (e.g. `jobs/x.yaml`) —
exactly as existing index entries. `test_node_ids` must be REAL collected
pytest node IDs (verify with `pytest --collect-only -q`).

## §8 Scenario ownership (evidence bindings each lane must return)

- Lane J: `NJE-004-S01..S05` (S05 = unchanged-v1 compatibility — the three
  frozen v1 schemas at `contracts/schemas/hermes-job-{envelope,run,event}.schema.yaml`
  still validate their pinned example fixtures byte-unchanged), plus
  `HGR-001-S01` (job evidence recorded), `HGR-001-S02` (record omits layer
  scope).
- Lane R: `HGR-009-S01..S05`; propose bindings for `SCO-002-S02`
  (published-tag verify), `SCO-002-S03` (pinned file drifts),
  `SCO-002-S04` (offline verification).
- Lane H: `SCO-002-S01, S05, S06, S07`; may co-bind S02/S03/S04 if its tests
  also exercise them.
- Coordinator: `HCS-005-S03` flip (evidence already wired); reconciles any
  double-claimed scenario (multiple node IDs per scenario are legal).

## §9 Verification bar per lane (before returning `complete-verified`)

1. `.venv/bin/python -m pytest <your test module> -q` — all green (RED-first
   during development; green at return).
2. `.venv/bin/python -m pytest tests/hermes_runtime_contracts -m 'not postgres' -q`
   — NO regression in existing 337 (do not fix others' failures; report).
3. `black --check <your .py files>`; `.venv/bin/python -m compileall -q <your .py>`.
4. `git status` shows ONLY your owned files changed.
5. Schemas: self-check `Draft202012Validator.check_schema` passes; positive
   and negative instances behave (your test module proves it).

## §10 Coordinator gate targets (post-T077, for reference)

Strict validator: 39 catalog members (34+5), 32 schema members (27+5),
fixture cases 79+N, 17 requirements / 85 scenarios (UNCHANGED), collected
nodes > 655, ZERO findings. Non-PG pytest: 337 + new, zero failures.
PG matrix: NOT re-run — `git diff --name-only 66b1406` intersected with the
78 inventory members MUST be empty at gate time. Count-pin edits
(coordinator only): `test_fixture_index.py` `== 79` → new total;
`test_validator_cli.py` mode-stub tests replaced by real-mode tests.
