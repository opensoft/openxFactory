# Design: add-doxbench-distilled-abstract

## Context

The requirements are in `specs/ideation-dashboard/spec.md` (three MODIFIED, seven
ADDED); the motivation and the eight rulings are in `proposal.md`; the five
council constraints this design must honour are in `clarifications.md` and are
answered by name below. What follows is the module map and the decisions behind
it.

Current state, verified on this tree:

- The docs subpane is already split — abstract region above, doc wheel below
  (`scripts/ideation_dashboard/web/views/staging-workbench.js:245-259`), with
  `renderAbstract` driven from the wheel's `onSelect`
  (`:285`), which the wheel fires on EVERY notch
  (`web/views/doc-wheel.js:205-212`) and once at mount (`:463`).
- The deterministic abstract is a pure function
  (`web/views/staging-workbench-model.js:1545-1592`) in a module that must stay
  DOM-free, I/O-free and import-free (header `:2-6`, pinned by
  `tests/ideation-dashboard/test_staging_workbench.py:798-801`).
- A real provider adapter exists: `OmpHarnessBridge`
  (`scripts/ideation_dashboard/doxbench_bridge.py:869-870`) supervises an
  `omp --mode rpc` child over stdio with no credential; its per-turn view
  `_ConversationPort` (`:1549`) is indistinguishable from the adapter to
  `dispatch_turn`.
- **But no entrypoint declares it.** Every `model_port_factory` reference is
  inside `serve.py` — parameter `:4645`, binding `:4784-4785`, class default
  `None` `:1372` — and `_workbench_model_port` returns `None` at `:1546-1547`
  whenever the factory is absent, which is every real serve: `cli.py:298` omits
  it and `serve()`'s own `build_kwargs.setdefault` block declares
  `adapter_factory` and `knowledge_declaration` only (`:4850`, `:4857`).

## Goals / Non-Goals

Realization evidence for the operator run is recorded at
`openspec/changes/add-doxbench-distilled-abstract/realization-evidence.md`.

**Goals.** One model-derived abstract per subject document, generated only when a
human asks, verified before it renders, captioned so it can never be mistaken for
the document's own account, and reachable through the seam that already exists.
Make the feature demonstrable on a real corpus.

**Non-Goals.** No snapshot field (ruling 2(b)). No second provider verb. No new
adapter. No widening of the disclosure rule (ruling 7(a)). No `Summary:` header
write — that is Option B′ in the proposal's Alternatives and stays unbuilt.

## Decisions

### D1 — A new same-origin route, not a scoped chat turn

`POST /actions/workbench/document-abstract` (name at realization), beside the
catalog and chat-turn routes, resolving the port through the EXISTING
`_workbench_model_port` accessor (`serve.py:1519-1551`) under the reused
`session` local-human verdict. Not a chat turn, because the released turn
envelope carries a bound buffer key, per-buffer observed hashes and a
buffer-keyed proposal target that an abstract request has none of, and
`dispatch_turn` would still demand a `{assistant_prose, proposals}` response from
a request that is not a conversation.

*Alternative rejected:* riding `CHAT_TURN_ROUTE` (`web/app.js:243`). Cheaper by
one route, and it would have put a non-chat consumer inside the chat contract
permanently.

### D2 — A non-chat prompt assembler and its own packet purpose

`doxbench_turns.build_abstract_envelope`, with its own section-order constant.
**No new packet purpose.** The earlier draft added
`PACKET_PURPOSE_DOCUMENT_ABSTRACT`; packet review was right that it would be dead
code — an abstract request carries NO context packet at all, so `require_valid`
never runs and the constant would be a declaration nothing reads. What replaces
it is a real pin: `build_abstract_envelope` REFUSES a `ContextPacket` handed to
it, of ANY declared purpose, because the refusal that matters is "this request
carries no packet" and not "this packet has the wrong label".
`build_prompt_envelope` (`:837`) cannot be
reused: it requires an outline plus one or more document buffers (`:880`,
refusing at `:648`), a non-blank human message (`validate_message`, `:493`), a
working subject, a transcript, and validates against the chat purpose (`:942`);
its system and response prose are chat instructions (`:239`, `:251`).

