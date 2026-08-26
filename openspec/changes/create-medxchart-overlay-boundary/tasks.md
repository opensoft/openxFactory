## 1. Preflight and governance

- [x] 1.1 Confirm the current openChart commit, origin, destination absence,
  and the unrelated dirty/staged state of the shared xFactory and MedxFactory
  checkouts.
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

## 4. Verification

- [x] 4.1 Verify the nested MedxChart/openChart gitlink, pin manifest, and
  aggregate MedxChart gitlink all resolve to the expected commits.
- [x] 4.2 Verify no committed file contains a host-absolute path and no direct
  aggregate `xFactories/openChart` submodule remains.
- [x] 4.3 Run targeted YAML/Markdown/Git consistency checks and report any
  pre-existing dirty work left untouched.
