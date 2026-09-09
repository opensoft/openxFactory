# Evidence: the dependency closure, measured 2026-09-08

Status: record

Measured by lane `codeXfactory-1` on 2026-09-08, on branch
`change/pin-openspec-cli-dependency-closure`, against the LIVE npm registry with
`npm 11.19.0` and `node v22.22.2`. Every number below is a command's own output
or a walk of a tree that command produced; nothing is transcribed from a prior
record.

## 1. What was unpinned, restated from the artifact itself

`@fission-ai/openspec@1.12.0` declares TEN runtime dependencies. NINE are caret
ranges and ONE is exact:

```
"@inquirer/core": "^11.2.1",  "@inquirer/prompts": "^8.5.2",
"chalk": "^5.6.2",            "commander": "^14.0.0",
"cross-spawn": "7.0.6",       "diff": "^9.0.0",
"fast-glob": "^3.3.3",        "ora": "^9.4.1",
"yaml": "^2.8.3",             "zod": "^4.4.3"
```

Read from `packages["node_modules/@fission-ai/openspec"].dependencies` in the
generated lockfile, which is the artifact's own manifest as npm resolved it.
There are no `bundledDependencies`.

## 2. The lockfile

```
npm install --package-lock-only --ignore-scripts --no-audit --no-fund
```

in a staging project whose only dependency is `"@fission-ai/openspec": "1.12.0"`
(root `name: openspec-cli-pin-closure`, `version: 0.0.0`).

| fact | value |
| --- | --- |
| committed at | `contracts/openspec-cli-pin.1.12.0.package-lock.json` |
| size | 42,613 bytes |
| `lockfileVersion` | 3 |
| `node_modules/` entries | **80** |
| entries lacking `resolved` or `integrity` | **0** |
| SHA-512 over the file's bytes | `sha512-aw5lIN45tQq2WZlltd+NtSaxP9Vg3TrFGP3reqI+3bDoE0YZjW+dPIVgdxQLE+Yn0nqwEequaC3+6ff5nkCORA==` |

The entry for the pinned package:

```json
"node_modules/@fission-ai/openspec": {
  "version": "1.12.0",
  "resolved": "https://registry.npmjs.org/@fission-ai/openspec/-/openspec-1.12.0.tgz",
  "integrity": "sha512-oFE2Lj7WVSc87nSibk6qe9HjHIOlxhcPAXbPey44DlLvJzBl5+9BZVrNiozOwv++CQhW+MG0kuP1XLZ/uQrrWw==",
  "bin": { "openspec": "bin/openspec.js" },
  "engines": { "node": ">=20.19.0" }
}
```

**That `integrity` is `integrity:` in `contracts/openspec-cli-pin.yaml`,
character for character.** The verifier refuses `pin-lockfile-mismatch` if the
two ever part, and
`test_the_real_committed_lockfile_verifies_against_the_real_pin` reconciles them
offline on every developer's machine.

## 3. The package count: 80, measured three ways

The brief this lane worked from recorded 94. Re-measured, it is **80**, and the
three measurements agree:

| measurement | result |
| --- | --- |
| `npm install --global --prefix … --ignore-scripts <tarball>` (the install path this change replaces) | `added 80 packages in 6s` |
| the generated lockfile's `node_modules/` entry count | 80 |
| a walk of the `node_modules` tree `npm ci` produced | 80 |

`npm` itself printed `added 80 packages` for both install shapes. 80 is what the
pin records in `lockfile_packages:` and what `verify_lockfile` checks.

## 4. `npm ci` installs the lockfile's tree, walked rather than asserted

A cached run's install prefix was walked and every installed package compared
against the lockfile entry of the same name:

```
locked entries   : 80
installed entries: 80
names identical  : True
version mismatches: []
  @fission-ai/openspec     locked 1.12.0     installed 1.12.0     integrity sha512-oFE2Lj7WVSc87nSibk6qe9H…
  zod                      locked 4.5.4      installed 4.5.4      integrity sha512-sC95tT5iHHH9gtpj6A81kh+…
  chalk                    locked 5.6.2      installed 5.6.2      integrity sha512-7NzBL0rN6fMUW+f7A6Io4h4…
  cross-spawn              locked 7.0.6      installed 7.0.6      integrity sha512-uV2QOWP2nWzsy2aMp8aRibh…
  ora                      locked 9.4.1      installed 9.4.1      integrity sha512-6VlU9MLXbjVQD04AZCMX28h…
  commander                locked 14.0.3     installed 14.0.3     integrity sha512-H+y0Jo/T1RZ9qPP4Eh1pkcQ…
```

