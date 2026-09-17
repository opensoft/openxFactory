# Design: add-citation-remainder-report

Status: ratified
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

**AND WHAT A BARE WORD TAKES IS STATED RATHER THAN LEFT TO BE GUESSED**, because
seven independent decisions make "ratify" ambiguous unless somebody says: **a
bare ratifying word takes the RECOMMENDED option at all seven; a veto NAMES the
decision, and costs that section alone.** That is the reading the shape twin
`gate-code-surface-declarations` records Brett Heap giving on 2026-09-13 — *the
bare word "ratify" takes the packet as encoded* — cited here as the house
reading this packet asks for, not as a ruling already given over this packet.

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

**AND THE 162 PARTITIONS FIVE WAYS, NOT FOUR.** `raw-missing` is every distinct
token whose literal path does not exist in the tree, and the resolver's answer
for such a token can be any of FIVE things — the fifth being the one it declines
to read as a packet reference at all, which is counted beside the remainder and
never inside it but is a raw-missing path just the same:

| the token has no raw path, and the resolver answers | tokens |
| --- | ---: |
| `RESOLVED` — the identity rule REPAIRED it | **76** |
| `DANGLING`, half `identity` | **74** |
| `DANGLING`, half `file` | **7** |
| `AMBIGUOUS` | **0** |
| `NOT_A_PACKET_REFERENCE` | **5** of the 7 (the other 2 DO have a raw path) |
| **raw-missing** | **162** — `76 + 74 + 7 + 0 + 5` |

The five are the SHAPES this corpus writes inside its own tooling and prose
rather than citations — `openspec/changes/archive/...` in
`scripts/validate-ideation-cross-reference.py`,
`openspec/changes/archive/proposal.md` in `scripts/proposal-support.py`,
`openspec/changes/archive/2026-09-01-` in `README.md`, and
`openspec/changes/archive/2026-09-11-` and `openspec/changes/archive/2026-09-11-...`
in `amend-register-act-5b-projection-proof` — which the resolver refuses as
references and which have no path either. D2's output rule 2 states the identity
with all five terms for exactly this reason.

