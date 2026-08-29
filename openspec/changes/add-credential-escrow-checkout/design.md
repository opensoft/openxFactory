# Design: add-credential-escrow-checkout

Six questions. § 1 is why the scope split lands where it lands and what the
first packet must contain to be worth splitting off. **§ 2 is the one decision
that departed from what Brett ruled — no schema here — and it was VETOED on
2026-08-28; it is rewritten as vetoed-and-reversed, with the authored argument
kept beneath because a veto is only readable against what it overturned.** § 3 is
why the checkout needed no new record kind — the authored § 2's load-bearing
claim, which SURVIVED the veto as a true statement that stopped being the
governing one — and § 3.5 is new: what the schema now carries, and why the entry
shape is the prior art rather than an invention. § 4 is the policy window, derived from the detection
mechanism rather than chosen. § 5 is the recipient topology and the one thing it
costs. § 6 is what makes a drill a drill.

## 1. Why the checkout comes first, and what it has to contain

Brett ruled the split (D) with a stated purpose: so that
`deployment-handoff-boundary`'s standing-admin exception can close. That purpose
is the design constraint, and it decides the packet's contents exactly.

The boundary's exception is held open by one clause —
"until the break-glass checkout path is realized and tested"
(`openspec/specs/deployment-handoff-boundary/spec.md:122-135`). Working
backwards from what would satisfy it:

- **"Tested"** is not "specified". A capability that only describes a checkout
  leaves the exception exactly as open as it was. So this packet's archive gate
  must be a performed act, not a merged document — hence the drill (requirement
  6), and hence `code_surface` is not `none`.
- **"The checkout path"** is the authorization, the evidence, and the aftermath.
  The boundary's own no-standing-credentials requirement already names all three
  in one sentence — "a time-boxed credential checkout with evidence, followed by
  a retroactive request within the governing policy window" — and leaves all
  three undefined. Requirements 1, 2, 3 and 4 are that sentence made
  enforceable, in its own order.
- **The recipient rule (5)** is here rather than in the registry packet for one
  reason: a checkout is a decryption, and which identity can decrypt is the
  checkout's own topology. Ruling B is about who can open the box, not about
  what is in it.
- **The re-mint test (7)** is here because Brett confirmed it with D rather than
  with A, and because it decides whether a given credential's loss is even a
  break-glass event.

Everything else in the staged topic — the inventory, the one-to-one
`vaultref://` mirroring, the completeness obligation, the drift audit, the
validator, the repository-policy carve-out, the registry home — is about the
BOX. None of it is needed to prove the checkout works, and all of it is needed
to prove the registry is complete. That is a clean seam, and it is the seam
Brett's ruling D drew.

## 2. VETOED AND REVERSED: the schema comes into this packet

**RULING, 2026-08-28, over PR #479.** OD-2 is vetoed. The `escrow:` relationship
block on `xfactory_credential_binding_template` AND the escrow-entry record kind
come into THIS packet, on ruling A's literal shape. Brett accepted the stated
consequence: realization now owes the additive contract cut. OD-3's deferral of
ruling C — the registry home, the grandfathered openxpki exception, the three
escalation tests — expressly STANDS; only the schema half moved.

**Why the veto is right on its own terms, stated before the history.** The
authored argument (below) was that the escrow entry is half of a relationship
whose other half is not here. That is true. What it under-weighted is that
**ruling A is itself the other half's design decision** — Brett had already ruled
the entry's shape ("inventory + restore target, shaped on the running prior
art"), so its fields were not open questions waiting on the successor's registry
work. They were settled, and deferring settled content to a later packet buys
nothing and costs a round trip. The successor's genuinely open work — where the
registry LIVES, whether every credential HAS an entry, and how a lint reads the
estate — none of it constrains what an entry CONTAINS.

