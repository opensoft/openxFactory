---
code_surface: openxFactory — AN EXTENSION OF THE TRANCHE-ONE CONTRACT FAMILY PLUS AN EXTENSION OF ITS RUNNING GATE, declared honestly because this tranche is not doctrine-only. `contracts/signed-execution-chain/` gains FIVE record kinds and one field discipline — the harness-controller SETUP ATTESTATION (link 4), the RUNNER ATTESTATION (link 5) carried together with the SIGNING REQUEST recorded beside its signature, the signed PR-OPEN DECISION (link 6), the CLOSURE record of the governed post-merge test (link 10), and the REMEDIATION DECLARATION that names an unclosed chain as a repairing chain's signed subject — plus the per-fact EVIDENCE CLASS (`controller_corroborated` / `hardware_attested` / `runner_claimed`) that keeps a runner's self-report from being read as controller-attested fact. `scripts/validate-signed-execution-chain.py` gains one named refusal per negative example, and the SHORT-CHAIN GATE tranche one wired as a required pull-request check EXTENDS from links 1–3 to links 1–6 — the same check, a longer walk, not a second gate. Packaged positive AND negative examples for every named refusal. Registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive bundle cut. NO CERTIFICATE AUTHORITY, NO issuance pipeline, NO key service, NO HSM procurement, NO anchor, NO chain, NO commitment format, NO consent plane — anchoring is the named tranche-three successor `add-chain-anchoring` and carries its own code surface. NO CHANGE TO `contracts/omnigent/omnigent-domain-overlay.schema.yaml` — no sixth archetype, no seventh permission boolean, and no widening of a closed matrix. NO SECOND identity, certificate, digest or proof vocabulary is defined: certificates are `add-trust-anchor`'s, signer identity is `add-identity-brokering`'s, and the digest construction is the ONE tranche one already put in force for every digest this capability computes.
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`. The figure is deliberately withheld rather than forgotten: `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v2.2` at this branch's tip, and `add-signed-execution-chain` — this packet's own predecessor — already names the next additive cut for the family's first contract bytes. A number written here would be a number another packet is already spending, and the realization confirms it against the manifest at ITS tip rather than trusting this line. THE CLASS IS ADDITIVE and nothing narrows: new record kinds in a family whose first cut has not shipped, no existing schema changes, no consumer pinned at the current bundle is made non-conformant, and no domain is obliged to adopt a chain. The one obligation that reaches an existing artifact — the gate's longer walk — reaches a check this family itself owns and that no domain runs.
Status: draft
Proposed: 2026-08-29
Origin: `openxFactory:staging:signed-execution-chain`, EXIT 2 OF THREE — the tranche the staged topic's `## Exit path` calls "harness and runner attestation", whose question-gate Q7 Brett Heap opened on 2026-08-29. Links 4–6 and 10. Tranche one (`add-signed-execution-chain`, ratified 2026-08-29, PR #495) is the direct predecessor and its ratified text governs every point of contact; tranche three (`add-chain-anchoring`, in parallel drafting) is a named sibling and none of its content appears here. THIS PACKET IS NOT RATIFIED. It is filed FOR COUNCIL REVIEW ON THE §7.4 PATH AND FOR BRETT HEAP'S RATIFICATION, in that order, on the pattern `add-binding-consumer-identity` established on 2026-08-29 — the first packet through that path end to end, whose `review/` directory this packet's own `review/` will mirror. Nothing in this document may be read as ratified, and `tasks.md` §2 and §3 are the two gates that stand between it and realization.
---

# Proposal: add-chain-attestation

**TRANCHE TWO of the signed-execution-chain family: links 4–6 and 10.** The
harness-controller setup attestation, the per-task runner attestations, the
signed pull-request-open decision, and the governed post-merge test that CLOSES
a chain.

