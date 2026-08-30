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
CLASS — `controller_corroborated`, `hardware_attested`, or `runner_claimed`. **An
unclassed fact is refused.**

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

## D3 — The gate's extension is ADDED, not MODIFIED, and the reading is written down

**Decision.** This packet carries NO `## MODIFIED Requirements` block. The gate's
extension from links 1–3 to links 1–6 is an ADDED requirement that states, in
requirement text, that links 4–6 stop being "a later tranche's link" on this
tranche's realization.

**The problem.** Tranche one's gate requirement says *"The gate's scope at this
tranche is links 1–3 and it SHALL NOT report the absence of a later tranche's
link as a break, because a gate cannot walk a link that does not exist yet"*, and
carries a scenario headed **"a tranche-two link does not exist yet"** whose WHEN
is *"the gate walks a chain that carries no attestation link"* and whose THEN is
that the absence *"is not reported as a break"*. Left alone after tranche two
lands, that is a permanent exemption for exactly the chain this tranche exists to
refuse.

**Why ADDED is the right instrument and not a dodge.** The sentence is
SELF-LIMITING on its own face — "at this tranche", "a later tranche's link", "a
link that does not exist yet", and a scenario heading that names its own
expiry. Tranche one wrote it that way deliberately, in the same requirement that
declares the hash-link rule takes effect at tranche two's first signed link. A
MODIFIED block would be restating a requirement to say what it already says.

**And the alternative carries a cost this packet is not entitled to impose
silently.** Tranche one is an ACTIVE change: its gate requirement lives in a
sibling's ADDED delta, NOT in `openspec/specs/`. A MODIFIED block here would
restate a requirement canon does not yet hold, and its correctness would depend
on archive order — the promotion-order hazard the repository is governing in its
own right (issue **#502**, and the `govern-sibling-added-modified-deltas` change
raised against it as PR #504). Restating it would also cost twelve scenarios of
verbatim carry, and the #329/#330 loss class is what happens when a restatement
carries fewer scenarios than the original.

**The reading is REPORTED, not applied silently.** It is in the delta's
requirement 6 body, it has its own scenario ("a chain carrying links 1–3 only
reaches the gate after this tranche is in force"), it is in the proposal, it is
in the pull request body, and **it is the second thing the council is asked to
rule on.** If a seat rules the composition insufficient, the named repair is a
SCENARIO-COMPLETE MODIFIED restatement of tranche one's gate requirement — all
twelve scenarios, not the two that change.

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

**Why the log and not link 4.** Declaring the expected task set in the setup
attestation was the other candidate and is worse: link 4 is signed BEFORE the
runners execute, so a dynamically fanned-out task set is not knowable at that
point, and a rule requiring it would be unbuildable for the ordinary case. The
log is written as the acts happen, which is the property the derivation needs.
**The residual is tranche one's declared one and is inherited, not re-declared:**
a store truncating its newest unobserved leaves could hide a link-5 leaf and make
an incomplete enumeration look equal — the suffix truncation tranche one's
transparency-log requirement already declares it cannot detect, with tranche-three
anchoring named as what closes it.

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

## What this design does NOT decide

Named so the review has the list rather than reconstructing it, and so none of
these reaches schema authoring open:

1. **The record home for the signing request.** Whether the runner's signing
   request is a field on the link-5 attestation or a sibling record it references.
   The requirement fixes that it is RECORDED ALONGSIDE the signature and refuses
   its absence; it does not fix the shape.
2. **The evidence-class vocabulary's closure.** Three classes are named
   (`controller_corroborated`, `hardware_attested`, `runner_claimed`). Whether the
   set is CLOSED at the schema, and what a fourth would have to establish to be
   admitted, is a contract decision and belongs with the schema.
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
