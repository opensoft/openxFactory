# Tasks: add-neutral-product-standalone-operability

Status: draft

Dependency-ordered. **Group 1 is the authoring THIS change performs and it
touches no code.** Groups 2-15 are the post-ratification realization, each in the
repository named in its heading and each carrying the FALSIFICATION COMMAND that
closes it — an exact invocation with its checkout preconditions and its expected
result, so the archive gate's evidence under `release-realization` is a command
re-run and quoted rather than a description believed.

**Groups 2-12 and 15 take one requirement each; TWO groups take more than one,**
because their requirements are satisfied by one act and splitting them would
produce boxes that cannot be closed independently: **Group 13** takes
requirements 12 and 13 (the install brings its datastore AND its identity mode —
one install story), and **Group 14** takes requirements 6, 14 and 15 (the store
that holds a finding, the loop that fixes it, and the exception that suppresses
it — one schema and one loop). Requirement 6 is therefore reached TWICE, by
Group 6 for the check itself and by Group 14 for where its results live, which is
the amendment the ruling of 2026-09-22 made to it. The requirement-to-group map is
the group headings, read as written; nothing below claims a bijection.

**Three classes of verb appear in the commands, and the difference matters.**

1. **Verbs that EXIST today**: `generate`, `generate-and-open`, `create` and
   `edit`, in the exact shapes task 10.1's table records against the parser. The
   arc packages and unblocks them; it does not change them.
2. **Verbs this arc CREATES**, each declared by name and shape in ONE numbered
   box: `submit` (12.4a), `land` (12.6a), and `health run|list|fix|accept`
   (14.5). A falsification that uses one is an acceptance test for surface the
   realization must add, not a re-run of surface that exists.
3. **Prerequisites by name.** A group MAY use a verb, or a surface, that an
   EARLIER group declares, and it says so. Group 15 runs Group 14's `health run`
   and `health list`, so Group 15 cannot close before 14.5 lands. Groups 14 and
   15 store their results in Group 13's bundled datastore, and each falsifier
   selects it with `OPENDOX_INSTALL_MODE=local` in a fresh `OPENDOX_STATE_DIR`.
   12.5 needs Group 9, because the whole suite must first be runnable.

**The rule:** no box closes on a command whose verb is neither in 10.1's table
nor declared by its own group or by an earlier one it names.

**Fixture corpora are DIRECTORIES in the code leg's checkout, never
repositories**, and none exists today — `git ls-tree` over openDox-code's
`tests/fixtures/` at `3c3a9e31` lists four files, none of them a corpus. Each is
shipped by the first group that needs it (5.0, 7.0, 14.9, 15.6a). **Every
falsification that needs a repository COPIES its fixture into a fresh `git init`
first**, so no command below can create a branch or a commit inside the checkout
it is testing, and a git adapter pointed at a fixture reads that fixture rather
than the enclosing repository. Each block carries its own three setup lines and
its own commit identity, so every group runs from a fresh shell on its own.
**Setup steps are ONE COMMAND PER LINE, never chained with `&&`.** Under
`set -e` a failure anywhere but the LAST command of an `&&` list does not stop
the shell. A failed `git init` or `python -m venv` would therefore be skipped
silently, and the acceptance would go on to run against a directory that is
not a repository, or against whatever `opendox` is already on the PATH.
**Scratch space is resolved at run time, never named.** Each block that needs
scratch space starts with `W=$(mktemp -d)` and keeps every venv, capture file
and throwaway repository under `$W`. No committed command therefore names a
host-absolute path (the constitution's Principle IV), and two runs cannot
collide. The kernel's own interfaces are named as interfaces: `/dev/null`,
`/dev/tty` and `/proc` are the same on every Linux host and describe no host's
layout, and neither does the `--tmpfs /tmp` that bwrap mounts INSIDE a pack's
sandbox (15.1b).

House rule: OpenSpec ratifies, Speckit builds. No group below is started before
ratification, no group is started without its own claim on
`opensoft/openxFactory#656` per lane-collision-protocol Rule 1, and this change
merges nothing anywhere.

Baselines. The invariant is a DELTA, not a count: against the `main` it lands on,
this packet adds **+1 item and +1 passed, with ZERO new failures**, under
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and the pinned gate
`python3 scripts/validate-openspec-cli-pin.py --all --no-cache` exits 0 with
`0 UNDISPOSITIONED failures` and its one accepted exception
(`add-chain-attestation`, ratified disposition). Absolute counts move whenever
another change lands, so each record below is paired with the `main` it was
measured on:

| measured on `main` | `main` alone | with this packet | delta |
|---|---|---|---|
| `4f92d651` (filing, 2026-09-22) | 109 passed / 1 failed of 110 | 110 / 1 of 111 | +1 item, +1 passed, 0 new failures |
| `a151e462` (after merging #1141 and #1143) | 111 / 1 of 112 | 112 / 1 of 113 | +1 item, +1 passed, 0 new failures |

**The gate that matters is the one run at landing, against the `main` of that
moment.** The PR description publishes the latest row, and the archive gate
re-measures the same delta rather than trusting either row.

## Group 1 — Authoring (THIS change; no code byte)

- [x] 1.1 Author `.openspec.yaml` — ad-hoc origin, the drafting-provenance shape
  with NO approval pair (`add-drafted-proposal-origin`), naming the archived
  packet's unclosed residue as the origin.
- [x] 1.2 Author `proposal.md`: the owner's goal in his own words from `#656`;
  the two-products measurement; the repository-choice FINDING; the G-to-
  requirement table; the explicit "what openxFactory keeps" section; honest
  `code_surface:` / `target_release:` front-matter.
- [x] 1.3 Author the `## ADDED Requirements` delta creating
  `neutral-product-standalone-operability` — 16 requirements, 71 scenarios,
  domain-neutral, openDox as the measured instance.
- [x] 1.4 Author `design.md`: D1-D8 and **R-G3** — filed as Q-G3, the one question
  put to Brett with three options and a recommendation; RULED the same day and
  rewritten as the record of the decision, the options as they were put, and the
  CORRECTION to this packet's own pricing of the rejected option.
- [x] 1.5 `OPENSPEC_TELEMETRY=0 openspec validate add-neutral-product-standalone-operability --strict`
  and `--all --strict` pass with no NEW failure against the baseline above.
- [x] 1.6 `python3 scripts/proposal-support.py . verify add-neutral-product-standalone-operability`
  passes; the `tests/sequenced_after/corpus-ledger.yaml` row is machine-seeded
  (`scripts/validate-sequenced-after.py --seed-ledger --moved-by … --moved-on …`),
  and the README "OpenSpec Records" *Active changes* bullet is added.
- [x] 1.7 **RULING G3 — GIVEN.** Brett Heap, `#656` comment `5783335210`,
  2026-09-22T20:08:59Z: *"yes, openDox gets its own neutral generator."* Group 5
  is no longer blocked and requirement 4 is written to the ruling. `design.md`
  § R-G3 records the options as they were put, what was ruled, and the CORRECTION
  to this packet's own pricing of option (a) — `generator.py:66-68` imports
  `doc_health`, which this packet had not measured when it recommended (c).
- [ ] 1.8 On ratification: `Status: ratified` + `Ratified by:` on all three
  lifecycle documents; `## Ratification record` in `proposal.md`; the approval
  pair ADDED beside the fixed origin in `.openspec.yaml`, never substituted.

## Group 2 — Requirement 2 / G1: imports with no consumer, publisher or host (openDox-code)

The highest-leverage box: TWO import statements, 1,232 of 1,298 measured errors
at `f8a1ece`, zero passed. An AST census of `src/` finds exactly two import-time
reaches (`serve.py:199`, `serve.py:206`) and two deferred ones; every other
mention in the package is prose.

- [ ] 2.1 Remove the module-level `from ideation_dashboard import
  serve_openxfactory_lanes` (`src/opendox/serve.py:199`) and the
  `from ideation_dashboard.serve_openxfactory_lanes import (…)` re-export block
  (`:206`). The five names (`ACTIONS_APPLY_REGISTER_EDITS_ROUTE`,
  `ACTIONS_DTN_SEED_ROUTE`, `ACTIONS_REFRESH_ROUTE`,
  `ACTIONS_STAGING_SEED_ROUTE`, `COMMITTED_INTENTS_ROUTE`) belong to
  openxFactory's lanes surface, filed `stays_openxfactory_adapter`. All five are
  plain route strings (`"/committed-intents.json"`, `"/actions/refresh"`,
  `"/actions/apply-register-edits"`, `"/actions/dtn-seed"`,
  `"/actions/staging-seed"`).
- [ ] 2.1a **DO NOT VENDOR the module.**
  `scripts/ideation_dashboard/serve_openxfactory_lanes.py` itself imports
  `from openxdox import snapshot_registry` (`:70`) and
  `from openxdox.serve_projection import hosted_ref_refused` (`:77`), so copying
  it into openDox re-creates the consumer dependency BUILD slice 2b removed.
- [ ] 2.2 Contribute those routes through the EXISTING seam —
  `serve.build_server(route_extensions=)` / `route_extension.RouteBinding` — from
  openxFactory's side, per the carve `design.md`'s own specification. No new
  mechanism is designed here.
- [ ] 2.3 Sweep every remaining module-level reach: grep `src/` for
  `ideation_dashboard`, `corpus_adapter_openxfactory`, `doc_health` and
  `openxdox` at import position, and close or defer each with a recorded reason.
- [ ] 2.4 Add a test in openDox-code's own suite that imports EVERY module of the
  package in a checkout with no sibling installed, failing with the name of the
  first module that still needs one.
- [ ] 2.5 Remove `validate.yml`'s three `--noconftest` steps and their enumerated
  file lists; the suite collects whole. Measured at `f8a1eced` by extracting the
  `run:` blocks that invoke pytest: **four blocks name 37 distinct test modules of
  the 63 in the tree** (`tests/` 53 + `tests_runtime/` 10), three of them under
  `--noconftest`; **26 modules are named by no pytest step at all**. This is the
  figure the whole packet uses — an earlier reading of "31 of 53" counted only the
  `--noconftest` blocks over `tests/`. The autouse fixture that produces
  the 1,298 setup errors is `tests/session_fixtures.py:413`, whose body is
  `from opendox import cli as cli_mod`.
- [ ] 2.6 Correct openDox-code's `README.md:39-42`, which still gives the
  narrowing's reason as *"Until the BUILD arc … inverts the openDox → openXdox
  dependency"*. That dependency IS inverted at import time; the live cause is
  `ideation_dashboard`.
- [ ] **FALSIFIED BY** (a checkout of openDox-code alone, installed WITH every
  extra it declares — `.[runtime,test]` — so that any `ImportError` left is a
  reach into a sibling and not a missing third-party package):

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

  **The sweep is generated, not listed.** `pkgutil.walk_packages` visits every
  module the package has: 57 `.py` files under `src/opendox/` at `3c3a9e31`. A
  module added later is covered without editing this command, and a fourth
  module keeping an import-time reach cannot pass beside three that were fixed.
  The absence of each sibling is ASSERTED first. Today the sweep fails on
  `opendox.serve`, `opendox.cli` and `opendox.notebook_action` at least, each with
  `ModuleNotFoundError: No module named 'ideation_dashboard'`.

## Group 3 — Requirement 3 / G2: a default domain profile (openDox-code)

- [ ] 3.0 **RATIFICATION READ FIRST.** Requirement 3 revisits the PREMISE of RULED
  ASK-2 option (2) (`#656` comment `5628886636`) — not its reasoning. An EMPTY
  default stays refused; what changes is the refusal text's premise that *"openDox
  … ships no profile of its own"*. If the ratification read takes ASK-2 to
  foreclose this, requirement 3 is struck and the other **fifteen** stand. See
  `design.md` § D5.
- [ ] 3.1 Ship a default profile for openDox's OWN domain — documents and ideas —
  carrying none of openxFactory's status taxonomy or change/spec/delta nouns
  (RULING C2, DIRECTION Q5). Note the standalone problem this closes: the only
  host that exists, openxFactory's `scripts/opendox_host.py`, builds a composite
  whose base class is `openxdox.domain_profile.DomainProfile`, so today's only
  real profile needs BOTH siblings present.
- [ ] 3.2 `build_parser()` and `build_server()` fall back to it when no host has
  called `domain_profile.register()`, and a registered profile still replaces it.
  `profile_proxy.py`'s refusal is kept for the case it was written for — an
  ambiguous registration — and is NOT weakened into an empty tuple.
- [ ] 3.3 Record in the carve manifest that the `deleted_at_carve` row for
  `profile_openxfactory.py` is UNCHANGED by this: openxFactory's profile stays
  deleted from the core and `scripts/opendox_host.py` remains openxFactory's host.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v3"                       # a FRESH environment: nothing already installed stands in
      . "$W/v3/bin/activate"
      pip install ".[test]"
      python -c "from opendox.cli import build_parser; build_parser(); print('OK')"
      python -c "from opendox import domain_profile as d; print('OK', d.name_of(d.current()))"
      python -m pytest -q tests/test_profile_registration.py   # a REGISTERED profile still replaces the default

  Both lines print `OK`, the second with the default profile's name. Today both
  raise `domain_profile.ProfileNotRegistered` (`domain_profile.py:220`). The
  second line asks `domain_profile.current()`, the call every consumer of the
  profile makes. An earlier draft called `build_server()` with no arguments, but
  it takes three required positional ones (`web_dir`, `snapshot_path`,
  `checkout_root`), so that line would have failed with a `TypeError` whatever
  the profile did.

## Group 4 — Requirement 5 / G4: the deferred reach resolves through the seam (openDox-code)

- [ ] 4.1 Replace `src/opendox/authoring.py:318`'s
  `from corpus_adapter_openxfactory import home_corpus` with a resolution of the
  REGISTERED home corpus through openDox's own `corpus_adapter` seam. The
  registration point is declared here, beside `domain_profile.register()`:
  `corpus_adapter.register_home(factory)`, where `factory` has `home_corpus`'s
  own shape (`adapter, ref = factory(root)`, as `authoring.py:324` calls it), and
  `corpus_adapter.home()` returns what was registered. openxFactory's host
  registers `corpus_adapter_openxfactory.home_corpus` at start, as it registers
  its profile.
- [ ] 4.2 Where nothing is registered, `corpus_adapter.home()` raises the
  interface's ONE exception, `CorpusRefused` (`corpus_adapter.py:164`), with a
  NEW refusal kind, `ADAPTER_NOT_REGISTERED`, added to `REFUSAL_KINDS` (`:135`).
  Its `subject` names the seam (`opendox.corpus_adapter`) and its `detail` names
  the remedy (`corpus_adapter.register_home(...)`). It is never a
  `ModuleNotFoundError` raised from inside a function, and never any other
  exception.
- [ ] 4.3 **Route EVERY deferred reach through a seam the product declares. None
  stays late-bound by name.** Requirement 5 admits no exception for a reach
  "owed to the consumer": a reach that names a consumer or publisher package by
  module name is exactly what keeps the product from standing alone. Measured at
  openDox-code `1e4a57fb` by the scan below, there are **27** deferred reaches.
  **19** go into openXdox, and they are the ratchet's (`branch_session.py` 7,
  `serve_workbench.py` 7, `serve.py` 2, `serve_project.py` 2, `cli.py` 1). **8**
  go into openxFactory, and no ratchet counts them: `authoring.py:318` (4.1);
  `doc_health` at `workbench.py:746` and `:1407-1409`, and at `serve.py:713`;
  and `ideation_dashboard` at `doxbench_packet.py:177` and `serve_wire.py:1369`.
  Each resolves through an existing seam (the `corpus_adapter` Protocol, the
  domain-profile registry, the route and subcommand extension points, 12.4's
  submission bindings) or through one declared for it, as 5.4 declares the
  generator's. With nothing registered, a verb refuses naming its seam and its
  remedy, which is 4.2's discipline. `workbench.py`'s four are the reaches
  `run_scoped_doc_health` makes (6.2). Once routed here, they refuse until Group
  6 registers openDox's own check. `consumer_reach.py` is the late stand-in whose
  own text calls this injection BUILD-arc work, and it is retired with its last
  name. openXdox-code's ratchet (`OPENDOX_BACK_IMPORTS`) is tightened to `(0, 0)`
  in the same landing. The import-time column is already `0` for the consumer,
  and the two import-time reaches into the publisher (`serve.py:199`, `:206`) are
  Group 2's.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling, no
  `corpus_adapter_openxfactory` importable):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v4"                       # a FRESH environment: nothing already installed stands in
      . "$W/v4/bin/activate"
      pip install ".[test]"
      if python -c "import corpus_adapter_openxfactory" 2>/dev/null; then echo "FAIL: the publisher's adapter is importable"; exit 1; fi
      python3 - <<'PY'
      import opendox.authoring as a
      from opendox import corpus_adapter as ca
      try:                                                  # NOTHING is registered in this process (4.2)
          got = a.required_header_fields()
      except ModuleNotFoundError as e:
          raise SystemExit(f"FAIL: the deferred reach still imports a publisher module: {e}")
      except ca.CorpusRefused as e:                         # the interface's ONE exception, and nothing else
          r = e.refusal
          assert r.kind == ca.ADAPTER_NOT_REGISTERED, f"refused for another reason: {r.kind!r}"
          assert "corpus_adapter" in r.subject, f"the refusal does not name the seam: {r.subject!r}"
          assert "register_home" in r.detail, f"the refusal does not name the remedy: {r.detail!r}"
      else:
          raise SystemExit(f"FAIL: nothing is registered, yet the verb answered {got!r}")
      PY
      # ...a REGISTERED adapter answers through the seam, not through a name (4.1):
      python -m pytest -q "tests/test_authoring_seam.py::test_required_header_fields_come_from_the_registered_adapter"
      # ...and NO deferred reach anywhere in the package names the consumer or the publisher (4.3):
      if [ -e src/opendox/consumer_reach.py ]; then echo "FAIL: the late stand-in consumer_reach.py survives"; exit 1; fi
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

  **With nothing registered, the block accepts exactly ONE outcome**:
  `CorpusRefused` of kind `ADAPTER_NOT_REGISTERED`, naming the seam and the
  remedy. Any other exception fails it, an unrelated `TypeError` included, and so
  does an answer. The named test then registers a stand-in adapter and requires
  the fields to be the ones that adapter declares, so the answer is proved to
  come through the registry and not through a name. **The scan reads the whole
  package**, not the ratchet's five modules. It is a static reading of every
  import and every `import_module`/`__import__` call with a literal name, written
  inside a function body, and it needs no sibling installed to find one. Run
  against `1e4a57fb` before this box was written, it names the 27 reaches above
  and exits non-zero. Retiring `consumer_reach.py` closes the one dynamic path the
  scan cannot read, a name held in a variable. Today `required_header_fields()`
  raises `ModuleNotFoundError: No module named 'corpus_adapter_openxfactory'`
  while `python -c "import opendox.authoring"` exits 0.

