# Tasks — admit-deliberation-clearing-operation

Status: draft

Phase 1 is this pull request. **Phases 2–4 are a SPECKIT SLICE AFTER
RATIFICATION** — ratification authorizes realization, it does not perform it, and
no `contracts/` byte moves before task 1.1 is done.

## Phase 1 — Governance (this pull request)

- [ ] 1.1 **RATIFICATION by Brett Heap (repository owner).** The basis requires
      "a spec delta and a reviewer" for an admission, so this is the task that
      makes the entry lawful. Record the act at
      `openspec/changes/admit-deliberation-clearing-operation/review/ratification-<YYYY-MM-DD>.md`
      — the record placement `add-clearing-dispatch-boundary` and
      `add-cpc-clearing-boundary` both use — carrying the verbatim word, the
      ratified head sha, and the lane the ruling targets (Lane Collision Protocol
      Rule 2: a ruling that names no lane, no PR and no head sha authorizes
      nothing). On ratification, `Status:` moves to `ratified` and the proposal
      gains a `Ratified:` line naming the record.
- [x] 1.2 **Duplicate check across FOUR surfaces, recorded in `.openspec.yaml`'s
      origin reason.** Active changes, open pull requests, remote branches, and
      same-day merges to `main` — run 2026-09-04T04:40Z and re-run 05:05Z at
      `origin/main` `9ef151ad`. Result: no sibling, no successor, no duplicate.
- [x] 1.3 **Rule 1 claim on the governing record**, codexFactory PR #165:
      https://github.com/opensoft/codexFactory/pull/165#issuecomment-5535747335
- [x] 1.4 **Rule 7 shared-substrate claim** for the README OpenSpec Records
      block (row 3) and the sequenced-after ledger (row 2), with the movement
      MEASURED rather than predicted:
      https://github.com/opensoft/openxFactory/issues/630#issuecomment-5535802164
