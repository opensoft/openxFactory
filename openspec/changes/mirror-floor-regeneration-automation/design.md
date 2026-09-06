# Design: mirror-floor-regeneration-automation

Status: draft (nothing here is ratified by being authored)

Every claim below about running code was read in a clone of this repository at
`0e47acc2` (openxFactory `main`) and of codexFactory at `8a406b10` (codexFactory
`main`), and is cited `file:line`.

## 1. What is being automated, exactly

The re-pin is five writes and one copy, and every one of them is mechanical.

| # | site | today | what an advance does |
|---|---|---|---|
| 1 | `contracts/review-lane-pin.yaml:60` | `core_commit: "ad15a8988490bf19c659254a92354987ec3a4028"` | replace with the new core commit |
| 2 | `.github/workflows/merge-master-approval.yml:410` | `PINNED_CORE_COMMIT: "ad15a898…"` | same |
| 3 | `.github/workflows/merge-master-approval.yml:525` | core checkout `ref: "ad15a898…"` | same |
| 4 | `.github/workflows/pytest-suite.yml:397` | core checkout `ref: "ad15a898…"` | same |
| 5 | `contracts/review-lane-floor-snapshot.yaml` + `contracts/review-lane-pin.yaml:627-632` | the byte copy, plus `sha256` and `entry_count: 68` | re-copy at the new core commit, recompute both |

The pin file states the procedure for site 5 in its own `refresh:` field
(`contracts/review-lane-pin.yaml:675-678`): *"Re-copy the file from
`scripts/merge_master/openxfactory-review-authority-floor.yaml` at the new
`core_commit`, recompute `sha256`, and update `entry_count`. Never hand-edit the
copy: it is a witness, and an edited witness proves nothing."* **The lane is
that sentence, executed.**

The ratified requirement *"The mirror is inert until the pin carries the rule,
and the pin moves as one act"* already enumerates the same five and already
refuses a partial advance
(`openspec/specs/review-lane-floor-mirror/spec.md:148-172`). So the sites and the
lockstep are settled canon; what this packet adds is an unattended AUTHOR for
them, and the confinements such an author needs.

## 2. The asymmetry with the codexFactory half, and why it matters here

codexFactory's lane needs two refusals a human supplies by reading a diff —
additions-only and block confinement — because it WRITES a governance document
whose contents are a judgment. **This repository's lane writes no judgment at
all.** Every one of the five sites is a transcription of one value: the commit
id, or a digest derived from bytes at that commit. There is no editorial content
to protect.

What this side needs instead is a proof that the transcription HAPPENED — all
five, not four — and a proof that the fifth was derived rather than copied from a
claim. That is why requirements 3 and 4 are written as MEASUREMENTS (re-read
each site; recompute from the bytes written) rather than as prohibitions.

**This is not a hypothetical failure mode.** The archived companion's own task
1.2 recorded the discipline as an operator practice: *"Advance all FIVE sites in
ONE commit, and verify each by reading it back rather than by trusting the
edit"*, with evidence *"all five sites re-read post-commit and equal
`e57643a7`"*
(`openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/tasks.md:20-31`).
Requirement 3 makes that the LANE's obligation instead of the operator's, which
is the only way it survives the operator being a machine.

## 3. The judge is not touched (M-4)

The freshness checks that will judge the bot's pull request are already in place
and are already hardened against silent degradation:

* the byte-for-byte comparison of the vendored snapshot against the pinned core
  runs only when the core checkout succeeded, and its checkout is
  `continue-on-error: true` — for the reason `pytest-suite.yml` gives itself at
  `:354-356`, quoting its own `:67-69`: *"a required check that fails for reasons
  the candidate cannot fix blocks everything"*;
* **and it cannot degrade silently**, because the verifier's `<testcase>` is
  looked up BY NAME in the JUnit report and required to have run and passed
  (`.github/workflows/pytest-suite.yml:359-380`). That named watch was a Codex P2
  finding on PR #569 against a first cut that leaned on an aggregate
  `EXPECT_SKIPPED` count, and the file records why the aggregate was not enough:
  two cancelling movements make the count right and the comparison silently gone.

