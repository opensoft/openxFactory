# Proposal Ratification: add-requirement-ref-resolution-integrity

Status: ratified
Decision date: 2026-09-01
Ratifier: Brett Heap (repository owner) — in-session, via an explicit
multi-choice put
Ratified: 2026-09-01 by Brett Heap (repository owner) — in-session via an
explicit multi-choice put, session `openxfactory-f5`; record: this file.
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `tasks.md`, `.openspec.yaml` and the single spec
delta `specs/credential-contracts/spec.md`. **THE SPEC DELTA IS BYTE-UNCHANGED
FROM BRANCH TIP `deb72c8e`**, the tip that was put to him and the tip the third
review round read; the ratification commit moves only the sites that assert the
packet's own standing, plus ONE measurement the catch-up merge falsified
(§ The catch-up merge, and the one measurement it made stale). No requirement
text, no scenario and no normative sentence moves in the ratifying commit.
Gates at the ratification commit, which are the COMMIT'S gates and not
`tasks.md` § 7's realization gates or § 8's archive gate:
`openspec validate add-requirement-ref-resolution-integrity --strict` VALID, and
`--all --strict` **80 passed / 0 failed**; `pytest tests/doc-health` carrying
EXACTLY ONE FAILURE, PRE-EXISTING ON `main` AND PROVEN NOT TO BE THIS PACKET'S
(§ The one red test, measured rather than waved past); doc-health
single-repo against the
`origin/main` baseline `1c1dcbbe`, both trees in identically named `openxFactory`
directories — **ZERO NEW FINDINGS, and the sixty-two finding rows are IDENTICAL
line for line in both directions** (nothing new, nothing dropped), totals
unchanged at 5 critical, 4 error, 39 warning, 14 info. **The full suite is left
to CI, this commit being documentation-only** — no `.py`, no fixture and no
workflow file moves in it, and CI was green on all four required checks at
`deb72c8e`.

## Decision

**RATIFY, BY DIRECT RULING OF THE REPOSITORY OWNER.** The two ADDED requirements
and their twelve scenarios stand as they are at tip `deb72c8e`. **AD-1 IS RULED
TWO CODES, AS DRAFTED** — zero-resolving and ambiguous reported apart, under
distinct codes, with separate remedies. AD-2 … AD-6 stand as drafted and OQ-1 …
OQ-4 stand open, routed exactly as the proposal routes them.

**Ratification authorizes realization and performs none of it.** `tasks.md` § 3
through § 6 — the validator arm, the two codes, the three fixtures, the declared
deprecation and the contract cut — are the realization slice and are not built by
this act. No validator line moves, no fixture is written, no bundle number is
allocated and no deprecation row is declared by ratifying.

## AD-1 — RULED: TWO CODES. The one-code branch is DECLINED, NOT DELETED

**The ruling is the packet's own recommendation, taken as drafted.** The
resolution-integrity finding carries TWO codes of one new family: a reference
resolving to ZERO requirements and a reference resolving to MORE THAN ONE are
reported under DISTINCT codes, on the measured ground the packet gives — their
remedies live in different files. A reference resolving to nothing is repaired at
the reference; a reference resolving to several is repaired in the requirements
document, by making the ids it declares unique. The delta's obligation that the
two be **NAMED APART** therefore stands, the second requirement's scenario *"Zero
and more-than-one are named apart"* stands with its DISTINCT-codes THEN bullet
intact, `code_surface`'s `DEPRECATION_CODES` growth from EIGHT to TEN stands, and
`tasks.md` § 3.3, § 4.1, § 4.2 and § 5.1 stand as written.

**THE TWELVE-ITEM AD-1/ONE-CODE AMENDMENT SET IS NOT EXECUTED.** Not one of its
twelve items is applied: the delta's *"ZERO AND MORE-THAN-ONE ARE NAMED APART"*
paragraph is unedited, the *"named apart"* scenario is neither retitled nor
rewritten, `code_surface` still says TWO CODES AND THREE FIXTURES, and the README
clause still names two codes and three fixtures.

