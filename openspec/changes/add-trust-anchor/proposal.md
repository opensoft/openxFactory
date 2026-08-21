---
code_surface: openxFactory (a NEW `contracts/trust-anchor/` family — trust-anchor record, certificate record with declared chain custody, issuance-evidence record, dependent-binding record, renewal/rebind-evidence record, revocation-propagation record, and realization conformance declaration — plus packaged positive and negative examples and the canonical `scripts/validate-trust-anchor.py`; registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive bundle cut). No certificate authority, no key, no issuance service, no deployment. The OpsxFactory `pki-administration` workflow capability, the `xFactory-OpenXPKI-Install` repository and its QA deployment topology, the aggregation pin, and the governed record for the live cloud-PKI canary are successor realization changes named in the impact map, NOT this change's surface.
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
Status: ratified
Ratified by: Brett Heap, 2026-08-21 — "ratify both proposals"; all design decisions adopted as written; OQ1 ruled as recommended (issuance evidence stays an establish-obligation with a declared floor, set before schema authoring per tasks 4.2) and OQ2 ruled as recommended (closed custody enumeration with derived evidences; operator escrow is a relationship on the credential record, not a custody tier, settled with client-credential-escrow-registry per tasks 4.1)
---

# Proposal: add-trust-anchor

## Why

The family is about to run **two certificate authorities in production
service**, for two different populations, from two different vendors — and
only one of them was ever discussed as "our PKI". There is no shared
contract, and whatever we require of a certificate is therefore about to be
written twice.

**One realization is already live.** Microsoft Intune Cloud PKI issues
device and host-broker certificates today: a tenant root CA
(`Opensoft xFactory Root CA`), an issuing CA, SCEP profiles, and a
TPM-bound broker certificate in service. It is the canary, and it already
contributed the first hard-won obligation the hard way — its
**auto-renew / keyCredential-rebind trap**. A certificate that renews
automatically produces new key material, and the directory keyCredential
that bound authority to the *previous* key keeps pointing at a key the
holder no longer uses. Authentication that was configured correctly stops
working, silently, and the thing that broke is not the thing that changed.

**The other realization is planned.** OpenXPKI is intended for the Opensoft
production core, and the upstream Docker image is explicitly a
demonstration artifact published with mutable tags. That specific hazard is
already being handled: the active OpsxFactory change
`add-openxpki-qa-image-pipeline` adds a tenant-owned build pinning the
release, package metadata, configuration snapshot, and base image, and
produces an immutable ACR digest with QA acceptance evidence. This proposal
does not re-solve that, and deliberately does not touch it beyond the
boundary amendment named below.

**Neither track is the contract.** The contract is what a governed system
may assume about a certificate it trusts, and it has to hold for a
cloud-managed authority we do not operate *and* for a self-hosted authority
we do. Written around either product it would encode that product's model
of a CA — a SCEP-profile-and-managed-root shape, or a realm-and-token shape
— and the other realization would be non-conformant for reasons that have
nothing to do with trust.

Origin: staged topic `openxFactory:staging:pki-trust-anchor-plane`, its
exit 1, recording Brett Heap's rulings of 2026-08-21 (R8, R2, R1, R7).

## What Changes

