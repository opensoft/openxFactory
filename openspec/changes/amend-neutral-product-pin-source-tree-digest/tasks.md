# Tasks: amend-neutral-product-pin-source-tree-digest

Status: ratified
Ratified by: amend-neutral-product-pin-source-tree-digest — 2026-09-22, Brett Heap, "ratify #1140 and #1141" at head `ca47e2cb` (record `review/ratification-2026-09-22.md`)
Kind: tasks

`code_surface: none`, `target_release: implemented`. **There is no realization
group, because there is nothing to realize.** The delta is requirement prose; the
behaviour it states has been the real behaviour of
`scripts/verify-opendox-pin.py` and `scripts/verify-openxdox-pin.py` since each
was written, and of the two pin files since they were filed. Under
`release-realization` an empty code surface archives ON LANDING plus this task
list rather than on merged-plus-green realization evidence. **The "realization"
of a wording amendment IS its promotion at archive.**

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box is a diff in this pull
request or a measurement recorded verbatim in its body. § 1 is OPEN: the word
that commissioned this amendment is not the word that ratifies the packet, and
that second act is Brett Heap's. § 4 (archive) stays entirely open.

## 1. Ratification — GIVEN 2026-09-22, at head `ca47e2cb`

- [x] 1.1 **RATIFIED 2026-09-22 by Brett Heap** (openxFactory operator
      authority), interactive in the lane session, verbatim **"ratify #1140 and
      #1141"**, at **2026-09-22T15:45:54Z**, recorded at `#656` comment
      `5779511063`. The CONTENT was already ruled — `5777949892`, **"(b) — AMEND
      THE CLAUSE"** — and this packet encodes that ruling and reaches no judgment
      beyond it; **the ratifying word is a second, separate act and it is Brett
      Heap's, not this lane's.** Record: `review/ratification-2026-09-22.md`.
      `Status:` moved in `proposal.md`, `design.md` and this file in one commit.
      **Ratification authorizes realization and does not perform it**: nothing is
      promoted until the archive, § 4.
- [x] 1.2 **THE DECISIONS BEYOND THE RULED WORD WERE CARRIED BESIDE THE WORD,
      declared for a veto and not vetoed.** The
      ruling fixes the OUTCOME (a whole-tree digest is an equivalent discharge)
      and names its ground (the reasoning already in the requirement). It does
      not fix the BOUNDARY sentences, and `design.md` D2 and D3 carry them: D2
      keeps an enumeration lawful and owed where no whole-tree digest is
      recorded, so the amendment admits a second form rather than replacing the
      first; D3 states in the text itself that the equivalence reaches WHICH
      FORM and never WHETHER, and that the runtime-deployment clause is
      untouched. Both are separable and the cost of vetoing either is written
      into D2 and D3 themselves.

- [ ] 1.3 **RE-RATIFICATION AT `9f82caeb` IS OWED, AND THIS BOX IS THE ASK.**
      **RULING NEEDED (Brett Heap).** The word named head `ca47e2cb`.
      `9f82caeb` was committed at **15:45:53Z — one second before the word** —
      and pushed around it, so it was in flight at the moment of ratification and
      **cannot have been read**. It is not cosmetic: it REVERSES the runtime
      exclusion `ca47e2cb` carried, on Copilot `r4073495698`'s measurement that
      the exclusion would have made `contracts/opendox-pin.yaml` — a `migration:`
      block at :190 AND a whole-tree digest with no per-file list —
      **non-conformant**, which is the opposite of what RULED `5768144952`
      settled. **The correction runs in the ratified direction, but it is
      requirement text moved after a ratify word**, and the estate's rule admits
      only NON-NORMATIVE folding after the word. So it is raised rather than
      absorbed. **(a)** re-ratify at `9f82caeb` — REC, the text is more correct
      than the ratified baseline and its defect is measured; **(b)** revert to
      `ca47e2cb`'s exclusion and land the ratified text as it stood, accepting
      that `contracts/opendox-pin.yaml` reads non-conformant against it;
      **(c)** something else. On the word, add a `Re-ratified:` line beside the
      `Ratified:` one in all three files, as `add-chain-attestation` carries.

## 2. The delta — LANDED IN THIS PULL REQUEST

- [x] 2.1 **ONE `## MODIFIED` BLOCK, on *An external neutral product is pinned
      by commit and digest, never by tag*.** One amendment paragraph and FIVE
      scenarios added; **not one character of any unit the requirement already
      carries is edited**, which is what the `modified-block-currency` carriage
      arm reads rather than what this line claims.
- [x] 2.2 **THE BLOCK IS WRITTEN OVER `split-opendox-two-layer-product`'s
      OUTCOME, and says so in the block.** That packet's active block on this
      same requirement was ratified 2026-09-05; its runtime-deployment clause,
      its own per-requirement record and both of its scenarios are carried here
      with the five promoted ones, for **seven carried scenarios and five
      added, twelve in the block**. The ordering is declared by
      `sequenced_after: [split-opendox-two-layer-product]` and by the named
      section in `proposal.md`, which is what the family reads.
- [x] 2.3 **THE BOUNDARY IS IN THE NORMATIVE TEXT, not only in the proposal.**
      The amendment paragraph states that the equivalence is about which form
      the digest obligation takes and never about whether digests are owed;
      that an enumeration stays lawful and stays owed where no whole-tree
      digest is recorded; that the runtime-deployment clause is untouched and
      narrowed in no respect; and that a pin recording NEITHER form has
      discharged nothing. Scenario *The equivalence is cited as permission to
      skip a digest* refuses the misreading directly.
- [x] 2.4 **README *Active changes* row added** to the **OpenSpec Records**
      block, per the corpus's own authoring rule.
