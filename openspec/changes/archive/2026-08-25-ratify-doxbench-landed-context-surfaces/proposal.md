---
code_surface: none
target_release: none
Status: ratified
Ratified: Brett, 2026-08-25 — ruling 0 of `add-doxbench-distilled-abstract` (SPLIT), recorded as a comment on `opensoft/openxFactory#84`
---

# Proposal: ratify-doxbench-landed-context-surfaces

## Why

Three surfaces shipped into the doxBench context panes on 2026-08-03, and the
spec does not mention any of them. Grep `openspec/specs/ideation-dashboard/spec.md`
for `abstract` or `subtab` and it returns nothing. The surfaces are the lens
restructured into three subtabs (`scripts/ideation_dashboard/web/views/staging-workbench.js:443-506`,
operator annotation `vibe_1785602062606_397p8iakz` quoted at `:443`), the docs
subpane split into an abstract region above a document wheel
(`staging-workbench.js:245-259`, annotation `vibe_1785602331813_gvku9sh2s` at
`:245`, the wheel at `web/views/doc-wheel.js:32-50`), and the deterministic
per-document abstract those two exist to carry
(`web/views/staging-workbench-model.js:1545-1592`).

One of them does worse than go unmentioned: it CONTRADICTS a ratified
requirement. `spec.md:439` requires the bullseye "above the always-present flat
matrix" and says in those words that the matrix "MUST NOT become a toggle-only
alternate"; its scenario at `:441-444` requires that the matrix "MUST still
render, as the always-available view of the same membership". The shipped subtabs
make the three sections MUTUALLY EXCLUSIVE tabpanels —
`staging-workbench.js:488` sets `subPanes.get(name).hidden = !on;` — so exactly
one renders at a time. The requirement has been false about this surface since
the day the subtabs landed.

That is the whole reason this change exists separately. It was carved out of
`add-doxbench-distilled-abstract` by Brett's ruling 0 on 2026-08-25, because that
change is blocked on seven further rulings, a real adapter wired at an
entrypoint, and a non-chat prompt assembler — while this one is doc-only, needs
no code, and every day it waits is a day the spec cannot be trusted about the
surface an operator is looking at.

The reversal is taken honestly rather than papered over. What `:439`'s
simultaneity clause was protecting is ACCESS to the flat matrix, not simultaneous
rendering of it; the annotation that replaced the long scroll with three subtabs
is the newer instruction and the panel is genuinely more readable for it. So the
clause is rewritten around what it protected — each section a named,
always-reachable member of one keyboard-driven tablist — rather than deleted.

## What Changes

- **BREAKING (governance): `spec.md:439`'s simultaneity clause is replaced.** The
  keyword rail, the bullseye and the flat matrix each become a named,
  always-reachable section of ONE APG tablist; no section is reachable only by
  dismissing another; the ordering the old `above` wording expressed is
  discharged by the tablist's declared section order. Scenario `:441-444` is
  rewritten to match, and a keyboard-reachability scenario is added, because the
  guarantee moved from geometry to a tablist and a tablist without arrow keys is
  a worse promise than the one it replaced.
- **The docs subpane's split, its wheel, and the deterministic abstract are
  stated as requirements** on the doxBench scoped view: an abstract region above,
  a single-reel document wheel below, wheel selection setting the abstract's
  SUBJECT, and the abstract RE-PRESENTING only snapshot-carried material.
- **The wheel's relation to the buffer contract is settled** per ruling 6: a
  surface that selects a subject to DESCRIBE is not a second buffer-selection
  surface, so the buffer contract needs no change — and pointing at a document
  neither loads nor keys nor dirties a buffer.
- **The docs verbs follow the presentation change**: read, load-for-editing and
  save attach to the wheel's expanded tile with their contract names, authority
  conditions and reporting obligations unchanged, and a change of presentation
  introduces no fourth verb.
- **ADDED: the deterministic abstract is never captioned as a distillation, and
  states its absences** — the never-a-distillation rule (already pinned by
  `tests/ideation-dashboard/test_doxbench_context_panes.py:144-152`), the stated
  absence rather than an empty box (shipped verbatim at
  `web/views/staging-workbench-model.js:1578-1581`), and field OMISSION rather
  than a placeholder that reads as a value.

