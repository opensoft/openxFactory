# Proposal Ratification: retire-doxbench-chat-turn-v1

Status: ratified
Decision date: 2026-09-01
Ratifier: Brett Heap (repository owner) — in-session, on the orchestrator's
report of the two packets read together
Ratified: 2026-09-01 by Brett Heap (repository owner) — in-session; record: this
file.
Ratified baseline: **this packet AS FILED at pull request #552 tip
`c5169476`** — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/ideation-dashboard/spec.md` (**TWO ADDED requirements over 12 scenarios,
plus ONE scenario-complete `## MODIFIED` requirement over 7 scenarios**),
validated `--strict` and `--all --strict`. The commit carrying this record moves
**no requirement text**: it adds this file and flips the packet's
self-description from draft to ratified, and nothing else.

## Decision

**RATIFY.** The requirement set stands as it is at `c5169476`.

This packet carries **entry 3 of openxFactory issue #522** — the doxBench
chat-turn v1 envelope family — **as its own slice**, which is the ruling's own
disposition and not an authoring preference. It is the only one of the three
entries whose warning actually fires, and the only one that moves a
digest-pinned schema's bytes, an inventory member's digest, twelve packaged
fixtures, a committed byte-identity baseline test and a server posture that must
be REDESIGNED rather than deleted.

**Ratification authorizes the requirement text. It performs nothing.** No schema
byte moves, no fixture is deleted, no manifest digest changes, no bundle number
is spent, and `contracts/` is untouched by the ratified diff.

---

## 1. The chain of authority, as THREE acts and not one

They are recorded separately because collapsing them would misstate what each
authorized. Each is a smaller thing than the next.

