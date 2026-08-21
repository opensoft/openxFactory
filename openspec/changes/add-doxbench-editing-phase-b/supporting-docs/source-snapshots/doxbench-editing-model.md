# Staged: left selects, chat works, right shows — the doxBench editing interaction model

Status: staged
Kind: capability-proposal
Summary: Settles the general interaction model for editing any document inside
doxBench: the left panel is the SELECTOR of what you are working on (docs,
lens, outline, plus a dynamic numbered tab per document opened in edit mode),
the center chat session always operates in whatever the left panel has
selected, and the right panel shows the result as an Editor/Preview TAB PAIR
(replacing today's split markdown-over-preview layout) carrying Save and
Cancel. A docs-wheel tile's expanded view gains a second verb — edit, beside
the existing read — and a doc with an open unsaved edit is visibly marked on
its wheel tile. RECOMMENDS PR-as-save (the ratified branch-session substrate)
as the Save mechanism, flags that today's buffer state, turn assembly, and
save ordering are all hard-coded to exactly two buffers (outline, document),
and treats this generalization as the open engineering core.
Topics: doxbench, editing-model, workbench, wheel-model, buffer-generalization,
chat-binding, save-cancel, dirty-tile, editor-preview-tabs, ideation-dashboard
Repository context: openxFactory owns `ideation-dashboard`, the sole target
capability — the doxBench workbench UI this topic reshapes end to end (left
selector, center chat, right editor/preview surface, wheel tile marking). The
relevant live modules, verified by reading in this session: buffer state
(`scripts/ideation_dashboard/web/views/doxbench-state.js`), turn assembly
(`scripts/ideation_dashboard/doxbench_turns.py`), the save pipeline
(`scripts/ideation_dashboard/web/views/doxbench-save.js`), the editor canvas
(`scripts/ideation_dashboard/web/views/doxbench-editor.js`), the left-panel
tab set (`scripts/ideation_dashboard/web/views/staging-workbench-model.js`),
the read-only doc-tile wheel (`scripts/ideation_dashboard/web/views/doc-wheel.js`),
the general wheel and its tile/badge rendering
(`scripts/ideation_dashboard/web/views/wheel.js`,
`scripts/ideation_dashboard/web/views/wheel-model.js`), and the external-editor
escape hatch (`scripts/ideation_dashboard/web/views/viewer.js`).
Staging ID: openxFactory:staging:doxbench-editing-model
Captured: 2026-08-15
Source: Brett Heap's direction 2026-08-15 (in-session, verbatim substance
encoded as claims below): the settled interaction model for how a user moves
between documents, how the chat's working context follows that selection, and
how the right-hand result surface should be redesigned from a split view into
tabs.
Target capabilities: MODIFIED `ideation-dashboard` (left-panel dynamic
document tabs generalizing the outline/document buffer pair to N document
buffers; chat-context binding to the active left-panel selection; docs-wheel
tile edit verb + dirty-tile marker; right-panel Editor/Preview tab redesign
with Save/Cancel)

## Last proposal attempt (round-trip provenance)

<!-- Stays "none yet" until this topic first reaches proposal. On DEMOTE,
     replace every field below with the ACTUAL values from the demoted
     change — never re-blank them. -->

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Claims

The following are settled by Brett's 2026-08-15 direction and are NOT reopened
by the open questions below — they are the fixed baseline the questions
iterate against:

1. **The left panel is the selector of what you are working on.** The
   existing tabs — docs, lens, outline — stay, PLUS a dynamic numbered tab
   ('1', '2', …) for every document a user opens in edit mode.
2. **Outline tab focused → the center chat session operates in THAT context**,
   editing the outline document; the right panel shows the chat's working
   output — a new 'unsaved' version of the outline.
3. **Docs tab → the docs wheel**; clicking a doc tile expands it (as today) →
   two options: **read** (goes to the immersive large-screen reader) and
   **edit** (loads the doc into the left panel as a new numbered tab).
4. **A doc with an open unsaved edit must be visibly marked on its wheel
   tile** (e.g., tile color change).
5. **When a doc tab is selected (edit mode): center chat binds to that doc's
   context; the right panel shows the updated doc as the chat and/or user
   edits it.**
6. **Right panel redesign: NOT split** (md top / preview bottom) — **TAB-BASED**:
   an **Editor** tab (the raw md) and a **Preview** tab (large rendered
   preview). The right panel carries **Save** and **Cancel**.
7. **The general model:** left selects the working doc, center chat works on
   it, right shows the result with save/cancel.

The following two claims are settled by Brett's 2026-08-18 live-UI
annotations on the running doxBench app (verbatim annotation text quoted in
the Q1 and Q3 dispositions below) and likewise are NOT reopened by any
remaining open question:

8. **The docs-wheel tile's action row carries three verbs: read, edit,
   save.** Read is unchanged — it still opens the immersive large-window
   reader experience. Edit is the verb that loads the document into the
   chat context; from 2026-08-18 onward, "loaded" throughout this fragment
   means exactly this — a document opened via a wheel tile's edit button —
   and the set of loaded documents is exactly the set Claim 9's rail
   dropdown lists. Save lives on the tile itself, is active only when that
   document's buffer has unsaved changes (dirty-gated — inactive otherwise),
   and performs the identical act as the right panel's existing Save button
   (same save mechanism, a second entry point onto it, not a second save
   pipeline).
