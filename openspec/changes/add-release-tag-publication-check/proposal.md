---
code_surface: openxFactory (`scripts/doc_health/release_tag_publication.py` — a new module owning the family, in the pattern `promotion_fidelity.py`, `release_inventory.py` and `family_enumeration.py` already set: its own severity and action constants, a pure function that answers the question from a declared bundle plus the repository's tag refs, and one `fam_release_tag_publication(ctx)` emit. `scripts/doc_health/__init__.py` — the family id joins the registered list. `scripts/doc_health/families.py` — the dispatch entry, and `FAMILY_SUMMARIES`/`FAMILY_RESOLUTION` if the family is to carry a summary line and a resolution class. THE FAMILY COUNT RIPPLE IS PART OF THIS SURFACE AND IS ENUMERATED IN TASKS: `docs/doc-health.md` says twenty-two families, `family_enumeration.py` measures the registered set against the documented one, and the `add-family-enumeration-check` capability exists precisely to redden when those disagree — so every place stating the count moves in the same commit as the registration, or the check this repository built for that purpose fires on its own release. `tests/doc-health/test_release_tag_publication.py` — the scenarios of this delta arrive as new tests with fixture repositories carrying real annotated tags, plus a self-gate probe over this repository. `docs/doc-health.md` — the family's row and its action line. NO change to `Finding`, to `report.render`, to the ranked-plan or finding grammars, to any threshold outside this family's own, to `release-inventory-drift`'s behaviour, or to `scripts/hermes_runtime_validation/release.py` — see D5, which is why `verify_tag` is not touched.)
target_release: implemented — the openxFactory main line. This surface cuts no contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed BY this change (which would be a pleasing irony to get wrong). The archive gate is therefore merge-plus-green on main, following `add-family-enumeration-check` and `add-unclassified-finding-class`: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly what this proposal predicts — see § What this will report on the day it lands, which predicts ZERO, and says why a nonzero answer there would be a finding about the estate rather than about the check.
Status: ratified
Proposed: 2026-08-31
Ratified: 2026-08-31 by Brett Heap (repository owner) — in session, in TWO ACTS. First, verbatim: "accept D1, D2, D5; threshold N=5", disposing four decisions and settling the one number the authoring session declined to pick; D4 was not named by that act and was carried as OWED rather than read as accepted. Then, on D4 being put to him as outstanding, verbatim: "accept D4, and yes that's the ratification". ALL FIVE orchestrator decisions are ACCEPTED AS DRAFTED. Record: `review/ratification-2026-08-31.md`.
Origin: issue #528, filed 2026-08-31 after `contract-v2.3` and `contract-v2.4` were both found declared-and-untagged by hand while completing the v2.4 cut's own record. Commissioned in session by Brett, verbatim: "take 528". The two bundles have since been tagged; the gap that produced them twice has not been closed, and closing it is what this proposes.
---

# Proposal: add-release-tag-publication-check

## Why

**The obligation is absolute, and nothing checks it.**
`docs/contract-versioning-policy.md` holds that the manifest version, the
changelog heading and the annotated tag *"MUST match"*, that *"the tag SHALL
point to that realized commit"*, and — the sentence that settles how a lapse is
to be read — that **"a bundle is not published until its tag exists"**. The same
document forecloses the obvious escape: *"THE RULE WAS NEVER ADVISORY, INCLUDING
WHILE IT WAS BEING BROKEN … No reader may cite this subsection, or the period it
narrates, to treat an untagged bundle as released."*

Four places could plausibly enforce that. None does:

* **No workflow calls the release validator at all.** `grep -rn
  "validate-contract-release\|verify-tag\|verify-commit" .github/workflows/`
  returns nothing.
* **`verify_tag` exists and is exercised only by unit tests** over synthetic
  repositories in `tmp_path` (`tests/hermes_runtime_contracts/test_release_inventory.py:818-848`).
  It is never run against this repository's real declared bundle.
* **`release-surface-integrity` deliberately does not anchor on tags** — *"A
  published annotated tag is NOT the reference point, deliberately: a declared
  bundle may exist before its published tag, so a rule anchored on a tag would be
  unevaluable for them"*, with an explicit scenario *"The declared bundle was
  never tagged."* That is correct **for that obligation**: it keeps drift
  evaluable at the commit. It also means the spec that knows most about the
  release surface is, by design, not the thing that will notice.
* **`tag-hygiene` is a different family.** It enforces `document-lifecycle`'s
  prose-tag grammar over document text (`scripts/doc_health/families.py:949`).
  The name is the trap: a reader who assumes tags are covered is reading the
  wrong sense of the word.

So the declaring commit and the published tag are two acts, by two actors,
separated in time, **with nothing joining them** — and the join is the thing the
policy requires.

