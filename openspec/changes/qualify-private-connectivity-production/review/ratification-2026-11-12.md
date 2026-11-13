# Ratification: Private connectivity production qualification

Status: ratified
Ratified: 2026-11-12 by Brett Heap, in session; the instruction and reviewed revision are recorded below.
Kind: ratification-record
Decision date: 2026-11-12
Decision timezone: America/La_Paz
Ratifier: Brett Heap, openXfactory repository owner

Brett Heap gave this instruction in the Codex session:

> go ahead and ratify qualify-private-connectivity-production, mark PR #1309 ready for review, request the required approvals, and merge it once all required checks and approvals are in.

This decision ratifies the policy and ownership boundaries reviewed in
[PR #1309](https://github.com/opensoft/openXfactory/pull/1309) at commit
2ee0e3cd2b982a36d89b779a035f8be260a0215f: 18 requirements and 39 scenarios
for local Headscale, standalone Hosted Headscale, and hosted DomainxFactories
on openXsoft.com, including staging qualification, a bounded production
canary and gated expansion.

The local Codex skill review and focused repair re-reviews closed the
canary-authority P2 before this decision. Managed targets retain accepted
requests and managing-factory execution, with request-scoped grants where their
channel requires them. Governed pull reconciliation retains the reviewed-merge
boundary without an additional push credential. Unmanaged customer-operated
targets require current customer-operator authority and required consent.

The ratification records approval in the packet's lifecycle headers and
ad-hoc origin declaration, completes governance task 1.1, and updates the
repository index. It does not amend the reviewed requirements or design
decisions. The earlier [validation note](validation-2026-11-12.md) records
draft publication and local review before this ratification; its draft-state
statements describe that earlier publication stage.

The instruction authorizes marking the PR ready, requesting eligible reviews,
and landing after the applicable checks and approval rules are satisfied.
The shared agent instructions' standing brettheap-author override, where
applicable, remains a separate merge-approval exception and is not a reviewer
approval.

Policy ratification does not complete Q0 commissioning or any later operating
gate. The coordinating Speckit feature, concrete owner/code/CI/schema scopes,
supported artifact releases, intended-platform decisions, staging execution,
production canary, commercial offers and expansion waves retain their separate
decisions and evidence requirements. Implementation handoff and acceptance
tasks 2.1–3.4 remain open. Feature 040 and its approved lab history are unchanged.


## Ratification validation

- Pinned OpenSpec 1.12.0 strict packet validation passes. Whole-corpus strict
  validation exits 0 with 123 raw passes and the one existing accepted
  add-chain-attestation finding; zero undispositioned failures.
- Sequencing, code-surface and target-release validation pass. The sanctioned
  ledger seed reports 248 rows and zero moved rows; the ledger diff is clean.
- Status-validity and duplicate-packet checks pass. This packet has no
  ratified-provenance or proposal-origin finding. The broader families report
  33 ratified-provenance findings and two proposal-origin findings outside this
  packet; every reported path is unchanged from the reviewed head. These are
  baseline findings, not a clean whole-repository provenance result or a waiver.
- The 647 sequencing, declaration, ratification-citation, record-subject,
  proposal-origin and status-reader regressions pass after materializing the
  exact pinned openDox/openXdox dependencies. No pin, test, skip or check policy
  was changed to obtain that result.
- The reviewed requirement and design wording is unchanged apart from lifecycle
  headers. Runtime implementation and qualification remain future work.
