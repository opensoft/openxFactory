# Design: admit-review-lane-repin-to-merge-approval-envelope

Status: draft
Kind: design

**NOTHING HERE IS SETTLED BY BEING WRITTEN.** Every decision below states a
recommendation, its alternatives and what a veto costs. Ruling on them is
`tasks.md` box 1.3, and it is Brett Heap's act. Where a figure appears it was
read back from the API or from the tree on 2026-09-10 and the read is named.

## 1. What actually stands between an enrolled class and a merged advance

`amend-mirror-floor-regeneration-merge-authority` § *The realization gate*
measured four refusals on 2026-09-08. **This packet retires ONE of them and
retires no other**, and the table below is that statement rather than a
restatement of the parent's.

| # | the refusal | what this packet does about it |
|---|---|---|
| 1 | **No candidate class admits the lane.** `.github/merge-approval-envelope.yml` enrols exactly one candidate, `intent-rolling-custody`; the lane's head is `bot/review-lane-repin` and its four writable files are none of that class's three paths. | **RETIRED BY THIS PACKET'S REALIZATION**, and by nothing else it does. § 3.1 of `tasks.md`. |
| 2 | **The floor is composed OVER the envelope.** `.github/workflows/merge-master-approval.yml:1603` parks when `FLOOR_MATCHED != 0`, *"whatever the envelope says"*, and `contracts/review-lane-pin.yaml` is a never-clearable floor member. | **NOT RETIRED HERE.** The N-1b (ii) carve is codexFactory's decision core to author; `tasks.md` box 4.1. The enrolment lands INERT behind it. |
| 3 | **Code-owner review is required on `main`** by ORGANIZATION ruleset `18834180` over `~ALL` / `~DEFAULT_BRANCH`; all four sites are CODEOWNERS-routed (`.github/CODEOWNERS:2`, `:20`, `:27`); a GitHub App cannot be named in CODEOWNERS. | **NOT RETIRED HERE, AND NO BYPASS IS PROPOSED.** `tasks.md` box 4.4 holds it for a word. |
| 4 | **codexFactory's promoted `Bounded autonomous surface`** forbids autonomously approving any CODEOWNERS-scoped path; `extend-merge-master-envelope-to-floor-bot-lanes` narrowed it under N-1 for the codexFactory regeneration lane ONLY. | **NOT RETIRED HERE.** It is codexFactory's text; `tasks.md` box 4.2. |

**So the honest headline is the same one `extend-merge-master-envelope-to-floor-bot-lanes`
was forced to write, and it is repeated rather than softened: THIS IS NOT A
CONFIGURATION CHANGE.** Enrolling the class retires one of four refusals. Three
remain, two of them in another repository, and one of those needs a word this
packet may not give itself. A reader who expects the enrolment to make the lane
autonomous on merge should read that sentence twice.

## 2. The never-clearable ground, and why an enrolment is not what it forbids

### 2.0 Every line number below was RE-MEASURED, and three of the inherited ones had moved

**The citations this packet inherited from its two source packets no longer
pointed where they said.** `extend-merge-master-envelope-to-floor-bot-lanes`
(2026-09-07) and `amend-mirror-floor-regeneration-merge-authority` (2026-09-08)
cite the floor park at `.github/workflows/merge-master-approval.yml:1494-1501` /
`:1499-1506` / `:1504` and the lane's run-time resolution at
`.github/workflows/review-lane-repin.yml:259-267` with its header at `:41-43`.
**On this branch's tree those are wrong**, because both workflows have moved
since — `merge-master-approval.yml` most recently at the #883 re-pin. Measured
here rather than copied:

