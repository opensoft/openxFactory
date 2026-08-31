---
code_surface: openxFactory — AN EXTENSION OF THE TRANCHE-ONE CONTRACT FAMILY PLUS AN EXTENSION OF ITS RUNNING GATE, declared honestly because this tranche is not doctrine-only. `contracts/signed-execution-chain/` gains SEVEN record kinds and three field disciplines — the harness-controller SETUP ATTESTATION (link 4) carrying the COMMITTED EXPECTED ATTESTATION SET inside its signed bytes, the CONTROLLER-SIGNED COMMITMENT EXTENSION that serves a dynamic fan-out and is written at or before the DISPATCH of the task it adds, the CONTROLLER-SIGNED TIER-2 SIGNED CHAIN BINDING carrying an identity's SUBJECT SCOPE, its CLOSED RECORD-KIND ENUMERATION and THE CHAIN IDENTITY IT SERVES, and referencing by identifier the two CANONICAL `add-trust-anchor` records it composes with — the `certificate-record` for the key and validity bounds and the `issuance-evidence` for the issuance act, both CONSUMED UNMODIFIED AND NEITHER DEFINED HERE, which is what keeps the no-second-certificate-vocabulary rule intact, the RUNNER ATTESTATION (link 5) carried together with the SIGNING REQUEST recorded beside its signature, the signed PR-OPEN DECISION (link 6), the CLOSURE record of the governed post-merge test (link 10), and the REMEDIATION DECLARATION that names an unclosed chain as a repairing chain's signed subject — plus TIER 2's TWO SUBJECT SCOPES, each with its own CLOSED ENUMERATION of authorized record kinds — the PER-TASK identity signs the task attestation (link 5) and nothing else, the ONE CHAIN-SCOPED identity per chain signs the aggregate records (link 6, link 10), and no authority record is signable under either, ever — plus the per-fact EVIDENCE CLASS (`controller_corroborated` / `independently_observed` / `runner_claimed`, ORDERED and composed with the ratified `contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml` rather than beside it) that keeps a runner's self-report from being read as controller-attested fact — plus THE SIGNER'S PUBLIC KEY CARRIED BESIDE EVERY SIGNATURE on every record this capability defines, which is the field verification RESOLVES against the consumed certificate's `subject.public_key_fingerprint` before any signature is checked, and without which the key-resolution rule has no input. `scripts/validate-signed-execution-chain.py` gains one named refusal per negative example, and the SHORT-CHAIN GATE tranche one wired as a required pull-request check EXTENDS from links 1–3 to links 1–6 — the same check, a longer walk, not a second gate. Packaged positive AND negative examples for every named refusal. Registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive bundle cut. NO CERTIFICATE AUTHORITY, NO issuance pipeline, NO key service, NO HSM procurement, NO anchor, NO chain, NO commitment format, NO consent plane — anchoring is the named tranche-three successor `add-chain-anchoring` and carries its own code surface. NO CHANGE TO `contracts/omnigent/omnigent-domain-overlay.schema.yaml` — no sixth archetype, no seventh permission boolean, and no widening of a closed matrix. NO SECOND identity, certificate, digest or proof vocabulary is defined: certificates are `add-trust-anchor`'s, signer identity is `add-identity-brokering`'s, and the digest construction is the ONE tranche one already put in force for every digest this capability computes. ONE `## MODIFIED Requirements` BLOCK, added in the 2026-08-30 council fix round, restates tranche one's gate requirement SCENARIO-COMPLETE AT ALL NINE SCENARIOS to re-scope the gate and extend its closed-list mapping table to all eighteen of this capability's requirements — it moves the SAME contract bytes the ADDED-only draft did and adds no record kind.
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`. The figure is deliberately withheld rather than forgotten: `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v2.2` at this branch's tip, and `add-signed-execution-chain` — this packet's own predecessor — already names the next additive cut for the family's first contract bytes. A number written here would be a number another packet is already spending, and the realization confirms it against the manifest at ITS tip rather than trusting this line. THE CLASS IS ADDITIVE and nothing narrows: new record kinds in a family whose first cut has not shipped, no existing schema changes, no consumer pinned at the current bundle is made non-conformant, and no domain is obliged to adopt a chain. The one obligation that reaches an existing artifact — the gate's longer walk — reaches a check this family itself owns and that no domain runs.
Status: draft
Proposed: 2026-08-29
Origin: `openxFactory:staging:signed-execution-chain`, EXIT 2 OF THREE — the tranche the staged topic's `## Exit path` calls "harness and runner attestation", whose question-gate Q7 Brett Heap opened on 2026-08-29. Links 4–6 and 10. Tranche one (`add-signed-execution-chain`, ratified 2026-08-29, PR #495) is the direct predecessor and its ratified text governs every point of contact; tranche three (`add-chain-anchoring`, in parallel drafting) is a named sibling and none of its content appears here. THIS PACKET IS NOT RATIFIED. It was filed FOR COUNCIL REVIEW ON THE §7.4 PATH AND FOR BRETT HEAP'S RATIFICATION, in that order, on the pattern `add-binding-consumer-identity` established on 2026-08-29 — the first packet through that path end to end, whose `review/` directory this packet's own `review/` mirrors. THE COUNCIL REVIEW IS HELD: `tasks.md` §2 was discharged by the sitting of 2026-08-30 — four seats, unanimous 4/4 that the drafted text was not ratifiable, thirteen blocking amendments, all discharged in the fix round. **`tasks.md` §3, BRETT HEAP'S RATIFICATION, IS THE SOLE REMAINING GATE BETWEEN THIS PACKET AND REALIZATION, AND IT IS NOT TAKEN.** Nothing in this document may be read as ratified.
---

