# Proposal Reality Check: split-opendox-two-layer-product — the § 4 boxes, and the § 5 shed's own prerequisite

Status: record
Kind: verification record
Decision date: 2026-09-10
Lane: openxfactory-4-opendox-extraction (formerly openxfactory-opendox)
Author: this lane, § 5-remainder session, after a measurement pass over the six
§ 4 boxes and a two-stage probe of the § 5.2 shed, taken against
`opensoft/openxFactory` `main` at `ea34f22a743ea797924ca1f1537db51db48a4a55`
and against the destination repositories' own `main` at the same hour

**This record decides nothing.** It records what was MEASURED when the § 5
remainder was started on Brett Heap's word *"then start the § 5 remainder when
the OQ-L pin lands"* (2026-09-10), and it exists because two of that act's
premises did not survive measurement. Every number below was re-derived by
command at the revisions named; none is carried forward from an issue thread.
Where this record and an earlier prose reading disagree, the command output is
the finding and the prose is the thing corrected.

---

## 1. The § 4 boxes — SIX MEASURED, SIX LEFT OPEN

The standard is tick PR **#897 → `021c3d3607a626730ae8d2027ca68c58ed14a3b6`**'s:
a box ticks only where **its own text is FULLY met** by cited, landed evidence
verified live, and a partly-met box stays open **with the failing clause
named**. Applied to § 4 against the four landed acts —

| act | merge commit | landed |
| --- | --- | --- |
| carve leg 3, `opensoft/openXdox-code` #5 | `59600412787de4bdad11678b49e13a01decfaf5d` | 2026-09-10T17:33:41Z |
| carve leg 4, `opensoft/openXdox-spec` #5 | `03eacc61b733272d836f7e859eba4ae345e0f73b` | 2026-09-10T18:10:13Z |
| openDox root pin, `opensoft/openDox` #4 | `49a99df2561bf70e49337c999d79b36836718349` | 2026-09-10T13:30:22Z |
| openXdox root pin, `opensoft/openXdox` #4 | `db58fffa58d49d92f58db40bd7e63cad3205052f` | 2026-09-10T18:45:40Z |

— **no § 4 box is fully met, and none is ticked.**

### 4.1 — LEFT OPEN. The carve clause is met; the `doc_health` clause is not.

**Met.** All thirteen modules § D3's openXdox column names are row-placed and
physically present at `opensoft/openXdox-code` `main`: `corpus_root`,
`generator`, `snapshot`, `snapshot_registry`, `register`, `completeness`,
`round_trip`, `gate_console`, `gate_routes`, `kickoff`, `record_binding`,
`register_edit_lane`, `doxbench_scope` — 11,823 lines summed, against the box's
"~10.9K". The arrival verifier reproduces live:

```
OK phase B — 92 row(s) arrived, 9 digest(s) verified, 81 declared-edit row(s)
within their lines, 4 unapplied; 6 of 6 declared replica(s) verified;
97 file(s) under scripts, src/openxdox, tests with none undeclared
```

**Not met.** The box's second clause — *"The 23 outbound `doc_health` imports
become the adapter's IMPLEMENTATION SURFACE here, where importing doc-health is
lawful"* — is not satisfied by arrival alone. The import STATEMENTS travelled
byte-identically (25 statements across 15 files at the leg, the same 25/15 the
source rows carry at `carve_commit`), but `doc_health` is **unreachable at the
destination**: it is not vendored in the leg's tree, not declared in its
dependency set (`runtime: ['opendox @ git+…@8e9ffa62', 'PyYAML>=6.0']`), and not
a package on PyPI. With the leg's full declared dependency set installed:

```
importable: 5/17   fail on doc_health: 12   fail on something else: 0
doc_health failures: cli_gate, completeness, corpus_root, gate_console,
  gate_routes, generator, kickoff, openxdox_surface, register_edit_lane,
  round_trip, serve_projection, snapshot_registry
```

The leg's own `pyproject.toml` concedes the gap in its own words — *"`doc_health`
is openxFactory's own corpus machinery … a BUILD-arc cross-column reach, not a
package on PyPI, and not this PR's to resolve"* — and its `validate` workflow
runs only `pytest -q tests/test_leg_shape.py --noconftest` under RULED Q-L8 (b′),
so nothing at the leg exercises them. A surface on which twelve of seventeen
modules raise `ModuleNotFoundError` is not yet an implementation surface.

