---
code_surface: none — MEASURED, not assumed, on `main` `16779816`. The delta is requirement prose, and the realization is sentences of ONE governance document, `docs/project-repo-schema.md`, which nothing mechanical reads by these sentences. Evidence: (1) `git grep -n "project-repo-schema.md" -- scripts tests .github contracts` finds path references only — the docstring of `scripts/validate-openreposhape-pin.py`, the pin file's `doctrine:` key (which the validator never reads) and header comment, the register schema's `description` and one comment, and three `contracts/CHANGELOG.md` entries — and none of them reads the heading, the count or any sentence this packet moves; (2) `git grep -n -i "naming-and-the"` finds nothing here, nor on `origin/main` of openRepoShape, codexFactory or the xFactory aggregation, so the heading can change without breaking a link; (3) no test pins this capability's requirement count, scenario count or titles — the files under `tests/` and `.github/` that name `project-repo-schema` cite `add-project-repo-schema` as history and read no requirement text; (4) `docs/project-repo-schema.md` is in neither `contracts/manifest.yaml` nor any `contracts/releases/` inventory. No pin, gitlink, contract, schema, script, test or workflow is edited. Landing this packet is corpus text only: its five files (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and one spec delta) plus its ratification record under `review/`, one README *Active changes* bullet, and the machine-seeded row in `tests/sequenced_after/corpus-ledger.yaml` that every filing owes.
target_release: implemented — the value `release-realization` names for a doc-only change: *"A proposal without the declarations is a doc-only change (`code_surface: none`, `target_release: implemented`) by default"*. No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves and no release tag is owed. The realization of a requirement amendment is its promotion at archive, plus the doctrine sentences `tasks.md` § 5.1 names, so the archive waits on that edit being merged (`tasks.md` § 6).
---

# Proposal: correct-naming-families-count

Status: ratified
Ratified: 2026-10-07T10:43:48Z by Brett Heap (openxFactory operator authority) — in session, verbatim "ratify as recommended when the PR opens" (logged RULED on the lane register at 2026-10-07T09:47:04Z), effective when PR #1266 opened, over its opening head `3bb38c20`; record at review/ratification-2026-10-07.md
Kind: proposal
Proposed: 2026-10-07, in lane `codeXfactory-5`, session
`ed23f049-7e99-4601-8a6d-760b6aeb5f26`.
Origin: Brett Heap's in-session word of 2026-10-07, quoted verbatim below and
recorded in `.openspec.yaml` (`kind: ad_hoc`, unapproved).

**RATIFIED ON 2026-10-07. The next paragraph is kept verbatim as the filing's
record.** It was true at filing and is superseded by the ratification cited
above and recorded under § Ratification record. That ratification settles each
of the three decisions as recommended. It is not a merge word and not a word to
realize anything: the merge rests on Brett Heap's separate merge word
(`tasks.md` 1.2).

**NOTHING HERE IS RATIFIED BY THE AUTHORING LANE, AND NOTHING HERE IS BRETT
HEAP'S RULING BEYOND HIS ONE SENTENCE.** This packet proposes how to correct the
stale naming-families count. The count-free reading, the scope of the
correction and the doctrine wording are put to him for ratification. Held for
Brett Heap's ratification and merge words.

## The word, verbatim

- **2026-10-07**, Brett Heap, in session, first-hand to lane `codeXfactory-5`,
  logged RULED on that lane's register at 2026-10-07T09:45:29Z: *"open an
  OpenSpec change for the four families heading"*.

That sentence authorized AUTHORING and OPENING this proposal. It is not a
ratification and it rules on no design point.

## The defect

Canon says *"The four live naming families SHALL be governed as DATA by the
naming policy of the pinned openRepoShape standard
(`contracts/repository-naming.yaml`)"* (`openspec/specs/project-repo-schema/spec.md:108`).
The ratified doctrine `docs/project-repo-schema.md` heads its section
*"Naming, and the four families"* (`:236`) and says *"The four families are
governed as DATA in the pinned standard's `contracts/repository-naming.yaml`"*
(`:248`).

The pinned policy does not say four. Read at each commit openxFactory has pinned
(`design.md` D1):