## The evidence that this is structural, not careless

**It has now happened twice, and a human found it both times.**

`contract-v1.33`, `contract-v1.35` and `contract-v1.39` went untagged for weeks
after mandatory publication began, were recorded as an undischarged gap in the
policy itself, and were discharged only on Brett's ruling of 2026-08-25 —
retro-published at each bundle's realized commit.

Then `contract-v2.3` (declared by #514, 2026-08-30) and `contract-v2.4`
(declared by #526, 2026-08-31). Neither surfaced from any check; both were found
while auditing something else.

**The detail that makes the case.** The #526 cut wrote a careful `contract-v2.3`
disposition subsection into `contracts/CHANGELOG.md` — measuring the target
commit by the ratified rule, running `verify-commit`, recording *"TAG PUBLICATION
IS THE REPOSITORY OWNER'S ACT AND IS RECORDED HERE AS PENDING"* — **and said
nothing about its own tag.** A cut that documents its predecessor's gap while
standing in it is not an inattentive cut. It is a process with no place to
notice, which is the definition of a missing check rather than a missing effort.
That omission was itself repaired by hand (#532), which is one more instance of
the same manual catch.

**And the policy's own standing sentence goes stale silently.** *"Every bundle
from `contract-v1.7` — where mandatory publication begins — is now tagged"* was
false for the whole v2.3/v2.4 window and is true again today. A sentence that
flips without anything noticing is an argument for a check, not for another
correction of the prose.

## What changes

A new deterministic doc-health family, `release-tag-publication`, which for
every repository in scope that declares a contract bundle asks one question the
policy already answers: **does that bundle have a published annotated tag, and
does it point where the policy says it must?**

The requirement is specified in `specs/doc-health/spec.md` in this packet. Its
shape in one paragraph: no finding while the declaring commit is still the
published tip, because that is the legitimate window every cut passes through; a
`warning` once further first-parent commits have landed on top of an untagged
declared bundle; an `error` past the threshold; a distinct `error` where a tag
exists but peels to a commit that does not declare the bundle, which is a worse
condition than absence and must not be reported in the same words; a skip,
never a silent pass, where the question cannot be asked; and no finding at all
below `contract-v1.7`, the legacy sequence the policy leaves untagged by design.

**The packet also carries a `## MODIFIED Requirements` block on "Deterministic
check families", and that is not optional.** That requirement NAMES every family
and COUNTS them three times in prose — the total, the scan-set split, and the
remainder — and `family-enumeration` measures those numerals against the code
registry. Every new family must restate the whole requirement to add itself, and
`add-family-enumeration-check` exists because that restatement was left
incomplete THREE TIMES IN THREE DAYS with all three catches human. So the block
is restated whole, all eight scenarios carried unchanged, with twenty-two
becoming twenty-three, the list gaining the family last, the scan-set split and
the remainder moving with it, and one sentence describing the new family's
document-list behaviour in the pattern the block already uses. A packet that
added the family and skipped this would redden `family-enumeration` on its own
landing.

The obligation belongs to `docs/contract-versioning-policy.md`; this requirement
defines only how doc-health checks it — the same by-reference relationship
`tag-hygiene` has with `document-lifecycle`'s marker grammar and
`release-inventory-drift` has with `release-surface-integrity`.

## Orchestrator Decisions — flagged for veto

These were taken by the authoring session under standing patterns. Brett's
commissioning covers the decision to build a check and nothing below.

**D1 — ACCEPTED 2026-08-31. A NEW REQUIREMENT, NOT A `## MODIFIED` BLOCK ON
`Release-inventory drift`.** Measured, not preferred. That requirement's non-`contested`
classification rests on a stated structural fact: its findings are *"RESOLVED BY
A RELEASE CUT, which is exactly the act that makes them vanish between
reports."* **A tag finding is not resolved by a cut.** It is resolved by a tag
publication — a different act, by a different actor, at a different time — so
folding it in would falsify the sentence that justifies the family's resolution
class. The archive rule that a MODIFIED delta wholesale-replaces its named
requirement is the second reason: it would put eight scenarios at risk to add
one.

**D2 — ACCEPTED 2026-08-31; the shape veto was not exercised. A NEW FAMILY,
NOT A FINDING CLASS INSIDE `release-inventory-drift`.**
Follows from D1: two different resolution acts should not share a family whose
resolution semantics are declared. The cost is real and is not hidden — the
family count ripples through `docs/doc-health.md`, the registered set, and
`family-enumeration`, which exists to redden when those disagree. Tasks
enumerate every site. **If Brett prefers the cheaper shape, the veto is here**,
and the requirement would move into `Release-inventory drift` as a MODIFIED
block with all eight scenarios restated and its resolution sentence amended.

**D3 — RULED 2026-08-31: N = 5. THE WINDOW, AND A THRESHOLD THE AUTHORING
SESSION SHOULD NOT PICK.** A
check that fires the moment the manifest moves is noise on every correctly
performed cut, because the tag legitimately follows the declaration. The shape
proposed is distance-based: silent while the declaring commit is the published
tip, `warning` after that, `error` past N further first-parent landings on
published `main`. **N is a governance number, not an implementation detail**, and
the packet proposes **five** only so the scenarios have something concrete to
say. The evidence for calibration: `contract-v2.3` sat untagged across six
first-parent landings before a human noticed; the August three sat for weeks.
**Brett ruled N = 5 on 2026-08-31**, which is the number the packet had proposed;
the scenarios now state it as the ruled default rather than as a placeholder.

**D4 — ACCEPTED 2026-08-31, in the second act. WHAT THE CHECK ASSERTS ABOUT
THE TARGET.** Existence alone is too weak: a
tag pointing at the wrong commit satisfies "a tag exists" and violates *"the tag
SHALL point to that realized commit."* Full derivation of the policy's target —
*"the EARLIEST FIRST-PARENT COMMIT on published `main` that DECLARES the bundle
and at which `verify-commit` PASSES"* — is expensive inside a doc-health run,
because the second conjunct is a digest verification per candidate. The packet
therefore specifies the **cheap half as an error and the expensive half as out of
scope for this family**: the tag MUST peel to a commit that DECLARES the bundle,
which catches the realistic failure (a tag placed on the wrong release, or on a
branch commit) without re-running the verifier. **The residue is disclosed rather
than hidden**: this family does not prove the target is the EARLIEST such commit,
and a tag on a later declaring commit passes it.

**D5 — ACCEPTED 2026-08-31. NOT BUILT ON `verify_tag`, WHILE #338 STANDS.** `verify_tag` cannot
distinguish *"I have not fetched"* from *"this tag is unreachable from `main`"* —
`git merge-base --is-ancestor` exits 128 when an argument is not a commit in the
local object store, and that is folded in with the genuine negative (#338).
Observed live while measuring this proposal's evidence: `verify-tag` fails
identically on `contract-v2.2`, whose tag is definitively correct. A family built
on it today would report the benign case in the serious case's words, which is
the failure mode doc-health exists to prevent. The family therefore reads tag
refs directly and does its own peel-and-compare. **If #338 lands first, this
decision is worth revisiting** — reusing the canonical verifier is otherwise the
better shape.

## The ruling of 2026-08-31

Brett Heap, in session, verbatim: **"accept D1, D2, D5; threshold N=5"**.

| Decision | Disposition |
|---|---|
| **D1** new requirement, not a MODIFIED of `Release-inventory drift` | **ACCEPTED** |
| **D2** a new family, not a finding class inside that one | **ACCEPTED** — the shape veto was available and not exercised |
| **D3** the window and its threshold | **RULED: N = 5** first-parent landings |
| **D4** what the check asserts about the target | **ACCEPTED** in the second act, after being put to him as unruled |
| **D5** not built on `verify_tag` while #338 stands | **ACCEPTED** |

**D4 was carried rather than assumed, and then ruled.** The first act named four
decisions and D4 was not among them. It is the one that decides what this family PROVES: the
packet proposes asserting the cheap conjunct — the tag must peel to a commit that
DECLARES the bundle — and disclosing that it does not prove the target is the
EARLIEST such declaring commit, so a tag on a later declaring commit passes and
remains a defect under the policy. A packet that read silence as acceptance would
be narrowing a ruling by omission, which is the failure this estate records
against itself most often. It was put to him as
outstanding rather than folded in, and the second act accepted it — so the
residue is ACCEPTED WITH ITS DISCLOSURE INTACT rather than accepted by silence,
which is the whole difference this paragraph exists to preserve.

**The second act is the ratification.** Verbatim: *"accept D4, and yes that's the
ratification"*. `Status:` is `ratified`, task 1.1 is discharged, and the record is
`review/ratification-2026-08-31.md`. **Ratification authorizes realization and
performs none of it** — group 2 is a Spec Kit feature and is not built by this act.

## What this will report on the day it lands

**ZERO findings.** Every bundle from `contract-v1.7` carries an annotated tag as
of 2026-08-31: 46 published tags against 53 changelog entries, with the seven
absences all in the `contract-v1.0`–`contract-v1.6` legacy sequence the policy
leaves untagged by design. `contract-v2.5`, cut by #533 and the current declared
bundle, is tagged.

That prediction is load-bearing. **A nonzero count on the first run is a finding
about the estate, not about the check** — and it is exactly the kind of finding
this family exists to produce, so it should be read that way rather than treated
as a false positive to tune away.

## What this packet moves in doc-health, MEASURED WITH REALIZATION LANDING WITH IT

**The unratified-packet prediction this section first carried is superseded, and
the reason is recorded rather than quietly overwritten.** It predicted +3
`warning` and +1 `info` for a packet whose delta declared twenty-three while the
registry still held twenty-two, and called that state acceptable. It was not:
`family-enumeration`'s self-gate asserts the real corpus reads ZERO on both
halves, so those three warnings did not merely move a count, they RED A GREEN
GATE — and `add-family-enumeration-check`, the packet that wrote that gate,
landed its own delta, module and tests in ONE commit (`bc779dcc`) for exactly
this reason. A family addition is one landing in this estate. Brett ruled the
packet land that way on 2026-08-31.

**Measured with the realization in place**, `--single-repo` against the
merge-base, same clock:

| | critical | error | warning | info |
|---|---|---|---|---|
| base | 5 | 4 | 28 | 12 |
| head | 5 | 4 | 28 | **13** |

**+1 `info`, and nothing else.** The three `family-enumeration` warnings are
gone because canon-pending-behind-a-complete-delta is quiet by that family's own
design — the case its `test_canon_pending_behind_a_complete_delta_is_quiet`
exists for. The one remaining `info` is `modified-block-currency` naming the two
body units this packet's MODIFIED block deliberately rewrites; three other active
packets carry the same shape, the arm says of itself that it *"CANNOT distinguish
[this] from a deliberate rewording, and does not claim to"*, and it clears when
the block promotes at archive.

**The family itself reports ZERO over this tree**, run directly:
`doc-health --single-repo . --family release-tag-publication` renders "No
findings" — not a skip, a genuine answer, because every bundle from
`contract-v1.7` is tagged and `contract-v2.5` is the current declared bundle.

## What this will report on the day it lands

**ZERO findings.** Every bundle from `contract-v1.7` carries an annotated tag as
of 2026-08-31: 46 published tags against 53 changelog entries, with the seven
absences all in the `contract-v1.0`–`contract-v1.6` legacy sequence the policy
leaves untagged by design. `contract-v2.5`, cut by #533 and the current declared
bundle, is tagged.

That prediction is load-bearing. **A nonzero count on the first run is a finding
about the estate, not about the check** — and it is exactly the kind of finding
this family exists to produce, so it should be read that way rather than treated
as a false positive to tune away.

## What this packet adds to doc-health WHILE IT SITS UNRATIFIED

Measured, not predicted: a `--single-repo` run with and without this packet, same
clock. **+3 `warning`, +1 `info`, and nothing else moves.** Every one of them is
the estate's own machinery reading this packet correctly, and every one clears at
realization rather than needing a disposition.

**The three warnings are `family-enumeration`, firing on this packet's own
delta**, and they are the reason the family exists. It measures a delta's
restatement against the CODE registry, and this packet is a proposal: the delta
says twenty-three, the registry still holds twenty-two, and the family says so
three times — the total, the scan-set split, and the name that resolves to no
registered id. **This is the correct answer to the question it asks.** A
propose-then-realize capability necessarily spends the interval between
ratification and realization in exactly this state, and the alternative — writing
the delta to match the registry — would be a restatement that omits the family
the packet exists to add, which is the defect `add-family-enumeration-check` was
built to catch. Group 2.3 clears all three by registering the family and moving
the count sites in the same commit.

**The one info is `modified-block-currency`**, reporting that the MODIFIED block
does not carry 2 of the 41 body units canon currently states — and the two it
names are precisely the two sentences this packet deliberately rewrites, the
total and the scan-set split. The arm says of itself that it *"CANNOT distinguish
[this] from a deliberate rewording, and does not claim to"*, and classes it
`contested` at `info` for that reason. Three other active packets carry the same
finding shape today for the same reason. It is the honest state of a genuine
MODIFIED block and it clears when the block promotes.

**Nothing else moves**: no severity count outside those four, no census, no word
count, no canon-share figure, no catalog record. If a reviewer's run disagrees
with this paragraph, the disagreement is the finding.

## Non-goals

* **Publishing tags.** The policy makes tag publication the repository owner's
  act and the changelog records it as such. This check reports; it never tags.
* **Re-deriving the retro-publication rule.** The policy owns it; this family
  does not reimplement its expensive conjunct (D4).
* **Fixing #338.** Separate defect, separate fix, and D5 explains why this
  packet routes around it rather than waiting on it.
* **Any change to `release-inventory-drift`'s behaviour**, its severities, or
  its resolution class (D1).
