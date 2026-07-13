# US4 Provider Adversarial Review — Findings & Dispositions

Status: record

Adversarial multi-lens review of the US4 provider surface (T066–T078,
commit range 66b1406..US4-checkpoint) run 2026-07-13 on Opus 4.8. Four
independent lenses (spec-conformance/fail-closed, release-verifier
correctness, resolver/git-object security, catalog/registration integrity)
produced 4 raw findings; each was adversarially verified with a
default-to-refuted bar. Result: 3 confirmed, 1 refuted. The two confirmed
P2s were FIXED in the checkpoint (they are fail-open bugs in NEW US4 code,
not ratified surfaces, and neither file is a PostgreSQL-evidence inventory
member — so fixing them does not invalidate the frozen matrix). The one
confirmed P3 is latent (behavior correct today) and is documented for
follow-up.

## Confirmed and FIXED in the checkpoint

### F-U1 — Cross-layer source scope compared only layer_id (fail-open)
Severity: P2. Verified CONFIRMED (module + reproduction).
File: `scripts/hermes_runtime_validation/semantics/jobs.py`
(`_validate_cross_layer`).

Defect: the cross-layer requirement check extracted only `job_scope[3]`
(layer_id) and tested `source.layer_id == job.layer_id`, ignoring
installation_id and stack_id. Because a layer_id is unique only within a
stack, a `source_resource` in a foreign installation or stack that reused
the job's layer_id string passed as "in-scope" — while the identical drift
on a run/event owning_scope WAS caught (those use the full scope tuple),
proving the cross-layer path was inconsistently loose. Violates HGR-001
(cross-layer records carry exact source/target scopes) and NJE-004-S03.

Fix: added `_resource_scope()` returning the exact
`(installation_id, stack_id, layer_id)` of a reference; the source must now
equal the job's full owning layer scope, and the target must share the job's
installation and stack while differing only in layer. Regression tests added
to `test_v2_jobs.py::test_cross_layer_reference_binds_exact_source_target_and_binding`
(foreign-installation source, foreign-stack source, foreign-installation
target — each now `HGR-JOB-CROSS-LAYER`; previously `[]`). Re-probe confirms
the foreign-installation source now fails closed.

### F-U2 — Handoff receipt missing a reproduced block raised KeyError (exit-code contract break)
Severity: P2. Verified CONFIRMED (module + live CLI reproduction).
File: `scripts/hermes_runtime_validation/consumer_handoff.py`
(`validate_handoff_receipt` → `_digest_findings`).

Defect: on the runtime path, `_digest_findings` read `closure_packet`, the
four artifact blocks (`compatibility_manifest`/`checker`/`runtime_binding`/
`evidence`), and `check_results` with raw subscripts, while
`_internal_findings` never asserted their presence. A receipt with a
canonical `consumer_repository` but omitting a required block raised an
uncaught `KeyError` that propagated out of the CLI (traceback, exit 1, no
finding, no `--json` payload), violating the documented 0/1/2 exit-code
contract (a contract defect must be a clean exit 1 with a finding). The
closed receipt schema that would reject it was applied only in the test
suite, never on the CLI path.

Fix: added `_structure_findings()` (called from `_internal_findings`, which
short-circuits before any object read) asserting each reproduced block is a
mapping with non-empty `path`/`digest` and each `check_results` entry carries
`evidence_path`/`evidence_digest`, emitting stable `HGR-HANDOFF-STRUCTURE`.
Regression tests added to `test_consumer_handoff.py`
(`test_receipt_missing_a_reproduced_block_is_a_clean_finding` [6 params],
`test_receipt_block_missing_digest_field_is_a_clean_finding`): the malformed
receipt now returns a clean finding with the resolver never invoked; live
re-probe confirms no exception.

## Confirmed and DEFERRED (documented, not fixed)

### F-U3 — Release membership: mandatory auxiliaries are exists()-gated
Severity: P3 (latent; behavior correct today). Verified CONFIRMED (static).
File: `scripts/hermes_runtime_validation/release.py` (`_collect_members`,
lines ~347–352).

Defect: catalog `release_member` entries are added to the closed membership
unconditionally (so an absent one hard-fails via `read_member` →
`ContentResolutionError` → exit 2), but the Decision-10/SIC-§5 mandatory
auxiliaries (`requirements/hermes-runtime-contracts.{in,lock}`,
`tests/hermes_runtime_contracts/postgres/images.lock.yaml`, the inventory
schema, `contracts/{manifest,CHANGELOG,README}`) are added only behind
`if source.exists(...)`. At a commit where one is absent, both the canonical
and candidate builds omit it and verification passes with a mandated pinned
member silently dropped. Related: nothing enforces the invariant
`semantic_member ⇒ release_member`.

Why deferred, not fixed: all seven auxiliary files are present at HEAD
(verified 2026-07-13), so the defect is latent. The correct fix restructures
membership (split unconditional Decision-10 members from conditional
"modified normative docs") and adds a catalog invariant with a test — and it
carries real risk of breaking the release lane's synthetic-repo tests
(which build inventories over minimal repos that may not carry every
auxiliary). That co-design is genuine follow-up work and should not be
rushed into this checkpoint. Tracked as the sole remaining P3 for the
release-realization work (T079+), which touches this surface anyway.

## Refuted

### F-U4 — validate_job_correlation skips a standalone job-scope assertion
Severity claimed P3. Verified REFUTED. `validate_job_correlation` on a job
with no runs/events and a missing owning_scope is degenerate, and the v2
envelope schema makes `owning_scope` required, so the structural registry
backstops it in the full pipeline. No fail-open of consequence; no change.

## Summary

- Confirmed: 3 (2 P2 fixed, 1 P3 deferred). Refuted: 1.
- Post-fix gates (all green): OpenSpec 24/0; strict validator zero findings
  (39 contracts, 32 schemas, 110 fixtures, 17 req, 85 scen, 803 nodes);
  non-PG pytest 485 passed; black/compileall/git-diff clean; PG-evidence
  inventory intersection EMPTY (frozen matrix not re-run).
- Remaining backlog into T079+: F-U3 (P3, latent).
