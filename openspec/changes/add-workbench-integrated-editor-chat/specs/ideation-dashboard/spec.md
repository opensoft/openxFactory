# ideation-dashboard Delta: doxBench Integrated Editor and Chat

This delta is stacked on the latest requirements in
`add-workbench-branch-sessions`. It MUST NOT archive until
`add-ideation-dashboard`, `add-propose-verb`, `add-staging-workbench`,
`add-workbench-bullseye-and-create`, `add-dashboard-repo-selector`, and
`add-workbench-branch-sessions` have archived in their declared dependency
order. Before this delta archives, its MODIFIED requirements MUST be rebased
from the resulting promoted `openspec/specs/ideation-dashboard/spec.md`.

## ADDED Requirements

### Requirement: doxBench surface identity
The dashboard SHALL name the integrated staging-workbench authoring surface **doxBench**, using that exact casing in visible product copy, navigation and heading text, accessible names, documentation, tests, and realization evidence. doxBench SHALL remain the named human-facing evolution of the existing `ideation-dashboard` staging workbench rather than a second capability. Existing technical identifiers — including `workbench-*` schemas, routes, module names, the `workbench-chat-turn` kind, `WorkbenchModelPort`, branch-session records, and persisted dashboard artifacts — MUST remain compatible and MUST NOT be renamed or rewritten solely to adopt the doxBench name.

#### Scenario: The integrated authoring surface is presented
- **WHEN** the dashboard exposes the integrated authoring surface
- **THEN** its visible heading and accessible surface name MUST use the exact name `doxBench`
- **AND** generic controls MAY retain descriptive workbench terminology where that terminology names an inherited technical concept

#### Scenario: Existing workbench artifacts are loaded
- **WHEN** doxBench consumes a pre-name snapshot, branch-session record, route, schema, or other `workbench-*` artifact
- **THEN** that artifact MUST remain valid and usable without migration
- **AND** no persisted identifier or artifact kind MUST be rewritten merely to carry the doxBench name

### Requirement: doxBench editor buffer contract
The local doxBench surface SHALL maintain exactly two explicit authoring buffers for its canvas — `outline` and `document` — and each buffer SHALL carry its kind, repository-relative path or `null` for a not-yet-created artifact, repository, base ref, base source revision, base content hash, current content hash, current text, and dirty state. The outline buffer SHALL be seeded from the opened scope's declared outline material when one exists and MUST NOT be fabricated from the active document's headings; the document buffer SHALL be seeded from the active document selected from the scoped document set or from the existing create-document flow. Editing either buffer MUST be a browser-local, reversible action that writes no corpus document, snapshot, register, workbench manifest, gate artifact, or branch until the human invokes Save. Save SHALL compare current and base hashes, persist a new path through `create-document` and an existing path through `edit-document`, preserve each verb's existing validation and authority boundary, and refresh/rebase each successfully saved buffer from the resulting session ref and source revision. Saving two dirty backed buffers SHALL invoke one existing gate action per changed document in deterministic outline-then-document order and MUST NOT invent a multi-document write verb, rewrite history, or hide partial success. Discard SHALL restore the last loaded/saved base content and MUST persist nothing.

#### Scenario: A human edits the outline before chatting
- **WHEN** a human changes the outline buffer without invoking Save
- **THEN** the canvas MUST show the outline as dirty
- **AND** no corpus file, branch, snapshot, register, manifest, or gate record MUST change

#### Scenario: A human selects a document
- **WHEN** a human selects a document from the scoped `docs` context
- **THEN** the `Document` buffer MUST load that exact document from the active repository/ref and record its source revision and content hash
- **AND** changing the selection with unsaved document edits MUST require the human to save or discard rather than silently replacing the buffer

#### Scenario: A scope has no outline
- **WHEN** the opened scope declares no outline material
- **THEN** the Outline tab MUST show an explicit empty state
- **AND** it MAY offer a new outline buffer whose first persistence uses `create-document`, but it MUST NOT fabricate or persist an outline merely by opening the tab

#### Scenario: One dirty buffer is saved
- **WHEN** the human invokes Save with exactly one backed buffer dirty
- **THEN** exactly one `create-document` or `edit-document` gate action MUST persist that buffer on the tile's branch session
- **AND** the successful response MUST become the buffer's new base ref, revision, content, and hash

