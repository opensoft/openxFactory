# Speckit F2: the modified-block-currency regression catalogue

**F2 of four** realizing the ratified change `add-modified-block-currency-check`
— its **§ 3, items 3.1–3.13**, and nothing else. F1 is on `main` at `19e3f6b5`.

**No behaviour is added to any module.**
`git diff --stat $(git merge-base HEAD origin/main) -- scripts/ openspec/ .github/`
is **empty**. Use the merge-base, never `origin/main` itself: that branch
advances independently, and diffing against its tip today reports its own
progress as 13 files and 2,443 deletions this feature never made.

## What this is

F1's implementation review found that F1 already realizes every scenario of the
ratified delta with a test. So F2 is an **audit first**, then the gaps:

1. **`contracts/coverage-audit.md`** maps all fourteen § 3 items across
   **18 rows** to the F1 test functions that discharge them — taken from the
   LANDED test file, not from F1's plan, its hand-off, or its spec § Out of
   Scope, which disagree with each other.
2. **The nine non-satisfied rows are closed**, RED-first, with a two-stage RED
   per fixture: the test errors with no fixture, then the built fixture is
   PERTURBED in the one way that matters and the test must fail on its
   *assertion*.

**Audit result: 8 satisfied · 1 satisfied-extended · 6 partial · 3 gapped.**
The eight `satisfied` rows gained no test — that is the point of auditing first.

## The audit's closing table — all nine non-satisfied rows closed

