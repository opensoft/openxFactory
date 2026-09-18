# ideation-dashboard

## ADDED Requirements

### Requirement: The served plane's baked artifacts are rebaked on a schedule at one revision
The served plane's BAKED artifacts — the fallback snapshot and the baked governed-corpus tree the read-only `/source` pass-through resolves against — SHALL be refreshed by a scheduled rebake lane, and every rebake MUST bake them at ONE revision: the snapshot SHALL be generated from the same corpus checkout whose roots are baked, so the snapshot's `source_revision` and the baked `/source` tree name the same commit by construction rather than by an operator's care. A rebake MUST NOT publish an image whose snapshot failed strict validation. The rebake SHALL reach the served plane only as a DIGEST pin proposed to the runtime install layer's own delivery path, never as an apply performed by the rebake lane: the dashboard's machinery holds no cluster authority, and this lane is machinery.

The one-revision rule exists to keep the freshness header honest. The header names the active snapshot's `source_revision`, and the document viewer serves the baked tree; an image whose snapshot names revision X while its `/source` tree carries revision Y presents a freshness claim the viewer cannot satisfy, and every document that landed between the two revisions resolves to nothing. A two-revision image is therefore a defect of the rebake, not a tolerable approximation.

#### Scenario: A scheduled rebake produces an image
- **WHEN** the rebake lane builds a served-plane image
- **THEN** the baked snapshot and the baked corpus roots MUST come from one checkout at one revision, and the snapshot MUST have passed strict validation
- **AND** the freshness header the resulting image displays MUST be satisfiable by the `/source` tree in that same image

#### Scenario: A rebake would mix revisions
- **WHEN** a realization would bake a previously committed snapshot alongside a freshly checked-out corpus, or a fresh snapshot over a corpus from a different revision
- **THEN** it MUST be rejected — the two artifacts are one fact about one revision

#### Scenario: The rebake lane is asked to deploy
- **WHEN** any path would have the rebake lane apply its own image to the serving host, or hold a credential that could
- **THEN** it MUST be refused — the lane proposes a digest pin and the runtime install layer's own delivery path applies it

## MODIFIED Requirements

### Requirement: Runtime snapshot fetch with baked fallback and displayed freshness
The served dashboard SHALL fetch the index and the active snapshot at RUNTIME from a declared external data source, and the served image SHALL bake the APPLICATION rather than the data — an image rebuild MUST NOT be required to reflect newly published snapshots. The runtime fetch SHALL be performed by the SERVING side into the snapshot registry, and the browser bundle MUST continue to address only its own origin, preserving the bundle's existing no-external-network boundary. A snapshot MAY remain baked into the image as a FIRST-BOOT and OFFLINE fallback ONLY. Whenever the fallback is what renders, the surface MUST display a stale banner naming the fallback's generated-at, and it MUST NEVER degrade to fallback data silently. Every view SHALL display a freshness header naming the active repository and ref, the active snapshot's `source_revision` in short form, and its generated-at, so the question "is the document I just landed in this view" is answerable without reasoning about deployment times.

The baked fallback's STALENESS SHALL be bounded rather than left to whenever the image was last built: a scheduled rebake keeps the baked snapshot and the baked `/source` corpus within a stated bound of the corpus's `main`, and that bound SHALL be stated wherever the served plane is documented. Bounding the fallback does NOT make rebuilds the data path, and this addition MUST NOT be read as licence to treat them as one — the rule above stands unchanged: reflecting newly PUBLISHED data requires no rebuild.

Two facts about the baked side SHALL be recorded rather than left to be inferred from a Dockerfile. First, the runtime fetch covers the INDEX and the SNAPSHOT; it does not cover the baked corpus tree the `/source` document viewer resolves against, so that tree goes stale on the IMAGE's cadence regardless of how fresh the fetched snapshot is, and a fresh snapshot over a stale corpus is the worse of the two failures because every document that landed since the bake resolves to nothing. Second, a served plane on which the runtime fetch is NOT YET realized is reading its baked artifacts AS its data, which makes the rebake cadence that plane's data cadence; that state SHALL be recorded as a conformance GAP against this requirement, with the rebake bound as its mitigation, and MUST NOT be presented as the intended design.

#### Scenario: The data source is reachable
- **WHEN** the served dashboard starts or refreshes with the data source reachable
- **THEN** it MUST render the fetched snapshot, not the baked one
- **AND** the freshness header MUST name the active repository and ref, the snapshot's short `source_revision`, and its generated-at

#### Scenario: The data source is unreachable
- **WHEN** the index or the active snapshot cannot be fetched
- **THEN** the baked snapshot MUST render as the fallback
- **AND** a stale banner MUST state that the fallback is in use and name its generated-at — the degradation MUST NOT be silent

#### Scenario: A newly published snapshot needs no rebuild
- **WHEN** the publication lane publishes a newer snapshot for the active repository
- **THEN** reflecting it MUST require no image rebuild and no rollout

#### Scenario: The browser is asked to reach the data source
- **WHEN** any realization would have the browser bundle fetch the external data source directly
- **THEN** it MUST be rejected — the serving side performs the fetch and the bundle stays same-origin

#### Scenario: The baked fallback ages without bound
- **WHEN** a served plane's baked snapshot or baked corpus is older than the stated rebake bound
- **THEN** it MUST be treated as a defect of the rebake schedule, not as an acceptable steady state

#### Scenario: A served plane has no runtime fetch yet
- **WHEN** a served plane serves only its baked snapshot and baked corpus because the runtime fetch is not yet realized on it
- **THEN** that plane's data cadence IS its rebake cadence, and the situation MUST be recorded as a conformance gap against this requirement rather than described as the design
- **AND** the rebake bound MUST be the stated mitigation until the runtime fetch is realized
