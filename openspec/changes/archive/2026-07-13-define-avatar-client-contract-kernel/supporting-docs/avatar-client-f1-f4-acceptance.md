# Avatar Client F1-F4 Acceptance Scenarios

Status: superseded
Kind: acceptance design
Captured: 2026-07-10
Updated: 2026-07-10 after lead architecture review
Superseded: 2026-07-10
Superseded by: avatar-client split proposal set
Relocation note: historical body frozen; supersession links updated for the split
Repository context: openxFactory (contract-level, cross-factory topic)
Proposed by: define-avatar-client-runtime
Staging ID: openxFactory:staging:avatar-client
Target capabilities: avatar-first-ui, avatar-client-runtime
Parent:
[Flutter Avatar Client And UI Lab](flutter-avatar-client-ui-lab.md)
Contracts:
[Avatar Client Neutral Runtime Contracts](avatar-client-neutral-contracts.md)

> Historical pre-review input. Do not implement this F1-F4 catalog from the
> current change. The authoritative scope is the
> [kernel design](../design.md), [runtime delta](../specs/avatar-client-runtime/spec.md),
> [UI delta](../../align-avatar-first-ui-standard/specs/avatar-first-ui/spec.md),
> and [parallel plan](avatar-client-parallel-workstream-plan.md). Flutter
> slice acceptance moves to `implement-avatar-client-lab`.

This superseded proposal supporting document is non-normative. It preserves
the acceptance intent considered before the change was reduced to the
openxFactory contract and reference-runtime kernel.

## Acceptance Harness

| Layer | Purpose |
| --- | --- |
| Contract fixture tests | Validate AVC-01 through AVC-12 parsing, authority, sequencing, redaction, and compatibility |
| Flutter unit tests | Validate reducers, state transitions, normalization, and offline draft logic |
| Flutter widget tests | Validate controls, semantics, focus order, state rendering, and error presentation |
| Golden tests | Detect layout, clipping, overlap, and visual-state regressions |
| Flutter integration tests | Exercise complete service-intake, confirmation, approval, and handoff flows |
| Windows and web smoke tests | Prove target-platform startup, offline operation, persistence, and keyboard/microphone permissions |
| Manual accessibility review | Screen reader, captions, reduced motion, contrast, zoom, and text-only review |

Automated tests must use deterministic clocks, IDs, and fixtures. A live model
is prohibited in F1-F4 acceptance because nondeterministic output would make the
UI contract difficult to prove.

## Viewport Matrix

Golden and interaction tests cover at least:

| ID | Target | Size | Purpose |
| --- | --- | --- | --- |
| VP-01 | Windows wide | 1440 x 900 | Normal operator desktop |
| VP-02 | Windows compact | 1024 x 768 | Constrained desktop/window |
| VP-03 | Web wide | 1366 x 768 | Common browser viewport |
| VP-04 | Web narrow | 390 x 844 | Responsive browser fallback; not native-mobile acceptance |
| VP-05 | Web zoom | VP-03 at 200% text/zoom | Reflow and text-fit verification |

No acceptance viewport may contain incoherent overlap, clipped commands,
unreachable controls, horizontal page scrolling for the primary workflow, or
text that becomes unreadable inside a fixed control.

## Fixture Catalog

| Fixture | Purpose |
| --- | --- |
| `service_intake_happy_path` | Complete request through governed-action proposal |
| `service_intake_missing_information` | Avatar requests required scope information |
| `service_intake_correction` | User corrects a consequential captured value |
| `service_intake_decline` | User declines confirmation or consent |
| `tool_approval_pending` | Tool proposal waits without implying completion |
| `tool_denied` | Hermes denies a proposed action with explanation |
| `tool_failed` | Approved tool fails and offers recovery/handoff |
| `policy_channel_lost` | Hermes/control path disappears while UI remains connected |
| `human_handoff` | User or policy requests an accountable human |
| `offline_draft_resume` | Draft survives restart without network access |
| `offline_draft_conflict` | Server revision conflicts with a resumed local draft |
| `unsupported_capability` | Required voice or language capability is unavailable |
| `persona_catalog` | Two approved personas and one suspended persona |
| `command_stale_revision` | Command is rejected against a newer authoritative revision |
| `event_gap_snapshot_recovery` | Missing authoritative predecessor forces AVC-12 recovery |
| `session_takeover` | A new client epoch revokes the prior lease and media leg |
| `control_lease_expired` | Provider media cannot outlive authoritative control lease |
| `unsafe_content` | Markup, URI, and provider authority claims remain inert |

