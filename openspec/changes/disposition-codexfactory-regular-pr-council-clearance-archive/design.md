# Design: disposition-codexfactory-regular-pr-council-clearance-archive

Status: draft
Date: 2026-09-11
Kind: design

Six decisions. Five are the shape of the precedent's; the sixth is new, because
this is the first packet in this corpus to RETIRE a disposition rather than only
add one, and the first to put a SECOND CLASS into a list that has been one
disagreement repeated since it was cut.

---

## 1. Why a DISPOSITION and not a copy-back

The tool's remedy is written into its own message: *"Copy them into the MODIFIED
block (a MODIFIED requirement replaces the whole block, so archive refuses to
drop them)."* Taking that remedy is what this packet refuses, and the refusal is
the convener's rather than this lane's.

**Copying the two scenarios in today makes a ratified packet restate a
requirement it does not govern.** `extend-merge-master-envelope-to-floor-bot-lanes`
narrows ONE clause of *Bounded autonomous surface* and says so in its own block:
*"Narrowed by `extend-merge-master-envelope-to-floor-bot-lanes` (2026-09-07) in
ONE clause and no other"*. `relocate-review-authority-floor` amends the
rationale and adds one scenario, and says so too. Neither touched the
human-authorship bar. The two scenarios canon now carries —
*"A human-authored pull request is never approved by tier 1 alone"* and *"A
gate-integrity path is never approved autonomously"* — are
`add-regular-pr-council-clearance`'s work, and that packet's BREAKING change is
what they state. Pasting them into a sibling's block would put text nobody
reviewed in that context into two ratified packets on the same afternoon their
author archived.

**The convener ruled the order instead, and the ruling is the citation.** Brett
Heap, 2026-09-11, verbatim *"This change first"* — codexFactory
`hermes/domain/review-councils/records/2026-09-11-gate-rules-provenance-axis-declaration.md:656-659`,
§ 8. The siblings re-derive against the archived canon before their own
archives; the finding is carried until they do; each re-derivation retires its
entry here.

**And the finding is not spurious.** Promoted `doc-health` § *Currency of an
active change's MODIFIED requirement blocks* (`:1597`) is the requirement this
check implements, and it holds that the family reads every active change
*"regardless of its lifecycle standing"* precisely because *"a finding against a
draft costs its author one line — which is the cheapest moment to pay it"*
(`:1625`). This packet does not argue with that. It records WHO owes the line
and WHEN, and accepts the finding in the meantime. That is the difference
between an exception and a suppression, and it is why the canon that makes the
finding legitimate is the canon these two entries CITE.

---

## 2. Why these two are a NEW CLASS, and why the pin's prose had to move

Until today every entry in `dispositions:` was the same thing: a change DECLARED
a retitle using the reserved
``**Merged into `<destination>` by <change-id> (<date>):**`` marker, and 1.12.0
is blind to that marker. The pin's own header said so — *"EVERY ENTRY BELOW IS
THE SAME DISAGREEMENT, five times"* — and every one of the four surviving
entries cites the marker requirement in `doc-health`.

**These two are not that, and pretending they were would be the easy lie.**
Neither sibling block carries a marker. Neither should: a marker declares a
deletion its author made, and these authors made none. Canon moved underneath
them. The honest consequences are all taken here rather than avoided:

* the pin's header block is rewritten into **two declared classes**, so the
  count sentence is replaced by a statement that survives the next entry;
* the two new entries cite `doc-health`'s **currency** requirement — the one
  that defines the check that reported them — rather than the **marker**
  requirement, which has nothing to do with them;
* the test asserts the marker citation **if and only if** the entry is of the
  marker-blindness class, so a future canon-moved entry that reached for a
  marker citation to satisfy a shared assertion would FAIL rather than pass.

That last one is the point of doing this now. A shared `doc-health/spec.md`
literal would have let the second class inherit the first class's citation
without ever pointing at anything true.

---

## 3. The spec-delta decision

**Criterion.** This packet writes a spec delta if and only if the rule it
exercises is not already stated. Four properties are needed: a disposition is
scoped to one repository; an entry naming another repository is out of scope and
can never be stale here; a consumer's entry REFUSES when its finding stops
occurring; and an entry carries a citation and exactly one of two authority
spellings.

**Reading.** All four are stated by the promoted requirement *"A dispositioned
finding is cited, upgrade-coupled, and refused when stale"*
(`openspec/specs/neutral-product-pin/spec.md:577`) and by the verifier's own
`DISPOSITION_AUTHORITY` tuple, and its scenario *"A dispositioned finding stops
occurring"* is a description of the retirement half written before that half had
ever fired across a repository boundary.

