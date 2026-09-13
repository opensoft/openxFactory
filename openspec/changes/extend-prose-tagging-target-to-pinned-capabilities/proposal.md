---
code_surface: openxFactory — `scripts/doc_health/families.py`, whose `_resolve_capability` (line 1317) and `fam_tag_hygiene` (line 1331) gain a second resolution arm for a pinned target, plus that arm's tests under `tests/doc-health/` (hyphen: the tests directory is `tests/doc-health/`, while the package under test is `scripts/doc_health/`), plus AT MOST THREE FURTHER FILES THE ARM'S OWN RULES REQUIRE and which are named here rather than discovered at realization: (i) ONE module under `scripts/doc_health/` holding the shared, PURE, NON-EXECUTING `pinned_contract_manifest` SHAPE ADAPTER — design D-2's single code-fixed route, which holds the per-shape table and reads the record and nothing else — and this file exists ONLY where the realization gives that adapter a module of its own; where the adapter lives inside `scripts/doc_health/families.py`, already named above, (i) ADDS NO FILE. Under EITHER placement the adapter NEITHER EDITS NOR CALLS any of the five per-product pin verifiers, which are product-specific, shell out, and in one case reach the network, so they are not a shape-only API to extract from; the only place any of them is imported at all is the GUARD LEG of the equivalence test (task 3.3(p)), which lives in that arm's tests under `tests/doc-health/` — already named above, so it adds no file either — and imports them at fixed, authored paths; and (ii) the containment helper of D-2 and task 3.3(m), EITHER as a parameter added to `resolve_in_tree` in `scripts/validate-pin-registrations.py` — that file's own edit, no further file — OR as one shared helper both callers use, which is a NEW file AND requires `scripts/validate-pin-registrations.py` itself to be edited to become the shared helper's second caller. THE BOUND IS EXACTLY THREE AND THE THREE ARE ENUMERATED: (1) the shape-adapter module under `scripts/doc_health/`, (2) the new shared containment helper, (3) `scripts/validate-pin-registrations.py` as that helper's second caller. THREE is reached only where (i) gives the adapter a module of its own AND (ii) takes the shared-helper branch; where the adapter lives in `scripts/doc_health/families.py` and (ii) takes the parameter branch the further-file count is ZERO, and the two intermediate combinations give ONE or TWO. No fourth file is admitted under any combination, and the five pin verifiers are in none of them. NO BYTE OF ANY OF THEM MOVES IN THIS PULL REQUEST. This pull request carries the PACKET ONLY — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, two `## MODIFIED` spec deltas, one README "Active changes" bullet, the machine-seeded per-change sweep-ledger row in `tests/sequenced_after/corpus-ledger.yaml`, and the two `_LEDGER_SUBJECTS` rows the two `## MODIFIED` deltas above require of `tests/doc-health/test_modified_block_currency_self_gate.py`'s own carriage-ledger self-gate (all three are bookkeeping the self-gates require of ANY filing that touches a promoted block, not test implementation for the pinned-target arm the realization proposes). THE REALIZATION IS A LATER PULL REQUEST in this same repository, authored after ratification, and it is FOUR surfaces and not more: (1) the resolver arm and its tests, together with the at-most-three further files named above that the arm's code-fixed-route and containment rules require; (2) the four affected markers retargeted from `target=openxwallet` to the pinned form; (3) `docs/document-lifecycle.md`'s Prose Tagging Markers section carrying the new form and the stale-target rule; (4) the stale sentence at `ideation/staging/INDEX.md:2262-2265`, which still calls three `openxwallet` blocks "all resolving" and has been false since 2026-08-28. NOT THIS PACKET'S SURFACE, each for a stated reason: no marker regex changes, because the existing `_CAND_OPEN` and `_ATTR` patterns already accept the proposed value unchanged (design D-1, measured); no pin record is edited and no pin schema member is added — D-2 RESERVES the member name `capabilities:` as the spelling of its enumeration PREREQUISITE, so that the prerequisite has a deterministic input contract rather than an intention, but it NAMES it and does not add it: no pin record gains that member here, no schema admits it here, and whether a real pin record may carry it is a `neutral-product-pin` question with the publisher (design D-2); no capability is created, deleted or renamed; no `openspec/specs/` directory moves; no contract byte, pin byte or digest moves; no contract bundle is cut.
target_release: implemented
---

# Proposal: extend-prose-tagging-target-to-pinned-capabilities

