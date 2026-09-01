# Tasks: retire-doxbench-chat-turn-v1

**NOTHING BELOW SECTION 1 WAS PERFORMED BY THE PROPOSAL, AND RATIFICATION DID
NOT CHANGE THAT.** The packet is `Status: ratified` — Brett Heap, 2026-09-01, in
session, at pull request #552 tip `c5169476`; record
`review/ratification-2026-09-01.md`. In the pull request that carried it no
schema byte moved, no fixture was deleted, no manifest digest changed and no
CHANGELOG row moved. **Ratification authorized the requirement text and
performed none of the work below.** **Sections 2-5 are the realization**; § 6 is
the `contract-v3.0` CUT, a separate act; § 7 is post-cut verification; and § 8
is the archive gate the realization must clear before this change may archive at
all. (That range read "Sections 2-6" until the realization: one of the four
low-severity round-three Copilot comments the ratification record § 3 left
standing, corrected here because this file is edited anyway.)

---

**REALIZATION §§ 2-5 IS DRAFTED AND NOT MERGED**, in its own pull request off
`main`, by a session that took no cut act. The ticks below carry their evidence
inline. Three things it deliberately did NOT do, each for a stated reason rather
than an omission:

* **§ 6 and § 7 are untouched.** No bundle number is spent, no CHANGELOG row
  moves, `docs/contract-versioning-policy.md` is not edited, no
  `contract-v3.0.digests.yaml` is written and no tag is published.
* **§ 2.2-2.4's byte removal IS performed, and it dragged ONE cut-filed line
  with it.** The schema's per-file `sha256` in `contracts/manifest.yaml` moved
  in the same commit as the bytes. That line is filed at § 6.1, but § 8.1
  requires §§ 2-5 to be MERGED AND `pytest-suite` GREEN, and the two cannot both
  hold: `doxbench_contracts._verified_bytes` refuses a checkout whose manifest
  records a digest the bytes do not hash to, so a schema edit without the
  manifest line fails 45 tests with `ContractPinError ... the checkout is not a
  coherent contract-v2.2 release`. Measured, not assumed. § 8.2's own wording —
  the bundle is later "declared with the MOVED digest" — reads the same way.
  **Nothing else in § 6.1 moved**: `contract_bundle_version` still says
  `contract-v2.5`, and `doxbench_contracts.CONTRACT_REF`/`CONTRACT_TAG` still
  name `contract-v2.2`, because bundle IDENTITY is the cut's to spend. The
  stale tag label is owed to the cut and named here so it is not discovered
  there.
* **§ 5.1's baseline retirement rides the same act as the bytes it guards** —
  see the box.

**ONE MEASUREMENT DID NOT SURVIVE CONTACT WITH THE TREE**, and § 2.1 is where it
is recorded rather than absorbed. See that box.

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
- [x] 1.7 **RATIFIED by the repository owner** — Brett Heap, 2026-09-01, in
      session ("ratify #551 and #552"), at pull request #552 tip `c5169476`, on
      an orchestrator's report of the two packets read together. Record:
      `review/ratification-2026-09-01.md`. Ratification authorizes the
      requirement text and performs none of the realization below. It ratifies
      the fallback posture AS ENCODED at 1.2; the #522 ruling set only its
      direction.
- [ ] 1.8 **Adversarial review to convergence — STILL OPEN, and the order this
      box originally stated was INVERTED by events rather than met.** It was
      written as "review to convergence, THEN ratification"; what happened is
      that three Copilot rounds ran and every finding through round two was
      taken, while **every one of three `@codex review` requests returned a
      PROVIDER USAGE-LIMIT REFUSAL and no verdict**. The absence was disclosed
      to Brett and he ratified against it. **FOUR low-severity round-three
      comments stand UNCORRECTED on the ratified head** — enumerated in the
      ratification record § 3 — because correcting them would have produced a
      head other than the one he ruled on. **A CODEX PASS REMAINS OWED and is
      blocked by nothing in this packet**; it and those four route to the
      amendment lane, not to doubt about the ratification.

## 2. Speckit F1 — the schema

