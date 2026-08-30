Seat: lead-security (domain seat) · Convening: gate_rules_council (§7.4 sitting), 2026-08-30
Packet: openspec/changes/add-chain-attestation/review/convening-packet-2026-08-30.md
Judged at: openxFactory main afe29561 / #510 e7f6ae0e / #513 cf5a24b8 / #509 26c7e778

# SEAT RETURN — `lead-security` (LS), domain seat

## 0. Persona declaration

My charter (codexFactory `hermes/domain/roles/lead-security.yaml`, read at
`sittingref` 3c71ddc9): `authority.owns: [security_posture, fail_closed_defaults]`,
`decides: [security_verdict]`, `escalates: {trigger: security_ambiguity, to:
park_for_liaison, then: council_large}`; `disposition: {rigor: high, risk_posture:
averse}`; `guardrail: character_never_overrides_authority`.

**Seat basis:** `members.domain`, the unconditional roster (packet §3.3). Model
inherited `opus`; I note without objection that the S5 target (R1–R4) is not in
force and the sitting followed the enrolled roster (packet §3.3).

**Assigned obligation:** packet §4 `lead-security` row (a)–(f) plus the EVERY SEAT
row (i)–(iii). **§3.2 expressly assigns me the exposure and supply-chain reading
the unseated `client-security-compliance-officer` would have carried.** I have
discharged that reading at the domain layer. I have **not** been able to supply the
client-layer voice on it, and I say so at T-0(b) and park exactly that.

**Boundary reading I take openly.** My charter reaches #509 only where the document
discloses something it should not (packet §1.3). I rule that limb and name the seats
for the rest. I do not rule A-1/A-3/A-4 on their merits.

**My stored must-not is live.** Where I could not resolve a security question I have
parked it and named what resolves it. I have parked one item. Everything else I
ruled, because a seat with grounds rules.

**Checkout hygiene.** `git status --porcelain` was **EMPTY in all five trees**
(`invmain`, `inv510`, `inv513`, `inv509`, `sittingref`) **before and after** my work.
I wrote nothing to any checkout; my scratch lived in `seat-scratch-LS/`.

---

## 1. What I verified BY EXECUTION

### 1.1 Re-verification of the convening's two carried facts (§0.4, §0.7) — both CONFIRMED, my measurement agrees

I counted rather than read, with my own script (`seat-scratch-LS/count.py`):

```
== invmain .../add-signed-execution-chain/specs/signed-execution-chain/spec.md
    391 sc= 9 kw=OK  A gate validates the short chain as a hash-linked chain   <-- SUBJECT
  TOTAL reqs=9 scenarios=45
== inv510 .../add-chain-attestation/specs/signed-execution-chain/spec.md
  TOTAL reqs=9 scenarios=59
== inv513 .../add-chain-anchoring/specs/chain-anchoring/spec.md
  TOTAL reqs=9 scenarios=52
```

**§0.4 CONFIRMED.** Tranche one's gate requirement carries **NINE** scenarios, not
twelve; the whole delta carries **45**. #510's four "twelve scenarios" sites inflate
the cost of the alternative it argues against by a third. Both packets' own counts
(9/59 and 9/52) are **CORRECT**, and every requirement's first body line carries
SHALL (`kw=OK` on all 27).

