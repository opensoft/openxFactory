# ideation-dashboard

## MODIFIED Requirements

### Requirement: doxBench scoped view
The dashboard SHALL provide doxBench as the named evolution of the staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — with three coordinated regions over that scope. A context region SHALL retain `docs` and `lens`: `docs` SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it, plus — Brett's 2026-07-25 dogfood ruling — the member documents of the topic's linked clusters as a THIRD, separately labelled cluster-neighbourhood section, inherited via clusters, never conflated with the topic's own material, and never an input to the topic's health or the readiness gate, which stay folder-scoped) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them; `lens` SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. An authoring canvas SHALL present exactly ONE buffer at a time — the ACTIVE buffer — and the CONTEXT REGION SHALL be what chooses it rather than the canvas: focusing the context region's `outline` selection tab SHALL make the `outline` buffer active, and selecting a document from the scoped `docs` set SHALL make the `document` buffer active and load that exact document. The `outline` buffer SHALL load the topic's declared outline material when one exists — for a staged topic, the fragment's outline material — and the `document` buffer SHALL load the active document selected from the scoped docs set; the canvas SHALL provide browser-local editing plus live rendered Markdown preview of the ACTIVE buffer on the local human console, presented as this capability's Editor/Preview view-tab pair rather than as a side-by-side split pane, while an absent outline remains an explicit empty/create state rather than fabricated content. The canvas MUST NOT render a second buffer-selection tablist beside the context region's selection, because two controls answering one question is how the two come to disagree. A chat region SHALL contain Working subject, transcript, server-declared model selection, and composer, and SHALL ground turns on the current canvas buffers as specified by this capability. doxBench's corpus write authority SHALL remain the human-only gate verbs `create-document`, `edit-document`, `open-pr`, and session abandon: buffer edits, chat turns, and AI Apply MUST write no corpus document, register entry, workbench manifest, snapshot, branch, or gate artifact; Save MAY materialize/join a branch session and invoke only create/edit as specified; no verb MAY delete a document; and no session write may touch the served checkout. With the gate/model capabilities absent or on the hosted plane, the context SHALL remain usable and doxBench SHALL render read-only outline/document content without reachable editing, chat, or write controls.

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

#### Scenario: A document becomes active
- **WHEN** a human selects a row in the scoped docs context
- **THEN** the canvas MUST load that exact document into the `document` buffer and make that buffer the ACTIVE one
- **AND** docs/lens context and chat state MUST remain available

#### Scenario: The outline selection tab becomes the working context
- **WHEN** a human focuses the context region's `outline` selection tab
- **THEN** the `outline` buffer MUST become the active buffer and the canvas MUST show that buffer's working content, including unsaved edits
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
- **AND** no editing, chat, Apply, Save, Cancel, or other write-implying control MUST be reachable

#### Scenario: doxBench is used on a narrow viewport
- **WHEN** the three desktop regions cannot remain usable side by side
- **THEN** the same context, authoring canvas, and chat regions MUST stack without losing state, labels, keyboard reachability, or focus order

## ADDED Requirements

### Requirement: The doxBench canvas presents Editor and Preview view tabs
The doxBench authoring canvas SHALL present the active buffer as exactly two VIEW TABS — `Editor`, the buffer's raw Markdown text, and `Preview`, its large rendered Markdown — and MUST NOT render the raw text and its rendering side by side in one pane. `Preview` SHALL be the tab selected when the canvas mounts, because most opens are to read or resume rather than to immediately type. Switching INTO `Preview` SHALL render the active buffer's current content before that tab becomes visible, so a switch never displays a rendering the debounce had not yet applied; switching into `Editor` SHALL require no such flush, because the raw text is never debounced. The view tabs SHALL reuse the capability's existing single Markdown rendering path and its existing debounce, and MUST NOT introduce a second rendering path, a second sanitizer, or a raw-markup sink. The view tabs answer WHICH VIEW of one buffer is shown and MUST NOT be used to answer which buffer is active — that choice belongs to the context region.

#### Scenario: The canvas mounts
- **WHEN** doxBench mounts its authoring canvas on a capable local human console
- **THEN** exactly two view tabs MUST be present, `Editor` and `Preview`
- **AND** `Preview` MUST be the selected tab
- **AND** the raw text and its rendering MUST NOT both be visible in one pane

