# Tasks: add-doxbench-editing-phase-a

## 1. The contract

- [x] 1.1 The `ideation-dashboard` delta: one MODIFIED requirement (`doxBench
      scoped view` — the canvas presents the ACTIVE buffer, chosen by the context
      region, and renders no second buffer-selection tablist) and five ADDED
      requirements (Editor/Preview view tabs; one Save and one Cancel; the chat
      binding and per-turn buffer attribution; the panel controls inside the
      per-buffer staleness guard; the view surface expressed over the buffer set
      rather than two literal names).
- [x] 1.2 `OPENSPEC_TELEMETRY=0 openspec validate add-doxbench-editing-phase-a
      --strict` and `--all --strict` both green.
- [x] 1.3 `design.md` resolves, in writing, the two things the staging topic left
      open: per-buffer Save/Discard versus panel-level Save/Cancel (Save is
      already whole-canvas and only drawn twice; Cancel is genuinely per-buffer
      and Q2 names the active buffer as its target), and the "tab"/"edit" naming
      collisions.
- [x] 1.4 README "OpenSpec Records" active block carries the entry.
- [x] 1.5 Doc-health pre/post diff shows zero NEW findings.

## 2. The canvas: view tabs replace the split

- [x] 2.1 `DOXBENCH_VIEW_TABS = [{ key: "editor", label: "Editor" },
      { key: "preview", label: "Preview" }]` in `doxbench-editor.js`, rendered as
      one ARIA tablist over the ACTIVE buffer, with `preview` selected at mount.
      The existing WAI-ARIA tablist discipline — roving tabindex, Arrow/Home/End,
      `aria-selected` as the ONLY spelling of selection, arrows consumed so they
      do not scroll the page — carries over unchanged; it was measured and fixed
      once already (CHK007) and MUST NOT be re-lost in the move.
- [x] 2.2 Retire the rendered buffer tablist. `DOXBENCH_BUFFER_TABS` stops being
      a control: its `Outline`/`Document` labels survive under a name that does
      not claim to be one (they still feed accessible names), and `BUFFER_KINDS`
      in `doxbench-state.js` remains the single enumeration authority, untouched.
- [x] 2.3 One pane per view tab instead of `editarea.append(textarea, preview)`.
      The textarea and the preview container are still built ONCE at mount and
      mutated afterwards through `textContent`/`.value`/attributes/`classList`;
      the preview container remains the sole exception and is still written only
      through `mountSafeMarkdown`. No new raw-markup sink, anywhere.
- [x] 2.4 Switching INTO `preview` calls the existing `flushOne` for the active
      buffer before the pane becomes visible; switching into `editor` does not
      flush. `schedulePreview`/`renderPreviewNow`/`previewDelayMs` are reused as
      they are — no second rendering path, no second debounce.