**Automating the AUTHOR while adjusting the JUDGE in the same act would be
marking one's own homework**, so this packet does neither: LQ-A7, its two
negative controls, the byte-identity verifier, its named watch and
`EXPECT_SKIPPED` are all out of scope and stated as such in `code_surface:`.

The consequence is worth stating plainly rather than discovering later: **if the
bot's advance is wrong, the required suite goes red on the bot's pull request and
nothing lands.** That is the intended behaviour and it is why no exemption is
requested. An exemption keyed on the author would be the CSC-F16 silent-false-
green shape granted on purpose — inside the guard against CSC-F16.

## 4. The trigger (M-1), and why the sweep is the mechanism

The natural-looking design is: the codexFactory regeneration lane merges, and it
dispatches this repository to re-pin. **That is rejected as the MECHANISM and
kept only as an accelerator, for one reason: the re-pin is owed whenever the
floor document moves, not whenever codexFactory's automation moves it.**

* A hand-authored codexFactory regeneration — which the runbook keeps, and which
  is the only path for a REMOVAL — sends no dispatch. A dispatch-only design
  would silently not re-pin.
* Coupling the two automations makes a failure in one a silent failure in both,
  and a silent failure is the thing this whole family is built to refuse.
* A sweep that reads codexFactory `main` is true regardless of how the document
  got there, which is the property the requirement asks for.

The cadence must be declared against the same bound the codexFactory side is
declared against: the ruled tolerance of `3`
(codexFactory `scripts/merge_master/openxfactory-review-authority-floor.yaml:45`)
and the measured rate of addition. But note the ASYMMETRY: this side's sweep
does not gate the tolerance directly — the pending set is cleared by the
regeneration, and this side's advance is what makes the regeneration take effect
in the required lane. A slower cadence here delays the CLEARING rather than
permitting an escalation, so the tolerance argument binds the codexFactory sweep
tightly and this one loosely. Stated so a reviewer does not assume the two
cadences must be equal.

Trigger shape, concretely: watch codexFactory `main` for a change to
`scripts/merge_master/openxfactory-review-authority-floor.yaml`, plus a
`schedule:`. **Note that this repository has no `schedule:` in any workflow
today** — the nightly doc-health run is scheduled by a thin caller in the
xFactory aggregation repository and invoked here through `workflow_call`
(`.github/workflows/doc-health-reusable.yml:1-12`). Whether this lane's schedule
lives here or in that caller is a realization choice with a real consequence for
where the credential lives, and it is named in `tasks.md` rather than assumed.

## 5. Identity (M-6)

The App is already installed in both repositories and is already minted here to
read codexFactory: `.github/workflows/pytest-suite.yml:318-324` mints
`secrets.OPENXFACTORY_APP_ID` / `secrets.OPENXFACTORY_APP_PRIVATE_KEY` and
`:392-400` uses the token to check codexFactory out at the pinned core commit.
codexFactory mints the same App from its side
(`.github/workflows/activation-open-pr.yml:34-41`).

