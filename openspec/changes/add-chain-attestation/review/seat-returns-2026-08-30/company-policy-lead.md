Seat: company-policy-lead (client seat) · Convening: gate_rules_council (§7.4 sitting), 2026-08-30
Packet: openspec/changes/add-chain-attestation/review/convening-packet-2026-08-30.md
Judged at: openxFactory main afe29561 / #510 e7f6ae0e / #513 cf5a24b8 / #509 26c7e778

# SEAT RETURN — `company-policy-lead` (CPL), client seat

## 0. Persona declaration

Neutral persona, `templates/client-layer/roles/company-policy-lead.yaml` (read at
`invmain`, verbatim):

> authority: owns: [operating_policy, house_team_coordination]; decides:
> [is_this_allowed_here]; escalates: [{trigger: policy_gap_or_conflict, to:
> responsible_operator}]
> character_frame: "The operating organization's chief of staff: holds 'how we
> do things here', translates between the domain's how and the business's why…
> when policy is silent or self-contradictory, surfaces it to the human
> operator rather than improvising a precedent."

Engineering-tenant specialization, `sittingref` codexFactory
`hermes/client/role-overrides.yaml:14-21`, verbatim:

> "The company's own frame over an engineering estate, seated only when a
> change speaks for the company to a reader outside the engineering
> conversation: tenant-facing content, published role/persona profiles, the
> contribution compact, and the repository README… this seat weighs what the
> company is saying, and to whom."

Model: `sonnet`, per `role-overrides.yaml:37-44` (`seat_representation`,
declared by `gate_rules_council` 2026-08-26, R23) — the tenant declaration R4
fixed as authoritative over any domain-file selector. Confirmed I am running
as the declared representation.

**Boundary reading I take, stated openly.** My charter is company voice over
engineering content: the README entries, the authorization posture, and — as
the packet's own reading holds (§1.3) — the #509 vendoring squarely. I do NOT
rule the architecture-substance ballot items (B-2..B-7 substance, C-1..C-7
substance, X-2/X-3 substance); where I touch them below it is only the
resolvability/voice edge of the question, named as such, with the substantive
seat named. T-0(a) ("is this allowed here") sits inside my authority verbatim
and I rule it rather than deferring it.

## 1. What I verified BY EXECUTION with real output

All five checkouts confirmed `git status --porcelain` EMPTY before and after
my work (re-verified at close, see command block at end of this section).

**README diffs, both packets, full text** —
`diff invmain/README.md inv510/README.md` and `... inv513/README.md`:
produced the two added README blocks in full (35 and 83 lines respectively;
quoted and analysed under Findings CPL-F8). `diff invmain/README.md
inv509/README.md` returned **empty** — confirmed #509 does not touch
`README.md` at all, contrary to nothing in the packet but worth stating as a
verified negative.

**Authorization-overreach sweep, both packets, exhaustive** —
`grep -rn "Brett" inv510/openspec/changes/add-chain-attestation/` → 12 hits;
`grep -rn "Brett" inv513/openspec/changes/add-chain-anchoring/` → 16 hits. I
read every hit in context (not just the grep line). Every one of the 28
either (a) cites an already-ruled Q-disposition or tranche-one text accurately,
or (b) explicitly states the packet is not ratified. Both `.openspec.yaml`
`approved_by` fields read in full:

- #510 `:40-49`: *"NOBODY YET, AND THE FIELD SAYS SO RATHER THAN IMPLYING
  OTHERWISE… Nothing here is ratified, and no requirement in this delta
  confers or refuses anything."*
- #513 `:43-49`: *"NO APPROVAL FIELD IS CLAIMED HERE, DELIBERATELY… the
  drafting was commissioned by an orchestrating session, which is not Brett
  Heap's word."*

**#509 read in full** (223 lines, `inv509/ideation/brainstorm/medxchain-blockchain-medical-records.md`),
Source block read with particular care (`:16-24`).

**Mapping-appendix verification against the actual staged topic**, by grep and
targeted reads of `invmain/ideation/staging/signed-execution-chain/signed-execution-chain.md`
(901 lines):

