---
code_surface: openxFactory — A NEW NEUTRAL CONTRACT FAMILY PLUS ITS RUNNING GATE, declared honestly because this tranche is not doctrine-only. `contracts/signed-execution-chain/` gains the chain-inception record (the ratification's signed registration, carrying the chain identity and the reference to the `openxwallet` exercise record that proved presentation), the traveling-contract artifact (the carried form of the signed ratification), the transparency-log leaf record (append-only, signed, hash-linked), and the realization conformance declaration on `trust-anchor`'s declared-shortfall pattern — plus packaged positive AND negative examples for every named refusal, and the canonical `scripts/validate-signed-execution-chain.py`. The GATE is a running check, not a described one: a short-chain verifier over links 1–3 wired as a pull-request check, on the shape `wallet-validation` already proved in this repository (`add-wallet-carried-review-authority` tasks 2.5/2.6 — a workflow file is not evidence; the ruleset state is). Registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive bundle cut. NO attestation record of any kind, NO controller certificate, NO per-task identity, NO certificate authority, NO key service, NO anchor, NO chain, NO commitment format, NO consent plane — links 4–6 and 10 are the named tranche-two successor and the anchoring layer is the named tranche-three successor, each carrying its OWN code surface. NO second identity, grant, proof-of-possession or certificate vocabulary is defined: link 1's instrument is the SHIPPED `xfactory_wallet_grant` / `xfactory_wallet_grant_exercise` pair consumed at the digest pin, and a new one here would be the collision the staged topic names as its first risk.
target_release: PROVISIONAL, FOR BRETT TO CONFIRM AT RATIFICATION — the next additive contract bundle after `contract-v2.1`, deliberately NOT numbered here and allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`, on `add-trust-anchor`'s precedent for a new neutral contract family ("next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)") and `add-credential-escrow-checkout`'s stated reason for not spending a number a parallel packet may already be spending. THE GROUND, MEASURED RATHER THAN REMEMBERED: `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v2.1`, so the era is v2.x; the pre-split v1.4x numbers are spent, `contract-v1.45` included — `contracts/releases/contract-v1.45.digests.yaml` is a cut inventory in the tree today, so any reservation of that number for a later candidate is already historical and this change could not take it even if it wanted to. THE CLASS IS ADDITIVE and nothing narrows: a new contract family is the versioning policy's "new contracts" case verbatim, no existing schema changes, no consumer pinned at `contract-v2.1` is made non-conformant, and no domain is obliged to adopt a chain. The archive gate is merge-plus-green-plus-the-cut; realization is a later commission.
Status: draft
Proposed: 2026-08-29
Origin: `openxFactory:staging:signed-execution-chain`, EXIT 1 OF THREE — the tranche the staged topic's own `## Exit path` marks "Composable TODAY", raised without waiting for the two rulings its siblings wait on. The topic was registered 2026-08-27 from Brett Heap's expansion ruling and hardened by five adversarial review rounds on its own pull request (PR #452, squash `6612d323`). Tranches two and three are named successors in this document and NOT drafted here.
---

# Proposal: add-signed-execution-chain

**THIS DOCUMENT IS NOT RATIFIED, AND A CLARIFY ROUND PRECEDES ITS
RATIFICATION.** The staged topic carries seven open questions; **Q1 is the one
this tranche's own text depends on**, and its recommended answer is carried
here FLAGGED rather than assumed. Q3, Q6 and Q7 gate the later tranches and are
recorded here only so the clarify round can take all seven in one sitting, per
the standing clarify rules (the full block goes to a file in the change
directory and to the terminal, path echoed top and bottom). Nothing in this
proposal is ratified-shape until that round is answered and Brett Heap rules.

## Why

**The family already signs the decision, and then loses the signature.**
`add-wallet-carried-review-authority` made review authority a wallet-carried
grant with a root issuer anchored to a named operator, and S2 realized it: the
validator refuses a review-class grant that names no `issued_by`, refuses a root
grant naming an agent as issuer, and the first live root grant
`governance/review-authority/grants/grant-mrc-0001.yaml` roots in the anchored
operator under the Human Escalation Contract. That is a signed ratification.
What happens next is unsigned. The work runs in a lane that cannot prove it
descended from that ratification, and the merge gate that lets it land cannot
ask.

**The inversion that makes this worth doing is that a validated chain is not an
audit trail — it is a permission.** An audit trail is written after the fact and
can be forged after the fact. A chain the gate WALKS before it permits the
terminal act cannot be forged after the fact, because the act does not happen
without it. The record and the control become the same object, which is the
property this repository keeps discovering it needs and keeps having to add
afterwards.

**The forcing fact is not hypothetical.** openxFactory issue **#351** landed a
reversion of ratified canon that passed `openspec validate --strict`, passed CI,
and passed a three-bot review lane; **#357** generalizes it into an open
validator gap. Every one of those gates asked *is this well-formed?* None of
them could ask *whose ratification is this work descended from, and does that
ratification permit it?* — because nothing carried the answer.

**And the neutral-layer argument is that the same shape occurs twice in two
domains.** MedxFactory's HealthLinc ratifies, simulates, reviews and "merges" a
treatment plan, where merge means pushed to the patient app or printed as signed
orders; LedgerxFactory's LedgerLinc runs the same chain over an analysis and
publishes. They differ in payload and regulator, not in chain. A family that fit
one domain would belong in that domain's repository.

## What this change is — TRANCHE ONE, and its boundary is the point

The staged topic's `## Exit path` fixes tranche one's scope and this proposal
does not widen it:

- **Links 1–3** — the wallet-presented ratification, the atomic
  ratified⇒chain-incepted act, and the traveling contract.
- **PLUS the signed transparency log**, which that same text places in tranche
  one by its own sequencing argument: *"the evidence plane of claim 6 — the
  signed transparency log — is a **tranche 1** artifact, not a tranche 3 one.
  The log is the record; the anchors are late additions to it. Building the log
  last would mean tranches 1 and 2 had nowhere to write their signed leaves."*
- **PLUS the gate, existing from tranche one and validating a SHORT chain**,
  again on the topic's own instruction: *"The gate should exist from tranche one
  validating a short chain, rather than arriving at the end validating a long
  one"*, so the refusal path is exercised from the start rather than first
  tested when it matters most.

**Named successors, NOT drafted here:**

- **Tranche two — `add-signed-execution-chain-attestation`** (working id): links
  4–6 and 10, the harness-controller setup attestation, per-task attestation
  identities, the signed PR-open decision and the governed post-merge test. It
  needs the omnigent layer to enforce the precondition and
  `implement-openxpki-install-repo` to issue the controller certificate, and its
  contract text is gated on **Q7**.
- **Tranche three — `add-signed-execution-chain-anchoring`** (working id): the
  commitment and anchor layer plus the permissioned consent plane whose state
  roots it anchors. Gated on rulings for **Q3** and **Q6**, not on more
  analysis.

**Neither successor's content appears in this change**, and no requirement here
may be read as authorizing it.

## The two convening-derived constraints

Both come from the `gate_rules_council` convening record
`opensoft/codexFactory` →
`hermes/domain/review-councils/records/2026-08-28-gate-rules-openxfactory-substantive-classes.md`
(unanimous 5/5; convener disposition §8, Brett Heap, 2026-08-28). They are not
background: each one bounds a requirement in this change's delta.

### Constraint A — the chain-inception act is OUT-OF-PIPELINE, by proven necessity

**A class over `openspec/changes/**` can never commission a council.** That
surface is a member of the canonical `GATE_INTEGRITY_FLOOR`, the PR-time floor
is evaluated **before** any clearable classification, so every candidate returns
`parked_never_clearable` and `council-convening-lane.yml:1022-1026` bails on
exactly that outcome. **Measured on openxFactory's real tree: 984 admitted
paths, 984 floored, 0 remaining.** And it is **code-level, not
document-level** — the record's own reproduction shows `gate_integrity`
declared, `gate_integrity` absent, and **no rule document at all** all parking
identically, with reasons byte-identical. CPL's sentence is the sharpest form:
*"No edit to this rule document — none — can make this class ever reach
classification."*

**This change's own ratification and chain inception land on
`openspec/changes/**`.** So the enrollment mechanism cannot be the clearance
pipeline — not by preference, but because the pipeline provably cannot reach it.
The inception act is therefore performed OUT-OF-PIPELINE and the delta says so
in requirement text, citing this record. A design that routed inception through
the envelope would be describing a control that cannot run, which is the LS-A3
failure this family has now named three times.

**And the measurement is not the whole ground.** 984/984/0 covers the surface
this repository's ratifications land on; the rule itself is not
surface-dependent, because **a pipeline that CLEARS candidates cannot also be
what CONFERS the authority those candidates are cleared against.** A chain whose
first link is minted by the mechanism it exists to permit is circular on any
surface, floored or not. The measurement makes the rule unarguable here; the
circularity makes it correct everywhere, and both are in the requirement.

### Constraint B — link 7 composes with the §7.4 path, not with the clearance envelope

The convener's ruled continuation is *"the council-reviewed-but-human-approved
path, which per the 2026-08-26 record §7.4 needs no class and no flip"* — and
that path *"reaches this repository without an envelope and without amending
FR-008"*. Link 7 (council review with the signed proposal as the brief) is
therefore expressed, in its short-chain tranche-one form, as **a signed review
of the traveling contract on the §7.4 path**, and NOT as an envelope entry, a
candidate class, a flip, or a soak threshold. **This change creates no
`merge-approval-envelope` instance and defines no candidate class**, and
`specs/025-openxfactory-review-lane-caller/spec.md`'s FR-008 is left exactly
where the convening left it: gated, task 3.2 open, undischarged.

## The vocabulary act — `chain inception`, and why it is not `enrollment`

**025 already owns "enrollment" in this repository**, for a different act: FR-008
reads *"The caller MUST declare no enrolled candidate class"*, and the word there
means **the entry of a candidate class into a `merge-approval-envelope`** so the
codexFactory decision core may classify and possibly clear it. A second, adjacent
sense of "enrollment" landing in a neighbouring capability is precisely the
second-vocabulary invention the 2026-08-28 seats named as the live risk — and it
would be worse than a normal collision here, because both words would sit on the
same pull requests, in the same repository, one week apart. The family already
carries a THIRD sense in `add-worker-enrollment-broker`, which is the proof the
word is loaded rather than free.

So this capability does not take the word at all. **The pair, stated once and
carried in requirement text:**

| This capability's act | 025's act |
| --- | --- |
| **`chain inception`** — the ratification's registration into the signed-execution-chain registry, performed in the SAME signed act as the ratification, minting the **chain identity** (the digest of the signed ratification) that every later link binds to | **candidate-class enrollment** — 025 FR-008's *"enrolled candidate class"*: the entry of a class into a `merge-approval-envelope` for the codexFactory decision core to classify |

**The non-collision, stated explicitly rather than left to inference:** chain
inception creates no envelope, names no candidate class, touches no ruleset,
produces no verdict, and changes nothing FR-008 governs; and 025's enrollment
mints no chain identity, signs nothing, and is not a link in any chain. **The
two never appear in the same sentence except this one.** The delta states the
non-collision in the requirement that owns the act, so a reader who arrives at
the spec without this proposal still finds it (`## ADDED Requirements`, the
inception requirement's body and its fourth scenario). The staged topic's own
prose calls link 2 "ratified ⇒ enrolled"; **this change renames that act on
purpose**, and the rename is recorded in `design.md` D1 so the topic's wording
and this spec's wording are never read as two different acts.

## Capabilities

### New Capabilities

- `signed-execution-chain`: the neutral tranche-one chain — a ratification
  admitted only on wallet-carried authority PROVEN BY POSSESSION in the shipped
  `openxwallet` vocabulary; ratification and chain inception as one signed act,
  performed out-of-pipeline, so a ratified-but-uninscribed state is
  constructively impossible; the signed ratification as a TRAVELING CONTRACT
  checkable at the point of use; an append-only signed transparency log as THE
  RECORD; a gate that validates links 1–3 as a HASH-LINKED chain and refuses a
  break as a fraud signal rather than reporting it as a warning; and tier-1
  ratifying authority held by a human, never by an agent, runner or lane.

### Modified Capabilities

**None.** No promoted requirement is restated or replaced, and this change
carries no `## MODIFIED Requirements` block anywhere. That is deliberate: every
adjacent capability this composes with is either still an ACTIVE change whose
ratified text governs (`add-wallet-carried-review-authority`, `add-trust-anchor`,
`add-identity-brokering`) or a promoted spec this change has no cause to move
(`roles-authority-model`, `credential-contracts`, `workflow-gate-contract`).
Composing by reference is the staged topic's own instruction and the condition
under which its Conflicts table admits this tranche at all.

## Impact

- **New code (this change authorizes; realization is a later commission)**: one
  contract family, packaged positive and negative examples, one canonical
  validator, the append-only log store, one required pull-request check, and
  manifest / CHANGELOG registration at the next additive bundle.
- **Consumes, and does not re-invent** — the composition target, cited at the
  artifacts that actually shipped rather than at the change that promised them:
  - `contracts/openxwallet-pin.yaml` pins `opensoft/openXwallet` at
    `6b248d4050e1f88b3ca75c1290ad2c81f465300c` (`wallet-v1.3`), digest
    `fde433c5…` for `contracts/openxwallet/openxwallet-grant.schema.yaml` and
    `f16ad312…` for `contracts/openxwallet/openxwallet-grant-exercise.schema.yaml`.
    **The exercise record is link 1's instrument and it already exists**: it
    requires `proof_of_possession`, distinguishes `verification_failure` from
    `unauthenticated_request` by `event_class`, and its closed refusal
    enumeration already names `missing_proof_of_possession` separately from
    `missing_grant`, because *"the grant was supplied and is not what was
    lacking"*.
  - `governance/review-authority/grants/grant-mrc-0001.yaml`,
    `.../register.yaml`, `.../wallets/wal-agent-mrc-0001.yaml` and
    `.../attestations/custody-attest-wal-agent-mrc-0001.yaml` — the realized S2
    issuer anchor, the register and its reader, and the first wallet, all read
    inside the REQUIRED `wallet-validation` check (org ruleset **21538893**).
  - `add-trust-anchor`'s ratified declared-custody rule — custody bounds what a
    signature evidences — which is what makes requirement 6's narrowing exact
    rather than assertive.
- **Composes with, and is bounded by**: `specs/025-openxfactory-review-lane-caller/spec.md`
  FR-008 (untouched, still gated), the 2026-08-28 convening record (both
  constraints above), and `omnigent-domain-overlay`'s constitutional
  `access_secrets: false`.
- **Obliges no domain.** No domain must adopt a chain, and no existing
  capability is modified in a way that requires action from a domain that has
  none. MedxFactory/HealthLinc and LedgerxFactory/LedgerLinc are named as the
  neutrality proof, not as consumers under obligation.

## Where the staged topic and a ratified artifact pull against each other

Recorded rather than smoothed, on this family's contested-finding rule. Both are
carried into the clarify round.

**1. "Tier 1 — authority credentials, HUMAN-HELD … never held by an agent"
versus a realized agent-held wallet.** The topic's tier model says authority
credentials are never held by an agent. But `wal-agent-mrc-0001` is a REALIZED
wallet whose holder is `agent:merge-readiness-council`, custody model
`holder_readable`, backing an active `review`-act grant — shipped, validated,
and register-backed. Read literally the topic refuses an artifact this
repository already runs. **This change narrows rather than contradicts**: tier 1
in requirement 6 is **RATIFYING** authority — the authority that INCEPTS a chain
— and that is human-held. A `review` grant is not a ratifying grant, and the
narrowing is not a convenience: `holder_readable` custody evidences that the
HOST acted, which under `add-trust-anchor`'s ratified custody rule is exactly
what a ratification may not stand on. The topic's stronger sentence is
preserved where it is true and narrowed where a ratified artifact contradicts
it, and the narrowing is flagged for Brett.

**2. Q1's "rather than a new artifact" versus a shipped record kind for exactly
this act.** Q1's recommended answer says to record the presentation *"in the
ratification record rather than a new artifact"*. The family already HAS an
artifact for it — `xfactory_wallet_grant_exercise`, shipped at `wallet-v1.3`.
This change reads Q1's intent as **invent no new artifact**, which is honoured
exactly by REFERENCING the existing exercise record from the ratification record
rather than minting a second proof vocabulary. Minting one would be the
collision the topic's Conflicts table names first. **The reading is flagged, not
assumed** — it is the Q1 flag on requirement 1.

## Open questions — the clarify round that precedes ratification

Per Brett's standing clarify rules, the full block WILL BE written to
`openspec/changes/add-signed-execution-chain/clarify-questions.md` (tasks.md
§2.1 — the file does not exist yet and this proposal does not pretend it does)
and presented in the terminal in block form with that path echoed top and
bottom. All seven of the staged topic's questions go in one sitting; only Q1
blocks this tranche.

| Q | Subject | Bearing on THIS change |
| --- | --- | --- |
| **Q1** | Wallet-presentation mechanics | **BLOCKING for tranche one.** Requirement 1 carries the recommended answer FLAGGED. Plus the two narrowings above. |
| Q2 | Where the on-chain boundary falls | Tranche three; recorded so the sitting is complete |
| Q3 | Which chain | Tranche three blocker; the vendored study's recommendation is on the table awaiting a ruling, not more analysis |
| Q4 | Where the tranche boundaries fall | **Partly answered by this document**: tranche one is links 1–3 **plus the log plus the gate**, on the exit path's own two sequencing sentences. The clarify round should confirm that reading. |
| Q5 | Smart contracts or an L2 | Tranche three; direction confirmed by the study, trigger condition still to be stated |
| Q6 | Does "patients put PHI portions on chain" mean commitments | Tranche three blocker; the one place the topic INTERPRETED a ruling |
| Q7 | Where an attestation signature physically happens | Tranche two's contract text; nothing in this tranche depends on it |

## Ratification

**Not ratified.** Ratification is Brett Heap's act and follows the clarify
round. It would authorize exactly one Speckit contract feature plus its gate,
and would create no certificate authority, no attestation identity, no anchor,
no chain, and no runtime beyond the validator and the pull-request check named
in `code_surface`.
