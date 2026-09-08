# Byte-identity proof — openXwallet `wallet-v1.0`

**Feature**: `017-openxwallet-carve` · **Date**: 2026-08-26

**NAMED CARVE COMMIT**: `30565e48ffe3d8a9773e10af33425701845e10f6`
(openxFactory; "Merge pull request #396 from opensoft/016-openxwallet-split-bookkeeping")

---

## T004 — the CONTROL: the recorded digests already describe the carve commit

Taken BEFORE the carve. Without it, a post-carve match would prove the manifest
stale rather than the carve faithful.

| # | id | recorded `sha256:` | recomputed at CARVE_COMMIT | match |
| --- | --- | --- | --- | --- |
| 1 | `openxwallet-record` | `2012ef432616e73ddaead17c5e79aefacef712c2049ff649c15d7230b1d4eb08` | `2012ef432616e73ddaead17c5e79aefacef712c2049ff649c15d7230b1d4eb08` | YES |
| 2 | `openxwallet-custody-registry-schema` | `df72638497a7f90c2a4dff47c429cb794bc4b6e270ce2dd2b17116478ae3b51a` | `df72638497a7f90c2a4dff47c429cb794bc4b6e270ce2dd2b17116478ae3b51a` | YES |
| 3 | `openxwallet-custody-registry` | `94d631d6ee76dab015628a1856afd82582b98d6a3733622c9afe8b13b5278539` | `94d631d6ee76dab015628a1856afd82582b98d6a3733622c9afe8b13b5278539` | YES |
| 4 | `openxwallet-grant` | `fde433c5821e2e6f62926a72c58a67a784961d2e9e27e9f2b3520fcc8e738e88` | `fde433c5821e2e6f62926a72c58a67a784961d2e9e27e9f2b3520fcc8e738e88` | YES |
| 5 | `openxwallet-grant-exercise` | `f16ad31246186cec36e142ae39bd831d98fbc5c0afd48685057bc39e113c8858` | `f16ad31246186cec36e142ae39bd831d98fbc5c0afd48685057bc39e113c8858` | YES |
| 6 | `openxwallet-distinct-holder-constraint` | `c2a6d2fd23fb3743fdaf0e165dabc4cb1dff24e52a8262a38c86ed1482374b25` | `c2a6d2fd23fb3743fdaf0e165dabc4cb1dff24e52a8262a38c86ed1482374b25` | YES |
| 7 | `openxwallet-subject-attestation` | `d29eca519462aff7871de3786f19c820e9fc3b95115ce30e57d1f1cc2bc0c0b2` | `d29eca519462aff7871de3786f19c820e9fc3b95115ce30e57d1f1cc2bc0c0b2` | YES |
| 8 | `openxwallet-agent-composition` | `aed3978e8ae952f3ff5b3de1f672bba5da350d5aaeb442feafaa870b4de4be91` | `aed3978e8ae952f3ff5b3de1f672bba5da350d5aaeb442feafaa870b4de4be91` | YES |

**Control result: 8/8 match** at the carve commit.

## T005 — the expected carve surface, measured

`git ls-tree -r --name-only <CARVE_COMMIT> --` over the twelve path sets, sorted:
**100 files.**

| # | Path set | Files |
| --- | --- | --- |
| 1 | `contracts/openxwallet/` | 55 |
| 2 | `contracts/openxwallet-agent-profile/` | 8 |
| 3 | `scripts/validate-openxwallet.py` | 1 |
| 4 | `scripts/wallet-yaml-syntax-gate.py` | 1 |
| 5 | `tests/wallet_yaml_syntax_gate/` | 1 |
| 6 | `.github/workflows/wallet-validation.yml` | 1 |
| 7 | `openspec/specs/openxwallet/` | 1 |
| 8 | `openspec/specs/openxwallet-agent-profile/` | 1 |
| 9 | `openspec/changes/archive/2026-08-08-add-openxwallet/` | 6 |
| 10 | `specs/006-openxwallet-contracts/` | 7 |
| 11 | `specs/010-wallet-validator-ci/` | 9 |
| 12 | `specs/012-wallet-issuer-anchor/` | 9 |
| | **Total** | **100** |

---

## T011 — the carve invocation, verbatim

```sh
git filter-repo \
  --path contracts/openxwallet/ \
  --path contracts/openxwallet-agent-profile/ \
  --path scripts/validate-openxwallet.py \
  --path scripts/wallet-yaml-syntax-gate.py \
  --path tests/wallet_yaml_syntax_gate/ \
  --path .github/workflows/wallet-validation.yml \
  --path openspec/specs/openxwallet/ \
  --path openspec/specs/openxwallet-agent-profile/ \
  --path openspec/changes/archive/2026-08-08-add-openxwallet/ \
  --path specs/006-openxwallet-contracts/ \
  --path specs/010-wallet-validator-ci/ \
  --path specs/012-wallet-issuer-anchor/ \
  --force
```

One `--path` per set, twelve sets, exact paths. **No `--path-glob`, no
`--path-regex`, no `--path-rename`.** 1452 openxFactory commits parsed; the carved
history is 26 commits — the ones that actually touched these paths.

Carve-layer head: `620974d3060f79da5d7dc41820012127a73174df`
("Tick 2.5: wallet-validation is now a REQUIRED check via org ruleset 21538893"),
tagged locally as `carve-base` so every subsequent diff has a stable referent
inside the carved repository. `carve-base` is a local marker and is never pushed.

## T012 — completeness check: EMPTY DIFF

```sh
$ diff expected-files.txt actual-files.txt
(no output)
$ wc -l < actual-files.txt
100
```

The carve commit's sorted tracked listing over the twelve prefixes **equals** the
carved repository's sorted tracked listing. **PASS.**

## T013 — the counts a shorthand loses, asserted explicitly

| Assertion | Expected | Measured | Verdict |
| --- | --- | --- | --- |
| files under `specs/006-openxwallet-contracts/` | 7 | **7** | PASS |
| …of which under its `evidence/` | ≥1 | 2 | present, not lost |
| `contracts/openxwallet/examples/negative/` | 32 | **32** | PASS |
| `contracts/openxwallet-agent-profile/examples/negative/` | 4 | **4** | PASS |
| both negative trees together — **the ratified "36"** | 36 | **36** | PASS |

**On the ratified figure.** Task 3.7 asserts "36 under
`contracts/openxwallet/examples/negative/`". That directory holds 32; the other 4
are in the second family. 32 + 4 = 36. The assertion is carried in the form the
shorthand collapsed, because asserting 36 in the core family alone would FAIL
against a correct carve. The property the number stands for — no negative was lost
— holds exactly.

## T014 — examples-prefix preservation

```
PRESENT at identical relative path: contracts/openxwallet/examples
PRESENT at identical relative path: contracts/openxwallet-agent-profile/examples
```

An acceptance line, not a hope: the validator's corpus exclusion keys on
`"examples" in path.parts` AND a part in
`("openxwallet", "openxwallet-agent-profile")`. A flattened or renamed prefix
would re-adjudicate 36 intended-invalid negatives as LIVE records inside a check
that becomes REQUIRED.

## T015 — full path history survived

| File | Commits in the carved history |
| --- | --- |
| `scripts/validate-openxwallet.py` | **17** |
| `contracts/openxwallet/openxwallet-record.schema.yaml` | 3 |
| the whole carved repository | 26 |

Oldest carried commit: `df5628d` (2026-08-07) — *"openxWallet lands: custody
declared, and the collapse it forbids made unrepresentable"*. The history is
openxFactory's own commits filtered to these paths, not a single import commit.
