# codexFactory Neutrality Sweep — Evidence Record

Status: record
Kind: analysis
Captured: 2026-08-03
Source: repo-wide sweep of xFactories/codexFactory against the
domain-neutral boundary, commissioned by Brett Heap during the
2026-08-03 housekeeping session; produced by an exploration agent over
the live tree and cross-referenced against the aggregation CLAUDE.md and
openxFactory docs/specs.

## Headline

~73,200 LOC of neutral-or-neutral-in-purpose source (plus ~47,900 test
LOC) is hosted in the engineering domain repo, against a domain-
legitimate core (Hermes/Omnigent content, credentials families, 13
engineering schemas, 18 engineering workflows, execution_lane +
merge_master) more than an order of magnitude smaller. None of the
neutral tooling appears in codexFactory's own stack.yaml declared-
artifact inventory.

## Ranked findings (strongest first)

1. **`scripts/doc_health/`** (21 py, 13,530 LOC + prompts; tests 11,863
   LOC). Deterministic 14-family governance-corpus checker. Own docstring:
   "codexFactory's implementation of the promoted openxFactory doc-health
   contract." Hardcodes openxFactory-only knowledge (DTN register path;
   families skip when openxFactory absent); zero engineering vocabulary;
   test fixtures model MedxFactory and openxFactory. Consumed by the
   aggregation nightly via `uses: opensoft/codexFactory/...` — the
   workspace-wide nightly for 14+ repos calls into a private domain repo.
   Neutral schemas cite its file paths (the clearest layering violation):
   `xfactory-document-catalog-snapshot.schema.yaml:17,:57`,
   `validate-document-catalog.py:527`.
2. **`scripts/ideation_dashboard/` + `web/`** (20,097 + 12,575 LOC; tests
   32,378 LOC). Snapshot generator, served renderer, gate console,
   workbench, branch sessions, nightly lane. Self-declares as the codex
   realization consuming the five openxFactory contract schemas
   read-only. Proven neutral in operation: the 2026-07-25 drive snapshot
   ran Medx/Adx/Ledgerx with the UNMODIFIED generator; 16 per-repo
   snapshots live in the aggregation `health/ideation-dashboard/`;
   roster is the aggregation-owned project-register.yaml. Codex-flavored
   mechanism: branch_session/session_git/session_pr (~5,600 LOC) — git
   verbs applied to governance docs in ANY repo. Single truly
   codex-specific line: kickoff.py DEFAULT_WORKFLOW.
3. **`scripts/sync-notebooklm-books.py`** (1,205 LOC; tests 1,467).
   Self-declares "Reference implementation of the openxFactory
   lifecycle-notebook-projection capability." Workspace-rooted; the
   workspace CLAUDE.md canonical command reaches into codex; openxFactory
   docs invoke it 8×; the neutral example workspaces file names it
   `managed_by` 3×; doc-health family 12 shells out to it.
4. **Routing/organizer/possibles lanes inside doc_health** (~5,594 LOC):
   ideation_routing, organizer(+dispatch), ideation_readiness,
   derive_possibles(+dispatch). The active add-cross-factory-ideation-
   routing change NORMATIVELY assigns codexFactory the orchestration —
   a cross-factory capability implemented inside one factory.
   Producer/consumer inversion: openxFactory's ideation/
   cross-reference.yaml is produced by the codex scorer while openxFactory
   owns bootstrap/render/validate.
5. **Three conformance-gate checks** (~310 LOC): check-inventory-
   consistency, check-workflow-state-parity, check-openxfactory-pin.
   Generic domain-repo checks; openxFactory hosts this class and rules
   "never copied into domain repos"; one duplicates
   validate-domain-openxfactory-pins.py.
6. **`scripts/proposal-support.py`** (545 LOC): zero domain vocabulary;
   the neutral doc-health contract checks the artifacts only it creates.
7. **`apps/avatar-client-lab/`** (22,862 LOC Dart): neutral in purpose
   (reference client of the neutral standard; ships a MedxFactory demo
   profile) but openxFactory's avatar-reference-runtime spec FORBIDS
   deployable surfaces — needs a neutral non-openxFactory home.
8. **`workflows/change-ratification.{md,yaml}`**: pure governance sidecar,
   zero engineering vocabulary; promote a neutral reference contract
   rather than relocating the codex instance.
9. **Review lane change-review half** (of 2,085 LOC): ten governance-doc
   review dimensions; resolves targets across all submodules; PR half is
   legitimately engineering.

## Infrastructure misplaced toward the AGGREGATION repo (not openxFactory)

- CloudPC runner readiness: doc_health/readiness.py (190) +
  readiness_dispatch.py (436).
- docs/council-lane-app-registration.md — configures variables/secrets
  that all live in the aggregation repo.
- Credential tax evidence: merge-master-approval.yml and
  council-convening-lane.yml mint a GitHub App token solely because
  codexFactory is a private sibling.

## Already registered / already staged (do not double-file)

- schemas/deployment-profile.schema.json → DTN-011 evidence (seed).
- docs/project-memory-fill-maintenance-mapping.md → DTN-012 evidence.
- Dashboard runtime-plane neutralization → staged dashboard-repo-selector
  exit 2 (this change relocates implementation only; see design D7).

## Verified legitimately codex-specific (stays)

hermes/ (8 engineering personas, policies, ontology, councils),
omnigent/ (engineering worker classes), credentials/ (six engineering
access families — DTN-004's intended instantiation), tenants/,
examples/golden-path/, 13 of 17 schemas, 9 of 10 workflows,
scripts/execution_lane/, scripts/merge_master/ (engineering mechanism;
its aggregation-repo consumer is a separate misplacement),
catalog/ (per-domain by contract), docs/document-catalog-adoption.md
(deliberate per-domain mirror), .specify/ (workspace-wide harness),
the engineering docs family (DTN-013's landing zone).
