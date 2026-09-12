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

## D-2 — Resolution: the pin record's existence is the check

**Decision.** Resolution of `pinned:<pin-id>/<capability>` has two arms:

1. **The pin id MUST resolve TO A NEUTRAL-PRODUCT PIN, and not to any
   pin-shaped file.** `<pin-id>` resolves when this repository carries
   `contracts/<pin-id>-pin.yaml` declaring **`kind: pinned_contract_manifest`**
   — the shape `neutral-product-pin` names in its own words: "`openxFactory`
   SHALL declare its consumption of an EXTERNAL neutral product in
   `contracts/<product>-pin.yaml`, REUSING `kind: pinned_contract_manifest`
   unchanged" (`openspec/specs/neutral-product-pin/spec.md:31-33`). An
   unresolvable pin id is a tag-hygiene finding exactly as an unresolvable
   capability is today.

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
"absent".** A `capabilities:` member that is present but is NOT a sequence of
well-formed capability names — a scalar, a mapping, an empty value, or a
sequence carrying an item that is not a capability-shaped name — is a
MALFORMED ENUMERATION, and the pass reports it as a finding against the PIN
RECORD. It MUST NOT be read as "this record carries no enumeration", because
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
   carries the reserved `pinned:` prefix is REFUSED (D-1.1); a record of a kind
   other than `pinned_contract_manifest` does not resolve a pinned target; a
   PRESENT but malformed `capabilities:` member emits a malformed-enumeration
   finding and the target naming it does not resolve; and the existing in-tree
   resolution is unchanged.
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
