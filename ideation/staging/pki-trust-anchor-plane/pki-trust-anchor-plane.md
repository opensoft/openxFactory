# Staged: PKI Trust-Anchor Plane — one neutral contract, two realizations

Status: staged
Kind: architecture
Summary: Adopts a product-agnostic trust-anchor contract for the family's
certificate infrastructure, because two realizations already exist or are
planned: Microsoft Intune Cloud PKI (device and host-broker certificates — the
live canary track) and OpenXPKI (intended for the Opensoft production core).
openxFactory owns the neutral contract (trust anchors, issuance evidence,
chain custody, revocation obligations); OpsxFactory owns the
`pki-administration` workflow; a new `xFactory-OpenXPKI-Install` repo owns the
deployable topology. Ruled 2026-08-21: image custody stays with the tenant
repo while QA deployment topology moves to the install repo, and the neutral
contract composes with `openxwallet` revocation propagation and
`credential-contracts` declared custody rather than inventing a parallel
authority vocabulary.
Topics: pki, trust-anchor, openxpki, intune-cloud-pki, scep, device-identity, certificate-lifecycle, revocation-propagation, credential-contracts, openxwallet, digest-pin, install-repo-boundary
Repository context: openxFactory owns the neutral trust-anchor contract (product-agnostic: anchors, issuance evidence, chain custody tiers, renewal and revocation obligations); OpsxFactory owns the governed administration workflow (`pki-administration`, sibling of `exchange-administration` / `aks-administration-workflow` / `github-administration-workflow` / `business-central-administration`, staged as `OpsxFactory:staging:identity-pki-administration`); `opensoft/Opensoft-Tenant` keeps image custody (build, pin, test harness); a new install repo `opensoft/xFactory-OpenXPKI-Install` (aggregation path `installs/openxpki-install`) owns the deployable topology consuming the pinned digest
Staging ID: openxFactory:staging:pki-trust-anchor-plane
Source: Brett Heap's rulings 2026-08-21 in the xFactory family session, taken together with the active OpsxFactory change `add-openxpki-qa-image-pipeline` (a tenant-owned OpenXPKI image build with QA acceptance) and the live Intune Cloud PKI canary track (tenant root CA `Opensoft xFactory Root CA` plus an issuing CA, SCEP profiles, a TPM-bound broker certificate); sibling of [identity-brokering-plane](../identity-brokering-plane/identity-brokering-plane.md), whose R1/R7 rulings were made once for both topics
Target capabilities: ADDED neutral `trust-anchor` (openxFactory); new OpsxFactory-owned `pki-administration` workflow capability; MODIFIED `repo-boundary-governance` (two new install repositories in scope); amendment to the active `add-openxpki-qa-image-pipeline` Impact section

The family is about to have **two** certificate authorities in production
service, for two different populations, from two different vendors — and only
one of them was ever discussed as "our PKI". That is the argument for a neutral
contract: whatever we require of a certificate — how issuance is evidenced,
who holds the chain, what renewal owes the record, how revocation reaches the
things a certificate authorized — must be stated once, product-agnostically,
or it will be stated twice and diverge.

## Why now

1. **The Intune Cloud PKI track is already live** as the canary. A tenant root
   CA (`Opensoft xFactory Root CA`) plus an issuing CA, SCEP profiles, and a
   TPM-bound broker certificate are in service for device and host-broker
   identity. It carries a known operational trap (below) that the family
   discovered by walking into it, which is exactly the kind of thing a
   contract obligation exists to prevent recurring.
2. **OpenXPKI is intended for the Opensoft production core**, and the upstream
   Docker image is explicitly a demonstration artifact published with
   **mutable tags**. That is already being addressed: the active OpsxFactory
   change `add-openxpki-qa-image-pipeline` adds a tenant-owned build that pins
   the release, package metadata, configuration snapshot, and base image, and
   produces an immutable ACR digest with QA acceptance evidence.
3. **Two realizations, one set of obligations.** Neither of those two tracks
   is the contract. The contract is what a governed system may assume about a
   certificate it trusts — and it has to hold for a cloud-managed CA we do not
   operate *and* for a self-hosted CA we do.

## Rulings — 2026-08-21 (Brett Heap, xFactory family session)

### R8 — Two PKIs, one contract

The neutral trust-anchor contract MUST be product-agnostic, because both
realizations are real:

| Realization | Population | Status |
| --- | --- | --- |
| Microsoft Intune Cloud PKI | device / host-broker certificates | live canary track |
| OpenXPKI | Opensoft production core | planned; QA image pipeline in flight |

Reasoning: a contract written around either product would encode that
product's model of a CA — Cloud PKI's SCEP-profile-and-managed-root shape, or
OpenXPKI's realm-and-token shape — and the other realization would then be
non-conformant for reasons that have nothing to do with trust. What both owe
is the same: a named anchor, evidence that issuance happened under the policy
claimed, declared custody of chain material, and a revocation path that
reaches whatever the certificate authorized.

