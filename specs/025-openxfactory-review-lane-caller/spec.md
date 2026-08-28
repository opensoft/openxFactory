# Feature Specification: openxFactory review-lane caller (advisory)

**Feature Branch**: `025-openxfactory-review-lane-caller`

**Created**: 2026-08-27

**Status**: Draft

**Input**: User description: "openxFactory gets its own merge-master-approval workflow instance that runs codexFactory's pinned Merge Master decision core over every openxFactory pull request and reports the `merge-master-approval` status check as ADVISORY only — it never approves, never touches a ruleset, and declares no enrolled candidate class. Realizes the workflow-instance half of `add-substantive-review-lane` task 5.1. Includes `contracts/review-lane-pin.yaml` (`kind: pinned_workflow`) plus a pytest drift test so the pinned core sha cannot drift silently."

## Why this exists, in one paragraph

`add-substantive-review-lane` is ratified (2026-08-22) and names
`opensoft/openxFactory` as its PILOT repository. Its task 5.1 says openxFactory
"gets its own workflow instance ... and its own ruleset wiring, since
`pull_request_target` fires in the repo the PR targets." Today openxFactory has
neither: `merge-master` appears in this repository only as prose, contract
vocabulary, and a cross-repo `gh workflow run` dispatch. Meanwhile codexFactory
already ships openxFactory's half of the governance data —
`scripts/merge_master/openxfactory-review-authority-floor.yaml`, a
`repository_gate_floor` naming three never-clearable openxFactory paths **at the
commit this caller pins** (a fourth, `contracts/review-lane-pin.yaml`, landed
upstream 2026-08-28 and reaches this repository only at follow-up 6.5's re-point)
— and nothing in openxFactory reads it. This feature lands the **workflow-instance
half only**, as an advisory reporter. The ruleset half of 5.1 is deliberately
NOT done here: it needs S3 and S5 of `add-wallet-carried-review-authority`
(the wallet-signed exercise record at `check_verdict`, and revocation at verdict
consumption) plus its own ratified ruleset change.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The reviewer sees the floor verdict on every pull request (Priority: P1)

A person opening an openxFactory pull request sees a `merge-master-approval`
status check that tells them, before any human looks, whether the pull request
touches a path the merge-readiness council may NEVER autonomously clear.

**Why this priority**: This is the whole advisory product. It is the only part
that changes what a reviewer sees today, and it is the part that proves the
pinned decision core is reachable from this repository at all — the wiring every
later, binding stage stands on.

**Independent Test**: Open a pull request that touches
`contracts/openxwallet-pin.yaml` and one that touches only `docs/`. The first
must report the pin as a floored path; the second must report no floored paths.
Both must report; neither may approve anything.

**Acceptance Scenarios**:

1. **Given** a pull request touching no path named in the openxFactory
   repository gate floor, **When** the caller runs, **Then** the
   `merge-master-approval` check reports success with an advisory verdict naming
   zero floored paths, and no review is submitted on the pull request.
2. **Given** a pull request touching `governance/review-authority/register.yaml`,
   **When** the caller runs, **Then** the check reports the floored path by name
   and states that autonomous clearance is permanently refused for this
   candidate, and no review is submitted.
3. **Given** any pull request whatsoever, **When** the caller finishes, **Then**
   no approving review, no merge call, and no auto-merge enablement has been
   performed by this workflow.

---

### User Story 2 - The pinned decision core cannot drift silently (Priority: P1)

A maintainer changing which codexFactory commit judges openxFactory pull
requests cannot do it without the change being visible as a diff in a
CODEOWNERS-gated pin file, and cannot leave the workflow and the pin
disagreeing.

**Why this priority**: Equal-first with Story 1. openxFactory has no
codexFactory gitlink, so nothing structural ties the workflow's `ref:` to a
recorded value. Without a recorded pin plus a test, "which core judged this pull
request" is answerable only by reading a workflow file, and advancing it is a
one-line edit nobody is obliged to notice. The precedent is xFactory's own pin
discipline, where the pin is asserted by test rather than trusted.

**Independent Test**: Change the `ref:` in the workflow without changing
`contracts/review-lane-pin.yaml` and run the repository's pytest suite. It must
fail, naming both values.

**Acceptance Scenarios**:

1. **Given** the workflow and the pin agree, **When** the suite runs, **Then**
   the drift test passes.
2. **Given** the workflow's `ref:` is edited and the pin is not, **When** the
   suite runs, **Then** the drift test fails and its message names the workflow
   value, the pin value, and the file to change.
3. **Given** the pin file is deleted or malformed, **When** the suite runs,
   **Then** the drift test fails rather than skipping.

---

### User Story 3 - A missing credential fails loudly, never vacuously green (Priority: P2)

An operator who has not yet granted openxFactory read access to the private
decision core sees a red check whose message names the exact secret to grant,
rather than a green check that proved nothing.

**Why this priority**: Third only because it is the state the repository is in
TODAY and will leave as soon as the grant lands. It is nonetheless mandatory:
the failure mode this forecloses — an advisory check that reports success
because it silently did nothing — is worse than having no check, because it
manufactures the appearance of review.

**Independent Test**: Run the caller in a repository without the decision-core
read credential. The check must conclude failure and its message must name the
absent secret.

**Acceptance Scenarios**:

1. **Given** the decision-core read credential is absent, **When** the caller
   runs, **Then** the check concludes FAILURE and the message names the exact
   secret identifiers required, and no fact is fabricated to keep the
   evaluation moving.
2. **Given** the credential is present but the pinned core checkout fails,
   **When** the caller runs, **Then** the check concludes FAILURE naming the
   pinned commit and the repository, never success.
3. **Given** the check is failing for either reason, **When** a human merges the
   pull request, **Then** nothing blocks them, because this check is configured
   in no ruleset.

---

### Edge Cases

- **A pull request whose changed-file set cannot be proven complete.** The
  platform's file listings truncate silently at documented ceilings. A gather
  that cannot prove it saw every changed path must PARK with that reason, never
  evaluate a floor over a list that was cut short — a floor evaluated over a
  truncated list reports "no floored paths" for a pull request that has them.
- **A force-push during the gather.** The head read at the start and the head
  read after pagination must agree, or the run refuses to decide over a mixed
  fact set.
- **A fork pull request.** It reaches the caller and must be evaluated with no
  head content executed and no secret exposed to head-authored code.
- **A pull request that edits this caller or its pin.** Rules must be read from
  the base branch only, so such a pull request governs nothing about its own
  evaluation.
- **The floor names a path absent from the openxFactory tree.** A floor that
  matches nothing is indistinguishable from no floor; the run must say so rather
  than report a clean verdict.
- **codexFactory ships no floor for `opensoft/openxFactory`.** The advisory
  verdict must name that absence as the reason it has nothing to judge, never
  render it as "clean".

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository MUST report a status check named exactly
  `merge-master-approval` on every pull request targeting its default branch.
  The name is load-bearing twice over: codexFactory's envelope excludes its own
  check-run by substring match on that literal, and a future ruleset will
  require that literal token.
- **FR-002**: The caller MUST read every rule, configuration, and pin it acts on
  from the BASE branch, never from the pull-request head, and MUST NOT check out
  or execute any pull-request head content.
- **FR-003**: The caller MUST obtain the decision core by checking out
  `opensoft/codexFactory` at an EXACT recorded commit, never at a moving ref.
- **FR-004**: The recorded commit MUST be declared in a committed pin artifact
  carrying `kind: pinned_workflow`, the pinned repository, the commit, and the
  date the pin was declared.
- **FR-005**: A test in this repository MUST fail when the workflow's pinned
  commit and the pin artifact's commit disagree, and MUST fail rather than skip
  when the pin artifact is missing or malformed.
- **FR-006**: The caller MUST evaluate the `repository_gate_floor` that the
  pinned core declares for `opensoft/openxFactory` against the pull request's
  changed paths, and MUST report which floored paths the pull request touches.
- **FR-007**: The caller MUST NOT submit any review, MUST NOT mint an approving
  identity's token, MUST NOT call merge, and MUST NOT enable auto-merge. This
  MUST be structural — the steps that would do those things are absent, not
  disabled by a condition.
- **FR-008**: The caller MUST declare no enrolled candidate class and MUST ship
  no `merge-approval-envelope` instance, because the `gate_rules_council` has
  defined **no OPERABLE candidate class** for this repository
  (`add-substantive-review-lane` task 3.2). The gate holds for as long as that
  remains true, and is discharged only when **BOTH** hold: **(i)** the class is
  **operable** per the criterion below, **AND (ii)** its clearance control is
  **ENCODED IN A LANDED, ACTIVE RULE** in the rule directory the decision core
  executes **at the commit `contracts/review-lane-pin.yaml`'s `core_commit`
  names**. **Declaration in a council record alone is insufficient**, and a rule
  that is present but `state: defined_not_wired`, or `active: false`, does
  **not** satisfy (ii) — a control that is recorded but not deployed is not a
  control.
  > **Why (ii) is separate from (i), and not pedantry.** A council record can be
  > ratified before its executable rule lands: `add-substantive-review-lane`
  > separates the executable `gate-rules.yaml` change (**task 3.1**) from the
  > council record (**task 3.2**) as distinct tasks, so the gap between them is
  > a real interval and not a hypothetical one. During it, a record could
  > *declare* a class human-only while the core enforces nothing — and per
  > `011`'s R4 an envelope entry alone can reach the active autonomous chain.
  > `specs/011-council-feature-clearance/tasks.md:38-42` already draws exactly
  > this line for its own entries: no live entry lands until the successor has
  > **LANDED** *and* its protections are **ACTIVE** — *"structurally excluded
  > from the autonomy branch, not merely intended to be."* Condition (ii) holds
  > this feature to that same standard.

  **OPERABLE, defined — this requirement's own criterion, dependent on no other
  document.** A candidate class is **operable for this repository** if and only
  if the set of paths it admits — its bound `path_allowlist`, evaluated against
  this repository's actual tree — is **NOT wholly contained** in that class's
  effective gate-integrity floor (the canonical `GATE_INTEGRITY_FLOOR` plus any
  widening the class itself declares). Equivalently, and this is the testable
  form: **at least one admissible candidate can reach classification instead of
  parking `parked_never_clearable`.**

  **The class's clearability tier is NOT part of this criterion.** A convenable
  class clears this gate **whatever its tier — advisory and human-only
  included** — because whatever an envelope may then DO is bounded by that
  class's **deployed clearance control**: the `clearance_rule` and
  classification intent as carried by the **landed, active rule the decision core
  reads from the base branch** at the pinned `core_commit`. **The council record
  authorizes that control; it is not itself what the core executes** — which is
  why discharge condition (ii) above names the rule and not the record. It is
  **never** bounded by anything the envelope itself carries. The
  envelope schema is `additionalProperties: false` and has no
  classification-intent field, so posture cannot be expressed there at all;
  posture lives class-side, in tier-2 state (`011-council-feature-clearance`
  `research.md` R2).

  **Guard, and it is not optional.** An envelope entry for a class whose posture
  is **not** so encoded class-side **remains prohibited by this requirement**.
  `011`'s `research.md` R4 states the reason: with tier-2 ACTIVE, a live envelope
  entry is *"not merely 'advisory recording'"* — if its facts ever prove
  clearable, *"the merge-master App could autonomously approve human feature
  code."* An entry alone can therefore reach the active autonomous chain with no
  posture encoded anywhere. What this requirement refuses is an envelope for a
  class that **can never convene at all**, and — by this guard — an envelope for
  any class that does not satisfy **BOTH** discharge conjuncts above: **operable**
  (i), **AND** its clearance control carried by a **LANDED, ACTIVE rule at the
  pinned `core_commit`** (ii). **A governed record declaring the posture does not
  satisfy (ii)** — the record authorizes the control, the rule is the control —
  so an envelope is refused throughout the record-landed-but-rule-not-yet-active
  interval.

  **Vocabulary bridge.** The ratified texts' terms — `human-only`, `clearable` —
  describe what a verdict may DO. **Operability describes whether any verdict
  can be PRODUCED**, which is the third property the 2026-08-28 record
  established the vocabulary lacked (lead-architect's *"unconvenable"* finding:
  *"a third thing the text has no word for and did not anticipate"*).

  **Machine check, stated honestly.** The same 2026-08-28 ruling adopted a
  definition-time predicate for exactly this property (gate-rules ballot **S-1**,
  from LQ-A2 / LS-A5 / LA-A4). **Its realization is in flight in codexFactory and
  is NOT on `main` today, so no function name is cited here as if it existed.**
  Once it lands, that predicate's verdict IS the operability test for this
  requirement; until then, the substantive definition above governs on its own.
  > **HISTORY, 2026-08-28.** A `gate_rules_council` record for this repository
  > now exists, and it **REFUSED** the class proposed to it:
  > `opensoft/codexFactory` →
  > `hermes/domain/review-councils/records/2026-08-28-gate-rules-openxfactory-substantive-classes.md`
  > (convener disposition §8; seat returns in the sibling
  > `2026-08-28-seat-returns/`).
  >
  > The council refused `openxfactory-proposal-review-advisory` over
  > `openspec/changes/**` **UNANIMOUSLY, 5/5**, on the ground that it can never
  > CONVENE: its admitted surface lies **wholly inside the canonical
  > `GATE_INTEGRITY_FLOOR`**, which is evaluated before any clearable
  > classification, so every candidate parks `parked_never_clearable` and the
  > convening lane bails on that outcome. Measured: **984 admitted paths, 984
  > floored, 0 remaining.** Proven code-level — removing the rule's
  > `gate_integrity` block, or supplying no rule document at all, parks
  > identically. **A class that can never convene is not an operable class**, so
  > that record defines none and the requirement above is unaffected by it.
  >
  > **`add-substantive-review-lane` task 3.2 therefore remains OPEN** (Brett
  > Heap, 2026-08-28: *"1a, 2 leave open, 3 adopt, 4 adopt all three"*).
  >
  > The ruled continuation is the **council-reviewed-but-human-approved path**,
  > which per the 2026-08-26 record §7.4 *"needs no class and no flip"* — so it
  > reaches this repository without an envelope and without amending FR-008.
- **FR-009**: The caller MUST gather the changed-path set PROVABLY COMPLETE — an
  authoritative declared total from the pull-request resource, a paginated
  listing whose entry count is compared against it, and a head-SHA recheck after
  pagination — and MUST park with a named reason rather than evaluate an
  unproven set.
- **FR-010**: When a required credential or the pinned core is unavailable, the
  run MUST conclude FAILURE with a message naming what is missing. It MUST NOT
  conclude success.
- **FR-011**: The caller MUST run as a single job, so the check-run name is
  exactly the job id. A second job in the same workflow would produce a
  check-run name that codexFactory's envelope self-exclusion does not match.
- **FR-012**: No ruleset, branch protection, or required-check configuration is
  changed by this feature.
- **FR-013**: The pin artifact MUST be routed to a human code owner, on the same
  ground as `contracts/openxwallet-pin.yaml`: a pull request that changes it
  changes the code a governance surface executes.
- **FR-014**: The pin's commit-shaped value MUST be a declared member of this
  repository's derivation-pin class, declared `CROSS_REPOSITORY`, so it is not
  reported as an unreachable orphan and so the key name is taught to the sweep
  vocabulary.

### What this feature explicitly does NOT do

Recorded as requirements-in-the-negative because each is a thing a reader will
otherwise assume landed.

- **NR-001**: **No wallet-bound exercise record.** A council seat casting a
  review here produces no wallet-signed exercise. That is S3 of
  `add-wallet-carried-review-authority` — the seat's wallet key minted inside
  the deliberation job and the signature verified at `check_verdict`. Until S3
  lands, an act of this kind records as `event_class: unauthenticated_request`
  and `unattributed`, and `openxwallet/spec.md` rules that such an act "is not
  assigned to a holder". This caller therefore claims no exercise of the
  `act`-tier review authority that `governance/review-authority/register.yaml`
  row `row-mrc-0001` records over `opensoft/openxFactory`.
- **NR-002**: **No revocation check.** S5's revocation-at-verdict-consumption,
  declared staleness bound, and unreadable-register-refuses rule are not
  implemented. The register is an issuance-time snapshot by its own header's
  admission.
- **NR-003**: **No ruleset change, and therefore no gate.** The human review gate
  on openxFactory is untouched. This check satisfies nothing and blocks nothing.
- **NR-004**: **No approval, autonomous or otherwise.** No candidate class, no
  tier-2 gate rule, no council convening, no verdict transport, no audit
  artifact, no approving review.
- **NR-005**: **No tier-1 envelope evaluation, and no envelope instance.** The envelope requires a
  non-empty `candidates` list (schema `minItems: 1`, and the runtime mirror
  refuses an empty one), and openxFactory has no council-defined OPERABLE
  candidate class to put in it. **What would permit an envelope is FR-008's
  two-conjunct discharge, not operability alone — see its definition, which
  governs.** Shipping a placeholder candidate would be inventing
  enrollment.
- **NR-006**: **`contracts/review-lane-pin.yaml` is not added to the openxFactory
  repository gate floor BY THIS FEATURE.** It arguably belongs there — it
  determines which core judges this repository — but that floor file lives in
  codexFactory. Named as a follow-up (6.2), not performed here.
  > **The follow-up has since been COMPLETED SEPARATELY, 2026-08-28.** This
  > non-requirement is unchanged in scope — it bounds what *this feature* does,
  > and this feature still does not touch that file. What has changed is the
  > world outside it: codexFactory PR **#125** *"Add the openxFactory review-lane
  > pin to the never-clearable floor"* **merged** (`99fa3ffe`, reachable from
  > `origin/main`), so `contracts/review-lane-pin.yaml` **IS** now in
  > `scripts/merge_master/openxfactory-review-authority-floor.yaml`'s
  > `never_clearable_paths`, pinned by per-path behavioural tests in
  > `tests/merge-master/test_repository_gate_floor.py`. **Task 6.2 is ticked.**
  > Read NR-006 as *"not by this feature"*, never as *"not done"*.
  >
  > **AND NOT YET AS "protected here".** That entry is live **upstream** and
  > **inert in this repository**: the caller and the pin both still name
  > `core_commit: 58bd3cf7…`, which predates it — verified, `99fa3ffe` is not an
  > ancestor of `58bd3cf7` and the floor file at the pinned commit contains zero
  > occurrences of `review-lane-pin.yaml`. **A pull request touching the pin
  > receives a zero-match advisory verdict today.** It becomes live when the
  > re-point ceremony of follow-up **6.5** advances the pinned commit, which is
  > deliberately held until codexFactory #126 and #127 land so one ceremony
  > converges all three. See tasks 6.2 (ii)–(iii).