# Proposal: add-chain-attestation

**TRANCHE TWO of the signed-execution-chain family: links 4–6 and 10.** The
harness-controller setup attestation, the per-task runner attestations, the
signed pull-request-open decision, and the governed post-merge test that CLOSES
a chain.

**THIS PACKET IS A DRAFT. ITS COUNCIL REVIEW IS HELD AND ITS RATIFICATION IS
PENDING.** Two acts stand between it and realization; **the first has happened
and the second has not.** The **§7.4 council review** — the
council-reviewed-but-human-approved path that needs no candidate class and no
flip, and that reaches this repository without an envelope — **was held on
2026-08-30**: four seats, **UNANIMOUS 4/4 that the drafted text was not
ratifiable**, THIRTEEN blocking amendments after two were elevated, all
discharged in the fix round, with the packet, ballot, four verbatim seat returns,
record and disposition filed at `review/`. **Brett Heap's ratification has NOT
been taken**, and until it is this packet is `Status: draft`, its requirements
confer and refuse nothing, and no realization may begin.

The house pattern is `add-binding-consumer-identity`, ratified 2026-08-29 after a
sitting that returned SPLIT 2–2 on the verdict word and UNANIMOUS 4/4 that the
drafted text was not ratifiable, with fifteen blocking amendments; the ruling was
accept all blocking, one fix round, ratification read after. **This packet asked
for the same treatment and got it** — the questions it raised against itself were
the review's material rather than decorations on a finished text, and the
sitting's decisive finding was reached by BUILDING the canon this delta would
promote rather than by reading its prose.

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
| `add-identity-brokering` (ACTIVE, 20/30) | Signer identity. Its ratified **"Workloads are not personas"** requirement is what the delta consumes, and it contributes a REFUSAL: a workload, agent, job or service is not a persona, its authority comes from `credential-contracts` grants and `openxwallet` holders, and it **never appears as the actor of a governed act**. A tier-2 attestation identity is a workload by that definition, at either subject scope | Requirement 2, two scenarios. The human actor stays link 1's stable opaque subject, per tranche one's actor-binding requirement |
| `contracts/omnigent/` (the neutral overlay family, registered since `contract-v1.16`) | The closed six-boolean permission matrix — `additionalProperties: false`, `execute_final_action` and `access_secrets` both `const: false` — over five archetypes `frame` / `generate` / `verify` / `challenge` / `assemble_for_admission` | Requirement 4 (custody's constitutional ground) and requirement 9 (the precondition composes with the matrix and widens nothing). **No schema change** |
| `add-wallet-carried-review-authority` (ACTIVE; S2 issuer anchor REALIZED, read inside the REQUIRED `wallet-validation` check) | Review authority as a wallet-carried grant with an anchored root issuer, exercised with proof of possession. It is what makes a review record's AUTHORITY establishable rather than merely its bytes | Requirement 7 — closure establishes the review record was produced under proven review authority, in this shipped vocabulary and no second one |
| `add-signed-execution-chain` (ACTIVE, RATIFIED 2026-08-29) | The chain identity, the ONE digest construction governing every digest including those a later tranche adds, the traveling contract, the transparency log AS THE RECORD, the short-chain gate, and the DECLARATION that the hash-link rule takes effect at link 4 | Requirement 6 realizes that declaration; the AUTHORITATIVE predecessor set is link 4's COMMITTED EXPECTATION and the log is the SECONDARY, bidirectional check against it (every committed task has a leaf; every leaf is covered by the commitment); requirements 1–9 write leaves into the same log and compute no digest under a second construction |

## Capabilities

### New Capabilities

**None.** This change adds no capability. It extends the `signed-execution-chain`
capability tranche one created.

### Modified Capabilities

- `signed-execution-chain`: **NINE ADDED requirements over 104 scenarios**, plus
  **ONE `## MODIFIED Requirements` block — tranche one's gate requirement,
  SCENARIO-COMPLETE AT ALL NINE OF ITS SCENARIOS** — the harness-controller
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

## Why this delta now carries ONE MODIFIED block, and why the ADDED-only draft was wrong

**The council ruled it, and it was proved by construction rather than argued.**
The §7.4 sitting of 2026-08-30 was **UNANIMOUS 4/4 that this packet as drafted
was not ratifiable**, and its decisive finding was reached by BUILDING the canon
these two changes actually promote: `lead-architect` archived tranche one and
then this packet into a scratch tree and read the result. It composed
mechanically — 18 requirements, 104 scenarios, `openspec` reporting `~ 0`
modified — **and held two contradictory scenarios on one antecedent, both
normative, both promoted:**

```
promoted canon :552   a chain carrying no attestation link
                      -> "validates links 1–3 … the absent later link is not reported as a break"
promoted canon :1141  the same chain, after this tranche
                      -> REFUSES
```

**The earlier draft's reasoning about the SENTENCE was right, and its conclusion
about the SCENARIO was wrong.** Tranche one's scope note does self-limit — *"at
this tranche"*, *"a later tranche's link"*, *"a link that does not exist yet"* —
but **prose in one requirement cannot repeal a scenario living in another**, and
no validator in the estate notices, because each delta is independently valid.

**The repair is in this packet:** a `## MODIFIED Requirements` block over tranche
one's gate requirement, **SCENARIO-COMPLETE AT ALL NINE OF ITS SCENARIOS** (the
figure is nine — an earlier draft said *twelve* at four sites, and three seats
measured it independently at nine). It re-scopes the gate to the links the
RATIFIED TRANCHES have put in force, re-conditions the scenario on a link no
tranche has yet put in force, and **extends the closed-list mapping table from
nine rows to all eighteen** of this capability's requirements — because tranche
one's *"THE LIST IS CLOSED … every requirement of THIS CAPABILITY is either
walked here or has its enforcement point named below"* is scoped to the
CAPABILITY, so promoted canon would otherwise have asserted that this packet's
own nine are requirements the capability does not enforce.

