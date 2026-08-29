# Tasks: add-signed-execution-chain (tranche one)

Governance-level and dependency-ordered. **§1 is this packet.** §2 onward is
realization, which runs after ratification and is what the archive gate measures
(`release-realization`: a change carrying a code surface archives only on merged
plus green realization evidence). §5 is the reserved-questions ledger and is NOT
work — it exists so that two questions held for Brett's clarify sitting cannot be
quietly answered by an implementer.

## 1. The proposal packet (THIS CHANGE)

- [x] 1.1 `signed-execution-chain` — TEN ADDED requirements, tranche one only:
      the ratification as a verified, key-attributed grant exercise with the
      standing-authority origin declared rather than exempted (R1); ratification
      and CHAIN ENROLLMENT as one signed act with neither half standing alone
      (R2); the chain identity as the digest of the signed ratification, fixed
      once (R3); every successor link signing the chain identity and its
      predecessor's digest (R4); the chain travelling with the work and
      verifiable at the point of use (R5); a gap refused as a fraud signal and
      never downgraded, binding validating consumers and naming no gate (R6); the
      append-only signed log in the governed store as THE record (R7); no second
      identity, certificate or custody vocabulary, and never bare "enrollment"
      (R8); the handshake performed outside the clearance pipeline and conferring
      no clearance (R9); and nothing conferred or refused until a named reader
      runs as a required check (R10).
- [x] 1.2 NO MODIFIED delta on any existing capability — a decision recorded at
      design D7 with its three grounds, not an omission. The openxFactory
      lifecycle binding is task 3.3, performed when the reader exists.
- [x] 1.3 NO staged file moves. Partial promotion of ZERO files: both documents
      in `ideation/staging/signed-execution-chain/` stay staged for tranches two
      and three. The primary fragment gains the `Staging ID:` header the origin
      contract requires at the proposal transition; the vendored
      `chain-selection-study.md` is not edited at all.
- [x] 1.4 `ideation/staging/INDEX.md` — the topic's row and detail section record
      that tranche one was raised and that tranches two and three stay staged,
      in this packet's own commit.
- [x] 1.5 `README.md` — one entry in the OpenSpec Records active block.
- [x] 1.6 `OPENSPEC_TELEMETRY=0 openspec validate add-signed-execution-chain
      --strict` green, and `--all --strict` green before commit.
- [x] 1.7 doc-health against a fresh `origin/main` baseline with ZERO new
      findings attributable to this packet, compared at matching identity
      `(family, repo, path)`.

## 2. Realization — the contract family

- [ ] 2.1 `contracts/signed-execution-chain/` — ONE record kind,
      `xfactory_execution_chain_link`, carrying: the chain identity; the link's
      ordinal and kind; the predecessor link digest (absent exactly on the genesis
      link); the declared chain ORIGIN (`wallet_exercise` | `standing_authority`,
      per R1); a reference to the `xfactory_wallet_grant_exercise` by
      `exercise_id` for a `wallet_exercise` origin; the actor as
      `identity-brokering`'s stable opaque subject; the signature block naming
      what the signature covers; and the evidence-plane leaf reference. **No field
      is added to any openXwallet schema** (design D4) — the wallet family is
      consumed at `wallet-v1.3` through `contracts/openxwallet-pin.yaml`, its
      exercise schema is `additionalProperties: false`, and an extension there is
      a publisher-side change plus a pin bump.
- [ ] 2.2 Packaged conformance examples: a positive genesis link; a positive
      successor link; and one NEGATIVE fixture per named refusal — grant presented
      without proof of possession; signature present and failing verification
      (distinct from no signature at all); unattributed act reaching its surface
      through a shared credential; grant revoked before exercise; second genesis
      link under an existing chain identity; successor link signing neither the
      chain identity nor its predecessor; links from different executions offered
      as one chain; carried copy not reproducing its chain identity; a chain link
      carrying its own actor identifier instead of the opaque subject; a leaf
      rewritten in place rather than superseded; and an undeclared chain origin
      offered for a signature-rooted assurance.
- [ ] 2.3 `scripts/validate-signed-execution-chain.py` — reads the family, refuses
      every fixture in 2.2, and refuses a chain it cannot evaluate rather than
      passing it (R6).
- [ ] 2.4 Register the family in `contracts/manifest.yaml` and
      `contracts/CHANGELOG.md` at the next additive bundle cut. The train is at
      `contract-v2.1` (declared at `contracts/manifest.yaml:3`, cut and tagged
      2026-08-28), so the next additive is `contract-v2.2` — **allocated at
      realization by merge order** per `docs/contract-versioning-policy.md`, and a
      sibling packet reaching the cut first does not renumber this one.
