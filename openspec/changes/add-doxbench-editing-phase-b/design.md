# Design: Phase B — N buffers, a thread per document, and a governed packet

## Context

Phase A's design ended with a list titled *"What Phase B gets, and why it has to
wait"*. Everything on that list needed N path-keyed buffers, and Phase A was
built so none of it would be harder afterwards: the view tabs render ONE active
buffer and do not care how many exist, Save was already whole-canvas over the
buffer enumeration, Cancel targets a single key, and the chat binds to a single
key. That prediction held. **Nothing on the view surface changes in Phase B.**
The widening happens in exactly the three places that ever enumerated `outline`
and `document`: the state contract, the turn contract, and the save ordering.

What Phase A could not predict is how much MORE the topic would ask for by the
time Q1, Q3 and Q7 were ruled. The rulings of 2026-08-18 turned "more buffers"
into a working session: a thread per document, a context that spans the staged
set, a governed retrieval service, a compression policy with three fidelity
contracts, and a harness. This design's job is to say how each of those is
built out of machinery that already exists, and to be explicit where it is not.

The dispositions this design implements, in the fragment's own words:

- **Q1, ruled** — "make this a dropdown box that lists the files that have been
  loaded by clicking the edit button on the wheel. the selected one is the file
  we are working on. if not fit in one line, then use hover to expand to see
  full filename." No numbered chips, no LRU fold.
- **Q3, ruled** — "add a load button. read will still pull up an imersive reader
  experience of the doc in a large window. the new \<Edit\> button will then load
  this into the chat context. Once loaded and editable by chat, color this tile
  so we know is must be saved. also add a save button here. So we have read,
  edit, save and save only active if there are changes. the save acts same as
  the save button that is in the preview panel."
- **Q7, ruled** — the two-plane memory design: session working memory (thread
  sidecars, truth) separate from the Staged-Set Knowledge Service (governed,
  shared, derived), plus the addendum's memory-gateway conformance and
  three-layer compression stack.

## 1. The N-buffer mechanism

### 1.1 The state model: a keyed set whose current shape is already legal

Reading `doxbench-state.js` closely settles this cheaply. Every per-buffer
primitive is ALREADY buffer-scoped and needs no change at all:
`beginBufferEdit`, `settleBufferHash`, `adoptSavedBase`, `discardBuffer`, and
`applyProposalToBuffer` all take one buffer and return one buffer, and the
generation guard (`hash_generation`/`hash_pending`, `current_hash`) is keyed to
CONTENT, not to a slot. What breaks is only the FIXED SLOT NAMES and the
validators that enumerate them:

| Site | Today | Phase B |
|---|---|---|
| `BUFFER_KINDS` | `Object.freeze(["outline","document"])` | the KIND vocabulary stays exactly this; it stops being the state's key list |
| `validatedDoxBenchState` | throws unless keys are exactly `{outline, document}` | requires `outline` present, every other key a document buffer whose key equals its own path, and the reserved `document` key at most once |
| `createDoxBenchState` | builds two buffers from two descriptors | builds `outline` plus zero or more document descriptors |
| `replaceBuffer` / `setActiveBuffer` | switch on the two kinds | operate on the buffer KEY |
| `persist`/`restoreDoxBenchState` | writes and demands exactly two | writes and restores the keyed set, refusing an envelope whose keys disagree with its buffers |

**D1. The buffer KEY is the document's repository-relative path; `outline` is
reserved; `document` stays reserved for the ONE unbacked create slot.** This is
chosen over an opaque generated id for one reason that matters more than
elegance: **today's state is then already a legal instance of the new shape.**
A current session holds `{outline, document}` — a reserved outline key plus the
reserved unbacked-document key — which the widened validator accepts unchanged.
The restore path therefore needs no migration, no version bump on the browser
envelope, and no "old shape" branch, and a Phase A session restored under a
Phase B build keeps working. Using the path as the key also makes
"load the same document twice" impossible by construction rather than by a
lookup, which is exactly the bug a generated id would have invited.

The reserved `document` key is the create lifecycle Phase A inherited: a buffer
with `path: null` cannot be keyed by its path because it has none. On its first
Save the server reports the path it created, so the buffer is RE-KEYED from
`document` to that path (`adoptSavedBase` already produces the advanced buffer;
the re-key is a state-level move, not a new buffer), and the reserved key frees
up. At most one unbacked buffer may exist at a time, which is not a new limit:
there is exactly one create flow.

