# Re-measure of research R1–R15 (T005)

Status: record

**Feature**: [`034-opendox-standalone-operation`](../spec.md) · **Task**: T005
([`tasks.md`](../tasks.md)) · **Taken**: 2026-09-25, 13:34–14:10Z ·
**Lane**: `openxfactory-4`

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`). It re-runs every measurement in [`research.md`](../research.md) at
the `main` of each repository on 2026-09-25 and records how far each figure
moved from 2026-09-24. research.md stays as the record of 2026-09-24. Where a
figure moved, the last section names the slice it re-plans. That re-plan is in
the same PR as this note, and it comes before T006's analyze.

## The trees

| repository | research (2026-09-24) | T005 (2026-09-25) | moved by |
|---|---|---|---|
| `opensoft/openDox-code` | `1e4a57fb` | `1e4a57fb` | — |
| `opensoft/openXdox-code` | `626f2c8d` | `e28930bf` | C3's PR 2, openXdox-code#28 |
| `opensoft/openDox-spec` | `8fe8c4c7` | `8fe8c4c7` | — |
| `opensoft/openXdox-spec` | `f088b097` | `f088b097` | — |
| `opensoft/openDox` | `36ded1cd` | `36ded1cd` | — |
| `opensoft/openXdox` | `2f3f857d` | `069fe471` | C3's root bump, openXdox#19 |
| `opensoft/openxFactory` | `dd2466ad` | `c415c3d1` | #1151–#1157 and #1162 |

The workspace is research R0's, with each repository checked out at the T005
column in place of the research column. The `od` and `ox` venvs, and the Group 2
measurement shim, are made by R0's commands unchanged. In the `ox` venv, openDox
still arrives at openXdox-code's pin, `5c137a90`.

One more venv, `oxr`, simulates T040's declaration of `rfc3339-validator`, which
R11 found missing. It is used only where this note says so:

```sh
python3 -m venv "$W/oxr"
"$W/oxr/bin/pip" install -q -e "$W/openXdox-code[test]" rfc3339-validator   # 0.1.4 was installed
```

The tools are the persisted ones (plan.md § "Persisted tools"), read from the
lane's workspace repository. Each one is byte-identical to its heredoc in
research.md § Appendix, and so is the shim:

| tool | sha256 |
|---|---|
| `ci_coverage.py` | `20f633d8a7240142a4f27367ebefa942eeed91007ad752d97bdf3946b95160e2` |
| `scan_deferred_reaches.py` | `fe11620319b02c23dd9a014bc581e1f4867f013f3c26890d43b12dccce5530a0` |
| `census_consumer_reach.py` | `7f36b848a3a0a93e3c7af8481d7248582254c1715247c11e4fe626cd4826c804` |
| `box_census.py` | `516f11c3b4c958f1b05db4a0919a1e48368dc9d49ef0bd6ed8d637411ca0f2b7` |

T005 adds one tool, `classify_whole_suite.py`, which is given in full in the
[Appendix](#appendix--classify_whole_suitepy) and persisted beside the others.

## Drift, figure by figure

| | 2026-09-24 (research) | 2026-09-25 (T005) | moved |
|---|---|---|---|
| **R1** | `imported 53 of 56`; `opendox.cli`, `opendox.notebook_action` and `opendox.serve` fail on `ideation_dashboard`; the four siblings are absent | the same | no |
| **R2** | `11 skipped, 1305 errors`; 1,239 lines name `ideation_dashboard` | the same | no |
| **R3** | `20 failed, 1217 passed, 13 skipped, 66 errors`; 86 red in nine files | the same, with each file's count unchanged (28, 25, 13, 12, 3, 2, 1, 1, 1) | no |
| **R4** | 63 modules (53 + 10); `validate` names 37; `runtime` runs `tests_runtime/` whole; 22 run by nothing; `--noconftest` on 18 lines (3 code, 15 comments); `collect_ignore` lists 7 | the same | no |
| **R5** | 27 deferred reaches; the ratchet is `(0, 7)`, `(0, 1)`, `(0, 2)`, `(0, 2)`, `(0, 7)` | the same 27, at the same lines and inside the same functions; the ratchet at `e28930bf` is unchanged | no |
| **R6** | 65 sites | 65 sites, split the same way | no |
| **R7** | `REFUSED: ConsumerReachUnavailable 'openxdox.snapshot_registry'…` at `serve.py:1647` | the same | no |
| **R8** | five verbs; `main(["--help"])` exits 0; the golden holds 31 sections, 11 + 20 | the same, with the golden read at `c415c3d1` | no |
| **R9** | one line: `src/opendox/conformance_corpus.py 35 .runtime.local_git_adapter` | the same | no |
| **R10** | 85 test files; `validate` names 16; 8 `--noconftest` lines; floors `564/558/6`; 57 collection errors (26 `doc_health`, 28 `ideation_dashboard`, 3 `test_gate_routes`); `DOC_HEALTH_SURFACE` declares 8 modules | **87 test files**: openXdox-code#28 added `test_snapshot_validator_home.py` and `test_validator_schema_home.py`, and `validate` runs neither. Everything else is the same | **yes** |
| **R11** | 22 protected suites; plain, 12 fail on `ideation_dashboard` and 10 on `doc_health`; with the shim, 19 fail on `doc_health`, `test_gate_loop_views` passes 74, `test_snapshot` fails 3 and passes 14, `test_snapshot_validation_launch` fails 9 | **23 protected suites**: 5.4a's glob `tests/test_snapshot*.py` now also selects `test_snapshot_validator_home.py`. Plain, 13 fail on `ideation_dashboard` (the new suite is the thirteenth) and 10 on `doc_health`. With the shim, the same 19 fail on `doc_health`, `test_gate_loop_views` passes 74, **`test_snapshot` fails 2 and passes 15**, `test_snapshot_validation_launch` fails 9, and `test_snapshot_validator_home` passes 12. The `getsource` probe is unchanged | **yes** |
| **R12** | 456 rows: 318 with destination fields and 138 with `reason` and `evidence`; the table of fifteen openDox-code files | the same counts, and every row in R12's table is unchanged. The manifest moved once, in #1153 (C3's PR 1): openXdox-code's `snapshot.py` row went from `moved_verbatim` to `moved_with_declared_edit`, with two `edits[]` entries | yes, outside R12's table |
| **R13** | openxFactory's `openXdox` pin `2f3f857d`; the openXdox root's `code` `626f2c8d` | **`069fe471`** and **`e28930bf`**, as C3 planned. The rest is the same: `dc7aa08f`, `d816cf06` (openDox-code's `main` is 4 ahead of it), `5c137a90` (11 behind, and an ancestor of `d816cf06`), and each ruleset requires `validate` alone | **yes** |
| **R14** | the snapshot contract's `required` list and its four enums | the same | no |
| **R15** | the seven tabs, the chat rail's one entry point, the catalog route's validators, and the rail's copy | the same | no |

The commands are research's. Two readings go beyond them: the `oxr` runs,
which are in the next two sections, and R10's counts by cause, which come from
the plain run's `ERROR collecting` sections.

## `tests/test_snapshot.py` after C3

T005 was asked whether the three failures research recorded at `626f2c8d`
cleared once C3's PR 2 landed. **One cleared, and two did not.**

`test_find_validator_locates_pinned_checkout` now passes, because C3 moved the
validator lookup into the product's own tree. The other two cases,
`test_minimal_snapshot_validates_against_pinned_validator` and
`test_referentially_broken_snapshot_is_rejected`, still fail. Each was run with
the shim, from `cd "$W/openXdox-code"`:

| venv | `CONTRACTS_DIR` | result | the two cases fail on |
|---|---|---|---|
| `ox` | unset | `2 failed, 15 passed` | the `date-time` format checkers: *"install rfc3339-validator"* |
| `ox` | `"$W/openXdox-spec/contracts"` | `2 failed, 15 passed` | the same |
| `oxr` | unset | `2 failed, 15 passed` | *"`…/openXdox-code/contracts/schemas` carries none of the family's 10 schemas (this tree carries no contracts/ and CONTRACTS_DIR is not set; export it as the spec leg's contracts directory)"* |
| `oxr` | `"$W/openXdox-spec/contracts"` | **`17 passed`** | — |

    PYTHONPATH="$W/shim" "$W/oxr/bin/python" -m pytest -q tests/test_snapshot.py
    CONTRACTS_DIR="$W/openXdox-spec/contracts" PYTHONPATH="$W/shim" "$W/oxr/bin/python" -m pytest -q tests/test_snapshot.py

So the lookup is fixed, but the schemas are not. C3's validator reaches its
schemas through `CONTRACTS_DIR`, which names the spec leg. openXdox-code's own
checkout, the one T043's required check runs, carries no `contracts/` and has
no spec leg beside it. That is 7.3's other half: *"openXdox's validator and its
three schemas … are located through the INSTALLED openXdox distribution"*.
T040's `rfc3339-validator` is needed as well, but it is not enough.

The contingency that T043 and T061 wrote down for this case therefore applies.
T061 moves into phase 1, between T040 and T043.

## openXdox-code's whole suite

T005 runs openXdox-code's whole suite, not only research's protected suites. A
plain `python -m pytest -q` stops at collection (R10), so each run below goes
on past collection errors:

    cd "$W/openXdox-code"
    "$W/ox/bin/python" -m pytest -q --continue-on-collection-errors
    PYTHONPATH="$W/shim" "$W/ox/bin/python" -m pytest -q --continue-on-collection-errors
    PYTHONPATH="$W/shim" "$W/oxr/bin/python" -m pytest -q --continue-on-collection-errors --junitxml="$W/whole.xml"
    python3 "$W/tools/classify_whole_suite.py" "$W/whole.xml"

| run | result |
|---|---|
| plain (`ox`) | `5 skipped, 1126 errors` |
| Group 2 simulated (`ox` with the shim) | `187 failed, 934 passed, 11 skipped, 126 errors` |
| Group 2 simulated, with T040's `rfc3339-validator` (`oxr` with the shim) | `166 failed, 967 passed, 10 skipped, 126 errors` |

The last run has 292 red results: 166 failures, 71 errors at setup, and 55
modules that fail at collection. The classifier puts each one in a class by its
own message, and every one of them lands in a class:

| class | cause | red | files | where it goes |
|---|---|---|---|---|
| A | `doc_health` | 53 | 51: 50 fail at collection, and `test_doxbench_packet.py` has 3 cases | T041's declared exclusion (R1Q6 (d)) |
| B | `test_gate_routes`, an openxFactory-only helper module | 3 | `test_create_project.py`, `test_edit_project.py`, `test_register_edit_lane.py` | T040, as planned |
| C | `test_doxbench_routes`, an openxFactory-only helper module | 3 | `test_doxbench_knowledge_service.py`, `test_doxbench_thread_wiring.py` (both at collection), `test_doxbench_blank_reason.py` (1) | T040, re-planned |
| D | `test_doxbench_model`, an openxFactory-only helper module | 2 | `test_doxbench_bridge.py` | T040, re-planned |
| E | the bridge's stand-in child, `tests/fixtures/fake_omp_child.py`, which exists only in openDox-code | 32 | `test_doxbench_bridge.py` (`BridgeUnavailable`, and one `ThreadMirrorFailed`) | T040, re-planned |
| F | `tests/fixtures/base-repo`, an openxFactory fixture | 13 | `test_snapshot_validation_launch.py` (9), `test_register.py` (4) | T040, as planned; `test_register.py` is new to the list |
| G | pre-carve source paths, `scripts/ideation_dashboard/<module>.py`, for modules that now live in the `opendox` package | 22 | `test_doxbench_packet.py` (13), `test_scope_column_split.py` (4), `test_doxbench_blank_reason.py` (3), `test_doxbench_bridge.py` (2) | T040, re-planned |
| H | openxFactory's status-exemption rail, reached through openDox's `doxbench_packet.py:177` (research R5) | 87 | `test_doxbench_packet.py` (54), `test_doxbench_turns.py` (32), `test_doxbench_abstract_envelope.py` (1) | **R1Q24** (new) |
| I | the contract family: its validator, schemas and examples, read at `ROOT = Path(__file__).resolve().parents[2]`, which is outside the checkout | 74 | `test_validate_ideation_dashboard_contracts.py` (32), `test_wheel_action_contracts.py` (18), `test_project_schema_election.py` (13), `test_project_action_contracts.py` (11) | **R1Q24** (new) |
| J | the validator's schemas: no `contracts/` in the tree, and no `CONTRACTS_DIR` | 2 | `test_snapshot.py` | T061, now in phase 1 |
| K | the shim itself: `test_dependency_direction.py` asserts that `ideation_dashboard` is not in `sys.modules`, and the shim put it there | 1 | `test_dependency_direction.py` | none, since the shim is never installed |

Without `rfc3339-validator` (the `ox` venv), class J is absent and a class M
takes its place: 23 red results that ask for the package, 21 in
`test_doxbench_blank_reason.py` and `test_snapshot.py`'s 2. Installing it
clears the 21, and `test_snapshot.py`'s 2 then fail as class J. The rest of
the table is the same, and the run's 313 red results are 292 − 2 + 23.

The 50 files that fail at collection on `doc_health` are these:
`test_authoring_agent`, `test_branch_session`, `test_canvas`,
`test_completeness`, `test_create_document_cli`, `test_doxbench_abstract_route`,
`test_doxbench_mutation_boundary`, `test_doxbench_request_handling`,
`test_doxbench_save`, `test_doxbench_scope`, `test_doxbench_share`,
`test_doxbench_threads`, `test_doxbench_transport`, `test_doxchat_model_intake`,
`test_edit_action`, `test_explorer_viewer`, `test_gate_console`,
`test_gate_failure_diagnostics`, `test_gateway_provenance`,
`test_generated_at_anchor`, `test_generator`, `test_grouping`,
`test_header_value_readers`, `test_hosted_actor`, `test_kickoff`,
`test_notebook_action`, `test_project_aggregates`, `test_readiness_gate`,
`test_renderer`, `test_repo_root_guard`, `test_repo_selector`,
`test_round_trip`, `test_session_commits`, `test_session_confinement`,
`test_session_document_ownership`, `test_session_gates`,
`test_session_lifecycle`, `test_session_notebook`, `test_session_records`,
`test_session_runbook`, `test_session_snapshot`, `test_session_transaction`,
`test_session_verbs`, `test_snapshot_determinism`, `test_snapshot_registry`,
`test_source_dot_directories`, `test_staging_workbench`, `test_trust_gaps`,
`test_wheel_model` and `test_wheel_verbs_cli`. Under R1Q6 (d), each of them goes
into T041's declared exclusion.

**Classes C, D, E and G are carve residue, of the same kind as B and F**, which
T040 already clears. None of those files is a protected suite, so none of them
needs R1Q7 (a)'s allow-list. **Classes H and I are not residue.** They reach
openxFactory, but not through `doc_health`, so R1Q6 (d)'s exclusion cannot hold
them. They are R1Q24.

### An experiment, and what it does not settle

In a scratch copy of the checkout, and not as a plan, classes C–G were cleared
by hand:

- the two helper modules were copied in from openxFactory;
- `fake_omp_child.py` was copied in from openDox-code;
- `base-repo` was copied in from openxFactory;
- the source paths were respelled to the installed `opendox` package.

Then the ten affected files were run with the shim, in the `oxr` venv.
`test_register.py` passed, and `test_doxbench_bridge.py` went from 36 red to 3.
The next layer that showed up is this:

- `test_snapshot_validation_launch.py` now fails 9 cases on
  `ProfileNotRegistered`. Nothing registers openDox's default profile until
  T016, so the result changes at the phase-1 pin.
- `test_scope_column_split.py` fails 3 cases. Its import parser knows relative
  imports and the pre-carve package name, so it cannot see an import like
  `doxbench_packet.py:78`'s `from opendox.doxbench_scope_types import …`.
- `test_doxbench_bridge.py` fails 3. Two fail on `carved_reach`, another
  openxFactory-only helper, which the copied `test_doxbench_model` imports. The
  third reads a source path that is spelled another way.
- `test_doxbench_blank_reason.py` reads openxFactory's `contracts/manifest.yaml`,
  and a `dashboard_web_root` that only openxFactory's conftest defines.
- The copied `test_doxbench_routes` helper imports `dashboard_web_root` from
  its conftest, and only openxFactory's conftest defines it. So its two
  importers still fail at collection. Like the copied `test_doxbench_model`, it
  shows that a helper of their own has to carry only the names they use.

So some of the residue can only be measured at the pin T040 moves to. T043
re-runs the whole suite there before it pins the floors, and the re-plan says
so.

## What moved, and what it re-plans

1. **`test_snapshot.py` is still red**, so the contingency applies. T061 moves
   into phase 1, after T040 and T019 and before T043, and its
   `After: T049, T009` is dropped. Dropping T009 would also drop T061's
   implicit wait on R1Q12. Under (b), R1Q12 re-homes two of the three schemas
   that T061 packages, so T061 now names R1Q12 on its own `Blocked by:` line,
   next to R1Q14. 7.3 and F7.1 now close in phase 1.
2. **5.4a's glob now selects seven suites.** C3's
   `test_a_start_outside_the_product_is_refused_not_walked` lives in
   `test_snapshot_validator_home.py`, which is one of the seven. Revising it, as
   R1Q14 (a) would, is therefore a second edit that F5.2 refuses, beside the new
   test in `test_snapshot.py`. R1Q14's text now says so. R1Q23's four
   `doc_health` suites are unchanged, and the seventh suite passes.
3. **The whole suite has six classes that no task named**, besides K, which
   is the shim's own. C, D, E and G widen T040. H and I become **R1Q24**. T043 now starts by re-running the
   whole suite at T040's pin, and it names the class of every red file it
   finds.
4. **The round.** T061 and T043 wait on questions that are still open, so a
   new holder task, **T019**, applies their answers. It encodes R1Q14, R1Q24
   and the part of R1Q12 that T061 needs. It then re-plans phase 1's
   openXdox-code tail and re-runs analyze before T061 or T043 starts. That is
   the step T009 and T069 take for their phases.

**Nothing moved for G1.** openDox-code is unchanged at `1e4a57fb`, so P1-A,
P1-B, P1-C and P1-E, and every other openDox-code slice, are planned on
figures that still hold. The openDox root is unchanged too. The re-plan touches
only the openXdox-code slices, which are G5 (P1-I and P1-J, and the new P1-M,
which is T061), and phase 1's close, which T049 reaches only through them.

## Appendix — `classify_whole_suite.py`

```sh
cat > "$W/tools/classify_whole_suite.py" <<'PY'
"""T005: every red result of an openXdox-code whole-suite JUnit report, by cause.
usage: python3 classify_whole_suite.py <junit.xml>   (from pytest --junitxml)"""
import collections, re, sys, xml.etree.ElementTree as ET
CLASSES = {
    "A": "doc_health (T041's declared exclusion)",
    "B": "test_gate_routes, an openxFactory-only helper module (T040)",
    "C": "test_doxbench_routes, an openxFactory-only helper module",
    "D": "test_doxbench_model, an openxFactory-only helper module",
    "E": "the bridge's stand-in child, tests/fixtures/fake_omp_child.py (openDox-code only)",
    "F": "tests/fixtures/base-repo, an openxFactory fixture (T040)",
    "G": "pre-carve source paths, scripts/ideation_dashboard/<module>.py",
    "H": "openxFactory's status-exemption rail, through openDox's doxbench_packet.py:177",
    "I": "the contract family's validator, schemas and examples, read outside the checkout",
    "J": "the validator's schemas: no contracts/ in the tree and no CONTRACTS_DIR (7.3)",
    "K": "the measurement shim itself (ideation_dashboard in sys.modules)",
    "L": "ideation_dashboard, an import-time reach (Group 2)",
    "M": "rfc3339-validator, which the test extra does not declare (T040)",
}
MODULES = {"doc_health": "A", "test_gate_routes": "B", "test_doxbench_routes": "C",
           "test_doxbench_model": "D", "ideation_dashboard.doxbench_status_exemption": "H",
           "ideation_dashboard": "L"}
