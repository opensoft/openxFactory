# Proposal Ratification: correct-naming-families-count

Status: ratified
Kind: report
Decision date: 2026-10-07
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-10-07 by Brett Heap (openxFactory operator authority) — in session, first-hand to lane `codeXfactory-5`, verbatim *"ratify as recommended when the PR opens"*, given at about **09:46Z**, logged RULED on the lane register at **2026-10-07T09:47:04Z** (`opensoft/brett-wip` `lanes/log/codeXfactory-5.md`), and effective when `opensoft/openxFactory` PR [#1266](https://github.com/opensoft/openxFactory/pull/1266) opened at **2026-10-07T10:43:48Z**.
Ratified baseline: PR #1266's opening head **`3bb38c20`** (`3bb38c2058b4e1d77a9b47b889ab915dff7f4590`), the head the word names: "when the PR opens". No commit came between it and the ratifying commit.

## Decision

**RATIFY, AS RECOMMENDED.** The packet stands as it was put. That is TWO
`## MODIFIED` requirements in `project-repo-schema`, titles unchanged. *The
naming families are governed by the pinned standard, and a descendant form is
a claim that needs a declared pin* becomes count-free, with one paragraph and
one scenario added and its referent sentence corrected. *A project's
repositories are named `<Project>`, `<Project>-spec` and `<Project>-code`* has
its CamelCase clause corrected. Three canon units are replaced under `Removed
from canon` markers, and every other sentence and all six promoted scenarios
are carried byte-identically. `design.md` and `tasks.md` stand as filed.

**The word is a ratification only.** It is not a merge word: the merge rests on
Brett Heap's separate merge word, *"merge the naming families PR when green"*,
logged RULED at 2026-10-07T09:59:10Z (`tasks.md` 1.2), and it is the
coordinating lane's act. It is not a word to realize anything: the `tasks.md`
§ 5.1 doctrine handoff waits on its own act. Nothing is promoted by it,
because `openspec/specs/` gains nothing until the archive, and the archive
waits for § 5.1 to be merged (`tasks.md` § 6).

**No code byte, pin, gitlink, contract bundle or release tag moves with this
record.**

## 1. The word, and exactly what it decided

> ratify as recommended when the PR opens

"As recommended" takes every recommendation the packet put, as written:

| decision | ruled answer | where it was put |
| --- | --- | --- |
| D1, the reading | the naming families are THOSE the pinned openRepoShape naming policy declares, governed there as data, and canon restates neither their number nor their full list | `tasks.md` 1.1; `design.md` D1 |
| D2, the scope | the correction also reaches the two sentences that restated a property of the whole set: the leg suffixes sit apart from *"every family the pinned standard's naming policy spells as a CamelCase word"*, and `<Domainx><Product>` is no longer *"the one family"* not decided by its characters | `tasks.md` 1.1; `design.md` D2 |
| D3, the doctrine wording | `docs/project-repo-schema.md` is realized as D3 proposes: the heading `## Naming, and the naming families`, the two sentences restated, one INFORMATIVE note dated to the pin, and an `Amended by:` line | `tasks.md` 1.1 and § 5.1; `design.md` D3 |

The packet put no open question. The alternatives `design.md` § D1 rejected
stay rejected: restating "six" (A1), a count tied to the data by a test (A2),
and a dated count in canon (A3).

## 2. Why no delta byte moves

Every ruling is the recommended option, and the spec delta already encodes
each one. D1 and D2 are the delta's text. D3 governs the doctrine document,
which the delta does not touch. So `specs/project-repo-schema/spec.md` is
byte-identical to the text put to ratification.

## 3. What the ratifying commit moves

- `proposal.md`: `Status: ratified` with a `Ratified:` citation; a qualifier
  above the filing's "NOTHING HERE IS RATIFIED" paragraph, which is kept
  verbatim as the filing's record; a RULED mark on each item of "What
  ratification decides"; a `## Ratification record` section with the rulings
  table; and the `code_surface:` gloss's file list corrected for this record
  (the head `none` is unchanged).
- `design.md` and `tasks.md`: `Status: ratified` with a `Ratified by:`
  citation. `design.md` gets a ratification qualifier above its opening
  paragraph, which is kept as filed, and a RULED mark on D1, D2 and D3 with
  their reasoning kept. `tasks.md` gets dated notes on owner boxes 1.1 and 1.2,
  and 1.3, the bookkeeping this commit performs, is ticked.
- `.openspec.yaml`: `approved_by` / `approved_on` are ADDED after
  `proposed_on`. `kind`, `id`, `reason`, `proposed_by` and `proposed_on` do not
  move.
- This record, and the README *Active changes* entry's status.

**Not moved:** `specs/project-repo-schema/spec.md`, and
`tests/sequenced_after/corpus-ledger.yaml`. The packet's row stays
`state: active`, `class: co-modifier`, and `--ledger-diff` reads it consistent.

## 4. Encodings, and why

- **The origin pair is spelled `approved_by` / `approved_on`.** That is
  openxFactory's proposal-origin contract: its approval pair is
  `APPROVAL_FIELDS = ("approved_by", "approved_on")`
  (`scripts/doc_health/proposal_origin.py`), and an `ad_hoc` origin under
  `Status: ratified` without that pair is reported as an error. The pair is
  added in this ratifying commit, which is the first commit to declare
  `Status: ratified` anywhere in the packet.
- **Owner boxes 1.1 and 1.2 are not ticked.** `tasks.md` § 1 says those are
  OWNER BOXES that "an agent never ticks", and an agent encoded this word. So
  each carries a dated note recording the word, and each is left for its owner.
- **The citation is the lane register, not a pull-request comment.** The word
  was given in session before the pull request existed, and it was logged on
  the lane register at 09:47:04Z. The RATIFIED comment on PR #1266 follows this
  commit and quotes the same word.

## 5. Verification

Measured on the encoded tree against clean `main` **`16779816`** and against the
opening head **`3bb38c20`**. doc-health and pytest ran in a scratch checkout
named `openxFactory`, with the submodules CI's `pytest-suite` initializes
(`openXwallet`, `openXdox`, `openDox`, recursively), so the repository identity
and the skipped-family set match CI.

- **Pinned OpenSpec CLI** (`@fission-ai/openspec@1.12.0`, content address
  verified):
  - `--change correct-naming-families-count --strict`: 1 passed, 0 failed.
  - `--all --strict`: **113 passed, 1 failed (114 items), exit 0**, against
    clean `main` at 112 passed, 1 failed (113 items), exit 0. Every finding
    line is identical on the two trees.
  - The one failure is not this packet's: the `add-chain-attestation`
    exception that `contracts/openspec-cli-pin.yaml` already accepts.
- **House validators, each exit 0:**
  - `validate-sequenced-after.py .`;
  - `--ledger-diff`: "consistent with the corpus (233 rows)";
  - `validate-code-surface.py .`;
  - `validate-target-release.py .`;
  - `proposal-support.py . verify correct-naming-families-count`: "proposal
    support verification ok".
- **doc-health** (`scripts/doc-health.py --single-repo . --as-of 2026-10-07`):
  clean `main`, the opening head and the encoded tree each report **31
  critical, 26 error, 69 warning, 19 info**, and the three reports are
  byte-identical. No finding names any file of this packet, this record
  included, in any family (`proposal-origin`, `ratified-provenance`,
  `status-validity` and `modified-block-currency` among them).
- **pytest** on the encoded tree, over every directory that reads the change
  corpus, the README, the ledger or the pins (`sequenced_after`, `code_surface`,
  `target_release`, `scope_globs`, `proposal-support`, `packet_reference`,
  `citation_remainder`, `former_id_arrival`, `estate_inventory`,
  `openspec_cli_pin`, `openreposhape_pin`, `intent-compliance`,
  `conformance-gate`, `pin_registrations`, `doc-health`), `-m "not postgres"`:
  **3872 passed, 2 skipped, 0 failed, exit 0**, the same counts as at the
  opening head. The full suite is CI's `pytest-suite`.
- **Spec delta:** `git diff 3bb38c20 -- openspec/changes/correct-naming-families-count/specs`
  is empty.
