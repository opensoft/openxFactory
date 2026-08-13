# lifecycle-notebook-projection

## ADDED Requirements

### Requirement: The session namespace is reconciled against live sessions
The sync SHALL provide a RECONCILIATION mode over the `xf-session-` notebook namespace that retires the notebook of every session that no longer exists, because a branch session's notebook is bound to a LIVE session and a session can end without either governed ending — a probe or a crash-residue cleanup removes a worktree and a branch directly, so no abandon runs and no retirement is recorded. Without reconciliation such a notebook survives its session indefinitely on an account shared across the family, holding quota and misstating the set of live sessions to every later reader.

Dead SHALL be established FORWARD, never by inverting a title. The alias derivation is lossy — it strips the `draft/` prefix and lowercases — so a notebook title cannot be resolved back to a `(repository, branch)` key. The mode SHALL compute the alias of every LIVE session, using the same joint worktree-and-branch liveness signal the session bootstrap uses, and SHALL treat an `xf-session-` notebook that matches no live session's alias as dead. A notebook matching a live session's alias SHALL never be retired.

Liveness SHALL be sought across EVERY WORKTREE of each session repository, not only its canonical checkout. A session's worktree container is keyed on the checkout the session was opened FROM, and sessions are routinely opened from a feature worktree, so a run that asks only the canonical checkout finds no sessions there — a legitimate answer for that checkout, and indistinguishable from the sessions living in another worktree of the same repository. The repository's own worktree list is what makes the enumeration completable, and a run that cannot read it SHALL treat that as an error rather than as an answer.

The mode SHALL FAIL CLOSED on incomplete knowledge. A session repository that cannot be enumerated — an absent checkout, a git failure, an unreadable worktree list, an unreadable session container — is indistinguishable from a repository whose sessions have all ended, and the difference cannot be recovered after a retirement. Any repository the run cannot enumerate SHALL refuse the whole reconciliation, naming the repository and the reason, and SHALL retire nothing.

Where the run resolves NO session repositories in scope at all, it SHALL retire nothing: a workspace carrying none of the repositories a session notebook could belong to has no standing to judge one, so pointing the mode at the wrong root is inert rather than destructive.

The mode SHALL be scoped to the session repositories of the workspace it is run against. The account is shared between workspaces, so a session notebook whose repository segment names a repository this workspace does not carry belongs to another workspace's sessions; such a notebook SHALL be reported as out of scope and SHALL NOT be retired.

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
