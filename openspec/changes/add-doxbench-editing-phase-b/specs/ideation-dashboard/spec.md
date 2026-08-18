# ideation-dashboard

Three MODIFIED requirements below — `The doxBench chat binds to the active
buffer selection`, `The canvas view surface is expressed over the buffer set,
not over two names`, and `One Save and one Cancel govern the doxBench canvas` —
amend requirement text that `add-doxbench-editing-phase-a` ADDED and that has
not promoted yet. They are declared relative to Phase A's OUTCOME per
`release-realization`'s ordered-deltas rule: Phase A's spec text promotes
first, then these amendments apply to it. The other five MODIFIED requirements
amend text already promoted.

## MODIFIED Requirements

### Requirement: doxBench editor buffer contract
The local doxBench surface SHALL maintain a KEYED BUFFER SET for its canvas — the permanently reserved `outline` key plus one key per LOADED document — and each buffer SHALL carry its kind, repository-relative path or `null` for a not-yet-created artifact, repository, base ref, base source revision, base content hash, current content hash, current text, and dirty state. A document buffer's key SHALL be its repository-relative path, so a document can be loaded at most once and no two buffers can claim the same file; at most ONE unbacked document buffer MAY exist, under the reserved key `document`, which is the not-yet-created artifact of the existing create flow and SHALL be re-keyed to its path when its first Save gives it one. The outline buffer SHALL be seeded from the opened scope's declared outline material when one exists and MUST NOT be fabricated from any document's headings; a document buffer SHALL be seeded from the document the human loaded or from the existing create-document flow. Editing any buffer MUST be a browser-local, reversible action that writes no corpus document, snapshot, register, workbench manifest, gate artifact, or branch until the human invokes Save. Save SHALL compare current and base hashes, persist a new path through `create-document` and an existing path through `edit-document`, preserve each verb's existing validation and authority boundary, and refresh/rebase each successfully saved buffer from the resulting session ref and source revision. Save ordering SHALL be an explicit rule rather than a fixed list: the `outline` buffer SHALL be persisted FIRST when it is dirty, because its commit establishes the session ancestry the document commits descend from; every dirty document buffer SHALL then be persisted in a DETERMINISTIC order the realization declares, each through its own existing gate action as one commit; and a dirty outline that did not land SHALL stop every document with a stated `not_attempted` verdict. One document's refusal SHALL NOT stop another document, because documents carry no ancestry dependency on each other and reporting one refusal as the cause of untried work is a false statement about both. Save MUST NOT invent a multi-document write verb, rewrite history, or hide partial success, and every buffer it acted on SHALL report its own verdict. Discard SHALL restore the last loaded/saved base content of the buffer it names and MUST persist nothing.

#### Scenario: A human edits the outline before chatting
- **WHEN** a human changes the outline buffer without invoking Save
- **THEN** the canvas MUST show the outline as dirty
- **AND** no corpus file, branch, snapshot, register, manifest, or gate record MUST change

#### Scenario: A second document is loaded
- **WHEN** a human loads a second document while the first is still loaded and dirty
- **THEN** both document buffers MUST exist under their own path keys with their own dirty state and their own base identity
- **AND** loading the second MUST NOT replace, discard, or flush the first

#### Scenario: A document already loaded is loaded again
- **WHEN** a human invokes the load verb on a document the loaded set already holds
- **THEN** that existing buffer MUST become the selected one and MUST NOT be reloaded from source, because reloading would silently discard its unsaved text

#### Scenario: A scope has no outline
- **WHEN** the opened scope declares no outline material
- **THEN** the outline buffer MUST show an explicit empty state
- **AND** it MAY offer a new outline buffer whose first persistence uses `create-document`, but it MUST NOT fabricate or persist an outline merely by being opened

#### Scenario: Several dirty documents are saved
- **WHEN** the human invokes Save with a dirty outline and three dirty documents
- **THEN** the outline action MUST run first and each changed document MUST then produce its own existing gate-action commit in the declared deterministic order
- **AND** no combined or hidden write verb MUST be introduced

#### Scenario: One document's save refuses
- **WHEN** the outline commits, the first document commits, and the second document's save refuses
- **THEN** the third document MUST still be attempted, because it descends from the same ancestry and the refusal was not about it
- **AND** the report MUST name the committed, refused, and remaining buffers separately

#### Scenario: The outline's save refuses
- **WHEN** the outline is dirty and its save refuses
- **THEN** every dirty document MUST be reported `not_attempted` with the missing-ancestry reason and MUST NOT be sent
- **AND** every buffer's text, base, and dirty state MUST be preserved exactly

#### Scenario: An unbacked document buffer is first saved
- **WHEN** the reserved unbacked document buffer is persisted through `create-document` and the server reports the path it created
- **THEN** that buffer MUST be re-keyed from the reserved key to its path
- **AND** the reserved key MUST become available for a later create without carrying anything from the buffer that left it

#### Scenario: A human discards local edits
- **WHEN** the human invokes Discard on a dirty buffer
- **THEN** that buffer MUST return to its last loaded or saved base content and no other buffer MUST change
- **AND** no gate action or provider call MUST occur

