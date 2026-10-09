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

### The key-fingerprint spelling, corrected on Brett Heap's ruling (2026-10-09T02:40Z)

- **The ruling.** Brett Heap, 2026-10-09T02:36:50Z, *"Estate spelling (Recommended)"*: `key_fingerprint` is `sha256:` + `sha256(raw 32-byte public key)`, as openXwallet `fingerprint_of_public_key` and codexFactory `key_fingerprint` compute it, and as T047 names it (RULED, log line 248, read at brett-wip `6e174ca8`, 2026-10-09T02:58:49Z).
- **What Phase 1 had.** The labelled fixture keys' `fingerprint` returned `sha256:` + the raw key's own hex, following data-model § Shared definitions' wording at line 36 (the `key_fingerprint` row).
- **What the estate computes.** Both estate functions hash the key:
  - openXwallet `scripts/validate-openxwallet.py:536-541`, at openXwallet `f3eb929b` (the commit openxFactory pins), returns `"sha256:" + hashlib.sha256(raw).hexdigest()`;
  - codexFactory `.github/workflows/scripts/council_seat_signing.py:199-205`, at codexFactory `48d0560e`, returns `sha256_digest(public_key_raw)`, the same expression (`:168-170`).
- **Every site.** `grep -rn -i fingerprint` over Phase 1's files found:
  - one computation, `FixtureKey.fingerprint` in `scripts/council_convening/generate.py`;
  - one assertion, `test_labelled_test_keys_are_deterministic_and_distinct`;
  - one stored description, `key_fingerprint` in `shared-definitions.schema.yaml`;
  - the same sentence in data-model.md:36, research.md:32 and plan.md:63.

  No vector derives a fingerprint from a key. The fingerprint-valued members use the arbitrary grammar value `sha256:` + `ab`×32, and the pattern `^sha256:[0-9a-f]{64}$` accepts both spellings.
- **Test first.** The assertion was corrected to `"sha256:" + hashlib.sha256(first.public_key).hexdigest()` and run red: 1 failed (`'sha256:026a9…' == 'sha256:5df2e…'`). Only then was the generator changed.
- **Regenerated.** `python3 -m scripts.council_convening.generate`, then `--check`: no corpus byte moved (`7255303a7`).
- **The documents.**
  - data-model § Shared definitions, line 36 (the `key_fingerprint` row), carries a dated correction citing the ruling, T047 and both estate functions.
  - research.md:32 and plan.md:63 stated the same wrong spelling and carry the same dated correction, so the three documents agree.
- **The known answer is pinned as literals, not recomputed** (`test_the_fixture_key_known_answer`, `a1375ac96`):
  - label `seat-alpha`;
  - public key `026a95888285641a4a68f38af4f24177db400f154f00c5d86d24fd0017a6ef03`;
  - estate fingerprint `sha256:5df2e785df8a21267679b0f4159bfff6040c4ef4bf0d0ae43820f649cae6083b`.

  This agrees with the value the PR-1 reviewer derived independently.

### The family keywords were dropped inside whole schema documents: found, reproduced, fixed (2026-10-09T02:45Z–02:53Z)

- **Found elsewhere.** The Phase 3 writer found the defect. The Phase 4 writer reproduced it from a second entry point, a record schema validated at its root. The coordinator relayed both.
- **Reproduced here first, before any change.**
  - `validator_for(protocol-registry.schema.yaml as written)` is `Draft202012Validator`.
  - A legacy entry with `introduced_in: "contract-v4.0\n"` gave **0 errors**.
  - A malformed tag drew jsonschema's stock message (`does not match '^contract-v…'`), not the family's `does not match the pattern, matched whole`.
