# Tasks: add-substantive-review-lane

## 1. Ratification gate (BRETT)

- [ ] 1.1 `OPENSPEC_TELEMETRY=0 openspec validate add-substantive-review-lane
      --strict` and `--all --strict` green; change listed in the README
      OpenSpec Records block.
- [ ] 1.2 RATIFICATION PENDING. The five open questions in `proposal.md`
      (rollout order beyond the pilot; persona home for non-engineering
      domain repos; whether company-policy-lead joins per-PR councils;
      per-repo ruleset interaction shape; risk-tiering taxonomy) are
      declared, not decided, by this proposal. At minimum the pilot-scoping
      questions (Decision E) do not need to be settled before ratifying the
      six ADDED requirements themselves, since the requirements only bind
      the pilot and require every candidate class to DECLARE a risk tier
      and clearance rule — not to use a specific vocabulary. Everything
      below is parked behind this gate.

## 2. Neutral contract delta (this change's own surface)

- [ ] 2.1 Six ADDED requirements on `roles-authority-model`
      (`specs/roles-authority-model/spec.md`): substantive review authority
      generalization; gate-rules-council-defined candidate classes;
      substantive review accountability; reviewer/enforcer identity
      separation from the author; fail-closed substantive review envelope;
      pilot repository and reviewing domain.
- [ ] 2.2 `docs/roles-and-authority.md` (or wherever the neutral roles doc
      lives per the "Neutral authority model ownership" requirement) gains a
      cross-reference to the new requirements, so the human-readable doc and
      the machine-checked spec do not diverge — text-only, no new authority
      concepts beyond what §2.1 already declares.

## 3. codexFactory instantiation (downstream; executed in codexFactory repo)

- [ ] 3.1 `hermes/domain/review-councils/gate-rules.yaml` gains a
      `risk_tier` and `clearance_rule` field per candidate class (schema
      addition to the codexFactory-owned `merge-approval-envelope` mechanics
      contract referenced from `.github/merge-approval-envelope.yml`'s
      header comment).
- [ ] 3.2 `gate_rules_council` produces a record defining
      `opensoft/openxFactory`'s substantive candidate classes (at minimum
      one to prove the generalization; risk tier and clearance rule
      declared per Decision B), with the company-policy-lead seat's
      compliance rationale and a domain seat's best-practice rationale on
      record per the "Substantive candidate classes" requirement.
- [ ] 3.3 Confirm `merge_readiness_council`'s existing seat composition
      (lead-quality, lead-security, lead-integration) is sufficient for the
      pilot's first substantive class, or record the open question from
      Decision D as still unresolved if a class seems to need the
      company-policy-lead seat per-PR.

## 4. Aggregation / workflow realization (downstream; executed in xFactory aggregation repo)

- [ ] 4.1 Generalize `.github/merge-approval-envelope.yml`'s `candidates: []`
      matching from the single `doc-health-nightly` entry to a list keyed by
      `(repo, author-shape, path/diff-shape, risk_tier)`, adding
      `opensoft/openxFactory` to `target_repos` for its own new candidate
      class(es) without touching the existing `doc-health-nightly` entry.
- [ ] 4.2 Generalize `.github/workflows/merge-master-approval.yml`'s
      candidate resolution and author/identity checks to iterate the
      candidate list rather than assume the single hard-coded class,
      preserving: base-branch-only rule reads, the anti-spoofing
      `COUNCIL_LANE_APP_ID` binding on the `council-verdict/merge-readiness`
      check-run, the dedicated merge-master token mint, and fail-closed
      parking on any unevaluable condition.
- [ ] 4.3 Verify author/enforcer identity separation holds for
      agent-authored candidates: the enforcer MUST refuse clearance when a
      candidate's author identity matches a participating council seat's
      identity or the merge-master approving identity itself (the
      "Reviewer and enforcer identity separation" requirement's scenario).

## 5. Pilot-repo wiring + records (downstream; executed in openxFactory repo)

- [ ] 5.1 `opensoft/openxFactory` gets its own workflow instance (or a
      cross-repo-capable instance of §4's generalized workflow) and its own
      ruleset wiring, since `pull_request_target` fires in the repo the PR
      targets — decide the ruleset interaction shape (required-review vs
      required-check-run, human review as an always-available alternate
      path) per repo, per the declared open question.
- [ ] 5.2 First live substantive candidate on `opensoft/openxFactory`:
      `gate_rules_council` record exists (§3.2), `merge_readiness_council`
      produces a per-PR verdict record, the signed check-run and audit
      artifact are produced, and a real `APPROVE` review lands from the
      dedicated identity — mirroring the 2026-08-14 xFactory PR #85/#100
      precedent, this time on openxFactory.
- [ ] 5.3 Record the pilot run's evidence (council records, check-run,
      audit artifact, approval) under this change's own evidence trail for
      the eventual archive.

## 6. Validation and exit

- [ ] 6.1 `openspec validate --all --strict` green; the six ADDED
      requirements' scenarios reviewed against the six decided principles
      for coverage (no principle without a requirement, no requirement
      re-deciding an open question).
- [ ] 6.2 `scripts/doc-health.py --single-repo .` shows no NEW findings
      beyond the pre-edit baseline captured at authoring time (3 critical,
      6 error, 39 warning, 3 info as of 2026-08-15).
- [ ] 6.3 Archive on realization evidence per `release-realization`: the
      six requirements alone do not gate archiving (they are the proposal's
      own surface, §2), but downstream sections 3–5 are named follow-ups
      whose own realization changes (or a tracked completion of this one)
      carry their own archive evidence — this proposal itself may archive
      once §2 lands and validates, per the same "spec delta lands, domain
      follow-ups are named not performed" pattern `add-client-identity-roster`
      used for its own domain-fragment tasks.
