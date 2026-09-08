---
code_surface: openxFactory — ONE NEW artifact and FOUR existing artifacts moved in substance, all in this pull request, none of them a new registered contract row. (1) NEW `contracts/openspec-cli-pin.1.12.0.package-lock.json`, an authored npm `lockfileVersion: 3` lockfile (42,613 bytes) locking the pinned CLI's whole dependency closure — 80 packages, every one carrying a `resolved` URL and an `integrity`, its entry for `@fission-ai/openspec` carrying the pin's own referent `sha512-oFE2Lj7WVSc87nSibk6qe9HjHIOlxhcPAXbPey44DlLvJzBl5+9BZVrNiozOwv++CQhW+MG0kuP1XLZ/uQrrWw==`. (2) `contracts/openspec-cli-pin.yaml`: three new fields — `lockfile:`, `lockfile_integrity: "sha512-aw5lIN45tQq2WZlltd+NtSaxP9Vg3TrFGP3reqI+3bDoE0YZjW+dPIVgdxQLE+Yn0nqwEequaC3+6ff5nkCORA=="`, `lockfile_packages: "80"` — the header's DECLARED SHORTFALL paragraph rewritten as CLOSED with the old text kept as `Was:` history, and a `dependency_closure:` statement inside the `rollback:` entry declaring `1.2.0` UNCOVERED. `version`, `integrity`, `shasum`, `tarball` and every one of the four `dispositions:` are BYTE-UNCHANGED. (3) `scripts/validate-openspec-cli-pin.py`: `pinned_lockfile` (check 1), `verify_lockfile` + `read_lockfile` + `staging_manifest` (check 3, run BEFORE the fetch), `install_locked` REPLACING `install_artifact` — `npm ci --ignore-scripts` in a staging project whose `package.json` is derived from the lockfile's own root entry, never `npm install` — a `cache_key` folding the lockfile's digest into the reuse directory's name, a stamp carrying both addresses, and ONE new refusal code `pin-lockfile-mismatch`. The five original checks, the exit-code semantics, the integrity-before-install ordering, the PATH-mismatch refusal, the disposition mechanism and the absence of a `--verify-only` mode are unchanged. (4) `scripts/install-pinned-openspec-cli.py` AND `scripts/proposal-support.py` — the estate's other TWO callers of `resolve_pinned`, the installer `pytest-suite.yml` runs and the entrypoint through which the ARCHIVE act runs: each gains two calls into the verifier's own `pinned_lockfile`/`verify_lockfile` and passes the bytes on; NO second parser and no copy of the version, the integrity, the lockfile's name or the lockfile's address in either. The archive entrypoint matters most of the three — `openspec archive` writes a ratified delta into canon, and until now the tree that adjudicated an archive could differ from the tree that adjudicated the validation clearing it. (5) `tests/openspec_cli_pin/test_openspec_cli_pin.py`: 93 tests → 124, including `test_every_caller_of_the_resolver_hands_it_the_closure`, which pins the caller list at exactly those three so a fourth fails there rather than in a required check; plus `tests/proposal-support/`, whose two synthetic pins gain synthetic lockfiles and whose two fictional npms learn `ci`. NOT THIS CHANGE'S SURFACE, each for a stated reason: `.github/workflows/openspec-cli-pin-gate.yml` and `.github/workflows/pytest-suite.yml` take NO edit at all, because neither ever named the version and neither now names the lockfile — the invocation they already run installs the closure by reading the pin; the `rollback:` entry gets NO lockfile and says so; no consuming repository's wiring moves, every one of them invoking this same entrypoint from the pinned checkout; and `contracts/manifest.yaml` gains no row, the lockfile being a member of the pin rather than a second published claim.
target_release: implemented (the openxFactory main line). No contract-bundle involvement: `contracts/openspec-cli-pin.yaml` is a registered CONSUMPTION-pin row that deliberately carries no `sha256` (its own comment records why: the file legitimately moves on a bump, a disposition added and a disposition retired), and the lockfile beside it is a member of that pin rather than a separate registered artifact. No digest set moves, no `contract_bundle_version` is spent and no release tag is owed. The archive gate is `release-realization`'s merged-plus-green evidence for a non-empty code surface: this packet's own `openspec-cli-pin` run — a REQUIRED check on `main` since 2026-09-08 — green THROUGH the lockfile path, plus `evidence/dependency-closure-2026-09-08.md`.
Status: draft
---

# Proposal: pin-openspec-cli-dependency-closure

Status: draft
Proposed: 2026-09-08
Origin: Operator ruling, Brett Heap, 2026-09-08T14:14:49Z, first-hand, in
session, on a four-option packet: *"Vendor a lockfile (Recommended)"*. **The
ruling settles WHICH of four exits is taken. It does not ratify this packet's
text**, which carries `Status: draft` and owes a ratification citation from a
separate act.

**THIS IS THE OPEN ITEM #667 DECLARED AND DID NOT CLOSE.** The pin's own header
has said since 2026-09-04 that its referent addresses the CLI's own bytes and
**not** its dependency closure, and has named the repair — *"a lockfile the
publisher does not ship"* — as successor work rather than quietly implying it.
`add-openspec-cli-pin` task 5.2 and `bump-openspec-cli-pin-to-1.12` task 6.4 are
the same shortfall, twice, unticked. This packet closes it and ticks both.

## Why

