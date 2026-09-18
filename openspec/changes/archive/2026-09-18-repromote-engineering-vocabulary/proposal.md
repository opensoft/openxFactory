---
code_surface: none — MEASURED on a fresh clone of `main` at `fa39141c`, not assumed. This packet's whole diff is corpus text: its own six files (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, ONE `## ADDED` spec delta, and `review/build-delta.py` — the one-shot authoring-and-verification helper that BUILDS that delta and proves the carry, committed inside the packet so the proof is reproducible from this checkout alone; it sits under no import path, is not under `scripts/` or `tests/`, is read by no gate, and runs only when a human runs it), one README *Active changes* bullet, and the machine-seeded per-change row in `tests/sequenced_after/corpus-ledger.yaml` that every filing owes. Evidence for the negative: (1) NOT ONE BYTE of `scripts/corpus_adapter_openxfactory/`, `scripts/corpus_adapter.py`, `scripts/ideation_dashboard/`, `scripts/doc_health/`, any other file under `scripts/`, or any file under `tests/` other than that generated ledger is edited, added or deleted — the fifteen requirements are CARRIED text, and the code that will have to satisfy them is the shed-and-floor work of `split-opendox-two-layer-product` § 5.2, § 5.4 and § 5.5, each with its own box and its own code surface; (2) nothing under `contracts/` moves — no schema, no pin record, no digest, no `contract_bundle_version`, no `contracts/CHANGELOG.md` line and no release tag is owed; (3) no workflow, no validator and no gate changes, and no byte of `openspec/changes/split-opendox-two-layer-product/` is touched — no tick, no map row, no design line; (4) nothing under `openspec/specs/` is edited: this packet's delta is a change-packet delta that reaches canon only at its archive. There is nothing left to build after this pull request lands, which is the test `release-realization`'s archive gate applies to an empty code surface.
target_release: implemented — the doc-only pair `release-realization` names (`code_surface: none`, `target_release: implemented`), on the openxFactory main line. No contract bundle is cut and no number is allocated.
sequenced_after: []
---

# Proposal: repromote-engineering-vocabulary

