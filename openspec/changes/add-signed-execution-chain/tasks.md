# Tasks: add-signed-execution-chain (tranche one)

Governance-level and dependency-ordered. **This change is not ratified and is
not being implemented now.** §1 is authored in this pull request; **§2 is
Brett's ratification act**; §3 onward are for the implementer and belong to a
single Speckit contract feature. Do not duplicate the executable contract list
here — §5 hands it off.

**THE CLARIFY ROUND THIS FILE USED TO CARRY AS §2 IS DISCHARGED, NOT DROPPED.**
Brett Heap ruled all seven of the staged topic's questions on 2026-08-29 (#499,
squash `9c501df6`) and ruled Narrowing A separately in the same session, so
every box that section held is closed by fact rather than by deletion; §1.9
records the discharge and what each ruling moved. Renumbering the sections after
it is bookkeeping — the discharge is the substance.

Evidence convention, unchanged from the family's standard: a box closes on a
FACT that survives the session — a merged commit, a green run named by id, a
live API read, a file path — never on an intention and never on a workflow file
standing in for a ruleset state.

## 1. Spec deltas and the packet (THIS PULL REQUEST)

- [x] 1.1 `signed-execution-chain` — **NINE ADDED requirements over 42
      scenarios**: wallet-presented ratification proven by possession and BOUND
      to the exact ratification (Q1 **as ruled**, no longer flagged); the
      recorded ACTOR bound to the wallet that signed, in the direction the
      pinned subject-attestation contract fixes; ratification and chain
      inception as ONE signed act, performed out-of-pipeline on the 2026-08-28
      convening's code-level ground, with per-ratification uniqueness ENFORCED
      and the non-collision against 025's "enrollment" stated in requirement
      text; ONE digest construction governing every digest the capability
      computes; the traveling contract, checkable at the point of use; the
      append-only signed transparency log as THE RECORD, with anchors named as
      tranche three, their absence declared not a defect, and the one uncovered
      residual declared; the short-chain gate validating links 1–3 as a
      HASH-LINKED chain, refusing a break as a fraud signal and refusing an
      unevaluable chain; tier-1 RATIFYING authority as human-held per **Brett
      Heap's Narrowing A ruling of 2026-08-29**; and the named-reader
      required-check rule without which none of it confers anything.
- [x] 1.2 NO `## MODIFIED Requirements` block anywhere in this packet, and no
      promoted requirement restated. Composition with `openxwallet`,
      `trust-anchor`, `identity-brokering` and `roles-authority-model` is BY
      REFERENCE, which is the staged topic's own instruction and the condition
      under which its Conflicts table admits this tranche.
- [x] 1.3 `design.md` records the real decisions — the vocabulary act, the
      out-of-pipeline ground, link 7 on the §7.4 path, log-before-anchors, the
      tier-1 narrowing now RULED, and the reading of Q1 now RULED — plus the
      deferral table naming where each deferred item lands, and D8 recording the
      four hardenings harvested from the closed #494.
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

- [x] 1.9 **THE SEVEN RULINGS AND NARROWING A ARE ENCODED**, and the packet no
      longer carries a clarify round. Ruled by Brett Heap 2026-08-29 (#499,
      squash `9c501df6`) plus his in-session Narrowing A ruling of the same day.
      What each one moved:
      **Q1** AS RECOMMENDED — the flag came OUT of requirement 1 and the
      requirement now reads as ruled (a flag left standing after its question is
      ruled is a stale contested marker).
      **Q4** AS RECOMMENDED — the scope section cites the ruling rather than the
      topic's instruction; the transparency-log and short-chain-gate
      requirements were already what Q4 ruled, so nothing moved but the citation.
      **Q5** OVERRIDES its recommendation — the packet's "trigger condition
      still to be stated" line is GONE, because the ruling forbids gating a
      future adoption on any condition written in advance; the compliance is now
      stated positively rather than left to inference.
      **Q2, Q3, Q6, Q7** govern later tranches and are RECORDED, pre-encoded
      nowhere — verified by grep: the delta names no chain, witness, anchor,
      commitment, salt, receipt, attestation mechanism or contract-code posture.
      **Narrowing A** RULED — requirement 8's grounding is now his ruling, dated
      and in-session, and not a narrowing this packet adopted on its own
      authority. **Narrowing B** needed no separate act: Q1's own disposition
      says no new artifact is created for the presentation.
- [x] 1.10 **THE COLLAPSE IS EXECUTED.** Brett Heap ruled 2026-08-29 that this
      packet is the surviving base and #494 is closed. Four of #494's hardenings
      are HARVESTED into the delta (actor↔wallet binding; per-ratification
      uniqueness enforced; one digest construction; the named-reader
      required-check rule) and cited to #494 in `proposal.md` and `design.md` D8,
      so four Codex rounds of work are provably carried rather than lost with
      the branch. One #494 requirement was deliberately NOT carried and the
      reason is recorded — its every-link-signs formulation cannot be performed
      on any link this tranche defines.
