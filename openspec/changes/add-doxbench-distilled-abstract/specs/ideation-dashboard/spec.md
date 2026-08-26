# ideation-dashboard — add-doxbench-distilled-abstract deltas

Authored relative to the outcome of `ratify-doxbench-landed-context-surfaces`
(`release-realization/spec.md:64-74`): the `doxBench scoped view` block below is
that change's landed text, edited further here.

## MODIFIED Requirements

### Requirement: Context compression is a three-layer stack with declared fidelity
Compression SHALL be organized as THREE layers, each with a declared fidelity contract, and no layer SHALL be described as doing another's work. Layer one is SELECTION, performed by the knowledge service: it is LOSSLESS BY REFERENCE, because material left out of a packet remains one retrieval call away and the packet names what it carries. Layer two is SEMANTIC COMPACTION into the thread-state header: it is LOSSY BY DESIGN, human-reviewable, promotion-gated, non-authoritative, and regenerable — it preserves commitments and discards narrative. Layer three is MECHANICAL REVERSIBLE COMPRESSION at the model boundary: heavy material offloads to session artifacts behind recoverable placeholders, and it SHALL be REVERSIBLE — an offloaded item MUST be retrievable in full by the same session — and SHALL run INSIDE this surface's own trust boundary, with no third-party proxy in the path and no new network dependency. Every artifact any layer produces SHALL be non-authoritative and regenerable, and MUST NOT become truth by being compressed, cached, or offloaded. The lifecycle-status exemption SHALL live UPSTREAM of layer three, in the assembler, and MUST NOT be delegated into any component that cannot read a lifecycle status — a compressor with no caller-metadata surface is disqualified from carrying it by construction, not by preference. A candidate component for any layer SHALL be recorded with its adoption gates rather than adopted provisionally, and this capability MUST NOT depend on a watch-listed candidate: a candidate is admitted only when every recorded gate holds, including a sandboxed trial measuring net benefit on this surface's own workload rather than a published headline. Every external claim about a candidate SHALL be verified against the upstream source before it enters contract text. A LAYER-2-CLASS SIBLING ARTIFACT MAY be declared: a derived artifact that carries layer two's FIDELITY WORD — lossy by design — without being layer two's own work, without writing the thread-state header, and without claiming layer two's commitment-preservation rule, which is shaped for a transcript and not for a document. A sibling SHALL declare its own verifier and its own refusal rule, and MUST NOT be recorded as a second OWNER of any layer: the declared owner of each layer stays exactly one component, because a fidelity contract with two owners in a one-owner field is a comment rather than a checker. A sibling is bound by every clause of this requirement that speaks of what ANY layer produces — non-authoritative, regenerable, never truth by being compressed, cached, or offloaded — and by the promotion rule, which stays a human creating a new object through review. Layer two's HUMAN-REVIEWABLE adjective SHALL be inherited by a sibling as a STATED OPEN OBLIGATION rather than claimed as discharged where the realization provides only presentation, because rendering an artifact in a pane is not a human reviewing it.

#### Scenario: A layer claims another's fidelity
- **WHEN** a realization describes selection as lossy, semantic compaction as lossless, or mechanical offload as a semantic summary
- **THEN** it MUST be rejected — the three fidelity contracts are what make the stack readable

#### Scenario: An offloaded item is needed again
- **WHEN** material offloaded at layer three is required in full later in the same session
- **THEN** it MUST be retrievable in full

#### Scenario: A third-party compressor is proposed
- **WHEN** a proposal would route model traffic through a third-party compressor or proxy
- **THEN** it MUST be rejected unless every recorded adoption gate holds, including a sandboxed trial on this surface's own workload
- **AND** the lifecycle-status exemption MUST NOT be moved into a component that cannot read a lifecycle status

#### Scenario: A compressed artifact is cited as truth
- **WHEN** any path would treat a summary, a thread-state header, an offloaded artifact, or a derived index as authoritative
- **THEN** it MUST be rejected — promotion happens only by creating a new object through review

#### Scenario: A sibling artifact is declared at a layer's fidelity class
- **WHEN** a derived artifact is declared as a layer-2-class sibling
- **THEN** it MUST carry the lossy-by-design fidelity word, declare its own verifier and refusal rule, and remain non-authoritative and regenerable
- **AND** the declared owner of layer two MUST remain exactly one component

#### Scenario: A sibling claims layer two's own obligations
- **WHEN** a sibling artifact is described as preserving commitments or as writing the thread-state header
- **THEN** it MUST be rejected — those are layer two's own work, and a sibling borrows the fidelity class and not the job

#### Scenario: Presentation is offered as human review
- **WHEN** a realization claims a sibling artifact is human-reviewable because it is rendered on a surface
- **THEN** the claim MUST be rejected and the adjective MUST stand as a stated open obligation

