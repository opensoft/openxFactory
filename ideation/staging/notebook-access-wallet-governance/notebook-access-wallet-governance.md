# Staged: notebook access is granted through the app, held in the wallet, and enforced by Google

Status: staged
Kind: capability-proposal
Summary: Sharing the governed NotebookLM books happens THROUGH THE APP, not by
opening the books to the organization. Brett ruled the Google-side posture
RESTRICTED and the app the SOLE GRANTOR: every person's access arrives as a
governed grant the app performs, because an org-visible book is provider-granted
access that no record of ours can subtract. This topic asks what holds those
grant authorities — openxWallet is the candidate — how the already-ratified
share-out roster entry becomes the wallet-governed record, and how far access
can be controlled per repository and finer, given that Google's own enforcement
atom is one notebook, one user, viewer-or-editor, and nothing smaller.
Topics: notebooklm, lifecycle-notebook-projection, openxwallet, access-control,
share-out-roster, identity-brokering, provider-enforcement, per-repo-policy
Repository context: openxFactory owns every capability this topic touches —
`lifecycle-notebook-projection` (the books, the share-out roster ratified by
`add-notebook-projection-identity`, and the sync that performs provider acts),
`openxwallet` (the candidate holder of the grant authorities), and
`identity-brokering` (the persona half of a grantee). The provider act itself
is `nlm share invite --profile`, run under the declared hosting account.
Staging ID: openxFactory:staging:notebook-access-wallet-governance
Captured: 2026-08-24
Source: Brett Heap's direction 2026-08-24, in session, verbatim: "we are doing
the sharing thru the app. so if we allow org wide in the google machinery, we
still have this on the user right? can we add this to the wallet and then
control with repo or even more fine grain access?" — followed by two
question-prompt rulings: the Google-side posture is RESTRICTED with the app as
the sole grantor (org-visible REJECTED), and this topic is staged rather than
proposed now.
Target capabilities: MODIFIED `lifecycle-notebook-projection` (the share-out
roster becomes a wallet-governed record; the grant lane's provider act and its
revocation semantics) and possibly MODIFIED `openxwallet` — though the grant
shape already closes the interesting half of that question: its `scope` is
closed and its `audience` must be a wallet, so the wallet can hold the
AUTHORITY to perform a granting act but cannot name the grantee or the
provider's resource (Open question 1). Possibly MODIFIED `identity-brokering`
if naming a grantee needs more than a persona reference (Open question 7).

## Last proposal attempt (round-trip provenance)

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Claims

Settled by Brett's 2026-08-24 rulings and NOT reopened by the open questions
below — they are the fixed baseline the questions iterate against:

1. **Sharing happens through the app.** A person's access to a governed book
   arrives as a grant the app performs, not as a side effect of who they work
   for.
2. **The Google-side posture is RESTRICTED.** Org-wide visibility is REJECTED.
3. **Google's ACLs are the OUTER enforcement.** An org-visible book is
   provider-granted access that no app-side record can subtract — the app could
   record a denial all day while Google keeps serving the notebook. Brett's own
   question named this ("we still have this on the user right?"); the answer is
   yes, and it is why the posture is restricted.
4. **Deny-by-default at the provider, every grant through the governed lane.**
   The default state of a book is that nobody but the hosting account can read
   it, and each exception is an act with a record.
5. **The provider's enforcement atom is per-notebook, per-user,
   viewer-or-editor.** That is the whole vocabulary Google gives us.
6. **Per-repo control maps to per-book, because the books ARE per-repo.**
   `split-ideation-book-per-repo` made every governed repository's ideation
   corpus its own book, so "control access by repository" is already expressible
   in the provider's own atom, with no new mechanism.
