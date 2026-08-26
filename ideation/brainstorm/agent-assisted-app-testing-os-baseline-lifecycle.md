# OS Baseline Lifecycle — Brainstorm

Status: brainstorm
Kind: process
Summary: Maintain approved visual references per supported OS/browser profile through immutable identities, candidate update pull requests, Subject Hermes experience admission, and explicit render-profile migration governance.
Topics: agent-assisted-app-testing, os-baselines, visual-regression, chromium, loki, baseline-maintenance, ci
Repository context: openxFactory; browser baseline maintenance for Linux Loki and supported macOS/Windows/Linux Chromium profiles, with a future Flutter golden-test mapping
Captured: 2026-08-02

## Possible feats

- **Render-profile registry** — enumerate supported OS/browser profiles and the exact environment inputs that make a baseline meaningful.
- **Baseline migration workflow** — generate candidate snapshot updates and require review whenever application code or the rendering environment changes.

## Focus

Pixel-perfect comparison is only useful when the approved reference is kept current without becoming mutable test noise. The reference must be per OS when OS-specific browser rendering is part of the product experience, while the canonical Loki container can still provide one deterministic, cross-developer CI lane.

The proposed model has two related lanes:

1. **Canonical lane:** pinned Chromium in the Loki container produces a stable Linux reference for deterministic gating.
2. **Platform lane:** supported macOS, Windows, and optionally Linux runners produce approved references for the user-visible rendering profile of each OS.

The platform references do not invalidate the canonical lane. They answer a different question: whether the application remains acceptable in a named supported environment.

## Profile identity

Every approved baseline is scoped to a profile containing, at minimum:

| Profile input | Example | Why it matters |
|---|---|---|
| OS identity | `windows-11-build-...` | Native text, controls, and compositor behavior can vary by OS build. |
| Architecture/runner | `amd64`, runner image digest | Machine and image changes can alter rasterization. |
| Browser | Chromium version and revision | A browser update can change layout, fonts, and rendering. |
| Browser binary/image | executable or OCI digest | A readable version is weaker than content identity. |
| Font bundle | font manifest and digest | Font availability and fallback affect geometry and pixels. |
| Viewport/DPR | `1920x1080`, `1` | Layout and rasterization depend on viewport and device scale. |
| Locale/timezone | `en-US`, `UTC` | Text, dates, and locale-sensitive layout must be stable. |
| Theme/motion/clock | light, reduced motion, frozen clock | Dynamic rendering must be controlled for repeatable captures. |
| Application state | route, fixture, state hash | A screenshot is meaningless if the rendered data differs. |

The profile ID should be content-addressed or linked to hashes of these inputs. A changed input creates a new profile or manifest identity; it does not silently move an old image under a new meaning.

## Repository representation

An illustrative layout is:

```text
ui-baselines/
  manifest.yaml
  profiles/
    linux-loki-chromium-v1.yaml
    macos-chromium-v1.yaml
    windows-chromium-v1.yaml
  components/
    CheckoutPanel/
      empty/
        linux-loki-chromium-v1.png
        macos-chromium-v1.png
        windows-chromium-v1.png
        state.yaml
```

The profile manifest should name the exact Chromium version/revision, runner or container digest, fonts, Playwright/Loki configuration, and rendering controls. The surface metadata should name the story or flow, state fixture, route, application revision, and expected comparison policy.

## Maintenance workflow

```text
code or render-environment change
          │
          ▼
capture every supported profile
          │
          ▼
raw deterministic diff + machine metrics
          │
          ▼
Hermes specialist classification and candidate explanation
          │
          ▼
baseline-update candidate PR
          │
          ▼
Experience Council + Project Owner admission
          │
          ▼
Merge Council/Master + Git/CI enforcement
          │
          ▼
merge snapshots and metadata together
```

The update must include before/current/expected images, raw diffs, profile IDs, application and fixture revisions, changed-region metrics, and the reason for the update. The Experience Council, Project Owner, and Merge Council should be able to tell whether the change is an intentional product adjustment, a rendering-environment migration, or an accidental baseline refresh.

The implementation or baseline worker may prepare the candidate branch or pull request. It must not replace an approved image in place, mark a failure as accepted by changing a threshold, or delete the prior reference before the Project Hermes admission and merge decision are recorded. A profile migration that changes the judging environment remains outside an ordinary UI repair unless policy explicitly classifies it.

## Update triggers and migration classes

- **Intentional UI change:** update only the affected surface/profile references after functional and spec checks pass.
- **Pinned Chromium update:** create a new render-manifest/profile family, recapture all required surfaces, and review the migration as a batch.
- **OS or runner image update:** create a new profile identity and retain the old profile for comparison until the migration is accepted.
- **Font or locale change:** treat as a rendering migration because small typography changes can affect large regions.
- **Fixture or clock change:** recapture only when the state contract deliberately changes; otherwise report state drift as a test failure.
- **Flaky capture:** quarantine and investigate the environment; do not bless a noisy capture as a new baseline.

Old baselines may be retired after migration, but the manifest should retain lineage from the superseded profile to the approved replacement. This makes a browser or OS upgrade explainable after the fact.

## Interfaces and boundaries

The lifecycle consumes application revisions, render manifests, test-state fixtures, and review policy. It emits approved references, candidate update evidence, and profile migration history.

It does not decide whether a design change is desirable, whether a spec violation is safe, or whether product value is preserved. Those decisions remain with the Project Owner, relevant spec authority, Experience Council, and v1 SDLC admission flow.

## Alternatives and tensions

- **Regenerate on every green build:** minimizes manual work but can erase regressions and makes approval implicit.
- **One Linux baseline only:** gives the simplest gate but cannot represent supported OS-specific rendering.
- **Per-OS baselines for every state:** maximizes fidelity but may create too much maintenance; coverage should begin with critical surfaces.
- **Hosted visual-regression service:** reduces local artifact handling but adds vendor, retention, and availability dependencies.
- **Repository images:** are transparent and reviewable, but large suites may need Git LFS or content-addressed storage later.

## Open questions

- Which OS/browser profiles are blocking in v1, and which are advisory parity checks?
- What is the minimum critical-surface set before per-OS coverage becomes too expensive?
- How are runner images and font bundles built, signed, and refreshed?
- Which profile migrations can Project Hermes admit, and which require shared design-system, infrastructure, or Domain Hermes authority?
- When can a superseded profile be retired, and how long must its evidence remain accessible?

## Relationships

- [Approved UI Source of Truth](agent-assisted-app-testing-approved-ui-source.md) defines what each profile's approved snapshot means.
- [Chromium Render Manifest](agent-assisted-app-testing-chromium-render-manifest.md) supplies the canonical environment identity.
- [Visual Diff Review](agent-assisted-app-testing-visual-diff-review.md) defines the evidence used before an update candidate is proposed.
- [Hermes Designer Visual Review](agent-assisted-app-testing-hermes-visual-review.md) explains the agent's role in update triage.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) supplies specialist findings and Project Owner admission for intentional baseline changes.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) prevents ordinary UI work from silently changing render profiles, thresholds, or masks.
- [Synthesis: Execution and Evidence](agent-assisted-app-testing-synthesis-execution-evidence.md) connects profile evidence to the intent and verification lineage.
