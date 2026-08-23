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
3. **Make MedxPractice an xFactory Medx satellite.** The aggregate will track
   `xFactories/MedxPractice`, and MedxFactory documentation will consume that
   sibling composition boundary. A direct public `openPractice` aggregate pin
   is not retained.
4. **Keep the public repository independent.** The standalone checkout moves to
   the shared projects area with its `.git` history intact. The private repo
   owns only composition and future branded overlay material.

## Risks / Trade-offs

- [Risk] The upstream revision may be unavailable to a fresh clone if the
  public remote does not retain it. → Verify the revision is reachable before
  publishing the MedxPractice and aggregate pins.
- [Risk] Existing shared worktrees may still contain historical openPractice
  paths. → Leave active worktrees untouched and report them separately.
- [Risk] Relative aggregate submodule URLs can resolve differently in local
  configuration. → Sync local submodule configuration and verify the published
  remote URLs after updating `.gitmodules`.

## Migration Plan

1. Record the current public openPractice revision.
2. Move the standalone checkout and create MedxPractice around that revision.
3. Publish MedxPractice privately, then add/update the xFactory gitlink.
4. Update MedxFactory documentation and verify recursive pins.
5. Roll back by restoring the previous aggregate pointer if publication or
   validation fails; no public upstream history is rewritten.
