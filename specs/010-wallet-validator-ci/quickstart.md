# Quickstart — 010-wallet-validator-ci

Runnable scenarios proving the gate works end-to-end. Run from the repository root of a
checkout containing this branch. Prerequisites: Python 3.12+ and the validator's dependency set installed
(`pip install pyyaml jsonschema rfc3339-validator`) — the syntax-gate helper
importlib-loads the validator module, so all three are required for every scenario.

## Scenario 1 — Self-test only (proves the negatives still bite)

```bash
python3 scripts/validate-openxwallet.py
```

**Expected**: exit `0`. The run asserts every packaged conforming example passes AND all
29 negative specimens fail with their declared `expected_failure` codes. Any output here
is a validator defect outside this feature's scope — stop and disposition.

## Scenario 2 — Whole-tree sweep (what the check runs)

```bash
python3 scripts/validate-openxwallet.py .
```

**Expected**: exit `0` on the current tree (warnings, if any, are logged but do not fail
— Q3 ruling). This is exactly the command the CI check executes against the checkout.

## Scenario 3 — Malformed live artifact is caught

Create a scratch copy test (do NOT commit):

```bash
cp -r . /tmp/opencode/oxf-gate-probe && cd /tmp/opencode/oxf-gate-probe
python3 - <<'PY'
from pathlib import Path
p = Path("contracts/openxwallet/examples/negative/grant-exceeds-custody-ceiling.yaml")
bad = p.read_text().replace("# expected_failure", "# not-an-expected-failure")
Path("malformed-live-grant.yaml").write_text(bad)
PY
python3 scripts/validate-openxwallet.py . ; echo "exit=$?"
```

**Expected**: non-zero exit; findings name `malformed-live-grant.yaml` and the violated
rule. A grant whose self-declared expectation header was stripped is adjudicated as a
LIVE artifact and must not slip through as an example. Clean up: `rm -rf /tmp/opencode/oxf-gate-probe`.

## Scenario 4 — The check exists and is shaped right (post-implementation)

On a PR from this branch:

- The Checks tab shows a check named exactly **`wallet-validation`**.
- Its job completed within 10 minutes under least-privilege permissions
(`contents: read`).
- Re-opening a draft PR triggers it like any other PR.

## Scenario 5 — Operator upgrade act (post-merge, human-only)

Follow the README section "Wallet validation gate" (added by this feature):
mark `wallet-validation` required via the active ruleset governing main
(Repo Settings → Rules → Rulesets → edit ruleset targeting main → Require status
checks → add `wallet-validation`), or via a classic branch protection rule
(Settings → Branches → main → Require status checks → select `wallet-validation`).
Afterwards, a PR with a red `wallet-validation` check cannot be merged through the UI.

## Scenario 6 — Syntax gate (FR-011 hardening)

```bash
python3 scripts/wallet-yaml-syntax-gate.py .
```

**Expected**: exit `0` on the clean tree. Negative rehearsal: create a file containing
`kind: xfactory_wallet_grant` plus deliberately broken YAML anywhere under a scratch
copy — the gate must exit `1` naming that file and the parse error, while a file with
broken YAML but NO family-kind reference keeps the validator's skip semantics.
