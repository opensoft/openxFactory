# Design: govern-derived-pin-reachability

Three decisions needed recording, and a fourth that is really a boundary. The
first is about how a defect that cannot be edited away gets repaired; the second
is about what "re-pinned" is allowed to mean; the third is about where a check
whose answer depends on clone depth may live. Everything else in this change is
the ordinary shape of a rule-stating packet.

## 1. The repair route for a `record` is RETENTION, not re-pinning

**Chosen. CLEARED AS AUTHORED 2026-08-27 (OD-4), and the namespace this entry
left open is now ruled (Q3) and executed (Q2).** When an artifact carrying
`status: record` holds a derivation pin no ref reaches, the pinned COMMIT is made
reachable again and the record's bytes are left exactly as captured. Retention
publishes `refs/retention/pins/<full-sha>` on the repository's own remote — one
ref per retained commit, its name COMPUTED from the pin's full forty-character
object name rather than chosen — and a local ref does not satisfy it. Where the
object is unrecoverable everywhere, the resolution is a superseding record naming
the loss plus a disposition for the standing finding.

The namespace was NOT invented at the archive to match what happened: Q3 ruled
the namespace and Q2's execution used it, and this repository's two instances are
the worked example — `refs/retention/pins/da9bf3b7…` and
`refs/retention/pins/f13a3b60…`, published on `origin` on 2026-08-27 and verified
by `ls-remote`, each at the commit its name states, with both records still
carrying their original pins UNEDITED. The design argument for deriving the name
from the pin rather than declaring it per artifact is the one this section's last
paragraph already made about measurement: a repairer who computes the ref name
cannot get it wrong, and a reader resolving a record's pin computes the same name
without a second lookup that could drift from it. RETENTION LIFETIME is
deliberately still unstated — a retained commit is retained because a committed
record names it, so the ref outlives the record, and a duration would need a rule
for what happens at its end.

This is forced rather than preferred, and the forcing is a collision between two
promoted rules. `ideation-cross-reference` persists derivation output as
IMMUTABLE evidence. `document-lifecycle` makes a content edit to a `record` after
capture a finding — it is named explicitly in `doc-health`'s lifecycle-conformance
scenario ("a content edit to a `record` doc after capture"). So the repair that
worked for the index — regenerate, re-pin, commit, which is what
`harden-ideation-readiness-check` § 3 did — is not available for the two records
this packet measured. Re-pinning a record would ALSO make it lie: the record says
what a run read, and the run read `f13a3b60`. Changing the number changes the
record's claim about history, which is the one thing a record exists not to do.

Once the record is fixed in place, only the commit can move, and "moving" a
commit means giving it a ref. That is the whole argument, and it is why this is
its own requirement rather than a clause of the reachability rule: the
reachability rule says what must be true, and for one artifact class the only
available way to make it true runs in the opposite direction from every other
repair in this repository.

**Rejected — edit the record's pin, with a disposition covering the immutability
finding.** This is the cheapest route and it is available: `doc-health`'s
contested-class machinery would take the disposition. It is refused because the
disposition would be covering the WRONG defect. A disposition says "this finding
is understood and accepted"; here it would be accepting a falsified record in
order to clear a reachability finding, and the falsification would then be
invisible while the pin looked healthy. The repository has already refused this
shape once in a different register — `harden-ideation-readiness-check`'s
`.openspec.yaml` records the refusal to fabricate approval provenance rather than
fill a required field. A record whose pin was edited to something the run never
read is the same fabrication with a different field.

**Rejected — delete the two records.** They carry `envelopes: []` and
`scored_clusters: []`, so nothing of substance would be lost, which is exactly
what makes this tempting. Refused: the reason the records are empty is itself
evidence about that lane's state on 2026-08-24, and a repository that deletes
records to clear findings has no records. It also does not generalize — the next
orphaned record will not be empty.

**Rejected — leave both, and disposition the findings as legacy.** Refused
because the recoverability window is closing. Both objects exist today in at
least one clone; a decision to defer is a decision to lose the ability to repair,
taken without saying so. If deferral IS the answer it should be taken knowing
that, which is why requirement 2 obliges a packet to MEASURE recoverability
before choosing a route rather than after.

## 2. Re-pinning is defined by REPRODUCTION, not by reachability

