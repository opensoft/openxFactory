# Tasks: declare-spent-bundle-state

Status: draft

**NOTHING BELOW GROUP 4 HAS BEEN DONE, AND GROUP 2 IS DELIBERATELY NOT STARTED.**
Group 1 is ratification, which has not happened. Group 2 is the realization plan
and every box in it is open by decision, not by omission — OD-8 splits this
packet from its code, so a tick in group 2 appearing in the same PR as this file
would be the thing that decision forbids. Group 4 records what the authoring
session MEASURED before the packet was put up, which is evidence rather than
implementation.

Build group 2 with Speckit, not `/opsx:apply`. OpenSpec ratifies; Spec Kit
builds. Group 2 is ONE Spec Kit feature: the reader, the ladder, the two emits,
the `contract-v2.6` declaration and the tests are a single vertical slice, and
splitting them would produce halves neither of which is green alone — a reader
with no declaration to read leaves the `error` standing, and a declaration with
no reader is a sentence in a changelog.

## 1. Ratification — NOT DONE, and it gates group 2

- [ ] 1.1 Put OD-1 … OD-8 and OQ-1 … OQ-3 to Brett Heap. His commissioning
      ("Merge now, fix #575 next") authorizes AUTHORING and covers nothing
      below it; every decision in § Orchestrator Decisions is the authoring
      session's and each names the alternative it rejected.
- [ ] 1.2 **OD-3 and OD-4 are the two that carry governance content and should
      be ruled explicitly rather than accepted by silence.** OD-3 decides
      whether a correctly declared spent bundle is RECORDED (`info`) or SILENT;
      OD-4 decides that the only way to quiet a bundle is to publish its
      successor's tag, which is what makes the state unabusable. A ruling that
      names four decisions and not these two leaves them OWED, in the shape the
      archived packet's D4 was carried rather than assumed.
- [ ] 1.3 Record the ratification at `review/ratification-<date>.md`, set
      `Status: ratified` and add the record-citing `Ratified:` line to
      `proposal.md`. Ratification authorizes realization and performs none of
      it.

## 2. Realization — ONE Spec Kit feature, gated on 1.1

- [ ] 2.1 **FIRST, AND NOT SILENTLY: write the `contract-v2.6` declaration.**
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
- [ ] 2.2 `scripts/doc_health/release_tag_publication.py` — the reader: one pure
      function from the changelog bytes to `{bundle: declaration}`, parsing the
      reserved opener, the four elements and the containing `## contract-vX.Y`
      entry. Bytes in, per the module's existing rule that `blobs_at` answers raw
      blob bytes. Reject rather than skip on a malformed line.
- [ ] 2.3 The ladder in `check_repo`, in the ABSENT arm only and after the
      `ok`/`lightweight`/`misplaced` branches, so OD-3's scope rule holds by
      construction rather than by care: no declaration → today's behaviour
      unchanged; declaration accepted and successor published → `info`;
      successor cut but unpublished → `warning`; successor never cut, element
      missing, duplicate declaration, wrong containing entry, or naming the
      currently declared bundle → `error`.
- [ ] 2.4 The two new emits, on `contracts/CHANGELOG.md` rather than `MANIFEST`
      (OD-5), with the spent `info` carrying `resolution="contested"`. New
      action constants beside the four the module already has.
- [ ] 2.5 The changelog read joins the manifest read at the SAME commit and
      carries the SAME guard: `blobs_at` answering None is a skip naming that
      read, never "no declaration". This is the #338 conflation one document
      over, and the family has already been caught by it once.
- [ ] 2.6 `tests/doc-health/test_release_tag_publication.py` — the ten new
      scenarios as tests over the file's existing real-git fixtures, each with
      the positive control the file's own convention requires. Include the
      RED-FIRST proof for 2.1's verification: the declaration removed, the
      `error` returns.
- [ ] 2.7 **Prove OQ-3 rather than inherit it**: a test that a contested `info`
      vanishing between reports produces an `uncited-resolution` ERROR. If it
      does not, OD-5's class choice returns to Brett as an open question and is
      not quietly dropped.
- [ ] 2.8 `docs/doc-health.md` — the family's row and action line gain the third
      state. Check the family count sentences are untouched: this change adds no
      family and `family-enumeration` must stay silent.
- [ ] 2.9 `python3 -m pytest tests/doc-health` green over the realized tree,
      including `test_this_repository_reads_zero_and_the_probe_can_fire`, which
      goes green as a CONSEQUENCE and is not edited.

## 3. Owed at the next contract cut — NOT here (OD-6)

- [ ] 3.1 `docs/contract-versioning-policy.md` gains the obligation-side
      statement of the SPENT state, beside § *Immutable Tag Correction* whose
      *"its version number is never reused"* the `contract-v2.6` disposition
      already leans on, and naming the reserved declaration form so a consumer
      reading the pinned policy can find the state without reading doc-health.
      **It rides the next cut** because the file is a NON-EDITORIAL member of
      `contracts/releases/contract-v3.0.digests.yaml` and editing it between cuts
      raises a `release-inventory-drift` ERROR. Nothing in the delta depends on
      it having landed.
- [ ] 3.2 At that same cut, `contracts/CHANGELOG.md`'s drift `info` clears on its
      own when the inventory re-baselines. No action; recorded so a reader does
      not go looking for one.

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
- [ ] 4.6 `--single-repo` doc-health with and without this packet, same clock,
      recorded here as a table. Expected: one `modified-block-currency` `info`
      and nothing else moves. **If a reviewer's run disagrees with that
      sentence, the disagreement is the finding.**

## 5. Archive — last, and open until the merge it follows exists

- [ ] 5.1 Archive via `scripts/proposal-support.py . archive`, never bare
      `openspec`, once group 2 is merged with green evidence. The surface cuts
      no bundle, so the gate is merge-plus-green.
- [ ] 5.2 At promotion, re-verify the MODIFIED block byte-for-byte against the
      canon it replaces. This requirement has now been restated once; the estate
      has lost scenarios to a MODIFIED block three times, and every catch was
      human until a check existed.