| what | inherited citation | **measured on this tree** |
|---|---|---|
| the floor park, composed OVER the envelope | `merge-master-approval.yml:1504` | **`:1602-1603`** — `if [ "${FLOOR_MATCHED:-}" != "0" ]` at `:1602`, the `park "…a never-clearable path is never autonomously approvable, whatever the envelope says"` at `:1603` |
| the run-time default-branch resolution | `review-lane-repin.yml:259-267` | **`:424-441`** — step *"Resolve codexFactory's default branch and head, at run time"* at `:433`, `gh api "repos/${SOURCE_REPOSITORY}" --jq .default_branch` at `:439`, the refusal at `:441` |
| the header recording that the trigger payload is ignored | `review-lane-repin.yml:41-43` | **`:67-69`** |

Verified UNMOVED and cited as they stand: `.github/CODEOWNERS:2` / `:20` /
`:27`; `scripts/review_lane_repin.py:28`, `:35` and `:153-156`;
`.github/workflows/review-lane-repin.yml:783-788`, `:789` and `:850`;
codexFactory `openxfactory-review-authority-floor.yaml:108-112`. **The
inherited numbers are left alone in the packets that carry them** — they were
true when written and those packets are dated records — and nothing in this
one repeats a number it did not read back.

### 2.1 The ground, quoted

codexFactory `scripts/merge_master/openxfactory-review-authority-floor.yaml`,
the comment at `:108-111` attached to the entry at `:112`:

> A fourth, separately grounded entry (not part of the wallet-register trio
> above): the review-lane pin selects which codexFactory commit's decision core
> judges this repository. Clearable, it would let a pull request choose its own
> judge.

And the canon that generalizes it — `extend-merge-master-envelope-to-floor-bot-lanes`'s
ratified `roles-authority-model` delta, *A never-clearable floor member is never
autonomously approvable*, whose second paragraph is the only door and it is
narrow: the permission "SHALL be expressed as a CARVE naming the candidate and
the exact member set it may touch — never as the removal of the member from the
floor".

### 2.2 The answer, and it turns on a distinction the ground does not draw

**The hazard the ground names is CHOOSING. What this lane does is DELIVERING.**
A clearable pin would let *a pull request* choose its own judge — that is, a
pull request would carry a value some author selected and the gate would not
stop it. The re-pin lane carries a value **nobody selects**, and the four
bindings that make that true are each running code rather than a promise:

1. **The author, head and base are measured, not asserted.** `gh api
   repos/opensoft/openxFactory/pulls/732 --jq '.user.login, .head.ref,
   .base.ref'` returns `openxfactory[bot]`, `bot/review-lane-repin`, `main` —
   read on 2026-09-10 from the lane's only merged advance. A pull request from
   any other author, or on any other head, matches no class and parks.
2. **The diff is the driver's, and the driver has no discretion.**
   `scripts/review_lane_repin.py:28` — *"It moves ALL FIVE SITES or it opens
   nothing, and it proves the move by reading it back"* — and `:35` — *"It
   writes nothing outside the five sites"*. The five sites are four files
   (`:153-156`), and `path_allowlist` names all four EXACTLY, so a fifth path
   parks the candidate whatever else is true.
3. **The value is not the lane's to pick.** `.github/workflows/review-lane-repin.yml:424-441`
   resolves codexFactory's default branch AT RUN TIME and refuses to pin at any
   other reference; the header at `:67-69` records that the lane *"ignores any
   commit, branch or reference named by its trigger"* and that the payload is
   never read. The only value this lane can ever propose is codexFactory's own
   default-branch head.
4. **The proposed judge is exercised on the candidate BEFORE the approval.**
   `pytest-suite`'s LQ-A7 freshness verifier
   (`tests/review_lane_pin/test_floor_snapshot.py::TheFreshnessVerifier`) runs
   against the core the pull request PROPOSES, not the superseded one, and it is
   a REQUIRED check — so `require_all_checks: true` conjuncts it into the
   approval condition. An approval cannot stand over a core the proposed core's
   own verifier refuses.