The envelope carries exactly ONE section pair — a subject header and the saved
document content — and NOTHING else: no layer-1 packet, no second buffer, no
transcript. Handing it a packet is a refusal, not a re-label. Byte-determinism comes from the same discipline as
`PromptEnvelope.rendered()` (`:476`): a fixed section order and no clock, no
counter, no set iteration in the rendered text.

### D3 — `DocumentAbstract`, a frozen sibling type with its own verifier

A new frozen dataclass in `doxbench_knowledge.py`: subject path, subject content
digest, model id, prose, `authority = NON_AUTHORITATIVE`,
`regenerable_from = "document"`. `DocumentThread` is NOT reused —
`doxbench_threads.py:593` fixes `regenerable_from` to the transcript constant and
`:619` refuses any other value, and `_refuse_lost_commitments` (`:1071-1093`)
keys on evidence refs (`:1088-1090`) and pending actions (`:1091-1093`) that a
document abstract does not have.

The verifier's base is the SNAPSHOT'S declared `topics` and `destinations` for the
subject — the same fields `documentAbstract` reads
(`staging-workbench-model.js:1565-1573`) — so it fires on generation #1. A
previous abstract is an additional base when one exists. Two rules:

1. **Subject-mention coverage** over the declared fields. Named exactly that, in
   the requirement text and in the code comments, because `dispatch_turn` returns
   one opaque string (`doxbench_model.py:985`) and nothing downstream can
   establish faithful treatment. Calling it fidelity would be this change
   committing the sin it exists to prevent.
2. **The path rule** — name the subject's path or title; name NO repository path
   the request did not carry. This is the one clause decidable from the response
   bytes, and it refuses both the wrong-document answer and the leaked-neighbour
   answer, which is what discharges the injection-leak case.

*Alternative rejected:* a structured coverage field parsed out of the response.
Stronger, and it needs a declared response schema, a parser, and its own refusal
code — a bigger change than this one. Named in the requirement as the follow-on.

*Alternative rejected:* full `governed-derived-model` conformance (ruling 4(b)).
The right instrument for a domain factory declaring a derived-model FAMILY; here
it would declare a family whose only member is one pane's string.

### D4 — Layer 2 gains a SIBLING, never a second owner

`CompressionLayer.owner` is a one-owner field (`doxbench_packet.py:224-229`) and
`assert_fidelity` keys on layer NUMBER (`:255-267`), so a comma-joined second
owner would degrade the checker to a comment. `layer(2).owner` stays
`"doxbench_threads.compact_thread"` and the equality pin at
`test_doxbench_packet.py:920-921` stays green UNCHANGED — asserted, not assumed.
The sibling class is declared in the spec and carried in code as the
`DocumentAbstract` type's own verifier.

### D5 — A separate, digest-and-model-keyed, bounded store with an explicit-refresh bypass (honours N1)

NOT the chat `TurnStore` instance. There is one per served process
(`serve.py:4796`) bounded at `MAX_IDEMPOTENCY_ENTRIES = 64` and
`MAX_IDEMPOTENCY_BYTES = 16 MB` (`doxbench_turns.py:998-999`), and abstract churn
would evict chat idempotency records — a 200-document scope exceeds a 64-entry
bound threefold, so eviction is the ORDINARY case here, not the edge.

