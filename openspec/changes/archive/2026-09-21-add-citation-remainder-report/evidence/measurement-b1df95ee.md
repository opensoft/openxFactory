# The citation remainder re-measured at `main` `b1df95ee`

**Subject:** openxFactory issue #1053, the `add-declared-former-id` § 6.1 successor.
**Tree measured:** `opensoft/openxFactory` at `b1df95ee80633339907c9e661164a783885a5d30`
(= `origin/main` at 2026-09-16T14:2xZ), in a dedicated clone, working tree clean, nothing committed.
**Instrument:** `measure.py`, run as
`python3 measure.py <clone> --json measurement-b1df95ee.json --classification classification-b1df95ee.json`.
**THE INSTRUMENT IS NOT COMMITTED AND IS NOT IN THIS PULL REQUEST.** It sat
beside this file in the writer's own attachments directory, which is where that
line was written and where it was true; only this READING was vendored into the
packet. The instrument, its run record and the two JSON dumps stand uncommitted
in the repository `opensoft/brett-wip` at
`handoffs/xFactory/attachments/openxfactory-1-2026-09-13/1053/`.
**WHAT A CLEAN CHECKOUT CAN AND CANNOT REPRODUCE WITHOUT IT, STATED PLAINLY
RATHER THAN IMPLIED.** Three different answers, and they are worth keeping
apart. (1) The OUTCOME COUNTS the packet's own `design.md` D0 states at
`b1df95ee` — the file population, the distinct-token count and the five resolver
outcomes — are reproducible from a recipe that is STATED rather than referenced,
and have been reproduced TWICE by independent re-implementations that never read
this instrument: the packet's adversarial verifier, and the bench round's
`recount.py`. (2) The readings THIS file adds on top of those — the
`issue-native` normalization of § 1.2 and the automated cross-repository
set-aside of § 1.3, which are what separate 78 from 81 from 86 and 57 from 78 —
are reproducible from the rules those two sections state, and those sections are
in this committed file rather than only in the instrument. (3) The
CLASSIFICATION in § 5 is a HAND READ, and NO instrument reproduces it — by
design rather than by omission, because `design.md` D4's whole recommendation is
that *never-existed* versus *synthetic*, *self-referential* and the two
file-half repair classes are questions about INTENT that nothing in the tree
answers. What § 5 offers in place of re-execution is an evidence line per token,
quoted at `path:line`, which is what a reader checks a judgment with.
**Control:** the same instrument at `8944758c`, the revision #1053 itself measured.
**Lane:** openxfactory-1 (openXfactory-1), writer `measure-1053`, session 393ade52.

---

## 0. The three headline numbers

