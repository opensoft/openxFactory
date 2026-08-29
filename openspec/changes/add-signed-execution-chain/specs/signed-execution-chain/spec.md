# signed-execution-chain Specification (delta)

## ADDED Requirements

### Requirement: Ratification presents wallet-carried authority, proven by possession

openxFactory SHALL admit a ratifying act only where the ratifying human has
PRESENTED a wallet-carried grant and that presentation has been PROVEN BY
POSSESSION, and SHALL express both the grant and the proof in the already
shipped `openxwallet` vocabulary rather than in any vocabulary this capability
defines. The grant is an `xfactory_wallet_grant`; the presentation is an
`xfactory_wallet_grant_exercise` whose `proof_of_possession` records what was
presented, whether it verified, what the signature covered, and which key
presented it. The ratification record REFERENCES that exercise by identifier and
carries no second proof, key, identity or grant vocabulary of its own — a
possession claim that is asserted rather than demonstrated is not a
presentation, and a second vocabulary for the same act would be the two-records-
of-one-decision defect at contract scale.

**THIS REQUIREMENT CARRIES A RECOMMENDED-BUT-UNRULED ANSWER.** It encodes the
staged topic's Q1 recommendation — grant vocabulary plus a proof-of-possession
step, recorded in the ratification record — and it reads Q1's "rather than a new
artifact" as *invent no new artifact*, honoured by referencing the shipped
exercise record. Q1 is OPEN and is answered in the clarify round that precedes
ratification; if it is ruled otherwise, this requirement is the text that moves.

#### Scenario: a grant is presented with no proof of possession

- WHEN a ratification presents a wallet-carried grant and no proof of possession
- THEN the ratification is REFUSED naming the missing proof, never the missing grant
- AND the refusal is recorded with the closed code `missing_proof_of_possession`

#### Scenario: a proof is presented and does not verify

- WHEN a presented signature is evaluated and does not verify
- THEN the event is recorded as a verification failure and NOT as an absent proof
- AND the ratification is REFUSED, because a failed proof is a stronger signal than a missing one, never a weaker one

#### Scenario: a presentation verifies

- WHEN the presented proof verifies against the presenting key
- THEN the ratification record names the exercise record, the grant, and the presenting key
- AND no new proof artifact, key record, or grant kind is created by this capability

#### Scenario: the grant was valid at issuance and is revoked now

- WHEN a grant is presented whose revocation check at exercise returns revoked
- THEN the ratification is REFUSED
- AND validity recorded at issuance is not accepted as evidence of validity at presentation

### Requirement: Ratification and chain inception are one signed act

openxFactory SHALL perform CHAIN INCEPTION — the registration of a ratification
into the signed-execution-chain registry, minting the CHAIN IDENTITY as the
digest of the signed ratification — in the SAME signed act as the ratification
it registers, so that a ratified-but-uninscribed state is constructively
impossible rather than merely discouraged. Either both stand or neither does: an
inception that fails leaves no standing ratification, and a chain identity that
exists with no ratification behind it is a fraud signal under this capability's
refusal requirement. The act SHALL be performed OUT-OF-PIPELINE — outside the
codexFactory clearance-envelope pipeline — and the record SHALL cite the ground:
the `gate_rules_council` convening of 2026-08-28 established, code-level and
unanimously, that a class over `openspec/changes/**` can never commission a
council, because that surface lies wholly inside the canonical
`GATE_INTEGRITY_FLOOR`, which is evaluated before any clearable classification
(984 admitted paths, 984 floored, 0 remaining; `gate_integrity` declared, absent,
and no rule document at all all park identically). Routing inception through the
pipeline would describe a control that provably cannot run. **That measurement
is the ground for the surface this repository's ratifications actually land on;
the rule itself is not surface-dependent**, because a pipeline that CLEARS
candidates cannot also be what CONFERS the authority those candidates are
cleared against — a chain whose first link is minted by the mechanism it exists
to permit is circular, and would be circular on any surface, floored or not.

