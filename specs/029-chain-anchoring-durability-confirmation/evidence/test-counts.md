# Test counts

Status: record
Kind: evidence

| Suite | Before this feature | After | Δ |
| --- | --- | --- | --- |
| `tests/chain_anchoring` | 25 passed (67s) | **59 passed (138s)** | +34, one per ratified scenario |
| `tests/signed_execution_chain` + `tests/manifest_digests` | 178 | **178 passed (98s)** | 0 new; one existing pin moved 28 → 34 subjects |
| `tests/doc-health` | 1542 passed | **1552 passed (399s)** | +10, from the six new contract files entering the corpus readers |

## The reader's own self-test, before and after

| | positives | negatives | closed codes red-proven | further findings probed | errors | warnings |
| --- | --- | --- | --- | --- | --- | --- |
| basis (`11feff75`) | 21 | 75 | 70/70 | 5 | 0 | 2 |
| this feature | **41** | **127** | **118/118** | **9** | **0** | **2** |

Both warnings are the standing honest pair and neither is this feature's to
close: `reader-not-required` (the canonical reader is not yet a REQUIRED check
on this repository, so every record this family defines confers and refuses
nothing until it is) and `archival-node-undeclared` (an operator gate that is
not met).

## Where the thirty-four live

`tests/chain_anchoring/test_durability_and_confirmation_scenarios.py` — one test
per scenario, each named for its scenario and quoting its WHEN/THEN in its own
docstring. Twelve of them are ACCEPTING scenarios and assert the positive half:
the empty day's root really is the released construction's declared empty root,
the midnight admission really enters the window that opens then, the two-leaf
batch's root and both membership paths really recompute, the replay really
consumes no sequence, the upgrade really appends against the same anchored
digest, and the retired-profile verification really reports current standing
without touching the immutable as-of token.

The module runs in **eight seconds** because each test builds a MINIMAL scope —
the durability subset — rather than the whole corpus. The reader's self-test
already adjudicates all forty-one positives together; repeating that per
scenario would multiply a quadratic cost for no further evidence.
