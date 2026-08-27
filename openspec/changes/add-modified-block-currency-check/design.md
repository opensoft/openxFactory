# Design: add-modified-block-currency-check

Status: draft
Proposed: 2026-08-27

This document records why the five decisions in the proposal's § Orchestrator
Decisions were taken as they were, and what was measured before taking them.
Every figure below came from a throwaway implementation of the matching rule
**exactly as the spec delta writes it** — same-kind exact units, backtick-masked
sentence split, scenario bullets compared across the whole block — run over this
repository at `9be81a40`. None of that spike is committed.

## D1 — A twenty-second family, not an extension of `promotion-fidelity`

#330 offers two shapes and says they are not exclusive. It is right, and this
change still builds only one of them.

**Canon has already argued this question, in its own words.** The promoted
requirement "One ruling, one discharge, across archived packets" contains this
paragraph, written for the duplicate-packet family:

> **This family answers a question the promotion fidelity family cannot.** That
> family compares an archived delta to CANON, and where one ruling has been
> discharged twice canon holds exactly what both packets said it should hold —
> so it reports zero either way. The comparison that can see the class is
> between the archived deltas themselves, which is why this is a separate
> family rather than a wider reading of that one.

Substitute this class and the paragraph holds unchanged: after an archive act
canon is the delta, so a block that dropped seven scenarios and a canon now
missing them agree, and the comparison that can see the loss is between an
active delta and the canon it has not yet replaced. Same argument, same shape,
same conclusion. Reaching a different one here would mean the corpus had two
rules for when a comparison earns a family.

**The measurement basis forbids the alternative.** #330's shape 1 — a
promoted→promoted arm diffing the spec across the archive commit — needs the
promoted spec's state at the archive commit's parent. "The promotion fidelity
measurement basis is declared" gives that family exactly two bases, checkout
and live `main`, and requires: "A run's report SHALL state which basis this
family measured, in the family's own report section, on every run and whether
or not the family found anything." A third basis inside that family would make
that line untrue of half its findings, and the requirement's own reasoning says
why that matters — "a report that mixed the two bases without saying which was
which would invite a reader to act on a stale finding as a current one".

**The finding must land where the remedy is.** `promotion-fidelity` is
archived-path-shaped throughout: latest-writer-wins orders archive folders by
`YYYY-MM-DD` prefix, the exemption reads an archived packet's `proposal.md`,
and dispositions key on the archived delta's stable path. Its own proposal
takes that decision under the heading "D4 — The finding lands on the archived
delta's path, not the promoted spec's", and gives as one reason that the path
"is what a disposition needs to key on". This class's remedy is an edit to an
ACTIVE delta on a branch, so a family reporting against archived paths cannot
address it.

**The dispositions would collide.** The aggregation checkout's
`health/dispositions.yaml` keys on `(family, repo, path)`. Folding this class
into `promotion-fidelity` would let one citation buy silence for a promotion
gap and a currency gap on the same path — the argument
`add-duplicate-packet-check` and `add-family-enumeration-check` both made, and
the shape their tests pin.

**What is given up, said plainly.** Shape 1 is the safety net that holds when
someone authors a lossy block anyway and archives it anyway. It is not built
here, so **#330 does not close with this change**; the pre-archive gate is the
cheaper of the two and the one #330 itself calls "where it is cheap", and
building the net first would have been building the second-best half first. The
open box carries an owner and a trigger — `tasks.md` § 7.1.

## D2 — Same-kind exact units, three arms, and a new reserved marker

### Why not lines

PR #358's human verification of the #351 repair was `canon ⊆ intake ⊆ B`
line-by-line, and it worked because that repair copied canon verbatim,
preserving its wrapping. A rule that only works when the author preserved
wrapping is not a rule. `add-family-enumeration-check` re-wrapped the
enumeration paragraph to change one word.

### Why not containment, which is what the first draft of this delta said

The first draft wrote carriage as a unit "appearing in the block" — substring
containment. The review measured what that reading actually does and it fails
the change's own headline case: canon's bullet `**THEN** the selector MUST show
exactly the available catalog entries and their data-handling badges` is a
SUBSTRING of the widened bullet `add-doxchat-model-intake` replaced it with, so
containment reports nothing on the very defect PR #358 had to repair by hand.
Widening a line is the commonest way a clause is silently replaced, and
containment is blind to all of it. Matching is therefore exact, unit for unit,
between units of the same kind.