**Together: the judge is chosen by the source floor, in codexFactory, under
codexFactory's own merge word. This repository's pull request is the delivery of
a choice already made elsewhere.** That is a different act from the one the
floor comment forbids, and the difference is structural rather than rhetorical —
there is no input to this pull request that a person or an agent can vary and
still match the class.

### 2.3 The residual risk, stated

**An autonomously approved delivery is the envelope approving a change to its own
NEXT judge.** Safeguards 1–4 bound WHICH value can arrive; they do not make the
arrival harmless if codexFactory's default branch is itself compromised. What
bounds the residual, and nothing more is claimed:

* a human may close the pull request at any time, and every required check still
  gates the merge;
* the enrolment carries a one-edit kill switch — removing the class from the
  declaration returns the lane to the human gate on the next evaluation
  (ratified: *An enrolled autonomous lane carries a one-edit kill switch*);
* the carve is per-candidate and per-member, so `contracts/review-lane-pin.yaml`
  stays never-clearable for every other candidate and every other author and
  `repository_floor_drift.py` continues to catch its removal;
* and the exposure this does NOT defend against is the exposure every hand merge
  already carries: the human who merged #883 checked that forty hex characters
  matched codexFactory `main`, not that codexFactory `main` was sound.

**That last bullet is the trade in one sentence: the enrolment does not lower the
trust floor, it removes a human act that was never exercising judgement over the
trusted thing.** A reader who ranks it differently should take D-1 (d).

### 2.4 What is refused outright, so the narrowing cannot drift

Two shapes would make this fire sooner and both are refused BY NAME, in the
requirement text and in a scenario each:

* **Removing `contracts/review-lane-pin.yaml` from the floor.** That is the
  state the ground exists to prevent. Refused, and the packet will not author it
  in any form.
