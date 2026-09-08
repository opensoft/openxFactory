# Data model: the fixture catalogue (F2)

This feature adds no runtime type. Its entities are **fixture trees on disk**,
the **provenance note** beside each, the **audit row**, and the two
**assertion classes** every test in this feature belongs to. They are set out
here because getting any of the four shapes wrong is how a fixture ends up
asserting something other than the rule it was built for.

---

## 1. Fixture tree

A directory under `tests/doc-health/fixtures/`. **The directory name is the
argument `conftest.make_ctx` takes**, and `make_ctx` loads EVERY repository
directory beneath it into one `Context`.

```text
tests/doc-health/fixtures/modified-block-currency-<case>/
├── README.md                              # the provenance note (§ 2)
└── <name>Factory/                         # one miniature repository
    └── openspec/
        ├── specs/<capability>/spec.md      # the promoted side — CANON
        └── changes/<change-id>/
            ├── proposal.md                 # Status: line only; the standing reader needs it
            └── specs/<capability>/spec.md  # the active delta — THE BLOCK
```

**Invariants**

| # | invariant | why, and what breaks without it |
| --- | --- | --- |
| I1 | one tree per case; never add a repository or change to an existing tree | F1's `_run()`, `_markers_run()`, `_res_run()`, `_tw_run()` assert over WHOLE-TREE results, several with `== []`. Adding to a tree silently changes what those tests see (research R7) |
| I2 | repository directory names are distinct from F1's (`alphaFactory`, `betaFactory`, `gammaFactory`, `quietFactory`, `emptyFactory`) | a finding's `repo` field then identifies its tree in any failure message |
| I3 | the canon file carries a `# <capability> Specification` heading, a `## Purpose`, `## Requirements`, and the requirement(s) under test — nothing else | `promoted()` stops at the next `## ` section; a stray section becomes body units nobody is testing (F1's `test_the_promoted_reader_stops_at_the_next_section`) |
| I4 | `proposal.md` exists and carries a `Status:` line | `_standing()` reads it; a change with no proposal reads standing `None`, which changes the two-writers arm's scope. `ratified` unless the case is about draft standing |
| I5 | the delta file's section headings are `## MODIFIED Requirements` / `## ADDED Requirements` / `## RENAMED Requirements` exactly | the delta side reads through `promotion_fidelity.parse_delta`, one grammar for four families |
| I6 | no tree contains a `Status:`-bearing governed document | `tests` is in `corpus.EXCLUDED_PARTS` and no `GOVERNED_ROOTS` entry covers it, so nothing here is scanned by the lifecycle families — verified, not assumed (research R6) |

**Trees this feature adds**

| tree | audit row | § 3 | repo dir | capability | reconstructed? |
| --- | --- | --- | --- | --- | --- |
| `modified-block-currency-history-351` | A1 | 3.1 | `intakeFactory` | `ideation-dashboard` | yes — `bcfc26a0` |
| `modified-block-currency-history-329` | A2 | 3.2 | `driftFactory` | `doc-health` | yes — `d5f447e8` |
| `modified-block-currency-merge-gut` | A3 | 3.3 | `mergeFactory` | `merge-gut` | no — synthesized |
| `modified-block-currency-tokens` | A6 | 3.5 | `tokenFactory` | `token-cases` | no — synthesized |
| `modified-block-currency-rewrap` | A7 | 3.6 | `rewrapFactory` | `rewrap-cases` | no — synthesized |
| `modified-block-currency-fence` | A11 | 3.7(d) | `fenceFactory` | `fence-cases` | no — synthesized |

A synthesized capability name that no promoted spec in this repository carries
(`merge-gut`, `token-cases`, …) is deliberate: it makes a fixture's capability
unmistakable in a finding and cannot collide with real canon.

---

## 2. Provenance note

`README.md` at the root of a fixture tree. **New to this suite** — no fixture
carries one today; the existing convention is a paragraph in the test module's
docstring, which F2 also keeps. The note exists so a reader can PASTE a command
and see the source text, which a docstring cannot offer.

**Required content, reconstruction:**

- the issue number and one sentence on what the defect was
- the commit the text was recovered from, in full 40 hex
- the repair or archive commit that ended the defect, and the merge commit /
  PR number
- one `git show <sha>:<path>` line per fixture file, verbatim and runnable
- **the scope of the verbatim guarantee** — for a canon file, that the
  REQUIREMENT is byte-identical and the surrounding `# … Specification` /
  `## Purpose` / `## Requirements` lines are synthetic scaffolding
- what the family reports on the tree, in one line, so a reader can tell
  whether a later change moved it

**Required content, synthesis:**

- an explicit statement that the text is invented
- the rule it illustrates, quoted from the ratified delta with its line span
- why a reconstruction was not used (for these four: no such instance exists
  in this corpus)

Contract detail: `contracts/fixture-provenance.md`.

---

## 3. Audit row

A row of `contracts/coverage-audit.md`. Fields: `id` (`A<n>`, stable, cited by
tasks), `§ 3 item`, `F1 tests` (function names that must exist in the landed
test file), `verdict` ∈ {`satisfied`, `partial`, `gapped`, `satisfied,
extended`}, and `what is missing` naming the F2 task.

**The row is the deliverable for a `satisfied` item.** FR-002: an item F1
covers gets no F2 test.

---

## 4. Assertion classes — the distinction every test in this feature obeys

The ledger renders each unit truncated to `_QUOTE_WIDTH = 140` characters
(research R4). So an assertion is one of exactly two kinds, and a test that
mixes them fails for reasons unrelated to its rule.

| class | asserted against | used for | example |
| --- | --- | --- | --- |
| **U — unit-level** | the `Unit` objects the comparison returns: `mbc.carried(basis.units, block.units)`, each a `(kind, text)` pair | full clause text, especially text past the 140th character of a long sentence; kind discrimination | `thread file` appears in the text of some returned `body` unit |
| **F — finding-level** | the emitted `Finding`'s `rule`, `severity`, `path`, `repo`, `family` | that the ARM fired, on the right path, at the right severity, naming the right subject | the `warning` names `The menu offers a routing rule` |

**Every § 3.1 / § 3.2 test pairs one of each.** The finding-level half proves
the arm ran; the unit-level half proves it found the right thing. Neither alone
is enough: a finding-level-only test passes over a build that reported the
wrong units, and a unit-level-only test passes over a build whose arms never
emit.

**Never asserted, anywhere in this feature**: a finding count, a unit count, a
scenario count, or `len(...)` as the whole assertion (orchestrator decision 3).

### The count-exception list — ONE home, and this is it

T059 step 2 greps the new test file for `len(`, `== <n>` and `count(` and
requires every hit to fall into one of the SHAPES below. **Shapes, not an
enumeration of lines**: the first cut of this section listed individual
assertions, and the review found ~20 of the file's 38 count-shaped lines
mapping to no row at all — including `len(holders) == 1`, which is the very
assertion that kills mutant #15. A list that does not cover the file makes
T059 step 2's claim false, and a per-line list goes stale on the next test.

**Five permitted shapes.**

| # | shape | why the count is legitimate | examples |
| --- | --- | --- | --- |
| **S1** | **Per-arm cardinality** — "exactly one finding of this class for this requirement" | the ledger's own promoted rule is "at most one finding per requirement, listing the units", and the title arm emits one per requirement too. The count IS the obligation | `len(hits) == 1` in T012, T017, T019's arm check, T027, T041, T042, T043a |
| **S2** | **Vacuity floors** — a non-empty or lower-bound check placed BEFORE a universal negative | "no finding is `error`" and "the token is absent from the rule" are both vacuously true of nothing, and nothing is exactly what a broken discovery returns. The floor is a guard, not a measurement | `assert findings`, `seen > 20`, `total > 20`, `len(cited) > 30`, `len(ALL_TREES) >= 13` |
| **S3** | **Fixture-premise guards** — "this fixture really has the shape this test needs" | a test whose premise silently evaporated passes while testing nothing. These assert the FIXTURE, never the family's output | `len(holders) == 1` (one body unit holds the token), `len(widened) == 1` (the containment premise), `len(notes) == 1`, `len(blocks) == 1`, `len(block.markers) == 1`, `len(bullets) == 2` templates, `changes == [...]` |
| **S4** | **The count that IS the rule under test** | § 3.2's flat file-level eight-and-eight, asserted precisely because it does NOT predict the outcome; § 3.5's "each bullet SHALL be one unit" and "the note is ONE unit, undivided", which are statements about cardinality | `len(canon.scenario_titles) == 8`, `delta_text.count(...) == 8`, `len(bullets) == 2`, `rule.count("CORRECTED 2026-08-27") == 1`, `note.count(...) == 1` |
| **S5** | **Figures parsed out of the arm's OWN finding** | the numerator and denominator are read from the text the arm emits, so the comparison is the arm's rule rather than an invented expectation | `len(_units(...)) == numerator` and the denominator check in `test_the_u_class_helper_reads_the_same_set_as_the_ledger_arm` |

**S6 — the audit's own structural claims** are counts too, and legitimate for
the same reason as S4: `len(rows) == 18` and the four verdict tallies are what
the audit asserts about itself, so a row that gained or lost a verdict is the
defect the assertion exists to catch.

A count-shaped line that fits none of S1–S6 is a count assertion that slipped
past decision D3, and is a finding against the implementation rather than a new
row here. **Backtick-and-parenthesis counts** (`chunk.count("`") % 2 == 0`) are
not measurements of anything the family reports — they are the tokenization
invariant expressed as parity, and belong to S3.

---

## 5. Reported unit

`modified_block_currency.Unit`: `kind` ∈ {`body`, `scenario-title`,
`scenario-bullet`}, `text` (whitespace-normalized), and for a bullet its
owning scenario. Consumed, never defined here. Two properties this feature
leans on:

- **same-kind matching**: a canon `body` unit is never carried by a block
  `scenario-bullet` of the same text
- **set semantics** (F1's decision O11): a normalized unit canon states twice
  is carried by one block occurrence. No fixture in this feature repeats a
  unit within a requirement, so the semantics are not exercised and not
  re-tested