- **The cause.** `SchemaSet.validator(ref)` builds `FamilyValidator({"$ref": ref})`. On every descent into a whole family document, jsonschema's `evolve` calls `validator_for(schema, default=cls)`. The house `$schema` header maps that to plain `Draft202012Validator`, so whole-string `pattern` and `x-max-utf8-bytes` stop applying to that document and everything beneath it: validation fails open. A `$ref` straight to a `$defs` member never enters a document, which is why the definition-boundary tests could not see it.
- **The fix (a), `2ac73e066`.**
  - The registry serves each document with `$schema` removed, so `validator_for` keeps `FamilyValidator` at every depth.
  - The metaschema check still runs on the document as written, and `SchemaSet.family` keeps that original.
  - A family document whose `$schema` names any other dialect is refused at load.
- **Option (b) was tested and rejected.** `validator_for` consults only jsonschema's module-global `_META_SCHEMAS`, so re-pointing the 2020-12 id at `FamilyValidator` changes every 2020-12 schema in the process. Demonstrated: once it is set, an unrelated `{"pattern": "^a$"}` schema refuses `"a\n"`, and the metaschema check itself resolves to `FamilyValidator`.
- **Hardening, `1d2adcf78`.**
  - `load_schemas` refuses any `$ref` or `$dynamicRef` whose target is not a loaded document (`references_outside`). jsonschema also resolves against the bundled dialect metaschemas, which keep their `$schema`.
  - Such a reference cannot strip a family keyword, since none sits beneath a metaschema, but it is outside the family.
  - **For successors:** a schema that `$ref`s another document must have that document loaded, or loading fails with `… outside the loaded documents`.