### Why not similarity

The obvious fix for "an edited sentence looks like a deleted one" is a
near-match threshold. The corpus has already ruled against that reasoning in
"One ruling, one discharge, across archived packets": "A similarity or
near-match rule MUST NOT be used: revising a requirement is not restating it,
and a rule loose enough to conflate the two would report the ordinary case."
Here the cost is sharper than noise: a threshold high enough to pass an ordinary
reword also passes a clause whose meaning has been REVERSED, and #351's ninth
item was exactly that — "every loaded editor MUST remain usable" reverted to
"the Outline and Document editors MUST remain usable".

### Units are normative, because a sentence is not self-evident

The review found 118 backticked tokens with internal periods in canon's
requirement bodies — `.openspec.yaml`, `promotion_fidelity.py`, version
strings. A naive split on `. ` shatters those into fragments that never match
anything, and the arm becomes noise. So the delta states the derivation rather
than leaving it to an implementation: mask backticked spans first, split on a
period, question mark or exclamation mark followed by whitespace or the end of
the paragraph, treat each bullet line as one unit with its marker stripped, and
treat a dated bold note as ONE undivided unit — a note is a single editorial
statement and reporting its sentences separately would be reporting noise about
noise.

### Why bullets are compared across the whole block

The review's fixture is the argument: rename `Gate verbs hide on a composed
view` to `Tile-bound gate verbs hide on a composed view`, declare the rename,
drop two of the four bullets, and a scenario-paired bullet comparison sees
nothing — title declared, no surviving pairing to compare. Four obligations
gone, zero findings. Comparing every canon bullet against every bullet ANYWHERE
in the block closes it: a retitle keeps its bullets or the ledger says which
ones it lost, and the `Merged into` marker handles the legitimate merge without
silencing the bullets underneath.

### Three arms, measured separately

| arm | unit | findings over the active corpus | reads |
| --- | --- | --- | --- |
| scenario-title completeness | a `#### Scenario:` title | **1** | a deletion, precisely |
| carriage ledger | a body unit, or a scenario bullet | **14 units / 10 requirements** | a divergence, of unknown intent |
| title resolution / two-writers | a `(capability, title)` pair | **0** | a structural error |

A single summed family would have buried the one precise signal under fourteen
editorial ones, and a single severity would have forced either a gate nobody
can keep green or an advisory nobody reads.

### The declaration is a NEW marker, and the precedent it was going to reuse
### does not exist

The first draft claimed the corpus already writes dated bold notes declaring
deletions, and pointed at `doc-health`'s "Deterministic check families". The
review checked all five instances of the convention in the corpus: **every one
of them records a caught near-miss and a RESTORATION, never a deletion.** The
note in that very requirement names SEVEN of its eight scenario titles in
backticks — as the seven that were *restored*. A rule that read deletion out of
prose would therefore have read a faithful, scenario-complete restatement of
that requirement as declaring seven deletions, on precisely the requirement
issue #329 is about. The convention cannot be reused, and reusing it would have
inverted the check on its own headline case.

So the marker is new, recognized by FORM: a fixed leading token, a change id, a
date, and unit names written as CommonMark code spans. Two spellings, because
there are two lawful acts — `Removed from canon by <change-id> (<date>):` and
``Merged into `<destination scenario title>` by <change-id> (<date>):``, the
destination naming where the superseded scenarios went rather than a unit.
Whitespace normalization applies to the marker as to every other unit, so a
marker wrapped across lines is still one marker. Three details the review
forced and that a naive form would have got wrong: a unit containing backticks
needs a longer fence, because roughly a third of this corpus's body units and a
sixth of its bullets cite something like `openxFactory` and a single-backtick
span would end at the first inner one; the merge destination must be exempt
from the names, or every valid merge marker reports itself; and a marker must
not be a carriage unit, or it promotes into canon and every later block has to
restate it forever. A marker suppresses only units it names AND that are
actually absent, and one naming a scenario the block still restates is itself
reported.

### The false-positive/false-negative trade, priced

