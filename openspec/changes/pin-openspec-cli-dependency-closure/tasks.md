# Tasks: pin-openspec-cli-dependency-closure

Status: ratified

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in this
pull request or a measurement recorded verbatim in
`evidence/dependency-closure-2026-09-08.md`, taken by this lane on 2026-09-08.
Group 6 is successor work and is not ticked.

**RATIFICATION HAPPENED ON 2026-09-09**, and is recorded in
`review/ratification-2026-09-09.md`. Brett Heap ruled *"Vendor a lockfile
(Recommended)"* on 2026-09-08T14:14:49Z, choosing among four exits — that settled
the APPROACH and did not ratify this text — and then ruled *"ratify 813"* on
2026-09-09T03:19Z, first-hand, which did. Task 5.1 is ticked on the second word
and on nothing else. **5.2 AND 5.3 REMAIN OWED:** ratification is not an archive,
and the validation and realization evidence are re-run at the archive gate rather
than trusted from here. Group 6 is successor work and stays unticked.

### 2026-09-09 — the origin declaration restored to its ratifying bytes (#709 precedent)

**THE ARCHIVE GATE REFUSED THIS PACKET BEFORE IT ARCHIVED IT, AND THE REFUSAL
WAS RIGHT.** `release-realization` § "Origin retention at archive": *"Mutation
of an origin declaration after ratification SHALL be rejected at the archive
gate."* This packet's `.openspec.yaml` `origin.approved_by` was rewritten
**twenty-eight minutes after ratification** by `1921e96a`
(2026-09-08T23:53:51-04:00 = **2026-09-09T03:53:51Z**, *"Finish the
ratification's own bookkeeping: every file in the packet says one thing about
its state (Copilot thread 14)"*), landing on `main` inside the #813 merge
`4c08a7a2`. The ratifying commit is `93ba99f0` — the first commit whose
`proposal.md` declares `Status: ratified`, resolved by the gate's own
`ratifying_commit` walk and not taken on report — and `scripts/proposal-support.py
… archive` refused with `changed keys: approved_by`, exit 2, no bypass flag.

`1921e96a` IS THE SOLE MUTATOR, PROVEN RATHER THAN ASSUMED. Six later commits
touch the file and every one of them is a MERGE that carried bytes and authored
none: each has a parent already at blob `701584a3` and produces `701584a3`
(`a1f08c39`, `7681e409`, `9a67d42c`, `1e8235fc`, `86651a58`, `18a5788d`).
`1921e96a` alone has a single parent — the ratifying commit, at blob `d3e4f174`
— and produced `701584a3`. **No key outside `origin:` moved after ratification**,
so restoring the origin block restores the whole file, and the packet's
`.openspec.yaml` is now byte-for-byte the ratifying commit's: `git diff 93ba99f0
-- <path>` is EMPTY and the blob is `d3e4f174` on both sides.

**THE SENTENCE IS NOT DROPPED — IT IS HERE, WHICH IS ITS PROPER HOME.** What
`1921e96a` added to the origin block, verbatim:

> THE SEPARATE ACT THIS FIELD ONCE SAID WAS OWED HAS HAPPENED: Brett Heap
> ratified the text on 2026-09-09T03:19Z, verbatim **"ratify 813"**, first-hand
> to lane codexfactory-1 with no relay, and the packet now carries
> `Status: ratified` with its citation; the record is
> `review/ratification-2026-09-09.md`. This field still describes the FIRST act,
> which is what `approved_by` means here — who authorized the AUTHORING — with
> the second named so the file does not assert a state that has moved.

**Every word of that is TRUE and none of it is withdrawn.** Ratification
happened exactly as it says; the record is `review/ratification-2026-09-09.md`;
this file's own header carries `Status: ratified` with its citation line, and
task 5.1 is ticked on it. **So read the restored origin block's *"This packet
carries `Status: draft`, carries no ratification citation, and owes one from a
separate act"* as THE STATE AT RATIFICATION, which is the only state an origin
declaration is ever allowed to describe** — an origin block records who
authorized the AUTHORING, is fixed at ratification, and is not a live status
field. The correction was right about the facts and wrong about the file: a
packet that has just been ratified must record that fact in its lifecycle
headers, its tasks and its record — all three of which it did, in the same
commit — and must NOT reach into the one block the retention rule freezes.

THE LESSON, WRITTEN DOWN RATHER THAN LEFT TO THE NEXT LANE. #709's operational
rule was *"a corpus-wide sweep MUST NOT touch a ratified packet's origin
block"*. This mutation was not a corpus-wide sweep — it was **the packet's own
ratification bookkeeping**, a reviewer-prompted pass making every file in the
packet say one consistent thing about its state, which is ordinarily exactly
the right instinct. That is what makes it worth recording: the origin block is
the one file in a ratified packet that must be left saying the OLD thing, and a
consistency sweep is therefore MORE likely to break it than a careless one.

Disposition for this contested-class act, as the retention requirement
requires: **Brett Heap, 2026-09-09T18:03Z, first-hand to lane `codexfactory-1`
(session name `codeXfactory-1`, `session_01VazHnCSe7mh4WUj7E97h8y`), verbatim
"restore per 709"** — taken in the shape issue #709 and its four landed
restorations [#710](https://github.com/opensoft/openxFactory/pull/710)–[#713](https://github.com/opensoft/openxFactory/pull/713)
set: restore byte-for-byte to the ratifying commit, relocate the later text to
the packet's proper home rather than dropping it, and record the disposition in
the commit message.

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
      `LOCKFILE SIZE DRIFT` and — both added 2026-09-08 on Copilot review of
      PR #813 — `LOCKFILE ENTRY UNADDRESSED`
      (`assert_every_entry_addressed()`: every `packages` entry other than the
      root carries a `resolved` AND an `integrity` of its own, and a
      `link: true` local-directory entry is a refusal and not an exemption; the
      three arms above address the file, the pin's own entry and the tree's
      size, and a lockfile can satisfy all three while ONE dependency is fetched
      on the registry's word alone) and
      `LOCKFILE ROOT DECLARES NOTHING TO INSTALL` (`root_dependency_spec()`:
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
      caller list at exactly three. THAT SWEEP PARSES RATHER THAN GREPS
      (rewritten 2026-09-08 on Copilot review of PR #813): it walks the AST of
      every `.py` under `scripts/`, `.github/` and `tests/` — 627 modules — and
      counts only real `Call` nodes, in both spellings (`resolve_pinned(...)`
      and `<module>.resolve_pinned(...)`). The imprecision was also a CEILING:
      a substring reader flags four files, the fourth being the test module
      itself, which names the resolver throughout and calls it never — so the
      sweep could not have been widened past `scripts/` until it read syntax.
      Two controls hold it there, one synthetic and one in situ.
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

- [x] 4.1 `tests/openspec_cli_pin/test_openspec_cli_pin.py`: **93 before this
      packet, 154 now.** COUNTS ARE MEASURED AND DATED, never arithmetic carried
      in prose — a hard-coded delta is a second copy of a number nothing checks,
      which is the defect this whole packet is about, and the four review rounds
      of 2026-09-08/09 moved this figure four times. Every number below is the
      tail of a real run, and § 7 of the evidence packet carries the same
      measurements with the same provenance.

      The added tests cover the closure declaration's shape, the mismatch forms,
      the unreadable/absent lockfile, an unimplemented `lockfileVersion`, a
      malformed lockfile address, a locked entry with no address of its own and a
      `link: true` entry, a root that asks for nothing, the ordering (no npm call
      is spent before a lockfile disagreement is reported), `npm ci` rather than
      `npm install`, the derived staging manifest, the installed tree being
      inspected rather than believed, the cache key and the two-address stamp,
      `--path-mode` saying it did not install the closure, `--tarball` installing
      through it anyway, the caller sweep's two controls, and — offline, against
      the REAL committed files — that the pin and its lockfile agree with each
      other.

      Measured on this branch at the RATIFYING commit, after its merge of
      `origin/main` (`ca4a1558`):
      `python3 -m pytest tests/openspec_cli_pin -q` → **`154 passed`**;
      `tests/proposal-support` → **`95 passed, 2 subtests passed`**;
      `tests/sequenced_after` → **`235 passed`**; the three together →
      **`484 passed, 2 subtests passed`**. With the pinned CLI on PATH exactly as
      the required job supplies it,
      `pytest tests/proposal-support tests/openspec_cli_pin -q` →
      **`249 passed, 2 subtests passed`**. `sequenced_after` moved 195 → 235
      from `main`'s own new tests, none of them this packet's; evidence § 7 says
      so rather than letting the figure read as growth here.

      The whole required suite, from CI rather than a workstation:
      `pytest-suite` run **34297941930** at head **`d538f9d8`** reported
      `selected=10495 passed=10474 skipped=21 failures=0 errors=0`, against
      floors `selected>=7090` and `passed>=7070`.
- [x] 4.2 No test skips, so `pytest-suite.yml`'s exact `EXPECT_SKIPPED: "21"` is
      untouched and its two FLOORS only rise. No `conftest.py` is added.
- [x] 4.3 Prove the entrypoint end to end for real, against the live registry, at
      the gate's own invocation:
      `python3 scripts/validate-openspec-cli-pin.py --repo . --all --no-cache`
      → exit 0, `2 applied`, `0 UNDISPOSITIONED failures`, and the corpus
      totals of the run that produced this line — `Totals: 102 passed, 2 failed
      (104 items)` on this branch at the ratifying commit; the item count rises
      as `main` lands changes and is recorded with its run rather than pinned,
      the load-bearing figures being the two dispositioned failures and the zero
      undispositioned ones. The closure line in the log:
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

- [x] 5.1 Ratification by Brett Heap, recorded in
      `review/ratification-2026-09-09.md`. Verbatim **"ratify 813"**,
      2026-09-09T03:19Z, first-hand to lane `codexfactory-1` (session name
      `codeXfactory-1`), with no relay. It is a SECOND and separate act: the
      2026-09-08 ruling authorized the AUTHORING and named no view on the
      content, which is why this box was held open through four Copilot review
      rounds. The record names the text ratified (head `f2f7ee8d` plus that
      commit's two cosmetic provenance edits), what ratification changes and does
      not, and the four design decisions ratified as written — the `1.2.0`
      rollback UNCOVERED, `pin-lockfile-mismatch` as the single new code, the
      cache-hit boundary, and the two pre-existing host-absolute fixture paths
      left standing.
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
