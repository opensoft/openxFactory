# Quickstart: The First Wallet (013)

Run all commands from the repository root of the `013-first-wallet` checkout.

## Verify the lane

```bash
# Whole-checkout sweep: live record must be discovered and validate green.
python3 scripts/validate-openxwallet.py . --strict

# Packaged corpus self-test must stay at the S2 baseline:
#   17 positives / 36 negatives across 13/13 requirements.
python3 scripts/validate-openxwallet.py

# Syntax-gate regression suite untouched by this change.
pytest tests/wallet_yaml_syntax_gate/ -q

# Governance validation.
openspec validate --all --strict
```

## Inspect the live artifacts

```bash
ls governance/review-authority/wallets governance/review-authority/attestations
```

The wallet file is a LIVE instance (no `examples` path segment), so the sweep
validates it against its audience-free rules: closed-set custody, closed-set
holder class, key REFERENCE only.

## Prove the boundaries

```bash
# No contract bytes moved:
git diff --stat origin/main -- contracts/ scripts/ .github/
# Expect empty output.

# No private material anywhere in the branch:
git diff origin/main | grep -iE "BEGIN|PRIVATE KEY|JWK" && echo "LEAK" || echo "clean"
```

## Minting (operator leg, T003)

On the OPERATOR'S machine only — any path that yields the raw 32-byte ed25519
public key, e.g.:

```bash
openssl genpkey -algorithm ed25519 -out mrc-wallet.key
openssl pkey -in mrc-wallet.key -pubout -outform DER | tail -c 32 | xxd -p -c 64
# → hex public key pasted to the assistant
```

The private half goes to the operator's vault and never enters git, CI, or an
agent session. The ASSISTANT derives `did:key:z6Mk…` from the public bytes
only (multicodec prefix `0xed01` + base58btc) — a deterministic,
public-material-only transformation:

```python
import hashlib
b = bytes.fromhex(PUB_HEX)
def b58(d):
    n = int.from_bytes(d, "big"); s = ""
    while n: n, r = divmod(n, 58); s = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"[r] + s
    return "z" + ("1" * (len(d) - len(d.lstrip(b"\x00")))) + s
print("did:key:" + b58(b"\xed\x01" + b))
print(b58(b"\xed\x01" + b))
```

The two outputs fill `key_reference.did` and `key_reference.public_key_multibase`.