A false positive costs a marker line or a disposition. A false negative costs
canon, silently, and is found by a human at an archive gate if it is found at
all. The arms therefore over-report and say so: the carriage ledger's rule text
in this change's own delta states that a finding "MUST NOT assert that the
divergence is unintended, the arm having no means to distinguish a rewording
from stale text".

## D3 — Advisory at launch, and what stays advisory

`warning` and `info` keep the family out of `runner.main`'s `{CRITICAL}` and
`{CRITICAL, ERROR}` gates. Absence from `FAMILY_RESOLUTION` is the half that is
easy to lose: `report.uncited_resolutions` turns a `contested` finding that
vanishes between reports into an `error`, so a `contested` advisory family reds
the nightly the first time anyone fixes a block. Both halves are pinned by test
and flip together, by ruling.

**The precedent, stated accurately.** Three families carry a
`_LAUNCH_SEVERITY` constant and launched advisory in both halves:
`promotion-fidelity`, `duplicate-packet` and `family-enumeration`. TWO of the
three have flipped to enforcing; `family_enumeration._LAUNCH_SEVERITY` is still
`WARNING`. `release-inventory-drift` never had an advisory launch to flip — it
is permanently absent from `FAMILY_RESOLUTION` with an `info` editorial band
chosen per finding class. `families.py`:1075-1077 records the count in the
corpus's own words: "Two of those three have since flipped to enforcing; this
one flips by its own ruling on its own measured population."

**The asymmetry between the arms is the new part.** The scenario-title arm's
standing population on this repository is ONE finding, on a change whose author
can discharge it with one marker line, so the precedent rule — the flip "SHALL
follow the discharge of the standing population rather than precede it" — is
satisfied by a single edit rather than a campaign. The carriage ledger's
population is standing by construction: every legitimate MODIFIED block edits
something, so the ledger is never empty and never should be. This packet
therefore proposes no flip for it — and does not rule one out either. The first
draft said "ever", which was a decision this packet has no standing to take and
which would have quietly consigned seven of #351's nine items to permanent
advisory status without saying so. The proposal now says which items those are,
in a table, so the scope of the gate is visible rather than inferred.

## D4 — Reuse `release-realization`, do not restate or widen it

`release-realization`'s "Ordered deltas and branch vocabulary" already says it:

> Changes SHALL sequence explicitly: a proposal modifying a requirement already
> modified by an active ratified change references that change and declares its
> deltas relative to that change's outcome.

#357 asks for a check on exactly this and cites those lines. Two temptations
were declined. The first is restating the rule inside `doc-health` so the
family's requirement reads self-contained — how a corpus ends up with two
spellings of one rule and no way to tell which is current, which "Explicit
delta rule" already names a defect. The second is subtler and the review caught
it: the first draft dropped the word `ratified`, obliging every active change
rather than every active ratified one. That is a silent widening of another
capability's rule, and it is now fixed in both deltas — the obligation carries
`ratified` verbatim, and a SEPARATE sentence states that the family's arms READ
every active change regardless of standing because they are advisory. Reading
scope and normative obligation are different things and are now written as
different things.

The reference is read mechanically rather than by judgement: the earlier
change's id occurring as a whole token in the later change's own `proposal.md`,
the same whole-token match the duplicate packet family already uses so that one
change id inside a longer one buys nothing.

Measured over this repository's active changes:

| measurement | figure |
| --- | --- |
| `(capability, requirement)` pairs written by ≥2 active changes | 7 |
| of those, where the modifying proposal names the sibling | **7 of 7** |
| MODIFIED titles resolving to no canon requirement | 7 |
| of those, resolving to an active sibling's `ADDED` | **7 of 7** |
| MODIFIED titles resolving to nothing at all | **0** |

Every one is the MODIFIED-over-a-sibling's-ADDED shape
(`implement-keycloak-install-repo` over `add-identity-brokering`,
`split-openxwallet-repo` over `add-wallet-carried-review-authority` and
`add-trust-anchor`, `add-wallet-carried-review-authority` over
`add-substantive-review-lane`, `implement-openxpki-install-repo` over
`add-trust-anchor`). The rule is already followed; the check makes the
following verifiable, and emits nothing today.

