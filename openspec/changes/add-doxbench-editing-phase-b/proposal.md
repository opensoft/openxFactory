---
code_surface: openxFactory (`scripts/ideation_dashboard/web/views/doxbench-state.js` — `BUFFER_KINDS` and the exactly-two-keys validator become a keyed buffer set with `outline` reserved; `doxbench-save.js` — `SAVE_BUFFER_ORDER` becomes the outline-ancestry rule plus documents in a deterministic order, and one document's refusal stops no other; `doxbench_turns.py` — `require_outline_and_document`, `PROPOSAL_TARGETS`, `ObservedHashes`, the nine-section `PROMPT_SECTION_ORDER` and `SYSTEM_CONTRACT_TEXT`; `doxbench-chat.js` — the rail header becomes the loaded-document selector; `doc-wheel.js` — the expanded tile's one `open` verb becomes read / edit / save with a loaded-and-dirty tile state; `doxbench-editor.js` and `staging-workbench.js` — the canvas and context region read the loaded set; `serve.py` — the thread sidecar and knowledge-service routes under the existing interactivity allowlist, the harness bridge behind the unchanged `WorkbenchModelPort`; `session_pr.py`/`gate_routes.py` — share-session reusing the port's existing `push` member and opening no pull request; NEW modules for the packet assembler, the Staged-Set Knowledge Service and its MCP boundary, and the stdlib-only harness bridge; `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml` plus the release surface `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, `contracts/releases/<tag>.digests.yaml`; and `tests/ideation-dashboard/` — the pinned buffer-shape, turn, save-order, DOM, accessibility and mutation-boundary assertions re-pinned honestly, never deleted)
target_release: implemented
contract_release: additive — a second, co-resident chat-turn envelope family in `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml`, published in the next available ADDITIVE bundle minor, ALLOCATED AT REALIZATION per `docs/contract-versioning-policy.md` ("a proposed change MUST NOT reserve a minor number before merge order is known"). No number is reserved here; the released v1 envelopes stay byte-identical and valid.
Status: draft
Sequenced-after: add-doxbench-editing-phase-a (three MODIFIED requirements below are declared relative to Phase A's outcome)
---

# Proposal: add-doxbench-editing-phase-b

## Why

Phase A landed the half of Brett's editing model that fits the machinery that
already exists: one active buffer, two views, one Save, one Cancel, and a chat
that binds to the selection. It said in writing what it was leaving behind —
"Phase B is everything that needs N path-keyed buffers" — and it left one
obligation on the record as a carve-out: **naming the bound buffer in the
durable turn RECORD needs a chat-turn contract release Phase A forbade itself,
so the obligation rides Phase B.**

Since then the topic stopped being half-ruled. Brett annotated the running
doxBench app twice on 2026-08-18 and then ruled the memory design in session,
and a verification pass the same day closed the two structural pieces the
ruling left implicit. The fragment now carries **26 settled claims and seven
dispositioned questions, none of them `open`.** Nothing in Phase B is a
recommendation waiting for an answer; the whole of it is transcription plus
mechanism.

What the rulings actually ask for is bigger than "more tabs", and the reason is
worth stating plainly: **the surface stops being an editor with a chat beside
it and becomes a working session over a staged set.** Three of Brett's rulings
say that in three different places.

- The rail header is not a label any more, it is a **selector** — "make this a
  dropdown box that lists the files that have been loaded by clicking the edit
  button on the wheel. the selected one is the file we are working on." A
  selector implies a set, and the set is what today's code cannot hold:
  `BUFFER_KINDS` is `Object.freeze(["outline", "document"])`,
  `validatedDoxBenchState` throws on any other key set,
  `require_outline_and_document` refuses a turn that does not carry exactly one
  of each, and `SAVE_BUFFER_ORDER` is a fixed ordered pair. Four enforced
  contracts, re-cut together.
- The chat is not one conversation any more, it is **one thread per document
  with one context across all of them** — "we need to save the thread per
  document. but the context for the chat has all the threads in it. so we need
  to look at a memory system that will allow that to work well for this chat
  window." Threads must be SAVED, which makes them artifacts, which makes them
  governed.
- The context is not the two buffers any more, it is a **bounded packet
  assembled from the staged set** — the active thread in full, every other
  thread's state header, and selected corpus evidence, with approved and
  ratified content protected from aggressive compression BY the assembler
  because only the assembler can read a lifecycle `Status:` header.

That third one is where this change stops being a doxBench feature. A governed,
shared, derived retrieval surface that assembles bounded context packets, ranks
sources by lifecycle status, meters what it spends, and refuses to let raw chat
become truth is not a new invention here — it is the ratified neutral
`memory-gateway` capability, and Brett's ruling addendum says so explicitly and
attaches an honest flag to it: *this may be the contract's first live consumer,
so read the full spec and declare conformance rather than take the summary on
faith.* This proposal did that, and the answer is in the next section: the
knowledge service realizes memory-gateway's M0 read-and-packet shape and two of
its M1 requirements, and memory-gateway needs **one small delta of its own**,
because every rail it defines for a customer subject and a credentialed
provider is inapplicable to a subject-free local retrieval consumer — and
"inapplicable" must be DECLARED, not silently skipped.

## What Changes

Ten things, in the dependency order they must land in. Everything here is
already ruled; the mechanism decisions are in `design.md`.

1. **The buffer set widens from exactly two to `outline` plus N loaded
   documents.** Three pinned layers change together: the state validator's
   exactly-two-keys rule becomes a keyed set with `outline` permanently
   reserved and every other key a document; the turn machinery's
   one-outline-one-document requirement and its two-value `PROPOSAL_TARGETS`
   become the request's own declared buffer set; and the fixed
   outline-then-document save order becomes an explicit rule — **the outline
   first because its commit establishes the session ancestry, then every
   document in a deterministic order, and one document's refusal stops no
   other document.** The per-buffer stale-hash guard changes not at all: it was
   always buffer-scoped, and widening the set means applying it N times.

2. **The loaded set is chosen by a dropdown in the chat rail header, and its
   selection IS the active buffer.** "Loaded" means exactly one thing from here
   on: opened through a docs-wheel tile's edit verb. The dropdown lists the
   loaded documents, scrolls rather than folding, hover-expands a filename that
   does not fit on one line, and the chat binds to whatever it names — Phase A's
   binding rule, generalized, with no second context-tracking mechanism beside
   `state.active_buffer`.

3. **The docs-wheel tile carries three verbs: read, edit, save.** Read is
   unchanged — the immersive large-window reader. Edit loads the document into
   the chat context, which is how a document joins the loaded set. Save lives on
   the tile, is reachable only when that document has unsaved changes, and
   performs the same governed act as the panel Save through the same pipeline —
   a second entry point, never a second save path. A loaded tile is COLORED so
   the human can see that it must be saved.

4. **Each loaded document carries its own persisted thread.** A sidecar file on
   the session branch, carrying a structured **thread-state header** — active
   goal, accepted facts, open questions, decisions made in-thread,
   retrieved-evidence refs, pending actions — above the transcript. Threads
   commit on the document's Save, riding the existing commit-per-gate-action
   substrate. Compaction preserves those commitments rather than narrative.
   Threads are working memory: excluded from PR-as-save promotion by default,
   and a finding leaves a thread only through the existing lifecycle verbs.

5. **Share-session is an explicit verb.** It commits the threads, pushes the
   session branch, and returns the ref; a colleague resumes the session from the
   fetched branch. Threads are local until it runs. It opens no pull request,
   grants no approval authority, and reuses the pull-request port's existing
   `push` member rather than adding a remote-write surface.

6. **The Staged-Set Knowledge Service assembles every turn's context as a
   memory-gateway bounded context packet** — the active thread in full, the
   other threads' state headers, and selected corpus evidence. It is exposed
   behind **one MCP boundary** (`search`, `get_source`, `promote_finding`,
   `reindex`; `graph_query` reserved and unimplemented) over an internal
   assembly port with provider profiles. **v1 is graph-less**: local hybrid
   retrieval — lexical plus small embedded vectors plus the structured
   thread-states. A graph provider is admitted only when a concrete graduation
   trigger fires (recurring dependency traversal, contradiction detection, or
   change-impact analysis), Cognee preferred and version-pinned, Graphiti +
   FalkorDB Lite the alternate. The retrieval backend is an **install-time
   declaration** per the ratified two-case principle. Approved and ratified
   content is exempt from aggressive compression BY THE ASSEMBLER, keyed on the
   content's lifecycle `Status:` header, and the source-ranking hierarchy —
   ratified canon > staged facts > promoted findings > thread state >
   harness-local memory last — is encoded in the harness system prompt.

7. **Compression is a three-layer stack with three distinct fidelity
   contracts**: selection (governed, lossless-by-reference), semantic
   compaction into the thread-state header (governed, lossy by design,
   human-reviewable, promotion-gated), and mechanical reversible compression at
   the LLM boundary — realized v1 by the harness's own `/shake` /
   `artifact://` offload, inside our own trust boundary, no proxy and no new
   dependency. Headroom is **watch-listed with its adoption gates recorded**,
   and this change deliberately does not depend on it.

8. **The chat harness is oh-my-pi behind a thin stdlib-Python bridge under the
   existing model port.** The bridge translates the serve's HTTP-shaped call to
   the harness's stdio RPC (`omp --mode rpc`) and is an ADAPTER for the
   unchanged three-member `WorkbenchModelPort` — no fourth port member, because
   per-turn model choice is set-model-before-prompt INSIDE the adapter. One
   harness session per document thread; doxBench mirrors turns to the sidecars,
   which remain the record; the harness's own memory backends never hold the
   threads. The model menu is `auto / Opus / Kimi K3 / …`, where `auto` is our
   own role-mapping rule rather than a provider feature, and where an
   API-backed entry gets its credential from the ratified broker lane and never
   from the bridge.

9. **A chat-turn contract release carries the bound buffer and the model.** The
   released envelope is closed in both directions, so the F2 obligation and the
   N-buffer request shape both need it. It is realized as a **second,
   co-resident envelope family** — the v1 envelopes stay byte-identical and
   accepted — which makes the release ADDITIVE, published in the next available
   bundle minor and **allocated at realization**, never reserved here.

10. **The verify list gates realization.** Seven items the ruling depends on
    that our own research has not independently confirmed — the harness's memory
    backends, its MCP client depth, whether it re-reads `SYSTEM.md` per turn,
    Cognee's current embedded backend after the Kuzu archival, where the
    `artifact://` store lands on disk, `/shake`'s programmatic surface, and
    memory-gateway's realization depth elsewhere in xFactory — are **blocking
    tasks**: each is verified and its finding recorded before the slice that
    depends on it may start.

## Memory-gateway conformance, declared

Read in full, not inherited from the ruling's summary. The knowledge service and
the per-turn packet assembler realize:

- **`Context Packets Bound Runtime Memory` (M0)** — the per-turn packet is
  purpose-bound, TTL-bearing, source-referenced, and rejected when presented for
  another purpose. v1 consults no ontology package, so the semantic-context pins
  that requirement demands *when semantic inference is included* do not arise —
  and admitting a graph provider later is exactly what makes them arise, which
  is why the graduation gate names them.
- **`Canonical Ports Are Product Neutral` and `Provider Profiles Declare
  Capability` (M0)** — the internal assembly port is the product-neutral
  surface; the local hybrid v1 and any later graph provider are profiles behind
  it that declare capability without granting authority.
- **`Rails Run Before Provider I/O` (M0)** — selection, the lifecycle-status
  exemption, and the compression policy run BEFORE any retrieval or provider
  call, and a refusal discloses no packet content.
- **`Gateway Callers Are Authenticated And Hold No Provider Credentials`
  (M0)** — the loopback console's resolved actor is the caller identity; the
  bridge and the retrieval provider hold no provider credential.
- **`Fail Modes Are Explicit And Break-Glass Is Audited` (M0, fail-modes
  half)** — the degraded postures are declared: no knowledge service means
  headers-only context, no model port means editor-only, and neither bypasses a
  rail to reach a provider. No break-glass path exists on this surface.
- **`Worker-Local Memory Remains Separate` (M1)** — the split-brain
  prohibition IS this requirement: the harness's native memory is worker-local
  and non-authoritative, the sidecars are the record, and an observation becomes
  durable only through promotion.
- **`Promotions Are Explicit And Reviewed` (M1)** — the promotion gate. Honest
  narrowing: the requirement's own scenarios speak of customer memory moving
  into client or domain layers; this consumer's promotion target is a document
  in the lifecycle, so what it realizes is the requirement's rule (no automatic
  durability, review before the target accepts it), not its layer vocabulary.

What it does NOT realize, stated rather than skipped: consent profiles and the
subject-safety rail (there is no customer subject anywhere on this surface),
provider bindings and short-lived grants (v1's provider is an in-process local
index with no credential; an API-backed model or a hosted retrieval backend
gets its credential from the ratified broker lane, which IS that mechanism),
revocation, erasure, migration, provider mapping, the customer fill and
maintenance modes, and the derived-memory-binding schema. **Usage metering
(M3) is partial**: per-turn and per-session token telemetry is emitted, but a
self-hosted authoring console has no client, domain, or bill-to target, so this
change claims compatibility with that requirement and not conformance to it.

**Hence one delta to `memory-gateway` itself.** Today the contract offers a
consumer exactly two honest options: claim conformance while quietly skipping
half of M0, or declare non-conformance and lose the vocabulary. This change
adds one requirement making a third option real — a **declared subject-free
local consumer class** whose declaration must NAME each rail it declares
inapplicable and why, which is refused to any consumer that holds provider
credentials or acquires a subject scope, and which loses the declaration the
moment either changes. That is a small, neutral addition that makes the
inapplicability auditable; it grants no exemption and relaxes no rail.

**And the honest "first consumer" statement, stated precisely**
(`verification-findings.md` §3.7): this change is the first consumer to declare
formal per-requirement conformance to `memory-gateway` and the first
SUBJECT-FREE one — not the first thing in xFactory to reference the contract's
vocabulary at all. `installs/hermes-install`'s `add-memory-gateway-binding`
(archived 2026-07-24) precedes it with real, tested code, and is narrower,
subject-bearing, and self-described as a runtime convention ahead of a gateway
service that does not exist there yet. That precedent strengthens rather than
weakens the case for the delta: its own text shows the contract has no
vocabulary for a consumer with no subject at all.

`governed-derived-model` is treated differently and deliberately. Claim 23 says
the thread-state header, the summaries, and any future graph index conform to
it. Read directly, that capability's conformance surface is a DomainxFactory's
`xfactory_derived_model_conformance` declaration over template-backed object
kinds — a declaration an authoring surface has no place in. So Phase B asserts
the PROPERTIES in its own requirements (non-authoritative by construction,
regenerable, promotable only by creating a new object through review) and does
NOT claim a tier it cannot be validated at. Flagged for Brett's ratification
read as an interpretation, not a silent narrowing.

## Impact

- `ideation-dashboard` — MODIFIED: the editor buffer contract (N path-keyed
  buffers; the ancestry-plus-independence save rule); the grounded chat turn
  (the widened request, the bound-buffer record, the model echo, the context
  packet, the degraded postures); typed proposals (target is a buffer key);
  the scoped view (the tile's three verbs; the canvas presents the selected
  loaded buffer); the model catalog and provider boundary (the menu, `auto` as
  a declared routing rule, the adapter behind the unchanged port). MODIFIED
  relative to Phase A's outcome: the chat-binding requirement (binding
  generalized; the F2 deferral DISCHARGED), the view-surface requirement
  (its "this does NOT widen the buffer set" clause is what Phase B is), and
  the one-Save-one-Cancel requirement (the canvas still carries exactly one of
  each; the tile's per-document Save is admitted as a scoped entry point).
  ADDED: the loaded-set buffer contract; the loaded-document selector; the
  tile's three verbs; per-document threads and their state header;
  share-session; the Staged-Set Knowledge Service and its packet; the
  three-layer compression stack; the harness bridge; the chat-turn release
  obligation.
- `memory-gateway` — ADDED: one requirement declaring the subject-free local
  retrieval consumer class.
- Code surface and the contract release surface: as declared in the
  front-matter. The chat-turn release is additive and its bundle minor is
  allocated at realization.
- **Sequencing**: this change's three Phase-A-relative MODIFIED requirements
  require Phase A's deltas to promote first. Phase A's own archive gate is
  still open on merged-commit evidence.

## Deliberately out of scope

- **A graph engine, in any form.** Not Cognee, not Graphiti, not FalkorDB, not
  a "small" one behind a flag. v1 is graph-less on the recorded Mem0 v3
  caution, and the graduation trigger is a named condition, not a preference.
- **Headroom**, or any third-party compression proxy. Watch-listed with
  adoption gates; encoding it as a dependency is exactly what this change
  refuses to do.
- **Any cloud or hosted backend as a default.** The retrieval backend is an
  install-time declaration whose self-hosted case is local-embedded.
- **Hosted-plane anything.** Branch sessions are a local-plane capability;
  threads, share-session, the knowledge service, and the harness bridge all
  inherit that and are absent on the hosted plane.
- **A real provider adapter's credential lane.** That is
  `add-model-provider-broker`'s subject and stays there; the bridge holds no
  secret and this change re-cuts no credential boundary.
- **Widening the model port.** Three members, unchanged. A fourth would be a
  second provider verb by another name.
- **Promoting a thread finding automatically, or a parallel decision store.**
  Promotion is gate-only, through the lifecycle verbs that already exist.
- **A `graph_query` implementation.** The name is reserved in the MCP tool
  contract so its later arrival is not a boundary change; reserving is not
  building.
- **Retiring the outline's reserved status.** `outline` stays a permanently
  reserved key with the ancestry role its commit already has.
