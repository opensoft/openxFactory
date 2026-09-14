# Ratification — 2026-09-05

Status: ratified
Ratified: 2026-09-05 by Brett Heap — verbatim "ratify 697", recorded below
under "Authority, and the two words".

## Decision

RATIFIED by Brett Heap.

## Authority, and the two words

Brett Heap's instruction, verbatim: **"ratify 697"** — given 2026-09-05, in his
own message, first-hand to Claude session `codeXfactory-1`
(https://claude.ai/code/session_01PXKjHRwEhuHDBwFixetmtT), lane
`codexfactory-1`, which authored this packet and writes this record.

**IT IS THE SECOND WORD THIS PACKET CARRIES, AND THE TWO DO DIFFERENT WORK.**
The first, also 2026-09-05 and also first-hand to this lane, is
**"use recommended name, go on 3 repo shape"**. That word settled the PLAN:
that codexFactory takes the same exit openxFactory took for its own pair —
declare the rename with the marker canon reserves for it and disposition the
residual finding, rather than copy the superseded scenario back — and that the
realization runs in three steps, of which this packet is step 2. The packet has
said since it was written that the plan-level word *"does not ratify this
packet's text, which carries `Status: draft` and owes a ratification citation
from a separate act"*. **"ratify 697" is that separate act.** Plan accepted
then; text ratified now. Same operator, same day, two decisions, both recorded
because both happened.

## What this ratification covers

The change as committed at **`bfc9451e`**, the head this word was given
against:

* **The four-entry disposition list** in `contracts/openspec-cli-pin.yaml` —
  specifically the TWO entries this packet adds, both `repo: codexFactory`,
  against `add-regular-pr-council-clearance` /
  `merge-master-approval/spec.md` and `amend-composition-selector-labelling` /
  `domain-hermes-content/spec.md`, each accepting one ERROR-level finding by its
  whole message, with six and seven citations. openxFactory's own two entries
  are untouched by this packet and are ratified by **"take exit 2"** (#677),
  not by this word.
* **The delta-less shape.** `.openspec.yaml` declares `skip_specs: true` and
  the packet writes no spec delta, on the reading recorded in `design.md` § 4:
  `bump-openspec-cli-pin-to-1.12`'s ADDED requirement already states that a
  disposition is scoped to one repository, that an entry naming another is
  neither applied nor stale, and that an entry refuses when its change archives.
  This is the first use of `skip_specs` in this corpus.
* **The corrected exit-3 record.** Three places in this packet said exit 3 was
  unfiled; it was filed 2026-09-05 as `Fission-AI/OpenSpec#1793` and recorded by
  #682 (`ff31fc7f`). Commit `bfc9451e` corrected all three, and corrected one
  leftover of the same error in #677's own README entry.
* **The measured claims** in `evidence/codexfactory-dispositions-2026-09-05.md`,
  including the property this packet exists to prove: the codexFactory entries
  are APPLIED on codexFactory's tree and are neither applied nor stale on
  openxFactory's.

## Order of events

1. The packet was authored and pushed by lane `codexfactory-1` on 2026-09-05 as
   openxFactory **#697**.
2. Every required check went green on `bfc9451e` — `pytest-suite` (23m17s),
   `openspec-cli-pin`, `merge-master-approval`, `signed-execution-chain-gate`,
   `clearing-dispatch-gate`, `wallet-validation`, `openreposhape-pin`,
   `release-tag-gate`, `lane-line`.
3. Brett Heap gave **"ratify 697"**.
4. This record was written, on the branch, AFTER that green run and BEFORE any
   merge.

**THE MERGE HAS NOT HAPPENED AND IS NOT AUTHORIZED BY THIS WORD.** It follows on
a separate merge word, performed by the orchestrator. This differs deliberately
from #677, whose record notes that the merge preceded the record on Brett's word
in the authoring lane; here the record precedes the merge, so nothing about #697
is ratified-in-fact ahead of being ratified-in-writing.

## Limits — what this word does NOT ratify

* **Step 3, `adopt-openspec-cli-pin-gate` in codexFactory.** The gate leg that
  runs `scripts/validate-openspec-cli-pin.py --all` in codexFactory CI is not in
  this packet and is not ratified here.
* **The `stack.yaml` re-pin and the aggregation pointer advance.** codexFactory
  must re-pin to an openxFactory commit AT OR AFTER this change's merge — an
  earlier pin resolves a pin file without these entries — and the xFactory
  aggregation's submodule pointer moves separately. Neither is this word's.
* **The ticks of `add-openspec-cli-pin` task 6.1 and
  `bump-openspec-cli-pin-to-1.12` task 6.3.** Both describe the WIRING, which is
  step 3. They stay unticked, and this ratification does not tick them.
* **The archive of this change**, or of any change named in its dispositions.
  `add-regular-pr-council-clearance` and `amend-composition-selector-labelling`
  remain `Status: draft` in codexFactory; each entry's `retires_when:` says what
  happens on the day they archive.
* **The watch on `Fission-AI/OpenSpec#1793`.** Filed is not fixed. If a later
  release honours a declared rename, all four dispositions go stale at the next
  pin bump and the pin refuses until every one is deleted. Nobody owns noticing
  that yet; `tasks.md` 5.5 is the open box that says so.
