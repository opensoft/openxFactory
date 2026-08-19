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
- [ ] 5.4 `PROMPT_SECTION_ORDER` grows deterministically: one section per loaded
      document in the declared order, plus the packet's sections (§10). The
      order stays a single declared constant.
      **HALF LANDED, half gated.** The document half is realized: the single
      `document_buffer` slot became the `document_buffers` GROUP, expanded by
      `prompt_section_keys` to one `document_buffer:<buffer key>` section per
      loaded document in the declared order, from ONE constant, pinned at both
      levels. The PACKET's sections wait on §10, which is gated on §3, so this
      task stays open until they land beside them.
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
- [ ] 7.2 Selecting an entry sets the selected buffer through the existing state
      primitive and switches the transcript to that document's thread. No second
      state authority.
      **HALF LANDED, half gated.** The selection half is realized: the selector
      sets the selected buffer through the canvas's own `setActiveBuffer` seam,
      immediately and with no confirmation step, and reads `state.active_buffer`
      back rather than tracking it a second time — no second state authority
      exists, and the review's F1 reproduction is now a composition test:
      loading a document, selecting it, and the released wire's own invariant are
      all driven through the real mount. The THREAD switch waits on §9's sidecar
      store; the change handler
      carries a `TODO(add-doxbench-editing-phase-b tasks.md §9)` naming it, and
      is deliberately left as the selection move alone rather than half-wired to
      a store that does not exist yet.
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
- [ ] 9.2 Threads commit WITH the document's Save through the existing
      one-commit-per-gate-action path, so a thread and its document cannot land
      in separate commits.
      **SEAM LANDED, route unwired.** `thread_commit_paths(document_path)` yields
      the paths a Save adds to `commit_gate_action`'s DECLARED document set (that
      function is untouched), and `write_thread(gate, thread)` is the only write
      route, going through the injected `HumanGate` inside the session worktree.
      What is not wired is the CALL from the save route, which belongs with §11's
      turn mirroring and the thread route §9.5 also waits on.
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
- [ ] 9.5 Thread routes live inside the serve's declared write allowlist (the
      interactivity boundary), are loopback-only, fail closed on an unresolved
      actor, and are absent without the gate capability and on the hosted plane.
      **ALLOWLIST AND POSTURES LANDED, route unwired.**
      `gate_routes.first_edit_gate_factory` — doxBench's governed Save — now
      DECLARES the thread prefix, without which the boundary refuses the sidecar
      as `outside-allowlist`; no other gate widens, and a test asserts the prefix
      appears exactly once. `require_thread_capability` refuses on the hosted
      plane and where the gate capability is absent, with a fixed reason and a
      named cause, and refuses an undeclared plane rather than guessing. What
      remains is the ROUTE itself — loopback-only and fail-closed on an
      unresolved actor at the HTTP surface — which belongs with §11's turn
      mirroring, the first caller a thread route would have.

## 10. The knowledge service v1

- [ ] 10.1 The internal ASSEMBLY PORT: the product-neutral surface a retrieval
      backend implements, with the v1 local-hybrid profile behind it (lexical +
      small embedded vectors + the structured thread-states). No graph engine,
      anywhere.
- [ ] 10.2 The MCP boundary: `search`, `get_source`, `promote_finding`,
      `reindex`, with `graph_query` RESERVED and unimplemented (a test asserts
      it is unimplemented).
- [ ] 10.3 The packet assembler: selection rail, then the lifecycle-status
      exemption rail keyed on each item's `Status:` header, then the bounds
      check, then deterministic assembly (design §3.1). Both rails run before
      any retrieval or provider I/O, and a refusal discloses no packet content.
- [ ] 10.4 The packet declares purpose, sources with refs, bound scope and
      expiry, and is rejected for another purpose, another scope, or after
      expiry.
- [ ] 10.5 Evidence is confined to the tile's staged set plus promoted findings;
      a retrieval that would return anything else is excluded, and a retrieved
      document never joins the loaded set.
- [ ] 10.6 The retrieval backend is read from an install-time declaration; no
      runtime, per-turn, prompt-driven or heuristic selection path exists.
- [ ] 10.7 Degraded posture: no knowledge service → the declared reduced packet
      with the posture stated, no unbounded substitute, no rail bypass, editors
      unaffected.
- [ ] 10.8 Per-turn and per-session token telemetry is emitted content-free.
      Where the metering requirement's client/domain/bill-to fields have no
      value on a self-hosted console, the absence is declared rather than
      filled with a placeholder.

## 11. The harness bridge and the model menu

- [ ] 11.1 The bridge: a stdlib-only local child process translating the
      server's call into the harness's stdio RPC, the only component that knows
      the harness protocol, loopback-local, holding no credential.
- [ ] 11.2 It is an ADAPTER for the UNCHANGED three-member `WorkbenchModelPort`.
      A test asserts the port still has exactly three members and that
      `FORBIDDEN_PORT_MEMBERS` still bans the rest.
- [ ] 11.3 Lifecycle: started on demand at the first turn that needs it,
      supervised, restarted on failure with a bounded retry, stderr to the
      serve's log and never to the wire; a dead or unstartable bridge surfaces
      as the honest model-unavailable posture with the route's existing refusal
      shape and gate order unchanged.
- [ ] 11.4 One harness session per document thread; switching the selected
      document switches the harness session; one session never serves two
      threads.
- [ ] 11.5 The sidecar is the record: every turn is mirrored to it, and the
      harness's native memory holds no thread. Any enabled harness-local memory
      is non-authoritative and ranked last.
- [ ] 11.6 Per-turn model choice is applied inside the adapter before dispatch,
      using the `model_id` the envelope already carries. No fourth port member.
- [ ] 11.7 The catalog declares the menu, `auto` declares itself a ROUTING RULE
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

## 12. Share-session

- [ ] 12.1 The verb: commit threads → `push` (the pull-request port's EXISTING
      member) → return and record the pushed ref. No `open_or_update`, no pull
      request, no review request, no approval or merge authority.
- [ ] 12.2 Nothing pushes implicitly: no Save, turn, compaction or scheduled
      task may push. A test asserts the negative.
- [ ] 12.3 Invoked with nothing new, it reports that honestly rather than
      pushing again.
- [ ] 12.4 Loopback-only, fail-closed on an unresolved actor, console-presence
      demonstrated, recorded as a human gate action; local-plane only, and a
      copyable descriptor where the gate capability is absent. The push identity
      follows the plane rule the save verb already carries.
- [ ] 12.5 A colleague's resume path is exercised end to end: fetch the shared
      branch, open the tile, join the session, see the threads.
- [ ] 12.6 (Scope call, recorded in the proposal) this slice MAY trail as a
      later realization slice; its CONTRACT does not.

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
- [ ] 13.6 The staged topic is EXITED: every question dispositioned, the topic
      folder's transition recorded, and the staging INDEX detail section updated
      to say Phase B carried the remainder.
- [ ] 13.7 **Archive order:** `add-doxbench-editing-phase-a` must archive FIRST,
      or the three Phase-A-relative MODIFIED requirements have nothing to amend
      and the promoted spec would keep Phase A's F2 deferral clause with nothing
      discharging it (design §9). Verify Phase A's archive before archiving
      this change.
- [ ] 13.8 Realization evidence for the archive gate: merged on the implemented
      target through the engineering gates, plus a green run of the runnable
      surface (`release-realization`'s realization archive gate).