**THIS PACKET IS A DRAFT AND IS FILED FOR REVIEW.** Two acts stand between it
and realization and neither has happened: a **§7.4 council review** — the
council-reviewed-but-human-approved path that needs no candidate class and no
flip, and that reaches this repository without an envelope — and, after it,
**Brett Heap's ratification**. The house pattern is
`add-binding-consumer-identity`, ratified 2026-08-29 after a sitting that
returned SPLIT 2–2 on the verdict word and UNANIMOUS 4/4 that the drafted text
was not ratifiable, with fifteen blocking amendments; the ruling was accept all
blocking, one fix round, ratification read after. This packet expects the same
treatment and asks for it: **the questions this document raises against itself
are the review's material, not decorations on a finished text.**

## Why

**Tranche one signed the ratification, and the work that runs under it is still
unsigned.** `add-signed-execution-chain` made a ratification admissible only on
wallet-carried authority proven by possession, minted a CHAIN IDENTITY in the
same signed act, carried it with the work as a TRAVELING CONTRACT, wrote every
act as a leaf in an append-only signed transparency log, and put a gate in front
of the terminal act that walks links 1–3 as a chain rather than a bag of
signatures. What it could not do is say WHAT ACTUALLY RAN.

That is not a gap in tranche one; it is the boundary Q4 ruled. Tranche one has
no link with a signer of its own after inception — the traveling contract is
CARRIED — so it establishes continuity by derivation and comparison, and it
DECLARES, in requirement text, that **the signed hash-linking rule takes effect
at the first link that has a signer of its own, which is the harness-controller
setup attestation — tranche two.** *That declaration is what this change
realizes.* From link 4 onward a signature exists, so the rule can be performed
rather than asserted.

**The specific thing an unattested chain cannot refuse** is the
fabricated-but-valid-looking record: a lane that runs a different model, at a
different version, under a different harness than the one the ratification
permitted, and whose artifacts all verify individually. Tranche one's gate would
pass it, correctly, because nothing it walks makes a claim about execution. Two
tiers answer two questions — tier 1 *who permitted this*, tier 2 *what actually
ran* — and a chain needs both.

**And the closure half is the other unsigned end.** A merge is not the end of a
chain. Tranche one's gate enforces before the merge; links 9 and 10 enforce
AFTER it, at CLOSURE, and nothing today distinguishes a chain that closed from a
chain that merged and was abandoned. That distinction is what makes promotion and
release refusable, and it is why link 10 is in this tranche rather than a later
one.

## What this change is — TRANCHE TWO, and its boundary is the staged topic's

**Links 4–6 and 10**, exactly as `## Exit path` scopes tranche two:

- **Link 4 — the harness-controller setup attestation.** The controller attests
  the environment it PREPARED, under a controller certificate expressed in
  `add-trust-anchor` vocabulary. It is the corroboration source for link 5.
- **Link 5 — runner attestations.** Per-task tier-2 identities, signed AT the
  controller by remote signing it serves, with the runner's signing REQUEST
  recorded beside the signature it received.
- **Link 6 — the signed pull-request-open decision.** Opening a pull request is
  a decision and is signed as one.
- **Link 10 — the governed post-merge test**, consuming the proposal AND the
  review notes, and the CLOSURE semantics that make a merged-but-unclosed chain
  a refusing state.

**Three rules ride with them**, each because leaving it out would leave a hole
the links themselves create:

- the **signed hash-link rule taking effect**, with the gate's walk extended
  from links 1–3 to links 1–6;
- **tier-2 custody** — the attestation key never enters a worker, in every
  configuration;
- the **omnigent precondition** — the executing layer refuses a step whose
  inbound chain does not verify.

**NOT in this change, and named rather than implied:** the on-chain anchoring
and consent layer is the sibling tranche-three change **`add-chain-anchoring`**,
in parallel drafting; **link 7's council seat signatures as a walked link** stay
outside the gate's scope, exactly as tranche one left them; and no certificate
authority, key service, HSM or anchor is created here.

## The question this packet puts to the council FIRST — Q4's re-derivation instruction

