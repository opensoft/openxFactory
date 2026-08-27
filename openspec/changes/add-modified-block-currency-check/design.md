# Design: add-modified-block-currency-check

Status: draft
Proposed: 2026-08-27

This document records WHY the five decisions in the proposal's § Orchestrator
Decisions were taken the way they were, and what was measured before taking
them. Every figure below came from a throwaway implementation of the proposed
rule run over this repository at `9be81a40` before the proposal was written.
None of that spike is committed; it was evidence, not a prototype to grow.

## D1 — A twenty-second family, not an extension of `promotion-fidelity`

#330 offers two shapes and says they are not exclusive. It is right that they
are not, and this change still builds only one of them.

**Canon has already argued this exact question, in its own words.** The
promoted "One ruling, one discharge, across archived packets" requirement
contains this paragraph, written for the duplicate-packet family:

> **This family answers a question the promotion fidelity family cannot.** That
> family compares an archived delta to CANON, and where one ruling has been
> discharged twice canon holds exactly what both packets said it should hold —
> so it reports zero either way. The comparison that can see the class is
> between the archived deltas themselves, which is why this is a separate
> family rather than a wider reading of that one.

Substitute this class and the paragraph holds unchanged: after an archive act
canon IS the delta, so a block that dropped seven scenarios and a canon now
missing them AGREE, and the comparison that can see the loss is between an
ACTIVE delta and the canon it has not yet replaced. Same argument, same shape,
same conclusion. Reaching a different conclusion here would mean the corpus had
two rules for when a comparison earns a family.

**The measurement basis forbids the alternative.** #330's shape 1 — a
promoted→promoted arm diffing the spec across the archive commit — needs the
promoted spec's state at the archive commit's PARENT. "The promotion fidelity
measurement basis is declared" gives that family exactly two bases, checkout
and live `main`, and requires: "A run's report SHALL state which basis this
family measured, in the family's own report section, on every run and whether
or not the family found anything." A third basis inside that family would make
that one line untrue of half its findings, and the requirement's own reasoning
says why that matters — "a report that mixed the two bases without saying which
was which would invite a reader to act on a stale finding as a current one".

**The finding must land where the remedy is.** `promotion-fidelity` is
archived-path-shaped throughout: latest-writer-wins orders archive folders by
`YYYY-MM-DD` prefix, the exemption reads an ARCHIVED packet's `proposal.md`,
and dispositions key on the archived delta's stable path. This class's remedy
is an edit to an ACTIVE delta on a branch. A family reporting against archived
paths cannot address it, and D5 of that family's own design — "the finding
lands on the archived delta's path, not the promoted spec's, because it is what
a disposition needs to key on" — is the reason the two cannot share a family.

**The dispositions would collide.** `health/dispositions.yaml` keys on
`(family, repo, path)`. Folding this class into `promotion-fidelity` would let
one citation buy silence for a promotion gap and a currency gap on the same
path — the argument `add-duplicate-packet-check` and `add-family-enumeration-check`
both made, and the shape their tests pin.

**What is given up, said plainly.** Shape 1 is the safety net that holds when
someone authors a lossy block anyway and archives it anyway. It is not built
here. The pre-archive gate is the cheaper of the two and the one #330 calls
"where it is cheap", and building the net first would have been building the
second-best half first. It is `tasks.md` § 5.1, with this reasoning attached.

## D2 — Verbatim after whitespace normalization, three arms, and where the
## declaration lives

### Why not lines

PR #358's human verification of the #351 repair was `canon ⊆ intake ⊆ B`
line-by-line, and it worked because that repair copied canon verbatim,
preserving its wrapping. A rule that only works when the author preserved
wrapping is not a rule. `add-family-enumeration-check` re-wrapped the
enumeration paragraph to change one word, which line containment would have
reported as several losses and one addition.

### Why not similarity

The obvious fix for "an edited sentence looks like a deleted one" is a
near-match threshold. The corpus has already ruled against that reasoning in
"One ruling, one discharge": "A similarity or near-match rule MUST NOT be used:
revising a requirement is not restating it, and a rule loose enough to conflate
the two would report the ordinary case." Here the cost is sharper than noise: a
threshold high enough to pass an ordinary reword also passes a clause whose
meaning has been REVERSED, and #351's ninth item was exactly that — "every
loaded editor MUST remain usable" reverted to "the Outline and Document editors
MUST remain usable". A rule that cannot see a reversion is not worth its false
negatives.

### So: three arms, measured separately