Status: ratified
Ratified: 2026-09-12 and 2026-09-13 by Brett Heap (openxFactory repository
owner), first-hand, in session, lane `openxfactory-2` (display
`openXfactory-2`) — FIVE SELECTIONS, not typed sentences, made via the
lane's interactive multi-choice. FOUR on 2026-09-12 at approximately
23:20Z, one question per `tasks.md` § 1 task: **"Ratify 1.1 as filed
(Recommended) / Ratify 1.2 as filed / Ratify 1.3 as filed (Recommended) /
Confirm 1.4 as filed (Recommended)"**. A FIFTH on 2026-09-13T01:25:07Z,
RE-RULING task 1.2 over Copilot review thread `PRRT_kwDOTAvnrs6h1H-H` on
ratification PR #1019: **"Tighten to fail-closed after all"** — which
SUPERSEDES the 23:20Z selection on that ONE box and on no other. THE ONE
CITATION, which supersedes and restates the 23:20Z record: openxFactory
#992 (comment
https://github.com/opensoft/openxFactory/issues/992#issuecomment-5649935136);
copy for the lane's status thread on openxFactory #745 (comment
https://github.com/opensoft/openxFactory/issues/745#issuecomment-5649935244).
Record: `review/ratification-2026-09-12.md`. **RATIFIED — 1.1, 1.3 and 1.4
AS FILED; 1.2 WITH TIGHTENING, D-2 FAILING CLOSED.** The packet was put to
him AS LANDED at `dafe8877e4c8f2d3a52cbe94307904b639b7bece`
(2026-09-12T23:16:13Z), PR #994; acts 1, 3 and 4 ratify that text unchanged,
and act 5 TIGHTENS D-2 — a pinned target now resolves only where the pin
record ALSO carries a well-formed `capabilities:` enumeration naming the
capability, an absent enumeration being an unresolved pinned target exactly
as a malformed one already was. NO VETO, and ONE AMENDMENT, which this
ratification pull request re-encodes on that word. REALIZATION AND ARCHIVE
ARE NOT AUTHORIZED BY EITHER WORD and remain separate later acts on Brett
Heap's word:
no byte of `scripts/doc_health/families.py` moves, no module is added under
`scripts/doc_health/`, no byte of `scripts/validate-pin-registrations.py` or
of any per-product pin verifier moves, no marker is retargeted, and item (7)
of the `split-openxwallet-repo` archived-ledger entry stays UNTICKED.

**THE `Proposed:` BLOCK IMMEDIATELY BELOW RECORDS THE AT-FILING STATE
(2026-09-12 ~01:55Z) AND IS KEPT VERBATIM AS HISTORY.** Its present-tense
negations — *"no ratification, no realization and no archive is claimed by
this packet"*, *"carry `Status: draft`"* — were true AT FILING and are
superseded by the ratification recorded above: ratification HAS now been
given, in the acts of 2026-09-12 ~23:20Z and 2026-09-13T01:25:07Z,
consolidated in one record — openxFactory #992 comment 5649935136, copied to
#745. Realization and archive remain separate later acts on
Brett Heap's word, and no word for either has been given.

Proposed: 2026-09-12 at approximately 01:55Z by Brett Heap (openxFactory
repository owner), first-hand, in session to lane `openxfactory-2` (display
`openXfactory-2`) — **a SELECTION, not a typed sentence**: presented with the
lane's multi-select question, he chose the option ***"#992 grammar-extension
OpenSpec change (Recommended)"***. Recorded on openxFactory #745. That word
commissioned the FILING of the change openxFactory issue #992 asks for, and
nothing further: **no ratification, no realization and no archive is claimed
by this packet**, and its three lifecycle documents — this one, `design.md`,
`tasks.md` — carry `Status: draft`; its two spec deltas are delta files and
carry no lifecycle header, as 299 of the 303 spec-delta files measured on
`origin/main` at `a72f0a76` do not (the four exceptions are deltas in one archived change — three `## ADDED`,
one `## MODIFIED` — each carrying an inherited `Status: ratified`).

## Why

### The four findings, and why no edit can clear them honestly

`python3 scripts/doc-health.py --single-repo . --family tag-hygiene` reports
FOUR `error`-band, `auto-fixable`-labelled findings on `origin/main`, all one
shape:

```text
[error] oxf:ideation/staging/notebook-access-wallet-governance/notebook-access-wallet-governance.md — unresolved target=openxwallet at line 107
[error] oxf:ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md — unresolved target=openxwallet at line 222
[error] oxf:ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md — unresolved target=openxwallet at line 242
[error] oxf:ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md — unresolved target=openxwallet at line 280
```

The archived change that produced them,
`openspec/changes/archive/2026-08-28-split-openxwallet-repo/`, already reasoned
through both mechanical fixes and rejected both, in its own
`tasks.md:1770-1786`:

