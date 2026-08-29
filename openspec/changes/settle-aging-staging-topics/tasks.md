# Tasks: settle-aging-staging-topics

Status: draft
Kind: tasks
Draft slice of: openspec/changes/settle-aging-staging-topics/proposal.md

THE GATES THAT ARE NOT OURS: **Omnigent-Install PR #40** and **OpsxFactory
`add-worker-enrollment-broker-service` tasks 8.1/8.2** are named by this
packet and performed by nobody in it. Everything below is authoring and
measurement.

## 1. Ratification

- [x] 1.1 RATIFIED 2026-08-28 by Brett — the four bulk rulings R1–R4 recorded
      verbatim in `.openspec.yaml`, given as answers to a read-only triage
      survey's multi-choice questions over the fourteen aging staging topics.
- [ ] 1.2 THE FIVE ORCHESTRATOR DECISIONS ARE FLAGGED FOR VETO and this box
      stays open until Brett has read § Orchestrator Decisions. OD-1 (the
      exit record instead of `superseded` for `dashboard-repo-selector`) is
      the one that departs visibly from R1's wording and is the one to read
      first. OD-2 (`Exit taken:` is not a status), OD-3 (per-section index
      reading), OD-4 (MODIFIED not ADDED), OD-5 (URL successor citations).
- [ ] 1.3 IF OD-1 IS VETOED: `ideation/staging/dashboard-repo-selector/
      dashboard-repo-selector.md` takes `Status: superseded` with a
      `Superseded by:` line naming
      `openspec/changes/archive/2026-08-01-add-dashboard-repo-selector`, and
      the `Exit taken:` line is removed. The measured silencing is identical
      — the topic goes quiet either way — so § Impact's numbers do not move.

## 2. The family fix (`scripts/doc_health/families.py`)

- [x] 2.1 Four helpers above `fam_staged_candidate_aging`, with the reasoning
      block that explains why the arm reads more than a date:
      `_archived_change_ids(ctx)` (the union of `ctx.change_ids` across
      repositories MINUS the union of `corpus.active_change_ids`, so an id
      active anywhere is archived nowhere), `_exit_taken_lines(text)` (lines
      outside code fences whose body starts `Exit taken:`, matched on the RAW
      line because the change id is conventionally in backticks and
      `_strip_inline_code` would delete it), `_index_section(text, topic)`
      (the `## <topic>` detail section of a staging index), and
      `_topic_outcome(...)` (the two skip arms, returning the REASON so a
      test can distinguish them).
- [x] 2.2 The staged-topic arm `continue`s on a recorded outcome, before the
      age is computed. `docs_by_path` and the archived-id set are built once
      per run, outside the repository loop.
- [x] 2.3 The action line, corrected from the unperformable "progress the
      topic to a proposal or mark it deferred" to "progress the topic to a
      proposal, or record the outcome it already reached — the primary
      fragment superseded/retired, or an Exit taken: line naming the archived
      change".
- [x] 2.4 NOTHING ELSE IN THE FAMILY MOVES: the candidate-block arm, the
      supersedes arm and the draft-age arm are byte-identical, `FAMILIES` is
      unchanged, and `tests/doc-health/test_family_enumeration.py` passes
      without an edit — no family was added, so no enumeration numeral moves.

## 3. The regressions (`tests/doc-health/`)

