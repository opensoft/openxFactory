# chain-anchoring (delta) — repoint-chain-anchoring-medxchain-citation

## MODIFIED Requirements

### Requirement: Served verification and access decisions are logged leaves

openxFactory SHALL write the VERIFY events, FAILED verifications, and BOTH
PERMITTED AND REFUSED ACCESS DECISIONS THAT THE FACTORY SERVES as signed leaves
in the evidence plane,
on the same footing as the events that produce material. The SERVED surface is
this capability's own verification surfaces, the permissioned plane's access
decisions, and any attempt against material the factory holds. **A PERMITTED
access is logged on the same footing as a refused one**, because a record of
refusals alone answers who was turned away and not who actually read, and the
question an audit asks first is the second one. An evidence plane
that records only what was written answers what happened and cannot answer who
tried — and for a capability whose whole purpose is external verifiability, an
unrecorded attempt against a surface this factory operates is a hole in exactly
the surface the design exposes. Checkpoints over these leaves are anchored
through the configuration above like any other checkpoint.

**AND WHAT THE FACTORY CANNOT OBSERVE IS NAMED HERE RATHER THAN DEMANDED,
BECAUSE A REQUIREMENT CANNOT BIND WHAT NOTHING CAN SEE.** The receipt
requirement above exists precisely so that a holder can check a receipt WITHOUT
contacting the party that minted it, against a canonical header set the holder
obtains for itself. A party doing exactly that is therefore INVISIBLE here by
construction: there is no request to serve, no surface to instrument, and no
honest way to write a leaf for an event this factory has no knowledge of.
**That invisibility is a PROPERTY OF THE DESIGN AND NOT A GAP IN THIS
REQUIREMENT** — it is what *"the receipt's trust root is a PUBLIC CHAIN the
verifier can independently reach"* means when it is true. This requirement
SHALL NOT therefore be read as claiming a census of every verification of
anchored material anywhere; **its completeness claim is over the SERVED surface,
and it names which surface that is.**

**AND THE OBVIOUS WAY TO CLOSE THAT GAP IS REFUSED, BECAUSE IT WOULD COST THE
PROPERTY THE CAPABILITY IS FOR.** A realization SHALL NOT discharge this
requirement by imposing a REPORTING OBLIGATION on independent verifiers — an
authenticated call-home before or after a local verification — because that
trades the receipt's self-sufficiency for a telemetry channel, makes the
minter's reachability a precondition of verification again, and turns the
who-verified-what trail this requirement's own last paragraph keeps off a public
ledger into a trail the minter collects instead. An unobservable verification is
the correct outcome, not a defect to instrument away.

**THIS OBLIGATION IS CARRIED FROM A NAMED SOURCE, AND THE SOURCE HAS LEFT THIS
REPOSITORY FOR GOOD.** The MedxChain notes (formerly
`ideation/brainstorm/medxchain-blockchain-medical-records.md` in this
repository, now at the same repository-relative path in
`MedxSoft/MedxFactory@74bed502 ideation/brainstorm/medxchain-blockchain-medical-records.md`
— vendored into openxFactory by pull request #509, then moved out to
MedxFactory by pull request #785, 2026-09-08, in the 2026-09-07
ideation-split ruling) log views, edits, FAILED ATTEMPTS and
administrative actions, and their appendix names verification-attempt auditing
as an addition the neutral family's ten links do not yet carry, since those
links are framed around what was signed and produced. **The path never
resolves inside this repository again — it is cited here, and in the three
other requirements below that share it, as HISTORICAL PROVENANCE ONLY**, said
in the requirement rather than only in the proposal, because a reader arrives
at a spec without one. **The obligation does not depend on the citation**: it
is normative on its own ground — an evidence plane that records only what was
written answers what happened and cannot answer who tried — and the citation
is PROVENANCE, naming where the obligation came from and whose design sketch
first stated it.

