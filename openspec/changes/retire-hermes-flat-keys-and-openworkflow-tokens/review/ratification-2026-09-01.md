# Proposal Ratification: retire-hermes-flat-keys-and-openworkflow-tokens

Status: ratified
Decision date: 2026-09-01
Ratifier: Brett Heap (repository owner) — in-session, on the orchestrator's
report of the two packets read together
Ratified: 2026-09-01 by Brett Heap (repository owner) — in-session; record: this
file.
Ratified baseline: **this packet AS FILED at pull request #551 tip
`64907604`** — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/contract-deprecation-execution/spec.md` (**FOUR ADDED requirements over
22 scenarios, no `## MODIFIED Requirements` block anywhere**), validated
`--strict` and `--all --strict`. The commit carrying this record moves **no requirement text**:
it adds this file and flips the packet's self-description from draft to
ratified, and nothing else.

## Decision

**RATIFY.** The requirement set stands as it is at `64907604`.

This packet carries **entries 1 and 2 of openxFactory issue #522** — the
`hermes` flat keys, split as ruled into a phased half that EXECUTES and a
refusing half that is RECORDED-WHY, and the `openworkflow`-prefixed tokens,
which EXECUTE. It adds ONE capability, `contract-deprecation-execution`, whose
first two requirements are the general obligations the mechanism never carried
(execute-at-the-major-or-restate; write the entry from the REFUSAL LIST, and an
unwarned shape is not phased) and whose last two discharge those obligations
against these two entries.

**Ratification authorizes the requirement text. It performs nothing.** No
validator line moves, no policy row moves, no changelog row moves, no bundle
number is spent, and `contracts/` is untouched by the ratified diff.

---

## 1. The chain of authority, as THREE acts and not one

They are recorded separately because collapsing them would misstate what each
authorized. Each is a smaller thing than the next.

| # | Act | Date | What it authorized |
|---|---|---|---|
| 1 | **Issue #522 FILED**, on Brett Heap's word — *"file the deprecations issue"* | 2026-08-30 (filed 2026-08-31T01:06Z) | The SUBJECT existed as repository business. It authorized no disposition: the issue's own scope line says *"either execute the three retirements … or record why each stays In Force"*, and leaves the choice open. |
| 2 | **Brett Heap's RULING**, in session, recorded as a comment on issue #522 — *"execute all three retirements at contract-v3.0, as the memo recommends"*, entry 1 **SPLIT**, entry 2 **EXECUTE**, entry 3 **EXECUTE, its own slice** | 2026-09-01 | The DISPOSITION, and the authoring of proposals to carry it. It adopted the memo's recommendations; it ratified no text, because no text existed when it was given. |
| 3 | **THIS RATIFICATION** — *"ratify #551 and #552"*, in session | 2026-09-01 | The requirement text of the two packets **as filed at their then-current tips** (#551 `64907604`, #552 `c5169476`). |

**Act 2 is not act 3, and this record does not let the packet claim otherwise.**
The `Origin:` field and `.openspec.yaml`'s `approved_by` both said in terms that
the ruling *"authorizes the proposals; it does not ratify this text"* — a
disclaimer written while act 3 was still outstanding, and it was accurate. Act 3
has now been given, separately, and it is what this file records.

## 2. What Brett was told before he ruled, stated exactly

His ratification followed an orchestrator's report that put the two packets
before him **together**. The report carried:

1. **The two proposals as filed** — #551 at `64907604`, #552 at `c5169476`.
2. **FOUR authoring findings where the investigation memo did not survive the
   tree.** Three of them are this packet's:
   * **The flat-key retirement is a REPLACEMENT, not a deletion.** The
     `hermes.layers missing required role` errors sit INSIDE the
     `if isinstance(declared, list)` branch, so deleting the `else` arm alone
     lets a `layers`-less stack fall through with an empty map and produce no
     finding at all — a silent WIDENING at a major. The removal owes one
     explicit error naming the missing or non-list `hermes.layers`.
   * **The `openworkflow` prefix is UNDER-DECLARED by one character, and the
     refusal list must be written BY PATH.** The policy entry and the validator
     docstring write `openworkflow_`; the code writes
     `token.startswith("openworkflow")`. And `domain_overlay` is ALSO a live,
     non-deprecated key under `omnigent:` — declared by all five supported
     consumers and read by the validator — so a refusal list written by key NAME
     would refuse, at a major and with no warning ever served, a shape the whole
     supported population legitimately carries. The deprecated key is
     `hermes.domain_overlay` and nothing else.
   * **The D4 canon/code divergence is RECORDED AND NOT FIXED.** Promoted canon
     says an unresolvable `owner_layer` is a WARNING; the shipped validator has
     ERRORED since six days before that requirement was promoted. This packet
     records it, files it as its own issue (`tasks.md` § 6.1), and does not
     resolve it.

   The fourth belongs to the sibling and is recorded in ITS ratification record:
   entry 3's packaged corpus is TWELVE fixtures, not four, eight of them
   negative and carrying seven refusal classes with no `-v2` equivalent.
3. **The sibling's `serve.py` fallback decision as encoded** — the surviving v2
   failure envelope with an explicit unknown-kind code where a wire-valid
   `client_turn_id` exists, and the pre-identity shape where it does not. That
   decision is the sibling's and is ratified there, not here.
4. **The Codex provider-refusal** — see § 3.
5. **The inherited `pytest-suite` red standing on `main`** — see § 4.

**He ratified against that disclosed state.** Nothing in this record is a fact
he was not given.

## 3. THE REVIEW STATE, AND WHAT IT IS NOT

**NO CODEX REVIEW OF THIS PACKET HAS HAPPENED, AND THIS RECORD MAKES NO CLAIM
THAT ONE DID.**

`@codex review` was requested on #551 four times across the arc — the automatic
request on open plus three explicit ones — and **every request returned a
PROVIDER REFUSAL**, not a verdict:

| time (UTC) | response |
|---|---|
| 03:52:18 | *"You have reached your Codex usage limits for code reviews."* |
| 04:00:44 | same |
| 04:07:22 | *"You have reached your Codex usage limits."* |
| 04:07:25 | *"You have reached your Codex usage limits for code reviews."* |

**Four refusals, zero verdicts, and zero Codex reviews naming any head of this
branch.** The refusal is the provider's usage ceiling. **It is not a finding, not
a silence basis, and not evidence of anything about the packet.**

**A CODEX PASS REMAINS OWED, AND IS BLOCKED BY NOTHING IN THIS PACKET.** When the
ceiling lifts, the pass is takeable against the ratified head with no
precondition. Anything it returns routes to the **amendment lane** — the same
disposition every ratification in this repository carries — and not to doubt
about this act, which is sound on what was known and disclosed.

**What review DID run, and what it returned.** Six Copilot rounds ran, one
against each of this pull request's six heads. (Sourcery returned an access-tier
upsell, not a review.) Every finding was taken, and two of them corrected the
packet's own subject rather than its prose:

* **Entry 2's entry under-declares its own prefix by one character** — accepted,
  pushed at `bcd0c568`, and promoted into the packet's argument, because it makes
  the refusal-list rule apply to BOTH entries rather than only to the flat keys.
* **The committed host-absolute memo path** — the review was RIGHT and the first
  answer to it was WRONG. Principle IV forbids a host-absolute path in a committed
  file; the memo is now **NAMED and not located** at every site
  (`f5c4b70f`), with issue #522 and its ruling comment standing as the durable
  in-repo referents.

The final round, against the ratified head `64907604`, **generated no new
comments**. One self-catch also landed in the arc, at `2becc22e`: the
replacement-not-deletion finding at § 2, which was this session's own and not any
reviewer's.

## 4. THE INHERITED CI STATE, DISCLOSED RATHER THAN INHERITED SILENTLY

**`main` IS RED on `pytest-suite`, and it was red before this branch existed.**
It is red at `1a69b7cb` and still red at `1c1dcbbe`, from **PR #510's**
carriage-ledger subject.

```
FAILED tests/doc-health/test_modified_block_currency_self_gate.py::test_every_carriage_ledger_finding_over_the_real_tree_is_named
  0 named subject(s) NO LONGER reported []
  1 unnamed subject(s) NEWLY reported
    [('add-chain-attestation', 'signed-execution-chain',
      'A gate validates the short chain as a hash-linked chain')]
```

#510 added that subject to the real tree without updating `_LEDGER_SUBJECTS`,
which the assertion compares as an EXACT SET.

**EXACTLY ONE FAILURE, AND IT IS #510'S SUBJECT.** The CI run on this pull
request reports `1 failed, 8363 passed` — the same single inherited failure and
no other. That is the expected result and it is structural, not lucky: the family
reports a subject only when a `## MODIFIED` block DROPS a canon body unit or
scenario bullet, and **this packet carries no MODIFIED block at all**, so it can
add no carriage-ledger subject.

**It is NOT fixed here.** The fix belongs to whoever moved the set. The other
three required checks — `merge-master-approval`, `wallet-validation`,
`signed-execution-chain-gate` — are green.

## 5. What this ratification does NOT authorize

- **No realization.** `tasks.md` §§ 2–5 are authorized and not performed. No
  line of `scripts/validate-domain-factory.py` or `scripts/apply-domain-starter.py`
  moves, and no row of `docs/contract-versioning-policy.md` moves, by this act.
- **No `contract-v3.0` cut.** The cut is its own act under § Bundle Realization
  Order, with the version confirmed at realization, every gate run against an
  unchanged candidate, and the annotated tag published and verified from an
  independently refreshed checkout. **This ratification spends no number and
  moves no CHANGELOG row.**
- **No archive.** This change has a CODE SURFACE, so under `release-realization`
  it archives ONLY on merged plus green realization evidence, never on landing.
  It stays ACTIVE.
- **No merge of this pull request.** That is a separate act and it is not
  performed by this record.
- **No Codex verdict.** § 3. The absence is disclosed, not converted into a
  basis.
- **No fix of the inherited `main` red.** § 4.
- **No disposition of OQ-1, OQ-2 or OQ-3.** They are named for the cut and the
  cut answers them. In particular, whether `contract-v3.0` carries this packet,
  the sibling, or both is the cutting session's decision and not this one's.
- **No resolution of the D4 canon/code severity divergence**, which is recorded,
  filed (`tasks.md` § 6.1) and deliberately out of scope.
- **No refusal of the co-resident `hermes` flat keys.** Entry 1's refusing half
  is RECORDED-WHY and stays In Force with a restated target of `contract-v4.0`,
  conditioned on the deprecating minor it owes. Brett's ruling on that half was
  *"not this, not yet"*, and this ratification does not widen it.

## 6. Next

Adversarial review stays open — a Codex pass is owed and unblocked (§ 3).
Realization is `tasks.md` §§ 2–5 and is a later commission. The D4 issue at
§ 6.1 rides along regardless. The sibling `retire-doxbench-chat-turn-v1` was
ratified in the same act, at `c5169476`, and carries its own record.
