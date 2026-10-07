# Tasks: prefer-triad-project-shape

Status: ratified
Ratified by: prefer-triad-project-shape — 2026-10-06, Brett Heap, "ratify 1249 as recommended" (PR #1249 comment 6020300563), over PR #1249's head `8f9c5855` (record `review/ratification-2026-10-06.md`)
Kind: tasks

OpenSpec records the governed decision and the handoff; Speckit owns the
implementation tasks. So § 1 is the owner's acts, §§ 2-4 are what this packet
itself authored and measured, and § 5 is HANDOFF and EVIDENCE boxes for work
other owners perform after ratification, each in its own repository and, where
it is implementation, in its own Speckit feature. None of § 5 is an
implementation step this packet takes.

## 1. Ratification — 1.1-1.5 are OWNER BOXES, and an agent never ticks them

Each is ticked only on Brett Heap's own recorded word, by whoever encodes that
word, citing it. 1.6 is the bookkeeping that follows the ratifying word and
never precedes it.

- [ ] 1.1 OWNER BOX. Brett Heap's word on the reading this packet encodes: the
  Triad is PREFERRED and not required; it is advised where a person starts
  work, once per session, and never stops anyone; and it is never a review
  input (`design.md` D1-D3). His sentences of 2026-10-06 are the direction and
  the authority to author and open this packet. They are not this word.
  **NOTE 2026-10-06 — THE WORD WAS GIVEN:** Brett Heap, 2026-10-06T16:02:16Z,
  in session, verbatim *"ratify 1249 as recommended"* (PR #1249 comment
  6020300563; record `review/ratification-2026-10-06.md`). It ratifies the
  reading as written. The box is left for its owner to tick, as this section's
  heading says.
- [ ] 1.2 OWNER BOX. OQ-1, the staying-single record's file name, location and
  schema (`design.md` D4). Recommendation: `single-repository.yaml` at the
  repository root, `schema_version: 1`, `kind: single-repository-record`,
  `decided_by`, `decided_on`, `reason`, optional `revisit_on`, schema owned by
  openRepoShape; never a field of `project.yaml`, which is the Triad detector.
  **NOTE 2026-10-06 — RULED, as recommended**, by the same word:
  `single-repository.yaml` at the repository root, schema owned by
  openRepoShape. Box left for its owner.
- [ ] 1.3 OWNER BOX. OQ-2, aggregation, configuration and dotfile repositories
  and vendored forks (`design.md` D4). Recommendation: no class-guessing; they
  receive the advisory until they migrate or record staying single.
  **NOTE 2026-10-06 — RULED, as recommended**, by the same word: no
  class-guessing. Box left for its owner.
- [ ] 1.4 OWNER BOX. OQ-3, whether the advisory re-homes the act of
  recommending the shape that `project-repo-schema` gives codexFactory
  (`design.md` D6). Recommendation: it does not, and no block is written on that
  requirement.
  **NOTE 2026-10-06 — RULED, as recommended**, by the same word: the advisory
  is not codexFactory's act of recommending the shape, and no block is written
  on the ownership requirement. Box left for its owner.
- [ ] 1.5 OWNER BOX. Brett Heap's merge word on this pull request. It is held
  for that word and is not merged by the authoring lane.
  **NOTE 2026-10-06 — NOT GIVEN.** The ratifying word is not a merge word;
  this box waits for one.
- [x] 1.6 On the ratifying word, and only then: `Status: ratified` + `Ratified:`
  in `proposal.md`, `Ratified by:` in `design.md` and this file, the
  `approved_by`/`approved_on` pair in `.openspec.yaml` ADDED BESIDE the drafting
  provenance and never substituted for it (`scripts/doc_health/proposal_origin.py`
  requires the pair the moment the status claims approval), a record under
  `review/`, and the README Records row moved with it.
  **DONE 2026-10-06 in the ratifying commit**, on the word above: all of it,
  with the record at `review/ratification-2026-10-06.md`. `kind`, `id`,
  `reason`, `proposed_by` and `proposed_on` did not move, and the spec delta
  did not move.

## 2. The packet

- [x] 2.1 `specs/project-repo-schema/spec.md`: ONE `## MODIFIED` requirement,
  *The project repository schema is elective and confers nothing*, carrying both
  promoted body paragraphs and all THREE promoted scenarios byte-identically and
  adding three paragraphs (the preference, the name, the posture-with-preference
  rule) and TWO scenarios; THREE `## ADDED` requirements — the advisory (five
  scenarios), never a review input (four), and the advisory's scope with the
  optional record (six). Twenty scenarios in the file.
- [x] 2.2 `.openspec.yaml`: `kind: ad_hoc`, id
  `openxFactory:adhoc:2026-10-06-prefer-triad-project-shape`, the unapproved
  shape `add-drafted-proposal-origin` admits (`proposed_by`/`proposed_on`, no
  approval pair), Brett Heap's two sentences verbatim with their UTC times,
  session `ed23f049-7e99-4601-8a6d-760b6aeb5f26`, lane `codeXfactory-5`.
  Written by hand in the block shape `scripts/proposal-support.py
  declare-adhoc` writes, because that command derives the id's repository
  segment from the checkout directory's name and this packet was authored in a
  worktree whose directory is not named `openxFactory`.
- [x] 2.3 README *Active changes*: one bullet.
- [x] 2.4 The per-change sweep ledger row, seeded by the sanctioned seeder
  (`scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#1249'`,
  this pull request): `active`, `co-modifier`, `declares: absent`. Exactly one
  row moved, this packet's own; `co-modifier` because the requirement key it
  writes was also written by the archived `add-project-repo-schema`, whose row
  was already `co-modifier` and does not move.

## 3. Measurement — each re-runnable, each taken on `main` `92010d3e`

- [x] 3.1 CARRIAGE: `diff <(sed -n 24,40p <delta>) <(sed -n 16,32p
  openspec/specs/project-repo-schema/spec.md)` and `diff <(sed -n 63,76p
  <delta>) <(sed -n 34,47p openspec/specs/project-repo-schema/spec.md)` both
  print nothing: the two body paragraphs and the three scenarios are
  byte-identical to canon.
- [x] 3.2 No active change carries a delta on `project-repo-schema`: the only
  delta file under `openspec/changes/` naming it is the archived
  `2026-09-03-add-project-repo-schema`.
- [x] 3.3 `ideation/staging/` searched for `triad`, `project-repo-schema`,
  `openreposhape`, `three-repository` and `three-leg`: three files match
  (`INDEX.md`, `wallet-carried-work-authority/`, `opendox-two-layer-product/`)
  and none proposes a preference, so the origin is `ad_hoc`.
- [x] 3.4 Triads: of the 22 submodule repositories the aggregation has checked
  out, three carry `project.yaml` with `kind: project-manifest`,
  `schema: project-repo-schema` and both legs — `openDox`, `openXdox`,
  `MedxEHR` — and 19 carry neither `project.yaml` nor `family.yaml`
  (`design.md` D7).
- [x] 3.5 Code-surface membership: `scripts/estate-repository-inventory.yaml`
  carries `opensoft/openRepoShape` and does not carry `opensoft/workBenches`,
  `opensoft/openRepoProject` or the private protocol source (`design.md` D9).
- [x] 3.6 Doctrine-edit precedent: `amend-register-act-5b-projection-proof`
  proposed `07b72078`, ratified `5daa96ec`, document realized `0446dece`;
  `split-ideation-book-per-repo` proposed `95ba14c3`, ratified `201e5bc5`,
  document realized `d2fcae43`; no `amend-*` proposal commit in the corpus
  edits a file under `docs/` (`design.md` D8).
- [x] 3.7 Every realization path in § 5 exists on its repository's `main`,
  read through the GitHub API on 2026-10-06. openRepoShape (`main`
  `39d5c986`): `README.md`, `AGENTS.md` (§ "What you must not tell them"),
  `templates/assembly-root/project.yaml`, `scaffold-project.py`,
  `adopt-project.py`, `shape-doctor.py`. workBenches:
  `devBenches/base-image/files/openspeckit/setup-openspeckit` (with
  `resolve_project_shape()` logging `shape: single repository`, and
  `openspec_speckit_protocol()`), `devBenches/devcontainer.test/test-openspeckit-bootstrap.sh`,
  `openspec/changes/project-command/`, `scripts/new-project.sh`; issue #22 OPEN.
  openxFactory: `docs/project-repo-schema.md`,
  `contracts/schemas/project-register.schema.yaml`,
  `contracts/openreposhape-pin.yaml`. The private protocol source is named by
  file and section only and was not read through the API.

## 4. Gate

- [x] 4.1 Pinned OpenSpec CLI (`@fission-ai/openspec@1.12.0`, content address
  verified), from the worktree root. `python3 scripts/validate-openspec-cli-pin.py
  --change prefer-triad-project-shape --strict`: **1 passed, 0 failed**, no
  info lines. `--all --strict`: **112 passed, 1 failed (113 items), exit 0**,
  against clean `main` `92010d3e` at **111 passed, 1 failed (112 items), exit 0**.
  The one failure is the same on both trees and is not this packet's:
  `add-chain-attestation`'s MODIFIED block, an ACCEPTED EXCEPTION that
  `contracts/openspec-cli-pin.yaml` `dispositions:` already carries (Brett
  Heap, 2026-09-05, "take exit 2").
- [x] 4.2 Each exits 0: `scripts/validate-code-surface.py .` (every identifier
  in the head carried by the estate inventory), `scripts/validate-target-release.py .`,
  `scripts/validate-sequenced-after.py .`, the same with `--ledger-diff`
  ("consistent with the corpus (231 rows)"), and `scripts/proposal-support.py .
  verify prefer-triad-project-shape` ("proposal support verification ok").
  `scripts/doc-health.py --single-repo` over this tree against the same run on
  clean `main` in the same directory: no finding names any file of this packet
  or its README bullet, in any family (`proposal-origin`,
  `modified-block-currency`, `status-validity` and `ratified-provenance`
  included). The only difference between the two reports is one `info`
  finding of `release-tag-publication` about `contract-v2.6`, a family the
  `main` run skipped because the network was down when it ran.
- [ ] 4.3 Required checks green at the pull request's head, the Codex review
  requested and read, every thread answered.

**§§ 1, 4.3, 5 and 6 KEEP A LITERAL `- [ ]` DELIBERATELY.** They are acts that
have not happened, and each is ticked by the act that performs it, never by the
authoring lane.

## 5. Realization handoffs — NOT performed by this packet

Each is its owner's act, after ratification, in its own repository and through
that repository's own governance and claims. The evidence each box owes is a
merged pull request (or, for the private source, a merged commit cited by sha)
with green checks.

- [x] 5.1 **openxFactory, the doctrine.** `docs/project-repo-schema.md`
  restated: the Triad is preferred, the shape still confers nothing, and where
  the advisory is and is not given; plus an `Amended by:
  prefer-triad-project-shape (ratified <date>)` header line (`design.md` D8).
  `contracts/schemas/project-register.schema.yaml`: its `description` restates
  the preference beside the posture it already restates. The register gains no
  field.
  **DONE 2026-10-06** in openxFactory PR
  [#1254](https://github.com/opensoft/openxFactory/pull/1254) →
  `31e0628a327b59341bf9d56136f3e0b534e1a9c6`, lane `codeXfactory-5`.
  `docs/project-repo-schema.md` gains the header line `Amended by:
  prefer-triad-project-shape (ratified 2026-10-06T16:02:16Z, openxFactory PR
  #1249)` and a new § The Triad is PREFERRED, and it still confers NOTHING. That
  section states the preference, the name and the posture beside it; where the
  advisory is given (once, at work start, never blocking or converting); that
  it is never a review input; the five silent cases; and the optional
  `single-repository.yaml`. No existing sentence is edited.
  `contracts/schemas/project-register.schema.yaml` gains one `description`
  paragraph that restates the preference beside the posture. Every existing
  paragraph and every other key is unchanged, and no field is added. Neither
  file is a registered release member, so no digest, inventory member or
  changelog entry moves. The tick holds on `main` only through that pull
  request's merge, which waits on Brett Heap's merge word and its required
  checks.
- [x] 5.2 **`opensoft/openRepoShape`, the mechanics.** The README posture box;
  AGENTS.md § "What you must not tell them", which must still forbid saying the
  shape confers anything and must gain what to tell them — the Triad is the
  preferred shape, and choosing a single repository is reviewed identically; the
  posture comment in `templates/assembly-root/project.yaml`; the optional
  staying-single record's schema and template (as OQ-1 is ruled: RULED
  2026-10-06, `single-repository.yaml` at the repository root); and the
  advisory in `scaffold-project.py`, `adopt-project.py` and `shape-doctor.py`,
  with no exit status changed on its account. Whoever takes this claims it in
  openRepoShape first.
  **DONE 2026-10-06** in opensoft/openRepoShape PR
  [#164](https://github.com/opensoft/openRepoShape/pull/164) →
  `1a9fc537bcce37301c85fc108fabd8a599b02000` (squash, merged
  2026-10-06T22:52:05Z), lane `codeXfactory-5`. It changes `README.md`,
  `AGENTS.md`, `templates/assembly-root/AGENTS-shape.md` and the posture
  comment in `templates/assembly-root/project.yaml`; adds the staying-single
  record's schema `contracts/single-repository-record.yaml` and its template
  `templates/single-repository/single-repository.yaml`; and gives the advisory
  to `scaffold-project.py`, `adopt-project.py` and `shape-doctor.py` out of the
  new `scripts/shape_advisory.py`. Checks green: tests, tests-macos,
  tests-windows and SonarCloud. Full suite (`python3 -m pytest tests -q -rs`):
  1159 passed, 33 skipped on clean `main` `39d5c986`; 1200 passed, 33 skipped
  at the final head `ff739588`. This tick is recorded in openxFactory PR
  [#1260](https://github.com/opensoft/openxFactory/pull/1260)
  and holds on `main` only through that pull request's merge, which waits on
  Brett Heap's merge word and its required checks.
- [x] 5.3 **openxFactory, the pin.** `contracts/openreposhape-pin.yaml`
  advanced onto the openRepoShape commit that realizes 5.2, every new file
  classified by the pin's own digested-or-path-only rule, and
  `openreposhape-pin-gate` green. Measured on 2026-10-06: the pin names
  `e9c4827b`, openRepoShape `main` is 56 commits ahead of it, and
  `shape-doctor.py` does not exist at the pinned commit, so this advance also
  carries everything those 56 commits brought. After 5.2.
  **DONE 2026-10-06** in openxFactory PR
  [#1260](https://github.com/opensoft/openxFactory/pull/1260) →
  `9af2207125d0cf4449ae68f600112b9b1d2b36bb`, lane `codeXfactory-5`.
  `contracts/openreposhape-pin.yaml` advances from `e9c4827b` to
  `1a9fc537bcce37301c85fc108fabd8a599b02000`, the commit that realizes 5.2,
  and so carries the 56 openRepoShape commits before it. Of the 28 files new
  since `e9c4827b`, each classified by the pin's own digested-or-path-only
  rule, 6 are digested and 22 path-only, for 37 digested and 67 path-only
  members over a 104-file surface; 21 of the 31 earlier digests moved, and
  nothing was removed or renamed upstream.
  `scripts/validate-openreposhape-pin.py --checkout` at `1a9fc537`: 37 digests
  recomputed, 67 members present, 104 files declared with none undeclared;
  `openreposhape-pin-gate` green on that commit, run
  [37550154276](https://github.com/opensoft/openxFactory/actions/runs/37550154276),
  with the same counts. `docs/project-repo-schema.md` gains a dated currency
  note, and the verifier's tests move with the pin. The pin is neither a
  registered manifest member nor a release-inventory member, so no digest,
  inventory member or changelog entry moves. The tick holds on `main` only
  through that pull request's merge, which waits on Brett Heap's merge word and
  its required checks.
- [x] 5.4 **`opensoft/workBenches`, the bootstrap.** In
  `devBenches/base-image/files/openspeckit/setup-openspeckit`,
  `resolve_project_shape()` — which today only logs `shape: single repository`
  — gains the advisory: a warning in a non-interactive run with the exit status
  unchanged, a question with "continue" as the default in an interactive
  terminal, and silence in every case the third ADDED requirement exempts; with
  tests in `devBenches/devcontainer.test/test-openspeckit-bootstrap.sh`. The
  existing governing record is workBenches issue #22. THEN, after 5.5 lands, the
  embedded fallback protocol `openspec_speckit_protocol()` — an f-string, so its
  braces are doubled — re-synced byte-identical to the shared protocol.
  **DONE 2026-10-06** in opensoft/workBenches PRs
  [#139](https://github.com/opensoft/workBenches/pull/139) →
  `9fbe609c977573f3d077240c771f7cac7665fab0` (the advisory in
  `setup-openspeckit` at bootstrap) and
  [#140](https://github.com/opensoft/workBenches/pull/140) →
  `d86ba59b1c81b777d05a7a5457553f3e9895432c` (after 5.5: the embedded protocol
  fallbacks re-synced, D001-D003, plus D004: `n` or `no` at the Triad question
  stops the run, as ratified design D2 says), lane `codeXfactory-5`.
  `devBenches/devcontainer.test/test-openspeckit-bootstrap.sh`: 1042 PASS,
  0 FAIL. Post-merge `main` CI green at `d86ba59b` (OpenSpeckit Bash on push,
  and CodeQL). The governing issue, workBenches#138, is closed as completed.
  This tick is recorded in openxFactory PR
  [#1260](https://github.com/opensoft/openxFactory/pull/1260)
  and holds on `main` only through that pull request's merge, which waits on
  Brett Heap's merge word and its required checks.
- [x] 5.5 **The shared agent protocol.** Its source is the PRIVATE repository
  `brettheap/new-workstation`, under `home/.agents/`, deployed per workstation.
  Surfaces: `AGENTS.md` (the shape bullet), `protocols/openspec-speckit-workflow.md`
  § "Repository Shape" / "Detecting the shape" (the once-per-session advisory,
  who says it, and the exemptions), and `protocols/project-agent-bootstrap.md`
  (what the bootstrap prints and asks). Its evidence is cited by commit sha and
  file name only; nothing from that repository is quoted here.
  **DONE 2026-10-06** in the PRIVATE source `brettheap/new-workstation`, cited
  by merged commit sha and file name only: #52 →
  `e081c5ab1166f0bbfd252973f32f21fa4c979131` (`home/.agents/AGENTS.md`,
  `home/.agents/protocols/openspec-speckit-workflow.md` and
  `home/.agents/protocols/project-agent-bootstrap.md`) and #53 →
  `cb4114602826efe0f4829d1cb4695b17d11beb2b`
  (`home/.agents/protocols/project-agent-bootstrap.md`), lane
  `codeXfactory-5`. That repository runs no CI. Both are deployed: the three
  files in the live `~/.agents` are byte-identical to `cb411460`'s. This tick
  is recorded in openxFactory PR
  [#1260](https://github.com/opensoft/openxFactory/pull/1260)
  and holds on `main` only through that pull request's merge, which waits on
  Brett Heap's merge word and its required checks.
- [ ] 5.6 **New-project creation offers the Triad first.** workBenches'
  `openspec/changes/project-command` (`scripts/new-project.sh`, `onp`) is held by
  lane `project-command` and forwards creation to `opensoft/openRepoProject`'s
  `project new`, whose `--shape` mode is opt-in today. The Triad-first offer
  routes THROUGH that lane's claim and openRepoProject's own governance, never
  around them; no repository is created that the person has not confirmed.
- [x] 5.7 **The estate inventory, a recommendation only** (`design.md` D7). For
  each repository in `scripts/estate-repository-inventory.yaml`, measured on its
  own `origin/main`: Triad, leg, family holder, workspace repository or single
  repository, and for each single repository a recommendation — migrate, or
  record staying single — for its owner. It converts nothing and records nothing
  on any repository's behalf. If ratification drops it, this box becomes `[~]`
  with the ruling cited.
  **DONE 2026-10-06** in openxFactory PR
  [#1255](https://github.com/opensoft/openxFactory/pull/1255), lane
  `codeXfactory-5`. The record is
  [`review/estate-inventory-2026-10-06.md`](review/estate-inventory-2026-10-06.md).
  All 37 rows were measured on their own `main`, and none went unmeasured.
  Classes: 3 Triads, 6 legs, 0 family holders, 0 workspace repositories and 28
  single repositories. Recommendations to the owners of those 28: migrate 12
  and record staying single 15. For the 1 `external` row (`Fission-AI/OpenSpec`,
  which the inventory defines as "NOT of this estate at all") none is made,
  and the record states this as a departure from "for each single repository a
  recommendation". They are recommendations only; nothing was converted or
  recorded on any repository's behalf. The tick holds on `main` only through
  that pull request's merge, which waits on Brett Heap's merge word and its
  required checks.

ORDER: 5.3 after 5.2; 5.4's fallback re-sync after 5.5. 5.1, 5.2, 5.4's
advisory, 5.5 and 5.6 are independent of one another.

## 6. Archive

- [ ] 6.1 Archive ONLY on merged plus green realization evidence across § 5 —
  the code surface is not empty, so `release-realization` holds the archive
  until then, and not on landing. The boxes for the three surfaces outside the
  `code_surface:` head — workBenches, openRepoProject and the private protocol
  source — are checked by the archiving actor and each one's evidence is cited
  in the archive record (`design.md` D9).
