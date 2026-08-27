# Tasks: adopt-council-cleared-merge-gate

Status: draft

**Tags.** `[openxFactory]` this repository. `[codexFactory]` the decision core
and its gate rules. `[hermes-install]` the Hermes runtime. `[OPERATOR]` an act
only the accountable human can perform (GitHub org/repo configuration, App
installation, secrets, register issuance) — these are NOT agent-executable and
are never ticked by an agent on its own authority.

**Ordering is load-bearing, and the council changed it.** The sequence is
§2 (G3) → §3 (G4a/c/d) → §4 (G4b) → §5 (G5) → §6/§7 (G1/G2) → §8 (G6) →
§10 (canary) → §11 (G7). **§4 runs AFTER §3**, reversing an earlier revision that
landed an approval-capable App token while the only remaining restraint was one
advisory field in another repository's YAML. §1 is this packet's own bookkeeping;
§9 (the ruleset hardening) may land any time and should outlive a rollback.

## 1. This packet

- [ ] 1.1 `[openxFactory]` Land this packet: `proposal.md`, `design.md`,
  `tasks.md`, `clarifications.md`, `specs/council-cleared-merge-gate/spec.md`,
  the two alignment records and the three council records.
- [ ] 1.2 `[openxFactory]` README "OpenSpec Records" entry for this change,
  added at the top of the active-changes block.
- [ ] 1.3 `[OPERATOR]` Convener's ruling on ratification. A gate-policy change
  is the convener's own act; this packet stops at `Status: draft` and no agent
  writes `Status: ratified`.
- [ ] 1.4 `[openxFactory]` On ratification, record the ruling verbatim in
  `proposal.md` and dispose **Q1-Q8** explicitly — each either answered, carried,
  or assigned to a named successor. Q7 (the locked `openspec/changes/**/tasks.md`
  class, where the traffic actually is) and Q8 (whether this family must state a
  falsifiable expected-benefit figure) were added by the council and are the two
  most likely to change what gets built next.
- [ ] 1.5 `[openxFactory]` This change SHALL NOT be archived while its adoption
  gate (G7) stands unopened. `code_surface: none` would otherwise archive it on
  landing, filing a policy as realized whose enabling acts are all ahead of it.

## 2. G3 — the advisory lane reports (nothing is enabled)

- [ ] 2.1 `[openxFactory]` Merge PR #439 (R1, `025-openxfactory-review-lane-caller`,
  head `f012eb10`). Not this change's act; recorded as the dependency it is.
- [ ] 2.2 `[openxFactory]` Confirm a real `merge-master-approval` check-run with
  a recorded conclusion on a named pull request AFTER #439 lands. R1's
  `pull_request_target` resolves from the base branch, so it cannot run on the
  pull request that introduces it — the first live report is the next one.
- [ ] 2.3 `[openxFactory]` Record the check-run URL and conclusion in
  `evidence/g3-first-report.md`. A gate whose evidence is a memory is not open.

## 3. G4 — the class boundary as rules-as-code

- [ ] 3.1 `[openxFactory]` Author `.github/merge-approval-envelope.yml` with the
  ONE candidate `openxfactory-governance-prose` (`docs/**/*.md`,
  `ideation/**/*.md`, `README.md`). Suffix-pinned patterns with non-empty literal
  prefixes only — a bare leading wildcard is refused, and `.md` is the only docs
  suffix the enforcer accepts. Required per-candidate fields, none optional:
  `target_repos: [opensoft/openxFactory]`; an author matcher
  (`author_class.council_cleared_logins: [brettheap]`);
  `require_same_repository: true` (**schema-forced** whenever
  `council_cleared_logins` is present); a **`head_ref_pattern`** — the ONLY
  selector `_find_surface` consults, since paths are never used for selection;
  `check_exclusions` listing **both** openxFactory job ids that emit a
  `merge-master-approval`-substring check; and
  `requires_intent_reference: true`, which is **opt-in** — `:1672` never checks
  intent without it.