**§0.7 CONFIRMED.** `invmain .../add-signed-execution-chain/tasks.md:187-190` reads
verbatim *"Re-derive the tranche two/three boundary against what actually exists
**when each is raised**"*. Grepping `"when each is raised"` and `"task 5.3"` across
both packets' `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`: **zero
citations** (the two `5.3` hits are the packets' own task numbering).

```
$ openspec validate add-chain-attestation --strict → Change 'add-chain-attestation' is valid
$ openspec validate add-chain-anchoring  --strict → Change 'add-chain-anchoring' is valid
```

### 1.2 #510's constitutional citation — EXECUTED against the schema, and it is EXACT

I loaded `invmain/contracts/omnigent/omnigent-domain-overlay.schema.yaml` and walked it:

```
$defs/worker_class/properties/permissions:
  type: object, additionalProperties: false
  required: [read_workspace, write_artifacts, run_validations,
             propose_admission, execute_final_action, access_secrets]
  execute_final_action: {const: false}
  access_secrets:       {const: false}
$defs/worker_class/properties/archetype.enum:
  [frame, generate, verify, challenge, assemble_for_admission]
```

#510's claim of a **closed six-boolean matrix, two `const: false`, five archetypes**
is accurate to the byte. Recorded in the packet's favour (§5).

### 1.3 SUBTRACTION on #510's tier-2 key rule (obligation b) — which removals still refuse

Conditions in requirement 4 (`inv510 .../spec.md:265-284`): **C1** key material out of
every worker/runner/lane, every configuration, every lifetime; **C2** realize as a
signing oracle, *"nothing else crosses the boundary"*; **C3** key bytes do not cross;
**C4** nor a dereferencing handle; **C5** nor a re-signing delegation; **C6** the
`access_secrets: false` ground.

| Removed | Still refuses? | By what |
|---|---|---|
| C3 key bytes | **YES** | C1 ("key material out") and C2 |
| C4 handle | **YES** | C2's "nothing else crosses" |
| C5 delegation | **YES** | C2 only — C1 does not reach a delegation |
| C2 oracle framing | **YES** | C4/C5 are separately enumerated |
| C6 the ground | **YES** | C1–C5 stand as SHALLs; C6 is justification |

The enumerated transfer modes are well defended in depth. **What no subtraction was
needed to find is what is not there at all.** Executed:

```
$ grep -rniE "co-locat|colocat|same host|same machine|isolat|trust boundary|
              network boundary|process boundary|separate host" inv510/openspec/changes/add-chain-attestation/
   (no output — ZERO hits across all 7 files)
```

**"In every configuration" enumerates HAND-OVERS and never REACHABILITY.** Every
refusal in requirement 4 is framed on a crossing — *"the breach is the crossing and
not the retention"* (`:302`). A controller process co-resident with the runner on a
self-hosted host, with a host-readable key, hands nothing across and is **conformant
as drafted**. Requirement 1's custody rule (`:22-25`) only *labels* such a key ("a
host-readable key evidences that the HOST acted") and bites solely where an assurance
demands hardware-bound custody — and **nothing in #510 demands one for tier 2**. This
is the exact shape of the family's own review lane (GitHub Actions runners). **LS-F3.**

### 1.4 SUBTRACTION on #510's attribution refusal — the P1-1 fix (obligations b, g)

`spec.md:110-114` — the fix: the controller **SHALL ATTRIBUTE** every request to the
task it provisioned, **SHALL REFUSE** what it cannot attribute, **SHALL cover the
attribution inside the signed bytes**. Nineteen lines later, `spec.md:123-133`:

> A realization SHALL therefore DECLARE … exactly what its platform lets the
> controller establish about a requester, and SHALL NOT assert an attribution
> stronger than that. Where a platform cannot distinguish two tasks the same
> controller provisioned, the realization DECLARES it and **the affected
> attestations are refused for uses requiring per-task attribution** — an undeclared
> shortfall is non-conformance, and **the identical shortfall declared is conformant**.

I then executed the only question that matters: **which uses require per-task
attribution?**

```
$ grep -rn "per-task attribution" inv510/openspec/changes/add-chain-attestation/
  spec.md:132  … refused for uses requiring per-task attribution — an undeclared …
  spec.md:181  … refused for uses requiring per-task attribution, the declaration …
```

**Two occurrences, both inside the escape clause itself. The set is never
enumerated anywhere in the packet.** So the mandatory refusal is dischargeable by
declaration, and what the declaration costs is undefined. Requirement 6's links 1–6
gate walk (`:422-431`) is **not** named as such a use. A realization that declares it
can establish nothing about a requester therefore runs an **unattributed signing
oracle**, passes the gate, and its link-5 records are refused only for a set with no
members. That is precisely the attack D10 P1-1 was raised to close (`design.md:290-297`)
— *"an opportunistic caller … could submit a payload that corroborates against link 4
and receive a signature indistinguishable from the provisioned task's"* — surviving
through the fix's own escape. **The P1 was repaired at the level of the record and
not of the control, which is the shape D10 itself names for all three.** **LS-F2.**

### 1.5 The P1-3 fix, driven to its instrument — MY STRONGEST #510 FINDING

`spec.md:519-527` requires link-10 closure to establish the review record was
produced under review authority **proven by possession**, *"its standing **current at
exercise**"*. I went to the shipped instrument rather than the prose:

```
$ head -25 invmain/governance/review-authority/register.yaml
# Q1c DESIGN CONSTRAINT, recorded here as ratified task 5.5 requires: a
# file-based register CANNOT satisfy revocation-at-exercise. Every
# distribution path is digest-pinned and lagging, so this file is an
# issuance-time snapshot; the conforming home for the REVOCATION SURFACE is a
# live lookup on the Hermes runtime (S5 successor). This file is right for
# the MVP's one row; it must not be pretended into a revocation surface.
```

```
$ grep -rni "revocation surface|live lookup|issuance-time|register\b|S5" \
      inv510/openspec/changes/add-chain-attestation/
   (no output — ZERO hits)
```

**#510 demands revocation-at-exercise from the one shipped instrument whose own
ratified text says it cannot provide it and must not be pretended into providing
it — and declares no shortfall for it**, though it declares two others (`:36-39`,
`:529-536`). By #510's own doctrine (*"an undeclared shortfall is non-conformance"*),
the packet is non-conformant to its own rule, at link 10, which the packet itself
calls *"the one link that has no gate behind it"* (`design.md:307-308`). A
bot-prescribed fix applied without running it against its instrument. **LS-F1.**

I also checked the vocabulary itself and **#510 is clean there**: `object_ref` is a
real shipped openxWallet exercise field, consumed by tranche one at
`invmain .../add-signed-execution-chain/specs/signed-execution-chain/spec.md:27`.
No vocabulary is invented. Recorded in favour.

### 1.6 The P1-2 fix, attacked (obligation g)

The fix derives the authoritative link-5 set from the log by a defined query and
requires EQUALITY (`spec.md:400-412`). I asked what fixes **who writes the leaf**:

```
$ grep -n "leaf" inv510/.../spec.md
  408, 409, 411, 412, 416, 468, 470, 472   ← all inside the P1-2 fix and its scenarios
```

Nothing in #510 obliges the **controller** — the only party trusted at that boundary
— to write the link-5 leaf. The fix closes *omission from the submission*; it does not
close *omission from the log*, and link 4 records the provisioned environment but no
count of expected runner tasks, so there is no independent cardinality to check
equality against. The packet declares tranche one's **suffix-truncation** residual
(`:414-420`), which is a different failure (a store dropping observed leaves) from a
leaf never written. **LS-F5.**

### 1.7 Evidence classes — the missing class (obligation c)

```
$ grep -rn "controller_corroborated|hardware_attested|runner_claimed|controller_claimed"
  → three classes only. controller_claimed: ZERO hits anywhere.
$ inv510/.../tasks.md:134-136
  4.2 Fix the evidence-class vocabulary's closure — whether … is a CLOSED set at the
      schema, and what a fourth class would have to establish.
```

Requirement 3 says **"EVERY ATTESTED FACT SHALL CARRY ITS EVIDENCE CLASS"** and that
an unclassed fact *"is read at the strength of the strongest fact beside it"*
(`:228-233`). Link 4's own facts — model surface, harness, toolchain, workspace
provenance — are attested facts, asserted by the controller **about itself**, with no
corroboration source at all (link 4 is *the* corroboration source). There is no honest
class for them; the only fitting label is `controller_corroborated`, which overstates
by exactly the amount the requirement exists to prevent. The requirement refuses an
**empty** link 4 (`:73-77`) and never a **false** one. **LS-F4.**

### 1.8 #513 C-2 — MISSING WITNESS, driven (obligation a)

I read `455bbdaa` in full rather than the current text. **It fixed the collision, it
did not move it**: the resolution is by the receipt's own rule, not by an exception —
the per-chain list gains an entry only on whole capture, an in-flight witness lives in
the ANCHOR-STATE record, and completion **APPENDS** against the same digest. I confirm
`2e539779` correctly propagated the fourth element (chain-acceptance evidence) into
that same paragraph and its scenario (`spec.md:216`, `:265-269`), so the three/four
element mismatch the earlier commit would have left does **not** survive. Clean work.

Then I drove the three questions:

**Can a missing witness stop the factory?** No. `spec.md:190-192` — *"a witness outage
SHALL NOT block ratification, execution, review or any gate"* — with a scenario
refusing a proposal to hold the gate (`:253-257`). Correct, and correctly grounded: the
log is the evidence plane and an anchor is a late addition to it.

**Contrast with requirement 6 (unreachable permissioned plane).** `spec.md:486-492`
refuses a consent-dependent act outright. **The asymmetry is deliberate and I rule it
CORRECT**: a missing WITNESS degrades a claim about the past; a missing CONSENT ANSWER
refuses an act in the present. Those are different objects and the packet says so in
terms. I tested the seam for an act that is both — anchoring the consent plane's state
root — and requirement 6 routes it as *"an ordinary anchored item"* (`:506-510`), so it
degrades rather than refuses. The boundary is crisp.

**Can a claim pass with one witness where Q3 requires both?** I read Q3 in the topic
itself (`invmain .../signed-execution-chain.md`, round-2 disposition): *"BOTH witnesses
on EVERY anchored item … Kaspa FIRST … corroborating evidence, never sole … ten-year
claims cite Bitcoin … No selectivity … no third chain."* #513 requirement 2 carries
every clause faithfully. Requirement 3 admits a ten-year claim on the durability
witness alone when the operational witness is missing (`:235-239`). **I rule that
consistent with Q3, not a re-litigation of it**: Q3 governs what is ANCHORED (the item
stays `anchor_incomplete` and is never presented as anchored), and the ten-year claim's
ground is Bitcoin, which landed. The reverse — Kaspa alone as sole evidence — is
explicitly refused (`:167-171`). Evidentially sound.

**What a receipt asserts when the Bitcoin half is absent — and this is where it
breaks.** The 455bbdaa/Copilot split makes the receipt **stateless by design**: *"The
RECEIPT holds proof material and never state … carries no field describing what has not
happened yet"* (`:131-133`). The incompleteness therefore lives **only** in the
minter's anchor-state record. But requirement 1's entire purpose is that a receipt is
*"checkable against a canonical header set the verifier obtains for itself"* (`:40-42`)
— an artifact handed to an independent third party. **A one-entry receipt in a third
party's hands is byte-indistinguishable from a receipt minted under a one-witness
configuration.** The holder cannot tell "durability-only because the operational
witness was down" from "durability-only by design", and requirement 3's disclosure is a
service only the minter can run. **The fail-closed disclosure does not travel with the
artifact the design exists to make independently checkable.** That is C-2's real
answer, and it is a defect of composition between two individually correct
requirements. **LS-F7, BLOCKING**, and it is cheap to discharge without disturbing the
split, because the CONFIGURED witness set is configuration, not "what has not happened
yet".

**Vocabulary collision, stated with its charitable reading.** `spec.md:185-186`
introduces `anchor_pending` as the state on submission; `:181-183` says an item
carrying fewer witnesses than configured **is** `anchor_incomplete`; the proposal's
`code_surface` lists three states. Every healthy item is in both descriptions for hours
by design. Read charitably the opening SHALL governs and `anchor_pending` is a
sub-state, so the fail-closed verification answer **is** pinned — which is why I mark
this SHOULD-FIX and not BLOCKING. The residual harm is real but lesser: if a
realization reads `anchor_pending` as a distinct benign state, the verification answer
for the state every item passes through is unstated; and if it reads it as
`anchor_incomplete`, the operator-obligation signal fires on every healthy item and
becomes noise. **LS-F11.**

### 1.9 #513 capture-time completeness — no finality condition (obligation a, driven)

```
$ grep -rniE "reorg|re-org|confirmation|finalit|confirmed|depth" inv513/openspec/changes/add-chain-anchoring/
  → 4 hits, ALL of them `target_release` "CONFIRMED" bookkeeping or Q6 "CONFIRMED".
  → ZERO on chain finality, confirmation depth, or reorganization.
```

Requirement 3 makes a **CAPTURED RECEIPT the only path to complete** (`:229-232`), and
requirement 1 defines capture with no confirmation depth, no work threshold and no
finality condition. So an item becomes anchor-complete on a receipt captured at zero
confirmations. The later failure direction is safe (verification against the canonical
header set fails, fail-closed) — but it is **silent and permanent**: the item was moved
to complete, the operational chain prunes within ~3 days, and the material needed to
re-capture is gone. **LS-F9.**

### 1.10 #513 Q6 — the commitment reading, driven in both directions (obligation d)

I read Q6 in the topic (`signed-execution-chain.md`, Q6 disposition): *"SALTED KEYED
COMMITMENTS … portion disclosed OFF-CHAIN under an anchored consent checkpoint … salt
destruction as the erasure mechanism. Literal raw PHI, encrypted PHI and plain-hashed
PHI on chain stay REFUSED. No later change re-litigates this."*

**#513 holds it, and holds it by checks a validator can actually run.** Requirement 5
requires a DECLARED CONSTRUCTION (algorithm, keyed, salted) plus a SALT CUSTODY
REFERENCE, and refuses: no declaration; a construction that is not keyed and salted; a
salt custody reference resolving onto a chain or into the anchored record (`:390-400`,
scenarios `:436-452`). The payload refusal is **structural by field shape** rather than
semantic (`:379-388`), which reaches raw, encrypted and plain-hashed alike without
domain semantics — genuinely runnable and genuinely neutral. The declaration-vs-bytes
residual is raised as an explicit gap rather than claimed closed (`:402-411`). The
erasure claim is honest in the overclaim direction: it states the permanent
unverifiability **before** the act, and refuses any un-publication claim (`:325-330`,
`:413-422`, `:460-464`).

**Where it is not honest is the understatement direction, and it is two omissions:**

```
$ grep -rniE "entropy|unguessable|random|cryptographically" inv513/openspec/changes/add-chain-anchoring/
   (no output — ZERO hits)
```

1. **No entropy floor on the salt.** A declared "salted" construction with an
   eight-bit salt passes every check in requirement 5 and is brute-forceable. The EDPB
   ground the requirement itself cites (`:419-422`) is *precisely* the
   guessable-input-hash problem, so the mechanism is asserted against the exact
   attack its own citation names.
2. **No custody rule for the KEY of the keyed commitment.** Requirement 5 writes a
   custody reference and a reachability refusal for the SALT and **nothing at all** for
   the KEY. A realization may hold the commitment key on chain, inside the anchored
   record, or shared across planes, and no drafted check refuses it — while
   requirement 8 is careful to require per-plane keys under per-plane salts for the
   plane-separation case (`:602-611`), so the packet knows the shape and applied it in
   one place only.

Q6's erasure property is the authority for the whole narrowing. It presently rests on
two parameters the contract does not fix. **LS-F8, BLOCKING.**

### 1.11 The anchor-state record's own integrity (#513)

```
$ grep -rniE "anchor-state record" inv513/.../spec.md → :130, :213, :218, :245, :268, :275
```

It is described as *"where every surface reads it"* (`:130`) and as the authority for
per-witness status — and is **nowhere required to be signed, leaf-derived, or equal to
the state the log implies**. Its transitions are written as leaves (`:225-228`), so the
truth is reconstructible; nothing requires the record read by surfaces to **equal** the
reconstruction. This is exactly the defect #510's P1-2 fix names — *"an enumeration can
only be judged incomplete against an AUTHORITATIVE SET"* — unapplied in the sibling
packet to its own state record. **LS-F10.**

### 1.12 Live key material (obligation e)

```
$ grep -rniE "mint.* key|generate.* key|create.* key|private key|Ed25519|keypair" both packets
  → 2 hits, both the same doctrinal sentence: "A private key is a secret".
```

**Neither packet creates, moves or reads live key material.** Both declare it
explicitly: #510 `proposal.md` — *"NO CERTIFICATE AUTHORITY, NO issuance pipeline, NO
key service, NO HSM procurement"*; #513 `proposal.md:92` — *"no per-task identity, no
certificate authority"*. `contracts/` is untouched by #510's diff (7 files, +1741/−0,
verified by `git diff --stat`). **Obligation (e) discharged: clean, in both.** The
R12-adjacent per-seat Ed25519 keys minted 2026-08-28 are not touched, used or
referenced.

