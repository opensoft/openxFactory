# Design: add-agent-wallet-identity

## Context

Organized from the `agent-certification-wallets` brainstorm (Brett,
2026-07-15/16) via the staging topic
`openxFactory:staging:agent-wallet-identity`, at the point a consumer named
itself rather than because the idea aged well.

The consumer is specific. On 2026-08-06 LedgerxFactory's poster identity
gained real posting rights in a live sandbox, created purchase invoice
`LXRP0002`, and posted it. The same session recorded what that cost: the
platform-level refusal that had made "agents never post" true by
enforcement was gone, leaving the disposition gate as the only gate. The
proposed replacement — refuse a post when the requesting agent created the
transaction — turned out to be unbuildable, because BC sees one
`userSecurityId` for every agent we run.

## Why the scope is this small

The brainstorm spans wallets, verifiable credentials, qualification levels,
autonomous-authority tiers, delegation chains, drift-triggered
recertification and certification batteries. That is at least three
capabilities, and the battery design carries genuinely unresolved
questions: who authors golden tasks per lane, how large a battery is
statistically sufficient, what tolerance band belongs to which authority
level, and whether batteries are themselves versioned artifacts (they must
be — a changed battery changes what "same agent" means).

Proposing all of it would produce a change nobody could ratify honestly.
This carries the four elements a consumer can use today and names the rest
as successors, each gated on a consumer of its own.

The cheap/expensive split inside decertification is the design's most
useful cut. **Declared change** — any component of the composition hash
moves — is a hash comparison over facts Omnigent heartbeats already
attest, and it catches the common case: somebody edited a prompt, a policy,
or a tool manifest. **Measured drift** — a hosted model changing beneath a
pinned identifier — needs the battery apparatus and all its unresolved
statistics. Taking the first and deferring the second buys most of the
protection for almost none of the cost.

## The two decisions, and why they are put to ratification

### Proof versus assertion

An asserted wallet id would let the LedgerxFactory consumer ship
immediately, and it would still defeat the failure mode most likely to
occur in practice: a bug or a runaway loop performing both halves of a
transaction. It fails only against an agent that deliberately claims
another's identity.

It is recommended AGAINST anyway, because the shape is familiar and was
recently ruled on. `modify-ledgerx-credential-contracts-for-test-asset-authority`
was ratified in August precisely to stop a comment standing in for a rule —
grants carrying `consent_ref: null` with an explanatory note. An asserted
identity is the same trade at a higher stake, and the neutral contract is
the wrong place to make it. A domain that wants the interim can record a
dated exception in its own records, where the exception is visible as an
exception.

### Mandate custody or declare it

Three options were considered.

**Mandate hardware backing.** Safest, and it stalls every consumer
indefinitely — there is no key infrastructure in the stack today.

**Say nothing about custody.** Lets a host-held key masquerade as proof
that the agent acted, which is worse than having no control, because the
audit record would assert something false.

**Declare it and cap authority by it** (recommended). The identity record
carries its custody model from a closed set; the contract states what each
model evidences; the authority an identity may hold is bounded by its
custody. A consumer can start at a low tier without the contract lying
about what its signature means, and raising authority becomes a custody
question rather than a trust assertion.

This is the same move as the `package_content_execution_mode` field
LedgerxFactory ratified in August: record the mode honestly, let consumers
read it, and refuse claims the recorded mode cannot support.

## What this deliberately does not do

- No wallet infrastructure, no issuance service, no key storage, no
  signing implementation. Contracts and schemas only.
- No modification to any existing capability. `roles-authority-model` and
  `credential-contracts` compose with this; neither changes.
- No new authority vocabulary. Authority scope reuses the job envelope's
  `approval_policy` values, so an agent's permission is stated in terms a
  job already carries.
- No obligation on any domain. The MedxFactory constraints are not
  worked around, they are adopted as a requirement: a domain must remain
  able to operate, reconstruct records, and resolve subjects with no
  wallet present at all.

## Risks

**The distinctness assumption.** Segregation of duties assumes two actors
are independent. Two agents from the same model, orchestrator and prompt
are not independent the way two humans are; this control defends against
slips and loops, not against a wrong policy applied consistently by both.
The composition hash gives an objective distinctness floor — different
hash, different agent — but whether that floor is sufficient is left to
the consuming domain and is recorded as an open question in staging.

**Decertification noise.** If the composition hash covers a retrieval
corpus that changes hourly, revocation fires constantly and gets routed
around. What the hash covers is a staging open question and should be
settled before the schema is authored, not after.

**A control that proves less than it appears to.** The custody-declaration
design is what keeps this honest, and it only works if consumers actually
record custody truthfully. The validator can check that a model is
declared and that authority does not exceed it; it cannot check that the
declared model is the real one.
