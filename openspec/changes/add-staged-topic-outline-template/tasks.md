# Tasks: add-staged-topic-outline-template

Sequenced in PARALLEL with `doxbench-editing-model` Phase A (Brett, 2026-08-15).
The decision half is done — all five questions accepted as recommended — so what
remains is the contract and the surface.

## 1. The template contract

- [x] 1.1 Write the canonical template into `docs/document-lifecycle.md`: the
      three required sections, the four-sub-field open-question shape, the
      `Added-by:` provenance rule, and the `xspec:` marker wrapping. The fenced
      skeleton already exists in the staging fragment — carry it verbatim rather
      than re-deriving it, so the ratified text and the drafted text cannot drift.
      Landed as `## The Staged-Topic Outline Template`. The 99-line skeleton was
      EXTRACTED programmatically rather than retyped, and the carry is proven
      byte-identical by sha256 rather than asserted. Also superseded the marker
      bullet that said staged fragments "need no inline markers" — true for
      QUEUING, no longer the whole story now that conforming fragments wrap
      proposal-element sections in the same ratified `xspec:` grammar.
- [x] 1.2 State the round-trip-on-demote rule as a testable property, not a
      description: a demoted fragment's proposal-element sections carry the last
      attempted `proposal.md` text, the change id, both dates, and the reason.
      Written as "the load-bearing rule", stating the testable question in the
      prose itself — does a demoted fragment's slot carry the prior change's
      real text — so the reason it is a requirement and not a convention is on
      the page rather than only in the proposal.
- [x] 1.3 Record Q1's ruling where the next reader will meet it — `primaryFragmentPath`
      is unchanged and the one-path rule is preserved, not extended. The function's
      own docstring is the right place; anyone proposing a second candidate file
      will read it there first.
      States that the `outline.md` alternative was PUT AND DECLINED, that a
      future second candidate is a reversal needing its own ruling rather than a
      patch to the list, and that doc-health's `_primary_fragment` mirrors this
      selection — change both together or neither.

## 2. Doc-health conformance nudge

- [x] 2.1 A warning-tier check: a staged topic's primary fragment carries the
      three required sections and every open question carries four sub-fields.
      Landed as doc-health family `staged-topic-template`. `_primary_fragment`
      mirrors `primaryFragmentPath` in wheel-model.js exactly — exact
      `<topic>.md` first, else shallowest markdown, path-only and never
      content-sniffed — so the checker and the wheel can never disagree about
      which file a topic's outline IS.
- [x] 2.2 REQUIRED for topics staged after ratification, OPT-IN before it. The
      discriminator is the topic's own staging date, not the file's mtime — an
      opt-in topic that gets touched for an unrelated reason must not silently
      become required.
      Needed a new git primitive: `first_commit_date`. The existing
      `last_commit_date` is the wrong signal by exactly the failure this task
      names — age uses the last touch, obligation uses the first. An unknown
      date is treated as opt-in, never required.
- [x] 2.3 Never gate-blocking (Q2). A finding here is a nudge; assert that in a
      test, because the default instinct on a new family is to fail the gate.
      Every finding is WARNING even where conformance is REQUIRED — the
      required/opt-in distinction lives in the rule TEXT, which is what a reader
      acts on, rather than in a severity that would fail a run under
      `--fail-on error`. Asserted by
      `test_non_conformance_is_never_gate_blocking`, and proven on the real
      corpus: the full doc-health run exits 0 with 29 new warnings and no new
      errors. Escalating this family needs a new ruling, which the code says.

## 3. The outline tab

- [x] 3.1 Render identified sections from headings and `xspec:` fences. No
      content-sniffing, no fabricated headings.
      MODEL BUILT, RENDERING NOW WIRED. `web/views/outline-model.js` is a pure,
      fence-aware section model — identifies sections from real `## ` headings
      and `xspec:` fences, classifies required / added / proposal-element,
      extracts `Added-by:` provenance, reports gaps. 9 tests under node,
      including that nothing is fabricated (every reported section is asserted
      to be a real line in the source) and that QUOTING the canonical fenced
      skeleton is not adopting it. Wiring waited on 3.2's ruling: the index and
      the add-section affordance share one pane, and building that layout twice
      is the avoidable cost.
      WIRED with 3.2 as the shared pane predicted — the outline selection tab now
      renders the section index (title, role, line, `Added-by:`) above the
      viewer's rendering of the same fragment, from the bytes `renderViewer`
      hands back through its new optional `onText`. The second fetch that a
      separate index pass would have needed does not exist: D15's one-read rule
      for document content is intact.
