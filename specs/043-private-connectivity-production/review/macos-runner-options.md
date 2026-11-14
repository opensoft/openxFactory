# macOS qualification runner preparation

Status: draft
Kind: review-packet
Prepared: 2026-11-14

Brett approved investigating GitHub macOS runners within included capacity with paid overages prohibited. This packet proposes exact runner and billing constraints for review. It starts no job, changes no billing setting and grants no enrollment or live test. The [approval register](production-approval-register.md), current task dependencies and Q0-Q5 gates still apply.

## Candidate target and finite limits

The [GitHub runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) currently lists standard private-repository macos-15 on a three-core M1 arm64 VM with 7 GB RAM, and macos-15-intel on a four-core Intel VM with 14 GB RAM. Both have 14 GB SSD and passwordless sudo. They are candidate client hosts; the Headscale server remains on its independently accepted target. They are not larger runners, and this proposal uses no mutable macos-latest alias.

Propose two sequential jobs, at most 20 minutes each and 40 rounded billed minutes total, with no automatic retry or periodic trigger. At the current [actions_macos rate](https://docs.github.com/en/billing/reference/actions-runner-pricing) of USD 0.062/minute, that is up to USD 2.48 of included compute value and USD 0 permitted paid usage. Queuing/actual VM availability, image identity, supported Tailscale distribution and real utun/network operation are not proved by documentation.

The labels select a maintained image family, not immutable image bytes. A separately authorized inventory preflight must capture actual OS/build, ImageVersion, architecture and client artifact identities; the qualification owner accepts that exact matrix before enrollment. Do not treat sudo, a successful package install or a userspace proxy as proof of the required actual client route/application path. GUI/App Store client coverage is not inferred from a CLI variant. No nested Docker/server workload or private Azure-network integration is assumed available on the Mac VM.

The intended owner is private opensoft/Headscale-Install and its accepted qualification surface, after T010/T011/T020-T023 and the applicable target gates. Do not move private implementation/evidence to a public repository to obtain free compute. Actual endpoint access, short-lived enrollment authority, protected output transport, revocation and cleanup require their accepted C-03/C-08/run plan. Workflow implementation, dispatch and a Mac client enrollment are distinct actions and have not occurred.

## Read-only account findings

The organization reports an Enterprise plan and existing macOS usage in the current month; reported Mac net charges were zero at inspection. GitHub now describes included compute as a monetary allowance. Its billing usage/summary APIs report gross, discounts and net usage, not a reserved remaining allowance for this proposed run. Public-runner discounts and shared account usage prevent treating a gross or net total as proof of available private capacity. The raw account/budget observations remain in the private preparation audit.

The existing organization-wide Actions hard budget permits positive paid usage. No inspected repository-specific zero-paid Mac guard covers this proposed qualification. Consequently the selected no-overage constraint is not yet enforced. Do not start a job based solely on current zero net charges or the organization plan's advertised allowance.

## Concrete billing guard proposed for approval

Propose one repository-scoped SKU budget through the documented [GitHub billing budgets API](https://docs.github.com/en/rest/billing/budgets), with this exact request body:

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

Approval of this proposed guard must precede the API mutation. After approval, require exact returned scope/SKU/amount/prevent_further_usage readback, no broader setting changes, and confirmation of effective budget semantics/current included headroom with the billing owner before any dispatch. If capacity or enforcement cannot be established, keep the jobs blocked; do not enable paid usage or raise the budget. Budget approval alone grants no runner job or live target action. Retain the guard unless a separate owning decision changes it; removing it can remove the spending protection.

No billing policy, GitHub workflow, runner allocation, secret, target or enrollment was changed by this investigation.