**AND "IN SCOPE" MEANS TRACKED ENTRIES, NOT FILES READ — THE TWO DIFFER BY
FOUR AND THE PACKET SAYS WHICH IT MEANS.** The `2,973` above is what the
`git ls-files` listing leaves after the three exclusions: tracked ENTRIES. Four
of them are skipped as non-files (below), so the report READS **2,969** files
and tokenizes those. Every "in scope" figure in this packet is the ENTRY count
and the read count is four fewer at every revision named here — the gitlink
count has been 4 at `b1df95ee`, at `origin/main` and at this branch's head.
`.openspec.yaml` and `tasks.md` § 1.1 carry the entry count with the gitlink
skip stated beside it; **`README.md`'s bullet, which is read on its own without
this packet beside it, now carries BOTH numbers rather than a label a reader
has to come here to disambiguate** (PR #1069, Copilot thread
`PRRT_kwDOTAvnrs6jFG02`); and the delta's own output scenario asks a report for
the pair rather than for "files in scope". The
spec's population requirement now makes the pair NORMATIVE rather than leaving a
CLI to pick one: a report states both, labelled, and presents neither as the
other (PR #1069, Copilot thread `PRRT_kwDOTAvnrs6jEUvn`).

**NO FILE IN THE POPULATION IS BINARY, AND THE FOUR ENTRIES THAT CANNOT BE READ
AS TEXT ARE NOT FILES.** Four of the 2,973 `git ls-files` entries in scope are
mode-160000 SUBMODULE GITLINKS — `installs/omnigent-install`, `openDox`,
`openXdox`, `openXwallet` — directories, not files. They are SKIPPED and
contribute no token. Measured on both trees: zero in-scope files carry a NUL
byte and zero fail a strict UTF-8 decode, so "read binary with character
replacement" describes code this report does not need and would not exercise.
**THE RULE IS PROMOTED ANYWAY, BECAUSE A POPULATION RULE THAT IS TRUE TODAY BY
LUCK IS NOT A RULE** (PR #1069, Copilot thread `PRRT_kwDOTAvnrs6jIP45`): the
delta now says a file the report cannot decode is SKIPPED, COUNTED and REPORTED
— never replacement-decoded, because bytes that are not text can yield matches
no record wrote, and never fatal — and that the arithmetic closes, entries in
scope = files read + entries skipped as non-files + files skipped as
undecodable. At `b1df95ee` that third term is **0** and at this branch's head it
is **0**, so no published figure moves; the rule exists so that the day it is
not zero, two readings still agree.
The open question a gitlink raises — whether another repository's tracked
content belongs in this repository's citation population at all — is answered NO
here by D7 fence 2, which forbids resolving anything cross-repository.

**#1053'S TABLE BESIDE IT, AND THE DIFFERENCE IS NOT CLAIMED AS A CORRECTION:**

| | M4 @ `9378eca5` | PR #1041 @ `701c8fde` | #1053 @ `8944758c` | here @ `b1df95ee` |
| --- | ---: | ---: | ---: | ---: |
| raw path absent | 94 | 104 | 153 | **162** |
| repaired by identity | 58 | 64 | 73 | **76** |
| inclusive remainder | 36 | 40 | 80 | **81** |

The four readings are at four commits and only the last two used the landed
resolver. They are approximately and not exactly comparable, which is the caveat
#1053 records against its own predecessors and this one records against #1053.

**THE DEEP RE-MEASUREMENT IS IN, AND THE SLOT IS FILLED.** The figures above are
the CHEAP reading — outcome counts, no manual classification. The DEEP one was
taken by a sibling writer in this lane at the same head and is committed in this
packet at `evidence/measurement-b1df95ee.md`, with its run record, its
instrument (`measure.py`), a 1.5 MB per-token JSON and a classification JSON
held UNCOMMITTED in this lane's handoff attachments — the repository
`opensoft/brett-wip`, path
`handoffs/xFactory/attachments/openxfactory-1-2026-09-13/1053/` — because the
packet needs the reading and not the raw dump. **THE ATTACHMENTS ARE CITED AS A
REPOSITORY AND A REPO-RELATIVE PATH, NEVER AS A CHECKOUT ON SOMEBODY'S
MACHINE**, which is not a style preference: this repository's own constitution
requires that *"Committed files MUST NOT contain host-absolute paths; use
repo-relative paths or runtime resolution"* (`.specify/memory/constitution.md`
Principle IV, `:72-73`), and it is the form this corpus already uses for this
same registry — `README.md:777`,
`openspec/changes/disposition-codexfactory-regular-pr-council-clearance-archive/proposal.md:10`
and the `register-gate-rules-council-seats` walk records all spell it
`` `opensoft/brett-wip` commit `<sha>` `` plus a repo-relative path. The
discipline is recorded discharged the same way in
`specs/017-openxwallet-carve/plan.md:103`: *"No host-absolute paths in any
committed file … the scratch clone location never appears in a commit."*

**ITS HEADLINE IS THREE NUMBERS, AND ONLY THE THIRD IS A CLASSIFICATION:**

| | #1053 @ `8944758c` | evidence @ `b1df95ee` |
| --- | ---: | ---: |
| INCLUSIVE remainder (cross-repository left in) | 80 | **78** |
| THIS-TREE-ONLY (automated qualifier check applied) | 59 | **57** |
| TRUE in-tree remainder (every token read by hand) | "about 48" | **39** |
| `AMBIGUOUS` | 0 | **0** |

**AND IT PROVES THE METHODOLOGY IS NOT THE VARIABLE, WHICH IS THE PART THAT
MATTERS.** Run against a control clone at `8944758c` — the revision #1053 itself
measured — the same instrument reproduces **ALL TWELVE** of #1053's published
figures exactly. So every delta is CORPUS MOVEMENT, and the movement has one
cause: PR #1064 archived `add-declared-former-id` on 2026-09-16, moving its
`design.md` M1/M2 fixture citations (`change-r`, `change-s`) under the excluded
`openspec/changes/archive/` path. Eight distinct tokens left, one arrived, and
only those two were ever counted — which is the whole −2.

**ALL 57 ARE CLASSIFIED AND NONE IS LEFT `unclassified`:** cross-repository 14,
tokenization artifact 4, self-referential illustrative 10, synthetic fixture 18,
never-existed 6, pre-tracking rename 1, file-half nested fixture 2, file-half
stale draft name 2. #1053's own two `unclassified` tokens are both resolved on
quoted evidence, and its "≥10" cross-repository lower bound becomes a complete
enumeration of 14. **THE DROP FROM 57 TO 39 IS NOT A REPAIR**: it is what a
human reading finds the 57 already were — 14 another repository's records, 4 not
citations at all.

**THREE HONEST READINGS OF ONE CORPUS GIVE THREE DIFFERENT REMAINDERS, AND THAT
IS THE SINGLE MOST IMPORTANT FINDING FOR D3.** At `b1df95ee`:

| reading | what it counts | remainder |
| --- | --- | ---: |
| `issue-native` (the evidence's PRIMARY) | trailing `.`/`/` stripped before dedup; `NOT_A_PACKET_REFERENCE` held OUT of the raw-absent population | **78** |
| this design's D0 table | the prose regex as written, `DANGLING` + `AMBIGUOUS` only | **81** |
| `literal` (the evidence's carried alternative) | the prose regex as written, remainder = raw-absent minus repaired | **86** |

The 81-to-86 gap is EXACTLY the five `NOT_A_PACKET_REFERENCE` tokens whose raw
path is also absent — re-derived here and confirmed at 5. The 78-to-81 gap is
the trailing-punctuation normalization of D0(ii). **None of the three is wrong;
they answer three different questions, and #1053's prose does not say which one
it asked.** That is why D3 states the recipe IN THE REQUIREMENT rather than
leaving it to an implementation: three re-implementations of one recipe have now
produced three numbers, which is precisely the drift #1053 predicted of itself
against M4 and PR #1041.

**THREE FACTS THIS RE-MEASUREMENT FOUND THAT #1053 DOES NOT CARRY.** Each moves
a decision below rather than decorating it.

**(i) THE 74 IDENTITY-HALF TOKENS ARE 48 DISTINCT IDENTITIES, AND ALL 81
REMAINDER TOKENS ARE 53 — TWO FIGURES, BOTH PRINTED, BECAUSE THEY ANSWER
DIFFERENT QUESTIONS.** The 74 is `DANGLING`(identity-half) ALONE, and 48 is what
it collapses onto; the sentence must say which half it counts, because the other
7 remainder tokens are `DANGLING`(file-half) and those DID resolve their packet —
their identity half succeeded and only the file under it is missing — so they
carry identities too. Those are **5** more, and measured, they are DISJOINT from
the 48. **Under the spec's own definition** — *"a remainder IDENTITY is one
packet id that at least one remainder token addresses"* — the remainder identity
total over all 81 tokens is therefore **53 = 48 + 5**, and the 48 is the
identity-half reading of it. Eighteen of the 48 are cited by more than one
identity-half token; twenty of the 53 by more than one remainder token of either
half:

| identity | remainder tokens | half |
| --- | ---: | --- |
| `add-council-clearance-rule-template` | 6 | identity |
| `add-openxfactory-tui-installer` | 4 | identity |
| `add-pre-archive-citation-gate` | 3 | identity |
| `foo` | 3 | identity |
| fourteen more (`2026-09-09-foo`, `add-assembly-plane-separation`, `add-demo-capability`, `add-ideation-governance`, `add-managed-service-inventory`, `add-managed-service-mapping`, `add-regular-pr-council-clearance`, `add-tenant-reader-grant-pipeline`, `add-x`, `change-x`, `clarify-gate-rules-decline-position`, `neg-neg-lin`, `prepare-openspec-1.12-readiness`, `relocate-review-authority-floor`) | 2 each | identity |
| `extend-merge-master-envelope-to-floor-bot-lanes`, `register-gate-rules-council-seats` | 2 each | file |

The five file-half identities are `define-avatar-client-contract-kernel`,
`disposition-codexfactory-floor-relocation-retitle`,
`extend-merge-master-envelope-to-floor-bot-lanes`,
`qualify-avatar-brokered-call-feasibility` and
`register-gate-rules-council-seats`.

Fifteen of the 81 tokens are a bare directory path ending in `/` whose sibling
token names the same identity without the slash. This is why D3 requires BOTH
counts: **a reader repairs identities, and the token count tells them nothing
about how much work that is.** That 48 equals #1053's hand-read "about 48" is a
COINCIDENCE OF TWO DIFFERENT QUANTITIES — #1053's 48 is 59 survivors minus
cross-repository misses and artifacts, and this 48 is 74 identity-half tokens
collapsed onto their identities. Recorded as a coincidence, never as a
confirmation; and the coincidence is one more reason the packet prints the scope
of every identity count it states, because the inclusive figure, 53, collides
with nothing.

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
PACKET EXISTED RATHER THAN PREDICTED BEFORE IT — AND STATED AS A DELTA AGAINST A
NAMED BASE, BECAUSE THE ABSOLUTE FIGURES MOVE EVERY TIME `main` DOES.** The same
recipe re-run on this branch at its head against the base that head merges:
**+6** entries in scope (this packet's own six files; `README.md` was already
tracked and the ledger row sits under the excluded `tests/`), **+8** distinct
tokens, **+6** `RESOLVED`, and the remainder **+1**. In absolutes at the pair
this bench round measured last — base `origin/main` **`4cef77af`** reading
**2,989 / 600 / 512 / 81**, branch reading **2,995 / 608 / 518 / 82**, the branch's
remainder being 75 identity-half, 7 file-half, 0 ambiguous, with 8
`NOT_A_PACKET_REFERENCE` and 70 citing files. **THE ABSOLUTE PAIR IS LABELLED
WITH ITS BASE AND IS A HISTORICAL READING; THE DELTA IS THE CLAIM.** To re-take
the absolutes at any later base, run the recipe against
`$(git merge-base origin/main HEAD)` and this branch's head. **BEFORE THE
EVIDENCE REPORT LANDED THE BRANCH'S REMAINDER DELTA WAS ZERO** — the branch read
its base's 81 — and the whole +1 arrives with `evidence/measurement-b1df95ee.md`;
the table below shows every step, each row pinned to the commit it was taken at
so no row moves when a base does.

**THE DELTA IS THE INVARIANT AND THAT IS MEASURED, NOT ASSERTED.** These figures
have now been taken at FIVE different bases — `b1df95ee`, `d5dd1ca5`,
`00b1e93b`, `fa39141c` and `4cef77af` — across four merges from `main`, thirteen
fix-round commits and the three bench rounds this paragraph has been rewritten
in. The absolutes moved with the base every time, three times inside this one
round; **`+6 / +8 / +6 / +1` did not move once.** Neither a merge nor a
prose correction mints a citation token the branch did not already carry.
**That is the fence working rather than a coincidence**: the tokens a packet adds
are the ones it QUOTES, and a correction that re-words a sentence about a token
quotes the token that was already there — which is also why the one place this
round had to describe a new token rather than spell it (D7's note on vendoring
the instrument) describes it.

**AND THE COMMITTED EVIDENCE REPORT DID WHAT D5 SAYS A COMMITTED REPORT DOES.**
Watch the population move as this packet was assembled, each reading taken with
the same recipe on the same branch, at the commit named:

| tree | files | tokens | `RESOLVED` | remainder |
| --- | ---: | ---: | ---: | ---: |
| `origin/main` `b1df95ee` | 2,973 | 586 | 498 | **81** |
| + the packet's five documents (`e87afeb1`) | 2,978 | 586 | 498 | **81** |
| + the README bullet and the ledger row (`daea4c34`) | 2,978 | 587 | 499 | **81** |
| + `tasks.md`'s mechanical fence proof (`3b4f1e12`) | 2,978 | 587 | 499 | **81** |
| + `evidence/measurement-b1df95ee.md` (`b07a4885`) | **2,979** | **594** | **504** | **82** |

**THE MEASUREMENT REPORT RAISED THE MEASURED REMAINDER BY ONE.** Diffing the
token sets at `1dd7b37d` and `b07a4885` gives SEVEN new tokens exactly: five name
the packet's own files (carried by `tasks.md`'s fence proof, all `RESOLVED`),
`…/archive/2026-09-15-` lands as `NOT_A_PACKET_REFERENCE`, and the seventh is the
remainder — `openspec/changes/foo/`, a `DANGLING`(identity-half) token minted out
of the evidence report's § 5.3 enumeration of the resolver's docstring examples.
**AND IT IS NOT THE EVIDENCE REPORT ALONE THAT CARRIES IT.** At that commit the
token's citing set is FOUR files — the evidence report, and `design.md`,
`proposal.md` and `tasks.md`'s own paragraphs ABOUT the +1, which quote the token
to say what it is. That is the same mechanism one level up, and it is why D3(a)'s
output-path fence is written before any output exists rather than after.
The packet's FOURTEEN citation tokens divide exactly: SIX name its own files
(the five documents and the committed evidence report) and all six resolve; THREE are `openspec/changes/archive…` debris the resolver
correctly hands back as `NOT_A_PACKET_REFERENCE`; and the remaining FIVE are
REMAINDER ENTRIES it joins the citing set of by QUOTING them — `README.md`,
`add-composition-drift-cascade/`, `add-ideation-governance/proposal.md`,
`foo/` and `foo/./proposal.md`.

**THIS IS NO LONGER A PREDICTION.** D5 argues that a report committed into the
corpus is counted by the next run, and here is the smallest possible instance
of it, measured: ONE report, ONE night, **+1 remainder**. A nightly report
would carry one such quotation per remainder line, every night, and D3(a)'s
output-path exclusion is the fence that closes it. **A DOCUMENT THAT DISCUSSES
A DANGLING CITATION BECOMES A RECORD THAT CARRIES ONE** — which is #1053's
"self-referential illustrative example" class being created, live, by the
packet that characterizes it. **THE FIGURES IN THIS PARAGRAPH MOVED THREE TIMES
WHILE IT WAS BEING WRITTEN** — the last time because `tasks.md`'s fence proof
came to list the evidence file itself, which is one more self-citation that
resolves. Every move is in the table above rather than quietly re-typed, and the
reading is taken at this packet's final committed state, the act of recording it
being part of what it records.

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
    [--json] [--all] [--tokens] [--history]
    [--include PREFIX ...] [--exclude PREFIX ...]

REPO_ROOT       repository root to scan (default: cwd), as every sibling
                scripts/validate-*.py already spells it
--json          machine-readable output instead of the human table
--all           also list RESOLVED and NOT_A_PACKET_REFERENCE tokens, which
                the default output only COUNTS
--tokens        group by TOKEN; the DEFAULT groups by IDENTITY (see below)
--history       OPT-IN: run the `git log --all --diff-filter=A` probe per
                identity. OFF by default, on a MEASURED 8.5x cost
--include/--exclude   REFINE the default file population — prefix semantics,
                precedence and the one exclusion neither can lift are fixed
                immediately below — so the recipe in D3 is a DEFAULT and not a
                hard-coding
```

**`--history` IS OPT-IN ON A MEASURED COST, NOT A PREFERENCE.** The probe RUNS
PER IDENTITY, NOT PER TOKEN: it caches on the identity key and invokes
`git log --all --diff-filter=A` only on the first token under each identity,
every later token sharing that identity re-using the cached answer instead of
re-running the probe (PR #1069, Copilot threads `PRRT_kwDOTAvnrs6jXaNU` and
`PRRT_kwDOTAvnrs6jXaPJ`). In the evidence run that is **38 identities, 76
invocations** (a literal-pathspec form and a corrected form, each run once per
identity) — measured at **17.0 of 19.0 seconds — 90% of the whole run** — and
it returned empty for **33 of the 38 identities**, equivalently 51 of the 57
tokens they cover (every token under one identity shares its identity's
answer), which the resolver had already said. It decides exactly ONE thing
the resolver cannot: an id that STOOD here and was renamed before former-id
tracking, against one that never stood here at all. Worth a flag; not worth the
default. **Without it the sweep is 2.0 seconds over 2,973 entries in scope
(2,969 files read)**, which is the difference between a report somebody runs
and a report somebody schedules.

**`--include` AND `--exclude` ARE GIVEN THEIR SEMANTICS HERE, BECAUSE A FLAG
NAMED IN A SURFACE THAT EXISTS SO THE REALIZATION CANNOT DRIFT, AND THEN NOT
DEFINED, IS A FLAG TWO REALIZATIONS WILL IMPLEMENT DIFFERENTLY.** A population
that differs between two runs breaks the only thing this capability produces — a
SERIES — and "override the default file population" answers none of the three
questions an implementer actually has. Four rules, and they are the whole of it:

1. **A PREFIX MATCHES ON PATH SEGMENT BOUNDARIES**, never as a bare string
   prefix: a path matches when it EQUALS the prefix with any trailing `/`
   removed, or begins with that plus `/`. This is the estate's own idiom rather
   than a new one — `scripts/validate-carve-manifest.py`'s `in_surface`
   (`:1653-1663`), whose docstring states the reason in one line: *"Segment-aware:
   `scripts/ideation_dashboard` does not swallow
   `scripts/ideation_dashboard_old/x.py`, which a bare `startswith` would."*
2. **BOTH FLAGS REFINE D3(a)'s POPULATION AND NEITHER REPLACES IT.** `--include`
   RE-ADMITS tracked entries under its prefixes that one of D3(a)'s three default
   exclusions removed — `--include tests/packet_reference` is how a reader asks
   about one fixture corpus deliberately — and `--exclude` REMOVES more. Passing
   neither leaves D3(a) exactly as written. *The alternative, `--include`
   REPLACING the population, is declined:* it makes a single `--include`
   silently DISCARD the corpus rather than widen it, which is the opposite of
   what a reader narrowing a question expects, and it would let a caller produce
   a headline remainder over three files that reads like a headline remainder
   over the corpus.
3. **`--exclude` IS APPLIED LAST AND WINS** on any path both flags name, so the
   pair is order-independent: a reader predicts the population without knowing
   which flag was typed first, and a wrapper that appends an `--exclude` cannot
   have it undone by an earlier `--include`.
4. **NEITHER FLAG CAN RE-ADMIT THE REPORT'S OWN OUTPUT PATH.** That exclusion is
   not a default and is not the caller's to lift: it is a promoted requirement —
   *"THE REPORT'S OWN OUTPUT SHALL BE EXCLUDED FROM THE POPULATION wherever that
   output is committed"* — and a flag that could turn it off is a flag that can
   restart the self-counting D5 exists to prevent.

**AND WHATEVER THE FLAGS SAY, THE REPORT STATES THE POPULATION IT ACTUALLY USED
AND THE OVERRIDES IT WAS GIVEN**, which the spec's population requirement
demands, so a reading taken under a refined population can never be read as one
taken under D3(a).

**GROUPING IS BY IDENTITY BY DEFAULT, AND THAT IS MEASURED TOO.** The evidence's
57 this-tree tokens are **38 identities**, twelve carrying more than one
spelling: five rows are one packet spelled five ways, four are one
questionnaire's sketch, three are one OpsxFactory register spelled active and
archived. A flat token list makes one act look like five findings.

**AND GROUPING NESTS RATHER THAN COLLAPSES — EVERY TOKEN IS LISTED IN EVERY
MODE** (PR #1069, Copilot thread `PRRT_kwDOTAvnrs6jIP3K`). The promoted
requirement is explicit that where several tokens address one identity *"each
token MUST still appear in the itemized remainder"*, so the default cannot show
one identity row carrying the first spelling and a count and call the other
spellings reported. Under the default the IDENTITY is the row and ITS TOKENS
ARE LISTED BENEATH IT, each with its own occurrences; `--tokens` changes the
ORDER things are grouped in and NEVER what is listed. The identity total still
counts the identity once — that is what the grouping is for — and the token
total still counts every spelling.

**THE OUTPUT, SHAPED BY THE HAND CLASSIFICATION RATHER THAN IMAGINED.** A human
table grouped by CLASS then by IDENTITY — counts first, then the remainder
itemized — plus, under `--json`, one object per token carrying `token`,
`status`, `half`, `identity`, `remainder`, every OCCURRENCE as `path:line`,
`class` and every flag. Six rules the evidence's § 6.3 derives from doing the
classification by hand, each adopted here:

1. **Print the resolver's own `report` sentence** for the first occurrence, and
   do not re-write it in a second voice — that is how two descriptions of one
   rule drift apart.
2. **Print the counted rows AND their arithmetic**, so a reader can check
   `raw-missing = repaired + identity-half + file-half + ambiguous +
   not-a-reference-with-no-raw-path` without re-deriving it. A remainder that
   does not sum is the first sign the reading changed — **AND THE FIFTH TERM IS
   NOT OPTIONAL**: a token the resolver declines to read as a packet reference
   at all can still have no path in the tree, and at `b1df95ee` five do. A
   four-term identity reads `76 + 74 + 7 + 0 = 157` against a raw-missing set
   of **162** and would either fail or conceal exactly those five (D0's
   partition above; PR #1069, Copilot thread `PRRT_kwDOTAvnrs6jFQmQ`).
3. **State the READING in the header** — the dedup normalization, whether
   `NOT_A_PACKET_REFERENCE` sits inside or outside the population, and the
   ANY-vs-ALL qualifier aggregation. D0's three-readings table is why.
4. **Show `AMBIGUOUS` even when it is zero.** It is the only outcome that
   indicts a `former_ids:` DECLARATION rather than a citation, and a report that
   omits its zero teaches readers not to look for it.
5. **Carry every occurrence into `--json`**, because the manual read is where
   the time goes and it is done in an editor over the JSON, not over the table.
6. **Both formats carry the headline numbers**: the POPULATION PAIR — tracked
   ENTRIES in scope and FILES read, neither standing for the other — distinct
   tokens, remainder TOKENS, remainder IDENTITIES.

**THE EXIT CODE IS 0 ON A FINDING AND NON-ZERO ONLY WHEN THE REPORT COULD NOT
RUN, AND A `--fail-on` IS EXPLICITLY NOT BUILT.** The requirement states the
two-case contract exactly: *"The report SHALL exit successfully whatever it
finds, and SHALL NOT provide an option that makes a finding fail a run"*, and
*"A NON-ZERO EXIT SHALL MEAN THE REPORT COULD NOT RUN, never that it found
something"* (`specs/packet-citation-report/spec.md`, Requirement: The citation
remainder report is advisory and gates nothing; PR #1069, Copilot thread
`PRRT_kwDOTAvnrs6jXaPs`). Exit 0 on any finding is what makes this a report
rather than a gate: nothing about the 81 tokens has been ruled a defect, and a
tool that can exit non-zero acquires that meaning the first time somebody
wires it into CI. `--fail-on` is RESERVED for option (a) under D1, where a
severity decision will have been taken by ruling. The only non-zero exit is
the ordinary one for a tool that CANNOT RUN — an unreadable tree, a root that
is not a git work tree — which is a different fact from a finding and says so.

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

**AND ONE ENTRY CLASS THE POPULATION SKIPS RATHER THAN EXCLUDES: A TRACKED
ENTRY THAT IS NOT A FILE.** `git ls-files` names four mode-160000 SUBMODULE
GITLINKS in scope (`installs/omnigent-install`, `openDox`, `openXdox`,
`openXwallet`) — directories with no text of their own. They are skipped and
contribute no token. This is stated because the alternative reading, "four
binary files read with character replacement", is DIFFERENT CODE and a different
fixture in § 2.1: measured on both trees, **no in-scope file is binary at all**
— zero carry a NUL byte, zero fail a strict UTF-8 decode.

**AND THE ENTRY CLASS THAT IS NOT HERE TODAY BUT WHOSE RULE MUST BE, BECAUSE THE
NAIVE IMPLEMENTATION IS WRONG ON IT: A SYMBOLIC LINK.** Measured rather than
assumed, at `b1df95ee` and again at this branch's head: `git ls-files -s | awk
'$1=="120000"'` returns **ZERO** at both. This repository tracks no symlink at
all today — at `b1df95ee` its 5,466 tracked entries are 5,462 regular files
(5,415 `100644` and 47 `100755`) and the 4 gitlinks above, and nothing else.
**THE RULE IS STATED ANYWAY, AND IT IS STATED IN THE
REQUIREMENT RATHER THAN LEFT TO THE REALIZATION**, because the obvious
implementation of D3(a) — `Path.is_file()` then `read_text()` — is a WRONG
implementation the day one link arrives: both tests FOLLOW the link and answer
about the target, so a link pointing out of the tree is read as though its
target's text were this corpus's, and its citations are reported as this
repository's. The report admits a link's text only after RESOLVING the entry and
finding it still under the root. **THAT IS THE RESOLVER'S OWN BOUNDARY, NOT A
NEW ONE**: `scripts/packet_reference.py`'s `_contained` (`:260-284`) resolves a
path "following every symlink in the chain" and returns it "only where it still
stands inside `root`", crediting the same idiom to
`scripts/validate-pin-registrations.py`'s `resolve_in_tree`. A population that
did not apply it would hand the resolver text the resolver would refuse to walk
to. (openxFactory PR #1069, Copilot thread `PRRT_kwDOTAvnrs6jCbwO`.)

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
  concatenation-split path and the tool cannot know the rest — **BUT THE
  TRAILING HYPHEN IS A SUSPICION AND NOT A VERDICT, AND RESOLUTION IS TRIED
  FIRST** (PR #1069, Copilot thread `PRRT_kwDOTAvnrs6jIP4S`): this estate's
  canonical change-id grammar is `[A-Za-z0-9][A-Za-z0-9._-]*`
  (`scripts/proposal-support.py`'s `CHANGE_ID_RE`, the one spelling all three
  readers share), and it ADMITS an id that ends in `-`, so a blanket rule would
  suppress a valid citation as a tokenization artifact. The report therefore
  RESOLVES the token first and classes it `truncated` only where it does not
  resolve; a valid resolver match WINS. Measured, nothing in this reading moves:
  **no id ends in `-` today** — 0 of the 48 active and 0 of the 169 archived
  packet directories — and both `-`-terminated remainder tokens at `b1df95ee`
  are genuinely severed paths that resolve to nothing;
- a `/./` segment is left exactly as it is, because `packet_reference`'s own
  `_normalised` already drops it.

**Every normalization the report applies is printed in its own row.** A reader
who cannot see that the tool changed the token cannot check the tool.

**AND THREE STEPS #1053'S PROSE DOES NOT STATE MUST BE STATED HERE, BECAUSE
THEY ARE WORTH EIGHT POINTS OF REMAINDER BETWEEN THEM.** The evidence
measurement re-ran #1053's recipe EXACTLY AS ITS PROSE READS IT and got 593
distinct tokens at `8944758c`, not the published 578; three decisions close the
gap, and each is a CHOICE a shipped report must make on purpose:

| step | the choice | what it is worth |
| --- | --- | ---: |
| trailing `.` and `/` stripped BEFORE dedup | **strip** — otherwise one citation is two tokens | 593 → 578 at `8944758c`, the issue's count to the token |
| `NOT_A_PACKET_REFERENCE` held OUT of the raw-absent population | **out** — the resolver's fifth answer hands the path back to the caller, so it was never a remainder | 156 → 153 raw-absent; and at `b1df95ee` it is exactly the 5 tokens separating this design's 81 from the literal reading's 86 |
| a token cited in several places, ONE of them qualified | **ANY occurrence qualified sets it aside** — which is the rule that reproduces #1053's own 22 | ANY sets aside 22 and leaves 57; ALL sets aside 16 and leaves 60 |

**AND ALL THREE ARE NOW IN THE PROMOTED TEXT AND NOT ONLY HERE**, together with
the extraction pattern itself. D3's recommendation is that the recipe live in
the REQUIREMENT; a requirement that promised a stated grammar and then stated
only the corrections applied to it would not have kept that promise, and
`design.md` is a working file that no realization is measured against. The spec
delta's *The reported population is derived from a stated recipe* now carries the
pattern verbatim and fixes the three choices above, with a scenario refusing a
reading taken under different ones a place in the same series (PR #1069, Copilot
thread `PRRT_kwDOTAvnrs6jCbzN`).

**THE REPORT DECLARES ITS READING IN ITS OWN HEADER** (D2 output rule 3), so
two runs that disagree can be told apart by a reader rather than by an
archaeologist. #1053 itself predicted this class of drift — *"a
RE-IMPLEMENTATION of M4's stated recipe, not the authoring script, which was
never committed"* — and three readings of one corpus have now produced 78, 81
and 86.

**(c) THE CROSS-REPOSITORY QUALIFIER, AND THE DECISION THAT MATTERS HERE: FLAG,
NEVER DROP.** #1053's automated check uses FIVE adjacency signals — a
path-joined prefix (`xFactories/LedgerxFactory/…`), a GitHub blob or tree URL, a
bare qualifier word immediately before the token (`codexFactory
openspec/changes/…`), **the `opsx:opensoft/…` CUSTODY-LOCATOR SCHEME this corpus
writes OpsxFactory citations in** (**24** occurrences across the tracked tree at
`b1df95ee`, **19** of them inside D3(a)'s own file population; and **FOUR** of
the evidence's fourteen hand-found cross-repository tokens are OpsxFactory's —
and worth saying because it is the kind of thing a signal list gets credited
with wrongly: NONE of those four is caught BY this scheme, the evidence
attributing all four to an adjacent qualifier word or a parenthetical. The
scheme is in the set because #1053's automated check uses it and because this
corpus writes citations in it, not because it is what found these), and
a trailing `(RepoName)` parenthetical — and #1053 itself measures their limit: *"the automated qualifier check only catches a
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

**AND WHETHER THE NUMERAL ITSELF BELONGS IN THE PROMOTED TEXT WAS A RATIFIER'S
CHOICE, NOT AN AUTHOR'S — AND THE RATIFIER HAS NOW MADE IT.** Review asked for
"the citing line plus the three lines above" to be promoted into the requirement
(PR #1069, Copilot thread `PRRT_kwDOTAvnrs6jEu29`), and the reproducibility
argument behind the ask is sound. The packet was FILED carrying only the half
that costs a ratifier nothing: the window and the signal set are properties of
the CAPABILITY rather than of a run — both fixed, both closed, no caller option
that varies either — so two runs of one report cannot disagree, and the HEADLINE
remainder is inclusive by the requirement beside it, so no window can move the
series D6 measures. **THE NUMERAL WAS DELIBERATELY LEFT HERE AND NOT PROMOTED AT
FILING**, because THREE is this section's RECOMMENDED value and this section is
one of the seven put for a word: D3(c) calls the window "a guess" derived from
#1053's observation and nothing else, and a veto that cost one design paragraph
would have cost a promoted requirement instead.

**AND THE STEP NAMED HERE — *"IF THE RATIFYING WORD TAKES D3(c) AS RECOMMENDED,
THE WINDOW AND THE FIVE SIGNALS SHOULD MOVE INTO THE REQUIREMENT AT THAT POINT"*
— HAS NOW BEEN TAKEN, ON THE WORD AND NOT ON A BENCH WRITER'S OWN.** The
ratifying word took D3(c) as RECOMMENDED (the bare *"ratify #1069"*, tasks.md
§ 1.17), and Brett Heap then asked for exactly this step, 2026-09-17T12:32:38Z,
verbatim **"fold it in before landing"** ([PR #1069, comment
5714405516](https://github.com/opensoft/openxFactory/pull/1069#issuecomment-5714405516)).
The THREE-line window and the FIVE signals above therefore now stand in
`specs/packet-citation-report/spec.md`'s *A suspected cross-repository citation
is flagged and never dropped* as normative text with scenarios of their own: the
window fixed as the citing line plus the three lines above it, the five signals
named in THIS SECTION'S ORDER and closed at those five, one scenario per signal,
one for a signal two lines above a citing line that IS flagged, and one for a
signal four lines above that is NOT. **NO DECISION MOVES WITH IT**: FLAG-never-drop,
the INCLUSIVE headline and the ADVISORY verdict read exactly as they read
before, and this section keeps the recommendation and the two alternatives it
was ratified on.

**AND THE WIDENED WINDOW IS NOW MEASURED RATHER THAN PROPOSED.** The evidence
ran exactly this rule — `validate-pin-registrations.py`'s own adjacency rule
plus any repository name in the THREE LINES ABOVE — over the classified corpus:
it catches **13 of the 14** hand-found cross-repository tokens, with **2 false
positives** among the other 43. That precision is why it ships as an ADVISORY
FLAG and never as a verdict, and it is the measured form of the recommendation
above rather than a hope about it. The one token no adjacency rule can reach is
`…/archive/2026-08-27-modify-ledgerx-document-estate-warrant-scope/design.md`,
whose evidence block names no repository at all — the only tell is that a
SIBLING path in the same block does not exist in this tree. That one is human,
and the report's job is to make it cheap to check rather than to decide it.

**ONE ARITHMETIC POINT THE REPORT MUST NOT GET WRONG**, because #1053's own
table reads oddly without it: the "22 cross-repository tokens set aside" is
counted over the WHOLE token population, and only **21** of the 22 sit in the
raw-absent population — the 22nd is a cross-repository citation whose raw path
happens to exist here. That is why `153 − 22 ≠ 132` while `153 − 21 = 132`.
Both counts hold unchanged at `b1df95ee`.

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

**(e) THE HISTORY PROBE'S PATHSPEC, CORRECTED.** #1053 states its never-existed
confirmation as

```text
git log --all --diff-filter=A -- "openspec/changes/<id>" "openspec/changes/archive/*-<id>"
```

**The SECOND pathspec matches nothing, on any input.** Git matches a wildcard
pathspec with wildmatch under `WM_PATHNAME`, where `*` does not cross a `/`, so
`openspec/changes/archive/*-<id>` is tested against full file paths like
`openspec/changes/archive/2026-09-15-<id>/proposal.md` and never matches one.
Proven on a packet known to be archived: `…/archive/*-add-declared-former-id`
returns 0 commits and `…/archive/*-add-declared-former-id/*` returns 1. **The
conclusion #1053 drew is nonetheless sound** — the evidence ran BOTH forms over
every remainder identity and they agree on all 57, because every archived packet
was active first, so the only case the broken half could hide is a packet that
appeared in the archive without ever being active, and this corpus has none.
**A shipped report spells it `…/archive/*-<id>/*`**, and runs it only under
`--history` (D2).

## D4 — RECOMMENDED: classify only what can be decided mechanically

**The question.** #1053's manual read puts the remainder in nine classes. How
many of them does a machine get to assert?

**RECOMMENDED — OPTION 1: A SMALL MECHANICAL SET, AND AN HONEST `unclassified`
FOR EVERYTHING ELSE.**

**AND A CLASS AND A FLAG ARE DIFFERENT THINGS HERE, SAID ONCE SO THE TWO TABLES
BELOW READ THE SAME WAY.** A CLASS is what the report ASSERTS about an entry and
is counted in the class totals D6's series is read from. A FLAG is what the
report SUSPECTS, carried in its own `--json` field beside `class` (D2's output
model) and never folded into a class count. `possibly-cross-repo` is a FLAG on
that split, not a class, everywhere in this packet: the entry keeps whatever
class its own evidence supports — usually `unclassified` — and carries the
suspicion alongside.

| #1053's class | report's verdict | why |
| --- | --- | --- |
| cross-repository (adjacency-missed) | **MECHANICAL, but a FLAG and NEVER a class** — `possibly-cross-repo` | D3(c): the window is stated, the hit is FLAGGED, the token stays in the count — and the flag sits in its own `--json` field beside `class`, so a suspicion is never counted as a classification |
| pure tokenization artifact | **MECHANICAL** — `truncated` / `punctuation-stripped` | D3(b): the tool knows what it did to the token, and three sub-probes catch 4 of 4 with ZERO false positives — where #1053's hand read found 1 of the 4 |
| DANGLING file-half, nested test fixture | **MECHANICAL** — `fixture-path` | the citing file's own path is under a `tests/` directory nested below the top-level exclusion; that is a path fact |
| synthetic fixture id under `examples/` or `ideation/dashboard/gate-records/` | **MECHANICAL** — `fixture-path` | same: the CITING file's location is knowable |
| self-referential illustrative example in a docstring | **HUMAN** — `unclassified`, with an ADVISORY `scripts/`-location flag beside it | the class needs a reading of what the prose is DOING; measured, location alone catches 10 of 12 but with 2 false positives, so it suggests and never asserts |
| id that never existed | **HUMAN** — `unclassified` | needs `git log --all --diff-filter=A` over two spellings, and a negative result is not proof of intent |
| pre-tracking rename | **HUMAN** — `unclassified` | needs the rename's history and a judgment that no `former_ids:` covers it |
| stale draft name, since finalized | **HUMAN** — `unclassified` | needs somebody to recognize the finalized file |
| unclassified | **HUMAN** — `unclassified` | it is already the honest answer |

**AND THE VOCABULARY, THE FLAG FIELDS AND THE PRECEDENCE ARE NOW IN THE PROMOTED
TEXT**, not only in this table: the spec's *The report classifies only what it
can decide mechanically* closes the vocabulary at `truncated`,
`punctuation-stripped`, `fixture-path` and `unclassified`, forbids a flag being
written into the class field or counted in a class total, and fixes the
precedence — a class about the report's own NORMALIZATION beats one about a
LOCATION. That precedence is not invented here: it is the order the evidence's
own § 5.1 decision rule uses, where *tokenization artifact* is read before
*synthetic example/fixture* so a token re-read lands in the same class twice.
An entry's DANGLING half is reported as a resolver OUTCOME under the first
requirement and is not re-spelled as a class name (PR #1069, Copilot thread
`PRRT_kwDOTAvnrs6jEu3i`).

**AND D4's OWN PRECISION TABLE BELOW IS CORRECTED TO SAY THE SAME** (PR #1069,
Copilot thread `PRRT_kwDOTAvnrs6jFQnV`): the `half == file` probe is free and
perfect — 5 of 5, no false positives — and it SHIPS, but as the OUTCOME the
resolver already returns and not as a member of the closed class vocabulary. A
document that closes the vocabulary at four labels, requires exactly one class
per entry, and then calls a fifth thing a class leaves a realization unable to
satisfy both halves and its class totals ambiguous. **NOTHING IS LOST BY THE
CORRECTION**: every file-half entry is still named, still counted, still
itemized under its own outcome, and its `class` is whatever its own evidence
supports — `fixture-path` for the nested-fixture ones, `unclassified` for the
rest. **AND THE OTHER READING IS STILL RATIFIABLE**: rule for a named
`file-half` CLASS, counted in the class totals, and D4 takes it — minting a
member of a closed vocabulary is a decision for the word, not for a review
round.

**WHY THE SPLIT FALLS THERE.** A class is MECHANICAL when the evidence is a
fact about a PATH or about the tool's own normalization, and HUMAN when the
evidence is a fact about INTENT. `unclassified` is not a failure of the report —
it is the report declining to assert what it cannot see.

**AND THE SPLIT IS NOW MEASURED RATHER THAN REASONED.** The evidence
measurement classified all 57 this-tree tokens by hand and then ran each
candidate probe against that ground truth. The precision decides whether a probe
ships as a CLASS (the report asserts it) or as an ADVISORY FLAG (the report
suggests it):

| probe | catches | false positives | ships as |
| --- | ---: | ---: | --- |
| synthetic fixture, by occurrence LOCATION (`examples/`, `ideation/dashboard/gate-records/`, `contracts/**/examples/`) | 17 of 18 | **0** | **a CLASS** |
| tokenization artifact, three sub-probes (a longer path on the line ends with the token and EXISTS; the next character is `<`; the token ends a string literal and the rejoined path resolves) | **4 of 4** | **0** | **a CLASS** |
| `half == file` | 5 of 5 | 0 | **AN OUTCOME, NOT A CLASS** — free, being `Resolution.half`, and already itemized as the resolver's own answer under the delta's first requirement; the class vocabulary is CLOSED at `truncated`, `punctuation-stripped`, `fixture-path` and `unclassified`, and minting a fifth member is a RULING (below), not a bench round's act |
| `possibly-cross-repo`, adjacency plus the three lines above | 13 of 14 | 2 of 43 | **an ADVISORY FLAG** |
| self-referential, by occurrence under `scripts/` | 10 of 12 | 2 | **an ADVISORY FLAG** |

**TWO THINGS MOVED ON THE MEASUREMENT AND ARE RECORDED AS HAVING MOVED.** The
tokenization-artifact probe catches **4 of 4 with zero false positives**, where
#1053 read that class by hand and found ONE of the four — so it earns a class
rather than a flag. And *self-referential*, which this design's first draft
placed in the HUMAN column, turns out to be 10-of-12 detectable by location
alone — but at 2 false positives it ships ADVISORY, not as a class, which is the
same verdict for a different reason.

**WHAT STAYS HUMAN, ON THE EVIDENCE'S OWN WORDS.** *never-existed* versus
*synthetic* is a question about INTENT and nothing in the tree answers it:
`add-invoice-retrieval` and `add-openxfactory-tui-installer` are both absent
from history and both live under `docs/`, and only reading the surrounding
sentence separates a worked example from a forward-looking sketch. The two
file-half repair classes are likewise human — both resolve their packet and
neither carries its file, and the difference is whether a test ASSERTS the
absence or a rename left it behind.

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
same 81 lines the issue already has, and the asserted classes — `truncated`,
`punctuation-stripped` and `fixture-path`, with the free `half == file`
itemized beside them as the resolver's own outcome — are exactly the ones a
human should never have to re-derive.

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
HYPOTHETICAL AND THIS PACKET PROVED IT ON ITSELF**: committing ONE measurement
report — `evidence/measurement-b1df95ee.md`, a single file, once — took the
measured remainder from **81 to 82** (D0(iv) carries the five readings, each at
the commit it was taken at). The new entry is `openspec/changes/foo/`, minted by
the report's own enumeration of the resolver's docstring examples — and carried,
at that commit, by the evidence report **and by this design's, the proposal's and
the tasks file's own paragraphs about it**, which is the same act at packet scale
rather than a different one. One report, one night, one point of remainder;
a nightly report is that act repeated forever, and every point of it is
manufactured rather than found. The fence (D3(a)) closes it,
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
   on ARRIVALS, not on the standing population; a standing 53 (D0(i)'s inclusive
   remainder identity count) that never moves costs a gate nothing, while three
   unexplained arrivals a week is what a gate is for.
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

**AND ONE THING FENCE 1 DOES NOT FORBID BUT THIS PACKET STILL DECLINES: VENDORING
THE MEASUREMENT INSTRUMENT.** `evidence/measurement-b1df95ee.md` is committed and
its 862-line instrument `measure.py` is not, which a reviewer reasonably reads as
a reproducibility gap (PR #1069, Copilot thread `PRRT_kwDOTAvnrs6jCby5`). Putting
the instrument in `evidence/` would breach no fence above — a file under
`openspec/changes/…/evidence/` is a PACKET ARTEFACT and not a member of
`scripts/`, so no validator arm, no gate import and no `scripts/` surface moves —
and the option is nonetheless declined on two measured costs:

1. **IT WOULD RAISE THE NUMBER THIS PACKET REPORTS.** `measure.py` carries five
   `openspec/changes/…` tokens; measured against this branch's token set, TWO are
   new, and one of them — the UNSLASHED spelling of the same `foo` docstring
   example this branch already carries with a trailing slash — resolves
   `DANGLING`(identity-half). Committing the instrument is **+1 remainder**, a
   second instance of D5's own mechanism taken for no additional reading. The
   packet would be manufacturing remainder in order to document remainder.
   *(That spelling is described rather than written out, deliberately: writing it
   here would mint the very token this sentence is about, which is D3(a)'s lesson
   and not a hypothetical — D0(iv) records the branch doing exactly that once
   already.)*
2. **IT WOULD MOVE THE `code_surface:` DECLARATION**, which is the one
   front-matter value in this packet that was RUN against a live reader rather
   than reasoned about (the probes above). `.openspec.yaml` says this pull request
   "adds no script, no workflow and no test" and the declaration's gloss says
   "THIS pull request carries the PACKET ONLY"; both would have to change, and the
   changed head would owe a fresh probe against PR #1029's
   `scripts/validate-code-surface.py`. That is a scope move, and a bench round is
   not where a scope moves.

*What is done instead:* the evidence's header now states where the instrument
stands (`opensoft/brett-wip`, repo-relative path), and separates what a clean
checkout reproduces without it — D0's outcome counts, reproduced twice by
independent re-implementations — from what no instrument reproduces, which is the
§ 5 hand read of INTENT that D4 exists to keep out of a machine's hands.

*OPTION 2 — leave the fences to the realization's own judgment.* Cost: the
realization is a later pull request on a later word, possibly by a different
hand; a fence written after the fact is a post-mortem.

## What is NOT decided here

- **The nine manual classes ARE re-derived, and this line used to say they were
  not.** D0's named slot is FILLED: `evidence/measurement-b1df95ee.md` § 5 carries
  a hand read of all 57 this-tree tokens with an evidence line each, and D4 ships
  every probe's measured precision against that read. What is NOT re-derived is
  #1053's own classification of its own 59 at its own revision; where the two
  differ, the evidence's § 5.2 names why and this packet quotes both rather than
  overwriting one with the other.
- **`N = 14` and "at most 3 arrivals" in D6 are proposed numbers.** They are
  derived from nothing but the shape of a two-week window and are the most
  vetoable figures in this packet.
- **The report's exact table layout** is the realization's, within the fields
  D2 fixes.
- **Whether option (a) is ever taken** is D6's trigger plus a later ruling, and
  this packet neither takes it nor forecloses it.
