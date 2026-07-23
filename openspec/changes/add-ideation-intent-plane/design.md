# Design: Ideation Intent Plane

## Context

D16 makes the dashboard read-only by construction: machinery/agents write
through `OutputBoundary` (no gate methods), lifecycle acts flow only through
`HumanGate` (identified human, gate-action record). The gate console engine
(codexFactory `gate_console.py`) carries five verbs; the deployed image is
baked, credential-free, Basic-Auth'd, with no write routes. The rolling-PR
delivery pattern (doc-health nightly, derive-possibles commit-back) is the
proven way unattended machinery lands governed commits under org rulesets.

## Goals / Non-Goals

**Goals**: hosted + mobile actions with zero write authority on serving
surfaces; one executor (the console engine); full audit (intent + record +
artifact committed together); immediate UI feedback despite bake latency;
identity that names the human from day one and upgrades to SSO without
contract change.

**Non-Goals**: editing documents from the hosted surface (redlines travel as
intent payloads, authored elsewhere); per-engineer hosted dashboards (the
local `generate-and-open` is the per-branch view — cloud-workstation-topology
lock); the Drive membrane (fragment 2, own change); replacing GitHub PR
review (rolling-PR approval deep-links, never re-implemented UI).

## Decisions

### D1 — Second touch: custody, not decision
The authenticated click IS the decision (it produces the intent and, once
applied, the gate-action record under that actor). The rolling intents PR is
CUSTODY under org rulesets: batched, auto-merge enabled, approved in the
existing Merge-Master ritual. The intent-feed overlay covers the latency,
and the apply lane may trigger snapshot regeneration + rebake on success so
verdicts publish in minutes. One decision serves the intake lane later (the
membrane fragment names the same tension).

### D2 — Inbox = dispatch-only authority
The inbox's credential can dispatch ONE workflow and nothing else
(`actions:write`, no `contents`). Compromising the inbox yields the ability
to submit well-formed intents as the ingress-authenticated user — which the
apply lane revalidates anyway (verb allowlist, target existence, lifecycle
legality, stale-view check). Hosting shape (sidecar vs own deployment) is an
open question resolved at realization; either way it sits behind the SAME
ingress auth as the dashboard.

### D3 — Intent kernel is its own schema, gate-action-record stays pure
An intent is a REQUEST; a gate-action record is an APPLIED act. Separate
kinds, one family: `gate-intent.schema.yaml` beside
`gate-action-record.schema.yaml`, both validated by the delegated dashboard
validator. The applied intent references its resulting record (and vice
versa via the record's artifacts), giving the request->act chain without
conflating the two.

### D4 — Stale-view refusal via snapshot_rev_seen
Every intent records the snapshot source_revision the actor was LOOKING at.
The apply lane refuses when the target's state has materially advanced
(register fingerprint CAS precedent) — refusals land in the intent feed
with reasons, rendered in the refusal panel.

### D5 — Local-first realization order
The LOCAL dashboard gets executing gate routes + the dispose tray FIRST
(behind the existing loopback gate; actor from local identity): no new
infrastructure, proves the UI, and the identical tray then targets the
intent API when hosted. Hosted enablement follows with htpasswd users +
inbox + lane.

### D6 — Per-actor verb allowlist, static first
A committed config maps actor -> permitted verbs (disposing possibles vs
ratifying proposals are different authorities). Binding to the full
roles-authority-model is deferred to a later delta; the config's SHAPE
anticipates it.

## Risks / Trade-offs

- **Latency between click and merged truth** -> overlay chips + on-apply
  rebake (D1); worst case the nightly closes it.
- **Inbox as attack surface** -> dispatch-only credential (D2) + apply-lane
  revalidation of everything + same-origin ingress auth.
- **Intent spam / replay** -> per-actor allowlist, inbox rate limit,
  idempotency key (actor, verb, target, snapshot_rev_seen digest); the lane
  skips already-applied duplicates.
- **Two sources on screen (snapshot + feed)** -> the feed NEVER mutates
  view-model state; it only decorates tiles and fills the refusal panel.

## Migration Plan

1. Land the gate-intent kernel + examples + validator delta (openxFactory).
2. codexFactory: local executing gate routes + dispose tray (D5) — ships
   value immediately with zero new infra.
3. omnigent-install: per-user htpasswd + ingress actor forwarding; inbox
   service deployment. Aggregation: apply-lane workflow.
4. Enable hosted tray -> intents; batched rolling PR; on-apply rebake.
5. Flutter verdict terminal consumes the same two endpoints (own feature).

Rollback at any stage: disable the inbox route (hosted falls back to
read-only + descriptors); the local surfaces and kernel remain valid.

## Open Questions

- Inbox hosting shape (sidecar vs deployment) — realization.
- Intent retention (committed forever beside records vs pruned with the
  record as durable trace) — realization, default keep-forever.
- Apply cadence (per-intent dispatch vs micro-batch) — realization, default
  per-intent with debounce.
