# Realization evidence — adopt-configured-notebook-hosting-identity

Packet task 6.4. Filed for the archive gate (`release-realization` requires
merged-plus-green evidence for a non-empty code surface).

**THIS FILE IS INCOMPLETE BY DESIGN AND THE BOX IT SERVES IS NOT TICKED.** Task
6.4 asks for four things and this branch can supply three: the sweep output, the
resolver test names and the pytest pin deltas are below; **the `--resolved`
green line is task 5.2's and belongs to the operator**, so the box stays open
rather than being ticked on four fifths of its content. Where it lands is the
one gap in this file.

## 1. The address sweep (task 4.5)

```console
$ git grep -nE '<the four addresses>' -- tests/ examples/ scripts/ openspec/specs/
openspec/specs/lifecycle-notebook-projection/spec.md:459: … the promoted identity bullet …
```

**One line, and over the whole tree the same one line and nothing else.**
Thirty-nine of the forty are gone. The survivor is the promoted spec's identity
bullet, which packet task 1.1 reserves for the archive act and forbids editing
by hand — measured, not assumed: this repository's promoted specs are written by
the ARCHIVE commit (`openspec/specs/lifecycle-notebook-projection/spec.md`'s own
last substantive writer is `4290cad2 Archive add-notebook-projection-identity`).
So the sweep is empty in every file this feature is permitted to touch, and
**FR-015 completes at the archive act**, not here.

The four addresses are not restated in this file, in any commit on this branch,
in either pull-request body, or in any test name or comment — which is the same
constraint that stopped the packet's own delta using the reserved
`Removed from canon by` marker.

## 2. Behaviour preservation (task 2.5), proven by equality

The pre-change module was loaded from `origin/main` alongside the post-change
one and both were pointed at the SAME still-committed record:

```console
keys read by the OLD constant path: ['account', 'account_type', 'case', 'domain',
    'migration_from_account', 'migration_from_nlm_profile', 'migration_state',
    'nlm_profile']
env  (workspace-relative) identical: True
env  (absolute)           identical: True
workspace config          identical: True
nothing configured -> UNDECLARED: True
```

Values elided; the comparison is dict equality, so eliding them costs the proof
nothing.

## 3. The twenty-four new tests

`tests/notebooklm/test_sync_notebooklm_books.py` —
`TheDeclarationsPathResolvesFromConfigurationTests` (11):

```text
test_the_env_var_resolves_the_declaration
test_a_workspace_relative_env_var_resolves_from_the_root
test_the_workspace_configuration_resolves_the_declaration
test_the_env_var_wins_over_the_workspace_configuration
test_absent_configuration_is_undeclared_and_does_not_break
test_a_configured_path_that_does_not_exist_is_undeclared
test_a_configured_path_resolving_to_the_shipped_example_is_refused
test_the_marker_is_read_from_the_record_not_from_the_path
test_the_shipped_example_is_not_the_last_resort
test_a_record_marked_live_binds                      (3 subtests)
test_an_empty_environment_value_is_unset
```

`tests/notebooklm/test_validate_hosting.py` —
`TheResolvedDeclarationIsValidatedTests` (9) and
`TheResolutionOrderIsOneOrderTests` (4):

```text
test_a_resolved_declaration_is_validated
test_a_resolved_declaration_that_does_not_conform_still_fails
test_the_workspace_configuration_resolves_the_declaration
test_the_env_var_wins_over_the_workspace_configuration
test_absent_configuration_resolves_to_nothing
test_resolved_refuses_rather_than_falling_back_to_the_fixture
test_resolved_refuses_a_record_marked_as_an_example
test_the_marker_does_not_make_an_otherwise_conforming_record_invalid
test_an_explicit_path_still_wins_over_everything
test_both_readers_name_the_same_environment_variable
test_both_readers_name_the_same_configuration_file
test_both_readers_agree_on_the_example_marker
test_both_readers_resolve_the_same_three_cases_the_same_way
```

One test is RENAMED and not added: `test_the_committed_record_conforms` ->
`test_the_committed_example_conforms`, keeping its assertion and changing its
subject. Together with `test_a_resolved_declaration_is_validated` and the
operator's `--resolved` step, those are the three things replacing the one check
the split costs (design § 3.4).

