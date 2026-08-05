## ADDED Requirements

### Requirement: Offline deterministic client-lab boundary
The avatar client lab SHALL be an offline, deterministic application that
contacts no live model, provider, session broker, or network media plane, and
loads no provider credential, in this change. Its purpose SHALL be to prove the
avatar-first interaction and authority model from replayed fixtures, not to run a
production session.

#### Scenario: Lab build is inspected for live surfaces
- **WHEN** the client build and its dependency surface are scanned for a provider credential, live model call, WebRTC media plane, or session-broker network client
- **THEN** the scan MUST find none, and any such code MUST route to `qualify-avatar-live-voice` rather than this change

#### Scenario: A test reaches for wall time, randomness, or network
- **WHEN** any lab or session-core code calls a wall clock, a random source, or a socket outside an explicit injected port
- **THEN** the deterministic gate MUST fail closed

### Requirement: Content-addressed contract consumption
The client SHALL consume the released avatar-client kernel and avatar-first UI
profile only by exact commit and per-file SHA-256, verified fail-closed before
any other build step. A tag-only or commit-less pin MUST fail.

#### Scenario: A pinned contract file drifts
- **WHEN** a vendored kernel (`contract-v1.7`) or UI-profile (`contract-v1.8`) file's recomputed digest does not match the recorded per-file SHA-256
- **THEN** the build MUST fail closed before running tests

#### Scenario: A tag-only pin is recorded
- **WHEN** the contract pin records a bundle tag without the exact commit and per-file digests
- **THEN** validation MUST reject it as not content-addressed

### Requirement: Fixture-replay determinism
Every canonical session state the lab renders SHALL be reachable by replaying an
ordered fixture event stream through a pure session core, and the same fixture
replayed twice MUST produce identical normalized view-state. Clocks and identifier
sources MUST be injected, never ambient.

#### Scenario: A fixture is replayed twice
- **WHEN** the same scenario fixture is folded through the session core on two runs
- **THEN** the resulting normalized view-state MUST be identical

#### Scenario: A canonical state has no fixture
- **WHEN** conformance checks the canonical session-state set against the lab fixtures
- **THEN** any state with no replayable fixture and expected view-state MUST fail conformance

### Requirement: Client re-derives authority and never decides it
The client SHALL render only canonical intent and approval state and MUST NOT
execute a model function call, grant authority, or treat a caption as an
authoritative record. On loss of the control or policy channel it MUST fail
closed.

#### Scenario: A tool call is proposed to the client
- **WHEN** a fixture presents a proposed governed action
- **THEN** the client MUST render its canonical approval state only and MUST NOT execute or imply execution of the action

#### Scenario: The control channel is lost mid-session
- **WHEN** a fixture drops the authoritative control or policy channel
- **THEN** the client MUST pause governed actions immediately and MUST NOT continue as though authority is held

#### Scenario: A consequential value arrives only as a caption
- **WHEN** a name, code, amount, or other consequential value appears in caption text
- **THEN** the client MUST require a structured confirmation before any governed write, never treating the caption as the record

### Requirement: Replaceable six-state avatar presentation seam
The avatar SHALL present exactly the six states `listening`, `thinking`,
`speaking`, `interrupted`, `blocked`, and `handoff` behind a replaceable renderer
interface whose input is a presentation state DERIVED from authority. The renderer
MUST receive no kernel state, own no clock, and be unable to affect authority.

#### Scenario: The control channel is lost while speaking
- **WHEN** authority is lost during a token stream
- **THEN** the derived avatar state MUST become `blocked` and MUST NOT remain `speaking`

#### Scenario: Reduced motion is requested
- **WHEN** the accessibility reduced-motion capability is set
- **THEN** the renderer MUST present a single static rest frame and ignore animation phase

#### Scenario: A different renderer is substituted
- **WHEN** the renderer implementation is swapped behind the interface
- **THEN** the derived-state selector, per-state non-color cue, and reduced-motion static frame MUST be preserved without changing application logic

