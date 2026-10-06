# Tasks: realize-doc-health-direction-arc

Status: draft
Authored: 2026-10-06, lane `openxfactory-4`, as plan 038's T070.

Each group names the plan 038 task it mirrors (`specs/038-opendox-document-tool-self-maintenance/tasks.md`).
The single-writer orders and `After:` lines there govern; this list adds the
falsifiers this change answers to.

**Trailers.** Every REALIZATION landing of this change carries
`Arc: realize-doc-health-direction-arc` and its lane's `Lane:` line, in every
repository it lands in (ARC-4): 2.1; 2.2 only where the arc brings its own pin
commits; group 3; 4.1 and 4.2; and 4.4. A 2.2 that rides plan 038's T062 and
T063 rides #1144's realization landings, which carry #1144's trailer and never
this change's, so #1144's own guards still find them. Bookkeeping carries no
`Arc:` trailer: this
filing (1.1), the ratification (1.2), evidence, #1144's edit (5.2), the
aggregation's pin-sync (4.5) and the archive (group 7). No commit message or
PR body carries a closing keyword.

**No realization step starts before 1.2.**

## 1. Filing and ratification (plan 038 T070, T071)

- [ ] 1.1 **File this packet.** `proposal.md`, `design.md`, `tasks.md` and
  `.openspec.yaml` (`skip_specs: true`; origin `kind: staged`, drafting
  provenance, no approval pair); the README *Active changes* bullet; the
  machine-seeded row in `tests/sequenced_after/corpus-ledger.yaml`. Landed
  under a Rule 6 window.
  - **Falsifier:** `python3 scripts/validate-openspec-cli-pin.py --all --strict`
    exits 0 with no undispositioned finding;
    `python3 scripts/validate-sequenced-after.py . --ledger-diff` exits 0;
    `python3 scripts/proposal-support.py . verify realize-doc-health-direction-arc`
    exits 0.
- [ ] 1.2 **Brett Heap's ratify word, and its record.** Put the change to
  Brett. Record his word verbatim on `#656` and in
  `review/ratification-<date>.md` (`Status: record`). Flip the three lifecycle
  documents to `Status: ratified` with ONE citation line each, and ADD
  `approved_by` and `approved_on` to the origin beside the drafting provenance.
  `kind`, `id`, `path`, `proposed_by` and `proposed_on` do not move. The word
  rules `design.md` § 11's D1–D7 as recommended unless it says otherwise; a different
  answer is encoded before 2.1 starts. Landed under a Rule 6 window.
  - **Falsifier:** as 1.1, plus the `proposal-origin` family reporting nothing
    for this change.

## 2. openDox-code: the generic slice (plan 038 T072)

- [ ] 2.1 **Re-author the generic slice.** ONE new standard-library module
  carrying `split_keepends`, `join_rows` and `head_sha` (`design.md` § 3),
  with its tests. Nothing is relocated out of openxFactory.
  - **Falsifier:** the module's own tests, including the round trip
    `join_rows(split_keepends(t)) == t` over CR, LF, CRLF, no final newline,
    mixed endings, form feed and U+2028; openDox-code's whole suite as its
    required `validate` job runs it, green.
- [ ] 2.2 **Its pin (ARC-6).** If 2.1 lands before plan 038's T061, it rides
  T062's root pin and T063's `opendox @` pin, which are #1144's landings under
  #1144's trailer, and this step is a note in the evidence. Otherwise the arc
  brings its own, under this change's trailer: the openDox root's `code`
  gitlink and `contracts/code-pin.yaml` in ONE commit, then openXdox-code's
  `pyproject.toml` `opendox @` to the same commit. T061 never waits for 2.1.
  - **Falsifier:** `make pins` in the openDox root; openXdox-code's install
    resolves the pinned commit (F9.2's `direct_url.json` check).

## 3. openXdox-code: the seams, the retargets, the respellings (plan 038 T074)

After 1.2, 2.2, plan 038's T021 and T073 (the single-writer order on
`tests/conftest.py`, `gate_console.py`, `tests/declared_exclusion.yaml` and the
workflows).

- [ ] 3.1 **Declare the four seams** S1–S4 (`design.md` § 4.1), each with a
  registration call, a call that answers whether it holds one, and a call
  that empties it.
  - **Falsifier:** tests that a seam takes one registration, refuses a
    different second one, treats the same one again as a no-op, and that a
    read from an EMPTY seam raises an error naming the seam (D3).
