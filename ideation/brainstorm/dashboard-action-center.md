# Dashboard Action Center — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Evolve the hosted ideation dashboard from a read-only projection into
the action center where a human manages the whole ideation process — WITHOUT
weakening D16: the dashboard never gains write authority; instead a click
emits a signed, audited INTENT that the existing gate-console engine applies
through the governed lane machinery (validate-before-persist, gate-action
records, rolling-PR delivery). Locked at capture: intent-queue-plus-lane over
an action-API sidecar; per-user htpasswd identity first (Keycloak SSO later,
shared with the NotebookLM share-list plan); the dispose-possible tray ships
first as the proof verb.
Topics: ideation-dashboard, gate-console, interactivity-boundary, intent-queue, possibles-register, roles-authority-model, keycloak, identity-brokering, doc-management, doc-workflow
Repository context: openxFactory (capability owner; realization spans codexFactory + omnigent-install + xFactory aggregation)
Captured: 2026-07-23

## The reframe (Brett + session, 2026-07-23)

Read-only-ness is D16 working, not a limitation to remove. "Make the
dashboard writable" decomposes into "let my click become a governed action":
the hosted surface becomes an INTENT EMITTER; write authority stays where it
already lives (the gate-console engine + factory-identity lane + rolling-PR
delivery). Same verbs, same records, same audit chain — one new artifact
class, the intent, which is honest anyway ("Brett decided X at 12:04" exists
even before it is applied). Captured the same day the first real
gate-disposition cycle ran end-to-end (three ai-derived possibles accepted
via `gate dispose-possible`).

## Locked directions (this capture)

1. **Write plane: intent queue + lane.** A minimal intent-inbox service
   behind the SAME ingress (`/api/intents`): POST accepts a verb intent,
   stamps `actor` from the ingress-authenticated username, dispatches the
   apply workflow. Its credential is `actions:write` on ONE workflow — never
   `contents:write`; it can wake the machinery but cannot touch the repo.
   The serving pod itself keeps zero credentials (unchanged).
2. **Identity: per-user htpasswd first.** Replace the shared password with
   per-user Basic Auth entries; ingress forwards the username as the actor
   for HumanGate. Keycloak SSO (existing keycloak-identity-brokering
   brainstorm) replaces it later without changing the intent contract — and
   the dashboard becomes SSO consumer #2 beside the NotebookLM share-list
   plan, strengthening the case for standing Keycloak up.
3. **First verb: the dispose tray.** Accept / reject(reason+citation) /
   defer buttons on pending_review possible tiles (wheel + canvas) — the
   engine (`gate_console.dispose_possible`, codexFactory PR #33) and the
   record contract (gate-action-record `dispose-possible`, e9b4a94) are
   fully built; only the surface and the intent path are new.

## Architecture sketch

- **Intent** (new kernel candidate `gate-intent`): actor, verb, target,
  args, requested_at, `snapshot_rev_seen` (optimistic concurrency — the
  executor refuses an intent formed against a stale view; the register
  fingerprint CAS is the precedent), status
  (pending|applied|refused + refusal reason).
- **Two-plane rendering.** The deterministic snapshot stays the only truth
  the views derive from; a small live intent feed (GET `/api/intents`, same
  auth) overlays pending/applied/refused chips per tile. No snapshot-purity
  loss; the overlay retires when the next snapshot confirms.
- **Executor = the existing console.** An apply lane (workflow) replays
  intents through the gate-console verbs with the intent's actor:
  server-side revalidation of everything (the browser is untrusted),
  validate-before-persist, intent + gate-action record + updated artifacts
  committed TOGETHER, delivered via the rolling-PR pattern.
- **Refusal ledger becomes UI.** GateRefused/boundary refusals render as a
  panel ("rejection refused: citation required") — the moment the surface
  feels like a console rather than a report.
- **Authority map.** Verb allowlist per actor (roles-authority-model
  tie-in): disposing derived possibles vs ratifying proposals are different
  authorities; the inbox enforces coarse verb access, the executor enforces
  the real rule.
- **Latency.** The apply lane triggers snapshot regeneration + image rebake
  on success (minutes), nightly as backstop; the overlay covers the gap.

## Action inventory (roughly in shipping order)

dispose-possible tray → pick-at-organize-gate wizard (accepted possible →
staged-topic scaffold; the next verb Brett actually needs) → human-seen
cluster submission (lens, already engine-backed) → create-brainstorm
authoring (create-only; boundary-legal today) → ratify / demote / kickoff
gate bars hosted → rolling-PR approval deep-links with status chips →
re-run-lane-on-demand.

## Open questions

- **Second-touch problem.** The click IS the decision, but org rulesets mean
  the commit lands via an approved PR. Batch the day's intents into one
  rolling PR approved in the existing Merge-Master ritual (lean), or treat
  PR approval as custody-not-decision with auto-merge on the actor's own
  approval? Decide at staging.
- Intent inbox hosting shape: sidecar container in the dashboard pod vs its
  own deployment (isolation vs simplicity); either way ingress-authed and
  repo-credential-free.
- Does the intent kernel live in the gate-action-record family or as its own
  schema? (It is a REQUEST, not a record of an applied action.)
- Multi-user semantics once htpasswd has more than one name: per-actor
  pending views, and whether disposition authority is per-cluster/per-domain.
- Whether the avatar-first-ui standard applies to the action center (a
  conversational disposition flow) or stays out of scope for v1.

## Possible feats

- Intent-queue contract (gate-intent kernel + inbox service + apply lane).
- Dispose tray on wheel/canvas pending tiles (hosted, intent-backed).
- Pick-at-organize-gate wizard from an accepted possible.
- Per-user htpasswd identity with ingress-forwarded actor.
- Refusal-ledger UI panel.
