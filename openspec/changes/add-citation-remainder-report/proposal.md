---
code_surface: openxFactory — nothing of it moves in this pull request; realization is a later PR after ratification. What that later pull request carries is named in `tasks.md` § 2: `scripts/report-citation-remainder.py` (NEW, the report CLI), `tests/citation_remainder/` (NEW, unit tests over a throwaway fixture corpus), one step added to `.github/workflows/doc-health-reusable.yml` (the nightly caller), and the one-line docstring correction `scripts/packet_reference.py` is owed by D2. No existing validator arm moves, no promoted byte moves, no contract member moves, no schema moves, and `scripts/validate-pin-registrations.py`'s `check_citations` is untouched by name (`design.md` D7). THIS pull request carries the PACKET ONLY.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves, no `contract_bundle_version` is spent and no release tag is owed. Under `release-realization` a non-empty code surface archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE rather than on landing, so this packet archives only after its realization pull request has merged and run green, and openxFactory issue 1053 closes there.
sequenced_after: []
---

# Proposal: add-citation-remainder-report

Status: draft

Proposed: 2026-09-16, in lane `openxfactory-1` (display `openXfactory-1`),
session `393ade52`, in answer to openxFactory
[#1053](https://github.com/opensoft/openxFactory/issues/1053) — the successor
`add-declared-former-id` `tasks.md` § 6.1 owed and that packet's archive act
filed, standing on [#1003](https://github.com/opensoft/openxFactory/issues/1003)
and [#833](https://github.com/opensoft/openxFactory/issues/833). The lane
CLAIMED #1053 before authoring.

Origin: openxFactory

**THE AUTHORING WAS COMMISSIONED BY TAKING A ROUTING RECORD; THE WORDING IS
OWED A RULING AND HAS NOT HAD ONE.** #1053 was filed by the orchestrator AS A
ROUTING RECORD and NOT CLAIMED. Taking it commissions the AUTHORING and ratifies
nothing, and Brett Heap's word of 2026-09-16, verbatim **"claim #1053 and #1013,
fan out wide"**, commissions the CLAIM and decides no wording either. Every
document in this packet therefore carries `Status: draft`, and `.openspec.yaml`
carries drafting provenance with NO `approved_by` and NO `approved_on` — the
lawful unapproved shape `add-drafted-proposal-origin` (issue #318) defined.
**THE SEVEN DECISIONS MOST WORTH A VETO ARE `design.md` D1 THROUGH D7**, each
put with its RECOMMENDED option first and the alternatives' costs written out
beside it. **NOTHING IS PROMOTED**: this pull request edits no file under
`openspec/specs/`. **NOTHING IS REALIZED**: it adds no script, no workflow and
no test, and `tasks.md` § 2 stays entirely open.

## Why

**THE RESOLUTION RULE LANDED. THE REPORT OF WHAT IT STILL CANNOT RESOLVE DID
NOT, AND NOTHING IN THIS REPOSITORY LOOKS AT THE REMAINDER.**

`add-declared-former-id` (archived 2026-09-15) gave every
`openspec/changes/<id>/…` citation in this corpus a resolution rule and shipped
it as `scripts/packet_reference.py`. That module's own docstring states the
boundary twice — once about itself:

> Run: this module is a library and has no CLI.

and once about the population it was built for: its single named consumer,
`scripts/validate-pin-registrations.py`'s `check_citations`, resolves ONE field
of registered pins (`dispositions[].cited_to`), which is a few dozen referents,
never the corpus. That packet's `design.md` D4 ruled a corpus-wide reporting
sweep out of scope ON COST — not on merit — and its `tasks.md` § 6.1
commissioned a successor and carried the figures forward so the successor would
not have to re-derive them. This packet is that successor, and the figures have
been re-derived anyway, because a population is a property of a TREE and this
tree is not the tree those figures were taken against.

## The measurement, taken before the design

**NOTHING BELOW RESTS ON A NUMBER ANYBODY TYPED.** Re-taken on a fresh clone at
`origin/main` `b1df95ee`, by #1053's own stated recipe so that it reproduces,
and run through the LANDED `packet_reference.resolve()` rather than a
hand-rolled raw-path check. The commands are in `design.md` D0.

| measure | #1053 at filing (`8944758c`) | re-measured (`b1df95ee`) |
| --- | ---: | ---: |
| tracked files | 5,467 | **5,466** |
| files in scope | 2,979 | **2,973** |
| distinct `openspec/changes/…` tokens | 578 | **586** |
| tokens with no raw path in the tree | 153 | **162** |
| of those, REPAIRED by the identity rule | 73 | **76** |
| `RESOLVED` | — | **498** (76 of them RELOCATED) |
| `DANGLING` identity-half | — | **74** |
| `DANGLING` file-half | — | **7** |
| `AMBIGUOUS` | 0 | **0** |
| `NOT_A_PACKET_REFERENCE` | 4 | **7** |
| **INCLUSIVE REMAINDER** | **80** | **81** |

**THE TWO READINGS DIFFER AND BOTH ARE REPORTED.** They are taken at different
commits several merges apart, so they are approximately and not exactly
comparable — the same caveat #1053 records against its own two predecessors
(M4's 36 at `9378eca5`, PR #1041's 40 at `701c8fde`). Nothing here claims one
corrects the other.

**THE CLASSIFIED FIGURES ARE #1053'S AND ARE CITED TO IT, NOT RE-DERIVED HERE.**
The refined this-tree-only reading (22 cross-repository tokens removed by an
automated qualifier check, leaving 59; a manual read of all 59 finding about 48
true in-tree remainder in nine classes) is #1053's hand work. The DEEP
re-measurement is a sibling writer's and lands beside this packet as
`evidence/measurement-<sha8>.md`; `design.md` D0 holds the named slot for it.

**THREE FACTS THIS RE-MEASUREMENT FOUND THAT #1053 DOES NOT CARRY**, each of
which moves a decision rather than decorating one:

1. **The 74 identity-half tokens collapse to 48 DISTINCT IDENTITIES.** Eighteen
   identities are cited by more than one remainder token — `add-council-clearance-rule-template`
   by six, `add-openxfactory-tui-installer` by four, `add-pre-archive-citation-gate`
   by three. Fifteen of the 81 remainder tokens are a bare directory path ending
   in `/` whose sibling token names the same identity without the slash. **A
   token count and an identity count are different quantities**, and the report
   must print both (D3), because a reader who repairs one identity clears up to
   six lines. That this 48 lands on #1053's hand-read "about 48" by a completely
   different route is a **coincidence of two different quantities** and is
   recorded as one, never as a confirmation.
2. **The token grammar itself manufactures remainder, in at least four shapes.**
   #1053 names ONE tokenization artifact (a Python implicit string concatenation
   in `scripts/doc_health/pin_class.py`). Measured: 15 tokens end in `/`; one
   ends in a sentence-terminal `.` — `…/codexfactory-floor-relocation-2026-09-10.md.`
   in `contracts/openspec-cli-pin.yaml`, where the regex swallowed the full stop
   that ended the sentence; two end in `-` where a source line broke mid-path;
   one carries a `/./` segment. **The recipe's grammar is part of the finding,
   and D3 makes it exact.**
3. **`openspec/changes/README.md` resolves DANGLING(identity-half) in this
   tree** — the very path `packet_reference.py`'s own docstring offers as the
   canonical `NOT_A_PACKET_REFERENCE` example, because that file does not exist
   here. The resolver's answer for a bare path depends on whether the raw path
   is PRESENT, so **the class of a citation moves with the tree**. It is cited
   from `scripts/packet_reference.py` and `scripts/validate-pin-registrations.py`.

**AND THE PACKET MEASURED ITS OWN EFFECT ON THE POPULATION, AFTER IT EXISTED.**
Re-run on this branch: 2,978 files in scope (+5), 587 distinct tokens (+1), 499
`RESOLVED` (+1), **remainder UNCHANGED at 81**. The packet mints no remainder —
but it JOINS THE CITING SET OF THREE REMAINDER ENTRIES simply by quoting them as
examples. **A document that discusses a dangling citation becomes a record that
carries one.** At this size it is three citing-file counts and nothing else; at
the size of a nightly report committed into the tree it is one such quotation
per remainder line, every night, which is the measured reason `design.md` D5
recommends artifact-only.

## What changes

**FIVE `## ADDED` REQUIREMENTS IN A NEW CAPABILITY, AND A REALIZATION THIS PULL
REQUEST DOES NOT PERFORM.** The delta is `specs/packet-citation-report/spec.md`:

1. **`### Requirement: The citation remainder is reported`** — a report exists,
   it runs over the whole corpus, and it prints the remainder by resolver
   outcome with both the token count and the identity count.
2. **`### Requirement: The reported population is derived from a stated
   recipe`** — the file population, the token grammar and the resolver outcomes
   are stated in the requirement rather than left to the implementation, so a
   figure the report prints can be reproduced by hand.
3. **`### Requirement: A suspected cross-repository citation is flagged and
   never silently dropped`** — the qualifier heuristics are a SUSPICION and are
   reported as one.
4. **`### Requirement: The report classifies only what it can decide
   mechanically`** — a small mechanical class set, an honest `unclassified`, and
   the rule that nothing is repaired.
5. **`### Requirement: The report is advisory and gates nothing`** — exit code
   always 0, no `--fail-on`, and promoting it to a gate is a separate act on a
   separate word.

**NO `## MODIFIED` BLOCK, AND THAT IS THE POINT OF THE SHAPE.** A twenty-fourth
doc-health family would be a MODIFIED block restating doc-health's whole
twenty-three-family enumeration; an eighth `proposal-origin` finding class would
be a MODIFIED block over a requirement about proposal ORIGINS. Five ADDED
requirements in a NEW capability directory owe neither, edit no promoted byte,
and collide with no other active change's MODIFIED block — which is why
`sequenced_after:` is the POSITIVE root claim `[]` rather than a dependency.

## What this packet does NOT do

- **It does not fix one citation.** `add-declared-former-id` D4 and
  `packet_reference.py`'s own docstring both hold that *"a reference that
  resolves owes the citing record no edit"*; this packet adds that **a dangling
  one owes the citing record no edit FROM THIS TOOL EITHER**. The report is a
  reader, and a reader that offers a corrected spelling is an editor.
- **It does not resolve anything cross-repository.** The other repository's
  corpus is that repository's to read; this tree can only SUSPECT, and D3 makes
  it say so.
- **It does not add a doc-health family.** D1 sizes that step and declines to
  take it, for the reason doc-health's own family-enumeration requirement gives:
  a severity decision *"SHALL follow a measurement of the population the gate
  would red rather than precede it"*. This packet is that measurement's
  producer.
- **It does not give `scripts/packet_reference.py` a CLI.** D2 recommends a
  sibling script, so the library's contract stays a library's.
- **It does not commit a report into the corpus.** D5 recommends artifact-only
  and gives a measured reason beyond merge conflicts: `health/` is INSIDE the
  measured file population and carries **0** citation tokens today, so a
  committed remainder report would be the first file there to carry them — one
  per remainder line — and the next run would count its own output.
- **It does not touch `check_citations`.** `scripts/validate-pin-registrations.py`
  keeps its scope exactly (D7).
- **It does not close the origin issue.** `code_surface` is non-empty, so the
  archive is a separate act on merged-plus-green realization evidence and a
  separate word, and openxFactory #1053 closes THERE, by a closing keyword
  written in the archive pull request and in no commit message on this branch.