- [ ] 3.2 **Retarget the eight modules.** `completeness.py`, `round_trip.py`
  and `generator.py`'s generic half import 2.1's module; every governed name
  is read through its seam at USE. The three module-level values computed
  from `doc_health` today (`generator.py:77`, `gate_console.py:76`,
  `corpus_root.py:43`) become use-time reads (D2).
- [ ] 3.3 **Respell the 7 test files** that import `doc_health` directly
  (`design.md` § 6), each import to one of its three homes. None is
  protected.
- [ ] 3.4 **The contribution modules** (`design.md` § 10).
  `column_contributions.py` keys openXdox's four governed columns as D4 rules;
  `tests/test_column_contributions.py` pins the new reason;
  `projection_contributions.py`'s docstring states the new cause.
- [ ] 3.5 **The surface and the declaration.** `DOC_HEALTH_SURFACE` in
  `tests/test_dependency_direction.py` falls to empty. The `doc_health` reason
  leaves `tests/declared_exclusion.yaml`: each of its 60 files is measured at
  this step's base and either leaves the declaration (it collects and passes
  alone) or stays as a declared composed integration test under the reason
  T073 gives such files. The PR quotes the count each way.
  `tests/test_declared_exclusion.py`'s `open_until` values follow.
- [ ] 3.6 **F9.2's two code removals** (`design.md` § 7). The help-tree
  node's `--deselect` (`LEFT_OUT`) leaves the workflow that carries it at this
  step's base (`validate.yml:161-164` at `56e1c238`), and the guard test
  `test_the_help_tree_is_left_out_only_while_its_stated_reason_holds` leaves
  with it.
- [ ] 3.7 **The interim registration** (ADV-19). Until 4.1 lands, the
  composed conftest registers openxFactory's governed implementations from the
  composed tree's `scripts/`, so the 12.5 suites never meet an empty seam.
  - **Falsifier for group 3**, in an openXdox-code checkout at the PR's head:

        set -euo pipefail
        W=$(mktemp -d)                                    # scratch space, resolved at run time
        rc=0; git grep -nE '^\s*(from doc_health|import doc_health)' HEAD -- src/ > "$W/reach.txt" || rc=$?
        test "$rc" -eq 1                                  # 1: no module under src/ imports doc_health; 0: a reach remains; >1: git failed
        python -m venv --clear "$W/lone" && . "$W/lone/bin/activate"
        pip install ".[test]"                             # openDox through the pin, no openxFactory anywhere
        python -c "import openxdox.cli_gate, openxdox.completeness, openxdox.corpus_root, openxdox.gate_console, openxdox.gate_routes, openxdox.generator, openxdox.round_trip, openxdox.snapshot_registry"
        python -m pytest -q tests/test_dependency_direction.py
        python -m pytest -q "tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_32_entry_tree_the_manifest_records"

    Then the composed workflow green at the head, and the protected-suite
    oracle over this change's openXdox-code landings (4.3, second command),
    exit 0.

## 4. openxFactory: the host fills the seams, with its pin pairs (plan 038 T075)

After group 3 and plan 038's T064.

- [ ] 4.1 **Register the governed implementations.** `scripts/opendox_host.py`
  adds the four seams to `seams()` with their `_TAKE_BACK` rows, as their own
  all-or-none group (D7), filled before the host's
  `column_contributions.register()` call. A host-wiring test under
  `tests/domain_profile/` registers them, reads each through openXdox, and
  shows a refusal part-way taking every written seam back.
- [ ] 4.2 **The pin pairs, in two repositories, in order** (`design.md` § 9,
  steps 5 and 6). Both are realization landings.
  1. **An opensoft/openXdox (root) PR, landed first:** its `code` gitlink and
     `contracts/code-pin.yaml` to group 3's openXdox-code commit. Its
     `contracts/opendox-pin.yaml` moves only if 2.2 brought the arc's own
     openDox root commit; a 2.2 that rode T062 is already pinned there by
     plan 038's T064.
  2. **Then ONE openxFactory PR carrying 4.1:** openxFactory's `openXdox`
     gitlink with `contracts/openxdox-pin.yaml`, naming the root commit of
     step 1, and the `openDox` gitlink with `contracts/opendox-pin.yaml` if
     2.2 brought the arc's own, one commit per pair. Host registration and pin
     move land together, so openxFactory's `main` never runs an openXdox whose
     seams it does not fill.
  - **Falsifier:** `make pins` in the openXdox root;
    `python3 scripts/verify-openxdox-pin.py` and
    `python3 scripts/verify-opendox-pin.py` in openxFactory; the host-wiring
    test; every required check of openxFactory green.
