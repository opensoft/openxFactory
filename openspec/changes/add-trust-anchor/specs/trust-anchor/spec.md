# trust-anchor Specification (delta)

## ADDED Requirements

### Requirement: Systems trust anchors, never individual certificates

openxFactory SHALL define a TRUST ANCHOR as a governed record naming the
anchor's identity, its position in a chain, its validity window, and the
declared custody of its private key material, and SHALL require that a
governed system's trust decision name an ANCHOR rather than an individual
certificate. The anchor record references key material and never carries
it. A certificate is trusted only through an anchor record the evaluating
system already holds; a certificate accepted on its own strength is an
untrusted certificate however well-formed it is, and a chain terminating
in no held anchor is refused with the missing anchor named rather than
accepted for resembling one.

#### Scenario: an anchor record is validated

- WHEN an anchor record is validated
- THEN it names identity, chain position, validity window, and declared custody
- AND a record carrying private key material is a validation failure

#### Scenario: a certificate arrives without an anchor

- WHEN a governed system evaluates a certificate whose chain terminates in no anchor record it holds
- THEN the certificate is refused and the missing anchor is named
- AND well-formedness is not accepted in place of an anchor

#### Scenario: an anchor leaves its validity window

- WHEN an anchor's validity window closes or its record is withdrawn
- THEN certificates chaining to it stop being trusted from that moment
- AND a certificate's own remaining validity does not extend the anchor's

### Requirement: A certificate issues only under recorded authority

openxFactory SHALL require every issuance to happen under a RECORDED
AUTHORITY — a grant or policy reference the anchor's record admits — and
SHALL require an ISSUANCE EVIDENCE record establishing which anchor issued,
under which authority, on whose request, and when. The obligation is stated
as what the evidence MUST ESTABLISH and never as the mechanism that
produces it, so a realization operating a certificate authority the family
does not itself run can satisfy it from whatever that authority exposes.
Where the authority exposes less than the obligation requires, the
realization declares the shortfall under the declared-obligation
requirement in this capability; it does not record evidence it does not
have, because an asserted-but-unestablished record is worse than a declared
gap.

#### Scenario: issuance with no admitted authority

- WHEN a certificate is issued with no grant or policy reference the anchor's record admits
- THEN the issuance is recorded as unauthorized
- AND the certificate's validity does not ratify it retroactively

#### Scenario: the issuing authority is not operated by the family

- WHEN a realization cannot extract per-certificate request provenance from the issuing authority
- THEN it declares the shortfall and records only what it can establish
- AND asserting unestablished provenance is a validation failure

#### Scenario: an unexplained certificate is found

- WHEN a certificate exists under an anchor with no issuance evidence record
- THEN the question "should this exist?" is answered as UNANSWERED, not as yes
- AND the certificate is treated as a candidate for revocation until the record is produced

### Requirement: Declared chain custody bounds what a certificate evidences

openxFactory SHALL require every anchor and certificate record to DECLARE
the custody of its private key from a defined set, and SHALL derive what
the certificate EVIDENCES from that declaration rather than from the
certificate's own contents, composing with `openxwallet`'s ratified rule
that custody caps what a signature evidences instead of restating a second
custody model. A key readable by the host that uses it evidences that the
HOST acted; only custody isolating the key from that host evidences that
the named holder acted. A certificate whose declared custody is host-held
SHALL NOT be presented as, or accepted for, an assurance that requires
hardware-bound custody, and raising assurance is a custody change rather
than a claim.

#### Scenario: a host-held key is offered for hardware-bound assurance

- WHEN a certificate declaring host-held custody is offered for an authority requiring hardware-bound custody
- THEN the request is refused with the custody ceiling named
- AND the refusal names custody rather than the certificate's contents

#### Scenario: custody is undeclared

- WHEN a certificate record carries no custody declaration
- THEN it evidences the weakest member of the defined set
- AND it may not hold authority above that member

#### Scenario: the audit says what was evidenced

- WHEN an act authenticated by a certificate is audited
- THEN the record carries the custody in force at the time of the act
- AND a reader can tell whether the holder or its host was evidenced

### Requirement: Renewal that changes key material is a rebind obligation

openxFactory SHALL treat a renewal producing new key material as
INCOMPLETE until every dependent binding that referenced the superseded
material has been re-bound and each rebind evidenced, and SHALL place that
obligation on the ISSUING WORKFLOW. A renewal that succeeds at the
authority while leaving a dependent binding pointing at superseded key
material MUST be recorded as a failure of the issuing workflow and MUST NOT
be recorded as a failure of the dependent that stopped authenticating: the
dependent was configured correctly when it was configured, and the renewal
is what changed beneath it. Renewal that is automatic is not therefore
exempt — an unattended renewal owes the same rebinds as a requested one,
and silence is not evidence.

#### Scenario: automatic renewal breaks a dependent binding

- WHEN a certificate renews automatically with new key material and a dependent authority binding still references the previous key
- THEN the renewal is recorded as failed with the unbound dependent named
- AND the failure is attributed to the issuing workflow, not to the dependent

#### Scenario: rebind is evidenced before renewal is reported complete

