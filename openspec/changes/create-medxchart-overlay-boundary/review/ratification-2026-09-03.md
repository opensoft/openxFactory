# Proposal Ratification: create-medxchart-overlay-boundary

Status: record
Kind: report
Decision date: 2026-09-03
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-03 by Brett Heap (openxFactory operator authority) —
in-session, verbatim: *"ratify both, 1 and 1"*.
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
`specs/medxchart-overlay-boundary/spec.md` (THREE ADDED requirements) and
`specs/domain-descendant-boundary/spec.md` (ONE MODIFIED requirement) — with
`openspec validate --strict` and `--all --strict` green (85/85) and the
verification run captured beside this file at `verification-2026-09-03.md`.

This is a CAPTURED record. It is written once and never edited.

---

## 1. The ruling, and what "1 and 1" meant

**"ratify both, 1 and 1."**

Three acts in six words, taken in session on 2026-09-03 over the two Medx
overlay-boundary packets after their review fixes were reported:

- **"ratify both"** — `create-medxchart-overlay-boundary` (this packet) AND
  `create-medxpractice-overlay-boundary` are ratified. Two packets, one word,
  two separate ratification acts recorded in two separate pull requests.
- **The first "1" — decision 1, option 1.** The question put was how to treat
  two descendant repositories that exist, are pinned, are aggregated, and carry
  no profile artifact of the product they pin. Option 1 was taken: **record both
  as REPORTED EMPTY BOUNDARIES**, explicitly NOT citable as precedent for
  creating more (§ 4 below), **and commission each descendant's pin validator
  plus required check as a BOUND FOLLOW-ON that gates ARCHIVE, not
  ratification** (§ 5 below).
- **The second "1" — decision 2, option 1**, which concerns
  `create-medxpractice-overlay-boundary`'s spec delta and is executed by that
  packet's own sibling pull request, landing after this one. **This record
  does not perform it and does not restate it**; naming it here is provenance,
  not authority.

**What the ruling did not do.** It did not merge this pull request, it did not
archive the change, it did not build the validator § 5 commissions, and it did
not move a contract byte — `contracts/` is untouched by the ratified diff, no
bundle is cut, and no release tag is owed. Ratification authorizes; it does not
perform.

## 2. The standing this packet had before today, and why it needed fixing

**Admission is not ratification, and this packet has been the corpus's clearest
example of the difference.** On 2026-08-25, openxFactory **PR #345** — "Admit
the two medx boundary packets: origin metadata only, not a ratification" —
merged at **`f90f3a0872e7b310ed63abb9d1dbb92ac7638635`** (2026-08-25T14:04:20Z),
writing this packet's `.openspec.yaml` origin block on Brett's word *"admit the
two medx boundary packets"*. That block says so in its own text: "THIS IS AN
ADMISSION INTO THE PROPOSAL QUEUE, NOT A RATIFICATION OF CONTENT … the packet
remains `Status: draft`, it carries no ratification citation, and none is owed …
Whether this change's content is ratified is a separate act that has not
happened."

Today is that separate act. **`.openspec.yaml` IS NOT TOUCHED BY IT.** It
records the 2026-08-25 admission, `release-realization`'s origin-retention rule
requires the archive gate to find that declaration unchanged, and mutating it
after ratification is a refusal at the gate. The origin stands as written.

**openxFactory issue #318** — "A drafted-but-unapproved change packet has no
lawful origin shape — every draft is a proposal-origin error until it is
approved" — is the general question this packet's history raised. It remains
**OPEN and unclaimed** (no assignee, no label) as of this ratification. This
record does not close it, does not answer it, and does not treat one packet's
ratification as its resolution: #318 is about every draft in the corpus, and
one packet leaving the draft state settles nothing for the rest.

## 3. The two review reports and how each finding was disposed

Both review reports were verified against live state by their reviewer, and
**every finding was re-verified independently by this lane before it was written
down** — the re-verification is `verification-2026-09-03.md`. Disposition, one
line each, with the file and line where the fix landed.

### P1 — blocking