The Cloud PKI track also contributes the contract's first hard-won
obligation. Its **auto-renew / keyCredential-rebind trap**: a certificate that
renews automatically produces new key material, and anything that bound
authority to the *previous* key (a directory keyCredential, in the live case)
keeps pointing at a key the holder no longer uses — so renewal silently breaks
authentication that appeared to be configured correctly. The neutral contract
should therefore treat **renewal as a rebind obligation, not a background
event**: whatever bound authority to the old key must be re-bound and the
rebind evidenced, or renewal is incomplete.

### R2 — The seam with `add-openxpki-qa-image-pipeline`

The active change and the new install repo split along **custody**, not along
convenience:

- **Stays in `opensoft/Opensoft-Tenant`**: the image build, the release /
  package / configuration / base-image pins, the offline and integration test
  harness, and the QA build/pull/scan helpers producing the immutable ACR
  digest. Reasoning: **image custody is a tenant trust decision.** The tenant
  decides what binary its CA runs, and the digest-pin convention governs
  native-manifest workloads exactly here. Moving the build out of the tenant
  repo would move a trust decision away from the party who owns it.
- **Moves to `xFactory-OpenXPKI-Install`**: the QA deployment topology
  manifests (server / client / web), which **consume the pinned ACR digest**
  rather than producing it, and the per-client instantiation under
  `config/clients/<tenant>/runtime-manifest.yaml`.
- **Therefore**: that change's **Impact section must be amended before
  ratification**. Today it names `opensoft/Opensoft-Tenant` as the home of
  "new image source, test harness, QA deployment manifests, and
  runbook/evidence templates" — the deployment-manifest half of that sentence
  is now the install repo's. The amendment is small and must land before
  ratification, not after, because the Impact section is what a reviewer reads
  to decide whether the boundary is right.

### R1 — Install repos own the deployable runtime

Recorded once for both topics (see
[identity-brokering-plane](../identity-brokering-plane/identity-brokering-plane.md)
§R1). For this topic: `opensoft/xFactory-OpenXPKI-Install` at aggregation path
`installs/openxpki-install`, following the `xFactory-Hermes-Install` naming and
pattern, with per-client instantiation as
`config/clients/<tenant>/runtime-manifest.yaml` (generated, never hand-edited,
digest-pinned by consumers). Repo creation rides `repo-boundary-governance`
through an OpenSpec change, whose "Install repository scope" requirement
enumerates the admitted install repos by name and must be amended to add both
new scopes.

### R7 — Ownership split, on the github-administration precedent

- **openxFactory** owns the neutral trust-anchor contract (this topic's exit
  1). Product-agnostic requirement text.
- **OpsxFactory** owns `pki-administration` as a **sibling** capability of
  `exchange-administration`, `aks-administration-workflow`,
  `github-administration-workflow`, and `business-central-administration` —
  not a profile of one of them. A certificate authority is a managed platform
  under the promoted `opsx-service-subject-model`, administered through the
  same plan / apply / verify / recover shape as every other managed platform.
- **New service-subject kinds register in lockstep**: `customer-kinds` **and**
  the Hermes template **and** `stack.yaml` in the same change, with grant
  ceilings in `credentials/requirements.yaml`. A CA subject that exists in one
  of those three files and not the others is an ungoverned subject.
- **The install repos own the runtime.**

## Composition with promoted capabilities

The trust-anchor contract must **compose**, not duplicate. Two promoted
capabilities already carry most of the authority story:

- **`openxwallet` — revocation propagation.** Its ratified requirement
  "Revocation propagates through the chain" is the mechanism a certificate
  revocation should ride: revoking the anchor's assertion must kill the
  unexpired grants that assertion supported, transitively. The trust-anchor
  contract should therefore state the **obligation** (a revoked certificate's
  downstream authority dies with it, within a bounded window, evidenced) and
  point at openxwallet for the mechanism — rather than defining a second
  revocation vocabulary that would inevitably lag.
- **`openxwallet` — declared custody bounds what a signature evidences.** Its
  closed three-member custody set, where `evidences` is *derived* from two
  declared booleans, is the right model for chain custody too: a certificate
  whose private key is readable by its host cannot evidence what a
  hardware-isolated key evidences. The Cloud PKI canary's TPM-bound broker
  certificate is precisely the isolated case, and a software-stored service
  certificate is precisely the readable one. The contract should express chain
  custody as **tiers that are declared and derive what the certificate
  evidences**, not as a free-text field.
- **`credential-contracts` — custody of the material.** Broker database
  credentials, IdP client secrets, and **CA material** are credential records
  with declared custody and vault bindings. **Never committed** — the contract
  states this as an obligation with no exception for test or QA material,
  because the QA CA's key is still a CA key.

