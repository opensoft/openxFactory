# macOS qualification runner preparation

Status: draft
Kind: review-packet
Prepared: 2026-11-14

Brett approved investigating GitHub macOS runners within included capacity with paid overages prohibited. He subsequently authorized the one-time billing-owner guard below, which was applied and verified on 2026-11-14. The runner options still require their consuming decisions; no job, enrollment or live test has started. The [approval register](production-approval-register.md), current task dependencies and Q0-Q5 gates still apply.

## Actual guard decision and readback

Brett reviewed [the exact proposed action](https://github.com/opensoft/openXfactory/blob/56ba53c89c69a0f1d8f9f4fba39794d4933c8bf5/specs/043-private-connectivity-production/review/macos-runner-options.md) and answered:

> Approve the one-time zero-paid Mac guard (Recommended)

The existing authenticated session was verified as brettheap with active organization-admin membership in Opensoft and the target as the private opensoft/Headscale-Install repository. A pre-action budget read found no matching repository Mac guard. The one-time owner action created one budget, and an independent GET returned repository scope opensoft/Headscale-Install, SkuPricing, actions_macos, budget_amount 0 and prevent_further_usage true, with alerts disabled and no recipients. All four pre-existing budget records matched their complete pre-action parsed JSON values; no other budget was added. The private preparation audit retains the original request, response and before/after readback. This reviewed summary is not commissioned rollout evidence or acceptance of remaining capacity.

This action implements only the supplied billing-owner exception. It grants no ongoing factory billing authority, runner dispatch, enrollment, target credential or paid overage. Current included headroom and actual VM/client capability remain pre-dispatch requirements. The storage financial approval does not pay for Mac compute.

## Candidate target and finite limits

The [GitHub runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) currently lists standard private-repository macos-15 on a three-core M1 arm64 VM with 7 GB RAM, and macos-15-intel on a four-core Intel VM with 14 GB RAM. Both have 14 GB SSD and passwordless sudo. They are candidate client hosts; the Headscale server remains on its independently accepted target. They are not larger runners, and this proposal uses no mutable macos-latest alias.

Propose two sequential jobs, at most 20 minutes each and 40 rounded billed minutes total, with no automatic retry or periodic trigger. At the current [actions_macos rate](https://docs.github.com/en/billing/reference/actions-runner-pricing) of USD 0.062/minute, that is up to USD 2.48 of included compute value and USD 0 permitted paid usage. Queuing/actual VM availability, image identity, supported Tailscale distribution and real utun/network operation are not proved by documentation.

The labels select a maintained image family, not immutable image bytes. A separately authorized inventory preflight must capture actual OS/build, ImageVersion, architecture and client artifact identities; the qualification owner accepts that exact matrix before enrollment. Do not treat sudo, a successful package install or a userspace proxy as proof of the required actual client route/application path. GUI/App Store client coverage is not inferred from a CLI variant. No nested Docker/server workload or private Azure-network integration is assumed available on the Mac VM.

The intended owner is private opensoft/Headscale-Install and its accepted qualification surface, after T010/T011/T020-T023 and the applicable target gates. Do not move private implementation/evidence to a public repository to obtain free compute. Actual endpoint access, short-lived enrollment authority, protected output transport, revocation and cleanup require their accepted C-03/C-08/run plan. Workflow implementation, dispatch and a Mac client enrollment are distinct actions and have not occurred.

## Read-only account findings

The organization reports an Enterprise plan and existing macOS usage in the current month; reported Mac net charges were zero at inspection. GitHub now describes included compute as a monetary allowance. Its billing usage/summary APIs report gross, discounts and net usage, not a reserved remaining allowance for this proposed run. Public-runner discounts and shared account usage prevent treating a gross or net total as proof of available private capacity. The raw account/budget observations remain in the private preparation audit.

The existing organization-wide Actions hard budget permits positive paid usage. The newly verified repository-specific zero-paid Mac guard now supplies the tighter spending control for this proposed qualification. Do not start a job based solely on that control, current zero net charges or the organization plan's advertised allowance: actual included headroom, target authority and the accepted run are still required.

## Approved billing guard request

The approved one-time action used the documented [GitHub billing budgets API](https://docs.github.com/en/rest/billing/budgets), with this exact request body:

```json
{
  "budget_amount": 0,
  "prevent_further_usage": true,
  "budget_scope": "repository",
  "budget_entity_name": "opensoft/Headscale-Install",
  "budget_type": "SkuPricing",
  "budget_product_sku": "actions_macos",
  "budget_alerting": {
    "will_alert": false,
    "alert_recipients": []
  }
}
```

The intended effect is to prohibit paid macOS overage in this repository while allowing eligible included use. This also covers future Mac jobs in that repository, not just this feature. It does not change another SKU, repository or the organization-wide budget. GitHub documents overlapping budgets as a possible source of job blocking; the tighter repository guard may stop Mac work when included capacity is exhausted. See [budget controls](https://docs.github.com/en/billing/how-tos/set-up-budgets).

Actual owner approval preceded the API mutation, and exact scope/SKU/amount/prevent_further_usage readback plus preservation of unrelated budgets passed. Confirm effective budget semantics/current included headroom with the billing owner again before any dispatch. If capacity or enforcement cannot be established, keep the jobs blocked; do not enable paid usage or raise the budget. Budget approval alone grants no runner job or live target action. Retain the guard unless a separate owning decision changes it; removing it can remove the spending protection.

The existing [Ops GitHub-administration workflow](https://github.com/opensoft/opsXfactory/blob/main/workflows/github-administration.yaml) explicitly prohibits organization/team/billing/security setting changes and reports its production mutation authority unrealized. The budget is not an accepted act of that workflow. Brett's separate explicit approval supplied the one-time direct billing-owner exception for only the request above, through the existing authenticated owner session. The workflow prohibition for factory automation is preserved; no credential, App scope or role was added. No broader automated billing administration or qualification job is authorized.

Only the approved repository Mac billing guard changed. No GitHub workflow, runner allocation, secret, target or enrollment changed.
