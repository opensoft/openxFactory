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

- [x] 1.1 `signed-execution-chain` — **NINE ADDED requirements over 76
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
      `--previous-report` manufactures phantom regressions). **ZERO-NEW HOLDS FOR
      EVERY AUTHORED BYTE OF THIS PACKET. IT DOES NOT HOLD FOR THE FILED SITTING
      BUNDLE, AND THAT IS RECORDED RATHER THAN TICKED THROUGH.** Filing
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
      doc-health/spec.md`, same requirement). The five findings are therefore
      reported as a KNOWN, EXPLAINED DELTA for the convener, and the resolution is
      owed as its own change rather than improvised here.
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
      set derived from tranche one's log by a defined query, and review authority
      in `add-wallet-carried-review-authority`'s shipped vocabulary — and each
      carries its residual DECLARED rather than closed.
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

- [ ] 4.1 Fix the **signing-request record shape** — a field on the link-5
      attestation or a sibling record it references. The requirement fixes that it
      is recorded alongside the signature and refuses its absence, not its shape.
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
      record, the closure record, the remediation declaration, the per-fact
      evidence class, and the **closed enumeration of record kinds a per-task
      tier-2 identity may sign**.
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
      expectation, a tier-2 identity offered for a record kind outside its closed
      enumeration, and the positive case of that identity signing its task's
      link-6 and link-10 records.
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
