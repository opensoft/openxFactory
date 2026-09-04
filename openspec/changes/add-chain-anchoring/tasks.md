# Tasks: add-chain-anchoring (tranche three)

Governance-level and dependency-ordered. **This change is a DRAFT and is NOT
being implemented now.** §1 is authored in this pull request; **§2 — the §7.4
council review — is COMPLETE as of 2026-08-30, and §3, Brett Heap's ratification
act, IS THE NEXT ACT AND IS OPEN**; §4 onward are for the implementer and belong
to Speckit contract features. Do not duplicate the executable contract list
here — §6 hands off the successors.

**RATIFICATION IS NOT SOUGHT BY THIS PACKET'S LANDING.** The order is: land the
draft, convene the council OUTSIDE the clearance pipeline, record the sitting in
`review/`, then Brett rules. That order is the house pattern
(`add-binding-consumer-identity`, whose council returned SPLIT 2–2 on the verdict
word and UNANIMOUS 4/4 that the drafted text was not ratifiable, with fifteen
blocking amendments — which is what a review is FOR, and why this packet does not
present its authoring decisions as settled).

Evidence convention, unchanged from the family's standard: a box closes on a
FACT that survives the session — a merged commit, a green run named by id, a
live API read, a file path — never on an intention and never on a workflow file
standing in for a ruleset state.

## 1. Spec deltas and the packet (THIS PULL REQUEST)

- [x] 1.1 `chain-anchoring` — **NINE ADDED requirements over 89 SCENARIOS** (52
      SCENARIOS at the head the council judged, `cf5a24b8`; the 2026-08-30 fix
      round of §2.4 and its NINE bot rounds added THIRTY-SEVEN SCENARIOS and NO NEW
      REQUIREMENT — the requirement count is unchanged at nine), in
      the order the exit path requires: the multi-anchor receipt FIRST, then the
      ruled two-witness configuration, the missing-witness semantics, anchor-late,
      the commitment boundary with its refusing validator, the permissioned
      consent plane, verification-attempt auditing, the meta-analysis lane, and
      the neutrality boundary.
- [x] 1.2 NO `## MODIFIED Requirements` block anywhere in this packet, and no
      restatement of any promoted or sibling requirement. A NEW capability rather
      than a second ADDED block on `signed-execution-chain`, so the sibling-delta
      shape of issue #502 has no surface here.
- [x] 1.3 `design.md` records the real decisions with their rejected
      alternatives — the Q3 divergence and why the study stands unedited (D1),
      the missing-witness semantics (D2), the structural payload refusal (D3),
      the declared-construction commitment refusal and its EDPB ground (D4), the
      identity-plane placement and why selecting a permissioned ledger does not
      re-open Q3 (D5), the naming divergence (D6), the per-plane key correction
      to a vendored source (D7), the item/checkpoint split that narrows
      anchor-late (D8), the fourth receipt element (D9), and the audit
      obligation scoped to what the factory SERVES (D10) — plus realization
      dependencies and what the design does NOT decide. D8, D9 and D10 each
      record a control that could not run as first written, all three raised by
      a bot on this packet's own pull requests.
- [x] 1.4 `OPENSPEC_TELEMETRY=0 openspec validate add-chain-anchoring --strict`
      green and `--all --strict` green before commit; counts recorded in the
      pull-request body.
- [x] 1.5 doc-health zero-new against `origin/main`, baseline worktree basename
      matching the working clone's (issue #342 — a mismatched-identity
      `--previous-report` manufactures phantom regressions). **This box closes
      over THE AUTHORED BYTES and says so, because at the current head the run
      is NOT zero**: carrying the sitting into `review/` added four
      `status-validity` findings that are the frozen bundle's and are ruled
      pending, §2.4. Every authored byte of this packet — §1's spec, design,
      proposal and tasks, and every amendment — remains zero-new, which is the
      claim this box was ever making. Read the two together; neither is the
      whole state on its own.
- [x] 1.6 README "OpenSpec Records" active block updated, newest first. Expect a
      union-merge with tranche two's line; both lines are kept.
- [x] 1.7 `ideation/staging/INDEX.md` — the topic's detail section records that
      EXIT 3 is raised, and by which change id.
- [x] 1.8 **EVERY RULED INPUT IS CITED WHERE IT BINDS, AND NONE IS RE-ARGUED.**
      Q3 round 2 (the configuration and the three conditions), Q2 (the boundary),
      Q6 (the commitment reading as the ruling's operative form), Q5 (no
      permanence claim and no trigger condition), the exit path's receipt-first
      instruction and corrected receipt form, and the anchor-late constraint —
      each cited to its section in the staged topic, with the vendored study
      cited for GROUNDS only.
