Seat: lead-quality (domain seat) · Convening: gate_rules_council (§7.4 sitting), 2026-08-30
Packet: openspec/changes/add-chain-attestation/review/convening-packet-2026-08-30.md
Judged at: openxFactory main afe29561 / #510 e7f6ae0e / #513 cf5a24b8 / #509 26c7e778
codexFactory (read-only precedent) 3c71ddc9

# SEAT RETURN — `lead-quality` (LQ), domain seat

## 0. Persona declaration

My charter, quoted from codexFactory `hermes/domain/roles/lead-quality.yaml`:

```yaml
authority:
  owns: [branch_review, quality_gates, review_standards, test_adequacy]
  decides: [review_verdict, check_sufficiency]
  escalates:
    - trigger: standard_contested
      to: council_large
      then: gate_rules_seat
disposition: {rigor: high, risk_posture: averse, bias: quality, autonomy: moderate}
guardrail: character_never_overrides_authority
```

```
character_frame: Your creed is evidence before trust. You draw a bright line
between "not yet proven" and "broken," and you never let the first masquerade as
the second — a change is not rejected because it might be wrong, it is not
admitted until it is shown right. You are constructive but uncompromising: you
tell an author exactly what evidence would move you, so a "no" is always a map
to "yes." You take no pleasure in blocking and no shortcuts around it.
```

