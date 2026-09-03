## 1. Preflight and governance

- [x] 1.1 Confirm the current openChart commit, origin, destination absence,
  and the unrelated dirty/staged state of the shared xFactory and MedxFactory
  checkouts.
  - *2026-09-03 — what the evidence is, appended at ratification and not
    substituting for the original run.* The commit half is RE-VERIFIED and
    reproduced in `review/verification-2026-09-03.md`: MedxChart's nested
    `openChart` gitlink, `contracts/openchart-pin.yaml`'s `pin.revision`, and
    each other all read `d2376a31dbafa413d8e5ba032f4a2620a75d578e`. The
    dirty/staged half was a point-in-time observation of shared working trees on
    2026-08-23 and is NOT reproducible after the fact; it is recorded as an
    unreproducible observation rather than re-asserted. Nothing was committed
    from those trees by this change — `git show --stat` on the three landing
    commits carries only the paths this packet names.
- [x] 1.2 Record the topology decision and implementation handoff in this
  OpenSpec change without adding host-absolute paths.

## 2. Move upstream repository and create MedxChart

- [x] 2.1 Move the canonical standalone openChart checkout from the xFactory
  submodule directory to the projects workspace root, preserving its `.git`
  directory and user files.
- [x] 2.2 Initialize a new local MedxChart Git repository with repository
  guidance, overlay-boundary documentation, and an explicit openChart pin
  manifest.
- [x] 2.3 Add the current openChart commit as MedxChart's nested submodule,
  normalize its committed URL to the portable upstream remote, and commit only
  MedxChart-owned files.

## 3. Replace aggregate boundary

- [x] 3.1 Replace the xFactory `.gitmodules` entry and gitlink from
  `xFactories/openChart` to `xFactories/MedxChart` using a portable relative
  submodule URL.
- [x] 3.2 Update the xFactory project register and repository documentation to
  identify MedxChart as the Medx clinical satellite and openChart as upstream.
- [x] 3.3 Update affected MedxFactory documentation links and local path
  references without rewriting unrelated dirty files or immutable source-digest
  evidence.
  - *2026-09-03 — the evidence, named precisely.* "Affected MedxFactory
    documentation links" is ONE LINE IN ONE FILE: MedxFactory `933c5025`
    ("Point intake plan at MedxChart composition", 2026-08-23), one insertion
    and one deletion in
    `ideation/brainstorm/one-patient-intake-vertical-slice-delivery-plan-and-acceptance-gates.md`,
    repointing row P4 of the delivery-plan table from `openChart` /
    `../../../openChart/openspec/...` to `MedxChart` /
    `../../../MedxChart/openChart/openspec/...`. The plural in the task text
    overstates it, and the correction is appended rather than made by editing
    the task, which is closed. The "immutable source-digest evidence" half is
    the DELIBERATE NON-ACT `design.md` Decision 4 records: MedxFactory's proof
    evidence still names `openChart` as its provenance and was not laundered
    into MedxChart.

## 4. Verification

- [x] 4.1 Verify the nested MedxChart/openChart gitlink, pin manifest, and
  aggregate MedxChart gitlink all resolve to the expected commits.
  - *2026-09-03 — RE-VERIFIED at ratification, in
    `review/verification-2026-09-03.md`.* All three agree:
    `MedxChart:openChart` gitlink and `contracts/openchart-pin.yaml`
    `pin.revision` both `d2376a31dbafa413d8e5ba032f4a2620a75d578e`; the
    aggregation's `xFactories/MedxChart` gitlink
    `68d2f1f5db932cb5099ceac75dab66316ef22579`, equal to `opensoft/MedxChart`'s
    `origin/main`. **Nothing in the repository ENFORCES that agreement today** —
    that is § 5's whole subject.
- [x] 4.2 Verify no committed file contains a host-absolute path and no direct
  aggregate `xFactories/openChart` submodule remains.
- [x] 4.3 Run targeted YAML/Markdown/Git consistency checks and report any
  pre-existing dirty work left untouched.
  - *2026-09-03 — the report this task promised was never written, and the
    checkbox is NOT being unticked.* The checks were run in-session on
    2026-08-23 and their result is not recoverable; what IS recoverable has been
    re-run now and written down, so the reader gets a report rather than a
    claim. See **`review/verification-2026-09-03.md`** (`Status: record`), which
    carries the actually-executed
    `openspec validate create-medxchart-overlay-boundary --strict`,
    `openspec validate --all --strict`, the three-way pin agreement, the
    aggregation `.gitmodules` entry and gitlink, and the host-absolute-path
    sweep, each with its command and its output. The pre-existing dirty work of
    2026-08-23 is the half that cannot be reconstructed; it is reported as
    unreproducible rather than described from memory.

