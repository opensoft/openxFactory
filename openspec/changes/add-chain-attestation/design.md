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
written to refuse. **That round's repair DERIVED THE SET FROM THE LOG** by a
defined query (every link-5 leaf committing to this chain identity, at or before
the successor's own leaf), requiring the enumeration to be EQUAL to it — not a
subset and not a superset, since a record enumerated but never written as a leaf
is UNPROVEN under tranche one's own rule. **THAT REPAIR IS SUPERSEDED and the
paragraphs below say why: a log query cannot see a leaf that was never written,
so the authority is now LINK 4's COMMITTED EXPECTATION and the log comparison is
a SECONDARY check.** The equality discipline and the UNPROVEN rule survive the
change of authority; only the source of the set moved.

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
   Repaired **at that round** by DERIVING the complete set from the transparency
   log by a defined query and requiring EQUALITY, with tranche one's
   suffix-truncation residual inherited rather than re-declared. **That repair is
   SUPERSEDED — see D11 and D4:** a log query cannot see a leaf that was never
   written, so the authoritative set is now link 4's COMMITTED EXPECTATION and the
   log comparison is secondary.
3. **Closure bound to review-record BYTES and not to review AUTHORITY**
   (requirement 7). A digest establishes only that the bytes did not change after
   the controller signed them, so a supplied or fabricated review record could be
   consumed by a passing test and CLOSE THE CHAIN — at the one link with no gate
   behind it. Repaired by requiring the review record to be established under
   review authority PROVEN BY POSSESSION in the shipped
   `add-wallet-carried-review-authority` vocabulary, with the per-seat residual
   declared and a walked link-7 check named as what closes it.

**None of the three was repaired by inventing vocabulary.** The attribution is
stated as what must be ESTABLISHED, that round's complete set came from the log
tranche one already makes the record, and the review authority is the instrument
this repository already reads inside a required check.

**FINDING 2's REPAIR DID NOT HOLD, AND D11 RECORDS WHAT REPLACED IT.** Deriving
the set from the log closed omission from the SUBMISSION and left omission from
the LOG open, which the second bot round and `lead-security`'s LS-F5 both reached
independently. The authority is now link 4's COMMITTED EXPECTATION; the log
comparison is retained as a secondary check in both directions. **This entry is
kept as the record of what round one did**, not as a statement of the rule in
force.

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

### D12 — the lineage fields' home: a second MODIFIED on tranche one, and why that is lawful

**Decision.** The three amendment-lineage fields live on **tranche one's
ratification/chain-inception record**, added by a **second scenario-complete
`## MODIFIED` requirement** in this packet's delta — not in a new record kind of
our own.

**The problem, which is a placement problem and not a design one.** Closure's
lineage limbs require the reviewed digest, the ratified subject digest and the
amendment-record reference to sit INSIDE THE BYTES THE RATIFYING SIGNATURE
COVERS. That signature belongs to an act tranche one owns. So the fields had
nowhere to live: `tasks.md` 5.4 commissioned only this packet's own record kinds,
and `proposal.md`'s `target_release` classified the release as changing no
existing schema. **Both lineage positives were unconstructible as commissioned.**

**Why ROUTE A — extend tranche one's record — is lawful, checked against the
ratified texts rather than assumed:**

1. **TRANCHE ONE IS RATIFIED-NOT-REALIZED. No contract byte exists to break.**
   `contracts/signed-execution-chain/` does not exist and the capability is
   absent from `contracts/manifest.yaml`. The extension therefore changes NO
   SHIPPED SCHEMA; it authors an uncut surface, which is what
   `target_release` now says in terms.
2. **THIS PACKET ALREADY HOLDS EXACTLY THIS INSTRUMENT, BY THE COUNCIL'S OWN
   PRESCRIPTION.** LA-A1 required a scenario-complete MODIFIED restatement of
   tranche one's GATE requirement. The second one follows the identical
   discipline — every scenario restated, none dropped (PR #331's lesson) — so
   this is a precedent applied, not a precedent set.
3. **NO SIBLING DELTA COLLIDES.** Only tranche one and this packet write to
   `signed-execution-chain`; tranche three took a distinct capability precisely
   to avoid the sibling-delta shape (openxFactory issue #502).
4. **THE ARCHIVE-ORDER DEPENDENCY IS THE ONE THIS PACKET ALREADY CARRIES** —
   tranche one archives first — and is not widened by a second MODIFIED block.

**Why not ROUTE B — an eighth record kind of our own.** A RATIFICATION LINEAGE
RECORD signed by the same tier-1 authority in the same act was the alternative,
with duplicates excluded by the log-position rule. It is coherent, and it is
WEAKER for one reason worth recording: **it would put the lineage in a record the
ratifying signature does not cover**, and this capability's own standing rule is
that an assertion attachable afterwards is an assertion anyone can attach. It
would also have minted an eighth record kind to carry three fields belonging to
an act we do not own — and the packet has now twice learned that adding a kind is
how an enumeration gets outrun. **Route B is recorded as considered and ruled
against**, not omitted.

**What the extension does NOT do.** It moves no contract byte, mints no record
kind, changes no shipped schema, and touches nothing about tranche one that this
capability was not already extending. Its scenario set is tranche one's six,
carried verbatim, plus two for the lineage itself.

## D11a — the THIRD round: the same conflict one level up, in SUBJECT rather than FORM

**The widening above fixed FORM and left SUBJECT unfixed, and a third bot round
caught it.** Link 6 is ONE decision committing to EVERY link-5 attestation for
the work it proposes; link 10 is ONE test outcome over that same whole. A signer
valid for one task and authorized only for records ABOUT that task therefore
still could not produce either **the moment a chain fans out to more than one
task** — whichever task's identity signed, the record would cover work from the
others. **The ordinary dynamic-fan-out case had no conforming link 6 through two
successive repairs**, which is the finding worth keeping: the first repair made
the record kinds legal and left the subject scope illegal, and the second reader
had to look one level up to see it.

**Decision: TIER 2 SPLITS BY SUBJECT SCOPE.** The controller issues, alongside
the per-task identities, exactly ONE **CHAIN-SCOPED tier-2 identity** per chain.
The enumerations split with it — per-task shrinks to the task attestation (link
5) alone; chain-scoped carries the aggregate records (link 6, link 10). Both are
tier 2, both are ephemeral, both keep the key at the controller's signing
boundary, and `access_secrets: false` is untouched: **adding a SUBJECT SCOPE
moves no key and widens no permission.** Authority records stay outside BOTH
enumerations forever, so the chain-scoped identity is broader in SUBJECT and not
in AUTHORITY.

**The alternative was refused on the ratified table.** Defining how several
task-scoped decisions COMPOSE into links 6 and 10 was the other option offered.
The staged topic's authoritative link table gives link 6 ONE signed decision —
*"opening a pull request is itself a decision and is signed as one"* — and a rule
assembling one link out of N signatures would invent a link this family does not
have, then owe an ordering and a completeness rule for the assembly. That is a
second plural-predecessor problem bought to avoid a second identity.

**What it departs from, flagged so a reviewer can disagree.** The topic's link
table names a *"per-task identity (controller-signed)"* as the signer for links 6
and 10. **This packet departs from that**, on the same footing D4 departs from
the topic's SINGULAR hash-link rule beside its PLURAL link 5 — the table's own
row 6 calls the PR-open one decision, so the table is internally in tension and
this delta resolves it toward the row rather than the column. Tranche one's
ratified text characterizes tier 2 as *"ephemeral per-task attestation
identities"* and, in the same sentence, says tier 2 *"is the named tranche-two
boundary and is NOT defined here"*, creating no attestation identity of any kind.
**Defining it is this tranche's act**, and the two operative constraints that
sentence does impose — EPHEMERAL, keys never entering a worker — bind the
chain-scoped identity exactly as they bind the per-task ones. **No seat return is
touched:** every custody passage in the four returns is about KEY MATERIAL
(`lead-security` §1.3's C1–C6 subtraction, LS-A3's reachability), and no return
makes any claim about identity CARDINALITY or record-kind scope.

**And the gate's enforcement mapping was stale in the same round.** The
scenario-complete MODIFIED block still described the gate as carrying a
*"log-derived authoritative set"*, contradicting D4's corrected rule one file
over. A realization following the mapping would have re-opened the
dropped-attestation attack the correction had just closed. **The mapping now
names link 4's committed expectation as THE AUTHORITY and the bidirectional log
comparison as SECONDARY**, and a sweep of the whole packet for every
authority-of-the-set phrase and every predicate-shaped sentence about what the
gate compares found four further sites reading in the superseded present tense —
all corrected, with the round-one narratives kept as history and explicitly
marked superseded. **This is the new-conjunct sweep this estate keeps paying
for**: a correction stated in a new paragraph does not retire the wording that
caused it elsewhere in the packet.

### D11b — the FOURTH round: bind-before-sign's last uncovered limb

**Every other link had moved its CLAIMS to the controller. Link 10 had left its
RESULT with the lane.** The corroboration rule binds a submitted attestation's
fields against link 4 and establishes nothing about whether the post-merge test
RAN, PASSED, or ran against the merged work — so a lane supplying a fabricated
passing outcome on an otherwise valid chain obtained a controller signature over
it, with correct proposal and review bindings, and **CLOSED THE CHAIN**,
unblocking promotion and release. The fabricated-but-valid-looking record this
family exists to refuse, arriving at the one link with no gate behind it, for the
FOURTH time in this packet's life and at the last place it had left to hide.

**Decision.** Link 10 binds, inside the controller-signed bytes: an
**AUTHENTICATED TEST EXECUTION** the controller itself dispatched or observed;
the **EXACT TESTED REVISION**, which must EQUAL the merge commit the chain closed
over; and the **RESULT**. An outcome that is merely runner- or lane-claimed is
REFUSED as closure grounds.

**This is the LS-A10 floor's first live application, and the requirement says so
rather than leaving it to be inferred.** A realization that cannot establish its
test's execution, revision or result **cannot declare its way to a closed chain**:
the declaration would disqualify the chain from closure, and closure is the only
thing this link confers, so the disqualified set would be everything and the
permitted set empty. That is exactly the class the floor was written for — *a
declaration never converts an unmeetable control into a met one* — and naming it
here keeps the two shortfalls this requirement DOES declare (the per-seat
residual; the revocation-at-exercise one) from reading as a pattern that extends
to the outcome.

**It composes with the two horizons rather than straining them, which was the
thing to check.** Nothing here reaches back through the merge. What it refuses is
the CLOSURE — which is the only thing link 10 ever controlled — so a chain whose
outcome is unestablished is MERGED-BUT-UNCLOSED, its downstream refusing and link
9's fraud signal firing, exactly as the horizons paragraph already provides.
`lead-security` endorsed that paragraph as *"the packet at its best"* (B-4) and
this addition uses it rather than qualifying it.

**A FOURTH RECORDED OUTCOME, ADDED DELIBERATELY.** The requirement said *"MISSING,
FAILED AND UNSIGNED ARE THREE OUTCOMES AND ARE RECORDED AS THREE"*; it now records
**FOUR**, adding UNESTABLISHED. An outcome the controller could not establish is a
different fact from a test that ran and failed, and a responder who conflates them
hunts a defect in the work when what is missing is evidence about the test. The
enumeration exists to preserve exactly that distinction, so extending it is using
the paragraph rather than overriding it.

**AND THE FIXTURE FIELD CARRIED A STALE CONJUNCT — the new-conjunct lesson one
field over.** `tasks.md` 5.5 still commissioned *"the positive case of that
identity signing its task's link-6 and link-10 records"*, a per-task identity
signing links 6 and 10, which D11a's closed enumeration makes IMPOSSIBLE and
explicitly refuses. Building it would have forced the validator to accept a
forbidden signature or left the task uncompletable. **The earlier sweep covered
PREDICATES and not FIXTURES**, which is the transferable part: a superseded rule
survives in the examples commissioned against it, not only in the sentences
asserting it. Withdrawn, named as withdrawn, and replaced by the chain-scoped
positive case.

### D11c — the FIFTH round: the split's own residue, in the mechanism and in the clause

**Two findings, and BOTH ARE RESIDUE OF D11a's OWN REPAIR** — which is the thing
worth recording, because it is the third distinct way this packet has learned
that a repair leaves work behind it.

**1. THE SPLIT CREATED A SIGNER THE ATTRIBUTION MECHANISM DID NOT REACH.** The
round-one repair attributes a signing request TO THE TASK THE CONTROLLER
PROVISIONED IN LINK 4 — **task-scoped by construction**. D11a then created a
CHAIN-scoped signer for links 6 and 10, which signs no record about a task, so
that attribution reached NONE of its requests. An opportunistic caller able to
reach the controller could submit a link-6 payload naming a valid chain, the
complete link-5 set and plausible work, satisfy every refusal in requirement 5,
and receive a chain-scoped signature nobody was established as entitled to ask
for. **The repair that made link 6 constructible is what opened it.**

**Discharged by EXTENDING the same mechanism, not by inventing a second one.**
The chain-scoped request is RECORDED beside its signature; the controller
ATTRIBUTES it to **the party the chain's own inception record binds** — the actor
bound to the wallet that signed the ratification, carried with the work by the
traveling contract — and REFUSES a chain-scoped request from any party that
binding does not name; and the attribution falls inside the signed bytes.

**No authority is minted, and that is the point of DERIVING the requester set.**
It is read off what the chain already carries: tranche one's actor-binding
requirement already fixes that the actor's subject carries a wallet attestation
naming the wallet whose key made the exercise, and the gate already walks exactly
that. This adds no vocabulary and no second source of truth — it obliges the
controller to ASK the question the chain already answers before signing on that
chain's behalf. A chain whose inception record binds nobody obtains no
chain-scoped signature, which is the correct fail-closed outcome rather than a
gap. Codex offered two other routes — a controller-dispatched act, and a one-time
binding to the actual PR; the authenticated-request route was taken because it is
the mechanism this capability already has, one link over.

**2. THE MODIFIED BLOCK'S OPERATIVE CLAUSE STILL SAID LINKS 1–3.** LA-A1's
discharge re-scoped the SCOPE-NOTE paragraph, re-conditioned the SCENARIO and
extended the MAPPING TABLE — and left the requirement's **leading normative
SHALL** reading *"a gate that validates links 1–3 before permitting the terminal
act"*, with the generic missing-link scenario still conditioned on *"any of links
1–3"*. Promoted canon would have carried **two conformance readings**, and an
implementation could have kept the short-chain gate while satisfying the leading
clause. **That is the exact defect class LA-A1 was raised to close, surviving
inside LA-A1's own repair.**

**Discharged, and then the whole block was re-read AS A SET** rather than at the
two reported sites — which found three more pieces of the same residue: the
closed-list clause's *"validates EXACTLY these checks"* (the eight checks are the
links 1–3 half, so it now names the links 4–6 legs as part of the same one walk);
*"At this tranche continuity is established by derivation and comparison"* (a
LINK-RANGE fact, not a tranche fact, now stated as "across links 1–3"); and the
completeness sentence, which now says in terms that it is complete over links 1–3
**and over nothing further**.

**THE LESSON, AND IT IS THE THIRD TURN OF THE SAME SCREW.** Round three swept
PREDICATES. Round four swept FIXTURES. This round shows that a repair's own
residue hides in the **MECHANISM the repair did not extend** and in the
**OPERATIVE CLAUSE the repair did not re-read** — and that the reliable instrument
is reading the amended requirement AS A SET, not at the sites a reviewer named.
A scenario-complete restatement is not thereby a coherent one.

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