Note `zod 4.5.4` against the declared `^4.4.3` and `commander 14.0.3` against
`^14.0.0`: those are exactly the ranges that used to resolve at install time, and
they are now facts in a committed file rather than a function of the clock.

The derived staging manifest, written by `staging_manifest()` from the lockfile's
own root entry — no second committed copy of the dependency declaration:

```json
{
  "name": "openspec-cli-pin-closure",
  "version": "0.0.0",
  "private": true,
  "dependencies": { "@fission-ai/openspec": "1.12.0" }
}
```

`staging_manifest()` REFUSES rather than deriving that block empty
(`pin-lockfile-mismatch`, `LOCKFILE ROOT DECLARES NOTHING TO INSTALL`, added
2026-09-08 on Copilot review of PR #813). A root entry that declared no
dependency would have produced a well-formed manifest asking for nothing, an
`npm ci` that installed nothing and exited 0, and a gate green over a tree it
never built; `optionalDependencies` and `peerDependencies` do not satisfy the
check, because npm may skip the first silently and the second is satisfied by the
rest of the tree. The install then INSPECTS what it built —
`node_modules/@fission-ai/openspec/package.json`, present and at the pinned
version — before `assert_reported_version` asks the binary anything.

The reuse directory's name and its stamp:

```
@fission-ai__openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef-6b0e6520de39b50a
.pin-verified:
  sha512-oFE2Lj7WVSc87nSibk6qe9HjHIOlxhcPAXbPey44DlLvJzBl5+9BZVrNiozOwv++CQhW+MG0kuP1XLZ/uQrrWw==
  sha512-aw5lIN45tQq2WZlltd+NtSaxP9Vg3TrFGP3reqI+3bDoE0YZjW+dPIVgdxQLE+Yn0nqwEequaC3+6ff5nkCORA==
```

The artifact's address and the closure's, both — so a directory built for one
tree cannot be served in another's name.

## 5. The gate, end to end, at its own invocation

```
$ python3 scripts/validate-openspec-cli-pin.py --repo . --all --no-cache
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (…/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
…
Totals: 99 passed, 2 failed (101 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

**Exit 0**, through the lockfile path, with the two standing dispositions applied
and nothing new. The two findings are the pin's existing openxFactory pair; this
change adds no disposition, retires none, and touches the list not at all.

## 6. The gate is a REQUIRED check, which is why the timing is what it is

Verified against the live GitHub API on 2026-09-08, after
`add-openspec-cli-pin` task 3.3 landed:

```
$ gh api /repos/opensoft/openxFactory/rules/branches/main --jq '[.[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context]'
["signed-execution-chain-gate","lane-line","openspec-cli-pin","wallet-validation","pytest-suite","lane-line","release-tag-gate"]

$ gh api /orgs/opensoft/rulesets/22551797 --jq '.name, (.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context)'
openxFactory pin-gate (require openspec-cli-pin)
openspec-cli-pin
```

The ruleset was created and task 3.3 ticked by **PR #810, merged to `main` as
`95e25409`** on 2026-09-08 — the same day as this packet, by a sibling lane.
That is the fact that ends option 4 ("accept the shortfall as declared"): a
DECLARED GAP IN A REQUIRED CHECK is a declared gap in the thing that stops
merges. This packet's own `openspec-cli-pin` run is therefore the enforced gate,
and § 5 above is that gate's own log line.

**A NOTE ON THE TWO QUOTED LOG LINES BELOW.** Both are reproduced VERBATIM except
for one elision: the runner's host-absolute prefix is replaced by an ellipsis
(`…/`), because Principle IV of `.specify/memory/constitution.md` forbids a
host-absolute path in a committed file and evidence that carries one is evidence
that stops being portable the moment the runner is recycled. The elided prefixes
were an ephemeral `mktemp` directory and the Actions runner's `_temp`
respectively; nothing the lines are quoted FOR lives in either. What each line is
quoted for is its TAIL, and the tails are byte-exact. (Redacted 2026-09-08 on
review of PR #813.)

## 7. The suite

`python3 -m pytest tests/openspec_cli_pin -q` → **`154 passed`** (was 93; 123
before the Copilot-review rounds of 2026-09-08, which added the
`lockfileVersion`, malformed-address, root-declaration, installed-tree and
`running_lines` cases in round 5, the entry-address cases in round 6, and the two
caller-sweep controls in round 7).
`python3 -m pytest tests/proposal-support -q` → **`95 passed, 2 subtests`**.
`python3 -m pytest tests/sequenced_after -q` → **`195 passed`**.
No test skips are added, so `pytest-suite.yml`'s exact `EXPECT_SKIPPED: "21"` is
untouched and its two floors only rise.

## 8. The gate, in CI, on this pull request

openxFactory PR **#813**, run `34240127032`, job *"Verify the OpenSpec CLI pin
and validate the corpus at it"*, on a fresh runner with `--no-cache`:

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (…/openspec-cli-pin-<mktemp>/prefix/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
Totals: 100 passed, 2 failed (102 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

The executable path is the giveaway that the closure ran: `…/prefix/node_modules/.bin/openspec`
is a PROJECT install produced by `npm ci`, not the `…/prefix/bin/openspec` a
`npm install --global --prefix` used to produce. The REQUIRED check is green
THROUGH the lockfile path, on a machine that had nothing cached.

The INSTALLER's own CI line, from `pytest-suite`'s "Install the pinned OpenSpec
CLI for tests/proposal-support" step on the same pull request — the second of the
three callers, resolving the same closure into the runner's `$GITHUB_PATH`:

```
install-pinned-openspec-cli: @fission-ai/openspec@1.12.0 verified against its content address (integrity sha512-oFE2Lj7WVSc87nSi…) and installed at …/_temp/openspec-cli-pin/@fission-ai__openspec-1.12.0-c844543999f673cdd72445879b86a4abea4c07ef-6b0e6520de39b50a/node_modules/.bin/openspec, over the pinned dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages, lockfile_integrity sha512-aw5lIN45tQq2WZll…, installed with `npm ci --ignore-scripts`).
```

The cache directory's name carries BOTH addresses — the artifact's shasum
`c844543999…` and the closure's `6b0e6520de39b50a` — which is the cache key doing
its job on a real runner.

## 9. THE THIRD CALLER, MISSED AND THEN CAUGHT BY THIS PULL REQUEST'S OWN GATE

`resolve_pinned` gained two required arguments. The estate has THREE callers of
it, not two, and the third — `scripts/proposal-support.py`, the entrypoint
through which the ARCHIVE act runs — was missed on the first pass. This pull
request's `pytest-suite` reported it as ten `TypeError`s
(`resolve_pinned() missing 2 required positional arguments: 'lockfile_bytes' and
'lockfile_integrity'`), which is the required check working exactly as intended.

It is recorded here rather than quietly repaired for two reasons. **The first is
that the archive act is where the closure matters most**: `openspec archive`
writes a ratified delta into canon, and until this fix the tree that adjudicated
an ARCHIVE could differ from the tree that adjudicated the VALIDATION that
cleared it — same day, same machine, nine caret ranges resolved twice. They are
one tree now. **The second is that the miss is the reason the invariant is now a
TEST**: `test_every_caller_of_the_resolver_hands_it_the_closure` enumerates the
callers under `scripts/`, pins the list at exactly those three, and requires each
non-defining caller to reach the closure through the verifier's own functions and
to restate no literal. A fourth caller added later fails there rather than in
somebody else's required check.

Measured after the fix, with the pinned CLI on PATH exactly as the required job
supplies it:

```
$ pytest tests/proposal-support tests/openspec_cli_pin -q
192 passed, 2 subtests passed
```

## 10. THE REQUIRED SUITE, GREEN, ON THE FIXED HEAD

`pytest-suite` run `34247095390`, the pinned-triple step's own arithmetic:

```
selected=10413 passed=10392 skipped=21 failures=0 errors=0
floors: selected>=7090 (margin 3323) passed>=7070 (margin 3322) skipped==21
```

`EXPECT_SKIPPED` is EXACT and it did not move: this change adds no skip, which is
what task 4.2 claims and this is the measurement of it. Both floors only rose.
All nine checks on the pull request are green.

## 11. THE COPILOT ROUNDS OF 2026-09-08, AND WHICH FINDINGS WERE REAL

Nine review threads stood on PR #813 across three rounds — seven, then one on the
head that fixed them, then one on the head that fixed that. Recorded here rather
than only in the threads, because two of them are findings about this verifier's
*stated contracts*, one is a finding about this file, one is a gap between what a
test guarded and what the running code enforced, and one is a test whose reader
could not tell a call from a sentence about one.

| # | Subject | Disposition |
| - | ------- | ----------- |
| 1 | `read_lockfile()` refuses "the lockfileVersion 2/3 shape" and never read `lockfileVersion` | **REAL, fixed.** `LOCKFILE_VERSIONS = (2, 3)` is the declaration; the reader refuses `pin-unreadable` outside it. A stated contract the code did not keep. |
| 2 | `resolve_pinned()` gained required arguments and a caller still used the old signature | **ALREADY FIXED** when the thread was written: raised 14:55:59Z, and the third caller was bound at 15:48:05Z (commit `152faba9`, § 9 above), with `test_every_caller_of_the_resolver_hands_it_the_closure` pinning the caller list at three. |
| 3 | `base64.b64decode(..., validate=True)` raises `binascii.Error`, which `except (ValueError, TypeError)` misses | **NOT A DEFECT.** `binascii.Error` IS a `ValueError` subclass, so both decode sites already produced `PinRefusal('pin-tag-only')` on impossible padding rather than a traceback. The type is now NAMED at both catch sites anyway — a guard a reader must derive from the exception hierarchy is a guard the next reader will re-raise — and a parametrized regression test asserts the refusal and the subclass relation. |
| 4 | `running_lines()` claims to remove "every comment" and removes only whole-line ones | **REAL in the CLAIM, not in the check.** The docstring is narrowed and the asymmetry stated: a whole-line comment is prose, a line carrying a trailing `#` is a line that RUNS, and the only failure the strictness can produce is a false positive fixed by moving a note onto its own line. Stripping inline comments would WIDEN the surface on which a second copy of the pin may sit, which is the surface those two tests exist to keep empty. Pinned by `test_running_lines_keeps_an_inline_comment_and_drops_a_whole_line_one`. |
| 5 | This evidence file embedded host-absolute runner paths | **REAL, fixed.** Both quoted log lines are elided to `…/`; Principle IV of `.specify/memory/constitution.md` forbids a host-absolute path in a committed file. The tails, which are what the lines are quoted for, are byte-exact. (Two host-absolute paths remain in `tests/openspec_cli_pin/fixtures/*.json` — captured CLI output landed on `main` by `bump-openspec-cli-pin-to-1.12`, untouched by this pull request and not this packet's to redact.) |
| 6 | Duplicate `import os` in `tests/proposal-support/test_proposal_support.py` | **REAL, fixed.** |
| 7 | `staging_manifest()` may derive a manifest with no dependencies, so `npm ci` installs nothing | **REAL, fixed, and in two places.** `root_dependency_spec()` refuses `pin-lockfile-mismatch` (`LOCKFILE ROOT DECLARES NOTHING TO INSTALL`) from `verify_lockfile` — before the fetch, on the ordering rule the rest of check 3 follows — and from `staging_manifest` itself, which is reachable on its own. `assert_installed_package()` then reads the installed tree before the binary is asked what it is. |

### Round 6, on the head that fixed those seven

| # | Subject | Disposition |
| - | ------- | ----------- |
| 8 | `verify_lockfile()` never checks that the OTHER locked entries carry `resolved` and `integrity`, so a regenerated lockfile with an unaddressed entry passes check 3 and `npm ci` fetches unverified bytes | **REAL, fixed.** `assert_every_entry_addressed()` refuses `pin-lockfile-mismatch` (`LOCKFILE ENTRY UNADDRESSED`) unless every `packages` entry other than the root carries BOTH. The finding is exact: the three arms above it address the file, the pin's own entry and the tree's size, and all three pass while one dependency has no integrity to be verified against. |

`resolved` is required BESIDE `integrity`, not instead of it — the integrity says
which bytes, the resolved URL says where they came from, and an entry with an
address and no origin is a package `npm ci` must go and find, which is the
range-resolution this whole change closes, one entry deep. **A `link: true` entry
is a refusal and not an exemption**: npm writes it for a workspace or a `file:`
dependency, the entry points at a local directory with no content address and no
origin, and its contents are whatever is on that disk at install time. Nothing
generates one here, which is why the rule is written down while it costs nothing.
The ROOT (`""`) entry is exempt because it DECLARES the tree rather than
belonging to it, and the exemption is asserted by a test rather than left to the
loop's shape.

The property was already true of the committed file and asserted by
`test_the_real_lockfile_locks_the_pinned_artifact_and_resolves_nothing` (80 of 80
entries carry both). That test guards THIS repository at pytest time; the finding
was that the VERIFIER did not enforce it, and the verifier is what runs in every
consuming repository and in the gate, where no pytest does.
`test_every_locked_entry_of_the_real_lockfile_is_addressed` now asserts the
verifier's own verdict on the real file, and two parametrized cases (an entry
missing `integrity`, an entry missing `resolved`) plus a `link: true` case cover
the refusal — each also asserting that no registry round trip is spent reaching
it.