### 1.13 #509 disclosure reading (obligation f)

I read all 223 lines. **No credential, secret, token, key, PHI, patient data or real
identifier appears anywhere in it.** I confirmed the corpus this lands in is
externally projected:

```
$ grep -n "brainstorm" invmain/scripts/sync-notebooklm-books.py
  86: IDEATION_STATUSES = {"brainstorm", "staged"}      ← Status: brainstorm IS projected
```

So the document does reach a third-party SaaS. Two things worth naming, neither
blocking: (i) it publishes three unregistered candidate commercial domain names
(`myHIPPAA.com`, `HappyHIPPAA.com`, `HIPPAA.org`, `:28-29`) into an externally-synced
corpus — a business-confidentiality question, not a security one, and the owner's own
material; (ii) it describes an architecture that is itself unsafe (PIIDB *"entirely on
the blockchain, encrypted"*, `:54-56`; per-access public entries, `:57-59`) — but the
appendix **corrects all three explicitly** (`:139-169`), so there is no risk of the
2024 sketch being read as endorsed. **On my limb, #509 discloses nothing that should
not sit there.** **LS-F13, OBSERVATION.**

### 1.14 T-0(b), executed against the code rather than the packet's account

```
$ sed -n '1,70p' sittingref/scripts/merge_master/seat_resolution.py
  "It asks a DEFINITION-TIME question whose input contract is `rule_touched_paths`,
   no gather produces that fact … Evaluating it against pull-request facts to close
   the gap would make a definition-time answer stand in for a per-PR one, which the
   input contracts below exist to prevent."
  "Unevaluable NEVER means absent (Q11). A missing input, an incomplete fact set, or
   a predicate that cannot decide raises ConditionUnevaluable. The caller refuses the
   rule or parks the convening. It must never be read as 'the condition does not
   hold', because that silently drops a required seat."
```

**This sitting sets no rule, so `rule_touched_paths` does not exist for it.** The
convening fed the predicate pull-request paths (§3.2) — the precise substitution the
module's input contract exists to prevent. The honest result is
`ConditionUnevaluable`, **not `False`**. I reach that independently and by execution,
and it confirms the 2026-08-29 `lead-security` dissent. See T-0(b) and my park.

---

## 2. Findings

**LS-F1 [510] BLOCKING** — Link-10 closure requires the review grant's *"standing
current at exercise"* (`inv510 .../spec.md:523`, scenario `:566-570`) from an
instrument whose own ratified header says a file-based register **cannot** satisfy
revocation-at-exercise and *"must not be pretended into a revocation surface"*
(`invmain/governance/review-authority/register.yaml:19-25`). #510 declares no shortfall
for it (zero hits, §1.5) though it declares two others. Non-conformant to #510's own
undeclared-shortfall doctrine, at the link it calls the one with no gate behind it.

**LS-F2 [510] BLOCKING** — The P1-1 attribution refusal (`:110-114`) is fully
dischargeable by declaration (`:123-133`), and the set of *"uses requiring per-task
attribution"* is never enumerated — two occurrences, both inside the escape itself
(§1.4). The gate walk is not named as such a use, so a realization declaring it can
establish nothing runs an unattributed signing oracle and still passes the gate. The
fix repairs the record and not the control.

**LS-F3 [510] BLOCKING** — *"In every configuration"* (`:265-272`) enumerates
transfer modes only. Zero hits for isolation, co-location, trust boundary or separate
host across all seven files (§1.3). A controller co-resident with the runner on a
self-hosted host with a host-readable key hands nothing across and is conformant as
drafted; requirement 1's custody clause only labels such a key and bites only where a
hardware-bound assurance is demanded, which #510 never demands.

**LS-F4 [510] SHOULD-FIX** — The evidence-class vocabulary carries no class for the
controller's own uncorroborated self-report; link 4's facts have no honest label and
default to `controller_corroborated`. Closure of the set is an open task
(`tasks.md:134-136`). Requirement 1 refuses an empty link 4 and never a false one.

**LS-F5 [510] SHOULD-FIX** — The P1-2 authoritative set is authoritative only over
what reached the log; #510 never fixes who writes the link-5 leaf (§1.6), and link 4
carries no expected-task cardinality. Suppression at source is undetected, and it is a
different residual from the declared suffix-truncation one.

**LS-F6 [510] OBSERVATION** — *"The ground is constitutional and already shipped"*
(`:274-284`) is exact for omnigent **worker classes** (§1.2) and is #510's own
extension for runners and lanes, which the schema does not reach. Correctly stricter
than its ground; worth saying so rather than inheriting authority it does not have.

**LS-F7 [513] BLOCKING** — The receipt is stateless by design (`:131-133`), so a
one-entry receipt handed to an independent verifier — the flow requirement 1 exists to
enable (`:40-42`) — is indistinguishable from a one-witness configuration. The
`anchor_incomplete` disclosure lives only in the minter's anchor-state record. The
fail-closed disclosure does not travel with the artifact (§1.8).

**LS-F8 [513] BLOCKING** — Q6's erasure property rests on two unspecified parameters:
**no entropy floor on the salt** (zero hits) and **no custody rule for the KEY** of the
keyed commitment, where the salt has both a custody reference and a reachability
refusal (§1.10). The EDPB ground the requirement itself cites is the
guessable-input-hash problem.

**LS-F9 [513] SHOULD-FIX** — A captured receipt is the only path to complete (`:229-232`)
and capture carries no confirmation depth or finality condition (zero hits, §1.9). An
item can be complete on a receipt that will never verify, discovered only later, after
the operational chain has pruned the material needed to re-capture.

**LS-F10 [513] SHOULD-FIX** — The anchor-state record is the authority every surface
reads and is nowhere required to be leaf-derived, signed, or equal to the log-implied
state (§1.11) — #510's own P1-2 lesson unapplied in the sibling packet.

**LS-F11 [513] SHOULD-FIX** — `anchor_pending` / `anchor_incomplete` describe the same
condition in the healthy path (§1.8). Charitably the opening SHALL governs, which is
why this is not blocking; the residual is an unstated verification answer under one
reading and an operator signal that fires on every healthy item under the other.

**LS-F12 [X] SHOULD-FIX** — The `add-trust-anchor` declared-shortfall pattern is now
load-bearing at **five** sites across the two packets (#510 `:36`, `:127`, `:533`; #513
`:402-411`, and its realization conformance declaration) with **no floor written
anywhere**: no drafted text says what a declared shortfall disqualifies a chain or a
receipt from. A pattern that converts every unmeetable control into a conformant
declaration needs a floor, or it becomes the estate's general-purpose exemption.

**LS-F13 [509] OBSERVATION** — No credential, secret, key, PHI or identifier (§1.13).
Two non-blocking notes: three unregistered candidate commercial domain names enter an
externally-synced corpus (`IDEATION_STATUSES` includes `brainstorm`); and the unsafe
2024 architecture it records is explicitly corrected in the appendix, so it cannot read
as endorsed.

**LS-F14 [510] OBSERVATION** — R12's four S5 envelope questions (standard, key
distribution, signature algorithm, evidence-retention location) are unaddressed in the
attestation tranche, and R12's no-self-attestation rule bears on LS-F4. See B-6.

