# ideation-dashboard Delta: Staging Workbench (read-only foundation)

## ADDED Requirements

### Requirement: Deterministic per-document completeness signal
The snapshot generator SHALL compute a per-document completeness signal at generation time and emit it as an additive `completeness` object on each `documents[]` entry — a `score` plus five named signals: `structure` (the fraction of the document's expected structural elements present, the expected set fixed per `Kind:` with a common fallback — H1 title, the governance header block, at least one section), `length` (body size normalized against a fixed saturation threshold, so padding past the threshold cannot outscore substance), `open_markers` (an INVERSE signal over open-question / TODO / TBD markers normalized against a fixed saturation count), `keyword_coverage` (the fraction of the document's declared `Topics:` subjects that resolve to the snapshot's keyword vocabulary), and `link_degree` (the document's snapshot edge degree — cluster document edges plus `destinations` staged topics, changes, and capabilities — normalized against a fixed saturation degree). Every signal SHALL be reported as a named normalized value beside the raw count that produced it, so a rendered bar is explainable. The computation MUST be deterministic and reproducible from the pinned tree alone: no model call, no wall clock, no network, no judgment input of any kind, with the `score` a fixed-weight combination of the normalized signals at a fixed decimal precision — the weights are contract constants in v1 (a tunable configuration would be a successor change, never a per-run input). The signal SHALL be informational only: it MUST NOT be an input to the readiness recommendation gate, MUST NOT produce a doc-health finding, and no gate verb, console guard, or lifecycle transition may consult it or refuse on it. Growth is additive — the field is optional, no existing snapshot is invalidated, and a renderer reading a pre-growth snapshot MUST degrade to showing no completeness rather than failing.

#### Scenario: The generator runs twice on the same tree
- **WHEN** the generator runs twice over an unchanged working tree
- **THEN** every document's `completeness` score and signals MUST be identical and the snapshot MUST stay byte-identical

#### Scenario: A document grows sections and links
- **WHEN** a document gains expected sections and gains edges (a new declared topic matching a cluster, or a new downstream destination) between two generations
- **THEN** its `structure` and `link_degree` signals MUST rise and its `score` MUST be strictly higher than the earlier generation's

#### Scenario: A stub scores low without becoming a defect
- **WHEN** a document carries only its headers, a short body, and standing TODO markers
- **THEN** it MUST score low on `structure`, `length`, and `open_markers`
- **AND** no doc-health finding, refusal, or lifecycle consequence MUST follow from the score

#### Scenario: A score is asked to gate an action
- **WHEN** any surface — the readiness recommendation gate, a console verb's guard, or a lifecycle transition — would consult a completeness score to allow or refuse
- **THEN** it MUST NOT — completeness is informational and gating stays with the human gate console and the governed readiness contract

#### Scenario: A signal would require judgment
- **WHEN** a proposed completeness signal cannot be computed from the pinned tree without model judgment
- **THEN** it MUST NOT enter v1 scoring — the signal set stays the five deterministic signals, and semantic assessment remains the agentic sweep's and the readiness panel's own capabilities

#### Scenario: A snapshot predates the field
- **WHEN** a renderer reads a snapshot generated before this growth landed
- **THEN** it MUST render the document list with no completeness bars and MUST NOT compute the signal itself

### Requirement: Staging workbench scoped view
The dashboard SHALL provide a staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — presenting three tabbed panels over that one scope. The `docs` panel SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them. The `lens` panel SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. The `outline` panel SHALL render the topic's outline when one exists — for a staged topic, the fragment's outline material — read through the same read-only `/source` pass-through the document viewer uses, and MUST show an explicit empty state when the scope carries no outline. The workbench SHALL be read-only in every panel: it MUST write no document, no register entry, no workbench manifest, and no gate artifact, and outline editing is out of scope here.

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
- **AND** the `outline` panel renders that fragment's outline material read-only

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

#### Scenario: The workbench is asked to write
- **WHEN** any workbench panel would write a document, a register entry, a workbench manifest, or a gate artifact
- **THEN** the write MUST be rejected and reported — this surface is read-only and every write path arrives in a later change

### Requirement: Workbench tile action
The wheel's expanded tile SHALL offer an `open workbench` action on the clusters, possibles, and staged wheels, mounted through the wheel's established per-wheel action-row extension point (one row in the pure action table plus one mounter entry, as `add-wheel-action-verbs` describes — not re-specified here), and the action SHALL carry NO gate capability requirement because it writes nothing: it is a read-only navigation verb like the existing read, lens, canvas, and landed verbs, offered whether or not the gate capability is live and therefore present on the deployed static image, where content-dependent panels degrade inline. The action SHALL open the workbench scoped to the tile it was activated from, and the wheels whose tiles are not topic-bearing SHALL NOT offer it.

#### Scenario: A topic-bearing tile offers the workbench
- **WHEN** a human expands a cluster, possible, or staged tile
- **THEN** the action row MUST include the workbench action
- **AND** activating it opens the workbench scoped to that tile

#### Scenario: The gate capability is off
- **WHEN** the loopback gate capability is unavailable
- **THEN** the workbench action MUST still be offered — it writes nothing and needs no gate

#### Scenario: A non-topic-bearing tile is expanded
- **WHEN** a human expands a document, active-change, or archived-change tile
- **THEN** the workbench action MUST NOT appear on that row