Each fixture includes canonical AVC-11 commands, AVC-04 observations and
authoritative events, AVC-12 snapshots, expected state revisions, visible text
keys, retention classes, and prohibited outcomes.

## F1 Shell

### F1-001 Required regions render

- **Given** an approved UI profile and persona
- **When** the shell opens at each VP-01 through VP-04 viewport
- **Then** avatar stage, conversation rail, context panel, action bar, handoff,
  and settings are reachable
- **And** the current interaction mode is visually identifiable without help
  text
- **And** no region overlaps or resizes because status text changes

### F1-002 Adaptive modes preserve context

- **Given** an active session in conversation mode
- **When** the user opens a structured task and then a review surface
- **Then** the shell transitions conversation -> work -> review
- **And** the same session, workflow, persona, transcript position, and pending
  decision remain selected
- **And** the avatar docks rather than disappearing in review mode

### F1-003 Keyboard-only operation

- **Given** no pointer input
- **When** the user navigates the complete shell
- **Then** every command and input is reachable in a stable logical order
- **And** focus is visible
- **And** opening and closing panels returns focus to the initiating control
- **And** no keyboard trap exists

### F1-004 Reduced motion and text-only modes

- **Given** reduced motion or text-only mode
- **When** avatar state changes through idle, listening, thinking, speaking,
  interrupted, blocked, and handoff
- **Then** each state remains distinguishable without motion
- **And** no essential information exists only in animation or audio

### F1-005 Persona selection and continuity

- **Given** two active personas and one suspended persona
- **When** the user opens persona selection before the session starts
- **Then** only active allowed personas are selectable
- **And** each presents its required disclosure and supported languages
- **When** the user selects one and starts the session
- **Then** persona ID and version remain stable throughout that session

### F1-006 Text and zoom fit

- **Given** the longest localized fixture strings and VP-05
- **When** every panel, action, status, and confirmation renders
- **Then** text wraps or scrolls within its content region
- **And** commands remain operable
- **And** text does not cover preceding or subsequent content

### F1-007 Recording and authority state are always apparent

- **Given** microphone, media, control, retention, and governed-action states
- **When** each state changes independently
- **Then** capture, sending, listening, speaking, control loss, retention, and
  action authority are each visible and announced semantically
- **And** mute and stop remain reachable whenever capture is possible
- **And** no state depends on color, audio, or animation alone

### F1-008 Untrusted content remains inert

- **Given** transcript, model, attachment, and tool-summary fixtures containing
  HTML, scripts, unsafe URI schemes, and false approval/completion language
- **When** the content renders
- **Then** active content and unsafe navigation are blocked
- **And** provider text never changes authoritative UI state
- **And** only canonical Hermes/workflow fields enable consequential commands

## F2 Deterministic Session

### F2-001 Offline startup

- **Given** network access is disabled
- **When** the UI lab starts
- **Then** scenario selection, fixture loading, and all deterministic session
  controls work
- **And** no hidden network request is required
- **And** live voice is visibly unavailable with a concise connectivity state

### F2-002 Canonical state coverage

- **Given** the deterministic scenario catalog
- **When** the complete catalog runs
- **Then** every canonical avatar session state is reached by at least one
  fixture
- **And** each state has one expected visual snapshot and one event assertion

### F2-003 Repeatable replay

- **Given** the same fixture, seed, deterministic clock, and initial profile
- **When** the fixture is replayed twice
- **Then** canonical states, source event ordering, visible outputs, and retained
  records are identical
- **And** generated IDs are stable or normalized before comparison

### F2-004 Pause, stop, and resume

- **Given** an in-progress text session
- **When** the user pauses, closes, and resumes it
- **Then** no new workflow is created
- **And** the prior transcript position, draft inputs, persona, and pending
  decision are restored
- **And** an abandoned or completed session cannot resume as active

### F2-005 Failure injection

- **Given** developer instrumentation is enabled
- **When** latency, provider disconnect, policy-channel loss, or event
  duplication is injected
