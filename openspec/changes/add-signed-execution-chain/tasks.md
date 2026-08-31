# Tasks: add-signed-execution-chain (tranche one)

Governance-level and dependency-ordered. **This change is RATIFIED (2026-08-29,
Brett Heap — `review/ratification-2026-08-29.md`) and its code surface is now
REALIZED.** §1 was authored in the pull request; **§2 is Brett's ratification act
and is DISCHARGED**; **§3 and §4 are realized in the pull request that carries
this edit**, except the three boxes that are not this author's to close —
4.5 is an OPERATOR act, 4.6 depends on it, and 4.7 rides a bundle cut whose
number is allocated by merge order. §5 names the successors and is not drafted.

**WHAT "RATIFICATION PERFORMS NO REALIZATION" MEANT, AND STILL MEANS.** That
sentence is about the RATIFYING ACT and it is untouched: `proposal.md`,
`.openspec.yaml` and the ratification record all say it, they were true when
written, and they are true now. What changed is that the later commission they
named has been carried out — in a separate pull request, by a separate act,
against the packet as ratified. The distinction is worth keeping because
collapsing it would make the ratification look like the thing that built the
family.

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

- [x] 1.1 `signed-execution-chain` — **NINE ADDED requirements over 45
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

- [x] 2.1 **RATIFIED 2026-08-29 by Brett Heap**, in session via question
      prompts; record at `review/ratification-2026-08-29.md`. **Ratification of
      this packet authorizes tranche one only** and creates no attestation
      identity, no certificate authority, no anchor and no chain. It performs no
      realization.
- [x] 2.2 **CONFIRMED at ratification.** `target_release` is **`contract-v2.3`**,
      FRESH-COUNTED at this branch's tip — `contracts/manifest.yaml:3` declares
      `contract-v2.2` and `contracts/releases/contract-v2.2.digests.yaml` is a
      cut inventory in the tree, so v2.2 is spent. It stays ALLOCATED AT
      REALIZATION by merge order per `docs/contract-versioning-policy.md`, and
      the realization re-counts against the manifest at ITS tip rather than
      trusting this line — that recount is §4's obligation, not an open half of
      this box.
- [x] 2.3 **DONE in the ratification commit.** Front-matter `Status: ratified` plus the
      `Ratified:` line naming approver, date and a resolvable record path, per
      the `sanction-ratified-record-spelling` three-way floor.

## 3. Settle before schemas are authored

Both are contract content, cheap now and expensive after a bundle ships. The
`openxwallet` custody enumeration is the standing precedent for how quietly a
wrong set re-opens the hole the rule was written to close.

- [x] 3.1 **FIXED as `xfc-jcs-sha256-1`**, declared once in
      `contracts/signed-execution-chain/digest-construction.schema.yaml` and
      taken by `$ref` everywhere else, so the family cannot grow a second
      construction rule beside the first. RFC 8785 JSON Canonicalization Scheme
      over the digest subject, SHA-256, rendered `sha256:` + 64 lowercase hex,
      and BOUNDED rather than half-implemented: object, array, string, INTEGER,
      boolean and null are admitted and a non-integer number is REFUSED, because
      ECMAScript number serialization is the one part of JCS a second
      implementation reliably gets wrong and a digest two readers compute
      differently is worse than a digest one of them refuses. **THE EXACT BYTE
      RANGE is the `signed_ratification` block** — the block the ratifying
      signature covers, and nothing outside it; the signature sits beside that
      block, not inside it. Pinned by the RFC's own worked example in
      `tests/signed_execution_chain/test_digest_construction.py`, including the
      UTF-16 code-unit ordering that disagrees with code-point ordering above
      the BMP.
- [x] 3.2 **FIXED against RFC 6962 / Rekor as a HASH-LINKED SIGNED LEAF
      SEQUENCE**, and the realization says which form it took rather than
      leaving a reader to assume a Merkle tree. A leaf carries its `leaf_index`,
      the `tree_size` it completes, its predecessor's digest, its own digest
      (over the leaf content — the record with `leaf_digest` and
      `leaf_signature` removed) and its own signature. **THE HEAD IS THE NEWEST
      LEAF**, so no separate tree-head record exists or is needed, and a
      consistency proof against an observed head is the re-derivation of the
      link chain from that leaf forward. What a verifier reads to detect an edit
      is the link chain; what it CANNOT detect — suffix truncation nobody has
      observed — is DECLARED in the conformance declaration's SEC-R6 entry with
      tranche-three anchoring named as what closes it.
