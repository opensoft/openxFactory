# worker-enrollment-broker — Spec Delta

## ADDED Requirements

### Requirement: One enrollment point serves both estates with two authentication modes
A governed worker host SHALL become a worker through exactly one enrollment exchange, which MUST accept two authentication modes and no others: a **fleet host** authenticating with a per-host identity provisioned in the managed-platform key vault, and a **volunteer workstation** authenticating as the ENGINEER through an interactive device-code flow. The request and response shapes MUST be identical across modes — the estate difference is who authenticates and where the host manifest comes from, never a second protocol. A volunteer-workstation enrollment MUST NOT cause any standing secret to be written to that machine, and a per-host fleet identity SHALL be broker ACCESS only and MUST NOT carry token-minting authority.

#### Scenario: A fleet host enrolls with its per-host identity
- **WHEN** an Intune-managed host presents the per-host identity provisioned for it in the managed-platform key vault
- **THEN** the broker authenticates it as a fleet-estate enrollment
- **AND** the resulting grant is bound to that host identity

#### Scenario: A volunteer workstation enrolls as the engineer
- **WHEN** an engineer runs the installer on an unmanaged workstation and completes the interactive device-code flow
- **THEN** the broker authenticates the ENGINEER as the enrolling subject and records the workstation as the temp estate
- **AND** no standing secret is written to the workstation — the device-code identity is used for the exchange and for renewals, never escrowed on the machine

#### Scenario: An unauthenticated or ineligible enrollment is refused
- **WHEN** an enrollment request arrives with no recognized fleet identity and no completed device-code authentication, or from a subject outside the eligibility policy
- **THEN** the broker refuses, emits a refusal audit record naming the reason, and issues no lease and no registration token

### Requirement: Enrollment grants a lease and a short-lived registration token
A successful enrollment SHALL return a LEASE — carrying a lease id, an expiry (TTL), a trust tier, and the runner group the worker is bound to — together with a runner registration token that MUST be short-lived and single-use. The lease, not the registration, is the record of authority: the token exists only to complete the runner's initial registration and MUST NOT be persisted by the host, written to any manifest or log, or reused for a second registration.

#### Scenario: A grant carries lease and token together
- **WHEN** the broker approves an enrollment
- **THEN** the response carries the lease (id, expiry, trust tier, runner group) and a short-lived registration token
- **AND** the host uses the token immediately to register and retains only the lease

#### Scenario: The token is never retained
- **WHEN** the host has completed runner registration
- **THEN** the token value exists in no file, manifest, log line, or audit record on the host or in the broker

#### Scenario: An expired token cannot register
- **WHEN** a host presents a registration token after its short lifetime has elapsed
- **THEN** registration fails and the host MUST re-enroll rather than reuse or extend the token

### Requirement: Token-minting authority is held only by the broker
The administration-tier GitHub App key that mints runner registration and runner REMOVE tokens SHALL be held only by the broker, under the canonical `credential-contracts` custody shapes (vaulted key custody binding, short-lived workflow-scoped runtime grants, human and domain approval before grant issuance, an audit record per action). No worker host, installer package, host manifest, escrow, or scheduled task MUST hold or be able to derive that authority, and remove-token brokering for drift repair SHALL ride the same authority and the same audit path as registration.

#### Scenario: Hosts hold no minting credential
- **WHEN** a fully enrolled worker host is inspected — files, manifests, escrows, task definitions, environment
- **THEN** no administration-tier App key or derived credential is present anywhere on it

#### Scenario: Drift repair brokers a remove token
- **WHEN** a host must deregister a stale or orphaned runner registration
- **THEN** it requests a remove token from the broker against its lease, receives a short-lived single-use token, and the request and its outcome are audited like an enrollment

#### Scenario: A host attempting to mint directly is refused
- **WHEN** any component other than the broker attempts to call the token-minting API path with an identity it holds locally
- **THEN** it has no credential capable of the call, and the attempt is visible as a failed call rather than a silent success

### Requirement: Leases renew on a cadence and every renewal response carries the version floor
A worker's supervisor SHALL renew its lease on a declared cadence before expiry, and every renewal response MUST carry the current minimum app version (the floor) and the lease state the broker has decided. Renewal is the only mechanism that extends authority: a lease that is not renewed within its TTL plus the declared grace window expires, and an expired lease MUST NOT be repaired by anything on the host.

#### Scenario: A healthy worker renews and stays current
- **WHEN** a worker at or above the floor renews before its lease expires
- **THEN** the broker extends the lease, returns the current floor and an active lease state, and the worker continues to execute lane work

#### Scenario: Missed renewals expire the lease
- **WHEN** a worker fails to renew for longer than its TTL plus the declared grace window (for example, an offline laptop)
- **THEN** the lease expires, the worker holds no authority, and returning online requires a successful renewal or a fresh enrollment

#### Scenario: The floor travels on every renewal
- **WHEN** the platform raises the minimum app version
- **THEN** the next renewal response every worker receives carries the raised floor, whether or not that worker is affected by it

### Requirement: A below-floor or lease-less worker fails closed
A worker whose app version is below the floor, or whose lease has been refused, expired, or revoked, MUST stop its runner services and MUST NOT execute lane work until it is updated and holds a valid lease again. The worker SHALL report the reason in its heartbeat — `update_required` for the version floor, the refusing lease state otherwise — so the condition is legible off-machine rather than inferred from silence. The platform SHALL NOT rely on any update machinery reaching an unmanaged workstation; denial of work is the enforcement.

#### Scenario: Raising the floor past a running worker stops it
- **WHEN** the floor is raised above a volunteer workstation's installed app version and its next renewal returns that floor
- **THEN** the worker's runner services stop, its heartbeat reports `update_required`, and it takes no further jobs