**Chosen. CLEARED AS AUTHORED 2026-08-27 (OD-3).** A re-pin satisfies requirement 3 only if the artifact's committed
body is reproduced at the new pin — byte-for-byte where the artifact's own
tooling defines derivation, and by a NAMED measurement where it does not.
Reachability of the new pin is necessary and nowhere near sufficient.

The reason is the forcing instance. On pull request #322 the pin was moved by
hand from `da9bf3b7` to `f13a3b60`, and at the moment of the edit `f13a3b60` was
a perfectly reachable branch tip. A reachability-only rule would have PASSED that
edit. It was still wrong: nothing established that the body listed the clusters
the corpus derives at `f13a3b60`, and the sibling packet later measured the two
revisions to disagree in the general case — the same body reproduces at
`da9bf3b7` and at `4e57009c`, and derives a different count at then-current
`main`. A pin whose body was never regenerated is a claim nobody checked, and the
only thing that distinguishes it from a claim that is false is luck.

The two-tier shape — byte-for-byte where a tool exists, a named measurement
otherwise — is deliberate. Byte-for-byte is available for the cross-reference
index (`scripts/bootstrap-ideation-cross-reference.py`, plus the strict index
validator in the per-repo preflight) and this repository already leans on it:
`harden-ideation-readiness-check` proved its own re-pin by reproducing the
committed 290-entry body at three revisions. It is NOT available for a gate
record or a traceability manifest, which no generator re-derives. Demanding
byte-for-byte universally would make the requirement unsatisfiable for four of
the eight in-scope artifacts, and a requirement nobody can satisfy is a
requirement everybody disposes.

**Rejected — reachability alone.** Cheap, checkable, and it ratifies the exact
act that caused the defect. Named here so that nobody re-proposes it as a
simplification.

**Rejected — byte-for-byte, universally, with no measurement tier.** It would be
the stronger rule if it were reachable. It is not: it silently obliges a
generator for every artifact class in the inventory, including two — the gate
records and `specs/008-.../traceability.yaml` — whose generators do not
re-derive and whose bodies are not projections of a corpus at a revision.
Building four generators is a much larger change than the rule it would serve.

**Rejected — regenerate always, drop the concept of a re-pin entirely.** The
cleanest rule to state ("never re-pin, always regenerate") and wrong on the
records: regeneration IS an edit, and § 1 has just established that a record
cannot be edited. The two decisions are coupled, and this is the coupling.

## 3. The enforcement home is the existing pin-verification surface, and adds no
check family

**Chosen. CLEARED AS AUTHORED 2026-08-27 (OD-2), the decision this packet flagged as most likely to be vetoed.** Requirement 4 lands in `doc-health` as an ADDED requirement that
extends the pin-verification obligation already promoted there
(`An unreachable pinned revision fails the proof`) from one artifact to a
declared class. It rides the readiness-proof surface and the per-repo validator
preflight — where the existing probe already runs — and it explicitly adds NO
deterministic check family, leaving the "Deterministic check families"
enumeration and its numerals untouched and unrestated.

Two independent arguments, and the first is about the check rather than about
process cost. The deterministic pass is DEFINED by the property that identical
inputs produce identical findings. A reachability probe does not have that
property: the same governance corpus, at the same revision, answers differently
in a shallow clone and a complete one, because the answer is a function of
FETCHED HISTORY rather than of the corpus the pass reads. The promoted
requirement this extends already concedes exactly that asymmetry by carrying a
truncated-clone skip branch — a deterministic family with a
"depends-on-your-clone" skip is a family in the wrong pass. This is also why the
readiness lane's own owning requirement says in as many words that it "adds no
deterministic check family": the precedent for a pin-shaped verification living
outside the families is already promoted.

The second argument is process, and it is real. At authoring,
`add-family-enumeration-check` was ACTIVE and held a `MODIFIED` block for
"Deterministic check families", moving canon from twenty families to twenty-one.
Its promoted text says what happens with more than one such block: "Where more
than one active delta restates the requirement, EACH SHALL be checked
independently against the registry, because a `MODIFIED` requirement replaces its
promoted counterpart wholesale and whichever change archives last is the one
canon keeps." A second restatement here would therefore be legal and would make
canon's family list a function of archive order — the precise hazard three
changes in three days already produced once, with all three truncations caught by
a human rather than by a check. Declining to add a family declines the whole
problem.

