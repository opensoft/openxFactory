---
code_surface: openxFactory — A NEW NEUTRAL CONTRACT FAMILY PLUS ITS REFUSING VALIDATOR, declared honestly because this tranche is not doctrine-only. `contracts/chain-anchoring/` gains the MULTI-ANCHOR RECEIPT record (material digest, anchored digest, aggregation Merkle path, and a per-chain list whose entries carry FOUR elements — anchor transaction bytes, transaction-to-block or DAG inclusion proof, block header, and chain-acceptance evidence — plus the declared independently-obtainable header source verification runs against, AND the MINT-TIME CONFIGURATION BLOCK — the configured witness set, each witness's declared completion horizon, and the submission time those horizons run from — which the ANCHORED DIGEST commits to in every representation, so a rewritten set or an extended horizon breaks the same proofs that check the anchor), the ANCHOR-BOUND COMMITMENT record (declared construction — algorithm, keyed, salted — plus a SALT custody reference AND a KEY custody reference, both resolving into the governed layer, and the salt's declared cryptographically-secure source and width at or above the floor), the ANCHOR STATE record (`anchor_pending` / `anchor_incomplete` / complete — DISJOINT states, per-witness, with declared completion horizons, the two EXPLICIT TRANSITIONS out of pending (horizon breach, terminal witness failure) each written as a leaf, and no aggregate boolean), the CONSENT-CHECKPOINT commitment record, the LOG-CHECKPOINT ANCHOR record carrying its own never-read-as-validation disclaimer, the PLANE-SEPARATION declaration (per-plane keys under per-plane salts), the AUTHORIZED LINKAGE DERIVATION record (issuing plane, the anchored consent checkpoint it was issued under, the per-analysis scope parameter, expiry, and the revocation surface a USE consults — with an unreadable revocation state refusing the correlation), the ANALYSIS RESULT record carrying a CLOSED-ENUMERATION STATUS DISCRIMINATOR, the NAMED omitted correlation with its refusal GROUND from a named enumeration rather than free text, and the per-plane results carried distinctly — so a complete result, a correlation-refused result and an arbitrary silent partial are decidable apart, and the realization conformance declaration on `add-trust-anchor`'s declared-shortfall pattern — plus packaged POSITIVE and NEGATIVE examples for every named refusal, and the canonical `scripts/validate-chain-anchoring.py`. Registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive bundle cut. NOT THIS CHANGE'S SURFACE, each for a stated reason - the anchoring RUNTIME (an archival node for the operational witness, an aggregation-calendar client for the durability witness, the batching scheduler) is OPERATOR INFRASTRUCTURE commissioned at realization and named in `tasks.md` §4, not contract bytes; the PERMISSIONED LEDGER SELECTION (Fabric or Besu class) is a realization decision this packet deliberately does not fix; the DOMAIN OVERLAYS (MedxChain/HealthLinc, LedgerLinc) belong to their own repositories; and the TRANSPARENCY LOG itself is `add-signed-execution-chain`'s tranche-one artifact, consumed here and not redefined. NO attestation record, NO controller certificate, NO per-task identity and NO certificate authority - those are tranche two's surface.
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`. The count was taken at this branch's tip rather than remembered: `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v2.2` and `contracts/releases/contract-v2.2.digests.yaml` is a cut inventory in the tree, so the era is v2.2 and the next additive minor is unspent. A NUMBER IS NOT WRITTEN HERE BECAUSE A SIBLING ALREADY HOLDS THE NEXT ONE: `add-signed-execution-chain` is ratified and names `contract-v2.3`, and `add-chain-attestation` (tranche two, in flight) reaches the same cut — several changes ride one additive cut, and a packet that spends a minor before merge order is known is the `contract-v1.28` renumber sweep repeating. THE CLASS IS ADDITIVE and nothing narrows: a new contract family is the versioning policy's "new contracts" case verbatim, no existing schema changes, no consumer pinned at the current bundle is made non-conformant, and no domain is obliged to adopt a chain.
---

# Proposal: add-chain-anchoring

Status: draft
Proposed: 2026-08-29, as EXIT 3 OF THREE of the staged topic
`signed-execution-chain`. **RATIFICATION HAS NOT HAPPENED AND IS NOT SOUGHT BY
THIS PACKET'S LANDING.** This packet is authored to be read adversarially by a
§7.4-shaped council convened OUTSIDE the clearance pipeline — proposals are
never-convenable through it, unanimously, 2026-08-28 — and Brett Heap's
ratification follows that review. The house pattern is
`add-binding-consumer-identity`, whose `review/` directory holds the sitting's
record and whose ratification came after it; a `review/` directory is CREATED
HERE WHEN THAT RECORD LANDS, because an empty one would assert a sitting that
has not happened. Every decision the authoring session took is
listed in § Authoring decisions put to the council rather than presented as
settled.

**THE COUNCIL HAS SINCE SAT, 2026-08-30, AND `review/` NOW EXISTS.** It holds
the convening packet, the ballot as put, the four verbatim seat returns, this
packet's council record and `disposition-2026-08-30.md`, the sole disposition of
record. Brett Heap ruled *"accept all fifteen as recommended, 14 folds into the
fix rounds"*; this packet's three blocking amendments and one folded bot finding
are discharged in the fix round, and the paragraph above now describes how the
directory came to be rather than the state of the tree. **RATIFICATION IS THE
NEXT ACT AND HAS STILL NOT HAPPENED** — the ruling authorized a fix round and
*"ratifies nothing, merges nothing, and moves no contract byte"*.

## Why

**The two rulings that gated this tranche were given on 2026-08-29, and the
gates are the only thing that was ever holding it.** Brett Heap ruled all seven
of the staged topic's questions in a clarify sitting that day (#499, squash
`9c501df6`). Q3 and Q6 were the tranche-three blockers, and the topic's own exit
path records the consequence in terms: *"Tranche 3 was gated by **Q3 and Q6**,
and both gates are now **OPEN**."* What remains for this tranche is machinery,
not a ruling — and machinery is what a proposal is for.

**The forcing shape is that tranche one signs the decision and tranche two
attests the execution, and neither is externally undeniable.** The transparency
log is the evidence plane and it IS the record — that is claim 6 of the staged
topic and a tranche-one artifact by Q4's ruling. But a log inside the factory's
own governed store is a record the factory keeps about itself. A party outside
it — a hospital verifying that a record's commitment matches what it holds, an
insurer verifying that a claim references a real and unaltered record, a
regulator asked whether a decision predates a dispute — has only the factory's
word for when a leaf appeared. **Anchoring is what converts the factory's own
record into a fact the factory cannot revise**, and it is the only thing in the
family that does.

**And the deletion residual tranche one DECLARED is what this tranche closes.**
`add-signed-execution-chain` states its own limit rather than overclaiming: a
store that drops its newest leaves and presents an earlier valid signed tree head
shows a shorter log that verifies perfectly, and that residual is DECLARED under
the realization-conformance obligation with **tranche-three anchoring named as
what closes it**. This packet is the named closure of a gap another packet
refused to paper over.

**The neutral-layer argument is the same one the family has made twice and it
holds here too.** MedxFactory's HealthLinc anchors treatment-plan commitments and
consent checkpoints; LedgerxFactory's LedgerLinc anchors analysis and review
records. They differ in payload and regulator, not in receipt, not in witness,
not in boundary. A capability that fit one domain would belong in that domain's
repository.

## What this change is — TRANCHE THREE, built to a RULED configuration

**Almost nothing in this packet is proposed. Most of it is ruled**, and the
document distinguishes the two everywhere rather than presenting a ruling as an
argument. What is ruled: the anchoring configuration (Q3, two rounds), the
on-chain boundary (Q2), the commitment reading of the expansion ruling (Q6), the
absence of a permanence claim about contract code (Q5), and the receipt-first
ordering (the topic's exit path). What this packet decides, and puts to the
council: the semantics of a missing witness, the structural form of the payload
refusal, the declared-construction form of the unsalted-commitment refusal, the
per-plane key correction, and the capability's name.

- **The multi-anchor receipt format, FIRST.** The topic's exit path is explicit
  that tranche three *"builds the multi-anchor receipt format FIRST — the receipt
  is what makes the anchor choice reversible, and it must carry BOTH witnesses'
  proofs from the start; anchoring to a single chain with a bespoke receipt would
  be the one-way door this design exists to avoid."* Requirement 1 is therefore
  first in the delta as well as first in the build.
- **The ruled anchoring configuration.** Both witnesses on every anchored item:
  the operational witness first in order of arrival, the durability witness on
  everything, no selectivity, no third chain, ten-year claims citing the
  durability witness.
- **The boundary as contract text with a refusing validator**, and the
  commitment reading as its operative form.
- **Anchor late**, because a false attestation that reaches a chain is permanent.
- **The permissioned consent plane**, whose state roots are anchored and whose
  rows never are.
- **Two obligations carried from a named source** — verification-attempt
  auditing and the meta-analysis lane — and one correction TO that source.
- **The neutrality boundary**, stated as a refusal rather than as an aspiration.

**Not in this packet:** no attestation record, no controller certificate, no
per-task identity, no certificate authority — those are tranche two's, and
`add-chain-attestation` is in flight beside this one. The transparency log is
tranche one's artifact, CONSUMED here and not redefined.

## The naming divergence, stated rather than left to be noticed

`add-signed-execution-chain`'s ratified text names this successor
**`add-signed-execution-chain-anchoring` (working id)** and tranche two
**`add-signed-execution-chain-attestation` (working id)**. Both are raised under
shorter identifiers — **`add-chain-anchoring`** here and **`add-chain-attestation`**
for tranche two — and the word "working" in the ratified text is what admits the
change. It is recorded here rather than glossed, because a reader arriving from
the ratified packet will look for the longer name and should find out in one
place why it is not there. **Nothing else moved**: the successor this packet
raises is the successor that packet named, with the same content boundary.

The capability is `chain-anchoring` rather than a second block of `## ADDED
Requirements` on `signed-execution-chain`. Two active changes writing ADDED
requirements into one capability is the sibling-delta shape openxFactory issue
**#502** was filed about and `govern-sibling-added-modified-deltas` (PR #504) is
proposing rules for; a distinct capability avoids it outright rather than
navigating it, and the anchoring plane is a distinct object in any case — it has
its own contracts, its own validator, its own refusals, and a domain may adopt
the chain without adopting an anchor. **This packet carries no `## MODIFIED
Requirements` block anywhere**, so it restates nothing and can drop nothing.

## The ruled inputs, cited where they bind

| Ruled input | Where it is recorded | What it binds here |
| --- | --- | --- |
| **Q3, round 2** — *"Bitcoin-via-OTS on everything."* Both witnesses on every anchored item; Kaspa FIRST as the operational witness under three unchanged conditions; Bitcoin batched via OpenTimestamps as the durability witness; ten-year claims cite Bitcoin; no selectivity; no third chain; "primary" is order of arrival, never evidentiary weight | `ideation/staging/signed-execution-chain/signed-execution-chain.md` § "The ruled configuration (Q3, ruled 2026-08-29 by Brett Heap)" and Q3's Disposition, ROUND 2 | Requirement 2, whole |
| **Q3's three conditions** — an archival node, inclusion proofs captured AND retained at anchor time, corroborating evidence never sole | Same section: *"adopted under the study's three conditions, unchanged"* | Requirement 2's second block, as SHALL-obligations; and `tasks.md` §4 as realization tasks |
| **Q2** — on chain: salted keyed commitments, consent-log CHECKPOINT commitments, the anchors. Off chain: every payload without exception, consent STATE, the SALTS. Drawn as CONTRACT TEXT with a validator refusing a payload-shaped record AND an unsalted commitment | Q2's Disposition, 2026-08-29 | Requirements 5 and 6 |
| **Q6, CONFIRMED and now the 2026-08-27 ruling's OPERATIVE FORM** — "patients put PHI portions on chain" means SALTED KEYED COMMITMENTS: a verifiable public handle, the bytes disclosed off-chain under an anchored consent checkpoint, erasure by salt destruction. Raw, encrypted and plain-hashed regulated content on chain stay REFUSED, and **no later change re-litigates it** | Q6's Disposition, 2026-08-29 | Requirement 5, including the erasure consequence |
| **Q5** — *"Allow contract code later."* Evidence-only is today's posture; the change MUST NOT constitutionalize "no contract code ever" and MUST NOT gate a future adoption on any trigger condition written in advance | Q5's Disposition, 2026-08-29 | Requirement 6's third block, and § Q5 compliance below |
| **The receipt-first instruction, and the corrected receipt form** — digest → aggregation Merkle path → per-chain {anchor transaction bytes, transaction-to-block or DAG inclusion proof, block header}, captured whole at anchor time. A FOURTH element, chain-acceptance evidence, is added by this packet's review round and is named in § What the review round corrected | § "Exit path", tranche 3; and the topic's standing correction over the study's compact sketch, recorded at Q3's Explanation and at claim 7 | Requirement 1, whole |
| **ANCHOR LATE** — a false attestation reaching a chain is permanent, so only validated material is anchored; the cost of lateness is one aggregation interval | § "Conflicts", the conflict inside the vision; and `ideation/staging/INDEX.md`'s topic detail | Requirement 4 |
| **Consent and execution logic NOT on the anchoring chain** — the governed policy plane, and a permissioned consortium ledger where several external covered entities share state, whose state roots are anchored; no smart contracts on the anchoring chain; not Kasplex or Igra in 2026 | § "The recommended architecture, from the study", carried unchanged by the ruling | Requirement 6 |

**Where the ruling and the study differ, the ruling governs and the study
stands.** The study seated Bitcoin as the primary anchor with Kaspa an OPTIONAL
secondary; the ruling keeps both chains, reverses which is called primary, and
makes neither optional. Every substantive finding of the study survives — its
Kaspa conditions, its pruning finding, its refuted cost prior, its refusal of
contract code on the anchoring chain — and what changed is ordering and
optionality. **The study is not edited by this packet and must not be**: it is a
dated research record, and a record rewritten to agree with a later ruling stops
being evidence. This packet cites it for GROUNDS
(`ideation/staging/signed-execution-chain/chain-selection-study.md` §6 for the
EDPB and HIPAA finding, §7 for the three-layer architecture and the Kaspa
conditions, §8 for the cost model that refuted the prior, §9 for what could not
be established) and cites the topic's ruled sections for the CONFIGURATION.

## The three obligations carried from the MedxChain notes

`ideation/brainstorm/medxchain-blockchain-medical-records.md` is Brett Heap's own
2024 design sketch for a blockchain-backed medical-records product, vendored into
this repository's ideation by **PR #509, which is IN FLIGHT at the time of
writing**. It is cited by path here because that is the path it lands at; a
reader checking the citation before #509 merges will not find the file, and this
sentence is why. The notes' own appendix names two additions the neutral family's
text did not carry and one framing worth stating, and this packet carries all
three as named requirements:

1. **Verification-attempt auditing** (requirement 7). The notes log views, edits,
   **failed attempts** and administrative actions. The family's ten links are
   framed around what was signed and produced; an evidence plane that records
   only writes cannot answer who tried, which for a capability whose purpose is
   external verifiability is a hole in the exposed surface. The neutral form adds
   the boundary consequence the notes do not: **attempt rows are never anchored
   directly**, because a per-attempt public trail leaks by metadata exactly what
   the payload rules keep off chain — only batched checkpoints over the attempt
   leaves are anchored.
2. **The meta-analysis lane** (requirement 8). The notes make record-plus-
   demographic analysis without the identity plane a first-class use case. It is
   carried as a named consumer rather than left as an emergent property of the
   segregation.
3. **The domain-instantiation mapping** (requirement 9). MedxChain and HealthLinc
   are MedxFactory's instantiations; LedgerLinc is LedgerxFactory's; the neutral
   layer authors no domain content. The notes read as an early, domain-specific
   sketch of the same shape, PREDATING the neutral family — with no interval
   stated, on LQ-A5's ground: the figure this once read was wrong, nothing here
   turns on how long, and the dates belong to the vendored document.

**And one CORRECTION to the source, raised rather than inherited.** The notes
segregate three databases but carry ONE shared record digest across all three,
which makes that digest a cross-plane JOIN KEY: a holder of a demographic row and
an identity row can link them without either plane's permission, and the
segregation is then nominal. Requirement 8 therefore requires per-plane keys
derived under per-plane salts, and requires that the anchored commitment — derived
under the record's own salt, held in the governed layer — does not function as a
join key. This is a **fourth 2026 upgrade** to the 2024 sketch, beside the three
the notes' appendix already records (plain hashes → salted keyed commitments; an
on-chain encrypted PII database → a permissioned plane with anchored state roots;
per-access public entries → signed leaves with batched anchored checkpoints).

## Authoring decisions put to the council

Listed rather than presented as settled. Each is this session's decision, and
each is the kind of thing a §7.4 sitting exists to contest.

**D-A. The semantics of a missing witness — the packet's largest decision.** The
staged topic rules the CONFIGURATION and says nothing about what happens when a
witness is unreachable, so this packet had to decide. It decides: **what fails
closed is the CLAIM, not the factory.** An item carrying fewer witnesses than the
configuration demands is `anchor_incomplete` with its missing witnesses NAMED,
verification of it returns `anchor_incomplete` rather than a bare pass or a bare
fail, a ten-year claim over it is refused while the durability witness is
missing, and the state and every horizon breach are written as leaves. A witness
outage never blocks ratification, execution, review or any gate. The two outages
are treated ASYMMETRICALLY and the requirement says so. The full ground, the
rejected alternatives and the asymmetry are `design.md` **D2**.

**D-B. The payload refusal is STRUCTURAL, not semantic.** The validator refuses
any anchor-bound record carrying a content-bearing field BY SHAPE, and never by
recognizing what the content is about. A neutral validator that refused protected
health information by name would need domain semantics to do it — which
requirement 9 forbids — while a validator that refuses EVERY payload needs none
and is strictly stricter. `design.md` **D3**.

**D-C. The unsalted-commitment refusal is BY DECLARED CONSTRUCTION, and its
residual is declared.** A salted keyed commitment and a plain digest of the same
record are indistinguishable by inspection — both are opaque values of the same
width — so the refusal cannot be by inspection and this packet does not pretend
it can. Records declare their construction and a salt custody reference; the
validator refuses an absent, unkeyed or unsalted declaration and a salt reference
resolving onto a chain. The residual — a record DECLARING a salted keyed
construction while anchoring a plain digest — is raised as an EXPLICIT GAP on
`add-trust-anchor`'s declared-shortfall pattern, closed at realization by making
the commitment path the only path that can mint an anchor-bound value.
`design.md` **D4**.

**D-D. The capability is `chain-anchoring`, and the change id is
`add-chain-anchoring`.** Both diverge from the working ids the ratified tranche
one named. § The naming divergence above.

**D-E. The permissioned ledger is NOT selected here.** Fabric or Besu class is
named as the class, the selection is a realization decision, and the council may
rule that it should be fixed now instead. Note precisely what this is NOT: Q3's
"no third chain" governs ANCHOR chains, and a permissioned consortium ledger is
not an anchor chain — its state roots are anchored BY the two ruled witnesses.
Selecting one re-litigates nothing. `design.md` **D5**.

**D-F. The per-plane key correction.** § The three obligations, above. It
corrects a vendored source rather than restating it, which is a thing to say out
loud.

## Q5 compliance, stated positively rather than left to inference

Q5's ruling contains a REFUSAL a packet can breach by writing too much, so this
one states its compliance. What Q5 preserved is the posture: the anchoring chains
stay evidence-only today, and no tranche now planned puts contract code on any of
them. What it REFUSED is the permanence the recommendation asked for.

**This packet therefore does three things and no more.** It puts no contract code
on any chain — requirement 6 states the evidence-only posture as THIS
CONFIGURATION'S, in the present tense. It writes **no "never"**: there is no
requirement, scenario or design note here forbidding on-chain contract code in a
future change. And it writes **NO TRIGGER CONDITION** — the recommendation would
have gated a future adoption on patient-facing verifiability across organizations
sharing no consortium, and the ruling refuses that gate, so this packet names no
condition under which contract code would become admissible. The same discipline
governs requirement 2's third-chain block: it refuses a third target adopted by a
realization or an operator ACTING ALONE, and it names no condition under which a
ruling would adopt one, because a later ruling answers to its own evidence.

The study's cautions — the EDPB and HIPAA posture, the unaudited-stack risk that
made Kasplex and Igra a refusal in 2026, the irrevocable-deployment vulnerability
class — survive as **ADVISORY CONTEXT** a later author must answer, never as this
packet's permission to withhold.

## What the review round corrected, before the council ever sits

Two Codex P1 findings and a Copilot cluster on this packet's own pull request,
all real, and all of the same shape the family keeps meeting — **a rule naming
something it could not actually do.** Recorded here rather than silently
patched; the full reasoning is `design.md` **D8** and **D9**.

1. **An anchored checkpoint cannot exclude an earlier leaf, so "no unvalidated
   material reaches a chain" was unachievable as written.** The log is
   append-only: every signed tree head commits to the whole prefix, refusals
   included, so anchoring late cannot keep a refused leaf out of a later
   checkpoint. **Resolved by naming two anchors rather than weakening one rule** —
   an ITEM ANCHOR, which only gate-passed material receives and which the
   anchor-late rule governs; and a LOG CHECKPOINT ANCHOR, which witnesses that the
   log SAID something and **makes no claim about any leaf's validity**, with
   inclusion never read, presented or verified as validation. **The staged
   topic's constraint is thereby NARROWED, and the narrowing is recorded rather
   than applied silently** — the constraint governs item anchors, and what it
   protects is honoured by the split.
2. **A block header is not canonicality.** Transaction bytes plus an inclusion
   proof establish only that the transaction sits under THE SUPPLIED HEADER's
   Merkle root; a fabricated header satisfies all three elements. The receipt
   gains a **fourth per-chain element — CHAIN-ACCEPTANCE EVIDENCE** (block height
   plus header-chain linkage, or a DAG-acceptance proof) and a NAMED,
   INDEPENDENTLY OBTAINABLE HEADER SOURCE, with the limit stated: a receipt is
   **checkable against** a canonical header set the verifier fetches for itself,
   never self-sufficient against a forged history, and a verification against a
   header source the minter supplied is REFUSED. This is the same defect class
   the requirement already refused one step earlier — the draft caught the
   header-plus-bare-reference shape and missed the fabricated-header shape.
3. **Terminology: the receipt was doubling as the state record.** Copilot read
   "the receipt records per-witness status" and "the pending receipt" as
   contradicting requirement 1's fully-populated receipt, and was right.
   **PER-WITNESS STATUS lives in the ANCHOR-STATE record; the receipt holds proof
   material and never state**, and a witness in flight is a PENDING DURABILITY
   PROOF that is upgraded and appended, never a half-filled receipt entry. The
   structure was already this; the words were not.

*One of these was self-caught before the bots ran* — the pending-entry collision,
commit `455bbdaa` — *and the round then showed the fix had repaired the structure
while leaving the vocabulary that caused it.* That is worth carrying: a
correction stated in a new paragraph does not retire the old wording elsewhere in
the packet, and a sweep is part of the fix.

## Capabilities

### New Capabilities

- `chain-anchoring`: the neutral public anchoring layer and the permissioned
  consent plane, **NINE ADDED requirements over 77 SCENARIOS** (52 scenarios at
  the head the council judged; the 2026-08-30 fix round and its six bot rounds
  added twenty-five scenarios and no new requirement), no `## MODIFIED
  Requirements` block anywhere — a chain-agnostic multi-anchor receipt defined
  FIRST and refused at capture time if any of its four per-chain elements is
  missing; the ruled two-witness configuration with no selectivity and no third
  chain, the operational witness under its three unchanged conditions and
  ten-year claims citing the durability witness; a missing witness as a DECLARED
  fail-closed state that degrades the claim and never the factory; anchoring only
  gate-passed material AS AN ITEM, with a log checkpoint told apart from an item
  anchor because an append-only prefix cannot be held back and a checkpoint is
  never a validity claim; the
  on-chain boundary as contract text with a validator refusing payload-shaped
  records STRUCTURALLY and unsalted commitments BY DECLARED CONSTRUCTION, with
  salt destruction's erasure and its permanent unverifiability stated together;
  consent state in the permissioned plane with only checkpoints and state roots
  anchored, revocation's limit stated rather than implied; verification attempts
  and refused access as logged leaves; the record and demographic planes
  analyzable without the identity plane BY CONSTRUCTION, with per-plane keys
  closing the join-key defect; and a neutrality boundary an overlay may tighten
  and may never relax.

### Modified Capabilities

**None.** No promoted requirement is restated or replaced, and this change
carries no `## MODIFIED Requirements` block anywhere. `signed-execution-chain` is
an ACTIVE change whose ratified text governs and which this packet composes with
by reference; `add-chain-attestation` is a live sibling and this packet touches
none of its ground; `add-trust-anchor`, `credential-contracts` and
`workflow-gate-contract` are composed with and not moved. Composing by reference
is the staged topic's own instruction and the condition under which its Conflicts
table admits a tranche at all.

