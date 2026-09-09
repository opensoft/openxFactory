# Tasks: pin-openspec-cli-dependency-closure

Status: draft

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in this
pull request or a measurement recorded verbatim in
`evidence/dependency-closure-2026-09-08.md`, taken by this lane on 2026-09-08.
Group 6 is successor work and is not ticked.

**RATIFICATION HAS NOT HAPPENED.** Brett Heap ruled *"Vendor a lockfile
(Recommended)"* on 2026-09-08T14:14:49Z, choosing among four exits. That settles
the approach and does not ratify this text. Task 5.1 records ratification when it
happens; nothing below decides it.

---

## 1. The vendored resolution

- [x] 1.1 Generate the lockfile from a CLEAN resolution of exactly the pinned
      artifact: `npm install --package-lock-only --ignore-scripts --no-audit
      --no-fund` in a staging project whose only dependency is
      `"@fission-ai/openspec": "1.12.0"` (root `name: openspec-cli-pin-closure`,
      `version: 0.0.0`). Result committed as
      `contracts/openspec-cli-pin.1.12.0.package-lock.json` — 42,613 bytes,
      `lockfileVersion: 3`, 80 `node_modules/` entries, every one carrying a
      `resolved` URL and an `integrity`.
- [x] 1.2 Assert the resolution against the referent rather than assume it. The
      lockfile's entry for `node_modules/@fission-ai/openspec` carries
      `sha512-oFE2Lj7WVSc87nSibk6qe9HjHIOlxhcPAXbPey44DlLvJzBl5+9BZVrNiozOwv++CQhW+MG0kuP1XLZ/uQrrWw==`,
      which is `integrity:` in the pin, character for character. Had they
      differed the lane was instructed to refuse and would have.
- [x] 1.3 All TEN declared runtime dependencies are locked — the nine caret
      ranges (`ora`, `zod`, `yaml`, `diff`, `chalk`, `commander`, `fast-glob`,
      `@inquirer/core`, `@inquirer/prompts`) and the one exact (`cross-spawn
      7.0.6`) — and so is every package they pull in. Asserted by
      `test_the_real_lockfile_holds_the_pinned_packages_declared_dependencies`.

## 2. The pin records it

- [x] 2.1 `contracts/openspec-cli-pin.yaml` gains `lockfile:` (the BARE NAME,
      resolving beside the pin), `lockfile_integrity:`
      (`sha512-aw5lIN45tQq2WZlltd+NtSaxP9Vg3TrFGP3reqI+3bDoE0YZjW+dPIVgdxQLE+Yn0nqwEequaC3+6ff5nkCORA==`,
      recomputed over the committed bytes by this lane) and
      `lockfile_packages: "80"`. `version`, `integrity`, `shasum`, `tarball` and
      all four `dispositions:` are byte-unchanged.
- [x] 2.2 The header's DECLARED SHORTFALL paragraph is rewritten as CLOSED, dated
      2026-09-08 and attributed to this change, with the whole of the old text
      kept as `Was:` history per the house convention — the shortfall is the
      argument for the mechanism, so deleting it would leave the mechanism
      looking like decoration.
- [x] 2.3 The header records the BUMP PROCEDURE the closure adds: five things now
      move together, and the regeneration command and staging shape are written
      down so a bump does not depend on remembering how the file was produced.
- [x] 2.4 The `rollback:` entry declares `dependency_closure:` UNCOVERED, with
      the consequence stated: a pin returned to `1.2.0` by moving the four
      referent fields alone is REFUSED on its first run rather than installed
      unlocked. Asserted by
      `test_the_real_pin_records_the_previous_referent_as_the_rollback`.

## 3. The verifier is bound to it

- [x] 3.1 `pinned_lockfile()` — check 1, before anything is fetched. Refuses
      `pin-tag-only` for an undeclared or malformed declaration, on the ground
      that unresolved caret ranges ARE the moving reference that code exists to
      refuse. Resolution is `pin_path.parent / name` and admits no traversal.
- [x] 3.2 `verify_lockfile()` — check 3, run BEFORE the registry round trip.
      ONE new refusal code, `pin-lockfile-mismatch`, added to `REFUSAL_CODES`,
      covering `LOCKFILE DIGEST DRIFT`, `LOCKFILE REFERENT DISAGREEMENT` (the
      lockfile locks a different artifact than the pin, or none),
      `LOCKFILE SIZE DRIFT` and — added 2026-09-08 on Copilot review of PR #813
      — `LOCKFILE ROOT DECLARES NOTHING TO INSTALL` (`root_dependency_spec()`:
      the root `""` entry must declare the pinned package under `dependencies`
      or `devDependencies`, `optionalDependencies` and `peerDependencies` NOT
      counting because neither reliably installs; the derived manifest is a
      function of that entry, so a root asking for nothing yields an `npm ci`
      that installs nothing and exits 0). An absent or unparseable lockfile — or
      one declaring a `lockfileVersion` outside `LOCKFILE_VERSIONS`, checked from
      the same review — is `pin-unreadable`, on the division that file already
      draws: a version 4 lockfile does not DISAGREE with the pin, it is
      illegible to this reader.
- [x] 3.3 `install_locked()` REPLACES `install_artifact()`: `npm ci
      --ignore-scripts --no-audit --no-fund` in a staging project whose
      `package.json` is DERIVED from the lockfile's own root entry
      (`staging_manifest()`), so there is no second committed copy of the
      dependency declaration. `--ignore-scripts` stays. The executable is
      `<prefix>/node_modules/.bin/openspec`, still a path this code returns and
      never a name a shell resolves. AND THE TREE IS INSPECTED, not believed
      (`assert_installed_package()`, added 2026-09-08 on the same review): a zero
      exit from `npm ci` is a statement about npm, so the package's own
      `package.json` must be present at `node_modules/@fission-ai/openspec/` and
      must declare the pinned version, BEFORE `assert_reported_version` asks the
      binary anything — one reads what the registry SHIPPED, the other what the
      BINARY SAYS, and a pin is satisfied only when both agree with it.