### Requirement: Grounded doxBench chat turn
The local human-console doxBench surface SHALL offer a chat rail containing a `Working subject` field, the loaded-document selector, transcript, server-declared model selection, and message composer. Each submitted turn SHALL use a versioned `workbench-chat-turn` request containing the repository/ref and tile scope, the BOUND BUFFER's key, `working_subject`, the new user message, the bounded prior transcript, the selected model id, a client-generated turn id, and the complete current descriptors and text of the outline buffer and of every loaded document buffer including their hashes. The server MUST independently resolve and confine the repository/ref, the tile, and every supplied buffer path before a provider call; MUST verify every declared content hash; MUST refuse a request whose bound-buffer key names no supplied buffer; and MUST record in the response the exact per-buffer hashes, the bound buffer's key, the model id, and the turn id used. The turn RECORD SHALL name the buffer the turn was bound to, so a transcript read later says which material the conversation was working on — Phase A deferred this because the released envelope had no room for it, and this capability's contract release discharges that obligation rather than substituting a server-side-only field no reader can consult. The response SHALL echo the model that answered together with the selected-model metadata the contract release carries, so a transcript states which model produced which turn rather than leaving it to be inferred. Unsaved buffer text SHALL be eligible turn input and MUST be labelled as working state rather than governed or committed content. Per-turn context SHALL be assembled as this capability's bounded context packet and MUST NOT be assembled by concatenating whatever the browser happened to send. The next turn SHALL use the buffer contents and thread state that exist when that next turn is submitted, including intervening human edits and locally applied AI proposals, rather than reusing a previous turn's text. The request/response schemas SHALL impose explicit byte, buffer-count, transcript-turn, and output bounds; an over-bound turn MUST refuse with the applicable measured limit and MUST NOT silently truncate, summarize, or omit any buffer. Exactly one turn MAY be in flight per browser conversation key. Within one server process the client turn id SHALL be idempotent: a repeated completed id with identical input hashes SHALL return the recorded result without another provider dispatch, an in-flight repeat SHALL attach to or report that turn, and reuse with different content or hashes MUST refuse. A provider or response-validation failure MUST return a fixed redacted error, preserve every buffer, append no assistant proposal, and disclose no credential, raw provider response, prompt, document content, thread content, or unsaved text in logs or error details.

#### Scenario: A turn is bound to one of several loaded documents
- **WHEN** four documents are loaded and the human sends a message with the third selected
- **THEN** the request MUST name that buffer's key as the bound buffer and MUST carry the outline and all four documents with their hashes
- **AND** the completed turn's durable record MUST name that same bound buffer

#### Scenario: A turn names a bound buffer it did not supply
- **WHEN** a request's bound-buffer key names no buffer in its own buffer set
- **THEN** the route MUST refuse before any provider call, exactly as the existing active-path revalidation does

#### Scenario: A human edit feeds the next turn
- **WHEN** a human edits any loaded buffer after one assistant response and submits another message
- **THEN** the new request MUST carry that buffer's edited current text and hash
- **AND** the response MUST identify that hash as the content the model saw

#### Scenario: Unsaved edits are discussed
- **WHEN** a dirty buffer is included in a chat turn
- **THEN** the model MAY use that exact unsaved text
- **AND** neither the request nor the response MUST represent the text as committed, governed, or present on `main`

#### Scenario: The route receives a mismatched path or hash
- **WHEN** a turn names a path outside the opened tile's allowed scope, a repository/ref other than the active binding, or a hash that does not match the supplied text
- **THEN** the route MUST refuse before any provider call
- **AND** no browser conversation state or corpus state MUST be persisted by the server

#### Scenario: A turn exceeds a declared limit
- **WHEN** the combined buffers, transcript, assembled packet, message, or requested output exceed the selected catalog entry's or route's limit
- **THEN** the route MUST refuse and name the exceeded dimension and limit
- **AND** it MUST NOT silently truncate or send a partial document to the provider

#### Scenario: A turn completes
- **WHEN** the provider returns a valid response for the exact request
- **THEN** the chat rail MUST append assistant prose and any typed proposals under one turn id, into the SELECTED document's thread
- **AND** focus, the selected document, the active view tab, editor selection, scroll position, and every buffer's dirty state MUST remain usable

#### Scenario: A completed turn is retried
- **WHEN** the same client turn id is submitted again in the same server process with identical content and hashes
- **THEN** the recorded result MUST be returned without a second provider dispatch

#### Scenario: A turn id is reused for different content
- **WHEN** a client turn id is repeated with different buffer text, hashes, bound buffer, subject, message, or model
- **THEN** the server MUST refuse the idempotency conflict before any additional provider call

#### Scenario: A provider or response validation fails
- **WHEN** the provider call fails or its response violates the typed response schema
- **THEN** every editor buffer MUST remain byte-identical and no assistant proposal MUST be appended
- **AND** the UI MUST receive a fixed actionable failure while logs and response details reveal no credential, raw provider payload, prompt, document content, thread content, or unsaved text

### Requirement: Typed AI proposals and stale-application protection
A workbench chat response MAY contain ordinary assistant prose and zero or more typed edit proposals, and each proposal SHALL name exactly one target BUFFER KEY drawn from the request's own supplied buffer set, carry complete proposed content, identify that buffer's input `base_hash`, and include a human-readable summary. A proposal naming a key the request did not supply MUST be refused as unroutable rather than guessed at, and two proposals MUST NOT name the same key in one response. The number of proposals in one response SHALL be bounded by the contract, and the bound SHALL be expressed over the request's buffer count rather than a fixed pair, so widening the loaded set does not silently widen what one response may rewrite beyond what it was grounded on. A provider response MUST NOT write, save, commit, create, delete, or apply any document by itself. The browser SHALL render Apply only for schema-valid typed proposals. Applying a proposal SHALL replace only the named browser buffer, mark it dirty, remain locally reversible, and MUST NOT invoke Save or any gate action. Immediately before Apply, the browser MUST recompute the target buffer hash and compare it with the proposal's `base_hash`; a mismatch MUST refuse as stale and offer inspection of current versus proposed content or a new turn, but MUST NOT silently merge or expose an authority-bypassing force-apply action. Chat prose without a typed proposal MUST NOT be inferred as replacement content.

#### Scenario: An AI proposes a revision to the selected document
- **WHEN** a valid response proposes content for the bound document's key against that buffer's current hash
- **THEN** the human MAY apply it to that buffer
- **AND** the buffer MUST become dirty while the corpus and branch remain unchanged until Save

#### Scenario: A proposal targets a buffer that was not sent
- **WHEN** a response names a buffer key absent from the request's buffer set
- **THEN** that proposal MUST be refused as unroutable and MUST NOT be rendered with an Apply control

#### Scenario: Two proposals name one buffer
- **WHEN** one response returns two proposals against the same buffer key
- **THEN** the response MUST be refused rather than applied in an arbitrary order