7. **Finer-than-book granularity is NOT provider-enforceable.** Per-source,
   per-section and lifecycle-status filtering cannot be expressed to Google at
   all; anything finer than a book exists only through our own surface
   (doxBench / the dashboard's packet rails), and is a NAMED NON-GOAL of the
   Google half of this topic.

## Why

<!-- xspec:candidate target=lifecycle-notebook-projection -->
`add-notebook-projection-identity` ratified that access is shared out FROM the
hosting account and that each share act is a governed decision recorded as a
share-out roster entry, keyed `(hosting_account, user, book_or_alias, role,
granted_at, granted_by)`. What it did not settle is WHO HOLDS THE AUTHORITY to
make that decision, or what the roster entry IS beyond a row — and the §12
platform correction has since established that the outbound act is scriptable
(`nlm share invite --profile`), so the grant lane is no longer hypothetical.

The pressure Brett named is the org-wide shortcut. Google Workspace can make a
notebook visible to everyone in `opensoft.one` at once, which would retire the
per-person invite entirely. It is refused, and the reason is the same doctrine
`client-identity-roster` already promotes: *"Where such a principal IS available
it SHALL be used and the bound SHALL be recorded as provider-enforced. A bound
recorded as provider-enforced when no per-unit principal exists SHALL be a
finding."* Google DOES offer a per-notebook, per-user principal. Choosing
org-visibility would take a provider-enforced bound that exists and downgrade it
to a logic-enforced one — our records asserting a restriction the provider is
not applying. That is precisely the shape the family refuses.

So the question is not whether to restrict, but what governs the exceptions:
where the authority to grant lives, what the roster entry becomes when it is
more than a row, and how far the control surface can go before it stops being
something Google will enforce.
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=openxwallet -->
The authority to grant access to a governed book becomes a held, attenuable
thing rather than an implicit property of whoever can run the sync.
`openxwallet` is the candidate holder: it already models authority travelling as
attenuated grants, proof-of-possession on use, key-attributed exercise, and
revocation propagating through a chain — which is the shape a share-granting
authority wants. What a wallet grant may hold is the first open question, and
the schema answers much of it already: the grant's `scope` is closed, its
`audience` must be a wallet, and there is nowhere to write a provider or an
external role. So the authority to PERFORM the granting act is what the wallet
can carry; "user X may view Google notebook Y" is not representable there at
all.
<!-- /xspec:candidate -->

<!-- xspec:candidate target=lifecycle-notebook-projection -->
The ratified share-out roster entry becomes the WALLET-GOVERNED RECORD of a
grant rather than a free-standing row: the same key, but issued under an
authority, attributable to the exercise that produced it, and revocable through
the same chain. The grantee's human half is named by an identity-brokering
persona wherever one resolves, which the ratified roster requirement already
asks for. The approval act (the governed manual lane) authorizes the grant; the
provider act (`nlm share invite --profile <declared-profile>`) realizes it
against Google; and the roster entry records that both happened.

Per-repository control needs no new mechanism — the books are already per-repo,
so a repository's access policy IS its book's grant set. Whether a repository
may DECLARE that policy itself, and have its book's grants derived from the
declaration, is open question 5.
<!-- /xspec:candidate -->

## Impact

<!-- xspec:candidate target=lifecycle-notebook-projection -->
- Affected specs: `lifecycle-notebook-projection` (MODIFIED — the share-out
  roster as a wallet-governed record, the grant lane's provider act, and
  revocation semantics); `openxwallet` (MODIFIED — if a grant may scope an
  external provider's resource at all); possibly `identity-brokering` if a
  grantee needs more than a persona reference.
- Affected code, eventually: `scripts/sync-notebooklm-books.py` (the provider
  act and a reconciliation of the roster against `nlm share status --json`),
  `examples/notebook-projection-hosting.yaml` (where the roster lives today),
  and whatever surface performs the approval.
- **Sequencing, deliberate:** this topic sequences AFTER the migration thread's
  held steps clear. There is nothing to grant access TO under the declared
  account until the books are re-derived there — the migration is in flight as
  PR #289 — and `add-notebook-projection-identity` and
  `add-notebook-hosting-credential-custody` are both still ACTIVE, so the
  requirements this topic would amend are ratified but not yet promoted.
- **Honest bound:** nothing in this topic can make Google enforce anything
  finer than one notebook for one user. Claim 7 is a limit, not a deferral.
- No access is granted, revoked, or changed by staging this topic.
<!-- /xspec:candidate -->

## Idea notes (pre-document, non-documented)

- The revocation question has a sharp precedent from three days ago. PR #282's
  review established that revoking a binding to a shared BEARER secret stops
  future fetches but cannot un-disclose what was already fetched. A share grant
  is the opposite shape and that is worth stating: Google's ACL is a REFERENCE,
  not a bearer token, so removing a collaborator genuinely removes their access
  — no rotation needed, nothing already-disclosed to chase. The lesson transfers
  as a contrast rather than as a constraint, and the topic should say which
  kind of thing each artifact is. — Added-by: Claude Opus 5 (session, Brett's
  direction) · 2026-08-24
- `nlm share status <notebook> --json --profile <p>` gives a live read of a
  book's collaborators, which makes the roster RECONCILABLE against reality —
  the same trick the parity mode uses for sources. A drift check ("who does
  Google think can read this book, versus who does the roster say?") is
  probably the cheapest real enforcement this topic can offer, and it is
  available today. — Added-by: Claude Opus 5 (session, Brett's direction) ·
  2026-08-24
- Brett's "or even more fine grain access" may be answerable in a different
  layer rather than refused outright. Google cannot enforce below a notebook,
  but doxBench's packet rails already decide what a reader is shown; a
  lifecycle-status or per-source filter could be real THERE while the book
  itself stays a single provider-enforced unit. That is a different capability
  and probably a different topic, and conflating the two is how a
  non-enforceable promise gets made. — Added-by: Claude Opus 5 (session,
  Brett's direction) · 2026-08-24
- A per-repo declared roster (open question 5) would make access review a
  code-review act: adding a reader to a repository's book becomes a PR against
  that repository. Attractive, and it inverts who holds the authority — the
  repository's own maintainers rather than the hosting account's operator —
  which may or may not be what Brett's "control with repo" meant. — Added-by:
  Claude Opus 5 (session, Brett's direction) · 2026-08-24

## Conflicts

- The wallet's eighth promoted requirement says the capability is "an authority
  control, never an identity substrate", and that "a wallet identifier SHALL NOT
  become a subject identifier". A share-out roster entry keyed on a USER is
  identity-shaped by construction, so putting it under wallet governance risks
  exactly the drift that requirement forbids. The tension is not fatal — the
  authority to grant is not the identity of the grantee — but it is real and the
  eventual change must show which half the wallet holds. — Added-by: Claude
  Opus 5 (session, Brett's direction) · 2026-08-24
- The ratified share-out roster lives in
  `examples/notebook-projection-hosting.yaml`, a governed record deliberately
  kept OUT of `contracts/` on the ownership test. If the roster entry becomes a
  wallet-governed record with a contract-family schema, that decision is
  reopened and the contract-release ritual would fire. This topic must not
  reopen it by accident. — Added-by: Claude Opus 5 (session, Brett's direction)
  · 2026-08-24
- Two of the three capabilities this topic would amend are carried by ACTIVE
  changes whose deltas are ratified but UNPROMOTED
  (`add-notebook-projection-identity`, `add-notebook-hosting-credential-custody`).
  A change raised from this topic before those archive would be amending
  requirement text that the promoted spec does not yet contain. — Added-by:
  Claude Opus 5 (session, Brett's direction) · 2026-08-24

## Open questions

### Q1. May an openxWallet grant scope an EXTERNAL provider's resource, or is that outside what the capability is for?

Context: checked against the schema rather than assumed, and the answer is
narrower than the question expects. `openxwallet`'s grant record
(`contracts/openxwallet/openxwallet-grant.schema.yaml`) closes its `scope`:
`additionalProperties: false`, required `acts` and `authority_tier`, optional
`objects` and `approval_posture`. There is NO property in which a provider, an
external resource or a provider-side role could be written, and inventing one
is a named validation failure (`authority-vocabulary-parallel`). Its `audience`
requires a `wallet_ref` — "always a wallet, because exercise requires proof of
possession of that wallet's key" — so a grantee who is an ordinary human with
no wallet cannot even be the audience. The capability's eighth promoted
requirement then bounds the whole thing as "an authority control, never an
identity substrate". Where the family DOES model reaching an external platform
is the exercise record, and it points the other way: the presenting wallet key
is recorded as the actor and the third-party credential "as transport, never as
the actor" (`openspec/specs/openxwallet/spec.md`). The external platform is
downstream plumbing, not the subject of a grant.
(Correction, same day: this question was first drafted saying the grant's scope
was open by construction and that a Google-notebook scope "would VALIDATE
today". That was wrong on the decisive point — the scope is closed. The binding
modes the framing also asked after do exist, but they are `content` and
`reference` in the agent-composition schema and govern what a component hash
covers, not how a grant composes.)
Recommended answer: NO — and the corrected reading makes this close to
determined rather than a preference. The wallet holds the AUTHORITY TO PERFORM
THE GRANTING ACT: a wallet-bearing actor holds a grant whose `acts` name the
share-granting act at some `authority_tier`, and `scope.objects` MAY narrow it
to particular books. The grantee never appears in the wallet at all, the
provider's ACL remains the access, and the roster records that the act
happened. Three nouns, kept apart: the AUTHORITY (wallet), the ACT (provider
call), the ACCESS (Google's ACL).
Explanation: this is what the shape already permits, so nothing has to be
widened to get it — and widening is the thing to avoid, because a scope key
naming a provider is exactly the parallel-authority-vocabulary failure the
schema refuses. It also keeps the wallet on the right side of its eighth
requirement, and matches the enforcement reality in Claim 3: Google's ACL is
the outer enforcement whatever our records say. A wallet grant that claimed to
BE the access would be a logic-enforced bound wearing a provider-enforced name
— the exact fault Claim 3's citation refuses.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-24

### Q2. Does the ratified roster entry BECOME the wallet-governed record, or does a wallet grant point at it?

Context: `add-notebook-projection-identity` ratified the share-out roster entry
as the record of a governed share act — "the entry IS the record, not an audit
trail beside one" — keyed `(hosting_account, user, book_or_alias)` with role,
grant time and granting actor as attributes. A wallet grant carries its own
identifiers, its own issuer and its own chain. Two records describing one act
is the shape that ratified sentence was written to prevent.
Recommended answer: ONE record. The roster entry stays the record of the act
and gains the grant's identifiers as attributes — the authorizing grant, the
exercise that produced it — rather than a second wallet-side record of the same
share existing in parallel.
Explanation: the ratified requirement's whole point was that approving writes
the roster rather than writing an audit trail beside it; introducing a wallet
record that also describes the share would reintroduce the split under a new
name. The uniqueness key already settled — the stable scope-and-principal
triple, with decisions as attributes — has room for the authority fields.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-24

### Q3. What does revoking a share grant MEAN, provider-side?

Context: PR #282's review established that revoking a binding to a shared bearer
secret cannot un-disclose what was already fetched, and that eviction needs
rotation. A Google collaborator ACL is a different class: it is a reference the
provider evaluates per request, so removing it genuinely removes access. What is
unsettled is what our side does — whether revocation is a roster deletion, a
tombstoned entry, a wallet-chain revocation propagating to the provider act, or
all three, and what happens to content the person already exported.
Recommended answer: revocation is a RECORDED ACT that performs the provider
removal and tombstones the roster entry — never a silent row deletion. The
wallet chain's revocation propagates the AUTHORITY (whoever could grant may
have that power withdrawn); the provider act removes the ACCESS; the roster
records both. Content already exported is explicitly out of reach and should be
said so rather than implied.
Explanation: keeping the tombstone matters for the same reason the roster
exists — a deleted row cannot answer "who used to have access and who removed
it". Distinguishing authority-revocation from access-revocation avoids the
category error #282 had to correct: one is about who may act, the other about
what a principal can still reach.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-24

### Q4. Who approves, and does this topic settle that or inherit it?

Context: `add-notebook-projection-identity`'s task 2.4 is open precisely
because the designated company-policy actor has never been named — the lane's
procedure is written and its actor is not. This topic gives that actor a
concrete authority to hold (Q1), which is either the natural moment to name
them or a reason to keep the two apart.
Recommended answer: name the actor HERE, as the holder of the granting
authority, and close task 2.4 from this topic's eventual change rather than
leaving it stranded in a change that has already archived its other work.
Explanation: an authority with no named holder is the same defect as a lane with
no named actor, and both would be closed by one decision. The alternative —
naming the actor in the earlier change's own realization — keeps them separate
but leaves task 2.4 waiting on a topic that had not been staged when it was
written.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-24

### Q5. May a repository DECLARE its own book's access policy?

Context: Claim 6 settles that per-repo control maps to per-book, because the
books are already per-repo. What it does not settle is where the policy is
authored. Today the roster lives centrally, in the hosting record beside the
declaration. A repository could instead declare its own readers, and the sync
could derive that book's grants from the declaration.
Recommended answer: lean toward allowing it, as a DERIVED input rather than an
independent authority — a repository declares who it believes should read its
book, and the governed lane still performs and records the grant. Do not let a
repository's declaration BE the grant.
Explanation: this is the same derivation discipline the projection already runs
on (membership is derived from `Status:` headers, never hand-curated), and it
makes access review a code-review act in the repository that owns the corpus.
Keeping the grant itself in the governed lane preserves Claim 4 — every grant
flows through one place — while letting the people who own the material say who
needs it. The risk is a repository declaring a reader nobody centrally approved,
which is exactly why the declaration must be an input and not an authority.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-24

### Q6. Where does finer-than-book access live, given Google cannot enforce it?

Context: Brett's direction asked for "repo or even more fine grain access".
Claim 7 settles that Google's atom is one notebook for one user and that
anything finer is not provider-enforceable. But doxBench and the dashboard
already decide what a reader is shown, and a lifecycle-status or per-source
filter could be genuinely enforced THERE — for readers who come through our
surface.
Recommended answer: treat finer-than-book as a NAMED NON-GOAL of this topic's
Google half, and record the surface-side route as a separate topic rather than
folding it in. Anyone reading a book directly in NotebookLM sees the whole book;
that is the honest statement.
Explanation: the two halves have different enforcement stories, and merging them
produces a promise that is true through one door and false through another. The
family has been bitten by exactly this shape before — a bound asserted by our
logic where the provider grants more broadly — which is Claim 3's whole subject.
Keeping them separate lets the surface-side filter be designed as what it is: a
presentation control for readers who arrive through our rails, not an access
control.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-24

### Q7. How is a grantee NAMED, when personas cannot hold an email and Google grants are addressed by one?

Context: the ratified roster requirement says an entry "SHALL reference a
governed persona wherever the identity-brokering family resolves one for that
human, falling back to a bare address only where no persona resolves". Checked
against the persona schema, that seam is tighter than it reads: a persona's
`subject` is an opaque broker-issued identifier whose pattern "admits no '@' and
no whitespace, so an email address and a display name are UNREPRESENTABLE in
this position rather than merely discouraged", and a linked upstream identity
carries the provider-issued `upstream_subject` (a Google numeric subject in the
worked example), not an address. Meanwhile the provider act needs an EMAIL:
`nlm share invite <notebook> <email>`. The roster's validated fields carry
`user` as a bare address today and have no persona-reference field at all.
Recommended answer: carry both, with distinct jobs — a persona reference as the
durable governed identity of the grantee, and the email as the PROVIDER
ADDRESSING DATUM the act needs, marked as such rather than as an identifier.
Resolve the address from the persona's linked Google identity where the broker
knows it, and treat an address with no persona as the honest fallback the
ratified text already allows.
Explanation: the two are not competing spellings of one thing. The persona is
what the governed record binds to and what survives an address change; the email
is a provider input, and the identity-brokering family refuses to let an
address be an identifier precisely so nobody builds on it. Keeping them in
separate fields lets the roster satisfy the ratified persona requirement without
pretending the provider can be addressed by an opaque subject.
Disposition status: open
Added-by: Claude Opus 5 (session, Brett's direction) · 2026-08-24

## Exit

Iterate this fragment until all seven open questions carry a disposition other
than `open`, then raise one OpenSpec change carrying the
`lifecycle-notebook-projection` delta (the wallet-governed roster entry, the
grant lane's provider act, and revocation semantics) together with whatever
`openxwallet` delta question 1 resolves to.

It SEQUENCES AFTER the migration thread's held steps clear. There is nothing to
grant access to under the declared account until the books live there, and the
two changes whose requirements this topic would amend are both still active
with ratified-but-unpromoted deltas — a change raised before they archive would
be amending text the promoted specs do not yet carry.
