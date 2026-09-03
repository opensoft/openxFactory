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
      - **2026-09-02 (lane openxfactory-1d): the CONTAINING-ENTRY half of this
        box is HARDENED by PR #589**, on top of the realization that landed as
        PR #587 (`3fa222f3`). Ten escapes measured against `main`'s reader
        before the fix, seven of them letting a declaration be ACCEPTED from
        outside its superseding bundle's entry: a non-release `##` heading, an
        incomplete version token (`## contract-v3.0.1`), a level-one heading, a
        heading inside a code fence, an indented ATX heading, Setext headings,
        and an empty ATX heading — plus a below-floor repository with no
        changelog being skipped entirely, a batch-read skip naming one of two
        members it read, and a spurious orphan warning on a below-floor
        subject. The rule now passes through one structural-boundary function
        and is pinned as one table; fenced blocks are declared OPAQUE. NOTHING
        IN THIS BOX IS RE-TICKED BY THAT PR — the ladder is #587's, and this
        line records what was hardened over it.
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
- [ ] 2.9 `python3 -m pytest tests/doc-health` green over the realized tree,
      including `test_this_repository_reads_zero_and_the_probe_can_fire`, which
      goes green as a CONSEQUENCE and is not edited.
      **DELIBERATELY UNTICKED, AND THE REASON IS A RULING RATHER THAN A MISS.**
      Brett Heap ruled 2026-09-02 (issue #575, lane openxfactory-1d): *"merge the
      realization on the dispositioned red."* The family resolves its tip with
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
      the inherited `error`. The test is NOT edited. This box is ticked by
      whoever confirms `main`'s suite green at the squash.

## 3. Owed at the next contract cut — NOT here (OD-6)

- [ ] 3.1 `docs/contract-versioning-policy.md` gains the obligation-side
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

- [ ] 5.1 Archive via `scripts/proposal-support.py . archive`, never bare
      `openspec`, once group 2 is merged with green evidence. The surface cuts
      no bundle, so the gate is merge-plus-green.
- [ ] 5.2 At promotion, re-verify the MODIFIED block byte-for-byte against the
      canon it replaces. This requirement has now been restated once; the estate
      has lost scenarios to a MODIFIED block three times, and every catch was
      human until a check existed.
