# Tasks: clean-doc-health-floor

Every read-back below was measured on 2026-08-28 in a fresh worktree off
`origin/main` at `6612d323`, and re-measured after each slice rather than
predicted from the one before.

## 0. Baseline

- [x] 0.1 Record the floor before anything moves.
      **DONE.** `python3 scripts/doc-health.py --single-repo .` —
      **5 critical, 11 error, 41 warning, 11 info**, 0 new regressions.
      By family: `status-validity` 4 error, `record-immutability` 5 critical,
      `location-conformance` 3 error, `ideation-routing` 4 error,
      `staged-topic-template` 19 warning.
- [x] 0.2 Record the test baseline under `set -o pipefail`.
      **DONE.** `python3 -m pytest tests/doc-health -q` —
      **1249 passed, 0 failed**, 7 warnings, 182.16s. Exit 0 read from
      `$?` rather than from the tail of a pipe.
- [x] 0.3 Collision-check every capability an ADDED or MODIFIED choice could
      touch, against the active set.
      **DONE — NO COLLISION.** Three active changes carry deltas on the two
      capabilities in question: `add-nightly-dashboard-refresh` (doc-health,
      7 ADDED — the refresh lane), `add-unclassified-finding-class`
      (doc-health, 1 ADDED — "A modified-block-currency finding its own class
      map cannot place is itself a finding") and `add-ideation-intent-plane`
      (document-lifecycle, 1 ADDED — "Gates happen on main"). **All three are
      ADDED-only**, none names `Proposal supporting-document integrity
      checks`, and this packet's only delta is a MODIFIED on that one
      requirement. No requirement name is claimed twice.
- [x] 0.4 Parse contract-bundle membership for every touched path.
      **DONE — NO BUNDLE OWED.** All 48 `contracts/releases/*.digests.yaml`
      inventories grepped for each path. Zero hits for the two pilot READMEs
      (no inventory carries ANY `domain-ontology` path), for
      `docs/notebooklm-sync-open-item.md`, for `scripts/doc_health/corpus.py`,
      `scripts/doc_health/families.py` or `tests/doc-health/test_families.py`
      (no inventory carries any `doc_health` path). The inventories are
      confined to `contracts/**`, `scripts/hermes_runtime_validation/**` and
      three named files. No schema moves, no digest set changes, no release
      tag owed.

## 1. W1 — the four status backfills

- [x] 1.1 `contracts/domain-ontology/examples/pilots/codex/README.md` →
      `Status: draft`.
      **DONE.** One line plus one blank separator, placed after the `# …
      (DRAFT)` title and inside the 15-real-line header window
      `corpus.parse_status` scans. The document titles itself `(DRAFT)` and
      calls itself a "Starter-seeded draft package", so the value is read off
      the record.
- [x] 1.2 `contracts/domain-ontology/examples/pilots/medx/README.md` →
      `Status: draft`. **DONE**, identically.
- [x] 1.3 `docs/notebooklm-sync-open-item.md`: `Status: open (operational)` →
      `Status: draft`.
      **DONE — one line replaced, no other line touched.** The prose framing
      ("This is an operational open item, not a capability change") is
      deliberately KEPT: Brett's ruling maps the free-form value into the
      controlled taxonomy, it does not reclassify what the document is. The
      taxonomy stays closed — nothing was added to it to accommodate this file.
- [x] 1.4 `openspec/changes/archive/2026-08-25-fix-abandoned-session-cleanup-terminal-states/proposal.md`
      → `Status: ratified` plus a derived `Ratified:` citation, two lines at
      the head of the file.
      **DONE — AND THIS DEPARTS FROM THE RULED VALUE, flagged as OD-5 rather
      than done quietly.** All three candidates were run before any was
      written:

      | Header | `status-validity` | `ratified-provenance` | `promotion-fidelity` |
      | --- | --- | --- | --- |
      | `draft` (as ruled) | clears | 0 | **NEW ERROR** |
      | `ratified`, uncited | clears | **NEW CRITICAL** | 0 |
      | `ratified` + citation | clears | 0 | 0 |

      **The ruled `draft` manufactures an error against an innocent packet.**
      `promotion_fidelity.PRE_RATIFICATION` is `{brainstorm, staged, draft}`,
      and a packet declaring one of those has its deltas discounted as
      archived design evidence. Marking this one `draft` therefore drops its
      `ideation-dashboard` delta as the authority for
      `Staged-topic proposal commissioning`, the family falls back to
      `2026-08-01-add-workbench-branch-sessions`, and that packet reports as
      having failed to promote 1 of its 7 ratified scenarios. **Isolated by
      reverting this single edit and re-running: `promotion-fidelity` reads
      1 error with the `draft` backfill and 0 without it.**
      **The citation is DERIVED, not invented.**
      `openspec/specs/document-lifecycle/spec.md:39-53` names "its origin
      declaration" as the FIRST source a ratification citation may be derived
      from; this packet's `.openspec.yaml` carries `approved_by: Brett Heap`
      and `approved_on: 2026-08-25`. The line clears the record-citing
      spelling's three-way floor on all three axes — approver, date, and a
      resolvable record path — rather than the one it needs. It also matches
      what the precedent actually did (43 of 44 took `ratified` + a citation)
      and Brett's own 2026-08-26 ruling `4dc57a4d`, which corrected a
      different archived packet FROM `draft` TO `ratified`.
- [x] 1.5 Verify `record-immutability` does not newly fire on the archived
      path — structurally and empirically, not by assumption.
      **DONE, BOTH WAYS. Structurally:** `fam_record_immutability`
      (`scripts/doc_health/families.py:584`) iterates `ctx.docs`, which
      `corpus.iter_doc_paths` builds from
      `GOVERNED_ROOTS = ("contracts", "docs", "examples", "ideation",
      "templates")` (`corpus.py:39`) — `openspec/` is NOT a governed root, so
      no archived proposal can reach the family at all — and its first
      statement is `if doc.status != "record": continue`, which a `draft`
      header fails a second time. It never reads `Kind:`. **Empirically:** the
      family reports 5 criticals before this edit and 5 after, the same five
      paths. This is also why the 44 backfills of 2026-08-23 needed no
      allowlist, no baseline entry and no disposition — stated in that
      packet's own words at `proposal.md:18-22` and proven at
      `tasks.md:1870-1874`.
- [x] 1.6 Verify the 5C.3 precedent at the archive before editing an archive
      path, as the commission required.
      **DONE — AND THE COMMISSION'S PREMISE IS CORRECTED IN THREE PLACES**,
      recorded in `proposal.md` § What was measured rather than smoothed over.
      (a) `5C.3` is the STOP-AND-REPORT guard rail (`tasks.md:1948-1956`), not
      the authorization; `OQ-6` (`proposal.md:511-556`) authorized the
      campaign. (b) The count is **44** archived proposals, not 46; 46 was the
      `status-validity` ERROR census before the slice (44 archived + 2
      active). (c) The value was `ratified` + a citation for **43** of them and
      `draft` for exactly **ONE**. Confirmed against the tree: of 112 archived
      proposals today, 110 read `ratified`, 1 reads `draft`, 1 reads nothing —
      and that last is this file. **The operative precedent is therefore the
      one-document ruling at `tasks.md:1768-1791`**, plus the two
      overlay-boundary stragglers tabulated at `tasks.md:2164-2166`, plus the
      promoted scenario `A record cannot support a derived header`
      (`openspec/specs/document-lifecycle/spec.md:75-79`). Three instances,
      one canon form, all on all fours with this case.
- [x] 1.7 Re-measure the four families W1 can touch.
      **DONE — `status-validity` 4 error → 0 error; `ratified-provenance`
      0 → 0; `promotion-fidelity` 0 → 0; `record-immutability` 5 critical →
      5 critical.** No family moved except the one this slice targets.

## 2. W3 — location-conformance exempts archived citations

- [x] 2.1 Add `corpus.active_change_ids(repo_path)`.
      **DONE** (`scripts/doc_health/corpus.py`). A SIBLING of `change_ids`,
      mirroring its active loop only, with a docstring stating why the two
      sets must stay distinct: the union answers "does this id name a change
      that ever existed", which `ratified-provenance` needs and must keep; the
      sibling answers "can an act still be performed against this change".
      **`change_ids` is not touched.**
- [x] 2.2 Read the active set in the staged-exit arm.
      **DONE** (`scripts/doc_health/families.py`). Three lines: a per-repo map
      built from `ctx.repo_paths` at the top of `fam_location_conformance`,
      and `ids = active_ids.get(...)` in place of
      `ids = ctx.change_ids.get(...)`. No `Context`, `runner.py` or
      `conftest.py` change was needed — see `proposal.md` OD-3 for why that
      was chosen over threading a new field. The brainstorm arm, the
      stray-staged arm, both support walks and the canonical-specs check are
      untouched.
- [x] 2.3 Add the two fixture regressions, both ways.
      **DONE** (`tests/doc-health/test_families.py`), on the `tmp_path` idiom
      this suite uses for every citation-arm test, with the repo named
      `alpha` and the five-line `make_ctx` ritual.
      `test_staged_citation_of_an_archived_proposal_is_silent` builds the
      archived packet in the real `2026-07-09-change-a` date-prefixed shape —
      so the exemption is proven against the `YYYY-MM-DD-` strip branch that
      actually matched before the fix — asserts NO finding, asserts the union
      still resolves the id (proving the ARM stopped reading it, not that the
      id stopped existing), then **mutates and re-asserts**: it adds the live
      active packet and requires the finding to land again unchanged, which is
      this suite's "the exemption is not blindness" pairing.
      `test_staged_citation_prefers_the_active_proposal_over_an_archived_one`
      names the archived change `aaa-change` and the active one `zzz-change`
      so the archived id would win on sort order, and pins that the finding
      reports the ACTIVE one. It also pins the action line verbatim, under the
      one-verbatim-pin-per-family convention.
- [x] 2.4 Run the family suite.
      **DONE — `python3 -m pytest tests/doc-health/test_families.py -q`:
      35 passed** (33 before). No existing test changed; the five pre-existing
      `location-conformance` tests pass untouched because each already builds
      its `openspec/changes/` tree on disk and sets `ctx.repo_paths`.
- [x] 2.5 Re-measure `location-conformance` on the live corpus, and record
      what did NOT move.
      **DONE — 3 error before, 3 error AFTER. The count does not move, and
      that is the fix working.** The forcing document cites TWO changes:
      `implement-avatar-client-lab` (ARCHIVED 2026-08-04) and
      `qualify-avatar-live-voice` (ACTIVE). `_staged_exit_changes` returns
      sorted ids and the finding reports `cited[0]`, so the archived id won on
      alphabetical order and HID the performable remedy behind an impossible
      one. The row is now re-pointed —
      `staged material already cites proposal qualify-avatar-live-voice` —
      and stays an error, correctly, because that move CAN be performed.
      **This corrects the commission's stated expectation that the row would
      clear**, and is recorded in `proposal.md` § What was measured as the
      most important number in the packet.
- [x] 2.6 Confirm no CONTESTED finding loses its match key.
      **DONE.** `Finding.match_key()` is `(family, repo, path)`
      (`scripts/doc_health/__init__.py:173-175`) — rule text is not part of
      it. The avatar row keeps family, repo and path across the change, so
      `report.uncited_resolutions` sees it present in the current report and
      manufactures nothing. **No disposition is owed by this packet and none
      is added**, which was verified rather than assumed because
      `location-conformance` is in the CONTESTED resolution class
      (`families.py:94`) and a vanishing contested finding becomes an
      `uncited-resolution` ERROR.
- [x] 2.7 Confirm the other two rows are untouched.
      **DONE.** `openxwallet-neutral-home` cites
      `create-ledgerxwallet-overlay-boundary` (ACTIVE) and
      `worker-enrollment-broker` cites `add-worker-enrollment-broker`
      (ACTIVE). Both rows are byte-identical before and after. The
      openxwallet row is another session's in-flight work and was not touched;
      the fix leaving both firing is the live-corpus half of the
      "not blindness" proof.

## 3. Canon

- [x] 3.1 MODIFIED delta on `doc-health`.
      **DONE** — `specs/doc-health/spec.md`, one MODIFIED requirement,
      `Proposal supporting-document integrity checks`. The promoted text PINS
      the defect twice ("active or archived" in the body sentence and again in
      the scenario WHEN), so an ADDED clarification would have left canon
      contradicting the code. The block restates the requirement in full per
      the MODIFIED-block currency rule, keeps all four original scenarios
      unedited, narrows the two pinned phrases, and adds two scenarios pinning
      the new behaviour on both sides (archived-only → silent; both kinds →
      reported against the active one).
- [x] 3.2 Register the archived-record edit.
      **DONE** — one appended addendum section in
      `docs/archive-record-discrepancies.md`, following the append discipline
      every prior archived-record correction there used. **The
      `record-immutability` cost is stated rather than discovered:** that file
      carries `Status: record`, so editing it trips the family — and that
      critical was ALREADY STANDING for that document and is unchanged by this
      entry, verified by running the family either side of the edit rather
      than assumed. Same verification `govern-openspec-corpus-membership`
      performed on the same file (`tasks.md:1700-1712`).
- [x] 3.3 README active-changes entry. **DONE** — one entry at the head of the
      Active changes block, which is ordered newest-first.

## 4. Gates

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate clean-doc-health-floor
      --strict` — **valid**.
- [x] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` —
      **77 passed, 0 failed (77 items)**, grown by exactly one for this
      packet joining the active set (76 before).
- [x] 4.3 `python3 -m pytest tests/doc-health -q` under `set -o pipefail`,
      exit read from `$?` rather than from the tail of a pipe —
      **1251 passed, 0 failed**, 159.03s, **EXIT=0**. Baseline was 1249;
      grown by exactly the two regression tests task 2.3 adds, and by nothing
      else.
- [x] 4.4 Full doc-health single-repo run, before vs after, whole-run counts.
      **DONE — 5 critical / 11 error / 41 warning / 11 info → 5 critical /
      7 error / 41 warning / 12 info.** Four errors cleared, all four from
      `status-validity`; **none introduced**; criticals and warnings unmoved;
      `location-conformance` still at 3 for the reason task 2.5 records. The
      one added INFO is `modified-block-currency` reporting this packet's own
      MODIFIED block as diverging from canon in exactly 2 of 10 units — the
      two "active or archived" phrases task 3.1 narrows on purpose. That arm
      cannot distinguish a deliberate rewording from drift and says so in the
      finding text; the line is the check working and the audit trail for the
      narrowing, and it retires when this packet archives and the block is
      promoted.
- [x] 4.5 Discharge the `modified-block-currency` SELF-GATE, which this
      packet falls due by existing.
      **DONE.** `tests/doc-health/test_modified_block_currency_self_gate.py`
      compares its named subject set with `==` rather than `<=`, deliberately,
      so that a newly lossy MODIFIED block cannot land unreported — which
      means ANY new MODIFIED block in the active set fails it until named. It
      failed exactly as designed, naming the unnamed subject
      `('clean-doc-health-floor', 'doc-health', 'Proposal supporting-document
      integrity checks')` and printing its own remedy. One row added to
      `_LEDGER_SUBJECTS`, in this commit, recording which subject moved and
      why: a deliberate narrowing, the two uncarried units named, and the
      retirement condition stated. **`pytest
      tests/doc-health/test_modified_block_currency_self_gate.py` — 15
      passed.**
- [ ] 4.6 Merge-plus-green on main: both required checks green on the
      proposing pull request, read back from the check-runs API rather than
      off the pull request page. **OWED AT REALIZATION** — this packet ships
      ACTIVE and archives only after the merge.

## 5. Named follow-ups, out of scope here

- [ ] 5.1 **The staged-exit arm still reports only `cited[0]`.** A document
      citing two ACTIVE changes names one of two possible destinations.
      Proposal § Open Questions Q1 recommends leaving it: it changes the
      finding COUNT rather than its content and needs its own cross-repository
      before/after.
- [ ] 5.2 **A staged fragment whose every cited exit has archived is now
      reported by nothing.** The silence is right for this family, and the
      lifecycle condition is real. Q2 recommends recording the gap rather than
      inventing a home for it inside a location-conformance fix;
      `staged-candidate-aging` is the plausible owner.
- [x] 5.3 **The third ruled workstream ships separately** as
      `declare-generated-projection-status` (OD-1), and owes a disposition
      entry in the AGGREGATION repository that this packet does not.
      **DISCHARGED AS A DECISION 2026-08-28**: Brett ruled that BOTH pull
      requests merge on green, so the split stands and the sibling lands on
      its own gate. **The aggregation disposition entry is assigned to the
      ORCHESTRATING SESSION as part of the merge sequence** and is not owed by
      either authoring session — recorded here so a later reader does not go
      looking for it in this packet's realization.

## 6. The veto window

- [x] 6.1 Record the rulings of 2026-08-28.
      **DONE.** By a multi-choice put to Brett by the orchestrating session
      and relayed the same day. Selections reaching this packet: **OD-5 KEEP
      `ratified` plus the derived citation** — the measured deviation from the
      ruled `draft` APPROVED as taken — and **both pull requests merge on
      green**, which confirms OD-1's split in the form that matters. On OD-5
      he took the packet's own recommendation, so **the clearance moved
      nothing**: not one byte of the archived record's header changed.
      **OD-2, OD-3 and OD-4 were NOT put to him and are NOT covered** — they
      stand as authored and remain flagged. No verbatim wording reached this
      session, so none is quoted; approver, date, mechanism and selections are
      recorded instead. The original flagged text is KEPT as marked history in
      `proposal.md` § Orchestrator decisions rather than rewritten.
- [x] 6.2 Confirm the ruling changed no artifact.
      **DONE — measured, not assumed.** `git diff` over the ruling commit
      touches `proposal.md` and `tasks.md` only. The archived record's header,
      the register addendum, the three live backfills, `corpus.py`,
      `families.py` and both test files are byte-identical to what the ruling
      approved.
- [ ] 6.3 **BEFORE ARCHIVE, THIS PROPOSAL'S OWN HEADER MUST MOVE OFF
      `Status: draft` — AND THIS PACKET IS THE REASON THAT MATTERS.** The
      header is deliberately left at `draft` here: the 2026-08-28 ruling
      approved OD-5 and directed the merge, and this session will not spell
      that as a ratification act Brett did not state, which is the same
      refusal § 1.4 makes about somebody else's archived record. But the
      header cannot STAY `draft` through archiving, and the defect is the one
      W1 measured: `promotion_fidelity.PRE_RATIFICATION` is
      `{brainstorm, staged, draft}`, so an archived proposal reading `draft`
      has its deltas discounted as archived design evidence rather than
      promoted canon — exactly what would have happened to an innocent third
      packet in § 1.4, here aimed at this packet's own `doc-health` MODIFIED
      block. Measured against the tree: **110 of 112 archived proposals read
      `ratified`.** Whoever performs the archive owes the header and its
      citation, derived from the ruling record. Named here rather than
      discovered later.
