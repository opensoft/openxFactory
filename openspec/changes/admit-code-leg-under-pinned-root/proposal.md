---
code_surface: openxFactory (and NOT ONE BYTE OF IT MOVES IN THIS PULL REQUEST). The realization this packet proposes is a LATER pull request in this same repository, authored after ratification, and it edits FOUR files that already exist and adds none: `scripts/estate_inventory.py` (the row-level judge: the `gitlink` carrier bound widened from a `governed` row to a `governed` row OR a `pinned` row admitted by exactly one `pin`, the bound that a row such a carrier admits declares no `governance: governed`, and the pinned-commit read of a verified carrier's `.gitmodules` out of the tree's own object store with every transport refused), `scripts/validate-estate-inventory.py` (its `--estate-tree` mode reads a pinned carrier at the commit the carrier's pin names, and reports NOT RE-CHECKED where the supplied tree cannot produce it), `scripts/estate-repository-inventory.yaml` (FOUR new rows, `opensoft/openDox-spec`, `opensoft/openDox-code`, `opensoft/openXdox-spec` and `opensoft/openXdox-code`, each `governance: pinned` and admitted by a `gitlink` in its root, with the header's `gitlink` definition and population note re-measured), and `tests/estate_inventory/test_estate_inventory.py` (one case per new scenario class, each failing against the unwidened judge before it passes). `scripts/validate-code-surface.py` is NOT edited: its membership arm reads the inventory through `load_inventory` and `evidence_verdicts`, so the four rows reach it exactly as any `pinned` `gitlink` row does. No contract member, no schema, no workflow, no digest and no promoted byte moves. THIS pull request carries the PACKET ONLY: `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, one spec delta carrying ONE `## MODIFIED` block, one README *Active changes* bullet, and the machine-seeded per-change sweep-ledger row in `tests/sequenced_after/corpus-ledger.yaml` that any filing owes.
target_release: implemented (the openxFactory main line). No contract bundle is cut and nothing under `contracts/` is touched: the two pins the widened carrier reads, `contracts/opendox-pin.yaml` and `contracts/openxdox-pin.yaml`, are READ and never edited, no digest set moves, no `contract_bundle_version` is spent and no release tag is owed. The inventory's placement under `scripts/` is `add-estate-repository-inventory`'s ruled D2 and is not reopened here. Under `release-realization` a non-empty code surface archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE rather than on landing, so this packet archives only after its realization pull request has merged and run green, and openxFactory issue 1150 closes THERE.
sequenced_after: []
---

# Proposal: admit-code-leg-under-pinned-root

Status: ratified
Ratified: 2026-09-24, approximately 16:52Z by Brett Heap (openxFactory
repository owner) — verbatim *"(a) recommended for both, ratify when the
draft is green"*, given in the lane's terminal to lane `openxfactory-5`
(session `d7c51922`); no GitHub comment carries the word, which the lane
recorded as a `RULED` entry against `opensoft/openxFactory#1150` in
`opensoft/brett-wip` `lanes/log/openXfactory-5.md` at commit `536b7ecf`; the
condition (the draft head green) was MET at head `f9e3d01124ccdc35dc5686b68ea54cfba25aade3`,
2026-09-24 ~20:17Z.