**D2. `owned` keeps its meaning and becomes load-relevant.** A context-only
document (inherited, cluster-neighbourhood, cited, inbound) is loadable — it is
useful to talk about — and its buffer carries `owned: false`, which
`doxbench-save.js` already withholds from the governed Save with a stated
context-only refusal. Phase B adds the UI half the fragment never mentioned:
such a tile shows no reachable Save and is not marked as needing one, because
marking a document "must be saved" when the tile may not save it would be a
false statement about the surface's own authority. This resolves a collision
between Claim 8's tile Save and the ratified rule that
"inherited, cluster-neighbourhood, cited, and inbound-context documents remain
read-only in this tile".

### 1.2 The turn contract

`doxbench_turns.py` is two-buffer-shaped at three points, and each has an exact
generalization:

- `require_outline_and_document` → **require exactly one outline and one or more
  documents, each bound to a distinct in-scope editable path.** The
  buffer-binding check (`_require_buffer_binding`) runs per buffer exactly as it
  does today, including the T104 R-12 session-base widening, which is
  per-buffer already.
- `revalidate_scope`'s `active_document_path != document_path` equality → **the
  request's declared BOUND-BUFFER key must name one of the supplied buffers**,
  and every supplied path must be in-scope and editable. This is the same
  refusal discipline, expressed over a set instead of a pair; a request that
  declares a binding it did not supply is refused before any provider call.
- `PROPOSAL_TARGETS = ("outline","document")` and `ObservedHashes(outline=…,
  document=…)` → **targets and observed hashes keyed by buffer key.** The
  proposal cap stops being the literal `2` and becomes a bound expressed over
  the request's own buffer count, so widening the loaded set cannot silently
  widen what one response may rewrite beyond what it was grounded on.

The nine-section `PROMPT_SECTION_ORDER` stays DETERMINISTIC and grows: the two
buffer sections become the outline section plus one section per loaded document
in the buffer set's deterministic order, and the packet contributes its own
sections (§3). `SYSTEM_CONTRACT_TEXT` gains the source-ranking hierarchy. The
order remains declared in one constant, because a prompt whose section order
depends on dictionary iteration is a prompt no test can pin.

### 1.3 Save ordering for N documents

