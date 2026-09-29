# Phase 1 checkpoint (T049)

Status: record

**Feature**: [`034-opendox-standalone-operation`](../spec.md) · **Task**: T049
([`tasks.md`](../tasks.md)) · **Run**: 2026-09-29, 13:48–14:00Z at openxFactory
`main` `e81eed62`, with the arrival check re-run at `08e97c27` ·
**Lane**: `openxfactory-4`

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`). It runs and quotes every check T049 names, at the commits phase
1 pinned. Every check passes except F9.2, which is red as ruled, on one test.
The last section records T092's phase-1 notes, which ride in this PR on the
holder's decision of 2026-09-28.

## Verdict

| # | T049's check | where it ran | result |
|---|---|---|---|
| 1 | F2.1 | openDox-code `2d116415` | **PASS**, exit 0 |
| 2 | F3.1, line 2 as amended (T007 batch A) | openDox-code `2d116415` | **PASS**, exit 0 |
| 3 | F9.1 (openDox-code), with the database's DSN exported | openDox-code `2d116415` | **PASS**, exit 0: `2468 passed, 11 skipped` |
| 4 | F9.1 (openXdox-code), as batches B and F amend it, with batch J's one `--deselect` | openXdox-code `6158151e` | **PASS**, exit 0: `881 passed, 4 skipped, 1 deselected` |
| 5 | F9.2 | openXdox-code `6158151e` | **RED, AS RULED**: exit 1 on the 31-entry help-tree test alone (§ 5) |
| 6 | `opendox --help` (F10.1's first assertion) | openDox-code `2d116415` | **PASS**, exit 0 |
| 7 | F4.1's scan: only `openxdox` targets | openDox-code `2d116415` | **PASS**: 19 deferred reaches, all `openxdox` |
| 8 | every module or case T034 or T035 removed, found where its PR's list sends it | all three legs | **PASS**: 19 of 19 (§ 8) |
| 9 | T043's R1Q24 (a) files and `tests/test_snapshot.py`, in the declared exclusion with their reasons | openXdox-code `6158151e` | **PASS**: 9 of 9 |
| 10 | T018's interim F11.1 | openxFactory `e81eed62` | **PASS**: quoted, and re-run with the same result |

**The holder's decisions at this checkpoint (2026-09-29, relayed to T049's
writer):**

- **F9.2 is quoted red, as ruled, and phase 1 closes.** RULED `5859927858`
  (Brett Heap, 2026-09-27, "(b) Exclude it until T008's arc (Recommended)"):
  "The test leaves T042's integration step, with its stated reason: cli_gate
  imports openxFactory's doc_health at load time, which is R1Q6 (d)'s kind of
  exclusion. It runs again once the doc_health direction arc (T008) lands.
  F9.2 is unchanged." So F9.2 stays red on that test until T008. Its box moves
  from T049 to "after T008" in plan 034 (this PR); #1144's F9.2 text is not
  touched.
- **The one case that was in no suite landed first.** Check 8 first found
  `test_worktree_container_is_gitignored_in_the_aggregation_repo` (T035's) in
  no suite. T007 batch E had held it out, "Held, not decided against; a later
  task takes it up". The holder took option (b), so it landed first, in its
  own openxFactory PR (opensoft/openxFactory#1203 → `08e97c27`). Check 8 was then re-run
  at `08e97c27`, and it finds all 19.

T049 is ticked in plan 034 on this record. As its text says, it ticks nothing
in #1144: T097 does.

## The pins

Read from openxFactory `main` `e81eed62`, the landing of opensoft/openxFactory#1202
(T017/T018):

| where | pin | resolves to |
|---|---|---|
| openxFactory `openDox` gitlink and `contracts/opendox-pin.yaml` | openDox root `663ac683` | `code` → openDox-code `2d116415` (T037's landing, `contracts/code-pin.yaml` agrees); `spec` → `8fe8c4c7` |
| openxFactory `openXdox` gitlink and `contracts/openxdox-pin.yaml` | openXdox root `57e2b8f2` | `code` → openXdox-code `6158151e` (T044's landing, `contracts/code-pin.yaml` agrees); `spec` → `f088b097`; its own `contracts/opendox-pin.yaml` → openDox `663ac683` |
| openXdox-code `pyproject.toml` | `opendox @ git+https://github.com/opensoft/openDox-code@2d116415159b721b55613fe20a159afc46202d1f` | F9.2's install records `commit_id` `2d116415…` (§ 5) |

