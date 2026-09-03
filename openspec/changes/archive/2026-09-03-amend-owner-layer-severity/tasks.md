# Tasks: Amend The Owner-Layer Severity, And Date The Retro-Tagged Bundles

## 1. Establish both defects and the lawful fix

- [x] 1.1 Read both issues in full, including every comment, before authoring:
      #561 (the canon/validator severity divergence, commissioned by
      `retire-hermes-flat-keys-and-openworkflow-tokens` tasks § 6.1) and #339
      (the three retro-published bundles left in the present tense). The ruling
      is recorded VERBATIM as the latest comment on each
- [x] 1.2 Confirm the divergence at the tree rather than from the issue text:
      canon says "SHALL be reported as a validator warning"
      (`openspec/specs/workflow-gate-contract/spec.md`, *Owner layer
      constraint*, promoted at `a1a2802b` on 2026-07-09); the validator says
      `rpt.error` (`scripts/validate-domain-factory.py`, `check_workflows`,
      unchanged since `493fb33d` on 2026-07-03 — six days EARLIER)
- [x] 1.3 Confirm #339's sentence sits INSIDE a requirement body rather than
      in preamble or purpose prose an OpenSpec delta cannot amend. It is in
      the body of `release-surface-integrity`'s *"The declared bundle describes
      the release surface"* — the requirement opens at `spec.md:6` and its
      first `#### Scenario:` is at `:45`, so the paragraph at `:38-43` is
      requirement body and IS amendable by a `## MODIFIED Requirements` block.
      A second delta is therefore carried rather than reported as unreachable
