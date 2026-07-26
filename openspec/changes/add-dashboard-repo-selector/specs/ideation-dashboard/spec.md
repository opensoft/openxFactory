# ideation-dashboard Delta: Repository Selector, (repository, ref) Snapshot Source, Refresh

## ADDED Requirements

### Requirement: Repository selector over the registered roster
The dashboard SHALL offer a repository selector whose roster is the repositories the project register declares, and MUST NOT maintain a second repository list of its own. Selecting a repository SHALL switch the ACTIVE snapshot to that repository at the default ref, after which every view renders from that one snapshot exactly as it does today. A repository whose corpus populates only SOME funnel stations SHALL render the stations it has data for and MUST NOT be refused, hidden, or degraded as a whole: adoption of any ideation convention MUST NEVER be a precondition of being selectable, and a station with no data in the selected repository MUST render an explicit empty state naming what is absent rather than a blank region. A repository present in the snapshot index but absent from the register SHALL remain selectable and render ungrouped, as the grouping hierarchy already requires. A selection naming an aggregate view across repositories SHALL compose from the snapshot index and the per-repository snapshots it names, and MUST NOT scan any repository directly.

#### Scenario: A human switches repositories
- **WHEN** a human selects a different repository in the selector
- **THEN** every view MUST re-render from that repository's snapshot, addressed at the default ref
- **AND** the roster offered MUST be the project register's repositories, not a list maintained by the dashboard

#### Scenario: A sparse repository is selected
- **WHEN** the selected repository's snapshot populates only some funnel stations — for example an install repository carrying only OpenSpec changes
- **THEN** the populated stations MUST render and the unpopulated ones MUST show an explicit empty state
- **AND** the repository MUST NOT be refused or hidden for lacking a convention

#### Scenario: A repository is missing from the register
- **WHEN** the index names a repository the project register does not
- **THEN** it MUST still be selectable and render ungrouped, without failing the dashboard

#### Scenario: An aggregate selection is rendered
- **WHEN** a selection spans repositories rather than naming one
- **THEN** it MUST compose from the index and the snapshots it names
- **AND** MUST NOT read any repository working tree directly

### Requirement: Snapshot source keyed by repository and ref
Every snapshot the dashboard reads SHALL be addressed by the PAIR (repository, ref), and a request that names no ref MUST resolve to `main`. The serving layer SHALL keep ONE snapshot registry keyed by that pair, and every renderer, index entry, and refresh binding MUST address snapshots through it rather than through a path convention of its own. The seam MUST carry `ref` from the first release even while only `main` is exercised, so a later session-scoped or runtime-plane consumer binds to it without the interface being re-cut. The served plane SHALL exercise only `(repository, main)`: a snapshot generated for any other ref is session-local derived data, MUST NEVER be published to the data source, MUST NEVER appear in the index the served plane fetches, and MUST NEVER become a shared view — main remains the shared truth on every shared surface. Source confinement SHALL hold per registry entry, so reading a document through a (repository, ref) entry MUST NOT be able to escape that entry's own root.

#### Scenario: A caller names no ref
- **WHEN** any renderer, refresh binding, or command requests a snapshot for a repository without naming a ref
- **THEN** it MUST resolve to that repository's `main` snapshot
- **AND** an existing consumer that never names a ref MUST keep working unchanged

#### Scenario: Two refs of one repository are registered
- **WHEN** the registry holds entries for the same repository at two different refs
- **THEN** each MUST serve its own snapshot and its own source root, with no cross-contamination between them

#### Scenario: A non-main snapshot is offered for publication
- **WHEN** any path would publish a snapshot for a ref other than `main`, or enter one into the served plane's index
- **THEN** it MUST be refused — non-`main` snapshots are session-local derived data and never shared state

### Requirement: Snapshot index contract
The available snapshots SHALL be enumerated by a thin, schema-versioned snapshot INDEX artifact carrying one entry per available (repository, ref) with that entry's repository, ref, snapshot location, `source_revision`, and generated-at stamp. The index SHALL be declared by its OWN contract and MUST NOT be folded into the snapshot schema: an index describes a SET of snapshots while a snapshot describes one repository's corpus at one revision, so carrying sibling facts inside a snapshot would break the determinism property that the same working tree yields a byte-identical snapshot. Each (repository, ref) pair MUST be unique within one index. The index MUST carry no funnel, document, cluster, possible, or keyword data — it is a locator, not a projection. Renderers and refresh bindings SHALL discover available snapshots only through the index, and an index entry whose snapshot cannot be fetched MUST be reported as that repository being unavailable, leaving the active view unaffected.

