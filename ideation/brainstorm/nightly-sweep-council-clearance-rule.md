# Nightly-Sweep Council Clearance: tier-2 rule for the doc-health rolling PR — Brainstorm

Status: brainstorm
Kind: process
Author: Brett Heap (concept: defaults let the council merge-or-not the nightly
sweep); drafted with Claude (session 2026-07-23)
Origin: human
Summary: Extends the ratified Merge Master autonomous-approval envelope
(`add-merge-master-autonomous-approval`, codexFactory) with a **tier-2
council-clearance path** for the nightly doc-health rolling PR: when the
conjunctive envelope fails on a condition in a declared *council-clearable*
set, the merge-readiness council (LQ/LS/LI) convenes and its unanimous
`ready` verdict — pinned to the exact head SHA — lets the Merge Master
approve; security-touching failures, check failures, and identity mismatches
are **never clearable** and park for the human as today. Includes an
anti-normalization rule (a condition cleared repeatedly stops being clearable
and parks with a fix-the-generator flag) and ships `configured_but_inactive`
behind an activation gate until council orchestration lands in the Omnigent
lane. Widening what auto-clears is a per-repo gate rule, so ratifying this is
the **Gate-Rules Council's first real exercise**.
Topics: codexfactory, merge-master, autonomous-approval, doc-health-sweep,
merge-readiness-council, gate-rules-council, auto-clear-envelope, tier-2,
nightly-sweep, omnigent-lane, activation-gate, cost-accountability
Repository context: codexFactory (envelope rules-as-code + per-repo gate rule); openxFactory (this leaf)
Captured: 2026-07-23

## The two tiers

- **Tier 1 (exists, ratified 2026-07-16):** the rules-as-code envelope
  auto-approves when ALL hold — content-App author, `doc-health/nightly`
  head ref, paths ⊆ `health/**`, all required checks green, no open
  regression finding. No council; deliberation on the happy path would fail
  the efficiency audit.
- **Tier 2 (this rule):** envelope fails → classify the failing conditions;
  if every failure is in the council-clearable set, convene the
  merge-readiness council instead of parking straight to the human.

## Draft rule (the ratifiable artifact)

```yaml
schema_version: 1
kind: per_repo_gate_rule
rule:
  id: nightly-sweep-council-clearance
  repository: opensoft/codexFactory
  applies_to:
    pr_class: doc-health-nightly-rolling      # tier-1 envelope's subject, unchanged
  default_state: configured_but_inactive      # activation gate below
  tier_1: merge_master_autonomous_envelope    # unchanged; this rule NEVER weakens it

  council_clearable:                          # closed, declared list — nothing else
    - id: docs_only_path_overflow
      condition: paths exceed health/** but every changed path is docs-class
      council_verifies: no behavioral or config surface touched
    - id: dispositioned_regression_finding
      condition: an open regression finding exists but carries a recorded
        disposition or contested-resolution in flight
      council_verifies: the finding does not bear on THIS PR's content

  never_clearable:                            # always park for the human
    - author_or_app_identity_mismatch         # identity stays hard — spoofing surface
    - head_ref_mismatch
    - any_required_check_failed               # checks are the enforceability floor
    - secret_scan_finding
    - security_touching_path                  # CI config, workflows, dependency
                                              # manifests, scripts/ — CSC/LS territory
    - gate_weakening_change                   # council_large territory, never tier-2

  council:
    body: merge_readiness_council             # LQ / LS / LI (change B object)
    quorum: all_seats                         # missing seat => REFUSED => park
    verdict_required: ready_unanimous         # split => park (council semantics)
    undispositioned_conditions: zero
    pinned_to: head_sha                       # any new push invalidates the verdict
    convene_at_most: once_per_head_sha        # spend discipline; convening clocks in

  anti_normalization:                         # deviance must not become the default
    same_condition_cleared_consecutively: 3   # nights
    then: park_with_fix_the_generator_flag    # stop clearing; fix the sweep instead;
                                              # efficiency-audit signal recorded

  human:
    step: acknowledgement_of_notice           # non-blocking notice per tier-2 clearance
    kill_switch: standing                     # the human can disable tier-2 at any time

  activation_gate:                            # inert until the lane can convene councils
    requires:
      - council_orchestration_available       # Omnigent-lane execution of council mixes
      - first_convening_rehearsed_and_recorded
    until_then: envelope_failure_parks_for_human   # exactly today's behavior
```

## Why this shape

- **Councils advise; the lever stays mechanical.** The council's `ready` is a
  recommendation record; the Merge Master still executes approval, checking
  the record's SHA pin and TTL like any other envelope condition. No persona
  and no council ever holds the merge lever (repository_owns:
  final_merge_enforcement).
- **Never-clearable is the security floor.** Identity, checks, secrets, and
  security-touching paths stay hard — so the CSC conjunction pull-in is not
  triggered by this rule (it widens nothing security-posture-shaped); noted
  explicitly so the gate-rules convening can verify that claim rather than
  assume it.
- **Anti-normalization** is the piece rules-as-code alone can't express: a
  clearance that recurs is not an exception, it's a defect in the sweep — the
  third consecutive clearance of the same condition parks the PR and flags
  the generator for a fix (feeds `efficiency_finding` in domain memory).
- **configured_but_inactive** mirrors the liaison pattern: ratify the rule
  now, activate when the Omnigent lane can actually convene the council;
  until then behavior is byte-identical to today.

## Governance path (exit)

1. **Gate-Rules Council first exercise:** domain seats LA/LS/LQ, client seat
   company-policy-lead (CSC pull-in explicitly evaluated and — per the
   never-clearable floor — not triggered), project seat = intent-owner slot
   (symbolic), **Brett's acknowledgement** as the human step. The convening
   itself can be run as a manual/rehearsed exercise before orchestration
   exists — its output is this rule ratified.
2. **codexFactory OpenSpec change** extending the merge-master capability:
   the rule record + the envelope.py rules-as-code for tier-2 classification
   and the recommendation-record check, tests mirroring the envelope's
   existing negative suite, `default_state: configured_but_inactive`.
3. **Activation** rides the Omnigent-lane council-orchestration increment;
   flipping the gate is a Lead-accepted recorded event once its two
   requirements hold.

## Open questions

- **docs-class definition** for `docs_only_path_overflow` — extension
  allowlist (`*.md`, `health/**`, doc-index lines in README) vs. a
  doc-health-owned classifier; who maintains it (Lead Quality).
- **Recommendation-record transport** — where the council's verdict record
  lives so the Merge Master (a GitHub App) can check it: a PR check-run
  emitted by the lane vs. a governed record the App queries.
- **Notice fatigue** — per-clearance acknowledgement notices vs. a weekly
  digest once tier-2 clears routinely (interacts with anti-normalization:
  if it clears routinely, the generator needs fixing anyway).
- **Does `dispositioned_regression_finding` belong in v1** — it is the
  riskier of the two clearable conditions; shipping v1 with only
  `docs_only_path_overflow` is a defensible narrower start.
