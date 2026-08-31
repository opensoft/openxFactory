# credential-contracts (delta) — add-notebook-hosting-credential-custody

## ADDED Requirements

### Requirement: An operated identity's credential is held in governed custody and reached only by reference
Where the family stands up an OPERATED IDENTITY on a third-party platform, the credential that authenticates it SHALL be held in a governed secret store and SHALL be reached only BY REFERENCE — an opaque secret reference resolved through a binding, never a value carried in a repository, an environment baked into an image, a person's password manager, or a human's memory alone. The existing prohibition on hard-coding an operated identity's credential states what must not happen; this states what must: an operated identity with no declared custody is not governed, it is merely undocumented.

Custody SHALL cover every secret the identity actually needs to authenticate, not the primary factor alone. Where the platform enforces a second factor, that factor's seed is part of the credential set and SHALL be held under the same custody: a password in a vault beside a TOTP seed on someone's phone is a single point of failure wearing governance.

The binding SHALL name the provider, the secret reference, the owner and the rotation policy, following the credential binding-template shape this capability already promotes. Naming a concrete vault and secret in a per-client BINDING INSTANCE is what a binding is for and does not breach the no-hard-coding rule, which binds contract artifacts, lane definitions and domain repositories — the neutral obligation lives in the contract, the concrete estate fact lives in the binding.

Custody SHALL NOT be claimed to deliver automation. Holding a password governs WHO MAY OBTAIN IT and proves who did; it does not by itself make an interactive sign-in unattended, and a custody record MUST NOT be read as evidence that an automated login exists.

#### Scenario: An operated identity is stood up with no declared custody
- **WHEN** an install declares an operated identity whose credential is held in no governed store
- **THEN** the identity is non-conforming — its credential is undocumented rather than governed
- **AND** the remedy is a custody binding, not a note recording where the password is kept

#### Scenario: A second factor is left outside custody
- **WHEN** the platform requires a second factor for the operated identity and only the primary credential is held under custody
- **THEN** the custody is incomplete, because the identity still cannot be authenticated from governed material alone

#### Scenario: A binding names the concrete vault
- **WHEN** a per-client binding instance names its provider, vault, secret reference, owner and rotation policy
- **THEN** that is conforming: the binding is exactly where a concrete estate fact belongs
- **AND** the same values appearing in a contract artifact or lane definition would not be

#### Scenario: Custody is mistaken for automation
- **WHEN** a custody record exists for an identity whose sign-in is an interactive browser flow
- **THEN** the sign-in remains interactive, and any claim that the credential's custody automates it is refused

### Requirement: Each consuming system reaches a shared operated identity through its own binding
Where more than one system authenticates as the SAME operated identity, each consuming system SHALL reach that identity's credential through its OWN binding: its own access identity against the secret store, its own grant, its own rotation visibility, and its own audit trail. One identity MAY be shared; one AUTHORITY SHALL NOT. A system SHALL NOT borrow another system's binding, and SHALL NOT consume the identity through a session another system established.

Per-system bindings are what make the consequential acts separable. With one shared route, revoking either system's access revokes both, the store's access log cannot say which system read the secret, and a compromise of one is indistinguishable from a compromise of the other. Each binding SHALL therefore be revocable on its own, and revoking one SHALL NOT disturb the other's ability to fetch.

WHAT REVOCATION REACHES, STATED HONESTLY, because a shared bearer secret bounds it. Revoking a binding stops that system's FUTURE fetches and nothing more: it cannot un-disclose a password already fetched, and it cannot terminate a session already established with it. Evicting a consumer that has already read the secret requires ROTATING it, and rotation necessarily reaches EVERY consumer of that identity — the one act per-system bindings cannot make independent. A change adopting this requirement SHALL record that cost rather than let per-system bindings read as per-system containment, and SHALL NOT claim an isolation the credential class cannot deliver.

A shared ambient session SHALL NOT be used as a substitute for a second binding. This restates, for operated identities, what this capability already refuses for worker credentials: a refreshable session-state credential is the wrong class to distribute, because an ephemeral copy's refresh silently stales the master. Two systems sharing one live session is that same defect with the copy left implicit.

#### Scenario: A second system needs the same identity
- **WHEN** a second system must authenticate as an operated identity a first system already uses
- **THEN** it is given its own binding — its own access identity, grant, rotation visibility and audit trail
- **AND** it does not reuse the first system's binding or its established session

#### Scenario: One system's access is revoked
- **WHEN** one consuming system's binding is revoked
- **THEN** that system can no longer FETCH the credential, the other system's binding is unaffected, and its lane keeps working
- **AND** the revocation is attributable to exactly one system

#### Scenario: A consumer that already holds the secret must be evicted
- **WHEN** a consuming system has already fetched the shared credential, or already established a session with it, and must be evicted
- **THEN** revoking its binding is insufficient — the credential is rotated, and the rotation reaches every consumer of that identity
- **AND** that shared cost is recorded rather than described as independent revocation

#### Scenario: The access log is asked which system read the secret
- **WHEN** the secret store's access log is examined after a fetch
- **THEN** it names which consuming system's identity performed it, because each has its own

**AMENDED 2026-08-31 — THIS BLOCK'S FIFTH SCENARIO IS STRUCK, NOT RE-SCOPED.**
The scenario "The published binding shape cannot yet express the access identity"
stood here and stands here no longer. AUTHORITY: Brett Heap, this packet's
ratifying owner, consenting to this in-place amendment on 2026-08-31 per
`govern-sibling-added-modified-deltas` `tasks.md` § 6.2, in the same in-session
ruling that routed that packet's OQ-4 as ONE SWEEP. GROUND: the falsified-scenario
clause — "LANDED REALITY CAN FALSIFY THE ADDING CHANGE'S SCENARIO BEFORE ITS
ARCHIVE, and the archive order is not the escape from that" — carried by that
change's `release-realization` delta at
`openspec/changes/govern-sibling-added-modified-deltas/specs/release-realization/spec.md`,
which is RATIFIED (2026-08-31, direct ruling) AND NOT YET CANON, cited at its
change-directory path because its deltas promote only at its own archive.
EVIDENCE: the struck scenario asserted that the promoted binding-template shape
"carries no consumer or access-identity field". It now carries one —
`contracts/schemas/xfactory-credential-contracts.schema.yaml:185-229` declares an
additive optional `consumer:` block with `holder_ref` and `fetch_identity` — cut
and published in `contracts/CHANGELOG.md` § `contract-v2.4 — 2026-08-31`. EVERY
clause of the scenario is falsified by that release: the shape's absence, the
authority being asserted rather than read, and the gap being owed to a successor
that had not arrived. Re-scoping it would leave a narrower false statement rather
than a true one, and the surviving truth — that what the record proves stays
bounded, reconciling a declaration against the store's actual grants remaining a
live-estate act — is already stated by the replacement scenario the successor
carries in its own block. THE SUCCESSOR THAT DISCHARGED THE GAP:
`add-binding-consumer-identity`, merged as PR #516 squash `5e8a33cf` and realized
by the `contract-v2.4` cut in PR #526 `afdf0e88`, whose annotated tag is
published. **THE ARCHIVE ORDER IS UNCHANGED BY THE FALSIFICATION.** This packet
still archives FIRST and the successor's modified block over this requirement
stays held while the title is unpromoted; this amendment is neither licence to invert that order nor licence to
convert that block, which is exactly what the clause authorising it says.

#### Scenario: A shared session is proposed instead of a second binding
- **WHEN** a second system proposes to consume the identity through a session the first system established
- **THEN** it is refused as the wrong credential class, on the same grounds this capability already refuses distributing refreshable session state
