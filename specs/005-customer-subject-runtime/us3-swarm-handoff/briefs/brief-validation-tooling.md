# Hermes Runtime Contract Family — Engineering Brief

Worktree root: `/workspace/projects/xFactory/openxFactory-worktrees/005-customer-subject-runtime`
Baseline verified live: `python3 scripts/validate-hermes-runtime-contracts.py --strict` → `pass (31 contracts, 25 schemas, 75 fixtures, 17 requirements, 85 scenarios, 407 tests collected)`.

## 1. Schema-authoring dialect (`contracts/hermes-runtime/*.schema.yaml`)

Every schema file is a YAML document that is simultaneously (a) a governance doc and (b) a JSON Schema Draft 2020-12 resource. Six **root annotations are mandatory** and are enforced by `catalog.py::_validate_schema_annotations` (any missing/mismatched one raises `CatalogError` → validator finding `HRC-CATALOG-INVALID`, which zeroes ALL counts):

```yaml
schema_version: 1                                          # must be exactly 1
kind: openxfactory-hermes-runtime-contract-schema          # exact constant (catalog.SCHEMA_KIND)
$schema: "https://json-schema.org/draft/2020-12/schema"    # exact constant (catalog.SCHEMA_META)
$id: "https://xforge.us/schemas/openxfactory/hermes-runtime/v2/<catalog path>"
contract_id: <must equal catalog entry contract_id>
contract_schema_version: 2                                 # must equal catalog entry value; family uses 2
```

`$id` MUST equal `catalog.CANONICAL_SCHEMA_BASE` (`https://xforge.us/schemas/openxfactory/hermes-runtime/v2/`) + the catalog `path` — enforced in `schema_registry.build_offline_registry` (`SchemaRegistryError` otherwise → `HRC-SCHEMA-REGISTRY`).

**Closed-record conventions** (see `traceability-edge.schema.yaml` as the model):
- Root: `type: object`, explicit `properties`, explicit `required` list, `additionalProperties: false`. Every nested object def also carries `required` + `additionalProperties: false`.
- Instance-level identity pinned via consts: `properties.schema_version: {const: 1}` and `properties.kind: {const: openxfactory-hermes-runtime-<record-name>}`.
- Local helper types live under root `$defs`; **nested `$id` anywhere below root is forbidden** (`_reject_nested_schema_ids`).
- Shared primitives come from `shared-definitions.schema.yaml` via relative refs: `$ref: shared-definitions.schema.yaml#/$defs/<name>` (e.g. `canonical_id`, `sha256_digest`, `record_digest`, `rfc3339_timestamp`, `layer_scope`, `governed_scope`, `content_resource_reference`, `principal_reference`, `authority_grant_reference`, `extensions`, `git_file_pin`, `contract_pin`). Same-file refs use `'#/$defs/...'`. To narrow a shared def use `allOf: [$ref, {required: [...]}]`.
- `$ref` hygiene enforced by `schema_registry._validate_reference_shape`: **no absolute URLs, no query, no percent-encoding, no backslash, no `.`/`..`/empty segments, no leading `/`**; after `urljoin($id, ref)` the target must start with `CANONICAL_SCHEMA_BASE` and resolve offline inside the registry (no filesystem/network fallback).
- Extension escape hatch: reuse `shared-definitions#/$defs/extensions` (namespaced, descriptive-only, banned words like role/authority/grant in property names).
- Relevant to migration: `shared-definitions#/$defs/content_resource_type` already enumerates `migration_mapping` and `dataset`; `authority_action` already includes `run_migration`.

**CRITICAL gotcha for `migrations/v1-to-v2-mapping.schema.yaml`**: subdirectory paths are legal catalog members (`_normalized_member_path` allows `migrations/...`, and `_schema_coverage_findings` rglobs `*.schema.yaml` recursively), BUT a schema whose `$id` ends in `.../v2/migrations/x.schema.yaml` **cannot reference root-level `shared-definitions.schema.yaml`**: the relative ref would need `../`, and `..` segments are rejected by `_validate_reference_shape`; a plain `shared-definitions.schema.yaml` ref urljoins to `.../v2/migrations/shared-definitions.schema.yaml`, which is unregistered → `SchemaRegistryError` "unresolved offline $ref". Options: (a) make the migrations schema fully self-contained ($defs duplicated), (b) place both new schemas at the family root like all 25 existing schemas, or (c) also publish a cataloged shared-defs schema under `migrations/`. Decide before authoring. `legacy-quarantine-record.schema.yaml` at family root has no such problem.