#### Scenario: Both dirty buffers are saved
- **WHEN** the human invokes Save with both backed buffers dirty
- **THEN** the outline action MUST run before the document action and each changed document MUST produce its own existing gate-action commit
- **AND** no combined or hidden write verb MUST be introduced

#### Scenario: The second save action fails
- **WHEN** the outline save commits and the subsequent document save refuses
- **THEN** the UI MUST report the committed outline and refused document separately
- **AND** the outline buffer MUST advance to its committed base while the document buffer remains dirty
- **AND** the system MUST NOT amend, reset, or otherwise erase the committed outline action

#### Scenario: A human discards local edits
- **WHEN** the human invokes Discard on a dirty buffer
- **THEN** that buffer MUST return to its last loaded or saved base content
- **AND** no gate action or provider call MUST occur

### Requirement: Grounded doxBench chat turn
The local human-console doxBench surface SHALL offer a chat rail containing a `Working subject` field, transcript, server-declared model selector, and message composer. Each submitted turn SHALL use a versioned `workbench-chat-turn` request containing the repository/ref and tile scope, active document path, `working_subject`, new user message, bounded prior transcript, selected model id, a client-generated turn id, and the complete current outline and document buffer descriptors and text including their hashes. The server MUST independently resolve and confine the repository/ref, tile, outline path, and active document path before a provider call; MUST verify every declared content hash; and MUST record in the response the exact buffer hashes, model id, and turn id used. Unsaved buffer text SHALL be eligible turn input and MUST be labelled as working state rather than governed or committed content. The next turn SHALL use the buffer contents that exist when that next turn is submitted, including intervening human edits and locally applied AI proposals, rather than reusing a previous turn's text. The request/response schemas SHALL impose explicit byte, transcript-turn, and output bounds; an over-bound turn MUST refuse with the applicable measured limit and MUST NOT silently truncate, summarize, or omit either buffer. Exactly one turn MAY be in flight per browser conversation key. Within one server process, the client turn id SHALL be idempotent: a repeated completed id with identical input hashes SHALL return the recorded result without another provider dispatch, an in-flight repeat SHALL attach to or report that turn, and reuse with different content or hashes MUST refuse. A provider or response-validation failure MUST return a fixed redacted error, preserve both buffers, append no assistant proposal, and disclose no credential, raw provider response, prompt, document content, or unsaved text in logs or error details.

#### Scenario: A human edit feeds the next turn
- **WHEN** a human edits either buffer after one assistant response and submits another message
- **THEN** the new request MUST carry the edited current buffer text and hash
- **AND** the response MUST identify that hash as the content the model saw

#### Scenario: Unsaved edits are discussed
- **WHEN** a dirty buffer is included in a chat turn
- **THEN** the model MAY use that exact unsaved text
- **AND** neither the request nor response MUST represent the text as committed, governed, or present on `main`

#### Scenario: The route receives a mismatched path or hash
- **WHEN** a turn names a path outside the opened tile's allowed scope, a repository/ref other than the active binding, or a hash that does not match the supplied text
- **THEN** the route MUST refuse before any provider call
- **AND** no browser conversation state or corpus state MUST be persisted by the server

#### Scenario: A turn exceeds a declared limit
- **WHEN** the combined buffers, transcript, message, or requested output exceed the selected catalog entry's or route's limit
- **THEN** the route MUST refuse and name the exceeded dimension and limit
- **AND** it MUST NOT silently truncate or send a partial document to the provider

#### Scenario: A turn completes
- **WHEN** the provider returns a valid response for the exact request
- **THEN** the chat rail MUST append assistant prose and any typed proposals under one turn id
- **AND** focus, active canvas tab, editor selection, scroll position, and dirty state MUST remain usable

#### Scenario: A completed turn is retried
- **WHEN** the same client turn id is submitted again in the same server process with identical content and hashes
- **THEN** the recorded result MUST be returned without a second provider dispatch

#### Scenario: A turn id is reused for different content
- **WHEN** a client turn id is repeated with different buffer text, hashes, subject, message, or model
- **THEN** the server MUST refuse the idempotency conflict before any additional provider call

