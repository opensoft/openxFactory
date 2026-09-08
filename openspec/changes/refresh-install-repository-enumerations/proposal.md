---
code_surface: none — this packet's whole diff is governance text in openxFactory: three spec deltas (`repo-boundary-governance` with 3 `## MODIFIED` and 1 `## ADDED`, `shared-contract-ownership` with 2 `## MODIFIED`, `canonical-contract-migration` with 1 `## MODIFIED`), this packet's own three documents plus `.openspec.yaml`, one README "OpenSpec Records" row, and one `tests/sequenced_after/corpus-ledger.yaml` row. NO contract is added or changed — `contracts/manifest.yaml` is untouched, no digest inventory moves, no `contracts/CHANGELOG.md` line is owed and no release tag is owed. NO validator, workflow, script or test changes, and DELIBERATELY NO GENERATOR: the ADDED requirement states that these enumerations are an index refreshed by a named act, and building a derivation for them is the option this packet REFUSES on a measurement (`design.md` D1). No repository is created, admitted, renamed or re-pinned; no submodule pointer moves anywhere; `opensoft/OmniWorker-Install` already exists and is already mounted, and this packet only writes that fact down.
target_release: implemented (the openxFactory main line; governance text only, so realization is the merge itself and no contract bundle is cut). Per `release-realization` an EMPTY code surface archives on landing rather than on merged-plus-green realization evidence — with the one owed act `tasks.md` § 4.1 names, the `repo-boundary-governance` `## Purpose` widening, which by the promoted rule CANNOT be carried in a delta and is therefore applied in the archive commit itself on the `publish-openspec-cli-pin-as-contract-member` § 5.8 precedent.
sequenced_after: [admit-install-repos-to-aggregation]
---

# Proposal: refresh-install-repository-enumerations

