# avatar-first-ui Specification

## Purpose
TBD - created by archiving change align-avatar-first-ui-standard. Update Purpose after archive.
## Requirements
### Requirement: Adaptive shell over orthogonal runtime state
An xFactory avatar client SHALL provide the domain-neutral regions
`avatar_stage`, `conversation_rail`, `context_panel`, `action_bar`,
`handoff_panel`, and `settings_panel`, and SHALL support `conversation`,
`work`, and `review` presentation modes as client-local state that never
conflates with the authoritative axes defined by `avatar-client-runtime`
(session lifecycle, control health, media state, workflow projection).

Conversation mode SHALL prioritize guided voice and text interaction. Work
mode SHALL prioritize structured fields, exact values, and evidence. Review
mode SHALL prioritize confirmations, consent, conflicts, and outcomes. Mode
changes SHALL preserve applicable logical session, workflow, persona, focus
target, pending decision, state revision, and trace context. The avatar MAY
become visually secondary but MUST NOT obscure structured work or claim
authority.

#### Scenario: User begins guided intake
- **WHEN** an authorized user starts avatar-guided service intake
- **THEN** conversation mode MUST expose the avatar, conversation state, required controls, and current workflow context

#### Scenario: Consequential values require review
- **WHEN** names, identifiers, dates, money, addresses, consent, or proposed effects must be entered or confirmed
- **THEN** the client MUST expose complete display-safe values in work or review mode and MUST NOT require voice-only confirmation

#### Scenario: Authoritative snapshot replaces stale projection
- **WHEN** recovery supplies a newer AVC-12 snapshot
- **THEN** the shell MUST reconcile to the snapshot, retain only valid local presentation preferences, and surface any discarded pending local intent

### Requirement: Hermes-layer surface defaults
Customer Hermes surfaces SHALL default to avatar-first interaction, Client
Hermes surfaces SHALL default to a hybrid avatar and conventional interface,
and Domain Hermes surfaces SHALL default to a conventional interface with an
avatar analyst or copilot. A DomainxFactory override SHALL identify the user
set, workflow need, risk class, accessibility fallback, and authority
boundary.

#### Scenario: Customer needs guided explanation
- **WHEN** a customer or subject performs intake, preference capture, consent discussion, comprehension checking, or handoff
- **THEN** the primary flow MUST be available through avatar guidance while exact facts, decisions, and records remain available in structured UI

#### Scenario: Client operator performs repeated work
- **WHEN** staff, operators, managers, approvers, or tenant administrators use dashboards, queues, rosters, integrations, or bulk operations
- **THEN** the conventional work surface MUST remain primary or immediately available while the avatar provides guidance and explanation

#### Scenario: Domain authority reviews policy
- **WHEN** a domain expert, maintainer, reviewer, or governance council edits policy, schemas, routing, evidence, or audit records
- **THEN** the conventional review surface MUST remain primary and the avatar MUST NOT replace the authoritative artifact

### Requirement: Flutter client and web-console responsibility split
The reusable avatar interaction client SHALL be implemented in Flutter with
Windows desktop and web as the first qualification targets, owning the
conversation experience, adaptive shell, deterministic local projection,
standard controls, persona presentation, read-only workflow summaries, and
handoff initiation. Dense administration, policy editing, bulk operations,
interactive workflow editing, and audit investigation SHALL remain in a
separate conventional web console governed by the existing
workflow-visualization specification.

The client MAY render a read-only canonical workflow summary and MAY offer
web-console handoff. Handoff URLs MUST NOT carry bearer tokens, subject
identifiers, transcripts, or provider secrets, and any future handoff
exchange MUST be server-issued, one-time, purpose-bound, and reauthorized at
the web boundary. The exchange protocol itself is deferred until the web
console exists. The client MUST NOT introduce a second interactive
workflow-canvas standard.

#### Scenario: User reviews workflow status in the client
- **WHEN** the avatar explains current, target, or blocked workflow state
- **THEN** the client MUST render a read-only canonical summary and MAY offer an authorized web-console handoff

#### Scenario: User edits workflow or policy
- **WHEN** an authorized user needs to edit workflows, inspect evidence graphs, bulk-operate, or change policy
- **THEN** the client MUST hand off to the conventional web console rather than embedding an editor

