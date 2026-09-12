---
code_surface: openxFactory — TWO artifacts move in substance, both in this pull request. (1) `contracts/openspec-cli-pin.yaml`: the `dispositions:` list LOSES one entry and GAINS two, going 5 -> 6. The DELETION is the whole `repo: codexFactory` / `item: add-regular-pr-council-clearance` / `path: merge-master-approval/spec.md` entry, because the event its own `retires_when:` named has happened. The two ADDITIONS are `repo: codexFactory`, `item: extend-merge-master-envelope-to-floor-bot-lanes` and `item: relocate-review-authority-floor`, both `path: merge-master-approval/spec.md`, both `level: ERROR`, each accepting one ERROR-level finding by its WHOLE message text quoted from 1.12.0's own report, with eight and nine citations and `ratified_by: 'Brett Heap, 2026-09-12, "ratified_by — ratify the entries as encoded"'`. Three prose blocks move so the file stops describing a list it no longer has: the rollback note's count, a NEW dated 2026-09-11 paragraph, and the block above `dispositions:` rewritten from "EVERY ENTRY BELOW IS THE SAME DISAGREEMENT, five times" into TWO DECLARED CLASSES, because that sentence becomes FALSE the moment these two land. A dated retirement note is added beneath the 2026-09-05 comment block, which is itself left UNEDITED. NO other field of the pin moves — not `version`, not `integrity`, not `shasum`, not `tarball`, not `lockfile`/`lockfile_integrity`/`lockfile_packages`, not `rollback:`, not `binary:`, not `verify_pin:`, not `consumer_entrypoint:`, not `pinned_invocation:`, not `resync_runbook:` — and NO surviving disposition entry is edited. (2) `tests/openspec_cli_pin/test_openspec_cli_pin.py`: the count-pinning test moves 5 -> 6 and is renamed; `DISPOSITION_MEASUREMENT` and `DISPOSITION_AUTHORITY_PREFIX` are RE-KEYED from `item` to the `(repo, item, path)` triple the verifier itself matches on, which is FORCED rather than cosmetic because one codexFactory change now carries TWO entries with different measurements and different authority dates; a new `DISPOSITION_CLASS` map asserts the reserved-marker citation IF AND ONLY IF the entry is of the marker-blindness class; and the authority is read through BOTH spellings `DISPOSITION_AUTHORITY` has always admitted, with a new assertion that exactly one stands. `tests/sequenced_after/corpus-ledger.yaml` gains this change's own row, by `--seed-ledger`. `README.md` gains its OpenSpec Records entry. NOT THIS CHANGE'S SURFACE: `scripts/validate-openspec-cli-pin.py` does not move — the per-repository scope, the whole-message match, the staleness asymmetry and the four refusal codes all already exist, and `DISPOSITION_AUTHORITY` has admitted `recorded_by:` since the bump; no workflow moves; nothing under `openspec/specs/` is written, so no capability is promoted and no floor advances; codexFactory is not touched at all — its pin advance is lane `codeXfactory-1`'s act in codexFactory's own pull request.
target_release: implemented (the openxFactory main line). No contract-bundle involvement: `contracts/openspec-cli-pin.yaml` is a CONSUMPTION pin whose registered `contracts/manifest.yaml` row deliberately carries NO per-file `sha256` — the row states the reason in its own comment, that the pin legitimately moves on a version bump, a disposition ADDED and a disposition RETIRED, and this packet is the first to do the third of those three — and it appears in no `contracts/releases/*.digests.yaml` inventory, so no digest set moves, no `contract_bundle_version` is spent and no release tag is owed. `release-tag-gate` short-circuits on exactly that fact: this pull request touches neither `contracts/manifest.yaml` nor `contracts/releases/**`. The archive gate is `release-realization`'s merged-plus-green evidence for a non-empty code surface: this packet's own `openspec-cli-pin` and `pytest-suite` runs, green on openxFactory's tree, plus the codexFactory-tree measurements recorded verbatim in `evidence/codexfactory-regular-pr-council-clearance-archive-2026-09-11.md`.
sequenced_after: []
---

# Proposal: disposition-codexfactory-regular-pr-council-clearance-archive