**AND THE SERVED SCOPING IS WHAT THE SOURCE ACTUALLY SAID, WHICH IS WORTH
STATING BECAUSE THIS PACKET GOT IT WRONG FIRST — AND THEN GOT THE OTHER HALF
WRONG TOO.** The notes log *"every access attempt to the … data"* and *"views,
edits, failed access attempts, and administrative actions"* — mediated access,
against a system that serves it, **VIEWS INCLUDED**, which is why the permitted
half is required above: the first scoping pass carried the source's refusals and
dropped its successes, leaving an observable class inside the served surface
unlogged —
and their appendix asks the neutral family for *"a generic verification-ATTEMPT
scenario alongside the successful-access case"*. **The over-reach was this
packet's own**, in first carrying that as an obligation over any verification by
any party anywhere, which is wider than the source and wider than anything a
factory can observe. The scoping above is therefore a correction to this
requirement's carrying of its source and **NOT a further correction to the
source**, which is why it is not numbered among the corrections requirement 8
records.

**AND THESE LEAVES ARE BOUND BY THE BOUNDARY LIKE EVERYTHING ELSE.** An attempt
leaf SHALL carry no payload and no unsalted commitment, and the checkpoint over
attempt leaves is what a chain sees — never an attempt row, which would publish a
who-looked-at-what trail to a permanent public ledger and leak by metadata what
the payload rules keep off it.

#### Scenario: a verification the factory serves succeeds

- WHEN an external party asks one of this capability's verification surfaces to verify an anchored item and it succeeds
- THEN the verification is written as a leaf naming what was verified and the outcome
- AND the leaf is covered by an anchored checkpoint like any other leaf

#### Scenario: a verification the factory serves fails

- WHEN a verification the factory serves is attempted and does not verify
- THEN the failure is written as a leaf recorded as a failure, never as an absent event
- AND a log that shows no leaf for that served attempt is non-conformant with this requirement

#### Scenario: an independent holder verifies a receipt locally

- WHEN a party holding a receipt verifies it on its own machine against a canonical header set it obtains for itself, without contacting the factory
- THEN NO leaf exists for that verification and none is claimed, because the factory has no knowledge of an event it did not serve
- AND the absence is NOT non-conformance, because it is the receipt's self-sufficiency working as the requirement above designed it

#### Scenario: a reporting obligation on independent verifiers is proposed

- WHEN a realization proposes requiring independent verifiers to report their local verifications so that every verification produces a leaf
- THEN it is REFUSED, because it makes the minter reachable-or-nothing again and collects the who-verified-what trail this requirement keeps off a public ledger
- AND the served scoping above is how this requirement is satisfied instead

#### Scenario: an access attempt is refused

- WHEN an access request is refused by the permissioned plane
- THEN the refused attempt is written as a leaf
- AND the leaf records the refusal without recording the material that was not disclosed

#### Scenario: an access request is permitted

- WHEN the permissioned plane PERMITS an authenticated read or view of material the factory holds
- THEN the permitted decision is written as a leaf on the same footing as a refusal, naming who was served and what was reached
- AND the leaf records neither the material nor an unsalted commitment to it, so the boundary above is unchanged
- AND a realization that logs only refusals is non-conformant, because refusals alone answer who was turned away and never who actually read

#### Scenario: a realization logs only successful writes

- WHEN an evidence plane records produced material and none of the verification or attempt events the factory served
- THEN it is REFUSED as non-conformant, naming this requirement
- AND the absence is not read as an implementation detail, because the missing events are the ones an attacker generates

#### Scenario: attempt rows are proposed for direct anchoring

- WHEN a realization proposes anchoring each attempt event directly to a public chain
- THEN it is REFUSED, because a per-attempt public trail leaks by metadata what the payload rules keep off chain
- AND batched checkpoints over the attempt leaves are anchored instead

### Requirement: The record and demographic planes are analyzable without the identity plane

