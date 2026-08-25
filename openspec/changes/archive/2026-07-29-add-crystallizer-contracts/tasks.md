## 1. Contracts

- [x] 1.1 Add the four record schemas under `contracts/schemas/`
      (`crystallization-decision`, `crystallization-spec`,
      `crystallization-build`, `crystallization-consent`), each with
      `schema_version` + `kind`, the frozen `automation_rung` L0–L6
      vocabulary, the `effect_class` vocabulary, and shape-only posture
      (policy lives in the canonical validator).
- [x] 1.2 Add the additive `omnigent-domain-overlay` schema fields:
      the crystallized worker-class marker block (`crystallized`,
      `capability_ref`, `automation_rung`, `replaces_configuration`,
      `throttle`) and the per-category `rung_ceilings` list — no change to
      the archetype vocabulary or the six-boolean matrix.
- [x] 1.3 Add positive and negative examples per kind — negatives MUST
      include: decision funding above the ceiling, decision without an
      open candidate ref, spend fields on a `not_yet` outcome, spec with
      zero counterexamples, byte-equality golden posing as an equivalence
      predicate, missing effect class, binding whose permissions exceed
      the replaced configuration, crystallized class inventing a sixth
      archetype, EV-rung decision without calibration evidence.
- [x] 1.4 Continue the MVP fixture corpus: a `crystallization_decision`
      (funded, L3, rungs-1–2 ladder), `crystallization_spec` (mined from
      the three packet-capture episodes, incl. the staging-variant branch
      and ≥1 counterexample), scope fence, and the crystallized-executor
      binding for the packet-capture family the ledger already nominates.
- [x] 1.5 Register per the "Contracts Pending Realization" policy:
      contracts/README rows now; manifest + CHANGELOG + version allocation
      at the archive bundle cut. — Rows added 2026-07-29; manifest +
      CHANGELOG + version (contract-v1.20 expected) at archive.

## 2. Validators

- [x] 2.1 Implement `scripts/validate-crystallizer-contracts.py`
      (derived-models/pattern-ledger style: dependency-free, self-testing
      positives + intended-reason negatives): decision evaluation-order
      rule (ceiling present, valuation rows only ≤ ceiling, funded rung ∈
      valuation), only-path-to-spend shape rules, not-yet completeness,
      braid completeness (domain + tenant + consent refs), spec
      counterexample floor, corpus digest pinning, fence presence, effect
      class enum, decision-ladder maturity rule.
- [x] 2.2 Extend `scripts/validate-omnigent-contracts.py`: crystallized
      binding rules (existing archetype only, subset-of-replaced
      permissions and credential families, throttle present, constitutional
      falses untouched) and rung-ceiling shape (category uniqueness,
      L3 default documented).
- [x] 2.3 Validator fixtures/tests wired into the `validate-*.py`
      discipline for both scripts.

## 3. Documentation

- [ ] 3.1 OpenSpec Records entry at raise; doc-index links land with the
      promoted specs at archive.
- [x] 3.2 Update the staging INDEX row/detail on partial promotion (the
      `crystallizer-contracts.md` and `authority-and-consent.md` fragments
      move to `supporting-docs/`).
- [x] 3.3 Record the artifact-residence lean (design doc table) in the
      build contract's guidance section — declared residence required,
      realization per domain. — Recorded 2026-07-29 in the
      crystallization-build schema description.

## 4. Validation and realization evidence

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate add-crystallizer-contracts
      --strict` and `--all --strict` green — verified at raise, ratify, and
      realization (2026-07-29).
- [x] 4.2 Declare staged origin (`openxFactory:staging:recurrence-crystallization`)
      in `.openspec.yaml`; verify the supporting-docs manifest and hashes.
- [x] 4.3 Obtain ratification approval and stamp the proposal front matter
      (`Status: ratified`, `Ratified by:`) — ratified by Brett 2026-07-29.
- [x] 4.4 Realization evidence per `release-realization`: schemas +
      validators merged and green; contract version allocated at the
      archive bundle cut with its annotated tag and release digest
      inventory; archive follows evidence, never precedes it. — Evidence:
      realization commit a06acd4 merged and green (crystallizer 4/9,
      omnigent all green, --all --strict 51/51); contract-v1.20 allocated
      at the 2026-07-29 archive cut with its annotated tag and inventory.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` real line 4 was respelled `Ratified by:` to `Ratified:` by slice