| row | § 3 | verdict at audit time | closed by | fixture tree |
| --- | --- | --- | --- | --- |
| **A1** | 3.1 | gapped | T010–T016, T022 | `…-history-351`, reconstructed @ `bcfc26a0` |
| **A2** | 3.2 | gapped | T017–T022 | `…-history-329`, reconstructed @ `d5f447e8` |
| **A3** | 3.3 | gapped — **the one true hole** | T027–T032 | `…-merge-gut` |
| **A5** | 3.4 | partial | T033 + T014 | — / `…-history-351` |
| **A6** | 3.5 | partial | T034–T037a | `…-tokens` |
| **A7** | 3.6 | partial | T038–T040 | `…-rewrap` |
| **A10** | 3.7(c) | partial | T043c | — (reads the ratified packet's own delta) |
| **A11** | 3.7(d) | partial | T041–T043 | `…-fence` |
| **A15** | 3.10 | partial | T043a–T043b | `…-name-order` |
| **A18** | 3.13 | satisfied, extended | T049 | all thirteen trees |

Satisfied, untouched: A4, A8, A9, A12, A13, A14, A16, A17.

## The two reconstructions are real text, and the tests prove it

- **#351** — `add-doxchat-model-intake`'s pre-repair block and the canon of
  2026-08-25, both at `bcfc26a0d2f182c652ed9054b82210ccbee8124a`, the parent of
  the repair `f68261f7` (merged `87d0b95a`, PR #358). One `warning` naming
  exactly `The menu offers a routing rule` and `A fourth provider verb is
  proposed`; one `info` listing 11 of canon's 25 units. Among them canon's
  badges bullet, which the block's replacement contains as a **strict prefix** —
  the packet's § 6.4 residue, the finding PR #358's manual
  `canon ⊆ intake ⊆ B` verification reported, and the case a containment rule
  loses.
- **#329** — `add-release-inventory-drift-check`'s pre-archive delta and canon,
  both at `d5f447e89cf619fd12113bcf03525468ece4470d`, the parent of the archive
  `38b548d4` (merged `b03b9992`, PR #331). Seven titles named; canon 8 scenarios
  and delta FILE 8 — flat, and the family fires anyway, which is why counting
  could never see this class.

`test_the_reconstructed_fixtures_are_the_history_they_claim` re-derives both
from git rather than trusting the files — the delta byte-for-byte, canon scoped
to the requirement section — telling a shallow clone (skip) apart from a
disagreement (fail) with `git rev-parse --is-shallow-repository`, exactly as
`test_ideation_readiness.py` does. CI checks out at `fetch-depth: 0`.

The other five trees are **SYNTHESIZED** and each says so on line 3 of its
`README.md`, because this corpus carries no instance of their shapes.

**The #329 tree is deliberately stale `doc-health` text** and its README says so:
a whole-family sweep over it would draw 3 `family-enumeration` warnings (its
restatement says "nineteen"; 22 are registered). Inert today — nothing sweeps
fixture trees — and refreshing that text would destroy the instance.

## The mutation round found two tests that asserted nothing

Thirty perturbations, each with a named test that must fail. **Two survived the
first pass, and both were genuinely weak:**

- **#15** stripped the backticks from `contract-v1.45` in BOTH canon and the
  block. `test_no_unit_boundary_falls_inside_a_versioned_token` survived,
  because it only asserted the token was ABSENT from the ledger — and when a
  sentence boundary moves on both sides at once the halves still match, nothing
  is reported, and the negative holds. **A negative cannot see a symmetric
  break.** The test now asserts positively on canon's own derivation.
- **#29** dropped the `kinds` filter from the U-class helper. Every U-class test
  survived, because each re-filters by kind afterwards, so the helper's own
  contract was asserted nowhere. Added
  `test_the_u_class_helper_reads_the_same_set_as_the_ledger_arm`, which parses
  the arm's OWN numerator and denominator out of the finding it emits.

**Final: 28 of 30 killed, 0 survivors** (2 rows N/A — pure test-body assertions
with no fixture to perturb, recorded as N/A rather than counted as kills). The
reviewer's independent re-run killed **10 of 10**.

Mutants #26, #27 and #30 edit the module deliberately, to prove the determinism,
severity-band and scope-guard tests are load-bearing. Each is reverted in the
same working step; none is committed.

## No module defect was found

**T053: nothing fired.** Every one of the nine closed rows was exercised against
F1's landed implementation and every arm behaved as the ratified delta states.
The scope of that claim is written down rather than implied: both carriage arms
on real historical text; marker suppression in all three branches of its
resolution; the `Merged into` titles-only rule; the fence rule in both
directions; basis substitution under a declaration; the sentence mask on three
token shapes; whitespace normalization over a fully re-wrapped block;
skip-vs-quiet; determinism and the advisory band over all thirteen trees.

What was found instead is F1 **documentation** residue — five items, none a
behaviour defect — appended to
`specs/019-modified-block-currency-family/tasks.md` § "Residue found by F2",
which is where F1's owner reads. No issue filed.

## Two of this feature's own verdicts were wrong

Recorded rather than smoothed over, because a wrong `satisfied` is this
feature's worst failure mode and it happened twice:

- **A15** was `satisfied` and is not. F1's cited
  `test_no_date_folder_or_created_field_decides_the_ordering` concedes in its
  OWN docstring that its fixture "sorts BEFORE … by name and by any date a
  fixture could carry, **and the declaration points the same way**", so it
  cannot be the discriminating test § 3.10 asks for. Its structural fallback
  forbids date readers and forbids **nothing** about ordering by folder or
  change-id name — which the delta prohibits in the same breath. A build sorting
  the ratified group by `b.change` passes every F1 test. The new `…-name-order`
  tree fixes that: `add-zz-first` DECLARES and is therefore the later writer
  while sorting LAST by name, so the finding lands on its path and names
  `add-aa-second`'s **delta** as the basis. Under name-ascending ordering the
  roles invert and the test fails.
- **A10** was `satisfied` on a claim no test made — "the anchor is asserted
  against this packet's OWN delta prose". F1 asserts it over text written inside
  its own test bodies, and the packet sets its two templates out as `- `
  BULLETS, which are carriage units the fenced-block exemption never reaches.

Both were caught by re-reading the cited test **bodies** rather than their
names, which is now T059 step 1.

**The honest limit, stated because it cannot be fixed:** the eight remaining
`satisfied` verdicts rest on a human reading of F1's test bodies.
`test_no_audit_row_cites_a_test_that_does_not_exist` mechanizes only the
citation; T059 step 1 mechanizes only the discipline of re-reading. **If one of
those eight is wrong, this change ships a hole it believes it closed.** The
mitigation is that F1's own hand-off, F1's mutation round, and two independent
reads of the landed file agree on all eight.

## One task expectation was wrong, and is corrected rather than worked around

`tasks.md` T042 predicted that a single-backtick marker naming a fragment would
ALSO be reported as a marker defect. **It is not, and should not be** — the
delta reports a marker only where it names a unit the block still carries; a
name matching no canon unit declares nothing and is silent, per
`suppression()`'s documented three-way resolution. The module is right; the task
was wrong. The test asserts the correct behaviour and the fence `README.md`
explains why.

## The audit reads itself

Three tests open `contracts/coverage-audit.md` and fail on it: every backticked
`test_*` name it cites must be defined (with a floor of thirty harvested names,
so a regex matching nothing cannot pass); all fourteen § 3 items must appear in
the `§ 3 item` column with exactly one bolded verdict per row and the four
tallies matching the row bodies; and every `T0NN` in the last column must exist
in `tasks.md`. That third test exists because this audit shipped, once, citing a
whole superseded task numbering after tasks were renumbered.

## Evidence

| gate | before | after |
| --- | --- | --- |
| `python3 -m pytest tests/doc-health -q` | 1077 passed | **1115 passed** (+38) |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | 75 passed / 0 failed | **75 passed / 0 failed** — unchanged |
| `git diff --stat $(git merge-base HEAD origin/main) -- scripts/ openspec/ .github/` | — | **empty** |
| mutation round | — | **28/30 killed, 0 survivors**; reviewer's re-run 10/10 |
| `test_family_enumeration` + F1's own file + scan-set | — | 138 passed, unchanged |

**38 tests** in one new file, **7 new fixture trees** (2 reconstructed, 5
synthesized), 66/66 tasks complete, zero lines of production code.

The whole-tree `pytest tests` is deliberately NOT run: it needs a live Postgres
this worktree has no access to, and a red there would say nothing about this
feature.

## What this change does NOT do

- **It does not close #330.** The post-archive safety net (packet § 7.1) is
  recorded, not built: it needs a third measurement basis inside a family whose
  promoted requirement obliges it to declare which of TWO it measured.
- **It proposes no severity flip** (packet § 7.2). `_LAUNCH_SEVERITY` is
  untouched and the family stays absent from `FAMILY_RESOLUTION`.
- It does not touch the report section, the action line or the workflow pin
  (packet § 5 — F4), nor the self-gate against this repository (§ 4 — F3).
- It changes no promoted spec, no delta, and nothing under `scripts/`.

Refs #357 #329 #330

🤖 Generated with [Claude Code](https://claude.com/claude-code)