## Group 5 — Requirement 4 / G3: openDox's own neutral projection (RULED, openDox-code)

**RULED: openDox gets its OWN neutral generator. `generator.py` does not move.**
The audit this box used to open with is spent — it would have priced a relocation
nobody is doing — and its decisive finding is recorded instead: `generator.py`
imports `doc_health` at `:66-68`, so relocating it was never lawful under
`corpus-adapter-seam` whatever its literals said.

- [ ] 5.0 **Ship `tests/fixtures/plain-documents`** — first needed here, and
  Groups 7 and 13 read it too: a handful of `.md` documents spread across the six
  neutral stages, carrying NONE of openxFactory's governance vocabulary, which is
  what lets the assertion below mean something. That vocabulary is DECLARED data,
  not a hand-picked sample. It is the eight document-lifecycle `Status:` words
  (`brainstorm`, `staged`, `draft`, `ratified`, `standard`, `superseded`,
  `retired`, `record`) and the change/spec/delta nouns (`openspec`,
  `proposal.md`, `tasks.md`, `design.md`, `ADDED Requirements`, `MODIFIED
  Requirements`). A test keeps the fixture free of all of them.
- [ ] 5.1 Write openDox's SMALL NEUTRAL PROJECTION over the `CorpusAdapter`
  protocol already declared at `src/opendox/corpus_adapter.py` (a
  `@runtime_checkable` `Protocol`, six closed members: `resolve`,
  `list_documents`, `read`, `classify`, `check`, `write_back`). New neutral code
  written to openDox's needs — NOT 3,164 lines re-expressed, and NOT a copy of
  openXdox's.
