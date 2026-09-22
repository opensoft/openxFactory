---
code_surface: none — MEASURED on `main` `4f92d651`, not assumed. Both deltas are requirement prose, and the running code ALREADY BEHAVES THE WAY THE AMENDED TEXT READS. THIS PACKET'S WHOLE DIFF IS CORPUS TEXT: its own six files (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, TWO `## MODIFIED` spec deltas, and `review/verify-carriage.py` — the carriage proof that re-extracts the promoted scenarios and compares them, committed inside the packet so the proof is reproducible from this checkout alone), one README *Active changes* bullet, and the machine-seeded per-change row in `tests/sequenced_after/corpus-ledger.yaml` that every filing owes. **`review/verify-carriage.py` IS NOT A CODE SURFACE and the distinction is the corpus's own, not this packet's convenience** (Copilot `r4076010268`): it sits under no import path, is not under `scripts/` or `tests/`, is read by no gate, is imported by nothing — `grep -rIn verify-carriage scripts/ .github/ tests/` returns nothing — and runs only when a human runs it. The precedent is exact and is the packet that promoted `openxfactory-engineering-adapter`: `repromote-engineering-vocabulary` (archived 2026-09-18) declared `code_surface: none` while committing `review/build-delta.py`, glossed in those same terms. NOT ONE CHARACTER OF THE REPOSITORY'S RUNTIME CODE MOVES — no validator, no verifier under `scripts/`, no test under `tests/`, no contract, no workflow. Evidence, each check run rather than asserted. (1) NOTHING ENFORCES THE CLAUSE BEING SCOPED. `grep -rIn "corpus-adapter-seam" scripts/ tests/ contracts/ .github/` returns ten lines and EVERY ONE names requirement 3 (the governed write path) or requirement 4 (the no-privileged-route rule): `route_extension.py:56`, `verify-carve-conformance.py:10` and `:214`, `corpus_adapter_openxfactory/write_path.py:15` and `shape.py:4` and `:15`, `tests/corpus-adapter/test_conformance.py:10`, `test_no_privileged_route.py:3` and `:119`, `test_no_home_vocabulary.py:26`. **Not one names requirement 1.** No test asserts that a corpus reader is external, is pinned, or appears in a `contracts/*-pin.yaml`; the forty-odd test functions across `tests/corpus-adapter/`'s 1,805 lines test the interface's shape, the fail-closed behaviour, the write path and the absence of a privileged route. (2) THE HOME ADAPTER'S OWN SOURCE ALREADY READS REQUIREMENT 4 AS ITS GOVERNING RULE, which is what the seam amendment writes into requirement 1: `scripts/corpus_adapter_openxfactory/shape.py:3-7` — *"THE ONE DESIGN DECISION THAT MAKES THE SEAM'S FOURTH REQUIREMENT TESTABLE. `corpus-adapter-seam`'s fourth requirement forbids openxFactory's own adapter any route the interface does not define"*. (3) NOTHING COUNTS AXES. `grep -rInE "five axes|exactly five"` over the repository returns no hit in `scripts/` or `tests/` that names `domain-mapping-declaration`; no validator, loader or test enumerates the declaration's axes or asserts their number. (4) THE REALIZED PROFILE ALREADY CARRIES SIX, so the count amendment makes a conformant artifact conformant and cannot make a conformant one fail: `contracts/domain-profiles/openxfactory-engineering.yaml` carries `artifact_kinds:`, `lifecycle:`, `gates:`, `acts:`, `evidence_classes:`, `authorities:` under its own `AXIS 1`..`AXIS 5` banners, and then `truth_store:` at line 415 — top level, sibling to the five, with `external_enforcement_point:` nested inside it at :417 and under NO axis banner of its own — while `DomainProfile`'s fields are `mapping_id`, `artifact_kinds`, `lifecycle`, `acts`, `evidence_classes`, `authorities`, `truth_store`, `neutral`, `domain_label`, `declared_by`, `gates`, `basis`, `notes`, `source`, `extra` (`tests/test_engineering_profile_display_facet.py:300-303`). BOTH AMENDMENTS ARE THEREFORE DOCTRINE-ONLY: they make the normative text agree with artifacts and readers that have behaved this way since they were written, and an artifact conformant before this lands is conformant after it. Under `release-realization` an empty code surface archives ON LANDING plus this task list rather than on merged-plus-green realization evidence.
target_release: implemented — the value `release-realization` names for a doc-only change. No contract bundle is cut, nothing under `contracts/` is edited, no `contracts/manifest.yaml` row moves, no digest inventory is recomputed and no consumer's pin has to advance to receive this. The realization of a wording amendment IS its promotion at archive, which is a separate act on a separate word.
sequenced_after: [split-opendox-two-layer-product]
---