- [x] 1.9 The in-flight `ideation/brainstorm/medxchain-blockchain-medical-records.md`
      (PR #509) is cited BY PATH with its in-flight status stated, and its three
      named additions land as requirements 7, 8 and 9 — plus the one CORRECTION
      to it (the cross-plane join key) recorded as a correction rather than
      folded in silently.

## 2. §7.4 COUNCIL REVIEW — HELD AND DISPOSED 2026-08-30; it preceded ratification

- [x] 2.1 Convene a §7.4-shaped council on this packet, **OUTSIDE the clearance
      pipeline**. The ground is measured and code-level: a class over
      `openspec/changes/**` can never commission a council — 984 admitted paths,
      984 floored, 0 remaining on this repository's real tree — so the review
      reaches this repository on the council-reviewed-but-human-approved path,
      which needs no class and no flip (2026-08-28 `gate_rules_council` convening
      record, unanimous 5/5). **HELD 2026-08-30**, four seats returning —
      `lead-architect`, `lead-security`, `lead-quality`, `company-policy-lead` —
      judged at this packet's head `cf5a24b8`. It was a COMBINED sitting over
      #510, #513 and #509, and the disposition RULES THAT INSTRUMENT WRONG
      (item 9): future sittings split, the chain pair together. That ruling is
      against the convening and not against this packet.
- [x] 2.2 Put the six AUTHORING DECISIONS to the seats explicitly (proposal
      § Authoring decisions put to the council): **D-A** the missing-witness
      semantics, **D-B** the structural payload refusal, **D-C** the
      declared-construction commitment refusal and its declared residual, **D-D**
      the change id and capability name, **D-E** deferring the permissioned-ledger
      selection to realization, **D-F** the per-plane key correction to a vendored
      source. D-A is the largest and should be read first. **All six were put and
      all six returned**; a SEVENTH decision this line did not carry was added by
      the convening as ballot C-1 and is 2.5 below.
- [x] 2.3 Record the sitting in `review/`, on `add-binding-consumer-identity`'s
      pattern: seats, verdicts, blocking amendments, and the convener disposition.
      The directory is CREATED WITH THAT RECORD — this packet ships no empty
      `review/`, because an empty one would assert a sitting that has not
      happened. **DISCHARGED IN FULL**: `review/` carries the convening packet,
      the ballot exactly as put (unedited, its two preserved convening errors
      included), the four verbatim seat returns — **which GOVERN over every
      summary** — the council record, and
      **`review/disposition-2026-08-30.md`, the SOLE disposition of record**,
      carried byte-identically in #510's bundle so one act cannot become two.
      Verdicts on this packet: **ACCEPT** from `lead-architect`; **ACCEPT AS
      AMENDED** from `lead-security`, `lead-quality`, and `company-policy-lead`
      within its charter only.
- [x] 2.4 Execute the amendment round the sitting returns, and re-run §1.4 and
      §1.5 against the amended text. **EXECUTED 2026-08-30 against the ruled
      ballot — "accept all fifteen as recommended, 14 folds into the fix
      rounds".** This packet's blocking set is THREE (disposition §5) and all
      three are discharged, plus the one crossing bot finding item 14 folded in:
      * **LS-A5** — the receipt now carries the CONFIGURED WITNESS SET AT MINT
        TIME, so a one-entry receipt is self-evidently incomplete to an
        independent holder and the fail-closed disclosure travels with the
        artifact. Configuration, not status; the receipt/state split is intact.
      * **LS-A6** — requirement 5 gains a KEY CUSTODY REFERENCE on the salt's
        footing (with a shared-across-planes refusal) and a DECLARED SALT SOURCE
        AND WIDTH with a refusal below 128 bits. These are the two parameters
        Q6's erasure property rests on.
      * **LQ-A5, its #513 limb** (disposition item 5) — the wrong *"eighteen
        months"* is STRUCK from requirement 9 rather than restated, on the seat's
        own alternative, since the requirement does not depend on the interval
        and a derived figure in normative text is how the error propagated in the
        first place. **Two seats measured the same gap and got different
        answers** — `lead-quality` 21 whole months (657 days, LQ-F4),
        `company-policy-lead` ~22 (CPL-A1, should-fix) — which is a further
        reason not to seat a contested arithmetic in contract text. The measured
        interval belongs to #509's own fix round, where it is provenance.
      * **The crossing Codex P2**, *"Require de-identification before treating
        metadata as reusable"* — requirement 8 now separates what plane
        separation delivers from what it does not, refuses the de-identified
        label on the strength of separation alone, and leaves the named
        determination to the domain overlay.

      TWO SWEEP COMMITS FOLLOWED, both of them the `455bbdaa` lesson this
      packet already recorded — *a correction stated in a new paragraph does not
      retire the old wording elsewhere in the packet, and a sweep is part of the
      fix*. One retired the *"already supports it"* wording the
      de-identification fix had answered but not replaced. The other struck
      *"eighteen months"* from `proposal.md` as well: **LQ-A5 named only
      `spec.md:658-659` and the disposition scoped it to the requirement text,
      so the blocking amendment was discharged with the proposal's copy still
      standing** — Copilot caught it on the fix round's own pull request, which
      is the same propagation path LQ-F4 named.

      **A BOT ROUND RAN ON THE FIX ROUND ITSELF, AND IT FOUND A P1 IN THE FIX.**
      Codex: LS-A5's discharge as first written bound the configured witness set
      to the proof only in the companion-object form, so in the one-blob form an
      untrusted HOLDER could edit the set rather than the entries and every
      per-chain proof would still validate — **a refusal addressed to the minter
      protecting against the holder, which is LS-F2's own shape reproduced by
      the fix for LS-F7.** Taken: the ANCHORED DIGEST now commits to the set in
      every representation. Two further Codex P2s taken — the `code_surface`
      front matter synchronized with the amended receipt and commitment records,
      and the proposal's *"a `review/` directory … deliberately does not exist
      yet"* paragraph corrected now that it does. The four
      `status-validity` findings are **independently confirmed by Copilot**,
      which prescribes the same remedy recorded above and does not change whose
      act it is.

      **A SECOND BOT ROUND, ON THE HEAD THE FIRST ONE PRODUCED, RETURNED TWO
      MORE P1s — AND BOTH WERE REAL.** Codex: (a) requirement 7 demanded a leaf
      for EVERY verification attempt while requirement 1 exists to let a holder
      verify a receipt WITHOUT contacting the minter, so the audit obligation
      reached events the factory cannot observe — now scoped to the SERVED
      surface, with the unobservable half named as a property of the receipt's
      self-sufficiency and the tempting alternative (a reporting obligation on
      independent verifiers) refused for what it would cost; (b) requirement 8
      named the meta-analysis lane a first-class consumer while its own fourth
      correction refused the stable shared key that lane needed to correlate
      anything — **an unachievable-by-construction obligation, the family the
      2026-08-28 convening refused a class over** — now answered by an
      AUTHORIZED, SCOPED LINKAGE DERIVATION whose every adjective is a refusal.
      Recorded as `design.md` D10 and as an amendment note under D7.
      **Three of this packet's ten design decisions now exist because a bot
      found a control that could not run**, which is the argument for the bot
      round being part of the work rather than a formality.

      **A THIRD BOT ROUND FOUND TWO MORE P1s, AND BOTH WERE HOLES THE SECOND
      ROUND'S OWN FIXES OPENED.** (a) Scoping requirement 7 to the SERVED
      surface carried the source's refusals and dropped its successes: a
      PERMITTED authenticated read is neither a verification nor a refused
      attempt, so an observable class inside the newly-drawn surface was
      unlogged — while the requirement's own provenance block quotes the source
      logging *"views"*. Permitted decisions are now required on the same
      footing as refusals, and the requirement is renamed to say so
      (**"Served verification and access decisions are logged leaves"** — the
      council record quotes its former title, and this line is where a reader
      follows the rename). (b) The linkage derivation was made revocable and
      consent-gated while requirement 8's scenario still promised the result was
      *"unaffected by whether the identity plane was reachable"* — which
      requirement 6 refuses outright, since an unevaluable consent never reads
      as permission. **Both could not hold**: an implementation would either
      bypass a fresh revocation or break the availability promise. Reconciled by
      scoping the promise to the UNCORRELATED analysis (which needs no
      derivation and no consent evaluation, and is all the headline ever
      claimed) and making every USE answer to the current revocation state, the
      correlation refusing when that state cannot be read.

      **THE PATTERN IS NOW THE FINDING.** Three consecutive bot rounds, and in
      each of the last two the P1 was in the previous round's fix rather than in
      the council-judged text. That is not a bot being pedantic — it is the
      measured cost of amending contract prose under time pressure, and it is
      why the rounds keep earning their place. Both P2s of this round are the
      same shape one layer down: the `code_surface` and the leaf-grammar task
      had not moved with the new record, so an implementer following either
      would have shipped without the derivation's fields or without anywhere to
      define its leaves. Both taken.

      **A FOURTH BOT ROUND RETURNED ONE P1 AND ONE P2, AND THE P1 CARRIES A
      GOVERNANCE FLAG THAT THE RATIFICATION READ MUST SEE.** Codex, at
      `bdb37517`: *"Define when pending becomes incomplete"* — every freshly
      submitted item has no witnesses yet, so requirement 3's opening SHALL made
      it `anchor_incomplete` while the next sentence had it enter
      `anchor_pending`, leaving no deterministic state for the ordinary
      aggregation window. **That is LS-F11, found independently and rated a full
      grade higher, and its discharge is LS-A9 — WHICH THE DISPOSITION DID NOT
      DISPOSE.** §6 leaves the should-fix schedule *"item by item"* open and §5
      lists LS-A9 among this packet's should-fix set; item 13 is the precedent
      for elevation and there it was done BY BRETT, BY NAME.

      **This session first escalated the finding rather than executing it, and
      then executed it on the direction of the session coordinating this fix
      round. BOTH FACTS ARE RECORDED BECAUSE THE SECOND DOES NOT ERASE THE
      FIRST.** What landed: the two states are now DISJOINT BY DEFINITION — an
      item is `anchor_pending` while every unmet witness is within its declared
      horizon, and becomes `anchor_incomplete` only on an explicit transition
      (horizon breach, or a named terminal witness failure), each written as a
      leaf; four scenarios pin the fresh item, the breach, the terminal failure
      and the healthy late arrival; and a verification of a pending item returns
      `anchor_pending` naming the witnesses in flight. **That second half was
      added because making the states disjoint without it would have sharpened
      LS-F11's other residual rather than closed it** — but it means the change
      now covers BOTH limbs of LS-A9, so this is LS-A9 executed, not merely the
      bot's narrower limb.

      **WHAT THE RATIFICATION READ IS OWED, PLAINLY: an amendment the convener
      left undisposed has been executed by a fix round.** It is one isolated
      commit, nothing is merged, and reversing it costs a revert. Brett may bless
      it, reverse it, or rule the elevation properly as item 13 did — and this
      box exists so that the choice is his and visible, rather than discovered
      later in a diff. **No other should-fix item has been touched**; LA-A7,
      LS-A7, LS-A8, LQ-A10, LQ-A11, LQ-A12, LQ-A14 and CPL-A5 remain open and
      undisposed.

      The P2 of that round — no decidable shape for the refused-correlation
      result, which is the seam this session asked the bot to break — **was taken
      without reservation**, because it lands on text this fix round authored and
      not on any seat's schedule. The result now carries a CLOSED-ENUMERATION
      status discriminator, the named omitted correlation, and its refusal ground
      from a named enumeration rather than free text, with the per-plane results
      carried distinctly; a silently partial result is refused as non-conforming.
      Settled in 5.6 alongside 5.3's leaf kinds, since the same events produce
      both.

      **A SIXTH BOT ROUND CLOSED THE SEAM THE FIFTH ONE OPENED, WHICH THIS
      SESSION HAD INVITED BY NAME.** Making the two states disjoint gave them
      different verification answers, and the receipt carried no timing at all —
      so a receipt-only verifier could not tell pending from incomplete, the
      artifact being byte-identical before and after a breach. **Both halves of
      the fix were taken, split by what each verifier can know**: the mint-time
      configuration block now carries each witness's DECLARED HORIZON and the
      SUBMISSION TIME they run from, bound by the anchored digest exactly as
      LS-A5's witness set already was — **one mechanism extended, not a second
      minted** — so a receipt-only verifier computes `anchor_pending` or the
      receipt-only `anchor_incomplete` LOCALLY; and the TERMINAL-failure
      distinction is scoped to STATEFUL verification, because a terminal failure
      arises after the receipt was minted and no artifact can carry it. Both
      limits are stated in the text rather than left to a reader: past the
      horizon a receipt-only answer cannot separate a breach from a terminal
      failure, and within it `anchor_pending` cannot exclude one. **That is D10's
      shape reapplied — what the artifact can prove it proves, what it cannot it
      names.** An extended horizon now breaks the proofs, closing the tamper this
      opened before anyone had to find it.

      **THE SETTLEMENT LIST WAS RE-DERIVED BY EQUALITY RATHER THAN PATCHED, AND
      THE SWEEP FOUND ONE MORE THAN THE BOT DID.** Codex named the missing
      TERMINAL-WITNESS-FAILURE leaf in 5.3. Re-running the check as an equality
      between every leaf the spec mandates and 5.3's list surfaced a second
      omission the bot had not reached — requirement 4's ITEM-ANCHOR-REFUSAL
      leaf, mandated in its scenario and settled nowhere. Both are added with
      their required fields, and requirement 4's VALIDATION-FAILURE leaf is
      recorded as deliberately absent with its ground: it is a GATE VERDICT,
      already in tranche one's ratified leaf set, and settling it here would mint
      the second grammar 5.3 forbids. **This is the two-field sweep lesson
      applied to a list instead of a pair** — a bot finds the instance, the
      equality check finds the class.

      Copilot, same round: §5's numbering ran 5.5, 5.6, 5.4 because the two new
      settle items were appended rather than placed. Reordered monotonically, so
      the cross-references in this file resolve in reading order.

      **A SEVENTH ROUND, TWO P1s AND TWO P2s, ALL FOUR INSIDE THE LAST TWO
      ROUNDS' OWN TEXT.** (a) **The minter's clock was trusted.** Binding the
      submission time into the anchored digest made it TAMPER-EVIDENT, not TRUE:
      a future-dated mint kept a receipt-only verifier reporting a healthy window
      long after the real horizon passed, suppressing the very transition the
      fix-closed design exists to force. Material cannot be anchored before it is
      submitted, so every landed entry's CHAIN-ACCEPTED TIME bounds the truth —
      the receipt-only determination now runs from the EARLIEST CHAIN-ACCEPTED
      TIME and never from the minter's claim, and a declared time later than it
      is refused as provably false. Where NOTHING has landed there is no chain
      evidence at all: the base is labelled MINTER-CLAIMED and the verifier makes
      no pending-versus-breached determination, naming the record as what can.
      **D10's rule applied to a clock instead of an event.** (b) **A surviving
      scenario branch still told the receipt-only verifier to claim no lifecycle
      state**, contradicting the paragraph that requires `anchor_pending` — so
      the whole receipt-only scenario SET was re-read as a set rather than the
      one branch patched, which surfaced two further inconsistencies the finding
      had not named: a bare *"returns INCOMPLETE"* predating the state
      vocabulary, and a horizon still measured from the submission time. (c)
      **Callers could not tell a receipt-only `anchor_pending` from a stateful
      one**, though a terminal failure inside an unexpired horizon makes them
      genuinely different answers — every verification result now carries a
      mandatory closed-enumeration VERIFICATION MODE, the same discriminator
      discipline the analysis-result shape uses, because a caller branches on a
      value and never on a paragraph. (d) The equality sweep's own omission,
      recorded above where the method is described.

      **AN EIGHTH ROUND, THREE P1s, AND THE THIRD ONE FOUND THE ESCAPE ROUTE.**
      (a) **CHAIN-ACCEPTED TIME was used as a clock without being one.** The
      evidence proved THAT a block was accepted and named no INSTANT, so a header
      timestamp, an observation time and a confirmation time were three
      admissible readings of a fail-closed decision. It is now derived FROM THE
      RECEIPT'S OWN BYTES — the block header each entry already carries, its time
      field, against that chain's cited consensus rule — deterministic given the
      bytes and identical for any two verifiers, with a DECLARED TOLERANCE
      applied in one direction only (never a false breach). A chain whose header
      has no usable time field is declared as contributing ORDERING AND INCLUSION
      ONLY rather than having a timestamp invented for it.
      (b) **The pre-anchor delay was unbounded, so the base itself was the
      attack** — a minter sitting on material moves every horizon later and keeps
      a receipt-only verifier saying `anchor_pending` forever. Two instruments,
      both already in this design's inventory: **THE LOG IS THE INDEPENDENT
      SUBMISSION WITNESS** (the submission leaf sits under anchored checkpoints,
      so the earliest checkpoint containing it upper-bounds the true submission
      on evidence no minter controls, and stateful verification enforces the
      bound against THAT), and a **DECLARED MAXIMUM SUBMISSION-TO-FIRST-ANCHOR
      DELAY carried in the mint-time configuration block** and bound by the
      anchored digest, so a receipt exceeding its own declared maximum is
      SELF-INCONSISTENT and refused. **AND THE EARLIER RESIDUAL CLAIM WAS WRONG
      AND IS CORRECTED IN THE TEXT**: "at most one aggregation interval" was
      asserted with nothing capping the delay, so the true bound was unlimited —
      this packet's own claims-outrunning-machinery defect, committed by the
      round that was fixing one.
      (c) **The proposal's D-A summary still classified the healthy window as
      `anchor_incomplete`**, five rounds after the disjoint-state fix. The spec
      had been swept for the state vocabulary; **the companion documents never
      had been** — the new-conjunct family's known escape route, the docs one
      ring out. Both were swept and the hits fixed:

      | Document | Site | Defect | State |
      |---|---|---|---|
      | `proposal.md` | D-A summary | healthy window called `anchor_incomplete` | FIXED |
      | `proposal.md` | `code_surface` mint-time block | no delay maximum; horizons still described as running from the minter's submission time | FIXED |
      | `design.md` | D2 bullet | "fewer witnesses than configured is `anchor_incomplete`" — the superseded predicate verbatim | FIXED |
      | `design.md` | D2 outage table | both outage rows stated `anchor_incomplete` with no pending phase | FIXED |
      | `design.md` | D2 LS-A5 note | "shorter than that set is incomplete on its face" — an artifact asserting a lifecycle state | FIXED |
      | `design.md` | D2 "permanently incomplete", D8/D9 prose | post-breach or rhetorical uses | CORRECT AS WRITTEN |

      **A NINTH ROUND, THREE P1s, ALL THREE INEQUALITY-DIRECTION ERRORS IN THE
      EIGHTH ROUND'S CLOCK — the sharpest class yet, because each one READ AS
      RIGOUR while pointing the wrong way.** (a) *"Material cannot be anchored
      before it is submitted"* is true of the anchoring ACT and false of the
      header TIMESTAMP, which consensus validates against a median of preceding
      blocks rather than against any submission's wall clock. A valid accepting
      block can therefore carry a time EARLIER than the submission it covers, so
      the round-eight refusal **would have rejected honest receipts** and the
      same backward skew would have manufactured breaches that never happened.
      Each chain's declared band is now stated as its consensus rule's WORST
      LEGAL CASE, cited, and **one declared value serves BOTH uses** — the
      pending computation and the self-consistency refusal — so two margins
      cannot drift apart. (b) The containing checkpoint is anchored AFTER the
      submission it witnesses, so the interval from it to the first anchor is a
      **LOWER bound** on the delay: it PROVES a breach when it exceeds the
      maximum and **NEVER PROVES COMPLIANCE**, which the text now says outright —
      *not-provably-breached is not compliant*. A **DECLARED CHECKPOINT CADENCE**
      makes the bound tight to one interval, and violating the cadence is a
      SECOND, INDEPENDENT breach with its own leaf, so withholding checkpoints to
      widen the bracket is visible rather than being the way out. (c) The time
      rule and its tolerance were not digest-committed, so a holder could swap
      the rule or enlarge the tolerance while every inclusion proof still
      validated.

      **AND (c) WAS THE THIRD OCCURRENCE, SO THE FIX IS A RULE AND NOT A FIELD.**
      The configured witness set, then the horizons and submission time, then the
      time rule and tolerance each arrived outside the committed block and each
      had to be swept in after a bot found it. The mint-time configuration block
      is now **CLOSED BY RULE — every value the receipt-only computation reads is
      committed by the anchored digest** — so a future input joins by that rule
      rather than by an enumeration chase. **The closure rule carries its own
      scenario** (an uncommitted receipt-only input is refused), because a rule
      with no scenario is precisely the described-control defect this packet has
      now paid for three times.

      **THE TIMING-MODEL TRIPWIRE: ARMED, AND UNFIRED FOR A REASON THAT IS NOT
      "CLEAN".** After three consecutive rounds found DIRECTION ERRORS in the
      same clock machinery, a pre-commitment was set: a further clock-area
      defect would stop the incremental patching and trigger a deliberate
      CONSOLIDATION — the timing model restated as ONE coherent section (the
      clocks, every bound with its direction as an inequality, every width with
      its citation, the closure rule, and what each verifier mode can and cannot
      conclude), derived fresh and then CHECKED AGAINST EVERY EXISTING SCENARIO,
      since the scenario set is nine rounds of accumulated adversarial knowledge
      and the consolidation must satisfy all of it or name which scenario was
      wrong. **It did not fire, and the honest reason is that ROUND TEN NEVER
      RAN**: the reviewing bot reached its usage limit and returned a quota
      refusal rather than a verdict. **That is not the same as a clean round and
      is not recorded as one.**

      **WHAT THAT LEAVES, STATED PLAINLY.** The head carrying round nine's three
      discharges is **UNREVIEWED BY ANY BOT**. The tripwire stays armed for
      whoever runs the next review. And the case for the consolidation does not
      depend on a tenth finding: the timing model is currently spread across
      **EIGHTEEN normative paragraphs in two requirements**, accreted over four
      rounds, holding three separately-established bounds, two declared widths, a
      cadence, a closure rule and two verifier modes — measured, not estimated.
      **Nobody can hold that as one model while reading it, which is the most
      likely reason three consecutive rounds found direction errors in it.** The
      consolidation is therefore available on a convener's or coordinator's word
      as a restructure-with-proof; **this session did not perform it, because an
      untriggered tripwire is not a mandate** and a fix round rewriting a
      requirement's structure on its own initiative is the shape of overreach
      this record has been careful about elsewhere.

      **BRETT HEAP'S CLOSING RULING, 2026-08-30 — SIX ITEMS, VERBATIM:** *"1 yes,
      2 yes with note, 3 merge, 4a, 5 bless, 6a."* Three of the six land in this
      box.

      **RULING 6a — THE TIMING-MODEL CONSOLIDATION IS PERFORMED, ON HIS WORD AND
      NOT ON THE TRIPWIRE.** The tripwire above was defined to fire on a further
      clock-area defect from a tenth bot round; **the tenth round never ran**, so
      it never fired and is superseded rather than triggered. **The distinction
      is recorded because a ruling and an automatic trigger are different
      authorities**, and a later reader must not conclude that the machinery
      decided this. Executed as pre-committed: THE TIMING MODEL is now one
      delimited section of the receipt requirement — three clocks, every bound as
      an inequality with its direction, every width with its citation, the three
      decisions and their shared one-directional margin, a closed table of what
      each verifier mode may conclude, and the closure rule — and the eleven
      scattered paragraphs plus four in requirement 3 are now REFERENCES to it.
      **SEMANTICS CHANGED NOWHERE**: round ten never ran, so nothing was learned
      that could justify one. The proof is the scenario set, checked in full —
      **every clock-relevant scenario satisfied, NONE overturned**, no scenario
      rewritten. Recorded as `design.md` **D11**, with the realization mirror at
      §5.2. Nine requirements and 89 scenarios, both unchanged.

      **RULING 5 — LS-A9's EXECUTION IS BLESSED.** Brett Heap, 2026-08-30,
      verbatim *"5 bless"*. This box recorded above that a fix round had executed
      an amendment the convener left undisposed, and that the ratification read
      was owed the plain version with a revert one commit away. **His blessing
      converts that execution into HIS ACT**, so the amendment stands as ruled
      rather than as tolerated, and **the revert path closes**. What is NOT
      rewritten is the history: this session escalated the finding first,
      executed it on the coordinating session's direction second, and is blessed
      third. All three remain on the record, because a blessing settles the
      authority and does not edit the sequence.

      **SEVEN ROUNDS, AND THE SHAPE OF THE FINDINGS HAS CHANGED.** The first
      rounds found defects in the council-judged text; the last four have found
      defects in this fix round's own repairs, each one narrower than the last.
      That is convergence rather than churn — but it is also the honest measure
      of how much a fix round costs to get right, and it is recorded here rather
      than smoothed into a clean summary.

      SHOULD-FIX items (LA-A7, LS-A7/A8/A9, LQ-A10/A11/A12/A14, CPL-A5) are
      **UNDISPOSED by the ruling and stay open** — disposition §6 says so
      expressly, and no silence here rules them.

      **§1.4 AND §1.5 RE-RUN, AND THE RESULT IS REPORTED RATHER THAN ROUNDED.**
      §1.4: `--strict` green and `--all --strict` **79 passed / 0 failed**;
      NINE requirements unchanged, **52 → 89 scenarios**, still no `## MODIFIED`
      block. §1.5: doc-health against `origin/main` with a matched baseline
      basename returns **four new findings, all `status-validity`, all on the
      carried `review/` bundle** — the sitting's four top-level records write
      `Status: record — <qualifier>` on one line and the family reads the
      remainder as a free-form status. **The amendment round itself is
      ZERO-NEW.** The four are NOT fixed here: the disposition rules the packet
      and the ballot unedited and requires itself carried byte-identically in
      #510's bundle, so normalizing this copy alone would manufacture the drift
      that rule exists to prevent. Two lawful remedies, both above a fix round —
      the record's owner normalizes all four headers in BOTH bundles (the
      qualifier moves verbatim to the next line, nothing lost), or a governed
      change widens the lifecycle scan set's byte-exact-evidence exclusion to
      reach carried sitting bundles, which the doc-health capability requires be
      a promoted change recording the measured effect. **Left visible rather
      than tidied**, because the nightly runs this family and an unreported
      regression surfaces later as somebody else's.