**And the veto makes the successor's lint possible earlier.** That lint is only
buildable if the entry is non-secret metadata BY CONTRACT rather than by
convention. Requirement 9 now states that property where it can be enforced,
instead of leaving it to the lint's author to preserve by discipline.

**What the veto costs, recorded honestly.** A contract cut this packet did not
previously owe, and a wider realization: the schema, its validator and the
fixtures now stand between the merge and the drill. `tasks.md` § 5 is unchanged
in substance but now sits behind a § 4 that grew.

**THE AUTHORED ARGUMENT, KEPT AS HISTORY.** As filed, this section read:

> Ruling A says the shape is an additive optional `escrow:` block on
> `xfactory_credential_binding_template` plus one new record kind for the escrow
> entry. Ruling D says the checkout may introduce them "if the checkout path
> needs them to be testable". This packet introduces neither, and the honest
> framing is that this is a DEPARTURE FROM THE DEFAULT READING OF A, permitted by
> D and flagged as OD-2.

**The alternative, argued fairly.** Introducing the escrow entry kind here would
let this packet's fixtures name a real escrow object, would let requirement 2's
enumeration point at a typed thing rather than at "every escrow object
decrypted", and would let the drill in requirement 6 be described against a
declared restore target instead of "its declared restore target". Those are real
gains and they are not nothing.

**Why they lose anyway.** Three measured reasons.

1. **The entry is half of a relationship and the other half is not here.** The
   trust-anchor ruling this shape descends from says escrow is "a relationship
   on the credential record". A relationship record whose registry, inventory
   semantics, completeness rule and home are all in another packet is not a
   contract; it is a stub whose fields are guesses about the successor's design.
   The `contracts/manifest.yaml:2477` consumption rule for the chain-custody
   registry states the same thing from the other side: escrow was excluded from
   that registry precisely BECAUSE it belongs on the credential record — and the
   credential record's escrow block is meaningful only once there is something
   for it to point at.
2. **Landing it here forces the successor to MODIFY days-old canon.** The
   successor owns inventory and restore semantics; those are exactly the fields
   the entry kind carries. A kind promoted now would be promoted with fields
   nobody has yet designed against a completeness rule, and the successor's first
   act would be to change it. Churn on a schema is worse than delay on one,
   because consumers pin schemas.
3. **The checkout does not need it** — § 3.

**What is carried instead, so the relationship is not dangling.** Requirement 2
requires the enumeration STRUCTURALLY ("every escrow object decrypted") rather
than by field name, and requires it through the promoted audit policy's
`minimum_fields`. When the successor names the entry kind, the enumeration
becomes a list of typed references without this packet's text changing a word.
That is the property that makes the deferral safe rather than merely convenient.

**How that authored design fared under the veto — the part worth keeping.** The
structural phrasing was written to survive the entry kind's arrival "without this
packet's text changing a word", and the arrival came the same day rather than a
packet later. **The text did not change a word.** Requirement 2 reads exactly as
filed and now resolves against a typed kind, and OD-7 stayed cleared because the
enumeration never needed to move into the schema. A design defended as
future-proof was tested almost immediately, which is more than most get.

## 3. Why the checkout needed no new record kind — TRUE, AND NO LONGER GOVERNING

The claim the authored OD-2 rested on, stated so it can be checked — and it does
check. **The veto did not refute it; it out-weighed it.** The checkout path
genuinely is expressible in the five promoted kinds, which is why the seven
authored requirements needed no schema and still need none. What the veto decided
is that ruling A's content was already settled and had no reason to wait, not
that this table is wrong. Kept in full, because a reader who later asks "could
the checkout have shipped without the schema?" deserves the measured answer,
which is yes.

**The escrow decryption identity is itself a credential**, and the five promoted
record kinds already carry it end to end:

| The checkout needs | Promoted kind that carries it |
| --- | --- |
| a declared identity with a purpose and a scope | `xfactory_credential_requirements` |
| where its private half durably lives (an approved secret provider) | `xfactory_credential_binding_template` (`provider`, `secret_ref`, `owner`, `rotation_policy` — all already required) |
| a time-boxed, scope-named checkout with issuer, approver, expiry and audit reference | `xfactory_runtime_capability_grant_template` (all four fields already required, and a grant lacking one is already invalid) |
| an audit record naming what the checkout opened | `xfactory_credential_audit_policy`, whose `audit.minimum_fields` is an open array of required field names |

The last row is where the argument could have failed, and it does not: the
decrypted-object enumeration is a FIELD REQUIREMENT, and the promoted audit
policy kind exists to declare field requirements. Requiring it needs a
requirement, not a schema.

**The one thing genuinely absent** is a typed handle for "the escrow object". The
requirements are written to survive its arrival (§ 2), and until it arrives the
enumeration is a list of references the audit record already accommodates
(`evidence_refs` in the credential access audit shape at
`docs/credential-access-model.md:336-357`). **AND THEN IT ARRIVED.** The OD-2
veto supplies exactly this handle — `xfactory_credential_escrow_entry` — so the
one genuine absence the authored design admitted is the one thing the veto
filled.

## 3.5. What the schema now carries, and why the entry shape is not invented

**The MODIFIED block is surgical, and its size is the point.** A promoted
requirement enumerating FIVE record kinds becomes false the moment a sixth
exists, so the block restates that requirement with six, adds the sixth name, and
adds one closing paragraph declaring both additions additive. Two of the six
promoted scenarios carry "five" in their own text and are amended to "six" — the
ONLY promoted words that move. Two scenarios are added, and they are added to pin
the property the whole cut depends on: a binding predating the block still
validates, and the sixth kind is a contract record rather than a domain policy
record skipped with notice. Those two scenarios are what make "additive" a
testable claim rather than a promise in a changelog.

**The escrow block names three things and refuses a fourth.** The entry it refers
to, the scope, and the MUST/SHOULD classification with its retained authority. It
carries no value, no recipient private half, and no restore instruction — those
are the ENTRY's, and splitting them this way is what keeps the binding readable
at the point of use. The refusal it enforces is Brett's trust-anchor ruling: no
custody or assurance axis may carry an escrow discriminator, because escrow
answers "who else can obtain this" and a custody axis answers "can the using host
read it". The family already holds the executable proof of what conflating them
costs — the negative fixture in which the escrow member is forced to declare
exactly the same two booleans as the member above it, differing only in something
the axis cannot express.

**The entry shape is the running prior art made neutral, and that is a
methodological choice worth defending.** `Opensoft-Tenant-openxpki-qa` has been
carrying `escrow/**/inventory.yaml` and `restore-map.yaml` in service:
`source.credential_requirement` with a non-secret fingerprint, `runtime_target`
with vault coordinates and secret name, `escrow.format: sops-age` with `file` and
`encrypted_fields`, and a restore map whose `validation` includes
`prohibit_plaintext_git_material`. Requirement 9 generalizes THAT rather than
designing a fresh record, because a contract invented ahead of practice is a
guess and this one has already survived contact with real disaster-recovery
material.

**One property does all the successor's work: every field is non-secret
metadata.** Field NAMES are metadata; field VALUES are not. That single line is
what makes a decryption-free lint possible at all — entries exist, recipients are
the declared ones, no plaintext is present, every entry has a restore target, all
checkable with no decryption capability anywhere in CI.

**And the derivative rule closes the gap the runtime store creates.** A vault
legitimately holding only a hash does not discharge the escrow duty, because a
hash restores nothing. This is the QA dashboard htpasswd case from the staged
topic's claim 5, promoted from an example into a rule.

## 4. The policy window, derived rather than chosen

The full derivation is in `proposal.md` § The policy window this packet sets.
Three design points that belong here rather than there.