**A second, independent reason the clause is not closed.** `design.md`:243 says
what the carve must achieve here: *"What must not survive is the direction, not
the calls."* The direction survives. The openDox commit this family pins carries
**34 back-imports into `openxdox` across six modules** — `branch_session.py`,
`cli.py`, `serve.py`, `serve_project.py`, `serve_workbench.py`, `workbench.py`
— e.g. `opendox/branch_session.py:77: from openxdox import gate_console`,
present both at `ce53b489` (what openDox's assembly root pins) and at
`8e9ffa62`.

**A counting note, recorded rather than resolved.** "23 outbound" is a
whole-package figure from § D3's `serve.py` paragraph; the openXdox-destined
rows carry 25. The clause is not exactly measurable as written. It is left open
on substance, not on the arithmetic.

### 4.2 — LEFT OPEN. The pin is correct; the HAND ACT the box also assigns is absent.

**Met.** `contracts/opendox-pin.yaml` exists in the openXdox **assembly root**
and names the openDox **assembly root** by commit and tree digest, and the
commit is current:

```
commit            = 49a99df2561bf70e49337c999d79b36836718349
opensoft/openDox main = 49a99df2561bf70e49337c999d79b36836718349   ✓
digest_definition = sorted-ls-tree-r-v1
carve_commit      = b075fd91dc8fced8e1373825ba80220c33536bae
```

`contracts/manifest.yaml` carries `carved_from:` (`opensoft/openxFactory` at
`b075fd91`, `carve_tag: opendox-carve-0`, `legs: {code: 92, spec: 47}`) and
`project.yaml` carries `neutral_product_pins: [openDox]`.

**Not met.** The box assigns a HAND ACT beyond § 1.2's `--pin` seed — *"the
per-file `sha256`, `pinned_by_commit_only:` and the migration
range/reversibility/runbook the MODIFIED `neutral-product-pin` requires are a
HAND ACT this task also performs"* — and **none of the five is present**. The
landed file's complete key list is `schema_version, kind, pin_role, product,
source_repository, materialization, commit, revision_kind, digest_algorithm,
digest_definition, digests, digest_source, carve_commit, declared_in,
verify_pin`: it is the seed plus `carve_commit`, and nothing else. The MODIFIED
`neutral-product-pin` requires the first two unconditionally for a source-tree
pin, and this pin is `materialization: referenced` / `revision_kind: commit`, so
the published-artifact exemption does not reach it.

**Two further clauses of the same box also fail.** *"The dependency points ONE
way and there is no cycle"* — the 34 back-imports above are a live cycle. And
the pin chain is out of order against the box's own two-pin-moves-per-hop
paragraph: openXdox-code's `pyproject.toml` consumes openDox-code at
`8e9ffa62`, which is one commit AHEAD of the `ce53b489` that openDox's assembly
root `49a99df2` pins in both its `code` gitlink and its
`contracts/code-pin.yaml`. openXdox reaches past the assembly root, which is
the one reach the elected shape exists to prevent.

### 4.3 — LEFT OPEN. No fork of the server; but nothing declares the contributions.

**Met, decisively — "No fork of the server."** `serve.py` and `cli.py` are
ABSENT from openXdox-code; the leg consumes openDox instead
(`serve_gate.py:43`, `serve_projection.py:51`: `from opendox.serve_wire import …`).
The three contribution modules are present and structurally conformant to the
§ 2.4 extension points: `serve_gate.py:41 import route_extension`, `:238
def routes(self) -> tuple[route_extension.RouteBinding, ...]`; the same shape at
`serve_projection.py:48/371/375`; and `cli_gate.py:1364 class GateSubcommands`
with `def register(self, subparsers)`, matching
`subcommand_extension.MEMBERS = ("register",)`.

**Not met.** The composition point is a dangling reference. openXdox-code ships
**no profile-shaped module** — yet the pinned openDox still composes through
openxFactory's:

```
opendox/serve.py:1376  route_bindings = route_extension.collect_bindings(
opendox/serve.py:1377      tuple(profile_openxfactory.ROUTE_EXTENSIONS) + tuple(route_extensions))
opendox/cli.py:914     subcommand_extension.register_all(
opendox/cli.py:915         profile_openxfactory.SUBCOMMAND_EXTENSIONS, sub)
```

and `profile_openxfactory` exists nowhere in the carved estate. The manifest
marks `scripts/ideation_dashboard/profile_openxfactory.py`
`not_moved / deleted_at_carve`; its own docstring line 7 says *"after the carve
openXdox declares its own"*; openXdox declares none
(`ModuleNotFoundError: No module named 'profile_openxfactory'`). Two of the
three contribution modules also cannot be imported at all with the declared
dependency set — `serve_projection` (via `snapshot_registry.py:85`) and
`cli_gate` (via `gate_console.py:63`), both on `doc_health`.

### 4.4, 4.5, 4.6 — LEFT OPEN, as expected. No landed evidence at all.

* **4.4 (PARAMETERIZE).** No domain profile at openXdox-code — a sweep of
  `src/` for `domain_profile|DomainProfile|domain-profile|STATUS_VOCABULARY|
  status_vocabulary` returns no matches — and the hardcoded status words the box
  calls a defect are still in the engine: eight literal lines across three
  modules, e.g. `gate_console.py:171 STAGED_STATUS = "staged"`,
  `gate_console.py:1151 if state in ("rejected", "superseded"):`,
  `generator.py:349 if origin.get("kind") != "staged":`.
* **4.5 (BUILD what does not exist).** None of the three named features exists at
  either leg. A path sweep for `scenario`, `governed[-_]derived`, `evidence`,
  `assumption_register`, `role_authority`, `authority_projection` returns only
  carved artefacts of existing surfaces. Build-arc work under RULED OQ-N.
* **4.6 (cut `xdox-v1.0`).** No tag of any kind exists anywhere in the family:
  `gh api repos/opensoft/openXdox/tags`, `…/openDox/tags`,
  `…/openXdox-code/tags`, `…/openXdox-spec/tags` and
  `…/openXdox/releases` each return an empty list. Phase 6 is Brett Heap's own
  act and has not been taken.

---

## 2. The § 5.2 shed cannot land while the manifest stands — TWO PROBES

The § 5 remainder was to begin with the manifest's `deleted_at_carve` rows —
one row, `scripts/ideation_dashboard/profile_openxfactory.py` — as the half that
needs no landed sha. **It is not separable, and the reason generalises to the
whole shed.** Both probes were taken on throwaway commits off `ea34f22a` and
discarded.

### Probe 1 — the one `deleted_at_carve` row, deleted alone

**It breaks the retained adapter suite.** Four `stays_openxfactory_adapter`
rows — `test_route_extension.py`, `test_cli_column_split.py`,
`test_serve_column_split.py`, `test_extension_point_parity.py` — reach the
profile through `scripts/ideation_dashboard/cli.py:104`
(`from . import profile_openxfactory`), which is an unconditional
module-level import:

```
BEFORE:  120 passed in 16.72s
AFTER:   ERROR tests/ideation-dashboard/test_route_extension.py
         ERROR tests/ideation-dashboard/test_cli_column_split.py
         ERROR tests/ideation-dashboard/test_serve_column_split.py
         ERROR tests/ideation-dashboard/test_extension_point_parity.py
         E  ImportError: cannot import name 'profile_openxfactory'
                         from 'ideation_dashboard'
         Interrupted: 4 errors during collection
```

The repair is not available inside this act: `cli.py` and `serve.py` are
`moved_with_declared_edit` rows to `opendox_code`, and check 3 pass 2 compares
each moved row's blob at the revision under test against the referent — so
editing either refuses `carve-digest-mismatch`. **The carve surface is frozen
until the shed takes all of it at once.** This is runbook § 8's *"no ordering of
two commits leaves a green intermediate"* measured rather than asserted.

**It also refuses FLOOR PART 1.** At the deleting commit:

```
FAIL docs/opendox-carve-manifest.yaml: carve-path-absent — 1 row(s) name
path(s) DELETED SINCE THE CARVE — under the surface at b075fd91dc8f, absent at
1a470ac82f56: scripts/ideation_dashboard/profile_openxfactory.py
exit=2
```

and the required-suite seat goes red with it —
`tests/carve_manifest/test_carve_manifest.py::test_the_real_repository_answers_at_the_ruled_path`,
`1 failed, 197 passed` against a `198 passed` baseline.

### Probe 2 — the whole shed, all 319 rows

The same refusal, from the first row rather than the last:

```
FAIL docs/opendox-carve-manifest.yaml: carve-path-absent —
contracts/schemas/gate-action-record.schema.yaml: DELETED SINCE THE CARVE —
rows[0] declares it `moved_verbatim` at b075fd91dc8f, and 8f4d3f4dc4d3 no
longer carries it as a file
```

**So the finding is not about one row.** `check_surface`'s walk at the revision
under test refuses ANY tree in which a manifest row's source path has been
deleted, and the § 5.2 shed deletes 319 of them by construction. The validator's
own remediation line names the only two exits it knows — *"re-cut the manifest
at a new carve commit … the § 6 ceremony re-cuts, it never carries digests
forward"* — and both are reserved: the manifest is not this packet's file, and a
re-cut is runbook § 11's ceremony, not a step inside the shed.

**This is an unresolved prerequisite of § 5.2, and it is owed a ruling** — a
post-shed mode on `validate-carve-manifest.py`, a re-cut at the shed, or a
declared retirement of the manifest as the shed lands. Nothing in this record
chooses among them, and no floor script or manifest was edited in taking these
measurements.

---

## 3. The adapter re-point's own prerequisites, measured

The re-point declares `openxdox` resolvable through the mounted leg once
RULED OQ-L's submodule lands. Three facts bear on when that can be proved:

1. **The mount is two levels deep.** `opensoft/openXdox` is an assembly root
   whose own `.gitmodules` nests `code` → `opensoft/openXdox-code` and `spec` →
   `opensoft/openXdox-spec`, and its gitlinks name exactly the two landed legs
   (`code` → `59600412`, `spec` → `03eacc61`). The importable tree is therefore
   `openXdox/code/src`, which carries `openxdox/` beside the two top-level seams
   `route_extension.py` and `subcommand_extension.py`.
2. **CI does not check it out.** `.github/workflows/pytest-suite.yml:339` inits
   one named gitlink and no others — `git submodule update --init openXwallet` —
   and the OQ-L pin pull request does not amend it. Until a step inits `openXdox`
   **recursively**, `openXdox/code/` is empty on the runner, so any assertion
   that the leg imports either fails or degrades to a skip — and
   `EXPECT_SKIPPED` is pinned EXACTLY, as a SUM, so a degrading assertion moves
   a floor.
3. **The surface does not import yet.** The re-export module landed at
   `src/openxdox/openxdox_surface.py`, and it re-exports
   `opendox.branch_session.bootstrap_sessions` — which back-imports
   `openxdox.gate_console` at `branch_session.py:77`, which needs `doc_health`.
   Importing the surface therefore raises `ModuleNotFoundError: No module named
   'doc_health'`. An openxFactory adapter test importing through it needs both
   `doc_health` reachable and the cycle of § 1 broken — the § 3.5/§ 3.6 BUILD
   arc's work, not this one's.

---

## 4. What was NOT touched

`docs/opendox-carve-manifest.yaml`, `scripts/validate-carve-manifest.py`,
`scripts/verify-carve-arrival.py`, `scripts/carve_lines.py`,
`scripts/verify-openxdox-pin.py`, `docs/opendox-cutover-runbook.md`,
`contracts/openxdox-pin.yaml`, the `openXdox` gitlink,
`contracts/review-lane-floor-snapshot.yaml`,
`.github/workflows/pytest-suite.yml`, and — named here because § 8 of the
runbook says review conflates them — `.github/merge-approval-envelope.yml` and
`.github/workflows/merge-master-approval.yml`, whose enrollment covers the live
DATA directories `ideation/dashboard/intents/**` and
`ideation/dashboard/gate-records/**` and not the `scripts/ideation_dashboard/`
code surface the shed is aimed at. The fourteen
`stays_openxfactory_governance` rows were confirmed present and unmodified
(`14 governance rows; missing at HEAD: NONE`).
