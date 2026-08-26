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
- [ ] 1.8 **[OPERATOR] [GOVERNANCE]** Ratify or return the proposal. Nothing in
      §2 onward is authorized work until this is discharged.
- [ ] 1.9 Before archive: re-check §1.3's restated requirement text against
      `add-substantive-review-lane`'s FINAL promoted text (design risk R6).

## 2. S1 — the reader: wire the validator into CI as a required check

*No grant is operative until this lands. It precedes everything.*

- [ ] 2.1 Author a `pull_request`-triggered workflow running
      `python3 scripts/validate-openxwallet.py <checkout> --strict`.
      **This is openxFactory's FIRST pull-request-triggered workflow** — both
      existing workflows are `workflow_call` / `workflow_dispatch` — so it needs
      its own trigger, permissions and concurrency design (clarifications N3).
- [ ] 2.2 Follow the house Python pattern: `actions/setup-python@v5` pinned to
      `3.12` plus `pip install pyyaml`; PyYAML is a hard dependency and the
      validator exits 2 without it (N4).
- [ ] 2.3 Pass the checkout path explicitly. A path-less invocation self-tests
      only and passes green while scanning nothing — the vacuous-pass trap this
      whole change exists to name (N5).
- [ ] 2.4 Decide and record whether the gate runs `--strict`; the doc-health
      precedent parameterizes `fail-on` rather than hard-coding it (N5).
- [ ] 2.5 **[OPERATOR]** Make the check REQUIRED in the branch ruleset. This is a
      repository setting, not a tree fact — a merged workflow file is not
      evidence (N6).
- [ ] 2.6 **Gate:** a deliberately malformed grant fails the pull request, and
      the realization evidence includes the ruleset state showing the check
      required (not just the workflow file).

## 3. S2 — the issuer anchor

*Precedes the first wallet: an unanchored root grant is an unbounded one.*

- [ ] 3.1 Implement `issued_by` as REQUIRED **for review-authority grants** — a
      scope restriction by the consuming capability, not a schema change. The
      field already exists and stays optional in the shared grant schema, so no
      `contracts/` edit, no manifest entry, no CHANGELOG line, no bundle cut.
- [ ] 3.2 Implement the ROOT-GRANT class: a grant with no `parent_grant_ref` is a
      root, and its issuer's authority is recorded OUTSIDE the register it
      writes into.
- [ ] 3.3 Record the root-issuer anchor: the responsible operator, standing under
      the Human Escalation Contract (`docs/roles-and-authority.md:103-140`,
      whose parked-decision list names "privileged capability grants"). No
      wallet, no grant.
- [ ] 3.4 **Gate:** the validator refuses a review-authority grant with no
      `issued_by`, and refuses a root grant naming an agent holder as issuer.

## 4. The first wallet

*Cold start. One holder, not eight.*

- [ ] 4.1 **[OPERATOR]** Mint one wallet for codexFactory's
      `merge_readiness_council` as a body, custody model `holder_readable` —
      the only realistic model with no key infrastructure in the stack, and the
      tier the registry designed for exactly this situation (N13).
- [ ] 4.2 Write the wallet record IN THE SAME TREE as the register: `repo_scan`
      builds its context from the scanned repository's own records, and a
      cross-repository audience wallet has no resolution path today (N7).
- [ ] 4.3 Record the custody ATTESTATION row — who verified the isolation,
      against what, when. Without it the intake caps grants to that wallet at
      `request`.
- [ ] 4.4 **[codexFactory]** Declare the holder's composition: map the six
      declared components (model version, prompt contract, tool manifest,
      policy version, parameters, retrieval corpus) onto the actual seat
      artifacts under `hermes/domain/review-councils/` and
      `hermes/domain/agent-mixes.yaml`. **No such mapping exists today** and
      S5's pinning rule is unimplementable without it (N10). The retrieval
      corpus is the PINNED seat prompt plus ontology package — never the
      candidate repository at HEAD.

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
    wallet-validation check (`scripts/validate-openxwallet.py`). An active
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

- [ ] 6.1 **[hermes-install] [GOVERNANCE]** Open a successor change against
      `council-orchestration`. **No amendment to the advisory-only requirement**
      — the work rides the SECOND requirement, "A convening verdict conforms to
      the council's materialized semantics or is refused", because a missing or
      unverifiable seat signature is a conformance defect of the same kind as a
      wrong pin or a missing seat result.
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

- [ ] 7.1 **[hermes-install]** Re-check revocation at VERDICT CONSUMPTION, not
      from the admission stamp. `verdict_for_completion` takes the roster and
      content provenance from the `convening` stamp written at admission, which
      is exactly the issuance-time trust `openxwallet:127-131` forbids.
- [ ] 7.2 **[hermes-install]** On a revoked or expired holder, PARK with a NAMED
      REFUSAL — never silently honour the stamp.
- [ ] 7.3 Declare the register's staleness bound as a duration.
- [ ] 7.4 **[hermes-install]** Unreadable register ⇒ REFUSE. Unreachable,
      unparseable, or older than the bound all refuse; never proceed.
- [ ] 7.5 **[codexFactory]** Pin model version and prompt corpus as declared
      components; forbid the candidate repository at HEAD as retrieval corpus.
- [ ] 7.6 **[OPERATOR]** Write the governed re-issuance RUNBOOK for a provider
      alias roll, and walk it once against a deliberate composition bump. Without
      it, one provider release revokes every seat grant at once, every convening
      parks under `missing_required_seat: refused`, and the only routine exit
      under a sole code owner is `--admin` — the ritual this change exists to
      break.
- [ ] 7.7 **Gate:** a revoked holder parks a convening with a named refusal in a
      rehearsed test; an unreadable register refuses; the runbook has been
      walked once.

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