- [x] 2.1 Compute the SURVIVING family's reference closure from
      `request_v2`/`success_v2`/`failure_v2` — the same computation the existing
      baseline test performs for v1 — and use it, not inspection, to decide
      which `$defs` may go. Expected retained: `content_hash`, `confined_path`,
      `scope_key`, `buffer_state`, `transcript_turn`, `typed_proposal`. Any
      definition the computation says is v1-only is removed; any surprise is a
      finding, not a licence.
      **PERFORMED, AND IT RETURNED A SURPRISE.** Run with `_local_refs`'s own
      algorithm seeded from the three `-v2` envelopes, against the schema as it
      stood at `af746459`:
      * v2 closure — `buffer_key`, `buffer_state`, `confined_path`,
        `content_hash`, `context_packet`, `failure_v2`, `keyed_observed_hashes`,
        `keyed_typed_proposal`, `provider_retry`, `request_v2`, `scope_key`,
        `selected_model`, `success_v2`, `transcript_turn`
      * v1 closure — `request`, `success`, `failure`, `content_hash`,
        `confined_path`, `scope_key`, `buffer_state`, `transcript_turn`,
        `typed_proposal`
      * **v1-ONLY (v1 closure minus v2 closure) — `request`, `success`,
        `failure`, and `typed_proposal`**
      * orphaned by neither closure — none
      **`typed_proposal` IS NOT REACHABLE FROM THE SURVIVING FAMILY**, and the
      ratified requirement says it is: *"`content_hash`, `confined_path`,
      `scope_key`, `buffer_state`, `transcript_turn` and `typed_proposal` are
      `$ref`-ed by the v1 envelopes AND reachable from the surviving family"*.
      The premise is false for one of the six. `keyed_typed_proposal` RESTATES
      the shape with a buffer-key target rather than `$ref`-ing
      `typed_proposal`, so the widened family never points at it.
      **DISPOSITION: RETAINED, and the surprise recorded.** This box's own rule
      is that a surprise is *"a finding, not a licence"*, so the realization does
      not use it as cover to remove bytes the ratified text names as retained.
      The definition stays, now unreferenced, carrying a comment at its site that
      states the measurement and hands the disposal decision to the cut. What is
      removed is exactly `request`, `success` and `failure`. The retention of
      the other five is measured, not assumed, and each is genuinely reached.
- [x] 2.2 Remove `$defs/request`, `$defs/success`, `$defs/failure` and their
      three `oneOf` refs at `:58-60`.
      Done: the top-level `oneOf` now holds exactly
      `request_v2`/`success_v2`/`failure_v2`, and `yaml.safe_load` over the file
      reports `$defs` without the three v1 keys.
- [x] 2.3 Remove the top-level `deprecated_envelopes` block (`:70-82`) and its
      explanatory comment (`:64-69`). A block declaring the deprecation of kinds
      the file no longer defines names nothing.
      Done: `"deprecated_envelopes" in yaml.safe_load(...)` is now `False`. The
      validator's READER of that block is deliberately kept (4.2) and simply
      reports nothing.
- [x] 2.4 Confirm the surviving envelopes' bytes are otherwise untouched — not
      one field added, removed or renamed.
      Confirmed: `git diff` over the file touches the three v1 `$defs`, the
      three `oneOf` refs, the `deprecated_envelopes` block and its comment, the
      file-level `description` prose, and one added comment inside
      `typed_proposal` (2.1). **No property, `required` entry, bound, pattern or
      `$ref` inside `request_v2`, `success_v2`, `failure_v2` or any retained
      shared definition changed.**
      **THE `description` PROSE WAS REPAIRED, and it is beyond this box's
      literal enumeration.** The file's own `description` said *"three closed
      envelopes … the request (workbench-chat-turn)"*, described the v1 family
      as *"DEPRECATED by this release; see `deprecated_envelopes` below"*, and
      documented `active_document_path`. Every one of those sentences names
      something this change removes. Leaving them is the exact failure the
      packet's own scenario "Prose that survives its own subject" forbids, so
      they are repaired here rather than left for the cut. Named as a judgement
      beyond the enumerated surface rather than folded in silently.