- [ ] 2.5 Verify the cut with the release-surface machinery
      (`release-surface-integrity` / `verify-commit`) before the tag moves, so the
      family's registration does not drift a bundle member.

## 3. Realization — the reader, without which R10 says the family confers nothing

- [ ] 3.1 Wire `scripts/validate-signed-execution-chain.py` into a workflow as a
      REQUIRED check on this repository. Until this box is ticked, R10's first
      scenario is the capability's true state and every statement of what the
      chain enforces must say so.
- [ ] 3.2 The evidence plane: choose and stand up the append-only signed log
      inside the governed store (R7 states the properties and names no
      implementation; the choice is realization's, and it is owed here).
- [ ] 3.3 The openxFactory-lifecycle binding deferred at design D7 — the change
      that makes a ratified openxFactory proposal carry its chain. Raised only
      once 3.1 and 3.2 exist, so the binding is true on the day it promotes rather
      than aspirational.

## 4. Successors, named so the tranche boundaries are on the record

- [ ] 4.1 `extend-signed-execution-chain-attestation` (tranche two) — links 4, 5,
      6 and 10; the two-horizon enforcement model; the unclosed-chain refusal with
      the remediation chain as its ONE exempt consumer; and the controller's
      obligation to bind submitted claims against its own setup attestation rather
      than notarize self-report. GATED on Q7, on the omnigent layer enforcing the
      precondition, and on `implement-openxpki-install-repo`.
- [ ] 4.2 `extend-signed-execution-chain-anchoring` (tranche three) — the public
      anchoring layer, the salted keyed commitments, the consent-log checkpoints,
      the permissioned consent plane, the multi-anchor receipt format, and the
      refusing boundary validator Q2 recommends. GATED on Q3 and Q6.
- [ ] 4.3 Domain realizations, in their own repositories: codexFactory's lane,
      MedxFactory's HealthLinc, LedgerxFactory's LedgerLinc. "Merge" is
      domain-interpreted and the neutral family says nothing about which act it is.

## 5. RESERVED — held for Brett's clarify sitting, NOT to be answered here

These two rows are a ledger, not work. They exist because an implementer reading
this packet must be able to see that the questions are open BY DECISION.

- [ ] 5.1 **Q6 — does "patients put PHI portions on chain" mean commitments?**
      OPEN. GATES TRANCHE THREE. The staged topic reads the 2026-08-27 ruling as
      salted keyed commitments — a verifiable handle to a PHI portion anchored
      publicly, with the portion disclosed off-chain under an anchored consent
      checkpoint — and raises the narrowing rather than assuming it, because a
      topic must not quietly narrow a ruling. **Do not decide this in any tranche
      of this family.** Tranche one is independent of the answer, and the proof is
      recorded at design.md § "Proving tranche one is Q6/Q7-independent".
- [ ] 5.2 **Q7 — where does an attestation signature physically happen?** OPEN.
      GATES TRANCHE TWO's contract text. Remote signing served by the harness
      controller, a co-process holding the key behind an attested boundary, and a
      hardware-backed signer are all consistent with the ratified
      `access_secrets: false` constraint and differ in exactly what an attacker who
      owns a runner for one task can obtain. The BOUNDARY is forced by ratified
      text — the key never enters the worker — and only the MECHANISM is open.
      **Do not decide this in any tranche of this family.** Tranche one contains no
      attestation link at all.

### The topic's other five questions, carried as the topic leaves them

Recorded here so a reader of `tasks.md` alone does not conclude that only two
questions are open.

- [ ] 5.3 **Q1 — wallet-presentation mechanics. OPEN.** Its recommended answer is
      adopted in substance by design D3: tranche one specifies what a ratification
      must EVIDENCE, not the ceremony by which a holder presents.
- [ ] 5.4 **Q2 — where exactly is the on-chain boundary. OPEN**, tranche three.
      The boundary was corrected by the vendored study; the refusing-validator
      shape is still unspecified.
- [ ] 5.5 **Q3 — which chain. OPEN.** Research COMPLETE and vendored; awaiting a
      ruling, not more analysis. Tranche three.
- [ ] 5.6 **Q4 — where do the tranche boundaries fall. OPEN**, and this packet is
      the first evidence on it: authoring tranche one showed that links 1–3
      additionally require the hash-linking rule and the evidence plane to be
      stateable at all (design D1). Offered to the question, not closing it.
- [ ] 5.7 **Q5 — smart contracts or an L2. OPEN.** Direction confirmed by the
      study; the trigger condition for a public programmable layer still unstated.
      Tranche three.
