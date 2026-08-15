---
code_surface: openxFactory (`scripts/ideation_dashboard/web/views/doxbench-editor.js` — the side-by-side textarea+preview pane replaced by an Editor/Preview view-tab pair over one active buffer, and the per-buffer Save/Discard toolbar replaced by one panel-level Save and one panel-level Cancel; `staging-workbench.js` — the context region's `outline` tab and scoped `docs` selection become the buffer selector, and the canvas mounts the active buffer; `doxbench-state.js` — `setActiveBuffer`/`discardBuffer` reused unchanged as the selection and Cancel primitives; `doxbench_turns.py` — the turn record names the buffer path it acted on, generalizing the existing `active_document_path` revalidation; `viewer.js` — the external-editor escape hatch relabelled so the bare word "edit" stops naming two different acts on one surface; and the pinned tests `tests/ideation-dashboard/test_doxbench_view.py`, `test_doxbench_accessibility.py`, `test_doxbench_mutation_boundary.py`, `test_doxbench_turns.py`, `test_staging_workbench.py`, whose DOM, tablist, and buffer-shape assertions this change re-pins honestly rather than deletes)
target_release: none
Status: draft
---

# Proposal: add-doxbench-editing-phase-a

## Why

Brett settled the doxBench editing interaction model on 2026-08-15 and it has
one sentence: **left selects, center chat works, right shows the result.** The
staged topic `doxbench-editing-model` carries that model as seven claims, and
its six open questions were split by Brett's own sequencing ruling the same day:
four were dispositioned `accepted-as-recommended` and feed THIS change; two —
the numbered multi-document tabs and the dirty-tile wheel marker — stay open,
because they are the two that require breaking an enforced runtime invariant.

That split is not an editorial convenience. It is where the engineering risk
actually sits, and reading the code proves it:

**Everything the four dispositioned answers ask for fits on the machinery that
already exists.** Preview reuse is the module's own debounced pipeline
(`schedulePreview`/`renderPreviewNow`, already rendering through the single
`mountSafeMarkdown` path). Cancel is `discardBuffer`, which already restores
`base_content`/`base_hash` and bumps `hash_generation`. Save is the ratified
branch-session substrate — commit-per-gate-action on `draft/<topic>`, with
`open-pr` as the promotion act — which `add-workbench-branch-sessions` settled
on 2026-07-26 and this change does not reopen. Staleness refusal is already
per-buffer by construction: the hash-generation guard is buffer-scoped, not
state-scoped.

**Everything the two open questions ask for breaks an invariant that three
modules enforce at runtime.** `BUFFER_KINDS` is `Object.freeze(["outline",
"document"])` and `validatedDoxBenchState` throws `"doxBench state must contain
exactly outline and document"` on any other key set; `require_outline_and_document`
refuses a turn that does not supply exactly one of each; `SAVE_BUFFER_ORDER` is a
fixed ordered pair whose first element establishes the session ancestry the
second depends on. Numbered per-document tabs mean N path-keyed buffers, which
means all three of those contracts get re-cut at once.

So Phase A is the half of the model that is a **layout and binding change on
proven substrate**, and Phase B is the half that is a **state-model
generalization**. Landing them together would put a UI redesign and a runtime
contract break in one review, and the UI half would inherit the risk of the
other half for no benefit — the redesign is useful on two buffers today.

There is also a finding the topic did not have, because it took reading the
code to see it. The topic's Conflicts section records that "each buffer tab
already carries its own Save button and Discard button" and treats reconciling
that with Claim 6's single right-panel Save/Cancel as unresolved design work.
It is less unresolved than it looked: `save()` in `doxbench-editor.js` already
computes `BUFFER_KINDS.filter((kind) => state.buffers[kind].dirty)` and hands
the whole changed set to the seam in one call. **Save is already panel-level in
SEMANTICS and only per-buffer in PLACEMENT** — two buttons that do the identical
thing. Discard is the genuinely per-buffer one. So Claim 6 is not asking for a
new Save; it is asking the surface to stop drawing the same Save twice. That is
the same call Brett already made on the draft-seed surface on 2026-08-10 ("keep
the tabs, put ONE save on both"), where the save action lives in chrome outside
both panes precisely so its answer is on screen whichever tab the human stands
on. Phase A applies that ruling to the canvas.

## What Changes

Six things, on the existing two buffers, with the two-buffer invariant held
intact and asserted.

1. **The right panel becomes an Editor/Preview view-tab pair, replacing the
   split.** Today `editarea.append(textarea, preview)` puts raw Markdown and its
   rendering side by side inside one pane, per buffer. Phase A makes them two
   tabs over one active buffer: `Editor` (the raw Markdown textarea) and
   `Preview` (a large rendered preview). Same rendering path, same debounce,
   same single `mountSafeMarkdown` sink — a layout change, not a new rendering
   feature.

2. **Preview is the default view tab, and re-renders on every switch into it**
   (Q5, accepted as recommended). Most opens are to read or resume rather than
   to immediately type, and a rendered pane that a human cannot see is exactly
   the pane a debounce is allowed to leave stale — so switching INTO Preview
   flushes it. The existing `flushOne(kind)` already does precisely this.

3. **One Save and one Cancel, on the panel, outside both view tabs** (Q2,
   accepted as recommended). Save = commit-per-gate-action on the session's
   draft branch through the ratified branch-session substrate, with PR-as-save
   (`open-pr`) still the promotion act — unchanged, not re-ratified here. Cancel
   = discard the ACTIVE buffer back to its `base_content`, reusing
   `discardBuffer` unchanged. Save keeps its existing whole-canvas semantics and
   its existing outline-then-document ordering; what goes is the duplicate
   button, not the behavior.

4. **The chat binds to the active left-panel selection, immediately, with no
   confirm step, and every turn record names the buffer path it acted on** (Q4,
   accepted as recommended). Focusing the context region's `outline` tab puts
   the chat in outline-editing context and shows the working unsaved outline on
   the right; selecting a document from the scoped `docs` set binds the chat to
   that document. This generalizes the turn module's existing
   `active_document_path` revalidation rather than adding a second
   context-tracking mechanism beside it.

5. **Staleness refusal is preserved per buffer, and the new panel-level controls
   introduce no way around it** (Q6, accepted as recommended). A turn, an Apply,
   or a Save against a buffer whose settled content identity moved since the
   acting request last observed it refuses — exactly as `applyProposalToBuffer`
   and the turn-assembly revalidation do today. No force-save, no force-cancel,
   no silent merge.

6. **The naming collisions are closed before Phase B can widen them.** "Tab"
   acquires two levels in one surface and "edit" already named two different
   acts. Both are resolved explicitly in `design.md` and asserted in the delta:
   the context region owns SELECTION tabs, the right panel owns VIEW tabs
   (`Editor`/`Preview`), the buffer tablist that used to sit between them is
   retired as a rendered control, and the bare word "edit" on a doxBench surface
   is reserved for in-app editing while the external-editor escape hatch is
   relabelled to name the external editor.

## Impact

- `ideation-dashboard` — MODIFIED: the authoring canvas presents the ACTIVE
  buffer chosen by the context region rather than its own two primary tabs.
  ADDED: the Editor/Preview view-tab pair and its default/refresh rule; the one
  Save and one Cancel that govern the panel; the chat-binding rule and per-turn
  buffer attribution; per-buffer staleness refusal under the new controls; and
  the explicit Phase A two-buffer invariant.
- `scripts/ideation_dashboard/web/views/doxbench-editor.js` — the canvas: view
  tabs replace the buffer tablist and the split pane; one Save and one Cancel
  replace the per-buffer toolbar pair.
- `scripts/ideation_dashboard/web/views/staging-workbench.js` — the context
  region's `outline` tab and scoped `docs` selection drive `setActiveBuffer`.
- `scripts/ideation_dashboard/web/views/doxbench-state.js` — reused unchanged;
  `BUFFER_KINDS` and the exactly-two-keys validator are deliberately untouched.
- `scripts/ideation_dashboard/web/views/doxbench-save.js` — reused unchanged;
  `SAVE_BUFFER_ORDER` stays the ordered pair it is.
- `scripts/ideation_dashboard/doxbench_turns.py` — the turn record names the
  acted-on buffer; `require_outline_and_document` and `PROPOSAL_TARGETS` stay.
- `scripts/ideation_dashboard/web/views/viewer.js` — one relabel.
- `tests/ideation-dashboard/` — the pinned DOM, tablist, accessibility, and
  mutation-boundary assertions are re-pinned to the new structure with the
  reason stated, never deleted to make a refactor pass.
- No contract release: no schema change, no new artifact kind, no new gate verb
  (`target_release: none`).

## Deliberately out of scope

Everything below is Phase B, and each item is out because it requires the
N-buffer generalization Phase A deliberately does not perform:

- **Numbered per-document left-panel tabs** (Claim 1's `1`, `2`, … chips) and
  their overflow policy — staged Q1, still `open`. This is the invariant break:
  `BUFFER_KINDS`, `validatedDoxBenchState`, `require_outline_and_document`,
  `PROPOSAL_TARGETS`, and `SAVE_BUFFER_ORDER` all re-cut together.
- **The docs-wheel `edit` verb** (Claim 3's second verb on the expanded tile).
  It exists to open a document as a new numbered tab, which Phase A has nowhere
  to put. The wheel's expanded tile keeps its single read verb.
- **The dirty-tile wheel marker** (Claim 4) — staged Q3, still `open`. It marks
  "this document has an open unsaved edit", which is only interesting once more
  than one document can be open at a time.
- **N-buffer save ordering.** Phase A keeps the fixed outline-then-document
  order because Phase A keeps exactly two buffers. The rule for "outline first
  as session ancestry, then every document buffer in any order" is Phase B's to
  ratify.
- **Retiring the canvas document picker.** The picker is a second route to the
  same `selectDocument`, and the left-panel selection is the primary one after
  this change. Removing a working keyboard-reachable control is a separate
  argument from adding the selection route beside it, and the dirty-buffer
  switch guard must keep firing on both routes either way.