- [x] 1.5 **OQ1 settled** by Brett Heap 2026-09-04 ("Ruling OQ1: new neutral
      deliberation-return schema"); encoded as design D4, not as an open
      question.
- [x] 1.6 **OQ2 resolved by measurement** (design D11): the live pin is the
      per-change ledger, this packet adds ONE row, flips no partner, and owes no
      MOVEMENT LOG entry.
- [ ] 1.7 **The consumer's dependency ticks when 1.1 lands.** codexFactory #165
      tasks.md 1.6 is a DEPENDENCY task on this change; report the ratified head
      and the merge sha there.

## Phase 2 — Realization (a Speckit slice, AFTER 1.1)

Each item names the assertion it must satisfy. `python3 -m pytest tests/clearing -q`
must be green at the end, and so must `python3 scripts/validate-clearing-dispatch.py .`

- [ ] 2.1 **`contracts/clearing/permitted-operations.registry.yaml` gains ENTRY
      NUMBER TWO.** Every field the ratified requirement fixes, in the order
      entry one uses: `operation_id: deliberation`; `title`;
      `permitted_semantics.may` / `.may_not` (both non-empty — an entry listing
      only permissions describes a capability, not a bound); `class_constraints`
      = `checks_out_code: false`, `writes: false`, `may_reference_secrets:
      false`, `token_scopes: [actions:read]`, a bounded `timeout_minutes`;
      `worker_profile: council-deliberation-worker`; ONE lane
      (`artifact` / `xfactory-artifact-workers` / `host-rider-cpc-brett01` /
      `xfactory-artifact-cpc-brett01`); `output_schema_ref:
      contracts/clearing/deliberation-return.schema.yaml`; `data_handling:
      internal-governance`; `repository_affecting_output: false`. The lane's
      `lane_key` is `artifact` — the register's lane shape requires all four
      members and none is optional. **ADVANCE `registry_version` 1 → 2**: the
      instance's identity is `const` but its version is not, and a governed
      change to the closed set that left the version at 1 would make two
      different registers indistinguishable by their own declaration
      (`test_the_registry_declares_its_own_identity` only asserts `>= 1`, so
      this one is on the author). Rewrite the instance's header comment: the
      "EXACTLY ONE MEMBER TODAY" paragraph and the "`deliberation` IS NOT HERE ON
      PURPOSE" paragraph both become the record of when and by what it arrived,
      and the honest-limit paragraph is retained. **Assertion:**
      `test_the_shipped_instance_holds_exactly_the_ratified_set`, plus a new
      entry-two twin of `test_the_entry_declares_every_ratified_fact` and of
      `test_both_ratified_lanes_are_declared_with_literal_group_and_label`
      (entry two declares ONE lane, and a test that only ever read entry one
      would pass over a malformed entry two in silence).
- [ ] 2.2 **Author the NEW NEUTRAL `contracts/clearing/deliberation-return.schema.yaml`**
      (OQ1, ruled — design D4). Minimal: the per-seat outputs as STRUCTURED
      EVIDENCE — seat identity, that seat's output (inline payload or reference),
      and the run identifiers binding the return to the convening job id, the
      VERIFIED subject pin, and the INBOUND bundle digest it answers.
      `additionalProperties: false`. **NO verdict / eligibility / decision /
      go-no-go / approval / recommendation member** — the `VERDICT_WORDS` scan
      applies (2.5). Declares no digest construction, no handling vocabulary and
      no job envelope; references the ones already in force. Its top-level
      `kind` is the ratified **`xfactory_clearing_deliberation_return`** (design
      D4/D13) — not a name chosen at realization. Registered in
      `contracts/manifest.yaml` (a SEVENTH family row, with its digest), added to
      the validator's `SCHEMA_FILENAMES` and `KIND_TO_SCHEMA`, listed in
      `contracts/clearing/README.md`'s shape table and the repository README doc
      index, with ONE positive example and AT LEAST ONE negative fixture.
      **Assertions:** `test_the_family_ships_five_schemas` moves to SIX and its
      exact filename list gains the new schema (its docstring: *"A sixth arriving
      without a change to this line is a shape nobody ratified"* — this change is
      that ratification); `test_the_corpus_covers_every_shipped_kind` is
      satisfied by the positive example; `test_every_schema_is_meta_valid_and_self_identifying`
      and `test_every_schema_closes_its_root_to_unknown_members` pass on it; the
      schema validates its own example and refuses its own fixture; and the
      clearing gate's `N/N closed refusal codes red-proven` line still reads
      `N/N`.
- [ ] 2.3 **FIVE frozen copies move in ONE reviewed diff** (design D9):
      (a) `scripts/validate-clearing-dispatch.py` `RATIFIED_OPERATIONS`;
      (b) `tests/clearing/test_register_closure.py` `RATIFIED` (the INDEPENDENT
      copy — do not import one from the other, the independence is the control);
      (c) the instance from 2.1; (d)
      `.github/workflows/clearing-dispatch-gate.yml`'s literal
      `\(1 registered operation\)` grep, which its own comment says only a
      governed contract change may move; (e)
      `tests/clearing/test_clearing_gate_wiring.py::test_the_assertion_pins_the_registers_literal_member_count`,
      which asserts that same literal from a SECOND file — found in review round
      1, and the copy a reader of the contract tree would never see.
      **Assertion:** `clearing-dispatch-gate` green on the PR, with its "the
      closed register was not opened" fail line not fired, and
      `pytest tests/clearing` green.
- [ ] 2.4 **Re-point the two `deliberation` negative fixtures to `coding`**
      (design D8) — `examples/negative/register-carrying-an-unratified-operation.yaml`
      and `examples/negative/manifest-naming-an-unregistered-operation.yaml` —
      and REWRITE THEIR COMMENTS to argue about `coding` (the basis's design D11
      names it as the next real later operation; `execution-lane-coding-worker.yml`
      is its grandfathered route on group 7). A fixture whose bytes say one thing
      and whose comment argues about another is worse than either.
      `tests/clearing/test_register_closure.py::test_deliberation_is_refused_by_name`
      re-targets with them AND IS RENAMED — `test_coding_is_refused_by_name` —
      keeping its docstring's argument intact: a test whose NAME says
      `deliberation` while its body builds `coding` is the same defect as a
      fixture whose comment and bytes disagree. **Assertion:**
      `clearing-register-member-unratified` and `clearing-unregistered-operation`
      both still FIRE, now on `coding`.
      **Also inspect, expecting NO change:**
      `examples/negative/dispatch-record-with-a-free-text-refusal-ground.yaml`
      claims `deliberation` as its operation but its declared failure is the
      free-text ground `operator_decided_it_looked_wrong`, which stays outside
      the enumeration after 2.10 and keeps the fixture red for its own reason.
      Confirm that by running it, not by reading it.
- [ ] 2.5 **Extend the verdict scan to the new return kind.** `check_operation_report`
      is dispatched by `kind == "xfactory_clearing_operation_report"`, so the
      `VERDICT_WORDS` name scan does NOT reach a return of a different kind today
      — measured, not assumed. Register the ratified kind
      **`xfactory_clearing_deliberation_return`** in `KIND_TO_SCHEMA` and route it
      through the verdict scan (extracting the shared check rather than copying
      it). **NO NEW FINDING CODE:** the refusal is the existing
      `clearing-report-carries-a-verdict`; the family's closed finding-code set
      is NOT widened by this change, and a return that fails JSON Schema is
      reported as the family's `schema` refusal, which that set deliberately
      excludes. **Assertion:** a negative fixture carrying a verdict-named member
      in a deliberation return is refused `clearing-report-carries-a-verdict`, and
      `test_no_fixture_declares_a_code_outside_the_closed_set` still passes.
- [ ] 2.6 **Prove each frozen copy fails ALONE.** Before the slice is called done,
      revert exactly one of the FIVE in 2.3 and confirm the change goes red, one
      at a time, five times. Five chances to move four and miss one is the
      failure mode (design D12); a copy that never went red is a copy nobody
      tested. Do the same for the three pinned numerals D9 names — the schema
      list five → six, the manifest rows six → seven, and the moved row
      digests.
- [ ] 2.7 **`examples/dispatch-record-refused.example.yaml` follows the fixture
      re-point** (design D8): its whole subject is a refused CLAIM of
      `deliberation`, which after admission documents a refusal that can no longer
      happen. `tests/clearing/test_dispatch_record.py::test_a_refusal_records_what_was_asked_for`
      asserts the claimed value literally and moves in the same commit.
- [ ] 2.8 **`contracts/clearing/README.md`**: the register section stops saying
      "exactly one member" and stops saying `deliberation` is deliberately
      absent; the shape table gains the return schema; the honest-limit paragraph
      is retained verbatim in substance and extended to name the gate's grep AND
      the test that pins that grep as the fourth and fifth copies (design D9).
- [ ] 2.9 **ADMIT THE THREE REFUSAL GROUNDS TO
      `contracts/clearing/dispatch-record.schema.yaml`** — `$defs.refusal_ground.enum`
      gains `lane_not_permitted`, `output_schema_failure` and
      `origin_scoped_credential`, and NOTHING ELSE (design D13; the six other
      awaited grounds stay absent until the operation that can emit them lands).
      Rewrite that `$defs`' description and the schema's header paragraph: "Two
      members today" becomes five, and the nine-awaited list shrinks to six, each
      naming the change that admitted it. The schema's `contracts/manifest.yaml`
      row DIGEST moves with the bytes
      (`test_the_row_digest_matches_the_artifact_on_disk`). **Assertion:** a
      packaged refused-dispatch record naming each of the three grounds validates
      clean, while
      `examples/negative/dispatch-record-with-a-free-text-refusal-ground.yaml`
      still fires `clearing-record-refusal-ground-unknown`. **THIS IS THE ONE
      TASK THAT WIDENS A CLOSED ENUMERATION, and it is lawful only because the
      ratified requirement names the three members; a fourth added here is the
      defect this packet exists to refuse.**
- [ ] 2.10 **Contract-tree bookkeeping that moves with the bytes.**
      `contracts/manifest.yaml`'s clearing-family header comment counts the
      corpus ("6 positive examples + 24 intended-invalid") and both numbers move
      — NOTE that the second is ALREADY STALE on `main`, where the validator's
      self-test reports 26 negative fixtures, so correct it to the measured
      count rather than incrementing the written one;
      the register instance's and the dispatch record schema's row digests move;
      `contracts/clearing/README.md`'s corpus counts move. **Assertion:**
      `tests/clearing/test_clearing_manifest_rows.py` green in full — rows,
      digests, ownership fields and declared bundle version.
- [ ] 2.11 **Green run of `python3 -m pytest tests/clearing -q`** and of
      `python3 scripts/validate-clearing-dispatch.py .` with the packaged corpus
      proving every closed refusal code still red-proven, and the whole corpus
      clean end to end.

## Phase 3 — The contract cut

- [ ] 3.1 **Claim the version number, not the files**, on openxFactory issue #630
      row 4 (Rule 7: a version number can be claimed once, and the tag is
      immutable). The minor is ALLOCATED AT REALIZATION by merge order:
      `docs/contract-versioning-policy.md` forbids a proposal reserving one.
- [ ] 3.2 **`contracts/manifest.yaml`** — register the new return schema and
      advance `contract_bundle_version` to the allocated minor, committed
      ATOMICALLY with the contract files.
- [ ] 3.3 **`contracts/CHANGELOG.md`** — one entry for the release, class
      **ADDITIVE (minor)**: a register gains a member and a new contract arrives;
      no shape is removed and no required field is added, so domain repos on the
      same major stay conformant without changes.
- [ ] 3.4 **`contracts/releases/<tag>.digests.yaml`** and the **annotated tag
      `contract-v<major>.<minor>` at the landed sha**, per the policy: the
      manifest version, changelog heading and tag must match, and the tag points
      at the realized commit.

## Phase 4 — Downstream notice (name it, do not do it)

- [ ] 4.1 **codexFactory #165 tasks.md 1.6 ticks** — report the ratified head, the
      merge sha, and the entry's declared facts on that PR so its legs 1–4 are
      written against the register rather than against this packet's prose.
- [ ] 4.2 **NAME, DO NOT DO: `opensoft/xFactory`'s `clearing-dispatch.yml`
      operation choice list.** `add-clearing-dispatch-boundary` tasks.md § 3.7
      makes it that lane's plumbing and states the consequence itself — once the
      registry instance exists, the workflow must validate the dispatched
      operation against the registry INSTANCE and stop relying on its own literal
      choice list as the authority. A green gate here does not discharge it.
- [ ] 4.2a **NAME, DO NOT DO — but WATCH: three packaged attestation fixtures in
      THIS repository carry `council-deliberation-worker.yml` as a LIVE
      allowlisted member of `xfactory-artifact-workers`**
      (`examples/negative/attestation-claiming-full-completeness-before-admission.yaml`,
      `attestation-filing-a-dark-lane-as-a-widening.yaml`,
      `attestation-with-one-estate-wide-expected-set.yaml`, and the positive
      `single-door-attestation.example.yaml`). The retirement in 4.3 makes each
      of them describe a world that no longer exists. They stay correct until
      that act and go stale the moment it lands, so the retiring change owes a
      follow-up openxFactory change refreshing them — named here so the staleness
      is scheduled rather than discovered.
- [ ] 4.3 **NAME, DO NOT DO: the route retirement.** The xFactory change that
      declares the `deliberation` host job must, in the same act, remove
      `council-deliberation-worker.yml`'s host jobs (`deliberate`, `smoke-seat`),
      remove its workflow-allowlist entry on `xfactory-artifact-workers`, and
      shrink the grandfather enumeration by that member (design D10; the entry's
      own scenario). Post the obligation on that repository's tracking record.

## Archive gate

- [ ] 5.1 **`release-realization`: a change with a non-empty code surface SHALL
      NOT archive until realization evidence is merged and green.** Evidence =
      Phase 2 merged on `main` with `pytest tests/clearing` and
      `clearing-dispatch-gate` green, plus Phase 3's cut.
- [ ] 5.2 **ORDERED AFTER `add-clearing-dispatch-boundary` ARCHIVES.** This
      packet's ADDED block rests on that change's unarchived addition; archiving
      first would promote an entry into a capability canon does not yet carry.
- [ ] 5.3 **Ledger row on archive.** Re-run
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`
      so this change's row flips `state: active` → `archived`; that move is
      explained by the row diff and owes no MOVEMENT LOG entry.
