---
code_surface: openxFactory — and the split is the capability's own. THE READ is `.github/workflows/review-lane-repin.yml`, which already resolves another repository over the API and hands this repository's decision code pure inputs; it gains the aggregation's three surfaces beside the source repository it already reads. THE JUDGMENT is `scripts/review_lane_repin.py`, which gains a comparison over supplied values and reaches no network, exactly as every other judgment in that module does. THE PULL-REQUEST-SIDE HOST is a NEW `pull_request`-triggered gate workflow under `.github/workflows/`, on the estate's own pin-gate pattern (`openspec-cli-pin-gate.yml`, `openreposhape-pin-gate.yml`) — measured, `review-lane-repin.yml`'s `on:` keys are exactly `['schedule', 'repository_dispatch', 'workflow_dispatch']`, so without it the requirement's pull-request clause has nowhere to run; and `review-lane-repin.yml` does NOT gain a `pull_request` trigger, which would fire the advance logic on every pull request. THE PROOF is `tests/review_lane_pin/`, which gains fixtures for the five scenarios — a stale `converged`, a stale `diverged`, surfaces disagreeing with each other, an unreadable aggregation, and the pure-function reproduction — plus the POSITIVE cases, a true `converged` and a true `diverged` each reported as agreeing, and the negative control that `review-lane-repin.yml` carries no `pull_request` trigger. NOT THIS PACKET'S SURFACE, each for a stated reason: `contracts/review-lane-pin.yaml` is NOT hand-patched and its `lockstep.status`, its `converged_with:` list and its append-only `reason:` narrative do not move — the declaration is what the check reads, and a packet that edited the value it proposes to start checking would be asserting the very fact it exists to stop asserting; `contracts/openspec-cli-pin.yaml` and `scripts/validate-openspec-cli-pin.py` are untouched, because the DISPOSITION MECHANISM is not this packet's subject in any respect; `scripts/review_lane_repin.py`'s `WRITABLE_PATHS` and `PINNED_SITES` do not gain a member — the remedy is an ASSERTION and not a widened write, for the reason at `design.md` D1; `.github/workflows/merge-master-approval.yml` and the vendored floor snapshot do not move; `opensoft/xFactory` is READ and never written, by this packet or by its realization, and no act in that repository is proposed here; no ruleset, schema, credential or pin moves. MEASURED, not assumed: `grep -nE "opensoft/xFactory|MIGRATION_PIN|council-convening" scripts/review_lane_repin.py .github/workflows/review-lane-repin.yml` returns ZERO HITS IN BOTH, and `MIGRATION_PIN` appears in no file under `scripts/` or `.github/workflows/` at all — so the surface below is genuinely new reach and not a re-wiring of something that already looks.
target_release: implemented — the value `release-realization` names for a change that realizes into this corpus rather than into a future contract bundle. No bundle is cut, no `contracts/manifest.yaml` row moves, no digest inventory is recomputed, no release tag is owed and no consumer's pin has to advance to receive this: `contracts/review-lane-pin.yaml` is READ by the new check and is not edited by it. SEPARATELY, and stated here so it is not discovered at the archive gate: the code surface above is NOT empty, so under `release-realization` this packet archives on merged PLUS green realization evidence — the check landed, its four scenarios exercised by fixtures, and ONE real observation of the check running against a proposed advance — and not on landing.
sequenced_after: [mirror-floor-regeneration-automation]
---

# Proposal: assert-review-lane-lockstep-against-aggregation