- [x] 2.5 **THE ANCHOR-LATE NARROWING IS ROUTED, NOT ONLY RECORDED.** The staged
      topic's constraint — *"anchoring LATE (commit only what has been
      validated)"*,
      `ideation/staging/signed-execution-chain/signed-execution-chain.md:471-478`,
      sitting in that topic's `## Conflicts` section and reached by none of its
      seven Q-dispositions — is NARROWED by this packet (requirement 4, design
      D8). **2.2 did not put it to the seats, so the convening added it as ballot
      C-1**, and it was RULED at disposition item 6: **(i) correct and faithfully
      recorded — the narrowing stands.** The ruling's other half is a standing
      rule on FUTURE packets: a packet that narrows a staged topic's constraint
      SHALL ROUTE the narrowing to its council as an explicit decision rather
      than merely record it (`review/disposition-2026-08-30.md` §3.1;
      `review/council-review-2026-08-30.md` §8.1). Recorded here because
      **recorded is not ruled**, and a `## Conflicts` section carries unruled
      material by design.

## 3. Ratification gate — Brett Heap's act, AFTER the review — DONE 2026-08-30

**RATIFIED 2026-08-30 BY BRETT HEAP**, in session, ruling item 2 of six:
*"2 yes with note"*. Record: **`review/ratification-2026-08-30.md`**.
**Ratification authorizes REALIZATION and performs none of it**, and it moves no
contract byte.

