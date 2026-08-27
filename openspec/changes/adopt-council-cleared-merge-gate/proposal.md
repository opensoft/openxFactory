---
code_surface: none — this change's own diff is spec text and packet records in openxFactory only: one ADDED capability (`council-cleared-merge-gate`) plus a `roles-authority-model` delta declared relative to the active ratified `add-substantive-review-lane`, and a `review-authority-intake` delta declared relative to the active ratified `add-wallet-carried-review-authority`. NO workflow, no ruleset, no `contracts/` artifact and no script is added or changed BY THIS CHANGE. That is deliberate and it is the whole point: this is the POLICY HALF, and every physical act it authorizes is named in `tasks.md` behind a realization gate that must report green first — `[OPERATOR]` for the App installation and credential acts, `[hermes-install]` for S3 and S5, `[codexFactory]` for the candidate-class enrollment and the floor widening, `[openxFactory]` for R1's caller and the canary records. Per `release-realization` a `code_surface: none` change archives when its artifacts land; this change nevertheless DECLARES that it must not archive while its own adoption gate stands unopened, because archiving it would file a policy as realized whose enabling acts are all still ahead of it.
target_release: none — no contract bundle is cut and no `contracts/` artifact moves. The realization this change gates lands as an App installation, repository secrets, a codexFactory gate-rules record, a widened floor file, and hermes-install runtime code, each in its own repository's main line under its own change.
---

# Proposal: adopt-council-cleared-merge-gate

Status: draft
Proposed: 2026-08-27 on the convener's direction "do all of these", given in
session in answer to a proposed plan to author this packet with a full
alignment review and council. The direction authorizes AUTHORING, explicitly
not ratification: "a gate-policy change is the convener's ruling; do not write
`Status: ratified`". The class boundary, the realization gates, the kill switch
and the canary below are therefore DECLARED, not decided.

## The question this answers, and the honest answer

Brett asked, in session: **"do we have ability for review and merge from codex
hermes now?"**

**No.** Two halves are missing and they are missing very differently.

The **mechanism half** is mostly built and is being built further as this is
written. codexFactory's `merge_readiness_council` and its mechanical Merge
Master operator are proven live — autonomous deliberation on 2026-08-14, three
seats, written rationales, unanimous READY, a signed council-verdict check-run,
and a real GitHub `APPROVE` review cast by a dedicated App identity, on
xFactory PRs #85 and #100. codexFactory has shipped openxFactory's own
repository gate floor
(`scripts/merge_master/openxfactory-review-authority-floor.yaml`) since the
`015-widen-review-authority-floor` work. openxFactory's own advisory reader of
that floor is **open right now as PR #439** (R1, branch
`025-openxfactory-review-lane-caller`, head `f012eb10`, opened 2026-08-27T22:42Z,
unmerged).

The **policy half does not exist at all**, and R1's own workflow header says so
in words that name this change's job. It lists, among the things it deliberately
does not do:

> NO RULESET CHANGE. This check is required by nothing, satisfies nothing, and
> blocks nobody. The human review gate on this repository is untouched. **It
> stays that way until S3 and S5 of `add-wallet-carried-review-authority` land
> AND a ratified ruleset change says otherwise.**

**This change is that ratified statement** — or rather, the proposal for it. It
proposes no mechanism and builds nothing. It writes down the boundary that the
in-flight mechanism work is aiming at, before anyone claims the aim has been
reached.

## Why now, and what it actually ends

`opensoft/openxFactory` is a contracts-and-documentation repository. Alongside
its governed proposal traffic it carries occasional pure prose: `docs/**`
governance writing, `ideation/**` brainstorm and staging fragments, and README
index lines. **"Occasional" is measured, not hedged — see "The value this
delivers, MEASURED", which puts it near zero per week today.** It sits under an
**organization-level** ruleset
requiring one approving review (see "The gate as it actually is" below). So a
documentation-only pull request in this repository has exactly two ways to land
today: a human review that the repository's own ratified doctrine says a diff of
that shape does not need, or an `--admin` bypass.

**That prose-and-derived slice is the whole of what this change reaches** — the
class boundary below shows why, and why openxFactory's proposal traffic is not
in it.

The bypass is the thing to end. It is not merely inelegant — it is
**strictly worse than either alternative**, because it leaves **no accountable
reviewer of record at all**. A human review records a human. A council-cleared
approval records a council, its seats, its rationales, and — once S3 lands — a
wallet-bound exercise of a registered authority. The bypass records an
administrator who declined to be reviewed. Replacing it with an accountable
reviewer is an increase in governance, not a relaxation of it.

## The gate as it actually is (verified 2026-08-27, not assumed)

Read from `gh api repos/opensoft/openxFactory/rules/branches/main`. **Every rule
on this branch is inherited from an ORGANIZATION ruleset. openxFactory has no
repository-level ruleset of its own.** Four org rulesets compose:

| Ruleset | Name | Targets | The rules that matter here |
| --- | --- | --- | --- |
| `18962101` | xFactory Tier-1 main protection (require PR + 1 approval) | default branch of **seven** repos: AdxFactory, LedgerxFactory, MedxFactory, OpsxFactory, codexFactory, openxFactory, xFactory | `pull_request`: `required_approving_review_count: 1`, `dismiss_stale_reviews_on_push: false`, `require_extra_approval_for_unattributed_changes: true` |
| `18834180` | Require Code Owner Review | default branch of **~ALL** org repos | `pull_request`: `required_approving_review_count: 0`, **`require_code_owner_review: true`**, **`dismiss_stale_reviews_on_push: true`** |
| `21538893` | openxFactory wallet-gate | default branch, **`openxFactory` only** | `required_status_checks`: `wallet-validation`, `pytest-suite`. **Created 2026-08-26, edited the same day** — the newest and least settled row. `wallet-validation` is the job id in `.github/workflows/openxwallet-consumer-gate.yml`; `pytest-suite` in `.github/workflows/pytest-suite.yml`. Both producing workflows recorded here so a rename is detectable. |
| `8981805` | Copilot Auto-Review All PRs | ~ALL repos | advisory review only, non-blocking for merge (it also carries an unbypassable `non_fast_forward` rule, as does `18834180` with `deletion` — irrelevant to review gating) |

All three of the gating rulesets carry exactly one bypass actor:
`OrganizationAdmin`, `bypass_mode: always`. **That is the admin-bypass ritual,
located.**

Four consequences follow, and each one changes the design:

1. **The 1-approval rule cannot be edited for openxFactory alone.** It lives in
   an org ruleset spanning seven repositories. "Turn off the approval
   requirement" is a **seven-repository blast radius**, six of them repositories
   this change has no authority over and no evidence about.
2. **A GitHub ruleset cannot branch on pull-request class.** Required checks and
   approval counts apply to every pull request on the branch. There is no
   ruleset expression of "one approving review, unless the class is docs". Any
   design that claims per-class gating **at the ruleset layer** is not
   implementable as described.