Status: draft
Proposed: 2026-09-11, in lane `provenance-autonomous-merge` (session
`codeXfactory-3`).
Origin: openxFactory
[#745](https://github.com/opensoft/openxFactory/issues/745), the governing issue
this packet's precedent cited and, not by coincidence, the proposal issue of one
of the two changes it dispositions. Claim at
[comment 5643012460](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5643012460).

**THE ENTRIES ARE RATIFIED; THIS PACKET'S TEXT IS NOT, AND THE DIFFERENCE IS
DELIBERATE.** Brett Heap, 2026-09-12T03:04:29.167Z, first-hand, in session, as a
selection in a multiple-choice round, verbatim: ***"ratified_by — ratify the
entries as encoded"*** — recorded at
[comment 5643056862](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5643056862)
and at `review/ratification-2026-09-12.md`. The question put to him was the
AUTHORITY SPELLING of the two new entries, and the word answers it and ratifies
their text. It was NOT a question about `proposal.md`, `design.md` or
`tasks.md`, so those carry `Status: draft`, and the pull request is opened DRAFT
and stays DRAFT. The precedent read the near-identical *"go A, ratify the
disposition entry as encoded"* as carrying its whole packet; **that reading is
available here and is deliberately not taken**, because it was not asked for.
Upgrading it costs one further word and one line per document, and this
paragraph exists so that upgrade is visible rather than assumed.

## Why

**AN ARCHIVE IN A CONSUMING REPOSITORY RETIRED ONE OF THIS PIN'S EXCEPTIONS AND
RAISED TWO MORE IN THE SAME ACT — and only this repository can write either
half.**

`bump-openspec-cli-pin-to-1.12` (#677) moved the fleet's OpenSpec CLI to
`@fission-ai/openspec@1.12.0` and, with it, added a disposition mechanism with
two clauses: an exception is ACCEPTED where a human rules it, and an exception
whose condition has GONE is REFUSED until it is deleted. Three packets have
exercised the first clause. **This is the first to exercise the second, and it
exercises both at once.**

codeXfactory/codexFactory PR **#434** (`archive/add-regular-pr-council-clearance`,
head `87ea247f`) archives `add-regular-pr-council-clearance`. That archive does
two things in one act:

* **It RETIRES this pin's `add-regular-pr-council-clearance /
  merge-master-approval/spec.md` entry.** The change has left the `--all`
  corpus, so its finding no longer occurs and the entry matches nothing. **The
  entry predicted this day in its own words**, and the prediction is quoted
  rather than paraphrased: *"add-regular-pr-council-clearance archives IN
  codexFactory — and on that day codexFactory's own `--all` run REFUSES
  `pin-disposition-stale` until this entry is deleted, which is the mechanism
  working."* Measured on #434's head: exactly that refusal, exit 2.
* **It PROMOTES the retitle that entry was granted for.** The archived packet's
  `## MODIFIED "Bounded autonomous surface"` block lands in codexFactory's
  `openspec/specs/merge-master-approval/spec.md`, replacing canon's single
  scenario *"A human-authored pull request is never auto-approved"* with *"A
  human-authored pull request is never approved by tier 1 alone"* and *"A
  gate-integrity path is never approved autonomously"*. Two still-ACTIVE
  changes — `extend-merge-master-envelope-to-floor-bot-lanes` and
  `relocate-review-authority-floor` — hold their own `## MODIFIED` block for
  that same requirement, each written against canon as it read BEFORE, so each
  now omits two scenarios canon carries.

**AND THIS SECOND HALF IS A CLASS THIS PIN HAS NEVER CARRIED.** Every entry in
the list until today is MARKER-BLINDNESS: a change DECLARED a retitle with the
reserved ``**Merged into `<destination>` by <change-id> (<date>):**`` marker and
1.12.0 cannot read the marker. **Neither of these two blocks carries a marker,
and neither should.** Neither change performed the retitle; neither has a
deletion to declare. Canon moved underneath them. A `Merged into` citation in
either entry would be a claim about a paragraph that is not in the block and
does not belong in it — which is why the pin's own header prose is rewritten
here into two declared classes rather than left saying *"EVERY ENTRY BELOW IS
THE SAME DISAGREEMENT, five times"*, a sentence these two entries falsify.

**The tool's own remedy is what this packet refuses, and the refusal is the
convener's, not this lane's.** Copying the two new scenarios into either block
today would make a ratified packet restate a requirement it does not govern and
was never reviewed against. Brett Heap ruled the order instead — verbatim
***"This change first"***, codexFactory
`hermes/domain/review-councils/records/2026-09-11-gate-rules-provenance-axis-declaration.md:656-659`,
§ 8 — so each sibling re-derives its block against the archived canon before its
own archive, and each re-derivation RETIRES its entry here. **These two entries
are written to be SHORT-LIVED**, which is what separates them from the four
above: nothing in either is a declared rename to be preserved, only a delta
waiting its turn in a ruled order.

**And the finding is REAL rather than spurious, which is why it is an exception
to ACCEPT and not a defect to argue away.** Promoted `doc-health` § *Currency of
an active change's MODIFIED requirement blocks*
(`openspec/specs/doc-health/spec.md:1597`) is the requirement that DEFINES this
check, and it states that the family *"SHALL read every active change regardless
of its lifecycle standing"* because *"a finding against a draft costs its author
one line — which is the cheapest moment to pay it"* (`:1625`). This packet does
not dispute that. It records that the one line is owed BY THE SIBLING PACKETS,
in an order a convener fixed, and carries the finding until each pays it.

## What Changes

* **One entry is DELETED, whole.** `repo: codexFactory`,
  `item: add-regular-pr-council-clearance`, `path: merge-master-approval/spec.md`.
  Deletion is this file's only form for a retirement — there is no retired
  section and no `retired:` key — and it is the tool's own printed remedy:
  *"delete the entry from `dispositions:` in contracts/openspec-cli-pin.yaml, in
  a change that says the condition is gone."* This change says so.
* **Two entries are ADDED**, `repo: codexFactory`, both
  `path: merge-master-approval/spec.md`, for
  `extend-merge-master-envelope-to-floor-bot-lanes` and
  `relocate-review-authority-floor`, each carrying the finding's WHOLE message
  text, a `why:` that says what moved and why copying the scenarios in today
  would be wrong, a non-empty `cited_to:` (eight and nine), Brett's word, and a
  `retires_when:` naming the sibling's re-derivation OR its archive, plus the
  live second staleness condition measured below.
* **`relocate-review-authority-floor` now carries TWO entries in this pin**,
  under two different delta paths, in two different classes, retiring on two
  different events. The second entry names the first so no reader takes one to
  cover the other, and the tests are re-keyed to the `(repo, item, path)` triple
  because an item-keyed map cannot tell them apart.
* **The pin's prose is made true again, and one class is declared for the first
  time.** The rollback note's count moves five -> six; a NEW dated 2026-09-11
  paragraph records how the fourth and fifth findings arrived and that they are
  not marker-blindness; the block above `dispositions:` becomes TWO CLASSES and
  two groups; and a dated retirement note is added BENEATH the 2026-09-05
  comment block, which is itself left exactly as its own change wrote it — it is
  a dated record of what arrived that day and stays true of that day.
* **The count-pinning test moves 5 -> 6, deliberately and visibly**, by one
  deletion and two additions, and its docstring reads the movement. Its
  per-repository split is KEPT.
* **The citation test is TIGHTENED in three ways and loosened in none.** Its
  maps are re-keyed to the triple; a class map asserts the reserved-marker
  citation IF AND ONLY IF the entry is marker-blindness; and the authority is
  read through both spellings the verifier has always admitted, with a NEW
  assertion that exactly one stands. The old test indexed `entry["ratified_by"]`
  directly and would have raised `KeyError` on the first `recorded_by:` entry —
  a grammar `scripts/validate-openspec-cli-pin.py` has accepted since the bump —
  so reading both is a CORRECTION, not a relaxation. The SPELLING is
  deliberately not pinned per entry: a convener's upgrade from the weaker
  authority to the stronger must cost one key name in the pin and nothing else.
* **No spec delta.** See *Capabilities*.

## Capabilities

**`neutral-product-pin` — exercised on BOTH clauses, extended on neither.** The
requirement *"A dispositioned finding is cited, upgrade-coupled, and refused
when stale"* is promoted at `openspec/specs/neutral-product-pin/spec.md:577` and
already states every property this packet relies on:

| property this packet needs | where promoted canon already states it |
| --- | --- |
| a disposition is scoped to one repository | "A DISPOSITION IS SCOPED TO ONE REPOSITORY… a disposition SHALL name the repository whose corpus it is about" |
| an entry for another repository is out of scope and never stale here | "…and a run over any other repository SHALL neither apply it nor treat it as stale"; scenario *"A consuming repository runs the same pin over its own tree"* |
| a consumer's entry retires when its finding stops occurring | "A DISPOSITION MATCHED BY NO FINDING IN A WHOLE-CORPUS SCAN SHALL REFUSE THE RUN"; scenario *"A dispositioned finding stops occurring"* |
| the entry carries the owner's word and a citation | "SHALL carry a non-empty CITATION… and SHALL name the authority that granted it" |
| either authority spelling, exactly one | `scripts/validate-openspec-cli-pin.py` `DISPOSITION_AUTHORITY = ("ratified_by", "recorded_by")`, refusing `pin-disposition-malformed` when neither is present |

**So this packet adds no rule and writes no delta**, and says so in the
machine's own grammar: `.openspec.yaml` declares `skip_specs: true`, the escape
1.12.0 reads at `dist/core/change-metadata/schema.js` and honours in
`openspec validate --strict`. The retirement clause has never fired across a
repository boundary before; firing a clause is not widening it. `design.md` § 3
records the criterion and the reading, and § 5 records what was refused.

## Impact

* **codexFactory's `validate` can go green on #434's tree** the moment its
  declared openxFactory pin resolves a pin file carrying this change: measured,
  exit 0 with `Totals: 33 passed, 3 failed (36 items)` unchanged, 4 applied, `0
  UNDISPOSITIONED failures`, printed on every run.
* **openxFactory's own gate is unchanged and must stay so.** Measured with the
  gate's literal invocation: exit 0, its own two applied, all four codexFactory
  entries neither applied nor stale.
* **THE ORDER BETWEEN THE TWO REPOSITORIES IS FIXED BY MEASUREMENT AND IS NOT A
  PREFERENCE.** On codexFactory `main` (`3c31a2e4`), where #434 is still OPEN,
  canon still carries the OLD scenario title, the pinned CLI words the finding
  differently, and BOTH new entries match nothing: this pin REFUSES
  `pin-disposition-stale`, exit 2, where the pre-edit pin exits 0. **So
  codexFactory's declared openxFactory pin MUST NOT advance to this change's
  merge commit before #434 merges.** The advance and the archive land together
  or the archive lands first; never the advance alone.
* **Still owed after this lands** — named so nobody reads it as done:
  * **codexFactory's declared openxFactory pin advance**, to a commit AT OR
    AFTER this change's merge. **Brett Heap ruled 2026-09-12T03:04:29.167Z that
    lane `codeXfactory-1` carries it** (*"codeXfactory-1 carries it"*), sequenced
    after that lane's **#435 → #433**, so the order is #435, then #433, then
    `advance-openxfactory-pin-<S>`, then — together with it or after it —
    codexFactory #434. It is codexFactory's act in codexFactory's own pull
    request and is not ridden on this diff.
  * **The two sibling re-derivations.** Each is its own packet's act, in
    codexFactory, under the convener's *"This change first"* ordering. Each
    retires its entry here and, on that day, codexFactory's `--all` REFUSES
    until the entry is deleted. **Nobody should be surprised by that refusal**:
    it is this same mechanism, working, and both `retires_when:` fields say so.
  * **The watch on `Fission-AI/OpenSpec#1793`.** Filed 2026-09-05, not fixed.
    When a release honours a declared rename, the next pin bump re-derives the
    list against it, the marker-blindness entries are matched by nothing, and
    the pin REFUSES until every one is deleted. That is the intended retirement
    path for the FIRST class and nothing written here is meant to survive it.
    **It does not reach the SECOND class**: these two entries do not exist
    because of marker-blindness and an upstream marker fix would not retire
    them. Only the re-derivations will.
