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

## 7. The suite

`python3 -m pytest tests/openspec_cli_pin -q` → **`123 passed`** (was 93).
`python3 -m pytest tests/sequenced_after -q` → **`177 passed`**.
No test skips are added, so `pytest-suite.yml`'s exact `EXPECT_SKIPPED: "21"` is
untouched and its two floors only rise.

## 8. The gate, in CI, on this pull request

openxFactory PR **#813**, run `34240127032`, job *"Verify the OpenSpec CLI pin
and validate the corpus at it"*, on a fresh runner with `--no-cache`:

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (/tmp/openspec-cli-pin-82zgjois/prefix/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
Totals: 100 passed, 2 failed (102 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
```

The executable path is the giveaway that the closure ran: `…/prefix/node_modules/.bin/openspec`
is a PROJECT install produced by `npm ci`, not the `…/prefix/bin/openspec` a
`npm install --global --prefix` used to produce. The REQUIRED check is green
THROUGH the lockfile path, on a machine that had nothing cached.
