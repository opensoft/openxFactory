# Data Model: The Register and Its Reader (S4)

**Feature**: 014-register-and-reader | **Date**: 2026-08-25

## Register: `governance/review-authority/register.yaml`

KINDLESS (D11) - `register_version: 1`, one row; THE READER IS THE SHAPE.

| Row field | Value | Why |
|---|---|---|
| `row_id` | `row-mrc-0001` | Stable handle for successor tooling |
| `holder_ref` | `agent:merge-readiness-council` | The ONE MVP holder (council body) |
| `wallet_ref` | `wal-agent-mrc-0001` | Resolves to 013's live wallet record |
| `target_repo` | `opensoft/openxFactory` | Operator ruling; the pilot repository |
| `act` | `review` | Exact REVIEW_ACT_TOKEN membership decides class |
| `authority_tier` | `act` | MVP tier; stands on the recorded custody attestation |
| `grant_ref` | `grant-mrc-0001` | Cross-resolved against the indexed grant |
| `expires_at` | `2026-11-23T12:00:00Z` | ~90-day term; COMPUTED at read time, never trusted from state |
| `state` | `active` | Checked AGAINST computed expiry (N8) |

Header documentation carries: Q1c constraint (task 5.5), the explicit
permanently-human-only declaration with by-name floor-entry pointer, and the
no-schema D11 note.

## Grant: `governance/review-authority/grants/grant-mrc-0001.yaml`

Schema'd live instance (`xfactory_wallet_grant`, v1) — first of its class.

| Field | Value | Why |
|---|---|---|
| `grant_id` | `grant-mrc-0001` | Referenced by the register row |
| `audience.wallet_ref` / `.holder_ref` | wal-agent-mrc-0001 / agent:merge-readiness-council | Audience binding to 013's wallet |
| `scope.acts` | `[review]` | Makes it REVIEW-class (S2 rule (t)) |
| `scope.objects` | `[opensoft/openxFactory]` | One object = one target repository |
| `scope.authority_tier` | `act` | Registry member; attestation-backed |
| `scope.approval_posture` | approval-before-apply true; authority_agents_may_approve false; human_escalation list `[]` | N13 compensating control, envelope-vocabulary keys |
| `issued_by` | `Brett.Heap@opensoft.one` | ROOT grant → anchored operator; FIRST positive OXWR-R2 exercise (issuer_identifier grammar admits `@`) |
| `parent_grant_ref` | ABSENT | Root grant class |
| `expires_at` / `issued_at` | 2026-11-23T12:00:00Z / 2026-08-25T12:45:00Z | ~90-day ruling; byte-equal to row's expires_at (reader enforces equality) |
| `state` | `active` | Cold start |

## Reader codes (scripts/validate-openxwallet.py, rule (u))

| Code | Fires when | Maps to |
|---|---|---|
| `register-unparseable` / `-version-unknown` / `-row-malformed` | parse/version/strict-field-set failure | reader IS the shape (D11) |
| `register-minimal-shape-exceeded` | >1 row | "minimal shape exceeded" scenario |
| `register-wallet-unresolved` / `-inactive` | row's wallet missing/not active | active-row precondition |
| `register-act-not-review` / `-tier-unknown` / `-tier-refused` | act token / ladder / act_unsupervised | req 1 + closed ladder + refusal |
| `register-grant-unresolved` / `-mismatch` | grant_ref missing or audience/acts/tier/expiry/state disagree | row↔grant reconciliation |
| `register-row-expired` / `grant-state-stale` | computed expiry past (regardless of state) | N8 |
| `register-tier-act-unattested` | act row without valid attestation | unattested-cap + 013 obligation |
| `attestation-unparseable` / `-malformed` | attestation file broken | fail-loud, never silent cap |
| `register-no-active-row` | active REVIEW-class grant without backing active row (incl. empty/absent register) | HEADLINE obligation |

## Self-test probes (8)

clean · computed-expiry (3 codes at once) · no-active-row via `rows: []` ·
tier-act-unattested · minimal-shape-exceeded · row-malformed ·
absent-register-clean · absent-register+grants ⇒ no-active-row.