#### Scenario: A human types and then switches to Preview
- **WHEN** a human edits the active buffer in `Editor` and switches to `Preview` before the debounce has elapsed
- **THEN** the rendering MUST be brought up to the buffer's current content as part of the switch
- **AND** the human MUST NOT see the pre-edit rendering

#### Scenario: A human switches back to Editor
- **WHEN** a human switches from `Preview` to `Editor`
- **THEN** the raw Markdown MUST be shown as it stands, with no re-render required and no content transformation

#### Scenario: A view tab is asked to select a buffer
- **WHEN** any realization would let the view tabs choose which buffer the canvas shows
- **THEN** it MUST be rejected — the context region selects the buffer and the view tabs select the view of it

### Requirement: One Save and one Cancel govern the doxBench canvas
The doxBench authoring canvas SHALL carry exactly ONE Save control and exactly ONE Cancel control, placed outside both view tabs so that each control and its answer are on screen whichever view the human is standing on, and MUST NOT render a duplicate Save or Cancel per view tab or per buffer. Save SHALL keep the semantics the editor buffer contract already gives it — it persists every dirty backed buffer through the existing `create-document`/`edit-document` gate actions in the established deterministic order, as commit-per-gate-action on the tile's branch session, with `open-pr` remaining the separate promotion act — and this requirement SHALL change no Save semantics, ordering, authority, or reporting: the whole change is that the one action is drawn once. Save's verdict SHALL continue to be reported PER BUFFER, so a partial success remains separately readable. Cancel SHALL discard the ACTIVE buffer back to its last loaded or saved base content and MUST NOT touch any other buffer, because discard destroys unsaved human work, has no cross-buffer dependency, and a single control that silently reverted a buffer the human is not looking at would be this surface's one irreversible surprise. Neither control SHALL grant any authority the surface did not already hold: no force-save, no force-discard, no bypass of a refusal, and no second write route. Where the gate capability is absent, both controls SHALL state that absence as visible text beside them rather than only in a hover title, and MUST NOT be reachable.

#### Scenario: The canvas offers its controls
- **WHEN** doxBench mounts its authoring canvas
- **THEN** exactly one Save control and exactly one Cancel control MUST be present, outside both view tabs
- **AND** no per-view-tab or per-buffer duplicate of either MUST be rendered

#### Scenario: Save is invoked with both buffers dirty
- **WHEN** a human invokes the one Save with both backed buffers dirty
- **THEN** each changed document MUST persist through its existing gate action in the established deterministic order, exactly as before this change
- **AND** the verdict MUST be reported per buffer, so a committed buffer and a refused buffer are separately readable

#### Scenario: Cancel is invoked
- **WHEN** a human invokes Cancel while a buffer is active and dirty
- **THEN** that buffer MUST return to its last loaded or saved base content, and no other buffer MUST change
- **AND** nothing MUST be persisted, committed, or dispatched

#### Scenario: A control is asked for authority it does not have
- **WHEN** any realization would add a force-save, a force-discard, a refusal bypass, or a second write route to either control
- **THEN** it MUST be rejected — moving a control MUST NOT widen what it may do

#### Scenario: The gate capability is absent
- **WHEN** the canvas renders on a surface with no gate capability
- **THEN** Save MUST be unreachable and MUST state that absence as visible text beside it, not only in a hover title

### Requirement: The doxBench chat binds to the active buffer selection
The doxBench chat SHALL take its working context from the ACTIVE BUFFER — the one the context region has selected — and MUST NOT maintain a second, separately-chosen context beside it. Changing the selection SHALL change the chat's working context IMMEDIATELY, with no confirmation step, because changing which buffer is active replaces no content and destroys nothing; the existing unsaved-edit guard that fires when switching to a DIFFERENT DOCUMENT SHALL be unchanged by this rule, since that switch does replace buffer content. Focusing the context region's `outline` selection tab SHALL put the chat in outline-editing context; selecting a document from the scoped `docs` set SHALL put the chat in that document's context. Every turn record SHALL name the exact buffer — by its repository-relative path, or by its buffer kind where the buffer has no path yet — that the turn was bound to, so a transcript read later states which material the turn was working on rather than leaving it inferable from which proposal came back. This SHALL generalize the existing active-path revalidation rather than replace it: a turn whose declared active binding does not match the supplied buffer MUST still refuse before any provider call. Binding SHALL govern what the chat is working ON and MUST NOT narrow what the turn may be grounded on — the turn continues to carry the canvas buffers the grounded-turn contract requires.

