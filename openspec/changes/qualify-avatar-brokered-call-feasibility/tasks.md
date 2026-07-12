## 1. Harness And Safety Boundary

- [ ] 1.1 Create `experiments/avatar-brokered-call/` with a pinned runtime/dependency lock, deterministic run configuration, generated-audio fixture, monotonic clock, bounded cleanup, and environment-only lab credential loading.
- [ ] 1.2 Implement configuration validation that rejects tenant data, enabled tools, unpinned candidate settings, credentials in arguments, readiness above 5,000 milliseconds, or any non-lab profile.
- [ ] 1.3 Implement an allowlisted result writer and offline tests proving that credentials, SDP, headers, provider payloads, audio, transcripts, arbitrary identifiers, and unbounded strings cannot enter committed evidence.

## 2. Trial Matrix

- [ ] 2.1 Implement baseline and delayed-sideband trials with answer holding, sideband verification, xFactory control readiness, authoritative media authorization, answer application, and first-media timing markers.
- [ ] 2.2 Implement sideband-failure, readiness-timeout, interrupted-run, and cleanup trials that never authorize media and terminate every known provider call. (Offline state: the sideband-failure and readiness-timeout paths are implemented in `trials/f0c_sideband_failure.py`; the readiness-timeout assertion `F0-C-READINESS_TIMEOUT` is wired into F0-C and the cross-cutting `F0-D-INTERRUPTED` / `F0-D-BOUNDED_CLEANUP` assertions are registered in the record + schema PASS conditional, with `cleanup.run_cleanup` invoked from the run-assembly path. Live per-trial execution of these paths is deferred to the supervised lab run — see 3.1.)
- [ ] 2.3 Implement exact-retry and changed-retry trials proving at-most-one provider call for an equivalent request and no prior-answer disclosure or second call for changed offer identity.
- [ ] 2.4 Implement consent-revocation and kill-path trials proving immediate control revocation and provider termination within five seconds, with request and observed-termination timing kept distinct.

## 3. Evidence And Handoff

- [ ] 3.1 Execute every mandatory trial against the pinned `gpt-realtime-2.1` candidate using a lab project key and generated audio; write schema-valid `evidence/f0-results.json` and `evidence/f0-results.md` with terminal status `PASS`, `FAIL`, or `INCONCLUSIVE`.
- [ ] 3.2 Write `evidence/f0-interface-impact.yaml` even when empty, mapping every variance to affected `ACR-*` IDs, severity, evidence, proposed correction, and closed-default continuation status.
- [ ] 3.3 Run strict target/all OpenSpec validation, offline harness tests, result-schema validation, redaction scans, supporting-document hash verification, and `git diff --check`. Confirm that no canonical contract, reference-runtime, UI, DomainxFactory, or deployment file changed.
