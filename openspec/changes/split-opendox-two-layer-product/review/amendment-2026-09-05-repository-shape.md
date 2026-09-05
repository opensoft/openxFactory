# Proposal Amendment: split-opendox-two-layer-product — repository shape

Status: record
Kind: decision record
Decision date: 2026-09-05
Lane: openxfactory-4-opendox-extraction (formerly openxfactory-opendox)
Ruler: Brett Heap (repository owner), in session, lane
`openxfactory-4-opendox-extraction`, session `012WPaY5WyCqq1p46F3Qtd7H`, after
a read of `opensoft/openRepoShape` against this ratified packet.
Ruled: 2026-09-05T14:52Z, verbatim: *"elect the shape for both, follow the pin
chain, no family yet"*.
Ruling URL:
<https://github.com/opensoft/openxFactory/issues/656#issuecomment-5552614170>
Amends: `split-opendox-two-layer-product`, RATIFIED 2026-09-05 (record
`review/ratification-2026-09-05.md`, Brett Heap, *"ratify #666"* at 01:38Z over
head `6935fb8b`), landed on `main` as `ceb6dc9e`.

**THIS IS AN AMENDMENT, NOT A RE-RATIFICATION.** The packet stays ratified; no
ruling in it is reopened; nothing above the amended lines is rewritten. Every
edit this record describes is VISIBLE in the tree as an inline amendment note in
the lifecycle's own form (`docs/document-lifecycle.md`, the `> Amended <date>.`
block), because a ratified record whose text silently changed is a record nobody
can cite.

## What the ruling settles

1. **The shape is elected for BOTH.** `openDox` and `openXdox` are each a
   three-repository `openRepoShape` project: an assembly root plus a `-spec` and
   a `-code` leg. SIX repositories, created by `scaffold-project.py`, PUBLIC and
   Apache-2.0 (RULING Q7 unchanged), the election recorded in each assembly
   root's `project.yaml` — `elected_by: Brett Heap`, `elected_on: 2026-09-05`,
   `reference: docs/project-repo-schema.md`. Descendants are scaffolded the same
   way with a pin on openXdox.
2. **Follow the pin chain.** A `<Domainx><Product>` name classifies as a
   descendant when its declared `neutral_product_pins` REACH the matching
   `open<Product>` through declared links — `codexDox` → `openXdox` → `openDox`.
   The mechanics are openRepoShape's and are authored there
   (`opensoft/openRepoShape`#40); this repository's doctrine sentence is amended
   in the same act.
3. **No family holder yet.** No `Dox` family repository is created. The option
   stays deliberately OPEN.

## What the read found, verified rather than assumed

Every fact below was re-measured in this session against a checkout of
`opensoft/openRepoShape` at `main` `f9ff3f8` and, where it matters, against
`122d729bc0c2f2e0ded0bb61b6b97f49512f613e` — the commit
`contracts/openreposhape-pin.yaml` pins. The commits are named because they are
what a reader can re-run against; the checkout's location on any one machine is
not a fact this record has any business carrying.

- **A project is three repositories.** Assembly root `<Project>` carries
  `project.yaml`, the two legs as submodules, `contracts/{shape,spec,code}-pin.yaml`
  (plus one `<product>-pin.yaml` per `--pin`) and the `validate` gate; the legs
  are `<Project>-spec` and `<Project>-code`. The doctrine is ratified HERE at
  `docs/project-repo-schema.md`; the mechanics live there. **Elective, and it
  confers nothing** — CONFIRMED, and it is why this is an amendment rather than
  a new boundary.
- **`scaffold-project.py` creates the three repositories via `gh repo create`**,
  writes the templates, sets the topic `xf-project-<id>`, writes
  `--pin openProduct@<40 hex>` into `contracts/<product>-pin.yaml` AND the
  manifest's `neutral_product_pins:` in one act, and records `--elected-by`,
  `--elected-on` and `--reference`. CONFIRMED by `--help` and by a `--dry-run`
  run.
- **What it does NOT produce** — CONFIRMED by enumerating `templates/`: no
  LICENSE text anywhere, no `CONTRIBUTING.md`, no `SECURITY.md`, no
  `CODE_OF_CONDUCT.md`, no `.github/CODEOWNERS`, no workflow in either leg (the
  legs get `.gitignore`, `README.md` and one `.gitkeep`), and NO branch-protection
  ruleset — the only ruleset text it emits is `RULESET_HINT`
  (`scripts/shape_materialize.py:150`), advice for the case where an EXISTING
  organisation ruleset refuses the seed push. `tasks.md` § 1.3 now says so item
  by item.
- **`scripts/validate-repository-naming.py --explain openDox openXdox`** → both
  `neutral-product`, each with `also_matches: project-leg/assembly`. CONFIRMED.
  `codexDox` with NO pin reports the descendant form as *a CLAIM: needs a
  declared pin on openDox or openxDox*, resolving to `project-leg / assembly`
  with `also_matches: domain-descendant`. CONFIRMED — this is the defect
  `opensoft/openRepoShape`#40 fixes. (The tool is at
  `scripts/validate-repository-naming.py`, not at the repository root; the
  read this amendment was commissioned from named it at the root.)