**RE-CHECKED 2026-08-27 AFTER THE PREMISE MOVED, AND THE CONCLUSION HELD.** The
paragraph above is kept as written because its reasoning is unchanged, but the
change it names is no longer the one holding the block:
`add-family-enumeration-check` ARCHIVED that day, promoting the twenty-one
enumeration, so canon and the registry now agree and the divergence this entry
cited is gone. **The hazard is not.** `add-modified-block-currency-check` went
active the same day, adds doc-health's TWENTY-SECOND family, and owes that same
`MODIFIED` block at its realization, restating canon's twenty-one to reach
twenty-two. A family added here would restate the same requirement beside it and
reach twenty-three, with canon's list decided by whichever archived last — and
that packet exists precisely because a `MODIFIED` block silently deletes what it
does not restate. So the volatility is the argument: an enforcement home whose
correctness depends on which change currently holds one requirement's block is
the wrong home, and this decision needs no answer to that question at all. The
delta states the argument in its durable form, about the mechanism rather than
about today's holder.

**Rejected — a twenty-second deterministic check family, `derived-pin-reachability`.**
The obvious shape, and it is what the commission anticipated. Refused on the
determinism argument first and the ordering argument second. Worth noting what
it would have cost concretely: a `MODIFIED` block restating the enumeration and
its three numerals correctly at a moment when canon says twenty and the code
registry already registers twenty-one, with the reconciliation itself in flight.

**Rejected — an index-side requirement in `ideation-cross-reference` and no
`doc-health` requirement at all.** This is nearly what the sibling's OD-1
reserved, and requirements 1 and 2 DO take the index-side obligation. But
stopping there would leave the rule unenforced, and the evidence against
stopping there is this packet's own measurement: the sibling repaired the INDEX
and both `health/` records kept their orphaned pins for a further day, unreported
by anything. A rule whose only enforcement is that someone states it produces
exactly the state `main` is in.

**Rejected — the release-inventory drift family absorbs it.** It is the closest
existing family in shape, since it already reads contract artifact BYTES and
resolves objects. Refused: its document list, its finding vocabulary and its
severity are all about a declared bundle inventory against the blobs it names,
and widening it to cover ideation evidence records would make one family answer
to two capabilities.

## 4. The class is DECLARED, not pattern-discovered

Less a decision than a boundary the inventory forced, recorded because the
alternative is what a reasonable implementer would reach for first.

A scanner that finds pin-carrying artifacts by looking for keys named
`source_revision` would have found seven of the nine pins in the inventory. It
would have missed the eighth — `ideation/cross-reference.md:9`, where the pin is
the prose line `- Source revision: \`4e57009c…\`` in a rendered projection — and
the ninth, where the pin sits INSIDE a `recipe:` prose string in a gate-action
record (`recipe: checked none · pinned none · at source_revision d09d5820…`).
It would also silently stop covering any artifact whose generator renamed its
key, and a silent loss of coverage is indistinguishable from a clean run, which
is the same defect `add-family-enumeration-check` exists to prevent one level up.

So the class is declared, and the DECLARATION is checked against what the
repository carries: an artifact recording a repo-local commit pin that no
declared member covers is reported, naming the artifact and the key. That keeps
the exactness of a declaration and the coverage of a sweep, and it puts the
failure where it belongs — on the declaration, at authoring time — rather than on
a run that quietly verified less than it claimed.

**WHERE THE DECLARATION LIVES: RULED 2026-08-27 (Q1) — a registry module beside
`scripts/doc_health/families.py`.** As authored this paragraph ended "Where the
declaration LIVES is Q1 and is deliberately not settled here"; it is settled now.
The recommendation was taken, and its argument is the one this section already
makes one level down: `add-family-enumeration-check` exists because an
enumeration that only a human re-reads is an enumeration that drifts, and its
answer was to make the registry the sole authority and check the prose against
it. A pin class faces the identical problem one layer out, so it takes the
identical shape rather than a second one. The two rejected homes are recorded
with it — a contract artifact under `contracts/` is schema-checkable but adds a
schema and, per `tasks.md` § 4.4, would change the no-bundle-owed answer; a table
in the promoted spec is readable but is prose a check must parse, which is the
defect being designed away. **The delta does NOT name the module**, deliberately:
a promoted requirement that pins an implementation path must be MODIFIED the next
time the module moves, and requirement 4's obligation is that the class is
declared and the declaration checked, not that it lives at a path.
