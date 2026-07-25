# ideation-dashboard Delta: Workbench Bullseye + Gated Document Creation

## ADDED Requirements

### Requirement: Workbench lens bullseye at tile scope
The staging workbench's `lens` panel SHALL render the match-count bullseye — the same rings-by-match-count, sectored-by-matched-subset, dotted geometry the keyword lens renders (rings index how many checked keywords a document matches, innermost = all) — at TILE SCOPE, above the always-present flat matrix, from the SAME scoped keyword-lens derivation the panel already performs. The bullseye MUST introduce no new analysis, no new score, and no new snapshot field: it renders the geometry the scoped derivation already returns, and each rail row's declared count stays the snapshot's corpus-wide number verbatim, labelled as such. The flat matrix SHALL remain always present and MUST NOT become a toggle-only alternate. There SHALL be exactly ONE bullseye renderer serving both the keyword-lens view and the workbench panel, so the two surfaces cannot drift. The human's checked-keyword selection SHALL persist across tab switches within one workbench session, and SHALL reset to the scope's seed when a different scope is opened or the workbench is closed.

#### Scenario: The workbench lens panel renders the bullseye
- **WHEN** a human opens the workbench's `lens` tab on any topic-bearing tile
- **THEN** the match-count bullseye MUST render at that tile's scope, above the flat matrix
- **AND** the flat matrix MUST still render, as the always-available view of the same membership

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

### Requirement: Gated document creation verb
The gate console SHALL offer a human-only `create-document` verb that brings a NEW ideation document into existence through the EXISTING tested authoring engine, enforced at the route so the workbench affordance, the CLI parity subcommand, and a direct request are gated identically. The verb SHALL accept an area, title, summary, topics, and optional repository context, kind, possible-feat seeds, and source citation, defaulting the repository context from the served snapshot's repository, and SHALL write the document through the authoring scaffold with its controlled header block (`Status`, `Kind`, `Summary`, `Topics`, `Repository context`, `Captured`) in the declared order. The write MUST be create-only: an EXISTING target refuses as a source-edit refusal and is never overwritten, and this verb grants NO edit or delete authority over any existing document. Every successful create SHALL persist a gate-action record naming the created document's repository-relative path. The verb MUST be loopback-only and MUST fail closed on an unresolved actor, and any agent or automated invocation MUST be rejected and reported, like every gate action. The verb SHALL make no engine change: the header contract, the filename normalization, and every refusal are the authoring engine's, surfaced verbatim at the route.

#### Scenario: A human creates a document through the gate
- **WHEN** a human invokes `create-document` with an area, title, summary, and topics
- **THEN** a header-compliant document is written into that area with the controlled header block in the declared order
- **AND** a gate-action record is persisted naming the created document's repository-relative path

#### Scenario: The target already exists
- **WHEN** the verb targets a path that already holds a document
- **THEN** the call MUST refuse as a source-edit refusal, persist nothing, and leave the existing document byte-identical

#### Scenario: An agent invokes the verb
- **WHEN** any agent or automated path calls `create-document`
- **THEN** the call MUST be rejected and reported — document creation by an agent remains the separate agent-capture surface with its own header enforcement

#### Scenario: The gate capability is unavailable
- **WHEN** the verb is reached on a non-loopback bind, or with no resolved human actor
- **THEN** the route MUST refuse and persist nothing

#### Scenario: The CLI reaches the same law
- **WHEN** the parity subcommand invokes the verb
- **THEN** it MUST be gated identically to the browser affordance, drive the same engine, and produce the same gate-action record

### Requirement: Workbench creation affordances and seeding
The staging workbench SHALL offer the `create-document` verb from each of its three tabs, seeded from the material that tab is showing, and the seeded values SHALL remain editable before the create fires. On the `docs` tab the affordance SHALL be a button on the pane's actions row, seeding topics from the tile's keywords, repository context from the snapshot's repository, the area from the scope (a staged scope's own staging topic folder; the brainstorm area for a cluster or possible scope), and a source citation naming the workbench scope by kind and id. On the `lens` tab the affordance SHALL be a button on the forming-set pane AND a click on the bullseye's CENTRE ring (the matches-ALL zone), both opening the SAME dialog with the same seeding rule, seeding topics from the LIVE checked keyword set and a source citation naming the recipe — the checked and pinned keywords — at the snapshot's source revision, so the membership that motivated the document re-derives from the record. On the `outline` tab the affordance SHALL be offered for staged scopes ONLY, as a new fragment in that topic with the area set to the staging topic folder, and MUST be hidden for cluster and possible scopes, which have no topic folder to write into. When the gate capability is absent the affordances SHALL render as COPYABLE CLI DESCRIPTORS carrying the seeded values and MUST NOT render as live buttons, and no write MUST be reachable from the page. On a successful create the workbench SHALL open the created document in the read-only viewer. The workbench's posture indicator SHALL state `read-only` when the gate capability is off and the gate-bearing posture when the capabilities grant gate, and MUST NOT claim a posture the surface does not have.