> "**The cause is this archive and nothing else.** `document-lifecycle`'s
> prose-tagging grammar resolves an `<!-- xspec:candidate target=… -->` marker
> through `families.py::_resolve_capability`, which admits a name only if it is
> a capability under `openspec/specs/` or an active change id, searched in this
> repository and then in `openxFactory`. Deleting `openspec/specs/openxwallet/`
> removed the only referent those four markers had.
>
> **They are NOT fixed here, deliberately.** The band says `auto-fixable`, but
> no mechanical fix is truthful: retargeting a marker to
> `domain-descendant-boundary` or `neutral-product-pin` would make the marker
> name a capability the tagged prose is not about, and deleting the markers
> would silently drop four blocks out of the conversion queue. The honest fix
> is a GRAMMAR EXTENSION — a target form that can name a capability which now
> lives in a pinned neutral product — and that is a change, not an edit."

### The grammar is silent, not merely unhelpful

`docs/document-lifecycle.md:182-183` defines only what a valid target IS:

> "`<capability>` is a spec capability id under `openspec/specs/` (or in an
> active change's `specs/` while the capability is pre-promotion)"

Neither that bullet nor any other sentence of that document addresses a target
that USED TO resolve and no longer does. The corpus's first capability EXIT
found the rule missing, and the checker's single fixed remedy string
(`families.py:1523-1524`, measured on `origin/main` at `177ba819`) inherits the silence: it tells an author what a valid
target looks like, and cannot tell them which capability is faithful to any one
of these four blocks — because the capability those blocks are about is not in
this repository at all.

### The owed successor has been on the register since the archive, unopened

`README.md:7075` carries it as numbered item (7) of the
`split-openxwallet-repo` archived-ledger entry, on `origin/main` at `177ba819`
(this branch's own copy is at a different line, `7061`, since main gained
unrelated content first):

> "(7) **A prose-tagging target form for a capability that has left the
> corpus** — added at the archive itself, because the act produced it: deleting
> `openspec/specs/openxwallet/` left four `<!-- xspec:candidate
> target=openxwallet -->` markers in `ideation/staging/` with no referent,
> since `families.py::_resolve_capability` admits only an in-tree capability or
> an active change id."

A corpus-wide search for that item's own wording returns only the one README
passage. No proposal, staged topic, or active or archived change anywhere else
picks it up. **This packet is that successor, and it is the first.**

### The house has already been working around the gap

A later staged topic, `wallet-carried-work-authority` (2026-09-02, after the
archive landed), declined to fence new wallet-topic prose as a candidate at
all, citing this exact precedent (`ideation/staging/INDEX.md:2362-2366`):

> "`openxwallet` and `work-authority-intake` are deliberately NOT fenced, on
> `openxwallet-neutral-home`'s recorded precedent: neither resolves as a
> capability in this repository, so fencing them would emit tag-hygiene
> unresolved-target findings."

That is a precedent for NOT FENCING NEW PROSE. It is not a rule, it is not
written anywhere a checker can read, and it costs the conversion queue every
block it touches. A grammar that can NAME the absent referent lets the prose be
fenced and queued truthfully instead.

## What Changes

**One grammar extension, in three parts, none of them realized here.**

1. **A target form that can name a capability in a pinned neutral product.**
   `target=pinned:<pin-id>/<capability>`, in an `xspec:candidate` marker's
   `target=` attribute and there only (design D-1.1 closes the
   `xspec:supersedes` `spec=` case explicitly rather than leaving it silent),
   where `<pin-id>` is the stem of a
   `contracts/<pin-id>-pin.yaml` record this repository already carries and
   `<capability>` is the capability name as the pinned product holds it. For
   the four affected markers that is `target=pinned:openxwallet/openxwallet`.
   The form is chosen because it is the ONLY candidate the existing marker
   regexes accept with no regex change at all — `_CAND_OPEN`'s attribute value
   class is `[^\s>]+` and `_ATTR`'s is `\S+`, both of which already admit `:`
   and `/`, and `spec=<capability>/<requirement-slug>` is the standing
   precedent for a `/` inside an attribute value. The value's OWN grammar is
   closed and checked before anything is read: exactly two
   `[a-z0-9]+(-[a-z0-9]+)*` components separated by exactly one `/` — the
   measured shape of all 62 in-tree capability ids and all six pin stems — so
   an extra segment, a dotted or traversal component or an empty one is a
   malformed pinned target, refused before any pin path is constructed. The
   unmoved marker regexes accept any non-whitespace value and are deliberately
   not the guard (design D-1).

