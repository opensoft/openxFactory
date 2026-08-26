---
code_surface: codexFactory (dispose tray + intent-feed overlay + refusal panel in the dashboard bundle, local executing gate routes behind the loopback gate, apply-lane orchestration module), openxFactory (gate-intent kernel schema + examples + delegated validator rules, document-lifecycle delta), omnigent-install (intent-inbox service deployment + per-user ingress auth), xFactory aggregation (apply-lane workflow wiring)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
Status: ratified
Ratified: 2026-07-23 by Brett — "we are there, this is ready now to lock", recorded in the proposal commit cf1c3d0 and in the README OpenSpec Records row
---

# Proposal: add-ideation-intent-plane

## Why

The ideation dashboard became the team's shared surface (the wheel, the
funnel, the register), and on 2026-07-23 the first full derive->dispose
cycle ran end-to-end — but every ACTION still requires a terminal: the gate
console's verbs (demote / ratify / edit-apply / kickoff / dispose-possible)
execute only via CLI against a local checkout, and the hosted dashboard is
read-only by construction (D16). Brett's direction (dashboard-action-center
brainstorm): make the dashboard "the action center where the user will
manage the process" — from the hosted web AND from mobile — without
weakening D16.

The reframe that unlocks it: the dashboard never gains write authority; a
click emits a signed, attributed INTENT, and the existing gate-console
engine — the only executor — applies it through the governed lane machinery.
Same verbs, same records, same audit chain; one new artifact class, which is
honest anyway ("Brett decided X at 12:04" exists before it is applied).

## What Changes

- ADD the `gate-intent` kernel: a request artifact (actor, verb, target,
  args, requested_at, snapshot_rev_seen, status pending|applied|refused with
  refusal reason) — never a write itself; validated by the delegated
  dashboard-family validator.
- ADD the intent-inbox service contract: the ONLY new credentialed
  component, holding `actions:write` on ONE workflow (dispatch-only, no
  repository contents authority); stamps the actor from the
  ingress-authenticated username; enforces a per-actor verb allowlist.
- ADD the apply lane: replays intents through the gate-console verbs against
  a fresh checkout with FULL server-side revalidation (the browser is
  untrusted), refuses intents formed against a stale view
  (snapshot_rev_seen), and commits intent + gate-action record + updated
  artifacts TOGETHER via the rolling-PR pattern. Second-touch DECIDED:
  custody-not-decision — batched auto-merge on approval in the existing
  Merge-Master ritual; the apply lane may trigger snapshot rebake on
  success.
- ADD two-plane rendering to the dashboard: the deterministic snapshot stays
  the only view-model source; a live intent feed overlays per-tile
  pending/applied/refused chips and a refusal panel.
- ADD the first hosted verb: the dispose-possible tray on pending_review
  tiles (wheel + canvas), plus LOCAL executing gate routes behind the
  existing loopback gate (upgrading the descriptor-only gate bar).
- ADD the identity ladder: per-user Basic Auth entries with
  ingress-forwarded actor now; Keycloak later replaces the authenticator
  without changing the intent contract. Hosted web and the Flutter
  verdict-terminal app are the same client class (snapshot consumer +
  intent emitter; no on-device checkout).
- MODIFY `document-lifecycle`: the GATES-HAPPEN-ON-MAIN rule — a lifecycle
  transition is not real until merged to main; unmerged transitions are
  exploration, not status.

## Impact

- New capability spec `ideation-intent-plane`; document-lifecycle delta.
- New kernel schema `gate-intent` + packaged examples + delegated validator
  rules (additive; no bump of existing kernels).
- codexFactory dashboard bundle grows the tray/overlay/refusal surfaces and
  local executing routes; a new apply-lane module joins the doc-health lane
  family; omnigent-install gains the inbox deployment and per-user auth;
  the aggregation repo gains the apply workflow.
- The deployed serving pod remains credential-free and read-only (D16
  intact) — verified by the existing boundary tests plus new intent tests.
