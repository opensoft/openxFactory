# Proposal Reality Check: split-opendox-two-layer-product — openRepoShape claims

Status: record
Kind: verification record
Decision date: 2026-09-05
Lane: openxfactory-4-opendox-extraction (formerly openxfactory-opendox)
Author: this lane, corrections-PR session, after a read-only workflow
checked forty-eight claims this packet makes about `opensoft/openRepoShape`
against a live checkout of that repository.
Amends: `split-opendox-two-layer-product`, RATIFIED 2026-09-05 (record
`review/ratification-2026-09-05.md`) and AMENDED 2026-09-05 (record
`review/amendment-2026-09-05-repository-shape.md`, Brett Heap, *"elect the
shape for both, follow the pin chain, no family yet"*).

**THIS IS A CORRECTIONS RECORD, NOT A RE-RATIFICATION.** The packet stays
ratified and amended as it stood; no ruling is reopened. Every correction
below is visible in the tree as a dated inline note beside the sentence it
corrects, in the same form the 2026-09-05 amendment already uses, citing this
record as its source.

## What happened

A prior workflow session (`wf_ba66b10a-c44`, journal
`journal.jsonl`) extracted forty-eight discrete, checkable claims this
packet's `proposal.md`, `design.md` and `tasks.md` make about the mechanics
of `opensoft/openRepoShape` — what `scaffold-project.py` writes, what it
refuses, what classifies as what, and what counts follow from those mechanics
— and checked twenty-four of them against a live clone before an API limit
stopped the run. Nineteen held. **Five were judged FALSE: `c4`, `c6`, `c18`,
`c19`, `c23`.** The adversarial refutation pass that should have stress-tested
those five verdicts never ran (the same limit). This lane's job was to
re-verify each of the five independently and correct the packet for every one
that is truly false.

## Method

Each of the five was re-measured directly, in this session, from a fresh
clone of `opensoft/openRepoShape` (`.../scratchpad/verify/oRS`, tip
`e9c4827b85f50503bbdd9e5b4fac9d6c3d0baf63` at read time) and a detached
worktree at `122d729bc0c2f2e0ded0bb61b6b97f49512f613e` — the commit this
repository's `contracts/openreposhape-pin.yaml` pins today —
plus, where a finding turned on it, a third worktree at `355f6ef4`, the exact
commit `tasks.md` § 1.1a names as the in-flight re-pin target. No
state-changing call was made against GitHub; the only network reads were the
initial `git clone` of `opensoft/openRepoShape` and, where a finding turned on
this organization's live ruleset state, `gh api orgs/opensoft/rulesets` and
the two ruleset ids the packet's own text names. `--dry-run` and
`--local-remote-dir` (bare repositories on disk, the tool's own documented
test path) materialized real file trees with nothing created upstream, and
the operator's local `openRepoShape` checkout (outside this repository) was
never touched.

## The five findings, re-verified

**`c4` (`proposal.md`:2, front matter) — REPRODUCED, split verdict.**
Claim: all six repositories are created by `scaffold-project.py`, PUBLIC and
Apache-2.0. Observed: `--dry-run` at tip prints the neutral-product/assembly
admission and the six names; the identical command at the pinned `122d729b`
exits 2 with `REFUSED naming-role-mismatch` (a CamelCase control name
succeeds at the same commit, isolating the refusal to the `open<Product>`
form). Apache-2.0 is false at BOTH revisions: `find templates -iname
'LICENSE*'` returns nothing at either commit, and `scaffold-project.py`'s
`gh repo create` call (line 666) carries no `--license` — the only
"Apache-2.0" string in the tool is its own SPDX header. PUBLIC holds only
because `tasks.md` § 1.1/1.2 pass `--visibility public` explicitly; the
tool's own unset default is `private`. Corrected in `proposal.md`:2 with a
dated parenthetical immediately after the sentence it qualifies.

**`c6` (`proposal.md`:2, item (4)) — REPRODUCED.** Claim: ruleset state in
SEVEN repositories, "every one... a separate act". Observed: `grep -rniE
"rulesets|branch_protection"` over the whole tree returns no API call at
either revision — `RULESET_HINT` is byte-identical between tip and pin and is
only ever printed to stderr. The "seven" count double-counts `openxFactory`
against the packet's own later text: `proposal.md`:417 and `tasks.md` § 1.5 /
§ 8.1 already say SIX. Read live, `gh api orgs/opensoft/rulesets` shows every
ruleset binding this organization is `source_type: "Organization"` (an
org-admin edit, not "a repository setting"), and the two rulesets the
packet's evidence lines depend on (`21538893`, `21957695`) name no
dashboard-workflow check today. Corrected in `proposal.md`:2, item (4), in
place, with the history preserved.

**`c18` (`tasks.md` §1.3, ~193-200) — REPRODUCED, false at both revisions,
differently.** Claim: the assembly root gets twelve named files "and nothing
else"; each leg gets three. Observed by materializing with
`--local-remote-dir` (no network): at the pin, the assembly root writes
FIFTEEN files — the claimed twelve plus `scripts/repo_shape.py`,
`scripts/validate-repository-naming.py` and
`contracts/repository-naming.yaml`, each digest-pinned in the project's own
`contracts/shape-pin.yaml` (9 rows). The three-file leg claim IS exact at the
pin. At `355f6ef4` (the re-pin target), the assembly root ALSO gets
`AGENTS-shape.md`, `AGENTS.md`, `CLAUDE.md` (eighteen files, 10
`shape-pin.yaml` rows) and each leg gets a rendered `AGENTS.md` plus a
one-line `CLAUDE.md` (five files) — openRepoShape PR #30 (`99b3774`), which
is an ancestor of `355f6ef4`. Corrected in `tasks.md` § 1.3 with one combined
note (see `c19` below — the two share the same paragraph).

**`c19` (`tasks.md` §1.3, ~201-206) — REPRODUCED, false in operation.**
Claim: `AGENTS.md`/`CLAUDE.md` remain a hand act. True at the currently
pinned `122d729b` (`git ls-tree -r --name-only` there shows no AGENTS/CLAUDE
path anywhere under `templates/`). False from `355f6ef4` onward — which is
the only revision `tasks.md` § 1.1a will ever let 1.1/1.2 run at, since those
tasks are explicitly BLOCKED UNTIL the re-pin lands. `git merge-base
--is-ancestor 99b3774 355f6ef4` confirms the enabling commit predates the
re-pin target. Every other item in the same hand-act sentence (LICENSE, the
four posture files, CODEOWNERS, the OpenSpec instance, `manifest.yaml`/
`CHANGELOG.md`, the four legs' pytest suite, 1.5's rulesets) was re-checked
and holds at every revision. Corrected in `tasks.md` § 1.3, jointly with
`c18`, as one dated paragraph appended after the original list (which stays
visible, unedited).

**`c23` (`tasks.md` §1.7, ~242-247) — REPRODUCED, pure arithmetic.** Claim:
"eighteen descendant names plus one install name". The packet itself names
exactly five descendants — `MedxDox`, `codexDox`, `LedgerxDox`, `AdxDox`,
`OpsxDox` — each three names under the shape (assembly + `-spec` + `-code`,
confirmed identical at tip and pin by `--dry-run` and by
`scripts/validate-repository-naming.py --explain`). 5 × 3 = fifteen, not
eighteen. Reproducible: `grep -ohE '(^|[^[:alnum:]_])[A-Za-z]+xDox([^[:alnum:]_]|$)'
proposal.md design.md tasks.md | sed -E 's/^[^A-Za-z]*//; s/[^A-Za-z]*$//' |
sort -u` (run from `openspec/changes/split-opendox-two-layer-product/`) — the
pattern is POSIX ERE with no Perl-style escapes (no `\b`, which POSIX ERE does
not define and GNU grep accepts only as an extension); the `-o`/`-h` options
are GNU/BSD grep extensions (available on Linux and macOS), not
POSIX-required. Returns
SEVEN distinct strings, not five, because the broad pattern also catches two
non-descendant artifacts: `medxDox`, a lowercase casing variant appearing
exactly once inside Brett Heap's verbatim quoted founding utterance
(`proposal.md`:59), never as a declared descendant name (the packet's own
registration in `tasks.md` § 1.7 spells it `MedxDox`); and `openxDox`, the
case-folded ALSO-ACCEPTED spelling of `openXdox` itself, named twice in the
pin-chain discussion (`tasks.md`:347, `design.md`:868), not a sixth descendant.
Excluding those two artifacts: `grep -owhE
'MedxDox|codexDox|LedgerxDox|AdxDox|OpsxDox' proposal.md design.md tasks.md |
sort -u | wc -l` — the pattern is POSIX ERE with no Perl-style escapes; the
`-o`/`-h`/`-w` options are GNU/BSD grep extensions (available on Linux and
macOS), not POSIX-required. Returns 5 — no sixth descendant exists anywhere in
the packet. Corrected in
`tasks.md` § 1.7 with
a dated parenthetical giving the arithmetic, so the next amendment that adds
or drops a descendant can re-derive the count instead of inheriting a stale
one.

## What did NOT reproduce

Nothing among the five failed to reproduce — all five findings held up
independently, at the revisions and by the methods described above. No
finding is reversed by this record.

## Claims not yet checked (`c24`–`c48`, minus `c26` which the prior session
already verified `holds=true`)

