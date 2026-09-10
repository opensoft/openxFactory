# Evidence: the pinned CLI's lockfile integrity values, attested 2026-09-10

Status: record
Kind: report

Task **6.1** of
[`pin-openspec-cli-dependency-closure`](../openspec/changes/archive/2026-09-09-pin-openspec-cli-dependency-closure/tasks.md)
asked for an independent attestation of the registry integrity values the
vendored lockfile captured, and recorded that nothing had attested them. This
is that attestation, produced by `scripts/attest-openspec-cli-pin-lockfile.py`
— read its module header for what the two links prove and, precisely, what
they do not.

Captured 2026-09-10T00:47:39Z against `https://registry.npmjs.org` with `npm
11.19.0` and `node v22.22.2`, at repository revision
`9c0e2cda4afeefc098044323fdc784ac47577697`. Every number below is a command's
own output.

## The subject

- pin: `contracts/openspec-cli-pin.yaml` at `@fission-ai/openspec@1.12.0`
- lockfile: `openspec-cli-pin.1.12.0.package-lock.json`, verified against the pin's
  `lockfile_integrity:` before anything was attested
- content-addressed entries: **80** — 79 dependencies plus the
  pinned CLI, whose own value the pin already corroborates

## Link A — the recorded values, re-captured and compared

Every one of the **80** recorded `integrity` values EQUALS the value the
registry serves for that exact `name@version` today. The registry serves a
signature over **80** of them, and every keyid it signed with is published at
`https://registry.npmjs.org/-/npm/v1/keys`.

```
entries compared:                80
distinct name@version fetched:   71
disagreements:                   0
```

## Link B — `npm audit signatures` over the locked tree

Installed with the clean-install verb through the committed lockfile, the
staging manifest derived from its own root entry:

```
audited 80 packages in 2s

80 packages have verified registry signatures

31 packages have verified attestations
(use --json --include-attestations to view attestation details)
```

```
npm audit signatures exit: 0
invalid:                   0
missing:                   0
```

**31** of the 80 entries additionally carry a Sigstore provenance attestation,
verified in the same run; the rest carry the registry's signature alone, which
attests what npm published rather than how it was built.

## Per-entry record

| package | version | registry agrees | signed | provenance |
| --- | --- | --- | --- | --- |
| `@fission-ai/openspec` | `1.12.0` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/ansi` | `2.0.8` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/checkbox` | `5.2.5` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `12.0.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/confirm` | `6.3.2` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `12.0.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `11.2.1` | yes | yes | — |
| `@inquirer/editor` | `5.3.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `12.0.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/expand` | `5.1.5` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `12.0.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/external-editor` | `3.0.5` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/figures` | `2.0.9` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/input` | `5.1.6` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `12.0.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/number` | `4.2.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `12.0.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/password` | `5.2.2` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `12.0.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/prompts` | `8.7.2` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/rawlist` | `5.3.5` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `12.0.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/search` | `4.3.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `12.0.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/select` | `5.2.5` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/core` | `12.0.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `@inquirer/type` | `4.1.1` | yes | yes | https://slsa.dev/provenance/v1 |
| `@nodelib/fs.scandir` | `2.1.5` | yes | yes | — |
| `@nodelib/fs.stat` | `2.0.5` | yes | yes | — |
| `@nodelib/fs.walk` | `1.2.8` | yes | yes | — |
| `ansi-regex` | `6.3.0` | yes | yes | — |
| `braces` | `3.0.3` | yes | yes | — |
| `chalk` | `5.6.2` | yes | yes | — |
| `chardet` | `2.2.0` | yes | yes | https://slsa.dev/provenance/v1 |
| `cli-cursor` | `5.0.0` | yes | yes | — |
| `cli-spinners` | `3.4.0` | yes | yes | — |
| `cli-width` | `4.1.0` | yes | yes | — |
| `commander` | `14.0.3` | yes | yes | — |
| `cross-spawn` | `7.0.6` | yes | yes | — |
| `diff` | `9.0.0` | yes | yes | — |
| `fast-glob` | `3.3.3` | yes | yes | — |
| `fast-string-truncated-width` | `3.0.3` | yes | yes | — |
| `fast-string-width` | `3.0.2` | yes | yes | — |
| `fast-wrap-ansi` | `0.2.2` | yes | yes | https://slsa.dev/provenance/v1 |
| `fastq` | `1.20.3` | yes | yes | https://slsa.dev/provenance/v1 |
| `fill-range` | `7.1.1` | yes | yes | — |
| `get-east-asian-width` | `1.6.0` | yes | yes | — |
| `glob-parent` | `5.1.2` | yes | yes | — |
| `iconv-lite` | `0.7.3` | yes | yes | — |
| `is-extglob` | `2.1.1` | yes | yes | — |
| `is-glob` | `4.0.3` | yes | yes | — |
| `is-interactive` | `2.0.0` | yes | yes | — |
| `is-number` | `7.0.0` | yes | yes | — |
| `is-unicode-supported` | `2.1.0` | yes | yes | — |
| `isexe` | `2.0.0` | yes | yes | — |
| `log-symbols` | `7.0.1` | yes | yes | — |
| `merge2` | `1.4.1` | yes | yes | — |
| `micromatch` | `4.0.8` | yes | yes | — |
| `mimic-function` | `5.0.1` | yes | yes | — |
| `mute-stream` | `3.0.0` | yes | yes | https://slsa.dev/provenance/v1 |
| `onetime` | `7.0.0` | yes | yes | — |
| `ora` | `9.4.1` | yes | yes | — |
| `path-key` | `3.1.1` | yes | yes | — |
| `picomatch` | `2.3.2` | yes | yes | — |
| `queue-microtask` | `1.2.3` | yes | yes | — |
| `restore-cursor` | `5.1.0` | yes | yes | — |
| `reusify` | `1.1.0` | yes | yes | — |
| `run-parallel` | `1.2.0` | yes | yes | — |
| `safer-buffer` | `2.1.2` | yes | yes | — |
| `shebang-command` | `2.0.0` | yes | yes | — |
| `shebang-regex` | `3.0.0` | yes | yes | — |
| `signal-exit` | `4.1.0` | yes | yes | — |
| `stdin-discarder` | `0.3.2` | yes | yes | — |
| `string-width` | `8.2.2` | yes | yes | — |
| `strip-ansi` | `7.2.0` | yes | yes | — |
| `to-regex-range` | `5.0.1` | yes | yes | — |
| `which` | `2.0.2` | yes | yes | — |
| `yaml` | `2.9.0` | yes | yes | — |
| `yoctocolors` | `2.2.0` | yes | yes | — |
| `zod` | `4.5.4` | yes | yes | https://slsa.dev/provenance/v1 |

## What stays open

The re-capture shares the original capture's NETWORK PATH — a later read over
the same route, not the independent route § 6.1 also names — so the
cryptographic weight rests on Link B's keys and transparency-log entries
rather than on the second read.

And this run is a CAPTURE, not a gate: nothing in CI invokes it. Making the
attestation a standing obligation of the pin, refused when a value is
unattested, would change what `contracts/openspec-cli-pin.yaml` declares and
what `neutral-product-pin` requires of it — an OpenSpec act, not a script's
side effect. The pin's declared-shortfall paragraph is therefore untouched,
and this record sits beside it as evidence rather than amending it.