- [x] 1.4 Confirm no ACTIVE change already holds a delta on either
      requirement, so this packet is not a second live writer of one:
      `find openspec/changes -mindepth 3 \( -path '*/specs/workflow-gate-contract/*'
      -o -path '*/specs/release-surface-integrity/*' \) -not -path '*archive*' -print`
      returned NOTHING when run against `origin/main` at `0bf37d14`, before
      this packet's own two delta directories existed; run today it returns
      those two and nothing else, which is the same answer read from the other
      side.
      THE PARENTHESES ARE LOAD-BEARING and are the command as run: `find`
      binds `-a` tighter than `-o`, so an ungrouped
      `-path A -o -path B -not -path '*archive*'` applies the archive
      exclusion to the SECOND branch alone and returns every archived
      `workflow-gate-contract` delta — including
      `archive/2026-07-09-promote-workflow-gate-contract/`, which exists — so
      the ungrouped form's "returns nothing" would be a claim no run supports.
      Raised by Copilot on this packet's own pull request and corrected to the
      run's own text. The finding was in the QUOTE and not in the measurement:
      the grouped form is what was executed, and the sentence that follows is
      an independent corpus-wide reading of the same absence
      The one active mention of `owner_layer` anywhere in a delta is
      `retire-hermes-flat-keys-and-openworkflow-tokens`'s
      `contract-deprecation-execution` requirement, which is a DIFFERENT
      capability and which defers the general severity by name ("whatever the
      general rule carries")
- [x] 1.5 Derive #339's replacement wording from the ruled precedent rather
      than inventing it: PR #333 handled the identical claim in
      `scripts/doc_health/release_inventory.py`'s docstring by DATING the
      examples — "were each declared and UNTAGGED for weeks … they were
      retro-published 2026-08-25 and the design stands on the general fact
      rather than on those three" — and the amended paragraph mirrors it

## 2. Restate both requirements, the ruled words excepted

- [x] 2.1 Build both blocks by EXTRACTING the requirement from canon and
      substituting only what the ruling changes, so no other byte can drift.
      Hashes recorded rather than asserted:

      | requirement | canon block sha256 | this delta's block sha256 |
      | --- | --- | --- |
      | Owner layer constraint | `abe58572…77118237` | `035fb896…bc4ed439` |
      | The declared bundle describes the release surface | `4c9e0b71…313f29567` | `6e102b2e…d02a1d19a` |

- [x] 2.2 Prove delta 1 differs from canon in TWO WORDS and nowhere else, by
      word-diff: `validator warning.` -> `validator error.` in the body, and
      `MUST report a warning identifying` -> `MUST report an error identifying`
      in the scenario. The canonical role list, the `stack.yaml` clause and
      the scenario's `**WHEN**` bullet are byte-identical
- [x] 2.3 Prove delta 2 differs from canon in ONE PARAGRAPH and nowhere else,
      by word-diff: four lines out, six in, all inside the tag-is-not-the-
      reference-point paragraph. Every other body paragraph and all four
      scenarios are byte-identical
- [x] 2.4 Prove scenario completeness on both blocks, the arm the
      `modified-block-currency` family gates at `error`: canon carries 1
      scenario under *Owner layer constraint* and 4 under *The declared bundle
      describes the release surface*; the deltas carry the same 1 and the same
      4, by title, in canon's order
- [x] 2.5 Confirm the SHALL/MUST keyword sits on the FIRST LINE of each
      requirement body, which is all the strict parser reads: "Gate and
      workflow `owner_layer` values SHALL be canonical role names" and "The
      contract bundle a repository DECLARES at a commit SHALL describe that"

## 3. Validation

- [x] 3.1 `OPENSPEC_TELEMETRY=0 openspec validate amend-owner-layer-severity --strict`
- [x] 3.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`
- [x] 3.3 `python3 scripts/proposal-support.py . verify amend-owner-layer-severity`
- [x] 3.4 List this change in the README's OpenSpec Records block
- [x] 3.5 Doc-health rendered on this branch and on a detached `origin/main`
      baseline at `0bf37d14`, and the finding sets diffed. TWO READINGS, taken
      at the two states this one commit passes through, and both recorded:
      with the packet ACTIVE, `6 critical / 6 error / 29 warning` IDENTICAL on
      both trees and `info` 14 -> 16, the two rows being the packet's own
      carriage-ledger rows enumerated in § 5, with ZERO findings lost; after
      the archive act of § 6, the two finding sets are IDENTICAL — 55 lines
      each, `6 critical / 6 error / 29 warning / 14 info` on both, zero new at
      any severity and zero lost — because the carriage rows retire with the
      promotion. The landed tree is the second reading
- [x] 3.6 `python3 -m pytest tests/doc-health`
- [x] 3.7 `python3 -m pytest tests/sequenced_after`

## 4. The two live corpus pins

Both COUNT THE CORPUS, so both move whenever any change is AUTHORED. Neither
is a code surface; each is moved in this change's own commit with a dated
note, which is those pins' own stated protocol, and the proposal's
`code_surface: none` names them rather than leaving them to a diff.

- [x] 4.1 `tests/sequenced_after/test_sweep.py` — `co_modified` 109 -> 111,
      `active_co_modified` 21 -> 22, `change_ids - 1` 157 -> 158,
      `sole_modifiers - 1` 48 -> 47, and `active_sole - 1` HELD at 11 with the
      hold asserted rather than assumed. The rise of two with the sole set
      falling by one is the `add-cpc-clearing-boundary` shape: the archived
      `promote-workflow-gate-contract` was SOLE on the owner-layer key and
      flips, while the archived `add-release-inventory-drift-check` was
      already co-modified and does not. `active_sole` holds because the
      flipped change is ARCHIVED
- [x] 4.2 Measured on both trees AND by exclusion rather than inferred:
      `origin/main` at `0bf37d14` reads `33 active + 125 archived` = 158,
      `109`, `49`, `21 / 12`; this branch reads `34 active + 125 archived` =
      159, `111`, `48`, `22 / 12`; the same sweep on this branch with only
      `openspec/changes/amend-owner-layer-severity/specs/` moved aside reads
      `159`, `109`, `50`, `21 / 13` — main's two co-modified readings exactly,
      which isolates the whole move to those two delta directories
- [x] 4.3 `tests/doc-health/test_modified_block_currency_self_gate.py` — the
      carriage-ledger population gains this packet's two subjects, each with a
      dated note naming the units the block deliberately does not carry and
      why, and each retiring when the packet archives and its blocks are
      promoted

## 5. What this packet MOVES in doc-health, measured

- [x] 5.1 WHILE THE PACKET STOOD ACTIVE: two new `info` findings, both its own
      carriage-ledger rows, and nothing else at any severity. The arm cannot
      distinguish a ruled amendment from stale text and does not claim to; the
      rows ARE the audit trail for the two amendments, and both name exactly
      the units the word-diffs in § 2 name. ON THE LANDED TREE both rows are
      GONE, retired by the promotion on the condition they were written with
      (§ 6.4), so the packet's net effect on the report is ZERO findings at
      every severity
- [x] 5.2 The `modified-block-currency` scenario-title arm — the one that
      gates at `error` — reads ZERO for this packet, both blocks carrying
      every promoted scenario title
- [x] 5.3 No `sibling-pairing` finding is possible: both requirement titles
      are promoted canon, not an active sibling's `## ADDED` block, so this
      packet owes no `Modified over` marker and carries none

## 6. Promotion and archive

PERFORMED IN THE LANDING COMMIT, the shape `2026-08-25-reconcile-lifecycle-books-count`
set for a doc-only packet: `code_surface: none` means the archive gate is
LANDING rather than merged-plus-green, so the promotion and the archive ride
the same pull request as the packet and canon moves in one commit rather than
two.

- [x] 6.1 Promote both deltas into
      `openspec/specs/workflow-gate-contract/spec.md` and
      `openspec/specs/release-surface-integrity/spec.md`, and archive this
      packet to `openspec/changes/archive/2026-09-03-amend-owner-layer-severity/`.
      Executed 2026-09-03 through
      `python3 scripts/proposal-support.py . archive amend-owner-layer-severity --yes`,
      never a bare `openspec archive`: the wrapper runs the origin gate, the
      incomplete-task gate and `openspec validate --strict` BEFORE the act, and
      it is the sanctioned path
- [x] 6.2 Prove the promotion by sha256 rather than asserting it. Each block
      extracted from canon AFTER promotion hashes identical to this packet's
      delta block — `035fb896…bc4ed439` for *Owner layer constraint* and
      `6e102b2e…d02a1d19a` for *The declared bundle describes the release
      surface* — and the post-promotion word-diff against pre-promotion canon
      (`abe58572…77118237`, `4c9e0b71…313f29567`) shows the two ruled words and
      the one dated paragraph and nothing else
- [x] 6.3 Re-run the promotion-fidelity family through the real code path.
      This change is now the latest archived writer of BOTH requirements, so
      the family measures IT against canon from this moment.
      `python3 scripts/doc-health.py --single-repo . --family promotion-fidelity`
      reports `0 critical, 0 error, 0 warning, 0 info` — openxFactory reads
      ZERO, no finding names this packet, and no finding appears anywhere else
- [x] 6.4 The two carriage-ledger subjects added in § 4.3 RETIRE ON THE
      CONDITION THEY WERE WRITTEN WITH — the packet archives and its blocks are
      promoted — and BOTH HALVES ARE VERIFIED BEFORE THE ROWS ARE DELETED, not
      after: the packet is at
      `openspec/changes/archive/2026-09-03-amend-owner-layer-severity/`, the
      promoted requirements are byte-identical to the delta blocks under the
      hashes in § 6.2, and the family excludes `openspec/changes/archive/` in
      its reader by construction, so no finding can name either path this
      packet ever had
- [x] 6.5 Re-measure the `sequenced_after` live pin on both trees after the
      act rather than adjusting § 4.1's numbers by arithmetic. The archive
      moves the packet from the ACTIVE corpus into the ARCHIVED one, so
      `active_co_modified` falls back to 21 while the corpus-wide
      `co_modified` HOLDS at 111 — an archive never un-shares a requirement
      key — which is the shape every archive in that pin's movement log has.
      `change_ids - 1` holds at 158 (moving a change between buckets cannot
      change the total) and `sole_modifiers - 1` holds at 47 (this change was
      always a co-modifier and never a sole one, and the change it flipped was
      already archived). MEASURED ON BOTH SIDES OF THE ACT rather than adjusted
      by arithmetic, via `python3 scripts/validate-sequenced-after.py . --sweep`:
      before the archive the branch read `34 active + 125 archived` = 159 change
      ids, `111`, `48`, `22 / 12`; after it the branch reads
      `33 active + 126 archived` = 159, `111`, `48`, `21 / 12`. EXACTLY ONE PIN
      MOVES, and the pre-archive reading is its own by-exclusion control, the
      archive act being the only difference between the two trees. Both halves
      of the day's movement are recorded in the pin rather than netted, because
      a reader who sees only the net cannot tell an archived packet from one
      that was never authored
- [x] 6.6 Move the README record row from `Active changes:` to
      `Archived changes:` and restate it in the archived voice, the shape the
      precedent set

## 7. Owed elsewhere, not here

- [x] 7.1 `scripts/validate-domain-factory.py` is NOT opened by this change,
      and that is the ruling rather than an omission from it. Nothing is owed
      there: the validator already behaves as the amended canon states
- [x] 7.2 OpsxFactory's three unrelated validator errors, surfaced by the
      2026-09-02 measurement (`tenancy.isolation.subject_context='per_subject'`
      unrecognised; two profiles missing `profile.id`), are that repository's
      own business. Recorded in `design.md` so the measurement is honest, not
      claimed here and not fixed here