- [x] 3.4 `cache_key()` folds `sha512(lockfile)[:16]` into the reuse directory's
      name and the `.pin-verified` stamp carries BOTH addresses, so a different
      tree is a different cache entry and a directory stamped for another closure
      is rebuilt rather than reused.
- [x] 3.5 BOTH OTHER CALLERS keep working by CALLING the verifier's own
      `pinned_lockfile`/`verify_lockfile` and passing the bytes to
      `resolve_pinned` — `scripts/install-pinned-openspec-cli.py` (the installer
      `pytest-suite.yml` runs) and `scripts/proposal-support.py` (the entrypoint
      through which the ARCHIVE act runs). No second parser, no `subprocess`, no
      staging project and no copy of the version, the integrity, the lockfile's
      name or its address in any line that runs, in either. Asserted by
      `test_the_installer_carries_no_copy_of_the_pin_at_all` and by
      `test_every_caller_of_the_resolver_hands_it_the_closure`, which pins the
      caller list at exactly three.
      THE ARCHIVE CALLER WAS MISSED ON THE FIRST PASS and this pull request's own
      `pytest-suite` reported it as ten `TypeError`s. Recorded rather than
      quietly repaired, because the miss is also the reason the invariant is now
      a TEST rather than a habit: `openspec archive` writes a ratified delta into
      canon, and until this the tree adjudicating an ARCHIVE could differ from
      the tree adjudicating the VALIDATION that cleared it.
- [x] 3.6 No `--verify-only` mode is added and none is considered; the
      prohibition is a ratified contract decision and
      `test_there_is_no_verify_only_mode` still asserts the absence.

## 4. Tests and proof

- [x] 4.1 `tests/openspec_cli_pin/test_openspec_cli_pin.py`: **93 → 124**. The
      thirty-one cover the closure declaration's shape, the three mismatch forms, the
      unreadable/absent lockfile, the ordering (no npm call is spent before a
      lockfile disagreement is reported), `npm ci` rather than `npm install`, the
      derived staging manifest, the cache key and the two-address stamp,
      `--path-mode` saying it did not install the closure, `--tarball` installing
      through it anyway, and — offline, against the REAL committed files — that
      the pin and its lockfile agree with each other.
      `python3 -m pytest tests/openspec_cli_pin -q` → **`124 passed`**; and,
      with the pinned CLI on PATH exactly as the required job supplies it,
      `pytest tests/proposal-support tests/openspec_cli_pin -q` →
      **`192 passed, 2 subtests passed`**.
- [x] 4.2 No test skips, so `pytest-suite.yml`'s exact `EXPECT_SKIPPED: "21"` is
      untouched and its two FLOORS only rise. No `conftest.py` is added.
- [x] 4.3 Prove the entrypoint end to end for real, against the live registry, at
      the gate's own invocation:
      `python3 scripts/validate-openspec-cli-pin.py --repo . --all --no-cache`
      → exit 0, `Totals: 99 passed, 2 failed (101 items)`, `2 applied`,
      `0 UNDISPOSITIONED failures`, with the closure line in the log:
      `dependency closure openspec-cli-pin.1.12.0.package-lock.json (80
      packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed
      with \`npm ci --ignore-scripts\``.
- [x] 4.4 Prove the INSTALLED TREE IS THE LOCKFILE'S TREE rather than assert it.
      A cached run's `node_modules` was walked and compared against the lockfile:
      80 locked entries, 80 installed entries, name sets identical, ZERO version
      mismatches, spot-checked integrity values agreeing
      (`zod 4.5.4`, `chalk 5.6.2`, `cross-spawn 7.0.6`, `ora 9.4.1`,
      `commander 14.0.3`). Recorded in the evidence.
- [x] 4.5 The two workflow tests are TIGHTENED rather than renumbered: the gate's
      and the test job's non-comment bytes must now carry neither the version,
      nor the integrity, nor the lockfile's address, nor the lockfile's name.
      Both workflows are byte-unchanged, which is what those assertions are for.

## 5. Archive preflight

- [ ] 5.1 Ratification by Brett Heap, recorded in `review/ratification-<date>.md`.
      Not sought by this packet's landing: the 2026-09-08 ruling authorized the
      AUTHORING and named no view on the content.
- [ ] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate pin-openspec-cli-dependency-closure
      --strict` and `--all --strict` green at the archive gate, re-run at that
      time rather than trusted from authoring.
- [ ] 5.3 Realization evidence per `release-realization`: merged, with the
      `openspec-cli-pin` required check green on this pull request THROUGH the
      lockfile path. `target_release` moves no bundle, so no cut is owed.

## 6. Successor work (not this packet)

- [ ] 6.1 An independent attestation of the 79 registry integrity values captured
      in the lockfile — a provenance attestation, a mirrored registry, or a
      second capture from an independent network path compared against this one.
      **Owner: openxFactory.** Design § 6.1 states precisely what this closure
      does and does not claim; nothing here pretends the gap is shut.
- [ ] 6.2 A `1.2.0` lockfile, IF a rollback is ever taken. **Owner: whoever takes
      the rollback**, in the same commit, per the pin's own `dependency_closure:`
      declaration. Not authored speculatively, and design § 6.3 says why.