2. **A resolution rule that rests on a VALID, COMPLETE pin record, and says
   so.** The `<pin-id>` MUST resolve to a NEUTRAL-PRODUCT pin record the
   RESOLUTION ROOTS carry — `kind: pinned_contract_manifest`, the shape
   `neutral-product-pin` requires; a `pinned_workflow` record pins executable
   governance code and is excluded, since it has no capability set for a name
   to be about. **AND THE KIND IS A LABEL, SO THE RECORD MUST BE COMPLETE FOR
   ITS RECORD SHAPE** against the members `neutral-product-pin`'s ratified text
   requires — this grammar enumerating NO MEMBER LIST OF ITS OWN and opening no
   delta against that capability. THE SHAPE AND NOT THE `revision_kind` ALONE IS
   THE UNIT, measured over all five `pinned_contract_manifest` records: THREE
   shapes, two of them sharing `revision_kind: commit`. **And each shape's
   member set is that shape's SHAPE-GUARD-REQUIRED SET** — exactly the top-level
   members its in-tree pin verifier refuses-when-absent IN ITS PURE,
   SOURCE-FREE GUARDS, measured from the verifier scripts: (a) the ENUMERATED commit pin, `revision_kind`, `commit`,
   `files` and one product-identity member whose spelling differs by mount
   (`submodule_path` at `scripts/verify-openxwallet-pin.py:194`,
   `source_repository` at `scripts/validate-openreposhape-pin.py:258`), with
   `files:` mappings each carrying a `sha256` beside path-only
   `pinned_by_commit_only:` strings that validly carry none and whose ABSENCE
   the shape guards accept (`openspec/specs/neutral-product-pin/spec.md:31-36`;
   `contracts/openxwallet-pin.yaml:70,104-110`); (b) the WHOLE-TREE DIGEST
   commit pin, `submodule_path`, `revision_kind`, `commit`, `digest_algorithm`,
   `digest_definition` and `digests.tree_sha256` with NEITHER list
   (`scripts/verify-opendox-pin.py:215-269`;
   `contracts/opendox-pin.yaml:108-110`, `contracts/openxdox-pin.yaml:92-94`);
   and (c) the PUBLISHED-ARTIFACT pin, NINE members — `revision_kind`,
   `version`, `integrity`, `shasum`, `package`, `lockfile`,
   `lockfile_integrity`, `lockfile_packages`, `binary`
   (`scripts/validate-openspec-cli-pin.py:592,601,619,646,658,698,708,731,748`;
   `:46-48`, `:62-65`, `:669-673`;
   `contracts/openspec-cli-pin.yaml:282,289,299,308,328-330,370`), the ratified
   text reaching six of the nine and the guards supplying `package` and
   `binary` it does not name. The table is PINNED to those guards by a TWO-LEG
   EQUIVALENCE TEST over each real record — a RECORD leg inside the adapter and
   a GUARD leg that calls each verifier's importable, source-free guard, or, for
   the two members reachable only inside `verify()`, re-reads a measured
   citation — so it can be neither narrower than the gate (admitting on a side
   run what the repository refuses at its first shape check) nor wider (refusing
   what it admits). **The judgement is NECESSARY for the record's FULL verifier
   and by design NOT SUFFICIENT for it**: a source-dependent check such as
   `scripts/validate-openreposhape-pin.py`'s `pin-surface-undeclared`
   (`:515-530`) compares the pin against the RESOLVED SOURCE, which an offline,
   tree-local resolver cannot do without reproducing that verifier's I/O — and
   on a landed tree every record has already passed its full verifier, those
   verifiers being required checks, so what this arm defends is the offline
   judgement over arbitrary trees. A record carrying a
   kind with a partial member set for the shape it matches, or matching no shape
   at all, is an INVALID PIN that reports with a finding NAMING THE SHAPE TRIED
   AND THE FAILING MEMBER and does not resolve; a table keyed on the revision
   kind alone would instead refuse the two whole-tree records this repository
   ships. **That judgement goes through ONE
   CODE-FIXED route** — a single shared, PURE, NON-EXECUTING adapter holding the
   per-shape table, in the resolver's own module or in one shared helper module
   beside it — and the pass NEVER executes, imports or opens a path a pin record
   selects, so `verify_pin:` is data it may compare and never a dispatch key. **And the record is looked for under
   EXACTLY the root precedence the in-tree arm already uses**, the document's own
   repository root then the `openxFactory` root
   (`scripts/doc_health/families.py:1317-1321`), with every pinned-arm finding
   naming the root it resolved against (design D-2). **AND THE `<capability>`
   SEGMENT MUST APPEAR IN THAT RECORD'S OWN `capabilities:` ENUMERATION — the
   RULING'S TIGHTENING, and D-2 FAILS CLOSED.** Resolution has three
   prerequisites and no arms: a valid, complete pin record; a well-formed,
   non-empty top-level `capabilities:` sequence on it; and the named capability
   as a member of that sequence. An ABSENT enumeration is an UNRESOLVED PINNED
   TARGET — a controlled finding naming the record and the remedy, "the
   publisher adds `capabilities:` through a `neutral-product-pin` change" —
   exactly as a MALFORMED one already was, so nothing degrades open and
   Principle VII is satisfied by construction. The enumeration is ONE NAMED
   MEMBER and not a search, which is what makes the prerequisite deterministic;
   naming it adds it to nothing.
   **THE MEASURED CONSEQUENCE, STATED PLAINLY: no pin record in this tree
   enumerates capabilities** — measured over all six at `323c7adf`.
   What each record addresses INSTEAD differs, and the differences matter
   enough to state rather than average: two enumerate files (`files:` beside
   `pinned_by_commit_only:`), two carry tree `digests:`, one carries workflow
   `pinned_members:`, and `contracts/openspec-cli-pin.yaml` enumerates NOTHING
   — it carries ONE whole-artifact `integrity:` digest over a published tarball
   plus a lockfile referent, and its own comment at
   `contracts/openspec-cli-pin.yaml:69-76` states why it has neither a `files:`
   nor a `pinned_by_commit_only:` list ("ONE digest covers ALL 389 files, so
   the completeness question the two lists answer is answered here by
   construction"). So the four markers this change was filed for do NOT resolve
   on the day the resolver lands: their findings CHANGE FORM, from "unresolved
   target=openxwallet — name a capability under `openspec/specs/`" to
   "unresolved pinned target — `contracts/openxwallet-pin.yaml` carries no
   `capabilities:` enumeration; remedy: the publisher adds one through a
   `neutral-product-pin` change" — still FOUR, still `error`-band, and for the
   first time naming the act that would clear them. That act is openXwallet's
   publisher's, through `neutral-product-pin`, and it is no part of this packet
   (design D-2).

3. **A stale-target rule, which `document-lifecycle` does not have today.**
   When a marker's target capability exits the corpus, the marker either takes
   the pinned form or the block is unfenced — never silently retargeted to a
   different capability, and never silently deleted (design D-3). This is the
   sentence issue #992 § 4's third bullet asks for, and it codifies the
   `wallet-carried-work-authority` precedent as a rule a reader and a checker
   can both apply.

**Spec deltas.** `## MODIFIED Requirements` against `document-lifecycle`'s
"Prose tagging marker hygiene" and `doc-health`'s "Tag hygiene enforced by
reference" — the second because the tag-hygiene family enforces the grammar BY
REFERENCE and its requirement enumerates what the family covers, an enumeration
the new arm extends.

**Not in scope, deliberately.** This packet does not retarget the four markers,
does not delete them, does not move a byte of the resolver, and does not correct
`ideation/staging/INDEX.md:2262-2265`. Those are the realization, and the
realization is a later pull request after ratification.

## Impact

- **Affected specs:** `document-lifecycle` (one MODIFIED requirement),
  `doc-health` (one MODIFIED requirement).
- **Affected code at realization, not here:** `scripts/doc_health/families.py`
  (`_resolve_capability`, `fam_tag_hygiene`) and its tests.
- **Affected documents at realization, not here:**
  `docs/document-lifecycle.md` (Prose Tagging Markers section), the four
  markers in `ideation/staging/`, and `ideation/staging/INDEX.md:2262-2265`.
- **Findings:** the four `tag-hygiene` findings stay OPEN, and this packet
  changes their count by zero. Under the tightening they stay open past
  realization too: they CHANGE FORM when the resolver and the retargeted
  markers land together — to unresolved PINNED targets naming
  `contracts/openxwallet-pin.yaml` and the publisher's remedy — and they reach
  ZERO only when openXwallet's pin record publishes a `capabilities:`
  enumeration naming `openxwallet`, which is the publisher's act through
  `neutral-product-pin` and no part of this packet or of its realization.
- **Release:** `target_release: implemented` and `code_surface` is non-empty,
  so per `release-realization` this packet archives ONLY on merged-plus-green
  realization evidence. No contract bundle is cut, nothing under `contracts/`
  moves, no `contract_bundle_version` is spent and no release tag is owed.
- **Other repositories:** none. The grammar is openxFactory's, the resolver is
  openxFactory's, and the four affected documents are openxFactory's. Sibling
  repositories inherit the extension when they next read the grammar; none is
  edited by this packet or by its realization.

refs #992 · refs #745