- [x] 3.3 **DECIDED: the register precedent, in this repository** — a tracked
      file whose READER is the shape, on
      `governance/review-authority/register.yaml`'s footing. The decision is
      FORCED rather than preferred: requirement 9 requires the named validator to
      run as a required check ON THE REPOSITORY THAT HOLDS THE RECORDS, and
      requirement 5 requires a point-of-use checker to establish a traveling
      contract's consistency with NO LIVE SERVICE in reach. A governed store
      outside the tree satisfies neither. **No live log instance exists yet and
      the realization says so** — inception is a human act with a wallet-held
      key, this realization mints no chain, and the reader's repo-scan note
      reports the empty sweep rather than passing over it in silence.

## 4. Realization — ONE Speckit contract feature

**WHAT THE REALIZATION'S OWN BOT BENCH CORRECTED, recorded rather than silently
patched**, on the same footing `design.md` D7 records the packet's rounds. Round
one on the realization pull request produced FOUR findings, all real, all taken,
and **the first was a live forgery rather than a hardening**:

| Round | Finding | Where it landed |
| --- | --- | --- |
| 1 | **P1 (Codex AND Copilot, independently)** — the Ed25519 verifier accepted SMALL-ORDER public keys. With an identity key the `[h]A` term vanishes, the equation stops depending on the message, and `R = identity, S = 0` verifies for ANY message — **a forgery needing no private key**, and every public half in this family arrives inside a record chosen by whoever assembled the chain. **Reproduced against the pre-fix code before repair**: the identity key accepted the forgery over every message tried, and two of the order-4 points over some | `ed25519._is_small_order`, refusing the whole class by `[8]P == identity` rather than a list of encodings; six negative-control tests, including one that confirms the published small-order list really is small-order by arithmetic — which caught a transcription slip in that list on its first run |
| 1 | **P1 (Codex)** — the log's append-only property was checked over consecutive PAIRS, so the lowest retained leaf's carried predecessor digest was compared against nothing. A store that DELETED a prefix presented a set in which every surviving pair linked correctly and every `tree_size` still agreed with its own index. Pre-fix: **zero findings** over a log whose genesis leaf was deleted | `check_log` now requires the retained set to begin at leaf 0 and run consecutively BEFORE any digest comparison, and reports an unverifiable link as unverifiable. Probed by the `log-skipping-a-leaf-position` fixture; the deleted-genesis case is pinned in pytest, because a fixture is ADDED to the corpus and cannot take leaf 0 away |
| 1 | **P2 (Codex)** — integers outside ±(2**53 − 1) are not serialized identically by an RFC 8785 reader, so two conforming readers could derive different chain identities in silence. Pre-fix: `9007199254740993` was emitted unchanged where an ECMAScript reader emits `9007199254740992` | The SAME bound one value class wider — not a second rule — in `canonical.serialize`, declared in the contract beside the non-integer refusal, with a sweep test asserting every integer the packaged corpus actually declares is inside it |
| 1 | **Copilot** — `uniqueItems` on the verdict's eight-check list closed nothing: two entries naming the same check with different outcomes are distinct objects, so a verdict could record one check twice, omit another, carry eight items and be schema-valid beside prose calling the list closed and ordered. Pre-fix: **zero schema errors** for exactly that verdict | `prefixItems` pins each position to its own `const`, making a duplicate, an omission AND a reordering unrepresentable. Repairing the reader alone would have left the shape admitting it |

**THE TRANSFERABLE PART IS THE SECOND COLUMN OF THAT TABLE.** Every one of the
four was a check that LOOKED like it was doing its job: pairs that linked, a list
that was eight long, a digest that serialized, an equation that balanced. None
would have been caught by a test written from the rule's own wording, and all
four were confirmed by RUNNING THE MUTATION AGAINST THE PRE-FIX CODE rather than
by reasoning about it — which is the only way to know a repair is anchored to
something.

**SO THE OWED PASS WAS RUN, RATHER THAN WAITING FOR THE CLASS TO APPEAR A FIFTH
TIME.** D7.8's lesson is that a rule written about a defect class is tested by
whether the NEXT instance is found by the author or by the bench. Three more
instances were found by the author, in the same sweep, and each was measured
against the round-one tip the same way:

