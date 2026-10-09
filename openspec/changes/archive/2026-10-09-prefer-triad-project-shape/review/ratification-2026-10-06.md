# Proposal Ratification: prefer-triad-project-shape

Status: ratified
Kind: report
Decision date: 2026-10-06
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-10-06 by Brett Heap (openxFactory operator authority) — in session, first-hand to lane `codeXfactory-5`, verbatim *"ratify 1249 as recommended"*, given at **2026-10-06T16:02:16Z** and recorded on `opensoft/openxFactory` PR [#1249](https://github.com/opensoft/openxFactory/pull/1249) comment [`6020300563`](https://github.com/opensoft/openxFactory/pull/1249#issuecomment-6020300563).
Ratified baseline: PR #1249's head **`8f9c5855`**, the head every required check had passed on when the word was given. Its packet text equals `2ee9ffd8`'s; the merge from `main` at `8f9c5855` touched no packet byte.

## Decision

**RATIFY, AS RECOMMENDED.** The packet stands as it was put. That is ONE
`## MODIFIED` requirement in `project-repo-schema` — *The project repository
schema is elective and confers nothing*, every canon sentence and scenario
carried byte-identically — and THREE `## ADDED` requirements, with twenty
scenarios in all, plus `design.md` and `tasks.md` as filed.

**The word is a ratification only.** It is not a merge word, and PR #1249 stays
held for Brett Heap's merge word. It is not a word to realize anything: each
`tasks.md` § 5 handoff waits on its own owner's act. Nothing is promoted by it,
because `openspec/specs/` gains nothing until the archive, and under
`release-realization` the archive waits for merged, green realization evidence
on every surface `tasks.md` § 5 names (`tasks.md` § 6).

**No code byte, pin, gitlink, contract bundle or release tag moves with this
record.**

## 1. The word, and exactly what it decided

> ratify 1249 as recommended

"As recommended" takes every recommendation the packet put, as written:

| question | ruled answer | where it was put |
| --- | --- | --- |
| the reading | the Triad is PREFERRED and not required; it is advised where a person starts work, once per session, and never stops anyone; it is never a review input | `tasks.md` 1.1; `design.md` D1-D3 |
| OQ-1 | the optional staying-single record is `single-repository.yaml` at the repository root, and openRepoShape owns its schema | `tasks.md` 1.2; `design.md` D4 |
| OQ-2 | no class-guessing: aggregations, configuration and dotfile repositories, and vendored forks get the advisory until they migrate or record staying single | `tasks.md` 1.3; `design.md` D4 |
| OQ-3 | the advisory restates the doctrine's preference and is not codexFactory's "act of RECOMMENDING the shape", so no `## MODIFIED` block is written on the ownership requirement | `tasks.md` 1.4; `design.md` D6 |

The alternatives `design.md` § Alternatives rejected (A1 a warning in review or
CI, A2 a mandatory Triad, A3 per-person suppression, A4 a blocking prompt)
stay rejected.

## 2. Why no delta byte moves

Every ruling is the recommended option, and the spec delta already says what
each ruling decides. Its third ADDED requirement describes the staying-single
record without naming a file, which is what OQ-1 decides, so the file name
lives in `design.md` and in the `tasks.md` § 5.2 handoff and not in the spec.
The same requirement already refuses class-guessing (OQ-2). And the delta
carries no block on the ownership requirement (OQ-3). So
`specs/project-repo-schema/spec.md` is byte-identical to the text put to
ratification.

## 3. What the ratifying commit moves

- `proposal.md`: `Status: ratified` with a `Ratified:` citation; a qualifier
  above the filing's "NOTHING HERE IS RATIFIED" paragraph, which is kept
  verbatim as the filing's record; a RULED mark on each item of "What
  ratification decides"; a `## Ratification record` section with the rulings
  table; and the `code_surface:` gloss's file count corrected for this record.
- `design.md` and `tasks.md`: `Status: ratified` with a `Ratified by:`
  citation. `design.md` gets a ratification qualifier above its opening
  paragraph, which is kept as filed, and a RULED mark on OQ-1, OQ-2 and OQ-3
  with their reasoning kept. `tasks.md` gets a dated note on owner boxes
  1.1-1.5, and 1.6, the bookkeeping this commit performs, is ticked.
- `.openspec.yaml`: `approved_by` / `approved_on` are ADDED after
  `proposed_on`. `kind`, `id`, `reason`, `proposed_by` and `proposed_on` do not
  move.
- This record, and the README *Active changes* entry's status.

**Not moved:** `specs/project-repo-schema/spec.md`, and
`tests/sequenced_after/corpus-ledger.yaml`. The packet's row stays
`state: active`, `class: co-modifier`, and `--ledger-diff` reads it consistent.

## 4. Two encodings that differ from the request, and why

- **The origin pair is spelled `approved_by` / `approved_on`.** The encoding
  request and the RATIFIED comment on PR #1249 name `ratified_by` /
  `ratified_on`. openxFactory's proposal-origin contract has no such keys: its
  approval pair is `APPROVAL_FIELDS = ("approved_by", "approved_on")`
  (`scripts/doc_health/proposal_origin.py`). An `ad_hoc` origin under
  `Status: ratified` without that pair is reported as an error ("approval MUST
  appear when the status claims it"). Both precedents spell it this way:
  `amend-register-act-5b-projection-proof` (`5daa96ec`) and
  `add-neutral-product-standalone-operability` (`cd494e4c`). So the request's
  purpose — the approval INSIDE the origin, in the ratifying commit itself, so
  the archive gate's origin-retention baseline carries it — is met in the
  contract's own spelling.
- **Owner boxes 1.1-1.4 are not ticked.** Both precedents ticked their
  ratification boxes in the encoding commit. But this packet's `tasks.md` § 1
  heading says those are OWNER BOXES that "an agent never ticks", and an
  agent encoded this word. So each box carries a dated note recording the word
  and its ruling, and is left for its owner. Ticking a box later moves no
  origin byte.

## 5. Verification

Measured on the encoded tree against clean `main` **`51456835`** and against the
pre-encode head **`8f9c5855`**. doc-health ran in a checkout named
`openxFactory`, with the submodules CI initializes, so the repository identity
and the skipped-family set match CI.

- **Pinned OpenSpec CLI** (`@fission-ai/openspec@1.12.0`, content address
  verified):
  - `--change prefer-triad-project-shape --strict`: 1 passed, 0 failed.
  - `--all --strict`: **113 passed, 1 failed (114 items), exit 0**, against
    clean `main` at 112 passed, 1 failed (113 items), exit 0.
  - The one failure is the same on both trees and is not this packet's: the
    `add-chain-attestation` exception that `contracts/openspec-cli-pin.yaml`
    already accepts.
- **House validators, each exit 0:**
  - `validate-sequenced-after.py .`;
  - `--ledger-diff`: "consistent with the corpus (232 rows)";
  - `validate-code-surface.py .`;
  - `validate-target-release.py .`;
  - `proposal-support.py . verify prefer-triad-project-shape`: "proposal support
    verification ok".
- **doc-health** (`scripts/doc-health.py --single-repo .`): clean `main`, the
  pre-encode head and the encoded tree each report **31 critical, 26 error, 69
  warning, 20 info**. Their finding lines are byte-identical: the diff is empty
  pre-to-post and main-to-post. No finding names any file of this packet,
  this record included, in any family (`proposal-origin`,
  `ratified-provenance`, `status-validity` and `modified-block-currency`
  among them).
- **pytest** on the encoded tree, over every directory that reads the change
  corpus, the README, the ledger or the pins (`sequenced_after`, `code_surface`,
  `target_release`, `scope_globs`, `proposal-support`, `packet_reference`,
  `citation_remainder`, `former_id_arrival`, `estate_inventory`,
  `openspec_cli_pin`, `openreposhape_pin`, `intent-compliance`,
  `conformance-gate`, `pin_registrations`, `doc-health`), `-m "not postgres"`:
  **3872 passed, 2 skipped, 0 failed, exit 0**. The full suite is CI's
  `pytest-suite`.
- **Spec delta:** `git diff 8f9c5855 -- openspec/changes/prefer-triad-project-shape/specs`
  is empty.