- [x] 3.1 Brett Heap ratifies or declines, having read the council record
      (`review/council-review-2026-08-30.md`), the disposition
      (`review/disposition-2026-08-30.md`) and this fix round.
      **RATIFIED, WITH A NOTE THAT IS PART OF THE ACT**: the heads from
      `fd7c1ca7` onward — round nine's three discharges, the tripwire
      bookkeeping, and the ruling-6a consolidation — are **UNREVIEWED BY ANY
      BOT**, the reviewing bot having returned a quota refusal rather than a
      verdict. Disclosed head-by-head on the pull request BEFORE the ruling, so
      the ratification is made with that tail in view and under the recorded
      prescribed-fix principle. A refusal to review is not a clean review and
      this box does not let the two read alike.
- [ ] 3.2 On ratification: `target_release` is CONFIRMED against
      `contracts/manifest.yaml` at that tip rather than at this one, and remains
      allocated by merge order — `add-signed-execution-chain` and
      `add-chain-attestation` reach the same additive cut.
- [x] 3.3 On ratification: front-matter gains `Status: ratified` plus the
      `Ratified:` line naming the record path, and the README record line is
      updated to match.

## 4. Realization — the contract family and its validator

- [x] 4.1 `contracts/chain-anchoring/` — the multi-anchor receipt record (four
      per-chain elements, the declared header source, and the MINT-TIME CONFIGURATION
      BLOCK — the configured witness set, each witness's declared horizon, and
      the submission time they run from — which the ANCHORED DIGEST commits to in
      every representation, the material digest staying nameable beside it), the
      DECLARED CHAIN-ACCEPTED-TIME RULE per configured chain (the entry's own
      block-header time field, its cited consensus rule, and its declared
      tolerance — or a declaration that the witness contributes ORDERING ONLY),
      the DECLARED MAXIMUM SUBMISSION-TO-FIRST-ANCHOR DELAY and the DECLARED
      CHECKPOINT CADENCE, all of them carried in the mint-time configuration
      block, which is CLOSED BY RULE — every value the receipt-only computation
      reads is committed by the anchored digest, so a later input joins the set
      by that rule and not by an enumeration chase. The
      VERIFICATION RESULT record carrying its mandatory VERIFICATION MODE
      (`receipt_only` / `stateful`, a closed enumeration) plus, for a
      `receipt_only` result, whether its horizon base was chain-derived or
      MINTER-CLAIMED, the
      log-checkpoint anchor record with its never-read-as-validation disclaimer,
      the anchor-bound commitment record (declared construction, SALT and KEY
      custody references, declared salt source and width), the anchor-state
      record (per-witness, with declared horizons and NO aggregate boolean), the
      consent-checkpoint commitment record, the plane-separation declaration,
      and the AUTHORIZED LINKAGE DERIVATION record (issuing plane, anchored
      consent checkpoint, per-analysis parameter, expiry and revocation, and
      the leaves issuance and use write), and the ANALYSIS RESULT record with
      its OUTCOME DISCRIMINATOR.

      **DONE — `contracts/chain-anchoring/`, twelve files.** `anchoring-definitions`
      (the shared vocabulary, declaring no record kind, taking the ONE digest
      construction by `$ref` and spelling no second witness role, plane name,
      custody reference, duration or refusal code), then eleven record shapes:
      `anchor-receipt` (four per-chain elements, the declared header source, and
      the mint-time configuration block the anchored digest commits to),
      `verification-result` (mandatory `receipt_only`/`stateful` mode, with the
      horizon base declared chain-derived or minter-claimed),
      `anchor-bound-commitment` (declared construction, SALT and KEY custody
      references, declared salt source and width), `anchor-state` (per-witness,
      declared horizons, no aggregate boolean),
      `consent-checkpoint-commitment`, `log-checkpoint-anchor` (carrying its own
      never-read-as-validation disclaimer), `plane-separation-declaration`,
      `linkage-derivation-issuance`, `linkage-derivation-use`,
      `analysis-result` and `conformance-declaration`. Each validates as YAML and
      as a stock Draft 2020-12 schema; the leaf kinds and digest subjects they
      need are settled in tranche one's grammar (5.3), not in a second one.