**IT IS DECLINED, AND IT IS DELIBERATELY LEFT STANDING IN THE PACKET.** The
amendment set is not struck from `proposal.md` by this ruling, because it is the
record of what was rulable. A ratifier who is offered a genuine alternative and
takes the other one leaves a better record by keeping the alternative legible
than by deleting the evidence that a choice existed — and the enumeration is the
thing that made the choice a one-sentence act rather than a reconstruction. AD-1
now carries the ruling in its own heading, so no reader can mistake a declined
branch for a live one, and `tasks.md` § 3.3's *"Subject to AD-1"* cross-reference
is DISCHARGED rather than deleted.

**What the enumeration bought, recorded because it is the transferable lesson.**
The one-code branch existed in an earlier draft as a single struck scenario, and
in that form it would have ratified a packet that simultaneously permitted and
forbade a single-code implementation — a delta obliging *"NAMED APART"* standing
beside a ruling that permits one code. Codex found exactly that (round 2, below),
and the repair was to write the branch out in full. The ruling then cost one
sentence and executes as zero edits. **A branch that cannot be executed
mechanically is not a rulable alternative; it is a gesture at one.**

## The path taken, and the path declined

**The packet did not prescribe a sitting for itself, and did not get one.**
`tasks.md` § 2.3, as authored, put the question rather than the answer: *"Whether
a §7.4-shaped council sitting is convened for this packet at all is BRETT'S CALL
and is not assumed here."* It named the nearer precedent in the same breath —
`govern-sibling-added-modified-deltas`, ratified 2026-08-31 by direct ruling with
the sitting it had prescribed for itself DECLINED — and gave two reasons the
direct path fits: the packet is small, and its subject is a RULED SUCCESSOR
rather than a new doctrine.

**He took the direct path, and it is the #504/#497-family precedent's direct
branch.** That branch is the estate's ordinary ratification shape: the OWNER'S
act carrying the whole verdict, with the machine bench as its input.
`add-notebook-projection-identity` (2026-08-23),
`add-standing-policy-compliance-contract` (2026-08-26) and
`govern-sibling-added-modified-deltas` (2026-08-31) each took it. It is distinct
from the SEATED §7.4 path that `add-binding-consumer-identity` (2026-08-29),
`add-chain-anchoring` (2026-08-30) and `add-chain-attestation` (2026-09-01) took.

**NO SEAT SAT, NO BALLOT WAS CAST, AND NO PART OF THIS RECORD MAY BE CITED AS A
COUNCIL DISPOSITION.** What differs from the `govern-sibling` precedent is only
this: that packet had ASKED for a sitting and was answered by a choice between
paths, whereas this one left the question open and had it answered. Neither is a
sitting, and neither is dressed as one.

## The review evidence — three Codex rounds, two repairs, and one finding OPEN

**THREE substantive Codex rounds ran on this pull request, not one**, and the
third read the fix tip. They are set out in full because the merge posture
recorded below was given on a count of ONE.

| # | Reviewed commit | Time (UTC) | Finding | Standing |
| --- | --- | --- | --- | --- |
| 1 | `1d6d58f7` | 2026-08-31 19:39 | **P2 — "Correct the claimed one-byte control."** *"Changing `example-secret-two` to `example-secret-one` changes three bytes (`two` → `one`), not one, so the documented control does not substantiate the normative scenario that says a one-byte edit must trigger the finding."* | **REPAIRED at `deb72c8e`** |
| 2 | `1d6d58f7` | 2026-08-31 20:34 | **P2 — "Reconcile all two-code requirements after a one-code ruling."** Striking one scenario would leave the delta requiring *"NAMED APART"* while tasks and `code_surface` still bought two codes — *"the resulting ratified packet would simultaneously permit and forbid a single-code implementation."* | **REPAIRED at `deb72c8e`** |
| 3 | `deb72c8e` | 2026-08-31 23:54 | **P2 — "Resolve ambiguity across all indexed requirement documents."** `resolve_requirement` matches `index.get(requirements_document_ref)`, so where one requirement id sits in TWO schema-valid documents a binding pointing at either gets `ok`; `tasks.md` § 3.4 freezes that resolver, so the proposed per-binding arm would stay silent on the cross-document case. | **OPEN — ROUTED, NOT REPAIRED** |

