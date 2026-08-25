# Tasks: ratify-doxbench-landed-context-surfaces

The spec delta is already authored (`specs/ideation-dashboard/spec.md`): six
MODIFIED requirements copied whole and edited, one ADDED. What remains is
bookkeeping and one substantive job — proving that every sentence promoted here
describes behaviour that ALREADY SHIPPED, because a doc-only change that quietly
specifies new behaviour is the worst kind of doc-only change.

## 1. Records

- [ ] 1.1 Add the `ratify-doxbench-landed-context-surfaces` entry to the
      README's "OpenSpec Records → Active changes" block, in the neighbours'
      prose form, naming the `:439` contradiction as the reason this change was
      split out and did not wait.
- [ ] 1.2 Confirm `.openspec.yaml` carries the ad-hoc origin (issue #84 plus
      Brett's ruling 0 of 2026-08-25) unchanged from creation — the
      origin-retention gate reads it again at archive
      (`release-realization/spec.md:97-103`).

## 2. Cross-check the promoted text against the shipped surface

Each item below is a claim this delta now makes. Read the code and the test, and
if the text is wrong, FIX THE TEXT.

- [ ] 2.1 The three lens sections are named, always-reachable members of one APG
      tablist with roving tabindex, arrows and Home/End — verify against
      `scripts/ideation_dashboard/web/views/staging-workbench.js:443-506` (the
      tablist construction and its `keydown` handler) and the subtab assertions
      in `tests/ideation-dashboard/test_doxbench_context_panes.py`. Confirm in
      passing that `:488` is the line that makes the sections mutually exclusive,
      which is what `:439`'s old clause forbade. **Record one stale comment**:
      `staging-workbench.js:508` still reads "the SHARED bullseye widget, ABOVE
      the always-present matrix", which the subtabs made false and this change's
      delta supersedes. It is a comment, not behaviour, so it is RECORDED here
      and corrected by the successor change — not edited under a doc-only
      change.
- [ ] 2.2 The docs subpane is a vertical split with the abstract region ABOVE and
      the wheel BELOW — verify against `staging-workbench.js:245-259` and the
      construction-order assertion in `test_doxbench_context_panes.py`.
- [ ] 2.3 The lower half is a single-reel drum over this scope's documents
      flattened into one ordered reel, with the surface's own click and spin
      gestures — verify against `web/views/doc-wheel.js:32-50` and
      `tests/ideation-dashboard/test_doc_wheel.py`.
- [ ] 2.3a **Expected findings, to be RECORDED not fixed.** Two places still
      assert the wheel is DEFERRED, and the wheel shipped:
      `test_doxbench_context_panes.py:19-25` (the module docstring: "The
      mini-wheel is NOT in this slice ... The lower half carries a compact
      document selector until that lands") and
      `test_doxbench_context_panes.py:217-229`
      (`test_the_deferred_wheel_is_recorded_where_the_selector_stands`, which
      asserts the word "wheel" appears NEAR `"swb-docselector"` as a record of
      why the wheel is absent). Both are stale in the same direction. Record
      them as findings for the successor; this change edits no test.
- [ ] 2.4 Selecting a wheel tile makes that document the abstract region's
      subject — verify the wiring at `staging-workbench.js:285` and confirm that
      selection alone creates no buffer, which is the claim the buffer-contract
      delta now makes.
- [ ] 2.5 The abstract RE-PRESENTS only snapshot-carried material and recomputes
      nothing — verify against `web/views/staging-workbench-model.js:1545-1592`
      and the derivation tests in `test_doxbench_context_panes.py`. Confirm the
      promoted text does not disturb the existing docs-row scenario at
      `openspec/specs/ideation-dashboard/spec.md:896-899`.
- [ ] 2.6 The honest-absence sentence matches what the module actually renders,
      verbatim — verify against `staging-workbench-model.js:1578-1581`
      ("this document is referenced but not catalogued in this snapshot, so there
      is nothing derived to show"). Verify the never-a-distillation rule is
      already pinned at `test_doxbench_context_panes.py:144-152`, and verify that
      field OMISSION is what the module does rather than placeholder rendering
      (`staging-workbench-model.js:1545-1592`). There is NO escape hatch here:
      the positive provenance caption was CUT from this change during packet
      review precisely because no caption ships — `renderAbstract`
      (`staging-workbench.js:147-196`) emits none — so nothing in this delta may
      name a caption string the surface does not render.
- [ ] 2.7 The region idiom holds: a named `role=region` with no heading of its
      own, exact `doxBench` casing where the name carries it — verify against
      `tests/ideation-dashboard/test_doxbench_accessibility.py:281-311` and the
      abstract region's own `role`/`aria-label` at
      `staging-workbench.js:248-250`. The region's name today is the STATIC
      string `"selected document"` (`:250`), which is why ruling 6's rename and
      the loaded-document-selector requirement were CUT from this change: they
      need code. Confirm the static string is still what ships, and hand the
      successor two items — the rename, and a PIN for the arrows/Home/End
      scenario this delta now requires, which
      `test_doxbench_context_panes.py:166-175` does not cover (it checks
      `role`, `aria-selected` and `tabIndex` only). Evidence for that scenario
      HERE is a code read at `staging-workbench.js:491-503`.
- [ ] 2.8 Record the cross-check outcome in one paragraph in this file: what was
      confirmed, and every place the delta text was corrected to match the code.

## 3. Validate and archive

- [ ] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate ratify-doxbench-landed-context-surfaces --strict`
      green, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
- [ ] 3.2 Confirm every MODIFIED requirement header matches the canonical spec's
      header text exactly, and that each carries its FULL updated content —
      partial MODIFIED content loses detail at archive time.
- [ ] 3.3 Archive. `code_surface: none`, so this change archives on landing with
      no realization evidence to gather
      (`release-realization/spec.md:23-32`).
- [ ] 3.4 Notify the successor: `add-doxbench-distilled-abstract` authors its
      `:863` delta against the text this change landed, so its delta cannot be
      finalized until this archive is done.
