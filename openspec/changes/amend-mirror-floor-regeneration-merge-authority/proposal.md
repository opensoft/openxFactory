---
code_surface: openxFactory, and it is DELIBERATELY SMALL. THIS PACKET'S OWN SURFACE at realization is `.github/workflows/review-lane-repin.yml` — ONE arming line in the existing "Open or update the single automated advance" step, on both the open and the update path — and `tests/review_lane_pin/test_repin_lane.py`, whose `AnAutomatedPinAdvanceOnlyEverProposes::test_the_lane_opens_a_pull_request_and_stops_there` is the ten-term disposal sweep that enforces the very sentence being narrowed, plus the negative controls that bound the narrowing and the `EveryRatifiedScenarioHasATest` mapping, whose scenario count is read out of the ratified delta and must be re-read rather than re-pinned. NOT THIS CHANGE'S SURFACE, each for a stated reason: `scripts/review_lane_repin.py` is untouched — the DRIVER arms nothing, it writes the five sites and re-reads them, and keeping it disposal-free is the narrowing's blast-radius bound (a control is ADDED for it at realization, because openxFactory's sweep reads only the workflow's shell today and the bound must be measured rather than assumed); `.github/merge-approval-envelope.yml` is untouched — this packet enrols nothing, and the enrolment it waits on is a SEPARATE successor named in § The realization gate; `.github/workflows/merge-master-approval.yml` is untouched — neither the floor composition at `:1499-1506` nor the approval it produces is edited here, and the N-1b carve that composition would need is codexFactory's decision core to author; `contracts/review-lane-pin.yaml`, `contracts/review-lane-floor-snapshot.yaml` and the vendored snapshot's witnesses do not move; no ruleset is edited by any agent; and no schema, credential or pin moves.
target_release: a code surface, so per `release-realization` it archives only on merged + green realization evidence. No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves and no release tag is owed. The evidence is TWO things and the second cannot be manufactured: the arming step landed with `tests/review_lane_pin/` green and the flipped disposal sweep passing; and ONE real `bot/review-lane-repin` pull request observed reaching an autonomous approval and MERGING with no human click. **THE SECOND IS NOT REACHABLE TODAY** — no candidate class admits this lane and the floor is composed over the envelope — so this packet's realization is expected to land INERT and its archive waits on the enrolment successor. That is stated here rather than discovered at the archive gate.
sequenced_after: [mirror-floor-regeneration-automation, extend-merge-master-envelope-to-floor-bot-lanes, codexFactory:amend-floor-regeneration-merge-authority]
---

# Proposal: amend-mirror-floor-regeneration-merge-authority