- **NR-007**: **`add-substantive-review-lane` task 5.1 is not ticked.** Its
  ruleset half remains owed, so the task stays open and this feature is recorded
  against it rather than closing it.

### Key Entities

- **Pinned workflow pin** (`contracts/review-lane-pin.yaml`): the recorded claim
  "openxFactory's review lane is judged by THIS codexFactory commit". Carries
  the pinned repository, the commit, the declaration date, and the workflow path
  the pin governs. Not a published contract, so — following
  `contracts/openxwallet-pin.yaml` — it takes no `contracts/manifest.yaml` row.
- **Repository gate floor** (`opensoft/codexFactory`
  `scripts/merge_master/openxfactory-review-authority-floor.yaml`): the
  never-clearable path set for `opensoft/openxFactory`. Owned by codexFactory,
  read here, never authored here.
- **Advisory verdict**: the rendered outcome of the run — which floored paths the
  candidate touches, or a named park reason. Carries no authority.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On every pull request opened against the default branch, a check
  named exactly `merge-master-approval` appears, and its message states in one
  line whether the pull request touches a never-clearable path.
- **SC-002**: The number of ways the pinned core commit can change without a
  reviewer seeing it is ZERO: the pin file is code-owner-routed and a test fails
  on disagreement.
- **SC-003**: The number of approving reviews, merge calls, or auto-merge
  enablements attributable to this feature is ZERO, verifiable by the absence of
  the steps that would perform them.