**YAML restrictions** (`loader.py::load_yaml_document`, `_StrictJsonLoader`): no anchors, no aliases, no merge keys, no duplicate keys, string keys only, no implicit/tagged timestamps (**quote all timestamps**), values must be JSON-compatible (finite floats only). Any violation is a `YamlLoadError` → catalog failure.

## 2. `contract-index.yaml` entry shape (`catalog.py`)

Top level (closed: unknown fields rejected): `schema_version: 1`, `kind: openxfactory-hermes-runtime-contract-index`, `contracts: [<entry>...]`. Each entry is a closed record with **exactly** these 7 fields (`_ENTRY_FIELDS`; missing OR unknown fields → `CatalogError`):

```yaml
- contract_id: v1-to-v2-mapping            # ^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,126}[A-Za-z0-9])?$, unique
  path: migrations/v1-to-v2-mapping.schema.yaml   # normalized POSIX repo-relative, unique, segments [A-Za-z0-9._-]+
  type: schema                             # lower-kebab; type "schema" REQUIRES path ending .schema.yaml
  contract_schema_version: 2               # positive int; must equal the annotation inside the schema file
  consumers: [openxfactory-validator, xfactory-hermes-install]   # non-empty, no duplicates
  semantic_member: true                    # bool required
  release_member: true                     # bool required
```

The file at `path` must be a regular non-symlink file inside the family root (resolved, containment-checked). Every `.yaml`/`.yml` member is parsed with the strict loader at catalog load time; schema-typed members additionally get the annotation check. The index does NOT bind fixtures/requirements/scenarios itself — those bindings live in three sibling catalog members that `validate-hermes-runtime-contracts.py::REQUIRED_CATALOG_MEMBERS` requires at exact ids/paths/types: `hermes-runtime-contract-index` (contract-index.yaml), `hermes-runtime-acceptance-map` (acceptance-map.yaml), `hermes-runtime-evidence-register` (evidence-register.yaml), `hermes-runtime-fixture-index` (fixtures/index.yaml), `shared-definitions` (shared-definitions.schema.yaml). The three YAML documents must carry kinds `openxfactory-hermes-runtime-{acceptance-map,evidence-register,fixture-index}` (`EXPECTED_DOCUMENT_KINDS`).

Cross-document invariants (`_cross_document_findings`): all three docs name the same `governed_change` (`add-hermes-customer-subject-runtime-contract`); `acceptance_map.fixture_index == "fixtures/index.yaml"`; `acceptance_map.evidence_register == "evidence-register.yaml"`; `evidence_register.expected_scenario_count == acceptance_map.expected_openspec_scenario_count`.

## 3. How the strict validator computes each count (and what breaks)

All in `scripts/validate-hermes-runtime-contracts.py::_validate_repository`; summary printed by `_render`.

| Count | Definition |
|---|---|
| **contracts (31)** | `len(catalog)` = number of entries in `contract-index.yaml:contracts`. Two new entries → 33. |
| **schemas (25)** | entries with `type == "schema"` (`catalog.schema_entries()`). Two new → 27. |
| **fixtures (75)** | `len(fixture_index["cases"])` in `fixtures/index.yaml`. |
| **requirements (17)** | `### Requirement:` headings extracted by `acceptance.extract_openspec_inventory` from every `openspec/changes/<governed_change>/specs/**/spec.md`. Each spec.md's **first non-blank line must be exactly `Status: ratified`** or `HRC-OPENSPEC-NOT-RATIFIED`. |
| **scenarios (85)** | total `#### Scenario:` headings under those requirements. |
| **tests (407)** | unique pytest node IDs from `collect_pytest_node_ids`: `python -m pytest -p no:cacheprovider --collect-only -q tests/hermes_runtime_contracts` (plugin autoload disabled, hashseed 0), lines starting `tests/` containing `::`. New test modules must live under `tests/hermes_runtime_contracts/`. |

Exit contract (`classify_exit_code`): 0 pass, 1 any finding (strict also promotes warnings), 2 harness/dependency error.

