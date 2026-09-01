# Design: retire-hermes-flat-keys-and-openworkflow-tokens

Status: ratified
Proposed: 2026-09-01
Ratified: 2026-09-01 by Brett Heap (repository owner) — in-session, on the
orchestrator's report of the two packets read together. Record:
`review/ratification-2026-09-01.md`. The decisions below are RATIFIED as
reasoning, not performed: ratification authorizes the requirement text and
carries out no retirement, no policy row and no cut.

One design question carries real weight in this packet: **what a
recorded-why-it-stays entry looks like**, because the mechanism has no spelling
for it and inventing one badly is how the next four days of releases go stale
the same way the last five minors did.

## The section has two spellings and needs a third

`docs/contract-versioning-policy.md` uses exactly two forms today, and they are
consistent across every entry:

| state | closing formula |
| --- | --- |
| in force | `Warned since contract-vX.Y; removal target contract-vA.B.` |
| executed | `Deprecated at contract-vX.Y, removed at contract-vA.B.` |

There is no form for **reached its target and was deliberately not executed**,
which is the state all three of #522's entries have been in since 2026-08-27 and
the state entry 1's refusing half will remain in after `contract-v3.0`. The
absence of a form is a large part of why nothing said so: an author with no
sentence to write writes none.

## The third form

```
Warned since contract-v1.1; removal target RESTATED to contract-v4.0 —
<the reason the removal was not taken, measured>; the deprecating minor it
owes is <what that minor must make warn>.
```

Three properties, each load-bearing:

1. **The tail still parses.** Every bullet in the section ends in the
   `removal target contract-vX.Y` formula — a convention
   `018-openxwallet-deprecation-minor` kept deliberately, recording that *"the
   three existing entries all write `removal target contract-v2.0`. Following
   the precedent is more useful…"*. The restated form keeps a
   `contract-vX.Y` token adjacent to the words `removal target`, so a reader —
   or the `deprecation-target-currency` family the memo designs and this packet
   does not propose — still recovers a target from the bullet. A restatement
   that left no parseable target would convert a deprecation into an
   unenforceable one, which the *Deprecating (minor)* class already forbids by
   requiring the removal version to be stated.
2. **`RESTATED to` is visible.** A silently swapped number is
   indistinguishable from an entry that always named the later version, and the
   section's own reason for keeping Executed rows — *"a deprecation silently
   disappearing from a policy document is indistinguishable from one that was
   never honoured"* — applies with equal force to a target that silently moves.
3. **The reason is measured, not asserted.** For entry 1 it is a validator run,
   reproducible from the tree: `python3 scripts/validate-domain-factory.py
   <repo>` against each of the five supported consumers emits no legacy-flat-key
   warning, because `check_hermes` reaches that warning only in the `else` arm
   taken when `hermes.layers` is absent, and all five declare `layers`.

## Why not `health/dispositions.yaml`

The memo raises it and it is the wrong instrument here, for a reason that is
about the reader rather than about the file:

* it lives at the **aggregation root** (`ctx.agg_root / "health" /
  "dispositions.yaml"`), one level above openxFactory, and does not exist in
  this repository at all;
* it suppresses **doc-health findings by path**, which is a statement about a
  report, not about a contract;
* a consumer upgrading across the major reads the **pinned policy document** and
  cannot see it.

A disposition is the right instrument for a contested doc-health finding. The
reason a deprecation was not executed is not a finding — it is part of the
deprecation.

## Why `contract-v4.0` and not "unscheduled"

Proposal D2 states the ruling; the design note is only about what the
alternatives cost. "Unscheduled" leaves no parseable target and is refused by
the *Deprecating (minor)* class. "Whatever major follows the phasing minor" is
honest prose but names no version, so it fails the same test. `contract-v4.0`
names a version that lies ahead of the declared bundle and states its own
precondition; if the precondition is unmet when `contract-v4.0` arrives, the
entry is restated AGAIN under exactly the rule this packet promotes. That is a
loop, and it is the intended loop: an entry that keeps getting restated is
visible, where an entry that keeps naming a spent target is not.

## Why the two retirements share one packet

They are the same class (Breaking), land at the same major, live in the same
file (`scripts/validate-domain-factory.py`), move the same four release-surface
members, and neither moves a schema byte. Splitting them would mean two
`contract-v3.0`-targeted proposals whose realizations both rewrite the same two
sections of `docs/contract-versioning-policy.md`, which is a merge conflict
manufactured for tidiness. The doxBench family is genuinely different — it moves
a digest-pinned schema, a packaged corpus, a byte-identity baseline and a server
posture — and is separate for that reason and on the memo's recommendation.
