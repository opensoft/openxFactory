# Design: retire-codexfactory-sibling-currency-dispositions

Status: ratified
Ratified by: retire-codexfactory-sibling-currency-dispositions — 2026-10-09, Brett Heap, "Ratify + land when green (Recommended)" (2026-10-09T21:00:16.594Z, first-hand, multiple choice, given over head ed0c67adde1c35bd1b1c1b6472246957f9263a7f; bare as to this text, so RATIFIED AS DRAFTED with OQ-1 to OQ-4 at their § 7 defaults, flagged; its "land when green" component is the landing word, and the merge is not covered by this header; record `review/ratification-2026-10-09.md`)
Date: 2026-10-09
Kind: design

Seven sections. Sections 1 to 6 follow the template,
`disposition-codexfactory-regular-pr-council-clearance-archive`. The one new
decision is in § 1: this is the first packet in this corpus to delete a
disposition BEFORE its finding stops occurring. Section 7 lists the open
questions, each with the default a bare ratification lands it at.

---

## 1. Why the deletion goes AHEAD of the re-derivations

Both entries carry the same `retires_when:` shape. The sibling re-derives its
block, codexFactory's `--all` REFUSES `pin-disposition-stale`, and the entry is
deleted. That order assumed one thing that does not hold: that codexFactory's
tree and this file move independently, so that a re-derivation could land
first and be refused on its own.

**They do not move independently.** codexFactory reads this file at the
openxFactory commit its own `stack.yaml` declares, and its `validate` checks
openxFactory out there (`contracts/manifest.yaml`, row `openspec-cli-pin`,
*"CHECK OUT, NEVER COPY"*). So a re-derivation in codexFactory is read against
whichever pin codexFactory already declares. Measured over codexFactory `main`
`33b916c1` (evidence §§ 2–5):

* re-derived blocks, pin with the entries: **exit 2**, both stale;
* re-derived blocks, pin without them: **exit 0**, 2 applied;
* blocks as they are, pin without the entries: **exit 1**, both UNDISPOSITIONED;
* blocks as they are, pin with the entries: **exit 0**, 4 applied.

**Every partial order is red on codexFactory.** A re-derivation landed alone
reads row one. A pin advance past this deletion landed alone reads row three.
The only green transition is from row four to row two in ONE codexFactory
commit, and that commit can exist only if the deletion already exists on
openxFactory `main`. So the deletion is published first.

**This is not a bypass of the stale refusal, and the reason is the refusal's
own.** Promoted `neutral-product-pin` says the moment a disposition goes stale
*"is precisely the moment a human should re-examine it"*. The refusal is the
mechanism that forces that re-examination. Here the re-examination happens
earlier, in this packet, and is put to the convener for ratification. Under
the sequence in `proposal.md`, each entry and its finding leave codexFactory in
the same commit, so the refusal is not printed there. Nothing about either entry is
waved through unread.

**And the authority differs from the template's, which is why this packet waits
for a word.** The template deleted a STALE entry, and its ratification record
says *"A human word is what ADDS an exception; the tool is what removes one."*
No tool has refused these two entries on any tree codexFactory reads. They are
removed by a human act, so the deletion's authority is this packet's
ratification. Brett Heap's word of 2026-10-09T17:35:29Z, *"This lane drafts
it (Recommended)"*, authorizes drafting it and nothing more.

---

## 2. Why it is safe to land first

**On openxFactory's tree:** every entry deleted here is `repo: codexFactory`.
A run over openxFactory neither applies nor stales a `repo: codexFactory` entry.
That is the property `test_the_consumers_entries_are_out_of_scope_on_this_repositorys_own_tree`
pins against the real pin, and `tasks.md` 4.1 measures it on this branch with
the gate's literal invocation.

