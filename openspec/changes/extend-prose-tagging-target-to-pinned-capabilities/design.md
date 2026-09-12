# Design: extend-prose-tagging-target-to-pinned-capabilities

Status: draft

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

## D-2 — Resolution: a VALID, COMPLETE neutral-product pin record is the check

**Decision.** Resolution of `pinned:<pin-id>/<capability>` has two arms:

1. **The pin id MUST resolve TO A NEUTRAL-PRODUCT PIN, and not to any
   pin-shaped file.** `<pin-id>` resolves when the RESOLUTION ROOTS carry
   `contracts/<pin-id>-pin.yaml` declaring **`kind: pinned_contract_manifest`**
   — the shape `neutral-product-pin` names in its own words: "`openxFactory`
   SHALL declare its consumption of an EXTERNAL neutral product in
   `contracts/<product>-pin.yaml`, REUSING `kind: pinned_contract_manifest`
   unchanged" (`openspec/specs/neutral-product-pin/spec.md:31-33`). An
   unresolvable pin id is a tag-hygiene finding exactly as an unresolvable
   capability is today. **And the kind alone is a LABEL, not a pin — SO THE
   RECORD MUST BE COMPLETE FOR ITS REVISION KIND, AGAINST
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
   tree it locks" (`:669-673`). Today's one published-artifact record carries
   exactly that set — `version`, `integrity`, `shasum`, `lockfile` at
   `contracts/openspec-cli-pin.yaml:289-328`, the `shasum` being the secondary
   address `:62-65` names rather than a member the spec spells. A
   `contracts/evil-pin.yaml` holding `kind`, `revision_kind: commit` and a
   `commit` satisfies the weaker wording and resolves arbitrary pinned targets
   under it; it does not satisfy the ratified one. The list stays with
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
   more. The realization instead picks ONE of exactly two code-fixed forms, both
   reviewed with the resolver: **(a) preferred — a shared, importable,
   NON-EXECUTING shape validator** for `pinned_contract_manifest` records, reused
   if the tree later carries one and otherwise added under `scripts/doc_health/`;
   **(b) a CLOSED dispatch table inside the resolver's own module**, mapping each
   admitted pin id to its validator, where a record whose `verify_pin:` value
   DIFFERS from the table's entry is itself a controlled finding rather than a
   redirection. Form (a) is preferred because it also answers the offline law:
   each of the five verifiers carries its shape guard inline (for example
   `_pinned_commit`, `scripts/verify-openxdox-pin.py:266-291`, and
   `pinned_version`, `scripts/validate-openspec-cli-pin.py:584-608`), every one
   of them shells out to a subprocess, and
   `scripts/validate-openreposhape-pin.py` reaches the network through `urllib`
   — work `neutral-product-pin`'s offline law forbids this pass, and work a
   non-executing validator never starts. NEITHER FORM EDITS THOSE FIVE
   VERIFIERS: they are product-specific rather than a shape-only API, so there
   is nothing in them to extract without changing them, and form (a) writes its
   own module instead. Both forms are inside the packet's DECLARED
   `code_surface`, which names them — the shape-validator module under
   `scripts/doc_health/` for form (a) (form (b) adds no file) and the
   containment helper of task 3.3(m) — rather than leaving the realization to
   discover a file the declaration does not admit.

   **And the ROOT is the in-tree arm's root, not a new one.** Capability
   resolution already reads the document's OWN repository root first and the
   `openxFactory` root second — `for name in (repo, "openxFactory")`,
   `scripts/doc_health/families.py:1317-1321`, over `Context.repo_paths`
   (`scripts/doc_health/runner.py:39`) — and a single-repository run has one root
   and no fallback. The pinned arm uses THAT precedence unchanged, so a marker
   resolves the same way whether the checker runs over one repository or over an
   aggregate; inventing a precedence here would make the same marker resolve
   against different `contracts/<pin-id>-pin.yaml` files depending on how the
   checker was invoked. And because there can be two roots, EVERY finding the
   pinned arm emits names the root it resolved against or failed to: under an
   aggregate run a bare "no pin record for `<pin-id>`" cannot be acted on.
   **And the path is RESOLVED
   before it is read**: the lexical grammar of D-1 stops a `..` inside the
   MARKER, and only resolved containment stops a committed SYMLINK at
   `contracts/<pin-id>-pin.yaml` redirecting the read out of the registry. The
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
   admitting it would let `pinned:review-lane/<anything>` resolve against a
   referent that has no capability set at all — the weakest possible reading of
   arm 2, and a strictly worse one than the neutral-product case, where the
   pinned product does have a capability corpus even though this repository may
   not read it. The admissible set is therefore FIVE records today, and it
   tracks `neutral-product-pin`'s own kind rather than the presence of a
   pin-shaped file.
2. **The capability segment is checked for SHAPE, and resolved further ONLY if
   the pin record enumerates capabilities.** Today none does. If a pin record
   carries a capability enumeration, the named capability MUST appear in it.