**Failure modes when files exist but are not registered:**
- Schema file present but no catalog entry → `HRC-CATALOG-SCHEMA-UNINDEXED` (rglob is recursive, so `migrations/*.schema.yaml` IS caught). Catalog entry but file absent → `HRC-CATALOG-SCHEMA-MISSING`. Symlink → `HRC-CATALOG-SCHEMA-NONREGULAR`.
- Bad annotations / dup id / dup path / unknown entry field → `CatalogError` → single `HRC-CATALOG-INVALID` finding and **all counts report 0**.
- `$id` wrong, nested `$id`, invalid Draft 2020-12, unresolvable or non-canonical `$ref` → `HRC-SCHEMA-REGISTRY`.
- Any `*.yaml` under `fixtures/` (except `index.yaml`) not listed in some case's `inputs` → `HRC-FIXTURE-UNINDEXED`.
- Fixture case naming unknown requirement/scenario IDs → `HRC-FIXTURE-REQUIREMENT-DANGLING` / `HRC-FIXTURE-SCENARIO-DANGLING`; missing `evidence_id` → `HRC-FIXTURE-EVIDENCE-ID`.
- Parity failures (semantic phase) → `HRC-PARITY-COUNT-MISMATCH` (stale `expected_openspec_requirement_count: 17` / `expected_openspec_scenario_count: 85` / `expected_scenario_count: 85`), `HRC-PARITY-MISSING` (requirement without acceptance mapping; scenario without evidence entry), `HRC-PARITY-DANGLING` (evidence `test_node_ids` not in the collected set; acceptance mapping for a nonexistent requirement), `HRC-PARITY-DUPLICATE`, `HRC-PARITY-SKIPPED-REQUIRED` (`status: skipped`).
- **Pinned tests to update**: `tests/hermes_runtime_contracts/test_fixture_index.py::test_current_fixture_index_preserves_75_cases` asserts exactly 75 cases; `test_acceptance_parity.py::test_extracts_exact_ratified_17_requirement_85_scenario_inventory` asserts 17/85. Adding fixtures/scenarios without updating these fails pytest even though the validator passes.

## 4. Fixture validation (`scripts/hermes_runtime_validation/fixtures.py`)

`validate_index(index, *, fixture_root, repository_root)` validates the **index**, not JSON-Schema conformance. Case record shape (see `fixtures/index.yaml`):

```yaml
- case_id: reference-uuidv4-subject        # kebab, unique
  phase: semantic                          # structural | semantic | database
  class: valid                             # valid | invalid (informational)
  requirement_ids: [HCS-002, HCS-006]      # must exist in acceptance-map openspec_parity ids
  scenario_ids: [HCS-002-S01, HCS-006-S02] # must exist in acceptance-map scenario_ids
  inputs: [references/uuidv4-subject.yaml] # fixture-root-relative; each path owned by exactly ONE case
  depends_on: []                           # case IDs; cycles/unknowns fail (dependency_order topo-sort)
  evaluation_time: "2026-07-12T12:00:00Z"  # REQUIRED for semantic phase; RFC3339 UTC, quoted
  expected:
    outcome: pass                          # pass → zero findings allowed
    allowed_secondary_codes: []
  evidence_id: EVIDENCE-FIXTURE-REFERENCE-UUIDV4-SUBJECT   # required
```

Negative cases use `expected: {outcome: fail, primary_finding_code: HCS-SUBJECT-ATTESTATION-REQUIRED, allowed_secondary_codes: []}`; the code must match `_CODE = ^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$`. `evaluate_expected_findings(case, findings)` enforces exact-reason semantics: the primary code must be present and any code outside {primary} ∪ allowed_secondary fails the case — a wrong failure reason does not satisfy an invalid fixture. Convention throughout the index: valid/invalid **pairs** per topic subdirectory (`references/`, `topology/`, `pins/`, `authority/`, `approvals/`, `artifacts/`, `traceability/`, `jobs/`, `isolation/`, `regression/`, `release/`, `postgres/`, and an already-created empty `migration/` directory awaiting this work).

Self-description rule: if a fixture YAML itself contains `case_id`, `phase`, `class`, `requirement_ids`, `scenario_ids`, or `evaluation_time`, each must equal the index entry (`HGR-FIXTURE-SELF-DESCRIPTION-MISMATCH`).

Actual **JSON-Schema validation of fixture documents happens in the pytest suite**, not fixtures.py: tests build a `referencing.Registry` from the loaded schemas and run `Draft202012Validator(schema, registry=registry, format_checker=FormatChecker()).iter_errors(document)` per indexed case (pattern: `test_topology_and_identity.py::test_all_indexed_topology_fixtures_close_against_offline_schema_family`, also `test_artifact_approval_trace.py::validators()`). Semantic finding codes (HCS-*/HGR-*) come from `scripts/hermes_runtime_validation/semantics/{topology,references,overlays,authority,evidence}.py`; a new `migration.py` module supplying migration finding codes should follow the semantics `_finding(code, path, message)` shape and deterministic sorted output. `database`-phase cases carry a closed `database:` block (engine/majors/source_paths/test_modules/seed_scripts/assertion_scripts/row & digest expectations/authoritative_deltas/result_refs) with digest-bound result evidence — reuse only if migration needs live-Postgres evidence.

