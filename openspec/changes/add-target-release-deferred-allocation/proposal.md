---
code_surface: openxFactory — `scripts/target_release.py` (the reader and judge: a third admitted token beside `implemented`, a `deferred_allocation` counter on the report, and an archived-unresolved count), `scripts/target-release-register.yaml` (its `deferred-allocation` class note, amended to record that canon now admits the value and that each standing entry retires on its own packet's correction) and `tests/target_release/test_target_release_gate.py` (new unit tests for the third value, the corpus gate re-run). NOTHING UNDER `contracts/` IS TOUCHED, no digest set moves, no schema member is added, no workflow changes (the required `pytest-suite` already runs `tests/`), and the `CLOSED_REGISTER` baseline does not move — this change admits a VALUE, and admits no ENTRY. No other packet's `proposal.md` is edited: the twelve standing `deferred-allocation` carriers are left to their owning lanes (OQ-7), and openxFactory #1017 — the first consumer, blocked today — is left to its own lane (OQ-9).
target_release: implemented (the openxFactory main line). THIS CHANGE CANNOT DECLARE THE VALUE IT ADMITS, and the reason is the admission's own rule rather than a timing accident: its code surface is a validator, a register note and a test, it cuts no contract bundle, nothing under `contracts/` moves, no `contract_bundle_version` is spent and no release tag is owed — so `deferred-allocation` would be a false declaration under the very sentence this packet writes. `gate-realization-axis-vocabulary` declared `implemented` for exactly this reason and wrote the reason into the register's own header: an exception file that could not be edited without cutting a contract release would be edited late or not at all. Under `release-realization` a non-empty code surface archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE rather than on landing, so this packet realizes through its own task list in this pull request and its realization evidence is that pull request's green `pytest-suite` run at the tree the merge carries.
sequenced_after: [add-structured-scope-substrate]
---

# Proposal: add-target-release-deferred-allocation

Status: ratified
Ratified: 2026-09-13T01:0xZ by Brett Heap (openxFactory repository owner) — verbatim "accept all A on 1022"; record at review/ratification-2026-09-13.md
Lane: hermes-wallet-exercise
Proposed: 2026-09-13, in lane `hermes-wallet-exercise` (window
`hermes-wallet-exercise`, session `codeXfactory-2`, workstation Eagle), on Brett
Heap's multiple-choice ruling of 2026-09-13 at approximately 00:5xZ, verbatim
**"(b) Author the 'deferred' vocabulary value first"**.
Origin: the successor question `gate-realization-axis-vocabulary` NAMES AND DOES
NOT TAKE — `tasks.md` § 6.1 of that packet, archived 2026-09-12 at openxFactory
[#1014](https://github.com/opensoft/openxFactory/pull/1014).

**THIS PACKET IS NOW RATIFIED.** It was filed `Status: draft` and HELD: the
word above commissioned the AUTHORING and ratified no wording, admitting no text
to canon and taking none of the ten decisions this packet carries. Every one of
them was put below as `## Open questions` OQ-1 … OQ-10, each with a RECOMMENDED
option first and the alternatives' costs written out beside it, and every
recommended option is what the delta already encodes. **Brett Heap ruled
2026-09-13T01:0xZ, verbatim *"accept all A on 1022"* — all ten at their
RECOMMENDED option (§ Rulings below), so the delta moved not one byte.** Any
other answer would have rewritten the requirement it names before ratification;
none was taken.

---

## Why

**CANON NAMED THIS GAP, MEASURED IT AT TWELVE PACKETS, AND LEFT IT OPEN ON
PURPOSE. IT IS NOW BLOCKING A RATIFIED CHANGE.**

`scripts/target-release-register.yaml`'s own header, over the twelve entries of
class `deferred-allocation`:

> The declaration names a release that EXISTS but is deliberately unnumbered,
> because the bundle's version is allocated at the cut. Under the promoted
> two-value sentence there is no spelling for "a release, not yet numbered", so
> an author obeying the versioning policy cannot also satisfy the vocabulary.
> **Whether canon should admit a deferred allocation as a third value is the
> successor question this packet names and does not take.**

The rule those twelve authors are obeying is
`docs/contract-versioning-policy.md` § Bundle Realization Order, first line:

> Contract-bundle realization is serialized and **allocates versions late**:
> 1. Fetch and rebase onto the final integration point, then immediately
>    recheck bundle/tag availability and **allocate the next available version**.

An author who named a number at proposal time would reserve one that policy
allocates at step 1 of the cut. So the promoted two-value sentence has no
spelling for a target that is real and unnumbered, and an author who needs one
must depart from one ratified rule in order to obey another.

And the register is CLOSED against solving it in code, in its own words:

> The file is CLOSED — an entry may be REMOVED when its declaration is corrected
> or its packet archives, and **an entry is never ADDED, because admitting a new
> value to the vocabulary is a canon act and not a validator edit.**

The promoted requirement says the same thing, and says where the act belongs —
which is the authority this packet stands on:

> The register SHALL be CLOSED: an entry may be REMOVED when its declaration is
> corrected or its packet archives, and **admitting a NEW value to the
> vocabulary SHALL be a change to this specification** rather than an addition
> to the register.
> — `openspec/specs/release-realization/spec.md` § *Realization axis vocabulary
> is gated*

**THIS IS THAT CHANGE TO THAT SPECIFICATION.**

## What forced it now

The gate landed on 2026-09-12 and is a RATCHET: every declaration the register
does not name is judged from the day the gate lands. The register's 21 entries
are the corpus AS IT STOOD THAT DAY. A proposal authored AFTER it — obeying the
versioning policy exactly as the twelve do — has no register entry and no
lawful spelling, so it reds the required `pytest-suite` and cannot land.

**One exists.** openxFactory
[#1017](https://github.com/opensoft/openxFactory/pull/1017)
(`encode-wallet-authority-rulings-r6-r12`) is RATIFIED — Brett Heap, 2026-09-12,
verbatim `accept all A on 1017` — and READY, and its merge word
(`merge 1017 when green`) is already given. It cannot merge:

```
tests/target_release/test_target_release_gate.py::test_corpus_target_release_validates
  openspec/changes/encode-wallet-authority-rulings-r6-r12/proposal.md:
  `contract` is outside the ratified vocabulary — `implemented` or a release
  this estate defines
```

Its declaration reads `target_release: contract bundle — … NO BUNDLE NUMBER IS
TAKEN OR RESERVED HERE`, which is the deferred allocation in a thirteenth
spelling. All three existing escapes are foreclosed, each by a ratified rule:
`implemented` would be a false declaration (its own `code_surface` moves a
`digest_subject` member — contract artifact bytes); a literal `contract-vX.Y`
would reserve a minor the versioning policy allocates at the cut; and the
register is closed against a new entry by the promoted sentence quoted above.
**The gap canon named as a successor is now a live block on a ratified change**,
which is why the successor is authored here rather than deferred again.

## What changes

**ONE NEW VALUE, TWO `## MODIFIED` REQUIREMENTS, AND A VALIDATOR THAT ADMITS
IT. NO ENTRY IS ADDED TO THE REGISTER AND NO OTHER PACKET IS EDITED.**

1. **`deferred-allocation` becomes the third value** the `target_release:`
   vocabulary admits, meaning: *a contract bundle this change realizes into,
   whose number this estate's own versioning policy allocates at the cut, so
   that no number exists to be named at proposal time.* The token is the
   register's OWN class word (OQ-1).
2. **`## MODIFIED Requirements` over *Realization axis declaration*** — the
   sentence that DEFINES the vocabulary. Its pre-text is `add-structured-scope-substrate`'s
   OUTCOME and not canon's, that change being ACTIVE and ratified and holding a
   `## MODIFIED` block over the same title; `sequenced_after:
   [add-structured-scope-substrate]` is declared, as *Ordered deltas and branch
   vocabulary* requires (OQ-2).
3. **`## MODIFIED Requirements` over *Realization axis vocabulary is gated*** —
   the gate's own restatement of the vocabulary, plus the four rules the new
   value needs and canon does not have: it is available only where a bundle is
   cut; it MUST be resolved before the packet archives; the resolving pull
   request MUST name the cut it observed; and the archive is REPORTED and still
   never judged.
4. **`scripts/target_release.py`** admits the token, counts it on the report,
   and counts archived records that still carry it unresolved. The
   `CLOSED_REGISTER` baseline **does not move** — this change admits a value,
   not an exception, which is exactly the distinction the promoted sentence
   draws.
5. **The register's `deferred-allocation` class note is amended** to record that
   canon now admits the value and that each of the twelve entries retires on its
   own packet's correction — not on this admission, the entries naming the
   tokens their authors actually wrote.

## What this proposal does NOT do

- **It does not sweep the twelve.** They are REGISTERED and green today;
  correcting another lane's declaration is that lane's act, and twelve
  `proposal.md` files across twelve active lanes is the collision surface the
  lane-collision protocol exists to avoid (OQ-7).
- **It does not edit openxFactory #1017.** That packet's one-line correction is
  its own lane's follow-up after this lands (OQ-9).
- **It does not add a register entry.** The register stays closed and its
  baseline stays where `gate-realization-axis-vocabulary` fixed it.
- **It does not touch the archive.** The 61 archived off-vocabulary records stay
  frozen, read, counted, and judged never.
- **It does not repair the "aggregation repository" wording.** That is
  `gate-realization-axis-vocabulary` `tasks.md` § 6.2's separate successor over
  the same title; folding it in would widen a ruled remedy into an unruled one.
- **It does not gate `code_surface:`.** That is § 6.3's successor, filed as
  openxFactory [#1013](https://github.com/opensoft/openxFactory/issues/1013).

## The measurement, before and after, on the real corpus

`python3 scripts/validate-target-release.py .`

| tree | exit | active | `implemented` | named release | `deferred-allocation` | registered | **refused** |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `origin/main` `a1429885` | **0** | 44 | 20 | 3 | n/a | 21 | **0** |
| THIS tree, after | **0** | 45 | 21 | 3 | 0 | 21 | **0** |

The `+1` active and `+1` `implemented` are this packet's own `proposal.md`,
judged by the gate it amends like every other active change. **The
`deferred-allocation` column is 0 on purpose**: this change admits the value and
declares no packet into it — the first consumer is #1017, whose own lane makes
that edit after this lands. Both rows are the same validator pointed at two
trees, and the `after` row is reproducible by the command above.

## Open questions

**Every recommended option below is what the delta already encodes.
`accept all A on <n>` ratifies this packet and moves not one byte of it.**

| # | decision | **(a) RECOMMENDED** | (b) | (c) |
|---|---|---|---|---|
| OQ-1 | the token's spelling | **`deferred-allocation`** — the register's own ratified class word, so the vocabulary and the register name one thing; retirement becomes mechanical (`class: deferred-allocation` ↔ `target_release: deferred-allocation`); follows the `repository-bootstrap` compound-token idiom; cannot be read as a work state | `deferred` — pairs with `implemented` as a participle, but reads as a STATE and invites the four registered `implementation_pending` carriers to "correct" into a token that does not describe them | `contract-deferred` — unambiguous, but invents a second name for a class the register already names |
| OQ-2 | where the widening is written | **BOTH promoted requirements**, `## MODIFIED` — *Realization axis declaration* (pre-text from `add-structured-scope-substrate`'s outcome, `sequenced_after` declared) and *Realization axis vocabulary is gated*. Both carry the enumeration; moving one leaves canon contradicting itself | the GATE requirement only — zero sequencing cost, but *Realization axis declaration* keeps saying the vocabulary is two values while the gate admits three | an `## ADDED` requirement over a novel title — no sequencing at all, but both promoted enumerations go stale and the vocabulary is then written in three places |
| OQ-3 | may a `deferred-allocation` change archive? | **NO** — the archiving act first resolves the token to the literal the cut allocated, or to `implemented` where no bundle was cut. A frozen record naming a number nobody allocated is the `none` defect with a better name | yes, with the token standing — the archive then carries a permanently unresolvable target | yes, with a disposition — makes the ordinary case a contested act |
| OQ-4 | how that archive rule is enforced | **Canon-enforced at the archiving act; the validator REPORTS an archived unresolved count and refuses nothing there.** Refusing would contradict the promoted *"SHALL refuse nothing there"*, and the sibling *Realization archive gate* is canon-enforced too (measured: `grep -rn 'Realization archive gate' scripts/ tests/ .github/` finds only register prose) | refuse an archived `deferred-allocation` — requires MODIFYING the never-judged sentence and creates a standing finding with no remedy on a frozen record | silent: neither report nor refusal, so nobody ever learns the rule was broken |
| OQ-5 | must the resolving edit cite the cut? | **YES** — it names the bundle version and the release surface carrying it, so the number is OBSERVED, mirroring § Bundle Realization Order steps 4–5 where the tag follows the landing | a bare token swap — indistinguishable from the reservation the policy forbids | cite only for a cut in another repository — a rule with a seam for no reason |
| OQ-6 | who may declare it | **Only a non-empty `code_surface:` whose realization lands in a contract bundle.** A value available to everybody becomes the second `none` | any change — re-opens the defect the gate was built to close | any non-empty code surface — would admit the four `realization-state` carriers this packet does not reach |
| OQ-7 | the twelve standing register entries | **NOT swept here.** Each retires when its owning packet corrects its own declaration, the entry deleted in that same pull request — which the exit-2 stale refusal already forces. Only the class NOTE is amended | sweep all twelve here (the precedent's ruled D2 shape) — twelve other lanes' `proposal.md` files plus twelve entry deletions plus a baseline move, in a packet whose realization evidence should be about the vocabulary | sweep only the quiescent lanes' — an arbitrary line nobody can re-derive later |
| OQ-8 | this packet's own `target_release:` | **`implemented`** — its surface is a validator, a register note and a test; it cuts no bundle, so `deferred-allocation` would be false under its own new sentence | `deferred-allocation` — false, and circular | omit it — but `code_surface:` is non-empty, so the doc-only default would misdescribe it |
| OQ-9 | openxFactory #1017 | **Not edited here.** Its lane makes the one-line correction after this lands; `merge 1017 when green` is already given and then applies | edit its front matter in this pull request — two lanes writing one packet | hold #1017 until its bundle is actually cut — blocks a ratified change on an unscheduled event |
| OQ-10 | where the realization lands | **THIS pull request**, mirroring `gate-realization-axis-vocabulary` exactly: non-empty `code_surface`, validator + register + tests in the same PR as the ratification, archiving later on merged-plus-green | a follow-up realization PR — leaves canon admitting a value no validator accepts, so #1017 stays blocked after ratification | — |

## Rulings

**Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — given in
session directly to this lane as a MULTIPLE-CHOICE ruling over all ten decisions
`proposal.md` § Open questions and `design.md` D1 through D10 put, and captured
in full at `review/ratification-2026-09-13.md`. The instant is recorded to the
precision the word was taken at and no finer: the minute is written `01:0xZ`
rather than invented, the same house form this packet's own filing provenance
uses for the commissioning word ("approximately 00:5xZ").

**THE WORD REACHES ALL TEN AT (a), THE RECOMMENDED OPTION, SO THE DELTA'S
WORDING STANDS UNCHANGED**: not one byte of
`specs/release-realization/spec.md` moves, and the two `## MODIFIED` blocks are
ratified exactly as authored.

| OQ | Decision | Ruled | Considered, not adopted |
| --- | --- | --- | --- |
| **OQ-1** — the token's spelling | `design.md` D1 | **RESOLVED (a) — Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — `deferred-allocation`, the register's own ratified class word, so vocabulary and register name one thing and retirement is mechanical | (b) `deferred` — pairs with `implemented` but reads as a work STATE and invites the four registered `implementation_pending` carriers to "correct" into a token that does not describe them; (c) `contract-deferred` — a second name for a class the register already names |
| **OQ-2** — where the widening is written | `design.md` D2 | **RESOLVED (a) — Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — BOTH promoted requirements, `## MODIFIED` — *Realization axis declaration* (pre-text from `add-structured-scope-substrate`'s outcome, `sequenced_after` declared) and *Realization axis vocabulary is gated* | (b) the gate requirement only — canon would then enumerate two values in one place and three in the other; (c) an `## ADDED` novel title — no sequencing, but both promoted enumerations go stale and the vocabulary is written in three places |
| **OQ-3** — may a `deferred-allocation` change archive? | `design.md` D3 | **RESOLVED (a) — Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — NO — the archiving act first resolves the token to the literal the cut allocated, or to `implemented` where no bundle was cut | (b) archive with the token standing — a permanently unresolvable frozen record; (c) archive with a disposition — makes the ordinary case a contested act |
| **OQ-4** — how that archive rule is enforced | `design.md` D4 | **RESOLVED (a) — Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — canon-enforced AT THE ARCHIVING ACT; the validator REPORTS an archived-unresolved count and refuses nothing there | (b) refuse an archived carrier — contradicts the promoted *"SHALL refuse nothing there"* and creates a standing finding with no remedy on a frozen record; (c) silent — nobody ever learns the rule was broken |
| **OQ-5** — must the resolving edit cite the cut? | `design.md` D5 | **RESOLVED (a) — Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — YES — it names the bundle version and the release surface carrying it, so the number is OBSERVED (§ Bundle Realization Order steps 4–5) | (b) a bare token swap — indistinguishable from the reservation the versioning policy forbids; (c) cite only for a cut in another repository — a seam for no reason |
| **OQ-6** — who may declare it | `design.md` D6 | **RESOLVED (a) — Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — only a change whose `code_surface:` is non-empty AND whose realization lands in a contract bundle | (b) any change — re-opens the defect the gate was built to close, a second `none`; (c) any non-empty code surface — would admit the four `realization-state` carriers this packet does not reach |
| **OQ-7** — the twelve standing register entries | `design.md` D7 | **RESOLVED (a) — Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — NOT swept here — each retires when its owning packet corrects its own declaration, the entry deleted in that same pull request, which the exit-2 stale refusal already forces; only the class NOTE is amended | (b) sweep all twelve — twelve other lanes' `proposal.md` files, twelve entry deletions and a baseline move inside a vocabulary packet; (c) sweep only the quiescent lanes' — an arbitrary line nobody can re-derive later |
| **OQ-8** — this packet's own `target_release:` | `design.md` D8 | **RESOLVED (a) — Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — `implemented` — its surface is a validator, a register note and a test; it cuts no bundle, so `deferred-allocation` would be FALSE under its own new sentence | (b) `deferred-allocation` — false, and circular; (c) omit it — but `code_surface:` is non-empty, so the doc-only default would misdescribe it |
| **OQ-9** — openxFactory #1017 | `design.md` D9 | **RESOLVED (a) — Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — NOT edited here — its own lane makes the one-line correction after this lands, and `merge 1017 when green` then applies unchanged | (b) edit its front matter in this pull request — two lanes writing one packet; (c) hold #1017 until its bundle is actually cut — blocks a ratified change on an unscheduled event |
| **OQ-10** — where the realization lands | `design.md` D10 | **RESOLVED (a) — Brett Heap, 2026-09-13T01:0xZ, verbatim "accept all A on 1022"** — THIS pull request, mirroring `gate-realization-axis-vocabulary` exactly: validator, register note and tests beside the ratification, archiving later on merged-plus-green | (b) a follow-up realization PR — leaves canon admitting a value no validator accepts, so #1017 stays blocked after ratification |

**EVERY RULING IS THE RECOMMENDED OPTION.** No requirement text was rewritten,
no delta directory was renamed, no `sequenced_after:` entry moved, and
`scripts/target-release-register.yaml`'s `CLOSED_REGISTER` baseline did not
move — this act admits a VALUE and admits no ENTRY. Realization (§ 2 of
`tasks.md`) rides in this same pull request per OQ-10; the ARCHIVE (§ 5) stays
entirely open, held behind merged-plus-green realization evidence, its own word,
and the § 5.2 ordering re-read against `add-structured-scope-substrate`. Merge
is a separate word from this ratification, and Rule 6 applies at landing.