openxFactory SHALL separate the planes so that analysis across the RECORD plane
and the DEMOGRAPHIC plane is possible WITHOUT the IDENTITY plane, BY
CONSTRUCTION rather than by policy. A record-plane entry and a demographic-plane
entry SHALL carry no identifier that resolves a person, and the linkage that
joins either to a person SHALL exist only inside the governed permissioned
identity plane. Analysis over the first two planes therefore exposes no DIRECT
identifier because there is none to expose, not because a query was written
carefully — a structural property, and a narrower one than de-identification,
which the block below distinguishes rather than assumes.

**THE CROSS-PLANE JOIN KEY IS THE DEFECT THIS REQUIREMENT CLOSES, AND IT IS A
CORRECTION TO THE SOURCE SKETCH RATHER THAN A RESTATEMENT OF IT.** The MedxChain
notes (cited above; now at `MedxSoft/MedxFactory@74bed502`, historical
provenance only) segregate three databases but carry ONE shared record digest
across all three, which makes that digest a join key: anyone holding a
demographic row and an identity row can link them without either plane's
permission. So the per-plane key SHALL be derived under that plane's OWN salt,
and the anchored commitment — derived under the record's salt, held in the
governed layer — SHALL NOT function as a cross-plane join key. The segregation is
only structural if the keys are.

**AND THE LANE STILL NEEDS A JOIN, SO THE JOIN IS DEFINED RATHER THAN LEFT
IMPOSSIBLE.** Correlating a demographic attribute with a record attribute
requires SOME correspondence between the two planes' rows, and the paragraph
above refuses the one thing that would silently supply it. Left there, this
requirement would name a first-class use case that its own refusals forbid —
**an unachievable-by-construction obligation, which is a worse defect than the
join key it closes**, because a stable key is a hazard an implementer can see
and an impossible requirement is one they will satisfy by inventing the hazard
back.

**THE MECHANISM IS AN AUTHORIZED, SCOPED LINKAGE DERIVATION, AND EVERY ADJECTIVE
IS LOAD-BEARING.** A realization SHALL provide cross-plane correlation only
through a derivation that is: **ISSUED BY THE IDENTITY PLANE**, which is the
only place linkage is permitted to live, and **UNDER AN ANCHORED CONSENT
CHECKPOINT**, on the same footing the ruled boundary already gives an off-chain
disclosure; **PER-ANALYSIS AND NEVER STABLE**, derived under a parameter unique
to the authorized analysis so that two analyses' derivations do not correlate
with each other or with anything outside them; **EXPIRING AND REVOCABLE**, so an
authorization that ends actually ends; **USABLE ONLY WITHIN THAT ANALYSIS**,
resolving no person and travelling to no other consumer; and **WRITTEN AS
LEAVES** at issuance and at use, on the served surface the requirement above
defines. The validator REFUSES a correlation path that is none of these.

**WHAT STAYS REFUSED IS UNCHANGED, AND THE HEADLINE ABOVE STAYS TRUE.** The
stable shared cross-plane key remains refused; a derivation minted anywhere but
the identity plane, or without an anchored consent checkpoint, or re-used across
analyses, is refused as that same key wearing a different name. **The identity
plane is still not READ BY the analysis**: the derivation is issued in advance
and under consent, the analysis runs over the record and demographic planes
alone, and no person-resolving identifier enters it — which is exactly what this
requirement's opening sentence claims and all it has ever claimed.

**AND CORRELATION IS A CONSENT-DEPENDENT ACT, SO THE FAIL-CLOSED DOCTRINE
REACHES IT — WHICH NARROWS WHAT THIS REQUIREMENT PROMISES ABOUT AVAILABILITY.**
Issuance authorizes; it does not immunize. A derivation is REVOCABLE, and a
revocation *"supersedes forward from the moment it is recorded and anchored"* on
the consent requirement's own terms, so every USE answers to the CURRENT
revocation state and not merely to the fact of issuance. Where that state cannot
be read — the identity plane unreachable, the permissioned plane unreachable —
**the CORRELATION is REFUSED**, on the same doctrine the consent requirement
states: an unevaluable answer never reads as permission, and a derivation
presented while its revocation state is unknown is exactly the unevaluable case.
A realization SHALL NOT treat a pre-issued derivation as self-authorizing
offline, because that is how a revoked authorization keeps working.

