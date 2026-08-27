# Implementation Plan: openxFactory consumes openXwallet and sheds the wallet paths (P3)

**Branch**: `023-openxwallet-consume-shed` · **Date**: 2026-08-27 · **Spec**: [spec.md](spec.md)

**Authority**: `openspec/changes/split-openxwallet-repo` — `tasks.md` §7 (33
tasks), design **D1**–**D4**, **D6**, **D9**–**D14**, clarifications
**N1/N4/N5/N7**. OpenSpec ratified; Speckit builds.

## Summary

One atomic pull request. openxFactory stops owning the openxWallet family and
starts consuming it at `opensoft/openXwallet` `wallet-v1.1` (commit
`63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`) through a nested gitlink plus
`contracts/openxwallet-pin.yaml`, verified by a new fail-closed
`scripts/verify-openxwallet-pin.py`. The REQUIRED `wallet-validation` check moves
into `.github/workflows/openxwallet-consumer-gate.yml`, KEEPING the job id, and
runs the PINNED readers over openxFactory's own tree with a POSITIVE assertion
that the intake register was opened. `scripts/validate-trust-anchor.py` reads the
wallet custody registry through the gitlink and refuses by NAMED CODE. Nine of
the twelve carved path sets are deleted (three are deliberate record exceptions),
and the cut is published as the MAJOR `contract-v2.0`.

## Technical Context

**Language/Version**: Python 3.12 (validators, verifier, tests); YAML (contracts,
pins, workflows); GitHub Actions.

**Primary Dependencies**: PyYAML, jsonschema ≥4.18, rfc3339-validator, pytest;
`actions/create-github-app-token@v2`; git submodules.

**Testing**: `python3 -m pytest tests/ -q -m "not postgres"` (the REQUIRED
`pytest-suite`), `pytest.ini` deliberately option-free.

**Target**: `opensoft/openxFactory` default branch, org rulesets 21538893
(`wallet-validation`) and the Tier-1 main protection.

**Constraints**:
- ONE pull request. `scripts/validate-trust-anchor.py` exits 2 when the wallet
  custody registry is absent, so no two-commit ordering has a green intermediate.
- Ruleset 21538893 is edited by NOTHING. The token is a job id; the alias carries
  it.
- Byte identity. The eight digests copied into the pin must equal the values
  `contracts/manifest.yaml` recorded at the NAMED CARVE COMMIT
  `30565e48ffe3d8a9773e10af33425701845e10f6`, and must equal `sha256sum` at
  `wallet-v1.1`. Verified both ways before anything else was written.
- `governance/review-authority/` is untouched (R6), all four files.
- Records are annotated, never rewritten.
- No merge, no tag: both are operator acts, and merge waits for P5a.2.

**Scale/Scope**: 92 files deleted, ~9 files added, ~14 files edited, one nested
submodule, one MAJOR bundle.

## Constitution Check

- **Contract-first, ratified before built.** The change is RATIFIED
  (2026-08-26); this feature is realization only. No requirement is invented
  here: every deliverable traces to a numbered task in §7.
- **Fail closed.** Every new refusal path exits non-zero with a NAMED code and
  one fixed remediation trailer. No new fallback, no new opt-in, no advisory
  tier.
- **No vacuous passes.** Each control has an explicit anti-vacuity partner: the
  gate's POSITIVE register conjunction, the invocation test's exact-string pin,
  `pytest-suite`'s pinned collected/passed/SKIPPED triple, and the verifier's
  separate gitlink-vs-checkout comparisons.
- **Records are annotated.** The archived `add-openxwallet` packet,
  `docs/archive-record-discrepancies.md` row 7, the `contract-v1.43` CHANGELOG
  worked example and the README archive-ledger entry are ANNOTATED. The two
  promoted specs are left for `openspec archive` to empty via the ratified
  REMOVED deltas.
- **Machine keys do not move (R2).** `openxwallet` ids, the `xfactory_wallet_*`
  prefix, every finding code, every filename and every path are unchanged. The
  brand moved; the wire label did not.

## Project Structure

### Documentation (this feature)

```
specs/023-openxwallet-consume-shed/
├── spec.md
├── plan.md              # this file
├── tasks.md
├── research.md          # the reachability decision and the digest proof
├── checklists/requirements.md
└── evidence/
    ├── operator-acts.md # the App-installation finding, recorded as an act
    └── validation.md    # every command run and its result
```

### Source Code (repository root)

