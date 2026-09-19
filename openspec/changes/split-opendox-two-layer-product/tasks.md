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
  discussion (`design.md`:981 at this amendment's ORIGINAL base `cbc3a2c6`, and — in
  THIS file — § 1.10's pin-chain paragraph, the one that reads *"the referent
  test compares CASE-FOLDED, and `openXdox`.casefold() equals
  `openxDox`.casefold() — so a pin on the INTEGRATION layer satisfies the
  referent test for the NEUTRAL CORE"*, cited by its SENTENCE and NOT by a
  line number: "`openXdox`.casefold() equals
  `openxDox`.casefold()"), not a sixth descendant. Excluding those two
  artifacts, `grep -owhE 'MedxDox|codexDox|LedgerxDox|AdxDox|OpsxDox' proposal.md design.md tasks.md | sort -u | wc -l` — the pattern is POSIX ERE
  with no Perl-style escapes, so no `\b` is needed; the `-o`/`-h`/`-w` options
  are GNU/BSD grep extensions (available on Linux and macOS), not
  POSIX-required. Returns **5**: the five names above are the only
  declared descendant base names in the packet. Read "fifteen descendant names —
  five descendants × three names each, the assembly name plus its two leg
  names — plus one install name, zero repositories" in place of the
  eighteen-count above; the rest of the sentence is unaffected.)*
  *(THE TWO COORDINATES WERE STALE AND ARE CORRECTED, amendment #5,
  registered on amendment #4's pull request at comment `5702495415`. They
  read `tasks.md`:347 and `design.md`:868; measured, `:347` of this file is a
  `gh api` tree read of the openDox root and the casefold discussion is at
  `:595` at the base `cbc3a2c6` — **and it has taken a DIFFERENT value at four
  of this branch's own heads since, every move made by this amendment's own
  insertions above the line. The values are deliberately NOT enumerated here,
  because the list would age exactly as the number did**: an earlier draft of
  this very sentence named three values and was already wrong about the last
  of them when a review read it, which is the third time the defect this
  paragraph documents has been committed by the paragraph documenting it — and
  in
  `design.md` it is at `:981`, which does not move because this branch does
  not touch that file. So the first attempt at a numeric repair went stale
  under the very act that wrote it, twice, which is § 1.8's thesis proved on
  this amendment's own body and the reason the in-file half of the citation
  is now a SENTENCE and carries no number at all (`design.md` keeps its
  number because the file is stable and the tree is named).
  Neither original number was right at any
  tree checked. The repair is taken here — rather than left to the act that
  claims this paragraph — because a stale COORDINATE is a currency fix that
  changes no normative reading, which is the line this estate keeps between a
  non-normative correction and a change to ratified wording; § 7.3's *"When
  the ruling lands"*, which IS ratified wording, is recorded below and left
  alone.)*

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
  **STATUS — authored 2026-09-14; tick JUDGED MET AT THIS AMENDMENT'S OWN
  LANDING, 2026-09-16: the boundary was INVENTED as a design note and REALIZED
  in an eight-slice arc.** *(The date is the AUTHORING SNAPSHOT and is labelled
  as one rather than moved forward, on the precedent `openDox-spec`'s own § 7
  header sets at its fix round 13: an amendment whose tick is judged AT ITS
  LANDING cannot be dated to the day it was written, and re-dating it would
  erase which of these statements were authored before the slices they record
  had merged. The acts recorded below ran on 2026-09-12/13 (S1–S6), 2026-09-15
  (S7 and the pin lockstep) and **2026-09-15/16** for S8 — its annotation `#1025`
  at 23:50:29Z on the 15th, leg A at 01:11:37Z and leg B at 01:23:16Z on the
  16th — with openDox-spec `#11` at **13:24:51Z** on the 16th. **This
  parenthetical gives DATES for the arc and a clock only where the ORDERING
  turns on one**: S8's three acts, which straddle midnight, and `#11`, which
  shares the 16th with S8's legs A and B, so only a clock orders the three.
  *(That last clause read "`#11`, which merged the same day this amendment
  lands" until this amendment DID NOT LAND on the day it was written —
  claimed 2026-09-16T21:39:02Z, still open past midnight UTC. Its replacement
  is keyed to two acts already named in this same parenthetical rather than
  to a date its writer does not control, which is this section's own thesis
  arriving from the inside.)* Every other clock sits beside the
  act it belongs to rather than here — S7's two in its own landing record below
  (21:40:25Z and 21:41:36Z, 71 seconds apart), S2's pair in the Q-L1 paragraph
  (15:45:51Z and 15:59:44Z) and the pin lockstep's at 2026-09-15T23:27:40Z —
  and **S1, S3, S4, S5 and S6 carry a date only**, their merge times readable
  from the pull requests the table names. *(This sentence claimed a clock for
  EACH act it dates, twice over: as "each with its own clock beside it" until
  fix round 10, and as "each of the acts this parenthetical dates carrying its
  own clock beside it" after it — while eight of the acts it dates carry no
  clock in it. A Copilot finding on #1035, accurate, taken at fix round 12,
  which also replaced that participial clause with finite sentences on the same
  review's wording note. The round-10 correction was right about `#11` and wrong
  to keep the word "each": narrowing a claim is not the same as measuring it.)*
  Fix round 10 added `#11`'s clock, which alone read as a bare date beside S8's
  three, and corrected this marker's own arithmetic in the same round: round
  6 took **THREE** Copilot findings, all three in the suppressed block of review
  `5223334808` at head `4355f0bd` — this date (`:887`, the same point the thread
  of 13:07:18Z had already raised, which is why the marker first read "two
  findings, one raised as a thread and one suppressed"), the stale *"six of the
  eight"* at `:1024`, taken at item (v) below, and the pull request's own
  DESCRIPTION, taken there and not in this file. Both corrections are Copilot
  findings on #1035, accurate, taken at fix round 10. The `#8`–`#11` amendment
  list below carries shas and not clocks for all four alike, so `#11`'s time is
  recorded here, where the claim that needs it is made.)*
  **ALL EIGHT are merged and every sha in the table below is final**, each one
  read from the merged pull request itself rather than from a report of it. The
  tick is therefore written for the state this pull request lands INTO, which is
  what this paragraph said it would be, and no box is ticked ahead of its act.
  *(The paragraph read "Six of the eight … S7 and S8 land AHEAD" until S7
  merged, then "SEVEN of the eight … S8 lands AHEAD of this amendment … it is
  the one row still carrying `[FILL AT LANDING]` below" until S8 merged. Both
  rows were filled IN PLACE at their own landings. **S7**, 2026-09-15: `#1030` →
  `b3a75537217d9b15684501684e9527f412d4e6b6` at **21:40:25Z** and openDox-code
  `#21` → `1e4697130855e9695a6acc3344b7c925bb3eeb09` at **21:41:36Z** — RULED
  Q-L1's annotation-first rule holding for the SIXTH time, by 71 seconds. **S8**, in
  three acts across 2026-09-15/16: the annotation openxFactory `#1025` →
  `e5896455ac74e126b7baa2ba81cf1cc9ae4d37f1` at **2026-09-15T23:50:29Z**, then leg A openXdox-code `#19` →
  `0a0265f7e53a1db30a0f51deb556231c2001285f` at **2026-09-16T01:11:37Z**, then leg B openDox-code `#23` → `0b4e8bbf68fabfcd65d4f0d80e619c20a013e888`
  at **2026-09-16T01:23:16Z** — the same rule holding for the **SEVENTH and LAST** time. The
  count is one holding per ANNOTATED slice, in landing order — S2, S3, S6, S4,
  S5, S7, S8 — S1 being the one slice correctly exempt because it creates files
  and edits no ARRIVED row; counted per annotation→LEG pairing instead — S6, S5
  and S8 carry two legs each, so the ten pairings run **S2 1 · S3 2 · S6 3–4 ·
  S4 5 · S5 6–7 · S7 8 · S8 9–10** — S7's is the EIGHTH and S8's the NINTH and
  TENTH of ten, and all ten are ordered right. These two ordinals read "a seventh" and
  "an EIGHTH" until openDox-spec `#11`'s fix round 18, where a Copilot finding
  caught that S7 and S8 could not both be the seventh: both had been minted by
  counting SLICES LANDED, S1 included.)* That is the
  discipline `openDox-spec`'s own amendment #3 applies to its § 5.0 landing
  record, which this table mirrors.

  **The boundary** is `openDox-spec` `docs/front-end-package-boundary.md` — the census,
  the three destination classes (A openDox core / B the gate loop / C the
  stage-named region), the registration mechanism, the four assertions and the
  slice plan — landed at openDox-spec **#8 → `a44ac06d`** and amended three
  times: **#9 → `61866d29`** (amendment #1, the five rulings Q1–Q5),
  **#10 → `7d12428c`** (amendment #2, five corrections and Q6), and
  **#11 → `54e910735b97b326d05250100104b3af07d3f5ae`** (amendment #3, the S8 premise RULED,
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
  | S8 | re-point the bundle paths, un-narrow `validate` for the web suites | `#1025` → `e5896455` | `#23` → `0b4e8bbf` | `#19` → `0a0265f7` |

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
  one commit — the lockstep invariant **§ 4.2** of this file describes and
  `#1054` performs. **§ 5.1 is NOT a second description of it, and citing it as
  one is corrected here.** That box, ticked under RULING F (`#656`, Brett Heap,
  *"rule F openXdox only, then do the corrections PR"*), records that
  `openxFactory` declares only its DIRECT upstreams and closes: *"No
  `contracts/opendox-pin.yaml` and no second gitlink exist anywhere in the
  tree."* **Measured at `main` `b1df95ee`, that closing sentence has been
  OVERTAKEN by the tree**: `contracts/opendox-pin.yaml` exists and carries its
  own `commit:`, its header saying in terms that *"openxFactory now has TWO ways
  to learn openDox's commit"*, and `git ls-tree -r` returns FOUR gitlinks —
  `installs/omnigent-install`, **`openDox`**, **`openXdox`**, `openXwallet`.
  **REGISTERED here, not corrected**: § 5.1 is a ticked box carrying a RULING,
  so the act that amends it is its own act with its own claim — the same rule
  this amendment applies to `design.md`, to `proposal.md` and to the packet's
  README entry. *(A Copilot finding on #1035, accurate about the
  cross-reference, taken at fix round 14. The invariant itself — the pin file
  and its gitlink moving in the SAME commit — is unchanged, and `#1054` shows it
  twice over.)* It is the bump the boundary note's § 1.2(d) SKIP waits on, arriving
  at the aggregation level; like the two acts above it is its own claim and not
  a condition of this box.

  **THE PACKET FIGURE, AMENDED HERE — this box's own "40 files, 30,410 lines"
  is a design-time reading no tree in the arc reproduces**, and the boundary
  note defers its correction to the packet in terms (*"a packet figure is
  amended in the packet"*, its § 1.1). Re-measured over every blob under each
  tree's bundle root, each row named with the tree it was read at — **the first
  four on 2026-09-14, the fifth at this amendment's landing on 2026-09-16**,
  which is why the table's introduction no longer carries one date for all of
  them (a Copilot finding on #1035, accurate):

  | tree | blobs | lines | hand-authored |
  | --- | ---: | ---: | --- |
  | openxFactory `scripts/ideation_dashboard/web/` at the carve commit `b075fd91` (tag `opendox-carve-0`) | 43 | 31,068 | 41 files / 31,066 lines |
  | openDox-code `a99eba03` — the note's census tree | 42 | 30,585 | 40 / 30,583 |
  | openDox-code `main` `8efb3cf5` — S1–S6 landed | 41 | 30,477 | 39 / 30,475 |
  | openDox-code `#21` head `c7a216c7` — the ARC-COMPLETE bundle | 42 | 31,955 | 40 / 31,953 |
  | openDox-code `main` **`0b4e8bbf`** — **ALL EIGHT landed**, read at this amendment's own landing | 42 | 31,955 | 40 / 31,953 |

  **The FILE count is right; the LINE count is 173 short.** The carve step is
  one file and is exactly accounted for: `views/intent-feed.js` (483 lines)
  did not travel, RULED `not_moved / stays_openxfactory_adapter` under OQ-F,
  and taking that one file out of 41 files / 31,066 lines leaves **40 /
  30,583** — the
  packet's "40 files" on the nose, its "30,410 lines" **173** short of what
  arrived and **656** short of what the carve commit held. Everything after
  that is the arc itself (five files in before S5, six out with S5, one in
  with S7), which is why the arc-complete bundle is 40 hand-authored files
  again at 31,953 lines. *(The last row was added at this amendment's landing
  and is the check that the arc ENDED where `#21`'s head said it would: S8 leg
  B merged after the first four rows were taken (2026-09-14) and before this
  fifth one was, and it moves not one byte under
  `src/opendox/web/`, so `main` `0b4e8bbf` reproduces the arc-complete figure
  exactly — 42 blobs / 31,955 lines, 40 hand-authored / 31,953 — which is what
  the boundary note's § 1.1 predicted and then read.)* **FOUR other occurrences in the packet's LIVE
  documents carry this figure and NONE is edited here** — `design.md`:52 and
  :351 and `proposal.md`'s `code_surface:` line each pair *"40 files"* with
  *"30,410"*, and `proposal.md`:208 carries the line count alone (*"30,410
  lines of front end"*) — because a ratified document is amended by an act that
  CLAIMS it, and this box claims neither. What it does is record the
  measurement, so the act that amends them does not have to re-derive it.
  **A FIFTH occurrence is in the packet and is of a different kind**, named so
  that a later reader who greps the packet for that figure does not read it as
  one this box missed: `review/ratification-2026-09-05.md`:549 quotes the
  figure inside the residual question `design.md` § D3 left open AT
  ratification. That file is a RECORD — `Status: ratified`, decision date
  2026-09-05, ratified baseline `6935fb8b` — of what the packet said on the day
  it was ratified, so no later act amends it, including the act that corrects
  the four live ones. **The grep is named WITH ITS SCOPE, because the bare
  instrument does not reproduce that five.** Run over the whole packet —
  `grep -rn "30,410" openspec/changes/split-opendox-two-layer-product/` — it
  returns **TWELVE** lines at this head, and they decompose exactly: **seven**
  are `tasks.md`'s own (the box's design-time figure in the § 3.4 text above,
  and six lines of this STATUS's prose about it — a share that GROWS with every
  fix round, this sentence included), **four** are the LIVE citations named in
  the paragraph above, and **one** is the RECORD named here. **The five this
  paragraph counts are those last five: every occurrence OUTSIDE the box's own
  text**, which is the scope an act that amends them works on. *(The sentence
  said "finds five" against an unscoped grep that returns twelve — a Copilot
  finding on #1035, accurate, taken at fix round 11. It is the same lesson as
  the hunk positions, the placeholder-marker grep and the README line numbers
  below: an instrument cited without its scope and its head stops reproducing,
  and here the amendment's own prose is what moved the count.)*

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
  still fails); (iv) the **THREE** floor acts above — RULED **Q6**'s
  `re_destined:` row form (`#1011` → `880c821c`) and the pin lockstep (`#1054` →
  `3c614d34`) have LANDED, and the `retired:` row form is the next carve-floor
  act and has not; all three are listed because each is its own claim rather
  than a condition of this box, which is what this list records *(the item read
  "the two floor acts above" from before the pin lockstep was named as a third
  act in the paragraph above it — a Copilot finding on #1035, accurate, taken at
  fix round 10)*; and (v) **the packet's own
  README entry, overtaken and NOT corrected here** — the packet's OpenSpec
  Records entry in `README.md` still reads *"IT STILL PERFORMS NOTHING. No
  repository is created, no code moves …"*, written 2026-09-05 (`ceb6dc9e`,
  `8b297c2f`) when that was exactly true and no longer is: `openDox-code` and `openXdox-code` exist and were cut
  from the carve commit `b075fd91` (tag `opendox-carve-0`), and **ALL EIGHT
  slices above are merged** *(this read "six of the eight" when it was authored
  and stayed stale through S7's and S8's landings — a suppressed Copilot finding
  on #1035, accurate, taken at fix round 6; the count is the one § 3.4's STATUS
  paragraph and the table above both carry)*. The staleness predates this amendment and is
  not made by it; it is left to the act that CLAIMS that text — the same rule
  this box applies to `design.md`'s and `proposal.md`'s four *"30,410"*
  occurrences — which is the packet's ARCHIVAL act, the README **OpenSpec
  Records** block being both where an archived packet's entry is rewritten and
  (lane-collision protocol, Rule 6) the one block a landing window exists to
  serialize. Recorded here so that act does not have to rediscover it.
  **An in-place correction at a realization landing HAS a precedent in this very
  block, and the precedent is a RULING**: the `add-declared-former-id` entry
  (`README.md`:534 at this head) was amended by its own realization, lane
  `openxfactory-1`, on Brett Heap's word of 2026-09-15 — verbatim *"Amend the
  row in #1041"*, recorded at `#1003` comment `5686628685` and quoted in the
  entry itself. So the path is open, and it is not this box's to take: it needs
  its own ruling and its own claim, and it lands on the one block a landing
  window serializes. *(A Copilot finding on #1035 asked for the correction to be
  made IN this landing rather than deferred; this paragraph is the answer,
  registered at fix round 11 and declined here on the rule this box applies to
  `design.md` and `proposal.md` alike — a document is amended by the act that
  CLAIMS it.)*
  **That entry is cited by its SENTENCE and not by a line number, deliberately,
  and it is the one citation in this box that could not be one.** Every other
  measurement here names the tree it was read at; this one can name no line,
  because the block it sits in is rewritten by every archival act and its line
  numbers move under any citation that outlives one. Measured rather than
  asserted, and now at SEVEN NAMED COMMITS rather than two: the entry opens at
  `README.md`:**1775** at openxFactory `main` `8944758c`, at :**1875** at
  amendment #3's pre-merge head `0a835098` — after `#1042` archived a sibling
  packet above it — at :**1813** at `main` `cb2d3a2c`, at :**1708** at `main`
  `c5f68457` and at amendment #4's head `cbc3a2c6` which merges it, and at
  :**1836** at `main` `4cef77af`, and :**1836** again at `main` **`ec5069bc`**
  — the `main` this branch merged, and therefore a commit in this pull
  request's own history that cannot go stale before the merge: **five
  positions across SEVEN NAMED COMMITS**, every move made by acts with nothing
  to do with this one. **This branch's own head is deliberately NOT an eighth
  entry**: it is not an immutable ref while the pull request is open, the
  paragraph's whole claim is that every value here names a tree, and the
  position it would report is `ec5069bc`'s anyway, inherited by merge rather
  than measured afresh. *(A Copilot finding on this amendment's own pull
  request, raised at two heads running, and correct both times.)*
  *(THIS SENTENCE SUFFERED ITS OWN THESIS, and the repair is amendment #5's,
  registered on amendment #4's pull request at comment `5702674145` — found
  by this lane's own sweep rather than by a review. It read *"three positions
  across four trees"* and extended the `cb2d3a2c` reading to *"this
  amendment's own head"*; at that head the entry had already moved to
  :**1708**, because the `main` amendment #4 merged (`c5f68457`) took 105
  lines out above it. A box whose whole point is that this block's line
  numbers move under every archival act had, within three commits, cited one
  that moved. The values above are each bound to a NAMED tree and none of
  them is "today"; the count will keep growing and that is the box working,
  not failing.)* The `30,410` citations beside it are
  **exact at every one of those seven commits** — re-measured by amendment #5
  at all seven (`design.md` 2, `proposal.md` 2, the RECORD 1, at `8944758c`,
  `0a835098`, `cb2d3a2c`, `c5f68457`, `cbc3a2c6`, `4cef77af` and `ec5069bc`
  alike). **FIVE occurrences in all: FOUR LIVE plus ONE RECORD.** The four live
  ones are `design.md`:52 and :351, `proposal.md`'s `code_surface:` front-matter
  line (:2) and `proposal.md`:208; the fifth is
  `review/ratification-2026-09-05.md`:549,
  which is the RECORD no later act amends — because no act has touched those
  three files since. *(This clause read "`README.md`:1875–1879" until fix round
  4, which measured the drift rather than re-pointing a number that moves again
  at the next archival — as it now has, twice. Until fix round 5 the list here
  named FOUR and had swapped the RECORD in for the `code_surface:` line while
  calling them "the four citations above", where the inventory above
  distinguishes four live from one record: a Copilot finding on openxFactory
  `#1035`, accurate, and the same set stated two ways is exactly the defect the
  fifth-occurrence paragraph above exists to prevent.)*
  `#656` records: CLAIM
  `5656686020`; rulings `5642758731` · `5647678655` · `5648044785` ·
  `5648049748` · `5648065587` · `5649094228` · `5656343213`.
  **THE Q7 TRIO IS COMPLETE — recorded by `tasks.md` amendment #6,
  2026-09-18.** `opensoft/openXdox-code` **#22 → `fa792cbb`**, merged
  **2026-09-18T09:53:32Z**: *"§ 3.4 RULED Q7 — the gate loop's stylesheets
  arrive with the bindings"* (LANDED note `5728368097`). **This box is already
  `[x]` and the record does not move it**; it is written here because the box's
  own evidence names Q7's acts, and a reader meeting the trio's third landing
  elsewhere should find it accounted for at the box that owns the ruling.
  **THE S7 RESIDUE PAIR IS COMPLETE — recorded by `tasks.md` amendment #6,
  2026-09-18** (`#656` note `5730727921`). `openxFactory` **#1085 →
  `1da7ea6e`** at **13:29:34Z**, *"§ 3.4 slice-S7 RESIDUE row annotation:
  declare the seven display-facet leaves"*, and `opensoft/openDox-code` **#28 →
  `52b237e8`** at **13:30:20Z**, *"§ 3.4 S7 residue: thread the display facet to
  the seven leaves it never reached"*. **This box is already `[x]` and the
  record does not move it.**
  *(RULED Q-L1's annotation-first rule holds again in FORM — the annotation
  merged 46 seconds ahead of its leg — but **the holding COUNT above stays at
  SEVEN and must not be read as an eighth**. That count is stated as one
  holding per ANNOTATED SLICE, and this pair is RESIDUE to S7, whose holding is
  already counted at 21:40:25Z/21:41:36Z on 2026-09-15. A residue pair that
  obeys the rule is evidence the rule is durable, not a new member of the
  enumeration; counting it would silently restate a figure this packet has
  already had to correct once. The arc remains eight slices and seven
  annotated holdings.)*
- [x] 3.5 `[oD]` The runtime, on the `xFactory-Hermes-Install` pattern (RULING
  Q2): FastAPI + Postgres, `migrations/` (ordered SQL, `0001` pinned canonical
  plus additive), `deploy/compose/` and `deploy/kubernetes/` — **all at the root
  of `openDox-code`, not of the assembly root** — one lifecycle CLI,
  OIDC through the Keycloak broker. The schema holds ONLY identity and
  coordination (RULING Q1): users, memberships, projects, the
  project-to-repository map, sessions, unsaved drafts.
  **TICKED 2026-09-18 by `tasks.md` AMENDMENT #6**: `opensoft/openDox-code`
  **#25 → `aca94ecb`**, merged **2026-09-18T18:15:40Z**, *"§ 3.5: the openDox
  runtime — FastAPI + Postgres, identity and coordination, and nothing else
  (RULED Q1/Q2)"*. The landing word was RULED 2026-09-18 17:55Z (`#656` comment
  `5734029578`) after a THIRD mini-batch took three security items; **the word
  authorized the landing and the box ticks on the LANDING**, which is the same
  two-act ordering § 6 uses for a disposition and § 5.3 used for `#1059`.
  **TWO THINGS ARE OWED AND NEITHER IS THIS BOX'S CONDITION.** First, **#25
  landed with three suppressed Copilot findings REGISTERED rather than fixed**,
  taken by the follow-up under the same claim — the same land-and-register shape
  § 5.5 used for `#1105` → `#1110` and § 3.7 used for `#1086`, now three times in
  this packet and therefore a practice rather than an exception. Second, **item
  (4), the `OPENDOX_SERVED_DATABASE` declaration, is a FOLLOW-UP ACT and was
  deliberately NOT in batch 3** — recorded so a reader meeting #25's landing
  does not expect that declaration in it, nor read its absence as an omission.
- [x] 3.6 `[oD]` **openDox CREATES A REPOSITORY AS A FIRST-CLASS ACT**, or the
  origin complaint returns one level down: RULING Q1 answers *"no good place to
  store my projects"* with its coordination half while the specs still land in a
  repository. Includes RULING C3's standalone shape — a PLAIN LOCAL GIT
  REPOSITORY per project, commits as the write path, a remote attachable later —
  as the trivial conformant adapter implementation, not as a mode.
  **TICKED 2026-09-18 by `tasks.md` AMENDMENT #7**: `opensoft/openDox-code`
  **#26 → `4f8ae01e`**, merged **2026-09-18T21:20:16Z**, *"§ 3.6: openDox
  creates a repository as a first-class act, with RULING C3's conformant
  local-git adapter"*. **The box's two halves are both in the landed files**:
  the first-class act is `src/opendox/runtime/repository_act.py`, and RULING
  C3's standalone shape is `src/opendox/runtime/local_git_adapter.py` — an
  adapter IMPLEMENTATION, which is what the box asked for, *"not a mode"*.
  **THE SECURITY HOLD IS DISCHARGED, AND HOW IT WAS CLOSED IS THE RECORD WORTH
  KEEPING**: the credential exposure at `app.py:1076` was fixed at `fe421882`,
  and the remaining findings were closed by **ONE REDACTOR AT THE BOUNDARY**,
  with the **pgid taken at `Popen`** and the **decoder bound** — one instrument
  for one class rather than one fix per finding, the shape this packet has
  preferred since `floor37` § 6.
  **AN OVERRUN IS RECORDED RATHER THAN PASSED OVER**: the actor pushed THREE
  times against a one-push word. It is accepted, and it is written down because
  a bounded round that silently runs long stops being a bound — the accepting
  is the act that keeps it honest, not the forgetting.
  **REGISTERED AS ONE FOLLOW-UP ACT under the same claim, and NOT a condition of
  this box**: three suppressed Copilot findings, `S8544`, and the
  `OPENDOX_SERVED_DATABASE` declaration — the fifth use of the land-and-register
  pattern in this packet.
  **THAT FOLLOW-UP HAS PART-LANDED — recorded by AMENDMENT #8, 2026-09-19.**
  `openDox-code` **`#30` → `5c867137`**, merged 2026-09-18T22:12:50Z, takes the
  seven findings `#26` registered plus eight cases. **Follow-up 2 is in flight**:
  the linked-worktree descriptor binding (RULED `5736683962`), `RefusedError`
  → 409, the fallback narrowing, and the mismatched-database cases. **Neither
  moves this box, which ticked on `#26`'s landing**; they are recorded here so
  the register stays where the instrument is.
  *(The superseded reading follows, kept because it records why the box was held
  at all.)*
  **PRIOR STATUS — LANDING WORD GIVEN, BUT #26 HAS NOT LANDED, AND THE BOX STAYS
  `[ ]`** (RULED 2026-09-18 17:55Z, `#656` comment `5734029578`; recorded by
  `tasks.md` amendment #6). The realization is `openDox-code` **#26**, paired
  with **#25** under the same word and the same third mini-batch of three
  security items. **#25 landed and § 3.5 ticks on it; #26 did NOT, and this box
  does not tick on its sibling's landing.**
  **THE REASON IT IS HELD IS A SECURITY DEFECT, AND IT IS WORTH RECORDING AS
  ONE**: #26's BASE MERGE introduced a **credential exposure at `app.py:1076`**,
  which is being fixed in #26 itself before it lands (holder decision, `#656`).
  *No credential is reproduced here, and none should be — the record needs the
  FACT, the file and the disposition, not the value.* **A landing word is not a
  landing**: the word was given before the defect was found, and it authorizes
  the act rather than certifying the result, which is exactly why this ledger
  ticks on landings and not on authorizations. Item (4), the
  `OPENDOX_SERVED_DATABASE` declaration, remains a follow-up act under the same
  claim and is not in batch 3.
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
  **BOTH MISSING READERS ARE NOW RULED AND IN FLIGHT — 2026-09-17, `#656`
  comment `5714365086`** (Brett Heap, by interactive multi-choice, on three
  questions from the helper's read-only `floor37` actor). **The verdict does
  not move and the box does not tick**; what changes is that the two build
  tasks named above now have rulings and pull requests.
  **Q-F1 (a) — how FLOOR PART 3 runs against a GIT-HISTORY reader: the
  DESTINATION transposes the corpus into git and says so**
  (`conformance_corpus.transpose()`, run with `--corpus <transposition>`),
  documents, keys and bytes unchanged. **`openxFactory` ships ONE neutral
  corpus and each reader proves itself on its own substrate** — the
  privileged route, `openxFactory` shipping both forms, was DECLINED, and so
  was ruling openDox's reader out of scope by deleting the word *"EVERY"*.
  That second refusal matters to this box more than the first: deleting
  *"EVERY"* is the shape of narrowing this box's own STATUS already calls
  *"FLOOR PART 3 deleted to tick FLOOR PART 3"*. The act is `openxFactory`
  **#1086** (*"FLOOR PART 3 accepts a destination's TRANSPOSED corpus and
  proves it faithful"*), OPEN as a DRAFT when read at 2026-09-17T14:34Z.
  **The clock is on the reading and not on the sentence** — a pull
  request's draft state is the most perishable thing this file cites, and an
  unbound *"is a draft"* turns false the hour somebody marks it ready.
  **Q-F2 (a) and Q-F3 (a) ARE TO LAND IN `openDox-code` #26, which is OPEN as
  a DRAFT at head `2f4f8114`, read 2026-09-17T14:36Z** — *to land*, not landed,
  and the figures below are the measurement, not the merge: `LocalGitCorpus`
  GROWS the three per-corpus construction data (`write_path`, `kind_field`,
  `required_fields`, defaults = today's values) and takes the
  `CORPUS_UNREADABLE` refusal-kind fix — measured **17 of 17** with a
  diagnostic subclass supplying the three — and `resolve` pins the
  repository root and REFUSES an enclosing repository, because *"a reader
  that can commit into somebody else's clone does not land"*.
  **WHERE THE TWO DESTINATIONS STAND, each figure bound to the tree it was
  read at** — because a reader who re-runs these at a later head of a moving
  draft and gets a different number should be able to tell drift from error:
  openDox's reader read **11 of 17** at `openDox-code` **#26** `6c8f19e7`
  **when pointed at a TRANSPOSITION of the corpus** (`floor37`'s read of
  2026-09-17T12:11Z, the measurement RULED Q-F1..F3 was given on). **A TREE
  IS NOT ENOUGH TO BIND A FIGURE — THE INPUTS BIND IT TOO**: the SAME reader
  at the SAME commit reads **1 of 17** when pointed at the fixtures AS THEY
  SHIP, refusing at resolution with `corpus-unclassifiable — the directory is
  not a git repository` and leaving sixteen *"not reached"*, which is the
  figure `openxFactory` #1086 records and the whole reason RULED Q-F1 exists.
  Neither number is the other's correction. It **reads `OK — 17 of 17
  check(s)`, exit 0, once Q-F2's
  construction data is applied in #26** — the REAL class, not the diagnostic
  subclass 17 of 17 was first reached with. **#26 does not thereby claim this
  box and says so in terms**: § 3.7 also owes a DECLARED factory and Q-F1's
  transposition, which is a separate act at `openxFactory` (#1086); **openXdox had no
  reader at all** at `openXdox-code` `589adee7`, where the runner refuses
  `conformance-adapter-undeclared` — **and now has one IN FLIGHT and not yet
  landed**, `openXdox-code` **#23**, OPEN as a draft at head `70ea05a9` read
  2026-09-17T14:45Z; its build is § 4.5a above, entered by
  this amendment on 2026-09-17; and the control, `openxFactory`'s own
  § 2.2a adapter, is
  **17 of 17**. **This box
  ticks when EVERY destination passes — openDox after #26 plus the Q-F1
  transposition, openXdox after § 4.5a lands — and not before.** § 8.2 reads
  this evidence, so nothing downstream loosens while it stands open.
  **REGISTERED, NOT YET CORRECTED — RULED Q-T1 (a), 2026-09-18.** Two figures in
  this box's inventory of the conformance machinery were put to the ruling as
  stale, and the correction is owed as ONE append **WHEN THIS BOX TICKS**, not
  before — non-normative figure currency, the class this packet has been
  repairing since amendment #4. **MEASURED HERE RATHER THAN CARRIED FORWARD, AND
  BOTH OF THEM HAVE NOW MOVED, AND ONE MOVED WHILE THIS AMENDMENT WAS BEING
  WRITTEN**. Every figure below is bound to `openxFactory`
  **`83a055a6`**, an IMMUTABLE MEASUREMENT SHA with `#1086` merged in, and must
  be re-derived rather than quoted.
  *(CORRECTED BY `tasks.md` AMENDMENT #7. This read "this amendment's own
  head" — a phrase that moved SIX times while amendment #6 was written, and
  which #6 used for TWO DIFFERENT COMMITS, here and at § 8.9 residue (v). Each
  reading is now bound to its own sha. **An evidence line names a commit, never
  a position in a process.**)*
  • `tests/carve_conformance/` is recorded above as **34 tests**; at `83a055a6`
  `test_verify_carve_conformance.py` carries **79** `def test_`, and it is the
  only test file in that directory.
  • The refusal codes are **SIX, not five**: `conformance-unreadable`,
  `-adapter-undeclared`, `-adapter-unresolvable`, `-corpus-missing`,
  `-check-failed`, and — added by `#1086` — **`conformance-corpus-unfaithful`**,
  the refusal that carries FLOOR PART 3's transposition contract.
  • The corpus is **still 17 checks** (`len(carve_conformance.CHECKS)`).
  *(This paragraph said "ONLY ONE OF THE TWO HAS MOVED", gave 35, and asserted
  the refusal codes were "STILL EXACTLY FIVE". All three were true when written
  and two were false by the time the amendment reached its window, because
  `#1086` landed in between and this branch then merged it. **The paragraph
  predicted exactly this** — it says a test count *"is exactly the kind of figure
  that moves under acts with nothing to do with it"* — and was then overtaken by
  it inside a single amendment. Caught by Copilot against head `83a055a6`.*
  **The instruction to the ticking act is unchanged and is now better evidenced:
  re-measure all three at YOUR head. A count in this row is a reading, never a
  fact.**
  *(The SIXTH refusal code matters beyond currency: a registered inventory that
  names five would send the next act to re-verify a refusal contract with one
  member missing, and `conformance-corpus-unfaithful` is precisely the member
  § 3.7's own transposition STATUS above depends on.)*
  **RULED Q-T2 (a) — NO CHANGE; the seventeen stay closed.** The list-versus-tuple
  reading of `list_documents` (raised at comment `5716870896`) is answered: the
  interface's return type is not widened and the corpus's seventeen checks are
  not reopened to accommodate it.
  **STATUS — THE TRANSPOSITION PROOF IS LANDED, AND THIS BOX STILL DOES NOT
  TICK.** `openxFactory` **#1086 → `049d54a9`**, merged **2026-09-18T17:09:24Z**,
  *"FLOOR PART 3 accepts a destination's TRANSPOSED corpus and proves it
  faithful"* — RULED **Q-F1 (a)**, `#656` comment `5714365086`; recorded by
  `tasks.md` amendment #6 (`#656` note `5733472993`).
  **What it discharges is the RULING, not the box.** This box's own words are
  *"EVERY DESTINATION PASSES IT"*, so it ticks only when **BOTH destinations
  pass the neutral corpus** — openDox and openXdox — and a
  proof that a TRANSPOSED corpus is faithful is the machinery those passes will
  run on, not one of the passes. Accepting the landing as the tick would
  discharge a two-destination condition on zero destinations.
  **THE THREE SIDES, MEASURED PER REPOSITORY 2026-09-18 BY AMENDMENT #7. THE
  `openxFactory` SIDE HOLDS; NEITHER DESTINATION PASS IS EVIDENCED YET.**
  • **`openxFactory` — HOLDS.** `#1086` → `049d54a9` (the transposition
  accepted and proved faithful, RULED Q-F1 (a)) and its follow-up `#1113` →
  `4401e1aa`, merged 18:00:25Z, closing the four findings `#1086` registered.
  • **openDox — NOT EVIDENCED YET, BUT NOW AT THE GATE.** At the time of
  amendment #7 `openDox-code` carried **no conformance reader at all**; see the
  measurement below. **`openDox-code` `#31` is now OPEN at head `4b9714d0`**,
  *"§ 3.7 FLOOR PART 3, openDox side: the declared conformance…"* — the
  missing reader. **This bullet ticks on its LANDED sha together with its own
  `OK — 17 of 17` evidence comment, and on nothing less**: the openXdox side
  has just shown that a reader existing is not a pass recorded.
  • **openXdox — THE READER HAS NOW LANDED, AND THIS BULLET IS BOUND TO TWO
  CLOCKS BECAUSE IT CHANGED UNDER ITS OWN AUTHOR.**
  **Measured at 21:40Z**: the pull request offered was `openXdox-code` `#22` →
  `fa792cbb`, titled *"§ 3.4 RULED Q7: the gate loop's stylesheets arrive with
  the bindings that own them"* — § 3.4's Q7 trio, already recorded at that box
  and nothing to do with the conformance corpus; and **`transpose` occurred ZERO
  times anywhere in `openXdox-code`**. On that reading the side was absent.
  **Measured again at 21:54Z, and the answer moved**: `openXdox-code` **`#23` →
  `3ee8cd31`**, merged **2026-09-18T21:46:37Z** — SIX MINUTES AFTER the sentence
  above was written — lands `src/openxdox/conformance_corpus.py`,
  `src/openxdox/corpus_shape.py` and `src/openxdox/domain_corpus_adapter.py`
  with their tests. **That module is exactly the `openxdox.conformance_corpus:reader`
  § 4.5a's exit command names**, so the openXdox READER exists and the earlier
  "absent" reading is superseded.
  *(`transpose` was the WRONG TOKEN to test with, and saying so is the point of
  keeping both readings: it is the transposition PROOF's vocabulary, not the
  corpus reader's. A search that returns zero answers only the question it was
  asked. The first reading is kept rather than overwritten because it was true
  when taken and because a bullet that silently re-wrote itself would hide that
  this ledger's own evidence can age in minutes.)*
  **THE SIDE IS STILL NOT DISCHARGED, AND THE BOX STAYS `[ ]`**: § 3.7 asks that
  every destination PASS the corpus, and a reader that exists is not a pass
  recorded. The exit line — the three-argument command returning **`OK — 17 of
  17`** at `openXdox-code` `main` `3ee8cd31` — is owed, and § 4.5a owes the same
  line for its own tick.
  **`#26` WAS EXPECTED TO SUPPLY THE openDox SIDE AND IT DOES NOT — MEASURED,
  2026-09-18, BY AMENDMENT #7.** `openDox-code` `#26` → `4f8ae01e` landed and
  § 3.6 ticks on it, but its FIFTEEN changed files are the runtime and its
  tests — `app.py`, `cli.py`, `config.py`, `identity.py`, `local_git_adapter.py`,
  `repository_act.py`, `tests_runtime/`, `docs/runtime.md`, `validate.yml` — and
  **NOT ONE of them is a conformance file**. `openDox-code` carries a
  `corpus_adapter.py` of its own, but it was already there and `#26` did not
  touch it. **`#26` was offered as carrying `transpose()` plus a factory; its
  diff contains no `def transpose` at all**, and across `openDox-code` the token
  `transpose` occurs in exactly ONE file, `src/opendox/doxbench_abstract_store.py`,
  which `#26` did not touch either. What `#26` does with the corpus adapter is
  IMPLEMENT its Protocol for the local-git case — which is § 3.6's subject and is
  why § 3.6 ticks on it. **So this box still waits on BOTH destinations, and
  citing `#26` here would be evidence claimed as proof it cannot give** — a
  landing in the right repository is not a pass of the corpus, and the box asks
  for the pass. The openXdox side remains § 4.5a, which is `[ ]`.
  **THE FOLLOW-UP'S SCOPE IS FOUR REGISTERED FINDINGS**, booked HERE rather
  than as § 8.9 residue because they belong to this box's own instrument:
  `#1086` landed AS IS at head `43a48ed5` with four Copilot findings
  **registered rather than fixed** (`#1086` comment `5732073951`), and the
  helper's `transpose37b` takes them as ONE follow-up pull request under claim
  `5714686940`. **They are not a condition of this box either** — the box waits
  on two destination passes, and these wait on their own act.
  *(Registering findings and landing anyway is a legitimate move and is the
  same shape § 5.5 used for `#1105` → `#1110`. It is recorded in both places
  because the pattern only works if the register is somewhere the next reader
  actually looks, which is the box that owns the instrument — not a residue
  list at the far end of the file.)*
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
  doc-health is lawful; **FIVE ARE ROUTED TO `openDox` UNDER THE CARVE** (routed
  there, which is a disposition, not a finding that they satisfy the seam — see
  the STATUS), **ONE stays in `openxFactory`** under RULED DQ-1, and **FIVE were
  DISCHARGED at the § 2 seam** and no longer exist as imports at all.
  *(AMENDED 2026-09-16 by RULED **R-1**,
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
  **STATUS — authored 2026-09-14, re-verified at this amendment's landing,
  2026-09-16; box STAYS OPEN, and the residue is now fully
  accounted for: § 3.4 moved none of it, and five of the eleven were
  DISCHARGED BY THE § 2 SEAM rather than relocated.** Re-measured 2026-09-14 at
  four trees — openXdox-code `main` **`c1ad341a`** (S5 leg A landed),
  openDox-code `main` **`8efb3cf5`** (S1–S6 landed), openxFactory `main`
  **`e6e1c968`**, and the carve commit **`b075fd91`** both legs were cut
  from — counting only real import statements
  (`^[[:space:]]*(from|import)[[:space:]]+.*doc_health`), each under the root that
  repository actually keeps them in: `src/openxdox/` at openXdox-code,
  `src/opendox/` at openDox-code, and `scripts/ideation_dashboard/` at
  openxFactory (both at `main` `e6e1c968` and at the carve commit — openxFactory
  has no `src/`, which is why a single root spelling would not reproduce).
  **RE-RUN AT THE FINAL HEADS for this landing (2026-09-16)**, because a header
  that says re-verified has to name what it re-verified and the rows below were
  taken at the S5-era trees: openXdox-code `main` **`0a0265f7`** (S8 leg A
  landed) returns the same **13** sites in the same **8** modules, per file
  identical to `c1ad341a` — `cli_gate` 1, `completeness` 1, `corpus_root` 1,
  `gate_console` 4, `gate_routes` 1, `generator` 3, `round_trip` 1,
  `snapshot_registry` 1; openDox-code `main` **`0b4e8bbf`** (ALL EIGHT landed)
  returns the same **5** — `serve.py` 1 and `workbench.py` 4 — with
  `workbench`'s four at **:746, :1407, :1408, :1409** unmoved and `serve`'s one
  at **:713** where `8efb3cf5` had :710, three lines down under the leg edits
  above it and the same import; and openxFactory `main` **`a499061e`** returns
  the same **3** — `doxbench_status_exemption.py`:63 and
  `serve_openxfactory_lanes.py`:178, :277. **Every COUNT below is unchanged at
  the landed heads; exactly one line number moved, and it is named here.**
  (A Copilot finding on #1035, accurate: the intervening slices are what a
  re-verification claim has to rule out, and this is the path-level check that
  rules them out.)
  All 23 of
  `design.md` § D3's inventoried outbound imports now have a position:

  | where the 23 stand | count | sites |
  | --- | ---: | --- |
  | `openXdox-code` `src/openxdox/` (the adapter's implementation surface, as 4.1 asks) | **12** | `completeness` 1, `corpus_root` 1, `gate_console` 4, `gate_routes` 1, `generator` 3, `round_trip` 1, `snapshot_registry` 1 |
  | `openDox-code` `src/opendox/` | **5** | `serve.py`:**710** `from doc_health.corpus import RealGit` — that position is `8efb3cf5`'s, and the same import is at **:713** at `main` `0b4e8bbf` (the re-run above); `workbench.py`:746, :1407, :1408, :1409, identical at both |
  | RULED to stay at `openxFactory` (DQ-1) | **1** | `design.md` § D3 inventories it at `doxbench_packet`; the import had already moved by the carve commit and the LIVE site is `scripts/ideation_dashboard/doxbench_status_exemption.py`:63 — `from doc_health.lines import split_keepends`, the same line at `b075fd91` and at `main` `e6e1c968` (reading (ii) below) |
  | **DISCHARGED at the § 2 seam** — the import became an adapter call or a late seam read, so there is nothing left to relocate | **5** | `authoring` 2 → `authoring.py`:317–318, `from .corpus_adapter import DocumentId` + `from corpus_adapter_openxfactory import home_corpus`; `cli` 1 → gone, only the path comment at `cli.py`:14 survives; `serve` 2 of 3 → gone before the carve, which the carve tree itself measures: openxFactory `b075fd91`'s `scripts/ideation_dashboard/serve.py` contains exactly ONE `doc_health` import, `from doc_health.corpus import RealGit` at `:618`, so two of the three inventoried are already absent there. **That surviving `:618` reach belongs to the RELOCATED five, not to this row** — and it did NOT travel in the § 3.4 arc. `src/opendox/serve.py` arrived at openDox-code with the Tranche-B adoption commit **`30c6baf`** (*"adopt the ideation dashboard runtime"*), carrying that import with it: `git log --follow --diff-filter=A` names that commit for the file and `git log -S "from doc_health.corpus import RealGit"` names it for the line. What the ARC moved was the line NUMBER — `:710` at `8efb3cf5`, `:713` at `main` `0b4e8bbf`, three lines down under the leg edits above it, the same import — which is what this box's own re-run records and why *"the § 3.4 arc moved none of them"* stands. *(Fix round 13 wrote "travels to the leg" and a Copilot finding on #1035 read that as the arc relocating it, and so as a contradiction of this box's own sentence: the reading of the wording is fair and the wording is now measured. Its attribution of the move to slice S6 is not what the history shows.)* *(Two corrections at fix round 13, both Copilot findings and both accurate. The cell cited `:618` as if it evidenced the discharge, when what it evidences is the arithmetic 3 − 1 = 2; and it named `from opendox import consumer_reach` at `serve.py`:146 as a late seam reading in the same breath, which is not a `doc_health` site at all — measured: it is openDox-code's OWN internal import of `opendox.consumer_reach`, present at `src/opendox/serve.py`:146 of `0b4e8bbf` and absent from the openxFactory file at the carve, where `consumer_reach` does not appear once. It is struck from this row. The two discharged `serve` imports left no replacement to cite, which is what DISCHARGED means here.)* **The instrument needs its scope, as ever**: `grep -n doc_health` on the carve file returns TWO lines and only one is an import — `:529` is a docstring naming `doc_health.corpus`, `:618` is the import |

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
  residue in the FIVE SOURCE MODULES it was inventoried in any more, and the one
  RULED to stay at openxFactory is not in the module this box assumed.**
  *(This read "holds none of the residue at the source any more" until fix round
  10, where a Copilot finding — accurate — read the unqualified half as denying
  the RULED import that DID stay; the scope was always the five modules the next
  sentence names, and it is now written rather than implied.)* The § 5.2 shed has landed: `scripts/ideation_dashboard/` is
  down to **nine `.py` modules and one subdirectory, `web/` — TEN tree entries**,
  an identical set at `main` `a80f0e3c` and at `main` `e6e1c968` *(this read "10
  files" until fix round 13, counting `web/` as a file; a Copilot finding on
  #1035, accurate, and the count is `git ls-tree` entries, nine of them blobs)*,
  none of the nine `authoring`, `cli`, `serve`, `workbench` or
  `doxbench_packet`. `doxbench_packet`'s one DID stay at openxFactory, as DQ-1
  requires — but the module it stayed IN is the § 2.4 one rather than the DQ-1
  adapter package: the `doc_health.lines.split_keepends` import travelled with
  the `Status:` read that used it into
  `scripts/ideation_dashboard/doxbench_status_exemption.py`:63 under RULED
  OQ-1, which openDox-code's own `src/opendox/doxbench_packet.py`:136–142
  states in terms (*"they took their `doc_health.lines.split_keepends` import
  with them … it can no longer take an openxFactory-only `doc_health`
  dependency along"*) and :66–67 asserts by a neutrality scan. **The two
  candidate homes were the § 2.4 module and the DQ-1 adapter package —
  `scripts/ideation_dashboard/doxbench_status_exemption.py` and
  `scripts/corpus_adapter_openxfactory/` — and BOTH are openxFactory**, so the
  box's *"never comes here"* holds whichever of the two it turned out to be.
  *(This read "Either module is openxFactory" until fix round 13, with
  openDox-code's `src/opendox/doxbench_packet.py` named in the sentence before
  it; a Copilot finding on #1035 read "either" as reaching that openDox-code
  path — which is cited only as the file that STATES this, never as a home for
  the import — so the two are now named instead of implied. Accurate as a
  reading, and the claim it doubted is unchanged.)* the placement is
  recorded because a citation of the DQ-1 package for this import would not
  reproduce. Separately, that DQ-1 ENGINEERING ADAPTER imports `doc_health` in
  **six** places of its own — `scripts/corpus_adapter_openxfactory/adapter.py`:58,
  `check.py`:39–41, `classify.py`:38, `home.py`:59 — and that is where the
  DISCHARGED `authoring` pair's dependency now sits, behind the § 2.2a seam
  instead of travelling to a leg: `authoring.py`:317–318 calls
  `corpus_adapter_openxfactory.home_corpus` (defined at `home.py`:160,
  and reached through the package's own FORWARDING WRAPPER of the same name at
  `__init__.py`:32–40, which is NOT a re-export — it imports `.home` **on the
  call**, at `:39`, deliberately, so the package can be imported without pulling
  the home layout in; the module docstring says why) and `home.py`:59 is the
  `doc_health` import
  that call reaches. Importing doc-health THERE is lawful, which is the whole
  of DQ-1. (iii) **This box's second sentence
  cannot be met AS WRITTEN, and that is a reconciliation owed rather than a
  residue still travelling.** *"The 23 outbound `doc_health` imports become the
  adapter's IMPLEMENTATION SURFACE here"* is a design-time expectation that the
  § 2.1 / 2.2 / 2.2a seam overtook: 12 arrived, 5 routed to openDox, 1 is
  RULED elsewhere, and 5 no longer exist as imports IN THOSE MODULES at all —
  what ended is the outbound import SITE and not the dependency, which reading
  (ii) above places behind the § 2.2a seam at
  `scripts/corpus_adapter_openxfactory/home.py`:59, where importing doc-health
  is lawful and is the whole of DQ-1 *(the unqualified "at all" reads as the
  dependency itself vanishing — a Copilot finding on #1035, accurate, taken at
  fix round 10)*. No further carve
  can move them, so the box is not waiting on § 3.4 (landed), and the wording
  needs a RULING or an amendment rather than another measurement. **The sentence
  that needs it is the box's own closing one** — *"Box stays open until the
  residue carve resolves where the remaining imports land"* — kept as written
  above under this file's no-deletion discipline and SUPERSEDED here: no carve
  can resolve it, because five of the eleven stopped being imports at the § 2
  seam and the other six are placed, so what this box now waits on is that
  reconciliation and not a carve. *(The two exit conditions read as
  incompatible until this paragraph named which one is live — a Copilot finding
  on #1035, accurate.)* Registered
  here, decided nowhere: this amendment records the accounting and leaves the
  box open on it. `#656` record: CLAIM `5656686020`.
  **STATUS — 2026-09-16, RULED R-1 DECIDES WHAT THE STATUS ABOVE REGISTERED, AND
  THE BOX TICKS** (`#656` comment `5690428146`, Brett Heap, by interactive
  multi-choice): *"the residue is settled by the measured accounting … amend the
  box to that accounting and tick it. No further carve."* The note above is left
  unedited as the record of what was registered; its closing "the box stays open"
  is superseded by this line and by the amendment to the box's own second
  sentence. **The accounting was re-derived before the tick, not carried forward
  from that note** — each tree named with the head it was READ at, because two of
  the three had moved since that note was written:
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
  **RE-READ AT THE THREE NEWEST HEADS, AND NOT ONE FIGURE MOVES.** The trees moved
  again while this amendment was open — the S8 legs landed and this branch merged
  the base that records them — so each reading was taken a SECOND time at the heads
  § 3.4's own re-run names: `openXdox-code` **`0a0265f7`**, the same **13** sites
  in the same **8** modules, line for line; `openDox-code` **`0b4e8bbf`**, the same
  **5** — `serve.py`:713 and `workbench.py`:746, :1407, :1408, :1409;
  `openxFactory` **`a499061e`** and again at `main` **`d5dd1ca5`**, the same **3**
  (`doxbench_status_exemption.py`:63, `serve_openxfactory_lanes.py`:178 and :277)
  and the same ten files (nine `.py`) under `scripts/ideation_dashboard/`. The
  older three heads are kept beside the newer because that is where each number
  was FIRST read, which is this packet's own discipline.
  *(A Copilot finding on this amendment's own pull request, round 10, and it
  arrived through the base merge: § 3.4's block above this one names the newer
  heads while this one named the older, which reads as stale evidence even where
  every count agrees. It does agree — measured, not assumed.)*
  12 + 5 + 1 + 5 = **23**, `design.md` § D3's inventory exactly. **No further
  carve can move any of them**, which is the ruling's own finding: the five
  DISCHARGED stopped being imports at the § 2 seam before the carve ran, and the
  five at openDox-code sit where the carve manifest routes their modules.
  **WHAT THIS TICK DOES NOT DECIDE, said here because the word it replaces
  claimed it.** The box first read that those five *"are lawfully openDox's"*,
  and "lawfully" is a verdict R-1 did not give: R-1 settled the ACCOUNTING —
  which imports went where, and that no further carve moves any — not whether
  openDox-code's five satisfy the ratified `corpus-adapter-seam`. **They are a
  live question, and the measurement is written down rather than left for the
  next reader to take.** `openDox-code` carries NO `doc_health` package of its
  own — `git ls-tree -r --name-only` over the whole tree returns no such path, at
  `1e469713` and at today's `main` `0b4e8bb` alike — so its five sites resolve to
  `openxFactory`'s own `scripts/doc_health/` when the tool runs inside an
  openxFactory checkout. The five, identical in line and in text at **both
  `openDox-code` heads named in this paragraph — `1e469713` and `0b4e8bb`** (and
  NOT at the earlier `8efb3cf5`, where `serve.py`'s site is :710; that three-line
  drift is the one recorded above, between a different pair of heads):
  `serve.py`:713 `from doc_health.corpus import RealGit`; `workbench.py`:746
  `from doc_health import corpus`, :1407 `from doc_health import
  DEFAULT_THRESHOLDS, corpus as dh_corpus`, :1408 `from doc_health.families
  import FAMILIES`, :1409 `from doc_health.runner import Context, run_suite`.
  **All five are inside function bodies, none at module scope**, and :746 says
  why in its own comment (*"lazy: keeps this module's graph flat"*).
  Requirement 4 of `corpus-adapter-seam`
  (`specs/corpus-adapter-seam/spec.md`:37-53) says *"no neutral product
  `openxFactory` pins SHALL import `openxFactory`'s own tooling"* and refuses the
  import where *"the dependency has reversed"*. Whether a lazily-resolved read of
  the corpus through the ADAPTER INTERFACE is such an import, or is the
  interface working, is exactly what **§ 3.7 (FLOOR PART 3)** asks and answers
  mechanically. **THE CRITERION § 3.7 APPLIES IS THIS:** the neutral
  conformance corpus green in EVERY destination, openDox included — that
  clause states
  the TEST and not its outcome — and **§ 3.7 is `[ ]` and records that the
  answer the test returns today is NO.** **The result it records is one pass
  and four refusals, said here rather than left to be looked up**: at each
  destination's then-current `main`
  on 2026-09-10, `openxfactory` (the § 2.2a adapter) is **OK — 17 of 17**, while
  `opendox_code` `8e9ffa62`, `openxdox_code` `59600412`, `opendox_spec`
  `41d570e9` and `openxdox_spec` `03eacc61` each return
  `conformance-adapter-undeclared` (`tasks.md`:1194-1205 above, which is § 3.7's
  own evidence, and :1206, where it closes with *"ONE of the three named destinations passes, so
  the box stays open"*). So the floor this tick declines to lean on is RED where
  openDox is concerned, which is the point: § 4.1 claims the accounting, and the
  seam question waits on a gate that has not gone green.
  *(A Copilot finding on this amendment's own pull request, round 13: the
  sentence named the gate and its verdict but not its measured result, which
  reads as a green floor to anyone who does not scroll up.)*
  *(GRAMMAR MADE EXPLICIT, amendment #5, registered at comment `5702227094`
  item 9: the criterion clause and the result clause were joined by a pair of
  dashes, so the first could be read alone as a measured PASS — the exact
  opposite of what the next clause records. The two are now separated into
  what § 3.7 ASKS and what it ANSWERS. No figure moves and no gate loosens;
  the result is still one pass and four refusals.)*
  So the obligation is open where it belongs, at a box that can
  run it, and § 4.1's tick claims the accounting and nothing else. § 8.2's
  archive-gate line reads § 3.7's evidence, so no gate is loosened by this tick.
  `#656` records: CLAIM `5690461589`; RULED R-1 `5690428146`.
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
- [x] 4.5a `[oXd]` **BUILD the corpus-adapter IMPLEMENTATION** — `design.md`
  § D4 machinery **(1)**, the one of the seven that § 4.5 did not name —
  **parameterized by the § 4.4 domain profile, and proved on § 3.7's neutral
  corpus.** Exit evidence is one command and one line, taken from the
  IMPLEMENTATION rather than composed here:
  `python3 scripts/verify-carve-conformance.py --destination openxdox_code
  --dest-root <the openXdox-code checkout> --adapter
  openxdox.conformance_corpus:reader` → **`OK — 17 of 17`**.
  **THREE arguments, not four and not one.** `--dest-root` and `--adapter`
  are each REFUSED-IF-ABSENT by the runner, in that order; the package sits
  under `src/`, which the runner already adds to the import roots, so no
  `--sys-path` is needed. **`--corpus` is deliberately ABSENT**: it defaults
  to the fixture tree (`tests/corpus-adapter/fixtures`) and THIS reader's
  location vocabulary IS a directory tree, so it reads the corpus as it
  ships. RULED Q-F1's `--corpus <transposition>` is for a HISTORY-backed
  reader — openDox's `LocalGitCorpus`, not this one — and passing it here
  would hand a filesystem reader a corpus built for somebody else.
  *(THE ABBREVIATED FORM WAS THIS BOX'S OWN AND IT DOES NOT RUN — measured,
  not supposed: `--destination openxdox_code` alone exits **2** with
  `conformance-unreadable — --dest-root is required with --destination`.
  It also contradicted this packet's own § 3.7, which already records the
  NEXT refusal in that chain, `conformance-adapter-undeclared`, as
  openXdox's state today. A command that cannot be run is not exit
  evidence; the flags are named here so the next reader RUNS it rather
  than reconstructs it.)*
  **TICKED 2026-09-19 by `tasks.md` AMENDMENT #8, on the exit line the box asked
  for.** The BUILD is `openXdox-code` **`#23` → `3ee8cd31`**, merged
  2026-09-18T21:46:37Z — `src/openxdox/conformance_corpus.py`,
  `corpus_shape.py` and `domain_corpus_adapter.py` with their tests — and the
  admissions rows are `openxFactory` **`#1091` → `eb2d4569`** (21:21:19Z).
  **THE EXIT LINE, posted as evidence at `#656` comment `5736681367`**:
  **`OK — 17 of 17`**, **exit 0**, at `openXdox-code` `3ee8cd31` with the runner
  at `openxFactory` `eb1880cb`.
  **THE PROCEDURE IS FOUR STEPS, NOT THREE ARGUMENTS ALONE, AND THE FOURTH IS
  WRITTEN IN HERE RATHER THAN LEFT AS A CAVEAT**: the declared git-pinned
  `opendox` dependency (`pyproject.toml:106`) MUST BE INSTALLED FIRST. A bare
  checkout exits **2** with `conformance-adapter-unresolvable — No module named
  'opendox'` before the corpus is reached.
  *(This is the box's OWN standard applied to itself. The parenthetical above
  already refused an abbreviated form of this command for exactly this reason —
  ***"A command that cannot be run is not exit evidence"*** — when the missing
  piece was `--dest-root`. The missing piece is now an install rather than a
  flag, and the standard does not change with the shape of what is missing. It
  is the same lesson § 8.3's clause-3 recipe learned twice: a procedure that
  needs a step its reader does not have is not a procedure.)*
  **§ 4.1 stays a carve box** and this is not part of it.
  **RULED Q-X1 (a) — 2026-09-17, `#656` comment `5715212264`** (Brett Heap,
  by interactive multi-choice), on three questions from the helper's
  read-only `xdoxadapter` scoping. **The box is NEW rather than a clause
  added to § 4.5, on this packet's own `Na` precedent** — § 2.2a, § 5.2a and
  § 5.6a are all boxes this packet grew when a ruling found work its
  neighbours did not carry, and a build with its own exit evidence is not a
  bullet inside a box that has already ticked.
  **WHY § 4.5 DID NOT ALREADY COVER IT, which is the whole reason a new box
  is honest here.** § 4.5 names THREE features and ticked on all three
  landing (`openXdox-code` #10/#11/#12, 2026-09-11). `design.md` § D4 lists
  **seven** machineries; the reader § 3.7 asks openXdox for is machinery (1),
  and it is the one none of the three named. So § 4.5's tick is undisturbed
  and § 3.7's missing half has a box of its own to tick in.
  **RULED Q-X2 (a) — openXdox's reader is the NEUTRAL, PROFILE-PARAMETERIZED
  reader.** Corpus terms arrive as CONSTRUCTION DATA, derived from the § 4.4
  `DomainProfile` where one is registered — not compiled in. **And RULING
  Q4's clause *"over openxFactory's corpus and check families"*
  (`5542823211`) is RECORDED AS SUPERSEDED, in this packet's no-deletion
  style**: superseded by RULING **C2** (`5544370242`), which made openXdox
  the domain-mapping core PARAMETERIZED rather than openxFactory's reader,
  and by **DQ-1**, which gave `openxFactory` its own § 2.2a adapter over its
  own corpus. Q4's STANDING clause — *"openDox defines a corpus-adapter
  interface; openXdox implements it"* — is untouched and is exactly what this
  box performs. The superseded clause is struck from FORCE and not from the
  record, which is how this packet has treated every overtaken ruling text.
  **RULED Q-X3 (a) — the `CorpusShape` carries `kind_field` and
  `required_fields_by_kind` as construction data for this act**, as
  `openxFactory`'s § 2.2a shape already does. **No spec change and no schema
  change**: the domain profile stays the vocabulary and lifecycle authority,
  and the shape only carries what a reader needs to read.
  **STATUS — CLAIMED 2026-09-17T13:33:17Z (CLAIM `5715212503`, this lane,
  authored by the helper's `xdoxbuild` actor) AND NOW FILED: `openXdox-code`
  **#23** (*"BUILD the corpus-adapter IMPLEMENTATION … answers the
  conformance corpus 17 of 17"*), opened 2026-09-17T13:53:24Z, **OPEN as a
  DRAFT at head `70ea05a9` when read at 2026-09-17T14:45Z**. It carries
  exactly the three modules named below under `src/openxdox/`, plus their two
  test files. **The box does not tick on the filing; it ticks on the
  landing.**
  Measured before the claim at `openXdox-code` `main` **`589adee7`**:
  `--destination openxdox_code --dest-root <the openXdox-code checkout>`
  refuses **`conformance-adapter-undeclared`** and no check is reached
  — which is the same verdict § 3.7 recorded on
  2026-09-10 and is why this box exists.
  *(THE `--dest-root` IS PART OF THE QUOTED COMMAND AND WAS MISSING — without
  it the runner refuses `conformance-unreadable` FIRST and never reaches the
  adapter check at all, exactly as the exit-evidence paragraph above this box
  records. Both refusals are real and they are DIFFERENT refusals; quoting the
  shorter command against the longer one's result made this measurement
  unreproducible and put the box at odds with its own neighbour. Re-measured
  here: bare, `conformance-unreadable — --dest-root is required`; with a
  destination root and no `--adapter`, `conformance-adapter-undeclared`.)*
  Branch
  `build/corpus-adapter-implementation` off `589adee7`: three NEW modules,
  **stdlib plus the PINNED `opendox.corpus_adapter`** and nothing else
  (`corpus_shape.py` carrying the construction data and
  a `from_profile()` over § 4.4's `DomainProfile`, `domain_corpus_adapter.py`
  implementing the six operations against the PINNED `opendox.corpus_adapter`
  under RULED OQ-2/OQ-Q — which is why the dependency line says *plus the
  pinned interface* and not *stdlib-only*, a contradiction this box carried
  between one line and the next — and `conformance_corpus.py` as the declared
  `--adapter` factory), no existing module edited and no `doc_health` reach
  added. Its arrival admissions rows land at `openxFactory` on
  `chore/admit-openxdox-corpus-adapter`. **Q-X4 needed no question**: its
  recommended precondition was the § 3.7 rulings Q-F1/Q-F2 (`5714365086`),
  already in hand, so the build proceeds on Q-F2's construction-data pattern
  rather than inventing a second one.
  **This box ticks on that landing and its one line of evidence, and on
  nothing else.** A possible `openXdox-spec` requirement row for the adapter
  — on § 4.5's own `add-openxdox-projection-surfaces` precedent — is FLAGGED
  and deliberately not scoped here; the building actor measures it and
  reports.
  **THE EXIT SENTENCE THIS BOX TAKES ON LANDING, AND THE ONE CORRECTION MADE TO
  IT.** `openXdox-code` `#23` offers the sentence verbatim in its own body, for
  this box to place: *"BUILD the corpus-adapter IMPLEMENTATION — `design.md`
  § D4 machinery (1), the one of the seven § 4.5 did not name — parameterized
  by the § 4.4 domain profile, and prove it on § 3.7's neutral corpus. Measured
  at openXdox-code `<merge sha>`: `verify-carve-conformance.py --destination
  openxdox_code --adapter openxdox.conformance_corpus:reader` → OK — 17 of
  17."* **IT IS PLACED WITH `--dest-root` ADDED, AND NOT AS OFFERED.** This lane
  measured twice, at amendment #5's rounds 15 and 25, that the runner refuses
  `conformance-unreadable — --dest-root is required with --destination` and
  **exits 2** before any check runs when that argument is absent; the offered
  sentence would therefore record a passing run of a command that cannot run.
  **The defect is the same one this box spent two rounds removing, and placing
  the sentence unamended would replant it.**
  **RULED `5728368325`, 2026-09-18 ~09:55Z** (Brett Heap, interactive
  multi-choice, three questions), on the two disclosures this box's own build
  raised. **(1) `xdoxbuild`'s BOT COMMITS ARE ACCEPTED AS DISPOSITIONED AND THE
  EPISODE IS REGISTERED AS A PROCESS BREACH.** The 2026-09-17 14:40Z ruling
  (`5716232555`) banned `@copilot review` COMMENTS on drafts precisely because
  they make `copilot-swe-agent[bot]` push commits; the relay reached actor
  `xdoxbuild` only at 16:38Z, and `#23` carries **eleven** such comments, **EIGHT
  of them post-ruling** (14:44:30Z-16:36:50Z) and none after the relay, with
  `#1091` carrying one, pre-ruling. **Seven bot commits resulted, and NO PLAIN
  REVERT EXISTS** — each was answered by a forward commit — so the disposition is
  the surviving content at HEAD: `5f947cd` (identity and refresh guards) KEPT;
  `f070e26` (refresh listings on each access) **CONTENT REVERTED**, it deleted
  the listing cache and took 801 documents from 0.07 s to 58.85 s; `fefcb0e`
  (root confinement) KEPT; `5930ff9` (dangling symlinks) KEPT; `6656d7b` (scope
  listing snapshots) **FINDING KEPT, IMPLEMENTATION REPLACED**, no `weakref` at
  HEAD; `a120b79` (a test-name typo) KEPT; and `ecb4496` on `#1091` (admissions
  pin text) KEPT and re-proved by mutation. Bot edits touch only the five CREATED
  files and `openxFactory`'s own `tests/carve_arrival/
  test_verify_carve_arrival.py`; the mutation sweep caught **69 of 69** at
  `5b8e527a`. **The cause is the relay lag and not the actor's judgment**, and
  the correction is procedural: from here every review is requested through the
  reviewer API only. **(2) Q-A, the DIRTY-WORK-TREE READER: LEAVE AS IS.** Both
  readers — `openxFactory`'s § 2.2a adapter and openXdox's
  `openxdox.conformance_corpus` — resolve HEAD over a dirty tree, and they do it
  CONSISTENTLY; the stamp's documented meaning is *"the tree at or after this
  commit"*. No spec text moves and no pin moves. **A refusal would have made an
  editor's swap file render the corpus unreadable**, which is a worse failure
  than the ambiguity it would remove.
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
  upstreams — **and since RULED Q7 (`#932` → `f4fb4ffc`) those upstreams are TWO**:
  openDox is pinned DIRECTLY, in `contracts/opendox-pin.yaml` beside its own
  gitlink, not read out of openXdox's pin.
  *(SECOND CLAUSE AMENDED 2026-09-16 by RULED **R-5**, with the clause below. It
  read "openDox's commit is READ from openXdox's own pin and recorded, if at all,
  as a DERIVED value" — true under RULING F, when openXdox was the only direct
  upstream, and false after Q7 mounted openDox as the second. The RULE is
  unchanged and is the reason the sentence had to move: `openxFactory` declares
  its DIRECT upstreams, and the set of those changed. openXdox's own
  `contracts/opendox-pin.yaml` still pins openDox for openXdox — that is the § 4.2
  chain and it is untouched; what is no longer true is that `openxFactory` reads
  openDox only through it.)*
  **TICKED — #917 → `edf0e24f45b6e7baf5322023cbc1c43d28ff46cd`**,
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
  **TWO OLDER TEXTS IN THIS PACKET'S REACH STILL SAY THE PRE-Q7 THING, AND THEY
  ARE NAMED HERE RATHER THAN LEFT TO COLLIDE WITH THIS CLAUSE** (a Copilot
  finding on this amendment's own pull request, round 12, in both of its halves).
  **(i) § 1.8 above**, `[x]` and DONE, QUOTES the sentence `opensoft/xFactory`
  **#284 → `05cb5abf`** appended to the aggregation's `CLAUDE.md`, and that
  sentence contains *"inside the openDox family, `openxFactory` pins `openXdox`
  ONLY; openDox's commit is read through openXdox's own pin — RULING F"*. The box
  is a RECORD of what landed and stays verbatim; what is overtaken is the
  AGGREGATION'S OWN FILE, which now describes a pin chain the estate no longer
  has. Repairing it is an act on `opensoft/xFactory`, the same class as the § 8.7
  re-point, and it is not this amendment's to make.
  **(ii) This packet's own `neutral-product-pin` DELTA**, whose RULED OQ-2
  narrative (`specs/neutral-product-pin/spec.md`:61-73, 2026-09-04T22:16Z) records
  *"openDox is pinned only by openXdox … No third MODIFIED requirement is added"*,
  and whose CHAIN scenario (:220-223) refuses *"a second declaration of A's commit
  at the consuming level"*. **The NORMATIVE rule is not contradicted, and the
  reason is the word DIRECT**: :195-199 requires each level to declare ITS OWN
  DIRECT UPSTREAM and forbids re-declaring a TRANSITIVE one, and Q7 made openDox
  a DIRECT upstream of `openxFactory` — a mounted submodule it consumes, not a
  product it merely reaches through openXdox. **The refusal shape at :225-227
  cannot fire either, measured live at `main` `d5dd1ca5`**: `openxFactory`'s
  `contracts/opendox-pin.yaml` reads `commit: 3819625e…`, its `openDox` gitlink
  reads `3819625e…`, and openXdox's OWN `contracts/opendox-pin.yaml` at the
  pinned `a6500141` reads `commit: 3819625e…` — three declarations, one answer,
  kept equal by the lockstep pin act (`#1054` → `3c614d34`, openDox `#8`,
  openXdox `#10`). **What IS owed is a dated amendment to the delta's OQ-2
  narrative**, which still reads as though a direct openDox pin were ruled out,
  and it is owed from the act that CLAIMS that spec — this packet's own
  promotion, or an amendment that names it — not from a `tasks.md` amendment,
  on the same rule this amendment applies to `design.md`, `proposal.md` and the
  scenario-4 defect recorded at § 7.1.
  `python3 scripts/verify-openxdox-pin.py` passes live at **#917's `edf0e24f`**, the
  commit this box TICKED on (named rather than left as "that commit", which three
  paragraphs of amendment now separate from its referent):
  `OK openxdox-pin verified: openXdox@db58fffa58d49d92f58db40bd7e63cad3205052f, gitlink read from HEAD, sorted-ls-tree-r-v1 tree digest recomputed (43c60b29693820d3e8c066e9c6a088f306bf0a7c0f2d818d72ceb62657c53209)`.
- [x] 5.2a `[oxF]` **The FIFTEEN engineering-vocabulary requirements are
  re-promoted HERE (RULING DQ-1), not shed.** They leave the capability
  `ideation-dashboard` and land in `openxFactory`'s own corpus under the § 2.2a
  adapter's own successor capability, whose id this task authors.
  `promotion_fidelity.py` keys on (capability, normalized title), so the successor
  is a distinct key and the REMOVED delta stays visible to the checker. The only
  edit they take is re-expressing path literals as `adapter calls` — one of
  RULING OQ-1's three classes, by name.
  **THE ID THIS TASK OWES IS AUTHORED: `openxfactory-engineering-adapter`**
  (recorded by `tasks.md` amendment #5, 2026-09-16; the box still does not
  tick). The act is `opensoft/openxFactory` **#1071**, *"Propose
  `repromote-engineering-vocabulary`: § 5.2a's successor capability, and the
  fifteen carried into it"*, opened 2026-09-16T19:22:04Z under CLAIM
  `5703096449`, carrying the delta at
  `specs/openxfactory-engineering-adapter/spec.md` inside
  `openspec/changes/repromote-engineering-vocabulary/`. It is a **FILING
  ONLY** —
  `Status: draft` on all three lifecycle documents, no ratification, no
  archive. **The FILING is what this sentence records; a filing buys no
  tick.** The tick's condition is stated ONCE, in the STATUS immediately
  below, and is deliberately NOT restated here.
  *(This sentence read "ticks on ITS landing and not on its opening" until
  the STATUS below grew the ratification clause, at which point the box
  carried two different completion conditions one line apart. Raised at
  review and fixed by deleting the weaker statement rather than restating
  the stronger one twice: a condition written in two places is a condition
  that will disagree with itself.)*
  **#1071 IS FILED AND LANDED — `repromote-engineering-vocabulary`, merged
  2026-09-17T14:43:42Z as `e83f8cd7` (note `5716296239`)**, carrying the
  successor id `openxfactory-engineering-adapter`. **THE BOX STILL DOES NOT
  TICK**: this box ticks on its landing AND on Brett Heap's RATIFICATION of
  that change, for which two judgments are declared — no second REMOVED block
  on `ideation-dashboard`, and it archives BEFORE the split packet. Arc F
  (§ 5.6) waits on its ARCHIVE, which is later still.
  **THREE readings, ALL KEPT**: at
  **2026-09-17T13:58Z** it was non-draft and `CONFLICTING` against `main`; at
  **14:34Z** non-draft and `MERGEABLE`; at **14:43:42Z** merged. It
  CONFLICTED because it collided with
  § 7.4's own #1073 on the README **OpenSpec Records** block — the one block
  the lane-collision protocol's Rule 6 landing window exists to serialize, and
  two acts of the SAME lane hit it on the same afternoon. **The conflict and
  the landing are both behind it now; the RATIFICATION named above is not**,
  and that is what this box waits on.
  *(ALL THREE readings are kept rather than each replacing the last, and that
  is exactly why the earliest was stamped: the state CHANGED TWICE inside
  three quarters of an hour, so claims bound to their clocks all stayed true
  where a single unbound one would have been false twice over. The remedy
  this amendment argues for, demonstrated on its own page.)* The id
  keeps its `openxfactory-` qualifier deliberately: `corpus-adapter-seam`
  requirement 4 makes the neutral capability openDox's under RULING Q4, and
  an unqualified `engineering-adapter` would read as that one.
  *(Recorded here because live work was blocked on the id's absence — **three
  classes, FOUR open acts**: § 5.6's de-floor, § 8.4's both-directions
  accounting, and the two § 6 closures already open, **#1060** and **#1065**,
  each of which carried its delta WHOLE rather than re-author it against an
  unnamed successor. #1071's own body counts THREE, treating the pair of
  closures as one class; the enumeration is identical either way and both
  counts are said here so neither reading contradicts the list — a Copilot
  finding on this amendment's own pull request, round 6, which was right that
  a bare "three" over four named items is a count contradicting its own
  evidence.)*
  **TICKED 2026-09-18 BY `tasks.md` AMENDMENT #6 ON RULED **R-A** — `#656`
  comment `5728607038` (Brett Heap, 2026-09-18 ~10:25Z, by interactive
  multi-choice).** `repromote-engineering-vocabulary` is **RATIFIED**. The box
  asked for the successor id to be AUTHORED and said it ticks on the filing's
  landing; amendment #5 then recorded that the landing alone was not the whole
  condition and that ratification was owed too. **Both are now in hand**: filed
  by `#1071 → e83f8cd7` (2026-09-17T14:43:42Z) and ratified on this word.
  `code_surface: none`, `target_release: implemented`, **so it archives with no
  BUILD — but not yet with no WORK**: the governed archive path refuses any
  packet whose `tasks.md` still matches `^- \[ \]`
  (`scripts/proposal-support.py`, *"change has incomplete tasks"*), and that
  packet's ratification tasks 1.1–1.6 are all open, so **the archive cannot
  land until the encoding act registered below closes them**. Caught by Copilot
  against head `7ac75a4e` and measured true; `code_surface: none` removes the
  build gate, not the task gate. Its archive pull request lands in a
  Rule 6 window AFTER `#1066`, because **§ 6.2** — which is `#1066`'s own
  box — promotes its forward delta INTO
  `openspec/specs/ideation-dashboard/spec.md`. *(This reason named § 6.5
  until it was measured: `#1066`'s title is literally "Close § 6.2 … and ITS
  delta promotes", and its file set touches that spec. The WAIT was right and
  the REASON was wrong, which is the worse of the two errors to leave — a
  correct instruction with a false rationale survives until someone acts on
  the rationale. Corrected on a Copilot finding raised against three separate
  heads before it was measured here.)* **The ARCHIVE is not this
  box's condition and is not claimed as one**: this box owed an authored id, and
  the id `openxfactory-engineering-adapter` is authored, filed and ratified.
  **THE RATIFICATION IS ON THE WORD; ITS ENCODING IN THE SUCCESSOR PACKET IS
  OWED AND IS REGISTERED HERE, 2026-09-18.** Raised by Copilot against three
  separate heads of amendment #6 and MEASURED TRUE at `6c3a8661`:
  `openspec/changes/repromote-engineering-vocabulary/` still carries
  `Status: draft` in `proposal.md`, `design.md` AND `tasks.md`; its own
  ratification tasks **1.1 through 1.6 are all `[ ]`**; and there is no
  `review/ratification-<date>.md` record beside them.
  **This box's tick STANDS**, because what ratifies a change in this house is
  Brett Heap's word and the word was given (RULED **R-A**, `#656` comment
  `5728607038`); the packet's headers RECORD a ratification, they do not
  perform one. **But the record owes the encoding**, and a corpus that says
  `draft` where the ledger says `RATIFIED` is a contradiction a later reader
  will meet without this note. The encoding act — `Status: ratified` plus the
  citation on all three documents, the `review/` record, the README record and
  tasks 1.1–1.6 — belongs to that packet's own owner under its own claim, NOT
  to this amendment, which must not edit a neighbouring packet's lifecycle
  headers on its way past. **Registered, not resolved, and it moves no box.**
  **DISCHARGED 2026-09-18 by `tasks.md` AMENDMENT #7 — the owed encoding has
  LANDED.** `openxFactory` **#1103 → `eb1880cb`**, merged **21:30:14Z** by merge
  commit, archives the packet at
  `openspec/changes/archive/2026-09-18-repromote-engineering-vocabulary`.
  **Measured there rather than taken on report**: `proposal.md`, `design.md`
  AND `tasks.md` all read `Status: ratified`; tasks **1.1–1.6 are all `[x]`**
  with **zero** unchecked tasks remaining; and `review/ratification-2026-09-18.md`
  is present. The contradiction this note registered — a corpus reading `draft`
  where the ledger read `RATIFIED` — no longer exists.
  *(Recorded as a CLOSE rather than by deleting the registration. The gap was
  real, a reviewer raised it against three separate heads, and the record of a
  finding that was right and then satisfied is worth more than a page that
  looks as though it never happened.)*
- [x] 5.2 `[oxF]` **Shed the dashboard corpus down to RULED DQ-1's KEPT SET.**
  The list is `docs/opendox-carve-manifest.yaml` and not a prose inventory: every
  row it routes to a destination LEAVES — **except the twenty
  `not_moved / replicated_at_destination` rows the manifest names**, whose source
  STAYS here while a copy arrives there (`tests/ideation-dashboard/conftest.py`
  and `staging_shapes.py` are two of them, which is why the STATUS below counts
  them present without counting them kept) — and the **117** rows carrying a
  `stays_openxfactory_*` reason (**103** `stays_openxfactory_adapter` + **14**
  `stays_openxfactory_governance`) STAY, because `openxFactory` keeps its own
  adapter and its own governance. Across the NINE SURFACES THE OLD DELETION LIST
  NAMED — which is what these figures walk, and NOT the whole kept set: 107 of
  the 117 kept rows sit in those nine and the other TEN sit outside them,
  enumerated in the STATUS below — measured at the carve commit `b075fd91` and at
  `#940`'s merge `cc4ae9d3`, files at the carve → **files PRESENT after it**:
  `scripts/ideation_dashboard/` 63 → **9**, its `web/` 43 → **1**
  (`views/intent-feed.js`, RULED `not_moved / stays_openxfactory_adapter` under
  OQ-F), `tests/ideation-dashboard/` 157 → **42 present, 40 KEPT ROWS**,
  `tests/ideation_dashboard/` (the four-file underscore spelling) 4 → **0**,
  `scripts/ideation-dashboard-nightly.py` 1 → **1** (it STAYS,
  `stays_openxfactory_adapter`), `scripts/validate-ideation-dashboard-contracts.py`
  1 → **0**, the dashboard contract schemas under `contracts/schemas/` **6 → 0**,
  `examples/ideation-dashboard/` 140 → **44**, and the dashboard governance docs
  7 → **6** (one leaves: `docs/ideation-dashboard-session-runbook.md`,
  `moved_with_declared_edit` to `opendox_spec`).
  *(COLUMN RE-LABELLED, amendment #5, registered at comment `5702227094`
  item 5 — a Copilot finding whose critique was right and whose figure was
  not. The heading read *"files kept"* over a column whose unit is FILES
  PRESENT, and the two coincide almost everywhere, which is what let the wrong
  word stand. Measured cell by cell at `b075fd91` and `cc4ae9d3` against the
  manifest's own kept set, across the five surfaces named by DIRECTORY — the
  only ones where "kept ROWS" is even the same population as "files":
  `scripts/ideation_dashboard/` 63 → 9 present = 9 kept rows, its `web/`
  43 → 1 = 1, `tests/ideation_dashboard/` 4 → 0 = 0,
  `examples/ideation-dashboard/` 140 → 44 = 44 — and
  `tests/ideation-dashboard/` 157 → **42 present against 40 kept rows**, the
  two being `conftest.py` and `staging_shapes.py`, both `not_moved /
  replicated_at_destination`, which is the distinction this box already
  discloses above the table (*"which is why the STATUS below counts them
  present without counting them kept"*). **The four cells named by
  FILE are counted on the OLD DELETION LIST's own populations** — the six
  dashboard contract schemas it names, the governance docs it names — which
  amendment #4 already reconciled as subsets by design in the STATUS below, so
  "kept rows" was never their unit either and re-labelling the column is the
  whole repair. **ONE HEADING was wrong and NO NUMBER was**, which is worth
  saying plainly: the finding asked for a figure to change and the answer is a
  word.)*
  *(THE DISPOSITION VECTOR IS RE-READ AT THREE TREES AND RECORDED HERE SO THE
  NEXT READER DOES NOT RE-RUN IT — amendment #5, registered at comment
  `5702227094` item 6. `docs/opendox-carve-manifest.yaml` yields **456 rows,
  `moved_verbatim` 143 / `moved_with_declared_edit` 175 / `not_moved` 138,
  kept 117** (103 `stays_openxfactory_adapter` + 14
  `stays_openxfactory_governance`) at `main` `cb2d3a2c`, at `main`
  `c5f68457`, and at this amendment's ORIGINAL base `cbc3a2c6` — **identical at all
  three**, which is what the row's own label "`main` `cb2d3a2c`, and this
  branch" asserts and had never been verified across the two base merges that
  happened under it. Twenty rows carry `replicated_at_destination` in
  total.)*
  *(RE-SCOPED 2026-09-16 by RULED **R-2**, `#656` comment `5690428146`, which
  supersedes this box's own deferral of the reconciliation to "a sweep at § 8".
  It read "Delete `scripts/ideation_dashboard/` (48 modules), `web/` (40 files),
  `tests/ideation-dashboard/` (125 files) and `tests/ideation_dashboard/` (the
  four-file underscore spelling), `scripts/ideation-dashboard-nightly.py`,
  `scripts/validate-ideation-dashboard-contracts.py`, the four dashboard contract
  schemas, the 142 packaged examples under `examples/ideation-dashboard/`, and the
  five dashboard governance docs" — a pre-DQ-1 deletion list wrong in SCOPE (the
  nine surfaces it names hold **107** of the 117 rows DQ-1 keeps — **94** in the
  five it names by DIRECTORY and **13** in the four it names by FILE, where a
  literal reading reaches fewer still — while the other **TEN** sit outside every
  surface it names and survive it untouched; 107 + 10 = 117, enumerated in the
  STATUS below) and in **six of its own seven counts** — "48
  modules" (63), "40 files" (43), "125 files" (157), "the four dashboard contract
  schemas" (six), "the 142 packaged examples" (140) and "the five dashboard
  governance docs" (seven); only *"the four-file underscore spelling"* is exact.
  Every figure
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

  **THE TABLE WALKS THE OLD LIST'S NINE SURFACES IN FILES; THE KEPT SET IS 117
  ROWS; THE TWO RECONCILE HERE RATHER THAN BY EYE.** (Raised at Copilot review
  round 8 on this amendment's own pull request, which was right that the kept
  column sums to **103** while the kept set is **117** — a sum that is not the
  kept set and was never meant to be one.) Two cells are deliberately narrower
  than their surface, and one is a different unit:
  - **`contracts/schemas/` reads "0 of the 6"** — a statement about the six
    dashboard schemas that LEAVE, not about the surface. That surface's twelve
    rows also carry **six KEPT rows**: `gate-intent`, `ideation-cross-reference`
    and `ideation-possibles-register` (`stays_openxfactory_adapter`), and
    `project-register`, `xfactory-ideation-organizer-recommendations` and
    `xfactory-ideation-routing-index` (`stays_openxfactory_governance`).
  - **`tests/ideation-dashboard/` holds 42 FILES at `cc4ae9d3` and 40 kept
    ROWS.** The two extra files are `conftest.py` and `staging_shapes.py`,
    `not_moved / replicated_at_destination` — the source stays here AND a replica
    arrives at the destination, so they are present without belonging to the
    kept set. Every other surface matches its own rows one for one: 9/9, 1/1,
    44/44, 0/0 (the underscore spelling), 1/1 (the nightly), 0/0
    (`validate-ideation-dashboard-contracts.py`), and `docs/` 6 of 7 — the
    seventh, `docs/ideation-dashboard-session-runbook.md`, is
    `moved_with_declared_edit` and absent at `cc4ae9d3`.
  **By ROWS the nine surfaces hold 107 of the 117** — 9 + 1 + 40 + 0 + 1 + 0 + 6
  + 44 + 6 — **and the other TEN sit outside the old deletion list entirely**,
  which is why no table of ITS surfaces can sum to 117:
  `examples/ideation-cross-reference/` **4** (its README, the example and two
  negative fixtures) and `tests/corpus-adapter/` **2**
  (`test_no_privileged_route.py`, `test_openxfactory_adapter.py`), six
  `stays_openxfactory_adapter` rows; `tests/notebooklm/` **3**
  (`test_hermeticity_guard.py`, `test_sync_notebooklm_books.py`,
  `test_workbench_sweep_wiring.py`) and `tests/header_contract_oracle.py` **1**,
  four `stays_openxfactory_governance` rows. **107 + 10 = 117**, and by reason it
  is 97 adapter + 10 governance inside the nine and 6 adapter + 4 governance
  outside them — the **103 + 14** this box names.

  **DQ-1's kept set is 117 rows**, and the manifest's 456 rows (`phase:
  post-shed`) split like this — **at TWO heads, because the moving half moved and
  the kept half did not**:

  | head | `moved_verbatim` | `moved_with_declared_edit` | `not_moved` |
  | --- | ---: | ---: | ---: |
  | `cc4ae9d3` (#940's merge) | 169 | 149 | **138** |
  | `main` `cb2d3a2c`, and this branch | **143** | **175** | **138** |

  **Twenty-six rows crossed from `moved_verbatim` to `moved_with_declared_edit`
  between those heads** — 169 − 143 = 26 = 175 − 149 — and the commits that moved
  them are named: the § 3.4 slice annotations `ee251d6c` (S5), `b3a75537` (S7)
  and `e5896455` (S8), each declaring edit lines on rows that had been verbatim.
  `docs/opendox-cutover-runbook.md`:143-145 carries the current split, and
  `tests/carve_manifest/test_carve_manifest.py` pins 176 edit-carrying rows (the
  175 plus one replica row under RULED Q-L7 (a)).
  **`not_moved` is 138 at BOTH heads and so is every one of its four reasons** —
  `stays_openxfactory_adapter` **103**, `replicated_at_destination` **20**,
  `stays_openxfactory_governance` **14**, `deleted_at_carve` **1**. 103 + 14 =
  **117**, which is the set the ruling names and the box now keeps, and it is
  untouched by the twenty-six. The other twenty-one `not_moved` rows are not a
  kept set: a `replicated_at_destination` row arrives somewhere and a
  `deleted_at_carve` row arrives nowhere.
  *(CORRECTED at Copilot review round 6 on this amendment's own pull request,
  which was right that `160 / 158 / 138` reproduces at neither head. The figure
  was a transcription that predates the slice annotations, and the paragraph
  claimed a re-read at `cb2d3a2c` it had not taken for this line — exactly the
  defect this amendment corrects elsewhere, found in its own text. The kept-set
  conclusion never depended on the moving half, which is why the error survived
  three rounds: 117 is read from the `not_moved` reasons, and those are identical
  at both heads.)*

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
  deprecation window is where this matters, and measuring it is what finally
  RECONCILES five with six rather than leaving them as a disagreement.** The
  window is `contracts/manifest.yaml`'s, and that file registers RELEASE
  CONTRACTS: `contract-v3.7` marked **five** rows `relocating:` and
  `contract-v4.0` removed them as BREAKING, which the file states about itself —
  *"this file's five `relocating.at:` values"* (:1778). **`ideation-workbench`
  was never in that file at all**: `grep -c ideation-workbench contracts/manifest.yaml`
  → **0**, `contracts/CHANGELOG.md` → **0**, and `git log -S ideation-workbench --
  contracts/manifest.yaml` returns NO commit, so it was never registered and never
  de-registered. Its schema `contracts/schemas/ideation-workbench.schema.yaml` is
  present at `b075fd91` and absent at `cc4ae9d3` on its CARVE-MANIFEST row alone.
  **The two numbers therefore count two populations and both are right**: FIVE is
  the release contracts inside the deprecation window, which is what RULING R-2's
  parenthetical and § 5.6a defect (a) are about; SIX is the schemas the carve
  manifest moves, which is what this box is about. A sixth `relocating:` marker
  was never owed for a file that was never a registered contract, so none is
  missing — and the window covers everything it is required to cover.
  `#656` records: CLAIM `5690461589`; RULED R-2 `5690428146`; the discharging
  act #940 → `cc4ae9d3`.
- [x] 5.3 `[oxF]` **AUTHOR `.github/workflows/openxdox-consumer-gate.yml` in
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
  `signed-execution-chain-gate`, and `git log --all --diff-filter=A --
  '.github/workflows/*dashboard*' '.github/workflows/*ideation*'` returns
  nothing over either pattern — no such file was ever added.
  *(BOTH PATTERNS SCOPED, corrected at Copilot review round 5 on this
  amendment's own pull request: this first ran the second pattern as a bare
  `*ideation*`, which is repository-wide rather than workflow-scoped and matches
  **276** commits that have nothing to do with `.github/`. The finding was right
  about the command and the command was doing no work; re-run scoped, both
  patterns return **0** adds, which is the same answer honestly derived.)*
  *(AND THE INSTRUMENT ITSELF IS REPLACED, amendment #5, registered on
  amendment #4's pull request at comment `5702227094` item 8 — a Copilot
  finding that was right about the METHOD while the conclusion survived it.
  `--diff-filter=A` cannot carry *"never carried a dashboard-named
  workflow"*, because a rename reports as `R` and not as `A`, so a file added
  under a dashboard name and later renamed would be invisible to it.
  **`--no-renames` is the option that closes it**: it decomposes every rename
  into a delete plus an add, so both the old and the new path appear in the
  log. **Quoted here exactly as it was RUN, pipeline included** — because
  `--name-only` under `--pretty=format:` prints one line per (COMMIT, PATH)
  PAIR and not one line per path, so the raw output runs many times the size
  of the distinct set, and the pipeline is what turns the one into the other:
  `git log --all --full-history --no-renames --pretty=format:
  --name-only -- .github/workflows/ | sed '/^$/d' | sort -u`. It returns
  **16 distinct paths ever**, listed here as BARE STEMS where the command
  itself emits full paths (`.github/workflows/clearing-dispatch-gate.yml`
  and so on, directory prefix and `.yml` included), the prefix being the same
  sixteen times and carrying nothing: `clearing-dispatch-gate`,
  `doc-health-reusable`, `former-id-arrival-gate`, `lane-line`,
  `merge-master-approval`, `openreposhape-pin-gate`, `openspec-cli-pin-gate`,
  `openxdox-consumer-gate`, `openxwallet-consumer-gate`,
  `proof-1-6a-codexfactory-app-install`, `pytest-suite`, `release-tag-gate`,
  `review-lane-repin`, `session-open-pr`, `signed-execution-chain-gate`,
  `wallet-validation` — and **not one of the sixteen matches
  `dashboard|ideation`**.
  *(THREE INSTRUMENT CHOICES, each measured rather than assumed, after a
  Copilot finding on this amendment's own pull request (round 1) that the
  command as first quoted was not reproducible. **`sort -u` is part of the
  query and is now inside it.** The RAW line count is deliberately NOT quoted
  as a figure: it is one line per (commit, path) pair over EVERY ref the
  running clone has fetched — 347 of them here — so it moves with other
  lanes' branches and with the clone, never with this repository's content.
  It read **177** when this note was first written and **179** on a later
  reading, while `main` took NO commit to that directory in between (`git log
  cbc3a2c6..origin/main -- .github/workflows/` is empty) — the two lines came
  in on sibling branches this clone had fetched. The DISTINCT set read **16**
  both times. That is why the distinct set is the figure this box rests on, and
  the raw one is described rather than counted.
  **`--all` is DELIBERATE and makes the claim STRONGER than the box needs**:
  it asks what any ref has ever held, not what one history holds. The
  base-scoped form `git log cbc3a2c6 --full-history --no-renames
  --pretty=format: --name-only -- .github/workflows/ | sed '/^$/d' | sort -u`
  returns **15**, and the ONE path that drops is
  `proof-1-6a-codexfactory-app-install.yml` — already named below as gone —
  with `dashboard|ideation` matching **0 either way**. **`--full-history` was
  added on that finding and changes nothing**: 16 with it and 16 without,
  because history simplification drops only commits whose change did not
  survive a merge, and every add in this directory did. The finding was right
  about the QUOTATION and the answer is unmoved by every variant of the
  instrument.)*
  Independently — and **with rename detection EXPLICITLY ON, because
  `--diff-filter=R` does not enable it by itself and an empty `R` set from a
  plain `git log` proves nothing** — `git log --all --full-history
  --find-renames --diff-filter=R -- .github/workflows/` returns **nothing at
  all**, and so do `-M` and `-M50%`; no rename has ever touched that
  directory, which is precisely why the weaker query happened to be
  complete. *(The flag was added at Copilot round 5 on this amendment's own
  pull request, which was right that the check was non-deterministic as
  written. The answer does not move under any of the three thresholds, and
  the same query over all of `.github/` finds no rename either.)*
  The sixteen exceed the thirteen counted at `main` `cb2d3a2c`
  above because that count is FILES PRESENT at one tree and this one is PATHS
  EVER across all refs — `openxdox-consumer-gate` and `wallet-validation`
  landed after it, and `proof-1-6a-codexfactory-app-install` no longer
  exists.)*
  The SHAPE, the pinned-tools reading and the job-id obligation
  are unchanged; only the act is. **This box does NOT tick with amendment #4**:
  the workflow is its own declared act under its own claim, and that act is
  `opensoft/openxFactory` **#1059** — *Wire the pinned openDox/openXdox
  tools into a consumer gate of their own (task 5.3, RULING R-4)*, opened
  2026-09-16T01:24:55Z against `main`. This box ticks on THAT pull request's
  merge and on the new gate reporting, not on amendment #4's.
  **#1059 MERGED WHILE THIS AMENDMENT WAS OPEN — `7ab3dd80`,
  2026-09-16T16:27:36Z**, and both halves of that condition are now met:
  `.github/workflows/openxdox-consumer-gate.yml` stands at `main` with `name:`
  and job id the single token `openxdox-consumer-gate`, and the gate HAS
  REPORTED — it is a required check on **amendment #4's own pull request,
  `opensoft/openxFactory` #1058**, SUCCESS at `d1314f4d` (run `35134189330`).
  *(This read "this very pull request" while #1058 was the only pull request
  carrying the box. In amendment #5's copy that would name #1078 and
  mis-attribute a run that never happened there — a Copilot finding on this
  amendment's own pull request, round 6, and the last of amendment #4's
  self-references to be bound to its own act.)*
  **THE TICK IS THEREFORE OWED, AND AMENDMENT
  #4 DOES NOT TAKE IT.** This box's own sentence earlier in this paragraph —
  *"This box ticks on THAT pull request's merge and on the new gate
  reporting"* — says it ticks on that pull request and not on amendment #4's;
  amendment #4's CLAIM (`5690461589`)
  and RULED R-4 reach the PREMISE only; and its ledger is declared 47/23/1 in
  the claim, the description and the squash body alike. The tick belongs to the
  act that records #1059's discharge — with this box's required-check WIRING,
  which was STILL OWED WHEN AMENDMENT #4 WROTE THIS (2026-09-16, before
  16:33:22Z) and is a human act on a human-only surface. *(Scoped to its own
  moment by amendment #5 — a fourth present-tense self-reference of #4's, and
  the one that mattered most, because the record below closes exactly this
  obligation and the packet cannot carry two present-tense answers to one
  question. A Copilot finding on **#1078**, amendment #5's own pull request,
  round 2 — bound to a NUMBER because the inherited sentence immediately
  below says "this amendment's own pull request, round 19", written by
  amendment #4 about **#1058**, which is where that round 19 happened.
  Amendment #5 has no round 19, and two neighbouring sentences using one
  phrase for two different pull requests is a trap for the next reader.)*
  *(A Copilot finding on this amendment's own pull request, round 19. What it
  caught is a fact that went stale between one commit and the next, not a
  reading: the sentence said "is now open" for two hours after the merge.)*
  **AND R-4's discharge is of the OLD clause, not of the NEW file's own
  obligation** — worth separating, because the two are easy to read as one.
  What R-4 discharges is *"retaining the job id **so a ruleset-pinned token
  survives a file rename**"*: there is no rename here and no token to carry
  across one, and `pytest-suite` — whose workflow name, job id and required check
  are the single token `pytest-suite` — is untouched by #1059, so nothing this
  repository already reports under moves. The NEW gate still owes a stable token
  of its own, and #1059 carries it: job id **`openxdox-consumer-gate`**, no job
  display name, on the `openxwallet-consumer-gate` lesson that *"a distinct job
  display name silently de-advises the gate"*. It WAS ADVISORY ON THE DAY IT
  LANDED — a check is not selectable in a ruleset until a workflow has reported
  under it once, and making it required is a human act on a human-only surface —
  so amendment #4 named the required-check WIRING as owed there rather than
  claiming it here. **That sentence is amendment #4's SNAPSHOT of 2026-09-16
  before 16:33:22Z, and it is superseded by the record immediately below**,
  which measures the wiring done. The RULE it states — a check must report
  before it can be pinned, and pinning is a human act — is unchanged and still
  true; what changed is that this gate has now been through it.)*
  **TICKED 2026-09-16 BY `tasks.md` AMENDMENT #5 (CLAIM `5704937336`, POSTED
  2026-09-16T21:39:02Z). THIS AMENDMENT SPANS TWO UTC DAYS, SO ITS TICKS DO
  NOT ALL CARRY ONE DATE: this one and § 8.7's differ by a day and both are
  right, because a tick is dated by the day ITS OWN evidence closed and not
  by the day the amendment opened. THIS IS THE TICK THIS BOX ITSELF DECLARED
  OWED, AND THE OBLIGATION IT NAMED AS STILL OPEN IS CLOSED TOO.**
  Amendment #4 recorded both halves of the condition as
  met and declined the tick, correctly: this box says in its own words that it
  ticks on #1059 and *"not on this one"*, and amendment #4's claim and RULED
  R-4 reach the PREMISE only. Amendment #5 is the act that records #1059's
  discharge, which is what the box names as the tick's owner. **Re-measured
  here rather than carried forward:** #1059 is MERGED as `7ab3dd80`
  (2026-09-16T16:27:36Z), its merge commit is on `main`, and
  `.github/workflows/openxdox-consumer-gate.yml` stands there with `name:` and
  job id both the single token `openxdox-consumer-gate` and no job display
  name. **And the WIRING — *"a human act on a human-only surface"* in this
  box's own closing line — was done six minutes after that merge**: ruleset
  **`23554310`**, *"openxFactory consumer-gate (require
  openxdox-consumer-gate)"*, `target: branch`, `enforcement: active`,
  `conditions.ref_name.include: ["~DEFAULT_BRANCH"]`, a single
  `required_status_checks` rule whose sole context is
  `openxdox-consumer-gate`, `created_at` **2026-09-16T16:33:22Z** (read live
  at `gh api repos/opensoft/openxFactory/rulesets`). The gate has therefore
  not only REPORTED; it is REQUIRED — it was a required check on amendment
  #4's own pull request, SUCCESS at `d1314f4d` (run `35134189330`) and at
  `cbc3a2c6`.
  **WHAT IS DISCHARGED IS THIS BOX'S OBLIGATION — THE REPOSITORY'S OWN RECORDS
  HAVE NOT CAUGHT UP, AND THAT IS SAID HERE RATHER THAN LEFT FOR A READER TO
  TRIP OVER.** #1059's shipped files still describe the gate as it stood on the
  day it landed, six minutes before the ruleset existed. Measured at this
  amendment's ORIGINAL base `cbc3a2c6`:
  `.github/workflows/openxdox-consumer-gate.yml`:48-56
  (*"THE GATE IS ADVISORY ON THE DAY IT LANDS … Nothing pins this one … It is
  owed and it is named"*);
  *(THE TREE IS NAMED BECAUSE "THIS AMENDMENT'S BASE" IS NOT ONE — it is a
  RELATIVE locator, and this branch's base MOVED: it started at `cbc3a2c6`,
  amendment #4's head, was retargeted to `main`, and took five merges forward.
  Once this lands, the phrase alone cannot tell a reader whether a coordinate
  was read at `cbc3a2c6` or at whichever `main` arrived later, so the
  stale-record claim would not be reproducible from the ledger. Raised at
  review; three of this amendment's six uses OF THAT PHRASE already named the
  tree and three did not, and all six now do — **a claim about the PHRASE and
  not about the citation list below, whose five reads are bound instead by the
  single lead-in they all sit under**. **And all six say ORIGINAL**, because after the
  retarget the amendment's base IS `main`: naming the tree made the reads
  reproducible, and naming it ORIGINAL stops the label contradicting the
  merge-forward this very note records.)*
  `tests/openxdox_consumer_gate/test_openxdox_gate_invocation.py`:8-11
  (*"ADVISORY on the day it lands — no ruleset pins its token yet"*) and
  `test_openxdox_gate_adjudicator.py`:10 (*"a gate no ruleset pins"*); and the
  *"Not yet wired into any required check"* comments at
  `contracts/openxdox-pin.yaml`:119-120 and `contracts/opendox-pin.yaml`
  :156-158. **All five were TRUE AT AUTHORING and are STALE FROM
  2026-09-16T16:33:22Z.** Their repair belongs to an act that CLAIMS those
  files and not to this packet's `tasks.md` — which is not a deferral invented
  here but the course this repository already took for the identical class:
  `split-openxwallet-repo` corrected `README.md`'s *"advisory until an operator
  marks it required"* IN PLACE, *"with its own history stated (true at
  authoring, stale from 2026-08-26)"*, from the act that owned the surface
  (`openspec/changes/archive/2026-08-28-split-openxwallet-repo/tasks.md`
  :972-974; the corrected text stands in `README.md` — cited by its SENTENCE
  and carrying NO line number, for a reason this amendment learned the
  expensive way. **That one coordinate went stale TWICE inside this single
  pull request**: it was written as one line range, moved **128 lines** when
  the `main` this branch merged landed under it, and moved **70 more** at the
  next merge forward — both by acts with nothing to do with this one, and the
  second arriving between the fix that re-pointed the number and the push
  that would have carried it. The DELTAS are recorded and the absolute
  positions deliberately are not, because a delta cannot go stale and a
  position in this file demonstrably does.
  Re-pointing it a third time would be the same mistake with fresher digits,
  which is exactly what § 1.8 argues at length and what § 1's casefold
  citation already does).
  Registered here with every coordinate measured, so that act re-derives
  nothing.
  *(A Copilot finding on this amendment's own pull request, round 1, and the
  sharpest kind: it read the tick's *"nothing is left owed"* against the
  shipped gate's own comment and found them contradicting. They did. **The
  tick stands** — the box's condition is about the ruleset and the ruleset is
  live — and the sentence that over-reached is narrowed to what was measured.)*
  *(Recorded with the ruleset's own identifiers rather than as "the wiring
  landed", because a ruleset is the one kind of evidence in this packet that
  lives outside git and cannot be read back from any tree: the id, the
  enforcement and the creation stamp are what a later reader can re-query.)*
  *(SEVEN of amendment #4's own sentences above are bound to amendment #4 by
  this one, in FOUR classes, and nothing else in them moves. **Three
  PRONOUNS**: "this amendment", "not on this one", "NOT TAKEN HERE".
  **Two STATUSES**: the wiring "is still owed", and "It is ADVISORY on the
  day it lands … named as owed there rather than claimed here". **One PULL
  REQUEST**: "a required check on this very pull request", which in this
  amendment's copy would name #1078 and attribute to it a run that happened
  on #1058. **One POSITION**: a "four lines up" cross-reference that this
  amendment's own inserted evidence falsified, now anchored to the sentence
  it means. All seven were unambiguous while #1058 was the only pull request
  carrying this box; with a second amendment below them a reader meets a
  `[x]` box that says three times it does not tick, twice that the wiring is
  open, and once that a run on another pull request happened here. Binding a
  pronoun, a date-bound status, a pull-request reference or a line offset to
  the act that wrote it is a currency fix, not a re-wording of what was
  ratified — the same line § 1's stale coordinates are repaired on and § 7.3's
  ratified sentence is left alone on. **The count is stated with its own
  history because it went stale three times inside one pull request**: it
  read "three" through Copilot rounds 2, 3 and 5, and "five" through round
  6, each time because the next round found another member of the class.)*
- [x] 5.4 `[oxF]` **FLOOR PART 2 (RULED OQ-1, RESTATED BY RULING OQ-K) — the
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
  **STATUS — THE MACHINE CHECKS FOR (a), (b) AND (c) HAVE LANDED, AND THE BOX
  STILL DOES NOT TICK.** `openxFactory` **#1080 → `4b53ea99`**, merged
  2026-09-17T14:46:30Z, brings `scripts/carve_test_mapping.py`,
  `scripts/verify-carve-test-mapping.py` and
  `tests/carve_test_mapping/test_carve_test_mapping.py`.
  **RE-DERIVED HERE RATHER THAN TRANSCRIBED FROM THE LANE'S EVIDENCE FILE** —
  run by this actor at the tree this amendment merged, which carries
  `4b53ea99` as an ancestor: `python3 scripts/verify-carve-test-mapping.py`
  returns **exit 0** and the sum the clause names —
  `source_count 4411` + `replica excess 60` + `also-replicated 0`
  + `retired term -31` = **`Σ(destinations) 4440`** — over **146** test-bearing
  rows of 456, **144** homed and **2** RULED-retired (31 `def test_`, RULED
  `5656343213`), with **3** test-bearing replicas carrying a declared
  multiplicity. The destination split is `openDox-code` **1097** ·
  `openXdox-code` **2345** · `openxFactory` **998**, the other three
  destinations zero.
  **WHY THE BOX STAYED `[ ]` UNTIL NOW: clause (d)'s LEG half was BLOCKED on the
  BUILD arc** (§ 3.5 / § 3.6). Both legs' `validate.yml` ran a NAMED FILE LIST
  under `--noconftest` with no JUnit and no triple, and both named the BUILD arc
  as the blocker in their own words; `openxFactory`'s half was already pinned.
  **§ 5.4 did not close until the BUILD arc landed** — three of four clauses
  proved is not the clause set, and this packet does not tick a box on its
  majority.
  **TICKED 2026-09-19 by `tasks.md` AMENDMENT #8. THE BLOCKER THIS BOX NAMED IS
  DISCHARGED, AND ALL FOUR CLAUSES HOLD.** The BUILD arc landed — § 3.5 on
  `openDox-code` `#25` → `aca94ecb` and § 3.6 on `#26` → `4f8ae01e`, both `[x]`
  above — and clause (d)'s three pins are now in place, **per destination and
  never as one cross-repository equality**, which is the clause's own rule:
  • **`openDox-code`** — `#29` → `373b05aa`: `MIN_SELECTED 1076`,
  `MIN_PASSED 1073`, `EXPECT_SKIPPED 3`, failures and errors zero, JUnit XML
  emitted by the required `validate` job (measured live on run `35398182026`).
  • **`openXdox-code`** — `#25` → `ab04453d`: `MIN_SELECTED 539`,
  `MIN_PASSED 533`, `EXPECT_SKIPPED 6` (run `35399041710`), over a named list of
  16 files under `--noconftest`. **`#25` also FOLDED AND CLOSED Q-A2** — the
  one-line docstring citation registered against this leg — so that residue is
  opened and closed in the same breath here, which is the only honest way to
  record a thing that never reached the page while it was open.
  • **`openxFactory`** — its own `pytest-suite.yml`, already pinned, and the
  model the clause names.
  **Verified in each leg's own workflow rather than taken from the report**:
  both files carry the pin variables above AND quote clause (d) verbatim —
  *"collection triple — SKIPPED exactly, SELECTED and PASSED as FLOORS,
  failures and errors zero. Per destination, never as one cross-repository
  equality"* — so the shape is the clause's, not an approximation of it.
  **(a), (b) and (c) were already proved** by `#1080` → `4b53ea99` and re-derived
  at this lane's own tree (exit 0, Σ 4440 over 146 test-bearing rows). **Four of
  four is the clause set, so the box closes.**
  *(A measured residue, registered and not resolved: all three of
  `openDox-code`'s report-producing commands run NAMED FILE LISTS under
  `--noconftest`, so `collect_ignore` never applies there — the ledger had this
  right — and **26 of the 61 `test_*.py` on disk are collected by no required
  command**. That does not touch clause (d), which pins what the required job
  DOES collect; it is booked because a reader could mistake the pinned triple
  for a statement about the whole tree, and it is not one.)*

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
- [x] 5.5 `[oxF]` **FLOOR PART 4 (RULED OQ-1) — the snapshot-equivalence run:**
  the new stack renders the SAME dashboard snapshot as the old, proven by matching
  snapshot digests over one corpus.
  **STATUS — THE FOURTH PART ALREADY HOLDS, AND WHAT IS OWED IS A RUNNER.**
  RULED **Q-P1..Q-P4**, `#656` comment `5728856581` (Brett Heap, 2026-09-18
  ~10:35Z, by interactive multi-choice on four questions), over the read-only
  measurement of helper actor `floor55` (`attachments/lane-opendox/floor55/
  SCOPING-floor55.md`, `brett-wip` `68cd72cb`). **The box did NOT tick at that
  ruling; IT TICKS NOW, on the runner the ruling asked for.**
  **TICKED 2026-09-18 by `tasks.md` AMENDMENT #6**: `openxFactory` **#1105 →
  `029674788c0e55dc04d03139daeae28126fa31b9`**, merged **2026-09-18T14:59:28Z**,
  *"FLOOR PART 4 (RULED OQ-1): the snapshot-equivalence runner and its suite"*
  (claim `5728621421`). **The box's own condition was a RUNNER THAT IS GATED,
  not a recorded run, and both halves are measured present**:
  `scripts/verify-snapshot-equivalence.py` and
  `tests/snapshot_equivalence/test_snapshot_equivalence.py` are the two files
  the commit adds, and `pytest-suite` runs `python3 -m pytest tests/ -q -m "not
  postgres" --junitxml=pytest-report.xml`
  (`.github/workflows/pytest-suite.yml:599`), so a suite under
  `tests/snapshot_equivalence/` is inside the gate by construction rather than
  by a wiring entry that could be dropped. **This is why Q-P1 (a) refused a
  one-shot run**: the post-split side is a pin that moves, and what now holds
  the equality is a gate that re-proves it on every pull request.
  **STATUS — ONE CLAUSE WAS OWED AS A REVIEW DEBT, NOT A RUNNER DEFECT, AND
  ITS FIRST HALF HAS NOW LANDED.** Copilot's review at the LANDED head
  `9ed3def3` (review `5249196044`) carried **four suppressed findings** that the
  holder's gate script did not surface before the landing — *a 0-unresolved-
  threads count is not evidence about a suppressed block*, which is the landing
  gate's own rule. **All four are taken by `#1110` → `313b2665`, merged
  2026-09-18T16:47:05Z**, a plain gate over the SAME TWO FILES `#1105` landed
  (`scripts/verify-snapshot-equivalence.py` and
  `tests/snapshot_equivalence/test_snapshot_equivalence.py`) and no other path.
  **FOLLOW-UP 2 HAS LANDED — recorded by AMENDMENT #8, 2026-09-19**:
  `openxFactory` **`#1115` → `4101fbe9`**, merged 2026-09-18T22:17:32Z, taking
  the eight registered hardening items. **Two residues are registered from it
  and not resolved** (`#656` comment `5736824535`): the `:608` wording, and
  `sys.pycache_prefix`. Neither moves this box, which ticked on the gated
  runner.
  **A SECOND FOLLOW-UP IS STILL OWED AND IS NOT THIS BOX'S CONDITION**: RULED
  **Q-P5 (a)** (`#656` comment `5731951297`) scoped `#1110` to those four alone,
  sending the remaining EIGHT registered items and runbook § 2.3 to a second
  act. **That act was held until `#1086` landed, and `#1086` HAS landed** —
  `049d54a9`, 2026-09-18T17:09:24Z, recorded at § 3.7 in this same amendment —
  **so the runbook-contention hold is DISCHARGED and follow-up 2 is unblocked**;
  any remaining wait belongs to its own owner's scheduling, not to that
  dependency. *(This sentence read "until `#1086` lands" while the same file
  already recorded `#1086` as merged — a forward reference contradicted by this
  amendment's own evidence two boxes away. Caught by Copilot against head
  `83a055a6`.)*
  *(This clause read "`floor55b` takes them as a follow-up act" until that act
  landed. Corrected here rather than left in the future tense — the same stale
  forward reference this amendment already had to repair once at § 6.4, where a
  list of "remaining" closures still named one that had landed. A ledger's
  forward references are the part of it that rots fastest.)*
  **The tick is not held on that**: this box asked for a gated runner and the
  gated runner is on `main`; unread review findings against landed code are an
  owed act with their own claim, and conflating the two would leave the floor's
  fourth part unticked for a reason the box never stated. *(Worth naming as a
  class: this is the SECOND time in this packet that a reviewer's body was
  posted per-push and went unread because a script looked at the wrong thing.
  The lane's own answer was to enumerate reviews by `commit_id` against a
  read-set rather than trust "I read the body at the head I pushed". The same
  remedy is available to the holder and is the reason this clause names the
  review ID rather than merely saying findings exist.)*
  **Q-P1 (a) — the act is to BUILD THE RUNNER AND GATE IT**, not to record a
  run: one `openxFactory` pull request on a plain gate carrying
  `scripts/verify-snapshot-equivalence.py` in FLOOR PART 3's idiom — named
  refusal kinds (`equivalence-pre-ref-unreachable`, `-pre-tree-unrenderable`,
  `-reach-unavailable`, `-profile-unregistered`, `-digests-differ`), `--json`,
  and the 0-pass / 2-refuse / never-1 exit contract — plus
  `tests/snapshot_equivalence/` wired into `pytest-suite`, where it NEVER skips.
  *(THE FIVE NAMED ABOVE ARE THE RULING'S PRESCRIPTION AND ARE LEFT AS RULED.
  **The landed runner carries SEVEN**, measured at `507b6233`:
  the five, plus `equivalence-unreadable` and — added by `#1110`'s watchdog —
  **`equivalence-post-stack-unrenderable`**, the symmetric counterpart to
  `-pre-tree-unrenderable` that refuses a non-terminating post-split render
  instead of hanging the required job. **A runner may carry MORE refusals than
  the ruling enumerated** — the ruling set a floor, not a closed set — so this
  is recorded as a delta rather than by editing the ruling's own words above,
  which would make the ruling appear to have said something it did not.
  Raised by Copilot against head `83a055a6`, which named ONE missing code; the
  measurement found TWO, and the larger number is the one recorded.)*
  **§ 5.5 ticks on that runner's evidence.** A one-shot recorded run was
  REJECTED because it proves only its own day, and *"evidence now, runner
  later"* was rejected as the shape that left this box unclaimed for fourteen
  days. **The reason a run is not enough is that the POST-SPLIT side is a PIN
  THAT MOVES**, so an equality proved once is not an equality held.
  **Q-P2 (a) — *"the pre-split tree"* IS THE PUBLISHED ANNOTATED TAG
  `opendox-carve-0` → `b075fd91`**, FLOOR PART 1's own `carve_commit`,
  `git archive`d into a temporary tree, with `--pre-ref` for any other pre-shed
  ref. The carve manifest's header already prescribes it and `pytest-suite`
  checks out at `fetch-depth 0`, so the tag is reachable where the gate runs. A
  committed golden digest was REJECTED — it is the scalar-in-a-ratified-document
  shape RULING OQ-K already killed — and so was a vendored pre-split copy, on the
  untracked-second-copy problem.
  **Q-P3 (a) — THE SNAPSHOT VALIDATOR IS NOT PART 4'S.** `design.md` § D6 (4)
  asks for equal DIGESTS, and `canonical_bytes` reaches no validator, so the run
  is complete without one. The three defects the carve left in it are registered
  as § 8.9 residue rows below, owed to a follow-up act with its own claim.
  **Q-P4 (a) — the run's evidence MAY say, in ONE sentence here and one in
  § 8.2's line, that § 4.4's domain profile reproduces `openxFactory`'s own
  vocabulary** (`picked` / `staged`, via `domain_profile.current()`).
  **NO BOX MOVES ON THAT SENTENCE** — it is a statement the evidence is entitled
  to make, not a second tick condition, and § 4.4 is already `[x]` on its own.
  **FLAGGED AND DELIBERATELY NOT SCOPED**: whether part 4 also covers the
  snapshot INDEX (`snapshot_registry.py`, which has its own schema). It is a
  fifth question, and the ruling declined to guess at it. **It is NOT answered
  by the runner that landed**: `scripts/verify-snapshot-equivalence.py:121-122`
  names the snapshot index *"also unmeasured and NOT claimed here"*, so it is a
  SEPARATE follow-up runner under its own ruling rather than something this
  run's first execution settles. *(This clause read "the ruling leaves it for
  the runner's first run to answer" until #1105 landed and the runner said
  otherwise in terms; corrected on a Copilot finding against head `a406915d`.)*
  CLAIM `5728621421`.
- [ ] 5.6 `[cxF]` `[oxF]` **DE-FLOOR BEFORE YOU REMOVE — Rule 7 substrate row 1,
  claimed HERE.** `openspec/specs/ideation-dashboard/` is REMOVED and two
  capability directories are ADDED by the archive, and the codexFactory
  review-authority floor is EXACT SET EQUALITY. Order: the codexFactory pull
  request FIRST (the machine block regenerated by
  `generate_specs_floor_block.py` at ONE `openxFactory` ref, with
  `SPECS_FLOOR_PATHS` moved in the SAME commit), then `openxFactory`'s five pin
  sites in ONE reviewed diff, then the removal. Never hand-edit the block or the
  snapshot.
  **STATUS — THE ORDER THIS BOX WRITES IS RULED AN EXCEPTION AND IS NOT
  PERFORMED. THE BOX DOES NOT TICK.** RULED **R-B**, `#656` comment
  `5728607038` (Brett Heap, 2026-09-18 ~10:25Z, by interactive multi-choice),
  over the read-only measurement of helper actor `defloor56`
  (`attachments/lane-opendox/defloor56/SCOPING-defloor56.md`, `brett-wip`
  `528853f2`) spot-checked by the holder at codexFactory `main` `22d44b09`.
  **THE WRITTEN ORDER AND THE MACHINERY ARE JOINTLY UNSATISFIABLE FOR A
  REMOVAL**, which is why this is an exception and not a preference:
  `scripts/merge_master/specs_floor_block.py::assert_landed_pin` REFUSES to
  write a block pinned at any `openxFactory` commit not reachable from
  `openxFactory` `main` (*"Land the change first, then regenerate at the merge
  commit"*), while `openspec/specs/repository-gate-floor/spec.md`'s scenario
  *"The ordering is unchanged"* keeps *"de-floor, advance the pin, then
  remove"* as the required order. **It has never been exercised** — no floored
  path has ever been removed — so the contradiction has never had to be faced.
  **THE COST WAS MEASURED, AND IT DECIDES.** De-floor-first REDS `openxFactory`'s
  **REQUIRED** `pytest-suite` repository-wide (uncovered = `{ideation-dashboard}`;
  the addition grace cannot cover a removal). Archive-first reds only
  codexFactory's **ADVISORY** merge-master lane, which no ruleset requires and
  which that spec's own design intends — *"the deleting PR carries the
  failure"*. **RULED ORDER**: (1) the `openxFactory` archive lands, carrying the
  removal of `ideation-dashboard` and the ADDs; (2) codexFactory regenerates the
  floor block at that merge commit (`generated_at` = the landed sha; entry_count
  62 → 64, floor total 70 → 72; dry-run diff `block-regenerated.diff`,
  seven lines); (3) `openxFactory`'s five pin sites move in ONE reviewed diff
  (`contracts/review-lane-pin.yaml`, `PINNED_CORE_COMMIT` and the caller ref in
  `.github/workflows/merge-master-approval.yml`,
  `.github/workflows/pytest-suite.yml`,
  `contracts/review-lane-floor-snapshot.yaml` with its sha256 and entry_count).
  **No REQUIRED check goes red at any step.** REJECTED: a codexFactory OpenSpec
  change first (days, and it blocks arc F behind another estate's ratification);
  certifying an unlanded head with `--default-branch` (it defeats the
  safeguard). The exception is recorded here and, with its evidence, on
  codexFactory `#232`, the floor's governing issue (comment `5728856293`).
  **R-C — the clause *"with `SPECS_FLOOR_PATHS` moved in the SAME commit"* IS
  READ AS SATISFIED BY THE REGENERATION, and no text moves.** Since codexFactory
  `#232` (2026-09-09) the constant is `_specs_floor_paths(FLOOR_DOCUMENT.
  read_text())`, computed at import from the floor document itself;
  codexFactory's `tests/merge-master/test_repository_gate_floor.py` and
  `docs/repository-gate-floor-repair-runbook.md` already say that regenerating
  the block IS moving it. **This amendment records the reading rather than
  editing the clause**, which is this packet's no-deletion style.
  **R-D — codexFactory's additions-only test is FIXED INSIDE THE DE-FLOOR PULL
  REQUEST as a test-scope correction.** `tests/merge-master/
  test_floor_addition_grace.py` asserts `removed == set()` over the LIVE
  document and was **proven RED on the dry run**; the repair declares the
  governed removal, subtracts it from the baseline and adds a negative control.
  **The test is broader than its own canon**: the spec scopes additions-only to
  the AUTOMATED regeneration, and the runbook routes removals to a governed hand
  act. CLAIM `5728856032`, with codexFactory `#232` comment `5728856293`.
  **COLLISION SEARCH, 10:14Z**: codexFactory's ten open pull requests (`#434`,
  `#477`-`#485`) touch none of the floor objects — `#485` owns the stale
  `tree-floor-probe` fixture and the de-floor must not touch it — `openxFactory`'s
  open pull requests touch none of the five pin sites, and `#656`'s 364 comments
  carry zero prior claims on § 5.6.
  **STATUS — THE GATE PRECONDITION HAS LANDED, recorded
  by `tasks.md` AMENDMENT #7, 2026-09-18.** `openxFactory` **#1103 →
  `eb1880cb`**, merged **21:30:14Z** BY MERGE COMMIT, archives
  `repromote-engineering-vocabulary` — the precondition this gate waits on.
  **PHASE 1 STILL WAITS ON THIS PACKET'S OWN ARCHIVE**, RULED **Q-D1 (a)**
  (`#656` comment `5735889836`), and **Phase 0 is the pin advance on the
  codexFactory bot pull request**.
  **PHASE 0 HAS LANDED — recorded by AMENDMENT #8, 2026-09-19, and it landed
  ITSELF.** `codexFactory` **`#491` → `b21f0100`** regenerated the openxFactory
  review-authority floor block (62 → 63 entries), merged 2026-09-18T22:50:17Z;
  the `openxFactory` repin **`#1122` → `38f826c2`** then advanced the pinned
  decision core TO `b21f0100`, merged **2026-09-19T00:53:37Z**.
  *(Corrected against the report this lane was given, which had `#1122` as OPEN
  with auto-merge armed: measured, it is MERGED and on `main` — the arming
  fired while the report was in flight. An armed auto-merge is a pull request
  that can land without anyone watching, so its state is worth reading rather
  than inferring from when it was last described.)*
  **Neither this box nor § 8.4 ticks here**: a
  precondition landing is not the act, and the ordering § 8.4 names — de-floor
  BEFORE the removal — is still ahead. *(Recorded at both boxes' shared subject
  because § 5.6 is where the order is argued and § 8.4 is where it is checked;
  a reader who meets one should not have to find the other to learn the gate is
  now unblocked at its front.)*
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

- [x] 6.1 `[oxF]` `[oXd]` **`add-nightly-dashboard-refresh`** → openXdox. Its 13
  open tasks and its 1 ADDED + 1 MODIFIED `ideation-dashboard` requirements
  re-home; the aggregation-side artifact-only worker stays in the aggregation.
  **Its SEVEN `doc-health` ADDED requirements do NOT travel and are NOT added to
  `openxFactory`** — they were authored on the dashboard's behalf and Q4 points
  that dependency one way, so they are re-authored against the ADAPTER in
  openXdox. This is the one genuine conflict RULING Q6 names and this is its
  resolution.
  **TICKED 2026-09-18 by `tasks.md` AMENDMENT #6**: `openxFactory` **#1060 →
  `e3647b6d`**, merged **2026-09-18T17:30:27Z**, *"Close add-nightly-dashboard-
  refresh as re-homed to openXdox (split-opendox § 6.1, RULING Q6)"*, with its
  destination half `openXdox-spec` **#15 → `f088b097`** already standing. Rule 6
  window 17:30:20Z → 17:30:32Z, and the measured merge time falls inside it.
  **BOTH CLAUSES OF THE § 6.4 LANDING RULE WERE EXERCISED AND BOTH HELD** — the
  first closure to meet the rule in its amended, two-clause form. **Clause 1**:
  `e3647b6d` has **two parents**, and `2026-09-16-add-nightly-dashboard-refresh`
  keeps an adding commit `a50a4e1a` dated **2026-09-16T01:28:33Z**, the day the
  directory is named for, so nothing mis-dates. **Clause 2**: the archive-date
  arm re-run on `origin/main` MERGED WITH THIS CANDIDATE — which is what this
  branch's tree now is — exits **0**, *"every archived directory is named for
  the UTC date of the commit that added it, or is dispositioned in place"*, so
  the stacked-history trap that produced INCIDENT 2 is measured absent rather
  than assumed absent. **That is the rule's first clean pass end to end.**
  **ONE ITEM REGISTERED FOR THE SUCCESSOR, AND IT IS NOT RESIDUE**: the
  self-gate `_REHOMED_AND_STILL_WHOLE` **cannot carry a row for a PARTIAL
  carriage** — this closure re-authored the proposal at the destination while
  the `doc-health` delta deliberately did NOT travel, and the gate's row shape
  admits only whole carriage. **A partial-carriage pin is owed to the
  successor** (`rehome-lander`'s measurement, `#1060` comment `5733632291`). It
  is booked at this box rather than in § 8.9 because it is a property of THIS
  closure's shape, and because § 6.1's own text is where the next partial
  carriage will be read from — the seven `doc-health` requirements not
  travelling is the very thing this box already calls *"the one genuine
  conflict RULING Q6 names"*.
- [x] 6.2 `[oxF]` `[oD]` **`retire-doxbench-chat-turn-v1` — THE ONE THAT CANNOT
  SIMPLY CLOSE.** Its schema removal is already realized in `openxFactory` bytes
  and `contract-v3.0` is published, so its remaining 7 tasks are `openxFactory`
  bookkeeping that completes HERE and it archives HERE on its own evidence.
  Only its FORWARD half — the surviving `-v2` family's requirements — re-homes to
  openDox. **Sequenced BEFORE § 8.**
  **TICKED 2026-09-18 by `tasks.md` AMENDMENT #7**: `openxFactory` **#1066 →
  `3bf63b8e`**, merged **2026-09-18T20:24:53Z**, *"Close § 6.2:
  retire-doxbench-chat-turn-v1 archives on its own evidence, and ITS delta
  promotes"*. **This box is the one that could not simply close, and it closed
  in the two halves it always named**: it archives HERE on its own evidence, and
  its FORWARD half promotes into `openspec/specs/ideation-dashboard/spec.md`.
  **THE LANDING RULE HELD ON BOTH CLAUSES, AND NO DISPOSITION IS OWED.**
  `3bf63b8e` has two parents; the archive directory
  `2026-09-16-retire-doxbench-chat-turn-v1` carries an adding commit `90bf93c3`
  dated **2026-09-16T14:38:38Z** — the day it is named for — so the
  archive-date arm has nothing to fire on and **this closure owes no
  disposition row at all**, unlike INCIDENT 1's. Clause 2 re-run on
  `origin/main` merged with this branch exits **0**.
  **§ 6 IS NOW COMPLETE EXCEPT FOR ITS STANDING CONDITION**: §§ 6.1–6.5 are all
  `[x]` and all five disposition directories are under
  `openspec/changes/archive/`, read from the tree rather than from this ledger.
  Only § 6.6 remains, and it is a standing condition rather than an act.
  **ONE FINDING IS REGISTERED, NOT RESOLVED** (`4050274179`): a Copilot
  qualification against the closure, carried as the follow-up's scope under the
  land-and-register pattern this packet has now used four times — `#1105`→`#1110`,
  `#1086`, `openDox-code #25`, and here.
  *(A release figure inside that closure is worth preserving as a measurement,
  because it is this packet's own defect class caught in someone else's prose
  and then in its own: the published run from the deprecation to the removal is
  **twenty** releases, counted BY TAG, after an earlier count wrongly included
  **`contract-v2.6`** — which the versioning policy rules *"permanently
  unreleased"*. Verified independently here: `git tag -l 'contract-v2.*'`
  returns `v2.0` through `v2.5` and **no `v2.6`**, so the bundle is absent from
  the tag space rather than merely unpublished. A count taken from intent
  rather than from the tag would have been wrong by one.)*
- [x] 6.3 `[oxF]` `[oD]` **`add-doxchat-model-intake`** → openDox. Built but
  unarchived; its code moves with the carve as `moved_with_declared_edit` rows,
  its four ADDED requirements are re-authored in openDox, and its one additive
  schema enum member is already `openxFactory` contract bytes and STAYS.
  **TICKED 2026-09-18 by `tasks.md` AMENDMENT #6**: `openxFactory` **#1057 →
  `4ccab7b9`**, MERGED **2026-09-18T13:31:51Z**, *"Close add-doxchat-model-intake
  as re-homed to openDox (split-opendox § 6.3, RULING Q6)"*. The closure is
  archived at `openspec/changes/archive/2026-09-16-add-doxchat-model-intake`.
  The Rule 6 landing window recorded for it is 13:31:44Z → 13:32:00Z, and the
  measured merge time falls INSIDE it, which is the check worth making on a
  window rather than reading it back.
  **This is the FIRST archive closure to land under the `--merge`-not-squash
  rule § 6.4 wrote into this ledger yesterday, and the rule held FOR THIS
  CLOSURE'S OWN DIRECTORY — but the same merge had a consequence elsewhere,
  recorded as INCIDENT 2 below, and this sentence is written narrowly on
  purpose.** Measured
  rather than assumed: `4ccab7b9` has **two parents**, which is what a merge
  produces and a squash cannot, and the archive directory's adding commit
  `cb147a71` is dated **2026-09-16T01:18:08Z** — the SAME day the directory is
  named for — so `archive-date-vs-commit` has nothing to fire on *for this
  directory*. The contrast
  is the proof: #1056, squashed two days earlier under the same naming
  convention, put a **2026-09-18** adding commit under a `2026-09-16`
  directory, reddened `main`, and cost a disposition row (#1106 → `bbd1cca8`)
  to clear. Same convention, same week, two landing forms, two outcomes —
  which is as close to a controlled comparison as this ledger gets, and it is
  recorded here so the rule is carried by evidence rather than by assertion.
  **INCIDENT 2, REGISTERED 2026-09-18 — THE SAME MERGE RETRO-CHANGED ANOTHER
  DIRECTORY'S ADDING COMMIT AND MADE A CORRECT DISPOSITION ROW STALE.**
  #1057's branch was stacked on #1056's PRE-SQUASH tip, so landing it by merge
  commit carried #1056's ORIGINAL archive commit **`d8ff2ec2`** (2026-09-16)
  into `main`'s history. The checker now reads `d8ff2ec2`, not the squash
  `3e32d987` (2026-09-18), as `2026-09-16-add-composed-view-authoring`'s adding
  commit; the directory name AGREES with it; and #1106's disposition row —
  correct when it landed — is reported **STALE: … remove the entry**. `main`
  went red again at `4ccab7b9`.
  **Measured here rather than taken on report**: `d8ff2ec2` is NOT an ancestor
  of `bbd1cca8` (#1106's merge, 13:28Z) but IS an ancestor of `origin/main`
  after `4ccab7b9` (13:32Z); it reaches `main` through #1057's **SECOND
  parent** and **not** along the first-parent line; and it adds that directory
  at **2026-09-16T01:01:38Z**. The row was correct for about four minutes and
  then became wrong with no edit to it and none to the directory.
  **What this teaches is NOT "the squash was fine after all".** A disposition
  row is not a statement about a directory; it is a statement about **WHICH
  COMMITS ARE REACHABLE FROM `main`**, so any landing that changes reachability
  can invalidate a row that is already landed and already correct. Squash caused
  INCIDENT 1 by MIS-DATING; merge caused INCIDENT 2 by RE-PARENTING.
  **So the § 6.4 rule GAINS A SECOND CLAUSE rather than being withdrawn: land
  stacked archive closures by merge commit, AND, before opening the window,
  re-run the archive-date arm on `origin/main` MERGED WITH THE CANDIDATE** —
  not on the candidate alone, which is what every run in both incidents
  actually measured. The two clauses answer the two incidents **one each**:
  clause one is what INCIDENT 1 needed and would not have caught INCIDENT 2,
  clause two is what INCIDENT 2 needed and could not have caught INCIDENT 1
  (the squash commit does not exist until the landing happens). Neither clause
  alone covers both, which is precisely why the rule now carries both.
  **THE REPAIR HAS LANDED: `#1109` → `dc242f3aa5cc02ab19cebc3bbdffae0dce88207a`,
  merged 2026-09-18T14:26:58Z**, retiring the disposition row that INCIDENT 2 made
  stale. **Verified at this branch's own merged tree rather than taken on
  report**: `validate-sequenced-after.py` exits **0** with *"archive-date-vs-commit
  agreement passed (every archived directory is named for the UTC date of the
  commit that added it, or is dispositioned in place; 13 disposition(s) in
  force)"*, and the retired key is genuinely absent — the four remaining
  mentions of `add-composed-view-authoring` in
  `tests/sequenced_after/archive-date-dispositions.yaml` are all COMMENTS
  recording why it was retired, with **13 live keys and none of them that one**.
  The corpus reconciles at **172 archived directories, 13 dispositioned, 159
  agreeing outright**.
  *(Worth naming: the repair for INCIDENT 2 was to REMOVE a row, where the
  repair for INCIDENT 1 was to ADD one — the same file, opposite directions,
  **about an hour apart on the SAME DAY** — `#1106` merged 13:28:21Z and
  `#1109` 14:26:58Z, both 2026-09-18 — because the underlying fact moved rather
  than the record
  being wrong either time. That is the clearest statement of residue (vi): a
  disposition is only as stable as `main`'s reachable history, so a checker
  that reads it as permanent will keep producing this pair of incidents.)*
  This box's tick is unaffected throughout, because § 6.3 is about
  `add-doxchat-model-intake` being closed and re-homed, which it is.
- [x] 6.4 `[oxF]` `[oD]` **`add-composed-view-authoring`** → openDox. One MODIFIED
  requirement, `target_release: none`, no contract bytes — the cheapest of the
  five.
  **THE DESTINATION HALF HAS LANDED AND THE BOX STILL DOES NOT TICK**
  (recorded by `tasks.md` amendment #5, 2026-09-16). **`opensoft/openDox-spec`
  #12 MERGED — `edeed08c`, 2026-09-16T17:37:41Z**: `add-composed-view-authoring`
  now stands at `openspec/changes/add-composed-view-authoring/` in the
  receiving repository, and the carry is BYTE-IDENTICAL — verified by this
  amendment at both ends rather than quoted from #12: the delta reads **3,557
  bytes** with digest
  **`1754e5d3f9803ea80b4e8a177fda8359a96d6c4b1024fce69893ee3cb3d716e1`** at
  openxFactory `cb2d3a2c` and at openDox-spec `main` alike. That is the
  *"destination named in the receiving repository"* half of § 8.5's gate.
  **The CLOSING half is `opensoft/openxFactory` #1056**, *"Close
  `add-composed-view-authoring` as re-homed to openDox (split-opendox § 6.4,
  RULING Q6)"*, open against `main` and Rule-6 sequenced. A § 6 disposition
  is TWO acts and it is the CLOSURE that discharges the box, so this ticks on
  #1056's merge and not on its receiving half — the same ordering discipline
  § 5.3 applies to #1059.
  *(Worth the sentence because only one half has landed: a reader who finds
  the change standing in openDox-spec and the box unticked here has every
  reason to read the box as stale, and it is not.)*
  **TICKED 2026-09-18 BY `tasks.md` AMENDMENT #6 ON THE CLOSURE, WHICH IS THE
  HALF THIS BOX NAMED AS ITS OWNER.** `opensoft/openxFactory` **#1056 →
  `3e32d9874b5c68e90b0cef62cd94f9e378831fa3`**, merged **2026-09-18T10:50:06Z**
  (Rule 6 window 10:50:00Z → 10:50:12Z), closing `add-composed-view-authoring`
  as RE-HOMED to openDox under RULING **Q6**. **BOTH HALVES ARE NOW ON THE
  RECORD AND THE ORDER HELD**: the destination half landed first
  (`openDox-spec` **#12 → `edeed08c`**, 2026-09-16T17:37:41Z, byte-identity
  re-verified at both ends by amendment #5), and the box ticked only on the
  closure — *"a § 6 disposition is TWO acts and it is the CLOSURE that
  discharges the box"*, which is the same ordering discipline § 5.3 applied to
  `#1059` and the reason this box sat `[ ]` for two days with its destination
  already standing in the receiving repository. **`#1057` (§ 6.3) HAS NOW
  LANDED — `4ccab7b9`, 2026-09-18T13:31:51Z — and § 6.3 is ticked on it above.**
  *(This sentence read "is retargeted to `main` and follows" until that landing;
  corrected in place rather than left to age, on a Copilot finding against the
  head `fe9e5e6f`, which is the class of defect this packet polices and is worth
  crediting when a reviewer catches it in our own text.)*
  **INCIDENT, REGISTERED — THE CLOSURE WAS LANDED BY SQUASH, AND THE LANDING
  FORM IS THE DEFECT.** `#1056` was merged with a SQUASH, so the archive
  directory `openspec/changes/archive/2026-09-16-add-composed-view-authoring`
  — named for the day the change was ARCHIVED — has an adding commit dated
  **2026-09-18**, and `openxFactory` `main` goes RED on
  `validate-sequenced-after`'s `archive-date-vs-commit` arm (main run
  **`35336659842`** at `3e32d987`). **Measured here rather than taken on
  report**: `3e32d987` has exactly ONE parent (`4ee21c40`), which is what a
  squash produces and a merge does not; the check re-run at `origin/main` in a
  clean worktree reproduces the single finding *"dated 2026-09-16, added
  2026-09-18 by `3e32d9874b5c68e90b0cef62cd94f9e378831fa3` — undispositioned"*.
  **THE ARCHIVE ITSELF IS CORRECT AND THIS BOX'S TICK STANDS**: the closure
  happened, the directory is where it belongs, and what is wrong is the
  ADDING DATE the squash stamped on it — not the act, not the destination and
  not the evidence. Renaming the directory is forbidden (`#812`). **The repair
  is one disposition row**, a single-row pull request by actor
  `rehome-lander` citing `#812` rule 1 and rule 2a, in exactly the form `#1099`
  used the day before.
  **THE RULE THIS PACKET NOW CARRIES, BECAUSE IT IS THE SECOND OCCURRENCE IN
  TWO DAYS: ARCHIVE CLOSURES LAND BY `gh pr merge --merge`, NEVER BY SQUASH.**
  The first was lane openXfactory-5's `#1076` → `5dd0a8dc` on 2026-09-17,
  repaired by `#1099` → `ad089e8a`; this is the same failure with a
  different actor, which is the evidence that **the cause is the FORM and not
  the operator**. A squash re-dates the archive directory's adding commit to
  the landing day, so any archive whose directory is named for an earlier UTC
  day reds `main` for everyone the moment it lands. **It binds every remaining
  § 6 closure and any later archive of this packet** — `#1066`, `#1103` — and
  it is written into the ledger rather than
  left in a runbook because the ledger is what the next closure's author reads.
  *(`#1057` and `#1060` were named in this list until they landed on 2026-09-18
  and became the rule's PROOFS instead of its subjects — `#1057` at § 6.3 for
  clause 1, `#1060` at § 6.1 for BOTH clauses. It is removed
  here on a Copilot finding against head `fe9e5e6f`, which observed that a list
  of "remaining" closures naming a completed one directs the next operator to
  redo finished work. The finding was correct. **Read § 6.3's INCIDENT 2 before
  applying this rule**: landing by merge commit is necessary and NOT sufficient,
  and the second clause — re-run the archive-date arm on `origin/main` merged
  with the candidate before opening the window — is the half that `#1057`'s own
  landing proved was missing.)*
- [x] 6.5 `[oxF]` `[oD]` **`add-lens-document-selection`** → SPLIT. The
  set-builder half to openDox; its `doc_health.staging_seed` drafter and route
  STAY in `openxFactory`'s own adapter (RULING DQ-1 — no longer a `codexDox`
  question). **The only one of the five whose content does not land in one
  place.**
  **TICKED 2026-09-18 by `tasks.md` AMENDMENT #6**: `openxFactory` **#1065 →
  `81903286`**, merged **2026-09-18T17:54:08Z**, *"Close add-lens-document-
  selection as re-homed to openDox, with the intra-requirement split named"* —
  RULINGS **Q6 + DQ-1**. **The landing rule held on both clauses again**:
  `81903286` has two parents, `2026-09-16-add-lens-document-selection` keeps an
  adding commit `49ec794d` dated **2026-09-16T13:29:40Z**, and the archive-date
  arm re-run on `origin/main` merged with this candidate exits **0**.
  **The SPLIT is what makes this box the awkward one, and the closure names it
  rather than eliding it**: the set-builder half re-homes while the
  `doc_health.staging_seed` drafter and route STAY in `openxFactory`'s own
  adapter, so the requirement is divided WITHIN itself. That is why the closure
  title carries *"with the intra-requirement split named"* — a re-home that
  moved the whole requirement would have been the easier record and the false
  one.
- [ ] 6.6 `[oxF]` **No new dashboard change opens in `openxFactory`** (RULING Q6),
  from this packet's ratification forward.
  **STATUS — RECORDED BY `tasks.md` AMENDMENT #7, AND DELIBERATELY NOT CLAIMED
  AS PROVEN.** This is a STANDING condition over a WINDOW, not a fact about a
  tree, so no single run can discharge it and this box will tick on a judgement
  at the packet's end rather than on a measurement.
  **What IS measurable at `507b6233`, recorded so the ticking act starts from a
  number rather than an impression**: 45 active changes, of which **16 mention
  `ideation-dashboard`** — and that figure is an UPPER BOUND on nothing useful,
  because a mention is not an opening and most of the 16 predate this packet.
  *(Stated plainly because the tempting move is to grep for mentions and call
  the result compliance. It would be evidence claimed as proof it cannot give:
  the condition names changes OPENED AFTER ratification, and the grep cannot
  see when a change opened. The ticking act needs the opening dates, not the
  mention count.)*

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
  **The test the requirement states, and what the five registered domain trees
  actually hold** — codexFactory first, because it is the one R-3 reasoned from,
  then all five. The promoted requirement *A descendant is created on its first profile, not before*
  (the **PROMOTED** `openspec/specs/domain-descendant-boundary/spec.md`:128-137
  — this packet's own MODIFIED delta carries the same requirement at
  `openspec/changes/split-opendox-two-layer-product/specs/domain-descendant-boundary/spec.md`:75-102,
  which is why two different line ranges for one requirement appear in this box;
  both are cited by path, and neither is stale) keys on **an
  artifact of the product's PROFILE KIND**, not on the word "dashboard". For a
  `<Domainx>Dox` the profile kind is what § 7.3 names — ONE domain-mapping
  declaration, five axes, per `domain-mapping-declaration` — and, under this
  packet's own MODIFIED delta (`proposal.md`:298-299, `design.md`:741, NOT yet
  promoted, since this packet archives later), a committed TENANT INSTALL.
  **Censused BY CONTENT, not by filename**, at codexFactory `main`
  **`761f49d0`**, 1,995 tracked files — because the requirement names an artifact
  KIND, and a declaration need not carry the word in its path: **ZERO files
  declare `kind: domain-profile`**, which is the literal the one real instance
  carries (`openxFactory` `contracts/domain-profiles/openxfactory-engineering.yaml`:61,
  `schema_version: 1` / `kind: domain-profile`). The `kind:` literals codexFactory
  DOES declare under `contracts/`, `profiles/`, `schemas/` and `tenants/` are
  `policy_allowance_registry` (5), `policy_allowance` (2), `veto_class_vocabulary`,
  `policy_allowance_revocation`, the three `intent_compliance_*`,
  `codex_deployment_profile` and `artifact_kind` — and `codex_tenant` (**3**, all
  under `tenants/`): **ten distinct literals over seventeen declarations, and not
  one of them is `domain-profile`.** **No `kind:` anywhere in the tree names dox**
  (`git grep -iE '^[[:space:]]*kind:.*dox'` → empty).
  **AND THE LITERAL IS NOT LEFT AS THE ONLY DISCRIMINATOR**, because it cannot
  be: the requirement keys on an artifact KIND, and this packet's own
  `domain-mapping-declaration` defines that kind STRUCTURALLY — *"The declaration
  SHALL cover exactly five axes: the domain's ARTIFACT KINDS; the LIFECYCLE
  VOCABULARY each kind travels …; the ACTS and the GATE each act passes; the
  EVIDENCE CLASSES a derived statement must cite; and the PROMOTING
  AUTHORITIES"* (`specs/domain-mapping-declaration/spec.md`:31-42). A file could
  carry that structure under any `kind:` word it liked, so the census was taken
  a THIRD way, over the AXES themselves, using the top-level keys the one real
  instance spells them with (`artifact_kinds:`, `lifecycle:`, `gates:`, `acts:`,
  `evidence_classes:`, `authorities:` at
  `contracts/domain-profiles/openxfactory-engineering.yaml`:80, :147, :361, :371,
  :396, :406). Across all 1,995 tracked files: `artifact_kinds:` **0**,
  `lifecycle:` **0**, `acts:` **0**, `evidence_classes:` **0**, `authorities:`
  **0**, `gates:` **2**. **No file reaches two of the five axes**, and the two
  that reach ONE are
  `hermes/domain/review-councils/templates/operator-exercise-gates.template.yaml`
  and its own test fixture under `tests/merge-master/` — the autonomous-merge
  operator-attestation template, which is a gate roster for a merge axis and not
  a domain's mapping. Broadened to any indentation and to hyphenated spellings,
  `artifact[_-]kinds`, `evidence[_-]classes`, `promoting[_-]authorit`,
  `lifecycle[_-]vocabular` and the declaration's own identity fields
  `mapping[_-]id` and `domain[_-]label` return **zero files each**. **So the
  answer does not rest on one `kind:` string**: by the literal, by the ten
  `kind:` words actually declared, and by the five-axis STRUCTURE independent of
  any naming, codexFactory holds no profile artifact.
  **AND THE CENSUS IS NOT codexFactory's ALONE, because the answer this box
  gives is GLOBAL** — *no domain gets the first descendant yet*, not *not this
  one*. Each of § 1.7's FIVE registered domain trees was censused the same three
  CONTENT ways at its own `main` — and then a FOURTH way, the MODIFIED delta's
  TENANT INSTALL, which no content probe reaches and which is censused for all
  five below this table:

  | domain tree | head | tracked | `kind: domain-profile` | `kind:` naming dox | `mapping_id:`/`domain_label:` | most of the five AXES in any ONE file |
  | --- | --- | ---: | ---: | ---: | ---: | ---: |
  | `codeXfactory/codexFactory` | `761f49d0` | 1,995 | 0 | 0 | 0 | **1** |
  | `MedxSoft/MedxFactory` | `9f125a6a` | 8,562 | 0 | 0 | 0 | **1** |
  | `ledgerXfactory/LedgerxFactory` | `090d1f50` | 1,245 | 0 | 0 | 0 | **1** |
  | `opensoft/AdxFactory` | `e794dc2f` | 85 | 0 | 0 | 0 | **1** |
  | `opensoft/OpsxFactory` | `6aa1512c` | 2,164 | 0 | 0 | 0 | **1** |

  **14,051 tracked files across the five: not one declares `kind:
  domain-profile`, no `kind:` anywhere names dox, `mapping_id:` and
  `domain_label:` do not occur at all, and NO SINGLE FILE reaches two of the five
  axes.** `artifact_kinds:`, `evidence_classes:` and `authorities:` are absent
  from every one of the five trees; the axis words that do occur are `gates:`
  (codexFactory 2, MedxFactory 52, LedgerxFactory 15, AdxFactory 8),
  `lifecycle:` (LedgerxFactory 7, OpsxFactory 1) and `acts:` (LedgerxFactory 2,
  OpsxFactory 4) — each ALONE, in templates, fixtures and archived proposals of
  those domains' own products, never two together and never beside a mapping
  identity. **So the laziness rule's answer is NONE YET for every registered
  domain**, which is the answer R-3 gives.
  *(ADDED at Copilot review round 6 on this amendment's own pull request, and it
  is the difference between a scoped claim and the global one this box makes:
  R-3 reasoned from codexFactory — the domain most likely to be first — while
  §§ 7.1/7.2 tick a conclusion about all five. § 7.2's REPORT proves zero
  descendant REPOSITORIES exist anywhere in the estate; this table proves zero
  PROFILE ARTIFACTS exist in any registered domain to trigger one.)*
  **AND A FOURTH WAY, BECAUSE THE THREE ABOVE ALL MEASURE CONTENT AND THIS
  PACKET'S OWN MODIFIED DELTA ADDS A PREDICATE NO CONTENT PROBE REACHES: A
  COMMITTED TENANT INSTALL.** The MODIFIED requirement's fourth scenario reads
  *"WHEN a DomainxFactory install stands up an instance of a runtime neutral
  product for a tenant THEN the tenant's instance declaration IS the domain's
  first profile artifact"*
  (`specs/domain-descendant-boundary/spec.md`:115-118). That is a RECORD, not a
  `kind:` literal and not an axis word, so it was censused separately in each of
  the five trees over one population defined the same way in every one: every
  tracked file under a `tenants/`, `clients/`, `installs/` or `deployments/`
  directory, UNION every file whose top-level `kind:` names a tenant, client,
  install or deployment. **BOTH HALVES OF THAT UNION ARE WRITTEN OUT, AND IN
  POSIX CHARACTER CLASSES, BECAUSE A PASTEABLE COMMAND IS THE WHOLE POINT OF
  QUOTING ONE.** The directory half is `git ls-files | grep -iE
  '(^|/)(tenants?|clients?|installs?|deployments?)/'`; the `kind:` half is
  `git grep -ilE "^[[:space:]]*kind:[[:space:]]*[\"']?[a-z_]*(tenant|client|install|deployment)" -- '*.yaml' '*.yml'`
  — DOUBLE-quoted, because the pattern contains a single quote and a
  single-quoted shell string cannot hold one — and the two are `sort -u`'d
  together, which is the population. The `kind:` half was RUN with GNU `\s` where
  `[[:space:]]` stands here, and the two forms return the **byte-identical file
  list in all five trees** (measured, md5-equal, not assumed), so no count in this
  box moves — but `\s` is a GNU extension POSIX ERE does not define, and this
  packet writes its other patterns in POSIX classes for exactly that reason
  (:479-483, :494-497, both naming macOS). It is not a style point: on a BSD/macOS
  grep `\s` is a literal `s`, the `kind:` half then matches **nothing at all**
  and returns zero files WITHOUT AN ERROR, and a reader pasting the GNU form there
  would read this census as unreproducible rather than as measured.
  *(A Copilot finding on this amendment's own pull request, and the most repeated
  one of the series: the missing directory half in rounds 14, 15, 16 and 17, the
  non-POSIX escape in round 17. Fixed rather than registered because what it
  falsifies is not prose but the box's own promise that the command can be
  pasted.)*
  Each record in the population is then read for an instance of a dox product.
  **THAT PATTERN TOLERATES INDENTATION, SO IT IS WIDER THAN "top-level" AND BOTH
  POPULATIONS ARE GIVEN** (a Copilot finding on this amendment's own pull request,
  round 10). Anchored strictly at column one — `^kind:` — the five populations read
  **9 / 8 / 142 / 7 / 117** instead of 9 / 8 / 142 / 7 / 124. **Four of the five
  are identical and the seven that drop are all OpsxFactory TEST FIXTURES** under
  `tests/fixtures/business-central-administration/` (six `negative/` adjudication
  and consent cases, one `positive/`), where the `kind:` sits nested inside a
  case. **Not one of the seven mentions dox**, so the `dox` column is **8** and the
  descendant column **0** under either anchoring, and the verdict does not depend
  on the choice. The wider pattern is the one reported above because a record
  whose `kind:` is nested is still a committed record. The
  pathspec is stated because the count is sensitive to it in exactly one place
  and the verdict is not: dropping it adds ONE codexFactory file —
  `openspec/changes/add-software-team-execution-lane/supporting-docs/01-tenant-and-approved-intent.md`,
  a markdown supporting-doc quoting a `kind: codex_tenant` block — which carries
  no mention of dox, so the population reads 10 / 8 / 142 / 7 / 124 instead of
  9 / 8 / 142 / 7 / 124 and every other column is unmoved.

  | domain tree | head | tenant/client/install records | naming `dox` | declaring a `<Domainx>Dox` instance |
  | --- | --- | ---: | ---: | ---: |
  | `codeXfactory/codexFactory` | `761f49d0` | 9 | 0 | **0** |
  | `MedxSoft/MedxFactory` | `9f125a6a` | 8 | 0 | **0** |
  | `ledgerXfactory/LedgerxFactory` | `090d1f50` | 142 | 0 | **0** |
  | `opensoft/AdxFactory` | `e794dc2f` | 7 | 0 | **0** |
  | `opensoft/OpsxFactory` | `6aa1512c` | 124 | **8** | **0** |

  **290 committed tenant-install records across the five (291 without the
  pathspec), and not one of them declares an instance of a descendant.**
  `git grep -ilE
  '(codex|medx|ledgerx|adx|opsx)dox'` returns **zero files** in all five trees —
  zero FILES, not merely zero records — and so does
  `dox_(instance|database|migration)`. **The `-i` is load-bearing and is why the
  packet's own CamelCase spellings are inside the probe**, not outside it:
  `codexDox`, `MedxDox`, `LedgerxDox`, `AdxDox` and `OpsxDox` all match that
  pattern case-insensitively, and run CASE-SENSITIVELY against those five
  literals (`git grep -lE '(codexDox|MedxDox|LedgerxDox|AdxDox|OpsxDox)'`) the
  answer is the same: **zero files in all five trees**. The only `[a-z]+xdox` string anywhere in
  the five is `openxdox`, the NEUTRAL product, in codexFactory (32 files, 84
  occurrences) and OpsxFactory (14 files, 23) — `git grep -hoiE '[a-z]+xdox'`
  returns that one token and no other in either tree. *(The bare string `dox`
  is not the probe and could not be:
  MedxFactory's 158 `dox`-matching files are `doxorubicin` (174 occurrences),
  `doxycycline` (52), `doxylamine`, `doxepin`, `pralidoxime`,
  `doxercalciferol`, `doxazosin` and `cefpodoxime` — a drug vocabulary, not a
  product.)* **Eight of OpsxFactory's 124 records name dox, and all eight are
  ONE tenant (`opensoft`, the estate's own) and ONE plane**: the two REAL intake
  cases (`tenants/opensoft-dox-intent-plane-intake.yaml`,
  `tenants/opensoft-dox-dispatch-minter-intake.yaml`, both
  `kind: opsx_client_infrastructure_execution_case`), `tenants/opensoft.yaml`
  (`kind: opsx_client`) registering the subject, the two DNS discovery dumps
  carrying the `A` records `dox-opensoft-qa` and `openxdox`, and three records
  about something else that mention it in passing
  (`opensoft-hermes-runtime-refresh-intake.yaml` cites the dox intake as a
  driven-shape precedent, `opensoft-codexfactory-mcp-hosting-plan.yaml` cites
  `tests/test_dox_workload_set.py`, and
  `opensoft-keycloak-qa-broker-bringup-plan.yaml` names the `dox` namespace in a
  gateway list). **So the fourth axis answers NONE YET for every registered
  domain too** — **FOUR** of the five trees hold no dox record at all
  (codexFactory, MedxFactory, LedgerxFactory, AdxFactory) and the **FIFTH**'s
  eight are one estate-tenant plane, which is read below rather than counted.
  *(The sentence said "three … and the fourth", which left one tree
  unaccounted and contradicted the table four lines above it — a Copilot finding
  on this amendment's own pull request, round 11, and a miscount of this
  amendment's own.)*
  *(ADDED at Copilot review round 8 on this amendment's own pull request, which
  was right that the three content axes measure `kind:`/axis content and none of
  them detects a committed tenant install, while the detailed reading that
  follows covers OpsxFactory alone — so a GLOBAL answer rested on a predicate
  never censused for MedxFactory, LedgerxFactory or AdxFactory. It is censused
  for all five now.)*
  **THAT ONE NEAR MISS IS NAMED RATHER THAN LEFT FOR A LATER READER TO FIND,
  because it is the only thing in 14,051 files that can be read against this
  tick.** `OpsxFactory`'s `tenants/` carries a REAL, non-fixture, COMMITTED
  record DECLARING AN ACTIVE dox deployment:
  `tenants/opensoft-dox-intent-plane-intake.yaml`
  and `tenants/opensoft-dox-dispatch-minter-intake.yaml` (both
  `kind: opsx_client_infrastructure_execution_case`), and `tenants/opensoft.yaml`
  (`kind: opsx_client`) registering the subject `opensoft-aks-qa-dox-plane` /
  `dox-opensoft-qa.xforge.us`, display name *"Opensoft openDox Hosted Plane (AKS,
  namespace dox)"*, `lifecycle_state: active`, registered 2026-08-10. That is
  worth stopping on, because this packet's own MODIFIED delta makes **a committed
  TENANT INSTALL a profile artifact** — so a committed install sitting inside a
  registered domain tree is exactly the shape that would trigger the laziness
  rule.
  *("LIVE" WAS THIS PACKET'S OWN WORD AND IT IS WITHDRAWN, amendment #5,
  registered at comment `5702227094` item 10 — a Copilot finding that is half
  right in a way worth landing the distinction on. The QUOTATION above is
  verbatim-accurate at OpsxFactory `6aa1512c`: `tenants/opensoft.yaml` does
  carry `lifecycle_state: active` and the stable key
  `dox-opensoft-qa.xforge.us`. But `openxFactory`'s own canonical naming
  record retires the HOST — `docs/openxdox-naming.md` **Amendment 1
  (2026-08-14)**, `:84-89` at this amendment's ORIGINAL base `cbc3a2c6`:
  *"`openxdox.opensoft.dev` replaces
  `dox-opensoft-qa.xforge.us` … the legacy names are cut dead at switchover
  — no dual-host period and no redirect"*. **So the RECORD is active and the
  HOST is retired**, and the word "LIVE" was this packet's characterisation
  rather than anything the record claims. The census VERDICT is invariant
  either way, which is why this is a wording repair and not a re-measurement:
  the predicate § 7.1 turns on is a `<Domainx>Dox` DESCENDANT instance and
  never liveness — an install of the NEUTRAL product openDox for the estate's
  own tenant is not a descendant whether its host answers or not. **That
  OpsxFactory's record is stale against `openxdox-naming` Amendment 1 is a
  finding about OpsxFactory's tree**, raised there rather than repaired from
  here: a neutral packet does not edit a domain factory's own ledger to keep
  its own quotation tidy.)*
  **It does not trigger it, and the reason is in the delta's own sentence.**
  `design.md`:741-743 says what that clause reconciles: *"a committed TENANT
  INSTALL is a profile artifact, which is what reconciles **Q3's commissioned
  descendants** with the standard's own laziness rule"* — the install that counts
  is an install OF A DESCENDANT, `<Domainx>Dox`. What OpsxFactory holds is an
  install of **the NEUTRAL PRODUCT openDox, for the estate's own tenant
  `opensoft`**, recorded in OpsxFactory's CLIENT-INFRASTRUCTURE intake ledger as
  the work product of the IT-operations factory that provisions infrastructure
  for everyone. Its own `kind:` literals say so —
  `opsx_client_infrastructure_execution_case` and `opsx_client`, neither of them
  an artifact of the dox product's profile kind — and the requirement's own
  second scenario settles it: *"the descendant is created AND THAT ARTIFACT
  RELOCATES INTO IT"* (PROMOTED
  `openspec/specs/domain-descendant-boundary/spec.md`:139-141; the delta's
  counterpart scenario is its :107-109). An intake case
  whose `request_ref_file` points at
  `installs/hermes-install/config/clients/opensoft/requests/` does not relocate
  into an `OpsxDox` repository; it belongs to OpsxFactory's own intake ledger.
  There is no `OpsxDox` instance, no `OpsxDox` database and no domain-mapping
  declaration anywhere in that tree.
  **THE DELTA'S OWN TWO SENTENCES POINT DIFFERENT WAYS HERE, AND THE ONE THIS
  READING RESTS ON IS NAMED RATHER THAN PICKED SILENTLY** (raised at Copilot
  review round 9 on this amendment's own pull request — the sharpest reading
  taken against this box in nine rounds). Scenario 4 read ALONE covers what
  OpsxFactory did: *"WHEN a DomainxFactory install stands up an instance of a
  runtime neutral product for a tenant"* — openDox and openXdox ARE runtime
  neutral products, `opensoft` IS a tenant, and the install IS committed.
  **The requirement's own BODY, a few lines above that scenario, says which
  instance the clause is about**: *"RULING Q3 … is that every domain install
  brings its own DESCENDANT INSTANCE and its own database inside the tenant"*,
  and then *"A domain that has committed to standing an instance up for a tenant
  therefore HAS its first profile artifact: the tenant's own instance
  declaration"* (`specs/domain-descendant-boundary/spec.md`:82-89). Scenario 2
  says it from the other side — the artifact *"RELOCATES INTO"* the descendant
  (:107-109) — and `design.md`:741-743 names what the clause was written to
  reconcile, *"Q3's commissioned descendants"*. **And this packet's `proposal.md`
  says the same thing in the line that ANNOUNCES the clause**: the requirement
  *"grows the DEPLOYMENT-UNIT clause (a committed tenant install IS a profile
  artifact, which reconciles RULING Q3 with the laziness rule the standard already
  carries)"* (`proposal.md`:297-300) — RULING Q3 being the ruling whose content is
  *one descendant instance and one database per tenant*, which is what the body
  spells out. **On the body's reading nothing
  triggers here**: those records declare no descendant instance and no
  descendant database, and nothing in them can relocate into an `OpsxDox` that
  does not exist. **On scenario 4's stand-alone reading something does**, and
  the consequence is written down rather than left implicit — § 7.1's answer
  would become *not codexFactory first but OpsxFactory*, § 7.2's report would
  have an instance to report, and § 7.3 would have a subject. **This amendment
  does not make that call.** §§ 7.1/7.2 tick on RULED **R-3**, which answered
  NONE YET on the laziness rule, and an amendment records a ruling rather than
  re-litigating its premise. What it does is (a) name the tension as a defect in
  THIS PACKET'S OWN DELTA — scenario 4 should read *an instance OF THE
  DESCENDANT* if the body means what it says, and only the act that promotes the
  delta can repair it — and (b) file the live reading where it can be decided,
  which is the next paragraph.
  **AND IT WAS DECIDED WHILE THIS AMENDMENT WAS OPEN, SO THE DISPOSITION IS CITED
  HERE RATHER THAN LEFT AS THIS BOX'S OWN READING** — **RULED 2026-09-16T16:06:59Z**,
  `#656` comment **`5700622683`** (Brett Heap, by interactive multi-choice):
  *"scenario 4 of the MODIFIED `domain-descendant-boundary` delta, read alone,
  would make OpsxFactory's committed openDox plane a 'profile artifact'; it is
  RECORDED as a defect in the packet's own delta text (it should read an instance
  OF THE DESCENDANT), to be fixed by a later spec-delta amendment; §§ 7.1/7.2 tick
  on R-3 (NONE YET) unchanged."* That is the disposition this box had already
  taken, now carrying the authority it lacked: the defect is recorded and not
  repaired here, the repair is owed from a later SPEC-DELTA amendment rather than
  from this one, and the ticks stand.
  **And the per-tenant install has its own OPEN box in this packet, which is
  where any other reading belongs**: § 7.4, `[OmI]` `[Opsx]`, still `[ ]` — *"one
  instance and one database per tenant in both cases (RULING Q3) … the `dox`
  workload set becoming per-tenant"*. If the tenant-install clause is ever read
  to cover an ops-provisioned plane for the estate's own tenant, that reading
  lands at § 7.4 and moves § 7.1's answer with it. It is not a reading this
  amendment makes, and it is written down here so the question is ASKED rather
  than rediscovered by somebody who finds `opensoft-dox-intent-plane-intake.yaml`
  after the box is ticked.
  **The mentions that DO exist in file CONTENT are named rather than hidden**,
  since a path-only census would have missed them.
  Matched case-INSENSITIVELY, `openxdox` is in **32** tracked files and `opendox`
  in **28** — **but 17 files carry both, so the union is 43 files**, not the 60
  that adding the two columns would give. The 32 `openxdox` files sit
  `openspec/changes` 14, `hermes/domain` 12 (council records and their evidence
  dumps), `specs/013-project-intake-provisioning` 3 (which excludes the openXdox
  migration from its scope in terms), `tests/merge-master` 2 and
  `scripts/merge_master/openxfactory_floor.py` 1; the 28 `opendox` files sit
  `openspec/changes` 18, `hermes/domain` 4, `tests/merge-master` 2, and one each
  in `specs/047-openxfactory-tree-floor-probe`, `scripts/merge_master`,
  `scripts/browser_ui_repair` and `README.md`. **The file that is the singleton
  of both columns is `scripts/merge_master/openxfactory_floor.py`**, which carries
  seven dox lines, of which :290–291 are `openxFactory`'s SUBMODULE GITLINK NAMES
  in a floor prober — declared as such at :275, beside `openXwallet` — and that is
  this packet's own § 5.1 / § 8.7 subject seen from codexFactory's side. The
  **four** `domain-profiles` line hits, across **three** files, and the one
  `domain-mapping-declaration` hit are all inside **path-listing fixtures and
  evidence dumps of openxFactory's own tree**
  (`tests/merge-master/fixtures/tree-floor-probe/openxFactory.tracked-paths.txt`
  twice, one of them :702 — the very
  `contracts/domain-profiles/openxfactory-engineering.yaml` named above, recorded
  there as a path string — and
  `hermes/domain/review-councils/records/*/evidence/openxfactory-*paths*.txt`) —
  another repository's filenames recorded as data, not artifacts of this one.
  **On the tenant-install half the nearest miss is named too**: codexFactory
  carries `profiles/software-team.yaml` (`kind: codex_deployment_profile`) and
  **two `kind: codex_tenant` DESCRIPTORS** — `tenants/examples/software-team.yaml`
  and the LIVE pilot `tenants/pilots/project-alfa.yaml`; the literal appears twice
  more and neither is a descriptor (`tenants/README.md`:11 shows the form, and
  `openspec/changes/add-software-team-execution-lane/supporting-docs/01-tenant-and-approved-intent.md`:55
  quotes it) — tenancy for codexFactory's OWN product, with no dox instance, no
  dox database and no `openXdox — <tenant>` App anywhere. **Zero artifacts of
  the product's profile kind — by content, by kind literal and by structure — so
  the laziness rule holds and the answer is NONE YET.**
  *(This paragraph replaced a PATH-ONLY census — `(?i)domain.mapping` 0,
  `(?i)codexdox` 0, `(?i)openxdox` 0, `(?i)opendox` 0 over path names — at
  Copilot review round 1 on this amendment's own pull request. The finding was
  right and is recorded rather than quietly fixed: those four greps read
  FILENAMES, the requirement reads ARTIFACT KIND, and the content census above
  finds 43 files mentioning the product that the path census could not see. The
  conclusion is unchanged and is now established by the evidence that would have
  overturned it. The § 7.2 REPORT carried the same path-only census and is corrected by its
  own erratum, cited there.)*
  **The clause this box carried does NOT reproduce, which is why it was
  amended rather than ticked around.** codexFactory holds **32** tracked paths
  whose name contains "dashboard", in four classes, and naming them is what makes
  the tick safe: (1) `specs/002-ideation-dashboard/` — four Speckit files
  (evidence, plan, spec, tasks); (2)
  `tests/browser-ui-repair/baselines/ideation-dashboard/brand/codexfactory-linux-chromium-v1/`
  — seventeen files, a visual-regression baseline corpus: `baseline.png` and
  four hash-named candidate PNGs, `index.json` and ten hash-named JSON
  sidecars, and one `.gitkeep`; (3)
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
  it** — `#656` comment **`5690553188`**, written against the PROMOTED
  requirement *A descendant is created on its first profile, not before*
  (the **PROMOTED** `openspec/specs/domain-descendant-boundary/spec.md`:128-145,
  not this packet's delta, whose counterpart runs :75-122) and in
  particular its scenario **An empty descendant exists** (:143-145). What the
  report finds, measured rather than asserted: the `opensoft` organization
  carries exactly SIX `*Dox*` repositories, the product's own
  (`openDox`, `openDox-spec`, `openDox-code`, `openXdox`, `openXdox-spec`,
  `openXdox-code`) and **ZERO `<Domainx>Dox` descendants**, so the :143-145
  scenario has no instance to report — which is itself the reportable fact, and
  the strongest form of "not cited as precedent for creating more" this box can
  reach. The fifteen descendant names plus one install name of § 1.7 stay
  registered with no repository behind any of them.
  **AND THE ENUMERATION IS NOT `opensoft`'s ALONE, because those fifteen names
  are not all `opensoft`'s** (raised at Copilot review round 9 on this
  amendment's own pull request, which was right that a one-org report cannot
  carry a claim about names belonging to three others). Re-enumerated LIVE
  **2026-09-16T14:37Z**, every org § 1.7's registry names:

  | org | repositories enumerated | `dox`-named |
  | --- | ---: | --- |
  | `opensoft` | 402 | **6** — `openDox`, `openDox-spec`, `openDox-code`, `openXdox`, `openXdox-spec`, `openXdox-code` |
  | `codeXfactory` | 1 | **0** |
  | `MedxSoft` | 13 | **0** |
  | `ledgerXfactory` | 1 | **0** |

  **417 repositories across the four orgs, six `dox`-named, and all six are the
  product's own** — the six § 8.1 requires to exist. `AdxFactory` and
  `OpsxFactory` have no org of their own; both live in `opensoft` and are inside
  its 402. So **no `<Domainx>Dox` repository exists in any org of this estate**,
  which is what the sentence above claims and what a one-org report could not
  establish. (`gh api orgs/<org>/repos --paginate --jq '.[].name'`, the same
  invocation § 8.8 uses, at the same reading.)
- [~] 7.3 `[?]` **DEFERRED SUCCESSOR (RULED R-3, 2026-09-16, `#656` comment
  `5690428146`) — carried out of this packet in the form § 4.5 was carried under
  openxFactory #714 and § 0.6's RULED PATH A**: the ruling § 7.1 owed has landed
  and its answer is NONE YET, so the act this box describes has no subject to
  perform on, and it does not tick here, block § 8's archive gate, or lapse.
  **The marker is `[~]`, the house's RESERVED DEFERRED FORM, and that is load
  bearing rather than cosmetic**: `scripts/proposal-support.py`:**4609-4610**
  refuses an archive whose `tasks.md` still matches `^- \[ \]` — *"change has
  incomplete tasks"* — so a deferred successor left at `[ ]` would contradict, in the
  archive machinery itself, the sentence before this one. The form is the one the
  archived packets use for exactly this standing:
  `archive/2026-09-09-add-openspec-cli-pin/tasks.md`:244-255 (which names it
  *"the house's reserved DEFERRED form"* and cites
  `archive/2026-08-21-add-doxbench-editing-phase-a/tasks.md` § 5.3 for it),
  `archive/2026-09-09-pin-openspec-cli-dependency-closure` §§ 6.1/6.2,
  `archive/2026-09-10-adopt-codexfactory-repository-identity` §§ 5.7, 8.4, 9.1-9.6,
  and `archive/2026-09-10-accept-sequenced-after-header-line` § 4.4 — **five
  archived packets, thirteen boxes, and that is every `^- \[~\]` in
  `openspec/changes/archive/`.**
  *(Measured rather than assumed, because "as § 4.5 was" invites the opposite
  reading: § 4.5 wore `- [ ]` while it was the recorded deferred successor — it
  reads `- [ ]` at `56e69a11`, the #832 archive commit that recorded the
  deferral, and `- [x]` at this packet's merge-base `8f393758` after it was
  built. What the ruling carries over from § 4.5 is the STANDING — open, owned,
  not lapsed, not gating — not the character in the box. This is the first `[~]`
  in this packet.)*
  **A DEFECT IN THIS BOX'S RATIFIED TEXT IS REGISTERED HERE AND DELIBERATELY
  NOT REPAIRED** (amendment #5, registered on amendment #4's pull request at
  comment `5702227094` item 7, from a Copilot finding that is correct). The
  specification below opens *"When the ruling lands"*, and the ruling has
  landed — RULED **R-3**, 2026-09-16, `#656` comment `5690428146` — so the
  phrase now reads as a past event while the act it governs has not run. The
  true trigger is stated in the sentence that immediately precedes the phrase,
  later in this box: *"the successor act that runs when a domain acquires its
  first profile artifact"*. **Measured, the phrase
  is the packet's OWN RATIFIED TEXT and no amendment authored it**: it enters
  at `ceb6dc9e`, the commit that ratified this packet (`#666`), stands
  identically at `main`, and amendment #4 only MOVED it — out of the box
  header `- [ ] 7.3 [?] When the ruling lands: …` into this body — while
  re-marking the box `[~]`. **Re-wording ratified specification text is a
  SPEC-DELTA-CLASS ACT**, which is exactly the disposition RULED
  `5700622683` (2026-09-16T16:06:59Z, by interactive multi-choice) gave §
  7.1's scenario-4 delta defect: recorded, repair owed from a later act that
  CLAIMS the delta, not silently corrected by a prose sweep. A bookkeeping
  amendment fixes stale COORDINATES (§ 1's two cites, § 1.8's positions) and
  does not re-word what ratification was over. Registered, with the correct
  trigger already quoted here, so the act that repairs it re-derives nothing.
  It is the successor act that runs when a domain acquires its first profile
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
  **SPLIT AND NARROWED 2026-09-16 — RULED `5704187317`** (`#656` comment,
  2026-09-16T20:40:06Z; Brett Heap, by interactive multi-choice, on one
  question from this lane's § 7.4 actor;
  measurement banked at `brett-wip` `fb3e0821`
  `attachments/lane-opendox/ops74/measurements.md`; no claim was posted and
  nothing was authored before the ruling). **THE BOX DOES NOT TICK HERE.** The
  ruling disposes of it in FOUR NAMED PARTS — **(A)**, **(B)**, **(D)** and
  **(E)**, the RULING'S OWN labels over the five measured reads the actor put
  to it. **There is no (C) here and the gap is load bearing rather than a
  typo**: read **(C)** was the DNS widening's MECHANICS — that it is a
  five-place lockstep whose first place, `infra/aks-security/
  prod-network-security/dns-ceremony-reach.yaml`, sits in
  `opensoft/Opensoft-Tenant`, a repository this lane holds no clone of and no
  claim in — and the ruling folds it into **(B)** rather than disposing of it
  separately, which is why (B)'s sentence below names the lockstep and that
  repository by name. Four dispositions over five reads, with the fifth's
  content inside the second:
  **(A) A SECOND § 7.4 DELTA-TEXT DEFECT IS RECORDED, IN THE CLASS OF RULED
  `5700622683`, AND NOT SILENTLY CORRECTED.** This packet's `design.md`
  lists under **## Non-goals**, verbatim at `:133-134`, *"Resolving
  codexFactory's false `stack.yaml` digest declaration, or the `openxdox` DNS
  record's ungoverned status, **beyond naming them**"* — while the closing
  sentence of this box says that record *"is governed here"*. **Two pieces of
  ratified text in ONE packet that cannot both be executed**, and `design.md`
  `:101-103` supplies the measured state they disagree about, in the same
  sentence that carries the workload coordinate: *"OpsxFactory declares the
  four `dox` workloads at `workflows/aks-administration.yaml:412-431`; the
  `openxdox` DNS A record exists on the live zone and is ungoverned"*. The
  contradiction is recorded for repair by a later act that CLAIMS the delta,
  on the same disposition § 7.1's scenario-4 defect took two hours earlier.
  **(B) THE DNS SENTENCE IS READ AS DISCHARGED BY NAMING**, per the packet's
  own Non-goal. The reach widening — governing the record itself — belongs to
  lane `opsXfactory-4`'s ACTIVE `add-governed-dns-administration` under Brett
  Heap's OQ-E word `5649809425`, and the act is a five-place lockstep reaching
  `opensoft/Opensoft-Tenant`. This packet names it and stops.
  **(D) THE `dox` WORKLOAD SET'S PER-TENANT DECLARATION IS LEFT FOR THE § 3.5
  REALIZATION** — there is no second tenant to describe until openDox's
  runtime exists, and the requirement it sits under is inside lane
  `opsXfactory-3`'s claim `5638511222`. *(The coordinate this box quotes has
  moved. Measured by this lane's § 7.4 actor at OpsxFactory `7e15da58` and
  banked at `brett-wip` `fb3e0821`: the `dox` workload set sits at
  `workflows/aks-administration.yaml`:733-753 there, not at the `:412-431`
  this box and `design.md`:102 both quote. Recorded, NOT re-pointed — for the
  same reason as (A), it is ratified text, and a quotation is bound to the
  tree the packet was written against.)*
  **(E) THIS LANE'S ONLY AUTHORED ACT UNDER § 7.4 IS A `credential-contracts`
  MODIFIED DELTA IN `openxFactory`** carrying the per-tenant App-Manifest
  PROVISIONING shape (tenant-org creation, `openXdox — <tenant>` naming,
  apply-repo home, credential capture) — OQ-1 option (a) of the staged topic
  `openxdox-install-app-provisioning`. The two-App dispatch/content
  SEPARATION is already canon — the promoted `credential-contracts` requirement
  *Dispatch-only credential least privilege and serving-tier separation*
  (`openspec/specs/credential-contracts/spec.md`:169 at this amendment's ORIGINAL base
  `cbc3a2c6`)
  — and what is missing is the provisioning shape. One repository,
  no Ops collision, CLAUDE.md working rule 1 satisfied. **The options are a
  SECOND enumeration and not a re-labelling of the reads** — they are what was
  put to the ruling as a multi-choice: **(1) SPLIT AND NARROW, which is what
  (A)-(E) above record and what was TAKEN**; **(2)** hand the DNS and workload
  halves to lanes `opsXfactory-4`/`-3`; **(3)** hold all of § 7.4. **(2) and
  (3) were DECLINED.**
  **THE TICK CONDITION, STATED SO A LATER READER NEED NOT RE-DERIVE IT:** this
  box ticks on (i) this ruling, (ii) the landed `credential-contracts` delta
  of (E), and (iii) § 3.5's per-tenant evidence when it exists.
  **(i) AND (ii) ARE NOW IN HAND; (iii) IS NOT, WHICH IS WHY THE MARKER IS
  UNTOUCHED.** Clause (ii) landed the NEXT UTC DAY after the ruling — the
  ruling at 2026-09-16T20:40:06Z, the delta at 2026-09-17T13:44:02Z,
  **seventeen hours and four minutes apart**:
  `add-per-tenant-app-manifest-provisioning`, `opensoft/openxFactory` **#1073
  → `74647dfc`** (CLAIM `5704248880`; LANDED note
  `5715385370`). It carries exactly (E)'s object and nothing else: the
  `credential-contracts` MODIFIED delta restates the `:169` invariant
  *Dispatch-only credential least privilege and serving-tier separation*
  VERBATIM — body and all three promoted scenarios — and grows it by FIVE
  clauses and TEN scenarios, counted in the landed tree at `74647dfc` rather
  than estimated: the requirement carries **13** `#### Scenario:` blocks where
  the promoted one carried **3**, and all three of those survive by title. The
  five clauses are tenant-org creation through a declared
  credential-free manifest and never by an operator identity; that the clause
  binds where the identity LIVES and not who drives the flow, so an
  operator-executed install may still drive it and a pair already in service
  is not retroactively refused; one App pair per
  tenant under a pattern-discoverable `<product> — <tenant>` name; the dispatch
  identity's one named target holding no governed content; and time-bound
  capture into the tenant's own custody BY REFERENCE, no material in any
  record. `code_surface: none`, `target_release: implemented`.
  *(THE LEAD-IN TO THIS PARAGRAPH SAID "THE SAME DAY" AND IT WAS WRONG —
  amendment #5's own defect, raised at review and corrected in the round that
  received it. The ruling's clock and the landing's clock were both already
  written in this box; neither was misread, they were never read TOGETHER.
  The remedy is the one this amendment applies to positions: quote both
  figures and let a reader subtract, rather than assert the relation between
  them and ask to be believed.)*
  **And it HONOURS (B) and (D) by omission**: `opensoft/OpsxFactory` and
  `opensoft/Omnigent-Install` are not touched by a byte, which is what the
  ruling narrowed this lane to. **That is evidence about THIS act's SCOPE and
  not about those dispositions, neither of which is discharged**: (B)'s reach
  widening is lane `opsXfactory-4`'s ACTIVE `add-governed-dns-administration`,
  and (D) waits on the § 3.5 realization by its own terms. *(This read "PROVES
  (B) and (D)" until review. An act's SILENCE about a repository proves only
  that the act stayed inside its narrowing; it says nothing about whether the
  work those clauses name has been done.)*
  It is `[ ]` and not `[~]` because this box is an IN-SCOPE GATING PREREQUISITE
  of this packet, where `[~]` is the reserved form for open, OWNED, NON-GATING
  successor work. *(WHAT WAS WRONG HERE WAS THE GENERALISATION, NOT § 7.3'S OWN
  SENTENCE. § 7.3 says the ruling its § 7.1 owed has landed and its answer is
  NONE YET, so the act THAT box describes has no subject to perform on — a true
  statement about one box's circumstances. THIS box read that particular fact as
  the MARKER'S RULE, which it is not, and a wrong rule in a ledger propagates to
  every amendment that reads it. Measured against the house's own use rather than
  recalled: EVERY `[~]` in the active corpus names an OWNER —
  `add-per-tenant-app-manifest-provisioning/tasks.md` carries six, among them
  *"Owner: lane `opsXfactory-4`"* and *"Owner: this lane's bookkeeper,
  amendment #5"* — so a deferred box HAS an owner even where, as at § 7.3
  today, it has nothing yet to act on. What it does not have is a claim on THIS
  packet's gate.)*

## 8. The archive gate

Under `release-realization` this change archives ONLY on merged plus green
realization evidence, never on landing. Each line is its own evidence.

- [x] 8.1 **All SIX repositories exist** (amended 2026-09-05 — this first said
  "Both repositories"), PUBLIC, Apache-2.0, each with a required check that has
  reported at least once and a ruleset promoted from EVALUATE to ACTIVE; each
  assembly root's `project.yaml` records the election (`elected_by: Brett Heap`,
  `elected_on: 2026-09-05`, `reference: openxFactory docs/project-repo-schema.md`) and its
  `validate` gate is green over its own legs.
  **TICKED 2026-09-16 ON EVIDENCE TAKEN THE SAME DAY, NOT ON THE 2026-09-06 READ
  IT SUPERSEDES** — `#656` comment **`5690559647`**, which carries each command
  and its output. All six of `opensoft/openDox{,-spec,-code}` and
  `opensoft/openXdox{,-spec,-code}` read `visibility=public`, `private=false`,
  `license=Apache-2.0`, `default=main`. The six ruleset ids this packet recorded
  at the 2026-09-06T08:56Z promotion (this file's :411-424) read back live as
  `enforcement: active`, `target: branch`, required check `validate` — the same
  six ids, ten days on. The EVALUATE→ACTIVE **transition** is § 1.5's record
  (created EVALUATE 2026-09-06, promoted on Brett Heap's ruling `5558170462`);
  both are cited because a live read proves the STATE and cannot re-prove a past
  transition. **A trap the evidence records rather than trips on:** `validate` is
  a `pull_request` gate in all six, so NOTHING attaches to any `main` head and a
  naive re-check reads six reds. This box's clause is *"has REPORTED at least
  once"*, and where it reported is the pull requests — **265 `validate` runs
  across the six** (11 + 45 + 94 + 12 + 43 + 60), the latest `success` in every
  one. The clause *"its `validate` gate is green over its own legs"* is the two
  ASSEMBLY-root runs, and they are pin lockstep #2's own pull requests —
  `opensoft/openDox#8` run `35027390906` and `opensoft/openXdox#10` run
  `35027756247`, both `success` — whose `validate` IS the leg-pin verification.
  The election reads live out of each assembly root's own `project.yaml` at
  `main`, the SOURCE from which the register row is derived (§ 1.9):
  `elected_by: "Brett Heap"`, `elected_on: 2026-09-05`,
  `reference: "openxFactory docs/project-repo-schema.md"`, verbatim in both.
  `#656` records: CLAIM `5690461589`; evidence `5690559647`.
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
  **The fourth part's evidence line MAY ALSO SAY that § 4.4's domain profile
  reproduces `openxFactory`'s own vocabulary** (`picked` / `staged`, via
  `domain_profile.current()`) — RULED **Q-P4 (a)**, `#656` comment
  `5728856581`, 2026-09-18. **It adds no part and moves no box**: the floor is
  four parts and stays four, § 4.4 is already `[x]` on its own evidence, and
  this is a statement the run is entitled to make rather than a fifth thing the
  line must prove.
  **PART 4'S EVIDENCE LINE NOW HAS ITS REFERENT — recorded by `tasks.md`
  AMENDMENT #6, 2026-09-18**: it points at `openxFactory` **#1105 →
  `02967478`** (merged 14:59:28Z), the gated snapshot-equivalence runner and its
  suite, **plus the § 4.4 profile-fidelity sentence per RULED Q-P4 (a)**. **This
  box stays `[ ]`**: § 8.2 owes ONE EVIDENCE LINE PER PART and is discharged by
  all four, not by the fourth; naming part 4's referent here is what lets the
  act that finally ticks this box quote a commit instead of re-deriving one.
- [x] 8.3 `openxFactory`'s shed merged, the MAJOR cut and TAGGED, and the tag
  verified from an INDEPENDENTLY REFRESHED checkout.
  *(TICKED 2026-09-18 by `tasks.md` AMENDMENT #6 on Brett Heap's word, against
  the live evidence posted verbatim at `#656` comment `5729935756` (claim
  `5728902552`). The box names THREE clauses and the tick is decided by reading
  its own text, clause by clause, each on its own artifact:*
  **(1) the shed merged** — `openxFactory` `#940`, `state=MERGED`,
  `mergedAt=2026-09-11T17:33:38Z`, merge commit **`cc4ae9d3`**.
  **(2) the MAJOR cut, and TAGGED** — `openxFactory` `#983`, `state=MERGED`,
  `mergedAt=2026-09-11T23:51:05Z`, merge commit **`ce5c054e`**; annotated tag
  `contract-v4.0`, tag object **`9e6c0ae4`**, which peels to `ce5c054e`
  EXACTLY — the tag names the cut itself and not a neighbouring commit —
  tagger Brett Heap 2026-09-12T00:21:18Z.
  **(3) verified from an INDEPENDENTLY REFRESHED checkout. THE PROCEDURE IS TWO
  STEPS, NOT ONE, and amendment #7 writes the second into it**: `gh repo clone
  opensoft/openxFactory && cd openxFactory && git submodule update --init
  --recursive openDox openXdox`. **The `cd` is part of the recipe, not an
  omission the reader is expected to supply**: `gh repo clone` leaves the shell
  in the PARENT directory, so a `git submodule update` written as a separate
  step runs outside the new checkout and fails before the verifier is reached.
  *(Caught by Copilot against `ec5d5144` — a recipe written to fix a recipe.)* Without the second step the verifier exits **2** on
  `ReleaseDependencyError` and emits NO finding, so a reader following the
  recorded procedure could not reproduce the pass the record claims. *(#6
  disclosed this at clause (c) below but left it out of the procedure — a
  warning the reader meets AFTER the command they already ran. The tick is
  unaffected: two independent checkouts did pass. This corrects the RECIPE, not
  the RESULT.)* The evidence: the helper's
  fresh `gh repo clone` today, AND re-derived in this lane's own clone rather
  than transcribed: `python3 scripts/validate-contract-release.py verify-tag
  --remote origin --tag contract-v4.0 --json`, and the matching `verify-commit
  --commit ce5c054e… --json`, each return `{"findings":[],"status":"pass"}` at
  `exit_code` 0, the second against inventory
  `contracts/releases/contract-v4.0.digests.yaml`. Two independent checkouts
  agree, which is the thing clause 3 actually asks for.*
  **Three readings that could be mistaken for defects are disposed of here
  rather than passed over in silence:**
  **(a) the tag is UNSIGNED.** It is a genuine annotated tag — `git cat-file
  -t contract-v4.0` returns `tag`, not `commit` — and it carries no signature.
  Measured across the repository, ALL 56 `contract-v*` tags are the same
  unsigned annotated form, so `contract-v4.0` matches standing practice
  exactly; and this box asks for the tag to be **verified**, which it is, not
  signed. Not a defect. Making release tags signed would be a corpus-wide
  change to 56 tags and belongs to its own claim, not to this tick.
  **(b) `verify-promotion` returns 4 findings** — `HGR-RELEASE-TAG-EXISTS` on
  `refs/tags/contract-v4.0`, plus `HGR-RELEASE-SURFACE-DRIFT` on
  `contracts/CHANGELOG.md`, `contracts/README.md` and `contracts/manifest.yaml`.
  This is a PRE-CUT gate read AFTER the cut, per its own docstring at
  `scripts/hermes_runtime_validation/release.py:1197` — *"Prove a candidate is
  promotable immediately before tagging."* Once the tag exists,
  `HGR-RELEASE-TAG-EXISTS` is guaranteed BY CONSTRUCTION, so the run is
  answering a question this box does not ask. Not a tag defect; it moves no box.
  **(c) a HARNESS error can impersonate a tag finding.** Run from a checkout
  whose `openDox`/`openXdox` legs are SHALLOW or partial, the run fails on
  `ReleaseDependencyError` WITHOUT emitting any finding — reproduced in this
  lane's clone, then cleared by `git submodule update --init --recursive
  openDox openXdox`. **The failure SHAPE is the tell, and the shape differs by
  how you call it**: the CLI CATCHES that error, prints a one-line
  `validate-contract-release: …` refusal on stderr and returns **exit 2** with
  NO `findings` at all (`scripts/validate-contract-release.py:182-184`), while
  a direct library call raises and gives a traceback — which is how this lane
  first met it. Either way the tell holds: **a tag defect arrives as a
  `findings` entry and a leg defect never does.** *(This passage said flatly
  that a leg defect "arrives as a traceback", which is true of the library
  call this lane made and NOT of the CLI the sentence records. Corrected on a
  Copilot finding against head `47a41ee5`; it was right, and a passage whose
  whole point is the failure shape has to get the failure shape right.)* A plain
  `gh repo clone` does not init submodules, so anyone re-running clause 3 from
  a fresh checkout meets this before they meet the tag.*
  *(One figure in the cited evidence is CLOCK-BOUND, and is restated as
  measured rather than copied across: the comment records `ce5c054e` as 438
  commits behind `origin/main`; at this lane's measurement it is **452**. The
  ANCESTRY is the durable fact — `git merge-base --is-ancestor ce5c054e
  origin/main` exits 0, so the cut is on the main line — while the DISTANCE
  moves every time anybody lands anything. The byte-identity of
  `contract-v4.0.digests.yaml` at the cut and at main's tip (blob `84db9ce6`
  at both) is the same assurance in a form that does not rot.)*
- [ ] 8.4 The codexFactory floor de-floored BEFORE the removal, in that order, with
  the five openxFactory pin sites moved in ONE reviewed diff. Note the floor must
  account for BOTH directions of this archive: `openspec/specs/ideation-dashboard/`
  removed, and the two new capability directories plus the § 5.2a adapter successor
  capability ADDED.
- [ ] 8.5 All five re-homed changes dispositioned, each with its destination named
  in the receiving repository; `retire-doxbench-chat-turn-v1` archived in
  `openxFactory` on its own evidence first.
  **STATUS — RECORDED BY `tasks.md` AMENDMENT #7, 2026-09-18. THE BOX DOES NOT
  TICK, AND WHAT IT STILL WANTS IS NAMED EXACTLY.** The openxFactory side IS
  complete — all five closures landed (§§ 6.1–6.5, shas in their own boxes) and
  all five directories are under `openspec/changes/archive/`, read from the
  tree — and the aggregation side is `xFactory` **#454 → `0b0c88f4`**
  (AGGREGATION-SIDE RECORD A1 at § 8.7). **Two things the box's own words ask
  for are not yet in hand:**
  **(a) IS NOW CLOSED — AMENDMENT #8 SUPPLIES THE TWO MISSING SHAS.** All four
  re-homes name a destination-side pull request in the receiving repository,
  and a fifth exists for § 6.2's forward half:
  • § 6.1 `add-nightly-dashboard-refresh` → `openXdox-spec` **#15 → `f088b097`**
  • § 6.3 `add-doxchat-model-intake` → `openDox-spec` **#13 → `3b7f80c4`**
  • § 6.4 `add-composed-view-authoring` → `openDox-spec` **#12 → `edeed08c`**
  • § 6.5 `add-lens-document-selection` → `openDox-spec` **#14 → `66d59778`**
  • § 6.2's FORWARD half → `openDox-spec` **#15 → `8fe8c4c7`**, *"Carry the
  surviving -v2 chat-turn family into openDox"* — named for completeness, since
  § 6.2 is the one that archives here rather than re-homing.
  *(Amendment #7 reported these two as missing. They were not missing from the
  CORPUS, only from this ledger — which is a different finding and is why #7
  wrote "or a finding that the destination half does not exist" rather than
  assuming either. They exist.)*
  **(b) IS NOW THE ONLY THING BETWEEN THIS BOX AND A TICK, AND IT IS A RULING
  RATHER THAN A MEASUREMENT. The word "FIRST" needs a reading, and it is NOT
  satisfied on the obvious one.** `retire-doxbench-chat-turn-v1` (§ 6.2) archived **LAST** of the
  five, not first: `#1056` 10:50:06Z, `#1057` 13:31:51Z, `#1060` 17:30:27Z,
  `#1065` 17:54:08Z, `#1066` **20:24:53Z**. If "first" means *before the other
  four*, the record contradicts it and the box cannot tick as written. If it
  means *before its own forward half promotes*, or *before § 8* (which § 6.2's
  box does say — *"Sequenced BEFORE § 8"*), it holds. **This is a ruling, not a
  measurement**, and it is left to the ticking act rather than decided here by
  picking the reading that happens to let the box tick.
- [x] 8.6 `ideation-intent-plane` in canon, or its non-promotion recorded (§ 0.6).
  **TICKED 2026-09-16 ON THE FIRST OF THE TWO DISCHARGES, RE-READ LIVE** —
  `#656` comment **`5690559647`**. `openspec/specs/ideation-intent-plane/spec.md`
  is present at `openxFactory` `main` **`cb2d3a2c`** (7,606 bytes, **seven**
  `### Requirement` headings), and there is no active change directory of that
  name: the change is archived at
  `openspec/changes/archive/2026-09-09-add-ideation-intent-plane/`.
  **RE-READ AT THE `main` THIS BRANCH MERGED — `c5f68457`, amendment #3's own
  landing, merged here at `f7a15723` — AND NOT ONE FIGURE MOVES**: the same
  **7,606** bytes, the same **seven** `### Requirement` headings, still no active
  change directory of that name, still archived at the same path. That re-read is
  bound to a commit IN THIS PULL REQUEST'S OWN HISTORY, which is what a claim
  about the CURRENT head needs in order to stay true between this line and the
  merge.
  *(A Copilot finding on this amendment's own pull request, raised in four
  consecutive rounds, 14-17. It is the one repetition that reaches a TICK, and
  that is why it is fixed rather than registered: everywhere else in this packet
  a figure measured at a NAMED tree is exactly right, but a box asserting that a
  gate is "still true of `main` today" is a claim about the current head, and
  `main` moved twice while this amendment was open — `cb2d3a2c` → `d5dd1ca5` →
  `c5f68457`. The first read is kept beside the re-read because that is where the
  figures were FIRST taken, which is this packet's own discipline.)*
  That is RULED
  PATH A (`5555554097`) reaching canon, so **no non-promotion disposition is owed
  and none should be written** — this box's `or` branch is the one that must stay
  empty. § 0.6's own DONE line (openxFactory #832 → `56e69a11`) is therefore
  still true of `main` today and not only of the day it landed, which is what
  re-reading it establishes and what a ticked archive-gate line has to mean.
- [x] 8.7 The aggregation's **openXdox AND openDox** gitlinks landed, **each
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
  and Q7 made those two.
  **THE RE-POINT LANDED WHILE THIS AMENDMENT WAS OPEN, AND THE EQUALITY THIS LINE
  CHECKS WAS KEPT THROUGH IT RATHER THAN RESTORED BY IT.** The act is
  `opensoft/xFactory` **#453 → `514605fb396d4ebd52914c58d7e22370309278ba`**,
  merged **2026-09-16T12:46:00Z** on Brett Heap's word by interactive
  multi-choice (CLAIM `5690483061`; four sites in one commit — the two gitlinks,
  the aggregation's own `openxFactory` gitlink, and
  `.github/clearing/openxfactory/PIN.yaml` beside it). Measured on BOTH sides of
  it, which is the point:
  — **BEFORE**, at the aggregation's own `784a7c6e` against `openxFactory`
  `75484b67`, all three readings of each name already agreed — aggregation
  gitlink `openDox` `8ec3036c` == `openxFactory`'s nested `openDox` `8ec3036c`
  == `contracts/opendox-pin.yaml`'s `commit:`, and `openXdox` `eca0b597` across
  the same three.
  — **AFTER**, at `514605fb` against `cb2d3a2c`, the same three agree again at
  `3819625e` and `a6500141`.
  **So the sync moved the pointers forward without ever breaking the equality —
  an invariant KEPT, not repaired**, which is worth writing down because a check
  that only ever runs after a re-point cannot tell those two apart. The
  ASSEMBLY-ROOT clause holds on both sides: `.gitmodules` at `514605fb` names
  `git@github.com:opensoft/openDox.git` and `git@github.com:opensoft/openXdox.git`,
  and `openxFactory`'s own `.gitmodules` at `cb2d3a2c` names the same two — four
  declarations, four assembly roots, no leg. The register clause is § 1.9's and
  already `[x]`: the two derived rows landed at `opensoft/xFactory` **#442 →
  `41d6d7ae`** and remain true across this re-point, because each assembly root's
  `project.yaml` — the SOURCE the rows are derived from — is **byte-identical at
  the old pointer and the new** (`openDox` 7,999 bytes at `8ec3036c` and at
  `3819625e`; `openXdox` 8,015 bytes at `eca0b597` and at `a6500141`), so no
  re-derivation was owed and none was made. A THIRD gitlink moved in that same
  re-point — the aggregation's own `openxFactory`, `75484b67` → `cb2d3a2c` — and
  this line does NOT check it, because it is not one of the two the descendant pin
  chain is about; named here so the re-point does not read this line as its whole
  checklist. **This box is NOT ticked by AMENDMENT #4** — *"this amendment"* in
  the sentence as amendment #4 wrote it, bound here because amendment #5's tick
  stands four lines below and an unbound pronoun makes a `[x]` box say it is not
  ticked. R-5 ruled the WORDING
  of the check, not the verdict on it, and the packet's tick standard puts a tick
  in the act that claims it — the same treatment § 5.2's STATUS gives § 5.6a
  defect (a). What is owed for that tick is now measured and on the record here.)*
  **TICKED 2026-09-17 BY `tasks.md` AMENDMENT #5 (CLAIM `5704937336`, POSTED
  2026-09-16T21:39:02Z — the SAME claim and the SAME amendment as § 5.3's
  tick of the 16th; one act, two UTC days, each box dated by the day its own
  evidence closed), ON PIN
  LOCKSTEP #3 — the act this box's own STATUS said would carry it.** The
  amendment above ruled the WORDING and left the verdict to the act that
  claims it; this is that act, and the evidence is a five-place lockstep
  closed end to end on 2026-09-17:
  `opensoft/openDox` **#9 → `c4c5014d`** (assembly root A1) ·
  `opensoft/openXdox-code` **#21 → `2529c10a`** ·
  `opensoft/openXdox` **#11 → `88a1047e`** (assembly root A2) ·
  `opensoft/openxFactory` **#1084 → `dc015d7a`** (2026-09-17T13:10:54Z) ·
  `opensoft/xFactory` **#458 →
  `b660266686025b7e38863d6186ccab5139d96ba7`** (2026-09-17T13:33:10Z, on
  Brett Heap's word, RULED **R-5**).
  **THE EQUALITY IS RE-DERIVED HERE FROM THE TREES RATHER THAN TRANSCRIBED
  FROM THE ACT THAT MADE IT** — which is the whole point of a check that only
  ever runs after a re-point. Read at `xFactory` `b6602666` and at
  `openxFactory` `dc015d7a`, **three independent readings of each name agree**:

  | read | `openDox` | `openXdox` |
  | --- | --- | --- |
  | aggregation gitlink at `b6602666` | `c4c5014d` | `88a1047e` |
  | `openxFactory`'s own nested gitlink at `dc015d7a` | `c4c5014d` | `88a1047e` |
  | `openxFactory`'s pin file `commit:` at `dc015d7a` | `c4c5014d` | `88a1047e` |

  — `contracts/opendox-pin.yaml` and `contracts/openxdox-pin.yaml`
  respectively. **And the aggregation's own `openxFactory` gitlink at
  `b6602666` is `dc015d7a`**, the very commit those pin files belong to, so
  the aggregation reads both products at exactly the commits the repository
  it pins declares for them. **All four names are ASSEMBLY ROOTS**, which is
  this box's other clause and is unchanged from the reading recorded above.
  The register clause is § 1.9's and is already `[x]`; this lockstep derives
  no new rows.
  *(The BEFORE/AFTER measurement in the amendment above stands as written —
  it recorded that the #453 re-point KEPT the equality rather than repairing
  it. This tick adds the third such passage and the same finding: the
  invariant held across pin lockstep #3 as it held across #453, and a box
  that ticks on an equality should say which of those two it saw. It saw the
  first.)*
  **AGGREGATION-SIDE RECORD A1 — § 6'S PROMOTION FIDELITY. Added by `tasks.md`
  AMENDMENT #7, 2026-09-18. IT IS NOT PART OF § 8.7's TICK EVIDENCE and moves
  no box** — § 8.7 ticks on GITLINKS, and this is a different aggregation-side
  act recorded beside it because this is where a reader looks for one.
  `opensoft/xFactory` **#454 → `0b0c88f4`**, merged **2026-09-18T21:15:14Z**,
  *"Record the four § 6 re-homed closures' five delta files' non-promotion as
  deliberate (promotion-fidelity dispositions)"*. It touches exactly one file,
  `health/dispositions.yaml`, and disposes **20 findings** measured at
  `openxFactory` `main` `3bf63b8e`; the aggregation gate reads **0/0/0/0**, and
  the header's own count was corrected from *"+15"* to a net **+20** before it
  landed.
  **FOUR CLOSURES, FIVE FILES — and § 6.2 RAISES NONE.** The asymmetry is the
  point and the dispositions file says so in terms: § 6.2 is the one of the five
  that is NOT closed as re-homed, so its delta's promotion obligation is
  discharged **by PROMOTION** rather than by a disposition, and it *"must not
  get one by analogy"*. The fifth file exists because
  `add-nightly-dashboard-refresh` carries TWO deltas (`doc-health` and
  `ideation-dashboard`), which is the same partial-carriage shape § 6.1's own
  STATUS registers against `_REHOMED_AND_STILL_WHOLE`.
  **ONE FACT REGISTERED AS RESIDUE, NOT RESOLVED HERE, owed to the next act that
  touches that file**: its header states *"three of the five files carry more
  than one affected requirement"*. **Measured at `3bf63b8e`, it is FOUR.**
  Counting `### Requirement` in each: `add-composed-view-authoring` → **1**;
  `add-doxchat-model-intake` → **5**; `add-lens-document-selection` → **5**;
  `add-nightly-dashboard-refresh`/`doc-health` → **7**; the same packet's
  `ideation-dashboard` → **2**. Only ONE of the five carries a single
  requirement, so four carry more than one.
  *(The figure changes nothing about the dispositions themselves — each entry is
  PATH-KEYED and deliberately not narrowed by `requirement:`, so the count is a
  statement in the header's prose rather than a key any entry turns on. It is
  registered because a header that miscounts its own subject is the defect class
  this packet has spent two amendments on, and because the next reader of that
  file will reach for the number rather than recount five files.)*
- [x] 8.8 Amendment 3 applied with the SIX repository names and the election,
  and the descendant names — each with its two leg names — registered with no
  repository created (amended 2026-09-05).
  **TICKED 2026-09-16, AND ITS SECOND HALF IS NOW PROVEN BY ENUMERATION RATHER
  THAN BY SIXTEEN NEGATIVE LOOKUPS** — `#656` comment **`5690559647`**. FIRST
  HALF: § 1.6 applied Amendment 3 to `docs/openxdox-naming.md` carrying the SIX
  repository names and the election, and § 1.7's own DONE record registers the
  fifteen descendant names (five bases × three) plus `openXdox-Install` inside
  Amendment 3's own paragraph, that paragraph being the registration because the
  file has no separate names table. Both boxes are `[x]` on their own evidence.
  SECOND HALF, re-measured today: all sixteen names return `404 Not Found`
  individually, as on 2026-09-06 — **and sixteen 404s prove only that those
  sixteen spellings are absent from ONE org**, while a descendant would plausibly
  be created in its own domain's org (`codexFactory` lives in `codeXfactory`,
  `MedxFactory` in `MedxSoft`, `LedgerxFactory` in `ledgerXfactory`). So the
  listing was taken org-wide across all four estate orgs for ANY repository whose
  name contains `dox`. **The two columns are separate and are reported
  separately**, because a repository TOTAL is not a `dox` result:

  | org | repositories enumerated | of those, `dox`-named (case-insensitive) |
  | --- | ---: | --- |
  | `opensoft` | 402 | **6** — `openDox`, `openDox-spec`, `openDox-code`, `openXdox`, `openXdox-spec`, `openXdox-code` |
  | `codeXfactory` | 1 | **0** |
  | `MedxSoft` | 13 | **0** |
  | `ledgerXfactory` | 1 | **0** |

  **417 repositories enumerated, six `dox`-named, and all six are the six § 8.1
  requires to exist.** Not one descendant name, not one leg name, not
  `openXdox-Install`, in any casing, in any of the four orgs. *(The evidence
  comment reports 401 and 416 at 01:1xZ; this re-read at 13:3xZ finds 402 and
  417 because `opensoft` gained one repository in the interval. The `dox` column
  is unchanged at 6/0/0/0, which is the column this box turns on — recorded
  rather than quietly re-stated, since a total that moves and a result that does
  not is exactly the distinction this line needs to make.)*
  `#656` records: CLAIM `5690461589`; evidence `5690559647`.
- [ ] 8.9 `python3 -m pytest tests/doc-health tests/sequenced_after -q` green,
  `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health
  run whose severity counts move by the amount **the archive pull request RECORDS
  AND EXPLAINS**.
  *(THIRD CLAUSE REWRITTEN 2026-09-16 by RULED **R-6**, `#656` comment
  `5690428146`. It read "a doc-health run whose severity counts move by exactly
  the amount the packet predicts" — **and the packet predicts no amount
  anywhere**. Measured across the whole packet OUTSIDE THIS BOX, `review/`
  included — the only framing of this count that stays true while the box is
  being written — "severity" occurs **SEVEN** times in **FIVE** files, with **no
  further occurrence anywhere in `tasks.md` outside this box** (inside it there
  are several, this sentence among them, which is the whole reason the count is
  scoped this way): `design.md`:225 (a glossary row),
  `review/ratification-2026-09-05.md`:649, :691 and :783,
  `review/reality-check-2026-09-05.md`:302,
  `review/amendment-2026-09-05-repository-shape.md`:246, and
  `review/amendment-2026-09-09-floor-part-2-mapping.md`:45 (which is a CHANGE
  NAME, `2026-09-03-amend-owner-layer-severity`, not a count at all). **Not one
  is a prediction.** The three review records each report a MEASURED
  doc-health delta of **ZERO** across every family and every severity for a
  packet that, at ratification, performed nothing — which is exactly why "the
  amount the packet predicts" has no referent for an archive that follows a
  carve, six repositories and a shed. The obligation is not weakened, it is
  relocated to the act that can discharge it: the archive pull request states the
  movement it caused and why, and a movement it does not explain fails this line.
  **"RECORDS AND EXPLAINS" IS NOT "SAYS SOMETHING AFTERWARDS", AND THE FORM IS
  FIXED HERE SO THE LINE STAYS FALSIFIABLE.** The archive pull request SHALL
  carry: (a) the BASELINE, **fixed before the run rather than chosen after it —
  the archive pull request's OWN BASE commit, the last pre-archive `main`, named
  as a sha** together with the doc-health invocation, both stated before the
  AFTER run is taken; a baseline selected afterwards, or any tree other than the
  one the archive merges into, does not discharge this clause, because a free
  choice of baseline can manufacture whatever delta the record wants. **The
  AFTER run is bound the same way and for the same reason**: it names the
  archive pull request's OWN HEAD as a sha — or, once it exists, the resulting
  merge commit — so the pair is BASE→HEAD of one pull request and neither end
  can be swapped for a convenient tree.
  (b) the per-severity BEFORE and AFTER vectors, every family and every
  severity, `info` included; and (c) a named reason for EVERY finding that
  entered or left **OR CHANGED SEVERITY**, diffed finding by finding rather than
  netted. A record that gives a total without the vector, or a vector without the
  findings behind a moved count, does not discharge this line.
  **THE "CHANGED SEVERITY" ARM IS NOT BELT-AND-BRACES; WITHOUT IT THE CLAUSE HAS
  A HOLE THE CHECKER ITSELF OPENS** (a Copilot finding on this amendment's own
  pull request, round 13, and it is right in the code):
  `doc_health.Finding.match_key()` is `(self.family, self.repo, self.path)` —
  `scripts/doc_health/__init__.py`, the method of that name (`:187-189` at
  this amendment's ORIGINAL base `cbc3a2c6`) — so SEVERITY is not part of a finding's
  identity.
  **That method's own docstring UNDERSTATES the key it returns, and the
  discrepancy is named here rather than quoted past**: it reads
  *"Regression-rule identity: contract matches by family + path"* while the
  return is `(family, repo, path)` — `repo` is omitted from the sentence and
  present in the tuple. **THE RETURN GOVERNS**, because it is what every
  caller compares: findings from different repositories do NOT collide, and
  the reading below rests on the tuple rather than on the sentence.
  *(A Copilot finding on amendment #4's pull request — review `5226920310`
  at `cbc3a2c6`, which arrived after that head was frozen and was read and
  answered only once #1058 had merged, at comment `5715028704`. It was right
  that the two were set side by side as if they agreed, and wrong that the
  packet mis-quoted: the quotation is verbatim and the tuple was already
  stated first. The imprecision is `doc_health`'s own, is a finding about
  that module, and is raised there rather than repaired from a `tasks.md`.)*
  And the family that exploits that is
  `_honour_grandfather_dispositions` (`scripts/doc_health/families.py`:529, read
  at :1005-1014): a finding whose `(family, repo, path)` carries a dated, cited
  entry in the aggregation's `health/dispositions.yaml` is **reported at `info`
  with the citation quoted — a DOWNGRADE rather than a suppression, on purpose**,
  and the pass is documented as preserving *"its family, its repository and its
  path"* so that *"the key set of `findings` is identical before and after"*
  (:588-593). A finding that moves `critical` → `info` that way ENTERS nothing
  and LEAVES nothing: it shifts two counts in the vector while the entered/left
  diff stays empty, which is exactly a changed vector with no accounting behind
  it. The arm closes that by name. That is the form the house already
  uses where it works — the archived
  `2026-08-25-add-projection-title-uniqueness` § 4.6 (`tasks.md`:315-328) reports
  *"before 5 critical, 5 error, 46 warning, 4 info and after 5 critical, 5 error,
  43 warning, 4 info"* and then names the three warnings that left and what
  closed them — and it is what the three review records of THIS packet did with
  their own zero. Fixing the form is what keeps R-6's relocation from becoming
  the licence to choose an amount after seeing the run.
  *(TWO rounds of this count were wrong and both are recorded rather than
  silently repaired. It claimed "exactly twice" until Copilot review round 1 on
  this amendment's own pull request, and that finding was right: the grep behind
  it was `grep -rn severity *.md` from the packet root, whose glob never entered
  `review/`. The repair then claimed "ten times in six files" and THAT was wrong
  too, for a different and more interesting reason — **a whole-packet count of a
  word is not stable while the prose doing the counting keeps using the word**:
  the corrected paragraph added three further occurrences to `tasks.md` and made
  its own measurement read thirteen the moment it landed. Hence the count is now
  taken OUTSIDE this box, where editing this box cannot move it, and it is stated
  as such. A count that does not reproduce is the same defect this amendment
  corrects in five other boxes; a count that MOVES WHEN YOU WRITE ABOUT IT is a
  different defect, and it is fixed by reframing the measurement rather than by
  running it again.)*)*
  **RESIDUE ROWS ADDED 2026-09-18 BY `tasks.md` AMENDMENT #6, ON RULED Q-P3 (a)**
  (`#656` comment `5728856581`). **The snapshot VALIDATOR is NOT FLOOR PART 4's**
  — `design.md` § D6 (4) asks for equal DIGESTS, and `canonical_bytes` reaches
  no validator, so § 5.5's run is complete without one. **The carve nevertheless
  broke it THREE WAYS, and the three are booked HERE so they are owed to a
  follow-up act with its own claim rather than quietly carried by part 4:**
  **(i)** `openXdox-code`'s `SCHEMAS_DIR` resolves to an ABSENT directory
  (`ROOT / "contracts" / "schemas"`), so as carved the validator cannot run from
  anywhere; **(ii)** `openxdox/snapshot.py`'s `VALIDATOR_RELPATH` names a path
  `openxFactory` SHED at `cc4ae9d3`, so the constant outlived its target;
  **(iii)** `find_validator`'s parent walk ADOPTS an enclosing pre-shed
  checkout — which is `floor37` § 6's defect class, *a reader adopting its
  enclosing tree*, appearing here for the second time in this packet and the
  reason it is worth naming as a class and not as three unrelated bugs.
  Measured by helper actor `floor55` (`attachments/lane-opendox/floor55/
  SCOPING-floor55.md`, `brett-wip` `68cd72cb`). **None of the three moves a box
  in this amendment**, and none of them is a finding against the corpus.
  **(iv) REGISTERED 2026-09-18 BY AMENDMENT #6 ON BRETT HEAP'S WORD, AND
  DELIBERATELY NOT RESOLVED HERE:** the § 8.9 BEFORE baseline
  (`BASELINE-8-9.md`, `brett-wip` `e9588455`) independently flags **two of the
  release bundle's OWN validator files as byte-drifted** against the digest set
  they are members of — `scripts/hermes_runtime_validation/catalog.py` and
  `scripts/hermes_runtime_validation/release.py` — reported by doc-health's
  `release-inventory-drift` against
  `contracts/releases/contract-v4.0.digests.yaml`. The cause is ordinary: the
  bundle froze a digest of each validator at the cut, and those validators'
  sources kept moving afterwards. **This is booked as § 8.9 residue owed to a
  follow-up act with its own claim, and this amendment does not resolve it.**
  It is also NOT a finding against § 8.3 above, and the two readings must not
  be collapsed: clause 3 verifies the tag by reading the HISTORICAL commit
  `ce5c054e`, where `verify-commit` passes against that very inventory,
  whereas this drift is measured against the WORKING TREE as it stands today.
  Both are true at once. Note further that these two files are NOT the three
  `HGR-RELEASE-SURFACE-DRIFT` paths disposed of at § 8.3 (b) — those are
  `contracts/CHANGELOG.md`, `contracts/README.md` and `contracts/manifest.yaml`
  — so the two drift reports are separate residue and neither subsumes the
  other.
  **(v) REGISTERED 2026-09-18 BY AMENDMENT #6, NOT RESOLVED HERE, for the next
  act on that file:** `scripts/validate-sequenced-after.py` states a
  CURRENT-CORPUS claim, **"124 of the 143"** archived rows legitimately carry a
  move date later than their directory's, and the corpus has moved out from
  under it. **Measured at the IMMUTABLE SHA `c2d5ce92`: 128 of
  172** (128 later + 44 equal = 172 archived rows, ledger and archive
  directories aligned 172/172, no row without a directory and no directory
  without a row).
  **In `validate-sequenced-after.py` the live claim lives at THREE sites** —
  `:42` and `:402` carry `124 of … 143`, and `:739` carries `124 rows`. `:739`
  is an argparse **help string**, so it is user-visible CLI text and not merely
  a comment.
  **A CORRECTION THIS ROW OWES ITS OWN READER, AND IT REVERSES AN EARLIER
  CORRECTION MADE HERE.** This paragraph previously claimed FIVE sites, adding
  `:36` and `:396`. **That was wrong and the three first reported were right.**
  Both of those read *"before it was made a gate"* — `:36` *"measured clean
  across all 143 archived rows before it was made a gate"*, `:396` *"measured
  across this corpus before it was made a gate — 143 archived rows, 0
  findings"*. They are **HISTORICAL STATEMENTS BOUND TO A MOMENT**, not
  current-corpus claims, and **renumbering them to 172 would destroy the
  evidence they exist to carry.** Caught by Copilot against head `93ffb197`.
  *(The irony is the point and is left on the page rather than tidied away:
  this row exists to say that a figure bound to a tree is safe and a bare
  figure rots — and its own author then mistook two correctly-bound figures
  for rot and proposed to break them. A dated claim is not a stale claim. The
  next owner must apply that test site by site rather than trusting this
  list.)*
  **AND THAT CENSUS IS ITSELF INCOMPLETE, WHICH IS THIS ROW'S OWN DEFECT
  COMMITTED BY THIS ROW.** It covered ONE FILE. The same current-corpus claim
  also stands elsewhere, **and AMENDMENT #7 SPLITS THE SITES LIVE FROM DATED
  BEFORE ANYONE EDITS THEM** — the distinction this row's own retraction
  established, which the list then failed to apply to itself.
  **LIVE — a bare, UNDATED current-corpus claim, safe to renumber. THERE ARE
  FOUR, AND ALL FOUR ARE OUTSIDE `sequenced_after.py`:**
  `scripts/validate-sequenced-after.py` `:42`, `:402` and `:739`, and
  `tests/sequenced_after/test_sweep.py` **`:2049`** *"124 of this corpus's 143
  archived rows do."* — each verified undated by reading its CONTINUATION line
  as well as its own.
  **DATED, THEREFORE EVIDENCE — DO NOT RENUMBER. `scripts/sequenced_after.py`
  HAS NO LIVE SITE AT ALL; EVERY CURRENT-CORPUS CLAIM IN IT CARRIES A DATE:**
  `:449` (*"as measured 2026-09-18"* on `:450`), `:1598` (*"before it was made a
  gate"*), `:1599` (*"re-measured 2026-09-18"* on `:1600`), `:1607` (*"as
  measured 2026-09-18"* on `:1608`), `:1927` (*"on 2026-09-18"*) and `:1958`
  (*"as measured 2026-09-18"*); plus `validate-sequenced-after.py` `:36` and
  `:396` (*"before it was made a gate"*). Each names its own moment, so each
  records what was true THEN, and rewriting it would destroy the evidence
  rather than refresh it.
  *(THIS ROW HAS NOW GOT THIS RULE WRONG THREE TIMES, and the third time it got
  it wrong WHILE WRITING THE RULE — #6 mis-listed `:36`/`:396`, then
  `:1927`/`:1958`, and #7's own corrected split still put `:449`, `:1599` and
  `:1607` under LIVE. **The mechanism is worth more than the apology: the date
  sits on the CONTINUATION LINE, not on the line carrying the figure**, so a
  line-anchored grep for the number never sees it. The test is not "does this
  LINE name a moment" but "does this SENTENCE name one" — and a sentence here
  routinely spans two lines. Caught by Copilot against `ec5d5144`.)*
  **Every line number here is bound to `507b6233` — an IMMUTABLE SHA, not
  "this amendment's head" — and must be re-derived, not trusted**: this row
  first cited that last site as `:2003`, which by the time it was written held
  `shutil.rmtree(…)` — the locator drifted between the grep and the sentence.
  Corrected on a Copilot finding against head `6061030f`.
  Caught by Copilot against head `47a41ee5` and MEASURED TRUE. **That the
  partially-updated figures disagree with each OTHER (143 beside 171 beside
  172) is the strongest argument in this row**: the corpus has been renumbered
  by hand more than once and drifted again each time. The site list has to be
  complete — across FILES, not one file — before anyone edits it.
  *(ONE FINDING IN THIS FAMILY IS DECLINED, WITH THE MEASUREMENT. A review
  against head `7ac75a4e` reported `archive-date-dispositions.yaml` as carrying
  stale `171` claims at `:43`, `:51` and `:101`. Measured at `507b6233`, it does
  not: the sentence spanning `:42-:43` reads *"159 of this corpus's 172
  directories agree"*, which is CURRENT and correct — quoted whole here
  because the fragment *"172 directories agree"* alone, which is what `:43`
  carries by itself, reads like a different claim;
  `:55` reads *"it moved from 157/171 on 2026-09-18"*, which is explicitly
  PAST-TENSE and is the kind of dated statement that does not rot; and `:51`
  and `:101` carry no such claim at all. That file is therefore NOT part of
  this residue, and saying so is worth as much as the sites that are — a
  register that inherits an unverified site sends its owner to the wrong
  file.)*
  **The next act should NOT simply renumber.** The denominator moved THREE
  TIMES in a single afternoon — 170 at this branch's pre-merge head
  `d323b9b5`, 171 at #1106's head `a96ecb5d` (#1106 comment `5730576589`), 172
  here — because every archive closure adds a row. The numerator held at 128
  throughout, since a closure archived on its own directory's date lands in the
  EQUAL bucket and not the LATER one. So the numerator is roughly stable and
  **the denominator rots by construction**: a fresh pair of literals would be
  wrong again at the next closure, which is how this one reached a drift of 29.
  The durable fix is to derive the figure or bind it to a named tree, and the
  choice belongs to that act with its own claim. **Registered here, not
  resolved, and it moves no box.**
  **(vi) REGISTERED 2026-09-18 BY AMENDMENT #6, NOT RESOLVED HERE, owed to the
  owner of `tests/sequenced_after`:** the `archive-date-vs-commit` arm is
  **HISTORY-SHAPE SENSITIVE**, and INCIDENT 2 at § 6.3 is the demonstration.
  `adding_commits()` picks a directory's adding commit from everything
  REACHABLE FROM THE CHECKOUT'S CURRENT `HEAD` — its one `git log` walk names
  no revision, so it is HEAD-relative and NOT `main`-relative, which makes the
  sensitivity WIDER than first written here: a PR merge ref or any other
  checked-out branch yields a different reachable history. So merging a branch
  that was stacked on a pre-squash
  tip can retro-change an already-landed directory's adding commit and turn a
  correct disposition row STALE without anyone editing the row or the
  directory.
  **Two candidate improvements, neither chosen here:** **(1)** pick the adding
  commit by a **FIRST-PARENT walk** from `main`, so a side branch's commits
  cannot displace the mainline one; or **(2)** disposition by the **(directory,
  adding commit) PAIR**, so a row whose adding commit has been displaced reads
  **SUPERSEDED** rather than STALE — a different instruction to its reader and
  a truer description of what happened to it.
  **Candidate (1) is MEASURED to work on this case**: `d8ff2ec2` is reachable
  from `origin/main` but NOT along its first-parent line, so a first-parent
  walk would still name `3e32d987` and #1106's row would still read valid.
  **That is one case and not a proof of the general rule** — choosing between
  the two candidates, or finding both wrong for some third history shape,
  belongs to that owner's act with its own claim. **Registered, not resolved,
  and it moves no box.**