- [x] 1.11 The staged fragment and `ideation/staging/INDEX.md` record the
      drafting GREEN-LIGHT, the collapse and Narrowing A. The sitting's own
      "drafting was NOT green-lit" sentence is LEFT STANDING with the later word
      recorded beneath it — rewriting it to agree would delete the distinction
      the sitting was careful to draw.

## 2. Ratification gate — Brett Heap's act

**This is the only gate left before realization.** The drafting green-light he
gave on 2026-08-29 is NOT this; it authorized the packet's existence and nothing
in its text.

- [ ] 2.1 Brett ratifies proposal, design and the delta. **Ratification of this
      packet authorizes tranche one only** and creates no attestation identity,
      no certificate authority, no anchor and no chain.
- [ ] 2.2 Confirm `target_release`. It is named **`contract-v2.3`**,
      FRESH-COUNTED at this branch's tip — `contracts/manifest.yaml:3` declares
      `contract-v2.2` and `contracts/releases/contract-v2.2.digests.yaml` is a
      cut inventory in the tree, so v2.2 is spent. It stays ALLOCATED AT
      REALIZATION by merge order per `docs/contract-versioning-policy.md`, and
      the realization re-counts against the manifest at ITS tip rather than
      trusting this line.
- [ ] 2.3 On ratification, set front-matter `Status: ratified` and add the
      `Ratified:` line naming approver, date and a resolvable record path, per
      the `sanction-ratified-record-spelling` three-way floor.

## 3. Settle before schemas are authored

Both are contract content, cheap now and expensive after a bundle ships. The
`openxwallet` custody enumeration is the standing precedent for how quietly a
wrong set re-opens the hole the rule was written to close.

- [ ] 3.1 Fix the **chain-identity digest** — algorithm, and the exact byte
      range of the signed ratification it covers. A chain identity whose
      derivation is ambiguous cannot be validated for continuity, which is the
      whole of the gate's job.
- [ ] 3.2 Fix the **leaf grammar** — what a transparency-log leaf carries, how
      leaves hash-link, and what a verifier reads to detect an edit. Chosen
      against RFC-6962 / Rekor rather than invented, per the vendored study.
- [ ] 3.3 Decide the **log's home** — the register precedent (a
      repository-tracked file whose READER is the shape) or a governed store
      outside the tree. `design.md` deliberately leaves this open; it must not
      reach schema authoring open.

## 4. Realization — ONE Speckit contract feature

- [ ] 4.1 `contracts/signed-execution-chain/` — the chain-inception record, the
      traveling-contract artifact, the transparency-log leaf, and the
      realization conformance declaration on `trust-anchor`'s declared-shortfall
      pattern.
- [ ] 4.2 Packaged POSITIVE and NEGATIVE examples for every named refusal:
      missing proof, failed verification, revoked-at-exercise, orphan chain
      identity, digest mismatch on the traveling contract, mix-and-match
      continuity, missing link, unevaluable chain, machine holder as ratifying
      authority.
- [ ] 4.3 `scripts/validate-signed-execution-chain.py` — the canonical
      validator, refusing each negative example by name.
- [ ] 4.4 The short-chain GATE as a running pull-request check, not a described
      one.
- [ ] 4.5 **[OPERATOR]** Make the check REQUIRED in the branch ruleset. A merged
      workflow file is NOT evidence; the evidence is the live ruleset state, as
      `add-wallet-carried-review-authority` task 2.5 established (org ruleset
      **21538893** for `wallet-validation`).
- [ ] 4.6 **Gate:** a deliberately broken chain FAILS a real pull request, and
      the evidence records the run id, the check id, the validator's single
      named refusal, and the live ruleset read showing the check required —
      the shape task 2.6 of that change proved on canary PR #387.
- [ ] 4.7 Registration in `contracts/manifest.yaml` and
      `contracts/CHANGELOG.md`, and the additive bundle cut, with
      `release-surface-integrity`'s verify-commit green from an independent
      clone.

## 5. Successors — NAMED, NOT DRAFTED

- [ ] 5.1 **Tranche two** — links 4–6 and 10: harness-controller setup
      attestation, per-task attestation identities whose keys never enter a
      worker, the signed PR-open decision, the governed post-merge test, the
      closure invariant AND the remediation exemption, and the
      controller-does-not-notarize-self-report binding. Needs the omnigent layer
      and `implement-openxpki-install-repo`. Contract text gated on **Q7**.
- [ ] 5.2 **Tranche three** — on-chain anchoring: the salted keyed commitment,
      the chain-agnostic multi-anchor receipt built FIRST, and the permissioned
      consent plane whose state roots are anchored. Gated on rulings for **Q3**
      and **Q6**.
- [ ] 5.3 Neither successor's content enters this packet. Re-derive the tranche
      two/three boundary against what actually exists when each is raised, per
      the topic's Q4 — a tranche that depends on an unbuilt layer is a plan, not
      a tranche.