- **ADD the neutral `trust-anchor` capability** — product-agnostic, eight
  requirements:

  - **Systems trust anchors, never individual certificates.** An anchor is
    a governed record: identity, chain position, validity window, declared
    custody. It references key material and never carries it.
  - **A certificate issues only under recorded authority**, with issuance
    evidence establishing which anchor, under which authority, on whose
    request, and when — stated as what the evidence MUST ESTABLISH rather
    than as a mechanism, so an authority whose internals we do not own can
    satisfy it, and declaring a shortfall beats asserting evidence we do
    not have.
  - **Declared chain custody derives what a certificate evidences**,
    composing with `openxwallet` rather than restating it: a host-readable
    key evidences that the HOST acted, and a host-held certificate may not
    be accepted for an assurance requiring hardware-bound custody.
  - **Renewal that changes key material is a rebind obligation** — the
    canary's trap generalized. Every dependent binding on the superseded
    key is a named re-bind, evidenced, and a renewal that breaks a
    dependent binding is a failure of the ISSUING WORKFLOW, never of the
    dependent that stopped authenticating.
  - **Dependent bindings are recorded against the certificate**, so the
    rebind set is computable before a renewal rather than discovered by an
    outage. This is what makes the previous requirement enforceable.
  - **Revocation propagates to the authority the certificate supported**,
    within a declared bounded window, evidenced, riding `openxwallet`'s
    ratified revocation-through-derivation rule; checked at use, never
    trusted from issuance.
  - **Authority key material and issuance credentials are
    `credential-contracts` records**, custody declared, vault-bound, never
    committed — with no exception for QA or demonstration material, because
    a QA authority's key is still an authority key.
  - **A realization declares the obligations it cannot meet.** An
    undeclared shortfall is non-conformance; the identical shortfall,
    declared, is conformant. This is what lets one contract cover both
    realizations honestly instead of one that only a self-hosted authority
    can pass.

- **ADD one requirement to `repo-boundary-governance`** — the OpenXPKI
  install repository boundary, on the ratified avatar-client template: a
  private, independently released `xFactory-OpenXPKI-Install` created by
  the `implement-openxpki-install-repo` successor change, aggregation path
  `installs/openxpki-install`,
  owning the server / client / web QA deployment topology and per-client
  instantiation, consuming ONLY the digest-pinned image whose custody stays
  in `opensoft/Opensoft-Tenant`, and containing no build sources, secrets,
  or key material. Aggregation admission remains a separate reviewed act.

- **No certificate authority, no anchor, no key, no issuance service, no
  deployment, no runtime.** Contracts, examples, and a validator.

## Capabilities

### New Capabilities

- `trust-anchor`: the neutral trust contract for the family's certificate
  infrastructure — anchors as governed records, issuance under recorded
  authority with evidence, declared chain custody deriving what a
  certificate evidences, renewal-as-rebind with recorded dependents,
  revocation propagation composing with `openxwallet`, authority material
  as a `credential-contracts` record, and the declared-degraded-obligation
  rule that keeps one contract honest across two realizations.

### Modified Capabilities

- `repo-boundary-governance`: one ADDED requirement admitting the OpenXPKI
  install repository scope. Additive — no existing requirement is restated
  or replaced (see design decision D8).

## Impact

- **New code (this change)**: one contract family, packaged positive and
  negative examples, one canonical validator, and manifest / CHANGELOG
  registration at the next additive bundle. No runtime behavior changes.
- **Composes with, and does not duplicate**: `openxwallet` (revocation
  propagation, and the declared-custody-caps-evidence model), and
  `credential-contracts` (authority material and issuance credentials as
  records with declared custody and vault bindings, distributed by
  reference into ephemeral scope).
- **REQUIRED pre-ratification amendment elsewhere — the one time-critical
  item.** The active OpsxFactory change `add-openxpki-qa-image-pipeline`
  must be amended **before it ratifies**, in three places that today name
  `opensoft/Opensoft-Tenant` as the home of the QA deployment manifests:
  its **Impact** section, its **"What Changes" bullet 3**, and its
  **tasks §3**. The deployment-manifest half of that scope belongs to
  `xFactory-OpenXPKI-Install`; the image-custody half stays exactly where
  it is. The amendment is small, and it must land before ratification
  rather than after, because the Impact section is what a reviewer reads to
  decide whether the boundary is right. Amending after ratification would
  ratify the wrong boundary and then correct the record.
