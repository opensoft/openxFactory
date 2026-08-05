# Chromium Render Manifest — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Define an immutable-by-identity rendering manifest that pins Chromium, the Loki container, fonts, and rendering settings for canonical visual baselines and paired user-browser comparisons.
Topics: agent-assisted-app-testing, chromium-render-manifest, loki, visual-regression, deterministic-rendering, browser-pinning
Repository context: openxFactory; v1 canonical browser-rendering contract for Loki baselines, verification evidence, and user-browser parity captures
Captured: 2026-08-02

## Possible feats

- **Chromium render-manifest schema** — describe the complete canonical rendering environment and its comparison policy in a versioned machine-readable record.
- **Baseline namespace registry** — store visual references under a manifest identity so a Chromium or font upgrade creates a new baseline family instead of silently changing history.
- **Paired capture record** — correlate a canonical Loki capture and a user's browser capture through a shared application state and intent revision.

## Focus

V1 needs one consistent visual reference for every developer regardless of whether their working browser is on macOS, Windows, or Linux. A pinned Loki/Chromium container can provide that reference, but Chromium's version alone is insufficient: the container image, fonts, locale, viewport, device scale factor, and runtime settings also affect the pixels.

The render manifest is the identity of the canonical rendering environment. It is separate from the application intent, user-browser metadata, and test-state fixture.

## Proposed model

The manifest should be immutable once used to create an accepted baseline. A new browser, OS, font, Loki, or rendering-policy change creates a new `manifest_id` and a new baseline namespace.

An illustrative Draft 2020-12 schema is:

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
$id: "urn:xfactory:agent-assisted-app-testing:chromium-render-manifest:v1"
title: Chromium Render Manifest
type: object
additionalProperties: false
required:
  - schema_version
  - manifest_id
  - browser
  - container
  - render
  - runner
  - comparison
properties:
  schema_version:
    const: "1.0"
  manifest_id:
    type: string
    pattern: "^[a-z0-9][a-z0-9._-]{2,127}$"
  browser:
    type: object
    additionalProperties: false
    required: [engine, version, revision]
    properties:
      engine:
        const: chromium
      version:
        type: string
        minLength: 1
      revision:
        type: string
        minLength: 1
      channel:
        const: pinned
      executable_sha256:
        type: string
        pattern: "^[a-f0-9]{64}$"
  container:
    type: object
    additionalProperties: false
    required: [image, digest, os, architecture, fonts_digest]
    properties:
      image:
        type: string
        minLength: 1
      digest:
        type: string
        pattern: "^sha256:[a-f0-9]{64}$"
      os:
        type: string
        minLength: 1
      architecture:
        enum: [amd64, arm64]
      fonts_digest:
        type: string
        pattern: "^sha256:[a-f0-9]{64}$"
  render:
    type: object
    additionalProperties: false
    required:
      - viewport
      - device_scale_factor
      - locale
      - timezone
      - color_scheme
      - reduced_motion
      - animations
      - clock
    properties:
      viewport:
        type: object
        additionalProperties: false
        required: [width, height]
        properties:
          width: { type: integer, minimum: 1 }
          height: { type: integer, minimum: 1 }
      device_scale_factor:
        type: number
        exclusiveMinimum: 0
      locale:
        type: string
        minLength: 2
      timezone:
        type: string
        minLength: 1
      color_scheme:
        enum: [light, dark, no-preference]
      reduced_motion:
        enum: [reduce, no-preference]
      animations:
        enum: [disabled, enabled]
      clock:
        enum: [frozen, real]
  runner:
    type: object
    additionalProperties: false
    required: [loki_version, config_digest]
    properties:
      loki_version:
        type: string
        minLength: 1
      config_digest:
        type: string
        pattern: "^sha256:[a-f0-9]{64}$"
  comparison:
    type: object
    additionalProperties: false
    required: [method, baseline_namespace]
    properties:
      method:
        enum: [pixel-diff]
      baseline_namespace:
        type: string
        minLength: 1
      max_diff_pixels:
        type: integer
        minimum: 0
      max_diff_ratio:
        type: number
        minimum: 0
        maximum: 1
      mask_set:
        type: string
        minLength: 1