- WHEN a renewal is reported
- THEN each dependent binding carries evidence of re-binding to the new material
- AND a renewal with an unevidenced dependent is not reportable as successful

#### Scenario: renewal preserves the key

- WHEN a renewal reuses the existing key material
- THEN no rebind obligation arises and the record says so explicitly
- AND the absence of rebind evidence is not read as an omission

### Requirement: Dependent bindings are recorded against the certificate

openxFactory SHALL require every authority binding that references a
certificate's key material — in any system, inside the family or outside
it — to be recorded against that certificate's record, so the set of
rebind obligations a renewal will create is computable BEFORE the renewal
happens. A dependent binding discovered only when it broke SHALL be
recorded as a defect of the certificate record and the record corrected,
because the rebind obligation is unenforceable against bindings no record
names, and the failure mode is silent precisely because nothing was
looking.

#### Scenario: the rebind set is computed before renewal

- WHEN a renewal is planned
- THEN the certificate's record enumerates every dependent binding to re-bind
- AND a renewal planned against a record known to be incomplete is refused

#### Scenario: an unrecorded dependent surfaces

- WHEN authentication fails at a binding no record named
- THEN the omission is recorded as a defect of the certificate record and the binding is added
- AND the incident is not closed by re-binding alone

### Requirement: Revocation propagates to the authority the certificate supported

openxFactory SHALL require that revoking a certificate or an anchor revoke
the authority that certificate or anchor supported, within a declared
bounded window and with the propagation evidenced, and SHALL realize the
propagation through `openxwallet`'s ratified revocation-through-derivation
rule rather than defining a second revocation vocabulary that would lag it.
Revocation standing SHALL be checked at USE rather than trusted from
issuance, and revoking an anchor SHALL revoke transitively what its
subordinate certificates supported. A revocation whose propagation cannot
be evidenced within the declared window SHALL be escalated as an open
exposure rather than recorded as complete.

#### Scenario: revoking an anchor kills what it supported

- WHEN an anchor is revoked
- THEN the authority its subordinate certificates supported is revoked transitively within the declared window
- AND an exercise attempt against any of it is refused

#### Scenario: validity at issuance is not current standing

- WHEN a certificate valid at issuance is presented after revocation
- THEN the presentation is refused
- AND issuance-time validity is not accepted as evidence of current standing

#### Scenario: propagation cannot be evidenced

- WHEN the declared window closes with no evidence that a dependent authority was revoked
- THEN the revocation is recorded as incomplete and escalated as an open exposure
- AND it is not reported as complete on the strength of the revocation request

### Requirement: Authority material and issuance credentials are credential records, never committed

openxFactory SHALL require private key material for an anchor, together
with every credential authorizing issuance, revocation, or anchor
administration, to exist only as a `credential-contracts` record with
declared custody and a vault binding, at the strictest custody tier the
family operates, and SHALL prohibit committing such material to any
repository in plaintext or in any encoding a reader can reverse. This
admits NO exception for test, demonstration, or QA material: a
non-production authority's key is still an authority key, and a committed
one is a compromised one. Workflows that must issue or revoke receive the
credential BY REFERENCE into ephemeral scope, per `credential-contracts`,
and never into their own storage.

#### Scenario: QA key material is proposed for a repository

- WHEN authority key material or an issuance credential is added to a repository, in plaintext or in a reversible encoding
- THEN validation MUST reject it and route it to a credential record with a vault binding
- AND "QA only" or "demonstration only" is not accepted as a reason

#### Scenario: issuance authority is brokered

- WHEN a workflow needs to issue or revoke
- THEN it receives the credential by reference into ephemeral scope
- AND the material is not written to the workflow's own storage or logs

### Requirement: A realization declares the obligations it cannot meet

openxFactory SHALL require each realization of this capability to publish a
CONFORMANCE DECLARATION stating, obligation by obligation, which of this
capability's obligations it satisfies fully, which it satisfies partially,
and which it cannot satisfy — with the reason in each case — and SHALL
treat an UNDECLARED shortfall as non-conformance even where the identical
shortfall, declared, would be conformant. A consuming capability SHALL be
able to read the declaration and refuse a claim the declaration cannot
support. A declared gap SHALL NOT be read as permission to assert the
missing evidence, and a realization operating an authority the family does
not run SHALL remain conformant on the strength of its declaration rather
than being excluded by obligations only a self-hosted authority could meet.

#### Scenario: a managed authority cannot evidence everything

- WHEN a realization runs on a certificate authority whose internals the family does not operate
- THEN its declaration names each obligation it cannot fully satisfy and why
- AND it remains conformant on the strength of that declaration

#### Scenario: a silent gap is found

- WHEN an obligation is unsatisfied and undeclared
- THEN the realization is non-conformant for the silence
- AND declaring the gap afterwards does not validate the claims made while it was silent

#### Scenario: a consumer reads the declaration

- WHEN a consumer requires an obligation the realization declares it cannot satisfy
- THEN the consumer refuses the certificate for that use with the declared gap named
- AND the gap is not closed by the realization asserting the evidence instead