A separate store with the same SHAPE (`doxbench_turns.py:1033-1069`): one
in-flight per key with attach-and-wait (which is the "regenerating" state, so
ruling 3(b) needs no new machinery), identical-key replay without a second
dispatch, deterministic non-clock eviction. **The key is
`(repository, ref, subject path, content digest, resolved model id)`** — five
facts, and two dated corrections put the last of them there. The digest MUST be
IN the key, because that store refuses a different digest under the same key as
a conflict, so a path-only key would hard-refuse every regeneration after every
edit. The RESOLVED MODEL ID must be in the key for the mirror-image reason: a
human can change the selected model while the document stands still, and on a
key without it that second request is IDENTICAL, so the first model's prose
would replay while `DocumentAbstract.model_id` (D3) records the model the reader
just picked. An artifact that names a model which did not answer is exactly the
kind of confident false claim this change exists to prevent, and the provider
boundary's "every consumer resolves a catalog model id" rule forbids it besides.
For an `auto` routing entry the key carries the RESOLVED id, not the rule's id —
same reason a turn records the model that actually answered. Re-dispatch after
eviction is specified expected behaviour, not an error.

**Corrected 2026-08-25 (adversarial review, S3): the SCOPE is in the key too.**
This section said `(subject path, content digest)` and the first realization
built exactly that, while the store is a single per-served-process dict and one
process resolves every repository its registry knows and every ref of each.
`ideation/staging/<topic>/README.md` exists in most of them, so two scopes
holding identical bytes at one path shared a cache entry — and `latest_for_path`
handed repository A's abstract to repository B as its PREVIOUS VERIFICATION
BASE.