#### Scenario: A provider or response validation fails
- **WHEN** the provider call fails or its response violates the typed response schema
- **THEN** both editor buffers MUST remain byte-identical and no assistant proposal MUST be appended
- **AND** the UI MUST receive a fixed actionable failure while logs and response details reveal no credential, raw provider payload, prompt, document content, or unsaved text

### Requirement: doxBench model catalog and provider boundary
The dashboard backend SHALL expose a same-origin workbench model catalog whose entries carry a stable opaque model id, human label, provider class, input/output limits, availability, and a human-readable data-handling badge. The catalog MUST NOT expose a provider credential, raw secret, raw endpoint, secret environment-variable name, or provider request template, and the browser MUST NOT call any model provider directly. A chat turn SHALL accept only a model id present and available in the current catalog and SHALL resolve that id through a server-side injected model-provider port. Provider credentials MUST come only from the deployment's approved server-side credential mechanism and MUST NOT enter browser storage, a request body, response body, dashboard snapshot, chat transcript, log, gate record, git artifact, or exception detail. A hosted fallback MAY be offered only when the deployment explicitly enables it and its configured data-handling policy meets the catalog badge; otherwise the model MUST be unavailable. The model catalog and turn routes SHALL be offered only on a loopback human console with a real checkout, resolved actor, and demonstrated console presence; the hosted/read-only plane MUST offer neither route.

#### Scenario: The browser loads model choices
- **WHEN** local doxBench opens with one or more allowed providers configured
- **THEN** the selector MUST show exactly the available catalog entries and their data-handling badges
- **AND** no credential or raw provider endpoint MUST be present in the page or catalog response

#### Scenario: No model is configured
- **WHEN** the model catalog is empty
- **THEN** the chat rail MUST explain that no allowed model is configured
- **AND** the Outline and Document editors MUST remain usable

#### Scenario: An unknown model id is submitted
- **WHEN** a chat request names a model id absent from or unavailable in the current catalog
- **THEN** the server MUST refuse before any provider call

#### Scenario: A browser attempts a direct provider call
- **WHEN** the dashboard bundle or runtime would contact a model endpoint other than the same-origin workbench routes
- **THEN** the renderer boundary MUST fail validation and the call MUST NOT ship

#### Scenario: Hosted doxBench is opened
- **WHEN** doxBench runs on the hosted/read-only plane
- **THEN** the model catalog and turn capabilities MUST be absent
- **AND** no chat or editor control implying unavailable authority MUST be reachable

### Requirement: Typed AI proposals and stale-application protection
A workbench chat response MAY contain ordinary assistant prose and zero or more typed edit proposals, and each proposal SHALL name exactly one target (`outline` or `document`), carry complete proposed content, identify the target buffer's input `base_hash`, and include a human-readable summary. A provider response MUST NOT write, save, commit, create, delete, or apply any document by itself. The browser SHALL render Apply only for schema-valid typed proposals. Applying a proposal SHALL replace only the named browser buffer, mark it dirty, remain locally reversible, and MUST NOT invoke Save or any gate action. Immediately before Apply, the browser MUST recompute the target buffer hash and compare it with the proposal's `base_hash`; a mismatch MUST refuse as stale and offer inspection of current versus proposed content or a new turn, but MUST NOT silently merge or expose an authority-bypassing force-apply action. Chat prose without a typed proposal MUST NOT be inferred as replacement content.

#### Scenario: An AI proposes a document revision
- **WHEN** a valid response proposes document content against the current document hash
- **THEN** the human MAY apply it to the Document buffer
- **AND** the buffer MUST become dirty while the corpus and branch remain unchanged until Save

#### Scenario: A proposal targets both buffers
- **WHEN** one turn returns valid outline and document proposals
- **THEN** each proposal MUST have its own target and base hash
- **AND** the human MUST be able to apply or reject each independently

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

### Requirement: Browser-local doxBench conversation
doxBench SHALL keep `working_subject`, selected model id, and bounded transcript in browser `sessionStorage` keyed by repository, ref, tile kind, and tile id, and SHALL treat that state as ephemeral per-browser working context rather than a branch-session descriptor, shared conversation, snapshot field, corpus artifact, or governance record. The working subject SHALL default from the tile's title or summary, remain editable, and affect authoring focus only; it MUST NOT be interpreted or copied into any customer `subject_ref`, actor, patient, tenant, authority, credential, routing identity, or other identity-bearing subject field. A normal refresh in the same browser session MAY restore matching working state, but changing to a different repository/ref/tile key MUST NOT leak the prior state into the new scope. Ending a branch session by merge or abandon SHALL clear state for that session key.