#### Scenario: Human work makes a proposal stale
- **WHEN** the human changes the target buffer after the turn was issued and then invokes Apply
- **THEN** Apply MUST refuse because the current hash differs from the proposal base hash
- **AND** the current human text MUST remain unchanged

#### Scenario: A provider returns prose that looks like a document
- **WHEN** assistant prose contains Markdown but no schema-valid typed proposal
- **THEN** the UI MUST render it as conversation only and MUST NOT offer or perform document replacement

#### Scenario: An applied proposal is saved
- **WHEN** the human reviews an applied proposal, optionally edits it, and invokes Save
- **THEN** persistence MUST occur only through the applicable existing create/edit gate action
- **AND** the saved gate record MUST attest to the human action, not claim that the provider held write authority

### Requirement: doxBench scoped view
The dashboard SHALL provide doxBench as the named evolution of the staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — with three coordinated regions over that scope. A context region SHALL retain `docs` and `lens`: `docs` SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it, plus — Brett's 2026-07-25 dogfood ruling — the member documents of the topic's linked clusters as a THIRD, separately labelled cluster-neighbourhood section, inherited via clusters, never conflated with the topic's own material, and never an input to the topic's health or the readiness gate, which stay folder-scoped) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them; `lens` SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. The `docs` context's expanded tile SHALL offer this capability's three document verbs — read, load-for-editing, and save — as specified by their own requirement. An authoring canvas SHALL present exactly ONE buffer at a time — the SELECTED buffer of the loaded set — and the SELECTION SHALL be made outside the canvas rather than by the canvas: the context region's `outline` selection tab SHALL select the `outline` buffer, loading a document SHALL select that document, and the chat rail's loaded-document selector SHALL select among the loaded documents. The `outline` buffer SHALL load the topic's declared outline material when one exists — for a staged topic, the fragment's outline material — and a document buffer SHALL load the exact document the human loaded; the canvas SHALL provide browser-local editing plus live rendered Markdown preview of the SELECTED buffer on the local human console, presented as this capability's Editor/Preview view-tab pair rather than as a side-by-side split pane, while an absent outline remains an explicit empty/create state rather than fabricated content. The canvas MUST NOT render a second buffer-selection tablist beside the selection surfaces the context region and the chat rail own, because two controls answering one question is how the two come to disagree. A chat region SHALL contain Working subject, the loaded-document selector, transcript, server-declared model selection, and composer, and SHALL ground turns on the current canvas buffers and this capability's bounded context packet as specified by this capability. doxBench's corpus write authority SHALL remain the human-only gate verbs `create-document`, `edit-document`, `open-pr`, session share, and session abandon: buffer edits, chat turns, thread writes, and AI Apply MUST write no corpus document, register entry, workbench manifest, snapshot, or gate artifact; Save MAY materialize/join a branch session and invoke only create/edit as specified; no verb MAY delete a document; and no session write may touch the served checkout. With the gate/model capabilities absent or on the hosted plane, the context SHALL remain usable and doxBench SHALL render read-only outline/document content without reachable editing, chat, threads, or write controls.

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

### Requirement: doxBench model catalog and provider boundary
The dashboard backend SHALL expose a same-origin workbench model catalog whose entries carry a stable opaque model id, human label, provider class, input/output limits, availability, and a human-readable data-handling badge. The catalog MUST NOT expose a provider credential, raw secret, raw endpoint, secret environment-variable name, or provider request template, and the browser MUST NOT call any model provider directly. A chat turn SHALL accept only a model id present and available in the current catalog and SHALL resolve that id through a server-side injected model-provider port whose member surface SHALL remain exactly the three declared members — the adapter-declared timeout, the catalog, and the single opaque dispatch — so that per-turn model selection, harness session handling, and any adapter-internal routing are performed INSIDE an adapter and MUST NOT be added as a fourth provider verb. A catalog entry MAY name a ROUTING RULE this capability owns rather than a single provider model — an `auto` entry that maps a turn to a model by declared role — and such an entry SHALL declare itself as a routing rule with the data-handling badge of the models it may route to, because an entry that hid a routing decision behind a model-shaped id would report a handling posture it does not control. Provider credentials MUST come only from the deployment's approved server-side credential mechanism and MUST NOT enter browser storage, a request body, response body, dashboard snapshot, chat transcript, thread file, log, gate record, git artifact, or exception detail; an adapter that reaches a hosted provider SHALL obtain its credential through the ratified broker lane and MUST NOT hold or read a raw secret of its own. A hosted fallback MAY be offered only when the deployment explicitly enables it and its configured data-handling policy meets the catalog badge; otherwise the model MUST be unavailable. The model catalog and turn routes SHALL be offered only on a loopback human console with a real checkout, resolved actor, and demonstrated console presence; the hosted/read-only plane MUST offer neither route.

#### Scenario: The browser loads model choices
- **WHEN** local doxBench opens with one or more allowed providers configured
- **THEN** the selector MUST show exactly the available catalog entries and their data-handling badges
- **AND** no credential or raw provider endpoint MUST be present in the page or catalog response

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

### Requirement: The doxBench chat binds to the active buffer selection
The doxBench chat SHALL take its working context from the SELECTED BUFFER of the loaded set and MUST NOT maintain a second, separately-chosen context beside it. Changing the selection SHALL change the chat's working context IMMEDIATELY, with no confirmation step, because changing which buffer is selected replaces no content and destroys nothing; the existing unsaved-edit guard SHALL be unchanged by this rule where it still applies, and it SHALL NOT be extended to selection, since a selection change no longer replaces any buffer's content once documents are held side by side rather than in one slot. Focusing the context region's `outline` selection tab SHALL put the chat in outline-editing context; selecting a loaded document in the chat rail's selector SHALL put the chat in that document's context. The chat SHALL STATE its current binding on the chat surface itself and SHALL make it SELECTABLE there, so which material a conversation is working on is both read and chosen where the conversation happens. Naming the bound buffer inside a turn's durable RECORD SHALL now be CARRIED rather than deferred: Phase A recorded the obligation against the buffer-set widening that next releases the chat-turn contract, this capability performs that release, and the record SHALL therefore name the bound buffer's key. A server-side-only field that no reader can consult MUST NOT be accepted as a substitute for it, and the record MUST derive the bound buffer from the request's DECLARED binding rather than inferring it from which document happened to be supplied. This SHALL generalize the existing active-path revalidation rather than replace it: a turn whose declared binding does not match a supplied buffer MUST still refuse before any provider call. Binding SHALL govern what the chat is working ON and MUST NOT narrow what the turn may be grounded on — the turn continues to carry the outline and every loaded document the grounded-turn contract requires, plus the assembled context packet.

