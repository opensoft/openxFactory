# Data Model & Rule Surface: Wallet Issuer Anchor (S2)

**Feature**: 012-wallet-issuer-anchor | **Date**: 2026-08-24

## New named constants (`scripts/validate-openxwallet.py`, beside CUSTODY_REGISTRY_PATH)

| Constant | Value | Authority |
|---|---|---|
| `REVIEW_ACT_TOKEN` | `"review"` | review-authority-intake requirement 1 ("scope.acts names the review act") |
| `ROOT_ISSUER_OPERATOR_TOKEN` | `"Brett Heap"` | Convener ruling 2026-08-23; anchor authority = Human Escalation Contract, cited as `docs/roles-and-authority.md:103-140` |
| `_MACHINE_ISSUER_RE` | machine-token shape | Detail-pin classification only; never weakens the exact-match refusal |

## Class detection

A grant is REVIEW-CLASS **iff** `REVIEW_ACT_TOKEN ∈ _hashable_set(scope.acts)`.
Scope content is the only trigger; kind, tier, posture, and audience play no part.

## New failure codes (fired inside `check_grant`, review-class grants only)

| Code | Condition | Detail pin behavior |
|---|---|---|
| `issuer-unrecorded` | `issued_by` absent/falsy on a REVIEW-CLASS grant | none |
| `root-issuer-unanchored` | ROOT (no `parent_grant_ref`) REVIEW-CLASS grant whose `issued_by` ≠ exact operator token | message names the value; machine-shaped values (resolve to a packaged wallet id, or match `_MACHINE_ISSUER_RE`) say MACHINE-NAMED; the literal legacy string says LEGACY; all other values get the generic unanchored refusal |

Sequential semantics: an absent issuer reports `issuer-unrecorded` only — the
anchor comparison needs a value to compare. Non-review grants are untouched
(no rule reads their `issued_by`). Review-class CHILDREN with any recorded issuer
keep existing attenuation semantics; S2 adds no child-specific rule.

## REQUIREMENTS map additions

| REQ-ID | Statement (map text) | Negative probe(s) |
|---|---|---|
| `OXWR-R1` | Every review-authority grant names its issuer | `grant-review-authority-omits-issued-by.yaml` |
| `OXWR-R2` | A root review-authority grant's issuer is anchored outside the register | `grant-review-root-issuer-is-a-machine.yaml` · `grant-review-root-issuer-says-opensoft.yaml` |

Family prefix follows the established pattern (core `OXW-R*`, profile
`OXWA-R*`): intake = `OXWR-R*`. Coverage closure moves 11/11 → 13/13.

## Specimen headers (negative-fixture contract)

```yaml
# expected_failure: <code>
# expected_failure_detail: <substring>   # optional pin into the fired lines
# requirement: OXWR-Rn
<schema-valid grant body, minimal everything else>
```

Machine specimen pins its issuer token (proves the machine branch); legacy
specimen pins the word `legacy` (proves the legacy branch, not merely the code).

## Boundary guard (self-test)

Synthesized schema-valid `post_transaction`-class root grant, NO `issued_by`,
audience resolving to a packaged wallet whose custody ceiling admits `act`:
must produce ZERO findings. Proves class membership cannot leak onto
non-review grants (US3 regression guard).