- **A CORRECTION TO `opensoft/openRepoShape`#40's OWN ISSUE BODY, measured
  here.** #40 states that `openXdox` *"is never a referent for
  `<Domainx>Dox`"*, so `codexDox` pinning openXdox would classify as a plain
  assembly root. **It does not — it PASSES today**, classifying as
  `domain-descendant` in the `assembly` role. The `naming:` block it writes:

  ```yaml
  naming:
    form: domain-descendant
    role: assembly
    also_matches: [project-leg/assembly]
    descendant_referent: openDox
    referent_declared: true
  ```

  and `templates/assembly-root/scripts/validate-manifest.py` accepts that
  manifest, because the pin file it looks for is
  `contracts/openxdox-pin.yaml`, which the scaffold wrote. **It passes by
  ACCIDENT.**
  `contracts/repository-naming.yaml` admits an x-stem spelling of the referent
  (`also_accepted: openx{product}`, present so `codexFactory` may descend from
  `openxFactory`); the referent test compares CASE-FOLDED; and
  `openXdox`.casefold() equals `openxDox`.casefold(). A pin on the INTEGRATION
  layer therefore satisfies the referent test for the NEUTRAL CORE, and the
  manifest asserts a declared `openDox` referent in a tree that declares no
  openDox pin at all. **The classification is right and the reason it records
  is false**, which is worse than a refusal because nothing surfaces it. This
  does not weaken #40 — it is the argument for it: #40 makes the same
  classification TRUE by naming the chain, and removes a pass that evaporates
  the moment anyone compares spellings exactly. `design.md` § D12 and
  `tasks.md` § 1.10 carry the measurement, and it is disclosed as a comment on
  #40 rather than edited into that issue's body by this lane.
- **CORRECTION TO THE READ THIS AMENDMENT WAS COMMISSIONED FROM.** The brief for
  this PR recorded that the scaffold *"REFUSES `--org opensoft` without an
  override flag"*. It does not: `--org opensoft --project TestThing --dry-run`
  plans three repositories without complaint. **The real refusal is on the
  PROJECT NAME, and there is no override flag at all:**

  ```
  $ python3 scaffold-project.py --org opensoft --project openDox --dry-run
  REFUSED naming-role-mismatch: 'openDox' classifies as neutral-product, not as
  the 'assembly' form of a project leg (the neutral-product form is unambiguous
  by construction, so it needs nothing declared)
  ```

  Identical for `openXdox`, with or without `--pin`, at `main` AND at the pinned
  commit. `accepts_role()` (`scripts/repo_shape.py:956`) admits exactly
  `("project-leg", <role>)` and `("domain-descendant", "assembly")`, and
  `scaffold-project.py:434` raises on anything else. **The ruling's own first
  clause cannot be executed by the tool as it stands.** Filed as
  `opensoft/openRepoShape`#41 and carried in `tasks.md` as the new item § 1.1a.
  Nothing is blocked TODAY, because this packet performs nothing.

## What changed, file by file