- [x] 4.2 Packaged POSITIVE and NEGATIVE examples for every named refusal — a
      receipt missing inclusion proof; a receipt missing transaction bytes; a
      receipt missing chain-acceptance evidence; a receipt whose header is
      non-canonical; a verification run against a minter-supplied header source;
      **a receipt carrying no configured witness set**; **a captured receipt
      whose configured witness set a holder has rewritten OR whose declared horizon
      a holder has extended**; **a representation
      carrying the configured set with no commitment binding it to the proof**;
      a checkpoint inclusion presented as validation; a
      single-witness item presented as anchored; a per-item selectivity rule; a
      third anchor target; a content-bearing field; ciphertext; an absent
      construction declaration; an honestly-declared plain digest; a salt custody
      reference resolving onto a chain; **a construction declaring no salt source
      or width**; **a declared salt width below the floor**; **a KEY custody
      reference resolving onto a chain or into the anchored record**; **a
      commitment key shared across planes**; a per-subject consent row offered
      for anchoring; an attempt row offered for direct anchoring; a
      direct identifier in the demographic plane; a shared cross-plane key;
      **a plane-separated analysis result labelled de-identified**; **a linkage
      derivation re-used across analyses**; **a correlation path derived
      outside the identity plane or without a consent checkpoint**; **a
      reporting obligation imposed on independent verifiers**; **a realization
      logging refused access but not permitted access**; **a correlation using a
      pre-issued derivation whose revocation state cannot be read**; **a receipt
      self-inconsistent about its own declared maximum delay**; **a horizon base
      taken from a minter's clock rather than a block header**; **a breach
      declared inside the declared timestamp tolerance**; **an honest receipt
      refused because its declared submission fell after the header time within
      the legal skew**; **a delay check read as proof of compliance**; **a
      realization anchoring checkpoints less often than its declared cadence**;
      **a receipt-only input carried outside the committed configuration
      block**; **an analysis
      result missing its correlation with no declared outcome**; a
      domain record kind; an overlay relaxing a neutral refusal. The bolded
      entries are the refusals the 2026-08-30 fix round added.

      **DONE — 21 positives and 75 single-fault negatives**, packaged under
      `contracts/chain-anchoring/examples/` and `examples/negative/`. The
      positives are adjudicated as ONE coherent scope (a healthy dual-witness
      receipt, the ordering-only chain reaching `no_determination`, the honest
      twin accepted inside the skew, the sat-on minter caught by the checkpoint
      bracket, the served/local pair over one item, the three-state lifecycle,
      the correction anchored forward, and the declared-shortfall declaration);
      each negative is NAMED for the code it provokes and pinned further by an
      `# expected_failure_detail:` substring. Measured by the reader's own
      self-test: **70/70 closed refusal codes red-proven**, plus five further
      finding codes probed for the semantic rules whose codes live outside the
      closed enumeration.
