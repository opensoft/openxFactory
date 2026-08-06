## 1. Dependency And Contract Baseline

- [x] 1.1 Complete, realize, and archive `add-doc-health-semantic-sweep` and `add-document-cataloging` without adding routing scope, then verify the promoted doc-health spec contains thirteen deterministic families plus its separate semantic pass.
- [x] 1.2 Rebase this change's doc-health delta onto that promoted wording, preserve `ideation-routing` as the fourteenth deterministic family, and run strict OpenSpec validation.
- [x] 1.3 Verify this change's staged-origin supporting-document manifest and hashes and leave general proposal-origin/archive-source-state policy to the staged `proposal-origin-contract` topic.

## 2. Neutral Routing Contracts

- [x] 2.1 Add canonical routing-record, `ideation/routing-index.yaml`, structured repository-reference, and organizer-recommendation schemas with controlled vocabularies, transition graphs, destination acceptance, numeric confidence, and evidence references.
- [x] 2.2 Add valid and invalid examples for unknown-owner intake, domain-origin expansion, multi-source routing, unresolved blockers, destination acceptance, and routed proposal provenance.
- [x] 2.3 Implement strict openxFactory validators for routing schema, central ID allocation, unique definitions, paired documents, legal transitions, accepted destinations, structured references, and prospective legacy compatibility.
- [x] 2.4 Register every schema and template in `contracts/manifest.yaml`, reconcile versions with `contracts/CHANGELOG.md`, update `contracts/README.md`, and add contract/validator tests. (Done 2026-08-06 at **contract-v1.30**, release commit 6c03d78: all four family schemas registered — routing record, routing-reference kernel, routing index, organizer recommendations — with per-file sha256; CHANGELOG v1.30 entry; contracts-README rows gain the registration; the family ships no templates, and the validator tests already exist at `tests/ideation_routing/` — 44 green at the cut.)
- [x] 2.5 Update openxFactory ideation, document-lifecycle, domain-to-neutral promotion, and doc-health guidance to reference promoted routing requirements without duplicating normative rules.

## 3. Domain Factory Adoption And Scaffolding

- [x] 3.1 Add reusable neutral ideation/routing guidance and update `scripts/apply-domain-starter.py` so future DomainxFactories inherit capture, provenance, acceptance, and disposition conventions.
- [x] 3.2 Update AdxFactory, LedgerxFactory, MedxFactory, OpsxFactory, and codexFactory ideation guides with known-domain capture, cross-domain routing pointers, destination acceptance, and owner-authorized disposition.
- [x] 3.3 Re-pin each adopting DomainxFactory to the promoted routing contract and verify unchanged legacy brainstorms receive no fabricated Idea IDs, Claim IDs, or routing history. — Done 2026-08-06: all five adopting domains re-pinned to the contract-v1.30 release commit `6c03d783` (LedgerxFactory 8b5c03a and MedxFactory 3c7715a with their consent conformance; AdxFactory 949e7d4; OpsxFactory 59db29d; codexFactory 04a87d0 via a scratch clone so the occupied shared checkout stayed untouched). No-fabrication verified: zero `XFI-` Idea/Claim IDs in any domain's legacy `ideation/brainstorm/` tree, zero `routing.yaml` records anywhere, and `validate-ideation-routing.py` 0 errors / 0 warnings over every domain repo and openxFactory itself.

## 4. Fourteenth Deterministic Family

- [x] 4.1 Add `scripts/doc_health/ideation_routing.py` in codexFactory and register it as the fourteenth deterministic family in the registry, runner, configuration, and report output.
- [x] 4.2 Implement schema/vocabulary, central Idea-ID and Claim-ID uniqueness, paired-document agreement, legal transition, blocker, destination acceptance, and 30/90-day aging checks.
- [x] 4.3 Implement the repository ID/gitlink resolver with POSIX/path-traversal checks, xFactory backlog-boundary inspection, strict-gate materialization, and explicitly skipped nightly external-path results.
- [x] 4.4 Implement lightweight source, destination, staged-fragment, and proposal provenance checks that distinguish canonical definitions from valid references and fenced examples.
- [x] 4.5 Add deterministic fixtures and tests for ordinary documents without routing sidecars, duplicate IDs, invalid transitions, unresolved blockers, copied records, stale references, safe normalization, contested decisions, and non-default thresholds.

