# Gates, with counts

Status: record
Kind: evidence

Run from the openxFactory checkout with `openXwallet` materialized. Readings
taken at the branch head before the catch-up merge to `origin/main`; re-taken
after the merge, and the after-merge readings are appended at the foot of this
file.

## The family's own gates

| Gate | Result |
| --- | --- |
| `python3 scripts/validate-chain-anchoring.py .` | **0 error(s), 2 warning(s)** — self-test: 41 packaged records as ONE coherent corpus, 126 negatives invalid for their intended reason, **118/118 closed refusal codes red-proven**, 8 further finding codes probed; repo scan 0 artifacts checked / 2150 skipped |
| `python3 scripts/validate-signed-execution-chain.py . --require-pinned-wallet-vocabulary` | **0 error(s), 0 warning(s)** |
| `python3 scripts/validate-manifest-digests.py .` | **OK — 187/187 per-file digest(s) verify** |
| `python3 -m pytest tests/chain_anchoring -q` | **59 passed** (138s) |
| `python3 -m pytest tests/signed_execution_chain tests/manifest_digests -q` | **178 passed** (98s) |

The two warnings are the standing honest pair, unchanged from the basis
realization: `reader-not-required` and `archival-node-undeclared`.

## The estate's gates

| Gate | Result |
| --- | --- |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | **89 passed, 0 failed** (89 items; the ratification commit saw 90 because `add-subject-establishment` archived in between) |
| `OPENSPEC_TELEMETRY=0 openspec validate amend-chain-anchoring-readiness-and-durability --strict` | **valid** |
| `python3 scripts/proposal-support.py . verify amend-chain-anchoring-readiness-and-durability` | **proposal support verification ok** |
| `python3 scripts/validate-sequenced-after.py . --ledger-diff` | **ledger consistent with the corpus (164 rows)**; deepest declared chain resolved 2 hops |
| `python3 -m pytest tests/doc-health -q -p no:cacheprovider` | **1552 passed** (399s) |
| `python3 scripts/doc-health.py --single-repo .` | 6 critical / 4 error / 27 warning / 16 info — **identical to `origin/main`, zero delta** (see [`doc-health-delta.md`](./doc-health-delta.md)) |

## `validate-contract-release.py verify-commit`, compared against the base

```
$ python3 scripts/validate-contract-release.py verify-commit --commit HEAD
HGR-RELEASE-DIGEST-MISMATCH error path=contracts/manifest.yaml: digest does not
  match the raw Git blob at the pinned commit
```

**The mismatch set is EXACTLY `origin/main`'s.** Run in a detached worktree at
`e4ff4fb3`, the base reports the same single entry for the same path:

```
$ (cd <worktree at origin/main>) && python3 scripts/validate-contract-release.py verify-commit --commit HEAD
HGR-RELEASE-DIGEST-MISMATCH error path=contracts/manifest.yaml: digest does not
  match the raw Git blob at the pinned commit
```

One path, `contracts/manifest.yaml`, which is the only path permitted to differ:
this feature adds six rows to it and re-pins six moved files, and the manifest
is an editorial member between cuts. **No other path differs, and
`contract_bundle_version` is untouched.**

## The pre-publication measurement, which is why this is additive

```
$ git tag --contains 11feff75
(empty)
$ grep -c chain-anchoring contracts/releases/contract-v3.3.digests.yaml
0
```

The `contract-v3.3` tag (`16b85614`) predates the basis realization
(`11feff75`) by twenty minutes, so the family is REGISTERED in
`contracts/manifest.yaml` and UNSHIPPED in every bundle. Replacing
`anchor-state.schema.yaml`'s closed per-witness `status` enumeration is
therefore additive to every bundle that has ever shipped — and it must land
BEFORE the next cut, because after publication the same edit is a compatibility
break.

## Red-first

With the amendment's eight check layers disabled, **52/52 of its negatives
validate cleanly** and the positive corpus reports **0 errors** — see
[`red-first.md`](./red-first.md).
