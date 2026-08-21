# Design: Trust Anchor — one neutral contract, two realizations

## Context

Organized from the staged topic
`openxFactory:staging:pki-trust-anchor-plane`
(`ideation/staging/pki-trust-anchor-plane/pki-trust-anchor-plane.md`), which
records Brett Heap's rulings of 2026-08-21 in the xFactory family session:
R8 (two PKIs, one contract), R2 (the seam with the active OpsxFactory change
`add-openxpki-qa-image-pipeline`), R1 (install repos own the deployable
runtime — ruled once for this topic and its identity sibling), and R7 (the
three-way ownership split, on the `github-administration-plane` precedent).

The forcing fact is not a product decision. It is that two certificate
authorities are converging on one family with no shared statement of what a
certificate is worth:

| Realization | Population | Status |
| --- | --- | --- |
| Microsoft Intune Cloud PKI | device / host-broker certificates | live canary track |
| OpenXPKI | Opensoft production core | planned; QA image pipeline in flight |

The canary is the interesting one, because it is where the first obligation
came from and because it is the harder conformance case: we do not operate
it. A contract that only a self-hosted authority can pass would classify the
live track as non-conformant for reasons that have nothing to do with trust.

## Decisions

### D1 — The contract is product-agnostic (R8)

Requirement text names no product, no protocol, and no vendor object model.
Reasoning: written around either realization, the contract would encode that
product's model of an authority — a SCEP-profile-and-managed-root shape or a
realm-and-token shape — and the other realization would fail on vocabulary
rather than on trust. What both owe is identical: a named anchor, evidence
that issuance happened under the authority claimed, declared custody of
chain material, and a revocation path that reaches whatever the certificate
authorized.

The corollary is a discipline, not a slogan: each requirement is phrased as
an obligation on the RECORD or on the WORKFLOW, never on a mechanism. That
is what makes the honest-shortfall rule (D6) expressible at all.

### D2 — Systems trust anchors; certificates are trusted only through them

An anchor is the governed record; a certificate is trusted derivatively.
Reasoning: this is the only framing in which revocation and rotation have
somewhere to attach. Trusting certificates individually produces a trust set
nobody can enumerate, and an anchor withdrawal that does not actually
withdraw anything.

Consequence carried into the schema work: an anchor record's validity window
bounds its subordinates, and a subordinate's own remaining validity may not
outlive its anchor's standing.

### D3 — Renewal is a rebind obligation, and the failure belongs to the issuer

The canary's auto-renew / keyCredential trap, generalized. A renewal that
produces new key material leaves every binding made against the old material
pointing at a key the holder no longer uses; the directory keyCredential in
the live case is one instance of a general shape. The contract therefore
states two things the trap taught:

1. Renewal is INCOMPLETE until each dependent binding is re-bound and the
   rebind evidenced.
2. The failure is attributed to the ISSUING WORKFLOW, never to the dependent
   that stopped authenticating.

Reasoning for the attribution half — which is the part that is easy to skip
and expensive to omit: the dependent was configured correctly when it was
configured. Attributing the outage to it produces an incident report that
teaches nothing, a fix that is a re-bind with no obligation attached, and a
guarantee of recurrence at the next renewal. Attribution is where the
recurrence gets prevented.

An automatic renewal is not exempt. Unattended issuance owes the same
rebinds as a requested one, and the absence of an error is not evidence that
nothing broke — the whole hazard is that the failure is silent.

### D4 — Dependent bindings are recorded, or D3 is unenforceable

The rebind obligation has no teeth unless the set of dependents is
computable before the renewal. So dependent bindings are recorded against
the certificate, and a dependent discovered by an outage is a DEFECT OF THE
RECORD, not merely an incident.

This decision is not in the staged topic's seven-point sketch. It is added
here because working through the topic's open question 3 (what evidences a
rebind, given the failure mode is silent) showed the sketch had an
unenforceable requirement: you cannot evidence the completion of an
obligation over a set you never enumerated. Recording the dependents is the
smallest addition that makes the rest checkable.

### D5 — Compose with `openxwallet`, twice, rather than restate it

**Revocation.** The ratified requirement "Revocation propagates through the
chain" already carries the mechanism: revoking a parent kills what derived
from it, checked at exercise rather than trusted from issuance. The
trust-anchor contract states the OBLIGATION (a revoked certificate's
downstream authority dies with it, within a declared bounded window,
evidenced) and rides that mechanism.

**Custody.** The ratified requirement "Custody is declared and bounds what a
signature evidences" — a closed set, with what each member evidences stated,
capping the authority a holder may hold — is exactly the right model for
chain custody. The canary's TPM-bound broker certificate is the isolated
case; a software-stored service certificate is the host-readable one. The
contract expresses chain custody as declared tiers that DERIVE what the
certificate evidences, not as a free-text field.

Reasoning for composing rather than defining: a second revocation or custody
vocabulary would lag the first one and would win locally by proximity —
whoever is writing PKI code would reach for the PKI words. One mechanism,
two contracts pointing at it.

### D6 — Declared degraded obligations, not a contract only one product can pass

