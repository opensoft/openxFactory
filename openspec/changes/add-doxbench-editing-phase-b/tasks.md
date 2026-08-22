# Tasks: add-doxbench-editing-phase-b

Sections 1–2 are this proposal's own work. Section 3 is a BLOCKING gate: every
verify item is discharged, with its finding recorded, before the slice that
depends on it may start. Sections 4–13 are realization and are DOWNSTREAM OF
RATIFICATION — none of them starts before Brett ratifies this change.

## 1. The contract

- [x] 1.1 The `ideation-dashboard` delta: eight MODIFIED requirements — five
      promoted (`doxBench editor buffer contract`, `Grounded doxBench chat
      turn`, `Typed AI proposals and stale-application protection`, `doxBench
      scoped view`, `doxBench model catalog and provider boundary`) and three
      declared RELATIVE TO PHASE A's outcome (`The doxBench chat binds to the
      active buffer selection`, `The canvas view surface is expressed over the
      buffer set, not over two names`, `One Save and one Cancel govern the
      doxBench canvas`) — plus nine ADDED requirements (the loaded set; the
      loaded-document selector; the tile's three verbs; per-document threads
      and their state header; share-session; the staged-set knowledge service
      and its bounded packet; the three-layer compression stack; the harness
      bridge; the chat-turn release obligation).
- [x] 1.2 The `memory-gateway` delta: one ADDED requirement declaring the
      subject-free local consumer class, with the honest reasoning for why the
      contract needs it rather than a silent skip (proposal + design §7.1).
- [x] 1.3 `OPENSPEC_TELEMETRY=0 openspec validate add-doxbench-editing-phase-b
      --strict` and `--all --strict` both green.
- [x] 1.4 `design.md` carries every mechanism decision the fragment left to a
      design pass: the buffer-key rule (D1), the N-document save ordering (D3),
      the tile Save's scope (D4, flagged), the packet pipeline and its degraded
      postures (§3), the bridge process lifecycle (§5.2), the thread-file format
      sketch (§4.1), the release shape (D15/D16), what stays out (§8), and the
      three conformance declarations (§7).
- [x] 1.5 README "OpenSpec Records" active block carries the entry.
- [x] 1.6 Doc-health pre/post diff shows zero NEW findings.
- [x] 1.7 `.openspec.yaml` declares the staged origin
      (`openxFactory:staging:doxbench-editing-model`) and the sequencing
      dependency on `add-doxbench-editing-phase-a`.

## 2. The claims-to-requirements audit

- [x] 2.1 Every one of the fragment's 26 claims maps to a requirement or is
      explicitly out of scope with a reason: Claims 1–7 (Phase A, landed),
      8 → the tile verbs, 9 → the selector, 10–12 → threads, 13–14 → threads +
      the state header, 15 → the MCP boundary + assembly port, 16 → the
      graph-less v1 and the graduation trigger, 17 → the install-time
      declaration, 18 → promotion is gate-only, 19 → the source hierarchy in the
      system prompt, 20 → the harness bridge, 21 → share-session, 22 → the
      memory-gateway conformance declaration and its delta, 23 → the
      property-level derived-model assertion (design §7.2, flagged), 24–25 →
      the three-layer compression stack, 26 → the watch-list discipline.
      **Claim 22's "first consumer" framing is stated PRECISELY** per task
      3.7's finding, in both `design.md` §7.1 and `proposal.md`: this change is
      the first consumer to declare FORMAL PER-REQUIREMENT conformance to
      `memory-gateway` and the first SUBJECT-FREE one — not the first thing in
      xFactory to reference the contract's vocabulary at all.
      `installs/hermes-install`'s `add-memory-gateway-binding` (archived
      2026-07-24) is the prior, narrower, subject-bearing and self-described
      provisional precedent, and it strengthens the case for the delta rather
      than weakening it.
- [x] 2.2 Every one of the seven questions carries a disposition other than
      `open`, so this change EXITS the topic. Q1/Q3/Q7 are the three Phase B
      inherits, and each ruling's verbatim text is quoted in `design.md`.
- [x] 2.3 The two naming debts Phase A opened are closed: the tile's `open`
      verb becomes `read`, and the new verb is `load-for-editing` in contract
      text so the bare word "edit" keeps the meaning Phase A reserved for it
      (design D8).

## 3. Verify list — BLOCKING, before any dependent slice starts

Each item: verify against the upstream source, record the finding in this
change's folder (an appended `verification.md` or the task line itself), and
state whether the finding CHANGES a mechanism this design assumed. A finding
that changes a mechanism reopens the affected design section before its slice
starts. Items are cited from the fragment's VERIFY LIST (a)–(g).

- [x] 3.1 **(a) The harness's memory backends** — the local / Hindsight /
      Mnemopi claims are cited from the harness README by an external design
      review and unverified by our own research. Verify what backends exist and
      what each stores. Blocks §11 (bridge). A backend that cannot be disabled
      would change the split-brain prohibition from a policy into a refusal.
      **Verified 2026-08-18** — see `verification-findings.md` §3.1. Four
      mutually-exclusive backends (`off|local|hindsight|mnemopi`), one enum,
      `off` is the default and a true no-op. Does not change the mechanism.
- [x] 3.2 **(b) MCP client depth** — how deep the harness's tool-calling
      support goes. Blocks §10 (knowledge service): the MCP boundary is only
      reachable from the model if the harness can call tools at all; if it
      cannot, the packet is assembled entirely server-side and the boundary
      serves our own assembler only. Record which of the two it is.
      **Verified 2026-08-18** — see `verification-findings.md` §3.2. Full
      hands-on end-to-end proof: real mid-turn MCP tool dispatch via
      `write xd://<tool>`. The boundary is model-reachable. Does not change
      the mechanism.
- [x] 3.3 **(c) `SYSTEM.md` re-read cadence** — per turn, or cached at session
      start. Blocks §10 (the source-ranking hierarchy): a cached read means the
      hierarchy is fixed for a session and a change requires a session restart,
      which the surface must then state.
      **Verified 2026-08-18** — see `verification-findings.md` §3.3. Read once
      at session start (`main.ts`), rebuilds reuse the captured string
      (`sdk.ts`), never re-read from disk mid-session. Does not change the
      mechanism.
- [x] 3.4 **(d) Cognee's current default embedded graph backend** — in flux
      after the Kuzu archival (watch `topoteretes/cognee#2098`). Blocks nothing
      in v1 by construction, and blocks any graduation: a version pin against a
      moving default is not a pin. Record the state and the date read.
      **Verified 2026-08-18** — see `verification-findings.md` §3.4. Migrated
      Kuzu → Ladybug (pinned `0.19.0`, merged 2026-08-15 upstream), still
      under active churn. Informational; blocks nothing in v1.
- [x] 3.5 **(e) Where the harness's session artifact store lands on disk** —
      inside the session worktree (so offloaded artifacts ride the branch under
      share-session) or outside it. Blocks §9 (threads) and §12
      (share-session): if it lands outside, share-session must say so rather
      than implying it shared everything.
      **Verified 2026-08-18** — see `verification-findings.md` §3.5. Lands
      OUTSIDE the worktree by default (`~/.omp/agent/sessions/...`), hands-on
      confirmed. Phase B's own-sidecar approach (§4.1) is unaffected and
      necessary; adds one concrete requirement to task 9.1 (dereference
      `artifact://` content before writing to the sidecar).
- [x] 3.6 **(f) `/shake`'s trigger surface** — manual command, automatic
      threshold, or both; and whether RPC mode exposes it programmatically
      rather than only interactively. Blocks compression layer 3's realization:
      an interactive-only command is not a mechanism a server can rely on, and
      the layer would then need a different v1.
      **Verified 2026-08-18** — see `verification-findings.md` §3.6. Both
      manual and automatic surfaces exist; manual `/shake` confirmed hands-on
      reachable in `--mode rpc` via `{"type":"prompt","message":"/shake elide"}`.
      Does not change the mechanism.
- [x] 3.7 **(g) `memory-gateway`'s realization depth elsewhere in xFactory** —
      is any conformant consumer live today, or is this the first? Blocks the
      `memory-gateway` delta's landing: a first consumer proposing a contract
      amendment must say that it is the first (Claim 22's honest flag).
      **Verified 2026-08-18** — see `verification-findings.md` §3.7.
      `installs/hermes-install`'s memory-boundary gate precedes Phase B
      (ratified 2026-07-24) but is subject-bearing and provisional; Phase B is
      the first subject-free consumer and the first to declare formal
      per-requirement conformance. Precision correction to Claim 22's framing
      recommended before landing (not a reversal).
- [x] 3.8 Record every finding, including "verified as assumed", so a later
      reader can tell a checked assumption from an unchecked one.
      Done — `verification-findings.md`, all seven items independently
      checked against upstream source or hands-on execution; none left as
      "verified as assumed."

## 4. State generalization (first, because everything depends on it)

- [x] 4.1 `doxbench-state.js`: the buffer set becomes KEYED — `outline`
      reserved, document buffers keyed by repository-relative path, the reserved
      `document` key for at most one unbacked create slot (design D1).
      `BUFFER_KINDS` survives as the KIND vocabulary and stops being the state's
      key list. The module stays import-free so the Node harness keeps
      executing the browser's exact bytes.
- [x] 4.2 `validatedDoxBenchState` enforces the new shape: `outline` present;
      every other key equal to its buffer's own path; the reserved key at most
      once; every buffer's repository equal to the scope's. The
      exactly-two-keys throw is replaced, not relaxed into silence.
- [x] 4.3 `createDoxBenchState`, `replaceBuffer`, `setActiveBuffer` operate on
      buffer KEYS. `beginBufferEdit`, `settleBufferHash`, `adoptSavedBase`,
      `discardBuffer`, `applyProposalToBuffer` are UNCHANGED — verify by diff
      that they are, since that is the design's central claim about this layer.
- [x] 4.4 A re-key primitive moves the reserved unbacked buffer to its path when
      the server reports one, stepping the hash generation as every other base
      transition does.
      The PRIMITIVE is realized and pinned (`rekeyDocumentBuffer`: the reserved
      key is freed carrying nothing from the buffer that left it, and the
      generation steps).
      **FINDING, recorded rather than papered over.** Its UI half is not
      reachable as the task assumes: the ratified seven-field per-buffer outcome
      row carries no path, so the canvas cannot learn the path a `create-document`
      reported and cannot call the primitive from a Save verdict. Widening the row
      to an eighth field would contradict the same requirement's
      "unchanged in shape" clause, so it is NOT done here. The canvas also cannot
      reach the case today: a path-less create request declares no document, which
      the server's own transaction refuses, so no unbacked create Save exists on
      this surface to re-key from. Resolving it is a choice between (a) the row
      carrying the created path and (b) the re-key staying a state-module
      primitive driven by whichever flow does create a document — and it is
      Brett's call, not a realization detail.
- [x] 4.5 `persistDoxBenchState`/`restoreDoxBenchState` carry the keyed set, and
      a Phase A session envelope (`{outline, document}`) restores unchanged —
      the migration-free property D1 was chosen for. Prove it with a test that
      restores a captured Phase A envelope.
- [x] 4.6 The per-buffer staleness guard is applied N times and nowhere widened:
      no force path, no cross-buffer settle, no shared generation counter.
- [x] 4.7 Re-pin `tests/ideation-dashboard/test_doxbench_state.py` and the
      module-boundary assertions in `test_staging_workbench.py` with the reason
      stated; never delete an assertion to make a refactor pass.

## 5. The turn contract

- [x] 5.1 `doxbench_turns.py`: `require_outline_and_document` becomes a
      one-outline-plus-N-documents requirement, refusing a duplicate path, a
      missing outline, and an unexpected kind with the same redacted shape.
- [x] 5.2 `revalidate_scope`: the declared BOUND-BUFFER key must name a supplied
      buffer; every supplied path must be in-scope and editable; the refusal
      leaks no projection or buffer content. The per-buffer binding check
      (including the session-base widening) runs once per buffer, unchanged.
- [x] 5.3 `PROPOSAL_TARGETS` and `ObservedHashes` become buffer-key-shaped; the
      proposal cap is expressed over the request's buffer count.
- [x] 5.4 `PROMPT_SECTION_ORDER` grows deterministically: one section per loaded
      document in the declared order, plus the packet's sections (§10). The
      order stays a single declared constant.
      **BOTH HALVES LANDED.** The document half: the single `document_buffer`
      slot became the `document_buffers` GROUP, expanded by
      `prompt_section_keys` to one `document_buffer:<buffer key>` section per
      loaded document in the declared order, from ONE constant, pinned at both
      levels.
      The PACKET half (with §10): four more groups joined the same constant in
      design §3.1 step 5's own order — the packet's DECLARATION, the selected
      thread, the other threads' state headers, the evidence with refs — all
      ahead of the outline and document buffers. Two of them EXPAND per item
      exactly as `document_buffers` does (`thread_state:<key>`,
      `evidence:<ref>`), and one function decides that expansion so the
      concrete keys and the rendered sections cannot disagree; a companion test
      asserts they do not.
      `prompt_section_keys` now takes the packet as a REQUIRED keyword rather
      than a defaulted one, because every turn carries a packet — an absent
      knowledge service yields the DECLARED REDUCED packet, not a packet-less
      prompt — and a `None` default would invent a second prompt shape no
      requirement sanctions.
      **JUDGEMENT CALLS, flagged rather than buried.** (a) `transcript` keeps
      Phase A's position. Step 5's list does not name it at all, so moving it
      would invent an ordering the design does not state, and dropping it would
      drop a released input; it sits adjacent to the thread sections it is the
      wire-carried counterpart of. (b) The packet's DECLARATION section is not
      in step 5's list either. It exists because the packet must declare its
      purpose, its sources with refs, its scope and its expiry somewhere a
      reader of the prompt can see, and because that is where a REDUCED posture
      is stated (§3.4) — neither of which has another readable home.
      **WHAT STILL WAITS, and on what.** Step 5's `model data handling`,
      `scope`, `working subject`, `outline buffer`, `document buffers`, `human
      message` and `response instruction` already existed and are untouched.
      Nothing in step 5 is now missing. The SECTIONS' contents that later
      slices own are the thread material itself (§11 mirrors turns into the
      sidecars this packet reads) and any layer-three offload placeholder (§11
      again) — both of which flow through the seams here without changing this
      order.
      **RE-PINNED, with the reason stated:** the turn suite's POSITIONAL
      section lookups (`envelope.sections[6]`) became key lookups. An index
      pinned a section's identity to a count the packet changes, and it had
      already gone quietly wrong once — `sections[6]` named the OUTLINE buffer
      in a test asserting about the DOCUMENT buffer, which passed only because
      both carried the label it checked for. The declared ORDER is still
      asserted whole against `prompt_section_keys`.
- [x] 5.5 `SYSTEM_CONTRACT_TEXT` carries the source-ranking hierarchy —
      ratified/standard canon > accepted/staged facts > promoted findings >
      active thread state > harness-local memory last and non-authoritative.
- [x] 5.6 Re-pin `test_doxbench_turns.py`. The F2 carve-out's note that
      `doxbench_turns.py` was left untouched by Phase A is superseded here, and
      the supersession is stated in the test's own reason.

## 6. Save ordering

- [x] 6.1 `doxbench-save.js`: `SAVE_BUFFER_ORDER` becomes the ordering RULE —
      outline first when dirty (ancestry), then documents in a declared
      deterministic order (design D3).
- [x] 6.2 A dirty outline that did not land reports every document
      `not_attempted` with the missing-ancestry reason. A document refusal stops
      no other document: the `blocked` chain applies to the ancestry step only.
- [x] 6.3 The seven-field per-buffer outcome row is unchanged in shape and has
      more rows; `wholeStatus`'s `partial` case gets direct coverage across
      three documents.
- [x] 6.4 `savePlanState`/`saveOrder` key rows by buffer key; the `owned:
      false` context-only withholding is unchanged.

## 7. The selector and the canvas

- [x] 7.1 `doxbench-chat.js`: the rail header's "Working on — …" line becomes
      the loaded-document SELECTOR — a scrolling list, hover-expanded full
      names, distinguishable entries when basenames collide, keyboard-reachable
      under the surface's existing selection semantics, with an honest empty
      state when nothing is loaded.
      **Proven in COMPOSITION** after the PR #207 adversarial review found the
      empty state unreachable (F6): the reserved `document` slot is present in
      every state the canvas produces, and counting it kept `documentCount` off
      zero forever, so the ratified sentence could never render on any real
      surface. `test_doxbench_composition.py` drives the real mount and pins the
      empty state on the state the canvas actually builds.
- [x] 7.2 Selecting an entry sets the selected buffer through the existing state
      primitive and switches the transcript to that document's thread. No second
      state authority.
      **The selection half landed with §7; §11 closes the thread half and the
      `TODO(add-doxbench-editing-phase-b tasks.md §9)` is gone.** The selection
      still moves FIRST, through the canvas's own `setActiveBuffer` seam, and the
      transcript follows it: `switchThread` reads the newly selected document's
      thread through the §9.5 route and `adoptThreadTranscript` replaces the
      rail's transcript with that thread's turns. ONE call site, and a test pins
      the count — a second one would be a second answer to "which thread is this
      rail showing", which is the second state authority this task forbids.
      **The real defect it closes, stated:** the rail's transcript is what the
      next turn's WIRE transcript is built from, so leaving document A's
      conversation on screen after selecting B carried A's turns into B's next
      request as B's context. A document with no thread — or a plane with no
      thread transport, or any of §9.5's four declared absences — adopts the
      EMPTY transcript, which is the honest answer for a document nobody has
      talked about.
      **Judgement call, flagged:** the switch clears `proposals` and
      `lastFailure` as well as the transcript. Both are facts about the PREVIOUS
      document's turn, and a proposal with an Apply control targeting a buffer
      the human is no longer looking at is exactly the stale-apply hazard the
      currency rules exist to prevent. It is deliberately NOT a re-key: the
      catalog, the model selection, the composer and the working subject all
      survive, because the SCOPE did not move.
      **CORRECTED 2026-08-19 (adversarial review P2-9): the switch had to be
      refused while a turn is in flight.** The change handler was not gated on
      `state.phase`, and `adoptThreadTranscript` did not change it — so
      selecting document B while A's turn was running swapped the transcript
      under the flight, and `settleTurnSuccess` then appended A's question and
      answer onto B's transcript AND onto B's WIRE transcript, making A's
      conversation B's context on B's next turn. A's proposal was restored under
      B too, with a live Apply control, defeating the very clearing this task's
      other judgement call describes. Reachable from the UI with no server race;
      the reviewer reproduced it against the shipped module.
      The model now REFUSES by returning the identical state object — the same
      "no" `beginTurn` and `rekeyChatState` give — and the handler refuses
      BEFORE the selection moves, saying so on the rail's own note rather than
      swallowing it. A turn finishes bound to the document it was sent for, and
      the selection moves once it settles. Pinned by the reviewer's own
      reproduction, including the wire transcript.
      **CORRECTED 2026-08-19 (PR #223, Codex C4 / Copilot CP2): a STALE thread
      answer could overwrite a newer selection.** The in-flight refusal above
      closes the case where a TURN crosses documents; this is the case where the
      thread READ does. Select A, then B before A's GET returns: A's slower
      answer arrived last and unconditionally replaced B's transcript with A's
      turns — which is also B's WIRE transcript, so B's next turn would carry
      A's conversation as its context. Reproduced against the shipped module.
      `switchThread` now stamps a generation before the await and drops its own
      answer if the selection moved while it was in flight — the last SELECTION
      wins, not the last ANSWER. A counter rather than a cancel because the
      transport is a plain fetch seam with no abort surface. Both arms are
      pinned: the race reproduces without the guard and does not with it.
      **NOTED, not fixed (adversarial review P3-22):** the composer survives a
      document switch — deliberately, and consistent with FR-016 and PR #63's
      ruling that typing is never discarded — but it carries no label naming the
      document it will bind to, so text typed about A can be sent bound to B
      with no visual cue. The in-flight refusal above closes the case where a
      TURN crosses documents; this is the case where a HUMAN's half-written
      thought does. It is a surface affordance (a binding label beside the
      composer) rather than a correctness fix, it belongs with whoever next
      touches the rail's chrome, and it is recorded here because this task owns
      the switch that makes it reachable.
      **Judgement call, flagged:** `loadThread` is an OPTIONAL seam. A shell
      that supplies none keeps the pre-§11 behaviour exactly, which is what lets
      the editor-only posture and every existing composition harness stand
      unchanged.
- [x] 7.3 `staging-workbench.js`: loading a document adds it to the loaded set
      and selects it; the `outline` selection tab still selects the outline;
      all three routes leave selector, canvas and chat agreeing.
- [x] 7.4 `doxbench-editor.js` is verified UNCHANGED in structure — the view
      tabs, the one Save and the one Cancel already read the buffer set and the
      selected key (Phase A's fifth ADDED requirement). Any change needed here
      is a finding against that requirement, not a task.
      **VERIFIED, WITH A FINDING — and the finding is exactly the one the task
      says to raise.** The STRUCTURE held: the view tabs still render whichever
      buffer is selected and enumerate none, the canvas still carries exactly one
      Save and one Cancel outside both tabs, Cancel still targets the selected key
      alone, and the chat still binds to the selected key. Widening the buffer set
      required no structural change to any of them, which is what the requirement
      predicted.
      What the requirement's own prohibition CAUGHT is that the module's buffer
      ENUMERATION was expressed over the `BUFFER_KINDS` constant rather than over
      `state.buffers` — a literal two-name list baked into the surface's own
      structure, which the delta forbids in as many words. So the SOURCE of every
      enumeration moved to the state (`bufferKeysInOrder`), and membership
      questions became "does the state hold this key" rather than "is this one of
      two names", which refuses strictly more. Per-buffer DOM became lazy
      (`ensureBufferDom`) so the initial DOM is byte-identical and a newly loaded
      document gets its own nodes; label and CSS-slug rules are declared and
      pinned. A second defect surfaced with it and is fixed: `switchDocument`
      called `replaceBuffer` without naming the key, which under the keyed set
      resolved by PATH and added a new key beside the reserved slot instead of
      replacing it.
- [x] 7.5 Re-pin the DOM, tablist, accessibility and mutation-boundary tests for
      the new rail control.

## 8. The tile verbs

- [x] 8.1 `doc-wheel.js`: the expanded tile's action row carries read (the
      existing immersive reader, relabelled from `open`), load-for-editing, and
      save.
- [x] 8.2 Save on the tile is reachable only while that document's buffer is
      dirty, visibly inert otherwise, and runs the same pipeline scoped to that
      document plus the ancestry step (design D4), reporting each buffer it
      acted on.
      **Proven in COMPOSITION** after the PR #207 adversarial review found it
      enabled-then-refusing for every restored Phase A session (F2): the marking
      resolved the buffer BY PATH and the save resolved it BY KEY, and the two
      differ for exactly a real document under the reserved `document` key. ONE
      resolver now answers both, so the control's enabled state and the act it
      performs can never name different buffers.
- [x] 8.3 A loaded tile is marked, and a loaded-and-dirty tile is marked as
      needing a save, in the wheel's existing badge/colour idiom, driven off
      live buffer state and never written into the snapshot.
- [x] 8.4 A context-only (`owned: false`) document loads for grounding but
      offers no reachable Save and no must-save marking.
- [x] 8.5 Where editing is unreachable, load and save state their absence rather
      than failing on activation; read stays available.
      **Proven in COMPOSITION** after the PR #207 adversarial review found it
      unrealized (F3): the verbs existed unconditionally, so a gate-off surface
      failed ON ACTIVATION with the wrong sentence. They are now withheld by the
      SAME `canvasOffered()` derivation the canvas mount reads — not by whether
      the controller happens to have mounted yet, which would have withheld them
      on capable surfaces too, since the docs pane is drawn first.

- [x] 8.6 **ADDED by the PR #207 adversarial review (F9 and F1).** Two acts the
      ratified requirements name had no control at all, so neither existed:
      * the loaded set's ONE WAY OUT — "a document SHALL leave the loaded set only
        by an explicit human act, and that act MUST refuse or require an explicit
        discard while the buffer is dirty". `unloadDocument` shipped as a state
        primitive with no caller, which also made the declared bound a dead end: a
        session that reached it could never get back under it. The control now
        lives beside the selector, is scoped to the selected document, is never
        offered for the reserved outline, and REFUSES a dirty buffer on the first
        press while re-labelling itself to say what a second press discards.
      * the tile's LOAD as the BINDING route. Phase A bound the canvas from a
        docs-row SELECTION, and keeping that made the loaded set unreachable —
        measured: a tile click switched the single reserved slot to that path
        first, so the LOAD that followed always found the document already loaded
        and the set could never hold two. The ratified delta names exactly three
        selection routes and a docs-row selection is not one of them, so a
        selection now moves the abstract above it and the tile's LOAD verb binds.
        `selectDocument` and its unsaved-edit guard are kept and still reached for
        the one transition that DOES replace content — filling a reserved slot
        that is still unbacked — which is the delta's own prediction that the
        guard is "unchanged WHERE IT STILL APPLIES" and never extended to
        selection.
      **THE TRADE THIS MAKES, recorded rather than glossed (PR #207
      re-verification, N4 — WITH BRETT).** Under the released v1 envelope the
      chat's DOCUMENT binding is pinned to the mount-time reserved slot once that
      slot is backed: no route re-points it, because the envelope carries exactly
      the outline plus that one slot and nothing may empty it (N3). Phase A DID
      allow a row-selection swap of which document the chat was about, so this is
      a **user-visible reduction**, accepted here as a stated interim posture —
      a human can load and edit any number of documents and Save each, and the
      chat states plainly when it cannot be bound to one, but it cannot be
      re-pointed at a different document within a session. It ends either with
      §13's widened envelope (which carries N documents and a declared bound-buffer
      key, retiring the limit entirely) or sooner, if Brett rules that a
      CLEAN reserved slot may be re-pointed. Selection semantics are NOT changed
      here pending that ruling.

## 9. Threads

- [x] 9.1 The thread sidecar file: one per loaded document, on the session
      branch inside the session worktree, with the structured state header above
      the transcript and the `authority`/`regenerable_from` fields written into
      the file (design §4.1).
      Realized in `scripts/ideation_dashboard/doxbench_threads.py`, pinned as a
      golden render with a byte-identical render/parse round trip. The path rule
      MIRRORS the document's own repository-relative path under
      `ideation/dashboard/session-threads/`, reversibly, so two `README.md`
      files in different folders never merge two conversations.
      `render_state_header` is a literal PREFIX of the file, so a packet can
      carry other threads' headers without their transcripts.
      **Task 3.5's verified finding is realized** (`verification-findings.md`
      §3.5): the harness's own artifact store lands OUTSIDE the git worktree, so
      an `artifact://` pointer in a sidecar would never resolve for a colleague
      who fetched the shared branch. A turn body carrying one is therefore
      REFUSED at construction — absolutely, with no flag and no strict-mode
      switch — and both of the finding's remedies exist:
      `dereference_bodies(..., dereference=...)` resolves the content through a
      seam the §11 bridge supplies (a half-resolving seam cannot slip a survivor
      through, because its answer goes straight back through the same refusal),
      and `elided_note(bytes, reason)` records the FACT and the size where
      inlining is infeasible. `mirror_turn` needs no check of its own: a turn
      holding a pointer cannot exist to be handed to it.