At the run, each leg's `main` was exactly its pinned commit (openDox-code
`2d116415`, openXdox-code `6158151e`). `f56c87c6` (T047, #1181) is still
openxFactory's only arc landing (`git log --first-parent --grep='^Arc:
neutral-product-standalone-operability$' 94b6f7f1..e81eed62`).

## How each check ran

- **The text is #1144's own.** Each falsifier was extracted byte-for-byte from
  `openspec/changes/add-neutral-product-standalone-operability/tasks.md` at
  `e81eed62` (sha256 `e9048b1c…`), by line range, and dedented by its six-space
  block indent: F2.1 `:274-296`, F3.1 `:346-353`, F4.1 `:438-487`, F9.1
  `:1108-1123`, F9.2 `:1183-1198`, F10.1 `:1280-1303`, F11.1 `:1371-1450`.
  Where T049 names an amended form, the one changed line is shown with its
  diff.
- **Each ran from a fresh clone of its leg at the pinned commit**, with an
  empty `git status --porcelain`, from the checkout root, under `bash`, and in
  the foreground.
- **Environment.** Python 3.12.3; `python` resolves to the host's Python 3.12
  interpreter through a `PATH` shim, because the host has no `python` and CI's
  `setup-python` gives 3.12. `TMPDIR` is a scratch directory, `LANG=C.UTF-8`,
  and `PYTHONPATH` is unset. The only other variable any run sets is the DSN in
  § 3. In the quoted output the scratch directory's host path is written
  `<workdir>` (Principle IV).
- **pip's install log is elided.** Each block quotes the output after pip's
  last line, `Successfully installed …`, which is quoted too. Progress dots
  are elided, as marked.

## 1. F2.1 (openDox-code `2d116415`)

As extracted (sha256 `f11e8145129f…`), run unchanged:

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
python -m venv "$W/v2"
. "$W/v2/bin/activate"
pip install ".[runtime,test]"
for sibling in openxdox ideation_dashboard doc_health corpus_adapter_openxfactory; do
  if python -c "import $sibling" 2>/dev/null; then echo "FAIL: $sibling is importable"; exit 1; fi
done
# EVERY module of the package, generated, not a hand-picked three:
python3 - <<'PY'
import importlib, pkgutil, sys, opendox
failed = []
for m in pkgutil.walk_packages(opendox.__path__, "opendox."):
    try:
        importlib.import_module(m.name)
    except Exception as e:                            # noqa: BLE001 - every failure is a finding here
        failed.append(f"{m.name}: {type(e).__name__}: {e}")
if failed:
    sys.exit("FAIL: modules that still need a sibling:\n  " + "\n  ".join(failed))
print("every module of opendox imports with no sibling")
PY
# ...and 2.4's own test, by name, so the suite keeps the sweep after the arc:
python -m pytest -q "tests/test_imports_standalone.py::test_every_module_imports_with_no_sibling"
```

**Exit 0.** The sibling loop printed no `FAIL` line, so none of
`openxdox`, `ideation_dashboard`, `doc_health` or `corpus_adapter_openxfactory`
imports. The generated sweep and 2.4's named test pass:

```
Successfully installed PyJWT-2.15.1 PyYAML-6.0.3 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 cffi-2.1.1 click-8.5.0 cryptography-50.0.1 fastapi-0.141.1 h11-0.16.0 httpcore-1.0.9 httptools-0.8.0 httpx-0.28.1 idna-3.20 iniconfig-2.3.0 opendox-0.0.0 packaging-26.3 pluggy-1.6.0 psycopg-3.3.6 psycopg-binary-3.3.6 psycopg-pool-3.3.3 pycparser-3.0 pydantic-2.13.5 pydantic-core-2.46.5 pygments-2.21.0 pytest-8.4.2 python-dotenv-1.2.3 starlette-1.7.0 typing-extensions-4.16.0 typing-inspection-0.4.4 uvicorn-0.54.0 uvloop-0.22.1 watchfiles-1.3.0 websockets-17.1
every module of opendox imports with no sibling
.                                                                        [100%]
1 passed in 1.48s
```

## 2. F3.1, with line 2 as amended (openDox-code `2d116415`)

T007 batch A (`5817152735`, R1Q3 (a)) amends line 2 to ask after
`build_parser()`. The run (sha256 `53172368b760…`) is the extracted
block with that one line changed:

```diff
-python -c "from opendox import domain_profile as d; print('OK', d.name_of(d.current()))"
+python -c "from opendox.cli import build_parser; from opendox import domain_profile as d; build_parser(); print('OK', d.name_of(d.current()))"   # line 2 AS AMENDED (T007 batch A, 5817152735, R1Q3 (a))
```

**Exit 0.** Both lines print `OK`, the second with the default profile's
name, and `tests/test_profile_registration.py` passes whole (it also asserts
that a bare process that builds nothing still meets `ProfileNotRegistered`):

```
Successfully installed PyJWT-2.15.1 PyYAML-6.0.3 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 cffi-2.1.1 click-8.5.0 cryptography-50.0.1 fastapi-0.141.1 h11-0.16.0 httpcore-1.0.9 httptools-0.8.0 httpx-0.28.1 idna-3.20 iniconfig-2.3.0 opendox-0.0.0 packaging-26.3 pluggy-1.6.0 psycopg-3.3.6 psycopg-binary-3.3.6 psycopg-pool-3.3.3 pycparser-3.0 pydantic-2.13.5 pydantic-core-2.46.5 pygments-2.21.0 pytest-8.4.2 python-dotenv-1.2.3 starlette-1.7.0 typing-extensions-4.16.0 typing-inspection-0.4.4 uvicorn-0.54.0 uvloop-0.22.1 watchfiles-1.3.0 websockets-17.1
OK
OK opendox.default_profile
...................................................                      [100%]
51 passed in 0.99s
```

## 3. F9.1 (openDox-code `2d116415`), with the database's DSN exported

F9.1 as extracted (sha256 `ec2acf0c0093…`), unchanged for openDox-code
(R1Q8 (a)). T036 has F9.1's runs "export the database's DSN the way the job
does, and quote the variables they set". The job sets exactly one, on its
`pytest` step, against its `postgres:16` service (user and database `opendox`,
with the throwaway password `validate.yml` declares). This run set the same
variable, with the same user, database and password, against a `postgres:16`
container of its own. Here the password, and that container's host and port,
are placeholders, so the record stores no credential and no host address
(Principle IV):

```
OPENDOX_TEST_DATABASE_URL=postgresql://opendox:<password>@<host>:<port>/opendox
```

**Exit 0.** The run collects `testpaths` whole (`tests`,
`tests_runtime`), and both `validate.yml` assertions pass (the `grep -c` is `0`,
and no pytest step names a test file). The count is CI's own triple at this
tree: `validate.yml`'s re-pin reads `selected=2479 passed=2468 skipped=11`. The
database-backed half ran against the service: its `xact_commit` went from 3
before the run to 2566 after it, and none of the 11 skips is in
`tests_runtime/`.

```
Successfully installed PyJWT-2.15.1 PyYAML-6.0.3 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 cffi-2.1.1 click-8.5.0 cryptography-50.0.1 fastapi-0.141.1 h11-0.16.0 httpcore-1.0.9 httptools-0.8.0 httpx-0.28.1 idna-3.20 iniconfig-2.3.0 opendox-0.0.0 packaging-26.3 pluggy-1.6.0 psycopg-3.3.6 psycopg-binary-3.3.6 psycopg-pool-3.3.3 pycparser-3.0 pydantic-2.13.5 pydantic-core-2.46.5 pygments-2.21.0 pytest-8.4.2 python-dotenv-1.2.3 starlette-1.7.0 typing-extensions-4.16.0 typing-inspection-0.4.4 uvicorn-0.54.0 uvloop-0.22.1 watchfiles-1.3.0 websockets-17.1
[35 line(s) of progress dots elided]
=============================== warnings summary ===============================
tests_runtime/test_api_endpoints.py::test_livez_answers_without_a_token
  <workdir>/tmp/tmp.BoU5flx5J1/v9/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
2468 passed, 11 skipped, 1 warning in 222.25s (0:03:42)
```

## 4. F9.1 (openXdox-code `6158151e`), as batches B and F amend it

The ratified block, with the one `--deselect` that RULED `5870594693` (Brett
Heap, 2026-09-28, "(b) Amend F9.1 to deselect it (Recommended)") adds to its
pytest line, and T007 batch J records (citing `5859927858`). It is the same
line T043 ran (openXdox-code#32):

```diff
-python -m pytest -q                                   # NOT --noconftest, NOT a file list
+python -m pytest -q --deselect tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records   # NOT --noconftest, NOT a file list
```

After the block, and only because `set -e` let it reach them, the run reads
batch B's first two assertions out of the declaration itself, and runs the
suite's own check of it by name (sha256 `f7b887248f19…`):

```sh
# Batch B's first two assertions, read from the declaration itself (its third, the printed
# title line, is read from this run's own output afterwards):
python3 - <<'PY2'
import yaml
d = yaml.safe_load(open("tests/declared_exclusion.yaml"))
ids = {r["id"] for r in d["reasons"]}
assert d["count"] == len(d["entries"]), f"count {d['count']} != {len(d['entries'])} entries"
for e in d["entries"]:
    assert e.get("reasons") and set(e["reasons"]) <= ids, f"entry without a declared reason: {e}"
only = {r["id"]: set(r["only"]) for r in d["reasons"] if "only" in r}
for e in d["entries"]:
    for r in e["reasons"]:
        assert r not in only or e["path"] in only[r], f"{e['path']} carries {r}, which is only for {only[r]}"
by = {}
for e in d["entries"]:
    for r in e["reasons"]:
        by.setdefault(r, []).append(e["path"])
print(f"=== declared exclusion: count {d['count']} == {len(d['entries'])} entries; every entry carries a declared reason")
for r in d["reasons"]:
    print(f"=== reason {r['id']}: {len(by.get(r['id'], []))} entries; ruled: {r['ruled']}; open until: {r['open_until']}")
PY2
echo "=== the suite's own check of the declaration, by name:"
python -m pytest -q tests/test_declared_exclusion.py
```

**Exit 0.** Batch B's three assertions all hold:

- the file's count equals its entries: `count 67 == 67 entries`;
- every entry carries a declared reason, and `consumer-schemas` only on
  `tests/test_snapshot.py`;
- the run prints the exclusion as an open extraction, under its title line
  `open extraction: the declared exclusion`, with its count and each entry's
  reason.

The two `validate.yml` assertions pass. `881 passed, 4 skipped, 1 deselected`
is CI's `885/881/4`:

```
Successfully installed PyYAML-6.0.3 attrs-26.1.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 opendox-0.0.0 openxdox-0.0.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-8.4.2 referencing-0.37.0 rfc3339-validator-0.1.4 rpds-py-2026.6.3 six-1.17.0 typing-extensions-4.16.0
[13 line(s) of progress dots elided]
=================== open extraction: the declared exclusion ====================
declared exclusion: 67 files, listed in tests/declared_exclusion.yaml and left out of this run. It is an OPEN extraction: each file runs again once its reason is cleared.
  reason doc_health (60 files): reaches openxFactory's doc_health, which openxFactory packages nowhere and no lone checkout supplies; open until the doc_health direction arc (plan 034 T008); ruled R1Q6 (d), openxFactory#656 comment 5817152735
  reason status-exemption-rail (3 files): needs openxFactory's status-exemption rail, which only openxFactory registers at openDox's status-exemption seam; open until the doc_health direction arc (plan 034 T008); ruled R1Q24 (a), openxFactory#656 comment 5850003126
  reason openxfactory-contracts (5 files): reads openxFactory's contracts (the contract family's validator, schemas and examples, or its contracts/manifest.yaml) where openxFactory's tree keeps them, which is outside this checkout; open until the doc_health direction arc (plan 034 T008); ruled R1Q24 (a), openxFactory#656 comment 5850003126
  reason consumer-schemas (1 file): needs the consumer validator's schemas, which neither a contracts/ in this tree nor CONTRACTS_DIR supplies until 7.3 finds them through the installed distribution; open until 7.3, the consumer's validator lookup (plan 034 T061, in phase 2); ruled R1Q25 (b), openxFactory#656 comment 5850003126
  excluded tests/test_authoring_agent.py: doc_health
  excluded tests/test_branch_session.py: doc_health
  excluded tests/test_canvas.py: doc_health
  excluded tests/test_completeness.py: doc_health
  excluded tests/test_create_document_cli.py: doc_health
  excluded tests/test_create_project.py: doc_health
  excluded tests/test_doxbench_abstract_envelope.py: status-exemption-rail
  excluded tests/test_doxbench_abstract_route.py: doc_health
  excluded tests/test_doxbench_blank_reason.py: doc_health, openxfactory-contracts
  excluded tests/test_doxbench_knowledge_service.py: doc_health
  excluded tests/test_doxbench_mutation_boundary.py: doc_health
  excluded tests/test_doxbench_packet.py: doc_health, status-exemption-rail
  excluded tests/test_doxbench_request_handling.py: doc_health
  excluded tests/test_doxbench_save.py: doc_health
  excluded tests/test_doxbench_scope.py: doc_health
  excluded tests/test_doxbench_share.py: doc_health
  excluded tests/test_doxbench_thread_wiring.py: doc_health
  excluded tests/test_doxbench_threads.py: doc_health
  excluded tests/test_doxbench_transport.py: doc_health
  excluded tests/test_doxbench_turns.py: status-exemption-rail
  excluded tests/test_doxchat_model_intake.py: doc_health
  excluded tests/test_edit_action.py: doc_health
  excluded tests/test_edit_project.py: doc_health
  excluded tests/test_explorer_viewer.py: doc_health
  excluded tests/test_gate_console.py: doc_health
  excluded tests/test_gate_failure_diagnostics.py: doc_health
  excluded tests/test_gateway_provenance.py: doc_health
  excluded tests/test_generated_at_anchor.py: doc_health
  excluded tests/test_generator.py: doc_health
  excluded tests/test_grouping.py: doc_health
  excluded tests/test_header_value_readers.py: doc_health
  excluded tests/test_hermeticity_gate_verbs.py: doc_health
  excluded tests/test_hosted_actor.py: doc_health
  excluded tests/test_kickoff.py: doc_health
  excluded tests/test_notebook_action.py: doc_health
  excluded tests/test_project_action_contracts.py: openxfactory-contracts
  excluded tests/test_project_aggregates.py: doc_health
  excluded tests/test_project_schema_election.py: openxfactory-contracts
  excluded tests/test_readiness_gate.py: doc_health
  excluded tests/test_register_edit_lane.py: doc_health
  excluded tests/test_renderer.py: doc_health
  excluded tests/test_repo_root_guard.py: doc_health
  excluded tests/test_repo_selector.py: doc_health
  excluded tests/test_round_trip.py: doc_health
  excluded tests/test_seam_assembly_beside_gate_and_projection.py: doc_health
  excluded tests/test_session_commits.py: doc_health
  excluded tests/test_session_confinement.py: doc_health
  excluded tests/test_session_document_ownership.py: doc_health
  excluded tests/test_session_gates.py: doc_health
  excluded tests/test_session_lifecycle.py: doc_health
  excluded tests/test_session_notebook.py: doc_health
  excluded tests/test_session_records.py: doc_health
  excluded tests/test_session_runbook.py: doc_health
  excluded tests/test_session_snapshot.py: doc_health
  excluded tests/test_session_transaction.py: doc_health
  excluded tests/test_session_verbs.py: doc_health
  excluded tests/test_snapshot.py: consumer-schemas
  excluded tests/test_snapshot_determinism.py: doc_health
  excluded tests/test_snapshot_registry.py: doc_health
  excluded tests/test_snapshot_validation_launch.py: doc_health
  excluded tests/test_source_dot_directories.py: doc_health
  excluded tests/test_staging_workbench.py: doc_health
  excluded tests/test_trust_gaps.py: doc_health
  excluded tests/test_validate_ideation_dashboard_contracts.py: openxfactory-contracts
  excluded tests/test_wheel_action_contracts.py: openxfactory-contracts
  excluded tests/test_wheel_model.py: doc_health
  excluded tests/test_wheel_verbs_cli.py: doc_health