## What the neutral contract has to say (sketch, product-neutral)

Working list for exit 1, deliberately stated without vendor vocabulary:

1. A **trust anchor** is a named, versioned entity with a declared policy and
   a declared custody tier; systems trust anchors, never individual
   certificates.
2. **Issuance is evidenced**: an issued certificate carries a record naming
   the anchor, the policy under which it was issued, and the request's
   provenance — sufficient to answer "should this exist?" without asking the
   CA product.
3. **Custody is declared and derives what the certificate evidences**
   (composing with openxwallet's custody model).
4. **Renewal is a rebind obligation** (R8's trap generalized): renewal that
   produces new key material must re-bind every authority binding that
   referenced the old material, and the rebind must be evidenced.
5. **Revocation propagates** to the authority the certificate supported,
   within a bounded window, evidenced (composing with openxwallet).
6. **CA material is a credential record** under `credential-contracts`, never
   committed, custody declared, at the strictest tier the family operates.
7. **A conformant realization declares which obligations it cannot meet** —
   the degraded-capability note pattern the `github-administration-workflow`
   plan-tier ladder already established. A cloud-managed CA we do not operate
   will not be able to evidence everything a self-hosted one can, and saying
   so explicitly is better than a contract only one product can pass.

## Open questions (carried, not resolved)

1. **What the neutral contract requires of issuance evidence.** The strictest
   honest requirement is a per-certificate record; the weakest useful one is a
   per-policy attestation plus the CA's own log. Cloud PKI constrains what we
   can extract, so the requirement has to be satisfiable by a CA whose
   internals we do not own.
2. **Chain custody tiers — how many, and are they closed?** The openxwallet
   precedent argues for a small **closed** enumeration with derived
   `evidences` rather than an open vocabulary. Candidate members: hardware
   isolated (TPM / HSM), host-readable, and operator-escrowed. Whether
   "operator-escrowed" is a custody tier or a separate escrow relationship is
   genuinely open, and touches the `client-credential-escrow-registry` topic.
3. **How renewal and rebind traps are represented as contract obligations.**
   Is the rebind obligation a requirement on the *certificate holder*, on the
   *administration workflow*, or on both — and what evidences that a rebind
   happened, given the failure mode is silent?
4. **Whether the two realizations are one capability or two conformance
   profiles.** One capability with declared degraded obligations (leaning), or
   a neutral core plus per-product profiles the way
   `openxwallet` / `openxwallet-agent-profile` split? The rule-of-three
   trigger has not fired: two realizations may not justify a profile seam.
5. **Where the Intune Cloud PKI track's governed record lives.** It is
   OpsxFactory-administered platform work, but the device population is the
   worker fleet's — so the seam with `add-cloudpc-worker-fleet-management` and
   the worker-enrollment broker's device identity needs checking before exit
   2 is scoped. The OpsxFactory `incident-diagnostics-and-intervention` staged
   topic already asks how TPM-backed keys are issued, attested, and rotated;
   that question should be answered by this contract, not twice.

## Exit

Three planned OpenSpec changes:

1. **openxFactory** — a neutral `trust-anchor` capability carrying the
   obligations sketched above: anchors, issuance evidence, declared chain
   custody deriving what a certificate evidences, renewal-as-rebind,
   revocation propagation composing with `openxwallet`, CA material as a
   `credential-contracts` record, and the declared-degraded-obligation rule.
   Product names appear in the design discussion only.
2. **OpsxFactory** — a `pki-administration` workflow capability, sibling to
   the four existing administration capabilities, with the new service-subject
   kind registered in lockstep (`customer-kinds` + Hermes template +
   `stack.yaml`, grant ceilings in `credentials/requirements.yaml`) —
   **plus the R2 amendment** to the active `add-openxpki-qa-image-pipeline`
   Impact section, which must land **before that change is ratified**.
   Developed in the sibling staged topic
   `OpsxFactory:staging:identity-pki-administration`
   (`xFactories/OpsxFactory/ideation/staging/identity-pki-administration/`),
   shared with the identity half because both need the same service-subject
   registration work.
3. **Aggregation + install** — create `opensoft/xFactory-OpenXPKI-Install`
   under `repo-boundary-governance` (the MODIFIED "Install repository scope"
   delta, shared with the Keycloak install repo), add the
   `installs/openxpki-install` submodule pin, and move the QA deployment
   topology manifests in per R2, consuming the pinned ACR digest.

Sequencing note: exit 2's amendment is the only time-critical piece — it is
gated by the ratification of a change already in flight. Exits 1 and 3 follow
the identity topic's sequencing (neutral contract ratifies before the runtime
is built against it). Engagement-shape questions raised by per-client CA
instances are developed in `OpsxFactory:staging:engagement-shapes`.