---

## 3. Positions on the ballot questions

**T-0(a)** — Within my charter only as it bears on fail-closed composition. **(i) this
council extends to it**, consistent with the 2026-08-29 LS position: a bench that owns
`fail_closed_defaults` is competent over objects whose whole content is fail-closed
rules, and refusing the seating would leave these three PRs with no bench at all, which
is worse than a disclosed stretch. I note the sanction was given for one subject and
this is three; see (c).

**T-0(b) — the CSC decline was WRONG IN ITS GROUND, and I now have the remedy the
2026-08-29 record left unresolved.** Executed at §1.14: this sitting sets no rule, so
the predicate's declared input `rule_touched_paths` does not exist; feeding it
pull-request paths is the exact substitution the module's input contract forbids. The
honest ground is **`ConditionUnevaluable`**, not `False`. Per the module's own words,
*"the caller refuses the rule or parks the convening"* — and there is no rule to refuse.
**The convening should have PARKED that determination rather than resolving it to
absent.** The substantive exposure reading was not lost, because §3.2 assigned it to me
and I discharged it. The **client-layer voice** on it was lost, and that is what I park.

**T-0(c) — answered honestly against the convening.** Three subjects degraded my
reading, and I can say where: I gave #509 a disclosure-limb pass rather than the
line-by-line provenance drive I would have given a single subject, and I did not drive
#510's requirements 6–9 by subtraction as I drove requirement 4. **It was lawful but
costly.** The one genuine argument for combining is §0.9 and it is real — #513's
requirement text cites a file only #509 creates, and I could not have judged those
citations without #509 in front of me. On balance: combining #510 and #513 was
defensible; adding #509 bought one real dependency at the price of attention.