### Requirement: doxBench model catalog and provider boundary
The dashboard backend SHALL expose a same-origin workbench model catalog whose entries carry a stable opaque model id, human label, provider class, input/output limits, availability, and a human-readable data-handling badge. The catalog MUST NOT expose a provider credential, raw secret, raw endpoint, secret environment-variable name, or provider request template, and the browser MUST NOT call any model provider directly. EVERY MODEL CONSUMER on this surface — a chat turn, and any further consumer such as a per-document derivation — SHALL accept only a model id present and available in the current catalog and SHALL resolve that id through a server-side injected model-provider port whose member surface SHALL remain exactly the three declared members — the adapter-declared timeout, the catalog, and the single opaque dispatch — so that per-turn model selection, harness session handling, and any adapter-internal routing are performed INSIDE an adapter and MUST NOT be added as a fourth provider verb. A catalog entry MAY name a ROUTING RULE this capability owns rather than a single provider model — an `auto` entry that maps a turn to a model by declared role — and such an entry SHALL declare itself as a routing rule with the data-handling badge of the models it may route to, because an entry that hid a routing decision behind a model-shaped id would report a handling posture it does not control. Provider credentials MUST come only from the deployment's approved server-side credential mechanism and MUST NOT enter browser storage, a request body, response body, dashboard snapshot, chat transcript, thread file, log, gate record, git artifact, or exception detail; an adapter that reaches a hosted provider SHALL obtain its credential through the ratified broker lane and MUST NOT hold or read a raw secret of its own. A hosted fallback MAY be offered only when the deployment explicitly enables it and its configured data-handling policy meets the catalog badge; otherwise the model MUST be unavailable. The model catalog and EVERY model-consuming route SHALL be offered only on a loopback human console with a real checkout, resolved actor, and demonstrated console presence; the hosted/read-only plane MUST offer NONE of them. The selector MAY additionally offer exactly ONE non-model INTAKE affordance, whose behaviour this capability's intake requirements govern. That affordance is not a catalog entry: it carries no model id, it can never be submitted as one, and a chat turn naming it MUST refuse exactly as a turn naming any absent model id refuses. The catalog's own contents remain SERVER-DECLARED — the intake affordance opens a governed path to a new declaration and MUST NOT become one. A NEW model consumer SHALL reach the provider through this same seam and MUST NOT be added as a fourth provider verb, MUST NOT open a second provider path, and MUST NOT be smuggled through the chat-turn envelope: a consumer whose request is not a conversation SHALL carry its own request shape and its own declared purpose. The port MUST also be DECLARED AT AN ENTRYPOINT for any consumer to reach a provider at all; where no entrypoint declares one, every consumer's honest posture is an absent capability rather than an error. Where the declared adapter is STATEFUL — a supervised harness child holding per-thread sessions — the declaration SHALL resolve to ONE instance for the life of the served process, and the per-request accessor SHALL return that same instance rather than constructing a new one, because an adapter rebuilt per request cannot hold the one-session-per-document-thread correspondence this capability requires elsewhere and would restart a child on every call.

#### Scenario: The browser loads model choices
- **WHEN** local doxBench opens with one or more allowed providers configured
- **THEN** the selector MUST show exactly the available catalog entries and their data-handling badges, plus at most the single intake affordance
- **AND** no credential or raw provider endpoint MUST be present in the page or catalog response

#### Scenario: The intake affordance is submitted as a model
- **WHEN** a chat request names the intake affordance's selector value rather than a catalog model id
- **THEN** the server MUST refuse with the same fixed refusal an absent model id produces, before any provider call
- **AND** no intake-specific failure code MUST be added, because the affordance is not a model and the existing refusal already states the truth

#### Scenario: The menu offers a routing rule
- **WHEN** the catalog offers an `auto` entry that this capability resolves to a model by role
- **THEN** the entry MUST declare itself a routing rule and carry the handling badge of every model it may route to
- **AND** the resolved model MUST be recorded on the turn, so a transcript names the model that actually answered

#### Scenario: No model is configured
- **WHEN** the model catalog is empty
- **THEN** the chat rail MUST explain that no allowed model is configured
- **AND** every loaded editor MUST remain usable

#### Scenario: An unknown model id is submitted
- **WHEN** a chat request names a model id absent from or unavailable in the current catalog
- **THEN** the server MUST refuse before any provider call

#### Scenario: A fourth provider verb is proposed
- **WHEN** any realization would add a port member beyond the declared three to carry model switching, session handling, or harness control
- **THEN** it MUST be rejected — that behavior belongs inside an adapter, and a fourth member is a second provider verb by another name

#### Scenario: A browser attempts a direct provider call
- **WHEN** the dashboard bundle or runtime would contact a model endpoint other than the same-origin workbench routes
- **THEN** the renderer boundary MUST fail validation and the call MUST NOT ship

#### Scenario: Hosted doxBench is opened
- **WHEN** doxBench runs on the hosted plane
- **THEN** the model catalog and turn capabilities MUST be absent
- **AND** no chat or editor control implying unavailable authority MUST be reachable
- **AND** the intake affordance MUST be absent with them, because a plane that may not run a turn may not enrol a provider either

