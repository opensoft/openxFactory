# Open Decisions — avatar client lab

Status: staged
Kind: architecture
Summary: The six forks that blocked the avatar-client-lab topic, now locked as
decisions with rationale (and, for the schema validator, a fallback trigger),
clearing the path to the implement-avatar-client-lab proposal.
Topics: avatar-client, locked-decisions, schema-validation, accessibility, goldens, fixtures
Repository context: openxFactory (neutral) with the Flutter realization in `xfactory-avatar-client`
Staging ID: openxFactory:staging:avatar-client-lab
Source: v1 brainstorm 2026-07-13 (six-dimension synthesis); decisions locked 2026-07-13 after schema/fixture inspection

Supporting fragment for [avatar-client-lab.md](avatar-client-lab.md). **These
were the blocking open questions; all six are now decided.** The three that
required investigation (Dart validator, fixture duality, web a11y) were resolved
against the actual AVC schemas (`avc-02`, `avc-04`, `shared-definitions`) and
both fixture formats; the other three were design-settled and are locked here
with rationale. Nothing below is a recommendation to confirm — each is a locked
decision.

## Decisions (locked)

1. **Dart JSON-Schema draft-2020-12 validator — adopt Workiva `json_schema`
   (Apache-2.0), gated behind a bounded spike; port only on a named failure.**
   Inspecting AVC-02, AVC-04, and shared-definitions, the load-bearing keyword
   subset is: a root `oneOf` (AVC-02 grant vs non_grant discriminated union);
   `not: {anyOf: [{required: [...]}]}` structural credential/SDP exclusion
   (AVC-02 non_grant, AVC-04 payload); `allOf` + `if`/`then` producer-authority-
   by-class (AVC-04); cross-file relative `$ref` into
   `shared-definitions.schema.yaml#/$defs/…` alongside local `#/$defs` refs; and
   `const`, `enum`, `pattern`, `additionalProperties: false`, `minLength`,
   numeric `minimum`/`maximum`, and single-schema `items`. Critically, the
   draft-2020-12 features Dart validators most often miss are **absent** — no
   `$dynamicRef`/`$dynamicAnchor`, no `unevaluatedProperties`, no tuple
   `prefixItems` — so the risk surface is confined to well-supported keywords.
   Workiva `json_schema` is the only Dart validator with declared 2019-09/2020-12
   support, an Apache-2.0 license compatible with this repo, and a synchronous
   `RefProvider`/registry that resolves the cross-file `$ref` graph fully offline
   (register shared-definitions + every AVC schema; no network). Hand-porting
   would duplicate a maintained, spec-tested engine for no gain unless it
   actually fails. **Fallback trigger (locked):** fall back to porting the
   keyword subset — a few-hundred-line hand-written validator covering exactly
   `$ref` (cross-file + local), `oneOf`, `allOf`, `not`, `anyOf`, `if`/`then`,
   `const`, `enum`, `pattern`, `additionalProperties: false`, `required`,
   `minLength`, numeric bounds, and single-schema `items` — **if and only if**
   the spike shows Workiva, at the pinned version, either (a) mis-evaluates any
   AVC case, specifically the `not/anyOf` credential-exclusion (redaction class),
   the grant/non-grant `oneOf` discrimination, the `if/then` producer-authority
   (unknown-authority class), or cross-file relative `$ref` resolution, such that
   any `fixtures/index.yaml` `expect` disagrees; or (b) lacks true draft-2020-12
   evaluation at that version; or (c) fails license or transitive-dependency
   review. The spike is a budgeted task, not incidental work: its exit gate is a
   clean replay of all eight fixture classes (valid / invalid / boundary /
   compatibility / unknown-field / unknown-authority / redaction / adversarial)
   plus the `release_pin_cases`. It is CI ground truth for type faithfulness, so
   it is decided before the dependency is pinned, not after.

