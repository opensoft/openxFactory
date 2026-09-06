# Tasks

**NO REALIZATION IS STARTED BY THE AUTHORING OF THIS PACKET, AND NO BOX IS
TICKED BY IT.** This is a PROPOSAL: groups 2 through 5 are realization work and
begin only after ratification. **Group 1 is the exception and is deliberate** —
it lists the PROPOSAL's own acts, the ones this packet performs, and its boxes
are still unticked, because authoring a proposal is not discharging it and a box
that moved on authorship would be a false completion the moment a ratification
did not follow. Group 6 is the owner's, and its boxes stay unticked even once
taken: an agent may not tick an owner's-act box, so those acts are recorded as
dated notes beneath them instead.

## 1. The proposal itself

- [ ] 1.1 Author the packet — `proposal.md`, `design.md`, the
  `review-lane-floor-mirror` delta and this file — with every factual claim about
  running code verified in a clone and cited `file:line`, and every authoring
  decision stated with the alternative it beat.
- [ ] 1.2 `OPENSPEC_TELEMETRY=0 openspec validate mirror-floor-regeneration-automation
  --strict` and `--all --strict` green at the CLI version
  `contracts/openspec-cli-pin.yaml` names, with this repository's pre-existing
  failures unchanged in count and identity.
- [ ] 1.3 List the change in this repository's README "OpenSpec Records" active
  block.
- [ ] 1.4 The codexFactory primary `add-floor-regeneration-automation` is open
  and names this change as its companion.
- [ ] 1.5 Post the packet for review, with the Codex and Copilot rounds run to
  exhaustion and every thread resolved on a measurement.

## 2. codexFactory's half — NOT DONE HERE

- [ ] 2.1 `codexFactory: add-floor-regeneration-automation` is ratified and
  realized: the regeneration lane runs the shipped generator at a LANDED
  openxFactory `main` commit and opens the regeneration pull request itself.
- [ ] 2.2 That lane's additions-only and block-confinement refusals are landed
  and tested there, not here.
- [ ] 2.3 No codexFactory file is edited by this change or by its realization,
  and this packet claims no authority over one.

## 3. openxFactory realization — the re-pin lane

- [ ] 3.1 Add `.github/workflows/` lane `floor-repin`: mint the App token; read
  codexFactory `main`; compare the floor document there against
  `contracts/review-lane-floor-snapshot.yaml`; act only on a disagreement.
- [ ] 3.2 The landed-core refusal (requirement 2): verify the candidate
  codexFactory commit is reachable from codexFactory's default branch, resolved
  at run time, never taken from an event payload; refuse and open nothing
  otherwise.
- [ ] 3.3 Move the FIVE sites in ONE commit — `contracts/review-lane-pin.yaml`
  `core_commit`; `.github/workflows/merge-master-approval.yml`'s
  `PINNED_CORE_COMMIT`; that workflow's core checkout `ref:`;
  `.github/workflows/pytest-suite.yml`'s core checkout `ref:`; and
  `contracts/review-lane-floor-snapshot.yaml` re-copied — then **RE-READ ALL
  FIVE from disk** and require each to equal the new core commit before
  committing (requirement 3).
- [ ] 3.4 Re-copy the snapshot from the codexFactory checkout and recompute
  `floor_snapshot.sha256` and `floor_snapshot.entry_count` FROM THE BYTES
  WRITTEN, never from a codexFactory report or pull-request body
  (requirement 4).
- [ ] 3.5 Compose the pull-request body from the witnesses in requirement 6,
  including the evidence that the pinned commit is reachable from codexFactory's
  default branch.
- [ ] 3.6 Trigger (M-1): the scheduled sweep is the MECHANISM and must be
  sufficient alone; any codexFactory-side notification leg is an accelerator.
  **Decide and record WHERE the schedule lives** — this repository has no
  `schedule:` in any workflow today (the nightly is scheduled by a thin caller in
  the xFactory aggregation repository and reaches here through
  `workflow_call`), so a schedule here is a first for this repository and a
  schedule there puts the credential in a third repository. Both consequences to
  be stated, one chosen.
- [ ] 3.7 Idempotence: at most one open re-pin pull request; a firing that finds
  one updates its branch; nothing to move is a clean named no-op.
- [ ] 3.8 Declare the credential binding as a TEMPLATE with placeholder
  references only, and make the lane FAIL LOUD when it does not resolve — no
  `|| github.token` fallback anywhere in this lane.
