# FINDING — task 3.2's shorthand refuses design.md's own prescription I

**Raised 2026-09-09 by lane `opsXfactory-1` during § 3 implementation. Found by
a fixture, not by reading.** The ratified delta arbitrates; nothing ratified was
widened or narrowed to resolve it.

## What happened

Task 3.2 words the rewritten-pin leg as:

> refuse an instrument whose `custody.sha256` equals **any entry's**
> `observed_sha256` **while a LATER entry exists**

Implemented exactly as written, that leg REFUSED
`examples/consent-instrument/consent-instrument-custody-chain-two-entry.example.yaml`
— the fixture modelled on `design.md` § *The consumer handoff* **prescription
I**, which is the estate's MEASURED repair for
`opensoft-exchange-monitor-reader-consent.yaml`.

## Why the shorthand fails

A `path_only` archive move changes **ZERO bytes**. So in prescription I:

```
custody.sha256      = bb8f89ea…
e1.previous_sha256  = bb8f89ea…   (anchors correctly)
e1.observed_sha256  = bb8f89ea…   (EQUAL — that is what path_only MEANS)
e2                  = the later entry
```

`custody.sha256` equals `e1.observed_sha256` **by construction**, and e2 supplies
the "later entry". The literal rule therefore refuses **every**
`archive_move` chain — making a member of a closed enumeration unusable by any
conforming record.

**That is the exact failure C-6a was raised to fix**, reappearing in a different
leg. C-6a's own words: *"A member of a closed enumeration that no conforming
record can ever use is not a member; it is a mistake."*

## What the ratified text actually says, and what was implemented

The delta's scenario *The executed pin is never rewritten to match the moved
target*:

> **THEN** the repair records the divergence and leaves `custody.sha256`
> **verbatim**
> **AND** an instrument whose pin **was rewritten** to the observed digest is
> nonconformant even though it now verifies

and the ADDED requirement's neutral-leg list: *"that no entry's digest has been
**written back into** `custody.sha256`"*.

**"Written back" is a claim about the pin having CHANGED**, not about it
coinciding with a value. The implemented condition is therefore ANCHOR-RELATIVE:

> the pin is REWRITTEN when it **no longer anchors the chain**
> (`custody.sha256 != e1.previous_sha256`) **AND** it equals some entry's
> `observed_sha256`.

Prescription I passes (the pin still anchors, so nothing was written back), and
a genuinely rewritten pin is still caught — with the specific
`custody-pin-rewritten` code rather than only the generic
`custody-chain-unanchored`, which is what the leg exists to add.
`examples/consent-instrument/negative/custody-pin-rewritten.yaml` is the
multi-entry fixture that proves it still fires.

## Disposition

**No ratified text was changed.** `tasks.md` § 3.2 keeps its wording; the delta
governs where the two differ, which is the packet's own rule. The reasoning is
carried in a comment at the leg itself so the next reader does not "simplify"
it back to the shorthand.

**For the architect:** this is a defect in the ratified TASK's paraphrase, not
in the requirement. It is recorded here rather than silently coded around.
