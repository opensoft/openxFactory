---
code_surface: openxFactory and codexFactory, and the split is decided by decision N-1. In codexFactory (a COMPANION change, authored there, not here): a `## MODIFIED` narrowing the PROMOTED requirement `openspec/specs/merge-master-approval/spec.md` § *Bounded autonomous surface*, whose CODEOWNERS-scoped prohibition forbids approving either bot lane's pull request today and which is the load-bearing act of the whole extension; a second candidate class in `.github/merge-approval-envelope.yml`; the enrolled-surface shape assertion in `tests/merge-master/test_enrolled_surface_config.py` that pins it; and an auto-merge arming step in `.github/workflows/floor-regeneration.yml` — because the merge-master lane submits an APPROVE review and never merges, so an approved bot pull request still sits until something merges it. In openxFactory, ONLY IF N-1 is vetoed toward admitting the re-pin lane as well: a second candidate class in `.github/merge-approval-envelope.yml`, its shape assertion in `tests/review_lane_pin/test_review_lane_caller.py`, an auto-merge arming step in `.github/workflows/review-lane-repin.yml`, AND a codexFactory decision-core change carving the floor composition at `.github/workflows/merge-master-approval.yml:1499` for one named candidate. NOT THIS CHANGE'S SURFACE, each for a stated reason: `scripts/merge_master/envelope.py` and `schemas/merge-approval-envelope.schema.json` are NOT modified — the conditions this packet asks for are members the schema and the core already carry, and the packet's whole point is that no new condition member is invented; the two bot lanes' generators, judges and refusals are untouched, because they are the JUDGE of the pull requests being enrolled; and NO floor path is removed from `scripts/merge_master/openxfactory-review-authority-floor.yaml` by any option here, including the vetoed one.
target_release: a code surface, so per `release-realization` it archives only on merged + green realization evidence. The evidence is ONE BOT PULL REQUEST OF EACH ADMITTED KIND LANDED WITH NO HUMAN CLICK — for the recommended scope that is a single codexFactory `floor/bot-regeneration` pull request approved by the merge-master identity, merged by armed auto-merge, with the human's only act being the ratification of this packet and the enabling acts in § 5; for the vetoed-wider scope it is that plus one openxFactory `bot/review-lane-repin` pull request landed the same way. No contract bundle is involved — this packet adds no registered contract row, moves no digest set, spends no `contract_bundle_version` and owes no release tag.
sequenced_after: [mirror-floor-regeneration-automation, codexFactory:add-floor-regeneration-automation, add-substantive-review-lane]
---

# Proposal: extend-merge-master-envelope-to-floor-bot-lanes

