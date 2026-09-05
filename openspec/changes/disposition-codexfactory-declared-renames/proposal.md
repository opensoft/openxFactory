---
code_surface: openxFactory — ONE artifact moves in substance and ONE test moves with it, both in this pull request, neither a registered contract row. (1) `contracts/openspec-cli-pin.yaml`: the `dispositions:` block gains TWO entries, both `repo: codexFactory`, each accepting exactly one ERROR-level finding of 1.12.0's scenario-currency check against one delta path of one codexFactory change, with six and seven citations respectively and `ratified_by: 'Brett Heap, 2026-09-05, "use recommended name, go on 3 repo shape"'`; four header paragraphs move from "the two dispositions" to "two pairs in two repositories" so the file does not describe itself falsely. NO other field of the pin moves — not `version`, not `integrity`, not `shasum`, not `tarball`, not `rollback:`, not `consumer_entrypoint:`. (2) `tests/openspec_cli_pin/test_openspec_cli_pin.py`: the count-pinning test that asserts the real pin carries exactly the two entries the bump carried moves 2 → 4 DELIBERATELY and gains the per-repository split, plus one new test asserting the codexFactory pair is out of scope on openxFactory's own tree. NOT THIS CHANGE'S SURFACE: `scripts/validate-openspec-cli-pin.py` does not move — the scoping, the whole-message match, the staleness asymmetry and the four refusal codes all already exist and this packet is their FIRST USE ACROSS A REPOSITORY BOUNDARY, which is the point; no workflow moves; codexFactory's own gate leg and its `stack.yaml` re-pin are step 3 and are not ridden on this diff; nothing in `openspec/specs/` is written, so no capability is promoted and no floor advances.
target_release: implemented (the openxFactory main line). No contract-bundle involvement: `contracts/openspec-cli-pin.yaml` is a CONSUMPTION pin — it is not a registered row in `contracts/manifest.yaml` and appears in no `contracts/releases/*.digests.yaml` inventory — so no digest set moves, no `contract_bundle_version` is spent and no release tag is owed. This is the same reasoning `bump-openspec-cli-pin-to-1.12` recorded for the same file, and it is recorded again rather than inherited because the file's status is the fact that decides it. The archive gate is `release-realization`'s merged-plus-green evidence for a non-empty code surface: this packet's own `openspec-cli-pin` gate run, green on openxFactory's tree, plus the codexFactory-tree measurement recorded verbatim in `evidence/codexfactory-dispositions-2026-09-05.md`.
Status: ratified
---

# Proposal: disposition-codexfactory-declared-renames

Status: ratified
Ratified: Brett Heap, 2026-09-05 — verbatim "ratify 697", heard first-hand by
session codeXfactory-1 (lane codexfactory-1, which authored this packet); record
at `review/ratification-2026-09-05.md`, which also records that the record was
written AFTER the green run on `bfc9451e` and BEFORE any merge.
Proposed: 2026-09-05
Origin: Operator ruling, Brett Heap, 2026-09-05, in session to lane
codexfactory-1, verbatim: *"use recommended name, go on 3 repo shape"* —
accepting, for codexFactory's pair of marker-blind findings, the same exit he
ruled *"take exit 2"* for openxFactory's own pair the same day (#677), and
commissioning the three-step realization this packet is step 2 of. **The ruling
settles WHICH EXIT codexFactory takes and in what order. It does not ratify this
packet's text**, which carries `Status: draft` and owes a ratification citation
from a separate act; when that act happens it will add Brett's *"ratify \<PR>"*
verbatim, as `bump-openspec-cli-pin-to-1.12` records *"ratify 677"*.

**2026-09-05: THAT ACT HAS HAPPENED.** The paragraph above is kept as written
because it is the record of what the PLAN-level word did and did not do, read as
of the day it was given. Brett Heap ratified this text separately the same day,
verbatim **"ratify 697"**, first-hand to this lane and against head `bfc9451e`;
the two words and the order of events are in
`review/ratification-2026-09-05.md`. The merge is a further, separate word and
has not been given.

## Why

**A consuming repository has hit the exact disagreement this pin already knows
how to carry, and the acceptance has to be written where the pin lives.**