**Rounds 1 and 2 were repaired in the packet, and the repairs are recorded in
`tasks.md` § 1.9 with their evidence.** Round 1's repair rebuilt the reproduction
on `example-secret-a` / `example-secret-b`, RE-RAN it against the validator at the
branch's merge-base `3a6a16e9`, and wrote BOTH reproduction files into
`proposal.md` § What was measured § 6 in full, so the run is re-executable from
the packet alone; the delta scenario now states the single-byte spacing in its
WHEN, so the claim is checkable rather than asserted. Round 2's repair replaced a
one-scenario strike with the complete twelve-item AD-1/ONE-CODE AMENDMENT SET —
the thing that made this ratification's AD-1 ruling a one-sentence act.

**ROUND 3'S FINDING IS OPEN AT THE RATIFIED TIP, AND THIS RECORD DOES NOT CLOSE
IT.** It is recorded here rather than absorbed, and it is ROUTED to `tasks.md`
§ 9.4 — *"Open — deliberately not closed by this change"* — with a pointer placed
in § 3.4, the realization row it lands on. Three facts make routing the honest
disposition rather than repair:

1. **It does not falsify this packet's normative text.** This delta's ambiguity
   scenario reads *"matching more than one requirement record"* and says nothing
   about how many documents those records sit in. Nothing ratified here becomes
   untrue if the resolver's lookup is later broadened.
2. **It lands on a REALIZATION row, and ratification realizes nothing.**
   § 3.4 — *"`resolve_requirement` is CALLED, not edited"* — is an instruction to
   an implementer who has not started. Routing it reaches that implementer at
   exactly the moment it bites.
3. **The defect it names is INHERITED, not introduced.** The promoted scenario it
   measures against — *"a named requirement reference matches requirement records
   in more than one document, or more than one record in a document"*, now canon
   at `openspec/specs/credential-contracts/spec.md` since PR #541 archived
   `add-binding-consumer-identity` — is already unmet by the shipped resolver.
   This packet neither created that gap nor closes it; what round 3 correctly
   observes is that § 3.4, as written, would carry it forward silently. § 9.4
   makes it loud.

**What round 3 therefore obliges, and where.** Before the realization slice may
be called complete, the implementer must either BROADEN the resolution lookup or
EXPLICITLY AMEND the promoted scenario — and must not do neither. That obligation
is now written in the packet.

**The other benches.** Copilot returned two rounds (2026-08-31 19:04 and 20:57);
the second raised no packet defect, only that the PULL REQUEST DESCRIPTION still
quoted the superseded `example-secret-two` -> `example-secret-one` control while
the committed artifacts carried the corrected one — a fact about the PR body, not
about the packet, and the committed text is the ratified baseline. Sourcery
returned its private-repo upsell stub and reviewed nothing.

**CI was green at `deb72c8e`**: `merge-master-approval` pass,
`pytest-suite` pass (19m27s), `signed-execution-chain-gate` pass,
`wallet-validation` pass.

## The provider refusal, recorded honestly

**Codex was PROVIDER-REFUSED on org usage limits across eight of eleven review
requests on this pull request**, and the refusals bracket round 3 on both sides
rather than beginning after it:

- ELEVEN `@codex review` requests were made by the repository owner between
  2026-08-31 19:34 and 2026-09-01 03:36 UTC, roughly hourly.
- THREE were answered with a review — 19:39 (round 1), 20:34 (round 2) and
  **23:54 (round 3, on the fix tip `deb72c8e`)**.
- EIGHT were answered with *"You have reached your Codex usage limits for code
  reviews"* — FOUR before round 3 (20:54, 20:58, 21:53, 22:48) and FOUR after it
  (00:46, 01:44, 02:40, 03:36).

**THE FIX TIP IS THEREFORE REVIEWED, NOT UNREVIEWED — ONCE, AND WITH A FINDING.**
That is recorded plainly because the merge posture below was given on the
understanding that `deb72c8e` had drawn no round at all. It had drawn one, at
23:54 UTC, and that round returned the P2 routed above. **What remains unavailable
is CONFIRMATION**: no round has read the packet since round 3's finding was
routed, and the four hourly retries that followed it were all refused. A reader
should treat the third round as the last word the bench has said, and § 9.4 as
this packet's answer to it rather than the bench's acceptance of that answer.

## The merge authorization, recorded for provenance and NOT exercised here

