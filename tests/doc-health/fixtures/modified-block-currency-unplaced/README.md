# Fixture: four plain-titled blocks whose findings the class map places

**SYNTHESIZED** — this text is invented and reproduces no historical instance.

## Which rule this exists for

`add-unclassified-finding-class` § 2.8, Speckit feature
`026-unplaced-finding-drift`. It is the behavioural tree for the family's FIFTH
finding class, `unplaced-finding drift`.

> The modified-block-currency family SHALL emit ONE ADDITIONAL `warning` finding
> per run for each DISTINCT SHAPE of rule text its own class map does not place
> — `openspec/changes/add-unclassified-finding-class/specs/doc-health/spec.md`

## Why this tree does NOT contain an unplaceable title

It cannot. Every rule text this family constructs is one of five fixed prefixes
plus `{title!r}`, and `_TITLE_REPR` admits both `repr` quotings and the `\.`
escape, so no corpus-supplied title falls outside the map. Fuzzed at packet
review: 13 adversarial titles plus 4000 random ones over an alphabet of quotes,
backslashes, control characters and class phrases, times the five rule shapes =
**20,065 rule texts, 0 unplaceable** (packet § 3.5).

**So the trigger is the DRIFT, not the title.** This tree supplies REAL arm
findings, and each test that exercises the fifth class removes one entry from
`_CLASS_PATTERNS` — which is precisely the live condition the class exists to
report: "the map has drifted behind the arms". The family, the classifier, the
summary and the renderer all run unmodified.

## Why every title here is plain

No requirement title contains another class's phrase (`omits`, `does not carry`,
`carries a … marker by`, `resolves to no promoted requirement`, `the ordering of
MODIFIED blocks`) or the fifth class's own opening phrase. F2's `CLASSIFIERS`
(`test_modified_block_currency_fixtures.py`) are UNANCHORED substring probes and
`test_every_finding_falls_into_exactly_one_class` asserts `len(hits) == 1` over
`ALL_TREES`, so a corpus-supplied phrase in a title would fail that pin from
this tree — the trap that narrowed F1's own `_ledger` helper.

## What the family reports here, over the UNMODIFIED map

Four findings, all placed:

| finding | class | why |
| --- | --- | --- |
| `Gamma boundary is declared` omits 1 of 2 scenarios | `scenario-titles` (`warning`) | the block restates one scenario heading and pools the other's bullets under it |
| `Zeta boundary is declared` does not carry 1 of 7 units | `carriage-ledger` (`info`) | one body sentence dropped — in the OTHER change directory |
| `Alpha boundary is declared` does not carry 1 of 7 units | `carriage-ledger` (`info`) | one body sentence dropped |
| `Beta boundary is declared` does not carry 1 of 7 units | `carriage-ledger` (`info`) | one body sentence dropped |

## Why there are TWO change directories

`add-a-drift-case/` carries Zeta alone, and it exists so the tree's EMISSION
order disagrees with the family's REPORT order. The arms emit by (capability,
normalized requirement title) — Alpha, Beta, Gamma, Zeta — while report order is
severity, then repo, then PATH, and `add-a-drift-case/` sorts before
`add-drift-cases/`. So the ledger shape's first-in-report-order is ZETA and its
first-in-emission-order is ALPHA.

That disagreement is the only thing that can falsify "the finding names the
FIRST of its shape in the family's own report order". Over a tree where the two
orders agree, grouping before the sort and grouping after it name the same
finding and the pin passes either way — which is exactly what the mutation round
measured against this tree's first, single-directory version: the mutant
"emit before the first sort" SURVIVED it.

The three ledger findings are ONE SHAPE (their rule texts are equal once every
quoted span and digit run is masked) and the titles finding is a SECOND. That is
what lets one tree drive both halves of the delta's third scenario:

- remove the `carriage-ledger` pattern → 3 unplaced findings, ONE shape → ONE
  drift finding naming the count 3;
- remove the `carriage-ledger` AND `scenario-titles` patterns → 4 unplaced
  findings, TWO shapes → TWO drift findings.

**THE GRAIN IS NOT "ONE FINDING PER REMEDY".** It is one finding per distinct
arm text after quoted-span and digit masking, which is FINER: a rule text's
unquoted parts (the promoted spec's path, the `[body]`/`[bullet]` kind list, a
change-id list) are shape-bearing. This tree collapses to one shape only because
its three ledger findings name the SAME spec and the same kind. On the real
repository the same dropped map entry yields SIX findings for seven unplaced
ones. That is the ratified delta's rule working as written; widening it is a
delta amendment, recorded open in
`specs/026-unplaced-finding-drift/plan.md`.

## Why this tree is not in F2's `NEW_TREES`

`NEW_TREES` means "the trees F2 adds", and its provenance checker additionally
requires each README to cite an F2 audit row and an
`add-modified-block-currency-check § 3.x` section. This tree belongs to neither.
Fabricating an audit row to satisfy a checker would be the false-documentation
defect this whole family exists to catch. The tree joins `ALL_TREES` by glob —
which is what the glob is for — and its provenance and its bands are pinned by
`026-unplaced-finding-drift`'s own tests instead.
