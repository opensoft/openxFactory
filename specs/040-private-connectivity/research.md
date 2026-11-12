# Planning Research: Private connectivity

Status: draft

## Pilot installation and topology

**Decision**: Use a pinned official Headscale release on dedicated Linux VMs. Each managed trust boundary receives one instance, HTTPS control endpoint, policy, keys, SQLite state, and backup scope. The synthetic customer-operated server and the client hosts are separate from the managed control hosts. Choose the exact build and client compatibility matrix at pilot entry.

**Rationale**: A dedicated instance matches the ratified boundary and limits the effect of changes and recovery. The upstream project describes a single-tailnet scope, recommends SQLite, and documents issues with colocating the control server and a tailnet node. [Headscale FAQ](https://headscale.net/stable/about/faq/) · [Official installation](https://headscale.net/stable/setup/install/official/) · [Upgrade and backup](https://headscale.net/stable/setup/upgrade/)

**Alternatives considered**: A shared customer instance would combine administrative and recovery boundaries. A container fleet or redundant control topology adds pilot dependencies that can be assessed with measured workload and recovery results.

## Enrollment, policy, and relay

**Decision**: Initialize an explicit empty grants policy and verify the applied revision before enrolling. Use short-lived single-use tagged keys for workload nodes. Use operator-approved registration for synthetic people. Exercise direct connectivity and an operator-owned embedded DERP relay with the third-party default map explicitly disabled. Qualify production identity, relays, and regional redundancy in their successor plans.

**Rationale**: An absent policy can allow traffic. Headscale provides single-use pre-authentication and tagged workload identity, and routes have separate approval semantics. A deliberately forced relay path tests actual connectivity when direct traffic fails. A single embedded relay shares the instance failure domain and is suitable only for this bounded pilot. [Policy](https://headscale.net/stable/ref/policy/) · [Registration](https://headscale.net/stable/ref/registration/) · [Routes](https://headscale.net/stable/ref/routes/) · [DERP](https://headscale.net/stable/ref/derp/)

**Alternatives considered**: Pilot federation would add an identity integration dependency. A shared relay fleet would need its own access controls and availability design.

## Rollout scope and evidence

**Decision**: Use two synthetic customers and a generic hosted DomainxFactory profile with a mock private service. Use one approved non-production region and a separate customer-site lab. Select the named domain owner and hosted repository before hosted execution. The generic profile qualifies the common onboarding path. Each named domain qualifies its own profile before release.

**Rationale**: The pilot can exercise cross-customer denial, environment separation, direct and relay paths, and application authorization without customer data. The proposed pilot windows are 5 minutes from accepted revocation to observed deny, 60 minutes from recovery start to verified service, and 15 minutes from rollback start to verified recovery of the prior authorized binding. Restore from a backup no older than 24 hours and replay all current revocations before activation. These are planning targets for the lab.

**Alternatives considered**: Starting with a production or clinical deployment adds obligations and dependencies unrelated to proving the shared path. A mock-only run can qualify the interface semantics but cannot prove the hosted product or real-client isolation.
