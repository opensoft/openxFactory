## Context

openxFactory already has an avatar-first standard, a registered profile schema,
a shared template, examples, and a validator. The AVC architecture adds more
precise state and authority semantics, but those semantics should not force the
UI-standard branch to edit canonical runtime contracts or wait for a live
provider experiment.

The sibling kernel owns neutral meaning. This change consumes the reviewed
`avatar-client-parallel-v1` names during parallel work and the exact released
registries for final realization.

## Goals / Non-Goals

**Goals:**

- Make the standard precise enough for one reusable Flutter client and diverse
  domain overlays.
- Preserve conventional UI where density, comparison, editing, or authority
  makes an avatar less useful.
- Represent runtime and workflow authority without letting presentation state
  author transitions.
- Require safe fallback, accessibility, disclosure, and handoff behavior.
- Validate domain-neutral profile, template, and example assets offline.
- Avoid write conflicts with the kernel, F0, and reference-runtime branches.

**Non-Goals:**

- Building Flutter widgets, rendering an avatar, or selecting media packages.
- Implementing WebRTC, WSS, provider calls, or a broker.
- Creating a conventional web console or workflow editor.
- Modifying DomainxFactory profiles in this change.
- Defining consent evidence, canonical AVC registries, or provider profiles.
- Completing live, platform, or formal WCAG qualification.

## Decisions

### 1. Own only the existing avatar-first standard surface

This change has exclusive write ownership of:

- `docs/avatar-first-ui-standard.md`;
- `contracts/schemas/avatar-first-ui-profile.schema.yaml`;
- `templates/ui/avatar-first.yaml`;
- `examples/avatar-first-ui/`; and
- `scripts/validate-avatar-first-ui.py`.

The profile schema is already registered in `contracts/manifest.yaml`.
Parallel implementation does not edit the shared manifest, changelog, or
contract README. After the kernel release, UI realization rebases, allocates
the next available bundle version, and updates those three integration files
atomically for the profile-schema revision.

### 2. Keep four authoritative axes separate from presentation mode

The profile and standard represent:

1. session lifecycle, broker-owned;
2. control health, lease-derived;
3. media state, trusted-adapter observation constrained by authority; and
4. workflow projection, Hermes/workflow-authority-owned.

`conversation`, `work`, and `review` are client-local presentation modes. A UI
may switch modes without changing authoritative state. AVC-12 replaces stale
projection while preserving only valid local preferences and surfacing
discarded local intent.

### 3. Use different defaults for the three Hermes user sets

Customer Hermes defaults to avatar-first because explanation, intake,
comprehension, preference, and handoff benefit from guided conversation.
Client Hermes defaults to hybrid because operators need queues, tables,
structured values, repeat actions, and approvals alongside guidance. Domain
Hermes defaults to conventional-first because policy, schemas, evidence, and
governance require dense authoritative artifacts; the avatar acts as analyst
or copilot.

A domain override records user set, workflow need, risk, accessibility
fallback, and authority boundary. It cannot make avatar text authoritative.

### 4. Keep stable shell regions and controls

The standard regions are `avatar_stage`, `conversation_rail`, `context_panel`,
`action_bar`, `handoff_panel`, and `settings_panel`. Compact surfaces may hide
or collapse regions, but must preserve their semantic functions and focus
order.

Required controls include start, pause/stop, mute, captions, language, repeat,
simple explanation, more detail, privacy/disclosure, workflow state, and human
handoff. Persona selection occurs before session start. A missing control needs
a declared policy or platform fallback. Stop and mute remain reachable whenever
capture is possible.

### 5. Render media authorization and AVC-02 outcomes explicitly

The UI distinguishes permission, authorized/pending capture, active capture,
listening, speaking, degraded/lost control, pending governed action, and active
retention. Receiving a held answer is not active media: the UI remains in a
connecting state until matching `media_authorized` is applied.