**Raised at the top rather than buried, because it is an objection to this
packet's own existence and the review is where it belongs.**

Q4, ruled by Brett Heap on 2026-08-29 AS RECOMMENDED, says tranche one is links
1–3 only and then adds: *"The later boundaries are RE-DERIVED when the omnigent
layer and the PKI plane are real, not fixed now — a boundary drawn against an
unbuilt layer is a guess wearing a tranche number."* **Neither is real today.**
`implement-openxpki-install-repo` is an ACTIVE change at 22/30 tasks; the
omnigent layer is a contract family with domain overlays and no runtime that
enforces a chain precondition.

**What this packet does about that, and what it does not.** It does not claim
the instruction is satisfied, and it does not rule on it — that is not this
document's act. It does three things instead:

1. **It ratifies-not-realizes, and says so in its own front matter.** The
   `code_surface` names contract bytes and a gate extension; `tasks.md` §5 is
   the realization commission and it is gated on both planes being real. This is
   `add-binding-consumer-identity`'s pattern: ratification authorizes
   realization and does not perform it.
2. **It writes requirements that name no interface either plane must expose.**
   Link 4's certificate is described in `trust-anchor`'s already-ratified
   vocabulary — anchor record, recorded issuance authority, declared custody,
   revocation at use — and NOT in terms of any API OpenXPKI happens to offer.
   The omnigent precondition is a REFUSAL composed with a closed permission
   matrix and adds nothing to it. A boundary written this way is re-derivable
   because it commits to no shape the unbuilt layers might not take.
3. **It puts the re-derivation in `tasks.md` as an explicit obligation of the
   realization**, so the instruction survives ratification rather than being
   discharged by it.

**Whether that is enough is the council's call and then Brett's.** A seat that
reads Q4 as forbidding the drafting of tranche two until both planes are real is
reading it literally, and the literal reading is available on the text. The
packet's answer is that a boundary is a guess when it is drawn AGAINST an unbuilt
layer's shape, and this one is drawn against ratified neutral vocabulary that
already exists — but that is an argument offered for review, not a ruling taken.

## The ruled inputs, cited

**Q7 — ruled 2026-08-29 by Brett Heap, AS RECOMMENDED, and this packet is where
it lands.** Attestation signatures happen by **remote signing served by the
harness controller**; the runner's signing **request is recorded alongside the
signature** it received; the controller **corroborates the submitted payload
against its own link-4 setup attestation** — it signs, it does not notarize
self-report; and **an HSM is a later HARDENING of the same shape**, not a
different answer. The staged topic records the gate this ruling opened in terms:
*"this gated TRANCHE TWO's contract text, which may now name the mechanism."*
Requirements 2, 3 and 4 of the delta are that ruling in requirement form, and
requirement 3 carries the half a mechanism does not discharge: **Q7 settles where
the key lives, never whether the claims are checked.**

**The tier model, which the topic derives from a ratified constraint rather than
choosing.** Every omnigent worker archetype carries `access_secrets: false` as a
constitutional constraint, so a worker cannot hold an authority credential — and
the same constraint reaches the ATTESTATION key, because `access_secrets: false`
is written to hold in *every* configuration and **a short lifetime does not stop
a private key being a secret**. "Ephemeral" describes the identity's lifetime,
never a relaxation of custody. Requirement 4 is that, and it is stated as a
CUSTODY rule rather than a lifetime rule for exactly that reason.

**The two enforcement horizons, and the remediation exemption.** The topic:
links 1–7 are enforced at the gate, and *"the chain is not complete at merge, it
is complete at CLOSURE"*; a merged-but-unclosed chain *"is a refusing state for
whatever consumes the merge … and fires link 9's fraud signal"*, while *"a merge
that already happened cannot be retroactively refused"*. One consumer is exempt
by design **or the invariant deadlocks** — the remediation chain, *"still a full
chain, ratified and signed like any other"*, whose *"declared, signed subject is
that failure"*, with promotion and release still refused until a chain closes.
Requirements 7 and 8 are those two paragraphs, with the exemption's conditions
made enforceable rather than described.