- [ ] 3.9 The workflow declares least privilege: `contents: write` and
  `pull-requests: write` on the job that opens the pull request, nothing wider,
  and no write privilege over codexFactory.

## 4. openxFactory realization — tests, and the judge left alone

- [ ] 4.1 `tests/review_lane_pin/`: a workflow-shape test pinning the lane's
  trigger legs, the absence of any merge or approve call, the absence of any
  `|| github.token` fallback, and the declared permissions.
- [ ] 4.2 NEGATIVE — a candidate core commit not reachable from codexFactory's
  default branch refuses and moves no site.
- [ ] 4.3 NEGATIVE — a run in which any one of the five sites does not read the
  new core commit after the write discards the advance and opens nothing.
- [ ] 4.4 NEGATIVE — the snapshot's digest and entry count are computed from the
  written bytes: a fixture in which a stale digest is supplied must be caught.
- [ ] 4.5 ANTI-VACUITY — each of 4.2, 4.3 and 4.4 is proven capable of failing:
  the positive fixture passes the same assertion the negative fixture reds.
- [ ] 4.6 **NO CHANGE** to `tests/review_lane_pin/test_floor_snapshot.py`'s LQ-A7
  assertion, its two negative controls, the byte-identity freshness verifier, its
  named-testcase watch, or `EXPECT_SKIPPED`. Assert this by diff: the realization
  pull request must touch none of them.
- [ ] 4.7 `python3 -m pytest tests/review_lane_pin -q` green, and green a second
  time with a codexFactory checkout on disk.

## 5. The first UNATTENDED cycle, observed end to end

- [ ] 5.1 A real `openspec/specs/**` promotion lands here and the advisory lane
  reports `pending_floor_extension` with a non-zero count — quoted verbatim.
- [ ] 5.2 The codexFactory regeneration pull request is opened BY THAT LANE, with
  no operator running the generator.
- [ ] 5.3 The re-pin pull request is opened BY THIS LANE, with no operator
  copying a digest; the five sites are verified by reading them back from the
  merged commit, not from the lane's own report.
- [ ] 5.4 The required suite judges that pull request GREEN with no exemption —
  and the byte-identity freshness verifier is confirmed to have RUN, by name, on
  it.
- [ ] 5.5 Both merge on a human word, and `covered-pending` returns to zero on
  the next main run — quoted verbatim from that run.
- [ ] 5.6 The end-to-end wall time is measured and recorded against the two hand
  cycles in `proposal.md` § Why (55 min and 77 min).
- [ ] 5.7 ONE observed refusal on a real run, of any kind (non-landed core, a
  site that did not move, an unresolved binding), quoted verbatim — or the box
  stays OPEN and says so rather than being ticked on a test-only observation.

## 6. Owner's acts (not an agent's)

- [ ] 6.1 Ratify or refuse this packet. The 2026-09-05 word authorized the
  PROPOSING, not the content.
  **2026-09-06 — TAKEN. Brett Heap ratified it in session, verbatim "ratify both
  when green, then land them" — a PAIR word over this companion and codexFactory
  #235 together, recorded 2026-09-06T01:18Z on PR #708 over head `e4ef8ade`, its
  `pytest-suite` condition met. The packet is now `Status: ratified` and the
  record is `review/ratification-2026-09-06.md`. The box is left UNTICKED
  deliberately — ticking an owner's-act box is a claim an agent may not make
  about the owner, and this dated note is how the act is recorded instead.**
- [ ] 6.2 Rule on the authoring decisions M-1 through M-7, and in particular on
  M-7 (the lane writes no comment-history paragraph, so eight advances of
  narrative in `contracts/review-lane-pin.yaml` stop accruing) and on M-1's
  schedule location.
  **2026-09-06 — STOOD. Under the ratification word, M-1 through M-7 stand as
  recommended and no veto was exercised; each remains one edit away. The box
  stays UNTICKED for the same reason 6.1's does.**
- [ ] 6.3 SEPARATE AND NOT ASKED FOR HERE: whether the merge-master low-risk
  envelope — live today only for the doc-health nightly lane — should ever be
  extended to this lane. The default is a human merge word, and it holds until
  this box is ruled. Named so the question is not silently assumed either way,
  and noting that `contracts/review-lane-pin.yaml` is itself a never-clearable
  floor entry whose stated ground is that a clearable pin *"would let a pull
  request choose its own judge"*.
- [ ] 6.4 Install or extend the App grant the binding in 3.8 names, if M-6 stands.
