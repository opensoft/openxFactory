# Phase 2 checkpoint (T063)

Status: record

**Feature**: [`034-opendox-standalone-operation`](../spec.md) · **Task**: T063
([`tasks.md`](../tasks.md)) · **Run**: 2026-10-02, 22:29–22:40Z, at the landed
phase-2 commits, with F5.2 run at openxFactory `main` `2656e8c2` and again at
T064's landing `fcb45380` · **Lane**: `openxfactory-4`

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`; T091). It runs and quotes every check T063 names, at the
commits phase 2 pinned. Every check passes except F5.2, which is red on three
cases of one suite. Those three are the pre-arc reds that the holder ruled
(a) at T059, and that T061 left open for T063. How phase 2 closes with them
is the holder's decision, and it is open (below). The last section records
T092's phase-2 notes, which ride in this PR on the holder's decision (b),
recorded in T064's PR (openxFactory#1215).

## Verdict

| # | T063's check | where it ran | result |
|---|---|---|---|
| 1 | F5.1 | openXdox-code `6a3b93b9`, with openDox-code `047bb4fa` installed over it | **PASS**, exit 0 |
| 2 | F5.2, as T007's batches C, F, G and K amend it, its last step passing `--chains` | openXdox-code `6a3b93b9`, openDox-code `047bb4fa`, and `OPENXFACTORY` at `fcb45380` (and, before T064 landed, at `2656e8c2`) | **RED**, exit 1, on three cases of `tests/test_session_snapshot.py` alone: 20 passed, 3 failed. Every other suite passes whole, and the `--chains` step prints `ok: 4 protected edit(s), each entered and holding` (§ 2) |
| 3 | F5.3 | openDox-code `047bb4fa` | **PASS**, exit 0: `documents: 8` |
| 4 | F7.1, its second named test read as batch I records R1Q27 (a) | openXdox-code `6a3b93b9` | **PASS**, exit 0: `2 passed` |
| 5 | F7.2 | openDox-code `047bb4fa` | **PASS**, exit 0: the malformed corpus is refused for `[title-and-summary-are-text]` |
| 6 | a standalone `generate-and-open` serving the fixture | openDox-code `047bb4fa`, a plain install | **PASS**, exit 0: it serves the eight documents, the core routes answer, and it stops on an interrupt with status 0 (§ 6) |
| 7 | T065's interim F11.1 | openxFactory, `ARC_TIP` at T064's landing `fcb45380` | **PENDING**: T065's own PR records it in `evidence/f11.1-phase2.txt`, and § 7 quotes it once that lands |

**F5.2, and the decision that is open.** F5.2's `set -e` stops at
`tests/test_session_snapshot.py`, the second suite its glob lists, on three
cases:

- `test_a_new_serve_process_re_registers_the_session_at_startup`:
  `opendox.serve` has no `SNAPSHOT_INDEX_ROUTE`;
- `test_a_session_key_is_validated_against_the_roster_before_url_composition`:
  the node probe copies `repo-selector-model.js` alone, which imports
  `./display.js`;
- `test_the_hosted_session_arrival_path_is_recorded_and_not_built`: the route
  `_handle_refresh_action` is not on openXdox's serve surface.

They are exactly the three that openXdox-code#35's body records as the holder's
ruling (a), item 6: *"They are deselected in T059's F5.2 run with the reason
"red at both pins; pre-arc carve residue; not the arc's", and this PR does not
edit them. They stay open for F5.2 whole (T061/T063)."* That body names the
cause of each, from the carve's § 2.4 moves and openDox-code#21. T061's
record (plan 034, T061's "Landed" bullets) left them to this task: *"the three
failures are T059's ruled pre-arc reds, which T063 still owns."* The red does
not depend on openxFactory's pins: it is the same at `2656e8c2` and at
`fcb45380` (§ 2c).

No ruling yet says how phase 2 closes with F5.2 red. The question went to the
holder during this run. T063 is not ticked in plan 034 until it is
answered. The choices put were:

- **(a)** quote F5.2 red as ruled and close phase 2, moving its box to a named
  later owner in plan 034 only, as T049 did with F9.2;
- **(b)** fix the three cases first, in an openXdox-code arc landing. It edits
  a protected suite, so each fix is an R1Q7 (a) allow-list entry, and phase
  2's pins move again;
- **(c)** another course.

## The pins

Read from openxFactory at T064's landing, `fcb45380` (opensoft/openxFactory#1215):

| where | pin | resolves to |
|---|---|---|
| openxFactory `openDox` gitlink and `contracts/opendox-pin.yaml` | openDox root `d5098297` (T062, openDox#16) | `code` → openDox-code `047bb4fa` (T058's landing); `spec` → `f7ee3c76` (T053, `dox-v1.1`) |
| openxFactory `openXdox` gitlink and `contracts/openxdox-pin.yaml` | openXdox root `f257e021` (openXdox#21) | `code` → openXdox-code `6a3b93b9` (T061's landing); `spec` → `f088b097`; its own `contracts/opendox-pin.yaml` → openDox `d5098297` |
| openXdox-code `pyproject.toml` | `opendox @ git+https://github.com/opensoft/openDox-code@047bb4fa394f3e1bf42466062a67ef18e99f8d6a` | the commit F5.1 and F5.2 install over it |

At the runs, each leg's `main` was exactly its pinned commit: openDox-code
`047bb4fa`, openXdox-code `6a3b93b9`, openXdox `f257e021`, openDox `d5098297`.
The phase-2 landings these pins carry are openDox-code #53, #56, #54, #57, #58,
#59, #70, #66 and #68 (T050–T058); openXdox-code #34, #35 and #36 (T060, T059,
T061); openDox#14, #15 and #16 (T053, T062); openXdox#21; and openxFactory#1215
(T064).

## How each check ran

- **The text is #1144's own.** Each falsifier was extracted byte-for-byte from
  `openspec/changes/add-neutral-product-standalone-operability/tasks.md` at
  `2656e8c2` (sha256 `dbd52691…`, the same file at `9093fdee`), by line range,
  and dedented by its six-space block indent: F5.1 `:639-656`, F5.2
  `:698-721`, F5.3 `:861-896`, F7.1 `:1060-1078`, F7.2 `:1103-1127`, and F4.1's
  scan `:527-549`. Where T063 names an amended form, the changed lines are
  shown with their diff.
- **Each ran from a fresh clone of its leg at the pinned commit**, with an
  empty `git status --porcelain`, from the checkout root, under `bash`, and in
  the foreground. Each checkout a run is handed through a variable
  (`OPENDOX_CODE`, `OPENXFACTORY`) was clean too. pip's in-tree build leaves an
  untracked `build/` in the tree it installs from, so each tree was cleaned
  (`git clean -fdxq`) before each run.
- **Environment.** Python 3.12.3; `python` resolves to the host's Python 3.12
  interpreter through a `PATH` shim, because the host has no `python`. Node
  v24.21.0, which one of F5.2's suites runs. `TMPDIR` is a scratch directory,
  `LANG=C.UTF-8`, and `PYTHONPATH` is unset, except where F5.2's own amended
  line sets it. The session exports `FORCE_COLOR=1`, so `FORCE_COLOR`,
  `CLICOLOR` and `COLORTERM` are unset for every run, which keeps the output
  free of colour codes. In the quoted output the scratch directory's host
  path is written `<workdir>`, and the user `<user>` (Principle IV). The
  scratch directory sits inside an xFactory aggregation checkout, as at T049
  and T064.
- **pip's install log is elided.** Each block quotes the output after pip's
  last line, `Successfully installed …`, which is quoted too. The declared
  exclusion's banner, which openXdox-code's suite prints after every run, is
  quoted in full once (§ 2a) and elided after, as marked.

## 1. F5.1 (openXdox-code `6a3b93b9`, openDox-code `047bb4fa`)

As extracted (sha256 `502acdc9c06c`), run unchanged, with
`OPENDOX_CODE` an openDox-code clone at `047bb4fa`:

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
: "${OPENDOX_CODE:?set OPENDOX_CODE to an openDox-code checkout at the tip of the arc}"
python -m venv --clear "$W/v5a"
. "$W/v5a/bin/activate"
pip install ".[test]"
pip install --force-reinstall --no-deps "$OPENDOX_CODE"   # the REALIZED openDox wins over any pinned one
python3 - <<'PY'
from opendox.display_profile import STAGE_ROLES, normalize_display
from openxdox.view_extensions import DISPLAY as facet  # a MODULE value (#26), never a DomainProfile field
assert facet, "openXdox declares no DISPLAY facet"
merged, neutral = normalize_display(facet), normalize_display(None)
done = merged["stages"]["completion"]
assert done["short"] == "implemented" and done["label"] == "implemented", done
assert neutral["stages"]["completion"]["short"] == "completed"   # the neutral word stands
for role in (r for r in STAGE_ROLES if r != "completion"):
    assert merged["stages"][role] == neutral["stages"][role], f"{role} was overlaid too"