## 5. Acceptance mapping (`acceptance-map.yaml` + `acceptance.py`)

Top fields: `schema_version: 1`, `kind: openxfactory-hermes-runtime-acceptance-map`, `feature: 005-customer-subject-runtime`, `governed_change`, `fixture_index: fixtures/index.yaml`, `evidence_register: evidence-register.yaml`, `us1_binding_status`/`us2_binding_status`, `expected_openspec_requirement_count: 17`, `expected_openspec_scenario_count: 85`, `openspec_parity: [...]`.

Each `openspec_parity` mapping:
```yaml
- id: HCS-005                              # requirement ID (regex [A-Z]+[A-Z0-9]*-\d{3})
  capability: hermes-customer-subject-runtime   # = spec dir name under specs/
  title: Customer-subject lifecycle preserves identity and evidence  # EXACT text after "### Requirement:"
  feature_requirement_ids: [FR-007, FR-039]     # optional Speckit cross-refs
  scenario_ids: [HCS-005-S01, HCS-005-S02, HCS-005-S03]   # <req>-S<NN>, globally unique
  scenario_titles:                          # EXACT text after "#### Scenario:", same order/length as scenario_ids
  - Provision request is retried
  - ...
```

`check_parity` joins acceptance mappings to the OpenSpec inventory on the key `(capability, title)` — titles must byte-match the spec heading. It enforces: one mapping per requirement (missing/dangling/duplicate), per-requirement scenario count == spec scenario count, both expected_* counts == actuals, total mappings == requirement count, total scenario_ids == scenario count. Then per-scenario evidence: `evidence-register.yaml:entries` must contain **exactly one** entry per scenario_id, whose `requirement_id` and `scenario_title` exactly repeat the acceptance metadata, whose `status` is not `skipped`, and whose `test_node_ids` (non-empty unique strings) all appear in the pytest collected set. Evidence entry shape: `scenario_id, requirement_id, scenario_title, status: bound, authorizes: false, evidence_id, planned_owner_task, fixture_case_ids: [...existing case_ids...], test_node_ids: [tests/hermes_runtime_contracts/<file>.py::<test>[param]], result_refs: []`. So per new scenario you need: acceptance mapping row + evidence entry + at least one real collected test node + bumped counts in BOTH acceptance-map (`expected_openspec_scenario_count`) and evidence-register (`expected_scenario_count`). New requirements/scenarios can only come from spec.md files under `openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/specs/` whose first line is `Status: ratified`.

Note: the migration requirement already exists ratified — `specs/hermes-governed-record-integrity/spec.md` "### Requirement: v2 persistence coexists with v1 and migrates atomically" defines the mapping payload, quarantine-record semantics, and the **`xfactory-v1-dataset-binary-v1`** dataset digest byte-framing (magic `XFV1DS` + `00 01`, `tag:u8 || len:u64be || payload` frames, table/column/row frame tags 10–36, bytewise table sort, primary-key-frame row sort, custom canonical JSON for tag 36). The digest CLI must implement that framing exactly; the spec's canonical JSON (raw-UTF-8 key sort, minimal escaping, arbitrary-precision decimals) is NOT identical to Python `json.dumps` — write a dedicated serializer for tag-36 values.

## 6. Reusable utilities and CLI conventions

**Canonical-JSON / digest helpers to reuse in `migration.py`:**
- `scripts/hermes_runtime_validation/semantics/authority.py::canonical_record_digest(record)` — the frozen `xfactory-canonical-json-v1` profile: sha256 over `json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")` with the record's own top-level `record_digest` omitted; fails closed on floats/non-JSON. Constant `RECORD_DIGEST_PROFILE = "xfactory-canonical-json-v1"`. Use this for mapping-payload / quarantine record_digest checks.
- `scripts/hermes_runtime_validation/fixtures.py::_canonical_digest(value)` — same compact sorted-key sha256 (`"sha256:" + hexdigest`) without the record_digest omission; private, so either import deliberately or mirror.
- `scripts/hermes_runtime_validation/content.py`: `normalize_repository_path(path)`, `resolve_git_object(repository, revision, path) -> ResolvedGitContent` (exact-commit blob resolution, env-hardened, digest field `sha256:<hex>`), `ContentResolutionError` (carries `exit_code = 2`, `code="HRC-CONTENT-DEPENDENCY"`). Use for content-addressed mapping-payload pins.
- `scripts/hermes_runtime_validation/loader.py::load_yaml_document` / `YamlLoadError` — the only sanctioned YAML reader.
- `scripts/hermes_runtime_validation/catalog.py::load_contract_catalog`, `ContractCatalog.schema_entries()`, `.document_for()`; `schema_registry.py::build_offline_registry(catalog)` for compiled offline Draft 2020-12 validation.
- `fixtures.py::database_matrix_identity` / `repository_source_identity` (profiles `xfactory-postgres-matrix-v1`, `xfactory-postgres-source-inputs-v1`) as worked examples of profile-tagged digest identities that survive clean clones.

