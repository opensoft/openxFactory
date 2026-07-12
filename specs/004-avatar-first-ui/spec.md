# Feature Specification: Avatar-First UI Standard Alignment

**Feature Branch**: `004-avatar-first-ui`

**Created**: 2026-07-11

**Status**: Draft

**Input**: OpenSpec change: "align-avatar-first-ui-standard" — align the reusable
avatar-first UI standard and domain profile carrier with the AVC kernel: update
the standard around four authoritative runtime axes and client-local
conversation/work/review presentation modes; set Hermes-layer surface defaults;
align the registered avatar-first profile schema; update the shared template and
validated examples; extend the offline validator; and publish deterministic UI
fixture shapes and evidence mappings — with no Flutter widgets, provider
adapters, or live client (those remain in `implement-avatar-client-lab`).

## Clarifications

### Session 2026-07-11

- Q: Does this feature define a persona-catalog schema, or does the UI profile only carry a reference to a catalog owned elsewhere? → A: Reference-only. The profile carries a persona reference (stable persona ID, version, and an optional non-secret catalog locator); the persona-catalog schema and instances remain domain/kernel-owned and out of scope. Resolution failures fail closed to an approved fallback; the UI never invents persona data.
- Q: Must the confirmation-before-action example be a domain-neutral archetype rather than embed Ledger/accounting specifics? → A: Yes. Publish a domain-neutral `confirmation-before-consequential-action` archetype in neutral vocabulary; Ledgerx is inspiration only and no accounting-specific fields or examples belong in openxFactory.
- Q: In what form and location are the deterministic UI fixture shapes published? → A: Versioned YAML/JSON fixture files under `examples/avatar-first-ui/fixtures/`, separate from profile examples. Each fixture carries fixed clock/ID/font/locale/platform inputs, canonical command/event/snapshot inputs, expected view-state/record shapes, and its AFU evidence IDs; the offline validator checks them.
- Q: Does the UI profile schema embed readiness/heartbeat/lease ceiling constants, or carry selected values validated against kernel-owned ceilings? → A: The profile carries selected readiness, heartbeat, and lease values. Numeric ceilings remain kernel-owned and are loaded read-only by the validator (parallel baseline during development, released registries at realization); the UI schema does not duplicate maxima, and missing or unresolvable bounds fail closed.
- Q: What does the profile's runtime compatibility field encode, and what does the final cross-check compare it against? → A: Exact content-addressed coordinates, no released version ranges. During parallel work it records the exact `avatar-client-parallel-v1` baseline identity and required baseline digests; at realization it records the released bundle tag, exact commit, and required registry/interface-lock digests, and validates every referenced ID against those bytes. A loose version range is not permitted for a released profile, and because profile fields already declare the specific capabilities/outcomes/states consumed, no second hand-maintained capability list is required.
- Q: What is the required minimum set of negative fixtures the validator must reject? → A: At least one negative fixture per enforced rule class (presentation-authored transition; out-of-range readiness/heartbeat/lease; missing control fallback; unknown/invalid persona reference; reserved/forbidden mode; unsafe rendering/HTML or URI; missing/invalid consent-purpose mapping; held-answer rendered as active), each failing one primary rule with a stable error/evidence ID. [Analyze-gate disposition 2026-07-11: the enforced-rule-class set was extended to nine — `unresolvable retention-policy reference` (AFUV-RETENTION-UNRESOLVED) was added to enforce FR-027's fail-closed requirement; see FR-019.]
- Q: How is the accessibility baseline represented in the profile schema? → A: As explicit structured per-capability declarations (keyboard operation, stable/visible focus, screen-reader announcements, captions, text-only mode, reduced motion, high contrast, non-color cues, zoom/reflow, and pseudo-locale coverage); every field has a closed default and is individually validator-checkable.
- Q: What does the profile's retention overlay carry? → A: References to externally owned retention-policy IDs plus presentation flags/labels needed to show resolved retention state. It contains no inline durations, legal policy, consent evidence, or authority to change retention; an unresolved policy reference fails closed.

## User Scenarios & Testing *(mandatory)*

<!--
  These stories describe the standards-and-validation work this feature owns.
  The "users" are the people and processes who consume the neutral standard:
  domain profile authors, standard maintainers, the offline validator, and the
  successor implementation changes that build the actual client. This feature
  does NOT build the Flutter client; it makes the standard precise enough that
  one reusable client and diverse domain overlays can be built from it.
-->

### User Story 1 - Author a conformant avatar-first UI profile (Priority: P1)

A DomainxFactory profile author uses the aligned profile schema, shared
template, and validated examples to declare a domain avatar-first UI overlay
that carries content-addressed runtime compatibility, a shell surface default,
interaction and speech-gate selection, selected readiness/heartbeat/lease values
(validated against kernel-owned ceilings), safe outcome and fallback slots,
media-authorization pending state, neutral consent-purpose mappings, a persona
reference, a retention overlay, and a structured accessibility baseline. The
offline validator confirms the profile is conformant, all defaults are closed,
and no authoritative axis is authored by presentation.

**Why this priority**: The profile is the domain overlay carrier — it is the
single artifact every domain and the reusable client depend on. Without a
precise, validated schema plus a working example and template, no domain can
express an avatar-first surface and no successor can build a client. This story
delivers the core deliverable end to end.

**Independent Test**: Author or load the four representative example profiles
(customer avatar-first, client hybrid, domain conventional-first, and the
domain-neutral confirmation-before-consequential-action archetype) plus
compatibility fixtures and one negative fixture per enforced rule class, run the
offline validator, and confirm valid profiles pass and each negative fixture
fails on its intended rule with a stable error/evidence ID — with no live
provider or runtime service involved.

**Acceptance Scenarios**:

1. **Given** a domain profile that carries content-addressed runtime
   compatibility, a shell surface default, interaction and speech-gate selection,
   selected readiness/heartbeat/lease values within kernel-owned ceilings, safe
   outcome and fallback slots, consent-purpose mappings, a persona reference, a
   retention overlay, and a structured accessibility baseline, **When** the
   offline validator runs, **Then** the profile passes and the validator reports
   full coverage of the required fields.
2. **Given** an existing static avatar-first profile authored before this
   alignment, **When** the offline validator runs, **Then** the profile remains
   valid because the new runtime fields are additive with explicit closed
   defaults.
3. **Given** a profile that omits a new runtime field, **When** the offline
   validator runs, **Then** the field resolves to its declared closed default
   rather than an open or permissive value.
4. **Given** a negative fixture that lets presentation author an authoritative
   transition, encodes an out-of-range lease/heartbeat/readiness value, omits a
   required control's fallback, or references an unknown persona, **When** the
   offline validator runs, **Then** the validator fails and identifies the
   violated rule with a stable error/evidence ID.

---

### User Story 2 - Read a precise, layered avatar-first standard (Priority: P1)

A successor implementer or standard reviewer reads `avatar-first-ui-standard.md`
and finds precise, technology-agnostic definitions of: the four authoritative
runtime axes kept separate from client-local `conversation | work | review`
presentation modes; the stable shell regions and controls; Hermes-layer surface
defaults (Customer avatar-first, Client hybrid, Domain conventional-first with
an avatar analyst/copilot) subject to domain risk and accessibility overrides;
media-authorization and held-answer semantics; AVC-02 denial and terminal
rendering; control-loss versus media-loss behavior; safe rendering of untrusted
content; persona disclosure duties; the conventional workflow boundary; and the
accessibility/localization evidence boundary that separates standard
requirements from later platform qualification.

**Why this priority**: The standard is the shared meaning that the schema,
template, validator, and every successor client depend on. It must be precise
enough for exactly one reusable client and diverse domain overlays while
preventing presentation from claiming authority. Without it, downstream work
would re-derive semantics inconsistently.

**Independent Test**: Review the standard against the eight capability
requirements and confirm each behavior is defined with an owner (Hermes layer,
runtime axis, kernel registry, or named successor) and that every deferred
item names its successor change and its closed default — with no reliance on a
running client.

**Acceptance Scenarios**:

1. **Given** the standard's runtime section, **When** a reviewer inspects it,
   **Then** the four authoritative axes (session lifecycle, control health,
   media state, workflow projection) are defined as authoritative and the
   `conversation | work | review` modes are defined as client-local
   presentation that never conflates with them.
2. **Given** the standard's Hermes-layer section, **When** a reviewer inspects
   it, **Then** Customer defaults to avatar-first, Client to hybrid, and Domain
   to conventional-first with an avatar analyst/copilot, and a domain override
   is required to record user set, workflow need, risk class, accessibility
   fallback, and authority boundary without making avatar text authoritative.
3. **Given** the standard's media and outcome section, **When** a reviewer
   inspects it, **Then** a held provider answer without a matching
   `media_authorized` event is defined as connecting/pending rather than active
   capture or playback, and AVC-02 denial/terminal results are defined to expose
   only safe message keys, retry guidance, and approved fallback modes.
4. **Given** the standard's accessibility section, **When** a reviewer inspects
   it, **Then** the standard's declarable requirements (keyboard, focus,
   screen-reader announcements, captions, text-only, reduced motion, high
   contrast, non-color cues, zoom/reflow, English plus a long-string/
   bidirectional pseudo-locale) are distinguished from later platform
   qualification evidence owned by named successors.