- [x] 4.3 `scripts/validate-chain-anchoring.py` — the canonical refusing
      validator. The payload refusal is STRUCTURAL (D3); the unsalted-commitment
      refusal is by DECLARED CONSTRUCTION plus salt-custody resolution, KEY-
      custody resolution, and the declared salt source and width against the
      floor (D4, as amended by LS-A6).

      **DONE — `scripts/validate-chain-anchoring.py`.** Run at this branch's head:
      `0 error(s), 2 warning(s)`, the two warnings being the family's own standing
      honest declarations (`reader-not-required`, `archival-node-undeclared`) and
      not defects. The payload refusal is STRUCTURAL — the shape refuses any
      content-bearing member rather than recognizing what content is about, which
      is what keeps it neutral — and the unsalted-commitment refusal is by
      DECLARED CONSTRUCTION plus salt-custody resolution, KEY-custody resolution,
      and the declared salt source and width against the floor.
- [x] 4.4 **The declared residual of D4 is discharged or DECLARED**: establish
      that the commitment path is the ONLY path that can mint an anchor-bound
      value, so an undeclared construction is unreachable; a realization that
      cannot establish it declares the shortfall on `add-trust-anchor`'s
      declared-shortfall pattern rather than asserting the property.

      **DONE BY THE SECOND BRANCH — the residual is DECLARED, not asserted
      closed.** This realization cannot establish that the commitment path is the
      only path that can mint an anchor-bound value: a reader cannot tell a
      declared salted keyed commitment from a plain digest by inspection, and it
      says so in its own docstring. So `CA-R5-COMMITMENT-PATH` is carried as a
      STRUCTURAL RESIDUAL on `add-trust-anchor`'s declared-shortfall pattern in
      `examples/conformance-declaration-1-declared-shortfall.example.yaml`, and a
      declaration recording that obligation `satisfied` is REFUSED by the reader
      — red-proven by `examples/negative/structural_residual_declared_satisfied.yaml`.
