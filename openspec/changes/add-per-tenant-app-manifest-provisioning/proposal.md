---
code_surface: none — MEASURED, not assumed, against the clone of `main` @ `4cef77af` this packet was authored on. The whole diff is governance text in `openxFactory`: this packet's five files, one README **OpenSpec Records** row, and TWO generated rows in `tests/sequenced_after/corpus-ledger.yaml` — this change's own `active` row AND the archived `add-dispatch-credential-contract` row the generator flips `sole` → `co-modifier` because this MODIFIED block creates that overlap (`scripts/sequenced_after.py:2244`), both written by the sanctioned `scripts/validate-sequenced-after.py . --seed-ledger` and derived from the packet's existence rather than authored; `tasks.md` § 1.6 reads the same two. Evidence for the negative, each check run rather than asserted: (1) `scripts/validate-credential-contracts.py` gains NO arm — the clauses this delta adds are about a PROVISIONING MANIFEST, a record kind that exists in NO corpus this repository validates (`grep -rn "provisioning manifest" contracts/ examples/ templates/ requirements/` returns nothing, exit 0 over four roots that all EXIST — an earlier spelling of this command named a root `schemas/` that this repository does not have, so it warned on the missing path instead of proving the zero; the schemas live at `contracts/schemas/` and are inside the first root), so there is no committed record for a validator to read and an arm authored now would have no fixture that is not invented; (2) `contracts/schemas/xfactory-credential-contracts.schema.yaml` is UNTOUCHED, no `contracts/manifest.yaml` row moves, no digest inventory is cut and no `contracts/CHANGELOG.md` line is owed — nothing this packet writes is a field, a shape or a warning code; (3) NO existing requirement text is deleted — the promoted body paragraph and all three promoted scenarios of the modified requirement are restated VERBATIM, which is checked by the carriage-ledger arm of `doc-health`'s modified-block-currency family rather than claimed here; (4) the two repositories § 7.4 of `split-opendox-two-layer-product` tags, `opensoft/OpsxFactory` and `opensoft/Omnigent-Install`, are not touched by a byte, on RULING `5704187317` clauses (B) and (D). Under `release-realization` an empty code surface archives ON LANDING plus its own task list, and the gate is mechanical: `archive_change()` refuses on any literal `- [ ]` anywhere in `tasks.md` (`scripts/proposal-support.py:4609`). § 1 and § 2 are this repository's surface and must be TICKED; the installer realization (§ 3) is owed in `Omnigent-Install` under its own change and its own code surface, cannot be ticked from here, and therefore carries the house's reserved DEFERRED marker `- [~]` with its holder named — open and addressed rather than gating.
target_release: implemented — an empty code surface archives on landing plus this packet's own task list (`release-realization`), and NO contract bundle number is reserved here. This is deliberate and is the difference between this packet and its two active siblings on this capability: `add-credential-escrow-checkout` and `add-requirement-ref-resolution-integrity` each owe an additive minor on the SAME schema file, and a number written here would be a number one of them is already spending. Nothing this delta says is expressible as a schema field today, because the record it constrains — a provisioning manifest — is not a record this repository carries; when the installer change in `Omnigent-Install` gives that record a shape, the bundle question is ITS to answer against a real artifact rather than this packet's to pre-empt against none.
---

# Proposal: add-per-tenant-app-manifest-provisioning

Status: draft

TAKES THE FIRST HALF of the declared exit path of
`ideation/staging/openxdox-install-app-provisioning/` (staged 2026-08-14, gate
met 2026-08-15, exit unraised for thirty-three days) and **does not close that
topic**, on **RULING `5704187317`** — `opensoft/openxFactory` issue #656,
2026-09-16, by interactive multi-choice, option (1) SPLIT AND NARROW, clause (E).