**The bound is set by the detector, not by comfort.** The boundary's
out-of-band detectability requirement turns an uncorrelated change into a
first-class finding at a PERIODIC audit. That gives an objective test for the
opening bound: it must be shorter than the audit period, or conforming
break-glass generates findings and the finding class loses its meaning. This is
the same reasoning the family already applies to standing maintenance requests —
a per-period standing request exists so that cadenced work does not manufacture
approvals — applied to the detection side.

**Non-tolling is a schema fact, not a strictness preference.** The
`client_infrastructure_request` contract documents `conditions` as
"orthogonal to `status`: overdue / escalation / holds coexist with the workflow
state and are never expressed as a status value"
(`contracts/schemas/xfactory-client-infrastructure-request.schema.yaml:234-241`),
with `overdue` and `awaiting_external_response` among the members and each
condition carrying `policy_ref`, `cleared_by` and `evidence_refs`. A tolling
window would need a second, competing mechanism for the same fact. Using the one
that exists keeps the wait VISIBLE, which a tolled clock does not.

**Lateness is a finding, not a void.** The alternative — a late request is no
request — has a perverse incentive at its centre: once the bound passes, filing
becomes strictly worse than silence. The rule chosen keeps the account and
records the lateness separately, so the incentive points the right way.

## 5. The recipient topology and its one honest cost

Ruling B, and what it buys.

**Two recipients, minimum.** One per-client escrow recipient and one operator
root on every object. One recipient alone fails in one of two ways: per-client
only means a lost key is a lost client; root only means every routine recovery
goes through the widest key, which is the thing you least want to normalize.

**Disjoint from every runtime decryption controller.** This is the promoted SOPS
requirement's "recipients are unique per environment or stronger trust boundary"
clause applied, with escrow as the stronger boundary — and the reason escrow IS
stronger is asymmetric in a way worth stating: the runtime store deliberately
holds derivatives where escrow holds recoverable values. The QA dashboard's
htpasswd HASH lives in the vault; the PASSWORD is what escrow must hold. A
recipient that decrypts both would make the runtime controller's compromise a
compromise of the recoverable values, and the same promoted requirement already
defines a controller compromise as compromise of everything that controller can
decrypt. The rule is therefore load-bearing rather than hygienic.

**It costs nothing operationally**, which is why it is enforceable: escrow WRITES
need only the committed public recipient, so separating the recipients never
makes a routine act harder. The only act that touches a private half is the
checkout, and the checkout is the thing being governed.

**The cost that is real, recorded rather than hidden.** The operator root appears
on every client's objects, so its worst-case blast radius is every client. That
is the price of surviving a lost per-client key, it was accepted at the ruling,
and requirement 5's fourth scenario makes recording it an obligation rather than
a footnote. OQ4 asks the follow-on question the ruling did not settle: how the
root's own private half is held.

**The separation already holds in practice**, which is the strongest evidence
that it is affordable: `Opensoft-Tenant-openxpki-qa`'s
`escrow/recipients/age-recipients.txt` carries two recipients, and neither is the
QA Flux reconciler's recipient in `Omnigent-Install/.sops.yaml`. The rule writes
down a decision the operator already made correctly and could otherwise lose.

## 6. What makes a drill a drill

A gate that a document can pass is not a gate. Requirement 6 is written as an
enumeration of exercised things for that reason, and each element excludes a
specific way of passing without proving anything:

- **A fresh clone with no prior local state** excludes a rehearsal that quietly
  depends on a decrypted artifact or a cached identity already on the operator's
  machine — which is the state a real disaster does not have.
- **A REAL approval-and-grant cycle** excludes a simulated approval. The
  authorization path is half of what is being proven; a drill that skips it
  proves the cryptography and nothing about the governance.