- [ ] 3.1a `[openxFactory]` Add a depth-independent PR-time refusal of the twelve
  `PROTECTED_ROOT_FILES` basenames. `PROTECTED_ROOT_FILES` is applied
  **root-exact** (`council_clearance.py:1045`), so `docs/**/*.md` otherwise
  admits `docs/AGENTS.md` and `docs/sub/CLAUDE.md` — which the enforcer's own
  comment calls "prompt injection into the governance loop".
- [ ] 3.1b `[openxFactory]` Retire R1's
  `test_the_caller_ships_no_envelope_instance`, which asserts the envelope does
  NOT exist and which task 3.1 necessarily turns red. Owned here rather than
  discovered in CI.
- [ ] 3.2 `[openxFactory]` Widen `.github/CODEOWNERS` from `.github/workflows/`
  to `.github/`, so `CODEOWNERS` itself and the new envelope are owner-routed.
  Today they are not, and the proposal must not claim the envelope's authoring is
  an owner-routed act until this lands.
- [ ] 3.3 `[codexFactory]` Author the `gate_rules_council` record defining
  openxFactory's ONE candidate class — the record `add-substantive-review-lane`
  task 3.2 still owes. At `classification_intent: advisory`.
- [ ] 3.4 `[codexFactory]` Author the per-repo gate rule (ONE document —
  `applies_to.candidate_id` is a single string), binding by explicit
  `applies_to.candidate_id`, never inferred from a rule id or repository field.
  Every field below is required, and three are hard validation failures if
  omitted: `risk_tier: {id, rationale}` — **and this change must DEFINE the `id`
  vocabulary, because `:1263` accepts any non-empty string and closes nothing**;
  `anti_normalization` with EXPLICIT semantics (`consecutive_candidates` +
  `same_condition_cleared_consecutively`, or `rolling_window` + its three
  parameters), never inferred from the surface (`:1338`);
  `activation_dependency`, required by the same `_validate_defined_not_wired`
  this change leans on; `gate_integrity.never_clearable_paths`, mandatory once
  `classification_intent` is declared; `council_clearable[]` entries with `id`,
  `owning_seat`, `tier1_condition` and allowlist, plus `docs_class_allowlist`
  for the `docs_only_path_overflow` entry this change invokes by name; exactly
  one resolving `clearance_rule`; `active` as a real bool; and
  `human.accountable: brettheap` as a **bare login** — `:1477` refuses a leading
  `@`, which every earlier revision of this packet wrote.
- [ ] 3.5 `[codexFactory]` Author `openxfactory-*-clearance.yaml` carrying the
  GLOB floor in the envelope dialect, following
  `codexfactory-routine-code-clearance.yaml`. The glob floor cannot live in the
  `repository_gate_floor` — `repository_floor.py` refuses wildcards outright.
- [ ] 3.6 `[codexFactory]` Add the exact-FILE entries closing the
  lead-security floor-reachability gap the floor file's own header records:
  `governance/review-authority/{grants,wallets,attestations}/` members, named as
  files. With tests.
- [ ] 3.7 `[codexFactory]` **Wire an advisory class's class-floor status into a
  PRODUCTION gate.** The proposal's largest single reliance was
  specified-only: `class_floor_problem` returns `None` for any advisory rule
  (`:1084`), its two callsites resolve no candidate for a foreign repository
  (`validate_rule:1500` guarded on `candidate is not None`;
  `_config_governs:289` False cross-repo), and the helpers that WOULD judge an
  advisory class (`would_pass_class_floor`,
  `advisory_as_currently_defined`) have **zero production callsites — tests
  only**. Wire one of them, and assert by test that it refuses `contracts/`,
  `.github/`, `scripts/`, `tests/`, `governance/`, `openspec/` and `schemas/`
  **for openxFactory specifically**, against the real base-branch candidate.
- [ ] 3.7a `[codexFactory]` Add a PR-time `baseline` SEGMENT guard on changed
  paths. `PROTECTED_PATH_SEGMENTS` is enforced only inside
  `pattern_is_docs_or_derived` — a definition-time PATTERN check — so
  `health/<root>/**` validates and then admits `.../baseline/...`. Not needed by
  this change's one class, and owed before any derived class is enrolled.