PY
```

**Exit 0.** The block prints nothing past the installs when its assertions
hold. A second run (sha256 `dd6b35213abf`) appends these lines after
the block's last line, so they run only if every assertion held, and they
print the values the assertions read:

```diff
18a19,29
> # --- T063 addition: the block above is F5.1 unchanged. Under set -e the lines below run only if
> # every assertion above held. They print the values those assertions read.
> python3 - <<'PY'
> from opendox.display_profile import STAGE_ROLES, normalize_display
> from openxdox.view_extensions import DISPLAY as facet
> merged, neutral = normalize_display(facet), normalize_display(None)
> print("=== the facet's completion stage:", {k: merged["stages"]["completion"][k] for k in ("short", "label")})
> print("=== the neutral completion stage:", {k: neutral["stages"]["completion"][k] for k in ("short", "label")})
> print("=== stages equal to the neutral ones:", [r for r in STAGE_ROLES if merged["stages"][r] == neutral["stages"][r]])
> print("=== the facet's top-level keys:", sorted(facet))
> PY
```

The facet names the completion stage "implemented" in both rendered names,
the neutral word stands, and the other five stages are the neutral ones. The
facet's `values` block sits beside its one stage (batch I, R1Q26 (a)), and
the falsifier reads only the stages:

```
Successfully installed PyYAML-6.0.3 attrs-26.1.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 opendox-0.0.0 openxdox-0.0.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-8.4.2 referencing-0.37.0 rfc3339-validator-0.1.4 rpds-py-2026.6.3 six-1.17.0 typing-extensions-4.16.0
Successfully installed opendox-0.0.0
=== the facet's completion stage: {'short': 'implemented', 'label': 'implemented'}
=== the neutral completion stage: {'short': 'completed', 'label': 'completed'}
=== stages equal to the neutral ones: ['source', 'grouping', 'candidate', 'selection', 'submission']
=== the facet's top-level keys: ['stages', 'values']
```

## 2. F5.2, as amended (openXdox-code `6a3b93b9`, openDox-code `047bb4fa`, openxFactory `fcb45380`)

F5.2 as extracted (sha256 `808619e066fa`), with two amendments:

- **Batch G** (`5850003126`, R1Q23 (a)): after the two installs, the block
  requires `OPENXFACTORY`, an openxFactory checkout, puts
  `"$OPENXFACTORY/scripts"` on `PYTHONPATH`, and quotes that checkout's commit.
- **Batches C, F and K** (`5817152735` R1Q7 (a); `5850003126` R1Q14 (a);
  `5916000030` item 4): the last step, the inline Python that intersected the
  landings' paths with the suites, becomes the reviewed allow-list check that
  T059 wired and T061 extended. It passes `--chains`, which only F5.2's call
  does (`scripts/protected_suites.py`'s docstring: *"The last step, the inline
  Python that intersected them, becomes this call"*).

The run (sha256 `4b1512c26814`) is the extracted block with those lines
changed:

```diff
7a8,11
> # --- AS AMENDED, T007 batch G (5850003126, R1Q23 (a)): after the two installs, compose openxFactory at a NAMED commit.
> : "${OPENXFACTORY:?set OPENXFACTORY to an openxFactory checkout at a named commit}"
> export PYTHONPATH="$OPENXFACTORY/scripts"                                  # doc_health lives in that directory
> echo "=== OPENXFACTORY (an openxFactory checkout) at $(git -C "$OPENXFACTORY" rev-parse HEAD)"
17,24c21,23
< python3 - "$W/x-paths.txt" "$W/gen-suites.txt" <<'PY'
< import sys
< touched = {l.strip() for l in open(sys.argv[1]) if l.strip()}
< suites = {l.strip() for l in open(sys.argv[2]) if l.strip()}
< edited = sorted(touched & suites)
< if edited:
<     sys.exit("FAIL: the arc edited the governed projection's own proofs: " + ", ".join(edited))
< PY
---
> # --- AS AMENDED, T007 batches C, F and K (5817152735 R1Q7 (a); 5850003126 R1Q14 (a); 5916000030 item 4): the last step,
> # the inline Python that intersected the two lists, becomes the reviewed allow-list check, passing --chains.
> python3 scripts/protected_suites.py --chains --landings="$(cat "$W/x-arc.txt")" --suites="$(cat "$W/gen-suites.txt")"
```

`ARC_BASE` is openXdox-code's, `e28930bf` (T003, [`arc-base.md`](arc-base.md)).

**The composed checkout must have its `openDox` gitlink initialized.** The
first attempt pointed `OPENXFACTORY` at a fresh clone with no submodules, and
openXdox-code's `tests/conftest.py` refused at import, because openxFactory's
adapter reads openDox's pinned interface out of the nested gitlink:

```
ImportError while loading conftest '<workdir>/openXdox-code/tests/conftest.py'.
tests/conftest.py:413: in <module>
<workdir>/oxf-run/scripts/corpus_adapter_openxfactory/__init__.py:27: in <module>
<workdir>/oxf-run/scripts/corpus_adapter_openxfactory/adapter.py:68: in <module>
E   ImportError: corpus_adapter_openxfactory.adapter: the pinned openDox corpus-adapter interface is not at <workdir>/oxf-run/openDox/code/src/opendox/corpus_adapter.py. Run `git submodule update --init --recursive openDox` from the repository root (openDox nests `code` as its own gitlink).
```

So each `OPENXFACTORY` below is a clone with `openDox` and `openXdox`
initialized recursively at its own gitlinks. At `fcb45380` those are openDox
`d5098297` (code `047bb4fa`, spec `f7ee3c76`) and openXdox `f257e021` (code
`6a3b93b9`, spec `f088b097`): the same commits under test.

### 2a. The run, at T064's landing

**Exit 1.** `ls` sorts `tests/test_session_snapshot.py` second, after
`tests/test_generator.py` (45 passed). It gives 20 passed and 3 failed, and
`set -e` stops F5.2 there:

```
Successfully installed PyYAML-6.0.3 attrs-26.1.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 opendox-0.0.0 openxdox-0.0.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-8.4.2 referencing-0.37.0 rfc3339-validator-0.1.4 rpds-py-2026.6.3 six-1.17.0 typing-extensions-4.16.0
Successfully installed opendox-0.0.0
=== OPENXFACTORY (an openxFactory checkout) at fcb45380a4d9d4933038157411944c4fefa59d13
.............................................                            [100%]
=================== open extraction: the declared exclusion ====================
declared exclusion: 65 files, listed in tests/declared_exclusion.yaml. 64 are left out of this run, and 1 is collected all the same, since pytest collects a file named on the command line whatever collect_ignore says. It is an OPEN extraction: each file runs again once its reason is cleared.
  reason doc_health (59 files): reaches openxFactory's doc_health, which openxFactory packages nowhere and no lone checkout supplies; open until the doc_health direction arc (plan 034 T008); ruled R1Q6 (d), openxFactory#656 comment 5817152735
  reason status-exemption-rail (3 files): needs openxFactory's status-exemption rail, which only openxFactory registers at openDox's status-exemption seam; open until the doc_health direction arc (plan 034 T008); ruled R1Q24 (a), openxFactory#656 comment 5850003126
  reason openxfactory-contracts (5 files): reads openxFactory's contracts (the contract family's validator, schemas and examples, or its contracts/manifest.yaml) where openxFactory's tree keeps them, which is outside this checkout; open until the doc_health direction arc (plan 034 T008); ruled R1Q24 (a), openxFactory#656 comment 5850003126
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
  collected tests/test_generator.py: doc_health
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
45 passed in 2.60s
..............F.F....F.                                                  [100%]
=================================== FAILURES ===================================
_________ test_a_new_serve_process_re_registers_the_session_at_startup _________

scratch_repo = ScratchRepo(root=PosixPath('<workdir>/tmp/F5.2-post/pytest-of-<user…>/pytest-1/test_a_new_serve_process_re_re0/openxFactory-worktrees'), repository='openxFactory', topic_id='demo-topic')
tmp_path = PosixPath('<workdir>/tmp/F5.2-post/pytest-of-<user>/pytest-1/test_a_new_serve_process_re_re0')

    def test_a_new_serve_process_re_registers_the_session_at_startup(scratch_repo,
                                                                     tmp_path):
        """quickstart step 3, which is deliberately a NEW serve process after the CLI
        opened the session: the fresh process must re-derive the
        `(repository, draft/demo-topic)` entry before it can answer anything. If the
        session ref 404s here, the bootstrap is missing — that is the bug, not a stale
        session."""
        payload = _create(scratch_repo, _registry_with_main(scratch_repo, tmp_path,
                                                            name="a.json")[0])
        main_path = _main_snapshot_file(scratch_repo, tmp_path / "served.json")
    
        with _serving(scratch_repo, main_path) as (host, port, _httpd):
            status, headers, body = _get(host, port, f"{serve_mod.SNAPSHOT_ROUTE}"
                                                     f"?repository={REPO}&ref={DRAFT}")
