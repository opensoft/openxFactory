# Design: disposition-codexfactory-floor-relocation-retitle

Status: ratified
Ratified by: disposition-codexfactory-floor-relocation-retitle — 2026-09-10, Brett Heap, "go A, ratify the disposition entry as encoded" (record `review/ratification-2026-09-10.md`)
Date: 2026-09-10
Kind: design

Five decisions, each recorded because a reader six months from now will ask why
this packet is as small as it is — and one of them is a decision the precedent
could not take.

---

## 1. Why a DISPOSITION and not a copy-back

The tool's remedy is written into its own message: *"Copy them into the MODIFIED
block (a MODIFIED requirement replaces the whole block, so archive refuses to
drop them)."* Taking that remedy is what this packet refuses.

**Copying the scenario back reinstates the gate the relocation replaced.**
Canon (promoted by codexFactory PR #318's archive) carries *"The human gate is
unchanged"*. `relocate-review-authority-floor`'s `## MODIFIED` block carries
*"The human gate is whatever the document's path routes to"* instead, and the
paragraph above it states the rule the retitle serves: the review routing that
governs the floor document "SHALL be whatever the repository's own rules say for
THE PATH THE DOCUMENT OCCUPIES, and it SHALL apply to the automated lane's pull
request exactly as it applies to a human's". A block carrying BOTH titles would
assert that the gate is unchanged and that it is whatever the path routes to, in
one requirement, at once. That is not a repair; it is a contradiction with a
green gate.

**The relocation is a landed fact, not a proposal.** The floor document moved
from `scripts/merge_master/openxfactory-review-authority-floor.yaml` to
`floor/openxfactory-review-authority-floor.yaml` in codexFactory #297
(`8165d1f3`, 2026-09-09), the openxFactory side landed as #823 and #829, and the
re-pin lane has been reading the new path in steady state since. Restoring a
scenario that says the gate is unchanged would describe an estate that no longer
exists.

**Canon already holds that this shape is a retitle.** Promoted `doc-health`
§ *Currency of an active change's MODIFIED requirement blocks* says a block that
adds a scenario title canon does not carry "is a retitle, whatever the marker
calls it" (`openspec/specs/doc-health/spec.md:1773`) and names `Merged into` as
the author's instrument for it, writing the form out at `:1793`. So what remains
is not a corpus defect: it is a pinned tool that cannot read a marker this
corpus ratified.

---

## 2. Why the marker is a CITATION here and not a PRECONDITION

A sibling lane added the reserved `Merged into` marker to the relocate block in
codexFactory — PR #339, LANDED on main `9b1b0a21` at 2026-09-10T14:33:55Z. This
packet **cites** that marker and never **waited** for it, and the distinction is
deliberate — and now measured, because the marker landed mid-authoring and gave
the argument a falsification test it passed.

The marker is `doc-health`'s instrument, not the pinned CLI's. 1.12.0 is blind
to it — that blindness is the entire reason `dispositions:` exists — so adding
the marker changes nothing about the finding, the run, or the exit code. What it
changes is where a HUMAN reading that block learns that the omission is
declared. The disposition's `why:` states the retitle; the marker states it in
the corpus's own grammar, in the block itself, at the place a reviewer looks.

**MEASURED, NOT ARGUED.** The marker landed while this packet was being
authored, so the claim was re-run rather than left as reasoning: over #318's head
merged with the marker-carrying main (`89ee5e84`), the pinned CLI's message is
**BYTE-IDENTICAL** to the pre-marker run on `32743fb7` — requirement title,
scenario title and remedy sentence all — and the pre-edit pin still exits 1 on
that tree with the finding UNDISPOSITIONED. The marker changed the corpus and
changed nothing about the tool, which is the whole premise of `dispositions:`
demonstrated on a live pair of trees.

Sequencing this packet behind that pull request would therefore have bought
nothing and cost the thing that matters: codexFactory's `validate` stays red on
#318's tree until this entry exists, and #318 is an ARCHIVE — the act that
promoted the requirement in the first place. The honest shape is to land the
acceptance and cite the marker at its path, which is what the entry does.

---

## 3. The spec-delta decision, and why the precedent's reasoning does NOT carry

**Criterion.** This packet writes a spec delta if and only if the rule it
exercises is not already stated. Three properties are needed: a disposition is
scoped to one repository; an entry naming another repository is out of scope and
can never be stale here; a consumer's entry refuses when the consumer's own
change archives.

**Reading.** All three are stated by
*"A dispositioned finding is cited, upgrade-coupled, and refused when stale"* —
and, unlike on 2026-09-05, that requirement is now **PROMOTED**, at
`openspec/specs/neutral-product-pin/spec.md:577`, `bump-openspec-cli-pin-to-1.12`
having archived on 2026-09-09. Its scenario *"A consuming repository runs the
same pin over its own tree"* (`:658`) is a description of this act written
before this act existed.

**THE PRECEDENT'S SECOND ARGUMENT IS GONE AND IS NOT REUSED.**
`disposition-codexfactory-declared-renames` § 4 refused a `## MODIFIED` block on
ORDERING: the requirement was not in `openspec/specs/`, so a MODIFIED block
would have targeted text that was not canon. That objection has expired. A
MODIFIED block is now REACHABLE, and this packet still does not write one — for
the only reason that survives scrutiny: **there is nothing in the rule to
modify.** The rule says a disposition is per-repository, cited, authority-named
and stale-refused; this entry is all four; the rule needs APPLYING. Writing a
MODIFIED block that restated text this packet agrees with would be a delta
authored to have a delta.

**Decision: no spec delta, declared rather than omitted.** `.openspec.yaml`
carries `skip_specs: true`. 1.12.0 reads the key
(`dist/core/change-metadata/schema.js`), reports it at INFO in validation, and
refuses `CHANGE_SKIP_SPECS_CONFLICT` if a `specs/` file appears beside it — so
the declaration is checked, not merely written. It is the second use of
`skip_specs` in this corpus, the first being the precedent.

**The alternatives, and why each was refused.**

* `## ADDED Requirements` restating the scoping rule — refused. A second copy of
  a promoted requirement, free to drift from the first, to make a point already
  made.
* `## MODIFIED Requirements` on that requirement — refused on SUBSTANCE now
  rather than on ordering. See above.
* Waiting for a rule change that would make this entry unnecessary
  (`Fission-AI/OpenSpec#1793`) — refused. Filed is not fixed, and
  codexFactory's gate is red today.

---

## 4. Why the count test moves 4 -> 5 and the citation test is TIGHTENED

`test_the_real_pin_declares_exactly_the_four_dispositions_two_repos_carry`
exists to make the list unable to grow unread. **It is doing its job right
now**: this packet cannot add an entry without touching it, which forces the
growth into the diff and into a human's reading. The correct response to a test
that fires for the reason it was written is to satisfy it deliberately and say
so, which is this paragraph. The per-repository SPLIT the precedent tightened it
into is KEPT — the assertion still names which item belongs to which repository,
in order.

`test_every_real_disposition_cites_canon_and_names_who_granted_it` needed more
than a rename, and the difference matters. It asserted, for EVERY entry, two
shared literals:

```python
assert any("openspec-1.12-readiness-2026-09-05.md" in citation for citation in entry["cited_to"])
assert entry["ratified_by"].startswith("Brett Heap, 2026-09-05")
```

Both were true of four entries measured by one sweep and granted on one day.
Neither is true of an entry measured on 2026-09-10 by its own packet's evidence
and granted by a different word. **The weak repair is to loosen both** — drop
the measurement literal, shorten the date to `"Brett Heap, "` — and a loosened
assertion never fires again. **The repair taken is to make them PER-ITEM**: a
map from item to the measurement file that entry rests on, and a map from item
to the authority date its word carries. Every entry must still cite the
measurement it rests on and name the human who granted it; a sixth entry fires
the test, which is what the test is for.

---

## 5. What this packet deliberately does not do

* **It does not move `scripts/validate-openspec-cli-pin.py`.** Every property it
  uses already exists, is already tested, and was already proven across this
  exact repository boundary by the precedent.
* **It does not move the pin's version, referent, lockfile or rollback.** Only
  `dispositions:` and the header prose that describes it.
* **It does not edit any existing disposition entry**, and it leaves the
  2026-09-05 comment block above the first codexFactory pair exactly as that
  change wrote it. That comment is a dated record of what arrived that day and
  it stays true of those two entries; a later count belongs in a later
  paragraph, which is where it is.
* **It does not touch codexFactory.** The `Merged into` marker (PR #339, landed)
  and the declared pin advance are codexFactory's own acts, in codexFactory's
  own pull requests. Every measurement run was issued from an openxFactory
  checkout with `--repo` over a READ-ONLY clone — including the merged tree,
  which is a LOCAL clone of that clone merged with `origin/main` and pushed
  nowhere — which is how a consuming tree is measured without writing to it.
* **It does not tick any other packet's task box.** In particular it ticks
  nothing in `relocate-review-authority-floor-mirror` or
  `mirror-floor-regeneration-automation`, whose boxes are theirs.
