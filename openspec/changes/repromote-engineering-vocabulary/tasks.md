# Tasks: repromote-engineering-vocabulary

Status: draft
Authored: 2026-09-16, lane `openxfactory-4` (display `openXfactory-4-openDox_extraction`), actor
`substrate52a`. Realizes `split-opendox-two-layer-product` § 5.2a and nothing else.

THREE ACTS, AND THEY ARE SEPARATE: the FILING (§ 2, this pull request), RATIFICATION (§ 1, Brett
Heap's word) and the ARCHIVE (§ 3, which is where the fifteen actually reach canon). This packet
performs only the first.

## 1. Ratification — BRETT HEAP'S WORD, NOT THIS LANE'S

- [ ] 1.1 The id `openxfactory-engineering-adapter` is accepted, or another is ruled. `design.md`
      § D1 derives it from the packet's own 22 uses of "engineering adapter", the ratified map's
      fifteen identical destination phrases, and the two LANDED machine names that fix its spelling.
      Four candidates are rejected there with reasons. **A different id is a one-command rebuild**:
      the delta is generated, not typed.
- [ ] 1.2 `design.md` § D2's TWO disclosed edits are accepted as the re-expression § 5.2a permits —
      both `resolve`, both in *doxBench resolves its released contract from the checkout it runs in*.
- [ ] 1.3 `design.md` § D2's RECORDED NON-EDITS are accepted, with the finding they carry: four of
      the six path-literal occurrences name a question the six-wide seam does not answer as its
      requirement states it (a topic's EXISTENCE under staging; the DESTINATION of authoring the
      console must not perform; twice the workspace returned documents land in), and `proposal.md`
      (×4) and `OPENXFACTORY_ROOT` (×3) are not locations at all.
- [ ] 1.4 `design.md` § D3 — NO second `## REMOVED Requirements` block on `ideation-dashboard` — is
      accepted, or the opposite is ruled and this lane authors the block. **This is the one judgment
      in the packet that a reasonable reader could take the other way**, and it is put here rather
      than resolved silently.
- [ ] 1.5 `design.md` § D4's archive ORDER — this packet archives BEFORE
      `split-opendox-two-layer-product` — is accepted.
- [ ] 1.6 On the word: `Status: ratified` + the citation on all three lifecycle documents, a
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
- [x] 2.7 GATES RUN ON THIS BRANCH, each recorded with its number in the pull-request body:
      the PINNED CLI (`1.12.0`, the version `contracts/openspec-cli-pin.yaml` names) on this change
      and on `--all --strict`; `python3 -m pytest tests/doc-health tests/sequenced_after`;
      `python3 scripts/validate-sequenced-after.py . --ledger-diff`; and the promotion-fidelity
      family single-repo run, whose count MUST NOT move — this packet promotes nothing.
- [x] 2.8 **THE DELTA CARRIES A WRITTEN `## Purpose`, BECAUSE THIS CAPABILITY DOES NOT EXIST YET.**
      `prepare-openspec-1-12-readiness`'s `document-lifecycle` delta states the rule and the trap:
      *"A `## Purpose` in a change's spec delta is read ONLY when the capability is created; on any
      later archive it is ignored"*, and the archive act otherwise writes `TBD - created by archiving
      change <X>. Update Purpose after archive.` — undischarged on 39 of this corpus's promoted
      specifications when they were last counted. This delta creates the capability, so its Purpose
      IS read, and it is written.
- [x] 2.9 **ARCHIVE DRY RUN, in a throwaway copy of `openspec/` and never in the repository** — the
      CLI's SPEC-APPLICATION step alone (pinned CLI 1.12.0, `archive --yes`), run to see what the
      promoted specification comes out as; the real archive goes through the sanctioned wrapper at
      § 3.1, whose gates this copy cannot run. Measured: `openxfactory-engineering-adapter: create` · `+ 15
      added` · `Totals: + 15, ~ 0, - 0, → 0`; the created promoted spec carries **0** occurrences of
      the placeholder sentence and **15 requirements / 84 scenarios**; all fifteen promote
      BYTE-IDENTICAL to this delta's text; and `openspec/specs/ideation-dashboard/spec.md` comes out
      of the run with an UNCHANGED sha256 — the mechanical proof of `design.md` § D3's claim that
      this packet removes nothing.

## 3. Archive — AFTER RATIFICATION, AND BEFORE THE SPLIT PACKET'S

- [ ] 3.1 On a separate word, through the SANCTIONED WRAPPER and never a bare `openspec archive`:
      `python3 scripts/proposal-support.py . archive repromote-engineering-vocabulary --date <YYYY-MM-DD> --yes`,
      so the origin, retention, task, pin and archive-date gates run. It creates
      `openspec/specs/openxfactory-engineering-adapter/spec.md` with the fifteen.
- [ ] 3.2 **ORDER (`design.md` § D4): this archive precedes `split-opendox-two-layer-product`'s.**
      Re-promotion first leaves the fifteen titles carried by two capabilities — distinct keys,
      no finding on either side. Removal first leaves fifteen ratified requirements in NO capability,
      which is the loss `promotion_fidelity` exists to prevent.
- [ ] 3.3 At that archive, re-run `python3 openspec/changes/repromote-engineering-vocabulary/review/build-delta.py .`
      (no `--write`, so it CHECKS the committed delta against a fresh build and exits non-zero on any
      difference) against the then-current promoted spec first: if
      `main` has moved the promoted text of any of the fifteen, the carry is re-proved or the
      difference is declared before anything promotes.
- [ ] 3.4 Re-seed the sweep ledger (`--seed-ledger --moved-by '#<PR>'`) and re-run
      `--ledger-diff`; the row moves `active` → `archived`.

## 4. What this packet leaves to its neighbours, by name

- [ ] 4.1 **§ 5.2a's TICK** rides the packet bookkeeper's own `tasks.md` amendment. No byte of
      `openspec/changes/split-opendox-two-layer-product/` is touched here — not a tick, not a map
      row, not a design line.
- [ ] 4.2 **§ 5.6 (the de-floor)** and **§ 8.4 (the floor accounting)** can now name the capability
      directory `openspec/specs/openxfactory-engineering-adapter/` in the ADDED direction. This
      packet does not move the codexFactory floor or any of the five openxFactory pin sites.
- [ ] 4.3 **§ 5.2 (the shed), § 5.4 and § 5.5 (floor parts 2 and 4)** are untouched: no module, test,
      example or governance doc is deleted here, and `docs/opendox-carve-manifest.yaml` is not edited.
- [ ] 4.4 **§ 6.1's seven `doc-health` requirements** and **§ 6.5's intra-requirement narrowing**,
      both of which were carried whole at their destinations for want of this id, are their own
      changes in their own repositories. This packet declares the id; it re-authors nothing there.
- [ ] 4.5 **BLOCKED, and named rather than performed: the four path literals no seam operation
      answers for.** `design.md` § D2 measures them and says what would unblock each — a scope the
      corpus DECLARES for staged topics (`ResolvedCorpus.scopes` is return data, so a home adapter
      may declare one without widening the six operations), or an answer that keeps *absent* and
      *empty* apart for a topic that exists and holds nothing. Both are openDox's to declare under
      RULING Q4 and neither is § 5.2a's to invent, so they are carried here with their literals
      intact and their reasons recorded — the same shape § 6.1 and § 6.5 used for work that was
      named and not performed.