---

### User Story 3 - Prove full requirement-to-evidence traceability offline (Priority: P2)

A standard maintainer runs the offline validator and reviews the acceptance
map so that every `AFU-*` requirement and scenario maps to standard, schema,
template, example/fixture, or a named successor as its evidence, and confirms
that deterministic UI fixture shapes are published while Flutter widget, golden,
platform-accessibility, and live-provider evidence stay explicitly
successor-owned.

**Why this priority**: Traceability is what lets this standards change archive
honestly without overclaiming a client it does not build. It guarantees no
requirement is silently unowned and no successor-owned evidence is claimed here.
It depends on Stories 1 and 2 producing the artifacts to trace.

**Independent Test**: Run acceptance-map parity and the offline validator over
the schema, template, examples, and fixtures; confirm every requirement and
scenario resolves to an owner and that successor-owned evidence types
(`successor`, live provider, golden) are annotated as deferred with a named
change.

**Acceptance Scenarios**:

1. **Given** the acceptance map and the UI capability delta, **When** parity is
   checked, **Then** all eight requirements and all twenty-five scenarios are
   present and each maps to standard/schema/template/fixture evidence or a named
   successor change.
2. **Given** a scenario whose evidence is deferred, **When** the map is
   reviewed, **Then** it retains a named successor owner
   (`implement-avatar-client-lab` or `avatar-pilot-hardening`) and a closed
   default rather than an open claim.
