# lifecycle-notebook-projection (delta) — add-notebook-projection-identity

## ADDED Requirements

### Requirement: The projection's hosting identity is declared at install
An xFactory install SHALL declare which Google identity hosts its NotebookLM projection, as an intake fact of standing that install up rather than an incidental consequence of whoever authenticated the `nlm` CLI first. The declaration SHALL name exactly one of two cases: OPERATOR-HOSTED, a company-owned account belonging to the operating party, or SELF-HOSTED, an individual installer's own personal account. Both cases are legitimate; the second is not a degraded form of the first.

The declared identity SHALL be a Google USER account. This is a platform constraint, not a preference: NotebookLM exposes no API and a provider service account cannot drive its consumer web UI, so no service-principal identity can host a projection at all.

An operator-hosted declaration SHALL name a Google Workspace user account in a domain the operating party controls, and SHALL NOT name a consumer account merely designated as the company's. A consumer account carries a personal recovery path back to one individual, no administrative console, and no enforceable organizational policy — it would be the operator-hosted case wearing the self-hosted case's risk.

An install that declares NOTHING is NONCONFORMING with this requirement — a transition state, not a third case. Every install predating this requirement is in it, so the sync SHALL NOT break on it: it falls back to the CLI's default profile, which is today's behavior. What it SHALL NOT do is present that install as governed. The projection SHALL be reported as carrying no declared hosting identity, and the undeclared state SHALL be reported as unmet rather than as a legitimate configuration, so an implementation and a validator agree about what is expected of it.

#### Scenario: An operating party declares the company account
- **WHEN** an install's intake declares operator-hosted and names a Google Workspace user account in the operating party's own domain
- **THEN** the declaration is valid, and every book, alias and session notebook of that install is created under the named account
- **AND** Opensoft's own install is such a declaration, naming `xFactor001@opensoft.one`

#### Scenario: An individual installer keeps their own books
- **WHEN** a person installs the system for themselves and declares self-hosted against their own personal Google account
- **THEN** the declaration is valid and complete, no company account is implied, and no share-approval governance obligation attaches

#### Scenario: A consumer account is offered as the company account
- **WHEN** an operator-hosted declaration names a consumer Google account rather than a Workspace user in a controlled domain
- **THEN** the declaration is refused, naming the missing administrative control rather than the account's label

#### Scenario: A service account is offered as the hosting identity
- **WHEN** a declaration names a provider service account or any non-user principal
- **THEN** the declaration is refused on the platform constraint: NotebookLM has no API and the identity could never drive the projection

#### Scenario: An install has not declared yet
- **WHEN** no hosting identity is declared for an install
- **THEN** the sync runs under the CLI's default profile as it does today, rather than breaking
- **AND** the install is reported as NOT MEETING this requirement — a transition state, never a third legitimate case

### Requirement: Access to the projection is shared out from the hosting account, and each share act is recorded
Where an install declares the operator-hosted case, individual users SHALL reach the projection only through an explicit share-out FROM the hosting account, and SHALL NOT each authenticate independently against the hosting account's own credentials. A shared login is not an access model: it defeats attribution, cannot be revoked per person, and is exactly the posture this declaration exists to retire.

A pending share request SHALL be decided by a designated company-policy actor as a GOVERNED ACT, in the hosting account's own interface, and SHALL NOT be left to whoever happens to read the account's mail. The decision SHALL be recorded whether it grants or denies.

The record of a granted share act SHALL BE the share-out roster entry itself, not a separate audit trail beside a list. Approving a request writes or updates the roster; denying one is recorded in the same lane.

A roster entry SHALL carry the hosting account, the person, the book or alias, the role, the grant time and the granting actor. Its UNIQUENESS SHALL be keyed on the stable scope-and-principal triple `(hosting_account, user, book_or_alias)`, with `role`, `granted_at` and `granted_by` held as ATTRIBUTES of that entry rather than as parts of its key. A re-approval, a role change, or a grant by a different actor therefore UPDATES the one live entry instead of creating a second: a roster that is the record of current access cannot simultaneously assert a stale grant and a current one for the same person on the same book. Superseded decisions SHALL be retained as history rather than as competing live entries.

