# Avatar-First UI Standard

Status: ratified
Ratified by: align-avatar-first-ui-standard
Kind: architecture
Repository context: openxFactory
Purpose: define the reusable user interface model for xFactories where an AI
avatar is the primary interaction surface.
Companion: [Workflow Visualization Standard](workflow-visualization-standard.md)
— sanctioned tooling and view coverage for the conventional visualization
surface beside the avatar.

## 1. Core Principle

An xFactory user interface should default to an avatar-first experience when
the work benefits from guided conversation, explanation, intake, review,
handoff, or ongoing collaboration.

The avatar is the primary presentation and interaction surface. It is not the
authority layer.

```text
User
  -> avatar-first UI
  -> conversation and media session
  -> governed xFactory workflow
  -> domain Omnigent execution
  -> Hermes policy, memory, and approval gates
  -> external enforcement or handoff system where applicable
```

The conventional UI still exists, but it supports the avatar. It should expose
controls, evidence, attachments, transcript, settings, structured choices, and
handoff actions without becoming the main workflow surface.

## 2. Ownership Boundary

openxFactory owns the generic avatar-first UI contract:

- interaction states
- channel separation
- required controls
- traceability and audit expectations
- persona and disclosure slots
- tool-call boundary shape
- handoff and escalation vocabulary
- accessibility and fallback requirements

Domain factory repos own domain specialization:

- approved persona catalogs
- domain tone and vocabulary
- domain-specific safety policies
- domain-specific tool classes
- domain-specific escalation triggers
- domain-specific human handoff roles
- domain-specific evidence and review records

MedxFactory can specialize this for patient-facing doctor and nurse agents.
codexFactory can specialize it for coding, review, planning, and repo
work. OpsxFactory can specialize it for operator and administrator workflows.
The avatar-first shell remains the same.

## 3. Standard Shell

Every avatar-first xFactory UI should define these regions.

```text
Avatar Stage
  the main visual or voice-first agent surface

Conversation Rail
  transcript, captions, user input, interruptions, and current turn state

Context Panel
  current workflow, selected subject, evidence, attachments, and pending
  decisions

Action Bar
  standard controls and domain-approved quick actions

Handoff Panel
  human escalation, expert routing, fallback mode, and emergency or blocked
  workflow handling where relevant

Settings Panel
  persona, language, captions, accessibility, privacy, and session controls
```

The shell may be rendered as web, mobile, desktop, kiosk, telehealth-style
session, voice-only session, or embedded widget. The contract is about
interaction structure, not a specific frontend framework.

## 4. Required Channels

Avatar-first UI must separate four channels.

```text
1. Avatar rendering channel
   Renders persona, motion, captions, status, disclosure, and handoff prompts.

2. Conversation and media channel
   Handles text, audio, video, captions, turn-taking, interruptions, and
   session lifecycle.

3. Workflow and tool channel
   Calls governed xFactory/domain tools. It must not store the only copy of
   domain state inside the realtime or avatar session.

4. Governance supervisor channel
   Monitors policy, scope, safety, escalation, audit, and blocked workflow
   conditions out of band from the speaking avatar.
```

These channels may run in one application, but their responsibilities must stay
separate in code, logs, audit records, and runtime permissions.

## 5. Standard Controls

The minimum reusable control set is:

```text
start session
pause or stop session
mute microphone
show or hide captions
switch persona
switch language
slow down
repeat
explain simply
show more detail
attach or share context
request human handoff
show privacy and disclosure
view transcript
view current workflow state
```

Domains may add controls, but they should not remove these unless the target
surface cannot support them. Missing controls require an explicit fallback.

## 6. Persona Contract

The standard persona object is domain-neutral.

```yaml
persona:
  id: string
  role: string
  presentation_style: string
  voice_style: string
  animation_level: none | low | subtle | moderate | rich
  supported_languages: []
  allowed_contexts: []
  required_disclosure: string
  impersonation_allowed: false
  status: draft | active | suspended | retired
  version: integer
```

Domain overlays decide whether the role is a doctor, nurse, coding guide,
operations copilot, bookkeeper, account strategist, claims assistant, or another
domain-specific role.

## 7. Disclosure And Trust

Every avatar-first UI must disclose that the user is interacting with a virtual
or AI-assisted interface when the avatar could reasonably be mistaken for a
human or authoritative actor.

Required rules:

- The avatar must not impersonate a real person unless the domain has explicit
  authorization and a disclosure policy.
- The avatar must not claim final authority when approval belongs to Hermes,
  accountable humans, or an external enforcement system.
- The user must be able to request a human or approved fallback where the
  domain supports one.