### Requirement: Standard controls, recording awareness, and fallback
The avatar client SHALL expose start, pause, stop, microphone mute,
captions, persona selection at session start, language, repeat, simple
explanation, more detail, human handoff, privacy/disclosure, and current
workflow-state controls whenever policy and platform permit; a missing
control SHALL have a documented policy or platform fallback.

The UI SHALL continuously distinguish microphone permission, capture
authorized or pending authorization, capture active, avatar listening, avatar
speaking, control degraded or lost, governed action pending, and retention
active. No status MAY be communicated by animation, audio, or color alone.
Stop and mute SHALL remain reachable whenever capture is possible. On control
loss the UI SHALL display the distinction between control loss and media loss
and present the stop, reconnect, or handoff options required by
`avatar-client-runtime`. AVC-02 denial and terminal results SHALL render only
their localization-safe message key, retry guidance, and approved fallback
modes; raw provider errors SHALL remain outside widget state.

#### Scenario: Microphone capture begins
- **WHEN** disclosure and consent pass, the user starts the session, and a matching authoritative `media_authorized` event arrives
- **THEN** the UI MUST present persistent visual and semantic capture state plus reachable mute and stop controls

#### Scenario: SDP answer is received before media authorization
- **WHEN** the trusted client media adapter has verified an AVC-02 grant and held provider answer but has not applied matching `media_authorized`
- **THEN** the UI MUST show media as connecting or pending, MUST NOT show capture or playback as active, and the adapter MUST leave the answer unapplied

#### Scenario: Session request returns a denial
- **WHEN** AVC-02 contains a denial or terminal result
- **THEN** the UI MUST present its safe message, retry state, and approved text, handoff, upgrade, or retry-later fallback without displaying provider error text

#### Scenario: Audio is unavailable
- **WHEN** microphone permission is denied, no device exists, media fails, or policy disables voice
- **THEN** the same eligible workflow MUST remain usable through text and structured controls without loss of authority or traceability

#### Scenario: Control is lost while audio remains connected
- **WHEN** the control lease becomes degraded or lost
- **THEN** the UI MUST distinguish control loss from media loss, show governed commands as disabled, and display the stop, reconnect, or handoff path

### Requirement: Accessibility and localization baseline
Windows desktop SHALL be the accessibility-qualified surface for the client
kernel, supporting keyboard-only operation, stable logical focus, visible
focus, screen reader labels and state announcements, captions, text-only
operation, reduced motion, high contrast, non-color cues, and zoom/reflow.
The web surface SHALL be screen-reader operable and keyboard operable with a
documented WCAG 2.2 AA exception register; the full web WCAG audit belongs
to the web-console change or the pilot gate. The qualified locale set SHALL
be English plus a pseudo-locale fixture covering long-string and
bidirectional rendering; additional locales are a successor change.

Avatar animation MUST NOT be required to understand listening, thinking,
speaking, interruption, control health, authority, errors, confirmations, or
outcomes. Dynamic status text MUST NOT resize fixed controls or cause
clipping, unreachable commands, or horizontal scrolling in the primary
workflow at qualified viewports.

#### Scenario: User enables reduced motion or text-only mode
- **WHEN** avatar and workflow state change through the acceptance catalog
- **THEN** every state, control, disclosure, caption, error, and outcome MUST remain perceivable and operable without motion or audio

#### Scenario: Pseudo-locale and zoom are applied
- **WHEN** the pseudo-locale long strings, bidirectional fixture, and maximum qualified zoom are applied
- **THEN** content MUST reflow without hiding, clipping, overlapping, or disabling required commands

#### Scenario: Screen reader follows a state transition
- **WHEN** media, control, confirmation, denial, failure, or handoff state changes
- **THEN** the client MUST announce the meaningful state once without repeatedly reading decorative avatar changes

### Requirement: Persona presentation and disclosure
Every selectable persona SHALL present a stable ID and version, role,
display name, required disclosure, supported languages, and lifecycle
status from the domain-owned catalog, and the client SHALL display the
persona's disclosure and record its ID and version before media starts.
Persona is fixed for the logical session; a persona change SHALL be
presented as ending the session and starting a new one, never as an
in-place substitution. Real-person impersonation SHALL default to
prohibited.

The client SHALL disclose that the user is interacting with an AI or
AI-assisted interface whenever the avatar could be mistaken for a human or
authoritative actor, SHALL display the current authority boundary, and
SHALL keep consent withdrawal reachable during the session. Before human
handoff shares context, the client SHALL display the target role, the exact
context classes to be shared, and the purpose, and SHALL let the user or
authorized representative remove optional context or decline sharing. The
UI SHALL distinguish requested, routing, accepted, unavailable, completed,
and canceled handoff states.

