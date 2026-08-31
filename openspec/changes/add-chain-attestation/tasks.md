# Tasks: add-chain-attestation (tranche two)

Governance-level and dependency-ordered. **This change is a DRAFT.** §1 is the
pull request. **§2 (the §7.4 council review) and §3 (Brett Heap's ratification)
are the two gates that stand between it and any realization, in that order.**
**§2 IS HELD AND DISCHARGED — the sitting of 2026-08-30, its thirteen blocking
amendments, and the fix round that landed them. §3 HAS NOT HAPPENED and is the
next act.** §4 settles what must not reach schema authoring open; §5 is
the realization commission and is gated on machinery that does not yet exist.

Evidence convention, unchanged from the family's standard: a box closes on a FACT
that survives the session — a merged commit, a green run named by id, a live API
read, a file path — never on an intention and never on a workflow file standing
in for a ruleset state.

## 1. Spec deltas and the packet (THIS PULL REQUEST)

- [x] 1.1 `signed-execution-chain` — **NINE ADDED requirements over 102
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
- [x] 1.2 **ONE `## MODIFIED Requirements` block**, carrying tranche one's gate
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
      record. The consumed record now SHALL NAME THIS CHAIN'S IDENTITY. (iii) and
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
      prevent. (ii) **THE SIGNED ORDER WAS OUTRUN AGAIN, BY A KIND THIS PACKET
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

## 3. RATIFICATION GATE — **NEXT.** Brett Heap's act, NOT YET TAKEN

- [ ] 3.1 Ratification by Brett Heap. **The review is HELD and the fix round it
      forced is LANDED (§2), so this is the next act on this packet** — the
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

- [ ] 4.1 Fix the **signing-request record shape**, for BOTH SUBJECT SCOPES — a
      field on the record or a sibling record it references, for the task-scoped
      link-5 request AND for the chain-scoped link-6/link-10 request. The
      requirement fixes for each that it is recorded alongside the signature, that
      the request is ATTRIBUTED (to the provisioned task; to the party the chain's
      inception record binds), and that absence is refused — not its shape.
- [ ] 4.2 Fix the **evidence-class vocabulary's closure** — whether
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
- [ ] 4.3 Fix **what a setup attestation enumerates** — how the model surface, the
      harness and its version, the toolchain and the workspace provenance are each
      expressed.
- [ ] 4.4 Fix the **ordering key for the plural-predecessor enumeration**, settled
      WITH tranche one's single digest construction and never beside it.
- [ ] 4.5 Confirm the extended gate stays **ONE required check walking further**,
      never a second gate.
- [ ] 4.6 Fix the **per-task reference** the expected attestation set is written
      in — the value link 4 commits to and the link-5 attestation carries back,
      settled WITH tranche one's single digest construction and never beside it.
      The requirement fixes that the reference is STABLE, that it falls inside the
      controller's signed bytes, and that an attestation for an uncommitted task
      is refused; it does not fix the reference's shape. **The extension record's
      own shape rides with it**, since an extension is the same commitment written
      later, and both are refused if the reference cannot be matched.
- [ ] 4.7 Fix the **chain-scoped identity's issuance and lifetime** — when the
      controller mints the one chain-scoped tier-2 identity per chain, and when it
      is destroyed. The requirement fixes that there is EXACTLY ONE per chain
      identity, that it is ephemeral, that its key stays at the controller's
      signing boundary, and that its authorized record kinds are links 6 and 10
      and nothing else; it does not fix the mint point. Settled WITH the per-task
      identities' lifetime and never beside it, since both are tier 2 under one
      custody rule.

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
- [ ] 5.4 `contracts/signed-execution-chain/` gains the setup-attestation record
      **carrying its committed expected attestation set**, the
      **controller-signed commitment-extension record**, the runner-attestation
      record together with the signing-request record, the PR-open decision
      record, the closure record, the remediation declaration, **the SIGNED CHAIN
      BINDING record** — this capability's seventh record kind, carrying a tier-2
      identity's SUBJECT SCOPE, its CLOSED RECORD-KIND ENUMERATION and THE CHAIN
      IDENTITY IT SERVES, and referencing by identifier the two CANONICAL
      `add-trust-anchor` records it composes with (`certificate-record` for the
      key and validity bounds, `issuance-evidence` for the issuance act), **both
      CONSUMED AND NEITHER REDEFINED HERE** — the per-fact evidence class, **THE
      SIGNER'S PUBLIC KEY CARRIED BESIDE EVERY SIGNATURE** on every record this
      capability defines (the field verification resolves against the consumed
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
- [ ] 5.5 Packaged POSITIVE and NEGATIVE examples for every named refusal: no
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
      replayed, refused because it does not name this chain's identity; an
      **record chaining from anything other than its actual nearest prior in-force
      record**, refused as a break; a **tier-2 certificate record with no
      `subject.public_key_fingerprint`**, refused; a **signing key whose computed
      fingerprint does not EQUAL the certificate's**, refused as a forged
      identity; a **controller-signed link-4 or extension record supplying its own
      key against a controller certificate with NO fingerprint**, refused; and
      POSITIVES for **the verification key resolving against the certificate**,
      for **records under a compliant CONTROLLER certificate verifying**, for **a review written BEFORE ratification closing its own chain through the equality chain**, for **a late-dispatched task's SIGNED CHAIN BINDING descending from the actual latest signed record**, and for **a later task dispatched after an earlier task has
      attested** — the extension chaining from that link-5 record and the gate
      walking the interleaved order; and
      two POSITIVES — **a genuine tier-2 identity's THREE records verifying end to
      end** (certificate valid and current, issuance evidenced, chain binding
      naming this chain and this scope — then the signature, then the link's own
      checks) and **a chain
      with commitment extensions walked for continuity** over
      4 → x₁ → … → xₙ → 5 → 6 → 10.

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

      **THE SECOND ROUND'S POSITIVE FIXTURE IS WITHDRAWN AND THE WITHDRAWAL IS
      NAMED.** It required *"the positive case of that identity signing its task's
      link-6 and link-10 records"* — a per-task identity signing links 6 and 10 —
      which the third round's closed enumeration makes IMPOSSIBLE and explicitly
      refuses. Building it would have forced the validator to accept a
      now-forbidden signature or left this task uncompletable. The chain-scoped
      positive case above replaces it.
- [ ] 5.6 `scripts/validate-signed-execution-chain.py` extended — one named
      refusal per negative example above.
- [ ] 5.7 The SAME required pull-request check walks links 1–6. **A merged
      workflow file is NOT evidence**; the evidence is the live ruleset state, as
      `add-wallet-carried-review-authority` task 2.5 established.
- [ ] 5.8 **Gate:** a chain with a dropped runner attestation, and a pull request
      with no signed open decision, each FAIL a real pull request, with the run id,
      the check id, the validator's single named refusal, and the live ruleset read
      recorded.
- [ ] 5.9 Registration in `contracts/manifest.yaml` and `contracts/CHANGELOG.md`,
      and the additive bundle cut, with `release-surface-integrity`'s verify-commit
      green from an independent clone.

## 6. Successor — NAMED, NOT DRAFTED

- [ ] 6.1 **Tranche three — `add-chain-anchoring`** (in parallel drafting): the
      salted keyed commitment, the chain-agnostic multi-anchor receipt built FIRST,
      the anchoring configuration Q3 ruled, and the permissioned consent plane whose
      state roots are anchored. None of its content enters this packet — this delta
      names no chain, no witness, no anchor, no commitment and no receipt format.