- [x] 3.1 `fixtures/staged-topic-outcomes/alpha/` — SIX topics at ONE age
      (130 days at the suite's `AS_OF`), so the only thing separating them is
      the outcome each records: `closed-topic` (`superseded`),
      `retired-topic` (`retired`), `exited-topic` (`Exit taken:` in the
      staging INDEX naming the archived
      `2026-01-05-add-exited-thing`), `inflight-topic` (`Exit taken:` naming
      the ACTIVE `add-live-thing`), `fenced-topic` (the record shown inside a
      code fence, as an example), `stale-topic` (nothing at all). Plus the
      two change folders that make one id archived and the other active.
- [x] 3.2 `test_a_recorded_outcome_stops_a_staged_topic_ageing` — the three
      that stay silent is the regression; `fenced-topic`, `inflight-topic`
      and `stale-topic` still firing is the positive control that the family
      did not simply go quiet.
- [x] 3.3 `test_the_three_silenced_topics_are_silenced_for_their_own_reason`
      — each skip arm asserted by NAME, so one arm cannot cover another's
      failure, plus the archived/active membership of the two fixture ids.
- [x] 3.4 `test_an_index_exit_record_binds_to_its_own_topic_section` — a
      neighbouring topic's record must not silence this one; asserted in both
      directions over the same index document.
- [x] 3.5 The action-line PIN in `test_staged_candidate_aging` moved by name
      with the comment recording WHY the old line was wrong. That pin is the
      guard `add-unclassified-finding-class` installed for exactly this: an
      action line is operator guidance nothing else notices changing.
- [x] 3.6 SUITE: `python3 -m pytest tests/doc-health -q` → **1281 passed**,
      0 failed (1278 before; the three new tests are the difference). Run
      under `set -o pipefail`.

## 4. The corpus edits

- [x] 4.1 R1 — four fragments take `Status: superseded` + `Superseded by:` +
      a `## Outcome (recorded 2026-08-28)` section carrying the verified
      archive table: `client-layer-tuning`,
      `codexfactory-domain-hermes-content`, `layer-content-materialization`,
      `medxfactory-domain-hermes-content`. `github-administration-plane` was
      NOT edited — it was already `superseded` and is silenced by task 2.2
      alone, which is the proof that the defect was in the reading.
- [x] 4.2 R1/OD-1 — `dashboard-repo-selector` takes `Exit taken:` in its
      fragment header AND an `- Exit taken:` bullet in its INDEX detail
      section; open questions 7–9 marked CLOSED with Brett's 2026-07-26
      rulings and the archived packet's `Ratified:` line as the citation; the
      exit-2 gate (open question 3) written into the exit path.
- [x] 4.3 R2 — `worker-host-app` and `context-compression-runtime` each gain
      a `## Deferral with a named gate (recorded 2026-08-28)` section naming
      the three-link chain, each stating in its own text that the deferral is
      a schedule and does not stop the topic ageing. The
      `worker-enrollment-broker` supporting-docs MOVE is NOT performed here.
- [x] 4.4 R4 — the same section for `proposal-origin-contract`,
      `layer-vocabulary-machine-migration` and `ideation-action-plane`'s
      `drive-membrane.md` (fragment 2).
- [x] 4.5 R3 — `ideation/staging/INDEX.md` only: one readiness correction on
      `subject-establishment` (its Ledgerx gate CLEARED 2026-08-04) with
      DTN-017's stale `staged` row FLAGGED and not fixed. NO edit to either
      R3 topic's documents, and NO edit at all to
      `client-credential-escrow-registry`, whose row was checked and is still
      true.
- [x] 4.6 R4 bookkeeping — `ideation-action-plane`'s row reconciled (exit 1
      is the ACTIVE `add-ideation-intent-plane` at 13/17 tasks, not merely
      "raised") and `medxfactory-domain-hermes-content`'s row corrected
      (change B archived 2026-07-30; the row said otherwise).
- [x] 4.7 A section placement rule observed throughout: no deferral text sits
      inside a `## Exit` heading, because `_staged_exit_changes` reads that
      section and an ACTIVE change id named there would raise a false
      `location-conformance` error. `worker-host-app.md` and
      `layer-vocabulary-machine-migration.md` are the two fragments whose
      heading matches exactly; both take the new section BEFORE it. Verified
      by measurement: `location-conformance` stays at 3.

## 5. Evidence

- [x] 5.1 THE MEASUREMENT THAT ISOLATES THE RULE. Every edit in § 4 writes
      into a topic folder and resets its git last-commit date, buying thirty
      days of silence the rule did not cause. So both trees were measured at
      a COMMON future as-of, by which date all 33 topics are old enough to
      fire either way: `python3 scripts/doc-health.py --single-repo . --family
      staged-candidate-aging --as-of 2026-12-31`, run once in a detached
      worktree at `origin/main` and once here. **33 → 27**, and the six that
      go quiet are exactly `github-administration-plane`,
      `client-layer-tuning`, `codexfactory-domain-hermes-content`,
      `layer-content-materialization`, `medxfactory-domain-hermes-content`
      and `dashboard-repo-selector`.