- [ ] 4.5 **[OPERATOR] The operational witness's ARCHIVAL NODE** — Q3's first
      condition. Evidence is a running node reachable by the anchoring subsystem,
      named by endpoint, not a plan to run one.
- [ ] 4.6 **[OPERATOR] Inclusion-proof CAPTURE AT ANCHOR TIME** — Q3's second
      condition, and the half most likely to be deferred. Evidence is a captured
      receipt for a real anchor carrying transaction bytes, inclusion proof and
      header and chain-acceptance evidence, verified with the chain unreachable
      against an independently obtained canonical header set.
- [ ] 4.7 **[OPERATOR] Inclusion-proof RETENTION** — Q3's second condition's other
      half. Evidence is a receipt verified AFTER the operational chain has pruned
      the transaction, which is the only test that actually proves retention.
- [x] 4.8 **Corroborating-only status is ENFORCED, not stated** — Q3's third
      condition. A claim standing on the operational witness alone is refused by
      a check, and a ten-year claim cites the durability witness.

      **DONE — enforced by the reader, not stated in prose.** Two closed refusals
      carry it, each red-proven by a named fixture:
      `examples/negative/claim_stands_on_operational_witness_alone.yaml` (a claim
      standing on the operational witness alone) and
      `examples/negative/ten_year_claim_on_operational_witness.yaml` (a ten-year
      claim not citing the durability witness). Selectivity is refused beside
      them (`witness_selectivity_rule.yaml`), and a third anchor target is refused
      by name (`third_anchor_target.yaml`). **THE OPERATOR CONDITIONS 4.5-4.7 AND
      4.9 REMAIN OPEN AND THIS BOX DOES NOT REACH THEM**: what is enforced here is
      that a realization cannot CLAIM more than its witnesses support, which is a
      different thing from a witness existing.
- [ ] 4.9 **[OPERATOR] The durability witness's aggregation path** — public
      calendars or a self-run hourly calendar (study §8: $0 marginal per item, or
      ≈$2.1k/yr self-run). Evidence is a completed upgrade on a real item.
- [ ] 4.10 The BOTH-WITNESSES rule is exercised end to end, including its
      degraded paths: an item with each witness missing in turn reaches
      `anchor_incomplete` naming that witness, a horizon breach writes its leaf,
      and the durability-calendar recovery UPGRADES THE PENDING DURABILITY PROOF
      and appends its entry rather than re-anchoring.
- [x] 4.11 Registration in `contracts/manifest.yaml` and `contracts/CHANGELOG.md`
      at the additive bundle cut, with `target_release` confirmed against the
      manifest at that tip.

      **THE TIMING IN THIS BOX'S OWN TEXT WAS OVERRULED BY THE REPOSITORY
      OWNER.** Brett Heap, 2026-09-04, in session, verbatim: *"merge 629,
      register now"* — a RULING for lane `openxfactory-1d`'s PR #629 that the
      registration is performed NOW, at realization, on this pull request. The
      ground is the TRANCHE-TWO PRECEDENT: `add-chain-attestation` added its
      eight manifest rows inside its realization (#556, squash `518c670b`) and
      left only the version bump and the changelog entry to the cut (#565,
      squash `bbbbeda9`). This box closes over THE REGISTRATION HALF and says
      so; the cut half is CARRIED to 4.12 rather than claimed here.

      **DONE — TWELVE ROWS in `contracts/manifest.yaml`**, one per schema in
      `contracts/chain-anchoring/`, in the order the family README's twelve-file
      table takes them: `chain-anchoring-definitions`, `-anchor-receipt`,
      `-anchor-state`, `-verification-result`, `-anchor-bound-commitment`,
      `-log-checkpoint-anchor`, `-consent-checkpoint-commitment`,
      `-plane-separation-declaration`, `-linkage-derivation-issuance`,
      `-linkage-derivation-use`, `-analysis-result`,
      `-conformance-declaration`. Each row id IS the schema's own `contract_id`,
      on #556's precedent, and each carries a per-file `sha256` over the bytes
      at this commit. Measured by `python3 scripts/validate-manifest-digests.py`
      at this head: `OK contracts/manifest.yaml: 175 per-file digest(s) verify`
      — **163 before, 175 after, the twelve added**. Plus **ONE README
      paragraph**: the family README's `Repository context:` block, which read
      **NOT YET REGISTERED** in the present tense and now states the
      registration, the owner's word, the precedent, and what remains the
      cutting session's.

      **NO BUNDLE NUMBER IS TAKEN OR RESERVED BY THIS COMMIT.**
      `contract_bundle_version` still reads `contract-v3.2` and no row names a
      forthcoming number — the ONE deliberate divergence from #556's row text,
      taken because `docs/contract-versioning-policy.md` § Bundle Realization
      Order fresh-counts the number at the tip the cut is taken from and a
      proposed change MUST NOT reserve a minor number before merge order is
      known. `contract-v3.3` is unspent at this writing and this commit does not
      spend it.

- [ ] 4.12 **THE CUT HALF, carried out of 4.11 rather than claimed by it.** The
      `contracts/CHANGELOG.md` entry, the `contract_bundle_version` bump to the
      number fresh-counted at the cut's tip, the `contracts/README.md` durable
      contract-index row (a release-inventory member, so it moves with the
      inventory the cut rebuilds), the digest inventory rebuilt with
      `scripts/validate-contract-release.py build`, `target_release` confirmed
      against the manifest at that tip, and `verify-commit` / `verify-tag` green
      from an independently refreshed clone. The CUTTING SESSION's act, on
      #565's precedent, and not this realization's.

## 5. Settle before schemas are authored

- [ ] 5.1 Fix the ANCHORED-ITEM UNIT — what exactly is anchored: a transparency-log
      checkpoint, a state root, or both, and at what granularity the aggregation
      batches. Requirement 1 fixes the receipt SHAPE and deliberately not the unit.
- [ ] 5.2 Fix the COMPLETION HORIZONS — the declared values per witness, bounded
      by the aggregation interval chosen in 5.1; the DECLARED MAXIMUM
      SUBMISSION-TO-FIRST-ANCHOR DELAY; and, per configured chain, the
      CHAIN-ACCEPTED-TIME RULE with its cited consensus rule and its declared
      TOLERANCE AND SKEW BAND stated as that rule's WORST LEGAL CASE (or the
      declaration that the witness contributes ordering only); and the CHECKPOINT
      CADENCE, which is what makes the delay bound tight.
      Requirement 3 requires that all of these be DECLARED; it names no numbers,
      and the fail-closed determination is only as good as they are.
      **THE REALIZATION MIRROR OF THE CONSOLIDATION (D11):** these values are the
      inputs THE TIMING MODEL names, and they are settled AS ONE SET rather than
      per-schema — the three clocks, `skew` and `tolerance` per chain with their
      cited consensus rules, `C` the checkpoint cadence, `D_max`, and each
      witness's horizon. **The model's closure rule binds this task**: any value
      the receipt-only computation reads joins the mint-time configuration block
      and is committed by the anchored digest, so a realization that introduces a
      new timing input settles it here and carries it there, rather than adding
      it beside the block as four rounds of this packet did.