#### Scenario: The selection changes mid-conversation
- **WHEN** a human with an open conversation changes the context region's selection to a different buffer
- **THEN** the chat's working context MUST follow immediately
- **AND** no confirmation step MUST be required, because no content is replaced by the change

#### Scenario: The outline is selected
- **WHEN** the context region's `outline` selection tab is focused
- **THEN** a turn submitted next MUST be bound to the `outline` buffer and its record MUST name that buffer

#### Scenario: A turn record is read later
- **WHEN** a human reads a completed turn's record
- **THEN** it MUST name the exact buffer the turn was bound to
- **AND** that name MUST NOT have to be inferred from the proposals the turn returned

#### Scenario: A turn's declared binding does not match its buffers
- **WHEN** a turn declares an active binding that does not match the buffer supplied under it
- **THEN** the route MUST refuse before any provider call, exactly as the existing active-path revalidation does

#### Scenario: Binding is mistaken for grounding
- **WHEN** any realization would use the binding to drop a buffer the grounded-turn contract requires the request to carry
- **THEN** it MUST be rejected — binding names what the chat works on, not what it may see

### Requirement: The canvas controls stay inside the per-buffer staleness guard
Every doxBench canvas control SHALL remain subject to the existing per-buffer content-identity guard, and consolidating controls onto the panel MUST NOT create a path around it. A Save attempted against a buffer whose settled content identity has moved since the acting request last observed it MUST refuse that buffer, exactly as it does today; an AI proposal applied against a moved identity MUST refuse as stale; a turn whose declared buffer hash does not match the supplied text MUST refuse before any provider call. The guard SHALL be applied PER BUFFER rather than per panel, because it describes one buffer's identity and nothing about it depends on how many buffers exist. Cancel MOVES a buffer's identity back to its base and SHALL therefore emit the same settled-identity notification an edit or a discard already emits, so no proposal card continues to offer Apply against text the buffer no longer holds. While a Save is in flight the canvas SHALL state that fact, withdraw the controls it would otherwise offer, and REFUSE rather than queue a second Save or a concurrent edit, because the bytes handed over are the bytes the verdict describes.

#### Scenario: Save meets a moved identity
- **WHEN** a buffer's settled content identity has moved since the request that is now being saved observed it
- **THEN** that buffer's save MUST refuse, and its text, base, and dirty state MUST be preserved exactly

#### Scenario: Cancel moves an identity
- **WHEN** Cancel restores the active buffer to its base content
- **THEN** the settled-identity notification MUST fire, exactly as it does for an edit or a discard
- **AND** any proposal card whose base no longer matches MUST stop offering Apply

#### Scenario: A second Save is attempted
- **WHEN** a human invokes Save while a Save is already in flight for this canvas
- **THEN** it MUST refuse and say so, and MUST NOT be queued

#### Scenario: An edit is attempted mid-save
- **WHEN** a human edits a buffer whose bytes are currently in flight to the save seam
- **THEN** the edit MUST refuse visibly rather than silently vanish or land underneath the verdict

### Requirement: The canvas view surface is expressed over the buffer set, not over two names
The view tabs, the one Save, the one Cancel, and the chat binding SHALL each be expressed over the capability's declared buffer enumeration and its active-buffer key, and MUST NOT hard-code the literal buffer names into their own structure. The view tabs render whichever buffer is active and MUST NOT enumerate buffers; Save operates over the declared buffer set; Cancel operates on the active-buffer key; the chat binds to the active-buffer key. This requirement does NOT widen the buffer set — the editor buffer contract's exactly-two rule stands unchanged, and a realization of this requirement that generalized the state model, the turn-assembly buffer requirement, or the save ordering MUST be rejected as out of its scope. Its purpose is that widening the buffer set later requires changing the buffer contract and nothing on this surface.

#### Scenario: A view surface names a buffer literally
- **WHEN** a realization builds the view tabs, Save, Cancel, or the chat binding around the literal names of the two current buffers
- **THEN** it MUST be rejected — these surfaces read the buffer set and the active key

#### Scenario: The buffer contract is unchanged
- **WHEN** this requirement is realized
- **THEN** the editor buffer contract's exactly-two-buffer rule, the turn-assembly buffer requirement, and the deterministic save ordering MUST all be observably unchanged