# Proposal: amend-home-adapter-scope-and-mapping-axis-count

Status: draft
Kind: proposal
Proposed: 2026-09-22, in lane `openxfactory-4` (display
`openXfactory-4-openDox_extraction`), actor `successor2`.
Origin: Copilot review
[`5273796676`](https://github.com/opensoft/openxFactory/pull/1139#pullrequestreview-5273796676)
on `opensoft/openxFactory`
[#1139](https://github.com/opensoft/openxFactory/pull/1139) — the archive of
`split-opendox-two-layer-product`, merged `e8fde27f` — comments
[`r4067852518`](https://github.com/opensoft/openxFactory/pull/1139#discussion_r4067852518)
and
[`r4067955892`](https://github.com/opensoft/openxFactory/pull/1139#discussion_r4067955892),
registered as REAL by the archiving lane at
[#1139 comment `5770749761`](https://github.com/opensoft/openxFactory/pull/1139#issuecomment-5770749761).

**NOTHING HERE IS RATIFIED BY THE AUTHORING LANE.** Both amendments touch
requirement text that Brett Heap ratified on 2026-09-05 (verbatim *"ratify
#666"*), and this lane's standing rule is that non-normative fixes may be folded
as an addendum while **requirement and scenario text goes to Brett Heap as a
ruling and is amended on his word** (the 2026-09-01 precedent). This packet is
the instrument that ruling would use; it is not the ruling.

## The set this packet closes

Review `5273796676` raised six findings. Three were facts about text `#1139`
itself wrote and were fixed there (`dee01d9c`). Three named RATIFIED requirement
text in three different capabilities — text `#1139` promoted verbatim out of the
ratified delta and did not author. One of those three,
[`r4067852551`](https://github.com/opensoft/openxFactory/pull/1139#discussion_r4067852551)
on `neutral-product-pin`, was ruled by Brett Heap at
[`#656` comment `5777949892`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5777949892)
(*"(b) — AMEND THE CLAUSE"*) and landed as `#1140` -> `e90997bc`. **The remaining
two are this packet.** With it the set of four findings that review registered
is closed, and the count is stated here so it can be checked rather than
trusted.

**EACH WAS RE-MEASURED AGAINST THE LANDED TEXT BEFORE A WORD WAS WRITTEN**, on
the standing that a finding wrong on the landed text is answered by measurement
and not by an amendment. Both hold. The measurements are below and each is
re-runnable.

## Finding 1 — `corpus-adapter-seam`: "every tool", and the tool the estate is required to keep

**The finding, in its own terms** (`r4067852518`): *"The `every tool` wording
makes the required local adapter non-conformant: `scripts/corpus_adapter_openxfactory`
is intentionally authored beside `doc_health` and is the implementation required
by the fourth requirement. Scope this rule to externally consumed readers or
explicitly exempt the home adapter; otherwise requirements 1 and 4 cannot both
be satisfied."*

**It holds, and it holds harder than the finding states.** The promoted first
requirement carries TWO clauses, and the home adapter fails both ways:

| clause, as promoted | the home adapter, measured on `main` `4f92d651` |
| --- | --- |
| *"SHALL consume every tool that reads its governed corpus as an EXTERNAL NEUTRAL PRODUCT pinned under `neutral-product-pin`"* | `scripts/corpus_adapter_openxfactory/` is in this repository's own tree and is named in NO `contracts/*-pin.yaml` — `grep -rn "corpus_adapter" contracts/` returns nothing. It is neither external nor pinned. |
| *"no neutral product `openxFactory` pins SHALL import `openxFactory`'s own tooling"* | It imports `doc_health` at SIX sites across four modules (`adapter.py:58`, `check.py:39-41`, `classify.py:38`, `home.py:59`) and `ideation_dashboard.intent_apply_lane` lazily at two (`write_path.py:134`, `:152`). |

**So the escape the first clause appears to offer is closed by the second.** A
reader who took "pin it" as the remedy would move the adapter into a pinned
product and immediately violate clause two, because RULING DQ-1 puts it *beside*
`doc_health` on purpose — verbatim: *"doc-health and OpenSpec stay in
openxFactory, and a small adapter package beside them implements the
corpus-adapter seam; `codexDox` becomes a thin descendant that pins openXdox and
reuses that adapter"*. The archived packet's own delta header says DQ-1 is what
makes the fourth requirement *"load-bearing rather than precautionary"*. What it
never did was go back and scope the first.

**And the estate has already been reading it the amended way.** Every reference
to this capability in running code names requirement 3 or requirement 4; not one
names requirement 1 (front-matter evidence (1)). The home adapter's own module
docstring names requirement 4 as the rule it is built to satisfy. A second
promoted capability, `openxfactory-engineering-adapter`, exists solely to carry
that adapter's obligations and says so: *"RULING DQ-1 kept that adapter and that
vocabulary HERE when the document-and-ideation workbench left"*.

**The minimum text that makes the requirement true** is therefore an exception
that is NAMED and BOUNDED: the home adapter DQ-1 keeps, governed by requirement 4
and by `openxfactory-engineering-adapter` in requirement 1's place; not a general
"openxFactory-authored" carve-out, which would let a second in-repository reader
escape the rule and reopen the vendoring hole the requirement's own third
scenario closes. The one-way dependency rule, the relocation rule, the measured
back-edge instance and all three promoted scenarios are carried unedited.

## Finding 2 — `domain-mapping-declaration`: "exactly five axes", and the sixth the corpus already declares

**The finding, in its own terms** (`r4067955892`): *"This requirement says a
declaration covers exactly five axes, but the third requirement additionally
mandates a truth store and an external enforcement point for every derived-model
family without assigning either field to one of those five axes.
`governed-derived-model` already treats truth store as its own dial, so an
implementation cannot tell whether these are a forbidden sixth axis or nested
data. Define that nesting or revise the axis list before consumers implement the
profile shape."*

**It holds, and the realized artifact has already answered it — the other way
from the promoted text.** `contracts/domain-profiles/openxfactory-engineering.yaml`,
the one realized declaration in the estate, carries:

- `AXIS 1` .. `AXIS 5` comment banners at lines 76, 146, 360, 395, 405, over
  `artifact_kinds:`, `lifecycle:`, `gates:` + `acts:`, `evidence_classes:` and
  `authorities:` — the five;
- then `truth_store:` at line **415**, top level, sibling to all five, with
  `external_enforcement_point:` nested inside it at :417, **under no axis banner
  at all**; and its own `description:` citing the requirement that mandates it:
  *"Named by `domain-mapping-declaration`'s third requirement itself"*.

`DomainProfile` carries `truth_store` as its own field beside `artifact_kinds`,
`lifecycle`, `acts`, `evidence_classes` and `authorities`
(`tests/test_engineering_profile_display_facet.py:300-303`). **So the
implementation treats it as a sixth axis, the promoted requirement says there
are exactly five, and nothing in the corpus reconciles them.** The amendment
states the count the corpus already keeps, and says in normative text which of
the two readings the finding names — *forbidden sixth axis* or *nested data* —
is right.

**The minimum text** is the axis list itself: six rather than five, the sixth
named as the DERIVED-MODEL BOUNDARY, its content deferred to the requirement
that already states it in full, and one sentence saying it is an axis of THIS
declaration rather than a field of `governed-derived-model`'s own dial. The
third requirement is not edited: this packet adds no obligation, it names one
the corpus already carries. All three promoted scenarios are carried unedited.

## What this packet does not do

- **It does not touch the archive.** `openspec/changes/archive/2026-09-22-split-opendox-two-layer-product/`
  is not edited. The delta it holds is what Brett Heap ratified on 2026-09-05 and
  it stays that way; amending PROMOTED text is a forward act, not a rewriting of
  the record.
- **It does not amend `corpus-adapter-seam`'s requirements 2, 3 or 4**, nor
  `domain-mapping-declaration`'s requirements 2 or 3. Two clauses are in scope
  and the blocks reach nothing else.
- **It does not answer `r4067852551`.** That finding was ruled and landed
  separately as `#1140`; it is named here only so the set of four is countable.
- **It does not fix two stale strings it found**, and says so rather than
  folding them in: `contracts/domain-profiles/openxfactory-engineering.yaml`'s
  `basis:` entry cites *"the five axes"* at a path
  (`openspec/changes/split-opendox-two-layer-product/...`) that the 2026-09-22
  archive moved, and `README.md`:3270 describes the promoted capability as *"3
  requirements: the five axes"*. The first is a contract edit and would give a
  doctrine-only packet a code surface for a stale citation the archive left, not
  this amendment; the second is a README narrative line about what the archived
  packet promoted. Both are registered at `tasks.md` § 5.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