- **Then** the canonical state changes according to the fixture
- **And** duplicate `event_id` values do not duplicate visible turns or records
- **And** instrumentation controls never appear in production mode

### F2-006 Retention behavior

- **Given** the default retention profile
- **When** caption deltas, a final transcript, and a structured confirmation are
  emitted
- **Then** caption and transcript material remain ephemeral
- **And** the confirmed structured value and consent/approval references are
  retained
- **And** no transport authorization, SDP, provider credential, or raw secret is
  logged

### F2-007 Commands, events, and snapshots keep distinct authority

- **Given** client commands, provider observations, and Hermes authoritative
  events for the same operation
- **When** the deterministic reducer processes them
- **Then** client/provider input cannot advance approval, execution, consent,
  confirmation, workflow, or lifecycle authority
- **And** only registry-authorized events advance `state_revision`
- **And** the matching AVC-12 snapshot reproduces the same authoritative state

### F2-008 Event gap requires snapshot recovery

- **Given** an authoritative stream with one missing predecessor
- **When** a later sequence arrives
- **Then** consequential commands and confirmations are disabled
- **And** the client requests replay or AVC-12
- **And** processing resumes only after chain and revision validation pass

### F2-009 Lease expiry and takeover revoke stale clients

- **Given** one active client, session epoch, lease, and media leg
- **When** the lease expires or a policy-approved takeover increments the epoch
- **Then** the stale client cannot submit commands or resume media
- **And** the stale media leg is closed no later than lease expiry
- **And** the new client begins from a new grant and authoritative snapshot

## F3 Generic Service Intake

### F3-001 Happy path

- **Given** a user starts `service_intake_happy_path`
- **When** they describe the requested service and provide required context
- **Then** the avatar explains the interpreted request
- **And** the conventional surface shows structured scope fields
- **And** no governed action is proposed until the user confirms the summary

### F3-002 Missing information

- **Given** a request lacks a required service date or location
- **When** the intake reaches scope validation
- **Then** the avatar asks only for the missing information
- **And** the context panel marks the missing field without implying an error
- **And** unrelated confirmed fields are preserved

### F3-003 Consequential correction

- **Given** a captured date or identifier is incorrect
- **When** the user corrects it by text, keyboard, or fixture-simulated voice
- **Then** the old confirmation becomes superseded
- **And** the complete corrected value is shown for confirmation
- **And** no action uses the value until the new confirmation is recorded

### F3-004 Decline or withdrawal

- **Given** a pending confirmation or consent request
- **When** the user declines or withdraws it
- **Then** the workflow does not treat silence as agreement
- **And** the avatar explains available revision, save-draft, and handoff paths
- **And** no denied data use or action occurs

### F3-005 Offline draft

- **Given** no network access
- **When** the user completes available intake fields and saves a draft
- **Then** the draft is locally recoverable after restart
- **And** it is clearly marked unsubmitted
- **And** governed action, live voice, and server approval remain unavailable

### F3-006 Governed action proposal

- **Given** all required fields and confirmations are valid
- **When** the user chooses continue
- **Then** the client emits a canonical `tool_intent_proposed` or workflow
  submission request
- **And** it displays pending status
- **And** it never reports completion before a canonical result event arrives

### F3-007 Offline synchronization conflict

- **Given** a locally edited draft whose base workflow revision changed on the
  server
- **When** synchronization begins
- **Then** neither revision silently overwrites the other
- **And** review mode shows field-level conflicts and the resulting values
- **And** every affected consequential confirmation becomes superseded
- **And** the resolved submission reuses one stable synchronization idempotency
  key

### F3-008 Web offline policy defaults closed

- **Given** a web client whose browser-storage capability or client policy does
  not satisfy the approved threat model
- **When** the user attempts to save an offline draft
- **Then** offline save is unavailable without storing the sensitive draft
- **And** the UI offers only policy-approved online continuation or exit

## F4 Governed Actions And Handoff

### F4-001 Client cannot receive or execute raw model tools

- **Given** a provider fixture emits a raw function/tool call
- **When** the control-plane adapter maps it and Hermes evaluates it
- **Then** Flutter receives only a presentation-safe canonical intent or
  approval state from Hermes
- **And** raw provider arguments are not forwarded to Flutter unless an
  approved field is required for user confirmation