881 passed, 4 skipped, 1 deselected in 45.84s
=== declared exclusion: count 67 == 67 entries; every entry carries a declared reason
=== reason doc_health: 60 entries; ruled: R1Q6 (d), openxFactory#656 comment 5817152735; open until: the doc_health direction arc (plan 034 T008)
=== reason status-exemption-rail: 3 entries; ruled: R1Q24 (a), openxFactory#656 comment 5850003126; open until: the doc_health direction arc (plan 034 T008)
=== reason openxfactory-contracts: 5 entries; ruled: R1Q24 (a), openxFactory#656 comment 5850003126; open until: the doc_health direction arc (plan 034 T008)
=== reason consumer-schemas: 1 entries; ruled: R1Q25 (b), openxFactory#656 comment 5850003126; open until: 7.3, the consumer's validator lookup (plan 034 T061, in phase 2)
=== the suite's own check of the declaration, by name:
[3 line(s) of progress dots elided]
=================== open extraction: the declared exclusion ====================
declared exclusion: 67 files, listed in tests/declared_exclusion.yaml and left out of this run. It is an OPEN extraction: each file runs again once its reason is cleared.
  reason doc_health (60 files): reaches openxFactory's doc_health, which openxFactory packages nowhere and no lone checkout supplies; open until the doc_health direction arc (plan 034 T008); ruled R1Q6 (d), openxFactory#656 comment 5817152735
  reason status-exemption-rail (3 files): needs openxFactory's status-exemption rail, which only openxFactory registers at openDox's status-exemption seam; open until the doc_health direction arc (plan 034 T008); ruled R1Q24 (a), openxFactory#656 comment 5850003126
  reason openxfactory-contracts (5 files): reads openxFactory's contracts (the contract family's validator, schemas and examples, or its contracts/manifest.yaml) where openxFactory's tree keeps them, which is outside this checkout; open until the doc_health direction arc (plan 034 T008); ruled R1Q24 (a), openxFactory#656 comment 5850003126
  reason consumer-schemas (1 file): needs the consumer validator's schemas, which neither a contracts/ in this tree nor CONTRACTS_DIR supplies until 7.3 finds them through the installed distribution; open until 7.3, the consumer's validator lookup (plan 034 T061, in phase 2); ruled R1Q25 (b), openxFactory#656 comment 5850003126
  excluded tests/test_authoring_agent.py: doc_health
  excluded tests/test_branch_session.py: doc_health
  excluded tests/test_canvas.py: doc_health
  excluded tests/test_completeness.py: doc_health
  excluded tests/test_create_document_cli.py: doc_health
  excluded tests/test_create_project.py: doc_health
  excluded tests/test_doxbench_abstract_envelope.py: status-exemption-rail
  excluded tests/test_doxbench_abstract_route.py: doc_health
  excluded tests/test_doxbench_blank_reason.py: doc_health, openxfactory-contracts
  excluded tests/test_doxbench_knowledge_service.py: doc_health
  excluded tests/test_doxbench_mutation_boundary.py: doc_health
  excluded tests/test_doxbench_packet.py: doc_health, status-exemption-rail
  excluded tests/test_doxbench_request_handling.py: doc_health
  excluded tests/test_doxbench_save.py: doc_health
  excluded tests/test_doxbench_scope.py: doc_health
  excluded tests/test_doxbench_share.py: doc_health
  excluded tests/test_doxbench_thread_wiring.py: doc_health
  excluded tests/test_doxbench_threads.py: doc_health
  excluded tests/test_doxbench_transport.py: doc_health
  excluded tests/test_doxbench_turns.py: status-exemption-rail
  excluded tests/test_doxchat_model_intake.py: doc_health
  excluded tests/test_edit_action.py: doc_health
  excluded tests/test_edit_project.py: doc_health
  excluded tests/test_explorer_viewer.py: doc_health
  excluded tests/test_gate_console.py: doc_health
  excluded tests/test_gate_failure_diagnostics.py: doc_health
  excluded tests/test_gateway_provenance.py: doc_health
  excluded tests/test_generated_at_anchor.py: doc_health
  excluded tests/test_generator.py: doc_health
  excluded tests/test_grouping.py: doc_health
  excluded tests/test_header_value_readers.py: doc_health
  excluded tests/test_hermeticity_gate_verbs.py: doc_health
  excluded tests/test_hosted_actor.py: doc_health
  excluded tests/test_kickoff.py: doc_health
  excluded tests/test_notebook_action.py: doc_health
  excluded tests/test_project_action_contracts.py: openxfactory-contracts
  excluded tests/test_project_aggregates.py: doc_health
  excluded tests/test_project_schema_election.py: openxfactory-contracts
  excluded tests/test_readiness_gate.py: doc_health
  excluded tests/test_register_edit_lane.py: doc_health
  excluded tests/test_renderer.py: doc_health
  excluded tests/test_repo_root_guard.py: doc_health
  excluded tests/test_repo_selector.py: doc_health
  excluded tests/test_round_trip.py: doc_health
  excluded tests/test_seam_assembly_beside_gate_and_projection.py: doc_health
  excluded tests/test_session_commits.py: doc_health
  excluded tests/test_session_confinement.py: doc_health
  excluded tests/test_session_document_ownership.py: doc_health
  excluded tests/test_session_gates.py: doc_health
  excluded tests/test_session_lifecycle.py: doc_health
  excluded tests/test_session_notebook.py: doc_health
  excluded tests/test_session_records.py: doc_health
  excluded tests/test_session_runbook.py: doc_health
  excluded tests/test_session_snapshot.py: doc_health
  excluded tests/test_session_transaction.py: doc_health
  excluded tests/test_session_verbs.py: doc_health
  excluded tests/test_snapshot.py: consumer-schemas
  excluded tests/test_snapshot_determinism.py: doc_health
  excluded tests/test_snapshot_registry.py: doc_health
  excluded tests/test_snapshot_validation_launch.py: doc_health
  excluded tests/test_source_dot_directories.py: doc_health
  excluded tests/test_staging_workbench.py: doc_health
  excluded tests/test_trust_gaps.py: doc_health
  excluded tests/test_validate_ideation_dashboard_contracts.py: openxfactory-contracts
  excluded tests/test_wheel_action_contracts.py: openxfactory-contracts
  excluded tests/test_wheel_model.py: doc_health
  excluded tests/test_wheel_verbs_cli.py: doc_health
