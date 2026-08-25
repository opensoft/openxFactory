# Design: Workbench Bullseye + Gated Document Creation

## Context

Two coupled deltas to the staged-workbench surface, both from Brett's
2026-07-25 dogfood pass on the workbench that landed the same day.

The workbench is a full-screen overlay scoped to exactly ONE topic-bearing
tile (a cluster, a possible, or a staged topic) with three tabs — `docs`,
`lens`, `outline`. `add-staging-workbench` deliberately shipped it read-only:
"nothing here may be designed as if the chat layer already exists". This
change does NOT open the chat layer. It finishes a renderer that was already
paid for, and it adds the ONE write the surface needs to be a working
surface: bringing a document into existence.

Three facts about the existing code set the shape:

1. **The bullseye geometry is already computed at tile scope and discarded.**
   The workbench lens panel calls `buildLensModel(scopedSnapshot, {checked})`
   — the SAME function the main lens tab calls — and that function returns
   `rings`, `sectors`, and `dots` from `bullseyeLayout()`. The panel renders
   only `model.matrix`. There is nothing to compute; there is a renderer to
   reach.
2. **The authoring engine is complete, tested, and create-only.**
   `authoring.render_scaffold` emits the controlled header block in the
   `ideation/README.md` order; `authoring.create_scaffold` writes it through
   `boundary.OutputBoundary.create_document`, which refuses an existing
   target as `SOURCE_EDIT`. `cli.py create` already composes this with
   `edit_command`. What has no wire is a GATE route.
3. **The gate-verb pattern is now well worn.** `add-propose-verb` and
   `add-lens-gate-verbs` both installed the same shape: a
   `POST /actions/gate/<verb>` route in `gate_routes.py` that constructs a
   `HumanGate` with the server's resolved local actor, drives an existing
   engine with no engine change, writes a gate-action record, surfaces the
   engine's refusal verbatim, and offers a CLI parity subcommand. This
   change is one more instance, not a new mechanism.

## Goals / Non-Goals

**Goals**: make the workbench's scope legible in the shape the dashboard
already teaches (rings by match count); stop discarding the human's checked
set between tabs; let the human create the document they have decided on
without leaving the scope that justifies it, with the seeding done from what
the scope already knows and the provenance recorded; keep every write on the
gate path, recorded, human-only, loopback-only, and reversible by the
ordinary means (the document is a new file, nothing existing was touched).

**Non-Goals**: any EDIT or delete path; the brainstorm's recipe-seeded
reference set and scratch notebook; doxBench's chat layer (then called Track C)
and any generated
prose; new snapshot fields; new analysis or scoring; the other two
keyword-lens feat requests; row-level "seed from this document" (open
question 3).

## Decisions

### D1 — One bullseye renderer in the bundle, lifted into a shared widget
**Decision**: the SVG bullseye renderer moves out of `views/lens.js` into a
shared widget module, and BOTH the main lens tab and the workbench lens panel
consume it. Neither view keeps a private copy.

**Rationale**: the alternative — a second renderer in
`staging-workbench.js` — would put two hand-written SVG layouts over one
geometry function, and the first divergence (a ring label, a dot radius, the
centre-zone shading) would be invisible until someone compared screenshots.
The geometry is already shared (`bullseyeLayout` in `lens-model.js`); the
drawing should be too. The lift is mechanical: `bullseye(model)` and its
`svg()` helper are already pure functions of the model plus `GEOM`, with no
lens-tab state reached into.

**Consequence**: the widget module takes `(model, opts)` and returns an SVG
node, with the centre-ring click handler supplied by the CALLER (D6) — the
main lens tab passes none in this change, so its behaviour is byte-identical
to today.

### D2 — The scoped bullseye introduces no new number
**Decision**: the workbench bullseye is rendered from the scoped
`buildLensModel` result verbatim. Rings are match counts over the LIVE
checked set; dots are the scope's own documents; the rail's `declaredCount`
stays the snapshot's corpus-wide declared count, labelled as such, exactly as
the panel already does.

**Rationale**: `add-staging-workbench`'s lens requirement is explicit that
the panel MUST NOT introduce a new analysis, a new score, or a new snapshot
field, and the model module's own comment states the principle — "the
workbench introduces no number the rest of the dashboard cannot show you". A
scoped recount of keyword counts would create a second, quieter set of
numbers for the same words. Rendering geometry the scoped model already
returns adds no number at all.

