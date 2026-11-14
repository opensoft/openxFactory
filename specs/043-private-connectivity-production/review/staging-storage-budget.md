# Dedicated staging-storage budget for review

Status: draft
Kind: review-packet
Prepared: 2026-11-14

Brett approved preparing this budget and subsequently accepted its USD 10 financial envelope on 2026-11-14. This is a storage-only financial limit for existing Opensoft QA in West US, not permission to provision or spend before the required execution gates. It supplies no C-03 execution grant, C-08 protected custody, Q1 entry or production allowance. The [approval register](production-approval-register.md) and frozen 043 gates remain authoritative.

## Actual financial decision

After reviewing the immutable packet in PR #1310, Brett answered:

> Approve the USD 10 financial envelope (Recommended)

The reviewed source is [the budget packet at the supplied decision](https://github.com/opensoft/openXfactory/blob/56ba53c89c69a0f1d8f9f4fba39794d4933c8bf5/specs/043-private-connectivity-production/review/staging-storage-budget.md). The answer accepts only the listed financial ceiling, quantities and window. Actual resource identities, capacity, protected custody/retention, execution authority and Q1 remain separate inputs. No Azure budget object, disk, container, snapshot or other resource was created by recording this acceptance.

## Proposed allocation and limits

The accepted financial ceiling is USD 10 for one staging run lasting at most 14 days, with the retained snapshot/object capacity below reserved for one full billing month. Refresh prices and reconcile the actual topology before execution; a changed quantity, duration, retention cost or ceiling requires a fresh affected decision. This estimate uses public retail rates, before tax or negotiated discounts; it is not an Azure invoice or an automatic spending cap.

| Proposed capacity | Purpose and constraint |
| --- | --- |
| Four 4-GiB Standard SSD LRS disks | Conservative allowance for separate Headscale state for two synthetic customer boundaries across standalone and hosted-factory paths; final instance identities must be accepted before allocation |
| Two 4-GiB Standard SSD LRS disks | Separate product operation state and authoritative current entitlement/revocation state; a runtime restore cannot roll back current authority |
| Two additional 4-GiB disks | Temporary quarantined recovery targets; maximum eight allocated disks including recovery, with sequential drills where necessary |
| 32 billed GB of Standard LRS snapshots | Aggregate used snapshot capacity, not 32 GB per snapshot; preserve separate identity and application-consistent capture |
| 10 billed GB of Hot LRS object storage | Dedicated protected backup/evidence allocation within an existing suitable QA account, subject to actual C-08 policy and permissions |
| 200,000 combined write/list operations and 200,000 read/other operations | Aggregate object-operation allowance for the run; versioned copies count toward the storage limit |

These quantities are engineering assumptions for review, not selected deployment topology or measured application demand. Local Linux Docker needs its own accepted host/state allocation; an AKS Pod or this disk quote does not qualify that server path. The final platform matrix cannot omit a delivery track to fit the budget. Four-GiB volumes require measured bounded synthetic data/WAL/log use and headroom before admission; insufficient space triggers a revised plan rather than an unreviewed resize or reduced coverage.

Read-only QA inspection found the existing managed-csi class uses StandardSSD_LRS, disk.csi.azure.com and WaitForFirstConsumer, with Delete reclaim policy. Do not change the default class, repurpose the unrelated application-specific Retain class, or reuse a bound customer volume. The owning plan must explicitly select safe retention, ext4/filesystem compatibility, single-writer fencing and quarantine/cleanup controls. The class's presence establishes neither free attachment slots nor spare node capacity.

## Pricing and calculation

Rates were read from the [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices) for westus, USD and Consumption pricing on 2026-11-14. Exact filters: serviceName Storage; productName Standard SSD Managed Disks, Standard HDD Managed Disks or General Block Blob v2; relevant LRS meters below. The private preparation audit retains the returned rows and query. No account keys or billing credentials are in this public packet.

| Meter | Observed unit rate | Conservative run estimate |
| --- | --- | --- |
| E1 LRS Disk | USD 0.30 per disk-month | 8 × 0.30 × 336 / 730 = USD 1.105 |
| Standard SSD operations, E4 LRS Disk Operations meter | USD 0.002 per 10,000 transactions | 8 × 6,800 × 336 / 10,000 × 0.002 = USD 3.656 |
| Standard HDD LRS Snapshots | USD 0.055 per used GB-month | 32 × 0.055 = USD 1.760 |
| Hot LRS Data Stored, first tier | USD 0.0208 per GB-month | 10 × 0.0208 = USD 0.208 |
| Hot writes and list/create-container operations | USD 0.055 per 10,000 | 200,000 / 10,000 × 0.055 = USD 1.100 |
| Hot reads/other operations | USD 0.0044 per 10,000 | 200,000 / 10,000 × 0.0044 = USD 0.088 |
| Calculated subtotal | | USD 7.917, rounded upward |
| Proposed ceiling | | USD 10; approximately USD 2.08 headroom |

The E1 Disk meter is distinct from E1 Disk Mount. This plan uses ordinary single-attached disks, not paid shared-disk extra mounts. The operations estimate conservatively uses the small-tier hourly billable transaction limit, including E1. Confirm its meter mapping against the actual subscription before approval. [Azure managed-disk pricing](https://azure.microsoft.com/en-us/pricing/details/managed-disks/) describes hourly capacity billing, Standard SSD transaction limits, separate shared-mount charges and snapshot billing on used capacity. Do not substitute the smaller mount price for disk capacity.

Disk allocation is costed for all 336 hours. Snapshots and object capacity are costed for a full month despite a shorter run, so deleting compute at day 14 is not assumed to erase retained-data charges. C-08 retention remains a separate decision; if required retention exceeds the reserved month or capacity, revise the budget rather than deleting evidence to meet this estimate.

## Boundaries and approval needed

The USD 10 proposal covers only the listed storage meters. It excludes additional compute/nodes, public IP/load balancer/DNS resources, storage accounts, private endpoints, network transfer, paid logging and production resources. None is implicitly free or authorized. Q1 must account for any incremental transfer/other costs and verify existing compute/network capacity before execution. No pool growth, customer-volume adoption, public application ingress or replacement of application authorization follows from this budget.

Before provisioning, require: accepted financial ceiling and exact resource inventory; current C-03 request/channel/actor; accepted filesystem/storage and protected custody policies; bounded data/fault/run/cleanup plan; confirmed node/attachment capacity; price refresh and Q1 acceptance. The Ops owner monitors allocation, operation and retained-capacity limits, stops new work before a bound is exceeded, and preserves failed/neighbor history. Azure budget alerts alone do not enforce the USD ceiling or authorize cleanup; the execution plan needs admission limits and authorized cleanup/readback.

No resource was created, resized, attached or deleted in preparing this packet. All three PRs remain draft, full Q0 is incomplete and Q1-Q5 are unentered.
