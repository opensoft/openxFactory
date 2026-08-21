# Trust Anchor Contract Family

Status: ratified
Ratified by: add-trust-anchor (approved Brett Heap 2026-08-21, with OQ1 and OQ2
ruled as recommended; registered in `contracts/manifest.yaml` +
`contracts/CHANGELOG.md` at **contract-v1.36** (2026-08-21), per
[Contract Versioning Policy](../../docs/contract-versioning-policy.md))
Kind: reference
Repository context: openxFactory owns this neutral contract; the OpsxFactory
`pki-administration` workflow and the `xFactory-OpenXPKI-Install` deployment
topology are named successors that consume its vocabulary rather than restate it

The neutral contract for **what a governed system may assume about a certificate
it trusts** — product-agnostic, and satisfiable by a certificate authority the
family does not operate as well as by one it does.

## Why this exists

The family is running **two certificate authorities**, for two populations, from
two vendors — one live and one planned — and only one of them was ever discussed
as "our PKI". Whatever we require of a certificate was therefore about to be
written twice.

Written around either product, the contract would encode that product's model of
an authority — a profile-and-managed-root shape, or a realm-and-token shape — and
the other realization would be non-conformant for reasons that have nothing to do
with trust. So every requirement here is an obligation on a RECORD or on a
WORKFLOW, and never on a mechanism. That discipline is what makes the
honest-shortfall rule expressible at all.

The live realization also contributed the first obligation, the hard way: an
**auto-renew / rebind trap**. A certificate that renews automatically produces new
key material, and anything that bound authority to the *previous* key keeps
pointing at a key the holder no longer uses. Authentication that was configured
correctly stops working, silently, and the thing that broke is not the thing that
changed.

## The five decisions this family carries

**Systems trust anchors; certificates are trusted derivatively.** An anchor is the
governed record. This is the only framing in which revocation and rotation have
somewhere to attach: trusting certificates individually produces a trust set
nobody can enumerate and an anchor withdrawal that withdraws nothing.
`trust_evaluation.basis` is a constant, so a certificate accepted on its own
strength has no shape here.

**Custody is declared from a closed set and DERIVES what a certificate
evidences.** A key readable by the host that uses it evidences that the HOST
acted; only custody isolating the key from that host AND requiring an
authorization it cannot supply evidences that the NAMED HOLDER acted. `evidences`
is derived from two declared booleans and recomputed by the validator — a
readable key cannot claim an isolated key's authority, and the collapse is
structurally impossible rather than discouraged. This composes with
[`openxwallet`](../openxwallet/README.md)'s ratified custody rule instead of
restating a second custody model: each member names its openxWallet counterpart
and the mapping is resolved against that registry AT RUN TIME.

**Renewal is a rebind obligation, and the failure belongs to the ISSUING
WORKFLOW.** A renewal producing new key material is incomplete until every
dependent binding is re-bound and each rebind evidenced.
`failure.attribution` is a constant: there is no field in which to record the
outage as the dependent's fault. The dependent was configured correctly when it
was configured; the renewal is what changed beneath it, and attribution is where
the recurrence gets prevented. An unattended renewal is not exempt — no rule in
the validator keys on `renewal_mode`, because a rule that did would put the
exemption into the mechanism whatever the requirement said.

**Revocation propagates to the authority the certificate supported**, within a
declared bounded window, evidenced, riding `openxwallet`'s
revocation-through-derivation rule rather than a second revocation vocabulary.
Standing is checked at USE; a window that closes unevidenced is escalated as an
OPEN EXPOSURE, and there is no "accepted risk" state to reach for.

**A realization declares the obligations it cannot meet.** Obligation by
obligation: satisfied, partial, or cannot, with a reason in each case. An
UNDECLARED shortfall is non-conformance even where the identical shortfall,
declared, would be conformant. The guards that keep this from becoming a loophole
are enforced across records rather than stated in prose: a declared gap is not
permission to assert the missing evidence (a consumer refuses the certificate for
that use), and declaring a gap afterwards does not validate the claims made while
the realization was silent (per-entry dates, checked against the records that
cite them, and refused where a record carries no date to compare).

A declaration is also not an exemption. **A realization that OPERATES the
authority cannot declare an authority-material shortfall** — nothing stands
between it and a credential record with a vault binding, so the shortfall shape
is for an authority the family does not run. Likewise a family-operated authority
may not record its issuances at the declared floor, and no record may assert a
stronger establishment level than the declaration says the realization achieves.
Those three facts were required by the schemas and read by nothing until the
adversarial review of 2026-08-21; a required-but-unread field is a ruling that
exists only in prose.