**Two clauses were CUT from this change during packet review, because they
describe behaviour that does not ship**, and a doc-only change may not specify
new behaviour under cover of ratifying old:

- The abstract region's accessible name today is the static string
  `"selected document"` (`web/views/staging-workbench.js:250`). Ruling 6's rename
  — the region named for its SUBJECT, and the selector keeping sole claim on the
  selected buffer's name — is therefore a CODE CHANGE. It moves to
  `add-doxbench-distilled-abstract`, which owns `:250`, and the
  loaded-document-selector requirement (`:1827`) is consequently NOT modified
  here at all.
- No provenance caption exists on the surface: `renderAbstract`
  (`staging-workbench.js:147-196`) emits none. The POSITIVE caption "From the
  document's own headers" and its accessible-name clause move to
  `add-doxbench-distilled-abstract`; what stays here is the NEGATIVE rule, which
  is already true and already pinned.

With those cuts this change ratifies what SHIPPED and nothing else. It asks for no
new code and no new behaviour, and it deliberately does not describe the
model-derived abstract, which is the other half of `#84`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `ideation-dashboard`: FIVE requirements MODIFIED — Workbench lens bullseye at
  tile scope (`:438`), doxBench scoped view (`:863`), A docs tile carries read,
  load-for-editing, and save (`:1853`), The canvas view surface is expressed over
  the buffer set (`:1705`), and doxBench editor buffer contract (`:948`) — plus
  ONE ADDED requirement for the never-a-distillation rule and the honest
  absences, which no existing requirement covers. The loaded-document selector
  (`:1827`) was in this list and is NOT modified here; see the cut above.

## Impact

- **Affected specs**: `ideation-dashboard` only.
- **Affected code**: none. Every requirement here describes behaviour that
  already exists in `staging-workbench.js`, `staging-workbench-model.js` and
  `doc-wheel.js`; the cross-check task below verifies that claim rather than
  assuming it.
- **Affected tests**: none changed. Three existing suites are the EVIDENCE this
  change is ratifying shipped behaviour and not writing new behaviour:
  `tests/ideation-dashboard/test_doxbench_context_panes.py`,
  `test_doc_wheel.py`, and `test_doxbench_accessibility.py`. Two of those
  suites carry assertions that are now STALE — they still record the wheel as
  deferred — and the cross-check records them for the successor rather than
  editing them here (§2.3).
- **One scenario has no test pin**: the arrows/Home/End reachability the
  bullseye delta now requires is checked only for roles and roving tabindex
  (`test_doxbench_context_panes.py:166-175`). Its evidence here is a CODE READ
  (`staging-workbench.js:491-503`), and the pin is handed to
  `add-doxbench-distilled-abstract`'s task list (§2.7).
- **Archive gate**: `code_surface: none`, so this change archives on landing
  under `release-realization/spec.md:23-32` — there is no runnable surface to run
  green, because nothing runs.
- **Sequencing**: `add-doxbench-distilled-abstract` declares its own deltas
  RELATIVE TO THIS CHANGE'S OUTCOME (`release-realization/spec.md:64-74`), so this
  change archives first. `add-lens-document-selection` touches
  `web/views/bullseye.js` and `web/styles.css`; no requirement here contradicts
  it, and this change touches no file at all.
- One deliberate overlap to note: `add-doxbench-distilled-abstract` also modifies
  `:863`, narrowing the lens no-new-analysis clause to the bullseye's own
  geometry. Its delta is authored against the text THIS change lands.

## Out of scope

- **The model-derived distilled abstract**, its route, its type, its verifier and
  its captions — all `add-doxbench-distilled-abstract`.
- **Any code change.** If the cross-check finds the shipped behaviour differs
  from the text promoted here, the resolution is to correct THIS proposal's text
  before ratification, not to change the code under a doc-only change.
- **Rendered geometry.** Measurements stay with the operator rig, as
  `test_doxbench_context_panes.py:31-34` records.
