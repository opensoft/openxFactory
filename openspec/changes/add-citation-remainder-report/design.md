# Design: add-citation-remainder-report

Status: draft
Kind: design

**EVERY DECISION THIS AUTHORING SESSION TOOK IS HERE, WITH ITS ALTERNATIVES AND
THEIR COSTS.** Taking openxFactory issue
[#1053](https://github.com/opensoft/openxFactory/issues/1053) — a ROUTING RECORD
the orchestrator filed at the archive of `add-declared-former-id`, and which this
lane CLAIMED before authoring — commissioned this authoring and took none of
them.

**THE SEVEN DECLARED VETO POINTS ARE D1 THROUGH D7.** Each is put with its
RECOMMENDED option FIRST and the alternatives' costs written out beside it, and
each stands whichever way the others go — no two rest on a shared predicate.
**BRETT HEAP RATIFIES OR VETOES BY NAME.** D0 is a measurement rather than a
decision and is carried beside them, available to be vetoed in the same word.

## 0. The brief

#1053 states the gap, re-measures it, sizes the alternatives, and RECOMMENDS
option **(b)** — *"a `packet_reference` CLI report, run nightly outside
doc-health"* — with **(a)**, a twenty-fourth doc-health check family, named as
*"the natural later step once (b)'s reports show the remainder is stable and
worth gating on."* This packet authors under (b). D1 records why, and sizes (a)
so the later step is already costed when somebody takes it.

## D0 — the measurement, taken before the design

**NOTHING BELOW RESTS ON A NUMBER ANYBODY TYPED, AND #1053'S OWN FIGURES ARE
RE-TAKEN RATHER THAN CARRIED.** Every unclassified figure in this packet was
measured on a fresh clone at `origin/main`
`b1df95ee80633339907c9e661164a783885a5d30` (`b1df95ee`), by #1053's
own stated recipe, run through the LANDED resolver.

```text
$ git ls-files | wc -l
5466
$ git ls-files | grep -v '^openspec/changes/archive/' | grep -v '^tests/' \
    | grep -v '^specs/' | wc -l
2973
```

then every `openspec/changes/[A-Za-z0-9][A-Za-z0-9._\-/]*`-shaped token
extracted from each file's text (**586** distinct), and each resolved through
`packet_reference.resolve(ROOT, token, index=PacketIndex(ROOT))`.

| outcome | tokens |
| --- | ---: |
| `RESOLVED` | **498** (of which `relocated` **76**) |
| `DANGLING`, half `identity` | **74** |
| `DANGLING`, half `file` | **7** |
| `AMBIGUOUS` | **0** |
| `NOT_A_PACKET_REFERENCE` | **7** |
| **inclusive remainder** | **81**, carried by **65** distinct citing files |
| tokens with no raw path in the tree | **162**, of which the rule REPAIRS **76** |

Four of the 2,973 in-scope files are binary and are read with character
replacement rather than skipped; none contributed a token.

**#1053'S TABLE BESIDE IT, AND THE DIFFERENCE IS NOT CLAIMED AS A CORRECTION:**

| | M4 @ `9378eca5` | PR #1041 @ `701c8fde` | #1053 @ `8944758c` | here @ `b1df95ee` |
| --- | ---: | ---: | ---: | ---: |
| raw path absent | 94 | 104 | 153 | **162** |
| repaired by identity | 58 | 64 | 73 | **76** |
| inclusive remainder | 36 | 40 | 80 | **81** |

The four readings are at four commits and only the last two used the landed
resolver. They are approximately and not exactly comparable, which is the caveat
#1053 records against its own predecessors and this one records against #1053.

**THE NAMED SLOT FOR THE DEEP RE-MEASUREMENT.** This is the CHEAP reading: it
counts and classifies by OUTCOME, and it does not re-derive #1053's nine manual
classes. The deep re-measurement is a sibling writer's work in the same lane and
lands beside this packet as:

`evidence/measurement-<sha8>.md`, packet-relative, where `<sha8>` is the head
it was taken at. **THE PATH IS WRITTEN PACKET-RELATIVE ON PURPOSE**: spelled in
full it would be a `openspec/changes/…` token whose file-half does not yet
exist, so naming the slot would mint a remainder entry in the very population
this packet measures. **UNTIL THAT FILE EXISTS, EVERY
CLASSIFIED FIGURE IN THIS PACKET IS CITED TO #1053 AND TO NOTHING ELSE** — the
22 qualifier-removed cross-repository tokens, the 59 survivors, the ~48 true
in-tree remainder, and the nine classes are all #1053's hand work, quoted with
attribution and never restated as this packet's own measurement. `tasks.md`
§ 2.3 is where that file becomes the first COMMITTED measurement, and the ruling
on D6 is what it is measured against.

**THREE FACTS THIS RE-MEASUREMENT FOUND THAT #1053 DOES NOT CARRY.** Each moves
a decision below rather than decorating it.

**(i) 74 remainder TOKENS are 48 distinct IDENTITIES.** Eighteen identities are
cited by more than one remainder token:

| identity | remainder tokens |
| --- | ---: |
| `add-council-clearance-rule-template` | 6 |
| `add-openxfactory-tui-installer` | 4 |
| `add-pre-archive-citation-gate` | 3 |
| `foo` | 3 |
| twelve more (`add-x`, `change-x`, `neg-neg-lin`, `add-demo-capability`, `2026-09-09-foo`, `add-assembly-plane-separation`, `add-ideation-governance`, `add-managed-service-inventory`, `add-managed-service-mapping`, `add-regular-pr-council-clearance`, `add-tenant-reader-grant-pipeline`, `clarify-gate-rules-decline-position`, `prepare-openspec-1.12-readiness`, `relocate-review-authority-floor`) | 2 each |

Fifteen of the 81 tokens are a bare directory path ending in `/` whose sibling
token names the same identity without the slash. This is why D3 requires BOTH
counts: **a reader repairs identities, and the token count tells them nothing
about how much work that is.** That 48 equals #1053's hand-read "about 48" is a
COINCIDENCE OF TWO DIFFERENT QUANTITIES — #1053's 48 is 59 survivors minus
cross-repository misses and artifacts, and this 48 is 74 tokens collapsed onto
their identities. Recorded as a coincidence, never as a confirmation.

**(ii) The token grammar manufactures remainder, in at least four shapes.**
#1053 names one (Python implicit string concatenation). Measured across the 81:

| shape | tokens | example |
| --- | ---: | --- |
| trailing `/` (a directory citation) | 15 | `openspec/changes/add-composition-drift-cascade/` |
| trailing `-` (a path split across source lines) | 2 | `…/archive/2026-08-27-add-hermes-customer-subject-` (`scripts/doc_health/pin_class.py`); `…/register-gate-rules-council-seats/walk-` |
| trailing `.` (a sentence-terminal full stop swallowed) | 1 | `…/codexfactory-floor-relocation-2026-09-10.md.` in `contracts/openspec-cli-pin.yaml` |
| a `/./` segment | 1 | `openspec/changes/foo/./proposal.md` (`scripts/packet_reference.py`'s own docstring) |

The trailing full stop is the sharpest of the four because it is not a defect in
any record: `contracts/openspec-cli-pin.yaml` cites a real file at the end of a
sentence, and the REGEX ate the punctuation. A report that printed it as a
dangling citation would be reporting its own grammar.

**(iii) `openspec/changes/README.md` is DANGLING(identity-half) in this tree.**
That path is the canonical `NOT_A_PACKET_REFERENCE` example in
`packet_reference.py`'s own docstring — *"a file that merely sits under
`openspec/changes/` without naming a packet, such as this corpus's own
`openspec/changes/README.md`"* — and `ls` says it does not exist here. The
resolver's rule for an unclaimed identity is: if the RAW PATH is present the
reference is a plain path (`NOT_A_PACKET_REFERENCE`), and if it is absent the
identity half failed. **So the class of a citation is a function of the tree,
not of the citation**, and a report that says "dangling" must be read as "in
this tree, at this commit". It is cited from `scripts/packet_reference.py` and
`scripts/validate-pin-registrations.py`, which makes it an instance of #1053's
"self-referential illustrative example" class as well.

**(iv) AND THIS PACKET'S OWN EFFECT ON THE POPULATION, MEASURED AFTER THE
PACKET EXISTED RATHER THAN PREDICTED BEFORE IT.** The same recipe re-run on
this branch: **2,978** files in scope (+5, this packet's own), **587** distinct
tokens (+1), **499** `RESOLVED` (+1), and the remainder **UNCHANGED at 81
tokens** — 74 identity-half, 7 file-half, 0 ambiguous. The packet carries FOUR
citation tokens and mints no new remainder: the one token it adds to the corpus
is `…/add-citation-remainder-report/proposal.md`, cited from `README.md`, and it
resolves. **BUT IT JOINS THE CITING SET OF THREE REMAINDER ENTRIES**, all three
by QUOTING them as examples — `openspec/changes/README.md` (from four of this
packet's own files), `…/add-composition-drift-cascade/` and
`…/foo/./proposal.md` (from `design.md`). **A DOCUMENT THAT DISCUSSES A
DANGLING CITATION BECOMES A RECORD THAT CARRIES ONE**, which is #1053's
"self-referential illustrative example" class being created, live, by the
packet that characterizes it. It is a real effect at a trivial size here — three
citing-file counts, no new remainder — and it is the same mechanism D5 refuses
at a serious size, where a nightly report would carry one such quotation per
remainder line, every night, forever.

## D1 — RECOMMENDED: (b), a report CLI outside doc-health

**The question.** Where does the remainder get reported: a twenty-fourth
doc-health check family, a standalone report, or nowhere?

**RECOMMENDED — OPTION (b): A STANDALONE REPORT CLI, RUN NIGHTLY OUTSIDE
DOC-HEALTH.** This is #1053's own recommendation and this packet does not
improve on it; what this packet adds is the SIZING of (a) so the later step is
costed rather than feared.

*Why (b) and not (a) now, in one sentence:* **doc-health's own promoted rule
says a new family's severity decision must FOLLOW a measurement of the
population it would red, and no such measurement exists yet** — this packet's
whole purpose is to produce one.

**THE COST OF (a), NAMED EXACTLY FROM THE PROMOTED TEXT RATHER THAN ESTIMATED.**
Four items, each verified in this tree at `b1df95ee`:

1. **A `## MODIFIED Requirements` block over the whole family enumeration.**
   `openspec/specs/doc-health/spec.md`'s *Deterministic check families* reads
   *"The doc-health deterministic pass SHALL implement twenty-three check
   families …"* and then NAMES all twenty-three. OpenSpec `MODIFIED` replaces
   wholesale, so the delta must restate that requirement in full — every
   sentence and every scenario — plus the new family, with the numeral bumped to
   twenty-four. A partial restatement drops scenarios silently.
2. **A registry edit.** `scripts/doc_health/families.py`'s `FAMILIES` mapping
   registers exactly 23 ids today (counted from the live registry, not from the
   prose: `client-identity-composition … tag-hygiene`). A twenty-fourth needs an
   id, a module and a reporting-list entry.
3. **The family-enumeration gate, which is the reason (1) cannot be skimped.**
   The promoted requirement *The family enumeration is derived, not restated on
   trust* makes the suite verify the enumeration against the registry and refuse
   a restatement that *"omits a registered family, names an unregistered one, or
   carries a numeral inconsistent with the registry in its own tree."* Its own
   text records why: *"A requirement whose text every new family must restate is
   a requirement every new family can truncate. Three changes in three days
   truncated it, and all three were caught by a human rather than by a check."*
4. **A severity decision that canon says must come SECOND.** The same capability
   states, of the family-enumeration family's own launch: *"This family SHALL be
   advisory at launch… Raising the severity and adding the contested
   classification are ONE later decision taken together by ruling, and SHALL
   follow a measurement of the population the gate would red rather than precede
   it."* `promotion-fidelity` and `duplicate-packet` each walked exactly that
   two-step path.

*What (a) buys, and it is real:* unified severity, a place in the ranked plan,
the nightly report everyone already reads, `--fail-on` semantics, and the only
option that can ever gate a pull request. **(a) is not rejected. It is
SEQUENCED**, and D6 states the condition on which it becomes takeable.

**OPTION (c): LEAVE IT UNREPORTED.** *Cost:* zero today, and it is the posture
`add-declared-former-id` D4 deliberately took. The risk is the one #1053 names:
this is exactly the posture that let issue #840's three dangling `cited_to`
citations go unnoticed until a human found them by reading a diff. That specific
instance is now fixed by `check_citations`; nothing generalizes the fix to the
81 tokens measured in D0, and a population nobody looks at cannot be known to be
stable or unstable.

**WHY A NEW CAPABILITY DIRECTORY RATHER THAN A DELTA ON AN EXISTING ONE.** Both
plausible homes are foreclosed by the same mechanism and it is worth writing
down once: `doc-health`'s enumeration is closed by the family-enumeration gate,
and `proposal-origin`'s classes are closed by its own promoted sentence *"The
family's finding classes are therefore SEVEN, named: …"* — so an eighth class is
a MODIFIED block over a requirement about proposal ORIGINS, carrying a class
about CITATIONS. `specs/packet-citation-report/` is novel, so every requirement
is `## ADDED`, no promoted byte moves, and `sequenced_after:` is the positive
root claim `[]`.

## D2 — RECOMMENDED: a sibling script, not a CLI bolted onto the library

**The question.** Does `scripts/packet_reference.py` grow a `__main__` and an
argparse surface, or does a new script import it?

**RECOMMENDED — OPTION 1: A SIBLING `scripts/report-citation-remainder.py` THAT
IMPORTS THE LIBRARY.** The library's contract stays a library's. Three reasons,
in order of weight:

1. **The docstring is a contract and it is cited.** `packet_reference.py` line
   91 reads *"Run: this module is a library and has no CLI."* Adding a CLI means
   that sentence changes — a one-line edit in a module whose docstring is quoted
   in an archived ratified packet's design. The edit is cheap; the precedent is
   not. A module that says what it is and then stops being it teaches readers not
   to trust module docstrings.
2. **The resolver is consumed by a gate; the report is not.** `check_citations`
   in `scripts/validate-pin-registrations.py` imports this module inside a
   validator that exits 1. Every line added to a module a gate imports is a line
   that can break the gate. A report that lives next door cannot.
3. **Two audiences, two argument surfaces.** The resolver answers ONE question
   about ONE reference. The report walks a tree, applies a file population, a
   token grammar and a suspicion heuristic — none of which belongs in a module
   whose whole design note says it *"holds NO repository vocabulary and NO
   module-level root"*.

**THE ARGUMENT SURFACE, STATED SO THE REALIZATION CANNOT DRIFT:**

```text
python3 scripts/report-citation-remainder.py [REPO_ROOT]
    [--json] [--all] [--identities] [--include PREFIX ...] [--exclude PREFIX ...]

REPO_ROOT       repository root to scan (default: cwd), as every sibling
                scripts/validate-*.py already spells it
--json          machine-readable output instead of the human table
--all           also list RESOLVED and NOT_A_PACKET_REFERENCE tokens, which
                the default output only COUNTS
--identities    group the remainder by identity rather than by token
--include/--exclude   override the default file population, so the recipe in
                D3 is a DEFAULT and not a hard-coding
```

**THE OUTPUT.** A human table by resolver outcome — counts first, then the
remainder itemized with its citing files — plus, under `--json`, one object per
token carrying `token`, `status`, `half`, `identity`, `remainder`, `citing_files`,
`class`, and `cross_repo_suspected`. Both carry the four headline numbers: files
in scope, distinct tokens, remainder TOKENS, remainder IDENTITIES.

**THE EXIT CODE IS ALWAYS 0, AND A `--fail-on` IS EXPLICITLY NOT BUILT.** Exit 0
is what makes this a report rather than a gate: nothing about the 81 tokens has
been ruled a defect, and a tool that can exit non-zero acquires that meaning the
first time somebody wires it into CI. `--fail-on` is RESERVED for option (a)
under D1, where a severity decision will have been taken by ruling. The only
non-zero exit is the ordinary one for a tool that CANNOT RUN — an unreadable
tree, a root that is not a git work tree — which is a different fact from a
finding and says so.

**OPTION 2: give `packet_reference.py` a `__main__`.** *Cost:* the docstring
contradiction above, plus the gate-coupling in (2), plus the module acquires a
file population and a token grammar it deliberately does not have. *What it
buys:* one file instead of two. Declined on that trade.

## D3 — RECOMMENDED: the recipe, made exact so it reproduces

**The question.** What exactly does the report read, tokenize and resolve?
#1053's recipe is a sketch that reproduces its own numbers; a shipped report
needs it fixed, because the next reading is compared against this one.

**RECOMMENDED — OPTION 1: THE RECIPE BELOW, STATED IN THE REQUIREMENT AND NOT
ONLY IN THE CODE.**

**(a) THE FILE POPULATION.** `git ls-files`, minus three prefixes, each with a
stated reason rather than an inherited one:

| excluded | why |
| --- | --- |
| `openspec/changes/archive/` | FROZEN RECORD. An archived packet's prose is not editable and its citations are not repairable, so reporting them is reporting work nobody may do. #1053 and M4 both exclude it. |
| `tests/` | FIXTURES. Test corpora deliberately carry synthetic ids (`add-x`, `foo`, `change-r`) and deliberately-absent files; every one would report as remainder. |
| `specs/` | SPEC KIT FEATS, a different tool's artifacts that cite packets illustratively. |

**AND ONE THE REPORT MUST ADD THE MOMENT D5 EVER CHANGES: the report's OWN
OUTPUT PATH.** `health/` is INSIDE this population — 7 tracked files at
`b1df95ee`, contributing **0** citation tokens. A committed remainder report
would be the first file there to carry them, one per remainder line, and the
next run would count its own output as citations from `health/…`. Under the
recommended D5 (artifact-only) nothing is committed and the hazard is
structural rather than live; the requirement names it anyway, because the fence
must exist BEFORE the file does.

**(b) THE TOKEN GRAMMAR, WITH ITS TRAILING-PUNCTUATION RULE MADE EXPLICIT.** The
extraction pattern is #1053's, `openspec/changes/[A-Za-z0-9][A-Za-z0-9._\-/]*`,
and it is kept so the two readings compare. What is ADDED is a normalization
step the measurement in D0 proves is needed, applied before resolution and
REPORTED rather than hidden:

- a trailing `/` is stripped (15 tokens), and the stripped token is merged with
  its unslashed sibling rather than counted twice;
- a trailing `.` is stripped where the token would otherwise end a sentence
  (1 token), which is the `contracts/openspec-cli-pin.yaml` case;
- a token ending in `-` is FLAGGED `truncated` and NOT resolved as if complete
  (2 tokens), because the citation it came from is a line-broken or
  concatenation-split path and the tool cannot know the rest;
- a `/./` segment is left exactly as it is, because `packet_reference`'s own
  `_normalised` already drops it.

**Every normalization the report applies is printed in its own row.** A reader
who cannot see that the tool changed the token cannot check the tool.

**(c) THE CROSS-REPOSITORY QUALIFIER, AND THE DECISION THAT MATTERS HERE: FLAG,
NEVER DROP.** #1053's automated check uses four adjacency heuristics — a
path-joined prefix (`xFactories/LedgerxFactory/…`), a GitHub blob or tree URL, a
bare qualifier word immediately before the token (`codexFactory
openspec/changes/…`), and a trailing `(RepoName)` parenthetical — and #1053
itself measures their limit: *"the automated qualifier check only catches a
qualifier immediately adjacent to the token; several citations name the other
repository one to three lines above instead"*, which a manual read found for at
least ten more.

**RECOMMENDED: the report widens the adjacency window to the citing LINE plus
the three lines above it, and then reports the hits as `possibly-cross-repo`
INSIDE the remainder rather than removing them from it.** Three reasons:

1. **A heuristic that drops is a heuristic nobody can audit.** A token silently
   removed from the population cannot be checked by a reader who disagrees with
   the window. A token printed as `possibly-cross-repo` can.
2. **The window is a guess and widening it does not stop being one.** Three
   lines is derived from #1053's own observation and from nothing else; a
   citation four lines below its qualifier is a miss, and a paragraph that
   happens to mention `codexFactory` above an in-tree citation is a false
   positive. Neither is safe to act on silently.
3. **The counts stay comparable.** The headline remainder stays the INCLUSIVE
   number, which is the one M4, PR #1041 and #1053 all report; the
   cross-repository reading is printed BESIDE it as a second row, not
   substituted for it.

*OPTION 2 — drop them silently, as the issue's own automated pass did.* Cost: it
makes the headline number depend on an unauditable window, and the number is the
input to D6's stability condition.
*OPTION 3 — count them as ordinary remainder with no flag.* Cost: it hides the
single largest known class (≥22 + ≥10) behind a number that looks like a defect
count, which is precisely the misreading `add-declared-former-id` D4 refused to
create.

**(d) THE RESOLVER OUTCOMES THE REPORT PRINTS.** `DANGLING` (identity-half and
file-half REPORTED SEPARATELY, because the resolver's own docstring insists *"a
failure SHALL say which half failed"* and the two want different repairs) and
`AMBIGUOUS` are ITEMIZED. `RESOLVED` and `NOT_A_PACKET_REFERENCE` are COUNTED
only, with `relocated` counted within `RESOLVED` — that count is the rule
working, and it is the single most useful number for a reader wondering whether
the resolver earns its keep (76 of 498 at `b1df95ee`).

## D4 — RECOMMENDED: classify only what can be decided mechanically

**The question.** #1053's manual read puts the remainder in nine classes. How
many of them does a machine get to assert?

**RECOMMENDED — OPTION 1: A SMALL MECHANICAL SET, AND AN HONEST `unclassified`
FOR EVERYTHING ELSE.**

| #1053's class | report's verdict | why |
| --- | --- | --- |
| cross-repository (adjacency-missed) | **MECHANICAL, as a SUSPICION** — `possibly-cross-repo` | D3(c): the window is stated, the hit is flagged, the token stays in the count |
| pure tokenization artifact | **MECHANICAL** — `truncated` / `punctuation-stripped` | D3(b): the tool knows what it did to the token, so it can say so |
| DANGLING file-half, nested test fixture | **MECHANICAL** — `fixture-path` | the citing file's own path is under a `tests/` directory nested below the top-level exclusion; that is a path fact |
| synthetic fixture id under `examples/` or `ideation/dashboard/gate-records/` | **MECHANICAL** — `fixture-path` | same: the CITING file's location is knowable |
| self-referential illustrative example in a docstring | **HUMAN** — `unclassified` | it needs a reading of what the prose is DOING; `add-x` in a docstring and `add-x` in a record look identical to a machine |
| id that never existed | **HUMAN** — `unclassified` | needs `git log --all --diff-filter=A` over two spellings, and a negative result is not proof of intent |
| pre-tracking rename | **HUMAN** — `unclassified` | needs the rename's history and a judgment that no `former_ids:` covers it |
| stale draft name, since finalized | **HUMAN** — `unclassified` | needs somebody to recognize the finalized file |
| unclassified | **HUMAN** — `unclassified` | it is already the honest answer |

**WHY THE SPLIT FALLS THERE.** A class is MECHANICAL when the evidence is a
fact about a PATH or about the tool's own normalization, and HUMAN when the
evidence is a fact about INTENT. `unclassified` is not a failure of the report —
it is the report declining to assert what it cannot see, and #1053's own manual
read is the proof that the human classes need a human.

**AND THE ONE RULE THAT GOVERNS ALL NINE: NOTHING IS REPAIRED.**
`add-declared-former-id` D4 and `packet_reference.py` both hold that *"a
reference that resolves owes the citing record no edit"* — the resolver
therefore *"offers no corrected spelling for a caller to write back — offering
one is how a reader becomes an editor"*. **THIS PACKET EXTENDS THAT SENTENCE TO
ITS OTHER HALF: A REFERENCE THAT DOES NOT RESOLVE OWES THE CITING RECORD NO EDIT
FROM THIS TOOL EITHER.** The report names, counts and classifies; it proposes no
spelling, writes no patch, opens no issue and ticks no box. Whether a given
dangling citation is worth repairing is a judgment for whoever owns the record,
and several of the 81 are deliberately dangling by their own file's design.

*OPTION 2 — mechanize all nine.* Cost: a machine guessing "never existed" from a
`git log` miss and "illustrative example" from a filename would assert intent it
cannot see, and every wrong guess becomes a number in D6's stability series.
*OPTION 3 — classify nothing, print the raw list.* Cost: it hands the reader the
same 81 lines the issue already has, and the four mechanical classes are exactly
the ones a human should never have to re-derive.

## D5 — RECOMMENDED: artifact-only, and the reason is not merely merge conflicts

**The question.** How is the report run nightly, and what does it leave behind?

**WHAT EXISTS TODAY, MEASURED RATHER THAN ASSUMED.** This repository has ONE
scheduled workflow of its own (`.github/workflows/review-lane-repin.yml`); the
nightly governance run is `.github/workflows/doc-health-reusable.yml`, whose own
header says *"The caller (the xFactory aggregation repo's thin nightly workflow)
owns scheduling, dispatch, and permissions; suite logic changes only here."*
Inside it, three lanes already write governed output and all three do it the same
way — to a ROLLING PULL-REQUEST BRANCH, never straight to `main`:

| lane | what it writes | where |
| --- | --- | --- |
| derive-possibles | `ideation/cross-reference.yaml`, `health/derive-possibles/<date>/…` | branch `doc-health/derive-possibles` |
| ideation-readiness | `health/ideation-readiness/<date>/…` | staged into the same commit-back |
| neutrality-drift | drafted seeds + lane state | branch of its own, *"dormant until first scout run"* |

and the doc-health report itself is committed on a delivery branch
(`Doc-health report ${RUN_DATE}`).

**RECOMMENDED — OPTION 1: A STEP IN `doc-health-reusable.yml` THAT RUNS THE
REPORT AND UPLOADS IT AS A WORKFLOW ARTIFACT, COMMITTING NOTHING.** It is the
smallest wiring that exists — one step, no branch, no commit, no permissions
beyond the run's own — and it has a second reason that is specific to THIS
report rather than general:

**A COMMITTED REMAINDER REPORT WOULD BE COUNTED BY THE NEXT RUN.** `health/` is
INSIDE D3(a)'s file population. It holds 7 tracked files at `b1df95ee` and they
contribute **0** `openspec/changes/…` tokens — measured, not assumed. A
committed report listing the remainder would be the FIRST file under `health/`
to carry such tokens, and it would carry one per remainder line: the next
night's run would find them, count them as citations FROM `health/…`, and
inflate the very series D6 measures stability on. **THE MECHANISM IS NOT
HYPOTHETICAL AND THIS PACKET DEMONSTRATES IT ON ITSELF**: D0(iv) measures this
packet joining the citing set of three remainder entries purely by quoting them,
which is the same act a report performs mechanically and at scale. The fence (D3(a)) closes it,
but a design whose correctness depends on remembering a fence is worse than one
that never opens the hole.

*The merge-conflict argument, which is the one the brief names, is real but
SECONDARY and is stated at its true size:* a ROLLING committed file would be a
conflict magnet, but the estate's own commit-back lanes do not write rolling
files — they write DATE-PARTITIONED new files on a lane-owned branch, which
conflicts with nothing. So "committed output conflicts" is not by itself a
reason to refuse option 2; the self-counting hazard is.

**OPTION 2: A DATE-PARTITIONED COMMIT-BACK, `health/citation-remainder/<YYYY-MM-DD>/…`,
on a rolling pull-request branch — the derive-possibles shape.** *What it buys,
and it is the strongest case against the recommendation:* D6's stability
condition is measured across N nightly runs, and an in-tree series is read with
one `git log` while an artifact series must be downloaded run by run and expires
with the repository's artifact retention. *Cost:* the self-counting hazard above,
a new lane-owned branch, a commit-back step with write permissions, and a
governed write to the corpus in a packet whose whole posture is that it changes
nothing. **NAMED AS THE PROMOTION STEP** — if D6's condition proves unmeasurable
from artifacts in practice, this is the wiring to adopt, and it pairs naturally
with D1 option (a).

**OPTION 3: A COMMITTED ROLLING `health/citation-remainder.md`.** *Cost:* the
self-counting hazard, PLUS a single file that changes on every nightly run and
that every concurrent lane's merge from `main` must reconcile. **REFUSED BY
NAME.** The estate has no rolling committed report today and this is not the
report to start one with.

## D6 — RECOMMENDED: what "stable" means before option (a) is takeable

**The question.** D1 defers (a) until the population is *"measured stable"*.
Stable how, measured against what, for how long? An undefined condition defers
forever.

**RECOMMENDED — OPTION 1: A THREE-PART CONDITION ON THE SERIES, ALL THREE PARTS
SATISFIED ON THE SAME DAY.** The series is the nightly report's headline numbers;
`N = 14` consecutive runs is the proposed window, which is two weeks and is
proposed as a number to be vetoed rather than derived.

1. **THE UNCLASSIFIED COUNT IS NOT GROWING.** Over the last N runs, the count of
   remainder IDENTITIES carrying class `unclassified` has no upward trend — its
   value on the last run is less than or equal to its value N runs earlier.
   *Rationale:* `unclassified` is the part a gate could not have justified
   refusing, and a growing `unclassified` means the corpus is producing citation
   shapes faster than anybody is reading them.
2. **NEW ARRIVALS ARE BOUNDED AND ATTRIBUTABLE.** Over the last N runs, the
   number of remainder identities that were NOT in the remainder N runs earlier
   is at most a small number (proposed: 3), and each one is attributable to a
   landed pull request the report's own diff can name. *Rationale:* a gate reds
   on ARRIVALS, not on the standing population; a standing 48 that never moves
   costs a gate nothing, while three unexplained arrivals a week is what a gate
   is for.
3. **THE MECHANICAL CLASSES ARE STABLE AT ZERO NET.** `truncated`,
   `punctuation-stripped` and `fixture-path` do not grow, because those are the
   classes a gate would red on that NOBODY SHOULD FIX — they are artifacts of
   the tool's own grammar and of deliberate fixtures. A gate that reds on them
   is a gate that will be turned off.

**AND THE CONDITION IS A TRIGGER TO PUT THE QUESTION, NOT AN AUTHORIZATION TO
ACT.** Meeting it entitles somebody to FILE the successor for option (a) with the
series attached; the severity and contested classification remain *"ONE later
decision taken together by ruling"*, which is doc-health's own promoted rule and
is not overridden here.

*OPTION 2 — "stable" = the remainder count is unchanged for N runs.* Cost:
measured at D0, the count moves whenever ANY packet archives (the relocation
repairs) or any new doc cites a packet; a flat total is a condition this corpus
will never meet, so the deferral would be permanent by accident.
*OPTION 3 — no condition; whoever wants (a) argues it then.* Cost: it is the
state #1053 already describes, and it is how a "later step" becomes a never
step.

## D7 — RECOMMENDED: the scope fences, stated so the realization cannot drift

**The question.** What is this packet, and its later realization, forbidden to
touch?

**RECOMMENDED — OPTION 1: FOUR FENCES, EACH NAMED WITH THE FILE IT PROTECTS.**

1. **NO CITATION IS EDITED.** Not by this pull request, not by the realization,
   not by the nightly run. D4's rule is the whole of it: a resolving reference
   owes the citing record no edit, and a dangling one owes it none FROM THIS
   TOOL. The report ships no `--fix`, no suggested spelling, and no patch
   output.
2. **NOTHING CROSS-REPOSITORY IS RESOLVED.** `packet_reference.py` states the
   boundary — *"THE CROSS-REPOSITORY CASE IS NOT DECIDED HERE"*, and the module
   *"holds NO repository vocabulary and NO module-level root"*. This report
   SUSPECTS (D3(c)) and never resolves. A sweep of OpsxFactory's,
   LedgerxFactory's, AdxFactory's or codexFactory's own corpora is a separate
   act in each of those repositories, and this packet does not file it.
3. **`scripts/validate-pin-registrations.py` IS UNTOUCHED.** Its
   `check_citations` arm keeps exactly the scope `add-declared-former-id`
   tasks § 5.0 gave it — the `dispositions[].cited_to` field of registered pin
   rows, refusing exit 1 on a genuine dangling reference. It is a GATE; this is
   a REPORT; and folding a corpus-wide sweep into a gate that exits 1 is the
   option `add-declared-former-id` D4 already considered and rejected on scope.
   No line of that file changes in this packet or in its realization.
4. **NO DOC-HEALTH FILE MOVES.** `openspec/specs/doc-health/spec.md`,
   `scripts/doc_health/families.py` and every module under `scripts/doc_health/`
   are untouched. D1's whole argument is that touching them is a different act
   with a different cost, and a realization that quietly registered a family
   would spend that cost without the ruling that authorizes it.

**AND THIS PACKET CONFORMS TO `gate-code-surface-declarations` BY
CONSTRUCTION.** That packet is ACTIVE and ratified (2026-09-13, Brett Heap,
verbatim *"ratify"*), and its realization — `scripts/code_surface.py` and
`scripts/validate-code-surface.py` — is in flight as openxFactory PR #1029 and
is NOT on `main` at `b1df95ee`. A sibling writer in this lane verified this
packet's front-matter shape against that reader on the realization branch at
`48bc7de7` rather than against the prose grammar — and it was RUN rather than
reasoned about, as five probes on a throwaway packet, one `code_surface:` value
at a time:

| probe | value | `validate-code-surface.py` |
| --- | --- | ---: |
| a | `openxFactory` | exit **0** |
| b | `openxFactory — <gloss>` | exit **0** |
| c | `openxFactory (<gloss>)` | exit **0** |
| d | `openxFactory: <gloss>` | exit **0** |
| e | `openxFactory, <gloss>` | exit **1** |

**THIS PACKET'S DECLARATION IS PROBE (b) EXACTLY**, which the reader admitted
with *"0 outside the grammar"* and *"code_surface validation passed (every
active declaration's head is admitted)"*. The HEAD is the single bare
repository identifier `openxFactory`; the gloss is introduced by a
whitespace-preceded em dash, which `_GLOSS_OPENER_RE`
(`scripts/code_surface.py:166`) admits, and the head parse STOPS at the opener
so nothing in the gloss — its semicolon, its colon, its full stops — is ever
judged. **A COMMA WOULD HAVE BEEN REFUSED** (probe (e)): a comma is a LIST
separator, so the reader tries to read the next word as a second repository
name and then runs into prose with no opener — the `list-runs-into-prose`
class that packet's closed register carries five of its eight entries in.
**SO NO REGISTER ENTRY IS OWED BY THIS PACKET AND NONE IS REQUESTED**, and the
register does not move. The verification record is `1053/head-verify.md` in
this lane's handoff attachments; the shape is the one the shape twin
`gate-code-surface-declarations` already uses for its own declaration.

*OPTION 2 — leave the fences to the realization's own judgment.* Cost: the
realization is a later pull request on a later word, possibly by a different
hand; a fence written after the fact is a post-mortem.

## What is NOT decided here

- **The nine manual classes are not re-derived.** D0's named slot carries that
  work; until `evidence/measurement-<sha8>.md` exists, #1053's classification is
  quoted and attributed, never restated.
- **`N = 14` and "at most 3 arrivals" in D6 are proposed numbers.** They are
  derived from nothing but the shape of a two-week window and are the most
  vetoable figures in this packet.
- **The report's exact table layout** is the realization's, within the fields
  D2 fixes.
- **Whether option (a) is ever taken** is D6's trigger plus a later ruling, and
  this packet neither takes it nor forecloses it.