3. **Given** the published deterministic UI fixture shapes under
   `examples/avatar-first-ui/fixtures/`, **When** the same fixture, seed,
   decisions, and contract version are evaluated twice, **Then** the declared
   canonical view-state, command, event, and record shapes are equivalent and
   carry the same AFU evidence IDs, without a live model.

---

### User Story 4 - Serialize the final contract release after the kernel (Priority: P3)

A release integrator, after the AVC kernel release lands, consumes any accepted
kernel variances by mapped UI fields only, pins and cross-checks the exact
released capability, outcome, consent-purpose, and state registries read-only,
rebases to the latest contract bundle, allocates the next available bundle
version, and updates `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and
`contracts/README.md` atomically for the profile-schema revision — publishing a
matching annotated tag without pre-reserving a version and without editing any
kernel file.

**Why this priority**: This is the final integration step and is deliberately
serialized after the kernel release to avoid write conflicts on shared release
metadata. It is last because it depends on the kernel release existing and on
all prior stories being merged and green.

**Independent Test**: Point the validator's final-realization mode at the exact
released kernel registries and confirm it fails closed on any drift; confirm the
manifest, changelog, and contract README change together for the profile-schema
revision with a version allocated at realization, and that no kernel,
reference-runtime, F0, DomainxFactory, Flutter, or deployment file changed.

**Acceptance Scenarios**:

1. **Given** the released kernel registries, **When** the validator runs in
   final-realization mode, **Then** it loads them read-only and fails on any
   registry drift between the parallel baseline and the released IDs.
2. **Given** an accepted kernel variance, **When** it is consumed, **Then** only
   the mapped UI fields and fixtures reopen and no sibling kernel path is
   edited.
3. **Given** the serialized release, **When** it lands, **Then**
   `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and
   `contracts/README.md` are updated atomically for the profile-schema revision
   with the next available bundle version and a matching annotated tag, and no
   version was pre-reserved in the proposal.

