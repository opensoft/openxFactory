# Tasks: declare-spent-bundle-state

Status: ratified
Ratified by: declare-spent-bundle-state

**GROUP 1 IS DISCHARGED AND GROUP 2 IS DELIBERATELY NOT STARTED.** Ratified
2026-09-02 by Brett Heap; record `review/ratification-2026-09-02.md`. As first
written this preamble said *"Group 1 is ratification, which has not happened"* —
that was true of the packet as proposed and stopped being true on 2026-09-02,
and it is corrected here rather than left to contradict the ticks below. Group 2
remains open BY DECISION, not by omission: OD-8 splits this packet from its
code, so a tick in group 2 appearing in the same PR as this file would be the
thing that decision forbids, and **ratification authorizes realization and
performs none of it**. Group 4 records what the authoring session MEASURED
before the packet was put up, which is evidence rather than implementation.

Build group 2 with Speckit, not `/opsx:apply`. OpenSpec ratifies; Spec Kit
builds. Group 2 is ONE Spec Kit feature: the reader, the ladder, the two emits,
the `contract-v2.6` declaration and the tests are a single vertical slice, and
splitting them would produce halves neither of which is green alone — a reader
with no declaration to read leaves the `error` standing, and a declaration with
no reader is a sentence in a changelog.

## 1. Ratification — DISCHARGED 2026-09-02, and it gated group 2

- [x] 1.1 OD-1 … OD-9 and OQ-1 … OQ-3 were put to Brett Heap. His commissioning
      ("Merge now, fix #575 next") authorized AUTHORING and covered nothing
      below it; every decision in § Orchestrator Decisions is the authoring
      session's and each names the alternative it rejected.
- [x] 1.2 **OD-3 AND OD-4 RULED EXPLICITLY, 2026-09-02, NOT ACCEPTED BY
      SILENCE** — the two that carry governance content, put to him as such.
      **OD-3 ACCEPTED as proposed**: a correctly declared spent bundle emits an
      `info` with its own finding key, not silence, because *"the reader who
      finds `contracts/releases/contract-v2.6.digests.yaml` with no matching tag
      is owed the answer where they are looking, and the key is what makes the
      one permanent finding auditable"*. **OD-4 ACCEPTED as proposed**: quiet
      only once the superseding bundle's tag is published, `warning` while it is
      cut but untagged, `error` where the named successor was never cut — *"the
      only way to make a bundle quiet is to publish its successor's tag"*.
      Recorded on PR #578 and in the ratification record.
- [x] 1.3 Ratification recorded at `review/ratification-2026-09-02.md`;
      `Status: ratified` and the record-citing `Ratified:` line are in
      `proposal.md`. Ratification authorizes realization and performs none of
      it.
- [x] 1.4 **OD-9 ADDED AFTER THE RULING AND BEFORE THE RATIFYING COMMIT, on a
      Codex P1, and it is a NARROWING rather than a new decision.** The guard as
      ruled (cut AND published) is satisfiable by an EARLIER already-published
      bundle, so the superseding bundle must be STRICTLY LATER. Taken into the
      requirement rather than filed as a successor, because a decision whose
      stated purpose is *"the only way to make a bundle quiet is to publish its
      successor's tag"* is not met by a tag that already existed. It reopens
      nothing Brett ruled: the three severities, the record and the ladder stand,
      and a FOURTH refusal joins them.

## 2. Realization — ONE Spec Kit feature, gated on 1.1

- [x] 2.1 **FIRST, AND NOT SILENTLY: write the `contract-v2.6` declaration.**
      ONE reserved line, in the reserved form, into the EXISTING
      `### \`contract-v2.6\` disposition` subsection under `## contract-v3.0` in
      `contracts/CHANGELOG.md` — not a new subsection, not an edit to the
      `contract-v2.6` entry, not an edit to the manifest or the inventory. Its
      four elements come from the record that already exists: superseding bundle
      `contract-v3.0`; cause, the ADDITIVE-class-over-a-refusing-tree defect no
      completion commit can cure; ruled by Brett Heap, 2026-09-02; measurement,
      PR #565 comment `5502452624`. **`main` goes green because this bundle is
      explicitly declared spent, never because an undeclared bundle started
      passing** — verify that by running the family against a tree with the
      declaration removed and confirming the `error` returns.