**THE FIRST FIRING OF A CLAUSE IS NOT AN EXTENSION OF IT.** This is the only
argument this packet could have used to justify a delta and it does not hold:
the rule says a stale entry refuses and must be deleted in a change that says
the condition is gone; this is that change; nothing about the rule needs to
change for it to be one. Writing a `## MODIFIED` block that restated text this
packet agrees with would be a delta authored to have a delta.

**Decision: no spec delta, declared rather than omitted.** `.openspec.yaml`
carries `skip_specs: true`, which 1.12.0 reads
(`dist/core/change-metadata/schema.js`), reports at INFO, and refuses
`CHANGE_SKIP_SPECS_CONFLICT` against if a `specs/` file appears beside it — so
the declaration is checked, not merely written. It is the third use of
`skip_specs` in this corpus.

---

## 4. Why the count test moves by a DELETION and two ADDITIONS

`test_the_real_pin_declares_exactly_the_five_dispositions_two_repos_carry`
exists to make the list unable to grow — or shrink — unread. **It is doing its
job**: this packet cannot touch the list without touching the test, which forces
the movement into the diff and into a human's reading. The correct response to a
test that fires for the reason it was written is to satisfy it deliberately and
say so, which is this section.

**The re-key from `item` to `(repo, item, path)` is FORCED, not cosmetic.** From
today `relocate-review-authority-floor` carries TWO entries: a declared retitle
on `repository-gate-floor/spec.md`, measured 2026-09-10 and granted by that
day's word, and a canon-moved finding on `merge-master-approval/spec.md`,
measured 2026-09-11 and granted by another. An item-keyed map has one slot for
both and would have asserted one entry's measurement and authority against the
other — silently, and in the direction of passing. The triple is exactly the
precision the matcher has; the map now has it too.

**The authority read is a CORRECTION, and the spelling is deliberately left
unpinned.** `pinned_dispositions` has accepted `ratified_by:` OR `recorded_by:`
since the bump, and `DISPOSITION_AUTHORITY` names both; the test indexed
`entry["ratified_by"]` and would have raised `KeyError` on the first
`recorded_by:` entry — it could not express a grammar the shipped verifier has
always had. It now reads whichever spelling stands and asserts that EXACTLY ONE
does, a property nothing checked before. What it does NOT do is pin WHICH
spelling each entry uses, and that is a decision rather than an omission: an
entry a convener later ratifies moves from the weaker authority to the stronger,
and that upgrade must cost the one key name in the pin and nothing else. A map
of spellings here would make a governed upgrade require a test edit to perform.
**This packet is itself the worked example** — it was authored with
`recorded_by:` and flipped to `ratified_by:` on Brett's word, and the flip
touched the pin and no test.

---

## 5. Why the 2026-09-05 comment block is left UNEDITED

That block says *"THE SECOND PAIR, IN A SECOND REPOSITORY"* and describes two
entries, one of which this packet deletes. Editing it to say "one" would be the
obvious repair and it is refused, on the precedent's own rule: it is a DATED
RECORD of what arrived on 2026-09-05 and it stays true of that day. A later
count belongs in a later paragraph. So a dated **RETIRED 2026-09-11** note is
added directly beneath it, naming the archive, quoting the retired entry's own
prediction, giving the measured refusal, and pointing at the two new entries at
the bottom of the list. A reader who lands on the 2026-09-05 paragraph reaches
the correction in the next sentence rather than being misled by it.

The prose that IS edited is prose that makes a PRESENT claim: the rollback
note's count of entries, and the header's "same disagreement, five times". A pin
whose prose describes a list it no longer has is a pin nobody can review.

---

## 6. What this packet deliberately does not do

* **It does not move `scripts/validate-openspec-cli-pin.py`.** Every property it
  uses already exists, is already tested, and both clauses of the disposition
  rule are already implemented. The retirement half firing for the first time is
  a fact about the corpus, not about the code.
* **It does not move the pin's version, referent, lockfile or rollback.** Only
  `dispositions:` and the prose that describes it.
* **It does not edit any surviving disposition entry.** The
  `relocate-review-authority-floor / repository-gate-floor/spec.md` entry is
  left byte-identical even though the change it names now carries a second
  entry; the NEW entry names the old one, rather than the old one being
  rewritten to name the new.
* **It does not touch codexFactory.** Every measurement was issued from an
  openxFactory checkout with `--repo` over a READ-ONLY local clone whose
  worktrees are detached and pushed nowhere. The pin advance is lane
  `codeXfactory-1`'s act on Brett's 2026-09-12 word, sequenced after that lane's
  #435 and #433, in codexFactory's own pull request.
* **It does not claim the sibling packets' work.** Neither re-derivation is
  ticked, drafted or begun here. The entries carry the finding; the packets pay
  the line.
* **It does not claim a ratification it was not given.** Brett's word ratifies
  the two ENTRIES as encoded. `proposal.md`, `design.md` and `tasks.md` carry
  `Status: draft` and the pull request is DRAFT.