---

### Edge Cases

- **Held answer before authorization**: A trusted media adapter has verified an
  AVC-02 grant and holds a provider answer but has not applied a matching
  `media_authorized` event — the standard requires the surface to remain
  connecting/pending and the adapter to leave the answer unapplied.
- **Denial or terminal outcome**: An AVC-02 result is a denial or terminal
  outcome — only its localization-safe message key, retry guidance, and approved
  text/handoff/upgrade/retry-later fallback may surface; raw provider errors
  never enter widget state.
- **Control lost while media connected**: The control lease degrades or is lost
  while audio remains connected — the standard requires distinguishing control
  loss from media loss, disabling governed commands, and offering the
  runtime-defined stop/reconnect/handoff path.
- **Audio unavailable**: Microphone permission is denied, no device exists,
  media fails, or policy disables voice — the same eligible workflow stays usable
  through text and structured controls without loss of authority or traceability.
- **Persona unavailable**: A persona is missing, suspended, retired, disallowed,
  or incompatible with the required language/profile — the profile must resolve
  to an approved fallback without inventing a persona or voice, and persona is
  fixed for the logical session (a change ends the session and starts a new one).
- **Untrusted markup or dangerous link**: Model or transcript output contains
  HTML, script, custom URI schemes, or a non-allowlisted destination — it renders
  inert or is rejected; provider text is never an authority, confirmation, hidden
  command, widget identifier, analytics key, or localization resource key.
- **Existing profile lacks new fields**: A static profile authored before this
  alignment omits new runtime fields — additive fields with closed defaults keep
  it valid, verified by a compatibility fixture.
- **Reserved/forbidden mode**: A profile selects push-to-talk (reserved,
  disabled) or `server_vad` neutral-mode details — the validator rejects it;
  `provider_vad` is the neutral interaction mode and push-to-talk must fall back
  to text or handoff.
- **Parallel registry drift**: A registry ID changes between the frozen
  `avatar-client-parallel-v1` baseline and the released kernel — the
  final-realization validator fails closed and reopens only mapped UI fields.

## Requirements *(mandatory)*

### Functional Requirements

**Standard document (`docs/avatar-first-ui-standard.md`)**

- **FR-001**: The standard MUST define the domain-neutral shell regions
  (`avatar_stage`, `conversation_rail`, `context_panel`, `action_bar`,
  `handoff_panel`, `settings_panel`) and the client-local `conversation`,
  `work`, and `review` presentation modes as state that never conflates with
  the four authoritative runtime axes (session lifecycle, control health, media
  state, workflow projection) owned by `avatar-client-runtime`. (AFU-001)
- **FR-002**: The standard MUST require that a mode change preserves applicable
  logical session, workflow, persona, focus target, pending decision, state
  revision, and trace context, and that an AVC-12 authoritative snapshot
  reconciles the surface while retaining only valid local presentation
  preferences and surfacing discarded pending local intent. (AFU-001)
- **FR-003**: The standard MUST set Hermes-layer surface defaults — Customer
  avatar-first, Client hybrid, Domain conventional-first with an avatar
  analyst/copilot — and MUST require that a DomainxFactory override records user
  set, workflow need, risk class, accessibility fallback, and authority
  boundary, and cannot make avatar text authoritative. (AFU-002)
- **FR-004**: The standard MUST require that consequential values (names,
  identifiers, dates, money, addresses, consent, proposed effects) be shown as
  complete display-safe values in work or review mode and MUST NOT be confirmed
  by voice alone. (AFU-001, AFU-002)
- **FR-005**: The standard MUST define the client/web-console responsibility
  split: the reusable client owns the conversation experience, adaptive shell,
  deterministic local projection, standard controls, persona presentation,
  read-only workflow summaries, and handoff initiation, while dense
  administration, policy editing, bulk operations, interactive workflow editing,
  and audit investigation remain in the conventional web console governed by the
  workflow-visualization standard; the client MUST NOT introduce a second
  interactive workflow-canvas standard. (AFU-003)
- **FR-006**: The standard MUST require that handoff URLs carry no bearer token,
  subject identifier, transcript, or provider secret, and MUST define any future
  handoff exchange as server-issued, one-time, purpose-bound, and reauthorized
  at the web boundary, with the exchange protocol itself deferred until the web
  console exists. (AFU-003)