- High-risk domains must repeat disclosure or authority boundaries when context
  changes.

## 8. Tool Boundary

Avatar sessions may request tools, but governed backend services decide what is
allowed.

The standard boundary is:

```text
Avatar/conversation layer
  may ask for tools and render approved results

Workflow/tool layer
  validates tool request, scope, credentials, consent, approval, and risk

Hermes/openxFactory gates
  approve, deny, pause, escalate, or require review

Domain Omnigent
  executes bounded domain work
```

The avatar must not bypass approval, credential, traceability, or review gates.

## 9. Interaction States

Avatar-first sessions use these neutral states:

```text
idle
preflight
disclosure
preference_selection
active_conversation
tool_request_pending
workflow_waiting
comprehension_or_confirmation_check
handoff_requested
handoff_active
paused
completed
abandoned
blocked
escalated
archived
```

Domain factories may add states, but they should map back to these canonical
states for audit and cross-factory dashboarding.

## 10. Implementation Levels

Use the lowest level that satisfies the workflow and trust need.

| Level | Name | Use |
| --- | --- | --- |
| L0 | Text avatar | Simple guided chat with persona, transcript, controls, and workflow state. |
| L1 | Audio-first visual avatar | Voice, captions, portrait or simple generated avatar, subtle animation, handoff controls. |
| L2 | Live 2D or 3D avatar | Speech-driven motion, expressions, visemes, gesture states, and synchronized captions. |
| L3 | Streaming avatar vendor | Polished streaming avatar after vendor, privacy, audit, and retention review. |
| L4 | Custom realtime avatar engine | Domain-owned Unity, Unreal, WebGPU, or equivalent engine for high-control immersive UI. |

The default openxFactory recommendation is L1 for the first reusable product
surface. L2 can follow once trust, safety, workflow, accessibility, and
handoff flows are solid.

## 11. Hermes Layer UI Defaults

The three Hermes layers should not use the same UI balance by default. They
serve different user sets.

| Hermes layer | Best default | Primary user set | Why |
| --- | --- | --- | --- |
| Subject Hermes | Avatar-first | Customer subjects and their representatives | These users usually need guidance, explanation, preference capture, language support, trust, and handoff more than dense controls. |
| Tenant Hermes | Hybrid | Staff, operators, managers, approvers, and tenant administrators | These users need conversational help for ambiguity, but also fast queues, dashboards, approvals, rosters, configuration, and audit views. |
| Domain Hermes | Conventional-first with avatar copilot | Domain experts, reviewers, maintainers, governance owners, and specialist councils | These users need precision, policy editing, schema review, source promotion, routing tables, evidence review, and trace inspection. |

### Subject Hermes UI

Subject Hermes should be avatar-first.

Use avatar UI for:

- intake
- follow-up
- explanation
- preference capture
- consent or authorization discussion
- language switching
- comprehension or confirmation checks
- handoff requests

Use conventional UI for:

- structured fact confirmation
- timeline review
- document upload
- preference settings
- consent and sharing settings
- workflow status
- transcript and history review

### Tenant Hermes UI

Tenant Hermes should be hybrid.

Use avatar UI for:

- guided workflow launch
- triage explanation
- training and onboarding
- blocked-workflow explanation
- policy interpretation
- review packet summaries
- next-best-action guidance
- customer handoff preparation

Use conventional UI for:

- dashboards
- queues
- rosters
- permissions
- credential bindings
- integration status
- schedules
- approval lists
- reporting
- bulk operations

### Domain Hermes UI

Domain Hermes should be conventional-first with an avatar analyst or copilot.

Use avatar UI for:

- policy explanation
- review-council summary
- onboarding a domain maintainer
- comparing implementation options
- explaining why a request is high-risk
- drafting policy or schema changes

Use conventional UI for:

- policy editing
- schema and version management
- routing tables
- gate configuration
- evidence review
- source promotion
- evaluation metrics
- approval records
- audit logs
- diff and trace inspection

The avatar-first shell is still reusable across all three layers. The default
weighting changes: customer-facing surfaces emphasize conversation, operator
surfaces balance conversation with dense workflow controls, and domain
governance surfaces emphasize structured review with avatar assistance.

## 12. Domain Overlay Requirements

A domain factory that adopts avatar-first UI must provide:

```text
avatar-first UI profile
approved persona catalog or persona source
supported languages and fallback behavior
domain-specific disclosure text
allowed and restricted tool classes
handoff roles and routing
escalation triggers
audit and transcript retention policy
accessibility support
conventional UI fallback
```

Domain overlays may define whether the avatar is generated, selected from an
approved library, custom-rendered, voice-only, or disabled for a workflow.

## 13. Traceability

