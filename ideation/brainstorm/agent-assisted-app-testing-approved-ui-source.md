# Approved UI Source of Truth — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Separate approved runtime pixels, project experience intent, specialist analysis, and Subject Hermes authority so autonomous pixel review has explicit sources of truth without making Figma a runtime dependency.
Topics: agent-assisted-app-testing, approved-ui-source, runtime-baselines, design-tokens, figma, xfactory
Repository context: openxFactory; repo-first visual authority for browser apps with an optional design-tool projection and a future Flutter adapter
Captured: 2026-08-02

## Possible feats

- **Approved runtime snapshot bundle** — store reviewable, per-profile UI references with the render manifest, fixture state, and application revision that produced them.
- **Visual authority ledger** — record which artifact is authoritative for runtime pixels, design intent, diff interpretation, and final approval for each change.

## Focus

Pixel-perfect comparison needs an approved reference, but “the source of truth” is not one undifferentiated artifact. A rendered screenshot answers what the application looked like under a particular runtime profile. The project UI constitution, component specifications, and token sources answer what the product is intended to optimize for and allow. A designer agent can interpret a difference, but its judgment is not itself an admitted design decision.

The proposed v1 boundary is repo-first: approved runtime snapshots and their metadata live with the application and are reviewed through normal change control. This keeps the visual gate close to the code, makes the reference available to local and CI runners, and fits the xFactory preference for inspectable repository artifacts.

## Proposed authority split

| Concern | V1 authority | What it may decide | What it must not silently replace |
|---|---|---|---|
| Approved runtime pixels | Versioned repository snapshot bundle keyed by a render profile | Whether a capture matches the accepted rendering reference for that profile | Project experience intent or Product Owner admission |
| Project experience intent | Project UI constitution, personas, journeys, component specs, design tokens, accessibility/workflow rules, and fixture contracts | Whether a proposed change improves or preserves the intended experience | The actual pixels produced by the runtime |
| Visual interpretation | Independent Hermes design specialists, using machine evidence and optional design context | Whether a diff looks like an intentional change, a platform variance, a regression, or an inconclusive case | The approved snapshot or admission decision |
| Product experience admission | Project/Subject Hermes Project Owner, with Project Manager disposition and Experience Council evidence | Whether a candidate baseline and code revision preserve or improve user-visible product value | Raw evidence, Merge Council readiness, or external enforcement |
| Merge enforcement | Merge Master plus configured Git/CI policy | Whether an admitted, in-envelope revision may enter the repository's final merge path | Product intent, governing policy, or historical evidence |
| Design-tool context | Optional Figma document, variables, components, and links | Provide intent context or receive a projection of approved work | The repository runtime baseline |

This produces a deliberate authority chain:

```text
approved repo snapshots ── runtime pixel truth
UI constitution/specs ───── experience intent and safety constraints
Hermes specialists ──────── classification and proposal
Subject Hermes PO + PM ──── product admission and management
Merge Master + Git/CI ───── readiness enforcement
raw captures and diffs ──── immutable evidence
```

The Linux Loki container can remain the universal deterministic reference for the first browser gate. If exact platform rendering is also a product requirement, each supported OS/browser profile gets its own approved reference. These are related baseline families, not interchangeable images.

## Repo-first bundle

An illustrative repository layout is:

```text
ui-baselines/
  manifest.yaml
  components/
    Button/
      default/
        linux-chromium-v1.png
        macos-chromium-v1.png
        windows-chromium-v1.png
        state.yaml
```

`manifest.yaml` should identify the baseline schema, supported profiles, comparison thresholds, mask policy, and ownership. Each `state.yaml` record should identify at least the component or flow, state/fixture, route, application revision, render-manifest ID, viewport, device scale factor, and capture hash. The filenames are for navigation; the metadata is the authority for identity.

The reference identity is the tuple:

```text
(surface, state, application revision, fixture/state hash, render profile, baseline revision)
```

An image must not be approved without that identity. A changed browser, font set, OS image, viewport, fixture, or animation policy should produce a new profile or baseline revision rather than overwriting history in place.

## Figma boundary

Figma can be valuable as optional design context: variables, components, layout relationships, intended states, and links to the design review. A Figma MCP integration could let Hermes retrieve that context or publish a Project Hermes-admitted projection back to the design workspace.

It should not be the v1 runtime pixel authority. Figma renders a design representation, while the browser renders application code with fonts, browser behavior, data, accessibility state, and runtime conditions. Treating a Figma frame as the exact browser baseline would conflate design intent with rendered output and add a hosted dependency to the blocking test path.

The boundary can be revisited when a design-system synchronization need is demonstrated. Until then, Figma is an optional input or projection, and the repository remains the auditable source for approved runtime snapshots.

## Interfaces and boundaries

The baseline bundle is consumed by the Loki runner, Playwright visual tests, the diff-review packet builder, preview evidence, and future Flutter golden-test adapters. It emits references and metadata; it does not contain secrets, live production data, or approval logic embedded in image files.

The bundle should be versioned in ordinary Git when its size is manageable. Git LFS or an artifact store may later hold large images, but the manifest, hashes, ownership, approval record, and links must remain reviewable and content-addressed from the repository.

## Alternatives and tensions

- **Figma-first:** aligns runtime review with design files but risks treating design renders as browser truth and introduces synchronization and availability concerns.
- **Repo-first:** keeps pixels, code, tests, and approvals close together but requires deliberate snapshot storage and baseline maintenance.
- **Single Linux reference:** cheap and deterministic for CI, but insufficient when OS-specific rendering is part of the acceptance criterion.
- **Per-OS references:** closer to user-visible pixels, but multiplies captures, review workload, and migration work.
- **Token-only validation:** catches many intent violations without image churn, but cannot prove the final layout and rasterized rendering.

## Open questions

- Which browser surfaces are covered by an approved baseline: component stories, panels, full flows, or only designated critical states?
- Should the initial snapshot bundle use Git, Git LFS, or a content-addressed artifact store with a Git manifest?
- How do Project Owner experience admission, shared design-system ownership, and Merge Master enforcement compose when one baseline spans projects?
- Which Figma context is useful enough to justify an optional MCP adapter?
- Which OS/browser profiles are supported in v1, and which remain advisory?

## Relationships

- [OS Baseline Lifecycle](agent-assisted-app-testing-os-baseline-lifecycle.md) defines profile identity, update triggers, and approval-preserving maintenance.
- [Visual Diff Review](agent-assisted-app-testing-visual-diff-review.md) defines how raw pixels and reviewer-friendly derivatives are handled.
- [Hermes Designer Visual Review](agent-assisted-app-testing-hermes-visual-review.md) uses the bundle as evidence but cannot replace it.
- [Project UI Constitution and Experience Memory](agent-assisted-app-testing-ui-constitution.md) supplies design intent and project-specific quality objectives that screenshots cannot express.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) assembles the independent findings required before an in-envelope baseline is admitted.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) governs when Subject Hermes may approve a baseline without human management.
- [Chromium Render Manifest](agent-assisted-app-testing-chromium-render-manifest.md) supplies canonical browser and runner identity.
- [Synthesis: Hermes Autonomy and Human Exception Control](agent-assisted-app-testing-synthesis-human-control-and-safety.md) places baseline admission inside the broader authority model.