The grantee SHALL be part of the key. That is the whole structural difference from the client-identity roster, whose uniqueness tuple omits the grantee and therefore collides when one scope is granted to two people.

An entry SHALL reference a governed persona wherever the identity-brokering family resolves one for that human, falling back to a bare address only where no persona resolves.

The share-out roster SHALL be its own artifact and SHALL NOT be carried by the client-identity roster, whose uniqueness key admits one principal against many scopes while a share-out list is the transposed shape — one scope against many principals.

Detection and relay of pending requests MAY be automated if and when the platform offers a surface for it; the approval SHALL remain a governed human act either way. No obligation in this requirement depends on an administrative or sharing API that NotebookLM does not currently expose.

#### Scenario: A share request is approved
- **WHEN** a person requests access to a book hosted by a declared operator-hosted account, and the designated company-policy actor approves it
- **THEN** the share is granted from the hosting account
- **AND** a share-out roster entry records the account, the person, the book or alias, the role, the grant time and the granting actor
- **AND** the entry references that person's governed persona where one resolves

#### Scenario: A share request is denied
- **WHEN** the designated actor denies a pending request
- **THEN** the denial is recorded in the same lane as approvals, rather than leaving the request to expire unrecorded

#### Scenario: Two people are granted the same book
- **WHEN** two different people are granted access to one book on one hosting account
- **THEN** both entries stand as distinct roster records, because the grantee is part of the key

#### Scenario: An existing grantee's access is re-decided
- **WHEN** a person already holding a recorded grant on a book is re-approved, has their role changed, or is granted again by a different actor
- **THEN** the existing entry is UPDATED, carrying the new role, grant time and granting actor
- **AND** no second live entry is created, so the roster never asserts a stale grant beside the current one
- **AND** the superseded decision is retained as history

#### Scenario: Individual authentication against the hosting account is attempted
- **WHEN** a user is given the hosting account's own credentials instead of a share
- **THEN** that is a violation of this requirement, not an alternative access route

### Requirement: A hosting-account migration re-derives, proves parity, then retires the originals by recorded act
Moving a projection from one hosting account to another SHALL be performed as a RE-DERIVATION, not as a data migration: membership is always derived from `Status:` headers and never hand-curated, so the books under the new account are reconstructed from the corpus rather than copied.

Parity SHALL be proven BEFORE anything is retired, and SHALL be established against the CORPUS SCAN rather than against the legacy books, which are the very artifact whose fidelity is in question. Parity SHALL consist of per-book title-set equality plus a union reconciliation against the corpus scan, followed by a final dry run showing zero pending additions, deletions or updates.

The migration SHALL account for the SESSION namespace explicitly. A lifecycle-book reconciliation does not create session notebooks, so every live `xf-session-*` notebook SHALL be re-created under the new account — through a bulk migration mode or per-session runs — before the old account is retired. A migration that moves the lifecycle books alone leaves live sessions hosted on the account being abandoned.

The migration SHALL replace each book's workspace record rather than merely retiring it. A re-created book keeps its derived key and therefore its record id, but carries a NEW provider notebook id; a registration step that refuses to overwrite an existing record, combined with retiring that record, would leave the new book with no active workspace record at all. The replacement SHALL be explicit and SHALL leave exactly one active record per live book.

Only once parity holds SHALL the previous account's books be RETIRED BY RECORDED ACT — archive-renamed, and their aliases DELETED rather than repointed. Retirement SHALL be declared, never implicit: a book left merely untouched is a book no one has judged, which is how the shared Ideation book reached its source cap before anyone called it old.

The retirement SHALL NOT retire the workspace record the replacement step just made current. Because the record id is derived from the book's key and that key is unchanged, the replaced record IS the live book's registration; retiring it would reproduce the unregistered-book failure the replacement exists to prevent. What is retired is the legacy PROVIDER NOTEBOOK, and the retirement is preserved in the recorded act and in the record's own history. Only where a migration leaves a genuinely SEPARATE legacy record — a distinct record id, as the 2026-08-10 per-repo split produced — SHALL that record be retired in place.