#### Scenario: A repository becomes available
- **WHEN** the publication lane adds an entry to the index for a newly registered repository
- **THEN** the selector MUST offer that repository with no application change and no image rebuild

#### Scenario: An indexed snapshot cannot be fetched
- **WHEN** an index entry names a snapshot the serving side cannot retrieve
- **THEN** that repository MUST be reported unavailable and the currently active view MUST continue to render

#### Scenario: The index is asked to carry projection data
- **WHEN** a change would add document, cluster, possible, or keyword data to the index
- **THEN** it MUST be rejected — that data belongs to the snapshot the index locates

### Requirement: Runtime snapshot fetch with baked fallback and displayed freshness
The served dashboard SHALL fetch the index and the active snapshot at RUNTIME from a declared external data source, and the served image SHALL bake the APPLICATION rather than the data — an image rebuild MUST NOT be required to reflect newly published snapshots. The runtime fetch SHALL be performed by the SERVING side into the snapshot registry, and the browser bundle MUST continue to address only its own origin, preserving the bundle's existing no-external-network boundary. A snapshot MAY remain baked into the image as a FIRST-BOOT and OFFLINE fallback ONLY. Whenever the fallback is what renders, the surface MUST display a stale banner naming the fallback's generated-at, and it MUST NEVER degrade to fallback data silently. Every view SHALL display a freshness header naming the active repository and ref, the active snapshot's `source_revision` in short form, and its generated-at, so the question "is the document I just landed in this view" is answerable without reasoning about deployment times.

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

### Requirement: Refresh affordances on both planes
The dashboard SHALL offer a refresh affordance, bound per plane, that grants NO authority the surface does not already have. On the SERVED plane refresh MUST re-fetch the index and the active snapshot into the registry and re-render, and MUST write nothing beyond that derived cache — fetching fresher derived data is a read. On the LOCAL plane refresh MUST re-run the snapshot generator against the served checkout and re-render, reachable only on a loopback bind, writing ONLY the derived snapshot artifact and mutating no governed content, with no server restart required. Neither binding MUST be able to trigger an image build, a rollout, a publication to the data source, or any write to a repository's governed content, and a refusal MUST leave the previously rendered snapshot in place rather than blanking the view.

#### Scenario: A document lands and the hosted viewer refreshes
- **WHEN** a document is committed to a repository's `main`, the publication lane runs, and a viewer clicks refresh on the served dashboard
- **THEN** the newly published snapshot MUST be fetched and the document MUST appear
- **AND** no image rebuild MUST have occurred and no write authority MUST have been exercised by the served surface

#### Scenario: A local author regenerates
- **WHEN** an author commits in the served checkout and uses the local refresh
- **THEN** the generator MUST re-run against that checkout and the document MUST appear without restarting the server
- **AND** only the derived snapshot artifact MUST have been written

#### Scenario: Refresh is asked to rebuild the app
- **WHEN** any refresh binding would trigger an image build, a rollout, or a publication
- **THEN** it MUST be rejected — refresh reads derived data and never executes a final action

#### Scenario: A refresh fails
- **WHEN** a refresh cannot complete
- **THEN** the previously rendered snapshot MUST remain rendered and the failure MUST be reported inline

#### Scenario: Newer data is advertised passively
- **WHEN** the served plane's background index poll (Brett's 2026-07-26 OQ2 ruling: passive hint, ~5-minute cadence) observes an index entry fresher than the loaded snapshot for the active repository
- **THEN** a passive newer-data hint MUST show on the surface
- **AND** the surface MUST NOT auto-reload — the view changes only when the viewer invokes refresh

