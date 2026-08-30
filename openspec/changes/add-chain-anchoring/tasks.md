# Tasks: add-chain-anchoring (tranche three)

Governance-level and dependency-ordered. **This change is a DRAFT and is NOT
being implemented now.** §1 is authored in this pull request; **§2 is the §7.4
council review and §3 is Brett Heap's ratification act, and BOTH ARE OPEN**; §4
onward are for the implementer and belong to Speckit contract features. Do not
duplicate the executable contract list here — §6 hands off the successors.

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

- [x] 1.1 `chain-anchoring` — **NINE ADDED requirements over 52 scenarios**, in
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
      to a vendored source (D7), plus realization dependencies and what the
      design does NOT decide.
- [x] 1.4 `OPENSPEC_TELEMETRY=0 openspec validate add-chain-anchoring --strict`
      green and `--all --strict` green before commit; counts recorded in the
      pull-request body.
- [x] 1.5 doc-health zero-new against `origin/main`, baseline worktree basename
      matching the working clone's (issue #342 — a mismatched-identity
      `--previous-report` manufactures phantom regressions).
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

## 2. §7.4 COUNCIL REVIEW — OPEN, and it precedes ratification

- [ ] 2.1 Convene a §7.4-shaped council on this packet, **OUTSIDE the clearance
      pipeline**. The ground is measured and code-level: a class over
      `openspec/changes/**` can never commission a council — 984 admitted paths,
      984 floored, 0 remaining on this repository's real tree — so the review
      reaches this repository on the council-reviewed-but-human-approved path,
      which needs no class and no flip (2026-08-28 `gate_rules_council` convening
      record, unanimous 5/5).
- [ ] 2.2 Put the six AUTHORING DECISIONS to the seats explicitly (proposal
      § Authoring decisions put to the council): **D-A** the missing-witness
      semantics, **D-B** the structural payload refusal, **D-C** the
      declared-construction commitment refusal and its declared residual, **D-D**
      the change id and capability name, **D-E** deferring the permissioned-ledger
      selection to realization, **D-F** the per-plane key correction to a vendored
      source. D-A is the largest and should be read first.
- [ ] 2.3 Record the sitting in `review/`, on `add-binding-consumer-identity`'s
      pattern: seats, verdicts, blocking amendments, and the convener disposition.
      The directory is CREATED WITH THAT RECORD — this packet ships no empty
      `review/`, because an empty one would assert a sitting that has not
      happened.
- [ ] 2.4 Execute the amendment round the sitting returns, and re-run §1.4 and
      §1.5 against the amended text.

## 3. Ratification gate — Brett Heap's act, AFTER the review

- [ ] 3.1 Brett Heap ratifies or declines, having read the council record.
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
      per-chain elements plus the declared header source), the log-checkpoint
      anchor record with its never-read-as-validation disclaimer, the
      anchor-bound commitment record, the anchor-state record (per-witness, with
      declared horizons and NO aggregate boolean), the consent-checkpoint
      commitment record, and the plane-separation declaration.
- [ ] 4.2 Packaged POSITIVE and NEGATIVE examples for every named refusal — a
      receipt missing inclusion proof; a receipt missing transaction bytes; a
      receipt missing chain-acceptance evidence; a receipt whose header is
      non-canonical; a verification run against a minter-supplied header source;
      a checkpoint inclusion presented as validation; a
      single-witness item presented as anchored; a per-item selectivity rule; a
      third anchor target; a content-bearing field; ciphertext; an absent
      construction declaration; an honestly-declared plain digest; a salt custody
      reference resolving onto a chain; a per-subject consent row offered for
      anchoring; an attempt row offered for direct anchoring; a
      direct identifier in the demographic plane; a shared cross-plane key; a
      domain record kind; an overlay relaxing a neutral refusal.
- [ ] 4.3 `scripts/validate-chain-anchoring.py` — the canonical refusing
      validator. The payload refusal is STRUCTURAL (D3); the unsalted-commitment
      refusal is by DECLARED CONSTRUCTION plus salt-custody resolution (D4).
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
- [ ] 5.3 Fix the NEW LEAF KINDS against tranche one's leaf grammar — verification,
      verification failure, refused access, anchor-pending, horizon breach, anchor
      completion. This packet adds no second grammar and must not.
- [ ] 5.4 Select the PERMISSIONED PLANE INSTANCE (D5), unless the council rules it
      should be fixed at ratification instead. The class is Fabric or Besu; the
      instance is not an anchor chain and selecting one re-opens nothing Q3 closed.

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