#### Scenario: The lifecycle books are re-derived under a new account
- **WHEN** an install's declared hosting identity changes and the sync next applies
- **THEN** the lifecycle books are re-created under the newly declared account from the corpus, as a re-derivation

#### Scenario: Parity is claimed against the legacy books
- **WHEN** a migration proposes to prove parity by comparing the new books against the old ones
- **THEN** that is insufficient: parity is established against the corpus scan, with a final zero-pending dry run

#### Scenario: Sessions are live at cutover
- **WHEN** any branch session is live when the hosting account changes
- **THEN** each live session's notebook is re-created under the new account before the old account is retired
- **AND** a lifecycle-only run is not accepted as having migrated them

#### Scenario: A re-created book collides with its own workspace record
- **WHEN** a re-created book resolves to an existing record id holding a different provider notebook id
- **THEN** the record is explicitly replaced, leaving one active record for the live book
- **AND** retiring the old record without that replacement is refused as leaving the book unregistered

#### Scenario: The previous account's books are retired
- **WHEN** parity has been proven and the new account's books are live
- **THEN** the previous books are archive-renamed and their aliases deleted rather than repointed
- **AND** the retirement is recorded as an act rather than left implicit

#### Scenario: The retirement is asked to retire the replacement record
- **WHEN** the retirement step would retire a workspace record whose id the replacement step reused for the live book
- **THEN** it is refused, because that record is the live book's registration and retiring it leaves the book unregistered
- **AND** the legacy provider notebook is retired instead, with the act preserved in the record's history

#### Scenario: A migration leaves a genuinely separate legacy record
- **WHEN** the migration produces a successor under a NEW record id, leaving the legacy record distinct and unreferenced
- **THEN** that legacy record is retired in place, as the 2026-08-10 split precedent did

## MODIFIED Requirements

### Requirement: Projection implementation ownership
`openxFactory` SHALL own this projection contract, the workflow
documentation, and the conforming sync implementation
(`scripts/sync-notebooklm-books.py`). Book identity, charter text, title
prefixes, and chat framing SHALL be treated as contract conformance, not
implementation preference.

The sync SHALL run under the install's DECLARED hosting identity, selecting the `nlm` CLI profile bound to that identity rather than taking the tool's default profile. Which account the projection is created in is contract conformance, not an incidental property of the host the sync happens to run on: the CLI is profile-aware, so the selection is between existing mechanisms, and an implementation that cannot name the account it is writing to cannot claim conformance.

#### Scenario: The sync implementation is modified

- **WHEN** the sync implementation changes book definitions, prefixes, charter, exclusions, or chat framing
- **THEN** the change MUST be preceded by an OpenSpec delta to this capability

#### Scenario: A workspace names the sync manager

- **WHEN** a lifecycle notebook declares its `managed_by` implementation
- **THEN** the declared path resolves inside openxFactory, and the invocation is run from the workspace root against every pinned repo

#### Scenario: The sync runs for an install with a declared hosting identity

- **WHEN** the sync runs against an install that declares a hosting identity
- **THEN** every CLI invocation it makes is bound to that identity's profile
- **AND** a run that cannot resolve the declared identity's profile fails rather than silently falling back to the default profile

### Requirement: The session namespace is reconciled against live sessions
The sync SHALL provide a RECONCILIATION mode over the `xf-session-` notebook namespace that retires the notebook of every session that no longer exists, because a branch session's notebook is bound to a LIVE session and a session can end without either governed ending — a probe or a crash-residue cleanup removes a worktree and a branch directly, so no abandon runs and no retirement is recorded. Without reconciliation such a notebook survives its session indefinitely on the hosting account, holding quota and misstating the set of live sessions to every later reader.