- a **ratification leaf** whose payload digest named the right SUBJECT and whose
  VALUE was never compared, though this chain's content digest is in scope — so a
  leaf could record the presentation of a different subject's ratification while
  reading as verified;
- a **chain incepted with no ratification leaf at all**, which passed because the
  atomicity rule checked only the other direction; and
- a **traveling contract whose issuance no leaf recorded**, which passed because
  nothing required it.

**ROUND TWO CONFIRMED THE SWEEP AND FOUND TWO MORE, AND THE OVERLAP IS THE
INTERESTING PART.** Codex independently raised the ratification-leaf payload and
the missing-leaf pair — the same two the author had just caught — which is
evidence the class was correctly identified rather than a lucky guess. It also
raised two the sweep had missed, both P1, and both about a REFERENCE that could
move independently of the thing it referenced:

| Round | Finding | Where it landed |
| --- | --- | --- |
| 2 | **P1 (Codex)** — per-act uniqueness keyed on `presentation.exercise_ref`, which is replaceable WITHOUT touching the exercise it names. Carrying the already-consumed exercise VERBATIM and changing only that outer label produced different signed bytes, a different chain identity, and a uniqueness key the map had never seen: **the consumed exercise was replayable past the rule written to prevent exactly that** | The reference must AGREE with the carried record (`continuity_broken`), AND uniqueness is keyed on the CARRIED identifier — both, because a rule that relies on another rule to be sound has a second failure mode. Probed by `inception-replacing-only-the-outer-exercise-reference` |
| 2 | **P1 (Codex)** — the scope-wide key map was built with `dict.update`, so when two carried wallets declared one `key_id` for DIFFERENT public halves, whichever was read last silently won. Valid leaves of the other chain would fail, and leaves signed by the colliding wallet's key would be ACCEPTED for a chain that never authorized it — **a verification result decided by iteration order** | An `AMBIGUOUS_KEY` marker carried forward rather than overwritten or dropped, at all three sites that resolve a key. An ambiguous identifier makes every signature naming it UNEVALUABLE, which is a refusal: verifying against a guess is worse than declining to verify. Probed by `two-wallets-declaring-one-key-id`, and pinned by a test that presents the two wallets in BOTH orders |

**BOTH ROUND-TWO FINDINGS ARE ONE SHAPE, and it is worth naming because it is not
the round-one shape:** a reference and its referent that can be moved
independently. The round-one class was a check that looked like it was working;
this one is two facts that looked like one fact. A capability whose whole subject
is binding one record to another should expect it.

**SO THAT SHAPE WAS SWEPT FOR TOO, in the same session it was named.** Every
remaining pair of the shape in the signed bytes is now compared: the outer
`grant_ref` against the carried exercise's, the carried wallet's id and holder
against the exercise's `attribution`, and — the load-bearing one — the wallet's
DECLARED CUSTODY against the exercise's `custody_model_in_force`. Custody is not
tidiness: `add-trust-anchor`'s ratified rule is that declared custody BOUNDS WHAT
A SIGNATURE EVIDENCES, so an exercise free to record a stronger model than its
wallet declares would let a `holder_readable` key evidence a human act — and
requirement 8's narrowing rests on that being impossible. Those four paths are
pinned by a test rather than by four more fixtures, deliberately: the refusal code
they report is already red-proven, and what needed pinning was that each
COMPARISON runs.

**ROUND THREE FOUND THE SAME SHAPE ONE LEVEL UP, AND IN THE RULE THE SWEEP HAD
JUST ADDED** — which is the honest measure of how far a self-run sweep gets:

| Round | Finding | Where it landed |
| --- | --- | --- |
| 3 | **P1 (Codex)** — a `traveling_contract_issued` leaf could name chain A in `chain_ref` while carrying the `payload_ref` and digest of chain B's traveling contract. BOTH checks that should have caught it looked SCOPE-WIDE: the payload-digest recomputation resolved the contract by IDENTIFIER across the whole store, so it matched and recomputed cleanly, and the missing-leaf rule collected recorded ids GLOBALLY, so chain A's leaf discharged chain B's obligation. **Chain B passed with its primary custody record silent about an act the contract requires to be recorded — the exact hole the missing-leaf rule had just been added to close.** Pre-fix, measured: the fixture validated CLEANLY | The lookup is chain-scoped and requires exactly one match; the recorded set is keyed on the **(chain, contract)** PAIR. An issuance is discharged only by a leaf on the ISSUING chain. Probed by `issuance-leaf-filed-under-another-chain`, and the remaining three leaf types were checked for the same defect — all were already chain-scoped |