Status: draft
Kind: proposal
Proposed: 2026-09-22, in lane `openxfactory-4` (display
`openXfactory-4-openDox_extraction`), actor `successor2`.
Origin: Copilot finding
[`r4067694104`](https://github.com/opensoft/openxFactory/pull/1136#discussion_r4067694104),
review
[`5273295522`](https://github.com/opensoft/openxFactory/pull/1136#pullrequestreview-5273295522)
on `opensoft/openxFactory`
[#1136](https://github.com/opensoft/openxFactory/pull/1136) — the lockstep flip
at the fourth re-point ceremony, merged `7c49825e`. The lane VERIFIED the
premise, DECLINED the remedy as out of that pull request's mandate, and
registered it: [#1136 comment `r4067703286`](https://github.com/opensoft/openxFactory/pull/1136#discussion_r4067703286).
**And the shape of the remedy was recorded IN THE PIN FILE ITSELF**, in the
`reason:` paragraph that flip appended, as option **(b)**: *"make the
CROSS-REPOSITORY fact assertable at all — nothing today reads xFactory's three
surfaces and compares them to this value, which is why a false `status` survives
in EITHER direction until a human notices … **(b) is the better fix, because (a)
still leaves this file's truth depending on a lane remembering to write it.**
Both are OpenSpec-class acts on a realized capability, which is exactly why
neither rides here."*

**This packet is that act.** `Status: draft`; it is not ratified by the authoring
lane.

## The hazard, and it is not hypothetical

`contracts/review-lane-pin.yaml` declares, at `lockstep.status`, whether this
repository's pinned decision core and the aggregation's `MIGRATION_PIN` name the
same commit. **Nothing measures that claim.** Measured on `main` `2e222d98`:

| fact | measurement |
| --- | --- |
| the declaring field | `contracts/review-lane-pin.yaml`:714 `status: converged` |
| the value it is about | `core_commit`:60 `b21f0100…` |
| the aggregation's three surfaces | `opensoft/xFactory` `main`: `merge-master-approval.yml`:152, `council-convening-lane.yml`:308, `tests/test_merge_master_workflows.py`'s `MIGRATION_PIN`:72 — all three `b21f0100…` |
| what the repin lane may write | `WRITABLE_PATHS` = four files (`review_lane_repin.py`:196-197); within the pin file, only the regex-anchored `core_commit`, `floor_snapshot.sha256` and `floor_snapshot.entry_count` |
| whether it can write the field | **the string `lockstep` occurs ZERO times in `scripts/review_lane_repin.py`** |
| whether anything reads the aggregation | **ZERO hits for `opensoft/xFactory`, `MIGRATION_PIN` or `council-convening` in `scripts/review_lane_repin.py` and `.github/workflows/review-lane-repin.yml` combined**; `MIGRATION_PIN` appears in no file under `scripts/` or `.github/workflows/` |
| the test that guards the field | `test_the_pin_records_its_lockstep_state_with_the_aggregation_pin` asserts `lockstep.status` equals a LITERAL in the test file — this file's own value compared to this repository's own constant |

So the declaration is true today and **nothing keeps it true.** It last went
false on 2026-09-18, when the hourly lane's advance (`#1122` -> `38f826c2`,
2026-09-18T20:53:37-04:00) moved `core_commit` and left `converged` standing;
the hand repair (`#1123` -> `8184d74a`, 21:27:43-04:00) followed **34 minutes 6
seconds later**, both first-parent on `main`. Thirty-four minutes because a human
was watching that evening. Nothing bounds it.

**And it is live at this moment.** `opensoft/openxFactory`
[#1138](https://github.com/opensoft/openxFactory/pull/1138) is OPEN, NOT a draft,
with platform auto-merge ARMED, proposing `core_commit` `b21f0100…` ->
`491fc54d…`. Its diff is four files, and `git diff main...bot/review-lane-repin |
grep -cE "^[-+].*(lockstep|converged|diverged)"` returns **0**;
`tests/review_lane_pin/test_review_lane_caller.py` is not in the diff at all.
**The hour that pull request merges, `lockstep.status` becomes false, the test
still passes, and nothing reports it.**

## What the remedy has to be, and why this one

The task admits two shapes: the declared state is **written by the same act that
moves `core_commit`**, or it is **derived and checked rather than declared**.
This packet takes the second. The reason is a measurement, not a preference, and
it is the capability's own doctrine:

**THE LANE CANNOT WRITE THE FIELD HONESTLY, because it has no reading of the
aggregation to write from.** Zero hits, in both files. A lane taught to write
`diverged` on every advance would be INFERRING from the rule *"`MIGRATION_PIN`
does not move on a routine advance"* — and that inference is FALSE in a case this
estate has already produced: at the fourth ceremony (`opensoft/xFactory` `#475`
-> `c88d1fdd`, 2026-09-21) the aggregation converged ONTO a commit this file had
already been pinned to since 2026-09-18, so the two moves were three days apart
and were not a pairing at all. An advance that lands where the aggregation
already is leaves the pair CONVERGED, and a lane writing `diverged` by rule would
have made the field false in the other direction.

**And this capability has already ruled on assertion-versus-measurement, one
requirement over.** *The automated pin advance moves every pinned site in one
commit or opens nothing* closes with: *"what is added here is that an UNATTENDED
author must prove the lockstep by measurement rather than assert it."* Shape (a)
would install, inside the same capability, exactly what that sentence forbids —
an unattended author asserting a lockstep it never measured. Shape (b) extends
the capability's own principle to the ONE lockstep it does not yet cover: the
five pin sites' internal lockstep is proved by re-reading every site after the
write; the cross-repository lockstep is proved by reading the other repository.

**The capability is also already built for it.** The realization's own split is
that *"the workflow reads the two repositories with `gh` — visible in the run
log, re-runnable by a reviewer with the same two API calls — and hands this
module PURE INPUTS … Every requirement's refusal is then a unit test with a
fixture, not a workflow that has to be fired to be believed."* The
cross-repository read goes where cross-repository reads already go; the
comparison goes where judgments already go. Shape (b) needs no new architecture,
only one more repository read and one more pure function.

**One further asymmetry decides it.** Shape (a) catches only divergence this
repository causes. A false state arising because the AGGREGATION moved — which is
what a re-point ceremony is — is invisible to it forever. The assertion catches
both, which is why the requirement is written symmetric.

## Boundaries this packet holds

- **The disposition mechanism is not touched.** `scripts/validate-openspec-cli-pin.py`,
  `reconcile()` and `contracts/openspec-cli-pin.yaml` are not this packet's
  subject in any respect, and nothing here proposes changing how a finding is
  dispositioned.
- **The pin file is not hand-patched.** `lockstep.status`, `converged_with:` and
  the append-only `reason:` narrative do not move. A packet that edited the value
  it proposes to start checking would assert the very fact it exists to stop
  asserting.
- **`WRITABLE_PATHS` and `PINNED_SITES` gain no member.** The remedy is an
  assertion, not a widened write.
- **No act in `opensoft/xFactory` is proposed.** The aggregation is READ. Its
  `MIGRATION_PIN` advances only at a recorded re-point ceremony — gated on the
  golden characterization suite, the envelope re-validation and the live lane
  re-prove — and this packet neither performs nor requires one.
- **The `obligation:` field's "only at a ceremony" clause is NOT narrowed here.**
  The pin file records that clause as in tension with a lane this repository runs
  and says *"Narrowing that clause is the ratifier's act, not this diff's."* That
  is still true and it is a DIFFERENT act: this packet makes the state
  measurable, which is what lets the clause be narrowed on evidence rather than
  on argument. Registered at `tasks.md` § 6.1.

## The ceremony evidence this rests on

The convergence the check would have measured on 2026-09-21 is real and was
proved behaviourally, which is why `converged` is a claim about behaviour and not
only about text. `opensoft/xFactory` `#475`, merge `c88d1fdd`, landed
2026-09-21T21:55:36Z on Brett Heap's explicit ceremony word, moved
`MIGRATION_PIN` `1f131a23` -> `b21f0100` at all three surfaces in ONE commit
(`96d0b91b`, 3 files / 3 insertions / 3 deletions). Gates G1-G4 are in that
commit's own message; **G5 — the live lane re-proved AT THE NEW PIN — is recorded
at `#475` comment
[`5769610282`](https://github.com/opensoft/xFactory/pull/475#issuecomment-5769610282)**:
three post-landing runs (`35660330263`, `35660933433`, `35661430301`) each
concluded `success` with `b21f0100` read out of its own checkout log and ZERO
occurrences of the superseded pin, each judging the SAME candidate object as the
pre-act baseline run `35658107765`, and each emitting a decision whose canonical
`sha256` is identical to that baseline's. The pin moved and the verdict did not.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