## 4. Validator green lines

```console
$ python3 scripts/validate-notebook-projection-hosting.py
validate-notebook-projection-hosting: 0 error(s) over …/examples/notebook-projection-hosting.yaml (the shipped fixture)

$ python3 scripts/validate-notebook-projection-hosting.py <the live record in its private home>
validate-notebook-projection-hosting: 0 error(s) over … (the path given)
```

The second line was taken against the record as placed by
xFactory-Hermes-Install PR #73 (path elided here; it is named in that pull
request). **It is not task 5.2's line** — 5.2 wants `--resolved`, run by the
operator against his own configuration, which is what proves the CONFIGURATION
as well as the record.

## 5. The record moved intact (task 5.1, OQ-E)

Structural comparison of the record in its new private home against the
openxFactory file at `e7c53012`:

```console
hosting block identical apart from the marker: True
approval block identical: True
share_out rows: 7 identical: True
denied rows: 1 identical: True
custody carried: True
```

And the synthetic instance against that live record:

```console
same keys in the same order: True
roster arity: 7 vs 7 | denied: 1 vs 1
markers: example / live
```

## 6. Suite and check movement, against a baseline taken on this branch's base

| check | baseline (`e7c53012`) | this branch | movement |
| --- | --- | --- | --- |
| `openspec validate --all --strict` | 100 passed, 1 failed | 100 passed, 1 failed | **none.** The failure is `disposition-codexfactory-declared-renames` in both, a deltaless disposition packet unrelated to this work |
| `pytest tests/notebooklm tests/doc-health tests/sequenced_after -q` | 1997 passed, 37 subtests | **2021 passed, 40 subtests** | +24 tests, +3 subtests, 0 failures, **0 skipped added** |
| `pytest tests/notebooklm -q --collect-only` | 227 | **251** | +24 |
| `scripts/doc-health.py --single-repo .` | 10 critical, 9 error, 55 warning, 16 info | **10 critical, 9 error, 55 warning, 16 info** | **none.** "New regressions vs previous report: 0" |
| `scripts/validate-sequenced-after.py .` | passed | **passed (41 active changes, 7 declaring the field)** | none |
| `release-inventory-drift` | 2 info (editorial members between cuts) | 2 info, same two paths | **none.** No inventoried blob moves; the record is deliberately not a `contracts/` member |

**The doc-health `info` population did not move**, which is the number the
packet asked to be watched: its own carriage-ledger row was added by PR #783
(its landing, not its realization), and this feature adds no MODIFIED block and
retires none, so the ledger's `==` comparison is untouched.

## 7. The pytest pins did not move, and that is the correct outcome

`.github/workflows/pytest-suite.yml` is **not touched**. `EXPECT_SKIPPED: "21"`
is exact and no test is added skipped. `MIN_SELECTED: "7090"` and `MIN_PASSED:
"7070"` are floors, and that file's own comment settles what a change like this
owes: *"(MIN_SELECTED and MIN_PASSED are FLOORS and need no edit: the new module
only raises the actuals, which widens the printed margin.)"* It pins its numbers
to a named CI run precisely because a developer worktree measures a different
SKIPPED, so raising a floor to a locally measured number is what that file
refuses. Packet task 4.4 can be read as asking for a raise; this is why it did
not happen, recorded rather than skipped silently.

## 8. What this feature did NOT do, and where it lands

| owed | where |
| --- | --- |
| The delta reaching canon (Group 1) | the ARCHIVE act. Task 1.1 says "by the archive act, never by hand", and this repository's promotion history agrees. |
| The live record's move, the workspace configuration, the `--resolved` proof, the flip gate (Group 5) | Brett Heap, in a private repository, on his own word. Prepared as xFactory-Hermes-Install PR #73 and NOT ticked. |
| `README.md`'s Records entry moving to archived state (6.3) | the archive act. The entry's *state* was corrected on this branch — it still read `Status: draft` and "five open questions, none answered", both false since PR #783 — but the archived-state move is 6.3's. |
| The sweep ledger's `--moved-by` write (6.5) | the merge or the archive; it needs a pull-request number this branch does not have. Run read-only here and clean. |
| The archive gate itself (6.6) | after this branch merges green on `main`. |