Status: draft
Proposed: 2026-09-08, in lane `openxfactory-2` (display `openXfactory-2`), as
the lockstep mirror **D-6** of codexFactory's
`amend-floor-regeneration-merge-authority` recommends and that packet's
`tasks.md` box 5.1 names as owed.
Origin: Brett Heap's ruling of 2026-09-08T13:22:40Z, in session, verbatim
**"rule on finding 3, do the mirror packet too"** — recorded on openxFactory
issue [#745](https://github.com/opensoft/openxFactory/issues/745), comment
[5585824802](https://github.com/opensoft/openxFactory/issues/745#issuecomment-5585824802),
which reads on the mirror clause: *"openxFactory lockstep amendment on
`mirror-floor-regeneration-automation` (`specs/review-lane-floor-mirror/spec.md:5`
carries the same "SHALL NOT merge, SHALL NOT approve") — proposal only, Brett
ratifies; its realization is gated on an approver existing for the
`review-lane-repin` lane (openxFactory's envelope enrols only
`intent-rolling-custody` today)."*
**THE WORD AUTHORIZED THE PROPOSING, NOT THE CONTENT. RATIFICATION IS OWED AND
IS BRETT HEAP'S ACT**; nothing below is ratified by being authored, no
requirement here may be cited as approved until he rules on this packet itself,
and **NOTHING IS REALIZED** — this packet edits no workflow, flips no test,
enrols no candidate, touches no ruleset, moves no pin byte and ticks no box.
Every judgment this authoring session took is listed in `design.md` as
**M-A through M-G**, each with a recommendation, each put for veto.

## Why

**A ratified sentence in this repository and its lockstep twin in codexFactory
now say different things, and the divergence was created deliberately, by a
ratification, three hours ago.**

codexFactory's `amend-floor-regeneration-merge-authority` was ratified on
2026-09-08 and landed at main merge commit
`93f0f0d71ed00dbb384101be779d62233f6367f5`. It narrowed ONE clause of *"An
automated floor regeneration only ever proposes"*: `SHALL NOT merge` became
`SHALL NOT merge by its own act`, and the lane gained leave to arm the
platform's auto-merge so that the merge completes only when another party's
envelope approval for that exact head stands and every required check has
succeeded. **Its `design.md` D-6 measured this repository's twin sentence,
recommended NOT amending it in that packet, and recommended filing this one:**

> **RECOMMENDATION: do NOT amend it here; file a lockstep mirror amendment as a
> SEPARATE openxFactory packet after this one is ratified, and gate its
> REALIZATION on an approver existing for that lane.**

Brett Heap's word of 2026-09-08T13:22:40Z took that recommendation. This is
that packet.

**The twin sentence, verbatim, as this repository ratified it on 2026-09-06**
(`openspec/changes/mirror-floor-regeneration-automation/specs/review-lane-floor-mirror/spec.md:5`,
requirement *An automated pin advance only ever proposes*, ratified under
*"ratify both when green, then land them"*, PR #708):

> An automated lane that advances this repository's pinned decision core MUST
> propose the advance as a pull request and MUST NOT dispose of it: it SHALL NOT
> merge, SHALL NOT approve, SHALL NOT push to this repository's default branch,
> and SHALL NOT hold any authority over the pin that the equivalent hand act does
> not already have.

**The bar is not prose only. It is swept in code**, in this repository, over the
shell the runner actually executes:
`tests/review_lane_pin/test_repin_lane.py::AnAutomatedPinAdvanceOnlyEverProposes::test_the_lane_opens_a_pull_request_and_stops_there`
asserts the absence of ten terms — `gh pr merge`, `gh pr review`, `gh pr close`,
`--auto`, `--admin`, `enable-auto-merge`, `--method PUT`, `-X PUT`, `/reviews`,
`enablePullRequestAutoMerge` — plus a regex refusing the merge endpoint reached
through the raw API, and `review-lane-repin.yml`'s own header at `:401-404`
claims their absence in English so the test can measure the claim. **Two of
those ten are what this packet's realization would narrow, for one target, in
one exact form.**

**Why lockstep matters more than convenience here.** The two lanes are one
mechanism split across two repositories: codexFactory regenerates the floor
block, this repository re-pins the decision core that judges it, and the pair
was designed, ratified and realized as a pair (`mirror-floor-regeneration-automation`
names `codexFactory:add-floor-regeneration-automation` as its parent;
`extend-merge-master-envelope-to-floor-bot-lanes` was ratified in both
repositories under one pair word). Leaving one half's disposal sentence narrowed
and the other's absolute is a divergence a reader will hit and cannot resolve
from either document alone — and it is the shape D-6 filed this packet to
prevent: *"Filing the packet anyway keeps the two texts from silently diverging
and records the asymmetry where a reader will find it."*

**Working rule 3 is why it is a packet and not an edit.** A ratified requirement
changes only by a ratified change. The sentence being narrowed was ratified here
on 2026-09-06; no amount of ruling on a task box moves it.

## What changes

**ONE requirement, in one clause, and no other requirement moves.**
`specs/review-lane-floor-mirror/spec.md` carries a single `## MODIFIED
Requirements` block restating *"An automated pin advance only ever proposes"* in
full. The narrowed first line, in lockstep with codexFactory's:

> An automated lane that advances this repository's pinned decision core MUST
> propose the advance as a pull request and MUST NOT dispose of it **by its own
> act**: it **SHALL NOT merge by its own act** and SHALL NOT approve; **it MAY
> arm the platform's auto-merge on that same pull request, so that the merge
> completes only when (a) the merge-master envelope approval for that exact head
> stands and (b) every required check has succeeded**; and it SHALL NOT push to
> this repository's default branch, and SHALL NOT hold any authority over the pin
> that the equivalent hand act does not already have.

The parent's second body paragraph — *"The pull request SHALL move the pin and
nothing else … composes with … 'The mirror is inert until the pin carries the
rule, and the pin moves as one act'"* — is carried **word for word**. Three
paragraphs are then added, bounding the grant in the requirement rather than
leaving it to the implementation: the arming is a request to the platform and
never a merge, and no other path to the merge is admitted (no administrative
override, no direct merge endpoint, no undeclared merge queue, no review
dismissal, no second act); the default-branch bar is restated as a bar on the
LANE'S OWN WRITES, so a platform-completed merge is not a loophole in it; an
unsatisfiable rule leaves the arming inert and the lane SHALL NOT widen a rule,
add itself or anyone to a bypass list, or re-arm with a stronger act; and the
releasing approval must be another party's and must bind to the head it was
given for.

**SIX SCENARIOS ARE ADDED, ONE CARRIED WITH NARROWED BULLETS, TWO CARRIED
VERBATIM.** Added: the envelope-approved, fully green advance that merges with
no human act; the parked advance; the head that moves after an approval; the
lane never posting an approval; **the inert arming this repository will actually
observe, because no candidate class admits the lane**; and the arming reported
where the run is read. Narrowed: *The lane opens a pull request and stops there*
(the stop is now "no further action beyond arming"). Carried verbatim: *The lane
never writes to the default branch* and *The advance carries nothing but the
advance*. Nothing is retitled, nothing loses a bullet, and no requirement is
removed.

## What does NOT change

* **"SHALL NOT approve" stands, untouched.** The lane never approves — not its
  own pull request, not under any identity, not at all. A scenario says so in
  its own right rather than leaving it to be inferred from the sentence.
* **"SHALL NOT push to this repository's default branch" stands, untouched**, and
  is restated as a bar on the lane's own writes so that a platform-completed
  merge cannot be read as a loophole in it. Every `git push` in the lane still
  names `${BOT_BRANCH}`, and
  `test_the_lane_never_writes_to_the_default_branch` still enumerates them.
* **The six sibling requirements of `review-lane-floor-mirror` this parent added
  are untouched**: the landed-core refusal, the all-five-sites-or-nothing
  lockstep, the snapshot re-copy and witness recomputation, the
  no-exemption rule, the pull-request witness set, the trigger-and-idempotence
  rule and the credential binding. No `## MODIFIED` reaches any of them.
* **The judge is not adjusted in the same act as the author.** LQ-A7, its two
  negative controls, the byte-identity freshness verifier and its named-testcase
  watch are untouched, and `EXPECT_SKIPPED` does not move. `mirror-floor-regeneration-automation`'s
  M-4 refused an author-keyed exemption outright; this packet asks for none and
  adds none.
* **The envelope is not widened.** `.github/merge-approval-envelope.yml` still
  enrols exactly one candidate, `intent-rolling-custody`. This packet edits no
  candidate class, no path allowlist, no author and no `check_exclusions`. It
  changes what an approval, once one can exist, is ALLOWED TO RELEASE — not who
  may give one or on what.
* **The floor composition is not carved.** `.github/workflows/merge-master-approval.yml:1499-1506`
  still parks any candidate touching a never-clearable path before the envelope
  is consulted, and `contracts/review-lane-pin.yaml` is still such a path. The
  N-1b carve is codexFactory's decision core to author and is not asked for here.
* **The pin, the snapshot and their witnesses do not move**, and no ruleset,
  credential, schema or contract member is touched by this packet or by its
  realization.

## The realization gate, stated rather than buried

**RATIFYING THIS PACKET AND REALIZING IT CHANGES NO OBSERVABLE BEHAVIOUR IN THIS
REPOSITORY, AND — UNLIKE ITS CODEXFACTORY TWIN — THERE IS NO SINGLE OWNER'S
CLICK THAT WOULD MAKE IT LIVE.** That asymmetry is the whole reason D-6 split the
two packets, and it is put here so nobody reads the mirror as buying what the
twin buys.

**Four things stand between an armed re-pin pull request and a completed merge.
Measured live on 2026-09-08 against `opensoft/openxFactory`, every figure read
back from the API or the tree rather than remembered:**

| # | the refusal | measured |
|---|---|---|
| 1 | **No candidate class admits the lane.** `.github/merge-approval-envelope.yml` has exactly one entry, `intent-rolling-custody` (`expected_head_ref: intents/rolling`, allowlist `ideation/dashboard/intents/**` + `ideation/dashboard/gate-records/**`). The re-pin lane's branch is `bot/review-lane-repin` and its four writable files are none of those. | the envelope file, and `tests/review_lane_pin/test_review_lane_caller.py`, which pins that exact shape |
| 2 | **The floor is composed OVER the envelope.** `.github/workflows/merge-master-approval.yml:1504` parks when `FLOOR_MATCHED != 0`, *"whatever the envelope says"* — and `contracts/review-lane-pin.yaml`, which every advance writes, is a never-clearable floor member whose stated ground is that a clearable pin *"would let a pull request choose its own judge"*. | the caller at `:1499-1506`; the floor entry in the vendored snapshot |
| 3 | **Code-owner review is required on `main`, every path the lane writes is code-owner routed, and NO BYPASS GRANT IS RECOMMENDED TO LIFT IT.** Ruleset **`18834180`** is ACTIVE with `require_code_owner_review: true`, `dismiss_stale_reviews_on_push: true`, count `0` — and it is an **ORGANIZATION** ruleset over `repository_name: ~ALL` / `ref_name: ~DEFAULT_BRANCH`, which is where this repository's code-owner gate comes from (`18962101` has `require_code_owner_review: false`). `.github/CODEOWNERS` routes all four sites: `.github/workflows/` (`:2`) covers `merge-master-approval.yml` and `pytest-suite.yml`, `:20` covers `/contracts/review-lane-pin.yaml`, `:27` covers `/contracts/review-lane-floor-snapshot.yaml`. **A GitHub App cannot be named in CODEOWNERS**, so the merge-master App's approval cannot SATISFY the rule — and the bypass remedy is WITHDRAWN (§ below). | `gh api orgs/opensoft/rulesets/18834180`; `gh api repos/opensoft/openxFactory/rules/branches/main`; the tree |
| 4 | **A promoted requirement forbids the approval outright.** codexFactory `openspec/specs/merge-master-approval/spec.md` § *Bounded autonomous surface* forbids autonomously approving any CODEOWNERS-scoped path. `extend-merge-master-envelope-to-floor-bot-lanes` narrowed it — under ratified decision **N-1, for the codexFactory REGENERATION lane only**; this lane was expressly left on a human merge word. | that packet's N-1 and its `## MODIFIED` block |

**So the successor is an ENROLMENT PACKET, and it is named here and NOT authored
here.** Its shape, so the naming is a referent and not a gesture:

> **`admit-review-lane-repin-to-merge-approval-envelope`** (openxFactory) — a
> second candidate class in `.github/merge-approval-envelope.yml` for the re-pin
> lane: `expected_head_ref: bot/review-lane-repin`; `expected_author:
> openxfactory[bot]` (**measured**, not assumed — `gh api
> repos/opensoft/openxFactory/pulls/732 --jq .user.login` on the lane's own
> observed advance); `expected_base_ref: main`; `path_allowlist` naming **exactly
> the four files the lane writes** — `contracts/review-lane-pin.yaml`,
> `contracts/review-lane-floor-snapshot.yaml`,
> `.github/workflows/merge-master-approval.yml`,
> `.github/workflows/pytest-suite.yml` (the five sites of
> `scripts/review_lane_repin.py:115-140`, two of which live in one file);
> `require_all_checks: true`; `check_exclusions` at least
> `[merge-master-approval, lane-line]`. It must additionally carry, or wait on,
> the **N-1b (ii) carve** for refusal 2 and an **owner's bypass act** for
> refusal 3, and it must reckon with refusal 4 — which is codexFactory's
> promoted text, so the enrolment is a two-repository packet exactly as § 6.3
> was.

**Until that successor lands, this packet's realization is observably inert** —
the arming is recorded, reported, and never fires. That is stated in the
requirement itself as its own scenario, so the inert state is a CONFORMING state
and not a silent failure. `tasks.md` § 4 says which box each of those acts ticks.

### The completion path is OPEN, and no bypass is proposed

**The remedy codexFactory's D-4 (i) recommended — add the merge-master App as a
bypass actor on ruleset `18834180` — was WITHDRAWN on 2026-09-08** (codexFactory
[#232](https://github.com/opensoft/codexFactory/issues/232) comment
`5585989018`, the guard firing under Brett Heap's own instruction to verify the
mechanism before acting). **This packet therefore proposes no bypass actor
anywhere**, and the withdrawal's grounds bind harder here than in codexFactory:

* bypass is per-ACTOR and is exercised by the actor taking the restricted
  action; the merge-master App submits a review and merges nothing, so a grant to
  it would never be exercised;
* the async auto-merge completion path is reported not to honour `bypass_actors`
  at all (community discussion
  [#162623](https://github.com/orgs/community/discussions/162623), with a repro
  on exactly this rule combination);
* **`18834180` is an ORGANIZATION ruleset over `~ALL` repositories**, so an entry
  on it grants that App bypass of the code-owner rule — plus `deletion` and
  `non_fast_forward`, because bypass is per RULESET and not per rule — on the
  default branch of every repository in `opensoft`. **In this repository it would
  remove the very gate that makes the pin's code-owner routing binding.**

**And the escape codexFactory has does not exist here.** There, the regeneration
bot writes ONE file, so relocating it off every CODEOWNERS-matched prefix
satisfies the code-owner rule vacuously with no bypass at all. Here the lane
writes FOUR files and **two of them are workflow files**, which cannot be
relocated off `.github/workflows/`; un-routing that prefix is refused on its face
as the 2026-08-23 convener ruling's routing for assembly-class gate surfaces. So
there is no relocation shape for this lane, and that is a measurement.

**What is put for Brett Heap's word, rather than assumed** (`design.md` M-D
enumerates all seven shapes with their costs): the PRECONDITION first — does
auto-merge fire at all on a rulesets-only `main`? `GET
/repos/opensoft/openxFactory/branches/main/protection` returns `404 "Branch not
protected"`, so protection here is rulesets-only, which is the configuration
#162623 reports auto-merge does not fire in; and **zero of the last 60 closed
pull requests in this repository carry a non-null `auto_merge`** — the mechanism
this packet admits has never once fired here. One throwaway armed pull request
settles it. **Until it is settled, every discussion of a completion shape is
premature**, and `design.md` M-G gates the live proof on BOTH the enrolment
successor AND that word.

**None of this changes what the packet asks for.** The narrowing is canon text;
it costs nothing while inert; and it is what stops the two repositories' twin
sentences from diverging while the completion question is open.

## This repository's own merge facts, measured

Stated for THIS repository rather than copied from codexFactory's D-1/D-2, because
three of them differ and the difference changes a recommendation.

| fact | `opensoft/openxFactory` | `opensoft/codexFactory`, for contrast |
|---|---|---|
| `allow_auto_merge` | **`true`** — the platform mechanism this packet's grant relies on is available | `true` |
| merge methods (repository) | **`merge: true`, `squash: true`, `rebase: true`** — all three | `merge: true`, `squash: false`, `rebase: false` |
| merge methods (rulesets) | `allowed_merge_methods: [merge, squash, rebase]` on both `pull_request` rules | same list |
| required status checks | **`signed-execution-chain-gate`, `lane-line`** (ruleset `21957695`) and **`wallet-validation`, `pytest-suite`, `lane-line`, `release-tag-gate`** (ruleset `21538893`) | `validate`, `lane-line` (ruleset `18793528`) |
| `strict_required_status_checks_policy` | **`false` on both** — a branch need not be up to date to merge | **`true`** |
| code-owner review | **required** — ruleset `18834180`, `require_code_owner_review: true`, `dismiss_stale_reviews_on_push: true`, count `0`; bypass actors: `OrganizationAdmin` only | identical ruleset id, same parameter |
| approving reviews | **`1`** required by ruleset `18962101`, with `require_last_push_approval: true` | `1` by `18962101` and `1` by `18793528` |
| unattributed changes | `require_extra_approval_for_unattributed_changes: true` on both `pull_request` rules | same on all three |
| observed bot merge | PR **#732** (`bot/review-lane-repin`, author `openxfactory[bot]`) merged 2026-09-06T23:46:28Z as `9ffc6252`, **one parent** — a SQUASH | #248/#254 merged as merge commits |
| classic branch protection on `main` | **ABSENT** — `404 "Branch not protected"`; protection is **rulesets-only** | also absent (`404`) |
| rulesets binding `main` | **all FIVE are ORGANIZATION rulesets**; the repository holds none of its own | same pattern |
| pull requests ever auto-merged | **ZERO** of the last 60 closed | zero across the estate |

**Two consequences follow and are carried into `design.md` rather than left
implicit.** First, `strict_required_status_checks_policy: false` here means the
head-moves-under-an-armed-advance latency codexFactory's D-1 warns about does not
arise from a mandatory up-to-date push — this lane's own single-flight update path
is what moves the head, and `dismiss_stale_reviews_on_push: true` still dismisses
the approval when it does, so the head-binding scenario holds for the same reason
by a different route (**M-A**). Second, this repository permits all three merge
methods, so unlike codexFactory the method is a CHOICE and must be made
deliberately; the lane's own observed precedent is a squash (**M-B**).

## What is NOT proposed

* **No enrolment.** The candidate class above is NAMED as the successor and is
  not authored here. Adding a second candidate to this repository's envelope is
  not a configuration change — it is a new grant needing its own word or its own
  council record, which is why `.github/merge-approval-envelope.yml` is routed to
  a code owner.
* **No carve of the floor composition, and no removal of any floor path.**
  `contracts/review-lane-pin.yaml` stays never-clearable.
* **No ruleset act, by any agent, and NO BYPASS ACTOR PROPOSED AT ALL.** The
  bypass shape codexFactory's D-4 (i) recommended was withdrawn on 2026-09-08 and
  is not revived here in any form. `tasks.md` § 4 carries the completion-path
  question as a dependency awaiting a word, not as an act to be taken.
* **No merge queue and no administrative merge.** Both are refused by name in the
  requirement, and the sweep keeps looking for both.
* **No second approver, and no self-approval under a second identity.** The
  narrowing admits ARMING, and arming is not approving.
* **No change to codexFactory.** Its amendment is ratified, landed and read here;
  this packet authors no byte of it.