Whitespace normalization — runs of whitespace to one space, strip — is the
minimum that survives re-wrapping and nothing more. The units are then split
three ways, and the arms are reported separately because their measured
signal-to-noise differs by an order of magnitude:

| arm | unit | findings over the active corpus | reads |
| --- | --- | --- | --- |
| scenario-title completeness | a `#### Scenario:` title | **1** | a deletion, precisely |
| carriage ledger | a body sentence, or a bullet of a restated scenario | **13 units / 10 requirements** | a divergence, of unknown intent |
| title resolution / two-writers | a `(capability, title)` pair | **0** | a structural error |

A single summed family would have buried the one precise signal under thirteen
editorial ones, and a single severity would have forced either a gate nobody
can keep green or an advisory nobody reads.

### The declaration

An intentional deletion needs a machine-readable statement, and the cheapest
honest one is the convention the corpus already writes: a dated bold note
INSIDE the MODIFIED block. Canon's own "Deterministic check families" carries
one — `**CORRECTED 2026-08-25 ON BRETT'S RULING — this block is now
SCENARIO-COMPLETE.**` — and it names its seven lost scenarios verbatim in
backticks, which is exactly the parse this family needs. Making an existing
convention machine-read costs an author nothing they were not already doing;
inventing a `REMOVED:` pseudo-block would add a second grammar for deletion
next to OpenSpec's own `## REMOVED Requirements`, which operates at requirement
granularity and has no scenario-level form.

The declaration lives in the delta rather than in `dispositions.yaml` for the
reason PR #85 and PR #358 both demonstrate: the record of a deletion should
travel with the text that performs it, so the next reader of the block sees it
without a second file. `dispositions.yaml` remains the fallback where the delta
is ratified and re-authoring it is itself a governance act.

### The false-positive/false-negative trade, priced

A false positive costs a declaration sentence or a disposition. A false
negative costs canon, silently, and is found by a human at an archive gate if
it is found at all. The arms are therefore tuned to over-report and to say so:
the carriage ledger's rule text states in canon that it "MUST NOT assert that
the divergence is unintended, the arm having no means to distinguish a
rewording from stale text".

## D3 — Advisory at launch, and only one arm ever asks for the flip

`warning` and `info` keep the family out of `runner.main`'s `{CRITICAL}` and
`{CRITICAL, ERROR}` gates. Absence from `FAMILY_RESOLUTION` is the half that is
easy to lose: `report.uncited_resolutions` turns a `contested` finding that
vanishes between reports into an `error`, so a `contested` advisory family reds
the nightly the first time anyone fixes a block. Both halves are pinned by test
and flip together, by ruling — the discipline `add-promotion-fidelity-check`
and `add-duplicate-packet-check` each took, in one commit, in both halves.

What is new here is the asymmetry. Four families have now launched advisory and
three have flipped; the reflex is to write "the flip is a task box" and stop.
That would be wrong for the carriage ledger, whose population is standing by
construction — every legitimate MODIFIED block edits something, so the ledger
is never empty and never should be. Declaring it a permanent editorial band
rather than a gate-in-waiting is the honest reading, and it protects the arm
that IS a gate: a section carrying ten permanent yellow rows is a section
readers learn to skip, and the one warning that matters would go with them.

The scenario-title arm's flip is unusually cheap to reach. Its standing
population on this repository is ONE finding, on a change whose author can
discharge it with one declarative sentence. The precedent rule — "SHALL follow
the discharge of the standing population rather than precede it" — is satisfied
by a single edit rather than a campaign.

## D4 — Reuse `release-realization`, do not restate it

`release-realization`'s "Ordered deltas and branch vocabulary" already says it:

> Changes SHALL sequence explicitly: a proposal modifying a requirement already
> modified by an active ratified change references that change and declares its
> deltas relative to that change's outcome.