**AND COPILOT FOUND A REFUSAL THAT WAS A CRASH INSTEAD** in the same round, which
is a class of its own: not a missing check, but a check whose ANSWER came out in
the wrong currency.

| Round | Finding | Where it landed |
| --- | --- | --- |
| 3 | **Copilot** — a string or member name holding an UNPAIRED SURROGATE passed the escaper and then raised `UnicodeEncodeError` at the encode step. That is not a `ConstructionError`, so it escaped the refusal path every caller handles and surfaced as a HARNESS FAILURE rather than as a finding. Pre-fix, measured: `UnicodeEncodeError` for both a value and a member name | `_escape` refuses U+D800–U+DFFF as a `ConstructionError`; the bound is DECLARED in the contract beside the integer one; and a test asserts the refusal for five shapes plus a VALID astral-character control, so the fix cannot have been achieved by refusing legitimate records |

**A CONSTRUCTION THAT CRASHES ON AN INPUT IT SHOULD REFUSE HAS TWO ANSWERS**, and
the whole point of one construction is that there is one. The general form is
worth carrying: *every refusal must reach the caller as the same kind of answer*.
The test that pins the integer bound's presence in the contract was widened into
the site that has to grow with each new refusal, rather than a second test being
added beside it.

**THE FIXTURE FOR THE CROSS-CHAIN FINDING WAS WRONG ON ITS FIRST DRAFT, AND THAT IS WORTH RECORDING**
because it nearly hid the finding. It reported as refused-for-the-intended-reason,
and the reason was an INCIDENTAL defect the draft had introduced — its
`inception_leaf_ref` named the wrong leaf — not the cross-chain filing under test.
A negative fixture that fails for a second reason is not a probe, it is a fixture
that agrees with you; the anchor only became real once the fixture was corrected
to a single fault and the pre-fix reader accepted it. **The instrument gets the
same scrutiny as the thing it measures**, which is the second time this
realization has had to apply that to its own harness.

**AND THE SWEEP MEASURED ITS OWN VALUE RATHER THAN ASSERTING IT.** Every packaged
negative was run through both readers and diffed: the second and third
strengthenings changed the verdict on FOUR committed fixtures, so they were
anchored already; the first changed the verdict on NONE, which made it dead code
until `ratification-leaf-committing-to-another-subject.yaml` was written for it.
A refusal no fixture provokes is a refusal nobody has seen work — the same rule
the self-test applies to the closed enumeration, applied to a check that sits
outside it. The diff harness also reported one row this round could not have
caused, and that row was the harness's own defect: the anchor worktree had no
`openXwallet` gitlink, so the two readers were validating carried blocks against
different vocabularies. **A measurement instrument gets the same scrutiny as the
thing it measures.**

- [x] 4.1 **BUILT** — `contracts/signed-execution-chain/` carries the FOUR
      record kinds `code_surface` names (`chain-inception.schema.yaml`,
      `traveling-contract.schema.yaml`, `transparency-log-leaf.schema.yaml`,
      `conformance-declaration.schema.yaml`) plus the definitions-only
      `digest-construction.schema.yaml`, which declares NO record kind and
      exists so 3.1's construction lives in one place. The declaration is
      `trust-anchor`'s declared-shortfall pattern with this family's nine
      obligations (SEC-R1..SEC-R9), closed in both directions, and the two
      residuals that are STRUCTURAL at this tranche — SEC-R1's missing signed
      digest value and SEC-R6's unobserved suffix truncation — are refused the
      word `satisfied` by the reader rather than left to an author's care.
      **NO SECOND VOCABULARY**: the presentation is the shipped
      `xfactory_wallet_grant_exercise` and the signing wallet the shipped
      `xfactory_wallet_record`, carried verbatim inside the signed bytes and
      validated against the PINNED schemas through the `openXwallet/` gitlink;
      the actor is `identity-brokering`'s `actor_subject_reference` carrying an
      `xfactory_wallet_subject_attestation`.
