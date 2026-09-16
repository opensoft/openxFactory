# Tasks: split-opendox-two-layer-product

Status: ratified
Ratified by: split-opendox-two-layer-product — 2026-09-05, Brett Heap, "ratify #666" (record `review/ratification-2026-09-05.md`)

Nine groups, mirroring the `split-openxwallet-repo` packet's shape and adapted
for a two-repository, non-byte-identical extraction of an APPLICATION. **Every
task names its repository in brackets.** Groups 1–8 are Speckit features, one per
group, on the convener's standing rule that **OpenSpec ratifies the boundary and
Speckit builds it** — ratification authorizes them and performs none of them.
Group 0 is this packet's own bookkeeping and the ratification read.

**NOTHING BELOW GROUP 0 IS PERFORMED BY THIS PULL REQUEST.** No repository is
created, no code moves, no capability is promoted or removed, and
`docs/openxdox-naming.md` is not edited.

Legend: `[oxF]` openxFactory · `[oD]` the opensoft/openDox PROJECT (new) ·
`[oXd]` the opensoft/openXdox PROJECT (new) · `[xF]` the xFactory aggregation ·
`[OmI]` Omnigent-Install · `[Opsx]` OpsxFactory · `[cxF]` codexFactory.

> Amended 2026-09-05 — repository shape. `[oD]` and `[oXd]` each name a
> THREE-REPOSITORY PROJECT rather than one repository: an assembly root
> (`openDox`, `openXdox`), a `-spec` leg and a `-code` leg, elected by Brett
> Heap on 2026-09-05T14:52Z — verbatim *"elect the shape for both, follow the
> pin chain, no family yet"* (`opensoft/openxFactory`#656 comment
> `5552614170`). Group 1 is rewritten around `scaffold-project.py`; group 7 is
> one scaffold run rather than one repository; groups 3 and 4 name the leg a
> destination path lands in. **Groups 2, 5, 6 and 8 did not move**, except the
> two evidence lines in § 8 that COUNT repositories, which are marked where they
> stand. Record: `review/amendment-2026-09-05-repository-shape.md`.

## 0. Ratification read, the FOUR RULED questions, and Amendment 3's text

- [x] 0.1 `[oxF]` This packet lands RATIFIED AND PERFORMING NOTHING,
  `Status: ratified`, at
  `openspec/changes/split-opendox-two-layer-product/`: `proposal.md`,
  `design.md`, this file, `.openspec.yaml` with the staged origin, five spec
  delta files, and `review/ratification-2026-09-05.md`. Plus the staging INDEX
  row recording the exit and one README "OpenSpec Records" row. **DONE —
  verified at origin/main `391d2404`, 2026-09-05T23:12Z**: PR #666
  squash-merged `ceb6dc9e` (`ceb6dc9ebbdc49b40d0d45046f476215a010b713`)
  2026-09-05T13:37Z (`gh pr view 666 --json mergeCommit`); `proposal.md` front
  matter reads `Status: ratified`; `review/ratification-2026-09-05.md` present
  (49460 bytes); `.openspec.yaml` carries `origin.kind: staged`; five spec
  delta files under `specs/`
  (`corpus-adapter-seam`, `domain-descendant-boundary`,
  `domain-mapping-declaration`, `ideation-dashboard`, `neutral-product-pin`);
  staging INDEX row at `ideation/staging/INDEX.md:80` (exit detail ~2686);
  README "OpenSpec Records" row at `README.md:711`. Later amendments to the
  same ratified packet, still performing nothing: PR #684 squash-merged
  `8b297c2f` 2026-09-05T20:08Z (repository shape) and PR #701 squash-merged
  `391d2404` 2026-09-05T23:08Z (reality-check corrections) — both confirmed
  via `gh pr view <n> --json mergeCommit`.
- [x] 0.2 `[oxF]` **The ratification read is over the 102-row successor map**, not
  only over the doctrine. A reviewer contesting a ROW contests a row; the
  mechanism (REMOVE with a per-requirement map rather than keep a stub) is taken
  as recommended per the topic's Q8 and RULING C2. **DONE — RATIFIED
  2026-09-05T01:38Z**, Brett Heap, verbatim *"ratify #666"*, over the packet as
  it stood at head `6935fb8b`; no row was contested. Record:
  `review/ratification-2026-09-05.md`; ruling:
  <https://github.com/opensoft/openxFactory/issues/656#issuecomment-5548470629>.
- [x] 0.3 `[oxF]` **RULED DQ-1 — 2026-09-04T22:14Z** (`#656` comment
  `5547049745`): **`openxFactory` KEEPS its own adapter**; `doc-health` and
  OpenSpec stay here, a small package beside them implements the seam, and
  `codexDox` is a THIN DESCENDANT that pins openXdox and reuses it. Encoded: the
  15 rows moved to the `openxFactory` column (map **71 / 16 / 15**), the
  disjunction removed from every row, and **§ 5 now PRECEDES § 7** rather than
  waiting on a descendant. Rejected: `codexDox` owning the adapter and the 15
  rows, with the shed waiting on the descendant.