**Corrected 2026-08-25 (packet review, Codex on PR #352): the RESOLVED MODEL ID
is in the key too**, for the reason two paragraphs up. THE TWO CORRECTIONS MAKE
ONE KEY, and they do not compete: the ratified requirement composes the key from
the three facts that can vary WITHIN one scope — path, digest, resolved model id
— and the scope qualification is this store's TENANCY boundary rather than a
fourth fact about the question. Adding it can only ever split a bucket and never
merge two, so every sentence the requirement says about the three still holds
exactly. `AbstractKey` therefore carries `repository`, `ref`, `subject_path`,
`content_digest`, `resolved_model_id` — five fields, not a composed string, so
injectivity is by construction. `latest_for_path` stays a per-`(scope, path)`
question ACROSS models, because it answers "what abstract does this document
already have", which the verification requirement takes as an ADDITIONAL base:
an answer from another model is still a previous answer about THIS document, and
the requirement says nothing that would narrow it to one model.

**Explicit refresh is a THIRD request mode, not a fourth store.** Replay on an
identical key and a working RE-GENERATE control are in direct conflict: a
regeneration against unchanged content and an unchanged model has an identical
key by construction, so plain replay makes the control inert except by the
accident of eviction. The request therefore carries a REFRESH INTENT flag —
realized 2026-08-25 as the request's own optional boolean `refresh`, inside the
same CLOSED shape, so an unknown key is still refused and an absent one still
means "no intent". Set, it invalidates the completed entry for its key,
dispatches, and replaces the entry. Unset — which is every selection, mount, and
tile re-entry — it replays. The in-flight arm is UNCONDITIONAL in both modes: a
refresh arriving while a generation is in flight for the same key attaches
rather than dispatching, so an impatient double-click costs one model call. That
is one boolean on the request and no change to the store's shape.

*Alternative rejected:* a nonce or attempt counter in the key. It works, and it
also makes every regeneration a permanent new entry, so N regenerations of one
document hold N slots in a bounded store and evict N-1 useful neighbours to keep
answers nobody asked for. Invalidate-and-replace keeps one live entry per real
(subject, digest, model).

*And the invalidated entry is not simply dropped* (2026-08-25 realization): the
lease hands its `DocumentAbstract` back to the route as that generation's
PREVIOUS verification base. The verification requirement makes a previously
generated abstract an ADDITIONAL base "where one exists", and RE-GENERATE is the
one path where one always exists — invalidating it out of the replay index and
out of the verifier's reach at the same moment would have made the regenerate
path verify against a strictly weaker base than every other path.

### D5a — The abstract binds its OWN conversation (2026-08-25, review B1)

`OmpHarnessBridge.dispatch` is `_dispatch_bound(None, …)`: it REFUSES an unbound
turn on a fresh process and, once any turn has bound a session, runs inside
whichever conversation the harness was last switched to. The first realization
handed the RAW port to `_deadline_bound_dispatch`, so on a real install the
first generation of a session could only fail, and every generation after a chat
turn would have been prompted INSIDE that document's chat session — against
`spec.md`'s one-session-per-document-thread rule and against this route's own
envelope contract, whose whole claim is that the model was shown ONE subject and
no other material.

The route therefore binds through `port.for_conversation(...)` — duck-typed
exactly as `dispatch` is — under a key of its own:
`serve.py:doxbench_abstract_conversation_key`, JSON-composed as
`["doxbench-abstract", repository, ref, tile_kind, tile_id, subject_path]`. Its
own KIND, never `doxbench_bridge.CONVERSATION_KEY_KIND`: reusing the document
thread's key would fix the refusal and keep the contamination, in the other
direction. A binding failure is refused with the route's fixed, redacted
`model_failed` and nothing is dispatched.

THE COST, stated: one harness session per (scope, document) abstract
conversation, and the bridge starts a fresh child per new thread
(`doxbench_bridge.py`'s recorded RPC-surface tradeoff). A per-TILE abstract
conversation would be cheaper and would put document A's abstract in document
B's context, which is the contract this route sells.

### D6 — The interaction: explicit invocation and a subject recheck at paint

`renderAbstract` stays wired to the wheel's `onSelect` for the DETERMINISTIC
abstract, which is pure and free. Generation is a separate explicit control on
the centred tile — never `onSelect`, which fires on every notch and at mount.
The response echoes the subject path and digest it was generated for; on resolve,
if the pane's current subject differs, the result is discarded UNRENDERED. Without
that check a slow answer paints itself over whatever the reader has since spun
to, under a confident caption.

The in-flight state is cancellable and states the ADAPTER'S OWN declared bound —
`port.timeout_seconds`, which the chat path already reads through
`validated_timeout_seconds` (`serve.py:3416-3417`) and which the bridge defaults
to `60.0` (`doxbench_bridge.py:881`). `MAX_ADAPTER_TIMEOUT_SECONDS = 120`
(`doxbench_model.py:54`) is the validated CEILING, not a prediction, and a region
that showed 120s while the adapter declared 60s would be lying in the safe
direction and still lying. The subject is the
SAVED file; a dirty loaded buffer is captioned as describing the saved version
and its unsaved text never leaves the browser.

### D7 — Subject eligibility (ruling 7(a))

The subject is drawn from `projection.editable_paths`. The standing rule is
`doxbench_scope.py:390` — "disclosure requires edit authority, which is the rule,
not an accident" — enforced at `doxbench_turns.py:585-591` and documented as
"always refused before any disclosure" (`:612-613`). `editable_paths` is fed only
from sections flagged `owned` (`:356-358`) and exactly ONE section carries that
flag (`:35-42`, `"owned": True` at `:41`), so on a cluster or possible tile the
eligible set is EMPTY and the region says so. Widening to `context_paths` is
ruling 7(b), a named follow-on with its own delta — not an implementation choice
made inside a UI pull request.

### D8 — Renderer surface

- **`web/app.js`**: ONE new fetch call site. The pin at
  `tests/ideation-dashboard/test_renderer.py:152` goes 5 → 6, declared by name in
  the `:129-133` docstring the way the thread-read route was.
  `staging-workbench.js` gains no fetch.
- **`web/views/staging-workbench-model.js`**: a PURE formatter for the
  model-derived abstract beside `documentAbstract` (`:1545`) — no DOM, no I/O, no
  imports; the transport stays in `app.js` and the wiring in
  `staging-workbench.js`.
- **`web/views/staging-workbench.js`**: the toggle between the two abstract
  STATES inside ONE region (deterministic first — the upper half is a measured
  280px, `test_doxbench_context_panes.py:231-240`), the generation and
  re-generate controls, the in-flight and stale states, and ruling 6's region
  rename.
- **Accessibility — ONE region, a composed name.** Packet review settled the
  one-region-or-two question: EXACTLY ONE `role=region`, whose accessible name is
  composed of the SUBJECT's title/path plus the provenance caption of the state
  shown, so the deterministic and model-derived states are distinguishable BY
  NAME and a reader knows which document they landed on. Two regions would have
  meant two names for one 280px box and a second thing to keep in sync. The house
  idiom at `test_doxbench_accessibility.py:281-311` stays satisfied —
  `role=region` named by `aria-label`, no heading of its own, exact casing — and
  this is where the static `"selected document"` at
  `staging-workbench.js:250` is replaced, since that name belongs to the
  loaded-document selector. **This change owns `:250`**: the split change cut the
  rename precisely because it needs code.

### D9 — Wire the adapter at the REAL entrypoint, once per process

Three corrections from packet review, all verified:

**The entrypoint is `cli.py`, not `serve()`.** `serve()` (`serve.py:4833`) has NO
CALLERS — grep confirms it. The real entrypoint is
`cli.py:298`'s `serve_mod.build_server(...)`, which already makes its own
install-time declarations there: `adapter_factory=serve_mod.real_notebook_adapter`
(`:304`) and `knowledge_declaration=knowledge_mod.SELF_HOSTED_LOCAL_EMBEDDED`
(`:311-312`). `model_port_factory` is declared BESIDE those two, for the reason
those comments already give: an operator must be able to read what their install
talks to. `serve()`'s `build_kwargs.setdefault` block (`:4850`, `:4857`) gets the
same declaration as the standalone secondary path, so the two do not drift.

*Test-safe, verified:* every existing test injects `model_port_factory` into
`build_server` directly, including the two absence pins
(`test_doxbench_request_handling.py:696`, `:727`), so declaring at the entrypoint
leaves those `None` and they keep passing.

**The factory takes no arguments, and `OmpHarnessBridge` cannot be built bare.**
`_workbench_model_port` calls `self.model_port_factory()` with NO args
(`serve.py:1549`), while `OmpHarnessBridge.__init__`
(`doxbench_bridge.py:879-886`) has a keyword-only `session_root` with NO DEFAULT
— unconstructible bare — and `catalog` defaulting to `EMPTY_CATALOG`
(`doxbench_model.py:719`), which is an INERT adapter: it would resolve, disclose
nothing, and look like a working install. So the declaration must supply all
three, at install time, in the idiom `knowledge_declaration` already uses:

- **catalog** — a declaration constant/module beside the knowledge declaration,
  not a per-turn parameter.
- **session_root** — a CLI flag on the entrypoint, defaulted next to the other
  path arguments.
- **`LaunchConfig`** — `provider_id` and `command`, the shape the live fixture
  already builds (`tests/ideation-dashboard/test_doxbench_bridge_live.py:145-146`).

Nothing here becomes a per-request or per-turn input. The port stays a
zero-argument factory; the factory is what closes over the declaration.

**One instance per process, not one per request.** `_workbench_model_port` is
called per request (`serve.py:2162`, `:2700`) and `OmpHarnessBridge` is STATEFUL
— `_sessions` and `_selected` at `doxbench_bridge.py:900-901`. Constructing per
request would break `spec.md:1991`'s "ONE harness session SHALL correspond to one
document thread" BY CONSTRUCTION, and would restart a supervised child on every
call. So the entrypoint builds the bridge ONCE and the factory returns that same
instance; the delta pins it with a same-object-identity scenario across two
requests.

Also correct two stale statements NOW, not "with the first call site" — a real
`dispatch` call site already exists at `serve.py:3422`, so both are false today:
the banner at `serve.py:2128-2134` ("no code below calls it") and
`_workbench_model_port`'s own docstring at `:1542-1544` ("no route below calls
it ... the dispatch arm is T051's").

Hermeticity: `tests/hermeticity.py` guards `nlm` and `gh` (`GUARDED_BINARIES` at
`:91`) and NOT `omp`. Adding `omp` has two knock-on effects that must be handled
in the same task, because both iterate the tuple:
`tests/ideation-dashboard/test_hermeticity.py:63` and `:75` parametrize over
`GUARDED_BINARIES`, and `tests/notebooklm/test_hermeticity_guard.py:43` loops it.
The refusal is also stamped `MARKER = "FR-043"` (`tests/hermeticity.py:95`) — a
NotebookLM requirement id, which would mislabel an `omp` refusal. Either
generalize the marker or document the mislabel explicitly; do not leave a
refusal citing the wrong requirement.

### D10 — The captioning pin moves onto the node harness (honours N5)

The current guard (`test_doxbench_context_panes.py:144-152`) is a whole-file
substring sweep, and after this change both captions live in one file, so it
cannot distinguish them. It is also weaker than it reads: it bans `distilled` but
not `distillation`. It moves onto the harness fixture (`:83-94`), which already
runs the model in node and returns JSON, asserting a CAPTION FIELD per abstract:
the deterministic one must not claim a distillation, the model-derived one must
claim model-derived / non-authoritative / regenerable.

Verifier tests seed their own `dispatch_result` — `FakeWorkbenchModelPort.dispatch`
returns a constant (`doxbench_model.py:1101`), so the default fake proves only
that the happy path does not crash. Prompt-side rules are checked through
`port.dispatched`, which needs no model at all and should carry the weight the
response-side tests cannot.

## Risks / Trade-offs

- **The feature is invisible until D9 lands** → wire the entrypoint in the same
  slice, and make one real-adapter operator run part of the realization gate. A
  green suite against a constant-returning fake is not evidence.
- **Two consoles at one (repository, ref) may show different abstracts** (the
  ruling 2(b) mirror, and where **N4** lands: the hosted plane's real problem was
  determinism, not caption wording) → accepted and recorded. A divergence two humans can see
  beats a snapshot field that silently breaks the projection contract.
- **`editable_paths` is empty on cluster and possible tiles** → the region states
  it. Visible, honest, and the cost of not relaxing a disclosure rule as a side
  effect of a UI change.
- **The abstract is terminal — no route from a good abstract to a better
  document** (N2) → stated as a deliberate boundary, with the attachment point
  named: a future "propose this as `Summary:`" verb rides the existing chat
  proposal → Apply → gate path (Option B′). Nothing in this slice writes a
  `Summary:` header.
- **Prompt injection: the subject document is the whole instruction-bearing
  text** → one subject only, no layer-1 packet, a tightened output bound, and the
  path rule that refuses any output naming a document the request did not carry.
  `_buffer_section` (`doxbench_turns.py:821-825`) frames content with a `Path:`
  header and a `---` rule; that is a LABEL, not a boundary, and the design does
  not pretend otherwise.
- **Subject-mention coverage is weaker than it sounds** → named honestly in the
  requirement and in code. The structured-coverage follow-on is recorded rather
  than implied.

## Migration Plan

Nothing to migrate: no schema, no contract bundle (ruling 2(b) →
`target_release: none`), no stored artifact, no snapshot field. Rollback is
removing the route and the control; the deterministic abstract is untouched and
remains the default view, so the pane degrades to exactly today's behaviour.

## Open Questions

1. **Ruling 7(b)** — widening the subject set to `context_paths` for read-only
   single-document derivation. Named in the spec as the follow-on; needs its own
   delta and Brett's ruling.
2. **Structured coverage** — a declared response shape with a parser and its own
   refusal code, replacing subject-mention coverage. Deliberately not taken here.
3. **Human-reviewable, discharged** — layer 2's adjective is inherited as an open
   obligation. What act would actually discharge it is unanswered, and
   "rendered before a copy affordance" was rejected as theatre.
4. **Prioritization** (N3) — the operator's still-open list carries a P1
   (unforwarded per-key storage; a reload destroys unsaved buffers) and four P2s
   ahead of these annotations. This change should not be scheduled ahead of them
   without Brett's say; the split change has no such constraint, since it removes
   a falsified requirement and adds no surface.