208 passed in 18.27s
```

## 5. F9.2 (openXdox-code `6158151e`): red, as ruled

F9.2 as extracted (sha256 `fca4704fbe1c…`), run unchanged. Batch J
amends F9.1 alone, and RULED `5859927858` says "F9.2 is unchanged":

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
python -m venv --clear "$W/v9i"                      # a FRESH environment: nothing already installed stands in
. "$W/v9i/bin/activate"
pip install ".[test]"                                 # openDox arrives at the pin pyproject.toml declares
python3 - <<'PY'
import importlib.metadata as md, json, pathlib, re, tomllib
deps = tomllib.loads(pathlib.Path("pyproject.toml").read_text())["project"]["dependencies"]
pins = [d for d in deps if re.match(r"opendox\s*@", d)]
assert len(pins) == 1 and re.search(r"@[0-9a-f]{40}$", pins[0]), f"the composition names no full-commit pin: {pins}"
got = json.loads(md.distribution("opendox").read_text("direct_url.json") or "{}").get("vcs_info", {}).get("commit_id")
assert got == pins[0].rsplit("@", 1)[1], f"the installed openDox is {got!r}, not the pinned commit"
PY
ls tests/integration/test_*.py > "$W/integration.txt"  # a DECLARED integration suite exists
while read -r f; do python -m pytest -q "$f"; done < "$W/integration.txt"
python -m pytest -q "tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records"
```

**Exit 1, on the one ruled test.** The install and the pin block pass, and
`test_assembled_bundle.py` passes. `test_assembled_surface.py` fails on
`test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records`, and
`set -e` stops F9.2 there. The failure is the ruled one: `cli_gate.py:47` →
`gate_console.py:63` runs `from doc_health import corpus`, and no lone
checkout supplies `doc_health`. The file's other case,
`test_the_help_tree_is_left_out_only_while_its_stated_reason_holds`, passes. It
holds the exclusion to exactly that reason:

```
Successfully installed PyYAML-6.0.3 attrs-26.1.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 opendox-0.0.0 openxdox-0.0.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-8.4.2 referencing-0.37.0 rfc3339-validator-0.1.4 rpds-py-2026.6.3 six-1.17.0 typing-extensions-4.16.0
....                                                                     [100%]
=================== open extraction: the declared exclusion ====================
[the declared exclusion's count, its four reasons and its 67 `excluded` lines: identical to § 4's, elided]
4 passed in 5.10s
F.                                                                       [100%]
=================================== FAILURES ===================================
____ test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records ____

composition = Composition(pin='2d116415159b721b55613fe20a159afc46202d1f', web=PosixPath('<workdir…>'))
tmp_path = PosixPath('<workdir>/tmp/pytest-of-<user>/pytest-1/test_the_assembled_help_tree_i0')

    def test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records(
            composition: Composition, tmp_path: Path) -> None:
        """openDox's parser at the pin, with this column's `gate` tree contributed
        by a host's own profile, is the 31-entry tree the carve manifest records:
        the same entry points, and the golden's text byte for byte."""
        done = _assemble(tmp_path)
        last = (done.stderr.strip().splitlines() or [""])[-1]
>       assert done.returncode == 0, (
            f"at {composition}: the assembled command line could not be built. "
            f"The child ended with: {last}\n{done.stderr[-4000:]}")
E       AssertionError: at openDox-code@2d116415159b721b55613fe20a159afc46202d1f: the assembled command line could not be built. The child ended with: ModuleNotFoundError: No module named 'doc_health'
E         Traceback (most recent call last):
E           File "<string>", line 5, in <module>
E           File "<workdir>/tmp/tmp.7JYzzP8feC/v9i/lib/python3.12/site-packages/openxdox/cli_gate.py", line 47, in <module>
E             from openxdox import gate_console as gate_mod
E           File "<workdir>/tmp/tmp.7JYzzP8feC/v9i/lib/python3.12/site-packages/openxdox/gate_console.py", line 63, in <module>
E             from doc_health import corpus
E         ModuleNotFoundError: No module named 'doc_health'
E         
E       assert 1 == 0
E        +  where 1 = CompletedProcess(args=['<workdir…>", line 63, in <module>\n    from doc_health import corpus\nModuleNotFoundError: No module named \'doc_health\'\n').returncode

tests/integration/test_assembled_surface.py:207: AssertionError
=================== open extraction: the declared exclusion ====================
[the declared exclusion's count, its four reasons and its 67 `excluded` lines: identical to § 4's, elided]
=========================== short test summary info ============================
FAILED tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records
1 failed, 1 passed in 0.69s
```

**The steps `set -e` did not reach, each run on its own** (holder decision,
2026-09-29). The run is F9.2's own preamble, byte for byte (its first 14
lines, through the `ls`), then the steps without `set -e`, each with F9.2's
own per-file command and its exit code (sha256 `2a452c0e291d…`):

```sh
# --- T049 addition (holder decision, 2026-09-29): F9.2's `set -e` stops at
# test_assembled_surface.py, so the two steps after it are run here on their
# own, each with F9.2's own per-file command, and each exit code is recorded.
python3 -c "import importlib.metadata as md, json; print('=== installed opendox commit_id:', json.loads(md.distribution('opendox').read_text('direct_url.json'))['vcs_info']['commit_id'])"
set +e
while read -r f; do echo "=== F9.2 per-file: $f"; python -m pytest -q "$f"; echo "=== rc=$? for $f"; done < "$W/integration.txt"
echo "=== F9.2 final line"
python -m pytest -q "tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records"
echo "=== rc=$? for the final line"
```

So the only red is the ruled test. The installed openDox is the pinned commit.
`test_assembled_bundle.py` gives `4 passed` and `test_declared_composition.py`
`5 passed`, and `test_assembled_surface.py` and the final named-test line are
red on the help-tree test alone:

```
Successfully installed PyYAML-6.0.3 attrs-26.1.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 opendox-0.0.0 openxdox-0.0.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-8.4.2 referencing-0.37.0 rfc3339-validator-0.1.4 rpds-py-2026.6.3 six-1.17.0 typing-extensions-4.16.0
=== installed opendox commit_id: 2d116415159b721b55613fe20a159afc46202d1f
=== F9.2 per-file: tests/integration/test_assembled_bundle.py
....                                                                     [100%]
=================== open extraction: the declared exclusion ====================
[the declared exclusion's count, its four reasons and its 67 `excluded` lines: identical to § 4's, elided]
4 passed in 4.24s
=== rc=0 for tests/integration/test_assembled_bundle.py
=== F9.2 per-file: tests/integration/test_assembled_surface.py
F.                                                                       [100%]
=================================== FAILURES ===================================
____ test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records ____

composition = Composition(pin='2d116415159b721b55613fe20a159afc46202d1f', web=PosixPath('<workdir…>'))
tmp_path = PosixPath('<workdir>/tmp/pytest-of-<user>/pytest-4/test_the_assembled_help_tree_i0')

    def test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records(
            composition: Composition, tmp_path: Path) -> None:
        """openDox's parser at the pin, with this column's `gate` tree contributed
        by a host's own profile, is the 31-entry tree the carve manifest records:
        the same entry points, and the golden's text byte for byte."""
        done = _assemble(tmp_path)
        last = (done.stderr.strip().splitlines() or [""])[-1]
>       assert done.returncode == 0, (
            f"at {composition}: the assembled command line could not be built. "
            f"The child ended with: {last}\n{done.stderr[-4000:]}")
E       AssertionError: at openDox-code@2d116415159b721b55613fe20a159afc46202d1f: the assembled command line could not be built. The child ended with: ModuleNotFoundError: No module named 'doc_health'
E         Traceback (most recent call last):
E           File "<string>", line 5, in <module>
E           File "<workdir>/tmp/tmp.iJwtOtmmEk/v9i/lib/python3.12/site-packages/openxdox/cli_gate.py", line 47, in <module>
E             from openxdox import gate_console as gate_mod
E           File "<workdir>/tmp/tmp.iJwtOtmmEk/v9i/lib/python3.12/site-packages/openxdox/gate_console.py", line 63, in <module>
E             from doc_health import corpus
E         ModuleNotFoundError: No module named 'doc_health'
E         
E       assert 1 == 0
E        +  where 1 = CompletedProcess(args=['<workdir…>", line 63, in <module>\n    from doc_health import corpus\nModuleNotFoundError: No module named \'doc_health\'\n').returncode

tests/integration/test_assembled_surface.py:207: AssertionError
=================== open extraction: the declared exclusion ====================
[the declared exclusion's count, its four reasons and its 67 `excluded` lines: identical to § 4's, elided]
=========================== short test summary info ============================
FAILED tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records
1 failed, 1 passed in 0.63s
=== rc=1 for tests/integration/test_assembled_surface.py
=== F9.2 per-file: tests/integration/test_declared_composition.py
.....                                                                    [100%]
=================== open extraction: the declared exclusion ====================
[the declared exclusion's count, its four reasons and its 67 `excluded` lines: identical to § 4's, elided]
5 passed in 0.84s
=== rc=0 for tests/integration/test_declared_composition.py
=== F9.2 final line
F                                                                        [100%]
=================================== FAILURES ===================================
____ test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records ____

composition = Composition(pin='2d116415159b721b55613fe20a159afc46202d1f', web=PosixPath('<workdir…>'))
tmp_path = PosixPath('<workdir>/tmp/pytest-of-<user>/pytest-6/test_the_assembled_help_tree_i0')

    def test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records(
            composition: Composition, tmp_path: Path) -> None:
        """openDox's parser at the pin, with this column's `gate` tree contributed
        by a host's own profile, is the 31-entry tree the carve manifest records:
        the same entry points, and the golden's text byte for byte."""
        done = _assemble(tmp_path)
        last = (done.stderr.strip().splitlines() or [""])[-1]
>       assert done.returncode == 0, (
            f"at {composition}: the assembled command line could not be built. "
            f"The child ended with: {last}\n{done.stderr[-4000:]}")
E       AssertionError: at openDox-code@2d116415159b721b55613fe20a159afc46202d1f: the assembled command line could not be built. The child ended with: ModuleNotFoundError: No module named 'doc_health'
E         Traceback (most recent call last):
E           File "<string>", line 5, in <module>
E           File "<workdir>/tmp/tmp.iJwtOtmmEk/v9i/lib/python3.12/site-packages/openxdox/cli_gate.py", line 47, in <module>
E             from openxdox import gate_console as gate_mod
E           File "<workdir>/tmp/tmp.iJwtOtmmEk/v9i/lib/python3.12/site-packages/openxdox/gate_console.py", line 63, in <module>
E             from doc_health import corpus
E         ModuleNotFoundError: No module named 'doc_health'
E         
E       assert 1 == 0
E        +  where 1 = CompletedProcess(args=['<workdir…>", line 63, in <module>\n    from doc_health import corpus\nModuleNotFoundError: No module named \'doc_health\'\n').returncode

tests/integration/test_assembled_surface.py:207: AssertionError
=================== open extraction: the declared exclusion ====================
[the declared exclusion's count, its four reasons and its 67 `excluded` lines: identical to § 4's, elided]
=========================== short test summary info ============================
FAILED tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records
1 failed in 0.56s
=== rc=1 for the final line
```

## 6. `opendox --help` (openDox-code `2d116415`)

F10.1's first assertion, which is phase 1's proof of 10.1 (#1144's release
map), run through F10.1's own preamble (a plain `pip install .` into a fresh
venv, and the sibling check), which is its first seven lines as extracted
(sha256 `d94265449831…`). Then, as marked, the same command with its output
shown, and T038's second falsifier:

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
python -m venv --clear "$W/v10"                      # a FRESH environment: nothing already installed stands in
. "$W/v10/bin/activate"
pip install .
if python -c "import openxdox" 2>/dev/null; then echo "FAIL: sibling present"; exit 1; fi
opendox --help >/dev/null                       # the console script MUST exist
# --- T049 addition: F10.1's first assertion is the line above (phase 1's proof of 10.1).
# The same command again with its output shown rather than sent to /dev/null, and
# T038's second falsifier; under set -e an echo below runs only if its command exited 0.
opendox --help
echo "=== opendox --help exited 0"
opendox runtime --help >/dev/null
echo "=== opendox runtime --help exited 0"
command -v opendox opendox-runtime
```

**Exit 0.** The plain install brings PyYAML and openDox alone, `openxdox`
does not import, and both console scripts exist:

```
Successfully installed PyYAML-6.0.3 opendox-0.0.0
usage: ideation-dashboard [-h]
                          {generate,generate-and-open,create,edit,model-binding,runtime}
                          ...

`generate` + (later) `generate-and-open` action subcommands (plan "cli.py";
change task 3.3).

Path-agnostic argparse front-end: `--output`-style arguments, no baked-in
snapshot path (the aggregation nightly lane wires the committed path). The
`generate` subcommand (this wave, T006) regenerates the deterministic snapshot
from the working tree, writes it through the interactivity boundary, and
validates it against the pinned openxFactory validator. The `generate-and-open`
subcommand (T012, US2) will layer `serve.py` + browser open on top of the same
generation path.

Runnable both as a module (`python3 -m ideation_dashboard.cli`) and as a script
(`python3 scripts/ideation_dashboard/cli.py`); it self-inserts `scripts/` onto
the import path so the sibling `doc_health` package resolves either way.

positional arguments:
  {generate,generate-and-open,create,edit,model-binding,runtime}
    generate            regenerate the deterministic snapshot
    generate-and-open   regenerate the snapshot, serve it locally, and open
                        the browser
    create              scaffold a new header-compliant ideation doc and open
                        it for editing
    edit                select-to-edit: launch the human's editor over a
                        listed document
    model-binding       model-provider settings: list / add / edit / remove
                        bindings, and hand a credential to the broker
    runtime             the identity and coordination runtime (split-opendox §
                        3.5)

options:
  -h, --help            show this help message and exit
=== opendox --help exited 0
=== opendox runtime --help exited 0
<workdir>/tmp/tmp.99rjQcKfro/v10/bin/opendox
<workdir>/tmp/tmp.99rjQcKfro/v10/bin/opendox-runtime
```

## 7. F4.1's scan (openDox-code `2d116415`)

F4.1 closes in phase 3 (T084, T089), so it is not run whole here. Its
`consumer_reach.py` line is phase 3's: that file is present until T084 retires
it. T049 asks for its scan, and the scan must list only `openxdox` targets.
This is the scan block as extracted, run alone from the checkout root (sha256
`43be8317d630…`):

```sh
set -euo pipefail
python3 - src/opendox <<'PY'
import ast, pathlib, sys
FOREIGN = ("openxdox", "ideation_dashboard", "corpus_adapter_openxfactory", "doc_health")
def named(node):
    if isinstance(node, ast.Import):
        return [a.name for a in node.names]
    if isinstance(node, ast.ImportFrom):
        return [node.module] if node.level == 0 and node.module else []
    if isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant) \
            and getattr(node.func, "attr", getattr(node.func, "id", "")) in ("import_module", "__import__"):
        return [node.args[0].value] if isinstance(node.args[0].value, str) else []
    return []