### Requirement: Accessibility baseline is gating acceptance
The lab SHALL satisfy the avatar-first UI accessibility-baseline capabilities as
gating tests, MUST allow keyboard-only completion of the F1-F4 workflows, and
MUST convey every avatar and status state by a non-color cue in addition to any
hue.

#### Scenario: A workflow is driven by keyboard only
- **WHEN** an F1-F4 workflow is completed using the keyboard with no pointer
- **THEN** every required control MUST be reachable and operable, with a visible focus state and correct focus order

#### Scenario: A state is distinguished only by color
- **WHEN** an avatar or authoritative status state is presented
- **THEN** it MUST carry a distinct shape, glyph, or motion cue and MUST NOT rely on hue alone

#### Scenario: Text-only mode is selected
- **WHEN** the text-only capability is active
- **THEN** a peer text renderer MUST carry all avatar semantics as a labeled status surface, not a degraded fallback page

### Requirement: Repository and ownership boundary
The Flutter avatar client application and its generated Dart bindings SHALL live
in codexFactory under `apps/avatar-client-lab/`, while openxFactory retains
ownership of the neutral contracts, conformance fixtures, and acceptance
requirements.

#### Scenario: A neutral contract or fixture is edited from the codexFactory app
- **WHEN** the codexFactory `apps/avatar-client-lab/` app proposes a change to a neutral contract, registry, or shared conformance fixture
- **THEN** boundary validation MUST reject it and require the change in openxFactory instead

#### Scenario: A new neutral scenario is authored for the lab
- **WHEN** the lab needs a neutral session scenario usable by the runtime and web console
- **THEN** it MUST be contributed to openxFactory's shared fixtures, not forked into the codexFactory app

### Requirement: Fail-closed deferral of voice, media, and Hermes
The client SHALL represent live voice, WebRTC media, brokered SDP, the real
session broker, and the real Hermes control channel only as port interfaces with
fixture adapters, and every deferred capability MUST keep a fail-closed default so
the later live seam is a clean line, not a hole.

#### Scenario: A deferred live capability is exercised
- **WHEN** the lab is asked to use voice, microphone, push-to-talk, brokered SDP, or a live media plane
- **THEN** it MUST fail preflight to a text or handoff path rather than opening a live connection

#### Scenario: A closed-default capability is left unspecified
- **WHEN** web offline drafts, attachments, or a second concurrent instance are not explicitly enabled by policy
- **THEN** the client MUST apply the closed default (drafts disabled, attachments reference-only, second instance denied)

#### Scenario: The live adapter is added later
- **WHEN** `qualify-avatar-live-voice` supplies a live transport behind the existing `SessionTransport` port
- **THEN** the session core reducer and the UI MUST require no change to consume it

### Requirement: Successor-register discharge of deferred scenarios is machine-checked
Discharging a released `deferred` scenario owned by this change SHALL be recorded
only by a successor evidence register beside the released one, and the discharge
MUST be machine-checked. The validator collects the successor registers matching
`evidence-register.*.yaml`; a discharge requires a `discharges_deferred: true`
entry whose `owner_change` matches the released deferred entry; the released,
content-addressed register and acceptance map stay byte-identical; and the
in-place `deferred->evidenced` flip remains illegal.

#### Scenario: A deferred scenario is discharged by a successor register
- **WHEN** this change discharges a scenario the released acceptance map deferred to it (e.g. SCO-001-S05) by adding a successor `evidence-register.<change>.yaml` entry with `discharges_deferred: true` and an `owner_change` matching the released deferred entry
- **THEN** the validator MUST accept the discharge while the released evidence register, acceptance map, and manifest remain byte-identical

#### Scenario: A discharge is forged in place or misattributed
- **WHEN** a released `deferred` entry is flipped to `evidenced` in place, or a successor discharge entry names an `owner_change` that does not match the released deferred entry, or a duplicate discharge targets the same deferred entry
- **THEN** the validator MUST fail closed and reject the discharge
