---
code_surface: openxFactory (the doxBench docs subpane's abstract region, its pure view-model, and the explicit human control that invokes generation; a model-derived per-document abstract behind the existing server-side `WorkbenchModelPort` seam, reached by ONE new same-origin route and ONE new `app.js` call site; a NON-CHAT prompt assembler — `doxbench_turns.build_abstract_envelope` with its own section-order constant, plus a second `PACKET_PURPOSE_*` in `doxbench_packet.py`, because the existing assembler is chat-shaped; a new frozen `DocumentAbstract` type with its own document-shaped verifier; the layer-2-class SIBLING-ARTIFACT declaration; the subject-eligibility rule read off `doxbench_scope.py`/`doxbench_turns.py`; an entrypoint declaration binding `OmpHarnessBridge` as `model_port_factory`, which no entrypoint does today; `omp` added to test hermeticity's guarded binaries; the captioning vocabulary and its relocated test pin; conditionally the snapshot schema and generator)
target_release: none — RULED 2(b), session-only. No contract bundle is cut. `none` does NOT mean doc-only: `code_surface` is non-empty, so the archive gate stays merge-plus-green plus the operator run named in Impact (`release-realization/spec.md:23-32`)
Status: ratified
Ratified: Brett, 2026-08-25 — all eight rulings taken as recommended, recorded as a comment on `opensoft/openxFactory#84`
---

# Proposal: add-doxbench-distilled-abstract

Closes the derivation half of `opensoft/openxFactory#84` — "doxBench R-8 (V2
family): lens subtabs + docs subpane wheel split with distilled abstracts".

## Ratified

Brett ruled every recommendation as written on 2026-08-25, recorded as a comment
on `#84`. One line per ruling:

- **0 — SPLIT.** The doc-only half is now
  `ratify-doxbench-landed-context-surfaces`, ratified the same day. **BREAKING #2
  and every Group B item moved THERE**; this change's deltas are authored
  RELATIVE TO ITS OUTCOME (`release-realization/spec.md:64-74`).
- **1 — (c)** on-demand through the existing server-side port seam, with a
  digest-keyed cache.
- **1(c)(i) — a NEW same-origin route**, not a scoped chat turn. The `app.js`
  fetch pin widens 5 → 6, declared by name.
- **2 — (b) session-only.** `target_release: none`. 2(a) is WITHDRAWN as an
  evolution and re-declared as a separate future change that must first amend
  `spec.md:7`'s byte-identical scenario.
- **3 — stale-shown-and-labelled, with a regenerating state in flight.** For an
  unloaded subject the digest is the served SAVED content's digest.
- **4 — the `compact_thread` DISCIPLINE in a new `DocumentAbstract` type**,
  declared a layer-2-class SIBLING artifact; base = the snapshot's declared
  topics and destinations; the check named honestly as subject-mention coverage;
  plus the subject-path rule.
- **5 — the five captions**, each with its declared accessibility carrier.
- **6 — the abstract follows the WHEEL TILE**, and the region is renamed so the
  selector keeps sole claim on the selected buffer's name.
- **7 — (a) `editable_paths` now**, with (b) — widening to `context_paths` by an
  explicit delta — named as the follow-on ruling rather than taken silently.

Spec deltas are now authored: `specs/ideation-dashboard/spec.md` carries three
MODIFIED requirements and seven ADDED. `clarifications.md` carries the five
council constraints the design honours.

**Disambiguation, first, because the issue title invites exactly one misreading.**
"V2 family" in #84 and in the codexFactory T100 residual register means a SECOND
VERSION OF THE DOXBENCH FEATURE — the FEATURE line the register handed over, as
distinct from the defect line. It does NOT mean the chat-turn envelope family
`request_v2` / `success_v2` at
`contracts/schemas/xfactory-workbench-chat-turn.schema.yaml:346` and `:390`.
Nothing in this change touches that envelope.

Requirement citations below are BODY lines, not heading lines, so the quoted
sentence is at the line named.

## Why

### The first reversal: a ruling about honesty, reversed honestly

On 2026-08-03 Brett scoped the docs-subpane abstract to "header + structure,
honestly labelled" — the facts the snapshot already indexes — and ruled that it
"is NOT an AI distillation, and nothing built from it may caption it as one; a
surface that claims an analysis nobody ran is worse than one that shows less"
(`scripts/ideation_dashboard/web/views/staging-workbench-model.js:1530-1544`).
That ruling was pinned as a test, not a comment:
`tests/ideation-dashboard/test_doxbench_context_panes.py:144-152` reads the shell
source and fails if `distilled`, `ai summary`, or `ai-generated` appears anywhere
in it (the tuple is at `:150`), and the module docstring restates the scope at
`:26-29`. On 2026-08-25 Brett ruled option C: build the REAL per-document
distilled abstract, produced by a model.

The 08-03 ruling was right for what shipped and is wrong for what #84 asked for.
It was a scope ruling made against a surface with no derivation story — and the
issue said so at the time: "the abstract is new derived content ... so it needs
its own derivation/generation story, not just UI" (#84 body). What shipped
honoured the ruling exactly. `documentAbstract`
(`staging-workbench-model.js:1545-1592`) is pure, reads one document object,
touches no DOM and fetches nothing; it re-presents the document's own `Summary:`
header, its declared `Topics:`, `stage`/`kind`, where it lands, and the five
completeness signals beside their score. The only per-document summary text
anywhere in the system is that header, lifted verbatim by the generator at
`scripts/ideation_dashboard/generator.py:424` (`_header_value(d.text, "Summary")`)
and declared at `contracts/schemas/ideation-dashboard-snapshot.schema.yaml:148`.
A document whose author wrote no `Summary:` header therefore has no summary at
all, and the pane says so in words rather than showing an empty box
(`staging-workbench-model.js:1575-1581`). That honest absence is the current
state of the art, and it is the thing option C replaces.

### The second reversal, found while grounding the first

Both UI halves of #84 are shipped, and one of them CONTRADICTS a ratified
requirement. `spec.md:439` requires the bullseye "at TILE SCOPE, above the
always-present flat matrix", and its scenario at `:441-444` requires that "the
flat matrix MUST still render, as the always-available view of the same
membership" — with the requirement text stating outright that the matrix "MUST
NOT become a toggle-only alternate". The shipped subtabs make bullseye and
matrix MUTUALLY EXCLUSIVE tabpanels: `staging-workbench.js:488` sets
`subPanes.get(name).hidden = !on;` inside `showSection`, so exactly one of the
three sections is visible at a time. The restructure Brett annotated
(`vibe_1785602062606_397p8iakz`, quoted at `staging-workbench.js:443`) is
architecturally a toggle, and the ratified text forbids exactly that.

This is a SECOND breaking reversal and it is owned here rather than left as an
undeclared divergence, because the alternative is a ratified requirement that
the code has quietly falsified since 2026-08-03. The annotation is the newer
instruction and the panel is genuinely more readable in three subtabs; what the
requirement was protecting was ACCESS to the matrix, not simultaneity. Proposed
replacement wording is in the Modified Capabilities inventory below.