The topic's Exit path states three things and this packet is straight about which
it meets. The contract home (Q1) is **RULED**. The managed-versus-self-hosted
flow (Q2) is **NOT ruled**, and is neither decided nor waived here. The further
condition — *"Gated on the opensoft QA dispatch migration completing"* — is **not
asserted met** by this packet. What authorizes the authoring anyway is not this
author's judgment that Q2 is dispensable, but the ruling's clause (E) DIRECTING
the authoring in the operator's own words — *"this lane authors ONLY a
`credential-contracts` MODIFIED delta in `openxFactory` carrying that shape"* —
and an authoring gate that exists to make the authoring wait on the operator is
dispositioned by the operator ordering it. The fragment therefore STAYS STAGED
(`tasks.md` § 4.2), its `ideation/staging/INDEX.md` row is where the position is
recorded, and the topic closes when ALL THREE of its stated conditions are met —
Q2 ruled, the named `Omnigent-Install` realization change in existence, AND the
opensoft QA dispatch migration complete — not when the first two are.

## Why

The dispatch/content separation is already canon. `credential-contracts`'
promoted requirement *Dispatch-only credential least privilege and serving-tier
separation* has said since `add-dispatch-credential-contract` archived on
2026-08-25 that the two credentials are DISTINCT bindings and that a
zero-write-authority serving surface must not hold — nor hold key material
capable of minting — a content-write credential. **That requirement governs a
credential that already exists. It says nothing about where the credential came
from**, and until 2026-09-04 nothing made that a gap worth closing: `opensoft`'s
QA install created both GitHub Apps BY HAND, in `opensoft`'s own organization,
hitting every manual step twice.

RULING Q3 (issue #656, 2026-09-04T15:32Z) makes it a gap. *"One instance and one
database per tenant, always … No cross-tenant data ever shares a store"* means
the pair is provisioned ONCE PER TENANT — N times, in N organizations this estate
does not own and cannot administer. Provisioning is exactly where a separation
invariant is cheapest to lose, and the two cheapest ways to lose it are the two
an unspecified install will reach for first: have an OPERATOR identity create the
Apps inside the tenant's organization (which puts an operator in the tenant's
credential path and gives that operator an identity capable of minting a
content-write token), or create ONE App and widen it (which collapses the
separation into a permission list). Both pass every check the promoted
requirement makes, because the promoted requirement is not looking there.

The measured facts the staged topic established are unchanged and are the reason
the shape is expressible at all: **the provider has no app-creates-app API**, so
the mechanism is the App Manifest flow — a committed manifest with permissions,
events and callback pre-filled, redirecting the tenant to the provider where
their own seat names and confirms it, the provider creating the identity IN THE
TENANT'S ORGANIZATION and returning its secrets once, within a bounded window.
Tenant ownership is therefore STRUCTURAL rather than promised. And because the
provider's App names are a GLOBAL namespace, the convention is a per-tenant name
(`openXdox — <tenant>`, `openxFactory — <tenant>`) rather than one name every
tenant contends for.

## What Changes

**ONE `## MODIFIED` block, on ONE requirement, over CANON.** *Dispatch-only
credential least privilege and serving-tier separation* is restated in full — its
promoted body paragraph and all three promoted scenarios verbatim — and grown by
five clauses and eight scenarios — the first two being the
provisioning rule and the scoping rider that keeps it case-neutral:

1. **Where the pair is provisioned through a manifest, creation is in the
   tenant's organization and the identity is never an operator-owned one
   installed into it** — and never one provisioned identity creating the other,
   which the promoted sentence already forbids the serving tier to be capable of.
   The clause binds WHERE the identity lives, not who drives the flow and not who
   holds its material.
2. **One pair per tenant, never shared**, with a per-tenant, pattern-discoverable
   naming convention where the provider's namespace is global.
3. **The dispatch identity's one named target is a repository that holds no
   governed content**, and that repository is part of the provisioning.
4. **Capture is time-bound, lands in the DECLARED custody by reference, and
   leaves whoever drives the flow not an UNDECLARED custodian** — the custody's
   operator being the per-install execution binding this capability already
   fixes rather than a party this contract names — and no manifest, record or
   template carries a secret value, private key or installation token.

**No new capability.** The topic's OQ-1 offered a new `install-app-provisioning`
capability beside the MODIFIED delta; RULING `5704187317` (E) took the delta.
Authoring a capability would have put the provisioning shape one indirection away
from the invariant it protects, and the invariant is what makes the shape
non-obvious.

## What is deliberately NOT changed

- **The other eleven requirements of `credential-contracts`.** A provisioned pair
  is two distinct bindings on two distinct secrets and reaches none of the
  six-condition shared-`secret_ref` lift; `A credential binding declares the
  consuming system that holds it and the identity it fetches with` is untouched
  and already covers what the bindings then declare.