#### Scenario: A second model consumer is added
- **WHEN** a capability adds a model consumer that is not a chat turn
- **THEN** it MUST resolve its model through the same server-side injected port under the same loopback-console gate
- **AND** the port's member surface MUST remain exactly the three declared members

#### Scenario: A non-conversation request is offered as a chat turn
- **WHEN** a model consumer whose request carries no human message, transcript, or buffer set would ride the chat-turn envelope
- **THEN** it MUST be rejected and MUST carry its own request shape and declared purpose

#### Scenario: No entrypoint declares a model port
- **WHEN** a served process is started by an entrypoint that declares no model-provider port
- **THEN** every model consumer MUST report an absent capability and MUST NOT fail as an error

#### Scenario: A stateful adapter is resolved twice in one process
- **WHEN** two requests in one served process each resolve the model port
- **THEN** both MUST receive the SAME adapter instance
- **AND** no adapter child process MUST be started a second time by the act of resolving

### Requirement: doxBench scoped view
The dashboard SHALL provide doxBench as the named evolution of the staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — with three coordinated regions over that scope. A context region SHALL retain `docs` and `lens`: `docs` SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it, plus — Brett's 2026-07-25 dogfood ruling — the member documents of the topic's linked clusters as a THIRD, separately labelled cluster-neighbourhood section, inherited via clusters, never conflated with the topic's own material, and never an input to the topic's health or the readiness gate, which stay folder-scoped) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them; `lens` SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. The `docs` context's expanded tile SHALL offer this capability's three document verbs — read, load-for-editing, and save — as specified by their own requirement. An authoring canvas SHALL present exactly ONE buffer at a time — the SELECTED buffer of the loaded set — and the SELECTION SHALL be made outside the canvas rather than by the canvas: the context region's `outline` selection tab SHALL select the `outline` buffer, loading a document SHALL select that document, and the chat rail's loaded-document selector SHALL select among the loaded documents. The `outline` buffer SHALL load the topic's declared outline material when one exists — for a staged topic, the fragment's outline material — and a document buffer SHALL load the exact document the human loaded; the canvas SHALL provide browser-local editing plus live rendered Markdown preview of the SELECTED buffer on the local human console, presented as this capability's Editor/Preview view-tab pair rather than as a side-by-side split pane, while an absent outline remains an explicit empty/create state rather than fabricated content. The canvas MUST NOT render a second buffer-selection tablist beside the selection surfaces the context region and the chat rail own, because two controls answering one question is how the two come to disagree. A chat region SHALL contain Working subject, the loaded-document selector, transcript, server-declared model selection, and composer, and SHALL ground turns on the current canvas buffers and this capability's bounded context packet as specified by this capability. doxBench's corpus write authority SHALL remain the human-only gate verbs `create-document`, `edit-document`, `open-pr`, session share, and session abandon: buffer edits, chat turns, thread writes, and AI Apply MUST write no corpus document, register entry, workbench manifest, snapshot, or gate artifact; Save MAY materialize/join a branch session and invoke only create/edit as specified; no verb MAY delete a document; and no session write may touch the served checkout. With the gate/model capabilities absent or on the hosted plane, the context SHALL remain usable and doxBench SHALL render read-only outline/document content without reachable editing, chat, threads, or write controls. The `docs` context SHALL present its document set as a VERTICAL SPLIT: a per-document ABSTRACT REGION above, and a single-reel DOCUMENT WHEEL below that places this scope's documents — every separately labelled section of them flattened into one ordered reel — in the surface's own drum projection with its own established click and spin gestures. Selecting a wheel tile SHALL make that document the abstract region's SUBJECT, and the abstract region SHALL RE-PRESENT ONLY what the snapshot already carries for that document — its own `Summary:` header, its declared topics, its stage and kind, its declared destinations, and its completeness score beside the five named signals — and MUST NOT compute, adjust, or re-weight any of it, exactly as the docs rows are already held to. The `lens` context SHALL present its three sections as named, always-reachable sections of one tablist as that panel's own requirement specifies. Neither presentation SHALL introduce a new score or a new snapshot field. The no-new-ANALYSIS clause in this requirement, and in the workbench bullseye requirement it restates, SHALL be read as governing THE BULLSEYE'S OWN GEOMETRY and the completeness signals — the derivations those clauses were written about — and SHALL NOT be read as forbidding a separately captioned, explicitly non-authoritative MODEL-DERIVED artifact that this capability's own requirements govern, feeds no score, no aggregate, no readiness tier and no gate, and never replaces or adjusts anything the snapshot carries. A model-derived artifact admitted this way SHALL be presented BESIDE the snapshot-derived material and never merged into it, so a reader can always tell which claim is the document's own and which a model made.