- [x] 9.2 Threads commit WITH the document's Save through the existing
      one-commit-per-gate-action path, so a thread and its document cannot land
      in separate commits.
      **SEAM LANDED at §9, ROUTE WIRED at §11.** `thread_commit_paths` is now
      CALLED: `gate_routes.execute_first_edit` injects it into
      `branch_session.commit_first_edit` as `thread_paths_for`, and the
      transaction adds the sidecar to the DECLARED path set
      `_commit_gate_action_locked` already commits as exactly ONE commit. That
      function is untouched, and `write_thread(gate, thread)` is still the only
      write route. Proven against REAL git: a turn writes a sidecar into the
      session worktree, the next Save's commit carries the document, its
      gate-action record and the sidecar together, and a Save with no sidecar
      written commits exactly what it always did.
      **Judgement call, flagged (the seam, not a computed list).** The route
      passes the FUNCTION rather than a computed path list, because the sidecar
      path must be derived from the NORMALISED document path the transaction
      settles on (`verdict.document`) — the path the turn's own mirror wrote
      under. Deriving it at the route from the caller's spelling could name a
      different file, and a Save that declared a path nothing wrote would refuse.
      **Judgement call, flagged (only a DIRTY sidecar joins).**
      `_commit_gate_action_locked` refuses any declared path that is not dirty
      ("already committed on this branch"), so declaring a sidecar no turn has
      touched since the last Save would refuse EVERY Save on a tile whose thread
      had not moved. The filter is therefore load-bearing rather than an
      optimisation, and it is stated where it is applied.
- [x] 9.3 Compaction preserves the header's commitments; a compaction that drops
      an open question, decision, accepted fact, evidence ref or pending action
      fails a test rather than a review.
      `compact_thread` is lossy over the TRANSCRIPT and a RAISE over the header:
      the refusal names the class and the item, each of the five classes is
      pinned separately, and the ACTIVE GOAL is treated as a sixth class —
      a strengthening past the delta's enumerated five, stated as such.
- [x] 9.4 Threads are excluded from the session pull request's promotion by
      default, and the promotion route for a finding is an existing lifecycle
      verb with provenance. No parallel decision store exists anywhere in the
      realization.
      DECLARED as `promotion_excluded_prefixes()` plus its stated reason, which
      the §12 verb consults. The negative is asserted rather than described:
      nineteen forbidden source spellings and a public-surface check prove there
      is no `promote*`/`publish*` name, no parallel store, and no write or push
      route of the module's own.