Status: ratified
Ratified: 2026-09-18 by Brett Heap (openxFactory operator authority), by interactive multi-choice (four questions, the recommended option each time) — recorded at [openxFactory #656, comment 5728607038](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5728607038), ruling **R-A**: *"§ 5.2a — `repromote-engineering-vocabulary` is RATIFIED"*.
Proposed: 2026-09-16, in lane `openxfactory-4` (display `openXfactory-4-openDox_extraction`), actor `substrate52a`, as the realization of `split-opendox-two-layer-product` **§ 5.2a** (`tasks.md` :1527-1535). CLAIMED on openxFactory issue #656, comment [`5703096449`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5703096449), after the three sibling reads lane-collision-protocol Rule 1 requires.
Origin: `openxFactory:adhoc:2026-09-16-repromote-engineering-vocabulary` — a BOX of an active ratified packet, not an `ideation/staging/` topic. FILING IS NOT RATIFYING: this packet carries `Status: draft` on all three lifecycle documents, admits no text to canon, and performs neither ratification nor archive. Both are later acts on Brett Heap's word.

## Why

**RULING DQ-1 (2026-09-04T22:14Z, `#656` comment `5547049745`) kept fifteen requirements in this
repository, and nothing has yet given them a home to be kept IN.** The ruling settled the
disjunction RULING C2 left open — *"openxFactory keeps its own adapter … `codexDox` becomes a thin
descendant that pins openXdox and reuses that adapter"* — and its first encoded consequence is that
the fifteen engineering-vocabulary rows STAY HERE. They still leave the CAPABILITY: `ideation-dashboard`
exits whole under `split-opendox-two-layer-product`, all 102 of its requirements, and the packet's
ratified per-requirement map assigns each one a destination — **71 openDox / 16 openXdox / 15
openxFactory**. For the fifteen the map says, fifteen times and in the same words, that the
requirement *"is re-promoted in `openxFactory`'s own corpus under that adapter's successor
capability, **whose id the realization authors** (`tasks.md` § 5.2a)"*.

**That id is this packet, and FOUR live dependents are blocked on it — two boxes and two open closures.** § 5.6's de-floor and
§ 8.4's both-directions floor accounting both have to name the capability directory that appears
under `openspec/specs/`; and two § 6 closures already in flight named the gap in terms while
declining to guess at it — § 6.1 (`#1060`) carried seven doc-health requirements into openXdox
byte-identical rather than re-author them against *"the successor capability id … § 5.2a, unbuilt
and assigned to another actor"*, and § 6.5 (`#1065`) carried its delta whole for the same reason.
Authoring against an undeclared capability is authoring on sand; this packet declares it.

**And the fifteen must not be left to fall out of canon while that is settled.** They are ratified,
promoted requirements today. The packet that removes them is ACTIVE and its archive gate (§ 8) is
distant. If the removal ever lands without this re-promotion, fifteen ratified requirements leave
canon with nothing recording where they went, and `promotion_fidelity.py` — which keys on
(capability, normalized title) — would have no successor key to find them under.

## What Changes

**ONE `## ADDED Requirements` block, under ONE new capability, carrying the fifteen.**

* The successor capability is **`openxfactory-engineering-adapter`**. The id is DERIVED — from the
  packet's own name for the thing, in the ratified map (15/15 rows: *"openxFactory's OWN ENGINEERING
  ADAPTER, the small package beside `scripts/doc_health/` that implements openDox's corpus-adapter
  seam"*), from `design.md` § D3's column head and § D1's topology block, and from the two LANDED
  machine names that fix its spelling (`scripts/corpus_adapter_openxfactory/`, sole public class
  `OpenxFactoryCorpusAdapter`, #725 → `ea4e6ff2`; and `contracts/domain-profiles/openxfactory-engineering.yaml`'s
  `mapping_id: openxfactory-engineering`, #984 → `a1ef886f`). `design.md` § D1 records the
  derivation and the four rejected candidates with their reasons.
* The fifteen are **CARRIED, not authored**: lifted from `openspec/specs/ideation-dashboard/spec.md`
  BY TITLE by a script, with every byte of their promoted text preserved except at the TWO sites
  `design.md` § D2 discloses OLD → NEW, where a path literal becomes the seam operation that answers
  for it — the ONLY edit `tasks.md` § 5.2a permits, and one of the three classes RULING OQ-1's closed
  list names by name (*adapter calls*). The carry is proved mechanically rather than asserted:
  reversing those edits reproduces the promoted bytes exactly, for all fifteen.
* **AND THE COUNT ITSELF IS A FINDING.** Six path-literal occurrences sit in the fifteen; only TWO
  name a question the six-wide seam answers as the requirement states it, and both are `resolve`.
  The other four — a topic's EXISTENCE under staging, the DESTINATION of authoring the console must
  not perform, and twice the workspace returned documents land in — are RECORDED NON-EDITS with their
  reasons in `design.md` § D2, because replacing a literal with prose that names no call is authoring
  rather than re-expressing. What would unblock them (a declared staging scope, or an existence
  answer that keeps *absent* and *empty* apart) is openDox's to declare under RULING Q4 and is carried
  as a BLOCKED box at `tasks.md` § 4.5, in the shape § 6.1 and § 6.5 used for the same class.
* Titles are therefore character-for-character identical to canon's, which is what makes the
  successor a DISTINCT (capability, title) key and keeps the packet's `## REMOVED` delta visible to
  the promotion-fidelity checker — the mechanism `tasks.md` § 5.2a names in its own text.

**This packet authors NO second `## REMOVED` block on `ideation-dashboard`, and that is a declared
judgment rather than an omission** — `design.md` § D3 states it in full. In short: the packet's own
ratified map IS the removal and is its single writer; a sixth live writer on that capability would be
an undeclared sibling collision this box has no authority to declare; and in one of the two possible
archive orders it becomes *"a removal of nothing … applied against a document that never held the
title"*, the defect the packet's own block (b) refuses. The mechanical evidence that the two do not
collide is this packet's own sweep row: `class: sole`, because no requirement key it writes is
written by any other change in the corpus.

## Impact

* **Canon**: one new capability directory, `openspec/specs/openxfactory-engineering-adapter/`, with
  15 requirements and 84 scenarios — created AT THE ARCHIVE, not by this pull request. § 8.4's
  floor accounting and § 5.6's de-floor can now name it.
* **`ideation-dashboard`**: unchanged by this packet, in canon and in the split packet both.
* **Archive order, declared here because it is the one consequence a reader must not discover late**:
  this packet archives BEFORE `split-opendox-two-layer-product`, so that the fifteen are in canon
  under the successor capability at every instant. The reverse order leaves a window in which fifteen
  ratified requirements sit in no capability at all. `tasks.md` § 3 carries it as a box.
* **Between the two archives the fifteen titles are carried by TWO capabilities**, which is the
  intended state and not a defect: the requirement key is (capability, normalized title), the sweep's
  own `class` computation confirms it, and `promotion_fidelity.py`'s latest-writer rule resolves each
  key independently.
* **No gate moves.** No validator, workflow, schema, digest or pin. `openspec validate --all --strict`
  and the house validators are run on this branch and reported in `tasks.md` § 2.