**AND THE ENUMERATION IS NAMED, so the arm has a deterministic input contract
rather than an intention.** The resolver reads ONE member and nothing else: a
top-level `capabilities:` sequence of capability names, in the same kebab-case
shape an in-tree capability id takes, on the pin record itself. A pin record
without that member carries no enumeration for this purpose — the resolver does
NOT go looking for `files:`, `digests:`, `pinned_members:`, or any other list
and read capabilities out of it, because none of those is a capability list and
guessing between them is exactly the non-determinism this paragraph exists to
remove.

**AND A MALFORMED ENUMERATION FAILS CLOSED, rather than degrading into
"absent".** A `capabilities:` member that is present but is NOT a NON-EMPTY
sequence of well-formed capability names — a scalar, a mapping, a null or
empty value, **an EMPTY sequence**, or a sequence carrying an item that is not
a capability-shaped name — is a MALFORMED ENUMERATION, and the pass reports it as a finding against the PIN
RECORD — reached THROUGH THE MARKER that names the record, since
`fam_tag_hygiene` is a document-and-marker scan: no registry-wide sweep of pin
records is added by this change, and a pin record no live marker names is
`neutral-product-pin`'s business. It MUST NOT be read as "this record carries no enumeration", because
that reading converts a broken enumeration into a licence: the record would
silently drop back to arm 1 and admit every capability name. Any pinned target
naming that record fails to resolve while the enumeration is malformed. This is
constitution Principle VII's fail-closed rule applied to the arm's own input,
and it is the one place the arm can turn a defect into permissiveness.

`capabilities:` is RESERVED here as the trigger's spelling; **this
packet adds it to no pin record and to no schema**, and admitting the member
into a real pin record is a `neutral-product-pin` change with the publisher, as
the paragraph below says. That is what makes arm 2 dormant today and
self-arming later: the trigger is a named member, checkable by reading, and the
realization's fixture cases (task 3.3(c) and (d)) are fixture pin records
carrying it — fixtures are not the pin registry and add no pin byte.

**Why the second arm is conditional — measured, not assumed.** All six pin
records in `contracts/` were read at `323c7adf`. NONE enumerates capabilities,
and that is the only property this arm rests on; what each record addresses
INSTEAD differs record by record — files, tree digests, workflow members, or no
enumeration at all:

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
the capability to appear in the pin record would therefore refuse every marker
the rule exists to admit**, including all four this change was filed for. That
is the whole argument for arm 2 being conditional.

**And the honest consequence, stated rather than hidden.** Under arm 1 alone, a
pinned target asserts less than an in-tree target does: it says "this block is
about a capability of a product this repository pins", and the pin is checked,
but the capability NAME is taken on the author's word. That is a real
weakening, and it is accepted for three reasons. First, it is strictly more
than the status quo, which resolves nothing and reports an error. Second, the
name is not unchecked by the house — it is unchecked by THIS checker; the
pinned product's own corpus is where a capability name is authoritative, and
openxFactory's offline law (`neutral-product-pin`: the verifier "never reads
the network") forbids the checker from going and looking. Third, the
requirement is written so that the moment a pin record DOES enumerate
capabilities, arm 2 binds automatically — no further grammar delta, no second
change, no migration of existing markers.

**THE CONSTITUTIONAL OBJECTION, PUT IN THE PACKET RATHER THAN LEFT TO A
REVIEWER.** Constitution Principle VII (`.specify/memory/constitution.md:99-103`)
says registries "of capabilities, outcomes, purposes, and states are closed:
unrecognized values are rejected, and deferred features fail closed rather than
degrade open." Under arm 1 alone the CAPABILITY segment is an OPEN set:
`pinned:openxwallet/typo` resolves, and so does a capability name belonging to
some other product entirely. That objection is sound as far as it goes, and
three things are true of it at once.

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

**This is the packet's one decision where the constitution can be read against
the design, and it is NOT resolved by argument here.** Task 1.2 puts it to
Brett Heap as a veto point in those terms.

**Why not require the enumeration and add it to `openxwallet-pin.yaml` in the
same breath.** Because that would be openxFactory writing a claim about
openXwallet's capability set into openxFactory's own pin record, where the
publisher cannot see it drift. The pin's discipline is that every row in it is
a byte the PUBLISHER published (`openxwallet-pin.yaml:66-69`: "the values are
copied unchanged, which is what makes the shed checkable against the carve").
An invented capability list is exactly the kind of row that file's own comments
refuse ("PATH ONLY, with no invented per-file digests"). Adding such a list is
a legitimate future change — one that belongs to `neutral-product-pin` and to a
conversation with the publisher, not to a marker-grammar extension.

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
  repository name unchecked — strictly weaker than D-2 arm 1, which at least
  checks the pin — or read the network, which the capability forbids.
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
2. **The tests.** Under `tests/doc-health/` — the hyphenated tests directory, beside the existing `tests/doc-health/fixtures/tag-hygiene/` tree; only the PACKAGE is `scripts/doc_health/` — and BOTH cases of D-2's
   conditional arm, so the realization cannot satisfy the list while omitting
   the branch: a resolving pinned target under a pin record carrying no
   capability enumeration emits nothing; an unresolvable pin id emits a finding
   naming the PIN REGISTRY; a fixture pin record that DOES enumerate
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
the four `tag-hygiene` findings at ZERO and no new regressions.