- [ ] 4.3 **The surfaces check over this change's own landings** (ARC-4;
  ADV-37; `design.md` § 8). Quoted in 4.1's PR and again at 7.1.
  In an openxFactory checkout:

      set -euo pipefail
      W=$(mktemp -d)
      : "${CHANGE_MERGE:?set CHANGE_MERGE to the merge commit of this change's filing on main}"
      : "${ARC_TIP:?set ARC_TIP to the last realization landing measured}"
      git log --first-parent --format=%H --grep='^Arc: realize-doc-health-direction-arc$' \
        "$CHANGE_MERGE..$ARC_TIP" > "$W/arc-commits.txt"
      test -s "$W/arc-commits.txt"                        # 4.1 lands here, so an empty list measured nothing
      : > "$W/arc-changes.tsv"
      while read -r c; do                                 # each landing against main before it, whole repository
        git diff --no-renames --name-status "$c^1" "$c" > "$W/arc-one.txt"
        while IFS=$'\t' read -r s p; do printf '%s\t%s\t%s\n' "$c" "$s" "$p" >> "$W/arc-changes.tsv"; done < "$W/arc-one.txt"
      done < "$W/arc-commits.txt"
      python3 - "$W/arc-changes.tsv" <<'PY'
      import copy, subprocess, sys, yaml
      MANIFEST = "docs/opendox-carve-manifest.yaml"
      HOST = {"scripts/opendox_host.py", "scripts/profile_openxfactory.py"}
      HOST_TESTS = "tests/domain_profile/"
      PIN_PAIRS = {"openDox", "contracts/opendox-pin.yaml",
                   "openXdox", "contracts/openxdox-pin.yaml"}
      COMPOSITION_TESTS = set()      # D5: #1144's named list is not inherited; grows only by a ruling
      ADMITTED_ARC_EDITS = set()     # D5: likewise
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
      for c, s, p in (l.rstrip("\n").split("\t") for l in open(sys.argv[1]) if l.strip()):
          if s not in ("A", "M"):
              breach.append(f"{c[:12]}: {'deleted' if s == 'D' else 'changed the type of'} {p}")
          elif p in HOST or p.startswith(HOST_TESTS) or p in PIN_PAIRS or p in COMPOSITION_TESTS or p in ADMITTED_ARC_EDITS:
              continue
          elif p != MANIFEST:
              breach.append(f"{c[:12]}: touched {p}")
          else:
              before, after = manifest_at(f"{c}^1"), manifest_at(c)
              if without_notes(before) != without_notes(after):
                  breach.append(f"{c[:12]}: changed the manifest beyond an edit's note")
                  continue
              for old_row, new_row in zip(notes(before), notes(after)):
                  for old, new in zip(old_row, new_row):
                      if old != new:
                          annotated += 1
                          if old is not None and not (new or "").startswith(old):
                              breach.append(f"{c[:12]}: rewrote an existing note instead of extending it")
      if breach:
          sys.exit("FAIL: the arc changed what requirement 1 keeps:\n  " + "\n  ".join(breach))
      print(f"requirement 1 holds: {annotated} note(s) annotated, every other path a declared surface (11.1)")
      PY

  And in an openXdox-code checkout, the protected-suite oracle over this
  change's landings there (`design.md` § 8):

      set -euo pipefail
      W=$(mktemp -d)
      git log --first-parent --format=%H --grep='^Arc: realize-doc-health-direction-arc$' HEAD > "$W/x-arc.txt"
      test -s "$W/x-arc.txt"                              # group 3 lands here
      printf 'tests/test_%s.py\n' branch_session doxbench_mutation_boundary doxbench_share gate_loop_views \
        gateway_provenance hosted_actor session_commits session_confinement session_gates session_lifecycle \
        session_notebook session_records session_runbook session_transaction session_verbs staging_workbench \
        > "$W/governed.txt"                               # 12.5's 16 protected suites
      ls tests/test_generator.py tests/test_snapshot*.py tests/test_session_snapshot.py > "$W/gen-suites.txt"
      python3 scripts/protected_suites.py --landings="$(cat "$W/x-arc.txt")" --suites="$(cat "$W/governed.txt")"
      python3 scripts/protected_suites.py --chains --landings="$(cat "$W/x-arc.txt")" --suites="$(cat "$W/gen-suites.txt")"

  - **Falsifier:** the first prints `requirement 1 holds`; both oracle calls
    exit 0.