- **P1-1, the placement delta the promoted spec asked for.**
  `openspec/specs/domain-descendant-boundary/spec.md:76-93` carries the
  `xFactories/` placement as "REALIZED BUT NOT YET RATIFIED … whose establishing
  act `create-medxchart-overlay-boundary` is still `Status: draft`", and its
  second scenario says that WHEN this change archives THEN the requirement "is
  amended by an EXPLICIT DELTA to say so rather than by re-reading".
  **FIXED — the delta is written**: a new
  `specs/domain-descendant-boundary/spec.md` in this packet carries a
  `## MODIFIED Requirements` block (`:12`, `:14`) restating the requirement in
  full with the placement **RATIFIED 2026-09-03** (`:18`) and naming BOTH
  realized placements, `xFactories/MedxChart` and `xFactories/MedxPractice`,
  with their gitlinks. All four canon scenario titles are kept; the two bullets
  and the one body sentence the amendment replaces are declared by a
  `**Removed from canon by create-medxchart-overlay-boundary (2026-09-03):**`
  marker (`:34`) rather than deleted silently, which is the instrument
  `doc-health`'s `modified-block-currency` family exists to require.
  **THIS CHANGE OWNS THE PLACEMENT DELTA AND THE SIBLING CARRIES NONE** — one
  requirement, one writer, so the ordering hazard `release-realization`'s
  sequencing rule governs never arises between the two Medx packets.
- **P1-2, the relative submodule URL this packet decided on was reversed.**
  `specs/medxchart-overlay-boundary/spec.md`'s "relative MedxChart submodule
  URL" scenario and `design.md` Decision 2 promoted a form that broke
  production. **FIXED, AND THE HISTORY IS KEPT RATHER THAN ERASED.** The
  requirement body now obliges the ABSOLUTE `git@github.com:opensoft/MedxChart.git`
  form (`specs/medxchart-overlay-boundary/spec.md:30`) with a new scenario for
  the resolution (`:43`) and a new one for the HTTPS-cloned runner that the old
  form killed (`:49`); `design.md` Decision 2 (`:45`) is retitled and rewritten
  as **REVERSED 2026-08-25, RECORDED HERE 2026-09-03** (`:47`), quoting the
  original decision verbatim, then the reversing commit verbatim, then keeping
  the rejected alternative on the record with the argument for it — because that
  argument is exactly what a later reader would reinvent, and what defeats it is
  not visible from the argument itself. The reversal is `opensoft/xFactory`
  **`386e7ee29fffab36197fbe12fe0139706a715f90`** (2026-08-25T19:13:51Z),
  verbatim: *"A relative submodule URL resolves to whatever cloned the
  superproject … on the nightly runner the superproject is HTTPS, so they
  resolved to plain https:// URLs the workflow's git@-only token rewrite never
  touches, and every nightly since 2026-08-24 died at their clone. Normalize
  both to the git@github.com: form their eighteen siblings use."*
- **P1-3, the remote exists.** `gh repo view opensoft/MedxChart` returns
  `{"pushedAt":"2026-08-23T20:23:45Z","url":"https://github.com/opensoft/MedxChart","visibility":"PRIVATE"}`
  — published hours after this packet wrote that it did not exist.
  **FIXED in all three places**: `proposal.md`'s final Impact bullet
  (`:63`, **CORRECTED 2026-09-03 — the remote EXISTS**, quoting what it used to
  say); `design.md`'s Open Question, struck through and **ANSWERED**
  (`:133`), including the half that was really open — the visibility is
  PRIVATE, so publishing the boundary did not publish the Medx composition; and
  `design.md`'s now-spent `[No remote yet]` risk bullet, marked **DISCHARGED**
  (`:101`). The README row is § 6 below.

### P2 — substantive

- **P2-6, front-matter.** `target_release: implementation_pending` was **not a
  legal value** of the field under `release-realization` (the legal values are
  `implemented` or a named release) and was also false — the topology is merged
  and realized. **FIXED**: `proposal.md:3` now reads `target_release:
  implemented`, with the evidence in the field: MedxChart's `main` is
  `68d2f1f5…`, exactly the aggregation's gitlink; the boundary landed at
  `bed2a69`, corrected at `386e7ee2`. `code_surface` (`:2`) is rewritten from
  the vague "xFactory aggregation and Medx clinical repository topology" to the
  three repositories and their actual paths, and it states plainly that the
  descendant pin validator and its required check DO NOT YET EXIST.
  `proposal.md:39-52`'s "Modified Capabilities: **None**" is replaced by
  `domain-descendant-boundary`, which is what the P1-1 delta modifies.
- **P2-4 / P2-5, Brett's option 1** — the empty-boundary position and the bound
  follow-on. **FIXED**: § 4 and § 5 of this record, and `tasks.md` § 6.1
  (`:127`) and § 5 (`:84`).