### D3 — The matrix stays ALWAYS present, below the bullseye
**Decision**: the bullseye renders ABOVE the flat matrix; the matrix is never
a toggle-only alternate and is never hidden.

**Rationale**: the promoted `Keyword lens set-builder` requirement carries
this as its own scenario ("a flat matrix or list view of the same membership
MUST be available"), and it is an accessibility guarantee, not a layout
preference — the SVG carries an `aria-label` but the table is the readable
surface. Placing the bullseye first matches the main lens tab's pane order so
the two surfaces read the same way.

### D4 — Checked-keyword selection is workbench-SESSION state
**Decision**: the checked set lives at the workbench shell's scope lifetime,
not inside the lens panel's `draw()` closure. Switching tabs preserves it;
opening a DIFFERENT scope or closing the workbench discards it and reseeds
from `lensSeedKeywords`.

**Rationale**: today the panel constructs `new Set(lensSeedKeywords(...))` on
every mount, so `lens → docs → lens` silently destroys the set the human just
built — and after this change that set is also the `Topics:` seed for a
create, which makes losing it a correctness problem and not just an
annoyance. Scope-lifetime (rather than page-lifetime) is the honest boundary:
a checked set is a statement about ONE scope's keywords, and carrying it into
a different tile would apply keywords the new scope may not even declare.

**Consequence**: the shell owns the state and hands it to the panel; the
panel's `draw()` mutates the shell's set rather than a local one. This is
also what lets a create dialog opened from the `docs` tab read the lens
tab's live selection if that is ever wanted — but in this change each tab
seeds from its own material (D7), so no cross-tab read is introduced.

### D5 — Renderer transport constraints, and where the POST goes
**Decision**: `views/staging-workbench.js` performs NO transport. The create
POST lives in a NEW sibling module (the `dispose.js` / `gate.js` /
`lens.js` pattern), which uses `const doFetch = fetcher || fetch` and takes
its fetcher by injection. `views/staging-workbench-model.js` stays
import-free.

**Rationale**: these are not style preferences, they are pinned invariants
that will fail the suite if violated, and realization must know them before
writing a line:

- `tests/ideation-dashboard/test_staging_workbench.py` asserts
  `"fetch(" not in view`, `"POST" not in view.replace("no POST", "")`, and
  `"XMLHttpRequest" not in view` against `staging-workbench.js`, and asserts
  the model module has NO top-level `import` (it is copied ALONE into the
  node harness).
- `tests/ideation-dashboard/test_renderer.py` pins the SET of bundle files
  containing `fetch(` to exactly `{app.js, viewer.js, notebook.js, wheel.js}`
  with a per-file call count. The `doFetch` spelling is what keeps
  `lens.js` / `dispose.js` / `gate.js` out of that set (the pin is
  case-sensitive on `fetch(`), so the new module MUST use the same spelling
  or it will trip the pin.
- `test_renderer.py` also bans external URLs and network primitives
  (`XMLHttpRequest`, `WebSocket`, `EventSource`, `navigator.sendBeacon`)
  across the bundle.

**Consequence**: `mountStagingWorkbench(container, snapshot, {onOpenDoc})`
grows `caps` and `fetcher` parameters — it receives NEITHER today, and
`app.js` must thread both (it already holds `caps` from the ONE capability
probe and already threads a fetcher pattern into the gate bar). Threading
`caps` is what makes the posture pill (D9) and the descriptor fallback (D8)
possible at all.

### D6 — The centre ring is a create gesture, WITH an explicit button
**Decision**: clicking the bullseye's centre ring (the matches-ALL zone)
opens the create dialog, AND the forming-set pane carries an explicit
labelled button that opens the same dialog. Both, not either.

**Ruled and EXTENDED, 2026-07-25 (Brett, open question 2)**: the centre-ring
gesture stays, and it generalizes — clicking or keyboard-activating ANY ring
SECTOR opens the same create dialog, seeded with THAT sector's matched
keyword combination. Each ring is sectored by which checked keywords a
document matched, so a sector already names a specific combination; the
centre region (matches-ALL) is simply the sector whose combination is the
whole checked set. Every sector is keyboard-reachable on the same terms as
the centre region, and every sector opens the ONE dialog with the ONE seeding
rule — the only thing a sector changes is which subset of the checked
keywords arrives as `Topics:`. The explicit labelled button remains (it seeds
the full checked set), so the discoverable path is unchanged.

**Rationale**: the centre ring is Brett's gesture from the brainstorm and it
is the right one — the innermost zone IS "the thing I am currently thinking
about", so acting on it there is the shortest honest path from thought to
document. But a click target with no label is undiscoverable and unreachable
by keyboard, so it cannot be the only affordance. The button is the
discoverable, focusable, screen-reader-legible path; the ring is the fast
one. They open ONE dialog with ONE seeding rule, so they can never diverge.
(Open question 2 records this as Brett's to confirm.)

**Consequence**: the widget module's hit regions — the centre region AND
every ring sector, per the ruling — take an `onActivate` callback from the
caller and are keyboard-reachable when one is supplied; when none is supplied
(the main lens tab, this change) every region is inert and the SVG is
byte-identically rendered. The callback receives the activated region's
matched-keyword subset, so the caller never has to re-derive it from
geometry.

### D7 — Seeding is per-tab and deterministic, and the human still confirms
**Decision**: each tab seeds the create dialog from the material that tab is
showing, and the dialog is EDITABLE before the create fires.

| tab | area | Topics: | Source: |
| --- | --- | --- | --- |
| `docs` | staged scope → the staging topic folder; cluster / possible scope → `ideation/brainstorm/` | the tile's `scope.keywords` | the workbench scope (kind + id) |
| `lens` | same rule as `docs` | the LIVE checked keyword set (D4) | the recipe — checked + pinned — at the snapshot's `source_revision` |
| `outline` | the staging topic folder (staged scopes only) | the tile's `scope.keywords` | the workbench scope (kind + id) |

`Repository context:` defaults from the served snapshot's `repository` on
every tab. `Kind:` defaults to the engine's own default. `Summary:` and
`Title:` have no honest machine seed and are the human's to type.

**Ruled 2026-07-25 (Brett, open question 1)**: `Status:` is seeded
`brainstorm` on every tab, in every area — "these are brainstorm docs". The
area column above is UNCHANGED and is where the packet tie lives: a create
from a staged tile lands the file inside `ideation/staging/<topic>/`, which
is what ties it to the packet and what makes it count toward that folder's
folder-scoped health and readiness; a create from a cluster or a possible
lands in `ideation/brainstorm/` and is tied to its neighbours only through
`Topics:`. PLACEMENT carries the relationship; `Status:` carries the
lifecycle stage, and the stage of a just-captured thought is `brainstorm`
wherever it sits. The field stays editable in the dialog, so a human who
knows they are writing an organized fragment can say `staged` on the spot.

**Ruled 2026-07-25 (Brett, open question 3)**: the per-row "seed from this
document" affordance on `docs` rows is DEFERRED to a follow-on change, as
recommended — it needs row-selection state the `docs` panel does not have.
Unchanged as a non-goal here.

**Rationale**: the seeding exists to stop the human retyping what the
workbench already knows; it does not exist to guess. `Topics:` and the area
are derivable with certainty from the scope; a summary is not, and a
generated one would be prose the dashboard invented — squarely doxBench
territory. Citing the recipe at the snapshot's `source_revision` (rather
than at wall-clock time) is what makes the `Source:` line reproducible: the
recorded keywords plus that revision re-derive the exact membership that
motivated the document, which is the brainstorm's own stated goal — "a
brainstorm born with machine-checkable provenance about WHY it exists".

**Consequence**: the `outline` affordance is HIDDEN, not disabled, for
cluster and possible scopes — there is no topic folder to write a fragment
into, and a disabled button implies a missing precondition the human could
satisfy from here, which they cannot.

### D8 — Gate-off renders a copyable CLI descriptor, never a live button
**Decision**: with `caps.actions.gate` false (the hosted static image, a
non-loopback bind, or an unresolved actor), every create affordance renders
as a copyable CLI descriptor — the exact `cli.py gate create-document ...`
invocation with the seeded values filled in — and no POST is possible from
the page.

**Rationale**: this is the established house posture (the gate bar's
descriptor rendering, the lens plan panel's plan-only fallback) and it is
what the brainstorm itself asked for: "like the gate bar, the gesture emits
the CLI descriptor ... until a write-enabled authenticated host phase
exists". A descriptor is strictly more useful than a greyed-out button
because it is the whole action, transportable to where the authority lives.
Enforcement is at the ROUTE regardless: the route is loopback-only and
fail-closed on an unresolved actor, so hiding the button is a UX courtesy,
never the security boundary.

### D9 — The posture pill stops being a constant
**Decision**: the workbench header's pill reads `read-only` when the gate
capability is off and states the gate-bearing posture (with the resolved
actor) when it is on.

**Rationale**: the pill currently says `read-only` with the tooltip "the
staging workbench writes nothing". After this change that is FALSE on a
loopback bind, and a surface that misdescribes its own authority is worse
than one with no pill. Making it capability-derived also means the hosted
image keeps the exact string it shows today, so the read-only audience sees
no change.

### D10 — `create-document` drives the existing engine; the route is transport
**Decision**: the route validates and normalizes the payload, constructs a
`HumanGate` with the server's resolved actor and the records allowlist, calls
`authoring.create_scaffold`, writes the gate-action record, and returns.
There is NO new writer, NO new header renderer, and NO change to
`authoring.py` or `boundary.py`.

**Rationale**: `gate_routes.py`'s own header states the rule — "this module
is transport, the console is the law" — and the engine's guarantees are
exactly the ones this verb needs: controlled header order, the
`— Brainstorm` H1 suffix, `slug()`-normalized filenames so a hostile title
cannot traverse the workspace, and create-only semantics. Re-deriving any of
that at the route would be a second implementation of a tested contract.

**Consequence**: two known realization details, recorded so they are not
discovered late. (a) `boundary.create_document` deliberately does NOT consult
the output allowlist — `area` is a SOURCE directory like
`ideation/brainstorm/`, not a declared output path — so ANY source area
works, and the create-only refusal (existing target → `SOURCE_EDIT`) is the
whole protection. That is the documented design of the engine, not a hole to
patch here. (b) `gate_console.write_gate_action_record` derives its record
filename's `target_id` from `change_id or possible_id or target["topic_id"]`
and will `KeyError` on a document-only target; the derivation must accept
`target["document"]` (slugged for the path segment) for this action.

### D11 — Human-only, at the route, with the agent path refused
**Decision**: the verb is `HumanGate` + `require_human_gate` — an agent actor
is refused and reported, and the refusal is a recorded refusal like every
other boundary refusal. Loopback-only; unresolved actor fails closed.

**Rationale**: identical posture to propose and the two lens verbs, and it is
structural rather than a runtime flag: `HumanGate.__init__` raises without an
identified human actor, and `boundary.py`'s "machinery vs. HumanGate" split
means there is no agent code path to this route to begin with. Document
CREATION by agents is a DIFFERENT, already-specified surface
(`authoring.agent_capture`, the `Agent create-only capture` requirement) with
its own header enforcement — this verb does not widen it and does not
replace it.

### D12 — Additive gate-action-record growth, mirroring the lens verbs
**Decision**: `contracts/schemas/gate-action-record.schema.yaml` grows the
`action` enum value `create-document`; the EXISTING optional
`target.document` field's commentary is broadened (it currently reads
"document path within the change — e.g. the concept `edit-apply`
targeted"); and one `allOf` conditional requires `target.document` when
`action == create-document`. No `schema_version` bump, no
`additionalProperties: false` anywhere, every prior record still valid.

**Rationale**: this is exactly the shape `add-lens-gate-verbs` used at
realization (commit `0cf3864`: enum growth plus one optional `target` field,
with the additive posture stated in the schema's own commentary). The
per-action conditional is safe because no record has ever carried
`action: create-document`, and it is worth having: a create record whose
target does not name the created document is not an audit record of
anything. The conditional mirrors the `propose` conditional's shape.

**Consequence (superseded by ruling)**: as authored, the record's single
artifact was to be the created document carried as an `other`-kind artifact
with the relpath as its `reference` — `artifacts` has `minItems: 1`, and the
existing `kind` enum had no document-shaped value. Whether that enum should
grow a named kind was open question 4.

**Ruled 2026-07-25 (Brett, open question 4)**: the artifact `kind` enum GROWS
a first-class `document` value NOW, and the create record's artifact rides as
`kind: document`. The `other`-in-v1 recommendation above is superseded by the
ruling — it is kept for the reasoning history, not as the decision. So D12's
schema growth is FOUR additive edits, not three: the `action` enum value
`create-document`, the broadened `target.document` commentary, the per-action
`allOf` conditional (which now also requires a `document`-kind artifact, the
enforcement the named kind makes possible and which `other` could never
carry), and the artifact `kind` enum value `document` with commentary naming
this change as the growth source. Still no `contract_schema_version` bump and
still no invalidated record: the enum only WIDENS what a `kind` may say, and
the one narrowing conditional is scoped to an action no record has ever
carried.

### D13 — This realizes ONE slice of the brainstorm, and says so
**Decision**: the change realizes the scaffolded-document slice of
`lens-brainstorm-session-launch.md` and NOT its other two composed
mechanisms (the recipe-seeded workbench reference set, the optional
`xf-wb-*` scratch notebook), nor the `lens-launch` manifest-history action
they imply. The brainstorm stays `brainstorm`, cited here as design
provenance.

**Rationale**: the set and the notebook are writes into a DIFFERENT family
(`workbench.py`'s `ideation-workbench` manifests — the other sense of
"workbench" that `add-staging-workbench` design D5 deliberately keeps
apart), and the `lens-save-recipe` verb `add-lens-gate-verbs` just landed
already covers assembling and persisting a reference set from the lens. A
human who wants both today does two gestures. Composing them into one is a
plausible successor and a bad thing to bundle into the change that first
introduces a workbench write.

**Consequence**: `lens-ring-combination-explorer.md` and
`lens-keyword-search-and-adhoc.md` are untouched. All three lens feat
requests remain live brainstorm material for a future `lens-enhancements`
staging topic, as their own Exit sections propose.

## Risks / Trade-offs

- **The first write on a surface that shipped as read-only.** The
  read-only guarantee was load-bearing — it is what let
  `add-staging-workbench` say doxBench would inherit "a clean, already-proven
  foundation". Mitigation: the write is ONE verb, on the gate path, recorded,
  human-only, loopback-only, and create-only — it cannot alter or remove
  anything that exists. The read-only guarantee is not weakened for EDITS,
  which is the guarantee doxBench actually depends on.
- **"Create" will be read as an invitation to draft.** A create dialog two
  clicks from a scope full of related documents makes a generated summary
  feel like the obvious next feature. Mitigation: D7's explicit rule that
  `Summary:` and `Title:` have no machine seed, and the non-goal naming
  generated prose as doxBench's.
- **Seeded areas can put a document in a surprising place.** A cluster-scoped
  create lands in `ideation/brainstorm/` even when the human was thinking
  about a staged topic the cluster feeds. Mitigation: `area` is editable in
  the dialog and the descriptor shows it verbatim; the create is create-only,
  so a wrong area costs one file in the wrong folder, not a lost document.
- **Lifting the bullseye renderer touches the live lens tab.** The main lens
  tab is deployed and dogfooded daily; a refactor there is a regression
  surface. Mitigation: the lift is a pure-function move with no signature
  change for the existing caller, the geometry module is untouched, and the
  existing lens tests plus a Playwright pass over both surfaces are the gate
  (task 6.2).
- **Session-scoped checked state is a small piece of hidden state.** A human
  who returns to the `lens` tab and sees their old selection may not
  remember making it. Mitigation: the selection is fully visible in the rail
  (it IS the checkboxes), and it resets on every scope change — the two
  cases where forgetting would matter.
- **Status headers on documents created into staging folders.** Open
  question 1 asked whether a `brainstorm`-status document sitting in
  `ideation/staging/<topic>/` is a lifecycle inconsistency the doc-health
  and completeness machinery will notice. Brett RULED `brainstorm` always
  (below), so this is now a deliberate state rather than an accident: a
  freshly captured thought inside a staging packet is a `brainstorm` doc in
  that packet, and the packet's health machinery sees it as unpromoted
  material — which is what it is. Residual risk: if doc-health treats
  `brainstorm`-in-staging as a FINDING rather than as normal unpromoted
  material, creates into staging folders will generate health noise.
  Mitigation: the `Status:` field is editable at create time, promotion to
  `staged` is the ordinary one-line lifecycle edit the pipeline already
  expects, and any doc-health rule that disagrees is a doc-health question
  to raise there, not a reason to born-mislabel a document.

## Open Questions — RULED 2026-07-25 (Brett, binding)

All four are closed. Brett's rulings are recorded VERBATIM below, each above
the question and recommendation it answers; the recommendations are kept as
reasoning history, and where a ruling went the other way the recommendation
is marked superseded rather than deleted.

> **Q1**: created documents are ALWAYS `Status: brainstorm` ("these are
> brainstorm docs"). The tie to a staging packet comes from PLACEMENT, which
> the generator already derives from path: created from a staged tile → the
> file lands in ideation/staging/<topic>/ (tied to the packet, counts toward
> its folder-scoped health/readiness); created from a cluster/possible →
> ideation/brainstorm/, tied only via Topics. NO area-derived `staged` status
> — that part of the realization is REVERSED.
>
> **Q2**: center-ring create stays, AND is EXTENDED — clicking ANY ring
> sector opens the create dialog seeded with that sector's matched keyword
> combination (each ring is sectored by which checked keywords matched; the
> center region = all checked). Keyboard-reachable like the center region.
>
> **Q3**: per-row "seed from this document" DEFERRED to a follow-on change
> (as recommended).
>
> **Q4**: the gate-action-record artifact `kind` vocabulary GROWS a
> first-class `document` value now (Brett rejected the `other`
> recommendation); the create record's artifact uses `kind: document`.

Where each ruling lands in this design: Q1 → D7 (and it REVERSES the
`status_for_area()` behaviour the first realization pass shipped; see
tasks.md "Realization notes"); Q2 → D6 and D1's widget seam; Q3 → unchanged
non-goal; Q4 → D12 and the schema growth.

1. **The `Status:` header for a document created into a staging folder.**
   **RULED: `brainstorm` always — the recommendation below is SUPERSEDED.**
   The authoring engine defaults to `brainstorm`, which is correct for
   `ideation/brainstorm/` and wrong for `ideation/staging/<topic>/` — a
   staging fragment is `staged`, and a `brainstorm`-status file in a staging
   folder will read as a lifecycle error to doc-health and drag the topic's
   completeness. **Recommendation: derive it from the area** — `staged` when
   the area is under `ideation/staging/`, `brainstorm` otherwise, with the
   field editable in the dialog either way. The alternative (always ask) puts
   a lifecycle question in front of a human who is trying to capture a
   thought. Brett decides.
2. **The centre-ring create gesture.**
   **RULED: gesture plus button as recommended — and EXTENDED to every ring
   sector (D6).** Should clicking the bullseye's
   matches-ALL zone open the create dialog, or should the explicit button be
   the only path? **Recommendation: yes to the gesture, plus the button** —
   the gesture is Brett's own from the brainstorm and it is the fastest path
   from a formed thought to a document; the button is what makes it
   discoverable and keyboard-reachable (D6). Brett decides.
3. **A per-document "seed from this document" affordance on `docs` rows.**
   **RULED: deferred to a follow-on change, as recommended.**
   Seeding a new document from ONE row (its topics, its repository context,
   citing it as `Source:`) is an obvious want when the human is reading a
   near-miss document. **Recommendation: defer to a follow-on** — it needs
   row-SELECTION state the `docs` panel does not have (rows are currently
   click-to-open, so a second click target on the row competes with opening
   it), and adding selection state is a bigger change to the panel than
   this one should carry. Brett decides.
4. **Whether the artifact `kind` enum should grow a document-shaped value.**
   **RULED: GROW IT NOW, as `document` — the `other`-in-v1 recommendation
   below is SUPERSEDED.** (The ruled spelling is `document`, not the
   `ideation-document` this question floated: the record already says
   `create-document` in `action` and names the path in `target.document`, so
   the shorter value reads consistently with both and stays usable by any
   future action that produces a document.)
   The create record's one artifact is the created document, which today can
   only be `kind: other` (D12). A named value — `ideation-document` — would
   let an audit consumer filter creates from the enum rather than from the
   action, and would let the schema require it by conditional. **Recommendation:
   ship `other` in v1** and grow the enum only if a consumer actually needs
   the filter; the `action` value already carries the meaning, and enum
   growth is cheap to do later and impossible to undo. Raised at authoring
   from inspecting the schema; Brett decides.