**CHAIN INCEPTION IS NOT ENROLLMENT.** `specs/025-openxfactory-review-lane-caller/spec.md`
FR-008 owns the word "enrollment" in this repository for a different act — the
entry of a candidate class into a `merge-approval-envelope` for the codexFactory
decision core to classify. Chain inception creates no envelope, names no
candidate class, touches no ruleset and produces no verdict; candidate-class
enrollment mints no chain identity and is not a link in any chain. FR-008 stays
gated exactly as the convening left it, and nothing in this capability
discharges, amends or relies on it.

#### Scenario: inception fails after a ratification is signed

- WHEN the inception half of the act cannot complete
- THEN the ratification does not stand and is not recorded as ratified
- AND no partial state is retained that a later reader could mistake for a ratification

#### Scenario: a chain identity is found with no ratification behind it

- WHEN a chain identity resolves to no signed ratification
- THEN it is refused as a fraud signal
- AND it is never treated as an incomplete record awaiting completion

#### Scenario: inception is attempted through the clearance pipeline

- WHEN chain inception is routed through the codexFactory clearance-envelope pipeline
- THEN it parks never-clearable before classification and produces no verdict
- AND the conforming path is the out-of-pipeline act, whose record cites the 2026-08-28 convening

#### Scenario: a reader asks whether inception is 025's enrollment

- WHEN a reader or an implementer treats chain inception as an enrolled candidate class
- THEN the two acts are distinguished by name and neither substitutes for the other
- AND no `merge-approval-envelope` instance is created by this capability

### Requirement: The signed ratification travels with the work

openxFactory SHALL require the signed ratification to be carried WITH the work
as a TRAVELING CONTRACT — a self-contained artifact checkable at the point of
use — rather than as a row in a table the checker must go and look up. The
traveling contract carries the chain identity, the reference to the presentation
that proved link 1, and the digest of the transparency-log leaf that recorded
inception, so that a checker can establish what permits this work without
resolving a live service. Work that arrives with no traveling contract is
UNPERMITTED at the point of use, not merely unattributed; and a traveling
contract whose chain identity does not match the record it claims is a fraud
signal under this capability's refusal requirement rather than a stale copy.

#### Scenario: work arrives with no traveling contract

- WHEN a consuming step evaluates work carrying no traveling contract
- THEN the step REFUSES, because nothing establishes what permits the work
- AND the absence is never read as an unremarkable omission

#### Scenario: the carried digest disagrees with the record

- WHEN a traveling contract's chain identity does not match the ratification it names
- THEN it is refused as a fraud signal
- AND the mismatch is never resolved in favour of the carried copy

#### Scenario: the checker cannot reach the registry

- WHEN a checker at the point of use cannot resolve the registry or any live service
- THEN it can still establish the traveling contract's internal consistency from the artifact alone
- AND that establishes consistency ONLY — a check whose question requires the log still refuses while the log is unreachable, per this capability's gate requirement
- AND an unresolvable external lookup never converts into permission

### Requirement: The signed transparency log is the record

openxFactory SHALL maintain an APPEND-ONLY SIGNED TRANSPARENCY LOG in the
governed store as the primary chain of custody, and SHALL record every act this
capability governs as a SIGNED LEAF on the RFC-6962 / Certificate-Transparency
and Sigstore-Rekor pattern: the wallet-presented ratification, the chain
inception, the issuance of a traveling contract, and every verdict the
short-chain gate returns. Leaves are appended and never edited or removed, and
the log's own hash structure — not an access control and not a convention — is
what makes an alteration detectable. THE LOG IS THE RECORD. Public anchoring is
a LATER ADDITION that makes the record externally undeniable and belongs to the
named tranche-three successor; the absence of an anchor at this tranche is
therefore NOT a defect, and no requirement here may be read as claiming external
undeniability the log alone does not provide.

#### Scenario: a governed act occurs and writes no leaf

- WHEN an act this capability governs completes with no corresponding signed leaf
- THEN the act is UNPROVEN and every consumer that requires the chain refuses it
- AND the act's own success is not evidence that it was permitted

#### Scenario: a leaf is altered or removed

- WHEN a leaf's bytes are changed or a leaf is deleted from the log
- THEN the log's hash structure fails verification and the alteration is detected
- AND the alteration is reported as a fraud signal rather than as a corrupted file

#### Scenario: an external anchor is expected at this tranche

