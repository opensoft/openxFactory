# client-identity-roster — add-client-identity-roster deltas

## ADDED Requirements

### Requirement: Roster axis is workload by authority class
Governed identities in a client tenant SHALL be enumerated on exactly one
axis: one identity per (workload, authority class) pair, where authority
class is one of `observe`, `mutate`, or `destructive`. No governed identity
SHALL span more than one workload, and none SHALL combine authority classes.
A single identity holding authority across workloads is prohibited because
the identity is the unit of grant for every provider-side scoping mechanism,
so a cross-workload identity forces the broadest available permission in
every workload it touches.

#### Scenario: A cross-workload identity is proposed
- **WHEN** a roster declares one identity holding authority in two or more workloads
- **THEN** the roster is invalid and the finding names each workload the identity spans

#### Scenario: Read and mutate authority are combined
- **WHEN** a roster entry declares both `observe` and `mutate` authority on one identity
- **THEN** the roster is invalid and the finding names the pair that must be split

#### Scenario: A workload is governed for observation only
- **WHEN** a domain has ratified an observation capability for a workload but no mutating capability
- **THEN** the roster carries only that workload's `observe` entry
- **AND** no `mutate` or `destructive` entry for that workload exists

### Requirement: Governed identities are single-tenant and client-resident
Governed identities SHALL be registered as single-tenant identities resident
in the client's own tenant, so the client is the blast-radius unit for
identity compromise. A multi-tenant identity resident outside the client
tenant SHALL NOT be used for a governed capability unless a ratified
exception declares it, and that exception SHALL carry a blast-radius
analysis stating that one credential set spans every consenting client.

#### Scenario: A multi-tenant identity is proposed without an exception
- **WHEN** a roster entry declares an identity resident outside the client tenant and cites no ratified exception
- **THEN** the roster is invalid and the finding names the missing exception

#### Scenario: A ratified multi-tenant exception exists
- **WHEN** a roster entry cites a ratified multi-tenant exception
- **THEN** the entry MUST reference that exception's blast-radius analysis
- **AND** the analysis MUST state the cross-client credential span explicitly

### Requirement: Workload admission and achieved scope are declared
Each roster entry SHALL declare both the provider-side admission act that
makes the identity usable in that workload (the second key, performed in the
workload's own administrative surface) and the scope that admission act
actually achieves. Provider consent alone SHALL NOT be recorded as
sufficient for workload access. Where the achieved scope is broader than the
governed blast-radius unit the entry SHALL declare the excess and name the
gate obligation that enforces the narrower bound, because a bound the
credential does not enforce is enforced only by logic.

#### Scenario: An entry records consent but no admission act
- **WHEN** a roster entry declares provider consent and omits the workload-side admission act
- **THEN** the entry is invalid and the finding states that consent is not admission

#### Scenario: An admission mechanism offers no scope selector
- **WHEN** an admission act achieves a scope broader than the governed blast-radius unit
- **THEN** the entry MUST declare the excess
- **AND** the entry MUST name the gate obligation that enforces the narrower bound
- **AND** the narrower bound MUST NOT be described as enforced by the credential

#### Scenario: A previously structural bound becomes logical
- **WHEN** an admission act widens an identity's reach so that a bound formerly enforced by the credential is no longer enforced by it
- **THEN** the roster records the transition from structural to logical enforcement as a declared change, never as an unstated condition

### Requirement: Every entry traces to a ratified capability
Every roster entry SHALL name the ratified capability that justifies the
identity's existence and authority class. An identity observed in a client
tenant with no corresponding roster entry, or a roster entry naming no
ratified capability, SHALL be reported as drift. Mutation and destructive
entries SHALL come into existence only when their capability is ratified, so
the client tenant's identity footprint remains a projection of ratified
governance.

#### Scenario: An identity exists with no ratified capability behind it
- **WHEN** an identity is observed in a client tenant and no roster entry names a ratified capability for it
- **THEN** the check reports drift naming the identity and the absent justification

#### Scenario: A capability is ratified with no roster entry
- **WHEN** a domain ratifies a capability requiring client-tenant authority and the roster declares no entry for it
- **THEN** the check reports the gap naming the capability

### Requirement: Identity drift detection is report-only
Drift detection over client-tenant identities SHALL be report-only: it SHALL
NOT create, modify, widen, narrow, or remove any identity, permission, or
admission, and a drift finding SHALL NOT trigger automated remediation.
Identity and permission mutations SHALL remain human acts recorded as their
own governed decisions.

#### Scenario: Drift is detected
- **WHEN** the check finds an identity, permission, or admission that diverges from the roster
- **THEN** it records the finding with the roster value and the observed value
- **AND** it performs no mutation of any kind

#### Scenario: Remediation is desired
- **WHEN** a drift finding warrants a change to a client-tenant identity
- **THEN** the change is performed as a separate human-authorized act with its own record

### Requirement: The roster composes across domain factories
The roster for a client SHALL be per-client and SHALL span every domain
factory holding identities in that client's tenant, with each domain
declaring its own entries against the neutral shape. Two entries claiming
the same identity, or two entries declaring the same (workload, authority
class) pair for one client, SHALL be reported as findings.

#### Scenario: Two domains hold identities in one client tenant
- **WHEN** two domain factories each declare entries for the same client
- **THEN** the client's roster contains both domains' entries under one per-client record

#### Scenario: Two domains claim overlapping authority
- **WHEN** two entries for one client declare the same (workload, authority class) pair
- **THEN** the check reports the overlap naming both domains and the pair