## The kinds

| File | Kind | What it carries |
| --- | --- | --- |
| `trust-anchor.schema.yaml` | `xfactory_trust_anchor` | Anchor identity, chain position, validity window, the issuance authorities it ADMITS, declared custody of its key. References key material; never carries it. |
| `certificate-record.schema.yaml` | `xfactory_certificate_record` | The anchor it is trusted through, subject, validity, declared chain custody, DERIVED `evidences` and assurance ceiling, issuance evidence (or the honest absence), the dependent-binding enumeration, record defects, and the evaluation with its standing check. |
| `issuance-evidence.schema.yaml` | `xfactory_certificate_issuance_evidence` | Which anchor issued, under which admitted authority, on whose request, when — and the establishment level actually achieved. |
| `dependent-binding.schema.yaml` | `xfactory_certificate_dependent_binding` | One authority binding referencing a certificate's key material, in any system inside the family or outside it: what holds it, what it binds, which key GENERATION, the assurance it requires, its admission, and its rebind status. |
| `renewal-record.schema.yaml` | `xfactory_certificate_renewal_record` | Whether key material changed, the enumerated dependents, per-dependent rebind evidence, and a completion state that cannot read "complete" with an unevidenced dependent. |
| `revocation-propagation.schema.yaml` | `xfactory_certificate_revocation_propagation` | What was revoked, the declared bounded window, the downstream authority reached, propagation evidence, and the escalated open-exposure state for a window that closed unevidenced. |
| `conformance-declaration.schema.yaml` | `xfactory_trust_anchor_conformance_declaration` | Per obligation: satisfied / partial / cannot, with a reason and a date. Closed over all eight obligations. |
| `chain-custody-registry.schema.yaml` + `trust-anchor-chain-custody.registry.yaml` | `xfactory_trust_anchor_chain_custody_registry` | THE closed chain-custody set and the ordered assurance ladder it caps, with `evidences` derived, the deliberate non-members recorded, and the openxWallet mapping each member must agree with. |

## The closed chain-custody set

`trust-anchor-chain-custody.registry.yaml`, three members, `evidences` derived
from two booleans:

| id | key readable by the using host | per-use authorization outside that host | evidences | assurance ceiling |
| --- | --- | --- | --- | --- |
| `host_held` | yes | no | `using_host` | `host_attributed_act` |
| `host_isolated_invocable` | no | no | `using_host` | `host_attributed_act` |
| `host_isolated_per_use_authorized` | no | yes | `named_holder` | `holder_attributed_act` |

`host_held` is also the FLOOR an undeclared certificate resolves to, and the
validator checks that the declared floor really is a weakest member — resolved in
the registry document's OWN members, so a registry that renames its members is
still held to the rule instead of reporting its own floor as unknown.

**A readable anchor key caps everything beneath it.** Where an anchor's declared
custody leaves its private key readable by the using host, no subordinate anchor
and no certificate chaining to it may carry a ceiling above that anchor's:
anything with read access to that host can issue under the chain, anywhere,
indefinitely, so nothing beneath it can attribute an act to a named holder. The
cap is keyed on READABILITY rather than on rank alone — an isolated anchor key
confines minting to a compromised host while it is compromised, which is the
bound a realization accepts when it declares the R7 shortfall for an authority
the family does not operate, and capping that case too would make a declared
shortfall a bar to conformance.

**"Hardware" is not the discriminator.** A hardware-resident key a host can use
without limit lands in `host_isolated_invocable` and evidences the HOST. Treating
hardware as the discriminator is precisely how a key the host can use at will ends
up carrying a holder's authority.

**Operator escrow is not a custody tier** (ratified OQ2 ruling). Escrow answers
"who else can obtain this key", which is orthogonal to "can the using host read
it"; it is a relationship on the `credential-contracts` record every custody block
already references. The structural guard is discriminator uniqueness: because
`evidences` derives from exactly two booleans, a member declaring the same pair as
another differs only in something this axis cannot express, and the registry is
refused rather than letting a second axis ride along invisibly.

## The issuance-evidence floor

Two levels, and nothing weaker is representable (ratified OQ1 ruling):

- `per_certificate_record` — required where the authority exposes per-certificate
  request provenance. Requires the requester, the request identity and the time.
