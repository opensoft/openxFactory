# Design: correct-naming-families-count

Status: ratified
Ratified by: correct-naming-families-count — 2026-10-07, Brett Heap, "ratify as recommended when the PR opens" (logged RULED on the lane register at 2026-10-07T09:47:04Z), over PR #1266's opening head `3bb38c20` (record `review/ratification-2026-10-07.md`)
Kind: design

**RATIFIED 2026-10-07, as recommended.** Every decision below was ratified as
written, and D1, D2 and D3 were each RULED to their recommendation (marked where
each is put). The paragraphs that follow are kept as filed.

Every decision below is PROPOSED for Brett Heap's ratification. His word of
2026-10-07, *"open an OpenSpec change for the four families heading"*, is the
authority to author and open this packet. It rules on no design point here, and
nothing below says it does. Each decision says what it costs and how a different
ruling would change the text.

**This packet puts NO open question.** Every choice it makes is a decision with
a recommendation (D1-D3), so a ratification "as recommended" settles all of it,
and a different ruling on any one changes the text named under that decision.

## D1 — The reading is count-free, so "four" is not corrected to "six"

**RULED 2026-10-07, as recommended.** Brett Heap, verbatim *"ratify as
recommended when the PR opens"*.

**The measured history.** The naming policy is DATA in openRepoShape's
`contracts/repository-naming.yaml`, and openxFactory reads it at a pin
(`contracts/openreposhape-pin.yaml`, which digests that file per file). Read at
each commit openxFactory has pinned:

| openxFactory pin | in force from | openxFactory PR | families the policy declares | the policy's own header |
| --- | --- | --- | --- | --- |
| `deacbdc` | 2026-09-02 | #605 | 4 | "the four live naming families" |
| `122d729b` | 2026-09-04 | #650 | 5 (`family` added) | "the five live naming families" |
| `e9c4827b` | 2026-09-05 | #700 | 5 | "the five live naming families" |
| `1a9fc537` | 2026-10-06 (landed 2026-10-07 as `f335c077`) | #1260 | 6 (`workspace` added) | "the six live naming families" |