Status: ratified
Proposed: 2026-09-07
Ratified: 2026-09-07, Brett Heap (openxFactory repository owner), in session,
verbatim **"ratify 746 and 272 as recommended when green, then land them"** — a
PAIR word given over this packet and its codexFactory companion #272 together,
recorded 2026-09-07T12:32:44Z on openxFactory issue #745 (and on PR #746,
codexFactory #272 and codexFactory #232), applied at head `6ebd7b24` with all
nine checks green and no open thread; record `review/ratification-2026-09-07.md`.
**DECISIONS N-1 THROUGH N-5 STAND AS RECOMMENDED** under that word — N-1 admits
the codexFactory REGENERATION lane only — and none is separately ruled; the owner
may veto any of them by follow-up. **NOTHING IS REALIZED BY THE RATIFICATION** —
it ratifies the PROPOSAL, and realization is a later word.
Origin: openxFactory issue
[#745](https://github.com/opensoft/openxFactory/issues/745) — the governing
issue, carrying lane `openxfactory-2`'s Rule-1 claim — over § 6.3 of BOTH
ratified option-(b) packets, which named this question and expressly refused to
assume it either way. The first-cycle record is codexFactory issue
[#232](https://github.com/opensoft/codexFactory/issues/232).

Authored: 2026-09-07, lane `openxfactory-2` (display `openXfactory-2`), on Brett
Heap's word in session, 2026-09-07 ~02:05Z, a multiple-choice ruling on this
lane's open questions, verbatim option chosen: **"Propose the extension now"**.
**THE WORD AUTHORIZED THE PROPOSING, NOT THE CONTENT. RATIFICATION IS OWED AND
IS BRETT HEAP'S ACT**; nothing below is ratified by being authored, no
requirement here may be cited as approved until he rules on this packet itself,
and **NOTHING IS REALIZED** — this packet enrols no candidate, edits no
envelope file, changes no floor, moves no pin, adds no workflow step and ticks
no box. Every judgment this authoring session took is listed under
§ Authoring decisions rather than presented as settled.
**Ratified 2026-09-07 — see `Ratified:` above; the paragraph above is kept as the
record of the packet's state at authoring.**

## Why

The two option-(b) bot lanes are realized and have run. One complete cycle was
observed on 2026-09-06/07 and is recorded on codexFactory #232: the codexFactory
regeneration lane opened `floor/bot-regeneration` pull requests
[#248](https://github.com/opensoft/codexFactory/pull/248) (merged `7f147070`),
[#254](https://github.com/opensoft/codexFactory/pull/254) (`307d38f1`) and
[#265](https://github.com/opensoft/codexFactory/pull/265), and the openxFactory
re-pin lane opened `bot/review-lane-repin` pull request
[#732](https://github.com/opensoft/openxFactory/pull/732) (`9ffc6252`). Three
defects were found BY RUNNING and fixed (codexFactory #252 `91fc95f5`, #260
`f430cf7e`; openxFactory #726 `0f9361e0`). The lanes work.

What they did not remove is the human. Every advance of the pinned decision core
costs **two human merges**, one in each repository, and the cycle is hourly.
Both ratified packets kept the human word as the DEFAULT and named the question
of removing it as a separate, unruled box — `openspec/changes/mirror-floor-regeneration-automation/tasks.md`
§ 6.3 and codexFactory `openspec/changes/add-floor-regeneration-automation/tasks.md`
§ 6.3 — recording, as the ground that would have to be answered, that
`contracts/review-lane-pin.yaml` is itself a never-clearable floor entry whose
stated reason is that a clearable pin *"would let a pull request choose its own
judge"*.

This packet answers that question with what the tree actually says, and the tree
says something neither the § 6.3 framing nor this packet's own first draft
anticipated. **The objection is not a paragraph to be argued with. It is running
code and ratified canon, in four independent places.** Two of them refuse the
re-pin lane today regardless of what any envelope declares, and one of them —
codexFactory's PROMOTED requirement *Bounded autonomous surface*, which forbids
autonomous approval on any CODEOWNERS-scoped path and was reaffirmed as absolute
eleven days ago — refuses **both** lanes. § 2 of `design.md` measures all four
and cites each one.

So the honest headline is a correction: **neither lane is a configuration
change.** Admitting either one requires a `## MODIFIED` to a promoted requirement
the estate has just re-declared absolute, and what is bought is one human click
per cycle per lane. The recommendation that survives the measurement — admit the
codexFactory regeneration lane, leave the openxFactory re-pin lane on a human
word — weakens ONE governance ground rather than two and needs no decision-core
carve. Whether even that trade is worth taking is a real question and is put as
N-1 (d); and N-1 (e) records the one option that buys the click without weakening
any ground at all.

## What changes

- **A neutral rule for enrolling a machine-derived lane.** `roles-authority-model`
  gains the requirements that make "which lane may be autonomously approved" a
  declared, measured, per-lane act rather than a property of an author identity:
  enrolment is per lane and per surface; a never-clearable floor member is never
  autonomously approvable whatever an envelope says; a lane that writes the
  artifact selecting its own repository's judge is enrolled only behind a named
  safeguard set; and every enrolled lane carries a one-edit kill switch.
- **The two floor bot lanes, named.** `review-lane-floor-mirror` gains the
  requirements that fix each lane's admission conditions as MEASURED facts —
  the exact author, the exact head ref, the exact writable path set, all judges
  green — and the ordering property that a re-pin is never approved against a
  core that is not codexFactory's default-branch head.
- **Nothing is enrolled by this packet.** The enrolment itself is realization,
  and realization is a later word.

## Impact

- Affected specs: `roles-authority-model` (ADDED), `review-lane-floor-mirror`
  (ADDED).
- Affected code, on realization only: codexFactory
  `.github/merge-approval-envelope.yml`,
  `tests/merge-master/test_enrolled_surface_config.py`,
  `.github/workflows/floor-regeneration.yml`; and, only under a veto of N-1
  toward the wider scope, the openxFactory counterparts plus a codexFactory
  decision-core change. Itemized with its cost in `design.md` § 6.
- Owner's acts that no agent may perform, listed in `tasks.md` § 5: the
  ratification; the ruling on N-1 through N-5; and the enabling acts — a code
  owner review accommodation in each repository whose paths are code-owner
  gated, without which an envelope approval changes nothing at all.
