# F4 — modified-block currency: reporting and workflow

Speckit feature `022-modified-block-currency-reporting`, realizing
`openspec/changes/add-modified-block-currency-check` **§ 5 (5.1–5.3)**. The
**last of four**: F1 `19e3f6b5` (the family), F2 `76a2ad27` (fixtures), F3
`f728d57f` (the self-gate).

**This PR does not archive the change.** § 8 is a separate later act and F4 is
its precondition; the three numbers § 8.1 gates on are recorded in
`specs/022-modified-block-currency-reporting/evidence/f4-gates.md` § 7.

## What landed

**§ 5.1 — the arms are visible without counting.** The family's report section
now states its four finding classes with their counts and bands, under its own
heading, before its rows:

```text
### modified-block-currency

Finding classes, counted apart so the gate-bearing arm is never read as one of the editorial rows:
- scenario-title completeness: 1 (`warning` — the arm carrying this family's gate)
- carriage ledger: 8 (`info` — editorial, and the arm says so in every finding)
- title resolution and ordering: 0 (`warning`)
- marker defects: 0 (`info`)

- [warning] …add-composed-view-authoring… omits 1 of the 2 scenarios …
- [info] …
```

**§ 5.2 — the action line is pinned.** Every finding of the three comparison
arms carries, verbatim, "restate the requirement as canon currently states it, or
declare the deletion with a `Removed from canon by` marker", on the finding and
in the rendered ranked plan.

**§ 5.3 — the workflow boundary is pinned, with no workflow change.** No step's
`run`, `env` or `with` names this family in either spelling; the CLI exposes no
option named after it; the generic `--family` / `--skip-family` still accept its
id. `.github/` and `openspec/` have an EMPTY diff.

## Decision R1 — FLAGGED FOR VETO

The subtotal reaches the report through a **new registry
`families.FAMILY_SUMMARIES`**, keyed by family id exactly like the existing
`FAMILY_NOTES`, whose value takes THAT family's findings and returns note lines;
`report.render` renders them in the position `FAMILY_NOTES` already renders in.

- **Why a sibling registry, not a widening of `FAMILY_NOTES`**: that one is
  `(ctx) -> lines` and answers a question about the RUN (which tree promotion
  fidelity measured). This is `(findings) -> lines` and answers a question about
  the FINDINGS. Widening the first would have changed `basis_notes`' contract
  for no gain.
- **Why in `report.render` and not the runner**: the tally is a function of the
  findings the renderer is about to print, it becomes testable in-process
  without a subprocess, and `report.py` is in the feature's stated scope.
- **Why not arm-prefixed rule text** (the alternative the brief listed second):
  it changes rule text, which F3's self-gate pins by subject; it moves every
  ranked-plan row, so the report diff would leave the family's own lines; and it
  does not satisfy § 5.1 — a reader would still tally nine long rows.
- **Reverting** is a clean deletion: four lines in `families.py`, a five-line
  branch in `report.render`, one class and three functions in
  `modified_block_currency.py`. No finding, no severity, no other family.

Full argument and ten more decisions: `specs/022-…/research.md`.

## Two imprecisions in § 5, recorded rather than worked around

1. **§ 5.2 reads as if the action line were F4's to add. It is not** — F1 landed
   it as `_ACTION`, verbatim § 5.2's wording. Read as "add", § 5.2 is a no-op;
   read as "pin", it is a real deliverable, and F4 implements the pin.
2. **§ 5.2 says "the action line"; the family has two.** The marker-defect class
   carries `_MARKER_ACTION`, because the remedy for a defective declaration is
   not the remedy for an uncarried unit. The split is F1's and is correct; the
   singular is the imprecision.

## The mutation round found three survivals; the combined review found two of them

`evidence/f4-gates.md` § 3. Ten mutants, seven killed on the first run.

