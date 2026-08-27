# Research: the modified-block-currency regression-fixture catalogue (F2)

**Phase 0 output.** Every question this feature could have carried as
`[NEEDS CLARIFICATION]` was resolved by reading the packet, the ratified
delta, F1's landed code and tests, or by MEASURING. Nothing below is a
preference; each item names what settled it.

The spec carries zero clarification markers because of this phase. Where a
reading is a choice rather than a finding, it is an orchestrator decision in
`plan.md` and is flagged for veto there.

---

## R1 — Both histories are recoverable, and both were recovered

**The question.** Packet § 3.1 and § 3.2 ask for two historical instances.
§ 3.2 hedges — "reconstruct from `add-release-inventory-drift-check`'s reverted
first archive attempt if recoverable, else synthesize faithfully and say so".
Orchestrator decision 2 makes reconstruction the default and synthesis the
labelled fallback. So: is either history actually in git?

**Finding: BOTH ARE, and neither needs synthesizing.**

### #351 — `add-doxchat-model-intake`

| fact | value |
| --- | --- |
| issue | #351 |
| repair commit | `f68261f775eb74455a16f7d4d67b576fd76618f0` ("The intake delta restates current canon, so archiving it no longer reverts six clauses (#351)") |
| merge commit | `87d0b95ae2970733f273cbac15beb847a5b562c5` (PR #358) |
| **the pre-repair state** | `bcfc26a0d2f182c652ed9054b82210ccbee8124a` — `f68261f7^` |
| capability | `ideation-dashboard` |
| requirement | `doxBench model catalog and provider boundary` |

The repair commit touched exactly two files —
`openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md`
and that change's `tasks.md`. **It did not touch canon**, so
`openspec/specs/ideation-dashboard/spec.md` reads identically at `bcfc26a0`
and at `f68261f7`, and the canon side of the fixture can be taken from either.
Taking it at `bcfc26a0` keeps one commit for the whole fixture.

Recovery:

```
git show bcfc26a0:openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md
git show bcfc26a0:openspec/specs/ideation-dashboard/spec.md
```

Shapes at `bcfc26a0`: canon's requirement carries **7** scenario titles; the
block carries **6**, five of canon's plus its own
`The intake affordance is submitted as a model`. The two canon titles the block
does not carry are `The menu offers a routing rule` and
`A fourth provider verb is proposed` — **exactly** the two § 3.1 names.

### #329 — `add-release-inventory-drift-check`

| fact | value |
| --- | --- |
| issue | #329 |
| archive commit | `38b548d46153e5e39c855aa105aa77cbb550894a` ("Archive add-release-inventory-drift-check: the drift gate is canon") |
| merge commit | `b03b9992d519dbfab78fa63a00c5c6e2413ae0e0` (PR #331) |
| **the pre-archive state** | `d5f447e89cf619fd12113bcf03525468ece4470d` — `38b548d4^` |
| capability | `doc-health` |
| requirement | `Deterministic check families` |

§ 3.2 called this a "reverted first archive attempt". **It was not a revert.**
The packet's own delta says the truncation was "caught by the byte-for-byte
promotion verification at archive time, before anything was committed", and
that is what the history shows: the truncated block lived in the ACTIVE change
directory from `e06b066b` (draft) through `57c26e1a` (PR #319) and was
rewritten scenario-complete inside the archive commit `38b548d4` itself. So
the recoverable state is the parent of the archive, not a reverted commit —
and the fixture is byte-faithful all the same. The audit and the fixture
provenance note both say this, because "reverted first archive attempt" is the
phrase a later reader will search for and not find.

Recovery:

```
git show d5f447e8:openspec/changes/add-release-inventory-drift-check/specs/doc-health/spec.md
git show d5f447e8:openspec/specs/doc-health/spec.md
```

Shapes at `d5f447e8` — the #329 claim, verified rather than assumed:

- canon's `Deterministic check families` carries **8** scenario titles
- the block's `## MODIFIED Requirements` restates **1** of them
  (`A run executes the check families`)
- the change's own `## ADDED Requirements` (`Release-inventory drift`) brings
  **7**
- so the delta FILE carries **8** `#### Scenario:` lines and canon's
  requirement carries **8**. **The file-level count is flat.** That is § 3.2's
  whole point, and it is real rather than constructed.

---

## R2 — What the family actually says about each reconstruction

Measured before the spec was written, by building both trees in a scratch
directory and calling `fam_modified_block_currency` on a `Context` shaped like
`conftest.make_ctx`'s. **Neither tree is committed by this phase**; these are
the acceptance figures the tasks will assert.

### Fixture A (#351) — 2 findings

| arm | outcome |
| --- | --- |
| scenario-title (`warning`) | one finding, naming `The menu offers a routing rule` and `A fourth provider verb is proposed`, and naming `openspec/specs/ideation-dashboard/spec.md` |
| carriage ledger (`info`) | one finding for the requirement, listing **11** uncarried units of canon's 25 — 3 `body`, 8 `scenario-bullet` |
| title resolution / ordering | none |
| marker defects | none |

The 11 ledger units, by kind:

- **body** — canon's sentence carrying the three-member port surface AND
  "MUST NOT be added as a fourth provider verb"
- **body** — canon's sentence carrying the `auto` routing-rule clause
- **body** — canon's sentence carrying the credential clause, `thread file`
  in the leak list, and the broker-lane clause
- **bullet** — `**THEN** the selector MUST show exactly the available catalog
  entries and their data-handling badges`  ← the containment instance
- **bullet** ×3 — the three bullets of `The menu offers a routing rule`
- **bullet** — `**AND** every loaded editor MUST remain usable`  ← the
  REVERTED scenario line § 3.1 names
- **bullet** ×2 — the two bullets of `A fourth provider verb is proposed`
- **bullet** — `**WHEN** doxBench runs on the hosted plane`  ← the
  "hosted plane" → "hosted/read-only plane" drift the repair commit records

### Fixture B (#329) — 2 findings

| arm | outcome |
| --- | --- |
| scenario-title (`warning`) | one finding naming all **7** omitted titles |
| carriage ledger (`info`) | one finding listing **17** uncarried units of canon's 28 — 2 `body`, 15 `scenario-bullet` |
| title resolution / ordering | none |
| marker defects | none |

The two body units are canon's enumeration sentence ("seventeen check
families…") and its "Four of the seventeen…" sentence — the same two-sentence
shape the packet's own § 2.1 block draws against itself (§ 6.6). That is a
coincidence of form, not of content, and the fixture is not evidence about
§ 2.1.

---

## R3 — The human's clause count is not the family's unit count

**The question.** § 3.1's ACCEPTANCE says "the ledger lists the six clauses".
The measurement lists **three** body units. Is the family wrong, or is § 3.1
counting differently?

**Finding: § 3.1 is quoting the REPAIR COMMIT's prose, which enumerates six
CLAUSES; the normative derivation's body granularity is the SENTENCE.** The
repair commit names: the three-member port-surface enumeration; "MUST NOT be
added as a fourth provider verb"; the `auto` routing-rule clause; the
broker-lane credential clause; and `thread file` in the credential-leak list.
Those five (the sixth being the reverted scenario line, which is a bullet, not
a body clause) lie inside three of canon's sentences: clauses 1 and 2 in one
sentence, clause 3 in a second, clauses 4 and 5 in a third.

The delta writes the derivation as normative — "every other paragraph SHALL be
split into sentences at a period, question mark or exclamation mark followed by
whitespace or the end of the paragraph" — so three units is the CORRECT
reading, not a defect. **This is why orchestrator decision 3 exists**: an
assertion on "six ledger rows" would have been wrong, and an assertion on the
six clauses' TEXT inside the reported units is right and is what the tasks
write.

Alternatives rejected: splitting canon's sentences at semicolons or em dashes
to make six units (would rewrite the ratified derivation, and F2 adds no
behaviour); asserting six rows and calling the difference a defect (the delta
says otherwise on its face).

---

## R4 — The rendered ledger truncates, so assertions split in two

**The question.** Can a test assert `thread file` against the ledger finding's
`rule` string?

**Finding: NO.** `modified_block_currency._QUOTE_WIDTH` is 140 and `_quote`
truncates each unit to it with an ellipsis. Canon's credential sentence is far
longer than 140 characters and `thread file` sits past the cut, so it is
absent from the rendered string by design — the arm renders a readable list,
not the corpus.

Consequence for every § 3.1 and § 3.2 assertion, and the reason this is a
research item rather than a task note:

- assertions on **full clause text** run against the units the comparison
  returns (`mbc.carried(basis.units, block.units)` — the same call the arm
  makes), naming `(kind, text)` pairs
- assertions on the **rendered finding** run against its quoted PREFIXES, the
  arm's own wording, the requirement title, and the promoted spec path

A test that asserted a late clause against the rendered rule would fail for a
reason unrelated to the rule under test, and a later session would "fix" it by
widening `_QUOTE_WIDTH` — a behaviour change F2 is forbidden.

---

## R5 — A reconstructed fixture freezes the REQUIREMENT, not the file

**The question.** "Byte-faithful" — to what?

**Finding: to the requirement.** `openspec/specs/ideation-dashboard/spec.md` is
279 KB at `bcfc26a0` and carries dozens of requirements this feature says
nothing about; `openspec/specs/doc-health/spec.md` is comparable. The family
reads per requirement (`promoted()` returns a dict keyed by normalized title),
so copying whole files would freeze unrelated canon into the test suite, make
every later canon edit look like a fixture concern, and add ~300 KB of test
data for no assertion.

The fixture therefore carries the requirement section VERBATIM — from
`### Requirement: <title>` to the line before the next `### Requirement:` —
inside a minimal spec file whose only added lines are a
`# <capability> Specification` heading, a short `## Purpose`, and
`## Requirements`. The delta side is copied WHOLE, because a delta file is
small and its `## ADDED Requirements` section is load-bearing for § 3.2's flat
count.

The provenance note records the scope of the verbatim guarantee. This mirrors
`test_promotion_fidelity.py`, whose module docstring says its fixture
"reconstructs the SHAPE … and says so"; F2 reconstructs the TEXT and says
that too.

---

## R6 — Where to record provenance

**The question.** Orchestrator decision 2 says "the commit SHAs recorded in the
fixture's README". No fixture in `tests/doc-health/fixtures/` carries a README
today.

**Finding: add one per new tree, and keep the module-docstring habit too.**
The precedent for provenance in this suite is
`test_promotion_fidelity.py`'s module docstring; the precedent for a
per-fixture note is nowhere. The decision introduces the file, and it is the
right home for a `git show` invocation a reader can paste. A test docstring
cannot be pasted.

Verified safe: `corpus.EXCLUDED_PARTS` contains `tests`, and
`corpus.GOVERNED_ROOTS` is `("contracts", "docs", "examples", "ideation",
"templates")`, so a `README.md` under `tests/doc-health/fixtures/` is outside
the governed corpus AND outside the lifecycle scan set. It needs no `Status:`
header and draws no `status-validity`, `location-conformance` or `doc-catalog`
finding. Checked because adding an ungoverned Markdown file to a repository
whose own health checker reads Markdown files is exactly the kind of move that
reds a gate nobody predicted.

---

## R7 — One tree per case, never an addition to an existing tree

**Finding.** `conftest.make_ctx(family)` loads EVERY repository directory under
`fixtures/<family>/` into one `Context`. Adding a repository or a change to an
existing tree therefore changes what every existing test over that tree sees —
F1's `_run()`, `_markers_run()`, `_res_run()` and `_tw_run()` all assert over
whole-tree results, several of them with `== []`.

So each new case is its own directory. Tree names, one per gapped item:

| tree | § 3 item | repo dir |
| --- | --- | --- |
| `modified-block-currency-history-351` | 3.1 | `intakeFactory` |
| `modified-block-currency-history-329` | 3.2 | `driftFactory` |
| `modified-block-currency-merge-gut` | 3.3 | `mergeFactory` |
| `modified-block-currency-tokens` | 3.5 | `tokenFactory` |
| `modified-block-currency-rewrap` | 3.6 | `rewrapFactory` |
| `modified-block-currency-fence` | 3.7(d) | `fenceFactory` |

Repository directory names are distinct from F1's `alphaFactory` /
`betaFactory` / `quietFactory` / `emptyFactory` / `gammaFactory` so that a
finding's `repo` field identifies its tree in any failure message.

---

## R8 — What F1 already covers: the audit, and how it was taken

**Method.** Not from F1's plan or hand-off prose — from the landed file.
`tests/doc-health/test_modified_block_currency.py` was read in full, its 97
test functions enumerated, and each packet § 3 clause matched against the test
bodies and fixture text that discharge it. Where § 3 phrases an obligation
more narrowly or more widely than the test asserts it, the difference is the
gap.

**Result: 11 of 18 rows fully satisfied, 7 gapped in whole or in part** — 18
rows because § 3.7's eleven obligations need five of them. The
audit is `contracts/coverage-audit.md` and is the single home for the mapping;
nothing else in this feature restates it.

The seven rows that are not fully satisfied, and what is missing from each:

| item | what F1 has | what § 3 asks that F1 does not do |
| --- | --- | --- |
| **3.1** | the SHAPE, in synthesized text, sharing one fixture with 3.2 | the REAL text at byte fidelity, from git |
| **3.2** | the SHAPE, including the flat-count pin, in the same synthesized fixture | the REAL text at byte fidelity, from git |
| **3.3** | a `Merged into` case whose merged source has ONE bullet, carried, so both arms are quiet | a `Merged into` marker over a FOUR-bullet scenario with TWO dropped → ledger reports them; and the companion that names them in a `Removed from canon` marker → quiet |
| **3.4** | `test_a_block_unit_containing_canon_s_unit_does_not_carry_it`, widening at the END only, at `carried()` level | widening "at either end" — before, and both ends; and the mechanism exercised THROUGH the family, which fixture A now does with real text |
| **3.5** | 2 tokens (`.openspec.yaml`, `openxFactory`), a TWO-sentence note, and the note DROPPED | `contract-v1.45` and `promotion_fidelity.py` as well; a note of THREE OR MORE sentences; and the note EDITED IN ITS THIRD SENTENCE reporting once |
| **3.7(d)** | `test_a_unit_containing_backticks_is_extracted_whole_under_a_longer_fence`, at `extract_code_spans` level | the longer fence exercised END TO END through the family, suppressing a whole unit |
| **3.6** | `test_a_scenario_complete_block_that_rewraps_every_paragraph_is_quiet`, asserting at `carried()` on units built in the test body; the `-quiet` tree carries NO MODIFIED block | a fixture tree whose MODIFIED block IS scenario-complete and re-wrapped, run through the family, returning `[]` and not skipped |

Two rows are satisfied and deserve their own note because § 3 invites a
duplicate:

- **3.11** — `test_the_three_launch_severities_are_named_apart` and
  `test_the_family_is_absent_from_family_resolution_at_launch` pin both halves
  exactly as § 3.11 asks. F1's hand-off says so in as many words: "§ 3.11 has
  nothing left to add and should say so rather than write a second copy."
- **3.12** — `test_a_scope_with_no_changes_directory_skips_with_its_reason` and
  `test_a_scope_with_active_changes_but_no_modified_block_is_not_skipped` match
  § 3.12 clause for clause, including the "cannot run, not found nothing"
  distinction.

---

## R9 — § 3.13 determinism: satisfied as phrased, extended anyway

**Finding.** § 3.13 asks for "two runs over ONE fixture tree". F1's
`test_two_runs_agree_byte_for_byte` runs the two-writers tree twice and
compares `__dict__`s, and
`test_the_family_returns_its_findings_sorted_severity_first` checks ordering
over THREE trees. The item is satisfied on its face.

F2 extends it to every tree, including the six new ones (FR-020), not because
§ 3.13 requires it but because a new fixture is exactly where nondeterminism
would enter — dict iteration over a freshly-parsed document, or a sort key that
ties. This is recorded as an EXTENSION in the audit row rather than as a gap,
so nobody later reads the row as F1 having left something undone.

---

## R10 — F1's spec and F1's hand-off disagree, and the hand-off wins

**The conflict.** F1's `spec.md` § Out of Scope assigns to F2 "the exhaustive
regression-fixture catalogue of packet § 3 …, the tokenization fixture, the
full marker matrix, the determinism pin and the structural launch pins". F1's
`tasks.md` § Hand-off says the opposite for three of those: "What F2 must NOT
duplicate. F1 already carries, with tests: the structural launch pin in BOTH
halves …; the full marker matrix …; the containment negative; the tokenization
invariant; determinism; and the skip/quiet pair."

**Resolution: the hand-off.** It is the later statement — written after F1's
implementation review, which is what discovered that F1's tests had grown to
cover the catalogue — and it is the reading consistent with orchestrator
decision 4 (minimal scope, no second copies). The audit records the
disagreement on the affected rows so the next reader does not re-litigate it,
and the tasks follow the hand-off: no duplicate launch pin, no duplicate skip
pair, no second marker matrix.

Note also that the hand-off is not fully right either: it lists "the
tokenization invariant" and "the full marker matrix" as done, and § 3.5 and
§ 3.7(d) show both are done in a NARROWER form than § 3 phrases. The audit is
taken from the test file, not from either document, which is why it catches
this.

---

## R11 — Suite evidence, and the one command that must not be run

**Finding.** `python3 -m pytest tests/doc-health -q` from this worktree reads
**1077 passed, 4 warnings** at `19e3f6b5` + the specify commit. That is the
baseline every task counts from.

The whole-tree `pytest tests` is NOT run from a worktree: parts of that suite
require a live Postgres this worktree has no access to, and a red result there
would say nothing about this feature. Orchestrator decision 5. `openspec
validate --all --strict` is the second gate and this feature changes no
`openspec/` path, so its count must be unchanged.