#### Scenario: A page refresh restores the same conversation
- **WHEN** the page reloads in the same browser session on the identical repository/ref/tile key
- **THEN** the matching working subject, selected available model, and bounded transcript MAY be restored
- **AND** no server-side conversation store or corpus artifact MUST be required

#### Scenario: doxBench changes scope
- **WHEN** the active repository, ref, tile kind, or tile id changes
- **THEN** working state from the previous key MUST NOT appear in the new chat rail or buffers

#### Scenario: A session ends
- **WHEN** the branch session merges or is abandoned
- **THEN** browser working state keyed to that session ref MUST be cleared

#### Scenario: Working subject resembles an identity
- **WHEN** a human types a customer, patient, tenant, or other identity-shaped value into Working subject
- **THEN** the system MUST continue to treat it only as free-form prompt focus
- **AND** it MUST NOT bind, validate, route, or persist it as an identity subject

## MODIFIED Requirements

### Requirement: Session-scoped document editing verb
The gate console SHALL offer a human-only `edit-document` verb that is valid inside an active branch session and MAY also be invoked by local doxBench as the tile's FIRST save when it targets that tile's own editable material. On an eligible first save, the route SHALL atomically materialize or join the tile's branch session, verify the supplied base ref/revision/content hash against the selected source, rewrite the existing document only in the resulting session worktree, and commit the rewrite as that action's single commit with its gate-action record. If validation or rewriting fails, the attempted first save MUST persist no document, commit, gate record, live registry entry, or orphan worktree. Every other invocation that names no live session MUST refuse. The verb MUST refuse a target outside the session worktree or outside the tile's own editable material; inherited, cluster-neighbourhood, cited, and inbound-context documents remain read-only in this tile even though they exist inside the worktree. The verb SHALL rewrite an EXISTING document, MUST NOT create one (that stays `create-document`), and MUST NOT delete one by any path. No per-edit redline ceremony SHALL be required of an on-branch edit, because THE PULL REQUEST REVIEW IS THE GOVERNANCE — the ratified gates-happen-on-main rule already holds that an unmerged transition is exploration and not status, which makes an unmerged branch precisely the place where ordinary editing is legal. The gate console's `edit-apply` redline path and the human external-editor escape hatch SHALL REMAIN UNCHANGED for a MAIN-RESIDENT document outside integrated branch-backed authoring. The `create-document` verb SHALL keep its create-only semantics unchanged and, inside a branch session, SHALL write into the session worktree instead of the served checkout. The verb MUST be loopback-only, MUST fail closed on an unresolved actor, and MUST reject and report any invocation that cannot demonstrate it originates from the human console this serve started, like every gate action — a process running as the identified human, which can read that console's own token, is NOT distinguished at this layer (D23), and every accepted invocation's record MUST therefore name the surface it arrived on and how console presence was shown.

#### Scenario: A document is edited inside a session
- **WHEN** a human invokes `edit-document` on the tile's own document in an active session's worktree with the current base hash
- **THEN** the document MUST be rewritten in that worktree and committed as that action's single commit with its gate-action record
- **AND** no redline artifact MUST be required before the edit lands

#### Scenario: An existing document is the first save
- **WHEN** local doxBench invokes `edit-document` as the tile's first save against the current base ref, revision, and hash of the tile's own editable material
- **THEN** the route MUST materialize or join the tile's branch session and commit the rewrite only in that session worktree
- **AND** the served checkout MUST remain untouched

#### Scenario: First-save validation fails
- **WHEN** the integrated first save carries a stale base hash, illegal target, invalid content, or any other edit refusal
- **THEN** it MUST persist no document, commit, gate record, live registry entry, or orphan worktree

#### Scenario: Editing is attempted without a session by another path
- **WHEN** `edit-document` is invoked with no active branch session and is not an eligible integrated first save
- **THEN** it MUST refuse and persist nothing — main-resident editing stays the `edit-apply` or external-editor path

#### Scenario: An edit targets a path outside the worktree
- **WHEN** `edit-document` names a path that does not resolve inside the active session's worktree root
- **THEN** it MUST refuse and persist nothing

