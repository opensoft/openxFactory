# Design: add-target-release-deferred-allocation

Status: ratified
Ratified by: Brett Heap, 2026-09-13T01:0xZ — verbatim "accept all A on 1022" (record `review/ratification-2026-09-13.md`)
Kind: design
Lane: hermes-wallet-exercise

**TEN DECISIONS, D1 … D10, ONE PER OPEN QUESTION, EACH WITH THE RECOMMENDATION
FIRST AND THE ALTERNATIVES' COSTS WRITTEN OUT.** Every recommended option is what
this packet already encodes, so `accept all A on <n>` ratifies and moves not one
byte. The decisions rest on no shared predicate and each stands whichever way the
others go, except where noted at D2 and D10.

## D0 — the measurement, taken before the design

Reproducible from the commands below, on this worktree, off `origin/main`
`a1429885` (itself the merge of PR #1014, the archive of
`gate-realization-axis-vocabulary`).

| fact | command | value |
| --- | --- | ---: |
| active proposals on `main` | `python3 scripts/validate-target-release.py .` | 44 |
| declaring `implemented` | same | 20 |
| declaring a release the estate defines | same | 3 |
| named by the closed register | same | 21 |
| refused on `main` | same | **0** |
| register entries of class `deferred-allocation` | `grep -c 'class: deferred-allocation' scripts/target-release-register.yaml` | **12** |
| archived proposals, read and never judged | validator report | 166 |
| of them outside the vocabulary | validator report | 61 |
| machine enforcement of *Realization archive gate* | `grep -rn 'Realization archive gate' scripts/ tests/ .github/` | **none** (register prose only) |

**`main` IS GREEN.** The gate is not failing today; it fails on a proposal
authored AFTER the register was fixed. That is the ratchet working as designed,
and it is why the remedy is an admission rather than a repair.

## D1 — the token's spelling — RULED (a), 2026-09-13T01:0xZ

**RECOMMENDED — `deferred-allocation`.** Four grounds, none of them taste:

1. **It cites rather than invents.** `scripts/target_release.py`
   `REGISTER_CLASSES` already carries `"deferred-allocation"` as a ratified,
   loader-enforced class word, and the register header already defines the class
   in exactly the terms the value needs. Choosing any other spelling would leave
   canon carrying two names for one thing.
2. **Retirement becomes mechanical.** An entry's `class: deferred-allocation`
   retires when its packet writes `target_release: deferred-allocation` — the
   class and the value are the same word, so a reader can see the retirement
   without reasoning about it.
3. **It follows the house's own compound-token idiom.** The estate's other
   non-`implemented`, non-release token is `repository-bootstrap`: a hyphenated
   compound naming the KIND of realization the two-value sentence has no
   spelling for. This is the same shape for the same reason.
4. **It cannot be read as a work state.** Canon REFUSES `implementation_pending`
   as "a state of the work, not a target" (register class `realization-state`,
   four carriers).

**OPTION (b) — `deferred`.** It pairs with `implemented` as a bare participle,
which is the only real argument for it. *Cost:* it reads as a STATE. The four
registered `implementation_pending` carriers are one plausible "correction" away
from a token that does not describe them — their realizations land on main lines,
not in unnumbered bundles — and the gate would accept the wrong value silently,
because the gate judges tokens and not meanings.

**OPTION (c) — `contract-deferred`.** Unambiguous about the bundle, and shares
the `contract-` prefix with `contract-vX.Y`. *Cost:* it invents a second name for
a class the register already names, and a reader who greps `deferred-allocation`
finds the class but not the value.

## D2 — where the widening is written — RULED (a), 2026-09-13T01:0xZ

**RECOMMENDED — BOTH promoted requirements, as `## MODIFIED` blocks.**

The enumeration lives in two places, measured:

- *Realization axis declaration* DEFINES it — "`target_release:` — `implemented`
  … or a named release defined in the aggregation repository".
- *Realization axis vocabulary is gated* RESTATES it in the gate's own apposition
  — "a value the ratified vocabulary admits — `implemented`, or a release
  identifier that resolves to a release this estate defines".

Widening one and not the other leaves canon saying two different things about one
vocabulary, which is precisely the contested-finding class this estate disposes of
rather than creates.

