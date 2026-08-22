# Design: Phase A — One Active Buffer, Two Views, One Save

## Context

Brett's 2026-08-15 model is three clauses: **left selects, center chat works,
right shows the result with Save and Cancel.** The staged topic
`doxbench-editing-model` holds it as seven claims and six open questions; four
of those questions came back `accepted-as-recommended` on the same day and are
the ratified design inputs for this change:

- **Q2 (Save/Cancel semantics)** — "Save = commit-per-gate-action on the
  session's draft branch (the existing branch-session substrate), with PR-as-save
  (`open-pr`) remaining the eventual promotion act exactly as already ratified
  elsewhere; Cancel = discard the active buffer back to its `base_content`,
  reusing `discardBuffer` unchanged."
- **Q4 (chat-context binding)** — "the chat always binds to the ACTIVE
  left-panel selection (the currently active buffer, in the generalized N-buffer
  sense); switching tabs switches the chat's working context immediately (no
  separate 'confirm context switch' step); and every turn record names the exact
  buffer (path) it acted on, generalizing today's `active_document_path`
  revalidation rather than replacing it."
- **Q5 (Editor/Preview default and sync)** — "Preview as the default tab …
  with a live re-render firing on every switch INTO Preview (reusing the existing
  debounced-preview machinery `doxbench-editor.js` already runs for the current
  side-by-side layout) so switching tabs never shows stale rendered content."
- **Q6 (concurrent-edit safety)** — "keep the existing content-hash generation
  guard exactly as designed, applied per buffer regardless of how many buffers
  exist — a turn or a Save attempted against a stale hash … refuses, exactly as
  `applyProposalToBuffer` and the turn-assembly revalidation already do for the
  two-buffer case today."

Q1 (numbered tabs) and Q3 (dirty-tile marker) are still `open`. That is the
phase boundary, and it is a real one: every claim resting on Q1/Q3 needs N
path-keyed buffers, and every claim resting on Q2/Q4/Q5/Q6 does not.

## The one structural decision

**The canvas stops choosing which buffer it shows; the context region chooses,
and the canvas shows the chosen one two ways.**

Today the buffer choice is a tablist INSIDE the canvas
(`DOXBENCH_BUFFER_TABS = [{outline}, {document}]`, a real ARIA tablist with
roving tabindex), and each of its two panes contains a textarea and a preview
side by side plus its own toolbar. That is three selection surfaces stacked in
two panels: the context region picks `docs`/`lens`/`outline`, the canvas picks
`Outline`/`Document`, and inside each canvas pane the human's eye picks between
raw text and rendering.

Phase A collapses the middle one. Selection moves OUT to the context region
(where Brett's model puts it, and where half of it already lives — the ratified
scenario "A document becomes active" already says selecting a `docs` row loads
that document), and the freed level becomes the Editor/Preview pair. After the
change:

| Level | Owner | Question it answers |
|---|---|---|
| Selection tabs (`docs`, `lens`, `outline`) + the scoped docs selection | context region (left) | **which material** am I working on |
| — | *(retired)* | ~~which buffer~~ |
| View tabs (`Editor`, `Preview`) | authoring canvas (right) | **which view** of that material |

The chat sits between them and follows the left, which is exactly Brett's
sentence.

## Reconciling per-buffer Save/Discard with panel-level Save/Cancel

The staging topic flagged this as unresolved: "reconciling 'one Save/Cancel pair
per active document' with the code's current 'one Save/Discard pair per buffer
tab' is design work this topic does not itself resolve." Reading the code
resolves most of it, and the residue splits cleanly in two.

**Save is already panel-level and only LOOKS per-buffer.** `save()` in
`doxbench-editor.js` takes no argument. It computes
`BUFFER_KINDS.filter((kind) => state.buffers[kind].dirty)` and hands the entire
changed set to the save seam in ONE call; the ordering and action choice belong
to `doxbench-save.js` (`SAVE_BUFFER_ORDER`), and the authority belongs to the
gate. Both rendered Save buttons invoke that same zero-argument function. So
there are not two Saves — there is one Save drawn twice, and Claim 6 is asking
for it to be drawn once. Phase A therefore **changes no Save semantics at all**:
same seam, same whole-canvas dirty set, same outline-then-document ordering,
same per-buffer verdict reporting, same in-flight discipline (`aria-busy`, both
controls withdrawn, a second Save and any edit refused rather than queued).
Exactly one control moves.