**T-1 — my limb is the security limb: NOT PREMATURE (option a), with a caveat.**
Writing a refusal down before its enforcer exists is how fail-closed design is supposed
to proceed, provided the packet **declares** rather than **asserts** the enforcement —
and #510 does declare, at `tasks.md:5.1`, `:5.2` and in three explicit residuals. Q4's
own words bind the **boundary re-derivation**, and the topic's Exit path says tranche
two's contract text may now name the mechanism. **The caveat is LS-F1**: the one place
#510 asserts an enforcement its instrument declares it cannot provide is exactly the
premature-assertion risk T-1(b) is worried about, and it materialized. That is a reason
to amend, not to end the round. The architectural limb of T-1 is `lead-architect`'s.

**T-2 — a ruling on #510 does not bind #513, on my limb.** #513's fail-closed rules
stand on Q3 and Q6, both ruled and both open for tranche three by the topic's own gate
lines. Its dependency on tranche two is stated as *"Sequencing, not blocking"*
(`design.md:415`, `tasks.md:177`) and is honest: an unattested chain is less worth
anchoring, not unanchorable. **None of my #513 findings depends on #510's fate.**

**T-3** — Not primarily my seat; it belongs to **company-policy-lead** (tenant voice on
authorization) with **lead-architect** on the process limb. My only security note: a
draft filed FOR REVIEW that creates nothing, moves no key material and touches no
`contracts/` byte (§1.12) is not a security-relevant unauthorized act, whatever the
governance answer.