- [x] 5.2 THE RUN AS IT STANDS TODAY, RE-MEASURED ON THE MERGED HEAD after
      main advanced sixteen commits and § 4's edits were committed. Both
      columns moved, neither because of this change, and this is the number
      task 7.1's archive gate is read against. Single-repo, default as-of:
      `4 critical, 7 error, 41 warning, 13 info` → `4 critical, 7 error, 30
      warning, 13 info`. Per family, before → after: `staged-candidate-aging`
      15 → 4 and EVERY OTHER FAMILY UNCHANGED — `staged-topic-template` 27,
      `modified-block-currency` 9, `record-immutability` 4, `tag-hygiene` 4,
      `location-conformance` 3, `ideation-routing` 2, `document-catalog` 1.
      THE FIRST READING OF THIS TASK said `5 critical … 41 warning, 12 info` →
      `… 35 warning, 12 info` with `staged-candidate-aging` 15 → 9; it is
      superseded on two independent counts, each named at § Impact — the
      baseline moved with `declare-generated-projection-status`'s landing
      (`record-immutability` 5 → 4) and the after column moved because the
      mtime reset 5.3 predicted arrived on the merge rather than after it.
      The invariant the task exists to state is untouched: no family but
      `staged-candidate-aging` moves in either direction.
- [x] 5.3 THE HONEST CAVEAT, WRITTEN AS A PREDICTION AND NOW OBSERVED. It said
      the five staged-topic warnings on topics § 4 WROTE INTO would fall
      silent by MTIME RESET rather than by rule, leaving only
      `client-credential-escrow-registry`, `subject-establishment` and
      `worker-enrollment-broker` warning continuously. The merged-head run
      reads exactly those three and no others, so the caveat was right and
      the reset landed one step earlier than described — on the commit, not
      on the merge. The five return 2026-09-27 still deferred.
      **Deferrals do not silence, and this change does not pretend
      otherwise.**
- [x] 5.4 EVERY ARCHIVE CITED WAS RESOLVED AT ITS OWN TREE on 2026-08-28, not
      inferred from the register: openxFactory (3 packets), codexFactory (3),
      MedxFactory (2), OpsxFactory (1), hermes-install (2), LedgerxFactory
      (1). The MedxFactory change-B packet and the three LedgerxFactory
      2026-08-04 packets are the two the register was stale about.
- [x] 5.5 THE CROSS-REPOSITORY GATE FACTS, resolved live: broker repository
      PR #1 MERGED 2026-07-27T00:09:13Z and PR #2 MERGED 2026-07-28T01:33:37Z;
      Omnigent-Install PR #40 created 2026-07-28T04:33:26Z, state OPEN, not a
      draft; OpsxFactory `add-worker-enrollment-broker-service` tasks 8.1 and
      8.2 both unticked in the live tree.
- [x] 5.6 THE `contract-v2.0` FACT AND ITS CORRECTION. The commission relayed
      "contract-v2.0 fired 2026-08-28"; the tag and its commit both date
      **2026-08-27**. The substance holds and is measured, not assumed:
      `git diff --stat contract-v1.47 contract-v2.0 -- contracts/hermes-runtime/
      contracts/schemas/` reports NO files changed, so the major moved no
      hermes-runtime schema and the frozen `customer|client|domain` spellings
      had nothing to ride. Recorded in the topic fragment.
