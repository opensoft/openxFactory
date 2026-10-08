# Tasks: amend-factory-mcp-conformance-auth-profile

Status: draft
Kind: tasks
Authored: 2026-10-08, lane `openxfactory-5` (display `openXfactory-5`).

These are governance checkpoints. The single Speckit feature created at 2.1
owns the executable implementation tasks, and this file does not duplicate
them. Boxes for acts that have not happened stay `- [ ]` until their act.
Boxes for work this change will never do carry `[~]`, in § 5.

## 0. Ratification

- [ ] 0.1 Brett Heap's ratify word on this exact packet, including his answer
  to OQ-1 to OQ-6 in `design.md` ("as recommended" adopts all six). The three
  rulings of 2026-10-08 decide what the packet must say. They do not ratify
  it.
- [ ] 0.2 On the word, in one commit: `Status: ratified` plus a `Ratified:`
  line in `proposal.md`; `Status: ratified` plus `Ratified by:` here and in
  `design.md`; the `approved_by`/`approved_on` pair in `.openspec.yaml` (the
  `proposal-origin` family refuses a ratified status without it); a record
  under `review/`; and the README *Active changes* entry updated.

## 1. This packet

- [x] 1.1 Authored: `proposal.md`, `design.md`, this file, `.openspec.yaml`,
  and one delta, `specs/factory-mcp-conformance/spec.md`, with four
  `## ADDED` requirements (15 scenarios) and one `## MODIFIED` requirement
  (3 scenarios). Every requirement has a scenario, and every body states its
  SHALL on its first line.
- [x] 1.2 The MODIFIED block is canon's block (`main` `80f47483`,
  `openspec/specs/factory-mcp-conformance/spec.md`, *Lossless results and
  explicit failures*, 15 lines) with only the narrowed words changed. `diff`
  of canon's block against the delta's reports exactly two hunks, `3c3` (the
  body paragraph: one sentence inserted, one clause qualified) and `10c10`
  (the *Unavailable dependency* WHEN bullet). The title, the THEN bullet, and
  the scenarios *Negative evaluation* and *Existing digested result* are
  byte-identical.
- [x] 1.3 Bookkeeping: one README *Active changes* bullet; the sweep-ledger
  rows in `tests/sequenced_after/corpus-ledger.yaml`, seeded by the sanctioned
  seeder with this packet's pull request number; one `_LEDGER_SUBJECTS` data
  row in `tests/doc-health/test_modified_block_currency_self_gate.py` naming
  this packet's MODIFIED block, which retires at 4.1.
- [x] 1.4 Gates at the packet's head, in a full clone named `openxFactory`
  with the three gitlinks initialized as CI initializes them: the pinned
  OpenSpec CLI (`scripts/validate-openspec-cli-pin.py --all --strict`, and
  `--change`), `scripts/proposal-support.py . verify`,
  `scripts/validate-sequenced-after.py .` (plain and `--ledger-diff`),
  `scripts/validate-code-surface.py .`, `scripts/validate-target-release.py .`,
  doc-health `--single-repo .`, the pytest modules CI runs for these surfaces,
  `git diff --check`, and a closing-keyword scan of every commit and the pull
  request body. The pull request body lists the results. Every red is
  compared with `main` in the same clone kind.

## 2. Realization (one Speckit feature, after 0.1 and never before it)

- [ ] 2.1 Create the Speckit feature from the ratified packet. Its spec and
  plan trace to this delta, and it runs clarify, plan, checklists, tasks and
  analyze.
- [ ] 2.2 Red-first tests in `tests/factory-mcp/`, committed before any schema
  or validator change and shown failing against the validator on `main`:
  - one test per code in `design.md` D7;
  - the scenarios of the four ADDED requirements, including a hosted
    declaration without the block, an algorithm list without RS256, `none`
    and each HMAC name in more than one letter case, an audience bound to
    another resource, and a stdio-only declaration that needs no block;
  - M5: an error-inventory dependency code mapped as a completed evaluation is
    refused, and a result status mapped as an execution failure is refused.
    The enforcement exists already, so these are shown red against a mutant
    of `main`'s validator with the classification comparison removed, and
    green against `main`'s own (`design.md` D8).
  Synthetic identifiers only: no real issuer, tenant, host or domain schema.
- [ ] 2.3 Schema: the `auth` property of the `deployed` service branch, closed
  as `design.md` D1 gives it, and the `auth` key in the evidence and gap
  concern vocabulary. A deployed synthetic example sits beside the existing
  not-deployed one.
- [ ] 2.4 Validator: the checks and stable codes of `design.md` D7, in the
  semantic pass, with the existing ordering and dimensions.
- [ ] 2.5 Runbook: `docs/factory-mcp-conformance.md` gains the block, its
  codes, the stdio rule, the narrowed M5 reading and the per-domain
  vocabulary statement. The "unbundled and unreleased" paragraph moves to the
  release the cut allocates.
- [ ] 2.6 Contract cut, under `docs/contract-versioning-policy.md` § Bundle
  Realization Order. First claim the version number as row 4 on #630. Then,
  in one candidate commit with the schema, add the declaration's manifest row
  with its digest, the `contracts/CHANGELOG.md` entry and
  `contracts/releases/<version>.digests.yaml`. Run `release-tag-gate`, and
  publish the annotated tag after landing.
- [ ] 2.7 Verification record in the feature: every gate, the full suite, and
  an out-of-tree check by a reviewer with access to the engineering domain
  (`--snapshot`, never vendoring its bytes). That check confirms that its
  hosted declaration reports `auth_rs256_missing` until its own slice lands,
  and that its stdio declaration validates as before.

## 3. Landing

- [ ] 3.1 This packet lands on Brett Heap's landing word, after 0.1, under the
  Rule 6 landing window, with every required check green and Copilot's and
  Codex's reviews read at the exact head.
- [ ] 3.2 The realization lands on its own word, merged and green.

## 4. Archive

- [ ] 4.1 After merged, green realization evidence exists (the code surface is
  not empty), and on its own word: archive with `python3
  scripts/proposal-support.py . archive amend-factory-mcp-conformance-auth-profile`
  (never a bare `openspec archive`), landed by merge commit and never by
  squash. Retire this packet's `_LEDGER_SUBJECTS` row, and move the README
  entry to the archive record. Canon then holds twelve requirements.

## 5. Downstream acts this change does NOT perform

- [~] 5.1 **codexFactory's RS256 slice**, lane `openXfactory-5`, as its own
  governed change in that repository. Two notes ride to it from `design.md`.
  The audience binding: its adapter compares `aud` with its canonical resource
  URI, while the estate issuer's tokens carry a client identifier (D3). The
  metadata location: it appends the well-known suffix to the resource URI (D4).
- [~] 5.2 **OpsxFactory's hosting-plan `issuer` correction**: a material
  amendment of the approved hosting plan, with a fresh task 4.2 approval. This
  change supplies the issuer rule that correction meets (`design.md` D4).
- [~] 5.3 **The Ops gateway's intake alignment**, lane `opsXfactory-4`, at
  gateway base task 3.1.
- [~] 5.4 **No shared transport package, server, token minting or client
  registration.** The shared-transport trigger is untouched.
