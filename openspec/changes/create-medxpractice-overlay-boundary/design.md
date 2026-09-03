## Context

`openPractice` is a standalone public practice-operations repository. The
Medx product needs a private boundary for branding and future Medx-specific
composition without turning the public repository into a Medx-owned fork.
The current workspace contains an untracked openPractice checkout, and the
top-level aggregation has no committed public openPractice submodule to
preserve.

## Goals / Non-Goals

**Goals:**

- Keep public upstream history independent and addressable.
- Pin the current upstream revision through both a gitlink and a manifest.
- Make the private MedxPractice boundary visible in xFactory composition.
- Make MedxFactory's intended practice-operations dependency explicit.
- Keep the layout portable across workstations and fresh recursive clones.

**Non-Goals:**

- Do not fork, copy, or rewrite openPractice history.
- Do not implement practice-operations behavior in MedxPractice yet.
- Do not rename historical MedxFactory ideation vocabulary retroactively.
- Do not remove active unrelated worktrees or dirty workspace files.

## Decisions

1. **Use a nested upstream git submodule.** MedxPractice will contain
   `openPractice/` as a gitlink to `opensoft/openPractice.git`, matching the
   MedxChart composition pattern. The gitlink is the executable pin; a
   committed YAML manifest records the repository, revision, path, and
   relationship for review and tooling.
2. **Use the current upstream checkout revision as the initial pin.** This
   preserves the user's current openPractice state and avoids an implicit
   upgrade during the boundary move.
   - *2026-09-03 — the pin has since fallen behind, BY DESIGN, and re-pinning
     is a deliberate act.* `opensoft/openPractice`'s `main` reads
     `0ec9fca72ecf493e2520e676387f0c3f327cc6e6` and the pin reads
     `9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d` — TWO commits behind
     (`0205901b` "Document reimbursement retention control", then the `#1` merge
     `0ec9fca7`). That distance is what an immutable pin IS, not drift to be
     chased: an upstream commit does not reach this composition until a change
     moves the gitlink and `contracts/openpractice-pin.yaml` together, under
     `domain-descendant-boundary`'s same-commit rule. **NOTED, NOT TASKED —
     there is no re-pin runbook in this repository today**, and writing one is
     neither this packet's work nor a condition of its archive; the note exists
     so a later reader does not read the distance as neglect and does not
     invent a procedure for closing it.
3. **Make MedxPractice an xFactory Medx satellite.** The aggregate will track
   `xFactories/MedxPractice`, and MedxFactory documentation will consume that
   sibling composition boundary. A direct public `openPractice` aggregate pin
   is not retained.
4. **Keep the public repository independent.** The standalone checkout moves to
   the shared projects area with its `.git` history intact. The private repo
   owns only composition and future branded overlay material.
   - *2026-09-03 — the workspace-root layout is recorded HERE as a LOCAL
     CONVENTION, and is deliberately not a requirement.* The canonical
     standalone `openPractice` checkout lives at the projects workspace root
     (beside the xFactory aggregation, not inside it), with its own Git history,
     origin and tracked content unchanged by the relocation. As authored,
     `specs/medxpractice-overlay-boundary/spec.md`'s second requirement swore
     this as a SHALL. It was moved here in this packet's pre-capture fix round
     because **no remote and no CI can settle it**: it is a statement about a
     developer's local filesystem, and the relocation's own success criterion is
     that it leaves no trace in Git — `review/verification-2026-09-03.md` § 9
     says exactly that, and a SHALL nothing can check is a rule that cannot be
     enforced or falsified. What the spec delta keeps is the half a remote
     reading DOES settle: the aggregation reaches `openPractice` only through
     `MedxPractice`'s nested gitlink and carries no direct
     `xFactories/openPractice` entry, confirmed at § 5 of that record. Anyone
     re-laying-out a workstation should follow this convention; nothing refuses
     a tree that does not.

## Risks / Trade-offs

- [Risk] The upstream revision may be unavailable to a fresh clone if the
  public remote does not retain it. → Verify the revision is reachable before
  publishing the MedxPractice and aggregate pins.
  **DISCHARGED 2026-09-03 — re-verified, not merely asserted.**
  `gh api repos/opensoft/openPractice/commits/9526bd9e…` resolves on the PUBLIC
  remote and returns "Initialize spec-driven openPractice repository",
  2026-08-02T20:34:55Z. Recorded with its output in
  `review/verification-2026-09-03.md` § 4.
- [Risk] Existing shared worktrees may still contain historical openPractice
  paths. → Leave active worktrees untouched and report them separately.
- [Risk] Relative aggregate submodule URLs can resolve differently in local
  configuration. → Sync local submodule configuration and verify the published
  remote URLs after updating `.gitmodules`.
  **THIS RISK MATERIALIZED AND WAS REVERSED; recorded 2026-09-03.** The entry
  landed at `3a365206` as `url = ../MedxPractice`. A relative submodule URL
  resolves against whatever URL cloned the SUPERPROJECT, and on the nightly
  runner the superproject is cloned over HTTPS, so it became a plain `https://`
  URL the workflow's `git@`-only token rewrite never touches — every nightly
  from 2026-08-24 died at the clone of these two submodules until
  `opensoft/xFactory` `386e7ee2` (2026-08-25T19:13:51Z) normalized BOTH Medx
  entries to `git@github.com:opensoft/…`. The live entry is
  `git@github.com:opensoft/MedxPractice.git`, and that absolute form is what
  `specs/medxpractice-overlay-boundary/spec.md`'s placement requirement obliges.
  The sibling packet, which made the same choice explicitly as its Decision 2,
  carries the full reversal record at
  `openspec/changes/create-medxchart-overlay-boundary/design.md` § Decision 2;
  it is cited here rather than restated.

## Known limitations (recorded 2026-09-03, not tasked)

- **MedxPractice's own `.gitmodules` names the PUBLIC upstream over SSH.** Its
  single entry reads `url = git@github.com:opensoft/openPractice.git`, so an
  anonymous `git clone --recursive` of MedxPractice cannot initialize the
  nested `openPractice/` checkout even though that upstream is public and would
  clone over HTTPS without credentials. The cost is real but small —
  MedxPractice is itself PRIVATE, so any clone of it is already an
  authenticated one — and the form matches every sibling submodule entry in
  the aggregation, which is what makes one convention rather than two. **This
  is reported as a known limitation and NOT changed by this ratification**: the
  fix would be a commit in `opensoft/MedxPractice`, a repository this packet
  does not edit from here, and it belongs with the follow-on that will next
  touch that tree (`tasks.md` § 5).

## Migration Plan

1. Record the current public openPractice revision.
2. Move the standalone checkout and create MedxPractice around that revision.
3. Publish MedxPractice privately, then add/update the xFactory gitlink.
4. Update MedxFactory documentation and verify recursive pins.
5. Roll back by restoring the previous aggregate pointer if publication or
   validation fails; no public upstream history is rewritten.