- [x] 4.2 **PACKAGED — 7 positives composing ONE whole chain, and 32 negatives.**
      All nine named refusals have a probe, and so does every other refusal this
      reader can emit: the enumeration is 24 codes and the self-test REFUSES A
      CODE WITH NO PROBE, so a refusal nobody has seen work cannot ship. Two
      further obligations are refused BY SHAPE instead, because unrepresentable
      is stronger than refused — an actor carrying no wallet attestation, and an
      actor binding outside the signed bytes. A negative is evaluated IN THE
      POSITIVE CORPUS'S SCOPE, because a refusal of a CHAIN is a property of a
      SET of records and a fixture adjudicated alone could not express one.
- [x] 4.3 **BUILT** — `scripts/validate-signed-execution-chain.py`, the NAMED
      READER, walking all EIGHT ordered checks over links 1-3 plus the four
      scope rules the gate cannot see (atomicity, per-act uniqueness, the log's
      append-only property, the declaration). It verifies the ratifying
      signature rather than reading a claim about it — `ed25519` per RFC 8032,
      pinned by that RFC's published vectors and their mutations — and refuses
      `ecdsa-p256` and `ecdsa-secp256k1` as UNEVALUABLE rather than accepting a
      signature it did not check.
- [x] 4.4 **RUNNING** — `.github/workflows/signed-execution-chain-gate.yml`, job
      id `signed-execution-chain-gate` (no display name, so the check surfaces
      as the token a ruleset would pin). It verifies the openXwallet pin BEFORE
      trusting it, walks the whole tree with
      `--require-pinned-wallet-vocabulary` so an unreachable pin REFUSES instead
      of silently checking less, and asserts POSITIVELY that the walk happened —
      a green check that proves nothing was walked is the vacuous pass this
      repository has already had to close once. The invocation is pinned by
      `tests/signed_execution_chain/test_gate_wiring.py` inside the required
      `pytest-suite` job, because a comment in a workflow protects nothing.
- [ ] 4.5 **[OPERATOR] — DELIBERATELY OPEN, and it is the one box that decides
      whether any of the rest confers anything.** Make the check REQUIRED in the
      branch ruleset. A merged workflow file is NOT evidence; the evidence is
      the live ruleset state, as `add-wallet-carried-review-authority` task 2.5
      established (org ruleset **21538893** for `wallet-validation`). Until it
      is done, requirement 9 is UNMET rather than partially met, and the
      packaged conformance declaration records
      `is_required_in_ruleset: false` while the reader emits a standing
      `reader-not-required` warning on every run. Neither is decoration: a test
      refuses a declaration that records SEC-R9 `satisfied` while the reader is
      unrequired.
- [ ] 4.6 **Gate — BLOCKED ON 4.5 BY CONSTRUCTION, not by effort.** A
      deliberately broken chain FAILS a real pull request, and the evidence
      records the run id, the check id, the validator's single named refusal,
      and the live ruleset read showing the check required — the shape task 2.6
      of that change proved on canary PR #387. The first three halves are
      producible today; the fourth cannot be read until 4.5 is performed, and a
      box closed on three of four conjuncts would be the closure-on-intention
      this family refuses.
- [ ] 4.7 **CUT-DEPENDENT, and left to the cutting session on purpose.**
      Registration in `contracts/manifest.yaml` and `contracts/CHANGELOG.md`,
      and the additive bundle cut, with `release-surface-integrity`'s
      verify-commit green from an independent clone. **THE NUMBER IS
      RE-COUNTED, AS 2.2 REQUIRED, AND `contract-v2.3` IS SPENT**: at this
      branch's tip `contracts/manifest.yaml:3` declares `contract-v2.3` and
      `contracts/releases/contract-v2.3.digests.yaml` is a cut inventory in the
      tree, so the next additive number is **`contract-v2.4`** — which
      `add-binding-consumer-identity`'s realization (#516, `5e8a33cf`) also owes
      and has not yet performed. Per `docs/contract-versioning-policy.md`
      several changes may ride ONE additive cut, so this family and #516's
      schema move can land in the same `contract-v2.4`; if #516 cuts alone
      first, this one re-counts again rather than reserving a number. **A
      PROPOSED CHANGE MUST NOT RESERVE A MINOR NUMBER BEFORE MERGE ORDER IS
      KNOWN**, which is why this realization registers nothing and bumps
      nothing: the manifest and changelog update is committed atomically WITH
      the cut, and the tag points at that commit.

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
