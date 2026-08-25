# Design: add-family-enumeration-check

Status: ratified
Ratified by: add-family-enumeration-check

The decisions this change had to take, and what each rests on. Every figure was
taken against this repository's checkout at branch point `fe34b73c`, through the
family itself rather than by inspection.

## D1 — A twenty-first family, not a checker folded into an existing one

The check could have lived inside `families.py` as a clause of an existing
family, or as a standalone `scripts/validate-*.py`. It is its own family, for
three reasons of decreasing abstraction.

**The dispositions would collide.** `health/dispositions.yaml` entries key on
`(family, repo, path)`. This family reports against
`openspec/specs/doc-health/spec.md` — the promoted spec — which is a path
`document-catalog` also reports against. Folding this class into an existing
family would let one citation buy silence for two unrelated governance
decisions, which is the argument `add-duplicate-packet-check` made for the same
reason and the shape its own tests pin.

**The remedy is its own.** This family's action line is "restate the
enumeration and its counts from `families.FAMILIES`". No existing family's
action string says anything like that, and a family carries one.

**The machinery is free.** Registration alone buys a report section, a
ranked-plan line, disposition keying, and — the one that matters here —
inclusion in the suite that gates every PR. A standalone validator would have
to be wired into CI separately and would be invisible to the report a session
actually reads.

**The irony is a feature, and it decided the question.** A twenty-first family
forces exactly the enumeration restatement it polices. A checker hidden inside
an existing family would NOT have forced it — and would therefore never have
exercised its own delta half on real text. Because it is a family, this
change's own restatement is the check's first live subject, and a wrong
restatement could not have landed. That is a better acceptance test than any
fixture, and it is only available at this architecture.

## D2 — Derive from `FAMILIES`, not `FAMILY_IDS`

`families.py`'s own docstring settles the authority question: "`FAMILIES` at the
bottom of this module is the count." It is what `run_suite` iterates, so it is
what the requirement is making a claim about.

`FAMILY_IDS` is a REPORTING list and is a strict subset today — nineteen
entries against twenty-one families. `proposal-origin` and
`staged-topic-template` run and report findings with no report section of their
own. Deriving the enumeration from that list would have made canon agree with a
list that is itself wrong, which is the failure mode of picking the convenient
authority instead of the correct one.

So the subset direction is NOT reported (it is another capability's recorded
defect, and § 5.2's box), while the phantom direction IS: a `FAMILY_IDS` entry
naming an unregistered family would render a heading nothing fills, and no
other check would notice. A test pins the two absences at exactly those two, so
a third cannot join them quietly.

## D3 — Two document sources, one comparison, and one exemption

The comparison function is written once and pointed at two kinds of statement:

- **Canon** — the promoted `doc-health` spec.
- **Every ACTIVE change delta** that restates the requirement. Archived packets
  are out of scope: their deltas are already promoted or deliberately not, they
  can no longer destroy canon, and `promotion-fidelity` and `duplicate-packet`
  are the families that read them.

**Canon is exempt from the comparison while an active delta restates the
requirement.** This is the load-bearing rule of the whole design and it is worth
being explicit about why it is not a hole:

A change that registers family N+1 does so in its own tree. Canon still says N,
because canon does not move until the change archives. Canon is not diverging
there — it is PENDING, and the delta is the statement carrying the obligation.
Without the exemption this family would fire on every legitimate family-adding
branch, including its own, and a check that reports healthy work is a check
someone disables. A fixture pins the pending case quiet, and it is the negative
that took the most thought.

Where TWO OR MORE active deltas restate the requirement — the exact situation
that produced three truncations in three days — each is checked independently.
That is not thoroughness for its own sake: `MODIFIED` replaces its promoted
counterpart wholesale, so whichever change archives last is the one canon
keeps, and a delta excused because a sibling was complete would be excused for
a promotion that never happens.

## D4 — Byte-equality of names, arithmetic of numerals

**Names** resolve to registry ids by a mechanical normalization — lowercase,
then `/` and whitespace to `-` — plus a DECLARED alias set. Nineteen of
canon's twenty names resolve mechanically. Exactly one does not: canon's
"client identity roster composition" is registered
`client-identity-composition`, without `roster`, because the family id predates
the prose.

That alias is declared rather than absorbed into a looser matcher, and the
distinction is the whole point of the family. A normalization loose enough to
bridge `roster` would also bridge a genuine mismatch — which is the class this
check exists to report. `test_every_alias_is_load_bearing` asserts each entry
still fails to normalize mechanically, so a rename that makes an alias
redundant fails by name instead of leaving a private dictionary of forgiveness
behind. A name resolving to nothing is REPORTED, never approximated.

**Numerals** are checked as a system rather than one at a time. Canon states
three: the total, the subset-of-total ("Four of the twenty"), and the remainder
("the other sixteen"). The total and the subset-of-total are compared to the
registry; the remainder is compared to total-minus-subset. So a stale total
reports once as a stale total, not also as a broken remainder — the fixtures
prove the classes separate, because a build that reported every numeral for one
root cause would bury the actual defect.

**The subset numeral itself (`Four`) is canon's own claim and is not derived.**
There is no runtime registry of which families read the lifecycle scan set. That
boundary is already pinned structurally by `test_lifecycle_scan_set.py`, which
asserts `_lifecycle_scope` appears in the source of exactly the four declared
readers. Inventing a second authority for it here would create precisely the
two-readers-disagree problem this codebase keeps paying for; verifying the
arithmetic around it is the honest scope.

**An unreadable numeral is reported, not coerced.** `word_to_int` returns None
rather than 0, so a numeral the family cannot read produces a finding that names
the unreadable word instead of a silent zero that then fails an arithmetic check
for the wrong reason.

## D5 — Advisory at launch, in both halves

`warning` severity keeps the family out of `runner.main`'s `{CRITICAL}` and
`{CRITICAL, ERROR}` gates. Absence from `FAMILY_RESOLUTION` is the half that is
easy to lose: `report.uncited_resolutions` turns a `contested` finding that
vanishes between reports into an `error`, so a `contested` advisory family would
red the nightly the first time anyone corrected an enumeration. Both halves are
pinned by test and flip together, by ruling.

Kept advisory **even though the corpus measures clean**, which deserves stating
because the temptation runs the other way. Two of the three sibling families
have flipped to enforcing and the flip is cheap. But the population this gate
would red is not today's canon — it is every future family-adding branch, which
cannot be measured in advance. Sequencing a flip behind a measured population is
the rule this campaign has now applied twice; treating it as an obstacle because
the current reading is zero would be learning the wrong lesson from two easy
flips.

## What was measured

| measurement | figure |
| --- | --- |
| registered families at branch point | 20 |
| canon enumeration names | 20, all resolving |
| canon numerals | total `twenty`, split `Four of the twenty`, remainder `sixteen` |
| canon-half findings before this change | **0** |
| findings with the family registered, delta NOT yet written | **3** |
| findings with this change's delta written | **0** |
| active deltas restating the requirement | 1 (this change's own) |
| MODIFIED block scenarios restated | 8 of 8, 7 byte-identical |
| `FAMILY_IDS` entries vs registry | 19 vs 21 — two families sectionless |
| aliases needed | 1, asserted load-bearing |

The three-to-zero transition is the design's own acceptance test: the check
reported this change's canon divergence, the restatement answered it, and the
check confirmed the answer before anything was committed.
