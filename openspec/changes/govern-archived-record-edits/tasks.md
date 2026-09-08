# Tasks: govern-archived-record-edits

Status: draft
Lane: opsXfactory-1

**NOTHING BELOW IS DONE. EVERY BOX IS UNTICKED, AND THAT IS THE STATE OF THE
PACKET RATHER THAN AN OVERSIGHT.** This is a PROPOSAL. No archived byte is
edited, no pin is re-derived, no checker is written, no repository's local
convention is amended, and no spec delta is promoted.

**Tags.** Untagged = openxFactory. `[OpsxFactory]` = `opensoft/OpsxFactory` and
its own OpenSpec instance — listed as the domain twin's acts, outside this
change's archive gate. `[OPERATOR]` = only Brett Heap can perform it.

## 0. Bookkeeping this branch carries, and the one stamp that is provisional

- [ ] 0.1 **RE-STAMP THE SWEEP LEDGER ROW WITH THE REAL PULL-REQUEST NUMBER.**
  `tests/sequenced_after/corpus-ledger.yaml` carries this change's row and its
  DERIVED keys are measured and correct (`--ledger-diff` exits 0 at this
  branch's head). Its `moved_by` is **PROVISIONAL** — no pull request existed
  when the seeder ran, and the value is a placeholder rather than an observed
  number. The ledger's own doctrine makes `moved_by` AUTHOR-SUPPLIED AND
  UNVERIFIED (only its `#<digits>` shape is checked), so this reds no gate; it
  is a pointer a human follows and it should be true.
  **IT IS ALREADY KNOWN TO BE WRONG, SO THIS BOX IS MANDATORY AND NOT TIDY-UP.**
  `#785` was the next number free when the seeder ran; it is now
  `ideation/remove-moved-domain-files`, another lane's OPEN pull request. This
  is the second time the trap has sprung on this lane —
  `add-consent-custody-rederivation-record`'s provisional `#757` was taken the
  same way while that packet was in review — and it will spring again for
  anyone who reads a placeholder as provenance.
  **DO NOT RE-RUN THE SEEDER FOR THIS — IT IS A NO-OP HERE, AND THAT IS
  MEASURED, NOT ASSUMED.** `--seed-ledger --moved-by '#<real>'` re-derives the
  corpus and stamps provenance only on rows whose DERIVED keys actually moved;
  this row's derived keys are already correct, so the seeder PRESERVES its
  existing provenance. Run at this head with a different number it reported
  `184 rows, 0 moved by #999` and produced a **ZERO-LINE DIFF**, leaving
  `moved_by: "#785"` in place — the documented recipe would look like a
  re-stamp and change nothing. **The re-stamp is a DIRECT ONE-FIELD EDIT** of
  this row's `moved_by` in `tests/sequenced_after/corpus-ledger.yaml`, followed
  by `python3 scripts/validate-sequenced-after.py . --ledger-diff`, which MUST
  report `per-change sweep ledger consistent with the corpus` — also measured at
  this head with the field edited by hand. That is legitimate because the
  ledger's own doctrine makes `moved_by` AUTHOR-SUPPLIED AND UNVERIFIED,
  shape-checked (`#<digits>`) and never resolved.

  **PERFORMED 2026-09-08.** openxFactory PR
  [#788](https://github.com/opensoft/openxFactory/pull/788) was opened by
  `openxfactory[bot]` on head `97d1e7fa`, so the real number is known. The row's
  `moved_by` was edited directly from `"#785"` to `"#788"` — ONE field, ONE
  line, nothing else in the file — and
  `python3 scripts/validate-sequenced-after.py . --ledger-diff` reports
  `per-change sweep ledger consistent with the corpus (184 rows)`. `moved_on`
  is NOT re-stamped: it records when the row's derived keys moved, which was
  2026-09-08, not when its provenance pointer was corrected.

  **THE BOX STAYS UNTICKED, AND THAT IS THE CONVENTION RATHER THAN AN
  OVERSIGHT.** This file's own preamble holds that every box is unticked while
  the packet is a proposal, and this packet is `Status: draft` awaiting
  ratification at task 1.1. The corpus precedent is exact:
  `add-consent-custody-rederivation-record` is `Status: ratified`, its ledger
  row carries the REAL pull request `#774`, and its `tasks.md` has ZERO ticked
  boxes — the ledger carrying a true number and the box staying unticked are
  not in tension, because the row is bookkeeping the branch carries and the box
  is a claim about the packet having begun.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **[OPERATOR] Ratify or veto.** The F.3 ruling came in TWO comments on
  OpsxFactory PR #248 — the SHAPE
  (*"Header/bookkeeping edits only + re-derive pins"*) on 2026-09-06T23:42Z,
  comment 5563099832, and the HOME (*"Both at once"*) on 2026-09-07T13:51Z,
  comment 5571629298. It chose no requirement title, no delta shape, no
  definition of the bookkeeping class, no ordering between ruling and edit, and
  no refusal posture. Each is `design.md`'s D-1..D-8 and each is a veto point.
- [ ] 1.2 **[OPERATOR] TWO named widenings and one split, each a veto point.**
  Mirrored from the domain twin's 1.2a/1.2b/1.2c, because the same three
  decisions are open in both halves and a ruling on one is a ruling on both.
  - [ ] 1.2a **The pin SCOPE.** Your 2026-09-06 shape selection (comment
    5563099832) says "every dependent **custody** pin". The second ADDED
    requirement reaches EVERY pin of EVERY declared family. Basis: your
    2026-09-07 restatement (comment 5571629298) drops the qualifier — "every
    edit of a pinned target re-derives dependent pins in the same change" —
    read with your F.2 scope selection of the same day, "Every in-repo sha256
    pointer to an in-repo target", the widest option put to you and the scope
    the OpsxFactory gate is built to. **The narrower reading — CUSTODY PINS
    ONLY — is available**: it matches the 2026-09-06 wording exactly, and its
    cost is that evidence digests, plan-acceptance references, fence baselines
    and contract pins are obliged by nothing while that gate re-derives them.
    Narrowing here forces the same narrowing on the OpsxFactory half.
  - [ ] 1.2b **The no-rule consequence, and WHEN it bites.** As written the
    requirement REPORTS such an edit — naming the family, the target and the
    home that owes the rule — and refuses only once that family declares.
    **THREE options, not two.** (i) Report-then-refuse, as written. (ii)
    **REFUSE FROM LANDING**: coherent, and measured it refuses EVERY
    pinned-target edit in the estate the day this change archives, because no
    family has a declared rule and `code_surface: none` means it archives on
    landing with nothing to sequence behind — the routine lifecycle-header
    discharge and the F.1/F.2 repairs included. (iii) **STRIKE the consequence**,
    leaving the obligation with no consequence for the families that need it
    most. Either alternative forces the OpsxFactory half to move in LOCKSTEP: it
    states the same rule at its own altitude, and a downstream `MUST` may not
    contradict a neutral `MUST NOT`.
  - [ ] 1.2c **The ONE-vs-TWO ADDED split.** Your F.3 wording names "an ADDED
    requirement" — singular — carrying both halves of the rule. This packet
    splits them into TWO, and `.openspec.yaml` flags the delta shape for veto.
    The measured reason is that the failures are invisible to each other: one of
    the three custody pins the motivating commit broke names a target in a
    change directory that has never been archived, so a single requirement
    scoped to `openspec/changes/archive/` would report itself satisfied while
    that pin stayed broken. **If one requirement is wanted**, the cost is that
    its scope sentence must reach outside the archive tree, and the OpsxFactory
    half must collapse the same way.
- [ ] 1.3 **[OPERATOR] Rule on D-3 specifically** — whether the `## MODIFIED`
  block closing *Proposal packets carry the lifecycle header*'s dangling "takes
  the route archived-record edits take" is wanted. Declining it leaves canon
  naming a route it does not define, which is the state that produced the
  finding; taking it means a MODIFIED block that must stay current until
  archive (task 4.2).
- [ ] 1.4 **[OPERATOR] Rule on the reading NOT taken** — a STRICT READ-ONLY
  ARCHIVE. `design.md` § *Readings not taken* 1 records why this packet declines
  it (it would make the pre-existing header population permanently unfixable,
  contradicting canon in force, and it would overturn the F.3 selection). It
  remains available and would be a different change.
- [ ] 1.5 Write `review/ratification-<date>.md` recording the word verbatim, the
  head it was given against, and what it does and does not authorize.

## 2. The delta — three requirement blocks, authored

- [ ] 2.1 `## ADDED` — *An archived record is edited only as a bookkeeping
  correction under a recorded ruling*. Authored.
- [ ] 2.2 `## ADDED` — *A change that edits a pinned target re-derives every
  dependent pin in the same change*. Authored.
- [ ] 2.3 `## MODIFIED` — *Proposal packets carry the lifecycle header*.
  Authored. Verified against canon: **canon's block is 5,815 characters, the
  delta block is 7,186, and the 1,371-character difference is entirely
  INSERTED** (slice from the requirement heading to the next, trailing newlines
  stripped both sides). EVERY canon byte is carried verbatim, all six promoted
  scenarios restated, and exactly two hunks of difference — both PURE INSERTIONS
  (one paragraph naming the route, one added scenario). Nothing is reworded and
  nothing is deleted, so no
  ``**Removed from canon by …**`` marker is owed and doc-health's
  `modified-block-currency` arm reports nothing against this block.

## 3. Composition — named here; 3.4 alone is this packet's own act

- [ ] 3.1 **[OpsxFactory]** The domain twin `govern-archived-record-edits`
  lands and is ratified. Both packets cross-cite by change id and repository;
  the citations are re-checked to resolve once both heads settle.
- [ ] 3.2 **[OpsxFactory]** `add-content-address-integrity-gate`'s family
  register declares a re-derivation rule per family. The second ADDED
  requirement REPORTS an edit whose family has declared no rule — naming the
  family, the target and the home that owes it — and becomes a REFUSAL for that
  family the day it declares. So each family the register leaves undeclared is a
  standing report this packet creates and that register closes, and the day the
  register lands is the day those families' edits start being refused.
- [ ] 3.3 The consent family's rule is `add-consent-custody-rederivation-record`'s
  `custody_rederivations[]`, merged 2026-09-08 as `543d47a9`. This packet NAMES
  it and restates none of it. Its contract cut and OpsxFactory's re-pin are that
  packet's tasks, not these.
- [ ] 3.4 **openxFactory ADOPTS THE NEUTRAL MINIMUM IN ITS OWN DOCS.** The
  first ADDED requirement states a neutral minimum for the bookkeeping note — a
  dated `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` line in
  the edited file's own lifecycle-header block. **This repository has no
  archived-packet convention at all**, which is why the minimum exists: an
  earlier spelling delegated the note to "the editing repository's own
  convention", leaving the obligation absent in the very repository promoting
  the rule, with only OpsxFactory having written one down. Record the minimum in
  `docs/document-lifecycle.md` beside the `Status:` / `Ratified by:` header
  rules, as a form the lifecycle header block accepts. A governance document, so
  `code_surface` stays `none`.
- [ ] 3.5 Every OTHER DomainxFactory reads its own archived-packet convention
  against the first ADDED requirement and amends whatever is looser, by a dated
  amendment keeping the stale text. Named as owed; not surveyed here.

## 4. Gates

- [ ] 4.1 `python3 scripts/validate-openspec-cli-pin.py --change openspec/changes/govern-archived-record-edits --strict`
  and `--all --strict` with no undispositioned finding.
- [ ] 4.2 **Currency of the MODIFIED block, continuously until archive.**
  `A MODIFIED requirement block restates the requirement as canon currently
  states it` attaches for as long as this change is active. Re-run the
  byte-identity check against `openspec/specs/document-lifecycle/spec.md` before
  archive and bring the block forward if canon moved.
- [ ] 4.3 `python3 scripts/validate-sequenced-after.py .`, `--ledger-diff`,
  `validate-scope-globs.py .`, `validate-manifest-digests.py .` all clean.
- [ ] 4.4 `python3 scripts/doc-health.py --single-repo . --fail-on error` with
  the finding set diff-identical to `main`'s.
- [ ] 4.5 `pytest tests/sequenced_after tests/proposal-support tests/scope_globs -q`
  green.

## 5. Bookkeeping and landing

- [ ] 5.1 One row in README's "OpenSpec Records" block in the neighbours' DRAFT
  form; re-derive at the union if another lane's substrate claim lands first
  (Rule 7). Note `main` moves hourly here: merge forward, never rebase pushed
  commits.
- [ ] 5.2 Rule 6 LANDING notice on the PR and in `LANES.md` before merging into
  `main`; LANDED with the merge sha after.
- [ ] 5.3 Discharge the object and substrate claims on openxFactory issue #630
  naming the PR and the merge sha.

## 6. Archive

- [ ] 6.1 **Archive WHEN ITS ARTIFACTS LAND**, per `release-realization`: the
  declared `code_surface` is `none`, so the archive gate is not merged-plus-green
  realization evidence. **This box said "nothing in § 3 gates it: those are
  other packets' acts", and § 3 holds THREE different kinds of act, not one.**
  3.1, 3.2 and 3.5 are OTHER REPOSITORIES' acts, all OpsxFactory's or a further
  DomainxFactory's. **3.3 is ANOTHER PACKET'S ACT IN THIS REPOSITORY** —
  `add-consent-custody-rederivation-record` is an ACTIVE openxFactory change
  (untagged, per the Tags note above; `543d47a9` resolves in this tree), so its
  contract cut is owed here even though its consumer re-pin is OpsxFactory's.
  **3.4 is THIS PACKET'S OWN act in this repository**: adopting the neutral
  minimum in `docs/document-lifecycle.md`. Only the last of the three can hold
  this packet open, and it does — what the archive act reads is the UNTICKED BOX
  3.4, with 3.1/3.2/3.3/3.5 named beside it for the chain's readability and
  gating nothing here.
- [ ] 6.2 Confirm at the archive act that the three requirement blocks reach
  `openspec/specs/document-lifecycle/spec.md` — *Ratified spec deltas reach the
  promoted specification* is checked against the archived delta's own bytes,
  which is the reason this packet exists.
- [ ] 6.3 [OPERATOR] The archive word.