*The cost, paid rather than avoided.* `add-structured-scope-substrate` is ACTIVE
and `Status: ratified` and holds a `## MODIFIED` block over *Realization axis
declaration* (`openspec/changes/add-structured-scope-substrate/specs/release-realization/spec.md:16-42`),
restating the two-value sentence verbatim and adding `scope_globs:`. Under
*Ordered deltas and branch vocabulary* this packet therefore declares
`sequenced_after: [add-structured-scope-substrate]` and writes its pre-text from
THAT change's outcome rather than from canon — which is exactly the cost
`gate-realization-axis-vocabulary` D1 wrote out when it declined this remedy, and
which is why it declined it. It is paid here because the alternative is a canon
contradiction.

**TWO THINGS THAT ARE OFTEN ASSUMED AND ARE NOT TRUE HERE, BOTH CHECKED:**

- **No `Modified over` marker is owed.** `document-lifecycle` scopes that
  reserved form to a block naming "a requirement the promoted specification does
  not carry" (`openspec/specs/document-lifecycle/spec.md:1012-1016`). Canon
  carries BOTH titles. The marker is not owed and is not written.
- **No archive-order hold binds this packet.** *Ordered deltas and branch
  vocabulary*'s hold — and every one of its scenarios — keys on "a requirement
  the promoted specification does not carry" / "while the requirement it modifies
  is still unpromoted". *Realization axis declaration* IS promoted. What this
  packet owes is the REFERENCE-AND-DECLARE half only. The residual hazard is the
  one the requirement states in its own words — "whichever writer archives last is
  the text canon keeps" — and it is carried as `tasks.md` § 5.2 rather than
  dressed up as a hold that canon does not impose.

**OPTION (b) — the gate requirement only.** Zero sequencing cost, one block, and
the operative clause ("a value the ratified vocabulary admits") is arguably a
DEFERRAL to the other requirement rather than a second definition. *Cost:*
*Realization axis declaration* would keep enumerating two values while the gate
admitted three, and a reader could not tell which sentence governs.

**OPTION (c) — an `## ADDED` requirement over a novel title.** No MODIFIED block,
no sequencing, no pre-text problem — the shape `gate-realization-axis-vocabulary`
itself took. *Cost:* it works for an ADDITION and not for an AMENDMENT. Both
promoted enumerations would go stale on the day it lands, and the vocabulary would
then be written in three places with the newest one winning by implication.

## D3 — may a `deferred-allocation` change archive? — RULED (a), 2026-09-13T01:0xZ

**RECOMMENDED — NO.** The declaration is temporary by construction: the number it
stands in for comes into existence at the cut, and by the time a code-surface
packet is archivable its realization has merged, so the number is knowable. The
archiving act resolves the token to the literal the cut allocated, or to
`implemented` where the realization ended up cutting no bundle.

*Why it matters more than it looks.* The archive is FROZEN RECORD —
`record-immutability` and `govern-archived-record-edits` put it beyond a plain
fix. A record that archives carrying `deferred-allocation` names a number nobody
ever allocated, permanently and unrepairably. That is the `none` defect with a
better name, and it would be introduced by the very act meant to remove it.

**(b) archive with the token standing** — the archive accumulates unresolvable
targets, and the count only grows. **(c) archive with a disposition** — makes the
ORDINARY case a contested act, which inverts the disposition mechanism's purpose.

## D4 — how that archive rule is enforced — RULED (a), 2026-09-13T01:0xZ

**RECOMMENDED — canon-enforced at the archiving act; the validator REPORTS and
refuses nothing in the archive.**

This is forced, not chosen. The promoted requirement this packet is amending says,
in the paragraph directly above the one being changed:

> AN ARCHIVED PROPOSAL SHALL BE READ AND NEVER JUDGED. … so the gate SHALL count
> what the archive carries and report it, and SHALL refuse nothing there. A gate
> that demanded an edit nobody may make would be a standing finding with no
> remedy, which is the defect this estate disposes of rather than creates.

So the new rule is written to bind the ARCHIVING ACT and not the archived record,
and the validator gains a COUNT — "N archived records carry an unresolved
`deferred-allocation`" — which is visible without being a refusal to anyone.

*And the sibling is enforced the same way, measured rather than assumed.*
`grep -rn 'Realization archive gate' scripts/ tests/ .github/` finds only prose in
the register YAML: the *Realization archive gate* itself has no machine
enforcement. A new archive rule enforced by canon and reported by the validator is
therefore consistent with its sibling rather than weaker than it.

**(b) refuse an archived `deferred-allocation`** — would require MODIFYING the
never-judged paragraph as well, and would create exactly the standing finding with
no remedy that paragraph exists to forbid. **(c) silent** — no report and no
refusal, so a breach leaves no trace anywhere.

## D5 — must the resolving edit cite the cut? — RULED (a), 2026-09-13T01:0xZ