```
$ grep -n "^#" signed-execution-chain.md
  205:## The on-chain layer, as ruled          <- exists, cited accurately
  326:### What goes on chain, and what must not <- exists, cited accurately
$ grep -n "commitments + anchoring" signed-execution-chain.md   -> 0 hits
$ grep -n "chain inception" signed-execution-chain.md            -> 0 hits
$ grep -n -i "fidelity property" signed-execution-chain.md       -> 0 matching hits
$ grep -n "meta-analysis" signed-execution-chain.md               -> 0 hits (confirms #509's claim of absence)
$ grep -n -i "failed attempt" signed-execution-chain.md            -> 0 hits (confirms #509's claim of absence)
$ grep -n "Ten links" signed-execution-chain.md                    -> line 78, matches
```

Read Q2 (`:553-578`) and Q6 (`:735-772`) formal disposition blocks in full.
Q2's disposition status, verbatim (`:568`): *"ruled 2026-08-29 — Brett Heap, in
session; AS RECOMMENDED."* Q6's, verbatim (`:753-754`): *"CONFIRMED 2026-08-29
— Brett Heap, in session; AS RECOMMENDED, and this is the ruling's OPERATIVE
FORM."*

Read the "Claims" block (`:414-450`) and confirmed claim numbering: claim 2 =
HealthLinc (`:423`), claim 3 = LedgerLinc (`:427`), claim 4 = *"The two mappings
are the same shape"* (`:430`, exact-quote match), claim 6 = the off-chain
evidence plane / transparency log (`:436`).

**Date-math check** (own execution, not taken from the packet): #509's
`Source:` line gives 2024-11-10; the appendix is headed 2026-08-29. 2024-11-10
→ 2025-11-10 = 12 months; → 2026-08-10 = 9 more months; → 2026-08-29 = 19 more
days. **Total ≈ 21 months 19 days (≈ 21.6 months, nearer 22 than 18).** #509
states "eighteen months" twice (`:102`, `:205`); the second occurrence is
independently restated in #513's own requirement text.

**#513's three normative citations of #509**, read in full at
`inv513/openspec/changes/add-chain-anchoring/specs/chain-anchoring/spec.md`
(`:535-556`, `:598-610`, `:650-660`): confirmed each explicitly marks #509 as
*"IN FLIGHT at this revision"* and states *"the obligation does not depend on
the citation… the citation is PROVENANCE."* Confirmed the third site
(`:658`) independently repeats *"predating the neutral family by eighteen
months."*

**Lifecycle-header conformance**, against `invmain/ideation/README.md:51-99`
("## Ideation Header Format") and the one existing imported-evidence precedent,
`invmain/ideation/brainstorm/notebooklm-import-test/notebooklm-ideas-2026-07-09.md`
(read in full, first 30 lines): the precedent uses title prefix `# NotebookLM
Ideas: <workspace> — Brainstorm` and drops `Captured:` entirely in favour of
`Source workspace:` / `Source workspace id:` / `Origin:`, per the documented
"instead" rule (`ideation/README.md:77-79`). Also read
`invmain/scripts/ideation_dashboard/authoring.py:64-66,267-291`
(`REQUIRED_HEADER_FIELDS`, `missing_required_headers`) — the code
unconditionally requires `Captured` with no carve-out for imported evidence,
which the precedent file would arguably fail and #509 (which retains
`Captured:`) would pass.

**Persona and specialization files** read in full (§0 above), confirming basis
and model declaration.

**Final git-status re-check, all five trees, empty:**

```
$ for d in invmain inv510 inv513 inv509 sittingref; do (cd "$d" && git status --porcelain); done
(no output from any tree — confirmed clean before and after, no writes made)
```

## 2. Findings

**CPL-F1 [509] SHOULD-FIX.** The `Source:` block (`:16-24`) states *"structure
and claims preserved… no content reworded"* two sentences before *"this
vendoring reconstructs the notes' section structure and enumerated claims from
that transcript rather than reproducing byte-identical prose."* Read together
these are in tension: "no content reworded" suggests verbatim wording; "not
byte-identical prose" admits the wording is reconstructed. The resolvable
reading is "content" = claims/substance, not exact prose — but the packet's
own instruction is to test the Source block's internal consistency, and on a
plain read it is not fully consistent. **Discharged by**: reword to something
like *"no claim added, removed, or altered; the wording is reconstructed from
transcript, not verbatim."*