| file | before | after |
| --- | --- | --- |
| `proposal.md` header | `Ratified:` … `Lane:` | an `Amended:` line naming the ruling, the verbatim word, the comment id and this record. The `Ratified:` and `Lane:` lines are UNTOUCHED — the lane rename of 12:46Z explicitly does not rewrite records |
| `proposal.md` `code_surface` | *SEVEN repositories, two of which do not exist*; items (1) and (2) each one repository | *ELEVEN repositories, SIX of which do not exist*, with the AMENDED note carrying what it first said; items (1) and (2) rewritten BY LEG — `-code` gets the app and the tests, `-spec` the OpenSpec instance and the requirements (including the corpus-adapter INTERFACE as a declaration), the assembly root the manifest, the pins, the gate, `contracts/manifest.yaml`, `contracts/CHANGELOG.md` and the bundle tag; item (4) three rulesets → seven; item (5) the gitlinks name the ASSEMBLY ROOTS and `project-register.yaml` gains two DERIVED rows |
| `proposal.md` body | RULING Q7 *"both repositories"*; § successors *"the two repositories bootstrapped"*; the wallet-departure row *"ONE new repository \| TWO"*; § Impact *"two new repositories each need a required check"*; § Realization evidence *"both repositories exist"* | each carries an amendment note in place; **nothing was deleted**. Q7's substance is explicitly not reopened |
| `tasks.md` legend + § 1 | two repositories created by hand, items 1.1–1.8 | `[oD]`/`[oXd]` name PROJECTS; § 1 rewritten around the scaffold with the two exact invocations (1.1, 1.2), the blocker (1.1a), what the tool writes vs the hand acts (1.3), posture-file PLACEMENT across six repositories (1.4), six rulesets with EVALUATE→ACTIVE unchanged (1.5), Amendment 3 carrying the six names and the election (1.6), descendant names WITH their leg names and still zero repositories (1.7), 1.8 unmoved, and two NEW items — 1.9 the derived `project-register.yaml` election rows, 1.10 the pin chain and its MEASURED interim (which is not the one #40's body predicts) |
| `tasks.md` §§ 3, 4 | destination paths at "openDox"/"openXdox" | one group note each fixing the leg rule, plus the items that name a path or a tag: 3.2/3.3/3.4/3.5 into `-code`, 3.8 and 4.6 cut in the ASSEMBLY ROOT, 4.1/4.3 into `-code`, 4.2 in the assembly root naming openDox's assembly root and stating the two-pin cost |
| `tasks.md` §§ 5, 7, 8 | 5.1/5.8 pins and gitlinks; § 7 one descendant repository; 8.1/8.7/8.8 counting two | 5.1 and 5.8 name the assembly roots and 5.8 carries 1.9's rows; § 7 is ONE scaffold run producing three thin repositories with `--pin openXdox@<sha>` — **which domain and when is still the open ruling**; 8.1/8.7/8.8 count six |
| `design.md` | R-index of eleven acts + four rulings; § D8's drafted Amendment 3; § D10's bootstrap list | an `Amended:` header line; a **SHAPE** row in the R-index pointing at the new § D12, with a note that it is the first row from a later date; § D8's draft now carries the six names, the election, the leg-suffix rule and the descendants' leg names; § D10 notes the distribution across three repositories; **NEW § D12 — Repository shape**, recording the decision, the three alternatives put and why each was not taken, the pin chain, its dependency on #40 AND the correction to #40's own account of what the tool does today, the second dependency #41, where the manifest and bundle tag live and why, and the cost accepted |
| `design.md` § D11 row 2 | *"No MOVEMENT LOG entry is owed"* | **corrected, and NOT part of the shape ruling.** `tasks.md` § 0.9 already carried the opposite (Copilot round 5, 2026-09-05: the seeding moves TEN rows, so an entry IS owed); D11 was left stale by that correction and the two documents contradicted each other. Fixed with its own amendment note rather than left standing, because this amendment was editing that table anyway and a ratified packet that disagrees with itself is not citable |
| `docs/project-repo-schema.md` | § *A descendant form is a claim…* ending at the `domain-descendant-boundary` paragraph | the original sentence and rule INTACT, with an appended `> Amended 2026-09-05.` note stating the chain rule as ruled, quoting the word, citing #656 and `opensoft/openRepoShape`#40 |
| `README.md` | the change's OpenSpec Records row | *"amended 2026-09-05 (repository shape)"* with the verbatim word and this record's path |
| `review/amendment-2026-09-05-repository-shape.md` | — | this file |

## What did NOT change

- **`tasks.md` groups 2, 5, 6 and 8 are unchanged**, save five lines that were
  wrong only in their COUNT or in which object a pin names: 5.1 (the pins name
  assembly roots), 5.8 (the gitlinks name assembly roots; 1.9's rows land with
  them), 8.1, 8.7 and 8.8. Group 2's seam, group 6's five re-homings and group
  8's four-part floor evidence stand exactly as ratified.
- **The doctrine**: `docs/project-repo-schema.md`'s governing sentence, the
  double pin, the lockstep invariant, the manifest-is-the-source direction and
  the confers-nothing posture are all unchanged; one section gained one note.
- **The 102-row successor map** and its 71 / 16 / 15 split.
- **The seam**: `corpus-adapter-seam`'s four operations plus the two derived
  ones, and RULING DQ-1's adapter staying in `openxFactory`.
- **The four-part floor** (RULED OQ-1) — manifest with per-file digests and a
  CLOSED three-class edit list, summing test counts, the neutral conformance
  corpus, the snapshot-equivalence run.
- **The pin grammar and its direction**: `neutral-product-pin`'s two MODIFIED
  requirements, commit-and-digest never tag, each level declaring only its
  DIRECT upstream. RULING OQ-2 is PRESERVED BY CONSTRUCTION — the chain rule of
  #40 exists precisely so a descendant can pin openXdox and still classify,
  rather than pinning openDox directly to satisfy a validator.
- **The two ADDED and two MODIFIED capabilities**, the one REMOVED, and the
  declared-not-modified list. No spec delta file is touched by this amendment.
- **The naming record** `docs/openxdox-naming.md` — NOT edited, per the packet's
  own rule that Amendment 3 applies at realization (§ 0.7, § 1.6). Only its
  DRAFTED text in `design.md` § D8 grew.

## Cross-repository dependency

**`opensoft/openRepoShape`#40** — *Descendant referent follows the declared pin
chain*: the mechanics of clause 2, authored in that repository under its own
lane. `tasks.md` § 1.10 sequences the descendant work after it and DECIDES the
interim rather than leaving it to whoever hits it — and the interim is the
MEASURED one above, not the one #40's body predicts: a descendant scaffolded
today PASSES as a `domain-descendant` on a case-fold collision between
`openXdox` and the also-accepted referent spelling `openxDox`, recording a
declared `openDox` referent it does not have. The interim is therefore to
scaffold AND record the chain actually relied on
(`naming.referent_chain: [openXdox, openDox]`), so the accidental pass is never
left standing as the explanation; #40 landing later makes the same
classification true and re-reads the same tree with no migration. It does NOT
license a direct `openDox` pin to force the classification.

**`opensoft/openRepoShape`#41** — *a neutral-product name refused as an assembly
root*: filed from this session's own measurement (above). It blocks the FIRST
ACT of `tasks.md` § 1 and nothing else; § 1.1a carries it.

Neither is a dependency of THIS pull request, which performs nothing.

## Sibling-lane disclosure

- **`repo-shape`** owns the `add-project-repo-schema` doctrine arc and is
  `docs/project-repo-schema.md`'s author. **This PR appends ONE amendment note
  to ONE section of that document and edits nothing else in it**, on Brett's
  ruling, keeping the original sentence intact. Disclosed here and in the pull
  request body; if that lane wants the note in its own arc instead, it says so
  and this hunk is dropped.
- **`codex-intake-shape`** holds `opensoft/openRepoShape` PR #37 (README +
  `setup.sh`). Nothing in this PR touches that repository; #40 and #41 are
  issues, and both name it.
