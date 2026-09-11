# Tasks: ratify-doxbench-landed-context-surfaces

The spec delta is already authored (`specs/ideation-dashboard/spec.md`): FIVE
MODIFIED requirements copied whole and edited, one ADDED. What remains is
bookkeeping and one substantive job — proving that every sentence promoted here
describes behaviour that ALREADY SHIPPED, because a doc-only change that quietly
specifies new behaviour is the worst kind of doc-only change.

## 1. Records

- [x] 1.1 Add the `ratify-doxbench-landed-context-surfaces` entry to the
      README's "OpenSpec Records → Active changes" block, in the neighbours'
      prose form, naming the `:439` contradiction as the reason this change was
      split out and did not wait.
      2026-08-25 — VERIFIED present. It landed with the packet itself
      (PR #352, commit `5c547610`) and reads at `README.md:347-393`, naming
      `spec.md:439`'s "toggle-only alternate" wording and
      `staging-workbench.js:488` as the reason for the split. Moved from
      "Active" to "Archived changes" by §3.3. One arithmetic slip is corrected
      in the archived entry rather than carried: the Active entry said "Six
      requirements MODIFIED whole" beside a list of FIVE refs
      (`:438`, `:863`, `:1853`, `:1705`, `:948`); the delta carries five, as
      the proposal's Capabilities block always said.
- [x] 1.2 Confirm `.openspec.yaml` carries the ad-hoc origin (issue #84 plus
      Brett's ruling 0 of 2026-08-25) unchanged from creation — the
      origin-retention gate reads it again at archive
      (`release-realization/spec.md:97-103`).
      2026-08-25 — VERIFIED UNMUTATED. `git log` reports exactly ONE commit
      touching the file (`5c547610`, its creation) and `git status` is clean for
      the change directory, so `openxFactory:adhoc:2026-08-25-ratify-doxbench-landed-context-surfaces`,
      its stated reason, `approved_by: Brett` and `approved_on: 2026-08-25` are
      the bytes written at creation. The ad-hoc arm of the gate applies: no
      support bundle exists, and the reason and approval provenance are retained.

## 2. Cross-check the promoted text against the shipped surface

Each item below is a claim this delta now makes. Read the code and the test, and
if the text is wrong, FIX THE TEXT.

- [x] 2.1 The three lens sections are named, always-reachable members of one APG
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
      2026-08-25 — CONFIRMED; delta text unchanged. `:457-459` builds
      `div.swb-subtabs` with `role="tablist"` and `aria-label="lens sections"`;
      `SECTIONS` (`:461-465`) is exactly the keyword rail, the bullseye and the
      matrix, each given a labelled `role="tab"` button (`:469-474`) and a
      labelled `role="tabpanel"` host (`:475-479`) — so every section is NAMED
      and none is reachable only by dismissing another. `showSection` sets the
      roving tabindex at `:486` (`btn.tabIndex = on ? 0 : -1`), and the `keydown`
      handler at `:491-503` serves ArrowRight/ArrowDown, ArrowLeft/ArrowUp, Home
      and End, calls `preventDefault`, and moves focus to the new tab — which is
      the whole of the keyboard scenario this delta adds. `:488` is confirmed as
      the mutual-exclusion line: `subPanes.get(name).hidden = !on;`, exactly what
      `:439`'s old clause forbade in words. RECORDED, NOT FIXED: the stale
      comment at `:508` ("the SHARED bullseye widget, ABOVE the always-present
      matrix (design D1/D3)") still stands; it is handed to
      `add-doxbench-distilled-abstract` tasks §2.5.
- [x] 2.2 The docs subpane is a vertical split with the abstract region ABOVE and
      the wheel BELOW — verify against `staging-workbench.js:245-259` and the
      construction-order assertion in `test_doxbench_context_panes.py`.
      2026-08-25 — CONFIRMED; delta text unchanged. `:245-246` names the
      annotation and the arrangement, `:247-250` builds `div.swb-docsplit`
      holding `div.swb-docabstract`, `:251-257` builds the wheel host
      `div.swb-docselector` under a comment recording the wheel as DELIVERED
      2026-08-03, and `:258` appends them in order —
      `split.append(abstract, selector)`. `test_doxbench_context_panes.py:203-214`
      pins both halves of the claim: the `.swb-docsplit` CSS rule contains
      `column`, and the abstract's construction index is asserted LOWER than the
      selector's.
- [x] 2.3 The lower half is a single-reel drum over this scope's documents
      flattened into one ordered reel, with the surface's own click and spin
      gestures — verify against `web/views/doc-wheel.js:32-50` and
      `tests/ideation-dashboard/test_doc_wheel.py`.
      2026-08-25 — CONFIRMED; delta text unchanged. `doc-wheel.js:49-53`
      declares `DOC_WHEEL = { drumF: 0.4, tileH: 56, key: "docs" }` with the
      comment "This drum has one column, so one constant name is the whole
      namespace" (`:47-48`), and the module header (`:8-44`) states why it is
      still "the same wheel": the projection is the SHARED `drumProject`, the
      click gesture the SHARED `nextExpanded` reducer, focusability the SHARED
      `inReelWindow` predicate — all imported at `:41-44`. The SPIN is real
      rather than nominal: `onWheelEvent` (`:445-447`) is bound
      `passive:false` at `:451`, and `nextExpanded(expanded, {type:"spin"})`
      (`:211`) collapses an expansion on it. The FLATTENING is
      `docWheelEntries` (`staging-workbench-model.js:1607-1615`), which walks
      `scope.sections` and pushes every `section.documents` row into ONE ordered
      list; `docWheelEntry` (`:1620-1644`) carries the section LABEL and its
      `inherited` flag onto the tile, so "every separately labelled section
      flattened into one ordered reel" loses no labelling. `test_doc_wheel.py`
      pins the radius (`:152`), one and only one projection definition (`:204`),
      second-click expansion through the same locked reducer (`:226`),
      off-window tiles not focusable (`:240`), every document in the scope
      carried (`:291`), and the section label surviving the flatten (`:299`).
- [x] 2.3a **Expected findings, to be RECORDED not fixed.** Two places still
      assert the wheel is DEFERRED, and the wheel shipped:
      `test_doxbench_context_panes.py:19-25` (the module docstring: "The
      mini-wheel is NOT in this slice ... The lower half carries a compact
      document selector until that lands") and
      `test_doxbench_context_panes.py:217-229`
      (`test_the_deferred_wheel_is_recorded_where_the_selector_stands`, which
      asserts the word "wheel" appears NEAR `"swb-docselector"` as a record of
      why the wheel is absent). Both are stale in the same direction. Record
      them as findings for the successor; this change edits no test.
      2026-08-25 — BOTH FOUND EXACTLY AS PREDICTED, BOTH RECORDED, NEITHER
      EDITED. The docstring at `:19-25` still reads "SCOPE RULED BY BRETT,
      2026-08-03. The mini-wheel is NOT in this slice … The lower half carries a
      compact document selector until that lands". The assertion at `:217-229`
      still describes the selector as an interim placeholder and demands the
      word "wheel" within the 1600 characters preceding `"swb-docselector"`; it
      is GREEN today only by accident, because what now sits in that window is
      `staging-workbench.js:251-256`, the comment announcing the wheel
      DELIVERED. The contradicting pin is already on main:
      `test_doc_wheel.py:393-400`, `test_the_deferral_note_is_gone`. Handed to
      `add-doxbench-distilled-abstract` tasks §2.5.
- [x] 2.4 Selecting a wheel tile makes that document the abstract region's
      subject — verify the wiring at `staging-workbench.js:285` and confirm that
      selection alone creates no buffer, which is the claim the buffer-contract
      delta now makes.
      2026-08-25 — CONFIRMED; delta text unchanged. The wheel is mounted at
      `:278` (`renderDocWheel(selector, entries, {…})`) and its `onSelect`
      (`:279-288`) calls `renderAbstract(abstract, entry ? entry.row.doc : null)`
      at `:285` and then does nothing but return past the `seeded` and
      `reconciling` guards. Its own comment states the rule in the delta's
      words — "The abstract above, and NOTHING else: a selection is not a
      binding route under Phase B" (`:280-281`) — and the Phase A `onBind` route
      that DID bind a buffer on selection is recorded as retired at `:197-199`.
      Nothing in the callback loads, keys, seeds or dirties a buffer, so the
      buffer-contract delta's "a document pointed at is not a document loaded"
      describes the shipped surface.
- [x] 2.5 The abstract RE-PRESENTS only snapshot-carried material and recomputes
      nothing — verify against `web/views/staging-workbench-model.js:1545-1592`
      and the derivation tests in `test_doxbench_context_panes.py`. Confirm the
      promoted text does not disturb the existing docs-row scenario at
      `openspec/specs/ideation-dashboard/spec.md:896-899`.
      2026-08-25 — CONFIRMED; delta text unchanged. `documentAbstract`
      (`:1545-1592`) is declared and is in fact PURE — "reads one document
      object, touches no DOM, fetches nothing" (`:1544`) — and every field it
      returns is READ rather than derived: `summary` is `doc.summary`, which
      `scripts/ideation_dashboard/generator.py:458` fills from the document's own
      `Summary:` header (`_header_value(d.text, "Summary")`), so the delta's
      "its own `Summary:` header" is literally true; `topics` is `doc.topics`
      copied; `stage` and `kind` pass straight through; `lands` is a flatten of
      `doc.destinations`; `score` is `completeness.score`; `signals` is the FIVE
      named entries `structure`, `length`, `open_markers`, `keyword_coverage`,
      `link_degree` (`:1551-1552`) copied with their own `value`/`count`. There
      is no arithmetic anywhere in the function. One thing the enumeration does
      not name and the region does render is the document's own TITLE
      (`path.split("/").pop()`, `:1548`) — checked and accepted rather than
      edited in, because a filename is snapshot-carried material by any reading
      and the operative prohibition ("MUST NOT compute, adjust, or re-weight")
      is untouched by it. The existing docs-row scenario at canon `:896-899` is
      carried into this delta byte-for-byte and is undisturbed: the new
      abstract-region scenario states the same obligation for a SECOND surface
      rather than replacing it, and the per-document completeness bar the flat
      list drew now rides on each wheel tile (`docWheelEntry`, `:1633-1641`;
      `doc-wheel.js:165-172`) as well as in the abstract.
- [x] 2.6 The honest-absence sentence matches what the module actually renders,
      verbatim — verify against `staging-workbench-model.js:1578-1581`
      ("this document is referenced but not catalogued in this snapshot, so
      there is nothing derived to show"). Verify the never-a-distillation rule is
      already pinned at `test_doxbench_context_panes.py:144-152`, and verify that
      field OMISSION is what the module does rather than placeholder rendering
      (`staging-workbench-model.js:1545-1592`). There is NO escape hatch here:
      the positive provenance caption was CUT from this change during packet
      review precisely because no caption ships — `renderAbstract`
      (`staging-workbench.js:147-196`) emits none — so nothing in this delta may
      name a caption string the surface does not render.
      2026-08-25 — CONFIRMED on all four counts; delta text unchanged. The
      stated absence is verbatim at `:1578-1581` — "this document is referenced
      but not catalogued in this snapshot, so there is nothing derived to show"
      — guarded by `!summary && !topics.length && !signals.length &&
      !lands.length`, i.e. exactly the "no derived material AT ALL" case the
      ADDED requirement names, and `renderAbstract:158-161` prints it as prose
      instead of leaving an empty box. FIELD OMISSION is what the module does:
      every block in `renderAbstract` (`:155-194`) sits behind an `if` on its own
      field — `if (meta)`, `if (model.summary)`, `if (model.lands.length)`,
      `if (model.topics.length)`, `if (model.signals.length)` — so an absent
      field renders NOTHING, and no placeholder string exists anywhere in the
      function. The never-a-distillation rule is pinned at
      `test_doxbench_context_panes.py:144-152`, a whole-file sweep banning
      "distilled", "ai summary" and "ai-generated". And the cut holds:
      `renderAbstract` emits no caption of any kind — the only strings it writes
      are the title, the `stage · kind` meta, the absence note, the labels
      "feeds", "topics" and "signals · score N", and the field values — so
      nothing in this delta names a caption string the surface does not render.
- [x] 2.7 The region idiom holds: a named `role=region` with no heading of its
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
      2026-08-25 — CONFIRMED, and the static string is still what ships.
      `:248-250` builds `div.swb-docabstract` with `role="region"` and the
      LITERAL `aria-label="selected document"`, constructing no heading of its
      own — the house idiom `test_doxbench_accessibility.py:281-311` pins on the
      canvas (`role=region` + `aria-label`, `el("h2"` absent, `canvasLabel =
      "doxBench"` casing exact) and names on the siblings at `:309-310`
      ("docs and lens context", "doxBench chat rail"). The name does NOT track
      the wheel's selection, which is exactly why ruling 6's rename and the
      loaded-document-selector requirement (`:1827`) were cut. The keyboard
      scenario's evidence here is the CODE READ at `staging-workbench.js:491-503`
      recorded in §2.1; `test_doxbench_context_panes.py:166-175` searches the
      first 4000 characters of the subtab strip for `role="tablist"`,
      `role="tab"`, `aria-selected` and `tabIndex` only, so arrows/Home/End have
      NO pin. Both successor items are already recorded in
      `add-doxbench-distilled-abstract`: the rename at its §7.10 (the change
      that owns `:250`), the missing pin at its §2.5.
- [x] 2.8 Record the cross-check outcome in one paragraph in this file: what was
      confirmed, and every place the delta text was corrected to match the code.
      2026-08-25 — CROSS-CHECK OUTCOME: **every sentence promoted by this delta
      describes behaviour that already ships, and NOT ONE WORD of the delta
      needed correcting.** All seven claims were checked against the source and
      against the suites that pin it: the three-section APG tablist with roving
      tabindex, arrows and Home/End (`staging-workbench.js:457-503`); the
      vertical split with the abstract above and the wheel below (`:245-259`,
      pinned at `test_doxbench_context_panes.py:203-214`); the single-reel drum
      over one flattened, still-labelled reel with the shared projection, the
      shared locked click reducer and a real spin (`doc-wheel.js:41-53`,
      `:211`, `:445-451`; `staging-workbench-model.js:1607-1644`; pinned across
      `test_doc_wheel.py`); selection driving the abstract's SUBJECT and nothing
      else (`:278-288`, comment at `:280-281`, the Phase A binding route recorded
      as retired at `:197-199`); a pure re-presentation that computes nothing,
      with `summary` traced back to the document's own `Summary:` header through
      `generator.py:458`; the honest-absence sentence verbatim at
      `staging-workbench-model.js:1578-1581` with true field OMISSION in
      `renderAbstract`; and the `role=region`/`aria-label` idiom with the name
      still the static `"selected document"`. TEXT CORRECTIONS MADE: **none** —
      the two clauses that would have needed them were already CUT during packet
      review (the subject-named region and the positive provenance caption), and
      re-reading `renderAbstract` confirmed the cut was right, since the function
      emits no caption at all. ONE nuance was checked and deliberately left
      as-authored rather than edited: the `:863` enumeration of what the abstract
      re-presents does not name the document's own filename title, which the
      region does render (`:1548`, `:155`) — accepted because a filename is
      snapshot-carried by any reading and the operative "MUST NOT compute,
      adjust, or re-weight" clause is unaffected, and recorded here so the next
      reader does not have to re-derive the judgement. THREE FINDINGS RECORDED
      RATHER THAN FIXED, all exactly as this change's packet predicted, and all
      already carried on `add-doxbench-distilled-abstract`'s task list: the stale
      comment at `staging-workbench.js:508` (§2.5 there), the stale wheel-is-
      deferred module docstring at `test_doxbench_context_panes.py:19-25` and the
      stale `test_the_deferred_wheel_is_recorded_where_the_selector_stands` at
      `:217-229` (§2.5 there), and the missing arrows/Home/End pin (§2.5 there)
      with the region rename (§7.10 there). No test and no JavaScript was touched
      by this change, which is what "doc-only" was supposed to mean.

## 3. Validate and archive

- [x] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate ratify-doxbench-landed-context-surfaces --strict`
      green, and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
      2026-08-25 — both green pre-archive: the change reported "is valid", and
      `--all --strict` reported **79 passed, 0 failed (79 items)**. Re-run
      post-archive in §3.3.
- [x] 3.2 Confirm every MODIFIED requirement header matches the canonical spec's
      header text exactly, and that each carries its FULL updated content —
      partial MODIFIED content loses detail at archive time.
      2026-08-25 — VERIFIED MECHANICALLY, not by eye. All five MODIFIED headings
      resolve to a canonical requirement by exact string match — `Workbench lens
      bullseye at tile scope` (canon `:438`), `doxBench scoped view` (`:863`),
      `A docs tile carries read, load-for-editing, and save` (`:1853`), `The
      canvas view surface is expressed over the buffer set, not over two names`
      (`:1705`), `doxBench editor buffer contract` (`:948`) — and every canon
      line of every block is present in the delta except the lines this change
      INTENDS to change. NOT ONE SCENARIO HEADING IS LOST from any of the five.
      Four of the five blocks are PURE ADDITIONS at the word level: `:863`,
      `:1853`, `:1705` and `:948` each keep their whole promoted paragraph
      verbatim and append one new clause plus one-to-three new scenarios. The
      fifth, `:438`, carries the only DELETION in the change and it is the
      intended one — "above the always-present flat matrix," is struck from the
      opening sentence, "always present" becomes "a first-class always-reachable
      section", "become a toggle-only alternate." becomes "be demoted to an
      opt-in alternate of the bullseye" plus the supersession sentence, and the
      two simultaneity bullets of the first scenario are rewritten to the
      tablist form. Net scenarios: `:438` 4→5, `:863` 13→16, `:1853` 5→6,
      `:1705` 2→3, `:948` 9→10, plus 3 on the ADDED requirement = **+10**.
- [x] 3.3 Archive. `code_surface: none`, so this change archives on landing with
      no realization evidence to gather
      (`release-realization/spec.md:23-32`).
      2026-08-25 — ARCHIVED to
      `openspec/changes/archive/2026-08-25-ratify-doxbench-landed-context-surfaces/`
      by `openspec archive ratify-doxbench-landed-context-surfaces --yes`, which
      reported `+ 1 added, ~ 5 modified` and applied the deltas into
      `openspec/specs/ideation-dashboard/spec.md`. Origin-retention gate:
      satisfied by §1.2; realization gate: `code_surface: none`, so
      `release-realization/spec.md:15-16` is the applicable arm and there is no
      runnable surface to run green. PROMOTION VERIFIED FOUR WAYS. (a) The
      promoted text is in canon: `subtab` 0 → 1 hits, `abstract` 0 → 20,
      `wheel` 14 → 26, `tablist` 1 → 10. (b) The falsified clause is GONE —
      `above the always-present flat matrix`, `toggle-only alternate` and
      `always-available view of the same membership` each return ZERO hits,
      where each returned one before. (c) Nothing unrelated moved: of the 87
      requirements in canon before the archive, **82 bodies are byte-identical
      after it**, the five that changed are exactly the five MODIFIED, one
      requirement was added, NONE was removed, and the requirement order is
      unchanged. (d) No scenario was lost: **376 → 386**, which is the +10 §3.2
      predicted (`:438` +1, `:863` +3, `:1853` +1, `:1705` +1, `:948` +1, ADDED
      +3), with zero scenario headings dropped from any requirement; canon grew
      2032 → 2083 lines. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`
      is green after the archive at **78 passed, 0 failed** (79 before, one
      fewer item because the archived change is no longer validated), and the
      archived `specs/ideation-dashboard/spec.md` is byte-identical to the
      authored delta — the record of what was promoted stays in the packet.
      README moved from "Active changes" to "Archived changes" in the same
      commit.
- [x] 3.4 Notify the successor: `add-doxbench-distilled-abstract` authors its
      `:863` delta against the text this change landed, so its delta cannot be
      finalized until this archive is done.
      2026-08-25 — CHECKED AGAINST THE NEW CANON, NO FIX NEEDED.
      `add-doxbench-distilled-abstract`'s MODIFIED `doxBench scoped view` block
      equals (new canon + its own additions): every one of the 16 scenario
      headings now in canon is present in B's block, every canon bullet is
      present, and its 63 canon lines are all carried. B diverges in exactly the
      three places its own proposal declares — it strikes "a new analysis," from
      the closing "Neither presentation SHALL introduce…" sentence, appends the
      two-sentence paragraph narrowing the no-new-ANALYSIS clause to the
      bullseye's geometry and the completeness signals, and adds two scenarios
      ("A model-derived artifact is admitted beside the snapshot's own", "The
      no-new-analysis clause is read against the bullseye"), taking it to 18.
      Nothing this archive landed is missing from it, so its `:863` delta needed
      no re-authoring; a confirming note is recorded on that change's §1.1, the
      box that tracks this fold. Its §1.1 gate — "confirm
      `ratify-doxbench-landed-context-surfaces` is archived" — is now satisfied,
      and its §2.5 and §7.10 carry the four findings this cross-check recorded.

## Bookkeeping correction (2026-09-11, `split-opendox-two-layer-product` § 5.9) — carry-forward

Edited (bookkeeping): 2026-09-11 by split-opendox-two-layer-product — carry-forward annotation

This packet's `specs/ideation-dashboard/spec.md` delta stays the record, unedited and unaugmented by anything below. The `ideation-dashboard` capability's artifacts — the `scripts/ideation_dashboard/` tree, `web/`, `tests/ideation-dashboard/`, the packaged examples under `examples/ideation-dashboard/`, the five dashboard governance docs, and the five dashboard contract schemas — were SHED from `openxFactory` by `split-opendox-two-layer-product` § 5.2, `opensoft/openxFactory` PR #940 → `cc4ae9d35b2dbd56743c8c19699fd685d4e49343` (merged 2026-09-11). They are now consumed at a pin from the `openDox`/`openXdox` legs per `docs/opendox-carve-manifest.yaml` (destinations `opendox_spec`, `opendox_code`, `openxdox_spec`, `openxdox_code`; `contracts/opendox-pin.yaml`, `contracts/openxdox-pin.yaml`). The five contract schemas associated with the `ideation-dashboard` capability — `gate-action-record`, `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog` — were DEPRECATED at `contract-v3.7` (`opensoft/openxFactory` PR #970 → `45bd9ee250ad1125f9227ad511bee0fec2b16306`, tag `ec3c17292c6dc2ca6004d158d6cc26bf5e6523e2`, merged 2026-09-11) and are slated for removal from the bundle at `contract-v4.0` (§ 5.7; cut PR `TBD-CUT-PR`, a placeholder the landing lane fills in when the cut lands). Ruled by Brett Heap, 2026-09-11 20:27Z, session `openXfactory-4 (5)`, on `opensoft/openxFactory`#656 comment `5640246046` (§ 5.9), realizing `split-opendox-two-layer-product` `tasks.md` § 5.9 — "ANNOTATE the 30 archived changes carrying an `ideation-dashboard` delta with the carry-forward." Nothing this packet asserts is changed by this annotation; immutable records are annotated, never edited into agreement.
