# Design: add-duplicate-packet-check

Status: ratified
Ratified by: add-duplicate-packet-check

The decisions this change had to take, and the measurements each rests on.
Every number below was taken against this repository's checkout — 91 archived
packets, 543 distinct (capability, requirement, content) identities — before
the proposal was written, and RE-TAKEN at `44505d1e` after this branch merged
main. The figures are identical across both measurements; they are re-stated
rather than carried, because #316, #320, #322, #323, #324 and #325 all landed
in between.

## D1 — A sibling family, not a finding kind inside promotion fidelity

The two questions look adjacent enough that folding them together is the
obvious first move. It is the wrong one, for three reasons of decreasing
abstraction.

**The dispositions collide, concretely.** `health/dispositions.yaml` entries
key on `(family, repo, path)`, optionally narrowed to a requirement. Both
families report against an ARCHIVED DELTA's path, and the same delta is exactly
the kind to attract both classes: a delta that failed to reach canon is a delta
somebody will write a remedial for, and a remedial is what this family
watches. One entry disposing a promotion gap on that path would silently
dispose a duplicate discharge on it too — two different governance decisions
bought with one citation, and the second one never taken by anybody.
`test_a_disposition_for_the_neighbouring_family_disposes_nothing` pins the
separation.

**The remedies are opposite.** Promotion fidelity's action line says "apply the
ratified delta to the promoted spec through an OpenSpec change, or record the
non-promotion as deliberate". This family's says "name the packet this one
restates in its proposal, or withdraw the duplicate discharge". A family
carries ONE action string; a reader acting on the wrong one would apply a delta
that has already been applied twice.

**The report's per-family count would conflate two questions.** "promotion-
fidelity: 3" means nothing if one of the three is a duplicate discharge, and
the nightly's ranked plan is read by count first.

What IS shared is shared completely. This module owns no delta grammar, no
`Status:` reader, and no dispositions reader: it reads through
`promotion_fidelity.parse_delta`, `promotion_fidelity.declares_pre_ratification`
and `promotion_fidelity.load_dispositions(ctx, FAMILY)`. The seams added to
that module are additive and behaviour-preserving — `DeltaRequirement.body` is
new data on an existing parse, and the two new names delegate to the existing
implementations so a test monkeypatching `_is_exempt_from_promotion` still
moves both callers. A second grammar for one document's headings is how two
readers of one document come to disagree about what it says, which is the
lesson that module already records about its own promoted-spec reader.

## D2 — Byte-equality above trailing whitespace, and the boundary is the design

The identity rule is the whole family. Loosen it and the family reports the
ordinary case; tighten it and it reports nothing.

**What is normalized: trailing whitespace only** — per-line trailing spaces,
and trailing blank lines. Both are invisible to every reader and are added or
removed by editors nobody chose. A requirement that sits at end-of-file in one
packet and above a following block in another is the same requirement.

**What is not: everything else.** A re-wrapped paragraph, a changed article, a
reordered scenario — each is an edit a human made to normative text. The
temptation is a similarity score, and it must be refused on principle rather
than on tuning: a deterministic family that decides two governance acts are
"the same enough" has invented judgement, and the judgement it invents lands on
the ordinary case. 59 (capability, requirement) pairs in this repository have
more than one archived writer, and revising a requirement is not restating it.

**Leading blank lines are NOT stripped**, which is a deliberate false-negative:
two packets differing only in the blank line between a requirement header and
its prose stay quiet. The promise is byte-equality above the trailing rule, not
a best effort at it, and for an advisory launch the safe direction is to
under-report.

**The requirement's own heading line is excluded from the compared bytes.** The
title is already compared through `norm` (whitespace-collapsed, casefolded), so
folding the heading into the body would let a title's spacing decide the
content rule — two packets spelling one title `### Requirement:  X` and
`### Requirement: X` would read as different statements.

**Scenario headings ARE included.** The body is the whole block. A build that
fingerprinted only prose would call two packets identical while their scenarios
differed, which is the exact gap the neighbouring family's own true positive
lived in — a requirement that arrived in canon carrying four of its six
ratified scenarios.

## D3 — The lineage exemption, and why the naming is not an authority claim