**The omnigent enforcement claim, which the topic calls the claim that makes it
worth raising.** *"The layer refuses to build an unverified chain … a claim about
a PRECONDITION, not about record-keeping."* The weak version is an audit trail a
compromised lane can write falsely; the strong version moves verification from
after to before. Requirement 9.

## Composition — what is consumed, and where each vocabulary is cited

**No second vocabulary is invented.** The staged topic names this as its first
risk: *"The collision risk this topic must actively avoid is inventing a second
identity or certificate vocabulary. Three of the four changes above already own
one."* Every point of contact is cited to the artifact that owns it.

| Consumed | What it contributes | Where the delta consumes it |
| --- | --- | --- |
| `add-trust-anchor` (ACTIVE, ratified 2026-08-21, realized at `contract-v1.37`) | Certificates and anchors. Four ratified obligations bind link 4 by composition: trust is through an ANCHOR RECORD and never a certificate's own strength; issuance is under RECORDED AUTHORITY with issuance evidence; DECLARED CUSTODY bounds what a signature evidences (host-readable evidences the HOST acted); REVOCATION IS CHECKED AT USE and propagates transitively. Its **conformance-declaration rule** is what a realization uses where the operated authority evidences less than the obligation requires | Requirement 1, all five scenarios |
| `implement-openxpki-install-repo` (ACTIVE, 22/30) | The runtime CA that would issue the controller certificate, at `opensoft/OpenXPKI-Install`. Its ratified boundary keeps openxFactory the canonical owner of the neutral `trust-anchor` contract while *"the install repository realizes both and owns neither"* | Requirement 1, as a REALIZATION DEPENDENCY explicitly not assumed. This packet creates no CA |
| `add-identity-brokering` (ACTIVE, 20/30) | Signer identity. Its ratified **"Workloads are not personas"** requirement is what the delta consumes, and it contributes a REFUSAL: a workload, agent, job or service is not a persona, its authority comes from `credential-contracts` grants and `openxwallet` holders, and it **never appears as the actor of a governed act**. A per-task attestation identity is a workload by that definition | Requirement 2, two scenarios. The human actor stays link 1's stable opaque subject, per tranche one's actor-binding requirement |
| `contracts/omnigent/` (the neutral overlay family, registered since `contract-v1.16`) | The closed six-boolean permission matrix — `additionalProperties: false`, `execute_final_action` and `access_secrets` both `const: false` — over five archetypes `frame` / `generate` / `verify` / `challenge` / `assemble_for_admission` | Requirement 4 (custody's constitutional ground) and requirement 9 (the precondition composes with the matrix and widens nothing). **No schema change** |
| `add-wallet-carried-review-authority` (ACTIVE; S2 issuer anchor REALIZED, read inside the REQUIRED `wallet-validation` check) | Review authority as a wallet-carried grant with an anchored root issuer, exercised with proof of possession. It is what makes a review record's AUTHORITY establishable rather than merely its bytes | Requirement 7 — closure establishes the review record was produced under proven review authority, in this shipped vocabulary and no second one |
| `add-signed-execution-chain` (ACTIVE, RATIFIED 2026-08-29) | The chain identity, the ONE digest construction governing every digest including those a later tranche adds, the traveling contract, the transparency log AS THE RECORD, the short-chain gate, and the DECLARATION that the hash-link rule takes effect at link 4 | Requirement 6 realizes that declaration AND derives the authoritative predecessor set from the log by a defined query; requirements 1–9 write leaves into the same log and compute no digest under a second construction |

## Capabilities

### New Capabilities

**None.** This change adds no capability. It extends the `signed-execution-chain`
capability tranche one created.

### Modified Capabilities

- `signed-execution-chain`: **NINE ADDED requirements over 59 scenarios**, and
  **no `## MODIFIED Requirements` block anywhere** — the harness-controller
  setup attestation under a `trust-anchor` certificate; runner attestations
  signed at the controller on a recorded request, with signer identity refused
  the persona population; the controller corroborating rather than notarizing,
  with a per-fact evidence class so a runner's self-report cannot be read as
  attested; tier-2 keys that never enter a worker in any configuration; the
  pull-request open as a signed, chain-bound decision; the signed hash-link rule
  taking effect at link 4 with the gate's walk extended to links 1–6 and a
  completeness rule for plural predecessors; closure as the point a chain
  completes, with a merged-but-unclosed chain refusing everything downstream;
  the remediation chain as the one admitted consumer, its exemption
  non-inheritable; and the executing layer refusing a step whose inbound chain
  does not verify.

## Why this delta is ADDED-ONLY, and the one composition that needed writing down

**There is no `## MODIFIED Requirements` block in this packet.** That is a
deliberate choice with a cost, and both are recorded.

Tranche one's gate requirement bounds itself: *"The gate's scope at this tranche
is links 1–3 and it SHALL NOT report the absence of a later tranche's link as a
break, because a gate cannot walk a link that does not exist yet"*, with a
scenario headed **"a tranche-two link does not exist yet"**. Read as a standing
rule, that sentence would let a chain carrying no attestation links pass the gate
forever. Read as what it says — a scope note conditioned on a link that does not
exist YET — it is spent the moment this tranche's links exist.

**This packet takes the second reading and writes it into requirement text**
rather than leaving it to a reader: requirement 6 states that links 4–6 STOP
BEING "a later tranche's link" on this tranche's realization, and carries a
scenario for exactly the chain that arrives with links 1–3 only. **The reading is
reported as a reading, not applied silently** — it is in the delta, in
`design.md` D3, and in this pull request's body, and it is the second thing the
council is asked to rule on after Q4.

**Why not a MODIFIED delta instead.** Tranche one is an ACTIVE change: its
requirement lives in a sibling's ADDED delta and not in `openspec/specs/`, so a
MODIFIED block here would restate a requirement that canon does not yet hold, and
its correctness would depend on which of the two changes archives first. That is
the promotion-order hazard the repository is currently governing in its own right
(openxFactory issue **#502** and the `govern-sibling-added-modified-deltas`
change raised against it). **If the council rules the composition insufficient,
the repair is a scenario-complete MODIFIED restatement of tranche one's gate
requirement — all twelve scenarios, not the two that change** — and this packet
names that as the remedy rather than leaving the alternative unstated.

## Impact

- **New code (this change would authorize; realization is a later commission):**
  five record kinds and one field discipline in `contracts/signed-execution-chain/`,
  packaged positive and negative examples for every named refusal, the validator's
  new refusals, and the EXTENSION of the existing required pull-request check from
  links 1–3 to links 1–6. Manifest and CHANGELOG registration at the next additive
  bundle.
- **Realization dependencies, and they are hard:** the **omnigent layer** must be
  real enough to enforce a precondition, and **`implement-openxpki-install-repo`**
  must be real enough to issue a controller certificate. Neither is today.
  Ratification of this packet would authorize the contract feature and NOT its
  deployment; `tasks.md` §5 is gated on both.
- **Obliges no domain.** No domain must adopt a chain. MedxFactory/HealthLinc and
  LedgerxFactory/LedgerLinc remain the neutrality proof and not consumers under
  obligation.
- **Touches no promoted specification.** Every capability this composes with is
  either an ACTIVE change whose ratified text governs or a shipped contract family
  consumed by reference.

## Where the ruled topic and a ratified artifact pull against each other

Recorded rather than smoothed, on this family's contested-finding rule. **Neither
is resolved by this packet's own authority; both are review material.**

**1. Q4's re-derivation instruction versus drafting tranche two now.** Stated in
full above, at the top, because it is an objection to the packet's existence
rather than to a line in it. The packet's position — ratifies-not-realizes, a
boundary drawn against ratified vocabulary rather than unbuilt shape, and the
re-derivation carried as a realization obligation — is an argument, not a
disposition.

**2. Tranche one's gate scope note versus the extended walk.** Stated in full
above. The packet takes the self-limiting reading and writes it down; the
alternative repair is named.

**3. The topic's link table gives link 5 a plural signer, and the hash-link rule
it states is singular.** *"Every link from enrollment onward signs over two
things besides its own content: the chain identity … and the digest of the link
that precedes it."* But link 5 is *"each runner attests"* — plural — so "the
link that precedes it" has no single referent for link 6. **This packet resolves
it by ADDITION rather than by choosing a referent:** a successor commits to an
ORDERED, DEDUPLICATED ENUMERATION of every predecessor record, and a successor
committing to a proper subset is refused. Without the rule, a lane could DROP THE
ATTESTATION IT DISLIKES and still present a continuous chain — which is the
mix-and-match attack the topic's own review round raised, arriving through a
different door. **This one IS resolved here**, because it is a gap in the topic
rather than a conflict with a ruling; it is flagged so a reviewer can disagree.

## What the first bot round corrected, before any review

Three P1 findings on this packet's own pull request, all real, and **all of one
shape: a record that NAMED something was standing where a record that ESTABLISHES
it belonged.** That is tranche one's *"a reference is not a binding"* defect
arriving three times at three different links, which is why the shape is recorded
and not just the fixes. Full reasoning in `design.md` D10.

1. **The signing request was recorded and not ATTRIBUTED.** An opportunistic
   caller that can reach the signing service could submit a payload corroborating
   against link 4 and receive a signature indistinguishable from the provisioned
   task's — satisfying every stated refusal. Worse, `design.md` D1 had explicitly
   claimed the record closed that case. Requirement 2 now requires the controller
   to ATTRIBUTE the request to the task it provisioned, refuse what it cannot
   attribute, and cover requester, chain identity and payload digest INSIDE the
   signed bytes — **with the residual DECLARED**, because `access_secrets: false`
   forbids the obvious mechanism of a request credential held by the runner.
2. **"A proper subset" named nothing.** The gate had no authoritative set to take
   a subset OF, so a lane omitting an unwanted link-5 record BEFORE presenting
   link 6 produced an enumeration complete over everything visible — the rule
   passed the exact chain it existed to refuse. Requirement 6 now has the gate
   DERIVE the complete set from the transparency log by a DEFINED QUERY and
   requires EQUALITY, inheriting tranche one's declared suffix-truncation residual
   rather than re-declaring it.
3. **Closure bound to the review record's BYTES and not its AUTHORITY.** A digest
   proves only that bytes did not change after signing, so a supplied or
   fabricated review record could be consumed by a passing test and CLOSE THE
   CHAIN — at the one link with no gate behind it. Requirement 7 now requires the
   review record to be established under review authority PROVEN BY POSSESSION in
   `add-wallet-carried-review-authority`'s shipped vocabulary, **and declares what
   that does not establish** — that every seat signed — naming a walked link-7
   check as what would close it.

**None was repaired by inventing vocabulary**, which is the constraint the staged
topic names as this family's first risk.

## The two acts that must follow, in order

**1. §7.4 council review.** The council-reviewed-but-human-approved path that
per the 2026-08-26 record *"needs no class and no flip"* and *"reaches this
repository without an envelope and without amending FR-008"*. This packet creates
no `merge-approval-envelope`, declares no candidate class, and leaves
`specs/025-openxfactory-review-lane-caller/spec.md` FR-008 exactly where the
2026-08-28 convening left it: gated and undischarged. The review's record lands
in `review/`, mirroring `add-binding-consumer-identity`'s directory.

**2. Brett Heap's ratification.** After the review and any fix round it forces.
Until it happens this packet is `Status: draft`, its requirements confer and
refuse nothing, and no realization may begin — and even ratification would
authorize the contract feature rather than perform it.
