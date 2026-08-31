# Design: add-chain-anchoring (tranche three)

The decisions this packet took, with their grounds and their rejected
alternatives. Where a decision is RULED it is cited and not re-argued; where the
authoring session decided, the decision says so and is listed in the proposal's
§ Authoring decisions put to the council.

The load-bearing distinction throughout: **the ruled texts fix the
configuration, and this packet fixes the machinery.** A design note that
re-argues a ruling has misread its job; a design note that leaves a machinery
question to an implementer has left the gap the review round will find.

## D1 — Q3 DIVERGES from the study, the ruling governs, and the study is preserved unedited

**The divergence.** The vendored `chain-selection-study.md` (dated 2026-08-27,
sourced and date-checked) recommends, at its §7 and §10: **Bitcoin as the primary
anchor** via OpenTimestamps aggregation, and **Kaspa as an OPTIONAL low-latency
SECONDARY anchor** under three conditions. Brett Heap ruled Q3 on 2026-08-29 in
TWO ROUNDS, and round two is the operative configuration: **both witnesses on
every anchored item**, **Kaspa FIRST** as the primary, OPERATIONAL witness under
the same three conditions unchanged, **Bitcoin batched via OpenTimestamps as the
DURABILITY witness on EVERY anchored item**, ten-year claims citing Bitcoin, **no
selectivity** and **no third chain**.

**What actually changed is ORDERING and OPTIONALITY, and nothing else.** The
staged topic states it in terms: *"The study seated Bitcoin as the primary anchor
and Kaspa as an OPTIONAL secondary; the ruling keeps both chains, reverses which
one is called primary, and makes neither optional… Every substantive finding of
the study survives: its Kaspa conditions, its pruning finding, its refuted cost
prior, its refusal of contract code on the anchoring chain."* This packet builds
to the ruling and cites the study for grounds, and the two are never in tension
in any requirement text, because the requirement carries the ruling's
configuration while its ground carries the study's evidence.

**"Primary" is order of arrival, not evidentiary weight**, and the requirement
text says so because the word is the trap. The pruning finding is not softened by
the promotion — the operational witness is still corroborating-only, still needs
an archival node, still needs its inclusion proofs captured at anchor time, and
the ten-year claim still rests on the other witness. A reader who takes "primary"
as "the one the claim rests on" has inverted the ruling.

**The study is NOT edited by this packet, and a later author must not edit it
either.** It is a dated research record; a record rewritten to agree with a later
ruling stops being evidence. The reconciliation lives in the staged topic, which
carries both rounds, the cost facts put between them, and the divergence stated
plainly. This packet adds nothing to that reconciliation and subtracts nothing
from it.

**Rejected: re-deriving chain selection here.** A proposal that re-argued the
selection would be relitigating a governance decision the repository owner has
already ruled, on evidence a research fan-out already gathered. The packet cites
and builds.

## D2 — What happens when a witness is unavailable — THE PACKET'S LARGEST DECISION

**Nothing ruled answers this.** Q3 fixes the configuration; the topic's exit path
fixes the ordering of the build; neither says what an item IS when a witness
cannot be reached. A tranche-three packet that left it unstated would be shipping
the interesting half as an implementer's choice, and the choice is precisely
where "an item with one witness is basically fine" becomes a habit — which is
selectivity arriving by the back door that the ruling closed at the front.

**The structural fact that forces the shape.** The durability witness's
aggregation is DEFERRED BY HOURS in the healthy path — that is what
OpenTimestamps aggregation IS, and it is why the study's cost model works at all:
a calendar batches commitments and the Bitcoin attestation completes by UPGRADE
when the calendar's own commitment confirms. So a rule of the form "an item is
anchored only when both witnesses have landed, and an item that is not anchored
is refused" would refuse EVERY item for hours, every day, with nothing wrong.
Any honest semantics has to be **two-phase and deadline-bounded** rather than
instantaneous.

**The decision: what fails closed is the CLAIM, not the factory.**