#### Scenario: User selects a persona before audio
- **WHEN** an active persona is permitted for the workflow and language
- **THEN** the client MUST display its disclosure and record its ID and version before media starts

#### Scenario: Persona is unavailable
- **WHEN** a persona is missing, suspended, retired, disallowed, or incompatible with the required language or profile
- **THEN** the client MUST refuse it and present an approved fallback without inventing a persona or voice

#### Scenario: User withdraws media consent
- **WHEN** the authoritative withdrawal event arrives
- **THEN** the UI MUST show capture and output stopped, show the resulting retention state, and offer only policy-valid text, exit, or handoff options

#### Scenario: Handoff context is reviewed
- **WHEN** a human handoff requires sharing workflow context
- **THEN** the client MUST show the share scope and purpose before dispatch and MUST record the resulting decision

### Requirement: Untrusted content and external-action rendering
The client SHALL treat transcript text, model output, tool summaries,
attachment names, URLs, visual result data, and provider error text as
untrusted, rendering plain text or a narrow sanitized format, and MUST NOT
render arbitrary HTML, executable content, provider-supplied widgets, or
unsafe URI schemes. External navigation and downloads SHALL use destination
allowlists, clear origin labeling, and policy-appropriate confirmation.

Provider text MUST NOT be used as an authority signal, confirmation, hidden
command, widget identifier, analytics key, or localization resource key.
Display-safe canonical fields from the authority boundary SHALL drive
consequential cards and actions.

#### Scenario: Model emits markup or a dangerous link
- **WHEN** transcript or model output contains HTML, script, custom URI schemes, or a non-allowlisted destination
- **THEN** the client MUST render it inert or reject it and MUST NOT execute, navigate, or load remote active content

#### Scenario: Tool summary contains command-like text
- **WHEN** a provider-generated summary appears to approve, deny, or complete an action
- **THEN** the UI MUST treat it as non-authoritative text until a matching canonical authoritative event arrives

### Requirement: Deterministic UI acceptance
Deterministic client slices SHALL use fixed clocks, IDs, fonts, locale
fixtures, platform capabilities, and canonical AVC commands, events, and
snapshots without a live model, and every acceptance scenario SHALL map to
automated evidence, manual evidence, or both. Avatar presentation-state
derivation SHALL conform to the landed neutral avatar-state derivation table
(the `avatar-lab-evidence` capability), which subsumes the former
interim-invariant-only posture; the deterministic fixture corpus SHALL give
every closed `media.state` — and the intake-remainder, takeover/recovery,
and `interrupted`/`handoff` scenario families — a replayable proof path
evidenced through kernel fields only. Golden tests SHALL render on
one pinned CI platform with one bundled font family including an
RTL-capable face, covering the qualified wide, narrow, and zoomed viewports
plus one long-string/bidirectional composite; high-contrast, reduced-motion,
and text-only verification SHALL use semantics and behavior assertions
rather than pixel goldens. Live provider tests SHALL reuse the same reducer
and view projections.

#### Scenario: Offline acceptance is replayed
- **WHEN** the same fixture, seed, decisions, and contract version run twice
- **THEN** canonical view state, commands, events, records, and normalized goldens MUST be equivalent

#### Scenario: Provider DTO reaches a widget test
- **WHEN** a widget or golden test depends directly on a provider event or model name
- **THEN** the test MUST fail architecture validation because widgets consume only canonical view state

#### Scenario: Required UI evidence is missing
- **WHEN** any required viewport, accessibility mode, control-loss state, confirmation state, or handoff state lacks evidence
- **THEN** the corresponding implementation slice MUST remain incomplete

#### Scenario: Derivation deviates from the landed table
- **WHEN** a client's presentation-state derivation resolves any axis combination differently from the landed avatar-state derivation table
- **THEN** the deviation MUST fail the client's authority-derivation acceptance rather than being carried as an implementation variance

#### Scenario: Closed media state lacks a kernel-evidenced fixture
- **WHEN** any of the ten closed `media.states` has no deterministic fixture evidencing it through kernel fields
- **THEN** state-reachability acceptance MUST report the gap as open rather than satisfied by presentation-field or derived-in-app evidence