### Requirement: Dispatchable publication, never from the served surface
The snapshot publication lane SHALL be manually dispatchable in addition to its schedule, so that an off-cycle data refresh is a governed CI action a human or a session triggers with an attributable run. The served dashboard MUST NOT be able to trigger publication, an image build, or a rollout by any path: a serving surface dispatches recorded requests at most and never executes a final action. A recorded-dispatch verb that would commission a rebake from the dashboard SHALL be out of scope here and MUST arrive, if ever, as its own change at its own gate. Off-cycle dispatch MUST change nothing else about the lane — the same generator, the same per-repository snapshots, the same index, the same commit posture as the scheduled run.

#### Scenario: An off-cycle refresh is needed
- **WHEN** a document lands shortly after the scheduled publication run
- **THEN** a human or a session MUST be able to dispatch the publication lane manually
- **AND** the dispatched run MUST produce the same artifacts as a scheduled run

#### Scenario: The dashboard is asked to commission a rebake
- **WHEN** any affordance on the served dashboard would trigger a build, a rollout, or a publication
- **THEN** it MUST be refused — the pod holds no build or rollout authority, and such a verb is a separate change at its own gate

## MODIFIED Requirements

### Requirement: Snapshot projection contract
The ideation dashboard SHALL be a generated projection, never a source of truth: a deterministic generator scans `ideation/` plus active and archived OpenSpec changes for ONE repository at ONE ref and emits one schema-versioned snapshot (`kind: ideation-dashboard-snapshot`, `schema_version`, and a `repository` field), and renderers SHALL read only snapshots, addressed by the (repository, ref) pair through the snapshot registry. When the dashboard disagrees with the repository, the dashboard is wrong and is regenerated. The generator SHALL be runnable for every registered repository, and the `repository` field plus the snapshot index are what make per-repository instances and an aggregate roll-up composable — no repository is privileged, and the earlier openxFactory-only scope is superseded.

#### Scenario: The generator runs twice on the same tree
- **WHEN** the generator runs twice over an unchanged working tree
- **THEN** it MUST emit byte-identical snapshots

#### Scenario: A renderer needs data the snapshot lacks
- **WHEN** a view requires information not present in the snapshot
- **THEN** the snapshot schema is extended by delta and the generator populates it
- **AND** the renderer MUST NOT scan the repository directly

#### Scenario: The dashboard disagrees with the repository
- **WHEN** rendered state diverges from repo state
- **THEN** the resolution is regeneration — dashboard artifacts are never hand-edited

#### Scenario: The generator runs for a second repository
- **WHEN** the generator is run against another registered repository
- **THEN** it MUST emit that repository's own snapshot under its own (repository, ref) address, with no change to any other repository's snapshot

### Requirement: Delivery and regeneration
The dashboard SHALL be delivered as a local generate-and-open command plus a publication lane that regenerates each registered repository's snapshot and publishes the snapshots and the index to a declared data source beside the dated doc-health reports. The served plane SHALL bake the APPLICATION — the renderer and its assets — and fetch its DATA at runtime from that source, keeping a baked snapshot only as a first-boot and offline fallback; the serving host is provided by the runtime install layer, and the dashboard MUST NOT be served from a public endpoint because the snapshot projects internal governance state. Regeneration is scheduled, on-demand, and manually dispatchable — still no per-commit regeneration. Dashboard artifacts remain generated: the served plane reads them, and neither the renderer nor a viewer ever hand-edits a snapshot or an index.

#### Scenario: An operator wants the current picture
- **WHEN** the local command runs
- **THEN** it regenerates the snapshot from the working tree and opens the renderer against it

#### Scenario: A team viewer opens the hosted dashboard
- **WHEN** a viewer opens the dashboard on the internal host
- **THEN** the host serves the baked application against the most recently fetched snapshot behind the existing access control, modifying neither

#### Scenario: A public endpoint is proposed
- **WHEN** any delivery path would serve the dashboard from a public, unauthenticated endpoint
- **THEN** it MUST be rejected — the snapshot projects internal governance state and is served only from an access-controlled internal host

#### Scenario: Only the application changes require a rebuild
- **WHEN** newly published data must be reflected on the served plane
- **THEN** an image rebuild MUST NOT be required — rebuilds are for application changes

#### Scenario: Backfill scope is exceeded
- **WHEN** generation would fabricate register history for documents outside the worked-example fixtures
- **THEN** it MUST NOT — legacy docs without `Possible feats:` sections simply carry no possibles
