# ideation-dashboard Delta: Staging Workbench (read-only foundation)

## ADDED Requirements

### Requirement: Deterministic per-document completeness signal
The snapshot generator SHALL compute a per-document completeness signal at generation time and emit it as an additive `completeness` object on each `documents[]` entry — a `score` plus five named signals: `structure` (the fraction of the document's expected structural elements present, the expected set fixed per `Kind:` with a common fallback — H1 title, the governance header block, at least one section), `length` (body size normalized against a fixed saturation threshold, so padding past the threshold cannot outscore substance), `open_markers` (an INVERSE signal over open-question / TODO / TBD markers normalized against a fixed saturation count), `keyword_coverage` (the fraction of the document's declared `Topics:` subjects that resolve to the snapshot's keyword vocabulary), and `link_degree` (the document's snapshot edge degree — cluster document edges plus `destinations` staged topics, changes, and capabilities — normalized against a fixed saturation degree). Every signal SHALL be reported as a named normalized value beside the raw count that produced it, so a rendered bar is explainable. The computation MUST be deterministic and reproducible from the pinned tree alone: no model call, no wall clock, no network, no judgment input of any kind, with the `score` a fixed-weight combination of the normalized signals at a fixed decimal precision — the weights are contract constants in v1 (a tunable configuration would be a successor change, never a per-run input). The per-document signal SHALL stay out of judgment surfaces: it MUST NOT be an input to the readiness recommendation gate and MUST NOT produce a doc-health finding; its ONE sanctioned gate consumer is the staged-to-proposal readiness gate defined in this change, which consumes document scores only through the staged-topic health aggregate — no other gate verb, console guard, or lifecycle transition may consult it or refuse on it (Brett's 2026-07-25 ruling supersedes this change's earlier informational-only bound). Growth is additive — the field is optional, no existing snapshot is invalidated, and a renderer reading a pre-growth snapshot MUST degrade to showing no completeness rather than failing.

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
- **WHEN** any surface OTHER than the staged-to-proposal readiness gate — the readiness recommendation gate, another console verb's guard, or a lifecycle transition — would consult a completeness score to allow or refuse
- **THEN** it MUST NOT — the readiness gate consumes document scores only through the staged-topic health aggregate, and every other consumer treats completeness as information

#### Scenario: A signal would require judgment
- **WHEN** a proposed completeness signal cannot be computed from the pinned tree without model judgment
- **THEN** it MUST NOT enter v1 scoring — the signal set stays the five deterministic signals, and semantic assessment remains the agentic sweep's and the readiness panel's own capabilities

#### Scenario: A snapshot predates the field
- **WHEN** a renderer reads a snapshot generated before this growth landed
- **THEN** it MUST render the document list with no completeness bars and MUST NOT compute the signal itself

