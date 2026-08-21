---
code_surface: openxFactory (`scripts/ideation_dashboard/web/views/doxbench-chat.js` — the selector's option list gains a first intake affordance and the empty-catalog default selection, and the send-control refusal stays byte-identical; `scripts/ideation_dashboard/web/views/staging-workbench-model.js` — the `approvedModels === 0` rung keeps its sentence and gains the intake-offered fact, and the two `catalogFailure` rungs must NOT offer it; `scripts/ideation_dashboard/web/app.js` — the catalog transport gains no new call site, and any intake route it does gain is budgeted by the transport-pin suite; `scripts/ideation_dashboard/serve.py` — a pending-declaration surface and the approval gate action beside the existing `_workbench_model_port` seam, both under the reused `session` local-human verdict; `scripts/ideation_dashboard/doxbench_model.py` — a proposed-vs-approved distinction that does NOT widen the closed seven-field public catalog entry; `contracts/schemas/gate-action-record.schema.yaml` — one additive `action` enum member for the approval act plus its `allOf` conditional; and `tests/ideation-dashboard/` — the selector-order, default-selection, no-secret-anywhere and approval-gating assertions). The credential BROKER itself (openProfiler), its custody, its OAuth authorization flow, and the provider client that would use a minted token are `add-model-provider-broker`'s surface, NOT this change's.
target_release: implementation_pending
Status: draft
Proposed: 2026-08-21
Origin: Brett's browser annotation on the live doxbench chat rail, 2026-08-21, targeting `select.doxchat-model`
Depends-on: add-model-provider-broker (the credential broker and the binding this flow writes into; that change is itself blocked on openProfiler, unbuilt)
---

# Proposal: add-doxchat-model-intake

## Why

Brett's browser annotation on the live console, 2026-08-21, against
`select.doxchat-model`, verbatim:

> this model selector is not working. what models should be available to us?
> also, in this dropdown, we need to have add model as the first option in
> the dropdown and if no current models loaded, that is the default. if user
> does add model, then we need to bring up a wizard that helps the user auth
> with oauth to their subscription or add a api

**The selector is not broken; it is empty, and it is empty by construction.**
`GET /workbench/model-catalog` returns the catalog its injected
`WorkbenchModelPort` declares, and returns the EMPTY catalog when no port is
declared — a successful editor-only posture, not an error. No port is
declared on this serve, and none can be: `serve.py`'s `build_server` accepts
`model_port_factory` as a keyword seam, `serve()` defaults only the notebook
adapter and the knowledge declaration through it, and `main()`'s argument
parser has no model flag at all. `scripts/reserve-dashboard.sh` runs
`python3 -m ideation_dashboard.serve`, so the live console reaches `main()`
and therefore declares nothing. The one real adapter in the repository,
`doxbench_bridge.OmpHarnessBridge`, is constructed by tests only.

So the honest answer to "what models should be available to us" is: **whatever
the deployment declares, and nothing is hardcoded.** There is no built-in
model list to be recovered, no provider allowlist to be turned on, and no
default anybody has been denied. The catalog is a deployment statement, and
this deployment has not made one.

**That answer is unsatisfying for a reason worth naming, and it is the reason
this proposal exists.** The only path from "no models" to "a model" that the
code offers today is: write Python that imports `build_server`, construct a
`ModelCatalog` by hand, construct an `OmpHarnessBridge` over it, and pass it
as `model_port_factory`. That is not an operator path. A human sitting in
front of the console cannot get a model, and the control that names the
problem — a selector reading "select an approved model" — offers no way to
approve one. Brett's annotation is asking for the missing path, from inside
the control where the absence is visible.

**The credential half of that path is already proposed and must not be
re-proposed here.** `add-model-provider-broker` (2026-08-08, `Status: draft`)
carries Brett's earlier ruling on exactly this — "we need to manage the api
keys or oAuth tokens for the user. The dashboard needs to set these in
settings. and will shell out to the openProfiler" — and specifies custody,
minting, the narrowed provider boundary, and the binding the dashboard keeps
instead of a secret. This change does not duplicate any of it. It adds the
three things that change does not cover: the affordance in the selector, the
human intake flow that reaches the broker, and the seam nobody has yet
written down — **how anything a human adds becomes APPROVED.**

**"Approved" is a real word here with a real referent, and it is presently
un-authored.** The promoted requirement says provider credentials "MUST come
only from the deployment's approved server-side credential mechanism", and in
the code approval is nothing but the conjunction of three facts: the entry is
in the `ModelCatalog` the install handed to the port, its `available` flag is
true, and the console passed the `session` local-human verdict (loopback, real
checkout, resolved actor). There is no approval instrument, no record, and no
approver. That is tolerable while only an operator editing Python can add a
model. It stops being tolerable the moment a wizard can, because then the act
of entering a payment credential silently becomes the act of approving a
provider for governed work. Those are two decisions and this proposal keeps
them two.

## What Changes

**The intake affordance is first, and it is the default only when the catalog
is empty.** Exactly as Brett asked. When a model IS available the default
stays a model, because a human with an approved model is trying to chat.

**Selecting intake does not select a model, and the rail does not change its
sentence.** The affordance carries no model id; a turn naming it refuses
through the existing absent-model refusal rather than a new code. The send
control stays refused for the reason it is refused today, and the rail keeps
saying that no approved model is configured. That sentence is TRUE and
actionable; replacing it with an invitation to enrol would trade a statement
of posture for a call to action, and the posture is the fact.

**Intake is not offered when the catalog could not be READ.** The dashboard
already distinguishes an empty catalog from an unreadable one and from a stale
console token, because those have different remedies. Offering enrolment as
the cure for a bug would send a human to buy a subscription to fix a reload.

**The flow captures either kind of authentication and the dashboard keeps
neither.** An API key goes straight to the declared broker and only the
returned reference is kept. For OAuth the dashboard is never the party that
receives tokens at all: it hands the human to the broker's own authorization
flow and gets back a reference. That is not fastidiousness — a refresh token
is a refreshable session-state credential, a class this workspace's credential
capability already refuses to distribute by any channel, and keeping it in one
custody is precisely what makes the OAuth kind conformant instead of an
exception.

**With no broker declared, the flow refuses rather than degrades.** A wizard
that collected a key with nowhere governed to put it would have to hold it
somewhere, and every somewhere available to the dashboard is forbidden.

**Intake PROPOSES; a recorded human act APPROVES.** Completing the flow yields
a pending declaration and a binding, disclosed as pending, contributing no
available catalog entry. Availability follows an explicit act by the resolved
local human actor, persisted as a gate action naming the declaration, carrying
the issuer/approver/expiry/audit reference the credential capability already
demands of an issued grant. Agent invocation refuses, like every gate action.

**The affordance ships with the flow behind it, or not at all.** An option
that names an action and does nothing is worse than no option: it converts a
plainly-stated posture into a dead end inside the very control the human was
told to use. Until the broker exists the selector keeps its present behaviour
unchanged — not a disabled intake option, which would only restate the rail's
sentence more weakly.

## Capabilities

### Modified Capabilities

- `ideation-dashboard` — MODIFIES **doxBench model catalog and provider
  boundary** to admit exactly one non-model intake affordance in the selector,
  to state that it can never be submitted as a model id, and to keep the
  catalog's contents server-declared. ADDS four requirements: the selector's
  intake-first ordering and empty-catalog default; the broker hand-off and
  binding-only retention; intake-proposes/human-approves with a recorded gate
  action; and the ship-with-the-flow sequencing rule.

## Impact

- Affected specs: `ideation-dashboard`
- Affected code: the chat view's selector, the workbench posture ladder, a
  pending-declaration surface and approval gate action in `serve.py`, and an
  additive `action` enum member on `gate-action-record.schema.yaml`
- **Depends on `add-model-provider-broker`**, which is itself blocked on
  openProfiler, unbuilt. Nothing here can ship before that custody exists,
  and the sequencing requirement says so rather than leaving it to a reader.
- The gate-action `action` enum is CLOSED, so the approval act needs an
  ADDITIVE enum extension and an additive contract bundle release, allocated
  at realization per `docs/contract-versioning-policy.md`. Reusing an existing
  member would misname a governance record, which is the failure mode
  `add-doxbench-editing-phase-b` already hit and declined to take.
- The closed seven-field public catalog entry does NOT widen. Proposed-versus-
  approved is a server-side distinction; a pending declaration is simply not
  in the catalog. Widening that schema is a separate, already-owed additive
  release (Phase B task 11.7) and this change does not spend it.
- Explicitly NOT in scope: openProfiler's design, its storage, its OAuth
  redirect handling, the minting seam, the provider client, and the narrowing
  of the provider boundary — all `add-model-provider-broker`'s.
- Also NOT in scope: giving the live serve a way to declare a model port from
  the command line. That is a real gap this proposal's Why documents, and it
  is worth its own small change; it is not a credential boundary and should
  not wait behind one.

## Open Questions

These are real forks, recorded rather than silently decided.

**OQ-1 — Which providers first?** The repository names `local-proxy` and
`anthropic` as harness provider ids, and the only worked credential runbook is
for OpenAI. RECOMMENDATION: ship the flow provider-agnostic and let the
binding's `provider` field carry the answer, exactly as
`add-model-provider-broker` keeps the broker invocation declared rather than
coded. A first provider is then a configuration fact, not a code change, and
whichever subscription Brett actually holds is the one that gets tested.

**OQ-2 — Where does the OAuth authorization flow live?** Three candidates: the
broker's own surface as redirect target; the dashboard as redirect target
handing the code straight to the broker; or the newly-ratified Keycloak
instance from `add-identity-brokering` acting as the broker for provider
grants too. RECOMMENDATION: the broker's own surface. It is the only option
where the dashboard never touches an authorization code, and
`add-identity-brokering` is scoped to HUMAN identity — reusing it for provider
subscriptions would conflate who-the-user-is with what-they-have-bought.
Deferred to openProfiler's own design, which that change already lists as its
open question 2.

**OQ-3 — Does approval require a Hermes consent instrument, or is a recorded
gate action enough?** The `consent-instrument` capability already models a
`credential_grant` dependent reference with withdrawal cascade, which would
fit. RECOMMENDATION: a recorded gate action is sufficient for the single-
operator loopback console — the human is spending their own subscription on
their own corpus, and requiring a consent instrument for that is ceremony
without a second party. A consent instrument SHOULD be required where the
model is enrolled on a tenant or shared install, or where a turn will process
another party's material; that condition needs Brett's ruling before the
approval act is implemented, because it determines whether the gate action
carries a `consent_ref`.

**OQ-4 — Should the empty-catalog default selection be the intake affordance
even though the send control stays refused?** Brett asked for it explicitly
and this proposal specifies it. RECOMMENDATION: keep it as asked — but note
the consequence honestly, which is that the selector will show a selected
option that is not a model while the rail says no model is configured. That
reads correctly ("here is the thing to do about it") and it is worth
confirming against the live console once the flow exists.

**OQ-5 — Does the approval act belong on the gate console, or inside the
intake flow's last step?** RECOMMENDATION: inside the flow's last step, as an
explicit confirmation that is plainly an approval and is recorded as one. A
human who just authorized a subscription is the right approver at the right
moment; routing them to a separate console to finish would make the pending
state a trap rather than a safeguard. The RECORD is what matters, not where
the button sits.