| # | Act | Date | What it authorized |
|---|---|---|---|
| 1 | **Issue #522 FILED**, on Brett Heap's word — *"file the deprecations issue"* | 2026-08-30 (filed 2026-08-31T01:06Z) | The SUBJECT existed as repository business. It authorized no disposition: the issue's own scope line says *"either execute the three retirements … or record why each stays In Force"*, and leaves the choice open. |
| 2 | **Brett Heap's RULING**, in session, recorded as a comment on issue #522 — *"execute all three retirements at contract-v3.0, as the memo recommends"*, entry 3 **"EXECUTE, its own slice"**, with the `serve.py` v1-fallback posture **"redesigned, not deleted"** | 2026-09-01 | The DISPOSITION, the SLICING, and the authoring of a proposal to carry them. It ratified no text, because no text existed when it was given. |
| 3 | **THIS RATIFICATION** — *"ratify #551 and #552"*, in session | 2026-09-01 | The requirement text of the two packets **as filed at their then-current tips** (#551 `64907604`, #552 `c5169476`). |

**Act 2 is not act 3, and this record does not let the packet claim otherwise.**
The `Origin:` field and `.openspec.yaml`'s `approved_by` both said in terms that
the ruling *"authorizes the proposal; it does not ratify this text"* — a
disclaimer written while act 3 was still outstanding, and it was accurate. Act 3
has now been given, separately, and it is what this file records.

**Act 2 set the fallback's DIRECTION; act 3 ratifies its ENCODING.** The ruling
said *"redesigned, not deleted"* and stopped there. What replaces the coercion is
this packet's own decision, and § 2.2 records that it was put to him as such.

## 2. What Brett was told before he ruled, stated exactly

His ratification followed an orchestrator's report that put the two packets
before him **together**.

### 2.1 The four authoring findings where the memo did not survive the tree

One of the four is this packet's, and it is the largest single thing the memo's
pricing missed:

* **The packaged corpus is TWELVE fixtures, not four.** The memo counted the four
  positive `.example.yaml` files — the four the default validator run warns on —
  and missed the **eight NEGATIVE fixtures** that also declare v1 kinds. Those
  eight carry **SEVEN refusal classes with NO `-v2` equivalent**: escaping path,
  hash mismatch, identity subject, over budget, unknown model, untyped proposal,
  and duplicate turn pair. The surviving family's own ten negatives cover a
  DIFFERENT set. **Retiring the family without re-expressing them silently
  deletes seven refusals from the packaged corpus**, which is how a refusal stops
  being tested without anyone deciding it should. D2 makes each one either a
  re-expressed `-v2` negative or a stated coverage loss with a reason, and says
  in terms that silence is not a third option.

The other three belong to the sibling and are recorded in ITS ratification
record: the flat-key retirement being a REPLACEMENT and not a deletion; the
`openworkflow` prefix under-declaration together with the by-path refusal list
that must exclude the legitimate `omnigent.domain_overlay`; and the D4 canon/code
severity divergence, recorded and deliberately not fixed.

### 2.2 The `serve.py` fallback decision AS ENCODED

Put to him as this packet's own decision rather than as a consequence of the
ruling, because it is one:

> An unrecognized or absent chat-turn `kind` is answered in the **surviving
> `-v2` failure envelope**, carrying an **explicit unknown-kind error code**
> registered in the server's error catalog, **whenever the request carries a
> wire-valid `client_turn_id`**. Where it does not, the existing **pre-identity
> refusal shape** answers, **unchanged**.

Three properties of it were reported with it, and each is a measurement rather
than a hope:

* **It is legal on the contract as it stands.** `$defs/failure_v2` constrains
  `error` by a lowercase-identifier PATTERN and by no enum, at the schema layer
  AND at the delegated validator layer. The only closed list is `serve.py`'s own
  `DOXBENCH_ERROR_CATALOG`. **No schema widening is needed and none is proposed**
  — the only schema movement in this change is REMOVAL.
* **It does not violate the no-invented-identity rule.** The pre-identity arm
  exists precisely because `failure_v2` requires a `client_turn_id` that no
  server may invent.
* **There are TWO fallback layers, not one** — the second memo correction. The
  lower one, `_refuse_turn`'s drop into the pre-identity shape, is **correct,
  untouched and not redesigned**. Naming it matters because a redesign that
  ignored it would either duplicate it or break the rule above.

The rejected alternative — refuse every unrecognized kind OUTSIDE any contract
envelope — was reported with the three costs that defeat it.

### 2.3 The rest of the report

**The Codex provider-refusal** (§ 3) and **the inherited `pytest-suite` red
standing on `main` from PR #510's carriage-ledger subject** (§ 4).

**He ratified against that disclosed state.** Nothing in this record is a fact he
was not given.

## 3. THE REVIEW STATE, AND WHAT IT IS NOT

**NO CODEX REVIEW OF THIS PACKET HAS HAPPENED, AND THIS RECORD MAKES NO CLAIM
THAT ONE DID.**

`@codex review` was requested on #552 across the arc — the automatic request on
open plus explicit ones — and **every request returned a PROVIDER REFUSAL**, not
a verdict:

| time (UTC) | response |
|---|---|
| 04:00:28 | *"You have reached your Codex usage limits for code reviews."* |
| 04:00:43 | same |
| 04:07:27 | same |

**Three refusals on this pull request, four on the sibling, zero verdicts, and
zero Codex reviews naming any head of this branch.** The refusal is the
provider's usage ceiling. **It is not a finding, not a silence basis, and not
evidence of anything about the packet.**

**A CODEX PASS REMAINS OWED, AND IS BLOCKED BY NOTHING IN THIS PACKET.** When the
ceiling lifts, the pass is takeable against the ratified head with no
precondition. Anything it returns routes to the **amendment lane** — the same
disposition every ratification in this repository carries — and not to doubt
about this act, which is sound on what was known and disclosed.

**What review DID run, and what it returned.** Three Copilot rounds ran, one
against each of this pull request's three heads. (Sourcery returned an
access-tier upsell, not a review.) Every finding through round two was taken:

* **The two measurement baselines read as a conflict** — accepted by
  DISAMBIGUATING rather than by aligning (`5219332e`). `4290cad2` is what the
  memo measured and what the ruling adopted; `1a69b7cb` is what this packet
  re-verified against. They are two acts, and the packet now says so rather than
  collapsing them to one SHA.
* **The committed host-absolute memo path** — the review was RIGHT and the first
  answer to it was WRONG. Principle IV forbids a host-absolute path in a
  committed file; the memo is now **NAMED and not located** at every site
  (`c5169476`), with issue #522 and its ruling comment standing as the durable
  in-repo referents.