## 3. Speckit F2 — the runtime, including the redesigned fallback

- [x] 3.1 `serve.py`: replace the kind-discrimination `else` arm (`:3554-3557`)
      with the answered posture. The surviving request kind parses as today;
      anything else refuses. **Do not merely delete the arm** — a deleted arm
      leaves the default selecting a parser and a builder that are gone.
      Done in `_handle_workbench_chat_turn`. The arm now reads
      `if request_kind != DOXBENCH_CHAT_TURN_V2_KIND: self._refuse_turn(
      validators, DOXBENCH_ERR_UNRECOGNIZED_TURN_KIND, turn_id,
      failure_kind=DOXBENCH_CHAT_TURN_V2_FAILURE_KIND); return`, and the
      surviving kind falls through to the parser and schema gate unchanged.
      **ONE ORDERING CHANGE THE REDESIGN FORCED, stated rather than slipped in:**
      the plane-level `validators is None` guard is HOISTED above the kind
      check. It used to sit below, which was harmless while the arm only
      SELECTED a parser; the arm now BUILDS a refusal that is self-validated
      against the released schema, and that cannot be done with no validators.
      The precedence is unchanged — a plane-level verdict still outranks any
      defect in the caller's request, and still answers in the fixed
      pre-identity shape.
- [x] 3.2 `serve.py`: register the unknown-kind code in `DOXBENCH_ERROR_CATALOG`
      with its status and fixed message, in the SAME commit as the code is first
      answered. An unregistered code raises rather than refuses (OQ-3 picks the
      token and the status).
      **OQ-3 ANSWERED: the token is `unrecognized_turn_kind` and the status is
      400.** `DOXBENCH_ERR_UNRECOGNIZED_TURN_KIND` and its fixed module-level
      message (*"this route does not serve the chat-turn kind the request
      declared"*) are registered in `DOXBENCH_ERROR_CATALOG` in the same commit
      as the arm at 3.1. The token satisfies `failure_v2`'s
      `^[a-z][a-z0-9_]{2,63}$`. `invalid_turn_request` was NOT reused: its fixed
      message says the request is malformed, which is a true sentence about a
      different failure — a request naming an unserved `kind` may be perfectly
      well formed in the family it names — and the record beside the constant
      says so.
- [x] 3.3 `serve.py`: remove the three v1 kind constants (`:377-379`), the v1
      success builder `doxbench_turn_success_body` (`:1025-1059`), and the v1
      parser `_parse_workbench_chat_turn_body` (`:3450-3462`). Re-point the v1
      DEFAULTS on `doxbench_turn_failure_body` (`:954-957`) and `_refuse_turn`
      (`:3277-3279`) at the surviving failure kind.
      All five done; `grep` for the three constant names, the builder and the
      parser returns only the sited comments that record their removal. Both
      defaults now read `DOXBENCH_CHAT_TURN_V2_FAILURE_KIND`. **A SIXTH SITE
      THE BOX DOES NOT NAME went with the builder:** the success-building
      `if success_kind == DOXBENCH_CHAT_TURN_V2_SUCCESS_KIND: … else: …` in the
      dispatch tail, whose `else` was the only caller of
      `doxbench_turn_success_body`. It collapses to the unconditional v2 build
      — a branch on `success_kind` would now test a condition that cannot be
      false — and the two RECORDED v1 limitations it carried (no
      `selected_model` on a routed turn, contract-v1.38 F3; no `context_packet`,
      contract-v1.40 task 10.7) end with the envelope that had no room for them.
- [x] 3.4 **Leave the pre-identity fallback in `_refuse_turn` (`:3310-3317`)
      exactly as it is.** It is the correct answer for a request with no
      wire-valid identity, and the surviving failure envelope requires a
      `client_turn_id` no server may invent.
      **UNTOUCHED.** The four executable lines are byte-identical: `status =
      doxbench_error_status(code)`, the `if turn_id is not None:` build +
      `_doxbench_wire_conforms` gate, and the unconditional
      `self._send_json(status, doxbench_error_body(code, limit=limit))`. Only
      the docstring changed, to say WHY the layer is unchanged rather than to
      change it.
- [x] 3.5 `scripts/ideation_dashboard/doxbench_contracts.py`: remove the three
      v1 kind constants (`:265-267`).
      Done, and the three names they fed went with them: `CHAT_TURN_DEFS` and
      `WIRE_KINDS` now hold the catalog kind plus the three `-v2` kinds.
      **`DEPRECATED_CHAT_TURN_KINDS` IS REMOVED RATHER THAN EMPTIED**, which
      this box does not name and which is a judgement worth stating: an empty
      tuple is an assertion that nothing in this family is deprecated, and this
      module has no business making that claim on the release's behalf. The
      schema's own `deprecated_envelopes` block is the authority, it is READ and
      never restated (4.2), and it is gone from the chat-turn file because it
      named only these three kinds.
- [x] 3.6 Confirm the shipped client needs no change —
      `web/views/doxbench-chat.js:37-39` is `-v2`-only — and that its failure
      handling routes the new code sensibly rather than rendering a raw token.
      **CONFIRMED, and no client byte changed.** `CHAT_TURN_KIND`,
      `CHAT_SUCCESS_KIND` and `CHAT_FAILURE_KIND` are the three `-v2` spellings,
      so the client never emits a removed kind. Its failure path matches on
      `response.payload.kind === CHAT_FAILURE_KIND` — which the new refusal
      carries — and hands the payload to `settleTurnFailure`, which retains the
      two released fields and renders the SERVER's fixed `message`. The human
      therefore reads *"this route does not serve the chat-turn kind the request
      declared"*, not the token. **The token itself needs no rail entry**:
      `fallbackShapeFailureFor`'s one-code whitelist is for the PRE-IDENTITY
      shape, and its recorded narrowness — never inventing prose for conditions
      a fix did not measure — is the reason not to add one here.

## 4. Speckit F3 — the validator and the packaged corpus

- [x] 4.1 `scripts/validate-ideation-dashboard-contracts.py`: remove the three
      v1 rows from the kind→schema map (`:144-146`), the three tag-dispatch arms
      (`:392-397`), and the v1 kind from the paired-family tuple (`:1561-1562`).
      All three done. The paired-family tuple is left a ONE-MEMBER TUPLE
      (`("workbench-chat-turn-v2",)`) rather than flattened to an equality: the
      rule is about REQUEST kinds as a class, and the next co-resident family
      joins it there.
- [x] 4.2 Decide what survives of the `deprecated_envelopes` reader
      (`:309-345`). It is a GENERAL mechanism, not a v1 one — it reads whatever
      any loaded schema declares — so removing it because its only current
      subject is going would delete the estate's only machine-readable
      deprecation reader. Default: KEEP it; it simply reports nothing.
      **DECIDED: KEPT, both halves — `deprecated_kinds` and
      `warn_if_deprecated_kind` — with not one line of logic changed.** It now
      returns `{}` over the packaged schemas, which is the correct report and
      not a defect. The reason is written at the site: deleting it because its
      only subject went would leave the NEXT deprecation inert, which is the
      precise failure this whole retirement exists to correct.
- [x] 4.3 Delete the four positive v1 fixtures under
      `examples/ideation-dashboard/`.
      Deleted: `workbench-chat-turn-unsaved-edits`, `-outline-only`,
      `-prose-only`, `-both-proposals` (`.example.yaml`). The packaged-positive
      count moves 46 → 42 and `examples/ideation-dashboard/README.md`'s layout
      tree and schema/fixture table drop their rows.
- [x] 4.4 **The eight NEGATIVE v1 fixtures: each of the seven refusal classes is
      re-expressed as a `-v2` negative or its loss is recorded with a reason.**
      escaping path; hash mismatch; identity subject; over budget; unknown model;
      untyped proposal; duplicate turn pair. None of the seven has a `-v2`
      equivalent today. Silence is not a permitted outcome for any of them.
      **ALL SEVEN RE-EXPRESSED. ZERO STATED LOSSES.** Every one was reachable in
      the surviving family, so the "or its loss is recorded" arm is never taken
      — which is itself the finding, and better than the packet feared. Each new
      fixture was run through `validate_instance` individually and refuses for
      the INTENDED reason, not merely for some reason:

      | # | refusal class | v1 fixture (removed) | `-v2` fixture (added) | the refusal it actually produces |
      |---|---|---|---|---|
      | 1 | escaping path | `negative/workbench-chat-turn-escaping-path.negative.yaml` | `negative/workbench-chat-turn-v2-escaping-path.negative.yaml` | `[path] buffers/../../etc/passwd/path: path escapes the checkout` |
      | 2 | hash mismatch | `negative/workbench-chat-turn-hash-mismatch.negative.yaml` | `negative/workbench-chat-turn-v2-hash-mismatch.negative.yaml` | `[hash] buffers/outline: content_hash mismatch (declared 000000000000…, actual 9bfe55abe3ac…)` |
      | 3 | identity subject | `negative/workbench-chat-turn-identity-subject.negative.yaml` | `negative/workbench-chat-turn-v2-identity-subject.negative.yaml` | `[schema] <root>` — refused by TYPE alone, exactly as in v1 |
      | 4 | over budget | `negative/workbench-chat-turn-over-budget.negative.yaml` | `negative/workbench-chat-turn-v2-over-budget.negative.yaml` | `[budget] request buffers total 4139 bytes over model 'hosted-zr-1' input limit 2048` |
      | 5 | unknown model | `negative/workbench-chat-turn-unknown-model.negative.yaml` | `negative/workbench-chat-turn-v2-unknown-model.negative.yaml` | `[unknown-model] model_id 'never-approved-9' is not in the approved catalog` |
      | 6 | untyped proposal | `negative/workbench-chat-turn-untyped-proposal.negative.yaml` | `negative/workbench-chat-turn-v2-untyped-proposal.negative.yaml` | `[schema] <root>` — `keyed_typed_proposal` requires `target`, as `typed_proposal` did |
      | 7 | duplicate turn pair | `negative/duplicate-turn-pair/{turn-a,turn-b}.yaml` | the SAME two paths, rewritten as `-v2` requests | `[duplicate-turn] turn-b.yaml: duplicate-turn id 'turn-dup-1' with different content (first seen in turn-a.yaml)` |

      **Conversion rule, applied uniformly to the six request-class fixtures:**
      `kind` → `workbench-chat-turn-v2`; `active_document_path` DROPPED and
      `bound_buffer` declared in its place, per design D17's "stated, never
      inferred". Class 6 is a SUCCESS envelope and converts differently — keyed
      `observed_hashes`, an added `selected_model`, a `bound_buffer` — while its
      one violation (a proposal with no `target`) is carried over untouched.
      **Class 1's `bound_buffer` deliberately names `outline`** so the escaping
      path stays the single intended violation rather than becoming two.
- [x] 4.5 Add a packaged `-v2` negative (or a test) for the NEW refusal: an
      unrecognized kind answered with the unknown-kind code.
      Added `negative/workbench-chat-turn-unrecognized-kind.negative.yaml`,
      refused `[kind] unrecognized document (no known kind, no
      'possibles_register' section)`. **Its `kind` is deliberately
      `workbench-chat-turn` — a RETIRED one** — because that makes the fixture
      the packaged proof of the ruled consequence: after the removal a retired
      kind and a kind that never existed are the same fact about the wire, and
      the closed `oneOf` refuses both identically. The RESPONSE half (the
      `workbench-chat-turn-v2-failure` body carrying `unrecognized_turn_kind`)
      is covered by test rather than by fixture — see 5.3 — because it is a
      SERVER-BUILT body and the route self-validates it, so a packaged instance
      would restate what the route already proves.
- [x] 4.6 Repair `examples/ideation-dashboard/README.md:307-313`, whose
      `--strict` note has been false since `contract-v2.0` shipped.
      Repaired, and the falsehood is NAMED rather than quietly overwritten: the
      note now records that it asserted a spent target for one major and five
      minors, that `contract-v2.0` shipped on 2026-08-27 without the removal,
      and that this is the silent failure issue #522 was filed about. The layout
      tree and the schema/fixture table in the same file are updated to the
      corpus as it now stands.
- [x] 4.7 Re-run `python3 scripts/validate-ideation-dashboard-contracts.py`.
      Expected: `0 error(s), 0 warning(s)` where it reports four warnings today,
      and `--strict` no longer failing on the chat-turn fixtures.
      **BOTH MET.** Default run:
      `validate-ideation-dashboard-contracts: 0 error(s), 0 warning(s)`
      (`examples: 42 valid example(s) confirmed valid, 81 negative example(s)
      confirmed invalid, 8 transition pair(s) confirmed`), against
      `0 error(s), 4 warning(s)` on `main` at `af746459`. **`--strict` now exits
      0** over `examples/ideation-dashboard/`, where it exited 1 before. The
      four warnings are gone because their subjects are gone, not because the
      reader that emitted them was removed — see 4.2.

## 5. Speckit F4 — the tests

- [x] 5.1 Retire `tests/ideation-dashboard/fixtures/chat-turn-v1-envelopes.baseline.yaml`
      and the byte-identity assertion at
      `tests/ideation-dashboard/test_doxbench_contracts.py:1213-1239`, **naming
      in the commit and in the changelog entry what the test was for**: it
      exists to prove the deprecated bytes never moved, and it ends because the
      shape it protects leaves the published surface.
      Done. `test_the_v1_envelope_bytes_are_unchanged_by_the_release`, the
      fixture, and the helpers that fed only it (`V1_ENVELOPE_BASELINE`,
      `_v1_ref_closure`, `_local_refs`, `_defs_order`) are removed;
      `_defs_blocks` SURVIVES, feeding
      `test_the_widened_family_is_the_only_one_the_file_declares`.
      **THE NAMING IS THE SUBSTANCE OF THIS BOX AND IT IS DONE IN THREE
      PLACES.** (1) A banner stands where the test was, recording what it
      asserted, the F1 hardening that widened it from the three envelope blocks
      to their whole `$ref` closure after a narrower guard went green while
      `buffer_state.kind`'s and `typed_proposal.target`'s enums were both
      mutated, and why it ends. (2) The commit message states it. (3) The
      CHANGELOG entry the CUT writes is where D4 requires it, and that is task
      **6.3** — **STILL OWED, and this box does not discharge it.**
      **WHY IT ENDS IS NOT "IT BECAME INCONVENIENT", AND THE DIFFERENCE IS
      CHECKABLE.** The assertion protects a shape consumers are PINNED to. At
      contract-v3.0 that shape leaves the published surface, so the assertion
      has no subject — there are no v1 `$defs` left to compare, and
      `_v1_ref_closure` would raise `KeyError` on its own seed rather than fail
      an assertion. A consumer pinned below contract-v3.0 keeps the promise it
      was given, and keeps it by the IMMUTABILITY OF THE BYTES ITS PIN NAMES
      rather than by their continued presence here.
- [x] 5.2 Move the v1 kind literals out of the remaining test files, across BOTH
      directory spellings: `tests/ideation-dashboard/` (`test_doxbench_contracts.py`,
      `test_doxbench_transport.py`, `test_doxbench_routes.py`,
      `test_doxbench_chat_view.py`, `test_doxbench_knowledge_service.py`,
      `test_doxbench_proposals.py`, `test_doxbench_view.py`) and
      `tests/ideation_dashboard/` (`test_validate_ideation_dashboard_contracts.py`).
      All eight done, **plus a NINTH this box does not name**:
      `tests/ideation-dashboard/test_doxchat_model_intake.py` also carried the
      literals. Recorded as an authoring finding rather than folded in silently.
      **AND A TENTH THAT NO KIND-LITERAL SWEEP COULD HAVE FOUND, because its
      coupling is to 3.2 rather than to a kind:**
      `tests/ideation-dashboard/test_doxbench_request_handling.py` holds
      `test_doxbench_error_catalog_has_exactly_the_grounded_code_set`, which
      asserts `DOXBENCH_ERROR_CATALOG`'s key set EXACTLY against a set built
      from per-era groupings, each carrying the grounding of its members. The new
      `unrecognized_turn_kind` entry made it fail with `Extra items in the left
      set: 'unrecognized_turn_kind'` — **which is the guard working correctly**:
      it is designed to fail on any code that has not had its provenance written
      down, and the packet's OQ-3 left this token to the realization to pick. It
      is answered the way the guard asks: a new `_REMOVAL_CODES` grouping, with
      the grounding recorded beside it — what the redesign requires, why 400,
      and why `invalid_turn_request` is not reused. **Ticking 3.2 without this
      would have left the estate's closed-catalog invariant red**, so the two
      boxes are one act.
      The discipline applied: a test exercising behaviour the surviving family
      ALSO has is RE-EXPRESSED against `-v2`; a test whose only subject was the
      v1 family's SURVIVAL or its DEPRECATION RECORD is deleted and replaced by
      the negative that now carries the claim. Every remaining occurrence of a
      v1 spelling in `tests/` is deliberate and is one of exactly three things:
      an assertion that a retired kind is ABSENT
      (`test_no_deprecated_kind_register_survives_the_removal`), a probe that a
      retired kind takes the unrecognized-kind path (5.3), or the
      `test_doxbench_chat_view.py` FOREIGN-KIND sample — kept as the retired v1
      failure spelling deliberately, because after the removal it is the most
      likely foreign kind that rail will ever actually see (an unupgraded
      client's own answer replayed at it) and the rule under test is about kinds
      the rail has no released reader for, which a retired one is by definition.
- [x] 5.3 New coverage for the redesigned fallback, in BOTH directions: an
      unrecognized kind WITH a wire-valid turn id -> the surviving failure
      envelope with the code, self-validated; WITHOUT one -> the pre-identity
      shape, unchanged. Plus a probe that a removed v1 kind takes exactly that
      path.
      All three directions covered in
      `tests/ideation-dashboard/test_doxbench_routes.py`:
      * a request naming NO kind at all, and one naming a RESPONSE kind, each
        refused `unrecognized_turn_kind` in a
        `workbench-chat-turn-v2-failure` envelope;
      * the same request with NO wire-valid `client_turn_id` answered in
        `doxbench_error_body`'s pre-identity shape — same code, same fixed
        message, no `kind` key;
      * **the probe**: `_turn(kind="workbench-chat-turn")` — a RETIRED kind —
        refused by exactly that path, asserting the failure envelope's `kind`
        and that the model port was never called. The retired spelling is a
        LITERAL rather than a `doxbench_contracts` constant, deliberately: the
        constant is removed with the kind, so a test that could only be written
        while the constant existed could not say what this one says.
      Plus a parity check that `DOXBENCH_ERR_UNRECOGNIZED_TURN_KIND` is
      registered in `DOXBENCH_ERROR_CATALOG` with its status and that its
      message IS the module-level constant, so an unregistered code cannot
      reach the refusal path (the "The new code is not registered" scenario).

## 6. The `contract-v3.0` cut (a SEPARATE act, listed for completeness)

- [ ] 6.1 `contracts/manifest.yaml`: the schema's `sha256` moves off
      `2ff5f222…`; the row prose drops its v1 clauses;
      `contract_bundle_version`, and `contract_schema_version` per OQ-2's answer.
- [ ] 6.2 `contracts/README.md:86`: the long row.
      **AND ONE MORE LINE THE REALIZATION'S REVIEW FOUND, RECORDED HERE SO THE
      CUT DOES NOT HAVE TO REDISCOVER IT.** `contracts/manifest.yaml`'s
      `consumption_rule` prose for `xfactory-workbench-chat-turn` still
      describes the co-resident layout as *"SIX closed envelopes"*. Copilot
      raised it against the realization pull request and it is CONFIRMED: the
      sentence is false the moment the v1 `$defs` leave. It is NOT fixed in the
      realization, and the reason is a boundary rather than an oversight — 6.1
      files "the row prose drops its v1 clauses" with the cut, and unlike the
      per-file `sha256` on the line above it, NOTHING FAILS while this prose is
      stale. The digest had to move for §§ 2-5 to be green at all (see the
      header); the prose does not, so the realization leaves it where the packet
      put it rather than crossing the same line twice.
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
