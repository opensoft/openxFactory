# Tasks: amend-home-adapter-scope-and-mapping-axis-count

Status: draft
Kind: tasks

## 1. Ratification

- [ ] 1.1 Brett Heap's word on the `corpus-adapter-seam` scope amendment.
  **THE QUESTION IS WHICH REMEDY, NOT WHETHER.** Copilot `r4067852518` named two
  and the archiving lane confirmed the defect real at `#1139` comment
  `5770749761`: *"the packet never says which wins. Real, and not resolvable by
  reading."* This packet takes the NAMED-EXCEPTION form for the reason at
  `design.md` D1 — a general "externally consumed" scoping would make the
  requirement's own third scenario unreachable. The alternative remains one edit
  away.
- [ ] 1.2 Brett Heap's word on the `domain-mapping-declaration` axis count.
  Same shape: `r4067955892` named two remedies — define the nesting, or revise
  the list. This packet revises the list, because the realized profile and
  `DomainProfile` both already carry the field as a sibling of the five
  (`design.md` D2), so nesting it would make the estate's one realized
  declaration non-conformant in order to repair a text defect.
- [ ] 1.3 On the word: `Status: ratified` + `Ratified:` in `proposal.md`,
  `Ratified by:` in `design.md` and this file, the `approved_by`/`approved_on`
  pair in `.openspec.yaml` (the `proposal-origin` check REQUIRES the pair the
  moment the status claims approval — `scripts/doc_health/proposal_origin.py`
  lines 103-110, 339-350), a record under `review/`, and the README Records row
  moved with it.

## 2. The two deltas

- [x] 2.1 `specs/corpus-adapter-seam/spec.md` — ONE `## MODIFIED` requirement.
  The external-product clause gains a NAMED, BOUNDED exception for the home
  adapter RULING DQ-1 keeps, deferring its obligations to requirement 4 and to
  `openxfactory-engineering-adapter`; the one-way dependency rule, the
  relocation rule and the measured back-edge instance are carried unedited.
  THREE promoted scenarios carried byte-identically, TWO added: the home adapter
  measured against the rule, and a second in-repository reader refused the
  exception.
- [x] 2.2 `specs/domain-mapping-declaration/spec.md` — ONE `## MODIFIED`
  requirement. `exactly five axes` becomes `exactly six`, the sixth named as the
  DERIVED-MODEL BOUNDARY with its content deferred to the requirement that
  states it in full, plus one sentence settling which of the finding's two
  readings is right. THREE promoted scenarios carried byte-identically, ONE
  added: a declaration carrying five axes and no derived-model boundary is
  reported as a MISSING AXIS rather than as a forbidden sixth.
- [x] 2.3 Neither block reaches any other requirement in either spec. Requirement
  3 of `domain-mapping-declaration` — the one that MANDATES the sixth axis — is
  not edited: this packet adds no obligation, it names one the corpus carries.

## 3. Measurement (each re-runnable, each taken on `main` `4f92d651`)

- [x] 3.1 The home adapter is neither external nor pinned:
  `scripts/corpus_adapter_openxfactory/` exists in tree;
  `grep -rn "corpus_adapter" contracts/` returns nothing.
- [x] 3.2 It imports this repository's own tooling at EIGHT sites — `doc_health`
  six times across four modules (`adapter.py:58`, `check.py:39`, `:40`, `:41`,
  `classify.py:38`, `home.py:59`) and `ideation_dashboard.intent_apply_lane`
  lazily twice (`write_path.py:134`, `:152`) — so pinning it would violate the
  requirement's SECOND clause. The escape clause 1 appears to offer is closed by
  clause 2.
- [x] 3.3 Nothing in running code enforces requirement 1:
  `grep -rIn "corpus-adapter-seam" scripts/ tests/ contracts/ .github/` returns
  ten lines and every one names requirement 3 or requirement 4.
- [x] 3.4 The realized declaration carries SIX:
  `contracts/domain-profiles/openxfactory-engineering.yaml` `AXIS 1`..`AXIS 5`
  banners at :76, :146, :360, :395, :405, then `truth_store:` at :415 under no
  banner, `external_enforcement_point:` nested at :417.
- [x] 3.5 Nothing counts axes: no `scripts/` or `tests/` file enumerates the
  declaration's axes or asserts their number.
- [x] 3.6 No active change carries a delta on either capability
  (`openspec/changes/*/specs/` enumerated), so no basis marker is owed.

## 4. Gate

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate amend-home-adapter-scope-and-mapping-axis-count --strict`.
- [x] 4.2 `python3 review/verify-carriage.py` — re-extracts both promoted
  requirements' scenarios from `openspec/specs/` and compares them to the
  blocks. Committed with the packet so the proof survives later edits.
- [x] 4.3 `validate-code-surface.py`, `validate-target-release.py`,
  `validate-sequenced-after.py`.
- [ ] 4.4 Required checks green at the head, Copilot review at the exact head
  read for its "Suppressed comments" block, every thread resolved.
- [ ] 4.5 The ledger row seeded with `--moved-by` once the pull request has a
  number.

## 5. Registered, not taken

- [~] 5.1 `contracts/domain-profiles/openxfactory-engineering.yaml`'s `basis:`
  entry cites the delta at its PRE-ARCHIVE path
  (`openspec/changes/split-opendox-two-layer-product/...`), which the 2026-09-22
  archive moved, and describes it as *"the five axes"*. The count is accurate as
  a description of what that delta said. The stale path is the archive's residue.
  Both are left: a contract edit would give a doctrine-only packet a code surface
  for a citation this amendment did not make stale. **Owed to whoever next opens
  that file with a code surface already declared.**
- [~] 5.2 `README.md`:3270 reads *"`domain-mapping-declaration` (3 requirements:
  the five axes ...)"*. In place it is the ARCHIVE RECORD's narrative of what
  `split-opendox-two-layer-product` promoted, and as a record it stays accurate.
  Registered so a reader who takes it for a live capability description finds the
  question already asked.
- [~] 5.3 The `openxfactory-engineering-adapter` capability's `## Purpose`
  already states the home adapter is *"one implementation among others with no
  privileged route to its home corpus"* under the seam's FOURTH requirement. It
  does not state the FIRST requirement's exception, because that exception did
  not exist when it was promoted (2026-09-18, `repromote-engineering-vocabulary`).
  Nothing there becomes false when this lands — it never claimed the adapter was
  pinned — so no delta on it is owed. Registered because the next author of that
  capability should know the seam's requirement 1 now names it.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