```

The exact schema remains exploratory. The load-bearing rules are:

- no mutable browser tags such as `latest` or an unqualified `chrome-stable` in the canonical manifest;
- the OCI image is pinned by digest, not only by a human-readable tag;
- browser, fonts, and runner versions are recorded together;
- all visual settings needed to reproduce the capture are explicit;
- baseline references are namespaced by `manifest_id`;
- changing the manifest requires an explicit baseline migration and review.

### Paired canonical and user capture

The user's capture is not another canonical baseline. It can be linked to the canonical result with a separate record:

```json
{
  "intent_id": "intent_01J...",
  "application_revision": "git:abc123",
  "state_hash": "sha256:...",
  "canonical_manifest_id": "chromium-128-loki-01",
  "canonical_capture": "artifact://screenshots/canonical.png",
  "user_capture": "artifact://screenshots/user-browser.png",
  "user_environment": {
    "os": "win32",
    "browser": "chrome",
    "browser_version": "128.0.x",
    "viewport": "1920x1080",
    "device_scale_factor": 1
  },
  "comparison_status": "advisory-difference"
}
```

The pair is comparable only when the application revision, state hash, route, fixture data, viewport, and capture region agree. Differences caused by fonts or rasterization should be classified separately from layout, semantics, or interaction differences.

## Interfaces and boundaries

The manifest is consumed by the Loki runner, baseline storage, verification events, and parity-reporting UI. It emits a stable environment identity and comparison policy; it does not contain application code, user secrets, intent text, or approval decisions.

The in-house annotation client records the user's environment as observation metadata. It does not claim that the user's browser matches the canonical container. The canonical lane should capture deterministic test fixtures and should not receive production credentials or uncontrolled live data.

## Alternatives and tensions

- **Chromium versus branded Chrome:** Chromium is easier to pin and redistribute; branded Chrome may better match a user's browser but introduces distribution, policy, and update considerations.
- **Version pin versus image digest:** a version is readable; a digest is stronger for reproducibility. V1 should keep both and make the digest authoritative.
- **Canonical namespace plus per-OS namespaces:** the Loki namespace keeps deterministic CI simple, while named OS namespaces can provide platform-specific blocking or advisory checks; the combined model costs more capture and migration work.
- **Pixel-only comparison versus structural comparison:** pixel diff is deterministic inside the canonical environment; user-browser parity needs geometry and semantic signals in addition to pixels.

## Open questions

- Which Chromium version and container image will be the initial approved v1 manifest?
- Will the canonical image run on `amd64` only, or must the manifest support equivalent `arm64` captures?
- Which fonts are included, and how is the font bundle digest produced?
- Which Chromium/profile migrations may Project Hermes admit, and which require infrastructure, shared design-system, or Domain Hermes authority?
- Which user-browser differences are advisory, blocking, or automatically classified as expected platform variance?

## Relationships

- [V1 SDLC Session Protocol](agent-assisted-app-testing-v1-sdlc-session.md) references the manifest from verification events.
- [Cross-Environment Verification and Parity](agent-assisted-app-testing-verification-parity.md) consumes canonical and user captures.
- [Approved UI Source of Truth](agent-assisted-app-testing-approved-ui-source.md) distinguishes the canonical runtime reference from design intent and approval authority.
- [OS Baseline Lifecycle](agent-assisted-app-testing-os-baseline-lifecycle.md) uses manifest identity to govern per-profile baseline updates and migrations.
- [Visual Diff Review](agent-assisted-app-testing-visual-diff-review.md) consumes the manifest when producing reproducible raw comparisons and derivatives.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) consumes manifest-bound evidence before an intentional baseline change is admitted.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) prevents an ordinary UI change from silently altering the render environment or comparison policy.
- [Preview Verification and Feedback Loop](agent-assisted-app-testing-preview-approval.md) presents paired evidence for Project Hermes and optional human review.