Canon was promoted on 2026-09-03 (`add-project-repo-schema`, archived by PR
#616) while the pin was `deacbdc`, so *"The four live naming families"* was true
the day it entered canon. It went false the next day, at the first pin advance,
and again at the pin advance of 2026-10-06. Nothing in either pin pull request
was wrong: each moved the pin within its own ratified grammar, and the doctrine's
own currency notes say of the first bump that *"Nothing in this doctrine moves
with that bump"*, and of each later one that nothing moves with it either. The sentence that went stale is the one that restated, in canon, a
number the pinned data owns.

**So the proposed reading is count-free.** The requirement says the naming
families are THOSE the pinned policy declares, governed there as data, and
restated here by neither their number nor their full list. It keeps the four
forms its own rules reach (`open<Product>`, `<X>-Install`, `<Domainx><Product>`
and the project legs) as named members, because the rest of the requirement
rules on them, and it adds one paragraph and one scenario saying that a family
the pinned policy adds or retires owes this capability no amendment for its
count or its listing. That makes the doctrine's "nothing moves with this bump"
true of every future pin advance, rather than true until the next form arrives.

**What it costs.** A reader of canon no longer finds the full list in one
place. The doctrine document gives it back as an INFORMATIVE note dated to the
pin (D3), which is the form the doctrine already uses for facts that move with
the pin.

**What a different ruling changes.** A ruling for "six" (A1) rewrites the first
sentence of the second block as *"The six live naming families SHALL be governed
as DATA … — `open<Product>` neutral products, `<X>-Install` installs,
`<Domainx><Product>` domain descendants, the project legs above, `family`
holders and `<user>-wip` workspace repositories — …"*, drops the added
paragraph and scenario, and leaves D2 and D3 as they are, since both of those
sentences are false at the pin either way.

### Alternatives considered and rejected

**A1 — Restate the count as "six".** Rejected. It is the same defect waiting for
the seventh form. The policy grew from four forms to six in under a week
upstream (openRepoShape PR #16 at 2026-09-04T03:01Z, PR #86 at
2026-09-10T13:11Z), and every growth
would again need a governed change of canon before the pin could advance without
making canon false.

**A2 — Keep a count and tie it to the data with a test.** This is what
openRepoShape did for its OWN prose. Its issue #87 found that `docs/handbook.html`
said "five" and "four" and the assembly-root README template said "four" while
the README said "six"; PR #88 (`cbca5b4`, 2026-09-10) corrected them and added
`test_every_naming_families_count_matches_the_policy`, which reads the expected
word from the policy. That works there because the prose and the data change in
one repository, in one commit. Here they do not: canon moves only through an
OpenSpec change, and the data arrives by a pin advance in another repository. A
test tying the two would fail the first pin advance that adds a family, and
would turn a pin bump into a forced amendment of canon. It is also a code
surface, which this packet does not need. Not taken. A guard that refuses ANY
spelled count of the naming families in canon or in the doctrine would fit the
count-free reading. It is named here as a possible successor and is not proposed.

**A3 — A dated count inside canon** (*"six, at the pin `1a9fc537`"*). Rejected.
Canon is normative text. A dated fact there is either normative, and stale at
the next pin, or informative text inside a normative requirement, which nothing
in this capability's promoted text does today. The informative, dated form
belongs in the doctrine document, beside the pin-currency notes that already do
exactly this for the pinned commit (D3).

## D2 — The correction reaches two more sentences that restate the whole set, and goes no further

**RULED 2026-10-07, as recommended.** Brett Heap, verbatim *"ratify as
recommended when the PR opens"*.

Reading the whole naming section against the pin in force found two more
sentences with the same defect: each states a property of the WHOLE set of
families, and each was made false by a family the pinned policy added.

1. **Canon `spec.md:85-88` and doctrine `:240-242`:** the leg suffixes sit *"in a
   different visual class from every other live family, all of which are
   CamelCase words"*. The `workspace` form, `^[a-z0-9]+(?:-[a-z0-9]+)*-wip$`, is
   lowercase and hyphenated, so this has been false since the pin moved to
   `1a9fc537`. The replacement says *"from every family the pinned standard's
   naming policy spells as a CamelCase word"*. That keeps what the sentence is
   for and claims nothing about the rest of the set. The policy's own wording
   for the same point is safe for a different reason: its `project-leg`
   description says *"every family above"*, meaning the families ahead of it in
   precedence, and `workspace` comes after it.
2. **Canon `spec.md:123-126`:** *"`<Domainx><Product>` is the one family whose
   membership is not decided by the characters alone"*. The `family` form is
   `declared_only: true` because, in the policy's words, *"the characters cannot
   tell you"*, so this has been false since the pin moved to `122d729b`. The
   replacement says the descendant form is NOT decided by its characters, its
   form being a claim of descent, *"which is why it carries a referent"*. That
   keeps the reason for the referent and claims nothing about the rest of the
   set. The doctrine's matching sentences (`:258-259`, *"`<Domainx><Product>`
   does not."*) make no uniqueness claim and are true as written, so they are
   not touched.

**Why these two ride in this packet.** Each is the defect this packet exists to
correct, in the same two requirements and the same doctrine section. The
owner's word names that section by its heading. Leaving them would promote two
sentences the authoring lane knows to be false at the pin, in a block that
restates both requirements whole.

**What it does not reach.** Every other mention of a naming family in canon and
in the doctrine was read, and each is true at any pin. A permission derived from
*"a naming family"* is about any family. The scenario titles *"An existing
repository fits no family"* and *"An organisation enforces the naming families"*
state no count. The doctrine's `<user>-wip` mentions (`:173`, `:182`) name one
family the policy does declare. `docs/openxdox-naming.md:176` is scoped to
*"every CamelCase product name this record governs"* and is true as written.

**What a different ruling changes.** A ruling that confines the packet to the
count withdraws the first block (*A project's repositories are named …*) and
restores the second unit of the second block to canon's text, with its marker.
It also drops the matching doctrine edit in `tasks.md` § 5.1.

## D3 — The doctrine wording, proposed for the § 5 realization

**RULED 2026-10-07, as recommended.** Brett Heap, verbatim *"ratify as
recommended when the PR opens"*.

The doctrine document is not edited in this pull request (D6). Its edit is
`tasks.md` § 5.1, and the wording proposed for it is fixed here so the
ratification covers it:

| at | today | proposed |
| --- | --- | --- |
| `:236` heading | `## Naming, and the four families` | `## Naming, and the naming families` |
| `:240-242` | *"…precisely so they sit in a different visual class from every other live family, all of which are CamelCase words."* | *"…precisely so they sit in a different visual class from every family the pinned standard's naming policy spells as a CamelCase word."* |
| `:248-251` | *"The four families are governed as DATA in the pinned standard's `contracts/repository-naming.yaml`, not by this prose: `open<Product>` neutral products, `<X>-Install` installs, `<Domainx><Product>` domain descendants, and the project legs above."* | *"The naming families are the ones the pinned standard's `contracts/repository-naming.yaml` declares, and they are governed there as DATA, not by this prose, which therefore states neither how many there are nor which. Among them are `open<Product>` neutral products, `<X>-Install` installs, `<Domainx><Product>` domain descendants, and the project legs above, which are the families the rules in this section reach."* |
| after `:251`, new | (none) | one INFORMATIVE note dated to the pin, below |
| header | (none) | `Amended by: correct-naming-families-count (ratified <date>, openxFactory PR #<n>)` beside the existing `Amended by:` line |

**The informative note, proposed text** (the realization fills in the pin it
reads, if the pin has moved by then):

> Informative, dated 2026-10-07 to the pin. At the commit
> [`contracts/openreposhape-pin.yaml`](../contracts/openreposhape-pin.yaml)
> names, `1a9fc537bcce…`, the naming policy declares six families: `neutral-product`
> (`open<Product>`), `install` (`<X>-Install`), `domain-descendant`
> (`<Domainx><Product>`, a claim answered by a declared pin), `project-leg`
> (`<Project>`, `<Project>-spec`, `<Project>-code`), `family` (a holder, reported
> only where its `family.yaml` declares it), and `workspace` (`<user>-wip`, one
> person's private index of unfinished work). This list is a reading of the data
> at that pin and governs nothing. The policy at the pin in force is where the
> families are read, and a later pin may declare more or fewer without this
> doctrine moving.

This follows the pin-currency-note precedent the document already uses: the
three `> Amended …` notes under § A project may start before this is ratified
each record a fact that moved with the pin, dated, and each says the PIN FILE
rather than the note is where the fact in force is read.

**No anchor breaks when the heading changes.** `git grep -n -i "naming-and-the"`
finds nothing in openxFactory, and the same search on `origin/main` of
openRepoShape, codexFactory and the xFactory aggregation finds nothing either.

**What a different ruling changes.** Ruling the note out deletes one row of the
table and the note text. The rest of the realization is unchanged.

## D4 — Which families are "live", answered from the data

Canon says *"live"*, so the count-free reading has to be tested against what the
policy calls live. The policy's header calls all six *"the six live naming
families"*, and no family carries a field marking it otherwise. `family` is
`declared_only: true`, which changes WHEN the classifier reports it (only when
the reader declares the question), not whether it is a family. At the pin in
force:

| id | form | precedence | decided by | added upstream | first in openxFactory's pin |
| --- | --- | --- | --- | --- | --- |
| `neutral-product` | `open<Product>` | 1 | its characters | v0, `86bf553` (#1), 2026-09-02 | `deacbdc` |
| `install` | `<X>-Install` | 2 | its characters | v0, `86bf553` (#1) | `deacbdc` |
| `domain-descendant` | `<Domainx><Product>` | 3 | its characters plus a declared pin (the referent; `deacbdc`, #4) | v0, `86bf553` (#1) | `deacbdc` |
| `project-leg` | `<Project>`, `<Project>-spec`, `<Project>-code` | 4 | its characters; the bare assembly root is the residual class | v0, `86bf553` (#1) | `deacbdc` |
| `family` | a bare CamelCase holder name | 5 | declared only, by the holder's `family.yaml` | v0.4, `d0df8d3` (#16), 2026-09-04 UTC | `122d729b` (#650, 2026-09-04) |
| `workspace` | `<user>-wip` | 6 | its characters (lowercase `-wip` suffix) | `3a927a2` (#86), 2026-09-10 | `1a9fc537` (#1260, 2026-10-06) |

Every row was read with `git show <sha>:contracts/repository-naming.yaml` from
openRepoShape. The file is byte-identical at `3a927a2` and `1a9fc537`, and its
sha256 at `1a9fc537`, `a4eebad2…f096a4`, is the digest
`contracts/openreposhape-pin.yaml` records for it.

Under the count-free reading the question "is `family` really live?" never has
to be answered in canon. It is the policy's to answer, and the policy answers
it.

## D5 — Ordering against `prefer-triad-project-shape`: disjoint keys, no declaration owed, either archive order

**The house rule is keyed to the requirement, not the capability.**
`release-realization`, *Ordered deltas and branch vocabulary*, obliges a
proposal *"modifying a requirement already modified by an active ratified
change"*, or one an active change ADDS or RENAMES to, to reference that change
and declare its deltas relative to its outcome, and it holds the archive order
only for such a pair. `document-lifecycle`'s currency requirement defers to that
rule for two writers of one requirement, and the per-change sweep ledger counts
a change as a `co-modifier` at requirement-key granularity.

**The two packets write disjoint keys.** `prefer-triad-project-shape` (active,
ratified 2026-10-06) writes four `project-repo-schema` titles: the MODIFIED
*The project repository schema is elective and confers nothing*, and the ADDED
*A person starting work outside a Triad is advised once, and is never stopped
for it*, *A project's shape is never a review input* and *The advisory is silent
where the shape question is answered or does not arise*. This packet writes two
other titles: *A project's repositories are named `<Project>`, `<Project>-spec`
and `<Project>-code`* and *The naming families are governed by the pinned
standard, and a descendant form is a claim that needs a declared pin*. No title
is in both, so neither antecedent of the ordering rule is met, no
`sequenced_after:` is owed, and the field is left absent, the lawful default.
No `Modified over` marker is owed either, because neither block here names a
title canon does not carry.

**Archive order is free.** If `prefer-triad-project-shape` archives first, it
replaces one requirement and appends three, and leaves both requirements this
packet modifies exactly as they are, so these blocks stay current. If this
packet archives first, it replaces two requirements prefer-triad does not
touch, so prefer-triad's MODIFIED block stays current. (prefer-triad's archive
waits on its § 5.6, so this packet may well archive first.) The two readings
also agree: prefer-triad's third ADDED requirement identifies a `<user>-wip`
repository by *"the naming family openRepoShape's naming policy declares for
it"*, which is the count-free reading already.

**The ledger.** The sanctioned seeder gives this packet's row `active`,
`co-modifier`, `declares: absent`. It is `co-modifier` because both requirement
keys it writes were written by the archived `add-project-repo-schema`, whose row
is already `co-modifier` and does not move (`tasks.md` § 2.4).

## D6 — The doctrine document is not edited in this pull request

This follows `amend-register-act-5b-projection-proof` (proposed `07b72078`,
ratified `5daa96ec`, document realized `0446dece`) and
`prefer-triad-project-shape` (proposed `2ee9ffd8`, ratified `020f2e4f`, doctrine
realized by PR #1254 at `31e0628a`). Editing a `Status: ratified` document
before its amendment is ratified would put an unratified sentence under that
status line. So `docs/project-repo-schema.md` moves only in `tasks.md` § 5.1,
after ratification, with an `Amended by:` header line naming this change.

## D7 — The historical records stay as written

Four records say "four naming families" and are TRUE AS RECORDS: each states
what `add-project-repo-schema` promoted, or what the doctrine said, on the day
it was written. They are left untouched:

- `README.md:7510`, the OpenSpec Records entry for the archived
  `add-project-repo-schema`;
- `contracts/CHANGELOG.md:2002`, the `contract-v3.1` entry describing the
  doctrine as it was cut;
- `ideation/README.md:392`, the pointer recording that change's exit from
  staging;
- `openspec/changes/archive/2026-09-03-add-project-repo-schema/specs/project-repo-schema/spec.md:97`,
  the archived delta, which archived changes never edit.

`contracts/policies/standards-bodies.yaml:1195` (*"the four family listings are
named here instead"*) is about O*NET occupational families (SOC 11, 13, 15 and
27) for the marketing standards body. It is unrelated. The full classification
of every hit is `tasks.md` § 3.3.

## Observed upstream, not acted on

openRepoShape's own policy carries the second D2 defect in a comment. Its
`domain-descendant` block says *"This is the one family here whose membership is
not decided by the characters alone"* (`contracts/repository-naming.yaml:206-207`
at `1a9fc537`), while its `family` block, two forms later, is `declared_only`
because *"the characters cannot tell you"*. The policy's DATA is consistent and
the comment is not. Correcting it is openRepoShape's act, under its own claims.
This packet names it for that repository's owner and acts in no other
repository.