def deferred(tree):                                   # every reach written INSIDE a function body
    for fn in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))):
        for node in ast.walk(fn):
            yield from ((node.lineno, name) for name in named(node))
hits = sorted({f"{p}:{line}: {name}"
               for p in pathlib.Path(sys.argv[1]).rglob("*.py")
               for line, name in deferred(ast.parse(p.read_text(), str(p)))
               if any(name == f or name.startswith(f + ".") for f in FOREIGN)})
assert not hits, f"{len(hits)} deferred reach(es) still name the consumer or the publisher:\n  " + "\n  ".join(hits)
print("no deferred reach names the consumer or the publisher")
PY
```

**Exit 1, and T049's condition holds.** It names 19 deferred reaches, and
all 19 are `openxdox` targets: `branch_session.py` 7, `serve_workbench.py` 7,
`serve.py` 2, `serve_project.py` 2 and `cli.py` 1. That is 4.3's measured
split of the 19 into openXdox exactly. None of 4.3's eight reaches into
openxFactory is left. The same scan at openDox-code `1e4a57fb`, where 4.3
measured them, names 27. The eight it names that are gone now are
`authoring.py:318`, `doxbench_packet.py:177`, `serve.py:713`,
`serve_wire.py:1369`, and `workbench.py:746` and `:1407-1409`:

```
Traceback (most recent call last):
  File "<stdin>", line 20, in <module>
AssertionError: 19 deferred reach(es) still name the consumer or the publisher:
  src/opendox/branch_session.py:1568: openxdox
  src/opendox/branch_session.py:1587: openxdox.register
  src/opendox/branch_session.py:2005: openxdox
  src/opendox/branch_session.py:2105: openxdox.snapshot_registry
  src/opendox/branch_session.py:2151: openxdox.snapshot_registry
  src/opendox/branch_session.py:2228: openxdox.snapshot_registry
  src/opendox/branch_session.py:3573: openxdox.snapshot_registry
  src/opendox/cli.py:628: openxdox.snapshot_registry
  src/opendox/serve.py:2118: openxdox.corpus_root
  src/opendox/serve.py:648: openxdox.corpus_root
  src/opendox/serve_project.py:246: openxdox.gate_console
  src/opendox/serve_project.py:247: openxdox.kickoff
  src/opendox/serve_workbench.py:1215: openxdox
  src/opendox/serve_workbench.py:1665: openxdox
  src/opendox/serve_workbench.py:2607: openxdox
  src/opendox/serve_workbench.py:347: openxdox
  src/opendox/serve_workbench.py:407: openxdox
  src/opendox/serve_workbench.py:408: openxdox
  src/opendox/serve_workbench.py:544: openxdox
```

F4.1's lines before the `consumer_reach.py` check also pass here: 4.1's,
4.1a's and 4.2's (sha256 `51a79ddd2747…`). With nothing registered
the one outcome is `CorpusRefused` of kind `ADAPTER_NOT_REGISTERED`, and both
named tests pass:

```
Successfully installed PyJWT-2.15.1 PyYAML-6.0.3 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 cffi-2.1.1 click-8.5.0 cryptography-50.0.1 fastapi-0.141.1 h11-0.16.0 httpcore-1.0.9 httptools-0.8.0 httpx-0.28.1 idna-3.20 iniconfig-2.3.0 opendox-0.0.0 packaging-26.3 pluggy-1.6.0 psycopg-3.3.6 psycopg-binary-3.3.6 psycopg-pool-3.3.3 pycparser-3.0 pydantic-2.13.5 pydantic-core-2.46.5 pygments-2.21.0 pytest-8.4.2 python-dotenv-1.2.3 starlette-1.7.0 typing-extensions-4.16.0 typing-inspection-0.4.4 uvicorn-0.54.0 uvloop-0.22.1 watchfiles-1.3.0 websockets-17.1
.                                                                        [100%]
1 passed in 0.44s
.                                                                        [100%]
1 passed in 0.18s
=== F4.1 lines 1-25 (4.1, 4.1a, 4.2) passed
=== src/opendox/consumer_reach.py is present (retired by T084, phase 3)
```

## 8. Every case T034 or T035 removed, found where its PR's list sends it

T049's check: "every module or case T034 or T035 removed, found where its PR's
list sends it: openXdox-code's `tests/integration/` or its declared exclusion,
or openxFactory, with its path in F11.1's named set".

- **The list.** opensoft/openDox-code#50 (T034, landed `71b631bc`) and #51
  (T035, landed `80acead1`) each list the cases they took out of openDox-code
  and where each one goes. Together that is 19 cases. The table's "from"
  column names the file and the commit each list quotes the case from
  (`19370adc` for #50, `68be484a` for #51). Each case is also present at its
  landing's first parent (`68be484a` for #50, `71b631bc` for #51) and absent
  at the landing. Neither landing removed a whole module: `git diff
  --name-status` over each landing shows only `M` rows.
- **How each was found.** `git grep -l -E "def <case>\("` over `tests/` at
  openxFactory `08e97c27` and at openXdox-code `6158151e`. At
  openDox-code `2d116415` the case must be absent, and it is, for all 19. A
  case sent to openXdox-code counts only if its file is an entry of
  `tests/declared_exclusion.yaml` there, and the table quotes the entry's
  reasons. A case sent to openxFactory counts only if its path is in F11.1's
  named set. The sets (`HOST`, `HOST_TESTS`, `PIN_PAIRS`, `COMPOSITION_TESTS`
  and `ADMITTED_ARC_EDITS`) are parsed out of the guard that #1144's
  `tasks.md` commits at `08e97c27`, not retyped.
- **The first run found 18.** At `e81eed62`, row 11,
  `test_worktree_container_is_gitignored_in_the_aggregation_repo`, was in no
  suite: T035 took it out of openDox-code, and T007 batch E held it out of
  #1181 ("Held, not decided against; a later task takes it up"). On the
  holder's decision (option (b), 2026-09-29) it landed first, in its own
  non-Arc openxFactory PR, opensoft/openxFactory#1203 → `08e97c27`. On a runner it skips,
  so `pytest-suite`'s `EXPECT_SKIPPED` moved from 5 to 6. Inside a fresh
  aggregation checkout it passes, and it fails once the aggregation's
  `*-worktrees/` ignore line is removed. That PR quotes all three runs. This
  re-run, at `08e97c27`, finds all 19. This PR also adds one sentence to
  batch E's `HELD OUT` paragraph in #1144's `tasks.md`, naming that landing.

| # | task | case | from (openDox-code) | its PR's list sends it to | found at | F11.1 surface |
|---|---|---|---|---|---|---|
| 1 | T034 | `test_the_model_and_the_doc_health_family_agree_on_the_contract` | `tests/test_outline_model.py` at `19370adc` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_outline_template_agreement.py` | `HOST_TESTS` |
| 2 | T034 | `test_the_roster_is_exactly_the_promoted_capabilitys_requirements` | `tests/test_doxbench_memory_gateway.py` at `19370adc` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_memory_gateway_roster.py` | `HOST_TESTS` |
| 3 | T034 | `test_the_tier_column_is_TRANSCRIBED_not_invented` | `tests/test_doxbench_memory_gateway.py` at `19370adc` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_memory_gateway_roster.py` | `HOST_TESTS` |
| 4 | T034 | `test_the_untiered_requirement_really_is_absent_from_the_tier_block` | `tests/test_doxbench_memory_gateway.py` at `19370adc` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_memory_gateway_roster.py` | `HOST_TESTS` |
| 5 | T035 | `test_saved_manifest_validates_clean_against_the_pinned_validator` | `tests/test_workbench.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_workbench_manifest_validation.py` | `HOST_TESTS` |
| 6 | T035 | `test_recipe_seeded_manifest_carries_the_recipe_block_and_validates` | `tests/test_workbench.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_workbench_manifest_validation.py` | `HOST_TESTS` |
| 7 | T035 | `test_committed_manifest_is_rejected_by_the_pinned_validator` | `tests/test_workbench.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_workbench_manifest_validation.py` | `HOST_TESTS` |
| 8 | T035 | `test_scoped_doc_health_runs_real_machinery_over_the_fixture` | `tests/test_workbench.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_workbench_scoped_doc_health.py` | `HOST_TESTS` |
| 9 | T035 | `test_scoped_doc_health_finds_a_real_missing_status` | `tests/test_workbench.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_workbench_scoped_doc_health.py` | `HOST_TESTS` |
| 10 | T035 | `test_scoped_doc_health_ignores_out_of_scope_docs` | `tests/test_workbench.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_workbench_scoped_doc_health.py` | `HOST_TESTS` |
| 11 | T035 | `test_worktree_container_is_gitignored_in_the_aggregation_repo` | `tests/test_session_harness.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_session_worktree_book_scan.py` | `HOST_TESTS` |
| 12 | T035 | `test_session_worktrees_never_reach_a_lifecycle_book` | `tests/test_session_harness.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_session_worktree_book_scan.py` | `HOST_TESTS` |
| 13 | T035 | `test_pinned_factory_paths_never_admits_a_worktree_container` | `tests/test_session_harness.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_session_worktree_book_scan.py` | `HOST_TESTS` |
| 14 | T035 | `test_the_browser_ceiling_is_pinned_to_the_RELEASED_maxLength` | `tests/test_doxbench_chat_view.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_doxbench_chat_ceiling.py` | `HOST_TESTS` |
| 15 | T035 | `test_a_pytest_run_started_inside_a_conftestless_directory_is_guarded` | `tests/test_hermeticity.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_hermeticity_probe_routes.py` | `HOST_TESTS` |
| 16 | T035 | `test_the_unittest_fallback_route_installs_the_same_guard` | `tests/test_hermeticity.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_hermeticity_probe_routes.py` | `HOST_TESTS` |
| 17 | T035 | `test_the_bare_unittest_route_is_detected_as_unguarded` | `tests/test_hermeticity.py` at `68be484a` | openxFactory | openxFactory `08e97c27` `tests/domain_profile/test_hermeticity_probe_routes.py` | `HOST_TESTS` |
| 18 | T035 | `test_an_unguarded_cli_scoped_create_is_refused` | `tests/test_hermeticity.py` at `68be484a` | openXdox-code exclusion | openXdox-code `6158151e` `tests/test_hermeticity_gate_verbs.py`, declared under `doc_health` | n/a (openXdox-code) |
| 19 | T035 | `test_the_cli_seam_with_a_fake_port_reaches_no_binary` | `tests/test_hermeticity.py` at `68be484a` | openXdox-code exclusion | openXdox-code `6158151e` `tests/test_hermeticity_gate_verbs.py`, declared under `doc_health` | n/a (openXdox-code) |

The openxFactory rows arrived in three landings. #1181 (T047, `f56c87c6`)
landed rows 1-10 and 12-14, opensoft/openxFactory#1195 (`b64ca540`) landed
rows 15-17 in `tests/domain_profile/test_hermeticity_probe_routes.py`, and
opensoft/openxFactory#1203 landed row 11.

**One record correction, and it is not a row.** T035 also ADDED a case,
`test_the_browser_ceiling_equals_the_servers_ceiling`, the openDox-code side
of the chat ceiling's triangle. T007 batch E's record put it in openxFactory's
`tests/domain_profile/test_doxbench_chat_ceiling.py`. It is in openDox-code's
own `tests/test_doxbench_chat_view.py` (`:4148` at `2d116415`), and openxFactory
names it only in that module's docstring. This PR corrects batch E's bullet in
#1144's `tasks.md` with one sentence. It is not one of the 19, because T035
added it rather than removing it.

## 9. T043's R1Q24 (a) files, and `tests/test_snapshot.py` (R1Q25 (b))

T043's triage (openXdox-code#32's body, its table of 67 red files with each
file's classes) classed three files under the status-exemption rail (class H)
and five under openxFactory's contracts (class I), and `tests/test_snapshot.py`
under the consumer's schemas (class J). Each is in `tests/declared_exclusion.yaml`
at openXdox-code `6158151e`, with its reason. The declaration was parsed as its
flow-style entry lines, and each class was compared with the entry's reasons:

```
T043's table (openXdox-code#32 body): 67 red files
declared exclusion at openXdox-code 6158151e: 67 entries
  OK  tests/test_doxbench_abstract_envelope.py: T043 class -> ['status-exemption-rail']; declared -> ['status-exemption-rail']
  OK  tests/test_doxbench_blank_reason.py: T043 class -> ['openxfactory-contracts']; declared -> ['doc_health', 'openxfactory-contracts']
  OK  tests/test_doxbench_packet.py: T043 class -> ['status-exemption-rail']; declared -> ['doc_health', 'status-exemption-rail']
  OK  tests/test_doxbench_turns.py: T043 class -> ['status-exemption-rail']; declared -> ['status-exemption-rail']
  OK  tests/test_project_action_contracts.py: T043 class -> ['openxfactory-contracts']; declared -> ['openxfactory-contracts']
  OK  tests/test_project_schema_election.py: T043 class -> ['openxfactory-contracts']; declared -> ['openxfactory-contracts']
  OK  tests/test_snapshot.py: T043 class -> ['consumer-schemas']; declared -> ['consumer-schemas']
  OK  tests/test_validate_ideation_dashboard_contracts.py: T043 class -> ['openxfactory-contracts']; declared -> ['openxfactory-contracts']
  OK  tests/test_wheel_action_contracts.py: T043 class -> ['openxfactory-contracts']; declared -> ['openxfactory-contracts']