**CPL-F2 [509|513] SHOULD-FIX.** *"Eighteen months"* (`#509 :102, :205`) is
arithmetically wrong — the true gap between 2024-11-10 and 2026-08-29 is
~21.6 months (see §1 date-math), not eighteen. This is a checkable,
false factual claim about the estate under A-2, and it is **not confined to
the brainstorm**: #513's own requirement text (`spec.md:658`) independently
restates the same wrong figure, so the error would enter proposed contract
narrative, not just brainstorm colour. **Discharged by**: correct both #509
sites and #513's citing site to "~22 months" / "nearly two years."

**CPL-F3 [509] SHOULD-FIX.** The appendix's "Convergences" section twice
claims the staged topic itself uses specific vocabulary it does not use:
*"the same pattern `signed-execution-chain` calls the **commitments +
anchoring** pattern"* (`:115`) and *"the property `signed-execution-chain`
calls **chain inception's fidelity property**"* (`:131`). Grep-verified: zero
hits for either phrase anywhere in `signed-execution-chain.md`. The
*substance* described is accurately drawn from the topic; the claim that the
topic *names* it this way is false. Neither of these two bullets is among
#513's three load-bearing citations (verified — those cite the
verification-attempt, cross-plane-key, and domain-mapping bullets, not these
two), so this stays confined to #509. **Discharged by**: reword from "X calls
this Y" to "this appendix calls it Y" (own label, not attributed vocabulary).

**CPL-F4 [509] SHOULD-FIX.** The appendix labels Q2 *"ruled 2026-08-29
(CONFIRMED operative form)"* (`:145-146`). Verified against the topic: Q2's
own disposition-status line (`signed-execution-chain.md:568`) reads *"ruled
2026-08-29 — Brett Heap, in session; AS RECOMMENDED"* — no "CONFIRMED," no
"operative form." That exact stamp — *"CONFIRMED… this is the ruling's
OPERATIVE FORM"* — belongs to **Q6** (`:753-754`), a different, later-settled
question about a different narrowing. The substantive claim attached (Q2
requires salted keyed commitments) is correct; the disposition-status label
borrowed to dress it is not Q2's. **Discharged by**: drop the parenthetical or
correct it to Q2's actual stamp.

**CPL-F5 [509] OBSERVATION — favour.** The appendix's own section header,
`## How MedxChain meets the signed-execution-chain architecture — 2026-08-29`
(`:100`), is an unambiguous, dated boundary between Brett's reconstructed 2024
notes (`:26-98`) and the vendoring author's 2026-08-29 analysis (`:100-224`).
This discharges A-1's "is Brett's text distinguishable from the framing"
cleanly and is worth recording as a design choice that works.

