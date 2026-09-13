# Design: gate-code-surface-declarations

Status: ratified
Ratified by: gate-code-surface-declarations — 2026-09-13, Brett Heap, verbatim "ratify" (recorded at https://github.com/opensoft/openxFactory/pull/1018#issuecomment-5649742729)
Kind: design

**EVERY DECISION THIS AUTHORING SESSION TOOK IS HERE, WITH ITS ALTERNATIVE AND
THE ALTERNATIVE'S COST.** Taking openxFactory issue
[#1013](https://github.com/opensoft/openxFactory/issues/1013) — an UNCLAIMED
residue another lane filed at the archive of `gate-realization-axis-vocabulary`
— commissioned this authoring and took none of them.

**THE FOUR DECLARED VETO POINTS WERE D1, D2, D3 AND D4, AND ALL FOUR ARE NOW
RULED.** Brett Heap ratified this packet on 2026-09-13 at 00:41Z, verbatim
**"ratify"**, recorded at
[#1018](https://github.com/opensoft/openxFactory/pull/1018#issuecomment-5649742729).
**THE WORD IS BARE AND THAT IS RECORDED AS WHAT IT IS**: unlike the sibling's
three labelled rulings, it names no option individually — it ratifies the PACKET,
and the packet encodes the RECOMMENDED option at each of the four, so **D1 =
GATE THE GRAMMAR**, **D2 = VALIDATOR PLUS CLOSED REGISTER PLUS ADDED
REQUIREMENT**, **D3 = REGISTER ALL SEVEN**, **D4 = REUSE AS THE CONSUMER AND
NARROW THE EXTRACTOR**. Each was the recommended and already-encoded option, so
**nothing in the delta moves on the ruling**; D0 and D5 through D8 were carried
beside them and none was vetoed. The alternatives below are retained as the
record of what was put and declined, not as work owed.

**THE RULING REACHES THE FIRST BENCH ROUND TOO, ON ITS OWN WORDS**, which direct
that the two confirmed findings be fixed *"before the record is cut, so the
ratified packet includes them"*. **D9** records both, and the ratified text is
the text they produced.

## 0. The brief

openxFactory #1013, filed as the successor `gate-realization-axis-vocabulary`
`tasks.md` § 6.3 owed: *"`code_surface:` IS NOT GATED. The other half of the
same sentence is equally unread; it is a second population with its own classes,
and folding it in here would widen a ruled remedy into an unruled sweep."* The
issue names three design questions and leaves the sizing to a taker:

1. what counts as "off-vocabulary" when the declared values are free prose
   repository lists;
2. whether a closed register or an ADDED requirement alone is the right shape;
3. whether `add-structured-scope-substrate`'s `scope_globs:` machinery is
   reusable.

D1, D3 and D4 answer them in that order; D2 is the shape question the issue's
(2) opens.

## D0 — the measurement, taken before the design

**NOTHING BELOW RESTS ON A NUMBER ANYBODY TYPED, AND THE ISSUE'S OWN FIGURES ARE
RE-TAKEN RATHER THAN CARRIED.** Every figure was measured on a fresh clone at
`origin/main` `bcde1575f060e6ee764a11bfe12610dec4a0d8da`, and on a worktree of
that same commit, by a stated method:

- **the population** is `openspec/changes/<change>/proposal.md`, ONE level deep,
  the `archive` directory excluded — the same top-level scan
  `scripts/target_release.py`'s `_proposals` performs, and never an `rglob`,
  because about a hundred `tests/doc-health/fixtures/**/proposal.md` carry this
  front matter as fixture text for other families;
- **a declaration** is a `^code_surface:` line INSIDE the leading `---` fence,
  read through the SHIPPED strict loader
  `scripts/frontmatter_strict.read_front_matter`, so this measurement and the
  house loader refuse the same documents;
- **the head** is the longest prefix of the declaration that reads as `none`, or
  as repository identifiers separated by `,` / ` and ` / ` + `;
- **the archive** is read one level down, counted, and judged never.

**THE ISSUE'S TABLE, RE-TAKEN:**

| measure | #1013 at filing | re-measured (`bcde1575`) |
| --- | ---: | ---: |
| ACTIVE proposals | 45 | **45** |
| declaring `code_surface:` | 45 | **45** |
| declaring `none` | 5 | **4** |
| declaring a non-`none` value | 40 | **41** |
| repeated declarations | — | **0** |
| refused by the strict loader | — | **0** |

The one that moved is one fact and it is the fact the sibling's D2a paid for: a
population is a property of a TREE, and this tree is not the tree #1013 was
filed against. The issue's fifth `none` carrier is no longer one.

**REPRODUCIBLE WITHOUT THE SCRIPT, AND THE TWO PLACES THE PLAIN COMMAND IS
WRONG ARE NAMED.** On a worktree of `bcde1575`:

```text
$ ls openspec/changes/*/proposal.md | wc -l
45
$ grep -l '^code_surface:' openspec/changes/*/proposal.md | wc -l
45
$ grep -h '^code_surface:' openspec/changes/*/proposal.md | awk '{print $2}' | sort | uniq -c | sort -rn
     28 openxFactory      4 openxFactory,     4 none         2 xFactory
      2 openxFactory.     1 openxFactory's    1 >-           1 opensoft/OpenXPKI-Install
      1 opensoft/LedgerxWallet                1 opensoft/Keycloak-Install
```

- **`ls -d openspec/changes/*/ | grep -v archive` UNDER-COUNTS BY ONE**, and the
  reason is a real change name: `disposition-codexfactory-regular-pr-council-clearance-archive`
  contains the word. The exclusion has to be the `archive` DIRECTORY, not the
  substring.
- **In the ARCHIVE the plain grep OVER-COUNTS BY 28.** `grep -l '^code_surface:'
  openspec/changes/archive/*/proposal.md` returns **147**; reading the leading
  fence through the strict loader returns **119**. The 28 are early packets that
  discuss the field in BODY prose at column 0 — `2026-07-09-add-release-realization-flow`
  is the capability's own founding proposal and is one of them. The field's own
  measurement must read the front matter, not the file.

**THE SHAPE OF THE POPULATION, WHICH IS WHERE THE DESIGN CAME FROM.** Asking,
for each of the 45, what FOLLOWS the declared head:

| what follows the head | active | archived (119) |
| --- | ---: | ---: |
| an opening parenthesis | **19** | 76 |
| an em dash | **17** | 38 |
| a full stop | **2** | 0 |
| end of the declaration | 0 | 2 |
| **conforming subtotal** | **38** | **116** |
| ordinary prose, no opener | **5** | 2 |
| a possessive | **1** | 0 |
| a YAML folding indicator | **1** | 1 |
| **non-conforming subtotal** | **7** | **3** |

**THE SEVEN, BY CLASS, EACH READ RATHER THAN CHARACTERIZED:**

| class | change | the declaration, as it stands |
| --- | --- | --- |
| block scalar | `adopt-configured-notebook-hosting-identity` | `code_surface: >-` then `  openxFactory — NOT \`none\`, and the surface is …` |
| possessive | `amend-kill-switch-to-declared-test-companion` | `openxFactory's half of this packet carries NO CODE — …` |
| apposition | `add-substantive-review-lane` | `xFactory aggregation repo (.github/workflows/merge-master-…` |
| list runs into prose | `admit-review-lane-repin-to-merge-approval-envelope` | `openxFactory, and it is THREE FILES at realization and not one. (1) …` |
| list runs into prose | `amend-mirror-floor-regeneration-merge-authority` | `openxFactory, and it is DELIBERATELY SMALL. …` |
| list runs into prose | `extend-merge-master-envelope-to-floor-bot-lanes` | `openxFactory and codexFactory, and the split is decided by decision N-1. …` |
| list runs into prose | `split-opendox-two-layer-product` | `openxFactory, the openDox PROJECT (NEW), the openXdox PROJECT (NEW), …` |

**THE BLOCK-SCALAR CASE IS NOT A TYPO AND IT IS WORTH ITS OWN SENTENCE.**
`code_surface:` is a PROSE HEADER of the realization-axis block, and
`frontmatter_strict.read_front_matter` loads only the STRUCTURED fields
(`scope_globs`, `sequenced_after`) through YAML; every other field is returned as
its raw joined string. So an author who writes `code_surface: >-` to fold a long
declaration gets the two characters `>-` back as the first thing in the value.
Nothing tells them. The declaration reads correctly to a human and opens with a
YAML folding indicator to every reader.

**AND THE FOUR `none` CARRIERS ARE LAWFUL, WHICH IS THE FIRST PLACE THIS
POPULATION DIVERGES FROM THE SIBLING'S.** For `target_release:`, `none` was a
value canon does not admit. For `code_surface:`, `none` IS the promoted value for
an empty surface and is the doc-only default named in the same sentence. All four
carriers (`add-wallet-carried-review-authority`,
`amend-register-act-5b-projection-proof`, `prepare-openspec-1-12-readiness`,
`repoint-chain-anchoring-medxchain-citation`) are conforming declarations. The
divergence is entirely inside the 41 non-`none` values.

## D1 — RULED: what "off-vocabulary" means when the value is prose

**RULED 2026-09-13 BY BRETT HEAP — the bare word "ratify" takes the packet as
encoded, which is OPTION 1.** The recommendation was taken, so the grammar, the
opener set and the refusal to judge membership stand exactly as authored.
Options 2 and 3 are retained below as the record of what was put and declined.

**RECOMMENDED AND RULED — OPTION 1: GATE THE GRAMMAR — a DECLARED HEAD, then a REQUIRED
GLOSS OPENER — and judge no name's membership of anything.**

The accepted grammar, derived from the population in D0 and stated in the delta:

```text
declaration := head [ gloss_opener  gloss ]
head        := "none" | repo ( SEP repo )*
SEP         := ","  |  " and "  |  " + "   (and ", and ")
repo        := <owner>/<name> | <name>
name        := [A-Za-z][A-Za-z0-9._-]*[A-Za-z0-9]
gloss_opener:= " — " | " – " | " (" | ". " | ": " | "; "   (or end of declaration)
```

The gate judges the HEAD and never the gloss. Three properties, each chosen:

- **The opener requirement is what does the work.** A shape test on the head
  alone cannot tell `it` from `agenttower`: both are lowercase words that match
  any repository-name shape this estate could write, and `hermes-install` and
  `agenttower` are real repositories spelled exactly like English. What
  distinguishes `openxFactory, and it is THREE FILES` from `openxFactory,
  openAvatar` is not the tokens — it is that the first never stops declaring.
  Requiring an opener asks the one question the corpus can answer: *is there a
  point in this string at which the declaration ends and the explanation
  begins?* For 38 of 45 there already is.
- **The opener set is MEASURED, not preferred.** It is exactly the set the
  conforming 38 use (parenthesis 19, em dash 17, full stop 2), widened only by
  the three the archive and the house style also use — en dash, colon,
  semicolon — so the gate cannot refuse a form the estate's own corpus writes.
- **Membership is NOT judged, and that is a finding rather than a shortcut.**
  Searched on 2026-09-12 for an inventory of the estate's repositories in this
  tree: `contracts/policies/repository-identity.yaml` is a former-to-current
  TRANSFER map and carries ONE row today (`opensoft/codexFactory` →
  `codeXfactory/codexFactory`), so it enumerates only repositories that MOVED;
  `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` is a
  five-row FIXTURE of domain factories and does not name `openxFactory` itself,
  the install repositories, or the neutral products; `contracts/*-pin.yaml`
  carries one `source_repository:` each, for the pinned product only. The
  aggregation repository's `.gitmodules` does enumerate the estate and is not in
  this tree. **There is no registry to resolve against.**

*The cost of option 1, stated plainly.* The gate cannot tell a real repository
from a plausible misspelling of one: `openxFactorie` passes. It buys legibility —
every reader can find where the declaration ends — and buys nothing about
correctness of the names. That is the honest bound of what this repository can
check today, and D8.1 names the registry as the successor that would lift it.

**OPTION 2: judge only the FIRST TOKEN, exactly as the sibling does for
`target_release:`.**
*Cost, and it is measured:* the first token is the whole declaration for
`target_release:` and is a fraction of it here. Token-only would refuse the
block scalar (`>-`) and the possessive (`openxFactory's`) — 2 of the 7 — and
would PASS the other five, including `openxFactory, the openDox PROJECT (NEW),
the openXdox PROJECT (NEW)`, whose second and third "repositories" are the words
`the` and `PROJECT`. It would also make the MULTI-REPOSITORY case unreadable by
construction, which is the case D4's consumer exists to serve: a rule that reads
one token cannot answer "which repositories did this change declare".

**OPTION 3: resolve each identifier against a repository inventory.**
*Cost, and it is fatal as things stand:* there is no inventory (measured above),
so on the day it landed the gate would refuse all 41 non-`none` declarations —
the exact trap the sibling's D3 named for `target_release:`, where resolving
"the aggregation repository" literally would have admitted nothing. Building the
inventory first is a real and useful act; it is a different act, with its own
authority question (who admits a repository to the estate), and D8.1 names it.

## D2 — RULED: the shape of the remedy

**RULED 2026-09-13 BY BRETT HEAP — the bare word "ratify" takes the packet as
encoded, which is OPTION 1.** The recommendation was taken, so the remedy is a
validator plus a CLOSED register plus the ADDED requirements, and the register's
closure stays SHALLed rather than left to the implementation. Options 2 and 3
are retained below as the record of what was put and declined.

**RECOMMENDED AND RULED — OPTION 1: an ADDED requirement, a HOUSE VALIDATOR, and a CLOSED
REGISTER — following the sibling.**

*Why the register rather than a bare refusal.* D0 says 7 of 45 active
declarations would red the gate on the day it lands, and all seven belong to
OTHER lanes' ratified packets. A gate that cannot land is not a gate. The
register is a RATCHET: every declaration it does not name is judged from day one,
the named ones are reported and cannot grow, and each entry retires on a named
event. It is this estate's own idiom rather than an invention —
`contracts/openspec-cli-pin.yaml`'s `dispositions:` block does exactly this for
the pinned CLI, and `scripts/target-release-register.yaml` did it for the other
half of this very sentence three weeks' work ago, down to the asymmetry this
design copies (an unmatched declaration FAILS, an unmatched entry REFUSES).

*Why the closure must be enforced and not merely written.* The sibling's own
bench found this defect in the sibling's own register (its D8 (d)): the file's
header said an entry is never added, and nothing stopped an appended line from
granting an exception with the gate green. The remedy there was a baseline
recorded in the MODULE, so granting an exception takes an edit where the refusal
is written. This packet adopts that finding before paying for it again, and the
delta SHALLs it rather than leaving it to the implementation.

*The cost of option 1, stated plainly.* The estate gains a seven-entry exception
file, and a reader must consult it to know what the corpus actually declares.
Every entry is event-coupled: when its packet corrects its declaration or
archives, the gate refuses until the entry is deleted — which will occasionally
red an unrelated lane's pull request, remedied by a one-line deletion in that
same pull request. That is the precedent's accepted cost and it is taken
deliberately.

**OPTION 2: an ADDED requirement alone, with a bare refusal and no register.**
*Cost:* it cannot land without D3's option 3 (sweep all seven) landing with it,
which couples two independent decisions into one word. And it leaves no place to
record WHY a declaration is tolerated, so the next author learns the rule from a
failing run rather than from a file that names the reason and the retirement
event.

**OPTION 3: the requirement plus an ADVISORY validator — report, never fail —
until the seven are corrected by their owners.**
*Cost:* an advisory gate refuses nothing, which is the state #1013 filed about.
It also makes the gate's landing date and its effective date two different
things, and nothing schedules the second.

## D3 — RULED: the disposition of the seven

**RULED 2026-09-13 BY BRETT HEAP — the bare word "ratify" takes the packet as
encoded, which is OPTION 1.** The recommendation was taken, so all seven are
registered and none is swept, and no other lane's ratified prose is
re-punctuated by this lane. **THE POPULATION IS STILL A FACT ABOUT A TREE** and
`tasks.md` § 3.3 re-measures it at the head the gate lands on; the ruling fixes
the DISPOSITION, never the count. Options 2 and 3 are retained below as the
record of what was put and declined.

**RECOMMENDED AND RULED — OPTION 1: REGISTER ALL SEVEN, sweep none.**

*Why this departs from the sibling, which swept.* The sibling's sweep was a
ONE-TOKEN correction whose meaning the declaration's own gloss already supplied:
`none` → `implemented` where the author had written "no contract bundle is cut",
which is what `implemented` means. There was no judgment in it, which is exactly
why a lane that did not own those packets could take it. Correcting a
`code_surface:` head is a different act: it RE-PUNCTUATES another lane's
ratified prose — a comma becomes an em dash, a possessive becomes a name plus a
dash — and for at least one of the seven it is a judgment rather than a
re-punctuation. `split-opendox-two-layer-product` declares `openxFactory, the
openDox PROJECT (NEW), the openXdox PROJECT (NEW)`; making that head readable
means deciding whether "the openDox PROJECT" is a repository, two repositories
(`openDox-code`, `openDox-spec`), or a project that is not a repository at all —
a question that packet exists to answer and that this lane must not answer for
it.

*And the structural reason, which is decisive on its own.* This packet is
PROPOSAL-ONLY. The sibling swept "in this PR" because its realization was in that
same pull request; here the validator, the register and the sweep would all be
in the LATER realization pull request. So "sweep in this PR" is not even an
available option — the choice is between a sweep and a register in the
realization, and by then the population will have moved again.

*What option 1 costs.* Seven standing entries where the sibling would have had
one or two, and seven packets that keep a declaration no reader can parse until
each corrects or archives it. Each entry names the remedy, so the correction is
available to the owning lane at any time.

**OPTION 2: sweep the six whose correction carries no judgment; register the
one that does.** The six: drop the `>-`; `openxFactory's half …` →
`openxFactory — its half …`; `xFactory aggregation repo (…` → `xFactory (the
aggregation repo; …`; and three `, and it is …` → ` — and it is …`.
*Cost:* it is six edits to six other lanes' ratified proposals by a lane that
owns none of them, for a defect that is cosmetic in each. The sibling's custody
check would hold (these are `Status: ratified` active packets, not `record`
documents, and neither *Origin retention at archive* nor *Scope retention at
archive* reaches `code_surface:`) — so the objection is not custody, it is that
six re-punctuations of other people's sentences is a larger imposition than one
token each, and the benefit is only that the register carries one entry instead
of seven.

**OPTION 3: sweep all seven.**
*Cost:* it takes the `split-opendox` judgment described above, in a lane that
does not own that packet and while that packet is itself active and mid-flight.

## D4 — RULED: is `add-structured-scope-substrate`'s `scope_globs:` machinery reusable?

**THE ANSWER IS SPLIT, AND BOTH HALVES ARE MEASURED: REUSABLE AS THE CONSUMER,
NOT REUSABLE AS THE GRAMMAR — AND THE EXTRACTOR IT SHIPS IS THE STRONGEST
ARGUMENT FOR THIS PACKET.**

**(a) NOT REUSABLE AS THE GRAMMAR, because `scope_globs:` never had one to
lend.** `scope_globs:` is a STRUCTURED field — a mapping from repository name to
a list of globs, loaded through the strict YAML loader and validated against the
merge-gate envelope glob dialect (`scripts/scope_globs.py` `validate_shape`,
`validate_dialect`). Its machinery validates GLOB SYNTAX and MAPPING SHAPE. Its
repository KEYS are validated by exactly one rule — `validate_cross_consistency`,
"every `scope_globs` repository key MUST be named in `code_surface`" — which
resolves the key against `code_surface:` rather than against any registry of
repositories. There is no repository grammar in it to borrow. Its own ratified
delta says so in terms: *"`code_surface:` and `target_release:` are UNCHANGED"*.

**(b) REUSABLE AS THE CONSUMER, and this is where the reuse is real.** That
cross-consistency rule is the one place in the estate that needs the answer to
"which repositories did this change declare", and it already asks the question.
What it asks it OF is the problem.

**IT IS ALSO THE ONLY READER THERE IS, WHICH THE COMMAND THE ISSUE NAMES
CONFIRMS.** `grep -rn code_surface scripts/ .github/` at `bcde1575` returns
seventeen lines. Fourteen are inside `scripts/scope_globs.py` and
`scripts/validate-scope-globs.py`; the other three are PROSE — a docstring
sentence in `scripts/target_release.py:23` quoting the promoted default, and
comments at `scripts/doc_health/corpus.py:267` and
`scripts/doc_health/lines.py:63`. Nothing in `.github/`. So exactly ONE machine
reader of this field exists, and it is the permissive one.
`scope_globs.code_surface_repositories` (`scripts/scope_globs.py`), wired live at
`scripts/validate-scope-globs.py:68`:

```python
raw = front_matter.get("code_surface")
if not isinstance(raw, str):
    return set()
tokens = re.split(r"[\s,()/]+", raw)
return {t for t in tokens if t and t != "none"}
```

Its docstring says what it is: *"It is intentionally permissive — the
cross-consistency check only needs to confirm a scope key APPEARS in the prose,
and a false accept here is caught by the human ratification read, while a false
reject would wrongly gate a valid scope."* **MEASURED over the 45 active
declarations at `bcde1575`:**

| measure | value |
| --- | ---: |
| distinct "repository" tokens across the corpus | **3,421** |
| the widest single declaration (`split-opendox-two-layer-product`) | **767** |
| the narrowest | **3** |
| declarations yielding an ESTATE repository their HEAD does not name | **27 of 45** |
| `none` carriers yielding a NON-EMPTY set | **3 of 4** |

Among the 767: `the`, `and`, `a`, `GitHub`, `Postgres`, `FastAPI`, `NotebookLM`,
`§`, `—`. Among the 27: `add-sequenced-after-substrate` declares `openxFactory`
and yields `codexFactory`; `add-trust-anchor` declares `openxFactory` and yields
`OpsxFactory` and `OpenXPKI-Install`; `create-ledgerxwallet-overlay-boundary`
declares `opensoft/LedgerxWallet` and yields five more. The `none` case is the
sharpest: the filter drops the word `none` and keeps the gloss, so a change that
declared NO code surface yields a non-empty repository set.

**WHAT THAT SET AUTHORIZES.** `scope_globs:` exists so a provenance-tie verifier
can confirm a pull request's changed paths fall within the scope its ratified
change declared — it bounds the paths a provenance-gated autonomous merge may
write. A scope key is admitted when it "appears in the prose". So the ceiling on
what a scope may authorize is currently *any word appearing anywhere in the
declaration's explanation*.

**THE DEFECT IS LATENT AND NOT STANDING, AND OVERSTATING IT WOULD BE THE SAME
ERROR THIS PACKET IS ABOUT.** **ZERO of the 45** active proposals declare
`scope_globs:` at `bcde1575`; the cross-check is vacuous over the live corpus and
bites the first time a `scope_globs:` lands. Nothing is mis-authorized today.
What exists is a guard that will answer wrongly the first time it is asked — the
sibling's D8c lesson (a latent defect made live by the next change) applied
before rather than after the fact.

**RULED 2026-09-13 BY BRETT HEAP — the bare word "ratify" takes the packet as
encoded, which is OPTION 1**, so the narrowing is owed by `tasks.md` § 3.5 and
the derivation rule stands in the delta. Options 2 and 3 are retained below as
the record of what was put and declined.

**RECOMMENDED AND RULED — OPTION 1: narrow `code_surface_repositories` to the
DECLARED HEAD, in this packet's realization, and SHALL it in the delta.** The requirement
*The declared repository set is derived from the head and never from the gloss*
states the rule; the realization makes that function call this capability's
reader, so there is ONE derivation and not two.
*Why this is a tightening and not an amendment of another change's rule.*
*Structured path-scope declaration* SHALLs that a key be "named in
`code_surface`" and is silent on what "named in" means. Answering it is not
editing it. And the answer breaks nothing standing: with zero `scope_globs:`
declarations the behaviour change is unobservable on the live corpus, which is
provable by running the existing gate before and after.
*Cost:* it edits a module another ACTIVE packet authored. That packet is
ratified and its file is merged on `main`, so the edit is a normal change to
shipped code rather than a rewrite of an unlanded diff — but it is another
lane's module and the change is recorded here rather than assumed.

**OPTION 2: leave the extractor exactly as it is and name a successor.**
*Cost:* the gate then reads one field two ways — strictly, in the new validator,
and permissively, in the authorization check — which is the show-one-authorize-
another shape the strict loader exists to refuse. And the successor's trigger
would be the first `scope_globs:` declaration, i.e. exactly the moment the
permissive answer starts mattering.

**OPTION 3: leave the extractor and put the 27 in the register.**
*Cost:* it registers 27 packets for a defect that is in the READER rather than
in any of their declarations. A register entry says "this declaration is
tolerated"; none of those 27 declarations is the problem.

## D5 — the code surface: a sibling validator, reading the shipped loader

**A NEW PAIR OF FILES IN THE SIBLING'S SHAPE, NOT A NEW ARM ON AN EXISTING
VALIDATOR.** `scripts/code_surface.py` holds the rules,
`scripts/validate-code-surface.py` is the thin CLI (`[REPO_ROOT]` plus
`--register PATH`), and `tests/code_surface/test_code_surface_gate.py` runs the
CLI over the live tree on every pull request — which is how the required
`pytest-suite` (`python3 -m pytest tests/ -q -m "not postgres"`, which runs
everything under `tests/`) comes to gate the corpus with NO workflow edit.

**IT READS THROUGH `frontmatter_strict.read_front_matter` AND ADDS NO SECOND
PARSER.** The loader is shipped, is vendored byte-for-byte into codexFactory, and
is not this packet's file to widen — and no widening is asked for:
`code_surface:` is a PROSE HEADER of the realization-axis block, not one of its
two STRUCTURED fields, so this gate CONSUMES the loader's refusals rather than
extending them. A document the loader refuses is reported here as a finding
against that document rather than as a traceback.

**THE SCAN IS TOP-LEVEL AND THAT IS LOAD-BEARING**, for `validate-scope-globs.py`'s
own reason: a recursive scan would reach the `tests/doc-health/fixtures/**`
proposals and make this gate a tax on every fixture the estate writes.

**THREE EXIT CODES, MIRRORING THE SIBLING.** 0 clean; 1 an unreadable
declaration the register does not name (a statement about the PROPOSAL, remedied
by its own packet); 2 a register that cannot be used, or an entry that matched
nothing (a statement about the REGISTER, remedied by deleting the entry). Where
both occur the run prints both and exits 1.

**THE REGISTER IS NOT UNDER `contracts/`, AND THAT IS DELIBERATE** — the
sibling's D4 reason, unchanged: a file under `contracts/` is a bundle surface
whose change owes a bundle cut, and an exception register that could not be
edited without cutting a contract release would be edited late or not at all.

## D6 — why an OpenSpec change and not a patch

**BECAUSE CANON GAINS THREE REQUIREMENTS AND ONE OF THEM IS AN AUTHORIZATION
RULE.** No promoted requirement says the `code_surface:` declaration has a form,
and none says where a consumer's repository set comes from — which is precisely
why a shipped reader could answer the second question with "every word in the
gloss" and no rule was violated. Adding a refusal, a closed exception mechanism,
an archive exemption and a derivation rule in `scripts/` alone would put four
governance decisions in code with no delta behind them, which is the shape this
repository refuses.

## D7 — sequencing, and the sibling search, pasted

Performed 2026-09-12 before authoring, on the lane-collision protocol's
claim-before-author rule, by FILE PATH and by subject.

```text
$ gh api '/repos/opensoft/openxFactory/pulls?per_page=50' --jq '.[] | "#\(.number) \(.head.ref)"'
#1015 archive/report-stale-grandfather-dispositions   #1014 archive/gate-realization-axis-vocabulary
#1011 feat/carve-manifest-re-destined-form            #1008 docs/governed-reissuance-runbook-5b-exit-condition
#1006 register/q-grc-4-h2-grant-grc-0003              #888  doc-health/derive-possibles
#594  rescue/worker-fleet-health-monitoring           #518  docs/add-usage-controlled-evidence-chain

$ for n in 1015 1014 1011 1008 1006 888 594 518; do gh api .../pulls/$n/files --jq '.[].filename' \
      | grep -E 'release-realization|code_surface|scope_globs|scripts/code'; done
#1014 only: openspec/changes/archive/2026-09-12-gate-realization-axis-vocabulary/specs/release-realization/spec.md
             openspec/specs/release-realization/spec.md
(every other open pull request: no output)

$ ls -d openspec/changes/*/specs/release-realization
add-sequenced-after-substrate   add-structured-scope-substrate   gate-realization-axis-vocabulary

$ gh search issues --repo opensoft/openxFactory 'gate code surface' --state open
#1013  (this packet's origin, and the only one)

$ grep -rln "Code-surface declaration grammar is gated" openspec/
(no output — the title is novel, and so are the other two)
```

**PR #1014 IS THE ONE TO KNOW ABOUT, AND IT DOES NOT COLLIDE.** It ARCHIVES
`gate-realization-axis-vocabulary` and promotes its ADDED requirement
*Realization axis vocabulary is gated* into
`openspec/specs/release-realization/spec.md`. This packet writes three different
titles, edits nothing under `openspec/specs/`, and is indifferent to whether the
sibling is active or archived when it lands. The one real interaction is the
README *OpenSpec Records* block, which both pull requests touch — a landing-window
matter under the lane-collision protocol, not a content collision.

**THE TWO ACTIVE SIBLINGS ON THIS CAPABILITY, BY REQUIREMENT HEADING:**

- **`add-structured-scope-substrate`** — one `## MODIFIED` block over
  ***Realization axis declaration*** plus five ADDED requirements (*Structured
  path-scope declaration*, *Structured path-scope validation*, *Trust-root
  integrity of the structured scope declaration*, *Scope retention at archive*,
  *Floor primacy over declared scope at check time*). This packet adds three
  NOVEL titles and modifies nothing, so no `sequenced_after` is owed. D4 answers
  a question *Structured path-scope declaration* leaves open and contradicts no
  sentence of it.
- **`add-sequenced-after-substrate`** — ADDED requirements only, among them
  ***Strict loading of the realization-axis front-matter block***, which reaches
  "every STRUCTURED field". `code_surface:` is a prose header and is not in its
  set. This gate CONSUMES the loader that rule produced rather than extending it.

`sequenced_after: []` is declared as a ROOT claim and it is corroborated rather
than asserted: no active change carries a `## MODIFIED` block over any title this
delta writes, the titles being new to the capability, and none is a title an
active change ADDS or RENAMES TO — the widened antecedent *Ordered deltas and
branch vocabulary* now carries.

## D8 — what is NOT taken here, measured and deliberately left

1. **AN INVENTORY OF THE ESTATE'S REPOSITORIES.** D1 option 3 needs one and this
   repository has none. Building it is a real act with a real authority question
   — who admits a repository to the estate, and what a row means for a repository
   that is pinned rather than governed — and it would let the gate resolve
   membership instead of shape. Named as the successor that lifts D1's stated
   bound. (`tasks.md` § 6.1)
2. **MAKING `code_surface:` A STRUCTURED FIELD.** The obvious machine-readable
   move is to give it `scope_globs:`'s shape — a list loaded through the strict
   YAML loader — at which point no grammar is needed because YAML supplies one.
   It is a `## MODIFIED` block over the title `add-structured-scope-substrate`
   holds, with the sequencing hold that carries, and it would obsolete a
   declaration form 45 active packets already carry. Named as a successor.
   (`tasks.md` § 6.2)
3. **THE THREE ARCHIVED NON-CONFORMERS**, and the 28 archived packets whose
   `code_surface:` line lives in body prose. Frozen record: read, counted,
   judged never.
4. **THE OTHER ESTATE REPOSITORIES ARE NOT SWEPT OR REGISTERED.** codexFactory,
   OpsxFactory and the rest carry their own corpora; the validator takes a
   `REPO_ROOT` and refuses a tree with no register rather than assuming an empty
   one.
5. **WHETHER A `none` DECLARATION MAY CARRY A GLOSS AT ALL.** Three of the four
   carriers do, and the delta admits it (the gloss is explanation). A stricter
   rule — `none` and nothing else — would refuse three lawful declarations for
   tidiness.
6. **NO DISPLAY SURFACE IS CHANGED, AND THERE IS NO LONGER ONE TO CHANGE.**
   `gate-realization-axis-vocabulary`'s D0 named the ideation dashboard's
   `scripts/ideation_dashboard/generator.py` `_release_frontmatter` as the one
   reader of the realization-axis headers. **That module is GONE from `main`**:
   `ce5c054e` (contract-v4.0) removed the five ideation-dashboard schemas at the
   openDox/openXdox split, and `scripts/ideation_dashboard/` carries no
   `generator.py` today. Re-measured rather than carried, which is the point —
   a figure quoted from a sibling packet three weeks old is a figure about that
   tree.

## D9 — the bench's first round: five threads, two code-of-canon findings TAKEN IN FULL, one REFUSED AS FALSE with evidence

The draft pull request's first automated review round opened FIVE threads. Two
were taken at `a5a707c7` and `83b13051` and are resolved (a scenario count
overstated by one, and a `§ 4` header reading DONE over unticked boxes — both
real, both the packet's own bookkeeping contradicting its diff, which is the
defect class this house has already paid for twice). Of the three that stood at
the ruling, **TWO ARE REAL DEFECTS IN THE RATIFIED TEXT AND BOTH ARE TAKEN**,
and **ONE IS FALSE AND IS REFUSED ON MEASUREMENT** rather than absorbed. The
ruling of 2026-09-13 directs in its own words that the two be fixed *"before
the record is cut, so the ratified packet includes them"*, so the text ratified
is the text they produced.

**(a) THE GRAMMAR NEVER RESERVED `none` OUT OF REPOSITORY IDENTIFIER**
(`specs/release-realization/spec.md`, the head definition). The first
requirement admitted a head that was "the single word `none`, or one or more
REPOSITORY IDENTIFIERS separated by a comma …" — an `or` between two
alternatives, with nothing forbidding a head from containing both. Read against
the grammar as it stood, **`none, openxFactory` parses as a two-member list**,
because `none` matches the repository-name shape like any other lowercase word:
the identifier rule judges SHAPE and deliberately not membership (D1), so it has
no ground on which to refuse the token. The derived set for that head is then
NON-EMPTY — one member `none`, one member `openxFactory` — for a change whose
declaration says the surface is empty, which contradicts the second
requirement's own rule that a `none` head derives the empty set, in the one
field where the two readings differ by an authorization.

THE FIX makes the two alternatives EXCLUSIVE in the requirement's first line
(`EITHER the single token none, OR a list … the two being EXCLUSIVE alternatives
and never mixed`), adds a paragraph stating why the exclusivity is written down
rather than left to good sense, and adds a tenth scenario — *A head mixes none
with a repository identifier* — that refuses the mixed head in either order,
forbids computing a derived set for it, and holds the refusal wherever in the
list the token appears, position being no part of the contradiction. The
remedy is a REFUSAL rather than a precedence rule ("`none` wins", or "the
repositories win") because both precedence rules silently discard something an
author wrote; the author of a self-contradictory head owes a correction, not a
reader a guess.

**(b) THE DELTA LEFT THE REGISTERED-EXCEPTION CASE UNDEFINED, AND BOTH OBVIOUS
FALLBACKS ARE DEFECTS** (`specs/release-realization/spec.md`, the register
requirement). The register tolerates seven declarations the grammar cannot read;
the second requirement makes every consumer derive its repository set from the
HEAD. **The two rules do not meet.** If one of those seven later declares
`scope_globs:`, there is no head to derive from, and the delta said nothing — so
an implementer would have chosen, and both available choices are wrong. Falling
back to the whole-declaration extractor re-admits the gloss as an authorization
surface, which is the single 3,421-token defect this packet exists to close and
which no exception may reopen. Returning an EMPTY set makes every scope key
unnameable while reporting the fault in the wrong place: the author reads a
refusal about their structured scope when the defect is in their code surface,
and a packet silently ineligible for the provenance axis is the fail-open-LOOKING
shape of a fail-closed intent — the same *"treated as ineligible rather than as
all paths in scope"* posture `add-structured-scope-substrate` states, but with
its reason hidden.

THE FIX states FAIL-CLOSED in canon and names both forbidden substitutes
explicitly: a REGISTERED proposal that also declares `scope_globs:` is REFUSED
by the cross-consistency check, naming the proposal AND its register entry, and
stays refused until the declaration is brought into the grammar — which retires
the entry in the same act. A sentence is added to the register requirement so
the boundary is legible from that side too (*an entry suspends the grammar's
refusal for one declaration and authorizes nothing derived from it*), a
distinction is drawn in the derivation requirement between an empty set the head
DECLARES and the ABSENCE of a head-derived set, and a fourth scenario — *A
registered-exception packet later declares a structured scope* — pins the
refusal and both prohibitions. `tasks.md` § 3.1, § 3.5 and § 3.6 carry the
realization.

**(c) THE CORPUS-LEDGER FINDING IS FALSE, AND IS REFUSED ON THE FILE ITSELF**
(`proposal.md`, the front-matter thread). The finding says
`tests/sequenced_after/corpus-ledger.yaml` "has no `gate-code-surface-declarations`
entry" and that `--ledger-diff` therefore reports a missing row. Measured on this
branch: the row is at **`tests/sequenced_after/corpus-ledger.yaml:236`** —
`gate-code-surface-declarations: {state: active, class: sole, declares: [],
depth: 0, prose: false, moved_by: "#1018", moved_on: "2026-09-12"}` — the file
is in this pull request's own diff, and `python3
scripts/validate-sequenced-after.py . --ledger-diff` exits **0** with
*"per-change sweep ledger consistent with the corpus (211 rows)"*. The row was
seeded by the sanctioned tool at `83b13051`, after the draft pull request existed
so the tool could stamp `moved_by`, exactly as `tasks.md` § 4.7 records. **A
finding is not taken for having been made**; this one is answered with the line
number, the command and the exit code, and the refusal is recorded on the thread.