- An item enters `anchor_pending` when validated material is submitted, and each
  witness carries a declared COMPLETION HORIZON (minutes for the operational
  witness, hours for the durability witness, matching its calendar's cycle).
- An item whose configured witnesses are not all present is `anchor_pending`
  while every unmet witness is within its declared horizon, and becomes
  `anchor_incomplete`, **with its missing witnesses NAMED**, only on a horizon
  breach or a named terminal witness failure. Neither state is ever reported,
  presented or verified as anchored.
- **A witness outage never blocks ratification, execution, review or any gate.**
  The ground is claim 6 and tranche one's ruled sequencing: the transparency log
  is the evidence plane and IS the record; anchors are LATE ADDITIONS to its
  leaves. A leaf's standing has never depended on an anchor, so an outage in the
  witness layer cannot invalidate a leaf and must not be allowed to stop the
  factory.
- **What the outage blocks is the CLAIM.** Verification of an incomplete item
  returns `anchor_incomplete` naming the missing witnesses — **never a bare pass
  and never a bare fail**, because the record supports neither. A ten-year claim
  over an item missing the durability witness is REFUSED outright.
- **The incompleteness is itself evidence.** Entry into `anchor_pending`, every
  horizon breach and the eventual completion are each written as leaves, so a
  silent gap is impossible. Past its horizon an item stays incomplete and an
  operator obligation is raised; nothing but a CAPTURED RECEIPT moves an item to
  complete.
- **There is no aggregate `anchored` boolean anywhere in the capability.** A
  single summarizing flag is the field that reads true while a witness is
  missing. Per-witness status lives in the ANCHOR-STATE record, which is what
  every surface reads; the RECEIPT holds proof material and never state.

**The two outages are NOT symmetric, and the requirement says which is which.**

| Outage | What completes | Item state | Ten-year claim | Repair |
| --- | --- | --- | --- | --- |
| **Operational witness unreachable** | the durability anchor, on its own horizon | `anchor_pending` while the operational witness is within its horizon, `anchor_incomplete` once it breaches — not the configured completeness either way, so never "anchored" | **AVAILABLE**, because that claim rests on the witness that landed | anchor the operational witness when it returns; the receipt gains its entry |
| **Durability calendar unreachable** | the operational anchor, in seconds | `anchor_pending`, then `anchor_incomplete` on the durability horizon's breach | **REFUSED** until the durability anchor lands | **UPGRADE THE PENDING DURABILITY PROOF** and append its entry when the calendar returns — do NOT re-anchor |

**The do-not-re-anchor rule is not a style note.** An aggregation proof completes
by upgrade: the pending durability proof already commits to the right digest,
and the calendar's later confirmation is what completes it. Re-anchoring would mint a
SECOND transaction for the same digest, leaving two proofs to capture, retain and
reconcile where one was owed — and on the operational witness, whose transactions
are pruned within days, a second anchor is a second thing that must be captured
before it disappears. The cheapest correct act is completion.

**THE RECEIPT IS PROOF MATERIAL; THE ANCHOR-STATE RECORD IS STATE. KEEPING THEM
APART IS WHAT STOPS THE TWO REQUIREMENTS COLLIDING.** Requirement 1 refuses a
per-chain entry missing any of its four elements AT CAPTURE TIME; requirement 3
has to describe a witness in flight. Resolved by the receipt's own rule rather
than by an exception to it: **the per-chain list gains an entry only when that
chain's material is captured WHOLE**, so a witness in flight lives in the
ANCHOR-STATE record as a PENDING DURABILITY PROOF or a pending operational
anchor — never as a half-filled entry, and never as a status field inside the
receipt. Upgrading appends an entry against the digest the receipt already
commits to.

*Corrected in the bot round, and the correction was terminological rather than
structural.* The first draft of this note had the right structure but wrote
"pending receipt" and "the receipt records per-witness status", which Copilot
read — correctly — as the receipt doubling as the state representation. A reader
who has to derive the split will instead implement the half-filled entry, and a
half-filled entry is precisely the receipt shape that proves nothing. The words
now match the structure.

**Rejected alternatives, and why each fails.**

1. **Refuse the act until both witnesses land.** Refuses every item for hours in
   the healthy path, and makes the factory's ability to operate depend on a
   third-party calendar's reachability. It also inverts claim 6 — it would make
   the WITNESS the record.
2. **Treat one witness as sufficient and log the other as best-effort.** This is
   selectivity, arrived at by circumstance instead of by rule, and the ruling
   refused selectivity on the ground that a per-item decision will eventually
   decide wrong about the item that matters. An outage is a per-item
   circumstance.
3. **A single `anchored: true` flag with a warning beside it.** The flag is what
   downstream code reads and the warning is what it ignores. This is the
   "described control" defect the family has now named several times: a state
   that can read complete while incomplete is a state that will.
4. **Retry until complete, with no declared state.** Unbounded retry hides the
   outage from the record, and the outage is exactly the thing an auditor needs
   to see. The horizon-breach leaf is what makes the gap visible.

**AMENDED IN THE FIFTH BOT ROUND — the two states were not disjoint, so neither
was deterministic.** This decision named `anchor_pending` and `anchor_incomplete`
and let the boundary between them be inferred from "fewer witnesses than
configured" — which every freshly submitted item satisfies, putting it in both
states at once for the whole ordinary aggregation window. `lead-security` filed
it as LS-F11 with its charitable reading; Codex found it independently and rated
it P1. **The states are now disjoint BY DEFINITION**: pending WHILE every unmet
witness is within its declared horizon, incomplete only on an EXPLICIT
transition — a horizon breach or a named terminal witness failure — each written
as a leaf, which this decision's own evidence rule already required. A
verification of a pending item returns `anchor_pending` naming what is in flight,
so the state every healthy item passes through has an answer and the operator
obligation fires at a transition rather than on everything.

**The governance note travels with it**: LS-A9 is the seat amendment that asked
for this, it was filed SHOULD-FIX, and the disposition did not dispose it.
`tasks.md:2.4` records that this session escalated it first and executed it on
direction, so the ratification read could bless or reverse it. **BLESSED BY
BRETT HEAP, 2026-08-30** — closing ruling item 5, verbatim *"5 bless"* — which
converts the execution into his act and closes the revert path. The sequence is
not rewritten: escalated, then executed on direction, then blessed.

**AND MAKING THE STATES DISJOINT IMMEDIATELY OWED THE RECEIPT SOMETHING, WHICH
THE NEXT ROUND COLLECTED.** Two disjoint states have two verification answers,
and the receipt carried no timing at all — so a receipt-only verifier, the
holder D9 and LS-A5 exist to serve, could not tell them apart: the artifact is
byte-identical before and after a breach. **The mint-time configuration block
therefore grew to carry each witness's DECLARED HORIZON and the SUBMISSION TIME
they run from**, bound by the anchored digest exactly as the witness set already
was — the same mechanism extended, not a second one minted — so the answer is
computed locally from the artifact. **The TERMINAL-failure distinction is scoped
to stateful verification**, because a terminal failure arises after the receipt
was minted and no artifact can carry it; the text names that limit in both
directions rather than leaving it. This is D10's shape reapplied inside D2: what
the artifact can prove, it proves; what it cannot, it names.

**What this decision does NOT do.** It does not soften "both witnesses on every
anchored item". The configuration is unchanged; what is named is the honest
TRANSIT between submission and completion, and the honest DEGRADATION when the
transit does not finish. An item that never reaches both witnesses never becomes
anchored — it stays visibly, permanently incomplete, and says which witness it
lacks.

**AMENDED BY THE §7.4 COUNCIL, 2026-08-30 — `lead-security`'s LS-A5, BLOCKING,
accepted at disposition item 3.** The split above was right and INCOMPLETE at the
composition seam: because the receipt is stateless by design, a one-entry receipt
in an independent holder's hands is byte-indistinguishable from a receipt minted
under a one-witness configuration, so the fail-closed disclosure this decision
writes did not TRAVEL with the artifact requirement 1 exists to make
independently checkable. It lived only in the minter's anchor-state record, and
consulting the minter is the one thing an independent verifier cannot be asked to
do. **The discharge is the seat's own and it does not disturb the split**: the
receipt now carries the CONFIGURED WITNESS SET AT MINT TIME, which is
CONFIGURATION rather than "what has not happened yet", so the receipt still holds
no status — and a per-chain list shorter than that set is a WITNESS SHORTFALL on
its face, with the missing witnesses readable as the difference. Which lifecycle
state that shortfall amounts to is the separate horizon determination the later
rounds added, not something the shortfall asserts by itself. The set is fixed at mint
time and rewriting it to match the entries present is refused, since that edit is
exactly how a missing witness would be laundered into a one-witness
configuration.

**AND THE FIRST DRAFT OF THAT DISCHARGE WAS ITSELF A DESCRIBED CONTROL — CODEX
P1, ON THIS FIX ROUND'S OWN PULL REQUEST.** It required a commitment only where
the set is held as a companion object, and wrote the one-blob case as a REFUSAL
addressed to a realization. A refusal addressed to the minter does not reach the
party the amendment exists to protect against: the untrusted HOLDER of an
incomplete receipt edits the set rather than the entries, and every per-chain
proof still validates, because those proofs are about a transaction and a digest
and know nothing of a field beside them. **That is LS-F2's shape exactly — a fix
that repairs the record and not the control — reproduced by the fix for LS-F7,
and caught by a bot rather than by me.** The binding is now cryptographic and
uniform: the ANCHORED DIGEST commits to the configured set, so a rewritten set
breaks the aggregation Merkle path and every inclusion proof at once and the
tamper is caught by the same verification that checks the anchor. The MATERIAL
DIGEST stays carried in its own right, so nothing about naming what was anchored
is lost, and a representation carrying the set unbound is refused in every
encoding rather than in one.

## D3 — The payload refusal is STRUCTURAL, and that is what makes it neutral

Q2 ruled the boundary is drawn as contract text with a validator that refuses a
payload-shaped record AND an unsalted commitment. It does not say HOW the
validator recognizes a payload, and the obvious reading — refuse protected health
information — cannot be implemented in the neutral layer without breaching
requirement 9.

**The decision: refuse EVERY payload, BY SHAPE.** The validator refuses any
anchor-bound record carrying a field that holds record content — cleartext,
ciphertext, or any content-bearing blob — on the field's declared shape, never on
what the content is about.

**Why it is both neutral and stricter.** A validator that refused PHI by name
would need to know what PHI is, which is domain semantics the neutral capability
is forbidden to carry; it would also need to be right about the boundary, and
would silently admit a regulated payload it failed to classify. A validator that
refuses every payload needs no domain knowledge and admits no payload at all.
Raw, encrypted and plain-hashed regulated content are all outside Q2's boundary,
and the structural refusal reaches all three without classifying any of them.

**Rejected: a classification hook the domain overlays fill in.** It moves the
neutral layer's correctness onto a domain's list, which means the neutral refusal
is only as good as the least careful overlay. Requirement 9's rule — an overlay
may ADD refusals and may never RELAX one — is the same principle from the other
side.

## D4 — The unsalted-commitment refusal is BY DECLARED CONSTRUCTION, and its residual is declared

**The fact that forces this.** A salted keyed commitment (an HMAC over content
under a per-record secret salt) and a plain SHA-256 of the same content are
**indistinguishable by inspection** — both are opaque 32-byte values. There is no
check over the anchored VALUE that can tell them apart. A requirement claiming
the validator "refuses unsalted commitments" by looking at them would be
describing a control that cannot run, which is the failure this family has now
named several times.

**The decision.** Every anchor-bound commitment DECLARES its construction — the
algorithm, that it is KEYED and SALTED, and a SALT CUSTODY REFERENCE resolving
into the governed layer — and the validator refuses: an absent declaration, a
declaration that is not keyed and salted, and a salt custody reference resolving
onto a chain or into the anchored record itself. That last check is the one that
matters most in practice: a salt reachable from the anchor destroys the erasure
property the salting exists to provide, and it is an easy mistake to make while
trying to make verification convenient.

**The residual, DECLARED and not claimed as closed.** A record that DECLARES a
salted keyed construction while anchoring a plain digest is not detectable from
the record. The declaration and the custody reference are enforceable today; the
step from "the record declares a salted keyed commitment" to "the anchored value
IS one" rests on the realization making the commitment path the ONLY path that
can mint an anchor-bound value — so an undeclared construction is UNREACHABLE
rather than merely refused. A realization that cannot establish that DECLARES the
shortfall on `add-trust-anchor`'s ratified declared-shortfall pattern. This is
the same move tranche one made with the `signed_over` enum selector, and it is
made for the same reason: a requirement that overclaims what a record can prove
is worse than one that names its gap.

**The EDPB ground, cited because the requirement rests on it.** The vendored
study §6 records **EDPB Guidelines 02/2025 (v2.0, adopted 2026-07-07)**: do not
store clear, encrypted **or hashed** personal data on-chain, because *a hash of
personal data is itself personal data*, and erasure and rectification must be
designed in from the start. Under HIPAA a bare record hash is not Safe-Harbor
de-identified either. The design consequence the study draws, and which Q2 and Q6
then ruled: anchor only salted keyed commitments, salt custody in the governed
layer, and **erasure by salt destruction** — destroy the salt and the on-chain
residue is effectively anonymous, which satisfies erasure by design against a
ledger that cannot forget.

**And the erasure's cost is stated in the requirement rather than in a footnote.**
Destroying the salt makes the handle PERMANENTLY UNVERIFIABLE: no later party,
the subject included, can ever again prove that a held copy matches the anchored
value. That is not a defect of the mechanism — it IS the mechanism, since a
handle that could still be verified would still be a handle to a person. A
surface offering erasure states the loss before performing it, because a subject
choosing erasure is choosing to give up their own future ability to prove the
record.

**AMENDED BY THE §7.4 COUNCIL, 2026-08-30 — `lead-security`'s LS-A6, BLOCKING,
accepted at disposition item 3.** The seat drove Q6 in both directions and found
the decision honest in the overclaim direction and short in the understatement
one: **the erasure property is the authority for this whole narrowing, and it
rested on two parameters the contract never fixed.** (i) The commitment is KEYED
and the decision above custodies only the SALT — a realization could hold the
commitment KEY on chain, inside the anchored record, or shared across planes, and
no drafted check refused it, while requirement 8 was already careful to demand
per-plane keys under per-plane salts. The packet knew the shape and applied it in
one place only. (ii) *"Salted"* carried NO ENTROPY FLOOR: an eight-bit salt
passes every check written above and is exhaustible, so the mechanism was
asserted against the exact attack its own EDPB citation names — the guessable
input. **The discharge is the seat's**: a KEY CUSTODY REFERENCE on the salt's
footing with the same three refusals plus a shared-across-planes refusal, and a
declared salt SOURCE and WIDTH with a refusal below 128 bits. Neither adds a
second custody vocabulary; both are this decision's own rule applied to the
parameters it left out.

## D5 — Where the identity plane sits, and why the permissioned ledger is NOT selected here

**The placement.** Consent state, access-control lists, subject-to-record
linkage and the commitment SALTS all live in the governed permissioned plane.
Only that plane's STATE ROOTS and its consent-log CHECKPOINTS are anchored. The
grounds, in the order they bind:

1. **A per-subject consent row on a public chain is publicly linkable to a
   person**, permanently. The study's §6 and the topic's own correction to its
   first draft both land here: consent STATE does not go on chain; only opaque
   commitments to consent-log checkpoints do.
2. **The salts must be somewhere the anchor cannot reach**, or the erasure
   property is decorative. The governed plane is that somewhere, and requirement
   5 refuses a salt custody reference that resolves onto a chain.
3. **Several external covered entities have to SHARE this state**, which is what
   a consortium ledger is for and what a single organization's private database
   is not. The study names the live precedents and notes both pivoted toward
   FHIR-based utility networks where the chain is plumbing rather than product —
   which is also the reality check the topic carries: US interoperability runs on
   FHIR and TEFCA rails, and a chain layer earns its place as the neutral
   INTEGRITY WITNESS those rails lack, not as a replacement for them.
4. **It is the only posture EDPB and HIPAA guidance cleanly supports**, per the
   study §6 and §7.

**The selection is a REALIZATION decision, and this is not Q3 being
re-litigated.** The class is named — Hyperledger Fabric or Besu class — and the
instance is not. **Q3's "no third chain" governs ANCHOR chains**: the chains that
witness commitments. A permissioned consortium ledger is not an anchor chain; it
is a shared-state plane whose state roots are anchored BY the two ruled
witnesses. Selecting one adds no anchor target, changes no receipt, and
re-opens nothing Q3 closed. Stated explicitly here because "we are adding a
ledger" reads at a glance like the thing the ruling refused, and a reviewer
should be able to see in one place that it is not.

**Why it is deferred rather than fixed.** The selection turns on facts a proposal
cannot supply: which entities are actually in the consortium, what they already
run, and what the operator will host. Fixing it now would be a boundary drawn
against an unbuilt layer — which is exactly what Q4's ruling refused for tranche
boundaries, applied to a component. The council may rule that it should be fixed
now; it is listed as **D-E** in the proposal's authoring decisions for that
reason.

## D6 — The change id, the capability name, and the sibling-delta shape

**The ratified working ids are not used.** `add-signed-execution-chain` names
this successor `add-signed-execution-chain-anchoring` **(working id)** and
tranche two `add-signed-execution-chain-attestation` **(working id)**. Both are
raised under shorter ids — `add-chain-anchoring` and `add-chain-attestation`. The
word "working" in the ratified text is what admits the change; the divergence is
recorded in the proposal rather than glossed, so a reader arriving from the
ratified packet finds out in one place why the longer name is not there.

**The capability is `chain-anchoring`, not more `## ADDED Requirements` on
`signed-execution-chain`.** Two active changes writing ADDED requirements into
one capability is the sibling-delta shape openxFactory issue **#502** was filed
about and `govern-sibling-added-modified-deltas` (PR #504) is proposing rules
for. A distinct capability avoids the shape outright rather than navigating it.
It is also the right decomposition on its own terms: the anchoring plane has its
own contracts, its own validator, its own refusals, and a domain may adopt the
chain without adopting an anchor.

**This packet carries no `## MODIFIED Requirements` block anywhere**, so it
restates nothing and can drop nothing — the promotion-fidelity loss class
(#329/#330) has no surface here.

## D7 — The per-plane key correction, and why a vendored source is corrected rather than inherited

The MedxChain notes segregate three databases — record, demographic, identity —
and carry ONE shared record digest across all three as the linkage. **That makes
the digest a cross-plane join key**: a holder of a demographic row and an
identity row can link them without either plane's permission, and the
segregation the design exists for becomes nominal. The notes' own stated benefit
— that meta-analysis can run without exposing PII — holds only against an analyst
who has no identity rows, never against one who has both.

**The correction.** Per-plane keys derived under per-plane salts, and the
anchored commitment — derived under the record's own salt, held in the governed
layer — does not function as a cross-plane join key. The segregation is only
structural if the keys are, which is the difference between plane separation
enforced by construction and plane separation enforced by hoping nobody joins.

**Why it is recorded as a correction.** The notes' appendix already lists three
2026 upgrades to the 2024 sketch (plain hashes → salted keyed commitments; an
on-chain encrypted PII database → a permissioned plane with anchored state roots;
per-access public entries → signed leaves with batched anchored checkpoints).
This is a fourth, found while carrying the meta-analysis lane forward, and it is
named as a correction to a vendored source rather than folded silently into a
requirement — the source is Brett Heap's own design sketch, and a packet that
quietly improved it would leave him no way to see that it had.

**AMENDED 2026-08-30, SECOND BOT ROUND — CODEX P1: THE CORRECTION HAD LEFT THE
LANE WITH NO LAWFUL JOIN AT ALL.** Refusing the stable shared key closed the
join-key defect and, with it, the only correspondence the named meta-analysis
consumer had between a demographic row and a record row: person linkage lives
only in the identity plane, the shared key is prohibited, and an analysis
excluding the identity plane could therefore inspect two datasets side by side
and correlate nothing. **The requirement named a first-class use case its own
refusals forbade** — an unachievable-by-construction obligation, which is the
family the 2026-08-28 convening unanimously refused a class over, and it is
worse than the hazard it replaced: a stable key is a hazard an implementer can
see, while an impossible requirement is one they satisfy by quietly inventing
that hazard back.

**The mechanism, defined in neutral terms because the shape is neutral and the
occasion is not.** Correlation runs only through an AUTHORIZED, SCOPED LINKAGE
DERIVATION — issued BY THE IDENTITY PLANE under an ANCHORED CONSENT CHECKPOINT,
PER-ANALYSIS and never stable, EXPIRING and REVOCABLE, usable only inside the
authorized analysis, with issuance and use written as leaves. The stable shared
key stays refused, and a derivation minted outside the identity plane, without a
consent checkpoint, or re-used across analyses is refused as that key wearing a
different name. **Q6's ruled pattern is the precedent, not an invention here**:
the ruling already puts a PHI portion *"disclosed OFF-CHAIN under an anchored
consent checkpoint"*, and this applies the same governed-authorization shape to
a join instead of to a disclosure. **Requirement 9's boundary is untouched** —
the neutral family says what a lawful correlation path must BE; the domain
overlay says when a lane may be authorized and against what standard, because
those are domain law.

**AMENDED IN THE THIRD BOT ROUND — issuance authorizes, it does not immunize.**
Making the derivation revocable and consent-gated collided with requirement 8's
standing promise that the result is *"unaffected by whether the identity plane
was reachable"*: requirement 6 refuses a consent-dependent act outright in
exactly that state, so an implementation had to either bypass a fresh revocation
or break the availability promise. **Reconciled by separating the two things the
promise had been conflating.** The UNCORRELATED analysis needs no derivation, no
consent evaluation and no identity plane, so it is genuinely unaffected — and
that is all the headline ever claimed. The JOIN is consent-gated end to end:
every USE answers to the CURRENT revocation state, and where that state cannot
be read the CORRELATION is refused, on the consent requirement's own doctrine
that an unevaluable answer never reads as permission. The refusal is scoped to
the correlation rather than to the run, so an analysis returns its per-plane
results and names the part it could not perform.

**AMENDED 2026-08-30 BY A BOT FINDING THE DISPOSITION FOLDED INTO THIS FIX ROUND
(disposition §4, item 14) — and it crosses because requirement 8 carries this
lane.** Codex, reviewing the vendored notes on pull request #509, found that
querying the record and demographic planes WITHOUT the identity plane does not
make the result de-identified: the attributes that remain can single out a person
and can link back to a record, and the estate requires a NAMED de-identification
determination rather than an assumed one
(`docs/knowledge-lifecycle-model.md`, the de-identify gate — *"the privacy
boundary … a named gate, not an assumed property"*). Describing the lane as
*"already supported"* could let a realization treat the output as reusable and
bypass that boundary. **The consequence taken here**: requirement 8 now states
what plane separation DOES buy (no direct identifier, no cross-plane join key,
the identity plane not required) and what it does NOT (a de-identified result),
refuses the de-identified label on the strength of separation alone, and leaves
the determination to the DOMAIN OVERLAY — this capability naming no standard for
it, since a determination standard is domain law and naming one would breach
requirement 9. **This is the crossing the
disposition names**: a privacy-boundary claim corrected in #509's brainstorm
colour and left standing in this packet's requirement text would reproduce the
error in governed text, which is LQ-A5's failure mode exactly.

## D8 — An anchored checkpoint witnesses the LOG, it does not validate a LEAF

**Raised by Codex on this packet's own pull request, and it is a real
contradiction in the first draft.** Requirement 4 promised that no unvalidated
material reaches a chain while requirement 4's own second block had the
transparency log written immediately, refusals included. Against an APPEND-ONLY
log those cannot both hold: every signed tree head commits to the whole prefix,
so a checkpoint anchored at any later time necessarily commits to the refused
leaf as well. **No amount of anchoring late can exclude an earlier leaf from a
prefix.** The rule as written described a control that cannot run.

**The resolution is to name two anchors rather than to weaken one rule.**

| | **Item anchor** | **Log checkpoint anchor** |
| --- | --- | --- |
| Commits to | a specific piece of material | the log's whole prefix, by construction |
| Governed by | the anchor-late rule — gate-passed material only | nothing can hold it back; the prefix is the prefix |
| Claims | that THIS material existed unchanged at this time | that the LOG SAID this at this time |
| Says about validity | that the material passed its gate | **NOTHING**, and the contract text says so |

A checkpoint covering a refusal leaf is not a leak — it is evidence that the
refusal happened, which is the whole point of an evidence plane. What would be a
defect is a reader taking inclusion for validation, so **inclusion in an anchored
checkpoint is never read, presented or verified as validation**, the checkpoint
record carries that disclaimer in its own contract text, and a surface that
breaks the rule is refused.

**AND THE NARROWING IS RECORDED RATHER THAN APPLIED SILENTLY.** The staged
topic's constraint reads *"anchoring LATE (commit only what has been
validated)"*. Taken literally that is unachievable against an append-only log,
and this packet narrows it: the constraint governs ITEM anchors, and what it
PROTECTS — that a false attestation must not become permanently backed by a chain
as valid — is honoured by the split plus the never-read-as-validation rule. A
topic's constraint is not a packet's to quietly reinterpret, so the narrowing is
in the requirement text, here, and in the pull-request record.

**AND RECORDING IT WAS NOT ENOUGH — IT IS NOW ROUTED, WHICH IS THE OTHER HALF.**
The constraint is the staged topic's, at
`ideation/staging/signed-execution-chain/signed-execution-chain.md:471-478`, in
its `## Conflicts` section — where two of the three conflicts carry disposition
stamps and this one does not, and none of the topic's seven Q-dispositions
reaches it, so **a constraint sitting inside a fully-ruled topic was not thereby
ruled**. This packet narrowed it and put six authoring decisions to its council
(`tasks.md:2.2`) WITHOUT this one; the convening had to add it as ballot **C-1**.
It was then RULED at disposition item 6 — **(i) correct and faithfully
recorded** — and the ruling produced a standing rule for future packets: **a
packet that NARROWS a constraint carried in a staged topic SHALL ROUTE the
narrowing to its council as an explicit decision, not merely RECORD it in its own
text** (`review/disposition-2026-08-30.md` §3.1;
`review/council-review-2026-08-30.md` §8.1). The rule is this packet's own
sentence, now binding — and it is a process obligation on future packets, **not**
a defect finding against this narrowing, which stands.

**Rejected: a second, validated-only tree whose checkpoints are the anchored
ones.** It would satisfy the literal constraint, and it would cost a second log,
a second tree head, and a permanent question about which of two logs is the
record — reintroducing the two-records-of-one-decision defect the family keeps
refusing. It also loses the property that makes an evidence plane worth having:
that refusals are IN it.

## D9 — A header is not canonicality, so the receipt carries a fourth element

**Also raised by Codex, and also a control that could not run as first
written.** Transaction bytes plus an inclusion proof establish that the
transaction sits under the Merkle root of THE SUPPLIED HEADER — and nothing
else. A fabricated or non-canonical header satisfies the first three elements
perfectly. The receipt shape as drafted could therefore be satisfied without
proving either witness, which is the same class of defect as the header-plus-bare-
reference shape the requirement already refused; the draft caught the first
instance and missed the second.

**The fix: a fourth per-chain element.** CHAIN-ACCEPTANCE EVIDENCE — for a linear
chain, the block height plus the header-chain linkage a verifier checks against
an independently obtained canonical header set; for a DAG, the DAG-acceptance
proof for the anchoring block — together with a NAMED, INDEPENDENTLY OBTAINABLE
HEADER SOURCE the verification runs against. The study's own note that
OpenTimestamps stays verifiable against a header chain is the ground.

**AND THE LIMIT IS STATED RATHER THAN OVERSOLD.** A receipt cannot carry a whole
chain, so the packet does NOT claim a receipt is self-sufficient against a forged
history. What it claims is that a receipt is CHECKABLE against a canonical header
set the verifier obtains for itself — so the trust root is a public chain the
verifier can independently reach, never a header this capability handed it. A
verification performed against a header source supplied by the receipt's own
minter is refused, because it proves self-consistency and calls it canonicality.

**What this does NOT change.** The pruning argument stands exactly as it was:
the TRANSACTION is the thing a pruning chain will not return, so the receipt
carries it. The header SET is the one thing a verifier always fetches for
itself, and fetching it from the minter was never the design — it was simply
unstated, and unstated is how an implementer ends up doing it.

## D10 — The audit obligation is scoped to what the factory SERVES

**Raised by Codex on the fix round, and it is the third control in this packet
that could not run as written.** Requirement 7 demanded a signed leaf for every
verification attempt. Requirement 1 exists to let a holder check a receipt
WITHOUT contacting the minter, and its scenarios say so. Put together, the audit
requirement demanded a record of events the factory has no way to observe —
**there is no request to serve, no surface to instrument, and no honest way to
write a leaf for something nothing here can see.** A completeness claim over
verifications-anywhere was unsatisfiable, and worse, it made the log look
complete when it could not be.

**The decision: scope the obligation honestly, and name the unobservable half as
a property rather than a gap.** The requirement covers the SERVED surface — this
capability's own verification surfaces, the permissioned plane's access
decisions, attempts against material the factory holds. An independent local
verification produces no leaf, none is claimed, and the absence is **not**
non-conformance. That invisibility is what *"the receipt's trust root is a
public chain the verifier can independently reach"* MEANS when it is true.

**Rejected: an authenticated reporting obligation on independent verifiers**,
which Codex named as the alternative. It would make the minter's reachability a
precondition of verification again — undoing D9 and the whole receipt-first exit
path — and it would collect the who-verified-what trail requirement 7's own last
paragraph works to keep off a public ledger, merely relocating it to the minter.
An unobservable verification is the correct outcome.

**And the scoping is what the SOURCE said**, which is worth recording because
this packet got it wrong first. The MedxChain notes log *"every access attempt to
the … data"* and *"views, edits, failed access attempts"* — mediated access —
and ask the neutral family for *"a generic verification-ATTEMPT scenario
alongside the successful-access case"*. **The over-reach was this packet's own
generalization**, so this is a correction to requirement 7's carrying of its
source and NOT a fifth correction to the source itself.

## D11 — The timing model is ONE model, and that is unify-don't-patch at design scale

**Ruled by Brett Heap, 2026-08-30, item 6a of the closing queue.** Not by the
tripwire this session had armed — that tripwire was defined to fire on a further
clock-area defect from a tenth bot round, **and the tenth round never ran**
because the reviewing bot reached its usage limit. The consolidation is
therefore performed on his word, and the distinction is recorded because a
ruling and an automatic trigger are different authorities.

**THE DEFECT WAS THE SHAPE, NOT ANY OF THE RULES.** Rounds six through nine each
found a timing defect and each added its repair where the defect surfaced: the
receipt's mint-time block, the state requirement, a scenario set, then the
clock. By round nine the model lived in **eighteen normative paragraphs across
two requirements**, carrying three separately-established bounds, two declared
widths, a cadence, a closure rule and two verifier modes. **Three consecutive
rounds then found DIRECTION ERRORS** — a header time asserted as an upper bound
it never was, a checkpoint bound read the wrong way, a margin applied to the
wrong side. A model nobody can hold whole is exactly the object in which an
inequality points the wrong way and no reader notices.

**So the family's own rule applies at design scale.** *Unify, don't patch, on a
defect's second appearance* was learned on code; this is its third appearance in
prose, and the answer is the same — **the family's home is rebuilt rather than
extended again.** The receipt requirement now carries THE TIMING MODEL as one
delimited section: the three clocks and only three, every bound as an explicit
inequality with its direction stated, every width with the reason it exists and
the authority it cites, the three decisions and the one-directional margin they
share, a closed table of what each verifier mode may and may not conclude, and
the closure rule. Every other timing paragraph in the packet is now a REFERENCE
to it.

**SEMANTICS CHANGED NOWHERE, AND THE PROOF IS THE SCENARIO SET.** Round ten never
ran, so nothing new was learned that could justify a semantic change; this is
**restructure-with-proof**. The scenario set is the accumulated adversarial
knowledge of nine rounds, so the consolidation was checked against ALL of it:
**every clock-relevant scenario is satisfied by the consolidated statement, and
NONE was overturned** — no scenario needed rewriting, which is the strongest
available evidence that the restatement is faithful rather than merely tidier.
The eleven paragraphs it replaced are recoverable from this branch's history.

**WHAT IT DOES NOT DO.** It fixes no defect, because none was outstanding. It
adds no requirement and no scenario. It does not touch the ruled configuration,
the boundary, or anything Q2/Q3/Q5/Q6 decided. **A reader who preferred the
scattered form loses nothing but the scattering.**

## Realization dependencies — what this tranche actually waits on

**A ruling is not what holds this tranche.** The topic's exit path says so:
*"What still holds this tranche is the PKI plane being real, not a ruling."*
Recorded here in dependency order, so realization is commissioned against facts
rather than against optimism.

| Dependency | State | What it gates |
| --- | --- | --- |
| **`add-signed-execution-chain` (tranche one) realized** | RATIFIED 2026-08-29; realization is a later commission | The TRANSPARENCY LOG. This capability writes leaves into it and anchors checkpoints of it; with no log there is nothing to anchor. Hard prerequisite. |
| **The PKI plane — `implement-openxpki-install-repo`** | 22 done / 8 open | The signing identities the anchoring subsystem itself uses, and the certificate chain tranche two needs. The topic names this as what holds tranche three. |
| **`add-chain-attestation` (tranche two)** | IN FLIGHT beside this packet | Not a hard prerequisite for anchoring a checkpoint, but the attested chain is most of what is WORTH anchoring — anchoring a log of unattested leaves witnesses less than the family intends. Sequencing, not blocking. |
| **The archival node for the operational witness** | Operator infrastructure, not yet commissioned | Requirement 2's first condition. Without it, the inclusion proofs cannot be captured before pruning and the witness cannot be used at all. |
| **The aggregation-calendar path for the durability witness** | Operator decision: public calendars, or a self-run hourly calendar | Requirement 2's durability half. The study's §8 cost model puts the public path at $0 marginal per item and a self-run hourly calendar at ≈$2.1k/yr. |
| **The permissioned plane instance** | Class named, instance deliberately unselected (D5) | Requirement 6. Realization-time selection. |

**The three Kaspa conditions are realization tasks, not prose.** An archival
node; inclusion proofs captured AND retained at anchor time; corroborating
status, never sole. `tasks.md` §4 carries each one as its own task with its own
evidence, because a condition recorded only in a requirement is a condition
nobody is assigned.

## What this design does NOT decide

- **The digest algorithm and byte encoding.** `add-signed-execution-chain`'s ONE
  digest construction requirement already reaches forward to *"any digest a
  later tranche adds"*. This packet declares no second
  digest rule and inherits that one; the algorithm is settled in tranche one's
  own §3 settling tasks.
- **The leaf grammar** for the new leaf kinds (verification attempt, refused
  access, anchor state, horizon breach). Tranche one owns the leaf grammar and
  settles it before schemas are authored; this packet names the leaf KINDS it
  needs and adds no second grammar.
- **The aggregation interval.** A realization-time tuning decision bounded by the
  horizons requirement 3 requires be DECLARED, not by a number written here.
- **Whether a future change may put contract code on an anchoring chain.** Q5
  refused the permanence and refused any trigger condition written in advance.
  This packet states today's evidence-only posture in the present tense and
  writes neither a "never" nor a condition. A later change answers to its own
  evidence.
- **Any domain's record kinds, regulators or product surfaces.** Requirement 9,
  and it is a refusal rather than a deferral.