**A verified tool running over an unverified tree is a verified tool in name
only.** `@fission-ai/openspec@1.12.0` declares TEN runtime dependencies, NINE of
them at caret ranges (`ora ^9.4.1`, `zod ^4.4.3`, `yaml ^2.8.3`, `diff ^9.0.0`,
`chalk ^5.6.2`, `commander ^14.0.0`, `fast-glob ^3.3.3`, `@inquirer/core
^11.2.1`, `@inquirer/prompts ^8.5.2`) and ONE exact (`cross-spawn 7.0.6`). Until
this change, npm resolved those nine ranges **at install time, on every run**, so
two runs of the identical, content-address-verified artifact could adjudicate
this corpus over two different dependency trees — on two machines, or on one
machine a week apart. The pin claimed nothing about that and said so; it is still
the difference between *"we know which tool ran"* and *"we know what ran"*.

**The cost is not hypothetical and the pin already knows what it looks like.**
The whole argument for pinning the CLI at all is measured: at `1.12.0` the same
trees that were clean at `1.2.0` reported 41 pre-existing failures here and 10 in
OpsxFactory, and one ambient `npm install -g` would have reddened two
repositories and stalled every archive in the estate. A transitive dependency
that changes how the CLI *parses*, *sorts* or *reports* does the same thing with
none of the visibility: no version moves, no pin changes, no commit is authored,
and a green gate turns red on somebody else's pull request. `--ignore-scripts`
mitigated the sharpest edge — a dependency's lifecycle script running inside a
gate — and the pin was explicit that mitigation is not repair.

**The estate now depends on this pin in five repositories.** codexFactory,
MedxFactory, LedgerxFactory, AdxFactory and openxFactory itself all run
`scripts/validate-openspec-cli-pin.py` from a pinned openxFactory checkout, and
since 2026-09-08 `openspec-cli-pin` is a REQUIRED check on openxFactory's `main`
(organisation ruleset 22551797, created and ticked as `add-openspec-cli-pin`
task 3.3 by PR #810, merged `95e25409`). Five gates now
resolve nine caret ranges independently. The shortfall stopped being a
declared-and-tolerable footnote at the point the pin became load-bearing.

## What changes

**An authored lockfile is committed beside the pin, its digest is recorded in the
pin, and the install runs through it.**

1. `contracts/openspec-cli-pin.1.12.0.package-lock.json` — generated by
   `npm install --package-lock-only --ignore-scripts` in a staging project whose
   only dependency is `@fission-ai/openspec` at the **exact** pinned version.
   80 packages, every one carrying a `resolved` URL and an `integrity`, so
   nothing in it resolves at install time.
2. `contracts/openspec-cli-pin.yaml` records it in the pin's own address
   vocabulary: `lockfile:` (a BARE NAME, resolving beside the pin and nowhere
   else), `lockfile_integrity:` (npm's `sha512-<base64>` over the file's exact
   bytes, exactly the form `integrity:` uses) and `lockfile_packages:` (the
   corroborating count, on exactly the terms `shasum:` corroborates `integrity:`
   — recorded because a reviewer reads a count, and CHECKED because a recorded
   value nothing verifies drifts).
3. `scripts/validate-openspec-cli-pin.py` hashes the committed lockfile
   **before any registry round trip**, refuses `pin-lockfile-mismatch` on
   disagreement, refuses the same code unless the lockfile's own entry for the
   package carries the pin's `integrity:` — so one pin cannot name two artifacts
   — and then installs with `npm ci --ignore-scripts`, never `npm install`.
   The reuse cache is keyed on the lockfile's digest as well as the artifact's.
4. The pin's header stops saying the closure is open. The old paragraph is kept
   as `Was:` history, because the shortfall is the ARGUMENT for the mechanism and
   deleting it would leave the mechanism looking like decoration.
5. `add-openspec-cli-pin` task 5.2 and `bump-openspec-cli-pin-to-1.12` task 6.4
   are ticked, in the house's amended style, citing this change.

## Impact

- **Affected specs:** `neutral-product-pin` — two ADDED requirements. Nothing is
  MODIFIED, deliberately: see `design.md` § 4.
- **Affected code:** `contracts/openspec-cli-pin.yaml`,
  `contracts/openspec-cli-pin.1.12.0.package-lock.json` (new),
  `scripts/validate-openspec-cli-pin.py`,
  `scripts/install-pinned-openspec-cli.py`,
  `tests/openspec_cli_pin/test_openspec_cli_pin.py`.
- **Affected workflows:** NONE. `.github/workflows/openspec-cli-pin-gate.yml`
  and `.github/workflows/pytest-suite.yml` are byte-unchanged, which is the
  single-source property paying out: neither ever named the version, so neither
  has to learn the lockfile.
- **Affected consuming repositories:** NONE by edit. codexFactory, MedxFactory,
  LedgerxFactory and AdxFactory each already invoke this entrypoint from a pinned
  openxFactory checkout, so each gains the closure at its next `contract_ref`
  advance and none needs a change of its own. Their gates begin installing an
  80-package pinned tree instead of resolving nine ranges, and nothing in their
  wiring notices.
- **What this does NOT claim:** trust-on-first-use of the 79 registry integrity
  values captured when the lockfile was generated; the `1.2.0` rollback entry,
  which is declared UNCOVERED in the pin itself; and the regeneration obligation
  at every bump, which is written into the pin's header and is enforced by the
  verifier refusing on its first run after a referent moves. All three are read
  in `design.md` § 6.
