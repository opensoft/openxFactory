# Quickstart: Plan validation and gated handoff

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](spec.md)

## Local planning validation

Use the existing owning bench and the linked 043 feature worktree. The feature selector resolves specs/043-private-connectivity-production. Do not run these commands against a pinned aggregation checkout or another feature.

The following commands are source/document validation only:

    git status --short --branch
    bash .specify/scripts/bash/check-prerequisites.sh --json
    python3 scripts/validate-openspec-cli-pin.py --change qualify-private-connectivity-production --strict
    python3 scripts/validate-openspec-cli-pin.py --all --strict
    python3 scripts/validate-sequenced-after.py . --ledger-diff
    python3 scripts/validate-code-surface.py .
    python3 scripts/validate-target-release.py .
    git diff --cached --check

Run focused doc-health status-validity and duplicate-packet checks separately using the existing CLI. Whole-corpus OpenSpec validation retains its existing accepted finding; a zero wrapper exit is not a clean whole-corpus claim. Existing broader provenance findings remain outside this packet.

The [validation matrix](validation-matrix.md) lists inspected owner source commands. Execute them only from the correct owner checkout/bench with its declared dependencies and accepted scope; this planning pass does not invoke them.

## Planning and task handoff

Read plan.md, research.md, owner-scopes.md, commissioning.md, data-model.md, [tasks.md](tasks.md), the [analysis/remediation record](analysis.md) and the contracts directory. T001–T005 preparation and T006's exact E/source-only custody acceptance are complete. The [owner ratification](../../openspec/changes/commission-private-connectivity-production-evidence/review/ratification.md) records the accepted scope; this pass stops before T007 helper implementation. Full program Q0 and every later gate retain their remaining decisions. Do not generate child implementation lists or reopen 040.

The complete specification/plan/tasks artifact handoff can satisfy governance task 2.1 after validation. It does not supply C-01 owner acceptance, governance task 2.2 or a passed Q0.

## Q0 commissioning package

Collect accepted exact owner/repository/code/CI/schema/test/verification scopes and the owning governance decisions. Select C-02 platform/provider and actual domain/targets before their dependent implementation. Name release/support, custody, operating-objective and cost/capacity responsibilities, and attach remaining decisions to their due gates.

Approve only work whose consumed decisions exist. Local package preparation may be independently commissioned for its actual scope; it does not select a hosted provider. New neutral publication, evidence verification/shared registration, required Ops CI and production domain protection need their owning authority before edits.

## Source implementation to Q1

After the applicable Q0 acceptance, implement accepted workstreams and explicit required CI, produce supported compatible releases, and verify consumer pins. T049 closes the final consumer/service/profile/harness matrix against actual final-candidate source integration and collected CI after domain integration; stale combinations return to accepted owner tasks before target preparation. Supply C-03–C-08: current target execution, actual integrations/custody, supported matrix/candidates, numeric limits, bounded staging and protected evidence/probes. Q1 is refused until every required input is current and complete.

The feature 043 verifier/registration and production qualification entry points are planned, not existing executables. Their paths, command interfaces, frozen cases and required wiring must be accepted and implemented before they can qualify a run.

## Q1–Q2 staging

Only a separate accepted Q1 decision permits its bounded run. Owners collect real-client observations for all four paths, two managed customer boundaries and environment separation, positive/denial and direct/relay controls, operational drills, measured limits and authorized neighbors. Review actual outputs and incidents before Q2 acceptance.

Historical Docker lab runners, self-signed fixture identities, synthetic applications and the feature 040 evidence checker are not production quickstart commands or substitutes for these observations.

## Q3–Q4 bounded production canary

Request a separate C-09/Q3 decision naming exact candidate, customer/site/network/domain/environment/region/resource/data/consent/spend/duration scope, monitoring/support/rollback roles and approved fault targets/windows. Refresh managing-factory request/channel-required grant or current unmanaged customer authority as applicable.

Accept Q4 only after the approved actual window, measured objectives, offered-path/isolation/application results, incident closure, cleanup/rollback readback and fresh affected-owner sign-offs. Monitoring gaps do not count. This document authorizes no activation.

## Q5 offer or wave; halt and resume

Admit only the named C-11 offer or C-12 wave against exact current eligible profiles/candidate and accepted Q4. Other profiles/regions/cohorts need their own qualification and decisions.

On a boundary violation, exposure, disclosure, duplicate/revived effect, drift or missed limit, halt affected enrollment/expansion and contain that scope. Preserve current revocations, evidence and authorized neighbors. C-13 requires reviewed remediation, affected/adjacent reruns and fresh scoped authority before resume; re-enter at the earliest affected gate.