Dead SHALL be established FORWARD, never by inverting a title. The alias derivation is lossy — it strips the `draft/` prefix and lowercases — so a notebook title cannot be resolved back to a `(repository, branch)` key. The mode SHALL compute the alias of every LIVE session, using the same joint worktree-and-branch liveness signal the session bootstrap uses, and SHALL treat an `xf-session-` notebook that matches no live session's alias as dead. A notebook matching a live session's alias SHALL never be retired.

Liveness SHALL be sought across EVERY WORKTREE of each session repository, not only its canonical checkout. A session's worktree container is keyed on the checkout the session was opened FROM, and sessions are routinely opened from a feature worktree, so a run that asks only the canonical checkout finds no sessions there — a legitimate answer for that checkout, and indistinguishable from the sessions living in another worktree of the same repository. The repository's own worktree list is what makes the enumeration completable, and a run that cannot read it SHALL treat that as an error rather than as an answer.

The mode SHALL FAIL CLOSED on incomplete knowledge. A session repository that cannot be enumerated — an absent checkout, a git failure, an unreadable worktree list, an unreadable session container — is indistinguishable from a repository whose sessions have all ended, and the difference cannot be recovered after a retirement. Any repository the run cannot enumerate SHALL refuse the whole reconciliation, naming the repository and the reason, and SHALL retire nothing.

Where the run resolves NO session repositories in scope at all, it SHALL retire nothing: a workspace carrying none of the repositories a session notebook could belong to has no standing to judge one, so pointing the mode at the wrong root is inert rather than destructive.

The mode SHALL be scoped to the session repositories of the workspace it is run against. One hosting account serves every workspace of its install, so a session notebook whose repository segment names a repository this workspace does not carry belongs to another workspace's sessions; such a notebook SHALL be reported as out of scope and SHALL NOT be retired. This scoping rule is unchanged by the hosting identity becoming declared: what was previously true of an undeclared shared account is true of a declared one, and the reconciliation SHALL be performed within the declared account rather than across accounts.

The mode SHALL report by default and act only when application is requested, and SHALL retire through the same adapter operation the governed endings use rather than a scratch-namespace delete, so the session-prefix and key-derived-title guards apply identically. The report SHALL state, for each dead notebook, how many sources a retirement would discard, because a notebook carrying hand-added sources is the one case where retirement loses something a human may want first.

#### Scenario: A session torn down outside a governed ending is reconciled
- **WHEN** the reconciliation runs against a workspace where an `xf-session-` notebook matches no live session's alias
- **THEN** the notebook is reported as dead, naming its title and the number of sources a retirement would discard
- **AND** with application requested it is retired through the session retire operation
- **AND** the run reports the retirement as its own act rather than as a governed ending

#### Scenario: A live session's notebook is never retired
- **WHEN** the reconciliation runs while a session is live
- **THEN** that session's notebook matches a live alias and is left untouched in both report and apply modes

#### Scenario: A session opened from a feature worktree is live
- **WHEN** a session's worktree container belongs to a FEATURE worktree of a session repository rather than to that repository's canonical checkout
- **THEN** the reconciliation still finds it live and leaves its notebook untouched
- **AND** a run that examined only the canonical checkout MUST NOT report it dead

#### Scenario: No session repository in scope retires nothing
- **WHEN** the reconciliation resolves no session repositories at all for the workspace it is run against
- **THEN** every session notebook is out of scope and nothing is retired

#### Scenario: A repository that cannot be enumerated refuses the run
- **WHEN** any session repository in the workspace cannot be enumerated for live sessions
- **THEN** the reconciliation refuses, names the repository and the reason, and retires nothing
- **AND** the refusal is reported as a refusal rather than as an empty result

#### Scenario: Another workspace's session notebook is out of scope
- **WHEN** an `xf-session-` notebook names a repository this workspace does not carry
- **THEN** it is reported as out of scope and is never retired

#### Scenario: An adapter without the retire operation refuses
- **WHEN** application is requested against an adapter exposing no session retire operation
- **THEN** the run refuses loudly and retires nothing, rather than reporting a retirement it did not perform
