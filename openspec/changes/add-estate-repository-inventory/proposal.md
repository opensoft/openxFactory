---
code_surface: openxFactory (and NOT ONE BYTE OF IT MOVES IN THIS PULL REQUEST). The realization this packet proposes is a LATER pull request in this same repository, authored after ratification, and it is THREE NEW FILES plus ONE NARROWING EXTENSION plus ONE TEST PACKAGE: `scripts/estate-repository-inventory.yaml` (NEW, the enumeration, one row per repository, carrying `schema_version` and `kind` like every other governed YAML here), `scripts/estate_inventory.py` (NEW, the reader and the row-level judge, in the shape `scripts/code_surface.py` uses and reading through the same shipped strict loader), `scripts/validate-estate-inventory.py` (NEW, the house validator CLI in the shape every other `scripts/validate-*.py` uses), ONE MEMBERSHIP ARM added to `scripts/validate-code-surface.py` so the declaration scan and the membership scan report in one run rather than in two a caller may run singly, and `tests/estate_inventory/` (NEW, the tests that pin them, each failing against the unbuilt arm before it passes). NO OTHER EXISTING FILE IS EDITED: `scripts/code_surface.py`'s grammar is untouched, `scripts/scope_globs.py`'s derivation is untouched, no existing test is edited, renamed, flipped or deleted, no workflow changes (the required `pytest-suite` already runs `tests/`), no contract member, no schema, no report field, no digest and no promoted byte. THIS pull request carries the PACKET ONLY: `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, one spec delta carrying ONE `## MODIFIED` block and TWO `## ADDED` requirements, one README *Active changes* bullet, and the machine-seeded per-change sweep-ledger row in `tests/sequenced_after/corpus-ledger.yaml` that any filing owes.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves, no `contract_bundle_version` is spent and no release tag is owed. THE PLACEMENT IS WHAT MAKES THAT TRUE AND IT IS A RULED DECISION, NOT A CONVENIENCE: `design.md` D2 puts the inventory under `contracts/policies/` as the alternative and costs it, the cost being that a file under `contracts/` is a bundle surface whose every correction owes a manifest entry, a recomputed digest and an additive minor, against a fact that moved NINETEEN times in seventy-four days. Under `release-realization` a non-empty code surface archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE rather than on landing, so this packet archives only after its realization pull request has merged and run green, and openxFactory issue 1087 closes THERE.
sequenced_after: []
---

# Proposal: add-estate-repository-inventory

Status: draft

Proposed: 2026-09-18, in lane `openxfactory-5` (display `openXfactory-5`),
session `651195c7`, in answer to openxFactory
[#1087](https://github.com/opensoft/openxFactory/issues/1087), which was FILED
at the landing of PR #1076 (the archive of `gate-code-surface-declarations`, merge
`5dd0a8dc`) as the successor that packet's `tasks.md` § 6.1 named, and which this
lane CLAIMED before authoring. **NO RATIFYING WORD HAS BEEN GIVEN.** Nothing here
is ratified, promoted, realized or archived by this filing; `tasks.md` § 1 is
Brett Heap's act and is not ticked by this lane.

Origin: openxFactory

## Why

**THE GATE KNOWS WHAT A REPOSITORY NAME LOOKS LIKE AND HAS NO WAY TO KNOW
WHETHER THE REPOSITORY EXISTS.**

`gate-code-surface-declarations` landed a grammar for `code_surface:` and stated
its own bound in the ratified text, in the promoted requirement *Code-surface
declaration grammar is gated*:

> The gate SHALL judge the identifier's SHAPE and SHALL NOT judge its MEMBERSHIP
> of any inventory, for the measured reason that this repository defines no
> inventory of the estate's repositories to resolve against.

Its `tasks.md` § 6.1 named the successor and refused to build it:

> AN INVENTORY OF THE ESTATE'S REPOSITORIES. Without one the gate judges a
> repository identifier's SHAPE and never its MEMBERSHIP, so a plausible
> misspelling passes.

**THE MISSPELLING IS NOT HYPOTHETICAL AND IT IS ALREADY IN THIS TREE.** § *The
measurement* below records it: `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`
names `opensoft/LegalxFactory`, an address the provider answers 404 for, which
no `.gitmodules` carries and no pin names. Two more rows in that same file name
repositories at addresses that survive only through a provider redirect, and this
repository's own transfer map states, in its own header, that a redirect is a
grace period and not an identity.

## The measurement, taken before the design

**NOTHING BELOW RESTS ON A NUMBER ANYBODY TYPED.** Taken on a fresh clone at
`origin/main` `ad089e8a`, by the methods `design.md` D0 records so they
reproduce. The candidate inventory is built from FIVE naming sites, and the
figure that matters is the last row of the second table.