**WHAT IS UNAFFECTED BY REACHABILITY IS THE UNCORRELATED ANALYSIS, AND THAT IS
ALL THIS REQUIREMENT EVER CLAIMED.** Inspecting the record plane and the
demographic plane independently needs no derivation, no consent evaluation and
no identity plane, so it runs regardless — which is the headline above,
unchanged. What needs a derivation is the JOIN, and the join is consent-gated
end to end. **The refusal is scoped to the correlation and not to the run**: an
analysis whose correlation is refused still returns its per-plane results, and
says which part it could not perform rather than failing whole or silently
returning less.

**AND "SAYS WHICH PART" IS A DECLARED OUTCOME ON THE RESULT, NOT A COURTESY IN A
LOG LINE — SO IT IS GIVEN A SHAPE A VALIDATOR CAN CHECK.** An analysis result
SHALL carry a STATUS DISCRIMINATOR drawn from a CLOSED ENUMERATION, a value
outside that enumeration being REFUSED rather than passed through; where a
correlation was refused, the result SHALL additionally carry the NAMED
CORRELATION that was not performed and the GROUND it was refused on, **itself
from a NAMED ENUMERATION rather than free text** — the revocation state
unreadable, the consent revoked, the derivation refused; and the PER-PLANE
RESULTS SHALL be carried DISTINCTLY from the correlated output, so what was
produced without a join is never read as the join's answer. **A silently partial
result — one missing its correlation with no declared outcome — is REFUSED**, on
the same reasoning the anchoring requirements refuse an aggregate `anchored`
boolean: a consumer reads the value it is given and not the circumstance behind
it, so a result that merely omits what it could not do will be consumed as a
result that had nothing to add. Free text cannot carry this, because a ground a
validator cannot compare is a ground it cannot check. This requirement fixes
that the outcome is DECLARED, ENUMERATED and distinguishable; the record's field
names and its enumerated members are realization's, and named there.

**AND THE NEUTRAL LAYER DEFINES THE SHAPE, NOT THE OCCASION.** This capability
fixes what a lawful correlation path must BE; it does not say when a lane may be
authorized, who may authorize it, or against what standard — those are domain
law and domain judgement, and the neutrality requirement below keeps them in the
domain overlay. A capability that answered them would be writing one domain's
research-governance policy into a neutral contract.

**AND THE LANE IS A NAMED CONSUMER RATHER THAN AN EMERGENT PROPERTY.**
Meta-analysis across the record and demographic planes is a first-class use case
of this capability, carried from the same MedxChain notes' appendix (cited
above; now at `MedxSoft/MedxFactory@74bed502`, historical provenance only),
which observes
that the neutral family's tranche-three text does not yet name this consumer
though the anchored, segregated design already supports it. **What that support
reaches, and where it stops, is the block below**: the structure enables the
analysis to run without the identity plane; it does not de-identify the result.

**AND WHAT PLANE SEPARATION BUYS THAT LANE IS STATED WITHOUT OVERSTATEMENT,
BECAUSE NOT QUERYING THE IDENTITY PLANE IS NOT DE-IDENTIFICATION.** What the
segregation delivers is that the identity plane is NOT READ BY the analysis —
correlation being authorized in advance by the derivation above rather than
resolved during the run — that neither analyzed plane carries a direct
identifier, and that no anchored value serves as a cross-plane join key. What it does NOT deliver is a
DE-IDENTIFIED result, and this requirement SHALL NOT be read as delivering one:
the attributes that remain — the demographic values and the record-plane
material the analysis exists to read — can SINGLE OUT a person in combination,
and can be linked back to a record, with no direct identifier present anywhere.
**A result of this lane SHALL NOT be labelled, released or reused as
de-identified on the strength of plane separation alone.**

