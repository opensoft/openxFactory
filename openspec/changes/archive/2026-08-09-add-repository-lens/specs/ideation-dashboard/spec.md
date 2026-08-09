# ideation-dashboard

## ADDED Requirements

### Requirement: The lens serves a repository vocabulary
The lens SHALL offer a REPOSITORY vocabulary alongside its keyword vocabulary wherever the rendered snapshot is composed, presenting the project's member repositories as the rail, one dot per cross-repository document IDENTITY, and rings by CARRIER COUNT — how many visible repositories carry that identity, the centre being every one of them. The two vocabularies SHALL be served by the same derivation, geometry, and renderer: the repository plane is supplied by re-expressing the composed snapshot in the shape the lens already reads, so no vocabulary-specific engine exists. Where the snapshot is not composed the switch SHALL NOT render and the keyword lens SHALL behave exactly as before. The repository rail's ticks ARE the view's visible member set: the lens SHALL open on the current set, write changes back so the project filter and the lens never disagree, and redraw from the aggregate it already holds rather than reloading.

#### Scenario: The repository lens draws carrier rings
- WHEN a human switches the lens to the repository vocabulary on a composed view
- THEN the rail lists the member repositories with their identity counts, and each document identity is a dot on the ring for the number of visible repositories carrying it
- AND the centre holds the identities every visible repository carries

#### Scenario: A tick moves both controls
- WHEN a human unticks a repository in the lens rail
- THEN the visible set records that change and the project filter reflects it
- AND the lens redraws over the remaining set without reloading the shell

#### Scenario: A single-repository view offers no repository vocabulary
- WHEN the rendered snapshot is not composed
- THEN no vocabulary switch renders and the keyword lens is unchanged

### Requirement: Drill-in scopes the dashboard to a region's documents
Activating a region of the repository bullseye — its centre, or a sector naming an exact repository combination — SHALL scope the whole dashboard to the documents behind that region, and the activation SHALL be reachable both from the region itself and from a labelled control beside it, because a hit region alone is undiscoverable. The scope is a DOCUMENT SET: every other plane SHALL keep only what references it — a cluster with an edge into the set, a change or staged topic with a file path in it, a keyword a kept document still declares — and planes with no document relationship SHALL be left alone rather than silently emptied. A scope SHALL be stated on screen with the count of documents, the count of identities behind them, and the repository combination, and SHALL be clearable from that statement.

#### Scenario: A sector scopes the shell to its documents
- WHEN a human activates a sector naming a repository combination
- THEN every view renders only the documents whose identity is carried by exactly that combination, one document per carrying repository
- AND clusters, changes and staged topics narrow to those that reference the kept documents

#### Scenario: The scope states itself and clears
- WHEN a drill-in scope is active
- THEN the shell states the document count, the identity count, and the combination scoped to
- AND clearing it restores the full visible-set view
