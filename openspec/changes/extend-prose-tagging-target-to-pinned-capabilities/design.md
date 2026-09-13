# Design: extend-prose-tagging-target-to-pinned-capabilities

Status: ratified
Ratified by: extend-prose-tagging-target-to-pinned-capabilities — Brett Heap
(openxFactory repository owner), FIVE SELECTIONS by interactive multi-choice:
FOUR on 2026-09-12 at approximately 23:20Z ("Ratify 1.1 as filed
(Recommended) / Ratify 1.2 as filed / Ratify 1.3 as filed (Recommended) /
Confirm 1.4 as filed (Recommended)"), then a FIFTH on 2026-09-13T01:25:07Z
RE-RULING task 1.2 over Copilot thread `PRRT_kwDOTAvnrs6h1H-H` on PR #1019:
"Tighten to fail-closed after all". THE ONE CITATION, which supersedes and
restates the 23:20Z record: openxFactory #992, comment
https://github.com/opensoft/openxFactory/issues/992#issuecomment-5649935136
(copy on #745, comment 5649935244). D-1, D-1.1, D-3 and D-5 stand AS FILED;
D-2 stands AS TIGHTENED — it FAILS CLOSED, and this document now states it
that way. Record: `review/ratification-2026-09-12.md`.

Every figure in this document was MEASURED at this branch's base
(`origin/main` = `323c7adf`), not remembered. Line numbers cite that tree.

## D-1 — The form: `target=pinned:<pin-id>/<capability>`

**Decision.** An `xspec:candidate` marker's `target=` attribute MAY name its
target as `pinned:<pin-id>/<capability>`, where:

- `pinned:` is a literal, reserved prefix. It is the discriminator, and it is
  unambiguous because **no capability id in this corpus contains a colon** —
  measured: all 62 directory names under `openspec/specs/` are kebab-case, and
  a capability id is a directory name.
- `<pin-id>` is the STEM of a pin record `contracts/<pin-id>-pin.yaml`. For the
  four affected markers, `openxwallet`, from `contracts/openxwallet-pin.yaml`.
- `<capability>` is the capability name as the PINNED PRODUCT holds it, in the
  same kebab-case shape an in-tree capability id takes.

**THE LEXICAL GRAMMAR, STATED BEFORE ANY PATH IS BUILT.** The value after
`pinned:` is EXACTLY TWO components separated by EXACTLY ONE `/`. Each
component matches `[a-z0-9]+(-[a-z0-9]+)*` — lower-case kebab-case, one or more
characters, no leading, trailing or doubled hyphen — which is measured to be
the shape of every one of the 62 capability ids under `openspec/specs/` and of
every one of the six pin stems in `contracts/` at `323c7adf`. A component
therefore cannot contain `/`, `.`, `:`, whitespace, an upper-case letter, or be
empty, and `..` is not expressible in it.

This matters because the marker regexes are deliberately NOT moving (the
argument above): `_CAND_OPEN`'s `[^\s>]+` and `_ATTR`'s `\S+` accept any
non-whitespace run, so the value reaching the resolver is unvalidated by the
grammar's own patterns. **The resolver therefore validates the value against
this grammar BEFORE it constructs any path or reads any file.** A value that
fails it is a MALFORMED PINNED TARGET finding and NOTHING further happens for
it: no `contracts/<pin-id>-pin.yaml` string is built, no pin lookup is
attempted, and no filesystem read occurs. That ordering is the point —
validating after building a path is how `pinned:../../etc/passwd/x` would
become a read outside the pin registry, and it is why this paragraph is
normative in the `document-lifecycle` delta rather than advisory here.

For the four markers this issue #992 is about, the form resolves to
`target=pinned:openxwallet/openxwallet` — the pin id and the capability name
coincide here, which reads redundant and is nonetheless exactly right: the
product is `openxwallet` and the capability that left
`openspec/specs/openxwallet/` was `openxwallet`.

**Why this spelling and not another — the measured argument.** The existing
marker regexes in `scripts/doc_health/families.py:1308-1314` are:

```python
_CAND_OPEN = re.compile(
    r"^<!--\s*xspec:candidate((?:\s+[\w-]+=[^\s>]+)*)\s*-->$")
_SUPERSEDES = re.compile(
    r"^<!--\s*xspec:supersedes((?:\s+[\w-]+=[^\s>]+)*)\s*-->$")
_ATTR = re.compile(r"([\w-]+)=(\S+)")
```

Both attribute value classes — `[^\s>]+` and `\S+` — already admit `:` and
`/`. **`<!-- xspec:candidate target=pinned:openxwallet/openxwallet -->` parses
against the CURRENT patterns with no regex change at all.** That matters for a
reason beyond convenience: those patterns carry the comment "Canonical marker
grammar — owned by document-lifecycle, transcribed by reference. Any grammar
change is an upstream delta; update these regexes to follow, never to extend."
A form that needs no regex movement is a form that keeps that comment true.

A `/` inside an attribute value is already precedented and already ratified:
`spec=<capability>/<requirement-slug>` uses exactly that separator, and
`families.py:1391` splits it with `spec.split("/", 1)[0]`. The pinned form
reuses the house's own separator rather than inventing one.

**Alternatives on the form, rejected.**

- **A separate attribute, `target-pinned=<pin-id>/<capability>`.** Rejected: it
  splits "what is this block about" across two attribute names, so every reader
  of a marker must now check for two keys, and `fam_tag_hygiene`'s
  `if not target:` arm (line 1362) would have to learn that a missing `target`
  is sometimes lawful. One key with one grammar is fewer places to be wrong.
- **A bare product-qualified name, `openxwallet/openxwallet`.** Rejected: with
  no discriminating prefix, a future capability id containing a `/` — or a
  typo — becomes indistinguishable from a pinned reference, and the resolver's
  only recourse is to guess by trying both. `pinned:` makes the author's intent
  explicit in the document.
- **A URI, `target=repo:opensoft/openXwallet#openxwallet`.** Rejected: it names
  a REPOSITORY rather than this repository's own PIN of that repository, so it
  resolves to something openxFactory does not govern and cannot verify offline
  (see D-4's third rejection).

### D-1.1 — The `supersedes` marker's `spec=` is OUT OF SCOPE, and CLOSED

**Decision.** The pinned form is admitted in an `xspec:candidate` marker's
`target=` attribute ONLY. An `xspec:supersedes` marker's `spec=` value MUST NOT
carry the reserved `pinned:` prefix; a `spec=` that does is a tag-hygiene
finding, and the realization tests that refusal (task 3.3(e)) rather than
leaving it to the resolver's accident.

**Why it cannot simply be "and supersedes too".** `xspec:supersedes` carries no
`target=` attribute at all. It carries `spec=<capability>/<requirement-slug>`,
and `families.py:1387-1392` reads the capability as `spec.split("/", 1)[0]` —
a split at the FIRST separator. A pinned value there would have to be
`spec=pinned:<pin-id>/<capability>/<requirement-slug>`: three segments across
two separators, which that split reads as the capability `pinned:<pin-id>`,
silently dropping the capability name and the requirement slug into one
unparsed tail. A pinned `spec=` therefore needs its own parse rule, and writing
one is a second grammar decision this packet has no measured demand for.

**The measured demand, or its absence.** Measured at `323c7adf`: the four
markers issue #992 names are all `xspec:candidate` `target=` markers. The only
live `xspec:supersedes` markers in this repository outside `tests/` fixtures are
the four in
`ideation/staging/notebook-projection-identity/notebook-projection-identity.md`,
and every one of them names an IN-TREE capability — `lifecycle-notebook-
projection` and `credential-contracts` — both of which resolve today. No live
`supersedes` marker has a stale target, so no `supersedes` marker is waiting on
this grammar.

**Why CLOSED and not merely unmentioned.** Constitution Principle VII
(`.specify/memory/constitution.md:99-103`) says deferred features fail closed
rather than degrade open. A silence here would degrade open: the `pinned:`
prefix would reach `spec=` through the shared `_ATTR` pattern and resolve or
misresolve by accident. The `document-lifecycle` delta therefore states the
refusal as a rule and carries a scenario for it. Admitting a pinned `spec=` is
a later change, on evidence that a stale supersedes target exists.

## D-2 — Resolution: a VALID, COMPLETE pin record THAT ENUMERATES THE CAPABILITY

**Decision — AS TIGHTENED, D-2 FAILS CLOSED.** A `pinned:<pin-id>/<capability>`
target RESOLVES only where ALL THREE of the following hold. They are
PREREQUISITES and not arms: any one of them failing is an UNRESOLVED PINNED
TARGET, reported as a controlled finding naming the record and the remedy, and
nothing resolves on the strength of the other two.

1. **The pin id MUST resolve TO A NEUTRAL-PRODUCT PIN, and not to any
   pin-shaped file.** `<pin-id>` resolves when the RESOLUTION ROOTS carry
   `contracts/<pin-id>-pin.yaml` declaring **`kind: pinned_contract_manifest`**
   — the shape `neutral-product-pin` names in its own words: "`openxFactory`
   SHALL declare its consumption of an EXTERNAL neutral product in
   `contracts/<product>-pin.yaml`, REUSING `kind: pinned_contract_manifest`
   unchanged" (`openspec/specs/neutral-product-pin/spec.md:31-33`). An
   unresolvable pin id is a tag-hygiene finding exactly as an unresolvable
   capability is today. **And the kind alone is a LABEL, not a pin — SO THE
   RECORD MUST BE COMPLETE FOR ITS RECORD SHAPE, AGAINST
   `neutral-product-pin`'S OWN MEMBER LIST AND NOT A LIST THIS GRAMMAR WRITES
   DOWN.** An earlier drafting of this arm asked only for a `revision_kind` with
   its top-level referent, and that is MEASURABLY WEAKER than the ratified
   shape: `neutral-product-pin`'s requirement *An external neutral product is
   pinned by commit and digest, never by tag* obliges a SOURCE pin to carry,
   beside its `commit` and `revision_kind`, "a per-file `sha256` for every
   artifact the product's own manifest digests per file, and
   `pinned_by_commit_only:` for every artifact the product content-addresses by
   commit alone" (`openspec/specs/neutral-product-pin/spec.md:31-36`); it obliges
   a PUBLISHED-ARTIFACT pin to carry the artifact's digest as its referent with
   `revision_kind` declared accordingly (`:46-48`), NEITHER per-file list
   (`:55-56`), and "every field the consumer's verifier checks — including any
   secondary address the registry publishes — so that no declared field goes
   unverified" (`:62-65`); and its requirement *A pinned artifact that resolves
   dependencies at install time carries a vendored lockfile, and the install
   runs through it* obliges the vendored resolution, "a lockfile … addressed by a
   digest over its exact bytes recorded in the pin, together with the size of the
   tree it locks" (`:669-673`).

   **THE UNIT OF THAT COMPLETENESS IS THE RECORD SHAPE, NOT THE `revision_kind`
   ALONE — measured over all five `pinned_contract_manifest` records on
   `origin/main`, which carry THREE shapes and not two.** Two of the five
   declare `revision_kind: commit` and ENUMERATE their surface; two more declare
   the same revision kind and address their WHOLE TREE by one digest, carrying
   neither per-file list; the fifth is the published artifact. A required-member
   table keyed on `revision_kind` alone would therefore refuse
   `contracts/opendox-pin.yaml` and `contracts/openxdox-pin.yaml` — two valid
   records this repository ships — for lacking lists their shape does not have.

   **AND THE MEMBER SET OF A SHAPE IS THE SHAPE'S SHAPE-GUARD-REQUIRED SET.**
   The table holds EXACTLY the top-level members that shape's in-tree pin
   verifier REFUSES-WHEN-ABSENT IN ITS PURE, SOURCE-FREE SHAPE GUARDS — the
   refusals whose ONLY INPUT IS THE RECORD, which is what the verifiers' reader
   and guard functions run before any checkout, `git` call or network read —
   measured from the verifier scripts and cited member by member below. The
   ratified text supplies members where it NAMES them and is silent elsewhere —
   on shape (b) entirely, and on the published artifact's `package` and
   `binary` — and the shape-guard-required set completes it.

   **Why the SHAPE GUARD and not the FULL verifier, stated once — and why the
   check is NECESSARY BUT NOT SUFFICIENT BY DESIGN.** This resolver judges
   whether a NAME resolves to a pin record OF AN ADMITTED SHAPE. It never judges
   whether the pin is FAITHFUL TO ITS SOURCE, and the completeness contract is
   therefore NECESSARY for the shape's full verifier and DELIBERATELY NOT
   SUFFICIENT for it. Two grounds, both measured. FIRST, on a landed tree the
   check is redundant anyway: every record in `contracts/` already passes its
   FULL verifier, those verifiers being required checks, so no landed record can
   reach the resolver incomplete on either reading. What the check actually
   defends is the OFFLINE JUDGEMENT over arbitrary trees — a doc-health fixture
   tree, an aggregate of repositories, a `--single-repo` run over an arbitrary
   checkout, an added `contracts/evil-pin.yaml` — where no pin verifier has run
   at all. SECOND, a SOURCE-DEPENDENT check cannot be part of an offline,
   tree-local resolver without REPRODUCING THE VERIFIER'S I/O, which is the
   checkout, `git` and network work `neutral-product-pin`'s offline law forbids
   this pass. The measured example of what that leaves outside the contract is
   `scripts/validate-openreposhape-pin.py`'s **`pin-surface-undeclared`**
   (`:515-530`): it takes `source.paths()` (`:520`) — the files the RESOLVED
   SOURCE carries — and refuses a record that names, in NEITHER `files:` nor
   `pinned_by_commit_only:`, some file the product actually ships. Strip the 45
   path-only entries from `contracts/openreposhape-pin.yaml:201-246` and that
   check fires, while every shape guard in that script still passes; the
   resolver would accept such a record, and that is the by-design gap, not a
   defect. It cannot be closed offline: the question `pin-surface-undeclared`
   asks has no answer without the source. What the set DOES close is the other
   direction — on exactly those side-run trees, a resolver whose table were
   NARROWER than the shape's own guards would admit a record the repository's
   gate refuses at its FIRST shape check, which is the whole defect this arm
   exists to close; and one WIDER would refuse a record the gate admits. So the
   table is neither, and **the realization PINS it there with a TWO-LEG
   EQUIVALENCE TEST** (task 3.3(p)): a RECORD leg — the adapter accepts each
   real record, refuses it naming `m` for each `m` IN the table, and still
   accepts it for each top-level member that is neither in the table nor the
   `kind:` discriminator, that discriminator being the precondition gated on
   before any shape is selected — and a GUARD leg,
   which holds the table to the VERIFIERS rather than to itself, by calling each
   verifier's IMPORTABLE, SOURCE-FREE guard on the record minus `m`, or, where a
   member's refusal is reachable only inside `verify()`, by a MEASURED CITATION
   in the adapter's source that the test re-READS at the pinned script and line.
   The table is still CODE the resolver is reviewed with — the record never
   selects the code that judges it — but it is code a test holds against the
   guards it tracks, rather than a list that can drift unobserved.

   | record (`origin/main`) | shape | verifier | shape-guard-required members (script:line) | how the GUARD LEG pins each (measured) |
   | --- | --- | --- | --- | --- |
   | `contracts/openxwallet-pin.yaml` | (a) enumerated commit pin | `scripts/verify-openxwallet-pin.py` (`verify_pin:` at `:64`) | `submodule_path` `:194`, `revision_kind` `:219`, `commit` `:227`, `files` `:392` | importable source-free guards for three: `_submodule_path` `:185`, `_pinned_commit` `:203` (both `revision_kind` and `commit`). `files` has NO source-free entrypoint — its record-only refusal sits in `verify()` behind checks 1-3 — so it is pinned by CITATION: `:392-397`, "the pin lists no \`files:\` members, so it pins no bytes" |
   | `contracts/openreposhape-pin.yaml` | (a) enumerated commit pin | `scripts/validate-openreposhape-pin.py` (`:121`) | `revision_kind` `:239`, `commit` `:247`, `source_repository` `:258`, `files` `:438` | importable source-free guards for three: `pinned_commit` `:231` (both `revision_kind` and `commit`), `_source_repository` `:257`. `files` by CITATION: `:438-443`, the same refusal text, inside `verify(source, pin)` which takes a resolved `Source` |
   | `contracts/opendox-pin.yaml` | (b) whole-tree digest commit pin | `scripts/verify-opendox-pin.py` (`:156`) | `submodule_path` `:215`, `revision_kind` `:226`, `commit` `:234`, `digest_algorithm` `:246`, `digest_definition` `:253`, `digests` `:262` + `digests.tree_sha256` `:269` | ALL by importable source-free guard: `_submodule_path` `:213`, `_pinned_commit` `:224`, `_pinned_tree_digest` `:244` (the last covering `digest_algorithm`, `digest_definition`, `digests` and its `tree_sha256`) |
   | `contracts/openxdox-pin.yaml` | (b) whole-tree digest commit pin | `scripts/verify-openxdox-pin.py` (`:121`) | `submodule_path` `:257`, `revision_kind` `:276`, `commit` `:284`, `digest_algorithm` `:307`, `digest_definition` `:314`, `digests` `:322` + `digests.tree_sha256` `:329` | ALL by importable source-free guard: `_submodule_path` `:249`, `_pinned_commit` `:266`, `_pinned_tree_digest` `:294` |
   | `contracts/openspec-cli-pin.yaml` | (c) published-artifact pin | `scripts/validate-openspec-cli-pin.py` (`:376`, `consumer_entrypoint:` `:394`) | `revision_kind` `:592`, `version` `:601`, `integrity` `:619`, `shasum` `:646`, `package` `:658`, `lockfile` `:698`, `lockfile_integrity` `:708`, `lockfile_packages` `:731`, `binary` `:748` | ALL NINE by importable source-free guard: `pinned_version` `:584`, `pinned_integrity` `:611`, `pinned_package` `:657`, `pinned_lockfile` `:674` (pure despite its `pin_path` argument — it JOINS `pin_path.parent / name` at `:744` and opens nothing), `pinned_binary` `:747` |

   **The measured split: 27 of the 29 member entries are on the GUARD leg, and
   TWO are on the citation route** — `files` under shape (a), once per shape-(a)
   verifier. Every member is additionally on the RECORD leg, which is the leg
   that proves the table is neither wider nor narrower than declared; the GUARD
   leg is what proves the table still matches the VERIFIERS. All five scripts
   are importable the way this repository already imports them in its own tests
   (`importlib.util.spec_from_file_location`, as `tests/openxwallet_pin/`,
   `tests/openreposhape_pin/`, `tests/opendox_pin/` and `tests/openxdox_pin/`
   already do), and each guards its command-line entry behind
   `if __name__ == "__main__":`, so importing one starts no work.

   NOT refused-when-absent at the guard, and therefore NOT in the table, though
   each is refused when PRESENT and malformed: `pinned_by_commit_only:` under shape (a)
   (`scripts/verify-openxwallet-pin.py:443-448`,
   `scripts/validate-openreposhape-pin.py:487-491`, both reading it with an
   absent-is-empty default), and `dispositions:` under shape (c)
   (`scripts/validate-openspec-cli-pin.py:801-803`). The first of those is a
   member the RATIFIED TEXT does name (`:31-36`) — so the text is stricter here
   than the guard, and the difference is resolved, not averaged: the text's
   obligation binds the pin's AUTHOR and is `neutral-product-pin`'s to enforce,
   while THIS table is what the resolver may refuse a record on, and it does not
   refuse what the shape's guard admits. And it is precisely here that the
   necessary-not-sufficient boundary shows: DELETE `pinned_by_commit_only:` from
   `contracts/openreposhape-pin.yaml` and every guard in that script still
   passes while the FULL verifier raises `pin-surface-undeclared` (`:515-530`)
   against the real source — so the resolver accepts a record its required check
   would refuse, on a tree where that required check has already run and passed
   for the record as it actually stands. That is the designed shape of the
   contract, not a gap in it.

   **And shape (a)'s product-identity member has two spellings, measured.**
   `scripts/verify-openxwallet-pin.py:194` refuses a record without
   `submodule_path`; `scripts/validate-openreposhape-pin.py:258` refuses one
   without `source_repository`; neither verifier reads the other's member. So
   shape (a)'s entry is `revision_kind`, `commit`, `files` and EXACTLY ONE
   product-identity member, and AT THE RECORD GRAIN it resolves to that record's
   own verifier's set. Neither flattening works: the UNION would refuse
   `contracts/openxwallet-pin.yaml` for lacking `source_repository`, and the
   INTERSECTION would admit a record naming no product at all — and the
   equivalence test above fails the intersection outright, `submodule_path`
   being a top-level member of that record which its verifier refuses without.

   Two consequences the earlier drafting of this section got wrong, both
   corrected here. **First, shape (b) is admitted and not an omission.**
   `neutral-product-pin`'s ratified text is SILENT on it — the spellings
   `digest_definition`, `digests` and `tree_sha256` occur nowhere under
   `openspec/specs/` — so it is a REALIZED record shape, and the table admits it
   from the records themselves on the reasoning those records give
   (`contracts/opendox-pin.yaml:97-107`: the digest covers mode, oid and path
   for every entry of `git ls-tree -r`, "which is what lets this ONE digest
   cover a three-repository product"), which is the same reasoning the spec
   gives for the published artifact needing no enumeration
   (`openspec/specs/neutral-product-pin/spec.md:59-61`). Because no text admits
   a MIXTURE, a record carrying both `digests.tree_sha256` and a `files:` list
   matches neither (a) nor (b) and is refused naming both shapes tried, on that
   capability's own fail-closed rule (`:89`). **Second, shape (c)'s required set
   is NINE members — the shape guards' set, not a reading of the text alone.** An
   earlier drafting of this section named four (`version`, `integrity`,
   `shasum`, `lockfile`) and a later one six (adding `lockfile_integrity` and
   `lockfile_packages`); both were under-measured. `scripts/validate-openspec-cli-pin.py`
   refuses a record without any of NINE: `revision_kind` `:592`, `version`
   `:601`, `integrity` `:619`, `shasum` `:646`, `package` `:658`, `lockfile`
   `:698`, `lockfile_integrity` `:708`, `lockfile_packages` `:731`, `binary`
   `:748`. The `shasum` is the secondary address `:62-65` names rather than a
   member the spec spells; `lockfile_integrity` and `lockfile_packages` are what
   `:669-673` obliges BESIDE the committed lockfile — the digest "over its exact
   bytes" and "the size of the tree it locks", which is the record's own reason
   for carrying them (`contracts/openspec-cli-pin.yaml:321-327`); and `package`
   `:282` and `binary` `:370` the ratified text does not reach at all, naming
   the product the referent is OF and the executable the artifact installs
   (`:657-663`, `:747-754`). Each omission would have made this resolver's
   notion of a complete pin WEAKER than the verifier's, which on a fixture or
   side run is the difference between admitting and refusing a record the
   repository's own gate would refuse. A
   `contracts/evil-pin.yaml` holding `kind`, `revision_kind: commit` and a
   `commit` satisfies the weaker wording and resolves arbitrary pinned targets
   under it; it matches neither commit-pinned shape. The list stays with
   `neutral-product-pin` because of two member lists the weaker is always the one
   that admits — and if that capability later ratifies a VALIDATOR INTERFACE for
   `pinned_contract_manifest` records, this resolver adopts it as a follow-up,
   which is a change of that capability's making and not this packet's: **this
   packet opens NO delta against `neutral-product-pin`.**

   **AND THE JUDGEMENT GOES THROUGH A CODE-FIXED ROUTE, BECAUSE A RECORD MUST
   NOT CHOOSE THE CODE THAT JUDGES IT.** An earlier drafting of this arm reached
   the judgement through the verifier each record NAMES in its own `verify_pin:`
   member (`contracts/opendox-pin.yaml:156`,
   `contracts/openreposhape-pin.yaml:121`, `contracts/openspec-cli-pin.yaml:376`
   with its `consumer_entrypoint:` at `:394`, `contracts/openxdox-pin.yaml:121`,
   `contracts/openxwallet-pin.yaml:64`) — and "a verifier this tree carries" is
   not an execution boundary at all: the path is SELECTED BY THE DATA UNDER
   JUDGEMENT, so an added `contracts/<anything>-pin.yaml` could point the
   judgement at any path in the checkout. That route is WITHDRAWN. The resolver
   SHALL NOT execute, import or open any path a pin record selects, and
   `verify_pin:` is neither a prerequisite of resolution nor part of the shape
   this grammar requires — an observation about today's five records, nothing
   more. The realization instead writes **ONE shared, PURE, NON-EXECUTING
   ADAPTER** for `pinned_contract_manifest` records, code-fixed and reviewed with
   the resolver: it HOLDS the per-shape table, READS THE RECORD AND NOTHING
   ELSE, and is the single place the completeness judgement is made. It lives
   EITHER inside the resolver's own module (`scripts/doc_health/families.py`,
   already named by the `code_surface`, adding no file) OR in ONE shared helper
   module beside it under `scripts/doc_health/` — a choice of WHERE, settled at
   realization and counted exactly in `proposal.md:2`'s file bound, not a choice
   of ROUTE. A record whose `verify_pin:` value DIFFERS from what the adapter
   holds for that record is itself a controlled finding rather than a
   redirection. **THE ADAPTER NEITHER EDITS NOR CALLS THE FIVE PER-PRODUCT
   VERIFIERS.** Each of them carries its shape guards inline (for example
   `_pinned_commit`, `scripts/verify-openxdox-pin.py:266-291`, and
   `pinned_version`, `scripts/validate-openspec-cli-pin.py:584-608`), every one
   of them shells out to a subprocess, and
   `scripts/validate-openreposhape-pin.py` reaches the network through `urllib`
   — work `neutral-product-pin`'s offline law forbids this pass, and work a pure
   adapter never starts; they are product-specific rather than a shape-only API,
   so there is nothing in them to extract without changing them, and the adapter
   writes its own table instead. **The GUARD LEG of the equivalence test is the
   one place a verifier is imported at all, and it is a TEST rather than the
   resolver**: the test imports a FIXED, AUTHORED script path — never a path any
   record names — and calls only the source-free guards the table cites. The
   adapter imports nothing from them, at authoring time or at run time. The
   adapter and the containment helper of task 3.3(m) are both inside the
   packet's DECLARED `code_surface`, which names them, rather than leaving the
   realization to discover a file the declaration does not admit.

   **And the ROOT is the in-tree arm's root, not a new one.** Capability
   resolution already reads the document's OWN repository root first and the
   `openxFactory` root second — `for name in (repo, "openxFactory")`,
   `scripts/doc_health/families.py:1317-1321`, over `Context.repo_paths`
   (`scripts/doc_health/runner.py:39`) — and a single-repository run has one root
   and no fallback. The pinned arm uses THAT precedence unchanged, so the ORDER
   is unchanged and deterministic FOR THE ROOTS PRESENT in the run; inventing a
   precedence here would make the same marker resolve against different
   `contracts/<pin-id>-pin.yaml` files depending on how the checker was invoked.
   **What is guaranteed is the ORDER, not an identical OUTCOME across invocation
   scopes**, and the difference is worth stating rather than papering over: a
   single-repository run has one root, so a marker whose pin record lives only
   in the `openxFactory` root resolves under an aggregate run and is an
   unresolved pinned target under a single-repository run of the other
   repository. That is a difference of the ROOT SET the run was given — the same
   difference the in-tree capability arm already has — and not of a precedence
   this arm invented; the arm does not widen its root set to close it, and the
   finding names the root it searched so the difference is readable. And because there can be two roots, EVERY finding the
   pinned arm emits names the root it resolved against or failed to: under an
   aggregate run a bare "no pin record for `<pin-id>`" cannot be acted on.
   **And the path is RESOLVED
   before it is read**: the lexical grammar of D-1 stops a `..` inside the
   MARKER, and only resolved containment stops a committed SYMLINK at
   `contracts/<pin-id>-pin.yaml` redirecting the read out of the registry.
   **AND THE BOUNDARY ITSELF IS CHECKED BEFORE ANY CANDIDATE IS**, because the
   containment check has a second escape the candidate check cannot see: if
   `<root>/contracts` is ITSELF a symlink to another directory, an
   implementation comparing the candidate against `(root / "contracts")
   .resolve()` accepts and reads a file that is outside the LEXICAL registry
   the boundary names — the redirection having moved the boundary rather than
   been caught by it, and the comparison still passing. So the arm first
   requires that root's `contracts` to be a REAL, NON-REDIRECTING DIRECTORY
   INSIDE THE ROOT — it is a directory, it is not a symlink, and its resolved
   path equals its lexical path — and where it is not, the pinned arm REFUSES
   FOR THAT ROOT as a whole with a controlled finding naming the root, reading
   no candidate at all. Refusing the root rather than the marker is the honest
   grain: every pinned target that would resolve through that root is affected,
   and the defect is the registry directory, not any one record. The
   realization reuses the repository's own containment dialect rather than
   inventing a second one, but it CANNOT reuse `resolve_in_tree`
   (`scripts/validate-pin-registrations.py:237-267`) AS WRITTEN: that helper
   resolves against a module-global `ROOT` and asks only
   `resolved.is_relative_to(ROOT)`, so it answers the REPOSITORY question and
   not the `contracts/` one — a committed
   `contracts/foo-pin.yaml -> ../openspec/specs/…` symlink stays inside the
   repository and passes it — and a module-global root cannot speak for the
   per-repository and fixture roots this family actually runs against. The helper
   the realization uses therefore RECEIVES THE
   RESOLVING REPOSITORY ROOT AS A PARAMETER and checks the resolved candidate
   against THAT root's `contracts/` boundary before any read, whether by
   parameterizing `resolve_in_tree` or by extracting a shared helper both call. **A record that EXISTS but is corrupt is the same class
   of event, not a crash**: invalid YAML, a non-mapping document, or a mapping
   with no `kind` is reported as an unreadable pin record and the target does
   not resolve, with the run completing. The resolver reads a registry file it
   did not write, so the family owns the failure rather than propagating it —
   the house's convention for malformed persisted data — and task 3.3(k) tests
   one case per shape.

   **`kind: pinned_workflow` IS EXCLUDED, deliberately.** Of the six pin
   records, five are `pinned_contract_manifest` and one —
   `contracts/review-lane-pin.yaml` — is `pinned_workflow`, and it pins
   EXECUTABLE GOVERNANCE CODE, not a product whose units are capabilities: by
   its own opening lines it records "which codexFactory decision core judges
   openxFactory", a checked-out workflow core, and its `pinned_members:` are
   workflow source files. A capability of it does not exist to be named, so
   admitting it would put prerequisites 2 and 3 over a referent that has no
   capability set at all — a strictly worse case than the neutral-product one,
   where the pinned product does have a capability corpus even though this
   repository may not read it. The admissible set is therefore FIVE records today, and it
   tracks `neutral-product-pin`'s own kind rather than the presence of a
   pin-shaped file.
2. **THE RECORD MUST CARRY A WELL-FORMED `capabilities:` ENUMERATION.** The
   enumeration is a PREREQUISITE of resolution, not a condition on it. A record
   that carries NO top-level `capabilities:` member carries no enumeration for
   this purpose, and a pinned target naming it does NOT resolve: the pass
   reports an UNRESOLVED PINNED TARGET naming the record path and the remedy —
   the PUBLISHER adds `capabilities:` through a `neutral-product-pin` change —
   exactly as a MALFORMED enumeration already does. ABSENT and MALFORMED are
   two findings with two texts and ONE outcome, and neither is a licence.
3. **`<capability>` MUST BE A MEMBER OF THAT ENUMERATION.** A well-formed,
   non-empty enumeration that does not carry `<capability>` is an unresolved
   pinned target naming the enumeration — which is what it already was.

**AND THE ENUMERATION IS NAMED, so the prerequisite has a deterministic input
contract rather than an intention.** The resolver reads ONE member and nothing else: a
top-level `capabilities:` sequence of capability names, in the same kebab-case
shape an in-tree capability id takes, on the pin record itself. A pin record
without that member carries no enumeration for this purpose — the resolver does
NOT go looking for `files:`, `digests:`, `pinned_members:`, or any other list
and read capabilities out of it, because none of those is a capability list and
guessing between them is exactly the non-determinism this paragraph exists to
remove.

**AND A MALFORMED ENUMERATION IS ITS OWN FINDING, not a re-spelling of an
absent one.** A `capabilities:` member that is present but is NOT a NON-EMPTY
sequence of well-formed capability names — a scalar, a mapping, a null or
empty value, **an EMPTY sequence**, or a sequence carrying an item that is not
a capability-shaped name — is a MALFORMED ENUMERATION, and the pass reports it as a finding against the PIN
RECORD — reached THROUGH THE MARKER that names the record, since
`fam_tag_hygiene` is a document-and-marker scan: no registry-wide sweep of pin
records is added by this change, and a pin record no live marker names is
`neutral-product-pin`'s business. It MUST NOT be read as "this record carries no
enumeration". Under the tightening ABSENT and MALFORMED reach the SAME
OUTCOME — the target does not resolve — and they remain TWO findings, because
they name two different defects with two different remedies: a malformed member
is REPAIRED by whoever wrote it, an absent one is PUBLISHED by the pinned
product's publisher. Reading a broken member as absent would print the
publisher's remedy at a defect the publisher did not cause; reading an absent
one as malformed would accuse a sound record of carrying a broken member. Any
pinned target naming that record fails to resolve while the enumeration is
malformed. This is constitution Principle VII's fail-closed rule applied to the
prerequisite's own input, and the tightening applies the same rule to the
member's ABSENCE.

`capabilities:` is RESERVED here as the prerequisite's spelling; **this
packet adds it to no pin record and to no schema**, and admitting the member
into a real pin record is a `neutral-product-pin` change with the publisher, as
the paragraph below says. THERE IS NO DORMANT ARM AND NOTHING SELF-ARMS: the
enumeration is a prerequisite, so until a publisher publishes one, NO pinned
target naming that record resolves. The trigger is still a named member,
checkable by reading, and the realization's fixture cases (task 3.3(c) and (d))
are fixture pin records carrying it — fixtures are not the pin registry and add
no pin byte.

**What the measurement over the pin registry shows, and what the tightening
costs.** All six pin
records in `contracts/` were read at `323c7adf`. NONE enumerates capabilities,
and that is the property the whole cost of the tightening turns on; what each
record addresses INSTEAD differs record by record — files, tree digests,
workflow members, or no enumeration at all:

| pin record | what it enumerates |
| --- | --- |
| `contracts/openxwallet-pin.yaml` | `files:` (8 digested paths) + `pinned_by_commit_only:` (6 paths) |
| `contracts/openreposhape-pin.yaml` | `files:` + `pinned_by_commit_only:` |
| `contracts/opendox-pin.yaml` | `digests:` (`digest_definition: sorted-ls-tree-r-v1`) |
| `contracts/openxdox-pin.yaml` | `digests:` (same definition) |
| `contracts/openspec-cli-pin.yaml` | NO enumeration of any kind: ONE whole-artifact `integrity:` digest over the published tarball + a `lockfile:` referent. It carries neither `files:` nor `pinned_by_commit_only:`, and its own lines 69-76 say why ("ONE digest covers ALL 389 files") |
| `contracts/review-lane-pin.yaml` | `pinned_members:` (workflow members) |

`grep -n 'capabilit' contracts/*pin*.yaml` returns only PROSE occurrences
inside comment banners — no key, no list, in any of the six. **A rule requiring
the capability to appear in the pin record therefore refuses, TODAY, every
marker this change was filed for** — all four of them. That is the COST of the
tightening; it was measured before the decision rather than discovered after
it, and the ratifier took it with the measurement in front of him (the RULED
paragraph below). What the four markers gain from the packet even so is a
LAWFUL FORM to be written in and a TRUE finding to carry — "unresolved pinned
target: `contracts/openxwallet-pin.yaml` carries no `capabilities:`
enumeration; the publisher adds one through a `neutral-product-pin` change" —
in place of today's false remedy, which instructs the author to name a
capability under `openspec/specs/` that does not exist.

**And the honest consequence, stated rather than hidden.** Under the tightening
a pinned target asserts EXACTLY what an in-tree target asserts: the referent is
checked, and the capability NAME is checked against a closed list — the pin
record's own enumeration, every row of which is a byte the PUBLISHER published
and this repository copied unchanged. Nothing is taken on the author's word,
and openxFactory's offline law (`neutral-product-pin`: the verifier "never
reads the network") is untouched, because the list being read is in this
repository's own tree. The price is paid in TIME rather than in strength, and
it is paid by the four markers this change was filed for. NO pin record in the
tree carries an enumeration today, so the four `target=openxwallet` findings
stay OPEN until this packet is RATIFIED (done), REALIZED (a separate later
word, not given) AND openXwallet's pin record publishes a `capabilities:`
enumeration (the publisher's act, not this repository's). After realization the
four findings CHANGE FORM rather than close: from "unresolved target=openxwallet
— name a capability under `openspec/specs/` or an active change" to "unresolved
pinned target — `contracts/openxwallet-pin.yaml` carries no `capabilities:`
enumeration; remedy: the publisher adds one through a `neutral-product-pin`
change". Still FOUR, still `error`-band, and at last pointing at the act that
would clear them.

**THE CONSTITUTIONAL OBJECTION, PUT IN THE PACKET RATHER THAN LEFT TO A
REVIEWER — AND ANSWERED BY THE RULING BELOW.** This section is KEPT as the
record of the tension and of exactly what was weighed; it describes the
AS-FILED design, which the re-ruling of 2026-09-13 superseded, and it is
history rather than a live reading of D-2. Constitution Principle VII
(`.specify/memory/constitution.md:99-103`)
says registries "of capabilities, outcomes, purposes, and states are closed:
unrecognized values are rejected, and deferred features fail closed rather than
degrade open." AS FILED, with the enumeration conditional, the CAPABILITY
segment was an OPEN set: `pinned:openxwallet/typo` would have resolved, and so
would a capability name belonging to some other product entirely. That
objection is sound as far as it goes, and three things were true of it at
once.

1. **The registry this repository OWNS is closed, and it is the one being
   checked.** `<pin-id>` is drawn from the pin registry, an unrecognized pin id
   is REJECTED, and that is strictly more than the status quo — which rejects
   the whole target and then instructs the author, in a fixed remedy string, to
   name a capability the prose is not about.
2. **The capability segment names a unit of a corpus openxFactory does not
   govern and may not read.** `neutral-product-pin`'s offline law binds the
   deterministic pass to this repository's tree. A closed registry over another
   publisher's capability set would have to be INVENTED here — exactly the row
   `openxwallet-pin.yaml:66-69` refuses ("the values are copied unchanged,
   which is what makes the shed checkable against the carve").
3. **The fail-closed alternative is a refusal of the change, not a tightening
   of it.** "Report a missing enumeration as unresolved" is, measured, the rule
   that refuses all four markers this change exists to admit, because no pin
   record in the tree carries an enumeration. It does not narrow the mechanism;
   it removes it.

**RULED — and the tension is closed by the RULING, not by the argument.** Task
1.2 put this to Brett Heap (openxFactory repository owner) as a veto point in
exactly those terms, and he ruled TWICE; the second ruling SUPERSEDES the first
on this decision. FIRST, 2026-09-12 at approximately 23:20Z, by interactive
multi-choice: **"Ratify 1.2 as filed"** — the options "Ratify with tightening:
fail closed" and "Ratify with tightening: enumeration owed as a named
successor" were offered and NOT taken. THEN, 2026-09-13T01:25:07Z (±3 min), on
the same question re-raised over Copilot review thread `PRRT_kwDOTAvnrs6h1H-H`
on ratification pull request #1019 — which put point 1 above back to him and
added that "merely recording this as a live constitutional question does not
create an exception or amend the constitution" — he selected **"Tighten to
fail-closed after all"**, whose description read, verbatim: *"Reopens 1.2: D-2
refuses a pinned target whose record carries no capabilities enumeration; the
four markers stay unresolvable until openXwallet's pin publishes one. Reverts
your 23:20Z selection; a fix round re-encodes and the record changes."* Not
taken: "Record my as-filed ruling as the explicit justification (Recommended)",
"Same, PLUS name a Principle VII clarification as an owed successor", "Hold
#1019 — I will read the thread myself". Record, and THE ONE CITATION:
openxFactory #992, comment
https://github.com/opensoft/openxFactory/issues/992#issuecomment-5649935136.
Point 3 above was the argument AGAINST fail-closed, and it is OVERRULED — with
its measurement intact and its conclusion refused. What fail-closed removes is
not the mechanism but the mechanism's ONE OPEN SET. The FORM (D-1), the pin
check (prerequisite 1), the stale-target rule (D-3) and a TRUE finding in place
of today's false remedy all stand; what the four markers wait on is a publisher
act, and a mechanism that waits is not a mechanism that was removed.

**PRINCIPLE VII IS THEREFORE SATISFIED BY CONSTRUCTION, and nothing is owed
around it.** The capability segment is no longer an open set: it is checked
against a closed registry — the pin record's own `capabilities:` enumeration —
and a deferred or absent enumeration FAILS CLOSED rather than degrading open,
which is the principle's own sentence. NO Complexity-Tracking justification and
NO constitution amendment is owed by this packet, because there is no longer a
violation to justify or to amend around.

**Why not require the enumeration and add it to `openxwallet-pin.yaml` in the
same breath.** Because that would be openxFactory writing a claim about
openXwallet's capability set into openxFactory's own pin record, where the
publisher cannot see it drift. The pin's discipline is that every row in it is
a byte the PUBLISHER published (`openxwallet-pin.yaml:66-69`: "the values are
copied unchanged, which is what makes the shed checkable against the carve").
An invented capability list is exactly the kind of row that file's own comments
refuse ("PATH ONLY, with no invented per-file digests"). Adding such a list is
a legitimate future change — one that belongs to `neutral-product-pin` and to a
conversation with the publisher, not to a marker-grammar extension. **Under the
tightening this paragraph is also the reason the four findings STAY OPEN**: the
act that clears them is the publisher's, and this repository declines to forge
it on the publisher's behalf.

## D-3 — The stale-target rule `document-lifecycle` does not have

**Decision.** `document-lifecycle` gains this sentence, which today it lacks in
any form:

> When a marker's target capability EXITS the corpus, the marker either takes
> the pinned form naming the product that now holds the capability, or the
> block is unfenced — never silently retargeted to a different capability, and
> never silently deleted.

**Why it is needed as a RULE and not only as a remedy string.** The archive
rejected both mechanical fixes in its own prose
(`archive/2026-08-28-split-openxwallet-repo/tasks.md:1779-1784`), and the house
then re-derived the same conclusion independently for
`wallet-carried-work-authority` (`ideation/staging/INDEX.md:2362-2366`). Twice
reasoned, nowhere written. The next author to meet a stale target has nothing
to read, and the checker's fixed remedy string actively points at the wrong
answer — "name a capability under `openspec/specs/`" is, for these four blocks,
an instruction to write something false.

**Why "or the block is unfenced" is in the rule and not omitted as obvious.**
Because unfencing is a REAL, LAWFUL outcome with a cost that should be visible
when it is chosen: an unfenced block leaves the conversion queue. The rule
names it as a choice an author makes deliberately, beside the pinned form,
rather than as the thing that happens when nobody decides. It is also the
outcome the house has already chosen once, on record, for
`wallet-carried-work-authority`.

## D-4 — Alternatives rejected

- **Retarget the four markers to an in-tree capability.** Rejected by the
  archive itself, verbatim: retargeting "would make the marker name a
  capability the tagged prose is not about"
  (`tasks.md:1781-1783`). The two candidates it names,
  `domain-descendant-boundary` and `neutral-product-pin`, are about the
  descendant boundary and about pinning MECHANICS; the tagged prose at
  `openxwallet-neutral-home.md:222-238` is about the wallet contracts being a
  product misfiled as features of a factory layer. The marker would resolve and
  the document would lie.
- **Delete the four markers.** Rejected by the archive itself, verbatim:
  deleting them "would silently drop four blocks out of the conversion queue"
  (`tasks.md:1783-1784`). It also clears the finding by removing the evidence,
  which is the failure mode `dispositions.yaml` exists to make visible rather
  than to enable.
- **Name the external repository directly** (`target=opensoft/openXwallet` or a
  URI form). Rejected: the checker cannot resolve it. `neutral-product-pin`'s
  offline law means the deterministic pass reads this repository's tree and
  nothing else; a bare repository name has no in-tree referent to check
  against, so the resolver would have to either accept every well-formed
  repository name unchecked — strictly weaker than D-2, which checks the pin
  record AND the capability against that record's own enumeration — or read the
  network, which the capability forbids.
- **Suppress the four findings with a disposition.** Rejected, and it would not
  work: `health/dispositions.yaml` is read only by the `uncited_resolutions`
  path, so a disposition does not remove an ACTIVE tag-hygiene finding. It
  would also be the wrong act — the findings are TRUE. The grammar is the
  defect, not the report.
- **Widen `_resolve_capability` to accept any name found in an archived
  change's spec deltas.** Rejected: `openspec/specs/openxwallet/` is gone from
  the live corpus but its text survives in the split archive, so this WOULD
  make all four markers resolve — and it would make every capability that has
  ever existed resolve forever, including ones deleted because they were wrong.
  A referent that cannot stop being a referent is not a check.

## D-5 — Realization is ONE later pull request, and this is not it

**Decision.** Realization is a single pull request in this repository, after
ratification, carrying four surfaces:

1. **The resolver.** `scripts/doc_health/families.py` —
   `_resolve_capability` (line 1317) gains the pinned arm, or a sibling
   resolver is added beside it and `fam_tag_hygiene`'s two call sites (lines
   1366 and 1390) dispatch on the `pinned:` prefix. The finding text for an
   unresolved pinned target names the PIN, not `openspec/specs/`. No regex
   moves (D-1).
2. **The tests.** Under `tests/doc-health/` — the hyphenated tests directory, beside the existing `tests/doc-health/fixtures/tag-hygiene/` tree; only the PACKAGE is `scripts/doc_health/` — and BOTH SIDES of D-2's
   enumeration PREREQUISITE, so the realization cannot satisfy the list while
   omitting either: a pinned target whose pin record carries NO `capabilities:`
   member does NOT resolve and emits an unresolved-pinned-target finding naming
   that record and the PUBLISHER's remedy; an unresolvable pin id emits a
   finding naming the PIN REGISTRY; a fixture pin record that DOES enumerate
   capabilities emits nothing for a LISTED capability and a finding naming the
   enumeration for an UNLISTED one; a `supersedes` marker whose `spec=` value
   carries the reserved `pinned:` prefix is REFUSED with the EXACT remedy
   sentence the scenario requires, asserted verbatim rather than as "a finding"
   (D-1.1); a record of a kind
   other than `pinned_contract_manifest` does not resolve a pinned target; a
   PRESENT but malformed `capabilities:` member — an EMPTY sequence among the
   malformed shapes — emits a malformed-enumeration finding and the target
   naming it does not resolve; a pinned value that does not match the lexical
   grammar (extra `/` segments, a traversal or dotted component, an upper-case
   or empty component) emits a malformed-pinned-target finding with NO path
   built and NO pin lookup attempted; and the existing in-tree resolution is
   unchanged. **And the family's own remedy pin moves with the arm**: every new
   action string goes into `EXPECTED_ACTIONS` at
   `tests/doc-health/test_families.py:751`, whose `assert_actions_pinned`
   requires that set to equal what the family statically carries and
   behaviourally emits, EXACTLY and in both directions — so a new arm that
   skips it reddens the suite, and that table is what keeps the pin-registry
   remedy and the candidate-`target=` remedy from drifting back to the in-tree
   string.
3. **The four markers**, retargeted to `target=pinned:openxwallet/openxwallet`
   — `openxwallet-neutral-home.md` lines 222, 242 and 280, and
   `notebook-access-wallet-governance.md` line 107 — together with
   `docs/document-lifecycle.md`'s Prose Tagging Markers section carrying the
   new form and D-3's sentence.
4. **The stale `INDEX.md` line.** `ideation/staging/INDEX.md:2262-2265` still
   reads "three live `xspec:candidate` blocks (all targeting `openxwallet`, all
   resolving…)" — true when written, false since 2026-08-28. The realization
   makes it true again rather than merely deleting the claim.

**Why one pull request and not four.** Because surfaces 1 and 3 are a lockstep
pair in both directions: retargeting the markers before the resolver lands
turns four `unresolved target` findings into four `malformed marker` findings,
and landing the resolver before the markers leaves the four findings standing
with a fix available and unapplied. The evidence `release-realization` wants —
merged plus green — is one run over a tree where both halves are present.

**The archive gate.** This packet carries a non-empty `code_surface`, so it
archives ONLY on merged-plus-green realization evidence, cited at the TREE
grain. The evidence is the realization pull request's green required
`pytest-suite` run plus a `--single-repo` doc-health run over that tree showing
NO NEW REGRESSIONS and the four `tag-hygiene` findings CHANGED IN FORM — from
`unresolved target=openxwallet` to an unresolved PINNED target naming
`contracts/openxwallet-pin.yaml` and the publisher's remedy. **The evidence
MUST NOT claim the four go to ZERO at realization, because under the tightening
they do not.** Their count reaches zero only when openXwallet's pin record
publishes a `capabilities:` enumeration carrying `openxwallet` — the
publisher's act, and no part of this packet or of its realization.