#### Scenario: Creating from the docs tab
- **WHEN** a human uses the create affordance on the workbench `docs` tab
- **THEN** the dialog opens seeded with the tile's keywords as topics, the snapshot's repository as repository context, the scope-derived area, and a source citation naming the scope's kind and id
- **AND** every seeded value is editable before the create fires

#### Scenario: Creating from the centre ring
- **WHEN** a human clicks the bullseye's matches-ALL centre ring, or the forming-set pane's create button
- **THEN** the SAME create dialog opens, seeded with the LIVE checked keyword set as topics
- **AND** the source citation names the checked and pinned keywords at the snapshot's source revision

#### Scenario: The outline affordance is scope-bound
- **WHEN** the workbench `outline` tab renders for a cluster or a possible
- **THEN** the create affordance MUST be hidden — there is no staging topic folder to write a fragment into
- **AND** for a staged scope it MUST be offered, writing into that topic's folder

#### Scenario: The gate capability is off
- **WHEN** the workbench renders on a surface without the gate capability
- **THEN** every create affordance MUST render as a copyable CLI descriptor carrying the seeded values
- **AND** no live create button and no write path MUST be reachable from the page

#### Scenario: A create succeeds
- **WHEN** a create lands through the gate
- **THEN** the workbench MUST open the created document in the read-only viewer

#### Scenario: The posture indicator is honest
- **WHEN** the workbench renders with the gate capability granted
- **THEN** its posture indicator MUST state the gate-bearing posture rather than `read-only`
- **AND** with the gate capability absent it MUST state `read-only`

## MODIFIED Requirements

### Requirement: Staging workbench scoped view
The dashboard SHALL provide a staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — presenting three tabbed panels over that one scope. The `docs` panel SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it, plus — Brett's 2026-07-25 dogfood ruling — the member documents of the topic's linked clusters as a THIRD, separately labelled cluster-neighbourhood section, inherited via clusters, never conflated with the topic's own material, and never an input to the topic's health or the readiness gate, which stay folder-scoped) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them. The `lens` panel SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. The `outline` panel SHALL render the topic's outline when one exists — for a staged topic, the fragment's outline material — read through the same read-only `/source` pass-through the document viewer uses, and MUST show an explicit empty state when the scope carries no outline. The workbench's ONLY write authority SHALL be the human-only `create-document` gate verb: it MUST write no register entry, no workbench manifest, and no gate artifact beyond that verb's own gate-action record; it MUST NOT modify or delete any existing document, in any panel, by any path; and outline EDITING remains out of scope. With the gate capability absent the workbench SHALL be read-only in every panel, as it is on the served static image.

#### Scenario: The workbench opens on a cluster
- **WHEN** a human opens the workbench from a cluster tile
- **THEN** the view scopes to that cluster: the `docs` panel lists exactly that cluster's snapshot document edges and the `lens` panel is scoped to that cluster's declared topics

#### Scenario: The workbench opens on a possible
- **WHEN** a human opens the workbench from a possible tile
- **THEN** the `docs` panel lists the documents its recorded supporting evidence cites
- **AND** any documents inherited from its claiming clusters appear in a separately labelled section, distinct from cited evidence

#### Scenario: The workbench opens on a staged topic
- **WHEN** a human opens the workbench from a staged-topic tile
- **THEN** the `docs` panel lists the topic folder's corpus documents together with every document whose declared destination names that staging topic
- **AND** the member documents of the topic's linked clusters appear in a separately labelled cluster-neighbourhood section, never conflated with the topic's own material
- **AND** the `outline` panel renders that fragment's outline material read-only

#### Scenario: Cluster-neighbourhood documents stay out of health
- **WHEN** a staged topic's health or its readiness gate is computed
- **THEN** cluster-neighbourhood documents contribute nothing — health and the gate stay derived from the topic FOLDER's own corpus documents only

#### Scenario: A docs row shows how far a document has come
- **WHEN** the `docs` panel renders a document the snapshot scores
- **THEN** its bar and named signals MUST come from the snapshot's `completeness` object verbatim
- **AND** the workbench MUST NOT compute, adjust, or re-weight any signal

#### Scenario: The source pass-through is absent
- **WHEN** the workbench runs against a served static image with no `/source` route
- **THEN** the `docs` and `lens` panels MUST still render from the snapshot
- **AND** the `outline` panel MUST report the missing pass-through inline and degrade, exactly as the document viewer does

#### Scenario: A scope carries no outline
- **WHEN** the opened tile has no outline material
- **THEN** the `outline` panel MUST render an explicit empty state rather than fabricating or drafting one

#### Scenario: The workbench is asked to modify an existing document
- **WHEN** any workbench panel would edit or delete an existing corpus document, or write a register entry, a workbench manifest, or any gate artifact other than the `create-document` verb's own gate-action record
- **THEN** the write MUST be rejected and reported — the workbench's only write is the create-only gated document creation, and every other write path arrives in a later change

#### Scenario: The workbench renders without the gate capability
- **WHEN** the workbench runs on a surface where the gate capability is absent
- **THEN** every panel MUST be read-only and no write MUST be reachable from the page
