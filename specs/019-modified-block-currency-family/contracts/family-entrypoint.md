# Contract: the family entry point, the three arms, and the registration surface

**Module**: `scripts/doc_health/modified_block_currency.py`
**Realizes**: FR-001 – FR-003, FR-011 – FR-014, FR-022 – FR-030.

---

## Module constants

```text
FAMILY               = "modified-block-currency"
_LAUNCH_SEVERITY     = WARNING   # scenario-title arm — THE ARM § 7.2's FLIP MOVES
_RESOLUTION_SEVERITY = WARNING   # title resolution / two-writers — does NOT flip
_LEDGER_SEVERITY     = INFO      # carriage ledger — no flip proposed (D3)
DELTA_GLOB           = "openspec/changes/*/specs/*/spec.md"   # archive excluded
CANON_TEMPLATE       = "openspec/specs/{capability}/spec.md"
```

Three constants, not one: `tasks:82-83` wants the flip to be one line, and
`tasks:333-339` reserves it for the scenario-title arm alone. The
flip-bearing constant keeps the `_LAUNCH_SEVERITY` name the three sibling
families use, because that identifier is the grep that ties every reader of a
launch decision together.

The family is **ABSENT** from `families.FAMILY_RESOLUTION`, deliberately and in
the same shape its three predecessors launched under: a `contested` class would
route a resolved finding into `report.uncited_resolutions` as an `error`, so an
advisory family would red the nightly the first time anyone corrected a block.
Both halves flip together, by ruling, and neither flips here.

---

## Discovery and reading

```text
active_blocks(root: Path) -> list[ActiveBlock]
```

- Glob `DELTA_GLOB` under `root`, EXCLUDING any path whose first component
  under `openspec/changes/` is `archive`.
- Read each file; `promotion_fidelity.parse_delta` gives requirements (with
  `op`, `title`, `scenarios`, `body`) and the change's `RENAMED` pairs.
- Keep the `MODIFIED` requirements. Derive units and markers from `body`.
- Read the change's lifecycle standing through `corpus.parse_status` +
  `promotion_fidelity.declared_standing`, for the two-writers `ratified`
  scoping ONLY. Standing NEVER gates whether a block is read (`dh:30-36`).

```text
promoted(root: Path, capability: str) -> dict[str, PromotedRequirement] | None
```

- Read `openspec/specs/<capability>/spec.md` from the CHECKED-OUT tree; cache
  per capability per repository. `None` where the file does not exist.
- Split into `### Requirement:` blocks with `promotion_fidelity`'s imported
  `_REQUIREMENT` and `_SCENARIO` regexes; derive units from each block's lines
  with the same `derive_units`.
- **THE SECTION-STOP INVARIANT** (N10, stated because getting it wrong is
  silent): a requirement block ends at the next `### Requirement:` heading OR at
  the next `## ` heading that is not a `### `. A promoted spec carries `## `
  sections after its requirements — `family_enumeration.requirement_prose`
  already stops on exactly that condition (`family_enumeration.py`:226-229) and
  this reader takes the same stop. Without it, the LAST requirement in a spec
  swallows every trailing section as body units, and every block that modifies
  it is reported as failing to carry text that was never part of it.

**No live-`main` basis exists in this module** — no `--*-basis` option, no
`FAMILY_NOTES` entry, no `GitRefTree`. `dh:206-210` reserves that basis for
promotion fidelity and calls it "actively wrong here".

---

## Title resolution (arm 3, part 1)

```text
resolve(block, canon, sibling_titles) -> Resolution
```

In order (`dh:58-64`):

1. `norm(block.title)` present in `canon` → measure against that requirement.
2. Else the change's OWN `RENAMED` pairs name `(old -> block.title)` and
   `norm(old)` is in `canon` → measure against canon under the OLD name. **The
   arms then run in full**; a rename changes a title, not the content a block
   must carry.
3. Else an ACTIVE SIBLING change's `ADDED` or `RENAMED` block names this title
   → not reported; the promoted requirement is PENDING, not absent, and there
   is nothing to compare.
4. Else → one `_RESOLUTION_SEVERITY` finding: "a block modifying nothing is a
   block whose promotion adds text nobody reviewed as an addition".