## 5. Non-Mutating Ideation Organizer

- [x] 5.1 Add a separate codexFactory organizer module, versioned prompt, selector, neutral job envelope, and output validator for qualifying changes, manual requests, cross-domain links, aged items, and strict pre-gate review.
- [x] 5.2 Require every recommendation to carry committed source revision, passage hash and section reference, rationale, confidence from 0 through 1, alternatives, exclusions, ambiguity, dependencies, and `pending_review` disposition.
- [x] 5.3 Allow only current, non-policy-blocked catalog entries matching locator or authorized opaque resolver, content hash, inventory snapshot, and taxonomy digest to enqueue optional routing review; prove tags cannot create routing authority or lifecycle state.
- [x] 5.4 Apply source handling and workload-specific host authorization before dispatch, fail closed when unauthorized, filter protected paths/tags/owners/destinations/summaries/evidence, and persist permitted recommendations with `status: record`.
- [x] 5.5 Add tests for changed-input, manual, aging, and optional catalog-signal selection; stale-signal rejection; stable evidence; output rejection; authorized disposition; protected-metadata suppression; and organizer failure isolation.

## 6. Organizer Worker And Workload Readiness

- [x] 6.1 Add the bounded read-only `ideation-organizer` profile and capability in omnigent-install, reusing the existing document-analysis host with a distinct job envelope and artifact lane.
- [x] 6.2 Add only organizer-specific checks to the Cloud PC runbook and readiness preflight: runner eligibility, heartbeat freshness, profile/version, tenant/data boundary, handling authorization, and absence of repository credentials.
- [x] 6.3 Reference the neutral infrastructure-readiness contract for generic evidence, trust, expiry, remediation, and outage semantics rather than defining a competing readiness-result schema.
- [x] 6.4 Add profile, envelope, handling, artifact-boundary, offline, restart, stale-job, and recovery integration tests.

## 7. Aggregation Workflow And Reporting