The nit, corrected: `:439` is the earlier and NARROWER statement of the
no-new-analysis constraint, and `:864` (doxBench scoped view) restates it at
the wider scope — not the other way round.

### Three landed surfaces, zero requirement text

The lens is in three subtabs (`staging-workbench.js:443-506`); the docs subpane
is split with the abstract above and the doc wheel below
(`staging-workbench.js:245-259`, annotation `vibe_1785602331813_gvku9sh2s` at
`:245`), the wheel being the deck's own drum at its own 0.4 radius
(`web/views/doc-wheel.js:32-50`). Grep `openspec/specs/ideation-dashboard/spec.md`
for `abstract` or `subtab` and it returns nothing: three landed surfaces with no
requirement text between them, one of them contradicting a requirement that
does not know it exists. Building a derivation on top of that would deepen the
gap, so this change promotes all three to spec text in the same delta.

### The guards the reversal must pass through, not around

The docs region SHALL render each row's completeness bar and named signals
VERBATIM from the snapshot, "never recomputing them", and the lens MUST NOT
introduce "a new analysis, a new score, or a new snapshot field"
(`spec.md:864`, narrower at `:439`). The dashboard is a generated projection and
never a source of truth, byte-identical for an unchanged tree (`spec.md:7`;
determinism pinned at `ideation-dashboard-snapshot.schema.yaml:17-21`, additive
growth at `:23-28`). Every artifact any compression layer produces "SHALL be
non-authoritative and regenerable, and MUST NOT become truth by being
compressed, cached, or offloaded" (`spec.md:1971`, with the scenario "A
compressed artifact is cited as truth" at `:1986`). And the model catalog and
turn routes "SHALL be offered only on a loopback human console with a real
checkout, resolved actor, and demonstrated console presence; the hosted/read-only
plane MUST offer neither route" (`spec.md:1046`).

A model-written abstract is a new analysis by any reading. The question this
proposal puts to review is not whether to weaken those guards — it is which
EXISTING frame the new content enters under, so the guard it trips becomes a
requirement it satisfies.

There is precedent for new derived content the guards accept: the
per-staged-topic health aggregate is computed at generation time, emitted as an
additive field, and required to be "deterministic and reproducible from the
pinned tree alone" (`spec.md:357`). That is the shape a DETERMINISTIC derivation
takes. A model's output cannot claim it, which is precisely why the frame
matters.

### Who this is for, and what they actually get

The reader is a human moving through a scope's staged ideation documents in the
docs pane, deciding which one to open. Measured on this repository's own corpus
today: **46 documents under `ideation/staging/`, 34 of them carrying a
`^Summary:` header and 12 not — 26% with no summary at all.** For those 12 the
deterministic abstract can only say the document is uncatalogued, so the delta
is total. For the other 34 the delta is narrower and needs stating honestly: the
declared `Summary:` header already exists, so a model-derived abstract earns its
place only where it says something the header does not. The highest-value case
is the one nobody can currently see — a document whose declared `Summary:`
DISAGREES with its body, which today reads as a confident one-liner over
material that has moved past it.