**CPL-F6 [509] SHOULD-FIX (weak; the gap may be in the contract, not #509).**
Compared against the one existing imported-evidence precedent
(`notebooklm-import-test/notebooklm-ideas-2026-07-09.md`), which drops
`Captured:` for `Source workspace:` / `Source workspace id:` / `Origin:` per
`ideation/README.md:77-79`'s documented "instead" rule, #509 instead keeps
`Captured: 2026-08-29` (the vendoring date) and adds an ad hoc `Source:` field
(not one of the three named fields) to carry the true 2024-11-10 origin. This
is a real deviation from the documented convention. **Mitigating**: the
code-level gate (`authoring.py` `REQUIRED_HEADER_FIELDS`) unconditionally
requires `Captured`, with no imported-evidence carve-out — so #509's choice
actually satisfies the code gate more safely than the precedent does, and the
doc/code disagreement predates this packet. **Discharged by**: either a
header edit to add `Origin:` alongside `Captured:`, or (better, since the
gap looks structural) a small addition to `ideation/README.md`'s
imported-evidence provision naming non-NotebookLM import paths.

**CPL-F7 [509] OBSERVATION.** The H1 (`# MedxChain — Blockchain-Backed Medical
Record Fidelity — Brainstorm`) correctly carries the required suffix but,
unlike the precedent's `# NotebookLM Ideas: <workspace> — Brainstorm`, carries
no title-level "this is imported" signal. A title-only reader (e.g. grepping
brainstorm titles) cannot tell this is 2024 vendored material from the H1
alone. Minor — the Summary line resolves it on open.

**CPL-F8 [510|513] SHOULD-FIX.** Both README "OpenSpec Records" entries are
clearly bookended by draft-status language (opening: *"`Status: draft` — NOT
RATIFIED, filed FOR REVIEW"* / *"RATIFICATION IS NOT SOUGHT BY THIS PACKET'S
LANDING"*; closing: *"TWO ACTS MUST FOLLOW, IN ORDER…"* / *"…allocated at
realization by merge order"*) — a reader of the whole entry is not misled.
But mid-entry both use present-tense operative verbs for drafted text: #510
*"the SIGNED HASH-LINK RULE takes effect at link 4"*, *"the short-chain gate's
walk EXTENDS from links 1–6"*; #513 *"Q2 AND Q6 **BECOME** CONTRACT TEXT WITH
A REFUSING VALIDATOR."* My obligation (a) is precisely "a reader who reads
only that entry" — a reader who lands on a middle sentence of a long README
list entry (plausible; these entries run to 35 and 83 lines) is exposed to
present-tense claims that a gate/contract change is already live. Not
blocking, because the entry as a whole is unambiguous and both packets'
underlying documents are otherwise scrupulous. **Discharged by**: hedge the
mid-entry verbs to conditional/drafted phrasing ("would take effect," "the
drafted text has the gate walk extend," "would become").

**CPL-F9 [510|513] OBSERVATION — favour.** The authorization-overreach sweep
is clean, in full (§1 above, 28 "Brett" hits read in context). No sentence in
either packet reads as though Brett has agreed to the packet's drafted
CONTENT, as opposed to having ruled the Q-dispositions it draws on or being
asked to rule/ratify it next. Both `.openspec.yaml` files decline an approver
in terms, and #513 goes further, naming the exact prior lesson (tranche one's
origin-record correction, cited at `:46`) it is deliberately not repeating.
This is a repeat-clean result against the 2026-08-29 sitting's identical sweep
(disclosed at packet §0.8), on a sharper text than last time.

**CPL-F10 [X] OBSERVATION.** Volume. See ballot T-0(c) below for the full
answer; recorded here as a finding because it is falsifiable: the convening's
own §0.4 finding (a false "twelve scenarios" count that survived four
citation sites inside #510's own text, unchallenged by the packet's own
authors) is direct evidence that volume degrades even the *author's* own
re-reading. My own reading was necessarily selective (README + `.openspec.yaml`
+ targeted `design.md` sections + full #509, not full `spec.md`/`tasks.md`
line-by-line for either #510 or #513) — disclosed honestly under T-0(c).

## 3. Positions on the ballot questions

**T-0(a) — is a §7.4 proposal review within this council's reach, and in this
shape? MY SEAT RULES THIS ONE** — `is_this_allowed_here` is my charter's
literal decision authority. Not per se unlawful: Brett's 2026-08-29 sanction
covers the convener act, and this packet discloses honestly (§0.1, §0.3) that
the sanction was given for ONE subject and has not been freshly given for
THREE. But as a matter of **house operating policy**, a "sanctioned pending
amendment" status that is now reused a second time, unrenewed, while the
promised amendment (codexFactory issue #131) still has not landed, is exactly
the drift my seat's `escalates: policy_gap_or_conflict → responsible_operator`
exists for. **My ruling**: lawful to proceed this once more on the standing
sanction (it is disclosed, not smuggled), but I escalate: Brett should either
land the amendment now or issue an explicit renewed sanction naming the
multi-subject shape, rather than let "pending" become the permanent state by
default. Recommend option (i) or (ii) be chosen deliberately at this ruling,
not left open a third time.

**T-0(b)** — primarily lead-security's (the CSC-predicate evaluability
question is a code-semantics call). Policy-level supporting view only: my
`risk_posture: averse` disposition favours the preserved dissent
(`ConditionUnevaluable` → refuse-or-park, not silently proceed) over treating
an unevaluable predicate as `False`. I do not rule the technical ground.

**T-0(c) — did combining three subjects degrade reading, honestly?** **Yes,
measurably, and I disclose it against my own return.** Even confined to my
own charter (README text, authorization posture, volume, #509), I read
`.openspec.yaml`, both README diffs in full, and #509 in full, but sampled
`design.md`/`spec.md`/`tasks.md` for #510 and #513 by targeted grep and
section reads rather than reading either packet's ~1,700–1,900 lines end to
end. That is a real depth cost directly attributable to sitting over three
subjects at once, on top of my own charter (which is narrower than
lead-architect's/lead-quality's, whose obligations against ~111 scenarios
combined are heavier still). **Combining #509 into this sitting is
independently justified** by §0.9 (three of #513's requirements cite it as
provenance) — that part of the combination was necessary. Combining #510 and
#513 together, when #513 composes on #510 and #510's own round could end
before #513's, is a **separable choice** the convening made for scheduling
convenience, not necessity, and it is the part I would not repeat.

**T-1 — is #510 premature?** **NOT MY SEAT** — this is lead-architect's per
the packet's own obligations table ("(a) T-1 is yours first"). My only
contribution: the tenant-voice angle is already covered by CPL-F9/CPL-F8 —
the README and proposal text disclose the Q4-versus-drafting tension honestly
rather than resolving it by assertion, so whichever way T-1 is ruled, the
public-facing text does not misstate its own settledness.

**T-2** — NOT MY SEAT, lead-architect (sequencing/architecture).

**T-3 — was the drafting authorized, and is that adequate?** **Mine.**
Answered in full at CPL-F9. My ruling: a draft filed FOR REVIEW without a
pre-existing drafting authorization is a lawful object before this council,
**provided the packet says so plainly rather than implying otherwise** — both
packets clear that bar. Requiring authorization to *precede* the sitting as a
hard rule would collapse the review-before-ratify pattern this family has now
used twice (`add-binding-consumer-identity`, and this). The defect, if the
bench finds one, is curable by Brett's ruling on this very ballot, as the
packets themselves anticipate.

**A-1 — provenance fidelity.** Adequate, not perfect. Author, date and process
are stated (`Source:` block); Brett's text is distinguishable from the
vendoring author's framing (CPL-F5, favour). The Source block's own fidelity
claim carries an internal tension (CPL-F1, should-fix) that should be
tightened but is resolvable on a careful read and does not, on its own, make
a reader mistake the vendoring author's words for Brett's. **Not blocking.**

**A-2 — invented claims about the estate.** Enumerated exhaustively (CPL-F2,
CPL-F3, CPL-F4): one arithmetic error repeated twice and inherited into
#513's requirement text; two mislabelled "the topic calls this X" vocabulary
attributions confined to #509; one disposition-status mislabel (Q6's stamp
attached to Q2). None touches a ruled disposition's *substance* — every
substantive claim about what Q2/Q3/Q6/claims 2/3/4/6 actually **say** checked
out true. All four are one-line, easily-discharged corrections. Brett's own
speculative/design content (the 2024 notes themselves) is not judged here, per
the packet's own rule.

**A-3 — mapping accuracy, table.**

| Appendix target | Exists? | Characterization accurate? | Cite |
|---|---|---|---|
| "The on-chain layer, as ruled" section | Yes | Yes | topic `:205` |
| "So the split is" table | Yes | Yes | topic `:346` |
| "What goes on chain, and what must not" | Yes | Yes | topic `:326` |
| Q2 boundary quote ("off chain: every payload…") | Yes | Yes, close paraphrase of `:558-562` | topic `:558` |
| Q2 disposition status "(CONFIRMED operative form)" | Exists (Q2 does) | **No — mislabelled**, Q6's stamp | topic `:568` vs `:753` (CPL-F4) |
| "chain inception's fidelity property" as topic's own term | Concept exists; term does not | **No** — invented label attributed to topic | 0 grep hits (CPL-F3) |
| "commitments + anchoring pattern" as topic's own term | Concept exists; term does not | **No** — invented label attributed to topic | 0 grep hits (CPL-F3) |
| claim 2 = HealthLinc | Yes | Yes | topic `:423` |
| claim 3 = LedgerLinc | Yes | Yes | topic `:427` |
| claim 4 = "the two mappings are the same shape" | Yes | Yes, exact quote | topic `:430` |
| claim 6 = transparency log / evidence plane | Yes | Yes | topic `:436` |
| Q3 configuration (Kaspa first, Bitcoin-OTS durability, no selectivity, no third chain) | Yes | Yes | topic `:625-637` |
| "meta-analysis lane" absent from topic | Confirmed absent | Yes | 0 grep hits |
| "failed attempts" auditing absent from topic | Confirmed absent | Yes | 0 grep hits |
| "Ten links" | Yes | Yes | topic `:78` |
| "eighteen months" between 2024-11-10 and 2026-08-29 | N/A (arithmetic) | **No — actual gap ≈ 21.6 months** | CPL-F2 |

**A-4 — lifecycle conformance.** Header-field minimum (Status/Kind/Summary/
Topics/Repository context/Captured) is met; H1 suffix rule is met. Compared
against the one imported-evidence precedent: a real convention deviation on
the `Captured:`-vs-`Origin:` question (CPL-F6), softened because the code gate
and the doc's prose disagree with each other already, and #509's choice is
the code-safe one. Title-level import signal weaker than precedent (CPL-F7).
**Net: conforms to the letter of the mandatory fields; falls short of the
precedent's convention on imported-evidence field naming and title signalling.
Should-fix, not blocking.**

**A-5 — is a council the right instrument for a brainstorm vendoring at all?**
Answered against the convening's interest, as instructed. **Generally, no** —
no brainstorm vendoring has ever carried a review record, and ordinary-PR
landing with routing-carried review remains the right general instrument; nothing
here argues for changing that going forward. **In this specific case**, the
inclusion is justified only because #513's own requirement text now cites
#509 normatively at three sites (§0.9, verified in §1) — that dependency, not
any general property of brainstorm vendorings, is what earns #509 a seat at
this table. A future vendoring that is not cited as provenance by a sibling
packet should not default to a council sitting.

**B-1 through B-7 (substance)** — **NOT MY SEAT**, lead-architect and
lead-quality per the packet's own obligations table. Limited CPL-scoped notes:
**B-7/C-4 (naming)** — resolvability is a company-voice-adjacent concern; a
one-line back-citation in tranche one's ratified text (*"raised as
`add-chain-attestation`"*) costs nothing and closes the grep-dead-end the
packet itself names at §1.4, whichever id the architecture seat prefers as
canonical. I recommend it as a light should-fix but leave the "which id"
question to lead-architect.

**B-8 — is a draft governance packet on `main` a safe object?** Mine. **Yes,
conditional on CPL-F8 being applied.** Both entries correctly gate the reader
at open and close; the mid-entry present-tense language is the one thing
standing between "safe" and "safe with a caveat." Fix CPL-F8 and B-8 clears
without qualification.

**C-1, C-2, C-5, C-6, C-7** — **NOT MY SEAT**, lead-architect (C-1, C-5, C-6,
C-7) and lead-security (C-2). No company-voice angle to add.

**C-3 — honest expression of dependency on an unratified sibling.** Partial
CPL note, architecture substance not mine: verified `.openspec.yaml`'s
`related:` block states plainly *"Tranche two, IN FLIGHT beside this packet.
Sequencing rather than blocking"* (`inv513/.../.openspec.yaml`) — that is
honest, plain, unhedged language, consistent with the voice standard my seat
applies elsewhere in this packet. I record this as accurate; the structural
question (is "sequencing not blocking" the *right* relation) is
lead-architect's.

**X-1** — primarily lead-quality's (claim-outrunning-machinery). Supporting
note only: I found no case in the README text itself where a not-yet-real
mechanism is asserted as already enforced — every README claim I checked was
either bookended by draft language (CPL-F8) or explicitly marked as a
realization dependency (e.g. "no certificate authority," "the operator
infrastructure… is commissioned at realization"). Defer the exhaustive
enumeration to lead-quality.

**X-2** — primarily lead-architect's. My contribution: CPL-F3 is a narrow
instance of this question confined to #509's own free-form appendix
vocabulary (not the normative contract text), so it does not bear on whether
#510/#513 themselves mint or consume vocabulary at the contract-text level.

**X-3** — NOT MY SEAT, lead-architect (#502/#504 sibling-delta class).

## 4. VERDICTS — ONE PER SUBJECT

### #509 — **ACCEPT AS AMENDED**, on the grounds that provenance and
lifecycle-header basics are met and the original/analysis boundary works
cleanly, but the mapping appendix — the one part of a brainstorm document the
packet's own rule holds is not free-form — carries four verifiable
inaccuracies (CPL-F2/F3/F4, plus the softer F1/F6/F7) that should be corrected
before any later reader, including #513, keeps treating them as settled fact.

### #510 — **ACCEPT AS AMENDED** (within my charter only; conditional on
lead-architect's T-1 ruling not ending the round first), on the grounds that
the README voice and authorization posture are clean (CPL-F9) subject to one
should-fix hedging pass (CPL-F8).

### #513 — **ACCEPT AS AMENDED** (within my charter only), on the same
grounds as #510 plus inheriting CPL-F2's arithmetic correction from #509 into
its own requirement text at `spec.md:658`.

### Amendments

- **CPL-A1 [509|513] SHOULD-FIX.** Correct "eighteen months" (#509 `:102`,
  `:205`; #513 `spec.md:658`) to the true ~22-month gap. Discharged by three
  one-line edits.
- **CPL-A2 [509] SHOULD-FIX.** Reword the two "signed-execution-chain calls
  this X" vocabulary attributions (`:115`, `:131`) to name them as the
  appendix's own labels, not the topic's. Discharged by rewording both
  bullets.
- **CPL-A3 [509] SHOULD-FIX.** Correct or drop the "(CONFIRMED operative
  form)" parenthetical attached to Q2 (`:145-146`) — that stamp is Q6's.
  Discharged by a one-line correction.
- **CPL-A4 [509] SHOULD-FIX.** Reword the `Source:` block's fidelity claim to
  remove the "no content reworded" / "not byte-identical" tension. Discharged
  by distinguishing claims-preserved from wording-reconstructed explicitly.
- **CPL-A5 [510|513] SHOULD-FIX.** Hedge mid-entry present-tense operative
  language in both README entries to conditional/drafted phrasing. Discharged
  by a wording pass; the entries' own opening/closing sentences are the
  template to match.
- **CPL-A6 [509] SHOULD-FIX (weak).** Align #509's header with the one
  imported-evidence precedent's field vocabulary (`Origin:`) or extend
  `ideation/README.md`'s imported-evidence provision to explicitly cover a
  non-NotebookLM (OneNote-via-transcript) import path. Discharged by either a
  header edit or a doc-contract addition — either resolves it.

### Conditions attached to the record

- **CPL-C1.** None of my findings are BLOCKING. I attach no hard condition
  beyond: CPL-A1 (the arithmetic error inherited into #513's own requirement
  text) should land before #513's requirement text is treated as settled
  narrative by any later reader or realization pass, since at that point it
  stops being brainstorm-stage free content and becomes governed text
  carrying a false claim.
- **CPL-C2.** T-0(a)'s escalation (above) is a standing condition on the
  *convening pattern*, not on any one subject: Brett should close codexFactory
  issue #131 or issue an explicit renewed sanction for multi-subject §7.4
  sittings before a fourth one of this shape is convened without either.

## 5. In the packets' and the changes' FAVOUR

- The authorization discipline in both packets is genuinely exemplary, not
  merely adequate: both `.openspec.yaml` files decline to claim an approver
  they cannot cite, and #513 names the exact prior overreach (tranche one's
  own corrected origin record) it is deliberately not repeating (CPL-F9).
- Both packets are honest about their own unresolved tensions in the very
  documents a casual reader would open first — the README entries disclose
  the Q4-versus-drafting question and the D8 narrowing rather than presenting
  either as settled (CPL-F8's caveat is about *mid-entry* wording, not about
  withheld disclosure).
- Neither packet spends a contract number or claims a schema change it has
  not made; both `target_release` fields state plainly why no number is
  written and point at the sibling that already holds the next cut.
- #509's dated section boundary (`## How MedxChain meets… — 2026-08-29`) is a
  clean, reusable pattern for future vendorings: it makes the
  original-versus-analysis line legible without a separate review record.
- The commit-level self-correction discipline on #513 is real, not
  performative: `455bbdaa`'s own message opens "Self-caught before the bot
  round" and shows its own reasoning rather than asserting a fix was applied.
- #509's `Source:` block, imperfect as flagged in CPL-F1, is more forthcoming
  than it needed to be about its own limits — it names the OneNote original as
  "the source artifact of record for exact wording" rather than letting this
  vendoring quietly stand in as that record.