Every avatar-first session must be traceable to:

- user or subject reference, using a domain-approved identifier class
- client or tenant reference where applicable
- workflow ID
- session ID
- persona ID and version
- disclosure status
- selected language
- transcript or transcript policy
- tool requests and tool outcomes
- handoff or escalation events
- final workflow state

The transcript does not have to live in openxFactory. The contract requires
that a domain-approved storage and retention policy exists.

## 14. Domain Examples

MedxFactory:

```text
Patient-facing doctor or nurse avatar
  -> patient language, captions, comprehension checks, clinician handoff
```

codexFactory:

```text
Engineering avatar
  -> repo context, task planning, code review explanations, PR readiness
```

OpsxFactory:

```text
Operations avatar
  -> privileged-action preflight, change explanation, approval handoff
```

LedgerxFactory:

```text
Accounting avatar
  -> books review, document collection, exception explanation, accountant handoff
```

The surface pattern is shared. Domain policy decides what the avatar is allowed
to say, request, execute, or escalate.

## 15. Authoritative Runtime Axes And Presentation Modes

The avatar client reflects four **authoritative runtime axes** owned by
`avatar-client-runtime` and consumed read-only. It never authors them:

1. **session lifecycle** — broker-owned;
2. **control health** — lease-derived;
3. **media state** — trusted-adapter observation constrained by authority; and
4. **workflow projection** — Hermes/workflow-authority-owned.

Separately, `conversation`, `work`, and `review` are **client-local presentation
modes**. A surface MAY switch modes without changing any authoritative axis.
Conversation mode prioritizes guided voice and text; work mode prioritizes
structured fields, exact values, and evidence; review mode prioritizes
confirmations, consent, conflicts, and outcomes. Presentation state MUST NOT be
used to author, imply, or fabricate an authoritative transition.

A mode change MUST preserve the applicable logical session, workflow, persona,
focus target, pending decision, state revision, and trace context. When recovery
supplies a newer AVC-12 authoritative snapshot, the shell MUST reconcile to it,
retain only valid local presentation preferences, and surface any discarded
pending local intent. Consequential values (names, identifiers, dates, money,
addresses, consent, proposed effects) MUST be shown as complete display-safe
values in work or review mode and MUST NOT be confirmed by voice alone.

The neutral mapping from these four authoritative axes (with the AVC-12
`session_outcome` terminal) onto the six avatar presentation states is the
openxFactory-owned **avatar-state derivation table**, landed at
`contracts/avatar-client-lab/avatar-state-derivation-table.{md,yaml}` (change
`adopt-avatar-client-lab-candidates`); `deriveAvatarState` implements it and CI
gate (vi) tests against it.

## 16. Hermes-Layer Surface Defaults (Authoritative)

The defaults in §11 are the authoritative Hermes-layer surface defaults:
Subject Hermes is **avatar-first**, Tenant Hermes is **hybrid**, and Domain
Hermes is **conventional-first with an avatar analyst or copilot**. A
DomainxFactory override MUST record the user set, workflow need, risk class,
accessibility fallback, and authority boundary, and MUST NOT make avatar text
authoritative. Domain risk and accessibility overrides may move a surface toward
conventional UI but never remove the authority boundary.

## 17. Media Authorization, Held Answer, And AVC-02 Outcomes

The surface MUST continuously distinguish microphone permission, capture
authorized or pending, capture active, avatar listening, avatar speaking,
control degraded or lost, governed action pending, and retention active. No
status may be communicated by animation, audio, or color alone. Stop and mute
MUST remain reachable whenever capture is possible.

Receiving a held provider answer is **not** active media. When a trusted client
media adapter has verified an AVC-02 grant and holds a provider answer but has
not applied a matching `media_authorized` event, the UI MUST show media as
connecting or pending, MUST NOT show capture or playback as active, and the
adapter MUST leave the answer unapplied.

AVC-02 denial and terminal results MUST render only their localization-safe
message key, retry guidance, and approved fallback modes (text, handoff,
upgrade, or retry-later). Raw provider errors MUST remain outside widget state.
The AVC-02 result union is `grant | denial | terminal`.

## 18. Control Loss Versus Media Loss

Control loss (lease degraded or lost) is distinct from media loss. On control
loss the UI MUST display the distinction, show governed commands as disabled,
and present the stop, reconnect, or handoff options defined by
`avatar-client-runtime`. Audio may remain connected while control is lost; the
UI MUST NOT present a lost lease as a healthy governed session.

## 19. Persona Reference And Disclosure