| source | what it yields |
| --- | ---: |
| `opensoft/xFactory` `.gitmodules` (via `gh api repos/opensoft/xFactory/contents/.gitmodules`) | **23** submodules |
| the aggregation repository itself, which no `.gitmodules` can name | **1** |
| a GOVERNED DomainxFactory's own `.gitmodules`, where the estate NESTED rather than sibling-linked | **11** nested gitlinks in 6 repositories, naming **7** no other site names |
| `contracts/*-pin.yaml` `source_repository:` / `repository:` | **7** pins naming **6** distinct repositories, **2** of them no submodule |
| `.github/workflows/` dispatching at a named ref | **1**, already a submodule |
| a RATIFIED active change whose realization CREATES a repository | **1**, in the window before any tree can name it |
| **candidate inventory** | **33 rows** |

**THE THIRD SITE WAS ADDED IN REVIEW, AND SAYING SO IS PART OF THE
MEASUREMENT.** A first filing read `gitlink` as the AGGREGATION's `.gitmodules`
alone. Copilot's review of PR #1101 showed that reading leaves the provisional
row of the fifth kind with no way to discharge — the realization that creates
`opensoft/LedgerxWallet` NESTS it under `ledgerXfactory/LedgerxFactory`, not
under the aggregation — so the kind was widened to a gitlink in ANY governed
estate repository, the evidence naming the repository that carries it, and the
measurement was RE-TAKEN rather than reasoned about. It found SIX further
members the narrow reading missed (`openChart`, `openPractice`, `MedxAvatar`,
`LedgerxAvatar`, `MedxEHR-spec`, `MedxEHR-code`), which is why the candidate
carries 33 rows and not 27.

And against that candidate, the population the gate actually judges:

| measure | at this head |
| --- | ---: |
| ACTIVE proposals | **49** |
| declaring `code_surface:` | **49** |
| declaring `none` | **7** |
| named by the closed register (head unreadable by design) | **8** |
| declaring a readable repository list | **34** |
| DISTINCT repository identifiers those 34 heads name | **6** |
| of those 6, carried by the candidate inventory | **6** |
| of those 6, refused by the membership arm on the day it lands | **0** |

**THAT LAST ROW IS THE FACT THAT MAKES THIS ACT SAFE, AND IT IS THE FACT THE
PREDECESSOR COULD NOT HAVE.** `design.md` D1 of `gate-code-surface-declarations`
rejected membership resolution as "fatal as things stand", on the reasoning that
"there is no inventory, so on the day it landed the gate would refuse all 41
non-`none` declarations". Measured now against a candidate inventory that exists:
the six identifiers the corpus declares are `openxFactory`, `xFactory`,
`openAvatar`, `opensoft/LedgerxWallet`, `opensoft/Keycloak-Install` and
`opensoft/OpenXPKI-Install`, and **all six resolve**. The predecessor's fatal cost
was a property of having no inventory, not a property of membership resolution.

**AND THE INVENTORY IS WIDER THAN ANY ONE SITE, WHICH IS WHY IT IS A FILE AND NOT
A DERIVATION.** The aggregation's `.gitmodules` reaches 23 of the 33 rows.
`opensoft/openRepoShape` is pinned here and is in no `.gitmodules`.
`Fission-AI/OpenSpec` is pinned here and is not of this estate at all.
`opensoft/xFactory` is the aggregation root and is in nobody's `.gitmodules`
because a superproject is not its own submodule. SEVEN MORE are nested inside a
governed DomainxFactory and appear in no aggregation `.gitmodules`, no pin and no
workflow. And `opensoft/LedgerxWallet` is the row that shows why a CHANGE is a
naming site of its own: it was declared by the RATIFIED
`create-ledgerxwallet-overlay-boundary` on 2026-08-27, one day BEFORE that
realization created and nested it. **A code surface is FORWARD-LOOKING, it names
where a change WILL write, so a repository the estate is creating is declared
before any tree can name it.** That window forced a fifth admission-evidence
kind, `change`, carrying a PROVISIONAL row that expires into a finding at its
change's archive (`design.md` D1.1); without it the membership arm would refuse a
ratified packet inside the window. What DISCHARGES such a row is the nested
gitlink the realization files, which is why `gitlink` reaches any governed estate
repository and not the aggregation alone. A rule that read one site would miss
members a rule reading another site would find.

## What changes

**ONE `## MODIFIED` BLOCK AND TWO `## ADDED` REQUIREMENTS.**