Each realization publishes a conformance declaration: obligation by
obligation, satisfied / partial / cannot, with reasons. An UNDECLARED
shortfall is non-conformance; the identical shortfall, declared, is
conformant.

Reasoning: the alternatives are both worse. A contract pitched at what a
self-hosted authority can evidence makes the live canary permanently
non-conformant, which teaches everyone to ignore conformance. A contract
pitched at the weakest realization's floor lets the self-hosted authority
under-evidence for free. Declaring the gap keeps the contract honest about
what it actually knows, and it makes raising assurance a change to the
declaration — visible, reviewable — rather than a quiet claim. Same move as
`openxwallet`'s custody ruling and LedgerxFactory's
`package_content_execution_mode`: record the mode, let consumers read it,
refuse claims the recorded mode cannot support. The pattern precedent inside
this family is the `github-administration-workflow` plan-tier ladder's
degraded-capability note.

The guard that keeps this from becoming a loophole is in the requirement
text: a declared gap is NOT permission to assert the missing evidence, and
declaring a gap afterwards does not validate claims made while it was
silent.

### D7 — The image-custody seam, and one time-critical amendment (R2)

The split between the active OpsxFactory change and the new install repo
runs along **custody**, not convenience:

- **Stays in `opensoft/Opensoft-Tenant`**: the image build, the release /
  package / configuration / base-image pins, the offline and integration
  test harness, and the QA build/pull/scan helpers producing the immutable
  ACR digest. Deciding what binary a tenant's certificate authority runs is
  a tenant trust decision; moving it out of the tenant repo moves a trust
  decision away from its owner.
- **Moves to `xFactory-OpenXPKI-Install`**: the QA deployment topology
  manifests (server / client / web), which CONSUME the pinned digest rather
  than produce it, plus per-client instantiation at
  `config/clients/<tenant>/runtime-manifest.yaml`.

Therefore `add-openxpki-qa-image-pipeline` must be amended **before it
ratifies**, in the three places that currently home the QA deployment
manifests in the tenant repo: its Impact section, its "What Changes" bullet
3, and its tasks §3. Before rather than after, because the Impact section is
what a reviewer reads to decide whether the boundary is right — ratifying
first would ratify the wrong boundary and then correct the record, which is
the expensive order.

Note the scope discipline this seam depends on: the ACR-mirror / digest-pin
convention governs native-manifest workloads, which is precisely what these
QA manifests are. The convention is the reason the install repo consumes a
digest and is not permitted to hold pinning logic of its own.

### D8 — The install repo is admitted as its OWN requirement, not by amending the enumeration

The staged topic's R1 says repo creation "rides `repo-boundary-governance`
through an OpenSpec change, whose 'Install repository scope' requirement
enumerates the admitted install repos by name and must be amended to add
both new scopes." This change deliberately does it differently: an ADDED
requirement, "OpenXPKI install repository boundary", on the ratified
avatar-client template ("Neutral avatar-client repository boundary" +
"Deferred aggregation and web-console integration").

Three reasons, in order of weight:

1. **Two parallel changes cannot both replace one requirement.** A MODIFIED
   delta wholesale-replaces the named requirement and only it, restating all
   its scenarios. The sibling `add-identity-brokering` needs the same
   admission for `xFactory-Keycloak-Install` in the same window. Two changes
   each replacing "Install repository scope" produce a merge in which one
   repo's admission silently disappears — the later delta's restatement wins
   and it does not know about the earlier one. ADDED requirements compose;
   replacements race.
2. **The enumeration cannot carry what a repository admission needs.**
   "Install repository scope" is a two-scenario requirement about where
   Hermes and Omnigent runtime procedure is homed. A repository boundary
   needs the creating successor change named, the owned surface enumerated,
   explicit MUST NOTs, the custody counterparty named, and aggregation
   admission held back as a separate reviewed act. The avatar-client
   requirements are the ratified template for exactly that, one requirement
   per repository.
3. **It keeps aggregation admission a separate act.** The avatar-client
   pattern's "Deferred aggregation" discipline is preserved verbatim in
   scenario 3: creating the repository is not pinning it.

What is deferred by this decision: refreshing the "Install repository scope"
enumeration so it lists all admitted install repos in one place. That is
bookkeeping over ratified text, best done once after both install repos
exist, by a single change that can restate the requirement without racing
anyone. It is named in tasks §8.

### D9 — One capability, not a core plus per-product profiles

The topic's open question 4 asked whether two realizations justify the
`openxwallet` / `openxwallet-agent-profile` seam. They do not, yet: the
rule-of-three has not fired, and a profile seam built for two realizations
would fix the axis of variation as PRODUCT when the real axis is
OBLIGATION SATISFACTION — which D6 already handles inside one capability.
If a third realization arrives that differs structurally rather than in
what it can evidence, a profile split is a NEW capability over this core,
not a modification of it. Recorded so it is a decision rather than an
omission.

### D10 — Authority material has no QA exemption