- **FR-007**: The standard MUST define the required controls (start, pause,
  stop, microphone mute, captions, persona selection at session start, language,
  repeat, simple explanation, more detail, human handoff, privacy/disclosure,
  current workflow-state) and MUST require that a missing control has a
  documented policy or platform fallback, with stop and mute reachable whenever
  capture is possible. (AFU-004)
- **FR-008**: The standard MUST require the surface to continuously distinguish
  microphone permission, capture authorized/pending, capture active, listening,
  speaking, control degraded/lost, governed action pending, and retention
  active, and MUST forbid communicating any status by animation, audio, or color
  alone. (AFU-004, AFU-005)
- **FR-009**: The standard MUST define held-answer/media-authorization behavior
  (a verified but unapplied provider answer shows as connecting/pending, never
  active), AVC-02 denial/terminal rendering (safe message key, retry guidance,
  approved fallback only; provider errors excluded from widget state), and
  control-loss-versus-media-loss behavior offering the runtime-defined stop,
  reconnect, or handoff path. (AFU-004)
- **FR-010**: The standard MUST define the accessibility and localization
  baseline it can declare (keyboard-only operation, stable/visible focus,
  screen-reader labels and single meaningful state announcements, captions,
  text-only operation, reduced motion, high contrast, non-color cues,
  zoom/reflow, and English plus a long-string/bidirectional pseudo-locale) and
  MUST separate these declarable requirements from later platform qualification
  evidence (Windows qualification, web WCAG 2.2 AA audit and exception register,
  additional locales) assigned to named successors. (AFU-005)
- **FR-011**: The standard MUST define persona presentation and disclosure
  duties: every selectable persona presents a stable ID/version, role, display
  name, required disclosure, supported languages, and lifecycle status resolved
  from the domain/kernel-owned catalog (which this feature does not schematize);
  the client displays disclosure and records persona ID/version before media
  starts; persona is fixed for the logical session; real-person impersonation
  defaults to prohibited; AI/AI-assisted disclosure, current authority boundary,
  and reachable consent withdrawal are required; and handoff shows target role,
  exact shared context classes, and purpose with the ability to remove optional
  context or decline. A persona reference that cannot be resolved MUST fail
  closed to an approved fallback; the client MUST NOT invent persona data.
  (AFU-006)
- **FR-012**: The standard MUST define safe rendering of untrusted content:
  transcript text, model output, tool summaries, attachment names, URLs, visual
  result data, and provider error text are untrusted and rendered as plain text
  or a narrow sanitized format; arbitrary HTML, executable content,
  provider-supplied widgets, and unsafe URI schemes are forbidden; external
  navigation/downloads use destination allowlists, origin labeling, and
  policy-appropriate confirmation; and provider text is never an authority,
  confirmation, hidden command, widget identifier, analytics key, or
  localization resource key. (AFU-007)

**Profile schema (`contracts/schemas/avatar-first-ui-profile.schema.yaml`)**

- **FR-013**: The profile schema MUST carry, as the domain overlay carrier:
  content-addressed runtime compatibility (per FR-025); a shell surface default;
  interaction-mode and speech-gate selection; selected readiness, heartbeat, and
  lease values (the numeric ceilings remain kernel-owned and are not duplicated
  in the schema, per FR-026); safe outcome and fallback slots; a
  media-authorization pending state; neutral consent-purpose mappings; a persona
  reference of stable persona ID, version, and an optional non-secret catalog
  locator (the persona-catalog schema is out of scope, per FR-011); a retention
  overlay of retention-policy references plus presentation flags/labels (per
  FR-027); a structured accessibility baseline of explicit per-capability
  declarations (per FR-028); and handoff roles. This is the umbrella carrier
  requirement; the individual field rules are specified in FR-025 through
  FR-028. (AFU-001, AFU-002, AFU-004, AFU-006)
- **FR-014**: The profile schema MUST reference the three neutral consent-purpose
  IDs and MAY allow stricter domain-specific IDs, but MUST NOT contain consent
  evidence or make the memory-gateway consent profile authoritative. (AFU-006)