## 5. Bound follow-on — the descendant pin validator (GATES ARCHIVE)

**Commissioned 2026-09-03 by the ratifying ruling, under decision 1 option 1.**
Ratification does NOT wait on this group; **ARCHIVE DOES.** The reason is that
this packet's own § 4.1 verification is a one-time human reading of two files
that nothing re-reads: `domain-descendant-boundary`'s pin rule says a descendant
pins the product BY COMMIT TWICE and that its "own validator REFUSES the tree
rather than preferring either" when the two disagree, and `opensoft/MedxChart`
has no such validator. Until it does, the boundary this change establishes is
asserted rather than enforced. The pattern to copy is LedgerxWallet's, which is
live and named in `docs/domain-neutralization-candidate-register.md:812-820`:
`tests/validate_pin.py` with fail-closed checks, the REQUIRED `pin-validation`
check, ruleset `21701436`.

- [ ] 5.1 Author `tests/validate_pin.py` in `opensoft/MedxChart`, fail-closed,
      REFUSING (never warning, never defaulting) when: the nested `openChart`
      gitlink and `contracts/openchart-pin.yaml`'s `pin.revision` name different
      commits; either is absent or unparseable; the pin manifest's
      `schema_version`/`kind` are not `1` / `medxchart_openchart_pin`; or the
      CHECKED-OUT `openChart/` revision differs from the recorded one or is
      dirty — the fourth check being the one that catches a fork executing at
      another commit while all three declarations agree.
- [ ] 5.2 Add `.github/workflows/pin-validation.yml` in `opensoft/MedxChart`
      running 5.1 on pull request and on push to `main`, with the check named
      `pin-validation` to match the LedgerxWallet precedent.
- [ ] 5.3 **[OPERATOR]** Create the branch-protection ruleset on
      `opensoft/MedxChart`'s default branch making `pin-validation` a REQUIRED
      status check, on the shape of ruleset `21701436`. This half is Brett's
      console act; no agent performs it, and an agent-reported "ruleset created"
      without the console act is not evidence.
- [ ] 5.4 Record the ruleset id and one green required run in this change's
      `review/` directory as realization evidence, then and only then open the
      archive gate.
- [ ] 5.5 Decide, in the same pass, whether `opensoft/MedxPractice` takes the
      same validator. It is the sibling realized placement this change's
      `domain-descendant-boundary` delta names, it carries the identical
      two-pin shape (`contracts/openpractice-pin.yaml`, `kind:
      medxpractice_openpractice_pin`, nested `openPractice` gitlink
      `9526bd9e`), and the sibling change
      `create-medxpractice-overlay-boundary` cites this delta rather than
      carrying its own. Deciding it here keeps one answer for one shape; the
      DOING of it belongs to whichever packet the decision assigns.

## 6. Standing of the boundary itself — reported, not precedent

- [x] 6.1 **MedxChart is a REPORTED EMPTY BOUNDARY under
      `domain-descendant-boundary` "A descendant is created on its first
      profile, not before" (`openspec/specs/domain-descendant-boundary/spec.md:103-120`),
      and is recorded as such rather than cited.** Its tracked tree at
      `68d2f1f5` is composition metadata ONLY — `.gitmodules`, `AGENTS.md`,
      `README.md`, `contracts/openchart-pin.yaml`, the `openChart` gitlink, and
      two `.gitkeep` placeholders under `openspec/` — with **ZERO openChart
      profile artifacts**. That rule's fourth scenario is exactly this shape:
      "WHEN a descendant repository exists carrying no profile artifact of the
      product THEN it is an empty boundary, and it is reported rather than cited
      as precedent for creating more." `opensoft/MedxPractice` at `d8d73195` is
      the same shape (`.gitmodules`, `AGENTS.md`, `README.md`,
      `contracts/openpractice-pin.yaml`, the `openPractice` gitlink).
      **Neither is citable as precedent for creating another descendant.** The
      PLACEMENT this change ratifies and the CREATION rule are different
      requirements, and ratifying the first grants nothing under the second.
      Both boundaries predate the rule that would have gated them
      (`split-openxwallet-repo`, 2026-08-28), which is why they are reported
      rather than refused.