This is the load-bearing decision, because without it the family fires on the
remedy its neighbour prescribes.

**The pattern that must stay legal.** codexFactory PR #85 and this repository's
own `apply-branch-sessions-deltas` both exist to apply a ratified delta that
archived without reaching canon. Both restate the original delta
BYTE-FAITHFULLY, deliberately: any edit would be new normative content carried
under an old ratification, and PR #85's evidence made the point by hashing its
delta against the archived one and diffing the extracted requirement block out
of canon afterwards. A byte-faithful restatement is therefore not a smell — it
is the prescribed shape.

**What separates it from a second discharge is the record, not the bytes.** The
remedial names the packet whose ruling it applies. So the rule is: a pair where
EITHER proposal names the other's change id is a recorded remedial lineage and
stays quiet. Bidirectional, because a superseding addendum on an original can
name a later packet as easily as the reverse.

**THE NAMING RECORDS LINEAGE, NOT AUTHORITY**, and the distinction is worth
stating precisely because the rule reads like a permission if you squint.
Naming the original does not establish that the restating packet had standing
to restate. The ratification that makes the restatement lawful is the
ORIGINAL's; a packet claiming standing it lacks is a ratification-citation
defect, and `ratified-provenance` is the family that reports it. What the naming
buys is TRACEABILITY: a reader of the archive can see one ruling, one
discharge, and a recorded application of it — rather than two independent
discharges that happen to agree. This family reports untraceable restatement.
It declines to adjudicate standing, and a build that let it start doing so
would be enforcement wearing an advisory label.

**Where the naming is read: `proposal.md`, and only there.** A packet's
`design.md` and `tasks.md` are working notes; the proposal is the packet's
normative face and the document every other lifecycle family already reads to
learn what a packet claims. Lineage recorded only in a task note is lineage a
reader of the record does not see, which is the state this family exists to
report.

**Both spellings, matched as a whole token.** The corpus names a packet as a
bare change id (`add-workbench-branch-sessions`) and as an archived folder
(`openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/`), often in
one paragraph — `apply-branch-sessions-deltas` does exactly that on consecutive
lines. Both are accepted. The boundaries are `[\w-]` rather than `\b`, because
change ids are hyphenated and `\b` treats a hyphen as a boundary: a plain
substring test lets `add-foo` match inside a packet that only ever names ITSELF
as `add-foo-extended`, and the exemption would be bought by a coincidence of
naming. The fixture carries that exact pair and
`test_a_substring_lineage_test_would_silence_the_prefix_pair` runs the same
fixture both ways to show the two rules DISAGREE — the measurement discipline
the neighbouring family used for its tie-break, applied here.

**Two exemptions are borrowed, not invented.** A packet declaring a
pre-ratification standing (the C5 rule) discharged no ruling and can duplicate
none; and `health/dispositions.yaml` suppresses under the same contested-finding
discipline every other family applies. Neither is a new marker.

## D4 — The pinned basis, deliberately unlike the neighbour's

