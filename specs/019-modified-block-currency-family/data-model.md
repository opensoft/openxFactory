# Data Model: F1 — the modified-block-currency family

**Feature**: `019-modified-block-currency-family` | **Date**: 2026-08-27

Six in-memory entities, no persistence. Nothing here is a schema, a contract
bundle or a stored record: the family reads two documents and emits `Finding`
values through the package's existing dataclass. The entities exist so the
three arms read one derivation instead of three.

---

## 1. `Unit`

One comparable fragment of a requirement. The atom of every comparison.

| field | type | meaning |
| --- | --- | --- |
| `kind` | `"body" \| "scenario-title" \| "scenario-bullet"` | the SAME-KIND constraint's discriminator |
| `text` | `str` | the ORIGINAL text, whitespace-normalized for display; what a finding names |
| `key` | `str` | the comparison spelling: `normalize(text)`, case preserved |
| `scenario` | `str \| None` | for a bullet, the normalized title of the scenario it sits under in ITS OWN document; `None` for body units and for titles |

**Rules**

- `key` is derived by `normalize` (whitespace only). Two units are equal iff
  `kind` and `key` are both equal. Nothing else is consulted — no casefolding,
  no containment, no similarity (FR-008/009/010).
- `scenario` is recorded but is NOT part of equality. It exists for exactly one
  rule: FR-019's "the bullets that scenario carried IN CANON". A block bullet's
  `scenario` is never read for matching, because bullets compare across the
  whole block (FR-012).
- A unit is never empty after normalization; an empty derivation result is
  dropped.
- A paragraph of marker form yields NO unit, in either document (FR-007).
- A line inside a FENCED CODE BLOCK yields no unit and is never read as a
  marker, in either document (ruled 2026-08-27, N7). The delta's own written-out
  marker examples live in a fenced block and promote into canon; without this
  rule the requirement defining the marker declares two of its own units
  removed.

**Kind boundaries.** `kind` is fixed by WHERE the text was found: above the
first `#### Scenario:` → `body`; a `#### Scenario:` heading → `scenario-title`;
a bullet line inside a scenario region → `scenario-bullet`. A bullet in the
BODY region is a `body` unit, not a bullet unit — the delta puts body bullets
in the body's own list (`dh:103-105`).

---

## 2. `Marker`

One declaration paragraph, recognized by form.

| field | type | meaning |
| --- | --- | --- |
| `form` | `"removed" \| "merged"` | which of the two lawful acts |
| `change_id` | `str` | the id in the prefix, as written |
| `date` | `str` | the ISO date in the prefix, as written |
| `names` | `list[str]` | normalized unit names, in document order |
| `destination` | `str \| None` | `merged` only: the normalized destination title |
| `reason` | `str \| None` | everything after the last name's following ` — `, or `None` |
| `paragraph` | `str` | the normalized paragraph, for the "marker names a carried unit" finding |

**Rules**

- Form is decided by the COMPLETE prefix anchor and nothing else (FR-015). A
  paragraph that quotes or templates the form is not a `Marker`.
- `names` never includes `destination` (FR-017).
- `reason` is optional and its absence does not affect form (FR-016).
- A `Marker` is not a `Unit` and never becomes one (FR-007, FR-021).

**Suppression semantics** — the only place a `Marker` acts:

| name resolves to | block carries it | effect |
| --- | --- | --- |
| a canon unit | no | that unit is suppressed |
| a canon unit | yes | the MARKER is reported; nothing is suppressed by that name |
| no canon unit | — | nothing suppressed, nothing reported (R10) |

Plus the scenario-title rule: where `form == "removed"` and a name resolves to
a canon `scenario-title` that the block does not carry AND the block adds no
scenario title canon does not already carry, every canon `scenario-bullet`
whose `scenario` equals that title is also suppressed — unless it appears as a
bullet anywhere in the block, in which case it is carried and reported nowhere
(FR-019). Where the block DOES add a new scenario title, that extension does
not apply (FR-020).

---

## 3. `ActiveBlock`

One `### Requirement:` block inside one active change's
`## MODIFIED Requirements` section.

| field | type | meaning |
| --- | --- | --- |
| `change` | `str` | the active change directory name |
| `capability` | `str` | from the delta path `openspec/changes/<change>/specs/<capability>/spec.md` |
| `title` | `str` | the requirement title as the block writes it |
| `delta_rel` | `str` | repository-relative delta path — the finding path and the disposition key |
| `units` | `list[Unit]` | derived from the block's raw lines |
| `markers` | `list[Marker]` | the block's declaration paragraphs |
| `renames` | `list[tuple[str, str]]` | the change's OWN `## RENAMED Requirements` pairs |
| `standing` | `str \| None` | the change's declared lifecycle standing, read through `corpus.parse_status` + `promotion_fidelity.declared_standing` |

**Rules**

- Discovered from `openspec/changes/*/specs/*/spec.md` with
  `openspec/changes/archive/` excluded, at ANY lifecycle standing (FR-001).
- `standing` is read for ONE purpose: the two-writers arm's `ratified` scoping
  (FR-014). It never gates whether the block is read.
- `renames` belong to the CHANGE, and are carried on the block because
  resolution is per block.

---

## 4. `PromotedRequirement`

| field | type | meaning |
| --- | --- | --- |
| `capability` | `str` | |
| `title` | `str` | as canon writes it |
| `spec_rel` | `str` | `openspec/specs/<capability>/spec.md`, named in every rule text |
| `units` | `list[Unit]` | the same derivation as an `ActiveBlock`'s |
| `scenario_titles` | `list[str]` | ordered, for the completeness arm's report order |