#### Scenario: doxBench opens on a cluster
- **WHEN** a human opens doxBench from a cluster tile
- **THEN** the view MUST scope to that cluster: `docs` lists exactly that cluster's snapshot document edges and `lens` is scoped to that cluster's declared topics
- **AND** the canvas MUST show an honest empty Outline state unless that scope declares outline material

#### Scenario: doxBench opens on a possible
- **WHEN** a human opens doxBench from a possible tile
- **THEN** `docs` MUST list the documents its recorded supporting evidence cites
- **AND** any documents inherited from its claiming clusters MUST appear in a separately labelled section, distinct from cited evidence

#### Scenario: doxBench opens on a staged topic
- **WHEN** a human opens doxBench from a staged-topic tile
- **THEN** `docs` MUST list the topic folder's corpus documents together with every document whose declared destination names that staging topic
- **AND** the member documents of the topic's linked clusters MUST appear in a separately labelled cluster-neighbourhood section, never conflated with the topic's own material
- **AND** the `outline` buffer MUST load that fragment's outline material from the active repository/ref

#### Scenario: A document is loaded for editing
- **WHEN** a human uses the load verb on a `docs` tile
- **THEN** the canvas MUST load that exact document as a buffer of the loaded set and select it
- **AND** docs/lens context, every other loaded buffer, and chat state MUST remain available

#### Scenario: The outline selection tab becomes the working context
- **WHEN** a human focuses the context region's `outline` selection tab
- **THEN** the `outline` buffer MUST become the selected buffer and the canvas MUST show that buffer's working content, including unsaved edits
- **AND** the context region's own outline pane MUST keep rendering the material as it stands in the source, so "what is stored" and "what I have unsaved" remain separately readable

#### Scenario: Cluster-neighbourhood documents stay out of health
- **WHEN** a staged topic's health or its readiness gate is computed
- **THEN** cluster-neighbourhood documents MUST contribute nothing — health and the gate stay derived from the topic FOLDER's own corpus documents only

#### Scenario: A docs row shows how far a document has come
- **WHEN** the docs context renders a document the snapshot scores
- **THEN** its bar and named signals MUST come from the snapshot's `completeness` object verbatim
- **AND** doxBench MUST NOT compute, adjust, or re-weight any signal

#### Scenario: The source pass-through is absent
- **WHEN** doxBench runs against a served static image with no `/source` route
- **THEN** the docs and lens context MUST still render from the snapshot
- **AND** the canvas MUST report unavailable source content inline and MUST NOT expose editing or chat

#### Scenario: A scope carries no outline
- **WHEN** the opened tile has no outline material
- **THEN** the canvas MUST render an explicit empty state for the `outline` buffer rather than fabricating or drafting one
- **AND** only a capable local human console MAY offer a create-backed outline buffer

#### Scenario: A human edits before a session exists
- **WHEN** a capable local human edits any buffer with no active branch session
- **THEN** the edit MUST remain browser-local and available to the next chat turn
- **AND** the served checkout and every shared surface MUST remain unchanged

#### Scenario: An existing document is saved
- **WHEN** a human saves an existing eligible buffer from doxBench
- **THEN** `edit-document` MUST persist it on the tile's branch session as that action's single commit
- **AND** the served checkout MUST remain untouched

#### Scenario: doxBench renders without gate or model capability
- **WHEN** doxBench runs on a surface where gate and model capabilities are absent
- **THEN** docs/lens and available source content MUST remain readable
- **AND** no editing, chat, Apply, Save, Cancel, load, share, or other write-implying control MUST be reachable

#### Scenario: doxBench is used on a narrow viewport
- **WHEN** the three desktop regions cannot remain usable side by side
- **THEN** the same context, authoring canvas, and chat regions MUST stack without losing state, labels, keyboard reachability, or focus order

#### Scenario: The docs context presents its documents as a split
- **WHEN** a human opens doxBench's `docs` context on any topic-bearing tile
- **THEN** the pane MUST render a per-document abstract region above and a single-reel document wheel below
- **AND** selecting a wheel tile MUST make that document the abstract region's subject

#### Scenario: The abstract region re-presents and never recomputes
- **WHEN** the abstract region renders a document the snapshot scores
- **THEN** its score and named signals MUST be the snapshot's `completeness` object verbatim
- **AND** doxBench MUST NOT compute, adjust, or re-weight any signal

#### Scenario: The lens context is presented in three sections
- **WHEN** a human opens the `lens` context on a topic-bearing tile
- **THEN** the keyword rail, the bullseye, and the flat matrix MUST each be a named, always-reachable section of one tablist

#### Scenario: A model-derived artifact is admitted beside the snapshot's own
- **WHEN** the docs context renders a model-derived abstract for a document
- **THEN** it MUST be presented beside the snapshot-derived material with its own caption, never merged into it
- **AND** it MUST feed no completeness score, no staged-topic aggregate, no readiness tier, and no gate