---

## The two-writers rule (arm 3, part 2)

```text
order(writer_set) -> Basis | Finding(s)
```

- `declares(change_a, change_b)` is
  `duplicate_packet._mention(change_b).search(read(proposal_of(change_a)))` —
  the whole-token matcher named by reference in `dh:71-74`, imported rather
  than re-spelled.
- Exactly one declaration among ≥2 active RATIFIED writers → the declarer is
  the LATER writer, and its basis is the declared sibling's OUTCOME: canon's
  units for that requirement, REPLACED by the sibling's MODIFIED block for the
  same requirement. **That is the whole of it — a BASIS SUBSTITUTION and
  nothing else** (ruled 2026-08-27). The three arms then run unchanged against
  the substituted basis, so an addition the sibling makes that the declaring
  block does not carry is reported by the CARRIAGE arms. The resolution arm
  emits NOTHING here: a second finding would report at `warning` the same units
  the ledger reports at `info`, and `dh:264` requires the missing addition to be
  reported, not to be reported twice.
- **No basis is ever synthesized from a sibling's ADDED block** (ruled
  2026-08-27, B4). `dh:278-280` says a title resolving to an active sibling's
  addition is "pending rather than absent", and pending means there is nothing
  to compare: such a block is compared against NOTHING and reported nowhere.
  Synthesizing a basis from the sibling's ADDED text would measure all seven of
  this corpus's MODIFIED-over-a-sibling's-ADDED pairs and add roughly six `info`
  findings the delta says must not exist.
- Zero declarations among ≥2 active RATIFIED writers → one finding against
  EACH block; both measured against canon.
- Two or more declarations → one finding; both measured against canon; mutual
  declaration decides nothing.
- An UNRATIFIED writer creates no declaration obligation (`release-realization`
  is not widened) but its block is still READ and still measured against canon.
- **No folder name, commit timestamp or `created:` field is consulted, ever.**
  A test asserts this by constructing a pair that would order one way by date
  and the other way by declaration.

---

## Arm 3 — what the resolution arm reports, exhaustively

At `_RESOLUTION_SEVERITY`, and NOTHING else:

1. a MODIFIED title that resolves to no promoted requirement, no own-RENAME and
   no active sibling's ADDED/RENAMED block;
2. an UNDECLARED ordering between two or more active RATIFIED writers of one
   requirement, and a MUTUAL one.

Not the units a substituted basis makes uncarried (the carriage arms own
those), and not a title pending on a sibling's addition (nothing is wrong).

---

## Arm 1 — scenario-title completeness

```text
_arm_titles(block, basis, suppressed) -> list[Finding]
```

Every `scenario-title` unit of the basis that the block does not carry and that
is not suppressed. ONE finding per requirement, at `_LAUNCH_SEVERITY`, naming
every omitted title and the promoted spec they were read from.

Rule text shape:

```text
active MODIFIED block for '<title>' omits 2 of the 8 scenarios
'<capability>' currently states in openspec/specs/<cap>/spec.md:
'The menu offers a routing rule', 'A fourth provider verb is proposed'
```

Titles are listed in CANON order and in full (they are short strings — the
truncation `promotion_fidelity` applies at three is not copied, because the
whole point of this arm is that a reader can act on the list).

---

## Arm 2 — the carriage ledger

```text
_arm_ledger(block, basis, suppressed) -> list[Finding]
```

Every `body` and `scenario-bullet` unit of the basis the block does not carry,
minus the suppressed set. **AT MOST ONE finding per requirement**, at
`_LEDGER_SEVERITY`, listing every uncarried unit with its kind.

The rule text MUST NOT assert intent (`dh:252-255`). The required hedge, in the
finding itself:

```text
active MODIFIED block for '<title>' does not carry 3 units
openspec/specs/<cap>/spec.md states — a divergence this arm CANNOT
distinguish from a deliberate rewording: [body] '…', [bullet] '…', …
```

Long unit texts are elided to a stable length with a marker, deterministically
(no hashing, no ordering by length): document order, truncation at a fixed
character count, and the count of units always stated in full.

---

## The fourth finding class — marker defects