- `per_policy_attestation_with_authority_log` — the declared floor where it does
  not. Requires BOTH halves, and forbids the per-certificate fields by shape: an
  asserted-but-unestablished record is worse than a declared gap.

The conformance declaration carries which form a realization achieves, so a
consumer reads it where it looks for everything else — and a record may not
assert a stronger form than the declaration claims.

## Key material: the scan is armor-independent

Every object in every schema closes `additionalProperties`, so no key-shaped
PROPERTY can be added at any depth, and the only key-adjacent value the shapes
admit is a pattern-restricted digest. A conformant shape can still carry a key
inside a string field that legitimately exists, so the validator walks names AND
values — and it tests the decoded BYTES for private-key STRUCTURE rather than for
the `-----BEGIN … PRIVATE KEY-----` label.

The label is what an evader drops. An earlier form of this rule matched the armor
after decoding, and an adversarial review walked five keys past it: unarmored
PKCS#8 DER as base64, the same DER as hex, a double-base64 wrapper, an armor
label split across two fields, and a DER blob labelled "QA only". So the scan
reverses two decode layers and both alphabets, joins the document's strings
before matching the armor, and recognises the PKCS#8, PKCS#1 and SEC1 prologues
with their algorithm OIDs. "QA only" remains a reason the contract does not
accept, and there is no field in which to record it as one.

## Validating

```bash
python3 scripts/validate-trust-anchor.py                 # family self-test
python3 scripts/validate-trust-anchor.py <repo-path>     # repo mode
python3 scripts/validate-trust-anchor.py --strict         # warnings are errors
```

The canonical validator runs schema conformance plus the rules the shapes cannot
express, and self-tests over the packaged corpus — 34 positive examples plus 65
intended-invalid fixtures under `examples/negative/`, each declaring the finding
code it exists to provoke and the requirement it confirms. Coverage is closed in
both directions: a requirement with no probe is a finding, and so is a fixture
claiming a requirement this capability does not have.

The suite that gates it in CI is `tests/trust-anchor/`:

```bash
python3 -m pytest tests/trust-anchor/
```

Three files — the validator's own exit code and reported corpus counts, every
negative fixture adjudicated independently so a regression names the probe that
stopped proving its rule, and the declaration-perimeter rules whose cases need
two records that disagree and therefore cannot be a single packaged fixture.

Reproduce the red-proof (every finding code load-bearing) with:

```bash
python3 specs/009-trust-anchor-contracts/evidence/red-proof.py
```

## Validating: what is an ERROR and what is a WARNING

Two rules report rather than refuse, and the line between them is the ratified
wording of the declared-obligation requirement — a consumer "refuses a claim the
declaration cannot support":

| Case | Outcome | Why |
| --- | --- | --- |
| A binding requires an obligation the realization declares it **cannot** satisfy, and is recorded admitted | **ERROR** (`declared-gap-claimed`) | The declaration cannot support the claim at all. The conformant record is a refusal naming the gap entry. |
| A binding requires an obligation the realization declares **partial**, and is recorded admitted | **WARNING** (`declared-partial-required`) | Partial is not cannot: R8 permits the admission. The report is the point-of-use cost made visible, so the shortfall is something a consumer weighed rather than discovered. |
| A declaration records more than one obligation as **cannot** | **WARNING** (`declaration-cannot-breadth`) | Conformance by declaration is the ratified arrangement, so breadth is not refused — but a realization claiming very little should say so where a consumer reads it. |

Warnings are a nonzero exit under `--strict`, which is how a point-of-use cost is
actually paid. And the cost has somewhere to land because `required_obligations`
is REQUIRED and non-empty on every dependent binding: without that, a realization
could declare every obligation `cannot`, name no obligations at any point of use,
and meet no refusal anywhere — the loophole this design names, and one an
adversarial review walked straight through.

## What this family deliberately does not do

No certificate authority, no anchor, no key, no issuance or revocation service, no
deployment topology, no runtime. No product profiles — a third realization that
differs STRUCTURALLY rather than in what it can evidence would be a new capability
over this core, not a modification of it. No escrow contract (that is the
`client-credential-escrow-registry` topic's). No administration workflow — that is
the OpsxFactory successor's.

And it cannot check what no validator can: that a DECLARED custody model, or a
DECLARED conformance state, is the real one. Declaration is what keeps this
contract honest, and it works only if realizations declare truthfully. A false
declaration is a governance finding, not a misconfiguration.
