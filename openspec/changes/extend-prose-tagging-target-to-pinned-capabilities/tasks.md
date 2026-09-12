# Tasks: extend-prose-tagging-target-to-pinned-capabilities

Status: draft

NO BOX BELOW IS TICKED BY THE FILING PULL REQUEST except the ones in § 2, which
record what that pull request itself did. § 1 needs Brett Heap's word, § 3 is
the later realization pull request, and § 4 is the archive act.

## 1. The ask — Brett Heap's ratification

- [ ] 1.1 **RATIFY or REFUSE the form (D-1):** the marker target may be
  `pinned:<pin-id>/<capability>`, where `<pin-id>` is the stem of a
  `contracts/<pin-id>-pin.yaml` record. For the four affected markers that is
  `target=pinned:openxwallet/openxwallet`. The form needs NO regex change —
  measured against `families.py:1308-1314`.
- [ ] 1.2 **RATIFY or REFUSE the resolution rule (D-2):** the pin id must
  resolve to a pin record this repository carries; the capability segment is
  checked for shape and resolved further ONLY where the pin record enumerates
  capabilities — which none of the six does today, measured. The weakening this
  accepts is stated plainly in D-2 and is worth a veto on its own.
- [ ] 1.3 **RATIFY or REFUSE the stale-target rule (D-3):** when a target
  capability exits the corpus the marker either takes the pinned form or the
  block is unfenced — never silently retargeted, never silently deleted.
- [ ] 1.4 **CONFIRM the realization split (D-5):** one later pull request
  carrying resolver, tests, the four retargeted markers and the `INDEX.md`
  correction together, rather than four separate ones.

## 2. This filing — done by the pull request that carries this file

- [x] 2.1 Packet authored: `proposal.md`, `design.md`, `tasks.md`,
  `.openspec.yaml`, and `## MODIFIED` deltas against `document-lifecycle` and
  `doc-health`. Every document carries `Status: draft`.
- [x] 2.2 Origin declared `kind: ad_hoc` with DRAFTING provenance
  (`proposed_by` / `proposed_on`) and NO approval pair — the lawful unapproved
  shape. The reason names Brett Heap's selection verbatim and its place.
- [x] 2.3 README "OpenSpec Records → Active changes" bullet added.
- [x] 2.4 Per-change sweep-ledger row seeded by
  `scripts/validate-sequenced-after.py --seed-ledger`, so `--ledger-diff`
  exits 0.
- [x] 2.5 **NOTHING REALIZED.** No byte of `scripts/doc_health/families.py`
  moves. No marker is retargeted or deleted. `ideation/staging/INDEX.md` is not
  touched. `docs/document-lifecycle.md` is not touched. The four `tag-hygiene`
  findings stand at FOUR, unchanged.
- [x] 2.6 **NO BOX ANYWHERE ELSE IS TICKED.** Item (7) of the
  `split-openxwallet-repo` archived-ledger entry (`README.md:6828-6832`) is NOT
  edited by this pull request and no tick is claimed on it; the archived packet
  is not edited at all, under the archived-record rule.

## 3. Realization — a LATER pull request, after ratification

- [ ] 3.1 `scripts/doc_health/families.py`: teach resolution the `pinned:`
  prefix — `_resolve_capability` (line 1317) gains the arm, or a sibling
  resolver is added and `fam_tag_hygiene`'s call sites (lines 1366, 1390)
  dispatch on the prefix. The regexes at 1308-1314 DO NOT MOVE.
- [ ] 3.2 The finding text for an unresolved PINNED target names the pin
  registry, not `openspec/specs/` — the present fixed string
  (`families.py:1367-1368`) is the wrong instruction for this class.
- [ ] 3.3 Tests under `tests/doc_health/`: a resolving pinned target emits
  nothing; an unresolvable pin id emits a finding naming the pin; the pinned
  form on a `supersedes` marker behaves consistently with the candidate arm;
  in-tree resolution is unchanged.
- [ ] 3.4 `docs/document-lifecycle.md` Prose Tagging Markers section: the new
  target form beside the existing `<capability>` bullet, and D-3's
  stale-target sentence.
- [ ] 3.5 Retarget the four markers to `target=pinned:openxwallet/openxwallet`
  — `ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md`
  lines 222, 242, 280 and
  `ideation/staging/notebook-access-wallet-governance/notebook-access-wallet-governance.md`
  line 107. Line numbers re-measured at that branch's tip, never carried from
  here on trust.
- [ ] 3.6 Correct `ideation/staging/INDEX.md:2262-2265`, which still describes
  three `openxwallet` blocks as "all resolving" and has been false since
  2026-08-28.
- [ ] 3.7 Evidence: a `--single-repo` doc-health run over the realization tree
  showing the four `tag-hygiene` findings at ZERO and `New regressions: 0`, and
  the green required `pytest-suite` run, both cited at the TREE grain.

## 4. Archive — a separate act on Brett Heap's word

- [ ] 4.1 Archive via `scripts/proposal-support.py` (never bare `openspec`),
  on merged-plus-green realization evidence per `release-realization`, since
  this packet's `code_surface` is non-empty.
- [ ] 4.2 The archived-ledger entry records that item (7) of
  `split-openxwallet-repo`'s successor register is discharged by this change,
  naming this change id and its realization pull request.
- [ ] 4.3 `openspec/specs/document-lifecycle/spec.md` and
  `openspec/specs/doc-health/spec.md` carry the promoted MODIFIED requirement
  text verbatim, per `promotion-fidelity`.
