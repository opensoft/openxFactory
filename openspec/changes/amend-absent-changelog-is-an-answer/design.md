# Design: amend-absent-changelog-is-an-answer

Status: draft
Date: 2026-09-07
Kind: design

## 0. The brief

openxFactory issue **#750**, and the ARCHIVED
`amend-unreadable-read-sibling-scenarios` (PR **#688**, merge `a59d5463`;
archived by **#703**) whose `design.md` **D6** wrote this successor's brief in
as many words:

> **What the successor owes**, so it is not re-derived: split the arm on the
> fact the read already has. A held tip with no readable changelog is an ANSWER
> — no SPENT declaration exists — and the loop should run with no declarations
> rather than be skipped past; a tip that could not be read at all keeps the
> skip. The `THEN` bullet carried here is what that successor amends, and it is
> the reason this packet did not rewrite it.

This document takes that brief, measures it before designing anything, and names
the two decisions worth a veto.

## D0 — the measurement, taken before the design

**THE SHIM, RE-TAKEN RATHER THAN QUOTED.** D6's measurement is reproduced on
this tree, at `origin/main` `d52e6b88` and again on this branch (re-taken at the
fix-round head; the earlier draft quoted `d5a549e4`, two main landings back).
One shim declaring `contract-v2.0`, its tip HELD (`present_commits`), its tag
absent, its first-parent walk declaring the bundle throughout so the distance arm
reaches its error band; the runs differ in ONE seam answer and in nothing else.

| the shim's `contracts/CHANGELOG.md` | at `origin/main` | on this branch |
| --- | --- | --- |
| absent — per-path `None` at a HELD tip, tree LISTS NO SUCH PATH | ONE `Skip`, nothing graded | ONE `error` on `contracts/manifest.yaml` naming the untagged bundle, PLUS one `info` on `contracts/CHANGELOG.md` recording the read |
| present and EMPTY | ONE `error` on `contracts/manifest.yaml` naming the untagged bundle | unchanged — the same ONE `error` |
| below the enforcement floor, no changelog | `[]` | `[]` |
| held tip, tree LISTS AN ENTRY at the path, blob absent | ONE `Skip`, in the HELD words | ONE `Skip`, in words that name the entry and the failed read |
| held tip, tree UNLISTABLE at that path | ONE `Skip`, in the HELD words | ONE `Skip`, saying UNESTABLISHED, and saying the tip is held |
| tip NOT held, no changelog | ONE `Skip` — and it says *"WHICH THIS CLONE HOLDS"*, asserting the opposite of its own condition | ONE `Skip` saying the clone does NOT hold the tip and that a bounded fetch was attempted |

The last three rows are the fix round's addition to this table: `origin/main` has
ONE arm and gives all four held/unheld states ONE answer, so the branch's four
distinct answers are the whole of what this packet does to the read.

The error's words, both sides, byte for byte: *"contract-v2.0 is declared and
has no published annotated tag more than 5 first-parent landings after the
commit that declared it — under the versioning policy it is NOT PUBLISHED, and
its presence in the manifest is not a release"*.

**A DOCUMENT THAT IS NOT THERE AND A DOCUMENT THAT SAYS NOTHING CARRY THE SAME
FACT.** Neither carries a SPENT declaration. One of them was graded and the
other was not, and the one that was not is the one an author can arrange by
deleting a file.

**THE FAMILY OVER THIS REPOSITORY: NO CHANGE, MEASURED.** openxFactory carries a
readable `contracts/CHANGELOG.md` at its published tip, so it never reaches this
arm. `python3 scripts/doc-health.py --single-repo . --family
release-tag-publication` reads the same single `info` — the `contract-v2.6`
SPENT record — before and after, at `0 critical, 0 error, 0 warning, 1 info`.
The whole-repository run's before/after columns are in the pull request; the one
new finding this packet can emit is `info`, so **no `--fail-on error` run that
is green today can turn red**.

**THE ESTATE-WIDE RUN IS NOT TAKEN HERE, AND THE REASON IS MECHANICAL RATHER
THAN AN OMISSION.** `doc-health.py --repo-root` reads every governed submodule
and `obtain_commit` FETCHES into each clone whose published tip is absent — it
writes into checkouts this lane does not own, which is not a read-only
measurement and is not a thing to do from a lane's own workspace. What #612
already measured is cited instead: on the aggregation nightly the commit WAS
fetched and nine of the ten governed repositories carry no
`contracts/manifest.yaml` at all, so they return at the MANIFEST arm long before
this one, and the tenth is this repository. **The expected estate delta is
therefore zero, and if a real untagged bundle at a held tip does exist somewhere,
the findings it receives are the point of this packet and not a regression.**
`tasks.md` § 6.1 names the run as owed at landing.

## D1 — THE VETO POINT: split the arm and grade (A), or keep the skip (B)

**The question.** At the changelog arm the family has a fact it did not have
before #688: the commit is HELD. Two things can be done with it.

**Option A — SPLIT THE ARM ON THAT FACT, AND GRADE.** Where the commit is held
and no readable `contracts/CHANGELOG.md` blob is reachable, the family treats
the read as an ANSWER — no SPENT declaration exists — and runs the `in_scope`
loop with an EMPTY declaration set, so the repository is reported exactly as it
would be with an empty changelog. Where the commit is NOT held, the skip stands.
`read_changelog(None)` already returns an empty read, so the fall-through
invents nothing.

**Option B — KEEP THE SKIP, ADD A DISTINCT REASON CLASS.** Leave the guard where
it is and give the held case its own reason class, so a reader can tell the two
skips apart mechanically rather than by reading prose.

**B's cost, stated plainly, because it is what decides this.** B leaves D6's
suppression EXACTLY where D6 found it. The held-and-absent case would still
return before the loop, an untagged bundle at such a tip would still receive no
finding, and the defect would still be that a file provably not there is treated
as a read that could not be performed. B also spends a packet — a MODIFIED
requirement, a ratification, an archive act — to improve the wording of a report
that is itself the defect. It is cheaper only in the sense that it changes less;
what it buys is a better-labelled silence. **Rejected on that.**

**A's cost, stated too.** A changes which findings an in-scope repository
receives — the reason D6 refused to take it inside a packet whose claim was
"one skip's TEXT". That is exactly why it is a packet of its own, with its own
scenarios, its own severity reading (D2), and its own measurement (D0). The
direction is the conservative one: a `Skip` becomes a grading, and the grading is
the one an empty document already receives, so nothing this family reports today
becomes quieter.

**Decision: option A**, and the veto point is that choice. A veto of A is a veto
of this delta's two bullets, and the packet does not land on it.

## D2 — the retired skip's FACT is re-reported at `info`, and that is separately vetoable

**The question A forces.** `fam_release_tag_publication` turns every
per-repository `Skip` into an `info` whose text is the skip's reason, on purpose:
a skip is *"reported, not dropped"*, because the obligation is per-repository and
a family that only spoke up when EVERY repository skipped would be silent about
nearly all of them. Retire the skip and that record goes with it — and so does
the obligation #688 ratified, that the held case SAY the presence.

**Option D2-a — say nothing.** The bundles are graded; the grading findings name
the bundles and prescribe publishing tags. **Rejected**, and on two counts.
First, it silently drops a ratified obligation: nothing in the report would then
state the presence, and the packet would be retiring #688's rule while claiming
to carry it. Second, it is a worse report. A reader of *"contract-v2.0 is
declared and has no published annotated tag…"* has no way to learn that this
repository carries no changelog at all — which is precisely the document the
SPENT remedy would be written into.

**Option D2-b — carry the fact onto an `info`.** One finding, `info`, on
`contracts/CHANGELOG.md`, gated on there being a bundle in scope, carrying the
words #688 ratified and saying what the family did with them. **Taken.**

- **`info`, so it can redden nothing.** The cut-time release-tag gate refuses on
  `error` and `warning`; `--fail-on error` refuses on `error`. An `info` reaches
  neither.
- **On `contracts/CHANGELOG.md`, not on the manifest.** A finding's identity in
  this capability is `(family, repository, path)`. Every other finding of this
  family lands on `contracts/manifest.yaml`, so a trace landed there would share
  an identity with the grading findings standing beside it and its disappearance
  would be masked by any one of them — the same reasoning that put the SPENT
  `info` on a per-bundle inventory.
- **Gated on `in_scope`.** A repository below the enforcement floor with no
  changelog is answered with silence, exactly as it always was. A permanent
  `info` about a document nobody is obliged to write is how a report teaches its
  readers to stop reading it.
- **AND THE SAME GATE REACHES THE SKIP, WHICH THE AMENDED `THEN` READS OVER
  WITHOUT QUALIFYING** (PR #753 fix round, DISCLOSED rather than fixed). The new
  `THEN` requires a skip *"wherever the document's own absence has not been
  established"*, unconditionally — and a BELOW-FLOOR repository is answered by
  neither: nothing is in scope, so the tree is never consulted and the arm
  returns `[]`. **This reading is PRE-EXISTING and undisturbed.** The promoted
  `THEN` carried the same unconditional MUST over the same `if not in_scope:
  return []`, put there by `declare-spent-bundle-state` on Copilot's PR #584
  round 3 finding and unchanged by this packet, which moves neither the gate nor
  the floor. Recording it rather than widening the delta is the conservative
  act: making the floor exemption explicit in canon is a MODIFIED unit this
  block does not declare, and it would want its own scenario. `tasks.md` § 6.5.
- **Classed `auto-fixable`, not `contested`.** It stops being reported when a
  readable changelog appears at the published tip, which is an ordinary repair
  and not a resolution anybody needs re-raised. The skip-derived `info` this
  replaces is classed the same way.
- **AND IT CLAIMS NO MORE THAN THE PRESENCE GIVES IT** (#688 adversarial review,
  P3, carried rather than re-derived). *"No readable blob came back at this
  path"*, never *"the commit carries no such file"* — a store holding the commit
  AND its trees can still fail to produce the blob. The over-claiming form is
  pinned against NEGATIVELY in the same test.

A veto of D2 removes one finding, one action string and part of one test, and
leaves D1's split standing.

## D3 — no probe is added, and the unfetched branch is KEPT although it is unreachable

**The probe is inherited and complete**, which #688 established and this packet
consumes rather than re-deriving: `obtain_commit` runs before both reads; both
`manifest is None` arms return before the changelog is consulted; `blobs_at`
sends `<commit>:<path>` to `cat-file --batch`, which reports every spec of a
commit the clone does not hold as *missing*. A manifest that READ is therefore
proof the commit is held. **No second probe, no second round trip**, and the
split costs one comparison of a boolean the function already computed.

**So the unfetched branch cannot be reached through `check_repo` on real git —
and it stays.** Deleting it would make that proof load-bearing FOREVER: any
later change to the manifest arm (a cached read, a second source, a manifest
served from a commit other than this tip) would silently convert an unfetched
tip into a graded one, which is the #338 conflation with the safety taken out.
The branch fails closed, costs one comparison, and carries a comment saying it is
unreachable and why it is kept. **It is also the branch the shim-level test
exercises**, `FakeGit`'s object store being pessimistic by default, so it is not
dead code in the suite either.

**The unfetched skip's WORDS do move, and only because its branch narrowed.** It
had #688's held-tip wording — *"WHICH THIS CLONE HOLDS"* — which on the arm where
the commit is NOT held would assert the opposite of its own condition. It now
says the clone does not hold the tip and that a bounded fetch of exactly that
commit was attempted and did not obtain it, which is the manifest arm's own true
words for the same fact. All three substrings the existing suite pins are
carried, so the existing test passes unchanged.

## D3a — THE THIRD STATE IS ESTABLISHED, NOT ASSUMED (Codex, PR #753 round 1, P2)

**The finding, at full strength.** `blobs_at`'s per-path `None` at a HELD commit
still stands for TWO facts: the tree at that commit carries no such path, or the
tree DOES carry it and the blob object is missing or corrupt in this store.
`amend-unreadable-read-sibling-scenarios` named that third state and narrowed its
skip's WORDS because of it — a held commit licenses *"no readable blob came back
at this path"*, never *"the commit carries no such file"*.

**GRADING IS A CLAIM ABOUT THE FILE, WHICH IS WHY THE NARROWING STOPS BEING
ENOUGH.** #688 only had to choose words; this packet acts. Grading a damaged
object store as an absent document would read a REAL SPENT declaration as absent
and answer an EXTINGUISHED obligation with the superseded-and-never-published
`error` — telling an operator to publish a tag whose obligation was extinguished
and which cannot be published. That is a FALSE `error`: it reddens a
`--fail-on error` run and fails the cut-time gate, on a repository whose records
are correct. It is the #338 conflation pointed in the third direction and made
expensive.

**Decision: consult the TREE, once, on that arm alone.** `ls_tree_paths` reads
the tree object rather than the blob, so it answers for exactly the path whose
blob this store cannot produce, and it is asked with the document's own path as
its pathspec. Three outcomes, and only one of them grades:

| what the tree says | the family's answer |
| --- | --- |
| the path is NOT listed | ESTABLISHED absence — grade with no declarations, and record the fact at `info` |
| the path IS listed | the tree lists an ENTRY there and no readable blob came back — KEEP THE SKIP, saying those two facts |
| the listing could not be performed | UNESTABLISHED — KEEP THE SKIP, saying that, and saying that the commit is held |

**AND THE MIDDLE ROW NAMES TWO FACTS RATHER THAN A CAUSE** (PR #753 fix round).
An earlier draft of this row, and of the skip it describes, said *"an object
store that cannot serve what it lists"* — which is a CAUSE, and one this arm
does not check. `ls_tree_paths` runs `ls-tree -r --name-only`, which filters by
NO OBJECT TYPE, so an entry that lists at that path may be a blob this store has
lost OR a GITLINK whose target commit this clone does not hold; measured on a
constructed repository, a submodule at `contracts/CHANGELOG.md` lists exactly as
a blob does while `cat-file --batch` answers `missing` for it. The skip is
therefore worded to the two facts the arm has — the tree lists an entry there,
and no readable blob came back for it — and to the conclusion those two support:
a read that FAILED. Making the listing type-aware instead was considered and
REFUSED: it would widen the seam, and it would buy a distinction this arm does
not act on, since both causes keep the same skip. **THE SKIPS ALSO STATE THE
PRESENCE.** Both of these arms stand BELOW the held-tip split and are unreachable
above it, so both say the tip is one this clone holds — the rule #688 ratified
over the sibling read, applied to the two skips a held tip still emits, so that
neither can be read as the unfetched case's words.

**The cost is one bounded call on an arm this family reaches only where a
changelog did not read at all**, which is a state no repository in this estate is
in. The alternative — grade on the held commit alone — was what the first draft
of this packet did, and it is rejected: it makes the packet's own canon false,
since the amended `AND` forbids asserting a file absence the held commit does not
establish, and grading asserts exactly that.

**THE THIRD BRANCH IS DOMINATED ON REAL GIT, AND IS KEPT FOR THE REASON THE
UNFETCHED ONE IS.** `cut_bundles` lists the tree under `contracts/releases/`
several guards earlier and returns a skip at `cut is None`, so a listing seam
that has failed has ALREADY returned before this arm is reached: only a failure
scoped to THIS ONE PATHSPEC lands on the `listed is None` branch, and real git
produces no such failure. The test's own docstring says so. It is kept for
exactly D3's reason — it costs one comparison, it fails closed, and it is the
only thing standing between an unanswered read and a grading if the listing seam
ever changes — and a reader should not take it for a live state.

**AND THE CANON SAYS IT, RATHER THAN THE CODE SAYING IT ALONE.** The amended
`THEN` keeps the skip *"wherever the document's own absence has not been
established"* and names all three states; the amended `AND` requires the record
to name the tree listing that establishes the absence. The delta's own note
carries the reasoning so a later reader meets it where the rule is.

## D4 — TWO markers, and the self-reference hazard

The block REPLACES two bullets, so under `doc-health`'s *Currency of an active
change's MODIFIED requirement blocks* each dropped canon unit is reported unless
a reserved marker declares it.

**TWO MARKERS AND NOT ONE, AND THE REASON IS THIS REPOSITORY'S OWN AMENDMENT.**
`amend-marker-reason-boundary` (PR #719, archived **#739**) promoted the rule
that a marker's names are the code spans closing BEFORE its first ` — ` standing
OUTSIDE every code span. A single marker naming two units separated by that
sequence would therefore declare only the FIRST and report the second — the
"conservative direction" that amendment deliberately chose.

**AND THE CORPUS'S OWN EXAMPLE SHOWS THE OTHER LAWFUL SHAPE, WHICH IS WHY THIS
IS A CHOICE AND NOT A CONSTRAINT.** Canon's written-out marker at
`openspec/specs/doc-health/spec.md:1778` separates two names with `; `, which
the boundary rule leaves wholly intact — so ONE marker naming both units was
available and would have parsed correctly. It is not taken, and the reason is
that **a marker carries ONE reason and these two removals have DIFFERENT
reasons**: the `THEN` bullet is retired because the skip it requires suppressed a
grading, and the `AND` bullet because it constrains the wording of a skip the
held case no longer emits. Folded into one marker, one of those reasons would
have to be dropped or the two blended into a sentence describing neither
accurately. So each dropped unit gets its own marker paragraph, one code span
each, with its own reason beside it.

**AND NEITHER REASON CARRIES A CODE SPAN**, which is the self-reference hazard.
The predecessors' markers quote `` `WHEN` `` and `` `AND` `` inside their reasons,
and under the RETIRED grammar those quotations became names — the defect #719
was written to fix. Writing both reasons span-free means the retired grammar and
the amended one derive the SAME single name and the SAME reason from each marker
here, so this block's markers read identically to any parser this corpus has had.
**Measured on this branch**: `derive_units` reads FOUR markers over the block —
#678's, #688's and these two — each with exactly ONE name.

Each unit is quoted in a DOUBLE-backtick span with its list marker stripped.
Double rather than single is belt and braces: the retired `AND` bullet contains
no backtick, but a double-backtick span is what both predecessors used and what a
later editor will copy, and CommonMark closes a run of N backticks only on a run
of exactly N. Both markers say the unit is REPLACED rather than deleted, and
name what replaced it.

**#678's and #688's notes and markers are canon units of this requirement now.**
They are carried BYTE-IDENTICAL and are not restated, reworded or merged; this
packet's note is added below them so the three amendments read in the order they
happened.

## D5 — the one existing test that is edited, and why it had to be

`test_an_absent_changelog_says_the_tip_is_held_rather_than_unfetched` asserted
`isinstance(out, Skip)` for the HELD case. That is the report this packet
retires, so the assertion is false under any option that fixes D6 — including
option B's, which would keep a skip but reword it. **There is no version of this
work in which that test survives untouched**, and it is CONVERTED rather than
deleted or weakened: every literal it pinned is re-asserted, unchanged, on the
`info` that now carries them —

- `WHICH THIS CLONE HOLDS`;
- `the commit is held in this store and no readable contracts/CHANGELOG.md blob
  is reachable at it`;
- NOT `a bounded fetch of exactly that commit was attempted and did not obtain
  it`, so the record can never drift into the manifest arm's words;
- NOT `carries no contracts/CHANGELOG.md`, so the tree assertion the read cannot
  support cannot come back;
- `fetch_calls == []`, so the held-tip precondition is proved rather than assumed
  (Copilot, PR #688 round 2);

plus one new negative pin — the record must not carry a skip's own words either,
so nobody grepping the report reads it as an unasked question.

**No other existing test is edited.** The other two changelog tests reach the
UNFETCHED arm, which does not move, and they pass unchanged. Six tests are
ADDED beside them — the D6 pair, the unfetched skip, the floor over the
trace, the two states D3a adds, and the floor over D3a's own two branches — and
the module goes 146 → 152.

**THE MUTATION PROBES, ON ALL THREE GUARDS, RE-TAKEN AT THE FIX-ROUND HEAD** (the
numbers below replace an earlier draft's, which were arithmetic from the
pre-D3a design and were never re-measured after D3a landed):

| the mutation | the result |
| --- | --- |
| revert the held-tip split to `if changelog is None:` | **5 failed, 147 passed** — the converted test, the D6 pair, both D3a third-state tests, and the below-floor third-state test |
| disable D3a's tree consultation (`if False:`) | **3 failed, 149 passed** — both D3a third-state tests and the below-floor third-state test |
| drop `and in_scope` from D3a's tree consultation | **1 failed, 151 passed** — the below-floor third-state test, and it is the ONLY thing that catches it |
| all three restored | **152 passed** |

The third row is why a test was ADDED in this fix round. Before it the mutation
left ALL 151 tests green: the below-floor control ran through `_NoChangelog`
alone, whose tree lists nothing, so it never reached either branch the gate holds
back — and a below-floor repository with a damaged store would have gained a
skip naming an EMPTY set of bundles. The D6 pair is written with a POSITIVE
CONTROL for the same reason: it asserts the empty-changelog run FIRES, so the
equality it checks can never be two empty lists agreeing with each other, and the
new below-floor test carries one too.

## D6 — what this packet does NOT reach

- **The other skips of this family are untouched.** Unlistable refs, an
  unresolvable declaring commit, a whole-batch read failure: each is a question
  that genuinely could not be asked, and whether any of them is an answer wearing
  a question's clothes is a separate reading with its own scenarios.
  `tasks.md` § 6.2.
- **The estate-wide run.** `tasks.md` § 6.1: owed at landing, in an owner-run
  nightly, for the mechanical reason in D0.
- **A LATE SKIP IN THE BUNDLE LOOP STILL DROPS THE TRACE, AND THAT IS DISCLOSED
  RATHER THAN FIXED HERE** (PR #753 fix round). The `info` is APPENDED, and three
  arms below it `return Skip(...)` — unlistable tag refs for a bundle, unlistable
  refs for a named superseding bundle, an unresolvable declaring commit — each of
  which discards `findings` whole. So on those paths the amended `AND`'s *"the
  fact MUST STILL BE RECORDED"* is not honoured. **Measured**: a held tip, a
  bundle in scope, no readable changelog and a tag-ref seam that answers nothing
  returns `Skip("alphaFactory: the published refs for contract-v2.0 could not be
  consulted")`, and the trace appended two lines earlier is gone.
  **The shape is PRE-EXISTING and general, not this arm's.** `check_repo` returns
  `Skip | list[Finding]` and `fam_release_tag_publication` branches on
  `isinstance`, so there is no return in which a skip travels beside findings.
  Every finding the function has already appended dies on those returns today:
  the raw-HTML `error`, every accepted-SPENT `info`, and any LIGHTWEIGHT or
  MISPLACED `error` raised for a bundle the loop reached before the one whose
  refs failed. This packet adds one more finding to that set; it does not create
  the set.
  **Fixing it is a different change.** It means widening `check_repo`'s return
  contract, re-reading `fam_release_tag_publication`'s skip accounting (its
  `len(skips) == len(scoped)` family-level skip is computed from repositories
  that skipped WHOLLY), and deciding what a partial skip MEANS to the cut-time
  gate, which fails closed on any skip. That is a reading with its own scenarios
  over every arm of this family — which is exactly what § 6.2 already declines to
  open — and doing it inside a wording amendment would put a control-flow change
  no scenario describes into a packet whose delta replaces two bullets.
  `tasks.md` § 6.6 names it.
- **The archived deltas that carry the retired bullets.** They are records of
  ratified acts and `promotion-fidelity` compares them against canon; editing one
  would mutate history and manufacture the divergence that family reports.
  `tasks.md` § 6.3.
- **A marker that names something no unit matches is still silent.**
  `suppression`'s third resolution is fail-closed by design and is openxFactory
  **#729**'s subject. Both markers here name units this block genuinely drops,
  and the pull request carries the measurement proving the family read them.