1. **`## MODIFIED` over *Code-surface declaration grammar is gated*.** ONE PARAGRAPH
   MOVES and the other nine and all ten scenarios are restated exactly as canon
   states them. The paragraph that moves is the one that says membership is not
   judged, and it moves because its own stated REASON stops being true at this
   packet's realization. **THE MODIFICATION IS OWED AND IS NOT A PREFERENCE**:
   the promoted sentence's `SHALL NOT` is unconditional in its text, so an
   ADDED-only delta would leave canon carrying "the gate SHALL NOT judge
   membership" beside "membership SHALL be judged", which is a contradiction and
   not a layering. `design.md` D3 retains the ADDED-only shape as the alternative
   and costs it.
2. **`## ADDED`: *The estate's repositories are enumerated in a governed
   inventory*.** The file, its per-row fields, the five admission-evidence kinds
   (the fifth measured into existence at `design.md` D1.1; `gitlink` reaching any
   governed estate repository, its evidence naming the carrier), the three
   governance classes, unique bare names, current addresses only, the BOUND ON
   THE EVIDENCE RE-CHECK (`design.md` D1.2: the four in-tree kinds on every run
   with no network call, a `gitlink` only against a supplied working tree and
   otherwise reported as NOT RE-CHECKED), and the measured reason it is not a
   `contracts/` member. EIGHT scenarios.
3. **`## ADDED`: *A declared repository is judged for membership against the
   estate inventory*.** The gate extension: an identifier the inventory does not
   carry FAILS CLOSED; a bare name resolves by row and never by provider; a former
   address REPORTS rather than refuses because it is interpretable; an `external`
   row refuses and says so; a REGISTERED declaration is not judged and the arm
   does not fall back; **an inventory row nothing names is a FINDING**; the
   archive is read and never judged. NINE scenarios.

**TWENTY-SEVEN scenarios in all** (10 + 8 + 9), counted from the delta file
rather than carried.

## The decision, put for a veto

**FOUR DECISIONS ARE PUT, EACH WITH THE RECOMMENDATION FIRST.** They are
`design.md` D2, D3, D4 and D5, and each carries the alternatives that were put
and the cost of taking them.

- **D2, where the inventory lives.** RECOMMENDED: `scripts/estate-repository-inventory.yaml`,
  beside the code-surface register, `target_release: implemented`. Against:
  `contracts/policies/estate-repository-inventory.yaml`, a manifest member owing
  an additive minor per correction, against a fact that moved nineteen times in
  seventy-four days. Against: no file at all, deriving membership live from
  `.gitmodules` on every run, which makes a required check depend on a network
  call and on read access to a private repository.
- **D3, MODIFIED or ADDED-only.** RECOMMENDED: one `## MODIFIED` block over the
  promoted grammar requirement, restated verbatim but for the paragraph whose
  reason this packet removes. Against: ADDED-only, which leaves the contradiction
  standing.
- **D4, what a row means for a repository that is pinned rather than governed**,
  which is the authority question #1087 carries. RECOMMENDED: three governance
  classes (`governed` / `pinned` / `external`) and an `admitted_by:` naming one of
  FIVE evidence kinds — `gitlink`, `pin`, `workflow`, `root`, `change` — so the
  inventory RECORDS an admission and PERFORMS none. Against: a flat membership
  list, which cannot refuse a surface declared in a repository the estate does
  not author, and cannot carry the provisional row a repository-creating change
  needs.
- **D5, the disposition of a former address in an active head.** RECOMMENDED:
  REPORT, naming the current address. Against: refuse, which teaches an author
  nothing the finding does not.

## What this packet does NOT do

- **It does not admit or retire one repository.** Every candidate row records a
  naming act already taken in a governed tree; the realization writes the record
  and takes no admission.
- **It does not edit one promoted byte.** This pull request touches no file under
  `openspec/specs/`; the MODIFIED block is a DELTA and promotes at the archive.
- **It does not correct the three divergent rows it measured.** `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`
  is a contract member whose correction owes a bundle, and one of its rows is the
  subject of the active `adopt-medxsoft-repository-identity`. Named as a
  successor (`tasks.md` § 6.1), not smuggled in here.
- **It does not resolve a name by asking the provider.** The measurement did, once,
  to establish that the six declared identifiers exist; the gate never does, for
  the reason the delta states.
- **It does not touch the archive**, the closed register, the grammar, or
  `scope_globs`'s derivation.
- **It does not close the origin issue.** `code_surface` is non-empty, so the
  archive is a separate act on merged-plus-green realization evidence and a
  separate word, and openxFactory issue 1087 is closed THERE.

Refs #1087