**A-1 / A-3 / A-4** — **NOT MY SEAT**: provenance fidelity and lifecycle conformance
belong to **company-policy-lead** and **lead-quality**; mapping accuracy to
**lead-architect**. I note only that A-1 is load-bearing for #513's three citations.

**A-2** — Not my seat (**lead-quality**), except that I found no assertion about the
estate in #509 that touches security posture.

**A-5** — Within charter only insofar as a council record is itself an artifact. My
view: a council was **not** the right instrument for #509 alone, but bringing it was
right *here* because #513's normative text cites it (§0.9). No review record should be
created for it (§1.3 measured that none has ever existed).

**B-1** — ACCEPT AS AMENDED; see verdicts.

**B-2 / B-3 / B-7 / X-3** — **NOT MY SEAT**: composition of ADDED-vs-MODIFIED, the
plural-predecessor ordering, naming, and the two-deltas-into-one-unpromoted-capability
question are **lead-architect**'s, with **lead-quality** on the counts. I contribute one
fact each: §0.4's twelve/nine inflation is **confirmed by my own count** (§1.1), and
D4's *"a dropped attestation is a break"* **is** enforced by drafted text, but only over
what reached the log (LS-F5).

**B-4 — D6, the revocation-after-signing horizon: SOUND, and I endorse it.** *"A
certificate revoked AFTER a signature was made does not retroactively unmake an act the
gate already permitted — it refuses everything the chain has not yet been permitted
for"* (`:41-47`) is the honest statement of what a control can reach, and it is
consistent with link 10's two-horizon rule. This is the packet at its best.

**B-5 — the three closed P1s: TWO DO NOT HOLD AS APPLIED.** P1-1 → **LS-F2** (the fix's
own escape reopens it). P1-3 → **LS-F1** (the fix binds to an instrument that declares
it cannot serve). P1-2 → holds against the attack it was written for, with a **new
adjacent residual**, LS-F5. I executed §1.4, §1.5, §1.6 rather than reading D10.

**B-6 — YES, #510 needs to consume R12, and it is the natural home.** #510 **is** the
attestation tranche; R12's four deferred envelope questions are attestation-envelope
questions; and R12's no-self-attestation rule bears directly on LS-F4 (the controller's
uncorroborated self-report about its own environment) and on the corroborate-vs-notarize
decision. R12 named "the signed-execution-chain change (staged; PR #452)", which meant
tranche one — and tranche one ratified without it, so the obligation is live and
unhoused. Tranche one cannot take it retrospectively; tranche three is the wrong layer.
**#510, or a named successor cited in #510.**

**B-8** — Not my seat (**company-policy-lead**). Security note only: a `Status: draft`
packet on main confers nothing and moves no contract byte (§1.12), so it is a safe
object in my sense.

**C-1 — D8, the anchor-late narrowing: (i) CORRECT and faithfully recorded, on my
limb.** The append-only mechanics are as the packet states — a checkpoint commits to
its whole prefix by construction, so the literal reading is unachievable — and what the
constraint PROTECTS (a false attestation permanently backed by a chain as valid) is
genuinely honoured by the item/checkpoint split plus the never-read-as-validation rule
and its contract-text disclaimer (`:288-323`). The rejected alternative (a second
validated-only tree) would have created a second log to keep consistent, which is a
worse security object. Whether *recorded* suffices where the topic called it *"a real
design constraint"* is a governance question for **lead-architect** and Brett.

**C-2 — see §1.8.** The claim fails closed and the factory keeps running: **correct**.
A missing witness cannot stop the factory: **correct, and deliberately asymmetric with
requirement 6, which I rule right.** A claim cannot pass presented as anchored on one
witness; a ten-year claim on the durability witness alone is admitted and I rule that
**consistent with Q3**. `455bbdaa` **fixed** the collision rather than moving it.
**What it does not reach is LS-F7**: the incompleteness cannot travel with the receipt,
so an independent holder of a one-entry receipt learns nothing of the missing witness.

**C-3 — the dependency expression is honest and safe** (`design.md:415`,
`tasks.md:177`): "Sequencing, not blocking", tranche two named as in-flight, and only
tranche one and the PKI plane named as hard prerequisites. No fail-closed rule of #513
depends on tranche two's text.

**C-4 / C-7** — **NOT MY SEAT**: naming and the unrouted D1/D9 are **lead-architect**'s.

**C-5** — Within charter on two of the four. **D-B, the structural payload refusal:
ACCEPT and commend it** — refusing by field shape rather than by semantics is both
neutral and strictly stronger, and it reaches raw, encrypted and plain-hashed content
without domain knowledge (`:379-388`). **D-C, the declared-construction refusal and its
residual: ACCEPT the refusal, and the residual is honestly stated** (`:402-411`) — but
see LS-F8, which is a gap in the refusal itself and not in the residual. **D-E**
(permissioned-ledger selection deferred) — acceptable to me: requirement 6's
unevaluable-consent refusal binds whatever is selected, so the deferral does not defer a
control. **D-F** (per-plane key correction) — the correction is made **in #513's own
requirement text** (`:602-611`) and the vendored study is untouched, which respects the
standing rule; and it closes a real defect (a shared record digest across three planes
is a join key). **ACCEPT.**

