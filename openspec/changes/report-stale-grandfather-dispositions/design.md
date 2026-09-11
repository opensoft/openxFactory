# Design: report-stale-grandfather-dispositions

Status: draft
Kind: design

**EVERY DECISION THIS AUTHORING SESSION TOOK IS HERE, WITH ITS ALTERNATIVE AND
THE ALTERNATIVE'S COST.** Brett Heap's word of 2026-09-11 at approximately
18:20Z — verbatim **"usage reset, resume all. read handoff and resume and fan
out wide and do as much as possible in parallel"** — commissioned the authoring
and took none of them.

**D1 IS THE DECLARED VETO POINT AND IT IS PUT AS A MULTIPLE-CHOICE QUESTION**,
recommendation first. D2 through D5 are carried beside it; D2's band sentence
follows D1 and everything else in D2 stands whichever way D1 goes.

## 0. The brief

openxFactory [#965](https://github.com/opensoft/openxFactory/issues/965), filed
by this lane at the archive of
`honour-grandfather-dispositions-in-ratified-provenance` as the successor that
packet's `tasks.md` § 7.1 owes. The landed grandfather pass reads
`health/dispositions.yaml` and downgrades what it MATCHES; nothing reads what
it matched NOTHING. Three of the eighteen entries standing over this family
match nothing today.

## D0 — the measurement, taken before the design

**NOTHING BELOW RESTS ON A NUMBER ANYBODY TYPED, AND EVERY FIGURE CARRIES THE
SHA IT WAS TAKEN AT.** Two aggregation rigs were assembled and the family was
run against the REAL `health/dispositions.yaml` each carries.

**THE FILE, AS IT STANDS.** `opensoft/xFactory` `main`
**`0ecb370e8fec2c1ac78498adf8f6a4ea3ca1c9bb`**: a **49**-entry list across
**nine** families — `ratified-provenance` **18**, `location-conformance` 10,
`proposal-origin` 8, `record-immutability` 5, `modified-block-currency` 4, and
one each of `semantic-contradiction`, `semantic-normative-prose`,
`uncited-resolution` and `document-catalog`. All eighteen of this family's
entries carry a `date` and a non-empty `cite`; **fifteen name `openxFactory`
and three name `codexFactory`**; and **all eighteen name a path under
`openspec/changes/archive/`**.

**RIG A — THE PINS THE AGGREGATION ITSELF HOLDS** (`openxFactory` `b91af6ea`,
`codexFactory` `2dd4e5a3`, materialized under a clone of that aggregation).
`python3 scripts/doc-health.py --repo-root <agg> --family ratified-provenance
--as-of 2026-09-11` → exit 0, *"Findings: 20 critical, 0 error, 0 warning, 15
info"*, 35 rows.

| | entries honoured | matching a finding | matching NOTHING |
| --- | ---: | ---: | ---: |
| `family: ratified-provenance` | 18 | 15 | **3** |

**RIG B — EACH REPOSITORY AT ITS OWN `origin/main`** (`openxFactory`
`8015d45f`, `codexFactory` `dc67ad82`), because the aggregation's `openxFactory`
pin is **233 commits** behind that repository's main at that authoring and a
population that only exists at a lagging pin is not a population. **IDENTICAL:
35 rows, 20 critical / 15 info, 15 matched, 3 unmatched.** The residue is a
fact about the file, not about the pin.

**RIG B, RE-TAKEN AT THE TIPS THIS BRANCH NOW CARRIES.** Both repositories moved
under this packet between the first authoring and the encode, so rig B was
rebuilt rather than carried: `openxFactory` **`c521504c`** (this branch's merge
base; the pin is now **237** commits behind it) and `codexFactory`
**`c3108adc`** (was `dc67ad82`). **IDENTICAL AGAIN: 18 entries honoured, 15
matched, 3 unmatched, the SAME three codexFactory paths, `by repo:
openxFactory 15, codexFactory 3`, `stale by repo: codexFactory 3`, and 18
archived / 0 non-archived.** The run on this branch reports `38 rows, 20
critical / 3 warning / 15 info` — the three `warning` rows being this packet's
own arm, which is the AFTER figure of the table below measured a second time at
a second pair of tips. The aggregation itself is byte-unmoved: `opensoft/xFactory`
`main` is still **`0ecb370e`** at the encode.

**WHY EACH OF THE THREE IS STALE, READ OFF THE RECORD RATHER THAN INFERRED.**
All three are codexFactory's, and all three are stale **by repair** — each
names a `review/ratification-2026-09-05.md` that EXISTS and now carries
`Status: ratified` with a `Ratified:` line naming an approver and a date, so
the citation arm is satisfied and no arm of this family opens a finding
against it:

- `openspec/changes/archive/2026-09-05-add-floor-addition-grace/review/ratification-2026-09-05.md`
- `openspec/changes/archive/2026-09-09-adopt-openspec-cli-pin-gate/review/ratification-2026-09-05.md`
- `openspec/changes/archive/2026-09-09-prepare-openspec-1.12-readiness/review/ratification-2026-09-05.md`

Each entry's own `cite` states the defect it was disposing — *"This archived
packet's `review/ratification-2026-09-05.md` carries `Status: ratified` with no
citation in …"* — and that sentence is now false of all three records. **ZERO
are stale by a VANISHED path** today. The arm reports both shapes because it
cannot tell them apart and does not need to: its predicate is that the entry
matched no finding, and a repaired record and a deleted one produce the same
absence.

**THE FAMILY, BEFORE AND AFTER THE ARM** (rig A, `--family
ratified-provenance`):

| | rows | critical | warning | info |
| --- | ---: | ---: | ---: | ---: |
| before | 35 | 20 | 0 | 15 |
| after | 38 | 20 | **3** | 15 |

- **The whole report diff is 12 lines**, counted rather than characterised: the
  three new rows in each of the TWO places the report renders a finding
  (`## Findings By Family` and `## Ranked Plan`, 3 lines a side), the one
  headline line that sums the bands, and the diff's own hunk markers. **No
  existing row moves** — not a severity, not a rule, not an action, not a
  resolution class.
- The three rows land at **one** `(repo, path)`, `xFactory` :
  `health/dispositions.yaml`, and are distinguished by their RULE, which is
  what a reader prunes by.
- Each row **parses**: `report.plan_line(f, strict=True)` → `report.PLAN_RE`
  matches, `report.unparsed_plan_rows` returns `[]`.

**THE SINGLE-REPO SCOPE IS UNAFFECTED AND THAT IS MEASURED TOO** (§ 5 of
`tasks.md`): `health/dispositions.yaml` lives at the AGGREGATION root and a
`--single-repo` run has `Context.agg_root is None`, so this repository's own
gate reports no row of this class at all.

## D1 — RECOMMENDED: a stale entry is a PRUNE PROMPT, at `warning`

**THIS IS THE DECISION PUT TO BRETT HEAP, AS A MULTIPLE-CHOICE QUESTION, WITH
THE RECOMMENDATION FIRST.** The packet encodes option 1.

### Option 1 — RECOMMENDED: a PRUNE PROMPT. A new finding class, `warning`, against the file

A stale entry is a line of a governance file that has stopped working. The run
reports it at **`warning`** against the AGGREGATION's own
`health/dispositions.yaml` — the file the entry is a line of — naming the
entry's repository and path and quoting the ruling it records, with the action
*"prune the entry, or re-point it at the record that still carries the
defect"*. The file then converges on the set the run reports: every entry
either downgrades a row or is reported as reaching nothing.

- **COST: three `warning` rows today**, and a governance file that acquires a
  standing obligation to be kept current. Whoever prunes an entry is
  performing a small governance act on a file two repositories read.
- **CONSEQUENCE: the disposition file becomes checkable.** Today its only
  evidence of correctness is that somebody once wrote it; after this, the
  report is the evidence, in the artifact a reader is already looking at. And
  `warning` is canon's own word for exactly this: *"drift or first-stage
  aging"* (`doc-health`, *Finding severity and regression handling*). A stale
  entry is drift — true when written, no longer true, nobody's governance
  broken.
- **IT REDS NO GATE AND ENTERS NO COMPARISON.** `--fail-on critical` and
  `--fail-on error` are the two dials that exist; a `warning` trips neither.
  `report.regressions` considers only `critical`/`error` findings and
  `report.parse_previous` admits only those to `keys`, so a stale row can
  never be a regression nor open an issue. This family carries no `contested`
  class, so it never enters `report.uncited_resolutions` either — see D2, where
  that is a decision and not an accident.
- **THE ESTATE HAS ALREADY RULED THIS WAY ONCE, IN A NEIGHBOURING VALIDATOR.**
  `scripts/validate-sequenced-after.py`'s archive-date arm reports *"a
  disposition that names a directory which does not disagree, no longer exists,
  or cites a commit history does not carry"*, on the stated ground that *"a
  stale disposition silences a finding on a fact nobody can check"*, and its
  output tells the author to *"remove any entry reported STALE"*. That is this
  option, in this repository, over a different disposition file — so option 1
  is the estate's existing answer rather than a new one.

### Option 2 — the EXPECTED RESIDUE of a repair, graded `info`, no action

A record being repaired is a GOOD outcome, and an entry left behind is the
harmless trace of one. Report it at `info` with no action, as inventory.

- **COST: the row asks for nothing**, so nothing converges. The file grows
  monotonically: every repair adds an entry that will never be removed, and the
  eighteen become twenty-five and then forty with no reader able to say which
  still do anything.
- **CONSEQUENCE: `info` would then carry two different facts for one family** —
  *"this record is grandfathered"* (the parent's ruling, D1 of the archived
  packet) and *"this entry no longer grandfathers anything"* — and a reader
  counting `info` rows of this family would be counting a union. The parent
  chose `info` precisely so the grandfathered population stayed COUNTABLE; a
  second `info` class un-counts it.
- It is the cheapest option and the one that changes least. If Brett Heap takes
  it, the delta's THEN bullet moves from `warning` to `info`, the action string
  becomes a statement rather than an instruction, and `tasks.md` § 1 records
  the re-authoring.

### Option 3 — an AGGREGATION DEFECT, at `error`

A dispositions file that names a record with nothing wrong with it is a defect
of the aggregation repository, of the same kind as a dangling pin.

- **COST: it punishes the good act.** The three entries are stale BECAUSE
  somebody repaired three records. Grading that `error` means the reward for
  repairing a record is an `error` in tonight's report, and `error` is the band
  that OPENS AN ISSUE: *"a regression — any `critical` or `error` finding not
  present in the previous report … MUST open a single issue per run in the
  aggregation repo"*. Three repairs would have opened an issue.
- **CONSEQUENCE: it would also red a gate.** `--fail-on error` is the dial the
  promotion gate uses; an `error` here makes an aggregation checkout's health
  run fail on a file in the aggregation that no repository's own gate can see
  (`--single-repo` has no aggregation root at all). A blocking finding nobody
  can reproduce in their own gate is the shape this estate has refused before.
- It is the strongest reading and the one to take if the file is to be treated
  as a pinned inventory rather than a ledger of rulings.

**RECOMMENDED: OPTION 1.** The subject is a line in a file somebody can edit
this afternoon, which is what separates it from the parent's subject — an
IMMUTABLE archived record — and is why the two get different bands. Option 3
grades a repair as a defect; option 2 records a fact and asks for nothing.

## D2 — the arm: a SECOND last pass, after the first

**RECOMMENDED: `fam_ratified_provenance` ends `graded =
_honour_grandfather_dispositions(ctx, findings); return graded +
_stale_grandfather_dispositions(ctx, graded)`.**

**WHERE IT RUNS, AND WHY AFTER.** The downgrade consumes the matches; this pass
reports the complement. Taking the difference AFTER is safe because of what the
downgrade PRESERVES: the promoted scenario requires a grandfathered finding to
keep *"its family, its repository and its path"*, so the key set of the finding
list is identical on both sides of it. `tasks.md` § 4 asserts that — the same
difference taken over the UNGRADED list returns the same rows — rather than
leaving it as a reading of canon.

**HOW IT GETS THE UNMATCHED SET.** `set(_grandfather_cites(ctx))` minus
`{(f.repo, f.path) for f in findings}`. `_grandfather_cites` is the map the
downgrade itself reads, which is the whole point: ONE admission rule serves
both halves, so an entry that would not have downgraded anything is not counted
as residue either. A second rule written here is exactly how a file comes to
have two readers that disagree about which of its entries are live — the drift
the parent's D3 refused, one level down.

**TWO NARROWINGS, EACH MEASURED.**

1. **A repository the run did not enumerate is passed over in silence.**
   `ctx.repo_paths` is what `corpus.discover_repos` actually found; an
   aggregation checkout with a submodule unmaterialized reports nothing for
   that repository, so every entry naming it would fall out of the difference
   and be reported stale on the strength of a measurement nobody took. Today
   that is not hypothetical: the three stale entries are codexFactory's, and a
   run that did not materialize codexFactory would report them stale for the
   wrong reason and the fifteen openxFactory ones as well.
2. **A `--single-repo` run reports nothing of this class**, inherited exactly as
   the downgrade inherits it — `_grandfather_cites` returns `{}` where there is
   no aggregation root. **This is the parent's pinned asymmetry, and it is
   pinned again here rather than quietly widened**; whether a run whose job is
   to report THIS repository's own defects should consult another repository's
   disposition file at all is
   [#968](https://github.com/opensoft/openxFactory/issues/968)'s open question.

**THE SUBJECT IS THE ENTRY, SO THE ROW LANDS ON THE FILE.** The record the
entry names is fine — that is the whole point — so a row against the record's
path would name a document with nothing wrong with it, and would collide in the
report with the `critical` row that document draws when it is NOT fine. The
defect is a line of the aggregation's `health/dispositions.yaml`, and that is
where the row goes, under the repository id **`xFactory`**. That id is the
estate's existing spelling and not a new one: `fam_submodule_pin_drift` and
`fam_notebook_projection_drift` already report under it and
`ideation_routing` already resolves it as a known repository id. **The
alternative considered and rejected** was a synthetic slug (`(stale
dispositions)`); issue #474's live case was exactly such a label in the path
slot, and `report.plan_line` now refuses one.

**THE RESOLUTION CLASS STAYS `auto-fixable`, AND THAT IS A DECISION.**
`ratified-provenance` is absent from `families.FAMILY_RESOLUTION`, so its
findings are `auto-fixable` by default and the new row needs no per-finding
`resolution=`. Making this one row `contested` would arm
`report.uncited_resolutions`: a contested finding that stops appearing without
a recorded disposition is re-emitted as an `error` naming it — so the moment
the lifecycle owner PRUNED the entry, doing exactly what the row asked, the
next nightly would raise an `error` unless a disposition entry were added to
the very file the row asked to prune. **A rule whose compliance manufactures an
error is not a rule.** Pruning an entry that reaches nothing arbitrates
nothing, reverses no gate decision, and changes no deliberately-set state that
is still doing anything, which is the `contested` test as canon writes it.

**ONE ROW PER ENTRY, AT ONE KEY.** Two stale entries are two rows at the same
`(family, repo, path)`. `Finding.match_key()` collapses them to one regression
key — which costs nothing, a `warning` never entering that comparison — and
`Finding.sort_key()` includes the rule, so the rows are ordered and rendered
distinctly. The target is written into the RULE rather than the path for that
reason: the path slot is the subject, and the subject is one file.

**ONE EXISTING TEST'S PINNED BEHAVIOUR IS DELIBERATELY OVERTURNED, AND IT IS
NAMED HERE RATHER THAN DISCOVERED IN REVIEW.**
`test_a_run_with_no_findings_reads_no_file` asserted that a CLEAN corpus never
opens the dispositions file. That was true only while nothing read the entries
that match NOTHING; a clean corpus is the EXTREME case of this class — every
honoured entry matches nothing — so a run with no findings now reads the file
and reports every in-scope entry. The downgrade pass's own early return is
unmoved and is asserted directly instead; `tasks.md` § 4.4 carries both halves.

## D3 — the tests extend the parent's rig rather than opening a new file

**RECOMMENDED: `tests/doc-health/test_grandfather_dispositions.py`, twelve
tests added.**

One mechanism, one home. That file already owns the fixtures this class needs —
`_entry`, `_dispositions`, `_ctx`, `_run` — and already reads the same file
under the same admission rule, so a second file would duplicate four helpers
and split one subject across two places. The added block carries its own
section banner and its own constants (`CLEAN_TEXT`, `OTHER_ARCHIVED`,
`VANISHED`) so the two halves stay legible apart.

**THE TWELVE, BY SUBJECT.** The two shapes of the class (stale by REPAIR, stale
by VANISHED path); the negative case (an entry that matched); the extreme (a
clean corpus makes every in-scope entry stale); the two narrowings (a repository
out of scope; a `--single-repo` run); malformed input unchanged (a scalar-root
file and an unhashable `repo`/`path`, both refused one level up); the admission
rule shared with the downgrade (undated, uncited, blank-cite and other-family
entries are not residue); the D2 boundary not overlapping this class (an ACTIVE
path whose finding stands is not stale); composition (the second pass returns
only its own rows, asserted by identity over the rows that pass through); and
the row's own grammar (`plan_line(strict=True)` parses, `parse_previous` yields
no key and no contested key, and a target spelled across two lines is collapsed
to one).

**MEASURED, BEFORE AND AFTER.** `grep -c '^def test_'` on that file: **22** on
`origin/main` `8015d45f`, **34** on this branch. `pytest
tests/doc-health/test_grandfather_dispositions.py -q` → **34 passed, exit 0**.
The whole-directory figures and the control run are in `tasks.md` § 5.

## D4 — `code_surface` is non-empty, so the archive waits for realization evidence

**RECOMMENDED: realize in this pull request; archive on merged-plus-green, at
canon's grain.**

`release-realization`, *Realization archive gate*:

> A change with a non-empty code surface SHALL NOT archive until realization
> evidence exists: its code merged on the implemented target through the owning
> domain's engineering gates, and — where the surface is runnable — a green run
> of that surface.

So this packet archives on **this pull request merged into `main` plus a green
`pytest-suite` run at the tree that merge carries** — the grain this estate has
already had a review blocked on: main's post-merge run is cancelled by the next
landing, so the citable evidence is the pull request's own green run on
`refs/pull/N/merge` together with proof that the merge commit's tree is the
tree that ran. `tasks.md` § 6 is entirely open and openxFactory #965 closes
THERE, by a closing keyword written in the archive pull request and in no commit
message on this branch.

## D5 — THE LIMIT: this rules `ratified-provenance`'s entries and nothing else

**RECOMMENDED: one family, and the other eight named rather than swept.**

At `0ecb370e` the file carries **31 entries for the other EIGHT families** —
`location-conformance` 10, `proposal-origin` 8, `record-immutability` 5,
`modified-block-currency` 4, and one each of `semantic-contradiction`,
`semantic-normative-prose`, `uncited-resolution` and `document-catalog`.
Whether any of THOSE should be read for staleness — and for four of them,
whether their entries are read at all — is a question about a different
subject, with a different population and a different set of readers, and it is
[#966](https://github.com/opensoft/openxFactory/issues/966)'s. Answering it here
would widen a single-family remedy into an unruled sweep of a file two
repositories read.

The arm is narrow by construction and not by convention: `_grandfather_cites`
asks `promotion_fidelity.load_dispositions(ctx, "ratified-provenance")` for its
key set, so an entry naming another family is not in the map this pass takes the
complement of, and cannot be reported by it however the file grows.

**#966 IS NO LONGER UNCLAIMED, AND ITS PACKET DOES NOT COLLIDE WITH THIS ONE —
READ OFF ITS BRANCH RATHER THAN ASSUMED.** `decide-disposition-reading-per-family`
(openxFactory PR [#978](https://github.com/opensoft/openxFactory/pull/978),
DRAFT, branch `change/decide-disposition-reading-per-family` at `59fb2047`)
was authored in parallel with this packet. It carries a `## MODIFIED` block
over **one requirement, and it is a DIFFERENT one** — *Finding severity and
regression handling* (canon line 198) against this packet's *Governed corpus
membership and the lifecycle scan set* (canon line 878). The two deltas
therefore write disjoint bytes of `openspec/specs/doc-health/spec.md` and
neither sequences after the other. **NO `sequenced_after:` IS DECLARED**, and
that is a rule rather than a convenience: a `sequenced_after:` target names a
change that exists on `main`, and #978's packet exists only on its own branch
at this authoring — declaring a branch-only parent would pin this packet to a
directory no validator on `main` can resolve. If #978 lands first, nothing here
moves; if this packet lands first, nothing there moves.

**THE ONE PLACE THE TWO TOUCH IS A CITATION, AND IT IS UNMOVED IN BOTH.** D1
above leans on canon's band vocabulary — `warning` as *"drift or first-stage
aging"* — which lives in the requirement #978 modifies. #978's block copies
that body paragraph byte for byte and appends one scenario (*A recorded
disposition names a family this capability gives no reading*); the band
sentence is not edited, so the ground D1 stands on is the same ground either
side of that landing. The two packets are complementary halves of one file's
reading: #978 rules what an entry naming a family with NO declared reading
does, and this packet rules what an entry naming ratified-provenance — a family
that HAS one — does when it reaches nothing. #978's own block says so in terms:
*"a family for which this capability DOES declare a disposition reading MUST be
read exactly as its own declaration says, this scenario neither widening nor
narrowing any of them."*

## D6 — the sibling search, pasted

Performed 2026-09-11 before authoring, on the lane-collision protocol's
claim-before-author rule, and recorded on #965 at the claim
(`issuecomment-5638957318`); **RE-RUN at `origin/main` `c521504c` when this
branch took that merge**, with the result recorded at the end of this section:

```text
$ gh api /repos/opensoft/openxFactory/pulls --jq '.[] | "#\(.number) \(.head.ref)"'
#974 change/ratify-amend-kill-switch-to-declared-test-companion
#963 change/gate-realization-axis-vocabulary
#962 change/rule-inherited-unit-naming-marker-spent
#888 doc-health/derive-possibles
#594 rescue/worker-fleet-health-monitoring
#518 docs/add-usage-controlled-evidence-chain

$ for n in <each>; do gh api .../pulls/$n/files --paginate --jq '.[].filename' \
      | grep -E 'doc_health|doc-health'; done
#962: openspec/changes/rule-inherited-unit-naming-marker-spent/specs/doc-health/spec.md
      tests/doc-health/test_modified_block_currency_self_gate.py
      (its MODIFIED block is "Currency of an active change's MODIFIED
       requirement blocks" — a DIFFERENT requirement)
(no other open pull request touches scripts/doc_health/ or openspec/specs/doc-health/)

$ grep -l 'Governed corpus membership and the lifecycle scan set' \
      openspec/changes/*/specs/doc-health/spec.md
(no output — NO active change writes this requirement)

$ ls -d openspec/changes/*/specs/doc-health
add-nightly-dashboard-refresh   (7 ADDED requirements, none this one)
settle-aging-staging-topics     (1 MODIFIED: "Aging threshold defaults")
```

**`sequenced_after: []`, AND THE PARENT IS WHY THAT IS CORRECT RATHER THAN AN
OMISSION.** The change whose text this block builds on —
`honour-grandfather-dispositions-in-ratified-provenance` — is **ARCHIVED AND
PROMOTED**: its scenario is in `openspec/specs/doc-health/spec.md` at
`origin/main` `c521504c` (and unmoved from `8015d45f`), promoted by the archive commit
**`bc1f25c4`**. A
`sequenced_after:` declaration names an ACTIVE parent whose outcome a block is
declared relative to; an archived parent's text IS canon, and this block slices
canon's own bytes rather than the parent's delta. No active change writes this
requirement, so there is no parent to declare.

`ideation/staging/` was enumerated (30 topic folders) and `INDEX.md` read: no
topic names doc-health severity policy, the disposition mechanism, a stale-entry
rule or ratification-record rules; the only `grandfather` hits are the
credential-escrow registry's ruling C, a different mechanism in a different
capability. Hence `kind: ad_hoc` (`.openspec.yaml`).

**THE RE-RUN, AT `origin/main` `c521504c`, PASTED.** The search was taken again
after this branch merged that tip, because a sibling authored in parallel is
invisible to a search taken before it existed:

```text
$ git ls-tree -r --name-only origin/main -- openspec/changes \
    | grep 'specs/doc-health/spec.md' | grep -v '/archive/'
openspec/changes/add-nightly-dashboard-refresh/specs/doc-health/spec.md
openspec/changes/settle-aging-staging-topics/specs/doc-health/spec.md

$ for f in <those two>; do git show origin/main:$f | grep -E '^## |^### Requirement'; done
add-nightly-dashboard-refresh : ## ADDED Requirements, 7 requirements, none this one
settle-aging-staging-topics   : ## MODIFIED Requirements, "Aging threshold defaults"

$ git show origin/change/decide-disposition-reading-per-family:\
      openspec/changes/decide-disposition-reading-per-family/specs/doc-health/spec.md \
    | grep -E '^## |^### Requirement'
## MODIFIED Requirements
### Requirement: Finding severity and regression handling      <- DIFFERENT heading
```

**UNCHANGED: no change on `main` writes *Governed corpus membership and the
lifecycle scan set*, and the one branch-only sibling writes a different
requirement.** `sequenced_after: []` stands for the same reason it stood
before, now measured at `c521504c` rather than at `8015d45f`. The archived
parent still needs no declaration: the canon file is byte-unmoved between those
two tips (`git diff --stat 8015d45f c521504c -- openspec/specs/doc-health/spec.md`
is empty), so the block this delta slices is the same block it sliced.