#### Scenario: The selection changes mid-conversation
- **WHEN** a human with an open conversation selects a different loaded document
- **THEN** the chat's working context MUST follow immediately and the chat MUST show that document's own thread
- **AND** no confirmation step MUST be required, because no content is replaced by the change

#### Scenario: The outline is selected
- **WHEN** the context region's `outline` selection tab is focused
- **THEN** a turn submitted next MUST be bound to the `outline` buffer
- **AND** the chat surface MUST state that binding, so the human can see which material the conversation is working on before they send

#### Scenario: A turn record is consulted for its bound buffer
- **WHEN** a reader consults a completed turn's durable record to learn which buffer that turn was bound to
- **THEN** the record MUST name it, carried on the released envelope this capability's contract release provides
- **AND** the named buffer MUST be the one the request DECLARED as bound, never one inferred from the supplied paths

#### Scenario: A turn's declared binding does not match its buffers
- **WHEN** a turn declares a binding that matches no buffer supplied under it
- **THEN** the route MUST refuse before any provider call, exactly as the existing active-path revalidation does

#### Scenario: Binding is mistaken for grounding
- **WHEN** any realization would use the binding to drop a buffer or a packet section the grounded-turn contract requires the request to carry
- **THEN** it MUST be rejected — binding names what the chat works on, not what it may see

### Requirement: The canvas view surface is expressed over the buffer set, not over two names
The view tabs, the canvas Save, the canvas Cancel, and the chat binding SHALL each be expressed over the capability's declared buffer set and its selected-buffer key, and MUST NOT hard-code any literal buffer name into their own structure. The view tabs render whichever buffer is selected and MUST NOT enumerate buffers; the canvas Save operates over the declared buffer set; Cancel operates on the selected-buffer key; the chat binds to the selected-buffer key. Phase A held this requirement WITHOUT widening the buffer set and required a realization that widened it to be rejected; that clause is now DISCHARGED, because the widening is exactly what this capability performs — in the buffer contract, the turn contract, and the save ordering rule, which are the three places that ever enumerated `outline` and `document`. The purpose of this requirement is unchanged and is now proven: widening the buffer set required changing those contracts and NOTHING on the view surface, and any FURTHER widening — a third buffer kind, a per-buffer view mode, a second selection surface — SHALL likewise be a change to the buffer contract alone. A realization that re-introduces a literal buffer name into the view tabs, the controls, or the binding MUST be rejected.

#### Scenario: A view surface names a buffer literally
- **WHEN** a realization builds the view tabs, Save, Cancel, or the chat binding around a literal buffer name
- **THEN** it MUST be rejected — these surfaces read the buffer set and the selected key

#### Scenario: The buffer set widens
- **WHEN** the buffer set grows from two buffers to the outline plus several loaded documents
- **THEN** the view tabs, the canvas Save, Cancel, and the chat binding MUST require no structural change to carry it
- **AND** the change MUST be confined to the buffer contract, the turn contract, and the save ordering rule

### Requirement: One Save and one Cancel govern the doxBench canvas
The doxBench authoring canvas SHALL carry exactly ONE Save control and exactly ONE Cancel control, placed outside both view tabs so that each control and its answer are on screen whichever view the human is standing on, and MUST NOT render a duplicate Save or Cancel per view tab or per buffer WITHIN THE CANVAS. A per-document Save on the context region's `docs` tile is NOT such a duplicate and SHALL be permitted: it lives on a different surface, is scoped to the document whose tile carries it, and reaches the same governed pipeline — one save mechanism with a second entry point, which is the opposite of a second save path. The canvas Save SHALL keep the semantics the editor buffer contract gives it — it persists every dirty backed buffer through the existing `create-document`/`edit-document` gate actions under that contract's ordering rule, as commit-per-gate-action on the tile's branch session, with `open-pr` remaining the separate promotion act. Save's verdict SHALL continue to be reported PER BUFFER, so a partial success across several documents remains separately readable. Cancel SHALL discard the SELECTED buffer back to its last loaded or saved base content and MUST NOT touch any other buffer, because discard destroys unsaved human work, has no cross-buffer dependency, and a single control that silently reverted a buffer the human is not looking at would be this surface's one irreversible surprise — a hazard that grows, not shrinks, as the loaded set grows. Neither control SHALL grant any authority the surface did not already hold: no force-save, no force-discard, no bypass of a refusal, and no second write route. Where the gate capability is absent, both controls SHALL state that absence as visible text beside them rather than only in a hover title, and MUST NOT be reachable.

#### Scenario: The canvas offers its controls
- **WHEN** doxBench mounts its authoring canvas
- **THEN** exactly one Save control and exactly one Cancel control MUST be present on the canvas, outside both view tabs
- **AND** no per-view-tab or per-buffer duplicate of either MUST be rendered inside the canvas

#### Scenario: The canvas Save is invoked with several buffers dirty
- **WHEN** a human invokes the canvas Save with the outline and two documents dirty
- **THEN** each changed document MUST persist through its existing gate action under the buffer contract's ordering rule
- **AND** the verdict MUST be reported per buffer, so a committed buffer and a refused buffer are separately readable

#### Scenario: Cancel is invoked with several documents loaded
- **WHEN** a human invokes Cancel while one of four loaded buffers is selected and dirty
- **THEN** only the selected buffer MUST return to its base content, and the other three MUST be untouched
- **AND** nothing MUST be persisted, committed, or dispatched

