## 1. Governance and upstream capture

- [x] 1.1 Record the current reachable openPractice revision and repository URL.
- [x] 1.2 Create the MedxPractice composition files, pin manifest, and portable
  agent context.

## 2. Repository and aggregate migration

- [x] 2.1 Move the standalone openPractice checkout to the shared projects
  area without rewriting its history.
- [x] 2.2 Publish MedxPractice as a private `opensoft` repository with the
  nested openPractice gitlink.
- [x] 2.3 Add MedxPractice to xFactory and remove any direct public
  openPractice aggregate entry without staging unrelated workspace changes.
  - *2026-09-03 — what the landing commit actually contains, appended and not
    substituting for the original run.* `opensoft/xFactory` `3a365206` ("Add
    MedxPractice composition boundary", 2026-08-23T20:46:44Z) carries SEVEN
    paths: `.gitmodules`, `README.md`, `CLAUDE.md`, `project-register.yaml`,
    the new `xFactories/MedxPractice` gitlink, `xFactories/MedxFactory` (task
    3.2's own pin-sync, accounted for) — **and `openxFactory`, a gitlink move
    from `f879070f` to `a3248684` that NO task in this list accounts for.**
    That is an ordinary submodule pin-sync and not unrelated user work, but it
    is outside the paths tasks 2.3–3.2 describe, so a reader comparing the task
    text to the commit will find one entry the text does not explain. It is
    DISCLOSED rather than glossed. The "remove any direct public openPractice
    aggregate entry" half was a NO-OP by construction, as `design.md` § Context
    says: the aggregation never carried a committed public `openPractice`
    submodule, so `3a365206` adds one entry and removes none.
- [x] 2.4 Update xFactory orientation and project-register documentation.

## 3. MedxFactory integration

- [x] 3.1 Update MedxFactory orientation/composition documentation to use
  MedxPractice as the branded practice-operations boundary.
  - *2026-09-03 — the evidence, named precisely.* ONE FILE, five insertions and
    ZERO deletions: MedxFactory `ccd407895f869a072eb920c2541ea9bc5b4b7723`
    ("Use MedxPractice branded practice overlay", 2026-08-23T20:45:44Z),
    `README.md` only — two lines added to the "MedxFactory uses" list and a
    three-line stanza to the layer ladder, both naming MedxPractice as branded
    practice operations "over its pinned public `openPractice` upstream". That
    is the whole of this change's MedxFactory surface, and the `code_surface`
    front-matter declares it in those terms.
- [x] 3.2 Update the xFactory MedxFactory submodule pointer after the child
  repository change is committed and pushed.

## 4. Verification

- [x] 4.1 Validate the OpenSpec change and verify the nested gitlink/manifest
  revision agreement.
  - *2026-09-03 — RE-VERIFIED at ratification, in
    `review/verification-2026-09-03.md`.* Read from an INDEPENDENT shallow clone
    of `opensoft/MedxPractice` rather than from any shared working tree: the
    nested `openPractice` gitlink and `contracts/openpractice-pin.yaml`'s
    `pin.revision` both read `9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d`, and the
    aggregation's `xFactories/MedxPractice` gitlink reads
    `d8d73195609df3b567643a7bf1252eac352d9996`, equal to that repository's own
    `main`. **Nothing in the repository ENFORCES that agreement today** — it is
    a human reading of two files, and that is § 5's whole subject.
- [x] 4.2 Verify remote reachability, recursive submodule status, and clean
  status for the newly changed repositories.
  - *2026-09-03 — the reachability half RE-VERIFIED; the clean-status half is
    NOT reproducible and is reported as such.* `9526bd9e…` resolves on the
    PUBLIC `opensoft/openPractice` remote today
    (`review/verification-2026-09-03.md` § 4), and the aggregation entry and
    gitlink were re-read through the GitHub API rather than from a local
    superproject (§ 3). The "clean status for the newly changed repositories"
    half was a point-in-time observation of shared working trees on 2026-08-23;
    that state is gone and is not reconstructable, and it is recorded as an
    unreproducible observation rather than restated from memory. What CAN be
    checked about it — the exact file list of each landing commit — is reported
    at task 2.3 above and in the verification record.

## 5. Bound follow-on — the descendant pin validator (GATES ARCHIVE)

**Commissioned 2026-09-03 by the ratifying ruling, under decision 1 option 1.**
Ratification does NOT wait on this group; **ARCHIVE DOES.** The reason is that
this packet's own § 4.1 verification is a one-time human reading of two files
that nothing re-reads: `domain-descendant-boundary`'s pin rule says a descendant
pins the product BY COMMIT TWICE and that its "own validator REFUSES the tree
rather than preferring either" when the two disagree, and **`opensoft/MedxPractice`
has no such validator** — measured 2026-09-03,
`gh api repos/opensoft/MedxPractice/actions/workflows` returns
`{"total_count":0,"workflows":[]}` and the repository's only two rulesets are
ORGANIZATION-sourced ("Copilot Auto-Review All PRs" `8981805`, "Require Code
Owner Review" `18834180`), neither of which requires a status check. Until the
validator exists the boundary this change establishes is asserted rather than
enforced. The pattern to copy is LedgerxWallet's, which is live and named in
`docs/domain-neutralization-candidate-register.md:812-820`:
`tests/validate_pin.py` with fail-closed checks, the REQUIRED `pin-validation`
check, ruleset `21701436`.

**THIS GROUP ANSWERS THE SIBLING'S OPEN 5.5.**
`create-medxchart-overlay-boundary`'s `tasks.md` 5.5 asks, unchecked, whether
`opensoft/MedxPractice` takes the same validator as MedxChart. **The answer is
YES, and it is recorded here because this is the packet that owns MedxPractice.**
The two descendants carry the IDENTICAL two-pin shape — a nested upstream
gitlink plus a `contracts/<product>-pin.yaml` with `schema_version: 1`, a
`<descendant>_<product>_pin` kind, and `relationship: pinned_upstream_composition`
— differing only in the product name and the four literal values that follow
from it, so one validator shape covers one pin shape and a second shape would be
two answers to one question. The DOING of it for MedxPractice is 5.1–5.4 below;
the sibling's 5.5 is discharged by this paragraph and needs no second decision.
**This paragraph is the answer; the sibling's 5.5 checkbox cannot be ticked from
this pull request and is left for the sibling's own pass to tick with a pointer
here.**

- [ ] 5.1 Author `tests/validate_pin.py` in `opensoft/MedxPractice`,
      fail-closed, REFUSING (never warning, never defaulting) when: the nested
      `openPractice` gitlink and `contracts/openpractice-pin.yaml`'s
      `pin.revision` name different commits; either is absent or unparseable;
      the manifest's TOP-LEVEL `schema_version`/`kind` are not `1` /
      `medxpractice_openpractice_pin`, or its `pin:` MAPPING is absent or is
      missing any of `repository`, `remote`, `revision`, `submodule_path`,
      `source_path` and `relationship: pinned_upstream_composition` — the
      manifest is NESTED, two declaration fields above and six pin fields under
      `pin:`, and a validator that reads them flat passes a file that does not
      exist; or the CHECKED-OUT `openPractice/` revision differs from the
      recorded one or is dirty — that last check being the one that catches a
      fork executing at another commit while all three declarations agree.
- [ ] 5.2 Add `.github/workflows/pin-validation.yml` in
      `opensoft/MedxPractice` running 5.1 on pull request and on push to
      `main`, with the check named `pin-validation` to match the LedgerxWallet
      precedent and the MedxChart sibling.
- [ ] 5.3 **[OPERATOR]** Create the branch-protection ruleset on
      `opensoft/MedxPractice`'s default branch (`main`) making `pin-validation`
      a REQUIRED status check, on the shape of ruleset `21701436`. This half is
      Brett's console act; no agent performs it, and an agent-reported "ruleset
      created" without the console act is not evidence. Note that the two
      rulesets already on this repository are ORGANIZATION-sourced and neither
      requires a status check, so this is a repository-level addition and not
      an edit of either.
- [ ] 5.4 Record the ruleset id and one green required run in this change's
      `review/` directory as realization evidence, then and only then open the
      archive gate.
- [ ] 5.5 While that tree is open, close the known limitation `design.md`
      records: MedxPractice's own `.gitmodules` names the PUBLIC
      `opensoft/openPractice` over `git@`, so an anonymous recursive clone
      cannot initialize the nested checkout. **This is a `[ ]` because it is a
      commit in another repository, not because it gates anything** — it does
      NOT gate the archive, which 5.4 alone opens, and it is carried here only
      so the next act on that tree does not have to rediscover it.

## 6. Standing of the boundary itself — reported, not precedent

- [x] 6.1 **MedxPractice is a REPORTED EMPTY BOUNDARY under
      `domain-descendant-boundary` "A descendant is created on its first
      profile, not before" (`openspec/specs/domain-descendant-boundary/spec.md:103-120`),
      and is recorded as such rather than cited.** Its ENTIRE tracked tree at
      `d8d73195` is FIVE entries — `.gitmodules`, `AGENTS.md`, `README.md`,
      `contracts/openpractice-pin.yaml`, and the `openPractice` gitlink — with
      **ZERO openPractice profile artifacts**. That rule's fourth scenario is
      exactly this shape: "WHEN a descendant repository exists carrying no
      profile artifact of the product THEN it is an empty boundary, and it is
      reported rather than cited as precedent for creating more."
      `opensoft/MedxChart` at `68d2f1f5` is the same shape with two `.gitkeep`
      placeholders besides. **Neither is citable as precedent for creating
      another descendant.** The PLACEMENT the sibling's delta ratifies and the
      CREATION rule are different requirements, and ratifying the first grants
      nothing under the second. Both boundaries predate the rule that would have
      gated them (`split-openxwallet-repo`, 2026-08-28), which is why they are
      reported rather than refused.
- [x] 6.2 **This change ratifies SECOND.**
      `create-medxchart-overlay-boundary` ratifies first, on the same ruling and
      in the pull request this one is STACKED on, and it archives first. The
      reason is not courtesy but ownership: the sibling carries the
      `domain-descendant-boundary` placement delta and this packet carries none,
      so the amendment must be on the base branch before the packet that cites
      it can be read against it.
      - *2026-09-03 — what an out-of-order merge would ACTUALLY cost, corrected
        pre-capture.* This note first said the cost was "a broken reference, not
        a wrong rule". **That understated it.** This pull request is STACKED on
        the sibling's; it is retargeted to `main` when the sibling merges, and a
        merge in the other order — this one onto `main` while the sibling's
        delta is still unmerged — would leave promoted
        `domain-descendant-boundary` (`openspec/specs/domain-descendant-boundary/spec.md:80-85`)
        still reading **"REALIZED BUT NOT YET RATIFIED … whose establishing act
        `create-medxchart-overlay-boundary` is still `Status: draft`"** at the
        same moment this packet's ratified
        `specs/medxpractice-overlay-boundary/spec.md` asserts that the placement
        IS ratified and that its ratifying delta exists. That is not a dangling
        path; it is **a ratified change contradicting promoted canon**, which is
        the `document-lifecycle` Explicit delta rule's own defect, and the only
        repair is merging the sibling — writing a second delta here would create
        the two-writers problem the whole arrangement exists to avoid.
      - **NOTHING IN THE REPOSITORY GATES THE ORDER.** No `sequenced_after:`
        declaration is owed and none is present, because the substrate keys on
        CO-MODIFICATION at requirement granularity and these two packets
        co-modify nothing: this one is ADDED-only on a capability it alone
        writes, and the sibling owns the `domain-descendant-boundary` block
        outright. `scripts/validate-sequenced-after.py` therefore has no hook to
        catch a wrong order, and no check anywhere else does either. **The order
        is protected only by this prose, by the pull request body, and by the
        coordinator who merges** — which is worth saying plainly rather than
        leaving a reader to assume a machine is watching.
