# Tasks: require-adjudicated-validation-entrypoint

Status: ratified
Ratified by: require-adjudicated-validation-entrypoint — 2026-09-22, Brett Heap, "ratify #1140 and #1141" at head `c36ff08c` (record `review/ratification-2026-09-22.md`)
Kind: tasks

`code_surface: none`, `target_release: implemented`. **There is no realization
group.** The one enforced corpus-wide gate in this repository already names the
entrypoint (`.github/workflows/openspec-cli-pin-gate.yml`:101), so the rule this
delta states is already true of the gate; what it adds is that a written
ASSERTION must name it too. Under `release-realization` an empty code surface
archives ON LANDING plus this task list rather than on merged-plus-green
realization evidence.

**NOTHING IS TICKED THAT DID NOT LAND.** **§ 1 IS COMPLETE**: ratification was
given 2026-09-22, and the word that settled the BOX (`5778397686`) and the word
that ratified this PACKET (`5779511063`) are two separate acts, both Brett
Heap's. **§ 4 (archive) stays entirely open**: ratification authorizes
realization and does not perform it.

## 1. Ratification — GIVEN 2026-09-22, at head `c36ff08c`

- [x] 1.1 **RATIFIED 2026-09-22 by Brett Heap** (openxFactory operator
      authority), interactive in the lane session, verbatim **"ratify #1140 and
      #1141"**, at **2026-09-22T15:45:54Z**, recorded at `#656` comment
      `5779511063`. The MEASUREMENT was accepted at `5778300335` and the
      PARTICULAR box was ruled at `5778397686`; **this word ratifies the GENERAL
      rule this packet states from that particular**, which is a separate act and
      Brett Heap's, not this lane's. Record:
      `review/ratification-2026-09-22.md`. `Status:` moved in `proposal.md`,
      `design.md` and this file in one commit. **The word named head `c36ff08c`
      and no commit moved this packet between the word and the record.**
      **Ratification authorizes realization and does not perform it**: nothing is
      promoted until the archive, § 4.
- [x] 1.2 **THE DECISIONS BEYOND THE RULED WORD WERE CARRIED BESIDE THE WORD,
      declared for a veto and not vetoed.** `design.md`
      D1 (the rule reaches the ASSERTION and not only the run — with the test of
      the contrary reading written out), D2 (`## ADDED` rather than a `##
      MODIFIED` fold into the PATH requirement), D3 (staleness carried as a
      scenario that defers by name rather than re-legislated), D4 (no checker
      proposed, and why), D5 (the upstream fix registered, never proposed). Each
      is separable and each carries its own veto cost.

## 2. The delta — LANDED IN THIS PULL REQUEST

- [x] 2.1 **ONE `## ADDED` REQUIREMENT in `neutral-product-pin`**, five
      scenarios. **No existing requirement is modified.**
- [x] 2.2 **THE BOUNDARIES ARE IN THE NORMATIVE TEXT.** The obligation reaches
      the written assertion as well as the run; a NARROWED claim about one
      change is explicitly not reached; ratified and archived text is explicitly
      not edited by the requirement, its remedy being the reserved `[~]` marker
      its own packet provides.
- [x] 2.3 **THE STALENESS PROPERTY IS CARRIED BY NAME, NOT RE-LEGISLATED.**
      Scenario *A reader asks whether naming the wrapper lowers the bar* answers
      the objection with the entrypoint's own refusals and states in its last
      bullet that these are the standing properties of *A dispositioned finding
      is cited, upgrade-coupled, and refused when stale*.
- [x] 2.4 **README *Active changes* row added** to the **OpenSpec Records**
      block.
- [x] 2.5 **The machine-seeded sweep-ledger row** in
      `tests/sequenced_after/corpus-ledger.yaml`, written by the sanctioned
      `python3 scripts/validate-sequenced-after.py . --seed-ledger` and by no
      hand.

## 3. The measurement — TAKEN, at this packet's own head