- [x] 3.2 Add-section affordance writing through `edit-document`, scoped by the
      target section; `Added-by:` provenance stamped on the added section.
      UNBLOCKED 2026-08-15 by Amendment 1 (Brett: "amend to edit-document").
      As ratified this said `edit-apply`, which is the gate console's
      main-resident redline verb — it requires a change id and applies to change
      documents, so it cannot write a staged fragment on a session branch, and a
      topic that HAS an owning change has already moved its material out of
      staging. `edit-document` is the session content verb the buffer contract
      already uses; Q4's intent (no second write verb, existing session path,
      section scoping as a targeting detail) is unchanged.
      LANDED as design (A): the affordance inserts the section skeleton into the
      outline BUFFER and stops. It performs no network call, no gate action and
      no save — the human's existing Save carries the text through
      `edit-document`, so the tab gained no write verb of its own. The insert
      lands through the canvas's OWN `applyProposal`, reused rather than
      paralleled: it already owns the settled-identity gate (an insert computed
      against text the buffer has since moved off is refused, never forced), the
      line-ending re-flavor (without which one insertion becomes a whole-file EOL
      rewrite), and `edit()` itself — so the dirty state, hashing and Save plan
      are byte-for-byte what typing produces. Scoping is a reported addressing
      key: a required section takes its canonical place in the skeleton's own
      order, and a free-form section is anchored by a target the human names.
      Provenance follows the contract's non-uniform rule rather than making it
      uniform — required sections stamp `Added-by:` on the seeded note or
      question the way the skeleton shows, and a section beyond the required set
      carries the section-level line.
      ADVERSARIAL REVIEW (FIX FIRST) closed three findings on this task. **F2**:
      the duplicate rule was rank-wide on BOTH routes, so on a fully templated
      fragment "Exit criteria", "Why we deferred", "Impact analysis", "Claims
      log", "Prior art on why", "Conflicts with promoted specs" and "Open
      questions for Brett" were all refused — naming a section the human never
      asked for, with an explicit target unable to get round it — while a
      near-miss like "Notes on conflicts" was silently rewritten to
      `## Conflicts` with the conflict seed. Since the free-form control is the
      ONLY route to the contract's "either a human or an AI may add a section
      beyond the required set", the grant was unusable. The two routes are now
      separated by an explicit `required` flag: the gap row keeps the loose
      label match and the rank clash (both doing necessary work there), and the
      free-form route is exact — exact-title duplicates, verbatim headings,
      canonical placement only for a title that already IS a canonical heading.
      All fourteen cases are pinned, and the pre-fix module was re-run to prove
      each one was genuinely refused rather than merely untested. **F3**: the
      refusal branch echoed the seam's `error` text, which both other consumers
      of `applyProposal` forbid (the chat calls its mapping a WHITELIST and drops
      the text unread; the canvas states its sentences are "never echoed") — so
      the reachable settling window handed the human "the buffer identity is
      still settling" with no recovery, and the stale sentence said "proposal", a
      noun this tab never uses. `outcome.code` is now mapped to four fixed
      tab-voiced sentences, each naming its own recovery, and the seam's own two
      refusals gained codes so they map accurately rather than falling through.
      The settling window is driven for real in the test through a holdable hash
      seam, including that the advice is TRUE: the same press lands once the
      identity settles. **F4**: on a fragment ending inside an unclosed fence the
      insert appended inside the fence, the model then saw zero sections, the
      "already carries" guard could never fire, and repeated presses piled up
      copies each reporting success. `insertSection` now refuses on an unclosed
      fence — refusal, not repair, because closing it would rewrite a fragment
      nobody asked us to change, which 3.3 forbids outright.
- [x] 3.3 Degrade on non-conforming fragments: render what is present, report
      nothing as broken, rewrite nothing on open.
      `outlineModel`'s `pre-template` state drives one calm sentence naming the
      MIGRATION STAGE — "staged before the outline template … the opt-in posture,
      not a fault" — asserted to contain none of error/invalid/broken/fail. A
      pre-template fragment's real sections render, the buffer is still clean
      afterwards, and its bytes are byte-identical to the stored bytes. A
      fragment whose bytes never arrive gets NO index at all rather than one
      derived from an absent load: the index is built from the text
      `renderViewer` hands back on a successful load and from nothing else.
      Review hardenings: the `onText` invocation is now CONTAINED (H1) — callers
      do not await `renderViewer`, so a throw inside a caller's derivation was a
      silent unhandled rejection after the document had already rendered; the
      honest outcome is a missing index, and the test proves it by removing the
      guard and watching the promise reject. The index header now says
      "as stored" (H2), because the index describes the SAVED fragment while the
      canvas holds unsaved work — without the label, a gap row above an
      "already carries" refusal reads as the surface arguing with itself rather
      than as the two honest answers the deliberate split gives.