Today's rule is a fixed pair with a fail-closed CHAIN: `SAVE_BUFFER_ORDER =
["outline","document"]`, and "ANY earlier buffer that neither committed nor was
unchanged stops the ones behind it". Widening the list would keep the chain and
get the semantics wrong, so the rule is restated:

**D3. Outline first as ANCESTRY; documents independent; determinism is the
realization's obligation.**

1. The `outline` buffer, when dirty, is persisted FIRST. Its commit establishes
   the session ancestry every document commit descends from — the module's own
   recorded reason, unchanged.
2. A dirty outline that did NOT land stops every document, each reported
   `not_attempted` with the missing-ancestry reason. Unchanged from today.
3. Every dirty document is then attempted INDEPENDENTLY. One document's refusal
   does NOT stop another, because documents carry no ancestry dependency on each
   other: each save is one gate action producing one commit on the same branch,
   and commit *n+1* descends from commit *n* regardless of which document *n*
   held. Keeping the chain here would report untried work as blocked by a
   refusal that had nothing to do with it — a false statement about both
   buffers.
4. Brett's rule is "documents in any order", which constrains the CONTRACT, not
   the code. The realization declares a deterministic order (lexicographic by
   path is the obvious one) so the commit series is reproducible and testable.
   "Any order" means no ordering rule is imposed on documents; it does not mean
   a nondeterministic one is acceptable.

The per-buffer verdict report (`outcomeRow`, seven fields, always present) is
unchanged in shape and simply has more rows. `wholeStatus`'s `partial` verdict
becomes much more likely, which is why the ratified per-buffer reporting
requirement matters more after this change than before it.

### 1.4 The tile Save's scope — an under-determination, resolved and flagged

Brett wrote "the save acts same as the save button that is in the preview
panel". The panel Save persists the WHOLE dirty set. The tile Save is enabled
by ONE document's dirtiness. Those two sentences do not fully determine the
scope of the tile's act, and this design picks one:

**D4. The tile Save runs the SAME pipeline, restricted to that document plus
the outline-ancestry step when the outline is dirty.**

Reasons: a control that lives on one document's tile and is enabled by that
document's state should not persist three other documents the human is not
looking at — the same asymmetry argument Phase A used to keep Cancel narrow
while Save stayed broad, and the hazard grows with the loaded set. The
ancestry step cannot be skipped, or a scoped entry point would become a way to
commit a document without the ancestry the ordering rule requires; so when the
outline is dirty, the tile Save commits it first and REPORTS it, on the same
per-buffer surfaces the canvas Save reports on. **Flagged for Brett:** the
alternative reading — the tile Save is literally the panel Save, drawn a third
time, persisting everything dirty — is one sentence away and easy to switch to
if that is what "acts same as" meant.

## 2. The loaded set, the selector, and the tile

**D5. "Loaded" has exactly one definition and one entry route.** A document
joins the loaded set only through a `docs` tile's load verb. Not a retrieval
result, not a proposal, not the snapshot, not an inherited edge. This is what
keeps the selector honest: it lists what a human chose to work on, so its
length is a decision the human made rather than a side effect of what the
retrieval happened to find.

**D6. The dropdown IS the overflow policy.** Q1's original recommendation was
numbered chips with an LRU fold; the ruling replaced it with a scrolling
selector, which dissolves the "many open edits" problem by construction. There
is therefore no eviction anywhere in this design — and deliberately so: every
loaded buffer may hold unsaved work, and a policy that evicts to make room is a
policy that discards human text. The loaded set is instead BOUNDED, and reaching
the bound REFUSES the load with the measured bound stated. That is the house
pattern (refuse and say the number) rather than the other house pattern (degrade
softly), because the soft degradation here would be data loss.

**D7. The selector is a selection surface, not a second state authority.**
`state.active_buffer` — now a buffer key — remains the one answer to "what is
selected". The selector renders it and sets it; loading sets it; the `outline`
selection tab sets it. Three routes, one value, and the requirement says all
three must agree. Basename collisions get a distinguishing rendering because two
identically-labelled entries in a selector are worse than one long label.

**D8. The tile's verbs are named read / load-for-editing / save in the
contract, and `read` replaces today's `open`.** Two naming debts get paid here.
The wheel tile's current verb is labelled `open` ("open … in the read-only
source viewer"); Brett's vocabulary is `read`, and the contract uses `read`.
Second, Phase A reserved the bare word "edit" for editing that happens INSIDE
the app and relabelled the external-editor escape hatch precisely so this verb
could exist without a third claimant to the word. The delta calls the verb
LOAD-FOR-EDITING because that is what it does — it loads; the editing happens
afterwards, in the canvas or through the chat — while the visible control
follows Brett's annotation. `edit-document` and `edit-apply` remain untouched
machine keys.

**D9. The tile marking is driven off live buffer state and is never persisted.**
Q3's recommended answer already argued this and the ruling kept it: "has an open
unsaved edit" is a fact about a browser, and the snapshot is a regenerated
derived projection whose generator cannot observe one. The marking reuses the
wheel's existing badge/colour idiom rather than inventing a second visual
language. Two states are distinguishable, because Brett named both: LOADED
(the tile is in the chat context) and LOADED-AND-DIRTY (it must be saved).

## 3. The packet-assembly pipeline

### 3.1 The pipeline, in order

```text
turn submitted (browser: outline + N loaded buffers + bound key + message)
  │
  ├─ 1. scope + binding + identity revalidation        [existing, per buffer]
  │
  ├─ 2. SELECTION rail  ────────────────────────────── layer 1 (lossless by ref)
  │      selected thread in full
  │    + other loaded threads' STATE HEADERS only
  │    + evidence: knowledge service search over
  │        {this tile's staged set} ∪ {promoted findings}
  │
  ├─ 3. lifecycle-status EXEMPTION rail
  │      each packet item carries its Status:; approved/ratified items are
  │      marked exempt from aggressive compression HERE, upstream of any
  │      compressor, because only this stage can read a Status: header
  │
  ├─ 4. bounds check → refuse with the measured dimension (no truncation)
  │
  ├─ 5. deterministic prompt assembly
  │      system contract (incl. the source-ranking hierarchy)
  │      · model data handling · scope · working subject
  │      · thread (selected, full) · thread-state headers (others)
  │      · evidence (with refs) · outline buffer · document buffers
  │      · human message · response instruction
  │
  ├─ 6. dispatch through the unchanged 3-member port → adapter → bridge
  │
  └─ 7. mirror the turn into the selected document's sidecar; meter tokens
```

Steps 2 and 3 are RAILS: they run before any retrieval provider or model
provider is reached, and a refusal at either discloses no packet content. That
ordering is not a preference — it is `memory-gateway`'s
`Rails Run Before Provider I/O` applied literally.

### 3.2 The packet is a memory-gateway bounded context packet

It declares purpose, the exact sources it carries with refs, its bound scope,
and its expiry; it is invalid for another purpose, another scope, or after
expiry; and a consumer presented with a stale or foreign packet requests a new
one. v1 consults no ontology package, so the semantic-context pins that
requirement demands *when semantic classification or inference is included* do
not arise — and that is precisely the clause the graph-graduation gate has to
satisfy if a graph provider is ever admitted (§5.2).

### 3.3 The MCP boundary and the assembly port

**One boundary, four tools, one reserved name.** `search`, `get_source`,
`promote_finding`, `reindex`; `graph_query` is RESERVED and unimplemented so its
later arrival is not a boundary change. Reserving a name is not building a
feature, and the delta says the reserved name must stay unimplemented until a
graduation trigger is recorded.

Behind the boundary is the **internal assembly port** — the product-neutral
surface a retrieval backend implements. This is the two-layer shape
`memory-gateway` asks for: the tool contract is what a caller sees, the port is
what a provider implements, and a backend swap changes neither. Backends are
declared PROVIDER PROFILES: capability declared, authority not granted.

**D10. v1 is graph-less, and that is a recorded finding rather than a
preference.** Local hybrid retrieval — lexical plus small embedded vectors plus
the structured thread-states. The caution on the record is the **Mem0 v3
finding** — graph memory lost on recall, roughly 3× slower, roughly 2× the
token cost, so it was removed — which reaches us through the external design
review Brett supplied and was dispositioned by his ruling as the MOTIVATING
caution rather than independently re-measured here. It is cited as a reason to
default off, not as a measurement of our own workload; the graduation trigger,
not this number, is what admits a graph. A graph engine is
admitted only when a concrete GRADUATION TRIGGER is recorded: a recurring need
for dependency traversal, contradiction detection, or change-impact analysis.
Cognee preferred and version-pinned; Graphiti + FalkorDB Lite the alternate.
Verify-list item (d) exists because Cognee's default embedded backend is in flux
after the Kuzu archival, and a pin against a moving default is not a pin.

**D11. The backend is an install-time declaration, never a runtime choice.**
The ratified two-case principle: local-embedded for a self-hosted install, a
hosted backend only where a tenant install declares one. A turn, a prompt, or a
heuristic MUST NOT pick a backend — the whole point of the declaration is that
an operator can read what their install talks to.

### 3.4 Degraded postures

Both are existing house patterns, extended:

| Missing | Posture | Precedent |
|---|---|---|
| knowledge service | reduced packet — selected thread + loaded buffers, reduced posture STATED; no unbounded substitute, no rail bypass | the empty-catalog SUCCESS posture: a plane with nothing configured gets a conformant honest answer, not the failure that means the contract could not be read |
| model port / bridge | editor-only: buffers, loaded set, save and threads-on-disk stay usable; the chat states why it is unavailable on the send control | Phase A annotation round 2's send-button posture, and the ratified FR-025/SC-008 editor-only plane |
| gate capability | no load, no tile save, no thread, no share-session; affordances render as copyable descriptors | `Branch sessions are a local-plane capability` |

The two are independent: a live model with no knowledge service is a reduced
packet, not a refusal, and a live knowledge service with no model is an editor
with retrieval that nothing consumes yet.

## 4. Threads

### 4.1 File format sketch

One sidecar per loaded document, on the session branch, inside the session
worktree. Illustrative — the realization pins the exact spelling:

```markdown
---
schema_version: 1
kind: doxbench-document-thread
document: ideation/staging/<topic>/<file>.md
scope: { repository: openxFactory, tile_kind: staged, tile_id: <topic> }
authority: non_authoritative
regenerable_from: transcript
---

## Thread state

Active goal: <one sentence>
Accepted facts:
  - <fact> [evidence: <ref>]
Open questions:
  - <question>
Decisions in thread:
  - <decision> — <basis>
Evidence refs:
  - <path|ref>
Pending actions:
  - <action>

## Transcript

### turn <id> · <model> · bound: <buffer key>
human: …
assistant: …
```

Three properties are load-bearing rather than cosmetic:

- **The header is above the transcript** so a reader — human or assembler —
  gets the commitments without reading the conversation, and so the packet can
  carry OTHER threads' headers without carrying their transcripts.
- **`authority: non_authoritative` and `regenerable_from: transcript` are
  written into the file**, so nothing downstream has to infer that a summary is
  not truth.
- **The turn line names the model and the bound buffer**, which is the same
  pair the released envelope carries. The sidecar and the wire agree by
  construction rather than by two independent conventions.

### 4.2 Persistence, compaction, promotion

**Threads commit with the document's Save**, riding
`commit_gate_action`/`commit_first_edit` so the thread and the document text it
discusses cannot land through separate commits — the ratified one-commit-per-
gate-action rule applied to a second artifact rather than relaxed for it.

**Compaction preserves commitments, not narrative.** Concretely: dropping an
open question, a decision, an accepted fact, an evidence ref or a pending action
is a DEFECT; dropping prose that merely restates them is the point. That is
layer 2 of the compression stack and it is governed: human-reviewable,
promotion-gated, non-authoritative, regenerable.

**Promotion is gate-only.** A finding leaves a thread by becoming an idea note,
a fragment, or a disposition on the topic, with provenance, through the
lifecycle verbs that exist. No parallel decision store, and no path by which raw
chat becomes durable truth automatically. Threads are excluded from the session
pull request's promotion BY DEFAULT — they are conversation scaffolding, and a
reviewer reading a PR of documents should not have to read the conversations
that produced them unless someone chose to include them.

### 4.3 Share-session

**D12. Share-session reuses the pull-request port's EXISTING `push` member and
opens no pull request.** `session_pr.py` already declares `push(branch)`
separately from `open_or_update(...)`, so the verb is strictly LESS than
`open-pr`: commit the threads, push, return the ref, record the gate action. No
new remote-write surface, no second identity path, and the plane rule the save
verb already carries applies unchanged (local plane = the invoking engineer's
own credential, never a stored service identity).

**D13. Nothing leaves the machine implicitly.** No Save, turn, compaction, or
scheduled task may push. A working note that leaves the machine without an
explicit act is a disclosure nobody chose, and threads are exactly the artifact
where that matters: they carry half-formed reasoning about material that is not
yet governed.

**Scope call, recorded:** the contract and the realization tasks for
share-session are in this change; the realization slice MAY trail as a later
one. It is the one item here with no UI dependency on anything else, so
sequencing it last costs nothing and delaying its CONTRACT would leave threads
with an unstated sharing model, which is worse.

## 5. The harness bridge

### 5.1 The seam, unchanged

`WorkbenchModelPort` has **exactly three members** — `timeout_seconds`,
`catalog()`, `dispatch(prompt_envelope)` — and a companion test's
`FORBIDDEN_PORT_MEMBERS` bans other spellings so nobody grows a second provider
verb by accident. Phase B respects that literally:

**D14. The bridge is an ADAPTER for the three-member port, not a widened
port.** Per-turn model choice is set-model-before-prompt INSIDE the adapter,
reading the `model_id` the envelope already carries. Harness session switching
is inside the adapter. `/shake`-style offload is inside the adapter. Every one
of those would otherwise have argued for a fourth member, and a fourth member is
a second provider verb by another name.

The model menu is `catalog()` output, which means `auto / Opus / Kimi K3 / …`
needs no new mechanism — and one honesty rule falls out of the ratified
data-handling badge: **`auto` is a ROUTING RULE we own, not a provider model**,
so its entry declares itself as such and carries the badge of every model it may
route to. An entry that hid a routing decision behind a model-shaped id would
report a handling posture it does not control. Kimi K3 in the menu means API
access — the open weights need ≥8×H100 and are not local — so its badge says
so, and its credential comes from the ratified broker lane
(`add-model-provider-broker`), never from the bridge.

### 5.2 Process lifecycle

The harness has no HTTP mode upstream; it speaks stdio RPC (`omp --mode rpc`).
So the bridge is a **local child process of the console's own server**, spoken
to over its stdin/stdout, and:

- **Started on demand**, at the first turn that needs it, not at serve start —
  an editor-only session must not spawn a model process it never uses.
- **Supervised**: one bridge per serve process, its liveness checked before a
  dispatch, its stderr captured to the serve's own log and never to the wire.
- **Restarted on failure**, with a bounded retry; a bridge that cannot start or
  has died surfaces as the honest model-unavailable posture, never as a crash, a
  hang, or a silent empty answer. The route's existing refusal shape and gate
  order are unchanged: it still refuses before consulting any port, still emits
  only the fixed code, and still leaks no diagnostic to the wire.
- **Loopback-local and credential-free**: unreachable from the browser or any
  non-loopback surface, and holding no secret of its own.
- **One harness session per document thread** (`switch_session`), so switching
  the selected document switches the harness session. Two threads sharing one
  harness session would let one document's context leak into another's.
- **The sidecar is the record.** doxBench mirrors each turn into the sidecar;
  the harness's native memory backends never hold the threads. Where such a
  backend is enabled at all it holds only non-authoritative material and is
  ranked LAST by the source hierarchy. Two stores claiming to be the same thread
  is a split brain, and the sidecar wins by contract rather than by convention.
  This is `memory-gateway`'s `Worker-Local Memory Remains Separate`, exactly.

Verify-list items (a), (b), (c), (e) and (f) all sit under this section:
the harness's memory backends, its MCP client depth, whether it re-reads
`SYSTEM.md` per turn (which decides whether the source-ranking hierarchy can
change mid-session or only at session start), where the `artifact://` store
lands on disk (which decides whether offloaded artifacts ride the branch under
share-session or sit outside it), and whether `/shake` is reachable
programmatically in RPC mode or only as an interactive command. Each is verified
and recorded before the slice that depends on it starts, because each could
change the mechanism rather than merely the settings.

## 6. The contract release

**D15. A second, co-resident envelope family — not a mutation of the closed
one.** The released schema declares `additionalProperties: false` on the
request AND the success envelope, `buffers` with `minItems: 2, maxItems: 2`,
`buffer_state.kind` as the two-value enum, `observed_hashes` requiring exactly
the keys `outline` and `document`, `typed_proposal.target` as the same
two-value enum, and `proposals.maxItems: 2`. Every one of those must widen.
Mutating them in place would make the widened shape the only shape, which is a
BREAKING change under `docs/contract-versioning-policy.md` — and the policy's
breaking path requires "at least one full minor release where the old shape
produced deprecation warnings" before a major, while a major would drag
`contract-v2.0`'s queued removals (the `hermes` flat keys, the `openworkflow_`
tokens) along with a doxBench wire widening. That is a blast radius nobody
asked for.