The prior session's limit stopped it after twenty-four of forty-eight claims
(nineteen held, five false, all twenty-four reconciled above or previously).
The following twenty-four remain UNCHECKED by either session — listed here
by id, source and text, so the next pass can pick them up without
re-deriving them from the journal:

- `c24` (`tasks.md`:253-257): project-register.yaml rows for the two elected
  projects. One row each for openDox and openXdox carrying `schema:
  project-repo-schema`, `reference: openxFactory docs/project-repo-schema.md`,
  the three repositories in `repositories`, and a `repository_roles` entry
  per repository (assembly, spec, code — at most one assembly per project).
- `c25` (`tasks.md`:258-262): The row is DERIVED and the manifest is the
  SOURCE (`docs/project-repo-schema.md` § The manifest is the source; a
  register row is derived): each field above is READ FROM that project's own
  `project.yaml` and the register never originates an election. Where the two
  disagree, the register wins for NAVIGATION only and the disagreement is
  reported as drift.
- `c27` (`tasks.md`:268-271): openXdox's `project.yaml` declares
  `neutral_product_pins: [openDox]` (written by 1.2's `--pin`); every
  descendant declares `neutral_product_pins: [openXdox]` and records the
  chain it relies on — `naming.referent_chain: [openXdox, openDox]` — per
  openRepoShape#40.
- `c28` (`tasks.md`:282-289): MEASURED 2026-09-05 at openRepoShape main
  `f9ff3f8`: codexDox with `neutral_product_pins: [openXdox]` classifies as a
  domain-descendant in the assembly role — it PASSES today
  (`also_matches: [project-leg/assembly]`, `descendant_referent: openDox`,
  `referent_declared: true`), and the assembly root's own
  `scripts/validate-manifest.py` accepts that manifest, because the pin file
  it looks for is `contracts/openxdox-pin.yaml`, which the scaffold wrote.
- `c29` (`tasks.md`:289-297): It passes by ACCIDENT, not by the chain:
  `contracts/repository-naming.yaml` admits an x-stem spelling of the
  referent (`also_accepted: openx{product}`), the referent test compares
  CASE-FOLDED, and `openXdox`.casefold() equals `openxDox`.casefold() — so a
  pin on the INTEGRATION layer satisfies the referent test for the NEUTRAL
  CORE, and the manifest asserts a declared openDox referent in a tree that
  declares no openDox pin.
- `c30` (`tasks.md`:301-303): What the interim does NOT permit is adding a
  direct openDox pin to a descendant to force the classification — that
  would break OQ-2 to satisfy a validator.
- `c31` (`tasks.md`:419-428): `contracts/opendox-pin.yaml` — openXdox pins
  openDox by commit and per-file digest, in the openXdox ASSEMBLY ROOT,
  naming the openDox ASSEMBLY ROOT's commit. The cost the shape adds,
  accepted: a change to openDox's code leg is not visible to openXdox until
  openDox's assembly root advances its own code pin and openXdox then bumps
  this file — two pin moves where a single-repository product had none.
- `c32` (`tasks.md`:402-405): Cut dox-v1.0 only after the floor's four parts
  are green. In the ASSEMBLY ROOT (amended 2026-09-05), over the commit that
  names both legs.
- `c33` (`tasks.md`:440-441): Cut xdox-v1.0 after its own suite is green. In
  the ASSEMBLY ROOT (amended 2026-09-05), on 3.8's reasoning.
- `c34` (`tasks.md`:466-473): FLOOR PART 2 (RULED OQ-1) — test counts that
  must SUM across the three repositories. 3,927 `def test_` leave — 52% of
  this repository's 7,612. openDox + openXdox + the openxFactory remainder
  (which now includes the adapter's own tests) SHALL equal the pre-split
  count.
- `c35` (`tasks.md`:593-596): 8.1 All SIX repositories exist (amended
  2026-09-05 — this first said "Both repositories"), PUBLIC, Apache-2.0,
  each with a required check that has reported at least once and a ruleset
  promoted from EVALUATE to ACTIVE; each assembly root's `project.yaml`
  records the election.
- `c36` (`tasks.md`:477-484): DE-FLOOR BEFORE YOU REMOVE — Rule 7 substrate
  row 1, claimed HERE. `openspec/specs/ideation-dashboard/` is REMOVED and
  two capability directories are ADDED by the archive, and the codexFactory
  review-authority floor is EXACT SET EQUALITY. Order: the codexFactory pull
  request FIRST, then openxFactory's five pin sites in ONE reviewed diff,
  then the removal.
- `c37` (`tasks.md`:538-543): The descendant is scaffolded the same way and
  is THREE repositories, not one: codexDox + codexDox-spec + codexDox-code,
  one `scaffold-project.py` run with `--pin openXdox@<sha>`. It stays THIN
  under DQ-1: it pins openXdox and reuses openxFactory's adapter.
- `c38` (`tasks.md`:568-574): `python3 scaffold-project.py --org opensoft
  --project codexDox --id codexdox --name 'codexDox' --visibility <follows
  codexFactory's own visibility, RULING Q7> --elected-by 'Brett Heap'
  --elected-on <the ruling's date> --reference 'openxFactory
  docs/project-repo-schema.md' --pin openXdox@<40 hex — the openXdox
  ASSEMBLY ROOT's commit>`.
- `c39` (`tasks.md`:576-580): Three repositories, THIN: the `-code` leg
  carries deploy configuration and branding, the `-spec` leg the one
  domain-mapping declaration, the assembly root the pins and the gate. It
  owns NO adapter (DQ-1). The `--pin` on openXdox — never on openDox — is
  RULING OQ-2 in the tree.
- `c40` (`design.md`:701-706): SIX REPOSITORY NAMES, AND THE ELECTION THAT
  PRODUCED THEM. The names this record registers are therefore six: openDox,
  openDox-spec, openDox-code, openXdox, openXdox-spec and openXdox-code.
- `c41` (`design.md`:712-720): The leg suffixes are not new brands. `-spec`
  and `-code` are lowercase and hyphenated precisely so they sit in a
  different naming family from every CamelCase product name this record
  governs: openDox-code is a LEG of the openDox project, not a product
  called "openDox-code". openXdox-Install keeps its own form and its own
  rule: it is an INSTALL name, not a leg.
- `c42` (`design.md`:722-729): The descendant spelling is unaffected — they
  are MedxDox, codexDox, LedgerxDox, AdxDox and OpsxDox — registered as NAMES
  here with no repository created; its leg names are registered beside it —
  codexDox-spec, codexDox-code, MedxDox-spec, MedxDox-code, and so on for
  LedgerxDox, AdxDox and OpsxDox.
- `c43` (`design.md`:824-832): The decision. openDox and openXdox are each a
  THREE-REPOSITORY project in the sense `docs/project-repo-schema.md`
  ratified on 2026-09-02: an assembly root carrying `project.yaml`, the two
  legs as submodules, the pins and the validate gate, plus a `<Project>-spec`
  leg and a `<Project>-code` leg. Six repositories, created by
  `scaffold-project.py` rather than by hand. No family holder is created.
- `c44` (`design.md`:832): Descendants are scaffolded the same way with
  `--pin openXdox@<sha>`.
- `c45` (`design.md`:845-847): Alternatives not taken: (1) two single
  repositories, on the neutral-product precedent — every open* neutral
  product in opensoft today is ONE repository (openxFactory, openXwallet,
  openChart, openPractice, openRepoShape); (2) a Dox family holder carrying
  `family.yaml` (`kind: family-manifest`) — NOT TAKEN, "no family yet"; (3)
  elect for openXdox only — NOT TAKEN by the ruling's own word, "for both".
- `c46` (`design.md`:912-916): Where `contracts/manifest.yaml` and the bundle
  tag live: In the ASSEMBLY ROOT of each project, with the release cut there.
  The assembly root is the only object whose single commit names both legs,
  so it is the only place a release identity can describe THE PROJECT rather
  than half of it; a tag on openDox-code says nothing about the requirements
  that shipped with it.
- `c47` (`design.md`:925-929): The cost accepted, stated rather than
  discovered. A change to openDox's code is not visible to openXdox until TWO
  pins move: openDox's assembly root advances its own code pin (gitlink plus
  `contracts/code-pin.yaml`, same commit), and openXdox then bumps
  `contracts/opendox-pin.yaml`. A single-repository product has neither move.
- `c48` (`design.md`:887-903): opensoft/openRepoShape#41 — scaffold-project.py
  REFUSED both invocations at the commit this repository pins. Verified at
  openRepoShape main `f9ff3f8` and at `122d729bc0c2f2e0ded0bb61b6b97f49512f613e`,
  the commit `contracts/openreposhape-pin.yaml` pins, so it was not a tip
  regression. openRepoShape PR #45, merge commit `5ffa8d58`, merged
  2026-09-05T17:19:12Z, authored by lane `xfactory-2`, is that admission.
  openRepoShape main is now at `355f6ef4` (#47), which carries both
  `c2cc9e25` and `5ffa8d58`.

## What remains owed

Finishing the check: the twenty-four claims above still need the same
treatment this record gave the first twenty-four — re-verified independently
against a live `openRepoShape` checkout, then corrected in the packet if
false or left standing with a citation if true — followed by the adversarial
refutation pass that never ran on this round's five verdicts, which should
stress-test the corrections this record just made, not only the original
nineteen that held. `c26` (already `holds=true`) needs no further action.

## Verification, from this session's own runs

| check | result |
| --- | --- |
| `openspec validate split-opendox-two-layer-product --strict` | `Change 'split-opendox-two-layer-product' is valid` |
| `openspec validate --all --strict` | `Totals: 94 passed, 0 failed (94 items)` |
| `python3 scripts/proposal-support.py . verify` | `proposal support verification ok` |
| `python3 -m pytest -q tests/sequenced_after tests/doc-health tests/proposal-support` | `1774 passed, 7 warnings, 2 subtests passed` |
| doc-health, `--single-repo`, fresh `origin/main` worktree (`8b297c2f`) | 8 critical, 7 error, 30 warning, 13 info |
| doc-health, `--single-repo`, this tree | 8 critical, 7 error, 30 warning, 13 info — **delta ZERO across every family and every severity, info included**, diffed line by line after normalizing the `Repo-Identity` prefix each run stamps from its own directory name. The new `review/reality-check-2026-09-05.md` file, carrying the same lifecycle header form as the other `review/` records, adds no finding.
