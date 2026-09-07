# Design: extend-merge-master-envelope-to-floor-bot-lanes

Status: draft

Every claim in § 1 and § 2 was read out of the working tree or the GitHub API at
authoring time and is cited `file:line`. Where the governing brief's premise and
the tree disagree, the tree is written down and the difference is flagged — § 1.1
is one such place and it is not a small one.

## 1. What the envelope actually is

### 1.1 Where it is declared — and the correction

The merge-approval envelope for this repository is declared in
**`.github/merge-approval-envelope.yml`**. It is not a `contracts/` policy and
not a `hermes/` document; it is a code-owner-routed file under `.github/`
(`.github/CODEOWNERS:8` names `/.github/merge-approval-envelope.yml`).

**THE BRIEF'S PREMISE IS WRONG FOR THIS REPOSITORY, and the correction matters
to every decision below.** The brief states that openxFactory's
`merge-master-approval` lane "approves ONE bot lane today — the doc-health
nightly (`doc-health-bot`)". It does not. openxFactory's envelope enrols exactly
one candidate and that candidate is **`intent-rolling-custody`** — the rolling
intent-custody pull request the aggregation intent-apply lane pushes
(`.github/merge-approval-envelope.yml:55-62`), authored by `openxfactory[bot]`
(`:70`), on the exact head ref `intents/rolling` (`:73`), confined to
`ideation/dashboard/intents/**` and `ideation/dashboard/gate-records/**`
(`:101-103`).