Proposed: 2026-09-24, in lane `openxfactory-5` (display `openXfactory-5`),
session `d7c51922`, in answer to openxFactory
[#1150](https://github.com/opensoft/openxFactory/issues/1150), filed on
2026-09-23 by lane `openxfactory-4` with three candidate shapes and CLAIMED by
this lane before authoring (2026-09-24T16:36:12Z). This lane realized the
inventory the packet widens (#1119 -> `5e122388`) and archived its packet
(#1149 -> `dd2466ad`).

**RATIFIED 2026-09-24, approximately 16:52Z, by Brett Heap, verbatim "(a)
recommended for both, ratify when the draft is green"**, given in the lane's
terminal to lane `openxfactory-5` (session `d7c51922`) BEFORE this pull
request existed, and recorded as a `RULED` entry against
`opensoft/openxFactory#1150` in `opensoft/brett-wip`
`lanes/log/openXfactory-5.md` (commit `536b7ecf`). The word RULES D1 = option
**(a)** (`design.md` D1) and is otherwise bare, so D4 and D6 take their
recommended options. **THE CONDITION — the draft head green — WAS MET at
head `f9e3d01124ccdc35dc5686b68ea54cfba25aade3`, 2026-09-24 ~20:17Z**: every
check-run `completed` with no failure (14 of 14, including `pytest-suite` run
36051629236, selected=8862 passed=8856 skipped=6 failures=0 errors=0),
Copilot's review present at that exact head (submitted 20:01:12Z, 0 new
findings), and zero unresolved review threads (`tasks.md` § 1.4). **NOTHING
IS PROMOTED, REALIZED OR ARCHIVED BY THIS FILING OR BY THAT WORD:** no file
under `openspec/specs/` is edited, the realization (§ 3) is a LATER pull
request the word now authorizes to be authored, and the archive (§ 5) is a
separate act on a separate word and on merged-plus-green evidence. No merge
word is quoted here: the verbatim word is "(a) recommended for both, ratify
when the draft is green" and nothing further; the register entry's own
reading of what follows ratification is the LANE'S READING and not more
words of Brett Heap's, and the merge of this pull request is a separate act
performed by whoever holds it, never by this lane alone.

**AMENDMENT PENDING RULING (R1, 2026-09-25):** the one-hop parenthetical at
`spec.md`'s `pinned`-row paragraph ("A `pinned` row that is not itself admitted
by a `pin` — every row this clause admits among them — SHALL carry no row's
`gitlink`") is reworded to the direct hop rule in this pull request; it lands
only on Brett Heap's word, before the § 5 archive.

Origin: openxFactory

## Why

**THE ESTATE INVENTORY CANNOT RECORD A CODE LEG NESTED UNDER A PINNED ASSEMBLY
ROOT, SO A `code_surface:` CANNOT NAME WHERE A NEUTRAL PRODUCT'S CODE IS
WRITTEN.**

`scripts/estate-repository-inventory.yaml` admits a repository by exactly five
kinds, closed "because they are exactly the ways this estate has ever named a
repository" (the promoted requirement *The estate's repositories are enumerated
in a governed inventory*). The two neutral products openxFactory pins,
`opensoft/openDox` and `opensoft/openXdox`, are each an ASSEMBLY ROOT whose one
commit names two legs, `spec` and `code`; the product's code is written in
`opensoft/openDox-code` and `opensoft/openXdox-code`. Each kind fails for them,
and each failure is a line of code, not a reading:

| kind | why it cannot admit a leg | where |
| --- | --- | --- |
| `gitlink` | the leg IS a gitlink, but in its root's `.gitmodules`, and the loader refuses every carrier that is not `governed`; both roots are `pinned` | `scripts/estate_inventory.py:966` |
| `pin` | openxFactory never pins or mounts a leg, "which is the assembly root's own job" | `split-opendox-two-layer-product` task 5.1; `contracts/opendox-pin.yaml:113-117`; `contracts/openxdox-pin.yaml:105-108` |
| `workflow` | evidence is read at three structural sites (`jobs.<id>.uses`, a step's `uses:`, a step's `with.repository:`) and never from a `run:` line, and openxFactory reaches the legs only in `run:` lines | `_workflow_names_repository`; `pytest-suite.yml:425`; `openxdox-consumer-gate.yml:239` |
| `change` | the kind admits an ACTIVE ratified change whose realization creates the repository, and the carving change is archived | `archive/2026-09-22-split-opendox-two-layer-product` |
| `root` | admits the aggregation repository alone | `AGGREGATION_ROOT` |

**THE REFUSAL IS MEASURED, NOT INFERRED.** On this branch's base `1d14fee6`, a
scratch inventory carrying `opensoft/openDox-code` as a `pinned` row admitted
by a `gitlink` in `opensoft/openDox` makes `python3
scripts/validate-estate-inventory.py . --inventory <scratch>` exit **2**, the
loader refusing the whole file: *"THE KIND SAYS GOVERNED and means it … Reading
their submodule lists as admissions would let a tree nobody here writes decide
who is in the estate"*. `design.md` D2 answers that sentence rather than
overriding it.

**THE CONSEQUENCE IS ALREADY IN THE CORPUS.** `add-neutral-product-standalone-operability`
(#1144, ratified 2026-09-24) writes its code in the two legs, and its head names
the two ROOTS instead, on Brett Heap's ruling `5804191141` (*"1, name the roots
and file the follow-up"*); its own design says the head "re-points at the legs"
once #1150 lands. Until then a root stands in for a repository the declaration
does not name.

## The measurement, taken before the design

Taken on a fresh clone at `origin/main` `1d14fee6`, by the commands `design.md`
D0 records so they reproduce.

| measure | at `1d14fee6` |
| --- | ---: |
| `pinned` rows admitted by a `pin` (the only carriers the widened kind can reach) | **4** — `openXwallet`, `openDox`, `openXdox`, `openRepoShape` |
| of those, carrying a submodule AT THE COMMIT their pin names | **2** — `openDox` at `dc7aa08f`, `openXdox` at `2f3f857d` |
| legs those two `.gitmodules` name | **4** — `openDox-spec`, `openDox-code`, `openXdox-spec`, `openXdox-code` |
| of those four, already inventory rows | **0** |
| `external` rows admitted by a `pin` (reachable by no carrier, before or after) | **1** — `Fission-AI/OpenSpec` |
| pinned commits equal to openxFactory's own gitlink for the same root | **2 of 2** |
| active declared heads, and distinct identifiers they name | **30** heads, **8** identifiers, **8** carried, **0** refused |

**THE WIDENED KIND ADMITS EXACTLY FOUR REPOSITORIES AND MOVES NO OTHER ROW.**
`openXwallet` and `openRepoShape` carry no submodule at their pinned commits, so
the one-hop reach finds nothing there; no leg is already a row; and no declared
head names a leg yet, so the membership arm's verdict on the corpus is
unchanged on the day the realization lands.

## What changes

**ONE `## MODIFIED` BLOCK, OVER *The estate's repositories are enumerated in a
governed inventory*, WRITTEN OVER CANON.** No active change writes that key, so
the block is SOLE and `sequenced_after: []` is a corroborated root claim.

1. **The `gitlink` bullet gains ONE sentence**: a PINNED ASSEMBLY ROOT's
   `.gitmodules` is a carrier too, read AT THE COMMIT openxFactory's own `pin`
   of that root names, the act of admission being openxFactory's pin and the
   root's gitlink the site it reaches. Every other sentence of the bullet is
   carried word for word; because a bullet is one unit to
   `modified-block-currency`, the old bullet is named in a `Removed from canon
   by admit-code-leg-under-pinned-root (2026-09-24)` marker carried inside the
   block.
2. **ADDED paragraph, the carrier bound**: the carrier's row is `pinned` and is
   admitted by EXACTLY ONE `pin`; an `external` repository's `.gitmodules`
   admits nothing; a row the gitlink admits carries no further row's gitlink of
   its own, so the reach is ONE HOP from an openxFactory pin; a row a pinned
   root admits declares no `governance: governed`; an inventory outside those
   conditions is REFUSED; nothing pins or mounts a leg.
3. **ADDED paragraph, the pinned-commit read**: after the unchanged carrier
   verification, the evidence is the carrier's `.gitmodules` AS OF THE PINNED
   COMMIT, read from the supplied tree's own object store, never its working
   files and never another revision, with NO NETWORK CALL; a tree that cannot
   produce it, or a pin naming no commit, leaves the row NOT RE-CHECKED and
   COUNTED.
4. **THREE ADDED scenarios** — *A code leg is nested under a pinned assembly
   root*, *A gitlink names a carrier outside the two lawful forms*, and *A
   pinned root's gitlink is re-checked at its pinned commit* — placed beside
   the scenarios they extend, and one `**AMENDED BY**` note.

**ELEVEN scenarios** (canon's eight, carried with every bullet, plus three),
counted from the delta file. *A declared repository is judged for membership
against the estate inventory* is NOT modified (`design.md` D6).

## The decision, put for a veto

**THREE DECISIONS WERE PUT, EACH WITH THE RECOMMENDATION FIRST, AND THE FIRST IS
NOW RULED.** They are `design.md` D1, D4 and D6. Brett Heap's word of
2026-09-24 (above) names option (a) for D1 and is otherwise bare, so D4 and D6
take the recommendation when the word applies.

- **D1, the shape — RULED (a).** **(a)**, the recommendation and now the ruled
  option: a `gitlink` whose carrier may be a
  `pinned` row admitted by exactly one `pin`, read at the commit that pin names.
  No kind is added, the closed set stays five, and the leg is still pinned by
  nothing in openxFactory. Against **(b)**: a SIXTH admission kind for a leg of
  a pinned root, which re-states in the admitted row a fact the carrier's row
  already carries, owes the same pinned-commit read under a second name, and
  reopens the closed set for an act that IS a gitlink. **(c) is REJECTED**:
  reading `run:` `git submodule update` lines as workflow evidence reverses a
  rule the reader states on purpose, makes shell text an admission, and names a
  PATH, which still needs the root's `.gitmodules` to become an address.
- **D4, the leg's governance class.** RECOMMENDED: a row a pinned root's
  gitlink admits SHALL NOT declare `governance: governed`, the same bound the
  loader already holds for a `pin`-admitted row. Against: leaving the class to
  the author, unchecked; and requiring exactly `pinned`, which would force a
  third-party repository a root nested into the estate's own class.
- **D6, the delta kind.** RECOMMENDED: one `## MODIFIED` block over the
  enumeration requirement alone. Against: also modifying the membership
  requirement to name the third NOT RE-CHECKED case, which restates 108 lines
  to add a clause its "on the terms the enumeration requirement states" already
  reaches.

## What this packet does NOT do

- **It does not pin or mount a leg.** No `contracts/<leg>-pin.yaml` is filed
  and no gitlink to a leg is added to openxFactory; the root's pin is the whole
  of the evidence, so the carving change's task 5.1 holds.
- **It does not write one inventory row.** The four rows are the realization's
  (`tasks.md` § 3.3), re-measured at its head.
- **It does not re-point #1144's head.** That is `add-neutral-product-standalone-operability`'s
  holder's act, after this realization lands; `tasks.md` § 6.3 records the
  hand-off and takes nothing.
- **It does not add an admission kind or change the governed carrier.** A
  governed carrier's evidence is still read from its working tree, there being
  no commit openxFactory consumes it at (`design.md` D9).
- **It does not fetch.** Every read the delta requires is local; a tree that
  cannot answer without the network is NOT RE-CHECKED.
- **It does not edit one promoted byte, the archive, or a contract member.**
- **It does not close the origin issue.** `code_surface` is non-empty, so the
  archive is a separate act on merged-plus-green realization evidence and a
  separate word, and openxFactory issue 1150 is closed THERE.

Refs #1150