- **P2-7, task 4.3's report that was never written.** **FIXED without unticking
  the box** — unticking would assert the checks were not run, and they were.
  A dated note under 4.3 (`tasks.md:71`) points to
  `review/verification-2026-09-03.md` (`Status: record`), into which this lane
  pasted the verification it actually ran today: both `openspec validate`
  invocations with their output, the pin agreement read from an INDEPENDENT
  shallow clone of `opensoft/MedxChart` rather than from any shared working
  tree, the aggregation `.gitmodules` entry and gitlink read through the GitHub
  API rather than from a local superproject, and the host-absolute-path sweep.
  **That record also reports what could NOT be reproduced** — the 2026-08-23
  dirty/staged state of shared checkouts, gone and not reconstructable — as
  unreproducible rather than restated from memory, and it discloses that
  `bed2a69` carries two gitlink paths (`openxFactory`,
  `xFactories/MedxFactory`) the task text does not account for.

### P2-8 / P3-9 / P3-11 — evidence precision

- **P2-8, task 3.3's "documentation links".** The evidence is **one line in one
  file**: MedxFactory `933c5025` ("Point intake plan at MedxChart composition",
  2026-08-23), one insertion and one deletion in
  `ideation/brainstorm/one-patient-intake-vertical-slice-delivery-plan-and-acceptance-gates.md`,
  repointing row P4 of the delivery-plan table. **FIXED by an append-only note**
  at `tasks.md:41`; the plural in the task text is corrected in the note rather
  than by editing a closed task.
- **P3-9, tasks 1.1 and 4.1.** **FIXED by append-only notes** at `tasks.md:6`
  and `tasks.md:59`, both pointing at the re-verification. 4.1's note adds the
  thing the original verification could not say: nothing ENFORCES the pin
  agreement today, which is § 5's whole subject.
- **P3-11, the MedxSoft transfer.** `adopt-medxsoft-repository-identity` names
  **only** `opensoft/MedxFactory` and `opensoft/MedxEHR`, and the aggregation
  commit that executed the operational half — `0c6ea39`, 2026-08-26, "Repoint
  the Medx submodules at MedxSoft, where they now live" — touched exactly those
  two `.gitmodules` entries. **MedxChart's `opensoft/` home is not moved by
  this act or by that one**, and the live entry still reads
  `git@github.com:opensoft/MedxChart.git`. Recorded at `proposal.md:63`.

## 4. The empty-boundary position

**MedxChart is a REPORTED EMPTY BOUNDARY, and this ratification does not make it
a precedent.**

`domain-descendant-boundary`'s fifth requirement (`openspec/specs/domain-descendant-boundary/spec.md:103-120`)
says a descendant "SHALL NOT be created before the domain tree carries at least
one artifact of the product's profile kind … so that an empty boundary is never
stood up as precedent", and its last scenario says that where one exists anyway,
"it is an empty boundary, and it is reported rather than cited as precedent for
creating more."

MedxChart's entire tracked tree at `68d2f1f5` is seven entries — `.gitmodules`,
`AGENTS.md`, `README.md`, `contracts/openchart-pin.yaml`, the `openChart`
gitlink, and two `.gitkeep` placeholders. **Composition metadata only. Zero
openChart profile artifacts.** `opensoft/MedxPractice` at `d8d73195` is the same
shape.

So the position taken under decision 1 option 1 is:

1. **Both boundaries are REPORTED**, here and at `tasks.md` 6.1, with the file
   list that makes the report checkable rather than assertive.
2. **Neither is citable as precedent for creating another descendant.** Anyone
   proposing a new `<Domainx><Product>` repository meets the lazy-creation rule
   on its own terms and gets no help from these two.
3. **The PLACEMENT is what is ratified, and it is a different requirement.**
   Requirement 4 (where a descendant is aggregated) and requirement 5 (when a
   descendant may be created) are separate obligations; ratifying the first
   grants nothing under the second. The MODIFIED delta says this in its own
   text so the distinction survives promotion.
4. **Neither boundary is refused, and the reason is chronology, not
   indulgence.** Both were created on 2026-08-23; the rule that would have gated
   them was ratified with `split-openxwallet-repo` on 2026-08-28. Reporting is
   what the rule itself prescribes for the state it finds.

## 5. The bound follow-on, which gates ARCHIVE

**Commissioned by this ruling; ratification does not wait on it, ARCHIVE does.**
`tasks.md` § 5, unchecked, five items.

