# Design: bringing canon to the validator, and dating an illustration that went stale

## Context

Two texts in this repository say something that is not true, and neither
defect is a design problem. One is a SEVERITY that promoted canon states as
`warning` while the shipped validator has reported `error` for fourteen months
of commits; the other is a PRESENT TENSE describing three bundles that were
tagged nine days ago. Both were filed rather than fixed — issues #561 and #339
— because a promoted specification is amended only through a ratified OpenSpec
change, and neither defect was large enough to carry one alone. Brett Heap's
2026-09-03 ruling put them in one packet.

This design records the three things a later reader will want and would
otherwise have to re-derive: the measurement that made the ruling free, why
no phasing is owed, and — stated plainly because it is the most likely
misreading of the whole change — **that the validator does not change.**

## The measurement

Item 2 of what issue #561 said a disposition owes was *"a measurement before
the ruling — how many gates across the five supported DomainxFactory consumers
carry an `owner_layer` that resolves to nothing today. If the answer is zero,
either direction is free; if it is not, the choice refuses somebody and owes
the deprecation phasing that goes with that."*

Taken 2026-09-02 by running `scripts/validate-domain-factory.py` at openxFactory
`96b2b968` (`origin/main` at the time) against the five supported consumers as
checked out in the xFactory aggregation workspace:

| consumer | exit | `owner_layer` findings | run result |
| --- | --- | --- | --- |
| codexFactory | 0 | 0 | 0 error(s), 0 warning(s) |
| MedxFactory | 0 | 0 | 0 error(s), 1 warning(s) |
| LedgerxFactory | 0 | 0 | 0 error(s), 1 warning(s) |
| OpsxFactory | 1 | 0 | 3 error(s), 26 warning(s) — all unrelated (`tenancy.isolation.subject_context='per_subject'` unrecognised; two profiles missing `profile.id`) |
| AdxFactory | 0 | 0 | 0 error(s), 1 warning(s) |

**Zero gates across the five consumers carry an `owner_layer` that resolves to
nothing.** OpsxFactory's non-zero exit is recorded rather than smoothed away:
it is real, it is that repository's own business, and not one of its findings
is an `owner_layer` finding.

The measurement is reproduced in this design rather than only cited, because
the issue thread it was posted to is not part of the ratified corpus and the
argument for taking no phasing rests entirely on it.

## Why no phasing is owed

A severity that RISES normally owes a deprecation window: somebody's tree
passes today and fails tomorrow, and the contract-versioning policy's refusal
list exists so that consumer can find out which of its own artifacts the major
refuses. **That reasoning has no subject here.** The population the rise would
refuse is empty, and it is empty in both directions:

* **No consumer is refused by the amendment.** Zero unresolvable tokens means
  no gate's status changes in any of the five repositories.
* **No consumer is refused by the run, either — because the run already
  errored.** The validator has failed a domain repository's conformance run on
  this condition since 2026-07-03. A consumer that had an unresolvable token
  would already know, from a red run, and would not learn it from this text.

So the amendment refuses nobody, warns nobody it has not already warned, and
carries no window, no refusal-list row and no deprecation entry. It is a
correction of a text, not the execution of a deprecation, and it is
deliberately not routed through `contract-deprecation-execution`.

## THE VALIDATOR DOES NOT CHANGE

Stated as its own section because the change's title invites the opposite
reading, and because issue #561's item 3 says only that *"ONE of the two texts
moves"* — leaving open, correctly, which one.

`scripts/validate-domain-factory.py`'s `check_workflows` carries:

```python
            if token not in allowed:
                rpt.error(f"workflows/{wf.name}: gate {gid} owner_layer {owner!r} does "
                          f"not resolve to a declared layer (allowed: {sorted(allowed)})")
```

**That line is not opened by this change and its severity does not move.** The
ruling is that CANON comes to the CODE, so editing the code would perform the
opposite of what was ruled. `code_surface: none` is therefore a statement about
the subject and not merely about the size of the diff: a version of this packet
that touched the validator would be a different change with a different
answer.

Two consequences follow and are recorded so nobody re-derives them:

1. **No release bundle is cut and no deprecation is executed.** Nothing under
   `contracts/` moves, so there is no changelog row, no manifest row, no
   digest set and no `contract-v3.x` obligation anywhere in this packet.
2. **#551's Executed row is untouched.** That packet retires the
   `openworkflow`-prefixed compatibility branch at `contract-v3.0` and states
   the general fall-through's severity as *"whatever the general rule
   carries"* — a deliberate deferral, written so that this change could move
   the general rule without reopening a ratified row. This change moves the
   general rule and does not reopen it.

## The #339 half: dating an illustration, not editing a rule

`release-surface-integrity`'s requirement *"The declared bundle describes the
release surface"* argues its reference point in one paragraph: a published
annotated tag is NOT the reference, deliberately, because a declared bundle
need not have one — and it names three bundles that had none.

All three were retro-tagged on 2026-08-25 by PR #333, so the paragraph's
present tense became false the same day. **The normative content is
unaffected.** The general fact the rule stands on — a declared bundle need not
carry a tag, so the inventory FILE at the commit is the reference — is still
exactly right, and the fourth scenario (*"The declared bundle was never
tagged"*) is restated unchanged because the state it describes remains
reachable for any future bundle.

**The treatment is not invented here.** PR #333 met the identical claim in
`scripts/doc_health/release_inventory.py`'s module docstring and handled it by
DATING the examples rather than deleting them, so that the rule keeps its
provenance:

> `contract-v1.33`, `contract-v1.35` and `contract-v1.39` were each declared
> and UNTAGGED for weeks, which is what this rule was written against; they
> were retro-published 2026-08-25 and the design stands on the general fact
> rather than on those three

Issue #339 named that treatment as the one that fits, and the amended paragraph
mirrors it: past tense, the duration kept, the retro-publication dated and
attributed to PR #333, and the closing sentence that the rule stands on the
general fact rather than on those three. A reader who deletes the three names
instead would remove the only evidence in canon that the untagged state ever
occurred.

## Decisions a reviewer may veto

| | Decision | Why |
| --- | --- | --- |
| **OD-1** | ONE packet carries both issues rather than two | Brett's ruling put them together; both are text-only amendments to promoted requirements, and #339's own text says it should ride "whoever next opens a change against `release-surface-integrity`" |
| **OD-2** | Canon moves, not the validator | The measured population is zero, the stricter gate is the one every consumer has conformed to for two months, and nobody asked to loosen it |
| **OD-3** | The word is `error`, with no added clause explaining the history | The requirement states an obligation; the history is this packet's, and belongs here and in the README record rather than in canon |
| **OD-4** | #339's paragraph is DATED, not deleted | PR #333's own precedent on the identical claim; deleting the names would erase canon's only evidence that the state occurred |
| **OD-5** | Both blocks are extracted from canon and edited, never retyped | `MODIFIED` replaces wholesale; extraction is what makes "two words and one paragraph" a measured claim rather than a hopeful one |
| **OD-6** | Two live corpus pins move in this commit | They count the corpus and any authored change moves them; each pin's own docstring prescribes moving it in the same commit with a dated note |

## Not in scope

- Any change to `scripts/validate-domain-factory.py` — § *The validator does
  not change*.
- The `openworkflow`-prefixed token branch, retired by #551's realization.
- OpsxFactory's three unrelated validator errors, which are that repository's
  own business and are recorded above only so the measurement is honest.
- The `contract-v1.33` / `v1.35` / `v1.39` release records themselves, which
  are the record of what was declared and are not edited to match a later
  world.