`bump-openspec-cli-pin-to-1.12` (#677) moved the fleet's OpenSpec CLI to
`@fission-ai/openspec@1.12.0` and, with it, added a disposition mechanism —
because 1.12.0's scenario-currency check is BLIND to this estate's reserved
narrowing marker, ``**Merged into `<destination>` by <change-id> (<date>):**``,
and re-reports declared, ratified retitles as ERRORs. That mechanism was written
to be fleet-wide: every entry carries `repo:`, the run resolves the validated
tree's identity from `git config --get remote.origin.url`, and a disposition
naming another repository is neither applied to nor stale on this one. Until now
it had exactly two entries and both named openxFactory, so that scoping had
never carried weight in production. **It carries weight now.**

codexFactory ran this repository's pinned entrypoint over its own tree at
PR #216's head `b2a6af34` on 2026-09-05:

```
Totals: 23 passed, 2 failed (25 items)
```

Twenty-three of twenty-five items clean. The two failures:

```
change/add-regular-pr-council-clearance
  ✗ [ERROR] merge-master-approval/spec.md: MODIFIED "Bounded autonomous surface" omits scenario(s) the current spec still has: "A human-authored pull request is never auto-approved". …
change/amend-composition-selector-labelling
  ✗ [ERROR] domain-hermes-content/spec.md: MODIFIED "The merge-readiness holder composition is declared from governed sources" omits scenario(s) the current spec still has: "Current aliases do not masquerade as immutable versions". …
```

**Both omissions are DELIBERATE, DECLARED, and RULED ON.** Each block announces
its own narrowing with the reserved marker, in the form canon writes out:

* `add-regular-pr-council-clearance` retitles *"A human-authored pull request is
  never auto-approved"* to *"A human-authored pull request is never approved by
  tier 1 alone"*. The successor keeps canon's `WHEN` verbatim and narrows its
  `THEN`: a human-authored pull request is still never approved by the tier-1
  envelope alone, and approval MAY now come from tier-2 council clearance
  carrying a unanimous verdict pinned to the candidate's exact head SHA — the
  BREAKING change that packet declares. **codexFactory PR #216 CONVERTED this
  block's marker** from `Removed from canon` to `Merged into` on Brett's
  2026-09-05 ruling, because promoted `doc-health` holds that a block which adds
  a scenario title canon does not carry "is a retitle, whatever the marker calls
  it" (`openspec/specs/doc-health/spec.md:1750`) and names `Merged into` as the
  author's instrument for that shape.
* `amend-composition-selector-labelling` retitles *"Current aliases do not
  masquerade as immutable versions"* to *"A selector is labelled for what it is,
  and none masquerades as an immutable revision"*, on Brett Heap's 2026-08-31
  ruling (`hermes/domain/review-councils/records/2026-08-31-enrolled-roster-model-pin-flip.md`
  §5.1/§12.0) that the old title's `THEN` needed a reading to stay true after the
  roster model-pin flip; the retitle restates it for exact identifiers and
  aliases alike so canon states the rule directly.

**The only edit that satisfies the tool reverts a ratified decision in each
case** — copying the first scenario back reinstates a bar `add-regular-pr-council-clearance`
was written to lower; copying the second back restores the clause the
2026-08-31 ruling found required a reading. That is not a defect to fix. It is
an exception to ACCEPT, in writing, with a citation, which is precisely what
`dispositions:` exists for and precisely what Brett ruled for openxFactory's own
identical pair on the same day.

**This is task 6.1 of `add-openspec-cli-pin`, step 2 of 3.** #667 named
"codexFactory wires the fleet OpenSpec-CLI pin into CI" as owed work. Step 1 is
codexFactory PR #216 (the marker conversion and the measurement quoted above).
Step 3 is `adopt-openspec-cli-pin-gate` in codexFactory. **Step 3 cannot land
before this one**: codexFactory's gate would go red on its first run, on two
findings the fleet has already decided are exceptions.

## What Changes

* **`contracts/openspec-cli-pin.yaml` gains two entries**, both
  `repo: codexFactory`, each naming one item, one delta path, `level: ERROR` and
  the finding's WHOLE message text quoted from 1.12.0's own JSON report. Each
  carries `why:`, a non-empty `cited_to:` (six and seven citations), and
  `ratified_by: 'Brett Heap, 2026-09-05, "use recommended name, go on 3 repo shape"'`.
  Each `retires_when:` names the archive of ITS OWN codexFactory change and
  states the consequence in the tool's vocabulary: on that day codexFactory's
  `--all` run refuses `pin-disposition-stale` until the entry is deleted.
* **Four header paragraphs of the pin are re-written** so the file describes
  itself truthfully: "THE TWO DISPOSITIONS" becomes "THE DISPOSITIONS", the
  rollback note's "two entries below" becomes "four", the block above
  `dispositions:` says two pairs in two repositories rather than "both entries
  below", and a new paragraph records how the second pair arrived. A pin whose
  prose says "two" over a list of four is a pin nobody can review.
* **The count-pinning test moves 2 → 4, deliberately and visibly.** Its own
  docstring says a bump that "silently grew a third exception would still be a
  bump nobody read" — so the growth is READ here, in this packet, and the test
  is strengthened rather than merely widened: it now asserts the per-repository
  split (two `openxFactory`, two `codexFactory`) instead of a single-repository
  set, which a bare count bump would have dropped.
* **One test is added**: the codexFactory pair is out of scope — neither applied
  nor stale — on openxFactory's own tree. That is the property keeping this
  repository's gate green, and it is now asserted against the REAL pin rather
  than only against a fixture.
* **No spec delta.** See *Capabilities*.

## Capabilities

**`neutral-product-pin` — exercised, not extended.** The ADDED requirement
`bump-openspec-cli-pin-to-1.12` carries, *"A dispositioned finding is cited,
upgrade-coupled, and refused when stale"*, already states every property this
packet relies on:

| property this packet needs | where the bump's requirement already states it |
| --- | --- |
| a disposition is scoped to one repository | "A DISPOSITION IS SCOPED TO ONE REPOSITORY… a disposition SHALL name the repository whose corpus it is about" |
| an entry for another repository is out of scope and never stale | "…and a run over any other repository SHALL neither apply it nor treat it as stale"; scenario *"A consuming repository runs the same pin over its own tree"* |
| a consumer's entry retires when the consumer's change archives | "A DISPOSITION MATCHED BY NO FINDING IN A WHOLE-CORPUS SCAN SHALL REFUSE THE RUN"; scenario *"A dispositioned finding stops occurring"* — "its change archived" |
| the entry carries the owner's word and a citation | "SHALL carry a non-empty CITATION… and SHALL name the authority that granted it" |

**So this packet adds no rule and writes no delta**, and says so in the machine's
own grammar: `.openspec.yaml` declares `skip_specs: true`, the escape 1.12.0
reads at `dist/core/change-metadata/schema.js` and honours in `openspec validate
--strict`. Restating a ratified requirement under `## ADDED Requirements` would
create a second, drifting copy of it. Writing `## MODIFIED Requirements` against
it would be the ordering refusal: that requirement is not yet promoted into
`openspec/specs/neutral-product-pin/spec.md`, the bump being active, so a
MODIFIED block would target text that is not canon. `design.md` § 4 records the
criterion and the reading.

## Impact

* **codexFactory's gate becomes possible.** Step 3 can wire
  `scripts/validate-openspec-cli-pin.py` into codexFactory CI and expect green:
  0 undispositioned failures, 2 named exceptions, printed on every run.
* **openxFactory's own gate is unchanged and must stay so.** The property is
  proven both ways in `evidence/codexfactory-dispositions-2026-09-05.md`: the
  gate's literal invocation on this tree still applies exactly its own two and
  reports no staleness over codexFactory's.
* **Two standing exceptions now exist against changes this repository does not
  own.** Neither retires on any openxFactory act, and each is re-derived at the
  next pin bump like every other. The refusal that enforces that lands on
  **codexFactory's** run, not on this one — which is correct, and is why
  `retires_when:` says which tree refuses.
* **Still owed after this lands** — named so nobody reads it as done:
  * **Step 3, `adopt-openspec-cli-pin-gate` in codexFactory**: the gate leg
    itself, plus the `stack.yaml` re-pin to an openxFactory commit AT OR AFTER
    this change's merge (an earlier pin resolves a pin file without these
    entries, and the gate would fail on its first run).
  * **Task 6.1 of `add-openspec-cli-pin` and task 6.3 of the bump stay UNTICKED
    here.** They tick when step 3 lands, not when its precondition does.
  * **Ratification.** Brett's ruling chose the exit; this text is `Status: draft`
    until a separate act says otherwise.