#### Scenario: The no-new-analysis clause is read against the bullseye
- **WHEN** the no-new-analysis clause is applied to a derivation
- **THEN** it MUST govern the bullseye's geometry and the completeness signals
- **AND** it MUST NOT be read as forbidding an artifact this capability's own requirements govern

## ADDED Requirements

### Requirement: The model-derived distilled document abstract
The `docs` context SHALL offer a MODEL-DERIVED distilled abstract of ONE subject document, declared as a layer-2-class sibling artifact — lossy by design, non-authoritative, and regenerable from the document — and it MUST NOT become authoritative by being cached, rendered, copied, or projected. The abstract's SUBJECT SHALL be the document the docs wheel has selected, which is a reading selection and never a buffer, and the bytes described SHALL be the SAVED file's content: where the subject is also a loaded buffer with unsaved edits, the abstract SHALL be captioned as describing the saved version, and unsaved buffer text MUST NOT be sent to any provider. The subject SHALL be drawn from the scope projection's EDITABLE path set, honouring the surface's standing rule that disclosure requires edit authority; where a pointed-at document is readable but not editable, the region SHALL state honestly that no distillation is available for it rather than generating one, and a realization MUST NOT widen the disclosure set to reach a subject. The deterministic snapshot-derived abstract SHALL remain present, separately captioned, and SHALL be the region's default, because it is the one that exists before any model runs. The model-derived abstract SHALL feed no completeness score, no staged-topic health aggregate, no readiness tier and no gate, and SHALL NOT be promotable except by a human creating a new document through an existing gate verb.

#### Scenario: A subject is readable but not editable
- **WHEN** the wheel's selected document is in the scope's context paths but not its editable paths
- **THEN** the region MUST state that no distillation is available for that document
- **AND** no provider MUST be reached and the disclosure set MUST NOT be widened

#### Scenario: The subject is a dirty loaded buffer
- **WHEN** the subject document is loaded and its buffer carries unsaved edits
- **THEN** the abstract MUST describe the SAVED content and MUST be captioned as describing the saved version
- **AND** the unsaved buffer text MUST NOT be sent to any provider

#### Scenario: A reader wants the document's own account
- **WHEN** the abstract region opens on any subject
- **THEN** the deterministic snapshot-derived abstract MUST be the default view
- **AND** the model-derived abstract MUST be separately captioned wherever it is shown

### Requirement: Abstract generation is explicitly invoked and never a side effect of selection
Generation of a model-derived abstract SHALL be invoked EXPLICITLY by a human control acting on the currently selected subject, and MUST NOT be triggered by a selection change, a mount-time seed, a scope opening, or any other side effect — the docs wheel notifies its consumer on every notch and at mount, so a selection-triggered design would dispatch a model call for every document a reader spins past. An in-flight generation SHALL be cancellable and SHALL state the expected wait with THE ADAPTER'S OWN DECLARED TIMEOUT as its visible bound — the value the adapter reports, not the contract's maximum, which is a validated ceiling and not a prediction. A RE-GENERATE control SHALL be offered against the subject's current content digest, and invoking it SHALL carry an EXPLICIT REFRESH INTENT that bypasses the abstract cache's completed-entry replay as that cache's own requirement specifies — without it the control would be inert whenever content and model are unchanged, which is the ordinary case a reader invokes it in. Every generation SHALL carry the subject path, the content digest, and the RESOLVED MODEL ID it was generated for, and WHEN a SUCCESSFUL generation resolves against a subject the pane no longer has selected, the result MUST be discarded unrendered and uncached and the not-yet-generated caption MUST show for the current subject; a REFUSAL or an ERROR answering the subject the request was DISPATCHED for SHALL be recorded against THAT subject and rendered on it when it is next shown — a refusal carries no prose, so it is the one answer that cannot paint a wrong document, and dropping it left an invoked control looking like one that did nothing — and MUST NOT be rendered against any other subject, while any answer NAMING A DIFFERENT subject than the one dispatched MUST be discarded whole and recorded against neither. Where the subject's content has moved past the digest an abstract was generated from, the abstract SHALL BE SHOWN AND LABELLED STALE with its source digest stated, and MUST NOT be silently discarded, silently refreshed, or presented as current; a regeneration in flight SHALL show the in-flight state over it. The SOURCE DIGEST for an unloaded subject SHALL be the digest of the SERVED SAVED CONTENT, and the per-buffer settled-content-identity guard SHALL be escalated to only where the subject is also a loaded buffer — most wheel subjects have no buffer, and a per-buffer rule applied to them would have nothing to compare. An abstract already generated in the session SHALL survive leaving and re-entering the tile, keyed by subject path, content digest and resolved model id, so returning to a document does not spend a second call on an answered question — and a re-entry SHALL carry NO refresh intent, because a reader coming back to a document has asked for nothing. Where the gate capability is absent on the local console, the generation control SHALL be ABSENT rather than present-and-refusing, and any already-generated abstract SHALL remain readable with its normal caption.

