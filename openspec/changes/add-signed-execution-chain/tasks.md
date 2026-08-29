# Tasks: add-signed-execution-chain (tranche one)

Governance-level and dependency-ordered. **This change is not ratified and is
not being implemented now.** §1 is authored in this pull request; **§2 is the
clarify round and it PRECEDES ratification**; §3 is Brett's ratification act;
§4 onward are for the implementer and belong to a single Speckit contract
feature. Do not duplicate the executable contract list here — §6 hands it off.

Evidence convention, unchanged from the family's standard: a box closes on a
FACT that survives the session — a merged commit, a green run named by id, a
live API read, a file path — never on an intention and never on a workflow file
standing in for a ruleset state.

## 1. Spec deltas and the packet (THIS PULL REQUEST)

- [x] 1.1 `signed-execution-chain` — SIX ADDED requirements: wallet-presented
      ratification proven by possession (carrying Q1's recommended answer
      FLAGGED); ratification and chain inception as ONE signed act, performed
      out-of-pipeline on the 2026-08-28 convening's code-level ground, with the
      non-collision against 025's "enrollment" stated in requirement text; the
      traveling contract, checkable at the point of use; the append-only signed
      transparency log as THE RECORD, with anchors named as tranche three and
      their absence declared not a defect; the short-chain gate validating
      links 1–3 as a HASH-LINKED chain, refusing a break as a fraud signal and
      refusing an unevaluable chain; and tier-1 RATIFYING authority as
      human-held, narrowed against a realized agent-held review wallet.
- [x] 1.2 NO `## MODIFIED Requirements` block anywhere in this packet, and no
      promoted requirement restated. Composition with `openxwallet`,
      `trust-anchor`, `identity-brokering` and `roles-authority-model` is BY
      REFERENCE, which is the staged topic's own instruction and the condition
      under which its Conflicts table admits this tranche.
- [x] 1.3 `design.md` records only the six real decisions — the vocabulary act,
      the out-of-pipeline ground, link 7 on the §7.4 path, log-before-anchors,
      the tier-1 narrowing, and the reading of Q1 — plus the deferral table
      naming where each deferred item lands.
- [x] 1.4 `OPENSPEC_TELEMETRY=0 openspec validate add-signed-execution-chain
      --strict` green and `--all --strict` green before commit; counts recorded
      in the pull-request body.
- [x] 1.5 doc-health zero-new against `origin/main`, baseline worktree basename
      matching the working clone's (issue #342 — a mismatched-identity
      `--previous-report` manufactures phantom regressions).
- [x] 1.6 README "OpenSpec Records" active block updated, newest first.
- [x] 1.7 The staged topic's primary fragment gains its `Staging ID:` header so
      the packet's `staged` origin RESOLVES. Recorded as a real repair, not
      bookkeeping: `doc-health`'s `proposal-origin` family raises
      `staged-origin-unresolvable` for an ACTIVE change whose staging folder
      exists and carries no document with a matching `Staging ID:`, and the
      topic was registered without one.
- [x] 1.8 `ideation/staging/INDEX.md` — the topic's detail section records that
      EXIT 1 has been raised as an active change. The row is NOT marked
      `Exit taken:`, deliberately: that record silences the
      `staged-candidate-aging` family only when it names an ARCHIVED change,
      and the topic must keep ageing while tranches two and three are unraised.

## 2. The clarify round — PRECEDES RATIFICATION

Brett's standing clarify rules govern the presentation: the full block goes to a
file in this change directory AND to the terminal in block form, with the file's
absolute path echoed at the TOP and again at the BOTTOM of the reply.

- [ ] 2.1 Author `clarify-questions.md` in this change directory carrying all
      SEVEN of the staged topic's questions in one block, each with its context,
      its recommended answer, and its bearing on this tranche.
- [ ] 2.2 Put the block to Brett. **Q1 is the only blocker for tranche one**;
      Q3 and Q6 gate tranche three, Q7 gates tranche two, and Q2/Q4/Q5 travel
      with them so the sitting is complete rather than repeated.
- [ ] 2.3 Carry the TWO flagged narrowings in the same round, named as
      narrowings rather than folded into Q1's text: (a) tier 1 narrowed to
      RATIFYING authority, because the literal topic text refuses the realized
      `wal-agent-mrc-0001` review wallet; (b) Q1's "rather than a new artifact"
      read as "invent no new artifact", honoured by referencing the shipped
      `xfactory_wallet_grant_exercise`.