- The two openRepoShape issues are CLAIMED for the finding only; their FIXES are
  unclaimed and belong to that repository's lane. The correction above — that
  `codexDox` pinning `openXdox` already classifies as a descendant, on a
  case-fold collision rather than on the chain — is posted as a COMMENT on #40
  by this lane and is not edited into that issue's body: the body is the
  ruler's, and a finding that arrives after it belongs beside it.

## Verification, from this session's own runs at the final tree

Every run below is at the branch head after `git merge origin/main`, whose tip
was `5a8a89a1` ("Merge pull request #683 from
opensoft/change/record-677-ratification") when this record was written.

| check | result |
| --- | --- |
| `openspec validate split-opendox-two-layer-product --strict` | `Change 'split-opendox-two-layer-product' is valid` |
| `openspec validate --all --strict` | `Totals: 93 passed, 0 failed (93 items)` |
| `python3 scripts/proposal-support.py . verify` | `proposal support verification ok` |
| `python3 -m pytest -q tests/sequenced_after` | 162 passed |
| `python3 -m pytest -q tests/doc-health tests/proposal-support` | 1612 passed, 2 subtests passed, 7 warnings |
| `python3 -m pytest -q tests/avatar_client_validator tests/hermes_runtime_contracts tests/notebooklm tests/scope_globs` (the other modules that read `openspec/changes/*/proposal.md`) | green |
| `python3 scripts/validate-sequenced-after.py . --ledger-diff` | `per-change sweep ledger consistent with the corpus (171 rows)` — **NO ledger row is owed**: this amendment adds no change directory, moves no requirement key and changes no row's classification, so `split-opendox-two-layer-product`'s existing row (`moved_by: "#666"`) stands unedited |
| doc-health, `--single-repo`, BASELINE at `origin/main` `5a8a89a1` | 8 critical, 7 error, 30 warning, 13 info |
| doc-health, `--single-repo`, THIS TREE | 8 critical, 7 error, 30 warning, 13 info — **delta ZERO across every family and every severity, info included**. Diffed finding by finding after normalising the `Repo-Identity` prefix each run stamps from its own directory name: 58 findings each side, IDENTICAL. (The seventh error is `bump-openspec-cli-pin-to-1.12/review/ratification-2026-09-05.md — missing status header`, which arrived on `main` with #683 and stands on both sides.) |

The counts moved against the numbers an earlier draft of this record carried
(6 critical, 169 ledger rows, 91 openspec items) because `main` advanced by
eleven commits between the two runs. The table above is the one measured at the tree
this pull request proposes; the DELTA — which is what this amendment owes — is
zero either way.

The full suite is covered by the repository's `pytest-suite` check on the pull
request; the runs above are the targeted ones this amendment's surface can move.