**THE DE-IDENTIFICATION DETERMINATION IS A SEPARATE, LATER, NAMED GATE, AND IT
IS THE DOMAIN OVERLAY'S TO NAME.** The estate already holds that this boundary
is *"a named gate, not an assumed property"* (`docs/knowledge-lifecycle-model.md`,
the de-identify gate), and the standard that determination is made against is
domain law and domain judgement — which the neutrality requirement below forbids
this capability to carry. So this capability names NO determination standard,
provides no path by which one is presumed, and SHALL NOT stand in for one:
absent the overlay's named determination, a plane-separated result remains
GOVERNED PERSONAL DATA and stays in the governed layer under the same custody as
the planes it came from. A realization that treats the lane's output as reusable
because the identity plane was not queried is REFUSED.

#### Scenario: an analysis runs across the record and demographic planes

- WHEN an analysis inspects the record and demographic planes independently, without correlating them and without the identity plane
- THEN it runs, and no DIRECT identifier is exposed because neither plane carries one
- AND that uncorrelated result is unaffected by whether the identity plane was reachable, because it needs no derivation and no consent evaluation
- AND the result is NOT thereby de-identified, and remains governed personal data until a named de-identification determination is made against it

#### Scenario: a correlation is attempted while the identity plane is unreachable

- WHEN an analysis holding a pre-issued linkage derivation attempts to correlate the two planes and the current revocation state cannot be read
- THEN the CORRELATION is REFUSED, because an unevaluable revocation never reads as permission and a pre-issued derivation is not self-authorizing offline
- AND the analysis still returns its per-plane results carrying an explicit CORRELATION-REFUSED outcome that names the correlation and its ground, rather than failing whole or silently returning less

#### Scenario: a refused correlation is returned as an undeclared partial result

- WHEN a correlation is refused and the analysis returns only its per-plane results, with no status discriminator distinguishing that from a result which had no correlation to add
- THEN it is REFUSED AS NON-CONFORMING, because a consumer reads the value it is given and not the circumstance behind it
- AND the status discriminator, the named omitted correlation and its enumerated ground are what make the three result shapes decidable apart by the result itself
- AND a result carrying a status value outside the closed enumeration, or a refusal ground written as free text, is REFUSED on the same rule

#### Scenario: a derivation is revoked while its analysis is still running

- WHEN a revocation for an authorized derivation is recorded and anchored partway through the analysis that holds it
- THEN further USE of that derivation is refused from that moment, because a revocation supersedes forward on the consent requirement's own terms
- AND what was already correlated is not recalled, and no claim of recall is made, because nothing already disclosed can be withdrawn

#### Scenario: an authorized analysis correlates the two planes

- WHEN an analysis holding a per-analysis linkage derivation issued by the identity plane under an anchored consent checkpoint correlates demographic rows with record rows
- THEN the correlation is PERMITTED within that analysis, and its issuance and its use are each written as leaves
- AND the derivation resolves no person, expires, is revocable, and is usable in no other analysis

#### Scenario: a linkage derivation is re-used across analyses

- WHEN a derivation issued for one authorized analysis is carried into a second one, or is derived so that two analyses' derivations agree
- THEN it is REFUSED, because a derivation that is stable across analyses is the shared cross-plane key under another name
- AND the per-analysis parameter is what keeps the refusal above from being reintroduced by convenience

#### Scenario: a correlation path is derived outside the identity plane

- WHEN a realization derives a cross-plane correspondence without the identity plane issuing it, or without an anchored consent checkpoint
- THEN it is REFUSED, because linkage lives only in the identity plane and an unauthorized derivation is a join key minted by whoever wanted one
- AND the refusal holds however the value is computed, since the defect is the missing authorization and not the arithmetic