So the release ADDS a family beside the existing one, discriminated as the file
already discriminates its three envelopes: the v1 request, success and failure
stay byte-identical and keep validating, and the widened family carries the
outline plus N document buffers, the bound-buffer key on both request and
record, per-buffer observed hashes keyed by buffer, a buffer-key proposal
target, and the selected-model metadata. Change class: **ADDITIVE (minor)**,
with the v1 family DEPRECATED in the same release and its removal target
recorded — which is itself a minor class, and which starts the clock the policy
requires before any later major may remove it.

**D16. No version number is reserved here.** The policy is explicit: "A
proposed change MUST NOT reserve a minor number before merge order is known."
The bundle minor, the changelog entry, the digest inventory and the annotated
tag are all allocated and published AT REALIZATION, through the serialized
realization order, exactly as `contract-v1.31` was for openxWallet. The file's
own `contract_schema_version` stays `1` because nothing previously valid becomes
invalid. **Flagged for Brett:** if the ruling is that any new envelope-version
family bumps the FILE's `contract_schema_version` regardless of
backward-compatibility, then this becomes a major and the consequence above
(dragging `contract-v2.0`'s removals) is the thing to decide, not the numbering.

**D17. The F2 obligation is discharged the way Phase A said it must be.** Phase
A tried a server-side-only `PromptEnvelope.bound_buffer` and its review killed
it on two counts: unreadable (nothing serialized, persisted or rendered it) and
mis-derivable (it was derived from `active_document_path`, so a human working
the outline with a document loaded was recorded as bound to the document). Both
failure modes are forbidden in the delta: the record carries the DECLARED
binding on the wire, and inference from an adjacent field is refused.

## 7. Conformance declarations

### 7.1 `memory-gateway` — realized, with one delta

Read in full from `openspec/specs/memory-gateway/spec.md` rather than inherited
from the ruling's summary, as the ruling's own honest flag required.

**Realized** (M0 read-and-packet shape, plus two M1 requirements):
`Gateway Mediates Governed Memory Access` (routed through the service, never a
direct provider call as authoritative context) · `Canonical Ports Are Product
Neutral` (the assembly port) · `Provider Profiles Declare Capability` (the
retrieval profiles) · `Rails Run Before Provider I/O` (§3.1 steps 2–3) ·
`Context Packets Bound Runtime Memory` (§3.2) · `Gateway Callers Are
Authenticated And Hold No Provider Credentials` (the loopback console's resolved
actor; a credential-free bridge and provider) · `Fail Modes Are Explicit`
(§3.4; no break-glass path exists here) · `Worker-Local Memory Remains
Separate` (M1 — the split-brain prohibition IS this requirement) ·
`Promotions Are Explicit And Reviewed` (M1 — the promotion gate).

**Honestly narrowed:** `Promotions Are Explicit And Reviewed`'s own scenarios
speak of customer memory moving into client or domain layers. This consumer's
promotion target is a document in the lifecycle, so what it realizes is the
requirement's RULE (nothing durable without review) and not its layer
vocabulary. `Usage Metering Is Gateway-Owned` (M3) is PARTIAL: per-turn and
per-session token telemetry is emitted, but a self-hosted authoring console has
no client, domain or bill-to target, so this change claims compatibility, not
conformance.

**Not applicable, and this is the gap that needs the delta:** consent profiles
and the subject-safety rail (no customer subject exists anywhere on this
surface), `Provider Access Uses Bindings And Short-Lived Grants` (v1's provider
is an in-process local index with no credential; an API-backed model or hosted
retrieval backend gets its credential through the ratified broker lane, which IS
that mechanism), revocation and tombstones, erasure, migration, provider
mapping, the customer fill/maintenance modes, and the derived-memory-binding
schema.

The contract as written leaves a consumer two bad options — claim conformance
while quietly skipping half of M0, or decline the contract and lose its
vocabulary. **So Phase B adds one requirement to `memory-gateway`: a DECLARED
subject-free local consumer class** that must name each inapplicable rail and
why, that is refused to any consumer holding provider credentials or addressing
a subject, that is LOST the moment either appears, and that never reduces what
remains applicable. It grants no exemption and relaxes no rail; it makes an
absence auditable. Verify-list item (g) asks the honest companion question —
whether any conformant consumer is live in xFactory today or whether this is the
first — because a first consumer proposing a contract amendment should say so.

### 7.2 `governed-derived-model` — property-level, not declaration-level

Claim 23 says the thread-state header, the summaries and any future graph index
"conform to `governed-derived-model`". Read directly, that capability's
conformance surface is a DomainxFactory's `xfactory_derived_model_conformance`
declaration over template-backed object kinds, validated by the domain-factory
validator, with six dials and a `governed | calibrated` tier. An authoring
surface inside openxFactory is not a domain factory and has no place to make
that declaration.

So Phase B asserts the PROPERTIES in its own requirements — non-authoritative by
construction, full provenance on the facts a header carries, regenerable,
read-only over the truth it summarizes, promotable only by creating a new object
through review — and does **not** claim a tier it cannot be validated at.
**Flagged for Brett** as an interpretation of Claim 23, not a silent narrowing.

### 7.3 `xfactory-semantic-kernel` — a gate, not a dependency

v1 has no graph and consults no ontology package, so `Bounded semantic context`
does not bind today. Admitting a graph provider is what makes it bind, and the
delta says so: the index stays a derived projection reproducible from a pinned
package, inferred relations stay advisory, and no inference may create or widen
authority, establish approval, promote scoped data, or authorize an action. That
is `Semantic inference cannot authorize` and `Storage and reasoner neutrality`,
carried as a graduation precondition.

## 8. What stays out, and why each one is a decision

- **A graph engine, in any form** — not behind a flag, not "just a small one".
  The Mem0 v3 finding is on the record and the graduation trigger is a named
  condition. Reserving `graph_query` is how the boundary stays stable without
  building anything.
- **Headroom** — watch-listed with adoption gates recorded, and deliberately
  NOT a dependency. The verification pass found a `SECURITY.md` credential
  claim contradicted by an open PR demonstrating plaintext credential
  persistence, default-on telemetry in the OSS build, an independent
  pre-registered benchmark measuring ~5–10% per-request and net-zero run-level
  savings against a 60–95% headline, recurring prompt-cache-fidelity
  regressions (one causing a 2–7× cost increase), and — decisively for this
  design — no caller-metadata hook, so the lifecycle-status exemption could not
  live inside it even if everything else cleared. Gates: credential findings
  fixed and `SECURITY.md` truthful; telemetry default-off; prompt-cache fidelity
  stable; a sandboxed trial showing net savings on doxBench's own workload.
- **Any cloud or hosted backend as a default** — the self-hosted case is
  local-embedded, by the two-case principle.
- **Hosted-plane anything** — threads, share-session, the knowledge service and
  the bridge all inherit the local-plane rule branch sessions already carry.
- **A fourth port member** — §5.1.
- **A parallel decision store, or automatic promotion** — §4.2.
- **Retiring the outline's reserved status** — its commit is the session
  ancestry; that role is why the save order has a rule at all.
- **An external-doc claim entering contract text unverified** — standing
  practice on this topic, twice proven necessary: "SpecLock" names no real
  project, and `Mnemopi`/`artifact://`/`/shake` are oh-my-pi features an
  external review misattributed to Headroom. Every attribution in this design
  was re-checked against the upstream source or is on the verify list.

## 9. Sequencing and the archive-order hazard

Three of this change's MODIFIED requirements were ADDED by
`add-doxbench-editing-phase-a`, which is ACTIVE and unarchived, so their text
lives in Phase A's delta and not yet in the promoted spec.
`release-realization`'s ordered-deltas requirement covers exactly this: "a
proposal modifying a requirement already modified by an active ratified change
references that change and declares its deltas relative to that change's
outcome." That is what the `(relative to Phase A)` markers do.

The hazard is real and worth naming: **if Phase B archived before Phase A, the
promoted spec would carry Phase A's deferral clause ("naming the bound buffer
in a turn's durable RECORD is DEFERRED and MUST NOT be claimed") with no
requirement discharging it, and Phase B's amendments would have nothing to
amend.** Phase A's own archive gate is still open on merged-commit evidence.
So Phase B's archive is gated on Phase A having archived first, and `tasks.md`
carries that as a check rather than as an assumption.

## 10. Decisions, listed

- **D1** buffer key = path; `outline` reserved; `document` reserved for the one
  unbacked create slot — chosen so today's state is already a legal instance.
- **D2** `owned: false` documents are loadable as context; no reachable tile
  Save, no must-save marking.
- **D3** outline-first ancestry; documents independent; realization declares a
  deterministic document order.
- **D4** the tile Save is scoped to its document plus the ancestry step —
  flagged; the alternative is the whole dirty set.
- **D5** one definition of "loaded", one entry route.
- **D6** the dropdown is the overflow policy; the set is bounded and refuses
  rather than evicting.
- **D7** one selection value, three routes, all must agree.
- **D8** verbs are read / load-for-editing / save; `read` replaces `open`.
- **D9** tile marking off live state, never persisted; loaded and
  loaded-and-dirty are distinguishable.
- **D10** v1 graph-less on a recorded measurement; graduation by named trigger.
- **D11** backend is an install-time declaration.
- **D12** share-session reuses the port's existing `push`; opens no PR.
- **D13** nothing leaves the machine implicitly.
- **D14** the bridge is an adapter for the unchanged three-member port.
- **D15** additive co-resident envelope family, v1 deprecated with a removal
  target.
- **D16** no version reserved at proposal — flagged if the file's
  `contract_schema_version` must bump anyway.
- **D17** the bound buffer is carried on the wire from the DECLARED binding;
  no unreadable server-side field, no inference.