#### Scenario: A control is asked for authority it does not have
- **WHEN** any realization would add a force-save, a force-discard, a refusal bypass, or a second write route to either control or to the tile's Save
- **THEN** it MUST be rejected — an additional entry point MUST NOT widen what the act may do

#### Scenario: The gate capability is absent
- **WHEN** the canvas renders on a surface with no gate capability
- **THEN** Save MUST be unreachable and MUST state that absence as visible text beside it, not only in a hover title

## ADDED Requirements

### Requirement: The doxBench loaded set is the outline plus the documents the human loaded
The loaded set SHALL be exactly the `outline` buffer plus every document a human has LOADED through the `docs` tile's load verb, and no other route SHALL add a document to it — not a chat proposal, not a retrieval result, not the snapshot, and not an inherited edge. A document SHALL leave the loaded set only by an explicit human act, and that act MUST refuse or require an explicit discard while the buffer is dirty, because unloading a dirty buffer destroys unsaved work exactly as Cancel does. Membership SHALL be session-local working state: it MUST NOT be written into the snapshot, the register, the workbench manifest, or any generated projection, because "a human has this open right now" is a fact about a browser the generator cannot observe. A document the tile offers as READ-ONLY CONTEXT — an inherited, cluster-neighbourhood, cited, or inbound-context document that is not the tile's own editable material — MAY be loaded for grounding and for conversation, and its buffer SHALL carry that non-owned status so the governed Save withholds it with the stated context-only reason exactly as it does today; such a buffer MUST NOT be offered a reachable Save on its tile and MUST NOT be marked as needing one. The loaded set SHALL be bounded, and reaching the bound SHALL refuse the load with the measured bound stated rather than silently evicting a buffer that may hold unsaved work.

#### Scenario: A retrieval result is not a loaded document
- **WHEN** the knowledge service returns a document as evidence for a turn
- **THEN** that document MUST NOT join the loaded set, MUST NOT appear in the selector, and MUST NOT become an editable buffer
- **AND** the human MUST use the load verb if they want to edit it

#### Scenario: A dirty document is unloaded
- **WHEN** a human unloads a document whose buffer has unsaved edits
- **THEN** the unload MUST refuse or require an explicit discard, and MUST NOT silently drop the text

#### Scenario: A context-only document is loaded
- **WHEN** a human loads an inherited or cited document that is not this tile's own editable material
- **THEN** it MAY be loaded for grounding and conversation with its non-owned status carried on the buffer
- **AND** its tile MUST NOT offer a reachable Save and MUST NOT be marked as needing one

#### Scenario: The loaded-set bound is reached
- **WHEN** a human loads one document past the declared bound
- **THEN** the load MUST refuse and state the measured bound
- **AND** no already-loaded buffer MUST be evicted to make room

#### Scenario: Membership is asked to persist
- **WHEN** any realization would record which documents are loaded into the snapshot, register, manifest, or a published projection
- **THEN** it MUST be rejected — membership is session-local, and a generator cannot observe a live browser

### Requirement: The loaded-document selector names the working document
The chat rail SHALL carry a SELECTOR listing every loaded document, and its selected entry SHALL BE the selected buffer that the canvas presents and the chat binds to. The selector SHALL be a scrolling list rather than a fixed-width row of chips, so a session that accumulates many loaded documents needs no folding, overflow, or least-recently-used eviction policy — the control is the overflow mechanism. An entry whose filename does not fit on one line SHALL reveal its full name on hover and to assistive technology, and MUST NOT be silently truncated or ellipsized into ambiguity with another entry. Every entry SHALL be distinguishable when two loaded documents share a basename, because a selector that cannot tell two files apart is worse than one that shows a longer name. The selector SHALL be keyboard-reachable and operable with the surface's established selection semantics, and MUST NOT introduce a second spelling of selection beside the one the surface already uses. Selecting an entry SHALL be immediate, SHALL switch the transcript to that document's thread, and MUST NOT be the surface's only route to selection: loading a document and focusing the `outline` selection tab SHALL both continue to select, and every route SHALL leave the selector, the canvas, and the chat agreeing about which buffer is selected. Where no document is loaded, the selector SHALL render its empty state honestly rather than hiding, and the `outline` buffer SHALL remain selectable and workable on its own.

#### Scenario: Several documents are loaded
- **WHEN** a human has loaded five documents
- **THEN** the selector MUST list all five and MUST name which one is selected
- **AND** no entry MUST be folded away, dropped, or evicted to fit

#### Scenario: A long filename does not fit
- **WHEN** a loaded document's name is longer than one line of the selector
- **THEN** hovering the entry MUST reveal the full name, and the full name MUST be available to assistive technology
- **AND** the entry MUST remain distinguishable from every other entry

#### Scenario: Two loaded documents share a basename
- **WHEN** two loaded documents have the same file name in different folders
- **THEN** the selector MUST distinguish them

#### Scenario: Selection is changed from another route
- **WHEN** a human selects the `outline` tab or loads a new document
- **THEN** the selector, the canvas, and the chat MUST all agree about which buffer is selected

#### Scenario: Nothing is loaded yet
- **WHEN** no document has been loaded
- **THEN** the selector MUST render an honest empty state rather than hiding
- **AND** the `outline` buffer MUST remain selectable and workable

### Requirement: A docs tile carries read, load-for-editing, and save
The `docs` context's expanded tile SHALL offer exactly three verbs — READ, which opens the immersive full-window read-only reader unchanged; LOAD-FOR-EDITING, which loads the document into the chat context as a member of the loaded set and selects it; and SAVE, which persists that document through the same governed pipeline the canvas Save uses. These are the CONTRACT names other requirements refer to; the visible control labels SHALL follow the surface's own copy, and load-for-editing MAY be labelled `edit` or `load` — the annotation that ruled this verb used both words — provided the label does not reclaim the bare word "edit" for an act that happens outside the app. The SAVE verb SHALL be reachable only while that document's buffer is dirty and SHALL be visibly inert otherwise, so the control's own state answers "does this need saving" without a sentence of standing text. The tile SAVE SHALL run the SAME pipeline as the canvas Save, restricted to that document plus the outline-ancestry step the buffer contract requires when the outline is dirty, and it MUST NOT persist another loaded document the human is not looking at; every buffer it acted on — including the outline when the ancestry step ran — SHALL report its own verdict on the same surfaces the canvas Save reports on. A tile whose document is LOADED SHALL be visibly marked as loaded and, where that buffer is dirty, as needing a save; the marking SHALL be driven from live session-local buffer state and MUST NOT be written into the snapshot, the register, or any generated projection. The three verbs SHALL be offered only where the surface already holds the authority each needs: READ requires no gate capability, and LOAD and SAVE MUST be unreachable wherever editing is unreachable, stating that absence rather than failing on activation. A document that is not this tile's own editable material MUST NOT offer a reachable SAVE.

