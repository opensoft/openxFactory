# ideation-dashboard — ratify-doxbench-landed-context-surfaces deltas

## MODIFIED Requirements

### Requirement: Workbench lens bullseye at tile scope
The staging workbench's `lens` panel SHALL render the match-count bullseye — the same rings-by-match-count, sectored-by-matched-subset, dotted geometry the keyword lens renders (rings index how many checked keywords a document matches, innermost = all) — at TILE SCOPE, from the SAME scoped keyword-lens derivation the panel already performs. The bullseye MUST introduce no new analysis, no new score, and no new snapshot field: it renders the geometry the scoped derivation already returns, and each rail row's declared count stays the snapshot's corpus-wide number verbatim, labelled as such. The keyword rail, the bullseye, and the flat matrix SHALL each be a NAMED, ALWAYS-REACHABLE SECTION of ONE tablist on that panel, and no section SHALL be reachable only by dismissing another; that tablist SHALL carry full APG semantics — roving tabindex, arrow keys, Home and End — and the ordering relation the earlier `above` wording expressed SHALL be discharged by the tablist's declared section order rather than by simultaneous rendering. The flat matrix SHALL remain a first-class always-reachable section and MUST NOT be demoted to an opt-in alternate of the bullseye. This supersedes the earlier simultaneity clause, which the shipped three-subtab restructure contradicted: what that clause protected was ACCESS to the matrix, and a named section of a keyboard-driven tablist protects access without spending a third of the panel on a second drawing. There SHALL be exactly ONE bullseye renderer serving both the keyword-lens view and the workbench panel, so the two surfaces cannot drift. The human's checked-keyword selection SHALL persist across tab switches within one workbench session, and SHALL reset to the scope's seed when a different scope is opened or the workbench is closed.

#### Scenario: The workbench lens panel renders the bullseye
- **WHEN** a human opens the workbench's `lens` tab on any topic-bearing tile
- **THEN** the match-count bullseye MUST be a named, always-reachable section of that panel's tablist, rendered at that tile's scope
- **AND** the flat matrix MUST be an equally named, always-reachable section of the same tablist
- **AND** neither MUST be reachable only by toggling the other off

#### Scenario: The scoped bullseye introduces no new number
- **WHEN** the workbench bullseye renders
- **THEN** its rings, sectors, and dots MUST come from the existing scoped keyword-lens derivation
- **AND** no new snapshot field, score, or recount of the keyword vocabulary is introduced

#### Scenario: A checked selection survives a tab switch
- **WHEN** a human checks keywords in the workbench `lens` tab, visits `docs` or `outline`, and returns to `lens`
- **THEN** the checked selection MUST be exactly the one they left

#### Scenario: A new scope reseeds the selection
- **WHEN** the workbench is closed, or opened on a different tile
- **THEN** the checked selection MUST reset to that scope's seed keywords rather than carrying the previous scope's keywords forward

#### Scenario: The lens sections are driven from the keyboard
- **WHEN** a human moves through the lens panel's section tablist with arrow keys, Home, and End
- **THEN** every section MUST be reachable without a pointer
- **AND** exactly one tab MUST be in the tab order at a time

### Requirement: doxBench scoped view
The dashboard SHALL provide doxBench as the named evolution of the staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — with three coordinated regions over that scope. A context region SHALL retain `docs` and `lens`: `docs` SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it, plus — Brett's 2026-07-25 dogfood ruling — the member documents of the topic's linked clusters as a THIRD, separately labelled cluster-neighbourhood section, inherited via clusters, never conflated with the topic's own material, and never an input to the topic's health or the readiness gate, which stay folder-scoped) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them; `lens` SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. The `docs` context's expanded tile SHALL offer this capability's three document verbs — read, load-for-editing, and save — as specified by their own requirement. An authoring canvas SHALL present exactly ONE buffer at a time — the SELECTED buffer of the loaded set — and the SELECTION SHALL be made outside the canvas rather than by the canvas: the context region's `outline` selection tab SHALL select the `outline` buffer, loading a document SHALL select that document, and the chat rail's loaded-document selector SHALL select among the loaded documents. The `outline` buffer SHALL load the topic's declared outline material when one exists — for a staged topic, the fragment's outline material — and a document buffer SHALL load the exact document the human loaded; the canvas SHALL provide browser-local editing plus live rendered Markdown preview of the SELECTED buffer on the local human console, presented as this capability's Editor/Preview view-tab pair rather than as a side-by-side split pane, while an absent outline remains an explicit empty/create state rather than fabricated content. The canvas MUST NOT render a second buffer-selection tablist beside the selection surfaces the context region and the chat rail own, because two controls answering one question is how the two come to disagree. A chat region SHALL contain Working subject, the loaded-document selector, transcript, server-declared model selection, and composer, and SHALL ground turns on the current canvas buffers and this capability's bounded context packet as specified by this capability. doxBench's corpus write authority SHALL remain the human-only gate verbs `create-document`, `edit-document`, `open-pr`, session share, and session abandon: buffer edits, chat turns, thread writes, and AI Apply MUST write no corpus document, register entry, workbench manifest, snapshot, or gate artifact; Save MAY materialize/join a branch session and invoke only create/edit as specified; no verb MAY delete a document; and no session write may touch the served checkout. With the gate/model capabilities absent or on the hosted plane, the context SHALL remain usable and doxBench SHALL render read-only outline/document content without reachable editing, chat, threads, or write controls. The `docs` context SHALL present its document set as a VERTICAL SPLIT: a per-document ABSTRACT REGION above, and a single-reel DOCUMENT WHEEL below that places this scope's documents — every separately labelled section of them flattened into one ordered reel — in the surface's own drum projection with its own established click and spin gestures. Selecting a wheel tile SHALL make that document the abstract region's SUBJECT, and the abstract region SHALL RE-PRESENT ONLY what the snapshot already carries for that document — its own `Summary:` header, its declared topics, its stage and kind, its declared destinations, and its completeness score beside the five named signals — and MUST NOT compute, adjust, or re-weight any of it, exactly as the docs rows are already held to. The `lens` context SHALL present its three sections as named, always-reachable sections of one tablist as that panel's own requirement specifies. Neither presentation SHALL introduce a new analysis, a new score, or a new snapshot field.

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

