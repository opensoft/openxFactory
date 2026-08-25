# Quickstart: The Register and Its Reader (S4)

Run all commands from the repository root of the `014-register-and-reader`
checkout.

## Verify the lane

```bash
# Whole-checkout sweep: register reader runs inside the required check.
python3 scripts/validate-openxwallet.py . --strict
#   expect: exit 0; repo scan reports BOTH live artifacts validated;
#           corpus unchanged at 17 positives / 36 negatives across 13/13.

# Layer-1 self-test incl. the eight S4 synthesized-tree probes.
python3 scripts/validate-openxwallet.py

pytest tests/wallet_yaml_syntax_gate/ -q      # regression suite untouched
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

## Prove the headline obligation (mutation probe — restore immediately!)

```bash
mv governance/review-authority/register.yaml /tmp/reg.bak
python3 scripts/validate-openxwallet.py . --strict   # FAILS:
#   ERROR [register-no-active-row] active REVIEW-class grants
#   ['grant-mrc-0001'] exist but … does not exist …
mv /tmp/reg.bak governance/review-authority/register.yaml
python3 scripts/validate-openxwallet.py . --strict   # green again
```

## Prove the boundaries

```bash
git diff dda06ba3 --stat -- contracts/ .github/    # expect empty
git diff dda06ba3 | grep -icE "BEGIN|PRIVATE KEY" || echo clean
```

## What each piece IS

- `governance/review-authority/register.yaml` — the intake register
  (kindless per D11; the reader is the shape; permanently human-only;
  Q1c constraint in its header).
- `governance/review-authority/grants/grant-mrc-0001.yaml` — the FIRST root
  review-authority grant (anchored operator issuer; review over
  opensoft/openxFactory at tier `act`, approval-before-apply posture).
- The reader inside `scripts/validate-openxwallet.py` — runs in the REQUIRED
  wallet-validation check on every PR.