- [x] 3.4 Gate-off posture: the affordance is not a live control and no write
      path is reachable.
      The predicate is `canvasOffered()` — the same derivation `drawCanvas` and
      `docTileVerbs` use, deliberately not `canvasController !== null`, because
      `drawTab` runs BEFORE the canvas mounts and a controller check would
      withhold the affordance on capable consoles too. With no seam the controls
      render disabled AND WITH NO LISTENER BOUND: disabled alone would leave a
      write path for anything that re-enabled the node. The index still READS on
      a gate-off plane — reading a topic's structure needs no authority.
- [x] 3.5 Leave the outline buffer's seeding, hashing, dirty-state and Save
      semantics untouched — this is presentation and addressing only. A diff in
      `BUFFER_KINDS` or the save order means the change has overreached into
      `doxbench-editing-model` Phase B's territory.
      Held. No line of `doxbench-state.js`, `doxbench-editor.js` or
      `doxbench-save.js` changed; `BUFFER_KINDS`, `SAVE_DOCUMENT_ORDER_RULE` and
      `saveBufferOrder` are asserted from the LIVE modules the composition
      imports. The one seam added anywhere is `viewer.js`'s optional `onText`
      read-back, which exists precisely so the tab does not open a second fetch
      for bytes the viewer already has.

## 4. Tests

- [x] 4.1 Template conformance: required sections present; a bare question with
      no recommended answer is non-conforming.
      MOSTLY ALREADY DISCHARGED by 2.1–2.3, and said so rather than re-proven:
      `tests/doc-health/test_families.py` already pinned the three required
      sections (both present and absent, including the fenced-skeleton quoter),
      that a missing sub-field is named, and the WARNING severity; the JS side
      already pinned the same rules through `outlineModel`. What none of them
      reached is the contract's own emphasis — "A question is never recorded
      bare. The template forces a recommendation and the reasoning for it even
      while the disposition itself stays `open`" — because the existing case drops
      `Explanation:` from an otherwise complete question, which is a missing field
      but not the shape the rule is about. Added, on BOTH sides because the
      checker and the surface must mean the same thing by conformance: a bare
      question reports all four fields; a question carrying Context and a
      disposition but NO recommendation is non-conforming and names exactly the
      two it owes; every incomplete question is reported, not only the first; and
      a `### ` sub-heading OUTSIDE Open questions is not an open question (without
      that last one the rule would fire on much of the corpus, and a family a
      human learns to ignore has lost its whole value).
      Each new case was proven to BITE by breaking the rule in the implementation
      and watching which test failed — `>=` to `>`, first-commit to last-touch,
      the open-questions scope gate, first-missing-field-only, and dropping
      `Recommended answer` from the sub-field tuple. The recommendation rule was
      caught by NOTHING before this task: that mutation passed the whole
      pre-existing suite on both sides.
      THE STRUCTURAL REASON IT WAS INVISIBLE, worth more than the fix: both
      pre-existing agreement tests assert in ONE DIRECTION — the checker's fields
      are named in the contract prose, and the checker's fields appear in the JS
      model. Neither asserts the reverse. A direction-blind pair cannot see
      SHRINKAGE: remove a field and both simply assert less, in step, and stay
      green. The new assertion therefore names the four literally rather than
      looping the constant, plus pins the tuple's exact contents, so the pair now
      closes in both directions. (Review round 2 caught that the bare-question
      test as first written still looped the constant, and so still passed the
      mutation it was added for.)
      ONE CONTRACT RULE IS STILL UNENFORCED AND DELIBERATELY LEFT SO: the four
      sub-fields are specified "in this order", and neither the family nor the
      model checks order — `families.py` collects them into a `set` and discards
      order outright; `outline-model.js` keeps encounter order but scores only
      membership. A test cannot fail-if-broken against a rule nothing implements.
      The reason it is not implemented HERE is that enforcing it needs a
      production change to `families.py` mirrored in `outline-model.js`, and this
      slice touches no production file — not corpus risk: the corpus was counted,
      and all 12 open questions carry all four sub-fields IN ORDER, so an order
      check would raise zero new findings today. (An earlier draft of this note
      claimed corpus risk. It was wrong, and the count is recorded here so the
      next reader does not inherit the excuse.) Either the ordering words are
      advisory or both implementations need the rule; that is a ruling, not a
      test.