| pin | in force from | families declared |
| --- | --- | --- |
| `deacbdc` | 2026-09-02 (#605) | 4 |
| `122d729b` | 2026-09-04 (#650) | 5: the `family` holder added (openRepoShape PR #16) |
| `e9c4827b` | 2026-09-05 (#700) | 5 |
| `1a9fc537` | 2026-10-06 (#1260, landed 2026-10-07 as `f335c077`) | 6: the `workspace` form `<user>-wip` added (openRepoShape PR #86) |

Canon was promoted on 2026-09-03 at `deacbdc`, when "four" was true. It has been
false since the next day. The policy's own header at the pin in force says
*"the six live naming families"*, and no family is marked otherwise
(`design.md` D4).

## Why a change, and why not "six"

Both sentences sit in canon and in a `Status: ratified` document, so neither
moves by an edit. Canon moves through a `## MODIFIED` block, and the doctrine
follows its amendment after ratification.

The count went stale twice in a month, at two pin advances that were each
correct, because canon restates a number the pinned DATA owns. Correcting it to
"six" would repeat the defect at the seventh form. So this packet proposes a
COUNT-FREE reading: the naming families are those the pinned policy declares,
governed there as data, and canon restates neither their number nor their full
list (`design.md` D1). Restating "six" (A1), tying a count to the data with a
test as openRepoShape did for its own prose (A2), and a dated count inside
canon (A3) are recorded and rejected there.

## What changes

**`project-repo-schema`, TWO `## MODIFIED` requirements, titles unchanged, each
restated whole from canon:**

1. ***The naming families are governed by the pinned standard, and a descendant
   form is a claim that needs a declared pin.*** The first sentence becomes
   count-free: *"The naming families SHALL be those the naming policy of the
   pinned openRepoShape standard (`contracts/repository-naming.yaml`) declares,
   governed there as DATA rather than by prose and restated here by neither
   their number nor their full list — among them `open<Product>` neutral
   products, `<X>-Install` installs, `<Domainx><Product>` domain descendants,
   and the project legs above — …"*, with its descendant clause carried word for
   word. One paragraph is added: a family the pinned policy adds or retires
   owes this capability no amendment for its count or its listing. One
   scenario is added: *The pinned policy declares a family no requirement here
   names*. One more sentence is corrected (D2): `<Domainx><Product>` is no longer
   called *"the one family whose membership is not decided by the characters
   alone"*, which the declared-only `family` form made false.
2. ***A project's repositories are named `<Project>`, `<Project>-spec` and
   `<Project>-code`.*** One clause is corrected (D2): the leg suffixes sit apart
   from *"every family the pinned standard's naming policy spells as a CamelCase
   word"*, no longer from *"every other live family, all of which are CamelCase
   words"*, which the lowercase `<user>-wip` form made false.

Three canon units are replaced. Each is declared by a `Removed from canon`
marker in the delta, and every other body sentence and all six promoted
scenarios are carried byte-identically (`tasks.md` § 3.1).

## What does not change

- Every SHALL of both requirements: the families stay governed as DATA by the
  pinned policy; a descendant-shaped name is a descendant only on a declared
  pin; the classification stays offline; the leg names and the topic are
  unchanged.
- The pinned policy, the pin, and every machine key, `kind`, field and family
  id.
- `prefer-triad-project-shape`'s four requirements, which this packet does not
  write (`design.md` D5).
- The historical records that say "four" as records of their day
  (`design.md` D7, `tasks.md` § 3.3).

## What ratification decides

1. **The count-free reading** (`design.md` D1). **RULED: ratified as
   recommended.**
2. **The scope**: the two further sentences that restate a property of the whole
   set (`design.md` D2). **RULED: ratified as recommended.**
3. **The doctrine wording** for the realization, including one informative note
   dated to the pin (`design.md` D3). **RULED: ratified as recommended.**

**No open question is put.** Each item above is a decision with a
recommendation, and `design.md` says, under each, what a different ruling would
change.

## Ratification record

**RATIFIED by Brett Heap**, in session, first-hand to lane `codeXfactory-5`,
verbatim *"ratify as recommended when the PR opens"*. It was given at about
09:46Z and logged RULED on the lane register at 2026-10-07T09:47:04Z, and it
took effect when PR #1266 opened at 2026-10-07T10:43:48Z. It is recorded in
full at [`review/ratification-2026-10-07.md`](review/ratification-2026-10-07.md).
The ratified text is the packet at PR #1266's opening head `3bb38c20`.

| decision | ruled | considered, not adopted |
| --- | --- | --- |
| D1, the naming families are count-free in canon | as recommended, 2026-10-07 | restating "six" (A1); a count tied to the data by a test (A2); a dated count in canon (A3) |
| D2, the correction also reaches the CamelCase sentence and the "one family" sentence | as recommended, 2026-10-07 | confining the packet to the count |
| D3, the doctrine wording, with one informative note dated to the pin | as recommended, 2026-10-07 | no informative note |

**Every ruling is the recommended option, so no delta byte moves.**
`specs/project-repo-schema/spec.md` is byte-identical to the text that was put
to ratification.

**The word ratifies and authorizes nothing further.** It is not a merge word:
the merge rests on Brett Heap's separate merge word (`tasks.md` 1.2). It is
not a word to realize anything: the `tasks.md` § 5.1 doctrine handoff waits on
its own act. Nothing is promoted until the archive (`tasks.md` § 6).

## Ordering

The only other active change with a delta on `project-repo-schema` is
`prefer-triad-project-shape` (ratified 2026-10-06). It writes four other
requirement titles, so no title is written by both packets. Neither antecedent
of `release-realization`'s *Ordered deltas and branch vocabulary* is met, no
`sequenced_after:` is owed, and the two may archive in either order
(`design.md` D5).

## Realization routing — a handoff, not performed here

- **openxFactory, the doctrine** (`tasks.md` § 5.1): `docs/project-repo-schema.md`
  `:236` heading, `:240-242` and `:248-251` restated as `design.md` D3 proposes,
  one informative note dated to the pin, and an `Amended by:` header line. The
  doctrine document is NOT edited in this pull request
  (`design.md` D6).

Nothing is owed in openRepoShape. Its own policy comment carries the second D2
defect, and `design.md` names it for that repository's owner without acting.

## Boundaries this packet holds

- No ratified document, pin, gitlink, contract bundle or release tag moves here.
- No act is taken in openRepoShape or in any other repository.
- No historical record is edited.
- The lane register is not written by this packet.
