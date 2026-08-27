# Speckit F2: the modified-block-currency regression-fixture catalogue

**F2 of four** realizing the ratified change `add-modified-block-currency-check`
— its **§ 3, items 3.1–3.13**, and nothing else. F1 is on `main` at `19e3f6b5`.

**No behaviour is added to any module.**
`git diff --stat $(git merge-base HEAD origin/main) -- scripts/ openspec/ .github/`
is **empty**.

## What this is

F1's implementation review found that F1 already realizes every scenario of the
ratified delta with a test. So F2 is an **audit first**, then the gaps:

1. **`contracts/coverage-audit.md`** maps all fourteen § 3 items across
   **18 rows** to the F1 test functions that discharge them — taken from the
   LANDED test file, not from F1's plan, hand-off, or spec § Out of Scope, which
   disagree with each other.
2. **The nine non-satisfied rows are closed**, RED-first, with a two-stage RED
   per fixture.

**Audit result: 8 satisfied · 1 satisfied-extended · 6 partial · 3 gapped.**
The eight `satisfied` rows gained no test — that is the point of auditing first.

## Rows closed

| row | § 3 | what was missing | closed by |
| --- | --- | --- | --- |
| A1 | 3.1 | the #351 instance in its REAL text | `…-history-351`, reconstructed @ `bcfc26a0` |
| A2 | 3.2 | the #329 instance in its REAL text | `…-history-329`, reconstructed @ `d5f447e8` |
| A3 | 3.3 | **the one true hole** — a `Merged into` marker over a four-bullet scenario with two dropped | `…-merge-gut` |
| A5 | 3.4 | widening BEFORE and at BOTH ends; containment through the family | T033 + the real #351 instance |
| A6 | 3.5 | `contract-v1.45`, `promotion_fidelity.py`, a 4-sentence note EDITED in its third sentence | `…-tokens` |
| A7 | 3.6 | re-wrap quiet END TO END, not at `carried()` | `…-rewrap` |
| A10 | 3.7(c) | the form anchor on the REAL packet file | reads the ratified delta |
| A11 | 3.7(d) | the longer fence through the family, SUPPRESSING | `…-fence` |
| A15 | 3.10 | a case whose declaration points AGAINST name order | `…-name-order` |
| A18 | 3.13 | (satisfied) extended to all thirteen trees | T049 |

## The two reconstructions are real text, and the tests prove it

- **#351** — `add-doxchat-model-intake`'s pre-repair block and the canon of
  2026-08-25, both at `bcfc26a0d2f182c652ed9054b82210ccbee8124a`, the parent of
  the repair `f68261f7` (merged `87d0b95a`, PR #358). One `warning` naming
  exactly `The menu offers a routing rule` and `A fourth provider verb is
  proposed`; one `info` listing 11 of canon's 25 units. Among them canon's
  badges bullet, which the block's replacement contains as a **strict prefix** —
  the packet's § 6.4 residue and the case a containment rule loses.
- **#329** — `add-release-inventory-drift-check`'s pre-archive delta and canon,
  both at `d5f447e89cf619fd12113bcf03525468ece4470d`, the parent of the archive
  `38b548d4` (merged `b03b9992`, PR #331). Seven titles named; canon 8 scenarios
  and delta FILE 8 — flat, and the family fires anyway.

`test_the_reconstructed_fixtures_are_the_history_they_claim` re-derives both
from git rather than trusting the files, telling a shallow clone (skip) apart
from a disagreement (fail) with `git rev-parse --is-shallow-repository`.

The other five trees are **SYNTHESIZED** and each says so on line 3 of its
`README.md`, because this corpus carries no instance of their shapes.

## The mutation round found two tests that asserted nothing

Thirty perturbations, each with a named test that must fail. **Two survived the
first pass, and both were real:**

- **#15** stripped the backticks from `contract-v1.45` in BOTH canon and the
  block. `test_no_unit_boundary_falls_inside_a_versioned_token` survived,
  because it only asserted the token was ABSENT from the ledger — and when a
  boundary moves on both sides at once the halves still match, nothing is
  reported, and the negative holds. **A negative cannot see a symmetric break.**
  The test now asserts positively on canon's own derivation.
- **#29** dropped the `kinds` filter from the U-class helper. Every U-class test
  survived, because each re-filters by kind afterwards. Added
  `test_the_u_class_helper_reads_the_same_set_as_the_ledger_arm`, which parses
  the arm's OWN numerator and denominator out of the finding it emits.

**Final: 28 of 30 killed, 0 survivors.** Two rows are N/A — pure test-body
assertions with no fixture to perturb — and are recorded as N/A rather than
counted as kills.

## Two of the audit's own verdicts were wrong

Recorded rather than smoothed over, because a wrong `satisfied` is this
feature's worst failure mode:

- **A15** was `satisfied` and is not. F1's cited
  `test_no_date_folder_or_created_field_decides_the_ordering` concedes in its
  OWN docstring that its fixture "sorts BEFORE … by name and by any date a
  fixture could carry, **and the declaration points the same way**", so it
  cannot be the discriminating test § 3.10 asks for. Its structural grep forbids
  date readers and forbids **nothing** about ordering by folder or change-id
  name — which the delta prohibits in the same breath. A build sorting the
  ratified group by `b.change` passes every F1 test.
- **A10** was `satisfied` on a claim no test made.

Both were caught by re-reading the cited test **bodies** rather than their
names. That reading is now T059 step 1.

## One task expectation was wrong and is corrected, not worked around

`tasks.md` T042 predicted that a single-backtick marker naming a fragment would
ALSO be reported as a marker defect. **It is not, and should not be** — the
delta reports a marker only where it names a unit the block still carries; a
name matching no canon unit declares nothing and is silent, per
`suppression()`'s documented three-way resolution. The module is right; the task
was wrong. The test asserts the correct behaviour and the fence `README.md`
explains why.

## No module defect was found

**T053: nothing fired.** Every one of the nine closed rows was exercised
against F1's landed implementation and every arm behaved as the ratified delta
states. What was found instead was F1 DOCUMENTATION residue, appended to
`specs/019-modified-block-currency-family/tasks.md` § "Residue found by F2" —
where F1's owner reads. No issue filed. Five items, none a behaviour defect.

## Evidence

| gate | before | after |
| --- | --- | --- |
| `python3 -m pytest tests/doc-health -q` | 1077 passed | **1115 passed** (+38) |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | 75 / 0 failed | **75 / 0 failed** — unchanged |
| `git diff --stat <merge-base> -- scripts/ openspec/ .github/` | — | **empty** |
| mutation round | — | 28/30 killed, **0 survivors** |
| `test_family_enumeration` + F1's file + scan-set | — | 138 passed, unchanged |

The whole-tree `pytest tests` is deliberately NOT run: it needs a live Postgres
this worktree has no access to, and a red there would say nothing about this
feature.

## What this change does NOT do

- **It does not close #330.** The post-archive safety net (packet § 7.1) is
  recorded, not built, and needs a third measurement basis inside a family whose
  promoted requirement obliges it to declare which of TWO it measured.
- **It proposes no severity flip** (packet § 7.2). `_LAUNCH_SEVERITY` is
  untouched and the family stays absent from `FAMILY_RESOLUTION`.
- It does not touch the report section, the action line or the workflow pin
  (packet § 5 — F4), nor the self-gate against this repository (§ 4 — F3).
- It changes no promoted spec, no delta, and nothing under `scripts/`.
