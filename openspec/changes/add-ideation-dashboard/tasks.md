# Tasks: Ideation Area Dashboard

## 1. Sequencing And Contract Baseline

- [ ] 1.1 Sequence the `ideation-cross-reference` delta with the active `add-ideation-cross-reference-readiness` change: verify at realization that the promoted (or pending) wording matches what this change's delta was declared against, rebase if needed, and re-run strict OpenSpec validation.
- [ ] 1.2 Verify this change's staged-origin `.openspec.yaml`, support-manifest origin repetition, and staging-header linkage.

## 2. Contracts And Schemas (openxFactory)

- [ ] 2.1 Define the `ideation-dashboard-snapshot` schema (kind + schema_version + repository field): per-doc stage/kind/summary/topics/dates/destination links, cluster entries with doc edges, possibles with states and pick citations, staged-topic rows, change entries with code_surface/target_release, readiness scores and conflict flags once the cross-reference index supplies them.
- [ ] 2.2 Define the `ideation-workbench` manifest schema (kind + schema_version): member references, seed provenance (cluster-seeded vs ad-hoc), action history, scratch-notebook binding.
- [ ] 2.3 Define the possibles-register consolidation contract in the cross-reference index: `Possible feats:` ingestion, states `latent/picked/rejected/superseded`, reason + citation requirements, pick edges citing staging IDs and inheriting change IDs at the proposal gate.
- [ ] 2.4 Add valid and invalid examples (multi-cluster possible, cited rejection, uncited rejection failing, pick edge inheritance, ad-hoc human-seen cluster submission) and a strict validator for snapshot, workbench manifest, and register transitions wired into the per-repo validator preflight; add `ideation/workbench/` to the repo gitignore with committed-manifest detection.
- [ ] 2.5 Register the schemas in `contracts/manifest.yaml`, reconcile `contracts/CHANGELOG.md`, and update ideation guidance (`Possible feats:` seeding in the README header-format section) referencing promoted requirements without duplicating them.
- [ ] 2.6 Define the `project-register` schema (kind + schema_version; D10): named projects with repository membership, project groups with project membership; valid/invalid examples (multi-repo project, ungrouped repository, empty group rejected) and validator wiring alongside 2.4; the register instance lands in the aggregation/workspace repo, not openxFactory.

## 3. Generator And Renderers (codexFactory)

- [ ] 3.1 Implement the deterministic snapshot generator (same tree in, same snapshot out) over `ideation/` plus active and archived changes, with the R4 fixture backfill (doc-health, avatar, ideation-governance, DTN register worked examples) and no historical fabrication.
- [ ] 3.2 Grow the staged mockup skeleton into the repo-tracked static renderer: six-column funnel with link-counted tallies and the five-column collapse mode, pipeline board with possibles badges, doc list, lineage, readiness heat, health overlay, stats strip — all reading only the adjacent snapshot.
- [ ] 3.3 Implement the local generate-and-open command.
- [ ] 3.4 Implement workbench actions: scratch `xf-wb-*` notebook creation/deletion with the sync orphan sweep, on-demand readiness scoring, scoped doc-health, and the draft-organize action that pre-fills a `staging/<topic>/` packet skeleton for human review without writing into `ideation/staging/`.
- [ ] 3.5 Implement human-seen-cluster submission under the full organizer/cataloger evidence contract with `pending_review` disposition.
- [ ] 3.6 Implement human authoring: a create action scaffolding a header-compliant doc (H1, Status, Kind, Summary, Topics, Repository context, Captured pre-filled) into the chosen ideation area, and select-to-edit opening any listed doc in the human's editor; the dashboard itself never rewrites content.
- [ ] 3.7 Enforce agent create-only authority: any agent write path can add new corpus docs with required headers but MUST reject and report edits or deletions of existing docs; notebook doc/source deletion drops the set reference only (workbench manifests) while lifecycle projections restore their sets on the next sync.
- [ ] 3.8 Implement project grouping (D10): generator resolves `repository` → `project` → `project_group` from the project register into the snapshot; renderer adds repo/project/group roll-up controls to the funnel, pipeline board, and stats strip, with ungrouped repositories rendering as their own implicit project.

## 4. Nightly Lane (xFactory aggregation)

- [ ] 4.1 Add the deterministic snapshot-generation lane to the nightly run after the deterministic pass, committing the snapshot beside the dated doc-health reports; a skipped or failed lane is reported as skipped and never affects deterministic results.
- [ ] 4.2 Serving (Option C, owned by Omnigent-Install / the runtime install layer): add an access-controlled static-serving route on the existing internal xForge host — a path or sibling ingress on the Azure Kubernetes cluster that already fronts `hermes-readiness.xforge.us` (`installs/omnigent-install/k8s/azure/hermes-readiness/ingress.yaml`) — that serves the committed renderer + nightly snapshot read-only behind the same access control, never a public endpoint. openxFactory owns only the requirement (spec: Delivery and regeneration); the ingress/static-serve mechanics land in Omnigent-Install and are referenced here without duplicating its task list. Local generate-and-open (3.3) remains the zero-infra fallback.

## 5. Tests And Records

- [ ] 5.1 Tests: snapshot and manifest schema validation; determinism; register transitions (uncited rejected/superseded fails); boundary (generator and workbench actions write only under their own output paths; no automated writes to `ideation/staging/` or existing source docs); scaffold header compliance; agent edit/delete rejection and reporting; notebook set-removal leaves the corpus doc intact and projections restore on sync; funnel fixtures from the R4 backfill; orphan-sweep removal of unbound `xf-wb-*` notebooks; committed workbench manifest detection; project-register validation and grouping roll-up (multi-repo project aggregation, ungrouped repository fallback, group tallies).
- [ ] 5.2 Obtain realization evidence (green nightly snapshot lane plus a working local generate-and-open run) and keep the openxFactory README "OpenSpec Records" entry current through ratification, realization, and archive.
