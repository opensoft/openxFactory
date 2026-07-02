# Avatar-First UI Standard

Status: shared xFactory standard
Repository context: openxFactory
Purpose: define the reusable user interface model for xFactories where an AI
avatar is the primary interaction surface.

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
| Customer Hermes | Avatar-first | Customer subjects and their representatives | These users usually need guidance, explanation, preference capture, language support, trust, and handoff more than dense controls. |
| Client Hermes | Hybrid | Staff, operators, managers, approvers, and tenant administrators | These users need conversational help for ambiguity, but also fast queues, dashboards, approvals, rosters, configuration, and audit views. |
| Domain Hermes | Conventional-first with avatar copilot | Domain experts, reviewers, maintainers, governance owners, and specialist councils | These users need precision, policy editing, schema review, source promotion, routing tables, evidence review, and trace inspection. |

### Customer Hermes UI

Customer Hermes should be avatar-first.

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

### Client Hermes UI

Client Hermes should be hybrid.

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
