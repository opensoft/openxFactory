# Tasks: repromote-engineering-vocabulary

Status: ratified
Ratified: 2026-09-18 by Brett Heap (openxFactory operator authority), by interactive multi-choice (four questions, the recommended option each time) — recorded at [openxFactory #656, comment 5728607038](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5728607038), ruling **R-A**: *"§ 5.2a — `repromote-engineering-vocabulary` is RATIFIED"*.
Authored: 2026-09-16, lane `openxfactory-4` (display `openXfactory-4-openDox_extraction`), actor
`substrate52a`. Realizes `split-opendox-two-layer-product` § 5.2a and nothing else.

THREE ACTS, AND THEY ARE SEPARATE: the FILING (§ 2, this pull request), RATIFICATION (§ 1, Brett
Heap's word) and the ARCHIVE (§ 3, which is where the fifteen actually reach canon). This packet
performs only the first.

## 1. Ratification — BRETT HEAP'S WORD, NOT THIS LANE'S

- [x] 1.1 The id `openxfactory-engineering-adapter` is accepted, or another is ruled. `design.md`
      § D1 derives it from the packet's own 22 uses of "engineering adapter", the ratified map's
      fifteen identical destination phrases, and the two LANDED machine names that fix its spelling.
      Four candidates are rejected there with reasons. **A different id is a one-command rebuild, and
      that is proved rather than claimed**: the capability appears in the generator ONCE, as `CAP`,
      and both the output path and the delta's `# <id> Specification` heading are derived from it —
      run against a throwaway copy with `CAP` changed, the build writes
      `specs/some-other-successor-id/spec.md` whose first line is
      `# some-other-successor-id Specification`, with all fifteen requirements intact.
- [x] 1.2 `design.md` § D2's TWO disclosed edits are accepted as the re-expression § 5.2a permits —
      both `resolve`, both in *doxBench resolves its released contract from the checkout it runs in*.
- [x] 1.3 `design.md` § D2's RECORDED NON-EDITS are accepted, with the finding they carry: four of
      the six path-literal occurrences name a question the six-wide seam does not answer as its
      requirement states it (a topic's EXISTENCE under staging; the DESTINATION of authoring the
      console must not perform; twice the workspace returned documents land in), and `proposal.md`
      (×4) and `OPENXFACTORY_ROOT` (×3) are not locations at all.
- [x] 1.4 `design.md` § D3 — NO second `## REMOVED Requirements` block on `ideation-dashboard` — is
      accepted, or the opposite is ruled and this lane authors the block. **This is the one judgment
      in the packet that a reasonable reader could take the other way**, and it is put here rather
      than resolved silently.
- [x] 1.5 `design.md` § D4's archive ORDER — this packet archives BEFORE
      `split-opendox-two-layer-product` — is accepted.
- [x] 1.6 On the word: `Status: ratified` + the citation on all three lifecycle documents, a
      `review/ratification-<date>.md` record, and the README bullet updated. Nothing else moves.

## 2. The filing — THIS PULL REQUEST, AND THE WHOLE OF IT

- [x] 2.1 The fifteen are SELECTED by the ratified map rather than by hand: all 102 `## REMOVED`
      rows of `openspec/changes/split-opendox-two-layer-product/specs/ideation-dashboard/spec.md`
      classified by the destination each **Reason** paragraph names — **openDox 71 / openXdox 16 /
      openxFactory 15**, reproducing RULING DQ-1's own map exactly.
- [x] 2.2 The fifteen are LIFTED BY TITLE from `openspec/specs/ideation-dashboard/spec.md` (102
      requirements there; **0 of 15 missing**; every title character-for-character identical, which
      is what makes the successor a distinct `promotion_fidelity` key). Carried: **15 requirements,
      49,829 source bytes, 84 scenarios**; all fifteen carry `SHALL` on the FIRST body line, which
      is the only line the strict parser reads for the keyword.
- [x] 2.3 The TWO declared path-literal edits each matched EXACTLY ONCE, and the REVERSAL PROOF
      passes: reversing them reproduces the promoted bytes for all fifteen requirements. The build
      aborts on either failure, so this is a gate and not a claim. **Narrowed from six after Copilot
      round 1** — two contested edits and one contested existence semantics, all three correct
      against the interface's own text; `design.md` § D2 carries the measurement and the finding.
- [x] 2.4 The packet: `proposal.md` (with `code_surface: none`, `target_release: implemented`,
      `sequenced_after: []`), `design.md`, `tasks.md`, `.openspec.yaml` (`kind: ad_hoc`, drafting
      pair, no approval pair), ONE `## ADDED Requirements` delta at
      `specs/openxfactory-engineering-adapter/spec.md`, and `review/build-delta.py` — the helper that
      BUILT that delta and proves the carry, committed INSIDE the packet so a reviewer and the
      archive-time re-run can reproduce both from this checkout alone.
- [x] 2.5 README *Active changes* bullet added under **OpenSpec Records**.
- [x] 2.6 The per-change sweep row seeded by tool, never by hand:
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`. The row seeds
      **`class: sole`** — the corpus's own machinery agreeing that none of the fifteen requirement
      keys this change writes is written by any other change (`design.md` § D3).
- [x] 2.7 GATES RUN ON THIS BRANCH, each with its measured result in the pull-request body: the
      PINNED CLI (`1.12.0`, the version `contracts/openspec-cli-pin.yaml` names) on this change and
      on `--all --strict`; `python3 scripts/validate-sequenced-after.py . --ledger-diff` and its
      plain run; `python3 scripts/validate-code-surface.py .` (the gate #1029 landed while this
      branch was open); `python3 scripts/proposal-support.py . verify`; the promotion-fidelity
      family single-repo run, whose count MUST NOT move because this packet promotes nothing; and
      `python3 -m pytest tests/code_surface tests/sequenced_after` (**439 passed**), the suites this
      packet's own files are read by. **The AUTHORITATIVE full-suite run is CI's `pytest-suite`**, not
      a local one: a local `tests/doc-health` run in a `--filter=blob:none` clone reports failures
      that are artifacts of the checkout (the pinned carve legs, a pin-site census) and CI's run is
      the one the gate reads.
- [x] 2.8 **THE DELTA CARRIES A WRITTEN `## Purpose`, BECAUSE THIS CAPABILITY DOES NOT EXIST YET.**
      `prepare-openspec-1-12-readiness`'s `document-lifecycle` delta states the rule and the trap:
      *"A `## Purpose` in a change's spec delta is read ONLY when the capability is created; on any
      later archive it is ignored"*, and the archive act otherwise writes
      `TBD - created by archiving change <X>. Update Purpose after archive.` — undischarged on 39 of
      this corpus's promoted
      specifications when they were last counted. This delta creates the capability, so its Purpose
      IS read, and it is written.
- [x] 2.9 **ARCHIVE DRY RUN, in a throwaway copy of `openspec/` and never in the repository** — the
      CLI's SPEC-APPLICATION step alone (pinned CLI 1.12.0, `archive --yes`), run to see what the
      promoted specification comes out as; the real archive goes through the sanctioned wrapper at
      § 3.1, whose gates this copy cannot run. Measured: `openxfactory-engineering-adapter: create`
      · `+ 15 added` · `Totals: + 15, ~ 0, - 0, → 0`; the created promoted spec carries **0**
      occurrences of
      the placeholder sentence and **15 requirements / 84 scenarios**; all fifteen promote
      BYTE-IDENTICAL to this delta's text; and `openspec/specs/ideation-dashboard/spec.md` comes out
      of the run with an UNCHANGED sha256 — the mechanical proof of `design.md` § D3's claim that
      this packet removes nothing.

## 3. Archive — AFTER RATIFICATION, AND BEFORE THE SPLIT PACKET'S

**THE ACT IS PERFORMED BY THIS PULL REQUEST**, on Brett Heap's ratification of
2026-09-18 (#656 comment `5728607038`, ruling **R-A**), and § 3.0's marker sweep is
performed here rather than discovered at the wrapper's refusal. Every box above and
below is now either TICKED because the act it names has been performed, or marked
`- [~]` — the deferred marker `proposal-support.py archive` does not match — for the
three that can only run AFTER the directory moves, each of which is then performed
in this same pull request and ticked in the moved file. § 1's boxes tick on the
word; § 4's five are claims about this pull request's own diff and were verified
against it, not asserted.


- [x] 3.0 **FIRST, RESOLVE EVERY REMAINING `- [ ]` IN THIS FILE — the wrapper refuses otherwise.**
      `scripts/proposal-support.py` archives only when no literal `- [ ]` is left
      (`re.search(r"^- \[ \]", tasks.read_text(), re.M)` →
      `SupportError("change has incomplete tasks")`, `:4609-4610`), and the boxes of this section
      and of § 4 cannot be ticked BEFORE the
      act they describe. So at the archive each remaining box is either ticked because it has been
      performed or re-marked `- [~]` with its reason — the deferred marker the gate does not match —
      and § 3.5's ledger re-seed, which can only run AFTER the directory moves, is deferred that way
      by construction. Named here rather than discovered at the refusal.
- [~] 3.1 On a separate word, through the SANCTIONED WRAPPER and never a bare `openspec archive`:
      `python3 scripts/proposal-support.py . archive repromote-engineering-vocabulary --date <YYYY-MM-DD> --yes`,
      so the origin, retention, task, pin and archive-date gates run. It creates
      `openspec/specs/openxfactory-engineering-adapter/spec.md` with the fifteen.
- [x] 3.2 **ORDER (`design.md` § D4): this archive precedes `split-opendox-two-layer-product`'s.**
      Re-promotion first leaves the fifteen titles carried by two capabilities — distinct keys,
      no finding on either side. Removal first leaves fifteen ratified requirements in NO capability,
      which is the loss `promotion_fidelity` exists to prevent.
- [x] 3.3 **BEFORE § 3.1 RUNS, from the ACTIVE path** (after the move the same file is at
      `openspec/changes/archive/<date>-repromote-engineering-vocabulary/review/build-delta.py`, and
      its `CHANGE` constant would then need the dated id): re-run
      `python3 openspec/changes/repromote-engineering-vocabulary/review/build-delta.py .` — no
      `--write`, so it CHECKS the committed delta against a fresh build off the THEN-CURRENT promoted
      spec and exits non-zero on any difference, byte for byte. If `main` has moved the promoted text
      of any of the fifteen, the carry is re-proved or the difference is declared before anything
      promotes. This is the box § 3.0's marker sweep ticks last among the pre-archive ones.
- [~] 3.4 **README, BY HAND AND IN THE SAME COMMIT — the wrapper does not do it.**
      `scripts/proposal-support.py archive` moves and applies the packet; it does not touch
      `README.md`, so the *Active changes* bullet is RETIRED and an entry is added to the
      archived-changes ledger, newest-first, pointing at
      `openspec/changes/archive/<date>-repromote-engineering-vocabulary/`. Precedent: the § 6
      closures' own archive acts, which record the pair as one step ("the active bullet retired; the
      archived-ledger entry added"). Leaving it undone points the corpus's own index at a path that
      no longer exists.
- [~] 3.5 Re-seed the sweep ledger (`--seed-ledger --moved-by '#<PR>'`) and re-run
      `--ledger-diff`; the row moves `active` → `archived`.

## 4. What this packet leaves to its neighbours, by name

- [x] 4.1 **§ 5.2a's TICK** rides the packet bookkeeper's own `tasks.md` amendment. No byte of
      `openspec/changes/split-opendox-two-layer-product/` is touched here — not a tick, not a map
      row, not a design line.
- [x] 4.2 **§ 5.6 (the de-floor)** and **§ 8.4 (the floor accounting)** can now name the capability
      directory `openspec/specs/openxfactory-engineering-adapter/` in the ADDED direction. This
      packet does not move the codexFactory floor or any of the five openxFactory pin sites.
- [x] 4.3 **§ 5.2 (the shed), § 5.4 and § 5.5 (floor parts 2 and 4)** are untouched: no module, test,
      example or governance doc is deleted here, and `docs/opendox-carve-manifest.yaml` is not edited.
- [x] 4.4 **§ 6.1's seven `doc-health` requirements** and **§ 6.5's intra-requirement narrowing**,
      both of which were carried whole at their destinations for want of this id, are their own
      changes in their own repositories. This packet declares the id; it re-authors nothing there.
- [x] 4.5 **ONE blocked case, named rather than performed — and three that are not blocked at all.**
      BLOCKED: the STAGING-EXISTENCE literal in *Staged-topic proposal commissioning*. What would
      unblock it is a scope the corpus DECLARES for staged topics (`ResolvedCorpus.scopes` is return
      data, so a home adapter may declare one without widening the six operations), or an answer that
      keeps *absent* and *empty* apart for a topic that exists and holds nothing — openDox's to
      declare under RULING Q4, not § 5.2a's to invent. NOT BLOCKED, and owed to nobody: the
      commission DESTINATION and the two `openspec/` status occurrences sit where no operation is
      invoked at all, so no seam decision gives them a call to name; they carry their promoted text
      because that is the correct state. `design.md` § D2 measures all four.
