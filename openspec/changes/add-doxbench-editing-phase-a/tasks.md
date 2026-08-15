# Tasks: add-doxbench-editing-phase-a

## 1. The contract

- [ ] 1.1 The `ideation-dashboard` delta: one MODIFIED requirement (`doxBench
      scoped view` — the canvas presents the ACTIVE buffer, chosen by the context
      region, and renders no second buffer-selection tablist) and five ADDED
      requirements (Editor/Preview view tabs; one Save and one Cancel; the chat
      binding and per-turn buffer attribution; the panel controls inside the
      per-buffer staleness guard; the view surface expressed over the buffer set
      rather than two literal names).
- [ ] 1.2 `OPENSPEC_TELEMETRY=0 openspec validate add-doxbench-editing-phase-a
      --strict` and `--all --strict` both green.
- [ ] 1.3 `design.md` resolves, in writing, the two things the staging topic left
      open: per-buffer Save/Discard versus panel-level Save/Cancel (Save is
      already whole-canvas and only drawn twice; Cancel is genuinely per-buffer
      and Q2 names the active buffer as its target), and the "tab"/"edit" naming
      collisions.
- [ ] 1.4 README "OpenSpec Records" active block carries the entry.
- [ ] 1.5 Doc-health pre/post diff shows zero NEW findings.

## 2. The canvas: view tabs replace the split

- [ ] 2.1 `DOXBENCH_VIEW_TABS = [{ key: "editor", label: "Editor" },
      { key: "preview", label: "Preview" }]` in `doxbench-editor.js`, rendered as
      one ARIA tablist over the ACTIVE buffer, with `preview` selected at mount.
      The existing WAI-ARIA tablist discipline — roving tabindex, Arrow/Home/End,
      `aria-selected` as the ONLY spelling of selection, arrows consumed so they
      do not scroll the page — carries over unchanged; it was measured and fixed
      once already (CHK007) and MUST NOT be re-lost in the move.
- [ ] 2.2 Retire the rendered buffer tablist. `DOXBENCH_BUFFER_TABS` stops being
      a control: its `Outline`/`Document` labels survive under a name that does
      not claim to be one (they still feed accessible names), and `BUFFER_KINDS`
      in `doxbench-state.js` remains the single enumeration authority, untouched.
- [ ] 2.3 One pane per view tab instead of `editarea.append(textarea, preview)`.
      The textarea and the preview container are still built ONCE at mount and
      mutated afterwards through `textContent`/`.value`/attributes/`classList`;
      the preview container remains the sole exception and is still written only
      through `mountSafeMarkdown`. No new raw-markup sink, anywhere.
- [ ] 2.4 Switching INTO `preview` calls the existing `flushOne` for the active
      buffer before the pane becomes visible; switching into `editor` does not
      flush. `schedulePreview`/`renderPreviewNow`/`previewDelayMs` are reused as
      they are — no second rendering path, no second debounce.