### Requirement: A docs tile carries read, load-for-editing, and save
The `docs` context's expanded tile SHALL offer exactly three verbs — READ, which opens the immersive full-window read-only reader unchanged; LOAD-FOR-EDITING, which loads the document into the chat context as a member of the loaded set and selects it; and SAVE, which persists that document through the same governed pipeline the canvas Save uses. These are the CONTRACT names other requirements refer to; the visible control labels SHALL follow the surface's own copy, and load-for-editing MAY be labelled `edit` or `load` — the annotation that ruled this verb used both words — provided the label does not reclaim the bare word "edit" for an act that happens outside the app. The SAVE verb SHALL be reachable only while that document's buffer is dirty and SHALL be visibly inert otherwise, so the control's own state answers "does this need saving" without a sentence of standing text. The tile SAVE SHALL run the SAME pipeline as the canvas Save, restricted to that document plus the outline-ancestry step the buffer contract requires when the outline is dirty, and it MUST NOT persist another loaded document the human is not looking at; every buffer it acted on — including the outline when the ancestry step ran — SHALL report its own verdict on the same surfaces the canvas Save reports on. A tile whose document is LOADED SHALL be visibly marked as loaded and, where that buffer is dirty, as needing a save; the marking SHALL be driven from live session-local buffer state and MUST NOT be written into the snapshot, the register, or any generated projection. The three verbs SHALL be offered only where the surface already holds the authority each needs: READ requires no gate capability, and LOAD and SAVE MUST be unreachable wherever editing is unreachable, stating that absence rather than failing on activation. A document that is not this tile's own editable material MUST NOT offer a reachable SAVE. Where the `docs` context presents its document set as a WHEEL rather than as a list, these three verbs SHALL attach to the WHEEL'S EXPANDED TILE, and their contract names, their authority conditions, their dirty-state gating, and their per-buffer reporting obligations SHALL be unchanged: how the document set is PRESENTED is not a change to the verbs a document carries, and a change of presentation MUST NOT introduce a fourth verb.

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

#### Scenario: The docs context presents a wheel
- **WHEN** the `docs` context renders its document set as a wheel rather than as a list
- **THEN** the three verbs MUST attach to the expanded wheel tile with their authority conditions unchanged
- **AND** no fourth verb MUST be introduced by the change of presentation

### Requirement: The canvas view surface is expressed over the buffer set, not over two names
The view tabs, the canvas Save, the canvas Cancel, and the chat binding SHALL each be expressed over the capability's declared buffer set and its selected-buffer key, and MUST NOT hard-code any literal buffer name into their own structure. The view tabs render whichever buffer is selected and MUST NOT enumerate buffers; the canvas Save operates over the declared buffer set; Cancel operates on the selected-buffer key; the chat binds to the selected-buffer key. Phase A held this requirement WITHOUT widening the buffer set and required a realization that widened it to be rejected; that clause is now DISCHARGED, because the widening is exactly what this capability performs — in the buffer contract, the turn contract, and the save ordering rule, which are the three places that ever enumerated `outline` and `document`. The purpose of this requirement is unchanged and is now proven: widening the buffer set required changing those contracts and NOTHING on the view surface, and any FURTHER widening — a third buffer kind, a per-buffer view mode, a second selection surface — SHALL likewise be a change to the buffer contract alone. A realization that re-introduces a literal buffer name into the view tabs, the controls, or the binding MUST be rejected. A surface that selects a SUBJECT TO DESCRIBE rather than a buffer to edit — the `docs` context's document wheel, whose selection drives the abstract region's subject — SHALL NOT be a second selection surface within the meaning of this requirement and SHALL therefore require no change to the buffer contract. The test is whether the surface can make a buffer the canvas's SELECTED BUFFER: the wheel cannot, and a surface that could would be a second selection surface however it is labelled.