**On codexFactory's tree:** codexFactory keeps reading the commit it declares
(`0992369a` today, `93d13d6c` after #549's first advance). Neither commit
contains this packet. So landing it moves nothing codexFactory reads until
codexFactory advances past it, and that advance is bound by the constraint in
`proposal.md` § Impact.

---

## 3. The spec-delta decision

**Criterion.** This packet writes a spec delta if and only if the rule it
applies is not already stated.

**Reading.** Promoted `neutral-product-pin`
(`openspec/specs/neutral-product-pin/spec.md:639`) already states each property
this packet relies on:

* a disposition is scoped to one repository;
* an entry for another repository is neither applied nor stale on this tree;
* a finding no disposition covers FAILS the run, and the remedy offered is to
  fix it or to disposition it;
* an entry's remedy is an edit to the pin file.

Nothing in canon says an entry may be removed ONLY once its finding stops. The
rule says a stale entry MUST go, and is silent on an entry removed earlier.
That silence is not a gap. Removing an entry early has exactly the consequence
the "uncovered finding" scenario already describes, on any tree where the
finding still occurs. The sequence is what keeps that tree from being
codexFactory `main`.

**Decision: no spec delta, declared rather than omitted.** `.openspec.yaml`
carries `skip_specs: true`, which the pinned 1.12.0 reads, reports at INFO, and
refuses with `CHANGE_SKIP_SPECS_CONFLICT` if a `specs/` file appears beside it.

---

## 4. Why the tests move 5 -> 3, and why three test files and not one

`test_the_real_pin_declares_exactly_the_five_dispositions_two_repos_carry`
exists to make the list unable to change unread. **It fires here for the reason
it was written**: this is its fifth firing, and the first by deletion alone.
It is renamed `..._three_...`, and its docstring reads the movement. Its
per-repository split is kept.

**In the same file,** the two triples leave `DISPOSITION_MEASUREMENT`,
`DISPOSITION_CLASS` and `DISPOSITION_AUTHORITY_PREFIX`. Their key sets must
equal the pin's entries, so a deleted entry must be deleted there too. The
triple keying added by the template stays: no change carries two entries
today, but the next one that does needs no re-key. `CANON_MOVED` is OQ-1.

**Two more test files move, and both read the LIVE pin rather than a fixture:**

* `tests/doc-health/test_pin_shape_adapter.py`,
  `test_the_real_record_still_resolves_at_both_the_guard_and_the_adapter`,
  asserts the live record's entry count at both the guard and the adapter. The
  count is the live record's and moves with it: 5 -> 3. The property the test
  exists for, that every entry the guard admits the adapter admits, is
  unchanged.
* `tests/pin_registrations/test_pin_registration_sweep.py`,
  `test_the_live_pin_registration_citations_still_resolve`, asserts a FLOOR on
  the number of the live pin's in-tree citations that resolve to an active
  packet. Measured with the checker's own reader: **5 such referents in 4
  packets at `9a272c6d`, and 3 in 3 packets on this branch.** The two deleted
  entries carried the only two citations into
  `disposition-codexfactory-regular-pr-council-clearance-archive`, so the old
  floor of 4 would red. A deletion of citing entries is not an archive of a
  cited packet, so this is the floor following the corpus, not the relocation
  that test exists to survive. Its docstring says so, and an unrelated
  docstring in the same file that counted "four actively-cited packets" is
  reworded so it does not go false.

---

## 5. What prose moves and what is kept

The template's rule is that **a dated record stays true of its day, and a later
count belongs in a later paragraph**. Applied here:

* **Kept:** the header paragraph *"AND THEN A FOURTH AND FIFTH TIME …"*, dated
  2026-09-11. It records how the two entries arrived, and that stays true. A
  NEW dated 2026-10-09 paragraph follows it. It records the deletion, the
  measured order, Brett's word, and the evidence path, so a reader of the old
  paragraph reaches the correction in the next one.
* **Deleted:** the comment block *"codexFactory, added 2026-09-11 by …"* that
  sat directly above the two entries. It is not a dated record of the list; it
  is a preface to two entries, and with the entries gone it would preface the
  end of the file. Its text survives at openxFactory `9a272c6d` and in the
  template's packet, which quotes its substance.
* **Edited, because they make a PRESENT claim:** the rollback note's count, and
  the block above `dispositions:`. That block keeps both declared classes and
  says the second now has no entry. The class declaration stays so that the
  next finding of that cause lands in a class that already says what it must
  cite.

---

## 6. What this packet deliberately does not do

* **It does not move `scripts/validate-openspec-cli-pin.py`.** Every property
  it relies on already exists and is already tested.
* **It does not move the pin's version, referent, lockfile or rollback.**
* **It does not edit any surviving entry.** The three that remain are
  byte-identical, `relocate-review-authority-floor` /
  `repository-gate-floor/spec.md` included.
* **It does not touch codexFactory.** Every codexFactory measurement was run
  from this openxFactory checkout with `--repo` over a scratch clone whose push
  URL is disabled. Nothing was committed there or pushed.
* **It does not perform or draft the re-derivations.** They are codexFactory
  acts under #549's gate G-2, each on its own owner word.
* **It does not edit the template packet.** Its `tasks.md` 6.3 stays open (OQ-2).
* **It does not narrow `tests/packet_reference/test_packet_reference.py`'s
  `CITED_ACTIVE_PACKETS`** (OQ-4).

---

## 7. Open questions

Each has a default. A bare ratification lands each question at its default and
leaves it flagged, not resolved.

| id | question | default if bare |
| --- | --- | --- |
| OQ-1 | `CANON_MOVED` has no member after this deletion. Keep the constant and its `DISPOSITION_CLASS_CITATION` row, or remove them along with the pin header's class declaration? | **Keep.** The constant is still referenced by `DISPOSITION_CLASS_CITATION`, and the pin header still declares the class. The next canon-moved entry should land in a class that already names the currency citation, not borrow the marker class's. Removing it would mean a later entry has to re-add both. |
| OQ-2 | The template's `tasks.md` 6.3: give it a dated cross-reference to this packet now, or leave it? | **Leave it untouched here.** It is another ratified packet's row. Its substance (the re-derivations) is discharged by codexFactory #549's second advance, and ticking or annotating 6.3 is that packet's own act, at that time. |
| OQ-3 | Land on ratification, or hold the landing until codexFactory's re-derived text (G-2) is drafted and put to Brett? | **Land on its own landing word, after ratification.** The coupling cost is that codexFactory cannot advance past D without the re-derivations (`proposal.md` § Impact). That advance is the next one #549 plans anyway, and holding D would only move the same coupling later. |
| OQ-4 | `tests/packet_reference/test_packet_reference.py` still lists the template in `CITED_ACTIVE_PACKETS`, a tuple named for the packets the live pin cites. Narrow it here? | **No.** The test asserts only that each listed packet still exists in the corpus, which stays true, so it does not fire. Its module docstring is dated "on the tree this suite was written against". A later tidy-up may narrow it. |

**2026-10-09: LANDED AT THEIR DEFAULTS, AND STILL FLAGGED.** Brett Heap's word
of 2026-10-09T21:00:16.594Z, *"Ratify + land when green (Recommended)"*, is
bare as to this text: it names no amendment and rules none of the four. So
each lands at the default its row states and stays flagged, not resolved:
OQ-1 keeps `CANON_MOVED`; OQ-2 leaves the template's 6.3 unedited; OQ-3 lands
on its own landing word after ratification; OQ-4 leaves `CITED_ACTIVE_PACKETS`
as it is. OQ-3's default waits for a landing word, and the same answer gives
it as its own component, *"land when green"*. The landing itself is the
coordinator's act under lane-collision Rule 6, read green on the head it
lands. Record `review/ratification-2026-10-09.md`.