Brett Heap's word on this packet is **"merge on clear, with Codex's refusal
recorded"**. It is recorded here because a ratification record is where the
provenance of the acts around it belongs. **THE MERGE IS NOT THIS RECORD'S ACT**,
this record does not perform it, and nothing here is conditioned on it.

**One qualification belongs with it, and is stated rather than resolved.** That
word was given on the count of ONE substantive round with both findings fixed.
The count is THREE, and the third round's P2 is open and routed rather than
repaired. Whether a routed finding satisfies *"clear"* is the merge authority's
call and not this record's; the record's duty is to make sure that call is taken
against the true count, which it now can be.

## What this ratification does NOT do

- **It realizes nothing.** The validator arm (`tasks.md` § 3), the three fixtures
  (§ 4), the declared deprecation (§ 5) and the contract cut (§ 6) are the
  realization slice and belong to a separate pull request, on the
  #497 -> #516 pattern this packet's own subject set established. No line of
  `scripts/validate-credential-contracts.py` moves by ratifying.
- **It allocates no bundle number.** § 6.1 stands: the number is read from
  `contracts/manifest.yaml:3` AT REALIZATION, not here.
  `contract_bundle_version` is `contract-v2.5` at this commit — re-read after the
  catch-up merge and UNCHANGED from the packet's merge-base — and other packets
  are queued on the same file.
- **It declares no deprecation.** `docs/contract-versioning-policy.md`
  § Deprecations Currently In Force is untouched, and the
  `add-binding-consumer-identity` entry's completeness claim is reconciled at
  realization (§ 5.1), not now.
- **It settles no open question.** OQ-1 … OQ-4 stand exactly as `proposal.md`
  § Open questions leaves them, each with its recommendation and no decision.
  The direct ruling reached AD-1 and did not reach the questions.
- **It does not close #523, and it states no intent to.** The packet nowhere
  claims a `Closes #523`, and `tasks.md` § 8 carries no such line. The issue is
  this packet's ORIGIN and its scope statement; it is answered when the
  resolution-integrity check exists, which is realization's act. A
  ratified-but-unrealized proposal closing the issue that commissioned it is the
  shape the estate has already refused once.
- **It performs no archive.** `tasks.md` § 8 is unchanged. § 8.3's re-verification
  survives the sibling's archive and is now easier, not harder — see below.
- **It convenes nothing retroactively.** No seat sat and no ballot was cast.

## The one red test, measured rather than waved past

**`pytest tests/doc-health` has ONE failure at this commit, and it is NOT this
packet's.** It is
`tests/doc-health/test_modified_block_currency_self_gate.py::test_every_carriage_ledger_finding_over_the_real_tree_is_named`
— the modified-block-currency self-gate, whose design is to go RED whenever the
corpus's carriage-ledger population moves without the named-subject list moving
with it. Its own assertion message says so: *"THE CORPUS MOVED, most likely, and
corpus movement is the EXPECTED cause of this failure."*

