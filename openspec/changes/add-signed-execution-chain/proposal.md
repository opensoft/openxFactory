---
code_surface: openxFactory — a NEW `contracts/signed-execution-chain/` contract family carrying ONE record kind, `xfactory_execution_chain_link`, together with packaged positive and negative examples for every refusal this packet names, and the canonical `scripts/validate-signed-execution-chain.py` that reads them; registration in `contracts/manifest.yaml` and `contracts/CHANGELOG.md` at the next additive bundle cut; and the workflow wiring that makes that validator a REQUIRED check, without which the family confers and refuses nothing (`review-authority-intake`'s ratified reader rule, restated here as R10 rather than inherited by implication). **NO BYTE OF THE WALLET CONTRACT FAMILY MOVES.** `xfactory_wallet_grant_exercise` is `additionalProperties: false` and is owned by `opensoft/openXwallet`, consumed here at `wallet-v1.3` through `contracts/openxwallet-pin.yaml`; the chain link REFERENCES an exercise by `exercise_id` and never extends its schema — see design.md D4, which records this as the packet's single hardest constraint. NO certificate record, NO anchor record and NO attestation record is added: those are tranche two and tranche three. The domain realizations (codexFactory's lane, MedxFactory's HealthLinc, LedgerxFactory's LedgerLinc) are successor changes in their own repositories, named in the impact map and not this packet's surface.
target_release: the next additive contract bundle — `contract-v2.2` as the train stands at authoring, since `contracts/manifest.yaml:3` declares `contract-v2.1` and that bundle was CUT AND TAGGED on 2026-08-28 — **allocated at realization by merge order** per `docs/contract-versioning-policy.md`, never spent in a proposal. The class is ADDITIVE (minor) and nothing narrows: a repository holding no chain link stays conformant, `contract_schema_version` is unchanged, no existing field is added, deprecated or removed, and every consumer pinned at `contract-v2.1` stays conformant until it deliberately upgrades. Several changes may ride one additive cut, so a packet that reaches the cut first does not renumber this one — the `contract-v1.28` renumber sweep is the standing precedent for why the number is not written down early.
Status: draft
Proposed: 2026-08-29
Origin: Staged topic `signed-execution-chain` (`openxFactory:staging:signed-execution-chain`), registered 2026-08-27 from Brett Heap's expansion ruling and landed as pull request #452 on 2026-08-28 with its chain-selection study vendored beside it. This packet raises TRANCHE ONE of that topic's own three-tranche exit path and moves no staged file: both documents stay staged for tranches two and three, and `ideation/staging/INDEX.md` records the raise. The origin declaration covers the MATERIAL, not this packet's text.
---

# Proposal: add-signed-execution-chain

## Why

### The one-sentence claim

**A ratification that cannot prove what descended from it is a signature with
no reach.** `add-wallet-carried-review-authority` makes review authority a
wallet-carried grant and anchors its root issuer to a named operator. What no
ratified text does yet is carry that signature FORWARD: the ratification is
signed, and then the work happens in a lane that cannot prove it descended from
that ratification. This packet closes the first gap — the act that ratifies and
the act that enrolls that ratification in a chain become ONE signed handshake, so
there is no ratified object without its chain and no chain without its
ratification.

### The inversion that makes it worth ratifying

This is not an audit trail. An audit trail is written after the fact and can be
forged after the fact. A chain that a consumer VALIDATES is a permission: you
cannot proceed on what you cannot prove. The record and the control are the same
object, which is why the staged topic states the strong form — the executing
layer refuses to build an unverified chain — rather than the weak one, where
something later checks a log a careless or compromised lane wrote.

Tranche one does not yet own the merge gate that makes the strong form bite
(that is link 8, and it arrives with the later tranches). What tranche one owns
is the chain's ROOT and its CONSTITUTION: what a first link is, what binds a
successor link to it, what a gap means, and where the record lives. Get those
wrong and every later tranche inherits the error; get them right and the later
tranches extend a shape rather than renegotiate one.

### The out-of-pipeline proof — why the handshake cannot ride the clearance lane

This is the part a reader coming to the packet cold most needs, because the
obvious question is "why is this a signed handshake instead of a gate?"

On 2026-08-28 codexFactory's `gate_rules_council` returned a **UNANIMOUS REFUSE,
5/5** on a proposed substantive candidate class over `openspec/changes/**`
(record: codexFactory
`hermes/domain/review-councils/records/2026-08-28-gate-rules-openxfactory-substantive-classes.md`).
The finding, at **§2** of that record, is that such a class **can never
commission a council**:

- `openspec/changes/**` is a member of the canonical `GATE_INTEGRITY_FLOOR`, and
  the PR-time floor is evaluated BEFORE any clearable classification. Every path
  the class admits is a path its own mandatory floor refuses, so every candidate
  returns `parked_never_clearable` and the convening lane bails on exactly that
  outcome.
- It was reached **independently, by execution, by three seats** before any could
  see another's return, and measured on openxFactory's real tree: 984 tracked
  paths admitted, 984 floored by the canonical minimum alone, **0 remaining**.
- It is **code-level, not document-level**. The record reproduces the proof:
  `gate_integrity` DECLARED, `gate_integrity` ABSENT, and NO RULE DOCUMENT AT ALL
  all park identically with byte-identical reasons, while a control allowlist
  over a non-floor path commissions normally. In the company-policy-lead seat's
  words, quoted in the record: *"No edit to this rule document — none — can make
  this class ever reach classification."*

Brett Heap ruled it at **§8.2** of the same record, the sole disposition of
record: **option (a), the class is refused as defined**, with *"no class over
`openspec/changes/**` under this or any adjacent id"*, and the continuation named
as *"§7.4's council-reviewed-but-human-approved path, which needs no class and no
flip"* (§7.4 of the 2026-08-26 classification-intent record). The refusal is of
the vehicle, not the destination: the same record carries the lead-quality seat's
affirmative, unhedged best-practice rationale that council review of proposal
pull requests **is** sound practice here, with the need measured on openxFactory
issues #351 and #357.

**So the only lawful home for a governance act over this surface is one that does
not enter the clearance pipeline at all** — a human authority whose standing to
act comes from somewhere other than a verdict, and whose act is made checkable by
a SIGNATURE rather than by a clearance. Note the two halves are separate: where
the standing comes from is what puts the act outside the pipeline, and R1's
wallet-carried exercise is what makes it checkable. An authority with standing
but no wallet has the first half and not the second, which is why R1 gives that
case no chain at all rather than a signature-free one. That is exactly what the ratify-and-enroll handshake is, and this packet
states it normatively (R9) rather than leaving it as a rationale a later reader
would have to reconstruct.

### The forcing fact, stated as an absence rather than a preference

There is today no artifact anywhere in this corpus that binds a ratification to
what descends from it. `xfactory_wallet_grant_exercise` records one exercise, in
isolation and with `additionalProperties: false`. The intake register records who
may act. Neither records that THIS act began THIS line of work, and neither can
be made to: the exercise schema is owned by another repository and is closed, and
the register is a standing-authority list, not a per-act ledger. A chain link is
the missing record, and it is the only new record kind this packet adds.

## What changes

**ONE new capability, `signed-execution-chain`, with ten ADDED requirements and
no MODIFIED requirement on any existing capability.** Why no MODIFIED block is a
decision, not an omission: see design.md D7. In one line — the neutral family
states what a chain IS and what refuses; binding openxFactory's own OpenSpec
lifecycle to it is a DOMAIN application performed at realization, when the reader
exists in a required check, and asserting it now would describe a control that
does not exist, which is the defect this family's neighbouring ratified text was
written to refuse.

The requirements, one line each:

| Id | Requirement | What it settles |
| --- | --- | --- |
| R1 | A governed ratification enters a signed execution chain only as a key-attributed grant exercise whose proof of possession was verified | Link 1's instrument is the wallet, EXERCISED — not presented; and a ratifier holding standing authority with no wallet begins no chain, recorded as a declared gap |
| R2 | Ratification and chain enrollment are one atomic act, and neither half stands alone | Link 2 — the divergence the handshake exists to make impossible |
| R3 | The chain identity is the digest of the signed ratification, fixed once at chain enrollment | What a chain IS identified by, and that re-ratification is a new chain |
| R4 | Every link signs the chain identity and its predecessor's digest | Hash-linked, so a bag of individually valid signatures is not a chain — and at most ONE link succeeds any link, so a fork of two verifying histories is refused rather than resolved |
| R5 | The chain travels with the work as a carried contract, verifiable at the point of use | Link 3 — checkable without resolving a mutable table |
| R6 | A gap in the links a chain is required to carry is refused as a fraud signal, never downgraded | Link 9's semantics; the required set comes from the consumer's declared expectation, never from what it was handed |
| R7 | The evidence plane is an append-only signed log in the governed store, and it is the record | Where a link is written; anchoring is explicitly not in scope |
| R8 | The chain names no identity, certificate or custody term of its own | The collision the staged topic names as its live risk |
| R9 | The ratify-and-enroll handshake is performed outside the clearance pipeline | The never-convenable finding, made normative |
| R10 | The chain confers and refuses nothing until a named reader runs as a required check | No described control is presented as an existing one |

## Scope — tranche one only

**IN SCOPE.** Links 1, 2 and 3 of the staged topic's ten-link model, plus the two
rules the atomicity and chain-identity claims strictly need in order to be
statable at all: the hash-linking rule (R4), without which "enrolled in a chain"
means only "signed twice", and the evidence plane (R7), without which enrollment
has nowhere to write. R6's refusal semantics and R9's out-of-pipeline placement
are in scope because both are properties of the links tranche one creates. R8 and
R10 are the two discipline requirements the neighbouring ratified text makes
mandatory for any packet in this family.

**EXPLICITLY NOT IN SCOPE — tranche two.** Links 4, 5, 6 and 10: the
harness-controller setup attestation, the runner attestations, the signed PR-open
decision, and the governed post-merge test that CLOSES a chain. Nothing about
attestation identities, per-task credentials, controller certificates, the
signing mechanism, or claim binding appears in any requirement below. Tranche two
needs the omnigent layer to enforce the precondition and
`implement-openxpki-install-repo` to issue the controller certificate, and it is
gated on Q7 — where an attestation signature physically happens — which is
reserved for Brett's clarify sitting and is NOT decided here.

**EXPLICITLY NOT IN SCOPE — tranche three.** The on-chain layer entirely: public
anchoring, salted keyed commitments, consent-log checkpoints, the permissioned
consent plane, the multi-anchor receipt format, and every question about what may
and may not leave the governed store. Tranche three is gated on Q3 (chain
selection, where a vendored study has completed and awaits a ruling) and Q6 (the
PHI reading), and neither is decided here.

**ALSO NOT IN SCOPE, and worth naming because a reader will look for it.** Link
7 (council review of the signed brief) and link 8 (the chain-validating merge
gate). The staged topic argues the gate should exist from tranche one validating
a short chain, and this packet honours that intent in the only way it lawfully
can: R6 states what ANY validating consumer must do with the links a chain is
required to carry, so the refusal path is specified from the start. It does NOT create a merge gate,
because a merge gate over this repository's proposal surface is precisely the
never-convenable object §2 of the council record refuses, and because R10 forbids
describing an enforcement point that does not exist.

## Composition map — which ratified text each link stands on

Stated as a map rather than as prose, because the staged topic names "inventing a
second identity or certificate vocabulary" as this family's live collision risk,
and a map is auditable where prose is not.

| Tranche-one element | Governing ratified text | What this packet takes from it |
| --- | --- | --- |
| Link 1's instrument | `add-wallet-carried-review-authority`, `review-authority-intake`: *"Review authority is held as an openxwallet grant and by nothing else"* | Authority is a grant; the closed `authority_tier` ladder; no parallel authority word |
| Link 1's proof | openXwallet `openxwallet`: *"Use requires proof of possession, not presentation"* (pinned at `wallet-v1.3`, `contracts/openxwallet-pin.yaml`) | A presented grant confers nothing; the refusal names the MISSING PROOF, not a missing grant |
| Link 1's attribution | openXwallet `openxwallet`: *"Every exercise is key-attributed"* | The presenting wallet key is the actor; a shared credential is transport; an unattributable act is `unattributed` and is not assigned to a holder |
| Link 1's currency | openXwallet `openxwallet`: *"Revocation propagates through the chain"* + `review-authority-intake`: *"Revocation is re-checked at verdict consumption against a declared staleness bound"* | Revocation is checked at exercise; issuance-time validity is not current validity |
| What a signature EVIDENCES | openXwallet `openxwallet`: *"Custody is declared and bounds what a signature evidences"*, composed by `add-trust-anchor`: *"Declared chain custody bounds what a certificate evidences"* | Custody caps the claim; this packet restates no custody model of its own |
| The unwalleted root ratifier | `review-authority-intake`: *"Every review-authority grant names its issuer, and a root grant's issuer is anchored outside the register"* — the root issuer is the responsible operator, whose standing *"requires no wallet and no grant of its own"* | R1: that ratifier begins NO chain, and the case is a DECLARED GAP naming the missing instrument; no signature-free chain mode is defined, so the gap stays visible instead of being filled with a weaker object |
| Who a signer IS | `add-identity-brokering`: *"A governed record binds its actor to a stable opaque subject"* | The actor reference on a link; this packet owns WHAT is attested, never WHO the signer is |
| Non-human signers | `add-identity-brokering`: *"Workloads are not personas"* | A workload's authority comes from a grant, never from a persona — which is why tranche one's only signer is human |
| The reader rule | `review-authority-intake`: *"A grant with no reader in a required check confers nothing"* and *"The register and the reader are ratified together"* | R10 verbatim in effect: no described control is stated as an existing one |
| Refusal doctrine | `workflow-gate-contract` and this family's standing rule that an unevaluable gate refuses | R6: a chain that cannot be evaluated refuses; it never degrades to a warning |
| Declaring what cannot be met | `add-trust-anchor`: *"A realization declares the obligations it cannot meet"* | Every gap in this packet is declared by name rather than softened |
| Release discipline | `release-realization`: realization axis declaration and archive gate | `code_surface` and `target_release` above; the packet archives on merged + green realization evidence |

**One dependency this packet declares rather than respells.** The wallet's
exercise record cannot carry a chain reference: `xfactory_wallet_grant_exercise`
is `additionalProperties: false` and lives in `opensoft/openXwallet`, which
openxFactory consumes at a pinned commit and digest and does not author. The
chain link therefore REFERENCES an exercise by its `exercise_id` and adds no
field to the wallet schema. If a future tranche needs the wallet record itself to
name its chain, that is a change in the publisher's repository under the
`neutral-product-pin` seam, and this packet says so instead of inventing a second
exercise record.

## Q6 and Q7 are open, and tranche one does not touch them

The staged topic reserves seven open questions. Two of them are held for Brett's
clarify sitting and are **not pre-decided anywhere in this packet**:

- **Q6 — does "patients put PHI portions on chain" mean commitments?** GATES
  TRANCHE THREE. The topic reads the 2026-08-27 ruling as commitments and raises
  the narrowing rather than assuming it, because a topic must not quietly narrow a
  ruling.
- **Q7 — where does an attestation signature physically happen?** GATES TRANCHE
  TWO's contract text. Remote signing served by the controller, a co-process
  behind an attested boundary, and a hardware-backed signer are all consistent
  with the ratified `access_secrets: false` constraint and differ in what an
  attacker owning a runner for one task can obtain.

Tranche one's independence from both is not asserted; it is checked, and the
check is recorded in design.md §"Proving tranche one is Q6/Q7-independent". In
short: tranche one anchors nothing and carries no payload, so Q6's answer changes
no requirement text; and tranche one contains no attestation link at all — its
only signer is a human wallet holder under tier 1 — so Q7's answer changes no
requirement text either.

Q1–Q5 are carried exactly as the topic leaves them and are restated in
design.md §"The topic's other open questions, as the topic leaves them": Q1
(open, and the reason tranche one specifies WHAT a ratification must evidence
rather than the presentation ceremony), Q2 (open, tranche three), Q3 (open —
research complete, awaiting a ruling), Q4 (open, and this packet is the first
evidence on it), Q5 (open — direction confirmed, trigger condition unstated).

## Impact

- **`openspec/specs/signed-execution-chain/`** — a new capability directory on
  promotion. Ten requirements.
- **`contracts/signed-execution-chain/`** — a new contract family at
  realization: one record kind, its examples, its validator, its manifest and
  changelog registration, at the next additive bundle cut.
- **No existing capability is modified.** No promoted requirement text moves.
- **No staged file moves, but the support manifest lands anyway.**
  `ideation/staging/signed-execution-chain/` keeps both documents for tranches two
  and three; the primary fragment gains the `Staging ID:` header the origin
  contract requires, and nothing else in it is edited. The vendored
  `chain-selection-study.md` is not touched at all — it is annotate-only research
  input, and nothing in it is ratified by being vendored. The packet nonetheless
  owns `supporting-docs/manifest.yaml` recording ZERO selected files, both
  remaining staged paths, the source revision and the repeated origin. Written on
  Codex's P1 over this packet, in a NARROWED form: the proposal-gate requirement
  binds "the SELECTED source documents" and nothing here is selected — three
  sibling ACTIVE staged-origin changes (`add-ideation-intent-plane`,
  `add-model-capability-vocabulary`, `add-notebook-projection-identity`) carry no
  supporting folder on the same reading — but `release-realization`'s "Origin
  retention at archive" scenario expects a staged origin's readable support
  manifest to carry the identical origin id and path, and a change with no
  manifest gives that gate nothing to read. So the manifest lands and the
  documents stay. `proposal-support.py verify add-signed-execution-chain` passes.
- **`ideation/staging/INDEX.md`** — the topic's row and detail section record
  that tranche one was raised and that tranches two and three stay staged.
- **`README.md`** — one entry in the OpenSpec Records active block.
- **Successors, named:** `extend-signed-execution-chain-attestation` (tranche
  two, gated on Q7, the omnigent layer and the PKI plane) and
  `extend-signed-execution-chain-anchoring` (tranche three, gated on Q3 and Q6).
  The domain realizations — codexFactory's lane, MedxFactory's HealthLinc,
  LedgerxFactory's LedgerLinc — are changes in those repositories, and the
  neutral family is authored here precisely so they differ in payload and
  regulator rather than in chain shape.

## What this packet deliberately does not claim

Written out because the family's recurring defect is text that outruns its
machinery.

1. **It does not claim any chain exists.** Zero chain links exist in this corpus
   today, and zero live wallets — the baseline
   `add-wallet-carried-review-authority`'s design verified on 2026-08-23 and this
   packet re-verified at authoring. R10 exists so no reader mistakes the
   requirement text for a running control.
2. **It does not claim a merge is refused today.** No merge gate is created here.
3. **It does not claim the omnigent layer refuses anything today.** The
   precondition claim is the family's destination and belongs to tranche two,
   which needs a layer that does not yet enforce it.
4. **It does not rule on Q3, Q6 or Q7**, and carries no text whose meaning would
   change once they are ruled.
5. **It does not restate a neighbour's requirement in its own words.** Where this
   packet relies on ratified text it cites the requirement by title and takes its
   terms unchanged; where it needs something no neighbour provides, it declares a
   dependency.