#### Scenario: A view surface names a buffer literally
- **WHEN** a realization builds the view tabs, Save, Cancel, or the chat binding around a literal buffer name
- **THEN** it MUST be rejected — these surfaces read the buffer set and the selected key

#### Scenario: The buffer set widens
- **WHEN** the buffer set grows from two buffers to the outline plus several loaded documents
- **THEN** the view tabs, the canvas Save, Cancel, and the chat binding MUST require no structural change to carry it
- **AND** the change MUST be confined to the buffer contract, the turn contract, and the save ordering rule

#### Scenario: A surface selects a subject rather than a buffer
- **WHEN** the docs context's wheel selection changes which document the abstract region describes
- **THEN** it MUST NOT change the canvas's selected buffer and MUST require no change to the buffer contract
- **AND** the view tabs, the canvas Save, Cancel, and the chat binding MUST be unaffected

### Requirement: doxBench editor buffer contract
The local doxBench surface SHALL maintain a KEYED BUFFER SET for its canvas — the permanently reserved `outline` key plus one key per LOADED document — and each buffer SHALL carry its kind, repository-relative path or `null` for a not-yet-created artifact, repository, base ref, base source revision, base content hash, current content hash, current text, and dirty state. A document buffer's key SHALL be its repository-relative path, so a document can be loaded at most once and no two buffers can claim the same file; at most ONE unbacked document buffer MAY exist, under the reserved key `document`, which is the not-yet-created artifact of the existing create flow and SHALL be re-keyed to its path when its first Save gives it one. The outline buffer SHALL be seeded from the opened scope's declared outline material when one exists and MUST NOT be fabricated from any document's headings; a document buffer SHALL be seeded from the document the human loaded or from the existing create-document flow. Editing any buffer MUST be a browser-local, reversible action that writes no corpus document, snapshot, register, workbench manifest, gate artifact, or branch until the human invokes Save. Save SHALL compare current and base hashes, persist a new path through `create-document` and an existing path through `edit-document`, preserve each verb's existing validation and authority boundary, and refresh/rebase each successfully saved buffer from the resulting session ref and source revision. Save ordering SHALL be an explicit rule rather than a fixed list: the `outline` buffer SHALL be persisted FIRST when it is dirty, because its commit establishes the session ancestry the document commits descend from; every dirty document buffer SHALL then be persisted in a DETERMINISTIC order the realization declares, each through its own existing gate action as one commit; and a dirty outline that did not land SHALL stop every document with a stated `not_attempted` verdict. One document's refusal SHALL NOT stop another document, because documents carry no ancestry dependency on each other and reporting one refusal as the cause of untried work is a false statement about both. Save MUST NOT invent a multi-document write verb, rewrite history, or hide partial success, and every buffer it acted on SHALL report its own verdict. Discard SHALL restore the last loaded/saved base content of the buffer it names and MUST persist nothing. A document that is the `docs` context's ABSTRACT SUBJECT SHALL NOT thereby become a buffer: the abstract subject is a READING selection over the scope's documents, independent of the keyed buffer set, so making a document the abstract's subject MUST NOT load it, key it, seed it, mark it dirty, or place it in the loaded set. Only the load-for-editing verb creates a document buffer.

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

#### Scenario: A document is pointed at but not loaded
- **WHEN** a human makes a document the docs context's abstract subject without invoking load-for-editing
- **THEN** no buffer MUST be created or keyed for that document
- **AND** the keyed buffer set MUST be unchanged

## ADDED Requirements

### Requirement: The deterministic document abstract is never captioned as a distillation and states its absences
The `docs` context's abstract region MUST NOT caption, label, or announce the deterministic abstract as a distillation, as a summary the surface produced, or as any analysis nobody ran — it re-presents fields the snapshot already carries, and claiming more would be the surface asserting work nobody did. Where the snapshot carries no derived material at all for the subject document, the region SHALL STATE that absence in words rather than rendering an empty box. Where a single named field is absent, the region SHALL OMIT that field rather than rendering a placeholder that reads as a value.

#### Scenario: A document carries no derived material
- **WHEN** the abstract region's subject is a document the snapshot references but does not catalogue
- **THEN** the region MUST state in words that there is nothing derived to show
- **AND** it MUST NOT render an empty abstract that reads as the document having no content

#### Scenario: A named field is absent for the subject
- **WHEN** the snapshot carries no summary for the subject document, or the document declares no topics
- **THEN** the region MUST omit that field rather than rendering a placeholder that reads as a value

#### Scenario: The deterministic abstract would be called a distillation
- **WHEN** any caption, label, or accessible name would describe the deterministic abstract as a distillation or as an analysis the surface performed
- **THEN** it MUST be rejected