| | at `8944758c` (#1053) | at `b1df95ee` (this) |
| --- | --- | --- |
| **INCLUSIVE remainder** (cross-repository citations left in) | 80 | **78** |
| **THIS-TREE-ONLY remainder** (automated qualifier check applied) | 59 | **57** |
| **TRUE in-tree remainder** (manual read of every token) | "about 48" | **39** |

The whole movement between the two columns is one act: PR **#1064** archived
`add-declared-former-id` on 2026-09-16 (§ 4). The methodology is not a source of
difference, and that is proven rather than asserted: run at `8944758c`, this
instrument reproduces **every one of #1053's twelve published figures exactly**
(§ 2.2).

The drop from 57 to 39 is not a repair. It is what a human reading finds the
57 already were: 14 of them are another repository's citations that the
automated adjacency check cannot see, and 4 are artifacts of the token regex
rather than citations at all.

---

## 1. The recipe, and the two steps #1053's prose does not state

### 1.1 What the issue states

1. **File population** — `git ls-files` minus `openspec/changes/archive/`,
   `tests/`, `specs/`. At `8944758c` that is **2979 of 5467** tracked files,
   which is #1053's own count, reproduced exactly. At `b1df95ee` it is
   **2973 of 5466**.

   > **CORRECTION — 2026-09-17, lane `openxfactory-1`, openxFactory PR #1069
   > (Copilot review thread `PRRT_kwDOTAvnrs6jJO-y`). THE COUNTS ABOVE ARE
   > RIGHT AND THE WORD BESIDE THEM IS WRONG. The original sentence is kept
   > rather than replaced, because this file is a RECORD of a measurement
   > taken on 2026-09-16, and what it called its own count is part of that
   > record.**
   >
   > `git ls-files` returns TRACKED ENTRIES, not files: a mode-160000
   > submodule gitlink is an entry with no text, and this tree carries four
   > of them inside every population this file states —
   > `installs/omnigent-install`, `openDox`, `openXdox`, `openXwallet`.
   > RE-MEASURED on both trees (fresh clones, working tree clean, via
   > `git ls-files -s | awk '$1=="160000"'`, both listing the same four
   > paths): so **2979 of 5467** above is 2,979 ENTRIES IN SCOPE of 5,467
   > TRACKED ENTRIES, and the sweep at `8944758c` actually READ **2,975
   > files**; **2973 of 5466** is 2,973 entries in scope of 5,466 tracked
   > entries, and the sweep at `b1df95ee` actually read **2,969 files**.
   >
   > **NO FIGURE THIS FILE MEASURED MOVES.** Neither pair above changes;
   > only the noun beside it does, and only in this note — the sentence
   > above is untouched. `design.md` D3(a) states the same arithmetic
   > (entries in scope = files read + gitlinks skipped, the gitlink count
   > held at 4 at every revision named in this packet); `README.md`'s
   > bullet, `proposal.md`'s comparison table, `tasks.md` § 1.1 and
   > `.openspec.yaml` now all carry the same pair, labelled the same way
   > (this same round).

2. **Token population** — every `openspec/changes/[A-Za-z0-9][A-Za-z0-9._\-/]*`
   match in each population file's text, deduplicated.
3. **Resolution** — each distinct token through the LANDED
   `scripts/packet_reference.py`, loaded by `importlib` exactly as the issue's
   snippet loads it: `PacketIndex(ROOT)` built once, then
   `resolve(ROOT, token, index=index)`; `status`, `half` and `relocated` read
   off the `Resolution` the module itself returns. No rule is re-spelled.

### 1.2 The two unstated steps

Run as its PROSE states it, the recipe gives **593** distinct tokens at
`8944758c`, not the published 578, and every downstream figure moves with it.
Two steps the prose does not mention close the entire gap. #1053 itself warns
its figures come from "a RE-IMPLEMENTATION of M4's stated recipe, not the
authoring script, which was never committed", so this is exactly the kind of
divergence it predicted, found and named:

| step | effect at `8944758c` |
| --- | --- |
| **(i) trailing `.` and `/` stripped before dedup.** The greedy regex captures `openspec/changes/foo/` out of prose and `…/x.md.` off the end of a sentence; counted as spelled, each is a second token for the same citation. | 593 → **578**, the issue's count to the token |
| **(ii) `NOT_A_PACKET_REFERENCE` held OUT of the raw-absent population** rather than counted in its remainder. The issue's own arithmetic requires it: its inclusive table is 153 = 73 + 80 and its this-tree table's 132 = 73 + 54 + 5 + 0 sums without the `NOT_A_PACKET_REFERENCE` row printed beneath it. | 156 → **153** raw-absent, 83 → **80** remainder |

Neither is a defect. (i) is what any path reader does; (ii) is what the
resolver's own fifth answer means — "a path that addresses no packet … is
handed straight back, and the caller's own path resolution is left exactly
where it was". They are named because an unstated step is precisely how two
honest re-implementations of one recipe report two different remainders, which
is what #1053 says happened between M4 and PR #1041.

**`issue-native`** (both steps applied) is therefore this measurement's PRIMARY
reading — it is the only reading under which #1053's published figures
reproduce. **`literal`** (the prose regex, nothing stripped,
`NOT_A_PACKET_REFERENCE` counted in) is computed in the same run and carried
beside it throughout, because the issue's stated words say that, and a
successor CLI must choose one on purpose rather than by accident.

### 1.3 The three choices the issue's prose leaves open

Each was decided once, deterministically, and the alternative is computed and
carried in the JSON:

| choice | taken | alternative | cost of the choice |
| --- | --- | --- | --- |
| a token cited in several places, ONE of them qualified | **ANY occurrence qualified sets it aside** | ALL occurrences qualified | ANY sets aside 22 tokens (#1053's own figure); ALL sets aside 16 and leaves the remainder at 60 rather than 57 |
| what counts as decoration around a prose qualifier | **`validate-pin-registrations.py`'s `_TOKEN_DECORATION` widened by `*` and `_`** (this sweep reads Markdown, where `**codexFactory**` is ordinary) | the house set verbatim | none on this corpus: the two readings agree on every token, at both revisions |
| how "the raw path is absent" is decided | **the resolver's own `_normalised` + `_contained`**, the same pair its `NOT_A_PACKET_REFERENCE`-vs-`DANGLING` branch uses | `(root / token).exists()` | `(root/token).exists()` follows a symlink out of the tree and reads `foo/` and `foo` as two citations |

---

## 2. The INCLUSIVE table

Directly comparable to M4's and PR #1041's own recipe, which does not separate
cross-repository citations out first.

### 2.1 Across all four measurements

| | M4 @ `9378eca5` | PR #1041 @ `701c8fde` | #1053 @ `8944758c` | **this @ `b1df95ee`** |
| --- | --- | --- | --- | --- |
| distinct tokens | not published | not published | 578 | **571** |
| distinct references, raw path absent | 94 | 104 | 153 | **151** |
| of which resolve BY IDENTITY (repaired) | 58 | 64 | 73 | **73** |
| **remainder, unresolved** | **36** | **40** | **80** | **78** |

M4's and PR #1041's figures are quoted from #1053 and were taken by two earlier,
also-uncommitted re-implementations; they are approximately, not exactly,
comparable, as both #1053 and PR #1041 say of their own predecessors. The
`73 → 73` column is the interesting one: the number of citations the archive
relocation broke and the identity rule repairs did not move at all.

> **CORRECTION — 2026-09-17, lane `openxfactory-1`, openxFactory PR #1069
> (Copilot review thread `PRRT_kwDOTAvnrs6jafyB`). THE TABLE ABOVE DID NOT
> NAME ITS OWN READING, AND BESIDE THIS PACKET'S OTHER FIGURES THAT READS AS A
> CONTRADICTION RATHER THAN A DIFFERENT QUESTION. The original table is kept
> rather than replaced, because this file is a RECORD of a measurement taken
> on 2026-09-16.**
>
> § 2.1 above is the **NORMALIZED `issue-native` reading** — trailing `.`/`/`
> stripped before dedup, `NOT_A_PACKET_REFERENCE` held OUT of the raw-absent
> population — the same reading `design.md` D0 names its PRIMARY. The
> identical corpus at `b1df95ee` reads **586/162/81** under this design's own
> recipe reading (the prose regex as written, `DANGLING` + `AMBIGUOUS` only)
> and **586/162/86** under the `literal` reading stated in full at § 2.3
> below. None of the three is wrong; they answer three different questions,
> and this section did not say which one it asked.
>
> **NO FIGURE THIS FILE MEASURED MOVES.** 571/151/78 is unchanged; only the
> label naming its reading is new.

### 2.2 The control: this instrument at #1053's own revision

Run at `8944758c` the instrument reproduces **all twelve** published figures:

| figure | #1053 published | this instrument @ `8944758c` |
| --- | --- | --- |
| distinct tokens | 578 | 578 ✓ |
| raw path absent | 153 | 153 ✓ |
| resolve by identity | 73 | 73 ✓ |
| remainder | 80 | 80 ✓ |
| cross-repo tokens set aside | 22 | 22 ✓ |
| raw-path-missing, this-tree | 132 | 132 ✓ |
| resolves by identity, this-tree | 73 | 73 ✓ |
| DANGLING(identity-half) | 54 | 54 ✓ |
| DANGLING(file-half) | 5 | 5 ✓ |
| AMBIGUOUS | 0 | 0 ✓ |
| remainder total | 59 | 59 ✓ |
| NOT_A_PACKET_REFERENCE | 4 | 4 ✓ |

So every figure in § 2.1 and § 3 that differs from #1053 differs because the
CORPUS moved, and § 4 names the commit that moved it.

One point of arithmetic the reproduction settles: #1053's "removes 22 tokens"
is counted over the WHOLE token population, and only **21** of those 22 sit in
the raw-absent population (the 22nd is a cross-repository citation whose raw
path happens to exist here). That is why 153 − 22 ≠ 132 while 153 − 21 = 132.
Both counts hold at `b1df95ee` unchanged: 22 over all tokens, 21 of the
raw-absent.

### 2.3 The same table under the `literal` reading

| | #1053 @ `8944758c` | literal @ `8944758c` | literal @ `b1df95ee` |
| --- | --- | --- | --- |
| distinct tokens | 578 | 593 | 586 |
| raw path absent | 153 | 164 | 162 |
| resolve by identity | 73 | 76 | 76 |
| remainder | 80 | 88 | 86 |

---

## 3. The THIS-TREE-ONLY table

Cross-repository citations pulled out first by the four automated qualifier
checks #1053 names (a path-joined repository prefix or forge URL; a bare
qualifier word immediately before; the `opsx:opensoft/…` custody-locator
scheme; a trailing `(RepoName)` parenthetical), each evaluated per occurrence
and aggregated to the token.

| | #1053 @ `8944758c` | **this @ `b1df95ee`** | delta |
| --- | --- | --- | --- |
| cross-repo tokens set aside | 22 (21 of the raw-absent) | **22 (21 of the raw-absent)** | 0 |
| raw-path-missing (this-tree only) | 132 | **130** | −2 |
| resolves by identity | 73 | **73** | 0 |
| **remainder** — DANGLING(identity-half) | 54 | **52** | −2 |
| **remainder** — DANGLING(file-half) | 5 | **5** | 0 |
| **remainder** — AMBIGUOUS | 0 | **0** | 0 |
| **remainder total** | **59** | **57** | **−2** |
| NOT_A_PACKET_REFERENCE (self-excluded by the resolver) | 4 | **4** | 0 |

`130 = 73 + 52 + 5 + 0`, and `151 − 21 = 130`. The four
`NOT_A_PACKET_REFERENCE` tokens sit outside both, exactly as in #1053's table.

**AMBIGUOUS is still zero.** No identity in this corpus resolves to two
packets: no duplicate dated archive directory, no live directory beside a
declared former id, no two packets declaring the same former id. That is the
whole `former_ids:` declaration surface reporting clean, and it is the figure
worth watching, because it is the only one of the four outcomes that indicts a
DECLARATION rather than a citation.

The four `NOT_A_PACKET_REFERENCE` tokens are the resolver's fifth answer doing
its job — paths under `openspec/changes/` that address no packet:
`openspec/changes/archive` (the archive directory itself),
`…/archive/proposal.md` (a child of it carrying no archive date), and
`…/archive/2026-09-01-` and `…/archive/2026-09-11-`, two dated names truncated
by the token regex at a `…` ellipsis. Under the `literal` reading the same
debris counts as seven, the two truncations each being a second token with the
ellipsis attached.

---

## 4. Every delta from #1053's counts, explained

Because § 2.2 pins the methodology, the deltas are corpus movement and nothing
else. `git log --oneline 8944758c..HEAD -- openspec/changes/` is 17 commits;
one of them moves every figure:

* **`0b22191a` — "Archive add-declared-former-id on its merged-plus-green
  realization evidence; thirty-one scenarios reach canon"**, landed in PR
  **#1064** (`c7daca4f`), 2026-09-16.

Exactly **eight** distinct tokens left the corpus and **one** arrived
(571 = 578 − 8 + 1), and all nine are that archive:

| token at `8944758c` | was | why it left |
| --- | --- | --- |
| `…/change-r/proposal.md` | **raw-absent, DANGLING** | cited only by `add-declared-former-id/design.md`, whose M1/M2 narrative names its THROWAWAY fixture repo; design.md moved under `openspec/changes/archive/`, which the population excludes |
| `…/change-s/proposal.md` | **raw-absent, DANGLING** | same sentence, same file |
| `…/add-declared-former-id` | raw-present, RESOLVED | cited by its own `proposal.md`, now archived |
| `…/add-declared-former-id/specs` | raw-present, RESOLVED | cited by its own proposal/ratification record, now archived |
| `…/archive/2026-09-09-bump-openspec-cli-pin-to-1.12/specs/neutral-product-pin/spec.md` | raw-present, RESOLVED | the #833 reference M4 quotes, cited by that design.md and proposal.md |
| `…/disposition-codexfactory-declared-renames/design.md` | raw-present, RESOLVED | cited by the same two files |
| `…/add-declared-former-id/proposal.md` | raw-present, RESOLVED | cited by `README.md`, whose OpenSpec Records block was re-spelled to the archive path at the archive |
| `…/add-declared-former-id/review/ratification-2026-09-13.md` | raw-present, RESOLVED | same README block |
| **arrived:** `…/archive/2026-09-15-add-declared-former-id/proposal.md` | raw-present, RESOLVED | the archive spelling the README now carries |

Only the first two were counted anywhere, which is why:

* distinct tokens 578 → 571 (**−7** = −8 + 1);
* raw-absent 153 → 151 (**−2**), the other six having been raw-PRESENT and so
  never in the 153;
* resolve-by-identity 73 → 73 (**0**);
* inclusive remainder 80 → 78, this-tree remainder 59 → 57, identity-half
  54 → 52 (**−2** each, the same two tokens);
* set-aside, file-half, AMBIGUOUS and `NOT_A_PACKET_REFERENCE` all **0**.

#1053 classified `change-r`/`change-s` under *self-referential illustrative
examples*, which is why that class alone falls from 12 to 10 in § 5.

The other 16 commits in the range are amendments, tick-throughs, pre-notes and
two merges inside the packet that archived; none of them adds or removes a
distinct token.

---

## 5. A manual read of all 57

### 5.1 The decision rule, stated so it is repeatable

Each token is classified by the FIRST class its evidence supports, in this
priority order, so that a token satisfying two classes lands in the same one on
a re-read: **cross-repository → tokenization artifact → self-referential
illustrative → synthetic example/fixture → never-existed → renamed before
former-id tracking**, then the three file-half classes for
`DANGLING(file-half)` tokens. *Synthetic* is read SEMANTICALLY (the token is
the subject of an example or fixture artifact, wherever it lives), not by
directory; *never-existed* is reserved for a citation written as a genuine
reference to a packet this repository never had.

### 5.2 The table, beside #1053's

| class | #1053 @ `8944758c` | **this @ `b1df95ee`** |
| --- | --- | --- |
| cross-repository, missed by the automated adjacency check | ≥10 | **14** |
| pure tokenization artifact | 1 | **4** |
| self-referential illustrative example in source/design prose | 12 | **10** |
| synthetic example/fixture id | 17 | **18** |
| ids that never existed as real packets in this repo | 13 | **6** |
| renamed BEFORE this repo tracked former ids | 1 | **1** |
| DANGLING(file-half): nested test fixture outside `tests/` | 2 | **2** |
| DANGLING(file-half): stale draft name, since finalized | 1 | **2** |
| DANGLING(file-half): unclassified | 2 | **0** |
| **total** | **59** | **57** |

**TRUE in-tree remainder = 57 − 14 (another repository's) − 4 (not citations at
all) = 39.** #1053 computed its "about 48" the same way (59 − 10 − 1).

Where this read differs from #1053's, it differs on evidence, and every move is
named:

* `add-composition-drift-cascade`, never-existed → **cross-repo**:
  `docs/governed-reissuance-runbook.md:50` says "(openXwallet PR #3…)".
* `add-pre-archive-citation-gate` ×3, never-existed → **cross-repo**:
  `README.md:1335` reads "Register: OpsxFactory" at the end of the line above,
  and "that is the live path at OpsxFactory main `40aaa93b`" below.
* `add-ideation-governance` ×2, never-existed → **tokenization artifact**: the
  full path on the line is
  `tests/ideation-dashboard/fixtures/base-repo/openspec/changes/add-ideation-governance/proposal.md`,
  which EXISTS in this tree. The citation resolves; only its tail was tokenized.
* `add-invoice-retrieval`, never-existed → **synthetic**: it sits in a worked
  example job-envelope in `docs/workflow-gap-solutions.md` whose sibling keys
  are `id: ledgerlink`, `repo: github.com/opensoft/ledgerlink`.
* `register-gate-rules-council-seats/walk-`, unclassified → **tokenization
  artifact**: all four occurrences are the template placeholder
  `walk-<YYYY-MM-DD>-register-act.md`, and the regex stops at `<`.
* `…/walk-PENDING-register-act.md`, unclassified → **file-half stale draft
  name**: `walk-2026-09-08-register-act.md:274-278` narrates the rename itself
  ("the fill step renamed that file to this one. All 23 now ERROR AT SETUP with
  `FileNotFoundError` on that path").

Both of #1053's unclassified tokens are therefore now classified, and the
cross-repository class is a complete enumeration rather than the "≥10" lower
bound the issue could state.

### 5.3 Every token, with its evidence line

Machine-readable, with `path:line` for every occurrence and the resolver's own
`report` sentence, in `measurement-b1df95ee.json`
(`tokens[].classification` / `.classification_evidence`); the classification
map alone is `classification-b1df95ee.json`. **NEITHER JSON IS COMMITTED** —
both stand with the instrument in `opensoft/brett-wip` at the path the header
names, which is why the enumeration below is given in full here rather than
cited to a file this pull request does not carry. In brief:

**cross-repository, missed by the automated adjacency check (14)** — the check
only reads a qualifier IMMEDIATELY adjacent on the same line:

| token | repository, and where the qualifier actually sits |
| --- | --- |
| `add-composition-drift-cascade` | openXwallet; trailing parenthetical that WRAPS to the next line |
| `add-floor-regeneration-automation/tasks.md` | codexFactory; same line, behind a backtick |
| `add-pre-archive-citation-gate/supporting-docs/owed-findings.md` | OpsxFactory; end of the previous line ("Register: OpsxFactory"), ×6 citations |
| `adopt-bundle-shaped-deliberation/tasks.md` | codexFactory; previous line, and a `git -C codexFactory show origin/main:<path>` locator |
| `adopt-neutral-omnigent-overlay/supporting-docs` | LedgerxFactory; previous comment line, path itself split across two |
| `amend-floor-regeneration-merge-authority/specs/repository-gate-floor/spec.md` | codexFactory; same line, behind a backtick, inside a table cell |
| `archive/2026-07-15-add-github-administration-workflow` | OpsxFactory; "(OpsxFactory)" two lines above |
| `archive/2026-07-22-add-seed-layer-content` | hermes-install; "Realized as hermes-install change" three lines above |
| `archive/2026-08-27-modify-ledgerx-document-estate-warrant-scope/design.md` | LedgerxFactory; NO qualifier anywhere near — the sibling citation in the same EVIDENCE block, `tests/validate_document_estate_surface.py`, is a file this repo does not track at all |
| `archive/2026-08-28-declare-review-holder-composition/design.md` | codexFactory; named in the item heading above AND "at codexFactory `0c7b69ae…`" below |
| `archive/2026-09-07-add-pre-archive-citation-gate` | OpsxFactory; the archive spelling of the same register |
| `archive/2026-09-07-add-pre-archive-citation-gate/supporting-docs/owed-findings.md` | OpsxFactory; ditto, ×4 citations |
| `clarify-gate-rules-decline-position` | codexFactory; "THE RATIFIED PACKET — codexFactory" ending the previous comment line |
| `clarify-gate-rules-decline-position/design.md` | codexFactory; previous line, and once same-line behind a backtick |

**pure tokenization artifact (4)** — the token is not the citation:

| token | what the citation actually is |
| --- | --- |
| `add-ideation-governance/proposal.md` | the tail of `tests/ideation-dashboard/fixtures/base-repo/…/proposal.md`, which exists |
| `add-ideation-governance/tasks.md` | the tail of the same fixture path, which exists |
| `archive/2026-08-27-add-hermes-customer-subject-` | a Python implicit string concatenation split across `pin_class.py:1248-1249`; rejoined, `…-runtime-contract/evidence/provider-verification.yaml` RESOLVES |
| `register-gate-rules-council-seats/walk-` | the template placeholder `walk-<YYYY-MM-DD>-register-act.md`, truncated at `<` |

**self-referential illustrative example (10)** — all ten live only in source
docstrings and comments about the resolution machinery itself:
`2026-09-09-foo`, `README.md`, `add-x`, `archive/2026-09-09-add-x`,
`archive/2026-09-09-change-x`, `archive/2026-09-09-foo`, `change-x`,
`foo/./proposal.md`, `foo/tasks.md`, `x` — in `packet_reference.py`,
`proposal-support.py`, `former_id_arrival.py`, `validate-pin-registrations.py`
and `validate-sequenced-after.py`.

> A by-product worth one line, claimed as an observation and not a defect
> (D4's posture is inherited): `packet_reference.py`'s docstring offers
> `openspec/changes/README.md` as "this corpus's own" canonical
> `NOT_A_PACKET_REFERENCE`, and **that file does not exist in this tree** — so
> the resolver answers `DANGLING(identity)` for its own worked example.

**synthetic example/fixture id (18)** — `add-chain-attestation-t2…t5` (4,
signed-execution-chain tranche-two examples), `neg-neg-lin`,
`neg-neg-lin/review`, `neg-neg-nolin` (3 negative fixtures),
`add-council-clearance-rule-template` ×5 (ideation-dashboard gate-records),
`add-first-feature/design.md`, `billing-self-service/spec.md`,
`archive/2026-07-09-add-doc-health` (a deliberate negative-fit fixture),
`archive/2026-08-21-add-demo-capability` ×2, `add-invoice-retrieval`.

**never existed as a real packet here (6)** —
`add-assembly-plane-separation/{.openspec.yaml,proposal.md}`: two 2026-08-22
alignment reviews of a packet whose own review records "Change is untracked" —
it existed as a worktree draft and was never committed; and
`add-openxfactory-tui-installer/{proposal,tasks,design}.md` and
`specs/tui-installer/spec.md`, a planning questionnaire's forward-looking
sketch. All six return nothing from `git log --all --diff-filter=A`.

**renamed before former-id tracking (1)** —
`prepare-openspec-1.12-readiness`, cited still-dotted at
`scripts/validate-openspec-cli-pin.py:115`; added `552a3a76` (2026-09-05),
renamed to `prepare-openspec-1-12-readiness` by PR #834 on 2026-09-09, four
days before `add-declared-former-id` was ratified, so no `former_ids:`
declaration covers it retroactively. Unchanged from #1053.

**DANGLING(file-half) (5)** — 2 nested test fixtures
(`define-avatar-client-contract-kernel/supporting-docs/x.yaml`,
`qualify-avatar-brokered-call-feasibility/supporting-docs/f0-results.schema.yaml`,
both cited by `experiments/avatar-brokered-call/tests/offline/test_scope_isolation.py`,
which asserts their absence); 2 stale draft names
(`…/gate-rules-council-admitting-record-DRAFT.md`, finalized as
`…-2026-09-10.md` by PR #912; `…/walk-PENDING-register-act.md`, renamed at the
fill step); 1 counted above as a tokenization artifact (`walk-`).

---

## 6. What the CLI should print

From doing the classification by hand, and measured on this corpus rather than
imagined. Feeds design.md D3/D4.

### 6.1 Which classes are MECHANICALLY DECIDABLE, with measured precision

| probe | catches | false positives | verdict |
| --- | --- | --- | --- |
| **`possibly-cross-repo`**: `read_citation`'s own adjacency rule (whitespace-split the LINE, take the word CONTAINING the path, read the word before it, strip decoration) **plus** any repository name in the 3 lines above | **13 of 14** cross-repo tokens | 2 of the other 43 | ship it as an **advisory flag**, never a verdict |
| **synthetic fixture**: every occurrence under `examples/`, `ideation/dashboard/gate-records/` or `contracts/**/examples/` | 17 of 18 | **0** | ship it as a class |
| **tokenization artifact**, three sub-probes: (a) a LONGER path on the same line ends with the token and EXISTS in the tree; (b) the next character is `<`; (c) the token ends the line inside a string literal and the next line opens one, and the rejoined path resolves | **4 of 4** | **0** | ship it as a class — #1053 read this class by hand and found 1 of 4 |
| **self-referential**: every occurrence under `scripts/` | 10 of 12 | 2 (the renamed case and one artifact) | advisory only |
| `half == file` | the 5 file-half tokens | 0 | already free — it is `Resolution.half` |

The single cross-repository citation no adjacency rule can reach is
`archive/2026-08-27-modify-ledgerx-document-estate-warrant-scope/design.md`:
its EVIDENCE block names no repository at all, and the only tell is that a
sibling path in the same block does not exist in this tree. That one is human,
and it is the shape a report should make cheap to check rather than try to
decide.

### 6.2 Which are HUMAN

*never-existed* versus *synthetic* is a question about INTENT (was this written
as a reference, or as an example?) and nothing in the tree answers it —
`add-invoice-retrieval` and `add-openxfactory-tui-installer` are both absent
from history and both live in `docs/`, and only reading the surrounding
sentence separates the worked example from the forward-looking sketch. The two
file-half repair classes (*nested fixture* versus *stale draft name*) are
likewise human: both resolve their packet and neither carries its file, and the
difference is whether a test asserts the absence or a rename left it behind.

### 6.3 What the output should look like

* **Group by CLASS, then by IDENTITY, not by token.** Five of the 57 rows are
  one packet spelled five ways (`add-council-clearance-rule-template`), four are
  one questionnaire's sketch, three are one OpsxFactory register spelled active
  and archived. A flat token list makes one act look like five findings; the 57
  tokens are **38 identities**, twelve of which carry more than one spelling.
* **Columns:** identity · outcome (`DANGLING identity` / `DANGLING file` /
  `AMBIGUOUS`) · citing `path:line` (first, plus a count) · flags
  (`possibly-cross-repo=<repo>`, `synthetic-location`, `tokenization-artifact`)
  · the class where mechanically decided.

  > **CORRECTION — 2026-09-17, lane `openxfactory-1`, openxFactory PR #1069
  > (Copilot review thread `PRRT_kwDOTAvnrs6jafyB`, which names the two
  > bullets above as carrying the same unlabelled-reading issue as § 2.1's
  > table). The original bullets are kept rather than replaced, for the same
  > reason as § 2.1's correction: this file is a RECORD of a measurement
  > taken on 2026-09-16.**
  >
  > The **57** rows and **38** identities above are the **NORMALIZED
  > `issue-native` reading, THIS-TREE-ONLY** (§ 3) — cross-repository
  > citations already set aside, trailing `.`/`/` stripped before dedup. It is
  > not the INCLUSIVE **78** of § 2.1, nor the `literal` **86**, nor this
  > design's own **81** (§ 2.1's correction above reconciles those three); it
  > is the population § 5's hand read classifies. **NO FIGURE THIS FILE
  > MEASURED MOVES** — 57 and 38 are unchanged; only the label naming their
  > reading is new.
* **Print the resolver's own `report` sentence for the first occurrence only.**
  It already names which half failed and why, in the estate's own words, and
  re-writing it in a second voice is how two descriptions of one rule drift.
* **Print the counted rows AND their arithmetic**, so a reader can check
  `raw-missing = by-identity + identity-half + file-half + ambiguous` without
  re-deriving it. A remainder that does not sum is the first sign a reading
  changed.

  > **CORRECTION — 2026-09-16, lane `openxfactory-1`, openxFactory PR #1069
  > (Copilot review thread `PRRT_kwDOTAvnrs6jFQm8`). THE IDENTITY IN THE BULLET
  > ABOVE IS SHORT ONE TERM. The original sentence is kept rather than
  > replaced, because this file is a RECORD of a measurement taken on
  > 2026-09-16 and what it recommended is part of that record.**
  >
  > `by-identity` above is this file's name for the **76** the identity rule
  > REPAIRS. RE-MEASURED, on a fresh clone at this file's own tree
  > `b1df95ee80633339907c9e661164a783885a5d30` (working tree clean), by
  > partitioning the raw-path-absent token set by the resolver's own outcome —
  > which is the one thing the original run did not print:
  >
  > | the token has no raw path, and the resolver answers | tokens |
  > | --- | ---: |
  > | `RESOLVED` — repaired by the identity rule (`by-identity`) | 76 |
  > | `DANGLING`, half `identity` | 74 |
  > | `DANGLING`, half `file` | 7 |
  > | `AMBIGUOUS` | 0 |
  > | `NOT_A_PACKET_REFERENCE` | **5** of the 7 — the other 2 DO have a raw path |
  > | **raw-missing** | **162** |
  >
  > `76 + 74 + 7 + 0 = 157`, and the raw-absent set this file measures is
  > **162** (§ 2.3). The five the four-term identity omits are exactly the
  > NOT_A_PACKET_REFERENCE tokens with no raw path —
  > `openspec/changes/archive/...` (in `scripts/validate-ideation-cross-reference.py`),
  > `openspec/changes/archive/proposal.md` (in `scripts/proposal-support.py`),
  > `openspec/changes/archive/2026-09-01-` (in `README.md`) and
  > `openspec/changes/archive/2026-09-11-` / `openspec/changes/archive/2026-09-11-...`
  > (in `amend-register-act-5b-projection-proof`). A report printing the
  > four-term check would fail it or conceal those five, which is the review's
  > point exactly. The identity a CLI should print is
  > **`raw-missing = repaired + identity-half + file-half + ambiguous +
  > not-a-reference-with-no-raw-path`**; `design.md` D0 and D2 now carry it in
  > that form.
  >
  > **NO FIGURE THIS FILE MEASURED MOVES**, and its own § 2.3 already sums
  > correctly under the five-term reading: the LITERAL remainder at `b1df95ee`
  > is **86 = 74 + 7 + 0 + 5**, and `162 = 76 + 86`. The defect was in the
  > CHECK this section recommends to a future CLI, not in a measurement.
  > Instrument for the re-measurement: `partition.py`, uncommitted, standing
  > with this file's own instrument in `opensoft/brett-wip` at
  > `handoffs/xFactory/attachments/openxfactory-1-2026-09-13/1053/`.
* **State the reading in the header** (dedup normalization; whether
  `NOT_A_PACKET_REFERENCE` is inside or outside the population; ANY-vs-ALL
  qualifier aggregation). § 1.2 exists because #1053 did not, and three
  measurements of one corpus disagreed.
* **`--json` with every occurrence and every flag**, because the manual read is
  where the time goes and it is done in a text editor over the JSON, not over
  the table.
* **Show AMBIGUOUS even when it is zero.** It is the only outcome that indicts
  a `former_ids:` DECLARATION rather than a citation, and a report that omits
  its zero teaches readers not to look for it.
* **Make the history probe OPT-IN.** `git log --all --diff-filter=A` per
  identity is **17.0 of this run's 19.0 seconds** — 90% of the runtime — and it
  returns empty for 51 of the 57, which the resolver already said. It
  distinguishes exactly ONE thing the resolver cannot: an id that stood here
  and was renamed before former-id tracking (`prepare-openspec-1.12-readiness`)
  from one that never stood here at all. Worth a flag, not worth the default.
  Without it the whole sweep is **2.0 seconds** over 2973 files.

  > **CORRECTION — 2026-09-17, lane `openxfactory-1`, openxFactory PR #1069.
  > THE SAME AMBIGUITY AS § 1.1 ABOVE, found by grepping this packet for it
  > while taking Copilot review thread `PRRT_kwDOTAvnrs6jJO-y` rather than
  > flagged here directly. The original sentence is kept rather than
  > replaced, for the same reason as the § 1.1 note: this file is a RECORD
  > of a measurement taken on 2026-09-16.**
  >
  > "2973 files" above is 2,973 TRACKED ENTRIES IN SCOPE (§ 1.1), four of
  > them mode-160000 submodule gitlinks contributing no token; the sweep this
  > bullet times — without the `--history` probe — actually reads
  > **2,969 files**. The 2.0-second figure does not move — it is wall-clock
  > time over the same run this file already measured — only the noun
  > beside the entry count does.

  > **CORRECTION — 2026-09-17, lane `openxfactory-1`, openxFactory PR #1069
  > (Copilot review thread `PRRT_kwDOTAvnrs6jXaNU`). THE BULLET ABOVE NAMES
  > THE PROBE "per identity" AND THEN COUNTS ITS EMPTY RESULT AGAINST 57 — A
  > TOKEN COUNT, NOT AN IDENTITY COUNT. The original sentence is kept rather
  > than replaced, for the same reason as the correction above: this file is
  > a RECORD of a measurement taken on 2026-09-16.**
  >
  > `measure.py`'s history loop (`measure.py:673-698`) iterates the 57
  > remainder tokens but invokes `git log --all --diff-filter=A` only on a
  > cache miss keyed by IDENTITY (`if identity not in seen`); every other
  > token sharing that identity is served the cached `seen[identity]` answer,
  > no second invocation. The probe RUNS per identity, never per token: **38
  > identities, 76 invocations** (a literal-pathspec form and a corrected
  > form, each run once per identity). Re-partitioned directly from
  > `measurement-b1df95ee.json`'s 57 per-token `history` records, grouped by
  > their shared `identity` field — the grouping first checked against the
  > cache's own guarantee: zero mismatches, every token under one identity
  > carries an IDENTICAL `history` value, across all 38 groups — the answer
  > is **empty for 33 of the 38 identities**. Those 33 identities account for
  > EXACTLY the 51 tokens the original sentence counted (33 identities → 51
  > tokens; the other 5 identities → the other 6 tokens; 38 → 57 in total):
  > the two counts are the SAME measurement read on two denominators, not a
  > disagreement between them. The **17.0 of 19.0 seconds — 90%** cost figure
  > does not move and needs no re-timing: it is already wall-clock time over
  > the 38-identity, 76-invocation run the code actually performs, never over
  > 57 token-level invocations that were never made. `design.md` D2 now
  > states the per-identity denominator beside the per-token one.

### 6.4 One correction the issue's own evidence command needs

#1053 states the confirmation as

```
git log --all --diff-filter=A -- "openspec/changes/<id>" "openspec/changes/archive/*-<id>"
```

**Its second pathspec matches nothing, on any input.** Git matches a wildcard
pathspec with wildmatch under `WM_PATHNAME`, where `*` does not cross a `/`, so
`openspec/changes/archive/*-<id>` is tested against full file paths like
`openspec/changes/archive/2026-09-15-<id>/proposal.md` and never matches one.
Proven on a packet known to be archived: `…/archive/*-add-declared-former-id`
returns 0 commits, `…/archive/*-add-declared-former-id/*` returns 1.

The conclusion #1053 drew is nonetheless sound, and this measurement ran both
forms over every remainder identity to be sure: they **agree on all 57**
(`history_forms_disagree: []`). The first pathspec carries the whole signal,
because every archived packet was active first, so the only case the broken
half would have hidden is a packet that appeared in the archive without ever
having been active — and this corpus has none. A CLI should spell it
`…/archive/*-<id>/*`.

---

## 7. What did not reproduce, and what is not claimed

* The token count, and with it every downstream figure, does **not** reproduce
  from #1053's stated prose alone — § 1.2 is that finding, and the two unstated
  steps are the whole of it.
* The `archive/*-<id>` pathspec does not work as the issue describes (§ 6.4).
* `add-composition-drift-cascade`, `add-pre-archive-citation-gate` ×3,
  `add-ideation-governance` ×2, `add-invoice-retrieval` and the two
  `walk-*` tokens are classified differently here than in #1053, on the
  evidence quoted in § 5.2 — eight tokens, no figure in §§ 2–3 affected.
* **Nothing here is claimed as a defect and nothing is repaired.** That is
  `design.md` D4's posture, which #1053 inherits and this measurement inherits
  in turn: *"a reference that resolves owes the citing record no edit"*, and a
  reference that does not resolve owes this instrument nothing but an accurate
  line in a report. No citation in this corpus was edited, and no file of the
  measured tree was changed.
* The cross-repository population is **this tree's to recognize and no other
  repository's to resolve**. The 22 set aside automatically and the 14 found by
  hand are OpsxFactory's, codexFactory's, LedgerxFactory's, openXwallet's and
  hermes-install's records. A sweep of each of those corpora is a separate act
  in each of those repositories.
