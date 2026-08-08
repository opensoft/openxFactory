---
code_surface: openxFactory (dashboard settings surface for model-provider bindings; a broker-backed WorkbenchModelPort that shells out; the honest unavailable posture; tests). openProfiler itself is OUT of scope and unbuilt.
target_release: none
Status: draft
---

# Proposal: add-model-provider-broker

## Why

doxBench has a model seam and no model. `doxbench_model.py` states it
outright — "There is no real provider adapter here and none is implied" —
`model_port_factory` is a seam only tests fill with a fake, and the chat-turn
handler builds its prompt envelope and then refuses
`model_capability_unavailable` unconditionally. Measured against the live
console on 2026-08-08: the model-catalog route refuses, so every
model-proposed affordance the lens now wants (Brett, 2026-08-08: "show the
user a list of possible subjects this document can be about") renders an
empty state and will keep doing so until something answers.

Brett's ruling on 2026-08-08 names what answers: **openProfiler**, not yet
built — "we need to manage the api keys or oAuth tokens for the user. The
dashboard needs to set these in settings. and will shell out to the
openProfiler."

That is a credential BROKER, and this repository already ratified the shape:
`credential-contracts` owns `xfactory_credential_broker_contract` and
`xfactory_credential_binding_template`, whose whole point is that a consumer
holds a binding and never a secret. The dashboard's own standing rule says
the same thing — never store raw credentials, grant and binding templates
only. So the boundary is not a new invention; it is an application of a
contract that exists, to a consumer that does not have one yet.

This proposal exists BEFORE the implementation because that is the rule for
a boundary: a surface that will accept an API key or an OAuth token from a
human, hand it to another process, and then dispatch paid provider calls on
their behalf is a policy question first and a UI second.

## What changes

**The dashboard never holds a provider secret.** Settings hold a BINDING per
provider: an id, a label, the credential reference the broker resolves, the
authentication kind (`api_key` | `oauth`), and the broker invocation. A
binding is safe to read, safe to log and safe to commit; a secret is none of
those and never enters the dashboard's state, its snapshot, or its checkout.

**Setting a credential is a hand-off, not a store.** When a human enters a
key or completes an OAuth flow, the value goes to the broker on its standard
input and the dashboard retains nothing — no variable that outlives the
request, no file, no echo in a response. What comes back is a reference.

**The broker invocation is DECLARED, not hardcoded.** openProfiler does not
exist yet, so this change must not encode a command line it cannot verify.
The binding carries the argv template; the adapter substitutes and executes
it. When openProfiler ships with a different surface, the binding changes and
no code does.

**Absent, unconfigured or failing, the answer is the same honest refusal it
is today.** `model_capability_unavailable` already has a defined shape, a
status and a rendered state; a broker that is missing, misconfigured, times
out, or returns garbage maps onto it rather than inventing new failure modes,
and the reason is stated to the human rather than to a log alone.

## Impact

- Affected specs: `ideation-dashboard`
- Affected code: a new settings surface, a broker-backed
  `WorkbenchModelPort`, `serve.py`'s `model_port_factory` wiring
- Depends on: **openProfiler**, unbuilt. Everything here is inert until a
  binding names a working broker, which is why it can land ahead of it.
- Explicitly NOT in scope: openProfiler's own design, its storage, its OAuth
  flows, and any provider SDK. No provider is ever contacted from this
  repository — that boundary, which the doxBench slice holds today, does not
  move.

## Open questions for openProfiler

These are the broker's to answer, and the binding shape above is deliberately
loose until it does:

1. Does the broker DISPATCH the provider call (the dashboard sends a prompt
   envelope and receives a completion), or does it only VEND a short-lived
   token the dashboard then uses? The first keeps every secret and every
   endpoint on the broker's side; the second puts a live token in the
   dashboard's memory. This proposal assumes the first.
2. How does a human complete an OAuth flow — in the browser, with the broker
   as the redirect target, or entirely in the broker's own surface?
3. What is the audit obligation per call, given `credential-contracts`
   requires `issued_by`, `approved_by`, `expires_at` and `audit_ref` on a
   grant?