The reason is that the pin agreement this packet rests on is verified **by a
human reading two files**, and nothing re-reads them. `domain-descendant-boundary`'s
pin rule requires that when a descendant's gitlink and pin manifest disagree,
"the descendant's own validator REFUSES the tree rather than preferring either,
because an unanswerable question is never an implicit pass." **`opensoft/MedxChart`
has no such validator.** Until it does, this boundary is asserted rather than
enforced, and a silent divergence would be found by whoever next happened to
look.

The pattern is LedgerxWallet's, which is live and recorded at
`docs/domain-neutralization-candidate-register.md:812-820`: `tests/validate_pin.py`
with four fail-closed checks, the REQUIRED `pin-validation` check, ruleset
`21701436`. § 5 commissions the same three parts for MedxChart — the validator
(5.1), the workflow (5.2), and the ruleset, marked **`[OPERATOR]`** (5.3),
because creating a branch-protection ruleset is Brett's console act and an
agent-reported "ruleset created" without it is not evidence. 5.4 records the
ruleset id and one green required run as realization evidence and is what opens
the archive gate. 5.5 decides in the same pass whether `opensoft/MedxPractice`
takes the same validator — it is the sibling realized placement this change's
own delta names and carries the identical two-pin shape, so one answer should
cover one shape.

**This change therefore stays ACTIVE after merge**, which is also what
`release-realization` requires of a change with a code surface: it archives only
on merged code plus green realization evidence, never on landing.

## 6. What this pull request changes, and what it does not

**Changes.** `proposal.md` (front-matter `Status: draft` → `ratified`,
`target_release` → `implemented`, `code_surface` made specific, the citation
line in the record-citing spelling, Modified Capabilities named, the Impact
bullet corrected); `design.md` (Decision 2 rewritten and the reversal recorded,
the risk bullet discharged, the Open Question answered); the existing spec delta
(the URL requirement and two scenarios); the NEW
`specs/domain-descendant-boundary/spec.md` delta; `tasks.md` (append-only notes
plus §§ 5 and 6); this record and `verification-2026-09-03.md`; and the
`README.md` "OpenSpec Records" row, rewritten to RATIFIED 2026-09-03 with the
ruling quoted, the false "the intended `opensoft/MedxChart` remote still
requires a separate publication act" sentence DELETED, and the archive gate
named.

**One file outside the packet moves, and it is bookkeeping rather than
substance**, disclosed rather than folded in: `tests/sequenced_after/test_sweep.py`
carries the LIVE corpus pin, whose own protocol is that it "MOVES WITH the
corpus … in the SAME COMMIT" with a dated MOVEMENT LOG entry saying which
subject moved and why. Adding a `## MODIFIED Requirements` block to an active
change moves four of its readings — `co_modified` 107 → 108,
`active_co_modified` 20 → 21, `sole_modifiers` 49 → 48 (`- 1`: 48 → 47), and
`active_sole` 12 → 11 (`- 1`: 11 → 10) — and moves `change_ids`, `active` and
`archived` **not at all**, because this is a RATIFICATION of a change that
already existed rather than the authoring of a new one. That is a THIRD distinct
cause of that test's failure, different from both causes its assertion messages
name, and the MOVEMENT LOG entry says so. The move was MEASURED BY EXCLUSION,
not inferred: removing only `specs/domain-descendant-boundary/` from this packet
reproduces the prior reading exactly (156 / 107 / 49 / 20 / 12), so this one
delta file is the whole of the difference and no other change moved in the same
window.

**Does not change.** `.openspec.yaml` — see § 2. No existing `tasks.md` checkbox
is flipped in either direction; every task edit is an append. No promoted
specification is edited directly; the amendment to `domain-descendant-boundary`
travels as a delta and promotes at archive, which is what "amended by an
explicit delta rather than by re-reading" asks for. And no contract byte,
schema, manifest row, digest, or release tag moves.

## 7. Sequencing, and the lane

**The sibling ratifies SECOND.** `create-medxpractice-overlay-boundary`'s
ratification pull request follows this one and merges after it. It **cites this
change's placement delta and carries none of its own** — the delta names
`xFactories/MedxPractice` as a realized placement, so the sibling needs no
second writer for one requirement. Decision 2 option 1, which concerns that
packet's own spec delta, is executed there.

**Lane claim.** This pull request is authored and carried by lane
`openxfactory-max001` (max-001, session `5e783e4d`) **through merge**. The lane
AUTHORS and does NOT MERGE: the merge of this pull request is the convener's own
act, as is the merge of the sibling, and neither is performed by this record.
