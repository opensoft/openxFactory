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
  heading regexes; derive units from each block's lines with the same
  `derive_units`.

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
  the LATER writer; its basis is the declared sibling's OUTCOME (canon's units
  for that requirement, replaced by the sibling's block where the sibling
  MODIFIES it, plus the sibling's ADDED units where it adds), and any addition
  the sibling makes that the declaring block does not carry is one
  `_RESOLUTION_SEVERITY` finding against the DECLARING delta's path.
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

## Registration surface (the same commit — FR-028)

| file | edit |
| --- | --- |
| `scripts/doc_health/families.py` | one name added to the existing `from . import (…)` block; one `FAMILIES` entry `"modified-block-currency": modified_block_currency.fam_modified_block_currency`; one comment recording the deliberate `FAMILY_RESOLUTION` absence, in the shape the four preceding families' comments use; the module docstring's owner list extended to name the twenty-second family |
| `scripts/doc_health/__init__.py` | one `FAMILY_IDS` entry with the twenty-second-family comment, so the family gets its own report section |
| `tests/doc-health/test_lifecycle_scan_set.py` | `"modified-block-currency"` added to `NON_READERS` with its reason; the `len(NON_READERS) == len(FAMILIES) - 4 == 17` literal becomes `18`; a `"modified-block-currency" in NON_READERS` assertion beside the four that exist |
| `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md` | the owed `## MODIFIED Requirements` block on "Deterministic check families" |
| `.github/workflows/**`, `report.py`, thresholds, every other family | **UNTOUCHED** |

**No `ALIASES` entry may be added to `family_enumeration.py`**:
`modified-block currency` normalizes mechanically to
`modified-block-currency`, and `test_every_alias_is_load_bearing` fails on an
alias that is not needed.

**The module must not contain the string `_lifecycle_scope(`** —
`test_the_reader_list_is_structural_not_incidental` asserts that call appears in
exactly the four declared scan-set readers and nowhere else in the package.