#357 asks for a check on exactly this and cites those lines. The temptation is
to restate the rule inside `doc-health` so the family's requirement reads
self-contained. That is how a corpus ends up with two spellings of one rule and
no way to tell which is current — the failure the "Explicit delta rule" already
names as a defect ("Accidental restatement of promoted policy in differing
words SHALL be treated as a defect"). So the new requirement adds only the
CONSEQUENCE that is genuinely new: a block declared relative to another active
change's outcome is measured against that outcome, and must carry that change's
additions.

Measured over this repository's active changes:

| measurement | figure |
| --- | --- |
| `(capability, requirement)` pairs written by ≥2 active changes | 7 |
| of those, where the modifying proposal names the sibling | **7 of 7** |
| MODIFIED titles resolving to no canon requirement | 7 |
| of those, resolving to an active sibling's `ADDED` | **7 of 7** |
| MODIFIED titles resolving to nothing at all | **0** |

Every one of the seven is the MODIFIED-over-a-sibling's-ADDED shape
(`implement-keycloak-install-repo` over `add-identity-brokering`,
`split-openxwallet-repo` over `add-wallet-carried-review-authority` and
`add-trust-anchor`, `add-wallet-carried-review-authority` over
`add-substantive-review-lane`, `implement-openxpki-install-repo` over
`add-trust-anchor`). The rule is already being followed; the check makes the
following verifiable, and emits nothing today.

The case the check would newly govern is two active changes writing one
requirement that canon ALREADY carries — the `add-doxchat-model-intake` /
`add-doxbench-distilled-abstract` pair PR #358 had to reason about by hand,
concluding that "archive safety is asymmetric" and that intake must archive
first. That reasoning is exactly what the arm mechanizes.

## D5 — The dogfooding decision, decided by running the check on itself

This is the decision the assignment named as a trap, and it turned out to have
a measured answer rather than a judged one.

**Canon still enumerates.** `openspec/specs/doc-health/spec.md` opens
"The doc-health deterministic pass SHALL implement twenty check families ...",
with three numerals in prose. `add-family-enumeration-check` was ratified
2026-08-25 to derive the enumeration from `families.FAMILIES` instead of
restating it, and its CODE has landed — `scripts/doc_health/family_enumeration.py`
is on `main` and `FAMILIES` registers twenty-one — but the change is ACTIVE and
its delta is not promoted. So the prose enumeration is still canon, and a
change registering a twenty-second family still owes a MODIFIED block.

**Writing it in a proposal is not possible without reddening a standing gate.**
That change's own promoted-to-be rule requires an active delta's restatement to
be "consistent with the registry in its own tree", and this packet registers
nothing. The block was written anyway — carried forward from
`add-family-enumeration-check`'s outcome per D4, twenty-one → twenty-two, all
eight scenarios restated, per-requirement scenario count 8 → 8 — and the check
was run against it:

```
findings: 3
 - names check family 'modified-block currency', which resolves to
   'modified-block-currency' and is not a registered family
 - says 'twenty-two' check families, but 21 are registered
 - says 'Four' of 'twenty-two', but 21 families are registered

tests/doc-health/test_family_enumeration.py::test_the_real_corpus_reads_zero_on_both_halves
FAILED — assert fe.fam_family_enumeration(Ctx()) == []
```

The block was withdrawn and moved to `tasks.md` § 2.1, to be written in the
same commit that registers the family. With the block removed the same call
reads `0`, and the suite is green.

**So this packet carries NO MODIFIED block, and that is the dogfooding result
rather than an evasion of it.** A change cannot commit the currency defect in a
block it does not have. What it can do — and what § 2.1 pins — is owe the block
at the moment the tree can make it true, write it relative to the other active
writer's outcome, and record the per-requirement count at that gate. The
ordering dependency on `add-family-enumeration-check` is recorded exactly the
way that change recorded its own dependency on `add-promotion-fidelity-check`:
in the packet, by name, as an ordering fact rather than a defect in either
change.

There is one asymmetry worth stating. If `add-family-enumeration-check`
archives first, § 2.1's block is written over canon-at-twenty-one and the
"relative to" note becomes historical. If this change's realization lands
first, § 2.1's block must still declare itself relative to that change's
outcome, and that change must then carry this family forward — which is the
same asymmetry PR #358 named for intake and B, and the same remedy: the later
archiver carries both.

## What was considered and not done

**A standalone `scripts/validate-*.py`.** It would need separate CI wiring and
would be invisible to the report a session actually reads. Registration as a
family buys the report section, the ranked-plan line, disposition keying, and
inclusion in the suite that gates every PR.

**An `openspec validate` pre-archive hook**, which #357 offers as an
alternative. `openspec` is a vendored external tool; a rule this corpus owns
should live where this corpus can amend it by proposal, and the archive gate
already runs the doc-health suite.

**Reporting the carriage ledger at `warning`.** Thirteen standing warnings on a
clean repository is how a report stops being read. `info` is the band
`release-inventory-drift` already uses for an expected steady state, for the
same reason.

**Folding #330's shape 1 in as a fourth arm.** It reads a different basis (a
commit's parent) and a different document pair (promoted vs promoted). It is
recorded as § 5.1, not built.
