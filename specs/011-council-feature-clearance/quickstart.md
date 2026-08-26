# Quickstart — 011-council-feature-clearance

Runnable scenarios proving the widening works. Prerequisites: `gh` authenticated with
operator authority on `opensoft/xFactory`; Hermes QA runtime reachable.

## Scenario 1 — Baseline posture (pre-entry)

```bash
gh workflow run merge-master-approval -R opensoft/xFactory && sleep 10 \
  && gh run list --workflow=merge-master-approval -R opensoft/xFactory --limit 1
```

**Expected**: run succeeds; before any new entry lands, log shows the early-exit
("No governed head refs…") or nightly-only classification. This is the regression base.

## Scenario 2 — Floor refusal (US2, post-entry)

After a floor-touching PR class gains an entry (or against an existing qualifying
assembly-class PR), dispatch the convening lane naming its number:

```bash
gh workflow run council-convening-lane -R opensoft/xFactory -f pr_number=<n>
```

**Expected**: configuration guard passes (`HAS_APP_ID/KEY: true`), preflight refuses
with the named never-clearable outcome, and **no runtime job is created**. Idempotent
on re-dispatch.

## Scenario 3 — Pilot convening (US1, conditional on convener ruling R4)

After the convener resolves the classification-mechanics escalation and the pilot
entry lands in `main`: open/observe the matching PR → approval run reaches
`awaiting_verdict` → lane auto-commissions → resolved verdict appears as
`council-verdict/merge-readiness` check-run with `.app.id == vars.COUNCIL_LANE_APP_ID`.

## Scenario 4 — Nightly regression proof

Re-run the approval workflow and confirm the nightly candidate's classification
output matches its pre-widening fixture byte-for-byte (SC-003).

## Scenario 5 — Second-repo fail-closed emission (US3)

With `pr_repo=opensoft/openxFactory` parameterization landed but BEFORE the operator
extends the lane App installation: a qualifying openxFactory candidate reaches
emission and FAILS CLOSED naming the missing installation — never silently skipping.
Post-install, the same path succeeds end-to-end.
