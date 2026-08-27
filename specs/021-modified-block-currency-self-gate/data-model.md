# Data Model: The modified-block-currency self-gate

The gate adds no persistent data. It manipulates four values, and naming them is
worth the page because three of the four mutation-round mutants are attacks on
one of them.

---

## 1. `RepositoryUnderTest`

The checkout the gate measures. **Not** a parameter a caller chooses; a value the
gate derives and then proves.

| field | value | how it is established |
| --- | --- | --- |
| `root` | absolute path | `Path(__file__).resolve().parents[2]` |
| `changes_dir` | `<root>/openspec/changes` | MUST be a directory |
| `canon_spec` | `<root>/openspec/specs/doc-health/spec.md` | MUST be a file |
| `toplevel` | `git -C <root> rev-parse --show-toplevel` | MUST equal `root` |

**Validation rules**

- Resolution starts and ends at the test file's own tree. There is **no ancestor
  walk**: a base missing either marker fails with a message naming both markers
  and the path searched. This is `harden-ideation-readiness-check`'s first
  resolution rung and its failure mode, with this family's markers.
- `toplevel == root` is the assertion that kills "point the resolver at another
  checkout". Another worktree of the same repository has a different toplevel;
  the aggregation checkout has a different toplevel; a subdirectory resolves to
  the tree above it and fails.
- The gate takes an optional `under_test` argument used **only** by the resolver's
  own negative test. No corpus assertion passes it.

**State transitions**: none. The value is computed once per test and never
mutated.

---

## 2. `NamedSubject`

The identity of a finding as a reader states it. The unit of assertion in this
feature, and the answer to the packet's § 4.1 anti-vacuity rule.

Two shapes, because the two arms make different claims:

| shape | fields | asserted as |
| --- | --- | --- |
| **scenario-arm subject** | `(change, capability, requirement_title, omitted_scenario_title)` | exactly one, by all four fields |
| **ledger subject** | `(change, capability, requirement_title)` | an exact SET of nine |

**Derivation from a `Finding`.** A `Finding` carries `severity`, `repo`, `path`
and `rule`. The `change` and `capability` are read off `path`
(`openspec/changes/<change>/specs/<capability>/spec.md`) using the family's own
`DELTA_GLOB` shape, and the `requirement_title` and any quoted unit are read out
of `rule` by the quoting the family itself applies (`'…'` around a title). No
second parser: the gate reads what the family wrote.

**Validation rules**

- The ledger set is compared with `==`, not `<=`. A subset comparison would let a
  newly lossy MODIFIED block land unreported, which is the defect the family
  exists to catch — asserted loosely, in the one place the assertion is about
  this repository.
- The scenario-arm subject is asserted *together with* `len(warnings) == 1`. The
  count alone is vacuous; the subject alone would pass beside a second unnoticed
  warning.
- Every comparison of a title is on the exact string. Canon's title is
  `Gate verbs hide on a composed view`; the rename destination is
  `Tile-bound gate verbs hide on a composed view`. A containment test would pass
  on the wrong one of those two, which is the family's own forbidden-containment
  rule applied to its gate.

---

## 3. `DiscoveryFloor`

The population of active MODIFIED blocks the family found, asserted **without
reference to any finding**.

| field | value at `76a2ad27` | assertion |
| --- | --- | --- |
| `blocks` | 22 | `len(blocks) >= 1` |
| `changes` | 12 | reported in the failure message |
| `capabilities` | 13 | reported in the failure message |

**Why a floor and not the number.** The corpus's MODIFIED-block count is nobody's
invariant — it moves on every proposal and every archive. F1's
`test_the_real_notes_this_corpus_carries_are_each_one_unit` records the cost of
getting this wrong: an exact pin "broke the moment `add-family-enumeration-check`
archived", making an unrelated archive look like this family's regression. The
floor's job is only to make an **empty read** impossible to pass, and `>= 1` does
that completely.

**Independence rule**: this value is asserted in its own test, which mentions no
severity, no change id and no requirement title. That independence is what makes
mutant M1 (remove the named-subject assertion) fail rather than pass.

---

## 4. `ReportMovement`

The per-severity difference between two renderings of this checkout differing
only by `--skip-family modified-block-currency`.

| field | value at `76a2ad27` | assertion |
| --- | --- | --- |
| `critical` | 0 | `== 0` |
| `error` | 0 | `== 0` |
| `warning` | +1 | `== len(family warnings)` |
| `info` | +9 | `== len(family infos)` |
| changed-line classes | 4 | every changed line falls in one of them |

**The four permitted line classes** (R7): the headline line; the
skipped-family notice; the `### modified-block-currency` section; the ranked-plan
rows whose `family=` is this family.

**Validation rules**

- `warning` and `info` movements are compared **against the family's own finding
  counts from the same tree**, never against literals. That is what makes this
  "the one count assertion" rather than a hard-coded total: the numbers 1 and 9
  appear nowhere in the assertion.
- `critical` and `error` are compared to zero, which IS a literal — and is the
  right one, because "this change does not move the failing bands" is the claim,
  not a measurement.
- Both runs are taken in the same test invocation, so `--as-of` defaults agree by
  construction.
- Neither run reads any tree but `RepositoryUnderTest.root`. The before-state is
  **this tree with the family skipped**, never another worktree's `main`.