- [x] 7.1 Extend the xFactory nightly workflow so deterministic routing completes before asynchronously dispatching an independent organizer child for qualifying or manual inputs. — Realized in the adopted nightly home (`.github/workflows/doc-health-reusable.yml`, `scripts/doc_health/organizer_dispatch.py`; the workflow steps cite tasks 7.1-7.4 inline): the prepare job completes the deterministic pass, builds the self-contained organizer bundle (`--organizer-prepare`), and only then dispatches the artifact-only `ideation-organizer-worker.yml` child gated on the fail-closed readiness evaluation; manual ideas enter via the `organizer-manual-ideas` input. Verified live green 2026-08-05/06 (runs 31001274147, 31068404946).
- [x] 7.2 Persist validated organizer evidence immutably, link it from the next report, and append only authorized disposition evidence to canonical routing records without editing closed reports. — Realized: validated recommendations persist `status: record` under `health/ideation-organizer/` (5.4's protected-output filter ahead of persistence); the report's `## Ideation Organizer` section links per-run evidence and the standing `linked evidence: N record(s)` count (rendering live in the 2026-08-06 report); closed reports are never edited — the organizer merge mode always engages so the section lands in the NEXT report.
- [x] 7.3 Add organizer selection, readiness, authorization, skip, queue, run, and recommendation counts to the report while keeping recommendations non-blocking and out of critical/error regression issues. — Realized: the live section carries exactly this vocabulary (selection/readiness/authorization/watchdog queue+run/recommendations/evidence, plus the skip reason — `heartbeat_api_unavailable` in the 2026-08-06 report); recommendations are non-blocking notes excluded from regression-issue classes (runner report folding + the 5.5 isolation tests; 107 organizer tests green at this tick).
- [x] 7.4 Add watchdog cancellation for children queued beyond ten minutes or running beyond thirty minutes and prove offline, unauthorized, stale-signal, invalid-output, or failed analysis cannot delay or suppress deterministic reporting. — Realized: the 600s-queue / 1800s-run deadlines with `gh run cancel` (the proven cataloger watchdog shape, reused at the organizer collect step with `continue-on-error`); isolation proven both by the 5.5 test matrix (offline/unauthorized/stale-signal/invalid-output/failure isolation; 107 tests green) and live — the 2026-08-05/06 nightlies stayed green with the organizer skipped (`worker_unavailable` / `heartbeat_api_unavailable`) and the deterministic report delivered on time.

## 8. Pilot, Realization, And Adoption

- [x] 8.1 Pilot one new unknown-owner idea and one domain-origin mixed idea across neutral, domain, installer/runtime, and aggregation claims without automatic movement. — Done 2026-08-06 (Brett's pilot commission, decision round): XFI-2026-001 (openxWallet, unknown-owner intake at `ideation/brainstorm/inbox/`, capture 47635d0 then organize gate a76755e) and XFI-2026-002 (Ledgerx subject-document-estate, domain-origin split at `ideation/brainstorm/cross-domain/`, sources referenced at full revision, never moved). Claims span neutral (routed), domain (routed, staying with xFactories/LedgerxFactory), and install/runtime (honestly unresolved with explicit blockers); nothing moved automatically. Strict routing validation 0/0.
- [x] 8.2 Record destination-owner acceptance, routed-claim provenance, organizer evidence, and an authorized accept/edit/reject disposition for each pilot. — Done 2026-08-06: three destination acceptances recorded (openxFactory ratify authority ×2, LedgerxFactory Domain Hermes ×1) with committed evidence refs; routed-claim provenance at full revisions throughout. Organizer evidence: a REAL ideation-organizer run through the claude-CLI seam on the authorized idea (job IDEAORG-27d6c614, run 7bf515a9092e; 6 recommendations validated 0-rejected; immutable record at xFactory `health/ideation-organizer/2026-08-06/`, commit 6e3babe) — XFI-2026-002's dispatch was DENIED by the fail-closed source-handling boundary, the recorded authorization evidence for that pilot. Authorized dispositions: candidate-01 ACCEPTED, candidate-05 REJECTED (both by the ratify authority under Brett's pilot commission), appended to the canonical record per the "Recommendation is reviewed" scenario.
- [x] 8.3 Run strict routing validation, codexFactory tests, skipped/offline and successful organizer runs, protected-output tests, and the full nightly workflow with no new critical/error regressions. — Done 2026-08-06: strict `validate-ideation-routing` 0/0 over openxFactory + all five domains; the adopted test suites green (202 across tests/ideation_routing + the routing family + organizer + organizer-dispatch incl. the protected-output matrix); organizer runs evidenced BOTH ways — skipped/offline in the live nightlies (worker_unavailable / heartbeat_api_unavailable, deterministic reporting never delayed) and successful via the real seam run (job IDEAORG-27d6c614, validated artifact, evidence xFactory 6e3babe); full nightly run 31129751955 GREEN end to end (its fail-on gate is the no-new-critical/error-regression check), with the deterministic ideation-routing family reporting No findings over the pilot records. (Investigation note: two earlier dispatches were cancelled because doc-health-nightly had been manually disabled at 15:17 EDT; Brett ruled re-enable, and the run above went straight through.)
- [x] 8.4 Promote routing contracts and guidance, re-pin consumers, archive this change with its verified supporting-document bundle, and confirm untouched sources retain no fabricated history. — Done 2026-08-06: contracts registered and tagged at contract-v1.30 (task 2.4); all five adopting domains re-pinned to the release commit (task 3.3); spec deltas promoted at archive; the supporting-document bundle packaged and verified; final sweep confirms zero fabricated Idea IDs in any domain's legacy brainstorm tree.

## Amendments

- 2026-08-03 — Pre-promotion amendment under `adopt-neutral-tooling-home`
  (ratified; design D5): the "Organizer execution, persistence, and
  readiness isolation" requirement's implementation-ownership clause now
  names openxFactory (selection, orchestration adapters, validation, and
  report integration moved home with the `scripts/doc_health/` package that
  hosts them; provenance codexFactory
  main@e4caa03bf48655b54bc96fc5450d9ad5bddf4886). xFactory aggregation
  keeps dispatch hosting and durable reporting. Edited in place in this
  change's `specs/ideation-routing/spec.md` because the requirement is
  active and unpromoted — no canon exists yet to carry a MODIFIED delta.
