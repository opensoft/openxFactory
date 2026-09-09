---
code_surface: none — MEASURED, not assumed. No script, test, workflow, contract, schema or example reads the word this packet reserves, and the delta is pure requirement prose. Evidence, taken 2026-09-09 on the clone of `main` this packet was authored against: (1) `grep -rn "lawful" scripts/ tests/` returns 66 lines across 33 files, and EVERY ONE is prose — a module or test docstring, a comment, or a fixture NAME (`tests/doc-health/fixtures/modified-block-currency-collision/.../lawful-rename`, `tests/ideation-dashboard/test_doxbench_status_exemption.py`'s local variable `lawful`) — with not one of them an assertion over the text of `openspec/specs/neutral-product-pin/spec.md` and not one of them reachable from this requirement; (2) `grep -rn "A consumption pin that another repository reads\|A repository with no stack pin adopts the gate anyway\|declared interim\|consumption copy" scripts/ tests/ .github/` returns exactly ONE line, `scripts/validate-pin-registrations.py:27`, and it is a DOCSTRING quoting the requirement's REGISTRATION sentences (the `id`/`path`/`type`/`intended_consumers`/`adapter_owner`/`consumption_rule` list and the checkout-at-the-pinned-ref recipe) — none of which this packet touches; that script reads `contracts/manifest.yaml` rows and never opens the specification file; (3) no test pins this capability's scenario count or scenario titles (`EveryRatifiedScenarioHasATest` exists only in `tests/review_lane_pin/test_repin_lane.py`, over `review-lane-floor-mirror`), so the one ADDED scenario reds nothing. The one mechanical consumer of the delta is `doc-health`'s modified-block-currency family, which reads every active block by construction and is a GATE rather than a surface. Under `release-realization` an empty code surface archives ON LANDING plus its own task list, not on merged-plus-green realization evidence.
target_release: none — no code surface, no contract bundle, no digest set and no release tag. Nothing under `contracts/` is touched, no `contracts/releases/<tag>.digests.yaml` moves, and no consumer's pin has to advance to receive this. The realization of a wording amendment IS its promotion at archive, which is a separate act on Brett Heap's word.
sequenced_after: []
---

# Proposal: amend-neutral-product-pin-interim-copy-vocabulary

Status: draft
Proposed: 2026-09-09, in lane `openxfactory-1` (display `openXfactory-1`), on
Brett Heap's word of 2026-09-09, verbatim **"R1 'lawful' amendment packet"**,
given in session as one option of several put to him.
Origin: openxFactory issue
[#868](https://github.com/opensoft/openxFactory/issues/868), filed by this lane
out of Codex's refused P2 on PR
[#780](https://github.com/opensoft/openxFactory/pull/780).
**THE WORD AUTHORIZED THE PROPOSING, NOT THE CONTENT. RATIFICATION IS OWED AND
IS BRETT HEAP'S ACT** — nothing below is ratified by being authored, no
requirement here may be cited as approved until he rules on this packet itself,
and **NOTHING IS PROMOTED**: this pull request edits no file under
`openspec/specs/`, no script, no test, no contract and no workflow. The
judgments this authoring session took are `design.md` **D1 through D6**, each
with a recommendation, each put for veto.

## Why

**One word carries two statuses in one ratified requirement, so the same
declared interim copy reads as admitted in the scenario and as not-compliant in
the body four lines above it.**

The requirement is *A consumption pin that another repository reads is a
PUBLISHED contract member, adopted by pin-sync*
(`openspec/specs/neutral-product-pin/spec.md:264-384`). Its body, at `:344-345`:

> Declaring the copy therefore makes it AUDITABLE and does not make it LAWFUL:
> the declaration is what lets a reader say which bytes ran, and that
> requirement's enforcement claim REMAINS UNMET for as long as the copy stands.

Its fallback scenario, at `:371-374`:

> #### Scenario: A repository with no stack pin adopts the gate anyway
> - **WHEN** a repository that carries no `xfactory:` stack pin wires the gate from a copy
> - **THEN** the copy is lawful ONLY as a declared interim naming the `openxFactory` commit it was taken from, the digest of what it copied, and the divergence it accepts
> - **AND** it is retired when that repository adopts a stack pin, an undeclared duplicate never becoming lawful by being useful

A third use, at `:299-300`, is the body's: *"a copy is not made lawful by being
current on the day it is taken."*

**THE TWO ARE NOT ACTUALLY IN CONFLICT ABOUT THE RULE, and this packet does not
move the rule.** They are scoped to different obligations, and the ratified text
says so. The body clause opens by naming ONE other requirement — *"This
capability's promoted requirement **A required check runs the pinned tool, at
the pinned digest** holds that a REQUIRED check SHALL NOT invoke an in-tree
copy…"* — so in that scope *"does not make it LAWFUL"* means the declared copy
does not satisfy THAT requirement, and the paragraph closes by saying it
directly: *"A packet admitting the fallback SHALL NOT describe the interim as
satisfying the required-check requirement."* The scenario is scoped to this
requirement's OWN fallback: the copy is admitted *"ONLY as a declared interim"*,
on three named terms and no others.

**What the text does not do is say that in one place with one pair of words.**
Using the single word `lawful` on both sides of the distinction is what makes
the two lines read as contradictory at a glance, and a reader who reaches `:373`
first can certify a declared interim copied gate as compliant — which the body
forbids in the next paragraph but the scenario does not say. That is a real
defect of expression in ratified canon.

## Why this is NOT a plain fix

**Because the text is PROMOTED, RATIFIED CANON, and the pull request that found
the defect refused to edit it for exactly that reason.**

The requirement was ratified by Brett Heap on 2026-09-07 as part of
`publish-openspec-cli-pin-as-contract-member` (PR
[#757](https://github.com/opensoft/openxFactory/pull/757) → `a5940811`,
ratifying commit `05a9db8b`) and written into the specification byte-for-byte by
the archive act, PR [#780](https://github.com/opensoft/openxFactory/pull/780) —
whose own evidence is that the promoted block is byte-identical to the ratified
delta (sha256 `8d31ffee932339919461da8d69ec4287ad15d14f39f9e64df7c2b13f82bbd902`,
9,462 bytes, on both sides).

Codex raised the defect there as a **P2** on
`openspec/specs/neutral-product-pin/spec.md:343`:

> Reconcile the fallback's conflicting compliance status … distinguish
> "permitted as an interim" from "compliant with the required-check
> requirement", or use one consistent status.

Lane `openxfactory-1` **REFUSED it in that pull request**, on the pull request's
hard limit rather than on the reading:

> Rewording the requirement here would (1) edit ratified text with no word
> behind it and (2) destroy the very byte-identity that makes this archive
> auditable. **Amending promoted canon is an amendment packet's act, on its own
> ratification** — the estate has a shape for exactly this (`amend-*` changes
> with a `## MODIFIED` block), and it is not something an archive may do in
> passing.

The same refusal recorded the remedy and left the successor to the owner's word:
*"the fix is a vocabulary change … and **not** a change to which behaviours are
admitted — no consumer's conformance outcome moves either way."* Working rule 3
says the same in general: a ratified requirement changes only by a ratified
change. **This packet is that successor**, and Brett Heap's word of 2026-09-09
— *"R1 'lawful' amendment packet"* — is what put it in the queue.

## What Changes

**ONE `## MODIFIED` requirement. TWO SCENARIO BULLETS, ONE ADDED BODY
PARAGRAPH, ONE ADDED SCENARIO — and every other word of the requirement is
canon's own.**

- **RESERVED, and scoped:** where THIS REQUIREMENT speaks of a consumption's
  status, `LAWFUL` names exactly ONE consumption and is spent on no other — the
  read a repository carrying an `xfactory:` stack pin performs by checking
  `openxFactory` out at its own `stack.yaml` `xfactory.contract_ref` and
  invoking the entrypoint the registered pin names FROM THAT CHECKOUT. The
  reservation is deliberately NOT capability-wide: the specification's fifth use
  of the word, at `:555`, is in a different requirement and on a different
  subject (*"the canon that makes the acceptance lawful"*, of a DISPOSITION),
  and a capability-wide claim would put that ratified sentence in violation on
  the day this promoted — a rule change and a scope widening in one.
  `design.md` **D0a** records the measurement.
- **GIVEN ITS OWN WORD:** a declared consumption copy is **TOLERATED** — admitted
  by this requirement's fallback, on its four terms (the `openxFactory` commit it
  was taken from, the digest of what it copied, the divergence it accepts, and
  its retirement when a stack pin is adopted) and on no others — and is never
  LAWFUL.
- **THE TWO BULLETS, one word each:** `:373` *"the copy is **lawful** ONLY as a
  declared interim…"* becomes *"the copy is **TOLERATED** ONLY as a declared
  interim…, and is never LAWFUL, which this requirement spends on a stack-pinned
  read alone"*; `:374` *"an undeclared duplicate never becoming **lawful** by
  being useful"* becomes *"…never becoming **tolerated** by being useful"*. Both
  are declared by one `Removed from canon` marker and replaced in place; neither
  is dropped.
- **THE ADDED PARAGRAPH** states the reservation in ONE place, so a later reader
  does not have to re-derive the two scopes from two paragraphs eighty lines
  apart, and forbids the substitution in records: *"A packet, a review record or
  a gate record SHALL NOT describe a tolerated interim as lawful or as
  compliant."*
- **THE ADDED SCENARIO** — *A record describes a declared interim copy as
  lawful* — asserts it, because a rule this capability states only in prose is a
  rule with no scenario a reader can point at.
- **CARRIED UNCHANGED, deliberately:** the `:299-300` and `:344-345` sentences.
  Both already use `lawful` the reserved way and are right as written; changing
  them would be the widening this packet refuses.

**NO BEHAVIOUR MOVES.** The same copies are admitted, on the same four terms.
The required-check enforcement claim stays unmet for exactly as long as it did
before, and is discharged by exactly the same act — retiring the copy for a
stack pin. No consumer's conformance outcome changes in either direction, which
is what the refusal on #780 predicted and what makes this a wording amendment
rather than a rule change.

## Impact

- **Specification:** one requirement of `neutral-product-pin`. No requirement is
  ADDED, RENAMED or REMOVED; no other capability is touched.
- **Code:** none. See the `code_surface` front matter for the measurement.
- **Contracts, bundles, digests, tags:** none.
- **The estate's one live declared copy** — `xFactory-Hermes-Install` #72 →
  `06c9083d`, recorded by #780's archived `tasks.md` § 5.1 as still owing this
  requirement's third field, the per-file digest — is UNAFFECTED. It was not
  compliant before and is not compliant now; what changes is the word a record
  must use for it, and the owed digest stays owed.
- **Readers:** a packet, review or gate record written after promotion must say
  TOLERATED where it means admitted-as-an-interim. Nothing already written is
  invalidated: the archived #780 record calls the interim's digest *"owed rather
  than counted as met"*, which is correct under both vocabularies.

## Sequencing

`sequenced_after: []` — the POSITIVE ROOT CLAIM, and it is measured rather than
assumed.

The requirement this block modifies is already promoted, so nothing has to land
first for the block to be written against canon. Exactly one other active change
carries a `neutral-product-pin` delta — **`split-opendox-two-layer-product`**
(ratified 2026-09-05, another lane's) — and it modifies *An external neutral
product is pinned by commit and digest, never by tag* and *The consuming
repository's pin is authoritative among reachable checkouts*. **Neither is the
requirement this packet modifies**, and no active change writes this
requirement's key (grepped across every active `openspec/changes/*/specs/*/spec.md`
on 2026-09-09). This change is therefore the **SOLE ACTIVE MODIFIER** of that
requirement: `modified-block-currency`'s two-writers rule is scoped to two
active writers, it does not reach the pair, no ordering declaration is owed in
either direction, and neither packet's block has to be measured against the
other's outcome. The two blocks share a spec FILE and no requirement key, which
is not a collision — a file is not the unit the rule is written over.

**AND THE SWEEP LEDGER SAYS SOMETHING DIFFERENT, WHICH IS NOT A CONTRADICTION
AND IS RECORDED RATHER THAN SMOOTHED.** `tests/sequenced_after/corpus-ledger.yaml`
grades `class` over the WHOLE corpus, archived changes included, so this row
reads `co-modifier`: the requirement key it writes is also written by the
ARCHIVED `publish-openspec-cli-pin-as-contract-member`, which is unavoidable and
definitional — that is the change that PROMOTED the requirement this packet
amends, and every amendment of promoted canon shares a key with the packet that
promoted it. Seeding this row therefore also flips that archived partner's row
from `sole` to `co-modifier`, which is the ledger's own documented behaviour
("a pull request moves ITS OWN ROW and a partner's row when its
`## MODIFIED Requirements` block flips that partner from sole to co-modifier").
The two gradings answer different questions — the ledger asks *has any other
change in history written this key*, the ordering rule asks *is another ACTIVE
RATIFIED change writing it now* — and only the second decides whether a
declaration is owed.

`split-opendox-two-layer-product` is named in `.openspec.yaml`'s `related:` as
the measured neighbour, and **that naming is not an ordering declaration**: the
family reads a declaration as the sibling's change id occurring as a whole token
in the DECLARING change's own `proposal.md`, and this proposal names it only to
record that the requirement sets are disjoint.

## What this proposal does NOT claim

- It does not claim the ratified rule was wrong. The two scopes were already
  distinguishable, and the refusal on #780 set out the reading that makes them
  so; what is fixed is that the distinction had no pair of words.
- It does not widen or narrow the fallback. Three declared fields plus the
  retirement trigger, before and after.
- It does not certify anything. No declared copy becomes compliant, and the
  required-check requirement is not modified, quoted differently, or reached.
- It does not fix the strict-validation failure this specification carries on
  `main` (`requirements.16.text: Requirement must contain SHALL or MUST
  keyword`, on *A pinned artifact that resolves dependencies at install time
  carries a vendored lockfile…* at `:645`). That is a different requirement and
  a different sentence, this block does not inherit it, and no word has been
  given for it — `design.md` D6 records the measurement and names it as an
  available successor rather than taking it.
- It ratifies nothing. `Status: draft`; ratification and archive are separate
  acts on Brett Heap's word.