`credential-contracts` already owns credential records with declared
custody and vault bindings; this contract adds only the explicit refusal of
the exemption everyone reaches for. A demonstration or QA authority's
private key is an authority key, and a committed one is compromised —
including in reversible encodings, which is where this usually goes wrong.
Stated because the OpenXPKI realization arrives through a QA pipeline, which
is exactly the context in which "it's only QA" gets said.

## Open questions carried, with a recommendation each

### OQ1 — What the contract requires of issuance evidence (hardest)

Flagged hardest in the staged topic. The strictest honest requirement is a
per-certificate record; the weakest useful one is a per-policy attestation
plus the authority's own log. A cloud-managed authority constrains what we
can extract.

**Recommendation:** keep the requirement stated as what the evidence must
ESTABLISH (anchor, admitted authority, request provenance, time) and let D6
carry the difference — per-certificate records where the authority exposes
them, and a declared floor of per-policy attestation plus the authority's
log where it does not. Reject the tempting middle option of writing the
weaker form into the requirement itself: that would let the self-hosted
authority, which can do better, stop at the floor. Settle the declaration's
shape before the schema is authored.

### OQ2 — Chain custody tiers: how many, and closed? (hardest)

Candidate members from the topic: hardware-isolated (TPM / HSM),
host-readable, operator-escrowed. Whether operator escrow is a custody tier
or a separate relationship is genuinely open and touches the
`client-credential-escrow-registry` topic.

**Recommendation:** a CLOSED enumeration with derived `evidences`, following
the `openxwallet` precedent, and **operator-escrowed modelled as a
relationship on the credential record rather than as a custody tier**.
Reasoning: escrow answers "who else can obtain this key", which is
orthogonal to "can the using host read it" — an HSM-held key with an escrow
copy is not the same object as a host-readable key, and collapsing them into
one axis makes both claims unreadable. Two axes, each declared.

Carry forward the `openxwallet` lesson explicitly: a set that fails to
distinguish a key readable by its own host from one isolated from it lets the
first claim the second's authority, which quietly re-opens the hole the rule
was written to close. Settle before the schema, and settle it with the
escrow topic in the room.

### OQ3 — Who owns the rebind obligation, and what evidences a silent failure

**Recommendation:** the obligation sits on the ISSUING WORKFLOW (D3); the
holder/consumer owns only the duty to DECLARE its bindings (D4). Evidence is
a post-renewal verification per dependent binding — an authentication or
binding-read against the new material — recorded on the renewal record. A
renewal is reportable as successful only when every enumerated dependent
carries that evidence. This turns a silent failure into a missing artifact,
which is the only kind of silent failure a validator can catch.

### OQ4 — One capability or two conformance profiles

**Recommendation:** one, per D9. Revisit when a third realization arrives
and only if it differs structurally rather than in what it can evidence.

### OQ5 — Where the cloud-PKI canary's governed record lives

It is OpsxFactory-administered platform work, but the device population is
the worker fleet's. **Recommendation:** the record lives with the
OpsxFactory `pki-administration` successor (impact item 1), and the seam
with `add-cloudpc-worker-fleet-management` plus the worker-enrollment
broker's device identity is checked BEFORE that successor is scoped, not
during. The OpsxFactory `incident-diagnostics-and-intervention` staged topic
already asks how TPM-backed keys are issued, attested, and rotated; that
question is answered once, in this contract's vocabulary, rather than twice
in two workflows.

## What this deliberately does not do

- No certificate authority, no anchor, no key, no issuance or revocation
  service, no deployment topology, no runtime. Contracts, examples, and a
  validator.
- No re-solving of the demonstration-image hazard. The active
  `add-openxpki-qa-image-pipeline` owns it; this change touches it only
  through the boundary amendment in D7.
- No obligation on any domain to operate a certificate authority, and no
  existing capability modified in a way that requires action from a domain
  that has none.
- No product profiles (D9), no escrow contract (OQ2 defers it to the escrow
  topic), and no administration workflow — that is the OpsxFactory
  successor's, by R7.

## Risks

**A declaration nobody audits.** D6 is honest only if the declarations are
true. A validator can check that every obligation is addressed and that no
claim exceeds what the declaration supports; it cannot check that the
declared state is the real one. Mitigation is the same as `openxwallet`'s:
the declaration is contract content, so a false one is a governance finding
rather than a misconfiguration.

**The degraded-obligation rule as a loophole.** If declaring a gap is
cheaper than closing one, everything gets declared. The requirement's guards
(a declared gap is not permission to assert the missing evidence; late
declaration does not validate earlier claims) are the floor; the real
control is that a consumer can refuse a certificate for a declared gap, so
declaration has a cost at point of use.

**Dependent-binding registry completeness.** D4 is only as good as the
enumeration, and the first realizations will discover dependents they did
not record. The requirement makes that discovery a record defect with a
correction, which converts an unbounded unknown into a shrinking list —
but the first renewals after adoption are the exposure window, and the
canary is already inside it.

**Two realizations, one contract, in sequence.** The live canary conforms
retroactively and the self-hosted authority conforms by construction. If the
canary's declaration turns out to be mostly gaps, the contract will look
like it was written for the planned realization. Answering OQ1 with the
declaration floor spelled out — before the schema — is what keeps that from
being decided by omission.