2. **State-management binding — Riverpod 2, one thin `Notifier` over the pure
   core; not flutter_bloc.** The session core is a pure, synchronous reducer with
   no `dart:async` in the reduce path, and the whole lab rests on bit-exact
   replay determinism. Bloc's Stream/async substrate would inject ordering
   nondeterminism where the runtime has exactly none. Riverpod's provider-override
   mechanism *is* the fixture-replay / injected-clock+id seam and doubles as DI,
   so the wiring the lab needs falls out of the framework rather than being bolted
   on. Both bind the same pure core, so the choice stays reversible at the wrapper
   — but there is no determinism-neutral reason to pay Bloc's async cost here.

3. **Contract pin tracking — one `contract_pin.yaml`, both digest sets, both
   gated.** Record `contract-v1.7` (kernel) and `contract-v1.8` (ui-profile)
   provenance in a single vendored `contract_pin.yaml` — exact commit **plus**
   per-file SHA-256 for every pinned file of both bundles — and gate CI on both
   digest sets. No submodule; a tag-only pin fails. The two bundles evolve on
   independent cadences, so a partial bump can silently mix incompatible minors;
   one pin file with both digest sets turns any drift into a hard CI failure and
   makes the content-addressed rule already encoded in `fixtures/index.yaml`
   `release_pin_cases` (SCO-001-S03) the exact gate — the pin-tag-only case must
   fail, the commit-plus-file-digests case must pass. A single file keeps the two
   cadences visibly coupled at review time instead of split across two places
   where one can be forgotten. The pin verifies against `contracts/manifest.yaml`
   — the authoritative published per-file-digest index for both bundles — rather
   than maintaining a divergent list; because the v1.8 UI-profile digested set
   (profile schema + its fixtures + acceptance map) has no published enumeration
   beyond the manifest, the pin must enumerate it explicitly.

4. **Web accessibility conformance claim — Windows desktop qualified for v1;
   documented WCAG exception register for canvas web; no web AA claim in F1-F4.**
   Accessibility is qualified on Windows desktop for v1; canvas-rendered
   (CanvasKit) Flutter web ships a documented WCAG 2.2 exception register; F1-F4
   makes **no** web AA conformance claim. Keyboard-only F1-F4 completion stays
   gating on desktop. Canvas web cannot pass full WCAG 2.2 AA today — its
   semantics layer is partial and its assistive-technology surface is not
   equivalent to native desktop — so an AA claim on web would be unprovable and
   misleading. Qualifying on Windows desktop lets the eleven avatar-first UI
   baseline capabilities and keyboard-only F1-F4 be real gating tests where they
   can actually be met, while the exception register makes the web gap explicit
   and auditable rather than hidden. Full WCAG audit + platform qualification is
   the deferred successor `avatar-pilot-hardening` (avatar-first UI acceptance
   map, AFU-005), not this lab.

5. **Golden platform + web renderer — authoritative goldens on the Linux CI job
   only.** Pixel goldens run only on the Linux CI job, with a bundled pinned font
   and a version-pinned Flutter SDK; Windows and web run every test **except**
   pixel goldens (web = headless-Chrome smoke). Any golden flake is treated as a
   determinism bug to fix, never a tolerance to widen. Flutter goldens vary across
   platform, font, and rasterizer (Skia vs Impeller, HTML vs CanvasKit); pinning
   goldens to one Linux job with a pinned font + SDK removes every one of those
   axes as a variable, so a diff means a real regression. Because the avatar
   renderer owns no clock (phase is injected) and presentation is a pure selector
   over authority, frame-exactness is achievable — so widening tolerance would
   mask exactly the determinism failures the lab exists to catch. Non-golden tests
   still run everywhere to keep cross-platform behavior honest.

