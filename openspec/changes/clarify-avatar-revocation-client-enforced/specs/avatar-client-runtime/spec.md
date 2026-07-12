## MODIFIED Requirements

### Requirement: Leased control channel and deterministic recovery
The control transport SHALL be authenticated WSS carrying commands, events,
snapshots, heartbeats, and revocation. The client SHALL send a heartbeat
every declared interval carrying session epoch and last-applied sequence;
each server heartbeat response SHALL extend the lease, return the new lease
expiry, and MAY carry a fresh scoped reconnect credential bound to session,
epoch, and client instance. Every media-capable profile SHALL set
`heartbeat_interval_ms` greater than zero and no greater than 5,000 and SHALL
set initial lease expiry no later than 10,000 milliseconds after grant
issuance. Each heartbeat response MAY extend lease expiry to no later than
10,000 milliseconds after that response. Profiles MAY use stricter values but
MUST NOT raise either neutral ceiling. Control health SHALL be degraded after
one missed response and lost after the profile-declared count or lease expiry,
whichever occurs first, evaluated against the client's monotonic clock.
Command results serve as acknowledgements; per-message acknowledgement frames
MUST NOT be required.

Loss of control SHALL immediately disable governed commands and pending
confirmations and stop capture and playback; there is no speech grace
interval. Lease expiry SHALL close the media leg even while provider
connectivity remains healthy. A dropped control connection SHALL reconnect
with the newest reconnect credential while the lease remains valid;
otherwise the client starts over with AVC-01.

Revocation SHALL be client-enforced: on any revocation trigger — an explicit
revoke, control loss, or lease expiry — the client SHALL disable governed
commands and pending confirmations, stop capture and playback, close the media
leg, and issue the provider revocation request within 5,000 milliseconds of the
trigger, evaluated against the client's monotonic clock. This client-side stop
is the revocation guarantee. The provider-side authoritative termination
confirmation MAY be eventually-consistent and lag the client-side stop, and
MUST NOT be the sole evidence that revocation occurred; a profile whose provider
cannot positively confirm termination within the bound SHALL still satisfy this
requirement through the client-side stop and the accepted revocation request,
and SHALL record the provider settle behavior as evidence.

Session lifecycle, control health, media state, and workflow projection
SHALL be separate authoritative axes with a transition registry declaring
allowed predecessors, terminal states, and authority sources; presentation
mode SHALL remain client-local. Provider reconnect SHALL create a new media
leg under the same logical session only while the lease is valid; pending
consequential commands SHALL reconcile by command ID before any retry.
Terminal, revoked, expired, completed, and abandoned sessions MUST NOT
resume as active.

#### Scenario: Control channel is lost while media remains connected
- **WHEN** the declared count of heartbeat responses is missed
- **THEN** the client MUST set control health to lost, disable governed commands and confirmations, and stop capture and playback no later than lease expiry

#### Scenario: A media profile exceeds the neutral lease ceilings
- **WHEN** a profile requests a heartbeat interval above 5,000 milliseconds, an initial lease beyond 10,000 milliseconds after grant issuance, or a renewal beyond 10,000 milliseconds after its heartbeat response
- **THEN** profile validation and session preflight MUST fail before a provider call is created

#### Scenario: Control connection drops transiently
- **WHEN** the WSS drops while the lease remains valid
- **THEN** the client MUST reconnect with the newest scoped reconnect credential and resume from its last-applied sequence via snapshot recovery

#### Scenario: Pending action exists during reconnect
- **WHEN** a disconnect occurs after command acceptance but before its outcome is displayed
- **THEN** recovery MUST query the recorded command result by command ID and MUST NOT issue a new external action

#### Scenario: User pauses and resumes
- **WHEN** a non-terminal session is paused and resumed within policy limits
- **THEN** capture and playback MUST stop while paused and resume from an authoritative snapshot without creating a second workflow

#### Scenario: Revocation is client-enforced within the bound
- **WHEN** a session is explicitly revoked, control is lost, or the lease expires
- **THEN** the client MUST disable governed commands and confirmations, stop capture and playback, close the media leg, and issue the provider revocation request within 5,000 milliseconds of the trigger
- **AND** the provider-side authoritative termination confirmation MAY settle later and MUST NOT be the sole evidence that revocation occurred, provided the client-side stop and the accepted revocation request completed within the bound
