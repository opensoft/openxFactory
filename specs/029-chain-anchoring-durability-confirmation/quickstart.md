# Quickstart: 029-chain-anchoring-durability-confirmation

Status: draft
Kind: runbook

Run from the openxFactory checkout root. The openXwallet submodule must be
materialized for the tranche-one gate:

```bash
git submodule update --init openXwallet
```

## The family's own gates

```bash
python3 scripts/validate-chain-anchoring.py .            # 0 errors, 2 standing warnings
python3 scripts/validate-chain-anchoring.py              # self-test only
python3 scripts/validate-signed-execution-chain.py . --require-pinned-wallet-vocabulary
python3 scripts/validate-manifest-digests.py .
python3 -m pytest tests/chain_anchoring -q               # 59 passed
```

`validate-chain-anchoring.py .` reports, on the note line: the packaged positive
count, the negative count, and **how many of the closed refusal codes are
red-proven**. That last number is the one to read — it is `118/118`, and the
reader refuses to pass if a code has no probe.

## The estate's gates

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
python3 scripts/proposal-support.py . verify amend-chain-anchoring-readiness-and-durability
python3 scripts/validate-sequenced-after.py . --ledger-diff
python3 scripts/validate-contract-release.py verify-commit --commit HEAD
python3 -m pytest tests/doc-health -q -p no:cacheprovider
python3 scripts/doc-health.py --single-repo .
```

## The red-first measurement, reproduced

With the amendment's eight check layers replaced by no-ops, every one of its
fifty-two negatives must validate CLEANLY inside the positive scope — which is
what proves each fails for the new rule and for nothing else. The script is in
`evidence/red-first.md`.

## The two standing warnings, and why they stay

`reader-not-required` — the canonical reader is not yet a REQUIRED check on this
repository, so every record this family defines confers and refuses nothing
until it is, and the packaged declaration must keep saying so in the present
tense. `archival-node-undeclared` — the operational witness's archival node is
an operator gate that is not met. Both are honest and neither is this feature's
to close.
