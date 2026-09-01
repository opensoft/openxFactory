# Tasks: retire-doxbench-chat-turn-v1

**NOTHING BELOW SECTION 1 IS PERFORMED BY THIS PROPOSAL.** The packet is
`Status: draft` and this is the OpenSpec-before-implementation stage: no schema
byte moves, no fixture is deleted, no manifest digest changes and no CHANGELOG
row moves in the pull request that carries it. Sections 2-6 are the realization,
and § 8 is the archive gate the realization must clear before this change may
archive at all.

## 1. Proposal (this pull request)

- [x] 1.1 Author the packet — `proposal.md`, `design.md`, `tasks.md`,
      `.openspec.yaml`, and the `ideation-dashboard` delta (two `ADDED`
      requirements and one scenario-complete `## MODIFIED` block) — off
      `origin/main`, citing issue #522, Brett's 2026-09-01 ruling comment on it,
      and the measurement memo.
- [x] 1.2 ANSWER the fallback-redesign question rather than routing it.
      `design.md` § 1 and proposal § "The design question this change must
      answer, ANSWERED": unrecognized kind -> the SURVIVING family's failure
      envelope with an explicit unknown-kind code where a wire-valid
      `client_turn_id` exists, and the existing pre-identity shape where it does
      not. The rejected alternative is recorded with its costs.
- [x] 1.3 Re-verify the memo's pricing. Two corrections recorded: the packaged
      corpus is TWELVE fixtures (eight of them NEGATIVE, carrying seven refusal
      classes with no `-v2` equivalent), and there are TWO fallback layers, the
      second of which is correct and stays.
- [x] 1.4 Verify the MODIFIED block carries every canon unit — body paragraph
      and all four scenarios with every bullet — so nothing is dropped, no
      `Removed from canon` marker is owed, and the carriage-ledger arm has
      nothing to report. Confirmed by running
      `tests/doc-health/test_modified_block_currency_self_gate.py` on this
      branch: no new named subject.
- [x] 1.5 Validate: `OPENSPEC_TELEMETRY=0 openspec validate
      retire-doxbench-chat-turn-v1 --strict` and `--all --strict`, both green.
- [x] 1.6 List the change in README § OpenSpec Records.
- [ ] 1.7 Adversarial review to convergence, then ratification by the repository
      owner. Ratification authorizes realization and performs none of it.

## 2. Speckit F1 — the schema

- [ ] 2.1 Compute the SURVIVING family's reference closure from
      `request_v2`/`success_v2`/`failure_v2` — the same computation the existing
      baseline test performs for v1 — and use it, not inspection, to decide
      which `$defs` may go. Expected retained: `content_hash`, `confined_path`,
      `scope_key`, `buffer_state`, `transcript_turn`, `typed_proposal`. Any
      definition the computation says is v1-only is removed; any surprise is a
      finding, not a licence.
- [ ] 2.2 Remove `$defs/request`, `$defs/success`, `$defs/failure` and their
      three `oneOf` refs at `:58-60`.
- [ ] 2.3 Remove the top-level `deprecated_envelopes` block (`:70-82`) and its
      explanatory comment (`:64-69`). A block declaring the deprecation of kinds
      the file no longer defines names nothing.
- [ ] 2.4 Confirm the surviving envelopes' bytes are otherwise untouched — not
      one field added, removed or renamed.

## 3. Speckit F2 — the runtime, including the redesigned fallback

- [ ] 3.1 `serve.py`: replace the kind-discrimination `else` arm (`:3554-3557`)
      with the answered posture. The surviving request kind parses as today;
      anything else refuses. **Do not merely delete the arm** — a deleted arm
      leaves the default selecting a parser and a builder that are gone.
- [ ] 3.2 `serve.py`: register the unknown-kind code in `DOXBENCH_ERROR_CATALOG`
      with its status and fixed message, in the SAME commit as the code is first
      answered. An unregistered code raises rather than refuses (OQ-3 picks the
      token and the status).
- [ ] 3.3 `serve.py`: remove the three v1 kind constants (`:377-379`), the v1
      success builder `doxbench_turn_success_body` (`:1025-1059`), and the v1
      parser `_parse_workbench_chat_turn_body` (`:3450-3462`). Re-point the v1
      DEFAULTS on `doxbench_turn_failure_body` (`:954-957`) and `_refuse_turn`
      (`:3277-3279`) at the surviving failure kind.
- [ ] 3.4 **Leave the pre-identity fallback in `_refuse_turn` (`:3310-3317`)
      exactly as it is.** It is the correct answer for a request with no
      wire-valid identity, and the surviving failure envelope requires a
      `client_turn_id` no server may invent.
- [ ] 3.5 `scripts/ideation_dashboard/doxbench_contracts.py`: remove the three
      v1 kind constants (`:265-267`).
- [ ] 3.6 Confirm the shipped client needs no change —
      `web/views/doxbench-chat.js:37-39` is `-v2`-only — and that its failure
      handling routes the new code sensibly rather than rendering a raw token.

## 4. Speckit F3 — the validator and the packaged corpus

- [ ] 4.1 `scripts/validate-ideation-dashboard-contracts.py`: remove the three
      v1 rows from the kind→schema map (`:144-146`), the three tag-dispatch arms
      (`:392-397`), and the v1 kind from the paired-family tuple (`:1561-1562`).