- [x] 2.5 The existing per-buffer focus/selection/scroll persistence
      (`rememberedFocus`, `rememberedView`, capture-on-hide, re-apply-on-show,
      scroll re-applied LAST so `focus()` cannot win over the human's place)
      keeps working across BOTH the new view-tab switch and the buffer switch.
      A hidden pane still never holds focus, and a pane that never held focus
      still never steals it.
- [x] 2.6 The canvas mounts the ACTIVE buffer only, reading `state.active_buffer`.
      The view surface reads the buffer set and the active key; it does not
      enumerate `outline` and `document` by name (contract 1.1's fifth ADDED
      requirement).

## 3. Selection moves to the context region

- [x] 3.1 `staging-workbench.js`: focusing the context region's `outline`
      selection tab sets the active buffer to `outline` through the existing
      `setActiveBuffer`, and the canvas re-mounts on it. No new state authority —
      `doxbench-state.js` stays the only one.
- [x] 3.2 Selecting a document from the scoped `docs` set continues to route
      through the existing `selectDocument` and now also makes the `document`
      buffer active. The dirty-Document switch guard fires on this route exactly
      as it does on the canvas picker's route — a different DOCUMENT still needs
      Save or Discard first, because that switch replaces buffer content.
- [x] 3.3 The canvas document picker stays (design D3) and shares one
      `selectDocument` with the left-panel route. Two routes, one refusal
      vocabulary, one guard.
- [x] 3.4 The context region's own outline pane keeps rendering the material as
      it stands in the source. Two renderings of "the outline" survive on
      purpose: the left says what is stored, the right says what the human has
      unsaved.

## 4. One Save, one Cancel

- [x] 4.1 One Save control and one Cancel control in canvas chrome OUTSIDE both
      view tabs, so each control and its answer are on screen from either view —
      the shape `staging-workbench.js`'s draft chrome already uses under Brett's
      2026-08-10 "keep the tabs, put ONE save on both" ruling.
- [x] 4.2 Save calls the SAME zero-argument `save()` it calls today: the dirty
      set over the buffer enumeration, one call to the save seam, `SAVE_BUFFER_ORDER`
      unchanged in `doxbench-save.js`, `adoptSavedBase` still the only way a base
      advances, and the session rekey on a landed session ref unchanged. No Save
      semantics change in this task — only the button count.
- [x] 4.3 Save's verdict stays PER BUFFER in each buffer's own status region.
      The partial-success case the buffer contract requires (outline committed,
      document refused, reported separately, the committed action never amended)
      MUST remain readable with one button on screen.
- [x] 4.4 Cancel calls `discardBuffer` on the ACTIVE buffer only, through
      `replaceBuffer`, and states which buffer it reverted. No other buffer moves.
- [x] 4.5 The in-flight posture carries over intact: `aria-busy`, the stated
      status, both controls withdrawn, a second Save refused with
      `SAVE_BUSY_REASON`, a concurrent edit refused with `EDIT_DURING_SAVE_REASON`
      and stated visibly rather than silently dropped.
- [x] 4.6 The absent-gate posture carries over intact: with no save seam, Save is
      disabled, `aria-disabled="true"`, and names its reason as VISIBLE text
      beside the control — not only in a hover title. With a seam, that fixed
      reason is GONE rather than restyled.
- [x] 4.7 Cancel emits the same settled-identity notification the existing
      Discard does (`onIdentitySettled`), so the chat rail re-scores proposal
      currency and stops offering Apply against text the buffer no longer holds.

## 5. Chat binding and turn attribution

- [x] 5.1 The chat's working context reads `state.active_buffer`. No second
      context-tracking mechanism is introduced beside it.
- [x] 5.2 A selection change switches the chat's context immediately, with no
      confirm step. The unsaved-edit guard on a DIFFERENT-DOCUMENT switch is
      untouched — it guards content replacement, not context binding.
- [~] 5.3 **DEFERRED — F2 carve-out, Brett's 2026-08-15 ruling on the PR #196
      review.** `doxbench_turns.py` was to name the bound buffer in the turn
      record. It cannot: `xfactory-workbench-chat-turn.schema.yaml` closes the
      request AND the success envelope (`additionalProperties: false`), so a
      record a reader can consult cannot carry the name without a chat-turn
      contract release — which this change forbids (`target_release: none`,
      task 9.3). The attempt (a server-side `PromptEnvelope.bound_buffer`) was
      REMOVED rather than kept: review found it unreadable (nothing serializes,
      persists or renders it) and mis-derivable (the wire carries the document
      path, never which buffer the human selected, so an outline-bound turn
      recorded as document-bound). The obligation rides Phase B, which re-cuts
      the turn machinery and releases that contract anyway; it is recorded on
      the staged topic so Phase B inherits it. What Phase A ships instead is the
      LIVE binding statement on the chat rail — see 5.1/5.2, and the delta's
      amended chat-binding requirement, which states the deferral rather than
      leaving a silent gap.
- [x] 5.4 `revalidate_scope`'s active-path check is PRESERVED, not replaced: a
      declared binding that does not match the supplied buffer still refuses
      before any provider call, leaking no projection or buffer content.
- [x] 5.5 `require_outline_and_document` and `PROPOSAL_TARGETS` are UNCHANGED.
      Binding says what the chat works on; the turn still carries the buffers the
      grounded-turn contract requires it to carry.

## 6. Staleness, unchanged and proven still there

- [x] 6.1 The per-buffer hash-generation guard is untouched: `beginBufferEdit` +
      `settleBufferHash` still paired against the LIVE buffer at settle time
      (never the snapshot the edit started from), `hash_generation` still bumped
      by discard, `applyProposalToBuffer` still refusing a moved base.
- [x] 6.2 A test proves a Save against a buffer whose settled identity moved
      refuses THAT buffer and preserves its text, base, and dirty state — driven
      through the new panel-level Save, so the consolidation is shown not to have
      opened a path around the guard.
- [x] 6.3 A test proves neither new control exposes a force-save, force-discard,
      refusal bypass, or second write route.

## 7. Naming

- [x] 7.1 Prose, code, and accessible names use SELECTION tab (context region),
      VIEW tab (`Editor`/`Preview`), and BUFFER (never "tab" again). New class
      prefix `doxbench-viewtab`; the view tablist's `aria-label` names the view
      choice, not "buffers".
- [x] 7.2 `viewer.js`'s `✎ edit` escape hatch is relabelled to name the EXTERNAL
      editor explicitly, so the bare word "edit" on a doxBench surface stops
      naming two structurally different acts. Behaviour unchanged — it still
      opens the file in the human's own editor and still edits nothing in-app.
- [x] 7.3 `edit-document` and `edit-apply` are MACHINE KEYS and are NOT renamed,
      here or later.

## 8. Tests: re-pinned honestly, never deleted

- [x] 8.1 `test_doxbench_view.py` — the assertions that drive
      `DOXBENCH_BUFFER_TABS` as a tablist, and `byClass('doxbench-save')[0]` as
      one of two Save buttons, are re-pinned to the new structure with the reason
      stated in the test. The retired `doxbench-tab-active` guard (no shadow
      class beside `aria-selected`) carries over to the view tabs.
- [x] 8.2 `test_doxbench_accessibility.py` — the tablist pattern is re-measured
      on the view tabs: roving tabindex, Arrow/Home/End, `aria-selected`, focus
      never trapped, and the AT measurement that produced CHK007 repeated rather
      than assumed.
- [x] 8.3 `test_doxbench_mutation_boundary.py` — the module still opens no
      network connection, imports nothing dynamically, and writes no raw HTML
      sink. The view-tab split MUST NOT add one.
- [x] 8.4 `test_doxbench_state.py` — `BUFFER_KINDS` is still exactly
      `["outline", "document"]` and `validatedDoxBenchState` still throws on any
      other key set. Phase A's invariant, asserted rather than assumed.
- [x] 8.5 `test_doxbench_turns.py` — the turn record names its bound buffer;
      `require_outline_and_document` and `PROPOSAL_TARGETS` still refuse exactly
      what they refuse today.
- [x] 8.6 `test_doxbench_save.py` — `SAVE_BUFFER_ORDER` and the partial-success
      reporting are unchanged under the single Save button.
- [x] 8.7 `test_staging_workbench.py` — the pinned module boundaries hold: the
      pure model module stays import-free (the node-harness standalone rule) and
      the renderer boundary still admits no transport call in the model.
- [x] 8.8 The full `tests/ideation-dashboard` suite green, with the count and
      exit code recorded.

## 9. Records

- [x] 9.1 The realization evidence recorded in this proposal's front matter at
      the archive gate — merged commit/PR plus the green test run that carries
      this change's own coverage.
      Recorded as the block at the head of `proposal.md`. The merged evidence is
      **PR #196 / `6ac42ed`** (2026-08-15), plus this change's own §10
      annotation round at **PR #199 / `224bf22`** and **PR #201 / `96975c1`**
      (both 2026-08-18). Derived from `git log` over this change directory
      rather than from recollection, and one correction fell out of that:
      **PR #207 did NOT realize any part of Phase A** — it realized doxBench
      Phase B's core and touched no file here, so it is named in the block only
      to say so.
      The green run is this change's OWN coverage, the five test files
      `code_surface:` names: **487 passed, exit 0**, with the full
      `tests/ideation-dashboard` suite at **3699 passed / 15 skipped, exit 0**
      re-taken at the gate (task 8.8's number, refreshed — the suite has grown
      with Phase B's slices, which is why the recorded figure moved).
      The block also states plainly what Phase B has since done to this
      surface, so a reader of the archived spec is not misled into thinking the
      two-buffer shape is still what the code does.
- [x] 9.2 The staging topic `doxbench-editing-model` stays STAGED with Q1 and Q3
      still `open`. Its "Last proposal attempt" slot is NOT filled — that slot
      fills on demote only, per the template. The staging INDEX detail section
      notes that Phase A was raised.
- [x] 9.3 No contract release: no schema change, no new artifact kind, no new
      gate verb. `target_release: none` verified still true at landing.

## 10. The annotation round (Brett, 2026-08-15, on the live Phase A canvas)

Two annotations left on the running surface by the ratifying authority, after
Phase A landed. Both are recorded here because each narrows or reverses
something this change decided; `design.md` carries the reasoning.

- [x] 10.1 **The `doxbench-chrome` section is retired** ("we do not need this
      section now that the left panel will let us select the active document").
      The canvas document picker goes with it: D3 kept it for its dirty-buffer
      guard, and the PR #196 review moved that guard — with the refusal sentence
      and the reconcile — into `selectDocument` (F4/F6), which is what made the
      control removable without losing a rule. The context region's docs wheel
      is now the sole human selection route, exactly as Phase A's model always
      said. G-1's outline-only posture survives in the Document buffer's own
      status, where it belonged.
- [x] 10.2 **Save and Cancel move into the view-tab row** ("place the save and
      cancel in line with the tabs"), in their own group inside the row but
      OUTSIDE the `role=tablist` element. The ratified requirement — one of
      each, "outside both view tabs so that each control and its answer are on
      screen whichever view the human is standing on" — is satisfied literally
      by that placement, so no spec text needed amending for it.
- [x] 10.3 **The per-buffer verdict surface survives** in a compact status row
      under the tab row: both regions, still `aria-live`, still per buffer
      (partial saves and stated refusals are load-bearing) — and each line now
      NAMES its buffer visibly, because stacked unlabelled they rendered as
      "no unsaved changesno unsaved changes", two identical sentences a reader
      could not attribute.
- [x] 10.4 **The `h2.doxbench-heading` is retired** ("why do we need this line?
      i do not see what it is adding to our UI"). The region keeps its
      `aria-label` — the house idiom its two sibling regions already use — so
      the accessible name is unchanged while the duplicate visible line goes.
- [x] 10.5 **The one collision with ratified text is AMENDED, not ignored.**
      `doxBench surface identity`'s scenario read "its visible heading and
      accessible surface name MUST use the exact name `doxBench`", and this
      canvas's heading was the surface's only visible statement of it. The
      delta carries that requirement as MODIFIED: the name is required wherever
      the surface names itself and in the ACCESSIBLE name, a region already
      carrying it need not restate it visibly, and any heading that IS rendered
      must still use the exact casing. Directed by Brett's 2026-08-15
      annotation round; the accessible name may never be dropped in exchange.

## Bookkeeping correction (2026-08-22, `archive-record-discrepancies`)

The front matter's `Status:` header read `draft` at the archive. The
ratification flip `document-lifecycle` requires in the same change as the
transition was never made, and the transition is on this change's own record
in four places. `.openspec.yaml` records `approved_by: Brett Heap (dispositions
and phase sequencing relayed in-session)` and `approved_on: 2026-08-15`. §10
above calls Brett "the ratifying authority" and speaks of "the ratified
requirement" and "ratified text" as this change's own. Task 9.1 recorded the
realization evidence at the archive gate under `release-realization`, which
admits only a ratified change. And the archival promoted this change's text,
+5 ADDED and ~2 MODIFIED, into `openspec/specs/ideation-dashboard/spec.md` —
which is precisely what gave Phase B's three Phase-A-relative MODIFIED
requirements something to amend.

Corrected here to `Status: ratified`, with a citation line beside it and this
note rather than silently. The citation is required, not decorative:
`docs/document-lifecycle.md` § Status Claim Rules says a `ratified` header
names its ratification, so a bare flip would replace one defective header with
another. The line added reads:

> `Ratified: 2026-08-15 by Brett Heap — record: this change's .openspec.yaml
> (approved_by, approved_on) …`

**Which spelling, and why.** The corpus carries two, both already accepted by
readers of these proposals, and both counted rather than guessed at:
`Ratified by:` on twenty-nine archived proposals (folder-dated 2026-07-23
through 2026-08-15), `Ratified:` on nine (2026-08-10 and later).

`Ratified by:` is the rule's literal spelling, and fifteen of its twenty-nine
do name their own change id ("Brett's approval of `<change>` on <date>"). The
other fourteen name Brett, a date, and a quoted instruction instead, so the
spelling does not strictly require a change id — but it does require one of
those two, and this change has neither: no approving OpenSpec change exists to
name, and no in-session utterance was written down to quote. What exists is a
record file. `.openspec.yaml` carries `approved_by` and `approved_on`.

The `Ratified:` spelling covers exactly that case. Eight of its nine instances
read `Ratified: <date> by Brett Heap — in-session, verbatim: "…"`, and the
ninth — the closest analogue of all,
`2026-08-22-add-roster-device-admission-surface` — reads
``Ratified: 2026-08-19 — record: `review/ratification-2026-08-19.md` (…)``: a
date plus a pointer to the record that carries the ratification, no change id
and no quote. That is precisely this case with `.openspec.yaml` in the record's
place, so `Ratified:` with a `record:` pointer is what is used. Nothing
invented: both the ratifier and the date are copied out of `.openspec.yaml`
verbatim. Reaching for `Ratified by:` would have meant naming a change that
does not exist, or manufacturing a quotation.

**The precedent, stated with its constraint, and how this extends it.** Brett's
2026-08-10 ruling is that a later change may correct an archived ledger — but
the ruling as recorded at `2026-08-13-align-doxbench-contract-pin-to-publisher`
task 6.2 carries an operative condition that must not be dropped in the
retelling: the correction was made "as an APPEND: the original open-item
sentence is left standing word for word and the resolution follows it, so the
record still says what was true when the tranche closed." This edit cannot
honour that literally. An append on the `Status:` line is mechanically
impossible — `doc_health.corpus.STATUS_RE` is `^Status:\s*(.+?)\s*$`, so it
swallows any trailing annotation into the value, and `Status: draft (corrected
to ratified)` would register as a free-form status rather than as either value.
So this is an in-place overwrite, and it is named as one: an **extension** of
the 2026-08-10 ruling, not an instance of it. The append's purpose is served
another way — the original value is preserved verbatim ("read `draft` at the
archive") in this note and again in
`docs/archive-record-discrepancies.md` B1, so a reader still finds what the
record said before. Whether an overwrite on a single-valued header is inside
the ruling is a question this change answers for itself and flags for Brett; it
is not covered by the words he gave.

The shape borrowed from `split-ideation-book-per-repo` 4.3 is likewise not
identical. That precedent is an **inline suffix on the task line** ("— Discharged
by the archive commit itself (e9a4be6, 2026-08-10); the box was left unchecked
… and corrected here with this note rather than silently"). This is a separate
`##` section appended to the ledger's end. Same spirit — the correction travels
with the change it corrects, and never lands silently — different shape.

This does NOT reopen what `efa42cf` closed, but the distinction is narrower
than a paraphrase makes it sound and is stated here in that commit's own words.
`efa42cf` says: "The archived change is therefore restored **byte-exact to
main's version**." Byte-exact is broader than requirement text, and this edit
is not byte-exact — it rewrites one line of this proposal's front matter and
adds one. The distinction that carries the weight is the *reason* efa42cf
gives, not the scope of the restoration it performed: "An archive amended after
the fact would have claimed Phase A ratified a conditional slot while the spec
its own archival produced said otherwise: a falsified record." What efa42cf
forbids is
an amendment that puts the archive into disagreement with the spec its archival
promoted. A lifecycle header cannot create that disagreement: it promotes no
requirement, and no reader consults it — `ideation_dashboard.generator` derives
a change's status from its folder location and its ratifier from
`.openspec.yaml`, "deliberately NOT the `Ratified by:` proposal header", and
doc-health's corpus does not scan `openspec/` at all. So the extension past
"byte-exact" is deliberate and named as such: the requirement text efa42cf was
protecting is untouched, and the two front-matter lines touched are lifecycle
bookkeeping that no promoted spec can contradict.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas this delta names — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and LEAVE the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