Indexed by `norm(title)` (casefolded — R3), because this is a LOOKUP key, not a
comparison unit.

---

## 5. `WriterSet`

The active changes writing one `(capability, norm(title))`, and what their
proposals say about each other.

| field | type | meaning |
| --- | --- | --- |
| `key` | `tuple[str, str]` | `(capability, norm(title))` |
| `blocks` | `list[ActiveBlock]` | every active MODIFIED writer, sorted by change id |
| `declarations` | `dict[str, set[str]]` | change → the sibling ids its own `proposal.md` names as whole tokens |

**Resolution outcome** — one of four, and the arm reports three of them:

| state | condition | basis | does the resolution arm report? |
| --- | --- | --- | --- |
| single writer | `len(blocks) == 1` | canon | no |
| ordered | ≥2 writers, exactly one declares | the declared sibling's OUTCOME — canon REPLACED by that sibling's MODIFIED block | **NO.** Basis substitution only; the carriage arms report whatever the substituted basis makes uncarried |
| undeclared | ≥2 active RATIFIED writers, none declares | canon | yes, against BOTH blocks |
| mutual | ≥2 declare | canon | yes, once |
| pending on a sibling's ADDED | title absent from canon, added by an active sibling | **none — nothing is compared** | no |

Two rulings of 2026-08-27 live in that table. **A declaration substitutes the
basis and does nothing else** (B3): a separate `_RESOLUTION_SEVERITY` finding
for the sibling's missing additions would report at `warning` the same units the
ledger reports at `info`, and `dh:264` asks for the addition to be reported, not
reported twice. **No basis is synthesized from a sibling's ADDED block** (B4):
`dh:278-280` calls such a title "pending rather than absent", and synthesizing
one would measure all seven of this corpus's MODIFIED-over-a-sibling's-ADDED
pairs and invent roughly six `info` findings.

No folder name, commit timestamp or `created:` field is read in any state
(FR-014).

---

## 6. `Finding` (the package's existing dataclass — FOUR classes of it)

Three arms, four finding classes. The numbers differ on purpose: the arms are
three COMPARISONS between two documents, and the fourth class is a defect in a
DECLARATION.

| class | severity | granularity | rule text names |
| --- | --- | --- | --- |
| scenario-title completeness (arm 1) | `_LAUNCH_SEVERITY` = `warning` | one finding per requirement, naming every omitted title | each omitted title, and the promoted spec read from |
| carriage ledger (arm 2) | `_LEDGER_SEVERITY` = `info` | AT MOST ONE per requirement | every uncarried unit, its kind, and the promoted spec |
| title resolution / ordering (arm 3) | `_RESOLUTION_SEVERITY` = `warning` | one per unresolved block, or per undeclared/mutual ordering | the unresolved title, or the two changes whose ordering is unstated |
| **marker defects** (ruled 2026-08-27, B6) | `_LEDGER_SEVERITY` = `info`, never `error` | one per offending marker | the marker's change id and date, and the unit it names that the block still restates |

The fourth class deliberately does NOT carry the ledger's hedge: a marker naming
a carried unit is wrong with certainty, so "cannot distinguish a rewording from
stale text" would be false of it.

Common fields: `family = "modified-block-currency"`, `repo` from
`ctx.repo_paths`, `path = block.delta_rel`, `action` = the F1 action string
(F4 owns the report-section wording; the finding's own action line ships here
because `Finding` requires it).

`resolution` is left at the dataclass default, because the family is absent
from `FAMILY_RESOLUTION` (R14) — `runner.py`:497-499 then leaves it untouched.

---

## Flow

```text
ctx.repo_paths ──┬─> discover active deltas (glob, archive excluded)
                 │      └─> parse_delta ──> ActiveBlock{units, markers, renames}
                 │
                 └─> read promoted spec per capability (cached)
                        └─> parse_spec_requirements ──> PromotedRequirement{units}

ActiveBlock.title ──> resolve: canon | own RENAMED (compare under OLD name)
                             | active sibling ADDED/RENAMED | UNRESOLVED -> finding

group blocks by (capability, norm(title)) ──> WriterSet ──> basis:
        canon, or the declared sibling's outcome, or canon + an ordering finding

for each (block, basis):
        suppressed = suppression(markers, basis.units, block.units)
        arm 1: basis scenario-titles not carried, minus suppressed  -> warning
        arm 2: basis body units + bullets not carried, minus suppressed -> info
        class 4: markers naming a unit the block still carries       -> info
        (arm 3 already emitted by resolution / WriterSet above)

dispositions (promotion_fidelity.load_dispositions(ctx, FAMILY)) filter by
(repo, delta_rel[, requirement]) before emission; findings are returned sorted.
```

## Validation rules, collected

1. Same-kind exact match after whitespace normalization; no other
   normalization; containment and similarity forbidden. (FR-008/009/010)
2. Backticked spans masked before any split; reported text is the original.
   (FR-004)
3. Marker-form paragraphs are units in neither document, and fenced-block lines
   are neither units nor markers. (FR-007, FR-021, ruling N7)
4. Scenario bullets compare across ALL bullets of the block. (FR-012)
5. At most one ledger finding per requirement. (FR-012)
6. A marker suppresses only units it names AND that are absent. (FR-018)
7. Scenario-title suppression reaches its bullets ONLY in a genuine removal.
   (FR-019/020)
8. Ordering is by declaration; no date, folder or timestamp. (FR-014)
9. Reading scope is every active change; the `ratified` scoping applies to the
   two-writers obligation ALONE. (FR-001, FR-014)
10. Findings land on the active delta's path and name the promoted spec.
    (FR-003)
11. Identical inputs produce byte-identical findings, ordering included.
    (FR-025)