This is the same call Brett already made on 2026-08-10 for the draft-seed
surface, recorded in `staging-workbench.js`: *"keep the tabs, put ONE save on
both"*, with the action living in chrome outside both panes *"so `save` and the
answer it gets are on screen whichever tab the human is standing on."* The
canvas now follows the surface beside it instead of contradicting it.

**Cancel is genuinely per-buffer, and Q2 says which buffer.** `discardBuffer` is
buffer-scoped by construction — it restores one buffer's `content`/`current_hash`
to its `base_content`/`base_hash`, clears `dirty`, and bumps `hash_generation`
so a late in-flight hash cannot overwrite it. Q2's disposition names the target:
"discard the ACTIVE buffer back to its `base_content`". So panel-level Cancel is
not a new whole-canvas reversal; it is the existing per-buffer discard, aimed by
the same active-buffer selection that aims everything else on the panel. The
asymmetry is deliberate and it is the honest one:

- **Save is broad** because a save is a governed act with an ordering
  dependency between the buffers (the outline's commit establishes the session
  ancestry the document's commit needs). Saving one buffer while leaving the
  other dirty is already an expressible and reported outcome — it just is not a
  SEPARATE BUTTON.
- **Cancel is narrow** because discard destroys unsaved human work and has no
  cross-buffer dependency whatsoever. A single control that silently threw away
  edits in a buffer the human is not currently looking at would be the one
  irreversible surprise on this surface.

Both halves keep their existing statement discipline: the Save verdict is
reported per buffer in each buffer's own status region (nothing about that is
per-BUTTON), and Cancel names the buffer it reverted.

**The panel-level controls introduce no new authority.** Neither Save nor
Cancel gains a force path, a bypass, or a second write route. Save still refuses
an unsettled identity, a stale base hash, and a context-only buffer; Cancel
still persists nothing. This is stated as its own requirement rather than left
implicit, because "one button now does more" is exactly the shape of change that
grows a bypass by accident.

## The naming resolutions

### "tab" — three levels, three nouns

The word already names one thing in the context region (`TAB_DEFS`, keys
`docs`/`lens`/`outline`) and a second thing in the canvas
(`DOXBENCH_BUFFER_TABS`, a real ARIA tablist). Claim 6 adds a third
(`Editor`/`Preview`), nested one level below a buffer selection the left panel
now owns instead. Three "tabs" in two panels is how a design conversation stops
being able to say which one it means.

Resolution — each level gets its own noun, in prose, in accessible names, and in
code:

- **Selection tab** — the context region's `docs` / `lens` / `outline`. Keeps
  the plain word "tab" in visible product copy (it is the one the human thinks
  of as the tab strip), and keeps `TAB_DEFS` unchanged.
- **View tab** — the canvas's `Editor` / `Preview`. New constant
  `DOXBENCH_VIEW_TABS`, new class prefix `doxbench-viewtab`, tablist
  `aria-label` naming the active buffer's view choice rather than a generic
  "buffers".
- **Buffer** — never a "tab" again. `DOXBENCH_BUFFER_TABS` is retired as a
  rendered tablist; the labels it carried (`Outline`, `Document`) survive as
  labels for accessible names, under a name that does not claim to be a control.
  `BUFFER_KINDS` in `doxbench-state.js` remains the single enumeration
  authority, unchanged and still exactly two.

This matters more for Phase B than for Phase A: when numbered per-document tabs
arrive, they are SELECTION tabs, and the vocabulary has to already be able to
say that without a paragraph of explanation.

### "edit" — two acts, one word, on the same surface

`viewer.js` renders `✎ edit`, and that button does not edit anything in the
app — it is the escape hatch that opens the file in the human's OWN local
editor. `edit-document` and `edit-apply` are gate verbs. Claim 3's docs-wheel
`edit` verb (Phase B) means a third thing again: load this document into the
app and chat-edit it in place.

Resolution:

- **`edit-document`, `edit-apply` are MACHINE KEYS** — gate verbs, named in
  records and routes. Never renamed, here or in Phase B. Not part of this
  question.