**C-6 — Q5 is held without being constitutionalized: CORRECT.** `:478-484` states
today's posture positively and writes *"NO permanent prohibition and NO condition under
which a different posture would become admissible"*, with a matching scenario at
`:524-528`. Requirement 2 does the same for a third chain (`:135-141`). Both are exactly
what Brett's ruling against permanence demands.

**X-1 — CLAIMS OUTRUNNING THE MACHINERY.** My census: #510 declares its major
enforcements as not-yet-existing with cites (the CA at `tasks.md:5.2`, the omnigent
layer at `5.3`, three explicit residuals) — **good practice, and mostly honest**. The
**one ASSERTED enforcement** is revocation-at-exercise, **LS-F1**, blocking. #513
declares its runtime as operator infrastructure and its validator as a code surface;
its one asserted-but-unreachable property is the commitment-path exclusivity, which it
**declares** as a shortfall (`:454-458`). **LS-F12** is the cross-cutting form: the
declared-shortfall pattern has no floor.

**X-2 — VOCABULARY: CONSUMED, not reinvented, in both, on every path I resolved.**
#510: `add-trust-anchor`'s certificate and declared-custody vocabulary; tranche one's
single digest construction (with `e1bd201d`'s correction to quote the requirement rather
than the proposal); `add-identity-brokering`'s persona refusal; `add-wallet-carried-
review-authority`'s `object_ref`, which I verified is a real shipped field (§1.5); and
the omnigent matrix, which I verified byte-exact (§1.2). #513 defines a new capability
and consumes tranche one's log and digest rules. **No second identity, certificate,
digest or proof vocabulary is minted in either.** The staged topic's first-named risk is
avoided.

**X-3** — **NOT MY SEAT** (**lead-architect**, with #504 open).

---

## 4. VERDICTS — ONE PER SUBJECT

### #509 — **ACCEPT**
On my limb only: the vendored document discloses no credential, secret, key, PHI or
identifier, and the unsafe 2024 architecture it records is explicitly corrected in its
own appendix so it cannot be read as endorsed (§1.13); provenance fidelity, mapping
accuracy and lifecycle conformance are `company-policy-lead`'s, `lead-architect`'s and
`lead-quality`'s and I do not rule them.

### #510 — **ACCEPT AS AMENDED**
The packet's fail-closed instincts are sound and its citations verify, but three
drafted controls do not hold under subtraction — a revocation requirement its own
instrument declares it cannot serve, an attribution refusal fully dischargeable by
declaration with no named floor, and a custody rule that enumerates hand-overs and
never reachability — and each is dischargeable by named text rather than by
restructuring, so the gate stays closed until LS-A1, LS-A2 and LS-A3 are discharged.

### #513 — **ACCEPT AS AMENDED**
Q3 and Q6 are carried faithfully, the missing-witness semantics are right and
`455bbdaa` genuinely fixed the collision it names, but the receipt/state split leaves
the incompleteness unable to travel with the artifact the design exists to make
independently checkable, and Q6's erasure property rests on an unbounded salt and an
uncustodied key; LS-A5 and LS-A6 discharge both without disturbing the split.

### Amendments

**LS-A1 [510] BLOCKING** — Declare the revocation-at-exercise shortfall, or bind
closure to an instrument that can serve it. *Discharged by* either (a) a declared
shortfall in requirement 7 on `add-trust-anchor`'s pattern, naming the file-based
register's issuance-time-snapshot limit and the Hermes-runtime live lookup (the S5
successor) as what would close it, or (b) requirement text conditioning closure on a
revocation surface that answers at exercise. Cite
`governance/review-authority/register.yaml:19-25`.

**LS-A2 [510] BLOCKING** — Give the attribution refusal a floor. *Discharged by*
naming, in requirement 2, at least one use that a declared attribution shortfall
disqualifies — specifically that a chain whose realization declares it cannot attribute
a request to a provisioned task **SHALL NOT satisfy the links 1–6 gate for the terminal
act**, or alternatively that its link-5 facts carry a class weaker than
`controller_corroborated`. Today the disqualified set has no members.

**LS-A3 [510] BLOCKING** — Make *"in every configuration"* reach reachability, not only
hand-over. *Discharged by* one added condition and one scenario: the tier-2 signing key
SHALL NOT be readable from any host, process or credential scope a worker, runner or
lane executes within, and a design co-locating the controller inside the runner's trust
boundary is REFUSED — with the same force as the existing crossing refusals.

**LS-A4 [510] SHOULD-FIX** — Admit a fourth evidence class for the controller's own
uncorroborated self-report (or state in terms that link 4's facts are outside the
class rule and why). *Discharged by* requirement 3 text plus one scenario; it also
settles half of `tasks.md:4.2`.

**LS-A5 [513] BLOCKING** — Make the incompleteness travel with the artifact.
*Discharged by* requiring the receipt (or a companion the receipt commits to) to carry
the **CONFIGURED witness set at mint time**, so a one-entry receipt against a
two-witness configuration is self-evidently incomplete to any independent holder
without consulting the minter. This is configuration, not *"what has not happened
yet"*, so it does not disturb the receipt/state split at `:131-133`.

**LS-A6 [513] BLOCKING** — Close Q6's two unspecified parameters. *Discharged by*
requirement 5 gaining (a) a **KEY custody reference** on the same footing as the salt,
with the same refusal for a key resolving onto a chain, into the anchored record, or
shared across planes; and (b) a **declared minimum salt entropy** (or a declared
CSPRNG source and width), with a refusal for a declared construction that omits it.

**LS-A7 [513] SHOULD-FIX** — Bound capture by finality. *Discharged by* requiring the
chain-acceptance evidence to carry a per-chain **declared confirmation depth or
finality condition met at capture time**, since a captured receipt is the only path to
complete.

**LS-A8 [513] SHOULD-FIX** — Make the anchor-state record answerable to the log.
*Discharged by* requiring the record every surface reads to be **derivable from, and
equal to**, the state its evidence-plane leaves imply, with a divergence treated as a
refusal — the same repair #510's P1-2 applied to enumerations.

**LS-A9 [513] SHOULD-FIX** — Resolve `anchor_pending` / `anchor_incomplete` in the
healthy path, and state what a verification returns for a pending item.

**LS-A10 [X] SHOULD-FIX** — Write a floor under the declared-shortfall pattern: a
sentence, in whichever packet Brett prefers, stating what a declared shortfall
disqualifies and that a declaration never converts an unmeetable control into a met
one. Five load-bearing sites, no floor.

### Conditions attached to the record

**LS-C1** — My two carried-fact re-verifications (§1.1) **agree with the convening's**
and are offered as independent confirmation, not as adoption of them.

**LS-C2** — My #509 verdict is **limited to the disclosure limb**. It must not be
tallied as a view on provenance fidelity, mapping accuracy or lifecycle conformance.

**LS-C3** — LS-F7 and LS-F8 are findings **about #513's own text and stand whatever is
ruled on #510**; they must not be swept up in a T-1 ruling.

**LS-C4 — MY PARK, recorded under my charter's `security_ambiguity → park_for_liaison`
must-not.** I park **the client-layer exposure verdict the unseated
`client-security-compliance-officer` would have carried**. I carried and discharged the
**domain-layer** exposure reading as §3.2 assigned; I cannot supply a client-layer
voice, and I will not wave one through by treating my own reading as covering both.
**What I could not resolve:** whether a client-layer security-compliance voice is owed
on a sitting that sets no rule — because the predicate that would have answered it
returns `ConditionUnevaluable`, not `False` (§1.14), and its own module says the caller
must then refuse the rule or **park the convening**, with no rule here to refuse.
**What would resolve it:** either (i) Brett seats the CSC for a supplementary reading
limited to LS-F1, LS-F3, LS-F7 and LS-F8, or (ii) Brett rules on the record that no
client-layer exposure voice is required for a §7.4 proposal review that sets no rule —
which would also discharge the 2026-08-29 dissent that has now stood unresolved through
two sittings. Either is a real answer; the present state, where the ground is recorded
as *false* and the code says *unevaluable*, is not.

---

## 5. In the packets' and the changes' FAVOUR

1. **#510's constitutional citation is exact.** I walked the schema rather than the
   prose: closed six-boolean matrix, `additionalProperties: false`, `execute_final_action`
   and `access_secrets` both `const: false`, exactly five archetypes. Every clause of
   the packet's characterization verifies (§1.2). Citations this precise are rare.
2. **`access_secrets: false` forbids custody, not duration** (`:279-284`) is the right
   reading of the constitution, and the *"issue it and destroy it"* scenario (`:298-302`)
   refuses the single most likely implementer shortcut with the right reason: the breach
   is the crossing, not the retention.
3. **BIND BEFORE SIGN** (`:212`) is the correct control and it is correctly placed:
   Q7 settles where the key lives and never whether the claims are checked, and the
   packet says exactly that (`:221-223`). The `runner_claimed` labelling rule, and the
   refusal of a consumer that quotes a runner-claimed fact as corroborated, are a
   genuinely good defence against laundering.
4. **#510's two-horizon doctrine is honest about what a control cannot reach.** *"A
   merge that already happened is not retroactively refused — that is not a concession
   but what an honest control says about a state it cannot reach"* (`:540-542`), paired
   with forfeiting everything downstream. This is the right shape and I would not want
   it changed.
5. **The remediation exemption's five conditions are well built**, and condition 4 —
   the exemption is **not inheritable** — cites the family's own prior defect (an
   exemption inheritable by identifier collision). A packet that learns from the
   estate's recorded failures is doing the thing this bench exists to encourage.
6. **#513's structural payload refusal is the best security idea in either packet.**
   Refusing by field shape rather than by semantics is simultaneously neutral (no domain
   terms) and **stricter** than a semantic refusal (it catches encrypted and
   plain-hashed content without classifying anything). That is a real design insight.
7. **`2e539779`'s fourth element is a genuine catch, honestly bounded.** Recognizing
   that bytes + inclusion proof prove only membership under *the supplied header*, and
   then **refusing verification against a minter-supplied header source**, closes a real
   forgery path — and the packet explicitly declines to claim self-sufficiency against a
   forged history. Both the fix and the disclaimer are right.
8. **`455bbdaa` is a model self-catch.** It resolved a two-requirement collision **by
   the receipt's own rule rather than by an exception to it**, and `2e539779` then
   propagated the fourth element into that same paragraph and scenario rather than
   leaving a three/four mismatch behind — the carry-forward failure this estate has
   recorded before, avoided here.
9. **#513's erasure honesty in the overclaim direction is exemplary**: it states the
   permanent unverifiability **before** the act, refuses any un-publication claim, and
   requires a retraction to be a new leaf and a new anchor. Many designs would have sold
   salt destruction as clean erasure; this one does not.
10. **Both packets refuse to constitutionalize** — no permanent bar on contract code, no
    condition written for a third chain — which is precisely what Brett's Q5 ruling
    against the recommendation's permanence demanded, and it would have been easy to get
    wrong in the safety-maximizing direction.
11. **Neither packet touches key material, `contracts/`, or any live surface** (§1.12),
    and both say so in terms. For a sitting about attestation and anchoring, that
    restraint is worth naming.
12. **Both packets decline to claim a drafting approver and say why**, with #513 citing
    tranche one's own corrected overstatement against itself. That is the family's lesson
    carried rather than repeated, and it made T-3 an honest question instead of a
    discovery.
13. **#509's appendix corrects the source rather than flattering it** — three named
    2026 upgrades over a 2024 sketch, including the one that matters most (encrypted PHI
    on a public chain is still refused). A vendoring that publishes its own subject's
    superseded assumptions, labelled, is a good record.