VERDICT: every R1Q24 (a) file and tests/test_snapshot.py is declared with its reason
```

§ 4's run shows the same entries printed as an open extraction, each with its
reason (`status-exemption-rail`, 3 files; `openxfactory-contracts`, 5;
`consumer-schemas`, 1). `tests/test_declared_exclusion.py` passes inside that
run, and again by name. It holds each listed file to failing, alone, for
exactly its entry's reasons.

## 10. T018's interim F11.1

T018 recorded it in [`f11.1-phase1.txt`](f11.1-phase1.txt), at `ARC_TIP`
`f56c87c6` (T047, #1181) and under the guard as amended by RULED `5890601202`
("Named closed list"). Its amended run printed, verbatim:

```
requirement 1 holds: 0 note(s) annotated, every other path a declared surface (11.1)
```

**Re-run here.** The guard was extracted byte-for-byte from #1144's `tasks.md`
at `e81eed62` (sha256 `60beede1244b…`), where #1202 landed it. It ran in an
openxFactory clone at `e81eed62` with an empty `git status`, with
`PACKET_MERGE=94b6f7f13b45c351b9142345738965c974b7dd37` and
`ARC_TIP=f56c87c6b8d7374d93facd7dfbbf02bd89a86a8b`. `f56c87c6` is still
openxFactory's only arc landing. Exit 0, stderr empty, and the same line:

```
requirement 1 holds: 0 note(s) annotated, every other path a declared surface (11.1)
```

## T092's phase-1 notes, carried in this PR

T092 puts one `edits[].note` in `docs/opendox-carve-manifest.yaml` for each
reach a phase closed. On the holder's decision of 2026-09-28, phase 1's notes
ride in this checkpoint PR rather than in T047's. There are six notes on five
rows, for the ten reaches phase 1 closed:

- `serve.py:199` and `:206`, #1144's 2.1 import-time reaches (T011,
  openDox-code#46 → `0e88454a`);
- `serve.py:713` (T012, #47 → `27683028`);
- `authoring.py:318` (T021, #44 → `9d13bd16`);
- `doxbench_packet.py:177` and `serve_wire.py:1369` (T027, #41 → `8017cd52`);
- `workbench.py:746` and `:1407-1409` (T025, #43 → `c46430fb`, and T026,
  #39 → `582ed073`).

This PR carries no `Arc:` trailer, so F11.1's count of annotated notes never
includes these. The checks below run F11.1's content rule over them directly.

**Each reach is a carve line.** The manifest numbers its lines in the carve
blob (`carve_commit` `b075fd91`). #1144 names each reach by its line at
openDox-code `1e4a57fb`. `difflib`, run over `carve_lines.text_records()` of
the two blobs, puts every reach inside an `equal` block, so each is
byte-identical to the carve line printed beside it. The script takes a
directory holding an openxFactory clone (`oxf`) and an openDox-code clone
(`odc`):

```python
# usage: t092-reach-mapping.py <W>
# Maps each reach phase 1 closed (#1144's 2.1 and 4.3 lines, at openDox-code 1e4a57fb) to its
# line in the carve blob (openxFactory carve_commit b075fd91, the manifest's numbering), through
# an `equal` opcode of difflib over carve_lines.text_records() of the two blobs.
import difflib, pathlib, subprocess, sys
W = pathlib.Path(sys.argv[1]); CARVE = "b075fd91dc8fced8e1373825ba80220c33536bae"; AT = "1e4a57fb"
sys.path.insert(0, str(W / "oxf" / "scripts")); import carve_lines
REACHES = [("serve.py", 199), ("serve.py", 206), ("serve.py", 713), ("authoring.py", 318),
           ("workbench.py", 746), ("workbench.py", 1407), ("workbench.py", 1408), ("workbench.py", 1409),
           ("serve_wire.py", 1369), ("doxbench_packet.py", 177)]