5B of `govern-openspec-corpus-membership` — the prefix only. Every byte after
the colon is carried verbatim, asserted identical at the edit, so the original
line is recovered exactly by reading `Ratified by:` back in its place and
nothing else on the page moved. The ruling is OQ-4's RULED extension of
2026-08-23 (Brett Heap, in-session), which widens the class to the sixteen
lines whose named change id is the DOCUMENT'S OWN. A change is not its own
approving change, and such a line passed `fam_ratified_provenance` only by
self-reference. This one emitted NO finding, so the respell is corrective
rather than a discharge and clears nothing from the census. The record that
justifies this line is Brett's approval of 2026-07-29 named on the line,
recorded by commit `57b5e70` of the same day, "Ratify
add-crystallizer-contracts (Brett, 2026-07-29)", over the
recurrence-crystallization staging decision record D1–D11 + V1–V2 the line
itself enumerates. An append on a single-valued header is mechanically
impossible — `doc_health.corpus.STATUS_RE` swallows any trailing annotation —
so this is an in-place overwrite and an extension of Brett's 2026-08-10 append
ruling, named as one, and it is entered in
`docs/archive-record-discrepancies.md`.

## Bookkeeping annotation — box 3.1 archived open and unannotated (2026-08-25)

No box is ticked here and no task text above is altered. This section records
what this change's own record shows about box **3.1**, which archived as a
bare open box with no reason beside it — the two-line remainder register entry
A4 in `docs/archive-record-discrepancies.md` names, corrected 2026-08-22 by
`archive-register-rulings` when its re-read found that two of A4's six open
boxes carry no annotation at all. The shape is the trailing `##` section and
the discipline is C6's: **annotate, tick nothing**, and assert nothing the
record does not carry.

Box 3.1 reads "OpenSpec Records entry at raise; doc-index links land with the
promoted specs at archive". It is two claims about README bookkeeping, and
this change's own commit history answers both.

**The raise half.** `README.md`'s `## OpenSpec Records` entry for this change
was added by commit `4aaf14dc`, "Raise add-crystallizer-contracts (exit 2 of
recurrence-crystallization)" — the raise commit itself, which is exactly when
the box says it should land. The entry stands today in the `Archived changes`
block, pointing at
`openspec/changes/archive/2026-07-29-add-crystallizer-contracts/proposal.md`.

**The archive half.** The `Crystallizer Contracts` doc-index entry was added
by commit `1ac471f1`, "Archive add-crystallizer-contracts; cut contract-v1.20
(crystallizer promoted)" — the same commit that created this archive folder,
again exactly when the box says. That entry links four promoted specs and all
four resolve in the tree today:
`openspec/specs/crystallization-decision/spec.md`,
`openspec/specs/crystallization-build/spec.md`,
`openspec/specs/crystallization-consent/spec.md`, and the
`openspec/specs/omnigent-domain-overlay/spec.md` this change grew by two
requirements.

**So the box's subject was discharged on schedule and the box was simply never
ticked back.** That is the whole finding, and it is a bookkeeping gap rather
than an evidence gap. The box stays open regardless: Brett's 2026-08-22 ruling
on C6 was to annotate rather than force-tick, this box was recorded rather
than annotated at that round because that ruling named only the four avatar
changes, and closing the gap by ticking now would substitute this annotation's
author for the ratifying record. Nothing above is altered.

The closure of the two-line remainder is appended to A4's entry in
`docs/archive-record-discrepancies.md` under the same date.