#### Scenario: a plane-separated result is labelled de-identified

- WHEN a realization treats an analysis result as de-identified, releasable or reusable because the identity plane was not queried
- THEN it is REFUSED, because the absence of the identity plane removes the direct linkage and not the identifying power of the attributes that remain
- AND the domain overlay's named de-identification determination is what carries that label, this neutral capability naming no standard for it and standing in for none

#### Scenario: a demographic-plane entry carries a direct identifier

- WHEN an entry in the demographic plane carries an identifier that resolves a person
- THEN it is REFUSED by a named check
- AND the refusal is structural, on the identifier's declared resolution rather than on its apparent content

#### Scenario: one key is shared across planes for convenience

- WHEN a realization uses one derived key across the record, demographic and identity planes so the planes can be joined easily
- THEN it is REFUSED, because a shared key makes the segregation nominal
- AND per-plane keys derived under per-plane salts are used instead

#### Scenario: re-identification is attempted through the anchored commitment

- WHEN a holder of an anchored commitment attempts to use it to join a demographic entry to an identity entry
- THEN the join fails, because the anchored commitment is derived under the record's own salt held in the governed layer
- AND no plane's key is derivable from the anchored value

### Requirement: This capability is neutral and names no domain semantics

openxFactory SHALL keep this capability DOMAIN-NEUTRAL, and SHALL NOT define,
name or encode any domain's record kinds, regulators, clinical or financial
semantics, or product surfaces in its contracts, schemas, field names or finding
codes. Domain products instantiate the capability through DIGEST-PINNED domain
overlays owned by their own repositories, on the pattern the estate already runs
for the omnigent family. A capability that fit one domain would belong in that
domain's repository, which is the staged topic's own neutrality argument and the
reason the two domain mappings are stated as a proof rather than as consumers
under obligation.

**THE MAPPING IS NAMED HERE AND AUTHORED ELSEWHERE.** MedxChain and HealthLinc
are MedxFactory's instantiations of this capability; LedgerLinc is
LedgerxFactory's. The MedxChain notes cited above — now at `MedxSoft/MedxFactory@74bed502`,
cited here as historical provenance only — read as an early, domain-specific
sketch of this same shape, PREDATING the neutral family. No interval is stated
here: nothing in this requirement turns on how long, and the dates the reader
would measure it from belong to the vendored document rather than to contract
text. This capability names those instantiations to show the shape occurs twice;
it authors no content for any of them, and no domain is obliged to adopt a
chain.

**THE STRUCTURAL REFUSALS ARE WHAT MAKES NEUTRALITY AFFORDABLE.** Because the
payload refusal and the identifier refusal above are shape-based rather than
semantic, this capability enforces the regulated-content boundary without
carrying a single domain term in its checks. A domain overlay MAY add stricter
domain-specific refusals on top; it SHALL NOT relax a refusal made here.

#### Scenario: a domain record kind is proposed for this capability

- WHEN a domain-specific record kind is proposed as a contract of this capability
- THEN it is REFUSED, and it lands in that domain's digest-pinned overlay instead
- AND the neutral capability gains no field, code or vocabulary naming the domain

#### Scenario: a domain overlay adopts the capability

- WHEN a domain repository pins this capability by commit and per-file digest and adds its own record kinds on top
- THEN the overlay is conformant, and the neutral contracts are unchanged by the adoption
- AND the domain's own regulator and semantics live entirely in the overlay

#### Scenario: an overlay relaxes a neutral refusal

- WHEN a domain overlay admits a record the neutral validator refuses
- THEN the overlay is non-conformant, because an overlay may add refusals and never remove them
- AND the neutral refusal is what the pin is for

#### Scenario: a domain is asked to adopt the chain

- WHEN a domain repository declines to instantiate this capability
- THEN nothing in this capability obliges it, and no existing capability of that domain is made non-conformant
- AND the two named mappings remain a neutrality proof rather than an obligation