>           _i, _ih, ibody = _get(host, port, serve_mod.SNAPSHOT_INDEX_ROUTE)
                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AttributeError: module 'opendox.serve' has no attribute 'SNAPSHOT_INDEX_ROUTE'. Did you mean: 'SNAPSHOT_ROUTE'?

tests/test_session_snapshot.py:594: AttributeError
__ test_a_session_key_is_validated_against_the_roster_before_url_composition ___

scratch_repo = ScratchRepo(root=PosixPath('<workdir>/tmp/F5.2-post/pytest-of-<user…>/pytest-1/test_a_session_key_is_validate0/openxFactory-worktrees'), repository='openxFactory', topic_id='demo-topic')
tmp_path = PosixPath('<workdir>/tmp/F5.2-post/pytest-of-<user>/pytest-1/test_a_session_key_is_validate0')

    def test_a_session_key_is_validated_against_the_roster_before_url_composition(
            scratch_repo, tmp_path):
        """FR-014, G11: a session ref entering the UI's key space is validated on the
        SAME path PR #48 added for the selector's stored key — membership in the index
        roster plus the character allow-list — and a session introduces no bypass. The
        roster here is the real serving index, session row included."""
        registry, _ = _registry_with_main(scratch_repo, tmp_path)
        _create(scratch_repo, registry)
    
>       r = _run_model(registry.index_document(), tmp_path)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test_session_snapshot.py:669: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

index = {'active': {'ref': 'main', 'repository': 'openxFactory'}, 'entries': [{'available': True, 'display_name': 'openxFactor...', 'ref': 'main', ...}], 'generated_at': '2026-10-02T22:39:30+00:00', 'kind': 'ideation-dashboard-snapshot-index', ...}
tmp_path = PosixPath('<workdir>/tmp/F5.2-post/pytest-of-<user>/pytest-1/test_a_session_key_is_validate0')

    def _run_model(index, tmp_path):
        if not NODE:
            pytest.skip("node not available for the JS derivation probe")
        shutil.copy(MODEL_JS, tmp_path / "repo-selector-model.mjs")
        (tmp_path / "harness.mjs").write_text(_NODE_HARNESS, encoding="utf-8")
        data = tmp_path / "index.json"
        data.write_text(json.dumps(index), encoding="utf-8")
        proc = subprocess.run([NODE, str(tmp_path / "harness.mjs"), str(data)],
                              capture_output=True, text=True, cwd=tmp_path)