**THE FINAL ROUND'S FINDINGS STAND OPEN ON THE RATIFIED HEAD, AND ARE LISTED
HERE RATHER THAN PASSED OVER.** Round three, against `c5169476`, posted **two
comments** and suppressed **two more**. All four are low-severity and none is
blocking, but all four are real:

| site | finding | class |
|---|---|---|
| `README.md:1508` | the record row names `validate-ideation-dashboard-contracts.py` without its `scripts/` prefix | citation |
| `tasks.md:8` | the header says *"Sections 2-6 are the realization"*, but § 6 is the cut (a separate act the same header names as such) and § 7 is post-cut verification | internal range |
| `README.md` (suppressed) | `$def` written for `$defs` in one sentence | spelling |
| `tasks.md` 3.6 (suppressed) | the shipped-client citation drops its `scripts/ideation_dashboard/` prefix | citation |

**NONE OF THEM IS CORRECTED BY THIS ACT**, and the reason is the ratification's
own discipline rather than convenience: ratification is not an editing pass, and
correcting the text here would produce a head other than the one Brett ruled on.
They route to the **amendment lane** with anything Codex later returns.

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
no other.

**That result is load-bearing here in a way it is not on the sibling**, because
**this packet DOES carry a `## MODIFIED` block**. The family reports a subject
only when a MODIFIED block DROPS a canon body unit or scenario bullet; this
block restates all four canon scenarios with every bullet and carries the body
paragraph verbatim, so it drops nothing, owes no `Removed from canon` marker,
and adds no carriage-ledger subject. `tasks.md` 1.4 records the same check run
directly on this branch. **The absence of a second failure is the evidence, and
it holds.**

**It is NOT fixed here.** The fix belongs to whoever moved the set. The other
three required checks — `merge-master-approval`, `wallet-validation`,
`signed-execution-chain-gate` — are green.

## 5. What this ratification does NOT authorize

- **No realization.** `tasks.md` §§ 2–7 are authorized and not performed. Not one
  schema byte, fixture, dispatch arm, catalog entry or test file moves by this
  act.
- **No `contract-v3.0` cut.** The cut is its own act under § Bundle Realization
  Order. **This ratification spends no number, moves no manifest digest, rebuilds
  no inventory and moves no CHANGELOG row.**
- **No archive.** This change has a CODE SURFACE and moves schema bytes, so under
  `release-realization` it archives ONLY on merged plus green realization
  evidence — including the moved manifest digest, the rebuilt inventory, and the
  published annotated tag verified from an independently refreshed checkout. It
  stays ACTIVE.
- **No merge of this pull request.** That is a separate act and it is not
  performed by this record.
- **No Codex verdict**, and no correction of the two open low-severity comments
  on the ratified head. § 3. Both absences are disclosed, not converted into a
  basis.
- **No fix of the inherited `main` red.** § 4.
- **No change to the surviving `-v2` family's shape.** Not one field is added,
  removed or renamed by anything ratified here.
- **No removal of the pre-identity refusal layer**, which is correct and stays.
- **No disposition of OQ-1 through OQ-4.** In particular the unknown-kind code's
  exact token and HTTP status (OQ-3) are the realization's to pick and register;
  ratifying the POSTURE does not name the token. And whether `contract-v3.0`
  carries this packet, the sibling, or both (OQ-1) is the cutting session's
  decision, not this one's.
- **No answer to OQ-4.** Whether an external doxBench client is pinned to v1 is
  the one measurement the memo wanted and could not perform. It is an ABSENCE of
  evidence and is named as one; if the answer turns out to be yes, this becomes
  record-why-it-stays until that client migrates, and under § Compatibility
  Direction such a client stays valid at its pin regardless.

## 6. Next

Adversarial review stays open — a Codex pass is owed and unblocked (§ 3), and two
low-severity comments stand on the ratified head. Realization is `tasks.md`
§§ 2–7 and is a later commission; D2's seven refusal classes and D3's measured
reference closure are its two hardest obligations. The sibling
`retire-hermes-flat-keys-and-openworkflow-tokens` was ratified in the same act,
at `64907604`, and carries its own record.