#### Scenario: Recovery is an update, not an override
- **WHEN** the engineer re-runs the installer at or above the floor and the worker renews
- **THEN** the lease returns to active, runner services restart, and the heartbeat clears `update_required`
- **AND** no local flag, retry, or configuration edit on the host can restore work without the version being at or above the floor

#### Scenario: An unreachable worker still loses authority
- **WHEN** a worker cannot be reached by any administrative path
- **THEN** its authority still ends at lease expiry, because authority is granted forward by renewal rather than removed after the fact

### Requirement: Revocation is expressed as refusing the next renewal
Revoking a worker SHALL be performed by marking its lease revoked so the next renewal is REFUSED, and MUST NOT depend on reaching the host, deleting a registration first, or an engineer's cooperation. The revocation and each subsequent refusal MUST be audited, and a revoked worker MAY additionally have its runner registration removed through brokered remove-token repair.

#### Scenario: A revoked worker stops within one cadence plus grace
- **WHEN** an operator revokes a lease
- **THEN** the worker's next renewal is refused, the worker fails closed, and the elapsed time is bounded by the renewal cadence plus the grace window

#### Scenario: Revocation needs no host access
- **WHEN** the machine is powered off, off-network, or in an engineer's home
- **THEN** the revocation still takes effect at the refused renewal or at lease expiry, whichever comes first

#### Scenario: Re-enrollment after revocation is a fresh decision
- **WHEN** a revoked host attempts to enroll again
- **THEN** the request is evaluated as a new enrollment against eligibility and approval policy, and the prior revocation is visible in the audit trail

### Requirement: Runner package policy splits by estate
A fleet enrollment SHALL be served a HARD-PINNED runner package — an exact version and sha256 with runner self-update disabled — whose bumps ride manifest rollouts through the managed delivery plane, while a temp-worker enrollment SHALL run with runner self-update ENABLED and its observed runner version recorded as informational only. A temp worker MUST NOT fail closed for runner-binary drift alone; the fail-closed control on volunteered hardware is the app-version floor.

#### Scenario: A fleet host gets the pin
- **WHEN** a fleet host enrolls
- **THEN** its grant names the pinned runner version and sha256 with self-update disabled, and the host verifies the digest before installing

#### Scenario: A volunteer workstation self-updates its runner
- **WHEN** a temp worker's runner binary is superseded upstream
- **THEN** the runner updates itself, the newly observed version is reported and recorded as informational, and the lease is unaffected

#### Scenario: A fleet runner bump is a manifest rollout
- **WHEN** the pinned runner version changes
- **THEN** the change is delivered as a manifest rollout through the managed delivery plane, not by a broker instruction to a running host

### Requirement: Temp workers are segregated by runner group, labels, and trust tier
A volunteer-workstation lease SHALL bind the worker to a dedicated temp runner group with temp labels and MUST NOT bind it into a standing execution-lane runner group. Every lease SHALL carry a trust tier, and a lane SHALL be able to decline dispatch to a tier — so sensitive work never reaches volunteered hardware, by policy rather than by convention.

#### Scenario: Enrollment places a volunteer in the temp group
- **WHEN** a volunteer workstation enrolls
- **THEN** its grant names the dedicated temp runner group and temp labels, and its trust tier marks it as volunteered hardware

#### Scenario: A request to join a standing lane is refused
- **WHEN** an enrollment request from the temp estate asks for a standing execution-lane runner group
- **THEN** the broker refuses the request rather than downgrading it silently, and the refusal is audited

#### Scenario: A lane excludes volunteered hardware
- **WHEN** a lane declares that it accepts no volunteered-hardware workers
- **THEN** no temp-tier worker is dispatched work from that lane, and the exclusion is expressed against the lease's trust tier rather than by enumerating hosts

### Requirement: Every enrollment decision is audited and no token value is ever recorded
Every enrollment, renewal, refusal, and revocation SHALL emit an audit record carrying the authenticated subject, the host and estate, the decision and its reason, the lease id, the trust tier, the runner group, the observed app version and the floor in force, and a reference to the policy version applied. The record MUST NOT contain any registration token, remove token, key material, or secret value, in any field, at any time — redaction is a property of the record shape, not of a logging convention.

#### Scenario: A refusal is recorded with its reason
- **WHEN** the broker refuses an enrollment or a renewal
- **THEN** an audit record is written naming the subject, the decision, and the specific reason (ineligible subject, below floor, revoked lease, expired lease)

#### Scenario: Records carry no token values
- **WHEN** any audit record produced by an enrollment, renewal, refusal, or revocation is validated
- **THEN** it contains no token, key, or secret value, and a record presenting one fails validation

#### Scenario: The audit trail is the evidence for a revocation
- **WHEN** an operator must show when a worker lost authority and why
- **THEN** the revocation record and the subsequent refusal records establish it without reference to host-side logs

### Requirement: The contract publishes as a versioned additive bundle its realizations pin
The enrollment, grant, lease, renewal, policy, and audit-record schemas SHALL publish as a versioned additive contract bundle per the contract-versioning policy, with a canonical validator and positive and negative fixtures, so the broker service, the host-app integration, and the managed-platform policy each validate against a PINNED release rather than a copied shape.

#### Scenario: Realizations pin a release
- **WHEN** the broker service, the Omnigent-Install integration, or the OpsxFactory policy instance adopts the contract
- **THEN** it names the pinned bundle release it was built against, and validates its own artifacts with the canonical validator

#### Scenario: Positive and negative fixtures both hold
- **WHEN** the canonical validator runs over the packaged examples
- **THEN** each positive example passes and each negative example fails with the finding for the rule it violates