#### Scenario: A human spins the docs wheel
- **WHEN** a human moves the docs wheel across N documents
- **THEN** no model dispatch MUST occur

#### Scenario: A slow generation resolves after the subject changed
- **WHEN** a generation resolves and the pane's selected subject is no longer the subject it was dispatched for
- **THEN** a SUCCESSFUL result MUST be discarded unrendered and MUST NOT be cached
- **AND** the region MUST show the not-yet-generated caption for the current subject
- **AND** a REFUSAL or ERROR answering the DISPATCHED subject MUST be recorded against that subject and rendered on it when it is next shown, and MUST NOT be rendered against any other subject
- **AND** a result NAMING A DIFFERENT subject than the one dispatched MUST be discarded whole, recorded against neither subject

#### Scenario: A generation is in flight
- **WHEN** a generation has been invoked and has not resolved
- **THEN** the region MUST show a cancellable in-flight state stating the expected wait bounded by the adapter's OWN declared timeout
- **AND** the stated bound MUST NOT be the contract's validated maximum where the adapter declares something shorter

#### Scenario: The subject has moved past the abstract's digest
- **WHEN** the subject document's content no longer matches the digest its abstract was generated from
- **THEN** the abstract MUST be shown, labelled stale, with its source digest stated
- **AND** it MUST NOT be silently discarded or presented as current

#### Scenario: An unloaded subject's digest is taken
- **WHEN** the subject is a document that is not a loaded buffer
- **THEN** the source digest MUST be the digest of the served saved content
- **AND** the per-buffer settled-content-identity guard MUST NOT be required of it

#### Scenario: The RE-GENERATE control is invoked on an already-generated abstract
- **WHEN** a human invokes RE-GENERATE on a subject whose abstract is already completed for the current content digest and resolved model
- **THEN** the request MUST carry refresh intent and a second dispatch MUST occur
- **AND** the completed entry MUST NOT be replayed as the answer

#### Scenario: The gate capability is absent
- **WHEN** the docs context renders on a local console without the gate capability
- **THEN** the generation control MUST be absent rather than present-and-refusing
- **AND** any already-generated abstract MUST remain readable

### Requirement: The abstract request carries exactly one subject document
An abstract request SHALL carry EXACTLY ONE subject document's content and MUST NOT carry the layer-one context packet, another buffer, another document, a transcript, or a human message — with no human message in the prompt, the subject document's own content is the entire instruction-bearing text, and every additional document is both an injection surface and a disclosure the request has no reason to make. The request SHALL be assembled by its own non-chat assembler and MUST NOT be expressed as a chat turn: the chat assembler requires an outline buffer, one or more document buffers, a non-blank human message, a working subject and a transcript, none of which an abstract request has. The assembled prompt SHALL be BYTE-IDENTICAL for identical construction input, so a prompt is reviewable and a dispatch is reproducible. The response bound SHALL be tighter than the chat surface's assistant-prose ceiling, because the region that renders it is a fixed-height pane and an abstract that overflows it is not an abstract. Provider-bound content MUST NOT include a credential, a raw endpoint, a secret name, or unsaved buffer text.

#### Scenario: A request would carry the context packet
- **WHEN** a bounded context packet of ANY declared purpose, or any second document, is handed to the abstract assembler
- **THEN** the assembler MUST refuse it before any provider is reached
- **AND** the refusal MUST NOT depend on the packet's declared purpose, because an abstract request carries no packet at all

#### Scenario: The same subject is assembled twice
- **WHEN** the same subject document, content digest and model are assembled twice
- **THEN** the rendered prompt bytes MUST be identical

#### Scenario: An abstract request is offered as a chat turn
- **WHEN** an abstract request would be dispatched through the chat-turn assembler
- **THEN** it MUST be rejected — the request carries its own assembler and its own declared shape

### Requirement: The distilled abstract is verified against the document's own declared fields
A returned abstract SHALL be verified before it is rendered, and the verification base SHALL be the SNAPSHOT'S OWN declared fields for the subject document — its declared topics and its declared destinations — so the rule fires on the FIRST generation and not only on a regeneration; a previously generated abstract, where one exists, SHALL be an ADDITIONAL base and never the only one. The declared-field check SHALL be described as SUBJECT-MENTION COVERAGE and MUST NOT be described as a fidelity or faithfulness check, because a provider returns assistant prose as one opaque string and nothing downstream can establish that a mentioned subject was treated faithfully; a realization that claims otherwise MUST be rejected. The abstract SHALL name the subject document's path or title, and MUST NOT name any repository path absent from its own request — this is the one structural clause the response bytes can decide, and it refuses both a wrong-document answer and a leaked-neighbour answer. A verification failure SHALL be a stated refusal that renders no abstract, and MUST NOT be silently downgraded to rendering the unverified text. The verified artifact SHALL be structurally non-authoritative and SHALL record what it is regenerable from, in the manner of this surface's existing compacted-artifact type, and it MUST NOT reuse that type where that type's own commitment classes do not apply. The artifact SHALL also record the SUBJECT PATH, the SUBJECT CONTENT DIGEST and the RESOLVED MODEL ID it was produced from, and the recorded model id MUST be the model that actually answered — which is why those three are also the cache key, since a store that replayed one model's prose under another model's recorded id would make the artifact lie about its own provenance.