3. **Stale-approval dismissal is already on, but it is INHERITED and this
   change should stop inheriting it.** `18834180` sets
   `dismiss_stale_reviews_on_push: true` while `18962101` sets it false, and
   GitHub aggregates composing rulesets so that the most restrictive value
   applies — so the obvious attack on an autonomous approval (get a docs diff
   cleared, then push code onto the approved head) is closed today. **But it is
   closed by the one ruleset this change has least standing to defend** — the
   `~ALL`-repos code-owner ruleset — and both `pull_request` rules carry
   `require_last_push_approval: false`, so dismissal is diff-state-based only.
   Anchoring it is cheap and blast-radius-free: `21538893` is openxFactory-only,
   so adding `dismiss_stale_reviews_on_push: true` **and**
   `require_last_push_approval: true` there makes the property locally owned
   instead of borrowed. That is an `[OPERATOR]` task, and it is the **only**
   ruleset edit this change proposes — a hardening, not a relaxation.
4. **The code-owner requirement is a native, un-spoofable human floor.**
   `18834180` requires code-owner review on any pull request touching an owned
   path, and openxFactory's `.github/CODEOWNERS` names `@brettheap` — a human
   user — for `.github/workflows/`, `/contracts/openxwallet-pin.yaml`,
   `/scripts/verify-openxwallet-pin.py`, `/openXwallet` and `/.gitmodules`. **No
   App can satisfy a code-owner rule whose owner is a human user.** The
   assembly-class floor is therefore enforced by GitHub itself, below and
   independent of anything codexFactory decides.

## What this change proposes

**The 1-approving-review rule STAYS. No org-wide ruleset is relaxed. No new
required check is added.** What changes is exactly one thing: **who is permitted
to cast the approving review**, and for which classes of diff. The single
ruleset edit proposed is a *hardening* of openxFactory's own repo-scoped
ruleset `21538893` (consequence 3 above), which affects no other repository.

For an openxFactory pull request whose classification is an autonomously
clearable docs/derived-artifact class, the approving review MAY be cast by the
merge-master App on a unanimous `merge_readiness_council` verdict backed by a
wallet-bound exercise record. The required checks `wallet-validation` and
`pytest-suite` are unchanged and still gate. For every other class, and for
every pull request touching a CODEOWNERS path or a floored path, the human
review stays exactly as it is today.

This is not the shape the direction sketched, and the difference is deliberate.
The sketch was "required checks `wallet-validation` + `pytest-suite` +
`merge-master-approval` **in place of** the 1-approving-review rule". **Ratified
doctrine forbids that shape**, in the `add-substantive-review-lane` requirement
*Ruleset interaction shape for the substantive review lane*, on three counts.
Note the citation form used throughout this proposal: that requirement is
**ratified but not yet promoted**, so it lives in the change delta, not in
`openspec/specs/` —
`openspec/changes/add-substantive-review-lane/specs/roles-authority-model/spec.md:284-296`.
The promoted `openspec/specs/roles-authority-model/spec.md` is 181 lines and
contains none of it.

> Where a candidate IS cleared under this lane, the approval SHALL satisfy the
> governed repository's required-review rule **by the merge-master App casting a
> real `APPROVE` review** […] the council-verdict check-run SHALL remain verdict
> transport only and **MUST NEVER be configured as a ruleset-accepted
> satisfier**; and **human review SHALL remain an always-available alternate
> satisfying path** on every governed repository, so no repository's ruleset may
> be configured such that only the council-cleared App path satisfies it […]

So the prescribed mechanism *is* an approving review; a check-run as satisfier is
prohibited outright with a stated anti-spoofing reason; and removing the human
path is prohibited by default. The mechanical analysis in "The gate as it
actually is" reaches the same place independently, from a different direction —
a ruleset cannot branch on class, so a check-satisfier design would have had to
move the enforcement of human review out of GitHub and into codexFactory's
Python. **Doctrine and mechanics agree, and the sketch is the thing that yields.**

### The alternative this change considered and rejected

Adding `merge-master-approval` to openxFactory's own repo-scoped ruleset
(`21538893`) as a required check was considered as additive hardening — making
the floor reader's verdict mandatory rather than advisory. **It is rejected**, on
four grounds, and the rejection is recorded rather than silent:

1. **Self-reference — real, but already solved, and therefore a burden rather
   than a bar.** `add-substantive-review-lane`'s *Fail-closed substantive review
   envelope*
   (`openspec/changes/add-substantive-review-lane/specs/roles-authority-model/spec.md:96`)
   is conjunctive and its third conjunct is that "the low-risk enforcement
   envelope otherwise holds"; that **promoted** envelope
   (`openspec/specs/roles-authority-model/spec.md:80-84`) opens with *every
   required deterministic check passes*. So the enforcer's own required check
   would sit inside the envelope it gates. **The house already fixed this** —
   xFactory's `.github/merge-approval-envelope.yml:85-87` carries
   `check_exclusions: [merge-master-approval]`, commented "Exclude this
   workflow's own check-run to avoid a self-reference deadlock", and it is why
   R1's job id must be that literal string. The correction to this proposal's
   earlier draft: the exclusion **exists**, so the hazard is not a deadlock we
   cannot escape but an invariant openxFactory's own envelope would have to
   carry — and an envelope that omitted it would deadlock silently. Grounds 2-4
   carry the rejection on their own.
2. **It buys no safety.** The floor is evaluated **inside** the approver. A
   broken, absent or credential-starved lane produces no verdict, so it produces
   no approval, so the human path is the only path. The design is already
   fail-closed without the check being required.
3. **It is a repo-wide wedge.** R1 deliberately **fails red** when App
   identifiers are missing, and R1's header says why that is safe: "Because no
   ruleset requires the check, the red blocks nobody." Making it required
   converts that considered choice into an outage on every open pull request the
   moment a credential rotates.
4. **A required context named `merge-master-approval` is weakly bound to the
   workflow that should own it.** Any job of that id reporting success satisfies
   the context. `.github/workflows/` is CODEOWNERS-routed to a human, which
   closes the vector — but the vector should not need closing.

If the convener wants the hardening anyway, the coherent form is a **separately
named** required check (say `review-lane-floor`) that is not the approver, so
nothing sits inside its own envelope. That is recorded as **Q3**, not decided.

## The class boundary

### First: the floor is not exhausted by paths

Before any path is named, one correction to a natural misreading. The
*Constitutional floor for autonomous clearance*
(`openspec/changes/add-substantive-review-lane/specs/roles-authority-model/spec.md:323-344`)
declares its own **SOURCE OF TRUTH** to be codexFactory's `gate_rules_council`
record of 2026-07-23, "and where it and that record ever diverge the record
governs". That record's floor has **six members**:

1. identity mismatch
2. HEAD-REF mismatch
3. failed or pending required checks
4. secret findings
5. security-touching paths
6. gate-weakening changes

**Only members 5 and 6 are path-shaped.** Everything this section draws is the
**path-shaped subset of a six-condition floor**, and a boundary stated in paths
alone would read as if the floor were exhausted by them. The other four are
enforced in the envelope, not in a path list — who restates them for
openxFactory is **Q5**.

### The doctrine draws the boundary in classes, not paths

**And neither may this change.** It draws it in **named candidate classes**, and getting that
vocabulary right is the difference between a policy that can be enforced and a
policy that reads well. A class is two base-branch-committed objects, verified
in `scripts/merge_master/council_clearance.py` on codexFactory `origin/main`:

1. An **envelope candidate** in the target repository's own
   `.github/merge-approval-envelope.yml`, matched on author, head ref, head
   repo and changed paths, and read "as committed on the base (default) branch,
   never from the pull-request head".