- **FR-015**: The profile schema MUST treat `provider_vad` as the neutral
  interaction mode, keep provider-native `server_vad` details in a separate
  server profile, and keep push-to-talk a reserved, disabled mode that falls
  back to text or handoff. (AFU-004)
- **FR-016**: The profile schema MUST make every new runtime field additive with
  an explicit closed default so that existing static profiles remain valid, and
  MUST NOT allow presentation state to author an authoritative transition.
  (AFU-001, AFU-004)
- **FR-017**: The profile schema MUST carry `schema_version` and `kind` and MUST
  remain a registered contract schema consumed read-only against the kernel's
  capability, outcome, consent-purpose, and state registries. (AFU-002)
- **FR-025**: The runtime-compatibility field MUST record exact content-addressed
  coordinates and MUST NOT permit a loose released version range: during parallel
  work it records the exact `avatar-client-parallel-v1` baseline identity and
  required baseline digests; at realization it records the released bundle tag,
  exact commit, and required registry/interface-lock digests. Because the profile
  fields already declare the specific capabilities, outcomes, and states they
  consume, the schema MUST NOT introduce a second hand-maintained capability
  list. (AFU-002, AFU-008)
- **FR-026**: The profile schema MUST carry only the per-profile selected
  readiness, heartbeat, and lease values; it MUST NOT hardcode duplicate numeric
  ceilings. The ceilings remain kernel-owned and are resolved read-only at
  validation (parallel baseline during development, released registries at
  realization); a selected value with a missing or unresolvable ceiling MUST fail
  closed. (AFU-004, AFU-008)
- **FR-027**: The retention overlay MUST carry only references to externally
  owned retention-policy IDs plus the presentation flags/labels needed to show
  resolved retention state; it MUST NOT contain inline durations, legal policy,
  consent evidence, or any authority to change retention, and an unresolved
  policy reference MUST fail closed. (AFU-006)
- **FR-028**: The accessibility baseline MUST be represented as explicit
  structured per-capability declarations — keyboard operation, stable/visible
  focus, screen-reader announcements, captions, text-only mode, reduced motion,
  high contrast, non-color cues, zoom/reflow, and pseudo-locale coverage — each
  with a closed default and each individually validator-checkable. (AFU-005)

**Template and examples (`templates/ui/avatar-first.yaml`, `examples/avatar-first-ui/`)**

- **FR-018**: The shared template MUST express the stable regions, standard
  controls, authority sources, media/recording awareness, fallback behavior,
  handoff boundary, and reserved-feature defaults, and MUST be marked as an
  instantiation stub rather than live configuration. (AFU-001, AFU-004)
- **FR-019**: The examples set MUST include validated customer avatar-first,
  client hybrid, and domain conventional-first profiles plus a domain-neutral
  `confirmation-before-consequential-action` archetype (neutral vocabulary, no
  domain-specific fields; Ledgerx is inspiration only), plus at least one
  compatibility fixture (existing profile stays valid) and at least one negative
  fixture per enforced rule class (presentation-authored transition; out-of-range
  readiness/heartbeat/lease; missing control fallback; unknown/invalid persona
  reference; reserved/forbidden mode; unsafe rendering/HTML or URI;
  missing/invalid consent-purpose mapping; held-answer rendered as active;
  unresolvable retention-policy reference), each
  failing one primary rule with a stable error/evidence ID. (AFU-002, AFU-004,
  AFU-006, AFU-007)

**Validator (`scripts/validate-avatar-first-ui.py`)**

- **FR-020**: The offline validator MUST check schema/template/example parity,
  required regions and controls, the state axes, safe outcome slots, held-answer/
  media-authorization state, selected readiness/heartbeat/lease values against
  kernel-owned ceilings, control fallbacks, consent-purpose mappings, persona
  reference resolution, retention-policy references, safe-rendering policy, the
  structured per-capability accessibility declarations, and forbidden/reserved
  modes, using no provider or runtime service, and MUST emit a stable
  error/evidence ID for each rejected rule. (AFU-004, AFU-005, AFU-006, AFU-007,
  AFU-008)
- **FR-021**: The offline validator MUST validate against the frozen
  `avatar-client-parallel-v1` baseline identity and required baseline digests
  during parallel work and, in final-realization mode, MUST load the exact
  released kernel registries read-only, validate every referenced ID against the
  released bundle tag, exact commit, and required registry/interface-lock digests
  (content-addressed, no loose version range), and fail closed on any drift,
  reopening only mapped UI fields on an accepted kernel variance. (AFU-008)