- [ ] 3.7b `[codexFactory]` Make `GATE_INTEGRITY_PROBES` repo-relative, resolving
  the widen-only / reachability contradiction: widen-only demands the declared
  floor cover `instantiation-answers.yaml` and `sonar-project.properties`, **both
  absent from openxFactory**, while reachability refuses entries matching
  nothing, and R1's `test_the_caller_opts_into_the_floor_reachability_check`
  requires openxFactory to opt in. The two controls contradict for any foreign
  repo. **Do not resolve this by silently declining to pass `tree_paths`.**
- [ ] 3.8 `[openxFactory]` `[OPERATOR]` Advance `contracts/review-lane-pin.yaml`
  to a codexFactory commit carrying 3.3-3.7, as the recorded re-point ceremony
  the pin file obliges. Accountable advancer is the code owner named on that
  path. Inherit the paired-landing discipline the `DERIVED_ARTIFACT_ROOTS`
  narrowing set with xFactory PR #153: sequence so the lane never goes dark.
- [ ] 3.9 `[openxFactory]` `tests/review_lane_pin/` green against the advanced
  pin.

## 4. G4b — an approval-capable caller exists

**Ordering: this group runs AFTER §3, not before.** A prior revision placed it
first, leaving a live App token whose only restraint was one advisory field in
another repository's YAML, read through a pin.

- [ ] 4.1 `[openxFactory]` Author the approval-capable workflow, SEPARATE from
  R1: reads the envelope from the base branch, computes the candidate class and
  the tier-1 envelope decision, holds `pull-requests: write`, mints a dedicated
  App token, submits the `APPROVE` review. R1 is structurally read-only, and its
  read-only-ness is proven by test over its own file text, so growing it would
  mean retiring the assertions that make its safety legible.
- [ ] 4.2 `[openxFactory]` Give the approver a job id that **shares the
  `merge-master-approval` substring but does not equal R1's** — e.g.
  `merge-master-approval-cast`. Shared because `excluded()` matches by substring,
  so a distinct name leaves the approver's own check inside the all-checks-green
  test it computes and **reopens the deadlock this packet records as closed**;
  not equal, because two same-named check-runs on one SHA are ambiguous for
  latest-run-per-name selection.
- [ ] 4.3 `[openxFactory]` Put `check_exclusions` on the **CANDIDATE in the
  envelope** — it is a per-candidate envelope field, not a workflow property —
  listing **both** job ids. A prior revision put it on the workflow and named
  only R1's check, which would have excluded the wrong check.
- [ ] 4.4 `[openxFactory]` Sequence: the envelope (3.1) lands BEFORE this
  workflow. The approver resolves the envelope from the base branch and therefore
  cannot see the pull request that introduces it.
- [ ] 4.5 `[openxFactory]` Tests: the exclusion lists both job ids;
  `GITHUB_TOKEN` is never used to cast a review; no approval is possible while
  the class is `advisory`; and **the caller never calls a review-dismissal
  endpoint** — `pull-requests: write` also permits dismissing a human's
  `CHANGES_REQUESTED` review, so the mechanism that adds an approval could
  otherwise remove a human's refusal.
- [ ] 4.6 `[openxFactory]` Share ONE pin per repository: the approver reads
  `council_clearance.py` and `envelope.py`, which R1's `pinned_members` does not
  list. Widen `contracts/review-lane-pin.yaml`'s `pinned_members`, and assert by
  test that every openxFactory workflow checking out the core resolves the same
  `core_commit`. Convert R1's prose `lockstep.obligation` into an executable
  check BEFORE adding this fifth pin surface.

## 5. G5 — the App can actually cast a review here

- [ ] 5.1 `[OPERATOR]` Install the merge-master App on `opensoft/openxFactory`
  with **write** access. GitHub counts approvals only from reviewers holding
  write permission — this is Q1 and it is gating.
- [ ] 5.2 `[OPERATOR]` Provision the App identifiers as repository secrets.
- [ ] 5.3 `[OPERATOR]` Confirm the App holds NO ruleset or branch-protection
  write, per the promoted authority-separation requirement: the identity doing
  routine work must not be able to weaken the gate it is subject to.