- **AT LEAST ONE LIVE REFUSAL** excludes a rehearsal that walks the happy path
  and infers the rest. This element was NOT authored — it arrived with OQ5's
  ruling of 2026-08-28, which went against this design's own recommendation that
  refusals be left to the negative fixtures. The argument that beat the
  recommendation is short and correct: the element above proves that the
  authorization path was FOLLOWED, and nothing in the authored list proves it
  would have BITTEN. A path observed only to permit has been shown to work and
  not shown to govern, and a fixture proves the schema refuses, not that the
  live grant surface does. The natural instance is a checkout attempted with no
  recorded human-and-domain approval.
- **At least one object decrypted AND verified against its restore target**
  excludes a decryption that produces bytes nobody checks. Recovering the wrong
  value successfully is the failure this catches.
- **The full evidence set, the rotation, and the retroactive request inside the
  window** exclude the most likely real-world failure of all: a rehearsal that
  proves recovery and skips the paperwork, thereby rehearsing the version of the
  procedure that leaves no account.

**One drill, two gates.** Its evidence is this change's archive gate and
`deployment-handoff-boundary`'s phased-never-gapped milestone. Nothing is
duplicated: the boundary's rule already says the exception closes when the
checkout is "realized and tested", so the drill IS its milestone rather than a
second artifact that references it.

**And the order is fixed by that same rule**: standing access is never removed
before the drill, and is removed on a dated milestone after it. Requirement 6's
third scenario states the failure in the other direction, because the eager
mistake here — removing standing access as soon as the contract lands — would
leave the family with neither a standing path nor a proven emergency one.

## Risks

**A drill that is run once and believed forever.** The gate proves the path
worked on one day with one operator. Key custody rots, password-manager items
move, and the operator who knows the runbook leaves. **OQ2 IS NOW RULED**
(2026-08-28, on the recommendation): the cadence is every escrow-identity
rotation plus at least annually, set in the successor alongside the rotation
runbook because rotation is what it is anchored to. The risk is not retired by
the ruling — this packet's own gate is still a point measurement, and the
cadence only starts binding when the successor states it.

**Thin approval at the first drill.** The opensoft tenant is a one-person
self-client, so the "human AND domain approval" requirement 1 imposes will be
satisfied by one person holding structurally distinct roles — the exact shape the
existing `thin-independent-approval` accepted-risk record already names for a
different scope. **OQ3 IS NOW RULED** (2026-08-28, on the recommendation): that
record is extended by an EXPLICIT SCOPE AMENDMENT covering escrow checkout,
never reused silently, and the amendment is a hard precondition of the drill
(`tasks.md` § 5.4). The ruling makes the thinness VISIBLE; it does not make the
approval thick, and the risk stands as written.

**A window nobody measures.** Both bounds are only real if something computes
them. The evidence-correlation audit that would compute the first is
`deployment-handoff-boundary`'s, and it is a realization obligation on
OpsxFactory rather than a thing this packet builds. Stated plainly: until that
audit runs, the window is a rule with a manual detector.

**~~Deferring the schema could strand the enumeration.~~ SPENT BY THE OD-2 VETO.**
As authored: "If the successor slips, requirement 2's enumeration stays a list of
untyped references for longer than intended. The mitigation is that it is USABLE
untyped — the drill can enumerate paths — so the deferral degrades rather than
blocks." The schema now lands here, so the risk is gone.

**The risk that replaced it: a wider realization before the drill can start.**
The schema, its validator and the fixtures now stand between merge and the
rehearsal, and the boundary's standing-admin exception stays open for all of it.
OQ5's ruling adds a live refusal to the drill on top. The honest reading is that
the veto bought a better contract at the cost of a later milestone, and that
trade was made with the consequence stated.

**A schema whose only conformant instances are fixtures.** Requirements 8 and 9
will be proven at realization by packaged examples, because the neutral layer
holds no escrow estate of its own — the same shape this capability's own
roster-drift precondition already uses and states in its promoted scenario. The
first REAL instances arrive with the Client Hermes records in `tasks.md` § 5, and
until then the schema is exercised rather than used.
