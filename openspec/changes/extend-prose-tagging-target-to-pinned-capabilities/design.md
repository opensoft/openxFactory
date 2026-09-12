# Design: extend-prose-tagging-target-to-pinned-capabilities

Status: draft

Every figure in this document was MEASURED at this branch's base
(`origin/main` = `323c7adf`), not remembered. Line numbers cite that tree.

## D-1 — The form: `target=pinned:<pin-id>/<capability>`

**Decision.** A candidate or supersedes marker MAY name its target as
`pinned:<pin-id>/<capability>`, where:

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

## D-2 — Resolution: the pin record's existence is the check

**Decision.** Resolution of `pinned:<pin-id>/<capability>` has two arms:

1. **The pin id MUST resolve.** `<pin-id>` resolves when this repository
   carries a pin record for it — today, `contracts/<pin-id>-pin.yaml` declaring
   `kind: pinned_contract_manifest` or `kind: pinned_workflow`. An unresolvable
   pin id is a tag-hygiene finding exactly as an unresolvable capability is
   today.
2. **The capability segment is checked for SHAPE, and resolved further ONLY if
   the pin record enumerates capabilities.** Today none does. If a pin record
   carries a capability enumeration, the named capability MUST appear in it.

**Why the second arm is conditional — measured, not assumed.** All six pin
records in `contracts/` were read at `323c7adf`. Their enumerations are of
FILES, never of capabilities:

| pin record | what it enumerates |
| --- | --- |
| `contracts/openxwallet-pin.yaml` | `files:` (8 digested paths) + `pinned_by_commit_only:` (6 paths) |
| `contracts/openreposhape-pin.yaml` | `files:` + `pinned_by_commit_only:` |
| `contracts/opendox-pin.yaml` | `digests:` (`digest_definition: sorted-ls-tree-r-v1`) |
| `contracts/openxdox-pin.yaml` | `digests:` (same definition) |
| `contracts/openspec-cli-pin.yaml` | a package `integrity:` + a lockfile |
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
2. **The tests.** Under `tests/doc_health/`, at minimum: a resolving pinned
   target emits nothing; an unresolvable pin id emits a finding naming the pin;
   a pinned form on a `supersedes` marker behaves consistently with the
   candidate arm; and the existing in-tree resolution is unchanged.
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
