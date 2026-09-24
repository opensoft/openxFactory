# Research: 034-opendox-standalone-operation

**Feature**: [`spec.md`](./spec.md) · **Plan**: [`plan.md`](./plan.md) ·
**Questions**: [`clarify-questions.md`](./clarify-questions.md)

Every figure the plan, the tasks and the questions rely on is measured here, and
each one comes with the command that reproduces it. The figures are evidence
from a single moment, 2026-09-24, and they move as the repositories move, so
T005 re-measures them before implementation starts. None of this is normative:
the ratified packet is the authority.

## R0 — The trees measured, and how to reproduce them

| repository | commit | role |
|---|---|---|
| `opensoft/openDox-code` | `1e4a57fb` | openDox code leg (`main`) |
| `opensoft/openXdox-code` | `626f2c8d` | openXdox code leg (`main`) |
| `opensoft/openDox-spec` | `8fe8c4c7` | openDox spec leg (`main`, and the openDox root's spec pin) |
| `opensoft/openXdox-spec` | `f088b097` | openXdox spec leg (`main`) |
| `opensoft/openDox` | `36ded1cd` | openDox assembly root (`main`) |
| `opensoft/openXdox` | `2f3f857d` | openXdox assembly root (`main`) |
| `opensoft/openxFactory` | `dd2466ad` | this repository (`main`; #1144 landed at `94b6f7f1`) |

After these measurements, #1144's ratification record, #1151, landed on
openxFactory `main` as `cd494e4c`. It changed lifecycle headers, ticked 1.8 and
3.0, and added the record itself. It changed no requirement text, no scenario,
and no falsifier, so none of the figures below moves. This feature's branch is
cut from `cd494e4c`.

Every block below starts from the same workspace. Scratch space is resolved at
run time and never named:

```sh
set -euo pipefail
W=$(mktemp -d)
while read -r r c; do                                   # every repository at the commit the table names, not today's main
  git clone -q "https://github.com/opensoft/$r" "$W/$r"
  git -C "$W/$r" checkout -q "$c"
done <<'REPOS'
openDox-code 1e4a57fb
openXdox-code 626f2c8d
openDox-spec 8fe8c4c7
openXdox-spec f088b097
openDox 36ded1cd
openXdox 2f3f857d
openxFactory dd2466ad
REPOS
python3 -m venv "$W/od"                                   # openDox-code alone, every extra it declares
"$W/od/bin/pip" install -q "$W/openDox-code[runtime,test]"
python3 -m venv "$W/ox"                                   # openXdox-code; openDox arrives at its pin (5c137a90)
"$W/ox/bin/pip" install -q -e "$W/openXdox-code[test]"
```

**The Group 2 simulation shim.** It is used ONLY for measurement and is never
committed anywhere. It stands in for openxFactory's lanes module so that
openDox-code's suite can be measured as though 2.1 had landed. It carries the
five route strings and an empty mixin, and nothing else:

```sh
mkdir -p "$W/shim/ideation_dashboard"
: > "$W/shim/ideation_dashboard/__init__.py"
cat > "$W/shim/ideation_dashboard/serve_openxfactory_lanes.py" <<'PY'
COMMITTED_INTENTS_ROUTE = "/committed-intents.json"
ACTIONS_REFRESH_ROUTE = "/actions/refresh"
ACTIONS_APPLY_REGISTER_EDITS_ROUTE = "/actions/apply-register-edits"
ACTIONS_DTN_SEED_ROUTE = "/actions/dtn-seed"
ACTIONS_STAGING_SEED_ROUTE = "/actions/staging-seed"
class LaneRoutes:
    pass
PY
```

The scripts named `$W/tools/*.py` below are reproduced in full in the
[Appendix](#appendix--the-measurement-scripts).

## R1 — Group 2's sweep: 53 of 56 modules import

Run from OUTSIDE the checkout, so that its `src/` is not on the path:

```sh
cd "$W"
"$W/od/bin/python" -c "import importlib.util as u, sys; sys.exit(any(u.find_spec(m) for m in ('openxdox', 'ideation_dashboard', 'doc_health', 'corpus_adapter_openxfactory')))"
"$W/od/bin/python" - <<'PY'
import importlib, pkgutil, opendox
ok, failed = 0, []
for m in pkgutil.walk_packages(opendox.__path__, "opendox."):
    try:
        importlib.import_module(m.name); ok += 1
    except Exception as e:
        failed.append(f"{m.name}: {type(e).__name__}: {e}")
print("imported", ok, "of", ok + len(failed)); print("\n".join(failed))
PY
```

It printed `imported 53 of 56`. The three failures are `opendox.cli`,
`opendox.notebook_action` and `opendox.serve`, each with
`ModuleNotFoundError: No module named 'ideation_dashboard'`. `openxdox`,
`ideation_dashboard`, `doc_health` and `corpus_adapter_openxfactory` are all
absent from that environment: the block's first line exits non-zero if any of
them can be found.

## R2 — openDox-code's plain suite: 0 passed

`cd "$W/openDox-code" && "$W/od/bin/python" -m pytest -q` printed
`11 skipped, 1305 errors`. 1,239 lines of the output name
`No module named 'ideation_dashboard'`. The packet quoted 1,298 and 1,232 at
`f8a1ece`; the head has moved since then, and the cause has not changed.

## R3 — With Group 2 simulated: 1,217 passed and 86 red, all in nine files

`cd "$W/openDox-code" && PYTHONPATH="$W/shim" "$W/od/bin/python" -m pytest -q`
printed `20 failed, 1217 passed, 13 skipped, 66 errors`. All 86 red results fall
in nine files. Each is a stale harness, a stale record, or a reach the carve left
behind in a test; none is a product defect:

| file | red | cause, from the first `E` line of each failure |
|---|---|---|
| `tests/test_doxbench_abstract_pane.py` | 28 | Node view harness (`doxbench-abstract-pane-harness.mjs`) assertions |
| `tests/test_outline_tab.py` | 25 | Node view harness (`outline-tab-harness.mjs`) assertions |
| `tests/test_doxbench_composition.py` | 13 | Node view harness (`composition-harness.mjs`) assertions |
| `tests/test_provider_boundary.py` | 12 | 16.6's three stale reasons: the runtime's `Authorization`, `Bearer ` and `access_token` literals; per-module scan suites absent from this checkout; `snapshot_registry.py` read |
| `tests/test_doxbench_memory_gateway.py` | 3 | reads `openspec/specs/…`, a path in openxFactory's tree |
| `tests/test_consumer_reach.py` | 2 | `STILL_REACHING` is stale: *"`import opendox.cli` now SUCCEEDS with no `openxdox` — good, and the record in this file is out of date"* |
| `tests/test_boundary.py` | 1 | the surface scan's pinned census is out of date |
| `tests/test_doxbench_mcp.py` | 1 | starts its MCP child as `python -m ideation_dashboard…`, an openxFactory module |
| `tests/test_outline_model.py` | 1 | imports openxFactory's `doc_health`, which makes it an integration test by requirement 9's definition |

`test_provider_boundary.py` is the file that 16.6 says *"is repaired in phase
1"*. The repair is T034.

## R4 — openDox-code's CI runs 41 of 63 modules; 22 are run by nothing

`cd "$W/openDox-code" && "$W/od/bin/python" "$W/tools/ci_coverage.py"` printed:

- The tree has 63 modules: 53 under `tests/` and 10 under `tests_runtime/`.
- The `validate` job names 37 modules. It is the only check a PR is required
  to pass (the repository ruleset requires `validate`).
- The `runtime` job runs `tests_runtime/` whole, against a Postgres service,
  and is not required.
- That leaves **22 modules that no pytest step runs**:

`test_boundary`, `test_bullseye_widget`, `test_doc_surfaces`,
`test_doxbench_abstract_pane`, `test_doxbench_bridge_live`,
`test_doxbench_chat_view`, `test_doxbench_composition`,
`test_doxbench_entrypoint`, `test_doxbench_mcp`, `test_doxbench_memory_gateway`,
`test_doxbench_tile_verbs`, `test_doxbench_view`, `test_hermeticity`,
`test_model_provider_broker`, `test_openprofiler_broker_e2e`,
`test_outline_model`, `test_outline_tab`, `test_provider_boundary`,
`test_session_git`, `test_session_harness`, `test_subcommand_extension`,
`test_workbench`.

The packet counted 26. It had not credited the `runtime` job with running
`tests_runtime/` whole. Two related measurements follow.

- **`--noconftest` appears on 18 lines of `validate.yml`: three in code and
  fifteen in comments.** F9.1's `grep -c -- --noconftest` counts every one of
  them, so the comments have to go as well (T036).
- **The root `conftest.py`'s `collect_ignore` lists 7 modules.** Six of them
  import `openxdox`: `test_doxbench_chat_view`, `test_doxbench_entrypoint`,
  `test_hermeticity`, `test_model_provider_broker`, `test_subcommand_extension`
  and `test_workbench`. The seventh, `test_session_harness`, runs a script that
  exists only in openxFactory. These are T035's work.

## R5 — The 27 deferred reaches, with the functions that make them

`cd "$W/openDox-code" && "$W/od/bin/python" "$W/tools/scan_deferred_reaches.py" src/opendox`
runs #1144's own F4.1 scan, extended to print the innermost function around
each reach. It printed `27 deferred reaches`:

| reach | target | inside | released by |
|---|---|---|---|
| `authoring.py:318` | `corpus_adapter_openxfactory` | `_classify_proposal` | phase 1 (4.1) |
| `branch_session.py:1568` | `openxdox.generator` | `_change_rows` | phase 2 (5.4) |
| `branch_session.py:1587` | `openxdox.register` | `_active_pick_fallbacks` | phase 3 |
| `branch_session.py:2005` | `openxdox.kickoff` | `proposal_state_for` | phase 3 |
| `branch_session.py:2105`, `:2151`, `:2228`, `:3573` | `openxdox.snapshot_registry` | `session_entry`, `register_session_entry`, `refresh_session_snapshot`, `refresh_main_view` | phase 2 |
| `cli.py:610` | `openxdox.snapshot_registry` | `_session_registry` | phase 2 |
| `doxbench_packet.py:177` | `ideation_dashboard.doxbench_status_exemption` | `_status_exemption` | phase 1 (seam), phase 3 (default) |
| `serve.py:629` | `openxdox.corpus_root` | `_checkout_real`, called by EVERY `build_server` (`:1687`) | phase 2 |
| `serve.py:713` | `doc_health.corpus` (`RealGit`) | `_head_of` (degrades to `None`) | phase 1 |
| `serve.py:1993` | `openxdox.corpus_root` | `_refuse_impossible_checkout_root`, called by `serve.main()` (`:2012`, `:2080`) | phase 2 |
| `serve_project.py:246`, `:247` | `openxdox.gate_console`, `openxdox.kickoff` | `_serve_project_register` | phase 3 |
| `serve_wire.py:1369` | `ideation_dashboard.doxbench_contracts` | `default_doxbench_validators` | phase 1 (seam), phase 3 (default) |
| `serve_workbench.py:347` | `openxdox.doxbench_scope` | `_is_live_session_ref` | phase 3 |
| `serve_workbench.py:407`, `:408` | `openxdox.gate_console`, `openxdox.gate_routes` | `_thread_gate` | phase 3 |
| `serve_workbench.py:544` | `openxdox.doxbench_scope` | `_handle_workbench_thread` | phase 3 |
| `serve_workbench.py:1215` | `openxdox.gate_console` | `_handle_workbench_model_approval` | phase 3 |
| `serve_workbench.py:1665` | `openxdox.doxbench_scope` | `_handle_workbench_chat_turn` | phase 3 |
| `serve_workbench.py:2607` | `openxdox.doxbench_scope` | `_handle_workbench_document_abstract` | phase 3 |
| `workbench.py:746` | `doc_health.corpus` | `session_documents` (the session notebook's membership, called from `branch_session.py:3293`) | phase 1 (R1Q9) |
| `workbench.py:1407`, `:1408`, `:1409` | `doc_health`, `.families`, `.runner` | `run_scoped_doc_health` | phase 1 (seam; refuses until Group 6) |

Eight reaches go into openxFactory: `authoring` 1, `doc_health` 5 and
`ideation_dashboard` 2. The other 19 go into openXdox, which is exactly the
`OPENDOX_BACK_IMPORTS` ratchet at openXdox-code `626f2c8d`: `branch_session`
`(0, 7)`, `cli` `(0, 1)`, `serve` `(0, 2)`, `serve_project` `(0, 2)` and
`serve_workbench` `(0, 7)`.

**One placement goes beyond the release map, and it is measured, not chosen.**
`serve.py:629` is reached by every `build_server`, so it moves with the
snapshot-source default in phase 2 (R7). The release map's own rule sets this:
*"each no later than the phase whose surface calls it"*.

## R6 — `consumer_reach`: 11 names at 65 use sites

`cd "$W/openDox-code" && "$W/od/bin/python" "$W/tools/census_consumer_reach.py"` counts
every read of a `consumer_reach` name outside `consumer_reach.py` itself: an
attribute read, or a load of an alias bound by `from … import` or by
`X = consumer_reach.Y`. It printed `total sites: 65`:

| module | uses | names |
|---|---|---|
| `serve.py` | 22 | `snapshot_registry` 18, `hosted_ref_refused` 2, `LateGateRoutes` 1, `LateProjectionRoutes` 1 |
| `branch_session.py` | 20 | `gate_console` 20 |
| `cli.py` | 18 | `gate_console` 7, `snapshot` 6, `generate_snapshot` 2, `corpus_root_refusal` 1, `is_rfc3339_datetime` 1, `scanned_roots` 1 |
| `serve_workbench.py` | 4 | `snapshot_registry` 4 |
| `workbench.py` | 1 | `find_validator` 1 |

An earlier count made while authoring this plan gave 129. That count was wrong:
it counted each alias use twice. The tokenizer confirms 65. For example,
`serve.py` holds 19 code tokens named `registry_mod`, of which one is the
binding and 18 are loads.

## R7 — A standalone `build_server` is refused at the snapshot source

This probe runs with the shim on the path (so the imports succeed) and a stand-in
host profile registered (so the profile refusal is not what gets measured):

```sh
cd "$W"
git init -q repo
printf '# a\n' > repo/a.md
git -C repo add -A
git -C repo -c user.name=f -c user.email=f@example.invalid commit -qm f
printf '{}' > snap.json
mkdir web
PYTHONPATH="$W/shim" "$W/od/bin/python" - <<'PY'
from opendox import serve, domain_profile
class P:
    SUBCOMMAND_EXTENSIONS = (); ROUTE_EXTENSIONS = (); DISPLAY = None
domain_profile.register(P())
try:
    serve.build_server("web", "snap.json", "repo", port=0); print("built")
except Exception as e:
    print("REFUSED:", type(e).__name__, str(e)[:120])
PY
```

It printed `REFUSED: ConsumerReachUnavailable 'openxdox.snapshot_registry'
belongs to openXdox, the layer that PINS this one…`, raised at `serve.py:1647`
(`registry_mod.SnapshotSource(...)`, which runs unless a `snapshot_source` is
injected). If that line were cleared, `serve.py:1687` (`_checkout_real`, which
imports `openxdox.corpus_root`) would be next. **So in phase 1 the server builds
standalone only with an injected snapshot source.** The server STARTING with
nothing else installed is phase 2's surface (T055), not phase 1's, and phase 1's
exit criteria in `plan.md` say so.

## R8 — The core parser offers five verbs, and the 31-entry golden is 11 + 20

With the same stand-in profile registered, `cli.build_parser()` builds, and its
subcommands are `create`, `edit`, `generate`, `generate-and-open` and
`model-binding`; `cli.main(["--help"])` exits 0. openxFactory's golden
`tests/ideation-dashboard/fixtures/cli-help-tree.golden.txt` holds 31
`=====` sections:

- 11 come from the core: the root, `create`, `edit`, `generate`,
  `generate-and-open`, and `model-binding` with its 5 subcommands.
- 20 are contributed by the host profile: `gate` and its 19 verbs.

Count the sections with `grep -c '^===== ' "$W/openxFactory/tests/ideation-dashboard/fixtures/cli-help-tree.golden.txt"`.

## R9 — The document surface never imports the runtime

This AST walk visits every module under `src/opendox/` except `runtime/`, and
prints each import that names `runtime`:

```sh
cd "$W/openDox-code"
"$W/od/bin/python" - <<'PY'
import ast, pathlib
root = pathlib.Path("src/opendox")
for p in sorted(root.rglob("*.py")):
    if p.relative_to(root).parts[0] == "runtime":
        continue
    for n in ast.walk(ast.parse(p.read_text(), str(p))):
        mods = [a.name for a in n.names] if isinstance(n, ast.Import) else \
               [("." * n.level) + (n.module or "")] if isinstance(n, ast.ImportFrom) else []
        for m in mods:
            if "runtime" in m:
                print(p, n.lineno, m)
PY
```

It printed exactly one line: `src/opendox/conformance_corpus.py 35
.runtime.local_git_adapter`. The runtime app declares only `/livez`, `/readyz`
and `/api/v1`, and `pyproject.toml:96-139` keeps its five packages in a separate
`runtime` extra. Both facts feed R1Q16.

## R10 — openXdox-code: 16 of 85 test files in CI, 57 that fail collection

- `cd "$W/openXdox-code" && "$W/ox/bin/python" "$W/tools/ci_coverage.py" tests` reports
  85 modules, of which `validate` names 16. `--noconftest` appears on 8 lines.
  The floors are `MIN_SELECTED 564`, `MIN_PASSED 558` and `EXPECT_SKIPPED 6`;
  the packet recorded `539/533/6` before #26 and #27 raised them.
- A plain run in the `ox` venv (`"$W/ox/bin/python" -m pytest -q`) stops at
  `57 errors during collection`:
  - 26 on `doc_health`;
  - 28 on `ideation_dashboard`;
  - 3 on `No module named 'test_gate_routes'`. These are
    `tests/test_create_project.py`, `tests/test_edit_project.py` and
    `tests/test_register_edit_lane.py`, which import a sibling test module
    that exists only in openxFactory
    (`tests/ideation-dashboard/test_gate_routes.py`).
- `tests/test_dependency_direction.py:290` (`DOC_HEALTH_SURFACE`) declares 8
  source modules that import `doc_health`: `cli_gate` (0, 1), `completeness`
  (1, 0), `corpus_root` (1, 0), `gate_console` (1, 3), `gate_routes` (0, 1),
  `generator` (3, 0), `round_trip` (1, 0) and `snapshot_registry` (1, 0).
- openxFactory has no `pyproject.toml` (`ls "$W/openxFactory/pyproject.toml"`
  fails), so `doc_health` cannot be installed as a distribution.

## R11 — The 22 protected suites

5.4a's six generator suites come from its falsifier's own glob. 12.5's sixteen
come from `git grep -l -e 'open-pr' -e 'open_pr' -e 'FakePullRequests' --
'tests/test_*.py'`. Run each suite on its own in the `ox` venv, first plain and
then with `PYTHONPATH="$W/shim"`:

| suite (5.4a ⊕ 12.5) | plain | with Group 2 simulated |
|---|---|---|
| `test_generator`, `test_snapshot_determinism`, `test_snapshot_registry`, `test_session_snapshot` (5.4a) | error | error: `doc_health` |
| `test_snapshot` (5.4a) | error: `ideation_dashboard` | 3 failed, 14 passed |
| `test_snapshot_validation_launch` (5.4a) | error: `ideation_dashboard` | 9 failed: `tests/fixtures/base-repo` is absent |
| `test_gate_loop_views` (12.5) | error: `ideation_dashboard` | **74 passed** |
| the other 15 of 12.5's set | error | error: `doc_health` |

Across all 22, the plain run errors 12 times on `ideation_dashboard` and 10
times on `doc_health`. With Group 2 simulated, 19 fail on `doc_health`.

- **`test_snapshot`'s three failures sit in the validator lookup (7.3) and in
  the schema path (7.1a and C3):**
  - `find_validator(REPO_ROOT)` returns `None`;
  - twice, `ERROR harness failure: … contracts/schemas/ideation-dashboard-snapshot.schema.yaml`
    is reported as absent.
  - Without `rfc3339-validator` installed, a missing-dependency error hides
    two of them. openXdox-code's `test` extra does not declare that package.
- **`test_snapshot_validation_launch`** needs `tests/fixtures/base-repo`, which
  is an openxFactory fixture (`tests/ideation-dashboard/fixtures/base-repo`
  there) that the carve did not bring.
- **`test_branch_session.py:1145-1154` introspects a forwarder.** With the
  shim, run
  `inspect.getsource(serve.DashboardHandler._handle_gate_action)` in the `od`
  venv:
  - the qualname is `LateGateRoutes._handle_gate_action`;
  - the source begins `def forward(self, *args: Any, **kwargs: Any)`;
  - `"session_registry=self._session_registry()" in source` is `False`.

  So the suite would fail on that assertion even once it imports (R1Q7).

## R12 — The carved files release 1 edits, and their manifest rows

Load `docs/opendox-carve-manifest.yaml` with PyYAML and select the rows whose
`destination_path` ends with each file. 318 of the 456 rows carry the fields
`destination`, `destination_path`, `disposition`, `git_mode`, `sha256`,
`source_path`, plus `edits` where there are any. The other 138 carry `reason`
and `evidence` instead.

| openDox-code file | disposition | `edits[]` (with a note) | release-1 box |
|---|---|---|---|
| `src/opendox/serve.py` | `moved_with_declared_edit` | 7 (6) | 2.1, 2.2, 4.3, 13.4a |
| `src/opendox/cli.py` | `moved_with_declared_edit` | 4 (3) | 3.2, 4.1a, 4.3 |
| `src/opendox/authoring.py` | `moved_with_declared_edit` | 1 (1) | 4.1 |
| `src/opendox/workbench.py` | `moved_with_declared_edit` | 2 (1) | 4.3 |
| `src/opendox/serve_workbench.py` | `moved_with_declared_edit` | 1 (0) | 4.3, 16.4, 16.5 |
| `src/opendox/serve_project.py` | `moved_with_declared_edit` | 1 (0) | 4.3 |
| `src/opendox/serve_wire.py` | `moved_with_declared_edit` | 1 (1) | 4.3 |
| `src/opendox/doxbench_packet.py` | `moved_with_declared_edit` | 1 (0) | 4.3 |
| `src/opendox/branch_session.py` | `moved_with_declared_edit` | 2 (1) | 4.3 |
| `src/opendox/doxbench_provider.py` | `moved_with_declared_edit` | 1 (0) | 16.1 |
| `src/opendox/doxbench_install.py` | `moved_with_declared_edit` | 1 (0) | 16.4 |
| `src/opendox/doxbench_binding.py` | **`moved_verbatim`** | **0** | 16.1, 16.2, 16.3 |
| `src/opendox/web/views/doxbench-chat.js` (likely) | **`moved_verbatim`** | **0** | 16.4 |
| `src/opendox/web/views/lens.js` (per R1Q19) | `moved_with_declared_edit` | 2 (2) | R1Q19 |
| `src/opendox/notebook_action.py` (if 2.2 touches it) | `moved_verbatim` | 0 | 2.2 |

The carved TESTS count too. Eight of R3's nine red files are
`moved_with_declared_edit` rows with 1–3 `edits[]` entries. The ninth,
`test_consumer_reach.py`, was created at the destination and has no row. Six of
the seven modules in `collect_ignore` (R4) are `moved_with_declared_edit` rows
as well; the seventh, `test_session_harness.py`, is `moved_verbatim`.

Files created at the destination have no row (RULED OQ-C): `consumer_reach.py`,
`corpus_adapter.py`, `domain_profile.py`, `display_profile.py`,
`route_extension.py`, `runtime/*.py` and the workflows. No CI job runs
`scripts/verify-carve-arrival.py` or `scripts/verify-carve-conformance.py`
against a live destination; their tests use synthetic trees. Together those two
facts are why R1Q22 was a question about discipline and not about a gate.
Brett answered it (a) in `5817152735`: the manifest records the carve as it
arrived.

## R13 — The pins, and how far they have drifted

| pin | value | read with |
|---|---|---|
| openxFactory `openDox` gitlink, `contracts/opendox-pin.yaml` | `dc7aa08f` (the openDox ROOT) | `git ls-tree HEAD openDox`; `grep '^commit:'` |
| openxFactory `openXdox` gitlink, `contracts/openxdox-pin.yaml` | `2f3f857d` (the openXdox ROOT) | same |
| openDox root `code` gitlink, `contracts/code-pin.yaml` | `d816cf06`; `main` is `1e4a57fb`, 4 commits ahead | `git -C openDox ls-tree HEAD code` |
| openDox root at `dc7aa08f`: its `code` | `d816cf06` | `git -C openDox ls-tree dc7aa08f code` |
| openXdox root `code` gitlink, `contracts/code-pin.yaml` | `626f2c8d` | as above |
| openXdox root `contracts/opendox-pin.yaml` | `dc7aa08f` (the openDox ROOT) | as above |
| openXdox-code `pyproject.toml` `opendox @ …` | `5c137a90`; 11 commits behind openDox-code `main`, whereas the packet measured 9 the day before | `git -C "$W/openDox-code" rev-list --count 5c137a90..1e4a57fb` |

`5c137a90` is an ancestor of `d816cf06`. On openDox-code, openXdox-code, openDox
and openXdox alike, the `main` ruleset's required status checks are `validate`
and nothing else. Read them with
`gh api repos/opensoft/<repo>/rules/branches/main`.

## R14 — The snapshot contract (R1Q11)

This reads openXdox-spec's
`contracts/schemas/ideation-dashboard-snapshot.schema.yaml` with PyYAML:

- the top-level `required` is `[schema_version, kind, repository, generation,
  documents, clusters, possibles, staged_topics, changes, keyword_index]`;
- `$defs.document.required` is `[id, path, stage]`;
- `stage` is a `$ref` to `$defs.lifecycle_status`, whose enum is `[brainstorm,
  staged, draft, ratified, standard, superseded, retired, record, projection]`;
- `$defs.possible.properties.state.enum` is `[latent, picked, rejected,
  superseded]`;
- `$defs.change.properties.status.enum` is `[active, archived]`.

`display_profile.py:227-231` makes the views match on `brainstorm`/`staged` and
on `latent`/`picked`/`rejected`/`superseded`.

## R15 — The chat pane and the served catalog (R1Q10, R1Q13)

- The seven tabs are `funnel`, `wheel`, `board`, `canvas`, `lens`, `docs` and
  `lineage` (`web/index.html:68-74`). The radar is the lens's bullseye widget
  (`web/views/bullseye.js`, `web/views/lens.js:318-422`).
- The chat rail lives inside the staging-workbench overlay, and the overlay
  opens ONLY from the wheel's `workbench` verb, on a grouping, candidate or
  selection tile (`web/views/wheel.js:261-282`; `app.js:1544` is its only
  caller).
- Before any turn, the rail reads the model catalog route.
  `_handle_workbench_model_catalog` (`serve_workbench.py:759`) and
  `_handle_workbench_chat_turn` (`:1515`) validate through
  `_doxbench_validators()`. By default that is `serve_wire.default_doxbench_validators`,
  which imports openxFactory's `ideation_dashboard.doxbench_contracts` and
  *"refuse[s] the two model routes"* when it is absent (`serve_wire.py:1354-1370`).
- The rail's current copy is *"chat is unavailable — no approved model is
  configured; both editors remain fully usable."*
  (`web/views/doxbench-chat.js:277-279`). It does not say how to configure a
  model, which requirement 17's third scenario asks for.

## R16 — Non-normative corrections to #1144, found while measuring

None of these changes a requirement, a scenario or a ruling. The ratification
record has landed (#1151), so each is offered to the holder for T097's
evidence notes.

1. **2.5.** *"26 modules are named by no pytest step at all"*: the number
   reached by no CI step is **22**, because the `runtime` job runs
   `tests_runtime/` whole (R4). 26 is correct for "named by no pytest step".
2. **9.4.** openXdox's floors are now `564/558/6`, not `539/533/6` (R10).
3. **4.3.** *"`workbench.py`'s four are the reaches `run_scoped_doc_health`
   makes"*: that function makes three; the fourth is `session_documents`
   (R5, R1Q9).
4. **3.2.** The proxy's refusal was written for NOTHING REGISTERED, not for "an
   ambiguous registration" (R1Q3 (i)).
5. **10.1.** Q-R4 is recorded at `runtime/cli.py:39-42`; the packet cites
   `:40-46`.
6. **9.5.** openXdox-code's openDox pin is now 11 commits behind openDox-code's
   `main`; the packet measured 9 on 2026-09-23 (R13).
7. **Group 2's heading.** 1,305 and 1,239 at `1e4a57fb`, against the packet's
   1,298 and 1,232 at `f8a1ece`. The head moved; the cause did not (R2).
8. **3.0.** It was discharged by the ratification word: `5815412869`,
   *"ratify #1144"*, which struck no requirement. design.md § D5 says
   *"ratifying this packet is the act that settles it"*. The ratification
   record ticked it (#1151 → `cd494e4c`).

## Appendix — the measurement scripts

Each script is written into `$W/tools/` from the heredoc below. They are also
persisted, byte for byte, to the lane's workspace repository (see `plan.md`
§ "Persisted tools").

```sh
mkdir -p "$W/tools"
cat > "$W/tools/ci_coverage.py" <<'PY'
"""Which test modules a leg's validate.yml names in pytest steps, and which no
pytest step reaches. Run from a code-leg checkout root.
usage: python3 ci_coverage.py [roots...]   (default: tests tests_runtime)"""
import pathlib, re, sys, yaml
roots = sys.argv[1:] or ["tests", "tests_runtime"]
wf = yaml.safe_load(pathlib.Path(".github/workflows/validate.yml").read_text())
tree = sorted(str(p) for r in roots for p in pathlib.Path(r).glob("test_*.py") if pathlib.Path(r).is_dir())
named, whole_dirs = set(), set()
for job_id, job in (wf.get("jobs") or {}).items():
    for step in job.get("steps") or []:
        code = "\n".join(l.split("#")[0] for l in (step.get("run") or "").splitlines())
        if "pytest" not in code:
            continue
        files = set(re.findall(r"tests(?:_runtime)?/test_[A-Za-z0-9_]+\.py", code))
        named |= {(job_id, f) for f in files}
        for r in roots:
            if re.search(rf"pytest[^\n]*\s{r}/?(\s|$)", code) and not files:
                whole_dirs.add((job_id, r))
print("modules in tree:", len(tree), {r: sum(1 for t in tree if t.startswith(r + "/")) for r in roots})
by_job = {}
for j, f in named:
    by_job.setdefault(j, set()).add(f)
for j, fs in sorted(by_job.items()):
    print(f"job {j}: names {len(fs)} modules")
print("jobs running a whole root:", sorted(whole_dirs))
reached = {f for _, f in named} | {t for j, r in whole_dirs for t in tree if t.startswith(r + "/")}
never = sorted(set(tree) - reached)
print("named by a pytest step:", len({f for _, f in named}), "| reached:", len(reached), "| never run:", len(never))
for n in never:
    print("  never:", n)
PY
cat > "$W/tools/scan_deferred_reaches.py" <<'PY'
"""#1144 task 4.3's scan (F4.1), extended to print each reach's innermost
enclosing function. usage: python3 scan_deferred_reaches.py src/opendox"""
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
hits = {}
for p in sorted(pathlib.Path(sys.argv[1]).rglob("*.py")):
    tree = ast.parse(p.read_text(), str(p))
    for fn in (n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))):
        for node in ast.walk(fn):
            for name in named(node):
                if any(name == f or name.startswith(f + ".") for f in FOREIGN):
                    hits[(str(p), node.lineno, name)] = getattr(fn, "name", "<lambda>")
for (p, line, name), fn in sorted(hits.items()):
    print(f"{p}:{line}: {name}  [in {fn}]")
print(len(hits), "deferred reaches")
PY
cat > "$W/tools/census_consumer_reach.py" <<'PY'
"""Every use of a consumer_reach name in openDox-code's src/opendox: an attribute
read `consumer_reach.X` (not the right-hand side of an alias binding), or a load
of a local alias bound by `from ... consumer_reach import X [as Y]` or by
`Y = consumer_reach.X`. Run from an openDox-code checkout root."""
import ast, pathlib, collections, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "src/opendox")
by_name, by_mod = collections.Counter(), collections.Counter()
detail = collections.defaultdict(collections.Counter)
for p in sorted(root.rglob("*.py")):
    if p.name == "consumer_reach.py":
        continue
    t = ast.parse(p.read_text(), str(p))
    cr_alias, aliases, rhs = set(), {}, set()
    for n in ast.walk(t):
        if isinstance(n, ast.ImportFrom):
            if (n.level == 0 and n.module == "opendox.consumer_reach") or (n.level == 1 and n.module == "consumer_reach"):
                for a in n.names:
                    aliases[a.asname or a.name] = a.name
            if (n.level == 0 and n.module == "opendox") or (n.level == 1 and n.module is None):
                cr_alias |= {a.asname or a.name for a in n.names if a.name == "consumer_reach"}
    for n in ast.walk(t):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Attribute) \
                and isinstance(n.value.value, ast.Name) and n.value.value.id in cr_alias:
            for tg in n.targets:
                if isinstance(tg, ast.Name):
                    aliases[tg.id] = n.value.attr
                    rhs.add(id(n.value))
    for n in ast.walk(t):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id in cr_alias and id(n) not in rhs:
            name = n.attr
        elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in aliases:
            name = aliases[n.id]
        else:
            continue
        by_name[name] += 1; by_mod[p.name] += 1; detail[p.name][name] += 1
print("total sites:", sum(by_mod.values()))
print("by module:", dict(by_mod.most_common()))
print("by name:", dict(by_name.most_common()))
for m, c in sorted(detail.items()):
    print(" ", m, dict(c.most_common()))
PY
cat > "$W/tools/box_census.py" <<'PY'
"""Every checkbox in #1144's tasks.md, by group, with its state and label.
A FALSIFIED BY box is labelled F<group>.<n> in document order.
usage: python3 box_census.py <tasks.md>"""
import re, sys, collections
group, rows, fcount = None, [], collections.Counter()
for line in open(sys.argv[1], encoding="utf-8"):
    g = re.match(r"^## (Group (\d+)|Follow-ons)", line)
    if g:
        group = g.group(2) or "F"
        continue
    m = re.match(r"^- \[( |x|~)\] (?:\*\*FALSIFIED BY\*\*|(\S+))", line)
    if not m:
        continue
    state, label = m.group(1), m.group(2)
    if label is None:
        fcount[group] += 1
        label = f"F{group}.{fcount[group]}"
    rows.append((group, state, label.rstrip(".")))
by = collections.defaultdict(list)
for g, s, l in rows:
    by[g].append(f"{l}[{s}]")
for g in by:
    print(g, len(by[g]), " ".join(by[g]))
print("total", len(rows), collections.Counter(s for _, s, _ in rows))
PY
```