- [ ] 5.2 Bind `src/opendox/runtime/local_git_adapter.py` (2,796 lines, RULING
  C3's plain local git repository) as the conformant implementation, so the
  projection has a real corpus to read with nothing else installed.
- [ ] 5.3 Render `NEUTRAL_DISPLAY`'s SIX WORDS and no others — `sources`,
  `groups`, `candidates`, `selections`, `submissions`, `completed` (RULED
  *"keep those six words"*, same comment; the sixth is **`completed`** by RULING
  `5784654370`, *"2, keep completed"*, which corrected this packet's earlier
  `completions` — the DECLARED value in `display_profile.py`, not the docstring
  that narrated it). **No word is re-authored and no workflow is designed.**
  `src/opendox/display_profile.py` is unchanged by this group.
- [ ] 5.3a **openXdox declares the estate's FIRST `DISPLAY` facet — partial, one
  stage** (openXdox-code; RULED `5784683830`, *"1, keep completed and overlay
  implemented"*). On the profile openXdox contributes —
  `src/openxdox/domain_profile.py:317`'s `DomainProfile`, which openxFactory's
  `scripts/opendox_host.py` composite inherits — declare `DISPLAY` labelling the
  `completion` stage **"implemented"**, the governed lifecycle's own word, in its
  `short` AND its `label` field (measured: a facet giving `short` alone leaves
  `label` at `completed`), and NOTHING ELSE — openDox fills every other role and
  field from `NEUTRAL_DISPLAY`. The neutral word does not move. Claim it on
  `#656` before starting, like every group here.
- [ ] **FALSIFIED BY** (openXdox-code checkout with openDox installed):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      : "${OPENDOX_CODE:?set OPENDOX_CODE to an openDox-code checkout at the tip of the arc}"
      python -m venv --clear "$W/v5a"
      . "$W/v5a/bin/activate"
      pip install ".[test]"
      pip install --force-reinstall --no-deps "$OPENDOX_CODE"   # the REALIZED openDox wins over any pinned one
      python3 - <<'PY'
      from opendox.display_profile import STAGE_ROLES, host_display, normalize_display
      from openxdox.domain_profile import DomainProfile
      facet = host_display(DomainProfile)                   # None today: no profile declares one
      assert facet is not None, "openXdox declares no DISPLAY facet"
      merged, neutral = normalize_display(facet), normalize_display(None)
      done = merged["stages"]["completion"]
      assert done["short"] == "implemented" and done["label"] == "implemented", done
      assert neutral["stages"]["completion"]["short"] == "completed"   # the neutral word stands
      for role in (r for r in STAGE_ROLES if r != "completion"):
          assert merged["stages"][role] == neutral["stages"][role], f"{role} was overlaid too"
      PY

  Three things, each an assertion: the governed host sees "implemented" wherever
  the stage is named; a host with no facet — and a standalone install — sees
  "completed"; and the facet is PARTIAL, the other five stages byte-identical to
  the neutral ones, so an overlay cannot quietly grow into a second vocabulary.
  The same calls were run against openDox-code `3c3a9e31` with a stand-in profile
  before this box was written, and behave as asserted.
- [ ] 5.4 **DECLARE THE GENERATOR SEAM — it does not exist and `CorpusAdapter` is
  not it.** `src/opendox/corpus_adapter.py`'s Protocol is CLOSED at six members
  (`resolve`, `list_documents`, `read`, `classify`, `check`, `write_back`) and its
  own docstring says *"Six methods. Nothing else, ever"* — none of them is a
  generator handoff, so "contribute it through the same seam" would name nothing
  and let two incompatible implementations both claim conformance. This box
  declares the seam: the operation handed over, the registration point (beside
  `domain_profile.register()`, which is the shape the product already uses), and
  the conformance a contributed generator must satisfy. `consumer_reach.py` says
  the corresponding injection *"does not exist yet and is BUILD-arc work"* — this
  is that work.
- [ ] 5.4a openXdox KEEPS `generator.py`, `snapshot.py`, `snapshot_registry.py`,
  `completeness.py` and `corpus_root.py`, and contributes its governed generator
  through the seam 5.4 declares. The publisher's corpus is projected exactly as
  today and the consumer loses no capability — requirement 4's third scenario is
  the check.
- [ ] **FALSIFIED BY** (5.4a; an openXdox-code checkout with the realized openDox
  installed and Group 9 landed): the governed projection's own suites pass, and the
  arc did not edit them.

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      : "${OPENDOX_CODE:?set OPENDOX_CODE to an openDox-code checkout at the tip of the arc}"
      python -m venv --clear "$W/v5b"
      . "$W/v5b/bin/activate"
      pip install ".[test]"
      pip install --force-reinstall --no-deps "$OPENDOX_CODE"   # the REALIZED openDox wins over any pinned one
      ls tests/test_generator.py tests/test_snapshot*.py tests/test_session_snapshot.py > "$W/gen-suites.txt"
      while read -r f; do python -m pytest -q "$f"; done < "$W/gen-suites.txt"
      : "${ARC_BASE:?set ARC_BASE to the commit of this repository before the first landing of the arc here}"
      git log --format=%H --grep='^Arc: neutral-product-standalone-operability$' "$ARC_BASE..HEAD" > "$W/x-arc.txt"
      test -s "$W/x-arc.txt"                                # 11.0: the arc DID land here (5.3a at least), so empty means a dropped trailer
      : > "$W/x-paths.txt"
      while read -r c; do
        git diff --name-only "$c^1" "$c" >> "$W/x-paths.txt"
      done < "$W/x-arc.txt"
      python3 - "$W/x-paths.txt" "$W/gen-suites.txt" <<'PY'
      import sys
      touched = {l.strip() for l in open(sys.argv[1]) if l.strip()}
      suites = {l.strip() for l in open(sys.argv[2]) if l.strip()}
      edited = sorted(touched & suites)
      if edited:
          sys.exit("FAIL: the arc edited the governed projection's own proofs: " + ", ".join(edited))
      PY

  Requirement 4's third scenario says the consumer loses no capability, and these
  are the suites that already pin the governed snapshot, including its
  determinism. Six exist at `ab04453d`: `test_generator.py`, `test_snapshot.py`,
  `test_snapshot_determinism.py`, `test_snapshot_registry.py`,
  `test_snapshot_validation_launch.py` and `test_session_snapshot.py`. The set is
  taken by glob rather than typed out, and a suite the arc rewrote would prove
  nothing, so edits to them are refused through 11.0's trailer.
- [ ] 5.5 Lower `consumer_reach.py`'s generator-facing deferred reaches as the
  projection replaces them; the import-time column stays at zero.
- [x] 5.6 **Do NOT author the view-wiring slice here** — and it can no longer be
  duplicated: it was CLAIMED on openDox-code under actor `viewwire` (RULED *"wire
  the views and land it"*, same comment) and LANDED as **openDox-code#35 →
  `3c3a9e31`** (2026-09-22T21:39:18Z), converting the hardcoded
  `stage-brainstorm` / `stage-staged` / `stage-realized` spellings in
  `src/opendox/web/views/` to role lookups and joining `lens.js` to the display
  facet. Ticked on that landing, which is the evidence; nothing in this arc
  re-does it. The ruling is explicit that the generator is not in that claim.
- [ ] **FALSIFIED BY** (openDox-code checkout, `pip uninstall -y openxdox` so that
  `python -c "import openxdox"` raises, AND `python -c "import doc_health"` raises
  too — the neutral projection must reach neither the consumer nor the publisher
  — over a fixture directory of plain `.md` documents carrying none of
  openxFactory's governance vocabulary):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v5"                       # a FRESH environment: nothing already installed stands in
      . "$W/v5/bin/activate"
      pip install ".[test]"
      for sibling in openxdox doc_health; do                # a FRESH environment makes them absent; ASSERT it
        if python -c "import $sibling" 2>/dev/null; then echo "FAIL: $sibling is importable"; exit 1; fi
      done
      # NOT the console script: 10.1 packages that later, and this list is
      # dependency-ordered. At group 5's boundary the module is importable
      # (group 2) and that is what this falsifier uses.
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

  Under `set -euo pipefail` the sequence exits non-zero on any step; the
  assertions are IN the command rather than in prose, so the check is
  machine-detectable. `python -m opendox.cli` is an entry point that EXISTS:
  `cli.py:30-58` runs under `__main__` and hands over to the package copy's
  `main()`, so this command reaches `cmd_generate` exactly as the console script
  10.1 later packages will. Every option follows the verb, as 10.1's table records
  against the parser.

## Group 6 — Requirement 6 / G5: a health check over openDox's own documents (openDox-code)

- [ ] 6.1 **Expect to find almost nothing generic, and plan for that.** A strict
  measurement — comments and docstrings stripped, so only executable code counts
  — finds exactly ONE of `scripts/doc_health/`'s 37 Python modules free of
  openxFactory/OpenSpec identifiers: `lines.py`, 133 lines of 31,437 (0.4%).
  About 13 modules mix a reusable mechanism with hard-coded corpus identifiers
  (`corpus.py:39,59,92-93`; `inventory.py:37,52`; `preflight.py:20-25,180-185`),
  and about 23 are corpus operations by subject. **There is no extractable
  generic doc-health core**, so requirement 6 is satisfied by openDox growing its
  own check over its own declaration — not by relocating families.
- [ ] 6.1a Where a module genuinely mixes both, relocate the generic part into a
  module both sides depend on BEFORE either side moves — `corpus-adapter-seam`'s
  relocation rule applied inside a module.
- [ ] 6.2 openDox carries a health check over its own documents, reading its own
  declaration. **No openxFactory check family moves** (requirement 1). The seam
  already exists and is DEAD: `src/opendox/workbench.py:1389`'s
  `run_scoped_doc_health` (families `status-validity`, `tag-hygiene`) catches the
  `ImportError` and records `status = not-available`,
  `detail = doc-health machinery unavailable: No module named 'doc_health'`. Give
  it something to call.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v6"                       # a FRESH environment: nothing already installed stands in
      . "$W/v6/bin/activate"
      pip install ".[test]"
      python3 - <<'PY'
      from opendox import workbench
      r = workbench.run_scoped_doc_health(".", ["README.md"])
      assert isinstance(r, workbench.ActionResult), type(r)
      assert r.status == "completed", f"the check did not run: status={r.status!r} detail={r.detail!r}"
      assert isinstance(r.findings, list) and r.reference, f"no result shape: {r!r}"
      PY

  The call returns an `ActionResult` DATACLASS (`workbench.py:1339`) whose
  `status` is one of `completed | not-available | skipped`, so the assertion is on
  the one value that means the check RAN — not merely on the call returning. The
  earlier form of this command printed the status and exited 0 whatever it was,
  and it subscripted the result (`['status']`), which a dataclass refuses with a
  `TypeError`: it could neither fail for the right reason nor pass. Today the
  assertion fails on `status='not-available'`, with
  `detail = doc-health machinery unavailable: No module named 'doc_health'`.

## Group 7 — Requirement 7 / G6: a validator openDox can run (openDox-code)

- [ ] 7.0 **Ship `tests/fixtures/malformed`**: 5.0's `plain-documents` with
  EXACTLY ONE rule violation the validator must name, so the falsification below
  can tell "refused for that rule" from "refused for anything". The fixture
  carries a file `EXPECTED_RULE` holding the IDENTIFIER the validator reports for
  that violation, so the acceptance asserts the rule itself and not a wording it
  guesses at.
- [ ] 7.1 **NARROW THE INPUT SET FIRST, then acquire what remains.** The existing
  validator's `SCHEMA_FILENAMES` names **ten** schemas and they have three
  different owners, so "give openDox the whole set" is the wrong shape:

  | owner | count | schemas |
  |---|---|---|
  | `opensoft/openDox-spec` | 3 | `ideation-workbench`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` |
  | `opensoft/openXdox-spec` | 3 | `ideation-dashboard-snapshot`, `ideation-dashboard-snapshot-index`, `gate-action-record` |
  | `openxFactory` | 4 | `ideation-possibles-register`, `project-register`, `demotion-execution-receipt`, `gate-intent` |

  Ownership is settled, not inferred: `docs/contract-versioning-policy.md`
  § 1047-1053 records openxFactory DIVESTING the first six to the two spec legs
  by canonical home, leg commit and unchanged `sha256`. Both code legs and both
  assembly roots carry **zero** schema files.

  **The default direction, and the one this task recommends:** openDox's
  validator validates openDox's OWN document kinds — its spec leg's **three** —
  which are openDox's own spec leg's. **How they reach the code leg is the part
  requirement 7 constrains and this box must settle, because the two obvious
  answers contradict each other.** `AGENTS-shape.md` puts a contract the code
  READS but does not OWN in the SPEC leg, reached from the assembly root with
  `CONTRACTS_DIR` — but `docs/project-repo-schema.md:54-58` puts the assembly and
  the code leg in DIFFERENT repositories, so an assembly-root read cannot satisfy
  requirement 7's one-checkout rule in a code-leg-only checkout. **The resolution
  this box takes: the INSTALLED product is the checkout requirement 7 means.** The
  three schemas ship as PACKAGE DATA of the openDox distribution, so
  `pip install openDox-code` puts them on disk beside the validator and the
  assembly root remains their source of truth for editing. The falsifications
  below therefore run against an INSTALLED product, not a bare clone. If that
  packaging is refused, the alternative is to run the validator from the assembly
  root and amend requirement 7's scenario to say so — recorded here so the choice
  is visible rather than discovered at implementation. The
  openXdox-spec three belong to the CONSUMER's validator and openDox never needs
  them. Only if a measured openDox verb genuinely needs one of openxFactory's
  four does it arrive as the DIGEST-PINNED VENDORED COPY `neutral-product-pin`
  admits — a CONSUMED manifest member, and note that capability admits **ONE**,
  so needing more than one is itself a finding to raise rather than a thing to do.
- [ ] 7.1b **AND TWO OF THOSE FOUR ARE NOT AVAILABLE BY THAT ROUTE AT ALL.**
  `gate-intent.schema.yaml` is an INTENT-PLANE schema — the carve manifest lists
  it among the validator's contract files (`docs/opendox-carve-manifest.yaml:459`)
  and requirement 1 keeps the intent-plane schemas with openxFactory. Vendoring
  it would satisfy requirement 7 by breaching requirement 1, which requirement 7's
  fifth scenario now refuses in terms. The same reasoning covers
  `ideation-possibles-register.schema.yaml`, filed
  `stays_openxfactory_adapter` as openxFactory's own candidate register. **If the
  narrowing in 7.1 is done properly, openDox needs neither**; if an openDox verb
  appears to need one, raise it as a finding about the boundary rather than
  copying the schema.
- [ ] 7.1a Record why the existing script cannot simply be reused: it derives
  `SCHEMAS_DIR` from `__file__` (`validate-ideation-dashboard-contracts.py:114-115`)
  and so looks for a `contracts/schemas/` its own leg does not have — run from
  openXdox-code it exits 2 with `ERROR .../contracts/schemas not found`. That is
  the G6 defect in one line, and it is the consumer's to fix for its own set.
- [ ] 7.2 openDox-code has **no `scripts/` directory at all** and one console
  script. Whatever validator it gains is new surface at the code leg, not a
  relocated one.
- [ ] 7.3 **Three carve-broken defects in `openxdox/snapshot.py` are unclaimed
  and belong to this box**, registered by the archived packet's § 5.5 residue and
  owed to *"a follow-up act with its own claim"* that nobody holds: `SCHEMAS_DIR`
  resolves to an absent directory; `VALIDATOR_RELPATH` names a path openxFactory
  shed; and **`find_validator`'s parent walk ADOPTS AN ENCLOSING PRE-SHED
  CHECKOUT** — which is exactly the "reaching into a host tree instead of an
  injected adapter" class this arc exists to close, appearing a second time.
  Claim them here or hand them on by name; do not leave them unowned again.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling, **INSTALLED into a
  fresh venv**, because 7.1 settles that the three schemas travel as PACKAGE
  DATA and a bare clone therefore cannot exercise the packaged set this box is
  about). Validation is the
  POST-RENDER step inside the generate verbs — there is no `validate` verb and
  this packet adds none — so it is exercised through `--strict`, which also makes
  a validator that could not RUN fatal instead of a warning:

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

  The first exits 0; the second exits NON-ZERO and the sequence asserts that
  rather than printing it, so a validator returning zero on a malformed corpus
  fails the check. **The refusal must carry the fixture's own rule identifier.**
  A validator that failed for a missing schema, a generic error, or with empty
  stderr would not produce it, so the positive `grep -qF` is what proves the
  intended rule ran. The negative line only closes the one failure this box
  measured today. The last line is a NEGATIVE `grep` — `! grep -q` — not
  `grep -qv`, which would have succeeded on any single non-matching line and so
  passed a mixed "missing schema AND rule error" stderr. **Neither may fail on an unresolvable schema path** — today
  that is exactly how it fails, because `--strict` makes "the validator is
  unreachable" fatal and the validator is unreachable.

## Group 8 — Requirement 8 / G7: openDox-spec governs openDox (openDox-spec) — BLOCKED

**These boxes carry the reserved `[~]` marker, not `[ ]`, and that is deliberate.**
They are NOT this packet's act — they are openDox-spec's, in a repository this
packet cannot write — so a literal unchecked box would make this packet
unarchivable for work it was never entitled to do. The marker is the corpus's own
(`split-opendox-two-layer-product` closed at 67 [x] / 0 [ ] / 5 [~]).
**Owner: whoever holds openDox-spec's instance.**
**Exit condition: requirement 8's third scenario — when openDox-spec has promoted
the requirements the carve's map assigns it, these boxes close there and this
packet's interim arrangement ends.**

- [~] 8.1 openDox-spec promotes the requirements the carve's ratified
  per-requirement map assigns to openDox (the map's split: **71 openDox / 16
  openXdox / 15 openxFactory**; the 16 were carried into openXdox by the carve's
  § 6.1 and § 6.5 closures, and the 15 were re-promoted here by
  `repromote-engineering-vocabulary` under RULING DQ-1 — only openDox's 71 have
  no home). Measured by normalized-title scan of every `spec.md` in openDox-spec:
  **68 of the 71 appear nowhere in the repository**, and the three that do appear
  only inside `## MODIFIED` blocks of draft changes.
- [~] 8.1a **Unblocks openDox-spec's own backlog, which is why this is not
  housekeeping.** Three of its four active changes carry `## MODIFIED` blocks
  against `ideation-dashboard`, a spec that does not exist there, so **they can
  never be archived** — the loop is open at both ends: nothing can be promoted
  because nothing has been archived, and nothing can be archived because nothing
  has been promoted. Promoting the 71 is what breaks it.
- [~] 8.1b **Raise openDox-spec's CLI pin while doing it.** Both spec legs pin
  `@fission-ai/openspec@1.2.0`; openxFactory pins 1.12.0 by content address. Run
  against the same tree, **1.2.0 emits none of the three "Archive would refuse
  this delta" notices** that 1.12.0/1.13.x report. openDox-spec's gate cannot see
  the defect in 8.1a.
- [~] 8.2 On that landing, requirement 8's third scenario fires and work scoped to
  openDox is authored in openDox-spec. This packet's interim arrangement ends.
- [~] **FALSIFIED BY** (openDox-spec checkout):

      OPENSPEC_TELEMETRY=0 openspec list --specs
      OPENSPEC_TELEMETRY=0 openspec validate --all --strict

  The first lists the promoted capabilities; the second passes with no "Archive
  would refuse this delta" notice under a CLI at or above the openxFactory pin.
  Today the first answers `No specs found.`, and three of four changes carry the
  notice under 1.12.0 while their own gate at 1.2.0 cannot see it.

## Group 9 — Requirement 9 / G8: each leg's suite green alone (both legs)

- [ ] 9.1 openDox-code's required check runs the whole suite, no `--noconftest`,
  no file list (follows group 2).
- [ ] 9.2 openXdox-code the same, with `OPENDOX_BACK_IMPORTS` lowered as each
  deferred reach closes. The import-time column is ALREADY zero and stays there.
- [ ] 9.2a **Add the missing instrument.** No gate watches the openDox →
  openxFactory direction — the ratchet measures openDox → openXdox only, which is
  how two import-time reaches into the publisher survived a completed inversion
  under a green check. Requirement 2's third scenario is that instrument.
- [ ] 9.3 Behaviours needing both legs become declared INTEGRATION tests naming
  the pin they compose at, rather than being dropped from both suites — including
  the 31-entry assembled `--help` tree the carve manifest records as one
  *"which after the carve neither leg produces alone"*
  (`docs/opendox-carve-manifest.yaml:3088`). Nothing anywhere reproduces it today.
- [ ] 9.4 **Restore the margin, and stop the skips carrying the gap.** Both legs
  pass their floors with ZERO margin (openDox `1114/1111/3`, openXdox
  `539/533/6`), and every one of openXdox's six skips carries the same reason —
  *"doc_health reachability is BUILD-arc work (§ 3.5/3.6) … this test will assert
  for real once that lands"*. Two of openDox's three are the mirror image. **The
  whole-product assertions are precisely the ones that skip**, which is why both
  legs report green while neither product runs.
- [ ] 9.5 Note for whoever takes this box: openXdox pins openDox at `5c137a90`,
  nine commits behind openDox-code `main`, and the openDox root's gitlink and
  `contracts/code-pin.yaml` name `d816cf06`, two behind. Both are ancestors —
  nothing is forked — but the pins move before the integration run means
  anything.
- [ ] **FALSIFIED BY** (each leg's own checkout, no sibling installed):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v9"                       # a FRESH environment: nothing already installed stands in
      . "$W/v9/bin/activate"
      pip install ".[test]"
      python -m pytest -q                                   # NOT --noconftest, NOT a file list
      test "$(grep -c -- --noconftest .github/workflows/validate.yml)" -eq 0
      # AND no pytest step enumerates a subset: a named file list with no
      # --noconftest would otherwise pass the assertion above.
      python - <<'EOF'
      import re, sys, pathlib
      w = pathlib.Path(".github/workflows/validate.yml").read_text()
      body = "\n".join(l.split("#")[0] for l in w.split("\n"))
      named = set(re.findall(r'tests(?:_runtime)?/test_[A-Za-z0-9_]+\.py', body))
      sys.exit(0 if not named else (print("FAIL: workflow still enumerates", len(named), "test files"), 1)[1])
      EOF

  All three statements must succeed: `set -e` propagates a failing suite (a passing
  `grep` after a failing `pytest` must not make the sequence exit zero), and the
  `test` asserts the exclusion count is ZERO rather than leaving it to a reader.
  Today openDox-code gives 1,298 errors / 0 passed and openXdox-code 1,089 / 0.

## Group 10 — Requirement 10 / G9, G10: one entry point (openDox-code + openDox root)

- [ ] 10.1 A `[project.scripts]` entry point for the DOCUMENT surface. **The verbs
  are NOT invented here — `src/opendox/cli.py` already declares them** and group 2
  is what makes them reachable; the entry point is the missing packaging line:

      opendox = "opendox.cli:main"

  and the surface it exposes is the one already in the tree, named here so every
  falsification below is executable rather than a placeholder:

  | verb | shape, as `cli.py` declares it today |
  |---|---|
  | `generate` | `generate --repo-root <corpus> --repository <id> --output <path>` (`:880-883`) |
  | `generate-and-open` | `generate-and-open --repo-root <corpus> --repository <id> [--run-dir P] [--host H] [--port N] [--no-open] [--no-serve]` (`:885-909`) |
  | `create`, `edit` | `create --repo-root <repo> --title … --summary … --topics … --repository-context …`; `edit --repo-root <repo> <path>` (`:911`, `:927`) |
  | every generation verb | `--repo-root` AND `--repository` are REQUIRED; `--strict`, `--no-validate`, `--source-revision`, `--generated-at`, `--project-register`, `--possibles` are accepted — declared ONCE, in `_add_generate_args` (`:822-849`) |

  **Every option FOLLOWS its verb.** The parser (`build_parser`, `:852`) declares
  NO top-level option at all — `--repo-root`, `--repository` and `--strict` are
  SUBCOMMAND arguments — so `opendox --repo-root X generate …` is refused by
  argparse before any code of this product runs. An earlier draft of this table
  put them before the verb and every acceptance command below inherited that; the
  table and the commands were corrected together, against the parser itself.
  `--repository` is the snapshot's canonical repository id, and the commands pass
  `fixture`. `python -m opendox.cli` is a real entry point today:
  `cli.py:30-58` runs under `__main__` and HANDS OVER to the package copy's
  `main()` before the rest of the file executes, so the commands of Groups 5 and 7
  need no console script and no hedge.

  **There is no `serve` verb and no `validate` verb**, and this packet does not
  add either: serving is `generate-and-open`, and validation is a POST-RENDER
  step inside the generate verbs, hardened by `--strict` and skipped by
  `--no-validate`. Today the only console script is
  `opendox-runtime = "opendox.runtime.cli:main"` — a subsystem, not the product —
  and there is no `__main__.py` anywhere under `src/`. **RULED Q-R4 already places this work in THIS act** (`#656` comment
  `5701772032`, Brett Heap, 2026-09-16, recorded at `runtime/cli.py:40-46`): *"the
  verbs are wired into `opendox.cli` in the BUILD-arc act that repairs
  `opendox.serve`, and `opendox-runtime` is the spelling until then."* So 10.1
  follows group 2 and discharges Q-R4's condition.
- [ ] 10.2 The web bundle is served by that entry point and is reachable in a
  browser from an openDox-only install. openDox-code carries **42** web files,
  self-contained by declaration (`src/opendox/web/index.html`: *"All assets are
  local/vendored: no CDN, no external fonts, no remote scripts"*), and **nothing
  serves them**: `serve.py` will not import, and `runtime/app.py` mounts no
  `StaticFiles` — its routes are `/livez`, `/readyz` and `/api/v1`. The bundle is
  not the gap; the door is.
- [ ] 10.2a `intent-feed.js` stays at openxFactory under RULED OQ-F and is NOT
  owed to openDox; openDox's replacement is `views/intent-binding.js`. Do not
  count it as a missing file.
- [ ] 10.3 **The assembly root DOCUMENTS the entry point; it does not host it.**
  `openDox/Makefile` carries a row in `contracts/shape-pin.yaml` (`:49-50`), and
  `AGENTS-shape.md` § "Never edit a file that has a row" is explicit: *"An edit
  in place is reported as DRIFT and refused."* A `run`/`serve` target added there
  would red `make pins`, and the lawful route would be an upstream change in
  `opensoft/openRepoShape` binding EVERY project that carries the shape. So the
  entry point is a `[project.scripts]` console script at the CODE leg (10.1),
  which is where the shape's own "What goes where" puts *"the implementation and
  its tests"*; the root's `README.md` has no shape-pin row and is the project's
  own to edit, so it documents and points at the command.
- [ ] **FALSIFIED BY** (clean checkout of openDox-code ONLY, fresh venv, no
  sibling installed — the server is started in the BACKGROUND with a readiness
  wait so the sequence runs to completion unattended):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv .venv
      . .venv/bin/activate
      pip install .
      if python -c "import openxdox" 2>/dev/null; then echo "FAIL: sibling present"; exit 1; fi
      opendox --help >/dev/null                       # the console script MUST exist
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      R=$(mktemp -d)/plain-documents
      cp -r tests/fixtures/plain-documents "$R"   # a FRESH repository (preamble)
      git -C "$R" init -q
      git -C "$R" add -A
      git -C "$R" commit -qm fixture
      opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8080 &
      SERVER=$!
      trap 'kill "$SERVER" 2>/dev/null || true' EXIT   # cleanup cannot mask the verdict
      ready=0
      for _ in $(seq 1 30); do
        if curl -sf http://127.0.0.1:8080/ >/dev/null; then ready=1; break; fi
        sleep 1
      done
      test "$ready" -eq 1                              # a server that never started FAILS here
      curl -sf http://127.0.0.1:8080/ > "$W/bundle.html"   # no pipeline: curl's status is the status
      grep -qi '<html' "$W/bundle.html"                # and it is really the bundle

  `opendox --help` exits 0, the readiness loop must SUCCEED within 30s or `test`
  fails the sequence, and the fetched body must really be HTML — the earlier form
  of this box could pass with a server that never started, because `kill` masked
  the preceding status and `curl | head` hid a failed fetch. Today `opendox` does not exist as a
  console script, there is no `__main__.py`, and nothing serves `web/` — the
  runtime's `app.py` mounts no `StaticFiles` and declares only `/livez`,
  `/readyz` and `/api/v1`.

## Group 11 — Requirement 1: the guard holds (openxFactory)

- [ ] 11.0 **Every commit this arc lands, in EVERY repository it touches —
  openxFactory, openDox-code, openXdox-code and openDox — carries the trailer
  `Arc: neutral-product-standalone-operability`**, checked at each PR's review
  like the `Lane:` line. The falsifiers in 5.4a and 12.5 read it in
  openXdox-code, and they assert the set is NON-EMPTY there, because the arc must
  land at least 5.3a's facet in that repository. An empty set would mean the
  trailer was dropped, not that nothing was edited. That trailer is how the guard below finds THE ARC'S OWN
  commits. The alternative, diffing `main` between two commits, measures
  everything that reached `main` in between, and in a shared repository that is
  every other lane's work. Such a guard would flag unrelated landings, or, with a
  pathspec narrow enough to avoid them, miss the arc's own edits outside it.
- [ ] 11.1 At the close of the arc, a diff of openxFactory across every group
  shows: no `scripts/doc_health/` family moved, no `openspec/specs/` capability
  removed, no corpus document moved, no intent-plane schema moved, and no
  integration test moved. The only openxFactory edits are carve-manifest
  ANNOTATIONS recording each closed reach. Each is prose in the `note` that an
  `edits[]` entry already admits (`scripts/validate-carve-manifest.py:689`,
  `EDIT_KEYS`), added where there was none or extended, never rewritten, so the
  manifest's closed grammar does not widen to hold them.
- [ ] **FALSIFIED BY** (openxFactory checkout, at the close of the arc).
  **`PACKET_MERGE` is THIS PACKET'S OWN MERGE COMMIT, not a pre-authoring
  commit.** The guard measures what the ARC does to openxFactory. The packet's
  own filing artifacts are the FILING, not the arc: the `openspec/changes/`
  directory, the README bullet and the machine-seeded
  `tests/sequenced_after/corpus-ledger.yaml` row. Defining the base any earlier
  makes the command self-failing, because this packet necessarily edits the
  ledger it would then flag:

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      # THE ARC'S OWN COMMITS (11.0), not everything that reached main meanwhile:
      : "${PACKET_MERGE:?set PACKET_MERGE to the merge commit of this packet on main}"
      : "${ARC_TIP:?set ARC_TIP to the last realization commit before the archive act}"
      git log --format=%H --grep='^Arc: neutral-product-standalone-operability$' \
        "$PACKET_MERGE..$ARC_TIP" > "$W/arc-commits.txt"
      test -s "$W/arc-commits.txt"                          # 11.1's annotations exist, so an empty list measured nothing
      : > "$W/arc-changes.tsv"
      while read -r c; do                                   # WHOLE repository, no pathspec
        git rev-list --parents -n 1 "$c" > "$W/arc-parents.txt"
        if [ "$(wc -w < "$W/arc-parents.txt")" -gt 2 ]; then
          kind=MERGE                                        # only what the merge ITSELF introduced (-c), never main's content
          git diff-tree -r -c --no-commit-id --name-only "$c" > "$W/arc-one.txt"
        else
          kind=COMMIT                                       # an ordinary commit against its parent
          git diff --name-only "$c^1" "$c" > "$W/arc-one.txt"
        fi
        while read -r p; do printf '%s\t%s\t%s\n' "$kind" "$c" "$p" >> "$W/arc-changes.tsv"; done < "$W/arc-one.txt"
      done < "$W/arc-commits.txt"
      python3 - "$W/arc-changes.tsv" <<'PY'
      import copy, subprocess, sys, yaml
      MANIFEST = "docs/opendox-carve-manifest.yaml"
      def manifest_at(rev):
          out = subprocess.run(["git", "show", f"{rev}:{MANIFEST}"], check=True, capture_output=True, text=True).stdout
          return yaml.safe_load(out)
      def notes(doc):
          return [[e.get("note") for e in (row.get("edits") or [])] for row in doc["rows"]]
      def without_notes(doc):
          doc = copy.deepcopy(doc)
          for row in doc["rows"]:
              for e in row.get("edits") or []:
                  e.pop("note", None)
          return doc
      breach, annotated = [], 0
      for kind, c, p in (l.rstrip("\n").split("\t") for l in open(sys.argv[1]) if l.strip()):
          if kind == "MERGE":
              breach.append(f"{c[:12]}: a merge introduced {p} itself; land it as an ordinary commit")
          elif p != MANIFEST:
              breach.append(f"{c[:12]}: touched {p}")
          else:
              before, after = manifest_at(f"{c}^1"), manifest_at(c)
              if without_notes(before) != without_notes(after):
                  breach.append(f"{c[:12]}: changed the manifest beyond an edit's note (a row, a field, a digest)")
                  continue
              for old_row, new_row in zip(notes(before), notes(after)):
                  for old, new in zip(old_row, new_row):
                      if old != new:
                          annotated += 1
                          if old is not None and not (new or "").startswith(old):
                              breach.append(f"{c[:12]}: rewrote an existing note instead of extending it")
      if breach:
          sys.exit("FAIL: the arc changed what requirement 1 keeps:\n  " + "\n  ".join(breach))
      print(f"requirement 1 holds: {annotated} note(s) annotated, nothing else touched")
      PY

  **The guard reads CONTENT, not only names. It covers the WHOLE repository, and
  only the arc.** There is no pathspec, so a change to `README.md`, `.github/`,
  `pyproject.toml` or any other root path is seen. The commits measured are the
  ones carrying 11.0's trailer, so another lane's landing in the same window is
  not mistaken for the arc's. An ordinary commit is diffed against its parent. A
  merge is charged only with what it introduced against EVERY parent (`git
  diff-tree -c`). Merging `main` into an arc branch is therefore not charged with
  `main`'s content, and a merge that introduces a change of its own is refused,
  because an edit hidden in a merge is the one a reviewer does not read.

  Every path must be `docs/opendox-carve-manifest.yaml`, and the manifest is then
  compared by CONTENT against the commit's parent. With every `edits[].note`
  removed, the two documents must be EQUAL. No row is added, removed or
  reordered, and no disposition, destination, line list or digest moves. A note
  that already existed may only be EXTENDED, so an annotation cannot erase the
  record it annotates.

  **Nothing is exempt.** The ledger row this packet seeds landed with the filing,
  before `PACKET_MERGE`. An arc commit that touches
  `tests/sequenced_after/corpus-ledger.yaml` is therefore a breach like any other.
  So is one that touches a promoted spec: the archive act that promotes this
  capability is the FILING's bookkeeping, like this packet's own merge, and lies
  outside `ARC_TIP`.

  Every intermediate list is captured to a file first, so a failing `git` fails
  under `set -e` instead of handing the check an empty list that would read as a
  pass. The parse needs PyYAML, which `scripts/validate-carve-manifest.py` itself
  imports.

  The guard was run before this box was written, against a scratch repository
  carrying the real manifest. It passed an added note, an extended note, and a
  clean merge of `main`. It refused a rewritten note, a changed digest, a ledger
  edit, and a merge carrying an edit of its own.

## Group 12 — Requirement 11: the neutral submission step (RULED, openDox-code)

**RULED** by Brett Heap, `#656` comment `5783934499`, 2026-09-22T20:49:40Z:
*"add a neutral publish step to the build arc"*. Named **submission** in the
delta, after the fifth of the six ruled words, for the reasons in `design.md`
§ D9 — "publisher" is already taken in this capability for the repository that
publishes the corpus and the contract bundle.

The seam is NOT invented here: `src/opendox/session_pr.py:98-99` already declares
`@runtime_checkable class PullRequestPort(Protocol)` with `push`, `open_or_update`
and `find_open`, and `FakePullRequests` (`:116`) is already a second
implementation. What is missing is a NEUTRAL implementation and a default binding
that does not name a platform.

- [ ] 12.1 **SPLIT THE PROTOCOL; do not bend the platform's one.**
  `PullRequestPort`'s `open_or_update` and `find_open` return a `PullRequest`
  carrying `url`, `number` and `state`. A plain push can implement neither
  operation nor produce that record, so a neutral class that claimed to be a
  `PullRequestPort` would be lying about two-thirds of its interface. The neutral
  act therefore gets its OWN protocol: `session_pr.SubmissionPort`, a
  `@runtime_checkable` `Protocol` with ONE operation, `submit(branch) ->
  Submission`. **`PullRequestPort` is UNCHANGED**: its three operations, its
  `push(self, branch: str) -> None` (`session_pr.py:103`), and FR-030's *"three
  operations, and the absence of every other one"* (`session_pr.py:99-101`). It
  remains the governed host's platform protocol, used by `gate open-pr`, and
  `FakePullRequests` and every existing test keep their meaning.
- [ ] 12.1a **`Submission` is the report requirement 11's second scenario needs.**
  It names the DESTINATION THE WORK REACHED: `remote`, `ref`, and the remote's
  `url` as git resolves it. Scenario 2 is then asserted rather than inferred from
  a side effect, and scenario 3's refusal is distinguishable from a silent success
  by what `submit` returns, not only by its logs.
- [ ] 12.2 Ship the NEUTRAL DEFAULT **as a named class in `opendox.session_pr`,
  `LocalGitSubmissions`, implementing `SubmissionPort` and constructed exactly as
  `GhPullRequests` is — `LocalGitSubmissions(Path(checkout_root))`, one positional
  argument (`serve.py:934`).** On a plain git repository with a remote attached,
  `submit` pushes the session branch there and returns the 12.1a `Submission`. The
  runtime already models the remote — `runtime/repository_act.py:1131`'s
  `attach_remote(..., executable="git")` takes ANY git remote and writes no
  object, *"which is what makes the eventual move a push, not a migration"*.
- [ ] 12.3 With NO remote attached, say so plainly. Not an opaque failure, not a
  reported success. This is the same refusal discipline `corpus-adapter-seam`
  requires of an unresolvable corpus, applied to an unresolvable destination.
  **The refusal is a named exception, `session_pr.NoSubmissionTarget`, whose
  message names what is missing** — named here so the falsification can catch that
  type and nothing else, which is what separates "refused for the right reason"
  from "raised something".
- [ ] 12.4 **The product's OWN submission binding names no platform.** It is a
  NEW pair of bindings for `SubmissionPort`: `submission_factory` beside
  `pull_request_factory` (`serve.py:766`), and `_submission_port` beside
  `_pull_request_port` (`cli.py:800`). Each defaults, when nothing is injected, to
  `LocalGitSubmissions`. A governed host MAY contribute its own `SubmissionPort`
  through them, for example one that pushes and then opens its pull request. The
  existing `PullRequestPort` bindings keep serving the governed verb they serve
  today. `cli.py:812-814` and `serve.py:933-934` still import and construct
  `GhPullRequests`, but only openXdox's `gate open-pr` reaches them (12.4a), so
  after this box no path of the product's own names a platform. *(An earlier
  draft of this box repointed `pull_request_factory` itself. That would have
  bound a push-only class to a protocol whose other two operations it cannot
  perform.)* `serve.py:1507` records
  that an unset injection *"builds the real `GhPullRequests`"*. The unset default
  becomes the neutral implementation; `GhPullRequests` becomes ONE contributed
  implementation. **NAME THE SUBMISSION REGISTRATION POINT, and keep it SEPARATE
  from the generator's.** The submission seam ALREADY EXISTS and is
  `pull_request_factory` — `serve.py:766` declares it, `:931-932` calls it, and
  `:1505` describes it as *"the same kind of seam"* — so this box repoints its
  UNSET DEFAULT to the neutral implementation rather than inventing a seam. The
  generator seam that task 5.4 declares is a DIFFERENT interface that does not
  exist yet; the two are contributed through the same PATTERN, not through the
  same registration point, and conflating them would make neither implementable.
- [ ] 12.4a **GIVE openDox ITS OWN SUBMIT ACT — today it has none, whatever port
  is bound.** Measured at openDox-code `3c3a9e31` and openXdox-code `ab04453d`:
  the ACT of submitting is openXdox's. The CLI verb is `gate open-pr`
  (`src/openxdox/cli_gate.py:634`, `cmd_gate_open_pr`), the engine is
  `execute_open_pr` (`src/openxdox/gate_routes.py:2417`), and the route is
  `POST /actions/gate/open-pr` — all in the governance column. openDox owns the
  port (`session_pr.py`), branch sessions, and both default bindings, and NEITHER
  binding has a caller in openDox: `cli.py:800`'s `_pull_request_port` is reached
  only from openXdox's `cmd_gate_open_pr` (`cli_gate.py:674`), and
  `serve.py:911`'s `_session_pull_requests` only from the gate route. **So a
  standalone openDox cannot submit at all, `gh` or no `gh`**, and repointing a
  default (12.4) that nothing in the product calls would change nothing a
  student can reach. This box adds the neutral verb and route in openDox's OWN
  surface, not under `gate`: CLI `submit --repo-root <repo> --branch
  <session-branch>` and route `POST /actions/session/submit`. Their engine
  obtains its `SubmissionPort` through the bindings 12.4 declares, then returns
  and prints the 12.1a `Submission`. openXdox's `gate open-pr` is UNTOUCHED by this
  box; 12.5 proves it.

  **The route is a SESSION VERB, gated exactly as the governed one is.**
  Measured at openXdox-code `195276b7`: `_handle_gate_action`
  (`src/openxdox/serve_gate.py:68`) refuses, in this order and before any body
  byte is read, a request off loopback (`:73`), a request without the capability
  or a resolved actor (`:78`), and, for a session-bearing verb such as `open-pr`
  (`gate_routes.py:111`), a request that `_not_the_human_console()` (`:105`) finds
  is not the console. The submit route takes the same three clauses in the same
  order, from openDox's own `serve.py` at `1e4a57fb`. The first two are the
  `session` capability, which `compute_capabilities` grants only to a loopback
  bind with a real checkout and a RESOLVED HUMAN ACTOR (`:498`, `:504`). The third
  is the human-console test (`:1224`): the per-serve token, a trusted loopback
  `Host`, a JSON submission, and no foreign `Origin` or `Referer`. **It takes NO
  repository from the request.** It submits a branch of the checkout
  `build_server` was started on, as `gate open-pr` passes
  `checkout_root=Path(self.checkout_root)` (`serve_gate.py:158`), so no caller can
  name another checkout. The hosted plane is the multi-user one, and it carries
  no `session` capability, so the route refuses there before anything else. That
  is deliberate: a push spends the invoking user's own git credentials, and a
  personal credential is what `compute_capabilities`' own docstring says a hosted
  plane must never hold (FR-034, D22). The CLI verb runs as that user, in that
  user's checkout.
- [ ] 12.5 **THE GOVERNED FLOW IS UNCHANGED.** With the host's implementation
  registered, openxFactory's GitHub pull-request flow behaves exactly as today.
  This is a generalization, not a replacement, and 12.5 is the box that proves it.
  **Measured: nothing proves it today.** Sixteen openXdox-code test files drive
  `gate open-pr` through the registered host path or inject `FakePullRequests`
  (`git grep -l` at `ab04453d`), `test_session_verbs.py`,
  `test_session_lifecycle.py` and `test_branch_session.py` among them. **None of
  the sixteen is among the 16 test files openXdox-code's `validate.yml` runs**,
  so the governed flow has no running regression check at all. This
  box's acceptance runs them, and needs Group 9 by name, since the whole suite
  must first be runnable.
- [ ] **FALSIFIED BY** (openXdox-code checkout with the realized openDox installed
  and Group 9 landed; openXdox's registered host path, `FakePullRequests`
  injected, so no network is reached):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      : "${OPENDOX_CODE:?set OPENDOX_CODE to an openDox-code checkout at the tip of the arc}"
      python -m venv --clear "$W/v12b"
      . "$W/v12b/bin/activate"
      pip install ".[test]"
      pip install --force-reinstall --no-deps "$OPENDOX_CODE"   # the REALIZED openDox wins over any pinned one
      # the WHOLE governed set, computed: every suite that drives open-pr or injects the fake
      git grep -l -e 'open-pr' -e 'open_pr' -e 'FakePullRequests' -- 'tests/test_*.py' > "$W/governed.txt"
      test "$(wc -l < "$W/governed.txt")" -ge 16            # 16 at ab04453d; fewer means a proof vanished
      while read -r f; do python -m pytest -q "$f"; done < "$W/governed.txt"
      # ...and not by editing those proofs: no commit of THIS arc (11.0's trailer) touches them
      : "${ARC_BASE:?set ARC_BASE to the commit of this repository before the first landing of the arc here}"
      git log --format=%H --grep='^Arc: neutral-product-standalone-operability$' "$ARC_BASE..HEAD" > "$W/x-arc.txt"
      test -s "$W/x-arc.txt"                                # 11.0: the arc DID land here (5.3a at least), so empty means a dropped trailer
      : > "$W/x-paths.txt"
      while read -r c; do
        git diff --name-only "$c^1" "$c" >> "$W/x-paths.txt"
      done < "$W/x-arc.txt"
      python3 - "$W/x-paths.txt" "$W/governed.txt" <<'PY'
      import sys
      touched = {l.strip() for l in open(sys.argv[1]) if l.strip()}
      edited = sorted(touched & {l.strip() for l in open(sys.argv[2]) if l.strip()})
      if edited:
          sys.exit("FAIL: the arc edited the governed flow's own proofs: " + ", ".join(edited))
      PY

  The suites must pass AND must be unedited by the arc, because a regression
  proof the change under test may rewrite proves nothing. **The set is computed,
  not typed.** Every openXdox test file that drives `open-pr` or injects
  `FakePullRequests` is included: 16 at `ab04453d`, where an earlier draft of
  this box listed five of them. The floor of 16 catches a proof that disappears.
  Files are read from a list one per line, so the command behaves the same under
  bash and zsh, which does not word-split a variable. The measurement behind 12.5
  stands: none of the 16 is among the files openXdox's `validate.yml` runs.
- [ ] 12.6 **MERGE AUTHORITY — RULED, HOLD RELEASED.** Brett Heap, `#656` comment
  `5784155201`, 2026-09-22T21:06:01Z: *"merge yes"* — landing authority follows
  whoever governs the repository. A GOVERNED host reserves landing and routes it
  to the governance's own instrument (openxFactory's flow unchanged); a STANDALONE
  owner IS the governance and openDox may land. **Three guardrails in EVERY mode,
  none configurable:** explicit human act, conflicts SHOWN, and a merge that is a
  COMMIT and therefore revertible. Implement all three as tests, not as prose.
  *(Superseded instruction, kept so the change of direction is legible:)* An earlier draft made the absence of `merge`, `approve`,
  `review`, `self_review`, `bypass_protection` and `enable_auto_merge` binding and
  refused a merging implementation in a scenario; **both were withdrawn from the
  delta** on Brett Heap's question of 2026-09-22 — *"if we are going to have
  openDox be standalone, then it will need to merge documents."* The two readings
  were set out for the operator and the packet recommended neither; the ruling
  above answers them. The GOVERNED host's implementation still declares no merge
  and openxFactory's flow is still unchanged (12.5) — that half was never in
  question.
- [ ] 12.6a **DECLARE THE LANDING SEAM. The guardrail tests need something to
  exercise, and today nothing in openDox lands.** The submission port KEEPS its
  three operations. FR-030's *"the absence of every other one"*
  (`session_pr.py:99-101`) stays true of `PullRequestPort`, and a governed host's
  implementation still declares no merge. Landing is a SEPARATE protocol,
  `session_pr.LandingPort`, with ONE operation, `land(branch, *, confirmation) ->
  Landed`. A GOVERNANCE QUERY decides whether it is bound at all:
  `session_pr.repository_governance(checkout_root)` answers `standalone`,
  `governed` or `unknown`, and **it FAILS CLOSED**. `standalone` requires TWO
  things at once. The install must be the explicit local one
  (`OPENDOX_INSTALL_MODE=local`, 13.4). The repository must carry a COMMITTED
  declaration, `.opendox/governance.yaml` with `governance: standalone`, **read
  from the tip of the DEFAULT BRANCH at the moment of landing**
  (`git show <default-branch>:.opendox/governance.yaml`). It is never read from the
  branch being landed or from the working tree. A branch cannot decide its own
  landing: a session branch that ADDS a standalone declaration to a repository
  whose default branch has none is still `unknown` and is refused. Precedence runs
  one way. A registered host profile that declares an instrument makes the
  repository `governed` whatever any file says. The default branch's declaration
  decides only in the absence of such a host. A branch's contents never decide.
  Because the declaration is a committed file, changing it is a landing like any
  other: in a governed repository it passes through that governance. `governed`
  is what a registered host profile declares, or what the committed declaration
  says. Everything else is `unknown`: no declaration, a host profile that fails
  to load, or a declaration that disagrees with the install mode. `unknown` is
  treated as governed-without-an-instrument, so NO lander is bound and `land`
  refuses, naming what is missing. A land request under `governed` is routed to
  the host's own instrument. Under
  `standalone` the neutral lander is bound through `landing_factory`, declared
  beside `pull_request_factory` (`serve.py:766`): the same pattern with its own
  registration point, like every seam in this packet. **The three guardrails are
  the operation's CONTRACT, not its options.** `confirmation` is a CAPABILITY,
  not a value a caller builds. It is an opaque, single-use token that only two
  issuers mint. One is the `land` verb's prompt, which reads the typed branch
  name from the CONTROLLING TERMINAL (`/dev/tty`, never stdin) and refuses when
  there is none. The other is the view's confirm control, which receives a nonce
  the loopback server issued for that branch. Each token is bound to the branch
  AND its head sha, and it is spent on use. `land` verifies all of it: a token
  constructed directly, minted for another branch or another head, or presented
  twice is refused, as is a `land` whose stdin is not a terminal. **Its limit is
  stated rather than hidden.** An in-process boundary cannot stop code the user
  runs on purpose. What it stops is the PRODUCT's own paths (the fix loop,
  scheduling, automation), because none of them can reach an issuer, and a test
  asserts that no module outside the two interactive layers calls one. Packs run
  out of process (15.1b), so they cannot reach one either. A conflict raises `MergeConflict` carrying the
  conflicting paths and leaves the default branch where it was. A landing is a
  `--no-ff` MERGE COMMIT whose sha `Landed` returns, so `git revert -m 1 <sha>`
  undoes it. The CLI verb is `land --repo-root <repo> --branch
  <session-branch>`, interactive by construction.
- [ ] **FALSIFIED BY** (openDox-code checkout, no sibling, installed IN the block
  below, and `gh` NOT installed, which is the student's machine):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v12"                       # a FRESH environment: nothing already installed stands in
      . "$W/v12/bin/activate"
      pip install ".[test]"
      if command -v gh >/dev/null 2>&1; then                # the precondition, ASSERTED: the student's machine
        echo "FAIL: gh is installed; this acceptance must run without it"; exit 1
      fi
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      git init -q "$W/plain"
      git -C "$W/plain" commit -q --allow-empty -m seed
      git -C "$W/plain" branch sess-1                       # the SESSION BRANCH must exist to be pushed
      git init -q --bare "$W/remote"
      git -C "$W/plain" remote add origin "$W/remote"
      # submit through the PRODUCT'S OWN VERB (12.4a), so the REAL default binding runs:
      opendox submit --repo-root "$W/plain" --branch sess-1 > "$W/submit.out"
      git -C "$W/remote" rev-parse --verify sess-1          # the branch ARRIVED
      grep -qF -- "$W/remote" "$W/submit.out"               # and the verb REPORTED where it went (12.1a)
      # ...and the binding that verb used is the NEUTRAL one, returning a Submission:
      python3 - "$W" <<'PY'
      import sys
      from pathlib import Path
      from opendox import cli, session_pr
      W = Path(sys.argv[1])
      port = cli._submission_port(W / "plain")              # the CLI's default (12.4), no injection
      assert isinstance(port, session_pr.LocalGitSubmissions), f"the default names a platform: {type(port)}"
      assert isinstance(port, session_pr.SubmissionPort)
      assert not isinstance(port, session_pr.PullRequestPort), "a push-only class claims the platform protocol"
      r = port.submit("sess-1")                             # idempotent: already there
      assert r is not None and r.ref.endswith("sess-1") and str(W / "remote") in r.url, r
      PY
      # the SERVER's unset default binds the same class — a named test, so its absence fails:
      python -m pytest -q "tests/test_submission_default.py::test_server_unset_submission_factory_binds_the_neutral_default"
      # the ROUTE is a session verb, gated as the governed one is (12.4a) — each refusal a NAMED test:
      python -m pytest -q \
        "tests/test_submit_route.py::test_submit_route_is_refused_off_loopback" \
        "tests/test_submit_route.py::test_submit_route_is_refused_without_a_resolved_actor" \
        "tests/test_submit_route.py::test_submit_route_is_refused_without_the_console_token" \
        "tests/test_submit_route.py::test_submit_route_is_refused_from_a_foreign_origin" \
        "tests/test_submit_route.py::test_submit_route_takes_no_repository_from_the_request"
      # and the NO-REMOTE case, through the same verb (scenario 3):
      git -C "$W/plain" remote remove origin
      rc=0; opendox submit --repo-root "$W/plain" --branch sess-1 > "$W/none.out" 2>&1 || rc=$?
      test "$rc" -ne 0                                      # refused, never a reported success
      grep -qi "remote" "$W/none.out"                       # naming what is missing
      rc=0; grep -q "Traceback" "$W/none.out" || rc=$?
      test "$rc" -eq 1                                      # ABSENT: plainly refused, not an opaque error

  **The acceptance runs the product's own verb, not a class it constructs by
  hand**, so it exercises the default binding a student's install really uses.
  The CLI binding is also asserted to BE the neutral class. The server binding
  has a named test, because a hand-built class passing proves nothing about what
  the product binds when nothing is injected. On the remote path two things are
  asserted: the branch arrived, and the verb REPORTED where it went. That second
  assertion is requirement 11's second scenario, and a `None`-returning `push`
  could not satisfy it however well the push worked. The no-remote path fails in
  BOTH wrong directions scenario 3 forbids. A silent success exits 0 and fails
  `test`. An opaque error leaves a traceback, and the traceback check refuses it.
  Each of the five route tests also asserts that the remote is unchanged, so a
  refusal that pushed anyway fails.

  **And the three guardrails are asserted, now that 12.6 is RULED — by NAME**, so
  a missing test FAILS the command rather than being quietly absent from it. 12.6
  owes these thirteen tests, and pytest exits non-zero (`ERROR: not found`) for any
  node that does not exist, so today the command fails:

      python -m pytest -q \
        "tests/test_landing_guardrails.py::test_land_requires_an_explicit_human_act" \
        "tests/test_landing_guardrails.py::test_land_shows_a_conflict_and_does_not_resolve_it" \
        "tests/test_landing_guardrails.py::test_a_landed_merge_is_a_commit_that_git_revert_undoes" \
        "tests/test_landing_guardrails.py::test_no_configuration_enables_automatic_landing" \
        "tests/test_landing_guardrails.py::test_a_governed_repository_binds_no_lander" \
        "tests/test_landing_guardrails.py::test_an_unknown_governance_binds_no_lander" \
        "tests/test_landing_guardrails.py::test_a_host_profile_that_fails_to_load_binds_no_lander" \
        "tests/test_landing_guardrails.py::test_a_branch_cannot_declare_its_own_governance" \
        "tests/test_landing_guardrails.py::test_a_registered_host_outranks_any_declaration" \
        "tests/test_landing_guardrails.py::test_a_directly_constructed_confirmation_is_refused" \
        "tests/test_landing_guardrails.py::test_a_confirmation_for_another_branch_or_head_is_refused" \
        "tests/test_landing_guardrails.py::test_a_spent_confirmation_is_refused" \
        "tests/test_landing_guardrails.py::test_only_the_interactive_layers_call_an_issuer"

  Each node exercises 12.6a's seam. The first builds a `confirmation` every way
  that is not a human act (a flag, a config key, a non-TTY stdin) and expects
  every one refused. The second lands a branch that conflicts and expects
  `MergeConflict` with the paths and an unmoved default branch. The third lands,
  then reverts with `-m 1`, and expects the tree restored. The fourth walks the
  configuration surface and fails if any key can switch a guardrail off: the
  "none configurable" clause made testable. The fifth registers a governed host
  and expects NO `LandingPort` bound. The sixth and seventh prove the query FAILS
  CLOSED: with no committed declaration, or with a host profile that fails to
  load, no lander is bound. The eighth lands a branch that ADDS a standalone
  declaration to a repository whose default branch has none, and expects a
  refusal. The ninth registers a governing host beside a standalone declaration,
  and expects the host to win. The last four test the capability itself.
  A token built directly is refused. So is one minted for another branch or
  another head, and so is one presented a second time. A static check proves
  that no module outside the `land` prompt and the view's confirm route calls an
  issuer. Naming test nodes in an ACCEPTANCE command is not the defect Group 9
  removes from `validate.yml` — CI must run the whole suite, and this command runs
  thirteen named proofs in addition to it.

  Today none of this is reachable: the only implementation is `GhPullRequests`,
  which shells `["gh", "pr", ...]` (`:367`) against `_GITHUB_HOST = "github.com"`
  (`:233`), so a machine without `gh` and a repository without a GitHub remote
  have no submission path at all.


## Group 13 — Requirements 12, 13: the standalone install's shape (RULED, openDox-code)

**RULED** `#656` `5784155201`, 2026-09-22T21:06:01Z: *"bundled postgres, local
identity yes"*. `design.md` § D10 carries the measurements and the two
amendments.

- [ ] 13.1 **Bundle Postgres with the standalone install** so a user installs the
  product and not a database. The pieces exist: `pyproject.toml:134` pins
  `psycopg[binary,pool]>=3.2` and `deploy/compose/docker-compose.yaml:25` is
  already `image: postgres:16`. But `psycopg` is a CLIENT and `pip install` starts
  no container, so neither piece brings a server by itself. This box makes the
  LOCAL install bring one: with `OPENDOX_INSTALL_MODE=local` (13.4) the product
  starts a PostgreSQL SERVER shipped inside the install and supplies BOTH DSNs
  itself. **The server's IDENTITY is fixed here; its packaging is the
  realization's choice.** The data directory and the Unix socket live under the
  install's own state directory, `OPENDOX_STATE_DIR`, which defaults to a
  per-user directory the install owns. The server listens on that socket and on
  NO TCP port, so no pre-existing service can stand in for it. `runtime status`
  and the served `install` block (13.4a) report a `database_bundle` block naming
  `data_dir`, `socket_dir` and the server's `pid`. The acceptance checks the
  directories against the fresh state directory, and checks the "no TCP port"
  invariant at the OPERATING SYSTEM rather than by the bundle's own report: no
  socket the server process holds may appear in LISTEN state in
  `/proc/net/tcp` or `/proc/net/tcp6`. With `hosted` or unset, a missing
  `OPENDOX_DATABASE_URL` stays the refusal `config.py:13` already makes, so a
  hosted install can no more fall into a private local database than into local
  identity.
- [ ] 13.2 **Add no SQLite dialect**, and record the refusal where a future reader
  will look for it: a second dialect doubles every migration and every schema test
  forever, for a database that under RULING Q1 holds no document. **A non-PostgreSQL
  DSN is REFUSED by `load_settings`, and the refusal names the one dialect kept.**
- [ ] 13.3 **Keep both DSNs.** `OPENDOX_MIGRATION_DATABASE_URL` for migrating and
  `OPENDOX_DATABASE_URL` for serving, with neither defaulted from the other —
  `config.py` already names the silent fallback as the thing not to do, and a
  single-user install is not a reason to serve from the migrating credential.
  **One credential given in both settings is REFUSED by `load_settings`, naming
  `OPENDOX_MIGRATION_DATABASE_URL`.** Today `load_settings` refuses only two DSNs
  that select different schemas (`_refuse_two_dsns_that_select_different_schemas`,
  `config.py:1291`, called at `:1411`), and it reads the migration DSN as
  OPTIONAL (`:1417`), so the collapse is not refused yet.
- [ ] 13.4 **A NAMED local single-user mode (AMENDS RULING Q2).** `config.py:89-92`
  makes `OPENDOX_OIDC_ISSUER` required — *"the Keycloak broker's issuer, pinned
  … (RULING Q2)"*. Add an explicit local mode that needs no broker. **The selector
  is `OPENDOX_INSTALL_MODE`, values `local` and `hosted`, read in
  `runtime/config.py` beside `OPENDOX_OIDC_ISSUER` and defaulting to `hosted`.**
  It selects the whole install shape at once, the identity mode here and the
  datastore source in 13.1, because requirements 12 and 13 both describe "the
  standalone install" and one deliberate choice should decide both. It is named
  here so the falsification below is executable, and so the default is the SAFE
  one: an install that sets nothing is hosted, and a hosted install with no
  issuer refuses (13.5). It is UNSET, not `local`, that must be safe. **And local
  mode binds LOOPBACK ONLY.** `generate-and-open` accepts `--host` (10.1), and
  local mode has no broker, so a local install bound to `0.0.0.0` would be an
  unauthenticated multi-user service wearing the word "local". A non-loopback
  `--host` under `local` is REFUSED, naming the loopback rule, and there is NO
  opt-in: an install that must be reachable from another machine is a hosted
  install with a broker. The server already treats a loopback bind as the
  precondition of its `session` capability (`serve.py:915`); this makes the same
  judgement at the mode's own boundary. *(An earlier
  draft called it `OPENDOX_IDENTITY_MODE`. Once it also chose the datastore, that
  name described half of what it selects.)*
- [ ] 13.4a **The serving process reports its own install shape.** The entry
  point's served `/capabilities` payload (the same crossing `display_manifest`
  already publishes, `display_profile.py:670`) gains an `install` block. It holds
  `mode` and `database_bundle` (`data_dir`, `socket_dir`, `pid`), read from the
  settings THAT PROCESS loaded. Requirement 10's one entry point is what makes
  this possible: the document surface and the runtime are one served product, so
  the process a user reaches is the process whose configuration is reported. A
  status probe from a second process could be right about the settings while the
  server ignored them.
- [ ] 13.5 **A hosted install SHALL NOT fall into local mode by omission.** An
  unset issuer in a hosted install stays a REFUSAL naming the setting. This box
  is the safety of 13.4 and must land with it, not after it.
- [ ] 13.6 The hosted multi-user mode is UNCHANGED: same broker, same pinned
  issuer, a token from any other issuer still refused.
- [ ] **FALSIFIED BY** (a machine with no database and no identity broker):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      # the install is group 10's, unchanged — one entry point, one command:
      python -m venv "$W/v13"
      . "$W/v13/bin/activate"
      pip install .
      unset OPENDOX_DATABASE_URL OPENDOX_MIGRATION_DATABASE_URL OPENDOX_OIDC_ISSUER OPENDOX_INSTALL_MODE   # NONE of them set
      export OPENDOX_STATE_DIR=$(mktemp -d)                 # a state directory NOTHING else has touched
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      R=$(mktemp -d)/plain-documents
      cp -r tests/fixtures/plain-documents "$R"   # this group's OWN corpus, not Group 12's
      git -C "$R" init -q
      git -C "$R" add -A
      git -C "$R" commit -qm fixture
      opendox --help >/dev/null
      # LOCAL mode starts, with no broker and no operator-supplied database:
      OPENDOX_INSTALL_MODE=local opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8080 &
      SERVER=$!; trap 'kill "$SERVER" 2>/dev/null || true' EXIT
      ready=0; for _ in $(seq 1 30); do curl -sf http://127.0.0.1:8080/ >/dev/null && { ready=1; break; }; sleep 1; done
      test "$ready" -eq 1
      # the SERVING process reports its OWN mode and datastore, so the claim is about the server
      # the user reached on :8080 and not about a second process that read the same settings:
      curl -sf http://127.0.0.1:8080/capabilities > "$W/caps.json"
      python3 - "$W/caps.json" <<'PY'
      import json, os, sys
      inst = json.load(open(sys.argv[1])).get("install") or {}
      assert inst.get("mode") == "local", f"the server on :8080 is not in local mode: {inst}"
      state = os.path.realpath(os.environ["OPENDOX_STATE_DIR"])
      for key in ("data_dir", "socket_dir"):
          got = os.path.realpath((inst.get("database_bundle") or {}).get(key, ""))
          assert got.startswith(state + os.sep), f"the served process uses {key} {got!r}, not the bundle under {state!r}"
      PY
      # and the bundled server has NO TCP listener, checked at the OS and not by self-report:
      python3 - "$W/caps.json" <<'PY'
      import json, os, re, sys
      pid = ((json.load(open(sys.argv[1])).get("install") or {}).get("database_bundle") or {}).get("pid")
      assert isinstance(pid, int), f"the bundle reports no server pid: {pid!r}"
      inodes = set()
      for fd in os.listdir(f"/proc/{pid}/fd"):
          try:
              m = re.match(r"socket:\[(\d+)\]", os.readlink(f"/proc/{pid}/fd/{fd}"))
          except OSError:
              continue
          if m:
              inodes.add(m.group(1))
      listening = [(tbl, row.split()[1]) for tbl in ("/proc/net/tcp", "/proc/net/tcp6")
                   for row in open(tbl).read().splitlines()[1:]
                   if row.split()[3] == "0A" and row.split()[9] in inodes]   # 0A = TCP LISTEN
      assert not listening, f"the bundled server listens on TCP: {listening}"
      PY
      # ...and what it answered from is the BUNDLED datastore, migrated (requirement 12):
      OPENDOX_INSTALL_MODE=local opendox-runtime runtime status --probe-timeout 10 > "$W/status.json"
      python3 - "$W/status.json" <<'PY'
      import json, os, sys
      s = json.load(open(sys.argv[1]))
      assert s.get("database") == "reachable", f"no bundled database answered: {s}"
      assert s.get("applied_migrations") and not s.get("pending_migrations"), f"not migrated: {s}"
      state = os.path.realpath(os.environ["OPENDOX_STATE_DIR"])
      bundle = s.get("database_bundle") or {}
      for key in ("data_dir", "socket_dir"):                 # the server that answered is the INSTALL'S OWN
          got = os.path.realpath(bundle.get(key, ""))
          assert got.startswith(state + os.sep), f"{key} {got!r} is not under the install's state dir {state!r}"
      PY
      kill "$SERVER"; wait "$SERVER" 2>/dev/null || true
      # LOCAL mode REFUSES a non-loopback bind, BOUNDED, naming the rule (13.4):
      rc=0
      OPENDOX_INSTALL_MODE=local timeout 30 opendox generate-and-open --repo-root "$R" --repository fixture --no-open --host 0.0.0.0 --port 8083 >/dev/null 2>"$W/bind.err" || rc=$?
      test "$rc" -ne 0                                      # refused, never started
      test "$rc" -ne 124                                    # and not merely killed by the bound
      grep -qi "loopback" "$W/bind.err"
      # ONE DIALECT, and the two connections NOT COLLAPSED (13.2, 13.3), asked of the
      # loader directly, with every other setting well-formed so the DSN is the only fault:
      python3 - <<'PY'
      from opendox.runtime.config import ConfigurationError, load_settings
      OK = {"OPENDOX_OIDC_ISSUER": "https://issuer.example.invalid/realms/fixture",
            "OPENDOX_OIDC_AUDIENCE": "fixture"}
      def refusal(**dsns):
          try:
              load_settings({**OK, **dsns})
          except ConfigurationError as e:
              return str(e)
          raise AssertionError(f"accepted: {dsns}")
      m = refusal(OPENDOX_DATABASE_URL="sqlite:///x.db", OPENDOX_MIGRATION_DATABASE_URL="sqlite:///x.db")
      assert "postgres" in m.lower(), f"a second dialect was refused for the wrong reason: {m}"
      one = "postgresql://one@127.0.0.1/opendox"
      m = refusal(OPENDOX_DATABASE_URL=one, OPENDOX_MIGRATION_DATABASE_URL=one)
      assert "OPENDOX_MIGRATION_DATABASE_URL" in m, f"a collapsed pair was refused for the wrong reason: {m}"
      PY
      # every setting a HOSTED install needs EXCEPT the issuer, so the issuer is the only fault:
      export OPENDOX_DATABASE_URL=postgresql://serve@127.0.0.1:1/opendox OPENDOX_MIGRATION_DATABASE_URL=postgresql://migrate@127.0.0.1:1/opendox OPENDOX_OIDC_AUDIENCE=fixture
      # a HOSTED install with no issuer REFUSES — same server path, BOUNDED, naming the setting:
      rc=0; OPENDOX_INSTALL_MODE=hosted timeout 30 opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8081 >/dev/null 2>"$W/hosted.err" || rc=$?
      test "$rc" -ne 0
      test "$rc" -ne 124   # refused: neither started, nor killed by the bound
      grep -q "OPENDOX_OIDC_ISSUER" "$W/hosted.err"
      # and the DEFAULT is hosted: the same install with the selector UNSET refuses identically:
      rc=0; timeout 30 opendox generate-and-open --repo-root "$R" --repository fixture --no-open --port 8082 >/dev/null 2>"$W/default.err" || rc=$?
      test "$rc" -ne 0
      test "$rc" -ne 124
      grep -q "OPENDOX_OIDC_ISSUER" "$W/default.err"

  **Six assertions. The last four are the safety, and the last two are bounded.**
  The local probe proves the install starts with no broker and no
  operator-supplied database. `runtime status` then proves the datastore it
  answered from is the bundled one, reachable and migrated; it reports JSON with
  `database` and `pending_migrations` keys (`runtime/cli.py:621`). **The identity
  is checked, not assumed.** Its data directory and socket must both lie under a
  state directory created empty for this run, and the bundled server has no TCP
  port. So a PostgreSQL that happened to be running on the machine cannot pass
  this check in the bundle's place. The dialect
  and collapse checks go to `load_settings(env)` directly (`config.py:1391`
  takes the mapping). Every other setting is supplied well-formed, so each
  refusal must be about the DSN it names: an implementation that used SQLite, or
  served from one credential, fails here and not somewhere unrelated. The two
  negative probes take the SAME `generate-and-open` path the local probe takes,
  under `timeout 30`. A regression that silently STARTS a hosted server would
  otherwise block the command forever; with the bound it exits 124, and `test`
  rejects 124 as firmly as 0. Each probe must also NAME `OPENDOX_OIDC_ISSUER`. Both
  probes run with every setting a hosted install needs except the issuer, so the
  only difference between them is the selector, and the last probe proves the
  unset DEFAULT refuses exactly as `hosted` does.

  Today none of it is reachable. The runtime refuses without
  `OPENDOX_DATABASE_URL` and `OPENDOX_OIDC_ISSUER`, there is no local mode, and
  `load_settings` accepts a collapsed DSN pair (the migration DSN is optional
  there).

## Group 14 — Requirements 6, 14, 15: health in the store, and the fix loop (RULED, openDox-code)

**RULED** `#656` `5784155201` (*"health in db"*) and `5784247356` (*"1, add the
fix loop to #1144"*). `design.md` §§ D10.4, D10.5 and D11.

- [ ] 14.1 **The health table arrives as `0003_`, NOT `0002_`.**
  `migrations/0002_migration_state.sql` already exists (the
  `opendox_schema_migrations` ledger). `0001` is applied verbatim behind
  `CANONICAL_MIGRATION_SHA256` and its own text says *"Changing the schema is
  therefore an ADDITIVE `0002_…`/`0003_…` file, never an edit here"*.
- [ ] 14.2 **DECLARE whether the health table is a DOMAIN table or install-owned,
  and say why.** This is the boundary claim, and the closure test is scoped to
  the CANONICAL migration only — which is why `0002`'s ledger table did not trip
  it. If DOMAIN: `identity.TABLES` and
  `tests_runtime/test_schema_shape.py`'s closure text move in the SAME change. If
  install-owned: the `0002` precedent already covers it and no closure text moves.
  **Either way the choice is stated in the open**, which is what
  `test_..._exactly_rulings_six_tables`'s message demands.
- [ ] 14.3 The store holds NO DOCUMENT and stays DISPOSABLE (Q1's principle,
  untouched): results are recomputable from git, so losing the store costs a
  recomputation.
- [ ] 14.4 **The neutral families**, as ruled: broken internal links, orphans,
  near-duplicates, missing neutral front matter from the adapter's fields, a
  declared stage that disagrees with the document's location among the six ruled
  words, and stale or empty stubs. On demand from dashboard and CLI, optionally on
  commit. Baseline-relative. Model-assisted checks only where a model is
  configured. **openxFactory's 23 governance families stay put** (requirement 1).
- [ ] 14.5 **The Health view, with CLI PARITY.** Every resolution action available
  in the view is available from the command line — requirement 14's last scenario
  exists because a standalone install may have no browser. **The verbs this arc
  adds to `opendox.cli`, named here so groups 14 and 15 close on an exact
  surface** (the preamble's rule: no box closes on a verb its own group did not
  declare):

  | verb | shape |
  |---|---|
  | `health run` | `health run --repo-root <corpus> [--pack ID] [--timeout SECONDS]` |
  | `health list` | `health list --repo-root <corpus> [--json]` |
  | `health fix` | `health fix --repo-root <corpus> --finding ID [--batch]` |
  | `health accept` | `health accept --repo-root <corpus> --finding ID --reason TEXT` |

  Options FOLLOW the verb, exactly as they do for every verb `cli.py` declares
  today (10.1).

  `health list --json` emits one object per finding, with `id`,
  `resolution_class`, `path` (the document the finding is about), `severity`,
  `evidence`, `pack_id` and `pack_version`. That is the shape the acceptances in
  Groups 14 and 15 read, declared here so they read a contract and not a guess.
  They are NEW surface — `cli.py` declares none of them today (10.1's table is the
  surface that exists) — and 14.6's applier is what `health fix` invokes. **The
  view's actions are published as DATA, so parity is a comparison and not a
  promise.** The `/capabilities` payload's health block lists every resolution
  action the Health view offers. The view is served by the entry point (10.2).
  Three named tests compare the two surfaces: the view is served, every view
  action has a CLI verb, and every CLI verb is offered by the view.
- [ ] 14.6 **The three resolution classes, spelled `auto-fix`, `assisted` and
  `human-only` — exactly as RULED (`5784247356`) and exactly as requirement 14
  declares them, in the store, the CLI, the view and the pack contract (15.2)
  alike**, because a pack must return an ENGINE-declared class and two spellings
  of one class are two classes. `auto-fix` for the mechanical findings (moved link
  target, derivable front matter, stage/location mismatch), written by the
  product; `assisted` (near-duplicates, empty stubs), proposed for the human to
  edit, model-written only where a model is configured; `human-only`, evidence
  shown.
  **THE APPLIER IS NEW WORK** — openxFactory CLASSIFIES
  (`scripts/doc_health/__init__.py:17-18`, `AUTO_FIXABLE`/`CONTESTED`) and
  `grep -rln 'def apply_fix|def autofix|def fix('` over `scripts/doc_health/`
  returns nothing. Nothing in this estate applies a fix today.
- [ ] 14.7 **Every repair is a DRAFT ON A BRANCH and lands only through the
  landing rule** (requirement 11, group 12): standalone owner lands in openDox, a
  governed repository gets the governance's instrument, and in every mode the
  landing is an explicit human act with conflicts shown and a revertible commit.
  **NOTHING auto-merges, not even a one-line fix.** Batching many repairs into ONE
  draft for ONE review is the pressure valve, and is allowed.
- [ ] 14.8 **EXCEPTIONS LIVE IN GIT, NOT THE STORE**, on the pattern of
  openxFactory's `health/dispositions.yaml` — whose semantics already match:
  `scripts/doc_health/families.py:370` reads *"removing its
  health/dispositions.yaml entry re-opens"* the finding. An exception is a
  judgement that exists nowhere else; the store is disposable, so an exception
  stored there is a judgement scheduled for deletion.
- [ ] 14.9 **Ship `tests/fixtures/health-corpus`**: a small corpus carrying ONE
  finding of EVERY kind requirement 14 names, and nothing else a neutral family
  would flag, so that every assertion below is about a finding the fixture put
  there on purpose. For `auto-fix`, one of each mechanical kind: `broken-link` (a
  moved link target), `derivable-front-matter`, and `stage-location-mismatch`.
  For `assisted`, `near-duplicate`. For `human-only`, `human-only-finding`. Plus
  the one it will accept, `accepted-finding`.
- [ ] **FALSIFIED BY** (openDox-code, installed, over 14.9's fixture corpus with a
  known broken link and a known accepted finding):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v14"                       # a FRESH environment: nothing already installed stands in
      . "$W/v14/bin/activate"
      pip install ".[test]"
      export OPENDOX_INSTALL_MODE=local                     # the store is Group 13's bundle: a prerequisite by name
      export OPENDOX_STATE_DIR=$(mktemp -d)
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      C=$(mktemp -d)/health-corpus
      cp -r tests/fixtures/health-corpus "$C"   # a FRESH repository: fix branches and commits land HERE
      git -C "$C" init -q
      git -C "$C" add -A
      git -C "$C" commit -qm fixture
      opendox health run --repo-root $C
      opendox health list --repo-root $C > "$W/h1.txt"
      grep -q 'broken-link' "$W/h1.txt"
      # a mechanical repair writes a DRAFT ON A BRANCH and never the default branch:
      before=$(git -C $C rev-parse HEAD)
      opendox health list --repo-root $C --json > "$W/h1.json"
      python3 - "$W/h1.json" "$W/paths.tsv" <<'PY'
      import json, sys
      want = {"broken-link": "auto-fix", "derivable-front-matter": "auto-fix", "stage-location-mismatch": "auto-fix",
              "near-duplicate": "assisted", "human-only-finding": "human-only"}
      found = json.load(open(sys.argv[1]))
      got = {x["id"]: x["resolution_class"] for x in found}
      wrong = {k: (v, got.get(k)) for k, v in want.items() if got.get(k) != v}
      assert not wrong, f"a finding is missing or carries the wrong class: {wrong}"
      with open(sys.argv[2], "w") as out:                   # each finding's own document, for the loop below
          for x in found:
              out.write(f"{x['id']}\t{x['path']}\n")
      PY
      for f in broken-link derivable-front-matter stage-location-mismatch near-duplicate; do
        opendox health fix --repo-root $C --finding "$f"    # EVERY auto-fix kind, and the assisted proposal
        test "$(git -C $C rev-parse HEAD)" = "$before"      # default branch UNMOVED, every time
        git -C $C rev-parse --verify --quiet "refs/heads/health-fix-$f"
        git -C $C diff --name-only "$before" "health-fix-$f" > "$W/fix-$f.txt"
        test -s "$W/fix-$f.txt"                           # the branch CARRIES a change, not merely a ref
        P=$(awk -F '\t' -v id="$f" '$1 == id { print $2 }' "$W/paths.tsv")
        test -n "$P"
        grep -qxF -- "$P" "$W/fix-$f.txt"                 # and the change is to the finding's OWN document
      done
      rc=0
      opendox health fix --repo-root $C --finding human-only-finding > "$W/ho.out" 2>&1 || rc=$?
      test "$rc" -ne 0                                      # human-only: the product proposes nothing it cannot justify
      test -z "$(git -C $C branch --list 'health-fix-human-only-finding')"
      # THE EXCEPTION IS PROVED TO EXIST BEFORE THE RESET, not merely absent after:
      opendox health accept --repo-root $C --finding accepted-finding --reason "fixture"
      test -n "$(git -C $C status --porcelain -- health/dispositions.yaml)" || { echo "FAIL: accept wrote nothing to git"; exit 1; }
      git -C $C add health/dispositions.yaml
      git -C $C commit -qm "accept fixture finding"
      opendox health run --repo-root $C
      opendox health list --repo-root $C > "$W/h2.txt"
      rc=0; grep -q 'accepted-finding' "$W/h2.txt" || rc=$?
      test "$rc" -eq 1                                      # ABSENT: suppressed BEFORE the reset
      # ...and it survives the store being dropped and rebuilt:
      opendox-runtime runtime reset --confirm yes-drop-the-coordination-database
      opendox-runtime runtime migrate
      opendox health run --repo-root $C
      opendox health list --repo-root $C > "$W/h3.txt"      # a FAILING list now fails the sequence
      grep -q 'broken-link' "$W/h3.txt"                     # the run really did produce findings
      rc=0; grep -q 'accepted-finding' "$W/h3.txt" || rc=$?
      test "$rc" -eq 1                                      # ABSENT: the exception still holds
      # CLI PARITY with the view, compared rather than promised (14.5):
      python -m pytest -q \
        "tests/test_health_parity.py::test_the_health_view_is_served" \
        "tests/test_health_parity.py::test_every_view_action_has_a_cli_verb" \
        "tests/test_health_parity.py::test_every_cli_verb_is_offered_by_the_view"

  Four things are proved in order, and the order is the point: the exception is
  written TO GIT (`git status --porcelain` must show the file, NEW or modified —
  `git diff` alone misses an untracked first write and would have failed a correct
  implementation),
  it suppresses the finding BEFORE the reset, the post-reset run really produced
  findings (`broken-link` is present, so an empty listing cannot masquerade as
  suppression), and only then is `accepted-finding` asserted absent. **Every
  listing is captured to a file first and grepped second**, so a `health list`
  that exits non-zero fails under `set -e` instead of being read as the desired
  absence — which is exactly what the earlier `if … | grep -q` form would have
  done. **An ABSENCE is asserted as grep's exit status 1 exactly, never as
  `! grep`.** Under `set -e` a `!`-inverted command never stops the sequence, so
  a `! grep -q` that is not the last line passes whatever it finds, and status 2
  (a grep that could not read its file) is not an absence either. The default
  branch must not move and the draft branch must exist.

  Today none of it exists: there is no health table, no health verb, and no
  applier anywhere in the estate.


## Group 15 — Requirement 16: the check-pack interface (RULED, openDox-code)

**RULED** `#656` `5784295745`, 2026-09-22T21:16:17Z: *"1, add the pack interface
to #1144"*. `design.md` § D12.

- [ ] 15.1 Declare the NEUTRAL CHECK-PACK CONTRACT in openDox, on the
  `src/opendox/corpus_adapter.py` Protocol pattern (a `@runtime_checkable`
  Protocol with a CLOSED member set, for the reasons that file's own docstring
  gives: structural conformance lets an implementation authored elsewhere satisfy
  it without importing this product's tooling).
- [ ] 15.1a **DECLARE HOW A PACK IS FOUND AND PINNED, in one committed
  manifest.** The engine loads packs ONLY from `health/packs.yaml` in the corpus.
  It is committed beside `health/dispositions.yaml` for the same reason: which
  checks judge a corpus is a human decision about that corpus, not derived data.
  Each entry carries `id`, `version`, `source` and `digest`. The `version` is the
  one every finding the pack raises is attributed to (15.7), so a new pack
  version is a committed decision about the corpus like any other. A pack whose
  own declaration (15.2) names another version, or none, is REFUSED as a finding
  against its entry, and so is an entry whose `id` is the product's own,
  `opendox` (15.7). The digest is the source-tree
  digest `neutral-product-pin` already defines, and it is REQUIRED for every
  source. **`commit` depends on where the source lives.** A git-URL source MUST
  carry it. A corpus-relative source MUST NOT: its referent is the corpus commit
  that carries both the manifest and the source, because the two are committed
  together, so the corpus's own history pins the pack and the digest proves its
  bytes. A corpus-relative entry that DOES carry a `commit` is refused, because it
  would name a commit the corpus cannot check; copying the corpus into a fresh
  repository, as every acceptance here does, would orphan it. The engine
  verifies the pin before importing a single line of the pack. **No entry-point scanning and no import-path
  discovery**: a pack that is installed but not listed does not run. A listed pack
  whose source no longer matches its digest is REFUSED, and the refusal is a
  FINDING against that pack carrying the expected and actual digests. The pack is
  never skipped silently.
- [ ] 15.1b **RUN EVERY PACK IN AN OS-ENFORCED SANDBOX, never by convention.**
  For each run the engine exports the corpus commit into a directory it owns
  (`git archive <commit> | tar -x`). It then starts the pack inside a sandbox that
  the KERNEL enforces. `chmod -R a-w` and a working directory are not a sandbox,
  because the pack runs as the same user and can undo the first and ignore the
  second. The reference realization on Linux is `bwrap` (bubblewrap):
  `--unshare-all` (network, PID, IPC, UTS and user namespaces),
  `--die-with-parent`, `--new-session`, `--ro-bind <copy> /corpus`,
  `--ro-bind <pack> /pack`, read-only binds of only the interpreter paths the
  pack's runtime needs, a private `--tmpfs /tmp`, and nothing of `$HOME` or of
  the checkout. **The process state is cleared as well as the filesystem.** A
  namespace hides paths, but it does not hide what the pack inherits.
  `--clearenv` is followed by `--setenv` of an explicit allowlist (`PATH`,
  `LANG`, `PYTHONNOUSERSITE=1` and nothing else), so no token, DSN or credential
  in the engine's environment reaches the pack. The engine spawns the sandbox
  with `close_fds=True` and passes exactly stdin from `/dev/null` and the two
  output pipes, so no database connection, socket or open file of the engine's
  is readable through `/proc/self/fd`. The pack's only output is findings and patches on stdout, in the
  neutral shape. **The time budget is enforced on the TREE, not the process.**
  Under `--unshare-pid` the pack runs in its own PID namespace, so ending the
  sandbox's init on timeout ends every descendant the pack forked, and none
  outlives the finding that records the timeout. **Where no such sandbox exists
  on the platform, packs do not run**, and `health run` reports that as a
  finding against the install rather than running packs unsandboxed. Other
  platforms need their own kernel-enforced equivalent before packs run there.
- [ ] 15.2 A pack DECLARES its own version, which must equal its manifest entry's
  (15.1a), and its check families: id, version, and which documents each
  applies to. It RETURNS findings in the neutral shape — severity, resolution
  class (`auto-fix` / `assisted` / `human-only`, 14.6's spellings and no
  other), evidence — and MAY return proposed
  fixes AS PATCHES ONLY.
- [ ] 15.2a **THE ENGINE VALIDATES EVERY PATCH BEFORE ANY BRANCH EXISTS.** The
  sandbox (15.1b) contains the pack while it runs. It cannot contain what the
  engine does next with a returned patch, and `health fix` is the engine
  writing. So the engine checks each patch itself, as a unified diff, before
  14.6's applier touches a branch. A patch is REFUSED when any of these holds:
  it edits a path other than the `path` its own finding names (a finding that
  names no document carries no patch); it names an absolute path, a path with a
  `..` component, or a path with a `.git` component in any letter case; its
  target is a symbolic link in the corpus or lies below one; it creates,
  deletes, renames, copies or re-modes a file, or is a binary patch, which the
  engine recognizes by the headers `new file mode`, `deleted file mode`,
  `rename from`, `copy from`, `old mode` and `GIT binary patch`; or it is larger
  than the engine's bound, 65,536 bytes by default (the order of the server's own
  `_MAX_BODY_BYTES`), which is declared here and never read from the pack. Each
  refusal is a finding against the pack that proposed it, whose `evidence` names
  the refused finding (`refused_patch`) and the check it failed (`reason`), and a
  refused patch creates NO branch. Only a patch that passes every check reaches
  `git apply --check` against the draft branch's base, and a patch that applies
  is still a draft on a branch (14.7).
- [ ] 15.3 A pack's labels resolve through the DISPLAY FACET
  (`src/opendox/display_profile.py`), never spelled into the neutral surface —
  the same rule slice S7 applied to the front end, and the reason
  `NEUTRAL_DISPLAY`'s six words stay openDox's own.
- [ ] 15.4 **THE ENGINE KEEPS**, identically for every pack: the Health view and
  its CLI parity, scheduling, the baseline, storage (results in the store,
  exceptions in git), and the fix loop with its landing rule.
- [ ] 15.5 **THE REFUSALS**, each as a test and not as prose: a pack that writes,
  commits or merges (15.1b: it cannot reach the checkout, and a refusal that
  surfaces as the pack failing is a finding); a pack consumed without its pin (15.1a: commit and digest, or
  digest alone for a pack the corpus carries); a pack that
  returns a class the engine does not declare, or declares its own baseline or
  landing rule; a patch beyond its own finding's document (15.2a); and a declared
  version that disagrees with the pack's manifest entry (15.1a).
- [ ] 15.6 **A PACK THAT CRASHES OR TIMES OUT IS A FINDING AGAINST THAT PACK**,
  and the other packs still run. Give it a time budget: `health run --timeout
  SECONDS` (14.5), default declared by this box, applied PER PACK and enforced by
  the engine rather than by the caller — a pack cannot opt out of it. So is a
  pack whose output the engine cannot parse as the neutral shape: none of that
  output is stored, and the finding says why. A health
  check whose failure mode is silence is worse than one that reports itself
  broken — the doc-health nightly failed silently every night from 2026-08-30 and
  nobody saw it.
- [ ] 15.6a **SHIP `tests/fixtures/pack-corpus`**: 14.9's `health-corpus` plus
  three fixture packs under `packs/`. `fixture-crashing-pack` raises on its
  first family, `fixture-slow-pack` sleeps past any timeout, and
  `fixture-writing-pack` tries to write, commit and merge in the tree it is given,
  and lets the operating system's refusal PROPAGATE, so that the failure is
  observable and the acceptance can require it to be reported. (A pack that
  swallowed the refusal would still be contained, and 15.1b does not promise to
  see it.) Two more test the SANDBOX rather than the contract.
  `fixture-escaping-pack` tries each escape in turn. It restores write
  permission and writes, follows a symlink planted to point out of its copy,
  opens a network connection, reads `$HOME`, looks for a CANARY variable the
  engine sets in its own environment before spawning, and walks `/proc/self/fd`
  for a CANARY descriptor the engine holds open. It reports which attempts succeeded,
  and the answer must be none. `fixture-forking-pack` forks a child that sleeps
  past the budget. Three more test what a pack RETURNS.
  `fixture-garbage-pack` writes bytes that are not the neutral shape to stdout and
  exits 0. `fixture-anonymous-pack` declares no version, while its manifest entry
  names one. `fixture-patching-pack` returns six findings, each naming its own
  document and carrying a patch: `patch-ok`, a valid edit of that document, and
  one of each kind 15.2a refuses — `patch-other-document`, `patch-traversal` (a
  `..` path), `patch-git-metadata` (`.git/config`), `patch-rename` and
  `patch-oversized`. A
  `health/packs.yaml` registers all eight through 15.1a's manifest by corpus-relative
  `source`, pinned by digest and carrying NO `commit`, as 15.1a requires of a
  source the corpus itself versions. Because packs and manifest travel INSIDE the corpus,
  copying the fixture into a fresh repository carries a valid registration with
  it, and the acceptance loads the packs through the product's real path rather
  than an in-process fake. A test keeps the fixture digests current. These are
  fixtures of the engine, not shipped packs, and they exist so 15.6 and 15.1a are
  falsifiable rather than asserted.
- [ ] 15.7 **PACK ID AND PACK VERSION ON EVERY FINDING, in the SAME additive
  migration as the results table** (group 14.1 — `0003_`, since `0002_` is the
  ledger), so the table is not migrated twice. **The ENGINE stamps both, and the
  pack is not asked.** `pack_id` and `pack_version` are the manifest entry's that
  launched the run (15.1a), never values read from the findings the pack
  returns, so a pack cannot attribute its findings to another pack, and a
  refusal raised before a pack ever runs still carries its entry's id and
  version. Both columns are `NOT NULL` in `0003_`, so no path can store a
  finding without them: requirement 16's provenance scenario, enforced at the
  store and not only in the engine. **The product's own checks are the one pack
  no manifest lists.** A finding a neutral family (14.4) raises carries
  `pack_id` `opendox`, the distribution name `pyproject.toml` declares, and
  `pack_version` the installed version,
  `importlib.metadata.version("opendox")`. 15.1a refuses a manifest entry whose
  `id` is `opendox`, so no pack can pass as the product.
- [ ] **FALSIFIED BY** (openDox-code, installed, over 15.6a's `pack-corpus`, whose
  manifest registers its eight fixture packs beside the neutral checks):

      set -euo pipefail
      W=$(mktemp -d)                                        # scratch space, resolved at run time (never a host path)
      python -m venv --clear "$W/v15"                       # a FRESH environment: nothing already installed stands in
      . "$W/v15/bin/activate"
      pip install ".[test]"
      export OPENDOX_INSTALL_MODE=local                     # the store is Group 13's bundle: a prerequisite by name
      export OPENDOX_STATE_DIR=$(mktemp -d)
      export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid
      C=$(mktemp -d)/pack-corpus
      cp -r tests/fixtures/pack-corpus "$C"   # packs + manifest travel inside
      git -C "$C" init -q
      git -C "$C" add -A
      git -C "$C" commit -qm fixture
      FIXTURE_HEAD=$(git -C "$C" rev-parse HEAD)
      # the eight fixture packs of 15.6a are registered; the run is itself bounded,
      # so a hang is a FAILED FALSIFICATION and never a hung falsifier:
      timeout 120 opendox health run --repo-root $C --timeout 5
      # the WRITING pack reached only its isolated copy (15.1b): the user's tree is untouched
      test -z "$(git -C "$C" status --porcelain)"           # nothing in the checkout moved
      test "$(git -C "$C" rev-parse HEAD)" = "$FIXTURE_HEAD" # and no commit landed on it
      # the FORKING pack left no descendant past its budget: the sandbox ended the whole tree
      test "$(ps -eo args | grep -c '[f]ixture-forking-pack' || true)" -eq 0
      # the neutral checks still produced findings despite a crashing pack:
      opendox health list --repo-root $C > "$W/p1.txt"
      grep -q 'broken-link' "$W/p1.txt"
      # and EVERY pack that misbehaves in the run is itself a finding, attributed:
      opendox health list --repo-root $C --json > "$W/p1.json"
      python3 - "$W/p1.json" <<'PY'
      import json, sys
      f = json.load(open(sys.argv[1]))
      ids = {x['pack_id'] for x in f}
      assert 'fixture-crashing-pack' in ids, 'crashing pack not reported'
      assert 'fixture-slow-pack' in ids, 'timed-out pack not reported'
      assert 'fixture-writing-pack' in ids, "a writing pack's failed write was not reported (it lets the refusal propagate)"
      assert 'fixture-garbage-pack' in ids, 'unparseable pack output was not reported'
      assert 'fixture-anonymous-pack' in ids, 'a pack declaring no version was not refused as a finding'
      escaped = [x for x in f if x['pack_id'] == 'fixture-escaping-pack' and x.get('evidence', {}).get('succeeded')]
      assert not escaped, f"a pack got out of its sandbox: {escaped}"
      assert all(x.get('pack_id') and x.get('pack_version') for x in f), 'a finding has no provenance'
      builtin = {x['pack_id'] for x in f if x['id'] == 'broken-link'}
      assert builtin == {'opendox'}, f"a built-in finding is not attributed to the product itself: {builtin}"
      print('packs attributed:', sorted(ids))
      PY
      # what a pack RETURNS is checked before any branch exists (15.2a):
      for f in patch-other-document patch-traversal patch-git-metadata patch-rename patch-oversized; do
        rc=0
        opendox health fix --repo-root "$C" --finding "$f" > "$W/pf.out" 2>&1 || rc=$?
        test "$rc" -ne 0                                    # refused...
        test -z "$(git -C "$C" branch --list "health-fix-$f")"   # ...and no branch exists for it
      done
      opendox health fix --repo-root "$C" --finding patch-ok
      git -C "$C" rev-parse --verify --quiet refs/heads/health-fix-patch-ok   # the valid patch IS a draft
      test "$(git -C "$C" rev-parse HEAD)" = "$FIXTURE_HEAD" # and the default branch never moved
      opendox health list --repo-root "$C" --json > "$W/p1b.json"
      python3 - "$W/p1b.json" <<'PY'
      import json, sys
      f = json.load(open(sys.argv[1]))
      refused = {x['evidence'].get('refused_patch') for x in f
                 if x['pack_id'] == 'fixture-patching-pack' and isinstance(x.get('evidence'), dict)}
      want = {'patch-other-document', 'patch-traversal', 'patch-git-metadata', 'patch-rename', 'patch-oversized'}
      assert want <= refused, f'a refused patch is not a finding against its pack: {sorted(want - refused)}'
      assert 'patch-ok' not in refused, 'the valid patch was refused'
      PY
      # a pack whose source no longer matches its PIN is refused, AS A FINDING (15.1a):
      echo "# tampered after pinning" >> "$C/packs/fixture-slow-pack/__init__.py"
      git -C "$C" commit -qam "tamper with a pinned pack"
      timeout 120 opendox health run --repo-root $C --timeout 5
      opendox health list --repo-root $C --json > "$W/p2.json"
      python3 - "$W/p2.json" <<'PY'
      import json, sys
      f = json.load(open(sys.argv[1]))
      hit = [x for x in f if x['pack_id'] == 'fixture-slow-pack' and 'digest' in json.dumps(x.get('evidence', '')).lower()]
      assert hit, 'a tampered pack ran, or was skipped silently, instead of being refused as a finding'
      assert all(x.get('pack_id') and x.get('pack_version') for x in f), 'a refusal has no provenance'
      PY
      # and 15.5's REFUSALS, each a NAMED test — a missing node fails the command:
      python -m pytest -q \
        "tests/test_check_packs.py::test_a_pack_that_writes_reaches_only_its_isolated_copy" \
        "tests/test_check_packs.py::test_a_pack_cannot_restore_write_permission_on_its_copy" \
        "tests/test_check_packs.py::test_a_pack_cannot_follow_a_symlink_out_of_its_copy" \
        "tests/test_check_packs.py::test_a_pack_has_no_network" \
        "tests/test_check_packs.py::test_a_pack_cannot_read_the_users_home" \
        "tests/test_check_packs.py::test_a_pack_sees_no_inherited_environment" \
        "tests/test_check_packs.py::test_a_pack_inherits_no_open_descriptor" \
        "tests/test_check_packs.py::test_no_descendant_of_a_pack_outlives_its_budget" \
        "tests/test_check_packs.py::test_no_sandbox_on_the_platform_means_no_packs_run" \
        "tests/test_check_packs.py::test_an_unpinned_pack_is_refused" \
        "tests/test_check_packs.py::test_a_pack_returning_an_undeclared_class_is_refused" \
        "tests/test_check_packs.py::test_a_pack_declaring_its_own_baseline_or_landing_rule_is_refused" \
        "tests/test_check_packs.py::test_unparseable_pack_output_is_a_finding_against_the_pack" \
        "tests/test_check_packs.py::test_a_declared_version_that_disagrees_with_the_manifest_is_refused" \
        "tests/test_check_packs.py::test_provenance_is_stamped_from_the_manifest_not_the_pack" \
        "tests/test_check_packs.py::test_the_store_refuses_a_finding_without_provenance" \
        "tests/test_check_packs.py::test_a_builtin_finding_carries_the_products_own_id_and_version" \
        "tests/test_check_packs.py::test_a_manifest_entry_claiming_the_products_id_is_refused" \
        "tests/test_check_packs.py::test_a_patch_may_edit_only_its_own_findings_document" \
        "tests/test_check_packs.py::test_a_patch_outside_the_corpus_or_into_repository_metadata_is_refused" \
        "tests/test_check_packs.py::test_a_patch_through_a_symlink_is_refused" \
        "tests/test_check_packs.py::test_a_patch_that_creates_deletes_renames_or_remodes_is_refused" \
        "tests/test_check_packs.py::test_a_patch_over_the_size_bound_is_refused" \
        "tests/test_check_packs.py::test_a_refused_patch_creates_no_branch"

  Every finding carries a pack id and version, the refusals and the product's
  own findings included (a neutral `broken-link` is attributed to `opendox`
  itself). **Every
  pack that misbehaves in the run** — crashing, slow, writing, unparseable and
  unversioned — appears as a finding, rather than as a stack trace, a hang, or an
  edit to the user's tree, and the run completes. Each of the five refused patches
  leaves no branch and a finding that names it, and the one valid patch is a draft
  on a branch while the default branch stays at the fixture's own commit. The
  writing pack is checked where it runs: straight after the run, the checkout
  must be clean and still at the fixture's own commit. An in-process pack would already have moved it. The
  outer `timeout 120` is the difference between a falsifier that FAILS on a
  runaway pack and one that HANGS on it: without it, the very defect 15.6 exists
  to prevent would take the acceptance command down with it, and the box would
  look unfinished rather than failed. The JSON is captured to a file and read by
  `sys.argv[1]`, because a heredoc and a stdin redirect cannot both feed the same
  interpreter and the heredoc wins.

  Today none of this exists: there is no pack contract, no health run, and no
  findings store.

## Follow-ons named here and NOT authored here

- [~] F1 **Port openxFactory's 23 governance families into the openXdox pack.**
  An openXdox FOLLOW-ON with its own claim. Until it lands, requirement 1 keeps
  those families with openxFactory. **Owner: whoever claims it on `#656`.**
- [~] F2 **Each DomainxFactory's own pack**, pinned in that domain's `stack.yaml`.
  That domain's own work. **Owner: each domain.**