- [x] 5.7 COLLISION CHECK on the `doc-health` capability, as the standing
      template requires. Of the active changes carrying a `doc-health` delta:
      `add-nightly-dashboard-refresh` is ADDED-only (7 requirements),
      `fix-pin-value-boundary-and-sentinel-split` is ADDED-only (1), and
      `clean-doc-health-floor` (merged as PR #465, ACTIVE until archived)
      holds ONE MODIFIED, on `Proposal supporting-document integrity checks`.
      This packet's MODIFIED is on `Aging threshold defaults`. No two MODIFIED
      blocks meet, so no coordination by ADDED text was needed.
- [x] 5.8 VALIDATION: `OPENSPEC_TELEMETRY=0 openspec validate
      settle-aging-staging-topics --strict` and `--all --strict`, both from
      the openxFactory root. Numbers in the PR body.

## 6. FOR THE ORCHESTRATING SESSION — the aggregation `HANDOFFS.md` row

**NOT EDITED HERE, DELIBERATELY.** `/home/brett/projects/xFactory/HANDOFFS.md`
lives in the shared aggregation checkout, which is dirty with other sessions'
work; this packet touches no file outside `openxFactory/`. The row is the one
for `worker-host-and-enrollment-broker-handoff.md` (line 29 at the time of
writing). Replace this EXACT trailing substring of its last cell —

```
phase-3 change authored Omnigent-Install `66d53f7c` (new `worker_enrollment` step ordered FIRST so renewal runs even when runner_services is a no-op); **broker service BUILT — PR #1 open at Brett's merge gate** (236 tests, validator 0/0, 22 panel findings fixed; repo secrets OPENXFACTORY_APP_* owed for CI). Next: Brett merges PR #1 → implement phase 3 → Brett's 8.1/8.2 deploy gates → acceptance 5.1 volunteer end-to-end on Brett's machine (doubles as the NT SERVICE fact-check) |
```

— with:

```
phase-3 change authored Omnigent-Install `66d53f7c` (new `worker_enrollment` step ordered FIRST so renewal runs even when runner_services is a no-op); **broker service BUILT AND MERGED — PR #1 merged 2026-07-27, PR #2 (secret-scan + container-build-scan unbricking) merged 2026-07-28** (236 tests, validator 0/0, 22 panel findings fixed; repo secrets OPENXFACTORY_APP_* owed for CI). **THE LIVE GATE IS NOW Omnigent-Install PR #40** — "Worker Host App phase 3: enrollment-broker client, leases, fail-closed floor", raised 2026-07-28 and STILL OPEN at 2026-08-28 (not a draft), awaiting Brett's merge. Next: merge PR #40 → Brett's 8.1/8.2 deploy gates in OpsxFactory `add-worker-enrollment-broker-service` (8.1 hosting target = publish the concrete Azure names in a ratified naming doc; 8.2 deployment credentials = the deploy identity behind a required-reviewer Actions Environment; BOTH still unticked) → acceptance 5.1 volunteer end-to-end on Brett's machine (doubles as the NT SERVICE fact-check) |
```

- [ ] 6.1 The orchestrating session lands the row above via its temp-index
      route (`read-tree` / `cacheinfo` / `commit-tree`, `push sha:main`), so
      the shared checkout's uncommitted work is not swept in.

## 7. Archive

- [ ] 7.1 ARCHIVE AFTER REALIZATION AND AFTER THE MERGE. The realization rides
      this packet (the family fix, its fixtures and its tests are here), so
      the archive gate is merge-plus-green on main: the doc-health suite
      green, `openspec validate --all --strict` green, and a single-repo run
      whose counts match § 5.2 exactly. The change ships ACTIVE.

## 8. Open — recorded, not fixed

- [ ] 8.1 AN EXIT RECORD DOES NOT EXPIRE. See the proposal's open question 1.
- [ ] 8.2 `staged-topic-template` READS NO STATUS EITHER, and now emits five
      findings against `superseded` fragments. Its own change; out of scope
      here so this packet moves one family.
- [ ] 8.3 THREE REPOSITORIES WITH STAGED TOPICS KEEP NO STAGING INDEX
      (MedxFactory 4 topics, OpsxFactory 7, LedgerxFactory 6). Only the
      fragment-header form of the record reaches them, which is why that form
      exists.
- [ ] 8.4 DTN-017 STILL READS `staged`. Flagged, not fixed, per R3 — the
      agent filing `subject-establishment` owns that row.
- [ ] 8.5 THE `worker-enrollment-broker` SUPPORTING-DOCS MOVE is a separate
      act dispatched after this lands; it collides on `INDEX.md` and
      `ideation/cross-reference.md`.
