Seat: lead-architect (domain seat) · Convening: gate_rules_council (§7.4 sitting), 2026-08-30
Packet: openspec/changes/add-chain-attestation/review/convening-packet-2026-08-30.md
Judged at: openxFactory main afe29561 / #510 e7f6ae0e / #513 cf5a24b8 / #509 26c7e778

# SEAT RETURN — `lead-architect` (LA), domain seat

## 0. Persona declaration

Charter, quoted from codexFactory `hermes/domain/roles/lead-architect.yaml`
(read at `sittingref` 3c71ddc9):

```yaml
authority:
  owns:    [system_architecture, cross_cutting_design, technical_consistency]
  decides: [architecture_direction, decomposition_shape_acceptance]
  escalates:
    - trigger: architecture_ambiguity_unresolvable
      to: council_large
      then: park_for_liaison
disposition: {rigor: high, risk_posture: averse, bias: quality, autonomy: high}
guardrail: character_never_overrides_authority
```

**Seat basis:** `gate-rules.yaml` `members.domain`, unconditional roster
(packet §3.3). Model `opus`, inherited per the 2026-08-29 §7.4 precedent.

**Assigned obligation:** packet §4 `lead-architect` row (a)–(e), plus the EVERY
SEAT row (i)–(iii).

**Boundary readings I take, stated openly.**

1. My charter's `technical_consistency` is what makes T-1 mine first: the
   question is whether three ruled texts about the same object cohere, which is
   a consistency question before it is a governance one. I answer it.
2. `decomposition_shape_acceptance` is the express grant that puts D3, X-3 and
   C-4 in my seat. I rule them.
3. #509 is mine ONLY as to mapping accuracy (§1.3 says so and I agree).
   Provenance-voice, lifecycle-header conformance and the tenant-voice question
   are **company-policy-lead**'s; falsity-sweeping is **lead-quality**'s. I
   answer A-3 fully, A-2 only where a mapping row carries an estate claim, and
   I decline A-1 and A-4.
4. I do **not** re-open any of the seven Q-dispositions. Where I say a packet
   misreads one, that is a finding about the packet.
5. **My verdicts do not depend on the convening's two carried facts.** I
   re-measured both. Both are correct. Had they been wrong my findings would
   stand on my own measurements, which are reproduced below.

---

## 1. What I verified BY EXECUTION

**Checkout hygiene, before and after.** Every tree was clean on entry and on
exit; I wrote to no checkout. All scratch work is under `seat-scratch-LA/`.

```
$ for d in invmain inv510 inv513 inv509 sittingref; do ... git status --porcelain ...
invmain      porcelain:[] HEAD:afe29561
inv510       porcelain:[] HEAD:e7f6ae0e
inv513       porcelain:[] HEAD:cf5a24b8
inv509       porcelain:[] HEAD:26c7e778
sittingref   porcelain:[] HEAD:3c71ddc
```

### 1.1 §0.4 RE-VERIFIED INDEPENDENTLY — the convening is RIGHT; #510 is wrong at four sites

I wrote my own counter (`seat-scratch-LA/count.py`) rather than take the
packet's. Against tranche one's delta at `origin/main`:

```
$ python3 count.py invmain/openspec/changes/add-signed-execution-chain/specs/signed-execution-chain/spec.md
  391  scenarios=  9   A gate validates the short chain as a hash-linked chain
TOTAL requirements: 9   TOTAL scenarios: 45
```

And the four assertions, quoted from #510 at `e7f6ae0e`:

```
$ grep -n "twelve" design.md tasks.md proposal.md
tasks.md:99:      requirement — all twelve scenarios, not the two that change — and the packet
design.md:114:raised against it as PR #504). Restating it would also cost twelve scenarios of
design.md:124:twelve scenarios, not the two that change.
proposal.md:243:requirement — all twelve scenarios, not the two that change** — and this packet
```

**My measurement agrees with the convening's: the gate requirement carries
NINE scenarios.** No requirement in tranche one carries twelve. The figure is
overstated by exactly one third in the one paragraph where the cost IS the
argument — and, per §2 below, it is the cost of a repair I find is actually
owed, so the inflation runs against the packet's own interest once B-2 is ruled.

