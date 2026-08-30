# Design: add-chain-attestation (tranche two)

Only decisions that are REAL decisions are recorded here — where a reader would
otherwise reasonably choose differently, or where this change departs from, or
fills a gap in, the staged topic's own wording. Everything the topic and tranche
one already settle is consumed by reference rather than re-argued.

**This document is part of a DRAFT packet.** Nothing in it is ratified. Where a
decision is this packet's own rather than a ruling's, it says so in terms, and
those are the ones the §7.4 council review is asked to test first.

## D1 — Q7 is the mechanism, and it is cited as ruled rather than chosen

**Decision.** Attestation signatures happen by **remote signing served by the
harness controller**, with the runner's signing **request recorded alongside the
signature** it received. This is not a design choice made here; it is **Q7 as
ruled by Brett Heap on 2026-08-29, AS RECOMMENDED**, and the staged topic records
the gate it opened in terms: *"this gated TRANCHE TWO's contract text, which may
now name the mechanism. The gate is OPEN."*

**Why the packet names it rather than describing a family of acceptable
mechanisms.** Three mechanisms are consistent with `access_secrets: false` — a
remote signing call the controller serves, a co-process holding the key behind an
attested boundary, and a hardware-backed signer — and the topic's own explanation
says they *"differ in exactly what an attacker who owns a runner for one task can
obtain."* A contract that admitted all three would be a contract that could not
say what an attestation proves. The ruling picked one, so the contract states one.

**What the recorded request buys — and what it does NOT, corrected by the first
bot round.** A signature shows WHAT was attested; it does not show WHO ASKED, so
the request is REQUIRED rather than recommended and its absence REFUSES rather
than degrading the record — the same shape as tranche one's missing-proof
refusal. **But this section first claimed that recording the request lets the
controller tell a provisioned task from an opportunistic caller, and that was
false.** Recording establishes that SOMETHING asked; it establishes nothing about
WHAT. A caller that can reach the signing service can submit a payload that
corroborates against link 4 and receive a signature indistinguishable from the
provisioned task's — every stated refusal satisfied. The repair is in requirement
2: the controller **ATTRIBUTES** the request to the task it provisioned, refuses
what it cannot attribute, and covers requester, chain identity and payload digest
INSIDE the bytes it signs. **The claim is corrected here rather than quietly
deleted**, because it is the family's own "a reference is not a binding" defect
arriving one link later: a record that NAMES the asker is not a record that
ESTABLISHES the asker.

**And the repair's own residual is declared rather than assumed away.** The
obvious mechanism — a per-task request credential the runner holds — is
unavailable, because `access_secrets: false` forbids putting one in a worker, and
that is the same constraint that forced remote signing in the first place. So the
requirement states WHAT MUST BE ESTABLISHED and not the mechanism, and obliges a
realization to DECLARE what its platform actually lets the controller establish.
A platform that cannot tell two tasks of the same controller apart is conformant
if it says so and refuses the uses that need the distinction; it is
non-conformant if it stays silent.

## D2 — The controller corroborates; it does not notarize — and the evidence class is PER FACT

**Decision.** The controller corroborates a submitted payload against its own
link-4 setup attestation before signing, refuses to sign a claim about something
it provisioned that it cannot match, and every attested fact carries an EVIDENCE
CLASS — `controller_corroborated`, `independently_observed`, or `runner_claimed`.
**An unclassed fact is refused.**

**Why this is a separate requirement from D1's mechanism, and not a clause inside
it.** Q7 settles WHERE THE KEY LIVES. It settles nothing about whether the claims
are checked — the topic says so directly: *"the mechanism question is about WHERE
the key lives, never about whether the claims are checked."* A packet that
encoded the ruling and stopped would have a chain in which a compromised runner
submits a false model/version/harness payload and links 5, 6 and 10 all still
chain. That is the fabricated-but-valid-looking record this family exists to
refuse, and it would have arrived *through the ruled mechanism*.

**Why the class is per FACT rather than per ATTESTATION — this packet's own
decision.** The topic requires that runner-only measurements be *"carried
explicitly as runner-claimed, never laundered into controller-attested fact"*,
and does not say where the label lives. A per-ATTESTATION label fails on the
ordinary case: a single link-5 record carries both corroborated facts (the model
the controller provisioned) and runner-only ones (a local measurement), so one
label for the record either downgrades the corroborated facts or launders the
claimed ones. **The unit of the claim is the fact, so the unit of the class is
the fact.** The refusal of an UNCLASSED fact follows tranche one's untagged-digest
rule: a marker that may be omitted will be, and an unclassed fact is read at the
strength of the strongest fact beside it.