- [x] 0.4 `[oxF]` **RULED OQ-1 — 22:15Z** (comment `5547060378`): the FOUR-PART
  FLOOR, **as a REQUIREMENT of this change and not a recommendation in it**.
  Encoded at § D6 with the ruling's own CLOSED edit-class list (import rewrites,
  path constants, adapter calls); built at § 3.1, § 3.7, § 5.4 and § 5.5; gated
  one evidence line per part at § 8.2. Rejected: manifest-with-digests only;
  snapshot-equivalence only.
  **AMENDED 2026-09-09 — RULING OQ-K** (2026-09-09T22:19:57Z, comment
  `5609526215`,
  <https://github.com/opensoft/openxFactory/issues/656#issuecomment-5609526215>):
  **PART 2's TEST is restated as a source→destination MAPPING with declared
  multiplicity**, because the ratified equality is false once the carve
  manifest's `replicated_at_destination` rows put the same test function at more
  than one home. **The floor still has FOUR parts, part 2 is still about tests,
  and both rejected single-instrument alternatives stay rejected** — this row's
  bookkeeping is otherwise unchanged. Restated at § D6 (2) and § 5.4; the
  § 8.2 evidence line moves with it. Record:
  `review/amendment-2026-09-09-floor-part-2-mapping.md`.
- [x] 0.5 `[oxF]` **RULED OQ-2 — 22:16Z** (comment `5547067574`): ONE CHAIN —
  inside the family openDox is pinned ONLY by openXdox and every descendant pins
  openXdox; outside the family openDox is used freely as open source. **No third
  MODIFIED requirement on `neutral-product-pin`** — verified: this packet modifies
  exactly two of its nine promoted requirements. **RULED OQ-3 — 22:21Z** (comment
  `5547107565`): NO `document-lifecycle` delta now; descendants declare their
  lifecycles via `domain-mapping-declaration`; revisit at `MedxDox`. Both encoded
  at § D3a.
- [x] 0.6 `[oxF]` **GATE — `ideation-intent-plane` reaches canon, or its
  non-promotion is RECORDED.** Ratified 2026-07-23, part-realized, absent from
  `openspec/specs/` for 43 days, and RULING Q1 has just made its apply lane the
  only governed write path. A capability that is ratified and absent from canon
  cannot be assigned a successor home. Discharge by `add-ideation-intent-plane`
  archiving, or by a recorded disposition under `document-lifecycle`'s
  deliberate-non-promotion scenario. **This gates § 3 onward, not this packet.**
  **RULED PATH A 2026-09-05T23:38Z (#656
  https://github.com/opensoft/openxFactory/issues/656#issuecomment-5555554097)**
  — discharge is by `add-ideation-intent-plane` ARCHIVING WITH PROMOTION after
  4.4/5.1/5.2; 4.5 deferred successor; Path B rejected. This gate ticks at
  that archive.
  **DONE — openxFactory #832 → `56e69a11c59d473da23eab455cb9848dc083fac3`,
  2026-09-09T07:49:06Z** (head `1e1b1aa9`, Rule 6 window): `add-ideation-intent-plane`
  ARCHIVED WITH PROMOTION (`openspec/changes/archive/2026-09-09-add-ideation-intent-plane/`),
  § 4.4/§ 5.1/§ 5.2 ticked on the D-2 live-exercise evidence, § 4.5 kept as the
  deferred successor exactly as openxFactory #714 encoded it. `#656` comment `5598218564`:
  "**→ § 0.6 is MET. Path A is COMPLETE**". Independent verification (Opus, own
  worktrees): PASS WITH NOTES, 13/13 items; CI 11/11 green.
- [x] 0.7 `[oxF]` Amendment 3's text is DRAFTED at `design.md` § D8 and is NOT
  applied here. It is applied at § 1.6, in the pull request that creates the
  repository, because amending a `ratified` record ahead of the act it describes
  would leave the record describing a repository that does not exist. **DONE
  AS SPECIFIED — verified at origin/main `391d2404`, 2026-09-05T23:12Z**:
  `design.md` line 649 carries the heading `### D8 — Amendment 3, drafted here and APPLIED AT REALIZATION`, followed by the drafted `> Amendment 3 — openDox is taken knowingly` text; `docs/openxdox-naming.md` carries no
  "Amendment 3" (`grep -n "Amendment 3" docs/openxdox-naming.md` → no match,
  exit 1). Ticked as done-as-specified: drafted, deliberately unapplied until
  § 1.6.
- [x] 0.8 `[oxF]` Rule 7 substrate claims posted on issue #630 for **row 2**
  (`tests/sequenced_after/corpus-ledger.yaml` + the MOVEMENT LOG) and **row 3**
  (README "OpenSpec Records"). **Row 1 (the codexFactory floor) is NOT claimed
  now** — this packet adds and removes no path under `openspec/specs/`; it is
  claimed at § 5.6. **DONE — verified 2026-09-05T23:12Z**: CLAIM comment
  `5545846232` (2026-09-04T20:04:23Z, lane openxfactory-opendox) carries both
  "SUBSTRATE CLAIMED" blocks — "Substrate: Row 2 —
  `tests/sequenced_after/corpus-ledger.yaml` + the MOVEMENT LOG" and
  "Substrate: Row 3 — `README.md` \"OpenSpec Records\" block" — and states
  "ROW 1 IS DELIBERATELY NOT CLAIMED NOW"; RELEASE comment `5552188390`
  (2026-09-05T13:37:59Z, lane openxfactory-4-opendox-extraction) reads "rows
  2+3 claimed 2026-09-04 (comment 5545846232) for
  split-opendox-two-layer-product are RELEASED — PR #666 landed as
  `ceb6dc9e`", posted after #666 landed. Both fetched and quoted via
  `gh api repos/opensoft/openxFactory/issues/comments/<id>`.
- [x] 0.9 `[oxF]` Ledger row seeded:
  `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`,
  then `--ledger-diff` clean. **A MOVEMENT LOG entry IS owed here and is
  written** (`tests/sequenced_after/test_sweep.py`): the seeding moved TEN rows,
  not one — this change's own row enters as an ACTIVE co-modifier and NINE
  ARCHIVED rows flip `sole` -> `co-modifier` in the same act, because a
  `## REMOVED Requirements` block naming all 102 `ideation-dashboard` titles
  shares a requirement key with every change that ever solely added one. Nine
  partner rows moving for somebody else's delta is not legible from the row diff
  alone, which is the condition the log entry exists for. (Corrects an earlier
  reading of this item that said no entry was owed — Copilot round 5, taken
  2026-09-05.) **DONE — verified at origin/main `391d2404`, 2026-09-05T23:12Z**:
  `tests/sequenced_after/corpus-ledger.yaml:237` carries
  `split-opendox-two-layer-product: {state: active, class: co-modifier, declares: absent, prose: false, moved_by: "#666", moved_on: "2026-09-04"}`;
  the MOVEMENT LOG entry "TEN ROWS MOVED FOR ONE CHANGE, AND NINE OF THEM ARE
  SOMEBODY ELSE'S" is present at `tests/sequenced_after/test_sweep.py:1108`;
  `python3 scripts/validate-sequenced-after.py . --ledger-diff` reports
  "per-change sweep ledger consistent with the corpus (175 rows)" — clean.

## 1. Repository bootstrap — TWO ELECTED PROJECTS, SIX repositories, public, Apache-2.0 (RULING Q7, as amended 2026-09-05)

> Amended 2026-09-05 — repository shape. This group first read *two
> repositories* and created them by hand. Brett Heap's ruling of
> 2026-09-05T14:52Z, verbatim *"elect the shape for both, follow the pin chain,
> no family yet"* (`opensoft/openxFactory`#656 comment `5552614170`), elects the
> `openRepoShape` three-repository shape for BOTH layers, so the group creates
> SIX repositories with `scaffold-project.py` rather than two by hand. Every
> item below that MOVED carries its own note; 1.8 did not move. Q7 is not
> reopened: `opensoft` owns them, all six are PUBLIC under Apache-2.0.
> Electing the shape CONFERS NOTHING — no gate, no floor, no grant, no
> authority — so no boundary this packet ratifies is changed by it. Record:
> `review/amendment-2026-09-05-repository-shape.md`.

- [x] 1.1 `[oD]` **SCAFFOLD the `openDox` project — three repositories in one
  run**, from a clean checkout of `opensoft/openRepoShape` at the commit
  `contracts/openreposhape-pin.yaml` pins. **UNBLOCKED** *(reality check
  2026-09-05, second run, claims C6/C7/C39/C42)* **— the re-pin landed as PR
  #700, commit `303bfd53`, moving the pin to `e9c4827b85f50503bbdd9e5b4fac9d6c3d0baf63`;
  the tool accepts this exact command there, measured `--dry-run`. Run
  `--dry-run` first and keep its output as the evidence line; see 1.1a for
  the now-historical refusal.**

  **DONE — hand-acts evidence (dry-run + real run) 2026-09-06T01:27:56–01:28:16Z;
  re-verified live 2026-09-06T04:58Z**: `--dry-run` at the landed pin
  (`e9c4827b85f50503bbdd9e5b4fac9d6c3d0baf63`) exited 0; the real run followed.
  `gh api repos/opensoft/openDox/commits/bad2d2ad4c93c2d0cc3ed82ec56de3e5eecbc2fe`
  reads the scaffold commit message "Scaffold openDox: manifest, two legs,
  three pins / Shape opensoft/openRepoShape @ e9c4827b… / spec
  beba24d45a7494e9070ff69f3e011de6f237a9c3 / code
  4e278d3619c2c3da2ad7eb188895e8dafee2991c" at `commit.author.date 2026-09-06T01:28:10Z` — inside the claimed window; `gh api repos/opensoft/openDox-spec/commits/beba24d4…` and
  `repos/opensoft/openDox-code/commits/4e278d36…` both resolve (01:28:06Z /
  01:28:08Z). `gh api repos/opensoft/openDox --jq '{visibility,license:.license.spdx_id,topics}'` reads `public` /
  `Apache-2.0` / `["xf-project-opendox"]`, and the same call on `openDox-spec`
  and `openDox-code` reads the same topic. No claim made on the `opendox`
  GitHub organization (unchanged, per RULING C1). No `RULESET_HINT` text
  observed in the scaffold's own emitted files (1.5 rulesets are separate hand
  acts, see below).

  ```
  python3 scaffold-project.py \
      --org opensoft --project openDox --id opendox --name 'openDox' \
      --visibility public \
      --elected-by 'Brett Heap' --elected-on 2026-09-05 \
      --reference 'openxFactory docs/project-repo-schema.md'
  ```

  It creates `opensoft/openDox`, `opensoft/openDox-spec` and
  `opensoft/openDox-code`, mounts the two legs at `spec/` and `code/`, writes
  `project.yaml` with the election and the pins, and sets the topic
  `xf-project-opendox` on all three. **Run `--dry-run` first and keep its
  output as the evidence line.** No claim is made on the `opendox` GitHub
  organization (RULING C1). *(Amended 2026-09-05: this first said "Create
  `opensoft/openDox`: PUBLIC, Apache-2.0, `opensoft`-owned" — one repository,
  created by hand.)*
- [x] 1.1a `[oD]` `[oXd]` **`opensoft/openRepoShape`#41 is RESOLVED, and the
  re-pin it moved to has LANDED** *(reality check 2026-09-05, second run,
  claims C6/C7/C38/C39/C42)*. #41 was CLOSED as completed 2026-09-05T17:19:12Z
  by openRepoShape PR #45, *A neutral product may elect the shape and be its
  own assembly root (#41)*, merge commit `5ffa8d58` (merged 17:19:11Z),
  authored by lane `xfactory-2`; `355f6ef4` (#47) and every descendant commit
  carry both `c2cc9e25` (#42) and `5ffa8d58` (#45). **The two invocations
  above WERE refused at the commit this repository pinned when this item was
  written** (`122d729bc0c2f2e0ded0bb61b6b97f49512f613e`) — kept below as
  history. Measured refusal, kept here as history:

  ```
  REFUSED naming-role-mismatch: 'openDox' classifies as neutral-product, not as
  the 'assembly' form of a project leg (the neutral-product form is unambiguous
  by construction, so it needs nothing declared)
  Remediation: re-run with a --project value that is one CamelCase token.
  ```

  `accepts_role()` in `scripts/repo_shape.py` admitted only `project-leg/<role>`
  and `domain-descendant/assembly`, and the offered remediation was not
  takeable — the name is the product's name and is what the ruling elected.
  `scripts/validate-repository-naming.py --explain openDox` already computed
  the resolution this needed (`also_matches: project-leg/assembly`) and
  `accepts_role()` discarded it. #45 is the admission #41 asked for.
  **THE RE-PIN LANDED** as PR #700, commit `303bfd53` (2026-09-05T17:50-04:00,
  lane openxfactory-4-opendox-extraction): `contracts/openreposhape-pin.yaml`
  now records `e9c4827b85f50503bbdd9e5b4fac9d6c3d0baf63` (31 digests / 45
  path-only / 76 files, verifier green), a descendant of `355f6ef4` and
  therefore of both #42 and #45. **1.1 and 1.2 are UNBLOCKED** — do not
  re-author this re-pin, and do not re-pin backward to `355f6ef4`. Nothing
  else in the packet ever waited on it, because the packet performs nothing.

  **DONE — bookkeeping, verified live 2026-09-06T04:58Z**: `gh pr view 45 -R opensoft/openRepoShape --json state,mergeCommit` reads `MERGED`, merge
  commit `5ffa8d58d1d5853f262bd11bc192e36f3dfd3b3d`; `gh pr view 700 -R opensoft/openxFactory --json state,mergeCommit,mergedAt` reads `MERGED`,
  merge commit `303bfd5322f64dad9945467e911d91a90475e938`, merged
  `2026-09-05T21:50:02Z`; this worktree's own
  `contracts/openreposhape-pin.yaml:114` (checked out at `origin/main`) reads
  `commit: "e9c4827b85f50503bbdd9e5b4fac9d6c3d0baf63"`, matching. `gh api repos/opensoft/openRepoShape/commits/e9c4827b85f50503bbdd9e5b4fac9d6c3d0baf63`
  resolves to a real commit descended from `5ffa8d58`. Unblocked and landed;
  ticked as bookkeeping per the item's own text.
- [x] 1.2 `[oXd]` **SCAFFOLD the `openXdox` project — three repositories, and the
  family's ONE pin (RULING OQ-2)**, after 1.1 has landed a commit on
  `opensoft/openDox`. **UNBLOCKED** *(reality check 2026-09-05, second run)*
  **— runnable at the commit this repository pins (`e9c4827b`); see 1.1a for
  the historical refusal at `122d729b`:**

  ```
  python3 scaffold-project.py \
      --org opensoft --project openXdox --id openxdox --name 'openXdox' \
      --visibility public \
      --elected-by 'Brett Heap' --elected-on 2026-09-05 \
      --reference 'openxFactory docs/project-repo-schema.md' \
      --pin openDox@<40 hex — the openDox ASSEMBLY ROOT's commit at that moment>
  ```

  `--pin` writes `contracts/opendox-pin.yaml` AND the
  `neutral_product_pins: [openDox]` entry in `project.yaml` in the same act;
  an unqualified name
  resolves under `opensoft` by default, which is where openDox lives. **A tag
  or an abbreviated oid is refused by the tool** — pass the full 40 hex of the
  assembly root, never a leg. *(Amended 2026-09-05: this first said "Create
  `opensoft/openXdox`: PUBLIC, Apache-2.0, `opensoft`-owned".)*

  **DONE — hand-acts evidence (dry-run with `--pin openDox@bad2d2ad4c93c2d0cc3ed82ec56de3e5eecbc2fe` + real run)
  2026-09-06T01:28:44–01:29:07Z; re-verified live 2026-09-06T04:58Z**: the
  real run's scaffold commit,
  `gh api repos/opensoft/openXdox/commits/460f2692a8dec3794ca8019e8cd982bfdd6b1fca`,
  reads "Scaffold openXdox: manifest, two legs, three pins / Shape
  opensoft/openRepoShape @ e9c4827b… / spec
  8358900476aa95de1c5055fead8836d26c04d5bb / code
  3f0c11774709baebbe8b31f137f189d4a290be71" at `commit.author.date 2026-09-06T01:29:01Z` — inside the claimed window; both leg seed commits
  resolve. `gh api repos/opensoft/openXdox/contents/contracts/opendox-pin.yaml?ref=0365cea5db7c203bc10b0aabefd99e8a1e17866e`
  (root main `0365cea5db7c203bc10b0aabefd99e8a1e17866e`, the PR#2 tip after the
  later re-pin-legs-to-tips hand act) reads `commit: "bad2d2ad4c93c2d0cc3ed82ec56de3e5eecbc2fe"` and `digests.tree_sha256: "5acff0af63d262bb2e48f90b5e9c8cafab260d383e5bc2a0c4a30b5e89f25308"`;
  `project.yaml` at the same ref reads `neutral_product_pins: [openDox]`,
  `elected_by: "Brett Heap"`, `elected_on: 2026-09-05`. Full 40-hex commit
  passed, no tag or abbreviated oid.
- [x] 1.3 `[oD]` `[oXd]` **WHAT THE SCAFFOLD PRODUCES, AND WHAT IS STILL A HAND
  ACT.** *(Amended 2026-09-05: this first said "Scaffold each: `README.md`,
  `LICENSE`, `AGENTS.md`/`CLAUDE.md`, `.github/CODEOWNERS`, its own OpenSpec
  instance, its own `contracts/manifest.yaml` and `contracts/CHANGELOG.md`, and
  `.github/workflows/` carrying one validation workflow plus a pytest suite" —
  as if one tool did all of it. It does not.)*
  **The tool writes**, in each assembly root: `project.yaml`, `Makefile`,
  `README.md`, `.gitignore`, `.github/workflows/validate.yml`,
  `contracts/shape-pin.yaml`, `contracts/spec-pin.yaml`,
  `contracts/code-pin.yaml`, one `contracts/<product>-pin.yaml` per `--pin`,
  `scripts/bootstrap.py`, `scripts/validate-manifest.py`,
  `scripts/validate-pins.py`, the two legs as submodules, and the topic. In
  each leg: `.gitignore`, `README.md` and one `.gitkeep`
  (`requirements/` for `-spec`, `src/` for `-code`) — **and nothing else**.
  **Every one of these remains a hand act:** the Apache-2.0 LICENSE TEXT (the
  tool writes no license file anywhere), 1.4's four posture files,
  `.github/CODEOWNERS`, `AGENTS.md`/`CLAUDE.md`, the OpenSpec instance in each
  `-spec` leg, `contracts/manifest.yaml` and `contracts/CHANGELOG.md` in each
  assembly root, a pytest suite and a required check in each of the FOUR legs
  (the scaffold's `validate.yml` covers the two assembly roots only), and 1.5's
  rulesets.
  *(Corrected by reality check 2026-09-05, second run (lane
  openxfactory-4-opendox-extraction; claims C10/C11), re-measured against a
  fresh `openRepoShape` clone at the commit this repository now pins,
  `e9c4827b85f50503bbdd9e5b4fac9d6c3d0baf63` (PR #700, `303bfd53`) — restated
  ONCE at the pin rather than compared across two revisions, since `122d729b`
  is no longer pinned anywhere and `355f6ef4` was never itself the pin, only
  an ancestor of it (the first run's two-revision comparison is superseded by
  this). A `--local-remote-dir` materialization (no network, nothing created
  on GitHub) of the `1.1` command above writes, in the assembly root —
  EIGHTEEN files plus the two legs as submodule gitlinks, TWENTY entries, not
  twelve: `.github/workflows/validate.yml`, `.gitignore`, `.gitmodules`,
  `AGENTS-shape.md`, `AGENTS.md`, `CLAUDE.md`, `Makefile`, `README.md`,
  `contracts/code-pin.yaml`, `contracts/repository-naming.yaml`,
  `contracts/shape-pin.yaml`, `contracts/spec-pin.yaml`, `project.yaml`,
  `scripts/bootstrap.py`, `scripts/repo_shape.py`,
  `scripts/validate-manifest.py`, `scripts/validate-pins.py`,
  `scripts/validate-repository-naming.py`, plus the `code/` and `spec/`
  submodule gitlinks. `scripts/repo_shape.py`,
  `scripts/validate-repository-naming.py` and `contracts/repository-naming.yaml`
  are copied out of `openRepoShape`'s own tree so the project carries the
  standard it was cut from, each carrying a row in the project's own
  `contracts/shape-pin.yaml`, so a realizer who deletes one as unaccounted-for
  turns `scripts/validate-pins.py` red on the first push. `AGENTS-shape.md` is
  itself digest-pinned there too — never hand-edit it; edits belong in the
  generated `AGENTS.md`, deliberately left unpinned. In EACH leg — FIVE files,
  not three: `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `README.md`, and one
  `.gitkeep` (`requirements/` for `-spec`, `src/` for `-code`). This makes
  "`AGENTS.md`/`CLAUDE.md`" in the hand-act sentence above FALSE in
  operation — the tool writes them, at this pin, in both the assembly root and
  every leg. Every other item in the hand-act sentence (LICENSE, 1.4's four
  posture files, `.github/CODEOWNERS`, the OpenSpec instance,
  `contracts/manifest.yaml`/`CHANGELOG.md`, the FOUR legs' pytest suite and
  required check, 1.5's rulesets) is unaffected and holds at this pin.)*

  **DONE — restated file sets confirmed against the six real repositories,
  live `gh api` reads 2026-09-06T04:58Z (citing the brief's hand-acts evidence
  for PR numbers/shas):** `gh api repos/opensoft/openDox/git/trees/1f0a7693824b01dbb7246701d02eccd0a729a769`
  (root main, after PR #1 `1c82b422` + PR #2 `1f0a7693`) lists exactly
  `.github`, `.gitignore`, `.gitmodules`, `AGENTS-shape.md`, `AGENTS.md`,
  `CLAUDE.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `LICENSE`, `Makefile`,
  `README.md`, `SECURITY.md`, `code` (submodule gitlink), `contracts`, `docs`,
  `project.yaml`, `scripts`, `spec` (submodule gitlink) — the scaffold's
  eighteen plus the 1.4 posture hand acts, matching the restated list above
  with none missing and nothing unaccounted-for. The same call on
  `repos/opensoft/openXdox/git/trees/0365cea5db7c203bc10b0aabefd99e8a1e17866e`
  (root main, after PR #1 `1a434a53` + PR #2 "Re-pin legs to their current
  tips") lists the same eighteen entries (no `docs` tree in this root, since
  no branch-protection doc hand act landed on it) plus the two gitlinks.
  `repos/opensoft/openDox-spec/git/trees/60e546c69963f9fe8a5071975f7c657ed95d0832`
  (PR #2 `60e546c6`) lists `.github`, `.gitignore`, `AGENTS.md`, `CLAUDE.md`,
  `LICENSE`, `README.md`, `SECURITY.md`, `docs`, `openspec`, `requirements`,
  `tests` — the scaffold's five plus LICENSE/SECURITY.md/OpenSpec instance/
  `docs/branch-protection.md`/tests hand acts. `repos/opensoft/openDox-code/git/trees/580f61dff7e6c0235ba1f5681432d10cf2e85fa1`
  lists the matching `src`-shaped set with no `openspec`. The same shapes hold
  for `openXdox-spec` at `274745b11f0fabeadbd1544d67b416c4d15a96ff` and
  `openXdox-code` at `3921f5035054684a12c1935536ee89df10cc9b61`. Every sha
  above is this repository's own live `main` head, read directly via `gh api`,
  not copied from a prior report.
- [x] 1.4 `[oD]` `[oXd]` **PUBLIC FROM DAY ONE MEANS A POSTURE EXISTS AT CREATION**,
  not after the first outside issue: `CONTRIBUTING.md`, `SECURITY.md` (a
  security-report path that is not an issue) and `CODE_OF_CONDUCT.md`. Retro-fitting
  a license or a posture onto a repository that has taken outside contributions is
  materially harder than choosing at creation, and every other `open*` repository
  in this organization is private and unlicensed — so nothing here can be copied.
  *(Amended 2026-09-05: WHERE, now that a project is six repositories. `LICENSE`
  and `SECURITY.md` in ALL SIX — each leg is separately clonable and GitHub
  surfaces the security-report path per repository, so a leg without one is a
  leg with no path. `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` in the two
  ASSEMBLY ROOTS, with each leg's `README.md` pointing at its root's copy: one
  contribution posture per project, not per repository.)*

  **DONE — verified live 2026-09-06T04:58Z**: `gh api repos/opensoft/<repo> --jq '.license.spdx_id'` reads `Apache-2.0` on all six
  (`openDox`, `openDox-spec`, `openDox-code`, `openXdox`, `openXdox-spec`,
  `openXdox-code`), confirming a detected `LICENSE` file in each; the same six
  git-tree reads used for 1.3's evidence each list a `SECURITY.md` blob
  (`openDox-spec` PR #1 `11480bbe` added "private vuln reporting"; the other
  five legs match). `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` appear ONLY in
  the two assembly-root trees (`openDox` root and `openXdox` root, both listed
  under 1.3's tree reads) and in none of the four legs' trees — matching the
  amended scope exactly.
- [x] 1.5 `[oD]` `[oXd]` Branch-protection ruleset created in **EVALUATE** mode in
  each, promoted to **ACTIVE** once its required check has reported once. Ruleset
  state is a repository setting, not a tree fact, and gets its own evidence line.
  *(Amended 2026-09-05: in each of SIX, not each of two. The EVALUATE→ACTIVE
  rule is UNCHANGED. `scaffold-project.py` creates no ruleset — the only ruleset
  text it emits is a hint for the case where an existing organisation ruleset
  refuses the seed push — so all six are hand acts, and the two `-spec`/`-code`
  pairs need theirs before their assembly root's `validate` gate can be trusted
  to mean anything.)*

  Evidence, verified live 2026-09-06T04:58Z via `gh api repos/opensoft/<repo>/rulesets/<id> --jq '{name,enforcement}'`: **openDox
  ACTIVE** — `openDox` `22364975`, `openDox-spec` `22364961`, `openDox-code`
  `22364973`, all `{"name":"Require validate check","enforcement":"active"}`
  (promoted by an agent after `validate` reported on PR #2 of each; disclosed
  to Brett on `#656` 02:2xZ). **openXdox EVALUATE** — `openXdox` `22371409`,
  `openXdox-spec` `22371411`, `openXdox-code` `22371412`, all
  `{"name":"Require validate check","enforcement":"evaluate"}` (created
  2026-09-06T04:50Z; `validate` had already reported SUCCESS on PRs #1/#2 of
  each; promotion to ACTIVE is OFFERED to Brett, not performed). Two org
  rulesets (`18834180`, `8981805`) also bind all six.

  **DONE — 2026-09-06T08:56Z.** All six repository rulesets requiring the
  `validate` status check are **ACTIVE**: openDox — `openDox` `22364975`,
  `openDox-spec` `22364961`, `openDox-code` `22364973` (created EVALUATE,
  `validate` reported on each repo's PR #2, promoted ACTIVE 2026-09-06
  ~02:1xZ); openXdox — `openXdox` `22371409`, `openXdox-spec` `22371411`,
  `openXdox-code` `22371412` (created EVALUATE 04:50Z, `validate` reported
  on PRs #1/#2 of each, promoted ACTIVE 08:56Z on Brett Heap's ruling
  https://github.com/opensoft/openxFactory/issues/656#issuecomment-5558170462
  — "§ 1.5 rulesets: PROMOTE openXdox's three to ACTIVE"). Each requires the
  `validate` status check on the default branch. Ruleset state read back
  live via `gh api repos/opensoft/<repo>/rulesets/<id>`:
  `{"name":"Require validate check","enforcement":"active"}` for all six,
  including a fresh read of openXdox's three (`22371409`, `22371411`,
  `22371412`) confirming the promotion took.
- [x] 1.6 `[oxF]` **Amendment 3 APPLIED** to `docs/openxdox-naming.md`, text as
  drafted at `design.md` § D8, in the SAME pull request as 1.1/1.2. The record is
  `ratified`; this is an amendment, not a rewrite. *(Amended 2026-09-05: its
  text now carries the SIX repository names — `openDox`, `openDox-spec`,
  `openDox-code`, `openXdox`, `openXdox-spec`, `openXdox-code` — the election
  (Brett Heap, 2026-09-05, reference `openxFactory docs/project-repo-schema.md`), and the
  leg-suffix rule that the lowercase hyphenated `-spec`/`-code` forms are NOT
  new brand names and sit in a different naming family. `openXdox-Install` is
  unchanged.)*

  **DONE — this pull request.** `docs/openxdox-naming.md` gains a new
  `## Amendment 3 — \`openDox\` is taken knowingly (2026-09-06)` section,
  appended after `## Amendment 2` in Amendment 2's own format (heading, then
  bolded lead-in paragraphs), de-blockquoted from the exact text drafted at
  `design.md` lines 666–729 (the blockquote running from `> ## Amendment 3 — \`openDox\` is taken knowingly (2026-<MM>-<DD>)` through `> created for any of them.`), with `2026-<MM>-<DD>` filled as `2026-09-06` (the date the six
  repositories were created — confirmed live above: `openDox`/`openDox-spec`/
  `openDox-code` `created_at 2026-09-06T01:28:0xZ`, `openXdox`/`openXdox-spec`/
  `openXdox-code` `created_at 2026-09-06T01:28:4x–01:28:5xZ`, all via `gh api repos/opensoft/<repo> --jq .created_at`). `Status: ratified` is untouched —
  this is an amendment, not a rewrite; no front-matter line was added noting
  when the amendment applied, because Amendments 1 and 2 carry no such line
  either (checked by reading the whole file before editing) — mirroring their
  convention exactly means adding none. The SIX repository names, the
  election, and the leg-suffix rule are all present in the appended text
  (the "SIX REPOSITORY NAMES…" and "The leg suffixes are not new brands…"
  paragraphs), and `openXdox-Install` is named as unchanged in the "leg
  suffixes" paragraph. 1.1/1.2's actual repository-creation acts landed
  earlier as separate hand acts against the six repositories themselves (see
  1.1/1.2's own evidence above) rather than in this pull request; this pull
  request is the one that performs the naming-record amendment 1.6 requires,
  per 0.7's own note that Amendment 3 applies "at § 1.6, in the pull request
  that creates the repository" — read here as the repositories already
  created by hand, amendment applied in the first pull request that follows.
- [x] 1.7 `[oxF]` Register the descendant NAMES in the naming record —
  `MedxDox`, `codexDox`, `LedgerxDox`, `AdxDox`, `OpsxDox`, and `openXdox-Install`
  — **and create no repository for any of them.** The wallet arc's own treatment;
  a named-and-absent repository is otherwise a thing people create by hand.
  *(Amended 2026-09-05: register each descendant's LEG NAMES beside it —
  `codexDox`, `codexDox-spec`, `codexDox-code`; `MedxDox`, `MedxDox-spec`,
  `MedxDox-code`; and the same for `LedgerxDox`, `AdxDox` and `OpsxDox` —
  because a descendant scaffolded the same way is three repositories, and a leg
  name nobody registered is exactly the name somebody creates by hand. STILL
  CREATING NONE: fifteen descendant names plus one install name, zero
  repositories.)* *(Corrected by reality check 2026-09-05 (lane
  openxfactory-4-opendox-extraction): "eighteen" is arithmetic wrong, at every
  `openRepoShape` revision checked (tip `e9c4827b` and `122d729b` — the pin
  of that moment, before PR #700 re-pinned to `e9c4827b` at 21:50Z — give
  byte-identical leg counts). Five descendants are named above — `MedxDox`,
  `codexDox`, `LedgerxDox`, `AdxDox`, `OpsxDox` — each three names (the assembly
  name plus its two leg names, confirmed by `scaffold-project.py --dry-run` at
  both revisions and by `scripts/validate-repository-naming.py --explain`
  classifying all fifteen as `project-leg`): 5 × 3 = **fifteen** descendant
  names, not eighteen. A sixth descendant would be needed to reach eighteen, and
  none exists anywhere in this packet — reproducible as
  `grep -ohE '(^|[^[:alnum:]_])[A-Za-z]+xDox([^[:alnum:]_]|$)' proposal.md design.md tasks.md | sed -E 's/^[^A-Za-z]*//; s/[^A-Za-z]*$//' | sort -u`, run from `openspec/changes/split-opendox-two-layer-product/` — the
  pattern is POSIX ERE with no Perl-style escapes (no `\b`, which POSIX ERE
  does not define and GNU grep accepts only as an extension; the boundary here
  is a bracket-class alternative, stripped afterward with `sed`); the `-o`/`-h`
  options are GNU/BSD grep extensions (available on Linux and macOS), not
  POSIX-required, and returns
  SEVEN distinct strings (`AdxDox`, `LedgerxDox`, `MedxDox`, `OpsxDox`,
  `codexDox`, `medxDox`, `openxDox`), not five, because the broad pattern also
  catches two non-descendant artifacts: `medxDox`, a lowercase casing variant
  appearing exactly ONCE, inside Brett Heap's verbatim quoted founding utterance
  at `proposal.md`:59 ("We then further pin that down to medxDox and CodeXdox
  …"), never as a declared descendant name (the packet's own registration in
  `tasks.md` § 1.7 spells it `MedxDox`); and `openxDox`, the case-folded
  ALSO-ACCEPTED spelling of `openXdox` itself named twice in the pin-chain
  discussion (`tasks.md`:347, `design.md`:868 — "`openXdox`.casefold() equals
  `openxDox`.casefold()"), not a sixth descendant. Excluding those two
  artifacts, `grep -owhE 'MedxDox|codexDox|LedgerxDox|AdxDox|OpsxDox' proposal.md design.md tasks.md | sort -u | wc -l` — the pattern is POSIX ERE
  with no Perl-style escapes, so no `\b` is needed; the `-o`/`-h`/`-w` options
  are GNU/BSD grep extensions (available on Linux and macOS), not
  POSIX-required. Returns **5**: the five names above are the only
  declared descendant base names in the packet. Read "fifteen descendant names —
  five descendants × three names each, the assembly name plus its two leg
  names — plus one install name, zero repositories" in place of the
  eighteen-count above; the rest of the sentence is unaffected.)*

  **DONE — this pull request; registered by Amendment 3's own paragraph
  (`docs/openxdox-naming.md` has no separate names table/list — the whole file
  was read before this PR's edit — so the amendment paragraph IS the
  registration, per this item's own fallback rule).** The "descendant spelling
  is unaffected" paragraph registers `MedxDox`, `codexDox`, `LedgerxDox`,
  `AdxDox`, `OpsxDox` and, beside them, their leg names `codexDox-spec`,
  `codexDox-code`, `MedxDox-spec`, `MedxDox-code`, `LedgerxDox-spec`,
  `LedgerxDox-code`, `AdxDox-spec`, `AdxDox-code`, `OpsxDox-spec`,
  `OpsxDox-code` — fifteen names — each "with no repository created"; the "leg
  suffixes are not new brands" paragraph separately names `openXdox-Install`
  as unchanged and still "registered with no repository created". Verified
  live 2026-09-06T04:58Z: `gh api repos/opensoft/<name>` returns `404 Not Found` for all sixteen — the five bases, the ten leg names, and
  `openXdox-Install` — checked individually — zero repositories, as required.
- [x] 1.8 `[xF]` Aggregation `CLAUDE.md` working rule #1 amended: it accommodates a
  neutral `open*` product `openxFactory` pins, and does NOT yet accommodate a
  neutral product that is an APPLICATION WITH A SCHEMA rather than a contract
  family.
  **DONE — opensoft/xFactory #284 → `05cb5abf9427b37f9d94ead5329bc0ee84408915`,
  2026-09-06T08:43:55Z**: an additive sentence appended to rule 1 (the existing
  sentences are unchanged) — "A neutral `open*` product may also be an
  APPLICATION with its own schema and database rather than a contract family
  (`openDox`, with `openXdox` as its openxFactory-tuned layer —
  split-opendox-two-layer-product, 2026-09-06): it is elected into the
  openRepoShape three-repository shape, `openxFactory` consumes it at a pin
  exactly as it consumes a contract family (inside the openDox family,
  `openxFactory` pins `openXdox` ONLY; openDox's commit is read through
  openXdox's own pin — RULING F), and domain repos consume it through their own
  descendant (`codexDox`, `MedxDox`, …) pinning `openXdox`." Verified live
  against `opensoft/xFactory`'s current `main`
  (`gh api repos/opensoft/xFactory/contents/CLAUDE.md`): the sentence is
  present verbatim in rule 1.
- [x] 1.9 `[xF]` **NEW (2026-09-05) — `project-register.yaml` rows for the two
  elected projects.** One row each for `openDox` and `openXdox` carrying
  `schema: project-repo-schema`, `reference: openxFactory docs/project-repo-schema.md`, the
  three repositories in `repositories`, and a `repository_roles` entry per
  repository (`assembly`, `spec`, `code` — at most one `assembly` per project).
  **The row is DERIVED and the manifest is the SOURCE**
  (`docs/project-repo-schema.md` § *The manifest is the source; a register row
  is derived*): each field above is READ FROM that project's own `project.yaml`
  and the register never originates an election. Where the two disagree, the
  register wins for NAVIGATION only and the disagreement is reported as drift —
  it does not re-elect anything. Lands with 5.8's other aggregation edits.
  **STATUS — 2026-09-12, tick JUDGED MET — the two derived election
  rows landed in the same PR.** `project-register.yaml`'s `opendox` and
  `openxdox` rows landed at `opensoft/xFactory` **#442 →
  `41d6d7aeb15dbb73c75ac4e9ba2cb2e8cfc6c1a3`** together with 5.8's other
  aggregation edits, exactly as this box's own last sentence says (5.8's
  STATUS line below carries the PR's landing detail). Each row is DERIVED,
  per this box's own rule and per the row's own header comment in
  `project-register.yaml`: the `opendox` row's `repositories` (`openDox` /
  `openDox-spec` / `openDox-code`) and `repository_roles` (assembly / spec /
  code) are read from `opensoft/openDox`'s own `project.yaml`, at the landed
  pointer `8ec3036ce496a90a3c92a89c4907e57941901b51`; the `openxdox` row's
  `repositories` (`openXdox` / `openXdox-spec` / `openXdox-code`) and
  `repository_roles` are read from `opensoft/openXdox`'s own `project.yaml`,
  at the landed pointer `eca0b5977b0cca1f39c725b95fc9fa8b4d307d72`. Both rows
  carry `schema: project-repo-schema` and `reference: openxFactory
  docs/project-repo-schema.md`, as required. `#656` record: `5646934254`.
- [x] 1.10 `[oXd]` `[oxF]` **NEW (2026-09-05) — THE PIN CHAIN. `opensoft/openRepoShape`#40
  is RESOLVED**, by openRepoShape PR #42, *Descendant referent follows the
  declared pin chain (#40)*, merge commit `c2cc9e25`, merged 2026-09-05T16:26:49Z
  — the same re-pin recorded at 1.1a *(reality check 2026-09-05, second run)*,
  LANDED as PR #700 / `303bfd53` → `e9c4827b`, covers #42 as well, since
  `e9c4827b` carries both. `openXdox`'s `project.yaml`
  declares `neutral_product_pins: [openDox]` (written by 1.2's `--pin`); every
  descendant declares `neutral_product_pins: [openXdox]` and — ONLY WHEN
  SCAFFOLDED WITH `--referent-chain openXdox,openDox` — records the chain it
  relies on: `naming.referent_chain: [openXdox, openDox]` is written by that flag
  alone (openRepoShape PR #42, `scaffold-project.py:464`,
  `shape_materialize.py:486-488`); a run without the flag exits 0 and records no
  chain. Per
  openRepoShape#40, which amends that standard's descendant-referent rule so a
  `<Domainx><Product>` name classifies as a descendant when its declared pins
  REACH the matching `open<Product>` through declared links. This preserves
  RULING OQ-2 exactly: inside the family openDox is pinned only by openXdox, and
  no descendant pins openDox directly.
  **#40 is resolved upstream (above); if the RE-PIN that carries it into this
  repository has not landed when § 7 runs, that is NOT a blocker — it is a
  recorded interim, and the decision is taken here rather than left to the
  session that hits it. It is also not the interim #40's own issue body
  predicts, and the measurement is recorded here so nobody re-derives it.**
  MEASURED 2026-09-05 at openRepoShape `main` `f9ff3f8`: `codexDox` with
  `neutral_product_pins: [openXdox]` classifies as **a
  `domain-descendant` in the `assembly` role — it PASSES today**
  (`also_matches: [project-leg/assembly]`, `descendant_referent: openDox`,
  `referent_declared: true`), and the assembly
  root's own `scripts/validate-manifest.py` accepts that manifest, because the
  pin file it looks for is `contracts/openxdox-pin.yaml`, which the scaffold
  wrote. **It passes by ACCIDENT, not by the chain:**
  `contracts/repository-naming.yaml` admits an x-stem spelling of the referent
  (`also_accepted: openx{product}`, present so `codexFactory` may descend from
  `openxFactory`), the referent test compares CASE-FOLDED, and
  `openXdox`.casefold() equals `openxDox`.casefold() — so a pin on the
  INTEGRATION layer satisfies the referent test for the NEUTRAL CORE, and the
  manifest asserts a declared `openDox` referent in a tree that declares no
  openDox pin. **The classification is right and the reason it records is
  false.** So the interim is: scaffold with `--referent-chain openXdox,openDox`,
  and RECORD the chain actually relied on (`naming.referent_chain: [openXdox, openDox]`) in the descendant's own manifest — written by that flag alone; it
  is never inferred, and a run without it records no chain and exits 0 — so the
  accidental pass is never left standing as the explanation;
  the re-pin landing later makes the same classification true (#40 already
  reasons this way upstream) and re-reads the same tree with no migration.
  What the interim does NOT permit is adding a direct
  `openDox` pin to a descendant to force the classification — that would break
  OQ-2 to satisfy a validator.

  **DONE — bookkeeping, verified live 2026-09-06T04:58Z**: `#40` is resolved
  upstream by openRepoShape PR #42, merge commit `c2cc9e25` (checked as an
  ancestor of the pin landed here — see 1.1a's evidence for the `gh pr view 45`/`700` reads that confirm the same lineage). **The re-pin HAS landed** in
  this repository (`contracts/openreposhape-pin.yaml` reads
  `e9c4827b85f50503bbdd9e5b4fac9d6c3d0baf63`, a descendant of `c2cc9e25`), so
  the item's own "not a blocker — recorded interim" condition is now moot for
  this repository rather than live. `openXdox`'s live `project.yaml`
  (`gh api repos/opensoft/openXdox/contents/project.yaml?ref=main`) reads
  `neutral_product_pins: [openDox]`, and `openDox` pins nothing — matching
  RULING OQ-2 exactly: inside the family, only `openXdox` pins `openDox`, and
  no descendant pins it directly (there being no descendant repository yet,
  per 1.7). The interim note — scaffold with `--referent-chain openXdox,openDox` and record `naming.referent_chain` rather than adding a
  direct `openDox` pin to force classification — stands unmodified for the
  first descendant that IS scaffolded; ticked as bookkeeping per the item's
  own framing ("not a blocker … the decision is taken here").

## 2. The seam — landed INSIDE openxFactory, before anything moves

**This group is worth doing whether or not the carve ever happens, and nothing
else in the arc can start while the two packages import each other.**

- [x] 2.1 `[oxF]` **BREAK THE CYCLE FIRST.** Relocate `OutputBoundary` out of
  `scripts/ideation_dashboard/boundary.py` into a small module BOTH packages
  import, and repoint `scripts/doc_health/derive_possibles.py:857` and
  `scripts/doc_health/ideation_readiness.py:1351`. After this task
  `scripts/doc_health/` imports NOTHING from `scripts/ideation_dashboard/`, proven
  by a test that greps for the direction rather than by inspection. **DONE — PR
  #724 squash-merged `e2b8f620` (`e2b8f620bce4d2a1c4cf6c9a1247ce6d810cda55`)
  2026-09-06T11:26Z, verified `gh pr view 724 --json mergeCommit`**: the whole
  guard moved by `git mv` to `scripts/output_boundary.py`, a module under
  `scripts/` that neither package owns;
  `ideation_dashboard/boundary.py` stays a 17-name re-export (its `__all__`,
  counted on this branch) so every existing
  import keeps working; both `doc_health` call sites repointed; and the
  direction is proven by an AST scan with a negative control
  (`tests/doc-health/test_import_direction.py`) rather than by the grep the item
  named, because four `doc_health` files mention the dashboard in prose on
  purpose.
- [x] 2.2 `[oxF]` Name the corpus adapter's operations and land them as an
  interface in-tree: **list, read, write back, check**, plus the two derived
  operations **classify** and **resolve** (`design.md` § D2). A repository created
  before the interface exists has its boundary drawn by whatever `git filter-repo`
  happened to move. **DONE — PR #725 squash-merged `ea4e6ff2`
  (`ea4e6ff2953c973df264ada3b8c7b986f31723f0`) 2026-09-06T17:43Z, verified `gh pr
  view 725 --json mergeCommit`**: `scripts/corpus_adapter.py` lands the six
  operations — `resolve`, `list_documents`, `read`, `classify`, `check`,
  `write_back` — as a closed-member `@runtime_checkable` Protocol over frozen
  plain-data types carrying no engineering vocabulary, so an implementation
  authored in openDox conforms structurally without importing openxFactory, and
  `write_back` hands a request to the declared write path and returns a receipt
  rather than being a write path itself. OQ-1..OQ-4 were ruled on #656
  2026-09-06 and are realized here.
- [x] 2.2a `[oxF]` **STAND UP `openxFactory`'s OWN ADAPTER PACKAGE (RULING DQ-1)**
  beside `scripts/doc_health/`: one conformant implementation of the interface
  from 2.2 over THIS repository's corpus, reached by no route the interface does
  not define — no privileged direct call, no bypass for the home corpus, no
  operation a domain implementation cannot also declare
  (`corpus-adapter-seam` requirement 4, which this ruling makes load-bearing). It
  is built HERE and it STAYS here; it is what makes § 5's shed possible without a
  descendant. **DONE — same PR #725, squash-merged `ea4e6ff2`
  (`ea4e6ff2953c973df264ada3b8c7b986f31723f0`) 2026-09-06T17:43Z**:
  `scripts/corpus_adapter_openxfactory/` holds this repository's layout as DATA
  (`shape.py`/`home.py`, `home.py` the only module naming the home layout), so
  requirement 4's no-privileged-route is testable rather than asserted — proven
  by an AST guard with four mutations biting, a no-home-vocabulary test, and the
  factory-parameterized neutral conformance suite, 88 tests in all under
  `tests/corpus-adapter/`.
- [x] 2.3 `[oxF]` `authoring.py`'s `REQUIRED_HEADER_FIELDS` — today co-authoritative
  with `doc_health.corpus.STATUS_SCAN_LINES` — becomes a CLASSIFY response rather
  than a constant. **DONE — PR #728 squash-merged `1a2ea821`
  (`1a2ea821114baed9457be81c60c59f370c86ec71`) 2026-09-06T23:10Z, verified `gh pr
  view 728 --json mergeCommit`**: the required fields are now derived from the
  adapter's `classify` response, with the pre-change contract frozen as an oracle
  at `tests/header_contract_oracle.py`; parity was proven over 679 documents,
  the mutations bite, the import direction stayed one-way, and the doc-health
  delta against the PR's own base was zero (advisory recorded: ~1 ms per call at
  the single per-submission gate).
- [x] 2.4 `[oxF]` Split `serve.py` (6,733 lines) BY FUNCTION behind an app-server
  **route extension point**, and `cli.py` (2,456) behind a **subcommand extension
  point**, both still in-tree. Without the extension point the integration layer
  forks the server, which is a fork rather than a profile and breaks the same rule
  `domain-descendant-boundary` applies one level down. **This is the critical
  path and it cannot be done last.** **DONE in FIVE landed PRs, each merge commit
  verified with `gh pr view <n> --json mergeCommit`**: PR-1 **#736 →
  `a83eb93a`** (`a83eb93a6e69ef608a217079e963ed4427e5cd02`, 2026-09-07) landed
  `scripts/route_extension.py` and `scripts/subcommand_extension.py` — stdlib
  only, closed membership, empty defaults, zero behaviour change; OQ-1 **#741 →
  `75467fef`** (`75467fefd97a2f72e1f7f5be4a2f0b0cf55e52a9`) carved the
  `Status:`-header exemption rail to
  `scripts/ideation_dashboard/doxbench_status_exemption.py` so the generic packet
  module imports no `doc_health` — the FALLBACK route, ACCEPTED by Brett Heap
  2026-09-07 because `classify()` carries no status VALUE and widening the closed
  `Classification` is exactly what RULING OQ-2 refused; PR-2 **#748 →
  `7f7ce75a`** (`7f7ce75a043daf419961980c233ba192dfa7f538`) moved the openDox
  column out of `serve.py` as mixins — `serve_workbench.py`, `serve_project.py`
  and the shared wire vocabulary in `serve_wire.py`, re-exported so every
  `serve_mod.X` reader keeps resolving; PR-4 **#742 → `421b52d8`**
  (`421b52d8d11570ed761f6d4a1ed4462022734e1e`) split `cli.py` into `cli_gate.py`
  (openXdox), `cli_project.py` and `cli_model_binding.py` (openDox) named by
  `profile_openxfactory.py`, with the 31-entry `--help` golden byte-identical;
  PR-3 **#761 → `7992b87a`** (`7992b87a622a7c81d2c31dd9af0ec497fdf77b3a`)
  extracted `serve_gate.py`, `serve_projection.py` and
  `serve_openxfactory_lanes.py` THROUGH the route extension point, with RULING A
  applied — `route_extension.collect_bindings` now fails closed on an exact
  pattern under an already-declared prefix, in either declaration order, so no
  caller-supplied extension can sit under a contributed gate prefix. RULING (a)
  (Brett Heap, 2026-09-07) governs the test edits throughout: tests that pin
  WHERE code lives are repointed to the module now holding the moved code, at the
  same strength, disclosed and mutation-proved.
- [x] 2.5 `[oxF]` `[OmI]` `[xF]` **HARDEN THE APPLY LANE BEFORE IT BECOMES THE ONLY
  WRITE PATH.** RULING Q1 promotes a path with ONE dispatch in its entire history
  (`intent-apply.yml`, 2026-08-15T01:22:04Z, success) to carrying every governed
  write from every tenant instance. Evidence is a real dispatch and a real
  refusal, not a dry run — the bar the wallet arc and the nightly-refresh lane
  both established. **PRECONDITION of § 3, not a follow-up.**
  **DONE — D-2 live exercise COMPLETE 2026-09-09T06:37:45Z** (`#656` comment
  `5597232065`): a real dispatch (act A — intent applied at `e970dfec`,
  `codexfactory[bot]` APPROVED, auto-merged into `intents/rolling` as openxFactory PR #176 →
  `7681e409890a64027018edd46593f2973ada4c86`) and a real refusal (act B — the D4
  stale-view rung, commit `36d07ecf`, run 34229563533; recorded live
  2026-09-08T13:30Z, comment `5585923935`), not a dry run. Eight defects found
  across six live runs, each fixed by its own verified, Brett-worded PR:
  openxFactory #808 → `2ef7d8c27c56cbf95c51db4a420d0e96d9f16e50`, #814 →
  `c991c0f34adb328980bfbaff17b807725683ad80`, #816 →
  `892423040a41c7c277c45bcf8474fefd3dce6bc3`, #830 →
  `202c170d8d56bf82c26facbc84ca13ebfa52ae7e`, plus xFactory #345/#362/#369.
  **Reading of `[OmI]`**: the box's own text names no Omnigent-Install-specific
  act — the evidentiary bar it states is "a real dispatch and a real refusal,
  not a dry run" against the apply lane (`intent-apply.yml`, hosted in xFactory
  `[xF]`, dispatching openxFactory's `[oxF]` `merge-master-approval`); `[OmI]`
  is a repository tag on the box with no clause behind it, so it ticks on the
  `[oxF]`/`[xF]` evidence alone, with no Omnigent-Install act in the record.
- [x] 2.6 `[oxF]` The whole group lands green:
  `python3 -m pytest tests/ideation-dashboard tests/doc-health` and
  `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`. **DONE — both gates
  run on THIS branch (off `origin/main` `7992b87a`), 2026-09-07**: `python3 -m
  pytest -q tests/ideation-dashboard tests/doc-health` → **1 failed, 6,681
  passed, 31 skipped, 7 warnings in 788.47s**, the only failure being the known
  ENVIRONMENTAL `tests/ideation-dashboard/test_snapshot.py::test_find_validator_locates_pinned_checkout`,
  which looks for a pinned sibling checkout this worktree does not carry and
  which fails identically in a fresh `origin/main` worktree (re-run there, same
  assertion); `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` → **98
  passed, 1 failed (99 items)**, the only failure being the known local-CLI
  artifact `change/disposition-codexfactory-declared-renames` (CI's pinned CLI
  passes it); and the change-local `OPENSPEC_TELEMETRY=0 openspec validate
  split-opendox-two-layer-product --strict` → `Change
  'split-opendox-two-layer-product' is valid`. Also measured here: `python3
  scripts/proposal-support.py . verify` → `proposal support verification ok`,
  and the `doc-health --single-repo .` report is BYTE-IDENTICAL to the one a
  fresh `origin/main` (`7992b87a`) worktree produces — 9 critical / 8 error /
  58 warning / 15 info on both sides, zero delta.

### § 2 carried items (recorded 2026-09-07, not applied)

Twelve things the § 2 landings established that this packet's normative text does
not yet reflect. They are RECORDED here and NOT applied: none is a § 2 defect,
each is decided where its line says, and `design.md` is deliberately untouched by
the bookkeeping that ticks this group.

- (a) `design.md` § D3 files `doxbench_packet.py` whole under the
  openxFactory-adapter column. After #741 that row is TWO rows — the generic
  packet module goes to openDox, and `doxbench_status_exemption.py` (which keeps
  the direct `doc_health` import) stays in the adapter column. § 3.1 carve
  manifest.
- (b) The generic packet module still imports `doxbench_scope`
  (`scripts/ideation_dashboard/doxbench_packet.py:78`,
  `ScopeKey`/`ScopeProjection`), which `design.md` files under openXdox — a
  cross-column edge the manifest has to resolve rather than inherit. § 3.1.
- (c) The post-carve default when the adapter-column module is ABSENT — today a
  loud `AttributeError` on the alias, versus a declared neutral posture — is
  left open by the OQ-1 ruling and is a § 3.1 decision.
- (d) The § 2.4 spec memo's § 2 assigns `CAPABILITIES_ROUTE` handling and
  `_session_repository` to `serve_project.py`; both STAY core, on test evidence
  from #748. The memo correction is owed before the § 3.1 manifest.
- (e) `cmd_generate_and_open` stays in `cli.py` (the assembly column), not
  `cli_project.py` — Brett Heap's call at § 3.1.
- (f) The gate column carries **19** `cmd_gate_*` verbs, not the memo's 17
  (counted on this branch in `scripts/ideation_dashboard/cli_gate.py`).
- (g) The travelling gate column carries the CLI's ONLY `doc_health` import
  (`cli_gate.py:251`, `from doc_health import derive_possibles`, inside
  `cmd_gate_dispose_possible`). § 3.1 decides its home.
- (h) `/snapshot.json` stays a CORE arm: its handler moved to
  `serve_projection.py` with its neighbours, but the arm tests
  `path == self.snapshot_route`, a per-server keyword a frozen
  `RouteBinding.pattern` cannot carry — contributing it would break
  `build_server(snapshot_route=…)`. § 3/§ 4 follow-up.
- (i) Core→column import edges remain in-tree: `cli.py → profile_openxfactory →
  cli_gate`, and `serve.py` imports the three route columns at module scope for
  the mixin bases. The seam is in-tree until the carve; § 3 resolves it.
- (j) `opensoft/openxFactory`#768 — `serve_openxfactory_lanes`'s `dtn-seed` and
  `staging-seed` assume a JSON OBJECT body. Pre-existing, found while moving
  them in § 2.4 PR-3, filed and UNCLAIMED.
- (k) `tests/ideation-dashboard/test_cli_column_split.py`'s surface-tuple
  non-vacuity floor names only `cli_gate.py` and `cli.py` — 2 of the 5
  `CLI_SURFACE` members. Follow-up, not a § 2 blocker.
- (l) § 2.4's own text cites `serve.py (6,733 lines)` and `cli.py (2,456)`,
  which were the figures at ratification (`ceb6dc9e`). Measured immediately
  before each split: `serve.py` **6,914** (at `5e4d960c`, PR-2's base) and
  `cli.py` **2,487** (at `f756a91f`, PR-4's base). Measured on this branch after
  the split: `serve.py` **1,748** and `cli.py` **996**. Recorded, not corrected
  in place.

## 3. The openDox carve — with the mapping manifest

> Amended 2026-09-05 — repository shape. Every destination path this group names
> at "openDox" lands in the **`opensoft/openDox-code` leg**, except requirements
> and decisions, which land in **`opensoft/openDox-spec`**, and the release
> identity, which is cut in the **assembly root** (3.8). The carve manifest of
> 3.1 therefore names a destination REPOSITORY as well as a destination path —
> the field it already carries, now answered with a leg. Nothing else in the
> group moved.

- [x] 3.1 `[oxF]` **FLOOR PART 1 (RULED OQ-1).** Emit
  `docs/opendox-carve-manifest.yaml` at the **NAMED CARVE COMMIT** BEFORE any file
  moves: for every file under the moved paths, its `openxFactory` path, its
  `sha256` at that commit, its destination repository and path, and one of exactly
  three dispositions — `moved_verbatim`, `moved_with_declared_edit`, or
  `not_moved` with a reason. **The edit-class list is CLOSED and is the ruling's
  own, verbatim: `import rewrites`, `path constants`, `adapter calls`** — three,
  not four; the packet's earlier "vocabulary parameterization" is not carried, so
  such an edit is either expressible as one of the three or it is not a carve edit
  and belongs to a later change. **A file in no row, or an edit in no class, is an
  UNDECLARED MOVEMENT and the carve REFUSES.**
  **DONE — openxFactory #865 → `17167481e9d69dec9347f1d26699b6218a697f53`,
  2026-09-09T22:20:29Z** (head `a0979c91`): `docs/opendox-carve-manifest.yaml`
  emitted at `carve_commit` `b075fd91dc8fced8e1373825ba80220c33536bae` (tag
  `opendox-carve-0`), 454 rows, before any file moved; independently
  re-verified PASS (454/454 surface, 318/318 digests). Amended by **#889 →
  `15ebb37d483b4bfd0665844967d2699a7be3df33`**, 2026-09-10T04:28:06Z (RULED
  Q-L1): 456 rows (172 `moved_verbatim` / 146 `moved_with_declared_edit` / 138
  `not_moved`, 20 replicas). `#656` comment `5609537944`: "**§ 3.1 IS
  COMPLETE**". (A further grammar amendment, PR #895 — RULED Q-L7 — is still
  OPEN and is not cited as landed.)
- [x] 3.2 `[oD]` Carve openDox's ~24.9K of modules **into `openDox-code`** per `design.md` § D3, plus the
  PULL-UP wave: `doxbench_knowledge` (1,231), `doxbench_abstract_store` (446) and
  the abstract-generation surface, the keyword-query half of `lens` (282), and
  `notebook_action` (239). **The stage-to-book mapping does NOT come up** — a
  per-project book is the neutral shape.
  **DONE — opensoft/openDox-code #6 → `ce53b489f8007c37f70da19c90c95ba89156feed`,
  2026-09-10T12:37:23Z** (re-cut under RULED Q-L4; history-preserving
  `filter-repo`, RULED OQ-H; independent verification: three-way digests
  123/123, phase A + B OK): all 123 `opendox_code`-destined manifest rows
  arrived. Cross-checked against `design.md` § D3's openDox column and the
  landed manifest (`docs/opendox-carve-manifest.yaml` at `15ebb37d`): every
  named module — the PULL-UPs (`doxbench_knowledge`, `doxbench_abstract_store`,
  the abstract-generation surface inside `doxbench_turns`, `notebook_action`,
  the keyword-query half of `lens`) and the rest of the column
  (`doxbench_turns/threads/model`, `canvas_drafts`, `doxbench_hash/bridge/
  provider/intake/binding/mcp/memory_gateway/telemetry/install`,
  `branch_session`, `session_git`, `session_pr`, `actor_identity`, `boundary`,
  `action_errors`, `fixtures`, `__init__`) — carries a manifest row with
  `destination: opendox_code`, disposition `moved_verbatim` or
  `moved_with_declared_edit`. Live-verified on `opensoft/openDox-code` main:
  `gh api repos/opensoft/openDox-code/contents/src/opendox` lists every one of
  them present.
- [x] 3.3 `[oD]` The app-server half of `serve.py` and the neutral half of
  `cli.py`, carrying the extension points § 2.4 created. **Both in `openDox-code`.**
  **DONE — landed inside the same PR, opensoft/openDox-code #6 →
  `ce53b489f8007c37f70da19c90c95ba89156feed`**: the manifest routes
  `serve.py`/`serve_wire.py`/`serve_workbench.py`/`serve_project.py` (the
  app-server half — `serve_projection.py`/`serve_gate.py`, the gate/neutral
  mechanism S-3 and RULED B-2 (i′) moved out, go to `openxdox_code` instead)
  and `cli.py`/`cli_project.py`/`cli_model_binding.py` (the neutral half —
  `cli_gate.py` goes to `openxdox_code`) all to `destination: opendox_code`;
  the § 2.4 extension points (`route_extension.py`, `subcommand_extension.py`,
  first landed at openxFactory #736 → `a83eb93a6e69ef608a217079e963ed4427e5cd02`)
  arrive as declared replicas (RULED Q-L1). Live-verified on
  `opensoft/openDox-code` main: `src/opendox/` carries `serve.py`,
  `serve_wire.py`, `serve_workbench.py`, `serve_project.py`, `cli.py`,
  `cli_project.py`, `cli_model_binding.py`; `src/` carries `route_extension.py`
  and `subcommand_extension.py` at top level.
- [x] 3.4 `[oD]` **INVENT the front-end package boundary** in `openDox-code` — 40
  files, 30,410 lines, and no boundary exists to discover. Account menu, canvas, editor, chat,
  docs tile and theme controls are openDox; the gate console and drill-in are the
  gate loop; the wheel, funnel and lens regions carry stage names. **This is where
  a student-usable openDox is won or lost**, and it is its own task rather than a
  consequence of the Python split.
  **STATUS — 2026-09-14, tick JUDGED MET AT THIS AMENDMENT'S OWN LANDING: the
  boundary was INVENTED as a design note and REALIZED in an eight-slice arc.**
  **SEVEN** of the eight are merged as this is written; **S8 lands AHEAD of
  this amendment** in the lane's recorded order — it is the one row still
  carrying `[FILL AT LANDING]` below — so the tick is written for the state
  this pull request lands INTO and not for the state it was authored in, and
  the box is not ticked ahead of it. *(S7's row was filled in place at its own
  landing, 2026-09-15, from the merged pull requests: `#1030` →
  `b3a75537217d9b15684501684e9527f412d4e6b6` at **21:40:25Z** and openDox-code
  `#21` → `1e4697130855e9695a6acc3344b7c925bb3eeb09` at **21:41:36Z** — Q-L1's
  annotation-first rule holding a seventh time, by 71 seconds. The paragraph
  read "Six of the eight … S7 and S8 land AHEAD" until then.)* That is the discipline `openDox-spec`'s
  own amendment #3 applies to its § 5.0 landing record, which this table
  mirrors.

  **The boundary** is `openDox-spec` `docs/front-end-package-boundary.md` — the census,
  the three destination classes (A openDox core / B the gate loop / C the
  stage-named region), the registration mechanism, the four assertions and the
  slice plan — landed at openDox-spec **#8 → `a44ac06d`** and amended three
  times: **#9 → `61866d29`** (amendment #1, the five rulings Q1–Q5),
  **#10 → `7d12428c`** (amendment #2, five corrections and Q6), and
  **#11 → [FILL AT LANDING — merge sha]** (amendment #3, the S8 premise RULED,
  the deferred re-measurement taken, a fifth declared class-A tail, and every
  open question closed). Its § 6's SIX questions are all RULED and its § 5.1
  counterpart's twelve are too. The realization, one row per slice, each leg
  pull request paired under RULED **Q-L1** with the openxFactory row annotation
  that lands FIRST — only S1 has none, because it creates files and edits no
  carved row (the manifest names no slice S1); the order is visible in the
  clock, S2's annotation merging 15:45:51Z and its leg 15:59:44Z on
  2026-09-12:

  | slice | what it did | openxFactory (Q-L1) | openDox-code | openXdox-code |
  | --- | --- | --- | --- | --- |
  | S1 | declare the census as DATA + the four assertions | — (created files) | `#13` → `e86deb2d` | — |
  | S2 | the intent chips become an optional contributed binding (RULED Q5) | `#1002` → `b3cc0181` | `#15` → `c7ab3d87` | — |
  | S3 | the view registry — `ViewBinding` + `collectViewBindings` | `#1001` → `f663b379` | `#14` → `c5edac88` | — |
  | S4 | split the three RULED `SPLIT` files — thirteen route tails | `#1010` → `bcde1575` | `#17` → `69d27602` | — |
  | S6 | `/source` becomes openDox's own fixed core arm (RULED Q4) | `#1009` → `468371dc` | `#16` → `3661345f` | `#17` → `d6e7bbe3` |
  | S5 | contribute the gate loop — six class-B modules leave | `#1023` → `ee251d6c` | `#20` → `8efb3cf5` | `#18` → `c1ad341a` |
  | S7 | parameterize class C — the display facet and the context hop | `#1030` → `b3a75537` | `#21` → `1e469713` | — |
  | S8 | re-point the bundle paths, un-narrow `validate` for the web suites | `#1025` → **[FILL AT LANDING]** | `#23` → **[FILL AT LANDING]** | `#19` → **[FILL AT LANDING]** |

  Two acts of the floor belong to the arc and are named with it: RULED **Q6**'s
  `re_destined:` row form, built for S8 and landed at openxFactory
  **#1011 → `880c821c`** — and then used by S5's four rows and by none of S8's,
  which the note records as a finding; and the **`retired:` row form**, RULED at
  `#656` comment `5656343213` as the NEXT carve-floor act, with the retirement
  of the three intent-feed suites under it (openDox-code
  `tests/test_intent_tray_dom.py` + `tests/test_wheel_verbs_dom.py`,
  openXdox-code `tests/test_staging_workbench.py`'s ending replay, all three
  driving `views/intent-feed.js`, RULED `not_moved` and present at neither leg).
  Both are registered acts under their own claims, not conditions of this box.
  **A THIRD act of the floor followed the arc's seventh slice and is named here
  because it is what carries these landings into the aggregation** — the **pin
  lockstep**, whose second run is openxFactory **`#1054` →
  `3c614d340777cb1ff825c04dbc78d98af1dc875e`** (2026-09-15T23:27:40Z). Read
  from that merge commit's own diff rather than from its title: it moves
  `contracts/opendox-pin.yaml`'s `commit:` `7cf6c143` → **`3819625e`** (the
  openDox assembly root, `opensoft/openDox` `#8` at 21:48:52Z, which names
  `code` leg **`1e469713`** — slice S7's own merge) and
  `contracts/openxdox-pin.yaml`'s `76df74c8` → **`a6500141`**
  (`opensoft/openXdox` `#10` at 21:54:21Z), with BOTH gitlinks moving in that
  one commit, which is the lockstep invariant §§ 4.2 and 5.1 of this file
  describe. It is the bump the boundary note's § 1.2(d) SKIP waits on, arriving
  at the aggregation level; like the two acts above it is its own claim and not
  a condition of this box.

  **THE PACKET FIGURE, AMENDED HERE — this box's own "40 files, 30,410 lines"
  is a design-time reading no tree in the arc reproduces**, and the boundary
  note defers its correction to the packet in terms (*"a packet figure is
  amended in the packet"*, its § 1.1). Re-measured 2026-09-14 over every blob
  under each tree's bundle root, each named with the tree it was read at:

  | tree | blobs | lines | hand-authored |
  | --- | ---: | ---: | --- |
  | openxFactory `scripts/ideation_dashboard/web/` at the carve commit `b075fd91` (tag `opendox-carve-0`) | 43 | 31,068 | 41 files / 31,066 lines |
  | openDox-code `a99eba03` — the note's census tree | 42 | 30,585 | 40 / 30,583 |
  | openDox-code `main` `8efb3cf5` — S1–S6 landed | 41 | 30,477 | 39 / 30,475 |
  | openDox-code `#21` head `c7a216c7` — the ARC-COMPLETE bundle | 42 | 31,955 | 40 / 31,953 |

  **The FILE count is right; the LINE count is 173 short.** The carve step is
  one file and is exactly accounted for: `views/intent-feed.js` (483 lines)
  did not travel, RULED `not_moved / stays_openxfactory_adapter` under OQ-F,
  and taking that one file out of 41 files / 31,066 lines leaves **40 /
  30,583** — the
  packet's "40 files" on the nose, its "30,410 lines" **173** short of what
  arrived and **656** short of what the carve commit held. Everything after
  that is the arc itself (five files in before S5, six out with S5, one in
  with S7), which is why the arc-complete bundle is 40 hand-authored files
  again at 31,953 lines. **FOUR other occurrences in the packet's LIVE
  documents carry this figure and NONE is edited here** — `design.md`:52 and
  :351 and `proposal.md`'s `code_surface:` line each pair *"40 files"* with
  *"30,410"*, and `proposal.md`:208 carries the line count alone (*"30,410
  lines of front end"*) — because a ratified document is amended by an act that
  CLAIMS it, and this box claims neither. What it does is record the
  measurement, so the act that amends them does not have to re-derive it.
  **A FIFTH occurrence is in the packet and is of a different kind**, named so
  that a later reader who greps for `30,410` and finds five does not read it as
  one this box missed: `review/ratification-2026-09-05.md`:549 quotes the
  figure inside the residual question `design.md` § D3 left open AT
  ratification. That file is a RECORD — `Status: ratified`, decision date
  2026-09-05, ratified baseline `6935fb8b` — of what the packet said on the day
  it was ratified, so no later act amends it, including the act that corrects
  the four live ones.

  **What the arc did NOT close, named so no later reader takes the tick for
  more than it is** — every item is someone else's act under its own claim and
  none is a condition of this box: (i) the FIFTH declared class-A tail
  (`views/viewer.js`:262, the rendered stage pill) is DECLARED by amendment #3
  and not built — it owes a census `tail:`, the `18` → `19` constant in the
  three places `tests/test_web_boundary.py` spells it, and a Q-L1 annotation,
  because that file's carve row is `moved_verbatim` with no `edits:`; (ii)
  `views/lens.js` stays class `?` with its two openxFactory-lane sites as
  assertion 2's declared exception until a ruling names its destination — the
  one RULING gap in the note; (iii) the FULL un-narrowing of both legs'
  `validate` waits on the BUILD arc, which RULED **Q-L5 (b′)** and **Q-L8 (b′)**
  each say in terms (S8 lifts it for the web suites only, and
  `tests/test_consumer_reach.py`'s `STILL_REACHING` asserts the openDox half
  still fails); (iv) the two floor acts above; and (v) **the packet's own
  README entry, overtaken and NOT corrected here** — the packet's OpenSpec
  Records entry in `README.md` still reads *"IT STILL PERFORMS NOTHING. No
  repository is created, no code moves …"*, written 2026-09-05 (`ceb6dc9e`,
  `8b297c2f`) when that was exactly true and no longer is: `openDox-code` and `openXdox-code` exist and were cut
  from the carve commit `b075fd91` (tag `opendox-carve-0`), and six of the
  eight slices above are merged. The staleness predates this amendment and is
  not made by it; it is left to the act that CLAIMS that text — the same rule
  this box applies to `design.md`'s and `proposal.md`'s four *"30,410"*
  occurrences — which is the packet's ARCHIVAL act, the README **OpenSpec
  Records** block being both where an archived packet's entry is rewritten and
  (lane-collision protocol, Rule 6) the one block a landing window exists to
  serialize. Recorded here so that act does not have to rediscover it.
  **That entry is cited by its SENTENCE and not by a line number, deliberately,
  and it is the one citation in this box that could not be one.** Every other
  measurement here names the tree it was read at; this one can name no line,
  because the block it sits in is rewritten by every archival act and its line
  numbers move under any citation that outlives one. Measured rather than
  asserted: the entry opens at `README.md`:**1875** at this amendment's own
  head and at :**1775** at openxFactory `main` `8944758c` — exactly **100**
  lines apart, after `#1042` archived a sibling packet above it — while
  `design.md`:52 and :351, `proposal.md`:208 and
  `review/ratification-2026-09-05.md`:549, the four `30,410` citations above,
  are each exact at BOTH heads, because no act has touched those three files
  since. *(This clause read "`README.md`:1875–1879" until fix round 4, which
  measured the drift rather than re-pointing a number that moves again at the
  next archival.)*
  `#656` records: CLAIM
  `5656686020`; rulings `5642758731` · `5647678655` · `5648044785` ·
  `5648049748` · `5648065587` · `5649094228` · `5656343213`.
- [ ] 3.5 `[oD]` The runtime, on the `xFactory-Hermes-Install` pattern (RULING
  Q2): FastAPI + Postgres, `migrations/` (ordered SQL, `0001` pinned canonical
  plus additive), `deploy/compose/` and `deploy/kubernetes/` — **all at the root
  of `openDox-code`, not of the assembly root** — one lifecycle CLI,
  OIDC through the Keycloak broker. The schema holds ONLY identity and
  coordination (RULING Q1): users, memberships, projects, the
  project-to-repository map, sessions, unsaved drafts.
- [ ] 3.6 `[oD]` **openDox CREATES A REPOSITORY AS A FIRST-CLASS ACT**, or the
  origin complaint returns one level down: RULING Q1 answers *"no good place to
  store my projects"* with its coordination half while the specs still land in a
  repository. Includes RULING C3's standalone shape — a PLAIN LOCAL GIT
  REPOSITORY per project, commits as the write path, a remote attachable later —
  as the trivial conformant adapter implementation, not as a mode.
- [ ] 3.7 `[oD]` `[oXd]` `[oxF]` **FLOOR PART 3 (RULED OQ-1).** The neutral
  conformance corpus — no `openspec/`, no `contracts/`, no lifecycle headers,
  positives plus negative confirmations — and **EVERY DESTINATION PASSES IT**, the
  ruling's own word: openDox, openXdox's adapter implementation, AND
  `openxFactory`'s own adapter from § 2.2a. That last one is the only mechanical
  proof that the home corpus has no privileged route.
  **NOT TICKED — the machine is built and the answer it returns is NO, at
  openxFactory #920, 2026-09-10.** The box asks for two things and only one of
  them was ever missing. The CORPUS exists: RULED OQ-3 (2026-09-06) seeded it
  at `tests/corpus-adapter/fixtures/` — three documents in two roots of their
  own under a two-field header vocabulary belonging to no governed repository,
  plus an empty sibling and a non-directory — and eleven manifest rows name
  those exact paths `not_moved / replicated_at_destination`, so it is not
  relocated and no second copy is authored. What did not exist is a way to run
  it against a reader `openxFactory` did not author, the seed being
  `pytest`-bound to a factory named in the file. That lands here:
  `scripts/carve_conformance.py`, the corpus as a closed set of **17 checks**
  (10 positives, 7 negative confirmations) over any reader, stdlib plus
  `corpus_adapter` only and held to the interface's own no-home-vocabulary
  scan; `scripts/verify-carve-conformance.py`, the runner in
  `verify-carve-arrival.py`'s idiom (`--destination`/`--dest-root`, exit 0 or
  2, five refusal codes, a `--json` seat, the seat-holding pass); and
  `tests/carve_conformance/` (34 tests; six non-conformant readers each
  failing the check that catches it, three live mutations of the corpus each
  turning its own case red, and one reader raising its OWN refusal class —
  every destination holds a replica of the interface — asserted to PASS).
  **Measured at each destination's then-current main, 2026-09-10:**
  `openxfactory` (§ 2.2a) **OK — 17 of 17**; `opendox_code` `8e9ffa62`,
  `openxdox_code` `59600412`, `opendox_spec` `41d570e9` and `openxdox_spec`
  `03eacc61` each `conformance-adapter-undeclared`. openDox-code holds the
  INTERFACE replica at `src/opendox/corpus_adapter.py` — byte-identical to the
  carve blob at `b075fd91` (`a0d971d6…`) and a `runtime_checkable Protocol`
  whose six methods are docstring-only, so pointing the runner at it returns
  `TypeError: Protocols cannot be instantiated` — and no implementation of it;
  an AST census over all four legs (91 / 1 / 98 / 1 `.py` files) finds no
  class defining the six operations anywhere but that Protocol, which
  independently reproduces the corpus-adapter non-placement leg 3 recorded and
  its verifier confirmed (`#656` comments `5621296616`, `5621719657`).
  **ONE of the three named destinations passes, so the box stays open**: the
  missing readers are § 3.6's "trivial conformant adapter implementation" for
  openDox and § 4's mapping core for openXdox, and they are build tasks at
  those destinations rather than findings against the corpus — narrowing the
  corpus to what the legs pass today would be FLOOR PART 3 deleted to tick
  FLOOR PART 3. § 3.8's tag waits on it. Runbook § 2.2 carries the runner, the
  refusal table and the same verdicts.
- [ ] 3.8 `[oD]` Cut `dox-v1.0` only after the floor's four parts are green.
  **In the ASSEMBLY ROOT** (amended 2026-09-05), over the commit that names both
  legs: a tag on a leg describes half a project, and the bundle tag,
  `contracts/manifest.yaml` and `contracts/CHANGELOG.md` live where a consumer's
  pin points.

## 4. The openXdox mapping core

> Amended 2026-09-05 — repository shape. Same leg rule as § 3: code into
> `opensoft/openXdox-code`, requirements and decisions into
> `opensoft/openXdox-spec`, pins and the release identity in the assembly root
> `opensoft/openXdox`.

- [x] 4.1 `[oXd]` Carve openXdox's ~10.9K **into `openXdox-code`** per `design.md` § D3: the adapter
  implementation and projection mechanism, the gate-and-commission loop, and
  `doxbench_scope`. Of `design.md` § D3's 23 outbound `doc_health` imports,
  **TWELVE become the adapter's IMPLEMENTATION SURFACE here**, where importing
  doc-health is lawful; **FIVE are lawfully `openDox`'s**, **ONE stays in
  `openxFactory`** under RULED DQ-1, and **FIVE were DISCHARGED at the § 2 seam**
  and no longer exist as imports at all. *(AMENDED 2026-09-16 by RULED **R-1**,
  `#656` comment `5690428146`. This sentence read "The 23 outbound `doc_health`
  imports become the adapter's IMPLEMENTATION SURFACE here, where importing
  doc-health is lawful" — a design-time expectation that the § 2.1 / 2.2 / 2.2a
  seam overtook before any carve ran, which the STATUS below measured and
  registered without deciding. The ruling settles it on that measured accounting
  and orders **no further carve**.)*
  **STATUS — 2026-09-11, tick NOT YET DUE (partially met), verified against
  `openXdox-code` main (`af15f71207797214ffd6340267b5cb2ecb40bf6a`, the pin
  landed at `#656` comment `5640535165`).** MET: all thirteen named modules
  are present in `src/openxdox/` — the seven "adapter implementation and
  projection mechanism" modules (`corpus_root.py`, `generator.py`,
  `snapshot.py`, `snapshot_registry.py`, `register.py`, `completeness.py`,
  `round_trip.py`), the five "gate and commission loop" modules
  (`gate_console.py`, `gate_routes.py`, `kickoff.py`, `record_binding.py`,
  `register_edit_lane.py`), and `doxbench_scope.py`. NOT MET: the second
  sentence's own claim, that all 23 outbound `doc_health` imports `design.md`
  § D3 counts (12 modules: `authoring` 2, `cli` 1, `completeness` 1,
  `corpus_root` 1, `doxbench_packet` 1, `gate_console` 4, `gate_routes` 1,
  `generator` 3, `round_trip` 1, `serve` 3, `snapshot_registry` 1, `workbench`
  4) become the adapter's implementation surface HERE. Live count in
  `openXdox-code`'s `src/`: 12 of the 23 (`completeness` 1, `corpus_root` 1,
  `gate_console` 4, `gate_routes` 1, `generator` 3, `round_trip` 1,
  `snapshot_registry` 1 — exactly the seven landed adapter/projection
  modules). The other 11 do not relocate here today: `doxbench_packet`'s 1 is
  RULED (DQ-1) to stay in `openxFactory`'s own engineering adapter and never
  comes here; `authoring` (2), `cli` (1), `serve` (3) and `workbench` (4) are
  the residue that splits BY FUNCTION between openDox and openXdox, owed to
  § 3.4 / 3.5 / 3.6, which the RECOUNT (`#656` comment `5638391057`) still
  lists open. `openXdox-code` also carries one further live `doc_health`
  import outside the original 23 — `cli_gate.py:251` — a new site from the
  § 4.3 routes/subcommands build, not one of `design.md`'s inventoried twelve
  modules. Box stays open until the residue carve resolves where the
  remaining imports land.
  **STATUS — 2026-09-14, box STAYS OPEN, and the residue is now fully
  accounted for: § 3.4 moved none of it, and five of the eleven were
  DISCHARGED BY THE § 2 SEAM rather than relocated.** Re-measured 2026-09-14 at
  four trees — openXdox-code `main` **`c1ad341a`** (S5 leg A landed),
  openDox-code `main` **`8efb3cf5`** (S1–S6 landed), openxFactory `main`
  **`e6e1c968`**, and the carve commit **`b075fd91`** both legs were cut
  from — counting only real import statements
  (`^\s*(from|import)\s+.*doc_health`), each under the root that repository
  actually keeps the inventoried modules in: `src/openxdox/` at openXdox-code,
  `src/opendox/` at openDox-code, and `scripts/ideation_dashboard/` at
  openxFactory (both at `main` `e6e1c968` and at the carve commit — openxFactory
  has no `src/`, which is why a single root spelling would not reproduce).
  All 23 of
  `design.md` § D3's inventoried outbound imports now have a position:

  | where the 23 stand | count | sites |
  | --- | ---: | --- |
  | `openXdox-code` `src/openxdox/` (the adapter's implementation surface, as 4.1 asks) | **12** | `completeness` 1, `corpus_root` 1, `gate_console` 4, `gate_routes` 1, `generator` 3, `round_trip` 1, `snapshot_registry` 1 |
  | `openDox-code` `src/opendox/` | **5** | `serve.py`:710 `from doc_health.corpus import RealGit`; `workbench.py`:746, :1407, :1408, :1409 |
  | RULED to stay at `openxFactory` (DQ-1) | **1** | `design.md` § D3 inventories it at `doxbench_packet`; the import had already moved by the carve commit and the LIVE site is `scripts/ideation_dashboard/doxbench_status_exemption.py`:63 — `from doc_health.lines import split_keepends`, the same line at `b075fd91` and at `main` `e6e1c968` (reading (ii) below) |
  | **DISCHARGED at the § 2 seam** — the import became an adapter call or a late seam read, so there is nothing left to relocate | **5** | `authoring` 2 → `authoring.py`:317–318, `from .corpus_adapter import DocumentId` + `from corpus_adapter_openxfactory import home_corpus`; `cli` 1 → gone, only the path comment at `cli.py`:14 survives; `serve` 2 of 3 → gone before the carve (openxFactory `b075fd91` already reads one, at `serve.py`:618), the leg's own late seam reading `from opendox import consumer_reach` at `serve.py`:146 |

  **The five DISCHARGED were discharged at the SEAM, before the carve, and the
  carve commit proves it.** At openxFactory `b075fd91` (tag `opendox-carve-0`,
  the tree all three legs were cut from) `scripts/ideation_dashboard/` carried
  **21** `doc_health` import sites: `authoring` **0** (was 2), `cli` **0**
  (was 1) and `serve` **1** (was 3) — the five already gone, taken by § 2.1's
  neutral module and the § 2.2 / 2.2a adapter seam rather than by any carve;
  the twelve adapter/projection sites intact; `workbench` 4 intact;
  `doxbench_packet`'s one already relocated to
  `doxbench_status_exemption.py`:63; **plus three sites outside `design.md`'s
  inventoried 23** — `cli_gate.py`:251 (§ 4.3, which this box already records)
  and `serve_openxfactory_lanes.py`:162 and :253, openxFactory's own lane
  adapter, which stayed and is still there at `main` `e6e1c968` (:178, :277).
  The arithmetic closes both ways: 12 + 4 + 1 + 1 = **18** = 23 − 5, and
  18 + 3 = **21**. The carve then routed those 18 by column, which is the
  table above; no later act moved any of them.

  **Three readings.** (i) **The § 3.4 arc moved none of them.** openXdox-code
  carries **13** live `doc_health` import sites across **8** modules — the
  same files at the same line numbers at `af15f712` (this box's own
  verification head), at `main` `c1ad341a` and at `#19`'s head `080dcfcd`.
  The boundary arc is a WEB-tier act and never touched the adapter surface, so
  nothing in 4.1 turns on it. The 13 are the 12 above plus `cli_gate.py`:251,
  the § 4.3 site this box already records as outside `design.md`'s inventoried
  twelve. **Exactly one of the 13 differs in TEXT across those heads, and not
  by a § 3.4 act**: `generator.py`:66 reads `from doc_health import TAXONOMY,
  corpus` at `af15f712` and `from doc_health import corpus` at `c1ad341a`,
  because openXdox-code `#16` → `17384c07` (§ 4.4's vocabulary half) took
  `TAXONOMY` out of it. Same site, same line, one name fewer. (ii) **`openxFactory` holds none of the
  residue at the source any more, and the one RULED to stay is not where this
  box assumed.** The § 5.2 shed has landed: `scripts/ideation_dashboard/` is
  down to **10 files**, an identical set at `main` `a80f0e3c` and at `main`
  `e6e1c968`, none of them `authoring`, `cli`, `serve`, `workbench` or
  `doxbench_packet`. `doxbench_packet`'s one DID stay at openxFactory, as DQ-1
  requires — but the module it stayed IN is the § 2.4 one rather than the DQ-1
  adapter package: the `doc_health.lines.split_keepends` import travelled with
  the `Status:` read that used it into
  `scripts/ideation_dashboard/doxbench_status_exemption.py`:63 under RULED
  OQ-1, which openDox-code's own `src/opendox/doxbench_packet.py`:136–142
  states in terms (*"they took their `doc_health.lines.split_keepends` import
  with them … it can no longer take an openxFactory-only `doc_health`
  dependency along"*) and :66–67 asserts by a neutrality scan. Either module
  is openxFactory, so the box's *"never comes here"* holds; the placement is
  recorded because a citation of the DQ-1 package for this import would not
  reproduce. Separately, that DQ-1 ENGINEERING ADAPTER imports `doc_health` in
  **six** places of its own — `scripts/corpus_adapter_openxfactory/adapter.py`:58,
  `check.py`:39–41, `classify.py`:38, `home.py`:59 — and that is where the
  DISCHARGED `authoring` pair's dependency now sits, behind the § 2.2a seam
  instead of travelling to a leg: `authoring.py`:317–318 calls
  `corpus_adapter_openxfactory.home_corpus` (defined at `home.py`:160,
  re-exported at `__init__.py`:32) and `home.py`:59 is the `doc_health` import
  that call reaches. Importing doc-health THERE is lawful, which is the whole
  of DQ-1. (iii) **This box's second sentence
  cannot be met AS WRITTEN, and that is a reconciliation owed rather than a
  residue still travelling.** *"The 23 outbound `doc_health` imports become the
  adapter's IMPLEMENTATION SURFACE here"* is a design-time expectation that the
  § 2.1 / 2.2 / 2.2a seam overtook: 12 arrived, 5 are lawfully openDox's, 1 is
  RULED elsewhere, and 5 no longer exist as imports at all. No further carve
  can move them, so the box is not waiting on § 3.4 (landed), and the wording
  needs a RULING or an amendment rather than another measurement. Registered
  here, decided nowhere: this amendment records the accounting and leaves the
  box open on it. `#656` record: CLAIM `5656686020`.
  **STATUS — 2026-09-16, RULED R-1 DECIDES WHAT THE STATUS ABOVE REGISTERED, AND
  THE BOX TICKS** (`#656` comment `5690428146`, Brett Heap, by interactive
  multi-choice): *"the residue is settled by the measured accounting … amend the
  box to that accounting and tick it. No further carve."* The note above is left
  unedited as the record of what was registered; its closing "the box stays open"
  is superseded by this line and by the amendment to the box's own second
  sentence. **The accounting was re-derived at TODAY's heads before the tick, not
  carried forward from that note** — each tree named with the head it was read
  at, because two of the three have moved since:
  — `openXdox-code` `main` **`c1ad341a`**: **13** live `doc_health` import sites
  across **8** modules under `src/openxdox/` — the **twelve** inventoried
  (`completeness` 1, `corpus_root` 1, `gate_console` 4, `gate_routes` 1,
  `generator` 3, `round_trip` 1, `snapshot_registry` 1) plus `cli_gate.py`:251,
  the § 4.3 site outside `design.md`'s inventoried twelve modules.
  — `openDox-code` `main` **`1e469713`**: **5** sites in **2** modules —
  `serve.py`:**713** and `workbench.py`:746, :1407, :1408, :1409. **One drift
  found by re-measuring rather than transcribing:** that `serve.py` site is
  :**710** at `8efb3cf5` (the head the note above cites) and :**713** at
  `1e469713`, moved three lines by slice S7's landing. Same site, same import,
  different line — each number is right at the head beside it, which is why both
  are written down.
  — `openxFactory` `main` **`cb2d3a2c`**: **3** sites, none of them residue —
  `scripts/ideation_dashboard/doxbench_status_exemption.py`:63 (the ONE RULED by
  DQ-1 to stay) and `serve_openxfactory_lanes.py`:178 and :277 (openxFactory's
  own lane adapter, never inventoried among the 23). Ten files survive under
  `scripts/ideation_dashboard/` there, nine `.py` and `web/views/intent-feed.js`.
  12 + 5 + 1 + 5 = **23**, `design.md` § D3's inventory exactly. **No further
  carve can move any of them**, which is the ruling's own finding: the five
  DISCHARGED stopped being imports at the § 2 seam before the carve ran, and the
  five at openDox-code are lawfully openDox's under the split this packet
  performed. `#656` records: CLAIM `5690461589`; RULED R-1 `5690428146`.
- [x] 4.2 `[oXd]` `contracts/opendox-pin.yaml` — openXdox pins openDox by commit
  and tree digest (`sorted-ls-tree-r-v1` over openDox's whole tree — the scaffold
  writes NO per-file `sha256`; the per-file `sha256`, `pinned_by_commit_only:`
  and the migration range/reversibility/runbook the MODIFIED `neutral-product-pin`
  requires are a HAND ACT this task also performs, not part of §1.2's seed)
  *(reality check 2026-09-05, second run, claim C26)*. The dependency points
  ONE way and there is no cycle. **In the openXdox ASSEMBLY ROOT, naming the openDox ASSEMBLY ROOT's
  commit** (amended 2026-09-05); § 1.2's `--pin` writes the file and the
  `neutral_product_pins: [openDox]` manifest entry together, so this task
  BUMPS it rather than creating it. **The cost the shape adds, accepted:** a
  change to openDox's code leg is not visible to openXdox until openDox's
  assembly root advances its own `code` pin and openXdox then bumps this file —
  two pin moves where a single-repository openDox would still need one — the
  consumer bump is owed regardless of the pinned product's shape (`openxFactory`
  performs the identical hand bump today for the single-repository
  `openRepoShape` and `openXwallet` pins); what the shape election ADDS is the
  first move, the assembly root's own leg lockstep. *(reality check 2026-09-05,
  second run, claims C27/C41.)*
  **STATUS — 2026-09-11, tick JUDGED MET, verified live against `openXdox`
  root main (`eca0b5977b0cca1f39c725b95fc9fa8b4d307d72`, #656 comment
  `5640651561`).** `contracts/opendox-pin.yaml` at that commit names
  `product: openDox`, `source_repository: opensoft/openDox`,
  `commit: "8ec3036ce496a90a3c92a89c4907e57941901b51"` (the openDox ASSEMBLY
  ROOT's own commit, #656 comment `5640527633` — not a leg commit),
  `revision_kind: commit`, and `digests.tree_sha256` under
  `digest_definition: sorted-ls-tree-r-v1`. The per-file `sha256` /
  `pinned_by_commit_only:` HAND ACT is the recorded judgment that both lists
  are empty because `opensoft/openDox`'s own `contracts/manifest.yaml`
  carries `contract_bundle_version: none` and `entries: []` — verified live
  at openDox root main `8ec3036c` — the identical judgment already accepted
  for openxFactory's own openXdox pin (5.1). The migration `range` /
  `reversible` / `runbook` triple is present, each `not_yet_deployed`, on
  **RULED ASK-1** (Brett Heap, `#656` comment `5628886636`: "the three fields
  are added now with an explicit `not_yet_deployed` sentinel, proving the
  schema shape before it is needed"). Every field the MODIFIED
  `neutral-product-pin` requirement and this task's own text name is present
  or is a documented, ruled HAND-ACT judgment — none silently omitted.
- [x] 4.3 `[oXd]` The routes and subcommands openXdox CONTRIBUTES to openDox's
  extension points, **from `openXdox-code`**. No fork of the server.
  **STATUS — 2026-09-12, tick JUDGED MET — both halves are landed.** CODE
  half: `opensoft/openDox-code` **#11 →
  `a99eba03e31a0aee1cc15a061fdf718cc88a2c44`**, 2026-09-11 19:04Z (#656
  comment `5639351854`) — the lazy proxy `profile_openxfactory` (RULED ASK-2
  → 2, `5628886636`) covering subcommands, with `cli.build_parser()` /
  `serve.build_server()` resolving the profile through it and refusing
  without a host; per **RULED ASK-6 → 1** (`5635150678`, ASK BLOCK
  `5635063050`), `serve.py` reads the same proxy for ROUTES too — one
  mechanism, one registration, under ASK-2, no second composition point.
  openxFactory HALF + PIN LOCKSTEP: **`opensoft/openxFactory` #984 →
  `a1ef886fdd65a4a530fe584c22b863b2106a0ac0`**, 2026-09-12 14:55Z (CLAIMED
  `5640395709`; landed #656 comment `5646646722`; plain gate; head
  `02a9f634`; six required checks SUCCESS; 10 threads / 0 unresolved) — the
  real engineering `profile_openxfactory` as ONE composite profile
  (`SUBCOMMAND_EXTENSIONS`, `ROUTE_EXTENSIONS`, and the CLI gate facet the
  proxy reads) registered ONCE at process start at every composition point
  that builds a parser or a server (the PR-2 stand-in
  `bind_composition_point()` collapsed into that call), riding the pin
  lockstep that moves openDox → `8ec3036c` and openXdox → `eca0b597` (both
  assembly roots carrying this landing).
- [x] 4.4 `[oXd]` **PARAMETERIZE, do not ship one domain's words (RULING C2).**
  The lifecycle engine reads its status vocabulary, transitions, authorities and
  immutability point from a domain profile. A hardcoded status word is a defect
  under `domain-mapping-declaration`.
  **STATUS — 2026-09-12, tick JUDGED MET — both halves are landed.** CODE
  half: `opensoft/openXdox-code` **#14 →
  `3840c1670771e2dc7bcd64eaafbc43169e0f383d`**, 2026-09-11 20:41Z (#656
  comment `5640381252`) — on RULING C2 and **RULED ASK-4 → "proceed"**
  (`5634195861`, over ASK-4 `5633855878`'s five Q1-Q5 sub-questions): the
  engine reads its status vocabulary, per-kind terminal statuses (Q4, per
  kind), immutability point (Q3, enforced in v1) and declared-only
  transitions/authorities from a registered `DomainProfile` (Q1, YAML
  canonical / dataclass runtime), `register()` the one process-start call
  with two accessors (Q5), `current()` refusing loudly when nothing is
  registered — sequenced after BUILD slice 2b on shared files
  (`5634218589`). openxFactory HALF + PIN LOCKSTEP: **`opensoft/openxFactory`
  #984 → `a1ef886fdd65a4a530fe584c22b863b2106a0ac0`**, 2026-09-12 14:55Z (same
  PR as 4.3's half; CLAIMED `5640395709`; landed #656 comment `5646646722`;
  plain gate; head `02a9f634`; six required checks SUCCESS; 10 threads / 0
  unresolved) — the real engineering `DomainProfile` YAML under `contracts/`
  (validating against openXdox-spec's schema, loaded with
  `openxdox.domain_profile.load()`) and the SAME process-start registration
  as 4.3's proxy, riding the pin lockstep that moves openDox → `8ec3036c`
  and openXdox → `eca0b597`.
- [x] 4.5 `[oXd]` **BUILD what does not exist**, named as three separate features
  rather than folded into a carve: the model/scenario workbench for
  `governed-derived-model` families (openXdox's centre of gravity and absent from
  all 80,000 lines), the evidence-and-provenance surface (invariant 2's evidence
  traces and assumption registers), and the role-and-authority projection.
  **STATUS — 2026-09-11, tick JUDGED DUE at the RECOUNT (#656 comment
  `5638391057`).** All three features landed at `openXdox-code`, in RULING
  ASK-3's order (`5628886636`): slice 1, the role-and-authority projection,
  **#10 → `4f98e77c7985f786af2ec295c38b6b06a7f5fce6`** (2026-09-11 03:51Z);
  slice 2, the evidence-and-provenance surface, **#11 →
  `427230c340cdb1f5d114d3868073cd156fa33ada`** (2026-09-11 10:39Z); slice 3,
  the model/scenario workbench, **#12 →
  `5333b125dc0f2dd9ee6f6e558c758fbfe6c49b4d`** (2026-09-11 11:24Z). The
  requirement row for all three landed as the change
  `add-openxdox-projection-surfaces` at `openXdox-spec`: proposed **#9 →
  `8557fc1912834491a8e97743376cf877601dbcae`**, ratified and archived **#10 →
  `0dd7621a983867806eb5fd93f164d4e5da189943`**, corrected **#11 →
  `d6b71aa31b21a39a90b7b6095b03fd8e083d41ba`** (the `projection` row + the
  out-of-band status allowance), and erratum'd **#12 →
  `6b92bdc40863b017926718ee314e9ca87e49ff09`** (ASK-5, the workbench
  scenario's four existing route-extension columns).
- [ ] 4.6 `[oXd]` Cut `xdox-v1.0` after its own suite is green. **In the ASSEMBLY
  ROOT** (amended 2026-09-05), on 3.8's reasoning.

## 5. openxFactory consumes and sheds; the MAJOR is cut. BREAKING

- [x] 5.1 `[oxF]` `contracts/openxdox-pin.yaml`, plus its one gitlink — the pin
  file and gitlink moving in the SAME commit. **Names the ASSEMBLY ROOT**
  (amended 2026-09-05; corrected 2026-09-05 per RULING F — `opensoft/openxFactory`
  issue #656, Brett Heap, "rule F openXdox only, then do the corrections PR":
  this task previously also listed `contracts/opendox-pin.yaml` and a second
  gitlink, which the rest of this same task already contradicted). `openxFactory`
  never pins or mounts a leg, which is the assembly root's own job.
  Per the MODIFIED `neutral-product-pin`, `openxFactory` declares only its DIRECT
  upstreams; openDox's commit is READ from openXdox's own pin and recorded, if at
  all, as a DERIVED value. **TICKED — #917 → `edf0e24f45b6e7baf5322023cbc1c43d28ff46cd`**,
  the § 5-remainder lane's own live re-verification (2026-09-10, on this packet's
  tick standard, PR #897 → `021c3d3607a626730ae8d2027ca68c58ed14a3b6`): at that
  commit the `openXdox` gitlink reads `db58fffa58d49d92f58db40bd7e63cad3205052f`,
  `.gitmodules` names the assembly root (`git@github.com:opensoft/openXdox.git`,
  not a leg), `contracts/openxdox-pin.yaml` carries that same commit, and both
  moved together in commit `7f76f978194150a73f6cbc56a2ee900d32ccf03e`,
  PR #917's first commit (**corrected 2026-09-10**, `#656` comment
  `5625808031`: this aside previously read "nothing else in that diff"; that
  is overstated — `7f76f978` also carried `.gitmodules`,
  `scripts/doc_health/pin_class.py`, and added
  `scripts/verify-openxdox-pin.py`. 5.1's own text holds regardless: the pin
  file and the gitlink moved in the SAME commit, which is what this task
  requires). **Both `contracts/opendox-pin.yaml` and a second gitlink NOW EXIST
  in this tree, and their existence does not disturb this box's own tick.**
  *(AMENDED 2026-09-16 by RULED **R-5**, `#656` comment `5690428146`. This read
  "No `contracts/opendox-pin.yaml` and no second gitlink exist anywhere in the
  tree", which was true when RULING F was written and stopped being true at
  **`#932` → `f4fb4ffc010a8fc2b5e101a8426316486fd5fd37`** (2026-09-11T01:42:09Z),
  where RULED **Q7** mounted `opensoft/openDox` as a SECOND submodule and pinned
  it in lockstep. At `main` `cb2d3a2c` the tree carries gitlinks `openDox` →
  `3819625e` and `openXdox` → `a6500141`, `.gitmodules` names both ASSEMBLY
  ROOTS, and `contracts/opendox-pin.yaml` sits beside `contracts/openxdox-pin.yaml`.
  What this box ticked on is unchanged — `contracts/openxdox-pin.yaml` and its
  gitlink moved in the SAME commit — and RULING F's own holding is unchanged:
  `openxFactory` declares its DIRECT upstreams, which Q7 made two. § 8.7 takes
  the same amendment.)*
  `python3 scripts/verify-openxdox-pin.py` passes live at that commit:
  `OK openxdox-pin verified: openXdox@db58fffa58d49d92f58db40bd7e63cad3205052f, gitlink read from HEAD, sorted-ls-tree-r-v1 tree digest recomputed (43c60b29693820d3e8c066e9c6a088f306bf0a7c0f2d818d72ceb62657c53209)`.
- [ ] 5.2a `[oxF]` **The FIFTEEN engineering-vocabulary requirements are
  re-promoted HERE (RULING DQ-1), not shed.** They leave the capability
  `ideation-dashboard` and land in `openxFactory`'s own corpus under the § 2.2a
  adapter's own successor capability, whose id this task authors.
  `promotion_fidelity.py` keys on (capability, normalized title), so the successor
  is a distinct key and the REMOVED delta stays visible to the checker. The only
  edit they take is re-expressing path literals as `adapter calls` — one of
  RULING OQ-1's three classes, by name.
- [x] 5.2 `[oxF]` **Shed the dashboard corpus down to RULED DQ-1's KEPT SET.**
  The list is `docs/opendox-carve-manifest.yaml` and not a prose inventory: every
  row it routes to a destination LEAVES, and the **117** rows carrying a
  `stays_openxfactory_*` reason (**103** `stays_openxfactory_adapter` + **14**
  `stays_openxfactory_governance`) STAY, because `openxFactory` keeps its own
  adapter and its own governance. Across the manifest's surface, measured at the
  carve commit `b075fd91` and at `#940`'s merge `cc4ae9d3` — files at the carve →
  files kept: `scripts/ideation_dashboard/` 63 → **9**, its `web/` 43 → **1**
  (`views/intent-feed.js`, RULED `not_moved / stays_openxfactory_adapter` under
  OQ-F), `tests/ideation-dashboard/` 157 → **42**,
  `tests/ideation_dashboard/` (the four-file underscore spelling) 4 → **0**,
  `scripts/ideation-dashboard-nightly.py` 1 → **1** (it STAYS,
  `stays_openxfactory_adapter`), `scripts/validate-ideation-dashboard-contracts.py`
  1 → **0**, the dashboard contract schemas under `contracts/schemas/` **6 → 0**,
  `examples/ideation-dashboard/` 140 → **44**, and the dashboard governance docs
  7 → **6** (one leaves: `docs/ideation-dashboard-session-runbook.md`,
  `moved_with_declared_edit` to `opendox_spec`).
  *(RE-SCOPED 2026-09-16 by RULED **R-2**, `#656` comment `5690428146`, which
  supersedes this box's own deferral of the reconciliation to "a sweep at § 8".
  It read "Delete `scripts/ideation_dashboard/` (48 modules), `web/` (40 files),
  `tests/ideation-dashboard/` (125 files) and `tests/ideation_dashboard/` (the
  four-file underscore spelling), `scripts/ideation-dashboard-nightly.py`,
  `scripts/validate-ideation-dashboard-contracts.py`, the four dashboard contract
  schemas, the 142 packaged examples under `examples/ideation-dashboard/`, and the
  five dashboard governance docs" — a pre-DQ-1 deletion list wrong in SCOPE (it
  deletes 117 rows DQ-1 keeps) and in five of its own six counts. Every figure
  above is measured at a named tree; the STATUS below records each one, and
  records where the measurement and the ruling's own parenthetical part company.)*
  **STATUS — 2026-09-10, `#656` comment `5625573095` (Brett Heap, verbatim
  "rule (a) post-shed mode, merge 924 when green").** RULING (a) resolves this
  box's own prerequisite — `design.md` § D6 (1)'s amendment. Realization is two
  pull requests. **PR-1** — the post-shed mode CAPABILITY alone (the `phase:`
  key, the `carve-shed-incomplete` refusal, their tests, the manifest's own
  documented `phase:` field, the runbook § 8 text) — **openxFactory #928,
  landing** at the time of this writing, not yet merged. **PR-2 — this box, the
  shed itself** (the phase flip to `post-shed`, the 319 deletions, and whatever
  the re-point needs) is **NOT STARTABLE** until three sub-questions are
  answered (addendum, `#656` comment `5625144570`):
  **(2)** does the six `contracts/schemas/*` moved rows' fallout — named by 127
  tracked files — join this atomic § 5 pull request, or land separately;
  **(6)** the RETAINED `tests/ideation-dashboard/conftest.py:106` still imports
  the shed's `session_fixtures` (RULING Q-L7 fixed the destination side and left
  this one) — edit the retained file, or change that manifest row's disposition;
  **(7)** the adapter re-point (104 import sites / 32 files; 17 of those modules
  are reachable only with BOTH legs' `src/` present) — defer to the BUILD arc
  (§ 3.5 / § 3.6) or give `openxFactory` its own reach to openDox (a second
  submodule, or a pinned wheel). None of the three is answered as of this
  writing, and this box does not tick until PR-2 lands.
  **Correction, 2026-09-10** (`#656` comment `5625808031`): the § 4 / shed
  reality-check record
  (`review/reality-check-2026-09-10-section-4-and-the-shed.md`, `Status:
  record`, immutable — corrected here rather than in that file) reports Probe 1
  as `Interrupted: 4 errors during collection`; that undercounts a FULL
  `tests/ideation-dashboard` collection, which measures **27** collection
  errors. The finding is stronger, not weaker, and this box stays open either
  way.
  **STATUS — 2026-09-12, box stays open; verified against
  `origin/main` directly, the realization is PARTIAL and 5.6a's wording
  defect is not the only reason.** `opensoft/openxFactory` **#940 →
  `cc4ae9d35b2dbd56743c8c19699fd685d4e49343`** (`#656` comment `5638315691`)
  cut `docs/opendox-carve-manifest.yaml`'s phase to `post-shed`, but most of
  this box's own listed clauses are NOT gone from the tree today:
  `scripts/ideation_dashboard/` (10 of 48 modules remain),
  `tests/ideation-dashboard/` (42 of 125 files remain),
  `examples/ideation-dashboard/` (44 of 142 remain), and
  `scripts/ideation-dashboard-nightly.py` (unchanged) all carry `not_moved`
  rows in the carve manifest (`stays_openxfactory_adapter` /
  `stays_openxfactory_governance`) under **RULING DQ-1** (openxFactory keeps
  its own adapter) — a plan this box's own text predates. The manifest's
  own `scripts/ideation-dashboard-nightly.py` row says so directly: "tasks.md
  § 5.2's deletion list predates DQ-1 and is recorded as a disagreement
  in the pull request." Confirmed actually gone: `web/`,
  `tests/ideation_dashboard/` (the underscore spelling),
  `scripts/validate-ideation-dashboard-contracts.py`, and the five contract
  schemas 5.6a's defect (a) names (`gate-action-record`,
  `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`,
  `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog`). Most
  of the governance docs this box counts as five are ALSO still present
  (`docs/d10-hosted-refresh-marker.md`, both `docs/doxbench-runtime-refresh-
  dogfood*.md` records, `docs/openxdox-naming.md`,
  `docs/project-repo-schema.md`) — only `docs/ideation-dashboard-session-
  runbook.md` left, `moved_with_declared_edit` to `opendox_spec`. **The box
  stays open on two defects, not one**: 5.6a's "four vs five schemas"
  wording defect, AND this fuller pre-DQ-1 staleness across the rest of its
  own listed clauses — neither fixed here. Reconciling the wording (or
  re-scoping the box to what RULING DQ-1 actually kept) is for a sweep at
  § 8, the archive gate, not a silent edit of this box's original text.
  **STATUS — 2026-09-16, RULED R-2 TAKES THE RE-SCOPING OUT OF THE § 8 SWEEP AND
  DOES IT HERE, AND THE BOX TICKS ON `#940` → `cc4ae9d3`** (`#656` comment
  `5690428146`, Brett Heap, by interactive multi-choice): *"re-scope to RULING
  DQ-1's kept set (the manifest's `stays_openxfactory_*` rows; FIVE schemas, not
  four) and tick on #940 → cc4ae9d3."* The two notes above are left unedited; the
  edit is not silent because this line and the box's own parenthetical say what
  was replaced and why. **The ruling's discharging act, read from the merged pull
  request rather than from the ruling:** `opensoft/openxFactory` **#940 →
  `cc4ae9d35b2dbd56743c8c19699fd685d4e49343`**, merged **2026-09-11T17:33:38Z**.
  **Every figure in the re-scoped box is measured at a named tree, at the carve
  commit `b075fd91` (tag `opendox-carve-0`) and at `cc4ae9d3`, and re-read at
  `main` `cb2d3a2c` where it is identical:**

  | manifest surface | rows | at `b075fd91` | kept at `cc4ae9d3` | at `main` `cb2d3a2c` | what the old list said |
  | --- | ---: | ---: | ---: | ---: | --- |
  | `scripts/ideation_dashboard/` excluding `web/` | 63 | 63 (all `.py`) | **9** | 9 | "48 modules" |
  | `scripts/ideation_dashboard/web/` | 43 | 43 (41 hand-authored) | **1** | 1 | "40 files" |
  | `tests/ideation-dashboard/` | 157 | 157 (140 `.py`) | **42** | 42 | "125 files" |
  | `tests/ideation_dashboard/` (underscore) | 4 | 4 | **0** | 0 | "the four-file underscore spelling" — exact |
  | `scripts/ideation-dashboard-nightly.py` | 1 | 1 | **1** | 1 | "delete" — DQ-1 keeps it |
  | `scripts/validate-ideation-dashboard-contracts.py` | 1 | 1 | **0** | 0 | "delete" — it left |
  | `contracts/schemas/` | 12 | 6 dashboard schemas present | **0 of the 6** | 0 | "the four dashboard contract schemas" |
  | `examples/ideation-dashboard/` | 140 | 140 (139 `.yaml`) | **44** | 44 | "the 142 packaged examples" |
  | `docs/` governance | 7 | 7 | **6** | 6 | "the five dashboard governance docs" |

  **DQ-1's kept set is 117 rows**: of the manifest's 456 rows (`phase: post-shed`)
  the dispositions are `moved_verbatim` **160**, `moved_with_declared_edit`
  **158**, `not_moved` **138** — and the `not_moved` reasons are
  `stays_openxfactory_adapter` **103**, `replicated_at_destination` **20**,
  `stays_openxfactory_governance` **14**, `deleted_at_carve` **1**. 103 + 14 =
  **117**, which is the set the ruling names and the box now keeps. The other
  twenty-one `not_moved` rows are not a kept set: a `replicated_at_destination`
  row arrives somewhere and a `deleted_at_carve` row arrives nowhere.

  **THE SCHEMA COUNT IS SIX, AND THIS IS WHERE THE MEASUREMENT AND THE RULING'S
  OWN PARENTHETICAL PART COMPANY — RECORDED, NOT QUIETLY RESOLVED.** The ruling
  says *"FIVE schemas, not four"*, which is § 5.6a defect (a)'s list carried
  forward: `gate-action-record`, `ideation-dashboard-snapshot-index`,
  `ideation-dashboard-snapshot`, `xfactory-workbench-chat-turn`,
  `xfactory-workbench-model-catalog`. The manifest moves **SIX**. The sixth is
  **`ideation-workbench.schema.yaml` → `opendox_spec`**, and § 5.6a's own
  parenthetical for it — *"`ideation-workbench.schema.yaml` moves as well while
  carrying no independent manifest row"* — is false at every head checked: the
  row is present at **`45bd9ee2^`** (the commit BEFORE #970, the pull request
  whose review raised the defect), at **`45bd9ee2`** itself, at **`cc4ae9d3`**
  and at **`cb2d3a2c`**. Two of the five are also no longer `moved_verbatim`:
  `ideation-dashboard-snapshot` and `ideation-dashboard-snapshot-index` are
  `moved_with_declared_edit` at `cc4ae9d3` and after, having been
  `moved_verbatim` at #970. So the six that leave, each with its destination
  read from its own row, are `gate-action-record` → `openxdox_spec`,
  `ideation-dashboard-snapshot-index` → `openxdox_spec`,
  `ideation-dashboard-snapshot` → `openxdox_spec`, `ideation-workbench` →
  `opendox_spec`, `xfactory-workbench-chat-turn` → `opendox_spec` and
  `xfactory-workbench-model-catalog` → `opendox_spec`; all six are present at
  `b075fd91` and absent at `cc4ae9d3` and at `main`. The six that stay are
  `gate-intent`, `ideation-cross-reference` and `ideation-possibles-register`
  (adapter) and `project-register`,
  `xfactory-ideation-organizer-recommendations` and
  `xfactory-ideation-routing-index` (governance). **The box therefore reads SIX**,
  because a ticked box whose count does not reproduce is the defect this packet's
  tick standard exists to refuse — and § 5.6a's defect (a), which is a different
  box's wording and already `[x]`, is NOT edited here: it is left to the act that
  claims it, with the sixth schema and the false parenthetical named for it. **The
  deprecation window is where this matters and it is unaffected**:
  `contract-v3.7`'s `relocating:` markers and the `contract-v4.0` BREAKING entry
  cover the schemas that left, and whether the prose around them says five or six
  changes no digest. `#656` records: CLAIM `5690461589`; RULED R-2 `5690428146`;
  the discharging act #940 → `cc4ae9d3`.
- [ ] 5.3 `[oxF]` **AUTHOR `.github/workflows/openxdox-consumer-gate.yml` in
  `openxFactory`** — a NEW consumer gate over the pinned tools, on the
  `openxwallet-consumer-gate` shape (a `<product>-consumer-gate.yml` whose job id
  is the stable required-check token, as that file's own `wallet-validation` is).
  There is **nothing to CONVERT**: `openxFactory` has never carried a
  dashboard-named workflow, and the workers that run the dashboard live in the
  `xFactory` aggregation, not here. **"Retaining the job id" is discharged by
  leaving `pytest-suite` UNTOUCHED** — workflow name, job id and required check
  are all the one token `pytest-suite`, and a token survives a rename that never
  happens.
  *(PREMISE REWRITTEN 2026-09-16 by RULED **R-4**, `#656` comment `5690428146`.
  It read "Convert the dashboard workflows to CONSUMER GATES over the pinned
  tools, on the `openxwallet-consumer-gate` shape, **retaining the job id** so a
  ruleset-pinned token survives a file rename" — which presumes workflows this
  repository does not have and never had: at `main` `cb2d3a2c` its thirteen
  workflows are `clearing-dispatch-gate`, `doc-health-reusable`,
  `former-id-arrival-gate`, `lane-line`, `merge-master-approval`,
  `openreposhape-pin-gate`, `openspec-cli-pin-gate`, `openxwallet-consumer-gate`,
  `pytest-suite`, `release-tag-gate`, `review-lane-repin`, `session-open-pr` and
  `signed-execution-chain-gate`, and `git log --all --diff-filter=A` over
  `.github/workflows/*dashboard*` and `*ideation*` returns nothing — no such file
  was ever added. The SHAPE, the pinned-tools reading and the job-id obligation
  are unchanged; only the act is. **This box does NOT tick with this amendment**:
  the workflow is its own declared act under its own claim.)*
- [ ] 5.4 `[oxF]` **FLOOR PART 2 (RULED OQ-1, RESTATED BY RULING OQ-K) — the
  source→destination TEST MAPPING, with declared multiplicity.** Not a scalar
  equality. Four clauses, the full text at `design.md` § D6 (2):
  **(a) TOTAL COVERAGE** — every file in the manifest's declared surface carrying
  at least one `def test_` has at least ONE post-split home named by its own row;
  a file with tests and no home is a LOST TEST and the carve REFUSES.
  **(b) DECLARED MULTIPLICITY** — each `not_moved / replicated_at_destination`
  row **THAT CARRIES TESTS** (at least one `def test_` at `carve_commit`)
  DECLARES the repository set its replica lands in, the retained `openxFactory`
  copy included, and `m` is that set's size. **The clause binds TEST-BEARING
  replicated rows only, because those are the only rows that enter (c)'s Σ:** the
  landed manifest carries 18 `replicated_at_destination` rows and 3 of them carry
  tests; a zero-test replica contributes `(m − 1) × 0 = 0` whatever its set, so it
  can neither move the sum nor make it uncomputable, and its replica set is FLOOR
  PART 1's business rather than part 2's. **For this carve the declared set is,
  for all three test-carrying replicated rows, `openxFactory`
  (retained) · `opensoft/openDox-code` · `opensoft/openXdox-code` — so `m = 3`**,
  and it is written out here rather than left to be read off § 3.7. This is one
  obligation ON FLOOR PART 1 and it is the input this part reads: the row grammar
  of `docs/opendox-carve-manifest.yaml` gains the field in FLOOR PART 1's OWN
  successor pull request (the manifest is not this packet's file), and until it
  lands the enumeration below IS the declaration. An undeclared replica set ON A
  TEST-BEARING ROW makes the check uncomputable, which is a REFUSAL and not a
  pass.
  **(c) THE SUM CHECK, OVER DECLARED MULTIPLICITIES** —
  `Σ(destinations) = source_count + Σ over replicated rows of (m − 1) × row_test_count`
  — the Σ ranges over the REPLICATED ROWS ONLY, and a row that is
  not replicated contributes nothing to it —
  every term read from the manifest at the carve commit. Measured against the
  LANDED 454-row manifest (#865 → `17167481`) at `carve_commit b075fd91`:
  source **4,411** over 146 `.py` rows (openDox-code 1,098 · openXdox-code 2,315 ·
  `openxFactory` 968 staying); THREE replicated test modules —
  `tests/corpus-adapter/test_conformance.py` (20), `test_interface_closure.py`
  (6), `test_no_home_vocabulary.py` (4), **30** in all — at `m = 3` each, because
  § 3.7 requires EVERY destination to pass the conformance corpus; destinations
  **1,128 + 2,345 + 998 = 4,471**; and `4,471 = 4,411 + (3 − 1) × 30`. ✔
  **(d) PINNED BY TEST** at each destination and in `openxFactory` (which under
  RULING DQ-1 includes the adapter's own tests), the way `pytest-suite.yml`
  already pins this repository's collection triple — SKIPPED exactly, SELECTED
  and PASSED as FLOORS, failures and errors zero. Per destination, never as one
  cross-repository equality: an equality pin on a sum goes RED on merge refs that add
  tests for reasons the candidate cannot fix, which is the deadlock class
  `pytest-suite.yml` already refuses by name.

  **THE CASES THIS CHECK OWES, EACH OF THEM A REFUSAL.** The floor carries no
  `#### Scenario:` blocks because it has no spec delta to host them (§ D6, *"WHY
  NO PROMOTED REQUIREMENT IS AUTHORED FOR THE FLOOR"*), so the obligation lands
  here as named cases on the build task. The first two are the ratified rule's
  own, kept in intent; the last two are RULING OQ-K's, and exist because a
  mapping can fail in ways an equality could not express.
  - **A TEST WITH NO HOME.** WHEN a file under the declared surface carries
    `def test_` AND its row names no home — no `destination`, and no `not_moved`
    reason that constitutes one (`stays_openxfactory_adapter` and
    `stays_openxfactory_governance` are a home AT `openxFactory`;
    `replicated_at_destination` is a home at `openxFactory` PLUS every home it
    declares) — THEN the carve REFUSES `test-home-missing`. A `deleted_at_carve`
    row carrying `def test_` is the same refusal under its own name: deleting
    tests is a decision to be RULED, never inferred from a disposition. Measured
    at `carve_commit`: **no row under the surface carries `def test_` and no
    home** — each of the 146 test-carrying rows names a destination, a
    `stays_openxfactory_*` reason or a replica set — and **no `deleted_at_carve`
    row carries a single `def test_`**, so neither limb of this case fires today.
    *(This is the intent the ratified text was reaching for — no
    test is lost — stated directly instead of inferred from an arithmetic
    identity.)*
  - **A SILENT DROP AT A DESTINATION.** WHEN a destination's collected
    `def test_` falls BELOW the total its own rows declare, THEN the carve
    REFUSES `destination-test-shortfall`. *(The most likely way a large suite
    loses coverage in a carve, and the part whose absence Brett named when he
    rejected snapshot-equivalence alone.)*
  - **A REPLICATED FILE — the case the equality could not express (NEW, RULING
    OQ-K).** WHEN a row is `not_moved / replicated_at_destination` declaring
    MULTIPLICITY 3 and carrying 20 `def test_`
    (`tests/corpus-adapter/test_conformance.py`) — the declared homes being
    `openxFactory` (retained), `opensoft/openDox-code` and
    `opensoft/openXdox-code` — THEN those 20 are counted ONCE
    in `source_count` and THREE times across the homes, the excess is exactly
    `(3 − 1) × 20 = 40`, and the check **PASSES** — **AND** deleting a replica to
    make a raw equality hold is ITSELF a refusal, because § 3.7 requires every
    destination to carry that corpus. The ratified equality had no way to state
    this and would have failed on it, on its first run, forever.
  - **AN UNDECLARED REPLICA SET (NEW, RULING OQ-K).** WHEN a
    `replicated_at_destination` row **THAT CARRIES `def test_`** names no homes,
    THEN its multiplicity is unknown, the Σ over replicated rows of
    `(m − 1) × row_test_count` is
    UNCOMPUTABLE, and the carve REFUSES
    `replica-multiplicity-undeclared` — an uncomputable check is never a pass.
    A ZERO-TEST replicated row is OUTSIDE this case: its term is
    `(m − 1) × 0 = 0` whatever its set, so it can make nothing uncomputable and
    it does not refuse here — its replica set is owed to FLOOR PART 1, not to
    this floor. Measured at `carve_commit`: **this case does not fire today** —
    of the manifest's 18 `replicated_at_destination` rows the 15 zero-test ones
    are outside the clause's domain, and each of the 3 test-bearing ones has its
    homes declared above.
    This is what clause (b)'s obligation on FLOOR PART 1 is owed FOR.

  > Amended 2026-09-09. This item first read: *"**FLOOR PART 2 (RULED OQ-1) —
  > test counts that must SUM across the three repositories.** 3,927 `def test_`
  > leave — 52% of this repository's 7,612. openDox + openXdox + the
  > `openxFactory` remainder (which now includes the adapter's own tests, per
  > RULING DQ-1) SHALL equal the pre-split count, pinned by test the way
  > `pytest-suite.yml` already pins the collection triple."* **RULING OQ-K**
  > (Brett Heap, 2026-09-09T22:19:57Z, by click-through in session
  > `openXfactory-4`; `opensoft/openxFactory`#656 comment `5609526215`),
  > verbatim: *"OQ-K → FLOOR PART 2 restated as a source→destination mapping
  > with declared multiplicity for replicated files (a small amendment PR to the
  > change)."* **THE INTENT IS UNCHANGED — no test is lost, and a silent drop
  > still refuses** — and only the TEST moves. The equality is false by design:
  > the landed manifest's replicated rows put the same 30 test functions at three
  > homes each, so the post-split sum exceeds the pre-split count by exactly 60
  > on its first run, and the only mechanical repair would be to DELETE replicas
  > that FLOOR PART 3 requires. It is also stale: 3,927 / 7,612 were measured at
  > `a858e5b0` on 2026-09-04, before the five pre-carve splits and before the
  > manifest existed. Record:
  > `review/amendment-2026-09-09-floor-part-2-mapping.md`.
- [ ] 5.5 `[oxF]` **FLOOR PART 4 (RULED OQ-1) — the snapshot-equivalence run:**
  the new stack renders the SAME dashboard snapshot as the old, proven by matching
  snapshot digests over one corpus.
- [ ] 5.6 `[cxF]` `[oxF]` **DE-FLOOR BEFORE YOU REMOVE — Rule 7 substrate row 1,
  claimed HERE.** `openspec/specs/ideation-dashboard/` is REMOVED and two
  capability directories are ADDED by the archive, and the codexFactory
  review-authority floor is EXACT SET EQUALITY. Order: the codexFactory pull
  request FIRST (the machine block regenerated by
  `generate_specs_floor_block.py` at ONE `openxFactory` ref, with
  `SPECS_FLOOR_PATHS` moved in the SAME commit), then `openxFactory`'s five pin
  sites in ONE reviewed diff, then the removal. Never hand-edit the block or the
  snapshot.
- [x] 5.6a `[oxF]` **THE DEPRECATING MINOR § 5.7 OWES — `contract-v3.7`, cut
  BEFORE the shed.** `docs/contract-versioning-policy.md` § Change Classes
  requires, before any Breaking removal, "at least one full minor release where
  the old shape produced deprecation warnings", and NO such minor existed for
  the five manifest-digested schemas `docs/opendox-carve-manifest.yaml` marks
  `moved_verbatim` to the spec legs (`gate-action-record`,
  `ideation-dashboard-snapshot-index`, `ideation-dashboard-snapshot`,
  `xfactory-workbench-chat-turn`, `xfactory-workbench-model-catalog`) or the
  conformance validator that leaves with them. RULED **ASK-10 → 1** (Brett Heap,
  `#656` comment `5635524078`): cut it FIRST, from pre-shed `main`, before PR-2
  `#940` lands. Landed as `opensoft/openxFactory` **#970** — a `relocating:`
  marker on the five manifest rows naming destination repository and leg commit,
  a § Deprecations Currently In Force entry, a DEPRECATING `contracts/CHANGELOG.md`
  entry carrying the removal version and the migration path, and
  `contracts/releases/contract-v3.7.digests.yaml`. **THIS BOX IS SATISFIED BY
  THAT PULL REQUEST LANDING.** The `contract-v3.7` annotated tag is Brett Heap's
  own act (ASK-9a, `5635150678`) and is 5.7's PRECONDITION, not this box's: a
  bundle whose warning window a major relies on must be PUBLISHED before that
  major cuts, so 5.7 does not open until the tag exists and
  `validate-contract-release.py verify-tag` passes on it.

  **TWO DEFECTS IN 5.2 AND 5.7 THIS BOX EXPOSED AND DOES NOT ITSELF FIX**, both
  raised by the review of #970 and both owed an answer before the MAJOR cuts:

  (a) **5.2 SAYS FOUR AND THE CARVE MANIFEST MOVES FIVE.** 5.2 reads "the four
  dashboard contract schemas" and names none of them; the carve manifest marks
  FIVE manifest-digested schemas `moved_verbatim` — `gate-action-record` is the
  fifth, and `ideation-workbench.schema.yaml` moves as well while carrying no
  independent manifest row. 5.2's wording must be reconciled to the carve
  manifest before the shed, or the shed and the deprecation window cover
  different sets.

  (b) **THE CONFORMANCE VALIDATOR IS SHARED WITH THREE ROWS THAT STAY.**
  `scripts/validate-ideation-dashboard-contracts.py`, which 5.2 deletes and
  which discharges § Change Classes' conformance-validator clause for the five
  BY LEAVING WITH THEM, is named by the `consumption_rule` of EIGHT manifest
  rows. `ideation-possibles-register` and `gate-intent` are `not_moved`
  (`stays_openxfactory_adapter`) and `demotion-execution-receipt` appears in no
  carve row at all. At contract-v3.7 all eight keep their validator; at the
  MAJOR those three would name a delegated owner this repository no longer
  contains. 5.7 may not treat the clause as discharged until it says what
  validates them. Recorded in `contracts/CHANGELOG.md` § contract-v3.7 and in
  `docs/contract-versioning-policy.md`'s Deprecations Currently In Force entry
  so it survives to the cut that must answer it.
  **STATUS — 2026-09-12, both defects tracked to where they resolve.**
  Defect (b) is ANSWERED: `contracts/CHANGELOG.md`'s `## contract-v4.0 —
  2026-09-11 (BREAKING; the five ideation-dashboard contract schemas are
  REMOVED and consumed at the openDox / openXdox spec legs)` entry, point 3,
  "An update to the conformance validator — discharged by the MOVE
  ITSELF" — "There is no second validator that accepts a new shape and
  rejects the old one, because there is no new shape: the BYTES are
  identical and the PUBLISHER changed. The question `contract-v3.7` left
  open is answered below." Defect (a) is 5.2's own wording defect, not this
  box's: tracked at 5.2's own STATUS line (this amendment), left open there
  rather than fixed here. This note's original text above is unedited.
- [x] 5.7 `[oxF]` Cut the **MAJOR** — a removed shape is BREAKING under
  `docs/contract-versioning-policy.md` § Change Classes, which also requires a
  CHANGELOG migration note and a preceding full minor of deprecation warnings.
  The NUMBER is allocated AT THE CUT by merge order, never reserved here. Owes its
  own `contracts/releases/<tag>.digests.yaml` under `release-surface-integrity`,
  and a published annotated tag verified from an independently refreshed checkout.
  **STATUS — 2026-09-12, tick JUDGED MET — the MAJOR is cut, published and
  verified.** Cut: **`opensoft/openxFactory` #983 →
  `ce5c054e8522499c6f4ff2039496243a09cb4acf`**, 2026-09-11 23:52Z (#656
  comment `5641952070`; plain gate, RULED ASK-9a → 1 `5635150678`; head
  `219bb357`, six required checks SUCCESS, `pytest-suite` run `34657479391`
  — 7086 passed / 6 skipped —, 8 threads / 0 unresolved, no
  `openspec/changes/` path). `contracts/manifest.yaml` on `main` now reads
  `contract_bundle_version: contract-v4.0`, the five relocating rows removed,
  and the three unrelated entries whose removal target was `contract-v4.0`
  RESTATED to `contract-v5.0` exactly as
  `docs/contract-versioning-policy.md`'s own text prescribes — ACCEPTED by
  Brett Heap in the tagging sitting (`5642131117`), no correcting PR owed.
  **The box's own "owes its own `contracts/releases/<tag>.digests.yaml` under
  `release-surface-integrity`"** is discharged:
  `contracts/releases/contract-v4.0.digests.yaml` exists on `main`, and
  post-land, from an independent clone at `ce5c054e`, both
  `validate-contract-release.py verify-commit` and `verify-promotion` read
  `pass` (#656 comment `5641952070`) — discharging PR-2's own OWED
  release-inventory bundle cut (`5638315691`). **The box's own "a published
  annotated tag verified from an independently refreshed checkout"** is
  discharged: `contract-v4.0` is the annotated tag object
  `9e6c0ae4596b6585016ec9efa2c9e3fdafef9e4b` →
  `ce5c054e8522499c6f4ff2039496243a09cb4acf`, pushed under Brett Heap's git
  identity from the independent clone (amending RULING 9c for this one tag,
  as with `contract-v3.7`), and
  `validate-contract-release.py verify-tag --remote origin --tag
  contract-v4.0` → `release verify-tag: pass` (#656 comment `5642131117`,
  RULED + EXECUTED 2026-09-12 00:21Z). Both of the box's own owed clauses are
  discharged; nothing remains owed.
- [x] 5.8 `[xF]` `.gitmodules`, two root gitlinks, `README.md`, `CLAUDE.md`,
  `project-register.yaml` — **including § 1.9's two derived election rows**
  (amended 2026-09-05). The aggregation's root gitlink for openXdox SHALL EQUAL
  `openxFactory`'s (one) nested gitlink commit, both naming the ASSEMBLY ROOT
  (RULING F, `#656`, 2026-09-05 — `openxFactory` nests openXdox only). The
  aggregation's root gitlink for openDox HAS an `openxFactory`-side counterpart
  and SHALL EQUAL it too — **corrected 2026-09-11**. The sentence this replaces
  read "has NO `openxFactory`-side counterpart to check against: `openxFactory`
  does not pin or mount openDox directly, so that gitlink is checked only
  against `opensoft/openDox`'s own assembly root", which was true when it was
  written and stopped being true at RULED Q7 (`#656` comment `5626248666`,
  2026-09-10): `openxFactory` now mounts the openDox assembly root DIRECTLY, as
  a second gitlink beside `contracts/opendox-pin.yaml` (PRs `#932` / `#952`), and
  declares two direct upstreams. So that gitlink is checked against BOTH
  `openxFactory`'s own direct openDox gitlink AND `opensoft/openDox`'s assembly
  root — the same equality 5.8 already states for openXdox, and RULING F's
  "openXdox only" clause is superseded for openDox alone by Q7.
  **STATUS — 2026-09-12, tick JUDGED MET — the aggregation row and
  re-point ceremony are landed.** `opensoft/xFactory` **#442 →
  `41d6d7aeb15dbb73c75ac4e9ba2cb2e8cfc6c1a3`**, admin-merged by the lane on
  Brett Heap's word by interactive multi-choice (RULED **ASK-9b → 1**,
  `#656` comment `5635150678`: "the lane authors the PR after 5.7's tag
  exists, citing the green `validate` run; Brett admin-lands it on his
  word"; head `25fd719b`; `validate` run `34701762754` SUCCESS; 11 threads /
  0 unresolved). Root gitlinks: `openDox` →
  `8ec3036ce496a90a3c92a89c4907e57941901b51`, `openXdox` →
  `eca0b5977b0cca1f39c725b95fc9fa8b4d307d72`; the `openxFactory` pointer
  moved to `75484b6742eb929c5216e110722394d7a3cfa08a` in the same commit,
  carrying `.github/clearing/openxfactory/PIN.yaml`'s `openxfactory_commit`
  with it. Both equalities this box states are discharged at that landing:
  `openXdox`'s root gitlink equals `openxFactory`'s own nested `openXdox`
  gitlink (RULING F, unchanged); `openDox`'s root gitlink equals
  `openxFactory`'s own nested `openDox` gitlink (RULING F superseded for
  openDox alone by **RULING Q7**, `#656` comment `5626248666`, 2026-09-10,
  "RULED (i): SECOND SUBMODULE") — both checked live against
  `opensoft/openDox` / `opensoft/openXdox`'s own assembly roots AND against
  `contracts/opendox-pin.yaml` / `contracts/openxdox-pin.yaml`'s `commit:`
  fields at the new `openxFactory` pointer, which agree exactly.
  `tests/test_opendox_openxdox_gitlink_parity.py` PASS is the landing check.
  `#656` record: `5646934254`.
- [x] 5.9 `[oxF]` ANNOTATE the 30 archived changes carrying an
  `ideation-dashboard` delta with the carry-forward. **Immutable records are
  annotated, never edited into agreement** — the wallet arc's own treatment, and
  the highest-volume bookkeeping in the realization.
  **STATUS — 2026-09-12, tick JUDGED MET — the 30 carry-forward annotations
  are landed.** RULED (Brett Heap, #656 comments `5640246046`,
  `5640938010`): one dated bookkeeping section per archived packet (the two
  carrying a `Status: ratified` header take the `Edited (bookkeeping):` line
  inside that block; the twenty-eight without a header carry it as the
  section's first line), naming split-opendox § 5.2's shed (`#940 →
  cc4ae9d3`), the legs and pins, the deprecation (`contract-v3.7`) and the
  removal (`contract-v4.0`, `#983 → ce5c054e`, tag `9e6c0ae4`), plus a
  companion disposition per packet. Landed: **`opensoft/openxFactory` #982
  → `db1f0cfa04b2e8d4d1d17d11eb25da2a0147f21b`**, 2026-09-12 00:27Z (Rule 6
  window posted and closed; head `21730067`, six required checks SUCCESS,
  `pytest-suite` run `34659735150`, 64 threads / 0 unresolved; 30 of 30
  archived changes annotated, 182 insertions / 0 deletions, nothing any
  packet asserts changed). Companion: **`opensoft/xFactory` #445 →
  `c81b957bfbc91e84e7e67bda00c8023d2d249950`**, the thirty dispositions,
  landed by the lane's admin merge on Brett Heap's ruling ("land it anyway
  as the governance record", `5640938010`) as the governance record: **doc-health
  does not scan `tasks.md`** (`govern-openspec-corpus-membership`, OQ-2), so
  these entries fire no `record-immutability` finding today and stand
  inert until a doc-health change reads them — the correction is stated in
  #445's own body and in `5640938010`. #656 record: `5642167113`.

## 6. Re-home the five frozen changes (RULING Q6)

Each closure moves that change's row in `tests/sequenced_after/corpus-ledger.yaml`
and removes its README "OpenSpec Records" entry; both are Rule 7 substrate
movements claimed at the time they land.

- [ ] 6.1 `[oxF]` `[oXd]` **`add-nightly-dashboard-refresh`** → openXdox. Its 13
  open tasks and its 1 ADDED + 1 MODIFIED `ideation-dashboard` requirements
  re-home; the aggregation-side artifact-only worker stays in the aggregation.
  **Its SEVEN `doc-health` ADDED requirements do NOT travel and are NOT added to
  `openxFactory`** — they were authored on the dashboard's behalf and Q4 points
  that dependency one way, so they are re-authored against the ADAPTER in
  openXdox. This is the one genuine conflict RULING Q6 names and this is its
  resolution.
- [ ] 6.2 `[oxF]` `[oD]` **`retire-doxbench-chat-turn-v1` — THE ONE THAT CANNOT
  SIMPLY CLOSE.** Its schema removal is already realized in `openxFactory` bytes
  and `contract-v3.0` is published, so its remaining 7 tasks are `openxFactory`
  bookkeeping that completes HERE and it archives HERE on its own evidence.
  Only its FORWARD half — the surviving `-v2` family's requirements — re-homes to
  openDox. **Sequenced BEFORE § 8.**
- [ ] 6.3 `[oxF]` `[oD]` **`add-doxchat-model-intake`** → openDox. Built but
  unarchived; its code moves with the carve as `moved_with_declared_edit` rows,
  its four ADDED requirements are re-authored in openDox, and its one additive
  schema enum member is already `openxFactory` contract bytes and STAYS.
- [ ] 6.4 `[oxF]` `[oD]` **`add-composed-view-authoring`** → openDox. One MODIFIED
  requirement, `target_release: none`, no contract bytes — the cheapest of the
  five.
- [ ] 6.5 `[oxF]` `[oD]` **`add-lens-document-selection`** → SPLIT. The
  set-builder half to openDox; its `doc_health.staging_seed` drafter and route
  STAY in `openxFactory`'s own adapter (RULING DQ-1 — no longer a `codexDox`
  question). **The only one of the five whose content does not land in one
  place.**
- [ ] 6.6 `[oxF]` **No new dashboard change opens in `openxFactory`** (RULING Q6),
  from this packet's ratification forward.

## 7. The first descendant — a task with a RULING CHECKBOX, not a decision

> Amended 2026-09-05 — repository shape. The descendant is scaffolded the same
> way and is THREE repositories, not one: `codexDox` + `codexDox-spec` +
> `codexDox-code`, one `scaffold-project.py` run with `--pin openXdox@<sha>`.
> **Which domain gets the first one, and when, is STILL the open ruling** — the
> shape ruling settles how a descendant is created, not whether this one is.
> It stays THIN under DQ-1: it pins openXdox and reuses `openxFactory`'s
> adapter, so its `-code` leg carries deploy configuration and branding rather
> than an adapter of its own.

- [x] 7.1 `[oxF]` **§ 7 FOLLOWS § 5, RULED (DQ-1).** The shed no longer waits on a
  descendant: `openxFactory` keeps its own adapter, so the carve completes on its
  own account and the first `<Domainx>Dox` follows when a domain has a profile.
  **THE RULING THIS BOX OWED IS ANSWERED: NONE YET.** On the brainstorm's
  evidence the first one is likely **`codexDox`** — engineering is the only
  corpus with a live consumer — but codexFactory holds **no artifact of the
  product's PROFILE KIND** today, so `domain-descendant-boundary`'s laziness rule
  says no descendant exists yet, and under DQ-1 `codexDox` is a THIN descendant
  that pins openXdox and reuses `openxFactory`'s adapter rather than owning one.
  **Ticked as *ruled: not yet*** — the box asked which domain gets the first
  descendant and when, and the answer is that no domain does yet and the laziness
  rule is what decides when one does. *(AMENDED AND TICKED 2026-09-16 by RULED
  **R-3**, `#656` comment `5690428146`. Two clauses changed: "**RULING STILL
  OWED: which domain gets the first one, and when.**" is now that ruling's
  answer; and "codexFactory holds **zero** tracked dashboard files today" is
  replaced by the test the requirement actually states, because the old clause
  does not reproduce — see the STATUS below, which measures 32 tracked
  dashboard-named paths in codexFactory and shows why not one of them is a
  profile artifact. The conclusion the ruling adopts is unaffected; the sentence
  that a tick makes load-bearing is the one that had to be measured.)*
  **STATUS — 2026-09-16, RULED R-3** (`#656` comment `5690428146`, Brett Heap, by
  interactive multi-choice): *"the first descendant is NONE YET … 7.1/7.2 tick as
  ruled: not yet, § 7.3 becomes a deferred successor as § 4.5 was."*
  **The test the requirement states, and what codexFactory actually holds.** The
  promoted requirement *A descendant is created on its first profile, not before*
  (`openspec/specs/domain-descendant-boundary/spec.md`:128-137) keys on **an
  artifact of the product's PROFILE KIND**, not on the word "dashboard". For a
  `<Domainx>Dox` the profile kind is what § 7.3 names — ONE domain-mapping
  declaration, five axes, per `domain-mapping-declaration` — and, under this
  packet's own MODIFIED delta (`proposal.md`:298-299, `design.md`:741, NOT yet
  promoted, since this packet archives later), a committed TENANT INSTALL.
  Measured at codexFactory `main` **`761f49d0`**, 1,995 tracked blobs: paths
  matching `(?i)domain.mapping` **0**, `(?i)codexdox` **0**, `(?i)openxdox`
  **0**, `(?i)opendox` **0**. **Zero artifacts of the profile kind, so the
  laziness rule holds and the answer is NONE YET.**
  **The clause this box carried does NOT reproduce, which is why it was
  amended rather than ticked around.** codexFactory holds **32** tracked paths
  whose name contains "dashboard", in four classes, and naming them is what makes
  the tick safe: (1) `specs/002-ideation-dashboard/` — four Speckit files
  (evidence, plan, spec, tasks); (2)
  `tests/browser-ui-repair/baselines/ideation-dashboard/brand/codexfactory-linux-chromium-v1/`
  — seventeen files, a visual-regression baseline corpus (baseline PNG,
  candidates, dispositions, history, index); (3)
  `scripts/browser_ui_repair/dashboard_adapter.py`; (4) ten documents — two
  `ideation/brainstorm/dashboard-*.md` and eight
  `openspec/changes/add-repo-enrollment/supporting-docs/repo-enrollment-dashboard-deployment-*.md`.
  **Not one is a profile artifact.** Class (2) is the closest thing and is worth
  saying why it is not: a baseline of a RENDERED dashboard is evidence that
  codexFactory CONSUMES the product — which is exactly § 7.1's own reason for
  expecting `codexDox` to be first — and consumption is what the laziness rule
  defers on, not what it triggers on. A further 26 paths match `(?i)dox`, every
  one of them under `specs/010-doxbench-editor-chat/`.
  **And no descendant exists to be empty.** The `opensoft` organization carries
  exactly six `*Dox*` repositories — `openDox`, `openDox-spec`, `openDox-code`,
  `openXdox`, `openXdox-spec`, `openXdox-code`, the product's own — and **zero
  `<Domainx>Dox`**. § 7.2's REPORT is the record of that, posted on `#656` before
  these boxes moved. `#656` records: CLAIM `5690461589`; RULED R-3 `5690428146`.
- [x] 7.2 `[oxF]` Until that ruling, descendant NAMES are registered (§ 1.7) and no
  repository is created. An empty descendant is REPORTED under the promoted
  requirement, not cited as precedent for creating more.
  **TICKED 2026-09-16 on RULED R-3 (`#656` comment `5690428146`) AND ON THE
  REPORT ITSELF, which is posted before the box moves rather than asserted in
  it** — `#656` comment **`[FILL AT LANDING — the § 7.2 empty-boundary REPORT
  comment id]`**, written against the PROMOTED requirement *A descendant is
  created on its first profile, not before*
  (`openspec/specs/domain-descendant-boundary/spec.md`:128-145) and in
  particular its scenario **An empty descendant exists** (:143-145). What the
  report finds, measured rather than asserted: the `opensoft` organization
  carries exactly SIX `*Dox*` repositories, the product's own
  (`openDox`, `openDox-spec`, `openDox-code`, `openXdox`, `openXdox-spec`,
  `openXdox-code`) and **ZERO `<Domainx>Dox` descendants**, so the :143-145
  scenario has no instance to report — which is itself the reportable fact, and
  the strongest form of "not cited as precedent for creating more" this box can
  reach. The fifteen descendant names plus one install name of § 1.7 stay
  registered with no repository behind any of them.
- [ ] 7.3 `[?]` **DEFERRED SUCCESSOR (RULED R-3, 2026-09-16, `#656` comment
  `5690428146`) — carried out of this packet in the form § 4.5 was carried under
  openxFactory #714 and § 0.6's RULED PATH A**: the ruling § 7.1 owed has landed
  and its answer is NONE YET, so the act this box describes has no subject to
  perform on, and it does not tick here, block § 8's archive gate, or lapse. It
  is the successor act that runs when a domain acquires its first profile
  artifact, and § 7.1's laziness rule is what starts it. The text below is its
  specification, unchanged and unticked, and § 8's gate reads it as deferred
  rather than open. **When the ruling lands**: the descendant carries ONE
  domain-mapping declaration (five axes, per `domain-mapping-declaration`),
  deploy configuration,
  branding, its double pin of openXdox (gitlink + pin file, SAME commit), and its
  DECLARED per-tenant operating cost — migration run per release, backup and
  restore policy, credential set — per the MODIFIED `domain-descendant-boundary`.
  **ONE scaffold run creates it** (amended 2026-09-05), on § 1.1's shape:

  ```
  python3 scaffold-project.py \
      --org opensoft --project codexDox --id codexdox --name 'codexDox' \
      --visibility <follows codexFactory's own visibility, RULING Q7> \
      --elected-by 'Brett Heap' --elected-on <the ruling's date> \
      --reference 'openxFactory docs/project-repo-schema.md' \
      --pin openXdox@<40 hex — the openXdox ASSEMBLY ROOT's commit> \
      --referent-chain openXdox,openDox
  ```

  *(reality check 2026-09-05, second run, claims C22/C30: without
  `--referent-chain`, the scaffold exits 0 and writes `descendant_referent: openDox` / `referent_declared: true` with NO `referent_chain` key — the
  same case-folding-coincidence pass § 1.10 documents, left standing with no
  chain recorded. The flag is required for this command to satisfy § 1.10.
  The run also prints `WARNING declared-unverified` when openXdox's tree is
  not reachable from the scaffold host — not a finding; `--link-source openXdox=<path>` or `SHAPE_PIN_SOURCE_OPENXDOX` clears it.)*

  Three repositories, THIN: the `-code` leg carries deploy configuration and
  branding, the `-spec` leg the one domain-mapping declaration, the assembly
  root the pins and the gate. It owns NO adapter (DQ-1). The `--pin` on
  openXdox — never on openDox — is RULING OQ-2 in the tree, and § 1.10 governs
  how it classifies before and after `opensoft/openRepoShape`#40 lands.
- [ ] 7.4 `[OmI]` `[Opsx]` The per-tenant install: one instance and one database
  per tenant in both cases (RULING Q3), the two GitHub Apps created through the
  **App Manifest flow** in the TENANT'S org with the dispatch/content separation
  as a SECURITY INVARIANT, and the `dox` workload set
  (`workflows/aks-administration.yaml:412-431`) becoming per-tenant. The ungoverned
  `openxdox` DNS record is governed here.

## 8. The archive gate

Under `release-realization` this change archives ONLY on merged plus green
realization evidence, never on landing. Each line is its own evidence.

- [ ] 8.1 **All SIX repositories exist** (amended 2026-09-05 — this first said
  "Both repositories"), PUBLIC, Apache-2.0, each with a required check that has
  reported at least once and a ruleset promoted from EVALUATE to ACTIVE; each
  assembly root's `project.yaml` records the election (`elected_by: Brett Heap`,
  `elected_on: 2026-09-05`, `reference: openxFactory docs/project-repo-schema.md`) and its
  `validate` gate is green over its own legs.
- [ ] 8.2 **The RULED four-part floor (OQ-1), one evidence line per part:** the
  carve manifest with every file in exactly one disposition and every edit in one
  of the three closed classes; the source→destination TEST MAPPING closing on
  § 5.4's ledger — every test function with at least one home, the replicated
  set enumerated with its multiplicity, and
  `Σ(destinations) = source_count + Σ over replicated rows of (m − 1) × row_test_count`
  (amended 2026-09-09 — RULING OQ-K; this first said *"the collection counts
  SUMMING across the three repositories"*, which the replicas make false as an
  equality); the neutral conformance corpus green in EVERY destination
  including `openxFactory`'s own adapter; and the snapshot-equivalence run's
  matching digests. **None of these is "the tests passed"**, and no part
  substitutes for another — the two single-instrument alternatives were rejected
  on the record.
- [ ] 8.3 `openxFactory`'s shed merged, the MAJOR cut and TAGGED, and the tag
  verified from an INDEPENDENTLY REFRESHED checkout.
- [ ] 8.4 The codexFactory floor de-floored BEFORE the removal, in that order, with
  the five openxFactory pin sites moved in ONE reviewed diff. Note the floor must
  account for BOTH directions of this archive: `openspec/specs/ideation-dashboard/`
  removed, and the two new capability directories plus the § 5.2a adapter successor
  capability ADDED.
- [ ] 8.5 All five re-homed changes dispositioned, each with its destination named
  in the receiving repository; `retire-doxbench-chat-turn-v1` archived in
  `openxFactory` on its own evidence first.
- [ ] 8.6 `ideation-intent-plane` in canon, or its non-promotion recorded (§ 0.6).
- [ ] 8.7 The aggregation's **openXdox AND openDox** gitlinks landed, **each
  equal to `openxFactory`'s own nested gitlink of the same name**, all four
  naming an ASSEMBLY ROOT, and the two derived `project-register.yaml` election
  rows landed with them (§ 1.9, amended 2026-09-05).
  *(AMENDED 2026-09-16 by RULED **R-5**, `#656` comment `5690428146`. It read
  "The aggregation's openXdox gitlink landed and equal to `openxFactory`'s (one)
  nested gitlink, both naming the assembly root (RULING F — `openxFactory` nests
  openXdox only; the aggregation's openDox gitlink has no `openxFactory`-side
  counterpart to check)". That parenthetical stopped being true at **`#932` →
  `f4fb4ffc`**, where RULED **Q7** mounted `opensoft/openDox` as `openxFactory`'s
  SECOND submodule: the counterpart exists, so it is checked. RULING F is not
  reversed — it settled that `openxFactory` declares only its DIRECT upstreams,
  and Q7 made those two. Live at the time of this amendment, which is why the
  check is worth having: the aggregation `opensoft/xFactory` `main` `784a7c6e`
  reads `openXdox` **`eca0b597`** against `openxFactory` `main` `cb2d3a2c`'s
  **`a6500141`**, and `openDox` **`8ec3036c`** against **`3819625e`** — both
  stale, both moved by the aggregation re-point Brett admin-lands, which is the
  act this line gates and not an act of this amendment. A THIRD gitlink moves in
  that same re-point — the aggregation's own `openxFactory`, `75484b67` against
  `main` `cb2d3a2c` — and this line does NOT check it, because it is not one of
  the two the descendant pin chain is about; named here so the re-point does not
  read this line as its whole checklist.)*
- [ ] 8.8 Amendment 3 applied with the SIX repository names and the election,
  and the descendant names — each with its two leg names — registered with no
  repository created (amended 2026-09-05).
- [ ] 8.9 `python3 -m pytest tests/doc-health tests/sequenced_after -q` green,
  `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health
  run whose severity counts move by the amount **the archive pull request RECORDS
  AND EXPLAINS**.
  *(THIRD CLAUSE REWRITTEN 2026-09-16 by RULED **R-6**, `#656` comment
  `5690428146`. It read "a doc-health run whose severity counts move by exactly
  the amount the packet predicts" — and the packet predicts no amount: the word
  "severity" occurs exactly twice in the whole packet, at `design.md`:225, a
  glossary row, and in this line itself, so the clause as written could never be
  satisfied or falsified. The obligation is not weakened, it is relocated to the
  act that can discharge it: the archive pull request states the movement it
  caused and why, and a movement it does not explain fails this line.)*
