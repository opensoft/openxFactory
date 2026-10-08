# Ratification record — 2026-10-03

Status: ratified
Ratified: 2026-10-03 by Brett Heap, in this Codex session, verbatim "ratify all three as disclosed"; exact reviewed scope is recorded below.
Recorded: 2026-10-03
Approver: Brett Heap
Disposition: RATIFIED AS DISCLOSED

## Owner word and exact reviewed scope

Brett instructed in this Codex session, verbatim:

> ratify all three as disclosed

The three unchanged, locally committed draft revisions presented for this decision are:

| Repository | Change | Reviewed head |
|---|---|---|
| `opensoft/openxFactory` | [`renew-resolved-council-protocol`](https://github.com/opensoft/openxFactory/blob/b5cdf154208c1a5fd59e3936b483f37448ca85f9/openspec/changes/renew-resolved-council-protocol/proposal.md) | `b5cdf154208c1a5fd59e3936b483f37448ca85f9` |
| `codeXfactory/codexFactory` | [`realize-resolved-council-protocol`](https://github.com/codeXfactory/codexFactory/blob/a73d19812feb5698677113d09af783bdf34ca142/openspec/changes/realize-resolved-council-protocol/proposal.md) | `a73d19812feb5698677113d09af783bdf34ca142` |
| `opensoft/xFactory-Hermes-Install` | [`admit-resolved-council-protocol`](https://github.com/opensoft/xFactory-Hermes-Install/blob/7a8d53dab5e18a9c8371c652f4a2c0c143def1cb/openspec/changes/admit-resolved-council-protocol/proposal.md) | `7a8d53dab5e18a9c8371c652f4a2c0c143def1cb` |

This record applies to **opensoft/openxFactory:renew-resolved-council-protocol** at `b5cdf154208c1a5fd59e3936b483f37448ca85f9`. The owner's word ratifies all three as disclosed, without amendments. This records the in-session act; publication of these local commits is still pending.

## Adopted decisions

Adopt the disclosed D1–D5 decisions in [design.md](../design.md), together with the linked provider D1–D5 and successor designs. This includes independently reproduced ordered membership and consumed provenance; immutable frozen assignments; isolated per-seat execution and ephemeral signing keys; independently authenticated assignment authority and verified workflow identity; a deprecation minor before breaking removal; explicit protocol selection; and coordinated pause/drain, activation and paired rollback.

Provider contract versions remain unallocated until governed realization and release serialization.

The proposal's original commission and origin declarations are retained exactly. This ratification freezes those declarations and records the new standing; it does not rewrite prior preparation evidence or infer that any implementation is finished.

## Authority limits and next step

Implementation preparation and realization may proceed through exactly one new Speckit feature for this packet. This session works outside a registered lane; no acceptance, transfer or claim on behalf of an existing lane is asserted. Existing ownership and holds remain respected.

Publication, version allocation, provider or consumer pin advancement, managing-factory deployment, credential/broker provisioning, activation, merge and old-checkout retirement remain separate evidence-bearing acts. This ruling supplies no completed-act evidence for them. Owner-act boxes remain unchecked, with dated evidence beside the relevant item in [tasks.md](../tasks.md). Archive remains gated on the declared exit evidence.

## ADDENDUM 2026-10-08 — the word covers the published text, and gate-conformance edits are approved

**Appended, not a rewrite.** Everything above is the record of 2026-10-03 and stands exactly as written.

### Confirmation, not a re-ratification

On 2026-10-08T17:43:04Z, Brett Heap answered a multiple-choice question with recommendations, first-hand in session to lane `codeXfactory-2` (session `8d6bf418-cc06-45d9-9406-2374935c6c72`). He chose the recommended option, label verbatim:

> **"Yes, it covers them (Recommended)"**

It is recorded as the RULED line at opensoft/brett-wip `lanes/log/codeXfactory-2.md` line 180 (commit `20d534ccdd7610846a17badd3d02301e1e2b44d1`). It says that his 2026-10-03 word "ratify all three as disclosed" covers this packet as published in opensoft/openxFactory#1267, and the consumer packet as published in opensoft/xFactory-Hermes-Install#111.

The basis was measured. At #1267's published head `237e63a0`, four files were byte-identical to the reviewed head `b5cdf154208c1a5fd59e3936b483f37448ca85f9`:

- `design.md`;
- `specs/roles-authority-model/spec.md`;
- `implementation-handoff.md`;
- `.openspec.yaml`.

The only differences were the ratification-recording edits of `968de748` and `001a998f`: the `Status:` and `Ratified:` headers, the decision-packet record, task 2.1's note, and this file.

This confirms scope; it is not a second ratification. The ratifying commit stays `968de7487c32d6f5f630b21e5be1dddecac2d819`.

### Amendment: gate conformance only

In the same sitting, with the same timestamp, he chose the recommended option of a second question, label verbatim:

> **"Approve both (Recommended)"**

It is recorded at line 181 of the same log.

It approves three edits, made in commit `c798f1a1e22847edd321e9ceae3937740f86884c`. They bring the ratified text into line with gates that landed on main after the packet was authored. They change no requirement, decision, scope, task or design text.

1. **`proposal.md` `code_surface:`.** The head `openxFactory` is added, and the ratified text becomes its parenthesized gloss, word for word. The gates are the `code_surface` grammar, `tests/code_surface/` and `tests/estate_inventory/`.
2. **`proposal.md` `target_release:`.** The token `implementation_pending` becomes `deferred-allocation`, which is the vocabulary's value for a contract bundle whose number the versioning policy allocates at the cut. The gloss is unchanged. The gates are `scripts/validate-target-release.py` and `tests/target_release/`.
3. **`.openspec.yaml` gains an `origin: kind: ad_hoc` block.** The gate is doc-health `proposal-origin`.
   - The block's `approved_by` and `approved_on` restate the 2026-10-03 word and this confirmation. They grant no new approval.
   - `openspec/origin-dispositions.yaml` records the addition on this word.

`proposal.md` carries a matching `Amended: 2026-10-08` header line.

### What this addendum does not decide

It is not a merge, release, pin, deployment or activation word. Landing is a separate act. Brett's same-sitting word, at line 183 of the same log with the label verbatim "Proposals only, when green (Recommended)", lands #1267 once every check passes, through the lane's Rule 6 window.
