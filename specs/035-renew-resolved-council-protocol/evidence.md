# Implementation evidence: Neutral resolved council protocol (feature 035)

Status: record
Kind: report
Lane: codexfactory-2 (codeXfactory-2)

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md) · **Tasks**: [tasks.md](tasks.md) · **Quickstart**: [quickstart.md](quickstart.md)

This is the feature's implementation record. Each phase has one section. Every entry is dated in UTC, and every count was measured by a command named beside it, in the declared py-bench container (Python 3.12.3) and in the phase's own worktree. Brett Heap's words are cited from opensoft/brett-wip `lanes/log/codeXfactory-2.md`, read at brett-wip `6f443b52` (2026-10-09T01:28:55Z). Word times come from the session transcript.

## Authority and preconditions (T001)

- **The lane's claim.** `CLAIMED — lane codeXfactory-2 … 2026-10-07T10:39:11Z, opensoft/openxFactory:openspec/changes/renew-resolved-council-protocol` (log line 169), after a sibling search that found no claim or PR.
- **The builder.** Brett Heap, 2026-10-08T17:43:04Z, *"This lane, 035 then 025 (Recommended)"* (RULED, log line 182).
- **The five OPEN rulings.** RULED at 2026-10-08T19:24:21Z: OPEN-1 *"600 s challenge, 6 h assignment (Recommended)"*, OPEN-2 *"Consumer's runtime config (Recommended)"*, OPEN-3 *"History + unchanged rule file (Recommended)"* and OPEN-4 *"Join behind a version floor (Recommended)"* (log lines 196–199). RULED at 2026-10-08T19:24:59Z: OPEN-5 *"Keep the existing names (Recommended)"* (log line 200).
- **The three OPEN-3 follow-ups and N10.** RULED at 2026-10-08T23:03:35Z: follow-up 1 *"Every governed source (Recommended)"*, follow-up 2 *"job_workflow_ref's repo (Recommended)"*, follow-up 3 *"At or after the frozen rev (Recommended)"*, and N10 *"Dated correction + tick 2.2 (Recommended)"* (log lines 209–212).
- **The governing packet.** #1267 landed in `main` as `80f47483fc94794d1417b8dc65c0b6a4c7db160e` at 2026-10-08T19:25:37Z (LANDED, log line 202).
- **This feature's plan.** #1268 landed in `main` as `de70915154f6126e3ab809b9305a6d988e4026ac` at 2026-10-09T01:24:27Z, on Brett Heap's word *"merge 1268 when green"* (LANDED, log line 236). That merge is the landing of #1268's tick of packet task 2.2 (T002, under N10).
- **Phase 1's start and landing words.** *"start 035 phase 1 while 1268 lands"*, 2026-10-09T00:34:33Z (WORD, log line 225), and *"merge PR-1 when green"*, 2026-10-09T00:42:13Z (WORD, log line 227).

## Phase 1 — Setup and foundational (PR-1)

### Base and start (2026-10-09)

- **Branch.** `035-phase1-foundation` was cut from the plan branch at `55bcddc8b` (2026-10-09T00:40:56Z; `origin/main` was then `564f565ad`). It took the plan branch's round-7 fixes by fast-forward to `9053e64eb`, then, once #1268 landed, fast-forwarded to `origin/main` at `de7091515`. No rebase, no force-push.
- **Phase 1's base is `de7091515`.** Measured there, before any Phase 1 file was written:
  - the pinned OpenSpec CLI, `python3 scripts/validate-openspec-cli-pin.py --all --strict`: exit 0, `Totals: 112 passed, 1 failed (113 items)`, with 0 undispositioned failures (the one failure is `add-chain-attestation`'s accepted exception, Brett Heap 2026-09-05, *"take exit 2"*);
  - doc-health in single-repo mode, `python3 scripts/doc-health.py --single-repo . --report-out <scratch>/doc-health-base-de709151.md`: exit 0, `Findings: 31 critical, 26 error, 59 warning, 20 info`.
- **The suites T014 names, at the plan tip `55bcddc8b`.** `python3 -m pytest tests/signed_execution_chain tests/clearing tests/code_surface tests/intent-compliance tests/manifest_digests -q`: 828 passed. This was measured at the plan tip, not at `de7091515`, and is a reference only; the same command is run at Phase 1's head below.

### Tests first, run red (2026-10-09T01:41Z)

T005–T011 were written, and the T009 foundation vectors authored, before any implementation module existed. The vectors were authored by hand, with every expected outcome written out, and spelled in the corpus's deterministic JSON form: 128 vectors, 102 at boundary `definition` and 26 at boundary `classification`, all `applies_to: [producer, consumer]` and `derived_origin: hand`.

`python3 -m pytest tests/council_convening -q -m "not postgres" --continue-on-collection-errors`: **32 failed, 17 passed, 11 errors**. Every failure is an absent name or file:

- 3 collection errors: `test_shared_definitions.py`, `test_protocol_registry.py` and `test_corpus_index.py` import `records`, `classification` and `corpus`, which did not exist;
- 8 errors in `test_gate_wiring.py`: `.github/workflows/council-convening-gate.yml` is absent;
- 29 failures in `test_validator_cli.py`: `scripts/validate-council-convening.py` is absent;
- 3 failures in `test_digest_subjects.py`: `council_convening` and `council_seat_return_payload` are not yet subjects.

The 17 passes are not implementation. 11 are pins on behaviour `canonical.serialize` already had: the float, integer-bound and lone-surrogate refusals, and the RFC 8785 known answer. 1 reads `pytest-suite.yml`. 5 pass by coincidence, because a missing script also exits 2 and prints nothing: the unreadable-path case, the three not-yet-landed modes, and the line-format check over empty output. Each of the 5 is re-run green against the real validator below.

**The RFC 8785 known answer was checked against the RFC itself.** `https://www.rfc-editor.org/rfc/rfc8785.txt`, fetched 2026-10-09 (SHA-256 `63d52294eb0e3f0014174288186d388b4ddbf2c67d1ce8af1d9726eb0c3ab240`): § 3.2.3's canonical output, lines 312–313 joined as the RFC says they wrap "for display purposes only", with the `numbers` member removed, equals `canonical.serialize` of § 3.2.2's input without `numbers`, byte for byte.