The avatar-first profile carries a **persona reference only**: a stable persona
ID, version, and an optional non-secret catalog locator. The persona catalog
(schema and instances) is owned by the domain/kernel and is out of scope for
this standard. The resolved persona exposes role, display name, required
disclosure, supported languages, and lifecycle status. The client MUST display
the disclosure and record the persona ID and version before media starts.
Persona is fixed for the logical session; a persona change MUST be presented as
ending the session and starting a new one, never as an in-place substitution.
Real-person impersonation defaults to prohibited. An unresolved persona
reference MUST fail closed to an approved fallback; the client MUST NOT invent
persona identity, voice, or data.

The client MUST disclose an AI or AI-assisted interface whenever the avatar
could be mistaken for a human or authoritative actor, MUST display the current
authority boundary, and MUST keep consent withdrawal reachable during the
session.

## 20. Safe Rendering Of Untrusted Content

Transcript text, model output, tool summaries, attachment names, URLs, visual
result data, and provider error text are untrusted. The client MUST render them
as plain text or a narrow sanitized format and MUST NOT render arbitrary HTML,
executable content, provider-supplied widgets, or unsafe URI schemes. External
navigation and downloads MUST use destination allowlists, clear origin labeling,
and policy-appropriate confirmation. Provider text MUST NOT be used as an
authority signal, confirmation, hidden command, widget identifier, analytics
key, or localization resource key. Display-safe canonical fields from the
authority boundary drive consequential cards and actions.

## 21. Client And Web-Console Boundary And Handoff

The reusable client owns the conversation experience, adaptive shell,
deterministic local projection, standard controls, persona presentation,
read-only workflow summaries, and handoff initiation. Dense administration,
policy editing, bulk operations, interactive workflow editing, and audit
investigation remain in the conventional web console governed by the
workflow-visualization standard. The client MUST NOT introduce a second
interactive workflow-canvas standard.

Handoff URLs MUST carry no bearer token, subject identifier, transcript, or
provider secret. Any future handoff exchange MUST be server-issued, one-time,
purpose-bound, and reauthorized at the web boundary; the exchange protocol is
deferred until the web console exists.

## 22. Accessibility And Localization Evidence Boundary

This standard **declares** an accessibility baseline: keyboard-only operation,
stable and visible focus, screen-reader labels and single meaningful state
announcements, captions, text-only operation, reduced motion, high contrast,
non-color cues, zoom/reflow, and English plus a long-string/bidirectional
pseudo-locale. Avatar animation MUST NOT be the sole carrier of listening,
thinking, speaking, interruption, control health, authority, errors,
confirmations, or outcomes.

These declared requirements are distinct from later platform qualification
evidence. Windows desktop qualification, the web WCAG 2.2 AA audit and its
exception register, widget semantics, pinned-font goldens, and additional
locales are owned by named successors (`implement-avatar-client-lab`,
`avatar-pilot-hardening`), not by this standard.

## 23. Profile Carrier And Deterministic Validation

The registered `avatar-first-ui-profile` schema is the domain overlay carrier.
New runtime fields are additive with explicit closed (fail-closed) defaults, so
existing static profiles remain valid. Runtime compatibility is pinned by exact
content-addressed coordinates (baseline identity and digests during parallel
work; released bundle tag, exact commit, and registry/interface-lock digests at
realization) — never a loose released version range. Readiness, heartbeat, and
lease values are per-profile selections validated against kernel-owned ceilings
resolved read-only; consent-purpose mappings reference the three neutral IDs;
the retention overlay references externally owned retention-policy IDs only.

The offline validator (`scripts/validate-avatar-first-ui.py`) checks schema,
template, examples, and fixtures with no provider or runtime service, emitting a
stable error/evidence ID for each rejected rule. Deterministic UI fixtures live
under `examples/avatar-first-ui/fixtures/`.

## 24. Requirement-To-Owner Map

Each avatar-first behavior has exactly one owner. Deferred behavior names a
successor and keeps a closed default.

| Behavior | Owner |
| --- | --- |
| Four authoritative runtime axes; control-loss options | `avatar-client-runtime` (read-only) |
| Capability, outcome, consent-purpose, state registries; timing ceilings | AVC kernel registries (read-only) |
| Presentation modes, shell, controls, safe rendering, persona reference, profile carrier, offline validation | this standard + `avatar-first-ui-profile` schema/validator |
| Hermes-layer surface defaults | this standard (Hermes layers apply them) |
| Flutter widgets, provider adapters, goldens, live-provider evidence | `implement-avatar-client-lab` |
| Formal accessibility qualification, domain onboarding | `avatar-pilot-hardening` |
| Conventional web console, workflow editor | workflow-visualization standard |
| Domain persona catalogs, retention policies, domain profiles/mappings | DomainxFactory repositories |