#### Scenario: A tile is expanded
- **WHEN** a human expands a `docs` tile on a capable local console
- **THEN** the action row MUST offer read, load-for-editing, and save
- **AND** save MUST be inert unless that document's buffer is dirty

#### Scenario: Read is unchanged
- **WHEN** a human activates read
- **THEN** the immersive full-window read-only reader MUST open exactly as it does today, and no buffer MUST be created or loaded

#### Scenario: A loaded document's tile is marked
- **WHEN** a document is loaded and its buffer becomes dirty
- **THEN** the tile MUST be visibly marked as loaded and as needing a save
- **AND** the marking MUST come from live buffer state and MUST NOT be recorded in the snapshot or any projection

#### Scenario: The tile save runs with a dirty outline
- **WHEN** a human invokes a tile's save while the outline is also dirty
- **THEN** the outline MUST be persisted first as the ancestry step and that document MUST then be persisted, each reporting its own verdict
- **AND** no other loaded document MUST be persisted by that act

#### Scenario: Editing is unavailable
- **WHEN** the tile renders on a surface where editing is unreachable
- **THEN** load and save MUST be unreachable and MUST state that absence rather than failing when activated
- **AND** read MUST remain available, because it needs no gate capability

### Requirement: Each loaded document carries a session thread with a structured state header
Every loaded document SHALL carry its own persisted chat THREAD, and switching the selected document SHALL switch which thread the chat shows and appends to. A thread SHALL persist as a SIDECAR FILE on the session's own branch, written only inside the session worktree and never into the served checkout, and it SHALL carry a STRUCTURED THREAD-STATE HEADER above its transcript declaring at least: the active goal, the accepted facts, the open questions, the decisions made in the thread, the refs of evidence the thread retrieved, and the pending actions. Thread state SHALL be NON-AUTHORITATIVE by construction and REGENERABLE from the transcript it summarizes: it MUST NOT be cited as governed truth, and it MUST NOT become truth by being compacted, promoted in place, or carried into a record that claims authority. COMPACTION SHALL preserve those commitments rather than the narrative that produced them: a compaction that drops an open question, a decision, an accepted fact, or a pending action SHALL be a defect, while dropping prose that restates them is the point. Threads SHALL commit with the document's Save, riding the existing one-commit-per-gate-action substrate so a thread and the document text it discusses cannot land through separate paths. Threads are WORKING MEMORY: they SHALL be excluded by default from the promotion a session's pull request performs, and a finding SHALL leave a thread only through the lifecycle verbs that already exist — an idea note, a fragment, or a disposition on the topic, with provenance — so no parallel decision store is created. Raw chat SHALL NOT become durable truth automatically by any path. Threads SHALL exist only where branch sessions exist, and MUST be absent on the hosted plane and wherever the gate capability is unavailable.

#### Scenario: The selected document changes
- **WHEN** a human selects a different loaded document
- **THEN** the chat MUST show that document's own thread and append to it
- **AND** the previous document's thread MUST be preserved unchanged

#### Scenario: A thread is compacted
- **WHEN** a thread is compacted to stay inside its bounds
- **THEN** every open question, decision, accepted fact, evidence ref, and pending action in the state header MUST survive the compaction
- **AND** the compacted result MUST remain non-authoritative and regenerable

#### Scenario: A document is saved
- **WHEN** a human saves a document whose thread has new turns
- **THEN** the thread MUST commit with that document's save inside the session worktree
- **AND** the served checkout MUST remain untouched

#### Scenario: A thread finding should become durable
- **WHEN** something decided in a thread should become part of the corpus
- **THEN** it MUST be promoted through an existing lifecycle verb with provenance
- **AND** the thread itself MUST NOT be promoted as truth and MUST NOT be published by default with the session's pull request

#### Scenario: Threads are asked for on a surface without sessions
- **WHEN** doxBench runs on the hosted plane or without the gate capability
- **THEN** no thread MUST be created, written, or offered

### Requirement: Share-session hands a live session to a colleague
The workbench SHALL offer an explicit human-only SHARE-SESSION verb that commits the session's threads, PUSHES the session branch, and returns the pushed ref, so a colleague can resume the same session from the fetched branch. Threads and every other session artifact SHALL be LOCAL until this verb runs: no thread, buffer, or session artifact SHALL be pushed as a side effect of a Save, a turn, a compaction, or a periodic task, because a working note that leaves the machine without an explicit act is a disclosure nobody chose. The verb SHALL open no pull request, request no review, and hold NO approval or merge authority; it SHALL reuse the existing remote-write path rather than introducing a second one, and it MUST NOT bypass any branch protection. Invoking it when nothing has changed since the last share SHALL report that honestly rather than pushing again. The verb SHALL be recorded as a human gate action naming the branch and the pushed ref, and it MUST be loopback-only, MUST fail closed on an unresolved actor, and MUST reject any invocation that cannot demonstrate it originates from the human console this serve started, exactly like every other gate action on this surface. The push identity SHALL follow the PLANE under the same rule the session save verb already carries: on the local plane the invoking engineer's own credential, never a stored service identity. Share-session SHALL be a local-plane capability, absent on the hosted plane, and where the gate capability is absent it SHALL render as a copyable descriptor rather than a live control.