def cause(el):
    txt = (el.get("message") or "") + "\n" + (el.text or "")
    mods = re.findall(r"No module named '([^']+)'", txt)
    if mods:
        return MODULES.get(mods[-1], "?")
    if "rfc3339-validator" in txt:
        return "M"
    if "CONTRACTS_DIR is not set" in txt:
        return "J"
    if "base-repo" in txt or re.search(r"'pos-|'cl-avatar'|'fixture-cor", txt):
        return "F"
    path = re.search(r"(?:No such file or directory: |can't open file )'([^']+)'", txt)
    if path:
        return "G" if "/scripts/ideation_dashboard/" in path.group(1) else "I"
    if "BridgeUnavailable" in txt or "ThreadMirrorFailed" in txt:
        return "E"
    if "'ideation_dashboard' not in" in txt:
        return "K"
    return "?"
red = collections.defaultdict(collections.Counter)
for tc in ET.parse(sys.argv[1]).getroot().iter("testcase"):
    cls = tc.get("classname") or ""
    f = (tc.get("name").replace(".", "/") + ".py") if not cls else "/".join(cls.split(".")[:2]) + ".py"
    for tag in ("failure", "error"):
        el = tc.find(tag)
        if el is not None:
            red[cause(el)][f] += 1
total = 0
for c in sorted(red):
    n = sum(red[c].values()); total += n
    print(f"{c} {n:4d} results in {len(red[c]):2d} files: {CLASSES.get(c, 'UNCLASSIFIED')}")
    print("       " + ", ".join(f"{p.split('/')[-1][:-3]} {k}" for p, k in sorted(red[c].items())))
print("red results:", total)
PY
```

The class rules read each result's own message, so a class is only as exact as
that message. Class F also matches `test_register.py`'s four cases, whose
messages name the fixture's content (`pos-…`, `cl-avatar`, `fixture-core`) and
not the fixture itself. The experiment above confirms them: all four passed
once `base-repo` was present.