**AND THE SET IS COMPOSED WITH THE RATIFIED CUSTODY LADDER RATHER THAN LEFT
BESIDE IT — the council's LA-A3, discharged here.** The estate already owns a
ratified, CLOSED assurance vocabulary on a neighbouring axis:
`contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml`, ratified by
`add-trust-anchor` (Brett Heap, 2026-08-21, OQ2) and realized at
`contract-v1.37`. It ranks `assurance_levels` 0/1/2, DERIVES `evidences` from two
booleans, forbids independent assertion, and carries a `composes_with` block
naming openxwallet's registry *"so the two sets cannot drift into two custody
models."* The first draft of this packet minted a three-member class beside it
and named the registry nowhere.

**The axes are DISTINCT, and this packet says which is which rather than
implying it.** The registry classes WHOSE ACT A SIGNATURE EVIDENCES — a property
of the certificate's custody. This set classes WHERE A FACT INSIDE THE SIGNED
PAYLOAD CAME FROM — a property of the claim, not of the key. They are therefore
composed rather than merged, on the registry's own pattern: an explicit
composition statement in requirement 3, a declared reading ORDER (the signing
certificate's custody ceiling BOUNDS what any fact under it evidences, so no
evidence class raises a fact above it), and a declared ORDERING WITHIN this set —
**`runner_claimed` < `controller_corroborated` < `independently_observed`**, on
one discriminator: how many parties independent of the claimant established the
fact. The strength sentence above ("read at the strength of the strongest fact
beside it") is a comparison, and a comparison over an undeclared order is not a
rule.

**AND THE THIRD MEMBER IS RENAMED, BECAUSE THE REGISTRY EXCLUDES WHAT IT WAS
CALLED.** The first draft named it `hardware_attested`. That registry's
`excluded_models` refuses `asserted_hardware_backing` BY NAME and gives the
reason: *"the family's own live canary runs certificates whose keys are
hardware-resident and usable by the host without limit, and those evidence the
HOST … where the key physically lives is a fact about blast radius that belongs
in `notes`, never a tier."* A member called `hardware_attested` would have
re-opened on this axis exactly the hole that ruling closed on the other. The
property the class actually asserts is **INDEPENDENT OBSERVATION** — the
requirement's own first sentence already said so — so the member is named
`independently_observed`, hardware attestation is recorded as ONE MECHANISM that
supplies it, and a hardware mechanism observing nothing independent of the
claimant earns nothing. Of LA-A3's three options — justify, rename, or drop to
two — **rename is taken**, because the property is real and worth a class; it is
only the name that borrowed an excluded discriminator.

## D3 — The gate's extension is a SCENARIO-COMPLETE MODIFIED restatement, and the earlier ADDED-only reading is recorded as WRONG

**Decision, as amended by the §7.4 council review of 2026-08-30.** This packet
carries a `## MODIFIED Requirements` block over tranche one's gate requirement
*"A gate validates the short chain as a hash-linked chain"*, **SCENARIO-COMPLETE
AT ALL NINE OF ITS SCENARIOS**. The gate's re-scoping and the amendment of the
`a tranche-two link does not exist yet` scenario happen WHERE THAT REQUIREMENT
LIVES. The ADDED requirement 6 still carries the extended walk; what it no longer
does is try to repeal a scenario in a different requirement by describing it.

**THE EARLIER READING WAS WRONG, AND IT IS RECORDED AS WRONG RATHER THAN
REPLACED QUIETLY.** This section previously decided that NO MODIFIED block was
needed, on the ground that tranche one's scope note is SELF-LIMITING — *"at this
tranche"*, *"a later tranche's link"*, *"a link that does not exist yet"*, and a
scenario heading naming its own expiry — and therefore SPENT once tranche two's
links exist. The reasoning about the SENTENCE was right. **The conclusion about
the SCENARIO was not, and the difference is the whole finding.** A scope note
that self-limits still leaves a normative SCENARIO standing in canon, and **prose
in one requirement cannot repeal a scenario in another.**

**IT WAS PROVED BY CONSTRUCTION, NOT ARGUED.** `lead-architect` copied the
repository's `openspec/`, dropped both deltas beside each other and ran the
estate's own promotion tool twice — tranche one, then this packet — and read the
canon they actually produce. It composed MECHANICALLY (18 requirements, 104
scenarios, `openspec` reporting `~ 0` modified, no collision, no error) and NOT
SEMANTICALLY:

```
promoted canon :552   #### Scenario: a tranche-two link does not exist yet
                      WHEN the gate walks a chain that carries no attestation link
                      THEN it validates links 1–3 and returns a verdict scoped to them
                      AND the absent later link is not reported as a break

promoted canon :1141  #### Scenario: a chain carrying links 1–3 only reaches the
                      gate after this tranche is in force
                      WHEN a chain presents the ratification, the inception and the
                      traveling contract and no attestation links at all
                      THEN the gate REFUSES to permit the terminal act
```

**Same antecedent. Opposite consequent. Both normative. Both promoted.** The
archive line `~ 0` is itself the proof that nothing was modified to reconcile
them, and no validator in the estate notices, because each delta is independently
valid. That is the sitting's decisive finding and this block is its repair.

**AND THE CLOSED-LIST CLAUSE FELL OUT OF THE SAME CONSTRUCTION — LA-A2.**
Tranche one's gate requirement carries *"**THE LIST IS CLOSED** … every
requirement of **this capability** is either walked here or has its enforcement
point named below"* — scoped to the CAPABILITY, not to the tranche — above a
mapping table of NINE rows. After promotion "this capability" numbers EIGHTEEN
requirements, so canon would have asserted, in its own words, that this packet's
own nine are *"requirement[s] this capability does not enforce."* The MODIFIED
block takes LA-A2's option (i), the better repair: **the table is extended to all
eighteen**, each new row naming where that requirement is enforced — the extended
walk's link-4/5/6 legs, the controller-time refusals a gate cannot observe, the
closure and consumer horizons after the merge, the execution-time precondition
before it, and the custody rule that is a design obligation and not a per-chain
check. Option (ii) — re-scoping the clause to the links the requirement walks —
was available and is not taken: the table is the reader's index to where each
obligation is enforced, and losing that at eighteen requirements costs more than
at nine.

**WHAT THE MODIFIED BLOCK CHANGES, AND WHAT IT CARRIES VERBATIM.** Substantively
it changes exactly two things — the gate's SCOPE SENTENCE, from "links 1–3 at
this tranche" to the links the ratified tranches have put in force, with the
scope note stated as unavailable for a link now in force; and the SCENARIO, whose
antecedent is re-conditioned on a link NO ratified tranche has yet put in force —
plus LA-A2's table extension. **Everything else is carried verbatim, and all NINE
scenarios are restated**, on the promotion-fidelity lesson of PR #331: a MODIFIED
delta that restates a subset silently drops the rest, invisibly to every count.

**THE FIGURE WAS NINE AND THIS PACKET SAID TWELVE — LQ-A1.** Four sites in the
earlier draft priced the restatement at *"all twelve scenarios"*. `lead-quality`
counted; three seats counted independently; the answer is **NINE**. The figure is
corrected everywhere it appeared, because a restatement briefed at twelve that
lands nine is itself the promotion-fidelity defect it was quoting.

**THE COST THE EARLIER READING NAMED IS REAL AND IS ACCEPTED RATHER THAN
AVOIDED.** Tranche one is an ACTIVE change: its gate requirement lives in a
sibling's ADDED delta, NOT in `openspec/specs/`, so this MODIFIED block restates
a requirement canon does not yet hold and its correctness depends on ARCHIVE
ORDER — tranche one first, which is the order the verifier above runs and the
only order in which this capability exists to be modified. That is the
promotion-order hazard the repository is governing in its own right (issue
**#502**, and `govern-sibling-added-modified-deltas`, PR #504). The hazard is
recorded here as a known dependency of this packet rather than as a reason to
keep prose where a delta belongs.

## D4 — Plural predecessors: the topic's hash-link rule is singular and link 5 is not

**Decision.** Where a link admits several records, its successor commits to an
ORDERED, DEDUPLICATED ENUMERATION of ALL of them, digested under the one
construction already in force, and a successor committing to a PROPER SUBSET is
REFUSED. **A dropped attestation is a break, never a shorter chain.**

**This fills a gap in the topic rather than departing from it**, and it is
flagged as this packet's own resolution so a reviewer can disagree. The topic's
binding rule reads *"the digest of the link that precedes it"* — singular — while
its own link table gives link 5 *"each runner attests"* — plural. With several
link-5 records, "the predecessor" has no referent for link 6, and any
implementation must pick one. Two of the three available pickings are holes: the
FIRST or the LAST attestation lets a lane drop every other one and still present
a continuous chain; a SET WITHOUT AN ORDER makes two verifiers derive different
digests over the same records, which tranche one's one-construction requirement
already refuses.

**Why this matters more than it looks.** It is the mix-and-match attack arriving
through a different door. The topic's review round raised assembly from DIFFERENT
executions; this is subtraction WITHIN one execution — the disfavoured runner's
attestation quietly absent — and the continuity check as tranche one states it
would not catch it, because what remains is genuinely continuous.

**AND THE FIRST FORM OF THIS RULE WAS UNENFORCEABLE, WHICH THE FIRST BOT ROUND
CAUGHT.** It said the gate refuses "a proper subset" and gave the gate nothing to
take the subset OF. A gate reading only the artifacts handed to it has no
authoritative set: a lane that omits an unwanted link-5 record BEFORE presenting
link 6 leaves an enumeration that is ordered, deduplicated and complete over
everything visible — so the rule as written passed exactly the chain it was
written to refuse. **The set is now DERIVED BY THE GATE FROM THE LOG** by a
defined query (every link-5 leaf committing to this chain identity, at or before
the successor's own leaf), and the enumeration must be EQUAL to it — not a subset
and not a superset, since a record enumerated but never written as a leaf is
UNPROVEN under tranche one's own rule.

**AND THE "WHY THE LOG AND NOT LINK 4" REASONING WAS WRONG — CORRECTED, NOT
DELETED.** This section previously rejected the other candidate outright:
*"Declaring the expected task set in the setup attestation was the other
candidate and is worse: link 4 is signed BEFORE the runners execute, so a
dynamically fanned-out task set is not knowable at that point, and a rule
requiring it would be unbuildable for the ordinary case."* **The buildability
objection was real. The conclusion drawn from it was not**, and the difference
cost the packet the whole attack.

**A LOG-DERIVED SET CANNOT SEE A LEAF THAT WAS NEVER WRITTEN.** The query is
*"every leaf … at or before the successor's own leaf"*, so a lane that never
writes an unwanted attestation — rather than omitting it from the submission —
produces an enumeration EQUAL to the derived set, and the gate PERMITS. The
leaf-ordering obligation (LQ-A3) does not repair it: refusing the late leaf when
it eventually appears lands after a merge this capability's own two-horizon
doctrine says is not retroactively refused, and a leaf never written never
appears at all. **`lead-security` had already named the missing instrument in
these words** (LS-F5, §1.6): *"link 4 records the provisioned environment but no
count of expected runner tasks, so there is no independent cardinality to check
equality against. Suppression at source is undetected."* The second bot round
reached the same place independently. **Two independent readers finding one hole
is the finding.**

**THE DECISION IS THEREFORE REVERSED: THE AUTHORITATIVE SET IS LINK 4'S COMMITTED
EXPECTATION.** The controller — the party that dispatches, and the only party
trusted at that boundary — commits the expected attestation set inside the bytes
it signs, and the gate compares link 6's enumeration for EQUALITY against that,
never against leaves already present. This is **BIND BEFORE SIGN's sibling one
link earlier**: at link 5 the controller refuses to sign a claim it cannot
corroborate; at link 4 it states, before any runner executes, what claims are
owed. A completeness rule whose expectation is inferred from the side that
benefits from shrinking it is satisfiable by writing less.

**AND THE BUILDABILITY OBJECTION IS ANSWERED RATHER THAN OVERRIDDEN**, because a
rule describing a control that cannot run is the failure this family has now
named several times. Where the task set is not knowable at link-4 signing time,
the commitment is EXTENDED by a controller-signed extension record written as a
leaf BEFORE the attestation it covers. The expected set is link 4 AS EXTENDED.
Three refusals stop the extension becoming the hole: an extension written after
the attestation it covers is refused; an attestation for a task no commitment
covers is refused; and an extension signed anywhere but at the controller is
refused. **Dynamic fan-out is served by extension and never by silence.**

**Why not simply oblige the controller to write every link-5 leaf**, which was
the third candidate. It fixes WHO WRITES and still fixes no EXPECTATION: a
controller that writes every leaf it is asked to write still has no independent
statement of how many were owed, so the same lane omits the request rather than
the leaf. Committing the expectation is strictly stronger and subsumes it.

**Two residuals, both declared.** A store truncating its newest unobserved leaves
could hide a link-5 leaf — tranche one's suffix truncation, inherited and not
re-declared, with tranche-three anchoring named as what closes it. And a
COMPROMISED CONTROLLER can under-commit: dispatch a task and never name it. That
one is not a gap this rule opens but **the trust boundary the tier split already
draws** — the controller's signature is the root of every fact link 5 carries in
any case — so the requirement claims detection against a lane, a runner or a
store and says so in terms.

## D5 — An HSM is deferred hardening, and the contract is written so that adopting one changes nothing

**Decision.** No hardware security module is specified, procured or required. The
requirement text says an HSM is a LATER HARDENING OF THE SAME SHAPE and carries a
scenario asserting that adopting one leaves every record the chain carries
unchanged.

**Why deferral is safe here specifically**, rather than the usual reason. Q7's
ruling says it in terms: *"An HSM remains a later HARDENING of the same shape, not
a different answer, so adopting one moves where the key sits and changes nothing
about what the chain carries."* Because the ruled mechanism is REMOTE SIGNING AT
THE CONTROLLER, the runner's side of the boundary is identical either way — it
submits a payload and receives a signature. **The HSM decision is entirely behind
the boundary the contract describes**, which is what makes deferring it a
hardening question rather than a contract question. Writing an HSM requirement now
would specify a procurement in a document that governs a record format.

## D6 — Revocation AFTER signing: this packet's own horizon decision, not a ruling

**Decision.** A controller certificate REVOKED AT SIGNING makes its attestation
refused outright. A certificate revoked AFTER a signature was made does NOT
retroactively unmake an act the gate already permitted; it refuses everything the
chain has not yet been permitted for.

**Flagged as a decision because it is one.** `add-trust-anchor` ratifies that
revocation standing is *"checked at USE rather than trusted from issuance"* and
that revoking an anchor revokes transitively what its subordinates supported. It
does not say what "use" means for an artifact signed at one moment and read at
another, and a chain has exactly that shape.

**Why this reading rather than a stricter one.** The strict alternative — a later
revocation refuses chains already permitted — is unbuildable against the same
horizon rule link 10's closure requirement states: *a merge that already happened
cannot be retroactively refused.* A rule that refuses a merged chain retroactively
would be describing a control that cannot run, which is the failure this family
has now named several times. The reading adopted keeps revocation SHARP where it
can act (nothing further is permitted) and HONEST where it cannot (the merge
stands, and what it forfeits is downstream).

**What it costs, stated rather than hidden.** A controller compromised and
revoked after a merge leaves that merge in place. What the family gets instead is
that the chain is unclosable-in-good-faith from that point, its downstream is
refused, and the remediation route is the one door open — which is the same
posture as a failed link 10.

## D7 — Q4's re-derivation instruction, and what this packet does about it

**Decision.** The packet is raised now, and it says out loud that Q4's
instruction is an objection to its own existence, puts it first in the proposal,
and routes it to the council rather than answering it.

Q4 ruled that later boundaries are *"RE-DERIVED when the omnigent layer and the
PKI plane are real, not fixed now — a boundary drawn against an unbuilt layer is
a guess wearing a tranche number."* Neither plane is real: `implement-openxpki-install-repo`
is ACTIVE at 22/30, and the omnigent family is contracts and overlays with no
runtime enforcing a chain precondition.

**The packet's argument, offered and not ruled.** A boundary is a guess when it
is drawn against an unbuilt layer's SHAPE. This one is drawn against ratified
neutral vocabulary that already exists — `trust-anchor`'s anchor records, recorded
issuance authority, declared custody and revocation-at-use; `identity-brokering`'s
workloads-are-not-personas refusal; omnigent's already-closed permission matrix —
and it names NO interface either plane must expose. The delta describes what a
record must establish, never the API that produces it, which is the same
technique `add-trust-anchor` used to stay conformant against a certificate
authority the family does not operate.

**And the re-derivation survives ratification rather than being discharged by
it**: `tasks.md` §5.1 makes re-deriving the boundary against what actually exists
an obligation OF THE REALIZATION, not a box this packet ticks.

**The literal reading is available and is not dismissed.** A seat may read Q4 as
forbidding the drafting of tranche two until both planes are real. That reading
is on the text, this packet cannot rule it out, and the council is where it goes.

## D7a — THE RAISING-TIME RE-DERIVATION, PERFORMED — 2026-08-30

**This section is an ACT OF AUTHORSHIP AND NOT A RE-RULING OF Q4.** Q4 stands
exactly as Brett Heap ruled it. What is performed here is the obligation tranche
one's own ratified task list places on the raising of a successor, which the
§7.4 sitting of 2026-08-30 ruled BLOCKING (`lead-architect`'s LA-A5, adopted as
decision 1's narrowing: *"NOT PREMATURE BUT NARROWED"*).

**(i) THE TRIGGER, CITED BY PATH AND TEXT.**
`openspec/changes/add-signed-execution-chain/tasks.md:187` — task **5.3**,
ratified 2026-08-29:

> *"Neither successor's content enters this packet. **Re-derive the tranche
> two/three boundary against what actually exists when each is raised**, per the
> topic's Q4 — a tranche that depends on an unbuilt layer is a plan, not a
> tranche."*

**"When each is raised" is NOW.** This packet is the raising of tranche two, so
the re-derivation is due at this document and not only at its realization. The
earlier draft carried the obligation forward to `tasks.md:5.1` alone, which is
the REALIZATION-time re-derivation, and a forward carry is not a discharge of a
trigger that has already fired.

**(ii) WHAT ACTUALLY EXISTS, MEASURED AT THIS BRANCH ON 2026-08-30.**

| Plane | State today | Measured how |
| --- | --- | --- |
| **The PKI plane** | `implement-openxpki-install-repo` is ACTIVE at **22/30 tasks**. **NO certificate authority is operated** by this family or by anyone on its behalf: the change creates the install repository, and openxFactory owns neither the CA nor its issuance pipeline | task-box count in that change's `tasks.md` |
| **The omnigent layer** | Contracts and overlays only — `contracts/omnigent/omnigent-domain-overlay.schema.yaml` and `omnigent-install-manifest.schema.yaml`, with per-domain overlays. **NO runtime enforces a chain precondition**; nothing in `installs/` reaches the omnigent family at all | file inventory of `contracts/omnigent/`; `grep -rl omnigent installs/` returns nothing |
| **The identity plane** | `add-identity-brokering` is ACTIVE at **20/30**. Its ratified *"workloads are not personas"* refusal — which is all this packet consumes from it — is TEXT and is available now | task-box count |
| **The instruments this packet actually binds to** | `add-trust-anchor` RATIFIED and REALIZED at `contract-v1.37`, including the chain-custody registry; `add-wallet-carried-review-authority`'s S2 issuer anchor REALIZED and read inside the REQUIRED `wallet-validation` check; tranche one RATIFIED 2026-08-29; the omnigent permission matrix SHIPPED and closed since `contract-v1.16` | contract manifest and the changes' own evidence |

**(iii) THE BOUNDARY DERIVED FROM THAT STATE — links 4–6 and 10 REMAIN tranche
two's set, and NO LINK MOVES.** The derivation, link by link, against what exists
rather than against what is planned:

- **Link 4** stays. Its content is a RECORD SHAPE expressed entirely in
  `add-trust-anchor`'s ratified vocabulary — anchor record, recorded issuance
  authority, declared custody, revocation at use — all of which exist and are
  realized. What does not exist is the CA that would issue the certificate, and
  that is a REALIZATION dependency this packet already names as hard and does not
  assume. A record shape drawn against a realized contract is not a guess wearing
  a tranche number; a record shape drawn against an unbuilt CA's API would be,
  and this packet names no such API.
- **Links 5 and 6** stay, and are the least dependent of all: their mechanism is
  Q7 AS RULED, their custody rule descends from a SHIPPED closed matrix, and
  their signer-identity refusal is ratified text. Nothing in either waits on a
  plane.
- **Link 10** stays, and the raising-time evidence STRENGTHENS its case rather
  than weakening it: closure binds to `add-wallet-carried-review-authority`,
  whose issuer anchor is realized and read inside a required check TODAY. Link
  10 is the tranche's most-realized dependency, not its least.
- **Requirement 9, the omnigent precondition, is the ONE that a literal reading
  of Q4 reaches** — it is a refusal a RUNNING LAYER performs and no such layer
  exists. **It is not moved out of the tranche, and the reason is stated:** it
  writes no interface the unbuilt runtime must expose, adds no archetype and no
  permission boolean, and is declared UNMET rather than partially met until a
  running layer refuses (`tasks.md:5.3`, and D9). Moving it would separate the
  precondition from the links it is a precondition ON, and would buy nothing the
  UNMET declaration does not already buy honestly.
- **Nothing is moved IN from tranche three.** Anchoring, commitments, receipts
  and the consent plane all depend on the PKI plane in a way these links do not,
  and they stay in `add-chain-anchoring`.

**The re-derivation therefore CONFIRMS the boundary rather than redrawing it, and
the confirmation is worth more than the answer** — it is on the record as
performed at the raising, with its inputs measured and dated, so a later reader
can check the derivation rather than take the conclusion.

**(iv) `tasks.md:5.1` IS THE SECOND RE-DERIVATION AND IS NOT DISCHARGED BY THIS
ONE.** Task 5.3 fires at the RAISING (here, discharged above). Task 5.1 fires at
the REALIZATION, when the planes are real, and asks a question this document
cannot answer: whether the boundary still holds against layers that then exist in
fact rather than in contract. Two triggers, two moments, two artifacts. **Neither
substitutes for the other**, and 5.1 is made decidable in its own right — see the
task, which now names the observable and the artifact.

## D8 — What stays out, and where each lands

| Kept out | Why it cannot land here | Where it lands |
| --- | --- | --- |
| **The on-chain anchoring and consent layer** — the salted keyed commitment, the chain-agnostic multi-anchor receipt, the permissioned consent plane | Tranche three's whole subject, ruled by Q2/Q3/Q6 and gated on the PKI plane being real. This delta names no chain, no witness, no anchor, no commitment and no receipt format | The sibling change **`add-chain-anchoring`**, in parallel drafting |
| **The certificate authority itself** | `implement-openxpki-install-repo` owns the runtime CA and its ratified boundary keeps openxFactory the owner of the neutral contract and the realizer of neither | That change, and the install repository it creates |
| **Link 7's council-seat signatures as a WALKED link** | Tranche one placed link 7 on the §7.4 path in short-chain form and left its seat signatures outside the gate's scope; extending the walk to them is a separate act with its own convening consequences | A later tranche or a successor change. **Closure does NOT merely bind to the review record's bytes** — that would let a fabricated record close a chain, which the first bot round caught: a digest proves the bytes did not change after signing and says nothing about who produced them. Link 10 now establishes that the review record was produced under REVIEW AUTHORITY PROVEN BY POSSESSION, in `add-wallet-carried-review-authority`'s shipped vocabulary. What that does NOT establish — that every seat signed — is DECLARED, with a walked link-7 check named as what closes it |
| **An HSM** | Deferred hardening behind the boundary the contract describes — see D5 | A realization decision, requiring no contract change |
| **Domain realizations (HealthLinc, LedgerLinc)** | They belong to MedxFactory and LedgerxFactory; openxFactory owns the neutral family | Domain repositories, consuming the released bundle |
| **A second digest construction** | Tranche one puts ONE in force for every digest this capability computes, including those a later tranche adds, and says so in its own scenario | Nowhere — it is refused, and requirement 6 carries the refusal |

## D9 — This packet RATIFIES-NOT-REALIZES, and the dependencies are named as hard

**Decision.** Ratification, if it comes, authorizes ONE contract feature plus the
extension of an existing gate. It performs no realization, creates no certificate
authority, mints no attestation identity, and deploys nothing.

**The two dependencies are hard and are stated as hard**, on the precedent
`add-binding-consumer-identity` set on 2026-08-29 — ratification authorizes
REALIZATION and does not perform it, and the change stays ACTIVE until merged
code, green evidence and the contract cut exist:

- **The omnigent layer must be real enough to enforce a precondition.** Requirement
  9 is a refusal a running layer performs. Until such a layer exists, the
  requirement is UNMET rather than partially met — tranche one's named-reader rule
  applies to this delta too, by composition, and this packet claims no enforcement
  it cannot name a check for.
- **`implement-openxpki-install-repo` must be real enough to issue a controller
  certificate.** Requirement 1's certificate is a `trust-anchor` shape and the
  authority that issues it is not this repository's.

**Neither dependency is softened by this packet's ratification**, and neither is
assumed by its requirement text.

## D10 — What the first bot round corrected, recorded as corrections

Three P1 findings on this packet's own pull request, all real, and **all of one
shape: a record that NAMES something was standing where a record that ESTABLISHES
it belonged.** Recorded here rather than silently patched, because the shape is
the transferable part — it is the same defect tranche one met as *"a reference is
not a binding"*, arriving three separate times at three different links.

1. **The signing request was recorded and not attributed** (requirement 2). An
   opportunistic caller reaching the signing service could submit a payload that
   corroborates against link 4 and receive a signature indistinguishable from the
   provisioned task's, satisfying every stated refusal — and D1 had explicitly
   CLAIMED the record closed that case. Repaired by requiring ATTRIBUTION to the
   provisioned task, refusal where it cannot be established, and coverage inside
   the signed bytes; with the residual declared, because `access_secrets: false`
   forbids the obvious mechanism.
2. **"A proper subset" named nothing** (requirement 6). The gate had no
   authoritative set to take the subset OF, so a lane omitting an unwanted link-5
   record before presenting link 6 produced an enumeration that was complete over
   everything visible — the rule passed the exact chain it was written to refuse.
   Repaired by DERIVING the complete set from the transparency log by a defined
   query and requiring EQUALITY, with tranche one's suffix-truncation residual
   inherited rather than re-declared.
3. **Closure bound to review-record BYTES and not to review AUTHORITY**
   (requirement 7). A digest establishes only that the bytes did not change after
   the controller signed them, so a supplied or fabricated review record could be
   consumed by a passing test and CLOSE THE CHAIN — at the one link with no gate
   behind it. Repaired by requiring the review record to be established under
   review authority PROVEN BY POSSESSION in the shipped
   `add-wallet-carried-review-authority` vocabulary, with the per-seat residual
   declared and a walked link-7 check named as what closes it.

**None of the three was repaired by inventing vocabulary.** The attribution is
stated as what must be ESTABLISHED, the complete set comes from the log tranche
one already makes the record, and the review authority is the instrument this
repository already reads inside a required check.

## D11 — What the SECOND bot round corrected, recorded as corrections

Two P1 findings on the council fix round's own head (`b7bc4f1f`), both real, and
**both of one shape — a rule that could not be CONSTRUCTED as written.** Recorded
here on D10's pattern, because the shape is the transferable part and it is a
different shape from D10's: D10's three were records that NAMED where a record
that ESTABLISHES belonged; these two are rules that, executed literally, either
detect nothing or forbid the very artifact the capability requires.

1. **The completeness rule could not see the attack it was written for**
   (requirements 1 and 6). The authoritative set was DERIVED FROM THE LOG, so a
   lane that never wrote an unwanted link-5 leaf produced an enumeration equal to
   the derived set and passed the gate; the ordering obligation could only refuse
   the leaf once it appeared, which is after a merge that is not retroactively
   refused. **Repaired by moving the authority to link 4's COMMITTED EXPECTATION**
   — the controller commits the dispatched task set inside the bytes it signs,
   extensible before each attestation it covers, with the log comparison retained
   as a second check in both directions. Full reasoning at D4. **`lead-security`'s
   LS-F5 had named the same missing instrument**, so this discharges a seat
   finding as well as a bot one.
2. **No conforming link 6 was constructible** (requirements 2, 5 and 7).
   Requirement 2 bounded the per-task tier-2 identity to *"exactly one thing —
   signing an attestation about that task"*, while requirements 5 and 7 required
   that same identity to sign a DECISION and a TEST OUTCOME. A realization
   enforcing the first could not produce the second: **two requirements of one
   capability demanding opposite things, with every realization forced to breach
   one.** Repaired by **WIDENING TO A CLOSED, NAMED ENUMERATION** of the identity's
   authorized record kinds — task attestation (link 5), PR-open decision record
   (link 6), post-merge test record (link 10) — rather than by minting SEPARATE
   task-scoped identities, which was the other option offered.

**Why widening and not separate identities.** Separate identities would have
multiplied the per-task credential population by three for no gain in what any
signature proves: all three records are produced at the same signing boundary,
under the same custody rule, about the same task, and the property that matters
— *this identity can say things about its task and can permit nothing* — is
carried by the ENUMERATION being closed, not by how many identities carry it.
Three identities with the same authority are one authority with more bookkeeping,
and each additional per-task credential is another thing a realization must mint,
scope and destroy.

**What closing the enumeration buys, and why it is stated as a permanent
exclusion.** The risk in widening a signer's authority is that the next widening
happens quietly. So the enumeration is CLOSED, and AUTHORITY RECORDS — a
ratification, an approval, a review grant, anything that CONFERS PERMISSION —
are excluded from it FOREVER rather than merely absent from it today. **Tier 2
answers *what ran*; tier 1 answers *who permitted*.** The exclusion is what keeps
a fourth record kind, added later for convenience, from moving an act across that
line; and it is the same discipline requirement 5 already states when it says
signing an open is not permitting a merge.

## What this design does NOT decide

Named so the review has the list rather than reconstructing it, and so none of
these reaches schema authoring open:

1. **The record home for the signing request.** Whether the runner's signing
   request is a field on the link-5 attestation or a sibling record it references.
   The requirement fixes that it is RECORDED ALONGSIDE the signature and refuses
   its absence; it does not fix the shape.
2. **The evidence-class vocabulary's closure.** Three classes are named
   (`controller_corroborated`, `independently_observed`, `runner_claimed`), and
   D2 now fixes their ORDER and their COMPOSITION with
   `contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml`. What stays
   open is only CLOSURE: whether the set is CLOSED at the schema, and what a
   fourth would have to establish to be admitted. **That registry is the named
   INPUT to the closure decision** — its `excluded_models` reasoning is the
   worked example of what admitting a member on the wrong discriminator costs,
   and a fourth class is judged against it rather than against intuition.
3. **What a setup attestation must enumerate.** The requirement fixes that link 4
   records what the controller PROVISIONED and refuses an attestation recording
   nothing; the enumeration itself — how a model surface, a harness version and a
   workspace provenance are each expressed — is contract content.
4. **The ordering rule for the plural-predecessor enumeration.** D4 fixes that it
   is ORDERED and DEDUPLICATED; the ordering key is a serialization decision under
   tranche one's single construction and is settled with it.
5. **Whether the extended gate is one check or two.** The packet says the SAME
   required check walks further. Whether a realization finds it operationally
   necessary to report link-scope separately is an implementation question that
   must not become a second gate.