- **Tests.**
  - Six were written first and run red (6 failed, 12 passed). Nine more followed the addendum (the closure ones run red: 3 failed).
  - They cover both entry points, a document's root and a `$ref` into a fragment of a header-carrying document, for both keywords.
  - They also cover a trailing newline reached through the whole registry document (the reviewer's `contract-v5.0\n` probe is now a `pattern` finding), and `x-max-utf8-bytes` reached through a whole-document `$ref` in a copied tree.
  - A foreign `$schema` is refused at load.
- **No vector changed:** 128/128 adjudicated as authored.

### The independent PR-1 review's fixes (2026-10-09T07:23Z–07:45Z, `a1375ac96`)

An independent Opus review of `396ef5dd7` returned READY AFTER FIXES. Its own runs matched this record: 244 passed, self-test exit 0 at 128/128, `generate --check` exit 0, the manifest row correct, the scope check empty, 0 secret hits, and vectors that are not circular. Each item below was written test-first.

The new tests ran red with 43 failed and 56 passed among those selected. That includes 7 landed-corpus tests that were red only because `index.json` had not yet been regenerated over the vector changes.

- **B1 (blocking): recognition rule (b) read paths no legacy artifact has.** This is an evidence-based reading where the plan is silent: data-model E1 names "a signing context in the legacy set" and no member path.
  - **Where the real legacy seat result carries the context string: `signature.protocol`.** codexFactory `council_seat_signing.py` (`48d0560e`, `:549-555`) returns the closed three-key block `{protocol, key_fingerprint, signature}`, and Hermes `review_authority.py` (`f9d0874ba`, `:127-128`, `:597-630`) reads it under the seat result's `signature` member (`SIGNATURE_BLOCK_KEY`, `SIGNATURE_BLOCK_KEYS`).
  - **The first reading was dropped, not kept.** `signing_context` and `context.signing_context` match no legacy artifact: `git grep signing_context` finds, in Hermes `origin/main`, only the error-code name `council.signing_context_incomplete`, and in codexFactory only a test name.
  - **The change.** `member_paths` is now `[[signature, protocol]]` in `protocol.registry.yaml`, in `LANDED_PROTOCOLS` and in the frozen test copy.
  - **The vectors.**
    - Removed: the 2 fictional-path vectors.
    - Re-shaped onto the real path: 2 (`cls-offline-replacement-context-without-protocol-refuse`, `cls-offline-replacement-with-legacy-shapes-accept`).
    - Added: 5. Three carry the Hermes shape: route offline; route under the legacy selection with the `in_use` override; and `legacy_protocol_refused` under the replacement selection. `cls-offline-signing-context-member-refuse` pins that a top-level `signing_context` member is `protocol_unknown`. `cls-offline-replacement-string-signature-accept` shows that a replacement return's string `signature` is decided by rule 1, unaffected.
  - **Red.**
    - Under the registry as committed at `1d2adcf78`, the three Hermes-shape vectors gave `refuse protocol_unknown`.
    - `check` on the Hermes seat result exited 1, `ERROR [council-convening-protocol-unknown]`, where it should exit 3.
    - The unit tests: 9 failed, 45 passed.
- **B2 (blocking): `check` exited 0 on non-record family kinds.** Each non-record kind is now judged:
  - an index runs `index_problems`;
  - a vector is adjudicated against its own expectation, through the same `adjudication_findings` the self-test uses, which removes the false note "the self-test adjudicates it";
  - a family schema needs the full house header (`schema_version` 1, a `name`, the 2020-12 `$schema`, an `$id` that is a `.schema.yaml` under the family base), carries no protocol shape, and uses only asserted formats;
  - anything else is classified, as before.

  The reviewer's three probes now exit 1.
- **M1: one malformed vector crashed the self-test.**
  - **Red.** On the committed code, an indexed vector missing `requirement_ids` raised `KeyError: 'requirement_ids'` out of `build_index`, after 7 note lines and **0 ERROR lines** (reproduced from a `git archive` of `1d2adcf78`).
  - **Now.** `render` runs the vector format and the corpus-token rule, and raises `ValueError` naming the file. The self-test prints its collected findings before the generator runs.
- **M2: a repeated YAML key was resolved, not refused.**
  - **Red.** `yaml.safe_load` turned `protocol: <legacy>` then `protocol: <replacement>` into `{'protocol': 'xfc-resolved-council-1'}`.
  - **Now.** Family schemas, the registry and `check`'s YAML records go through the Hermes runtime family's fail-closed `load_yaml_bytes` (`scripts/hermes_runtime_validation/loader.py`), reused rather than copied. It also refuses aliases, anchors, merge keys, non-string keys and implicit timestamps.
  - **Unchanged.** All four family YAML documents load identically under it.
- **Formats.**
  - The checker is built from `ASSERTED_FORMATS = ("date-time",)`, not from whatever optional libraries are installed.
  - A family schema using any other `format` is refused at load (`email`, `uri`, `hostname` and an unknown name were each probed).
  - Loading still fails closed without `rfc3339-validator`.
- **L1.** The RFC 8785 known answer lives in `tests/council_convening/test_digest_subjects.py`, not in the corpus. Phase 1's boundaries, `definition` and `classification`, take no digest, so it is deferred to Phase 2's digest-bearing vectors, where a vector can carry it as a `derived` known answer.
- **L2: chosen, a dated sentence in [contracts/conformance-corpus.md](contracts/conformance-corpus.md).** A classification refusal carries `derived: {}`. Its refusal code already fixes the class wherever one exists: `legacy_protocol_refused` goes only to a legacy record, `protocol_not_selected` only to a replacement record, and `protocol_unknown` has no class. Emitting the class would add no agreement for any vector to check, and would rewrite every refusal vector.
- **L3.** The gate's backreference greps are `([1-9][0-9]*)/\1`, so a `0/0` run that walked nothing fails. The tests pin `|| fail` after every grep, plus `set -euo pipefail`, `fail()`, and `shell: bash` on both steps, which gives the `tee` pipeline `pipefail`.
- **L4.** A `kind` that is not a string is `council-convening-schema` in `check`, with no traceback, and no longer crashes the classification boundary.
- **L5: refused in the vector format, rather than pinned by a vector.**
  - **The split.** jsonschema's `integer` accepts `2.0`, while `xfc-jcs-sha256-1` refuses it as a non-integer number, and a reader whose numbers are all doubles cannot tell it from `2`.
  - **Why not pin a vector.** Pinning one would encode one reader's type system.
  - **What now happens.** Every corpus file is parsed with `corpus_tokens`, so an integral number spelled as a float (`2.0`, `2e0`, `20E-1`, `-0.0`) is `IntegralFloatToken`, a `council-convening-schema` finding. `1.5` is unaffected.
- **L6.** The `$parts` test asserts adjudication. It also shows the join ran: at least one `$parts` vector accepts, and its unjoined value would be refused.
- **L7: a known limit, documented and guarded.**
  - **The limit.** `whole_match` rewrites only a pattern's final `$`.
  - **The guard.** The new invariant test found two family patterns with an inner `$`, `relative_path` and `decimal_string`. Both sit inside negative lookaheads, in patterns whose characters exclude U+000A, so Python's extra match position can only add a refusal of a string the final `\Z` already refuses. They are pinned with behavioural checks, and any new inner `$` fails the test for review.
- **L8.** `def-matched-class-refuse-trailing-newline`.
- **L9.**
  - `check`, `corpus`, the generator and the self-test classify nothing against a registry whose schema or closure findings are not empty (`load_closed_registry`). `check` and `corpus` print the findings and exit 1, and the generator raises.
  - Before the fix, the self-test printed the registry findings and still adjudicated the corpus against that registry.
- **Reading 3.** A dated sentence in data-model § Shared definitions says that at boundary `definition` the grammar is checked first and admissibility second.
- **Three test-setup corrections, none a weakening.**
  - The format tests' `_rewrite_vector` now indexes by hand a vector the generator rightly refuses.
  - The registry-entry test deep-copies the entry: a shared list made `yaml.safe_dump` write an alias, which the strict loader rightly refuses.
  - The M1 test breaks an indexed vector.
- **The corpus.** It now holds 132 vectors: 103 `definition`, 29 `classification`; outcomes accept 42, refuse 82, route 8. `index.json` is `sha256:45c54abac797791d20cf796933a1ef016424cad52b8881b42b91d759d9072581`.
- **Pushed early** at `a1375ac96`, before the full suite, on the coordinator's word, so the other phases could merge the fixes.

### Green at Phase 1's head (2026-10-09)

- **Merged with `main`, and measured at the code head.** `origin/main` at `93d13d6c8` (#1274) was merged as `84501bedf`, with no conflict, no rebase and no force-push. The code head is `a1375ac96`. The commit carrying this record changes only this file and tasks.md.
- **The package.** `python3 -m pytest tests/council_convening -q -m "not postgres"`: **308 passed**. These include the five tests that passed by coincidence in the red run, now against the real validator:
  - `test_check_on_an_unreadable_path_exits_2`;
  - the three `test_modes_that_have_not_landed_are_exit_2` cases;
  - `test_every_output_line_is_a_finding_or_a_note`.
- **The self-test.** `python3 scripts/validate-council-convening.py`: exit 0, printing:

  ```text
  note  schemas loaded: 2 (family) + digest-construction
  note  protocol registry closed: 2 entries
  note  corpus index: 132 vectors, 132 both-sides, sha256:45c54abac797791d20cf796933a1ef016424cad52b8881b42b91d759d9072581
  note  vectors adjudicated: 132/132
  note  refusal codes probed: 5/5
  note  finding codes probed: 1/1
  note  requirements probed: 2/2 (FR-001, FR-011)
  note  generator reproduced corpus byte-for-byte
  note  self-test: 0 error(s), 0 warning(s)
  ```

- **The corpus.**
  - `python3 -m scripts.council_convening.generate --check`: exit 0, no drift.
  - `python3 scripts/validate-council-convening.py corpus`: `132 vectors, agreement set 132 (applies to both sides)`; by area `foundation=132`; by outcome `accept=42, refuse=82, route=8`.
- **The suites T014 names.**
  - `python3 -m pytest tests/signed_execution_chain tests/clearing tests/code_surface tests/intent-compliance tests/manifest_digests -q`: **828 passed**.
  - `python3 scripts/validate-signed-execution-chain.py`: `0 error(s), 0 warning(s)`.
  - `python3 scripts/validate-clearing-dispatch.py`: `0 error(s), 0 warning(s)`.
- **The pinned OpenSpec CLI.** `python3 scripts/validate-openspec-cli-pin.py --all --strict`: exit 0, `Totals: 113 passed, 1 failed (114 items)`, with 0 undispositioned failures.
  - The one failure is the same accepted `add-chain-attestation` exception as at base.
  - The added item is `main`'s new `amend-factory-mcp-conformance-auth-profile` (#1274).
- **doc-health, head against base.** `python3 scripts/doc-health.py --single-repo . --previous-report <scratch>/doc-health-base-de709151.md --new-findings-out <scratch>/doc-health-new.md`: exit 0, `Findings: 31 critical, 26 error, 59 warning, 21 info. New regressions vs previous report: 0`, and the new-findings file is `[]`. Two lines differ from base, both info:
  - the draft-age trend line, `min=3` → `min=0`;
  - one finding in `openspec/changes/amend-factory-mcp-conformance-auth-profile/`, which the `main` merge brought in. It is not a Phase 1 path.
- **The full suite.** `python3 -m pytest tests/ -q -rfE -m "not postgres" --junitxml=…`, in the background.
  - Submodules: the ones `pytest-suite.yml` initializes (`:430-431`) are initialized here too: `openXwallet`, and `openXdox` and `openDox` recursively. `installs/omnigent-install` is uninitialized, as in CI.
  - Result, counted by `pytest-suite.yml`'s own JUnit rule (`:895-940`): **selected 10126, passed 10111, skipped 6, failures 9, errors 0** (pytest: `9 failed, 9510 passed, 6 skipped, 338 deselected, 601 subtests passed in 2803.16s`, started 2026-10-09T07:45:41Z at `a1375ac96`). The floors are `MIN_SELECTED` 7050, `MIN_PASSED` 7044 and `EXPECT_SKIPPED` 6.

  Locally, the six skips include the two named verifiers (`TheFreshnessVerifier`, `TheVectorReplay`): they skip because no pinned decision core is on disk, and CI checks one out. The others are the two `notebooklm` collections and two `conformance-gate` tests.

  **All nine failures are this container, not this branch.** All nine also fail when re-run alone, and none reads a file the branch changes:
  - **`tests/factory-mcp/test_factory_mcp_conformance.py`.** Four failures: `test_nul_bytes_are_refused_not_raised`, and three `test_local_fragments_may_carry_uri_characters` subtests, which expect `invalid_pointer` and get `invalid_json_schema`.
    - **The cause.** The container carries `rfc3987_syntax`, `rfc3986_validator` and `fqdn`, which the CI lock (`requirements/hermes-runtime-contracts.lock`) does not. jsonschema's default `FormatChecker` therefore asserts `uri-reference` here, and the metaschema check refuses before the pointer check runs.
    - **The proof.** With those three libraries hidden from the interpreter (a `sitecustomize` meta-path block), the same file passes in full at this head: `88 passed, 203 subtests passed`.
    - This is exactly the environment split the format allowlist above closes for this family.
  - **`tests/hermes_runtime_contracts/test_validator_cli.py::test_release_mode_field_is_preserved_on_the_real_repository[--require-realization-realization]`.** It failed with `subprocess.TimeoutExpired` at the test's fixed `timeout=30`.
    - **The answer is right.** Run directly, the command exits 2 with `mode: realization`, which is everything the test asserts, in 37.1 s at a load average of 13.8–17.2. The `--require-candidate` case takes 26.2 s.
    - **The time is git.** The profile puts it in `verify_inventory_against_commit`: 5,840 `git` subprocesses reading 1,132 members of the tagged release. This family is not a release member until Phase 7, and the branch adds no manifest row.
  - **`tests/ideation-dashboard/`.** Four tests in `test_gate_routes.py`, `test_human_seen.py`, `test_lens.py` and `test_lens_gate_cli.py`, all on `the pinned openxdox_spec leg is not materialized: openXdox/spec is empty`.
    - **The cause.** `human_seen.find_cross_reference_validator` walks up from this worktree, `openxFactory-worktrees/035-phase1-foundation`, to `/workspace/projects/xFactory/openxFactory/scripts/validate-ideation-cross-reference.py`. That is the shared aggregation checkout, whose submodules are uninitialized.
    - **Why it is not this branch.** The code that failed is that checkout's validator, run against that checkout, with no file of this branch involved. In CI, the repository is itself checked out at `openxFactory`, and the walk finds it.
    - In this worktree's own `openXdox/spec`, `contracts/schemas/ideation-dashboard-snapshot.schema.yaml` is present.

  So `main` is not re-measured on a second checkout here (the brief confines this writer to its worktree). The three causes are each shown independent of the branch instead, and the required `pytest-suite` check on the PR is the measurement in CI's own environment.
- **Scope (quickstart step 5).** `git diff --name-only origin/main...HEAD -- governance/review-authority openXwallet openspec/changes/renew-resolved-council-protocol` prints nothing.

### Interpretations, as the review settled them

- **Reading 1 is superseded by B1.** Recognition rule (b) reads `signature.protocol`, as above.
- **Reading 2 is sound, and E1 rule 2 settles it.** `protocol: xfactory-council-seat-key-authorization/v1`, a legacy *signing context* used as a protocol value, is `protocol_unknown`, not legacy. The vector `cls-offline-legacy-context-as-protocol-refuse` pins it.
- **Reading 3 is sound, and data-model now says so** in a dated sentence: at boundary `definition` the grammar is checked first, then canonicalizability.
- **Reading 4 is justified.** Two tests were corrected while going green:
  - the digest `$ref` test allows a `description` annotation beside the `$ref`;
  - the gate-wiring test separates the negated `! grep` pattern from the required ones.
- **Local runs.** Local pytest runs used `-p no:cacheprovider`, so that no `.pytest_cache` was written into the worktree.

### The delta review of `a1375ac96`, and SonarCloud on #1284 (2026-10-09T13:25Z onward)

The reviewer's delta review of `a1375ac96` returned READY AFTER FIXES. Every required check on #1284 at `3672b4e49` was green, but SonarCloud's quality gate failed on `new_security_rating` = 3 because of two new MAJOR issues. Each fix below was written test-first: the new tests ran red with 10 failed, alongside 168 that passed.

- **MEDIUM: a `$schema` below a document's root still switched the dialect.**
  - **Reproduced first.** In a copied tree, the reviewer's probe put `$schema: https://json-schema.org/draft/2020-12/schema` inside `$defs/opaque_id`. The schemas loaded, and `check_definition("opaque_id", "x\n")` ACCEPTED the value.
  - **Why.** 2020-12 allows `$schema` only at a resource root, but the metaschema check does not enforce that, and jsonschema re-selects the validator class at any subschema carrying one. The "at every depth" in `_registered_resource`'s docstring was therefore untrue.
  - **The fix.** `records.headers_below_root` walks each document. Loading refuses any `$schema` or `$id` below its root, and `check`'s family-schema judgement flags it too. An embedded `$id` is refused for the reason `references_outside` already assumed: such a resource is one it does not track.
  - **Now.** The reviewer's probe is refused at load: `shared-definitions.schema.yaml: carries $schema below its root, at $defs/opaque_id/$schema`. A test injects the nested header three ways: `$schema` and `$id` in the shared definitions, and a draft-07 `$schema` in the registry schema.
- **LOW: the pointers.** plan.md:63, research.md:32 and this record said "data-model E1 `key_fingerprint`", but that row lives in data-model § Shared definitions, and the pointers now say so.
- **LOW: a vector's name.**
  - `cls-offline-replacement-string-signature-accept` carries a `protocol` member, so it never reached the `signature.protocol` path its name suggests. It is renamed `cls-offline-replacement-protocol-with-string-signature-accept`, since rule 1 decides it.
  - New: `cls-offline-string-signature-without-protocol-refuse`. A seat result with no `protocol` member and a string `signature` is `protocol_unknown`, because recognition rule (b)'s path cannot reach into a string.
- **LOW: `check` on a family schema now runs the same `$ref` closure that load runs.** A `$ref` to a dialect metaschema or to an unloaded document is refused, and a `$ref` to the shared definitions or into the document itself is accepted.
- **Vectors changed their expectation after implementation, because of B1.** The red run of 2026-10-09T01:41Z measured against vectors authored on the first reading of recognition rule (b), which was `signing_context` and `context.signing_context`.
  - B1's evidence-based reading moves the rule to `signature.protocol`: the legacy seat result as codexFactory `council_seat_signing.py` writes it and Hermes `review_authority.py` reads it (§ The independent PR-1 review's fixes).
  - **Removed:** the two `signing_context` route vectors, `cls-offline-legacy-signing-context-route` and `cls-offline-legacy-nested-signing-context-route`.
  - **Expectation changed:** the record of the first of them now expects `refuse protocol_unknown`, not `route`, as `cls-offline-signing-context-member-refuse`.
  - **Inputs re-shaped onto the real path, outcomes unchanged:** `cls-offline-replacement-context-without-protocol-refuse` and `cls-offline-replacement-with-legacy-shapes-accept`.
  - No other vector moved.
- **SonarCloud `pythonsecurity:S8707` at `scripts/validate-council-convening.py:178`: path injection through a CLI an agent may drive.**
  - **The fix.** `check` now reads a PATH only after `_within_invocation_directory` canonicalizes it with `os.path.realpath`, which resolves `..` and symbolic links, and shows it equals, or lies below, the canonical working directory plus a separator. This is the rule's own compliant form. Any other PATH is refused as a harness failure, exit 2, and never read.
  - **Why not the repository root.** The sibling validators (`validate-signed-execution-chain.py`, `validate-clearing-dispatch.py`) only `resolve()` the path and check that it exists, so they offered no confinement to mirror. Confinement to the repository root would also break the contract's cross-repository use, in which a successor checks its own records. The working directory keeps that use.
  - **The contract changed, and says so.** [contracts/validator-cli.md](contracts/validator-cli.md) carries a dated "Tightened 2026-10-09" sentence, and its exit-2 row names a PATH outside the invoking directory.
  - **Tests.**
    - Refused: an absolute path, `../`, and a `..` inside an absolute path that leaves the directory, plus a symbolic link that does. Each exits 2 with no ERROR line.
    - Accepted: a relative path inside the directory, which reads and routes with exit 3.
    - The existing `check` tests now run from their own temporary directory.
- **SonarCloud `githubactions:S8541` at `.github/workflows/council-convening-gate.yml:64`: setup scripts could run during install.**
  - **The fix.** The install is now `pip install --require-hashes --only-binary :all: -r requirements/hermes-runtime-contracts.lock`, in a literal block, mirroring `former-id-arrival-gate.yml` and `openxdox-consumer-gate.yml`.
  - **Measured first.** `pip install --require-hashes --only-binary :all: --ignore-installed --dry-run --report … -r requirements/hermes-runtime-contracts.lock` on Python 3.12.3: exit 0, 17 packages, 17 wheels, 0 sdists.
  - **The wiring test.** `test_gate_wiring.py` pins the flag as the gate's only install, still ordered before the validator run. It holds `pytest-suite.yml` to the same lock and not to the same flags, since that workflow still carries the older form.
- **Not marked in Sonar.** Neither issue was marked false positive or accepted. The code was fixed, and SonarCloud's next analysis of #1284 is the measure.
- **Gates at this round's code (before the push):**
  - `python3 -m pytest tests/council_convening -q -m "not postgres"`: **320 passed**, at a load average of 168.
  - `python3 scripts/validate-council-convening.py`: exit 0, `133 vectors, 133 both-sides, sha256:b74c6dd509fca0a8a0b708820e38439a96259dc36777a2c11f6f6d70bd1ca745`, `vectors adjudicated: 133/133`, `refusal codes probed: 5/5`, `finding codes probed: 1/1`, `requirements probed: 2/2 (FR-001, FR-011)`, generator reproduced, 0 errors, 0 warnings.
  - `python3 -m scripts.council_convening.generate --check`: exit 0.
  - The corpus by outcome: accept 42, refuse 83, route 8.
  - On the coordinator's word, no local full suite this round: CI's `pytest-suite` is the measure.
