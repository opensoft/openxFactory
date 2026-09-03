# Tasks: Amend The Owner-Layer Severity, And Date The Retro-Tagged Bundles

## 1. Establish both defects and the lawful fix

- [x] 1.1 Read both issues in full, including every comment, before authoring:
      #561 (the canon/validator severity divergence, commissioned by
      `retire-hermes-flat-keys-and-openworkflow-tokens` tasks § 6.1) and #339
      (the three retro-tagged bundles left in the present tense). The ruling
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
      `find openspec/changes -mindepth 3 -path '*/specs/workflow-gate-contract/*'
      -o -path '*/specs/release-surface-integrity/*' -not -path '*archive*'`
      returns nothing, re-run after refreshing to `origin/main` at `0bf37d14`.
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
      baseline at the same commit, and the finding sets diffed: ZERO new
      `critical`, `error` or `warning` findings. The `info` rows this packet
      adds are its own carriage-ledger rows and are enumerated in § 5
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

- [x] 5.1 Two new `info` findings, both this packet's own carriage-ledger
      rows, and nothing else at any severity. The arm cannot distinguish a
      ruled amendment from stale text and does not claim to; the rows ARE the
      audit trail for the two amendments, and both name exactly the units the
      word-diffs in § 2 name
- [x] 5.2 The `modified-block-currency` scenario-title arm — the one that
      gates at `error` — reads ZERO for this packet, both blocks carrying
      every promoted scenario title
- [x] 5.3 No `sibling-pairing` finding is possible: both requirement titles
      are promoted canon, not an active sibling's `## ADDED` block, so this
      packet owes no `Modified over` marker and carries none

## 6. Promotion and archive

- [ ] 6.1 Promote both deltas into
      `openspec/specs/workflow-gate-contract/spec.md` and
      `openspec/specs/release-surface-integrity/spec.md` through
      `openspec archive`, and archive this packet. `code_surface: none`, so
      the archive gate is LANDING and not merged-plus-green — but the act is
      still an act, and it is deliberately NOT performed on an unmerged
      branch. Owed at landing
- [ ] 6.2 After promotion, re-run the promotion-fidelity family: this change
      becomes the latest archived writer of BOTH requirements, so the family
      measures it from that moment and must read zero findings for
      openxFactory
- [ ] 6.3 After promotion, the two carriage-ledger subjects added in § 4.3
      RETIRE — the blocks are canon rather than active deltas — and the
      `sequenced_after` pin's `active_co_modified` falls by one while the
      corpus-wide `co_modified` holds, the shape every archive in that pin's
      movement log has

## 7. Owed elsewhere, not here

- [x] 7.1 `scripts/validate-domain-factory.py` is NOT opened by this change,
      and that is the ruling rather than an omission from it. Nothing is owed
      there: the validator already behaves as the amended canon states
- [x] 7.2 OpsxFactory's three unrelated validator errors, surfaced by the
      2026-09-02 measurement (`tenancy.isolation.subject_context='per_subject'`
      unrecognised; two profiles missing `profile.id`), are that repository's
      own business. Recorded in `design.md` so the measurement is honest, not
      claimed here and not fixed here