- [x] 3.1 **BOTH COMMANDS RUN OVER ONE TREE, and the verdicts are opposite.**
      `python3 scripts/validate-openspec-cli-pin.py --all --no-cache` →
      `Totals: 108 passed, 1 failed (109 items)`, the 1 finding DISPOSITIONED
      and printed by name with its citation and granting authority, **exit 0**.
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` → the same totals
      and the same finding, **exit 1**. The finding is `add-chain-attestation`,
      `ratified_by: 'Brett Heap, 2026-09-05, "take exit 2"'`.
- [x] 3.2 **THE RAW RUN WAS NOT EVEN AT THE PINNED VERSION.** `openspec
      --version` on `PATH` at this workstation reads **1.13.1**; the pin is
      **1.12.0** (`contracts/openspec-cli-pin.yaml`:318). Recorded because it is
      a SECOND, independent ground on which that verdict is not this
      repository's — and because it is exactly the failure the existing
      PATH requirement describes, met in the wild while authoring the packet.
- [x] 3.3 **THE ENFORCED GATE ALREADY NAMES THE ENTRYPOINT.**
      `.github/workflows/openspec-cli-pin-gate.yml`:101 is
      `python3 scripts/validate-openspec-cli-pin.py --all --no-cache`, the
      workflow's sole step. This is why `code_surface:` is `none`.

## 4. Archive — OPEN

- [ ] 4.1 **ARCHIVE ON A SEPARATE WORD.** Run it through
      `python3 scripts/proposal-support.py . archive
      require-adjudicated-validation-entrypoint` in the pinned checkout, never an
      ambient `openspec archive` — which is this requirement's own doctrine
      applied to its own promotion.

## 5. Residue — named, not swept, and carrying the reserved DEFERRED marker

**WHY `[~]` AND NOT `- [ ]`.** Every item here is work this packet will NEVER do,
so a literal `- [ ]` would be a box that can only ever be ticked falsely — and
`archive_change()` refuses an archive on any literal `- [ ]` anywhere in this
file (`scripts/proposal-support.py`:4633, `re.search(r"^- \[ \]", ...)` →
`"change has incomplete tasks"`). The reserved DEFERRED marker is the house form
for exactly this, and it is the same contingency RULED `5778397686` put § 8.9
into. **§§ 1 and 4 keep `- [ ]` deliberately**: those WILL be ticked, by the
ratifying and archiving acts. *(Raised by Copilot `r4073184032`.)*

- [~] 5.1 **NO CHECKER IS PROPOSED, AND THE MEASUREMENT THAT WOULD JUSTIFY ONE IS
      NOT TAKEN** (`design.md` D4). A successor that wants a
      `scripts/validate-*.py` sibling owes two readings first: how many live,
      non-archived assertions the rule reaches, and whether a mechanical reader
      can tell an ASSERTION of a green corpus from a CITATION of this defect —
      this packet's own files contain the raw command as quoted text, and so
      would every future record about it.
- [~] 5.2 **THE EXISTING OCCURRENCES ARE NOT SWEPT.** Non-archived task boxes,
      plans, quickstarts and evidence lines elsewhere in the corpus name the raw
      command. Archived records are frozen and ratified text is amended only by
      its own instrument, so this packet edits none of them and the requirement
      says so in its own body. Whether any LIVE box needs the same `[~]` remedy
      § 8.9 took is a reading for the packet that owns it.
- [~] 5.3 **THE UPSTREAM FIX IS REGISTERED, NEVER PROPOSED** (`design.md` D5).
      The CLI is consumed and never vendored (`package:
      "@fission-ai/openspec"`, `source_repository: Fission-AI/OpenSpec`); the
      pin is `1.12.0` and `1.13.1` is published upstream. A bump is a
      ratified HUMAN-ONLY act owing target-version evidence and a re-derivation
      of every disposition in the same change, and whether `1.13.1` reads the
      marker is UNMEASURED here. **Retiring that class would not retire this
      requirement** — a second disposition class is live in the pin file today.