And one sober fact about scale: until a real adapter is wired at an entrypoint
(see the Impact section's real blocker), the caption most readers see is the
not-yet-generated one.

### Alternatives considered

**Option B′ — the model proposes the document's own `Summary:` header.** Instead
of a new read-only artifact, the model drafts a better `Summary:` and offers it
through the path that already exists end to end: a chat turn, a typed proposal,
Apply into the buffer, and Save through a gate verb. That route improves EVERY
plane forever — the snapshot's `summary` field
(`generator.py:424`), the deterministic abstract, the hosted read-only plane,
every future consumer — with no new route, no new type, no new caption
vocabulary, and no reversal of the 08-03 ruling. It is strictly cheaper and
strictly more durable, and it is recorded here because a proposal that hides its
cheaper alternative is not giving review a real choice.

Option C was ruled anyway, and this proposal does not reopen that: Brett ruled
it on 2026-08-25, and the two are not the same product. B′ edits the source and
therefore needs a human at a gate for every document; C is read-only derived
content that never touches the source, which is what makes it usable while
BROWSING dozens of documents. The honest statement is that C is the browsing
surface and B′ is the fixing surface, and B′ remains available afterwards.

## What Changes

- **doxBench gains a real per-document distilled abstract, produced by a
  model** — the plain reading of annotation `vibe_1785602331813_gvku9sh2s`
  ("the doc slected distilled summary abstract ... an abstract that surfaces the
  key items delivered by doc"), which the 08-03 scope ruling deferred.
- **BREAKING (governance) #1: the 2026-08-03 honest-labelling ruling is
  reversed** for this surface. The pin is RELOCATED, not deleted — and its
  current form could not survive the change anyway. `test_the_abstract_is_never_captioned_as_a_distillation`
  (`test_doxbench_context_panes.py:144-152`) is a WHOLE-FILE substring sweep, and
  after this change both captions live in the same file, so a file-level
  assertion cannot distinguish "the model-derived abstract says distilled" from
  "the deterministic one does". It is also already weaker than it reads: it bans
  `distilled` but not `distillation`, and `distilled` is not a substring of
  `distillation` — three of the five proposed captions would not trip it. The pin
  moves onto the Node harness (`test_doxbench_context_panes.py:83-94`), which
  already executes the model in node and returns JSON, and asserts a CAPTION
  FIELD per abstract object: the deterministic one must not claim a
  distillation, and the model-derived one must claim exactly the
  model-derived / non-authoritative / regenerable posture.
- **BREAKING (governance) #2 MOVED.** `spec.md:439`'s "MUST NOT become a
  toggle-only alternate" clause, which the shipped subtabs falsified, is
  replaced by `ratify-doxbench-landed-context-surfaces` under ruling 0. The
  argument is unchanged and is recorded there; this change neither restates it
  nor depends on it beyond authoring its own `:863` delta against the text that
  change lands.
- **The deterministic abstract survives** as its own thing. `documentAbstract`
  (`staging-workbench-model.js:1545-1592`) is not replaced; the two are
  separately labelled, because "what the document declares about itself" and
  "what a model read out of it" are different claims and a pane that merged
  them would be unreadable. It also stays the DEFAULT: it is the one that exists
  before any model runs.
- **The abstract is a LAYER-2-CLASS SIBLING ARTIFACT, not a second owner of
  layer 2.** The tempting move — widen `layer(2).owner` to name two functions —
  is refused here: `CompressionLayer.owner` is a ONE-OWNER field
  (`doxbench_packet.py:224-229`), and a comma-joined string in it degrades the
  checker to a comment while `assert_fidelity`
  (`doxbench_packet.py:255-267`) still keys on layer NUMBER and cannot tell the
  two artifacts apart anyway. Layer 2 as specified is compaction "into the
  thread-state header... preserving commitments and discarding narrative"
  (`spec.md:1971`) — and a document abstract does NEITHER of those things. So the
  abstract is declared a SIBLING at layer 2's fidelity CLASS (lossy-by-design),
  governed by `:1971`'s universal final clause — "Every artifact any layer
  produces SHALL be non-authoritative and regenerable, and MUST NOT become truth
  by being compressed, cached, or offloaded" — and by its scenario at `:1986`,
  with its OWN document-shaped verifier rather than `compact_thread`'s. Layer 2's
  `owner`, its `note`, and the equality pin at
  `test_doxbench_packet.py:920-921` are all left untouched. Layer 2's
  "human-reviewable" adjective is INHERITED BUT NOT DISCHARGED in this slice, and
  the proposal says so rather than claiming it: rendering an abstract in a pane
  is presentation, not review, and the only thing that would discharge it is a
  human act this slice does not define. Requiring "rendered before any copy
  affordance" was considered and rejected as theatre — it would let a scroll past
  a region count as review.
- **The abstract is a NEW frozen type, because `compact_thread`'s shape does not
  transfer literally.** `DocumentThread` (`doxbench_threads.py:577`) fixes
  `regenerable_from: str = REGENERABLE_FROM_TRANSCRIPT` (`:593`) and refuses any
  other value at construction (`:619`) — "no other origin is a thread state
  header" — and `_refuse_lost_commitments` (`:1071-1093`) keys on commitment
  classes a document abstract does not have, including evidence refs (`:1088-1090`)
  and pending actions (`:1091-1093`). So this change declares
  **`DocumentAbstract`**: frozen, `authority = NON_AUTHORITATIVE`,
  `regenerable_from = "document"`. `compact_thread`'s DISCIPLINE transfers
  (`doxbench_threads.py:1096-1122`: "summarizing is a model's job and verifying
  is this module's" — output passed IN, verified here, refused on loss,
  non-authoritative by construction); its TYPE does not.
- **The verifier's rule, stated so it can actually fire.** Four things the
  earlier draft got wrong and this one fixes:
  **(i) The comparison BASE is the document's own snapshot-declared fields** —
  the `topics` and `destinations` that `documentAbstract` already reads
  (`staging-workbench-model.js:1565-1573`) — NOT the previous abstract. Keying
  only on a previous abstract would leave generation #1 unverifiable, which is
  the generation that matters. A previous abstract, where one exists, is an
  ADDITIONAL base.
  **(ii) The check is SUBJECT-MENTION COVERAGE, not fidelity, and the
  requirement text says so.** `dispatch_turn` returns `assistant_prose` as ONE
  STRING (`doxbench_model.py:985`), so nothing downstream can verify that a
  declared topic was treated FAITHFULLY — only that it was MENTIONED. Calling
  that fidelity would be this proposal committing the exact sin it is written to
  prevent. If review wants a real structural check, the follow-on is a declared
  coverage field with a named parser and its own refusal code, and that is a
  bigger change than this one.
  **(iii) One fidelity clause the rule CAN test:** the abstract MUST name the
  subject document's path or title, and MUST NOT name any repository path absent
  from its own request. That single clause catches both failures that matter —
  output about the WRONG document, and output that leaked a NEIGHBOUR's material
  — and it is decidable from the response bytes alone.
  **(iv) The verifier needs hand-written RED cases.**
  `FakeWorkbenchModelPort.dispatch` returns a CONSTANT
  (`doxbench_model.py:1101`: `{"assistant_prose": "fake grounded answer",
  "proposals": []}`), so no verifier test gets meaningful coverage from the
  default fake — each needs a seeded `dispatch_result`. What IS falsifiable
  cheaply is the PROMPT: `port.dispatched` records every envelope handed over,
  so the one-subject-only rule below is testable without a model.
- **The three landed surfaces are promoted to spec text**: the lens's three
  subtabs, the docs subpane's abstract-above/wheel-below split, and the
  deterministic abstract's derivation and honest-absence behaviour.
- **The model is reached SERVER-SIDE, through the existing seam, by one new
  route.** `WorkbenchModelPort` (`doxbench_model.py:791`) is resolved per
  request by `serve.py:1519-1551` (`_workbench_model_port`), gated on the reused
  `session` local-human verdict — loopback plus real checkout plus resolved
  actor — and injected by `model_port_factory` (`serve.py:4645`, bound at
  `:4784`). The browser holds two model routes only (`web/app.js:242-243`:
  `CATALOG_ROUTE`, `CHAT_TURN_ROUTE`) and no credential;
  `gate_routes.py` contains no model-port reference at all (its three
  case-insensitive `model` matches are `data-model` prose at `:1128` and `:1838`
  and a filename at `:1668`). Any abstract generation therefore reaches the port
  from `serve.py`, not from a gate verb and not from a view module.
- **Dispatch obeys `dispatch_turn`'s contract.** `dispatch_turn`
  (`doxbench_model.py:924`) takes `(port, prompt_envelope, *, entry, clock,
  proposal_validator=None)`, raises `TypeError` unless `entry` is a
  `ModelCatalogEntry` (`:955`), requires an injected `clock`, and accepts ONLY a
  dict whose key set is exactly `{"assistant_prose", "proposals"}` (`:985`) —
  anything else is `response_invalid`. So the abstract arrives as
  `assistant_prose` with an empty `proposals` list, and the verification that it
  is a well-formed abstract happens on this side of the seam, in the
  `DocumentAbstract` constructor. The three-member port surface does NOT widen.
- **A NON-CHAT prompt assembler is needed, and this is new surface the earlier
  draft missed.** `dispatch_turn` is correctly OPAQUE to the envelope — it just
  hands it over (`doxbench_model.py:972`) — but the thing that BUILDS envelopes,
  `build_prompt_envelope` (`doxbench_turns.py:837`), is chat-shaped throughout:
  it demands exactly one outline plus one or more document buffers
  (`:880`, refusing otherwise at `:648`), requires a non-blank human message
  (`validate_message`, `:493`), requires a working subject and a transcript, and
  validates its packet against `purpose=PACKET_PURPOSE_CHAT_TURN` (`:942`) —
  which is the ONLY purpose constant that exists (`doxbench_packet.py:308`, used
  at `:1154`). Its system and response prose are chat instructions in so many
  words (`SYSTEM_CONTRACT_TEXT` at `doxbench_turns.py:239`,
  `RESPONSE_INSTRUCTION_TEXT` at `:251`). An abstract request has no human
  message, no transcript, no outline and no proposal, so it needs
  `build_abstract_envelope` with its own section-order constant and a SECOND
  `PACKET_PURPOSE_*`. **Requirement + scenario:** the abstract prompt SHALL be
  byte-identical for identical construction input, mirroring
  `PromptEnvelope.rendered()` (`doxbench_turns.py:476`) — *WHEN the same subject
  document, digest and model are assembled twice THEN the rendered envelope bytes
  MUST be identical.*
- **Prompt injection is a bounded obligation here, not an out-of-scope note.**
  With no human message, the SUBJECT DOCUMENT'S CONTENT is the entire
  instruction-bearing text in the prompt, and `_buffer_section`
  (`doxbench_turns.py:821-825`) frames content with a `Path:`/working-state
  header and a `---` rule — a LABEL, not an injection boundary. So: the abstract
  request MUST carry EXACTLY ONE subject document's content, and MUST NOT include
  the layer-1 context packet or any other buffer — which also keeps it away from
  the indexed corpus bound (`MAX_INDEXED_SOURCES = 200`, `serve.py:1556`). Output
  is bounded well below `MAX_ASSISTANT_PROSE_BYTES` (65,536 —
  `doxbench_turns.py:80`), because the region it renders into is 280px. The
  verifier's clause (iii) above — refuse any output naming a path absent from the
  request — is what discharges the leak case, and it is the reason that clause is
  worth its cost.
- **A snapshot field is proposed but NOT assumed** — see ruling 2. If review
  takes it, it is one additive, optional `documents[]` property, tolerated-absent
  under the schema's own additive-growth rule
  (`ideation-dashboard-snapshot.schema.yaml:23-28`).
- **Generation never blocks a snapshot, and the observable runs in BOTH
  directions.** Forward: when the port raises, times out, or is absent, the
  emitted snapshot MUST be byte-identical to a run with no abstract at all, and
  the pane MUST state the not-yet-generated caption. Backward, and this is the
  harder half: a model-derived value MUST NOT be a snapshot field for as long as
  `spec.md:7`'s byte-identical scenario stands. Digest-keying makes a cache
  STABLE, not a tree REPRODUCIBLE — a cold cache, a swapped adapter, or a
  provider revision all yield different bytes from the same working tree, which
  is exactly what that scenario forbids. Both halves together are the testable
  form of `ideation-dashboard-snapshot.schema.yaml:17-21`.
- **Caching reuses an existing shape; no new mechanism is introduced.** Two
  digest-keyed caches already exist with exactly the semantics ruling 1 needs:
  `TurnStore` (`doxbench_turns.py:1033-1069`) is bounded and thread-safe, gives
  one-in-flight attach-and-wait, replays an identical digest without a second
  dispatch, and refuses a different digest for the same key as a conflict
  without blocking; and `_VALIDATOR_CACHE` (`doxbench_contracts.py:515-549`) is
  keyed on digests the per-call verification just PROVED (`:541`), never on time
  or trust.

## The interaction, stated

The council flagged this as the largest hole in the first draft, and it is a
hole with a live mechanism behind it. `setFocus` in the docs wheel fires
`onSelect` on EVERY NOTCH (`web/views/doc-wheel.js:205-212`) and once more at
mount (`:463`), and `staging-workbench.js:285` calls `renderAbstract` from that
callback. A design that generated on selection would therefore dispatch a model
call for every document a reader spins past. So the interaction is specified,
not left to implementation:

- **Generation is EXPLICITLY invoked** by a human control acting on the
  currently centred tile. It is never a side effect of selection, of a
  mount-time seed, or of opening a scope. *Scenario: WHEN a human spins the docs
  wheel across N documents THEN no model dispatch occurs.*
- **The in-flight state is cancellable and states the expected wait**, with the
  adapter ceiling as its visible bound: `MAX_ADAPTER_TIMEOUT_SECONDS = 120`
  (`doxbench_model.py:54`). A spinner with no stated bound in front of a
  two-minute ceiling is a surface that looks broken.
- **Re-generation is its own explicit control**, run against the subject's
  CURRENT digest — the affordance ruling 3's stale caption implies.
- **Subject recheck at paint.** The response carries the subject path and digest
  it was generated for. *WHEN a generation resolves and the pane's selected
  subject differs THEN the result MUST be discarded unrendered and the
  not-yet-generated caption MUST show for the current subject.* Without this, a
  slow answer paints itself over whatever the reader has since spun to — a
  wrong-document abstract under a confident caption.
- **Which bytes are the subject: the SAVED file.** A dirty loaded buffer is
  captioned as describing the SAVED version, and unsaved text never crosses to a
  provider — `spec.md:1046` already bans that content from the snapshot,
  transcript, thread file, log, gate record and exception detail, and there is no
  reading under which sending it to a model is the safer choice.
- **Whether an abstract survives leaving and re-entering the tile in-session** is
  a stated behaviour, not an accident of component lifetime. Proposed: it
  survives, keyed by (path, digest), because a reader comparing two documents
  will move between them and regenerating on every return would spend a model
  call on a question already answered.
- **A reader with no gate capability on the loopback console.** `spec.md:864`
  requires the context to "remain usable" there. Proposed: the generation control
  is ABSENT (not present-and-refusing), and any already-cached abstract stays
  readable with its normal caption — the same posture the surface already takes
  for session affordances.

## Capabilities

### New Capabilities

None. The obligation belongs inside the surface that already owns the docs
subpane and the model boundary; a second capability describing one pane would
split the doxBench contract across two specs, which is how two specs come to
disagree about one pane.

### Modified Capabilities

`ideation-dashboard`, in two groups. Every one is MODIFIED rather than added
beside, because adding a requirement that permits a new analysis while an
existing one forbids it is how a spec starts contradicting itself.

**Group A — the derivation and its authority. THREE requirements MODIFIED, and
the delta says so; the earlier draft listed six, and ruling 0 plus a closer read
account for the other three.**

1. **Context compression is a three-layer stack with declared fidelity**
   (`:1971`) — modified to admit a LAYER-2-CLASS SIBLING ARTIFACT and name its
   fidelity word (lossy-by-design). Layer 2 itself is untouched: it stays
   compaction into the thread-state header, owned by ONE component, because the
   abstract neither writes that header nor "preserves commitments and discards
   narrative". What binds the abstract is the requirement's UNIVERSAL final
   clause — non-authoritative, regenerable, never truth by being compressed or
   cached — plus the `:1986` "cited as truth" scenario, unchanged and now
   covering this artifact too. The sibling is **promotion-gated** and
   **human-reviewable by inheritance but NOT discharged** in this slice, stated
   as an open obligation rather than claimed, because presentation is not review.
2. **doxBench model catalog and provider boundary** (`:1046`) — the port
   resolution and the loopback-console-only gate are written about *a chat
   turn*; they widen to EVERY model consumer, so a second consumer cannot be
   argued to sit outside them. Three further clauses land here: a new consumer
   MUST NOT be smuggled through the chat-turn envelope, MUST NOT open a second
   provider path, and the port must be DECLARED AT AN ENTRYPOINT for any
   consumer to reach a provider at all — with an absent declaration read as an
   absent capability rather than an error, which is the state of the tree today.
   The three-member port surface does NOT widen, pinned by
   `test_doxbench_model.py:482` (`FORBIDDEN_PORT_MEMBERS`) and `:522`. This
   requirement is also the MECHANISM that makes ruling 2(b)'s hosted-plane
   absence mandatory rather than a design preference.
3. **doxBench scoped view** (`:864`) — the lens's "MUST NOT introduce a new
   analysis" clause is narrowed to the BULLSEYE'S OWN GEOMETRY and the
   completeness signals, the derivations it was written about, so it is not read
   as forbidding an artifact this capability's own requirements govern; and a
   model-derived artifact is required to be presented BESIDE snapshot-derived
   material, never merged into it. **Scenario `:896-899` is NOT disturbed** —
   "MUST NOT compute, adjust, or re-weight any signal" survives verbatim, and the
   added text says the abstract RE-PRESENTS. Authored against
   `ratify-doxbench-landed-context-surfaces`'s landed version of this
   requirement, not against canon.

**The three that are NOT modified, and why** — a proposal that quietly drops
three claimed modifications should say so:

- **Workbench lens bullseye at tile scope** (`:439`) — MOVED to the split change
  under ruling 0. Its no-new-analysis narrowing is stated inside `:864`'s delta,
  which names the bullseye requirement explicitly, so the narrowing binds both
  without editing the same requirement from two changes.
- **Snapshot projection contract** (`:7`) — NOT modified, because ruling 2(b)
  means no model-derived value ever becomes a snapshot field. `:7` is HONOURED
  and cited; the obligation lives in this change's own added requirement, which
  is where a future 2(a) change would have to come and amend it.
- **Delivery and regeneration** (`:263`) — NOT modified, for the same reason:
  with generation session-local and outside every lane, nothing about delivery or
  regeneration cadence changes. The never-blocks obligation is stated in the
  added requirement instead of loosening a lane requirement that currently says
  something true.

**Group B — MOVED to `ratify-doxbench-landed-context-surfaces` (ruling 0).** All
six integration-surface requirements the alignment review found — the docs tile
verbs against a wheel rather than a list (`:1853`), the per-buffer staleness
guard (`:1685`), the canvas view surface and the buffer contract
(`:1705` / `:948`), the session thread (`:1880`), and the selector's claim on the
accessible name (`:1827`) — belong to the surfaces that ALREADY SHIPPED, not to
the model-derived abstract. Four of them are modified by that change; `:1685` and
`:1880` are honoured here without modification, because ruling 3's digest rule
and ruling 4's sibling-artifact framing both sit inside what those requirements
already say. Surface identity (`:931`) and the shared-height budget also move
there, except for the two-accessible-names consequence of having a SECOND
abstract, which is this change's own and is stated in its added captioning
requirement.

`governed-derived-model`: modified ONLY if ruling 4 takes the full-conformance
option. Under the recommended framing it is honoured and cited, not changed.

## Rulings requested

Eight decisions plus one sub-ruling. None is decided; each carries options and a
recommendation, and the recommendation is an argument, not a default.

### Ruling 0 — One change, or two

All three council reviewers arrived at the same recommendation independently, so
it goes first.

- **(a) Keep it as one change.** Everything lands together or nothing does.
- **(b) SPLIT.** Change one — `ratify-doxbench-landed-context-surfaces` — is
  DOC-ONLY: promote the three landed surfaces (lens subtabs, the split+wheel,
  the deterministic abstract) to spec text, replace `:439`'s simultaneity clause
  (BREAKING #2), take the Group B integration-surface items, and settle ruling
  6's region naming. Change two is this proposal reduced to rulings 1-5 and 7
  plus `DocumentAbstract`.

**Recommendation: (b) SPLIT.** The two halves have nothing in common except the
pane they touch. Change one has no code surface worth the name, needs no ruling
beyond 6, and — decisively — REMOVES A LIVE FALSIFIED REQUIREMENT: `spec.md:439`
has forbidden the shipped subtabs since 2026-08-03, and every day that stands is
a day the spec cannot be trusted about this surface. Change two is blocked on
seven rulings, a real adapter at an entrypoint, and a non-chat prompt assembler.
Holding the first hostage to the second is how a cheap correction waits a month.
Note also that Group A item 6's delta text CANNOT be authored until
`add-doxchat-model-intake` realizes (`release-realization/spec.md:64-74`), which
is a second reason the doc-only half should not wait on this one.

**The second change is deliberately NOT created here** — Brett rules 0 first.

### Ruling 1 — Generation mode

- **(a) Deterministic extraction at generation time.** Cheapest, and it inherits
  the health aggregate's precedent verbatim (`spec.md:357`). But a deterministic
  extract is what already ships, so this option answers #84 with the thing #84
  asked to replace.
- **(b) Build-time model call in the publication/nightly lane**, keyed by the
  source document's digest. Every reader sees the same abstract, and the
  snapshot stays byte-identical for an unchanged tree because the key is
  content, not clock. But it puts a model in the path of a lane whose whole
  contract is determinism, and a provider outage becomes a publication failure.
- **(c) On-demand through the existing server-side port seam.** Generation runs
  in `serve.py`, resolving `WorkbenchModelPort` through `_workbench_model_port`
  (`serve.py:1519-1551`) under the reused `session` local-human verdict — the
  same gate the catalog and chat-turn routes already sit behind — and dispatches
  through `dispatch_turn` (`doxbench_model.py:924`). The browser's role is one
  fetch; the model is never reached from a view module, from
  `staging-workbench-model.js` (which stays pure and import-free —
  header `:2-6`, pinned by `test_staging_workbench.py:798-801`), or from a gate
  verb.

**Recommendation: (c), with a digest-keyed cache reusing `TurnStore`'s shape**
(`doxbench_turns.py:1033-1069`) rather than a new caching mechanism — one
in-flight per key, identical-digest replay, different-digest conflict — and
`_VALIDATOR_CACHE`'s discipline of keying on bytes already verified
(`doxbench_contracts.py:515-549`, key at `:541`) — with the caveat N1 records:
a SEPARATE, separately-bounded store, never the chat `TurnStore` instance, whose
64-entry / 16 MB bound abstract churn would evict. **The observable that makes
this safe:** when the port raises, times out, or is absent, the snapshot MUST be
byte-identical to a run with no abstract AND the pane MUST show the
not-yet-generated caption — one scenario covering both halves. (c) is also the
only option under which the pane can honestly say "not generated yet". Note that
(c) does NOT make (b) reachable later as a cheap evolution; see ruling 2.

#### Sub-ruling 1(c)(i) — which route

Given (c), the generation call is either:

- **(i-a) a scoped turn on the existing `POST /actions/workbench/chat-turn`**
  (`app.js:243`) — no new route, no widening of the fetch-site pin.
- **(i-b) a NEW same-origin route** beside the catalog and turn routes, with one
  new `app.js` call site.

**Recommendation: (i-b).** A scoped chat turn would smuggle a non-chat consumer
through the chat envelope: the released turn contract carries a bound buffer key,
per-buffer observed hashes, and a proposal target expressed as a buffer key
(`spec.md:2013`), none of which an abstract request has, and `dispatch_turn`
would still demand a response shaped `{assistant_prose, proposals}` (`:985`)
from a request that is not a conversation. The cost of (i-b) is explicit and
budgeted: `test_renderer.py:142-143` fixes the fetch-FILE set and `:152` asserts
`len(by_file["app.js"]) == 5`, widening only by "the arithmetic of new
SAME-ORIGIN backend routes... declared loudly" (`:129-133`). So the pin goes 5 →
6, named in that docstring the way the thread-read route was. `app.js` remains
the ONE call site; `staging-workbench.js` gains no fetch and
`staging-workbench-model.js` stays transport-free.

### Ruling 2 — Snapshot entry, or session-only

- **(a) Snapshot entry**: one additive, optional `documents[]` property in the
  next additive cut. Every plane sees the same abstract; the hosted read-only
  plane gets it for free.
- **(b) Session-only**: the abstract lives in the console session and never
  enters the snapshot. The hosted read-only plane shows the DETERMINISTIC
  abstract plus an honest note that no distillation is available there — which
  `spec.md:1046` does not merely permit but REQUIRES, since that plane "MUST
  offer neither route" and therefore cannot generate one.

**Recommendation: (b), and (a) is WITHDRAWN as a declared evolution.** The
earlier draft offered (a) as the natural next step; the council was right that it
cannot be, for two independent reasons. First, determinism: `spec.md:7` requires
a byte-identical snapshot from an unchanged tree, and a digest-keyed model value
is cache-STABLE, not tree-REPRODUCIBLE — a cold cache, a swapped adapter or a
provider revision all change the bytes without the tree moving. Second,
regenerability: `spec.md:1046` forbids the hosted/read-only plane from reaching
the model at all, so a projected L2-class artifact would land precisely where the
"regenerable" half of its own authority claim is structurally unavailable. So (a)
is not an evolution of (b) — it is a SEPARATE FUTURE CHANGE that must first amend
`:7`'s byte-identical scenario, and it should be argued on its own terms rather
than pre-blessed here. **This ruling sets `target_release`:** (a) makes it the
next additive cut, fresh-counted at realization; (b) makes it `none`.

**The 2(b) mirror, recorded rather than hidden:** with the abstract session-local,
two consoles opened at the same (repository, ref) may show DIFFERENT abstracts
for the same document. That is the honest cost of (b), and it is smaller than the
cost of (a) — a divergence between two humans' screens is visible to them, while
a non-reproducible snapshot field is a silent breach of the projection
contract.

### Ruling 3 — Staleness over an edited buffer

The abstract is derived from a document the human may be actively editing. When
the buffer has moved past the digest the abstract was generated from:

- **(a) Show it, labelled stale**, with the digest mismatch stated.
- **(b) Show a regenerating state** and replace it when the new one lands.
- **(c) Show nothing** until regenerated.

**Recommendation: (a), with (b) while a regeneration is in flight.** The
governing rule is `spec.md:1686` — the canvas controls stay inside the
per-buffer staleness guard, whose settled content-identity notification is
exactly the mechanism (b) would ride; `TurnStore`'s attach-and-wait
(`doxbench_turns.py:1033-1069`) already encodes (b)'s semantics on the server
side, so neither state needs new machinery. **One collision with ruling 6 to
settle explicitly:** `:1686` is a PER-BUFFER guard, and under ruling 6(a) most
wheel subjects have no buffer at all — so for an UNLOADED subject the source
digest is the digest of the SERVED SAVED CONTENT, and the per-buffer
settled-identity notification is escalated to only when the subject happens to be
a loaded buffer. Two precedents point the same way:
`documentAbstract` states an absence rather than rendering an empty box
(`staging-workbench-model.js:1575-1581`), and the stale-application protection
refuses on a hash mismatch while offering inspection — never a silent merge, no
force-apply (`spec.md:1081`). A stale abstract is information; a blank pane is
not. (c) is the option that makes the pane look broken.

### Ruling 4 — Authority frame

- **(a) The `compact_thread` DISCIPLINE in a new type.** Model output passed IN,
  verified here, refused on loss, non-authoritative and regenerable by
  construction — but as a new frozen `DocumentAbstract`, because
  `DocumentThread` hard-codes `regenerable_from = transcript`
  (`doxbench_threads.py:593`, refused at `:619`) and its refusal rule keys on
  evidence refs and pending actions a document abstract has none of
  (`:1071-1093`). The abstract's rule is document-shaped and is stated in full
  under "The verifier's rule" above: coverage measured against the SNAPSHOT'S
  declared topics and destinations (so it fires on generation #1, not only on a
  regeneration), described honestly as subject-mention coverage rather than
  fidelity, plus the one clause that is genuinely testable — name the subject,
  name no path the request did not carry.
- **(b) Full `governed-derived-model` conformance**: a declared conformance
  family with all six dials (`governed-derived-model/spec.md:6`),
  `authority_status` as a single-value `[non_authoritative]` enum with in-place
  promotion forbidden (`:26`), full provenance in one of its TWO declared forms
  — evidence trace with source references, or the assumptions-forbidden form
  (`:46-51`), where the minimum-one-item evidence trace plus the single-value
  `[none]` invented-facts enum belong specifically to the assumptions-forbidden
  scenario at `:58-61`, spelled `minItems` in
  `contracts/schemas/xfactory-derived-model-conformance.schema.yaml:63` and
  `:90` — plus human-gated promotion (`:88`) and the `calibrated` tier (`:100`).

**Recommendation: (a).** It is the frame this surface already runs under, it is
already executable, and its guarantees are structural rather than declared — the
constructor cannot return an authoritative artifact. (b) is the heavier and more
general instrument, built for a domain factory declaring a derived-model FAMILY
across object kinds; a per-document abstract inside one pane is not that shape,
and adopting (b) would mean declaring a conformance family whose only member is
a UI-adjacent string. Named because if review wants the abstract to be a
first-class governed derived object rather than a pane's content, (b) is the
right instrument and this recommendation is the wrong one.

### Ruling 5 — Captioning

The new abstract MUST be captioned as model-derived, non-authoritative and
regenerable — the exact inverse of the guard it replaces. Proposed vocabulary,
with the accessibility carrier declared per caption (see `:931` above):

- On the model-derived abstract: **"Distilled by a model — not authoritative;
  regenerable from the document."** — visible text AND part of the region's
  accessible name.
- Beside it, on the deterministic one: **"From the document's own headers"** —
  visible text AND part of its region name; never "distilled", which is the half
  of the old guard that stays true.
- When the buffer has moved on: **"Distilled from an earlier version of this
  document"**, with the source digest stated — visible text only.
- When none has been generated: **"No distillation generated for this document
  yet"** — visible text only; an absence STATED, in the register
  `staging-workbench-model.js:1579` already uses.
- On the hosted read-only plane under ruling 2(b): **"No distillation is
  available on this plane"** — visible text only, and a statement about the
  PLANE, never about the document.

The load-bearing rule under all five: the caption states WHO derived it and WHAT
it is not. "AI-powered", bare "Summary", and any wording implying the abstract
can be cited are out.

### Ruling 6 — What the abstract's subject follows

Two surfaces now claim the phrase "selected document": the abstract region's
`aria-label` (`staging-workbench.js:250`) and the loaded-document selector,
whose scenario requires the selector, the canvas, and the chat to agree about
the selected BUFFER (`spec.md:1844-1846`). So:

- **(a) The abstract follows the WHEEL TILE** — it describes whatever document
  the reader last pointed at in the docs pane, whether or not that document is
  loaded for editing.
- **(b) The abstract follows the SELECTED BUFFER** — it describes what the
  canvas is editing, and the wheel only navigates.

**Recommendation: (a), with the region renamed.** The docs pane is a READING
surface; its wheel exists to let a reader move through a scope's documents, most
of which are never loaded. Under (b) the pane would go blank or stale the moment
a reader looked at an unloaded document, which is the common case. (a) also
keeps `spec.md:1706` satisfied without touching the buffer contract: the wheel
selects a SUBJECT TO DESCRIBE, not a buffer to edit, so it is not a second
buffer-selection surface. The region's `aria-label` changes from
`"selected document"` to something that names the pointed-at document rather
than the working one, which is what `:1828`'s agreement scenario needs in order
to stay true.

### Ruling 7 — Which documents are eligible subjects at all

This is the sharpest finding of the review, and it can invalidate ruling 6(a) if
ruled the wrong way. The existing rule on this surface is that **disclosure
requires edit authority.** `_require_in_scope_and_editable`
(`doxbench_turns.py:585-591`) refuses a path that is in scope but not editable
with "path is readable but not editable", and the guard's own docstring says a
readable-but-not-editable path "is always refused before any disclosure"
(`:612-613`). `doxbench_scope.py:390` states the principle in one line:
"disclosure requires edit authority, which is the rule, not an accident."

And `editable_paths` is NARROW. It is populated only from sections flagged
`owned` (`doxbench_scope.py:356-358`), and exactly ONE section carries that flag
— `folder`, the topic's own material (`:35-42`, `"owned": True` at `:41`). So on
a CLUSTER or POSSIBLE tile there is no folder section and `editable_paths` is
EMPTY. Under ruling 6(a), where the abstract follows whatever the reader spins
to, most wheel subjects on a staged topic are non-owned, and on a cluster tile
(`spec.md:868`) the eligible set is empty outright. Either the abstract is
refused for 100% of documents on those tiles, or an implementation quietly opens
a NEW provider-disclosure path that the rule above forbids — and it would do so
by accident, in a pull request about a UI pane.

- **(a) Subject restricted to `editable_paths`.** The existing rule holds
  untouched; elsewhere the caption states honestly why no abstract is available.
- **(b) Widen to `context_paths` via an explicit spec delta** relaxing the
  disclosure rule for single-subject, read-only derivation with no edit
  authority attached.
- **(c) For non-editable subjects, derive from snapshot-indexed fields only** —
  which is the deterministic abstract, so the model half simply does not exist
  there.

**Recommendation: (a) for the first slice, with (b) named as the follow-on
ruling.** (a) is the only option that does not relax a security rule as a side
effect of a feature, and its cost is honest and visible: on a cluster tile the
pane says so. (b) is very likely the RIGHT long-term answer — a read-only
single-document derivation is genuinely not the disclosure risk the rule was
written against — but it deserves its own delta, its own scenario, and Brett's
explicit ruling, not an implementation decision. (c) is a trap: it would present
two different products under one caption depending on the tile, which is exactly
the confusion ruling 5 exists to prevent.

Whichever way this goes, the delta MUST state WHICH PATH SET the subject is
drawn from. That sentence is the whole point.

## Impact

- **Affected specs**: `ideation-dashboard` (twelve requirements plus surface
  identity, inventoried above); `governed-derived-model` cited, modified only
  under ruling 4(b).
- **Affected code**:
  `scripts/ideation_dashboard/web/views/staging-workbench-model.js` (the new
  abstract's view-model beside `documentAbstract` at `:1545`, and the reversed
  comment at `:1530-1544` — the module stays PURE, import-free and
  transport-free, header `:2-6`);
  `web/views/staging-workbench.js` (the abstract region at `:245-259`, its
  consumer at `:149`, the region name at `:250`, and — under BREAKING #2 — the
  subtab visibility at `:488`);
  `web/app.js` (the ONE new fetch call site, never a view module);
  `scripts/ideation_dashboard/serve.py` (the generation route beside
  `_workbench_model_port` at `:1519-1551`, and the STALE banner at `:2128-2134`
  which still asserts "no code below calls it" of `dispatch` — corrected as part
  of this change, not left to contradict a live call site);
  `scripts/ideation_dashboard/doxbench_packet.py` (a SECOND `PACKET_PURPOSE_*`
  beside `:308`, and the layer-2-class sibling declaration — layer 2's own
  `owner` and `note` at `:224-229` are NOT touched);
  `scripts/ideation_dashboard/doxbench_turns.py` (`build_abstract_envelope` with
  its own section-order constant, beside the chat-shaped
  `build_prompt_envelope` at `:837`);
  `scripts/ideation_dashboard/doxbench_scope.py` (whichever path set ruling 7
  selects, read off `:356-358` / `:35-42`);
  `scripts/ideation_dashboard/doxbench_knowledge.py` (the `DocumentAbstract`
  type and its verifier — one of the two homes #84's own re-grounding comment
  names);
  **the ENTRYPOINT** — `cli.py` at its `build_server` call (`:298`) and/or
  `serve.py`'s `serve()` in the `build_kwargs.setdefault` idiom it already uses
  for the notebook adapter and the knowledge declaration (`:4850`, `:4857`) —
  to declare `OmpHarnessBridge` as `model_port_factory`, which nothing does
  today. Under ruling 2(a) only:
  `scripts/ideation_dashboard/generator.py` and
  `contracts/schemas/ideation-dashboard-snapshot.schema.yaml`.
- **Affected tests**:
  `test_doxbench_context_panes.py` — the captioning pin relocated from the
  whole-file sweep at `:144-152` onto the node harness fixture at `:83-94` as a
  per-abstract caption assertion, with the docstring's scope statement
  (`:26-29`) rewritten to RECORD the reversal rather than erase the old ruling,
  and the `:31-34` note that rendered geometry stays with the operator rig left
  standing; plus the shared-budget rule at `:231-240` / `:264-269`.
  `test_doxbench_packet.py:920-921` — **unchanged**, and asserted to be
  unchanged: `layer(2).owner` stays `"doxbench_threads.compact_thread"`, which is
  the point of declaring the abstract a sibling rather than a second owner.
  `test_renderer.py:152` — the `app.js` fetch count widens 5 → 6, declared by
  name in the `:129-133` docstring.
  `test_doxbench_accessibility.py:281-311` — a second named region under the
  same idiom.
  `test_doxbench_model.py:482` / `:522` — unchanged, and asserted to be
  unchanged: the port surface does not widen.
  `test_staging_workbench.py:798-801` — the import-free assertion, unchanged.
- **Hermeticity, stated correctly.** `tests/hermeticity.py` is NOT a network
  guard: it makes the real `nlm` and `gh` binaries unreachable (`:1`,
  `GUARDED_BINARIES` at `:91`) through a PATH shim plus two in-process seams
  (`workbench._default_runner` and `session_pr.SubprocessCommandRunner.run`,
  which also covers the branch `git push`). The BUNDLE network ban is
  `test_renderer.py:115` plus the doxBench-module sweep at `:990-992`, applied
  at `:1031`. And the guarded set is `nlm` and `gh` — **not `omp`**, which the
  real adapter below spawns. So two tasks, not an assumption: **add `omp` to
  `GUARDED_BINARIES`, or pin that abstract coverage injects its own `spawn=`**;
  and **any new coverage that could reach a provider needs its own seam or shim
  entry.**
- **A real adapter EXISTS — the earlier draft was wrong to say otherwise.**
  `OmpHarnessBridge` (`scripts/ideation_dashboard/doxbench_bridge.py:869-870`) is
  a real `WorkbenchModelPort` adapter: it supervises an `omp --mode rpc` child
  over stdio, holds no credential, runs with an allowlisted child environment,
  and is loopback by construction; its per-turn view `_ConversationPort` (`:1549`)
  is, in its own words, something `dispatch_turn` "cannot tell from the adapter".
  Live smoke coverage exists and skips without a harness
  (`tests/ideation-dashboard/test_doxbench_bridge_live.py`). So
  `FakeWorkbenchModelPort` (`doxbench_model.py:1037`) is the only adapter the
  MODEL MODULE defines — not the only adapter this surface has.
- **The real blocker, named.** NO ENTRYPOINT DECLARES A MODEL PORT. Every
  `model_port_factory` reference lives inside `serve.py` — the parameter (`:4645`),
  the binding (`:4784-4785`), the class default `None` (`:1372`) — while `cli.py`
  omits it at its `build_server` call (`:298`) and `serve()`'s own
  `build_kwargs.setdefault` block declares `adapter_factory` and
  `knowledge_declaration` and never a model port (`:4850`, `:4857`). So
  `_workbench_model_port` returns `None` at `:1546-1547` on every real serve, and
  the pane's honest caption is the only thing any operator can see today.
  Declaring `OmpHarnessBridge` at the entrypoint in that same setdefault idiom is
  a TASK OF THIS CHANGE.
- **Realization evidence, tightened.** Because of the two points above, a green
  suite against `FakeWorkbenchModelPort` alone SHALL NOT close this change.
  Realization evidence SHALL include at least ONE OPERATOR RUN on the real
  corpus through a real adapter — the bridge lane, or the T100 rig's
  operator-supplied adapter. A feature whose only proof is a constant-returning
  fake (`doxbench_model.py:1101`) has not been shown to work.
- **Archive gate.** `code_surface` is non-empty under EITHER branch of ruling 2,
  so this change cannot archive on landing: `release-realization/spec.md:23-32`
  requires merge evidence plus a green run of the runnable surface, and only
  then do the deltas promote (`:39-41`). A `target_release` of `none` means NO
  BUNDLE IS CUT — it does not mean doc-only. Realization evidence is
  `pytest tests/ideation-dashboard` green plus
  `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, PLUS the operator run
  named above.
- **Contract release.** `contract-v1.41` is the current bundle
  (`contracts/manifest.yaml` line 3 `contract_bundle_version: contract-v1.41`;
  `contracts/CHANGELOG.md:76`; `contracts/releases/contract-v1.41.digests.yaml`;
  annotated tag `contract-v1.41`) — state of the surface, not an allocation. The
  number for any cut this change needs is fresh-counted AT REALIZATION and is
  deliberately not written here: `spec.md:2013` requires late allocation and its
  scenario at `:2020-2022` rejects early reservation outright, and the
  `Unreleased` block already accumulating two additive items
  (`contracts/CHANGELOG.md:12`) may fold first. Precedents:
  `declare-client-standing-policy-contract` and
  `add-model-capability-vocabulary` (whose front-matter records the same
  "fresh-counted at realization" posture at its `proposal.md:3`).
- **Sequencing** — three changes, all ahead of this one:
  - `add-doxchat-model-intake` (**ratified** 2026-08-21) MODIFIES the SAME
    requirement as Group A item 6 — doxBench model catalog and provider boundary
    (`its proposal.md:139`) — and declares `staging-workbench-model.js`,
    `serve.py` "beside the existing `_workbench_model_port` seam", and `app.js`
    transport in its `code_surface`. Per `release-realization/spec.md:64-74`,
    this change references it and **declares its deltas relative to that
    change's outcome**.
  - **The BRIDGE lane, not the broker lane, is what makes this feature
    demonstrable.** `add-model-provider-broker` (draft) is about CREDENTIALED
    HOSTED providers — it narrows the boundary to one module and mints a
    short-lived token — and this feature needs neither a credential nor a hosted
    provider. `OmpHarnessBridge` already runs a local child with no secret. So
    the sequencing dependency is the bridge being DECLARED AT AN ENTRYPOINT (a
    task here), and the broker is an unrelated later lane; if it lands first,
    hosted models become an additional option rather than a prerequisite.
  - `add-lens-document-selection` (ratified, 14 tasks done / 1 open) touches
    `web/views/lens.js`, `lens-model.js`, `bullseye.js` and `web/styles.css` —
    the KEYWORD-LENS surface and the theme tokens, not the workbench lens tab or
    the docs subpane; but `bullseye.js` and `styles.css` are shared, so it lands
    first.
- **Speckit follow-on**: exactly ONE feature, `specs/014-*`. `specs/013-*` is
  claimed by `013-first-wallet`.
- **Origin**: recorded in this change's `.openspec.yaml` as an ad-hoc origin
  (issue #84 plus Brett's 2026-08-25 option-C ruling), per
  `add-lens-document-selection/.openspec.yaml`'s form and the origin-retention
  gate at `release-realization/spec.md:97-103`. The ruling was made in session,
  so it is also recorded as a comment on #84 — an in-session ruling with no
  durable record is not an origin anyone can audit.
- No register, manifest, notebook or gate-verb change. Nothing here grants write
  authority; the abstract feeds no completeness score, no staged-topic health
  aggregate, no readiness tier and no gate.

## Out of scope

- **Any authority for the abstract.** Never citable, never an input to
  completeness (`spec.md:329`), never an input to staged-topic health or the
  readiness gate (`:357`), never promoted in place — promotion happens only by a
  human creating a new document through a gate verb.
- **Widening the provider port.** The three declared members stay three
  (`test_doxbench_model.py:522`). Prompt assembly is NOT out of scope and does
  not "stay where `dispatch_turn` puts it" — `dispatch_turn` performs no
  assembly at all (it hands the envelope over opaquely at
  `doxbench_model.py:972`); assembly is new surface in `doxbench_turns.py`, above.
  What stays out of scope is any SECOND provider verb.
- **Building a NEW provider adapter.** A real one exists
  (`doxbench_bridge.py:869-870`) and this change WIRES it at an entrypoint rather
  than writing another. Credentialed hosted providers, token minting, and the
  narrowed provider boundary remain `add-model-provider-broker`'s.
- **Prompt-injection defence beyond the bounded obligation stated above.** The
  one-subject-only rule, the tightened output bound, and the refuse-a-foreign-path
  clause are in scope; a general-purpose untrusted-content sandbox for the whole
  chat surface is not.
- **Layer 3 of the compression stack**, still declared unrealized
  (`doxbench_packet.py:230-240`).
- **The chat-turn envelope family** `request_v2` / `success_v2`
  (`xfactory-workbench-chat-turn.schema.yaml:346`, `:390`) — see the
  disambiguation above.
- **Abstracts for anything but a document**: no cluster, possible, staged-topic
  or repository-level distillation.
- **Rendered geometry.** The context panes' measurements stay with the operator
  rig, exactly as `test_doxbench_context_panes.py:31-34` records.