What the lane needs beyond that: `contents: write` and `pull_requests: write` in
THIS repository, to push a branch and open a pull request. The doc-health
delivery job is the shape and the precedent for those two permissions
(`.github/workflows/doc-health-reusable.yml:1057-1066`, whose comment records
exactly why `pull-requests: write` became necessary: org ruleset `18962101`
protects the default branch, so *"the nightly can no longer push reports
directly — it delivers them through a rolling PR instead"*).

**Why refusal rather than fallback.** `pytest-suite.yml:400` writes
`${{ steps.app-token.outputs.token || github.token }}`, and that is right THERE:
the step is `continue-on-error`, the fallback degrades to a narrower identity,
and the degradation is caught by the named-testcase watch. Here the same pattern
would degrade to an identity that cannot read codexFactory, so the lane would
compare the pin against nothing, find no disagreement, and exit green. **A
missing credential must not be able to look like a clean run.**

The binding is declared as a TEMPLATE. This repository's neutral
`credential-contracts` requires it from the consuming side —
*"A credential binding declares the consuming system that holds it and the
identity it fetches with"*
(`openspec/specs/credential-contracts/spec.md:300`) — and the
`kind: xfactory_credential_binding_template` shape with `vault://EXAMPLE-VAULT/…`
placeholders is the one codexFactory already ships
(`credentials/bindings.template.yaml`). No live value goes into either
repository.

## 6. Merge authority (M-5), and the one precedent that exists

openxFactory has exactly one bot-authored pull request that an App may approve:
the doc-health nightly. Its delivery step opens the pull request
(`.github/workflows/doc-health-reusable.yml:2898-2901`), comments the envelope on
it (`:2902-2903`), enables auto-merge (`:2907-2908`) and dispatches the approval
workflow (`:2920-2922`). The comment it posts states the terms: Merge Master
*"approves it autonomously only when every condition holds. Any failed or
unevaluable condition leaves the PR parked for the human gate."*

That envelope is a reviewed LOW-RISK class. **A pin advance is not obviously in
it, and this packet does not argue that it is.** `contracts/review-lane-pin.yaml`
is itself a never-clearable floor entry in codexFactory's floor
(`codexFactory scripts/merge_master/openxfactory-review-authority-floor.yaml`,
the fourth hand-reasoned entry, whose ground is written there in one sentence:
*"the review-lane pin selects which codexFactory commit's decision core judges
this repository. Clearable, it would let a pull request choose its own judge."*).
**A lane that could both propose and land a change to that file would be a lane
that chooses its own judge**, which is the exact thing the floor entry exists to
prevent. So the default is a human merge word, and the question of ever
extending the envelope is put in `tasks.md` § 6 as a separate ruling — named so
it is not silently assumed either way.

## 7. What this design deliberately leaves alone

- **The rule.** `evaluate_floor_completeness`, the two graces, the fail-safes and
  the report shape are codexFactory's and are read here, never redefined.
- **The judge.** LQ-A7, its two negative controls, the byte-identity verifier,
  its named watch and `EXPECT_SKIPPED`.
- **The floor and its tolerance.** Neither moves here; both are codexFactory's
  CODEOWNERS-routed document.
- **The pin's grammar.** `kind: pinned_workflow` and its stated reason for not
  being `pinned_contract_manifest` (`contracts/review-lane-pin.yaml:24-56`) are
  untouched; this packet adds no pinned member and no digest set.
- **The hand path.** An operator can still advance the pin by hand, and must,
  whenever the lane refuses.

## 8. The corpus's second cross-repository `sequenced_after:` entry

`sequenced_after: [codexFactory:add-floor-regeneration-automation,
mirror-floor-addition-grace]` mixes a QUALIFIED FOREIGN entry with a BARE local
one. Both forms are in the grammar: `scripts/sequenced_after.py`'s own docstring
names *"bare `<change-id>` or `<repository>:<change-id>`, with a self-qualified
entry normalized to bare"*, and the module declares *"NO depth limit and NO
fan-out limit"*, so two parents are well-formed.

The foreign entry is checked for well-formedness only — the neutral validator
*"cannot read another repository's corpus and MUST NOT pretend to"* — which is
the same disposition the archived `mirror-floor-addition-grace` recorded when it
became the corpus's FIRST foreign entry. **"Second" is measured, not
remembered**: at this head `corpus_sweep('.')` reports `declaring=5` over
`change_ids=176`, and of those five declaring changes exactly TWO carry a
qualified foreign entry — `mirror-floor-addition-grace`
(`codexFactory:add-floor-addition-grace`) and this one. This is the second, and the prose
statement of the dependency is kept in `proposal.md` and in requirement 2's body
for the same reason that packet kept its own: a foreign entry resolves for no
validator, so a reader must be able to see what it means.

The bare entry `mirror-floor-addition-grace` resolves locally at
`openspec/changes/archive/2026-09-05-mirror-floor-addition-grace/` — the archived
anchor, one of the exactly two locations the grammar accepts.