def blob(repo, rev, path):
    return subprocess.run(["git", "-C", str(W / repo), "show", f"{rev}:{path}"], check=True, capture_output=True).stdout
for f, n in REACHES:
    carve = carve_lines.text_records(blob("oxf", CARVE, f"scripts/ideation_dashboard/{f}"))
    arrived = carve_lines.text_records(blob("odc", AT, f"src/opendox/{f}"))
    sm = difflib.SequenceMatcher(None, carve, arrived, autojunk=False)
    hit = [(i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag == "equal" and j1 <= n - 1 < j2]
    if not hit:
        print(f"{f}:{n} @{AT} -> NO equal block (the line is not byte-identical to a carve line)"); continue
    i1, i2, j1, j2 = hit[0]; k = n - 1 - j1
    print(f"{f}:{n} @{AT} -> carve line {i1 + k + 1} (equal carve[{i1}:{i2}]/arrived[{j1}:{j2}] offset {k})")
    print(f"    arrived: {arrived[n - 1].rstrip(chr(10))!r}")
    print(f"    carve  : {carve[i1 + k].rstrip(chr(10))!r}")
```

```
serve.py:199 @1e4a57fb -> carve line 171 (equal carve[170:171]/arrived[198:199] offset 0)
    arrived: 'from ideation_dashboard import serve_openxfactory_lanes  # noqa: E402'
    carve  : 'from ideation_dashboard import serve_openxfactory_lanes  # noqa: E402'
serve.py:206 @1e4a57fb -> carve line 178 (equal carve[177:184]/arrived[205:212] offset 0)
    arrived: 'from ideation_dashboard.serve_openxfactory_lanes import (  # noqa: E402,F401'
    carve  : 'from ideation_dashboard.serve_openxfactory_lanes import (  # noqa: E402,F401'
serve.py:713 @1e4a57fb -> carve line 618 (equal carve[578:627]/arrived[673:722] offset 39)
    arrived: '        from doc_health.corpus import RealGit'
    carve  : '        from doc_health.corpus import RealGit'
authoring.py:318 @1e4a57fb -> carve line 318 (equal carve[317:426]/arrived[317:426] offset 0)
    arrived: '    from corpus_adapter_openxfactory import home_corpus'
    carve  : '    from corpus_adapter_openxfactory import home_corpus'
workbench.py:746 @1e4a57fb -> carve line 745 (equal carve[70:1522]/arrived[71:1523] offset 674)
    arrived: "    from doc_health import corpus            # lazy: keeps this module's graph flat"
    carve  : "    from doc_health import corpus            # lazy: keeps this module's graph flat"
workbench.py:1407 @1e4a57fb -> carve line 1406 (equal carve[70:1522]/arrived[71:1523] offset 1335)
    arrived: '        from doc_health import DEFAULT_THRESHOLDS, corpus as dh_corpus'
    carve  : '        from doc_health import DEFAULT_THRESHOLDS, corpus as dh_corpus'
workbench.py:1408 @1e4a57fb -> carve line 1407 (equal carve[70:1522]/arrived[71:1523] offset 1336)
    arrived: '        from doc_health.families import FAMILIES'
    carve  : '        from doc_health.families import FAMILIES'
workbench.py:1409 @1e4a57fb -> carve line 1408 (equal carve[70:1522]/arrived[71:1523] offset 1337)
    arrived: '        from doc_health.runner import Context, run_suite'
    carve  : '        from doc_health.runner import Context, run_suite'
serve_wire.py:1369 @1e4a57fb -> carve line 1369 (equal carve[1206:1377]/arrived[1206:1377] offset 162)
    arrived: '    from ideation_dashboard import doxbench_contracts'
    carve  : '    from ideation_dashboard import doxbench_contracts'
doxbench_packet.py:177 @1e4a57fb -> carve line 177 (equal carve[79:1419]/arrived[79:1419] offset 97)
    arrived: '    import ideation_dashboard.doxbench_status_exemption as rail'
    carve  : '    import ideation_dashboard.doxbench_status_exemption as rail'
```

**Each note is on the entry that declares its line.** Each carve line is in
the `lines` of exactly one `edits[]` entry of its row, and that entry's note
now records the close:

```
  serve.py carve line 171: edits[0] (import rewrites), note closed: True
  serve.py carve line 178: edits[0] (import rewrites), note closed: True
  serve.py carve line 618: edits[3] (adapter calls), note closed: True
  authoring.py carve line 318: edits[0] (adapter calls), note closed: True
  workbench.py carve line 745: edits[1] (adapter calls), note closed: True
  workbench.py carve line 1406: edits[1] (adapter calls), note closed: True
  workbench.py carve line 1407: edits[1] (adapter calls), note closed: True
  workbench.py carve line 1408: edits[1] (adapter calls), note closed: True
  serve_wire.py carve line 1369: edits[0] (import rewrites), note closed: True
  doxbench_packet.py carve line 177: edits[0] (import rewrites), note closed: True
every reach's carve line is in exactly one edits[] entry, and its note records the close
```

**F11.1's content rule holds.** The rule is the guard's `notes()` and
`without_notes()`, copied from #1144's `tasks.md`, and applied to `main`'s
manifest and this PR's. With every note removed, the two are equal. Two notes
are new, and each of the other four begins with the note it extends:

```python
# usage: t092-content-rule.py <manifest-before.yaml> <manifest-after.yaml>
# F11.1's manifest content rule (notes() and without_notes() copied from the committed guard,
# #1144 tasks.md), applied to one pair of manifests instead of to each Arc landing:
# with every edits[].note removed the two documents must be equal, and a note that
# already existed may only be extended.
import copy, sys, yaml
def notes(doc):
    return [[e.get("note") for e in (row.get("edits") or [])] for row in doc["rows"]]
def without_notes(doc):
    doc = copy.deepcopy(doc)
    for row in doc["rows"]:
        for e in row.get("edits") or []:
            e.pop("note", None)
    return doc
before, after = (yaml.safe_load(open(p)) for p in sys.argv[1:3])
if without_notes(before) != without_notes(after):
    sys.exit("FAIL: the manifest changed beyond an edit's note (a row, a field, a digest)")
breach, annotated = [], 0
for row, old_row, new_row in zip(after["rows"], notes(before), notes(after)):
    for i, (old, new) in enumerate(zip(old_row, new_row)):
        if old != new:
            annotated += 1
            kind = "added" if old is None else ("extended" if (new or "").startswith(old) else "REWRITTEN")
            print(f"  {kind}: {row['source_path']} edits[{i}]")
            if kind == "REWRITTEN":
                breach.append(f"{row['source_path']} edits[{i}]: rewrote an existing note instead of extending it")
if breach:
    sys.exit("FAIL:\n  " + "\n  ".join(breach))
print(f"F11.1's manifest content rule holds: {annotated} note(s) annotated, nothing else in the manifest moved")
```

```
  extended: scripts/ideation_dashboard/authoring.py edits[0]
  added: scripts/ideation_dashboard/doxbench_packet.py edits[0]
  added: scripts/ideation_dashboard/serve.py edits[0]
  extended: scripts/ideation_dashboard/serve.py edits[3]
  extended: scripts/ideation_dashboard/serve_wire.py edits[0]
  extended: scripts/ideation_dashboard/workbench.py edits[1]
F11.1's manifest content rule holds: 6 note(s) annotated, nothing else in the manifest moved
```

`scripts/validate-carve-manifest.py` accepts the manifest:

```
OK docs/opendox-carve-manifest.yaml: phase post-shed, 456 row(s) at opensoft/openxFactory@b075fd91dc8f (opendox-carve-0), verified at 08e97c27ebc9 — 142 moved_verbatim, 176 moved_with_declared_edit, 138 not_moved; 318 digest(s) recomputed; 456 file(s) in the declared surface with none undeclared; 319 shed row(s) absent at source as declared; 4 row(s) RE-DESTINED by ruling (RULED Q6); 2 row(s) RETIRED by ruling (RULED 5656343213)
```
