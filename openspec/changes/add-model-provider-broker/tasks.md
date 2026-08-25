# Tasks: add-model-provider-broker

## 0. Ratification

- [x] 0.1 DECIDED (Brett, 2026-08-08): the broker MINTS a short-lived token
      and doxBench calls the provider directly — brokered dispatch "would be
      too slow".
- [ ] 0.2 openProfiler declares its CLI surface AND what a minted token
      carries (lifetime, scope, provider-native or broker-issued). Nothing
      below hardcodes the command; the binding carries the argv template
      precisely so this can land first.
- [x] 0.3 DECIDED (the `ideation-dashboard` expiry scenario): discard an
      expired token and surface the fixed refusal; a later call mints again.
      No automatic re-mint/retry occurs during the expired call.

## 1. The binding (implementable now)

- [x] 1.1 A `model-provider-binding` record: id, label, credential
      reference, auth kind (`api_key` | `oauth`), broker invocation. No
      secret field exists in the shape — not optional, ABSENT, so no code
      path can populate one.
- [x] 1.2 Settings surface: list, add, edit, remove bindings. Read-back
      discloses the binding and states plainly that the credential lives in
      the broker.
- [x] 1.3 A credential hand-off that retains nothing: value to the broker's
      stdin, reference back, and a test that greps the whole checkout and
      every response for the value afterwards.

## 2. Minting and the narrowed boundary

- [x] 2.1 A minting seam that shells out to the declared invocation and
      returns `(token, expires_at)` — memory only, never written, never
      logged, never in a response.
- [x] 2.2 ONE provider-client module behind it. Every other module stays
      free of provider endpoints, SDKs and tokens.
- [x] 2.3 REWRITE the structural provider check to enforce the narrower
      boundary rather than deleting it: today it asserts no provider is
      contacted from anywhere; it becomes "from nowhere except this one
      module", and the views clause stays absolute.
- [x] 2.4 Expiry handling per 0.3, and discard-on-expiry regardless.
- [x] 2.5 Wire `serve.py`'s `model_port_factory`; unconfigured stays exactly
      the posture it is now.

## 3. Verification

- [x] 3.1 No minted token reaches the browser, appears in a log, or lands in
      the checkout — asserted, not assumed.
- [x] 3.2 Every broker and provider failure maps onto the fixed redacted
      refusal, and a missing capability is distinguishable from a failed
      call.
- [x] 3.3 The unconfigured posture is byte-for-byte what it is today.