- [ ] 4.4 **The composed pin advances** (an openXdox-code PR, and a
  REALIZATION landing: it removes 3.7's interim registration, so it carries
  this change's `Arc:` trailer). After 4.2 lands,
  `tests/composed_host_pin.yaml` advances to openxFactory's new commit, and
  3.7's interim registration leaves in the same PR. Plan 038's T073 re-runs
  after it, as #1144's work.
  - **Falsifier:** the composed workflow green at that PR's head, with no
    registration left in the composed conftest that the host now makes.
- [ ] 4.5 **The aggregation's routine pin-sync** (bookkeeping, no `Arc:`).
  `opensoft/xFactory` moves its `openxFactory` gitlink with
  `.github/clearing/openxfactory/PIN.yaml`, and keeps its root `openXdox` (and
  `openDox`, if 2.2 moved it) gitlink equal to openxFactory's nested gitlink
  and to the matching `contracts/*-pin.yaml` `commit:`, in ONE commit (that
  repository's `CLAUDE.md`, working rule 2).
  - **Falsifier:** `python3 -m pytest tests/ -q` in the aggregation with
    `openxFactory` initialized, quoted.

## 5. F9.2 (plan 038 T076; ARC-5 (a))

- [ ] 5.1 **Re-run F9.2** after groups 3 and 4, as #1144's `tasks.md` states
  it, and quote it in `evidence/f9.2-run.md` (`Status: record`).
  - **Falsifier:** F9.2 exits 0.
- [ ] 5.2 **Close it where it lives.** If #1144 is still ACTIVE: remove
  batch J's `--deselect` from F9.1's realized pytest line and tick F9.2 in
  #1144's `tasks.md`, under a Rule 6 window (bookkeeping, no `Arc:`). If
  #1144 has ARCHIVED: its archived `tasks.md` is never edited, and 5.1's
  evidence is the closure (ADV-20).

## 6. The trailer census (ARC-4)

- [ ] 6.1 **Every realization landing names this change.** In each
  repository the arc landed in, `git log --first-parent --grep='^Arc:
  realize-doc-health-direction-arc$'` lists the landings, and the list is
  NON-EMPTY in openDox-code (2.1, whichever pin it later rides),
  openXdox-code (group 3 and 4.4), the openXdox root (4.2 step 1) and
  openxFactory (4.1 with 4.2 step 2). Where 2.2 brought the arc's own pins, it
  is NON-EMPTY in the openDox root too, and openXdox-code's list also holds
  2.2's `opendox @` pin commit. Recorded in
  `evidence/landings.md` (`Status: record`), per repository.

## 7. Archive, and the staged topic's exit (plan 038 T077)

- [ ] 7.1 **The surfaces check at the close.** 4.3's two commands, with
  `ARC_TIP` the last realization landing before the archive act, quoted in
  the archive PR.
- [ ] 7.2 **Realization evidence** (`release-realization`'s archive gate):
  each repository's landings merged through its required checks, and a green
  run at `ARC_TIP` of openXdox-code's composed workflow, openDox-code's
  `validate` job and openxFactory's `pytest-suite`, cited by run.
- [ ] 7.3 **Exit the staged topic through this change.** Move
  `ideation/staging/doc-health-direction-arc/` into this change's
  `supporting-docs/` with `scripts/proposal-support.py transition`, whose
  support manifest repeats this packet's origin (`kind`, `id`, `path`)
  exactly, and update the topic's row in `ideation/staging/INDEX.md` to
  record the exit.
- [ ] 7.4 **Archive.** `scripts/proposal-support.py archive` (the UTC date
  rule), under a Rule 6 window, landed by MERGE COMMIT and never squash, so
  the archive directory's date holds. The ledger row flips to `archived` in
  the same PR (`validate-sequenced-after.py . --seed-ledger`).
  - **Falsifier:** `python3 scripts/validate-openspec-cli-pin.py --all --strict`
    exit 0; `python3 scripts/validate-sequenced-after.py .` exit 0; the
    archive gate's origin retention passes.