2. A **per-repo gate rule** bound to it by an explicit
   `applies_to.candidate_id`, which "SHALL NOT infer the binding from the rule
   identifier, the repository field, or the candidate class".

Clearability is one declared field on the rule —
`classification_intent: advisory | clearable` (`council_clearance.py:186`) — and
it is "the SOLE authority for advisory-versus-clearable intent". **Nothing is
classified by label, by pull-request body, or by author self-declaration.**

So this change's job is not to name clearable paths. It is to state **which
openxFactory candidate class may ever carry `classification_intent: clearable`**,
and to let the two implemented floors decide the paths.

### The two floors, verified verbatim

They are complementary, both enforced, and neither is a restatement of the other.

**PR-time — `GATE_INTEGRITY_FLOOR` (`council_clearance.py:136`)**, evaluated
against the files a pull request actually changed:
`scripts/**`, `tests/**`, `pytest.ini`, `sonar-project.properties`,
**`openspec/changes/**`**, `instantiation-answers.yaml`, `.gitignore`.

**Definition-time — `PROTECTED_CLASS_SURFACES` (`:852`)**, evaluated against
everything a class's allowlist *could* ever reach; a class that can reach any of
these is human-only regardless of unanimity:
`scripts/`, `tests/`, `.github/`, `schemas/`, `contracts/`, **`openspec/`**,
`specs/`, `hermes/`, **`governance/`**, `credentials/`, `workflows/`,
`omnigent/`, thirteen agent-instruction dot-directories, `pytest.ini`,
`sonar-project.properties`, `instantiation-answers.yaml`. Plus
`PROTECTED_ROOT_FILES` (`:900`) for the paths a prefix cannot reach at the root:
`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md` and seven further
agent-instruction files.

The positive term is narrow and conservative. `pattern_is_docs_or_derived`
(`:960`) admits only `DOCS_FILE_SUFFIXES = (".md",)` — **prose means `.md`, and
nothing else** — under a real literal prefix, because "LOCATION MUST WIN OVER
EXTENSION" and a bare `**/*.md` is refused outright; or a path under
`DERIVED_ARTIFACT_ROOTS` (`:765`), narrowed by R5 on the convener's 2026-08-26
disposition to eight exact subtrees, of which exactly **two are openxFactory's**:

```
health/derive-possibles/     # openxFactory: generated registers
health/neutrality-drift/     # openxFactory: generated drift output
```

and whose own comment records their standing: "no class uses them today
(Phase 2 is held), and the floor describes what IS derived rather than what is
currently claimed."

### The boundary this change draws: ONE class

**ONE candidate class, `openxfactory-governance-prose`.** An earlier draft drew
two. The council removed the second, and the removal is the single largest change
the council made.

| Field | Value |
| --- | --- |
| `candidate_id` | `openxfactory-governance-prose` |
| `target_repos` | `[opensoft/openxFactory]` |
| `path_allowlist` | `docs/**/*.md`, `ideation/**/*.md`, `README.md` |
| author matcher | `author_class.council_cleared_logins: [brettheap]` |
| `require_same_repository` | `true` — **schema-forced** by the `if/then` whenever `author_class.council_cleared_logins` is present |
| head-ref matcher | `head_ref_pattern` — **required, and it is the only selector that runs** |
| `check_exclusions` | both openxFactory job ids that produce a `merge-master-approval`-substring check (see G4b) |
| `requires_intent_reference` | `true` — **opt-in, not automatic** |
| gate rule | ONE document; `applies_to.candidate_id` is a single string |
| `human.accountable` | `brettheap` — a **bare login**; `council_clearance.py:1477` refuses a leading `@` |

### Why the derived-artifact class was removed, not narrowed

Three seats reached this independently, from three directions, and it is worth
recording all three because each alone would have been arguable.