#### Scenario: An abstract mentions none of the declared subjects
- **WHEN** a returned abstract mentions no declared topic and no declared destination of its subject document
- **THEN** it MUST be refused and no abstract MUST be rendered

#### Scenario: An abstract names a foreign path
- **WHEN** a returned abstract names a repository path that its own request did not carry
- **THEN** it MUST be refused as a wrong-document or leaked answer

#### Scenario: Coverage is described as fidelity
- **WHEN** a realization or its documentation describes the declared-field check as verifying faithfulness
- **THEN** it MUST be rejected — the check is subject-mention coverage over one opaque string

#### Scenario: The first generation is verified
- **WHEN** the first abstract for a document is returned and no previous abstract exists
- **THEN** it MUST still be verified against the snapshot's declared topics and destinations

### Requirement: A model-derived abstract is session-local and never a snapshot field
A model-derived abstract SHALL be session-local and MUST NOT be written into the dashboard snapshot for as long as the snapshot's byte-identical guarantee stands, because keying a model value by content digest makes a CACHE stable and does not make a TREE reproducible — a cold cache, a substituted adapter, or a provider revision all change the bytes while the working tree does not. The observable SHALL hold in BOTH directions: an emitted snapshot MUST be byte-identical whether or not any abstract was generated, and no snapshot field MUST carry a model-derived value. Generation MUST NOT block, delay, or fail a snapshot, a publication lane, or a gate action; where the port raises, times out, or is absent, the snapshot MUST be unaffected and the region MUST state the not-yet-generated caption. On the hosted read-only plane, where no model-consuming route is offered, the region SHALL render the deterministic abstract and state that no distillation is available ON THAT PLANE — a statement about the plane and never about the document. Projecting an abstract into the snapshot in future SHALL require its own change amending the byte-identical scenario first, and MUST NOT be treated as an additive growth this requirement already permits.

#### Scenario: The generator runs on a tree with and without generation
- **WHEN** the generator runs over an unchanged working tree, once with abstracts generated in the session and once without
- **THEN** both snapshots MUST be byte-identical
- **AND** no snapshot field MUST carry a model-derived value

#### Scenario: The provider is absent or fails
- **WHEN** the model port is absent, raises, or exceeds its timeout
- **THEN** the snapshot MUST be unaffected and no lane or gate action MUST fail
- **AND** the region MUST state the not-yet-generated caption

#### Scenario: The hosted plane renders the docs context
- **WHEN** a viewer opens the docs context on the hosted read-only plane
- **THEN** the deterministic abstract MUST render and the region MUST state that no distillation is available on that plane

### Requirement: The abstract cache is a separate bounded store keyed by path, digest and model, and an explicit refresh bypasses it
An abstract cache SHALL be a SEPARATE, separately bounded store and MUST NOT share the chat surface's turn-idempotency ledger, whose per-process instance is bounded by entry count and total bytes and would evict chat records under abstract churn — a scope larger than that bound is the ordinary case, not an edge case. The cache key SHALL be composed of the subject's PATH, its CONTENT DIGEST, and the RESOLVED MODEL ID the request dispatched against, QUALIFIED BY the request's SCOPE — its REPOSITORY and REF — so no key is ever shared across scopes. The digest MUST be in the key so a regeneration after an edit is a NEW key rather than a same-key conflict; a store that refused a changed digest under an unchanged key would refuse every regeneration after every edit. The RESOLVED MODEL ID MUST be in the key because this surface lets a human change the selected model while the document stands still: on a path-and-digest key that second request is identical, so the first model's answer would replay while the artifact records the newly selected model — a claim the artifact's own recorded model id makes false on its face, and one the provider boundary's rule that every consumer resolves a catalog model id forbids. Where the selected entry is a ROUTING RULE rather than a single provider model, the key SHALL carry the RESOLVED model id and not the rule's id, for the same reason a turn records the model that actually answered. The cache SHALL admit at most ONE in-flight generation per key, with a concurrent request for the same key attaching to it rather than dispatching a second time. A request carrying NO REFRESH INTENT SHALL replay a completed result for an identical key without a second dispatch — this is the path that makes an abstract survive leaving and re-entering the tile. A request carrying an EXPLICIT REFRESH INTENT — which is what the RE-GENERATE control issues — SHALL BYPASS completed replay: it SHALL invalidate the completed entry for its key, dispatch again, and its result SHALL replace that entry. Without that bypass the RE-GENERATE control would be INERT for the ordinary case it exists for, because a regeneration against unchanged content and an unchanged model has an identical key. A refresh intent MUST NOT open a second in-flight generation where one is already in flight for the same key: a second invocation attaches to the first, so an impatient double-click spends one model call and not two, and refresh intent MUST NOT be inferred from a selection change, a mount, a re-entry, or any other event that is not the human control being invoked. Eviction SHALL be deterministic and MUST NOT be ordered by wall-clock time, and a re-dispatch after eviction SHALL be stated expected behaviour rather than an error. Nothing in the cache SHALL be authoritative, and its contents MUST NOT outlive the session or be written to any corpus, snapshot, register, or gate artifact.