* **A bypass actor on a ruleset.** codexFactory's D-4 (i) was WITHDRAWN
  2026-09-08 (codexFactory #232 comment `5585989018`); here the grant is worse —
  `18834180` is an ORGANIZATION ruleset over `repository_name: ~ALL` /
  `ref_name: ~DEFAULT_BRANCH`, so an entry lifts the code-owner rule, plus
  `deletion` and `non_fast_forward` (bypass is per RULESET, not per rule), on
  every default branch in `opensoft` — including the gate that makes this
  repository's own pin routing binding — and the async auto-merge path is
  reported not to honour `bypass_actors` at all (community discussion #162623).
  **No agent may take a ruleset act.**

**And codexFactory's escape does not exist here.** There, the regeneration bot
writes ONE file, so relocating it off every CODEOWNERS-matched prefix satisfies
the code-owner rule vacuously. Here the lane writes FOUR files and **two are
workflow files**, which cannot leave `.github/workflows/`; un-routing that prefix
is refused on its face under the 2026-08-23 convener ruling's routing for
assembly-class gate surfaces. That is a measurement, not a preference.

## 3. Authoring decisions

### D-1 — ASK AT ALL, or leave the click where it is

**RECOMMENDED: ask — file the enrolment, on the word that commissioned it, with
the re-opening of N-1 declared.**

Grounds: the third cycle produced the asymmetry as a figure (22 min 16 s
unattended on one side, ~10 h and a human word on the other, openxFactory #745
comment 5618883586); the parent packet's arming is already in production and
already names this packet in its witness line; and the thing being bought is
exactly one human click on a byte-identical mirror advance.

Alternatives:

- **(b) file a NARROWER packet that asks only for the carve** and leaves the
  enrolment for later. Rejected because the carve is meaningless without a class
  to carve for — codexFactory would be asked to name a candidate that does not
  exist.
- **(c) file nothing and ask Brett Heap to rule N-1 on the issue instead.**
  Cheaper by a pull request, and it was refused because box 4.3's tick condition
  is the successor being NAMED **as a packet or an issue**, and a ruling with no
  packet leaves the shape written only in the parent's prose where the next
  reader must reconstruct it.
- **(d) LEAVE IT HUMAN — status quo.** **A serious contender and it is written as
  one.** One click per cycle is the whole benefit; the price is re-opening a
  decision ratified three days ago, a carve in another repository's decision
  core, a narrowing of a promoted requirement in that same repository, and a
  ruleset question with no clean answer. **A veto to (d) costs nothing already
  spent**: the parent's arming stays inert exactly as it is, its box 4.3 still
  ticks on this packet being NAMED, and this packet archives unratified with the
  measurement it recorded intact.

### D-2 — WHERE THE DELTA LIVES, and why there is no `## MODIFIED`

**RECOMMENDED: four `## ADDED` requirements in `review-lane-floor-mirror`, and
no `## MODIFIED` block anywhere.**

`extend-merge-master-envelope-to-floor-bot-lanes` already ADDS the general rules
to `roles-authority-model` (*enrolled per lane and per surface*; *a
never-clearable floor member is never autonomously approvable*; *a lane writing
its own repository's judge is enrolled only behind named safeguards*; *a one-edit
kill switch*; *an autonomous approval is not a merge*). **This packet is the
INSTANCE of those rules, not a revision of them**, so it composes with them and
restates none. Writing a `## MODIFIED` over an ACTIVE SIBLING'S ADDITION would
drag in `govern-sibling-added-modified-deltas`' pairing declaration and an
archive-ordering hold this packet does not need.

- **Alternative: add to `roles-authority-model` instead.** Rejected: the four
  requirements are all about THESE two lanes, and `review-lane-floor-mirror` is
  the capability that already carries *Each floor bot lane's admission
  conditions are measured, not asserted*.
- **Alternative: split across both capabilities.** Rejected as ceremony for one
  packet.

### D-3 — INERT ON LANDING, or hold the enrolment until codexFactory carves

**RECOMMENDED: land the enrolment INERT, with the inertness declared in the
requirement and reported in the witness — the same answer the parent's box 1.3
gave for the arming ("rule land inert, this lane realizes it", 2026-09-09).**

Both answers are conforming: the requirement admits the inert state by name, so
this is a sequencing choice and not a correctness one. Landing inert puts the
class in a code-owned file where codexFactory can see the candidate id its carve
must name; holding means codexFactory is asked to carve for a class that does not
exist. **Carried as `tasks.md` box 1.5 so it can be ruled on its own.**

### D-4 — THE MERGE METHOD, which is a CHOICE here and is not in codexFactory

**RECOMMENDED: SQUASH.**

This repository permits all three methods — `merge: true`, `squash: true`,
`rebase: true` at the repository and `allowed_merge_methods: [merge, squash,
rebase]` on both `pull_request` ruleset rules — where codexFactory permits merge
only. So the method must be chosen deliberately, and the lane's own precedent
chooses it: PR **#732** merged 2026-09-06T23:46:28Z as `9ffc6252` with **one
parent**, a squash. The arming call already in production is `gh pr merge --auto
--squash "${BOT_BRANCH}"` (`review-lane-repin.yml:850`), so recommending
anything else would mean editing a ratified realization to no benefit.
**Carried as `tasks.md` box 1.4.**

### D-5 — THE REALIZATION SURFACE IS THREE FILES, and the second one is the load-bearing edit

**RECOMMENDED: name all three in `code_surface:` up front rather than discovering
the second at realization.**

| file | what moves | why it is not optional |
|---|---|---|
| `.github/merge-approval-envelope.yml` | one ADDED candidate class | the enrolment itself |
| `tests/review_lane_pin/test_review_lane_caller.py` | `sole_candidate()` REPLACED by a per-class shape assertion | the helper refuses anything but one candidate **in terms** — *"a second entry is a NEW GRANT rather than a configuration change"* — so the suite goes red the moment a second class lands |
| `.github/workflows/review-lane-repin.yml` | the second sentence of `ARMED_TAIL` (`:789`) | the file's own comment at `:783-788` says it "MUST BE DROPPED THE DAY IT STOPS BEING TRUE" and names this lane as what drops it |

### D-6 — THE WITNESS TEXT WHEN THE CLASS LANDS BUT THE CARVE HAS NOT

**RECOMMENDED: replace the sentence rather than delete it, and name what is
still missing.**

If the class lands inert (D-3) the current sentence — *"NO CANDIDATE CLASS ADMITS
THIS LANE TODAY"* — becomes FALSE while the arming stays inert for a different
reason. Deleting it would leave the log claiming an autonomy the machinery does
not have. The requirement *The armed witness drops its inertness clause only when
a class actually admits the lane* is written to forbid both errors, in both
directions, and its two scenarios are the two ways the claim can go stale.

### D-7 — REPLACE `sole_candidate()`, DO NOT RELAX IT

**RECOMMENDED: a per-class assertion that pins BOTH classes by id and fails on a
THIRD.**

The obvious cheap edit is to change `len(candidates) != 1` to `!= 2`. Refused:
the helper's value is not the number, it is the sentence attached to it — that a
new class is a NEW GRANT. A count assertion carries that sentence for exactly as
long as nobody bumps the number again. A per-class assertion carries it
structurally: each enrolled class is pinned by id and by its own conditions, and
an unpinned class fails whatever the count. **Carried as `tasks.md` box 3.2.**

### D-8 — WHAT THIS PACKET REFUSES TO CARRY, so scope does not creep

**RECOMMENDED: refuse all four of the following in this packet, each with its
reason recorded rather than left as an omission.**

- **The carve itself.** codexFactory's decision core. Box 4.1.
- **The `Bounded autonomous surface` narrowing.** codexFactory's promoted text.
  Box 4.2.
- **The precondition measurement (does auto-merge fire at all on a rulesets-only
  `main`?).** Cheap, unmeasured, and carried from the parent's box 4.4 to this
  packet's box 4.3 because it is a precondition for every completion shape and
  belongs where the completion is asked for. `GET
  /repos/opensoft/openxFactory/branches/main/protection` returns `404 "Branch
  not protected"` and ZERO of the last 60 closed pull requests here carry a
  non-null `auto_merge`. **Until it is settled every completion shape is
  premature.**
- **The completion-path word.** Box 4.4, Brett Heap's, no bypass proposed.

## 4. Open questions, declared rather than answered

- **OQ-1.** If the precondition measurement (box 4.3) shows auto-merge does not
  fire at all on a rulesets-only `main`, the enrolment approves and nothing
  lands. **Is the enrolment still worth having in that state?** The
  recommendation is yes — an approval that lands nothing is still a recorded
  autonomous judgement and the class is what codexFactory's carve must name —
  but it is put rather than assumed.
- **OQ-2.** `check_exclusions` is recommended as `[merge-master-approval,
  lane-line]`. `merge-master-approval` is the self-reference exclusion and is not
  in doubt. **`lane-line` is:** the bot's pull-request body carries `Lane:
  review-lane-repin-bot` (`review-lane-repin.yml:719`), so the check may well
  pass on its own — in which case excluding it is a needless widening.
  **Measure before encoding**, on the next real advance.
- **OQ-3.** `revert_suffices` — the enrolled `intent-rolling-custody` declares
  `true` on an append-only invariant. A re-pin is a MODIFICATION of four files,
  and reverting the merge restores the prior pin exactly, but the *effect* of the
  revert is that the superseded core judges again. Whether that counts as
  "reverting suffices" is a real question about the field's meaning and is put to
  the owner rather than answered by an author.
- **OQ-4.** Whether this packet and codexFactory's carve should be ONE
  two-repository packet, as § 6.3 was, or two coordinated ones. The
  recommendation is two — the carve is decision-core code and this is an
  enrolment declaration — but the parent's § The realization gate reads *"the
  enrolment is a two-repository packet exactly as § 6.3 was"*, so the reading is
  contested and is recorded as contested.
