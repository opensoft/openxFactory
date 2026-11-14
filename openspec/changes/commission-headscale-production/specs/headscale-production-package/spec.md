# Commission the supported Headscale package

Status: ratified
Ratified: 2026-11-14 by Brett Heap, through [commission-headscale-production](../../proposal.md).

## Purpose

Provide opensoft/Headscale-Install's production behavior and verifiable source, release and qualification boundary while retaining neutral private-connectivity and rollout authority requirements.

## ADDED Requirements

### Requirement: Supported package and independent local operation

The package SHALL use explicit immutable supported server/helper inputs, dedicated instance state and deny-by-default policy before enrollment. Customer-operated install-new/connect-existing and unbound use MUST remain independent of Hosted Headscale entitlement.

#### Scenario: Supported package and independent local operation succeeds within scope
- **WHEN** an authorized customer selects a supported local package
- **THEN** the actual local path retains independent operation

#### Scenario: Supported package and independent local operation refuses invalid scope or proof
- **WHEN** a mutable or unqualified input or missing policy is supplied
- **THEN** readiness is refused without pilot fallback

### Requirement: Verified endpoint identity and renewal

The package SHALL verify actual HTTPS identity, hostname/trust and applicable renewal/reachability controls. A caller flag MUST NOT bypass verification or manufacture readiness.

#### Scenario: Verified endpoint identity and renewal succeeds within scope
- **WHEN** the actual endpoint controls pass in the approved scope
- **THEN** their observed results remain bound to that target/candidate

#### Scenario: Verified endpoint identity and renewal refuses invalid scope or proof
- **WHEN** identity, expiry, renewal or reachability proof is invalid or absent
- **THEN** the instance remains unready

### Requirement: Fenced recovery with current revocations

Recovery SHALL fence the previous writer, restore in quarantine and reconcile authoritative current revocations independently of an old snapshot before activation. Rollback MUST reauthorize original prior subjects and preserve neighbors.

#### Scenario: Fenced recovery with current revocations succeeds within scope
- **WHEN** a qualified snapshot is restored under current authority
- **THEN** writer/state/revocation checks precede activation

#### Scenario: Fenced recovery with current revocations refuses invalid scope or proof
- **WHEN** a stale writer or revoked prior binding is encountered
- **THEN** activation and rollback fail with original cleanup subjects retained

### Requirement: Supported release and truthful qualification

Publication SHALL retain actual collected source/CI and immutable supported candidate/provenance readback. Source or fixture evidence MUST NOT satisfy actual-client/target observations required by rollout gates.

#### Scenario: Supported release and truthful qualification succeeds within scope
- **WHEN** the exact source candidate is released through the accepted process
- **THEN** its artifact/dependency identity can be independently verified

#### Scenario: Supported release and truthful qualification refuses invalid scope or proof
- **WHEN** only a pilot fixture or source pass exists
- **THEN** no customer or production qualification is inferred