6. **Fixture-format duality — one loader; `index.yaml` authoritative for
   conformance; example fixtures are UI seeds.** The two formats are genuinely
   different because they test different things, so they are normalized at load
   time, not on disk. The exact shape difference (from reading both):

   - **Conformance suite — `contracts/avatar-client/fixtures/index.yaml`:** a
     single index file holding two lists, `cases` and `release_pin_cases`. Each
     `cases` entry keys on `case_id`, names a `target` schema file +
     `target_kind: schema`, declares `expect: valid|invalid` and a taxonomy
     `class:` (valid / invalid / boundary / compatibility / unknown-field /
     unknown-authority / redaction / adversarial), carries `scenario_ids: []` and
     an optional single `evidence_id` (a `TEST-*` id), and puts the payload under
     `instance:` — a raw AVC message validated against the draft-2020-12 schema
     named by `target`. `release_pin_cases` entries swap `instance` for a `pin:`
     descriptor (`bundle_tag`/`commit`/`file_digests`). Portable: any conformant
     validator runs the whole suite from this one file.
   - **UI-example fixtures — `examples/avatar-first-ui/fixtures/*`:** one fixture
     per file, `kind: xfactory_avatar_first_ui_fixture`, keyed on `fixture_id`,
     with `evidence_ids` as a **list** of scenario ids (`AFU-*-S*`). There is no
     `target`/`class`/`expect`. Instead: deterministic fixtures carry `inputs:` +
     `canonical:` + `expected:` (a positive expected view-state / records);
     negative fixtures carry `expect_error: <AFUV-rule-code>` + `candidate:` (a UI
     profile that must fail a named validator rule); compatibility fixtures carry
     just `candidate:` (a profile that must validate clean). The payload key is
     `candidate:` (a UI profile), not `instance:` (an AVC message), and the
     checker is `scripts/validate-avatar-first-ui.py` against the UI standard, not
     a JSON-schema engine.

   So they differ on file organization (one index of lists vs one-fixture-per-
   file), id key (`case_id` vs `fixture_id`), evidence (single string
   `evidence_id`/`TEST-*` vs list `evidence_ids`/`AFU-*-S*`), expectation model
   (`expect: valid|invalid` against a named schema vs positive `expected:`
   view-state or negative `expect_error:` rule-code), payload key (`instance:` raw
   AVC message vs `candidate:` UI profile or the `inputs`/`canonical`/`expected`
   triple), and validator (portable draft-2020-12 schema vs
   `validate-avatar-first-ui.py`). **Decision:** one loader in the lab normalizes
   both into a common in-memory fixture record — `{ id, source, evidence_ids[],
   expectation, payload }` where `expectation` is a tagged union over
   {schema-valid, schema-invalid, expect-error(rule), expected-view-state} — while
   the two on-disk formats stay distinct and each authoritative in its own lane.
   `contracts/avatar-client/fixtures/index.yaml` is the authoritative conformance
   suite (AVC message → draft-2020-12 schema; CI type-faithfulness ground truth);
   `examples/avatar-first-ui/fixtures/*` are UI-scenario seeds that drive the
   presentation / view-state acceptance, not conformance. New **neutral**
   conformance scenarios are contributed upstream into `index.yaml` first; only
   app-specific presentation scenarios stay local. The loader never rewrites
   either file into the other's shape — it reads both and yields one record type.
   Collapsing them into one on-disk schema would either weaken the portable
   conformance suite or force UI seeds to masquerade as AVC messages; normalizing
   at load time keeps each file's authority and portability and keeps the
   neutral-first contribution rule (architecture-and-stack.md claim 7)
   enforceable.

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
- The F1-F4 acceptance-focus decomposition proposed in
  [acceptance-and-tests.md](acceptance-and-tests.md) — organizational, not
  architectural; confirm at the proposal gate.

## Exit

All six forks are locked, so this topic is ready to promote. Create
`implement-avatar-client-lab` (`code_surface: openxFactory,
xfactory-avatar-client`; `target_release: implemented`); at the proposal gate,
move this folder's files into that change's `supporting-docs/` with the six
decisions above carried in as locked constraints on the F1-F4 build — the
Workiva-with-fallback spike as a budgeted first task, `contract_pin.yaml` (both
digest sets) and the Linux-only goldens as CI gates, the one-loader fixture
normalization as the acceptance harness, and the desktop-qualified accessibility
claim (web exception register) as the conformance boundary.