`_arm_marker_defects` (see [marker-parser.md](./marker-parser.md), and
note it is a CLASS not an arm) emits one `_LEDGER_SEVERITY` finding per marker
that names a unit the block still carries. Three arms, four finding classes; the
numbers differ and are kept apart deliberately.

---

## Dispositions

```text
dispositions = promotion_fidelity.load_dispositions(ctx, FAMILY)
... if promotion_fidelity.disposed(dispositions, repo, block.delta_rel,
                                   block.title): continue
```

No new reader (`tasks:113-116`). `load_dispositions` is already parameterized by
family and `disposed` is already generic — `duplicate_packet.py`:410-415 uses
both in this exact shape — so `promotion_fidelity.py` is not edited by this
feature. An entry without a `cite`, or naming another family, suppresses
nothing. The aggregation-root caveat is inherited: a `--single-repo` self-gate
applies no dispositions.

---

## Skip vs. quiet

```text
fam_modified_block_currency(ctx) -> list[Finding] | Skip
```

- `Skip(FAMILY, "no repository in scope carries an OpenSpec changes
  directory")` where NO repository in `ctx.repo_paths` has a readable
  `openspec/changes/`.
- A scope that HAS active changes but no `## MODIFIED Requirements` block among
  them returns `[]` — it ran and found nothing. Canon's skip rule is "cannot
  run", not "found nothing" (`dh:291-294`).

Findings are returned SORTED (repo, path, arm, rule) so a `--family` run is
byte-stable independently of `runner.run_suite`'s own global sort.

---

## Registration surface (GATED — FR-028, FR-028a, FR-028b)

**This whole section is unreachable until `add-family-enumeration-check` has
archived on `main` and been merged into this branch.** Registering a
twenty-second family while it is active emits three `family-enumeration`
findings against THAT packet's delta path, which no edit inside this change can
clear. Measured on this branch: 0 findings at 21 registered, 3 at 22. Ruled
2026-08-27, option (a).


| file | edit |
| --- | --- |
| `scripts/doc_health/families.py` | one name added to the existing `from . import (…)` block; one `FAMILIES` entry `"modified-block-currency": modified_block_currency.fam_modified_block_currency`; one comment recording the deliberate `FAMILY_RESOLUTION` absence, in the shape the four preceding families' comments use; the module docstring's owner list extended to name the twenty-second family |
| `scripts/doc_health/__init__.py` | one `FAMILY_IDS` entry with the twenty-second-family comment, so the family gets its own report section |
| `tests/doc-health/test_lifecycle_scan_set.py` | `"modified-block-currency"` added to `NON_READERS` with its reason; the `len(NON_READERS) == len(FAMILIES) - 4 == 17` literal becomes `18`; a `"modified-block-currency" in NON_READERS` assertion beside the four that exist |
| `tests/doc-health/test_family_enumeration.py` | THE ENUMERATION COLLATERAL (B2): the numeral and family-name assertions at :65, :67, :75, :78, :79, :81, :118, :128, :136, :164, :178 move from twenty-one to twenty-two |
| `tests/doc-health/fixtures/family-enumeration-*/` (7 directories) | the same collateral in fixture spec text — enumeration member list and the three numerals |
| `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md` | the owed `## MODIFIED Requirements` block on "Deterministic check families" |
| `.github/workflows/**`, `report.py`, thresholds, every other family | **UNTOUCHED** |

Both new rows are `add-family-enumeration-check`'s OWN declared code surface
(`openspec/changes/add-family-enumeration-check/proposal.md`:2 names
`tests/doc-health/test_family_enumeration.py`,
`tests/doc-health/fixtures/family-enumeration*/` and
`tests/doc-health/test_lifecycle_scan_set.py`). Editing them is not scope creep:
this change moves the registry those files assert against, and they have no
other way to hear about it.

**No `ALIASES` entry may be added to `family_enumeration.py`**:
`modified-block currency` normalizes mechanically to
`modified-block-currency`, and `test_every_alias_is_load_bearing` fails on an
alias that is not needed.

**The module must not contain the string `_lifecycle_scope(`** —
`test_the_reader_list_is_structural_not_incidental` asserts that call appears in
exactly the four declared scan-set readers and nowhere else in the package.