- WHEN a reader asks the log for an external anchor or an inclusion receipt
- THEN the log states that anchoring is a named tranche-three successor and claims none
- AND the missing anchor is not counted as a broken link

### Requirement: A gate validates the short chain as a hash-linked chain

openxFactory SHALL operate, FROM THIS TRANCHE, a gate that validates links 1–3
before permitting the terminal act, and SHALL validate them as a HASH-LINKED
CHAIN rather than as a bag of signatures: every link from inception onward signs
over the chain identity AND the digest of the link that precedes it, and the
gate validates that CONTINUITY, never merely the presence of the required
signatures. Individually valid artifacts drawn from DIFFERENT executions MUST
NOT assemble into a chain, because with concurrent or repeated work a signature
bag is exactly what a badly-behaved lane would submit. A BROKEN OR MISSING LINK
IS A FRAUD SIGNAL AND A REFUSAL, never a warning and never a finding downgraded
for convenience: a missing link means either the act did not happen or something
is misrepresenting that it did, and both are refusals. A chain the gate cannot
EVALUATE is refused on the family's fail-closed doctrine — an unevaluable answer
never reads as permission. The gate's scope at this tranche is links 1–3 and it
SHALL NOT report the absence of a later tranche's link as a break, because a
gate cannot walk a link that does not exist yet.

#### Scenario: valid artifacts from different executions are submitted together

- WHEN the gate receives links that individually verify but do not share one chain identity and predecessor sequence
- THEN it REFUSES, naming the broken continuity
- AND per-link validity is never accepted in place of continuity

#### Scenario: a link is missing

- WHEN any of links 1–3 is absent
- THEN the gate REFUSES and reports a fraud signal
- AND the outcome is never downgraded to a warning, an advisory, or a finding to be triaged

#### Scenario: the gate cannot evaluate the chain

- WHEN the log is unreachable, a key is unresolvable, or the chain cannot otherwise be evaluated
- THEN the gate REFUSES rather than proceeding
- AND an unevaluable condition is never reported as a pass

#### Scenario: a tranche-two link does not exist yet

- WHEN the gate walks a chain that carries no attestation link
- THEN it validates links 1–3 and returns a verdict scoped to them
- AND the absent later link is not reported as a break

### Requirement: Ratifying authority is human-held

openxFactory SHALL require the authority that INCEPTS a chain — the tier-1
ratifying credential — to be held by a NAMED HUMAN, and SHALL refuse it to an
agent, a runner, a lane, a workflow identity, or any other machine holder. The
ground is constitutional rather than conventional: every omnigent worker
archetype carries `access_secrets: false`, so a worker cannot hold an authority
credential, and a design in which a runner signs AUTHORITY contradicts ratified
text. The narrowing to RATIFYING authority is exact and is the reason this
requirement does not disturb a realized artifact: an agent-held wallet backing a
`review`-act grant is not a ratifying credential, and its `holder_readable`
custody evidences that the HOST acted — which under the ratified declared-custody
rule is precisely what a ratification may not stand on. Tier 2 — ephemeral
per-task attestation identities, whose keys never enter a worker — is the named
tranche-two boundary and is NOT defined here; no attestation identity of any
kind is created by this capability.

#### Scenario: a machine holder is named as ratifying authority

- WHEN a grant naming an agent, runner, lane, or workflow identity as holder is presented to incept a chain
- THEN the ratification is REFUSED
- AND the refusal names the holder class rather than the missing signature

#### Scenario: a runner asks for the ratifying key

- WHEN any worker, runner, or lane requests custody of a tier-1 credential
- THEN the request is REFUSED and no key material crosses into it
- AND a short credential lifetime is not accepted as making a key non-secret

#### Scenario: an attestation is offered as authority

- WHEN a record attesting what ran is presented in place of a record of who permitted
- THEN it is REFUSED as answering a different question
- AND neither tier is ever accepted as standing in for the other

#### Scenario: an agent-held review grant is presented for review, not ratification

- WHEN an agent-held wallet exercises a `review`-act grant
- THEN this requirement does not refuse it, because reviewing is not incepting a chain
- AND the same holder remains refused for any ratifying act