The 2026-08-24 ruling (task 4.1, PR #315) put the live-`main` basis on the
promotion-fidelity family AND ON THAT FAMILY ALONE, and that family's
`basis_notes` prints, on every run including a clean one: "every other family in
this report measures the pinned checkout." Joining the ruled basis would make
that sentence false, and amending a ruled sentence to accommodate an
implementation choice is the wrong direction of travel.

So `_repo_trees` builds a `WorkingTree` and nothing else, structurally — the
module cannot even name the basis option, and a test asserts it. The cost is
bounded: on an aggregation run a lagging pin delays a duplicate's report by
however long the pin lags. The catch point that matters is unaffected, because
a duplicate arrives in the PULL REQUEST that adds the second packet and a
repository's self-gate run reads its own tree at that tip. Moving this family
onto live mains is available as a ruling — tasks §5.2 — and is not available as
an implementation detail.

## D5 — Pairwise, and one finding per unaccounted pair

Three packets restating one requirement produce three pairs, not one group.
That is the arithmetic tonight's near miss actually needs: an original and two
remedials, both remedials naming the original, means two pairs carry lineage and
ONE does not. A group-level rule ("this requirement is stated by three packets")
would either fire on all three or on none, and both answers are wrong.

The finding lands on the LATER packet's delta path — the redundant discharge is
what a reader acts on — with the earlier packet named in the rule text. "Later"
is the archive folder's date, then the folder name, and version-control history
is deliberately NOT consulted. The neighbouring family consults it because
ordering decides WHICH statement canon must match, so a wrong answer there is a
wrong finding; here it decides only which of two already-reported packets
carries the path. A rule needing no history is the right cost for a cosmetic
ordering, and it makes a fixture tree with no commits report exactly what a
real checkout does.

## D6 — Advisory at launch, in both halves — FLIPPED TO ENFORCING 2026-08-25

**Ruled by Brett, verbatim: "flip the duplicate-packet check to enforcing".**
Both halves in one commit: `_LAUNCH_SEVERITY = ERROR` and
`FAMILY_RESOLUTION["duplicate-packet"] = CONTESTED`. The reasoning below is the
launch reasoning and is kept, not rewritten — it is what the flip flipped FROM,
and the sequencing rule it states is the rule the flip had to satisfy.

It did satisfy it. The population was measured on the basis this family
enforces on (the pinned checkout) and read **zero across five governed
repositories and 206 archived packets** — decisively including codexFactory,
whose single restated identity is PR #85's remedial, the archetype of the
lawful pattern D3's exemption exists to protect. What the flip did NOT get is
the full fourteen-submodule discharge `add-promotion-fidelity-check` §4.3 took
before its own flip; that gap is recorded as an open box (`tasks.md` §5.4)
rather than folded into the tick.

The flip settles nothing about D4: this family enforces on the PINNED basis,
which is the basis it was measured at zero on. Enforcing on a tree is not an
argument for enforcing on a different one, so §5.2 stays open.

### The launch reasoning, kept

Identical to the neighbouring family's D3 AS THAT FAMILY LAUNCHED, and taken
for the same reason on the same day. Not identical to that family's state
today: PR #325 flipped promotion fidelity to `error` + `CONTESTED`, both halves
together, and copying the flipped values here would copy a conclusion without
its premise. That flip was ruled "ENFORCING, SEQUENCED" and sequenced behind
the discharge of a measured standing population, on
`govern-openspec-corpus-membership`'s rule that "a gate that goes red on the
commit that introduces it teaches everyone to route around the gate". This
class has no discharged population; it has a corpus measured at zero and one
near miss.

The flipped neighbour is also a hazard this family must not create, and the
`44505d1e` skip-path fix is the shape of it — a contested family's findings
being read as resolved by a run that never ran them, manufacturing
`uncited-resolution` errors. It cannot reach here: `runner` applies
`FAMILY_RESOLUTION.get(f.family, f.resolution)` on a finding's OWN family, so a
`duplicate-packet` finding never inherits the neighbour's class even when both
families report against the same archived delta. `warning` severity keeps the family out of `runner.main`'s
`{CRITICAL}` and `{CRITICAL, ERROR}` gates. Absence from `FAMILY_RESOLUTION` is
the half that is easy to lose: `report.uncited_resolutions` turns a `contested`
finding that vanishes between reports into an `error`, so a `contested` entry
would red the nightly the first time anyone withdrew a duplicate this family
reported — enforcement arriving through the back door on the very run that
proved the advisory launch worked. Both halves are pinned by test, and the flip
raises severity and adds the entry TOGETHER, by ruling (tasks §5.1).

## What was measured, and what it says

| measurement | figure |
| --- | --- |
| archived packets in scope | 91 |
| distinct (capability, requirement, content) identities | 543 |
| identities restated by more than one packet | 2 |
| findings WITH the lineage exemption | **0** |
| findings WITHOUT it | **2** |

Both restated identities are the original `2026-08-01-add-workbench-branch-sessions`
and its landed remedial `2026-08-25-apply-branch-sessions-deltas`. The remedial's
proposal names the original six times, in both spellings. The exemption is
therefore not a hypothetical accommodation — it is the only thing standing
between this family and a false positive on the corpus's single instance of the
lawful pattern, and the corpus proves it uses the exemption rather than merely
tolerating it.
