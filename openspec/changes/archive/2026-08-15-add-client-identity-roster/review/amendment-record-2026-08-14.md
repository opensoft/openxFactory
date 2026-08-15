# Amendment record: add-client-identity-roster — Decisions A and B

Status: record
Date: 2026-08-14
Ruled by: Brett Heap (openxFactory operator authority), 2026-08-14, in
session, both decisions "amend the change" (option i in each).
Companion to: `decision-review-2026-08-14.md` (the first-draft cross-model
review, `Status: record` — appended to here rather than edited, per the
record-immutability rule).
Raised by: the cross-model adversarial review of the Speckit clarify rulings
for feature `007-client-identity-roster`
(`specs/007-client-identity-roster/clarify-rulings-2026-08-14.md`, rulings R2
and R4/N3, both escalated because they are ratified-scope decisions rather
than architect calls).

## The shared defect: a modification in substance, undeclared in the packet

Both amendments cure one defect class. The ratified proposal and design
MANDATE a behaviour that only exists by changing a capability the proposal
does not list as MODIFIED. Left uncured, the change would have archived while
silently rewriting a promoted capability's exhaustive enumeration (A), or
would have shipped a ratified blocking clause with no neutral artifact behind
it at all (B). The alternative in each case was to REDUCE ratified scope,
which the ratifier declined.

## Decision A — `domain-conformance-checks` is MODIFIED (pack grows to four)

Ratified answer 2 makes intra-repo entry conformance BLOCK the owning
domain's gate. The adversarial review established that pack membership is the
ONLY promoted mechanism that confers blocking status on a canonical check
(`openspec/specs/domain-conformance-checks/spec.md`: "a nonzero exit from any
check fails the domain gate"), that domain gates invoke no canonical
validator today, and that domain-repo edits are out of scope for this feature.
The promoted pack requirement enumerates its three scripts EXHAUSTIVELY, so
enrolling `scripts/validate-client-identity-roster.py` modifies that
capability whether or not the packet says so. Dropping enrollment instead
would have reduced a ratified deliverable. Brett ruled AMEND: this packet now
carries `specs/domain-conformance-checks/spec.md`, a MODIFIED delta growing
the pack to four checks and adding the roster property to the conformant-repo
requirement, and `domain-conformance-checks` is declared in the proposal's
Modified Capabilities. Per ruling R5 the check enforces no completeness rule:
in a target repo publishing no roster fragment it passes with an explicit
notice, so the added blocking surface cannot fire on absence.

## Decision B — `credential-contracts` is MODIFIED (`issuance_preconditions`)

Ratified answer 2's third clause makes an open drift finding REFUSE grant
issuance for that identity, and the packet routes it through "the existing
`issuance_preconditions` mechanism". The adversarial review verified that no
such neutral mechanism exists: `issuance_preconditions` appears nowhere in
openxFactory's contracts, schemas, scripts or promoted specs — it is a
domain-local extra key in OpsxFactory's `credentials/requirements.yaml`,
riding a neutral schema that neither declares nor forbids extra keys. Giving
the refusal any neutral home therefore modifies `credential-contracts`, the
same undeclared-modification defect as A. Routing it through the active
`add-dispatch-credential-contract` lane was rejected as cross-lane coupling;
shipping nothing neutral was rejected as reducing ratified scope. Brett ruled
AMEND: this packet now carries `specs/credential-contracts/spec.md`, a
MODIFIED delta giving the canonical credential schema a closed
`issuance_preconditions` vocabulary whose first member is the roster-drift
precondition, optional and additive so no existing record changes shape.
Realization is proven at the neutral level by a CONFORMANT
requirement-record fixture, because no producer of live drift findings exists
anywhere in the family at archive time; live refuse-then-allow is proven in
the domain follow-up at the mint surface.

## Consequences recorded

- Modified Capabilities are now four: `consent-instrument`, `doc-health`,
  `domain-conformance-checks`, `credential-contracts`.
- Archive blockers (clarify ruling C2) accordingly include OpenSpec task 3.1
  (pack enrollment) and task 3.3 (the neutral refusal fixture); both are
  dispositioned by these decisions rather than by silence. Only section 4
  (domain fragments) remains exempt.
- Strict validation re-run over the amended packet and over the whole
  OpenSpec corpus before the amendment was committed.
