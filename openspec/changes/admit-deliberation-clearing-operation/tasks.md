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
      internal-governance`; `repository_affecting_output: false`. Rewrite the
      instance's header comment: the "`deliberation` IS NOT HERE ON PURPOSE"
      paragraph becomes the record of when and by what it arrived. **Assertion:**
      `test_the_shipped_instance_holds_exactly_the_ratified_set`.
- [ ] 2.2 **Author the NEW NEUTRAL `contracts/clearing/deliberation-return.schema.yaml`**
      (OQ1, ruled — design D4). Minimal: the per-seat outputs as STRUCTURED
      EVIDENCE — seat identity, that seat's output (inline payload or reference),
      and the run identifiers binding the return to the convening job id, the
      VERIFIED subject pin, and the INBOUND bundle digest it answers.
      `additionalProperties: false`. **NO verdict / eligibility / decision /
      go-no-go / approval / recommendation member** — the `VERDICT_WORDS` scan
      applies (2.5). Declares no digest construction, no handling vocabulary and
      no job envelope; references the ones already in force. Registered in
      `contracts/manifest.yaml`, listed in `contracts/clearing/README.md`'s shape
      table and the repository README doc index, with ONE positive example and AT
      LEAST ONE negative fixture. **Assertion:** the schema validates its own
      example and refuses its own fixture, and the clearing gate's
      `N/N closed refusal codes red-proven` line still reads `N/N`.
- [ ] 2.3 **FOUR frozen copies move in ONE reviewed diff** (design D9):
      (a) `scripts/validate-clearing-dispatch.py` `RATIFIED_OPERATIONS`;
      (b) `tests/clearing/test_register_closure.py` `RATIFIED` (the INDEPENDENT
      copy — do not import one from the other, the independence is the control);
      (c) the instance from 2.1; (d)
      `.github/workflows/clearing-dispatch-gate.yml`'s literal
      `\(1 registered operation\)` grep, which its own comment says only a
      governed contract change may move. **Assertion:** `clearing-dispatch-gate`
      green on the PR, with its "the closed register was not opened" fail line
      not fired.
- [ ] 2.4 **Re-point the two `deliberation` negative fixtures to `coding`**
      (design D8) — `examples/negative/register-carrying-an-unratified-operation.yaml`
      and `examples/negative/manifest-naming-an-unregistered-operation.yaml` —
      and REWRITE THEIR COMMENTS to argue about `coding` (the basis's design D11
      names it as the next real later operation; `execution-lane-coding-worker.yml`
      is its grandfathered route on group 7). A fixture whose bytes say one thing
      and whose comment argues about another is worse than either.
      `tests/clearing/test_register_closure.py::test_deliberation_is_refused_by_name`
      re-targets with them, keeping its docstring's argument intact.
      **Assertion:** `clearing-register-member-unratified` and
      `clearing-unregistered-operation` both still FIRE, now on `coding`.
- [ ] 2.5 **Extend the verdict scan to the new return kind.** `check_operation_report`
      is dispatched by `kind == "xfactory_clearing_operation_report"`, so the
      `VERDICT_WORDS` name scan does NOT reach a return of a different kind today
      — measured, not assumed. Register the new schema's kind in `KIND_TO_SCHEMA`
      and route it through the verdict scan (extracting the shared check rather
      than copying it). **Assertion:** a negative fixture carrying a verdict-named
      member in a deliberation return is refused `clearing-report-carries-a-verdict`.
- [ ] 2.6 **Prove each frozen copy fails ALONE.** Before the slice is called done,
      edit exactly one of the four in 2.3 and confirm the other three go red, one
      at a time. Four chances to move three and miss one is the failure mode
      (design D12); a copy that never went red is a copy nobody tested.
- [ ] 2.7 **`examples/dispatch-record-refused.example.yaml` follows the fixture
      re-point** (design D8): its whole subject is a refused CLAIM of
      `deliberation`, which after admission documents a refusal that can no longer
      happen. `tests/clearing/test_dispatch_record.py::test_a_refusal_records_what_was_asked_for`
      asserts the claimed value literally and moves in the same commit.
- [ ] 2.8 **`contracts/clearing/README.md`**: the register section stops saying
      "exactly one member" and stops saying `deliberation` is deliberately
      absent; the shape table gains the return schema; the honest-limit paragraph
      is retained verbatim in substance and extended to name the gate's grep as a
      fourth copy.
- [ ] 2.9 **Green run of `python3 -m pytest tests/clearing -q`** and of
      `python3 scripts/validate-clearing-dispatch.py .` with the packaged corpus
      proving every closed refusal code still red-proven.

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