#### Scenario: A session is shared
- **WHEN** a human invokes share-session on an active session with uncommitted threads
- **THEN** the threads MUST commit, the branch MUST be pushed, and the pushed ref MUST be returned and recorded
- **AND** no pull request MUST be opened and no review MUST be requested

#### Scenario: A colleague resumes the session
- **WHEN** a colleague fetches the shared branch and opens the same tile
- **THEN** they MUST be able to resume that session — its documents and its threads — from the fetched branch under the existing session-join rules

#### Scenario: Nothing has changed since the last share
- **WHEN** share-session is invoked with nothing new to push
- **THEN** it MUST report that honestly and MUST NOT push again

#### Scenario: A thread leaves the machine without the verb
- **WHEN** any realization would push a thread, a buffer, or a session artifact as a side effect of a Save, a turn, a compaction, or a scheduled task
- **THEN** it MUST be rejected — sharing is an explicit act

#### Scenario: Share-session is asked for approval authority
- **WHEN** any path would have share-session merge, approve, request review, or bypass protection
- **THEN** it MUST be refused

### Requirement: The staged-set knowledge service assembles a bounded context packet
Per-turn context SHALL be assembled as a BOUNDED CONTEXT PACKET by a Staged-Set Knowledge Service, and the packet SHALL contain the SELECTED document's thread in full, the THREAD-STATE HEADERS of the other loaded documents' threads, and SELECTED corpus evidence from the tile's staged set plus promoted findings only — never an unrestricted corpus, never another tile's material, and never a thread the session does not hold. The packet SHALL declare its purpose, the exact sources it carries with their refs, its bound scope, and its expiry, and it SHALL be invalid as input to any other purpose, scope, or expired turn; a consuming surface presented with such a packet MUST reject it and request a new one. Assembly SHALL run as a RAIL BEFORE any retrieval provider or model provider is reached: selection, the lifecycle-status exemption below, and the compression policy are decided first, and a refusal at that stage MUST disclose no packet content. The service SHALL be exposed behind exactly ONE tool boundary declaring a small tool contract — search, get_source, promote_finding, and reindex, with a graph query name RESERVED and unimplemented — and behind that boundary an INTERNAL ASSEMBLY PORT SHALL be the product-neutral surface a retrieval backend implements as a declared PROVIDER PROFILE. The v1 profile SHALL be local and GRAPH-LESS: lexical retrieval plus small embedded vectors plus the structured thread-states, with NO graph engine, on the recorded caution that a graph memory layer measured worse on recall, latency, and token cost than the retrieval it replaced. A graph provider SHALL be admitted only when a concrete GRADUATION TRIGGER is recorded — a recurring need for dependency traversal, contradiction detection, or change-impact analysis — and admitting one SHALL require the semantic-plane bounds to hold at that time: its index stays a derived projection, its inferred relations stay advisory, and no inference MAY create or widen authority, establish approval, or authorize an action. The retrieval backend SHALL be an INSTALL-TIME DECLARATION under the ratified two-case principle — local-embedded for a self-hosted install, a hosted backend only where a tenant install declares one — and a backend MUST NOT be selected at runtime by a turn, a prompt, or a heuristic. Content whose lifecycle status is APPROVED or RATIFIED SHALL be EXEMPT from aggressive compression, and the exemption SHALL be applied BY THE ASSEMBLER keyed on the content's own lifecycle status header; it MUST NOT be delegated to any component that cannot read that status. The source-ranking hierarchy SHALL be stated in the harness system prompt in this order — ratified or standard canon, then accepted or staged facts, then promoted findings, then active thread state, then harness-local memory last and explicitly non-authoritative — and MUST NOT be left to the model to infer. Where the knowledge service is unavailable the turn SHALL degrade to a declared reduced packet — the selected thread and the loaded buffers, with the reduced posture STATED — and MUST NOT bypass a rail to reach a provider, MUST NOT silently substitute an unbounded context, and MUST NOT fail an editor that does not need it.

#### Scenario: A turn is assembled
- **WHEN** a turn is submitted with four documents loaded
- **THEN** the packet MUST carry the selected document's thread in full, the other three threads' state headers, and the evidence the service selected
- **AND** the packet MUST declare its purpose, sources, scope, and expiry

#### Scenario: A packet is reused for another purpose
- **WHEN** a packet issued for one turn's purpose or scope is presented for another, or after it has expired
- **THEN** the consuming surface MUST reject it and request a new packet

#### Scenario: Evidence outside the staged set is requested
- **WHEN** retrieval would return material outside the tile's staged set and the promoted findings
- **THEN** it MUST be excluded from the packet

#### Scenario: A graph engine is proposed for v1
- **WHEN** any realization would add a graph engine, graph store, or graph index before a graduation trigger is recorded
- **THEN** it MUST be rejected, and the reserved graph query name MUST remain unimplemented

#### Scenario: A graph provider is graduated in
- **WHEN** a recorded graduation trigger admits a graph provider behind the assembly port
- **THEN** its index MUST remain a derived projection and its inferred relations MUST remain advisory
- **AND** no inference MUST create authority, establish approval, or authorize an action

#### Scenario: Ratified content meets the compressor
- **WHEN** the packet carries content whose lifecycle status is approved or ratified
- **THEN** the assembler MUST exempt it from aggressive compression before any provider is reached
- **AND** the exemption MUST NOT be delegated to a component that cannot read a lifecycle status

#### Scenario: The backend is chosen at runtime
- **WHEN** a turn, a prompt, or a heuristic would select the retrieval backend
- **THEN** it MUST be rejected — the backend is an install-time declaration

#### Scenario: The knowledge service is unavailable
- **WHEN** the knowledge service cannot answer
- **THEN** the turn MUST degrade to the declared reduced packet with the reduced posture stated
- **AND** it MUST NOT substitute an unbounded context, bypass a rail, or make the editors unusable