- [x] 2.5 **The machine-seeded sweep-ledger row** in
      `tests/sequenced_after/corpus-ledger.yaml`, written by the sanctioned
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
      '#1140'` and by no hand. **ONE row moved, not two**, and the difference is
      recorded rather than smoothed: this change's own row, read `co-modifier`
      because its block writes a requirement key
      `split-opendox-two-layer-product` also writes. **NO PARTNER ROW FLIPPED** —
      the basis at `tests/sequenced_after/corpus-ledger.yaml`:291 was ALREADY
      `co-modifier` before this packet existed, so there was no `sole` to flip.
      *(An earlier draft of this line predicted the flip from the rule rather
      than from the generated diff, and the seeder's own output — `224 rows, 1
      moved by #1140` — is what corrected it. Caught by Copilot `r4073364921`
      against head `4f786903`. **A row count in this line is a reading of the
      diff, never a prediction from the rule.**)*

## 3. The measurement — TAKEN, and recorded in the pull request body

- [x] 3.1 **`code_surface: none` IS MEASURED, NOT ASSUMED.** Neither
      `scripts/verify-opendox-pin.py` nor `scripts/verify-openxdox-pin.py`
      reads `files:` or `pinned_by_commit_only:`; the only two occurrences of
      the latter across both are module-docstring prose about the openXwallet
      pin. Neither closed refusal vocabulary carries a code for a missing
      per-file list. The two verifiers that DO read the key read it with an
      absent-is-empty default, transcribed by `scripts/doc_health/pin_shapes.py`.
- [x] 3.2 **THE TESTED SHAPE IS ALREADY THE WHOLE-TREE ONE.**
      `python3 -m pytest tests/opendox_pin tests/openxdox_pin -q` reads **105
      passed** at this head, over fixtures that build pins from
      `digest_definition` plus `digests.tree_sha256` with no per-file key at
      all. **A pin conformant before this lands is conformant after it.**
- [x] 3.3 **VALIDATION RUNS THROUGH THE PINNED CONSUMER ENTRYPOINT**,
      `python3 scripts/validate-openspec-cli-pin.py`, and not through the
      `openspec` on `PATH` — which at this workstation is **1.13.1** against a
      pin of **1.12.0**, so its verdict would not be this repository's on two
      separate grounds. Counts are recorded in the pull request body.

## 4. Archive — OPEN

- [ ] 4.1 **ARCHIVE ON A SEPARATE WORD.** Promotion writes the amended block
      into `openspec/specs/neutral-product-pin/spec.md`. Run the archive through
      `python3 scripts/proposal-support.py . archive
      amend-neutral-product-pin-source-tree-digest` in the pinned checkout,
      never an ambient `openspec archive`.
- [ ] 4.2 **ORDER AGAINST THE BASIS.** `split-opendox-two-layer-product` is this
      packet's declared predecessor and archives first. Should this packet
      somehow reach archive ahead of it, the promotion would write the basis's
      clause into canon before the basis's own archive did — so the order is
      checked at the archive rather than assumed here.

## 5. Residue — named, not swept, and carrying the reserved DEFERRED marker

**WHY `[~]` AND NOT `- [ ]`.** Every item here is work this packet will NEVER
do — it belongs to another repository, another packet or another act — so a
literal `- [ ]` would be a box that can only ever be ticked falsely, and
`archive_change()` refuses an archive on any literal `- [ ]` anywhere in this
file (`scripts/proposal-support.py`:4633, `re.search(r"^- \[ \]", ...)` →
`"change has incomplete tasks"`). The reserved DEFERRED marker is the house form
for exactly this, and each item names its holder. **§§ 1 and 4 keep `- [ ]`
deliberately**: those WILL be ticked, by the ratifying and archiving acts.
*(Raised by Copilot `r4073184032` against the sibling packet and applied here
for the same reason.)*

- [~] 5.1 **THE openXdox-SIDE HEADER AMENDMENT is a different act in a different
      repository and is NOT this packet's.** `5768144952` registered it: the
      openXdox `contracts/opendox-pin.yaml` header still carries the un-amended
      trigger text at `646f1dc0`, owed to a small follow-up pull request there.
      This packet edits no pin file in any repository.
- [~] 5.2 **THE OTHER TWO PRE-STAGE FINDINGS ARE NOT ANSWERED HERE.** `#1139`
      review `5273796676` registered three; `5777949892` answers only the
      `neutral-product-pin` per-file one, which is this packet. The
      `corpus-adapter-seam` "every tool" finding and the
      `domain-mapping-declaration` five-axes finding remain as the pre-stage
      recommends — left as ratified, registered for a successor amendment
      change. **Naming them here is not adopting them.**
- [~] 5.3 **THE REQUIRED-CHECK REQUIREMENT'S WORDING IS KEYED TO AN ENUMERATED
      PIN, AND THIS PACKET DOES NOT AMEND IT.** Measured on Copilot
      `r4073110728`: the scenario *The pinned reader runs before the pin is
      verified* (`openspec/specs/neutral-product-pin/spec.md`:147-149) conditions
      on "the pin's per-file digests and its `pinned_by_commit_only:` set", which
      a whole-tree pin does not carry. **THE GAP IS NOT CREATED BY THIS PACKET
      AND PREDATES IT**: `contracts/opendox-pin.yaml` and
      `contracts/openxdox-pin.yaml` have carried the whole-tree form since they
      were filed, so the scenario has read this way against live pins all along.
      This amendment makes the form explicitly lawful and therefore sharpens the
      question, which is why it is registered here rather than left unstated.
      **Amending a SECOND requirement is beyond this packet's commission** —
      RULED `5777949892` names one clause — so the remedy is a successor that
      scopes that scenario to the enumerated form or names the whole-tree digest
      beside it. Holder: unassigned; raise with the ruling that commissions it.