- **And** no privileged credential or direct execution handler exists in the
  client
- **And** Hermes approval is required according to tool class

### F4-002 Read action under standing policy

- **Given** a read-only tool is preapproved and consent permits it
- **When** Hermes authorizes the intent
- **Then** the UI may proceed without redundant confirmation
- **And** it shows pending state when latency is noticeable
- **And** the result records its policy and tool references

### F4-003 Confirmation-first action

- **Given** a write or consequential action
- **When** the model proposes the action
- **Then** the client renders the exact proposed effect and confirmed inputs
- **And** Hermes does not execute until explicit confirmation and approval exist
- **And** changing an input invalidates the prior confirmation

### F4-004 Denied action

- **Given** Hermes denies an intent
- **When** `tool_denied` arrives
- **Then** the UI stops pending animation
- **And** explains the denial without claiming the tool failed
- **And** presents only policy-approved revision or handoff actions

### F4-005 Tool failure

- **Given** an approved tool starts but fails
- **When** `tool_failed` arrives
- **Then** failure is distinguished from denial and cancellation
- **And** no success state or false confirmation is recorded
- **And** retry is available only when policy and idempotency permit it

### F4-006 Policy channel loss

- **Given** media or text interaction remains available
- **When** Hermes supervision or workflow authority disconnects
- **Then** governed actions pause immediately
- **And** the avatar may explain and attempt reconnection
- **And** it cannot propose that an external action completed

### F4-007 Human handoff

- **Given** the user requests a human or policy requires escalation
- **When** handoff begins
- **Then** the UI shows target role, current routing state, and context-sharing
  scope
- **And** the user can review what will be shared
- **And** `handoff_completed` or a clear unavailable result terminates pending
  handoff state

### F4-008 Audit trace completeness

- **Given** happy, denied, failed, and handoff fixtures
- **When** each finishes
- **Then** every retained action record resolves session, workflow, client,
  user/subject, persona ID/version, confirmation/consent, policy, and result
  references
- **And** ephemeral captions, audio, and credentials are absent unless an
  explicit retention fixture allows them

### F4-009 Command retry and stale revision cannot duplicate work

- **Given** one accepted consequential command and a newer authoritative state
- **When** the same command ID is retried and a second command uses the stale
  prior revision
- **Then** the retry returns the original result without another external action
- **And** the stale command returns conflict plus snapshot/replay guidance

### F4-010 Confirmation is bound to exact effect

- **Given** a pending confirmation with a binding digest, expiry, actor, epoch,
  policy, consent, and state revision
- **When** any bound value changes or a mismatched, expired, superseded, or
  stale decision is submitted
- **Then** execution remains blocked
- **And** a new challenge is required when the action remains eligible
- **And** silence or affirmative transcript text never substitutes for AVC-11

### F4-011 Control lease expires during pending action

- **Given** provider media remains connected while an action is pending
- **When** authoritative control is lost through lease expiry or revocation
- **Then** governed commands and confirmation submission stop immediately
- **And** media closes according to the fail-closed policy
- **And** no provider message can report authoritative completion

## Cross-Cutting Exit Criteria

F1-F4 are complete only when:

- every scenario ID has an automated test owner and evidence output path
- VP-01 through VP-05 golden checks pass without overlap or clipping
- keyboard, reduced-motion, text-only, and manual screen-reader reviews pass
- all AVC-01 through AVC-12 fixtures validate in Dart and a language-neutral
  validator
- offline tests run with network access blocked
- logs and crash output pass transport-authorization, SDP, and secret scans
- fixture events are replayable without a live OpenAI account
- user-facing states distinguish pending, approved, denied, failed, blocked,
  disconnected, and handed-off outcomes
- no test treats transcript text as confirmation or silence as consent
- command retries, stream gaps, state conflicts, takeover, revocation, and lease
  expiry remain fail-closed and deterministic
- untrusted markup, links, provider errors, and authority claims remain inert

## Deferred From F1-F4

- live OpenAI Realtime connection
- GPT-Live-1 API adapter
- microphone/audio routing
- native iOS and Android acceptance
- full lip synchronization
- interactive React Flow workflow editing
- production analytics and numeric voice-latency SLOs

Those concerns enter F5 and later after the deterministic interaction and
authority model is proven.
