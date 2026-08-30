# Tasks: add-chain-attestation (tranche two)

Governance-level and dependency-ordered. **This change is a DRAFT.** §1 is the
pull request. **§2 (the §7.4 council review) and §3 (Brett Heap's ratification)
are the two gates that stand between it and any realization, in that order**, and
neither has happened. §4 settles what must not reach schema authoring open; §5 is
the realization commission and is gated on machinery that does not yet exist.

Evidence convention, unchanged from the family's standard: a box closes on a FACT
that survives the session — a merged commit, a green run named by id, a live API
read, a file path — never on an intention and never on a workflow file standing
in for a ruleset state.

## 1. Spec deltas and the packet (THIS PULL REQUEST)

- [x] 1.1 `signed-execution-chain` — **NINE ADDED requirements over 59
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
- [x] 1.2 NO `## MODIFIED Requirements` block anywhere in this packet, and no
      promoted requirement restated. Composition with `add-trust-anchor`,
      `add-identity-brokering`, `implement-openxpki-install-repo`,
      `contracts/omnigent/` and tranche one's `add-signed-execution-chain` is BY
      REFERENCE. `design.md` D3 records why the gate extension is ADDED rather than
      MODIFIED, and names the scenario-complete restatement as the repair if the
      council rules the composition insufficient.
- [x] 1.3 `design.md` records the real decisions — Q7 as the ruled mechanism and
      what it does NOT settle; corroborate-versus-notarize with the per-FACT
      evidence class; the ADDED-not-MODIFIED gate composition; the plural-predecessor
      enumeration that fills a gap in the topic; the HSM as deferred hardening; the
      revocation horizon as this packet's own decision; Q4's re-derivation
      instruction routed to the council; the deferral table; and the five open
      design points that must not reach schema authoring open.
- [x] 1.4 `OPENSPEC_TELEMETRY=0 openspec validate add-chain-attestation --strict`
      green and `--all --strict` green before commit; counts recorded in the pull
      request body.
- [x] 1.5 doc-health zero-new against `origin/main`, baseline worktree basename
      matching the working clone's (issue #342 — a mismatched-identity
      `--previous-report` manufactures phantom regressions).
- [x] 1.6 README "OpenSpec Records" active block updated, newest first.
- [x] 1.7 `ideation/staging/INDEX.md` — the topic's detail section records that
      EXIT 2 has been raised as an active change. The row is NOT marked
      `Exit taken:`, on the same ground tranche one recorded: that record silences
      the `staged-candidate-aging` family only when it names an ARCHIVED change, and
      the topic must keep ageing while tranche three is unraised.
- [x] 1.8 **THE THREE PULLS BETWEEN A RULED INPUT AND AN ARTIFACT ARE RECORDED,
      NOT SMOOTHED**, per the family's contested-finding rule: Q4's re-derivation
      instruction versus drafting this tranche now (routed to the council,
      unresolved here); tranche one's gate scope note versus the extended walk
      (read as self-limiting, the reading written into requirement text and
      reported); and the topic's SINGULAR hash-link rule versus its PLURAL link 5
      (resolved here by addition, and flagged as this packet's own resolution).
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

## 2. §7.4 COUNCIL REVIEW — the first gate, NOT YET HELD

The council-reviewed-but-human-approved path that per the 2026-08-26 record §7.4
needs no candidate class and no flip, and reaches this repository without an
envelope and without amending FR-008. This packet creates no
`merge-approval-envelope` and declares no candidate class.

- [ ] 2.1 Convene the §7.4 sitting on this packet, OUTSIDE the codexFactory
      clearance-envelope pipeline, mirroring the procedure
      `add-binding-consumer-identity` ran on 2026-08-29 — the first packet through
      that path end to end.
- [ ] 2.2 The sitting rules FIRST on **Q4's re-derivation instruction versus
      drafting tranche two before the omnigent layer and the PKI plane are real**
      (`design.md` D7; `proposal.md`, first substantive section). A ruling that the
      packet is premature ends the round; nothing below it survives.
- [ ] 2.3 The sitting rules on **the ADDED-not-MODIFIED gate composition**
      (`design.md` D3). If it rules the composition insufficient, the named repair
      is a SCENARIO-COMPLETE MODIFIED restatement of tranche one's gate
      requirement — all twelve scenarios, not the two that change — and the packet
      takes a fix round.
- [ ] 2.4 The sitting rules on **the plural-predecessor enumeration** (`design.md`
      D4), which is this packet's own resolution of a gap in the ruled topic rather
      than a ruling encoded.
- [ ] 2.5 The sitting rules on **the revocation-after-signing horizon**
      (`design.md` D6), likewise this packet's own decision.
- [ ] 2.6 The review record lands in `review/`, mirroring
      `add-binding-consumer-identity`'s directory, and names each seat, each
      blocking amendment, and the verdict word.

## 3. RATIFICATION GATE — Brett Heap's act, NOT YET TAKEN

- [ ] 3.1 Ratification by Brett Heap after the review and any fix round it
      forces, with the record at `review/ratification-<date>.md` and front-matter
      `Status: ratified` plus a `Ratified:` line naming approver, date and a
      resolvable record path, per the `sanction-ratified-record-spelling` three-way
      floor.
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
      `controller_corroborated` / `hardware_attested` / `runner_claimed` is a CLOSED
      set at the schema, and what a fourth class would have to establish.
- [ ] 4.3 Fix **what a setup attestation enumerates** — how the model surface, the
      harness and its version, the toolchain and the workspace provenance are each
      expressed.
- [ ] 4.4 Fix the **ordering key for the plural-predecessor enumeration**, settled
      WITH tranche one's single digest construction and never beside it.
- [ ] 4.5 Confirm the extended gate stays **ONE required check walking further**,
      never a second gate.

## 5. Realization — ONE Speckit contract feature, GATED ON MACHINERY

**Both gates are hard and neither is discharged by ratification.**

- [ ] 5.1 **[GATE] Re-derive the tranche boundary against what actually exists**
      when the omnigent layer and the PKI plane are real, per Q4's ruling. This
      obligation survives ratification deliberately: a packet cannot discharge it,
      because it is an obligation about a state the packet cannot observe.
- [ ] 5.2 **[GATE] `implement-openxpki-install-repo` real enough to issue a
      controller certificate**, with the issuance evidence `add-trust-anchor`
      requires, and with any shortfall DECLARED under its conformance-declaration
      rule rather than asserted.
- [ ] 5.3 **[GATE] The omnigent layer real enough to enforce a precondition.**
      Until a running layer refuses, requirement 9 is UNMET rather than partially
      met, and this packet claims no enforcement it cannot name a check for.
- [ ] 5.4 `contracts/signed-execution-chain/` gains the setup-attestation record,
      the runner-attestation record together with the signing-request record, the
      PR-open decision record, the closure record, the remediation declaration, and
      the per-fact evidence class.
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
      verify, and execute-then-verify.
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