**The cost the earlier draft named is real, is accepted, and is recorded.**
Tranche one is an ACTIVE change: its requirement lives in a sibling's ADDED delta
and not in `openspec/specs/`, so this MODIFIED block restates a requirement canon
does not yet hold and its correctness depends on ARCHIVE ORDER — tranche one
first, the only order in which this capability exists to be modified. That is the
promotion-order hazard the repository is governing in its own right (openxFactory
issue **#502** and `govern-sibling-added-modified-deltas`, PR #504). It is a
known dependency of this packet, not a reason to leave prose where a delta
belongs.

## The naming divergence, stated rather than left to be noticed

`add-signed-execution-chain`'s ratified text
(`openspec/changes/add-signed-execution-chain/proposal.md:82-100`) names this
tranche **`add-signed-execution-chain-attestation` (working id)** and its sibling
**`add-signed-execution-chain-anchoring` (working id)**. Both are raised under
shorter identifiers — **`add-chain-attestation`** here and
**`add-chain-anchoring`** for tranche three — and **the word "working" in the
ratified text is what admits the change**: no ratified identifier is broken,
because tranche one marked both successor names as provisional on their face. It
is recorded here rather than glossed, because a reader arriving from the ratified
packet will look for the longer name and should find out in ONE PLACE why it is
not there. **Nothing else moved**: the successor this packet raises is the
successor that packet named, with the same content boundary — links 4–6 and 10.

**This section is owed, and it is owed because the sibling already paid it.**
`add-chain-anchoring` carries the same section; a grep for the long id in this
packet returned zero before this round. The council's decision 12 ruled the short
ids STAND and that **#510 owes the back-citation #513 already made**. A
back-citation in the RATIFIED packet itself — so a reader grepping tranche one
for its successors finds the ids as raised — is a separate, later act on that
change and is not performed here.

## Impact

- **New code (this change would authorize; realization is a later commission):**
  SEVEN record kinds and three field disciplines in `contracts/signed-execution-chain/`
  — the same set the `code_surface` header enumerates —
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

**1. Q4's re-derivation instruction versus drafting tranche two now. RULED
2026-08-30: NOT PREMATURE, BUT NARROWED.** The §7.4 sitting ruled the threshold
question in this packet's favour on all three seats whose charter reaches it, and
narrowed it: the re-derivation tranche one's ratified `tasks.md:5.3` owes *"when
each is raised"* is due AT THIS RAISING and not only at realization. **It is now
PERFORMED, dated and measured, at `design.md` D7a**, and the boundary it derives
confirms links 4–6 and 10 with no link moved. The packet's original position —
ratifies-not-realizes, a boundary drawn against ratified vocabulary rather than
unbuilt shape — survives the ruling and is no longer the packet's only answer.

**2. Tranche one's gate scope note versus the extended walk. RESOLVED
2026-08-30, AGAINST THE PACKET'S FIRST READING.** The earlier draft took the
self-limiting reading and wrote it into requirement text. The council proved by
construction that prose cannot repeal a scenario in another requirement, and the
packet now carries the scenario-complete MODIFIED restatement it had named only
as an alternative. **The contested pull is discharged rather than carried**, and
what remains recorded is that this packet got it wrong first.

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
   passed the exact chain it existed to refuse. **That round** had the gate DERIVE
   the complete set from the transparency log by a DEFINED QUERY and require
   EQUALITY, inheriting tranche one's declared suffix-truncation residual rather
   than re-declaring it. **That repair is SUPERSEDED by the second bot round
   below**: the authoritative set is now LINK 4's COMMITTED EXPECTATION and the
   log comparison is a secondary check. The equality discipline survives; the
   source of the set moved.
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

## What the SECOND bot round corrected, after the council fix round

Two P1 findings on the fix round's own head, both real, and **both of one shape:
a rule that could not be CONSTRUCTED as written.** A different shape from the
first round's, and recorded separately for that reason. Full reasoning in
`design.md` D11.

1. **The completeness rule could not detect the attack it was written for.** The
   authoritative link-5 set was DERIVED FROM THE LOG, so a lane that never wrote
   an unwanted attestation — rather than omitting it from the submission —
   produced an enumeration EQUAL to the derived set and passed the gate. The
   leaf-ordering obligation the council's LQ-A3 added could only refuse the leaf
   once it appeared, which is after a merge that is not retroactively refused,
   and a leaf never written never appears. **The authority moves to LINK 4's
   COMMITTED EXPECTATION**: the controller commits the dispatched task set inside
   the bytes it signs, extensible before each attestation it covers, and the gate
   compares link 6's enumeration for EQUALITY against that. **`lead-security`'s
   LS-F5 had already named the same missing instrument** — *"link 4 records the
   provisioned environment but no count of expected runner tasks, so there is no
   independent cardinality to check equality against"* — so the repair discharges
   a seat finding as well as a bot one.
2. **No conforming link 6 was constructible.** Requirement 2 bounded the per-task
   tier-2 identity to *"exactly one thing — signing an attestation about that
   task"*, while requirements 5 and 7 required that same identity to sign a
   DECISION and a TEST OUTCOME. Two requirements of one capability demanded
   opposite things and every realization would have had to breach one. **Repaired
   by widening to a CLOSED, NAMED ENUMERATION** of the identity's authorized
   record kinds — link 5, link 6, link 10 — with authority records excluded from
   it permanently, so that widening what tier 2 may SAY never widens what tier 2
   may PERMIT.

**Neither was repaired by inventing vocabulary either.** The commitment is a
field on the record link 4 already is, its extension is signed by the signer link
4 already has, and the enumeration names three record kinds this delta already
required.

## What the THIRD bot round corrected — the same conflict one level up

**The record-kind enumeration fixed FORM and left SUBJECT unfixed.** Link 6 is
ONE decision committing to EVERY link-5 attestation, and link 10 is ONE test
outcome over that same whole, so a signer valid for one task and authorized only
for records ABOUT that task still could not produce either **once a chain fans
out past one task**. The ordinary dynamic-fan-out case had no conforming link 6
through two successive repairs.

**TIER 2 NOW SPLITS BY SUBJECT SCOPE.** The controller issues, alongside the
per-task identities, exactly ONE **chain-scoped tier-2 identity** per chain: the
per-task enumeration shrinks to the task attestation (link 5) alone, and the
chain-scoped identity carries the aggregate records (link 6, link 10) — records
whose subject IS the chain. Both scopes are tier 2, ephemeral, keyed at the
controller's signing boundary, with `access_secrets: false` untouched: **adding a
SUBJECT SCOPE moves no key and widens no permission**, and authority records stay
outside BOTH enumerations forever. Composing N task-scoped decisions was refused:
the staged topic's authoritative link table gives link 6 ONE signed decision, and
assembling one link from several signatures would invent a link the family does
not have. Full reasoning, and the departure from the topic's signer column, at
`design.md` **D11a**.

**And the gate's enforcement mapping was stale in the same round** — the MODIFIED
block still said *"log-derived authoritative set"*, contradicting the corrected
rule. It now names link 4's committed expectation as THE AUTHORITY with the
bidirectional log comparison SECONDARY, and a packet-wide sweep corrected four
further sites still reading in the superseded present tense.

## What the FOURTH bot round corrected — the result, and a stale fixture

**BIND BEFORE SIGN'S LAST UNCOVERED LIMB.** Every other link had moved its CLAIMS
to the controller; **link 10 had left its RESULT with the lane.** The
corroboration rule binds an attestation's fields against link 4 and establishes
nothing about whether the post-merge test RAN, PASSED, or ran against the merged
work — so a lane supplying a fabricated passing outcome on an otherwise valid
chain obtained a controller signature over it and **CLOSED THE CHAIN**,
unblocking promotion and release.

**Link 10 now binds, inside the controller-signed bytes**: an AUTHENTICATED TEST
EXECUTION the controller itself dispatched or observed; the EXACT TESTED
REVISION, which must EQUAL the merge commit the chain closed over; and the
RESULT. A merely runner- or lane-claimed outcome is REFUSED as closure grounds,
fail-closed, leaving the chain merged-but-unclosed exactly as the two enforcement
horizons already provide — **nothing here reaches back through the merge**.

**AND NO DECLARED-SHORTFALL PATH EXISTS FOR THE OUTCOME**, stated in terms rather
than inferred. This is the first live application of the council's **LS-A10**
floor: a realization that cannot establish its test's execution, revision or
result cannot DECLARE its way to a closed chain, because the declaration would
disqualify the chain from closure and closure is the only thing this link
confers. The requirement's two genuine declared shortfalls do not extend to it.

**MISSING, FAILED, UNSIGNED and now UNESTABLISHED are FOUR outcomes recorded as
four** — an outcome the controller could not establish is a different fact from a
test that ran and failed, and the enumeration exists to preserve exactly that
distinction.

**A stale FIXTURE, one field over from the last round's sweep.** `tasks.md` 5.5
still commissioned a positive example in which a per-task identity signs links 6
and 10 — impossible under the closed enumeration, and explicitly refused by it.
The earlier sweep covered PREDICATES and not FIXTURES, which is the transferable
part: a superseded rule survives in the examples commissioned against it, not
only in the sentences asserting it. Withdrawn, named as withdrawn, replaced by
the chain-scoped positive case. Full reasoning at `design.md` **D11b**.

## The two acts, in order — ONE IS DONE, ONE IS OUTSTANDING

**1. §7.4 COUNCIL REVIEW — ✅ HELD 2026-08-30. THIS STEP IS COMPLETE AND IS NOT
TO BE REPEATED.** The council-reviewed-but-human-approved path that per the
2026-08-26 record *"needs no class and no flip"* and *"reaches this repository
without an envelope and without amending FR-008"*. It ran as designed: four seats
returned, **UNANIMOUS 4/4 that the drafted text was not ratifiable**, thirteen
blocking amendments after Brett Heap elevated two, and the fix round discharged
all thirteen. The record, the sole disposition, the ballot as put, the packet as
read and the four verbatim seat returns are filed in `review/`, mirroring
`add-binding-consumer-identity`'s directory. **This packet still creates no
`merge-approval-envelope`, declares no candidate class, and leaves
`specs/025-openxfactory-review-lane-caller/spec.md` FR-008 exactly where the
2026-08-28 convening left it: gated and undischarged** — the sitting changed
none of that.

**2. BRETT HEAP'S RATIFICATION — ⬜ NOT TAKEN. THIS IS THE SOLE REMAINING GATE.**
It follows the review and the fix rounds it forced. **Until it happens this
packet is `Status: draft`**, its requirements confer and refuse nothing, and no
realization may begin — and even ratification would authorize the contract
feature rather than perform it.

**A reader arriving at this section should advance the packet to step 2 and to
nothing else.** Five bot rounds have also run, four of them after the council;
their findings are recorded as corrections in `design.md` D10, D11, D11a, D11b
and D11c. None of them is a gate — only the two acts above are.