- **FR-022**: The validator or acceptance map MUST confirm that every `AFU-*`
  requirement and scenario maps to standard, schema, template, fixture, or a
  named successor as its evidence, keeping Flutter widget, golden,
  platform-accessibility, and live-provider evidence explicitly successor-owned.
  (AFU-003, AFU-005, AFU-007, AFU-008)

**Deterministic fixtures and release**

- **FR-023**: The feature MUST publish deterministic UI fixture shapes as
  versioned YAML/JSON files under `examples/avatar-first-ui/fixtures/`, separate
  from the profile examples. Each fixture MUST carry fixed clock/ID/font/locale/
  platform inputs, canonical AVC command/event/snapshot inputs, expected
  view-state/record shapes, and its AFU evidence IDs, so acceptance is
  reproducible across identical runs and checkable by the offline validator,
  without creating Flutter widgets, provider adapters, goldens, or a live client.
  (AFU-008)
- **FR-024**: The final serialized release MUST, only after the kernel release,
  rebase to the latest contract bundle, allocate the next available bundle
  version at realization (never pre-reserved), update `contracts/manifest.yaml`,
  `contracts/CHANGELOG.md`, and `contracts/README.md` atomically for the
  profile-schema revision, publish a matching annotated tag, and change no kernel,
  reference-runtime, F0, DomainxFactory, Flutter, or deployment file. (AFU-008)

### Key Entities *(include if feature involves data)*

- **Avatar-first UI profile**: The domain overlay carrier. Carries
  content-addressed runtime compatibility, shell surface default, interaction-mode
  and speech-gate selection, selected readiness/heartbeat/lease values (ceilings
  kernel-owned, not duplicated), outcome and fallback slots, media-authorization
  pending state, consent-purpose mappings, a persona reference, a retention
  overlay, a structured accessibility baseline, and handoff roles. Additive
  fields have closed defaults; existing static profiles remain valid.
- **Runtime compatibility**: Exact content-addressed coordinates the profile
  pins — baseline identity plus required digests during parallel work; released
  bundle tag, exact commit, and registry/interface-lock digests at realization.
  No loose released version range; no second hand-maintained capability list
  (the profile fields already declare the capabilities/outcomes/states consumed).
- **Persona reference**: A reference to a domain/kernel-owned persona catalog
  carrying a stable persona ID, version, and an optional non-secret catalog
  locator; the catalog schema and instances are out of scope for this feature.
  The resolved persona exposes role, display name, required disclosure, supported
  languages, and lifecycle status. Persona is fixed for a logical session;
  real-person impersonation defaults to prohibited; an unresolved reference fails
  closed to an approved fallback and the client never invents persona data.
- **Fallback slot**: The declared safe response for a denial, terminal outcome,
  missing control, unavailable persona, or unavailable audio — a
  localization-safe message key plus approved text/handoff/upgrade/retry-later
  modes, never raw provider text.
- **Consent purpose mapping**: A mapping from profile behaviors to the three
  neutral consent-purpose IDs (with optional stricter domain IDs). Carries no
  consent evidence and does not make the memory-gateway consent profile
  authoritative.
- **Retention overlay**: References to externally owned retention-policy IDs plus
  the presentation flags/labels needed to show resolved retention state. Carries
  no inline durations, legal policy, consent evidence, or authority to change
  retention; an unresolved policy reference fails closed.
- **Accessibility baseline**: A structured set of explicit per-capability
  declarations (keyboard operation, stable/visible focus, screen-reader
  announcements, captions, text-only mode, reduced motion, high contrast,
  non-color cues, zoom/reflow, and pseudo-locale coverage), each with a closed
  default and each individually validator-checkable.
- **Authoritative runtime axes** (referenced, not owned): session lifecycle
  (broker-owned), control health (lease-derived), media state (trusted-adapter
  observation constrained by authority), and workflow projection
  (Hermes/workflow-authority-owned). Consumed read-only from `avatar-client-runtime`.
- **Presentation mode**: Client-local `conversation | work | review` state that
  a surface may switch without changing any authoritative axis.
