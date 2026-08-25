---
code_surface: openxFactory (dashboard settings surface for model-provider bindings; a token-minting broker seam that shells out to openProfiler; ONE server-side provider client behind it; the honest unavailable posture; the narrowed structural provider boundary; tests). openProfiler itself is OUT of scope and unbuilt.
target_release: none
Status: draft
Ruling: Brett, 2026-08-08 — the broker MINTS a short-lived token and doxBench calls the provider directly; brokered dispatch "would be too slow"
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

**The broker MINTS; doxBench calls.** Brett's ruling of 2026-08-08: putting
openProfiler in the request path "would be too slow" — a broker between the
console and the provider adds a hop to every turn, and to every chunk of a
streamed one, which is the wrong place to spend latency in an interactive
authoring surface. So openProfiler's job is custody and issuance: it holds
the long-lived API key or OAuth grant and mints a SHORT-LIVED, SCOPED token,
and the dashboard uses that token against the provider directly.

**That has a consequence this proposal states rather than buries.** Today
this repository contacts no provider at all, and that is structurally
enforced — serve.py carries the banner, and a test reads the source to keep
it true. Minting means the dashboard becomes a provider client. The
invariant therefore NARROWS rather than disappears: exactly one module may
hold a provider endpoint and a token, the structural test is rewritten to
enforce that narrower boundary instead of being deleted, and every other
module — every view above all — stays exactly as bounded as it is now.

**A minted token is memory-only and never crosses to the browser.** The
provider call is made server-side, from the loopback console process. A
token in a page is exfiltratable by anything that can run script there, and
the doxBench views hold no transport by construction; that property is worth
more than the hop it would save. The token is never written to a file, never
placed in a response, never logged, and never survives the process.

**The dashboard still holds no long-lived secret.** Settings hold a BINDING
per provider: an id, a label, the credential reference the broker resolves,
the authentication kind (`api_key` | `oauth`), and the broker invocation. A
binding is safe to read, safe to log and safe to commit. When a human enters
a key or completes an OAuth flow, the value goes to the broker on its
standard input and the dashboard retains nothing — no variable that outlives
the request, no file, no echo in a response. What comes back is a reference,
and later, on demand, a short-lived token.

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
- Explicitly NOT in scope: openProfiler's own design, its storage, and its
  OAuth flows.
- The "no provider is ever contacted from this repository" boundary DOES
  move, narrowly and deliberately, and that is the single most consequential
  line in this proposal. It becomes "no provider is contacted from anywhere
  except one named module", structurally enforced as before.

## Open questions for openProfiler

DECIDED 2026-08-08 (Brett): the broker MINTS, it does not dispatch. The
remaining questions are the broker's to answer, and the binding shape is
deliberately loose until it does:

1. What does a minted token carry — lifetime, scope, and whether it is
   provider-native (an OAuth access token the provider itself accepts) or a
   broker-issued credential the provider was pre-configured to trust? The
   first is the fast path Brett asked for; the second would put the broker
   back in the path it was just taken out of.
2. How does a human complete an OAuth flow — in the browser, with the broker
   as the redirect target, or entirely in the broker's own surface?
3. What is the audit obligation per MINT, given `credential-contracts`
   requires `issued_by`, `approved_by`, `expires_at` and `audit_ref` on a
   grant? Minting is the moment those fields exist, so the mint is the
   auditable event and the provider calls under one token are its children.
4. What happens at expiry mid-turn: does the dashboard re-mint and retry
   once, or surface the refusal? A long generation can outlive a short
   token, and silently retrying a paid call is a decision, not a detail.
