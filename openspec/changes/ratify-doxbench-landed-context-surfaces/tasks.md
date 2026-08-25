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
      which is what `:439`'s old clause forbade.
- [ ] 2.2 The docs subpane is a vertical split with the abstract region ABOVE and
      the wheel BELOW — verify against `staging-workbench.js:245-259` and the
      construction-order assertion in `test_doxbench_context_panes.py`.
- [ ] 2.3 The lower half is a single-reel drum over this scope's documents
      flattened into one ordered reel, with the surface's own click and spin
      gestures — verify against `web/views/doc-wheel.js:32-50` and
      `tests/ideation-dashboard/test_doc_wheel.py`.
- [ ] 2.4 Selecting a wheel tile makes that document the abstract region's
      subject — verify the wiring at `staging-workbench.js:285` and confirm that
      selection alone creates no buffer, which is the claim the buffer-contract
      delta now makes.
- [ ] 2.5 The abstract RE-PRESENTS only snapshot-carried material and recomputes
      nothing — verify against `web/views/staging-workbench-model.js:1545-1592`
      and the derivation tests in `test_doxbench_context_panes.py`. Confirm the
      promoted text does not disturb the existing docs-row scenario at
      `openspec/specs/ideation-dashboard/spec.md:896-899`.
- [ ] 2.6 The honest-absence sentence and the "From the document's own headers"
      caption match what the module actually renders — verify against
      `staging-workbench-model.js:1575-1581`. If the shipped caption string
      differs from the one this delta names, the delta adopts the shipped string.
- [ ] 2.7 The region idiom holds: a named `role=region` with no heading of its
      own, exact `doxBench` casing where the name carries it — verify against
      `tests/ideation-dashboard/test_doxbench_accessibility.py:281-311` and the
      abstract region's own `role`/`aria-label` at
      `staging-workbench.js:248-250`. This is also where ruling 6's rename lands:
      confirm the region is NOT named "selected document" once that rename is
      made, or record the rename as the one code follow-up this change hands to
      its successor.
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
