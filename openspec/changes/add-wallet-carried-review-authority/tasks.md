# Tasks: add-wallet-carried-review-authority

Dependency-ordered. **Only §1 is this change's own work**; §2–§7 are the named
successors S1–S5 plus the bench items, listed here so the build order is one
document rather than five, and so nothing named in the proposal loses its home.
Each successor carries its OWN `code_surface` and archives on merged, green
realization evidence per `release-realization` — do not tick a successor's boxes
from this change.

**Repository tags.** Untagged = openxFactory. `[hermes-install]` =
`opensoft/xFactory-Hermes-Install` and its own OpenSpec instance.
`[codexFactory]` = `opensoft/codexFactory`. `[OPERATOR]` = only Brett can
perform it (a GitHub setting, a key, a ratification). `[GOVERNANCE]` = it needs a
ruling or an OpenSpec change before the work is legal.

**One standing constraint on every runtime task.** codexFactory `3143f34`
(`records/2026-08-23-reseed-deploy-ordering-addendum.md`): **no reseed until a
hermes-install image at `3de0519`+ is deployed.** Anything below that exercises
materialized `review_council` content in the live stack is gated on that image
shipping.

---

## 1. This change: doctrine, deltas, bookkeeping

- [x] 1.1 Restructure `proposal.md` on the convener's 2026-08-23 ruling —
      PART I doctrine, PART II substrate (S1–S5 with honest current state),
      PART III the declined floor. Answer Q1–Q7 and stop posing them; raise Q8
      (composition drift), Q9 (the floor's source-of-truth inversion) and Q10
      (the `isolated_per_use_authorized` authorizer). Write
      "The first bypass this ends: NONE, directly" into ## Why and delete every
      sentence that sells more.
- [x] 1.2 `specs/review-authority-intake/spec.md` — **12 ADDED requirements**:
      authority held as a grant and by nothing else; a grant with no reader in a
      required check confers nothing; register-and-reader ratified together with
      the MVP shape; the register as a permanently human-only surface; the
      issuer anchor and the root-grant class; the `act_unsupervised` refusal;
      the unattested-custody cap at `request`; never both the review and the
      approval act over one object; the exercise at verdict conformance (exit B
      rejected); revocation re-checked at verdict consumption with a staleness
      bound and unreadable⇒refuse; composition pinning and governed
      re-issuance; the refusal's input derived, never reported.
- [x] 1.3 `specs/roles-authority-model/spec.md` — **2 ADDED** (spec authority and
      code authority as named held delegable roles; the general refusal-only
      non-self-review rule) **and 1 MODIFIED** ("Pilot repository and reviewing
      domain", gaining its authority counterpart). Declared RELATIVE TO
      `add-substantive-review-lane`'s outcome per `release-realization:64-74`,
      referencing that change AND restating the target requirement's full text
      as that change's delta will promote it (design D9).
- [x] 1.4 `design.md` — Context, Goals/Non-goals, 11 Decisions with their
      rejected alternatives (topology, `consent-instrument`, the inherited
      ceiling, exits A and B, the file-based revocation options, repairing the
      narrowed floor), 6 Risks (the `--admin` composition loop, the day-one
      empty world, the vacuous-pass class, the refusal that cannot see the
      attack, register drift, sequencing), the S1–S5 build plan with gates, and
      the reduced open-question set.
- [x] 1.5 `clarifications.md` — the 15 NOTED-class constraints: the scale
      question answered by the absent store, the CI/tooling facts for S1
      (openxFactory has no pull-request-triggered workflow at all; PyYAML is a
      hard dependency; a path-less invocation self-tests and passes vacuously;
      "required" is a ruleset setting, not a tree fact), `repo_scan`'s
      closed-over-itself context, the stale `state` field, and the rest.
- [x] 1.6 `OPENSPEC_TELEMETRY=0 openspec validate
      add-wallet-carried-review-authority --strict` green, and
      `--all --strict` green.
- [x] 1.7 List the change in `README.md`'s `## OpenSpec Records` →
      `Active changes:` block (Architect F20).
- [x] 1.8 **[OPERATOR] [GOVERNANCE]** Ratify or return the proposal. Nothing in
      §2 onward is authorized work until this is discharged.
  - RATIFIED 2026-08-23 by Brett Heap (openxFactory operator authority),
    in-session — `proposal.md` header and the ratification record at
    `proposal.md:13` ("Ratified as restructured", PART I/II/III).
- [ ] 1.9 Before archive: re-check §1.3's restated requirement text against
      `add-substantive-review-lane`'s FINAL promoted text (design risk R6).

## 2. S1 — the reader: wire the validator into CI as a required check

*No grant is operative until this lands. It precedes everything.*

- [x] 2.1 Author a `pull_request`-triggered workflow running
      `python3 openXwallet/scripts/validate-openxwallet.py <checkout> --strict`
      (the path as of `contract-v2.0`: the reader is the PINNED one, consumed
      through `contracts/openxwallet-pin.yaml`; it read
      `scripts/validate-openxwallet.py` when this task was authored).
      **This is openxFactory's FIRST pull-request-triggered workflow** — both
      existing workflows are `workflow_call` / `workflow_dispatch` — so it needs
      its own trigger, permissions and concurrency design (clarifications N3).
  - Realized as `.github/workflows/wallet-validation.yml` (feature
    010-wallet-validator-ci T002), which is
    `.github/workflows/openxwallet-consumer-gate.yml` from `contract-v2.0`
    forward — the FILE was renamed by `split-openxwallet-repo` P3 and the JOB ID
    the ruleset pins was deliberately retained, so this task's realization is
    unaffected: `on: pull_request` targeting `main`, single
    unnamed job so the status check surfaces as exactly `wallet-validation`,
    `permissions: contents: read`. As amended by review rounds the invocation
    omits `--strict`; that deviation is the RECORDED decision, see task 2.4.
- [x] 2.2 Follow the house Python pattern: `actions/setup-python@v5` pinned to
      `3.12` plus `pip install pyyaml`; PyYAML is a hard dependency and the
      validator exits 2 without it (N4).
  - Workflow pins `actions/setup-python@v5` to Python `3.12` and installs
    `pyyaml jsonschema rfc3339-validator` per the review-round amendment
    (feature 010 T002).
- [x] 2.3 Pass the checkout path explicitly. A path-less invocation self-tests
      only and passes green while scanning nothing — the vacuous-pass trap this
      whole change exists to name (N5).
  - Both steps pass the checkout explicitly
    (`openXwallet/scripts/wallet-yaml-syntax-gate.py .`,
    `openXwallet/scripts/validate-openxwallet.py .` since `contract-v2.0`;
    `wallet-yaml-syntax-gate.py .` and `validate-openxwallet.py .` before it);
    observed live on every PR since landing
    (green `wallet-validation` runs on #363/#366/#369). The explicit `.` is now
    additionally pinned by
    `tests/openxwallet_consumer_gate/test_gate_invocation.py` under the REQUIRED
    `pytest-suite`, so the vacuous-pass trap this task names cannot be reopened
    by an edit to the workflow alone.
- [x] 2.4 Decide and record whether the gate runs `--strict`; the doc-health
      precedent parameterizes `fail-on` rather than hard-coding it (N5).
  - DECIDED: no `--strict`. Recorded in feature 010 T002 ("No scoping logic,
    no `--strict` (R2/R4/R5; R5 partly superseded — see its header note)",
    `specs/010-wallet-validator-ci/tasks.md`).
- [x] 2.5 **[OPERATOR]** Make the check REQUIRED in the branch ruleset. This is a
      repository setting, not a tree fact — a merged workflow file is not
      evidence (N6).
  - DONE 2026-08-26 on operator delegation: org ruleset **21538893**
    "openxFactory wallet-gate (require wallet-validation)" targets this
    repository's default branch with enforcement ACTIVE and requires status
    check `wallet-validation`; strict policy OFF per task 2.4's recorded
    decision; OrganizationAdmin bypass always (house pattern, matching the
    Tier-1 ruleset's shape). Verified live:
    `GET repos/opensoft/openxFactory/rules/branches/main` returns
    `required_status_checks → [wallet-validation]` sourced from ruleset
    21538893. The org-scoped form was used because the repo-level ruleset
    endpoints were unavailable to the acting token; scoping confines the
    requirement to openxFactory alone.
- [x] 2.6 **Gate:** a deliberately malformed grant fails the pull request, and
      the realization evidence includes the ruleset state showing the check
      required (not just the workflow file).
  - PROVED 2026-08-26 on draft canary PR #387 at commit `423b8f92`: removing
    only `issued_by` from the live production-scanned
    `governance/review-authority/grants/grant-mrc-0001.yaml` passed the YAML
    syntax gate, then required check `wallet-validation` failed in run
    **32997867639**, job/check **98271703098**. `validate-openxwallet.py .`
    emitted exactly one `issuer-unrecorded` error (`records no issued_by`),
    zero warnings, and exited 1.
  - GitHub reported the PR `BLOCKED`; live
    `GET repos/opensoft/openxFactory/rules/branches/main` independently returned
    required context `wallet-validation`, sourced from active org ruleset
    **21538893** with strict policy OFF. PR #387 was closed unmerged, its canary
    branch was deleted, and `origin/main` retained the valid `issued_by` field.

## 3. S2 — the issuer anchor

*Precedes the first wallet: an unanchored root grant is an unbounded one.*

- [x] 3.1 Implement `issued_by` as REQUIRED **for review-authority grants** — a
      scope restriction by the consuming capability, not a schema change. The
      field already exists and stays optional in the shared grant schema, so no
      `contracts/` edit, no manifest entry, no CHANGELOG line, no bundle cut.
  - Validator rule (t) requires a REVIEW-class grant to name `issued_by`
    (`openXwallet/scripts/validate-openxwallet.py` since `contract-v2.0`,
    `scripts/validate-openxwallet.py` before it); shared schema untouched. Feature
    012-wallet-issuer-anchor tasks all complete (11/11).
- [x] 3.2 Implement the ROOT-GRANT class: a grant with no `parent_grant_ref` is a
      root, and its issuer's authority is recorded OUTSIDE the register it
      writes into.
  - Root class implemented in rule (t); the live first root
    `grants/grant-mrc-0001.yaml` carries no `parent_grant_ref` and roots in
    the anchored operator (feature 012/014 records).
- [x] 3.3 Record the root-issuer anchor: the responsible operator, standing under
      the Human Escalation Contract (`docs/roles-and-authority.md:103-140`,
      whose parked-decision list names "privileged capability grants"). No
      wallet, no grant.
  - Anchor recorded in validator rule (t) citing the Human Escalation
    Contract; machine-named issuers refused with their own wording; legacy org
    strings do not grandfather (feature 012-wallet-issuer-anchor, 11/11).
- [x] 3.4 **Gate:** the validator refuses a review-authority grant with no
      `issued_by`, and refuses a root grant naming an agent holder as issuer.
  - Refusal probes pinned by feature 012's red/green evidence and exercised by
    the wallet-validation suite; pytest-suite green on every recent PR run
    (#366/#369).

## 4. The first wallet

*Cold start. One holder, not eight.*

- [x] 4.1 **[OPERATOR]** Mint one wallet for codexFactory's
      `merge_readiness_council` as a body, custody model `holder_readable` —
      the only realistic model with no key infrastructure in the stack, and the
      tier the registry designed for exactly this situation (N13).
  - Wallet minted in-tree:
    `governance/review-authority/wallets/wal-agent-mrc-0001.yaml`, holder
    `agent:merge-readiness-council`, custody model `holder_readable`
    (feature 013-first-wallet, 7/7).
- [x] 4.2 Write the wallet record IN THE SAME TREE as the register: `repo_scan`
      builds its context from the scanned repository's own records, and a
      cross-repository audience wallet has no resolution path today (N7).
  - Same tree confirmed: `governance/review-authority/wallets/` beside
    `register.yaml` / `grants/` / `attestations/` (landed #341).
- [x] 4.3 Record the custody ATTESTATION row — who verified the isolation,
      against what, when. Without it the intake caps grants to that wallet at
      `request`.
  - Attestation recorded:
    `governance/review-authority/attestations/custody-attest-wal-agent-mrc-0001.yaml`,
    referenced by the act-tier register row (feature 013/014 records).
- [x] 4.4 **[codexFactory]** Declare the holder's composition: map the six
      declared components (model version, prompt contract, tool manifest,
      policy version, parameters, retrieval corpus) onto the actual seat
      artifacts under `hermes/domain/review-councils/` and
      `hermes/domain/agent-mixes.yaml`. **No such mapping exists today** and
      S5's pinning rule is unimplementable without it (N10). The retrieval
      corpus is the PINNED seat prompt plus ontology package — never the
      candidate repository at HEAD.
  - Realized by codexFactory PR #115, merged at `4d62e94` on
    2026-08-27T03:05:48Z: the merge-readiness council now declares the exact
    six-component `composition_source_map`, and its council profile binds all
    four seats to the existing workflow, prompt, schema, authority, and
    retrieval sources. Parity and mutation guards refuse drift, including
    retrieval from candidate HEAD.

## 5. S4 — the register and its reader, in ONE change

*Cannot precede S1, by the capability's own ratification condition.*

- [x] 5.1 Create the register at a fixed path in openxFactory (canonical home:
      `canonical-policy-migration:33-38`, `repo-boundary-governance:8-13`), at
      the MVP shape: one holder, one target repository, one act, tier `act`, one
      `expires_at`, one row.
  - Realized by xFactory#341 (merged `410fa18`, 2026-08-25T16:14:41Z):
    `governance/review-authority/register.yaml` carries exactly ONE row
    (`row-mrc-0001`) — one holder (`agent:merge-readiness-council`), one
    target repository (`opensoft/openxFactory`), one act (`review`), tier
    `act`, one `expires_at` (2026-11-23T12:00:00Z).
- [x] 5.2 Author its reader IN THE SAME CHANGE. Its only obligation at this
      shape: fail a convening that admits a holder with no active row.
  - Same change (#341): validator rule (u) + `check_register` /
    `_load_attestations` wired into `repo_scan` inside the REQUIRED
    wallet-validation check
    (`openXwallet/scripts/validate-openxwallet.py` since `contract-v2.0`,
    `scripts/validate-openxwallet.py` before it). An active
    REVIEW-class grant with no backing active row is refused; the
    production-wiring mutation probe fired `register-no-active-row` and was
    refused, restored immediately (feature 014 T003, T007x).
- [x] 5.3 The reader COMPUTES expiry from `expires_at` and treats a stale
      `state` field as a finding rather than as truth — nothing in the family
      recomputes `state` (N8).
  - Rows and grants are judged expired by COMPUTED time from `expires_at`;
    the stored `state` field is never truth about expiry; the stale-state
    finding is implemented and pinned by the computed-expiry probes
    (feature 014 T003/T004; validator rule (u)).
- [x] 5.4 **[codexFactory]** Enter the register's path BY NAME as a
      never-clearable floor member in the gate rules. Do not rely on inference
      from the floor's four path clauses: a grant register is authority policy
      but is not literally contract bytes, gate/workflow definitions, credential
      surfaces or security posture, and openxFactory is the lane's PILOT
      repository — without this, councils clear their own commissions.
  - Realized as the codexFactory successor change `protect-review-authority-register`
    (Speckit feature 012): a new exact, repository-scoped, never-clearable
    `repository_gate_floor` kind names `governance/review-authority/register.yaml`
    for `opensoft/openxFactory`, loaded from the same base-branch governance
    inputs as the gate rules and applied to matched candidates before every
    tier-1 approval, already-approved result, or council exit — no candidate
    enrolment, no inference from floor path clauses. Production floor document:
    codexFactory `scripts/merge_master/openxfactory-review-authority-floor.yaml`.
    Realization: codexFactory PR #91 merged at `da6795b` (2026-08-25T19:40:27Z,
    green merge-master-approval/validate/Sonar), archive + promotion PR #92
    merged at `8dcd5bc`; canonical spec `codexFactory
    openspec/specs/repository-gate-floor/spec.md`.
- [x] 5.5 Record the Q1c design constraint IN the register's own documentation:
      a file-based register cannot satisfy revocation-at-exercise, and the
      conforming home for the REVOCATION SURFACE is a live lookup on the Hermes
      runtime. The file is right for one row; it is not pretended to be a
      revocation surface.
  - Recorded verbatim in `register.yaml`'s header (Q1c DESIGN CONSTRAINT
    block): the file is an issuance-time snapshot; the conforming REVOCATION
    SURFACE is a live lookup on the Hermes runtime (S5 successor); it must
    not be pretended into a revocation surface.
- [x] 5.6 **Gate:** a convening admitting a holder with no active row fails the
      required check.
  - Gate evidence ACCEPTED by the operator (Brett) on 2026-08-26: feature
    014's T007x live mutation probe emptied the register in the production
    tree and the REQUIRED wallet-validation check refused with
    `register-no-active-row`, restored immediately (nothing red was ever
    committed). The probe exercises exactly the required check a convening's
    holder admission rides, so an admission with no active row fails it by
    construction. Evidence: `specs/014-register-and-reader/tasks.md` T007x,
    `implementation-notes.md`. This acceptance closes S4.

## 6. S3 — the exercise, at verdict conformance

*`[hermes-install]` throughout: openxFactory cannot author a delta into another
repository's spec corpus, and refusal vocabulary is ratified as the consumer's
(`hermes-domain-overlay:254-264`).*

- [x] 6.1 **[hermes-install] [GOVERNANCE]** Open a successor change against
      `council-orchestration`. **No amendment to the advisory-only requirement**
      — the work rides the SECOND requirement, "A convening verdict conforms to
      the council's materialized semantics or is refused", because a missing or
      unverifiable seat signature is a conformance defect of the same kind as a
      wrong pin or a missing seat result.
  - Opened and ratified by xFactory-Hermes-Install PR #46, merged at
    `401da4f` on 2026-08-27T04:16:31Z: successor
    `add-wallet-exercise-verdict-conformance` modifies only the second
    requirement, makes missing, unauthorized, replayed, or unverifiable
    required-seat signatures fail closed, and requires atomic exercise
    evidence while preserving the separate advisory-only requirement. Tasks
    6.2-6.8 remain explicit unchecked realization work.
- [ ] 6.2 **[codexFactory]** Mint the seat's wallet key INSIDE the deliberation
      job.
- [ ] 6.3 **[hermes-install]** Verify the signature over the seat return at
      `check_verdict` and write the exercise record there.
- [ ] 6.4 **[hermes-install]** Decide where exercise records are STORED —
      runtime Postgres (queryable, satisfies the distinct-holder store need, but
      outside the governed git corpus) or a git artifact (auditable but not
      queryable, and subject to the pinning lag that disqualifies a file-based
      revocation surface). Undecided here (N9).
- [ ] 6.5 **[hermes-install]** Implement the derived candidate-side input for the
      non-self-review refusal: compute the touched-object set from the subject
      pin under the runtime's OWN credential; unavailable, self-reported or
      unverifiable ⇒ REFUSE. Costs named: a per-target repository credential
      held by Hermes, cluster egress, a per-target machinery map.
- [ ] 6.6 If the derived input needs a field on the posted convening block, that
      is a `neutral-job-envelope` delta in **openxFactory** — a declared
      successor, not declared now.
- [ ] 6.7 **Gate:** a seat return with no verifiable signature is refused
      fail-closed; a conforming one writes an exercise record. Only then does
      `distinct_holder_constraint_refs` become the observable that supersedes
      QA 4.2, since its comparison basis is the prior act's RECORDED holder.
- [ ] 6.8 State in the realization record that the refusal's reachable subject is
      MATERIALIZED DOMAIN CONTENT ONLY, that it would not have caught the
      executed `scripts/yaml.py` attack, and that it is ADDITIVE to
      codexFactory's `"scripts/**"` floor entry, CODEOWNERS line and import-root
      test — which are not retired.

## 7. S5 — revocation, lifecycle, blast radius

**S5's build, 2026-08-27/28. Four pull requests, NONE MERGED, none tickable.**
`[hermes-install]` #50 (the OpenSpec change `add-wallet-revocation-lifecycle`,
`Status: draft`) and #51 (Speckit feature `016-wallet-revocation-lifecycle`, the
code, held on #50's ratification); `[codexFactory]` #123 (7.5's prompt-corpus
pin); and this branch (7.3's declaration + this ledger). Every box below stays
UNCHECKED on purpose: this change's own rule is that a successor archives on
MERGED, green realization evidence, and ticking on an open pull request is the
described-control-treated-as-an-existing-one shape (design R3) performed by the
change that names it.

**The honest headline, because an over-claim here would be worth less than a
gap:** S3 had already discharged more of §7 than §7 assumed, and had left
exactly the parts it said it was leaving. 7.1's property was structurally true
the day S3 landed and was merely UNPINNED; 7.2 already refused and merely
refused ANONYMOUSLY; 7.4 was half-built on a wrong diagnosis; 7.3 was
unimplementable, and `projection.py`'s property 5 said so in as many words.

- [ ] 7.1 **[hermes-install]** Re-check revocation at VERDICT CONSUMPTION, not
      from the admission stamp. `verdict_for_completion` takes the roster and
      content provenance from the `convening` stamp written at admission, which
      is exactly the issuance-time trust `openxwallet:127-131` forbids.
  - **PINNED, not built** (hermes-install #51). This task's premise was half
    wrong and the half that was right is worth keeping. AUTHORITY never came
    from the admission stamp: S3's `DatabaseSeatExerciseGate._load` already
    calls `resolve_seat_authority(..., now=occurred_at)` once per required seat
    inside `check_verdict`, and the reader deliberately does not cache. What did
    not exist was a test that would FAIL if someone later resolved authority
    once at admission and stamped it into the envelope — so the property was
    true and unguarded. `test_a_revocation_after_admission_refuses_the_completion`
    is now that guard.
  - What the task's premise got RIGHT and this feature did NOT close: the
    ROSTER, the subject pin and the council-content provenance are all still
    taken from the admission stamp, and `domain_council_content` is re-read only
    when that stamp is empty. The roster being issuance-time is correct — a
    convening is over the roster it was convened with. Whether the CONTENT
    PROVENANCE should also be re-derived at consumption is named as an open
    ruling in #51's realization record and is NOT answered there.
- [ ] 7.2 **[hermes-install]** On a revoked or expired holder, PARK with a NAMED
      REFUSAL — never silently honour the stamp.
  - **BUILT** (hermes-install #51), and it uncovered a real defect rather than a
    naming complaint. The refusal already existed and was already fail-closed
    before the first durable write, with the run left open. Two things were
    wrong. First, `GrantNotActiveError` carried ONE code
    (`review_authority.grant_not_active`) for revoked, expired and
    unrecognized-state alike, so a consumer could not tell an authority
    WITHDRAWN from one that RAN OUT — now three codes under the same base, so
    every existing `except` still catches. Second, and the substantive half:
    `api/routers/runs.py`'s `except ReviewAuthorityProjectionError` branch
    HARD-CODED `seat_id=None` into the audit event. A refusal on this path
    writes nothing durable, so that redacted event is the ONLY trace a convening
    was refused and why — and a revoked holder parked a convening with the seat
    named in prose and absent from every structured field. That is the "silent
    skip" this task forbids, in its real form. Fixed, and pinned over HTTP.
  - PARKING stays the CONSUMER's semantics, deliberately and with the rejected
    alternative recorded: there is no `parked` run status in the runtime
    (`JobsRepository.resolve()` takes only `completed`/`failed`), and the
    proposal's own §S5 text describes the park as codexFactory's downstream
    effect of `missing_required_seat: refused`. The runtime's obligation is a
    fail-closed refusal carrying a reason the consumer can park ON, which is
    what it now does.
- [ ] 7.3 Declare the register's staleness bound as a duration.
  - DECLARED in this branch: `governance/review-authority/register.yaml` gains
    the top-level `revocation_staleness_bound: P7D`, with the reasoning recorded
    beside it — the runtime does not read this file but an operator-established
    PROJECTION of it, so the bound is the maximum age of that projection at the
    instant an exercise is judged; the runtime holds a ceiling of its own and
    honours whichever is tighter, so this declaration can only ever NARROW the
    window a deploy allows. P7D is deliberately loose: nothing refreshes the
    projection automatically, and a bound tighter than the refresh cadence parks
    every convening — design R1/R5's `--admin` pressure. Tightening it is an
    edit to that one line, no code and no deploy; the target once refresh is
    automated is P1D or tighter.
  - NOT YET TICKED because the enforcement half is unmerged (see 7.4) and this
    declaration is itself unmerged. **A FINDING this task uncovered:** the
    pinned reader ACCEPTS the new key silently — `check_register` is strict on
    the row field set but reads only `register_version` and `rows` at the top
    level — so a governed declaration sits in a required check's blind spot,
    which is the vacuous-pass class (design R3). Extending the reader to
    validate the bound is recorded as a named successor on openXwallet PR #3,
    because the reader left this repository at the `split-openxwallet-repo`
    carve.
  - **THE FINDING'S BLIND SPOT IS CLOSED (2026-08-28), and STILL NOT TICKED.**
    openXwallet's `add-per-seat-register-entries` — ratified by Brett Heap
    2026-08-28 (openXwallet PR #4, `10cbdca`) and realized at `wallet-v1.2`
    (PR #5, `93b0a47`) — closes the reader's top level as an ENUMERATED set
    (`register_version`, `revocation_staleness_bound`, `rows`, `seat_keys`;
    anything else refused as `register-top-level-unknown`) and brings
    `revocation_staleness_bound` into the ENFORCED read set. So the vacuous-pass
    class this task uncovered is now structurally closed rather than fixed once:
    the NEXT governed declaration added to this file is refused as unknown
    instead of passing unread. That reader arrives here with THIS pull request
    (pin + gitlink → `wallet-v1.2`), which is what makes the bound actually
    adjudicated by the required `wallet-validation` check.
  - It stays UNTICKED because this task's OWN enforcement half is 7.4's
    (hermes-install: older-than-the-bound ⇒ REFUSE), and 7.4 is BUILT but not
    ticked. Closing a reader's blind spot is not the same as the runtime
    refusing a stale projection. Tick 7.3 when 7.4 ticks.
- [ ] 7.4 **[hermes-install]** Unreadable register ⇒ REFUSE. Unreachable,
      unparseable, or older than the bound all refuse; never proceed.
  - **BUILT** (hermes-install #51). Half of it existed — absent, unreadable,
    unparseable, wrong-kind and schema-invalid each already had their own named
    class. The missing half was a WRONG DIAGNOSIS, not a missing refusal: the
    reader decided absence with `Path.exists()`, which returns `False` for a
    permission error on a parent directory, so an UNREACHABLE store was reported
    as an ABSENT one. Nothing was ever wrongly admitted — both refuse — but an
    operator following that refusal would go and create a file that already
    existed, which is a repair that cannot work. `os.stat` now separates the two:
    `FileNotFoundError` is absent (the store answered), any other `OSError` is
    unreachable (the store could not be consulted, so the answer is unknown).
  - STALE did not exist at all and is now its own refusal
    (`review_authority.register_stale`), naming the projection's age and the
    effective bound. The enforcement half of 7.3 rides here: the projection
    schema gains `projected_at` and `staleness_bound` as REQUIRED fields, the
    document version goes 1 → 2 with v1 refused by its own named error, the
    runtime holds a ceiling, and the effective bound is `min(declared,
    ceiling)` — an artifact must never widen its own trust window. The version
    bump is safe because S3 is NOT deployed and no projection exists in
    production; that fact is recorded in #51 as the reason rather than assumed.
- [ ] 7.5 **[codexFactory]** Pin model version and prompt corpus as declared
      components; forbid the candidate repository at HEAD as retrieval corpus.
  - This task is THREE halves, not one, and they are in three different states.
  - **Retrieval corpus — ALREADY DISCHARGED** by the 4.4 work (codexFactory
    #115/#119). `agent-mixes.yaml` carries `candidate_repository_head:
    excluded`, the ontology is pinned by `package_digest`, and
    `test_review_holder_composition_mutations.py` refuses both a candidate-HEAD
    corpus and a candidate-branch source. Nothing was rebuilt here.
  - **Prompt corpus — BUILT**, codexFactory PR #123 (`61a6811`, OPEN, not
    merged; `validate` / `merge-master-approval` / Sonar all green). #115 left
    this as a source PATH with a re-render parity check and no content hash;
    it is now a true content pin. Determinism was PROVEN before pinning, not
    assumed: `seat_system_prompt` was shown to be a pure function of the seat
    across repeated calls, a fresh module load under mutated
    `GITHUB_REPOSITORY`/`GITHUB_SHA`/`PR_NUMBER`/`SEAT`/`MODEL` and a changed
    cwd, two materially different assembled candidates (one injection-shaped),
    and the production CLI's bytes versus the in-process render — byte-identical
    per seat every time. `rendered_set_digest:
    sha256:9e66f1ad83be6dd1e4920a199567b3dc76923077a6c5ed9cd1ba67a3fb1d0140`
    over `<seat>` NUL `<prompt>` NUL per seat in lexicographic seat order, with
    a `digest_basis` that makes it reproducible from the declaration alone.
    Ten tests in `tests/merge-master/test_review_holder_prompt_pin.py`, inside
    the REQUIRED gate's pytest path; a prompt edit, a shared-protocol edit, a
    dropped seat and a per-seat re-pin that forgets the set digest each trip it.
  - **Model version — BLOCKED, and `pin_status: required_by_s5` deliberately
    stays.** Flipping `opus`/`sonnet` to exact provider version ids is two
    decisions this lane does not hold: WHICH model represents a seat is a
    Gate-Rules Council matter (model-diverse roster ruled 2026-08-22;
    `council-deliberation-worker.yml:710-723` — "this lane will not choose
    one"), and WHICH provider version to stand behind is an operator choice.
    Whether a family pin with an attested resolved-version record is admissible
    at all is the question carried to the convener under 8.1. So 7.5 stays
    UNTICKED, and the flip is folded into 7.6's runbook walk rather than
    performed ahead of it.
  - **Supporting guidance only:** the [S5 model-version governance research
    report](research/s5-model-version-governance-research-report.md) prepares
    decision/evidence packets but selects no Council model or Operator version
    and does not discharge 7.5; it authorizes no implementation, reopens no
    Q8, amends no design, and satisfies no S5 gate.
  - **RULINGS RECORDED 2026-08-29** ([`rulings-2026-08-29.md`](rulings-2026-08-29.md),
    R1–R5). Brett ruled the TARGET composition: Option D, all-Anthropic 2:2 —
    `lead-quality` → `claude-sonnet-5`, `lead-security` and `lead-integration`
    → `claude-opus-5`, and the tenant declaring `claude-sonnet-5` for
    `company-policy-lead` in its parallel lane; the Operator plane is the
    DIRECT ANTHROPIC API, reached through today's Claude Code transport and
    EVIDENCED by read-back — partner-plane routing to Bedrock, Vertex or
    Foundry shown unset, the base URL resolving to the direct API, the
    opt-in server-side `fallbacks` beta asserted UNSET — never inferred from
    the transport, and fail-closed if the read-back shows a partner plane.
    A ruled target is not a Council selection: the Gate-Rules
    Council's soak-evidenced selection act and the roster-change Lead's
    `lead_accepted_recorded` acceptance are STILL OWED, and the Council must
    rule in the same act whether the alias-to-exact flip re-opens the soak. So
    **7.5 stays UNTICKED** and the flip stays folded into 7.6's runbook walk.
  - **THE COUNCIL SAT 2026-08-29.** `gate_rules_council` convened on the S5
    seat-to-model selection and returned **UNANIMOUS ACCEPT AS AMENDED, 5/5**,
    and **UNANIMOUS 5/5 that no slot can carry an unqualified SELECT on the
    evidence before the bench on 2026-08-29**. The record of authority is
    codexFactory
    `hermes/domain/review-councils/records/2026-08-29-gate-rules-s5-seat-model-selection.md`
    — **its §8 is the sole disposition** — with the verbatim seat returns beside
    it at `hermes/domain/review-councils/records/2026-08-29-seat-returns-s5/`,
    the ballot at
    `hermes/domain/review-councils/records/2026-08-29-ballot-s5-seat-model-selection.md`
    and the convening packet at
    `hermes/domain/review-councils/convening-packets/2026-08-29-s5-seat-model-selection.md`
    (codexFactory **PR #139**).
    - **The THREE DOMAIN pins are CONDITIONAL SELECT**, on the union of the
      bench's conditions (record §8.3): `lead-quality` → `claude-sonnet-5`,
      `lead-security` → `claude-opus-5`, and `lead-integration` →
      `claude-opus-5` **additionally conditional on LA-C3**, the four-class
      integration soak, being run and recorded first (§8.4). **The TENANT slot
      is not on that union** — see the next bullet. **No unqualified SELECT was
      returned by any seat or recorded by the convener.**
    - **R4 is an OWED TENANT ACT**, not a completed declaration. Four seats
      measured that the tenant's authority file still reads `model: sonnet` with
      no `claude-` string in it; `company-policy-lead` CONFIRMED the family and
      WITHHELD confirmation of the exact-version act. The tenant edit lands in
      the same change as the domain roster edit — red in either order alone.
      **It is expressly NOT gated on CPL-C2**: ballot option (b), commissioning
      CPL's policy case before the tenant act, was declined (record §8.5).
    - **Seven blocking repairs accepted** (R-I…R-VII), chief among them carrying
      the SERVED model read-back into a durable artifact and refusing on
      mismatch; twenty should-fix items accepted as should-fix, not as gates.
    - **The soak union is commissioned**, with a ruled order: served-model
      read-back landed → the flip → the first soak row → activation.
    - **This does NOT discharge 7.5.** The record selects nothing
      unconditionally, applies nothing to the enrolled roster (the roster-change
      Lead's `lead_accepted_recorded` act is still OWED), ticks no task here, and
      discharges no S5 gate or activation-gate entry. **7.5 stays UNTICKED.**
- [ ] 7.6 **[OPERATOR]** Write the governed re-issuance RUNBOOK for a provider
      alias roll, and walk it once against a deliberate composition bump. Without
      it, one provider release revokes every seat grant at once, every convening
      parks under `missing_required_seat: refused`, and the only routine exit
      under a sole code owner is `--admin` — the ritual this change exists to
      break.
  - STAYS OPEN, and it is now the load-bearing operator item of S5. 7.5's model
    half is blocked ON it: the seat model is a Gate-Rules Council decision
    (`council-deliberation-worker.yml:710-723`, ruled 2026-08-22 — "this lane
    will not choose one"), so the alias-to-exact-version flip IS the deliberate
    composition bump this runbook is supposed to be walked against. The runbook
    and that flip are one act, not two.
  - **Supporting guidance only:** the [S5 model-version governance research
    report](research/s5-model-version-governance-research-report.md)'s
    unresolved-decision matrix informs the runbook but is not a runbook walk,
    re-issuance act, or completion evidence; it selects no Council model or
    Operator version, authorizes no implementation, discharges no task,
    reopens no Q8, amends no design, and satisfies no S5 gate.
  - **THE RUNBOOK'S TARGET SHAPE IS NOW RULED, 2026-08-29**
    ([`rulings-2026-08-29.md`](rulings-2026-08-29.md)). R8 fixes the
    re-issuance record the runbook must produce — superseding grant ref,
    superseded grant ref, composition hash, ratifying human, effective time,
    as a MINIMUM and not a ceiling. R9 fixes the in-flight behavior it must
    describe — a revoked holder PARKS with a named refusal, no
    grandfathering, no earlier admission stamp honored, resume only under a
    new human-ratified issuance. Write the runbook against those; neither
    ruling is enforced until the change carrying R6–R12 is ratified, so this
    task stays OPEN.
- [ ] 7.7 **Gate:** a revoked holder parks a convening with a named refusal in a
      rehearsed test; an unreadable register refuses; the runbook has been
      walked once.
  - **RUNTIME HALF DONE, gate NOT met.** Limbs one and two — "a revoked holder
    parks a convening with a named refusal in a rehearsed test" and "an
    unreadable register refuses" — are both asserted in hermes-install #51, on
    real Postgres and over HTTP, not only in unit isolation. They are on an
    UNMERGED branch whose code is held on #50's ratification, and they are
    additionally gated on the standing constraint at the head of this file: no
    reseed until a hermes-install image at `3de0519`+ is deployed, and
    codexFactory convenings currently FAIL CLOSED pending seat-key provisioning.
    Limb three is 7.6, unstarted. The gate is not met.
  - **A DATED CONSEQUENCE, recorded here so it is not a surprise.** The live
    register row `row-mrc-0001` expires `2026-11-23T12:00:00Z`, and #51 now
    asserts that boundary in both directions
    (`test_the_live_register_rows_expiry_is_a_fact_a_test_asserts`) rather than
    leaving it a date in a file nobody re-reads. On that day every convening
    parks under `review_authority.grant_expired` with no code change and no
    deploy to blame. Re-issuance is an operator act with a lead time, and this
    is where the date is stated as a SCHEDULED EVENT.
  - **Supporting guidance only:** research completion in the [S5 model-version
    governance research report](research/s5-model-version-governance-research-report.md)
    is not gate completion; it selects no Council model or Operator version,
    authorizes no implementation, discharges no task, reopens no Q8, amends no
    design, and satisfies no S5 gate.

## 8. Bench and governance items carried, not performed

- [x] 8.1 **[GOVERNANCE]** Rule **Q8** — composition drift for hosted-model
      holders: a standing reissue policy as a first-class intake act; whether
      derived grants survive a parent revoked for DRIFT rather than CAUSE; who
      tells the operator the register emptied (the Human Escalation Contract's
      parked decision-ready packet is the house shape — N12); whether a hosted
      holder may pin a model FAMILY (today a validation failure). Exits (b) and
      (c) of the first two limbs need `openxwallet` / `openxwallet-agent-profile`
      core deltas.
  - RULED 2026-08-26 by Brett Heap — fail-closed bundle
    (`rulings-2026-08-26.md`): reissue is always an explicit register act;
    DRIFT cascades revocation to derived grants exactly like CAUSE;
    empty-register notification rides the HEC decision-ready packet; exact
    model versions only, no family pinning. Cascade enforcement rides the
    named core deltas at S5.
  - **Supporting guidance only:** the [S5 model-version governance research
    report](research/s5-model-version-governance-research-report.md) is
    post-ruling research under the exact-version Q8 baseline; it neither
    reopens Q8 nor changes 8.1's checked state, selects no Council model or
    Operator version, authorizes no implementation, discharges no task, amends
    no design, and satisfies no S5 gate.
  - CORE DELTAS AUTHORED at S5, in openXwallet as the Addendum requires:
    **openXwallet PR #3** (`change/add-composition-drift-cascade`, `fc68f13`,
    `Status: draft`, checks green, NOT merged — held for the convener's
    ratification). Two MODIFIED requirements, the first `## MODIFIED
    Requirements` block that repository has ever carried. `openxwallet`
    "Revocation propagates through the chain" gains: a recorded revocation
    reason class that is NEVER consulted to narrow propagation, so DRIFT
    cascades exactly as CAUSE (stated in the CORE because the profile delegates
    there); every propagated revocation records the edge it descends from; a
    revoked grant never returns to active, so resumption is a NEW grant naming
    what it supersedes; a holder left with no active standing reaches a human
    through the consuming capability's declared escalation path rather than a
    log line. `openxwallet-agent-profile` "A composition change revokes the
    agent's grants immediately" gains: the change is a DRIFT-class revocation
    cascading under the core rule; `grants_state:
    revoked_on_composition_change` is a DECLARATION and not the revocation, so
    a declaration standing beside a still-active grant is a validation failure
    — this closes the real mechanical gap, which was that nothing walked from
    the composition record's self-declaration to the wallet's actual grant
    records the way the core's chain check already does for parent and holder
    revocation; resumption requires an explicit human-ratified issuance act;
    and a declared model component names an EXACT version, a family or alias
    being a validation failure (limb (d), restated where it binds).
  - Q8's REISSUANCE POLICY PROPOSED by S5's implementer, per this task's
    reservation, in that PR's `design.md`: reissuance is a first-class ACT
    recording the superseding grant, the superseded grant, the composition hash
    issued against, the ratifying human and the instant — an act and not a
    state transition, because anything triggerable can be triggered by the very
    thing it polices; no standing form exists, a standing reissue being a
    pre-signed blanket for a composition that did not yet exist. Derived grants
    survive NEITHER class; the class is evidence, never a gate. Notification
    takes the decision-ready packet shape, deduped by root cause. Design R1 is
    named honestly as MADE LOAD-BEARING rather than closed: the exit from a
    fleet-wide park is task 7.6's runbook, not an automatic reissue.
  - **AWAITING THE CONVENER — the model-family pin, carried and NOT decided.**
    Limb (d) ratified exact-versions-only and left family pinning revisitable
    "only through a future core delta that can police it". The question put
    back to Brett, verbatim from the proposal: *"Should the core delta being
    authored now define that policing mechanism — a family pin PLUS an attested
    resolved-version record, re-attested on every roll — or does
    exact-versions-only stand un-revisited?"* Both exits are costed there; the
    admitting exit's hidden cost is a NEW window between the roll and the
    re-attestation — a fresh fail-open inside a change that exists to close
    one. The authored deltas are consistent with the standing ruling, so this
    question sits AHEAD of PR #3's ratification gate: admitting the family pin
    would amend a paragraph of the delta before it is ratified, not after.
  - **RESOLVED — recorded 2026-08-29; the ruling is dated 2026-08-28.**
    The question above was answered by ratification: Brett ratified
    openXwallet PR #3 (`add-composition-drift-cascade`) AS AUTHORED on
    2026-08-28 (`f3f72c6`), and the ratified change's own text records the
    outcome — `proposal.md:115-117` and `design.md:227-229`, verbatim and
    identical in both: *"Resolved 2026-08-28 by ratification as proposed:
    the delta's exact-version rule stands — a declared model component
    names an exact version, and a family pin is a validation failure.
    Admitting a family pin would now be a new change."* Brett confirmed on
    2026-08-29 that this ratification settled the question:
    exact-versions-only stands un-revisited, and a family pin is a
    NEW-CHANGE act, not a pending convener decision. No checkbox changes
    here; the research report's section 4 "Ruling Of Record"
    (`research/s5-model-version-governance-research-report.md`) mirrors
    this entry.
    The remaining Packet 4 rulings this ratification did NOT settle —
    canonical serialization, digest, re-issuance grammar, corpus drift,
    lifecycle roles, and the signer deferral — are recorded as R6–R12 in
    [`rulings-2026-08-29.md`](rulings-2026-08-29.md), dated 2026-08-29.
- [x] 8.2 **[GOVERNANCE]** Rule **Q9** — the floor's source-of-truth inversion.
      Either move the floor's source of truth into a seedable, schema-validated
      `.yaml` carrier and demote the record to evidence, or amend
      `roles-authority-model` so the PROMOTED SPEC TEXT governs. Both amend
      `add-substantive-review-lane`'s ratified text, so both need their own
      declared delta.
  - RULED 2026-08-26 by Brett Heap — Exit A (`rulings-2026-08-26.md`): the
    seedable, schema-validated YAML carrier is THE source of truth; the record
    is demoted to evidence. The declared delta that moves floor authority into
    the carrier remains to be authored.
- [ ] 8.3 **[GOVERNANCE]** Rule **Q10** — does a non-human authorizer satisfy
      `isolated_per_use_authorized`? Does not block anything above, because
      §1.2's `act_unsupervised` refusal excludes those holders from
      review-authority grants until it is ruled.
  - DIRECTION RULED 2026-08-26 by Brett Heap — ADMIT WITH CONDITIONS
    (`rulings-2026-08-26.md`). Stays OPEN by design until the per-use
    admission conditions are designed, recorded, and validated; §1.2's
    exclusion remains in force until then.
- [ ] 8.4 **[codexFactory]** Scaffold the OFFER of the three-repository project
      schema, if and when a project's `PA` elects it. Offering is realization
      work; electing is a human's per-project act; neither is performed by this
      change, and electing it confers nothing.
- [ ] 8.5 NOT A TASK, recorded so it is not mistaken for one: defining a real
      reviewer-independence test. The narrowed floor is DECLINED and no
      independence test is currently definable. If someone later believes it is,
      that is a new proposal starting from zero, carrying its own declared
      MODIFIED delta on the floor requirement.

## Addendum — `split-openxwallet-repo` P3 (2026-08-27, `contract-v2.0`)

Recorded here because P3 changes WHERE two of this change's obligations are
discharged, and neither change may quietly assume the other's tree.

**Task 2.6's red-proof is RETARGETED at the consumer gate.** 2.6 is already
discharged above (draft canary PR #387, run 32997867639, a malformed GRANT). P3
re-discharges it against the REPLACEMENT gate, because the thing being proven
changed: it is no longer "the workflow refuses" but "the PINNED reader, run from
the `openXwallet` gitlink at the digest `contracts/openxwallet-pin.yaml` records,
still refuses on openxFactory's own tree". P3's form is a deliberately malformed
ROW under openxFactory's `governance/review-authority/`, turning an openxFactory
pull request RED with a `register-*` finding naming the full path. **It cannot
discharge in openXwallet**: `review-authority-intake/spec.md:30-33` confers
authority only where the reader "runs as a REQUIRED check on the repository that
holds the register", R6 keeps the register HERE, and openXwallet's tree has no
`governance/review-authority/` for a malformed row to sit in.

**S3 and S5's `openxwallet` / `openxwallet-agent-profile` core deltas are
authored in openXwallet from here on.** Those two capabilities left the
openxFactory corpus at `contract-v2.0` (`split-openxwallet-repo`'s two
`## REMOVED Requirements` blocks), so a delta authored against them in this
repository would modify a capability this corpus no longer holds. The
`tasks.md` 8.1 ruling itself needs no edit and is unchanged: it already puts
those deltas at S5, and only their HOME moved. openxFactory-side work in S3/S5 —
the register, its reader's wiring, the runtime's admission stamp — is unaffected,
because the DATA stayed and only the READER travelled.

**What P3 did NOT change here.** `governance/review-authority/` is untouched, all
four files. Ruleset 21538893 is untouched: the required token `wallet-validation`
is a job id and the renamed workflow retains it. The declined narrowed floor
(8.5) stands. The pre-existing gap that codexFactory's floor omits
`governance/review-authority/{grants,wallets,attestations}/` is neither fixed nor
depended on by P3, and remains this change's to own.

## 9. Deltas carried in from `split-openxwallet-repo` P7 (2026-08-28)

`split-openxwallet-repo` archived 2026-08-28 as
[`../archive/2026-08-28-split-openxwallet-repo/`](../archive/2026-08-28-split-openxwallet-repo/proposal.md).
It authored THREE `## MODIFIED Requirements` deltas against `review-authority-intake`,
declared relative to the OUTCOME of THIS change rather than against a promoted spec,
because `review-authority-intake` is not in `openspec/specs/` and all three targets are
among this change's own twelve ADDED requirements.

**They could not be applied at that archive, and were not forced.** `openspec archive`
aborts on a MODIFIED delta whose target capability does not yet exist — verbatim:
`review-authority-intake: target spec does not exist; only ADDED requirements are allowed
for new specs. MODIFIED and RENAMED operations require an existing spec.` The delta
directory therefore travelled into the archived packet UNAPPLIED, as the record of an
obligation that falls due HERE. This is `release-realization`'s ordered-delta rule
(`openspec/specs/release-realization/spec.md:64-79`) applied by PARITY — its letter covers
a requirement already MODIFIED by an active ratified change and these are ADDED — recorded
rather than forced, exactly as that proposal's § Modified Capabilities declared.

- [ ] 9.1 **At this change's promotion, the ADDED text of these three requirements MUST
      carry the amendments.** Verbatim source, with every scenario:
      [`../archive/2026-08-28-split-openxwallet-repo/deferred-specs/review-authority-intake/spec.md`](../archive/2026-08-28-split-openxwallet-repo/deferred-specs/review-authority-intake/spec.md).
      1. *A grant with no reader in a required check confers nothing* — the reader test
         moves from "present" to "present, whether in-tree or REACHABLE THROUGH A
         DIGEST-PINNED SUBMODULE, in which case the pin's digest is what makes WHICH READER
         RAN auditable". This STRENGTHENS the rule rather than narrowing it, and it is not
         optional: after `contract-v2.0` the validator is no longer in this repository at
         all, so the unamended scenario is UNSATISFIABLE. Two scenarios are added — the
         reader invoked as `python3 openXwallet/scripts/validate-openxwallet.py .` from the
         openxFactory root under a required check at the pinned digest, and the malformed-row
         red proof discharging in the register-holding repository and never in the product
         repository.
      2. *Review authority is held as an openxwallet grant and by nothing else* — the
         citations at that spec's `:10` and `:15` are repointed, because they resolve into
         paths that left this repository.
      3. *A reviewing holder's composition is pinned, and a composition roll is a governed
         re-issuance* — the citation at `:208` is repointed for the same reason.
      **What does NOT change in any of the three:** the register's location, its human-only
      floor, or the fact that it is openxFactory's own review authority. R6 kept the register
      here; only the READER travelled.
      Realizing code already landed at P3 (`.github/workflows/openxwallet-consumer-gate.yml`
      invoking the pinned reader as a required check; red proof discharged on pull request
      [#432](https://github.com/opensoft/openxFactory/pull/432), run 33109857156, job
      98649492960), so only the requirements' TEXT is outstanding.