#### Scenario: An edit targets context owned by another scope
- **WHEN** the tile's edit names an inherited, cluster-neighbourhood, cited, inbound, or other context document that is not the tile's own editable material
- **THEN** it MUST refuse even when that path exists inside the session worktree

#### Scenario: A session edit is asked to delete
- **WHEN** `edit-document` is invoked in a way that would remove a document
- **THEN** it MUST refuse — the verb rewrites, and no session verb grants delete authority

#### Scenario: Creating inside a session
- **WHEN** `create-document` is invoked while a branch session is active on the tile
- **THEN** the document MUST be created in the session worktree with the create-only semantics unchanged, and committed as that action's single commit

#### Scenario: A non-console path invokes the edit verb
- **WHEN** any caller that cannot demonstrate it originates from the human console this serve started calls `edit-document`
- **THEN** the call MUST be rejected and reported
- **AND** a process running as the identified human, which can read that console's own token, is NOT distinguished here — that distinction requires the xForge-host identity work deferred under D22, and the residual is accepted by D23
- **AND** the record of any accepted call MUST carry the surface it arrived on and how console presence was shown, so an act performed this way is auditable rather than invisible

### Requirement: doxBench scoped view
The dashboard SHALL provide doxBench as the named evolution of the staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — with three coordinated regions over that scope. A context region SHALL retain `docs` and `lens`: `docs` SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it, plus — Brett's 2026-07-25 dogfood ruling — the member documents of the topic's linked clusters as a THIRD, separately labelled cluster-neighbourhood section, inherited via clusters, never conflated with the topic's own material, and never an input to the topic's health or the readiness gate, which stay folder-scoped) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them; `lens` SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. An authoring canvas SHALL present exactly two primary tabs, `Outline` and `Document`: Outline SHALL load the topic's declared outline material when one exists — for a staged topic, the fragment's outline material — and Document SHALL load the active document selected from the scoped docs set; both SHALL provide browser-local editing plus live rendered Markdown preview on the local human console, while an absent outline remains an explicit empty/create state rather than fabricated content. A chat region SHALL contain Working subject, transcript, server-declared model selection, and composer, and SHALL ground turns on the current canvas buffers as specified by this change. doxBench's corpus write authority SHALL remain the human-only gate verbs `create-document`, `edit-document`, `open-pr`, and session abandon: buffer edits, chat turns, and AI Apply MUST write no corpus document, register entry, workbench manifest, snapshot, branch, or gate artifact; Save MAY materialize/join a branch session and invoke only create/edit as specified; no verb MAY delete a document; and no session write may touch the served checkout. With the gate/model capabilities absent or on the hosted plane, the context SHALL remain usable and doxBench SHALL render read-only outline/document content without reachable editing, chat, or write controls.

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
- **AND** the Outline canvas MUST load that fragment's outline material from the active repository/ref

#### Scenario: A document becomes active
- **WHEN** a human selects a row in the scoped docs context
- **THEN** the Document canvas MUST load that exact document and make Document the active authoring tab
- **AND** docs/lens context and chat state MUST remain available

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
- **THEN** the Outline canvas MUST render an explicit empty state rather than fabricating or drafting one
- **AND** only a capable local human console MAY offer a create-backed outline buffer

#### Scenario: A human edits before a session exists
- **WHEN** a capable local human edits an outline or document buffer with no active branch session
- **THEN** the edit MUST remain browser-local and available to the next chat turn
- **AND** the served checkout and every shared surface MUST remain unchanged

#### Scenario: An existing document is saved
- **WHEN** a human saves an existing eligible buffer from doxBench
- **THEN** `edit-document` MUST persist it on the tile's branch session as that action's single commit
- **AND** the served checkout MUST remain untouched

#### Scenario: doxBench renders without gate or model capability
- **WHEN** doxBench runs on a surface where gate and model capabilities are absent
- **THEN** docs/lens and available source content MUST remain readable
- **AND** no editing, chat, Apply, Save, or other write-implying control MUST be reachable

#### Scenario: doxBench is used on a narrow viewport
- **WHEN** the three desktop regions cannot remain usable side by side
- **THEN** the same context, Outline/Document canvas, and chat regions MUST stack without losing state, labels, keyboard reachability, or focus order