Denial and terminal outcomes expose only safe message keys, retry guidance, and
approved fallback modes. Provider errors and DTOs never enter widget state.
Control loss is distinct from media loss and offers stop, reconnect, or handoff
according to the kernel.

### 6. Use the profile as the domain overlay carrier

The profile carries runtime compatibility, shell default, interaction mode,
speech gate, timeout and lease bounds, purpose mappings, persona catalog,
retention overlay, fallback slots, accessibility baseline, and handoff roles.
It references the three neutral consent-purpose IDs and allows stricter domain
IDs, but does not contain consent evidence or make the memory-gateway consent
profile authoritative.

The neutral interaction mode is `provider_vad`; provider-native `server_vad`
details stay in a server profile. Push-to-talk remains a reserved, disabled
mode and must fall back to text or handoff.

### 7. Keep avatar presentation non-authoritative and content untrusted

Persona identity/version, role, disclosure, supported languages, and lifecycle
come from a domain-owned catalog. Real-person impersonation is prohibited by
default. Persona remains fixed for the logical session.

Transcript text, model output, summaries, attachment names, URLs, and provider
errors are untrusted. The standard permits plain text or a narrow sanitizer,
safe URI schemes, allowlisted destinations, and canonical authority cards. It
forbids arbitrary HTML, executable content, provider widgets, hidden commands,
and text-as-confirmation.

### 8. Preserve the conventional workflow boundary

The avatar client may show read-only workflow summaries and initiate handoff.
Dense administration, policy editing, bulk operations, evidence investigation,
and interactive workflow editing remain in the conventional web surface under
the workflow-visualization standard. Handoff URLs carry no token, subject,
transcript, or provider secret; the future exchange protocol is separately
approved.

### 9. Define accessibility and localization evidence honestly

The standard requires keyboard operation, stable focus, visible focus,
screen-reader names and state announcements, captions, text-only mode, reduced
motion, high contrast, non-color cues, and zoom/reflow. Animation is never the
sole state carrier. English plus a long-string/bidirectional pseudo-locale is
the deterministic baseline.

This change validates declared profile and fixture coverage. Actual Windows
qualification, web exception register, widget semantics, pinned-font goldens,
and formal audit evidence belong to the client and pilot successors.

### 10. Validate structure and closed defaults offline

The validator checks schema/template/example consistency, required regions and
controls, state axes, outcome slots, timeout/lease bounds, fallback coverage,
purpose mappings, persona references, safe-rendering policy, accessibility
fields, and forbidden/reserved modes. It uses no provider or runtime service.

During parallel work it validates the fixed baseline IDs. Final realization
loads the exact released kernel registries read-only and fails on drift. An
accepted kernel variance reopens only mapped UI fields and fixtures.

## Risks / Trade-offs

- The standard may outrun the Flutter implementation -> successor evidence is
  explicit and fail-closed; no client is claimed here.
- Existing profiles may lack new fields -> use additive fields and documented
  defaults, then validate migration fixtures.
- UI may duplicate authority -> validator requires source ownership and rejects
  presentation-authored transitions.
- Accessibility prose may overclaim -> distinguish standard requirements from
  later platform qualification evidence.
- Parallel registry drift can cause rework -> use stable IDs and a final exact
  kernel cross-check.

## Migration Plan

1. Update the standard and profile schema against `avatar-client-parallel-v1`.
2. Update the shared template and four representative examples.
3. Extend the offline validator and add compatibility/negative fixtures.
4. Consume accepted kernel variances by mapped fields without editing sibling
   paths.
5. Cross-check exact released registries, record the kernel pin, and serialize
   the profile-schema contract release against the latest bundle metadata.
6. Run strict validation and archive after the standards surface is merged and
   green.

## Open Questions

- Renderer, Flutter state management, media/storage packages, and native/web
  packaging remain ADRs in `implement-avatar-client-lab`.
- Formal accessibility qualification and domain onboarding remain in
  `avatar-pilot-hardening`.
