# Open Decisions — avatar client lab

Status: staged
Kind: architecture
Summary: The unresolved forks that block the avatar-client-lab topic from
becoming a proposal; each carries a recommended resolution to confirm or
override.
Topics: avatar-client, open-questions, decisions, schema-validation, accessibility, goldens, fixtures
Repository context: openxFactory (neutral) with the Flutter realization in `xfactory-avatar-client`
Staging ID: openxFactory:staging:avatar-client-lab
Source: v1 brainstorm 2026-07-13 (six-dimension synthesis)

Supporting fragment for [avatar-client-lab.md](avatar-client-lab.md). **These are
the blocking open questions — resolving them is the remaining staging work before
this topic promotes to a proposal.**

## Open questions (blocking)

1. **Dart JSON-Schema draft-2020-12 validator — adopt Workiva `json_schema`
   (Apache-2.0), or port the keyword subset?** The AVC schemas lean on `oneOf` +
   `not/anyOf` + `if/then` + `$ref`; several Dart validators implement these
   incompletely. It is the CI ground truth for type faithfulness.
   *Recommendation:* spike Workiva against all `fixtures/index.yaml` classes
   (redaction, unknown-authority, boundary) first; port the few-hundred-line
   subset if it or its license fails. Budget it as a real task.

2. **State-management binding — Riverpod 2 wrapping the pure core, or
   flutter_bloc?** *Recommendation:* Riverpod 2, one thin `Notifier` — its
   override mechanism most directly expresses injected clocks/ids + fixture
   replay, and doubles as DI. Both wrap the same pure core, so it is reversible at
   the wrapper. (Design-settled unless overridden.)

3. **Contract pin tracking — how are the two bundles (kernel v1.7 + ui-profile
   v1.8) tracked?** They evolve on different cadences; a partial bump could mix
   incompatible minors. *Recommendation:* record both refs (exact commit +
   per-file SHA-256) in one `contract_pin.yaml`; gate CI on both digest sets.

4. **Web accessibility conformance claim.** Canvas-rendered Flutter web cannot
   pass full WCAG 2.2 AA today. *Recommendation:* qualify accessibility on Windows
   desktop for v1; ship a documented WCAG exception register for web; do not claim
   web AA in F1-F4. Keyboard-only F1-F4 completion stays gating on desktop.

5. **Golden platform + web renderer.** Flutter goldens flake across
   platform/font/Skia-vs-Impeller and HTML-vs-CanvasKit. *Recommendation:*
   authoritative goldens on the Linux CI job only, bundled pinned font +
   version-pinned SDK; Windows and web run all tests except pixel goldens (web =
   headless-Chrome smoke). Treat any golden flake as a determinism bug, not a
   tolerance to widen.

6. **Fixture format duality.** The portable conformance suite
   (`contracts/avatar-client/fixtures/index.yaml`) and the UI-example fixtures
   (`examples/avatar-first-ui/fixtures/`) use slightly different shapes.
   *Recommendation:* one loader/normalization layer; `index.yaml` is authoritative
   for conformance, the example fixtures are UI-scenario seeds. Contribute neutral
   new scenarios upstream to openxFactory first; keep only app-specific
   presentation scenarios local.

## Lower-stakes (record, not blocking)

- Avatar animation-tech ADR: CustomPainter now; Rive documented as the
  interface-compatible later swap. The golden contract for any future renderer is
  the reduced-motion static frame + selector wiring + per-state non-color-cue
  presence — **not** animated pixel equality — so a swap cannot silently void the
  determinism guarantee.
- Renderer for the lightly-animated portrait behind the animation-state interface
  (procedural vs asset-driven) — decide at implementation.
- Read-only workflow rendering approach (structured Flutter widgets vs generated
  images) — the interactive canvas stays in the separate web console regardless.

## What resolving these unblocks

Once questions 1, 4, and 6 are decided (2, 3, 5 have strong recommendations),
this topic is ready to promote to the `implement-avatar-client-lab` proposal with
the forks recorded as locked decisions.
