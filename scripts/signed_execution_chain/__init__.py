"""Reader-side primitives for the `signed-execution-chain` contract family.

Two modules, both VERIFICATION-ONLY and both stdlib-only:

* `canonical` — the one digest construction in force, `xfc-jcs-sha256-1`.
* `ed25519`   — Ed25519 signature verification and `did:key` public-half
  recovery.

They live beside `scripts/validate-signed-execution-chain.py` rather than inside
it because both are exercised directly by `tests/signed_execution_chain/`
against published known-answer vectors, and a primitive whose only caller is a
1,000-line validator is a primitive nobody tests on its own terms.
"""