**The subject it reports as unnamed is `add-chain-attestation`'s** —
`('add-chain-attestation', 'signed-execution-chain', 'A gate validates the short
chain as a hash-linked chain')` — a MODIFIED block that arrived on `main` with
PR #510 (`1a69b7cb`), NOT with this packet, which carries no `## MODIFIED
Requirements` block anywhere (`tasks.md` § 1.2) and writes nothing under
`signed-execution-chain`.

**IT WAS PROVEN PRE-EXISTING RATHER THAN ASSUMED.** The same test was run against
an UNTOUCHED `origin/main` checkout at `1c1dcbbe` — no packet edits present — and
FAILED IDENTICALLY, reporting the same single unnamed subject: *"0 named
subject(s) NO LONGER reported []; 1 unnamed subject(s) NEWLY reported
[('add-chain-attestation', …)]"*. The catch-up merge INHERITED this red; the
ratification did not cause it, and reverting every edit in the ratifying commit
would not clear it.

**IT IS NOT THIS PACKET'S TO FIX, AND IS NOT FIXED HERE.** Re-aiming the named
subjects is an amendment to the self-gate on behalf of whichever packet moved the
population — `add-chain-attestation`'s, on the gate's own "update the named
subjects in this module, in the same commit, saying which subject moved and why"
instruction. Silently re-aiming another packet's ledger inside a ratification
commit would be exactly the kind of quiet sweep this estate refuses.

**WHAT WAS ACTUALLY MEASURED LOCALLY, STATED AS MEASURED RATHER THAN ROUNDED UP.**

- A `-x` run over `tests/doc-health` returned **1 failed, 713 passed** — the 713
  being everything ordered before the self-gate, and the 1 being it.
- That same test, run ALONE against the untouched `origin/main` checkout at
  `1c1dcbbe`, returned **1 failed, 14 passed** with the identical unnamed subject.
  That is the proof of inheritance, and it is a run of `main`, not of this branch.
- The suite re-run with that one test deselected, and with the two
  network-bound modules held back, returned **1250 passed, 1 deselected, 0
  FAILED**.
- Those two held-back modules — `test_pin_reachability.py` and
  `test_release_inventory.py`, which make per-case
  `git ls-remote origin refs/retention/pins/*` calls against the real remote —
  were then run on their own and returned **96 passed, 0 failed**.

**SO THE WHOLE OF `tests/doc-health` WAS DRIVEN TO A LOCAL TOTAL AFTER ALL:
1346 PASSED, 1 FAILED, and the 1 is the inherited self-gate above.** No test in
this suite fails because of anything in this commit. CI's own
`pytest-suite` was PASS at `deb72c8e` in 19m27s, and the full repository suite is
left to CI, this ratification commit moving no `.py`, no fixture and no workflow
file. The substantive doc-health gate, the REPORT comparison, is likewise driven
to completion above and is clean in both directions.

## The catch-up merge, and the one measurement it made stale

**A catch-up merge of `origin/main` (`1c1dcbbe`) landed before this ratification,
as its own commit**, because `main` had moved seven commits under a five-day-old
merge-base and the pull request was CONFLICTING. The conflict was `README.md`'s
"Active changes:" list, where both sides had inserted an entry at the head;
resolved as a union, both texts byte-unchanged.

**PR #541 archived `add-binding-consumer-identity`** (basis-first, with
`add-notebook-hosting-credential-custody`), promoting its requirements into
canon. `openspec/specs/credential-contracts/spec.md` went from SEVEN promoted
requirement titles to TWELVE, and the two titles this packet measured as ABSENT
are now among them. **The packet's § The sibling rule, measured was therefore TRUE
WHEN WRITTEN at merge-base `3a6a16e9` and FALSE after the merge**, so it is
RE-MEASURED in the ratifying commit rather than ratified as written.

**THE CONCLUSION IS UNCHANGED, AND THAT IS THE POINT OF RE-MEASURING RATHER THAN
DELETING.** The packet chose an ALL-ADDED delta. Before the archive, a MODIFIED
block over either title would have been `govern-sibling-added-modified-deltas`'
governed shape — a ``Modified over`` marker plus an archive-order hold behind the
sibling. After it, such a block would be an ORDINARY MODIFIED block over promoted
canon, needing neither. **Either way a pure ADDED requirement serves**, because
the reporting duty is one this capability states nowhere: the sibling states the
duty FOR THE REFERENCE, and this states WHERE IT IS OWED. The reason the marker
rule does not apply has changed; the choice it was cited to justify has not. The
re-measurement is recorded in `proposal.md` § The sibling rule, measured and in
`tasks.md` § 1.2, and `tasks.md` § 8.3's archive-time `grep` stands as written.

**Two collateral facts were checked rather than assumed.** Neither ADDED title —
*"A declared requirement reference is resolved on its own binding, whatever that
binding shares"* nor *"Resolution integrity carries its own code and phases like
every other narrowing"* — appears among the twelve promoted titles, so the
all-ADDED delta raises no ADDED-over-canon collision against the newly promoted
text. And `contract_bundle_version` did not move, so `target_release` and § 6.1
stand.

**The reproduction of § What was measured is NOT re-run, deliberately.** It is
PINNED at merge-base `3a6a16e9` and says so on its face; the branch moves no
validator line, no fixture and no test, and the catch-up merge moves none either,
so the tree it was measured against and the validator this packet describes are
the same. A pinned measurement that names its pin is evidence; re-running it to a
different number without moving the pin would be worse.