- [ ] 2.5 The existing per-buffer focus/selection/scroll persistence
      (`rememberedFocus`, `rememberedView`, capture-on-hide, re-apply-on-show,
      scroll re-applied LAST so `focus()` cannot win over the human's place)
      keeps working across BOTH the new view-tab switch and the buffer switch.
      A hidden pane still never holds focus, and a pane that never held focus
      still never steals it.
- [ ] 2.6 The canvas mounts the ACTIVE buffer only, reading `state.active_buffer`.
      The view surface reads the buffer set and the active key; it does not
      enumerate `outline` and `document` by name (contract 1.1's fifth ADDED
      requirement).

## 3. Selection moves to the context region

- [ ] 3.1 `staging-workbench.js`: focusing the context region's `outline`
      selection tab sets the active buffer to `outline` through the existing
      `setActiveBuffer`, and the canvas re-mounts on it. No new state authority —
      `doxbench-state.js` stays the only one.
- [ ] 3.2 Selecting a document from the scoped `docs` set continues to route
      through the existing `selectDocument` and now also makes the `document`
      buffer active. The dirty-Document switch guard fires on this route exactly
      as it does on the canvas picker's route — a different DOCUMENT still needs
      Save or Discard first, because that switch replaces buffer content.
- [ ] 3.3 The canvas document picker stays (design D3) and shares one
      `selectDocument` with the left-panel route. Two routes, one refusal
      vocabulary, one guard.
- [ ] 3.4 The context region's own outline pane keeps rendering the material as
      it stands in the source. Two renderings of "the outline" survive on
      purpose: the left says what is stored, the right says what the human has
      unsaved.

## 4. One Save, one Cancel

- [ ] 4.1 One Save control and one Cancel control in canvas chrome OUTSIDE both
      view tabs, so each control and its answer are on screen from either view —
      the shape `staging-workbench.js`'s draft chrome already uses under Brett's
      2026-08-10 "keep the tabs, put ONE save on both" ruling.
- [ ] 4.2 Save calls the SAME zero-argument `save()` it calls today: the dirty
      set over the buffer enumeration, one call to the save seam, `SAVE_BUFFER_ORDER`
      unchanged in `doxbench-save.js`, `adoptSavedBase` still the only way a base
      advances, and the session rekey on a landed session ref unchanged. No Save
      semantics change in this task — only the button count.
- [ ] 4.3 Save's verdict stays PER BUFFER in each buffer's own status region.
      The partial-success case the buffer contract requires (outline committed,
      document refused, reported separately, the committed action never amended)
      MUST remain readable with one button on screen.
- [ ] 4.4 Cancel calls `discardBuffer` on the ACTIVE buffer only, through
      `replaceBuffer`, and states which buffer it reverted. No other buffer moves.
- [ ] 4.5 The in-flight posture carries over intact: `aria-busy`, the stated
      status, both controls withdrawn, a second Save refused with
      `SAVE_BUSY_REASON`, a concurrent edit refused with `EDIT_DURING_SAVE_REASON`
      and stated visibly rather than silently dropped.
- [ ] 4.6 The absent-gate posture carries over intact: with no save seam, Save is
      disabled, `aria-disabled="true"`, and names its reason as VISIBLE text
      beside the control — not only in a hover title. With a seam, that fixed
      reason is GONE rather than restyled.
- [ ] 4.7 Cancel emits the same settled-identity notification the existing
      Discard does (`onIdentitySettled`), so the chat rail re-scores proposal
      currency and stops offering Apply against text the buffer no longer holds.

## 5. Chat binding and turn attribution

- [ ] 5.1 The chat's working context reads `state.active_buffer`. No second
      context-tracking mechanism is introduced beside it.
- [ ] 5.2 A selection change switches the chat's context immediately, with no
      confirm step. The unsaved-edit guard on a DIFFERENT-DOCUMENT switch is
      untouched — it guards content replacement, not context binding.
- [ ] 5.3 `doxbench_turns.py`: the turn record names the exact buffer the turn
      was bound to — repository-relative path, or buffer kind where the buffer
      has no path yet. Additive to the existing request/response shape.
- [ ] 5.4 `revalidate_scope`'s active-path check is PRESERVED, not replaced: a
      declared binding that does not match the supplied buffer still refuses
      before any provider call, leaking no projection or buffer content.
- [ ] 5.5 `require_outline_and_document` and `PROPOSAL_TARGETS` are UNCHANGED.
      Binding says what the chat works on; the turn still carries the buffers the
      grounded-turn contract requires it to carry.

## 6. Staleness, unchanged and proven still there

- [ ] 6.1 The per-buffer hash-generation guard is untouched: `beginBufferEdit` +
      `settleBufferHash` still paired against the LIVE buffer at settle time
      (never the snapshot the edit started from), `hash_generation` still bumped
      by discard, `applyProposalToBuffer` still refusing a moved base.
- [ ] 6.2 A test proves a Save against a buffer whose settled identity moved
      refuses THAT buffer and preserves its text, base, and dirty state — driven
      through the new panel-level Save, so the consolidation is shown not to have
      opened a path around the guard.
- [ ] 6.3 A test proves neither new control exposes a force-save, force-discard,
      refusal bypass, or second write route.

## 7. Naming

- [ ] 7.1 Prose, code, and accessible names use SELECTION tab (context region),
      VIEW tab (`Editor`/`Preview`), and BUFFER (never "tab" again). New class
      prefix `doxbench-viewtab`; the view tablist's `aria-label` names the view
      choice, not "buffers".
- [ ] 7.2 `viewer.js`'s `✎ edit` escape hatch is relabelled to name the EXTERNAL
      editor explicitly, so the bare word "edit" on a doxBench surface stops
      naming two structurally different acts. Behaviour unchanged — it still
      opens the file in the human's own editor and still edits nothing in-app.
- [ ] 7.3 `edit-document` and `edit-apply` are MACHINE KEYS and are NOT renamed,
      here or later.

## 8. Tests: re-pinned honestly, never deleted

- [ ] 8.1 `test_doxbench_view.py` — the assertions that drive
      `DOXBENCH_BUFFER_TABS` as a tablist, and `byClass('doxbench-save')[0]` as
      one of two Save buttons, are re-pinned to the new structure with the reason
      stated in the test. The retired `doxbench-tab-active` guard (no shadow
      class beside `aria-selected`) carries over to the view tabs.
- [ ] 8.2 `test_doxbench_accessibility.py` — the tablist pattern is re-measured
      on the view tabs: roving tabindex, Arrow/Home/End, `aria-selected`, focus
      never trapped, and the AT measurement that produced CHK007 repeated rather
      than assumed.
- [ ] 8.3 `test_doxbench_mutation_boundary.py` — the module still opens no
      network connection, imports nothing dynamically, and writes no raw HTML
      sink. The view-tab split MUST NOT add one.
- [ ] 8.4 `test_doxbench_state.py` — `BUFFER_KINDS` is still exactly
      `["outline", "document"]` and `validatedDoxBenchState` still throws on any
      other key set. Phase A's invariant, asserted rather than assumed.
- [ ] 8.5 `test_doxbench_turns.py` — the turn record names its bound buffer;
      `require_outline_and_document` and `PROPOSAL_TARGETS` still refuse exactly
      what they refuse today.
- [ ] 8.6 `test_doxbench_save.py` — `SAVE_BUFFER_ORDER` and the partial-success
      reporting are unchanged under the single Save button.
- [ ] 8.7 `test_staging_workbench.py` — the pinned module boundaries hold: the
      pure model module stays import-free (the node-harness standalone rule) and
      the renderer boundary still admits no transport call in the model.
- [ ] 8.8 The full `tests/ideation-dashboard` suite green, with the count and
      exit code recorded.

## 9. Records

- [ ] 9.1 The realization evidence recorded in this proposal's front matter at
      the archive gate — merged commit/PR plus the green test run that carries
      this change's own coverage.
- [ ] 9.2 The staging topic `doxbench-editing-model` stays STAGED with Q1 and Q3
      still `open`. Its "Last proposal attempt" slot is NOT filled — that slot
      fills on demote only, per the template. The staging INDEX detail section
      notes that Phase A was raised.
- [ ] 9.3 No contract release: no schema change, no new artifact kind, no new
      gate verb. `target_release: none` verified still true at landing.