- **The bare word "edit" in doxBench product copy is reserved for editing that
  happens INSIDE the app.** In Phase A that is the `Editor` view tab, which is
  labelled `Editor` rather than `edit` precisely so it reads as a place, not an
  act.
- **The external-editor escape hatch is relabelled to name the external
  editor** — it stops being the surface's unqualified "edit". One label, changed
  now rather than after Phase B has added a third claimant to the word.

The point is not tidiness. Phase B will put an `edit` verb on a wheel tile a few
hundred pixels from a button that today says `✎ edit` and means something
structurally different. Closing this while there are two claimants is cheaper
than closing it with three.

## The chat-binding rule

Q4, applied to two buffers:

1. **The chat's working context IS the active buffer.** There is no second
   context-tracking mechanism; `state.active_buffer` (maintained by
   `setActiveBuffer`, already persisted and already restored) is the one answer.
2. **Focusing the context region's `outline` selection tab makes the `outline`
   buffer active** — the chat is then editing the outline, and the canvas shows
   the working, unsaved outline. Note the deliberate division of labour this
   creates and does not collapse: the LEFT outline pane keeps rendering the
   material as it stands in the source (a read-only pass-through render), and
   the RIGHT panel shows the working buffer. Two renderings of "the outline"
   that answer different questions — *what is stored* and *what I have* — which
   is exactly Claim 2's "the right panel shows … a new 'unsaved' version of the
   outline."
3. **Selecting a document from the scoped `docs` set makes the `document`
   buffer active** and loads that document — the already-ratified behavior,
   now also stated as a chat-binding fact rather than only a loading fact.
4. **The switch is immediate; there is no confirm step.** Q4 says so explicitly.
   The one thing that DOES interrupt a switch is unchanged and unrelated: the
   existing dirty-Document guard, which fires when switching to a DIFFERENT
   DOCUMENT with unsaved edits, because that switch would replace buffer
   contents. Changing which buffer is ACTIVE replaces nothing and asks nothing.
5. **The binding is STATED where the human is working.** The chat rail names the
   active buffer above the transcript, live, so "what is this conversation
   working on" is answered on the surface the conversation happens on rather
   than inferred from which proposal comes back. The turn still carries BOTH
   buffers as grounding — binding says what the chat is working ON, not what it
   may see. Naming the bound buffer in the durable TURN RECORD as well was the
   original Phase A intent; it is deferred, and the next subsection says why.

## Turn-record naming — deferred (F2 carve-out, Brett 2026-08-15)

This design originally asked for one more thing: that every turn RECORD name
the buffer the turn was bound to, so a transcript read later says "this turn
was working on the outline". Realizing it revealed that Phase A cannot, and the
attempt was withdrawn on Brett's F2 ruling.