- [ ] 5.3a `[OPERATOR]` Enumerate the installation's permission set in the
  evidence record, and confirm `POST /pulls/{n}/reviews` is the only write the
  approver performs.
- [ ] 5.4 `[openxFactory]` Capture the evidence artifact: a throwaway pull
  request, the App's `APPROVE` cast on it, and the
  `gh api repos/opensoft/openxFactory/pulls/<N>` JSON showing
  `reviewDecision: APPROVED` plus `mergeable_state`, committed verbatim to
  `evidence/g5-app-review.md`. The general question is closed by xFactory PRs
  #85 and #100 under the same ruleset; this closes the repository-specific
  residual, and a sentence in a session log may not close it.

## 6. G1 — S3 realized and deployed, with the refusal PROVEN

- [ ] 6.1 `[hermes-install]` Complete S3 (exercise-at-verdict): tasks 6.2-6.8 of
  `add-wallet-carried-review-authority`. **State as of 2026-08-27: 6.1 alone is
  ticked, satisfied by hermes-install PR #46 — governance packet only, whose own
  body says it changes no runtime code. 6.2-6.8 are unchecked; there is no
  wallet, signature or exercise code in hermes-install `src/`, no endpoint, and
  nothing deployed.**
- [ ] 6.2 `[hermes-install]` The 6.2-6.8 numbering exists in TWO packets —
  openxFactory's `add-wallet-carried-review-authority/tasks.md` §6 and
  hermes-install's `add-wallet-exercise-verdict-conformance/tasks.md`. Tick both
  explicitly; ticking one does not tick the other.
- [ ] 6.3 `[hermes-install]` Deploy, green.
- [ ] 6.4 `[hermes-install]` Prove the fail-closed refusal of an unverifiable
  seat signature by a NAMED test file, record its path, **and show it GREEN IN CI
  on hermes-install `main`** — a skipped or `xfail` test satisfies "named test
  file" while asserting nothing. An exercise evidenced only by the existing
  council or enforcement audit trail is explicitly insufficient under the
  requirement.

## 7. G2 — S5 merged

- [ ] 7.1 `[hermes-install]` Complete S5 (revocation-at-consumption): tasks
  7.1-7.7 of `add-wallet-carried-review-authority`. **State as of 2026-08-27: all
  seven unchecked; the only `revok*` code in hermes-install governs unrelated
  manager-review decisions.**
- [ ] 7.2 `[hermes-install]` Name the test file asserting that a revoked or
  expired holder parks a convening with a NAMED refusal, and that an unreadable
  register refuses. Task 7.7 is a prose `**Gate:**` line, not a test, so the test
  must be named explicitly.
- [ ] 7.3 `[hermes-install]` Commit a dated runbook-walk record at a stated path,
  **countersigned by a NAMED verifier who is not the walker**. Task 7.6's "walked
  once" otherwise leaves no artifact and no attestor.

## 8. G6 — the register row is live at exercise

- [ ] 8.1 `[OPERATOR]` Re-issue `row-mrc-0001` before its
  `expires_at: 2026-11-23T12:00:00Z`. Expiry is judged from `expires_at`, not
  from the stored `state`, so a lapsed row refuses the lane rather than degrading
  it.
- [ ] 8.2 `[openxFactory]` Confirm the register reader runs inside the required
  `wallet-validation` check against the re-issued row.

## 9. G2/D2 — the one ruleset hardening

- [ ] 9.1 `[OPERATOR]` Add `dismiss_stale_reviews_on_push: true`,
  `require_last_push_approval: true` **and
  `strict_required_status_checks_policy: true`** to ruleset `21538893`, which
  targets
  `openxFactory` alone. This makes locally owned a property currently inherited
  from the `~ALL`-repositories ruleset `18834180`. `strict` is currently
  **false**, so an approval survives a BASE advance as well as a head push — the
  stale-approval analysis covered only the latter. It is a HARDENING and the only
  ruleset edit this change proposes; it should survive a rollback rather than be
  undone by one.
