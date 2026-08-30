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

- [x] 1.1 `chain-anchoring` — **NINE ADDED requirements over 77 SCENARIOS** (52
      SCENARIOS at the head the council judged, `cf5a24b8`; the 2026-08-30 fix
      round of §2.4 and its SIX bot rounds added TWENTY-FIVE SCENARIOS and NO NEW
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

      SHOULD-FIX items (LA-A7, LS-A7/A8/A9, LQ-A10/A11/A12/A14, CPL-A5) are
      **UNDISPOSED by the ruling and stay open** — disposition §6 says so
      expressly, and no silence here rules them.

      **§1.4 AND §1.5 RE-RUN, AND THE RESULT IS REPORTED RATHER THAN ROUNDED.**
      §1.4: `--strict` green and `--all --strict` **79 passed / 0 failed**;
      NINE requirements unchanged, **52 → 77 scenarios**, still no `## MODIFIED`
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

## 3. Ratification gate — Brett Heap's act, AFTER the review — THIS IS NEXT

**The review is behind this line and the ratification is in front of it.** The
2026-08-30 disposition authorized fix rounds and **ratifies nothing**: *"It
ratifies nothing, merges nothing, and moves no contract byte"* (§6). §2 is now
discharged, so 3.1 is the next act on this packet.

- [ ] 3.1 Brett Heap ratifies or declines, having read the council record
      (`review/council-review-2026-08-30.md`), the disposition
      (`review/disposition-2026-08-30.md`) and this fix round.
      Ratification would authorize REALIZATION and would perform none of it.
- [ ] 3.2 On ratification: `target_release` is CONFIRMED against
      `contracts/manifest.yaml` at that tip rather than at this one, and remains
      allocated by merge order — `add-signed-execution-chain` and
      `add-chain-attestation` reach the same additive cut.
- [ ] 3.3 On ratification: front-matter gains `Status: ratified` plus the
      `Ratified:` line naming the record path, and the README record line is
      updated to match.

## 4. Realization — the contract family and its validator

- [ ] 4.1 `contracts/chain-anchoring/` — the multi-anchor receipt record (four
      per-chain elements, the declared header source, and the MINT-TIME CONFIGURATION
      BLOCK — the configured witness set, each witness's declared horizon, and
      the submission time they run from — which the ANCHORED DIGEST commits to in
      every representation, the material digest staying nameable beside it), the
      log-checkpoint anchor record with its never-read-as-validation disclaimer,
      the anchor-bound commitment record (declared construction, SALT and KEY
      custody references, declared salt source and width), the anchor-state
      record (per-witness, with declared horizons and NO aggregate boolean), the
      consent-checkpoint commitment record, the plane-separation declaration,
      and the AUTHORIZED LINKAGE DERIVATION record (issuing plane, anchored
      consent checkpoint, per-analysis parameter, expiry and revocation, and
      the leaves issuance and use write), and the ANALYSIS RESULT record with
      its OUTCOME DISCRIMINATOR.
- [ ] 4.2 Packaged POSITIVE and NEGATIVE examples for every named refusal — a
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
      pre-issued derivation whose revocation state cannot be read**; **an analysis
      result missing its correlation with no declared outcome**; a
      domain record kind; an overlay relaxing a neutral refusal. The bolded
      entries are the refusals the 2026-08-30 fix round added.
- [ ] 4.3 `scripts/validate-chain-anchoring.py` — the canonical refusing
      validator. The payload refusal is STRUCTURAL (D3); the unsalted-commitment
      refusal is by DECLARED CONSTRUCTION plus salt-custody resolution, KEY-
      custody resolution, and the declared salt source and width against the
      floor (D4, as amended by LS-A6).
- [ ] 4.4 **The declared residual of D4 is discharged or DECLARED**: establish
      that the commitment path is the ONLY path that can mint an anchor-bound
      value, so an undeclared construction is unreachable; a realization that
      cannot establish it declares the shortfall on `add-trust-anchor`'s
      declared-shortfall pattern rather than asserting the property.
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
- [ ] 4.8 **Corroborating-only status is ENFORCED, not stated** — Q3's third
      condition. A claim standing on the operational witness alone is refused by
      a check, and a ten-year claim cites the durability witness.
- [ ] 4.9 **[OPERATOR] The durability witness's aggregation path** — public
      calendars or a self-run hourly calendar (study §8: $0 marginal per item, or
      ≈$2.1k/yr self-run). Evidence is a completed upgrade on a real item.
- [ ] 4.10 The BOTH-WITNESSES rule is exercised end to end, including its
      degraded paths: an item with each witness missing in turn reaches
      `anchor_incomplete` naming that witness, a horizon breach writes its leaf,
      and the durability-calendar recovery UPGRADES THE PENDING DURABILITY PROOF
      and appends its entry rather than re-anchoring.
- [ ] 4.11 Registration in `contracts/manifest.yaml` and `contracts/CHANGELOG.md`
      at the additive bundle cut, with `target_release` confirmed against the
      manifest at that tip.

## 5. Settle before schemas are authored

- [ ] 5.1 Fix the ANCHORED-ITEM UNIT — what exactly is anchored: a transparency-log
      checkpoint, a state root, or both, and at what granularity the aggregation
      batches. Requirement 1 fixes the receipt SHAPE and deliberately not the unit.
- [ ] 5.2 Fix the COMPLETION HORIZONS — the declared values per witness, bounded
      by the aggregation interval chosen in 5.1. Requirement 3 requires that they
      be DECLARED; it names no numbers.
- [ ] 5.3 Fix the NEW LEAF KINDS against tranche one's leaf grammar. This packet
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
      * `verification` and `verification-failure` (requirement 7)
      * `permitted-access` and `refused-access` (requirement 7)
      * `linkage-derivation-issuance` and `linkage-derivation-use` (requirement 8)
      NOT here, and each for a stated reason: the VALIDATION-FAILURE leaf of
      requirement 4 is a GATE VERDICT, which tranche one's ratified leaf set
      already carries, so settling it here would mint the second grammar this
      task forbids.
- [ ] 5.4 Select the PERMISSIONED PLANE INSTANCE (D5), unless the council rules it
      should be fixed at ratification instead. The class is Fabric or Besu; the
      instance is not an anchor chain and selecting one re-opens nothing Q3 closed.
- [ ] 5.5 Fix the LINKAGE-DERIVATION CONSTRUCTION — the per-analysis parameter,
      the expiry and revocation surface, and how the identity plane binds an
      issuance to its anchored consent checkpoint. Requirement 8 fixes the
      SHAPE and the refusals and deliberately not the construction; the
      domain overlay fixes the OCCASION and the standard.
- [ ] 5.6 Fix the ANALYSIS-RESULT SHAPE — the CLOSED STATUS ENUMERATION and its
      members, the fields a correlation-refused result carries (the NAMED omitted
      correlation and its refusal GROUND, itself a named enumeration — revocation
      state unreadable, consent revoked, derivation refused), and how the
      per-plane results are carried distinctly from correlated output. Settled
      ALONGSIDE 5.3's leaf kinds, since the same events produce both. Requirement
      8 fixes that the outcome is DECLARED, ENUMERATED and distinguishable and
      deliberately not its field names; without this settled before schemas are
      authored, "names the part it could not perform" has no shape a validator
      can check and a silent partial is indistinguishable from a complete run.

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