#### Scenario: Abstract churn over a large scope
- **WHEN** abstracts are generated across a scope holding more documents than the cache bound
- **THEN** eviction MUST be deterministic and re-dispatch after eviction MUST be expected behaviour
- **AND** the chat surface's turn-idempotency records MUST NOT be evicted by abstract activity

#### Scenario: The subject is edited and regenerated
- **WHEN** a subject document changes and an abstract is requested again
- **THEN** the request MUST be treated as a new key rather than refused as a conflict

#### Scenario: Two requests race for one subject
- **WHEN** a second request arrives for a key whose generation is in flight
- **THEN** it MUST attach to the in-flight generation rather than dispatching a second time

#### Scenario: RE-GENERATE is invoked on an unchanged document with an unchanged model
- **WHEN** a human invokes the RE-GENERATE control and neither the subject's content digest nor the resolved model has changed since the completed entry
- **THEN** the completed entry MUST be invalidated and a second dispatch MUST occur
- **AND** the new result MUST replace that entry rather than being discarded as a duplicate

#### Scenario: RE-GENERATE is invoked twice before the first resolves
- **WHEN** the RE-GENERATE control is invoked a second time while its own generation is still in flight for the same key
- **THEN** the second invocation MUST attach to the in-flight generation rather than dispatching a third time

#### Scenario: The selected model changes while the document stands still
- **WHEN** an abstract is requested for a subject whose content digest is unchanged but whose resolved model id differs from the completed entry's
- **THEN** it MUST be treated as a DIFFERENT key and MUST dispatch against the newly resolved model
- **AND** the first model's result MUST NOT be replayed under the new model's identity

#### Scenario: Re-entering the tile is not a refresh
- **WHEN** a reader leaves the tile and returns to a subject whose abstract is already generated, with no control invoked
- **THEN** the completed result MUST replay with no second dispatch
- **AND** refresh intent MUST NOT be inferred from the re-entry

### Requirement: One abstract region, named for its subject and its provenance
The `docs` context SHALL carry EXACTLY ONE abstract region, presenting ONE abstract at a time — switched by an explicit control, opening on the DETERMINISTIC one — because the upper half of the docs split carries a measured fixed height that two regions cannot share and the deterministic abstract is the only one that always exists. That region's ACCESSIBLE NAME SHALL be composed of the SUBJECT's title or path together with the provenance caption of the state currently shown, so a reader using assistive technology can tell WHICH DOCUMENT and WHICH PROVENANCE they have landed on from the name alone, and the deterministic and model-derived states are distinguishable without reading the body. The region MUST NOT be named `selected document` or otherwise announced as the selected buffer: that name belongs to the loaded-document selector, and two surfaces claiming one name is how the two come to disagree. Each state SHALL carry its own caption declaring who derived it and what it is not — the model-derived abstract as model-derived, non-authoritative and regenerable; the deterministic abstract as derived from the document's own headers, and NEVER as a distillation; a stale abstract as describing an earlier version, with the source digest stated; an ungenerated abstract as not yet generated; and, on the hosted plane, as unavailable on that plane. The model-derived and deterministic captions SHALL be BOTH visible text and part of the region's accessible name; the stale, ungenerated and hosted-plane captions SHALL be visible text inside the already-named region. The region SHALL follow this surface's established idiom — a named `role=region` carrying no heading of its own, in the surface's exact casing. No caption SHALL describe the model-derived abstract in terms that imply it may be cited.

#### Scenario: Both abstracts exist for one subject
- **WHEN** a subject has both a deterministic and a model-derived abstract
- **THEN** exactly ONE abstract region MUST exist and exactly one abstract MUST render at a time, switched by an explicit control
- **AND** the deterministic abstract MUST be the opening view

#### Scenario: A reader lands on the region with assistive technology
- **WHEN** a reader enters the abstract region with assistive technology
- **THEN** the region's accessible name MUST carry both the subject's identity and the provenance of the state shown
- **AND** it MUST NOT be announced as the selected document

#### Scenario: The provenance state changes
- **WHEN** the region switches between the deterministic and the model-derived abstract for one subject
- **THEN** the accessible name MUST change with it, so the two states are distinguishable by name

#### Scenario: A caption implies citability
- **WHEN** a caption describes the model-derived abstract as a summary of record, an authoritative account, or otherwise citable
- **THEN** it MUST be rejected
