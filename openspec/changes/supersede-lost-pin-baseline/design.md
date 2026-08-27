# Design: supersede-lost-pin-baseline

Four decisions carry this change: where the requirement lands, what "discharge"
means mechanically, where the record lives, and why the record says more than
"this is gone".

## 1. Where the requirement lands — `doc-health`, one ADDED requirement

Two capabilities meet on this pin and the split between them is already drawn.
`ideation-cross-reference` owns the PIN OBLIGATION: a committed pin stays
resolvable, an orphaned pin on an immutable record is repaired by retention, and
where the object is unrecoverable the resolution is a superseding record plus a
disposition. `doc-health` owns the VERIFICATION: what the suite checks, what it
reports, and what it calls fully verified.

The gap this change closes is on the verification side of that line. The pin
obligation says the act is owed; it does not say what the verification does once
the act lands, and it cannot without reaching into a capability it does not own.
Meanwhile the verification had exactly one route from "carries a permanently lost
pin" to "fully verified", and it ran through deleting the declaration. So the
requirement is ADDED to `doc-health`, and the pin obligation's requirement is
neither restated nor modified.

That also avoids a hazard rather than managing it. AS AUTHORED: the pin
obligation's requirements were still in an ACTIVE change
(`govern-derived-pin-reachability`) rather than promoted, so a `MODIFIED` block
over one would have been a delta against text canon did not yet carry, while the
parallel session archiving that packet owned its surface. **AND IT LANDED WHILE
THIS PACKET STOOD OPEN, 2026-08-27**: that packet archived as pull request #428
and its requirements are now promoted — "A committed derivation pin stays
resolvable" and "An orphaned pin on an immutable record is repaired by
retention, never by editing the record" in `ideation-cross-reference`,
"Derivation-pin reachability is verified across a declared artifact class" in
`doc-health`. The conclusion is unchanged and the reason for it is now stronger
rather than weaker: those requirements say what the repair route is and what the
verification covers, and NEITHER says what the verification does once the owed
act lands. This delta adds that, in the capability that owns the verification,
with no `MODIFIED` block over promoted text and no restatement of it. Main was
merged into this branch after that archive, so the delta is authored against
canon as promoted rather than as proposed.

## 2. What discharge means mechanically — a citation that is READ

The whole mechanism is four lines of state and one function.

```python
superseding_record: tuple[str, ...] = ()   # where the record stands
discharged: str = ""                       # what it established
```

```python
def discharging_record(repo, rev, loss, *, paths=None) -> str | None
```

It resolves the globs against committed paths at the revision under test, reads
the file, and returns it only if the text NAMES the pin. Three failure modes
therefore behave identically to no citation at all: a record nobody committed, a
record deleted after the row cited it, and a stub at the right path that never
mentions the lost object. This is the same discipline the loss declaration
already lives under — the row's `measured` field is re-measured by test rather
than believed — applied to the row's new field.

`fully_verified` then consults `lost_awaiting_record` instead of `lost`. **This
completes the property rather than redefining it**; its docstring already asked
for "no declared loss awaiting its superseding record", which is the question
`lost` could not answer and the new property can.

**WHY THE VERDICT STAYS `LOST`.** Two questions live in one report and only one
of them has changed. "Is this pin reachable?" is answered LOST for ever, with
the measurement, in every run. "Is an obligation outstanding?" is answered by
whether the record exists. Introducing a fourth verdict for "lost but
discharged" would encode the second answer in the field that carries the first,
and a reader scanning for losses would stop finding this one. So the marker
stays `[LOST]`, the `how` string gains a `DISCHARGED:` clause naming the record,
and `summary()` reports the split so both facts are visible at a glance.

**WHY DELETION FAILS LOUDLY.** Remove the row and `known_loss()` returns None,
the site falls through to the ORPHAN branch, and the run FAILS with a repair
route it cannot follow. That is not a punishment; it is the report the repository
would have carried all along if the loss had never been declared, and it means
the declaration cannot be traded for a clean report.

## 3. Where the record lives — this packet, cited by a glob pair

The record cannot live in the archived packet it supersedes: that packet is
closed, and reaching into an archive is the act supersession exists to avoid. It
does not belong in `health/`, which holds machine-generated lane records. So it
lives in the packet that issues it, at
`evidence/pin-loss-supersession.yaml`, and the citation is the live-plus-archive
glob pair every hermes evidence member is already declared with:

```text
openspec/changes/supersede-lost-pin-baseline/evidence/pin-loss-supersession.yaml
openspec/changes/archive/*-supersede-lost-pin-baseline/evidence/pin-loss-supersession.yaml
```

**The record is a DECLARED non-member of the pin class**, with the reason stated
in the declaration: its subject is a pin, so every pin-shaped value in it cites
another artifact's derivation claim and none is its own. The module's own
coverage test names exactly two conforming options for a pin-shaped value in a
swept root — declare a member, or declare a non-member with a reason — and this
takes the second. The route not taken is worth naming because it was easy:
choosing a key the sweep vocabulary does not know would have hidden the file
with no declaration at all, which is the silent-coverage defect
`us3_baseline_commit` proved on this very pin.

## 4. Why the record says more than "this is gone"

A supersession that only admitted the loss would be honest and nearly useless:
the archived record's readers would be left to guess which of its claims survive.
The record therefore states three things the measurement supports.

**The cause, so the class of defect is legible.** Every commit of the landed
branch shares one committer timestamp while author dates spread over the previous
day — one rebase, rewriting the whole branch. The record was written before it and
carried through it unchanged, so it kept naming its pre-rebase parent. Nobody
skipped a retention ref: the namespace was ruled six weeks later.

**The surviving state, identified by measurement.** The parent of the commit that
ADDED the record is the US3 checkpoint by construction, it is an ancestor of
`main`, and all three differential counts the record states about its baseline
agree when re-measured at both commits. The record labels this CORROBORATION, not
recovery — the object is gone, so tree equality is unprovable, and any one count
disagreeing would have falsified the identification.

**The standing, split three ways.** RETAINED: every gate verdict, which is a
claim about canonical content at a reachable checkpoint — the record's own
argument, quoted from its note field. LOST: reconstruction of the tree as NAMED,
and the three differentials now standing on this record's measurement rather than
on the pin. NEVER CHECKABLE AT ANY COMMIT: the two PostgreSQL digests, which
appear in no other committed artifact and are reproduced by no committed
generator — recorded so a later reader does not blame the loss for a gap in the
evidence contract.