### Round 7, on the head that fixed round 6

| # | Subject | Disposition |
| - | ------- | ----------- |
| 9 | `test_every_caller_of_the_resolver_hands_it_the_closure` found callers by substring (`"resolve_pinned(" in text`), so a docstring, comment or string-literal mention counted as a caller | **REAL, fixed.** `resolver_calls()` walks the AST and counts only real `ast.Call` nodes, in both spellings — `resolve_pinned(...)` (`ast.Name`) and `<module>.resolve_pinned(...)` (`ast.Attribute`, matched on the attribute, so a verifier bound under another name is still seen). |

**The imprecision was also a CEILING on the sweep's reach, and that is the part
worth recording.** Measured on the fixed head over `scripts/`, `.github/` and
`tests/` — **627 Python modules**:

```
substring would flag: scripts/install-pinned-openspec-cli.py
                      scripts/proposal-support.py
                      scripts/validate-openspec-cli-pin.py
                      tests/openspec_cli_pin/test_openspec_cli_pin.py
AST finds callers   : scripts/install-pinned-openspec-cli.py
                      scripts/proposal-support.py
                      scripts/validate-openspec-cli-pin.py
```

The fourth is the TEST MODULE ITSELF, which names the resolver throughout and
calls it never. A text reader could not have been pointed at `tests/` without
immediately reporting it as a fourth caller and demanding it bind a closure — and
the cheapest way to make that green would have been to delete the explanation,
which is `tests/import_scan.py`'s own argument for parsing rather than grepping,
quoted in the new reader's docstring. So the sweep now reads syntax AND covers
all three trees; the two changes are one change. `.github/` holds no `.py` today
and is swept anyway, because a workflow that grew an inline script is exactly the
caller nobody thinks to look for.

Two controls keep it there: `test_the_caller_sweep_reads_calls_and_not_mentions`
(a synthetic module that mentions the name in a docstring, a comment and a string
literal — asserted to be flagged by a substring reader and NOT by this one — plus
a synthetic module that calls it both ways), and
`test_this_very_module_names_the_resolver_and_is_not_a_caller`, the same control
in situ on a real committed file. The sweep also REFUSES an unparseable module
rather than skipping it, a skipped file being a hole that reports itself as a
pass.

`pin-lockfile-mismatch` rather than `pin-unreadable` for thread 7, and
`pin-unreadable` rather than `pin-lockfile-mismatch` for thread 1, on the ONE
division this file already draws and `design.md` § 2.3 states: a MISMATCH is a
disagreement between two well-formed, readable statements, with a remedy
(regenerate the lockfile at the pinned version); `pin-unreadable` is the state in
which no comparison can be reached at all. A root that asks for the wrong thing
disagrees. A `lockfileVersion` this reader has never implemented is illegible.