- **Canon's two legitimate operating models, and the ratified operator-hosted
  runbook.** *The credential vault operator is an execution binding, never
  contract content* keeps BOTH cases legitimate
  (`openspec/specs/credential-contracts/spec.md:141`) and
  `docs/openxdox-dispatch-credential-binding.md:31-37` records a LIVE Case A in
  which the operator creates the dispatch App and holds its key in the operator's
  vault. The added clauses are scoped to provisioning THROUGH A MANIFEST, name no
  custody party, and do not retroactively refuse a pair already in service — two
  of the eight added scenarios assert exactly that. Whether Case A migrates to
  the manifest shape is the installer's act and the topic's unruled Q2.
- **Any schema, validator arm, warning code or contract bundle.** See the
  `code_surface:` declaration: the record these clauses constrain does not exist
  in a corpus this repository validates.
- **`opensoft/OpsxFactory` and `opensoft/Omnigent-Install`**, the two repositories
  § 7.4 of `split-opendox-two-layer-product` tags. RULING `5704187317` (B) reads
  that box's `openxdox` DNS sentence as discharged by NAMING — per the packet's
  own `design.md` § Non-goals — and leaves the ceremony-reach widening inside lane
  opsXfactory-4's `add-governed-dns-administration` on Brett's OQ-E word
  (`opensoft/OpsxFactory` issue #207 comment `5649809425`); clause (D) leaves the
  `dox` workload set's per-tenant declaration to § 3.5, its requirement standing
  under lane opsXfactory-3's claim `5638511222`.
- **The installer itself.** `Omnigent-Install` owns the flow that drives the
  manifest and wires the two bindings so the minter REACHES the material by
  reference from the custody the install declares — not a hand-off of the
  material to the minter, which is the wording the corrected clause removed and
  which would make the flow's driver a custodian — under its own change and its
  own code surface; § 3 names it as owed and authors none of it.
  That repository's own README forbids the alternative in terms — it *"should not
  contain … canonical shared contracts that belong in `openxFactory/contracts`"* —
  which is the same boundary CLAUDE.md working rule 1 states.

## Open questions

- **OQ-1 — the managed flow (the staged topic's Q2), CARRIED AND NOT BLOCKING.**
  In the `opsxfactory_executed` case, does the operator drive the manifest flow on
  the tenant's behalf, or does the tenant always click through their own? The
  delta is written CASE-NEUTRAL and does not turn on the answer: what it binds is
  WHERE the identity is created and WHOSE it is, and both cases put it in the
  tenant's organization under the tenant's ownership. The answer changes the
  installer's sequence, which is `Omnigent-Install`'s change to write. Recommended
  when it is put: the tenant's own seat always confirms, because the clause's
  refusal is about the created identity being an operator's OWN, and a
  confirmation the operator performs is the shortest path to one that is.
- **OQ-2 — the apply-workflow repository's provenance (the topic's Q3, second
  half).** Created fresh per install, or a template the tenant forks; and does
  `opensoft`'s own `intent-apply.yml` migrate to the small-repo pattern for parity
  with tenant installs? The requirement binds the PROPERTY (the dispatch
  identity's one named target holds no governed content) and not the provenance,
  so either answer satisfies it. Recommended: fresh per install, which is what
  makes the property checkable at provisioning time rather than inherited.

## Impact

- Affected capability: `credential-contracts` — ONE MODIFIED requirement.
- Affected code: NONE in this repository (see `code_surface:`).
- Realization owed elsewhere and named, not authored: the installer change in
  `opensoft/Omnigent-Install`; the manifest files and install-doc pointer in the
  first consuming domain repository, which the staged topic names as
  `codexFactory`.
- § 7.4 of `split-opendox-two-layer-product` **stays OPEN and is not this
  packet's to tick.** Its tick is owned by this lane's bookkeeper in amendment
  #5 (`tasks.md` § 5.3), and the conditions that amendment weighs are RULING
  `5704187317`, this delta landing, and § 3.5's per-tenant evidence — none of
  which this packet asserts as met, and the last of which does not exist yet.
  **This packet edits that packet's `tasks.md` by not one byte.**