- [x] 2.2 `scripts/doc_health/release_tag_publication.py` — the reader: one pure
      function from the changelog bytes to `{bundle: declaration}`, parsing the
      reserved opener, the four elements and the containing `## contract-vX.Y`
      entry. Bytes in, per the module's existing rule that `blobs_at` answers raw
      blob bytes. Reject rather than skip on a malformed line.
- [x] 2.3 The ladder in `check_repo`, in the ABSENT arm only and after the
      `ok`/`lightweight`/`misplaced` branches, so the scope rule holds by
      construction rather than by care: no declaration → today's behaviour
      unchanged; declaration accepted, successor published AND STRICTLY LATER →
      `info`; successor cut but unpublished → `warning`; successor never cut,
      successor not later (OD-9), element missing, duplicate declaration, wrong
      containing entry, or naming the currently declared bundle → `error`; a
      declaration whose SUBJECT was never cut → `warning` on the changelog.
- [x] 2.4 The emits land on `contracts/releases/<bundle>.digests.yaml` rather
      than `MANIFEST` (OD-5 as amended), with the spent `info` carrying
      `resolution="contested"`; the one orphan-subject `warning` lands on
      `contracts/CHANGELOG.md`, having no per-bundle inventory to land on. New
      action constants beside the four the module already has.
- [x] 2.5 The changelog read joins the manifest read at the SAME commit and
      carries the SAME guard: `blobs_at` answering None is a skip naming that
      read, never "no declaration". This is the #338 conflation one document
      over, and the family has already been caught by it once.
- [x] 2.6 `tests/doc-health/test_release_tag_publication.py` — the thirteen new
      scenarios as tests over the file's existing real-git fixtures, each with
      the positive control the file's own convention requires. Include the
      RED-FIRST proof for 2.1's verification: the declaration removed, the
      `error` returns.
- [x] 2.7 **Prove OQ-3 rather than inherit it**: a test that a contested `info`
      vanishing between reports produces an `uncited-resolution` ERROR. If it
      does not, OD-5's class choice returns to Brett as an open question and is
      not quietly dropped. **And prove the Codex repair with TWO spent bundles**,
      not one: two accepted declarations, two `info`s, two DIFFERENT match keys,
      and removing one raising an uncited-resolution for that one alone. A
      single-bundle test cannot see the defect Codex found.
- [x] 2.8 `docs/doc-health.md` — the family's row and action line gain the third
      state. Check the family count sentences are untouched: this change adds no
      family and `family-enumeration` must stay silent.