9. **The chat rail header's "Working on — …" line (`doxbench-chat.js`)
   becomes a dropdown box** listing every currently loaded document (loaded
   per Claim 8's edit verb). The dropdown's selected entry IS the active
   working document/buffer — i.e., the active buffer in the generalized
   N-buffer model, and the concrete resolution of Q4's "active left-panel
   selection" for the loaded-document case. An entry whose filename does not
   fit on one line hover-expands to show the full filename rather than
   truncating.

Dispositioned-by: Brett Heap (live-UI annotation) · 2026-08-18

The following three claims are settled by a further round of Brett's
2026-08-18 live-UI annotations on the running doxBench app (verbatim
annotation text quoted in full below) and likewise are NOT reopened by any
remaining open question:

10. **The chat is THREAD-BASED PER DOCUMENT.** Each open/loaded document
    (per Claim 8's edit verb) carries its own persisted chat thread; switching
    the working document (per Claim 9's dropdown) switches which thread the
    chat window shows and appends to. This is a chat-header annotation,
    verbatim: "we need to save the thread per document. but the context for
    the chat has all the threads in it. so we need to look at a memory system
    that will allow that to work well for this chat window. discuss options
    with me."
11. **The chat CONTEXT spans the staged set, not just the active thread.** The
    model working any one document's thread sees all of the staged set's
    threads — the working unit for context purposes is the whole staged set,
    while the persisted, switchable unit for conversation purposes is the
    per-document thread. This is a chat-rail annotation, verbatim: "This is
    the window that will be thread based on the document, but the context is
    for this staged set. so the context has all the chat threads."
12. **Threads must be SAVED.** Per-document threads are not disposable
    session state — Claim 10's "save the thread per document" is a persistence
    requirement, not merely an in-memory switch, and Open question 7 below is
    exactly the mechanism question this claim raises.

Dispositioned-by: Brett Heap (live-UI annotation) · 2026-08-18

The following nine claims are settled by Brett's 2026-08-18 in-session ruling
on the chat memory design (synthesizing his live-UI annotations, an
in-session web-research pass on harnesses and graph-context managers, and an
external design review he supplied) and likewise are NOT reopened by any
remaining open question:

13. **Chat memory is a two-plane design**: session working memory (per-document
    thread sidecar files, truth) is separate from the Staged-Set Knowledge
    Service (governed, shared, derived retrieval over the staged set plus
    promoted findings only).
14. **Each thread file carries a structured thread-state header** — active
    goal, accepted facts, open questions, in-thread decisions,
    retrieved-evidence refs, pending actions — above the raw transcript;
    compaction preserves these commitments, not narrative.
15. **The Staged-Set Knowledge Service is exposed behind one MCP boundary**
    (a small tool contract: search, get_source, promote_finding, reindex;
    graph_query later) plus an internal assembly port that a future backend
    swaps behind without changing the boundary.
16. **v1 retrieval is graph-less**: local hybrid (lexical/BM25 + small
    embedded vectors + structured thread-states); a graph manager (Cognee
    preferred, version-pinned; Graphiti+FalkorDB Lite the alternate) slots in
    behind the same port only when a concrete graduation trigger fires
    (recurring dependency traversal, contradiction detection, or
    change-impact-analysis need).
17. **The retrieval backend is an install-time declaration**, per the
    ratified two-case principle: local-embedded for self-hosted installs,
    hosted backends (e.g. Vertex) for tenant installs.
18. **Promotion is gate-only**: raw chat never becomes durable truth
    automatically; a thread finding enters the corpus only through the
    existing lifecycle verbs (idea note / fragment / disposition on the
    topic, with provenance) — no parallel decision store.
19. **Source ranking is status-driven**: ratified/standard canon >
    accepted/staged facts > promoted findings > active thread state >
    harness-local memory (non-authoritative, ranked last), encoded in the
    harness system prompt.
20. **The chat harness is oh-my-pi (`can1357/oh-my-pi`)**, run behind a thin
    stdlib-Python HTTP-to-stdio bridge under the existing WorkbenchModelPort
    seam; one OMP RPC session per document-thread (`switch_session`); the
    sidecar thread files remain the record — OMP's native memory backends
    never hold the threads (split-brain prohibition), and if enabled at all
    hold only non-authoritative lessons.
21. **Share-session is an explicit commit-and-push act**: threads are local
    until a share-session verb commits them and pushes the session branch; a
    colleague resumes the session from the fetched branch.

Dispositioned-by: Brett Heap (in-session ruling) · 2026-08-18
Source: the graph-engine options (Cognee/Graphiti+FalkorDB), the Mem0 v3
finding, and the OMP/oh-my-pi harness integration details derive from an
external design review supplied by Brett 2026-08-18, synthesized and adapted
in-session.

The following five claims are settled by a second round of Brett's 2026-08-18
in-session ruling — a verification research pass conducted after Claims 13-21
landed, checking the external design review's claims and the harness
mechanism details against the ratified xFactory contracts and against
Headroom's actual repository state — and likewise are NOT reopened by any
remaining open question:

22. **The knowledge service and per-turn context assembly realize the
    ratified neutral `memory-gateway` capability.** Per-turn context
    assembled for a document's active thread IS a memory-gateway bounded
    context packet (`Context Packets Bound Runtime Memory`); the Staged-Set
    Knowledge Service's retrieval backends (Claim 16's local hybrid v1, the
    later graph-manager slot) are provider profiles behind canonical,
    product-neutral ports (`Canonical Ports Are Product Neutral`, `Provider
    Profiles Declare Capability`); promoting a thread finding into the
    corpus (Claim 18) realizes `Promotions Are Explicit And Reviewed`; the
    compression/assembly policy (Claims 24-25) runs as a rail before
    provider I/O (`Rails Run Before Provider I/O`); and per-turn/per-session
    token telemetry realizes gateway-owned usage metering (`Usage Metering
    Is Gateway-Owned`). Honest flag, not a fully proven claim:
    memory-gateway's realization depth elsewhere in xFactory is unverified
    in this session — this may be the contract's FIRST live consumer — so
    the Phase B proposal must read the full `memory-gateway` spec itself and
    declare conformance (and any small delta it needs) rather than inherit
    this summary uncritically.
23. **Every compressed artifact this design produces conforms to
    `governed-derived-model`, and any future graph layer stays bounded by
    the semantic kernel.** The thread-state header (Claim 14), any
    distilled summary, and any future graph-manager index (Claim 16) are
    non-authoritative by construction, regenerable, and promotable only by
    creating a new object through review (`governed-derived-model`'s
    Non-authoritative by construction and Human-gated promotion
    requirements) — none of them becomes truth by being compressed. If a
    graph manager (Cognee/Graphiti) is ever graduated in per Claim 16, its
    semantic layer is bounded by `xfactory-semantic-kernel`'s Bounded
    semantic context and Semantic inference cannot authorize requirements:
    inferred relations stay advisory, never an authorization input.
24. **Compression runs as a three-layer stack, each layer a distinct
    fidelity contract.** Layer 1 — SELECTION (governed): the Staged-Set
    Knowledge Service packs only relevant evidence into the bounded context
    packet; lossless-by-reference, since excluded material is one retrieval
    call away. Layer 2 — SEMANTIC COMPACTION (governed): the structured
    thread-state header (Claim 14) preserves commitments — goals, accepted
    facts, decisions, open questions, evidence refs, pending actions — not
    narrative; lossy by design, human-reviewable, promotion-gated, itself a
    governed derived model per Claim 23.
25. **Layer 3 — mechanical reversible compression at the LLM boundary — is
    realized v1 by oh-my-pi's own `/shake` / `artifact://` mechanism.**
    Heavy tool results offload to session artifacts with recoverable
    placeholders — the compress-cache-retrieve pattern, running entirely
    inside our own trust boundary (Claim 20's harness choice) with no proxy
    and no new dependency. The exempt-approved-content policy — protecting
    approved/ratified content from aggressive compression — lives UPSTREAM,
    in the packet assembler, keyed on the content's lifecycle `Status:`
    header (the same source-ranking hierarchy Claim 19 already encodes); it
    is never delegated into a third-party compressor, which would have no
    visibility into lifecycle status.
26. **Headroom (`headroomlabs-ai/headroom`) is a WATCH-LIST candidate, not
    adopted, for any layer of this design.** A 2026-08-18 verification pass
    found it disqualifying today on independent grounds: (a) its
    `SECURITY.md` on `main` claims no credential storage while an open PR
    (`headroom#2684`) demonstrates plaintext credential persistence (OAuth
    tokens; the CCR store writes pre-compression originals to unencrypted
    SQLite; settings persist credential-shaped headers) alongside a
    default-ON telemetry beacon in the OSS build; (b) an independent
    pre-registered benchmark (`Entelligentsia/tokbench`, discussed at
    `headroom#645`) measured ~5-10% per-request and net-zero run-level
    savings on a real agentic workload against the project's 60-95%
    headline; (c) recurring Anthropic prompt-cache-fidelity regressions (one
    causing a 2-7x cost INCREASE, `headroom#2438`) and several open
    Claude-Code-lane bugs, plus a CCR retrieval path that fails on plain
    streaming-proxy clients (it needs the MCP path) and a `ContentRouter`
    with no caller-metadata hook — so Claim 25's exempt-approved-content
    policy could not live inside it even if the other findings cleared.
    Adoption gates (revisit only when ALL hold): the credential-storage
    findings fixed and `SECURITY.md` made truthful; telemetry default-off;
    prompt-cache fidelity stable; a sandboxed trial showing net savings on
    doxBench's own workload. An integration path exists for if/when it
    matures: a community `pi-headroom` bridge, and open `headroom wrap omp`
    requests upstream.

Dispositioned-by: Brett Heap (in-session ruling) · 2026-08-18
Source: verification research pass 2026-08-18 — `memory-gateway`,
`governed-derived-model`, and `xfactory-semantic-kernel` specs read directly
from `openspec/specs/`; Headroom's repository, `SECURITY.md`, PR #2684, the
`tokbench` benchmark discussion, and its issue tracker checked directly;
corrects two factual errors carried in the external design review supplied
2026-08-18 (see the "External-doc reliability" idea note below).

## Why

<!-- xspec:candidate target=ideation-dashboard -->
doxBench's left panel already carries three fixed tabs (`CREATE_TABS =
["docs", "lens", "outline"]`, `staging-workbench-model.js`), and its center
canvas (`mountDoxBenchCanvas`, `doxbench-editor.js`) already renders exactly
two buffers — outline and document — as a fixed internal tablist inside one
mounted canvas. This was proven live by reading the code in this session:
`BUFFER_KINDS` is `Object.freeze(["outline", "document"])`
(`doxbench-state.js`), the state validator throws `"doxBench state must
contain exactly outline and document"` if the buffer set is anything else,
the turn-assembly module's `require_outline_and_document` refuses any request
that does not supply precisely one outline buffer and one document buffer
(`doxbench_turns.py`), and the save pipeline's `SAVE_BUFFER_ORDER =
["outline", "document"]` commits them in that fixed order because the
outline's commit establishes the session ancestry the document buffer's
commit depends on. None of this generalizes today to "however many documents
a user happens to have open." Separately, the right panel's editor canvas
already renders a textarea and a preview `<div>` SIDE BY SIDE inside one pane
(`editarea.append(textarea, preview)`) — the literal split view Brett wants
retired — and the docs-wheel's expanded tile offers exactly ONE verb today
(the read-only viewer; `doc-wheel.js`'s own comment: "the docs pane's one verb
is the read-only viewer"), with no edit option and no wheel-tile marking for
an in-progress edit anywhere in `wheel.js`/`wheel-model.js`.
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=ideation-dashboard -->
The left panel's tab model generalizes from three fixed tabs plus one fixed
internal outline/document split into three fixed tabs PLUS a dynamically
growing set of numbered tabs, one per document a user has opened in edit
mode; selecting any tab (fixed or numbered) sets the chat's active working
context to that tab's document, and the right panel mounts that document's
Editor/Preview tab pair with Save and Cancel bound to it. The docs wheel's
expanded-tile action row gains a second verb (edit) beside the existing read,
which opens the clicked document as a new numbered left-panel tab rather than
the read-only immersive viewer. A doc carrying an open, unsaved edit is
visibly marked on its wheel tile (a distinct color/badge state, following the
same visual idiom `wheel.js` already uses for its `wheelhealth-ind` status
badges). Underneath, the two-buffer-shaped state model, turn-assembly
contract, and save ordering all generalize to N document buffers keyed by
path, with Save continuing to ride the ratified branch-session substrate
(commit-per-gate-action, PR-as-save `open-pr`) as its persistence mechanism
and Cancel continuing to mean discarding a buffer back to its `base_content`
— both already-designed primitives this topic reuses rather than replaces.
<!-- /xspec:candidate -->

## Impact

<!-- xspec:candidate target=ideation-dashboard -->
- Affected specs: `ideation-dashboard` (MODIFIED — left-panel dynamic
  document-tab model; chat-context binding rule; docs-wheel edit verb +
  dirty-tile marker; right-panel Editor/Preview tab redesign with Save/Cancel;
  the underlying N-buffer generalization of what is today an outline/document
  pair).
- Affected code: `scripts/ideation_dashboard/web/views/doxbench-state.js`
  (BUFFER_KINDS and the state validator's exactly-two-keys rule),
  `scripts/ideation_dashboard/doxbench_turns.py`
  (`require_outline_and_document`, `PROPOSAL_TARGETS`),
  `scripts/ideation_dashboard/web/views/doxbench-save.js`
  (`SAVE_BUFFER_ORDER` and its outline-then-document ancestry dependency),
  `scripts/ideation_dashboard/web/views/doxbench-editor.js` (the split
  textarea+preview pane, replaced by Editor/Preview sub-tabs),
  `scripts/ideation_dashboard/web/views/staging-workbench-model.js`
  (`CREATE_TABS`, growing to admit numbered document tabs),
  `scripts/ideation_dashboard/web/views/doc-wheel.js` (the expanded tile's
  single read verb, gaining edit), `scripts/ideation_dashboard/web/views/wheel.js`
  / `wheel-model.js` (a new dirty-tile visual marker), and
  `tests/ideation-dashboard/test_staging_workbench.py` /
  `test_doxbench_state.py` / `test_doxbench_turns.py`, whose pinned
  module-boundary and buffer-shape assertions this topic's eventual change
  must either preserve or deliberately re-pin.
- **Honest gap:** no new capability is proposed here — `ideation-dashboard` is
  verified to already own every surface this topic touches (left panel,
  center chat, right panel, docs wheel, wheel tiles). What is genuinely
  unresolved is the SHAPE of the generalization from two named buffers to N
  path-keyed buffers, which is exactly what the open questions below and an
  eventual design pass must settle.
- No existing behavior changes by staging this topic. The two-buffer model,
  the split editor pane, and the single-verb docs-wheel tile all keep working
  exactly as they do today until a real change lands.
<!-- /xspec:candidate -->

## Idea notes (pre-document, non-documented)

- The existing buffer machinery generalizes further than it first looks: a
  buffer already carries `path`, `dirty`, `base_content`, `current_hash`, and
  an async `hash_generation`/`hash_pending` guard keyed to content, none of
  which assumes there are only two of them — the assumption that breaks is
  purely the FIXED SLOT NAMES (`outline`, `document`) and the validators that
  enumerate exactly those two keys. Generalizing to a `Map`/dictionary of
  buffers keyed by path, with `outline` as a permanently reserved key and
  every other key being a document path, looks like the smallest change that
  preserves every other primitive (`beginBufferEdit`, `settleBufferHash`,
  `adoptSavedBase`, `discardBuffer`) unchanged. — Added-by: Claude Opus 4.8
  (session, Brett's direction) · 2026-08-15
- PR-as-save is already the right substrate for Save: `add-workbench-branch-sessions`
  (ratified 2026-07-26) gives sessions on `draft/<topic>` branches,
  commit-per-gate-action, and an `open-pr` verb as the save-to-persistence
  act — this topic's Save button does not need new plumbing, only a save
  ORDERING rule that works for N buffers instead of the current fixed
  outline-then-document sequence (`SAVE_BUFFER_ORDER`). — Added-by: Claude
  Opus 4.8 (session, Brett's direction) · 2026-08-15
- This topic is the sibling of `staged-topic-outline-template`'s Open
  question 4 (which intent verb authorizes an AI patching one template
  section — recommended answer: `edit-apply`, scoped by the targeted
  section). That topic answers WHICH VERB authorizes an AI content edit; this
  topic answers WHAT THE UI LOOKS LIKE while a human or the chat performs
  that edit — a content-contract question and an interaction-model question
  about the same underlying act, deliberately kept as two separate topics so
  neither's exit gates the other. — Added-by: Claude Opus 4.8 (session,
  Brett's direction) · 2026-08-15
- **HANDOFF (correction to the bullet above):** `add-staged-topic-outline-template`
  Amendment 1 (2026-08-15) renamed Q4's verb from `edit-apply` to
  `edit-document` — `edit-apply` is the gate console's main-resident redline
  verb (needs a change id, applies to change documents) and cannot reach a
  session branch. The upgrade Q4 names — this topic's freeform chat rewrites
  becoming marker-scoped section patches, addressed by a section's heading or
  its `xspec:candidate` fence — shipped in neither the realized Phase A
  (`add-doxbench-editing-phase-a`) nor Phase B; it remains for a successor
  change to build. — Added-by: Claude (bookkeeping,
  `add-staged-topic-outline-template` task 6.3) · 2026-08-21
- The word "edit" is already load-bearing for something else in this corpus:
  `viewer.js`'s "✎ edit" button is a select-to-edit ESCAPE HATCH that opens
  the file in the user's own LOCAL editor and explicitly "does not edit
  anything itself" inside the app. Brett's new doc-wheel "edit" verb means
  something structurally different — load the document into the app's OWN
  left-panel tab and chat-edit it in place. Two verbs, same word, different
  surfaces; worth a deliberate naming choice (or an explicit disambiguating
  label) rather than letting both live as "edit" side by side. — Added-by:
  Claude Opus 4.8 (session, Brett's direction) · 2026-08-15
- Likewise, `doxbench-editor.js` already calls its outline/document split a
  "tab" (`DOXBENCH_BUFFER_TABS`, a real ARIA tablist). Brett's right-panel
  redesign introduces a SECOND, different meaning of "tab" (Editor vs.
  Preview) nested one level below the buffer selection that the left panel
  now owns instead. The naming needs to distinguish "which document" tabs
  (left panel, numbered) from "which view of this document" tabs (right
  panel, Editor/Preview) so the two concepts do not collide in code or in
  conversation. — Added-by: Claude Opus 4.8 (session, Brett's direction) ·
  2026-08-15
- `wheel.js` already has a precedent visual idiom for a status marker on a
  tile — the `wheelhealth-ind wheelhealth-<status>` badge rendered on health
  indicators. The dirty-tile marker this topic's Claim 4 asks for is a
  genuinely new signal (nothing today marks "has an open unsaved edit"), but
  it does not need a new visual language — reusing the badge idiom (a new
  status value, e.g. `wheelhealth-editing` or a dedicated
  `wheeltile-dirty` class) keeps one consistent marker vocabulary on the
  wheel rather than inventing a second one beside it. — Added-by: Claude
  Opus 4.8 (session, Brett's direction) · 2026-08-15
- Annotation round 2 (same day, 2026-08-18) also queued a chat MODEL
  SELECTOR next to the send button — not one of this fragment's two open
  questions, but relevant to Phase B's scope: if a per-turn model choice
  needs a wire field (e.g. recording which model handled a turn), it rides
  the same Phase B chat-turn contract release as the turn-record obligation
  Q4 already settled (every turn record names the exact buffer it acted
  on) — one release carrying both additive fields, not two separate
  releases. — Added-by: Claude Opus 4.8 (session) · 2026-08-18.
  Dispositioned-by: Brett Heap (live-UI annotation) · 2026-08-18
- **VERIFY LIST before Phase B realization** (extended 2026-08-18, second
  session pass) — items the ruled two-plane memory design (Claims 13-21,
  Q7's Ruling block) and its addendum (Claims 22-26, the Ruling addendum)
  depend on that our own research has not independently confirmed: (a)
  OMP's memory-backend claims (local / Hindsight / Mnemopi), cited from its
  README by the external design review — unverified by our own research;
  (b) the depth of OMP/pi's MCP client (tool-calling) support; (c) whether
  OMP re-reads `SYSTEM.md` per turn or caches it at session start; (d)
  Cognee's current default embedded graph backend, in flux after the Kuzu
  archival (Apple acqui-hire, Oct 2025) — watch `topoteretes/cognee#2098`;
  (e) where OMP session artifacts (the `artifact://` store, Claim 25) live
  on disk, and whether they land inside the session worktree — so they ride
  the branch, per Claim 21's share-session act — or somewhere external to
  it; (f) `/shake`'s exact trigger surface — a manual chat command, an
  automatic threshold-triggered behavior, or both — and whether OMP's RPC
  mode (Claim 20) exposes it programmatically rather than only as an
  interactive command; (g) `memory-gateway`'s current realization depth
  anywhere in xFactory — is any conformant consumer actually live today, or
  is this topic's Phase B the first (Claim 22's honest flag). — Added-by:
  Claude Opus 4.8 (session) · 2026-08-18. Dispositioned-by: Brett Heap
  (in-session ruling) · 2026-08-18. Source: external design review supplied
  by Brett 2026-08-18, synthesized and adapted in-session (item (a) is a
  direct citation from that review); items (e)-(g) added 2026-08-18 in a
  second session pass following the memory-gateway/Headroom verification
  research (Claims 22-26).
- **External-doc reliability note** (standing practice, proven twice). The
  external design reviews Brett has supplied for this topic have been
  directionally valuable but factually loose: "SpecLock" appears in no real
  project this session's verification research could find (invented
  vocabulary in the review), and "Mnemopi"/`artifact://`/`/shake` are
  `oh-my-pi` features misattributed to Headroom in the review Brett
  supplied 2026-08-18. Standing practice going forward: every external-doc
  claim gets verified against the actual upstream source before it enters
  contract text — this is now twice proven necessary on this single topic
  (once for the harness/memory review behind Claims 13-21, again for the
  Headroom review behind Claim 26). — Added-by: Claude Opus 4.8 (session) ·
  2026-08-18. Dispositioned-by: Brett Heap (in-session ruling) · 2026-08-18.

## Conflicts

- `doxbench-state.js`'s `BUFFER_KINDS` is `Object.freeze(["outline",
  "document"])`, and `validatedDoxBenchState` throws `"doxBench state must
  contain exactly outline and document"` whenever the buffer key set is
  anything else (verified by reading the module directly, twice — once in
  `validatedDoxBenchState` and once in `restoreDoxBenchState`'s restore path).
  Brett's numbered multi-document tabs deliberately break this invariant: the
  state shape must generalize from two named slots to N path-keyed document
  buffers. This is not a convention to relax — it is an enforced runtime
  contract this topic's eventual change must directly modify. — Added-by:
  Claude Opus 4.8 (session, Brett's direction) · 2026-08-15
- `doxbench_turns.py`'s `require_outline_and_document` refuses any turn
  request that does not supply EXACTLY one outline buffer and one document
  buffer, and `PROPOSAL_TARGETS` is the fixed two-tuple `("outline",
  "document")` naming what an AI proposal may target. The turn/chat
  machinery is two-buffer-shaped at the same depth as the state model, not
  merely at the UI layer — the chat-context-binding claim (Claim 5) needs
  this contract to admit an arbitrary active document path, not one of
  exactly two enum values. — Added-by: Claude Opus 4.8 (session, Brett's
  direction) · 2026-08-15
- `doxbench-save.js`'s `SAVE_BUFFER_ORDER = ["outline", "document"]` is a
  fixed, ORDERED two-buffer commit sequence: the module's own comments state
  the outline's commit establishes the session ancestry the document
  buffer's commit depends on, and a buffer that neither committed nor was
  unchanged stops every later buffer in the order. Generalizing Save to N
  document buffers needs an explicit ordering/dependency rule (recommended
  below: outline first, established as session ancestry, then every document
  buffer in any order since they do not depend on each other) — not simply
  "outline then document" widened to a longer fixed list. — Added-by: Claude
  Opus 4.8 (session, Brett's direction) · 2026-08-15
- The right panel today (`mountDoxBenchCanvas`, `doxbench-editor.js`) already
  renders a textarea and a preview `<div>` side by side inside ONE pane per
  buffer tab (`editarea.append(textarea, preview)`) — this is the literal
  split-view layout Claim 6 asks to retire in favor of Editor/Preview
  sub-tabs. Today's per-buffer-tab Save/Discard buttons (verified present:
  each buffer tab already carries its own Save button and Discard button)
  are close to, but not identical to, Claim 6's single right-panel-level
  Save/Cancel — reconciling "one Save/Cancel pair per active document" with
  the code's current "one Save/Discard pair per buffer tab" is design work
  this topic does not itself resolve. — Added-by: Claude Opus 4.8 (session,
  Brett's direction) · 2026-08-15
- `tests/ideation-dashboard/test_staging_workbench.py` pins real module
  boundaries as executable assertions — e.g. that the pure model module
  stays import-free (the node-harness standalone rule) and that the renderer
  boundary allows no transport calls in the model. Any refactor that
  generalizes buffer state, turn assembly, or the left-panel tab set must
  either preserve these pinned invariants or explicitly re-pin them with a
  reasoned replacement; this topic does not itself relax any of them. —
  Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15
- `wheel.js` / `wheel-model.js` carry no "dirty" or "has an open edit" tile
  concept today — only a health-status badge (`wheelhealth-ind`). Claim 4's
  dirty-tile marker is a wholly new UI signal requiring new wheel-tile state
  plumbing (session-local, per Open question 3 below), not a rename or
  extension of an existing field. — Added-by: Claude Opus 4.8 (session,
  Brett's direction) · 2026-08-15

## Open questions

### Q1. Numbered tabs vs. named tabs for open edits, and the tab-overflow policy?

Context: Claim 1 specifies numbered tabs ('1', '2', …) for documents opened
in edit mode, beside the fixed docs/lens/outline tabs. A workbench session
could plausibly accumulate many open edits before saving or canceling any of
them, and the left panel has finite width.
Recommended answer: numbered chips (matching Claim 1's literal spec) that
carry the document's filename as a tooltip/`aria-label` for identification,
with an LRU overflow policy once the visible chip row is full — the least
recently focused numbered tab folds into a dropdown/overflow menu rather than
silently discarding it or blocking new opens.
Explanation: pure numbering keeps Claim 1's literal shape and avoids
truncated-filename chips competing for narrow tab width, while the tooltip
keeps the tab identifiable without a rename. LRU overflow (rather than a hard
cap that refuses a new open) matches how the rest of doxBench treats
degradation — never blocking a governed action outright when a softer
fallback exists — and keeps every already-open edit reachable, just not
all simultaneously visible.
Ruling (overrides Recommended answer above): Brett annotated the live UI
directly on the chat rail header ("Working on — ..."), verbatim: "make this
a dropdown box that lists the files that have been loaded by clicking the
edit button on the wheel. the selected one is the file we are working on.
if not fit in one line, then use hover to expand to see full filename."
This replaces numbered chips + LRU overflow with a DROPDOWN BOX in the chat
rail header (the existing "Working on — {boundName}" element in
`doxbench-chat.js`) listing every document currently loaded into the chat
context (loaded = opened via the docs-wheel tile's edit verb, per Claim 3
and new Claim 8); the dropdown's selected entry IS the active working
document/buffer; an entry whose filename does not fit on one line
hover-expands to show the full filename rather than truncating or
ellipsizing. There is no chip row, no numbered ('1', '2', …) tabs, and no
LRU-fold-to-overflow-menu — the dropdown itself is the overflow mechanism
(a scrollable list, not a fixed-width row), so the "many open edits" concern
this question raised is resolved by construction rather than by a folding
policy.
Re-affirmed (same day, second annotation): Brett annotated the chat header a
second time on 2026-08-18, verbatim: "this is only the Name of the document
selected that we are chatting on. This should be a dropdown to select the
'open' docs that are being edited this session." This re-states the ruling
above rather than changing it — the dropdown-of-loaded-docs shape stands as
already ruled.
Disposition status: overridden-by-ruling (Brett, 2026-08-18, live-UI annotation)
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15
Dispositioned-by: Brett Heap (live-UI annotation) · 2026-08-18

### Q2. What are Save and Cancel's exact semantics?

Context: Claim 6 gives the right panel Save and Cancel controls but does not
itself specify what each commits to. The workbench already has a designed
persistence substrate (`add-workbench-branch-sessions`: sessions on
`draft/<topic>` branches, commit-per-gate-action, PR-as-save `open-pr`) and a
designed reversal primitive (`discardBuffer`, which resets a buffer's
`content`/`current_hash` back to `base_content`/`base_hash`).
Recommended answer: Save = commit-per-gate-action on the session's draft
branch (the existing branch-session substrate), with PR-as-save (`open-pr`)
remaining the eventual promotion act exactly as already ratified elsewhere;
Cancel = discard the active buffer back to its `base_content`, reusing
`discardBuffer` unchanged.
Explanation: both halves of this recommendation are already-designed,
already-ratified primitives (the branch-session model for Save, `discardBuffer`
for Cancel) — this topic's Save/Cancel controls are a UI binding onto
existing machinery, not a new persistence or reversal mechanism. The only
open engineering question underneath is the N-buffer save-ordering rule
(see the Conflicts section), not the semantics of what Save or Cancel MEAN.
Disposition status: accepted-as-recommended (Brett, 2026-08-15) — feeds the Phase A proposal
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15
Dispositioned-by: Brett Heap (ruling relayed in-session) · 2026-08-15

### Q3. How does dirty-tile signaling on the wheel get stored and displayed?

Context: Claim 4 requires a doc with an open unsaved edit to be visibly
marked on its wheel tile. `wheel.js`/`wheel-model.js` have no such concept
today; the closest precedent is the `wheelhealth-ind` status-badge idiom.
The workbench's existing buffer `dirty` flag already tracks exactly this
fact per buffer, session-locally, and is explicitly never persisted into the
generated snapshot (snapshots are regenerated, read-only projections).
Recommended answer: a distinct visual state (a badge or tile-color class,
following the existing `wheelhealth-ind` idiom) driven directly by the live
buffer `dirty` flags for whatever documents are currently open in this
session — never written into the snapshot or any persisted register field.
Explanation: the dirty flag is inherently session-local working state (it
describes an in-browser, unsaved edit, not a fact about the corpus), and the
snapshot's whole design principle is that it is a regenerated, derived
projection — writing a "has an open edit" fact into it would make the
snapshot generator responsible for knowing about live browser sessions it
has no way to observe. Driving the tile marker off the already-live
`dirty` state keeps the marker honest and keeps the snapshot's derivation
model unchanged.
Ruling (overrides Recommended answer above): Brett annotated a docs-wheel
tile directly on the live UI, verbatim: "add a load button. read will still
pull up an imersive reader experience of the doc in a large window. the new
<Edit> button will then load this into the chat context. Once loaded and
editable by chat, color this tile so we know is must be saved. also add a
save button here. So we have read, edit, save and save only active if there
are changes. the save acts same as the save button that is in the preview
panel." The ruled shape (see new Claim 8): the wheel tile's action row
carries three verbs — read (unchanged, the immersive large-window reader),
edit (loads the document into the chat context), and save (lives on the
tile itself). The tile is COLORED whenever its document is
loaded-and-editable-by-chat — the visual-state idiom the recommended answer
proposed (a badge/tile-color class in the `wheelhealth-ind` idiom) stands,
but the trigger condition is now explicitly "loaded into chat context",
still driven off the live session-local buffer state, never persisted into
the snapshot. New beyond the recommended answer: the tile also gains its
own Save control — active (clickable) only when the buffer has unsaved
changes, inactive otherwise — that performs the identical save act as the
right panel's existing Save button (Q2's already-ratified Save semantics;
one save mechanism, two entry points). The tile is therefore both a status
signal and an action surface, not a passive badge only.
Disposition status: overridden-by-ruling (Brett, 2026-08-18, live-UI annotation)
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15
Dispositioned-by: Brett Heap (live-UI annotation) · 2026-08-18

### Q4. What is the chat-context binding rule, precisely?

Context: Claims 2 and 5 both say the chat operates in the context of
whichever tab is focused (outline or a document tab), but neither states the
mechanical rule for HOW that binding updates as a user switches tabs, nor
what a turn record should say about which buffer it acted on. Today's turn
assembly (`doxbench_turns.py`) already carries an `active_document_path`
concept it revalidates against the supplied document buffer's path before
running a turn.
Recommended answer: the chat always binds to the ACTIVE left-panel selection
(the currently active buffer, in the generalized N-buffer sense); switching
tabs switches the chat's working context immediately (no separate "confirm
context switch" step); and every turn record names the exact buffer (path)
it acted on, generalizing today's `active_document_path` revalidation rather
than replacing it.
Explanation: this is the smallest rule that satisfies Claims 2 and 5 exactly
as stated and reuses the turn module's EXISTING active-path revalidation
discipline (refuse a turn whose declared active path does not match the
supplied buffer) rather than inventing a second context-tracking mechanism
beside it — the generalization is in WHAT can be named as active (any open
buffer, not only "outline" or "the one document"), not in the binding rule
itself.
Disposition status: accepted-as-recommended (Brett, 2026-08-15) — feeds the Phase A proposal
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15
Dispositioned-by: Brett Heap (ruling relayed in-session) · 2026-08-15

### Q5. What is the Editor/Preview tab pair's default and sync behavior?

Context: Claim 6 specifies Editor (raw md) and Preview (large rendered
preview) as the right panel's two tabs, replacing today's side-by-side
textarea+preview pane, but does not state which tab is selected by default
or whether Preview re-renders live as the chat/user edits while Editor is
the visible tab.
Recommended answer: Preview as the default tab (favors read-leaning users
opening a document, since most opens are to review or resume rather than to
immediately type), with a live re-render firing on every switch INTO Preview
(reusing the existing debounced-preview machinery `doxbench-editor.js`
already runs for the current side-by-side layout) so switching tabs never
shows stale rendered content.
Explanation: defaulting to Preview matches the "large-screen reading"
framing Claim 3 already uses for the read verb, and reusing the debounced
preview pipeline that already exists (rather than building a second
rendering path) keeps this a layout change, not a new rendering feature.
Disposition status: accepted-as-recommended (Brett, 2026-08-15) — feeds the Phase A proposal
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15
Dispositioned-by: Brett Heap (ruling relayed in-session) · 2026-08-15

### Q6. How is concurrent-edit safety preserved once state generalizes to N buffers?

Context: today's buffer model already guards against acting on stale content
via a per-buffer content-hash generation (`hash_generation`/`hash_pending`,
`current_hash`), and `applyProposalToBuffer` already refuses an AI proposal
whose declared base hash does not exactly match the buffer's settled current
hash. Generalizing to N document buffers multiplies the number of
independently-editable surfaces a chat turn or a Save could race against.
Recommended answer: keep the existing content-hash generation guard exactly
as designed, applied per buffer regardless of how many buffers exist — a
turn or a Save attempted against a stale hash (any buffer whose settled
identity has moved since the acting request last observed it) refuses,
exactly as `applyProposalToBuffer` and the turn-assembly revalidation already
do for the two-buffer case today.
Explanation: the per-buffer hash-generation guard was already designed to be
buffer-scoped, not state-scoped — nothing about it assumes there are only
two buffers, so widening the buffer set does not require a new safety
mechanism, only applying the existing one N times instead of twice. This is
the one place the generalization is close to free.
Disposition status: accepted-as-recommended (Brett, 2026-08-15) — feeds the Phase A proposal
Added-by: Claude Opus 4.8 (session, Brett's direction) · 2026-08-15
Dispositioned-by: Brett Heap (ruling relayed in-session) · 2026-08-15

### Q7. Which memory system persists the per-document threads and assembles the set-wide context?

Context: Brett explicitly asked to discuss options before ruling (Claim 10's
annotation, verbatim: "discuss options with me") rather than annotating a
ruling directly onto the UI as he did for Q1 and Q3 — this question is
deliberately left open for that discussion, not merely undecided. The turn
store is in-memory today; the chat-turn wire is closed for Phase B's release
(the Phase A/B split above already sequences a wire-carrying release); branch
sessions provide a commit-per-action durable substrate already ratified for
Save; and the serve's write surface is the interactivity boundary's declared
allowlist, which any persistence mechanism for threads must fit inside.
Recommended answer: the orchestrator's recommendation, PENDING Brett's ruling
from the options discussion he asked for — threads persist as per-document
sidecar files in the session branch, committed alongside the document's Save
(riding the existing commit-per-action substrate rather than adding a new
persistence path); each thread file maintains a distilled summary block
alongside its full turn history; context assembly for any one document's
active thread = that thread in full + every other loaded document's thread
summary + the loaded documents themselves, assembled server-side from the
session tree so no wire change is needed for threads themselves (only the
already-planned Phase B wire release carries the turn-record fields it
already carries). Threads stay session-branch working memory and are excluded
from PR-as-save promotion by default (they are conversation scaffolding, not
document content).
Explanation: repo-native durability and provenance come for free from the
same branch-session substrate Q2 already ratified for Save, rather than
inventing a second persistence mechanism; the distilled-summary-plus-full-
thread shape matches the outline-template sibling topic's existing
distill-everything pattern (`staged-topic-outline-template`); keeping
assembly server-side and out of the wire preserves the serve's write
discipline (the interactivity boundary's declared allowlist); and a summary-
per-other-thread (rather than every thread in full) bounds context growth as
the staged set's document count grows.
Ruling: THE RULED TWO-PLANE MEMORY DESIGN (Brett, 2026-08-18, synthesizing his
live-UI annotations, an in-session web-research pass on harnesses and
graph-context managers, and an external design review he supplied).

- **Plane 1 — session working memory (truth).** Per-document chat threads
  persist as sidecar files on the session's draft branch. Each thread file
  carries a structured THREAD-STATE HEADER — active goal, accepted facts,
  open questions, decisions made in-thread, retrieved-evidence refs, pending
  actions — above the raw transcript; compaction preserves these commitments,
  not narrative. Threads commit on the document's Save (local until pushed).
  Sharing is an explicit act: a share-session verb commits threads and pushes
  the session branch; a colleague resumes the session from the fetched
  branch. Threads are working memory, excluded from PR-as-save promotion by
  default.
- **Plane 2 — the Staged-Set Knowledge Service (governed, shared, derived).**
  Retrieval over the staged set's documents plus PROMOTED findings only.
  Exposed behind one MCP boundary (a small tool contract: search, get_source,
  promote_finding, reindex; graph_query later) and an internal assembly port.
  v1 retrieval is local hybrid (lexical/BM25 + small embedded vectors + the
  structured thread-states); no graph engine in v1. A graph manager (Cognee
  preferred, version-pinned; Graphiti+FalkorDB Lite the alternate) slots in
  behind the same port when a concrete graduation trigger fires: recurring
  need for dependency traversal, contradiction detection, or change-impact
  analysis. The Mem0 v3 finding — graph memory lost on recall, 3x slower, 2x
  token cost, so they removed it — is the recorded caution motivating a
  graph-less v1. The retrieval backend is an install-time declaration per the
  ratified two-case principle: local-embedded for self-hosted installs,
  hosted backends (e.g. Vertex) for tenant installs — the same intake family
  as the credential/notebook hosting declarations.
- **Promotion gate.** Raw chat never becomes durable truth automatically. A
  thread finding enters the corpus only through the existing lifecycle verbs
  (promoted into an idea note / fragment / disposition on the topic, with
  provenance) — no parallel decision store.
- **Source-ranking hierarchy** (encoded in the harness system prompt, driven
  by lifecycle Status headers): ratified/standard canon > accepted/staged
  facts > promoted findings > active thread state > harness-local memory
  (non-authoritative, ranked last).
- **Harness.** The chat runs through oh-my-pi (`can1357/oh-my-pi`, MIT)
  behind a thin stdlib-Python HTTP-to-stdio bridge under the existing
  WorkbenchModelPort seam (`omp --mode rpc`; no HTTP mode exists upstream).
  One OMP RPC session per document-thread via `switch_session`; doxBench
  mirrors turns to the sidecar files, which remain the record — OMP's native
  memory backends do NOT hold the threads (split-brain prohibition); if
  enabled at all, they hold only non-authoritative lessons. Per-turn model
  choice = `set_model` before prompt. The model menu is `auto / Opus / Kimi
  K3 / ...` where `auto` is our own routing rule (a role-mapping/extension —
  OMP has roles and fallback chains, but no native `auto`). Kimi K3 in the
  menu means API access (Moonshot/Together — the 594GB open weights need
  ≥8xH100; not local).

**Ruling addendum (2026-08-18, second session pass).** A follow-up
verification pass the same day fills in the two structural pieces the
ruling above left implicit: which ratified xFactory contract this design
realizes, and exactly how "compaction preserves commitments, not narrative"
(Claim 14) turns into working token discipline.

- **Memory-gateway conformance.** The knowledge service and per-turn context
  assembly above SHALL be written as a realization of the ratified neutral
  `memory-gateway` capability, not a bespoke mechanism beside it: per-turn
  context is a memory-gateway bounded context packet; the retrieval backends
  (local hybrid v1, the later graph-manager slot) are provider profiles
  behind memory-gateway's canonical, product-neutral ports; promoting a
  thread finding (the Promotion gate above) realizes `Promotions Are
  Explicit And Reviewed`; the compression stack below runs as a rail before
  provider I/O; and token telemetry realizes gateway-owned usage metering.
  Every compressed artifact (the thread-state header, any summary, any
  future graph) additionally conforms to `governed-derived-model` —
  non-authoritative by construction, regenerable, promotable only by
  creating a new object through review — and any future graph layer stays
  inside `xfactory-semantic-kernel`'s bounded-context and
  inference-cannot-authorize requirements. Honest flag: memory-gateway's
  realization depth elsewhere in xFactory is unverified — this may be the
  contract's first live consumer — so the Phase B proposal must read the
  full spec itself and declare conformance (and any small delta) rather
  than take this summary on faith. (See new Claims 22-23.)
- **The three-layer compression stack.** Layer 1, SELECTION (governed): the
  Staged-Set Knowledge Service packs only relevant evidence into the
  context packet — lossless-by-reference, excluded material stays one
  retrieval away. Layer 2, SEMANTIC COMPACTION (governed): the structured
  thread-state header — lossy by design, human-reviewable, promotion-gated,
  itself a governed derived model. Layer 3, MECHANICAL REVERSIBLE
  COMPRESSION at the LLM boundary: v1 is oh-my-pi's own native `/shake` /
  `artifact://` mechanism — heavy tool results offload to session artifacts
  with recoverable placeholders, inside our own trust boundary, no proxy,
  no new dependency. The exempt-approved-content policy (protecting
  approved/ratified content from aggressive compression) lives upstream in
  the packet assembler, keyed on lifecycle status — never inside a
  third-party compressor. (See new Claims 24-25.)
- **Headroom is watch-listed, not adopted.** `headroomlabs-ai/headroom`
  (Apache-2.0) was evaluated as a candidate for Layer 3 and rejected for
  now: verification found a SECURITY.md credential-storage claim
  contradicted by an open PR proving plaintext credential persistence plus
  default-on telemetry, an independent benchmark showing ~5-10%
  per-request / net-zero run-level savings against its 60-95% headline,
  recurring Anthropic prompt-cache-fidelity regressions, and no
  caller-metadata hook for the exempt-approved-content policy even setting
  the other findings aside. Adoption gates and the integration path are
  recorded in new Claim 26. This also surfaced a naming correction:
  "SpecLock" matches no real project, and "Mnemopi"/`artifact://`/`/shake`
  are oh-my-pi features the external review misattributed to Headroom (see
  the Idea notes external-doc-reliability entry) — the design as ruled here
  uses the corrected attributions throughout.

Addendum source: verification research pass 2026-08-18 — the
`memory-gateway`, `governed-derived-model`, and `xfactory-semantic-kernel`
specs read directly from `openspec/specs/`; Headroom's repository,
`SECURITY.md`, PR #2684, the `tokbench` benchmark discussion, and its issue
tracker checked directly.

Source: the graph-engine options (Cognee/Graphiti+FalkorDB), the Mem0 v3
finding, and the OMP/oh-my-pi harness integration details derive from an
external design review supplied by Brett 2026-08-18, synthesized and adapted
in-session.
Disposition status: ruled (Brett, 2026-08-18) — the two-plane memory design
below, extended 2026-08-18 (second session pass) with memory-gateway
conformance and the three-layer compression stack
Added-by: Claude Opus 4.8 (session) · 2026-08-18
Dispositioned-by: Brett Heap (in-session ruling) · 2026-08-18

## Exit

All seven open questions above now carry a disposition other than `open` —
Q7 was ruled 2026-08-18 as the two-plane memory design recorded above
(session-working-memory thread sidecars as truth, plus a Staged-Set
Knowledge Service behind one MCP boundary). The
likely landing is a single OpenSpec change carrying one `ideation-dashboard`
delta: the N-buffer state/turn/save generalization, the left-panel numbered-
tab model, the chat-context binding rule, the docs-wheel edit verb plus
dirty-tile marker, the right-panel Editor/Preview redesign with Save/Cancel,
and the thread-per-document / set-wide-context chat memory model — sequenced
so the buffer/turn/save generalization lands first, since every UI-facing
claim above depends on it.
