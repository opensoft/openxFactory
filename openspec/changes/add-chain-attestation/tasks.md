# Tasks: add-chain-attestation (tranche two)

Governance-level and dependency-ordered. **This change is a DRAFT.** §1 is the
pull request. **§2 (the §7.4 council review) and §3 (Brett Heap's ratification)
are the two gates that stand between it and any realization, in that order.**
**§2 IS HELD AND DISCHARGED — the sitting of 2026-08-30, its thirteen blocking
amendments, and the eighteen bot rounds that followed. §3 IS TAKEN — RATIFIED BY
BRETT HEAP ON 2026-09-01 at `f54cb5bc` and RE-RATIFIED at `6d7ef17b` after the
amendments that head's own verdict forced.** Both gates are now behind this packet; what remains is
§5's realization, gated on machinery that does not yet exist. §4 settles what must not reach schema authoring open; §5 is
the realization commission and is gated on machinery that does not yet exist.

Evidence convention, unchanged from the family's standard: a box closes on a FACT
that survives the session — a merged commit, a green run named by id, a live API
read, a file path — never on an intention and never on a workflow file standing
in for a ruleset state.

## 1. Spec deltas and the packet (THIS PULL REQUEST)

- [x] 1.1 `signed-execution-chain` — **NINE ADDED requirements over 108
      scenarios**: the harness-controller setup attestation under a certificate
      expressed in `add-trust-anchor` vocabulary, with the issuing authority named
      as a realization dependency and never assumed; runner attestations signed AT
      the controller by remote signing it serves, with the signing REQUEST recorded
      beside the signature and signer identity refused the persona population per
      `add-identity-brokering`; the controller corroborating against its own link-4
      attestation rather than notarizing self-report, with a per-FACT evidence
      class and an unclassed fact refused; tier-2 keys that never enter a worker in
      EVERY configuration, on omnigent's `access_secrets: false`; the pull-request
      open as a signed, chain-bound decision whose absence is an orphan act; the
      SIGNED HASH-LINK RULE taking effect at link 4 with the gate's walk extended to
      links 1–6 and a completeness rule for plural predecessors; CLOSURE as the
      point a chain completes, with a merged-but-unclosed chain refusing everything
      downstream and firing the fraud signal; the remediation chain as the ONE
      admitted consumer, its exemption non-inheritable and its own closure owed; and
      the executing layer REFUSING to execute a step whose inbound chain does not
      verify.
- [x] 1.2 **TWO `## MODIFIED Requirements` — 2 requirements over 17 scenarios,
      each SCENARIO-COMPLETE.** The second, added in the eighteenth bot round,
      carries tranche one's RATIFICATION/CHAIN-INCEPTION requirement (all SIX of
      its scenarios verbatim, plus two for the lineage) and adds the three
      AMENDMENT-LINEAGE FIELDS closure's limbs read; `design.md` **D12** records
      why extending tranche one is lawful — it is ratified-NOT-realized, so no
      contract byte exists to break — and why an eighth record kind of our own was
      ruled against. The first carries tranche one's gate
      requirement *"A gate validates the short chain as a hash-linked chain"*
      **SCENARIO-COMPLETE AT ALL NINE OF ITS SCENARIOS** — added in the 2026-08-30
      council fix round, replacing this packet's ADDED-only draft. Substantively it
      changes the gate's SCOPE SENTENCE, re-conditions the `a tranche-two link does
      not exist yet` scenario on a link no ratified tranche has yet put in force,
      and extends the closed-list mapping table from nine rows to all EIGHTEEN of
      this capability's requirements; everything else is verbatim. No OTHER promoted
      or sibling requirement is restated. Composition with `add-trust-anchor`,
      `add-identity-brokering`, `implement-openxpki-install-repo`,
      `contracts/omnigent/` and tranche one's remaining eight requirements is BY
      REFERENCE. `design.md` D3 records why the ADDED-only reading was WRONG and how
      the construction proved it.
- [x] 1.3 `design.md` records the real decisions — Q7 as the ruled mechanism and
      what it does NOT settle; corroborate-versus-notarize with the per-FACT
      evidence class, its declared ORDER and its composition with the ratified
      chain-custody registry (D2); the MODIFIED gate restatement and the ADDED-only
      reading it replaces (D3); the plural-predecessor
      enumeration that fills a gap in the topic; the HSM as deferred hardening; the
      revocation horizon as this packet's own decision; Q4's re-derivation
      instruction routed to the council AND the raising-time re-derivation performed
      against it (D7, D7a); the deferral table; and the five open
      design points that must not reach schema authoring open.
- [x] 1.4 `OPENSPEC_TELEMETRY=0 openspec validate add-chain-attestation --strict`
      green and `--all --strict` green before commit; counts recorded in the pull
      request body.
- [x] 1.5 doc-health zero-new against `origin/main`, baseline worktree basename
      matching the working clone's (issue #342 — a mismatched-identity
      `--previous-report` manufactures phantom regressions). **ZERO-NEW OVERALL,
      AS OF BRETT HEAP'S RULING 4a OF 2026-08-30 — not zero-new-for-authored-bytes
      with a known exception, but zero-new full stop.** The history is kept,
      because the collision and its resolution are both worth reading. Filing
      `review/` produced **FIVE new `status-validity` errors**, one per direct
      child of `review/` — ballot, packet, record, disposition and the #509
      summary — because each carries `Status: record — <elaboration>` where the
      family requires a bare taxonomy value. The four seat returns are unaffected:
      `LIFECYCLE_SCAN`'s glob is `openspec/changes/**/review/*.md` and they sit one
      level deeper. **THIS IS THE COLLISION AND IT IS NOT THIS PACKET'S TO
      RESOLVE:** the sitting artifacts are byte-exact evidence frozen by the
      disposition's own §3.7 (*"THE PACKET IS NOT EDITED … The ballot is likewise
      unedited"*), and the doc-health capability already rules that *"the scan set
      SHALL NOT reach a document that is byte-exact evidence rather than live
      prose … a frozen record reported for the state it preserves is a false
      finding"* — but it implements that exclusion by PATH SEGMENT
      (`supporting-docs` / `source-snapshots` / `evidence`), none of which these
      paths carry. **Editing the artifacts would falsify the record; widening or
      narrowing the scan set is expressly A GOVERNED CHANGE** (`openspec/specs/
      doc-health/spec.md`, same requirement). The five findings were therefore
      reported as a KNOWN, EXPLAINED DELTA for the convener rather than improvised
      away.

      **HE RULED IT, AND THE THIRD DOOR WAS HIS TO OPEN — RULING 4a, 2026-08-30.**
      Neither of the two doors this packet could reach was lawful: editing the
      artifacts would have falsified the record the disposition freezes at §3.7,
      and widening the scan set is expressly a governed change. **The record's
      OWNER normalizing his own header is neither**, and it is an act only he can
      take. The transformation is deterministic, so that both bundles' twin
      disposition files stay BYTE-IDENTICAL as the disposition itself asserts: in
      each file whose header line matches `Status: record — <elaboration>`, that
      single line becomes `Status: record` followed by
      `Record scope: <elaboration verbatim>`. **Nothing else in any file changed** —
      five files, one line each, every elaboration preserved verbatim, both
      preserved convening errors and every mis-measured figure untouched. The four
      seat returns needed no change (`LIFECYCLE_SCAN` is `review/*.md`; they sit one
      level deeper). **doc-health now reports ZERO NEW FINDINGS against
      `origin/main` with the matched baseline basename**, and the five
      `status-validity` errors are gone.
- [x] 1.6 README "OpenSpec Records" active block updated, newest first.
- [x] 1.7 `ideation/staging/INDEX.md` — the topic's detail section records that
      EXIT 2 has been raised as an active change. The row is NOT marked
      `Exit taken:`, on the same ground tranche one recorded: that record silences
      the `staged-candidate-aging` family only when it names an ARCHIVED change, and
      the topic must keep ageing while tranche three is unraised.
- [x] 1.8 **THE THREE PULLS BETWEEN A RULED INPUT AND AN ARTIFACT ARE RECORDED,
      NOT SMOOTHED**, per the family's contested-finding rule, and **two of the
      three are now DISCHARGED BY THE 2026-08-30 SITTING RATHER THAN CARRIED**:
      Q4's re-derivation instruction versus drafting this tranche now — **RULED NOT
      PREMATURE BUT NARROWED**, with the raising-time re-derivation performed at
      `design.md` D7a; tranche one's gate scope note versus the extended walk —
      **RESOLVED AGAINST THIS PACKET'S FIRST READING**, the self-limiting reading
      shown by construction to leave a contradicting scenario standing in canon and
      replaced by the MODIFIED restatement at 1.2; and the topic's SINGULAR
      hash-link rule versus its PLURAL link 5 (resolved here by addition, flagged as
      this packet's own resolution, and hardened in the fix round by the leaf-order
      obligation LQ-A3 required).
- [x] 1.9 **THE FIRST BOT ROUND'S THREE P1 FINDINGS ARE CLOSED, AND RECORDED AS
      CORRECTIONS** (`design.md` D10; `proposal.md` § "What the first bot round
      corrected"). All three were one shape — a record that NAMED something
      standing where a record that ESTABLISHES it belonged: the signing request
      recorded but not ATTRIBUTED to the provisioned task (with `design.md` D1
      having claimed otherwise); "a proper subset" with no authoritative set to be
      a subset OF, so a lane could omit a link-5 record before presenting link 6;
      and closure bound to the review record's BYTES rather than its AUTHORITY, so
      a fabricated review record could close a chain. Each repair uses an existing
      instrument — attribution stated as what must be ESTABLISHED, the complete
      set derived AT THAT ROUND from tranche one's log by a defined query, and
      review authority in `add-wallet-carried-review-authority`'s shipped
      vocabulary — and each carries its residual DECLARED rather than closed.
      **THE SECOND REPAIR DID NOT HOLD AND WAS REPLACED AT 1.10** — a log query
      cannot see a leaf that was never written — so the authoritative set is now
      LINK 4's COMMITTED EXPECTATION, with the log comparison secondary. This box
      records what round one did and is not a statement of the rule in force.
- [x] 1.10 **THE SECOND BOT ROUND'S TWO P1 FINDINGS ARE CLOSED, AND RECORDED AS
      CORRECTIONS** (`design.md` D11; `proposal.md` § "What the SECOND bot round
      corrected"). Both were one shape, and a DIFFERENT shape from the first
      round's: **a rule that could not be CONSTRUCTED as written.** (i) The
      completeness rule derived its authoritative set FROM THE LOG, which cannot
      see a leaf that was never written — so a lane that never wrote an unwanted
      attestation passed the gate, and the council's own LQ-A3 leaf-ordering
      obligation could only refuse the leaf once it appeared, after a merge that
      is not retroactively refused. **The authority moves to link 4's COMMITTED
      EXPECTATION**, extensible before each attestation it covers, with the log
      comparison kept as a second check in both directions — which also
      discharges `lead-security`'s **LS-F5**, that named the identical missing
      instrument in the sitting. (ii) Requirement 2 bounded the per-task tier-2
      identity to *"exactly one thing — signing an attestation about that task"*
      while requirements 5 and 7 required it to sign a DECISION and a TEST
      OUTCOME, so **no conforming link 6 was constructible**. Repaired by a
      CLOSED, NAMED ENUMERATION of authorized record kinds (links 5, 6, 10), with
      authority records excluded permanently. Neither repair invents vocabulary.
- [x] 1.11 **THE THIRD BOT ROUND'S TWO P1 FINDINGS ARE CLOSED, AND RECORDED AS
      CORRECTIONS** (`design.md` D11a; `proposal.md` § "What the THIRD bot round
      corrected"). (i) The record-kind enumeration fixed FORM and left SUBJECT
      unfixed: link 6 is ONE decision committing to EVERY link-5 attestation and
      link 10 ONE test outcome over the same whole, so a task-scoped signer still
      could not produce either **once a chain fans out past one task** — the
      ordinary case had no conforming link 6 through two successive repairs.
      **TIER 2 NOW SPLITS BY SUBJECT SCOPE**: one chain-scoped identity per chain
      for the aggregate records, per-task identities shrunk to link 5, both under
      one custody rule, authority records outside both enumerations forever.
      Composing N task-scoped decisions was REFUSED on the topic's authoritative
      link table, which gives link 6 one signed decision. **This DEPARTS from the
      topic's signer column for links 6 and 10 and is flagged as such**, on D4's
      footing; tranche one's ratified text defers tier 2's definition to this
      tranche and imposes only EPHEMERAL and keys-never-in-a-worker, both of which
      bind the new scope. **No seat return is touched** — every custody passage in
      the four returns is key-material, and none makes an identity-cardinality
      claim. (ii) The MODIFIED block's enforcement mapping still said
      *"log-derived authoritative set"*, contradicting the corrected rule; it now
      names link 4's committed expectation as THE AUTHORITY with the bidirectional
      log comparison SECONDARY. **A packet-wide NEW-CONJUNCT SWEEP** over every
      authority-of-the-set phrase and every predicate-shaped sentence about what
      the gate compares found four further sites in the superseded present tense,
      all corrected, with round-one narratives kept as history and marked
      superseded.
- [x] 1.12 **THE FOURTH BOT ROUND'S P1 AND P2 ARE CLOSED, AND RECORDED AS
      CORRECTIONS** (`design.md` D11b; `proposal.md` § "What the FOURTH bot round
      corrected"). (i) **P1 — bind-before-sign's last uncovered limb.** Every other
      link had moved its CLAIMS to the controller; link 10 had left its RESULT with
      the lane, so a fabricated passing outcome on an otherwise valid chain drew a
      controller signature and CLOSED THE CHAIN. Link 10 now binds, inside the
      signed bytes, an AUTHENTICATED EXECUTION the controller dispatched or
      observed, the EXACT TESTED REVISION equal to the merge commit closed over,
      and the RESULT; a lane-claimed outcome is REFUSED as closure grounds. **NO
      DECLARED-SHORTFALL PATH EXISTS FOR THE OUTCOME** — the first live application
      of LS-A10's floor, stated in the requirement and cited to it. Recorded
      outcomes go THREE → FOUR with UNESTABLISHED, added deliberately because it is
      a different fact from FAILED. **Checked and clean**: it composes with the
      two-horizon doctrine (nothing reaches back through the merge; the closure is
      what is refused), and no seat return blesses a lane-claimed outcome —
      `lead-security`'s B-4 endorsement is of the revocation horizon, a different
      limb. (ii) **P2 — a stale FIXTURE**, one field over from the third round's
      sweep: 5.5 still commissioned a per-task identity signing links 6 and 10,
      which the closed enumeration makes impossible and explicitly refuses.
      Withdrawn, named as withdrawn, replaced by the chain-scoped positive case.
      **The earlier sweep covered PREDICATES and not FIXTURES** — a superseded rule
      survives in the examples commissioned against it, not only in the sentences
      asserting it.
- [x] 1.13 **THE FIFTH BOT ROUND'S P1 AND P2 ARE CLOSED, AND RECORDED AS
      CORRECTIONS** (`design.md` D11c). **BOTH ARE RESIDUE OF THE THIRD ROUND'S
      OWN REPAIR.** (i) **P1 — the subject split created a signer the attribution
      mechanism did not reach.** The round-one attribution is TASK-SCOPED by
      construction, so it reached none of the chain-scoped identity's requests: an
      opportunistic caller could obtain a chain-scoped link-6 signature nobody was
      established as entitled to ask for. Discharged by EXTENDING the same
      mechanism — the chain-scoped request is RECORDED, ATTRIBUTED to the party
      the chain's own INCEPTION RECORD BINDS, refused from any other, and covered
      inside the signed bytes. **No authority is minted**: the requester set is
      DERIVED from tranche one's actor-binding requirement, which the gate already
      walks. (ii) **P2 — the MODIFIED block's leading operative SHALL still said
      "validates links 1–3"**, with the generic missing-link scenario likewise, so
      canon would have carried two conformance readings and an implementation
      could have kept the short-chain gate while satisfying the leading clause —
      **the defect class LA-A1 exists to close, surviving inside LA-A1's own
      repair.** Fixed, and the ENTIRE MODIFIED BLOCK was then re-read AS A SET,
      which found three further residues (the closed-list clause's "EXACTLY these
      checks"; "at this tranche" as a link-range fact; the completeness sentence's
      unstated bound). **THE STALENESS SWEEP** ran the two fields across the
      packet and its consumers: README.md, `ideation/staging/INDEX.md`,
      `.openspec.yaml`'s `approved_by` and `proposal.md`'s header all asserted
      PRE-COUNCIL state (59 scenarios, "no MODIFIED block", `hardware_attested`,
      "neither has happened") and now state it accurately — **council review HELD
      2026-08-30, ratification PENDING**; §4's ordering is corrected (4.6 before
      4.7) and 4.1 now covers both subject scopes.
- [x] 1.14 **THE SIXTH BOT ROUND'S TWO P2s ARE CLOSED — both bookkeeping lag,
      and each closed its family by running the check one level up.** (i) The
      `proposal.md` front-matter ORIGIN block still said *"`tasks.md` §2 and §3 are
      the two gates that stand between it and realization"* — the SECOND missed
      announcement site after the PR body. It now records §2 discharged by the
      2026-08-30 sitting and names **§3 as the SOLE REMAINING GATE**. **THE
      ANNOUNCEMENT-FAMILY SWEEP then ran over EVERY file in the change directory**
      for gate-count and process-state phrasing (*"two gates"*, *"two acts"*,
      *"must follow"*, *"remaining gate"*, *"neither has"*, *"both gates"*,
      *"stand(s) between"*): six sites, and the origin block was **the family's
      last member** — the other five already state the acts as a pair and then
      mark their state, and one is a historical quotation inside 1.13's own sweep
      record. **THE FAMILY IS CLOSED.** (ii) Task 5.5 never commissioned the fifth
      round's chain-scoped request scenarios, so 5.6 — one named refusal per
      example here — could have shipped a validator with **no test for the
      authentication path**, and the positive closure fixture could have omitted
      the attributed link-10 request. All three added, plus the note that the
      positive closure fixture carries its attributed request. **THE
      FIXTURE-EQUALITY CHECK then ran the one-pass method over the ADDED
      scenarios** — every scenario naming a validator-observable behaviour against
      the 5.5 commission — and **found five more that had been named in the delta
      since the first draft and never commissioned**: a persona proposed for a
      runner; a payload the controller provisioned nothing for; a one-task
      lifetime offered as making a key non-secret; **valid artifacts from
      DIFFERENT EXECUTIONS submitted together** — the mix-and-match refusal this
      family exists for, and the most conspicuous omission; and the remediation
      POSITIVE admission. All five commissioned. Three scenarios are
      DELIBERATELY uncommissioned and say so: two are the reader-correction shape
      **LQ-A8** (undisposed SHOULD-FIX) asks be rewritten, whose THEN no check can
      run, and one asserts conformance INVARIANCE rather than a named refusal.
- [x] 1.15 **THE SEVENTH BOT ROUND'S THREE P1s AND ONE P2 ARE CLOSED** — and
      **TWO OF THE THREE P1s WERE DEFECTS THIS PACKET'S OWN EARLIER ROUNDS
      INTRODUCED**, which is the argument for the round rather than against the
      packet. (i) **A FAILING POST-MERGE TEST CLOSED THE CHAIN.** Round four's
      closure conjuncts required the result be ESTABLISHED and never PASSING, so a
      genuine, honestly-reported, correctly signed FAILURE satisfied every
      conjunct and the normative THEN closed the chain — contradicting this same
      requirement's rule that a FAILED link 10 is a refusing state, and permitting
      promotion and release over work its own governed test called broken.
      Closure now requires an established **PASSING** result; an established
      FAILING one refuses and routes to remediation. **A GUARD WALK then asked of
      EVERY permitting conjunct set "what input makes this pass wrongly?" and
      found FOUR MORE**: the link-6 positive admitted an unbound caller's
      signature; both HSM positives admitted hardware custody REACHABLE from the
      runner's scope; and the remediation positive admitted a chain with no links
      1–6. All five tightened. (ii) **THE EXTENSION DEADLINE REOPENED THE
      DROPPED-ATTESTATION ATTACK.** "Before the attestation it covers is produced"
      let the controller commit AFTER observing execution, and let a realization
      minting extensions on signing-request arrival never commit a task whose
      attestation the runner SUPPRESSED. The deadline is now **DISPATCH** — at or
      before, never later — which is the last moment before the runner can
      influence anything. (iii) **LINK 10 HAD NO CONSTRUCTIBLE PREDECESSOR**: the
      table makes it link 9, a refusing STATE with no record kind, with links 7–9
      outside this code surface. The predecessor of a signed link is now **the
      nearest prior link possessing a RECORD KIND IN FORCE** — at this tranche
      4 → 5 → 6 → 10 — written so a later tranche adding record kinds EXTENDS the
      order without contradicting it, with 7, 8 and 9's roles named explicitly.
      (iv) **P2 — the review-authority fixtures**: the fabricated review record and
      the revoked-before-exercise authority were named refusals that 5.5 never
      commissioned, so 5.6 could have shipped without testing the check that stops
      a fabricated or revoked review record closing a chain. Both added.
      **AND THE 79/79 EQUALITY FIGURE THIS PACKET REPORTED WAS WRONG** — it was
      **77/79**, and the checker over-reported because keyword overlap against a
      long commission block is a weak test. Corrected on the record where the
      claim was made rather than silently.
- [x] 1.16 **THE EIGHTH BOT ROUND'S FOUR P1s AND ITS BOOKKEEPING SET ARE
      CLOSED**, and the round was reached by the POSITIVE-VERDICT RULE working:
      Codex reviewed `a9db0fe8` and the review was NOT CLEAN, which is why no
      ratification was written against it. (i) **THE ARC'S DEEPEST FINDING — a
      lane could FORGE A TIER-2 IDENTITY.** Nothing defined controller-signed
      ISSUANCE EVIDENCE, so a lane could mint a keypair, label it with the
      expected scope, and forge BOTH the record and its request attribution under
      that untrusted key — every attribution rule in this capability satisfied by
      the forgery, because they check the record against the key and never the key
      against an issuer. **The staged topic already required the fix**
      (`:137-139`, `:461` — tier 2 issued under the controller's certificate, in
      `trust-anchor` SHAPES and no parallel vocabulary), so this was a gap against
      the ruled source. Every tier-2 identity of BOTH scopes now carries
      controller-signed issuance evidence binding {public key, subject scope,
      closed record-kind enumeration, chain identity, validity bounds}; **every
      verification verifies issuance FIRST**; a signature with no issuance is a
      FORGED IDENTITY refused with fraud-signal force; and the gate's continuity
      walk includes issuance per link. Rounds five and seven's attribution
      scenarios were re-walked and now rest on established issuance. (ii)
      **REVIEW-RECORD REPLAY**: a genuine, authority-proven review record from
      ANOTHER PROPOSAL closed this chain, because link 10 referenced proposal and
      review independently and the authority exercise bound only to the review
      record. The consumed record was made to NAME THIS CHAIN'S IDENTITY — **a
      rule SUPERSEDED TWICE SINCE and recorded here as what round eight did, not
      as the rule in force**: round fourteen (1.23) found it unsatisfiable, since
      the review predates the chain identity, and round fifteen (1.24) replaced
      its equality bridge with the AMENDMENT LINEAGE. (iii) and
      (iv) **TWO COLLISIONS BETWEEN ROUND SEVEN'S OWN FIXES**: the dispatch-
      deadline fix made commitment extensions load-bearing while the
      predecessor-order fix enumerated an order that OMITTED them — extensions now
      sit in the order by its own general rule (4 → x₁ → … → xₙ → 5 → 6 → 10); and
      the guard walk's own tightening of the closure positive added ATTRIBUTED
      while omitting RECORDED and INSIDE-THE-SIGNED-BYTES. **THE GUARD RE-WALK
      THEN RAN OVER ALL SEVEN PERMITTING CONJUNCT SETS INCLUDING THE ONES THE LAST
      WALK TOUCHED, AND FOUND TWO MORE** — an identity whose validity bounds were
      merely PRESENT rather than MET, and the link-6 positive still missing
      inside-the-signed-bytes and issuance. **The walk's own lesson, now proven on
      itself: the fix's conjunct set is also a conjunct set.** (v) **BOOKKEEPING**:
      the 85 → 94 total is synced at README, `INDEX.md`, `proposal.md` and here;
      `proposal.md`'s Impact said five record kinds where `code_surface` enumerates
      them. **THIS ENTRY ORIGINALLY CLAIMED "both now read SEVEN" AND THAT CLAIM
      WAS FALSE** — the Impact bullet was corrected and `code_surface`'s leading
      number was left at SIX while its own sentence enumerated seven, which the
      ninth round caught (`3893609589`). **A CLAIMED SYNC IS NOT A SYNC**, the
      same honesty the 77/79 correction owed: the fix was applied to one site and
      asserted of two. Both now read SEVEN — verified by ENUMERATING the record
      kinds rather than by restating the number. **COPILOT'S
      COUNT ADVICE WAS TAKEN IN REVERSE AND THE REASON IS RECORDED**: it asked that
      `tasks.md` be changed 89 → 85 to match the other sites; the count was
      MEASURED at 89 then and the other sites were the stale ones, which is what
      Codex's P2 independently found. **A majority of stale sites is not a
      measurement.**
- [x] 1.17 **ONE FINDING IS DECLINED, AND THE GROUND IS THE DISPOSITION'S OWN.**
      Copilot reports that `review/seat-returns-2026-08-30/README.md:63` says
      *"Sixteen blocking amendments"* where its own breakdown sums to SEVENTEEN
      (11 + 3 + 3). **The arithmetic error is real. It is NOT THIS PACKET'S TO
      CORRECT.** That file is a FROZEN SITTING ARTIFACT (`Status: record (evidence
      appendix)`), and the disposition rules at §3.7 that the sitting's records are
      not edited: *"It is the evidence of what the seats actually read, and
      correcting it now would falsify that record"* — the same discipline that
      preserved the ballot's two convening errors rather than tidying them. It is
      recorded here as a PRESERVED ERROR, on the footing those two already have.
      **Only the record's owner can normalize it**, as Brett did for the header
      grammar under ruling 4a, and it is surfaced for that decision rather than
      taken silently.
- [x] 1.18 **THE NINTH BOT ROUND'S P1 AND P2 ARE CLOSED.** (i) **THE
      ISSUANCE-EVIDENCE REQUIREMENT WAS UNIMPLEMENTABLE AS WRITTEN.** Round eight
      asked for five bindings in *"issuance evidence expressed in
      `add-trust-anchor` vocabulary"*; **verified against the schemas, that record
      cannot exist**. `contracts/trust-anchor/issuance-evidence.schema.yaml` is
      `additionalProperties: false` at the root and at all four sub-objects and
      carries the ISSUANCE ACT (authority, establishment level, request
      provenance, issuing authority) — **zero** fields for subject scope, record-
      kind enumeration or chain identity. `certificate-record.schema.yaml` is
      likewise closed and holds the PUBLIC KEY (`subject.public_key_fingerprint`)
      and VALIDITY BOUNDS (`validity.not_before` / `not_after`) and none of the
      other three. An implementer could only have invented the parallel
      certificate-like record the requirement itself FORBIDS, or dropped the
      bindings and re-opened the forged-identity gap. **Repaired by COMPOSITION**:
      the canonical `certificate-record` (key + bounds) and canonical
      `issuance-evidence` (the issuance act), both CONSUMED UNMODIFIED, plus a
      record kind THIS CAPABILITY DEFINES — the **SIGNED CHAIN BINDING**, carrying
      subject scope, the closed record-kind enumeration and the chain identity,
      referencing the other two by `certificate_id` and `issuance_evidence_id`.
      Verification composes all three and the FORGED-IDENTITY refusal fires on ANY
      ONE MISSING. **The chain binding is not a certificate shape** — it asserts
      no key, no validity, no issuing authority and no trust, so the
      no-second-vocabulary rule survives intact — and it belongs to this
      capability's own code surface. All issuance scenarios re-walked onto the
      composition. (ii) **THE RECORD-KIND COUNT, ENUMERATED RATHER THAN CLAIMED**:
      `code_surface` read SIX while its own sentence enumerated seven. **The count
      is SEVEN and stays SEVEN after the composition** — the two trust-anchor
      shapes are CONSUMED, not defined here, so they add nothing to this
      capability's surface; the signed chain binding replaces the record round
      eight wrongly counted. Every site synced in this one commit, and 1.16's
      false "both now read SEVEN" is corrected above.
- [x] 1.19 **THE ELEVENTH BOT ROUND'S TWO P1s ARE CLOSED.** (i) **THE
      COMPOSITION CARRIED NO VERIFICATION KEY.** Verified against the schema:
      `certificate-record.schema.yaml`'s `subject` is
      `required: [identifier, subject_class]` with `additionalProperties: false`,
      and `public_key_fingerprint` is OPTIONAL — a FINGERPRINT, not a key — while
      `issuance-evidence` carries neither. So *"the signature verifies under the
      certified key"* was UNRUNNABLE from the three records, and with the
      fingerprint absent even an out-of-band key could not be bound. Closed
      WITHOUT MOVING A CANONICAL BYTE, on the estate's scope-restriction grain:
      (a) a tier-2 certificate record **SHALL** carry
      `subject.public_key_fingerprint` — this capability's CONSUMPTION
      requirement, on `add-wallet-carried-review-authority`'s S2 precedent where
      `issued_by` is optional in the canonical wallet shape and the register's
      reader refuses a record without it; and (b) every signed record THIS
      capability defines carries **the signer's public key beside its signature**,
      a discipline on our own record surface. **Resolution then runs**: compute
      the supplied key's fingerprint under the one digest construction, require
      EQUALITY with the certificate's, and only then verify the signature —
      mismatch or absent fingerprint being the FORGED-IDENTITY refusal.
      (ii) **A LAWFUL LATER DISPATCH COULD SATISFY NEITHER ORDERING RULE.** Fan-out
      may discover a task after an earlier task has attested; the extension owed
      at that dispatch had a nearest-prior of that link-5 record, which the
      special placement clause (*"the setup attestation, or the prior
      extension"*) forbade. **THE UNIVERSAL RULE NOW GOVERNS ALONE** — an
      extension descends from THE ACTUAL NEAREST PRIOR IN-FORCE SIGNED RECORD,
      whatever its kind — and `4 → x₁ → … → xₙ → 5 → 6 → 10` is demoted to **the
      NO-INTERLEAVING CASE**, not a rule. **The constraint that actually mattered
      is restated precisely**: an extension precedes the dispatch of THE TASKS IT
      COMMITS, never every attestation of the chain. The dispatch-deadline rule
      was already per-task and composes unchanged; the continuity scenario was
      rescoped. **The verifier caught a side effect of my own fix** — the
      rescoped scenario's antecedent read loosely enough to look like a chain
      presented with links missing, pushing the permitting count 3 → 4; tightened,
      and back to 3.
- [x] 1.20 **THE TWELFTH BOT ROUND'S P1 IS CLOSED — the round-eleven key rule was
      SCOPED PER TIER, and the scope was the defect.** It required
      `subject.public_key_fingerprint` of TIER-2 certificates only. Link 4 and the
      commitment extensions are signed under the **CONTROLLER** certificate, so a
      canonical controller certificate omitting its optional fingerprint left both
      **forgeable by exactly the supplied-key trick the tier-2 clause had
      closed**: the record supplies a key, the signature verifies under it, and no
      required equality check binds it to certified material. **THE RULE IS NOW
      WRITTEN ONCE OVER THE CAPABILITY'S CONSUMED-CERTIFICATE SET** — the
      controller certificate and the tier-2 certificates at both subject scopes —
      and placed in requirement 1, where certificates ENTER this capability, with
      requirement 2 CITING it rather than restating it, on the same
      place-it-once footing as the declared-shortfall floor. Both obligations and
      the RESOLVE-COMPARE-THEN-VERIFY order now bind every member, and **any
      certificate a later tranche adds to the set is covered on the day it is
      added**. **THIS IS THE ONE-RULE-NOT-SLOTS LESSON FOR THE SECOND TIME** — the
      predecessor order learned it when extensions were given a placement of their
      own, and the packet now says so in terms: *a rule that enumerates the slots
      it covers will be outrun by the next slot.* **THE CERTIFICATE-SITE SWEEP
      PROVES THERE IS NO THIRD SCOPE**: every `certificate` mention in the delta
      resolves to one of the three set members, or to a non-consumption mention —
      the CA as a realization dependency, revocation STANDING of the controller
      certificate, the custody registry's assurance axis, or the omnigent
      public-material statement — none of which verifies a signature against a
      key.
- [x] 1.21 **THE THIRTEENTH BOT ROUND'S TWO P2s ARE CLOSED, AND EACH LEAVES A
      STANDING RULE BEHIND IT.** (i) **THE SIGNER-PUBLIC-KEY DISCIPLINE WAS NEVER
      COMMISSIONED.** Round eleven required every signed record to carry the
      signer's public key beside its signature — and neither `code_surface` nor
      5.4 asked for the field, so **the schema checklist could have completed
      without the input the verifier resolves against**, leaving the positive
      key-resolution fixtures unconstructible. Added at BOTH sites as the THIRD
      field discipline; the phrase moves *two field disciplines* → **three**
      everywhere it appears. **THE EQUALITY CHECK IS WIDENED, BECAUSE THIS
      FINDING WAS ITS BLIND HALF**: it compared 5.4 against `code_surface` over
      RECORD KINDS ONLY, so a missing DISCIPLINE passed it every time. It now runs
      over both halves — 7/7 kinds and 3/3 disciplines, declared, enumerated and
      commissioned. (ii) **THE ANNOUNCEMENT SITES LAGGED 94 → 100.** README:399,
      `INDEX.md`:1907 and `proposal.md`:208 still advertised the pre-round total
      while the delta and this ledger carried the new one. Synced to the
      **MEASURED** figure — counted fresh at **100**, not taken from the report.
      **THE STANDING RULE THIS LEAVES**, recorded at 1.22 so the next count move
      carries its own sync.
- [x] 1.22 **STANDING SWEEP RULES FOR THIS PACKET — the methods the rounds paid
      for, written down so they fire without being asked.** Each exists because
      its absence cost a round.
      - **THE ANNOUNCEMENT-FAMILY SWEEP FIRES ON ANY COUNT-MOVING COMMIT.** A
        commit that changes a scenario total, a record-kind count or a field-
        discipline count SHALL, IN THE SAME COMMIT, sync every announcement site:
        `README.md`, `ideation/staging/INDEX.md`, `proposal.md`'s `code_surface`
        AND its Modified-Capabilities bullet AND its Impact bullet, `tasks.md` 1.1,
        and the pull-request body. **A majority of stale sites is not a
        measurement**, and the figure is COUNTED rather than carried forward.
      - **A FIX THAT MOVES A PREDICATE RETIRES THE PREDICATE'S OLD STATEMENT AT
        EVERY OPERATIVE SITE, IN THE SAME COMMIT — AND THE SWEEP IS SUBJECT-KEYED,
        NEVER PHRASE-KEYED.** Adding the new rule is half the work; the superseded
        sentence left standing elsewhere is still normative, and a realization may
        conform to it. **THE SWEEP ENUMERATES EVERY OPERATIVE SITE THAT TOUCHES
        THE PREDICATE'S SUBJECT** — every requirement clause, scenario and design
        sentence about that subject — **BY READING THE PACKET SECTION BY SECTION
        FOR THE SUBJECT**, and verifies each against the current rule. It does NOT
        grep for the old wording. **GREPPING FOR THE OLD PHRASE IS THE
        FOURTH-APPEARANCE DEFECT ITSELF**: a predicate survives in prose that
        never used the phrase — *"inside the gate's scope is 4 → 5 → 6"*,
        *"certificate-record holds the key"*, *"does not EQUAL this ratification's
        content digest"* all restated a retired rule in words the phrase-keyed
        sweep could not see. This is `#513`'s settlement lesson — **clause-keyed
        beats phrase-keyed** — applied to retirement. Table every site with its
        verdict: CURRENT, RETIRED-THIS-ROUND, or MARKED-HISTORY. **AND THE SWEEP
        SPANS BOTH FIELDS BY DEFINITION — WHAT THE PACKET ASSERTS AND WHAT IT
        COMMISSIONS — PLUS THE DEFINITIONS THE ROUND RECORDS CARRY.** A retired
        predicate hides one layer down: a fixture commissioned through it, or a
        round record stating it in the PRESENT TENSE, is still a live instruction
        to a realization. The subject sweep is not complete until §4–§5's
        commissions and the `1.x` definitions have been read for the subject too. **This family has
        now cost six rounds** — the log-derived authority, the per-tier key
        clause, the kind-only signed order, the chain-identity review binding, the
        equality bridge, and the three predicates that survived a phrase-keyed
        sweep.
      - **THE TWO-FIELD SWEEP**: what the packet ASSERTS and what it COMMISSIONS
        — a superseded rule survives in the examples built against it.
      - **THE GUARD WALK** over every permitting conjunct set, asking *what input
        makes this pass wrongly?* — **including the sets a previous walk touched**,
        because the fix's conjunct set is also a conjunct set.
      - **THE SET-READ**: after amending a requirement, read it AS A SET, not at
        the sites a reviewer named. A scenario-complete restatement is not thereby
        a coherent one.
      - **ONE RULE, NOT SLOTS**: a rule that enumerates the slots it covers will
        be outrun by the next slot. State it over the set.
      - **EQUALITY CHECKS COVER EVERY DECLARED AXIS**, not the first one — 5.4
        against `code_surface` over record kinds AND field disciplines.
- [x] 1.23 **THE FOURTEENTH BOT ROUND'S TWO P1s AND ONE P2 ARE CLOSED.**
      (i) **THE REPLAY FIX DEMANDED A VALUE THAT CANNOT EXIST YET.** The §7.4 flow
      puts the COUNCIL REVIEW BEFORE THE RATIFICATION, and tranche one mints the
      chain identity as the digest of the signed ratification IN that later act
      (`add-signed-execution-chain/spec.md:151-159`). Round eight's binding asked
      the review record to name a value minted after it was written — **so no
      genuine review could ever have satisfied the positive closure path**, and
      the record cannot be amended afterwards without falsifying what it is.
      **Repaired by binding to what exists at review time and bridging through the
      ratification's own bytes**: the review names THE CONTENT DIGEST OF THE
      PROPOSAL IT REVIEWED, and closure verifies the EQUALITY CHAIN — that digest
      EQUALS the ratification's CONTENT DIGEST (taken over the subject ratified),
      whose SIGNED BYTES recompute to THE CHAIN IDENTITY the traveling contract
      carries. Replay stays refused: a review of another proposal names another
      digest and fails the first limb. **The two digests are the ones tranche one
      already distinguishes**, each used for the comparison it was defined for
      rather than collapsed — the error the gate's checks 2 and 3 exist to
      prevent. **THIS LIMB IS SUPERSEDED AND THE ENTRY IS THE RECORD OF WHAT
      ROUND FOURTEEN DID, NOT A STATEMENT OF THE RULE IN FORCE** — round fifteen
      (1.24) replaced the EQUALITY of the two digests with the AMENDMENT LINEAGE,
      because an accepted-as-amended packet's reviewed and ratified digests
      legitimately differ. The temporal diagnosis above stands; the repair it
      describes does not. (ii) **THE SIGNED ORDER WAS OUTRUN AGAIN, BY A KIND THIS PACKET
      ITSELF CREATED.** Round eleven generalized the order and then folded in a
      NAMED KIND — commitment extensions — rather than stating the rule over the
      SET; the ninth round's SIGNED CHAIN BINDING then fell outside the walk,
      because a late dispatch mints one after the hash-link rule is in force.
      **THE PACKET HAD ALREADY RECORDED THIS LESSON AT 1.22 AND THIS SECTION DID
      NOT FOLLOW IT** — recorded plainly rather than smoothed. The rule now governs
      EVERY signed record kind this capability defines, full stop; **a record's
      KIND never determines its place, its POSITION IN THE LOG does**; and
      `4 → x₁ → … → xₙ → 5 → 6 → 10` is marked PURELY ILLUSTRATIVE of the
      no-interleaving case, binding nothing. (iii) **P2 — the composition called a
      FINGERPRINT a KEY.** `subject.public_key_fingerprint` is a fingerprint and
      the canonical shape holds no key at all; the verification key is SUPPLIED by
      the signed record. Both sites corrected to the real mechanics — supply the
      key, compute its fingerprint, compare, then verify — and the requirement was
      swept for other conflation: the four remaining "key" mentions are each
      correct. **1.22's announcement sweep fired in this commit**, the scenario
      total moving 100 → 102 at all four sites.
- [x] 1.24 **THE FIFTEENTH BOT ROUND'S P1 AND ITS THREE PROPAGATION SITES ARE
      CLOSED.** (i) **ROUND FOURTEEN'S EQUALITY BRIDGE WOULD HAVE REFUSED THIS
      PACKET'S OWN RATIFICATION.** *Accepted as amended* is what this council
      returns constantly, and it means the REVIEWED bytes and the RATIFIED bytes
      LEGITIMATELY DIFFER — **this packet is the proof**: the council record pins
      the reviewed head, the thirteen blocking amendments and the bot rounds that
      followed changed the packet many times over, and task 2.6 FORBIDS rewriting
      the sitting artifacts. Requiring digest EQUALITY was the second
      unsatisfiable binding at this link in two rounds, reached by TIGHTENING.
      **The ratification now carries the AMENDMENT LINEAGE** — its signed bytes
      commit to the REVIEWED DIGEST, the RATIFIED SUBJECT DIGEST, and the
      AMENDMENT RECORD connecting them (the `review/` directory this flow already
      mandates: council record, disposition, discharge trail) — and closure
      verifies three limbs: the review names the reviewed digest; the ratification
      commits to that review and that lineage; the ratified subject IS the
      lineage's endpoint. **Replay is refused for a better reason** — another
      proposal's review appears in NO lineage this ratification commits to — and a
      ratification cannot merely ASSERT a lineage its committed record does not
      support. **The unamended case is the DEGENERATE form of the same rule**, a
      lineage of length zero: one rule, not two paths. (ii) **THREE SITES WHERE
      ROUND FOURTEEN'S FIX DID NOT RETIRE THE OLD WORDING** — the positive closure
      scenario still required the review to name the chain identity; the operative
      predecessor sentence and the link-9 scenario still declared the fixed order
      **is** 4 → 5 → 6 → 10; and the replay fixture still refused on
      chain-identity-not-named. All retired to the new rules, with the numbered-
      link order now stated as an ILLUSTRATION ON THE SIMPLEST CHAIN that binds
      nothing. **THE RETIRE-SWEEP RAN OVER BOTH SUPERSEDED PREDICATES** across the
      whole packet; every surviving mention is now the new rule or marked history.
      **AND THE STANDING RULE IS ADDED TO 1.22**: a fix that moves a predicate
      retires the predicate's old statement at every operative site IN THE SAME
      COMMIT — this family has now cost five rounds.
- [x] 1.25 **THE SIXTEENTH BOT ROUND'S THREE FINDINGS ARE CLOSED, AND ALL THREE
      ARE THE RETIRE-FAMILY'S FOURTH APPEARANCE — because round fifteen's sweep
      was PHRASE-KEYED and each predicate survived in prose that never used the
      phrase.** (i) The replay scenario still refused on *review digest ≠
      ratification's content digest* — **which the lineage rule makes the ORDINARY
      case for an accepted-as-amended packet**, so implementing it literally
      would have rejected legitimate closure while the positive scenario admitted
      it. Retired to the lineage limbs, with an explicit AND stating that the
      difference is NOT the ground of refusal. (ii) The operative gate-walk
      paragraph still defined the in-scope sequence as `4 → 5 → 6`, letting a gate
      omit interleaved extensions and chain bindings from continuity. Retired to
      the universal rule: **the walk is over THE RECORDS THE LOG HOLDS IN THE
      ORDER IT HOLDS THEM**, and a signed record omitted because its kind is
      unnumbered is an UNLINKED RECORD. (iii) The composition still claimed
      `certificate-record` **holds the key**; it holds a FINGERPRINT and no key.
      Retired there, in `code_surface`, and in 5.4 — all three realization sites.
      **THE METHOD IS FIXED AT 1.22: THE SWEEP IS NOW SUBJECT-KEYED.** Every
      operative site touching a moved predicate's SUBJECT is enumerated by reading
      the packet section by section — not by grepping the old wording, which is the
      defect itself. **THE THREE SUBJECT SWEEPS RAN**: closure/review-binding **51
      operative spec sites**, predecessor/order **30**, certificate/key/fingerprint
      **32**, plus the non-spec operative surfaces (`code_surface`, Impact, tasks
      §4–§5). **After this round's four retirements, ZERO stale sites remain on any
      of the three subjects.**
- [x] 1.26 **THE EIGHTEENTH BOT ROUND'S P1 IS CLOSED — THE LINEAGE FIELDS HAD NO
      SCHEMA HOME.** Closure's limbs require the reviewed digest, the ratified
      subject digest and the amendment-record reference to sit INSIDE THE BYTES
      THE RATIFYING SIGNATURE COVERS — and that act is TRANCHE ONE's. 5.4
      commissioned only this packet's seven kinds and `proposal.md`'s
      `target_release` classified the release as changing no existing schema, so
      **both lineage positives were unconstructible as commissioned.** **ROUTE A
      TAKEN — a SECOND scenario-complete `## MODIFIED` on tranche one's
      ratification/chain-inception requirement**, verified lawful against the
      ratified texts rather than assumed: (1) **~~tranche one is
      RATIFIED-NOT-REALIZED~~ — SUPERSEDED 2026-09-01, SEE 1.27**: that was true when
      the round was written and died with PR #524 (`9af98c4d`), which realized
      tranche one at `contract-v2.5`. Re-grounded on the #497 precedent — the
      MODIFIED on the REQUIREMENT TEXT is lawful canon amendment, and its schema
      consequence is an ADDITIVE EXTENSION of the shipped schema at this packet's
      own cut; (2) **this packet already holds exactly this
      instrument by the council's own prescription** (LA-A1's scenario-complete
      MODIFIED on the gate requirement), so it is a precedent APPLIED, not set;
      (3) **no sibling delta collides** — only tranche one and this packet write
      to `signed-execution-chain`; (4) the archive-order dependency is the one
      already carried and is not widened. All SIX of that requirement's scenarios
      are restated verbatim (PR #331's rule) plus two for the lineage. **ROUTE B —
      an eighth record kind of our own — is recorded as considered and RULED
      AGAINST at `design.md` D12**: it would put the lineage in a record the
      ratifying signature does not cover, which this capability's own rule calls
      attachable-afterwards, and it would mint a kind to carry three fields
      belonging to an act we do not own. The three closure limbs are re-expressed
      to read the fields that now exist; 5.4 commissions them CROSS-TRANCHE and
      says why; `target_release` states what is true — **as re-grounded 2026-09-01, an
      ADDITIVE EXTENSION of the shipped `chain-inception.schema.yaml` at this
      packet's own cut.** **1.22's
      announcement sweep fired**: the MODIFIED block moves 1 requirement / 9
      scenarios → **2 requirements / 17 scenarios** at every site.
- [x] 1.27 **THE NINETEENTH BOT ROUND — THE RATIFIED HEAD'S OWN VERDICT — AND
      BRETT'S ROUTE-A GROUND CORRECTION, DISCHARGED AS ONE ACT.** A Codex review
      naming `f54cb5bc` arrived AFTER the ratification, the sixth time a verdict
      landed in a gap. **THREE P1s, none bookkeeping.** (i) **A RIVAL
      AUTHORITY-PROVEN REVIEW OF THE SAME BYTES COULD CLOSE THE CHAIN** — limb 1
      compared SUBJECTS and not review IDENTITY, and the committed fields named no
      review record at all, so **limb 2 was not constructible as written**, a
      defect introduced in round eighteen. The ratifying bytes now commit to a
      FOURTH lineage field, **THE CONSUMED REVIEW RECORD'S OWN DIGEST**, and limb 1
      compares identity TWICE — against that digest and against the review the
      amendment record names. (ii) **LINK 6 BOUND TO NO PULL REQUEST**: a decision
      reused after a branch move, retargeted, or attached to another PR carrying
      the same chain identity permitted **a merge of work the controller never
      signed as the proposed work**. The signed decision now carries the PR
      IDENTIFIER and HEAD REVISION and the gate refuses unless both EQUAL the
      merge. (iii) **A NO-OP TEST COULD CLOSE THE CHAIN**: rounds four and seven
      hardened the OUTCOME and never checked the test was the RIGHT test, so
      *"governed"* constrained nothing a verifier could check. **The ratified
      subject now NAMES the governed test**, the controller dispatches THAT test,
      and the closure record's test identity must EQUAL it. Plus the two
      announcement P2s — `proposal.md`'s heading said ONE MODIFIED block where
      there are TWO, and the PULL-REQUEST DESCRIPTION still called the packet a
      draft. **THE GUARD WALK RAN over all nine permitting conjunct sets**: the new
      PR-binding positive is scoped to *"proceeds to the rest of the walk"* by
      construction, and the closure positive gained the test-identity conjunct.
      **AND THE ROUTE-A GROUND IS CORRECTED IN THE SAME ACT** — see 1.28.
- [x] 1.28 **THE ROUTE-A GROUND MOVED, AND BRETT RE-RULED IT.** The merge-up
      against `main` surfaced that **PR #524 (`9af98c4d`) realized tranche one at
      `contract-v2.5`**, falsifying Route A's first precondition — *"tranche one is
      ratified-not-realized, so no contract byte exists to break"* — which was TRUE
      at `dd847e44` and verified there. **The merge was ABORTED rather than
      pushed**, because pushing it would have landed a ratification record the
      same tree disproves. Brett was given the correction in full and ruled
      **"route A"** (2026-09-01). **THE ROUTE STANDS; ITS GROUND MOVES**: the MODIFIED on
      tranche one's REQUIREMENT TEXT is lawful OpenSpec canon amendment, and its
      SCHEMA consequence is an **ADDITIVE EXTENSION OF THE SHIPPED
      `chain-inception.schema.yaml` AT THIS PACKET'S OWN RELEASE CUT** — the
      precedent being `add-binding-consumer-identity` (#497), ratified extending a
      SHIPPED template with an additive optional block. **THE SUBJECT-KEYED
      RE-GROUND SWEEP** ran over both fields and corrected every site: the
      ratification record's basis §2.1, `design.md` D12, `tasks.md` 1.26 and 5.4,
      and `proposal.md`'s `target_release`. **Superseded grounds are MARKED AND
      DATED, not rewritten** — they were the reasoning of their round — and **Route
      B's refusal ground is recorded as UNAFFECTED**, having never depended on
      tranche one being uncut.

## 2. §7.4 COUNCIL REVIEW — **HELD 2026-08-30. THE FIRST GATE IS DISCHARGED.**

The council-reviewed-but-human-approved path that per the 2026-08-26 record §7.4
needs no candidate class and no flip, and reaches this repository without an
envelope and without amending FR-008. This packet creates no
`merge-approval-envelope` and declares no candidate class.

**The sitting is on the record in `review/`**, filed byte-faithfully as it was
put and returned: the record `review/council-review-2026-08-30.md` (Status:
`record — VALID`, all three operator slots filled), the **SOLE disposition of
record** `review/disposition-2026-08-30.md` (Brett Heap, 2026-08-30), the ballot
as put `review/ballot-2026-08-30.md`, the packet as read
`review/convening-packet-2026-08-30.md`, and the four verbatim seat returns at
`review/seat-returns-2026-08-30/`. **THE RETURNS GOVERN** over every summary in
that paperwork, the disposition included.

- [x] 2.1 The §7.4 sitting was CONVENED on 2026-08-30 on `gate_rules_council`,
      OUTSIDE the codexFactory clearance-envelope pipeline, mirroring the
      procedure `add-binding-consumer-identity` ran on 2026-08-29. Four seats
      returned: `lead-architect`, `lead-security`, `lead-quality`,
      `company-policy-lead`. **Judged at `e7f6ae0e`**, this packet's head.
- [x] 2.2 **Q4's re-derivation instruction — RULED FIRST, AND RULED NOT
      PREMATURE.** Decision 1 of the disposition: *"(c) NOT PREMATURE BUT
      NARROWED"* — the round did NOT end, Q4 is not re-ruled, and the narrowing is
      `lead-architect`'s LA-A5, **BLOCKING**: the re-derivation tranche one's
      ratified `tasks.md:5.3` owes *"when each is raised"* is due at THIS raising.
      Discharged in the fix round at `design.md` **D7a**, dated and measured.
- [x] 2.3 **The gate composition — RULED INSUFFICIENT, and the named repair was
      taken.** The bench was **UNANIMOUS 4/4** that the packet as drafted was not
      ratifiable, on a finding reached BY CONSTRUCTION: archiving tranche one and
      then this packet produces a canon holding **two contradictory scenarios on
      one antecedent**, both normative, with `openspec` reporting `~ 0` modified.
      The repair is LA-A1's SCENARIO-COMPLETE MODIFIED restatement of tranche
      one's gate requirement — **all NINE scenarios** (LQ-A1: the packet had said
      *twelve* at four sites; three seats measured nine) — with LA-A2's mapping
      table extended to all eighteen requirements. Landed at 1.2.
- [x] 2.4 **The plural-predecessor enumeration — the resolution STANDS**, and was
      hardened: `lead-quality`'s LQ-A3 (BLOCKING) closed the deferred-leaf path
      the derived-set repair left open. `lead-architect` and `lead-quality`
      DISAGREE on the P1-2 fix and **the disagreement is PRESERVED UNRECONCILED**
      by the disposition (§6); LQ-A3 is blocking regardless and is discharged
      without settling it.
- [x] 2.5 **The revocation-after-signing horizon — the decision STANDS**, and
      LQ-A4 (BLOCKING) gave it something to rule on: it had zero scenarios and no
      `SHALL`. Requirement 1 now carries both and two revocation scenarios.
- [x] 2.6 The review record landed in `review/`, mirroring
      `add-binding-consumer-identity`'s directory, and names each seat, each
      blocking amendment, and the verdict word. **No sitting artifact is edited by
      this packet** — the packet-as-read and the ballot-as-put are preserved
      including their recorded errors, on the discipline the disposition states at
      §3.7.
- [x] 2.7 **THE FIX ROUND — THIRTEEN BLOCKING AMENDMENTS, ALL DISCHARGED.**
      Brett Heap ruled *"accept all fifteen as recommended, 14 folds into the fix
      rounds"* (disposition §1). #510's blocking set is **THIRTEEN**, not eleven:
      LA-A1, LA-A2, LA-A3, LA-A5 · LS-A1, LS-A2, LS-A3 · LQ-A1, LQ-A2, LQ-A3,
      LQ-A4 · **LS-A10** and **LQ-A13**, both filed SHOULD-FIX by their seats and
      **ELEVATED TO BLOCKING** by decision 13. Each is discharged per its return's
      own named discharge, and LA-A1's verifier — LA's own §1.3 construction — was
      re-run and reported.
- [ ] 2.8 **THE SHOULD-FIX SCHEDULE IS UNDISPOSED AND STAYS OPEN.** *"Accept all
      fifteen"* reached the fifteen §12 decisions and the blocking sets they
      carry; it did NOT rule the should-fix items, except LS-A10 and LQ-A13 which
      decision 13 elevated by name (disposition §6). Still owed on #510: LA-A4
      (subsumed by LQ-A1's identical correction), LA-A6 (constrain the archive
      order — now load-bearing, because 1.2's MODIFIED block depends on tranche
      one archiving FIRST), LA-A9 (consume R12 as a named carry), LA-A10's tranche-
      one half, LS-A4, LQ-A8, LQ-A9, CPL-A5. **None is performed in this fix
      round**, and the omission is deliberate rather than overlooked.

## 3. RATIFICATION GATE — **TAKEN 2026-09-01.** Brett Heap's act

- [x] 3.1 **RATIFIED BY BRETT HEAP, 2026-09-01, at `f54cb5bc`, AND RE-RATIFIED THE SAME DAY at `6d7ef17b` after the amendments (record §7)** — record:
      `openspec/changes/add-chain-attestation/review/ratification-2026-09-01.md`. The review was HELD and the
      fix rounds it forced were LANDED (§2), and the ratification read followed
      them — the
      ratification READ the disposition names at §8, taken against the amended
      text and not against the text the bench judged. The record lands at
      `review/ratification-<date>.md` with front-matter `Status: ratified` plus a
      `Ratified:` line naming approver, date and a resolvable record path, per the
      `sanction-ratified-record-spelling` three-way floor.
- [ ] 3.2 `target_release` CONFIRMED at ratification against
      `contracts/manifest.yaml` at that tip — the number is deliberately unnamed in
      this draft and stays ALLOCATED AT REALIZATION by merge order per
      `docs/contract-versioning-policy.md`, because tranche one already names the
      family's next additive cut.
- [ ] 3.3 Ratification, if it comes, authorizes ONE contract feature plus the
      extension of an existing gate. It creates NO certificate authority, NO
      attestation identity, NO anchor and NO chain, and it performs NO realization.

## 4. Settle before schemas are authored

The five open design points `design.md` names, plus the one this tranche inherits.
Each is contract content — cheap now, expensive after a bundle ships.

- [x] 4.1 Fix the **signing-request record shape**, for BOTH SUBJECT SCOPES — a
      field on the record or a sibling record it references, for the task-scoped
      link-5 request AND for the chain-scoped link-6/link-10 request. The
      requirement fixes for each that it is recorded alongside the signature, that
      the request is ATTRIBUTED (to the provisioned task; to the party the chain's
      inception record binds), and that absence is refused — not its shape.
      **SETTLED: a REQUIRED member INSIDE the signed block, not a sibling record**
      (`contracts/signed-execution-chain/attestation-common.schema.yaml`
      `$defs.signing_request`, consumed by `$ref` from the runner attestation,
      the PR-open decision and the closure record). One shape, two attribution
      modes (`controller_provisioning` for link 5; `chain_inception_binding` for
      links 6/10), the request's own `payload_digest` taken over the signed block
      WITH the request removed so the commitment is well-founded, and ABSENCE IS
      UNREPRESENTABLE rather than refused — the member is `required`, which is
      stronger than the requirement asked for and recorded as such in the
      conformance declaration's SEC-R11 entry.
- [x] 4.2 Fix the **evidence-class vocabulary's closure** — whether
      `controller_corroborated` / `independently_observed` / `runner_claimed` is a
      CLOSED set at the schema, and what a fourth class would have to establish.
      **THE NAMED INPUT TO THIS DECISION IS
      `contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml`** — the
      ratified, CLOSED assurance registry `add-trust-anchor` put in force at
      `contract-v1.37` (Brett Heap, 2026-08-21, OQ2). Its `excluded_models` block
      is the worked example of what admitting a member on the wrong discriminator
      costs, and it is why this packet's third class is named
      `independently_observed` rather than `hardware_attested` (`design.md` D2). A
      fourth class is judged against that registry's reasoning and against the
      composition and ORDER D2 declares — not against intuition — and the schema
      SHALL carry an explicit composition statement on that registry's own
      `composes_with` pattern so the two sets cannot drift into two custody models.
      **SETTLED: CLOSED at three members**
      (`attestation-common.schema.yaml` `$defs.evidence_class`, `enum` of exactly
      `controller_corroborated | independently_observed | runner_claimed`), with
      the composition statement carried in that file's prose on the registry's
      own `composes_with` pattern, naming
      `contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml` and the
      ORDER D2 declares (custody ceiling first, evidence class second, and no
      class raises a fact above the ceiling — `custody_ceiling_exceeded` is the
      reader's named refusal for the drift). A fourth class is a governed change
      to that enum judged against the registry's `excluded_models` reasoning.
- [x] 4.3 Fix **what a setup attestation enumerates** — how the model surface, the
      harness and its version, the toolchain and the workspace provenance are each
      expressed.
      **SETTLED: four NAMED fact lists under one fact shape**
      (`setup-attestation.schema.yaml` `provisioned_environment`, members
      `model_surface`, `harness`, `toolchain`, `workspace_provenance`, each a
      non-empty list of `$defs.attested_fact` — fact name, value, REQUIRED
      evidence class, and `observed_by` wherever the class asserts independent
      observation). The four surfaces are the requirement's own enumeration; the
      fact shape is shared with link 5 so corroboration is a comparison over one
      grammar rather than a translation between two.
- [x] 4.4 Fix the **ordering key for the plural-predecessor enumeration**, settled
      WITH tranche one's single digest construction and never beside it.
      **SETTLED: THE LOG'S OWN ORDER IS THE KEY.** A record's predecessor is the
      actual nearest prior IN-FORCE signed record of its chain, resolved by leaf
      position in the one transparency log — not by record kind, which is what
      lets the interleaved fan-out (packaged chain two) and the up-front fan-out
      (chain three) walk under one rule. The predecessor digest is taken under
      `xfc-jcs-sha256-1` and NAMES ITS SUBJECT (`attestation-common.schema.yaml`
      `$defs.predecessor`; eleven subjects added to the construction's
      enumeration and NO second construction); a link-5 leaf deferred past its
      successor's is the reader's `attestation_leaf_deferred_past_successor`.
- [x] 4.5 Confirm the extended gate stays **ONE required check walking further**,
      never a second gate.
      **CONFIRMED IN THE ARTIFACT: the same job id, the same workflow, the same
      ruleset entry** (`signed-execution-chain-gate`, org ruleset 21957695,
      untouched by this realization). The walk gains three legs at their own
      positions inside the ONE ordered check list (eleven for `links_1_6`), a
      NEW `links_1_3` verdict over a chain carrying tranche-two records is
      refused as `gate_scope_understated`, a `links_1_6` verdict recording only
      the shorter walk is `gate_walk_incomplete`, and the packaged tranche-one
      chain keeps its own cut-time verdict on the two-horizon doctrine.
- [x] 4.6 Fix the **per-task reference** the expected attestation set is written
      in — the value link 4 commits to and the link-5 attestation carries back,
      settled WITH tranche one's single digest construction and never beside it.
      The requirement fixes that the reference is STABLE, that it falls inside the
      controller's signed bytes, and that an attestation for an uncommitted task
      is refused; it does not fix the reference's shape. **The extension record's
      own shape rides with it**, since an extension is the same commitment written
      later, and both are refused if the reference cannot be matched.
      **SETTLED: an opaque stable string, matched by EQUALITY and never parsed**
      (`setup-attestation.schema.yaml` `expected_attestation_set[].task_ref`;
      `commitment-extension.schema.yaml` `added_tasks[]` is the SAME member shape
      with `dispatched_at` and the dispatch-deadline rule). Link 5 carries the
      reference back verbatim in its signed bytes, the reader's
      `attestation_for_uncommitted_task` refuses a reference outside the
      committed union, and link 6's enumeration must EQUAL that union in both
      directions.
- [x] 4.7 Fix the **chain-scoped identity's issuance and lifetime** — when the
      controller mints the one chain-scoped tier-2 identity per chain, and when it
      is destroyed. The requirement fixes that there is EXACTLY ONE per chain
      identity, that it is ephemeral, that its key stays at the controller's
      signing boundary, and that its authorized record kinds are links 6 and 10
      and nothing else; it does not fix the mint point. Settled WITH the per-task
      identities' lifetime and never beside it, since both are tier 2 under one
      custody rule.
      **SETTLED: MINTED WHEN THE CONTROLLER FIRST NEEDS IT AND NO EARLIER THAN
      SETUP, DESTROYED WITH THE CHAIN'S CLOSE** — both tier-2 scopes under the
      ONE custody rule: a signed chain binding descending from the chain's own
      hash-linked order (the packaged chains mint it up front in chain three and
      after the first attestation in chain two, both lawful), a certificate whose
      `validity` bounds close the same day the chain does
      (`signed-chain-binding.schema.yaml` `validity_statement`), EXACTLY ONE per
      chain enforced by the reader (`subject_scope_mismatch` on a second), and
      the closed enumeration links 6 and 10 and nothing else — with the lifetime
      never offered as a custody relaxation
      (`ephemeral_lifetime_offered_as_non_secret`).

## 5. Realization — ONE Speckit contract feature, GATED ON MACHINERY

**Both gates are hard and neither is discharged by ratification.**

- [ ] 5.1 **[GATE] Re-derive the tranche boundary against what actually exists**
      when the omnigent layer and the PKI plane are real, per Q4's ruling — the
      SECOND re-derivation. **The FIRST fired at the raising and is DISCHARGED at
      `design.md` D7a**, per tranche one's ratified `tasks.md:5.3` (*"when each is
      raised"*); this one fires at the REALIZATION and neither substitutes for the
      other. This obligation survives ratification deliberately: a packet cannot
      discharge it, because it is an obligation about a state the packet cannot
      observe. **ITS TRIGGER AND ITS OUTPUT ARE NAMED, SO IT IS DECIDABLE RATHER
      THAN PERPETUAL** — the family's evidence convention applies, and each
      observable closes on a FACT that survives the session:
      - **"THE PKI PLANE IS REAL" — THE OBSERVABLE.** A CONTROLLER CERTIFICATE HAS
        BEEN ISSUED by the authority `implement-openxpki-install-repo` operates,
        with the ISSUANCE EVIDENCE record `add-trust-anchor` requires — naming
        which anchor issued, under which authority, on whose request and when —
        and that certificate's chain TERMINATES IN AN ANCHOR RECORD THE GATE
        HOLDS. Recorded by anchor id, issuance-evidence path and certificate
        subject. **Not** the change reaching 30/30, and **not** a deployed
        install: an operated CA that has issued nothing has not been shown to
        issue.
      - **"THE OMNIGENT LAYER IS REAL" — THE OBSERVABLE.** A RUNNING LAYER HAS
        REFUSED a step whose inbound chain does not verify, recorded as a REFUSAL
        TO EXECUTE and not as a failed execution, with the run id and the refusing
        component named. Until that read exists, requirement 9 is UNMET rather
        than partially met (5.3), and this trigger has not fired.
      - **THE ARTIFACT THE RE-DERIVATION PRODUCES.** A dated re-derivation record
        at `review/re-derivation-<date>.md`, on the form `design.md` D7a uses:
        (i) the two observables above with their evidence cited by id or path;
        (ii) what each plane actually exposes, measured rather than assumed;
        (iii) the boundary derived FROM that, stated link by link, **naming any
        link it moves and stating explicitly where it moves none**; and (iv) what
        it obliges — either a successor change, or a recorded finding that the
        ratified boundary holds. **This box closes on that file and on nothing
        else**; a re-derivation performed and not written down has not been
        performed, on the same footing this capability applies to every other
        record it governs.
- [ ] 5.2 **[GATE] `implement-openxpki-install-repo` real enough to issue a
      controller certificate**, with the issuance evidence `add-trust-anchor`
      requires, and with any shortfall DECLARED under its conformance-declaration
      rule rather than asserted.
- [ ] 5.3 **[GATE] The omnigent layer real enough to enforce a precondition.**
      Until a running layer refuses, requirement 9 is UNMET rather than partially
      met, and this packet claims no enforcement it cannot name a check for.
- [x] 5.4 `contracts/signed-execution-chain/` gains the setup-attestation record
      **carrying its committed expected attestation set**, the
      **controller-signed commitment-extension record**, the runner-attestation
      record together with the signing-request record, the PR-open decision
      record, the closure record, the remediation declaration, **the SIGNED CHAIN
      BINDING record** — this capability's seventh record kind, carrying a tier-2
      identity's SUBJECT SCOPE, its CLOSED RECORD-KIND ENUMERATION and THE CHAIN
      IDENTITY IT SERVES, and referencing by identifier the two CANONICAL
      `add-trust-anchor` records it composes with (`certificate-record` for the
      PUBLIC-KEY FINGERPRINT and validity bounds — a fingerprint and NO key, the
      key being supplied by this capability's signed record — and
      `issuance-evidence` for the issuance act), **both
      CONSUMED AND NEITHER REDEFINED HERE** — the per-fact evidence class, **THE
      SIGNER'S PUBLIC KEY CARRIED BESIDE EVERY SIGNATURE** on every record this
      capability defines, **AND — CROSS-TRANCHE, STATED HONESTLY — THE THREE
      AMENDMENT-LINEAGE FIELDS ON TRANCHE ONE'S RATIFICATION/CHAIN-INCEPTION
      RECORD** (the reviewed digest, the ratified subject digest, and the
      amendment-record reference), which this packet's second `## MODIFIED`
      requirement adds to that record's definition. **They are commissioned here as an ADDITIVE
      EXTENSION OF THE SHIPPED SCHEMA** — tranche one's contract surface WAS CUT
      by PR #524 (`9af98c4d`) at `contract-v2.5`, and
      `contracts/signed-execution-chain/chain-inception.schema.yaml` is
      `additionalProperties: false` carrying NO lineage fields — so this
      realization EXTENDS a released schema at this packet's own cut, on the #497
      precedent. This task names them so neither tranche can assume the other
      did (the field verification resolves against the consumed
      certificate's `subject.public_key_fingerprint`, and without which the
      key-resolution rule has no input), and
      **tier 2's TWO SUBJECT SCOPES with their two closed enumerations of
      authorized record kinds** — per-task (link 5) and chain-scoped (links 6 and
      10), with authority records outside both.

      **WITHOUT THE BINDING'S SCHEMA THIS CHECKLIST COULD COMPLETE WHILE THE
      COMPOSITION STAYED UNREPRESENTABLE** — 5.5 and 5.6 commission fixtures and a
      named refusal against a record `contracts/` would not hold. The two
      canonical shapes are NOT commissioned here because they are not this
      capability's to define; they are consumed from `add-trust-anchor` at
      `contract-v1.37`.
- [x] 5.5 Packaged POSITIVE and NEGATIVE examples for every named refusal: no
      anchor held, host-held custody offered for hardware-bound assurance, absent
      link 4, empty setup attestation, runner-produced signature, missing signing
      request, attestation identity as actor, reused per-task identity, payload
      disagreeing with link 4, unclassed fact, runner-claimed fact read as
      attested, key crossing into a worker, reusable signing delegation, orphan
      pull request, subset commitment, second digest construction, unnamed digest
      subject, unevaluable chain, links 1–3 only after this tranche, proposal-only
      post-merge test, unsigned pass, merged-and-never-closed, release over an
      unclosed chain, exemption claimed by mention, exemption inherited, remediation
      skipping the gate, seventh permission boolean, worker given key material to
      verify, and execute-then-verify — **plus the eight the 2026-08-30 fix round
      added**: certificate revoked at signing, certificate revoked after signing
      (the horizon case, where the permitted act stands and the remainder is
      refused), a chain from a platform that declared it cannot attribute reaching
      the gate, both attribution branches holding at once, a signing key readable
      from the scope the runner executes within, a controller co-located inside the
      runner's trust boundary, a link-5 leaf written after its link-6 successor's,
      and a review-authority standing read from a projection older than the
      register's declared staleness bound — **plus the nine the second bot round
      added**: a setup attestation committing to no expected attestation set, an
      expectation carried outside the signed bytes, a commitment extension written
      after the attestation it covers, an attestation for a task no commitment
      covers, an extension signed away from the controller, a dispatched runner's
      leaf never written at all, an attestation produced outside the committed
      expectation, and a tier-2 identity offered for a record kind outside its
      closed enumeration — **plus the four the third bot round added**: a
      multi-task fan-out whose single link-6 decision is signed by the CHAIN-SCOPED
      identity (**the positive case that proves producibility**), a per-task
      identity offered for the PR-open decision, the chain-scoped identity offered
      for a runner attestation, and a tier-2 identity of EITHER scope offered for
      an authority record — **plus the four the fourth bot round added**: a lane
      supplying a fabricated passing outcome, a tested revision that is not the
      merge commit the chain closed over, a declared shortfall offered as grounds
      for closure, and **the positive closure case** (the controller dispatches the
      test, the revision matches, and execution, revision and result all fall
      inside the signed bytes) — **plus the three the fifth bot round added**: a
      chain-scoped signing request from **a caller the chain's inception record
      does not bind**, REFUSED; a chain-scoped link-6 or link-10 record carrying
      **no recorded signing request**, REFUSED; and **the positive attribution
      case** — the party the chain's inception record binds asks, the request is
      ATTRIBUTED to it, RECORDED beside the signature it receives, and the
      attribution falls INSIDE the signed bytes.

      **AND THE SEVENTH ROUND'S SET**: an established post-merge result that is a
      **FAILURE**, refusing closure and routing to remediation; a **commitment
      extension written after the dispatch** of the task it adds, refused; a
      realization that **mints extensions on signing-request arrival** while a
      runner suppresses its attestation, refused; **link 10's signature hashing a
      link-9 artifact**, refused; **two realizations picking different
      predecessors for link 10**, the second refused; and the two the review-
      authority repair named and this list omitted — **a FABRICATED REVIEW RECORD**
      consumed by a passing test, and **REVIEW AUTHORITY REVOKED BEFORE ITS
      EXERCISE** — both refusing closure. **The positive closure fixture binds a
      PASSING result**, since an established failing one is now a refusal.

      **AND THE EIGHTH AND NINTH ROUNDS' SET**: a **lane-minted keypair labelled
      with the expected scope**, refused AT ISSUANCE because it has no certificate
      record, no issuance evidence and no signed chain binding; **an identity
      MISSING ANY ONE of the three composed records**, refused; a signed chain
      binding **naming another chain**, refused; a tier-2 signature over **a record
      kind outside the closed enumeration ITS OWN SIGNED CHAIN BINDING carries**,
      refused; an identity whose **`validity.not_after` in its CERTIFICATE RECORD
      had passed at signing**, refused; **a genuine review record from ANOTHER
      PROPOSAL**
      replayed, refused because its REVIEWED DIGEST appears in no amendment
      lineage this ratification commits to; **a ratification claiming a lineage
      its own committed amendment record does not support**, refused; an
      **record chaining from anything other than its actual nearest prior in-force
      record**, refused as a break; a **tier-2 certificate record with no
      `subject.public_key_fingerprint`**, refused; a **signing key whose computed
      fingerprint does not EQUAL the certificate's**, refused as a forged
      identity; an **earlier REJECTED review of the same reviewed bytes** replayed,
      refused on the REVIEW-IDENTITY comparison; a **link-6 decision reused after a
      branch move, a retarget, or attached to another PR on the same chain**,
      refused; **an arbitrary passing test on the right revision**, refused on the
      governed-test identity; POSITIVES for **the open decision matching the merge
      it permits**; a **controller-signed link-4 or extension record supplying its own
      key against a controller certificate with NO fingerprint**, refused; and
      POSITIVES for **the verification key resolving against the certificate**,
      for **records under a compliant CONTROLLER certificate verifying**, for **a review written BEFORE ratification closing its own chain through THE THREE LINEAGE LIMBS** — the review naming the reviewed digest, the ratification committing to that review and that lineage, and the ratified subject being the lineage's endpoint — for **a late-dispatched task's SIGNED CHAIN BINDING descending from the actual latest signed record**, and for **a later task dispatched after an earlier task has
      attested** — the extension chaining from that link-5 record and the gate
      walking the interleaved order; and
      two POSITIVES — **a genuine tier-2 identity's THREE records verifying end to
      end** (certificate valid and current, issuance evidenced, chain binding
      naming this chain and this scope — then the signature, then the link's own
      checks) and **a chain
      with commitment extensions walked for continuity** over the illustrative
      4 → x₁ → … → xₙ → 5 → 6 → 10; and **AN AMENDED PACKET CLOSING ON ITS OWN
      LINEAGE** (reviewed digest ≠ ratified subject digest, connected by the
      committed amendment record) beside **an UNAMENDED review closing by the
      same three limbs** over a zero-length lineage; and, on tranche one's
      now-extended ratification record, **an inception whose signed bytes OMIT any
      of the three lineage fields**, refused, beside **an unchanged subject
      ratified with a ZERO-LENGTH lineage carried by the same three fields**.

      **AND FIVE THE FIXTURE-EQUALITY CHECK FOUND, NAMED IN THE DELTA SINCE THE
      FIRST DRAFT AND NEVER COMMISSIONED HERE**: a **persona proposed for a
      runner**, refused; a signing request naming **a subject the controller
      provisioned nothing for**, refused; **a one-task lifetime offered as making
      a key non-secret**, refused; **valid artifacts from DIFFERENT EXECUTIONS
      submitted together**, refused on broken continuity — the mix-and-match
      attack this family exists to refuse, and the most conspicuous of the five;
      and the remediation **POSITIVE case**, a corrective change declaring the
      failed closure as its signed subject and being ADMITTED as the one
      permitted consumer of an unclosed chain.

      **THREE SCENARIOS ARE DELIBERATELY NOT COMMISSIONED, AND THE OMISSION IS
      RECORDED RATHER THAN LEFT TO LOOK LIKE A GAP.** *"a reader treats an
      unclosed chain as pending"* and *"an unpermitted step is recorded as a
      failed execution"* are the reader-correction shape `lead-quality`'s **LQ-A8**
      (SHOULD-FIX, undisposed) asks be rewritten: their THEN is *"it is
      corrected"*, with no actor and no system consequent, so **no check can run
      them as written**. They get fixtures when LQ-A8 is taken, not before. And
      *"an HSM is adopted"* asserts CONFORMANCE INVARIANCE — that no record the
      chain carries changes — which is a property of the whole corpus rather than
      a named refusal, and 5.5 commissions examples per refusal.
      **AND THE POSITIVE CLOSURE FIXTURE CARRIES ITS ATTRIBUTED REQUEST.** Link 10
      is signed under the chain-scoped identity, so its request is attributed and
      recorded exactly as link 6's is; a closure fixture built without one would
      exercise the outcome rule and silently skip the authentication rule that
      landed beside it. The positive closure case above is therefore built with
      the attributed, recorded chain-scoped request present, and a **link-10
      record with no recorded request** is one of the negative examples.

      **DONE — `contracts/signed-execution-chain/examples/tranche-two/`**
      (positives landed at `b63fa61a`, the negative corpus completed at
      `9b7bf18e`): FOUR positive chains — chain two, the multi-task fan-out
      DISCOVERED AS THE WORK RAN with its extension chaining from the earlier
      task's link-5 record, its single chain-scoped link-6 decision, its
      attributed recorded requests and its AMENDED lineage; chain three, the
      UNAMENDED zero-length lineage and the up-front fan-out; chain four, the
      remediation positive (a full chain, closing on a PASS, declaring an
      unclosed chain outside the corpus by identity); chain five, the complete
      single-task append target — plus the consumed trust-anchor records carried
      so every reference resolves, and SEVENTY-FOUR intended-invalid negatives,
      one per named refusal above, each re-signed after mutation so it tests the
      rule and not a broken signature (except the fixture whose subject IS the
      broken signature). Every fixture carries its `expected_failure` code and,
      where load-bearing, the expected message fragment; the two lineage defects
      that live inside signed bytes carry their own bespoke inception. The three
      deliberately-uncommissioned scenarios remain uncommissioned exactly as
      recorded below.

      **THE SECOND ROUND'S POSITIVE FIXTURE IS WITHDRAWN AND THE WITHDRAWAL IS
      NAMED.** It required *"the positive case of that identity signing its task's
      link-6 and link-10 records"* — a per-task identity signing links 6 and 10 —
      which the third round's closed enumeration makes IMPOSSIBLE and explicitly
      refuses. Building it would have forced the validator to accept a
      now-forbidden signature or left this task uncompletable. The chain-scoped
      positive case above replaces it.
- [x] 5.6 `scripts/validate-signed-execution-chain.py` extended — one named
      refusal per negative example above.
      **DONE**: the tranche-two walk lives in
      `scripts/signed_execution_chain/attestation.py`, invoked by the SAME
      reader over TWO packaged corpora (the split forced by the log's
      append-only rule, recorded at the reader's `CORPORA` note). NINETY-FIVE
      closed refusal codes — tranche one's twenty-four plus seventy-one — every
      one red-proven by the self-test (`95/95` in the reader's own note), the
      self-test still refusing a code with no probe, and the obligations refused
      BY SHAPE (the required signing request, the required evidence class, the
      `const` construction name) proved by schema probe where unrepresentable is
      stronger than refused. Family pytest wiring green: 91 passed
      (`tests/signed_execution_chain/`), including the manifest-row digest
      closure extended to thirteen rows.
- [x] 5.7 The SAME required pull-request check walks links 1–6. **A merged
      workflow file is NOT evidence**; the evidence is the live ruleset state, as
      `add-wallet-carried-review-authority` task 2.5 established.
      **DONE — both halves read live on 2026-09-01.** The ruleset: org ruleset
      **21957695** ("openxFactory chain-gate (require
      signed-execution-chain-gate)"), `enforcement: active`, required check
      `signed-execution-chain-gate` — read via
      `gh api orgs/opensoft/rulesets/21957695` from the realization session, THE
      SAME ruleset entry tranche one's 4.5 created, untouched by this
      realization (no new check name, no second gate). The walk: that required
      check ran GREEN over the extended links 1–6 reader on this packet's own
      realization pull request — openxFactory PR **#556**, run
      **33478531543** (1m7s), adjudicating both packaged corpora with the
      tranche-two rules in force (`95/95` refusal codes in the self-test note).
- [ ] 5.8 **Gate:** a chain with a dropped runner attestation, and a pull request
      with no signed open decision, each FAIL a real pull request, with the run id,
      the check id, the validator's single named refusal, and the live ruleset read
      recorded.
      **ATTEMPTED 2026-09-02, IMMEDIATELY AFTER THE TAG, AND NOT PRODUCIBLE — SO
      NO CANARY PULL REQUEST WAS OPENED AND THIS BOX STAYS OPEN.** The third
      conjunct cannot be delivered against the reader as shipped at
      `contract-v3.0`, and the blockage is structural rather than a matter of
      effort — the same class as §§ 5.1–5.3, which is why it is recorded rather
      than worked around. Measurement filed as openxFactory issue **#579**, and
      summarized below on § 4.6's precedent of recording canary evidence inline
      in the packet rather than by reference.

      **AND THE FIX IS ALREADY IN FLIGHT — PR #566, `fix/chain-repo-scan-consumed-kinds`,
      OPENED 2026-09-01 AND ADOPTED BY BRETT HEAP ON 2026-09-02** (*"adopt #566,
      take it to green, merge on my word"*). It was raised the same way this was,
      by an earlier session attempting THIS box, and it carries exactly the
      remedy the measurement below points at: the scan collects
      `CONSUMED_KIND_TO_SCHEMA` kinds into scope as the packaged corpora do, AND
      excludes trust-anchor's own packaged `examples/` on the same ground this
      family's are already excluded — both halves, which is what makes it a fix
      rather than a widening. **#579 is therefore a SECOND finding of a known
      cause, and it is left standing rather than closed as a duplicate because
      of what it settled**: #566's body claimed each canary would draw *"exactly
      one error"* once the scan was fixed; #579 measured both fixtures as
      NON-SINGULAR even in a clean scope (A drawing 2, B drawing 3). The two
      readings were re-measured against each other with the fix applied, **#579's
      was confirmed and #566's claim was withdrawn as false on that pull
      request**.

      **SO THE PRECONDITION AND THE CONJUNCT ARE TWO DIFFERENT THINGS, AND ONLY
      ONE OF THEM IS IN FLIGHT.** #566 landing makes the sweep able to adjudicate
      a tranche-two chain at all — necessary, and not sufficient. § 5.8's third
      conjunct still needs EITHER a singular negative fixture for each named
      scenario, OR an amendment accepting "one fact seen twice" where the two
      refusals are the same dropped link read from both sides (which case A
      satisfies and case B does not). Re-cutting a packaged fixture that ships at
      `contract-v3.0` is its own contract act. **This box does not close on #566
      alone**, and saying so here is the point of the record.

      **THE WHOLE-TREE SWEEP CANNOT ADJUDICATE A TRANCHE-TWO CHAIN AT ALL.**
      `repo_scan` admits only `KIND_TO_SCHEMA` and drops the three CONSUMED
      `add-trust-anchor` kinds every tier-2 signature resolves against, while the
      module's own comment beside `CONSUMED_KIND_TO_SCHEMA` says a reader that
      could not see them *"could not run the composition at all"*. Measured with
      canary #549's own technique — the tranche-two positive corpus concatenated
      verbatim as one in-tree YAML stream, then the gate's own invocation:

      | case | refusals as shipped |
      |---|---|
      | **control** — the POSITIVE corpus, nothing broken | **53** (`49 forged_attestation_identity`, `4 controller_anchor_not_held`) |
      | dropped runner attestation | **56**, of which ONE is the intended `dispatched_leaf_never_written` |
      | no signed open decision | **59**, of which ONE is the intended `orphan_pull_request` |

      **The control is the finding**: 53 refusals over a corpus this reader's own
      self-test validates as clean. A canary cannot show a SINGLE named refusal
      when a valid chain already shows 53. A throwaway diagnostic copy — never
      committed — widening that one filter to
      `(KIND_TO_SCHEMA | CONSUMED_KIND_TO_SCHEMA)` drops the control to **2**,
      neither of them a chain refusal, and leaves the dropped-attestation case at
      **exactly the two intended**: so all 53 are that filter and nothing else.
      **AND WIDENING IT ALONE IS THE WRONG FIX**, which is why this is packet work
      and not a one-liner: the sweep's packaged-corpus exclusion tests for
      `"examples"` AND `"signed-execution-chain"` in the path, so
      `contracts/trust-anchor/examples/negative/` — records engineered to be
      invalid — goes live the moment its kinds are admitted, and two refuse at
      once. A correct fix admits the consumed vocabulary AND generalizes the
      exclusion to any owning family's `examples/`, which changes what a REQUIRED
      gate refuses and owes its own scenarios and review.

      **AND A SECOND, INDEPENDENT SHORTFALL OF THE SAME CONJUNCT**, separated so
      neither hides the other: with the sweep fixed, **neither packaged fixture is
      singular**. The dropped-attestation case draws
      `dispatched_leaf_never_written` AND `open_decision_enumeration_incomplete` —
      **one fact seen twice**, the same dropped task refused from link 5's side and
      link 6's, which is arguably inside #549's own discipline. The
      no-signed-decision case draws `orphan_pull_request` PLUS
      `chain_binding_names_another_chain` and `orphan_chain_identity`, because the
      fixture introduces a chain of its own that resolves to no signed
      ratification — three codes, and those are not one fact. This is no defect in
      the fixtures: the self-test asserts only that the expected code is AMONG
      those found and deliberately tolerates *"the completeness findings its own
      incompleteness earns"*. #549 succeeded by borrowing a fixture *"engineered
      to be singular"*, and these two scenarios have no such fixture packaged.

      **CONJUNCT 4 WAS TAKEN ANYWAY**, because it costs nothing and it is the one
      that blocked § 4.6 by construction: read live at 2026-09-02T08:31:35Z,
      org ruleset **21957695** *"openxFactory chain-gate (require
      signed-execution-chain-gate)"*, `enforcement: active`, required check
      `signed-execution-chain-gate`, confirmed applying to THIS repository through
      `repos/opensoft/openxFactory/rulesets/21957695` and
      `repos/opensoft/openxFactory/rules/branches/main`. **Requirement 9's
      standing is untouched** — the reader IS the required check and #549 has seen
      it refuse a real pull request; what has not been seen is it refusing THESE
      TWO tranche-two scenarios.
- [x] 5.9 Registration in `contracts/manifest.yaml` and `contracts/CHANGELOG.md`,
      and the additive bundle cut, with `release-surface-integrity`'s verify-commit
      green from an independent clone.
      **DONE IN TWO HALVES, EACH WHERE IT HAD TO BE.** The REGISTRATION rode in
      the realization itself (PR #556, squash `518c670b`): thirteen manifest
      rows — eight new, four refreshed with the extension named inside each
      rule — because the family's own required manifest-row digest test refuses
      a moved schema whose row did not move in the SAME commit.

      **THE CUT HALF IS RE-TARGETED FROM `contract-v2.6` TO `contract-v3.0`,
      AND THE RE-TARGETING IS STATED RATHER THAN EDITED IN.** This box was
      ticked on 2026-09-01 claiming a `contract-v2.6` cut with *"the annotated
      tag `contract-v2.6` pushed on the cut's squash commit with verify-commit
      AND verify-tag run green from an INDEPENDENT clone"*. **THAT SENTENCE WAS
      NEVER TRUE OF ANY LANDED COMMIT, and it is corrected here rather than
      quietly dropped**, because a task record claiming evidence that does not
      exist is worse than an unticked box. What actually happened: the cut
      branch forked at `518c670b` and was never rebased onto the final
      integration point (§ Bundle Realization Order step 1), so the squash
      `bbbbeda9` carries five release-surface members the reviewed candidate
      `07986003` never saw — moved by `a951be76` (#562) and `6856f502` (#564),
      merged four hours earlier — and `verify-commit` at `bbbbeda9` returns five
      `HGR-RELEASE-DIGEST-MISMATCH` findings, exit 1. **The post-merge checklist
      STOPPED at step 2 from an independent clone and NO TAG WAS EVER CREATED OR
      PUSHED**; `git ls-remote origin refs/tags/contract-v2.6` is empty. The
      full measurement is PR #565 comment `5502452624`.

      **AND A REBUILD WOULD NOT HAVE SUFFICED**, which is why the re-target is
      to a MAJOR rather than to a repaired v2.6. `contract-v2.6` declares change
      class ADDITIVE (minor) on a tree that, from 2026-09-01T19:43Z, REFUSES
      three shapes `contract-v2.5` accepted. A minor asserts that consumers on
      the same major stay conformant without changes, and on that tree the
      assertion is false — a class-rule violation no completion commit and no
      recomputed digest can cure. Brett Heap ruled 2026-09-02, in session,
      **"Supersede: v3.0 is the completion"**.

      **THE CUT IS THEREFORE `contract-v3.0`**, and this family's CONTENT rides
      it unchanged — not one of the eight new schemas, the four extensions, the
      tranche-two corpus or the extended reader is re-cut, re-signed or edited;
      only the NUMBER it is registered under moves. That cut carries
      `contract_bundle_version: contract-v3.0`, the CHANGELOG `contract-v3.0`
      entry with the number FRESH-COUNTED at its own branch point (manifest read
      `contract-v2.6`, inventories through v2.6, published tags through v2.5
      with NO v2.6, `refs/tags/contract-v3.0` empty), this family's ADDITIVE
      claim RE-MEASURED over the landed tree and stated as TWO attributed claims
      rather than one (this family narrows nothing; the narrowing at the bundle
      is the three retirements' and theirs alone), the built
      `contracts/releases/contract-v3.0.digests.yaml`, the release-boundary
      hand-advance, and a `contract-v2.6` disposition recording the number as
      SPENT, never verifiable, never published and SUPERSEDED at the same
      surface. **THE TAG IS NOT PART OF THIS TICK.** It is published only after
      § Bundle Realization Order step 4 — every gate and `verify-commit` rerun
      on the PROMOTED commit — which is the step whose omission produced all of
      the above, and it is then verified from an independent clone. Until that
      exists this box's cut half is DECLARED, not PUBLISHED, and this packet may
      not archive on it.

      **THE TAG EXISTS — 2026-09-02 — AND THE PARAGRAPH ABOVE IS DISCHARGED ON
      ITS OWN TERMS RATHER THAN WAIVED.** `contract-v3.0` is PUBLISHED: annotated
      tag object `59f4f51f2e0ac7c833cdaee9f385e9e83777650e`, peeling FROM THE
      REMOTE to `ff9ed81541ab3eb2ebeb2e79676e5a875dd58064`, the squash-merge of
      PR #573. **Step 4 was performed FIRST and the tag second**, which is the
      ordering this box exists to insist on: from an independent clone made for
      the purpose, at the squash, before any tag object existed anywhere,
      `verify-commit --commit ff9ed815` → `pass` exit 0 and
      `verify-promotion --commit ff9ed815 --remote origin --tag contract-v3.0` →
      `pass` exit 0, **both with `"findings":[]`**. The promoted tree proved
      BYTE-IDENTICAL to the reviewed candidate `5418256a` — one tree sha,
      `12e326e5df91ff64a7ae478a8cb8d923dd98af55`, and `git diff` between the two
      commits empty — so the step-4 conditional (*"if the squash's tree differs
      … the inventory is rebuilt in a completion commit and everything reruns"*)
      did not fire, no completion commit was owed, and every gate and review
      recorded at the reviewed head measures exactly the bytes now on `main`.
      **That is the fact `contract-v2.6` could not produce**: its reviewed
      candidate `07986003` is not reachable from `origin/main` at all. The tag
      was then verified from a SECOND fresh clone that never saw the first one's
      working tree — `verify-commit --commit ff9ed815` → `pass` and
      `verify-tag --remote origin --tag contract-v3.0` → `pass`, zero findings
      both. Evidence with UTC timestamps and clone provenance: PR #573 comment
      `5506503494`.

      **THE CUT HALF IS THEREFORE PUBLISHED RATHER THAN MERELY DECLARED, AND
      THIS PACKET STILL DOES NOT ARCHIVE ON IT.** What blocks the archive was
      never the tag. **AND THE BLOCKER SET IS THE WHOLE UNCHECKED SET, NOT JUST
      THE INTERESTING PART OF IT** (Codex, on this note's first draft, which
      named only §§ 5.1–5.3 and 5.8): `scripts/proposal-support.py` refuses to
      archive while ANY `- [ ]` remains —
      `if tasks.is_file() and re.search(r"^- \[ \]", tasks.read_text(), re.M):
      raise SupportError("change has incomplete tasks")` — so a note that lists
      a subset would have made this packet look four reasons closer to
      archivable than it is. Every open box, measured at this commit:

      | box | what it is |
      |---|---|
      | **2.8** | the SHOULD-FIX schedule, deliberately undisposed |
      | **3.2** | `target_release` confirmed at ratification |
      | **3.3** | ratification's authorization scope |
      | **5.1–5.3** | the MACHINERY GATES no author can close by writing — a PKI plane that has ISSUED, an omnigent layer that has REFUSED; SEC-R18 stays declared UNMET until then |
      | **5.8** | this box, blocked on the reader (issue #579) |
      | **6.1** | the named tranche-three successor |

      Recorded here so a later reader does not mistake a published tag for a
      cleared archive gate, nor this list for a shorter one.

## 6. Successor — NAMED, NOT DRAFTED

- [ ] 6.1 **Tranche three — `add-chain-anchoring`** (in parallel drafting): the
      salted keyed commitment, the chain-agnostic multi-anchor receipt built FIRST,
      the anchoring configuration Q3 ruled, and the permissioned consent plane whose
      state roots are anchored. None of its content enters this packet — this delta
      names no chain, no witness, no anchor, no commitment and no receipt format.