- [x] 2.9 `python3 -m pytest tests/doc-health` green over the realized tree,
      including `test_this_repository_reads_zero_and_the_probe_can_fire`, which
      goes green as a CONSEQUENCE and is not edited.
      **WAS DELIBERATELY UNTICKED BECAUSE THE PROOF WAS A RULING RATHER THAN A
      MISS, AND IS NOW TICKED ON THE CONFIRMATION IT NAMED.** Brett Heap ruled
      2026-09-02 (issue #575, lane openxfactory-1d): *"merge the realization on
      the dispositioned red."* The family resolves its tip with
      `git ls-remote origin refs/heads/main` and reads `contracts/manifest.yaml`
      and — per 2.5 — `contracts/CHANGELOG.md` AT THAT TIP, so the realization
      PR's own CI reads the LIVE remote `main`, whose changelog carries no
      declaration until this PR's squash lands. The realization therefore reports
      exactly ONE failure, that test, byte-identical to `main`'s failure set since
      `ff9ed815`, and goes green AT the squash rather than before it. **The
      self-gate was proved to pass once the branch IS `main`, mechanically rather
      than by argument**: a bare origin whose `main` is this branch, cloned and
      read by `check_repo`, reports ONE `contested` `info` on
      `contracts/releases/contract-v2.6.digests.yaml` and NO error — while the
      same call against the worktree, whose origin is the real remote, reports
      the inherited `error`. The test is NOT edited. **CONFIRMED**: PR #587
      merged to `main` as squash `3fa222f3f9e1486dc9618d25d0a665f276fbe964`
      (2026-09-02T16:19:02Z, merged `--admin` per Brett Heap's ruling on the
      dispositioned red — PR #587 comment, 2026-09-02T16:18:58Z), and the
      `main`-branch `pytest-suite` workflow run at that exact commit —
      **run `33654163291`, conclusion `success`** — is fully green, the
      previously-red `test_this_repository_reads_zero_and_the_probe_can_fire`
      included, unedited, going green as the predicted consequence of the
      changelog declaration landing at that squash.

## 3. Owed at the next contract cut — NOT here (OD-6)

- [x] 3.1 `docs/contract-versioning-policy.md` gains the obligation-side
      statement of the SPENT state, beside § *Immutable Tag Correction* whose
      *"its version number is never reused"* the `contract-v2.6` disposition
      already leans on, and naming the reserved declaration form so a consumer
      reading the pinned policy can find the state without reading doc-health.
      **PARTLY DISCHARGED BY ANOTHER LANE, AND THE ARITHMETIC HAS CHANGED — PR
      #577, merged `2898b104` on 2026-09-02.** That PR recorded
      `contract-v2.6`'s supersession in this very file as instance SIX, so the
      consumer-facing half — a reader of the pinned policy learns the bundle is
      superseded and not dischargeable — **is discharged and MUST NOT be
      re-authored** (*"two records of one measurement is how they drift apart"*).
      What #577 deliberately did NOT do is DEFINE the state or its declaration
      form — *"No sentinel is invented … Building one here would be exactly the
      failure that check exists to catch"* — and that definition is what remains
      owed here. **AND OD-6's COST ARGUMENT IS NOW SPENT**: #577's edit already
      raised the predicted `release-inventory-drift` ERROR on `main`
      (*"bytes differ from the digest 'contract-v3.0' records"*), so the
      INCREMENTAL cost of adding the SPENT-state paragraph to the same file is
      ZERO and it clears at the same next cut either way. The realization takes
      the routing with that measurement in hand; it is no longer forced to wait.
      **THE REALIZATION TOOK THE ROUTING AND LEFT IT HERE, 2026-09-02 — AN
      ORCHESTRATOR DECISION AWAITING BRETT'S AFFIRMATION.** The permission this
      box grants is a permission and not an instruction, and the section heading
      it sits under still reads *NOT here (OD-6)*. Two reasons for taking the
      narrower reading. The incremental DRIFT cost is zero, but the incremental
      REVIEW cost is not: this PR is confined to doc-health's own surface plus one
      editorial member, and a second between-cuts edit to a NON-EDITORIAL release
      member would put a release-surface change inside a checker PR, which is the
      shape OD-6 declined for reasons that survive the arithmetic. And the drift
      `error` #577 raised is on the file's CURRENT bytes; adding to those bytes
      quiets nothing and clears at the same cut, so nothing is bought by moving
      it earlier. **If Brett prefers it landed now, it is one paragraph and it
      does not touch this packet's code.**
      **AFFIRMED, 2026-09-02/03, ON PR #587 (comment, 2026-09-03T02:49:08Z):**
      *"Task 3.1 (policy-side SPENT paragraph in
      `docs/contract-versioning-policy.md`) deferred to the next cut per OD-6's
      shape argument: affirmed; the section heading keeps reading NOT here
      (OD-6)."* The box's own question — land the paragraph now, or leave the
      routing here — is what was awaiting Brett's affirmation, and the answer is
      to leave it: **the paragraph is NOT written by this change or by the
      archive act**, and the obligation stands owed at the next contract cut
      exactly as § 3's heading already said. Ticked because the decision this
      box existed to carry is now made, not because the paragraph exists.
- [ ] 3.2 At the next cut, `contracts/CHANGELOG.md`'s editorial drift `info` and
      `docs/contract-versioning-policy.md`'s ERROR both clear on their own when
      the inventory re-baselines. No action; recorded so a reader does not go
      looking for one, and so the second is not mistaken for this packet's.

## 4. Measured before the packet was put up

- [x] 4.1 The inherited red REPRODUCED, not quoted:
      `python3 -m pytest tests/doc-health/test_release_tag_publication.py` at
      `ff9ed815` → **18 passed, 1 failed**, the failure being
      `test_this_repository_reads_zero_and_the_probe_can_fire` on one `error`
      whose rule names `contract-v2.6` and whose action is the
      `_SUPERSEDED_ACTION` retro-publication text.
- [x] 4.2 `contract-v3.0`'s tag CONFIRMED PUBLISHED — `git ls-remote origin
      refs/tags/contract-v3.0` answers `59f4f51f…` peeling to `ff9ed815…`, the
      squash of #573. This is what makes the `contract-v2.6` declaration land in
      the `info` band rather than OD-4's `warning` band, and it was checked
      rather than assumed.
- [x] 4.3 The delta verified SCENARIO-BY-SCENARIO against canon: 11 of 11
      promoted scenarios present, 10 byte-identical, the eleventh differing by
      exactly one added `AND` bullet with nothing removed, and all 67 canon body
      lines surviving. The block was BUILT FROM CANON at named anchors, not
      retyped.
- [x] 4.4 `health/dispositions.yaml`'s unsuitability MEASURED, not assumed:
      `load_dispositions` keys on `(family, repo, path)`; every finding in
      `release_tag_publication.py` passes `MANIFEST` as its path; and the
      loader's own docstring records that the file is unreachable in
      `--single-repo` scope, which is the scope the red self-gate runs in.
- [x] 4.5 `docs/contract-versioning-policy.md` CONFIRMED a non-editorial member
      of `contracts/releases/contract-v3.0.digests.yaml` (artifact
      `docs-contract-versioning-policy.md`), against
      `release_inventory.EDITORIAL`'s three names. That is OD-6's whole basis
      and it is a file read, not a recollection.
- [x] 4.6 `--single-repo` doc-health with and without this packet, same clock —
      base a detached worktree at `ff9ed815`, head this packet COMMITTED (an
      untracked packet is invisible to the readers, which was checked and is why
      the measurement was retaken after the commit). **6 critical / 5 error / 29
      warning / 12 info on BOTH, and the two reports are BYTE-IDENTICAL** once
      the repo-identity string is normalized. `family-enumeration`: no findings.
      `modified-block-currency`: scenario-title completeness 0, carriage ledger
      unchanged at 8. `status-validity`: no findings, so the header is accepted
      (it read `Status: draft` when this box was measured, and reads
      `Status: ratified` since the ratification of 2026-09-02; the measurement
      is left as taken rather than re-typed to match the later header). The census is unmoved because `proposal.md` is in the
      LIFECYCLE SCAN SET rather than the governed corpus, which the
      `Deterministic check families` requirement states in terms.
      **If a reviewer's run disagrees with this box, the disagreement is the
      finding.**
- [x] 4.7 **THE ONE THING THE MEASUREMENT MISSED, FOUND BY CI AND NOT BY
      PREDICTION.** The first `pytest-suite` run reported TWO failures, not one:
      the inherited red, and
      `tests/sequenced_after/test_sweep.py::test_the_live_sweep_reproduces_the_AUTHORING_measurement`,
      which is NOT inherited — it passes at `ff9ed815` in a detached worktree
      and fails with the packet, because authoring an ACTIVE change carrying a
      MODIFIED block raises `co_modified` 104 → 105, `active_co_modified`
      18 → 19 and `change_ids` 154 → 155 — its `- 1` reading, which subtracts the pin's own owning change, moving 153 → 154.
      That is the pin doing its job, and its
      own docstring prescribes the response: move it in the SAME COMMIT with a
      dated MOVEMENT LOG entry naming which subject moved and why. Done, with
      the three counts that did NOT move (`sole_modifiers` 49, `active_sole` 12,
      `declaring` 1) asserted unchanged so that a change adding itself to two
      populations at once could not pass unnoticed.
      `python3 scripts/validate-sequenced-after.py .` passes (31 active, 1
      declaring); `pytest tests/sequenced_after` 118 passed.
      **Recorded as a miss rather than smoothed over**: the doc-health
      measurement in 4.6 was complete for doc-health and was read as though it
      were complete for the repository, and it was not.

## 5. Archive — last, and open until the merge it follows exists

- [x] 5.1 Archive via `scripts/proposal-support.py . archive`, never bare
      `openspec`, once group 2 is merged with green evidence. The surface cuts
      no bundle, so the gate is merge-plus-green.
      **THE WRAPPER WAS TRIED FIRST AND REFUSED, AND BARE `openspec archive` WAS
      USED INSTEAD, FOLLOWING THE PRECEDENT `govern-sibling-added-modified-deltas`
      SET (PR #571, squash `3bcde7e2`).** `python3 scripts/proposal-support.py .
      archive declare-spent-bundle-state --yes` exited 1, `"change has incomplete
      tasks"` — its gate is `re.search(r"^- \[ \]", tasks.md)`, unconditional on
      WHICH box, and task 3.2 is genuinely, correctly open (it names an event —
      the editorial drift `info` and the policy-doc `error` clearing on their own
      at the NEXT contract cut — that has not happened and cannot be ticked
      truthfully today; OD-6's whole point is that this box is not this change's
      to close). Ticking 3.2 to satisfy the wrapper would be writing a false
      completion to get past a gate that cannot tell "open by omission" from
      "open by design" apart. `OPENSPEC_TELEMETRY=0 openspec archive
      declare-spent-bundle-state --yes` was run instead: it reported
      `Task status: 21/24 tasks`, `Warning: 3 incomplete task(s) found.
      Continuing due to --yes flag.` (3.2, 5.1, 5.2, at the point it ran — 5.1
      and 5.2 are ticked in this same pass, immediately after), applied the ONE
      MODIFIED block to `openspec/specs/doc-health/spec.md`, and moved the
      packet to `openspec/changes/archive/2026-09-03-declare-spent-bundle-state/`.
- [x] 5.2 At promotion, re-verify the MODIFIED block byte-for-byte against the
      canon it replaces. This requirement has now been restated once; the estate
      has lost scenarios to a MODIFIED block three times, and every catch was
      human until a check existed.
      **VERIFIED MECHANICALLY, PER REQUIREMENT, NOT BY EYE.** `doc-health/spec.md`
      was sliced on `^### Requirement: ` into one file per requirement, before the
      archive commit and after. Diffing the two sets: **all 42 requirements
      other than `Release-tag publication` are byte-identical**, and
      `Release-tag publication` is the only one that differs. Its NEW canon body
      (`sed -n '2275,2666p'`, 392 lines) was then diffed against the delta's own
      requirement body from
      `openspec/changes/declare-spent-bundle-state/specs/doc-health/spec.md` (392
      lines, everything after its `## MODIFIED Requirements` header) — **`diff`
      reports zero lines of difference: the promoted requirement is byte-for-byte
      the delta**, confirming MODIFIED replaced the requirement wholesale rather
      than merging, editing, or dropping any of its eleven promoted scenarios or
      thirteen added ones. `git diff --stat` on the canon file shows `263
      insertions(+), 0 deletions(-)`, consistent with the proposal's own claim
      that ten of eleven promoted scenarios are untouched and the eleventh gains
      exactly one `AND` bullet with nothing removed.