- [ ] 2.4 Encode the answers back into `proposal.md` and the delta. **If Q1 is
      ruled otherwise, requirement 1 is the text that moves**, and the Q1 flag
      comes OUT of the requirement body at the same commit — a flag left
      standing after its question is ruled is a stale contested marker.
- [ ] 2.5 Update the staged topic's `## Open questions` dispositions in place,
      so the topic and the packet do not diverge on what is still open.

## 3. Ratification gate — Brett Heap's act

- [ ] 3.1 Brett ratifies proposal, design and the delta, having ruled Q1 and the
      two narrowings. **Ratification of this packet authorizes tranche one
      only** and creates no attestation identity, no certificate authority, no
      anchor and no chain.
- [ ] 3.2 Confirm or correct `target_release`. It is PROVISIONAL as filed — the
      next additive bundle after `contract-v2.1`, unnumbered, allocated at
      realization by merge order per `docs/contract-versioning-policy.md`.
- [ ] 3.3 On ratification, set front-matter `Status: ratified` and add the
      `Ratified:` line naming approver, date and a resolvable record path, per
      the `sanction-ratified-record-spelling` three-way floor.

## 4. Settle before schemas are authored

Both are contract content, cheap now and expensive after a bundle ships. The
`openxwallet` custody enumeration is the standing precedent for how quietly a
wrong set re-opens the hole the rule was written to close.

- [ ] 4.1 Fix the **chain-identity digest** — algorithm, and the exact byte
      range of the signed ratification it covers. A chain identity whose
      derivation is ambiguous cannot be validated for continuity, which is the
      whole of the gate's job.
- [ ] 4.2 Fix the **leaf grammar** — what a transparency-log leaf carries, how
      leaves hash-link, and what a verifier reads to detect an edit. Chosen
      against RFC-6962 / Rekor rather than invented, per the vendored study.
- [ ] 4.3 Decide the **log's home** — the register precedent (a
      repository-tracked file whose READER is the shape) or a governed store
      outside the tree. `design.md` deliberately leaves this open; it must not
      reach schema authoring open.

## 5. Realization — ONE Speckit contract feature

- [ ] 5.1 `contracts/signed-execution-chain/` — the chain-inception record, the
      traveling-contract artifact, the transparency-log leaf, and the
      realization conformance declaration on `trust-anchor`'s declared-shortfall
      pattern.
- [ ] 5.2 Packaged POSITIVE and NEGATIVE examples for every named refusal:
      missing proof, failed verification, revoked-at-exercise, orphan chain
      identity, digest mismatch on the traveling contract, mix-and-match
      continuity, missing link, unevaluable chain, machine holder as ratifying
      authority.
- [ ] 5.3 `scripts/validate-signed-execution-chain.py` — the canonical
      validator, refusing each negative example by name.
- [ ] 5.4 The short-chain GATE as a running pull-request check, not a described
      one.
- [ ] 5.5 **[OPERATOR]** Make the check REQUIRED in the branch ruleset. A merged
      workflow file is NOT evidence; the evidence is the live ruleset state, as
      `add-wallet-carried-review-authority` task 2.5 established (org ruleset
      **21538893** for `wallet-validation`).
- [ ] 5.6 **Gate:** a deliberately broken chain FAILS a real pull request, and
      the evidence records the run id, the check id, the validator's single
      named refusal, and the live ruleset read showing the check required —
      the shape task 2.6 of that change proved on canary PR #387.
- [ ] 5.7 Registration in `contracts/manifest.yaml` and
      `contracts/CHANGELOG.md`, and the additive bundle cut, with
      `release-surface-integrity`'s verify-commit green from an independent
      clone.

## 6. Successors — NAMED, NOT DRAFTED

- [ ] 6.1 **Tranche two** — links 4–6 and 10: harness-controller setup
      attestation, per-task attestation identities whose keys never enter a
      worker, the signed PR-open decision, the governed post-merge test, the
      closure invariant AND the remediation exemption, and the
      controller-does-not-notarize-self-report binding. Needs the omnigent layer
      and `implement-openxpki-install-repo`. Contract text gated on **Q7**.
- [ ] 6.2 **Tranche three** — on-chain anchoring: the salted keyed commitment,
      the chain-agnostic multi-anchor receipt built FIRST, and the permissioned
      consent plane whose state roots are anchored. Gated on rulings for **Q3**
      and **Q6**.
- [ ] 6.3 Neither successor's content enters this packet. Re-derive the tranche
      two/three boundary against what actually exists when each is raised, per
      the topic's Q4 — a tranche that depends on an unbuilt layer is a plan, not
      a tranche.