### Requirement: Context compression is a three-layer stack with declared fidelity
Compression SHALL be organized as THREE layers, each with a declared fidelity contract, and no layer SHALL be described as doing another's work. Layer one is SELECTION, performed by the knowledge service: it is LOSSLESS BY REFERENCE, because material left out of a packet remains one retrieval call away and the packet names what it carries. Layer two is SEMANTIC COMPACTION into the thread-state header: it is LOSSY BY DESIGN, human-reviewable, promotion-gated, non-authoritative, and regenerable — it preserves commitments and discards narrative. Layer three is MECHANICAL REVERSIBLE COMPRESSION at the model boundary: heavy material offloads to session artifacts behind recoverable placeholders, and it SHALL be REVERSIBLE — an offloaded item MUST be retrievable in full by the same session — and SHALL run INSIDE this surface's own trust boundary, with no third-party proxy in the path and no new network dependency. Every artifact any layer produces SHALL be non-authoritative and regenerable, and MUST NOT become truth by being compressed, cached, or offloaded. The lifecycle-status exemption SHALL live UPSTREAM of layer three, in the assembler, and MUST NOT be delegated into any component that cannot read a lifecycle status — a compressor with no caller-metadata surface is disqualified from carrying it by construction, not by preference. A candidate component for any layer SHALL be recorded with its adoption gates rather than adopted provisionally, and this capability MUST NOT depend on a watch-listed candidate: a candidate is admitted only when every recorded gate holds, including a sandboxed trial measuring net benefit on this surface's own workload rather than a published headline. Every external claim about a candidate SHALL be verified against the upstream source before it enters contract text.

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

### Requirement: The chat harness runs behind the existing model port through a local bridge
The chat harness SHALL be reached as an ADAPTER for the existing three-member model port, through a THIN LOCAL BRIDGE that translates the server's call into the harness's own process protocol, and the bridge SHALL be the only component that knows the harness's protocol. The bridge SHALL be a local child process of the console's own server, MUST NOT be reachable from the browser or from any non-loopback surface, and MUST NOT hold, read, or log a provider credential — where a menu entry reaches a hosted provider, its credential comes from the deployment's approved credential mechanism through the ratified broker lane. The bridge's process lifecycle SHALL be declared: it is started on demand, supervised, and restarted on failure, and a bridge that cannot start or has died SHALL surface as the honest model-unavailable posture — the editors and the loaded set stay usable and the chat states why it is not — rather than as a crash, a hang, or a silent empty answer. ONE harness session SHALL correspond to one document thread, so switching the selected document switches the harness session, and the harness's own session identity MUST NOT be shared across two documents' threads. The SIDECAR THREAD FILES SHALL REMAIN THE RECORD: doxBench mirrors each turn into the sidecar, and the harness's native memory backends MUST NOT hold the threads. Where a harness-native memory backend is enabled at all it SHALL hold only non-authoritative material, SHALL be ranked last by the source hierarchy, and MUST NOT be consulted as a source of governed truth — two stores claiming to be the same thread is a split brain, and the sidecar wins by contract, not by convention. Per-turn model choice SHALL be applied inside the adapter before the prompt is dispatched, and MUST NOT be expressed as an additional port member.

#### Scenario: The bridge is not running
- **WHEN** a turn is submitted and the bridge cannot start or has died
- **THEN** the surface MUST show the honest model-unavailable posture and state why
- **AND** the editors and the loaded set MUST remain fully usable

#### Scenario: The selected document changes mid-session
- **WHEN** the human switches to another loaded document and sends a turn
- **THEN** the harness session MUST switch with the thread
- **AND** one harness session MUST NOT serve two documents' threads

#### Scenario: The harness offers to remember the thread
- **WHEN** the harness's native memory would store the thread, or a turn would be reconstructed from it
- **THEN** it MUST be rejected — the sidecar is the record
- **AND** any harness-local memory that is enabled MUST be treated as non-authoritative and ranked last

#### Scenario: The bridge is reached from outside
- **WHEN** anything other than this server's own process would reach the bridge
- **THEN** it MUST be refused — the bridge is loopback-local and holds no credential of its own

### Requirement: The chat-turn contract release carries the bound buffer and the model
This capability's widened turn SHALL be carried by a RELEASED chat-turn contract, and the release SHALL be additive: the currently released envelopes SHALL remain valid and byte-identical, and the widened shape SHALL be introduced as a co-resident envelope family rather than by mutating a closed envelope, so nothing that validates today stops validating. The released widened family SHALL carry, at minimum: the outline plus every loaded document buffer, the BOUND BUFFER's key on both the request and the durable record, the per-buffer observed hashes keyed by buffer, a proposal target expressed as a buffer key, and the SELECTED-MODEL metadata that lets a record state which model answered. The release version SHALL be ALLOCATED AT REALIZATION under the repository's contract-versioning policy and MUST NOT be reserved by this proposal, because a reserved number is a claim about a merge order nobody knows yet. The release SHALL record its change class, its migration note, and the removal target for anything it deprecates, and the older family SHALL keep working for at least one full published release after it is deprecated. The runtime SHALL keep resolving its pinned wire schemas from the checkout it runs in and MUST keep refusing before consulting any provider when a pinned contract cannot be read; a release MUST NOT relax that refusal. A field the released envelope has no room for MUST NOT be carried as a server-side-only value that no reader can consult, and MUST NOT be inferred from an adjacent field that answers a different question — the record either names the thing or the gap stays stated.

#### Scenario: An older client sends a released v1 turn
- **WHEN** a client submits a turn in the previously released envelope shape
- **THEN** it MUST still validate and MUST still be served
- **AND** the older shape's bytes MUST be unchanged by this release

#### Scenario: The release version is reserved early
- **WHEN** a proposal would reserve the release's version number before merge order is known
- **THEN** it MUST be rejected — the version is allocated at realization

#### Scenario: A record is asked which model answered
- **WHEN** a reader consults a turn record for the model that produced it
- **THEN** the record MUST name it from the released envelope's own metadata

#### Scenario: A field has no room in the envelope
- **WHEN** a needed field does not fit the released envelope
- **THEN** it MUST NOT be carried as an unreadable server-side-only value or inferred from a field that answers a different question
- **AND** the obligation MUST be recorded against the release that will carry it
