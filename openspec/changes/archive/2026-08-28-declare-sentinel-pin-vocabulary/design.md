# Design: declare-sentinel-pin-vocabulary

Four decisions carry this packet, and each one was taken against a measurement
rather than against a preference. § 1 is why an untrue pin is a different defect
from an unreachable one, which is what earns the packet its own requirements
rather than a clause in an existing one. § 2 is why the legal non-pin is a fifth
outcome instead of a pass. § 3 is where the vocabulary lives and why the delta
refuses to name the path. § 4 is why the committed spellings are grandfathered
and what that costs.

## 1. An untrue pin and an unreachable pin are different defects

The promoted canon this packet sits beside is entirely about a pin that STOPPED
being resolvable. Read the shape of it: the pin was written truthfully, the
object went away, the class declares the loss, retention is the repair where the
object survives, a superseding record is the resolution where it does not. Every
mechanism in it assumes the artifact's claim was once checkable.

A dirty-tree stamp breaks that assumption at the root. The commit is reachable —
it is `main`'s tip, usually — and the tree it names is not the tree the generator
read. Nothing is missing, so:

- **Reachability answers PASS.** `merge-base --is-ancestor` returns 0. The
  strongest verification this repository has says the artifact is fine.
- **Retention has nothing to retain.** The object is already reachable.
- **A superseding record has nothing to supersede.** The loss it would name did
  not happen.
- **Re-derivation is not available either**, because the content that was
  recorded exists in no commit to re-derive from.

So the defect is not merely unrepaired; it is unreachable by every instrument the
pin canon carries, and it is invisible to the one verification that would have
caught it. That is why the obligation states itself BEFORE the reachability rule
rather than inside it: the reachability rule governs which commit a pin may name,
and this one governs whether a commit may be named at all.

**THE ORDERING IS ALSO WHY THE DELTA RESTATES NEITHER PROMOTED REQUIREMENT.** A
`MODIFIED` block over "A committed derivation pin stays resolvable" would have
been the tempting shape — widen it to say "and only where the commit describes
the content". It is refused for the same reason the family-enumeration hazard is
refused: a promoted requirement that a later change replaces wholesale is a
requirement a later change can truncate, and the two rules are separable in fact.
An artifact can satisfy either and violate the other, and a reader needs to be
able to tell which one failed.

## 2. The legal non-pin is a fifth outcome, not a pass

The verification today has four ways to end up: reachable, orphaned, lost,
uncovered — plus an inconclusive skip when the clone cannot answer. A sentinel
belongs to none of them, and each near-miss costs something specific.

| Folding it into | What breaks |
| --- | --- |
| reachable / PASS | Claims a resolution nobody performed; the report says a commit was found when none was named |
| orphaned | Offers retention as the repair for a commit that does not exist to retain |
| lost | Puts a row in `KNOWN_LOSSES` describing an object nobody lost, and holds `fully_verified` open on an obligation nobody owes |
| uncovered | Sends the next reader to widen a declaration that is already correct — the key IS declared, the member IS in good standing |
| skipped / inconclusive | Says the clone could not answer, when the clone answered perfectly and the answer is "no commit here" |

So it is its own outcome, and the report says so in its own words. **It does NOT
hold full verification open**, and that is the deliberate part: an artifact
carrying an honest sentinel is CONFORMING. It did what the generator obligation
asks. Treating it as an open item would punish exactly the behaviour this packet
exists to require, which is the fastest way to teach the next generator author to
stamp `HEAD` and stay quiet.

**THE UNDECLARED BRANCH FAILS, AND FAILS WITHOUT GUESSING.** A value that is
neither a commit nor a declared member is reported as a defect with the artifact,
the key and the value. The verification does not try to tell "a generator invented
a spelling" from "somebody typed a truncated sha" from "a member drifted by one
character", because the remedy is identical for all three and because a near-miss
match is precisely the condition under which every consumer guarding on an exact
string already fails. Guessing would make the check agree with a consumer that
crashes.

## 3. Where the vocabulary lives, and why canon does not say