- **SC-004**: The number of ruleset or branch-protection changes made by this
  feature is ZERO.
- **SC-005**: A run that could not read the decision core concludes FAILURE 100%
  of the time; there is no input under which it concludes success without having
  evaluated the floor.
- **SC-006**: The repository's pytest suite adds no skipped test, so the CI
  gate's exact skip count is unchanged.

## Assumptions

- **The check may run red on landing, and that is correct.** openxFactory is not
  in the selected-repository list for the org secrets that grant read access to
  the private decision core. Story 3 is therefore the live behaviour until an
  operator grants them. Because no ruleset requires this check, a red advisory
  check blocks nobody — and per SC-005 a red check that names its reason is the
  designed outcome, not a defect.
- **`pull_request_target` is the right trigger even though it means this feature
  cannot demonstrate itself on its own pull request.** The trigger runs the
  workflow definition from the base branch, so a workflow absent from the base
  branch does not run. Choosing `pull_request` instead would run this file from
  the pull-request head WITH the secret that reads a private repository, which is
  the exfiltration shape the base-branch rule exists to prevent. The
  demonstration cost is accepted; the first live report is the next pull request
  after this one lands.
- **The pinned commit is codexFactory `origin/main` at declaration time, not
  xFactory's migration pin.** xFactory's two merge-master surfaces pin
  `3c35ca8b` (2026-08-21) in lockstep. That commit predates both
  `scripts/merge_master/repository_floor.py` and
  `scripts/merge_master/openxfactory-review-authority-floor.yaml`, so it cannot
  evaluate the only thing this caller judges. A newer pin is forced by the
  feature, not chosen for freshness; the divergence and the lockstep obligation
  are recorded in the pin file and in the workflow header.