### Requirement: Staged-topic health signal
The snapshot generator SHALL compute a per-staged-topic health aggregate at generation time and emit it as an additive `health` object on each `staged_topics[]` entry, derived exclusively from the topic FOLDER's own corpus documents — documents that merely declare the topic as a destination are context, never health inputs. The object SHALL carry `standing_open_items` (the sum of the member documents' `open_markers` raw counts), `doc_score_min` and `doc_score_mean` (over the member documents' completeness scores, at the same fixed decimal precision), a `blockers` array of typed, explainable reasons (each standing-open-items document with its count; each document whose score falls below the ready threshold, with the score and the constant), and a derived `status`: `ready` when the blockers array is empty, `stub` when the folder carries no corpus documents, `developing` otherwise. The ready threshold is a contract constant in v1 (`READY_MIN_SCORE`), pinned beside the completeness weights and calibrated at realization — never a per-run input. The computation MUST be deterministic and reproducible from the pinned tree alone, exactly as the per-document signal is. The aggregate SHALL NOT be a readiness judgment: it MUST NOT feed the readiness recommendation gate or re-score any readiness tier, and no cluster or possible gains any aggregate. Growth is additive — the field is optional and a pre-growth snapshot stays valid.

#### Scenario: A topic carries standing open questions
- **WHEN** any of the topic folder's corpus documents carries standing open-question / TODO markers
- **THEN** the topic's `status` MUST NOT be `ready`
- **AND** `blockers` MUST name each such document with its standing count

#### Scenario: A topic is worked to done
- **WHEN** every member document's standing open markers reach zero and every member document's score is at or above the ready threshold
- **THEN** the topic's `blockers` MUST be empty and its `status` MUST be `ready`

#### Scenario: A topic folder is a stub
- **WHEN** a staged topic's folder carries no corpus documents
- **THEN** its `status` MUST be `stub`

#### Scenario: Health is deterministic
- **WHEN** the generator runs twice over an unchanged working tree
- **THEN** every staged topic's `health` object MUST be identical and the snapshot MUST stay byte-identical

#### Scenario: Health is mistaken for readiness
- **WHEN** the readiness recommendation gate, a readiness tier, or any cluster/possible surface would consume the health aggregate
- **THEN** it MUST NOT — health is a structural doneness signal for staged topics, and the governed readiness judgment keeps its own authorities

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

### Requirement: Staged-to-proposal readiness gate
The gate console's `propose` action SHALL refuse to commission proposal authoring for a staging topic whose health status is not `ready`, so a topic cannot move from staging toward proposal while open questions stand or its documents fall short of the ready threshold. The guard SHALL be enforced at the propose route itself, so every surface that reaches it — the staged tile's action, the CLI, a direct request — is gated identically, and it adds to (never replaces) the existing refusals for a missing topic and a duplicate commission. The check MUST be evaluated live against the pinned checkout at request time using the same deterministic scoring the generator uses — never against the served snapshot, which may be stale. A refusal SHALL cite the topic's blockers concretely (each document with standing open items and its count; each document below the threshold with its score and the constant) and SHALL persist nothing, exactly like the existing propose refusals. The gate consumes per-document completeness ONLY through the staged-topic health aggregate, and the action remains human-only as the commissioning requirement prescribes.

#### Scenario: A topic with standing open questions is proposed
- **WHEN** a human runs propose on a staging topic whose folder documents carry standing open-question markers
- **THEN** the console MUST refuse, naming each document and its standing count, and persist nothing

#### Scenario: A topic with an underdone document is proposed
- **WHEN** a human runs propose on a topic whose every open question is closed but a member document's completeness score is below the ready threshold
- **THEN** the console MUST refuse, citing that document's score against the contract constant, and persist nothing

#### Scenario: A ready topic is proposed
- **WHEN** a human runs propose on a topic whose live-computed health is `ready`
- **THEN** the commission proceeds exactly as the staged-topic proposal commissioning requirement prescribes — descriptor plus gate-action record

#### Scenario: The snapshot and the checkout disagree
- **WHEN** the served snapshot shows a topic `ready` but the pinned checkout has since gained a standing open marker in that topic's folder
- **THEN** the live evaluation governs and the console MUST refuse, citing the marker the snapshot has not yet seen

### Requirement: Staged tile health display
The wheel's staged tiles SHALL surface the topic's health at two levels matching the tile interaction model: the FOCUSED (centred, first-click) tile face SHALL carry a compact health indicator showing the tri-state status, and the EXPANDED (second-click) tile SHALL render the full health block — status, standing open items with each document's count, the doc score minimum and mean, and the blockers list — VERBATIM from the snapshot's `health` object, never recomputing any value client-side. Resting drum faces SHALL stay unadorned. A renderer reading a pre-growth snapshot MUST show no indicator and no health block rather than computing the signal itself. The display never gates: allowing or refusing stays with the server-side readiness gate, whose refusal message is the authoritative account when the snapshot has drifted from the checkout.

#### Scenario: A staged tile is focused
- **WHEN** a human clicks a staged tile to centre it
- **THEN** the focused tile face MUST show the compact health indicator reflecting the snapshot's `status`

#### Scenario: A focused staged tile is expanded
- **WHEN** the human clicks the centred staged tile again
- **THEN** the expanded tile MUST render the full health block, including every blocker, verbatim from the snapshot

#### Scenario: The snapshot predates the health field
- **WHEN** the renderer reads a snapshot with no `health` object on a staged topic
- **THEN** the tile MUST render with no indicator and no health block, and MUST NOT compute health itself

#### Scenario: The display disagrees with the gate
- **WHEN** a tile shows `ready` from a stale snapshot but the live gate refuses the propose
- **THEN** the refusal's cited blockers are the authoritative account and the display MUST NOT suppress or restate the refusal