- [x] 5.3 Fix the NEW LEAF KINDS against tranche one's leaf grammar. This packet
      adds no second grammar and must not, so tranche one's grammar is where each
      event discriminator and its required fields are settled; requirements 3, 4,
      7 and 8 mandate these leaves and none of them defines a field. **THE LIST IS
      SETTLED BY A ONE-PASS EQUALITY CHECK against every leaf the spec mandates,
      not by accumulation** — the check is recorded in §2.4 and is to be re-run
      whenever a requirement gains or loses a leaf:
      * `anchor-pending` entry (requirement 3)
      * `horizon-breach` transition — witness named (requirement 3)
      * **`terminal-witness-failure` transition — WITNESS NAMED and FAILURE GROUND
        named (requirement 3).** One of the two permitted transitions out of
        pending; without a settled shape a realization can omit the evidence for
        half the state machine
      * `anchor-completion` (requirement 3)
      * **`item-anchor-refusal` — the material refused and the ground
        (requirement 4).** Its scenario mandates a leaf and no settlement named it
      * **`correction-anchored-forward` — the superseded anchored material, the
        correcting material, and the ground (requirement 4).** *"A RETRACTION IS
        A NEW LEAF AND A NEW ANCHOR, NEVER AN ERASURE"*: the correction is
        recorded and anchored forward, and nothing is withdrawn
      * `verification` and `verification-failure` (requirement 7)
      * `permitted-access` and `refused-access` (requirement 7)
      * `linkage-derivation-issuance` and `linkage-derivation-use` (requirement 8)
      NOT here, and each for a stated reason: the VALIDATION-FAILURE leaf of
      requirement 4 is a GATE VERDICT, which tranche one's ratified leaf set
      already carries, so settling it here would mint the second grammar this
      task forbids.
      **THE EQUALITY IS RE-RUN, NOT ASSUMED, AND ITS FIRST RE-RUN CAUGHT ITS OWN
      OMISSION.** The sweep's first pass keyed on the phrase *"as a leaf"* and so
      missed requirement 4's retraction, whose sentence reads *"recorded and
      anchored forward"* — the leaf named in the heading and not in the clause.
      **A method that finds its own first miss on re-application is the method
      working**; a list that had merely been appended to would have carried the
      gap silently. Re-run against every leaf-mandating clause rather than every
      occurrence of one phrase, the table above is now complete at TWELVE
      mandated kinds plus one deliberate exclusion.

      **DONE — twelve kinds, settled inside tranche one's grammar and pinned by
      test.** `contracts/signed-execution-chain/transparency-log-leaf.schema.yaml`
      carries them in 5.3's own order, each paired to its own `anchor_event` shape
      by the file's `allOf` rather than by prose, and the deliberate exclusion is
      asserted as an absence with a name
      (`tests/signed_execution_chain/test_anchor_event_settlement.py`, which also
      holds three commissioned mutation proofs and a healthy control per kind).
      The one-pass equality against every leaf-mandating clause is what the module
      re-runs. No second grammar was minted, and the eleven digest subjects went
      into the single `digest_subject` enumeration on
      `digest-construction.schema.yaml`'s own written invitation.
- [ ] 5.4 Select the PERMISSIONED PLANE INSTANCE (D5), unless the council rules it
      should be fixed at ratification instead. The class is Fabric or Besu; the
      instance is not an anchor chain and selecting one re-opens nothing Q3 closed.
- [ ] 5.5 Fix the LINKAGE-DERIVATION CONSTRUCTION — the per-analysis parameter,
      the expiry and revocation surface, and how the identity plane binds an
      issuance to its anchored consent checkpoint. Requirement 8 fixes the
      SHAPE and the refusals and deliberately not the construction; the
      domain overlay fixes the OCCASION and the standard.
- [x] 5.6 Fix the ANALYSIS-RESULT SHAPE — the CLOSED STATUS ENUMERATION and its
      members, the fields a correlation-refused result carries (the NAMED omitted
      correlation and its refusal GROUND, itself a named enumeration — revocation
      state unreadable, consent revoked, derivation refused), and how the
      per-plane results are carried distinctly from correlated output. Settled
      ALONGSIDE 5.3's leaf kinds, since the same events produce both. Requirement
      8 fixes that the outcome is DECLARED, ENUMERATED and distinguishable and
      deliberately not its field names; without this settled before schemas are
      authored, "names the part it could not perform" has no shape a validator
      can check and a silent partial is indistinguishable from a complete run.

      **DONE — `contracts/chain-anchoring/analysis-result.schema.yaml`.** The
      status discriminator is CLOSED at three members — `complete`,
      `correlation_refused`, `correlation_not_requested` — so the three shapes are
      decidable apart by the result itself; a correlation-refused result carries
      the NAMED omitted correlation and its refusal GROUND from a named
      enumeration rather than free text; and the per-plane results are carried
      distinctly from correlated output. Four refusals hold it, each red-proven:
      `analysis_result_silently_partial`, `analysis_result_status_outside_enumeration`,
      `analysis_result_refusal_ground_free_text` and
      `analysis_result_labelled_deidentified`.

## 6. Successors and dependencies — NAMED, NOT DRAFTED

- [ ] 6.1 **Hard prerequisite: `add-signed-execution-chain` realized.** The
      transparency log is its tranche-one artifact; with no log there is nothing
      to anchor and no leaves to write.
- [ ] 6.2 **Hard prerequisite: the PKI plane** (`implement-openxpki-install-repo`).
      The topic's exit path names it as what holds this tranche.
- [ ] 6.3 **Sequencing, not blocking: `add-chain-attestation`** (tranche two, in
      flight). Anchoring a log of unattested leaves witnesses less than the family
      intends.
- [ ] 6.4 **Domain overlays are NOT authored here** — MedxChain/HealthLinc in
      MedxFactory, LedgerLinc in LedgerxFactory, each pinning this family by
      commit and per-file digest. Requirement 9 is what keeps their content out.
- [ ] 6.5 **The openXwallet successor field** tranche one named remains
      tranche one's to raise; this packet neither closes it nor waits on it.