## Impact

- **New code (this change authorizes; realization is a later commission)**: one
  contract family, packaged positive and negative examples for every named
  refusal, one canonical validator, and manifest / CHANGELOG registration at the
  next additive bundle.
- **New operator infrastructure, named and NOT authorized as contract bytes**: an
  ARCHIVAL NODE for the operational witness, an aggregation-calendar client for
  the durability witness, and the batching scheduler that makes anchoring cost
  one interval rather than one transaction per item. These are `tasks.md` §4
  realization tasks with an operator marker, and the Kaspa conditions are
  discharged there or the requirement is unmet.
- **Consumes, and does not re-invent**:
  - `add-signed-execution-chain`'s **transparency log** — the evidence plane, a
    tranche-one artifact by Q4's ruling. This packet writes leaves into it and
    anchors checkpoints of it; it does not redefine it, and it adds no second
    log.
  - `add-signed-execution-chain`'s **ONE digest construction** requirement, which
    already declares that one construction governs every digest the family
    computes and reaches forward to *"any digest a later tranche adds"*. Every
    digest in this packet — the
    anchored digest, the aggregation root, the checkpoint commitment — is that
    construction, and this packet declares no second digest rule.
  - `add-trust-anchor`'s ratified **declared-shortfall** pattern, which is what
    D-C's residual is declared under.
  - The **fail-closed doctrine** the family already applies: a gate that cannot
    evaluate its condition refuses, and an unevaluable answer never reads as
    permission. Requirement 6 applies it to an unreachable permissioned plane;
    requirement 3 explains why an unreachable WITNESS is a different case and
    does not.