- **M4 (leak one blank line into every family's section) SURVIVED 26 green
  tests.** The byte-identity test was purely differential — registry-on vs
  registry-off over one finding set — and a mutant that moves both sides equally
  is invisible to it. Fixed by stating the before-state absolutely: another
  family's whole section, and its whole ranked-plan rows with `action="…"`,
  asserted byte-for-byte. M4 re-run: killed.
- **M2 (change another family's action line) SURVIVED, and cannot be killed from
  here.** The brief predicted it would red the byte-identity test; by
  construction it cannot, for M4's reason. **And no test in this repository pins
  any other family's action text at all** — `promotion_fidelity._ACTION` was
  mutated and 85 tests stayed green. That is a gap in that family's suite;
  closing it from F4 would mean snapshotting twenty-one families' action strings
  in this test file, which would red on their authors' PRs for their own
  legitimate edits. **Recorded as a follow-up for the doc-health steward**, whose
  correct home is one pin per family in that family's own suite.
- **M5b (a JOB-level `env` carrying the flag) SURVIVED — found by the combined
  review.** The § 5.3 probe walked `jobs.*.steps.*` only, and Actions resolves
  `env` at three levels; both jobs here already carry a job-level `env` block, so
  the missed shape was one line from an existing one. Fixed by walking
  workflow-level `env`, `jobs.<id>.env`/`.with`, and every step's `env`/`with`
  beside `run`. **M5b re-run: killed**, tracked file byte-identical afterwards.

## Two review findings in the tests themselves

- **The partition assertion was tautological.** It read
  `[c.id for c in mbc.CLASSES if mbc.classify(f) == c.id]`, which can never
  exceed one hit however many patterns match — so it asserted "classify returns
  something in CLASSES", not "exactly one pattern matches". Rewritten to iterate
  `_CLASS_PATTERNS`. **Measured on the corrected assertion: 37 findings across
  thirteen fixture trees and the real corpus, 0 multi-matches.**
- **A docstring overclaimed.** `FindingClass` said `band` and `action` are read
  from the module constants "so the flip moves the rendered label"; `action` is
  not rendered by `class_summary` at all. Corrected to say what each is for —
  `band` rendered, `action` carried so the per-class pin has one source.

## One test outside this feature changed, deliberately and visibly

`test_modified_block_currency_fixtures.py::test_this_feature_touches_no_production_module`
snapshots the family module's public callable surface, and F4 adds four names
(`FindingClass`, `classify`, `class_counts`, `class_summary`). It reddened on the
first full run. **The guard worked, and its own docstring is the instruction that
was followed**: the snapshot was extended as its own task (T040) with a dated
paragraph naming who added the names and why, and it is named here. F2's claim
that *F2* adds no behaviour is untouched; no severity, rule text or fixture
assertion moved.

## Gates

| gate | result |
| --- | --- |
| `pytest tests/doc-health -q` | **1204 passed** (+26 vs 1178 at the branch point) |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | **76 passed, 0 failed** |
| F1 + F2 + F3 + promotion-fidelity + F4 | **235 passed** |
| `git diff --stat <merge-base> -- .github/ openspec/` | **empty** |
| report movement | **0 critical, 0 error, +1 warning, +8 info** — equal to the family's own counts |
| movement confinement | **3 of the report's 30 headings** differ: `## Headline`, `### modified-block-currency`, `## Ranked Plan` (9 rows, all this family's) |
| repo-local validators | none affected — every `scripts/validate-*.py` validates contract YAML, and this feature adds none |
| CI shape | **26 passed** in a `git archive HEAD` extraction with a fresh `git init` — no worktree, no remote |

**Independently reproduced by the combined review**, which additionally checked:
byte-identity against `origin/main`'s own `report.py`; a `--previous-report`
round-trip (0 regressions, 0 uncited resolutions — the subtotal cannot re-enter
as a finding); canon's "Health report contract" and "Finding severity and
regression handling" unviolated; and an archive dry-check reading 8 → 8 with
exactly the six predicted differences.

## Scope

Changed, by `git diff --numstat` against the merge base: `modified_block_currency.py`
**+189/−0** (additive: the class map and the summary), `families.py` **+30/−0**
(the registry), `report.py` **+19/−2** (an additive render branch),
`__init__.py` **+9/−0** (a docstring), `test_modified_block_currency_fixtures.py`
**+14/−2** (the snapshot amendment above), plus one new test file. **No rule text, severity, resolution class, finding
grammar or ranked-plan grammar changed. `.github/` and `openspec/` untouched.**

## #330 IS NOT CLOSED BY THIS

Per the packet's § 7.1, and stated here because § 7.1 asks every PR in this
change to state it: the post-archive safety net — diffing a promoted spec against
its own prior state across the archive commit — is **not built** by this change
and #330 stays open. Its owner is the doc-health steward at the next family
change touching `promotion_fidelity.py`.

## OPEN QUESTION FOR BRETT — carried forward from F3, undecided

`_LEDGER_SUBJECTS` in F3's self-gate is an exact set of live corpus triples, and
`pytest-suite` is a REQUIRED check on `main` (org ruleset 21538893). Any PR that
adds a lossy MODIFIED block, archives one of the changes in that table, or edits
canon in a way an active block quotes will red that gate — on a branch whose
author may have nothing to do with doc-health. **That is § 4's intent working as
written, and a cost nobody has priced.** The option, if the cost is too high: a
pytest marker routing the six corpus-facing tests to the nightly lane, keeping
the structural pins in `pytest-suite`. It already fell due once, on F3's own PR
#427, and that event is evidence for both sides.

**F4 does not decide it and changes nothing about it.**

**A SECOND QUESTION, also for Brett, also undecided** (`specs/022-…/tasks.md`
§ SECOND OPEN QUESTION): the `unclassified` residual row is TEXT — no severity,
no ranked-plan item, no `--fail-on` reach — and the only real-corpus
classification test reads openxFactory alone while the nightly runs eighteen
repositories. The cheapest close is to have a nonzero count emit one `warning`
finding, which makes the residual a FIFTH finding class of a family whose
promoted requirement enumerates three arms and four classes. **That is a delta
change and needs a ruling**, so F4 leaves it as text and says so in the contract,
the research record and the hand-off. One datum F4 adds: every
corpus-facing assertion in F4's own test file is a floor or an invariant, never a
named set or an absolute count — a choice available to F4 because it asserts a
RENDERING rather than a verdict, and not an argument that F3 could have made the
same one. The full text is in `specs/022-…/tasks.md` § OPEN QUESTION FOR BRETT.

---

Refs #357 #329 #330

🤖 Generated with [Claude Code](https://claude.com/claude-code)