**RECOMMENDED — YES: the resolving pull request names the bundle version and the
release surface that carries it.** § Bundle Realization Order runs land-then-tag
(step 4 lands the reviewed commit, step 5 publishes the tag), so at resolution
time the number is an OBSERVED fact with a surface to point at. A bare token swap
cites nothing and is, on the diff, indistinguishable from the reservation the
policy forbids — which is the whole reason the value exists.

**(b) a bare swap** — cheap, and gives a reviewer nothing to check. **(c) cite
only for a cut in another repository** — a seam in the rule with no principle
behind it.

## D6 — who may declare it — RULED (a), 2026-09-13T01:0xZ

**RECOMMENDED — only a change whose `code_surface:` is non-empty AND whose
realization lands in a contract bundle.** A value available to every proposal
becomes the second `none`: a word that means "I did not want to answer". The
promoted default already covers the doc-only case and says so.

**(b) any change** — re-opens the defect the gate was built to close. **(c) any
non-empty code surface** — would silently admit the four `realization-state`
carriers, whose realizations land on main lines and have nothing to defer.

## D7 — the twelve standing register entries — RULED (a), 2026-09-13T01:0xZ

**RECOMMENDED — NOT swept here; only the class NOTE is amended.**

Admitting the value does not make a standing entry's declaration lawful: the
entries name the tokens their authors actually wrote (`THE`, `next`, `the`,
`contract-v<next`), none of which is `deferred-allocation`. So each retires when
its owning packet corrects its own declaration, and the entry is deleted in that
same pull request — which the validator's exit-2 stale refusal ALREADY FORCES
without any new mechanism. The class note is amended to say so, resolving the
`retires_when` disjunction cleanly.

*Why not sweep, when the precedent swept.* `gate-realization-axis-vocabulary` D2
swept six carriers that were REFUSED — red on the day the gate landed, unlandable
otherwise. These twelve are REGISTERED and GREEN; sweeping them is not needed to
land this packet or to unblock #1017. Against that: twelve `proposal.md` files
across twelve active lanes, plus twelve entry deletions, plus a `CLOSED_REGISTER`
baseline move — a cross-lane edit of a size the lane-collision protocol exists to
avoid, in a packet whose realization evidence ought to be about the vocabulary.

**(b) sweep all twelve** — the precedent's shape, and a defensible ruling; it
makes the corpus consistent in one act at the cost above. **(c) sweep the
quiescent lanes' only** — an arbitrary line nobody can re-derive later.

## D8 — this packet's own `target_release:` — RULED (a), 2026-09-13T01:0xZ

**RECOMMENDED — `implemented`, and the reason is the admission's own rule.**

This packet's code surface is a validator, a register note and a test. It cuts no
contract bundle, nothing under `contracts/` moves, no `contract_bundle_version` is
spent, no release tag is owed. Under D6's rule — the rule this very packet writes
— `deferred-allocation` would therefore be a FALSE declaration. It cannot declare
the value it admits, and that is a feature of the rule rather than an awkwardness
of the timing.

The precedent declared `implemented` for the identical reason and wrote the reason
into the register's own header: *"an exception file that could not be edited
without cutting a contract release would be edited late or not at all."*

**(b) `deferred-allocation`** — false, and circular. **(c) omit the field** — the
doc-only default is `code_surface: none`, which this packet is not.

## D9 — openxFactory #1017 — RULED (a), 2026-09-13T01:0xZ

**RECOMMENDED — not edited here.** Its front matter is its own lane's file; two
lanes writing one packet is the collision the protocol names. After this lands,
that lane makes the one-line correction — value token only, prose gloss preserved
verbatim, the method `gate-realization-axis-vocabulary` D2 used for its own six —
and `merge 1017 when green`, already given, applies to that head unchanged.

**(b) edit it here** — couples two ratifications and puts this packet's landing on
that packet's review. **(c) hold #1017 until a real cut** — blocks a ratified
change on an unscheduled event, which is what the value exists to avoid.

## D10 — where the realization lands — RULED (a), 2026-09-13T01:0xZ

**RECOMMENDED — this pull request**, mirroring `gate-realization-axis-vocabulary`
exactly: non-empty `code_surface`, the validator and register and tests in the
SAME pull request as the ratification, archiving later on merged-plus-green.

*And the alternative has a concrete failure here.* **(b) a follow-up realization
PR** would leave canon admitting a value that no validator accepts — so #1017
would remain red after this packet ratified, and the block this packet exists to
lift would still be in force. D10 is the one decision that interacts with D9: a
split realization makes D9's follow-up unperformable until a third pull request
lands.