- [x] 4.2 Round-trip: demote a fragment that reached proposal and assert the
      proposal-element sections carry the real prior text, not the aspirational
      original. This is the requirement's whole point and the one test that must
      not be a shape assertion.
      **UNBLOCKED AND DISCHARGED 2026-08-19** by
      `align-demote-to-round-trip-rule`, which was proposed, ratified, realized
      (PR #215) and archived precisely because this task could not be written
      honestly against the old mechanism. The blocker's full diagnosis is kept
      below, unedited, because it is the reason that change exists.
      THE TEST, in `tests/ideation-dashboard/test_gate_console.py`, drives BOTH
      GATES rather than constructing the middle: the real
      `proposal-support.py transition` forward — so "reached proposal" is the
      mechanism's own doing, with the fragment really moved into
      `supporting-docs/`, flipped to `Status: draft`, its original bytes kept under
      `source-snapshots/`, the manifest's `transitioned_at` written, and the topic
      folder emptied — then the real console demote back. Both DATES are therefore
      real: `Raised` from the transition that raised it, `Demoted` from the demote
      that returned it. The marked section is asserted to carry the proposal's
      distinctive in-flight text and NOT the equally distinctive aspirational
      guess, so neither a template placeholder nor a snapshot echo can pass; the
      forward transition's `Status: draft` is asserted undone; and a second test
      takes a second lap through both gates, because "nothing learned may be lost"
      has to survive more than one use.
      WHAT WAS ALREADY PINNED and is cited rather than repeated: the
      absent-destination restore, the marked-section refresh against a returned
      proposal, the five slots, `Raised` from a manifest, the never-byte-replace
      guard, and the CRLF drive all landed with the realizing change. What none of
      them did was reach proposal for real — they hand-built the post-transition
      shape — and that gap is exactly what 4.2 adds.
      MUTATION-VALIDATED: disabling the marked-section refresh, disabling the
      outline arm entirely, and making `Raised` unresolvable are each caught by
      both new tests. (A first pass at the outline-arm mutation hit an
      identically-indented line in `executable_plan` instead and appeared to catch
      nothing — recorded because "the mutation found no coverage gap" and "the
      mutation edited the wrong line" look identical in the output.)
      THREE FINDINGS CAME OUT OF DRIVING IT, all recorded in the realized change's
      §7.2: `plan_demotion` resolves the origin topic only from a possible's pick
      edge that the forward transition erases, so a genuinely-transitioned change
      reports `origin_staging_id: None` and the demote needs `--staging-topic`
      (measured TOTAL: 12 of 12 active changes on the real corpus, not just the 4
      that declare `origin.kind: staged`); a demote leaves its own
      `openspec/INDEX.md`, which has no `Status:` header and so refuses the next
      whole-folder forward transition; and `Proposed by:` accumulates one line per
      lap. Also corrected in the test itself: a first draft
      asserted the FIRST lap's proposal text also survived the second lap. The
      contract promises "the last attempted `proposal.md`", singular — the earlier
      text is superseded in the marked slot, not lost by the demote — so the
      assertion was wrong and the code was right.
      THE BLOCKER, AS DIAGNOSED, kept for the record:
      Not because the rule is unimplemented — because THE MECHANISM ACTIVELY
      INVERTED IT.
      (An earlier draft of this note said the demote "does not touch the primary
      fragment at all". That was FALSE, and it is the fourth time this change has
      been bitten by a claim about a mechanism that nobody drove. It was corrected
      by driving the mechanism, which is the only thing that has ever settled one
      of these.)
      THE MECHANISM. `gate_console.py`'s `plan_demotion` / `demote` /
      `execute_demotion_plan`, reachable as `cli.py gate demote --execute` and
      `POST /actions/gate/demote`, with eight tests in
      `tests/ideation-dashboard/test_gate_console.py` including byte-exact CRLF
      preservation. `proposal.md` and its siblings return to
      `ideation/staging/<topic>/openspec/` as `Status: draft`, a
      `## Returned drafts` note is appended to the topic README carrying the change
      id, the demote date and the reason, an `openspec/INDEX.md` is written, and the
      change folder is removed.
      THE INVERSION. `classify_change_file` (gate_console.py:548-549) routes
      ANYTHING under `supporting-docs/` back to the TOPIC ROOT by bare basename
      with a `Status: draft` flip. And the supporting-docs manifest that
      `proposal-support.py transition` writes records the topic's own primary
      fragment under exactly that bare basename — this change's own manifest has
      `path: staged-topic-outline-template.md` with `remaining_paths: []`. Since
      the primary fragment's basename IS `<topic>.md`, the demote's destination IS
      the primary fragment path.
      Driven, not reasoned: a fixture whose fragment carried real post-proposal
      text plus a filled round-trip slot, demoted through the real console and
      executor, came back carrying the ASPIRATIONAL snapshot verbatim — the real
      in-flight text gone, all four slots gone, and `Status: draft` on a file
      `_primary_fragment` still selects as the staged topic's outline.
      So the ratified rule titled "A demoted topic does not reset to its
      aspirational text" describes precisely what the mechanism performs, silently,
      over the one file the wheel, doc-health and the outline tab all read.
      GENERALITY. Not a special case: of the 9 changes carrying a supporting-docs
      manifest, 2 declare a `staged` origin, and BOTH record a file whose basename
      equals `<topic>.md` — i.e. 2 of 2 would overwrite their topic's primary
      fragment on demote. The other 7 predate the origin contract and declare none.
      This is the shape `transition` produces.
      SECONDARY DEFECT, worth its own line: the destination is flipped to
      `Status: draft` while `_primary_fragment` and `primaryFragmentPath` still
      select it as the STAGED topic's outline — a staged topic whose outline
      announces itself as a draft, which `status-validity` and the wheel both read.
      LATENT, AND ONLY LATENT BY ACCIDENT: today the restore reads as harmless
      because `transition` empties the topic folder on the way out
      (`remaining_paths: []`), so the destination is usually absent when the move
      lands. If a fragment were ever left behind, or the topic re-staged and worked
      before a demote, the identical move overwrites live human work byte for byte
      with no diff, no prompt and no record beyond the README note.
      NO CHECKER READS THE SLOTS EITHER, so the fallback this task allows —
      distinguishing a genuine round-trip slot from the aspirational original —
      has no purchase: `fam_staged_topic_template` scores the three sections and
      four sub-fields only, and `location-conformance`'s `_staged_exit_changes`
      scans `## Exit`. Nothing anywhere writes `Status at demote` or
      `Demote reason`.
      THE MISCONCEPTION IS RECORDED AS FACT in the corpus:
      `openspec/changes/add-doxbench-editing-phase-a/tasks.md:193-194` says the
      slot "fills on demote only, per the template". Nothing fills it, and the same
      demote deletes it.
      DISPOSITION IS BRETT'S, and this is a contract/mechanism divergence needing
      OpenSpec, not a test. Recommendation carried forward: treat it as a DEFECT
      FIX in demote — keep `Status: staged` on a fragment destination, and fill the
      four slots from values `execute_demotion_plan` already holds (change id,
      demote date, reason; `Raised` from the change's own transition manifest) —
      with the `xspec:candidate` refresh from the returned `proposal.md` as the
      genuinely new surface, possibly its own change. Deliberately NOT built here.
      What was refused: writing a harness that "demotes" by hand-authoring the
      expected fragment and asserting it. That is a shape assertion in a costume,
      and it would have hidden the inversion instead of finding it.
      (END OF THE BLOCKER RECORD. Brett ruled the recommendation above, and
      `align-demote-to-round-trip-rule` built all four parts of it — including the
      `xspec:candidate` refresh — and is archived at
      `openspec/changes/archive/2026-08-19-align-demote-to-round-trip-rule/`. The
      refusal in the paragraph above is what made the test worth writing once the
      mechanism could support it.)
- [x] 4.3 Opt-in boundary: a pre-ratification topic warns and does not block; a
      post-ratification topic is required.
      The three ends were already pinned by 2.2/2.3 — pre-ratification is opt-in,
      post-ratification is REQUIRED, an unknown date is opt-in — so what this task
      added is the BOUNDARY itself and the trap 2.2 was built to avoid, neither of
      which any existing test reached. The discriminator is
      `staged_on >= TEMPLATE_RATIFIED`: a topic staged ON the ratification day is
      REQUIRED and the day before is opt-in, pinned as a pair so the comparison
      cannot drift by one day in either direction — and a whole day of topics
      claiming the opt-in posture forever is not a recoverable error, because
      obligation never re-derives.
      The trap is now DRIVEN rather than described: the context offers a
      contradictory `last_commit_date` well after ratification AND a freshly
      touched mtime, and the verdict must still be opt-in. Swapping
      `first_commit_date` for `last_commit_date` in the family is caught by that
      test (and, it turns out, by three others — recorded because it means the
      existing suite already had partial protection against exactly one mutation
      of this line, which is not the same as pinning the rule). Finally both
      postures are exercised in ONE run to prove the verdict is per topic, since
      Q2 means the corpus stays deliberately non-uniform for a while and a family
      deciding once per run would mislabel every topic on one side of it.
      `_ctx_for` gained an additive `last_dates` parameter to make the trap
      expressible; every existing caller is unchanged.
- [x] 4.4 Outline tab: sections identified from headings/fences; add-section
      goes through `edit-document` with provenance; non-conforming fragment renders
      without rewrite; gate-off offers no live control.
      Two files, split by what each can actually prove. The PURE insertion rules
      (canonical placement, the heading a required section really lands under,
      provenance placement, the already-present refusal, explicit targeting, EOL
      blindness, one blank line each side) extend `test_outline_model.py`'s node
      harness — 12 new cases, no DOM. The WIRING is
      `tests/ideation-dashboard/test_outline_tab.py`, which mounts the REAL
      `mountStagingWorkbench` against the DOM instrument `test_doxbench_view.py`
      owns (imported, never copied) and presses the buttons: the add dirties the
      outline buffer, and the Save that follows is the shipped
      `savePlanState` + `runSave` over a recording transport — wired exactly as
      app.js wires it — so `action: "edit-document"` is READ OFF THE WIRE rather
      than asserted from a fixture. Three assertions exist because the first
      draft of the test got them wrong and the code was right: the fixture quotes
      the canonical skeleton inside a ```markdown fence, so every heading
      assertion in the harness is fence-aware and INDEPENDENTLY implemented — a
      check routed through the scanner under test could not have caught a fence
      bug in it.
      REVIEW ROUND 2 grew the set to 72 cases and, more usefully, made three of
      them honest. **F1** was a test-coverage regression this task itself
      introduced: loosening `test_session_confinement.py`'s call-site pin to a
      substring made it a prefix of the DECLARATION too, so it stopped
      constraining the call — the reviewer swapped `sourceBase` for `null` at the
      call site and the whole suite stayed green, re-opening the finding-16
      failure ("a draft view mistaken for main") the pin exists to catch. It is a
      regex through the call's own closing arguments now, and the mutation was
      re-run to confirm it FAILS. **F5**: `"Added-by: brett · 20"` passed on a
      literal "20"; the date half is a `\d{4}-\d{2}-\d{2}` match. And every new
      regression test was validated by re-running the PRE-FIX code against its
      fixture rather than assumed — which is what caught that F2's seven headings
      only misbehave on a FULLY templated fragment, so the original three-section
      fixture would have proven nothing.

## 5. Gates

- [ ] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate add-staged-topic-outline-template
      --strict`, then `--all --strict`, from the `openxFactory/` root.
- [ ] 5.2 `python3 -m pytest tests/ideation-dashboard -q` and
      `tests/doc-health` — exit codes read directly, never through a pipeline.
- [ ] 5.3 doc-health full run: 0 new regressions beyond the new warning family's
      own intended findings, which should be enumerated rather than counted.
- [ ] 5.4 Live proof in a browser: open a conforming topic and a pre-template
      topic in the outline tab, add a section to the conforming one, confirm the
      commit lands through `edit-document` on the session branch.

## 6. Bookkeeping

- [ ] 6.1 README "OpenSpec Records" active block.
- [ ] 6.2 Tick the staging topic's exit and mark the INDEX row proposed.
- [ ] 6.3 Hand Q4's ruling to `doxbench-editing-model` Phase A — `edit-document`
      is the verb (Amendment 1; ratified as `edit-apply`, which cannot reach a
      session branch), so Phase A's chat edits become marker-scoped section
      patches.
      That upgrade belongs to Phase A, not here; this task is the handoff, not
      the build.