`doc-health-nightly` is a candidate in a DIFFERENT repository — `opensoft/xFactory`'s
own `.github/merge-approval-envelope.yml` — and this repository's envelope cites
it only as THE PRECEDENT IT MIRRORS (`.github/merge-approval-envelope.yml:42-48`:
"bot author, exact head ref, narrow derived-tree path allowlist,
`require_all_checks: true`, self-excluding check name. Live since 2026-07-28 and
narrowed by the council's own R5 on 2026-08-26. The candidate below is the same
shape over a different derived tree.").

Why the difference is load-bearing rather than pedantic: the admission precedent
this repository actually has is **a derived-tree custody lane on paths NO CODE
OWNER GATES**. That is the property § 2.2 shows both floor bot lanes lack, and
it is the property that made `intent-rolling-custody` a workable "narrow first
candidate" in the first place.

The grant is recorded where a reader meets it: Brett Heap, 2026-09-06, on
openxFactory #656, verbatim *"author the envelope PR now as a narrow first
candidate"*, and "HIS MERGE WORD ON THAT PULL REQUEST IS THE GRANT, and it is a
grant for the ONE candidate class enrolled below and for nothing else"
(`.github/merge-approval-envelope.yml:8-13`). It landed as
[#735](https://github.com/opensoft/openxFactory/pull/735), merge `6d3237e6`, the
only commit in the file's history. The file states its own extension rule:
"Adding a second is not a configuration change: it is a new grant, needing its
own word or its own council record" (`:24-27`). **This packet is the request for
that word.**

### 1.2 How admission is decided, and by whose code

openxFactory re-implements none of the decision. The evaluating code is
codexFactory's `scripts/merge_master/envelope.py`, checked out at the commit
`contracts/review-lane-pin.yaml` pins (`.github/merge-approval-envelope.yml:3-6`;
pin `core_commit: "19f2ab0c9f04d4cf24af11c2551cb1a19263e41b"` at
`contracts/review-lane-pin.yaml:60`). The schema is codexFactory's
`schemas/merge-approval-envelope.schema.json`.

The conditions the core evaluates, in order, are exactly these — read out of
`envelope.py` rather than assumed:

| # | Condition | Where |
|---|---|---|
| 1 | candidate class — `target_repos`, author (`expected_author` or `author_class`), head ref (`expected_head_ref` or `head_ref_pattern`), `expected_base_ref`, `require_same_repository` | `envelope.py:510-610`, phase-one gate list |
| 2 | `path_allowlist` — every changed path inside it; **no changed paths at all parks** | `envelope.py:997-1008` |
| 3 | `require_all_checks` — latest completed run per non-excluded check name concluded success, minus `check_exclusions` | `envelope.py:1010-1019` |
| 4 | no open regression/security finding — `open_finding_title_prefixes`, `open_finding_labels` | `envelope.py:1021-1025` |
| 5 | idempotency — already approved by the merge-master identity for this head | `envelope.py:1027-1038` |

**THERE IS NO DIFF-SHAPE CONDITION.** No member of the schema and no branch of
`evaluate()` inspects whether a diff is additions-only, pin-only, or confined to
a machine-generated block. That is a finding with a direct consequence for N-2:
the shape guarantees the two lanes rely on are supplied by THE LANES' OWN JUDGES,
and the only thing the envelope contributes is `require_all_checks: true`, which
conjuncts those judges in as check-runs on the head. An enrolment that ASSERTS
"pin-only shape" as an envelope condition would be asserting something the
envelope cannot measure.

Two structural safeguards are already in place and are relied on below rather
than re-invented. The envelope and the core are read **from the base branch
only** — `merge-master-approval.yml` runs on `pull_request_target`, no step
checks out or executes head content, and any diff editing the envelope file
lands outside every `path_allowlist` in it
(`.github/merge-approval-envelope.yml:31-40`). And the approval is reachable
through exactly one door: every approval-shaped step carries
`steps.envelope.outputs.decision == 'approve'`, written by nothing but the pinned
core's exit code (`merge-master-approval.yml:61-70`, submit step at `:1706`).

### 1.3 What the lane does NOT do, and why it matters here

`merge-master-approval.yml:47-50` and `:74-76`: **"NO MERGE, EVER. This lane
submits a review and stops. It issues no merge call and enables no auto-merge —
the aggregation's own intent-apply lane arms GitHub's auto-merge on its side
(ruling D-3 on #656)"**, and the test refuses every merge-shaped string in the
file.

So an envelope approval, on its own, lands nothing. Whatever is enrolled, the
lane that opens the pull request must arm auto-merge itself. Neither
`.github/workflows/review-lane-repin.yml` nor codexFactory's
`.github/workflows/floor-regeneration.yml` does so today. This is a realization
item nobody would derive from the § 6.3 wording, and it is carried into § 6.

## 2. The three refusals standing between the bot lanes and the envelope

### 2.1 Refusal one — the floor is composed OVER the envelope

`.github/workflows/merge-master-approval.yml:1494-1501`, verbatim:

```
          # ---- the floor, composed OVER the envelope ------------------------
          # `matched` is the number of never-clearable paths this candidate
          # touches, computed by the pinned core in step 8. Anything but a
          # literal `0` — including an EMPTY value, which is what a skipped or
          # failed floor step leaves — refuses.
          if [ "${FLOOR_MATCHED:-}" != "0" ]; then
            park "the candidate touches the repository gate floor (matched=${FLOOR_MATCHED:-unavailable}); a never-clearable path is never autonomously approvable, whatever the envelope says"
          fi
```

And `contracts/review-lane-pin.yaml` IS a never-clearable floor member. In
codexFactory `scripts/merge_master/openxfactory-review-authority-floor.yaml`, at
line 112, under the ground written at `:108-111`:

```
    # A fourth, separately grounded entry (not part of the wallet-register
    # trio above): the review-lane pin selects which codexFactory commit's
    # decision core judges this repository. Clearable, it would let a pull
    # request choose its own judge.
    - contracts/review-lane-pin.yaml
```

The re-pin bot writes that exact path. Measured, not assumed — openxFactory PR
#732, read from the API, changed exactly four files: `contracts/review-lane-pin.yaml`,
`contracts/review-lane-floor-snapshot.yaml`,
`.github/workflows/merge-master-approval.yml`, `.github/workflows/pytest-suite.yml`
(the five sites of `scripts/review_lane_repin.py:115-140`, two of which live in
one file).

**Therefore: enrolling the re-pin lane in the envelope today changes nothing.
The candidate parks at line 1499 before the envelope is consulted.** The § 6.3
objection is not an argument to be weighed against the convenience — it is the
gate, in code, and it fires first.

### 2.2 Refusal two — code-owner review, in both repositories

Ruleset `Require Code Owner Review` (id 18834180) is **ACTIVE** on
`opensoft/openxFactory` with `require_code_owner_review=true`, and the identically
named ruleset (same id) is **ACTIVE** on `opensoft/codexFactory` with the same
parameter. Both read from the API at authoring time. The only bypass actor on
openxFactory's is `OrganizationAdmin … always`.

Every path either bot lane writes is code-owner gated:

| Lane | Path written | CODEOWNERS entry |
|---|---|---|
| re-pin | `.github/workflows/merge-master-approval.yml`, `.github/workflows/pytest-suite.yml` | openxFactory `.github/CODEOWNERS:1` `.github/workflows/ @brettheap` |
| re-pin | `contracts/review-lane-pin.yaml` | openxFactory `.github/CODEOWNERS:6` |
| re-pin | `contracts/review-lane-floor-snapshot.yaml` | openxFactory `.github/CODEOWNERS:7` |
| regeneration | `scripts/merge_master/openxfactory-review-authority-floor.yaml` | codexFactory `.github/CODEOWNERS:29` `/scripts/ @brettheap` |
| regeneration | `tests/merge-master/test_repository_gate_floor.py` (only when floor membership changes; `scripts/merge_master/floor_regeneration.py:577-641`, the LS-A3 `SPECS_FLOOR_PATHS` mirror) | codexFactory `.github/CODEOWNERS` — `/tests/**` is covered per the note at `:107` |

A GitHub App cannot be named in CODEOWNERS. So the merge-master App's APPROVE
review does not, and cannot, satisfy code-owner review on any of these paths.
**This is why `intent-rolling-custody` was a workable first candidate and these
are not**: its two admitted prefixes appear in no CODEOWNERS entry at all.

Clearing this needs an owner's act, and there are only three shapes of it:
(a) add the merge-master App as a bypass actor on the `Require Code Owner Review`
ruleset in the repository concerned — narrow, visible in the ruleset, reversible
in one click, and it lifts ONLY that ruleset for that App; (b) remove the paths
from CODEOWNERS — refused here, it weakens the human gate on a governance surface
for every author, not just the bot; (c) keep the human click. § 5 carries (a) as
the enabling act and names (c) as what happens if it is refused.

### 2.2a Refusal three — and it is PROMOTED CANON, not configuration

The three sections around this one describe settings and code. This one
describes a ratified requirement, and it is the reason none of the options below
is a configuration change.

codexFactory `openspec/specs/merge-master-approval/spec.md:175-186`, **promoted**,
originally ratified by `2026-07-28-add-merge-master-autonomous-approval`:

```
### Requirement: Bounded autonomous surface

The autonomous-approval mechanism MUST NOT approve any pull request outside
the allowlisted bot-authored in-envelope surfaces, and MUST NOT approve any
pull request on a surface scoped to a human gate (a CODEOWNERS-scoped path) or
authored by a human. …

#### Scenario: A human-gated surface is untouched

- **WHEN** a candidate pull request touches any CODEOWNERS-scoped path
- **THEN** no autonomous approval is submitted and the human gate is required
```

**Every path either bot lane writes is a CODEOWNERS-scoped path** — § 2.2's table
is the enumeration. So the prohibition is not incidental to these two lanes; it
names them exactly.

And it has been REAFFIRMED, not relaxed, by the change that widened this
mechanism the furthest. codexFactory's active `add-regular-pr-council-clearance`
carries a `## MODIFIED` block on this very requirement
(`openspec/changes/add-regular-pr-council-clearance/specs/merge-master-approval/spec.md:130`,
scenario at `:143`) which keeps the CODEOWNERS clause intact, and its proposal
states the position in terms that leave no room for reading it as a soft default:
*"CODEOWNERS-scoped governance paths remain absolutely forbidden"*
(`proposal.md:527`), *"Human-authored, CODEOWNERS-scoped … remain parked for the
human gate"* (`:622`). Even the tier-2 council-clearance route — a unanimous
SHA-pinned council verdict — does not reach a CODEOWNERS-scoped path.

**The consequence, stated plainly: admitting EITHER lane requires a `## MODIFIED`
narrowing a promoted requirement that the estate has just re-declared absolute.**
Not a config edit, not a ruleset click, and not something a lane may do quietly
as part of a realization. It changes the answer to N-1's cost comparison (§ 2.4),
to N-5's surface, and to OQ-2 — which this finding effectively answers.

### 2.3 Refusal four — codexFactory's envelope does not admit this author or this surface

codexFactory `.github/merge-approval-envelope.yml` enrols one candidate,
`codexfactory-routine-code` (`:29`). It fails the regeneration lane twice over:

- **author** — `author_class.content_app_logins: [codexfactory[bot]]` (`:49-50`).
  The regeneration bot authors as `openxfactory[bot]`: codexFactory PRs #248,
  #254 and #265 all report `author = app/openxfactory`, read from the API.
- **surface** — `path_allowlist` is `catalog/** examples/** ideation/**
  profiles/** tenants/** specs/** README.md CONTRIBUTING.md` (`:68-76`).
  `scripts/**` and `tests/**` are outside it, deliberately and by the design note
  at `:33-39`.

Unlike openxFactory's, codexFactory's `merge-master-approval.yml` composes NO
repository gate floor over its envelope — grepped for `repository_gate_floor`,
`FLOOR_MATCHED` and `never_clearable`, none present. Its floor lives inside the
tier-2 clearance rule `scripts/merge_master/codexfactory-routine-code-clearance.yaml`,
which is a separate mechanism. So on the codexFactory side there is **exactly one
refusal to clear (§ 2.2's code-owner review) plus one new candidate class to
declare** — no floor is touched, and no decision-core code changes.

### 2.4 What the measurement adds up to

| | codexFactory regeneration lane | openxFactory re-pin lane |
|---|---|---|
| floor composed over the envelope | not present (§ 2.3) | **refuses today** (§ 2.1) |
| code-owner review ruleset | one bypass act (§ 2.2) | one bypass act (§ 2.2) |
| promoted "Bounded autonomous surface" | **`## MODIFIED` required** (§ 2.2a) | **`## MODIFIED` required** (§ 2.2a) |
| candidate class exists | no — must be declared | no — must be declared |
| decision-core change needed | none | **yes** — carve the composition at `merge-master-approval.yml:1499` |
| governance grounds weakened | ONE — the CODEOWNERS-scoped prohibition | TWO — that, plus "choose its own judge" |

**NEITHER LANE IS A CONFIGURATION CHANGE.** That is the correction § 2.2a forces,
and it is the single most important thing on this page: the § 6.3 framing, the
governing issue and this packet's own first draft all treated the extension as an
enrolment plus a click, and it is not. Both lanes require narrowing a promoted
requirement that codexFactory canon calls absolutely forbidden.

What survives the correction is the ASYMMETRY, and it is what N-1 turns on: the
regeneration lane weakens ONE ground, the re-pin lane weakens that same ground
AND the "choose its own judge" ground, and additionally needs a decision-core
carve and a re-pin cycle to make the carve live. The regeneration lane is
strictly cheaper by every measure, and each lane buys back exactly one of the two
clicks.

## 3. Authoring decisions

Each decision states the recommendation, the alternatives, and what a veto costs.
**None is settled by being written here.** Ruling on them is § 5.2.

### N-1 — SCOPE. Which lanes are admitted

**RECOMMENDED: admit the codexFactory regeneration lane ONLY. Leave the
openxFactory re-pin lane on a human merge word.**

Grounds, all from § 2, and stated with the § 2.2a correction included rather than
around it. **This is not a cheap option; it is the cheapest option that exists.**
The regeneration lane costs one new candidate class in a code-owned file, one
shape assertion, one auto-merge step, one ruleset bypass act, AND a `## MODIFIED`
narrowing the promoted `Bounded autonomous surface` requirement — because its one
writable path is code-owner scoped and canon forbids approving there. It weakens
exactly ONE governance ground, that one.

What it does NOT weaken, and this is the whole of the asymmetry:
`scripts/merge_master/openxfactory-review-authority-floor.yaml` is not on any
floor composed over any envelope (§ 2.3), its content is machine-generated from a
source of truth in another repository, its diff is judged by codexFactory
`validate` and by `tests/merge-master/test_repository_gate_floor.py`, and
reverting the merge restores the prior tree exactly. The re-pin lane costs
everything above PLUS a change to the pinned decision core making a
never-clearable floor member conditionally clearable — the thing the floor's own
comment exists to prevent — PLUS a re-pin cycle to make that carve live.

The benefit is symmetrical and small: the cycle costs two human merges, and
admitting either lane removes one of them. **One click per cycle is what is being
bought, and § 2.2a is the price.** Whether that trade is worth taking at all is
N-1 (d), and it is a serious option rather than a courtesy one.

Alternatives, each one veto away:

- **(b) admit BOTH.** The re-pin admission additionally requires N-1b below. Take
  this if the residual risk in N-1b is judged acceptable and the second click is
  worth it. The packet is written so that a veto to (b) adds requirements rather
  than rewriting them — the `review-lane-floor-mirror` delta names both lanes and
  conditions the re-pin lane on the carve.
- **(c) admit the re-pin lane ONLY.** The brief's own reading, and it is the one
  option the measurement rules out: it is the more expensive lane, not the
  cheaper one. Recorded so the inversion is on the record rather than silently
  dropped.
- **(d) neither — status quo.** Two clicks per cycle, nothing carved, nothing
  declared, and no promoted requirement narrowed. **Strengthened by § 2.2a into a
  serious contender rather than a courtesy option**: the lanes are a day old,
  three defects were found by running them, the thing being bought is one or two
  clicks on an hourly cycle, and the price is narrowing a requirement the estate
  re-declared absolute eleven days ago. A reader who ranks those differently to
  this packet should take (d), and the packet is written so that (d) costs
  nothing already spent.
- **(e) SATISFY THE CANON INSTEAD OF NARROWING IT — move the derived artifact off
  the code-owner-gated surface.** `Bounded autonomous surface` forbids approving
  on a CODEOWNERS-scoped path. It says nothing against approving a
  machine-generated artifact that is not on one. Splitting the floor document's
  machine-generated block into its own file outside `/scripts/` — read by the
  core exactly as now, with the hand-reasoned chokepoints staying where they are
  and staying code-owned — would leave the prohibition intact, word for word,
  and make the regeneration lane admissible under canon as written. **Not
  recommended for THIS packet, and the reason is scope, not merit**: it is a
  change to what the decision core reads and to the floor document's shape, it
  touches `repository_floor_drift.py` and the LS-A3 mirror, and it is
  codexFactory's architecture to decide. It is recorded because it is the only
  option on this page that buys the click WITHOUT weakening a governance ground,
  and an owner reading § 2.2a should know it exists before ruling. If N-1 is
  refused on § 2.2a grounds, **(e) is the successor to file.**

### N-1b — THE CARVE, and it is only live if N-1 is vetoed to (b)

If the re-pin lane is to be admitted, `merge-master-approval.yml:1499` must stop
refusing it. Three shapes, and the difference between them is everything:

- **(i) leave the floor composition alone.** Then the re-pin lane cannot be
  enveloped, and (b) collapses into the recommendation. This is what "admit both"
  means if no carve is made, and it should be said out loud rather than
  discovered at realization.
- **(ii) RECOMMENDED IF (b) IS CHOSEN — a carve for one named enrolled candidate,
  authored in codexFactory's decision core.** The composition would refuse as it
  does today unless ALL of: the candidate is the named enrolled re-pin class; its
  floor-matched set is exactly `{contracts/review-lane-pin.yaml}` and nothing
  else; and every other envelope condition holds. The path stays never-clearable
  for every other candidate and every other author. It is a carve, not a removal
  — `contracts/review-lane-pin.yaml` is not taken off the floor, and
  `repository_floor_drift.py` continues to catch its removal.
- **(iii) remove `contracts/review-lane-pin.yaml` from the floor. REFUSED, and
  this packet will not author it.** That is precisely the state the ground at
  `openxfactory-review-authority-floor.yaml:108-111` exists to prevent.

**The residual risk under (ii), stated plainly rather than argued away.** The
re-pin pull request moves the pin that selects which codexFactory core judges the
NEXT pull requests. Approving it autonomously means the envelope approves a
change to its own future judge. The safeguards that bound it, each verified:

1. **The lane cannot choose an arbitrary core.** `review-lane-repin.yml:259-267`
   resolves codexFactory's default branch AT RUN TIME and refuses to pin at any
   other reference; the header at `:41-43` records that the lane "ignores any
   commit, branch or reference named by its trigger" and that the payload is never
   read. So the only value the lane can ever propose is codexFactory's own
   default-branch head.
2. **The candidate core judges the candidate.** `pytest-suite`'s LQ-A7 freshness
   verifier (`tests/review_lane_pin/test_floor_snapshot.py::TheFreshnessVerifier`)
   runs against the core the pull request proposes, and it is a required check —
   so `require_all_checks: true` conjuncts it in.
3. **The five sites move together or nothing opens.** `scripts/review_lane_repin.py:28`,
   ":It moves ALL FIVE SITES or it opens nothing, and it proves the move by
   reading it back", and `:35` "It writes nothing outside the five sites".
4. **The rules are read from the base branch.** § 1.2. The pull request cannot
   edit the class that approves it.
5. **A human can still veto by closing the pull request**, and the kill switch of
   N-4 returns the lane to human merges in one edit.

What none of that removes: a codexFactory default-branch head that is itself bad
would be pinned automatically, one hour after it lands, with no human in the
path. Today a human reads that pull request. That is the risk being bought, and
it is why the recommendation is (a).

### N-2 — ADMISSION CONDITIONS. What is measured

**RECOMMENDED: the conditions are exactly the members the schema and the core
already carry, filled with values MEASURED off the observed bot pull requests,
and NOTHING is asserted that the envelope cannot check.**

For the codexFactory regeneration candidate:

| Member | Value | Measured from |
|---|---|---|
| `target_repos` | `[opensoft/codexFactory]` | — |
| `expected_author` | `openxfactory[bot]` | cxF #248/#254/#265 `author = app/openxfactory` |
| `expected_head_ref` | `floor/bot-regeneration` (exact form, not the pattern form) | the same three pull requests |
| `expected_base_ref` | `main` | the same three |
| `require_same_repository` | `true` | the fork defence on `pull_request_target` (cxF envelope `:61-65`) |
| `path_allowlist` | the two paths named EXACTLY, no globs: `scripts/merge_master/openxfactory-review-authority-floor.yaml`, `tests/merge-master/test_repository_gate_floor.py` | cxF #248/#254/#265 changed exactly the first; the second moves only on a membership change (`floor_regeneration.py:613-641`) |
| `require_all_checks` | `true` | the precedent, and the only way the lane's own judges bind |
| `check_exclusions` | `[merge-master-approval]` | self-reference deadlock, cxF envelope `:81-88` |
| `revert_suffices` | `true` | the block is machine-derived; reverting restores the prior tree |

**And what is deliberately NOT declared, each with its reason.** No diff-shape
condition, because § 1.2 shows the envelope has none and inventing one would mean
a schema change plus a core change to express a property the lane's own required
checks already prove. No `open_finding_title_prefixes`/`labels`, on the same
ground `intent-rolling-custody` records at `.github/merge-approval-envelope.yml:120-130`
— no finding class in codexFactory is ABOUT the generated floor block, so a prefix
would park this lane on unrelated repository-wide findings; if a finding class
ever does tie to this surface it is a one-line reviewed edit. No
`head_ref_pattern`, because the exact form is available and a pattern admits more
than is meant.

Alternative: declare a `head_ref_pattern` of `floor/**` and a broader
`path_allowlist` of `scripts/merge_master/**`. **Not recommended** — an allowlist
is bought precisely for the failure direction where a mistyped entry admits
nothing, and `scripts/merge_master/**` would admit the decision core itself.

### N-3 — ORDERING. The re-pin must not outrun the regeneration

**RECOMMENDED: record the property as a requirement and add NO new mechanism,
because the property already holds structurally and a second enforcement of it
would be a second thing to keep true.**

The rule is that the envelope must never approve a re-pin whose core commit is
not codexFactory's default-branch head. It holds because
`review-lane-repin.yml:259-267` resolves that head at run time and refuses every
other reference — the lane is structurally incapable of proposing a core that is
not on `main`, whatever its trigger says. Under N-1 as recommended the question
is moot for the envelope entirely, since the re-pin lane is not enrolled; the
requirement is still written, because it must hold before any future admission.

Alternative: add an explicit envelope condition comparing the proposed core to
the source repository's default-branch head. **Not recommended** — it needs a new
schema member and a new core branch to express what the lane already refuses to
violate, and a condition that can never fire is a condition nobody maintains.

### N-4 — OBSERVABILITY AND THE KILL SWITCH

**RECOMMENDED: the approval comment already exists and is extended, not
replaced; and the kill switch is the candidate entry itself.**

The lane already posts a sticky comment on approve and on park, carrying the
decision, the candidate id and the core's reason, and stating the narrowness of
the grant (`merge-master-approval.yml:1740`, `:1767-1799`). What a floor-lane
approval should add to it, and it is all already computed: the measured changed
path set, the floor-matched count, and the check names the all-green condition
quantified over. A human is told by that comment on the pull request itself; no
separate #232-style record is proposed, because a record nobody is obliged to
write is a record that stops being written — the comment is on the artifact.

**The kill switch is the candidate entry.** Deleting it from
`.github/merge-approval-envelope.yml` returns the lane to human merges, takes one
edit, is a code-owner-reviewed act by construction, is read from the base branch
so it takes effect on the next run, and is visible in the diff forever.

Alternatives: a boolean `active:` member on the candidate — **not recommended**,
it is a schema change, and a disabled entry reads as enrolled to anyone skimming;
a repository variable — **refused**, it is invisible in the diff and defeats the
whole reason the envelope is a reviewed file.

### N-5 — REALIZATION SURFACE

**RECOMMENDED: the realization is a codexFactory COMPANION CHANGE and this
openxFactory packet, and the openxFactory half carries no code at all under the
recommended scope.**

Under N-1 (a), recommended:

| Repo | File | Change |
|---|---|---|
| codexFactory | `.github/merge-approval-envelope.yml` | second candidate `openxfactory-floor-regeneration`, per N-2 |
| codexFactory | `tests/merge-master/test_enrolled_surface_config.py` | assert the exact new shape — two candidates, these exact paths, `require_all_checks: true` |
| codexFactory | `.github/workflows/floor-regeneration.yml` | arm auto-merge on the opened pull request (§ 1.3 — the approval merges nothing) |
| codexFactory | `openspec/specs/merge-master-approval/spec.md` § *Bounded autonomous surface* | **`## MODIFIED`, and it is the load-bearing act** (§ 2.2a) — narrow the CODEOWNERS-scoped prohibition to admit one named machine-derived class, leaving it absolute for every other candidate and every human author |
| codexFactory | ruleset `Require Code Owner Review` | add the merge-master App as bypass actor — **Brett's act**, § 5.3 |
| openxFactory | this packet's spec deltas | the rules; no code |

The codexFactory companion is therefore **not a configuration pull request**. It
carries a `## MODIFIED` on promoted canon and belongs in that repository's normal
governance path with whatever instrument OQ-2 selects. **It is authored, as draft
[codexFactory #272](https://github.com/opensoft/codexFactory/pull/272)** — the
narrowing, its two added scenarios, a recommendation for a Gate-Rules Council
record (its OQ-C1) and a reasoned deferral of the two-writers declaration against
the sibling `add-regular-pr-council-clearance` (its OQ-C2, with the finding that
forced the deferral measured rather than asserted: carrying that sibling's
retitled scenario reports an undispositioned strict-validation ERROR, and an
unratified draft may not borrow a ratification to clear one).

Under a veto to N-1 (b), add: openxFactory `.github/merge-approval-envelope.yml`
(second candidate), `tests/review_lane_pin/test_review_lane_caller.py` (its
shape), `.github/workflows/review-lane-repin.yml` (arm auto-merge), the
openxFactory ruleset bypass, and the codexFactory decision-core carve of N-1b(ii)
with its own tests — after which the openxFactory pin must be advanced to the
carrying core before the carve is live, which is itself a re-pin cycle.

`code_surface:` is therefore NOT `none`, and per `release-realization` this packet
archives only on merged and green realization evidence. That evidence is named in
`tasks.md` § 4 and is deliberately behavioural: **one bot pull request of each
admitted kind landed with no human click.** An enrolment that is declared but
never observed to fire proves nothing — that is the lesson the first cycle taught
three times over (codexFactory #252, #260, openxFactory #726 were all found by
running, not by reading).

## 4. Open questions for the owner

- **OQ-1.** Is the ruleset-bypass shape of § 2.2(a) acceptable at all? If the
  answer is no, every option except N-1 (d) is unreachable and this packet should
  be refused rather than narrowed — an envelope approval that cannot clear
  code-owner review changes nothing, and declaring it would be worse than
  declaring nothing.
- **OQ-2.** Should the second codexFactory candidate be enrolled on Brett's word
  alone, mirroring the `intent-rolling-custody` grant, or does it need a
  Gate-Rules Council record? **§ 2.2a effectively answers this and the answer is
  the council**, and the packet says so rather than leaving the owner to infer
  it. The `intent-rolling-custody` precedent is a word over a record tree that no
  CODEOWNERS entry gates and no promoted requirement forbids; this class needs a
  `## MODIFIED` to a requirement codexFactory canon calls absolutely forbidden and
  reaffirmed eleven days ago. A word can grant a candidate class inside the rules;
  it should not be the instrument that changes the rule, and
  `add-substantive-review-lane` task 3.2 — the council's general grant of an
  operable candidate class — is still open. The recommendation is therefore a
  council record; the owner may of course rule otherwise, and that ruling belongs
  on the record precisely because the alternative was named.
  (The 2026-08-28 unanimous refusal is undisturbed either way: it refused a class
  over `openspec/changes/**`, and this class admits no `openspec/` path —
  `.github/merge-approval-envelope.yml:15-22`.)
- **OQ-3.** The `intent-rolling-custody` precedent pairs a bot approval with a
  lane that arms auto-merge on its own side (ruling D-3 on #656). Should the floor
  lanes do the same, or should the merge-master lane learn to merge? This packet
  recommends the former and changes nothing about the latter, because
  "NO MERGE, EVER" is asserted by a test over the workflow's text
  (`merge-master-approval.yml:74-76`) and unpicking it is a much larger act.