```
.gitmodules                                       # + openXwallet
openXwallet/                                      # gitlink @ wallet-v1.1
contracts/openxwallet-pin.yaml                    # NEW — the pin
contracts/manifest.yaml                           # − 8 rows, 7 citations reworded, bundle → contract-v2.0
contracts/CHANGELOG.md                            # + the MAJOR entry
contracts/README.md                               # 3 rows → 1 "consumed at pin"
contracts/releases/contract-v2.0.digests.yaml     # NEW — built by the house tool
docs/contract-versioning-policy.md                # deprecation recorded EXECUTED
docs/archive-record-discrepancies.md              # row 7 NOTE
scripts/verify-openxwallet-pin.py                 # NEW — six checks, six codes
scripts/validate-trust-anchor.py                  # registry through the gitlink; refusal by name in main()
scripts/validate-identity-brokering.py            # prose citations → the pin
scripts/proposal-support.py                       # staged-origin comment annotated
.github/workflows/openxwallet-consumer-gate.yml   # NEW — replaces wallet-validation.yml, job id retained
.github/workflows/pytest-suite.yml                # app token + insteadOf + scoped init + pinned triple
.github/workflows/doc-health-reusable.yml         # both init filters widened, guarded
.github/CODEOWNERS                                # − 2 validator lines, + pin/verifier/gitlink/.gitmodules
README.md                                         # 8 ranges: gate, index, ledgers, archive annotation
tests/openxwallet_pin/test_verify_pin.py          # NEW — 35 cases, six codes
tests/openxwallet_consumer_gate/test_gate_invocation.py  # NEW — the invocation pin
tests/trust-anchor/test_openxwallet_pin_refusal.py       # NEW — named-code refusals
openspec/changes/add-wallet-carried-review-authority/tasks.md  # 5 live-change edits + addendum
DELETED: contracts/openxwallet/, contracts/openxwallet-agent-profile/,
         scripts/validate-openxwallet.py, scripts/wallet-yaml-syntax-gate.py,
         tests/wallet_yaml_syntax_gate/, .github/workflows/wallet-validation.yml,
         specs/006-openxwallet-contracts/, specs/010-wallet-validator-ci/,
         specs/012-wallet-issuer-anchor/
KEPT DELIBERATELY: openspec/specs/openxwallet/, openspec/specs/openxwallet-agent-profile/
         (emptied by `openspec archive`, not here),
         openspec/changes/archive/2026-08-08-add-openxwallet/ (a record, annotated)
```

## Ordering, and why it is not negotiable

1. **CI reachability, fail-fast.** Establish that the gate can clone a second
   private org repository from openxFactory Actions BEFORE anything is written.
   If it cannot, the whole pull request is unmergeable and nothing else matters.
2. **The gitlink, then the pin.** The pin's digests are checked against the
   submodule, so the submodule exists first.
3. **The verifier, then everything that depends on a verified pin.** The
   trust-anchor repoint calls it; the gate's first step is it.
4. **The workflows before the deletions**, so the replacement gate exists in the
   same commit that removes the file it replaces — the atomicity requirement.
5. **The deletions, then the manifest and the bundle**, because the release
   inventory is computed over the post-deletion tree.
6. **The documents last**, so every path they name is the final one.
7. **Numbers pinned from a real run.** `pytest-suite`'s triple is read from CI's
   own JUnit XML, not guessed: the first run establishes it and the pin is
   corrected once, with the reason recorded.

## Complexity Tracking

| Deviation | Why | Simpler alternative rejected because |
| --- | --- | --- |
| The gate mints `OPENXFACTORY_APP_*`, not the `XFACTORY_APP_*` names `doc-health-reusable.yml` uses | The org secret `XFACTORY_APP_ID` is visibility-`selected` and openxFactory is not among its two repositories. The PATTERN is the house one; only the secret names differ. | Adding openxFactory to that org secret's repository list is an org-settings change with no ratified authority in §7, and this repository already holds a content-App secret pair whose installation covers the whole org. |
| A scoped `git submodule update --init openXwallet` instead of `submodules: true` | `tasks.md` 7.13/7.16 require it and 7.16 says `submodules: true` alone is explicitly NOT the fix. | A blanket init also fetches `installs/omnigent-install`, which no gate here reads, and `--recursive` would pull every nested submodule of every consumer. |
| The validator step declares `shell: bash` | The default `run` shell does not set `-o pipefail`, so `\| tee` would return 0 over a failing validator. | Dropping the `tee` loses the log the POSITIVE register assertion reads; `set -o pipefail` inside the block would break the exact-invocation pin. |
| The nested init in `doc-health-reusable.yml` is GUARDED on the nested `.gitmodules` | P4 bumps the aggregation's openxFactory pin in a later pull request; before that the gitlink is not declared. | An unguarded init reds the nightly for the wave's ordering rather than for a defect. |
| The `contract-v1.43` CHANGELOG worked example and README archive entry are ANNOTATED rather than reworded in place | They are published records; at their own version the paths were correct. | Rewriting a record into agreement with a later tree is the failure this repository's own doctrine forbids. |