Status: draft
Proposed: 2026-09-08
Lane: openxfactory-3 (openXfactory-3)
Origin: openxFactory issue
[#796](https://github.com/opensoft/openxFactory/issues/796) — OQ-9 and task
§ 8.4 of the archived `implement-omniworker-install-repo`, filed AT that
packet's archive (2026-09-08, `d7fbe933`) so the owed box ticked on a naming
rather than staying open forever, and extended the same day by an addendum that
raised the count from three enumerations to FOUR. Admitted to the queue by
Brett Heap, in session on 2026-09-08 (~14:3xZ), recorded on openxFactory issue
[#591](https://github.com/opensoft/openxFactory/issues/591), verbatim: *"do
794, 795 and 796"*.

**THAT WORD ADMITS THE WORK; IT RATIFIES NO TEXT.** It selects three filed
issues to be worked and says nothing about which of #796's two options is
right, what any requirement should say, or whether the widening should happen
at all. Every decision in `design.md` is this packet's proposal and is open to
veto. The packet is `Status: draft` and carries no ratification citation,
which is the lawful unapproved shape `add-drafted-proposal-origin` defined:
drafting provenance in `.openspec.yaml`, no `approved_by`, no `approved_on`.

**AND NOTHING IS REALIZED BY IT.** No promoted specification byte moves — a
change's spec delta is a PROPOSAL about canon, and canon is written by the
archive act. Every box in `tasks.md` is unticked.

## Why

**A fifth install repository exists, and four hand-written enumerations still
describe an estate of two or four.** `opensoft/OmniWorker-Install` was
created 2026-09-05T16:15:48Z (private, default branch `main`) and admitted to
the top-level xFactory aggregation at `installs/omniworker-install` on
2026-09-05 by opensoft/xFactory#274 → merge commit
`648c8bd3fc4717e5b969cd95ea3e0207700e8925`. Its boundary requirement
*"OmniWorker install repository boundary"* was promoted into
`repo-boundary-governance` on 2026-09-08 by opensoft/openxFactory#803 →
`d7fbe933`. So the repository exists, is mounted, and is governed — and the
enumerations that index the install repositories were left exactly as they
were, by that packet's own stated recommendation.

**The deferral was deliberate and it was the right call; what was missing is
the act it deferred to.** `implement-omniworker-install-repo`'s `proposal.md`
declared *"No existing requirement is MODIFIED — in particular the 'Install
repository scope' enumeration is left alone"*, on
`implement-keycloak-install-repo`'s reasoning that two changes sharing one
requirement collide at archive time. This packet is the successor that
deferral named. It is also the first act in this family to CHECK the collision
rather than assume it (`design.md` D2): **the collision does not exist**, and
the measurement is the reason this packet widens now instead of deferring a
fourth time.

**One of the four is THREE repositories behind, and it got that way by exactly
this mechanism.** `repo-boundary-governance`'s `## Purpose` has not moved since
`9ebceeff` (2026-06-26) and still names `openxFactory`, `Hermes-Install` and
`Omnigent-Install` — two install repositories, while the capability's own
*"Install repository scope"* requirement enumerated four and now governs five
boundaries. That is 74 days and three repositories of drift.
`admit-install-repos-to-aggregation` widened the requirement on 2026-08-21 and
left the Purpose alone; #803 added a fifth boundary and left it alone again,
declining the Copilot finding that raised it because #803's packet declared no
owed Purpose act and editing canon prose without one is an unratified edit.
That finding is accepted as correct here and is discharged with the authority
it lacked there: an owed task in a ratified packet (`tasks.md` § 4.1).

## What Changes

- **Widen the enumerations to five, in three capabilities, as SEVEN
  `## MODIFIED` requirements.** Each block restates the promoted requirement
  word for word and changes only the named unit, and each carries a
  `**Removed from canon by refresh-install-repository-enumerations
  (2026-09-08):**` marker naming the replaced sentence or bullet as a code
  span — the reserved form `document-lifecycle` requires so a replacement is
  declared by form rather than left for a reader to infer from a diff. The
  blocks were BUILT from the promoted text programmatically rather than
  retyped, so nothing is dropped by transcription.

  | Capability | Requirement | The unit that moves |
  |---|---|---|
  | `repo-boundary-governance` | Install repository scope | the four-name body sentence → five; the admission paragraph gains `OmniWorker-Install`'s own record (path, remote, opensoft/xFactory#274's merge commit); a third routing scenario is ADDED beside the Hermes and Omnigent ones |
  | `repo-boundary-governance` | Canonical workflow authority | *"Install repo needs policy context"* — its `WHEN` bullet named two |
  | `repo-boundary-governance` | Copy-first migration | *"Canonical policy exists in an install repo"* — its `WHEN` bullet named two |
  | `shared-contract-ownership` | Contract version pinning | *"Install repo consumes a contract"* — its `WHEN` bullet named two |
  | `shared-contract-ownership` | Submodule sequencing | *"Submodule is proposed"* — its `WHEN` bullet named two; widened OPEN-ENDED, see below |
  | `canonical-contract-migration` | Contract provenance and compatibility | *"Contract breaks an adapter"* — its `WHEN` bullet named two runtime adapter families |

- **State the maintenance rule as ONE `## ADDED` requirement**, so the sixth
  repository is a one-line index edit rather than a fifth archaeology
  exercise: *"Install-repository enumerations are an index with a named
  authority"*. It says the enumerations are an INDEX and not the authority for
  which repositories exist; that the authority for existence is the
  aggregation's `installs/` mount list and the authority for scope is each
  repository's own boundary requirement; that the two sets are DIFFERENT (nine
  mounts against five indexed repositories, measured 2026-09-08) so a
  mechanical derivation must declare its filter; and that a change admitting a
  further install repository must either refresh every enumeration or NAME the
  successor that will.

- **One widening is deliberately open-ended and the marker says so.**
  *"Submodule sequencing"*'s scenario governs the act of ADMITTING a
  repository — which by definition is not yet in any index — so a closed
  five-name list there would exempt the sixth admission from the decision
  record the scenario exists to require. It reads *"an install repository —
  … or a later one — as a submodule"*.

- **Declare the `## Purpose` widening OWED, and apply it in the archive
  commit.** `repo-boundary-governance`'s Purpose is prose about a capability,
  not a requirement, and the promoted rule is that a `## Purpose` in a spec
  delta is read ONLY at capability creation and is ignored on any later
  archive. So it cannot travel in this packet's deltas at all. `tasks.md`
  § 4.1 books it as one sentence, in a hunk separate from the promotion,
  exactly as `publish-openspec-cli-pin-as-contract-member` § 5.8 took the
  `neutral-product-pin` widening it had declared owed at its own archive
  (2026-09-08, `d712ce29`).

## What it does NOT change, each with the reason

**Six sites name install repositories and are NOT touched here.** They were
measured, not skipped, and none of them is an index of install repositories:

1. `shared-contract-ownership` *"Contract version pinning"* body — the Gate G0
   handoff sentence requiring `opensoft/xFactory-Hermes-Install` and rejecting
   `FarHeap/Hermes-Install`. That is ONE consumer receipt's remote-identity
   rule, and widening it would say the other four repositories must present a
   Hermes remote. Carried word for word.
2. `shared-contract-ownership` *"Hermes-Install remote is unresolved"* — a
   scenario whose subject is one repository's unresolved remote as a
   CONDITION. Carried word for word.