- [x] 9.5 Thread routes live inside the serve's declared write allowlist (the
      interactivity boundary), are loopback-only, fail closed on an unresolved
      actor, and are absent without the gate capability and on the hosted plane.
      **ALLOWLIST AND POSTURES LANDED at §9, ROUTE LANDED at §11.**
      `gate_routes.first_edit_gate_factory` — doxBench's governed Save — DECLARES
      the thread prefix, without which the boundary refuses the sidecar as
      `outside-allowlist`; no other gate widens, and a test asserts the prefix
      appears exactly once. The WRITE goes through that gate and no other:
      `serve._mirror_turn_into_sidecar` builds it through the factory rather than
      beside it.
      `GET /workbench/thread` is the read route, and all four clauses are
      answered in order by `doxbench_threads`' own capability rule rather than by
      a second copy of it: not loopback → the hosted-plane cause; no gate
      capability or no resolved actor → the no-gate-capability cause; a
      non-console caller → the existing fixed `console_required`; a scope with no
      live session → the same declared absence, never an oracle about which refs
      or tiles exist. The read is confined by `resolve_within`, the same
      containment authority `/source` uses, so a traversal-shaped document name
      answers "no thread" rather than another tree's file.
      **CORRECTED 2026-08-19 (adversarial review P2-10): session-ness came from
      two ADVISORY fields.** `_session_worktree_for` gated on
      `session_tile or session_base`, and `snapshot_registry` documents both as
      advisory — `session_tile` is "None on a bootstrap-reconstructed entry" and
      `session_base` "degrades ... advisory ... **and never the reason a session
      fails**". This route made them exactly that, and the consequences were
      silent: no threads in the packet, NO MIRRORED RECORD with nothing on the
      wire saying so, and a 403 from the thread route. It was also the one
      method no test executed — every route test overrode it. It now asks
      `branch_session.live_session_branches`, the liveness authority the Save
      path itself trusts and which the turn route already calls one step
      earlier, and four tests drive the REAL method against a real git session,
      including the bootstrap-reconstructed entry that used to lose records.
      **CORRECTED 2026-08-19 (PR #223, Copilot CP1), both halves.** (1) An
      unresolved actor borrowed the no-gate-capability cause — a true sentence
      about a different situation, since the plane HAS the capability and there
      is simply no identified human to attribute a gate action to. It has its
      own `NO_RESOLVED_ACTOR_CAUSE` now. This is precisely the class this
      slice's own P3-19 fixed for the no-live-session branch, missed one clause
      over, which is worth recording as such. (2) The wire's `cause` field
      carried `thread_capability_absence`'s full `"<REASON> — <cause>"` string
      while the body already carries the reason in its own field, so the reason
      appeared twice and `cause` was not a cause; the route reads
      `ThreadCapabilityAbsent.cause` directly now. Every declared cause is a
      bare cause, and a test asserts the reason never appears inside one.
      **NOTED (re-verify N-6):** the liveness question now has ONE spelling —
      `doxbench_scope.is_live_session_ref`, beside the other consumer of the
      same question. `serve.py`'s copy had already diverged from it in two ways
      (raw vs normalised ref comparison, bare `Exception` vs `SessionRefused`),
      and the shared one keeps the safer reading of each: normalised refs, so
      `refs/heads/draft/x` and `draft/x` are one branch; and the NARROW catch,
      which is a judgement call — a declared branch-layer refusal answers "not
      this tile's session", while a genuine defect propagates instead of being
      reported as an honest absence.
      **NOTED (adversarial review P3-19):** the "no live session" branch now
      answers its OWN cause rather than borrowing the no-gate-capability one,
      which was a true sentence about a different situation. It stays generic,
      so the route is still no oracle for which refs or tiles exist.
      **Judgement call, flagged (the wire shape).** The thread body is an
      UNVERSIONED console-internal JSON shape, like `/capabilities`, and
      deliberately not a released envelope: no openxFactory schema declares a
      thread, and minting a `schema_version` here would claim a release nobody
      cut. The governed artifact is the sidecar FILE, which carries its own
      `schema_version`, `authority` and `regenerable_from`.
      **Judgement call, flagged (a new error code).**
      `thread_capability_unavailable` (403) joins `DOXBENCH_ERROR_CATALOG`'s
      closed set, in the packet pair's own pattern: the released failure
      envelope's `error` is a free-form pattern string rather than an enum, so no
      contract change was needed, and reusing `model_capability_unavailable`
      would name a different absence while `turn_scope_refused` would blame the
      scope for a capability verdict.

## 10. The knowledge service v1

- [x] 10.1 The internal ASSEMBLY PORT: the product-neutral surface a retrieval
      backend implements, with the v1 local-hybrid profile behind it (lexical +
      small embedded vectors + the structured thread-states). No graph engine,
      anywhere.
      `scripts/ideation_dashboard/doxbench_knowledge.py`. Four product-neutral
      members (`profile`/`index`/`retrieve`/`source`), pinned as an EQUALITY
      with a `FORBIDDEN_ASSEMBLY_PORT_MEMBERS` companion in the same shape
      `WorkbenchModelPort`'s is, and DELIBERATELY not the tool names: one
      vocabulary for both layers would make a backend swap look like a boundary
      change the first time they had to differ.
      The v1 profile is in-process and stdlib-only: BM25 over the confined
      corpus, plus a deterministic hashed token/character-trigram projection
      (96 dimensions, `hashlib.blake2b` rather than the per-process-randomized
      `hash()`, so two independently built indexes rank identically), plus the
      structured thread-states as a third signal — fused on declared weights
      summing to one, with ties broken on the ref. Each of the three signals
      has a test showing it selecting something the others cannot.
      **N-GRAM OFF-BY-ONE FIXED (Copilot review of PR #216).** The strict
      length comparison skipped the single n-gram of a token exactly
      `CHARACTER_NGRAM` long, so every three-letter token contributed NO n-gram
      feature while four-letter tokens contributed two — contradicting the
      function's own docstring and weakening the vector leg precisely for the
      short tokens the lexical leg generalizes over worst. The pin is on the
      feature ENUMERATION rather than on a score, and both score-coupled
      scenarios were re-derived rather than tuned: the null query still yields
      zero on both textual legs, and the vector-leg case still fires with
      `lexical == 0`.
      No graph engine, store, or index: `ProviderProfile` REFUSES a profile
      declaring `graph`, and eleven engine/candidate spellings are asserted
      absent from the module's source.
- [x] 10.2 The ONE tool boundary: `search`, `get_source`, `promote_finding`,
      `reindex`, with `graph_query` RESERVED and unimplemented (a test asserts
      it is unimplemented). *(The line read "The MCP boundary" until the
      adversarial review's F10; the delta says "exactly ONE tool boundary" and
      never says MCP, so the heading is aligned with the note below rather than
      left contradicting it.)*
      `KnowledgeToolBoundary`, dispatching through a FIXED table rather than
      `getattr`, so a caller cannot reach a private helper by naming it and the
      reserved name answers from the same table. `graph_query` is IN
      `declared_tools()`, is NOT an attribute of the boundary, and refuses with
      a fixed governance reason naming the graduation trigger — not a
      `NotImplementedError`, not a missing name, and a different exception class
      from an undeclared name, because a typo must never read as a governance
      verdict.
      `promote_finding` writes nothing and stores nothing: it returns a request
      naming the reviewed act, read from this surface's own `memory-gateway`
      declaration so "how a finding becomes durable here" has ONE spelling. An
      unattributed finding is refused.
      **IT IS AN IN-PROCESS BOUNDARY (adversarial review, F10).** The ratified
      delta asks for "exactly ONE tool boundary declaring a small tool
      contract" and never says MCP; an earlier docstring here called it "the
      MCP tool boundary", naming a protocol nothing in this slice speaks. The
      requirement is satisfied by the boundary being one and being small, not
      by its transport. **OWED AT §11:** the stdio MCP server that exposes
      these same four tools to the harness, and the mount-name pin
      `verification-findings.md` §3.2 asks for
      (`xd://mcp__<server>__<tool>`) — §11 is the first slice with a harness to
      expose them to, and until then no test can assert a mount name nothing
      mounts.
      **DISCHARGED AT §11** (`scripts/ideation_dashboard/doxbench_mcp.py`): the
      stdio MCP server implements `initialize`, `tools/list` and `tools/call`
      per the MCP 2025-03-26 spec in front of the SAME `KnowledgeToolBoundary`
      — not beside a second one — and the four mount names are pinned STRING
      FOR STRING — and CORRECTED 2026-08-19 to the SINGLE-underscore form the
      harness actually mints: `xd://mcp__doxbench_search`,
      `xd://mcp__doxbench_get_source`, `xd://mcp__doxbench_promote_finding`,
      `xd://mcp__doxbench_reindex`. Confinement travels WITH the mount:
      a server process serves ONE tile's confined set, declared in a manifest
      the bridge writes beside the registration, so a mount cannot be talked
      into another tile because the refs it could name are the only ones it was
      ever given. The two verdicts stay apart on this transport exactly as they
      are in-process — `graph_query` answers with the boundary's fixed
      governance refusal, an undeclared name answers as unknown — and
      `graph_query` is NOT listed in `tools/list`, because a mount that always
      refuses is a tool the model spends system-prompt budget reading about and
      can never use. `reindex` rebuilds from the MOUNT's own manifest and takes
      no sources from the caller, since a reindex the model could supply
      sources to would put material outside the tile's staged set INSIDE the
      confinement. Registration is written BEFORE the child starts, which is
      the whole guarantee on offer: MCP discovery is asynchronous, and a turn
      that races it degrades to design §3.4's reduced-packet posture — the
      correct fallback already specified, so no wait-for-discovery mechanism
      was invented.
      **NOTED, not fixed (adversarial review P3-18):** `promote_finding`'s
      `provenance` refs are NOT confined to the mount's manifest — a caller can
      name a ref outside the tile's staged set and see it echoed back in the
      returned request. This is a note rather than a defect because
      `promote_finding` WRITES NOTHING and STORES NOTHING: it returns a request
      naming the reviewed act, and the human performing that act is the gate
      that would notice an unrelated provenance. The confinement claim the
      boundary makes is correctly scoped in its own docstring to `search` and
      `get_source`, both of which ARE confined and tested. Confining provenance
      too would be a real strengthening; it belongs with whoever gives
      `promote_finding` a durable consumer, and it is recorded here so that
      slice inherits it rather than rediscovering it.
      **THE MOUNT SEPARATOR: SETTLED 2026-08-19, AND THE FIRST READING WAS
      WRONG** (adversarial review P1-2). `verification-findings.md` §3.2 stated
      the convention twice and the two disagreed — its PROSE wrote
      `xd://mcp__<server>__<tool>` (DOUBLE underscore), its own EVIDENCE wrote
      `xd://mcp__verify_echo_echo` and `xd://mcp__sonarqube_*` (SINGLE). This
      realization took the prose. The EVIDENCE was right: `createMCPToolName`
      (`packages/coding-agent/src/mcp/tool-bridge.ts:345-358`, v17.3.7) returns
      `mcp__${sanitizedServerName}_${normalizedToolName}`, and
      `sanitizeMCPToolNamePart` collapses `_+` to `_`, so a double separator is
      not merely unused — it is UNPRODUCIBLE. Re-confirmed LIVE by registering
      this slice's own server as `doxbench` against a real `omp --mode rpc` and
      reading the four names out of the running system prompt.
      `verification-findings.md` §3.2 now carries a dated correction note at
      the source. The one-constant isolation did its job — the fix was one
      character plus three pinned test strings — and the test now pins against
      a re-implementation of the harness's OWN composition rather than against
      four literals, so the next rename is checked against the rule.
      **NOTED:** `mount_name` also REFUSES a server or tool name the harness's
      sanitiser would rewrite (a digit, a hyphen, a capital), because such a
      name mounts under a different string than it is spelled with and a pin
      that did not know that would pin a lie.
- [x] 10.3 The packet assembler: selection rail, then the lifecycle-status
      exemption rail keyed on each item's `Status:` header, then the bounds
      check, then deterministic assembly (design §3.1). Both rails run before
      any retrieval or provider I/O, and a refusal discloses no packet content.
      `scripts/ideation_dashboard/doxbench_packet.py`. The CONFINEMENT is
      computed first and HANDED to the retrieval boundary rather than left for
      it to respect — a recording boundary reports what it was given, so the
      ordering is a fact about a call rather than a comment — and the
      assembler re-filters the provider's answers against it anyway.
      The exemption rail reads each item's own `Status:` header IN THE
      ASSEMBLER and marks the item; the marking travels with it, upstream of a
      layer-three compressor that does not exist yet and cannot be delegated to
      one. The read is cross-checked against the repository's own
      `doc_health.corpus.parse_status` over real documents, because the same
      rule living in two places is how two places drift.
      The bounds rail has TWO ARMS, and the difference between them is layer
      one's fidelity contract (**adversarial review, F2 — the first version of
      this rail had only the second arm**):
      (a) EVIDENCE is what retrieval SELECTED, so an oversized packet FITS by
      selecting less — evidence is walked best-ranked first and kept while it
      fits the remaining budget, and every dropped ref is NAMED in the
      declaration. That is lossless-by-reference, not truncation: no source is
      ever shortened, and what is dropped stays one retrieval call away.
      Dropping strictly from the tail was the obvious alternative and is worse
      — one oversized top hit would evict every smaller item behind it.
      (b) THE THREADS are not selected and appear nowhere else, so if they
      alone exceed the bound the packet REFUSES with the measured dimension.
      That refusal is actionable: layer two exists to compact a thread.
      **The wire codes are two RECORDED judgement-call spellings**, not a reuse
      of `request_limit_exceeded` — which said "the request exceeds the allowed
      size for this route" about a few-hundred-byte request whose oversize was
      server-selected evidence, and refused every turn on that tile forever.
      The released failure envelope's `error` is a free-form pattern string,
      not an enum, so `context_packet_bound_exceeded` (409, carrying the
      dimension, message naming the compaction that fixes it) and
      `context_packet_invalid` (500) needed no contract change.
      **THE PACKET'S BOUND COMPOSES WITH THE MODEL'S (Codex review of PR #216,
      CODEX-B).** The request bytes are measured against the catalog entry's
      effective input limit BEFORE the packet exists, and the packet's sections
      are appended after — so an accepted turn could dispatch a prompt past the
      model's declared capacity and fail at the PROVIDER rather than at a
      measured bound. The route now passes the REMAINING budget (the limit,
      minus the measured request, minus a declared scaffold reserve for what
      the prompt spends outside both) as the packet's bound, and the fit
      carries what fits. Fitted rather than refused, for the same reason F2
      recorded; the genuinely-unfittable case still refuses through the 409
      arm. The reserve's adequacy is MEASURED against real rendered prompts at
      three ceilings rather than asserted.
      **THE 409 ARM'S REACHABILITY, CORRECTED AT §11.** When this task shipped
      the route supplied NO threads, so the only thing that could exceed the
      packet's bound was evidence — which the fit selects away rather than
      refusing — and the arm could be reached only by injecting an assembler
      that put a thread in. That was recorded honestly as a synthetic pin. §11
      wires the route to the session's own sidecars, so the arm now has a REAL
      route test: a thread larger than what the model's declared ceiling leaves
      refuses with `context_packet_bound_exceeded`, the measured dimension
      `context_packet_bytes`, nothing dispatched and no thread content in the
      body — with a control test proving the identical sidecar under a generous
      ceiling still answers 200, so the refusal is about the BOUND rather than
      about threads being present.
      **RAILS-BEFORE-PROVIDER, STATED PRECISELY (CODEX-A, refuted).** Codex
      read design §3.1 as requiring that no provider be touched until after
      selection, and asked for a reorder. The design does not read cleanly on
      this point — step 2's own box CONTAINS "evidence: knowledge service
      search" while the prose beneath says steps 2–3 run before any provider is
      reached — and the reorder is not a stricter reading but an incoherent
      one: it would mean selecting evidence before knowing what evidence
      exists. The implementation takes the reading that preserves what the
      rails are FOR, and now SAYS so where the claim is made rather than only
      where the code is: the rail that governs the retrieval provider is the
      CONFINEMENT, computed first and handed to it; selection, the exemption
      and the bounds fit all precede the MODEL provider; and the index the
      provider searches is a SUBSET of the confinement by construction, which
      is now asserted by a test rather than argued.
      **THE LEASH IS PULLED (F1).** `require_valid` had ZERO production call
      sites: a packet issued for another repository, another tile, or an
      expired turn rendered into the prompt unexamined. `build_prompt_envelope`
      — the consuming surface — now revalidates purpose, scope and expiry
      BEFORE assembling any section text, on the SAME injected clock the packet
      was issued on. At the route the delta's own words are realized literally:
      a rejected packet makes the route REQUEST A NEW ONE, and only a second
      failure refuses.
      **EXEMPT-STATUS JUDGEMENT CALL, flagged (accepted by the adversarial
      review).** The delta says "approved or ratified". This repository's
      lifecycle spells the approved end `ratified` AND `standard`, and the
      source-ranking hierarchy this same change ratified ranks "ratified or
      standard canon" together at the top, so exempting `ratified` while
      compressing `standard` would compress the most authoritative material
      this surface has. `EXEMPT_STATUSES` is therefore
      `{approved, ratified, standard}` — where `approved` is FOREIGN-CORPUS
      TOLERANCE and not a fourth local status: it is not in this repository's
      lifecycle vocabulary and a corpus-wide grep finds ZERO documents carrying
      it, so it is honoured for a corpus that does use the word and recorded as
      tolerance so no reader mistakes it for a status this repository issues.
      A DECORATED status (`ratified (2026-08-01)`, `record · …`) keeps its
      status word: the corpus already carries decorated forms, and a decorated
      `ratified` would otherwise lose its exemption silently.
- [x] 10.4 The packet declares purpose, sources with refs, bound scope and
      expiry, and is rejected for another purpose, another scope, or after
      expiry.
      `ContextPacket` + `require_valid`, with a test per rejection axis and a
      declaration section that renders the purpose, the scope, the expiry, the
      retrieval provider profile, and every source with its ref, its own
      `Status:`, and its exemption verdict. Expiry is compared against an
      INJECTED clock (`time.monotonic` by default), the same discipline
      `dispatch_turn`'s deadline uses.
- [x] 10.5 Evidence is confined to the tile's staged set plus promoted findings;
      a retrieval that would return anything else is excluded, and a retrieved
      document never joins the loaded set.
      `confined_refs` reads `projection.context_paths` — the tile's own staged
      set — plus the promoted findings the caller names. Confinement governs
      the SOURCE FETCH as well as the search, because a confinement that
      governed one and not the other would be none at all. A rogue backend
      answering outside the set has its answer dropped at the assembler and is
      never even fetched.
      "Never joins the loaded set" is asserted through the STATE AUTHORITY, not
      only through the packet: the assembled prompt's buffer sections still
      enumerate exactly the buffers the request supplied, both at the assembler
      and through the real serve, and the assembler's source contains no buffer
      type and no state-route spelling.
      **RECORDED, not deferred:** the promoted-findings set is EMPTY at the
      route today, and deliberately — reading a promoted-findings register
      would mean BUILDING one, which is the parallel decision store the
      contract forbids. A finding becomes promoted only when a human performs
      the reviewed act that creates the target object.
      **CORRECTED (adversarial review, F5).** The first version of this note
      justified the empty set by claiming the created object "is then an
      ordinary document of the tile which the staged set already carries."
      That is FALSE for the case that matters: a `create-document` gate action
      writes into the SESSION WORKTREE, while the retrieval corpus is read from
      the SERVED CHECKOUT, so a freshly created finding is confined-but-
      unindexable — `resolve_within` finds no such file and it is skipped. The
      empty set is right for the reason above (no register may be built), NOT
      because the staged set already covers it, and the packet now states which
      bytes its evidence is so no reader concludes otherwise.
      **THE SAME BOUNDARY, stated in full:** evidence is the served checkout at
      `projection.source_revision`. A document the session has SAVED is
      therefore eligible evidence at its PRE-SESSION bytes, and one the session
      CREATED is not eligible at all. The packet declares both facts. Reading
      the session worktree instead is not a silent fix — it would put unmerged
      session text into the corpus lane that the confinement rail governs — so
      it is left to the slice that owns session-aware retrieval rather than
      taken here.
- [x] 10.6 The retrieval backend is read from an install-time declaration; no
      runtime, per-turn, prompt-driven or heuristic selection path exists.
      `RetrievalBackendDeclaration` enforces the ratified two-case principle:
      a self-hosted install declares `local-embedded`, and a hosted backend is
      declarable only by a TENANT install — which v1 then refuses to build,
      naming the gap, rather than falling back to a local backend nobody
      declared. `build_server` takes the declaration and the two production
      entrypoints (`serve()` and the CLI's generate-and-open) make it
      explicitly, the same discipline `real_notebook_adapter` carries.
      The negative is CONSTRUCTIVE: `build_backend`'s signature has exactly one
      parameter, so there is no turn, prompt, or heuristic to pass it, and a
      test asserts that against `inspect.signature` rather than against a
      comment; the route's own source is asserted free of every
      per-turn-selection spelling.
      The backend INSTANCE is built per request from the process-wide
      declaration: the server is threaded, and one tile's derived index must
      never be visible to another tile's turn.
      **THE ASSEMBLER SEAM IS GUARDED (re-verify NF6).** `packet_assembler` is
      injectable — it is what makes the packet leash testable end to end — and
      it carries the governance rails, so a swapped assembler bypasses the
      confinement, the exemption and the bounds fit while still passing the
      leash. It therefore gets the guard `knowledge_declaration` has: a server
      built with no kwarg is asserted to bind the REAL assembler, and neither
      production entrypoint may pass the argument at all (asserted against the
      `build_server` call sites' own AST, not against a grep).
      **THE INDEX BOUND IS STATED, NOT SILENT (adversarial review, F6).** The
      index carries a declared bound (`MAX_INDEXED_SOURCES`) and the
      confinement does not, so a tile with more documents than the bound has
      refs that are confined but were never indexed. That was the exact
      "silently shortened" class the bounds rail's own docstring forbids, and
      it falsified the packet's "one retrieval call away" note. The packet now
      DECLARES coverage — indexed of confined — and says in as many words that
      the uncovered remainder was not retrievable this turn. Stating it was
      chosen over refusing past the bound because refusing would reproduce
      exactly the un-actionable, permanent per-tile refusal F2 just removed;
      the ratified text asks for bounds to be visible, and a stated shortfall
      is visible in the one place the reader of the context is looking.
      **AND THE BOUND IS ON WHAT IS INDEXED, NOT ON WHAT IS ATTEMPTED (Codex
      review of PR #216, CODEX-C).** The slice ran BEFORE the readability
      filter, so an unreadable entry consumed index capacity and readable
      documents behind it were never considered — reproduced at a bound of 2
      over three paths: ONE indexed — and the coverage line then blamed "the
      declared index bound" for an omission the bound had nothing to do with.
      `CorpusCoverage` now keeps the two omission classes apart:
      unreadable-at-this-revision versus beyond-the-bound, since the first
      stays absent until someone fixes it and the second would return under a
      larger bound.
- [x] 10.7 Degraded posture: no knowledge service → the declared reduced packet
      with the posture stated, no unbounded substitute, no rail bypass, editors
      unaffected.
      **PACKET HALF LANDED, SURFACE HALF GATED** — half-open in the same shape
      task 5.4 carried, because half of this requirement genuinely is not
      built.
      The reduced packet is the SAME pipeline with one input absent, not a
      second pipeline with the rails skipped — a test drives a bounds refusal
      through it to prove that. A `ContextPacket` cannot be reduced without
      stating its reason, and the reason says in as many words that nothing
      unbounded was substituted and no rail was bypassed.
      INDEPENDENCE is proven through the real serve: a live model with no
      knowledge service SUCCEEDS with a reduced packet rather than refusing,
      and a live knowledge service with no model leaves the route's
      model-capability refusal shape and gate order byte-identical and leaks no
      evidence into it. The success envelope is the same with and without.
      **OBLIGATION RECORDED AGAINST THIS TASK, in §11.7's pattern.** The
      reduced posture is STATED in the assembled context, which is where the
      ratified sentence puts it, and the packet half is done. What is NOT done
      is the posture being visible to the HUMAN on the surface.
      `workbench-chat-turn-v2-success` is a CLOSED envelope
      (`additionalProperties: false`) with no field for a context posture, so
      no conformant success body can carry one today, and the delta's own rule
      forbids carrying it as a server-side value no reader can consult. This
      task therefore needs its OWN contract release — **an additive
      chat-turn-success growth carrying the assembled context's posture
      (`full | reduced`) and its reason, allocated at ITS realization under
      `docs/contract-versioning-policy.md`, exactly as contract-v1.34 was
      allocated at §13's** — before the ratified "with the reduced posture
      STATED" clause can be claimed as visible rather than only as assembled.
      Until then the gap is stated rather than papered over.
      **CORRECTED (adversarial review, F3):** an earlier version of this note
      claimed the obligation was "recorded against the release that will carry
      it" and cited §13 and §11.7 as precedents. Both citations were wrong. §13
      is CLOSED and shipped and carries nothing forward; §11.7 records its
      obligation by naming its OWN future release and staying open — which is
      what recording looks like, and is what this task now does.
      **SURFACE HALF LANDED 2026-08-22 — `contract-v1.39`, and the box is now
      CHECKED because the ratified `The knowledge service is unavailable`
      scenario is claimable in full.** Its THEN is that the turn "MUST degrade
      to the declared reduced packet with the reduced posture stated", and the
      half that was missing was never the degrading — it was that the posture
      was stated only where no reader and no human could consult it.
      `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml` grows ONE
      OPTIONAL property on `$defs/success_v2`, `context_packet`, referencing one
      new CLOSED `$def` with two members: `posture` (`full | reduced`, required)
      and `reduced_reason` (`minLength` 1, `maxLength` 500 — code points, which
      the producer's own guard shadows with the stricter UTF-8 byte count),
      present IFF the posture is reduced.
      ADDITIVE by construction and verified case by case against the released
      bytes: the key is optional, so the pre-release record shape still
      validates — a packaged instance whose INSTANCE bytes are unchanged (only
      its header comment grew) IS that proof — and
      `contract_schema_version` stays 1 with the manifest row's `schema_version`
      beside it.
      The PACKET'S ASSEMBLY was not rebuilt, which was the point:
      `assemble_packet` and both `REDUCED_*` reasons are byte-identical to what
      §10 shipped, `tests/ideation-dashboard/test_doxbench_packet.py` is
      unmodified and still green, and the release reads the packet rather than
      re-deriving anything the packet already knows.
      **ONE LINE OF `ContextPacket` DID MOVE, and an earlier version of this
      sentence said none did (review N-1).** The bot round tightened the
      CONSTRUCTION gate's full-arm predicate from truthiness to presence
      (`self.reduced_reason is not None`) — one predicate, no other byte of the
      type or the module. It is not a carve-out from "not rebuilt", it is the
      cost of the three-gates-one-rule claim being TRUE: the released shape
      forbids the field's presence on a full posture, and a type that forbade
      only a useful value did not assert the same rule.
      `serve.doxbench_context_packet` is the ONE derivation, beside
      `doxbench_selected_model` and on its precedent, and it runs INSIDE the
      route's existing packet boundary so its refusals land on the fixed
      `invalid_turn_request` every other structural packet refusal uses. Four
      lying-assembler cases go through the injected `packet_assembler` seam —
      reduced-with-no-reason, full-carrying-a-reason, an unknown posture, and no
      posture at all — and each refuses with nothing dispatched. A defaulting
      derivation would have shipped a record claiming a full context for all
      four.
      THE SURFACE, which is the half this task was open for. The rail renders
      one live-announced note under the transcript — `reduced context: <the
      reason>` — for a turn that ran reduced, and nothing at all for a full one.
      **AND THE WORD "LIVE-ANNOUNCED" WAS NEARLY FALSE (adversarial review S1).**
      The note was written and THEN un-hidden, so the text mutation happened
      while the node was still out of the accessibility tree and no live region
      observed it; the `aria-live` attribute read `polite` either way, which is
      why the probe's attribute assertion could not catch it. The order now
      matches the failure note beside it — un-hide first, then write — and the
      probe pins the ORDER by recording `hidden` AT THE MOMENT of the write,
      which is the only observation that tells the two apart. `styles.css`
      states the same rule in writing one region over.
      **AND THE LIVE REGION IS NOT RE-ANNOUNCED (review NEW-3).** `render()` runs
      on every composer keystroke, and re-writing a live region with the SAME
      sentence re-announces it: the reviewer measured seven repeats of the same
      227-character disclosure while typing one follow-up. The note is written
      only when its text actually CHANGES, and a probe pins the write count
      across seven keystrokes.
      `settleTurnSuccess` adopts the record's posture instead of projecting it
      away (the browser state model kept only `proposals` and `transcript`, so
      the field would have been dropped on arrival), and the three other
      answer-replacing paths carry it too, so the note never outlives the answer
      it describes and never survives one. A node probe mounts the SHIPPED
      `doxbench-chat.js` bytes and
      drives real turns through it: reduced renders the note and the reason,
      full renders nothing, a record with no posture renders no phantom badge,
      and both self-contradicting records render silence rather than half a
      statement.
      END TO END, at the REAL route and on the WIDENED lane: no knowledge
      service records `reduced` with `REDUCED_NO_KNOWLEDGE_SERVICE`; the
      declared local-embedded backend records `full` with no reason; the wire
      record and the packet's own prompt declaration are pinned EQUAL; and a
      DECLARED backend that REFUSES a retrieval records
      `REDUCED_RETRIEVAL_REFUSED` — the case an implementation that asked "did
      this serve have a knowledge service?" would get exactly backwards.
      TWO RULES ARE DELEGATED to
      `scripts/validate-ideation-dashboard-contracts.py`
      (`check_context_packet`). The pairing, which the shape also expresses and
      which is RESTATED on purpose — §11.7's F2 found a file gate strictly
      weaker than the type gate beside it while claiming parity, so THREE gates
      now assert this one rule (the two conditionals,
      `ContextPacket.__post_init__`, and the validator) and a test asserts they
      AGREE on the packaged corpus. And the credential/endpoint spelling scan
      over `reduced_reason`, which the shape CANNOT express: it is the release's
      one new free-prose field, and its packaged negative is structurally
      perfect, so the shape must not catch it — that is what makes it the rule
      worth delegating.
      **AND THAT SECOND RULE IS A LINT, NOT A GUARD (review N1).** The
      credential/endpoint patterns are spelling heuristics over free prose and
      miss in both directions — they refuse innocent text saying `api_key` and
      pass a real token shaped unlike their patterns. Kept, because it raises
      the cost of a careless paste and catches the obvious shapes; reworded
      everywhere it was called a guard, because a clean scan establishes
      nothing. The structural protection is that this producer's reasons are
      MODULE CONSTANTS rather than formatted provider errors, so no value flows
      into the field for a scan to have to catch.
      FIVE PACKAGED NEGATIVES, each failing at the gate that owns it and the
      table recording WHICH: reduced-without-reason and reason-on-full (shape +
      delegated `context-packet`), an unknown posture and a fourth field on the
      closed object (shape alone — the validator restates neither an enum nor a
      closure), and the leaking reason (delegated alone). Two positives beside
      them, and the unchanged pre-release record as the third shape.
      **THE CEILING IS ENFORCED WHERE THE REASON IS CARRIED — corrected at
      adversarial review (S2), which found the claim that it already was to be
      FALSE, in released bytes.** The schema comment said "the producer's own
      guard checks the stricter UTF-8 BYTE count"; no such guard existed
      anywhere. Reproduced through the real route against the RELEASED
      validators: a 500-code-point CJK reason (1,500 UTF-8 bytes) was SERVED
      200, and a 501-code-point reason answered 502 `response_invalid` with
      `dispatch` ALREADY COUNTED — a provider call paid for and the human's
      answer produced and thrown away.
      Three fixes. The schema comment now says what is true (the unit is CODE
      POINTS, so 500 CJK characters is conformant at ~1,500 bytes and a consumer
      sizing a buffer must size it in bytes). The constants test's docstring,
      which called the ceiling "500-byte", now names its unit and says why it
      uses the STRICTER byte count on text this repository authors. And
      `serve.doxbench_context_packet` gained the bound itself, in CODE POINTS so
      it refuses exactly what the shape refuses and no conformant record more —
      pre-dispatch, on the route's existing packet boundary, which also covers a
      `REDUCED_*` constant added later that nobody thought to hold to the bound.
      `CONTEXT_REDUCED_REASON_MAX_LENGTH` is pinned to the released `maxLength`
      by a test, on `MAX_ROUTING_TARGETS`' precedent. Nothing is truncated:
      truncating a statement about a degradation is how a degradation goes quiet.
      **AND A TENSION RECORDED RATHER THAN RESOLVED**: all four refusals in that
      function have SERVER-AUTHORED causes and none is caller-fixable, which is
      exactly the class the route's `context_packet_invalid` (500) arm exists for
      and says so ("never a 4xx blaming the turn") — yet they answer
      `invalid_turn_request` (400). They are kept on one code because one
      function should have one refusal shape and all four are unreachable in
      production; moving the whole function to the 500 arm is a named follow-up,
      not something smuggled into a fix pass that four tests pin.
      **A SECOND FOLLOW-UP, NAMED AND DELIBERATELY NOT CODED HERE (review, last
      note).** `adoptContextPacket` applies NO length bound to a RESTORED
      reason, so a tampered browser-local snapshot renders a note of arbitrary
      length — the reviewer's instance was 200,000 code points. It is neither a
      security nor a correctness defect: the blob is browser-local and
      per-viewer, so the only party who can tamper with it is the person who
      would then read it, and nothing it produces reaches the wire, the server,
      or another viewer. The fix is one line
      (`reason.length <= CONTEXT_REDUCED_REASON_MAX_LENGTH` in the adopter) and
      it belongs to the slice that touches this function next; adding it in a
      round whose whole purpose was closing NAMED review findings would be
      exactly the unreviewed drive-by this discipline exists to prevent.
      THE ORIGINAL HAZARD NOTE STANDS: the route self-validates every success
      body and answers
      `response_invalid` if the schema refuses it, so a reduction reason longer
      than the released ceiling would turn a degraded-but-successful turn into a
      refusal —
      on the one path nobody exercises by hand. A test reads the bound OUT OF
      THE SCHEMA and checks every `REDUCED_*` constant against it. Nothing is
      truncated to fit; truncating a statement about a degradation is how a
      degradation goes quiet.
      THE TAG IS NOT CUT HERE. Per the versioning policy the annotated
      `contract-v1.39` tag is published against the commit that actually lands,
      so this tick claims the CHANGELOG entry (the availability test), the
      recomputed manifest digest, the bundle bump and the 190-entry digest
      inventory built AFTER that bump — `verify-commit --commit HEAD` passes on
      the cut, exactly four digests moved — and the consuming repin carries the
      `unpublished:contract-v1.39` sentinel until a follow-up commit resolves
      it, exactly as 11.7 did for `contract-v1.38` and 13.3 for
      `contract-v1.34`.
      **CHECKED AT ALLOCATION, and this time the surface was clean.**
      `contract-v1.39` was available at the branch base `66140613` — CHANGELOG
      heading and bundle both read `contract-v1.38` — and
      `verify-commit --commit origin/main` PASSED there against v1.38's
      inventory, so the `HGR-RELEASE-DIGEST-MISMATCH` §11.7's tick left red on
      the v1.37 lane no longer applies. Recorded because the two preceding
      releases both found the surface broken when they got there, and the habit
      is to check rather than to assume in either direction.
      **Judgement call, flagged — ONE OBJECT, and its members carry the
      PACKET'S OWN NAMES.** The wire names are `context_packet.posture` and
      `context_packet.reduced_reason`, which are `ContextPacket`'s own two
      members, so no third vocabulary for the same fact exists. Nesting follows
      the `selected_model` `$def` one line above and buys three things: the
      present-iff rule stays LOCAL to the object that owns it instead of
      becoming a cross-field rule on a ten-key envelope; the ENVELOPE's key set
      is then IDENTICAL for a full turn and a reduced one, which is the ratified
      independence claim read on the wire — asserted by a NEW route-level test
      that drives the same widened request with and without a knowledge service
      and requires the two records' key sets to be equal, a test two sibling
      keys would have made unwritable (a reduced record would carry one key
      more than a full one), while the pre-existing equality test on the
      DEPRECATED v1 lane is untouched and says nothing about this because that
      envelope gains no key at all; and a reader consults one object rather than
      correlating two keys that could disagree.
      Two sibling keys (`context_posture` / `context_reduced_reason`) were the
      alternative and were rejected on all three counts.
      **Judgement call, flagged — THIS PRODUCER ALWAYS STATES THE POSTURE,
      INCLUDING `full`, which is the OPPOSITE of §11.7's disclosure call.**
      `doxbench_turn_v2_success_body` takes the posture as a REQUIRED argument,
      so no v2 record this repository builds can omit it. §11.7 rejected
      always-emitting for the catalog projection because there omission and
      explicit-`false` were the SAME fact and emitting changed every existing
      response's bytes for nothing. Here they are DIFFERENT facts — a turn always
      ran under some posture, and the only question is whether the producer
      stated it — so omitting on a full turn would make the posture inferable
      only by ABSENCE, which is exactly the reading this release forbids. The
      cost is stated rather than hidden: every v2 success body this server
      produces now carries one more key, as does the copy the idempotency store
      replays. NOTHING DURABLY STORES A v2 BODY (review N6 caught the earlier
      wording calling that store durable): `TurnStore` is per-process, in-memory
      and bounded. The durable record of a turn is the thread sidecar, and it
      does not carry the wire body at all.
      **Judgement call, flagged — OMISSION IS NOT A POSTURE CLAIM.** An absent
      `context_packet` means the producer predates `contract-v1.39`; it does NOT
      mean the context was full, and a consumer that needs the posture must
      treat absence as UNKNOWN. Both readings are packaged so the difference is
      instances rather than prose: the unchanged pre-release record states
      nothing, `workbench-chat-turn-v2-full-context` states `full`, and both are
      valid.
      **Judgement call, flagged — NO `dependentRequired`, deliberately.**
      §11.7's growth used one beside its conditionals and its review found the
      two guard different paths. Here `posture` is REQUIRED, so
      `dependentRequired: {reduced_reason: [posture]}` could never fire — a
      clause no revert-test can make fail documents rather than enforces. What
      IS taken from that lesson is the testing discipline: each conditional was
      reverted on its own and each has its own negative, and the case NEITHER
      conditional touches (an unknown posture, refused by the `enum` underneath
      them) has its own negative too.
      **Judgement call, flagged — THE NOTE IS RAIL-LEVEL AND DESCRIBES THE LAST
      ANSWER.** Per-turn badges in the transcript were designed and REJECTED: the
      browser transcript is restored from the SERVER'S THREAD SIDECAR on a
      document switch, and the sidecar records no posture, so a badge would be
      present on a lived-through turn and absent on the byte-identical restored
      one — a difference a reader would have to explain away. The note is
      therefore a function of THE TRANSCRIPT'S LAST ASSISTANT ANSWER, and it
      changes exactly when that answer does. A full turn shows NOTHING new, also
      deliberately: a standing "full context" badge is a line every operator
      learns to stop reading, which is exactly how the reduced one would stop
      being noticed.
      **Judgement call, flagged — WHAT THE NOTE IS KEYED TO, corrected at
      adversarial review (S4), which upheld the rail-level shape only ON
      CONDITION that this was fixed.** The first version cleared the note at
      `beginTurn`, and the reviewer broke it in one move: a reduced answer
      followed by a FAILED follow-up left the reduced answer holding the
      transcript with its disclosure GONE — the very lost-badge defect this task
      cited when it rejected per-turn badges, reappearing at rail level.
      Reproduced before fixing (`reduced answer -> note: true`; `FAILED
      follow-up -> note: false`, transcript unchanged, last assistant turn still
      the reduced answer).
      The review offered two shapes and this slice took the SECOND. Rejected:
      restoring the posture in `settleTurnFailure` — `beginTurn` would have to
      stash a value for it to hand back, and `abortTurn` and
      `recordLocalFailure` would each need the same restore, so ONE invariant
      would be re-implemented at three sites. Taken: DELETE the `beginTurn`
      clear, because a flight STARTING replaces no answer. Every path that does
      replace the answer already replaces the posture beside it — there are
      FOUR, and this enumeration said THREE until the review's second round
      (NEW-1): `settleTurnSuccess` adopts the new record's (null included, for a
      producer older than v1.39), `adoptThreadTranscript` clears it with the
      transcript, `rekeyChatState` starts fresh, and `restoreChatState` adopts
      the SNAPSHOT's. So the invariant holds by not being violated rather than
      by being restored. Both directions are probed
      (reduced -> failure KEEPS the note beside the failure note; reduced -> a
      full success CLEARS it) and both are revert-tested.
      **THE FOURTH PATH, AND THE SNAPSHOT THAT MADE IT ONE (review NEW-1 and
      NEW-2).** `restoreChatState` replaces the transcript WHOLESALE and left
      `contextPacket` untouched, so a restored answer could be captioned by a
      note that never described it — reproduced by the reviewer, and false in
      three places that each claimed the enumeration was complete at three
      paths. Reachability was nil (the sole caller restores onto a freshly
      mounted rail, where the field is already null); the SENTENCE was the
      defect, and it was about to be frozen into a released CHANGELOG.
      **NEW-2 TAKEN AS (a) — CLOSE IT, WITH NO VERSION BUMP.** The chat snapshot
      is a browser-local, versioned blob this release fully controls, and unlike
      the thread sidecar there is no second reader and no migration — so the
      disclosure can survive a tile being closed and reopened, which is the same
      lost-badge class one lifecycle up from S4. `chatSnapshot` gains one
      OPTIONAL field carrying the released posture object whole (named
      `context_packet`, so ONE validator serves a stored blob and a wire record
      and no third spelling exists), and `restoreChatState` adopts it through
      that same validator — a hand-edited blob claiming `reduced` with no
      readable reason fails closed to null rather than captioning the transcript
      with a reduction nobody can check.
      NO BUMP, because `CHAT_SNAPSHOT_VERSION` is a FAIL-CLOSED gate:
      `restoreChatState` keeps the FRESH state on an unrecognized version, so
      bumping would discard every stored blob on the first reopen after the
      upgrade — the operator's composer text, subject, model choice and
      proposals, spent to add a caption. An optional field invalidates nothing
      instead: an old blob lacks the key and restores to posture-unknown, which
      renders no note and is exactly the pre-release behaviour, and a NEW blob
      read by an OLDER build is ignored because this restore reads named fields
      and never enumerates. Both directions safe — the same additive reasoning
      the released wire contracts use when they grow without moving
      `contract_schema_version`, applied to a blob rather than a contract.
      AN EXPLICIT `full` IS PERSISTED TOO, which the first version of the probe
      called an oversight and which is in fact the doctrine: absent and `full`
      are DIFFERENT facts everywhere else in this release, so dropping `full`
      from the blob would restore "unknown" over a posture somebody checked and
      re-introduce the inference-by-absence the release forbids. The key is
      omitted only when there is no posture to state at all.
      **FLAGGED AS A GAP, NOT AS A DECISION SETTLED IN THIS RELEASE'S FAVOUR —
      THE THREAD SIDECAR STILL CANNOT STATE THE POSTURE, and the contrast with
      NEW-2 is exactly why one closed and the other did not.** The durable
      transcript on disk names the turn id, the model and the bound buffer, and
      gains nothing here. Extending it was considered and refused ON THE FORMAT:
      `doxbench_threads._parse_turn` refuses any turn header that does not split
      into EXACTLY three fields, so a fourth would make every sidecar already on
      disk unreadable by the new parser and every new sidecar unreadable by the
      old one — a breaking change to a record people trust, inside an additive
      release. So a reader of a thread file can learn WHICH MODEL answered
      (§11.7's F3 fixed that) and cannot learn WHAT CONTEXT it answered on.
      That is the honest counterpart to F3 and it is recorded rather than
      papered over; closing it needs a sidecar format migration, which is a
      successor change's act.
      **A SECOND RECORDED v1 LIMITATION** (the first was §11.7's, about the
      requested versus the answering model). The DEPRECATED
      `workbench-chat-turn-success` has no `context_packet` and gains none, so a
      v1 turn that ran reduced SUCCEEDS — the ratified "MUST NOT make the editors
      unusable" half — and cannot say so on the wire. The reduction is still
      stated inside the packet, where it always was. Widening a deprecated closed
      shape whose whole promise is byte-identical stability is what
      `contract-v1.34`'s deprecation forbids; the migration path is the v2
      envelope. Recorded at the v1 arm in `serve.py`, in the CHANGELOG, and
      pinned by a test that fails if the v1 record ever grows the key.
      **PRESENCE IS NOT TRUTHINESS — the bot round's finding, and it reached
      FOUR gates where the reviewer named two (Copilot on PR #256).** The
      released shape forbids `reduced_reason`'s KEY on a `full` posture
      (`not: {required: [reduced_reason]}`); three of the family's other gates
      forbade only a USEFUL value, so `{posture: "full", reduced_reason: ""}`
      passed them. Reproduced across all five gates before anything was
      touched — the shape refused it, the delegated validator refused it, and
      `ContextPacket.__post_init__`, `serve.doxbench_context_packet` and the
      browser's `adoptContextPacket` all ACCEPTED it, the first two normalizing
      it into a record with the key silently dropped.
      A FOURTH GATE WAS FOUND WHILE FIXING THE OTHER THREE: the delegated
      validator read `reason is not None` where the shape reads the key, and
      `.get()` cannot tell `reduced_reason: null` from an absent one — so it
      accepted a NULL on a full posture that the shape refuses. Copilot named
      two; there were four.
      Fixed at each: `is not None` at the type and the derivation (a Python
      attribute has no key/value distinction, so that IS presence there), and
      own-key presence in the validator and the adopter, which read JSON and do.
      **THE REDUCED ARM IS DELIBERATELY UNCHANGED and the asymmetry is the
      shape's own**: `full` refuses the field for BEING THERE, `reduced` refuses
      it for being UNUSABLE (`required` plus `minLength: 1`). Two rules, not one
      predicate — said at each site, because collapsing them is exactly how this
      defect would come back. Both directions are pinned: a blank still refuses
      on `reduced`, a real reason still passes, and an absent key still adopts
      on `full`.
      Two packaged negatives earn their own files, because each is the instance
      a different gate missed: `-context-empty-reason-on-full` and
      `-context-null-reason-on-full`. NO CONTRACT BYTE MOVES for any of it — the
      shape was right all along — so the schema digest is unchanged at
      `cc874fef…`, the inventory is untouched, and `verify-commit` still passes;
      asserted rather than assumed, and the two new examples are confirmed NOT
      inventory members.
      **REVERT-TESTED — 53 MUTATION RUNS over 47 distinct mutations, and FOUR
      came back GREEN.** (29 before the adversarial review; nine at its first
      round; eight at its second; seven at the bot round.)
      Every schema clause was reverted individually WITH THE DIGEST REPINNED, so
      each case fired on the clause rather than on the pin: both conditionals,
      the posture enum, the object's closure, its `required`, the reason ceiling
      in BOTH directions (raised → the over-ceiling refusal stops firing;
      lowered → the shipped-reason guard fires), `context_packet` made required
      (additivity broken), removed altogether, and added to the v1 envelope.
      All THREE pin surfaces were drifted back to their v1.38 values, each on
      its own and each RED on its own: `CONTRACT_TAG`, the module's chat-turn
      digest, and the manifest row's digest. Serve: the derivation as a constant `full`, the reason
      re-derived rather than carried, the fail-open default, the key not
      emitted, and each of the three refusal arms on its own. Browser: the
      adopter not adopting, the adopter failing OPEN, `beginTurn` not clearing,
      the note rendering for a full turn, the note never hidden, and
      `adoptThreadTranscript` not clearing. THE FIRST GREEN was that last case —
      deleting the thread-switch clear broke no test — and the probe now asserts
      it (re-run RED). The second is the validator arm below.
      THE REVIEW ROUND ADDED NINE MORE: the S1 write-order defect restored; the
      S2 ceiling dropped, made to count bytes instead of code points, its
      constant drifted, and the released `maxLength` drifted the other way; the
      S4 `beginTurn` clear restored and `settleTurnSuccess` made to keep a stale
      posture; and the N3 released-lane test driven against a posture emitted
      without its reason.
      **THE THIRD GREEN WAS THE S1 PROBE ITSELF, and it is the most useful
      result in this table.** Restoring the write-order defect (R27) left the
      new S1 test PASSING. Cause: under the wrong order a reduced turn produces
      TWO non-empty writes — the settling render writes the text while the node
      is still hidden, and a LATER re-render writes the identical text with it
      already visible — and the probe read `writes[length - 1]`, which is the
      benign one. It now asserts over EVERY non-empty write (none may happen
      while hidden) and the re-run is RED. The reviewer predicted this class
      exactly when they said an attribute assertion cannot catch the order; the
      first attempt at the fix reproduced their point one level up.
      THE SECOND ROUND ADDED EIGHT: `restoreChatState` keeping the stale posture
      and nulling instead of adopting; the snapshot not carrying the posture and
      always writing the key; the stored posture trusted unvalidated; and the
      identical-text guard dropped.
      THE BOT ROUND ADDED SEVEN: truthiness restored at the type, at the
      derivation and at the adopter; the validator's key-presence check reverted
      to a value check (run twice, against its self-test and against the
      finding-code pin); and the reduced arm loosened at the type and at the
      derivation, to prove the fix tightened `full` WITHOUT weakening `reduced`.
      NO FIFTH GREEN: the validator revert leaves its own self-test green, which
      is not news — it is the SAME diagnostic behaviour already recorded above
      (the shape refuses those instances anyway), and the finding-code pin that
      guards it went RED, exactly as designed. The behaviour was predicted by
      the earlier finding and then observed, which is what a recorded diagnostic
      is supposed to do.
      **THE FOURTH GREEN WAS THE SAME CLASS AS THE THIRD, one layer along.**
      Removing the stored-blob VALIDATION (R39) left the contradictory-blob test
      passing, because `reducedContextNote` holds its own second guard on the
      same rule and the probe was reading the rendered NOTE. It now reads the
      ADOPTED STATE across five contradictions, and also asserts the honest blob
      still adopts, so the guard is shown to be discriminating rather than
      merely refusing everything; the re-run is RED. Twice now a probe has been
      satisfied by a downstream guard rather than by the thing it names — worth
      recording as a habit to check, not just as two fixed tests.
      (A PROCESS NOTE, since the table would otherwise show a phantom fifth
      GREEN: the revert harness restores with `git checkout -- .`, so a
      strengthening that has not been COMMITTED is reverted before the mutation
      is applied and the old probe is what runs. That happened once here. Commit
      before revert-testing.)
      **AND ONE ARM IS A DIAGNOSTIC RATHER THAN A GUARD, stated because
      revert-testing is what proved it.** Disabling BOTH pairing arms in the
      delegated validator leaves its own packaged self-test GREEN, because the
      shape refuses the same two instances anyway. That is exactly the class
      §11.7's revert-testing found for its separator-collision and
      self-reference arms, and it is handled the same way: the arms are pinned
      on their finding CODE, which is the only guard that fails when they are
      deleted. They are defence in depth and the diagnostic a reader of
      validator output actually gets — not a second refusal, and the tick does
      not claim they are.
      A THIRD DELEGATED RULE WAS CONSIDERED AND REJECTED: requiring the reason to
      SAY that nothing unbounded was substituted and no rail was bypassed. Both
      shipped reasons do say it, and a rule to that effect is prose-matching a
      contract — it refuses a conformant producer worded differently and passes a
      dishonest one that quotes the sentence. What the wire can check is that a
      reduction is STATED; whether the statement is TRUE is the assembler's rail,
      enforced where the rails run.
      OWED CROSS-REPO FOLLOW-UP, recorded and not performed: the schema's
      description names codexFactory's
      `specs/010-doxbench-editor-chat/contracts/chat-turn.md` as its consumer
      contract. That file is NOT in this checkout and was NOT read, so the claim
      here is the OBLIGATION and not a finding — if it enumerates the v2 success
      envelope's fields it is now short by one, exactly as §11.7 recorded for the
      model-catalog document. It remains CORRECT either way while that repository
      pins `contract-v1.27`; updating it is its own governed act under the domain
      upgrade runbook.
- [x] 10.8 Per-turn and per-session token telemetry is emitted content-free.
      Where the metering requirement's client/domain/bill-to fields have no
      value on a self-hosted console, the absence is declared rather than
      filled with a placeholder.
      `scripts/ideation_dashboard/doxbench_telemetry.py`, cited from
      `memory-gateway`'s `Usage Metering Is Gateway-Owned` (the requirement
      whose `client`/`domain`/`bill-to`/customer-subject fields this console
      cannot fill), and emitted from `build_prompt_envelope` — the one place
      where both the packet's byte count and the prompt's are real
      measurements.
      Content-freedom is STRUCTURAL: every field is a count, a
      closed-vocabulary label, a scope key, or a `DeclaredAbsence`, so there is
      no field a caller could put text in. Each unfillable field accepts ONLY a
      declared absence carrying its reason, so a later caller cannot quietly
      fill one in. The meter is bounded, per-process, and writes nowhere.
      **TOKENS, honestly.** A token count is carried only when a PROVIDER
      reports one and is a declared absence otherwise: this surface measures
      exact UTF-8 bytes and has no tokenizer, and multiplying bytes by a
      guessed ratio would be a fabricated measurement in a usage record. §11
      owns the dispatch operation that will carry a reported count.
      **"EMITTED" RESTATED HONESTLY (adversarial review, F9).** Telemetry is
      MEASURED AND RETAINED IN-PROCESS, readable from the served process's own
      meter (`handler.usage_meter`, per-turn and per-session). `record`'s
      return value is not consumed by its caller, and NOTHING emits the record
      off-process: there is no log line, no wire field, and no store, because
      the released success envelope has no room for one and this slice may not
      touch `contracts/`. The emission surface is owed to the slice that gets
      one, and until then "emitted" means "measured, retained, and readable
      here" — which is what the tests assert.
      **AND THE RETENTION IS BOUNDED, VISIBLY.** An evicted scope used to
      answer `None`, byte-identical to a scope that never ran, so a
      conversation with five hundred metered turns and one with none read the
      same. `session()` now has three distinct answers, evictions are counted,
      and eviction is least-recently-RECORDED rather than first-opened so the
      busiest live conversation is not the first dropped.

**The `memory-gateway` conformance declaration** (design §7.1) is realized as a
first-class machine-readable artifact,
`scripts/ideation_dashboard/doxbench_memory_gateway.py`: the capability's whole
21-requirement roster with its published tiers, a disposition AND a reason for
every one of them, and the reviewed act (`create-document`, carried to review by
the session pull request) that satisfies promotion where the target is not a
Hermes memory layer. Conformance validation READS it — `assess_conformance(None)`
refuses rather than passing — and an incomplete declaration is refused, because
"an unnamed absence is the thing it replaces". The three refusal conditions are
constructive: a consumer holding a provider credential, addressing a customer
subject, or routing to a networked provider never obtains a declaration to
annotate, and one that acquires any of them LOSES it. The seven requirements the
delta says a declaration may not reduce cannot be declared inapplicable at all.
The roster is asserted against the promoted spec file itself, and the
declaration's claims are cross-examined against the modules that realize them.
**Two dispositions the design left unnamed, flagged rather than assumed:**
`Expert Memory And Knowledge DBs Are Gateway-Governed` is INAPPLICABLE (no
Domain Omnigent expert and no external knowledge DB is in this path), and
`Gateway Conformance Is Testable` is **NARROWED** — **corrected from REALIZED
by the adversarial review (F4)**, which was right: that requirement's scenarios
are about a DomainxFactory declaring a `memory_gateway` block in its
`stack.yaml` that the canonical domain-factory validator checks, and doxBench
is not a domain factory and declares no such block. Nothing outside this
repository's own test run reads this declaration today, so REALIZED rested on
"this declaration IS the artifact validation reads" — a claim with no reader
behind it. What IS realized is the requirement's rule, that a conformance claim
executes rather than asserts; that is what NARROWED now says, with the reason.
**The TIER column is transcribed, not invented (F7):** it carried `M0` for a
requirement the spec's tier block never tiers, and flattened
`Expert Memory And Knowledge DBs Are Gateway-Governed` to `M4` where the spec
says in as many words that it follows the tier of the operation it mirrors.
`TIER_UNTIERED` and `TIER_MIRRORS_OPERATION` replace both, and the roster test —
which checked NAMES only — now asserts every value against the spec's own
tier block.

**The three-layer compression stack's fidelity vocabulary** is pinned as data
with a checker in `doxbench_packet`: describing selection as lossy, semantic
compaction as lossless, or mechanical offload as a summary RAISES. Layer one is
realized here; layer two names `doxbench_threads.compact_thread` as its real
owner; layer THREE declares itself unrealized and names §11, and the note says
where the lifecycle exemption sits relative to it and why a compressor with no
caller-metadata surface is disqualified from carrying it. The watch-listed
candidate is recorded with its five gates and CANNOT be constructed as adopted;
no module in this slice depends on one.

**Thread read side — the seam §10 shipped, FILLED at §11.** The packet carries
the selected document's thread in full and the other loaded documents' state
headers through `doxbench_threads`' own `render_thread`/`render_state_header`.
When this task shipped nothing wrote a turn into a sidecar (tasks 9.2/9.5 were
"route unwired" by design), so the route supplied no threads and the packet
DECLARED the absence honestly. §11 fills the seam: `serve._document_threads`
reads each loaded document's sidecar out of the SESSION WORKTREE and hands the
mapping to `assemble_packet`, and the honest absence now means what it says — a
document with no sidecar, an unreadable one, a scope with no live session — while
a document that HAS one is carried. The unwired note is retired rather than left
standing; `test_doxbench_thread_wiring.py` is where the wiring is proven.

**Layer THREE is realized at §11**, on the surface `verification-findings.md`
§3.6 verified: `OmpHarnessBridge.shake()` sends the recorded slash-command frame
(`{"type": "prompt", "message": "/shake elide"}`), reads back
`data.agentInvoked: false` plus the free-text `command_output` summary, and
reports that summary for BOOKKEEPING ONLY — there is no structured
bytes-reclaimed field in the RPC response, so `ShakeReport` claims no number and
a test asserts it carries none. The fidelity vocabulary's layer-three entry is
untouched: mechanical, reversible, at the model boundary.

## 11. The harness bridge and the model menu

- [x] 11.1 The bridge: a stdlib-only local child process translating the
      server's call into the harness's stdio RPC, the only component that knows
      the harness protocol, loopback-local, holding no credential.
      Realized as `scripts/ideation_dashboard/doxbench_bridge.py`. Stdlib only;
      every seam a test needs — the spawn, the clock, the log sink, the child
      environment — is injected, so no gate depends on `omp` being installed,
      and it is not installed on this host.
      LOOPBACK-LOCAL BY CONSTRUCTION rather than by configuration: there is no
      socket here at all, the transport is the child's own stdin/stdout pipe,
      and upstream has no HTTP mode to add one.
      CREDENTIAL-FREE BY CONSTRUCTION too: `child_environment` is an ALLOWLIST
      (`PATH`, `HOME`, `LANG`, `LC_ALL`, `TMPDIR`) rather than a denylist,
      because a denylist of credential-shaped names is a list somebody has to
      keep up with and the one it misses is the one that leaks. A test drives a
      base environment carrying `ANTHROPIC_API_KEY`/`AWS_SECRET_ACCESS_KEY` and
      asserts the child sees neither, and a second test asserts the module's own
      source names no credential spelling at all.
      **Judgement call, flagged (the child's cwd).** The child runs in the
      bridge's own session directory, never a git worktree or the served
      checkout. Two things follow, both wanted: the harness's project-scoped
      `.omp/mcp.json` discovery finds the knowledge-mount registration the bridge
      wrote there and nothing else, and a harness tool that reaches for the
      filesystem lands in a scratch directory rather than in the corpus.
      Grounding comes from the packet, which is assembled and bounded before the
      child process exists.
      **CORRECTED 2026-08-19 AFTER LIVE VERIFICATION (adversarial review P1-1).**
      The first realization guessed `--setting memory.backend=off` and ticked
      this box on it. There is no such flag: real v17.3.7 answers
      `Error: unknown flag: --setting` and exits, so the bridge could never have
      started a harness. The pin now rides `--config=<overlay>` — a real,
      repeatable flag whose overlay outranks both the global and the project
      settings layers — written into the bridge's own session root, so pinning
      the harness's memory backend touches no operator's home and no corpus.
      LIVE: the child starts, `get_state` answers, and `/memory diagnose` reports
      *"Memory backend is off — there is nothing to show."* from inside the
      running session, while `backend: local` in the same slot answers
      differently. The one-constant isolation the original tick claimed as its
      safety net did work — the correction was one constant plus one test — but
      the tick itself should not have been `[x]` on an unexecuted launch line,
      and this note is the record of that.
      **RECORDED, not fixed (an air-gapped install's first turn).**
      `providers.tinyModel`, `.memoryModel` and `.autoThinkingModel` default to
      `online`, and on a host with no egress the agent turn BLOCKS on them
      before it ever reaches a local model — the live smoke pins all three local
      in its own overlay to get past it. That is a property of the install, not
      of the bridge, and the bridge deliberately does not pin them: choosing a
      model role is an operator decision, and a bridge that quietly rewrote
      three of them would be making it. An operator deploying this somewhere
      without egress will meet it, so it is written here and in the smoke's own
      docstring.
- [x] 11.2 It is an ADAPTER for the UNCHANGED three-member `WorkbenchModelPort`.
      A test asserts the port still has exactly three members and that
      `FORBIDDEN_PORT_MEMBERS` still bans the rest.
      D14, literally: the port's `__protocol_attrs__` equality is re-asserted in
      the slice that would have widened it, and the ADAPTER's own public surface
      is asserted disjoint from `FORBIDDEN_PORT_MEMBERS` as well — a
      strengthening past the task, because the ban is only worth anything if the
      thing behind the seam respects it too. Per-turn model choice, session
      switching, `/shake` and `artifact://` dereferencing all live INSIDE the
      adapter; each of them is a fourth port member somebody would otherwise have
      argued for.
      **NOTED (adversarial review P3-21): the ban list cannot see the whole
      surface.** The PORT is three members and `FORBIDDEN_PORT_MEMBERS` polices
      exactly those, but the ROUTE reaches five more names on the adapter
      DUCK-TYPED — `conversation_key`, `outline_conversation_key`,
      `for_conversation`, `mirror`, `dereference` — and a duck-typed call is not
      a protocol member, so no `__protocol_attrs__` equality can see them.
      (`select_thread` is NOT among them since PR #223's C2: the route asks for
      a per-turn conversation view instead, and `select_thread` stays public for
      the live smoke and for binding a builtin.) That is not a D14 violation:
      none is a second spelling of the provider verb, and every one is a
      capability D14 explicitly puts INSIDE the adapter rather than on the port.
      But it is a contract nothing else stated, so a test now declares that set
      and asserts the route reaches nothing outside it — a fifth name arriving
      without that list moving is the thing to argue about.
- [x] 11.3 Lifecycle: started on demand at the first turn that needs it,
      supervised, restarted on failure with a bounded retry, stderr to the
      serve's log and never to the wire; a dead or unstartable bridge surfaces
      as the honest model-unavailable posture with the route's existing refusal
      shape and gate order unchanged.
      ON DEMAND is asserted as a NEGATIVE: `catalog()` — the route's pre-turn
      call — must not start a child, and a test drives `started is False` across
      it and `True` only after the first `dispatch`. An editor-only session
      therefore spawns no model process it never uses.
      SUPERVISED: liveness is checked before every dispatch, the restart is
      bounded (`MAX_RESTARTS = 2`, and a test counts the attempts so the bound is
      a number something reads), and the child's stderr is drained to an injected
      log sink and to nothing else — a test scripts a sentinel on the child's
      stderr and asserts it reaches the log and never the answer.
      **Judgement call, flagged (#1 — the honest model-unavailable posture has
      TWO LEGS, and the split is worth adjudicating).** (1) A bridge known dead or unstartable
      makes `catalog()` report every entry `available: false`, which fails
      `selectable_entry_for` at the route's EXISTING model step — so the refusal
      shape and the gate ORDER are byte-identical, nothing is dispatched, and no
      packet is even assembled. (2) A child that dies MID-turn, after the catalog
      said available, surfaces by `dispatch` raising, which
      `doxbench_model.dispatch_turn` maps to its fixed redacted `model_failed` —
      the route's existing shape for an adapter that failed. Leg (2) is not
      spelled `model_unavailable` because the port has no channel to say so
      without a fourth member, and inventing one would be exactly the widening
      D14 forbids.
      **CORRECTED 2026-08-19 (adversarial review P2-8): leg (1) did not engage
      for the commonest failure.** `_unavailable` was set only where `Popen`
      itself raised or the bounded retry was spent, so a child that SPAWNS and
      then exits — which is exactly what the `--setting` defect produced — left
      the catalog advertising the model as available forever and pushed every
      later turn onto leg (2). The reviewer proved it twice, live and
      hermetically. Two changes: every public entry point now marks the bridge
      unavailable when a `BridgeUnavailable` escapes it, and `catalog()` also
      consults the child's own liveness. The prose above is now true of the
      failure class it was written for, and a test drives a spawn-then-die child
      through `catalog()` on both sides of the failure.
- [x] 11.4 One harness session per document thread; switching the selected
      document switches the harness session; one session never serves two
      threads.
      `select_thread(document_key)` binds the harness to one document's session:
      a thread already seen is re-attached with `switch_session` carrying the
      path `get_state` reported when that thread's session was created (the
      recorded second-process flow, verbatim), a thread never seen gets a FRESH
      session, and a session path already bound to another thread is REFUSED
      (`BridgeSessionConflict`) rather than shared. The route calls it before
      dispatch, and a bind failure REFUSES the turn rather than dispatching into
      another document's conversation.
      FRESH-PER-THREAD is what makes §3.3 safe for free: `SYSTEM.md` is read once
      at session start and every later rebuild replays that captured string, so a
      source-ranking hierarchy that must not change mid-conversation is
      guaranteed by never reusing a session across threads.
      **CORRECTED 2026-08-19 (adversarial review P2-11): the rule is now TOTAL.**
      The bind was gated on `bound_buffer_key in document_keys`, so an
      OUTLINE-bound turn never bound at all and was prompted into whichever
      DOCUMENT session the harness was last switched to — accumulating in that
      document's session `.jsonl`, so the document's next turn carried the
      outline conversation in the harness's own context. That is the second
      store design §5.2 keeps apart, cross-contaminated. Now every turn binds: a
      document by its path, an outline by a TILE-SCOPED key
      (`outline_conversation_key`, so two tiles' outlines are two conversations),
      and the bridge REFUSES an unbound dispatch outright rather than running it
      in whatever session it happens to be on — the invariant made structural so
      a later caller cannot reintroduce it by forgetting.
      **Judgement call, flagged (#JC-2 — ONE named channel for harness
      builtins).** `/shake`, `/memory` and `/mcp` all ride the generic
      slash-command-over-`prompt` frame, so the framing is named once
      (`run_command`) and `shake()` is a thin wrapper over it rather than a
      second copy. The FACTORING stands; the SAFETY CLAIM that first shipped
      with it did not.
      **CORRECTED 2026-08-19 (re-verify N-2): an unlisted slash command is not
      an error, it is a model turn.** The docstring claimed this channel
      "cannot carry a model prompt — a caller passing prose gets it interpreted
      by the harness as an unknown command". Live, `/definitelynotacommand`
      answers with the model-turn response shape and runs a real turn to
      `agent_end` — unbounded by the packet assembler, uncounted by the byte
      bounds, unrecorded in any sidecar. No `serve.py` caller reached it that
      way, but a false safety claim in the one module that knows this protocol
      is worth more than the bug it hid. The head is now a CLOSED allowlist
      (`HARNESS_COMMAND_HEADS`), a builtin requires a bound conversation exactly
      as a turn does (an unbound `/shake` would compact somebody else's
      context), and a response reporting that the agent WAS invoked raises
      rather than returning. Pinned hermetically and against the real binary.
      **CORRECTED 2026-08-19 (PR #223, Codex C1 and C2): the binding was right
      in shape and wrong in two mechanics.**
      C1 — the conversation key was the bare `bound_buffer_key`, a
      repository-relative path against a SINGLE per-serve session map, so two
      scopes loading the SAME path (one repository at two refs, or two
      repositories on a multi-repository plane) collided and the second silently
      inherited the first's harness session. Reproduced: two `select_thread`
      calls with one path returned one session file. The key is now composed
      from the whole `ScopeKey` plus the buffer key, as JSON so the composition
      is INJECTIVE — no spelling of one scope can forge another. Outline keys
      are scoped identically, where they had been tile-only.
      C2 — `select_thread` and `dispatch` each took the bridge lock SEPARATELY,
      and this is a threading server: handler A selects A, handler B selects B,
      then A's dispatch sends A's prompt into B's session. Reproduced directly.
      The bind is now PART of the dispatch: the route asks for a per-turn
      `for_conversation(key)` view whose `dispatch` binds and prompts inside one
      lock acquisition. The view is exactly the three-member port, so
      `dispatch_turn` is untouched and D14 stands.
      **Judgement call, flagged (#JC-3 — an unbound dispatch is REFUSED).**
      STRENGTHENED by C2: the refusal was only ever a check that SOME
      conversation was selected, which is the weaker half of the property. The
      binding is now atomic with the turn, so "the turn runs in its own
      conversation" is structural rather than a rule the route follows.
      Given its own entry rather than living only inside the P2-11 correction
      above (re-verify N-5). A turn — and now a builtin — runs only in the
      conversation it belongs to; the alternative, defaulting to whichever
      session the harness was last switched to, is the leak itself.
      **Judgement call, flagged (how a fresh session is made).** The recorded RPC
      surface has `switch_session` and it has process start with `--session-dir`;
      it has no in-session "start another session" command. So a thread nothing
      has opened a session for gets one by RESTARTING the child under this
      bridge's own session directory and recording the `get_state.sessionFile`
      the new process reports. That is a real cost — one process start per new
      thread in a serve — and it is the option that keeps every frame inside the
      verified set instead of inventing one. The recorded session PATHS survive a
      restart deliberately (a session file outlives the process that opened it,
      which is why `switch_session` by path works at all); what does not survive
      is the selection.
- [x] 11.5 The sidecar is the record: every turn is mirrored to it, and the
      harness's native memory holds no thread. Any enabled harness-local memory
      is non-authoritative and ranked last.
      **THE RECORD.** Every answered turn is mirrored into the SELECTED
      document's sidecar before the answer is stored or sent, through
      `doxbench_threads`' one write route and the doxBench Save gate's own
      declared allowlist. The turn id is the DERIVED `assistant_turn_id`, not the
      caller's `client_turn_id`: the released schema bounds that field's LENGTH
      and nothing else, so a client could spell one carrying the sidecar's own
      turn-header separator, and a record must not take its identity from a
      string a caller chose freely. The sidecar format is LF-only and the wire
      carries whatever a browser and a provider produced, so the mirror
      NORMALISES CRLF at the one place a turn becomes a record — a normalisation,
      not an edit: the bytes the model returned still ride the response envelope
      unchanged.
      **THE HARNESS HOLDS NO THREAD, and since 2026-08-19 that really is an
      install fact rather than a policy.** The first realization asserted this
      on a flag the harness rejects, which made the whole claim untrue
      (adversarial review P2-12): a bridge that cannot start pins nothing. The
      pin now rides a `--config` overlay — a real, repeatable flag whose overlay
      outranks the global and project settings layers — and it is OBSERVABLE
      from inside the running session: `/memory diagnose` answers *"Memory
      backend is off"*, and the live smoke reads that back out of a real harness
      rather than trusting the file the bridge wrote. The dedicated
      `--profile doxbench-bridge` still isolates auth, sessions, settings and
      caches, so a developer's personal interactive settings cannot bleed in.
      `HarnessThreadMirror` re-asserts the DECLARATION as belt and braces — a
      bridge whose launch config lost the pin REFUSES to mirror rather than
      quietly starting a second store — and that guard is honestly a check on
      the bridge's own config rather than on the harness's state; the harness's
      state is what the live smoke reads. The source-ranking hierarchy already ranks any
      harness-local memory LAST and says in as many words that it is never
      governed truth (`SOURCE_RANKING_TEXT`, task 5.5).
      **CORRECTED 2026-08-19 (adversarial review P1-3/P1-4): what was being
      recorded was an EMPTY answer.** The reader looked for a flat
      `text`/`delta`/`content`/`message` at a frame's top level, and a real
      `message_update` carries the text one level down inside
      `assistantMessageEvent`; and an omitted `agentInvoked` — which is what a
      real prompt response has — was read as "the agent was not invoked", the
      opposite of `rpc.md:104`. So `dispatch` returned `{"assistant_prose": ""}`
      before the turn had happened, and THIS TASK'S mirror wrote that empty
      answer into the sidecar as the durable record. Both are fixed and
      live-proven; the mirror now records the model's own text.
      **CORRECTED 2026-08-19 (PR #223, Codex C3): the sidecar came from the
      buffer KEY, not the document's path.** Key and path differ for exactly one
      buffer — the reserved unbacked slot, whose key is `document` and whose
      path is None — and a turn bound to it wrote
      `session-threads/document.thread.md`: a sidecar for a document that does
      not exist. No Save could commit it (`thread_commit_paths` is called with
      the real path), and a later re-key stranded it while a second thread
      started at the document's own path. This is the key-vs-path resolver split
      PR #207's F2 closed elsewhere, re-opened one layer down. The sidecar is
      now derived from the bound buffer's own `path`, and a buffer with NO path
      records no thread — which makes judgement call #15 below true of every
      pathless buffer rather than of the outline alone.
      **Judgement call, flagged (#15 — a turn on a buffer with NO DOCUMENT
      writes no thread).**
      A thread belongs to a DOCUMENT, and the outline buffer is the tile's, not
      a document's, so an outline turn records no sidecar. This was true of the
      sidecar and NOT of the harness session until P2-11 was fixed (see 11.4);
      it was also missing from this list entirely, which the reviewer counted
      as a material honesty gap rather than a bookkeeping nit.
      **Judgement call, flagged (#16 — where the assistant's text is read
      from).** ONE reader, driven by a CLOSED table of event types
      (`text_delta`, `text_end`) rather than a guess-list of field names, plus
      one reader for a terminal frame's whole message list. The answer prefers
      `agent_end.messages` (the harness's own final state), then a
      `turn_end`/`message_end` message, then the accumulated deltas. The
      original version of this call guessed a flat tuple of top-level names and
      was wrong IN KIND, not in spelling — no addition to that tuple could have
      found a nested field — and it was recorded only in a module comment, never
      here. Both corrected.
      **Judgement call, flagged (a record that cannot be written).** The provider
      has already answered by the time the record is written, and there is no
      released refusal code for "the record could not be written". Losing the
      human's answer to protect a record that failed for an environment reason is
      the worse trade, so the answer still ships, the failure goes to the serve's
      own log — where every other non-wire diagnostic goes — and the NEXT turn's
      packet declares that document's thread ABSENT, honestly, rather than
      implying a conversation that was never recorded. A test pins that the wire
      outcome, its status and its envelope are unchanged and that nothing leaks.
      **`artifact://` (task 3.5's finding), both remedies live.** The bridge
      supplies the dereference seam `dereference_bodies` asks for: it resolves a
      pointer's content out of the harness's own store — the sibling directory of
      the session file, derived from it and nothing else — and where inlining is
      infeasible (unreadable, undecodable, or past
      `MAX_INLINE_ARTIFACT_BYTES`) it returns `elided_note(bytes, reason)`
      instead. A serve with NO bridge supplies a seam that resolves nothing, so a
      pointer-bearing body is refused by `ThreadTurn` and the sidecar records
      NOTHING rather than an unresolvable pointer; the turn itself still answers.
      **OBLIGATION INHERITED FROM §10 — DISCHARGED BY THIS SLICE, and the fix
      option is recorded below with its re-measurement** (re-verify carry-forward
      NF-A). §10's packet bound composes
      with the model's declared input limit through
      `doxbench_packet.packet_budget_for`, which subtracts a FLAT
      `PROMPT_SCAFFOLD_RESERVE_BYTES` (16 384) for everything the rendered
      prompt spends outside the packet's own source bytes and outside the
      request bytes the route already measured — section labels, the
      non-authoritative notes each thread section carries, the evidence
      headers, and the packet's declaration line per source.
      That reserve is adequate for the shape §10 SHIPS, which carries evidence
      and no threads, and it is measured against real rendered prompts at three
      ceilings. It is NOT adequate for the shape THIS task creates. Measured:
      24 thread-state sections plus 6 evidence sections at 120-character refs
      spend **19 745 bytes** of uncounted overhead, and the packet's own
      48-source bound spends **31 211** — both past the flat 16 384, so a turn
      near its model's ceiling could be accepted and then dispatch a prompt over
      that ceiling. That is exactly the defect CODEX-B closed for the
      evidence-only shape, re-opened by the section count this slice adds.
      **FIX OPTIONS, both viable, neither prejudged:** (a) charge the RENDERED
      section bytes against the budget rather than the source bytes — the
      honest measurement, and it makes the reserve cover only the genuinely
      fixed constants; or (b) scale the reserve with `MAX_PACKET_SOURCES` and
      the observed ref length, keeping the cheaper single subtraction.
      **RE-MEASURE METHOD:** render a real turn at a narrowed catalog ceiling
      with threads mirrored and evidence carried, sum
      `utf8_size(section.text)` across the assembled envelope, and compare it
      to the entry's `effective_input_limit` — the same approach
      `test_the_scaffold_reserve_is_MEASURED_adequate_not_asserted` already
      uses, extended to the thread sections this slice starts writing.
      Recorded against THIS task rather than left in §10's ticks, so it
      survives §10's archive the way task 10.7's release obligation does.
      **DISCHARGED — FIX OPTION (a), and why.** The RENDERED section scaffolding
      is now charged against the budget, per source, from the SAME literals the
      renderer uses: the three section preambles and the declaration line became
      module constants (`SELECTED_THREAD_PREAMBLE`, `THREAD_STATE_PREAMBLE`,
      `EVIDENCE_PREAMBLE`, `DECLARATION_LINE`), `PER_SOURCE_SCAFFOLD_BYTES` is
      DERIVED from the widest instantiation of them rather than typed in, and
      `packet_scaffold_reserve(thread_refs=…, evidence_slots=…)` charges one
      per-source cost per thread ref the route holds and per evidence slot it may
      fill. `PROMPT_SCAFFOLD_RESERVE_BYTES` keeps only what is genuinely FIXED,
      and the defaults reproduce the pre-§11 number exactly — so a caller
      carrying neither threads nor evidence stays on the arithmetic it was
      measured under.
      Option (b) — scaling one flat number by `MAX_PACKET_SOURCES` — was
      REJECTED, and the reason is a real cost rather than a preference: it
      charges every turn for 48 sections it will not carry, which on a narrow
      catalog ceiling refuses turns that would have fitted. Charging what the
      turn's OWN refs render is both the honest measurement and the cheaper one.
      **RE-MEASURED, three ways.**
      (1) `test_the_rendered_prompt_stays_inside_the_ceiling_WITH_threads`
      extends §10's method to thread sections: a real turn at three narrowed
      catalog ceilings (60 000 / 120 000 / 400 000) with a thread mirrored and
      evidence carried, summing `utf8_size(section.text)` across the assembled
      envelope and comparing it to the entry's effective input limit.
      (2) `test_the_FLAT_reserve_really_was_too_small_for_the_shape_this_slice_makes`
      drives the OBLIGATION'S OWN SHAPE through the real route — 24 loaded
      documents each with a thread, plus the evidence slots — and measures the
      scaffolding the rendered prompt actually spends: **16 477 bytes against the
      old flat 16 384**. So the breach is measured, not argued, and it is small,
      which is worth saying plainly: the flat number was inadequate, and it was
      inadequate by ~93 bytes at 30 sections rather than by the ~3 KB the
      obligation's own estimate implied.
      (3) The arithmetic is asserted to COVER both numbers the obligation itself
      recorded (19 745 at 24 thread-states plus 6 evidence refs of 120
      characters, and 31 211 at the 48-source bound).
      **CORRECTED 2026-08-19 (PR #223, Copilot CP3): one section key was left
      out of the derivation.** `_widest_per_source_bytes` counted only the two
      PREFIXED keys (`thread_state:`, `evidence:`) and missed the SELECTED
      thread's fixed `selected_thread`, which is the longest of the three — so a
      selected-thread source undercounted its key bytes by 2.
      `PER_SOURCE_SCAFFOLD_BYTES` moves 313 -> 315, and both of the obligation's
      recorded thresholds are still cleared with room:
      20 250 >= 19 745 at 24 thread-states plus 6 evidence refs of 120
      characters, and 32 400 >= 31 211 at the 48-source bound. The default
      reserve is unchanged, so a caller carrying neither threads nor evidence is
      on exactly the arithmetic it was measured under.
      **Judgement call, flagged (the ref is charged THREE times).** A source's
      ref renders in the declaration line and in its own section's preamble —
      that is two — and a third time in the section KEY (`thread_state:<ref>`,
      `evidence:<ref>`). The keys are not part of `section.text` and the bridge's
      own renderer does not emit them, so charging them is deliberately
      GENEROUS; it is also what brings the arithmetic above the obligation's two
      recorded measurements, which were taken against a shape this module can no
      longer reproduce exactly. Matching a number somebody else measured from
      ABOVE rather than from below is the honest direction for a reserve.
- [x] 11.6 Per-turn model choice is applied inside the adapter before dispatch,
      using the `model_id` the envelope already carries. No fourth port member.
      `OmpHarnessBridge.dispatch` sends `set_model` and then `prompt`, in that
      order, reading the `model_id` off the envelope — the recorded ordering
      (`switch_session` → `set_model` → `prompt`), verified hands-on in the
      findings' RPC-mechanics note. A test spies the frames a real child receives
      and asserts the pair and its order; another asserts a harness that refuses
      the model refuses the TURN rather than prompting a model nobody chose.
      **CORRECTED 2026-08-19 (adversarial review P1-5): the PROVIDER half was
      wrong, and every real `set_model` was refused.** The frame carried
      `entry.provider_class` as the harness provider id, and `provider_class` is
      a GOVERNANCE data-handling classification (`on-tenant`, `self_hosted`, …).
      Live, side by side on one session:
      `{"provider":"self_hosted"}` → `success:false, "Model not found:
      self_hosted/local-model"`; `{"provider":"local-proxy"}` →
      `success:true, data.id: local-model`. So no turn could ever have been
      dispatched, and the ordering this tick verified was the ordering of two
      frames the second of which always failed.
      **CORRECTED 2026-08-19 (re-verify N-1): the shipped DEFAULT refused every
      real turn.** With no `provider_id` declared, `_apply_model` omitted the
      `provider` key on a docstring claim that the harness would "resolve the
      model id by its own matching". Live, it answers
      `Model not found: undefined/<model>` — so `provider_id=None`, the shipped
      default, could not dispatch at all, and the fixture ACCEPTED the
      provider-less frame the real binary refuses (the P1-7 pattern recurring;
      the fixture now refuses it identically, which is what makes that lesson
      complete). A provider-less `set_model` is never sent now: with no
      declaration the bridge asks the harness which model it is ALREADY on —
      live-proven to work, a turn with no `set_model` at all completes on the
      profile's own default — and proceeds only if that is the model this turn
      asked for.
      **Judgement call, flagged (#JC-5 — an undeclared provider REFUSES a
      model the harness is not already on).** The alternative, letting the
      profile's default answer anyway, would put a model on the turn's durable
      record that did not answer it — the same class of untruth §13's
      `selected_model` exists to prevent. So an install that declares no harness
      provider serves exactly the model its profile holds, and says so plainly
      when asked for another.
      **Judgement call, flagged (where the harness provider id lives).** On
      `LaunchConfig.provider_id`, the bridge's INSTALL-SIDE declaration — the
      same placement §10 chose for the retrieval backend, and for the same
      reason: which provider an install talks to is an operator fact an operator
      must be able to read where the install is declared. Deliberately NOT on
      the catalog entry: that schema is a CLOSED seven-field shape whose
      widening is task 11.7's future release, and smuggling a harness-routing
      field into a governance record is the exact conflation that caused this
      defect. Undeclared, the `provider` key is OMITTED and the harness resolves
      the model id by its own matching. LIVE-PROVEN end to end: `dispatch` now
      returns `{"assistant_prose": "MOCK_DONE", "proposals": []}` in 1.40 s.
- [x] 11.7 The catalog declares the menu, `auto` declares itself a ROUTING RULE
      carrying the badge of every model it may route to, and the resolved model
      is recorded on the turn. An API-backed entry's credential comes from the
      ratified broker lane; the bridge holds no secret.
      **OBLIGATION RECORDED AGAINST THIS TASK by §13's release** (the delta's own
      rule: a field the released envelope has no room for MUST have its
      obligation recorded against the release that will carry it). The turn
      RECORD can already state a routing rule — `workbench-chat-turn-v2-success`
      carries `selected_model.routing_rule` beside the resolved `model_id`, and
      the route derives both from the catalog entry in ONE place
      (`serve.py doxbench_selected_model`). What has NO room for it is the
      CATALOG: `xfactory-workbench-model-catalog.schema.yaml` declares a CLOSED
      seven-field entry with no `routing_rule` and no resolved-model field, so no
      conformant catalog can declare an `auto` entry today, and the record's
      `routing_rule` is truthfully `false` for every entry that exists. This task
      therefore needs its OWN contract release — an additive model-catalog
      growth, allocated at ITS realization under the same versioning policy —
      before the ratified `The menu offers a routing rule` scenario can be
      claimed. Until then the gap is stated rather than papered over, which is
      the same discipline §13 applied to the bound buffer.
      **RUNTIME HALF REALIZED AT §11, RELEASE HALF STILL OWED — half-ticked in
      prose on task 10.7's precedent, and the box stays UNCHECKED because the
      ratified `The menu offers a routing rule` scenario still cannot be
      claimed.** What §11 built: the adapter applies the RESOLVED model id where
      a catalog entry can say so and the requested id otherwise
      (`OmpHarnessBridge._apply_model`), so the day an additive model-catalog
      release lets an entry declare `routing_rule` and a resolved model, the
      bridge already honours it with no change. A test drives a duck-typed entry
      that DOES declare one and asserts the harness is set to the resolved model.
      What §11 did NOT build, and must not: the catalog schema is untouched, no
      release was cut, and `routing_rule` stays truthfully `false` for every
      entry that can exist today — a test asserts `ModelCatalogEntry` has neither
      a `routing_rule` nor a `resolved_model_id` attribute, so the record's
      `false` is a fact about the TYPE rather than a default nobody checked.
      The credential clause IS discharged: the bridge's child environment is an
      ALLOWLIST no credential-shaped variable can pass, and the module's own
      source names none (task 11.1).
      **AND THE OTHER HALF OF IT, STATED (adversarial review P3-23).** Because
      the allowlist strips every provider credential variable, a live bridge can
      only authenticate from the `doxbench-bridge` PROFILE's own stored
      credentials — verified live: with an empty profile the harness answers
      *"No models available. Use /login or set an API key environment
      variable."*, which is the right posture (it refuses rather than reaching
      for an ambient key). What §11 never said is where that profile's
      credentials come from, and the answer is the sentence this task already
      carries: an API-backed entry's credential comes from the ratified broker
      lane (`add-model-provider-broker`), which provisions the profile — the
      bridge neither holds nor fetches one. A self-hosted, keyless provider (the
      live smoke's `auth: none`) needs no credential at all. Naming the
      provisioning step is part of the release this task still owes, since a
      catalog that can declare an API-backed routing entry is exactly the point
      at which an operator has to know how the profile got its key.
      **RELEASE HALF LANDED 2026-08-21 — `contract-v1.38`, and the box is now
      CHECKED because the ratified `The menu offers a routing rule` scenario is
      claimable.** `contracts/schemas/xfactory-workbench-model-catalog.schema.yaml`
      grows three OPTIONAL properties on `$defs/model_entry` that travel
      together: `routing_rule` (true means this entry is a rule, not a model),
      `routes_to` (every model it MAY route to, as unique non-empty `model_id`
      REFERENCES into the same catalog), and `resolved_model_id` (the one that
      ANSWERS, which is what the record's `model_id` carries beside
      `selected_model.requested_model_id`). ADDITIVE by construction and
      verified case by case against the released bytes: one `dependentRequired`
      block plus two `allOf` conditionals, and BOTH conditionals require
      `routing_rule` to be PRESENT, so an entry declaring no routing rule
      matches neither and is judged exactly as it was before.
      `contract_schema_version` stays 1 and the manifest row's `schema_version`
      stays 1 with it.
      The RUNTIME was not rebuilt, which was the point: `_apply_model` and
      `serve.py doxbench_selected_model` are byte-identical to what §11 and §13
      shipped, and each of their pre-existing duck-typed tests is KEPT VERBATIM
      and still green — that is the evidence the one-place derivation was written
      correctly the first time — with a REAL-`ModelCatalogEntry` sibling added
      beside it. `ModelCatalogEntry` gains the three fields as defaulted
      members, so every construction that predates the release still means
      `routing_rule=False`, no routable set, no resolved id.
      Five rules the shape cannot express are enforced BOTH in the delegated
      validator and at catalog construction (an in-process catalog never becomes
      a validated file; a file is never constructed through that type): no
      dangling target, no chained rule, an available rule resolves to an
      available model, THE BADGE COVERING, and a rule declaring no more headroom
      than the model that ANSWERS. Each has a packaged negative that fails
      for exactly its own reason; each was revert-tested (disable the rules ->
      5 validator errors, restore -> 0), and every schema clause was
      revert-tested individually with the digest repinned so the case fired on
      the clause rather than on the pin.
      **SEVEN RULES, NOT FIVE — corrected at adversarial review round 1 (F2).**
      The file gate never checked `resolved_model_id ∈ routes_to` nor
      self-reference, so it was strictly WEAKER than the type gate while its own
      docstring claimed the two were identical. The reviewer walked a catalog
      past it whose rule was badged safe and whose `resolved_model_id` named a
      model badged *"retained and used for vendor model training"* — every
      covering check had skipped that model, because they all iterate
      `routes_to`, which it was not in. Both checks are added, and the parity
      claim is no longer prose: a test runs BOTH gates over all TEN packaged
      routing negatives and requires both to refuse each one, plus a second test
      pinning every negative's own finding code.
      **THE TRANSCRIPT NAMED THE RULE, NOT THE MODEL THAT ANSWERED — corrected
      at review round 1 (F3), and this was the release's worst defect.** The
      ratified THEN's own purpose clause is "so a transcript names the model that
      actually answered", and the wire record did that correctly while the THREAD
      SIDECAR — the durable transcript on disk, the thing a human reads later —
      was handed the REQUESTED id. On a routed turn the file said `auto` and no
      reader could learn which model wrote the answer. The cause was placement,
      not logic: `doxbench_selected_model(model_entry)` was computed inside the
      v2 arm, AFTER the sidecar was written. It is hoisted above the sidecar and
      the sidecar takes the resolved id. Two route-level tests drive a routing
      entry through the real POST and assert the wire record and the sidecar
      header TOGETHER, with an unrouted sibling proving the hoist did not move
      the ordinary case; un-hoisting fails the routed test.
      **A RECORDED v1 LIMITATION (F3's other half).** The DEPRECATED v1 success
      envelope has one `model_id` field and no `selected_model`, so on a routed
      turn it cannot state both the requested and the answering model. It carries
      the REQUESTED id, which is what every v1 consumer already reads and
      revalidates. Widening a deprecated closed shape whose whole promise is
      byte-identical stability is the one thing contract-v1.34's deprecation
      forbids, and the fix is the v2 envelope, which exists. Recorded at the v1
      arm in `serve.py` and in the CHANGELOG entry rather than fixed. The SIDECAR
      on the v1 lane does name the answering model, because it is written above
      the branch.
      The CREDENTIAL SENTENCE IS NOW IN THE RELEASE, which is what P3-23 asked
      for: the schema's own description and the CHANGELOG entry both name the
      provisioning step — an API-backed entry's credential is provisioned into
      the `doxbench-bridge` PROFILE by the ratified broker lane
      (`add-model-provider-broker`), the adapter holds and fetches nothing
      because its child environment is an allowlist, and a keyless self-hosted
      provider needs none.
      THE TAG IS NOT CUT HERE. Per the versioning policy the annotated
      `contract-v1.38` tag is published against the commit that actually lands,
      so this tick claims the CHANGELOG entry (the availability test), the
      recomputed manifest digest, the bundle bump and the 190-entry digest
      inventory built AFTER that bump — `verify-commit` passes on the cut — and
      the consuming repin carries the `unpublished:contract-v1.38` sentinel until
      a follow-up commit resolves it, exactly as 13.3 did for `contract-v1.34`.
      **FLAGGED — THE VERSION IS v1.38, NOT v1.37.** Main moved under this
      slice: `6cbb4495` (PR #235, identity-brokering + trust-anchor) allocated
      `contract-v1.37` while this was in flight, although its own squash message
      still says "at contract-v1.36". CHANGELOG presence is the availability
      test, so v1.37 was taken and the next available number is v1.38.
      **FLAGGED, NOT this task's to fix — repaired by its own lane, AND BACK.**
      At `6cbb4495`, `validate-contract-release.py verify-commit` exited 1 with
      `HGR-RELEASE-INVENTORY-MISSING`: that cut bumped the bundle to v1.37
      without shipping `contracts/releases/contract-v1.37.digests.yaml`, the same
      class of miss `contract-v1.36`'s first tag hit, one step earlier. Recorded
      rather than repaired here, because a release surface belongs to the release
      that cut it — and `c1ffa0fd` (PR #238) shipped that inventory, at which
      commit `verify-commit` PASSED. It is RED AGAIN at `8924838d`: `e11a057b`
      (PR #242) edited `contracts/CHANGELOG.md`, a v1.37 inventory MEMBER,
      without rebuilding v1.37's inventory, so `verify-commit --commit
      origin/main` exits 1 with `HGR-RELEASE-DIGEST-MISMATCH` on that file
      (bisected: green at `c1ffa0fd`, red from `e11a057b`). Still that lane's to
      repair, and still the same habit this note names. This cut resolved its own
      v1.38 inventory throughout and was never affected in any of those states.
      **Judgement call, flagged — the badge covering is SEGMENT MEMBERSHIP over a
      DECLARED SEPARATOR, and the first answer was WRONG.** The ratified THEN is
      that a routing entry "MUST ... carry the handling badge of every model it
      may route to", *because* an entry that hid a routing decision would "report
      a handling posture it does not control". The entry's own `data_handling` is
      the ONE badge string the selector shows for it, so the covering must be
      about that string.
      **OVERTURNED AT ADVERSARIAL REVIEW ROUND 1 (F1).** This slice first shipped
      the covering as raw substring containment, which is wrong in exactly the
      direction the requirement exists to prevent, and the reviewer broke it
      twice on the released bytes: a rule badged *"Routes to a non-tenant
      endpoint."* was accepted as carrying a target badged *"on-tenant"*, because
      `"on-tenant" in "non-tenant"` is True — so the menu would show the INVERSE
      of the posture it routes to — and a rule ending *"...retain nothing."* was
      accepted as carrying a target badged *"retain"*. Both false-accepts passed
      BOTH gates. The same review found the predicate simultaneously
      OVER-strict in the harmless direction: a trailing full stop, a capital, or
      a line wrap all refused a badge that was plainly present.
      The rule is now: a routing entry's `data_handling` is a list of badge
      segments joined by `" / "` — the separator is DECLARED in the schema — and
      each routed model's own badge must be one of those segments, compared with
      whitespace collapsed, case folded and trailing `.;,` dropped. Extra
      segments are permitted, so a rule keeps its own lead-in. INTERIOR
      characters are never rewritten, and that is the load-bearing part: it is
      exactly where the difference between `on-tenant` and `non-tenant` lives, so
      no normalization may touch it. A test pins that the three forgiven
      transformations cannot make a different posture compare equal.
      The separator is `" / "` because a badge is free prose and any separator
      can collide with one: `;`, `.` and `,` all occur in the packaged badges and
      `/` does not. The residual collision is REFUSED rather than hoped away — a
      routed entry whose own badge contains the separator could never be one
      segment, so that catalog is refused as ill-formed. (Revert-testing showed
      that refusal, and the explicit self-reference refusal F2 asked for, are
      DIAGNOSTICS rather than independent guards — the covering rule and the
      chained-rule rule respectively refuse the same catalogs under a misleading
      name — so each is pinned on its own finding CODE and MESSAGE, which is the
      only guard that fails if the arm is deleted.)
      The alternative — per-target badge OBJECTS on the wire plus a view that
      composes them — was designed and REJECTED, and the reason survives the
      correction: it duplicates authored text that then drifts from the target's
      own entry. What did NOT survive is the claim that containment "buys nothing
      the covering rule does not already guarantee"; containment guaranteed the
      wrong thing. The consequence is stated rather than hidden:
      `data_handling`'s pre-existing 500-byte ceiling is UNCHANGED and therefore
      bounds how many segments one rule can carry. Widening that ceiling was
      rejected as a consumer-visible change to an existing field, which the
      additive class does not permit.
      **Judgement call, flagged (`routes_to` holds REFERENCES, not badges).** The
      routable set is a list of `model_id` handles resolved inside the same
      catalog, so each badge has exactly one authoring home — the target's own
      entry — and PUBLIC-ONLY BY CONSTRUCTION is preserved trivially, because an
      opaque catalog handle can express nothing a plain entry could not already
      express. §11.6's ruling that the harness provider id belongs on
      `LaunchConfig.provider_id` and NOT on the catalog entry is therefore
      untouched: the entry is still closed, `provider_id` on it is still refused
      structurally, and a test asserts that against these exact bytes.
      **Judgement call, flagged (disclosed only when DECLARED).**
      `as_public_dict` emits the three keys only for an entry that IS a routing
      rule, so a plain entry's public dict is byte-identical across the release
      boundary. Always emitting them with plain-model defaults was rejected: it
      would change the bytes of every catalog response that exists, hand every
      consumer a `resolved_model_id: null` it never asked for, and put
      `routes_to: []` on entries the schema forbids to carry it. The WIRE is
      additive in both directions and tolerates an explicit `routing_rule: false`
      with no siblings — it is simply not what this projection emits — so a
      consumer must not read omission and explicit-false as different facts.
      **Judgement call, flagged (three rules the ratified text does not literally
      state) — and rule 5 was RULED BY BRETT after the review.** Rule 3 (an
      AVAILABLE rule must resolve to an AVAILABLE model), rule 5 (a rule may
      declare no more headroom than the model that answers) and rule 2 (no
      chained rule) are all inferred from how the turn gate actually works:
      `dispatch_turn` checks availability, `effective_limit_bytes` computes the
      budget from the SELECTED entry — which for a routed turn is the RULE — and
      `selected_model`'s resolved id is recorded as the model that ANSWERED, so
      it must name something that answers. Without them an available `auto` could
      dispatch to a model the catalog calls unavailable, admit a turn its
      destination cannot take, or resolve to a second indirection. All three
      refuse the WHOLE catalog rather than dropping an entry, matching the
      duplicate-`model_id` posture, and an UNAVAILABLE rule is exempt from rules
      3 and 5 — which is also what keeps the bridge's degraded projection
      (`catalog()` marking every entry unavailable) constructible.
      **RULE 5 -> RULE 5', RULED BY BRETT 2026-08-21, in-session: "Swap to rule
      5'".** The adversarial review upheld rules 2 and 3 outright and upheld rule
      5 only WITH RESERVATION — it permanently capped an `auto` entry's declared
      limits at its NARROWEST destination to compensate for the runtime computing
      budgets from the selected entry. The bound is now the RESOLVED model's
      alone. Three reasons: under this release's STATIC resolution the promise
      that matters is that the menu's declared limits are honoured by the model
      that actually answers; the un-resolved destinations are not load-bearing,
      because no turn reaches them while the rule resolves elsewhere; and
      min-capping would BAKE IN semantics contradicting the sanctioned future
      direction — a per-turn, FIT-AWARE router choosing a destination by the
      assembled packet's size and by other capability dimensions, which Brett
      ruled "Stage the topic" for the same day and which is now
      `ideation/staging/doxchat-auto-fit-routing/` (registered with his
      requirements as a VERBATIM origin quote, 6 claims, 6 open questions,
      sequenced after this sprint archives). Under that design a rule's declared
      ceiling is the WIDEST thing it can serve, not the narrowest, and a min-cap
      would have had to be undone to get there. A packaged POSITIVE carries the
      difference rather than leaving it to prose —
      `workbench-model-catalog-routing-rule-wider-than-a-non-resolved-member`
      declares 800,000 bytes while a routable-but-not-resolved member accepts
      2,048, and is VALID where the first form refused it — with a test named for
      the ruling and a revert-test proving the old min-cap fails exactly that
      test and nothing else.
      **NO VIEW CHANGE, and it is proved rather than argued.**
      `doxbench-chat.js` already renders each option as `label — data_handling`
      and `sendDisclosure` already names the selected entry's `data_handling`, so
      for a conformant rule both already show every routed badge — the covering
      rule is what makes that true. A node probe mounts the SHIPPED rail over the
      packaged routing catalog and asserts the `auto` option's visible text
      contains both routed badges; if a future release moved the badges off
      `data_handling` that probe fails and a view change is then owed.
      `adoptCatalog` spreads the whole entry (`{...entry}`), so the three new
      fields reach browser state rather than being silently projected away, and
      `staging-workbench-model.js` reads only an approved-model COUNT and is
      untouched.
      **RECONCILIATION with `add-doxchat-model-intake` (ratified, UNBUILT), stated
      rather than silently diverged (#226's lesson).** That change's packet is
      another lane's and is NOT edited here; its "closed seven-field shape"
      descriptions were true when it was ratified and its own no-widening promise
      is about its own delta. What changed is the referent — the closed entry is
      now the v1.38 shape, seven required base fields plus the three optional
      routing-declaration fields — and its task 3.5 should be read against that
      shape when the lane builds. A proposed-versus-approved distinction is still
      not a widening of it. Recorded in the CHANGELOG entry as well, so a reader
      of the release finds it without reading this task.

## 12. Share-session

- [x] 12.1 The verb: commit threads → `push` (the pull-request port's EXISTING
      member) → return and record the pushed ref. No `open_or_update`, no pull
      request, no review request, no approval or merge authority.
      `gate_routes.execute_share_session` — three steps and no fourth, beside
      `execute_open_pr` because §12 requires REUSING that remote-write path
      rather than introducing a second one. The forbidden set is DERIVED
      (`FORBIDDEN_SHARE_OPERATIONS` = `session_pr.PORT_OPERATIONS` minus `push`),
      so a port that grows a fourth member fails the assertion instead of
      silently widening the verb, and it is asserted against the port's own CALL
      LOG rather than against source text.
- [x] 12.2 Nothing pushes implicitly: no Save, turn, compaction or scheduled
      task may push. A test asserts the negative.
      §11's four-module source sweep is EXTENDED rather than restated: the list
      moved to `tests/ideation-dashboard/conftest.py` as
      `NO_IMPLICIT_PUSH_MODULES`, §11's test now reads it from there, and §12
      widened it to SEVEN — adding the turn assembler, the packet builder and the
      scheduled lane, which is the "periodic task" the requirement names. §12's
      test also asserts §11's four are a SUBSET, so the list can be widened and
      never quietly narrowed; two copies of a negative drift apart invisibly,
      because both copies keep passing. Two BEHAVIOURAL negatives sit beside it:
      a real Save through the real route with a port that would record a push and
      does not, and the bare-origin check that the branch is absent from the
      remote until the verb runs.
- [x] 12.3 Invoked with nothing new, it reports that honestly rather than
      pushing again.
      **"NOTHING NEW" IS TWO CONDITIONS, AND ONE WOULD HAVE BEEN A DEFECT** — no
      dirty thread sidecars AND the remote already at this sha. Reading only
      dirtiness looked sufficient and is not: nothing pushes implicitly, so a run
      of Saves leaves NO dirty sidecar and several unpushed commits, which is the
      ordinary state a share exists to publish. One condition would have reported
      "nothing to share" and stranded the colleague. Decided by
      `plan_share`, a side-effect-free read (`git status` plus `ls-remote`, which
      never fetches) taken BEFORE the port is touched, so the honest answer costs
      no remote write. Both arms are pinned, and the revert of the second
      condition fails three tests.
- [x] 12.4 Loopback-only, fail-closed on an unresolved actor, console-presence
      demonstrated, recorded as a human gate action; local-plane only, and a
      copyable descriptor where the gate capability is absent. The push identity
      follows the plane rule the save verb already carries.
      Every posture is INHERITED rather than forked: loopback-only and the
      capability refusal come from `_handle_gate_action`, console presence from
      membership in `SESSION_BEARING_VERBS` (which is what makes FR-019's third
      clause ENFORCED for this verb rather than merely observed), and the plane
      rule from the same `session_pull_requests` port `open-pr` is handed — a
      plane that declares none is refused with the FR-034 sentence naming the
      invoking engineer's own credential. `share_session_gate_factory` is
      deliberately NARROWER than the Save's: records tree only, no thread prefix,
      because a share writes no sidecar (it commits ones already on disk).
      The descriptor half is the session panel's existing FR-046 posture, which
      is why the CLI verb `cli.py gate share-session` had to exist: the
      descriptors are asserted by PARSING each one with the real CLI parser.
- [x] 12.5 A colleague's resume path is exercised end to end: fetch the shared
      branch, open the tile, join the session, see the threads.
      Driven as a REAL test against a REAL bare-repo origin on disk: share, clone
      the origin into a separate directory, check out the shared branch, and find
      both the document and its thread. **P3-17 IS DISCHARGED HERE** and has its
      own named test — a document created, DISCUSSED via a dirty sidecar and
      never Saved again, followed through that clone to prove the thread arrives;
      it fails with "the thread did not travel" if the sweep regresses.
      **THE FAILED-THEN-RETRIED TRAIL, stated because the composite is worth
      knowing even though each half is truthful.** A branch-resident record must
      ride the commit it describes (FR-006), so it is written BEFORE the push it
      names; if that push then fails, the branch carries a record of the failed
      attempt and the retry — which finds nothing dirty and takes the
      main-resident path — puts the successful one in the served checkout. An
      auditor therefore finds TWO share records for one delivered share, in two
      places. Each is individually accurate about the act it recorded, and the
      false-looking one is unreachable while it is false: its only copy sits on a
      branch no remote has. Pinned by three tests in the FAILURE WINDOW section.
      The mechanism is `doxbench_threads.shareable_thread_paths`, a
      CROSS-DOCUMENT sweep by prefix over the worktree's dirty set, committed as
      the share's OWN single gate action. It is a separate function from
      `branch_session._dirty_thread_paths` rather than a widening of it, and that
      is the point: the Save filter stays scoped to the one document being saved,
      which is what keeps one document's sidecar out of another's Save commit.
      Both halves are pinned in one test.
      **OBLIGATION RECORDED HERE BY §11 (adversarial review P3-17), because this
      is the task that will meet it.** A thread rides only ITS OWN document's
      Save, and only while its sidecar is DIRTY (task 9.2's filter, which is
      load-bearing — declaring a clean path refuses the Save). So a document
      that was DISCUSSED but never Saved again keeps an UNCOMMITTED sidecar, and
      an uncommitted file does not travel on the branch this task's colleague
      fetches: they resume with that document's thread missing, silently.
      Nothing in §11 can close it — committing a thread without its document
      would break the one-commit-per-gate-action rule 9.2 exists to honour, and
      §12's verb is the first thing with a reason to commit threads on their
      own, which is why the obligation is recorded against THIS task rather
      than left in a ticked one. The cross-document half is sound and stays so:
      `_dirty_thread_paths` derives its candidates from the document being
      saved, so one document's sidecar can never join another's commit.
- [x] 12.6 (Scope call, recorded in the proposal) this slice MAY trail as a
      later realization slice; its CONTRACT does not.
      **RESOLVED 2026-08-21 BY BRETT'S RULING: exit (a) — realize §12 as its own
      slice against this change.** The scope call was real and is kept here
      rather than deleted: §12 DID trail, by three slices, exactly as this task
      anticipated, and the contract did not — the share-session requirement was
      ratified with the rest of Phase B and has been binding throughout. What the
      ruling settles is only which of the two recorded exits was taken. Exit (b)
      (carve §12 into a successor change and narrow this change's `code_surface`)
      was NOT taken and needs no disposition, because it was a contested-class
      act that is now moot.

- [x] 12.7 **RELEASE OBLIGATION — the annotated tag and the submodule pin for
      `contract-v1.36`.** Realizing 12.4 required an ADDITIVE growth of
      `gate-action-record.schema.yaml`'s `action` enum, and this task carries the
      half of that release the slice cannot perform in-branch.
      **WHY A CONTRACT CHANGE AT ALL — this was a scope discovery, and the
      implementer brief said there would be none.** The ratified requirement says
      share-session "SHALL be recorded as a human gate action naming the branch
      and the pushed ref". Gate-action records are validated against that schema;
      its `action` enum was CLOSED at seventeen members with no `share-session`;
      the file is digest-pinned in `contracts/manifest.yaml`; and the shapes each
      verb emits are validated as files on disk by
      `tests/ideation-dashboard/test_session_records.py`. So the action could not
      be recorded honestly without the enum, and the enum could not grow without
      recomputing a pinned digest — which `contract-v1.35` establishes is a
      release cut even when `contract_schema_version` stays `1`.
      REUSING AN EXISTING ACTION WAS CONSIDERED AND REJECTED: `open-pr` is the
      only near fit, and its own conditional REQUIRES a `pull-request` artifact,
      so recording a share as an open-pr would both fail validation and assert a
      pull request this verb is forbidden to open.
      DONE IN-BRANCH, all of it inside ONE commit so the cut reverts as a unit:
      the enum member, a conditional constraining only the new member, the
      recomputed `manifest.yaml` digest, the `consumption_rule`, the CHANGELOG
      entry (CHANGELOG presence is the availability test under the versioning
      policy, not tag presence), and the RELEASE DIGEST INVENTORY
      `contracts/releases/contract-v1.36.digests.yaml` — built with
      `scripts/validate-contract-release.py build`, 190 entries, exactly three
      digests moved (the changelog, the manifest, and the schema itself, which is
      a release-inventory member). The inventory ships INSIDE the cut because
      both precedents did — `contract-v1.34` at `5daa173` and `contract-v1.35` at
      `78f8e01` — and because no gate in the local set would have caught its
      absence: its only consumer test lives in the environmentally-broken
      `tests/hermes_runtime_contracts` suite. It was missing from the first
      version of this cut and was added by the §12 review (P2-1).
      **THE TAG HALF IS DISCHARGED — `contract-v1.36` IS PUBLISHED AND
      VERIFIED.** Brett RATIFIED the cut 2026-08-21; PR #234 squash-merged as
      `08c5aa9`; every gate reran at that exact commit before anything was
      tagged (identical tree to the branch tip `a734417`; ideation-dashboard
      3733 passed / 15 skipped, ideation_dashboard 63, doc-health 691,
      proposal-support 31, `openspec --all --strict` 63 passed, the dashboard
      validator 0 errors / 4 by-design warnings, manifest digests 135, doc-health
      zero-new against a same-clock `5f59a32` baseline).
      **THE FIRST TAG WAS WRONG AND THE POLICY'S OWN VERIFY STEP CAUGHT IT**,
      which is worth recording because it is the step earning its place:
      `validate-contract-release.py verify-commit` failed at the freshly
      published tag with three `HGR-RELEASE-DIGEST-MISMATCH` errors on exactly
      the three files the cut changed. The digests were correct; the cut had left
      `contracts/manifest.yaml`'s own `contract_bundle_version` at
      `contract-v1.35`, and `resolve_committed_inventory` deliberately reads that
      line at the commit so historical inventories are ignored — so the tool
      correctly checked v1.36's tree against v1.35's inventory. Every prior cut
      bumps that line (`5daa173` for v1.34, `78f8e01` for v1.35) and this one had
      not. Corrected on main at **`d37cfa1`** — the bundle version plus the
      rebuilt inventory, since the manifest is itself an inventory member — and
      the annotated tag was RE-POINTED there rather than burning `v1.37` on the
      error, which was safe only because the tag was minutes old in the same
      session with no submodule pin yet referencing it.
      The tag now verifies from the REMOTE rather than from the local ref that
      created it: tag object `42c76966d91e4eeb1dd6b7f34efa78cf550586c8`,
      dereferencing to `d37cfa1095ffb2558efb65e0b44d6c683501423a`
      (`git ls-remote --tags origin`), annotated, with
      `validate-contract-release.py verify-commit --commit contract-v1.36` and
      `verify-tag --remote origin --tag contract-v1.36` both PASSING against
      `contracts/releases/contract-v1.36.digests.yaml`.
      NO SENTINEL TO REPLACE, unlike 13.3's `contract-v1.34`:
      `doxbench_contracts.CONTRACT_REF` pins the CHAT-TURN family's release
      commit, and v1.36 grows a different schema that no code pins by ref.
      THE PIN HAS LANDED, completing the ledger: the aggregation repo
      (`opensoft/xFactory`) pins this repository at `3f9aa8e` (the commit that
      recorded the tag half) in its commit `04366e3`, pushed 2026-08-22 by the
      orchestrating session immediately after the tag verified — with the
      gitlink object's existence checked inside the submodule first, per the
      standing pin-sync discipline. Nothing on this task remains.
      **A FAMILY-WIDE SCHEMA NOTE** (§12 review, P3-7), recorded in full in the
      `contract-v1.36` CHANGELOG entry because it is a property of the whole
      per-action conditional family rather than of this cut: a conditional of the
      form `if action then artifacts contains kind` REQUIRES a companion artifact
      but does not FORBID the others, so the schema does not prevent a
      `share-session` record from carrying a `pull-request` artifact.
      `abandon-session` has had the identical hole since
      `add-workbench-branch-sessions`. The runtime is what forbids it — the verb
      reaches exactly one port member, asserted against the port's own call log —
      and closing it schema-side would narrow several pre-existing actions that
      already have valid records in the corpus.
      **This is a JUDGMENT CALL and it is separable**: the contract growth is its
      own commit and reverts as a unit if Brett rules the other way.

**§12 IS THE BLOCKING STATE FOR THIS CHANGE'S ARCHIVE — adjudicated 2026-08-21
from the record, at the landing.** Brett ruled the same day that §12 trails; the
landing round then had to answer whether this change can archive with §12
recorded as a trailing successor. It cannot. The record says so three times over,
and the reading is the honest one rather than the convenient one:

1. **The gate is written over the WHOLE code surface.**
   `release-realization`'s *Realization archive gate*: "A change with a
   non-empty code surface SHALL NOT archive until realization evidence exists:
   its code merged on the implemented target … **Until then the change remains
   active as approved-but-unrealized intent**, preserving the invariant that
   promoted specs describe what the code does." This change's `code_surface:`
   names `session_pr.py`/`gate_routes.py` — "share-session reusing the port's
   existing `push` member and opening no pull request" — and that code is not
   written. Not "mostly merged": the gate has no proportion in it.
2. **Archiving would promote a SHALL that the code does not do.** §12's delta
   is an ADDED requirement, *"Share-session hands a live session to a
   colleague"*, whose text is a page of SHALLs about a verb, a push identity, a
   gate-action record and a hosted-plane absence. Promotion would put all of it
   in `openspec/specs/ideation-dashboard/spec.md` as description of the built
   system. That is exactly the invariant the gate names, violated directly.
3. **The record supports a successor CHANGE, never a trailing promise inside an
   archived one.** Searched for a mechanism and there is none: no promoted spec
   defines a trailing-realization or successor-slice archive. What the corpus
   does contain is the opposite pattern, stated repeatedly — "a tunable
   configuration would be a **successor change**", "any future override would be
   … defined by a **successor change**", "per-tile repository binding remains a
   **successor change**". The sanctioned way to land nine-tenths and defer one is
   to carve the tenth into its own change, not to archive the parent over it.
   The `recurrence-crystallization` topic is the worked precedent for the
   adjacent case (partial promotion, remainder left staged and named).

**Mechanically the sanctioned path already refuses**, independently of the
reading above: `scripts/proposal-support.py archive` raises "change has
incomplete tasks" on any `- [ ]` in `tasks.md`, and 12.1–12.6, 11.7 and 13.8 are
open. So archiving Phase B today would require going around the archive gate,
which is the one thing the standing rule forbids.

**Therefore: this change stays ACTIVE, and Phase B was NOT archived in the
landing round.** Two exits exist and BOTH are Brett's call, not this round's:

- **(a) Realize §12** as its own slice against this change — the shape 12.6
  anticipated.
  **CORRECTED 2026-08-21, at §12's realization: the clause that used to end this
  line — "then 13.8 ticks and the whole change archives" — WAS AN OVERCLAIM, and
  it contradicted the F5 ledger printed a few paragraphs below it.** Realizing
  §12 does not tick 13.8 and does not archive the change. 10.7 and 11.7 are still
  open, each owes a contract release that has not been cut, and the archive gate
  is written over the WHOLE code surface with no proportion in it. §12 was the
  largest of the three blocking families and it is now closed; the change stays
  ACTIVE on the other two. Left as a correction rather than a silent edit
  because a false promise in the record is what the next session would have
  planned against.
- **(b) Carve §12 out** into its own successor change, narrow this change's
  `code_surface:` to what shipped by a recorded ruling, move the share-session
  delta with it, then this change archives and the successor carries its own
  gate. Note this is a `code_surface` amendment after ratification, which is a
  contested-class act and needs the disposition to say so.

**§12 IS NOT THE WHOLE LEDGER — corrected 2026-08-21 (review finding F5).** The
first version of this note named §12 alone, which would have put a partial
ledger in front of the ruling. NINE tasks are open, across THREE families, and
only one of them is §12:

| open | what it needs | who can close it |
|---|---|---|
| ~~**10.7**~~ | ~~an additive **chat-turn-success** release carrying the assembled context's posture (`full \| reduced`) and its reason — the packet half is built and the browser half has no field to land in~~ | **CLOSED 2026-08-22** — cut as `contract-v1.39`; the record now carries `context_packet` (posture + the reduction's own reason, present iff reduced), the rail states the reduced posture to the human, the packet's ASSEMBLY was not rebuilt (`assemble_packet` and both `REDUCED_*` constants byte-identical, `test_doxbench_packet.py` unmodified; the construction gate's full-arm predicate was tightened at the bot round so the three-gates-one-rule claim holds), and `verify-commit` passes on the cut |
| ~~**11.7**~~ | ~~an additive **model-catalog** release — the released entry is a CLOSED seven-field shape, so no conformant catalog can declare `auto` as a routing rule; the runtime already honours one~~ | **CLOSED 2026-08-21** — cut as `contract-v1.38` (v1.37 was taken mid-flight by PR #235); the entry now carries `routing_rule`/`routes_to`/`resolved_model_id`, the runtime was not rebuilt, and `verify-commit` passes on the cut |
| ~~**12.1–12.6**~~ | ~~share-session: the verb, the no-implicit-push negative, the nothing-new report, the four postures, the colleague resume path (which also carries P3-17's uncommitted-sidecar tail), and 12.6's own scope call~~ | **CLOSED 2026-08-21** — realized as its own slice under Brett's exit (a); P3-17 discharged |
| ~~**12.7**~~ | ~~the annotated tag + submodule pin for `contract-v1.36`, the additive `share-session` enum growth 12.4 turned out to require (the in-branch half is done; see the task for why it was unavoidable)~~ | **CLOSED** — struck 2026-08-21 as a bookkeeping correction, on the authority of the task's OWN already-ticked discharge: `contract-v1.36` is tagged and the aggregation repo's pin landed at `04366e3`, and 12.7's body ends "Nothing on this task remains." The row simply outlived it |
| ~~**13.8**~~ | ~~the realization-evidence tick, which cannot be true until the code surface is whole~~ | **CLOSED 2026-08-22** — every row above is struck, so the code surface IS whole; ticked at 10.7's release, which was the last to land. The published tag and the landing sha are the post-land step the task names, not a claim it makes |

So the two contract-release obligations are NOT waiting on §12 and do not become
satisfiable by carving it out: even with share-session gone, 10.7 and 11.7 would
still hold this change open under the same archive gate, because each names a
release that has not been cut. Option (b) above therefore narrows the blocking
set from three families to two — it does not clear it.

**UPDATED 2026-08-21, after §12 realized under exit (a).** The ledger above is
now: NINE open tasks became FOUR, and THREE families became three again rather
than two, because §12's realization discharged 12.1–12.6 and created 12.7. That
is not a regression — it is the same additive-release obligation 10.7 and 11.7
already carry, discovered at the only point it could be (the requirement's
"recorded as a human gate action" meets a closed enum), and its in-branch half is
already done. The honest headline is that this change is now blocked by exactly
ONE thing in three places: **three additive contract releases that have not been
cut.** No verb, route, or runtime behaviour is missing any more.

**UPDATED 2026-08-21, after 11.7's release landed — and CORRECTED the same day
at that release's adversarial review (F5), which caught this note overstating
the blocking set.** FOUR open rows became TWO, not three. `contract-v1.38`
carries the model-catalog routing rule, so 11.7's row is struck; and 12.7's row
is struck too, as bookkeeping rather than news — that task has been TICKED since
§12's release landed, its tag is published, its aggregation pin is at `04366e3`,
and its body ends "Nothing on this task remains." The row had simply outlived
the task.

**The residual set is therefore 10.7 and 13.8**: one additive
chat-turn-success release carrying the assembled context's posture, and the
realization-evidence tick that cannot be true until it lands. The headline is
otherwise unchanged: what holds this change open is a contract release, not
missing behaviour.

**UPDATED 2026-08-22, after 10.7's release was CUT — not landed; see the verb
below. TWO open rows became ZERO, and the table above has no unstruck row
left.** `contract-v1.39` carries the chat-turn record's `context_packet` — the
assembled context's posture and the reduction's own reason — and the browser
surface states the reduced posture to the human, which was the half 10.7 stayed
open for. 13.8 ticks with it, on its own terms.
**THE VERB, HERE TOO (adversarial review S3, residual).** An earlier version of
this paragraph said the release had "landed" and that the gate's sentence ("its
code merged on the implemented target", over the WHOLE declared code surface)
"is true … and it now is". Both are the same overclaim 13.8's own block was
corrected for, sitting in the summary a reader reaches FIRST. What is true is
that the whole surface is BUILT AND GATED on a branch off the implemented
target; MERGED — and LANDED — become true at the landing squash and not one
commit before it.

**So this change is no longer blocked on anything it can do itself.** Every task
box is checked. What remains is NOT a task: `contract-v1.39` is cut but its
annotated tag is published against the commit that actually LANDS, so the
post-land step is the one §11.7 performed — rerun every gate at the squash,
publish and remotely verify the tag, then resolve the
`unpublished:contract-v1.39` sentinel in `doxbench_contracts.CONTRACT_REF` and
record the squash sha in 13.8's block.

**ARCHIVING IS STILL BRETT'S ACT AND WAS NOT PERFORMED.** The mechanical refusal
that stood in the way ("`proposal-support.py archive` raises 'change has
incomplete tasks' on any `- [ ]`") no longer applies, and that is a statement
about the gate rather than permission to walk through it: the exits above are
Brett's call, the archive runs through `proposal-support` on his explicit word,
and nothing here decides it.

Note for whoever cuts that release — 11.7's realization found that PR #235 had
taken `contract-v1.37` mid-flight AND left
`contracts/releases/contract-v1.37.digests.yaml` absent, so
`verify-commit --commit 6cbb4495` exited 1. PR #238 shipped that inventory and
`verify-commit` PASSED at `c1ffa0fd` — then PR #242 (`e11a057b`) edited
`contracts/CHANGELOG.md`, a v1.37 inventory member, without rebuilding v1.37's
inventory, and main is RED again at `8924838d` with
`HGR-RELEASE-DIGEST-MISMATCH`. So expect to find the preceding release surface
failing when you get there, and check rather than assume. The two habits the
episode earns are unchanged and now doubly earned: recheck bundle availability
against the CHANGELOG at the moment you allocate, and REBUILD THE INVENTORY
whenever you touch an inventory member — the CHANGELOG is one.

Whichever Brett picks, the next session starts here. Nothing else in the wave-2
landing is blocked by it: Phase A is archived, the staged topic is exited, and
the realization evidence for everything built is recorded in `proposal.md`.

## 13. The contract release, and landing

- [x] 13.1 `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml` gains a
      second, CO-RESIDENT envelope family: the v1 request/success/failure stay
      BYTE-IDENTICAL and keep validating (a test asserts the bytes), and the new
      family carries the outline plus N document buffers, the bound-buffer key
      on request and record, per-buffer observed hashes keyed by buffer, a
      buffer-key proposal target, and the selected-model metadata.
      Released at **contract-v1.34** as `workbench-chat-turn-v2` /
      `-v2-success` / `-v2-failure`, added to the file's top-level `oneOf` and
      discriminated by `kind` exactly as the three v1 envelopes already
      discriminate each other. Every closed constraint the design named widens in
      the NEW family only: `buffers` `minItems: 2, maxItems: 2` → `maxItems: 25`
      (the declared 24-document loaded-set bound plus the reserved outline);
      `observed_hashes`' exact `{outline, document}` keys → a map keyed by BUFFER
      KEY with `outline` still required; `typed_proposal.target`'s two-value enum
      → a buffer key; `proposals.maxItems: 2` → the buffer-set bound, with the
      one-per-supplied-buffer RULE staying the delegated validator's. The v1
      bytes are asserted against a COMMITTED BASELINE
      (`tests/ideation-dashboard/fixtures/chat-turn-v1-envelopes.baseline.yaml`),
      not by re-validating an instance — a widened `maxItems` would still
      validate. The widened request carries NO `active_document_path`: the
      binding is declared, and the closed envelope leaves nothing to infer it
      from.
      **JUDGEMENT CALLS, flagged rather than buried.** (a) The design says
      `buffer_state.kind`'s two-value enum "must widen"; design §1.1 also says
      the KIND vocabulary "stays exactly this". Both hold only if what widens is
      the buffer's IDENTITY, which moves from `kind` to the derived buffer key —
      so `buffer_state` is REUSED unchanged by the widened family and no
      redundant `key` field is added that could disagree with `path`.
      (b) `additionalProperties: false` stays false: what widened is the closed
      property SET, not the closedness. (c) The envelope-level `schema_version`
      stays `1` beside the file's own (D16).
- [x] 13.2 The v1 family is DEPRECATED in the same release with its removal
      target recorded. Change class stated as ADDITIVE (minor) plus a
      deprecation, per `docs/contract-versioning-policy.md`.
      Recorded in THREE places, each for a different reader: the schema's own
      top-level `deprecated_envelopes` block (machine-readable, and placed
      OUTSIDE every envelope precisely so the deprecated bytes do not move); the
      CHANGELOG entry, which states the class against the policy's own test and
      carries the migration note; and the policy's "Deprecations Currently In
      Force" list. Removal target **contract-v2.0** — the next major, which is
      the earliest release at which removing a released shape is legal, and this
      release is the full minor of deprecation the breaking path requires.
      Deprecated is not withdrawn: all six kinds stay dispatchable, and a v1 turn
      is still served and still answered in ITS own family.
- [x] 13.3 The bundle version is ALLOCATED AT REALIZATION through the
      serialized realization order — fetch, rebase, recheck availability,
      allocate, update manifest + CHANGELOG + digest inventory atomically with
      the schema, gate and review the exact candidate commit, land it, then
      publish and verify the annotated tag. No number is reserved before then.
      **DONE — the tag exists.**
      Fetched origin, confirmed the branch already sat on `origin/main`
      (`a4a6f6e`, no rebase needed), rechecked availability at allocation time —
      `contract-v1.33` present in the CHANGELOG and manifest with no published
      tag, `contract-v1.34` absent from the CHANGELOG, the manifest, the
      `contracts/releases/` inventories and the remote tags — and allocated
      **contract-v1.34**. Manifest, CHANGELOG, README, the versioning policy's
      deprecation list and `contracts/releases/contract-v1.34.digests.yaml` moved
      ATOMICALLY with the schema in one commit. NO TAG IS PUBLISHED on this
      branch: steps 4-5 (land the exact reviewed commit, then publish and verify
      the annotated tag from an independently refreshed checkout) happen after
      merge, against the commit that actually lands.
      **STEPS 4-5, DISCHARGED AT THE LANDED COMMIT.** PR #210 squash-merged as
      **`5daa1731f24010356b044971328f8a7aa321994c`** on `origin/main`. Because a
      squash creates a NEW commit, every gate reran against that exact commit
      before anything was tagged — `verify-commit` pass, the dashboard validator
      0 errors / 4 deprecation warnings / exit 0, `openspec validate --all
      --strict` 61 passed, doc-health 0 new regressions, and the three ideation
      suites run separately (3174 + 63 + 665 passed, 7 skipped) — and the
      availability recheck confirmed no `contract-v1.34` tag had appeared.
      The annotated tag is PUBLISHED and VERIFIED: tag object
      `439d76b88044edbb22ccf677d57e76dd8a6da350`, dereferencing to
      `5daa1731f24010356b044971328f8a7aa321994c` — confirmed from the remote
      (`git ls-remote --tags`) rather than from the local ref that created it,
      and `validate-contract-release.py verify-commit --commit contract-v1.34`
      reproduces every digest in
      `contracts/releases/contract-v1.34.digests.yaml` from the tag's own
      objects.
      **THE SENTINEL IS REPLACED**, which is what closes this task rather than a
      follow-up anyone could forget: `doxbench_contracts.CONTRACT_REF` carried
      `unpublished:contract-v1.34` across the realization branch — a value no
      `stack.yaml` can declare, so a CONSUMER comparing against it refused
      rather than matched by accident — and now names the published commit, in
      the same spelling the v1.31 pin used (the tag's dereferenced commit, never
      the tag object).
- [x] 13.4 The runtime keeps resolving its pinned wire schemas from the checkout
      it runs in, and both model routes keep refusing before consulting any port
      when a pinned contract cannot be read. The repin is digest-checked.
      `doxbench_contracts` moved v1.31 → v1.34 with the chat-turn digest (the
      catalog's is unmoved), and the repin is NOT digest-neutral because the
      release widens that file itself — a runtime pinned to v1.31's digest cannot
      read v1.34's schema at all, which is the fail-closed chain working. Nothing
      in it relaxed: declared pin, checkout resolution, manifest parity and
      released bytes all still run per request, and both model routes still fail
      closed on an unreadable contract. The route now reads WHICH FAMILY a turn
      arrived in off the payload's own `kind` and answers in that family; the
      gate order, the fixed codes and the redaction are unchanged, and identity
      verification and the request-byte bound run over EVERY loaded document
      rather than the first.
- [x] 13.5 The F2 obligation is verified discharged: the record names the
      DECLARED bound buffer, and no server-side-only field and no inference from
      `active_document_path` remains anywhere.
      The record names it: a route test posts a widened turn bound to the OUTLINE
      while a document buffer rides beside it — exactly the case Phase A's review
      found mis-recorded — and reads `bound_buffer` back off the released success
      envelope. Both negatives are PROVEN rather than described, in
      `tests/ideation-dashboard/test_doxbench_bound_buffer.py`: no
      `PromptEnvelope` field reads as a binding claim (asserted on the dataclass,
      not its docstring) and no runtime module assigns one onto the envelope; the
      widened request envelope is CLOSED and declares no `active_document_path`,
      so a request carrying one is refused by the released validator itself; and
      neither browser module carries the seam that used to feed it. The
      deprecated v1 lane still reads its own declared `active_document_path` —
      that envelope's own field, and reading a KEY off a declared path is a
      spelling change, not the killed derivation — but the handler passes the
      PARSED binding whichever family it came from.
      **N4 DISSOLVED WITH IT** (task 8.6's recorded interim posture): the chat
      binds to the SELECTED buffer through the existing single state authority,
      the binding is declared on the request and echoed in the record, and the
      interim send-gate, its visible reason and the shell's narrowing to the
      reserved slot are REMOVED — not left unreachable. Proven through the REAL
      mount in `test_doxbench_composition.py`: load a document, select it, send,
      and read the declared binding and the whole loaded set off the wire.
- [x] 13.6 The staged topic is EXITED: every question dispositioned, the topic
      folder's transition recorded, and the staging INDEX detail section updated
      to say Phase B carried the remainder.
      All SEVEN questions carry a disposition other than `open` (checked, not
      assumed: `Disposition status: open` appears zero times in the fragment).
      `scripts/proposal-support.py transition` moved
      `ideation/staging/doxbench-editing-model/` into this change's
      `supporting-docs/` on 2026-08-21 — status `staged` → `draft`,
      `Proposed by:` recorded, per-file sha256 manifest plus a byte-exact
      `source-snapshots/` copy — and the change's `.openspec.yaml` origin block
      was diffed byte-for-byte before and after and is IDENTICAL, because an
      origin mutated after ratification is rejected at the archive gate. The
      staging folder is empty by design; the INDEX row and detail section stay
      as the topic's index entry and its exit record, following the
      `staged-topic-outline-template` precedent rather than deleting the row.
      **THE TWO PARKED ITEMS ARE DISPOSITIONED, NOT SWEPT.** A topic exit must
      neither silently adopt nor silently drop what it carried, and this one
      carried two things Brett has not ruled on. Both are named in the INDEX
      detail with a location that survives the exit, and both are LIVE CODE
      rather than prose, so neither can be flipped by a document edit:
      **Headroom** stays watch-listed in `doxbench_packet.WATCH_LISTED_CANDIDATES`
      with all five of the topic's gates, and its `WatchListedCandidate`
      constructor RAISES on `adopted=True`; the **graph-engine graduation
      trigger** stays recorded in `doxbench_knowledge.RESERVED_REFUSAL`, where
      `graph_query` is declared-but-reserved and names the trigger it would have
      to clear. Neither is a task here and neither blocks the landing.
- [x] 13.7 **Archive order:** `add-doxbench-editing-phase-a` must archive FIRST,
      or the three Phase-A-relative MODIFIED requirements have nothing to amend
      and the promoted spec would keep Phase A's F2 deferral clause with nothing
      discharging it (design §9). Verify Phase A's archive before archiving
      this change.
- [x] 13.8 Realization evidence for the archive gate: merged on the implemented
      target through the engineering gates, plus a green run of the runnable
      surface (`release-realization`'s realization archive gate).
      **THE EVIDENCE FOR EVERYTHING REALIZED IS RECORDED** in the block at the
      head of `proposal.md` (2026-08-21) so it does not have to be re-derived:
      §4–§9 core at PR #207 / `a4a6f6e`, §13 at PR #210 / `5daa173` with the
      published annotated tag `contract-v1.34` and its sentinel replacement at
      `7c544c8`, §10 at PR #216 / `ece236a`, §11 at PR #223 / `7312c25`; green
      on the implemented target at the landing tree — `tests/ideation-dashboard`
      3699 passed / 15 skipped, `tests/ideation_dashboard` 63, `tests/doc-health`
      691, `tests/proposal-support` 31, `openspec validate --all --strict` 0
      failed, the contracts validator 0 errors / 4 by-design warnings, and the
      §11 live harness smoke 8 passed against real `omp` v17.3.7 (skipped
      cleanly without it).
      **THE TASK STAYS OPEN, and the reason is the gate itself, not the
      bookkeeping.** `release-realization`'s realization archive gate is written
      over the change's WHOLE declared code surface — "its code merged on the
      implemented target" — and this change's `code_surface:` names
      `session_pr.py`/`gate_routes.py` — share-session reusing the port's
      existing `push` member`, which §12 has not built. Recording evidence for
      the realized nine-tenths does not make the gate's sentence true, and
      ticking this would assert that it is.
      **RE-ADJUDICATED 2026-08-21, AT §12's REALIZATION — AND THIS TASK STILL
      DOES NOT TICK.** The sentence above used to end "it ticks when §12
      realizes", which is now falsified by events and is corrected rather than
      quietly satisfied. §12 HAS realized: the `code_surface:` clause that named
      `session_pr.py`/`gate_routes.py` — "share-session reusing the port's
      existing `push` member" — is built, tested against a real remote, and its
      evidence is recorded against 12.1–12.5. That removes the LARGEST of the
      three blocking families and it does not empty the set.
      What still holds the gate is unchanged in kind: **10.7** owes an additive
      chat-turn-success release and **11.7** owes an additive model-catalog
      release, and §12 added **12.7**, which owes the annotated tag and pin for
      `contract-v1.36`. Each names a release that has not been cut, so "its code
      merged on the implemented target" is not yet true of the whole surface, and
      the gate has no proportion in it. Mechanically the sanctioned path also
      still refuses: `proposal-support.py archive` raises "change has incomplete
      tasks" on any `- [ ]`, and four remain.
      So this ticks when 10.7, 11.7 and 12.7 have landed — whichever is last —
      and NOT before. Nothing was archived by this slice.
      **RE-ADJUDICATED 2026-08-22, AT 10.7's RELEASE — AND THE SENTENCE ABOVE IS
      NOW STALE IN ONE PARTICULAR, corrected rather than left to mislead.** It
      says "**11.7** owes an additive model-catalog release". 11.7 does not owe
      one any more: it was CUT as `contract-v1.38` on 2026-08-21 (PR #244, squash
      `0f50b352`, annotated tag published and its pin resolved at `58e4aecd`),
      and 11.7's own box has been checked since. 12.7 is likewise discharged —
      `contract-v1.36` is tagged and the aggregation pin landed at `04366e3`.
      The correction is made HERE, by this slice, because 11.7's own tick
      deliberately did not edit this task's prose (it said so: "its owner's to
      re-adjudicate"), and this is the owner arriving.
      **READ THIS FIRST — THREE FACTS BELOW ARE STILL PENDING, and one of them
      is the gate's own verb (adversarial review S3).** While this branch is in
      flight NOTHING here is merged, pushed or tagged, so:
      (1) the SQUASH SHA this slice lands as does not exist yet;
      (2) the annotated `contract-v1.39` tag is not published — the versioning
      policy publishes it against the commit that ACTUALLY LANDS, and every gate
      reruns at that squash first, because promotion creates a commit nothing
      has gated;
      (3) `doxbench_contracts.CONTRACT_REF` still carries the
      `unpublished:contract-v1.39` sentinel.
      The post-land step is therefore the same three-part one §11.7 performed at
      `58e4aecd`: rerun the gates at the squash, publish and REMOTELY verify the
      tag, then a follow-up commit resolves the sentinel and fills in the SHA
      line at the foot of this block. Until it runs, read every claim below as
      "built and gated", not as "landed".
      **AND THE BOX IS CHECKED, because the set the sentence names is EMPTY.**
      The three releases it waits on are all CUT: `contract-v1.36` (§12.7,
      tagged and pinned), `contract-v1.38` (§11.7, tagged and pinned), and
      `contract-v1.39` (§10.7, cut on this branch — CHANGELOG entry, manifest
      digest, bundle bump, and the 190-entry inventory built after it, with
      `verify-commit --commit HEAD` passing on the cut).
      **THE VERB, STATED EXACTLY** — an earlier version of this tick said the
      gate's sentence was "now true without proportion or interpretation", which
      was itself an overclaim in the one word that matters. The gate reads "its
      code merged on the implemented target". What is true HERE is that the
      whole declared `code_surface:` is BUILT AND GATED on a branch off the
      implemented target, with nothing owed but the landing; MERGED becomes true
      at the landing squash and not one commit before it. The box is checked on
      the surface being whole, which is the substantive condition and the one
      this task could not meet for four months; the verb is completed by the
      merge, which is not this slice's act.
      THE EVIDENCE BLOCK AT THE HEAD OF `proposal.md` STANDS AS WRITTEN and is
      not restated here; what this tick adds is the tail it could not yet carry:
      §12 share-session realized under Brett's exit (a); §11.7 at
      `contract-v1.38`; §10.7 at `contract-v1.39`. Green on this branch at the
      tick, measured AFTER merging `origin/main` at `0f9e14b4` into the branch
      rather than before it, and RE-MEASURED after BOTH rounds of the
      adversarial review's fixes: `tests/ideation-dashboard` 3930 passed / 15
      skipped, `tests/ideation_dashboard` 63, `tests/doc-health` 691,
      `openspec validate --all --strict` 65 passed / 0 failed, the contracts
      validator 0 errors / 4 by-design warnings (41 valid + 66 negative
      packaged examples confirmed), doc-health pre/post ZERO-new against a
      same-clock `origin/main` baseline, and `validate-contract-release.py
      verify-commit --commit HEAD` passing on the cut. The fifteenth skip is a
      CHECKOUT-LAYOUT artifact and not a regression:
      `test_landed_parses_a_real_archived_change_delta` looks for a SIBLING
      `openxFactory` checkout two directories up, which this isolated clone has
      no sibling for.
      THE THREE PENDING FACTS ARE STATED AT THE HEAD OF THIS BLOCK, where a
      reader meets them before any claim they qualify (S3 moved them there;
      they used to trail every green number in the tick). The line below is what
      the post-land follow-up fills in, exactly as 11.7's did.
      §10.7 — PR #___ / `_______`, annotated tag `contract-v1.39` (to be
      published against the landing commit and verified from the remote).
      **NOTHING IS ARCHIVED BY THIS SLICE.** `proposal-support.py archive` is
      the sanctioned path and it is Brett's act on his explicit word, not a
      consequence of this box being checked. With 10.7 and 13.8 ticked the
      mechanical refusal ("change has incomplete tasks") no longer stands in the
      way — which is a statement about the gate, not an instruction to walk
      through it.