I also confirmed both packets' own headline counts, since counting was already
in hand: **#510 = 9 ADDED / 59 scenarios** and **#513 = 9 ADDED / 52** — both
as claimed. (Deeper count work is `lead-quality`'s row; I report what I ran.)

### 1.2 §0.7 RE-VERIFIED INDEPENDENTLY — the convening is RIGHT

```
$ sed -n '187,190p' invmain/openspec/changes/add-signed-execution-chain/tasks.md
- [ ] 5.3 Neither successor's content enters this packet. Re-derive the tranche
      two/three boundary against what actually exists when each is raised, per
      the topic's Q4 — a tranche that depends on an unbuilt layer is a plan, not
      a tranche.

$ grep -ci "when each is raised|task 5.3|tasks.md:5.3"  # all 8 packet files
inv510/.../proposal.md :0   design.md :0   tasks.md :0   .openspec.yaml :0
inv513/.../proposal.md :0   design.md :0   tasks.md :0   .openspec.yaml :0
```

**Zero hits in all eight files, reproduced.**

### 1.3 D3 BY CONSTRUCTION — I built the promoted canon and read it

This is obligation (b), and I discharged it by making the artifact rather than
reasoning about it. I copied `invmain/openspec` to scratch, dropped #510's
change directory beside tranche one's, and ran the estate's own promotion tool.

```
$ openspec archive add-signed-execution-chain --yes --no-validate
Specs to update:  signed-execution-chain: create
  + 9 added        Totals: + 9, ~ 0, - 0, → 0

$ openspec archive add-chain-attestation --yes --no-validate
Specs to update:  signed-execution-chain: update
  + 9 added        Totals: + 9, ~ 0, - 0, → 0
```

Mechanically it composes: 18 requirements, 104 scenarios, no name collision, no
error. **Semantically it does not.** The promoted file
`openspec/specs/signed-execution-chain/spec.md` now holds, verbatim:

```
:552  #### Scenario: a tranche-two link does not exist yet
      - WHEN the gate walks a chain that carries no attestation link
      - THEN it validates links 1–3 and returns a verdict scoped to them
      - AND the absent later link is not reported as a break

:1141 #### Scenario: a chain carrying links 1–3 only reaches the gate after this tranche is in force
      - WHEN a chain presents the ratification, the inception and the traveling
        contract and no attestation links at all
      - THEN the gate REFUSES to permit the terminal act, because links 4–6 are
        in scope from this tranche and are no longer "a later tranche's link"
      - AND tranche one's scope note is not available as a permission, having
        been written for the period before this tranche existed
```

**Same antecedent. Opposite consequent. Both normative. Both in canon.** The
archive line `~ 0` is the proof that nothing was modified to reconcile them.

I then checked whether tranche one's gate requirement really self-limits, which
is the precise question I was set. **It self-limits its SCOPE NOTE and not its
CLOSED-LIST CLAUSE.** In the promoted file at `:444`:

```
**THE LIST IS CLOSED, AND CLOSING IT IS ITSELF AN OBLIGATION.** Because the gate
validates EXACTLY these checks before the terminal act, **every requirement of
this capability is either walked here or has its enforcement point named
below** — a requirement absent from both is a requirement this capability does
not enforce, however firmly its own text is written.
```

The mapping table beneath it has **nine rows, one per tranche-one requirement**.
After promotion "this capability" numbers **eighteen** requirements. #510 adds
no row and amends no clause:

```
$ grep -rn "LIST IS CLOSED|EXACTLY these checks|Where it is enforced" inv510/.../add-chain-attestation/
NO HITS
```

So promoted canon asserts, in its own words, that #510's nine requirements are
"requirement[s] this capability does not enforce."

### 1.4 THE ARCHIVE-ORDER HAZARD (X-3) — demonstrated, not argued

Because both siblings write ADDED into a capability that does not exist:

```
$ ls invmain/openspec/specs/ | wc -l          → 52   (signed-execution-chain absent)
$ ls -d invmain/openspec/specs/signed-execution-chain
ls: cannot access ...: No such file or directory
```

I archived them in the reverse order, in a second scratch tree:

```
$ openspec archive add-chain-attestation --yes --no-validate   # tranche one still ACTIVE
Specs to update:  signed-execution-chain: create
  + 9 added
$ grep -c "^### Requirement" openspec/specs/signed-execution-chain/spec.md
9
:6 ### Requirement: The harness controller attests the environment it prepared
```

**Whichever sibling archives first CREATES the capability, silently, and both
orders "succeed."** Archived tranche-two-first, canon holds tranche TWO's nine
requirements as the entirety of `signed-execution-chain`, with the ratified nine
absent. Nothing in either packet or in the tool orders them.

### 1.5 THE VOCABULARY AUDIT (obligation c) — every citation resolved

| Cited authority | What #510 claims | Resolved at | Verdict |
|---|---|---|---|
| `add-trust-anchor` — certificates | link 4's cert is a `trust-anchor` shape, "in no parallel one" | `openspec/changes/add-trust-anchor/specs/trust-anchor/spec.md` — 8 requirements incl. *"Declared chain custody bounds what a certificate evidences"* (:69); #510 `spec.md:57` mirrors its host-held/hardware-bound scenario | **CONSUMED** |
| `add-trust-anchor` — "conformance-declaration rule" | the technique for declaring what a realization cannot meet | The label is absent from that change's SPECS (the requirement is titled *"A realization declares the obligations it cannot meet"*, :214) but resolves to the REALIZED artifact `contracts/trust-anchor/conformance-declaration.schema.yaml` | **CONSUMED** (label taken from the shipped schema, not coined) |
| `add-identity-brokering` — signer identity | who a signer is | `.../identity-brokering/spec.md` — 10 requirements incl. *"Workloads are not personas"* (:191), *"A governed record binds its actor to a stable opaque subject"* (:149) | **CONSUMED** |
| `contracts/omnigent/` — the constitutional ground | "closed six-boolean matrix, `additionalProperties: false`, `execute_final_action` and `access_secrets` both `const: false`, five archetypes" | Parsed the schema: `permissions` at `$defs/worker_class/properties`, `additionalProperties: False`, **6** booleans, `execute_final_action const=False`, `access_secrets const=False`; archetype enum `frame … assemble_for_admission` | **CONSUMED — verbatim accurate** |
| `add-wallet-carried-review-authority` | closure established under "review authority PROVEN BY POSSESSION in the shipped vocabulary" | That change's spec has *"Review authority is held as an openxwallet grant and by nothing else"* (:5). Proof-of-possession is openxwallet's, which that grant requires by construction. #510 says *"No second review-authority, proof or grant vocabulary is defined"* | **CONSUMED** — the chain of citation resolves; I had suspected a mis-citation and execution corrected me |
| Tranche one — the ONE digest construction | no second construction declared | #510 `spec.md:386` states it and adds a refusing scenario (`:474`) | **CONSUMED** |
| **The evidence class** `controller_corroborated` / `hardware_attested` / `runner_claimed` | proposal.md:2 — *"NO SECOND identity, certificate, digest or proof vocabulary is defined"* | See below | **MINTED** |

**The minted vocabulary, and why it is the risk the topic names.** The estate
already owns a ratified, CLOSED assurance vocabulary on this axis:
`contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml`, ratified by
`add-trust-anchor` (Brett Heap, 2026-08-21, OQ2), realized at `contract-v1.37`.
It carries ranked `assurance_levels` (0/1/2), derives `evidences` from two
booleans and forbids independent assertion, and carries a `composes_with` block
naming openxwallet's registry so *"the two sets cannot drift into two custody
models."* It also carries this, verbatim:

```
excluded_models:
  - id: asserted_hardware_backing
    reason: >-
      "Hardware-backed" as a self-standing member would re-open the hole from
      the marketing side: the family's own live canary runs certificates whose
      keys are hardware-resident and usable by the host without limit, and
      those evidence the HOST. The discriminators are readability and per-use
      authorization; where the key physically lives is a fact about blast
      radius that belongs in `notes`, never a tier.
```

#510 mints a three-member class one of whose members is **`hardware_attested`**,
uses it with strength semantics — *"an unclassed fact is read at the strength of
the strongest fact beside it"* (`spec.md:231`) and a scenario refusing a
`runner_claimed` fact read *"as though it were corroborated"* (`:252`) — and
**declares no ordering, no derivation, and no composition with the ratified
ladder**:

```
$ grep -rn "chain-custody|custody registry|assurance_ceiling|assurance ladder|
           host_held|holder_attributed|excluded_models|asserted_hardware"  inv510/.../add-chain-attestation/
>>> ZERO HITS <<<
```

And the packet defers the closure question to schema authoring
(`design.md` "does NOT decide" item 2; `tasks.md:4.2` — *"whether … is a CLOSED
set at the schema, and what a fourth class would have to establish"*) **without
naming the registry that already answers exactly that question for this axis.**

**#513, by contrast, mints nothing.** It cites `add-trust-anchor` 8×, cites
tranche one 19×, names no certificate or identity vocabulary in its spec, and
carries requirement 9 *"This capability is neutral and names no domain
semantics."* Commitments, receipts and anchors have no incumbent owner in this
estate. **CONSUMED / no collision.**

### 1.6 #513's D8, AND THE CONSTRAINT'S ACTUAL STATUS (obligation d)

I read the constraint in the topic, not in a summary. It sits inside
`## Conflicts` (`:451`) at `:474`, and I confirm the packet's §0.6 correction
against my own read: the second conflict carries *"RESOLVED 2026-08-29"*, the
third is *"left OPEN by design"*, and **the anchor-late paragraph carries no
ruling stamp, no date and no `Dispositioned-by` line.** Repo-wide:

```
$ grep -rn "only what has been validated" invmain/
INDEX.md:1820 ... signed-execution-chain.md:474      → exactly two hits
```

D8's engineering is correct and I verify the mechanism it rests on: against an
append-only log a signed tree head commits to the whole prefix by construction,
so **no amount of anchoring late can exclude an earlier leaf**, and the literal
constraint is unachievable for checkpoints. The two-anchor decomposition
(ITEM anchor governed by anchor-late; LOG CHECKPOINT anchor claiming only that
the log said something) preserves exactly what the constraint protects. The
rejected alternative — a second validated-only tree — is rejected on the
**two-records-of-one-decision** ground, which is the family's own named FIRST
risk (`:465-469`), and I endorse that rejection as an architect: a second
authoritative tree is a worse defect than the one it cures.

It also preserves the topic's own reasoning verbatim (`#513 spec.md:284-286`:
*"because anchoring is aggregated and batched in any case, the cost of lateness
is one aggregation interval rather than an architectural concession"*), records
the narrowing IN the requirement text (`:316`), and adds a retraction rule
(*"A RETRACTION IS A NEW LEAF AND A NEW ANCHOR, NEVER AN ERASURE"*).

### 1.7 #509's MAPPING APPENDIX (obligation e) — every target resolved

| # | What the appendix asserts | Verified at `origin/main` | Verdict |
|---|---|---|---|
| 1 | *"its 'The on-chain layer, as ruled' section"* | heading exists, `:205` | **TRUE** |
| 2 | *"its 'So the split is' table"* | `:346` `So the split is:` followed by the table at `:352` | **TRUE** |
| 3 | *"What goes on chain, and what must not"* section | heading exists, `:326` | **TRUE** |
| 4 | Q2 quotation *"off chain: every payload without exception… on chain: salted keyed commitments… and the chain anchors"* | Source (whitespace-normalized): *"ON CHAIN, and nothing else: salted keyed commitments, commitments to consent-log CHECKPOINTS, and the chain anchors. OFF CHAIN: every payload without exception, plus consent STATE and the SALTS."* Fragments verbatim; **clauses transposed** (source is on-chain first) without marking the transposition | **SUBSTANTIVELY TRUE, quotation transposed** |
| 5 | *"claim 2 names HealthLinc … 'pushed to the patient app, or printed as signed orders'"* | claim 2 at `:423`, wording verbatim | **TRUE** |
| 6 | *"Claim 3's LedgerLinc"* | claim 3 at `:427` | **TRUE** |
| 7 | *"claim 4's 'two mappings are the same shape'"* | claim 4 at `:430` *"The two mappings are the same shape."* | **TRUE** |
| 8 | transparency log = *"claim 6"* | claim 6 at `:437` is the evidence-plane/transparency-log claim | **TRUE** (claim 7 is the anchoring claim proper; citing claim 6 for "commitments + anchoring" in bullet 1 is loose — OBSERVATION) |
| 9 | Q3's three conditions *"archival node; inclusion proofs captured and retained at anchor time; corroborating evidence, never sole"* | Q3 at `:628-630`: *"archival node; inclusion proofs captured AND retained at anchor time; corroborating…"* | **TRUE** |
| 10 | *"EDPB Guidelines 02/2025 (v2.0)"* | Q2 at `:567` cites *"EDPB 02/2025 v2.0"* | **TRUE** |
| 11 | *"Q2's ruled boundary excludes this outright"* (encrypted PHI on a public chain) | Q2 disposition: *"OFF CHAIN: every payload without exception"* | **TRUE** |
| 12 | tranche 3 *"does not yet name this consumer"* (meta-analysis lane) | `grep meta-analysis\|de-identif` → no such consumer named | **TRUE** |
| 13 | the topic *"framed around what was signed and produced"*, failed-attempt logging not carried | `grep "failed attempt\|verification attempt\|refused access"` → zero | **TRUE** |
| 14 | **"Q2, ruled 2026-08-29 (CONFIRMED operative form)"** | Q2 `:568`: *"Disposition status: ruled 2026-08-29 — Brett Heap, in session; **AS RECOMMENDED**"*. **"CONFIRMED" is Q6's label** (`:753` *"Disposition status: CONFIRMED 2026-08-29"*), and *"the ruling's operative form"* is the Conflicts section's phrase about **Q6** | **FALSE AS TO THE LABEL** — Q6's disposition type transplanted onto Q2. The substance (Q2 does require salted keyed commitments) is correct |
| 15 | **"the property `signed-execution-chain` calls chain inception's fidelity property"** | `grep "fidelity"` in the topic → ONE hit, `:88`, in an unrelated sense (*"which is the fidelity defect this family keeps finding"*). **The topic never uses this term** | **FALSE** — a coinage of the vendoring author presented as the topic's vocabulary |
| 16 | **"arriving eighteen months before"** / *"predating the neutral family by eighteen months"* | Notes dated 2024-11-10 (Source block); sitting 2026-08-29. `(b-a).days = 657 → 21.6 months` | **FALSE** — understated by ~4 months, asserted twice |

Rows 14–16 are all in the **vendoring author's appendix**, not in Brett's notes.
None touches Brett's speculative content, which I do not judge.

### 1.8 THE INHERITED BOT SURFACE — I attacked the fixes (EVERY SEAT (ii))

**#510's three P1s (`design.md` D10).** All three are one shape — *"a record that
NAMED something standing where a record that ESTABLISHES it belonged."*

* **P1-2, "a proper subset named nothing" — the fix HOLDS, and it is the best
  work in either packet.** The repair does not weaken the rule; it supplies the
  missing authoritative set and specifies the query that produces it
  (`spec.md:400-413`): *"every leaf of the link-5 record kind committing to this
  chain identity, at or before the successor's own leaf"*, with **EQUALITY**
  required — *"Not a subset and not a superset"* — plus a scenario for the
  precise attack (`a lane omits an attestation before presenting its successor`).
  It is runnable as written, and it **inherits** tranche one's suffix-truncation
  residual rather than re-declaring it. I could not break it.
* **P1-3, closure bound to review AUTHORITY — the fix HOLDS.** Verified the
  citation chain resolves (§1.5) and the scenarios cover the fabricated record,
  the revoked grant and the "closure ≠ each seat signed" misreading.
* **P1-1, the signing-request attribution** — the repair requires attribution
  inside the signed bytes with the residual declared. Sound on my axis; the
  subtraction testing of it is `lead-security`'s row.

**#513's four fix commits — read, then attacked.**

* `455bbdaa` — resolves the receipt/pending collision by the receipt's own rule
  rather than an exception, moving in-flight state to an **anchor-state record**.
  My attack was that a fix curing a collision by introducing an undefined record
  merely moves it. **It does not:** the record is in the declared code surface
  (`proposal.md:2` — *"the ANCHOR STATE record (`anchor_pending` /
  `anchor_incomplete` / complete…)"*), it is used consistently at four spec
  sites, and `:275` states the separation of concerns explicitly — *"the receipt
  holding proof material and never state."* **HOLDS.**
* `e1bd201d` — claims correction "in the proposal, design.md and the origin
  manifest." My first grep found only two of the three and I nearly filed it as
  an incomplete fix; the third is line-wrapped. Reading the commit itself shows
  `design.md` corrected `"and any a later tranche adds"` → `"any digest a later
  tranche adds"`, which matches tranche one's spec `:247` verbatim. **All three
  sites. HOLDS.** (Recorded because it is the sort of near-miss the method rule
  exists to prevent, in my own work.)
* `2e539779` — the D8 two-anchor split. Assessed in §1.6. **HOLDS.**
* `cf5a24b8` — **the one fix I find defective.** It cures a dead reference by
  writing a transient fact into **normative requirement text**, at three sites:

```
:546 **That file is vendored by openxFactory pull request #509, which is IN FLIGHT at
:547 this revision**, so the path resolves once #509 lands …
:604 MedxChain notes (cited above; vendored by pull request #509, IN FLIGHT at this
:658 #509, IN FLIGHT at this revision — read as an early, domain-specific
```

  These are in `specs/chain-anchoring/spec.md`, which promotion carries verbatim.
  Once #509 lands and #513 archives, promoted canon asserts three times that a
  merged pull request is "IN FLIGHT," and the qualifier *"at this revision"* is a
  deictic with no referent in a promoted spec — **structurally identical to the
  "this tranche" problem I proved in §1.3.** The fix is the P1 shape it was
  meant to cure, one level down: a record naming a moment where a record stating
  a durable fact belongs. The stronger half of the same commit — *"The obligation
  does not depend on the citation … the citation is PROVENANCE"* — is right and
  is what makes the repair cheap.

### 1.9 `openspec validate --strict` on both branches

```
$ (inv510) openspec validate add-chain-attestation --strict
Change 'add-chain-attestation' is valid
$ (inv513) openspec validate add-chain-anchoring --strict
Change 'add-chain-anchoring' is valid
```

Both clean. **This is worth stating precisely: the tool passes both, and every
defect I report in §1.3 and §1.4 passes with them.** The checker validates a
change against itself; it does not validate what promotion produces. That gap is
the whole of my D3 and X-3 findings.

---

## 2. Findings

**LA-F1 [510] — BLOCKING. Promoted canon would hold two contradictory scenarios
on one fact pattern.** Built and read (§1.3). Canon `:552` and `:1141` share an
antecedent — a chain carrying links 1–3 and no attestation link — and give
opposite consequents: validate-and-scope versus REFUSE. Both are promoted
verbatim; the archive reports `~ 0` modified. The only reconciliation is prose
inside the second requirement (`:1087-1090`), and **prose in requirement B
cannot repeal a scenario in requirement A.** #510's own claim that *"No
requirement of tranche one is restated or replaced and none needs to be"*
(`:1090`) is disproved by construction: one does need to be.
Return citation: `seat-scratch-LA/promo/openspec/specs/signed-execution-chain/spec.md:552,1141`.

**LA-F2 [510] — BLOCKING. Tranche one's CLOSED-LIST clause does not self-limit,
and #510 leaves it orphaned.** (§1.3.) The clause is scoped to *"every
requirement of **this capability**"*, not to this tranche, and its mapping table
has nine rows. After promotion the capability has eighteen requirements and the
table still has nine — so canon states in terms that #510's nine *"are
requirement[s] this capability does not enforce."* This is the direct answer to
my obligation (b): **the gate requirement self-limits its SCOPE NOTE and not its
CLOSED-LIST CLAIM**, and #510 addresses only the half that was already
self-limiting (`grep`: zero hits for the clause anywhere in the packet).

**LA-F3 [510] — BLOCKING. A parallel assurance vocabulary is minted on an axis
that already has a ratified, closed registry — the topic's FIRST named risk.**
(§1.5.) `hardware_attested` is, by name and by substance, the member
`trust-anchor-chain-custody.registry.yaml` **excludes by ruling**, on reasoning
that applies with full force to a measurement root as it does to a key root. The
minted class carries strength semantics with no ranks and no derivation, where
the incumbent registry has ranked levels, derived `evidences`, and a
`composes_with` block written precisely so *"the two sets cannot drift into two
custody models."* The packet's disclaimer at `proposal.md:2` — *"NO SECOND
identity, certificate, digest or **proof** vocabulary is defined"* — enumerates
four kinds and omits the fifth, and the fifth is the one it mints. I take the
disclaimer as accurate-as-written rather than as evasion, and the finding is that
the enumeration is under-inclusive, not that the packet dissembled.

**LA-F4 [510] — SHOULD-FIX. The "twelve scenarios" figure is wrong at four
sites, and it prices the repair that is actually owed.** (§1.1.) NINE, measured
twice. It matters more than a typo because LA-F1/F2 make the MODIFIED
restatement the discharge, so the bench and Brett are being quoted a price a
third too high for the road I am recommending they take.

**LA-F5 [510] — BLOCKING (threshold). The re-derivation owed AT THE RAISING is
undischarged and uncited.** (§1.2, §3 T-1.) Tranche one's **ratified** task 5.3
fixes the trigger — *"when each is raised"* — and #510 IS the raising. #510
converts the obligation into a realization gate (`tasks.md:5.1`) and never
engages 5.3. `design.md` D7 argues the case honestly and well, and does not
mention it either.

**LA-F6 [X] — SHOULD-FIX. Archive order is unconstrained and both orders pass
silently.** (§1.4.) Demonstrated: archiving #510 first CREATES
`signed-execution-chain` holding only tranche two. #510's `.openspec.yaml` names
tranche one a hard prerequisite in prose; nothing enforces it. This is issue
**#502 / #504**'s class with a reproducible instance attached.

**LA-F7 [513] — SHOULD-FIX. `cf5a24b8` writes a transient fact into normative
text that promotion carries.** (§1.8.) Three sites assert a merged PR is "IN
FLIGHT," qualified by a deictic with no referent in canon.

**LA-F8 [509] — SHOULD-FIX. Three verifiable inaccuracies in the mapping
appendix**, rows 14–16 of §1.7: Q6's disposition label transplanted onto Q2;
*"chain inception's fidelity property"* presented as what the topic *"calls"* it
when the topic never uses the term; *"eighteen months"* where the arithmetic
gives 21.6, asserted twice. All three are the vendoring author's, none is
Brett's, all are cheap.

**LA-F9 [509] — OBSERVATION.** The Q2 quotation (row 4) is verbatim in its
fragments but transposes on-chain and off-chain clauses without marking the
transposition. Substance unaffected.

**LA-F10 [X] — OBSERVATION, in the packets' favour and against my own first
instinct.** I looked for an internal contradiction between `design.md`'s
"closure NOT decided" and `tasks.md:4.2`, and there is none — 4.2 says *"whether
… is a CLOSED set"*. I record the near-miss because it is the same discipline
§3.4 asks of the bench, applied to myself.

---

## 3. Positions on the ballot questions

### T — THRESHOLD AND SITTING

**T-0(a) — I hold to (ii): it needs a chartered third body.** `gate-rules.yaml`
declares `scope: per_repository_rule_setting` and asks *"what are the merge/gate
rules for this repo?"*. This sitting sets no rule; it reviews three proposals.
Reading the charter to reach proposal review makes `scope` decorative, and a
charter whose scope line does not bind is the same defect this council rules
against elsewhere. **The act is nonetheless lawful for a different reason — the
2026-08-29 sanction — and I do not disturb it.** But the sanction was for ONE
proposal; extending it to three by the convener's own motion stretches it. My
recommendation is unchanged from 2026-08-29: land codexFactory **#131**, and
until it lands treat each §7.4 seating as a fresh convener act requiring its own
disclosure — which this packet does, creditably, at §0.1.

**T-0(b) — the decline was RIGHT in outcome; the honest ground is
*inapplicable*, not *false*.** I re-offer the repair Brett's 2026-08-29 ruling
left undecided. The predicate `rule_touches_security_posture` asks a
definition-time question about *"the rule being SET"*. No rule is being set, so
the predicate has no subject — that is unevaluable, and `lead-security`'s reading
of `seat_resolution.py:40-44` (*"Unevaluable NEVER means absent"*) is correct as
a matter of code. Returning `False` from a predicate with no subject is how a
seat gets dropped by accident rather than by decision. **On the facts here the
seat would have been correctly absent either way** — no listed surface is
touched — so nothing turns on it in this sitting, which is exactly why it is the
right sitting to fix the ground. `lead-security`'s dissent should be resolved,
not preserved for a fourth convening.

**T-0(c) — combining three was lawful but was the wrong instrument, and it did
degrade my reading.** Answering honestly as asked: I gave #509 materially less
than I gave #510, and I would not have found LA-F1 had I paced all three
equally — it cost a build, two archives and a diff of the result. §0.9's
argument for combining is real but it argues for **sequencing** #509 before
#513, not for one sitting. The correct instrument was two sittings: the chain
pair together (they genuinely compose), #509 by ordinary pull request.

**T-1 — (c) NOT PREMATURE BUT NARROWED.** This is my seat's first question and I
rule it on the topic's own text, read whole rather than in either packet's
summary.

The estate contains three texts and they are consistent **only if their objects
are kept distinct**:

* **Q4** (`:672-683`) governs the **BOUNDARY** — which links fall in which
  tranche. Its verb is *"RE-DERIVED"*; its timing *"not fixed now"*. Its warning
  — *"a boundary drawn against an unbuilt layer is a guess wearing a tranche
  number"* — is about treating a boundary as SETTLED, not about writing prose.
* **The Exit path** (`:829-837`), ruled the same day in the same topic, governs
  the **CONTRACT TEXT**: tranche two's *"contract text may now NAME the
  mechanism"*, and *"what remains is machinery rather than a ruling."* That is an
  affirmative permission to draft, in the same ruled document.
* **Tranche one's ratified `tasks.md` 5.3** governs the boundary again and is the
  **only text in the estate that fixes a trigger**: *"when each is raised."*

Read together: **Q4 does not forbid the drafting.** It forbids fixing a boundary
as settled. The Exit path permits the drafting expressly. So option (b) fails —
it reads Q4's object as the drafting act when the same ruling's own exit path
says otherwise, and a reading that makes two halves of one ruling contradict is
the weaker reading.

But option (a) fails too, on a narrower point. **The re-derivation is owed NOW,
not at realization.** #510 relocates it to `tasks.md:5.1` and defends the move as
*"an obligation about a state the packet cannot observe."* That is true of the
SECOND re-derivation and false of the FIRST: task 5.3 asks for a re-derivation
*"against what actually exists"* **at the raising**, and what exists is
observable today and was in fact observed by the packet — `design.md` D7 records
that `implement-openxpki-install-repo` is ACTIVE at 22/30 and the omnigent family
is *"contracts and overlays with no runtime enforcing a chain precondition."*
**The packet performed the observation and did not perform the derivation from
it**, and it never cites the ratified task that asks for it.

I also record, because my charter teaches through rationale and because
conceding is part of it: **D7's substantive argument is good and I largely accept
it.** *"A boundary is a guess when it is drawn against an unbuilt layer's
SHAPE … this one is drawn against ratified neutral vocabulary that already
exists … and it names NO interface either plane must expose"* is the technique
`add-trust-anchor` used to ship a certificate contract without operating a CA —
and I **verified that precedent** rather than accepting the analogy
(`contracts/trust-anchor/` ships nine schemas including
`conformance-declaration.schema.yaml`, at `contract-v1.37`, with no CA). That is
the estate's established pattern for exactly this situation. It is why my answer
is (c) and not (b).

**The named narrowing** is therefore not a subset of the packet to strike. It is
one act to add: **perform the raising-time re-derivation, in this packet, and
cite task 5.3.** See LA-A5.

**T-2 — No, a ruling on #510 does NOT bind #513, and #513 is not premature *a
fortiori*.** #513's gates are Q3 and Q6, both OPEN, neither dependent on tranche
two. Its subject — commitments, receipts, anchors, the permissioned plane — is
reachable from tranche one's transparency log alone, and anchoring a checkpoint
of that log requires no link 4. #513 states the relation as *"Sequencing, not
blocking"* at four sites and names only tranche one and the PKI plane as hard
prerequisites; **I verified that this is architecturally true, not a convenience:**
`design.md:415` calls tranche two *"Not a hard prerequisite for anchoring a
checkpoint"*, and nothing in `specs/chain-anchoring/spec.md` requires a link-4,
-5 or -6 record to exist. Further, the T-1 narrowing I impose on #510 does not
transfer: task 5.3's raising-time obligation applies to #513 too, but #513 names
its unbuilt dependency (the permissioned-ledger selection) and **defers it
explicitly to realization as a routed decision (D-E / D5)** rather than silently.

**T-3 — NOT MY SEAT as to the governance question; one architectural
observation.** Whether a draft without a recorded drafting authorization is a
lawful object before this council belongs to **company-policy-lead** (tenant
voice) with **lead-quality** on the record-keeping half. My observation: both
packets decline to claim an approver and say why, and #513 cites the family's own
corrected overstatement against itself. Architecturally that is the right
posture — a packet that cannot cite an authorization should say so — and it is
the single most creditable thing in either document.

### A — SUBJECT #509

**A-1 — NOT MY SEAT** (**company-policy-lead**; §1.3 of the packet agrees).
Within my reach I note only that the `Source:` block is unusually candid about
what it is NOT: *"this vendoring reconstructs the notes' section structure and
enumerated claims from that transcript rather than reproducing byte-identical
prose"*, and names the OneNote original as *"the source artifact of record for
exact wording."*

**A-2 — Partly mine.** Confined to estate claims in the mapping appendix:
**three are false** (§1.7 rows 14, 15, 16). Every other estate claim I tested —
thirteen of them — is TRUE. Brett's speculative content I do not judge, and I
record that the appendix keeps the two cleanly apart: the estate claims are
confined to the appendix, and the appendix is separately headed and dated.
The exhaustive falsity sweep across the whole document is **lead-quality**'s.

**A-3 — MINE, and the table is at §1.7.** Sixteen rows, one cite each. Thirteen
accurate, one transposed quotation, three false. **Not blocking**: the three are
label-level and arithmetic errors in a brainstorm-stage appendix, none changes a
ruled disposition's substance, and all are cheap. But §1.3 of the packet is right
that the mapping appendix is *"the one part of a brainstorm document that is not
free-form"*, and row 14 in particular — a disposition label moved from one Q to
another — is the exact error class this estate's discipline exists to prevent.

**A-4 — NOT MY SEAT** (**company-policy-lead** on the header contract,
**lead-quality** on `document-lifecycle.md` conformance).

**A-5 — A council was NOT the right instrument, and I say so against the
convening's interest.** No brainstorm vendoring in this repository has carried a
review record; `ideation/` has no `review/` directory; the lifecycle makes
brainstorm the one stage where contradiction is legal. The mapping appendix is a
real review surface — I found three defects in it — but that is an argument for
**reviewing the appendix on the pull request**, which is where every comparable
object has been reviewed. Convening a bench over it sets a precedent that
brainstorm intake needs a council, which would make the cheapest stage of the
pipeline the most expensive. **The right instrument was ordinary PR review, with
the appendix specifically called out.**

### B — SUBJECT #510

**B-1 — ACCEPT AS AMENDED.** Conditional on T-1 as narrowed. The packet is
strong work — see §5 — and its defects are repairable without redesign.

**B-2 — THE COMPOSITION IS INSUFFICIENT AS DRAFTED. Take the repair, but a
NARROWER one than the packet names, and at the REAL price.** My ruling is by
construction (§1.3), not by preference between delta kinds:

* ADDED-only leaves canon holding a **direct scenario contradiction** (LA-F1) and
  an **orphaned closed-list obligation** (LA-F2).
* The packet's proposed repair — a scenario-complete MODIFIED restatement of the
  whole gate requirement — **is the right kind of instrument**, and it must
  indeed be scenario-complete: this estate has already proved that a MODIFIED
  delta restating a subset silently drops the rest (the archive that stopped
  itself over 1-of-8, PR #331). So the repair carries **all NINE scenarios**, not
  twelve, and not two.
* **But the repair is smaller than the packet fears in a second way:** only ONE
  scenario's TEXT changes (`a tranche-two link does not exist yet`), plus the
  scope-note sentence and the mapping table. The other eight ride verbatim as
  carry, which is bookkeeping, not authorship.

I record the alternative I considered and rejected: leaving ADDED and adding a
"reader's reconciliation" note. **Rejected** — it is precisely the *"two records
of one decision"* pattern, one level up. The reconciliation would live in a
requirement that the contradicted scenario does not reference, and canon would
still hold both.

**B-3 — D4 IS SOUND, AND IT IS THE BEST-ENGINEERED DECISION IN EITHER PACKET.**
The rule *"a dropped attestation is a BREAK, never a shorter chain"* IS enforced
by the drafted text, and I verified the enforcement rather than the slogan
(§1.8): the complete set is DERIVED BY THE GATE from the append-only log by a
**defined query**, EQUALITY is required in both directions, an enumerated record
with no leaf is REFUSED as UNPROVEN, and the residual is inherited from tranche
one rather than re-declared. The plural-predecessor gap in the ruled topic was
real and this is the correct closure of it.

**B-4 — NOT MY SEAT** (**lead-security**: the revocation-after-signing horizon is
a fail-closed-under-subtraction question). One architectural note: D6 is the
packet's own decision over a gap the ruling did not reach, it is flagged as such
(`tasks.md:2.5`), and that flagging is correct practice.

**B-5 — TWO OF THREE HOLD; ALL THREE HOLD ON MY AXIS.** §1.8. P1-2's repair is
exemplary and I could not break it. P1-3 resolves through a citation chain I
followed to ground. P1-1 is sound architecturally; its subtraction testing is
`lead-security`'s. **None was repaired by inventing vocabulary**, which the
packet claims and which I verified for all three.

**B-6 — R12 belongs to TRANCHE TWO, i.e. to #510, and it should be consumed
before ratification — but as a NAMED CARRY, not as four answers.** My grounds are
architectural, not chronological. R12 defers the attestation-envelope SIGNER and
names four questions — standard, key distribution, signature algorithm,
evidence-retention location. **Three of the four are exactly what #510's
requirements 1–4 decide**: where a signature happens, what key tier it uses, what
never enters a worker. R12's substantive rule — *"a holder signing its own
composition attests nothing an independent party can rely on"* — is the same
principle as #510's *"BIND BEFORE SIGN … the controller is a SIGNER, never a
notary."* They are one design, reached twice. Leaving R12 uncited invites a later
author to answer it a second time somewhere else, which is the family's own
two-records defect. **It does NOT belong to tranche one** (ratified without it,
and tranche one has no signer of its own — R12's naming of "PR #452" was written
before the tranche split was ruled). **It does not belong to tranche three**,
which anchors rather than attests. Not blocking: this is chronology, the
convergence is real, and a citation plus a task discharges it. See LA-A9.

**B-7 — THE SHORT IDS SHOULD STAND, AND A BACK-CITATION IS OWED.** Tranche one
marks both names *"(working id)"* on their face, so no fixed identifier was
breached and the shortening is lawful. The short ids are also better: they are
shorter, they are already cited across two packets and two README blocks, and
`add-chain-anchoring` is a capability name as well as a change name. **What is
owed is resolvability** — a reader grepping the ratified packet for its named
successor finds nothing. The cheap discharge is a one-line back-citation in
tranche one's `proposal.md:82-100` naming the ids as raised. I note that **#513
addresses this directly in `design.md` D6 and #510 does not** (verified by grep),
which is a small asymmetry worth correcting in #510 rather than a defect.

**B-8 — A DRAFT-STATUS PACKET ON `main` IS A SAFE OBJECT, AND #510's README ENTRY
IS UNUSUALLY GOOD AT MAKING IT ONE.** Read as a standalone entry it opens
*"`Status: draft` — NOT RATIFIED, filed FOR REVIEW"*, names the **two acts that
must follow, in order**, and records all three contested pulls including the
unresolved Q4 one. No schema byte moves; `contracts/` is untouched by the diff;
no bundle number is spent. The residual risk is not the README — it is LA-F6
(archive order), which is about what happens LATER, not about the draft sitting
on main. The tenant-voice reading of the same entry is
**company-policy-lead**'s.

### C — SUBJECT #513

**C-1 — (i) CORRECT AND FAITHFULLY RECORDED.** My grounds, in order.
(1) **There was no ruling to override** — verified in the topic itself: the
sentence sits in `## Conflicts`, with no disposition status, no date and no
`Dispositioned-by`, beside two siblings that DO carry stamps. (2) **The literal
constraint is unachievable, and I verified the mechanism rather than accepting
the assertion**: an append-only log's signed tree head commits to its whole
prefix by construction, so no lateness excludes an earlier leaf. A constraint
that cannot be executed is not narrowed by being decomposed; it is made
executable. (3) **The narrowing preserves what the constraint protects** — that a
false attestation must not become permanently backed as valid — via the
never-read-as-validation rule and the disclaimer carried in the checkpoint
record's own contract text. (4) **The rejected alternative is rightly rejected**:
a second validated-only tree reintroduces the two-records-of-one-decision defect,
which is the family's FIRST named risk, and loses the property that makes an
evidence plane worth having. (5) **It is recorded where it binds** — in the
requirement text (`:316`), not only in `design.md` and the PR.

I add one qualification for Brett rather than for the packet: the convening is
right that *recorded is not ruled*. #513 has correctly discharged the
contested-finding obligation, and what remains is his to notice, not a defect to
repair.

**C-2 — NOT MY SEAT** (**lead-security**; §4 assigns missing-witness semantics
there and calls it the sitting's largest security question). Architecturally I
note only that `455bbdaa`'s resolution — state in the anchor-state record, proof
material in the receipt, *"the receipt holding proof material and never state"* —
is the correct separation of concerns, and that the record it routes state to is
declared in the code surface.

**C-3 — THE EXPRESSION IS HONEST AND SAFE, AND ARCHITECTURALLY TRUE.** *"Sequencing,
not blocking"* at four sites, tranche two marked IN FLIGHT in the origin manifest
and the design's dependency table, and **only tranche one and the PKI plane named
as hard prerequisites**. I tested the claim rather than accepting it (T-2): no
requirement in `specs/chain-anchoring/spec.md` needs a link-4/5/6 record to
exist. The one residual coupling is that #513 cites `add-chain-attestation` by an
id that B-7/C-4 could still change — trivial, and it argues for settling B-7.

**C-4 — THE ASYMMETRY IS RIGHT, AND I ENDORSE IT.** A NEW capability gets a new
directory; an extension of an existing capability adds to it — even one not yet
promoted. `openspec/specs/chain-anchoring/` does not exist and no incumbent owns
commitments, receipts or anchors, so a new directory is correct. Forcing #513
into `signed-execution-chain` would bind a domain-facing anchoring layer to the
execution-chain capability's lifecycle for no reason and would double the
LA-F6 hazard. **The asymmetry is a consequence of the two changes being genuinely
different shapes, not an inconsistency.** Note that this is also why LA-F6 and
LA-F1/F2 touch #510 and not #513.

**C-5 — Within my charter, all four are sound; D-F is the one I checked hardest.**
D-B (structural payload refusal) and D-C (declared-construction refusal with its
residual) are decomposition decisions I accept: refusing by SHAPE rather than by
prose is the family's own doctrine and Q2 ruled expressly that *"the refusal is
the durable form because prose about where PHI may not go erodes and a validator
does not."* D-E (deferring the permissioned-ledger selection to realization) is
correct and is the same discipline I am imposing on #510 at T-1 — it names the
unbuilt dependency instead of guessing at it. **D-F respects the
do-not-edit rule**: the vendored study at
`ideation/staging/signed-execution-chain/chain-selection-study.md` is byte-identical
between `origin/main` and #513's head — the packet corrects the study's per-plane
key claim **in its own design record**, not in the research record. That is
exactly right: *a research record rewritten to agree with a later ruling stops
being evidence.* The substantive correctness of D-B/D-C is **lead-security**'s.

**C-6 — YES, #513 HOLDS THE POSTURE WITHOUT CONSTITUTIONALIZING IT**, and the
distinction is drawn where it belongs. The topic itself carries the standing
tension as *"ADVISORY to a future change rather than a bar on one"*, and #513
carries today's evidence-only posture as contract text without a
never-contract-code requirement and without gating a future adoption on the
study's trigger. A later author reading #513 finds a posture, not a prohibition —
which is what Q5 ruled.

**C-7 — D1 and D9 do NOT need rulings, on my axis.** D9 (*"a header is not
canonicality, so the receipt carries a fourth element"*) is a format decision
inside the packet's own declared surface, reached from the receipt's chain-agnostic
requirement, and it is exactly the class of decision a proposal is for. D1
likewise. **Routing every design note to a council would make the council the
author**, which is the failure mode `## Alternatives` sections exist to prevent.
The two the convening ADDED (C-1, C-3) were correctly added because each concerns
a relation to text OUTSIDE the packet's authority; D1 and D9 do not.

### X — CROSS-CUTTING

**X-1 — Partly mine; the systematic sweep is `lead-quality`'s row.** On my axis
the answer is favourable and I want it on the record: **the enforcement claims I
tested are DECLARED, not ASSERTED.** #510's realization dependencies are carried
as `[GATE]` tasks naming the unbuilt planes (`tasks.md:5.1-5.3`); the CA is
explicitly not created (*"This packet creates no CA"*); `design.md` D7 states
that neither plane is real in its own words. #513 defers the permissioned-ledger
selection to realization and declares the deletion residual it inherits rather
than papering it. **My one X-1 finding is LA-F2 in reverse**: promoted canon
would carry tranche one's assertion that the gate validates *"EXACTLY these
checks"* while #510's nine requirements add checks the list does not name — a
claim that outruns its own enumeration, created not by either packet's drafting
but by their composition.

**X-2 — Answered in full at §1.5.** Per packet, per authority: **#510 CONSUMES
five of six** (`trust-anchor` certificates and the conformance-declaration
technique, `identity-brokering`, `contracts/omnigent`,
`add-wallet-carried-review-authority`, tranche one's digest construction — every
one resolved by execution) **and MINTS one** — the evidence class, on the axis
where `trust-anchor-chain-custody.registry.yaml` is the ratified incumbent and
where one of the three minted members is that registry's expressly EXCLUDED
model. **#513 mints nothing.** This is the staged topic's FIRST named risk and it
is why LA-F3 is blocking: the topic's own words are that *"a new schema here
would be the 'two records of one decision' defect at contract scale"*, and
`tasks.md:4.2` currently routes the closure question to schema authoring, which
is where it would become a schema.

**X-3 — NOT SAFE AS IT STANDS; demonstrated, not argued.** §1.4. Both archive
orders succeed silently and produce different canon. This is the #502/#504 class
and the convening is right that neither packet may be delayed for those issues —
but a two-line ordering precondition in #510's own `tasks.md` closes the instance
without waiting for the general fix. See LA-A6.

---

## 4. VERDICTS — ONE PER SUBJECT

### #509 — **ACCEPT AS AMENDED**

The vendoring is sound in kind and the appendix is thirteen-for-sixteen accurate
against my own execution, but a mapping appendix is the one part of a brainstorm
that is not free-form, and three of its estate claims are false — a disposition
label moved from Q6 to Q2, a term attributed to the staged topic that the topic
never uses, and a date interval understated by four months and asserted twice.

### #510 — **ACCEPT AS AMENDED**

The packet is not premature and its engineering is largely excellent, but I
BUILT the canon it would promote and it holds two contradictory scenarios on one
fact pattern and an orphaned closed-list obligation; it mints an assurance
vocabulary on the one axis with a ratified closed registry; and it defers a
re-derivation that tranche one's own ratified task list says is owed at the
raising, which is now.

### #513 — **ACCEPT**

Its largest decision (D8) is a faithful, well-recorded narrowing of an UNRULED
design observation that the mechanics make literally unachievable; it consumes
the estate's vocabulary and mints none; its four inherited fixes hold on
inspection; and its dependency on an unratified sibling is expressed honestly and
is architecturally true. My one defect (LA-F7) is SHOULD-FIX and does not
condition acceptance.

### Amendments

**LA-A1 [510] — BLOCKING. Reconcile the two gate requirements with a MODIFIED
delta, not with prose.**
*Discharged by:* a `## MODIFIED Requirements` block over tranche one's *"A gate
validates the short chain as a hash-linked chain"*, **scenario-complete at all
NINE scenarios** (per the promotion-fidelity lesson of PR #331 — a MODIFIED delta
restating a subset silently drops the rest), whose only substantive change is the
`a tranche-two link does not exist yet` scenario and the links-1–3 scope
sentence. *Verifier that would close it:* re-run my §1.3 construction — archive
tranche one then #510 into a scratch tree and confirm that no two scenarios in
`openspec/specs/signed-execution-chain/spec.md` share an antecedent with opposite
consequents.

**LA-A2 [510] — BLOCKING. Repair the orphaned closed-list obligation.**
*Discharged by:* in the same MODIFIED delta, either (i) extend the mapping table
to cover #510's nine requirements and the checks they add, or (ii) re-scope the
clause from *"every requirement of this capability"* to the links the requirement
walks. **(i) is the better repair** — the table is the reader's index to where
each obligation is enforced, and losing that at eighteen requirements costs more
than at nine. *Verifier:* in the promoted file, every `### Requirement:` heading
appears in the mapping table or is named in a walked check.

**LA-A3 [510] — BLOCKING. Compose the evidence class with the ratified assurance
registry, or drop `hardware_attested`.**
*Discharged by:* (a) a design decision and a task naming
`contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml` and stating
whether the evidence class is a distinct axis or a facet of it; (b) if distinct,
adopting that registry's own pattern — an explicit `composes_with` statement and
a declared ordering, so the two sets *"cannot drift into two custody models"*;
and (c) either justifying `hardware_attested` against
`excluded_models: asserted_hardware_backing` and its ruled reasoning, or renaming
it to the property it actually asserts (independent observation), or dropping it
to two classes. *Verifier:* `grep` for the registry path returns non-zero in the
packet, and `tasks.md:4.2` names the registry as the input to the closure
decision.

**LA-A4 [510] — SHOULD-FIX. Correct "twelve scenarios" to NINE at all four
sites** (`design.md:114`, `design.md:124`, `tasks.md:99`, `proposal.md:243`).
*Discharged by:* the edit, plus a re-count. It rides with LA-A1 because the
figure prices LA-A1's discharge.

**LA-A5 [510] — BLOCKING (this is the T-1 narrowing). Perform the raising-time
re-derivation and cite the task that asks for it.**
*Discharged by:* a short, dated section in `design.md` or `proposal.md` that
(i) cites `add-signed-execution-chain/tasks.md:5.3` — *"Re-derive the tranche
two/three boundary against what actually exists **when each is raised**"* — by
path and text; (ii) states what actually exists TODAY (`implement-openxpki-install-repo`
ACTIVE at 22/30 with no CA operated; the omnigent family contracts and overlays
with no runtime enforcing a chain precondition) — which D7 already observes;
(iii) states the boundary derived FROM that, i.e. whether links 4–6+10 remain the
right tranche-two set given it, and names any link it would move; and (iv) keeps
`tasks.md:5.1` as the SECOND, realization-time re-derivation rather than as a
substitute for the first. **This is an act of authorship, not a re-ruling of Q4**
— Q4 stays exactly as Brett ruled it.

**LA-A6 [X, primarily 510] — SHOULD-FIX. Constrain the archive order.**
*Discharged by:* a task in #510's `tasks.md` stating that
`add-signed-execution-chain` archives BEFORE `add-chain-attestation`, with the
reason (whichever archives first CREATES the capability). *Verifier:* my §1.4
reverse-order archive, which currently produces a nine-requirement canon holding
only tranche two.

**LA-A7 [513] — SHOULD-FIX. Take the in-flight status out of normative text.**
*Discharged by:* at `spec.md:546`, `:604` and `:658`, citing the path
`ideation/brainstorm/medxchain-blockchain-medical-records.md` and its vendoring
PR **without** a status that expires — the in-flight caveat belongs in
`proposal.md` and the PR body, which already carry it. The commit's stronger half
(*"The obligation does not depend on the citation … the citation is PROVENANCE"*)
stays and is what makes this cheap.

**LA-A8 [509] — SHOULD-FIX. Correct the three mapping-appendix defects.**
*Discharged by:* (i) replacing *"Q2, ruled 2026-08-29 (CONFIRMED operative
form)"* with Q2's actual disposition status, *"ruled 2026-08-29 … AS
RECOMMENDED"* — and, if the CONFIRMED framing is wanted, attributing it to **Q6**
where it belongs; (ii) removing *"the property `signed-execution-chain` calls
chain inception's fidelity property"* or re-casting it as the vendoring author's
description rather than the topic's term, since the topic never uses it; (iii)
correcting *"eighteen months"* to roughly twenty-one, at both sites. *Verifier:*
each corrected phrase greps to a matching string in
`ideation/staging/signed-execution-chain/signed-execution-chain.md`, and the
interval recomputes from the Source block's own date.

**LA-A9 [510] — SHOULD-FIX. Consume R12 as a named carry.**
*Discharged by:* a citation of
`add-wallet-carried-review-authority/rulings-2026-08-29.md:191-199` in #510's
`proposal.md` or `design.md`, stating (i) that R12's no-self-attestation rule and
requirement 3's *"BIND BEFORE SIGN … never a notary"* are the same principle
reached twice, (ii) which of R12's four envelope questions this tranche's
requirements 1–4 already decide, and (iii) a task carrying the remainder. **Not
blocking:** R12 landed on main after the branch cut, and the substantive
convergence is already present in the drafted text.

**LA-A10 [510] — SHOULD-FIX. Add the back-citation for the change id.**
*Discharged by:* a line in `design.md` addressing the id question as #513's D6
does, plus (as a separate, later act on tranche one) a back-citation at
`add-signed-execution-chain/proposal.md:82-100` naming the ids as raised, so a
reader grepping the ratified packet for its successors finds them.

### Conditions attached to the record

**LA-C1.** My verdicts on #510 and #513 are given on the packets as they stand at
`e7f6ae0e` and `cf5a24b8`. **LA-A1 and LA-A2 are discharged by ONE MODIFIED delta
that must be scenario-complete**, and this estate has already proved that a
scenario-incomplete MODIFIED delta drops requirements silently and invisibly to
every count (PR #331). If the amendment is taken, **re-run the promotion
construction rather than reading the delta** — my §1.3 method — before the
resulting packet is ratified. A prescribed fix applied without a verifier is an
unverified change, whatever its provenance, and this one is prescribed by me.

**LA-C2.** My T-1 ruling of (c) rests on keeping Q4's OBJECT (the boundary)
distinct from the Exit path's OBJECT (the contract text). **If Brett rules that
Q4's object is the drafting act itself, my answer becomes (b) PREMATURE and my
#510 verdict becomes REFUSE AS DEFINED.** I state the hinge so the ruling can
turn on it directly. It does not touch #509 or #513.

**LA-C3.** LA-F3 (the minted vocabulary) is blocking at the PACKET stage
deliberately, because `tasks.md:4.2` currently routes the closure decision to
schema authoring. If it reaches the schema uncomposed, the second vocabulary is
shipped and the repair becomes a contract change rather than a paragraph. **This
is the cheapest moment it will ever be fixable.**

**LA-C4.** I recorded T-0(c) against the convening honestly, as asked: the
three-subject load degraded my reading of #509, and my decisive #510 finding cost
a build that equal pacing would not have funded. **If a future §7.4 sitting sits
over more than one object, it should say which object each seat is expected to
build rather than read.**

**LA-C5.** T-0(b) leaves `lead-security`'s dissent unresolved for a fourth
convening. Nothing turns on it here, which is why it should be settled here.

---

## 5. In the packets' and the changes' FAVOUR

A record listing only defects misreports what I read. What follows I verified,
not merely noted.

1. **#510's plural-predecessor closure (D4 / requirement 6) is the best piece of
   engineering in this sitting.** The bot found that *"a proper subset"* named
   nothing; the repair did not weaken the rule but supplied the missing
   authoritative set and specified the query producing it, required EQUALITY in
   both directions, refused an enumerated-but-unlogged record as UNPROVEN, and
   inherited tranche one's suffix-truncation residual rather than re-declaring it
   as new. **I tried to break it and could not.** That is a fix with a verifier
   built into it.

2. **#513's D8 is a genuine architectural advance over the text it narrows.** It
   found that a stated constraint described a control that cannot run against an
   append-only log, resolved it by decomposition rather than by weakening,
   preserved the protected interest, rejected the tempting alternative on the
   family's own first-risk ground, and recorded the narrowing in the requirement
   text where it binds. **The estate is better for the change than it was for the
   sentence.**

3. **The omnigent characterization is verbatim accurate.** I parsed the schema
   rather than reading the claim: closed six-boolean matrix,
   `additionalProperties: false`, `execute_final_action` and `access_secrets`
   both `const: false`, five archetypes. Every element as stated.

4. **Both packets decline to claim an approver and say why.** #513 goes further
   and cites the family's own corrected overstatement against itself: *"the
   drafting was commissioned by an orchestrating session, which is not Brett
   Heap's word."* This is a lesson carried rather than repeated, and it is the
   single most creditable sentence in either document.

5. **#510 puts the objection to its own existence FIRST and routes it unresolved.**
   `design.md` D7 states the literal reading of Q4, says the packet cannot rule it
   out, and sends it to the council. Its substantive argument — a boundary drawn
   against ratified vocabulary that names no interface is not a guess — is a
   **good** argument, it cites the precedent that supports it, and **I checked
   that precedent and it holds** (`contracts/trust-anchor/` ships nine schemas at
   `contract-v1.37` against a CA the family does not operate). It is why my T-1
   answer is (c) and not (b).

6. **Three of #513's four fix rounds hold under attack, and one of them corrected
   me.** `e1bd201d` claimed three sites; my first grep found two and I nearly
   filed an incomplete-fix finding. The third was line-wrapped. The commit did
   exactly what it said.

7. **`455bbdaa` routes state to a declared record, not an invented one.** The
   anchor-state record is in the code surface with its own value set, and the
   separation it establishes — *"the receipt holding proof material and never
   state"* — is the right one.

8. **#510's README entry is a model of what a draft-status entry should say.** It
   opens with NOT RATIFIED, names the two acts that must follow in order, and
   records all three contested pulls **including the one that could end its own
   round**. It does not read as a fait accompli.

9. **Both changes validate clean under `--strict`**, and both packets' headline
   counts (9/59 and 9/52) are accurate to my own count. The counting defect is
   confined to a claim about a THIRD document.

10. **#513 consumes and mints nothing**, carries requirement 9 as an explicit
    neutrality guard, respects the do-not-edit rule on the vendored study by
    correcting it in the packet's own design record, and expresses its dependency
    on an unratified sibling as sequencing — a claim I tested and found
    architecturally true rather than merely convenient.

11. **#509's mapping appendix is thirteen-for-sixteen accurate**, and it keeps
    Brett's speculative content and the vendoring author's estate claims cleanly
    apart — the estate claims are confined to a separately headed, separately
    dated appendix. Its `Source:` block is candid about what the vendoring is
    NOT, naming the OneNote original as the artifact of record for exact wording.
    **The three defects I found are in the author's appendix and none is in
    Brett's voice.**

12. **The convening disclosed against its own interest at §0.1, §0.3, §0.6 and
    §3.1, carried only two mechanical facts and labelled both, and told seats to
    re-verify them.** I did. **Both are correct.** The discipline is worth saying
    plainly: a packet that hands a bench its own possible unlawfulness as T-0 is
    a packet doing its job.
