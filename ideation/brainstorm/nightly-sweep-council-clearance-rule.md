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
Updated: 2026-07-23 (Q1+Q4 decided; convening packet assembled; CONVENED —
rule ratified as amended, record at codexFactory
`hermes/domain/review-councils/records/2026-07-23-gate-rules-nightly-sweep-clearance.md`)

## Convened (2026-07-23)

The Gate-Rules Council's first exercise ran as a recorded manual rehearsal:
all seat verifications HOLD (LS floor verified against `envelope.py`, CSC
pull-in evaluated and not triggered; LA composition; CPL kill switch +
notices; project seat vacant-symbolic), with one **LQ amendment** — the
docs-class allowlist narrowed from `**/*.md` to
`["health/**", "docs/**/*.md", "README.md"]` (workflow contracts, openspec
records, and `hermes/` governed content are not docs-class). Q2 blessed:
lane-emitted PR check-run transport. **Rule v1 RATIFIED AS AMENDED**,
`configured_but_inactive`; Brett Heap's acknowledgement registered. The
rehearsal satisfies `first_convening_rehearsed_and_recorded`; the remaining
activation-gate requirement is council orchestration in the Omnigent lane.
Exit IMPLEMENTED 2026-07-23: codexFactory change
`add-nightly-sweep-council-clearance` — rule YAML + council_clearance.py
decision core (composes tier 1, envelope.py untouched) + 18 negative-suite
tests, all green, on main 8931ee2. Ships active: false (report-only).
Pending: ratification; archives after its parent
add-merge-master-autonomous-approval. Activation awaits council
orchestration in the Omnigent lane.

## Decided (2026-07-23)

- **Q1 — docs-class is a static allowlist, Lead Quality owns it.**
  Rules-as-code: `**/*.md` plus `health/**`; everything else — workflows,
  scripts, schemas, any YAML outside `health/**` — is NOT docs-class.
  Allowlist changes are Lead-Quality-accepted recorded events. Deterministic,
  auditable, no new code surface, no circularity.
- **Q4 — v1 clears docs-only overflow alone.**
  `dispositioned_regression_finding` is dropped from v1 (riskier, rarer);
  adding it later is a normal rule amendment through the same council. One
  crisp condition for the council's first exercise.

## Decided (2026-07-25)

- **Verdict-emitting identity is a DISTINCT lane identity, `checks: write`
  only** (Brett, 2026-07-25, at the `add-council-clearance-lane-wiring`
  proposal gate). Three-identity separation on the candidate PR: the
  content App authors, the lane identity emits the verdict check-run, the
  Merge Master App approves — no identity both produces evidence and
  consumes it for its own act. Reusing the content App was considered and
  set aside: the PR author emitting the clearance evidence for its own PR
  weakens the separation the envelope is built on.
- **Backing stack for rehearsal + initial active period** — DECIDED
  (Brett, 2026-07-26, option B): the live opensoft self-client QA stack
  (`hermes-opensoft-qa`) backs both the rehearsal and the initial active
  period. Conditions recorded with the decision: (1) a named migration
  trigger — the lane moves to a production-posture stack at P5 self-host
  landing OR at the first domain-layer reseed of the QA stack, whichever
  comes first; (2) a lane-side duplicate guard — the lane never
  commissions a convening for a head SHA that already carries a verdict
  check-run (protects the convene-at-most-once discipline against a
  reseed wiping the runtime's job ledger). Both conditions ride the
  `council_orchestration_available` attestation packet. Risk basis: the
  clearable set is docs-class overflow on the bot-authored nightly PR
  only — unanimous SHA-pinned verdict, independently re-judged by the
  tier-2 core, anti-normalization at 3, standing kill switch,
  per-clearance notice.

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

  council_clearable:                          # closed, declared list — nothing else (v1)
    - id: docs_only_path_overflow
      condition: paths exceed health/** but every changed path is docs-class
      docs_class:                             # DECIDED: static allowlist, no classifier
        allowlist: ["health/**", "docs/**/*.md", "README.md"]   # as amended at the convening
        everything_else: not_docs_class       # workflows, scripts, schemas, YAML outside health/**
        owner: lead-quality                   # allowlist changes = Lead-accepted recorded
      council_verifies: no behavioral or config surface touched

  deferred_amendments:                        # NOT in v1; normal rule amendment later
    - id: dispositioned_regression_finding
      note: riskier and rarer; propose through the same council when wanted

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

## Convening packet (Gate-Rules Council first exercise — rehearsal)

Everything the seats need in one sitting; the human step is Brett's
acknowledgement.

1. **The rule** — the v1 YAML above (docs-only overflow, static allowlist,
   never-clearable floor, unanimous SHA-pinned verdict, once-per-SHA,
   anti-normalization at 3, kill switch, configured_but_inactive).
2. **Verification claims for the seats to check, not assume:**
   - *Lead Security:* the never-clearable floor covers every security
     surface (identity, checks, secrets, security-touching paths, gate
     weakening) — therefore the rule widens nothing security-posture-shaped
     and the **CSC conjunction pull-in is not triggered** (evaluated on the
     record, not waved through).
   - *Lead Quality:* the docs-class allowlist is deterministic and owned;
     the anti-normalization threshold turns recurring clearances into
     generator fixes (evidence before trust holds).
   - *Lead Architect:* tier-2 composes with tier-1 without weakening it;
     the council output is a recommendation, the Merge Master remains the
     only approver, repository enforcement stays final.
   - *Company Policy Lead:* "is this allowed here" — the tenant accepts an
     agent council clearing a docs-maintenance exception class with a
     standing kill switch and per-clearance notices.
   - *Project seat (intent-owner, symbolic):* recorded as vacant-symbolic;
     binds when the subject-layer roster lands.
3. **Q2 recommendation carried into the convening:** verdict transport as a
   **PR check-run emitted by the lane** — already SHA-bound, visible in the
   PR, and the Merge Master App already reads check state; the alternative
   (governed record the App queries) adds an API surface. Council blesses
   or redirects.
4. **Output:** the ratified `per_repo_gate_rules` record + Brett's
   acknowledgement notice → then the codexFactory OpenSpec change
   (envelope.py tier-2 classification + recommendation-record check +
   negative tests, shipped configured_but_inactive).

## Open questions

- ~~docs-class definition~~ — DECIDED 2026-07-23: static allowlist, Lead
  Quality owns (§Decided).
- **Recommendation-record transport** — recommendation in the convening
  packet (check-run emitted by the lane); the council blesses or redirects.
- **Notice fatigue** — deferred to activation-gate time, informed by real
  clearance counts (anti-normalization bounds the worst case anyway).
- ~~v1 scope~~ — DECIDED 2026-07-23: docs-only overflow alone;
  `dispositioned_regression_finding` is a deferred amendment (§Decided).
