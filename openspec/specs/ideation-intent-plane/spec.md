# ideation-intent-plane Specification

## Purpose

Define how a surface that holds no write authority can nevertheless be the place
where decisions are taken. A click on the hosted dashboard — or on a mobile
client — emits a `gate-intent` carrying the actor, the verb, the target, the
args, the `snapshot_rev_seen` the actor was looking at and a one-way status, and
the gate-console engine, still the only executor of a gate verb, replays it
against a fresh checkout with full server-side revalidation before anything is
written. The serving surface keeps no repository credential and gains no write
route, so the read-only posture the hosted dashboard was built on is preserved
rather than traded away for the ability to act.

Keep the authority minimal and the accounting honest at every step. Exactly one
new credentialed component exists — the intent inbox — and it holds dispatch
authority over a single apply workflow and no repository-contents authority; it
stamps the actor from the ingress-authenticated identity rather than from
anything the browser claimed, and enforces a per-actor verb allowlist before it
dispatches. The lane refuses an intent formed against a materially stale view,
records every refusal with its reason rather than dropping it, and lands an
applied intent together with its gate-action record and the artifacts it moved in
one commit. The rolling pull request that carries them is CUSTODY under the
repository's own rulesets and never a second decision gate — the authenticated
intent was the decision.

And keep the two planes as separate on the screen as they are in the record: the
deterministic snapshot stays the only view-model source, while a live intent feed
overlays per-tile pending / applied / refused indicators and a refusal panel
without mutating it. Identity climbs its own ladder underneath — per-user
authentication at the ingress first, SSO afterwards — without the intent contract
moving, because the client class is the same either way: a snapshot consumer that
emits intents and holds no checkout on the device. `dispose-possible` is the first
verb to cross, offered locally through loopback-gated executing routes and
remotely through intents, both driving the same engine to the same register
lifecycle outcome.

## Requirements

### Requirement: Intents are requests, never writes
A dashboard or mobile action SHALL be captured as a `gate-intent` artifact — actor, verb, target, args, requested_at, the `snapshot_rev_seen` the actor was viewing, and a status of `pending`, `applied`, or `refused` (with a refusal reason) — and no serving surface (hosted dashboard pod, mobile app) SHALL hold write authority or repository credentials; the gate-console engine remains the only executor of gate verbs.

#### Scenario: A hosted click becomes an intent
- **WHEN** an authenticated user activates an action affordance on the hosted dashboard
- **THEN** a `gate-intent` is created carrying the ingress-authenticated actor and the snapshot revision they were viewing
- **AND** no write occurs on the serving surface

#### Scenario: The serving pod stays credential-free
- **WHEN** the intent plane is enabled for the hosted dashboard
- **THEN** the serving image carries no repository credential and no write route beyond intent emission

### Requirement: Minimal-authority intent inbox
The intent inbox SHALL be the only new credentialed component, holding dispatch authority over exactly one apply workflow and no repository-contents authority; it SHALL stamp the actor from the ingress-authenticated identity (never from the request body) and SHALL enforce a per-actor verb allowlist before dispatch.

#### Scenario: A forged actor is ignored
- **WHEN** a request body claims an actor different from the ingress-authenticated user
- **THEN** the inbox stamps the authenticated identity and discards the claimed one

#### Scenario: An unauthorized verb is refused at the inbox
- **WHEN** an authenticated user submits an intent for a verb outside their allowlist
- **THEN** the inbox refuses it with a recorded reason and dispatches nothing

### Requirement: Apply lane revalidates and commits atomically
The apply lane SHALL replay each intent through the gate-console engine against a fresh checkout with full server-side revalidation (verb authority, target existence, lifecycle legality, validator-clean artifacts), SHALL refuse an intent whose `snapshot_rev_seen` is materially stale for its target, and SHALL commit the applied intent, its gate-action record, and the updated governed artifacts together, delivered via the rolling-PR pattern.

#### Scenario: A stale-view intent is refused
- **WHEN** the target's governed state has materially advanced past the intent's snapshot_rev_seen
- **THEN** the lane refuses the intent with a stale-view reason and persists nothing

#### Scenario: Applied atomically
- **WHEN** an intent is applied
- **THEN** the intent (status applied), the gate-action record, and the updated artifacts land in the same commit

#### Scenario: A refused intent is visible
- **WHEN** the lane refuses an intent for any reason
- **THEN** the intent's status and reason are recorded and surfaced to the intent feed, never silently dropped

### Requirement: Second touch is custody, not decision
The authenticated intent SHALL be treated as the human decision; the rolling intents PR SHALL be custody under repository rulesets — batched, auto-merge on approval — and MUST NOT be construed as a second decision gate; the apply lane MAY trigger snapshot regeneration on successful application so verdicts publish promptly.

#### Scenario: Batched custody
- **WHEN** several intents apply during one period
- **THEN** they deliver on one rolling PR whose approval is a custody act within the existing merge ritual

### Requirement: Two-plane rendering
The deterministic snapshot SHALL remain the only view-model source; a live intent feed SHALL overlay per-tile pending/applied/refused indicators and a refusal panel, and the overlay MUST NOT mutate snapshot-derived state.

#### Scenario: Immediate feedback without forking truth
- **WHEN** a user submits an intent
- **THEN** the affected tile shows a pending indicator from the feed while the snapshot remains unchanged until the applied state is baked

### Requirement: Identity ladder without contract change
Actor identity SHALL come from per-user authentication at the ingress (per-user Basic Auth entries first), forwarded as the intent's actor; replacing the authenticator (Keycloak SSO) MUST NOT change the intent contract. Hosted web and mobile clients SHALL be the same client class — snapshot consumer plus intent emitter — with no repository checkout on any client device.

#### Scenario: SSO swap is contract-invisible
- **WHEN** the ingress authenticator is replaced by SSO
- **THEN** intents carry the same actor field semantics and no schema change is required

### Requirement: Dispose tray is the first verb
The dispose-possible verb SHALL be the first action surfaced — accept, reject (reason and citation required), defer — on pending_review possible tiles, available on the LOCAL dashboard through loopback-gated executing routes and on the hosted dashboard through intents, both driving the same gate-console engine and register lifecycle rules.

#### Scenario: Hosted and local trays agree
- **WHEN** the same disposition is performed via the local executing route and via a hosted intent
- **THEN** both produce the same register lifecycle outcome and equivalent gate-action records differing only in transport provenance