- [ ] 4.2 Decide what survives of the `deprecated_envelopes` reader
      (`:309-345`). It is a GENERAL mechanism, not a v1 one — it reads whatever
      any loaded schema declares — so removing it because its only current
      subject is going would delete the estate's only machine-readable
      deprecation reader. Default: KEEP it; it simply reports nothing.
- [ ] 4.3 Delete the four positive v1 fixtures under
      `examples/ideation-dashboard/`.
- [ ] 4.4 **The eight NEGATIVE v1 fixtures: each of the seven refusal classes is
      re-expressed as a `-v2` negative or its loss is recorded with a reason.**
      escaping path; hash mismatch; identity subject; over budget; unknown model;
      untyped proposal; duplicate turn pair. None of the seven has a `-v2`
      equivalent today. Silence is not a permitted outcome for any of them.
- [ ] 4.5 Add a packaged `-v2` negative (or a test) for the NEW refusal: an
      unrecognized kind answered with the unknown-kind code.
- [ ] 4.6 Repair `examples/ideation-dashboard/README.md:307-313`, whose
      `--strict` note has been false since `contract-v2.0` shipped.
- [ ] 4.7 Re-run `python3 scripts/validate-ideation-dashboard-contracts.py`.
      Expected: `0 error(s), 0 warning(s)` where it reports four warnings today,
      and `--strict` no longer failing on the chat-turn fixtures.

## 5. Speckit F4 — the tests

- [ ] 5.1 Retire `tests/ideation-dashboard/fixtures/chat-turn-v1-envelopes.baseline.yaml`
      and the byte-identity assertion at
      `tests/ideation-dashboard/test_doxbench_contracts.py:1213-1239`, **naming
      in the commit and in the changelog entry what the test was for**: it
      exists to prove the deprecated bytes never moved, and it ends because the
      shape it protects leaves the published surface.
- [ ] 5.2 Move the v1 kind literals out of the remaining test files, across BOTH
      directory spellings: `tests/ideation-dashboard/` (`test_doxbench_contracts.py`,
      `test_doxbench_transport.py`, `test_doxbench_routes.py`,
      `test_doxbench_chat_view.py`, `test_doxbench_knowledge_service.py`,
      `test_doxbench_proposals.py`, `test_doxbench_view.py`) and
      `tests/ideation_dashboard/` (`test_validate_ideation_dashboard_contracts.py`).
- [ ] 5.3 New coverage for the redesigned fallback, in BOTH directions: an
      unrecognized kind WITH a wire-valid turn id -> the surviving failure
      envelope with the code, self-validated; WITHOUT one -> the pre-identity
      shape, unchanged. Plus a probe that a removed v1 kind takes exactly that
      path.

## 6. The `contract-v3.0` cut (a SEPARATE act, listed for completeness)

- [ ] 6.1 `contracts/manifest.yaml`: the schema's `sha256` moves off
      `2ff5f222…`; the row prose drops its v1 clauses;
      `contract_bundle_version`, and `contract_schema_version` per OQ-2's answer.
- [ ] 6.2 `contracts/README.md:86`: the long row.
- [ ] 6.3 `contracts/CHANGELOG.md`: the `contract-v3.0` BREAKING entry — the
      migration note, the three Breaking-clause preconditions each discharged
      and checkable, the baseline test's retirement named, and the coverage
      decisions from 4.4.
- [ ] 6.4 `docs/contract-versioning-policy.md`: the entry LEAVES § Deprecations
      Currently In Force and arrives in § Deprecations Executed carrying all six
      elements the one exemplar row establishes, closing
      `Deprecated at contract-v1.34, removed at contract-v3.0.`
- [ ] 6.5 `contracts/releases/contract-v3.0.digests.yaml`: the cut's inventory,
      rebuilt over the moved schema digest.
- [ ] 6.6 Follow § Bundle Realization Order exactly: allocate late, move every
      release surface atomically with the code, run every gate against the
      unchanged candidate, land the exact reviewed commit, publish the annotated
      tag, verify from an independently refreshed checkout.
- [ ] 6.7 Decide OQ-1 at the cut: whether this packet and
      `retire-hermes-flat-keys-and-openworkflow-tokens` ride the same major.

## 7. Post-cut verification

- [ ] 7.1 From a refreshed checkout at the tag: the validator reports zero
      chat-turn deprecation warnings, `--strict` passes over
      `examples/ideation-dashboard/`, and a v1 instance is refused.
- [ ] 7.2 Exercise the redesigned fallback against the running serve, both
      directions, and record the responses.

## 8. Archive gate

**This change has a CODE SURFACE and moves SCHEMA BYTES, so under
`release-realization` it archives ONLY on merged plus green realization
evidence — never on landing.** The evidence set:

- [ ] 8.1 §§ 2-5 merged on `openxFactory` `main`, `pytest-suite` green on the
      merge commit.
- [ ] 8.2 The `contract-v3.0` bundle declared with the moved digest and the
      rebuilt inventory, and its annotated tag PUBLISHED and verified from an
      independently refreshed checkout.
- [ ] 8.3 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
- [ ] 8.4 The 4.7 validator run recorded at `0 error(s), 0 warning(s)`.
- [ ] 8.5 The seven refusal-class dispositions of 4.4 recorded, each one either
      a named `-v2` fixture or a stated loss with a reason.