**Seat basis.** `gate-rules.yaml` `members.domain`, unconditional roster (packet
§3.3). I note without re-arguing it that Brett's S5 ruling R2 targets this seat
at `claude-sonnet-5` and that the target is not in force (packet §3.3, quoting
the ruling's own enforceability sentence); I sit at the enrolled selector, as
the convening decided.

**Assigned obligation.** Packet §4 `lead-quality` row (a)–(f) and the EVERY SEAT
row (i)–(iii). Every one is discharged below by execution.

**Boundary reading I take, stated openly.** My charter reaches `test_adequacy`
and `check_sufficiency`. Where a ballot question is about *whether a composition
is architecturally right* or *whether an authority was lawful*, I answer only
the limb that asks whether a claim is **checkable** and whether the drafted
scenarios **discharge** the requirement they sit under, and I name the seat that
owns the rest. I did **not** treat any prescribed bot-round fix as sound because
it was prescribed. The 2026-08-29 `lead-quality` seat recorded its own miss in
these words — *"I executed the CURRENT schema and did not execute the PRESCRIBED
one"* — and the rule that came out of it, *"a prescribed fix applied without a
verifier is an unverified change, whatever its provenance,"* is the rule I
applied to all seven inherited fixes below.

**Read-only discipline.** `git status --porcelain` was EMPTY in all five trees
(`invmain`, `inv510`, `inv513`, `inv509`, `sittingref`) **before** my work and
**empty again after**, verified by execution and reproduced in §1. I wrote
nothing to any checkout. All scratch is under `seat-scratch-LQ/`.

---

## 1. What I verified BY EXECUTION

### 1.1 Tree cleanliness, before and after

```
$ for d in invmain inv510 inv513 inv509 sittingref; do
    git -C $d status --porcelain | wc -l; git -C $d rev-parse HEAD; done
  invmain    0   afe29561a317853eb22f1e6b248f7029fa2fb2a7
  inv510     0   e7f6ae0e400719894fbaa0d14be274ba86b2e3b3
  inv513     0   cf5a24b89870a87663c595550210ee4deb0ac28e
  inv509     0   26c7e778682089789795befad4c28af509ff2706
  sittingref 0   3c71ddc910b8e0b119d0e1ee40a5523dfa294f07
```

Final check, after all work:

```
  invmain: porcelain lines = 0 ; HEAD = afe29561
  inv510:  porcelain lines = 0 ; HEAD = e7f6ae0e
  inv513:  porcelain lines = 0 ; HEAD = cf5a24b8
  inv509:  porcelain lines = 0 ; HEAD = 26c7e778
  sittingref: porcelain lines = 0 ; HEAD = 3c71ddc
```

### 1.2 (a) The validators — real output

```
$ openspec --version
1.2.0

# in inv510
$ OPENSPEC_TELEMETRY=0 openspec validate add-chain-attestation --strict
Change 'add-chain-attestation' is valid
EXIT=0

# in inv513
$ OPENSPEC_TELEMETRY=0 openspec validate add-chain-anchoring --strict
Change 'add-chain-anchoring' is valid
EXIT=0

# --all --strict, per tree
inv510 : Totals: 79 passed, 0 failed (79 items)
inv513 : Totals: 79 passed, 0 failed (79 items)
invmain: Totals: 78 passed, 0 failed (78 items)
inv509 : Totals: 78 passed, 0 failed (78 items)
```

**Totals I measure: 79 / 79 / 78 / 78.** Each chain branch adds exactly one item
to main's 78; #509 adds none, as a brainstorm vendoring should not.

Diff magnitudes, measured against the shared merge-base `b710976b`:

```
#510  7 files changed, 1741 insertions(+)      #513  7 files changed, 1884 insertions(+)
#509  1 file changed,   223 insertions(+)
```

All three match the packet's figures exactly.

### 1.3 (b) The counts, measured myself — script and output

I wrote `seat-scratch-LQ/count.py`: it walks each delta, records the `##
ADDED|MODIFIED|REMOVED` block, counts `#### Scenario:` per `### Requirement:`,
and captures the **first non-blank body line** of every requirement to test the
SHALL/MUST-on-line-one rule the OpenSpec parser enforces.

```
#510  openspec/changes/add-chain-attestation/specs/signed-execution-chain/spec.md
OK  L5   [ADDED] scen=5  kw=SHALL  The harness controller attests the environment it prepared
OK  L79  [ADDED] scen=10 kw=SHALL  A runner attestation is produced at the controller, on a recorded request
OK  L207 [ADDED] scen=5  kw=SHALL  The controller corroborates what it signs and never notarizes self-report
OK  L265 [ADDED] scen=5  kw=SHALL  A tier-2 attestation key never enters a worker, in every configuration
OK  L315 [ADDED] scen=5  kw=SHALL  Opening a pull request is a signed decision, bound to the chain
OK  L368 [ADDED] scen=9  kw=SHALL  The signed hash-link rule takes effect at link 4, and the gate walks the extended chain
OK  L497 [ADDED] scen=8  kw=SHALL  The chain completes at CLOSURE, and the governed post-merge test is what closes it
OK  L602 [ADDED] scen=6  kw=SHALL  A remediation chain is the one admitted consumer of an unclosed chain
OK  L670 [ADDED] scen=6  kw=SHALL  The executing layer refuses a step whose inbound chain does not verify
BLOCK ADDED: requirements=9 scenarios=59
TOTAL requirements=9 TOTAL scenarios=59

#513  openspec/changes/add-chain-anchoring/specs/chain-anchoring/spec.md
OK  L5   [ADDED] scen=8  kw=SHALL  The multi-anchor receipt format is defined FIRST and is chain-agnostic
OK  L104 [ADDED] scen=6  kw=SHALL  Both ruled witnesses anchor every anchored item, with no selectivity
OK  L179 [ADDED] scen=7  kw=SHALL  A missing witness is a declared, fail-closed state and never silently fine
OK  L277 [ADDED] scen=6  kw=SHALL  Only validated, gate-passed material is anchored AS AN ITEM
OK  L368 [ADDED] scen=7  kw=SHALL  The on-chain boundary is contract text carrying a refusing validator
OK  L466 [ADDED] scen=5  kw=SHALL  Consent state lives in the permissioned plane and only checkpoints are anchored
OK  L530 [ADDED] scen=5  kw=SHALL  Verification attempts and refused access are logged leaves
OK  L591 [ADDED] scen=4  kw=SHALL  The record and demographic planes are analyzable without the identity plane
OK  L643 [ADDED] scen=4  kw=SHALL  This capability is neutral and names no domain semantics
BLOCK ADDED: requirements=9 scenarios=52
TOTAL requirements=9 TOTAL scenarios=52
```

**#510's 9/59 and #513's 9/52 are CORRECT.** Every requirement carries SHALL on
its FIRST body line — no line-two keyword anywhere. Every requirement has ≥1
scenario; the minimum is 4. **Neither delta declares any block but `## ADDED
Requirements`** — I grepped for `^## (MODIFIED|REMOVED|RENAMED)` across both
`specs/` trees and found none, so `tasks.md:1.2` in each packet is true.

Every site where each packet states its own count is internally consistent with
my measurement:

```
#510 : proposal.md:199, tasks.md:16, README.md:399, INDEX.md:1907  — all "NINE ... 59"
#513 : proposal.md:310, tasks.md:24, README.md:468, INDEX.md:1916  — all "NINE ... 52"
```

### 1.4 (b) §0.4 RE-VERIFIED — the convening is RIGHT, and I confirm it independently

```
$ git diff --stat afe29561 e7f6ae0e -- openspec/changes/add-signed-execution-chain/
(empty)                # the two copies ARE byte-identical

#510's four "twelve" sites, located by grep — all four resolve exactly as §0.4 says:
  proposal.md:243   design.md:114   design.md:124   tasks.md:99

Tranche one, measured at origin/main afe29561:
OK L5   [ADDED] scen=6  Ratification presents wallet-carried authority, proven by possession
OK L103 [ADDED] scen=4  The actor a chain records is bound to the wallet that signed
OK L151 [ADDED] scen=6  Ratification and chain inception are one signed act
OK L241 [ADDED] scen=5  One digest construction governs every digest this capability computes
OK L305 [ADDED] scen=3  The signed ratification travels with the work
OK L337 [ADDED] scen=4  The signed transparency log is the record
OK L391 [ADDED] scen=9  A gate validates the short chain as a hash-linked chain   <-- THE SUBJECT
OK L557 [ADDED] scen=4  Ratifying authority is human-held
OK L613 [ADDED] scen=4  The capability confers and refuses nothing until a named reader runs as a required check
TOTAL requirements=9 TOTAL scenarios=45
```

**CONFIRMED: NINE, not twelve. No requirement in tranche one carries twelve. The
whole delta carries forty-five.** The overstatement is 33% on the single figure
that quantifies the cost of the alternative D3 argues against.

### 1.5 (b) §0.7 RE-VERIFIED — confirmed by my own execution

```
$ sed -n '185,192p' openspec/changes/add-signed-execution-chain/tasks.md   # on main
- [ ] 5.3 Neither successor's content enters this packet. Re-derive the tranche
      two/three boundary against what actually exists when each is raised, per
      the topic's Q4 — a tranche that depends on an unbuilt layer is a plan, not
      a tranche.

$ grep -ci "when each is raised|task 5.3" over both packets' four files
  proposal.md : #510=0  #513=0
  design.md   : #510=0  #513=0
  tasks.md    : #510=0  #513=0
  .openspec.yaml : #510=0  #513=0
```

**CONFIRMED. Zero hits in all eight files, and the ratified trigger reads "when
each is raised."** §0.5's R12 limb likewise confirmed: `R12` and
`rulings-2026-08-29` return 0 files in both packets.

### 1.6 (b) THE SWEEP OF EVERY OTHER NUMERIC CLAIM — and where the convening's own numbers fail

The convening said plainly it may have found only one wrong number. **It found
one and made two.**

| Claim | Where | My measurement | Verdict |
|---|---|---|---|
| "#510 cites `add-wallet-carried-review-authority` **five times**" | packet §0.5 | proposal 2 + design 2 + tasks 2 + `.openspec.yaml` 1 = **7** over the four files the convening names; **8** counting `spec.md` | **CONVENING WRONG, low by 2** |
| "#513 declares the relation as 'Sequencing, not blocking' at **four sites**" | packet T-2 | `grep -rio` returns **2** — `design.md:415`, `tasks.md:177` | **CONVENING WRONG, high by 2** |
| tranche one's gate carries **twelve** scenarios | #510 ×4 sites | **9**; delta total **45** | **PACKET WRONG** (§0.4 confirmed) |
| `implement-openxpki-install-repo` "**22/30**" | #510 proposal.md:103 | 30 boxes, 22 `[x]`, 8 `[ ]` | **CORRECT** |
| `add-identity-brokering` "**20/30**" | #510 proposal.md:185 | 30 boxes, 20 `[x]`, 10 `[ ]` | **CORRECT** |
| "Requirement 1, **all five** scenarios" (consumption of `add-trust-anchor`) | #510 proposal.md:183 | #510's own requirement 1 has **5** | **CORRECT** (the column is "where the delta consumes it") |
| "closed **six-boolean** matrix … **five** archetypes `frame/generate/verify/challenge/assemble_for_admission`" | #510 spec.md:274-279, :680-686 | schema `$defs/worker_class/properties/permissions`: `additionalProperties: false`, 6 required booleans, `execute_final_action`/`access_secrets` both `const: false`; `archetype.enum` = exactly those 5 | **CORRECT, verified against the schema** |
| "adds NO **sixth** archetype, NO **seventh** permission boolean" | #510 spec.md:681-684 | consistent with 5 and 6 measured above | **CORRECT** |
| "**984** admitted paths, 984 floored, 0 remaining" | #513 tasks.md:70-73 and README | verbatim at codexFactory `2026-08-28-seat-returns/README.md:110` and ballot `:100-101` | **quotation CORRECT**; but present-tense and **48 stale** — today `git ls-files openspec/changes` = **1032** |
| "2026-08-28 `gate_rules_council`, **unanimous 5/5**" | #513 tasks.md:73, README | record line 47: "**UNANIMOUS REFUSE, 5/5.**" | **CORRECT** |
| "SPLIT **2–2** … UNANIMOUS **4/4** … **fifteen** blocking amendments" | #513 tasks.md:12-14 | record lines 83 and 431, verbatim | **CORRECT** |
| "**eighteen months**" before the neutral family | #509 ×2, **#513 spec.md:658-659** | 2024-11-10 → 2026-08-29 = **657 days = 21 whole months** | **WRONG, understated by ~3.5 months** |
| "EDPB Guidelines 02/2025 (v2.0, **adopted 2026-07-07**)" | #513 spec.md:420-421 | study line 155: "Guidelines 02/2025 (v2.0 adopted 2026-07-07)" | **CORRECT** |
| "this chain's L1 prunes transaction data after roughly **three days**" | #513 spec.md:120-122 | study line 108: "Standard nodes retain ~**3 days** of transaction data" | **CORRECT** |
| fix commit "48 now, was 47" (`455bbdaa`) | commit message | 800158f0=47 → 455bbdaa=**48** | **CORRECT** |
| fix commit "52 scenarios now, was 48" (`2e539779`) | commit message | e1bd201d=48 → 2e539779=**52** | **CORRECT** |
| #510 fix round | `bf021888`=50 → `e7f6ae0e`=**59** | consistent with the 59 claimed | **CORRECT** |
| "its three named additions land as requirements **7, 8 and 9**" | #513 tasks.md:59-63 | #509 names three additions; #513 reqs 7/8/9 are attempt-logging, plane-analysis, neutrality-mapping | **CORRECT** |

### 1.7 (c) THE CLAIM-OUTRUNNING-THE-MACHINERY SWEEP — and the live ruleset read

I enumerated every place either packet asserts a gate, check, refusal or
enforcement, and classified each **DECLARED** (not-yet-existing, with a cite) or
**ASSERTED** (stated as fact). Both packets carry the doctrine in their own
evidence conventions, identically:

```
#510 tasks.md:9-12 / #513 tasks.md:17-20
"a box closes on a FACT that survives the session — a merged commit, a green run
named by id, a live API read, a file path — never on an intention and never on a
workflow file standing in for a ruleset state."
#510 tasks.md:157-159  "Until a running layer refuses, requirement 9 is UNMET rather
than partially met, and this packet claims no enforcement it cannot name a check for."
#510 tasks.md:178-180  "A merged workflow file is NOT evidence; the evidence is the
live ruleset state."
```

**Everything in the two spec deltas is DECLARED** — every refusal is a `SHALL`
obligation on a future realization, and §5 of each `tasks.md` gates realization
explicitly. My present-tense enforcement grep over both packets returned exactly
**one** live-enforcement assertion in normative text:

```
#510 spec.md:526-527  "the instrument is the one this repository already reads
                       inside a required check"
#510 proposal.md:187  "S2 issuer anchor REALIZED, read inside the REQUIRED
                       wallet-validation check"
```

I did **not** accept the workflow file. I read the **live ruleset**:

```
$ gh api repos/opensoft/openxFactory/rulesets/21538893
name: openxFactory wallet-gate (require wallet-validation)
enforcement: active
target: branch
conditions: {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}}
RULE required_status_checks {"required_status_checks":
     [{"context": "wallet-validation"}, {"context": "pytest-suite"}]}

$ grep -n "review-authority" .github/workflows/openxwallet-consumer-gate.yml
132: grep -qE '^note  intake register read: governance/review-authority/register\.yaml \([0-9]+ row\(s\)\)$' wallet-gate.log
133:   || fail "... the pinned reader did not resolve openxFactory's intake register at the scan target"
```

**ASSERTED AND TRUE, on a live ruleset read.** The check is required on the
default branch under an active ruleset, and the job asserts positively that the
pinned validator read `governance/review-authority/register.yaml`. This is the
one place either packet could have outrun its machinery, and it does not.

### 1.8 (f) #509 — the header contract and doc-health, executed

I ran the **enforcing code itself**, not the README's prose:

```
$ python3 -c "from ideation_dashboard import authoring; ..."
REQUIRED_HEADER_FIELDS = ('Status','Kind','Summary','Topics','Repository context','Captured')
BRAINSTORM_SUFFIX      = ' — Brainstorm'

ideation/brainstorm/notebooklm-import-test/notebooklm-ideas-2026-07-09.md
   missing -> ['Captured']                       # the ONE existing imported precedent
ideation/brainstorm/medxchain-blockchain-medical-records.md
   missing -> []                                 # #509

H1 = '# MedxChain — Blockchain-Backed Medical Record Fidelity — Brainstorm'
H1 ends with suffix -> True
```

`Kind: reference` is in the README's declared vocabulary (`architecture | plan |
process | runbook | report | register | template | reference`). `Status:
brainstorm` is the lifecycle's own word (`docs/document-lifecycle.md:41`). The
`## Possible feats` omission is inside the README's own carve-out —
*"Evidence/reference-gathering brainstorms may omit it."*

**doc-health, branch-vs-baseline, with the #342 hazard avoided** — I copied each
tree under a parent so both checkouts had basename `openxFactory`, since the
repo identity is derived from the basename:

```
$ basename A/openxFactory ; basename B/openxFactory   →   openxFactory / openxFactory
$ python3 scripts/doc-health.py --single-repo . --report-out lq-base.md        # main
$ python3 scripts/doc-health.py --single-repo . --previous-report lq-base.md \
      --new-findings-out lq-<n>-new.json                                       # each branch

  #509 : NEW FINDINGS count: 0
  #510 : NEW FINDINGS count: 0
  #513 : NEW FINDINGS count: 0
```

**Zero new findings on all three.** Both chain packets claim exactly this at
`tasks.md:1.5`, citing #342 by number; I reproduced it independently and their
claim is true.

### 1.9 (g) THE INHERITED BOT SURFACE — I read every commit and attacked the fixes

```
#510  bf021888  Draft tranche two            (50 scenarios)
      e7f6ae0e  Fix round: three records that named what they had to establish (59)
#513  800158f0  Tranche three builds to a ruled configuration       (47)
      455bbdaa  A pending witness contributes no receipt entry      (48)
      e1bd201d  Quote tranche one's digest rule in its own words    (48)
      2e539779  Take both Codex P1s and the Copilot cluster         (52)
      cf5a24b8  The in-flight citation says so in the requirement   (52)
```

Findings from attacking them are LQ-F9, LQ-F10, LQ-F15 and LQ-F16 below. Three
fixes I attacked and could **not** break — `e1bd201d`, `cf5a24b8` and #510's
P1-3 — are recorded in §5.

### 1.10 (d) SCENARIO-VERSUS-REQUIREMENT — the sample, hard

I read the requirement body and then every scenario under it for **six**
requirements (three per packet, the packet's floor) and swept the remaining
twelve for conjunct discharge. #510 requirements 1, 6 and 7; #513 requirements
1, 2 and 3. Results are LQ-F11 through LQ-F16 and LQ-F22.

### 1.11 (e) TASKS EXECUTABILITY

Both `tasks.md` files are dependency-ordered, gate-marked and evidence-bound to
an unusually high standard — #513's `4.5`–`4.9` name the evidence in terms (*"a
running node reachable by the anchoring subsystem, named by endpoint, not a plan
to run one"*; *"a receipt verified AFTER the operational chain has pruned the
transaction, which is the only test that actually proves retention"*). One task
in each is not checker-decidable; see LQ-F17.

### 1.12 Cross-cutting measurements

```
$ [ -d openspec/specs/signed-execution-chain ] → NO       # at main afe29561
$ [ -d openspec/specs/chain-anchoring ]        → NO
$ ls -d openspec/changes/*/specs/signed-execution-chain   # in inv510
    openspec/changes/add-chain-attestation/specs/signed-execution-chain
    openspec/changes/add-signed-execution-chain/specs/signed-execution-chain   # TWO
$ git diff --stat afe29561 cf5a24b8 -- ideation/staging/signed-execution-chain/
(empty)                     # #513 edits NOTHING in the staged topic dir, study included
$ git ls-files openspec/changes | wc -l  → 1032           # today, vs the quoted 984
```

---

## 2. Findings

### LQ-F1 [510] — OBSERVATION (confirms the convening)
**§0.4 is right and I measured it myself.** Tranche one's gate requirement
(`add-signed-execution-chain/specs/signed-execution-chain/spec.md:391`) carries
**nine** scenarios; the delta carries **forty-five**; no requirement in it
carries twelve. The two copies are byte-identical (`git diff` empty). #510
asserts "twelve" at `design.md:114`, `design.md:124`, `tasks.md:99`,
`proposal.md:243` — in the one paragraph where the number **is** the argument
(D3's cost of the MODIFIED alternative). My measurement governs and it agrees
with the convening's.

### LQ-F2 [X] — SHOULD-FIX (against the convening)
**The convening's own §0.5 and T-2 counts are wrong.** §0.5: "#510 cites
`add-wallet-carried-review-authority` five times" — measured **7** over the four
files it names (2/2/2/1), **8** with `spec.md`. T-2: "#513 declares the relation
as 'Sequencing, not blocking' at four sites" — `grep -rio` returns **2**
(`design.md:415`, `tasks.md:177`). Both substantive conclusions survive (neither
packet cites R12; #513 does declare the relation non-blocking), but the ballot
carries two figures nobody measured. **My measurements govern.**

### LQ-F3 [510][513] — OBSERVATION (in the packets' favour)
**Every count either packet makes about itself is CORRECT.** 9 ADDED / 59 and 9
ADDED / 52, consistent at all four sites each; SHALL on the first body line of
all eighteen requirements; ≥1 scenario on all eighteen; no `MODIFIED`/`REMOVED`
block anywhere; `--strict` green; `--all --strict` 79 vs main's 78 in each
branch. Every fix commit's own scenario delta verifies exactly (47→48→52;
50→59). This is the opposite of the defect the packet warned me to look for.

### LQ-F4 [509][513] — BLOCKING
**"Eighteen months" is wrong, and #513 carries the wrong number into NORMATIVE
requirement text.** #509 fixes its own anchor — *"arriving eighteen months
before the `signed-execution-chain` topic's 2026-08-29 clarify sitting"*
(`:102-104`), repeated at `:207`. From the notes' own authoring date
2024-11-10 to 2026-08-29 is **657 days = 21 whole months**. #513
`spec.md:658-659` restates it inside requirement 9: *"predating the neutral
family by eighteen months."* A wrong figure in a brainstorm is a small thing; the
same wrong figure inside a requirement body is a spec defect, and it arrived
there by inheritance, which is the propagation path this estate keeps meeting.

### LQ-F5 [509] — BLOCKING
**A ruled disposition's label is attached to the wrong Q.** #509 `:146-147`:
*"Q2, ruled 2026-08-29 (**CONFIRMED operative form**), requires salted keyed
commitments … and the ruled boundary buys **erasure by salt destruction**."*
Measured in the topic at main:

```
:568  Q2  Disposition status: ruled 2026-08-29 — Brett Heap, in session; AS RECOMMENDED
:753  Q6  Disposition status: CONFIRMED 2026-08-29 — Brett Heap, in session; AS
          RECOMMENDED, and this is the ruling's OPERATIVE FORM
:757  Q6  "... and salt destruction as the erasure mechanism."
```

"CONFIRMED … operative form" is **Q6's status verbatim**, and salt-destruction
erasure is **Q6's** ruled property. Q2 is the boundary and is `AS RECOMMENDED`.
This is not Brett's 2024 speculation — it is the vendoring author's 2026-08-29
appendix asserting a fact about the estate, and per packet §1.3 the mapping
appendix is *"the one part of a brainstorm document that is not free-form."*
(Q2 **does** require salted keyed commitments and **does** cite EDPB 02/2025
v2.0 — the substance survives; the label and the erasure attribution do not.)

### LQ-F6 [509] — BLOCKING
**Two phrases presented as what the topic "calls" something do not exist
anywhere in the repository.** Case-insensitive, repo-wide over `*.md`:

```
"commitments + anchoring"       → 0 files, 0 hits in the topic   (#509:115)
"fidelity property"             → 0 files, 0 hits in the topic   (#509:131)
"chain inception"               → 3 files, 0 hits in the topic
```

#509 writes *"the same pattern `signed-execution-chain` **calls** the commitments
+ anchoring pattern"* and *"the property `signed-execution-chain` **calls** chain
inception's fidelity property"*, and its own appendix says it *"cites
`ideation/staging/signed-execution-chain/signed-execution-chain.md` by its
section and question anchors."* Neither name is that document's. `chain
inception` is real vocabulary — it is tranche one's, minted at main commit
`91cf0a46` — but it is not the topic's and there is no "fidelity property"
anywhere.

### LQ-F7 [509] — OBSERVATION (in the packet's favour)
**The rest of the mapping appendix verifies, target by target.** See the A-3
table in §3. Claim 2, claim 3 and claim 4 exist and are quoted **verbatim**;
`"So the split is"` is a real table at `:346`; `"The on-chain layer, as ruled"`
(`:205`) and `"What goes on chain, and what must not"` (`:326`) exist; *"ten
links"* is the topic's own first line of `## The chain` (`:78`, "Ten links.");
claim 6 is the transparency log; and the claim that tranche 3 *"does not yet
name this consumer"* is TRUE — `meta-analysis` returns **0 hits repo-wide**.

### LQ-F8 [509] — OBSERVATION (in the packet's favour)
**#509 passes the code-enforced header contract where the one existing imported
precedent fails it.** `missing_required_headers` returns `[]` for #509 and
`['Captured']` for `notebooklm-ideas-2026-07-09.md`. The README's
imported-evidence sentence offers `Source workspace:` / `Source workspace id:` /
`Origin:` *"instead"* of `Captured:`, but those three fields are NotebookLM-shaped
and `REQUIRED_HEADER_FIELDS` requires `Captured` unconditionally — the README and
the code diverge. #509 satisfies the code and supplies provenance through the
`Source:` line `render_scaffold` exists to emit (`authoring.py:112`, *"the
provenance citation"*). The divergence is the repo's, not the packet's.

### LQ-F9 [510] — BLOCKING
**The P1-1 attribution fix leaves two scenarios with opposite consequents on the
same antecedent, and nothing distinguishes them.** Requirement 2 now reads
(`spec.md:110-114`) *"the controller SHALL **ATTRIBUTE** every signing request TO
THE TASK IT PROVISIONED IN LINK 4, SHALL **REFUSE** a request it cannot so
attribute."* Its own residual (`:123-133`) then says a realization whose platform
cannot attribute *"DECLARES it and the affected attestations are **refused for
uses requiring per-task attribution**"* — a use-time refusal, not a sign-time
one. Both are scenario'd, in opposite directions:

```
:159  WHEN a caller the controller cannot attribute to a task it provisioned in link 4
      submits a payload that matches the setup attestation
      THEN the request is REFUSED and no signature is produced

:177  WHEN a realization's platform cannot attribute a request to one provisioned task
      THEN it DECLARES that shortfall ... AND the affected attestations are refused
      for uses requiring per-task attribution, the declaration leaving the realization conformant
```

The intended distinguisher is presumably *this request* versus *this platform*,
but it is nowhere in the requirement body, and a validator author reading only
this text cannot decide which branch governs a platform that cannot attribute
**any** request — which is the ordinary case, since the requirement itself says
the obvious mechanism is constitutionally unavailable (`access_secrets: false`).
The bot round asked for a refusal and got a refusal beside a conformant
declaration.

### LQ-F10 [510] — BLOCKING
**The P1-2 fix moves the attack rather than closing it, at the horizon that
matters.** The derived-set repair (`spec.md:400-412`) defines the authoritative
set as *"every leaf of the link-5 record kind committing to this chain identity,
**at or before the successor's own leaf**"* and refuses a successor whose
enumeration is not EQUAL to it. **Nothing in the delta requires a link-5 leaf to
be written before its link-6 successor's leaf.** I grepped: the only ordering
language is `:452` (predecessor *sequence* across executions) and `:409` itself.
So a lane that wants to drop an unwanted attestation no longer omits it from the
submission — it **defers writing its leaf** until after link 6's. The query then
excludes it, the enumeration is EQUAL, and the **gate passes**. Closure (link 10)
would catch it, because its own query window is wider — but by the packet's own
two-horizon doctrine (`:538-546`, *"A MERGE THAT ALREADY HAPPENED IS NOT
RETROACTIVELY REFUSED"*) the merge has landed. The P1 was raised because *"the
rule passed the exact chain it was written to refuse"* at the **gate**; after the
fix, a variant still does.

### LQ-F11 [510] — SHOULD-FIX
**Three of #510's fifty-nine scenarios are not testable as written.** Their THEN
is a reader correction with no actor and no system consequent:

```
:575  THEN it is corrected: closure establishes PROVEN REVIEW AUTHORITY and not per-seat signatures
:599  THEN it is corrected to a REFUSING state
:728  THEN it is corrected to a refusal
```

No check can run *"a reader is corrected."* Each states a true and useful thing
about how the record must be read; none is a scenario. #513 has **zero** of these
(`grep -c "THEN it is corrected"` = 0), which shows the house can write them the
other way. A 59-scenario packet that includes three assertions-as-scenarios
proves 56.

### LQ-F12 [510] — SHOULD-FIX
**Requirement 6's two conjuncts are unevenly discharged.** Its SHALL line
(`:370-375`) requires every signature from link 4 onward to cover *"(a) THE CHAIN
IDENTITY … and (b) THE DIGEST OF ITS PREDECESSOR."* Conjunct (a) has a direct
omission scenario (`:444`, "a signature from link 4 onward omits the chain
identity"). Conjunct (b) has scenarios for its **construction** (`:474`) and for
its **subject naming** (`:480`) and **none for its absence**. This is the
two-conjunct discharge family the estate recorded at FR-008.

### LQ-F13 [510] — SHOULD-FIX
**Requirement 7 asserts a three-way distinction and scenarios two of it.**
`:548-552`: *"MISSING, FAILED AND UNSIGNED ARE THREE OUTCOMES AND ARE RECORDED AS
THREE."* Scenarios cover missing (`:584`) and unsigned (`:578`). **FAILED has
none** inside requirement 7, and no scenario tests that the three are not
collapsed — which is the property the paragraph exists to protect.

### LQ-F14 [513] — SHOULD-FIX
**Requirement 2 declares three conditions non-optional and scenarios two.**
`:116-119`: *"THE OPERATIONAL WITNESS IS ADOPTED UNDER THREE CONDITIONS AND NONE
OF THEM IS OPTIONAL"* — an archival node; capture-and-retain of inclusion proofs
at anchor time; corroborating-never-sole. Inclusion-proof capture is scenario'd
(`:161`), corroborating-only is scenario'd (`:167`). **The ARCHIVAL NODE
condition has no scenario at all.** It is the condition the study says is hardest
to satisfy (study `:108`, *"archival nodes, which are hard to run"*) and the one
`tasks.md:4.5` marks `[OPERATOR]`. The contract text obliges it and nothing tests
it.

### LQ-F15 [513] — SHOULD-FIX
**The four-element receipt is refused on two elements, and the realization
enumerates three.** `2e539779` added chain-acceptance evidence as the fourth
per-chain element, but requirement 1's **capture-time refusal sentence**
(`:21-24`) was not updated with it and still reads *"A receipt that omits the
**transaction bytes or the inclusion proof** … SHALL BE REFUSED AT CAPTURE
TIME."* The **block header** has no capture-time refusal in requirement 1. Whole
capture is enforced — but in **requirement 3** (`:214-217`), not where the
refusal lives. And `tasks.md:4.2`'s negative-example list enumerates *"a receipt
missing inclusion proof; a receipt missing transaction bytes; a receipt missing
chain-acceptance evidence; a receipt whose header is non-canonical"* — **no
missing-header example**, so the realization would package 3 of 4. This is
precisely the carry-forward defect `2e539779`'s own message names: *"a correction
stated in a new paragraph does not retire the wording that caused it elsewhere in
the packet."* The fix diagnosed the pattern and then repeated it one requirement
away.

### LQ-F16 [513] — SHOULD-FIX
**A named receipt element has zero coverage.** Requirement 1 defines the receipt
as *"the anchored DIGEST, then the **AGGREGATION MERKLE PATH** from that digest
to the aggregated root, then a PER-CHAIN LIST…"* (`:9-11`). No scenario tests a
receipt with a missing, malformed or non-verifying aggregation path, and
`tasks.md:4.2` names no negative example for one. For a design whose durability
witness is *aggregated* by construction, the aggregation path is the load-bearing
element between the item and the anchor.

### LQ-F17 [510] — SHOULD-FIX
**One task states an obligation no checker can decide.** `tasks.md:149-152`:
*"5.1 **[GATE]** Re-derive the tranche boundary against what actually exists
**when the omnigent layer and the PKI plane are real** … This obligation
survives ratification deliberately: a packet cannot discharge it."* There is no
predicate for "real", no artifact the re-derivation must produce, and no
completion evidence — so nothing can ever decide that 5.1 is due or done, and it
will sit `[ ]` forever without anyone being wrong. Contrast 5.2, which names the
evidence (*"issuance evidence `add-trust-anchor` requires"*), 5.3 (*"Until a
running layer refuses"*), and #513's `4.5`–`4.9`, which are exemplary. **This
matters beyond bookkeeping: T-1 turns on this obligation, and the packet's answer
to T-1 is to carry it as a gate — a gate whose trigger is undefined.**

### LQ-F18 [X] — OBSERVATION
**§0.7 and §0.5's R12 limb both CONFIRMED by my own execution** (output at §1.5).
Tranche one's ratified `tasks.md:5.3` reads *"when each is raised"*; zero hits
across all eight files; zero R12 citations in either packet.

### LQ-F19 [X] — OBSERVATION (strongly in the packets' favour)
**Neither packet outruns its machinery, and the one live claim survives a ruleset
read.** Full sweep at §1.7. Everything in both spec deltas is a `SHALL` on a
future realization, gated in §5 of each `tasks.md`; both packets state the
workflow-file-is-not-evidence doctrine in their own evidence conventions; #510
`tasks.md:157-159` says in terms *"this packet claims no enforcement it cannot
name a check for."* The single ASSERTED live claim — that review authority is
*"read inside a required check"* — is **true against ruleset 21538893, active, on
`~DEFAULT_BRANCH`, `required_status_checks: wallet-validation, pytest-suite`**,
with the job asserting positively that the register was read
(`openxwallet-consumer-gate.yml:132`). On this family, the estate's most-recorded
defect, I found nothing blocking in either packet.

### LQ-F20 [513] — SHOULD-FIX (small)
**A quoted measurement is restated in the present tense and is 48 stale, in the
README.** `tasks.md:70-73` and the README record entry both say *"984 admitted
paths, 984 floored, 0 remaining **on this repository's real tree**."* The
quotation is verbatim and correctly attributed. But the tree has moved: today
`git ls-files openspec/changes` = **1032**. The conclusion is unaffected — more
paths strengthen it — but the README speaks outside the engineering conversation,
and a present-tense count there should be a count of today or be dated.

### LQ-F21 [X] — OBSERVATION (in all three packets' favour)
**doc-health branch-vs-baseline: ZERO new findings on all three subjects**, run
with matched checkout basenames so #342's phantom-regression hazard cannot fire.
Both chain packets claim exactly this at `tasks.md:1.5` and cite #342 by number;
I reproduced it independently and the claim holds.

### LQ-F22 [510] — BLOCKING
**A decision the packet routes to this council for a ruling has zero scenario
coverage.** `tasks.md:2.5` asks the sitting to rule on *"the
revocation-after-signing horizon (`design.md` D6)"*. The contract text is
`spec.md:41-47` — *"a certificate already revoked at signing makes the
attestation refused outright. A certificate revoked AFTER a signature was made
does not retroactively unmake an act the gate already permitted."* Requirement 1
has **five** scenarios and **none of them is about revocation**:

```
REQ 1 scenarios: no anchor held · host-held custody for hardware assurance ·
  no issuance provenance · link 4 absent · empty setup attestation
```

The only revocation scenario in the whole 59 is `:566`, under requirement 7, and
it is about **review-grant** revocation — a different subject. The paragraph also
carries no `SHALL`. So the bench is asked to rule on a decision whose text is
untestable prose. I cannot certify check sufficiency for something with no check
to be sufficient.

---

## 3. Positions on the ballot questions

### T — THRESHOLD AND SITTING

**T-0(a) — Is a §7.4 proposal review within this council's reach?** **(i) — this
council extends to it.** My charter's `owns` is `branch_review, quality_gates,
review_standards, test_adequacy` and my `decides` is `review_verdict,
check_sufficiency`. A proposal review is a branch review against review
standards; it is the thing this seat is defined to do, whatever the council's
`scope:` line says about rule-setting. I record the honest limit against my own
answer: the 2026-08-29 sanction was given for a sitting over **one** subject, and
this is three, so (a) and (c) are not independent.

**T-0(b) — Was declining the CSC seat right, and is the ground *false* or
*inapplicable*?** **NOT MY SEAT — it belongs to `lead-security`**, whose
2026-08-29 dissent on `seat_resolution.py:40-44` is the live text and whose
obligation here (§4) explicitly carries the exposure reading. I record only the
mechanical fact I can measure: none of the three PRs touches
`scripts/merge_master/**`, `.github/workflows/**`,
`hermes/domain/review-councils/**` or `schemas/**` — all three touch only
`openspec/changes/**`, `ideation/**` and `README.md`.

**T-0(c) — Was combining three subjects lawful, and did it degrade my reading?**
Answered honestly and against the convening. **It did not degrade the mechanical
half** — validators, counts, first-line keyword checks, doc-health and the
ruleset read are cheap and I ran all of them on all three subjects to
completion. **It did compress the judgement half.** Obligation (d) asks me to
sample "at least three requirements per packet"; I read six requirements'
scenarios against their bodies in full and swept the other twelve for conjunct
discharge rather than reading each with the same care. On one subject I would
have read all eighteen the deep way, and LQ-F12/F13/F14 tell me that method
finds things. So: **lawful in my view, and lossy in a way I can name.** I also
record the one argument the other way that I verified: #513's requirement text
cites #509's file at three sites, so a seat judging #513 without #509 could not
have checked them.

**T-1 — Is #510 PREMATURE?** My limb is testability, and I answer **(a) NOT
PREMATURE, with a caveat that is mine to raise.** The drafting question — does
Q4 forbid writing tranche two's text today — is `lead-architect`'s first
(packet §4). On my limb: the packet's own answer is to carry the obligation as
an undischargeable gate at `tasks.md:5.1`, and **that gate is not decidable**
(LQ-F17) — no trigger predicate, no completion evidence. A packet that answers a
prematurity objection with a gate owes a gate that can close. I do **not** think
this makes the packet premature; I think it makes the answer to prematurity
unverifiable, which is repairable in one edit. I also record what I verified in
§1.5: the only text in the estate that fixes a trigger is tranche one's ratified
`tasks.md:5.3`, *"when each is raised"* — and **#510 is the raising**, and does
not cite it.

**T-2 — Does a ruling on #510 bind #513?** **NO, on my limb.** I read #513's
entire `spec.md`: it cites the staged topic, the vendored study, #509,
`add-trust-anchor` and tranche one — and **no requirement of #510**. Its
prerequisites are declared as tranche one and the PKI plane (`tasks.md:6.1`,
`6.2`) with #510 marked *"Sequencing, not blocking"* (`tasks.md:177`,
`design.md:415` — two sites, not four, LQ-F2). #513 also creates a **new**
capability directory, confirmed absent at main, so it shares no delta surface
with #510. Nothing in #513 becomes untestable if #510 ends.

**T-3 — Was the drafting authorized?** **NOT MY SEAT** — it belongs to
`company-policy-lead` (the tenant voice on whose word a packet stands) with the
convener. I record only that both packets' disclaimers are verifiable as written
and that neither claims an approver.

### A — SUBJECT #509

**A-1 — PROVENANCE FIDELITY. YES, and it is careful.** The `Source:` block
(`:16-24`) names the author (Brett Heap), the authoring date (2024-11-10), the
original artifact (OneNote), the share date (2026-08-29), the transport (session
transcript), **exactly what was normalized** (page footers, orphaned
bullet/number fragments, duplicated headers) and — the part I weigh most — it
declines to claim byte-fidelity: *"this vendoring reconstructs the notes' section
structure and enumerated claims from that transcript rather than reproducing
byte-identical prose."* Brett's material is `## Overview` through `## Access
Control Logging` (`:26-98`); the vendoring author's framing is the appendix from
`:100`, headed and dated *"— 2026-08-29"*. **Distinguishable.** Not blocking on
A-1. But note where the defects are: **all three of LQ-F4/F5/F6 are in the
appendix**, which is the half that is not Brett's.

**A-2 — INVENTED CLAIMS. YES, three, all in the appendix and all verified by
executing a search.** LQ-F4 (the eighteen-month figure — 21 measured), LQ-F5 (Q6's
`CONFIRMED … OPERATIVE FORM` label and Q6's erasure property attached to Q2),
LQ-F6 (two names presented as the topic's that return 0 hits repo-wide). **Brett's
own 2024 content is not judged and I judge none of it** — the PIIDB-on-chain
design, the IPFS anchoring, the HIPAA audit positioning are all legitimate
brainstorm speculation and the document itself already marks them as superseded
in its "three 2026 upgrades" section.

**A-3 — MAPPING ACCURACY.** Every target, with a cite per row:

| # | What #509 asserts | Cite | Measured at main | Verdict |
|---|---|---|---|---|
| 1 | topic §"The on-chain layer, as ruled" exists | :117 | heading at `:205` | **TRUE** |
| 2 | topic §"What goes on chain, and what must not" exists | :160 | heading at `:326` | **TRUE** |
| 3 | topic §"So the split is" is a table | :128 | `:346` + a 6-row table | **TRUE** |
| 4 | the topic **calls** it the "commitments + anchoring" pattern | :115 | **0 hits repo-wide** | **FALSE** (LQ-F6) |
| 5 | the topic **calls** it "chain inception's fidelity property" | :131 | `"fidelity property"` 0 hits repo-wide; `"chain inception"` 0 hits in the topic | **FALSE** (LQ-F6) |
| 6 | claim 6 is the transparency log | :136 | claim 6 = *"The evidence plane is OFF chain, and it is the record… signed transparency log"* | **TRUE** |
| 7 | Q2 quotation *"off chain: every payload without exception… on chain: salted keyed commitments… and the chain anchors"* | :121-123 | Q2 disposition `:569-574`, wording matches | **TRUE** |
| 8 | Q2 label = "CONFIRMED operative form" | :146 | Q2 `:568` = **AS RECOMMENDED**; that label is **Q6's** `:753-754` | **FALSE** (LQ-F5) |
| 9 | Q2's boundary "buys erasure by salt destruction" | :148-150 | erasure-by-salt-destruction is **Q6's** ruled property `:757-760` (topic prose `:341-344` does attach it to the on-chain row) | **MIS-ATTRIBUTED** (LQ-F5) |
| 10 | EDPB Guidelines 02/2025 (v2.0), hash of personal data is personal data | :147-149 | Q2 explanation `:566-567`; study `:155` | **TRUE** |
| 11 | Q3 ruled 2026-08-29 in two rounds; Kaspa first; Bitcoin/OTS on every item; three conditions; no selectivity; no third chain | :171-181 | Q3 `:609-659`, all six elements present | **TRUE** |
| 12 | claim 2 names HealthLinc, *"pushed to the patient app, or printed as signed orders"* | :201-205 | claim 2 `:423-426`, **verbatim** | **TRUE** |
| 13 | claim 3's LedgerLinc is the financial analogue | :206-207 | claim 3 `:427-429` | **TRUE** |
| 14 | claim 4's *"two mappings are the same shape"* argument | :207-208 | claim 4 `:430`, **verbatim** | **TRUE** |
| 15 | the topic's **ten links** are framed around what was signed and produced | :197-198 | `:78` "Ten links." | **TRUE** |
| 16 | tranche 3 does not yet name the meta-analysis consumer | :190-193 | `meta-analysis` = **0 hits repo-wide** | **TRUE** |
| 17 | the 2026-08-29 sitting ruled Q2, Q3 and Q6 | :103-104 | all three ruled that day (all seven were) | **TRUE, partial** |

**Fifteen of seventeen check out; two are false and one of those two is a
disposition label.**

**A-4 — LIFECYCLE CONFORMANCE. YES.** All six `REQUIRED_HEADER_FIELDS` present
(`missing_required_headers` → `[]`), H1 carries ` — Brainstorm`, `Kind:
reference` is in the declared vocabulary, `Status: brainstorm` is the lifecycle's
own word. Compared against the one existing **imported** brainstorm
(`notebooklm-import-test/notebooklm-ideas-2026-07-09.md`), #509 is **more**
conformant, not less — the precedent is missing `Captured` outright. The README's
imported-evidence provision offers three NotebookLM-shaped fields *"instead"* of
`Captured:`; #509's material is not a NotebookLM export and it supplies provenance
through the `Source:` line `render_scaffold` emits for exactly that purpose. The
one thing the precedent has that #509 lacks is an imported-evidence disclaimer
paragraph — a precedent, not a contract, and I raise it only as LQ-C2.

**A-5 — Is a council the right instrument for a brainstorm vendoring?** Answered
against the convening's interest, and the evidence points **both ways, which is
the honest answer**. For lifecycle and header conformance: **no council was
needed** — `authoring.py` and doc-health decide it mechanically and both pass, and
a council that only ran those checks would have added nothing. For the mapping
appendix: **a council was the right instrument, and nothing else in this estate
would have caught it** — LQ-F4/F5/F6 are three false statements about ruled
dispositions that no running check reads. So my answer is: **yes for this
document, and the finding is not that brainstorm vendorings need councils but
that appendices asserting ruled facts have no checker.** The durable repair is
LQ-C3, not a standing council.

### B — SUBJECT #510

**B-1 — The packet as a whole.** **ACCEPT AS AMENDED**, on the three blocking
amendments below. I record explicitly, in the 2026-08-29 formula: **the text as
drafted is not ratifiable**, and the packet as an object stands.

**B-2 — D3, the ADDED-not-MODIFIED gate composition.** The composition question
is `lead-architect`'s. On **my** limb — `check_sufficiency` — I support **ADDED**:
a `MODIFIED` block restating a requirement that `openspec/specs/` does not hold
would be checked by nothing until promotion, its correctness would depend on
archive order, and the #329/#330 scenario-loss class is a measured precedent in
this repository, not a hypothesis. **But the cost figure the argument rests on is
wrong at all four sites and must be corrected regardless of which way the bench
rules** (LQ-A1). If the bench takes the named repair, the restatement carries
**nine** scenarios, not twelve — and a repair briefed at twelve that lands nine
would itself trip the promotion-fidelity family.

**B-3 — D4, the plural-predecessor enumeration.** Sound in principle;
**not fully enforced by the drafted text.** *"A dropped attestation is a BREAK,
never a shorter chain"* holds against **omission from the submission** — the fix
works, and it is a real repair. It does **not** hold against **deferral of the
leaf** past the successor's, at the gate horizon (LQ-F10). That is the amendment.

**B-4 — D6, the revocation-after-signing horizon.** **I cannot certify it,
because there is nothing to certify** — the decision routed to this council has
zero scenarios and no `SHALL` (LQ-F22). The doctrine it states is consistent with
requirement 7's two-horizon paragraph, so I expect the bench to like it; I am
saying it is untested, not that it is wrong.

**B-5 — The three closed P1s: do the repairs hold *as applied*?** I read
`e7f6ae0e` and `design.md` D10 and attacked each.
- **P1-1 (attribution): DOES NOT HOLD as applied** — LQ-F9, two scenarios with
  opposite consequents on the same antecedent.
- **P1-2 (the derived complete set): DOES NOT HOLD as applied** — LQ-F10, the
  attack moves from omission to deferral and the gate horizon loses it.
- **P1-3 (closure establishes review AUTHORITY, not bytes): HOLDS.** I tried to
  break it and could not. The instrument it names is real, shipped, and — I
  checked the **live ruleset**, not the workflow file — read inside a check that
  is genuinely required on the default branch (§1.7). Its residual (per-seat
  signatures) is declared with a walked link-7 check named as the closer, and
  the standing-at-exercise scenario (`:566`) is a real refusal.

**B-6 — R12 and the four S5 envelope questions.** Substance belongs to
`lead-security` (the no-self-attestation rule) and `lead-architect` (which tranche
carries it). My contribution is the measurement: **0 citations of R12 or
`rulings-2026-08-29.md` in either packet**, and it is chronology — R12 landed on
main after both branches cut from `b710976b`.

**B-7 — NAMING.** Not primarily mine. One measurable point: tranche one marks
both successor ids *"(working id)"*, so nothing is breached, and the cost is
**resolvability** — a reader grepping the ratified packet for its named successor
finds no such change. **Nothing in this estate checks that**, so if the short ids
stand, the back-citation is the only mechanism and it should be owed.

**B-8 — Does landing a draft governance packet on `main` commit anything?**
**No, on every check I can run.** `contracts/` is untouched by either diff; no
`openspec/specs/` directory is created; `openspec validate --all --strict` is
green at 79 in each branch; doc-health returns **zero** new findings; and both
README entries carry explicit draft framing to a reader who reads only that
entry — #510: *"`Status: draft` — NOT RATIFIED, filed FOR REVIEW"*; #513:
*"`Status: draft` — RATIFICATION IS NOT SOUGHT BY THIS PACKET'S LANDING."*
`target_release` is deliberately unnumbered in both. **A draft-status packet on
`main` is a safe object here.** (The one thing that does reach a public surface
is LQ-F20's stale 984.)

### C — SUBJECT #513

**C-1 — D8, the two-anchor narrowing.** **`lead-architect`'s** (packet §4 assigns
it). My limb: the narrowing is **recorded, not silent** — it is in requirement
text (`spec.md:316-323`, *"THIS IS RECORDED AS A TENSION THE STAGED TOPIC DID NOT
RESOLVE, NOT AS A RESTATEMENT OF IT"*), in `design.md` D8, and in the PR record,
with the rejected alternative stated. I verified the convening's §0.6 correction:
the anchor-late sentence sits in the topic's `## Conflicts` and carries **no
ruling stamp, no date and no disposition-by line**. So a seat is weighing a
**recorded** constraint, not a ruled one — but "recorded is not ruled" cuts both
ways and I do not rule the entitlement question.

**C-2 — D2/D-A, missing-witness semantics.** **`lead-security`'s** (§4). My limb
only, and I read `455bbdaa`: the receipt/state collision **is** resolved by the
receipt's own rule rather than by an exception to it — pending state lives in the
anchor-state record, an upgrade **appends**, and the item is never re-anchored;
the fix's own scenario count (47→48) verifies. What the fix did **not** do is
retire the two-element refusal sentence in requirement 1 (LQ-F15), and requirement
1's phrase *"CAPTURED WHOLE AT ANCHOR TIME"* now means "at the time that chain's
anchor is captured," reconciled only in requirement 3.

**C-3 — Dependency on an unratified sibling.** **Honest and safe**, on my
measurement: declared *"Sequencing, not blocking"* at two sites (not four —
LQ-F2), with tranche one and the PKI plane named as the hard prerequisites, and
**no requirement of #513 cites a requirement of #510**. #513 stands alone as a
testable object.

**C-4 — D6/D-D, the change id, capability name and the sibling-delta
asymmetry.** The asymmetry is **measured and real**: at main neither
`openspec/specs/signed-execution-chain/` nor `openspec/specs/chain-anchoring/`
exists; in `inv510` **two** ADDED deltas now target the same unpromoted
capability directory, while #513 creates a new capability and has no such
surface. On check sufficiency #513's shape is the safer one and its `tasks.md:1.2`
says so in terms. Whether the ids should be corrected is `lead-architect`'s.

**C-5 — D-B, D-C, D-E, D-F.**
- **D-B (structural payload refusal): sound and testable.** Refusing by field
  *shape* rather than by content semantics is the only formulation a neutral
  validator can actually run, and it reaches raw, encrypted and plain-hashed
  content without classifying any of them. Four scenarios back it.
- **D-C (declared-construction refusal and its residual): sound, and the residual
  is honestly declared** — `spec.md:402-411` states plainly that a record
  declaring a salted keyed construction while anchoring a plain digest *"is not
  detectable from the record"*, names what would close it (the commitment path as
  the only minting path), and routes the shortfall to `add-trust-anchor`'s
  declared-shortfall pattern with its own scenario (`:454-458`). This is the
  correct shape for a limit.
- **D-E (deferring the permissioned-ledger selection): fine on my limb** —
  `tasks.md:5.4` names the class (Fabric or Besu) and the decision point, and
  selecting an instance is decidable.
- **D-F (the per-plane key correction to a vendored source): RESPECTS THE
  STANDING RULE, verified by execution.** `git diff afe29561 cf5a24b8 --
  ideation/staging/signed-execution-chain/` is **empty** — #513 edits **nothing**
  in the staged topic directory, the study included. The correction lives in
  #513's own requirement 8 (`:602-611`) as a correction, which is exactly the
  form that keeps the research record evidence.

**C-6 — Q5's standing tension.** **Complied with, verified textually.** #513
states today's posture positively and writes neither permanence nor a trigger:
`:481-484` *"this capability writes NO permanent prohibition and NO condition
under which a different posture would become admissible"*; scenario `:528` *"the
refusal states no permanent bar and names no trigger condition"*; and the same
discipline is applied to the third-chain rule at `:136-141` / `:177`. No "never"
anywhere.

**C-7 — D1 and D9 unrouted.** **NOT MY SEAT** — `lead-architect`'s. I record only
that D1 (why the study stands unedited) is verified true by the empty diff above,
so nothing turns on it for my purposes.

### X — CROSS-CUTTING

**X-1 — CLAIMS OUTRUNNING THE MACHINERY.** **Nothing blocking, in either
packet** — see LQ-F19 and the full sweep at §1.7. Every enforcement in both spec
deltas is DECLARED as a future obligation with its realization gate named; both
packets carry the doctrine explicitly in their evidence conventions; and the one
ASSERTED live claim survives a **live ruleset read**. On the estate's
most-recorded defect family, these two packets are the cleanest I have measured.

**X-2 — VOCABULARY: consumed or reinvented?** **`lead-architect`'s** (§4c). Two
data points I can supply from execution: #510's account of the omnigent matrix is
**exactly right** against the schema (6 closed booleans, two `const: false`, 5
archetypes named correctly), and #510's `spec.md:386-390` declares no second
digest construction and scenarios the refusal of one (`:474-478`).

**X-3 — Two ADDED deltas into one unpromoted capability.** Measured (§1.12): the
capability is **not** in `openspec/specs/`, and `inv510` holds two ADDED delta
directories against it. `openspec validate --all --strict` is green with both
present, so the tool does not object today; the hazard is at **promotion**, which
is what #502/#504 are open on. **On my limb the risk is that the tool's silence is
not evidence** — validation green here proves the deltas parse, not that they
compose on archive. #513's new-capability shape has no such surface and that is a
point in its favour.

---

## 4. VERDICTS — ONE PER SUBJECT

### #509 — **ACCEPT AS AMENDED**
The vendoring is provenance-honest, lifecycle-conformant against the code that
enforces it (more so than the one existing imported precedent), doc-health-clean,
and fifteen of its seventeen mapping targets verify — but the appendix, which is
the one part of a brainstorm that is not free-form, carries three checkable
falsehoods about ruled dispositions and one wrong figure that #513 has already
inherited into requirement text.

### #510 — **ACCEPT AS AMENDED**
The packet is genuinely well-built — every count it makes about itself is
correct, every requirement carries SHALL on line one, doc-health is zero-new, and
it does not outrun its machinery anywhere I could find, including under a live
ruleset read — but two of the three inherited P1 fixes do not hold as applied,
one routed decision has no scenario at all, and I record in the 2026-08-29
formula that **the text as drafted is not ratifiable**.

### #513 — **ACCEPT AS AMENDED**
The strongest-drafted of the three on my measures — 52 scenarios that all test
system behaviour with no assertions-as-scenarios, an unedited vendored study, a
correctly-declared residual, Q5 complied with positively, and negative-example
task lists that name real evidence — held back by one inherited wrong figure
inside requirement text and by a four-element receipt that is refused on two and
packaged as three.

### Amendments

**LQ-A1 [510] — BLOCKING.** Correct "twelve scenarios" to **nine** at all four
sites (`design.md:114`, `design.md:124`, `tasks.md:99`, `proposal.md:243`).
*Discharged by:* the four edits, plus a one-line note that the figure was
measured. **This is owed whichever way B-2 is ruled** — if the repair is taken, a
restatement briefed at twelve that lands nine is itself a promotion-fidelity
defect.

**LQ-A2 [510] — BLOCKING.** Resolve the attribution collision (LQ-F9). *Discharged
by:* stating the distinguisher in requirement 2's body — a **request** the
controller cannot attribute is refused at signing; a **platform** that cannot
attribute any request declares the shortfall and its attestations are refused at
use — and adding one scenario that fixes which branch governs when both hold.

**LQ-A3 [510] — BLOCKING.** Close the deferred-leaf path (LQ-F10). *Discharged
by:* requiring, in requirement 6, that every link-5 leaf for a chain identity be
written **before** that chain's link-6 leaf and refusing a link-5 leaf sequenced
after its successor; **or** replacing the *"at or before the successor's own
leaf"* bound with a rule that no link-5 leaf for the chain identity exists
anywhere in the log outside the enumeration. Either, plus one scenario:
*"a lane defers an unwanted link-5 leaf until after link 6."*

**LQ-A4 [510] — BLOCKING.** Give D6 something to rule on (LQ-F22). *Discharged
by:* two scenarios under requirement 1 — a certificate **revoked at signing** →
the attestation is REFUSED outright; a certificate **revoked after signing** →
what the gate already permitted stands and everything not yet permitted is
refused — and a `SHALL` on the revocation-standing sentence.

**LQ-A5 [509][513] — BLOCKING.** Correct "eighteen months" (LQ-F4). *Discharged
by:* replacing it with the measured interval (**twenty-one months**, 2024-11-10 →
2026-08-29) at #509 `:102` and `:207` **and** at #513 `spec.md:658-659`; or, in
#513, striking the interval from requirement text entirely, since the requirement
does not depend on it.

**LQ-A6 [509] — BLOCKING.** Correct the disposition label (LQ-F5). *Discharged
by:* attributing the salted-keyed-commitment ruling and the erasure-by-salt-
destruction property to **Q6** (`CONFIRMED … the ruling's OPERATIVE FORM`), and
citing **Q2** (`ruled … AS RECOMMENDED`) for the boundary and the refusing
validator — which is what each actually says.

**LQ-A7 [509] — BLOCKING.** Remove or ground the two invented names (LQ-F6).
*Discharged by:* deleting *"calls the commitments + anchoring pattern"* and
*"calls chain inception's fidelity property"*, or replacing each with a phrase
that resolves — e.g. claim 7's *"anchoring is multi-target and reversible by
construction"*, and tranche one's requirement *"Ratification and chain inception
are one signed act"* cited to the change rather than to the topic.

**LQ-A8 [510] — SHOULD-FIX.** Rewrite the three reader-correction scenarios
(LQ-F11) so each THEN names a system consequent, on #513's pattern.

**LQ-A9 [510] — SHOULD-FIX.** Add the missing conjunct scenarios: a signature
from link 4 onward that **omits the predecessor digest** (LQ-F12), and a **FAILED**
link-10 outcome recorded distinctly from missing and unsigned (LQ-F13).

**LQ-A10 [513] — SHOULD-FIX.** Add a scenario for the **archival-node** condition
(LQ-F14) — the one of Q3's three that has none.

**LQ-A11 [513] — SHOULD-FIX.** Extend requirement 1's capture-time refusal
sentence (`:21-24`) to all **four** per-chain elements, and add *"a receipt
missing its block header"* to `tasks.md:4.2`'s negative-example list (LQ-F15).

**LQ-A12 [513] — SHOULD-FIX.** Give the **aggregation Merkle path** at least one
scenario and one negative example (LQ-F16).

**LQ-A13 [510] — SHOULD-FIX.** Make `tasks.md:5.1` decidable (LQ-F17): name the
observable that makes the omnigent layer and the PKI plane "real", and name the
artifact the re-derivation produces. **This is the gate the packet offers as its
answer to T-1**; an undecidable gate is a weak answer to a prematurity objection.

**LQ-A14 [513] — SHOULD-FIX.** Date or re-measure the 984 figure in
`tasks.md:2.1` and in the README record entry (LQ-F20); today's count is 1032.

**LQ-A15 [X] — SHOULD-FIX (against the convening).** Correct §0.5's "five times"
to **seven** and T-2's "four sites" to **two** in the ballot (LQ-F2), so the
record Brett rules on carries measured figures.

### Conditions attached to the record

**LQ-C1.** My verdicts on #510 and #513 are conditional on **T-1 not ending
#510's round**. If the bench rules #510 premature, my #510 verdict is vacated;
my #509 and #513 verdicts stand unchanged, and LQ-A5's #513 limb survives
independently.

**LQ-C2 [509].** The one existing imported brainstorm carries a standing
disclaimer — *"These notes are imported evidence and idea material. They do not
decide policy, memory, release scope, or OpenSpec approval."* #509 carries none.
That is a precedent and not a contract, so I attach it as a condition rather than
an amendment: **either carry the disclaimer or record that it was considered and
declined.**

**LQ-C3 [X].** LQ-F5 and LQ-F6 are exactly the class no checker in this estate
reads: a prose appendix asserting facts about ruled dispositions and about what a
document "calls" something. Three of them survived authoring, a bot round and the
convening's own §1.3 warning. **I record, as a condition on this sitting's
record, that a doc-health family for disposition-label and named-phrase
resolution over `ideation/**` appendices is owed as a successor** — this seat's
answer to A-5, and the only durable one.

**LQ-C4 [X].** I found no defect in the claim-outrunning-machinery family in
either chain packet, and I want that recorded as a **measured** result rather than
an absence of effort: I swept both packets, classified every enforcement
assertion, and read the **live ruleset** for the single ASSERTED one. If a later
reader disagrees, the disagreement should start from ruleset 21538893's state on
2026-08-30.

---

## 5. In the packets' and the changes' FAVOUR

A record that lists only defects misreports what I read, and what I read was
good.

1. **Every self-count in both chain packets is correct.** 9/59 and 9/52,
   consistent at four sites each, and every fix commit's own scenario delta
   verifies to the unit (47→48→52; 50→59). I went looking for a second wrong
   number after §0.4 and **the two I found were the convening's, not the
   packets'.**

2. **Every requirement carries SHALL on its first body line.** All eighteen. The
   parser trap that has bitten this estate before is closed in both.

3. **doc-health is zero-new on all three subjects**, and both chain packets
   claimed exactly that at `tasks.md:1.5` **citing issue #342 by number** and
   describing the basename hazard correctly. They ran the check the right way and
   reported it honestly; I reproduced it and they were right.

4. **Neither packet outruns its machinery.** Both carry the
   workflow-file-is-not-evidence doctrine in their own evidence conventions;
   #510 `tasks.md:157-159` states *"this packet claims no enforcement it cannot
   name a check for"*; #510 `tasks.md:178-180` insists the evidence is the live
   ruleset. And the single live claim either packet makes **survives a live
   ruleset read**. On this family this is the best pair of packets I have
   measured.

5. **#513 edits nothing in the staged topic directory — the vendored study
   included.** `git diff` over `ideation/staging/signed-execution-chain/` is
   empty. The standing rule that *"a research record rewritten to agree with a
   later ruling stops being evidence"* is not just cited, it is obeyed, and the
   correction to the source sketch lives in #513's own requirement 8 as a
   correction.

6. **The declared residuals are real declarations, not softenings.** #510's
   attribution residual names the constitutional reason the obvious mechanism is
   unavailable; #513 `:402-411` states in terms that a lying construction
   declaration *"is not detectable from the record, and this requirement does not
   pretend otherwise"* and names what would close it. Both route to
   `add-trust-anchor`'s declared-shortfall pattern rather than inventing one, and
   both carry their own scenario.

7. **#513's negative-example task lists name evidence a person could actually
   produce** — `4.5` refuses a plan for a node, `4.7` demands a receipt verified
   *after* the chain has pruned *"which is the only test that actually proves
   retention"*. That is what an executable task looks like.

8. **#510's P1-3 repair holds under attack.** I tried to break it. The instrument
   it names is shipped, the check that reads it is genuinely required on the
   default branch, the standing-at-exercise refusal is scenario'd, and the
   residual it cannot close is declared with the closer named.

9. **#513 has zero assertions-dressed-as-scenarios** where #510 has three. Every
   one of its 52 THENs names a system consequent.

10. **Both packets decline to claim an approver and say why**, and #513 cites
    tranche one's own overstatement against itself. I verified the disclaimers
    match the record: nothing at `origin/main` authorizes drafting tranche two or
    three, and neither packet says otherwise.

11. **#509's `Source:` block declines to claim byte-fidelity.** It would have been
    easy to imply a verbatim vendoring; it says instead that it *"reconstructs the
    notes' section structure and enumerated claims from that transcript"* and
    names the OneNote original as the artifact of record. That sentence is why I
    can rule A-1 without hesitation, and it is why the appendix's three errors are
    correctable rather than corrupting.

12. **The convening disclosed its own hazards against its own interest** — §0.3's
    three-subject risk, §0.6's correction of its own earlier draft, §3.1's refusal
    to present a hand roster as a tool output, §3.2's recording of the CSC ground
    against itself, and §3.4's statement that it is withholding findings on
    purpose. My two corrections to its counts (LQ-F2) are offered in the same
    spirit and change none of its conclusions.