- **PyYAML and a POSIX `bash` are available to the test.** Both are already
  relied on by the repository's existing suite and CI image.
- **The floor's reachability check is opt-in and this caller opts in.** The core
  will only verify that floored paths exist in the tree when a caller supplies
  the tree listing; supplying it converts "a floor that matches nothing" from
  silence into a named failure.

## Clarifications

### Session 2026-08-27 — no questions asked, and why

The clarify round ran and produced ZERO questions. That is a finding, not a
skipped step, so it is recorded with the sources that closed each candidate
question rather than left as silence.

- **Does openxFactory enroll a candidate class?** No — closed by
  `add-substantive-review-lane` task 3.2 (the `gate_rules_council` record that
  defines openxFactory's candidate classes is owed and absent) and by the
  codexFactory envelope schema, where `candidates` is required with
  `minItems: 1`. There is no legal "empty enrollment", so the only honest option
  is no envelope at all. Encoded as FR-008 and NR-005.
  > **The clause above is what was true on 2026-08-27 and is kept as the
  > decision-log entry it is. It is NOT current fact.** As of 2026-08-28 a
  > `gate_rules_council` record exists and **refused** the one class put to it
  > (FR-008's history note has the detail). **The answer is unchanged and the
  > settled premise is FR-008's: what is absent is a council-defined OPERABLE
  > candidate class, never the record.** A class that can never convene is not an
  > operable class, so the refusal defines none. Task 3.2 stays OPEN.
- **Fixed head ref or a pattern?** Moot, since nothing is enrolled — but had it
  mattered: Brett ruled 2026-08-25 (recorded in `add-substantive-review-lane`
  task 4.4) that first-tranche classes are fixed-branch BY RULING on
  anti-spoofing grounds, not by mechanical limit. `head_ref_pattern` ships and
  works; it is simply not permitted for a first class.
- **Advisory or binding?** Advisory — closed by
  `add-wallet-carried-review-authority` S1's verbatim adversary rule ("an intake
  entry with no reader confers nothing"), plus S3 and S5 being unlanded.
  Encoded as NR-001..NR-004.
- **Which commit does the caller pin?** Forced, not chosen: xFactory's
  `3c35ca8b` predates the only module and the only data file this caller reads.
  Recorded under Assumptions.
- **Does the pin need a `contracts/manifest.yaml` row?** No — closed by the
  `contracts/openxwallet-pin.yaml` precedent, which was deliberately REMOVED
  from that manifest at `contract-v2.0` because a pin is not a published
  contract. It does need a derivation-pin-class member (FR-014).
