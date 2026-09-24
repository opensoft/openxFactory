# Design: admit-code-leg-under-pinned-root

Status: draft

For: openxFactory [#1150](https://github.com/opensoft/openxFactory/issues/1150)
Lane: openxfactory-5 (openXfactory-5)

**WHAT THIS DOCUMENT IS.** D0 is the measurement, taken before any decision,
with the commands so it reproduces. D1 is the shape, put with its alternatives
costed and now RULED. D2, D3 and D5 are what the ruled shape is made of and are
not put separately. D4 and D6 are put for a veto with the recommendation first.
D7 is the rows the realization owes, D8 the sequencing and sibling search, and
D9 what is measured and deliberately not taken.

## D0. The measurement, taken before the design

Taken on a fresh clone of `opensoft/openxFactory` at `origin/main` `1d14fee6`.

### D0.1 The two pins, and openxFactory's own gitlinks for the same roots

```
$ grep -n '^source_repository:\|^submodule_path:\|^commit:\|^revision_kind:' \
    contracts/opendox-pin.yaml contracts/openxdox-pin.yaml
  contracts/opendox-pin.yaml:   source_repository: opensoft/openDox
                                submodule_path: openDox
                                commit: "dc7aa08fe48c8d17b596b0daa1ce87cdc0472aca"
                                revision_kind: commit
  contracts/openxdox-pin.yaml:  source_repository: opensoft/openXdox
                                submodule_path: openXdox
                                commit: "2f3f857daccce6ade3a15e0f3d0e926f9ff7c925"
                                revision_kind: commit

$ git ls-files -s | awk '$1=="160000"'
  160000 dc7aa08fe48c8d17b596b0daa1ce87cdc0472aca 0  openDox
  160000 2f3f857daccce6ade3a15e0f3d0e926f9ff7c925 0  openXdox
  (and openXwallet, installs/omnigent-install)
```

**BOTH PINNED COMMITS EQUAL openxFactory's OWN GITLINK FOR THE SAME ROOT.** The
equality is not this packet's to keep: `scripts/verify-opendox-pin.py` and
`scripts/verify-openxdox-pin.py` hold each pin's `commit:` to its gitlink. What
this packet reads is the pin, the contract openxFactory wrote.

### D0.2 Every carrier the widened kind can reach, read at its pinned commit

The widened kind reaches a `pinned` row admitted by a `pin`, and nothing else.
The live inventory carries FOUR such rows. Each root's tree was read at the
commit its pin names:

```
$ gh api "repos/opensoft/openDox/contents/.gitmodules?ref=dc7aa08f…" -q .content | base64 -d
  [submodule "spec"]  path = spec  url = https://github.com/opensoft/openDox-spec.git
  [submodule "code"]  path = code  url = https://github.com/opensoft/openDox-code.git
$ gh api "repos/opensoft/openDox/git/trees/dc7aa08f…" -q '.tree[]|select(.type=="commit")'
  160000 d816cf06…  code        160000 8fe8c4c7…  spec

$ gh api "repos/opensoft/openXdox/contents/.gitmodules?ref=2f3f857d…" -q .content | base64 -d
  [submodule "spec"]  path = spec  url = https://github.com/opensoft/openXdox-spec.git
  [submodule "code"]  path = code  url = https://github.com/opensoft/openXdox-code.git
$ gh api "repos/opensoft/openXdox/git/trees/2f3f857d…" -q '.tree[]|select(.type=="commit")'
  160000 626f2c8d…  code        160000 f088b097…  spec

$ gh api "repos/opensoft/openXwallet/git/trees/f3eb929b…"    -> 0 gitlinks, no .gitmodules
$ gh api "repos/opensoft/openRepoShape/git/trees/e9c4827b…"  -> 0 gitlinks, no .gitmodules
```

**FOUR LEGS, AND NOTHING ELSE MOVES.** `openXwallet` and `openRepoShape` carry
no submodule at their pinned commits. `Fission-AI/OpenSpec` is the fifth
`pin`-admitted row and is `external`, which no carrier form reaches before or
after this change. `opensoft/openAvatar` and `opensoft/LedgerxWallet` are
`pinned` but admitted by no `pin`, so neither can carry. And one hop further
down there is nothing to reach either:

```
$ for leg in openDox-code@d816cf06 openDox-spec@8fe8c4c7 \
             openXdox-code@626f2c8d openXdox-spec@f088b097; do
    gh api "repos/opensoft/${leg%@*}/git/trees/${leg#*@}?recursive=1" \
      -q '[.tree[]|select(.type=="commit")]|length'; done
  0  0  0  0
```

**RE-MEASURED AFTER MAIN RE-PINNED `openXdox`.** `main` (`1edbb3dd`, #1157,
already on this branch by Round A's merge) moved `contracts/openxdox-pin.yaml`
`commit:` and openxFactory's own `openXdox` gitlink together from `2f3f857d`
to `069fe471`. Re-read at `069fe471`: the same two legs at the same URLs
(`openXdox-spec` unchanged at `f088b097`, `openXdox-code` now `e28930bf`), the
new code leg carries 0 gitlinks, and the pin again equals openxFactory's own
gitlink for the root; `openDox`, `openXwallet` and `openRepoShape` are
unmoved. So the conclusion above — four legs, one-hop reach empty, every pin
equal to its gitlink — holds at `main` as merged into this branch. `tasks.md`
§ 4.3 already owes the re-measure again at the realization head.

### D0.3 The refusal, reproduced

```
$ cp scripts/estate-repository-inventory.yaml <scratch>; cat >> <scratch> <<'ROW'
  - repository: opensoft/openDox-code
    name: openDox-code
    role: code leg of the openDox assembly root
    governance: pinned
    admitted_by:
      - kind: gitlink
        carrier: opensoft/openDox
ROW
$ python3 scripts/validate-estate-inventory.py . --inventory <scratch>
  estate inventory validation CANNOT RUN:
    - row 34 (opensoft/openDox-code) is admitted by a gitlink in
      `opensoft/openDox`, whose own row 13 declares `governance: pinned`. THE
      KIND SAYS GOVERNED and means it: a `pinned` repository is one this estate
      consumes at a commit and digest and authors none of, and an `external`
      one is not of this estate at all, so neither performs an ACT OF
      ADMISSION when its `.gitmodules` happens to name something. Reading their
      submodule lists as admissions would let a tree nobody here writes decide
      who is in the estate
  exit 2
```

The refusal is `scripts/estate_inventory.py` line 966 and it refuses the WHOLE
FILE, not the row. D2 answers its reason.

### D0.4 Existence checked once, at the measurement and never at the gate

```
$ for r in opensoft/openDox-spec opensoft/openDox-code \
           opensoft/openXdox-spec opensoft/openXdox-code; do gh api repos/$r; done
  all four -> exists (public), default branch main
```

### D0.5 The declared population

```
$ python3 scripts/validate-code-surface.py .
  at 1d14fee6:    45 active proposals; membership: 30 readable heads naming
                  8 distinct identifiers — 8 carried, 0 refused
  at this branch: 46 active proposals; membership: 31 readable heads naming
                  8 distinct identifiers — 8 carried, 0 refused
```

The one extra head at this branch is THIS packet's own, `openxFactory`, already
carried. The eight identifiers include `opensoft/openDox` and `opensoft/openXdox`,
which #1144's head names as stand-ins for the legs; no active head names a leg,
so the realization refuses nothing and admits nothing new in the declared
corpus on the day it lands.

### D0.6 The one new hazard the shape brings, measured

Every read the inventory reader makes today is a file read or a git CONFIG read
(`remote get-url`, `rev-parse`), which never needs an object's content. The
pinned-commit read of D5 reads a BLOB out of an object store, and a partial
clone does not have every blob. Measured on git 2.43.0 (the Ubuntu package
`1:2.43.0-1ubuntu7.3` build) against a local `--filter=blob:none` clone whose
pinned commit's `.gitmodules` blob was absent:

```
$ GIT_ALLOW_PROTOCOL=none git show <pinned>:.gitmodules
  fatal: transport 'file' not allowed
  fatal: could not fetch c948daad… from promisor remote          exit 128
  (the blob is still absent afterwards)

$ git show <pinned>:.gitmodules
  [submodule "code"] …                                            exit 0
  (the blob is now PRESENT: the read fetched it from the promisor remote)

# a second clone, its own config set to allow every transport:
$ git config protocol.allow always; git config protocol.file.allow always
$ GIT_ALLOW_PROTOCOL=none git show <pinned>:.gitmodules
  fatal: transport 'file' not allowed                             exit 128
$ GIT_NO_LAZY_FETCH=1 git show <pinned>:.gitmodules
  warning: lazy fetching disabled; some objects may not be available
  fatal: could not fetch c948daad… from promisor remote           exit 128
  (the blob stays absent on THIS build: GIT_NO_LAZY_FETCH=1 also refused the
  fetch here, but it is a BUILD-DEPENDENT extra, not asserted of every git —
  GIT_ALLOW_PROTOCOL=none above, refused on both clones, is the guard relied on)
```

**AN UNGUARDED READ REACHES THE NETWORK ON A PARTIAL CLONE.** The requirement's
"no network call" is therefore not free under (a): it is an obligation D5 puts
on the realization, with its test.

## D1. The shape — RULED (a)

**RULED by Brett Heap (openxFactory repository owner), 2026-09-24, approximately
16:52Z, verbatim *"(a) recommended for both, ratify when the draft is green"*,**
given in the lane's terminal to lane `openxfactory-5` (session `d7c51922`)
BEFORE this pull request existed, and recorded as a `RULED` entry against
`opensoft/openxFactory#1150` in `opensoft/brett-wip` `lanes/log/openXfactory-5.md`
at commit `536b7ecf`. The word names option (a) for this decision; its second
clause is a ratification conditional on this draft's head being green, and is
recorded in `tasks.md` § 1, not here. The three options below are the ones #1150
put, each costed as it was costed before the word, so a later reader can see
what was chosen against what.

### D1.1 (a) — RULED: a `gitlink` whose carrier may be a pin-admitted `pinned` root

A `gitlink` row's carrier may be a `pinned` row PROVIDED that row is itself
admitted by exactly one `pin`: openxFactory pins the root by commit and digest,
and the root's `.gitmodules` AT THAT COMMIT is the evidence of reach. The leg is
NOT pinned by openxFactory and is not mounted by it, so the carving change's
task 5.1 — "`openxFactory` never pins or mounts a leg, which is the assembly
root's own job" — holds, as does the one-chain rule #1150 cites as RULING OQ-2.

- **What it costs.** One sentence in the `gitlink` bullet and two paragraphs;
  one load-time bound widened and one added; one read path in the
  `--estate-tree` mode; four rows. No kind, no class and no resolution rule
  moves, and the membership arm is untouched.
- **What it buys.** The closed set stays five, because the act that names a leg
  IS a gitlink. What differs is who carries it, and the inventory already
  records the carrier's class on the carrier's own row.

### D1.2 (b) — a sixth admission kind for a leg of a pinned root

`admitted_by: - kind: leg, root: opensoft/openDox`, say.

- **It re-states in the admitted row a fact the carrier's row already
  carries.** A `leg` differs from a `gitlink` only by the class of the carrier,
  and the carrier's `governance:` column already says it. Two statements of one
  fact can disagree — a `leg` whose root is `governed`, a `gitlink` whose
  carrier is `pinned` — and each disagreement owes a load-time refusal of its
  own.
- **It owes the same pinned-commit read under a second name.** Its evidence is a
  `.gitmodules` entry in another repository's tree, so it needs the carrier
  verification, the pinned-commit read and the NOT RE-CHECKED bound of D5
  exactly as (a) does, in a second branch of the validator.
- **It reopens the closed set for an act that is not new.** The set is closed
  "because they are exactly the ways this estate has ever named a repository",
  and the root names its leg by a gitlink. `ADMISSION_KINDS`, every report
  string that enumerates the kinds, the inventory header, the live-kinds test
  and the requirement's "exactly these five" all move.
- **The estate has declined a sixth kind once already**, for row 3 on
  2026-09-21 ("Drop the pin admission on row 3"), because an existing kind
  sufficed. The ground here is the same.
- **What (b) would buy.** A reader of the leg's row would see at a glance that
  its reach runs through a pin. (a) buys the same by the one-hop bound: a
  `gitlink` whose carrier is `pinned` can only be a root's leg.

### D1.3 (c) — REJECTED: `run:` `git submodule update` lines as workflow evidence

openxFactory's workflows reach the legs only in `run:` lines —
`pytest-suite.yml:425` (`git submodule update --init --recursive openXdox
openDox`) and `openxdox-consumer-gate.yml:239` — and (c) would read them.

- **It reverses a rule the reader states on purpose.**
  `_workflow_names_repository` reads three structural sites "and no fourth",
  because "every OTHER string in the document — a comment, a `run:` script line,
  an `echo`, an `::error::` message — is prose ABOUT the repository and not the
  workflow's own claim to dispatch into it"; `merge-master-approval.yml` names
  `codeXfactory/codexFactory` in exactly that prose form more than a dozen
  times.
- **It makes shell text an admission.** A `run:` block is a shell program;
  deciding what it initializes means reading variables, loops and quoting, or
  matching text — the substring defect the pin and workflow readers were
  hardened against in #1119's review.
- **And it does not even avoid the root's tree.** The line names a PATH
  (`openDox`, `--recursive`), not an address. Turning it into `opensoft/openDox-code`
  needs the root's `.gitmodules`, which is (a)'s evidence, read without (a)'s
  commit binding.

## D2. Why the pinned-commit binding is what makes (a) sound

The loader's refusal (D0.3) is a real argument and it is answered, not
outvoted: a `pinned` repository "is one this estate consumes at a commit and
digest and authors none of … so [it performs no] ACT OF ADMISSION when its
`.gitmodules` happens to name something. Reading their submodule lists as
admissions would let a tree nobody here writes decide who is in the estate."

**Under (a) the act of admission is NOT the root's.** It is openxFactory's pin:
a file under `contracts/` that openxFactory wrote, fixing the root at one
commit and one whole-tree digest. The root's `.gitmodules` is read AT THAT
COMMIT and at no other, so what decides membership is the tree openxFactory
CHOSE to consume, and a change to the root's `.gitmodules` on the root's own
main line changes nothing in the estate until openxFactory re-pins. The digest
already covers it: `sorted-ls-tree-r-v1` records each nested gitlink as
`160000 commit <oid>`, which is what `contracts/opendox-pin.yaml` says lets "this
ONE digest cover a three-repository product without mounting the other two".

**WITHOUT THE BINDING, THE LOADER'S SENTENCE WOULD BE TRUE OF (a).** Read at the
supplied tree's working files, or at whatever the tree has checked out, the
root's current `.gitmodules` would decide membership and a tree nobody here
writes would indeed decide who is in the estate. That is why the binding is in
the requirement text and not left to the realization.

**AND THE GOVERNED CARRIER STAYS AS IT IS**, read from its working tree: openxFactory
consumes no governed carrier at a commit, so there is no revision to bind it to
(D9).

## D3. The carrier bound: pinned, one pin, one hop

Part of (a) and not put separately; each clause is the narrowest that keeps D2
true.

- **`pinned`, never `external`.** An `external` repository is "NOT of this
  estate at all", so its `.gitmodules` admits nothing whatever openxFactory pins
  of it. `Fission-AI/OpenSpec` is pin-admitted and stays unable to carry.
- **Admitted by EXACTLY ONE `pin`.** The commit that pin names is the revision
  the evidence is read at; two pins would make it a pick, and picking is how an
  authorization lands in the wrong repository. *Alternative:* read at every
  pinned commit and require the leg at each. *Cost:* two pins of one product is
  the defect `neutral-product-pin`'s chain clause exists to end, and no row
  carries two today. Declined.
- **ONE HOP, CHECKED DIRECTLY.** A row this shape's `gitlink` admits carries no
  further `gitlink` of its own: the load refuses it AS A CARRIER in its own
  right, whether or not that row also carries a `pin`, so the reach ends one
  hop from an openxFactory pin without leaning on the pin-count bound above.
  *Alternative:* follow the chain. *Cost:* membership would rest on a walk of
  trees no openxFactory file names; and D0.2 measures the walk at zero
  repositories today. Declined.
- **A REFUSAL, NOT A REPORT, outside these conditions** — the same verdict the
  loader already gives a carrier no row names or a non-governed carrier today.

## D4. The leg's governance class: PUT FOR A VETO

**RECOMMENDED: a row a pinned root's gitlink admits SHALL NOT declare
`governance: governed`.** openxFactory reaches the leg only through its pin of
the root, at the commit that pin fixes — which fixes the leg's own commit, a
commit content-addressing its tree — and authors none of it. That is what a
`pin`-admitted row is too, and the loader already refuses a `governed` row
admitted by a `pin` (#1119 round 6, generalizing Brett Heap's "Drop the pin
admission on row 3"). All four legs are `opensoft`-owned and carved from this
repository, so all four are `pinned`.

**ALTERNATIVE: leave the class to the author.** *Cost:* a leg could be written
`governed`, claiming the estate authors directly a repository whose only
admission is openxFactory's consumption of a pinned root — the collapse the
predecessor's D4 refused, readmitted at a new door. Declined.

**ALTERNATIVE: require exactly `pinned`.** *Cost:* a root that nests a
third-party repository would force that repository into the estate's own
class, where `external` is the class that says "known, pinned, not ours".
Declined; the bound leaves `pinned` and `external` open and refuses only
`governed`, exactly as the `pin` bound does.

## D5. The re-check mechanics, and what they owe

The explicitly invoked mode is kept, and so is the carrier verification. Only
what is read after it changes, and only for a pinned carrier.

1. **VERIFY, UNCHANGED.** `carrier_identity` binds the supplied tree to the
   carrier by its own origin URL or the transfer map, exactly as for a governed
   carrier (ruling "Bind the carrier identity").
2. **READ THE PINNED COMMIT FROM THIS CHECKOUT.** The carrier row's one `pin`
   admission names a file under `contracts/`; its `commit:` is read through the
   strict loader, and a pin whose `revision_kind` is not `commit` or whose
   `commit` is not 40 hex names no revision — the shape
   `scripts/verify-opendox-pin.py::_pinned_commit` refuses as
   `opendox-pin-tag-only` — so the row is NOT RE-CHECKED, naming the pin.
3. **READ `.gitmodules` AT THAT COMMIT, FROM THE TREE'S OWN OBJECT STORE.**
   `git -C <tree> show <commit>:.gitmodules`, through the module's existing
   sanitized, time-bounded `_git`. The estate already reads a pin this way:
   `scripts/verify-opendox-pin.py::_openxdox_derived_commit` reads openXdox's
   own pin "as a git BLOB … AT THE COMMIT THE `openXdox` GITLINK RECORDS — never
   the openXdox working tree". The URLs are normalized by the same
   `_GITMODULES_URL_RE` and `normalize_origin` a working-tree `.gitmodules` goes
   through, so a leg's `https://` URL and a carrier's `git@` origin are read by
   one rule.
4. **REFUSE EVERY TRANSPORT FOR THAT READ (D0.6).** The environment the read
   runs in sets `GIT_ALLOW_PROTOCOL` to a value naming no protocol — THIS IS
   THE GUARD RELIED ON, measured (D0.6, the git 2.43.0 build there) to refuse
   every transport even where the repository's own config allows them all.
   `GIT_NO_LAZY_FETCH=1` may be set beside it; D0.6 measured it to ALSO refuse
   the fetch on that build, but whether it does is BUILD-DEPENDENT, so it is
   not what this design relies on. A tree whose store lacks the blob then
   answers "cannot produce", and the row is NOT RE-CHECKED, never fetched.
   **The realization's test is the D0.6 transcript**: a local `blob:none`
   clone, the read refused, the blob still absent.
5. **VERDICTS.** Carried: NAMED. Not carried by a verified tree at the pinned
   commit: a finding (exit 1), exactly as a governed carrier's absence is. Pin
   naming no commit, commit or blob not producible locally: NOT RE-CHECKED and
   COUNTED, naming the pin and the commit.

**THE NATURAL SUPPLIED TREE IS ALREADY IN openxFactory's OWN CHECKOUT.**
`git submodule update --init openDox` materializes a tree whose origin is
`opensoft/openDox` and whose object store holds the gitlink's commit, which
equals the pinned commit (D0.1). So `--estate-tree opensoft/openDox=openDox`
re-checks both openDox legs with no second clone. Wiring that into the
required check is D9's, not this packet's.

## D6. The delta kind: PUT FOR A VETO

**RECOMMENDED: one `## MODIFIED` block over *The estate's repositories are
enumerated in a governed inventory*, written over canon.** The `gitlink`
bullet's definition is what excludes the legs, so the definition has to move;
an ADDED requirement beside it would leave canon's bullet saying "a GOVERNED
ESTATE REPOSITORY's `.gitmodules`" while another requirement says otherwise.

- **CARRIAGE IS BYTE-FOR-BYTE, MEASURED.** The block was generated from canon's
  own bytes with every splice asserted, and a line diff of canon's block
  against it shows ONE canon line re-wrapped — where the new sentence enters
  the `gitlink` bullet — and every other canon line carried verbatim. All
  eight canon scenario titles and every one of their bullets are carried.
- **THE ONE REPLACED UNIT IS DECLARED.** `modified-block-currency` reads a body
  bullet as ONE unit, so adding a sentence to the bullet leaves canon's bullet
  uncarried; the block names it in a `**Removed from canon by
  admit-code-leg-under-pinned-root (2026-09-24):**` marker, whose reason says
  every sentence of it is carried word for word. `tasks.md` § 2.8 records the
  family's verdict at this head.
- **THE MEMBERSHIP REQUIREMENT IS NOT MODIFIED.** A leg's row is a `pinned` row,
  and *A head names a repository the inventory carries* already passes
  `governed` or `pinned`. Its bound on where the evidence lives restates two NOT
  RE-CHECKED cases — no tree, or a tree that does not verify — and takes them
  "on the terms the enumeration requirement states", which is where the third
  case (a verified tree that cannot produce the pinned commit) is written. It
  lists cases that MUST be NOT RE-CHECKED and says nothing a third case would
  make false.

**ALTERNATIVE: modify the membership requirement too**, naming the third case in
its bound sentence and in *An inventory row nothing names*. *Cost:* 108 lines
restated byte-for-byte to add a clause its own deferral already reaches, and a
second requirement key to keep current while this packet waits. *If Brett Heap
takes this alternative, the membership block is added and nothing else in the
packet changes.*

## D7. The rows the realization owes

**FOUR, NOT TWO.** The scenario *A code leg is nested under a pinned assembly
root* says the inventory SHALL carry a row for a leg the pinned root's
`.gitmodules` names, and at the pinned commits both roots name a `spec` leg as
well as a `code` leg. Writing two would leave two repositories a naming site
names with no row, which the enumeration requirement forbids in the same
sentence that admits the code legs.

| # | `<owner>/<name>` | role in the layer model | gov | admitted_by |
| ---: | --- | --- | --- | --- |
| 34 | `opensoft/openDox-spec` | spec leg of the openDox assembly root | pinned | gitlink (`opensoft/openDox`) |
| 35 | `opensoft/openDox-code` | code leg of the openDox assembly root | pinned | gitlink (`opensoft/openDox`) |
| 36 | `opensoft/openXdox-spec` | spec leg of the openXdox assembly root | pinned | gitlink (`opensoft/openXdox`) |
| 37 | `opensoft/openXdox-code` | code leg of the openXdox assembly root | pinned | gitlink (`opensoft/openXdox`) |

After them: **37 rows — 26 governed, 10 pinned, 1 external; 1 provisional; 34
`gitlink` rows**, the four new ones NOT RE-CHECKED on a default run like every
other, and re-checked at their pinned commits when the two root trees are
supplied. Bare names stay unique (`openDox-spec` and `openDox-code` collide with
nothing, `MedxEHR-spec` and `MedxEHR-code` being different names). The file
grows by about one kilobyte against a 19,037-byte file and a 65,536-byte
strict-loader ceiling. `tasks.md` § 4.3 re-measures all of it at the
realization head.

## D8. Sequencing, and the sibling search

**`sequenced_after: []`, a corroborated root claim.** No active change writes
`(release-realization, The estate's repositories are enumerated in a governed
inventory)` or the membership key beside it:

```
$ grep -rln "Requirement: The estate's repositories are enumerated in a governed inventory\|Requirement: A declared repository is judged for membership" \
    openspec/changes --include=spec.md | grep -v /archive/
  (nothing but this packet's own delta)
```

Three active changes carry a `release-realization` delta —
`add-sequenced-after-substrate`, `add-structured-scope-substrate` and
`add-target-release-deferred-allocation` — each over a different key.

**The sibling search**, 2026-09-24, before authoring: `ls openspec/changes
openspec/changes/archive | grep -i 'code-leg\|pinned-root\|admit-code'` returns
nothing, so `admit-code-leg-under-pinned-root` collides with no change id;
`ideation/staging/` names no topic about the inventory, a code leg or a pinned
root; and the claim's three reads on #1150 found no other claim, no branch and
one related pull request, #1144, which is the declaring packet and not a
sibling.

## D9. What is measured and deliberately not taken

Carried to `tasks.md` § 6 with its measurement, not restated here.