- **Acceptance/evidence map**: Registers the eight `AFU-*` requirements and
  twenty-five scenarios and binds each to standard, schema, template, fixture,
  or a named successor change, with evidence type (automated, manual, successor).
- **Kernel registries** (referenced, read-only): capability, outcome,
  consent-purpose, and state registries owned by the AVC kernel; consumed but
  never edited by this feature.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the eight `AFU-*` requirements and all twenty-five
  scenarios in the acceptance map resolve to owned evidence (standard, schema,
  template, fixture) or a named successor change, with zero unowned items.
- **SC-002**: The offline validator passes on the shared template and all four
  representative example profiles, and fails on every negative fixture (at least
  one per enforced rule class), each on the specific rule it targets and reported
  with a stable error/evidence ID, using no provider or runtime service.
- **SC-003**: 100% of existing static avatar-first profiles that predate this
  alignment remain valid under the aligned schema, confirmed by at least one
  compatibility fixture — every new runtime field is additive with an explicit
  closed default.
- **SC-004**: Every new runtime field in the profile schema resolves to a closed
  (fail-closed) default when omitted; the validator reports zero fields that
  default to an open or permissive value.
- **SC-005**: The standard defines all four authoritative axes and the three
  presentation modes, and a reviewer can, for each of the eight requirements,
  identify a single owner (Hermes layer, runtime axis, kernel registry, or named
  successor) with no requirement left ownerless.
- **SC-006**: Deterministic UI fixture shapes under
  `examples/avatar-first-ui/fixtures/` produce equivalent declared canonical
  view-state, command, event, and record shapes — carrying the same AFU evidence
  IDs — across two identical runs (same fixture, seed, decisions, and contract
  version).
- **SC-007**: The change introduces zero edits to kernel, reference-runtime, F0,
  DomainxFactory, Flutter, or deployment files during parallel work, verified by
  a clean cross-check; the final release updates the manifest, changelog, and
  contract README together for exactly one profile-schema revision.
- **SC-008**: OpenSpec strict validation (target and `--all`) and the avatar-first
  UI validator both pass, and the acceptance-map parity check reports the expected
  8 requirements and 25 scenarios.

## Assumptions

- The AVC kernel change (`define-avatar-client-runtime` / the `avatar-client-runtime`
  capability) supplies the four authoritative runtime axes and the capability,
  outcome, consent-purpose, and state registries; this feature consumes them
  read-only and never edits `contracts/avatar-client/`.
- The frozen interface baseline `avatar-client-parallel-v1` provides the exact
  baseline identity and digests pinned during parallel work; final realization
  re-pins to the released bundle tag, exact commit, and registry/interface-lock
  digests (content-addressed, no loose version range) and fails closed on drift.
- The avatar-first standard, registered profile schema, shared template,
  examples, and validator already exist and are being aligned and extended by
  this feature, not created from scratch; the profile schema is already
  registered in `contracts/manifest.yaml`.
- Three neutral consent-purpose IDs exist in the kernel; domains may add stricter
  IDs but this feature does not define consent evidence.
- `provider_vad` is the neutral interaction mode; `server_vad` provider-native
  details live in a separate server profile; push-to-talk is a reserved, disabled
  mode.
- Deterministic fixtures use fixed clocks, IDs, fonts, locale fixtures, and
  canonical AVC commands/events/snapshots without any live model or provider.
- "Additive with a closed default" means an omitted new field resolves to the
  most restrictive fail-closed value, preserving existing-profile validity.
- Final release metadata (manifest, changelog, contract README, annotated tag)
  is serialized after the kernel release to avoid write conflicts with parallel
  siblings; version numbers are allocated at realization, never pre-reserved.
- Flutter widgets, provider adapters, live client, goldens, platform
  accessibility qualification, and live-provider evidence are owned by
  `implement-avatar-client-lab`; formal accessibility qualification and domain
  onboarding are owned by `avatar-pilot-hardening`; the conventional web console
  and workflow editor are owned by the workflow-visualization standard;
  DomainxFactory repositories provide domain profiles and mappings later.
- The persona catalog (schema and instances) and retention-policy definitions
  are domain/kernel-owned and out of scope for this feature; the UI profile
  carries only references to them and fails closed when a reference cannot be
  resolved.