**CLI conventions for `scripts/hermes-runtime-dataset-digest.py`** (model: `validate-hermes-runtime-contracts.py`; the only other hermes-runtime CLI is POSIX-sh `run-hermes-runtime-postgres-tests.sh` with `--major 15|16 --json --update-image-lock`, usage→stderr, exit 2):
- Hyphenated thin entrypoint that inserts `Path(__file__).resolve().parents[1]` into `sys.path` and imports the real logic from `scripts.hermes_runtime_validation.migration` (so pytest can import the module directly).
- `argparse` with `--json`/`--strict` style flags; exit codes via `classify_exit_code` semantics: 0 pass, 1 finding, 2 dependency/harness error.
- Findings are dicts `{code, severity, case_id, path, message}` sorted by `(case_id, path, code, message)`; JSON output is one line: `json.dumps(payload, sort_keys=True, separators=(",", ":"))` with keys `exit_code, findings, mode, selection, status, summary`; human output is one summary line on pass or `CODE severity case=... path=...: message` lines.
- Determinism: subprocesses run with `LANG/LC_ALL=C.UTF-8, PYTHONHASHSEED=0, TZ=UTC, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` (see `collect_pytest_node_ids` and `tests/hermes_runtime_contracts/support.py::deterministic_environment`).

## Registration checklist for clean count rise (31→33, 25→27, 75→75+N, 17/85→ratified deltas, 407→407+M)

1. Author both schemas with the 6 root annotations, closed records, `$id = base + path` (resolve the subdirectory-$ref decision first).
2. Add two `contracts:` entries to `contract-index.yaml` (type `schema`, `contract_schema_version: 2` matching the file, consumers, both booleans).
3. Add migration fixture YAMLs under `fixtures/migration/` and index every file in exactly one case's `inputs`; semantic cases need quoted `evaluation_time` and `evidence_id`; negative cases need a stable `primary_finding_code`.
4. If new scenarios are added: edit ratified spec deltas, bump `expected_openspec_requirement_count`/`expected_openspec_scenario_count` (acceptance-map) and `expected_scenario_count` (evidence-register), add parity mappings with byte-exact titles, add one evidence entry per scenario with real collected `test_node_ids`.
5. Put new tests in `tests/hermes_runtime_contracts/` (e.g. `test_migration_mapping.py`); update the pinned-count tests `test_current_fixture_index_preserves_75_cases` and (if counts change) the 17/85 assertions in `test_acceptance_parity.py`.
6. Re-run `python3 scripts/validate-hermes-runtime-contracts.py --strict` (and `--json`) from the worktree root; it must exit 0 with the new counts.

## Open questions
- Path conflict: schema_registry._validate_reference_shape forbids '..' and absolute $refs, so a schema at migrations/v1-to-v2-mapping.schema.yaml cannot $ref the root-level shared-definitions.schema.yaml (urljoin from its $id lands in .../v2/migrations/). Engineers must choose: self-contained $defs, root placement instead of migrations/, or a cataloged shared-defs under migrations/.
- Do the two new schemas map to already-ratified scenarios of requirement 'v2 persistence coexists with v1 and migrates atomically' (keeping 17/85 fixed), or do they need new spec-delta scenarios (which requires editing ratified spec.md files and bumping three expected-count fields plus pinned tests)?
- tests/hermes_runtime_contracts/test_fixture_index.py::test_current_fixture_index_preserves_75_cases hard-pins 75 fixture cases — adding migration fixtures requires updating this assertion in the same change.
- The spec's xfactory-v1-dataset-binary-v1 canonical JSON (raw-UTF-8 byte key sort, minimal escaping, arbitrary-precision decimal rendering) is not byte-identical to Python json.dumps(sort_keys=True); the dataset-digest CLI needs a purpose-built serializer for tag-36 JSON value frames rather than reusing canonical_record_digest for that stream.
- fixtures.py::_canonical_digest is module-private; confirm whether migration.py should import it, import semantics.authority.canonical_record_digest, or host a new shared public helper.
- The v1-to-v2 migration requirement's scenarios are largely evidenced via the database phase (run-hermes-runtime-postgres-tests.sh); confirm whether migration fixture cases should be phase: semantic (portable) or phase: database (needs result_refs, image lock, and matrix evidence).