- **Successor realization changes** (each pins the released bundle):
  1. **OpsxFactory `pki-administration`** — a workflow capability, sibling
     of `exchange-administration`, `aks-administration-workflow`,
     `github-administration-workflow`, and `business-central-administration`
     rather than a profile of one of them, with the new certificate-
     authority service-subject kind registered in lockstep (`customer-kinds`
     **and** the Hermes template **and** `stack.yaml`, grant ceilings in
     `credentials/requirements.yaml`). Developed in the OpsxFactory staged
     topic `OpsxFactory:staging:identity-pki-administration`, which is
     shared with the identity half because both need the same
     service-subject registration work.
  2. **`xFactory-OpenXPKI-Install` creation** — `implement-openxpki-install-repo`,
     the successor change this proposal's `repo-boundary-governance`
     requirement names:
     create the repository, move the QA deployment topology per the
     custody split, and land the first
     `config/clients/<tenant>/runtime-manifest.yaml`.
  3. **Aggregation pin** — `installs/openxpki-install`, a separate reviewed
     change recording path, remote, visibility, exact validated commit,
     checkout, compatibility, update, and rollback.
  4. **The cloud-PKI canary's governed record** — where the live device and
     host-broker certificate track is recorded, which needs the seam with
     `add-cloudpc-worker-fleet-management` and the worker-enrollment
     broker's device identity checked first. The OpsxFactory
     `incident-diagnostics-and-intervention` staged topic already asks how
     TPM-backed keys are issued, attested, and rotated; that question is
     answered by this contract once, not twice.
- **Sibling proposal, same session, same rulings**: `add-identity-brokering`
  (staged topic `openxFactory:staging:identity-brokering-plane`) carries the
  neutral persona/claims contract and its own install-repository boundary
  requirement for `xFactory-Keycloak-Install`. R1 (install repos own the
  deployable runtime) and R7 (the three-way ownership split, on the
  `github-administration-plane` precedent) were ruled once for both topics.
  The two changes are independent by construction: each adds its own
  `repo-boundary-governance` requirement rather than both replacing the
  same enumeration (design D8).
- **Not obliged**: no domain must adopt a certificate authority, and no
  existing capability is modified in a way that requires action from a
  domain that has none.

## Decisions carried into this proposal

**Two PKIs, one contract** (Brett, 2026-08-21, R8). The neutral contract is
product-agnostic because both realizations are real — a live cloud-managed
authority and a planned self-hosted one. Product names appear in this
proposal and in the design discussion; they do not appear in requirement
text.

**Renewal is a rebind obligation, not a background event** (R8's trap,
generalized). The canary's failure was not a broken consumer; it was an
incomplete renewal that reported success.

**Compose, do not duplicate** (R8 / the topic's composition section).
Revocation propagation and declared custody already exist as ratified
`openxwallet` rules, and authority material already has a home in
`credential-contracts`. A second authority vocabulary would lag the first
and win by proximity.

**Image custody stays with the tenant; deployment topology moves to the
install repo** (R2). Deciding what binary a certificate authority runs is a
tenant trust decision, and moving it out of the tenant repo would move a
trust decision away from the party that owns it.

## Open questions carried to ratification

Recorded with a recommendation each in `design.md`. The two the staged
topic flags as hardest: **what the contract requires of issuance evidence
for an authority we do not operate**, and **whether chain-custody tiers are
a closed enumeration** (and whether operator escrow is a tier at all). Both
must be settled before schemas are authored, not during — the `openxwallet`
custody enumeration is the precedent for how quietly a wrong set re-opens
the hole the rule was written to close.

## Ratification

Ratified by Brett Heap, 2026-08-21 (session instruction: "ratify both
proposals"). All design decisions adopted as written. The two hardest open
questions are ruled per their recommendations: **OQ1** — issuance evidence
remains an obligation on what the record must *establish*, with the
declared floor (per-certificate record where the authority exposes it;
per-policy attestation plus the authority's own log where it does not)
fixed before schema authoring (tasks 4.2), refusing the
weaker-form-in-requirement middle option; **OQ2** — the custody
enumeration is CLOSED with `evidences` derived, and operator escrow is
modelled as a relationship on the credential record rather than a custody
tier, settled with the `client-credential-escrow-registry` topic in the
room (tasks 4.1). The remaining OQs keep their recommendations and named
settlement points. Ratification authorizes exactly one Speckit contract
feature and creates no authority, anchor, key, or runtime. The
time-critical §2 amendment of `add-openxpki-qa-image-pipeline` remains
open and must precede THAT change's ratification.