The case it would newly govern is two active changes writing one requirement
that canon ALREADY carries — the `add-doxchat-model-intake` /
`add-doxbench-distilled-abstract` pair PR #358 reasoned about by hand,
concluding that "archive safety is asymmetric" and that intake must archive
first. Which is also the case this change's own § 2.1 creates; see D5.

## D5 — The dogfooding decision, decided by running the check on itself

**Canon still enumerates.** `openspec/specs/doc-health/spec.md` opens "The
doc-health deterministic pass SHALL implement twenty check families ...", with
three numerals in prose. `add-family-enumeration-check` was ratified 2026-08-25
to derive the enumeration from `families.FAMILIES` instead of restating it, and
its CODE has landed — `scripts/doc_health/family_enumeration.py` is on `main`
and `FAMILIES` registers twenty-one — but the change is active and its delta is
unpromoted. So the prose enumeration is still canon, and a change registering a
twenty-second family still owes a MODIFIED block.

**Writing it in a proposal reds a standing gate.** That change's rule requires
an active delta's restatement to be "consistent with the registry in its own
tree", and this packet registers nothing. The block was written anyway —
carried forward from `add-family-enumeration-check`'s outcome per D4,
twenty-one → twenty-two, all eight scenarios restated, per-requirement count
8 → 8 — and the check was run:

```
findings: 3
 - names check family 'modified-block currency', which resolves to
   'modified-block-currency' and is not a registered family
 - says 'twenty-two' check families, but 21 are registered
 - says 'Four' of 'twenty-two', but 21 families are registered

tests/doc-health/test_family_enumeration.py::test_the_real_corpus_reads_zero_on_both_halves
FAILED — assert fe.fam_family_enumeration(Ctx()) == []
```

The block was withdrawn to `tasks.md` § 2.1. With it removed the same call
reads `0` and the suite is green.

**Two consequences are carried forward rather than hidden.** First, § 2.1's
block is itself a MODIFIED block and this family reads it: measured against
`add-family-enumeration-check`'s outcome it does not carry two body sentences —
the enumeration sentence and the `Four of the twenty-one` sentence, both changed
by exactly the numerals this change moves — so it adds ONE carriage-ledger
finding, taking the realization prediction to +1 `warning` and +11 `info`. That
figure is now in the proposal's table rather than being discovered later.

Second, § 2.1 creates the corpus's FIRST two-writers instance between two
ACTIVE changes on a requirement canon already carries. `promotion-fidelity`
orders archived packets by folder date with an archive-commit tie-break; active
changes have neither. The spike resolved "later" by `.openspec.yaml` `created:`
— this packet's 2026-08-27 against `add-family-enumeration-check`'s 2026-08-25 —
which is a reasonable reading and is NOT a ruled one. The delta therefore
states the consequence (the later block is measured against the earlier
outcome) without stating how "later" is decided, and `tasks.md` § 7.3 carries
the open question with an owner. Reading it the other way would measure
`add-family-enumeration-check` against this change's outcome and move the
prediction; that is exactly why it needs a ruling rather than a default.

**So this packet carries no MODIFIED block, and that is the dogfooding result
rather than an evasion of it.** A change cannot commit the currency defect in a
block it does not have. What it can do — and what § 2.1 pins — is owe the block
at the moment the tree can make it true, write it relative to the other active
writer's outcome, and record the per-requirement count at that gate.

## What was considered and not done

**A standalone `scripts/validate-*.py`.** It would need separate CI wiring and
would be invisible to the report a session actually reads. Registration as a
family buys the report section, the ranked-plan line, disposition keying, and
inclusion in the suite that gates every PR.

**An `openspec validate` pre-archive hook**, which #357 offers as an
alternative. `openspec` is a vendored external tool; a rule this corpus owns
should live where this corpus can amend it by proposal, and the archive gate
already runs the doc-health suite.

**Reporting the carriage ledger at `warning`.** Ten standing warnings on a
clean repository is how a report stops being read. `info` is the band
`release-inventory-drift` already uses for an expected steady state.

**Folding #330's shape 1 in as a fourth arm.** It reads a different basis (a
commit's parent) and a different document pair (promoted vs promoted).
Recorded as § 7.1, not built.