>       assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
E       AssertionError: node harness failed:
E         node:internal/modules/esm/resolve:272
E             throw new ERR_MODULE_NOT_FOUND(
E                   ^
E         
E         Error [ERR_MODULE_NOT_FOUND]: Cannot find module '<workdir>/tmp/F5.2-post/pytest-of-<user>/pytest-1/test_a_session_key_is_validate0/display.js' imported from <workdir>/tmp/F5.2-post/pytest-of-<user>/pytest-1/test_a_session_key_is_validate0/repo-selector-model.mjs
E             at finalizeResolution (node:internal/modules/esm/resolve:272:11)
E             at moduleResolve (node:internal/modules/esm/resolve:879:10)
E             at defaultResolve (node:internal/modules/esm/resolve:1006:11)
E             at #cachedDefaultResolve (node:internal/modules/esm/loader:705:20)
E             at #resolveAndMaybeBlockOnLoaderThread (node:internal/modules/esm/loader:725:38)
E             at ModuleLoader.resolveSync (node:internal/modules/esm/loader:763:56)
E             at #resolve (node:internal/modules/esm/loader:687:17)
E             at ModuleLoader.getOrCreateModuleJob (node:internal/modules/esm/loader:607:35)
E             at ModuleJob.syncLink (node:internal/modules/esm/module_job:276:33)
E             at ModuleJob.link (node:internal/modules/esm/module_job:381:17) {
E           code: 'ERR_MODULE_NOT_FOUND',
E           url: 'file://<workdir>/tmp/F5.2-post/pytest-of-<user>/pytest-1/test_a_session_key_is_validate0/display.js'
E         }
E         
E         Node.js v24.21.0
E         
E       assert 1 == 0
E        +  where 1 = CompletedProcess(args=['<node>', '<workdir>/tmp/F5.2-pos...work/T063/tmp/F5.2-post/pytest-of-<user>/pytest-1/test_a_session_key_is_validate0/display.js'\n}\n\nNode.js v24.21.0\n").returncode

tests/test_session_snapshot.py:656: AssertionError
________ test_the_hosted_session_arrival_path_is_recorded_and_not_built ________

    def test_the_hosted_session_arrival_path_is_recorded_and_not_built():
        """FR-048's second half: the (repository, ref) seam is named as the FUTURE
        binding point, at the refusal site, and the binding is NOT built here. The
        assertion is deliberately on the refusal site's own comment — that is where
        the next reader will be standing when they ask "why can this not be hosted?"
        """
        # REPOINTED by `split-opendox-two-layer-product` § 2.4 PR 3 of 4, disclosed
        # in that PR's body. Every anchor below used to be read out of `serve.py`
        # alone. PR 3 moved `hosted_ref_refused` itself into `serve_wire.py` (both
        # openXdox's projection column and the openxFactory lane column read it, and
        # a column importing `serve` is the cycle `serve_wire` exists to prevent),
        # `_serve_snapshot`/`_serve_source` into `serve_projection.py` and
        # `_handle_refresh_action` into `serve_openxfactory_lanes.py`. Pointed at one
        # file this test would have failed outright, and narrowed to that file's
        # remaining content it would have gone hollow. It reads the whole serve
        # surface instead — the same widening the `apply_lane` absence below already
        # took, at the same strength: the definition, its named prose, the call-site
        # floor and the per-route bodies are all still asserted.
        src = serve_surface_source()
        marker = "def hosted_ref_refused("
        assert marker in src
        block = src.split(marker, 1)[1].split("\ndef ", 1)[0]
        assert "add-ideation-intent-plane" in block
        assert "apply-lane" in block
        assert "(repository, ref)" in block
        # RECORDED, not built: no apply-lane binding exists anywhere in the serve.
        # This is an ABSENCE over the whole serve (`split-opendox-two-layer-
        # product` § 2.4 made it seven files), so it is asserted over the surface,
        # not just this one file — widened, never narrowed, per the standing
        # ruling for this slice.
        assert "apply_lane" not in src
        # every route that accepts a ref asks the one predicate
        assert src.count("hosted_ref_refused(") >= 4   # the definition + 3 call sites
        for route in ("_serve_snapshot", "_serve_source", "_handle_refresh_action"):
>           body = src.split(f"def {route}(", 1)[1].split("\n    def ", 1)[0]
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           IndexError: list index out of range

tests/test_session_snapshot.py:861: IndexError
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 2a, elided. Its one `collected` line, naming the file this run collects although the exclusion lists it, is:]
  collected tests/test_session_snapshot.py: doc_health
=========================== short test summary info ============================
FAILED tests/test_session_snapshot.py::test_a_new_serve_process_re_registers_the_session_at_startup
FAILED tests/test_session_snapshot.py::test_a_session_key_is_validated_against_the_roster_before_url_composition
FAILED tests/test_session_snapshot.py::test_the_hosted_session_arrival_path_is_recorded_and_not_built
3 failed, 20 passed in 8.76s
```

### 2b. The steps `set -e` did not reach, each run on its own

T049's precedent (the holder's decision of 2026-09-29, for F9.2). The run is
F5.2's preamble as amended, byte for byte (its first 12 lines, through the
`ls`), then every later step without `set -e`, each with the block's own
command and its exit code (sha256 `7097e084d9ea`):

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
: "${OPENDOX_CODE:?set OPENDOX_CODE to an openDox-code checkout at the tip of the arc}"
python -m venv --clear "$W/v5b"
. "$W/v5b/bin/activate"
pip install ".[test]"
pip install --force-reinstall --no-deps "$OPENDOX_CODE"   # the REALIZED openDox wins over any pinned one
# --- AS AMENDED, T007 batch G (5850003126, R1Q23 (a)): after the two installs, compose openxFactory at a NAMED commit.
: "${OPENXFACTORY:?set OPENXFACTORY to an openxFactory checkout at a named commit}"
export PYTHONPATH="$OPENXFACTORY/scripts"                                  # doc_health lives in that directory
echo "=== OPENXFACTORY (an openxFactory checkout) at $(git -C "$OPENXFACTORY" rev-parse HEAD)"
ls tests/test_generator.py tests/test_snapshot*.py tests/test_session_snapshot.py > "$W/gen-suites.txt"
# --- T063 addition (T049's precedent, 2026-09-29): F5.2's `set -e` stops at tests/test_session_snapshot.py,
# the second suite `ls` lists, so every step after the preamble above is run here on its own, each with its
# own command from the block and its exit code.
python3 -c "import importlib.metadata as md; print('=== installed opendox from:', md.distribution('opendox').read_text('direct_url.json'))"
echo "=== the protected suites, as the glob selects them:"; cat "$W/gen-suites.txt"
set +e
while read -r f; do echo "=== F5.2 per-suite: $f"; python -m pytest -q "$f"; echo "=== rc=$? for $f"; done < "$W/gen-suites.txt"
: "${ARC_BASE:?set ARC_BASE to the commit of this repository before the first landing of the arc here}"
git log --first-parent --format=%H --grep='^Arc: neutral-product-standalone-operability$' "$ARC_BASE..HEAD" > "$W/x-arc.txt"   # LANDINGS (11.0)
echo "=== rc=$? for the landings' git log; the arc's landings here, oldest last:"
while read -r c; do git log -1 --format='  %H %s' "$c"; done < "$W/x-arc.txt"
test -s "$W/x-arc.txt"
echo "=== rc=$? for test -s"
: > "$W/x-paths.txt"
while read -r c; do
  git diff --name-only "$c^1" "$c" >> "$W/x-paths.txt"
done < "$W/x-arc.txt"
echo "=== protected suites the landings touched (the block's own intersection, shown, not enforced):"
sort -u "$W/x-paths.txt" | /bin/grep -Fx -f "$W/gen-suites.txt"
python3 scripts/protected_suites.py --chains --landings="$(cat "$W/x-arc.txt")" --suites="$(cat "$W/gen-suites.txt")"
echo "=== rc=$? for the --chains step"
```

So the only red is those three cases. The installed openDox is the
`OPENDOX_CODE` checkout at `047bb4fa`. The seven suites the glob selects (seven
since T005, `e28930bf`) are all run. Six pass whole: `test_generator` 45,
`test_snapshot` 18, `test_snapshot_determinism` 6, `test_snapshot_registry`
40, `test_snapshot_validation_launch` 9 and `test_snapshot_validator_home`
12. The arc has eight landings here, so `test -s` holds (11.0). Four protected
suites were touched by them, and the `--chains` step admits each by its
entries and exits 0. That covers T059's respelling (entry 3), batch F's two
(entries 4 and 6) and batch K's chains (entries 5 and 7–15):

```
Successfully installed PyYAML-6.0.3 attrs-26.1.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 opendox-0.0.0 openxdox-0.0.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-8.4.2 referencing-0.37.0 rfc3339-validator-0.1.4 rpds-py-2026.6.3 six-1.17.0 typing-extensions-4.16.0
Successfully installed opendox-0.0.0
=== OPENXFACTORY (an openxFactory checkout) at fcb45380a4d9d4933038157411944c4fefa59d13
=== installed opendox from: {"dir_info": {}, "url": "file://<workdir>/openDox-code"}
=== the protected suites, as the glob selects them:
tests/test_generator.py
tests/test_session_snapshot.py
tests/test_snapshot.py
tests/test_snapshot_determinism.py
tests/test_snapshot_registry.py
tests/test_snapshot_validation_launch.py
tests/test_snapshot_validator_home.py
=== F5.2 per-suite: tests/test_generator.py
.............................................                            [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 2a, elided. Its one `collected` line, naming the file this run collects although the exclusion lists it, is:]
  collected tests/test_generator.py: doc_health
45 passed in 2.21s
=== rc=0 for tests/test_generator.py
=== F5.2 per-suite: tests/test_session_snapshot.py
..............F.F....F.                                                  [100%]
[the three failures' tracebacks: identical to § 2a's, elided]
=========================== short test summary info ============================
FAILED tests/test_session_snapshot.py::test_a_new_serve_process_re_registers_the_session_at_startup
FAILED tests/test_session_snapshot.py::test_a_session_key_is_validated_against_the_roster_before_url_composition
FAILED tests/test_session_snapshot.py::test_the_hosted_session_arrival_path_is_recorded_and_not_built
3 failed, 20 passed in 8.96s
=== rc=1 for tests/test_session_snapshot.py
=== F5.2 per-suite: tests/test_snapshot.py
..................                                                       [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 2a, elided. It has no `collected` line here, since the file this run names is not in the exclusion]
18 passed in 1.26s
=== rc=0 for tests/test_snapshot.py
=== F5.2 per-suite: tests/test_snapshot_determinism.py
......                                                                   [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 2a, elided. Its one `collected` line, naming the file this run collects although the exclusion lists it, is:]
  collected tests/test_snapshot_determinism.py: doc_health
6 passed in 0.72s
=== rc=0 for tests/test_snapshot_determinism.py
=== F5.2 per-suite: tests/test_snapshot_registry.py
........................................                                 [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 2a, elided. Its one `collected` line, naming the file this run collects although the exclusion lists it, is:]
  collected tests/test_snapshot_registry.py: doc_health
40 passed in 2.07s
=== rc=0 for tests/test_snapshot_registry.py
=== F5.2 per-suite: tests/test_snapshot_validation_launch.py
.........                                                                [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 2a, elided. Its one `collected` line, naming the file this run collects although the exclusion lists it, is:]
  collected tests/test_snapshot_validation_launch.py: doc_health
9 passed in 0.86s
=== rc=0 for tests/test_snapshot_validation_launch.py
=== F5.2 per-suite: tests/test_snapshot_validator_home.py
............                                                             [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 2a, elided. It has no `collected` line here, since the file this run names is not in the exclusion]
12 passed in 0.55s
=== rc=0 for tests/test_snapshot_validator_home.py
=== rc=0 for the landings' git log; the arc's landings here, oldest last:
  6a3b93b93cd647ea0c62aa7bb5cdff529a2c35e8 T061, the consumer's validator located through the installed distribution (7.3) (plan 034) (#36)
  839492d905f470903cc80421fd536826f78cbcde T059, openXdox contributes its governed generator, registry and source through openDox's seams (5.4a) (plan 034) (#35)
  c41063d6aaada96258331ef39c9978fdf10a154b T060, openXdox's facet carries the governed snapshot values (5.3a) (plan 034) (#34)
  6158151e7f5202e1894f13365702daedca88cc26 Plan 034 T044 (P1-J): the six doc_health skips assert for real in a declared file; the triple 885/881/4 (#33)
  4610bca5f6dd462936d54687499165715e04d73a Plan 034 T043 (P1-J): the required check runs the whole suite, less the declared exclusion (#32)
  4e16db95ff9e6c531dfbe79f517e0384399b947c Plan 034 T042 (P1-J): tests/integration/ at the declared composition; stacked on #30, and the 31-entry tree needs a ruling (#31)
  5fbd188ed4fe3681e189fafe49d7d0699d70a2ee Plan 034 T041 (P1-J): the declared exclusion, 66 files each held to its reason; stacked on #29 (#30)
  d84b5048955add697dcf2f60bd3e4244500d0a49 Plan 034 T040 (P1-I): clear the carve residue, classes B–G, and declare rfc3339-validator; the opendox pin bump waits on P1-R (#29)
=== rc=0 for test -s
=== protected suites the landings touched (the block's own intersection, shown, not enforced):
tests/test_session_snapshot.py
tests/test_snapshot.py
tests/test_snapshot_validation_launch.py
tests/test_snapshot_validator_home.py
admitted: 839492d905f4 tests/test_session_snapshot.py, by entry 3 of tests/protected_suite_respellings.yaml
admitted: 6a3b93b93cd6 tests/test_snapshot.py, by entries 4, 5, in that order, of tests/protected_suite_respellings.yaml
admitted: 6a3b93b93cd6 tests/test_snapshot_validation_launch.py, by entries 7, 8, 9, 10, 11, 12, 13, 14, 15, in that order, of tests/protected_suite_respellings.yaml
admitted: 6a3b93b93cd6 tests/test_snapshot_validator_home.py, by entry 6 of tests/protected_suite_respellings.yaml
ok: 4 protected edit(s), each entered and holding
=== rc=0 for the --chains step
```

### 2c. The same two runs before T064 landed (`OPENXFACTORY` at `2656e8c2`)

Run first, at openxFactory `main` `2656e8c2`, whose pins were still openDox
`663ac683` (code `2d116415`) and openXdox `57e2b8f2` (code `6158151e`). The
results are the same, case for case, so the three reds do not depend on the
composed openxFactory. The block exits 1 at the same suite. Its summary
lines, selected from the run, are:

```
=== OPENXFACTORY (an openxFactory checkout) at 2656e8c254ec76d012142a02be9e3282bc342f9b
45 passed in 2.49s
FAILED tests/test_session_snapshot.py::test_a_new_serve_process_re_registers_the_session_at_startup
FAILED tests/test_session_snapshot.py::test_a_session_key_is_validated_against_the_roster_before_url_composition
FAILED tests/test_session_snapshot.py::test_the_hosted_session_arrival_path_is_recorded_and_not_built
3 failed, 20 passed in 8.35s
```

and the unreached steps give the same per-suite counts and the same
`--chains` verdict (the summary lines again):

```
=== OPENXFACTORY (an openxFactory checkout) at 2656e8c254ec76d012142a02be9e3282bc342f9b
=== F5.2 per-suite: tests/test_generator.py
45 passed in 2.92s
=== rc=0 for tests/test_generator.py
=== F5.2 per-suite: tests/test_session_snapshot.py
FAILED tests/test_session_snapshot.py::test_a_new_serve_process_re_registers_the_session_at_startup
FAILED tests/test_session_snapshot.py::test_a_session_key_is_validated_against_the_roster_before_url_composition
FAILED tests/test_session_snapshot.py::test_the_hosted_session_arrival_path_is_recorded_and_not_built
3 failed, 20 passed in 9.00s
=== rc=1 for tests/test_session_snapshot.py
=== F5.2 per-suite: tests/test_snapshot.py
18 passed in 1.65s
=== rc=0 for tests/test_snapshot.py
=== F5.2 per-suite: tests/test_snapshot_determinism.py
6 passed in 0.79s
=== rc=0 for tests/test_snapshot_determinism.py
=== F5.2 per-suite: tests/test_snapshot_registry.py
40 passed in 2.57s
=== rc=0 for tests/test_snapshot_registry.py
=== F5.2 per-suite: tests/test_snapshot_validation_launch.py
9 passed in 1.22s
=== rc=0 for tests/test_snapshot_validation_launch.py
=== F5.2 per-suite: tests/test_snapshot_validator_home.py
12 passed in 0.73s
=== rc=0 for tests/test_snapshot_validator_home.py
=== rc=0 for the landings' git log; the arc's landings here, oldest last:
=== rc=0 for test -s
admitted: 839492d905f4 tests/test_session_snapshot.py, by entry 3 of tests/protected_suite_respellings.yaml
admitted: 6a3b93b93cd6 tests/test_snapshot.py, by entries 4, 5, in that order, of tests/protected_suite_respellings.yaml
admitted: 6a3b93b93cd6 tests/test_snapshot_validation_launch.py, by entries 7, 8, 9, 10, 11, 12, 13, 14, 15, in that order, of tests/protected_suite_respellings.yaml
admitted: 6a3b93b93cd6 tests/test_snapshot_validator_home.py, by entry 6 of tests/protected_suite_respellings.yaml
ok: 4 protected edit(s), each entered and holding
=== rc=0 for the --chains step
```

## 3. F5.3 (openDox-code `047bb4fa`)

As extracted (sha256 `e3c082902540`), run unchanged:

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
python -m venv --clear "$W/v5"                       # a FRESH environment: nothing already installed stands in
. "$W/v5/bin/activate"
pip install ".[test]"
for sibling in openxdox doc_health; do                # a FRESH environment makes them absent; ASSERT it
  if python -c "import $sibling" 2>/dev/null; then echo "FAIL: $sibling is importable"; exit 1; fi
done
# the MODULE, not the console script, so this proof does not depend on
# 10.1's packaging line: the module is importable once group 2 lands, and
# that is what this falsifier uses.
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
R=$(mktemp -d)/plain-documents
cp -r tests/fixtures/plain-documents "$R"   # 5.0's fixture, as a FRESH repository
git -C "$R" init -q
git -C "$R" add -A
git -C "$R" commit -qm fixture
python -m opendox.cli generate --repo-root "$R" --repository fixture --output "$W/snap.json"
python3 - "$W/snap.json" <<'PY'
import json, re, sys
d = json.load(open(sys.argv[1]))
assert d["documents"], "snapshot is empty"
WORDS = ["brainstorm", "staged", "draft", "ratified", "standard", "superseded", "retired", "record",
         "openspec", "proposal.md", "tasks.md", "design.md", "added requirements", "modified requirements"]
pat = re.compile(r"\b(" + "|".join(re.escape(w) for w in WORDS) + r")\b")
def values(o):                                        # string VALUES only: keys are the product's own structure
    if isinstance(o, dict):
        for v in o.values(): yield from values(v)
    elif isinstance(o, list):
        for v in o: yield from values(v)
    elif isinstance(o, str):
        yield o
leaks = sorted({m.group(1) for v in values(d) for m in pat.finditer(v.lower())})
assert not leaks, f"openxFactory's vocabulary leaked into the neutral projection: {leaks}"
print("documents:", len(d["documents"]))
PY
```

**Exit 0.** Neither sibling imports, the generate verb writes the neutral
snapshot from the fixture as a fresh repository, and none of the fourteen
declared words is in any of its string values:

```
Successfully installed PyJWT-2.15.1 PyYAML-6.0.3 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 certifi-2026.7.22 cffi-2.1.1 click-8.5.0 cryptography-50.0.2 fastapi-0.142.2 h11-0.16.0 httpcore-1.0.9 httptools-0.8.0 httpx-0.28.1 idna-3.20 iniconfig-2.3.0 opendox-0.0.0 opentelemetry-api-1.45.0 packaging-26.3 pluggy-1.6.0 psycopg-3.3.6 psycopg-binary-3.3.6 psycopg-pool-3.3.3 pycparser-3.0 pydantic-2.13.5 pydantic-core-2.46.5 pygments-2.21.0 pytest-8.4.2 python-dotenv-1.2.4 starlette-1.7.0 typing-extensions-4.16.0 typing-inspection-0.4.4 uvicorn-0.54.0 uvloop-0.23.0 watchfiles-1.3.0 websockets-17.1
wrote <workdir>/tmp/F5.3/tmp.I2l5SZYx6r/snap.json
  repository=fixture kind=opendox-snapshot
  source_revision=a66a7eb85cd6c58766fa8027db461c2635ac9909
  generated_at=2026-10-02T22:30:56+00:00
  documents=8 clusters=2 possibles=1 staged_topics=1 changes=2 keywords=28
  validation: opendox-snapshot: 0 violations, by opendox.validator, over its packaged copy opendox-snapshot (sha256 f9e3e111af1d)
documents: 8
```

## 4. F7.1 (openXdox-code `6a3b93b9`)

As extracted (sha256 `821603ad1b33`), run unchanged. Batch I
(`5851950767`, R1Q27 (a)) changes no line of the block. It reads the second
named test as "every schema THIS INSTALL validates is on disk", and the test
at `6a3b93b9` is that reading (T061, openXdox-code#36):

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
python -m venv --clear "$W/v7x"                      # a FRESH environment: nothing already installed stands in
. "$W/v7x/bin/activate"
pip install ".[test]"
mkdir -p "$W/preshed/openxFactory/scripts" "$W/preshed/work"
printf 'raise SystemExit(0)\n' > "$W/preshed/openxFactory/scripts/validate-ideation-dashboard-contracts.py"
python3 - "$W/preshed" <<'PY'
import sys
from pathlib import Path
from openxdox import snapshot
planted = Path(sys.argv[1]).resolve()
found = snapshot.find_validator(planted / "work")     # the lookup starts INSIDE the planted tree
assert found is not None, "the consumer found no validator of its own"
assert planted not in Path(found).resolve().parents, f"it adopted the enclosing tree's validator: {found}"
PY
python -m pytest -q \
  "tests/test_snapshot.py::test_the_validator_is_the_installed_consumers_own" \
  "tests/test_validate_ideation_dashboard_contracts.py::test_every_schema_the_consumer_validates_is_on_disk"
```

**Exit 0.** The lookup, started inside the planted pre-shed tree, answers a
validator outside it, and both named tests pass. The second test's file is in
the declared exclusion (`openxfactory-contracts`), and pytest collects it
because it is named on the command line, as the banner's `collected` line
says:

```
Successfully installed PyYAML-6.0.3 attrs-26.1.0 iniconfig-2.3.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 opendox-0.0.0 openxdox-0.0.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-8.4.2 referencing-0.37.0 rfc3339-validator-0.1.4 rpds-py-2026.6.3 six-1.17.0 typing-extensions-4.16.0
..                                                                       [100%]
[the declared exclusion's banner, its three reasons and its `excluded` lines: as in § 2a, elided. Its one `collected` line, naming the file this run collects although the exclusion lists it, is:]
  collected tests/test_validate_ideation_dashboard_contracts.py: openxfactory-contracts
2 passed in 0.88s
```

## 5. F7.2 (openDox-code `047bb4fa`)

As extracted (sha256 `9150ca36af98`), run unchanged:

```sh
set -euo pipefail
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
python -m venv "$W/v7"
. "$W/v7/bin/activate"
pip install .   # PACKAGE DATA on disk (7.1)
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
OK=$(mktemp -d)/plain-documents
cp -r tests/fixtures/plain-documents "$OK"
git -C "$OK" init -q
git -C "$OK" add -A
git -C "$OK" commit -qm fixture
BAD=$(mktemp -d)/malformed
cp -r tests/fixtures/malformed "$BAD"
git -C "$BAD" init -q
git -C "$BAD" add -A
git -C "$BAD" commit -qm fixture
python -m opendox.cli generate --repo-root "$OK" --repository fixture --strict --output "$W/ok.json"
if python -m opendox.cli generate --repo-root "$BAD" --repository fixture --strict --output "$W/bad.json" 2>"$W/err"; then
  echo "FAIL: a malformed corpus validated"; exit 1
fi
RULE=$(cat tests/fixtures/malformed/EXPECTED_RULE)
test -n "$RULE"
grep -qF -- "$RULE" "$W/err"                          # refused for THE rule the fixture breaks
rc=0; grep -q "No such file or directory" "$W/err" || rc=$?
test "$rc" -eq 1                                      # ABSENT: not refused for a missing path
```

**Exit 0.** The good fixture validates under `--strict`. The malformed one
exits non-zero, its stderr carries the fixture's rule, and it has no `No such
file or directory`:

```
Successfully installed PyYAML-6.0.3 opendox-0.0.0
wrote <workdir>/tmp/F7.2/tmp.8FvbGiNShj/ok.json
  repository=fixture kind=opendox-snapshot
  source_revision=5ba8c0398960585773bfcd7c0efda327ebd9fdcb
  generated_at=2026-10-02T22:31:03+00:00
  documents=8 clusters=2 possibles=1 staged_topics=1 changes=2 keywords=28
  validation: opendox-snapshot: 0 violations, by opendox.validator, over its packaged copy opendox-snapshot (sha256 f9e3e111af1d)
wrote <workdir>/tmp/F7.2/tmp.8FvbGiNShj/bad.json
  repository=fixture kind=opendox-snapshot
  source_revision=cc82fd162b9049eb4da670b192c221bac901375f
  generated_at=2026-10-02T22:31:03+00:00
  documents=2 clusters=0 possibles=0 staged_topics=0 changes=0 keywords=5
```

The block keeps the malformed run's stderr in `$W/err` and does not print it.
A second run (sha256 `46915b32478c`) appends three lines after the
block's last line, so they run only if every check held:

```diff
25a26,31
> # --- T063 addition: the block above is F7.2 unchanged. Under set -e the lines below run only if
> # every check above held. They print what the block asserts on: the fixture's rule, and the
> # malformed run's stderr, which the block keeps in "$W/err".
> echo "=== EXPECTED_RULE: $RULE"
> echo "=== the malformed corpus's generate --strict stderr ($W/err):"
> cat "$W/err"
```

openDox's own validator (T058) rejected the snapshot for the one rule the
fixture breaks (T051), over its packaged copy of T053's schema (T057):

```
=== EXPECTED_RULE: title-and-summary-are-text
=== the malformed corpus's generate --strict stderr (<workdir>/tmp/F7.2-shown/tmp.kP5KueAenF/err):
  validation FAILED — the pinned validator REJECTED <workdir>/tmp/F7.2-shown/tmp.kP5KueAenF/bad.json. This is the SNAPSHOT, not the environment: the validator ran fine and found the data non-conformant.
    [title-and-summary-are-text] /documents/1/title: '' is shorter than 1
    1 violation(s) of the opendox-snapshot contract, by opendox.validator, over its packaged copy opendox-snapshot (sha256 f9e3e111af1d)
```

## 6. A standalone `generate-and-open` serving the fixture (openDox-code `047bb4fa`)

T063's last run, after the five falsifiers. #1144 has no block for it, so
this one follows T056's own test of the path
(`tests/test_standalone_generate_path.py::test_generate_and_open_starts_a_server_that_answers_with_no_sibling`):

- a plain `pip install .` into a fresh venv, with no `--local`, which arrives
  in phase 3 (T070);
- the four siblings asserted absent;
- 5.0's fixture copied as a fresh repository;
- the server started with `--no-open --port 0`, and its core routes read
  while it serves;
- then an interrupt, and the port checked closed.

`OPENDOX_STATE_DIR` is set to a short directory, and the run dir is
`$OPENDOX_STATE_DIR/run`. Nothing in openDox-code at `047bb4fa` reads
`OPENDOX_STATE_DIR` (`git grep` finds it nowhere), so the run dir is passed as
`--run-dir`. The script (sha256 `ef6d0496455e`):

```sh
# T063: a standalone `generate-and-open` serving 5.0's fixture (openDox-code checkout, plain install, no sibling).
set -euo pipefail
set -m                                                # job control, so the background server keeps SIGINT
W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
python -m venv --clear "$W/vgao"                     # a FRESH environment: nothing already installed stands in
. "$W/vgao/bin/activate"
pip install .                                         # a plain install, as T056 runs it (no --local before phase 3)
for sibling in openxdox ideation_dashboard doc_health corpus_adapter_openxfactory; do
  if python -c "import $sibling" 2>/dev/null; then echo "FAIL: $sibling is importable"; exit 1; fi
done
echo "=== no sibling imports: openxdox, ideation_dashboard, doc_health, corpus_adapter_openxfactory"
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
R=$(mktemp -d)/plain-documents
cp -r tests/fixtures/plain-documents "$R"             # 5.0's fixture, as a FRESH repository
git -C "$R" init -q
git -C "$R" add -A
git -C "$R" commit -qm fixture
: "${OPENDOX_STATE_DIR:?set OPENDOX_STATE_DIR to a short state directory}"
mkdir -p "$OPENDOX_STATE_DIR"
python -m opendox.cli generate-and-open --repo-root "$R" --repository fixture --no-open --port 0 \
  --run-dir "$OPENDOX_STATE_DIR/run" > "$W/out" 2> "$W/err" &
pid=$!
for i in $(seq 1 120); do                             # bounded: at most 60 s for the server to say where it is
  grep -qE '^http://[0-9.]+:[0-9]+/index\.html$' "$W/out" && grep -q 'serving until interrupted' "$W/out" && break
  kill -0 "$pid" 2>/dev/null || { echo "FAIL: the server exited before serving"; cat "$W/out" "$W/err"; exit 1; }
  sleep 0.5
done
URL=$(grep -oE '^http://[0-9.]+:[0-9]+' "$W/out" | head -1)
test -n "$URL"
echo "=== generate-and-open's own output, read while it serves:"; cat "$W/out"
echo "=== its stderr so far:"; cat "$W/err"
python3 - "$URL" "$OPENDOX_STATE_DIR/run/snapshot.json" "$R" <<'PY'
import json, sys, urllib.error, urllib.request
base, written, repo = sys.argv[1], sys.argv[2], sys.argv[3]
def get(path):
    try:
        with urllib.request.urlopen(base + path, timeout=10) as r:
            return r.status, r.headers.get("Content-Type"), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type"), e.read()
s, ct, b = get("/index.html")
assert s == 200 and "<html" in b.decode("utf-8", "replace").lower(), (s, ct)
print(f"GET /index.html -> {s} {ct}, {len(b)} bytes, an HTML page")
s, ct, b = get("/snapshot.json")
assert s == 200, s
served = json.loads(b)
assert served == json.load(open(written)), "the served snapshot is not the one this run wrote"
docs = served["documents"]
print(f"GET /snapshot.json -> {s} {ct}: kind {served['kind']!r}, {len(docs)} documents, equal to the run dir's snapshot.json")
for d in docs:
    print(f"    {d.get('path') or d.get('id')}: stage {d.get('stage')!r}")
s, ct, b = get("/capabilities")
assert s == 200, s
caps = json.loads(b)
print(f"GET /capabilities -> {s} {ct}: actions {json.dumps(caps.get('actions'), sort_keys=True)}; refresh binding {caps.get('refresh', {}).get('binding')!r}")
doc = "notes-toolshed-inventory.md"
s, ct, b = get(f"/source/{doc}")
assert s == 200 and b == open(f"{repo}/{doc}", "rb").read(), s
print(f"GET /source/{doc} -> {s}, byte-identical to the fixture's file")
s, ct, b = get("/source/.git/config")
assert s == 404, s
print(f"GET /source/.git/config -> {s} (refused)")
PY
kill -INT "$pid"
rc=0; wait "$pid" || rc=$?
echo "=== the server stopped on an interrupt with status $rc"
test "$rc" -eq 0
python3 - "$URL" <<'PY'
import socket, sys, urllib.parse
u = urllib.parse.urlparse(sys.argv[1])
with socket.socket() as s:
    s.settimeout(5)
    assert s.connect_ex((u.hostname, u.port)) != 0, "the port still accepts connections"
print(f"=== {u.hostname}:{u.port} is closed")
PY
```

**Exit 0.** The server writes the neutral snapshot (`opendox-snapshot`, eight
documents: three sources and one in each of the other five stations), validates it with
openDox's own validator (0 violations), and serves it. `/index.html`,
`/snapshot.json` (byte-equal, as JSON, to the run dir's file) and
`/capabilities` answer. A document's source is served byte for byte, and
`/source/.git/config` is refused. The interrupt stops it with status 0, and
the port is closed:

```
Successfully installed PyYAML-6.0.3 opendox-0.0.0
=== no sibling imports: openxdox, ideation_dashboard, doc_health, corpus_adapter_openxfactory
=== generate-and-open's own output, read while it serves:
wrote <workdir>/s/run/snapshot.json
  repository=fixture kind=opendox-snapshot
  source_revision=a1c47db602ccf6239403746cf01846ea2fbc6f7a
  generated_at=2026-10-02T22:35:49+00:00
  documents=8 clusters=2 possibles=1 staged_topics=1 changes=2 keywords=28
  validation: opendox-snapshot: 0 violations, by opendox.validator, over its packaged copy opendox-snapshot (sha256 f9e3e111af1d)
  serving http://127.0.0.1:43375/index.html
  snapshot http://127.0.0.1:43375/snapshot.json
http://127.0.0.1:43375/index.html
  serving until interrupted (Ctrl-C to stop)
=== its stderr so far:
GET /index.html -> 200 text/html, 7556 bytes, an HTML page
GET /snapshot.json -> 200 application/json; charset=utf-8: kind 'opendox-snapshot', 8 documents, equal to the run dir's snapshot.json
    candidate-toolshed-rebuild.md: stage 'candidate'
    completion-path-resurfacing.md: stage 'completion'
    grouping-compost-corner.md: stage 'grouping'
    notes-rain-barrel-leak.md: stage 'source'
    notes-rain-barrel-overflow.md: stage 'source'
    notes-toolshed-inventory.md: stage 'source'
    selection-spring-planting-plan.md: stage 'selection'
    submission-shed-door-repair.md: stage 'submission'
GET /capabilities -> 200 application/json; charset=utf-8: actions {"edit": true, "gate": true, "intent": false, "notebook": true, "refresh": true, "session": true}; refresh binding 'regenerate'
GET /source/notes-toolshed-inventory.md -> 200, byte-identical to the fixture's file
GET /source/.git/config -> 404 (refused)
=== the server stopped on an interrupt with status 0
=== 127.0.0.1:43375 is closed
```

`/capabilities` reads `gate: true` here, while no gate route is served
standalone. That is the over-claim T007's batch L records at 4.3 (`5920216845`,
item 1), which T084 fixes in phase 3. It is not one of phase 2's checks.

## 7. T065's interim F11.1

<!-- T063 PLACEHOLDER: T065's interim F11.1 output, quoted from `evidence/f11.1-phase2.txt` once T065's PR lands it. -->

**PENDING.** T065 runs F11.1 by T093's procedure, with
`PACKET_MERGE=94b6f7f1` and `ARC_TIP` at T064's landing `fcb45380`, and its own
PR records the output in `evidence/f11.1-phase2.txt`. This section quotes that
output, and links the file, once it lands.

## T092's phase-2 notes, carried in this PR

T092 puts one `edits[].note` in `docs/opendox-carve-manifest.yaml` for each
reach a phase closed. Each phase's notes were to ride in its openxFactory pin
PR (T047, T064, T094). On the holder's decision (b), recorded in T064's PR
(openxFactory#1215), phase 2's ride in this checkpoint PR instead, as phase 1's
rode in T049's. There are three notes on three rows (two added, one extended),
for the eight reaches phase 2 closed.

This PR carries no `Arc:` trailer, so F11.1's count of annotated notes never
includes these notes. The checks below run F11.1's content rule over them
directly.

**The reaches phase 2 closed.** F4.1's scan (extracted at `:527-549`, sha256
`2c1bbe9f49f2`), run over `src/opendox` at three openDox-code commits,
names 27 deferred reaches at `1e4a57fb` (4.3's measurement), 19 at
`2d116415` (phase 1's pin; the 19 into openXdox) and 11 at `047bb4fa` (phase 2's).
Along the first-parent history from `2d116415` to `047bb4fa`, the count drops
once, at T055's landing (openDox-code#59 → `fa140875`):

```
dc3765dd  19 reach(es)  T050, the plain-documents fixture, spread across the six stations (#53)
86647320  19 reach(es)  T051, the malformed fixture (title-and-summary-are-text) (#56)
fa8862cc  19 reach(es)  T052, declare the generator seam (5.4) and register openDox's own generator (plan 034) (#54)
a691e4e4  19 reach(es)  T054, openDox's small neutral projection (5.1-5.3) (plan 034) (#57)
8ec08e91  19 reach(es)  T057, openDox's own validator and its input set (7.1, 7.1a, 7.1b, 7.2) (plan 034) (#58)
fa140875  11 reach(es)  T055, serve and generate standalone (5.5, 4.3 part) (plan 034) (#59)
75bd8703  11 reach(es)  T055 follow-up: confine to the resolved entry, no second lookup (default_registry.resolve_source) (#70)
a23e4224  11 reach(es)  T056, the standalone generate path, end to end (5.1 part) (plan 034) (#66)
047bb4fa  11 reach(es)  T058, the post-render validator in the generate verbs (7.2 part) (plan 034) (#68)
```

The eight it closed are 4.3's reaches into openXdox. At `1e4a57fb`, where
#1144 names them, they are `branch_session.py:1568`, `:2105`, `:2151`,
`:2228` and `:3573`, `cli.py:610`, and `serve.py:629` and `:1993`. Each is among
the uses T055's own text lists. The 11 left are phase 3's (T084–T086):

```
Traceback (most recent call last):
  File "<stdin>", line 20, in <module>
AssertionError: 11 deferred reach(es) still name the consumer or the publisher:
  src/opendox/branch_session.py:1592: openxdox.register
  src/opendox/branch_session.py:2010: openxdox
  src/opendox/serve_project.py:271: openxdox.gate_console
  src/opendox/serve_project.py:272: openxdox.kickoff
  src/opendox/serve_workbench.py:1219: openxdox
  src/opendox/serve_workbench.py:1669: openxdox
  src/opendox/serve_workbench.py:2611: openxdox
  src/opendox/serve_workbench.py:351: openxdox
  src/opendox/serve_workbench.py:411: openxdox
  src/opendox/serve_workbench.py:412: openxdox
  src/opendox/serve_workbench.py:548: openxdox
exit 1
```

**Each reach is a declared carve line.** The manifest numbers its lines in
the carve blob (`carve_commit` `b075fd91`). The carve rewrote each of these
eight lines from an `ideation_dashboard` or relative import to `openxdox`, so
unlike phase 1's ten, none is byte-identical to its carve line. Each sits in a
one-line `replace` block of `difflib` over `carve_lines.text_records()` of the
two blobs, so the pairing is exact. The carve line is in the `lines` of one
`import rewrites` entry, as the mapping prints (after this PR's notes). The
script takes a directory holding an openxFactory clone (`oxf`) and an
openDox-code clone (`odc`):

```python
# usage: t092-reach-mapping-p2.py <W>
# Maps each reach phase 2 closed (4.3's reaches into openXdox, at openDox-code 1e4a57fb, as F4.1's scan
# names them) to its line in the carve blob (openxFactory carve_commit b075fd91, the manifest's numbering),
# through difflib over carve_lines.text_records() of the two blobs, and names the edits[] entry whose
# `lines` hold that carve line.
import difflib, pathlib, subprocess, sys, yaml
W = pathlib.Path(sys.argv[1]); CARVE = "b075fd91dc8fced8e1373825ba80220c33536bae"; AT = "1e4a57fb"
sys.path.insert(0, str(W / "oxf" / "scripts")); import carve_lines
REACHES = [("branch_session.py", 1568), ("branch_session.py", 2105), ("branch_session.py", 2151),
           ("branch_session.py", 2228), ("branch_session.py", 3573), ("cli.py", 610),
           ("serve.py", 629), ("serve.py", 1993)]
def blob(repo, rev, path):
    return subprocess.run(["git", "-C", str(W / repo), "show", f"{rev}:{path}"], check=True, capture_output=True).stdout
manifest = yaml.safe_load(open(W / "oxf" / "docs" / "opendox-carve-manifest.yaml"))
rows = {r["source_path"]: r for r in manifest["rows"]}
for f, n in REACHES:
    carve = carve_lines.text_records(blob("oxf", CARVE, f"scripts/ideation_dashboard/{f}"))
    arrived = carve_lines.text_records(blob("odc", AT, f"src/opendox/{f}"))
    sm = difflib.SequenceMatcher(None, carve, arrived, autojunk=False)
    hit = [(tag, i1, i2, j1, j2) for tag, i1, i2, j1, j2 in sm.get_opcodes() if j1 <= n - 1 < j2]
    tag, i1, i2, j1, j2 = hit[0]; k = n - 1 - j1
    if tag == "replace" and (i2 - i1) != (j2 - j1):
        print(f"{f}:{n} @{AT} -> UNEVEN {tag} carve[{i1}:{i2}]/arrived[{j1}:{j2}]; lines below are by offset only")
    c = i1 + k + 1
    print(f"{f}:{n} @{AT} -> carve line {c} ({tag} carve[{i1}:{i2}]/arrived[{j1}:{j2}] offset {k})")
    print(f"    arrived: {arrived[n - 1].rstrip(chr(10))!r}")
    print(f"    carve  : {carve[c - 1].rstrip(chr(10))!r}")
    row = rows[f"scripts/ideation_dashboard/{f}"]
    ent = [(i, e) for i, e in enumerate(row.get("edits") or []) if c in e.get("lines", [])]
    for i, e in ent:
        print(f"    declared by: {row['source_path']} edits[{i}] ({e['class']}), note present: {'note' in e}")
    if len(ent) != 1:
        print(f"    !! carve line {c} is in {len(ent)} edits[] entries")
```

```
branch_session.py:1568 @1e4a57fb -> carve line 1555 (replace carve[1554:1555]/arrived[1567:1568] offset 0)
    arrived: '    from openxdox import generator'
    carve  : '    from . import generator'
    declared by: scripts/ideation_dashboard/branch_session.py edits[0] (import rewrites), note present: True
branch_session.py:2105 @1e4a57fb -> carve line 2092 (replace carve[2091:2092]/arrived[2104:2105] offset 0)
    arrived: '    from openxdox.snapshot_registry import SnapshotEntry   # lazy: keeps the import graph flat'
    carve  : '    from .snapshot_registry import SnapshotEntry   # lazy: keeps the import graph flat'
    declared by: scripts/ideation_dashboard/branch_session.py edits[0] (import rewrites), note present: True
branch_session.py:2151 @1e4a57fb -> carve line 2138 (replace carve[2137:2138]/arrived[2150:2151] offset 0)
    arrived: '    from openxdox.snapshot_registry import entry_from_snapshot_file'
    carve  : '    from .snapshot_registry import entry_from_snapshot_file'
    declared by: scripts/ideation_dashboard/branch_session.py edits[0] (import rewrites), note present: True
branch_session.py:2228 @1e4a57fb -> carve line 2215 (replace carve[2214:2215]/arrived[2227:2228] offset 0)
    arrived: '    from openxdox.snapshot_registry import BINDING_REGENERATE, SnapshotSource'
    carve  : '    from .snapshot_registry import BINDING_REGENERATE, SnapshotSource'
    declared by: scripts/ideation_dashboard/branch_session.py edits[0] (import rewrites), note present: True
branch_session.py:3573 @1e4a57fb -> carve line 3560 (replace carve[3559:3560]/arrived[3572:3573] offset 0)
    arrived: '    from openxdox.snapshot_registry import ('
    carve  : '    from .snapshot_registry import ('
    declared by: scripts/ideation_dashboard/branch_session.py edits[0] (import rewrites), note present: True
cli.py:610 @1e4a57fb -> carve line 577 (replace carve[576:577]/arrived[609:610] offset 0)
    arrived: '    from openxdox.snapshot_registry import SnapshotRegistry'
    carve  : '    from ideation_dashboard.snapshot_registry import SnapshotRegistry'
    declared by: scripts/ideation_dashboard/cli.py edits[0] (import rewrites), note present: True
serve.py:629 @1e4a57fb -> carve line 534 (replace carve[533:534]/arrived[628:629] offset 0)
    arrived: '    from openxdox.corpus_root import corpus_scan_defect'
    carve  : '    from ideation_dashboard.corpus_root import corpus_scan_defect'
    declared by: scripts/ideation_dashboard/serve.py edits[0] (import rewrites), note present: True
serve.py:1993 @1e4a57fb -> carve line 1639 (replace carve[1638:1639]/arrived[1992:1993] offset 0)
    arrived: '    from openxdox.corpus_root import corpus_root_refusal, corpus_scan_defect'
    carve  : '    from ideation_dashboard.corpus_root import corpus_root_refusal, corpus_scan_defect'
    declared by: scripts/ideation_dashboard/serve.py edits[0] (import rewrites), note present: True
```

**Each note is on the entry that declares its line**, and records the close:

```python
# usage: t092-note-check-p2.py <manifest.yaml>
# Each carve line phase 2 closed is in the `lines` of exactly one edits[] entry of its row,
# and that entry's note records the close (names phase 2 and the carve line).
import sys, yaml
CLOSED = {"branch_session.py": [1555, 2092, 2138, 2215, 3560], "cli.py": [577], "serve.py": [534, 1639]}
rows = {r["source_path"]: r for r in yaml.safe_load(open(sys.argv[1]))["rows"]}
ok = True
for f, lines in CLOSED.items():
    row = rows[f"scripts/ideation_dashboard/{f}"]
    for c in lines:
        ent = [(i, e) for i, e in enumerate(row.get("edits") or []) if c in e.get("lines", [])]
        closed = len(ent) == 1 and "CLOSED IN PHASE 2" in (ent[0][1].get("note") or "") and str(c) in ent[0][1]["note"].split("CLOSED IN PHASE 2", 1)[1]
        ok &= closed
        print(f"  {f} carve line {c}: " + ", ".join(f"edits[{i}] ({e['class']})" for i, e in ent) + f", note closed: {closed}")
print("every reach's carve line is in exactly one edits[] entry, and its note records the close" if ok else "FAIL")
sys.exit(0 if ok else 1)
```

```
  branch_session.py carve line 1555: edits[0] (import rewrites), note closed: True
  branch_session.py carve line 2092: edits[0] (import rewrites), note closed: True
  branch_session.py carve line 2138: edits[0] (import rewrites), note closed: True
  branch_session.py carve line 2215: edits[0] (import rewrites), note closed: True
  branch_session.py carve line 3560: edits[0] (import rewrites), note closed: True
  cli.py carve line 577: edits[0] (import rewrites), note closed: True
  serve.py carve line 534: edits[0] (import rewrites), note closed: True
  serve.py carve line 1639: edits[0] (import rewrites), note closed: True
every reach's carve line is in exactly one edits[] entry, and its note records the close
```

**F11.1's content rule holds.** The rule is the guard's `notes()` and
`without_notes()`, copied from #1144's `tasks.md`, and applied to `main`'s
manifest and this PR's. The script is T049's (`checkpoint-phase1.md`), byte
for byte. With every note removed, the two are equal. Two notes are new, and
the third begins with the note it extends (phase 1's, on `serve.py`'s first
entry):

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
  added: scripts/ideation_dashboard/branch_session.py edits[0]
  added: scripts/ideation_dashboard/cli.py edits[0]
  extended: scripts/ideation_dashboard/serve.py edits[0]
F11.1's manifest content rule holds: 3 note(s) annotated, nothing else in the manifest moved
```

`scripts/validate-carve-manifest.py` accepts the manifest:

```
OK docs/opendox-carve-manifest.yaml: phase post-shed, 456 row(s) at opensoft/openxFactory@b075fd91dc8f (opendox-carve-0), verified at 9093fdee12f1 — 142 moved_verbatim, 176 moved_with_declared_edit, 138 not_moved; 318 digest(s) recomputed; 456 file(s) in the declared surface with none undeclared; 319 shed row(s) absent at source as declared; 4 row(s) RE-DESTINED by ruling (RULED Q6); 2 row(s) RETIRED by ruling (RULED 5656343213)
```
