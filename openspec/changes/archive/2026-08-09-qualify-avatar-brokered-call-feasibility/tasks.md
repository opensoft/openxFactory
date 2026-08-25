> Realized 2026-07-12 — live lab run against the pinned `gpt-realtime-2.1`
> candidate: **Overall PASS, 70/70 trials** (F0-A 20, F0-B/C/D/E/F 10 each);
> evidence at `evidence/f0-results.json` / `evidence/f0-results.md` /
> `evidence/f0-interface-impact.yaml`, pinned by the realized kernel's
> `contracts/avatar-client/interface-lock.yaml` (`f0_status: PASS`,
> `f0_source_commit: 5142065b`). The change is **kept active deliberately** —
> archiving would break the fail-closed F0 evidence pin or force a
> `contract-v1.7` re-tag (see root README). Checkboxes reconciled to the
> landed evidence 2026-07-17; they were never ticked at realization.

## 1. Harness And Safety Boundary

- [x] 1.1 Create `experiments/avatar-brokered-call/` with a pinned runtime/dependency lock, deterministic run configuration, generated-audio fixture, monotonic clock, bounded cleanup, and environment-only lab credential loading.
- [x] 1.2 Implement configuration validation that rejects tenant data, enabled tools, unpinned candidate settings, credentials in arguments, readiness above 5,000 milliseconds, or any non-lab profile.
- [x] 1.3 Implement an allowlisted result writer and offline tests proving that credentials, SDP, headers, provider payloads, audio, transcripts, arbitrary identifiers, and unbounded strings cannot enter committed evidence.

## 2. Trial Matrix

- [x] 2.1 Implement baseline and delayed-sideband trials with answer holding, sideband verification, xFactory control readiness, authoritative media authorization, answer application, and first-media timing markers.
- [x] 2.2 Implement sideband-failure, readiness-timeout, interrupted-run, and cleanup trials that never authorize media and terminate every known provider call. (The sideband-failure and readiness-timeout paths live in `trials/f0c_sideband_failure.py`; `F0-C-READINESS_TIMEOUT` wired into F0-C and the cross-cutting `F0-D-INTERRUPTED` / `F0-D-BOUNDED_CLEANUP` assertions registered in the record + schema PASS conditional, with `cleanup.run_cleanup` invoked from the run-assembly path. Live per-trial execution completed in the 3.1 supervised lab run — F0-C 10/10, F0-D 10/10.)
- [x] 2.3 Implement exact-retry and changed-retry trials proving at-most-one provider call for an equivalent request and no prior-answer disclosure or second call for changed offer identity.
- [x] 2.4 Implement consent-revocation and kill-path trials proving immediate control revocation and provider termination within five seconds, with request and observed-termination timing kept distinct.

## 3. Evidence And Handoff

- [x] 3.1 Execute every mandatory trial against the pinned `gpt-realtime-2.1` candidate using a lab project key and generated audio; write schema-valid `evidence/f0-results.json` and `evidence/f0-results.md` with terminal status `PASS`, `FAIL`, or `INCONCLUSIVE`. (Landed: Overall `PASS`, 70/70.)
- [x] 3.2 Write `evidence/f0-interface-impact.yaml` even when empty, mapping every variance to affected `ACR-*` IDs, severity, evidence, proposed correction, and closed-default continuation status.
- [x] 3.3 Run strict target/all OpenSpec validation, offline harness tests, result-schema validation, redaction scans, supporting-document hash verification, and `git diff --check`. Confirm that no canonical contract, reference-runtime, UI, DomainxFactory, or deployment file changed. (Closed at the kernel's `realized` completion stamp, 2026-07-12: threat model accepted, `contract-v1.7` tag published, per-file digests in `contracts/manifest.yaml`.)

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting exactly those two lines recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (b), the archive act itself, because no explicit ratification act appears anywhere on the record: the archive commit `e34dce6` applied this change's spec delta into the canonical specs, and a change whose spec deltas have PROMOTED is ratified by construction — the reasoning `bdd09c2` recorded and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites as its own. The three-way floor is cleared on the APPROVER axis, the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

**What Brett's named decision here is and is not.** The archive commit records "Option C of issue #30, accepted by Brett 2026-08-09, superseding the 2026-08-04 hold". That acceptance LIFTED AN ARCHIVE HOLD; it is not a ratification, the word appears nowhere on this record, and the citation says so. It is named as the word the archive act was taken on, and the citation rests on the promotion.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