- **Composes with, and is bounded by**: `add-chain-attestation` (tranche two, in
  flight — this packet defines no attestation and no certificate), and the
  domain overlays, which are authored in their own repositories.
- **Obliges no domain.** No domain must adopt a chain or an anchor, and no
  existing capability is modified in a way that requires action from a domain
  that has none.

## Where the ruled texts and a ratified artifact pull against each other

Recorded rather than smoothed, on this family's contested-finding rule. **One
item, and it is a naming divergence rather than a substantive conflict**: the
ratified `add-signed-execution-chain` names this successor
`add-signed-execution-chain-anchoring` and tranche two
`add-signed-execution-chain-attestation`, both explicitly as **working ids**, and
both are raised under shorter names. § The naming divergence records it. The
authoring session found **no substantive conflict** between the ruled Q2/Q3/Q5/Q6
text, the vendored study, the tranche-one ratified packet and the in-flight
MedxChain notes; the Q3-versus-study divergence is not a conflict but a
divergence the record itself already reconciles, in the direction it names.

## Review and ratification — the order, stated

1. **This packet lands as a draft.** It ratifies nothing and asks for nothing.
2. **A §7.4-shaped council reviews it**, convened OUTSIDE the clearance pipeline,
   because a class over `openspec/changes/**` can never commission one — measured
   on this repository's real tree, 984 admitted paths, 984 floored, 0 remaining,
   and reproduced code-level (the 2026-08-28 `gate_rules_council` convening
   record, unanimous 5/5). The §7.4 council-reviewed-but-human-approved path
   needs no class and no flip and reaches this repository without an envelope.
   The record lands in this change's `review/` directory, on
   `add-binding-consumer-identity`'s pattern.
3. **Brett Heap ratifies, or does not**, after that review. Ratification would
   authorize realization and would perform none of it.

**STEPS 1 AND 2 ARE DONE; STEP 3 IS WHAT IS NOW OPEN.** The council sat
**2026-08-30** — four seats, judged at head `cf5a24b8` — and returned ACCEPT
(`lead-architect`) and ACCEPT AS AMENDED (`lead-security`, `lead-quality`,
`company-policy-lead` within its charter). Brett Heap ruled the ballot *"accept
all fifteen as recommended, 14 folds into the fix rounds"*, which accepted this
packet's **three blocking amendments** — LS-A5, LS-A6, and LQ-A5's #513 limb —
and folded in one crossing bot finding. **All four are discharged in this
packet** (`tasks.md:2.4`), and the whole sitting is in `review/`, where
`review/disposition-2026-08-30.md` is the sole disposition of record and the
verbatim seat returns govern over every summary of them, this one included.
**The ruling authorized a fix round and ratified nothing.**