- [ ] 9.2 `[OPERATOR]` Do NOT edit ruleset `18962101`. It targets seven
  repositories and the 1-approving-review rule stays.

## 10. The canary

- [ ] 10.1 `[openxFactory]` Run **three** dual-run observations on the prose
  class — council verdict AND human approving review on the same pull request.
  An earlier revision required six split across two classes; the second class has
  no producer, so that canary could never complete and G7 would have been
  structurally unreachable. **Each future class carries its own canary in the
  change that enrolls it.**
- [ ] 10.2 `[OPERATOR]` Named recorder for the canary. Record each observation at
  `evidence/canary/<pr>.md`: pull request, verdict, human judgement, agreement. A
  verdict that lands at no path is not an observation. The record is trustworthy
  for a structural reason worth stating: `evidence/canary/` sits under
  `openspec/changes/**`, which `GATE_INTEGRITY_FLOOR` floors at PR time, so **the
  canary record can never be cleared by the lane it judges.**
- [ ] 10.3 `[openxFactory]` A single disagreement stops the canary and reopens
  this change. Record the stop if it happens; do not re-run to a better result.
- [ ] 10.4 `[openxFactory]` G7's evidence must COUNT the records, not assert the
  canary complete.

## 11. G7 — the flip, which this change does NOT authorize

- [ ] 11.1 `[OPERATOR]` A SEPARATE ratified change naming the classes it flips
  to `classification_intent: clearable`, raised only on G1-G6 green and the
  canary complete with zero disagreements. **This change authorizes the boundary
  and the advisory enrollment, never the flip.**
- [ ] 11.2 `[openxFactory]` Re-verify every gate state at that moment against
  the running system. No gate is opened on evidence inherited from this
  document's text.

## 12. Kill switch, rehearsed before it is needed

**TWO stops exist today, not three.** A prior revision claimed three; one
depends on substrate this change records as unbuilt.

- [ ] 12.1 `[codexFactory]` Rehearse stop A (RUNNING): `human.kill_switch` on the
  gate rule (`:1995`, `:2023`), and the `clearable` → `advisory` reversion.
- [ ] 12.2 `[OPERATOR]` Rehearse stop B (RUNNING): remove the APPROVAL-CAPABLE
  caller's App credentials and confirm no approver token can be minted. This is
  the §4 workflow, **not R1** — R1 holds no write permission and mints nothing,
  so removing its credential stops a report, not an approval.
- [ ] 12.3 `[openxFactory]` Stop C is **NOT AVAILABLE until G2**: setting
  `row-mrc-0001` `state` to revoked refuses the lane only under S5's
  revocation-at-consumption, and S5 is unbuilt. Rehearse after G2. **G6's expiry
  safety rests on the same unbuilt S5** and carries the same caveat.

## 13. Deliberately NOT in this change

- [ ] 13.1 Narrowing the `OrganizationAdmin` bypass actor. All three gating
  rulesets keep `bypass_mode: always` and this change touches none of it. What
  ends is the bypass's ROUTINE USE, not the bypass. Raised as Q6.
- [ ] 13.2 Any extension of the lane to a repository beyond openxFactory. That
  requires its own change naming the repository, and must meet the beyond-pilot
  evidence bar (≥3 council-cleared PRs spanning ≥2 candidate classes, zero
  enforcer incidents, one completed gate-rules review cycle) which this change
  does not claim.
- [ ] 13.3 Making `openspec/**` clearable. Floored twice, and narrowing a floor
  is forbidden. **But this is where the traffic is** — 4 of the recent 40 merged
  pull requests are `openspec/changes/**/tasks.md`-only checkbox ticks, more than
  this change's class at its historical peak. Raised as Q7: a doctrine amendment
  defining a checkbox-only class by DIFF SHAPE rather than path, or moving the
  pilot to `opensoft/xFactory` which has real traffic.
- [ ] 13.4 Enrolling `openxfactory-derived-health-artifact`. Deferred to its own
  change, gated on a wired producer existing, the
  `add-classification-intent-and-substantive-classes` Phase-2 hold being lifted,
  and task 3.7a's PR-time `baseline` guard landing first.