- **It has no traffic.** `health/neutrality-drift/` has produced **zero pull
  requests ever**. `health/derive-possibles/` produced two (#38 merged
  2026-07-23, #39 closed) and nothing in five weeks. The whole `health/` tree is
  five files; the two named roots hold three, last written 2026-07-26. Both lanes
  are documented dormant in their own comments ("no worker host advertises the …
  profile"), and the genuinely nightly doc-health pull request lands in
  `opensoft/xFactory`, not here.
- **Its only historical PR shape was structurally unclearable anyway.** Both
  derive-possibles pull requests also carried `ideation/cross-reference.yaml` — a
  `.yaml` outside `DERIVED_ARTIFACT_ROOTS`, which `pattern_is_docs_or_derived`
  refuses. Widening to admit it would fail the class floor.
- **Its allowlist re-admitted a protected comparator, which is a floor narrowing
  wearing a boundary's clothes.** `health/neutrality-drift/**` admits
  `health/neutrality-drift/baseline/codexFactory.yaml` — **the only tracked file
  in that tree** — which `scripts/doc_health/neutrality.py:89-92,599-620`
  documents as the recorded, **immutable** baseline that `load_baseline` reads
  back to decide "the docs the scout has already judged."
  `PROTECTED_PATH_SEGMENTS = ("baseline",)` cannot stop it:
  `_has_refused_segment` walks the **pattern**, not the changed paths, so
  `health/neutrality-drift/**/baseline/**` is refused while the broader glob
  validates. R5's own comment claims "the roots above are enumerated so a
  `baseline/` under them is already refused today" — **true of the xFactory
  roots, false for the two openxFactory roots R5 added** on the note that "no
  class uses them today". The enforcer's docstring at `:929-950` names the cost
  verbatim: "a derived root re-admitting its own PREV comparator … Exactly what
  R5 protected, **reachable by moving one glob**." An earlier draft of this
  proposal wrote that glob. `regular-pr-council-clearance/spec.md:55` forbids
  narrowing a floor outright.

Consequences carried honestly: the canary is now **prose-only** (a canary
requiring ≥3 observations in a class with no producer could never complete, so
the earlier N=6 split made the flip structurally unreachable), and the derived
class is **deferred to its own change**, to be enrolled when a wired producer
exists and Phase 2 is unheld — carrying its own canary at its own enrollment,
which preserves class-boundary-error detection without conditioning this class's
adoption on traffic that does not exist.

### A succession claim this proposal withdraws

An earlier draft said codexFactory's `openxfactory-derived-health-artifact-advisory-v1`
was "PREPARED AND PARKED 2026-08-25" with `state: defined_not_wired`, and that
this change's derived class succeeded it.

**That artifact does not exist in rules-as-code.** It appears only in prose, in
the **active, unarchived** change
`add-classification-intent-and-substantive-classes`, at tasks **7.2 and 7.3,
both unchecked**, where it is merely *"propose[d] … for the Council to accept or
amend"*. Task 7.1 additionally **holds Phase 2**: "If Phase 1 is refused or
amended beyond the packet's proofs, Phase 2 is void."

So the draft attributed a shipped rules-as-code state to an unchecked task, and
claimed succession from an artifact never authored — **the exact LS-A3 error this
packet exists to prevent, committed by this packet.** It is recorded here rather
than quietly deleted, because a withdrawn claim that leaves no trace teaches
nobody.

### The mixed-diff rule this proposal previously asserted is NOT implemented

An earlier draft said "a mixed diff takes the most restrictive class of any path
it touches", presenting it as the existing `docs_only_path_overflow` discipline.

**There is no cross-candidate arbitration.** `_find_surface`
(`envelope.py:510`) selects on `target_repos` **and head ref only** — paths are
never consulted — and it is **first-match-wins**. The real semantics: a mixed
diff parks on the selected candidate's `path_allowlist` overflow. That is
fail-closed, so the safety conclusion survives; the stated mechanism was wrong,
and with one class the question of overlapping candidates does not arise at all.
Any future second class must therefore prove its head-ref matcher is **disjoint**
from this one's and declare candidate order, or it is dead code.

### The fields the enforcer requires and this proposal must define

Recorded because "declares a `risk_tier`" is unreviewable until the vocabulary
exists, and because several of these are hard validation failures if omitted:

- **`risk_tier: {id, rationale}`** — `council_clearance.py:1263` accepts **any
  non-empty string**, so the code closes no vocabulary. This change must define
  one rather than gesture at the field.
- **`anti_normalization` with EXPLICIT semantics** — either
  `consecutive_candidates` + `same_condition_cleared_consecutively`, or
  `rolling_window` + `{same_condition_cleared_within, window_hours,
  history_entry_requires}`. Never inferred from the surface's shape (`:1338`).
  Omission is a validation failure.
- **`activation_dependency`** — required by the same `_validate_defined_not_wired`
  this change leans on for advisory-forcing.
- **`gate_integrity.never_clearable_paths`** — mandatory, because
  `_requires_enrolled_controls` trips on any rule declaring
  `classification_intent`.
- **`council_clearable[]`** entries each with `id`, `owning_seat`,
  `tier1_condition` ∈ {`path_allowlist`, `author_requires_clearance`} and an
  allowlist; plus `docs_class_allowlist` where the entry id is
  `docs_only_path_overflow`, which this proposal invokes by name. Exactly one
  such entry must resolve as the `clearance_rule`.

**One contradiction in the enforcer blocks this today and needs a codexFactory
change this proposal names rather than works around.** Widen-only forces a
declared floor to cover every `GATE_INTEGRITY_PROBES` path, including
`instantiation-answers.yaml` and `sonar-project.properties` — **both absent from
openxFactory**. If `tree_paths` is supplied, reachability then refuses them ("a
floor that matches nothing is indistinguishable from no floor"), and R1's own
`test_the_caller_opts_into_the_floor_reachability_check` establishes that
openxFactory **must** opt in. The two controls contradict each other for any
foreign repository. The fix is repo-relative probes in codexFactory, named as
task 3.10 — **not** silently declining to pass `tree_paths`.

### Answering the direction's three flagged questions, and correcting its premise

- **`scripts/**`?** **Human-only, and already floored twice** — PR-time as "the
  decision core's whole import root (D2)" and at class level as "the decision
  core and every validator". Not a judgement this change had to make; the
  implemented floor made it.
- **`.github/workflows/**`?** **Human-only**, floored at class level via
  `.github/`, and independently CODEOWNERS-routed to `@brettheap`. But the
  routing is **narrower than `.github/**`**: openxFactory's CODEOWNERS names
  `.github/workflows/` only, so `.github/CODEOWNERS` **itself** and a new
  `.github/merge-approval-envelope.yml` are **not** owner-routed today. The
  class floor still refuses them, and codexFactory floors `.github/**` for
  exactly this reason — CODEOWNERS "can be wrong". This proposal therefore owes
  a CODEOWNERS realization task widening the route to `.github/`, and must not
  claim the envelope's authoring is an owner-routed act until it is.
- **`contracts/*.schema.yaml`?** **Human-only.** `contracts/` and `schemas/` are
  both class-floored as "contract bytes", and the positive term admits only
  `.md` and the derived roots, so a `.yaml` under `contracts/` fails twice over.

**And the premise that "openxFactory is a contracts/docs repo so most PRs
qualify" is FALSE. It is the most important correction in this proposal.**
`openspec/changes/**` is in the PR-time gate-integrity floor and `openspec/` is
in the class floor. openxFactory's dominant traffic *is* `openspec/changes/**`
and `openspec/specs/**` — proposals, spec deltas, packet records. **None of it is
autonomously clearable, and none of it becomes clearable under this change.**

The honest scope of the relief is therefore narrow: documentation prose, ideation
`.md` and the README index — one class, after the council removed a second.
**This proposal's own diff would not qualify under it** — it is `openspec/changes/**`, floored at PR
time — and that is the correct outcome, not an irony to be engineered around.

What the change buys is real but bounded: the routine prose traffic stops needing
either a human review it does not merit or an `--admin` bypass that records no
reviewer. Everything substantive keeps its human. Anyone
reading this proposal hoping it ends the bypass ritual for openxFactory's
*proposal* traffic should stop here: it does not, and no ratified doctrine
currently permits a change that would.

### The value this delivers, MEASURED — and it is very small

The council required this proposal to state a falsifiable throughput claim rather
than assert relief. Every file of the last 140 merged pull requests on
`opensoft/openxFactory` was classified against the allowlist, counting a pull
request only if **all** its files fall inside:

| Window | Merged PRs | Entirely inside the allowlist |
| --- | --- | --- |
| Most recent 40 (2026-08-26 → 08-27) | 40 | **0** |
| Next 100 back (2026-08-24 → 08-26) | 100 | **13** |
| The removed derived class, all history | ~400 | **0** |

**And the 13 are not a rate — they are one finished campaign.** Nine are
single-file appends to *one* file, `docs/archive-record-discrepancies.md`; two
are `ideation/staging/` pairs; one is a runbook typo fix. Twelve of the thirteen
landed on 2026-08-24/25, and the trailing 40 pull requests contain **zero
successors**.

So the honest expected benefit is **approximately zero pull requests per week
today**, and about three per week at the peak of a campaign that has ended. The
phrase "a steady stream", used in an earlier draft, is withdrawn.

**This measurement is the strongest argument against ratifying the change on
throughput grounds, and it is published rather than buried.** The proposal's
defence is not throughput — it is option-closing (see "Why author the policy
first"), and the convener should weigh it on that basis or decline it.

### The high-value class this change cannot reach, named so it is not invisible

The measurement also found where openxFactory's bypass traffic actually lives.
**Four of the recent 40 merged pull requests are single-file diffs whose only
file is `openspec/changes/**/tasks.md`** — checkbox ticks. That is 10% of recent
traffic, higher than this proposal's clearable class at its historical peak, and
the pattern is unmistakable: **openxFactory's bypass ritual is bookkeeping under
`openspec/`, not prose.**

This change cannot touch it. `openspec/changes/**` sits in the PR-time
`GATE_INTEGRITY_FLOOR` and `openspec/` in the class floor, and
`regular-pr-council-clearance/spec.md:55` forbids narrowing a floor. Reaching it
would require a **doctrine amendment nobody has proposed** — plausibly a
`tasks.md`-checkbox-only class with a diff-shape predicate rather than a path
predicate, since the objection to `openspec/changes/**` is that it holds the
change records, and a checkbox tick alters no record's content.

**Recorded as Q7 rather than left unasked**, because a reader currently closes
this packet believing the narrow slice is all there could ever be, when the
high-value class exists and is merely locked. If the convener will not amend that
floor, the honest alternative is to say so and consider moving the pilot to
`opensoft/xFactory`, which already carries the org's only `clearable` class and a
recurring nightly derived-artifact producer — that is, actual traffic to canary
against.

### The enrollment surface openxFactory does not have

The architecture is **per-repo self-hosted**, not federated from codexFactory.
Each enrolled repository carries **its own** `.github/merge-approval-envelope.yml`
and its own approval-capable workflow, checking out codexFactory purely as a
pinned decision-core library. Verified on openxFactory `origin/main`:
`.github/merge-approval-envelope.yml` **absent**, any
`merge-master-approval.yml` **absent** (R1 adds an advisory workflow and
deliberately **no** envelope), `scripts/merge_master/` **absent**.

The only two `target_repos` allowlists in existence are
`[opensoft/codexFactory]` and `[opensoft/xFactory]`. **openxFactory is in
neither.** The one openxFactory-shaped object codexFactory ships is
`openxfactory-review-authority-floor.yaml`, which is **deny-side only** — it
subtracts authority and grants none.

Even codexFactory's own in-repo docs-adjacent class, `codexfactory-routine-code`,
runs **advisory** — "The blast radius is real product code, so this class is NOT
autonomously eligible". The only `clearable` class anywhere is the `health/`
nightly derived-artifact class in `opensoft/xFactory`.

So the enrollment path is: openxFactory authors its own envelope candidate,
codexFactory authors the bound gate rule at `classification_intent: advisory`,
the canary runs, and only then does a **separate** ratified act flip that one
field to `clearable`. **This change authorizes the boundary, not the flip.**

### The per-repo floor, and what it can and cannot hold

The floor file codexFactory ships for openxFactory (landed via codexFactory
PR #118; read at R1's pinned commit `58bd3cf7`, **byte-identical to codexFactory
`origin/main`** — the pin is behind main in general but **not stale for this
file**) contains exactly **three** never-clearable paths:
`governance/review-authority/register.yaml`, `contracts/openxwallet-pin.yaml`,
and `openXwallet`.

Most of the human-only surface is covered by the two **global** floors rather
than by this per-repo file, so the gap is narrower than it first looks. Two
things are nonetheless owed, and neither can live in that file:

- `openxfactory-review-authority-floor.yaml` is `kind: repository_gate_floor`,
  and `repository_floor.py` **refuses wildcards outright** ("must be exact;
  wildcards are not allowed") with `matching_paths` doing exact set membership.
  It can hold exact chokepoint FILES and nothing else. A glob floor belongs in a
  **clearance rule**'s `never_clearable_paths`, in the envelope glob dialect, as
  `codexfactory-routine-code-clearance.yaml` already does.
- The file's own header records an unclosed gap:

  > PRE-EXISTING and out of scope here (`split-openxwallet-repo` §8.3): this
  > floor omits `governance/review-authority/{grants,wallets,attestations}/`, and
  > lead-security's 2026-08-26 floor-reachability finding stands.

  Those three must be enumerated as exact files, or moved to the glob carrier.

Closing both is a realization gate (G4), not an assumption. Stating it here
rather than in a footnote is deliberate: a floor narrower than the policy it is
supposed to enforce is precisely how a described control comes to be treated as
an existing one.

## Realization gates

**None of the acts below may be performed until the gate above it reports
green.** Each gate names the evidence that opens it. `tasks.md` carries them as
ordered, tagged tasks.

- **G1 — S3 realized and deployed, with the refusal PROVEN.**
  `add-wallet-carried-review-authority` S3 (*the exercise, at verdict
  conformance*) requires the seat's signature to be verified when the runtime
  checks the verdict, and the exercise record written there.
  **Current state, verified 2026-08-27: NOT MET, and barely begun.** Parent
  task 6.1 alone is `[x]` — satisfied by hermes-install PR #46 (merged
  2026-08-27), which landed a *governance packet only*, whose own `tasks.md`
  says every checkbox in it "remains intentionally incomplete in this
  governance-only pull request". Parent tasks **6.2 through 6.8 are unchecked**.
  There is **no wallet or signature code in hermes-install `src/`**, **no
  exercise endpoint**, and **nothing deployed**. Evidence to open G1: 6.2-6.8
  checked, the merged code on hermes-install main, a green deploy, and the
  fail-closed refusal of an unverifiable seat signature demonstrated by a named
  test. Two precision points, because this gate is the likeliest to be waved
  through. (i) The requirement
  (`openspec/changes/add-wallet-carried-review-authority/specs/review-authority-intake/spec.md:157-180`)
  refuses an exercise "evidenced only by the existing council or enforcement
  audit trail", so an audit-trail demonstration does **not** open this gate.
  (ii) The 6.2-6.8 numbering exists in **two** packets — openxFactory's
  `add-wallet-carried-review-authority/tasks.md` §6 and hermes-install's own
  successor `add-wallet-exercise-verdict-conformance/tasks.md` — and **ticking
  one does not tick the other**. The openxFactory ticks are conditional on the
  hermes-install ones, and the gate record must quote the **path and name of the
  test file** asserting the refusal, not a checkbox count — **and that test must
  be GREEN IN CI on hermes-install `main`**, not merely present, since a skipped
  or `xfail` test satisfies the words "named test file" while asserting
  nothing.
- **G2 — S5 merged.** Revocation re-checked at verdict *consumption*, a revoked
  or expired holder parking with a **named refusal**, an unreadable register
  refusing. **Current state: NOT MET. Tasks 7.1-7.7 are ALL unchecked, and no
  revocation-of-review-authority code exists in hermes-install** (the only
  `revok*` code there governs unrelated manager-review and approval decisions).
  Evidence: 7.1-7.7 checked; a **named test file path** asserting that a revoked
  holder parks a convening with a named refusal and that an unreadable register
  refuses — task 7.7 is a prose `**Gate:**` line, not a test, so the test must be
  named explicitly; and a **dated runbook-walk record committed at a stated
  path**, countersigned by a NAMED verifier who is not the walker, since 7.6's
  "walked once" otherwise leaves no artifact and no attestor.
- **G3 — R1 merged and reporting.** **Current state: NOT MET, but closer than
  the rest.** R1 is **OPEN as PR #439** at head `f012eb10` — not draft,
  `wallet-validation` SUCCESS, `pytest-suite` in progress at the time of
  writing — and it is **unmerged**. `merge-master-approval` has **never
  reported** on this repository: neither on `main` (check-runs API returns
  `pytest-suite` only) nor on PR #439 itself, whose rollup carries no such
  context. Note R1's own accepted cost, which is why those two facts are
  consistent: `pull_request_target` resolves the workflow from the **base**
  branch, so R1 does not run on the pull request that introduces it. Evidence to
  open G3: PR #439 merged, **and** a named subsequent pull request showing a
  real `merge-master-approval` check-run with a recorded conclusion.
- **G4 — the class boundary exists as rules-as-code.** Four parts, and the
  ordering between them matters because the architecture is per-repo
  self-hosted. **Current state: NOT MET at every part.**
  (a) `[openxFactory]` the repository must author its own
  `.github/merge-approval-envelope.yml` with one candidate whose
  `path_allowlist` is exactly the four entries in "The boundary this change
  draws" — a `.github/**` file and therefore a CODEOWNERS-routed human act.
  (b) `[codexFactory]` the bound gate rule must exist, at
  `classification_intent: **advisory**`, carrying `applies_to.candidate_id`;
  `add-substantive-review-lane` task 3.2 still owes the `gate_rules_council`
  record, and today openxFactory has **no gate rule at all**. The prepared
  `openxfactory-derived-health-artifact-advisory-v1` is `defined_not_wired`, and
  `_validate_defined_not_wired` **forces** advisory in that state, so
  `clearable` is not merely unset but structurally unreachable until (a) lands.
  (c) `[codexFactory]` the floors must be completed **in the right carriers**,
  which is not one file. `openxfactory-review-authority-floor.yaml` is
  `kind: repository_gate_floor`, and `repository_floor.py` **refuses wildcards
  outright** ("must be exact; wildcards are not allowed") with `matching_paths`
  doing exact set membership — so it can only ever hold exact chokepoint FILES,
  and the three `governance/review-authority/{grants,wallets,attestations}/`
  entries the lead-security finding names must be enumerated as files or moved
  to a glob carrier. The glob-capable carrier is a **clearance rule**'s
  `never_clearable_paths` in the envelope glob dialect, as
  `codexfactory-routine-code-clearance.yaml` already does. So (c) splits:
  **(c-i)** an `openxfactory-*-clearance.yaml` carrying the glob floor;
  **(c-ii)** the exact-file additions to the `repository_gate_floor`; and
  **(c-iii)** **the claim an earlier draft made here is WITHDRAWN.** That draft
  said "nothing further is owed" because the repo-independent class floor
  (`class_floor_problem`) "already refuses `contracts/`, `.github/`, `scripts/`,
  `tests/`, `governance/`, `openspec/` and `schemas/` for every repository, wired
  or not". **It does not, for openxFactory.** `class_floor_problem` validates a
  *gate rule*, taking `(rule, candidate)`; its two callsites are
  `validate_rule:1500`, guarded `if candidate is not None`, and
  `evaluate_with_clearance:2071`. **A repository with no gate rule gets no
  evaluation at all** — today's protection is the absence of a mechanism, not a
  running control. And `:1084` returns `None` for any advisory rule, so the floor
  is a **no-op on exactly the class this change enrolls**; `load_rule()` never
  passes a candidate, and `_config_governs:289` returns False cross-repo, so
  codexFactory CI validating openxFactory's rule resolves no candidate and skips
  the floor permanently. The helpers that *would* judge an advisory class —
  `would_pass_class_floor`, `advisory_as_currently_defined` — have **zero
  production callsites; tests only.**
  **This was the packet's single largest reliance, and it was specified-only.**
  So (c-iii) is not "nothing" but two acts: wire one of those helpers into a
  production gate so an advisory class's floor status is COMPUTED rather than
  skipped, and require G7's flip evidence to include that call returning `None`
  for this class against the real base-branch candidate.
  **(c-iv)** repo-relative `GATE_INTEGRITY_PROBES`, resolving the widen-only /
  reachability contradiction for a foreign repository lacking
  `instantiation-answers.yaml` and `sonar-project.properties`.
  (d) `[openxFactory]` R1's `contracts/review-lane-pin.yaml` must then advance
  to a codexFactory commit carrying (b) and (c). **The accountable advancer is
  the code owner named on that path, `@brettheap`** — the advance touches two
  owner-routed paths (`/contracts/review-lane-pin.yaml` and, if the workflow
  moves with it, `.github/workflows/`), so it is human-only under this
  proposal's own boundary and must be performed as the recorded re-point
  ceremony the pin file already obliges, not as a one-line edit. Note the
  ordering constraint the `DERIVED_ARTIFACT_ROOTS` narrowing set as precedent: it
  was a **paired landing** with `opensoft/xFactory` PR #153, sequenced so the
  lane never went dark. Any pin advance here inherits that discipline.
  Evidence: the envelope merged, the gate-rules record merged, the clearance-rule
  and floor additions with tests green, and the advanced pin with
  `tests/review_lane_pin/` green.
  **Recorded so it is not re-litigated:** the floor file at R1's pinned commit
  `58bd3cf7` is **byte-identical to codexFactory `origin/main`** — the pin is
  behind main in general but **not stale for this file**.
- **G4b — an APPROVAL-CAPABLE caller exists in openxFactory.** `[openxFactory]`
  **This gate was missing from an earlier draft of this proposal and its absence
  was the draft's most serious defect.** R1 is structurally read-only —
  `permissions: contents: read, pull-requests: read`, and its header states
  "NO APPROVAL … The absence is STRUCTURAL", "NO ENROLLED CANDIDATE CLASS", "no
  tier-1 envelope decision is computed here at all". **So nothing in G1-G4 lands
  the thing that would actually cast the review.** A separate openxFactory
  workflow is required, under its own change — and the council corrected four
  things about its decomposition that an earlier draft got wrong.
  (i) **Its job id must SHARE the `merge-master-approval` substring** (e.g.
  `merge-master-approval-cast`) yet must not EQUAL R1's. R1 is
  `name: merge-master-approval` / `jobs.merge-master-approval`, and its
  "exactly one job" test is scoped to its own file, so a second file reusing that
  id would produce **two same-named check-runs on one SHA** — ambiguous for the
  envelope's latest-run-per-name selection. The shared substring is REQUIRED
  because `excluded()` matches by substring: a wholly distinct id such as
  `review-lane-approver` would **not** be excluded, and the approver's own
  check-run would then sit inside the all-checks-green test it computes,
  **reopening the very deadlock this packet records as closed.**
  (ii) **`check_exclusions` is a PER-CANDIDATE ENVELOPE field, not a workflow
  property.** The earlier draft told the workflow to "carry
  `check_exclusions: [merge-master-approval]`" — the wrong layer AND the wrong
  target, since that string excludes *R1's* check. The candidate must list
  **both** job ids.
  (iii) **The envelope lands BEFORE the approver**, explicitly: the approver
  reads the envelope from the base branch, so the pull request that *introduces*
  the envelope is evaluated by an approver that cannot see it.
  (iv) **G4(a) will turn a landed green test RED**, and this packet owns it —
  R1's `test_the_caller_ships_no_envelope_instance` asserts
  `.github/merge-approval-envelope.yml` **does not exist**. Retiring it is a
  named task, not a surprise.
  The workflow holds `pull-requests: write`, mints a dedicated App token (never
  `GITHUB_TOKEN`), and submits the `APPROVE`.
  Evidence: the workflow merged; a test asserting the exclusion lists both job
  ids; a test asserting `GITHUB_TOKEN` is never used to review; the
  installation's permission set enumerated; `POST /pulls/{n}/reviews` named as
  the **only** write it performs; and a test asserting it never calls a
  review-dismissal endpoint — because `pull-requests: write` also permits
  **dismissing a human's `CHANGES_REQUESTED` review**, so the mechanism that adds
  an approval could otherwise remove a human's refusal.
- **G5 — the App can actually cast a review here.** `[OPERATOR]`: the
  merge-master App installed on `opensoft/openxFactory` **with write access**
  (GitHub counts approvals only from reviewers holding write permission), and its
  identifiers present as repository secrets. **Evidence must be an artifact, not
  an assertion** — this is the gate on which the whole mechanism turns, and a
  sentence in a session log must not be able to close it: a throwaway pull
  request on `opensoft/openxFactory`, the App's `APPROVE` cast on it, and the
  `gh api repos/opensoft/openxFactory/pulls/<N>` JSON showing
  `reviewDecision: APPROVED` plus the `mergeable_state`, captured verbatim into
  a committed record at
  `openspec/changes/adopt-council-cleared-merge-gate/evidence/g5-app-review.md`.
  The general question is **already answered in-org and is no longer open**: on
  `opensoft/xFactory` — targeted by the same ruleset `18962101`, unmodified since
  2026-07-14 — PRs #85 and #100 each carried exactly one `APPROVED` review, cast
  by the App `codexfactory`, and GitHub computed `reviewDecision: APPROVED`. And
  `require_extra_approval_for_unattributed_changes` keys on the pull request's
  **author** (GitHub documents it for unattributed Copilot-authored pull
  requests, raising the required count by one), **not** on who reviews, so it
  does not bear on an App's eligibility to approve at all. The residual is
  narrow and repository-specific: does *this* installation hold write on *this*
  repository — **Q1**.
- **G6 — the register row is live at exercise.** Row `row-mrc-0001` expires
  `2026-11-23T12:00:00Z`. It must be re-issued before then, and — per
  `review-authority-intake` `spec.md:181-201` — expiry is judged from
  `expires_at`, **not** from the stored `state`. A lapsed row does not degrade
  the lane; it refuses it.

- **G7 — the flip to `clearable` is a SEPARATE ratified act.** This change
  authorizes the boundary and the advisory enrollment. It does **not** authorize
  setting `classification_intent: clearable`. That flip requires G1-G6 green,
  the canary complete with zero disagreements, and a named successor change
  recording it. Stating it as a gate rather than as a closing paragraph is the
  point: the flip is one field in one YAML file, which is exactly the kind of
  act that gets made because everything around it looked ready.

**Gate ordering, corrected by the council.** The sequence is
**G3 → G4(a) → G4(c) → G4(b) → G5 → G1/G2 → G6 → canary → G7**. An earlier draft
placed G4(b) and G5 before G4(c), landing an approval-capable caller holding a
live App token while the only remaining restraint was `is_advisory(rule)` — one
field, in a different repository, reached through a pin that G4(d) advances. The
draft named that hazard in G7 and then adopted the ordering that maximised it.
G4(b) and G5 now land immediately before the canary, and G4(c) carries an
explicit dependency on G4(a).

**G1 and G2 are the load-bearing ones and neither is close.** This proposal is
being authored while the mechanism it governs is unbuilt, on purpose, so that
the boundary is ratified before the capability arrives rather than after.

**Nothing in this packet may be read as evidence that any gate is open.** Every
gate above is recorded as NOT MET as of 2026-08-27, and the state of each is a
fact to be re-verified at adoption, never inherited from this text.

## Canary, kill switch, rollback

- **Canary — dual-run, N = 3, prose class only.** The first three
  candidate-class openxFactory pull requests run **both** paths: the council
  reaches and records a verdict, **and** a human casts the approving review that
  actually merges the pull request. Three agreements with zero disagreements is
  the bar. A single disagreement stops the canary and reopens this change.
  An earlier draft required **six, split ≥3 across two classes**. The council
  established that the second class has produced **zero pull requests ever** in
  one of its trees and none in five weeks in the other, so that canary could
  never complete and **the flip to `clearable` was structurally unreachable** —
  the packet would have ratified a boundary it made permanently unexercisable.
  With the derived class deferred, **each class carries its own canary in the
  change that enrolls it**, which preserves the class-boundary-error detection
  the review round asked for without conditioning this class's adoption on
  traffic that does not exist.
- **Canary recording — and the property that makes it trustworthy.** Each pair is
  recorded at
  `openspec/changes/adopt-council-cleared-merge-gate/evidence/canary/<pr>.md`:
  pull request, verdict, human judgement, agreement. A verdict that lands at no
  path is not an observation. The council's objection — that the canary is
  self-reported, with no named recorder, no mechanical count, and no blinding, so
  a disagreement is discoverable-then-editable by whoever writes the file —
  stands as an acknowledged weakness in the *process*. **The structural mitigation
  the packet should have claimed and did not:** `evidence/canary/` sits under
  `openspec/changes/**`, which `GATE_INTEGRITY_FLOOR` floors at PR time, so **the
  canary record can never be cleared by the lane it judges.** The recorder is
  named as an `[OPERATOR]` task, and G7's evidence must count the records rather
  than assert the canary complete.
- **Kill switch — revoke, do not reconfigure. TWO stops today, three after G2.**
  An earlier draft claimed three independent stops. The council traced them and
  found one of the three depends on substrate this change itself records as
  unbuilt. Corrected:
  - **Stop A (running).** Set `human.kill_switch` on the codexFactory gate rule,
    or flip `classification_intent` back to `advisory` — the standing STOP the
    rules-as-code already carries (`council_clearance.py:1995`, `:2023`).
  - **Stop B (running).** Remove the approval-capable caller's App credentials
    from openxFactory's repository secrets, so no approver token can be minted.
    Note this names the **approval-capable caller of G4b**, not R1: R1 is
    structurally read-only and mints nothing, so removing *its* secrets stops a
    report, not an approval — an attribution the earlier draft got wrong.
  - **Stop C (NOT AVAILABLE until G2).** Setting `row-mrc-0001`'s `state` to
    revoked refuses the lane only under S5's revocation-at-consumption, and
    **S5 is G2, which this change records as NOT MET with no such code in
    hermes-install.** Until G2 is green this stop does not exist. **G6's
    expiry safety rests on the same unbuilt S5** and inherits the same caveat.
  None of the available stops touches a rule affecting the other six
  repositories.
- **Rollback.** There is nothing to revert in the review rule, which is the
  design's main safety property; the one ruleset edit is a hardening that should
  survive a rollback rather than be undone by it. Rolling back is returning the
  class to `advisory` and leaving openxFactory's lane where R1 already stands.
  The bypass ritual returns with it; that is the cost, and it is accepted.
- **What "ending the bypass" does and does not mean.** All three gating rulesets
  keep `OrganizationAdmin / bypass_mode: always`, and **this change proposes no
  task that narrows or removes it.** The bypass *capability* survives adoption
  untouched. What ends is its **routine use** as the merge path for prose pull
  requests. The evidence that this is a real ritual and not a rhetorical one: the
  last 25 merges to openxFactory `main` all show
  `reviewDecision: REVIEW_REQUIRED` with `mergedBy: brettheap` — merged, every
  one, with the review rule unsatisfied.
  **And the council found the ritual is not merely habit but structurally
  forced.** `@brettheap` is the sole CODEOWNERS owner **and** the
  `OrganizationAdmin` bypass actor, and GitHub bars self-approval — so for a pull
  request he authors touching an owned path, the code-owner floor **can only ever
  be discharged by the bypass this change exists to end**. Consequence 4's claim
  that CODEOWNERS provides independent human accountability is therefore
  corrected: it is un-spoofable **against the App**, and **unsatisfiable by its
  sole owner**. The owed widening of the route to `.github/` *enlarges* that
  bypass-only surface. Folded into **Q6**, which asks whether the actor should be
  narrowed — deliberately not folded into this change, because narrowing an
  org-level bypass is a seven-repository act.

## Relationship to the two active ratified changes

Per `docs/release-realization-flow.md:88-91`, a proposal modifying a requirement
an active ratified change already modifies must reference it and declare its
deltas relative to that change's outcome (**first-ratified wins**).

- **`add-substantive-review-lane`** (ratified 2026-08-22, active, unarchived).
  Its `roles-authority-model` delta is **the parent doctrine of this change**,
  and this change claims **PARITY, not amendment**, with three of its
  requirements: *Ruleset interaction shape* (this change adopts the prescribed
  App-review shape and declares **no divergence**, so the
  divergence-recording clause is not invoked); *Pilot repository and reviewing
  domain* (which **names `opensoft/openxFactory` as the pilot** — this change is
  that pilot's adoption change, not an extension, so the ≥3-verdict evidence bar
  for adoption *beyond* the pilot does not apply to it and is not claimed);
  *Constitutional floor* (adopted as the class boundary's source, with its
  six-member source record named and only its two path-shaped members drawn
  here).
  One caveat carried rather than hidden: that change's `tasks.md` 8.2 records a
  2026-08-26 convener ruling **inverting the floor's source of truth** to a YAML
  carrier, and **the delta moving it has not been authored**. This change cites
  the floor as it currently reads and flags the pending inversion as **Q2**.
- **`add-wallet-carried-review-authority`** (ratified 2026-08-23, active,
  unarchived). This change is a **CONSUMER** of its `review-authority-intake`
  capability and amends none of it. It depends on S3 (`spec.md:157-180`) and S5
  (`spec.md:181-201`) and treats both as unrealized. It also inherits that
  capability's requirement that **no holder is issued both the review act and
  the approval act over one object** (`spec.md:140-149`) — which this design
  must answer, because the merge-master App casting the approving review while
  the council holds the review act is exactly the collapse that requirement
  polices. The `distinct_holder_constraint_refs` treatment is **Q4**.

## Open questions

Five questions the earlier draft carried are **closed**, by shipped
rules-as-code rather than by argument, and are recorded as closed so they are not
re-opened as though undecided:

- **CLOSED — is `scripts/**` human-only?** Yes, and not by this change's
  assertion. `scripts/**` is in `GATE_INTEGRITY_FLOOR`
  (`council_clearance.py:136`, "the decision core's whole import root") **and**
  `scripts/` is in `PROTECTED_CLASS_SURFACES` (`:852`). Same for `tests/**`,
  `contracts/*.schema.yaml` (via `contracts/` and `schemas/`) and `.github/**`.
  The earlier draft presented these as boundary calls it was making and owed a
  CODEOWNERS task; they are **inherited controls already running**, and
  presenting a shipped control as an owed one is the same error as the reverse.
- **CLOSED — does an App-cast `APPROVE` satisfy `18962101`?** Yes; xFactory PRs
  #85 and #100 under the same unmodified ruleset. See G5.
- **CLOSED — does `require_extra_approval_for_unattributed_changes` block it?**
  No; it keys on the pull request's author, not the reviewer. See G5.
- **CLOSED — is the self-reference deadlock escapable?** Yes;
  `check_exclusions: [merge-master-approval]` already exists and is why the job
  id is load-bearing. See rejection ground 1.
- **CLOSED — does the beyond-pilot ≥3-verdict evidence bar bind this change?**
  No; openxFactory is the **named pilot**
  (`add-substantive-review-lane` … `spec.md:149`), and the bar's subject is
  "Extension … beyond the pilot repository". The canary is set by this change's
  own choice instead.

What remains genuinely open:

- **Q1 — does the merge-master App installation hold write access on
  `opensoft/openxFactory`?** GitHub counts approvals only from reviewers with
  write permission. This is the residual of the old Q1 after the in-org evidence
  closed its general form, and it is **repository-specific, empirical, and
  gating**: if the answer is no and cannot be made yes, this change's core
  mechanism does not work and must return. G5 answers it with an artifact.
- **Q2 — which floor source of truth does this change cite?** The floor's
  ratified source of truth is codexFactory's `gate_rules_council` record of
  2026-07-23, and `add-substantive-review-lane`'s `tasks.md` 8.2 records a
  2026-08-26 convener ruling **inverting** that to a YAML carrier — with the
  delta moving it **not yet authored**. This proposal cites the requirement text
  as it currently reads and does not presume the inversion.
- **Q3 — is the separately-named required floor check (`review-lane-floor`)
  wanted as hardening**, or is fail-closed-by-absence-of-verdict sufficient?
  Rejection grounds 2-4 argue sufficient; the convener may disagree.
- **Q4 — the merge-master App's approval act has NO register row.** The register
  holds one row, `row-mrc-0001`, `act: review`, held by
  `agent:merge-readiness-council`. `review-authority-intake` requires that no
  holder hold both the review act and the approval act over one object and names
  `distinct_holder_constraint_refs` as the instrument. Today the separation is
  satisfied **vacuously**, because the approving act is held by nobody. So the
  question is not interpretive but a **missing artifact**: does the App's
  approval act need its own row, and what binds it to `row-mrc-0001`?
- **Q5 — the six-member floor's four non-path conditions.** The ratified floor is
  not exhausted by paths: its source record carries **identity mismatch,
  head-ref mismatch, failed or pending required checks, secret findings**,
  security-touching paths and gate-weakening changes. This proposal draws only
  the **path-shaped subset**. Who states, and where, that the openxFactory lane
  enforces the other four? They are in codexFactory's envelope today; the
  question is whether openxFactory's own envelope must restate them.
- **Q6 — should the `OrganizationAdmin` bypass actor be narrowed?**
  Deliberately excluded from this change: narrowing an org-level bypass is a
  seven-repository act, and this change's whole design premise is to avoid
  seven-repository acts. But leaving it unasked would let this proposal claim to
  "end the bypass" while the bypass stands untouched. **The council sharpened
  this**: `@brettheap` is both the sole code owner and the only bypass actor, and
  GitHub bars self-approval, so the code-owner floor on his own pull requests is
  *structurally* dischargeable only by bypass. Q6 is therefore not a tidiness
  question but the question of whether the assembly-class floor means anything
  today.
- **Q7 — the high-value class is locked, and nobody has proposed the key.** The
  measurement found that **4 of the recent 40 merged pull requests are
  `openspec/changes/**/tasks.md`-only checkbox ticks** — more traffic than this
  proposal's class at its historical peak. `openspec/changes/**` is floored at PR
  time and `openspec/` at class level, and narrowing a floor is forbidden, so
  this change cannot reach it. Does the convener want a doctrine amendment
  defining a checkbox-only class by DIFF SHAPE rather than by path — the
  objection to `openspec/changes/**` being that it holds the change records,
  which a checkbox tick does not alter? If not, should the pilot move to
  `opensoft/xFactory`, which already carries the org's only `clearable` class and
  a recurring producer, i.e. real traffic to canary against?
- **Q8 — should every clearance proposal in this family be required to state a
  falsifiable expected-benefit figure** measured against merged-pull-request
  history? This proposal was scrupulous about verifying gate states and never
  asked how many pull requests its relief touches; it would have failed such a
  test at authoring, four days before the council caught it.