3. `repo-boundary-governance` *"Install repo scope links"* — its body is
   already general (*"Install repositories SHALL explicitly link back…"*) and
   its two scenarios are per-repository instances, not an index. The same
   obligation for the fifth repository is ALREADY promoted, in
   *"OmniWorker install repository boundary"*'s own first scenario; for the
   third and fourth it is booked in `implement-keycloak-install-repo` and
   `implement-openxpki-install-repo`, which are ACTIVE. Widening it here would
   collide with the two packets #796 asked this one to check for — the one
   place in this capability where that collision WOULD be real.
4. `canonical-contract-migration`'s `## Purpose` — it names one repository and
   hedges it, *"source repos (e.g. Omnigent-Install)"*. An `e.g.` list does not
   go stale, which is precisely what makes `repo-boundary-governance`'s closed
   Purpose different and worth an owed task. **This corrects #796's
   description of enumeration 2:** measured at `main` `131adf11`, that
   capability names `Hermes-Install` NOWHERE and `Omnigent-Install` only inside
   that `e.g.`; the one unit a fifth repository made incomplete is the
   *"Contract breaks an adapter"* bullet, and that is the one this packet
   widens.
5. `contracts/README.md` line 18 (*"Hermes-Install and Omnigent-Install"*) —
   an editorial member of the release inventory. Editing it moves a digest
   `contract-v3.4` records and puts a `release-inventory-drift` finding on
   `main` until the next cut. It is out of scope by class: this packet cuts no
   release. Named as a candidate, unclaimed.
6. `docs/repo-boundary-pilot-plan.md` line 100 — a dated pilot plan describing
   what the pilot's acceptance criteria WERE. A historical record is not an
   index and is not edited to match today's estate.

**And it changes nothing about the repositories themselves.** No boundary is
widened or narrowed — the index sentence *"it neither widens nor narrows the
scope each repository's own `repo-boundary-governance` requirement fixes"* is
carried unchanged and is now stated as a requirement in its own right. No
repository is admitted; `OmniWorker-Install`'s admission already happened and
this packet only records it in the index. `Omnigent-Install` is not renamed,
the `contracts/omnigent/` family is not re-digested, and no `omnigent/` overlay
moves.

## Impact

- **Affected specs**: `repo-boundary-governance` (3 MODIFIED, 1 ADDED),
  `shared-contract-ownership` (2 MODIFIED), `canonical-contract-migration`
  (1 MODIFIED). No capability is created and none is removed.
- **Affected code**: none. No script, workflow, test or contract file is
  touched.
- **Consumers**: no consumer re-pins. The widened triggers name repositories
  that were already governed by the same requirements through their own
  boundary requirements; nothing that passed validation before this change
  fails after it, and nothing that failed before now passes.
- **Collision**: none live, measured — see `design.md` D2. No ACTIVE change
  writes any of the seven requirement keys this packet writes, so
  `release-realization`'s ordered-deltas rule is not engaged and there is no
  archive-time race with either packet #796 named. The sweep-ledger row
  nevertheless reads `class: co-modifier`, because the ledger's corpus includes
  ARCHIVED changes and `admit-install-repos-to-aggregation` wrote the same key
  in August — so this packet DECLARES the sequence it is in,
  `sequenced_after: [admit-install-repos-to-aggregation]`, resolving at depth
  1. Seeding the row moves exactly one row: this change's own.
- **Archive gate**: `code_surface: none`, so this change archives on landing
  per `release-realization`, discharging `tasks.md` § 4.1 (the Purpose
  widening) and § 4.2 (closing #796) in the archive act.

## Ratification

`Status: draft`. Brett Heap's word of 2026-09-08 admitted the work and
ratifies none of the text below. **The decision most worth a veto is
`design.md` D1**: *widen the enumerations now and state the index rule*
(recommended), against *replace the hand lists with a list derived from the
aggregation's `installs/` mount list* — #796's own second option, refused here
on the measurement that the mount list carries NINE paths against an indexed
set of FIVE, so a derivation would enrol `AgentTower`, `CloudPC-Install` and
`xFactory-MedxRootTruth-Install`, which no reviewed act placed under this
requirement, and would duplicate `xFactory-Installer`, which its own *"Neutral
installer repository integration"* requirement already governs.

**Two smaller veto points are carried separately** so each can be refused on
its own: **D3**, the seven-requirement scope — this packet widens FOUR units
#796 did not list (three more bullets in `repo-boundary-governance` and
`shared-contract-ownership`, plus the corrected reading of
`canonical-contract-migration`), on the reasoning that leaving stale pairs
inside the very capabilities being refreshed is the defect the issue's own
addendum names; and **D5**, the open-ended widening of *"Submodule
sequencing"*, the one place where a closed list would be wrong.
