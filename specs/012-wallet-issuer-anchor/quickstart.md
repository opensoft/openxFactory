# Quickstart: Run the Issuer-Anchor Sweep

**Feature**: 012-wallet-issuer-anchor | **Date**: 2026-08-24

## Run the validator (self-test layer, what CI runs)

```bash
python3 scripts/validate-openxwallet.py            # exit 0 = corpus clean
python3 scripts/validate-openxwallet.py --strict   # warnings are errors too
```

Expected closing note after S2:

```
note  corpus: 17 positive example(s), 36 negative confirmation(s) across 13/13 requirements
```

(Counts recorded as SC-002 evidence at implementation; the run output is the
authority if this file drifts.)

## Regression gates

```bash
pytest tests/wallet_yaml_syntax_gate/ -q    # S1's kind-aware YAML gate unchanged
openspec validate --all --strict            # change-set hygiene
```

## Author a review-class fixture

A grant becomes REVIEW-CLASS the moment `scope.acts` contains `review`:

```yaml
schema_version: 1
kind: xfactory_wallet_grant
grant_id: grant-review-<suffix>
audience:
  wallet_ref: wal-agent-poster-0001     # must resolve for ceiling checks
  holder_ref: agent:ledger-poster
scope:
  acts:
    - review                            # <- class marker (do not borrow casually)
    - post_transaction                  # mixing acts is fine; review triggers class
  authority_tier: act
  approval_posture:
    hermes_approval_required_before_apply: true
    authority_agents_may_approve: false
    human_escalation_required_for:
      - irreversible_external_effect
expires_at: "2027-12-31T23:59:59Z"
issued_at: "2026-08-24T00:00:00Z"
issued_by: Brett Heap                    # exact; root grants accept ONLY this
state: active
```

Refusals you can provoke:

| Omit / set | Result |
|---|---|
| no `issued_by` | `issuer-unrecorded` |
| root + `issued_by: sub-0123456789abcdef` | `root-issuer-unanchored` (machine-named pin) |
| root + `issued_by: opensoft` | `root-issuer-unanchored` (legacy pin) — legacy values do NOT grandfather |
| root + `issued_by: " brett heap"` | `root-issuer-unanchored` (generic) — exact match, never normalized |

Negative specimens live in `contracts/openxwallet/examples/negative/` and MUST
carry the three-line header contract (`expected_failure`, optional detail,
`requirement:` naming an existing REQ-ID).