Q1 of `govern-derived-pin-reachability` ruled the registry-module home for the
declared pin class — beside `families.py`, on the derived-not-restated shape
`add-family-enumeration-check` established — and pointedly did NOT put the path in
the delta. This packet copies both halves of that ruling.

**The home follows from what the vocabulary is FOR.** It is read by the
verification, by every generator that stamps a pin, and by every consumer that
guards on a pin value. A contract artifact under `contracts/` would be
schema-checkable and would add a schema plus a release-bundle question this packet
has measured as not owed. A table in the promoted spec would be readable and would
be prose a check has to parse — and worse, would make the vocabulary a thing that
changes only by OpenSpec change, which is wrong for a list whose whole job is to
absorb a new condition the day a generator meets one. A registry module beside the
class it qualifies is exact, importable by the generators, and checkable against
the corpus by the same machinery that already checks the class.

**The delta says "the same place and the same form as the declared pin class" and
stops.** Whether realization adds a module or adds constants inside `pin_class.py`
is genuinely open and either satisfies the obligation. Naming a path in canon
would mean a `MODIFIED` block the next time the module moves, which is the cost
that ruling already priced.

**THE CHECK RUNS IN BOTH DIRECTIONS, AND THE SECOND DIRECTION IS THE UNOBVIOUS
ONE.** Corpus-against-declaration catches a generator inventing a spelling — the
failure everybody expects. Declaration-against-corpus catches a vocabulary that
accumulates entries nobody writes, which is a slower and more corrosive failure: a
reader looks up a value, finds a plausible condition, and believes something about
an artifact that no generator has ever produced. The pin class already carries
this shape in `vanished_members()` and `arrived_future_members()`, and reporting a
stale member is deliberately not the same as deleting it — a condition may be
declared before its generator lands, exactly as the class declares FUTURE members.

**THE SCOPE IS THE PIN CLASS'S OWN INVENTORY, STATED RATHER THAN INFERRED.** Same
files, same keys, same serializations, same declared exclusions with their same
stated reasons — prose included, because a governance document narrating a
dirty-tree derivation quotes a sentinel exactly as it quotes a commit name, and
the trade that markdown is unswept is one the class already states. A vocabulary
checked over a different set than the pins it qualifies would report gaps the pin
class does not have and miss gaps it does, and nobody reading either report could
tell which corpus each answered for.

## 4. Grandfathering, and what it costs

Seven committed values become vocabulary members as they stand. The alternative —
normalize the spellings and edit the manifests — is refused twice over.

**It is refused by this capability's own rule.** All seven sit inside archived
packets. A content edit to captured material after capture is a finding, and a
value edited to a spelling the run did not write makes the artifact state
something that did not happen. This is the identical ordering that makes retention
rather than re-pinning the repair for an orphaned record pin: when the record
cannot move, the thing that accommodates it is the declaration.

**And it is refused because those seven are the argument.** Nobody designed the
sentinel practice. Seven times, an author confronted with content no commit held
wrote down which condition applied instead of stamping a commit that would have
resolved and lied. That is the evidence the rule is right, and it is why the delta
says so in canon rather than leaving it as packet trivia.

**THE COST IS REAL AND THE DELTA CARRIES THE MITIGATION.** The vocabulary ends up
with more than one spelling per condition — `"uncommitted-worktree"` from the
corpus and `"uncommitted"` from the generator, both circling the same territory
while naming different conditions (Q1). A list of equal members would be drift
wearing a declaration's clothes. So every member states its condition, and every
condition names ONE canonical member for new output with the rest marked legacy:
legal where already committed, never written afresh. A legacy member without that
marking is indistinguishable from a second canonical spelling, which is the exact
failure being declared away.

**THE CONSUMER CLAUSE IS THE PART THAT PAYS FOR ITSELF IMMEDIATELY.** Requiring
that a guard consult the declaration rather than a literal is not tidiness — it is
the fix for a measured latent raise. Three comparisons in `proposal-support.py`
recognize one spelling of one condition; the sixth committed manifest that reaches
them raises `SupportError` instead of returning findings. Whether that repair
rides this packet's realization is Q4; that the delta obliges it is not in
question.