**The wire is closed in both directions.** `contracts/schemas/`
`xfactory-workbench-chat-turn.schema.yaml` declares `additionalProperties:
false` on the request AND on the success envelope, with fixed `required` lists.
A turn record a reader can actually consult is a record that crossed that wire,
so naming the bound buffer in one means releasing that contract — and this
change declares `target_release: none` and forbids exactly that (see the
proposal's Impact section, and task 9.3, which re-verifies it at landing).

**A server-side-only field does not substitute for it, on two counts.** The
realization added `PromptEnvelope.bound_buffer`, derived from the request's
`active_document_path`. Review found it (a) unreadable — nothing serializes,
persists or renders it, so no human ever reads the record it was supposed to
improve — and (b) mis-derivable: the wire carries the document path and nothing
about which buffer the human had SELECTED, so a human working on the outline
with a document loaded for grounding was recorded as bound to the document.
Dead code that is also wrong is worse than an honest gap, so it is removed
rather than kept as a placeholder.

**Where the obligation goes.** Phase B reworks the turn machinery already —
`require_outline_and_document`, `PROPOSAL_TARGETS` and the request's buffer
shape all re-cut for N path-keyed buffers, which is itself a chat-turn contract
release. The turn-record naming obligation rides that release rather than
forcing a release of its own for one field. It is recorded on the staged topic
`doxbench-editing-model` so Phase B inherits it as a stated obligation, not as
something a later reader has to rediscover.

What Phase A keeps of Q4 is everything that does not need the wire: the chat's
working context IS `state.active_buffer`, the switch is immediate with no
confirm step, the binding is stated live on the rail, and the existing
active-path revalidation still refuses a declared binding that does not match
the supplied buffer, before any provider call.

## Staleness, unchanged and re-asserted

Q6's disposition is "keep the existing guard exactly as designed, applied per
buffer". Phase A changes no guard. It asserts one thing that would otherwise be
a gap: the NEW panel-level controls are inside the guard, not around it. A Save
invoked from the panel refuses a buffer whose settled identity moved, exactly as
before; a Cancel is a discard and therefore MOVES an identity, so it fires the
same `onIdentitySettled` notification the existing Discard does, keeping the
chat rail's proposal cards from offering Apply against text the buffer no longer
holds. A Save may not be invoked while one is in flight; an edit may not land
while one is in flight. All of this is existing behavior, and the requirement
exists so that a Phase A realization cannot quietly drop it while moving buttons.

## What Phase B gets, and why it has to wait

Phase B is everything that needs N path-keyed buffers:

- **Numbered per-document selection tabs** and their LRU overflow policy (Q1,
  still open).
- **The docs-wheel `edit` verb** — it opens a document as a new numbered tab,
  which does not exist yet.
- **The dirty-tile wheel marker** (Q3, still open) — only meaningful once more
  than one document can be open.
- **The N-buffer generalization itself**: `BUFFER_KINDS` and
  `validatedDoxBenchState`'s exactly-two-keys rule; `require_outline_and_document`
  and `PROPOSAL_TARGETS`; `SAVE_BUFFER_ORDER` and its ancestry dependency, which
  needs a real ordering rule ("outline first as session ancestry, then every
  document buffer in any order") rather than a longer fixed list.

Phase A is deliberately built so that none of that is harder afterwards. The
view-tab pair renders ONE active buffer, so it does not care how many buffers
exist. The Save is already whole-canvas over `BUFFER_KINDS`, so it widens when
`BUFFER_KINDS` widens. Cancel targets the active buffer, which is already a
single value. The chat binds to `state.active_buffer`, which is already a single
key. The one thing Phase A must not do is bake "two" into any NEW surface — and
the delta says so as a requirement, so a realization that hard-codes `outline`
and `document` into the view tabs is refused at review rather than discovered in
Phase B.

## Decisions, stated so they can be argued with

- **D1. Preview default, Editor second.** Q5 ruled Preview default. The pair
  renders in the order `Editor`, `Preview` (Claim 6's own naming order, and
  raw-before-rendered reads correctly as a progression) with `Preview` selected.
  Selection and reading order are different questions and this change answers
  them differently on purpose.
- **D2. Switching INTO Preview flushes; switching into Editor does not.** A
  debounce exists to avoid re-rendering while typing. The pane a human cannot
  see is the one it is safe to leave pending — and the moment it becomes visible
  is exactly when it must not be stale. `flushOne(kind)` already implements this;
  Phase A calls it on the switch.
- **D3. The canvas document picker stays — REVISITED and REVERSED, see the
  annotation round below.** As originally decided: it is a working, labelled,
  keyboard-reachable route to `selectDocument`, and its dirty-buffer guard is
  load-bearing; the left-panel selection becomes the primary route beside it,
  and removing a control is a separate argument from adding a route. That
  argument has since been made and won — the guard is no longer the picker's,
  and Brett retired the control.
- **D4. Phase A holds the two-buffer invariant explicitly rather than
  incidentally.** The delta states it as a requirement so that "we didn't
  generalize the state model" is a checked property of this change and not an
  observation someone makes later.
- **D5. Save's verdict stays per buffer.** One button, still two answers.
  Collapsing the report to a single "saved" would hide the partial-success case
  the ratified buffer contract explicitly requires to be reported separately.

## The annotation round (Brett, 2026-08-15, on the live Phase A canvas)

Phase A shipped, Brett used it, and left two annotations on the running
surface. Both are UI decisions by the ratifying authority, recorded here
because each one reverses or narrows something this design argued for.

### Annotation 1 — the chrome section goes; Save and Cancel move into the tab row

> *"we do not need this section now that the left panel will let us select the
> active document. remove this but place the save and cancel in line with the
> tabs."* — on `div.doxbench-chrome`

**The picker is retired, and D3's reason for keeping it no longer applies.** D3
kept the canvas picker because its dirty-buffer guard was load-bearing — and at
the time that was literally true: the guard, the revert-on-refusal and the
refusal sentence lived partly in the picker's own `change` handler. The PR #196
review moved all three INTO `selectDocument` (F4/F6): one refusal vocabulary
for every route, one guard, and a reconcile that puts the context region's own
selection back on the document the canvas really holds. **That is what made the
control removable without losing a rule**, and it is why the two changes had to
happen in that order. Phase A's model always said *left selects*; the picker
was the transitional second route, and the wheel is now the only one.

The G-1 outline-only posture survives in a better place. It used to be stated
twice — on the picker's label and in the Document buffer's status — and the
status keeps it: it is a fact about the BUFFER, not about a control.

**Save and Cancel move into the view-tab row.** The ratified requirement is
that exactly one of each sits *"outside both view tabs so that each control and
its answer are on screen whichever view the human is standing on"*. A row that
carries the tabs on the left and the two controls on the right satisfies that
literally: the controls are outside both tabpanels and scoped to neither view.
No spec text needed amending for the placement. The controls sit in their own
group INSIDE the row but OUTSIDE the `role=tablist` element — a button inside a
tablist is announced as a tab and joins the roving-tabindex cycle, which is
exactly the two-level confusion the naming resolution exists to prevent.

**Where the verdict surface went.** The per-buffer status regions are
load-bearing: a partial Save reports per buffer by the ratified buffer
contract, and every stated refusal on this surface lands in those same regions.
They move, intact and still `aria-live`, into a compact status row directly
under the tab row — with one change: **each line now names its buffer
visibly.** Stacked unlabelled in the old chrome, a clean canvas rendered "no
unsaved changes" twice with nothing to attribute either sentence to, which is
visible in the annotated screenshot and is precisely the case a partial Save
has to report. The accessible name carried the buffer already; now the visible
text does too.

### Annotation 2 — the canvas heading goes

> *"why do we need this line? i do not see what it is adding to our UI."* — on
> `h2.doxbench-heading`

Nothing an assistive technology did not already get. A `role=region` is
announced by its accessible name on entry, and the `h2` rendered that identical
string a second time, visibly, costing a row of a narrow panel. The heading is
removed and the region keeps its `aria-label` — which is the house idiom, not a
new one: the two sibling regions (`swb-context`, `doxbench-rail`) have always
been named exactly this way, with `aria-label` and no heading. A
visually-hidden `h2` was considered and rejected for the same reason: inside a
region that already has a name, it is simply announced twice.

This DOES collide with ratified text, and the collision is amended rather than
ignored — see the `doxBench surface identity` MODIFIED requirement in this
change's delta, and the note at the end of `tasks.md`.

## Annotation round 2 (Brett, 2026-08-18, on the live canvas and rail)

Two more annotations after round 1 landed. Both say the same thing in different
places: **the surface should be legible from its controls, not from standing
prose.** Neither reverses a decision this design argued for; both remove text it
never argued for.

### Annotation A — the standing status text goes

> *"remove these lines. the UI must be intuitive and not rely on this text to
> inform the user."* — on `div.doxbench-statusbar`, whose captured text read
> `Outline: no unsaved changesDocument: no unsaved changesSave persists only the
> changed buffers, in th…`

Three things stood there, and they are answered three different ways.

**The dirty/clean state becomes CONTROL state.** "No unsaved changes" is
exactly what a disabled Save says, without asking anyone to read a sentence:
Save is now reachable when any buffer is dirty and unreachable when none is,
Cancel when the ACTIVE buffer is dirty. That is a strictly better statement than
the text, because it also tells the human what they can *do* about it. (Save
keeps its other gate untouched: an in-flight Save still withdraws both controls,
and a missing seam still makes Save unreachable for its own stated reason.)

**The "Save persists only the changed buffers…" note is deleted.** It explained
the behaviour the control now demonstrates. Nothing replaces it.

**The per-buffer sentences go SR-ONLY, and this is the load-bearing part.**
Those two regions are not decoration: the ratified buffer contract requires a
PARTIAL Save to be reported per buffer, every stated refusal on this canvas
lands in them, and they are `aria-live`. Deleting them would delete a contract
obligation and an accessibility surface at once. So they stay in the DOM under
`.doxbench-sronly` — the same recipe `.doxchat-announce` uses one region over:
`position: absolute` + `clip-path: inset(50%)`, never `display: none` and never
the `hidden` attribute, either of which would take the live region out of the
accessibility tree along with the text.

**EVENTS get one transient visible line.** A refusal, or a Save that did not
wholly land, is something a sighted human must not miss — and it is an EVENT,
not a state, so it must not stand there afterwards. `.doxbench-eventnote`
appears when there is such a thing to say, names the buffer it is about, and
clears itself after `eventNoteMs` (injectable, like `previewDelayMs`, because a
timer a test cannot pin is a timer nobody can trust). A COMMITTED buffer gets no
event: Save going unreachable and the buffer going clean is the report.

The division is the honest one: **state on the controls, durable detail in the
sr-only regions, events on a transient line.**

### Annotation B — the model selector moves to the send button

> *"add a model selector down next to the send button. make this text the hover
> text for the send button if no model selected."* — on `div.swb-posture-note`,
> reading "chat is unavailable — no approved model is configured; both editors
> remain fully usable."

**What the model machinery actually is** (inspected before implementing, and it
decided the shape of this):

- the server exposes models on `GET /workbench/model-catalog`, gated on the same
  loopback + `session` + resolved-actor verdict the session capability uses;
- the catalog comes from an injected `WorkbenchModelPort` — `serve.py`'s
  `model_port_factory` seam. There is **no CLI flag, no config file and no
  env-var read**: `ideation_dashboard.serve --help` has no model argument;
- with no factory injected — the shipped default, and this local serve's posture
  — the route answers `EMPTY_CATALOG` as a **success**, not an error. That is
  the ratified editor-only posture (FR-025/SC-008);
- **the chat-turn request already carries `model_id`**, in the released
  envelope's own `required` list, and the rail already sends
  `state.selectedModelId` there.

That last point matters: **carrying a per-turn model choice needs no wire change
at all.** The mechanism exists, the selector exists, and `canSend` already
refuses a turn with no model selected. So this annotation is a MOVE, not a new
feature — the selector was three regions above the control its choice governs.

- The selector joins Send in a `doxchat-sendrow`. Same element, same
  `selectModel` binding, same `canSend` authority.
- With nothing selectable it renders **empty and DISABLED** rather than hiding.
  That is the honest shape of this plane: the server answers with a catalog and
  the catalog is empty. (This replaces T104 F5-9's selector-XOR-note trade,
  whose reason — never look live when you are not — is served better by a
  visibly inert control than by an absent one.)
- The unavailability sentence becomes the send button's `title` **and** its
  `aria-describedby` target, so the reason is programmatically associated rather
  than living only in a tooltip a screen reader may never surface. The note
  itself goes sr-only. One selector (`unavailabilityNote`) still chooses WHICH
  sentence — stale token, unreadable catalog, or configured-none — so the
  button's tooltip and the F10-1 vocabulary can never drift.
- The shell's standing posture note now renders only for the PLANE rungs. The
  three CHAT rungs are marked `chat: true` in `presentationPosture`; their
  sentence lives on the send button. The plane rungs (hosted, gate-off, unkeyed,
  source-unavailable) keep the inline note: they explain a canvas that is
  WITHHELD, the rail is not even mounted for most of them, and there is no
  control to hang the sentence on.

**The wire limitation, flagged.** Everything above works within the released
contract because `model_id` is already a field. What does NOT work without a
contract release is anything the envelope has no room for — and the standing
example is the turn-record buffer naming deferred in the F2 carve-out. If a
future round wants per-turn model METADATA beyond the id (a provider hint, a
selected-model echo in the response), that is the same closed-envelope wall, and
it rides Phase B's chat-turn contract release alongside the F2 obligation rather
than forcing a release of its own.

### Spec text

No ratified scenario pins the statusbar's visible text, the posture note's
placement, or the selector's position, so no amendment was needed for either
annotation. The one clause that came close is the gate-absent rule — *"both
controls SHALL state that absence as visible text beside them rather than only
in a hover title"* — and it is **honoured unchanged**: the fixed
`SAVE_UNAVAILABLE_REASON` still renders as visible text beside Save wherever
there is no gate seam. It is the WIRED posture's standing note that was deleted,
which no requirement ever asked for.
