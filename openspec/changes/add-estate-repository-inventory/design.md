# Design: add-estate-repository-inventory

Status: draft

For: openxFactory [#1087](https://github.com/opensoft/openxFactory/issues/1087)
Lane: openxfactory-5 (openXfactory-5)

**WHAT THIS DOCUMENT IS.** D0 is the measurement, taken before any decision, with
the commands so it reproduces. D1 through D5 are the decisions; D2, D3, D4 and D5
are put for a veto at `proposal.md` § *The decision, put for a veto*, each with
the recommendation first and the alternatives retained with their costs. D6 is
the sibling search. D7 is what is measured and deliberately not taken.

## D0. The measurement, taken before the design

Taken on a fresh clone of `opensoft/openxFactory` at `origin/main` `ad089e8a`.

### D0.1 The five naming sites, and the commands

**THE FIFTH SITE WAS ADDED IN REVIEW AND THE REASON IS RECORDED RATHER THAN
SMOOTHED OVER.** A first filing of this packet enumerated FOUR sites, all of
them in the aggregation or in this repository, and read `gitlink` as the
AGGREGATION's `.gitmodules` alone. Copilot's review of PR #1101 showed that
reading refuses to discharge its own provisional row (D1.1), because the estate
also NESTS a repository inside a governed DomainxFactory. The site was widened
and the measurement RE-TAKEN on 2026-09-18 rather than reasoned about; the six
rows it adds are rows 28-33 and they are disclosed at D0.2 as what the narrow
reading missed.

```
$ gh api repos/opensoft/xFactory/contents/.gitmodules -q .content | base64 -d \
    | grep -oP 'github\.com[:/]\K[^ ]+' | sed 's/\.git$//' | sort
  -> 23 submodule addresses

$ for r in <the 19 governed non-root rows of D0.2>; do \
    gh api repos/$r/contents/.gitmodules -q .content 2>/dev/null | base64 -d \
      | grep -oP 'github\.com[:/]\K[^ ]+' | sed 's/\.git$//'; done | sort -u
  -> 11 nested gitlinks in SIX governed repositories (openxFactory 4,
     MedxEHR 2, LedgerxFactory 2, MedxFactory 1, MedxChart 1, MedxPractice 1),
     naming SEVEN repositories no other site names: openChart, openPractice,
     MedxAvatar, LedgerxAvatar, MedxEHR-spec, MedxEHR-code and LedgerxWallet.
     openxFactory's own four (Omnigent-Install, openXwallet, openXdox, openDox)
     are already aggregation submodules.

$ grep -rn 'source_repository\|^repository:' contracts/*.yaml
  -> 7 pin declarations naming 6 distinct repositories

$ grep -rhoP 'uses:\s*\K[A-Za-z0-9._-]+/[A-Za-z0-9._-]+' .github/workflows/ | sort -u
$ grep -rn 'codeXfactory/codexFactory' .github/workflows/
  -> 1 estate repository dispatched at a named ref (already a submodule)

$ python3 scripts/validate-code-surface.py .
  code_surface: 49 active proposals, 49 declaring — 7 `none`, 34 a repository
  list, 8 named by the register, 0 outside the grammar.
    archive (read, never judged): 170 proposals, 124 declaring, 3 outside.
```

**THE FIGURES ABOVE ARE THE CORPUS THIS PACKET WAS MEASURED AGAINST AND NOT THE
CORPUS AT THIS BRANCH'S HEAD, and the difference is disclosed rather than left to
a reader to notice.** They are taken at `origin/main` `ad089e8a`, BEFORE this
packet was filed. Run at this branch's head the same command reports **50** active
proposals and **35** readable repository lists, the extra one being THIS PACKET'S
OWN declaration, whose head is the single identifier `openxFactory` and which the
candidate inventory carries at row 2. Nothing else moved, and no figure this
design reasons from changes.

The declared identifier census was taken through the SHIPPED reader
(`scripts/code_surface.py`, `declaration` then `parse_head`) over every active
`proposal.md`, never by a private scan, so this count and the gate's count cannot
diverge.

### D0.2 THE CANDIDATE INVENTORY: 33 rows, measured

`governance`: `governed` the estate authors its contents, `pinned` openxFactory
consumes it at a commit and digest, `external` pinned and not of this estate.
`admitted_by`, in the FIVE kinds the delta closes: `gitlink` a GOVERNED ESTATE
REPOSITORY's `.gitmodules` carries the submodule and the evidence NAMES the
repository that carries it (the aggregation in the wide case, a governed
DomainxFactory where the estate nested rather than sibling-linked); `pin` a
`contracts/` pin file; `workflow` an openxFactory workflow; `root` the
aggregation itself; `change` a ratified change whose realization creates it
(PROVISIONAL until another kind names it, D1.1). The kinds are spelled here
exactly as D1.1, D4 and the delta spell them.

| # | `<owner>/<name>` | role in the layer model | gov | admitted_by |
| ---: | --- | --- | --- | --- |
| 1 | `opensoft/xFactory` | aggregation root; owns workspace assembly and pins only | governed | root |
| 2 | `opensoft/openxFactory` | canonical domain-neutral contract repository | governed | gitlink |
| 3 | `codeXfactory/codexFactory` | DomainxFactory, engineering | governed | gitlink (`opensoft/xFactory`), pin (`review-lane-pin.yaml`), workflow |
| 4 | `MedxSoft/MedxFactory` | DomainxFactory, medical | governed | gitlink |
| 5 | `ledgerXfactory/LedgerxFactory` | DomainxFactory, accounting | governed | gitlink |
| 6 | `opensoft/OpsxFactory` | DomainxFactory, IT operations | governed | gitlink |
| 7 | `opensoft/AdxFactory` | DomainxFactory, marketing | governed | gitlink |
| 8 | `opensoft/MedxChart` | Medx composition boundary | governed | gitlink |
| 9 | `opensoft/MedxPractice` | Medx practice-operations boundary | governed | gitlink |
| 10 | `MedxSoft/MedxEHR` | Medx satellite | governed | gitlink |
| 11 | `opensoft/HealthLinc` | Medx satellite | governed | gitlink |
| 12 | `opensoft/openXwallet` | neutral product, wallet standard | pinned | gitlink, pin (`openxwallet-pin.yaml`) |
| 13 | `opensoft/openDox` | neutral product, document layer | pinned | gitlink, pin (`opendox-pin.yaml`) |
| 14 | `opensoft/openXdox` | neutral product, document layer | pinned | gitlink, pin (`openxdox-pin.yaml`) |
| 15 | `opensoft/openAvatar` | neutral product, avatar client | pinned | gitlink |
| 16 | `opensoft/openRepoShape` | neutral product, repository shape | pinned | pin (`openreposhape-pin.yaml`) ONLY |
| 17 | `opensoft/AgentTower` | install, AgentTower runtime | governed | gitlink |
| 18 | `opensoft/xFactory-Hermes-Install` | install, three-layer Hermes | governed | gitlink |
| 19 | `opensoft/Omnigent-Install` | install, Omnigent | governed | gitlink |
| 20 | `opensoft/OmniWorker-Install` | install, OmniWorker | governed | gitlink |
| 21 | `opensoft/CloudPC-Install` | install, CloudPC | governed | gitlink |
| 22 | `opensoft/xFactory-Installer` | install, workspace installer | governed | gitlink |
| 23 | `opensoft/xFactory-MedxRootTruth-Install` | install, Medx root truth | governed | gitlink |
| 24 | `opensoft/Keycloak-Install` | install, Keycloak | governed | gitlink |
| 25 | `opensoft/OpenXPKI-Install` | install, OpenXPKI | governed | gitlink |
| 26 | `Fission-AI/OpenSpec` | third-party CLI, pinned by `openspec-cli-pin.yaml` | external | pin ONLY |
| 27 | `opensoft/LedgerxWallet` | neutral product, Ledgerx wallet overlay, nested in LedgerxFactory | pinned | gitlink (`ledgerXfactory/LedgerxFactory`), change (`create-ledgerxwallet-overlay-boundary`, ratified) |
| 28 | `opensoft/openChart` | nested submodule of `MedxChart`, the Medx composition boundary | governed | gitlink (`opensoft/MedxChart`) |
| 29 | `opensoft/openPractice` | nested submodule of `MedxPractice`, the practice-operations boundary | governed | gitlink (`opensoft/MedxPractice`) |
| 30 | `opensoft/MedxAvatar` | nested submodule of `MedxSoft/MedxFactory` | governed | gitlink (`MedxSoft/MedxFactory`) |
| 31 | `opensoft/LedgerxAvatar` | nested submodule of `ledgerXfactory/LedgerxFactory` | governed | gitlink (`ledgerXfactory/LedgerxFactory`) |
| 32 | `MedxSoft/MedxEHR-spec` | nested submodule of `MedxSoft/MedxEHR` | governed | gitlink (`MedxSoft/MedxEHR`) |
| 33 | `MedxSoft/MedxEHR-code` | nested submodule of `MedxSoft/MedxEHR` | governed | gitlink (`MedxSoft/MedxEHR`) |

Row 16 and row 26 are rows a `.gitmodules`-only derivation would miss; row 1 is
the row no `.gitmodules` can ever carry; row 26 is the row a flat membership list
could not refuse a surface in; **row 27 is the row that forced the fifth
admission kind** (D1.1); and **rows 28-33 are the SIX rows the narrow reading of
`gitlink` missed**, measured on 2026-09-18 by the second command of D0.1 after
the review widened the kind. Each is a real submodule of a governed estate
repository and each is named by NO aggregation gitlink, NO openxFactory pin and
NO openxFactory workflow, which is exactly why a `gitlink` read as the
aggregation's alone left them admitted by nothing.

*The governance class of rows 28-33 is stated as the four openxFactory sites
measure it and NOT further.* None of the six is named by any openxFactory
`contracts/*-pin.yaml` (checked: the pin corpus names `opensoft/openXdox`,
`opensoft/openDox`, `Fission-AI/OpenSpec`, `opensoft/openRepoShape`,
`codeXfactory/codexFactory` and `opensoft/openXwallet` and nothing else), so
none is `pinned` in this repository's sense, and none is third-party, so none is
`external`. Whether the NESTING repository pins rather than authors any of them
is a fact in that repository's tree and not in any of the five sites; `tasks.md`
§ 4.3 re-measures the rows at the realization head and discloses any that moved.

### D0.3 The declared population, against that candidate

The 34 readable heads name SIX distinct identifiers, and each is checked against
the candidate:

| identifier as declared | resolves to | how |
| --- | --- | --- |
| `openxFactory` (30 heads) | row 2 | bare name |
| `xFactory` | row 1 | bare name |
| `openAvatar` | row 15 | bare name |
| `opensoft/LedgerxWallet` | row 27 | address; the case that forced the fifth kind (D1.1) |
| `opensoft/Keycloak-Install` | row 24 | address |
| `opensoft/OpenXPKI-Install` | row 25 | address |

**ALL SIX RESOLVE, AND THE SIXTH IS THE ROW THE FIRST FOUR SITES COULD NOT
REACH.** `opensoft/LedgerxWallet` is a REAL repository (D0.4) that the first four
naming sites do NOT name: no AGGREGATION gitlink (measured 2026-09-18 — the
aggregation's `.gitmodules` carries `openXwallet` and no `LedgerxWallet`), no
openxFactory pin, no openxFactory workflow. TWO THINGS NAME IT, and the packet
states both rather than the one that suited its first draft:

- the RATIFIED active change `create-ledgerxwallet-overlay-boundary`, whose own
  declaration reads `opensoft/LedgerxWallet (new), …` and whose realization
  CREATES it; and
- the FIFTH SITE, `ledgerXfactory/LedgerxFactory`'s `.gitmodules`, which has
  carried `[submodule "LedgerxWallet"]` since 2026-08-28 (that packet's
  `tasks.md` § 5.1, LedgerxFactory PR #31, commit `2c96b0b`) — verified live on
  2026-09-18, not read from the packet's own tick.

**A CODE SURFACE IS FORWARD-LOOKING, it names where a change WILL write, so a
repository the estate is CREATING is declared before any site can name it.**
That window is the measured origin of the fifth admission kind (D1.1), and the
window on THIS case is measured at ONE DAY: declared 2026-08-27, nested
2026-08-28. The kind is what keeps the membership arm from refusing a ratified
packet inside such a window; the nested gitlink is what DISCHARGES the row
afterwards, and D1.1 records that a kind with no discharge would have been a
defect rather than a mechanism.

It is also the measurement that decides D1: an inventory derived from the
AGGREGATION's `.gitmodules` alone would carry twenty-three rows, would miss ten
of the thirty-three, and would refuse a lawful declaration on its first day.

### D0.4 Existence checked once, at the measurement and never at the gate

```
$ for r in opensoft/LedgerxWallet opensoft/xFactory opensoft/openRepoShape \
           Fission-AI/OpenSpec opensoft/LegalxFactory; do gh api repos/$r; done
  opensoft/LedgerxWallet   -> exists (private)
  opensoft/xFactory        -> exists (private)
  opensoft/openRepoShape   -> exists (public)
  Fission-AI/OpenSpec      -> exists (public)
  opensoft/LegalxFactory   -> 404 Not Found
```

The gate never makes this call (D4). It was made here to establish two facts: that
the six declared identifiers name real repositories, and that the estate already
writes one that does not.

### D0.5 THE DIVERGENCES THE CANDIDATE SURFACES, which are the defect standing today

`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` is the file
`gate-code-surface-declarations` D1 called "a five-row domain-factory regression
fixture". It has six rows now, and three of them diverge:

| the fixture writes | the provider answers | the candidate carries |
| --- | --- | --- |
| `opensoft/LegalxFactory` | **404** | no row; no gitlink, no pin, no workflow |
| `opensoft/LedgerxFactory` | redirect -> `ledgerXfactory/LedgerxFactory` | row 5, at the current address |
| `opensoft/MedxFactory` | redirect -> `MedxSoft/MedxFactory` | row 4, at the current address |

And `contracts/policies/repository-identity.yaml`, the estate's transfer map,
carries **ONE** row (`opensoft/codexFactory` -> `codeXfactory/codexFactory`). The
Medx and Ledger transfers are NOT in it; the Medx half is what the ACTIVE draft
`adopt-medxsoft-repository-identity` owes. So a former address in the corpus today
resolves through the map for one repository and through a provider redirect for
two more, and that file's own header says a redirect "is a grace period, not an
identity".

`opensoft/LegalxFactory` is the § 6.1 class, standing, in a contract member.

### D0.6 The churn rate, which decides D2

```
$ gh api "repos/opensoft/xFactory/commits?path=.gitmodules&per_page=100" \
    -q '.[] | .commit.committer.date[0:10]' | sort | uniq -c
  19 commits, 2026-07-01 .. 2026-09-12 (74 days)
```

Reading their subjects: "Add installs/omniworker-install as a sibling submodule",
"Admit Keycloak-Install + OpenXPKI-Install submodules", "Repoint the Medx
submodules at MedxSoft", "Repoint the LedgerxFactory submodule at ledgerXfactory",
"Replace openChart aggregate with MedxChart", "Add MedxPractice composition
boundary", "Pin openAvatar at the neutral root". **Nineteen of nineteen move an
inventory row**, at one every four days.

## D1. A FILE, not a derivation

**RECOMMENDED: a committed enumeration whose rows carry evidence.**

The alternative is to derive membership live: read the aggregation's
`.gitmodules` on every run and treat it as the estate. D0.3 measures it false —
`opensoft/LedgerxWallet` is declared by an active packet, is a real repository,
and is in NO AGGREGATION `.gitmodules`, so a derived gate would refuse a lawful
declaration on its first day, which is exactly the trap D1 of the predecessor
named. That one site reaches 23 of the 33 rows. It misses two the pins reach
(`openRepoShape`, `Fission-AI/OpenSpec`), SEVEN the nested gitlinks reach (rows
27-33, none of them an aggregation submodule), and one it cannot reach in
principle (the aggregation root, which is not its own submodule).

And the derived shape has a second cost that has nothing to do with completeness:
it makes a REQUIRED CHECK depend on a network call to a PRIVATE repository. The
aggregation repository is private (D0.4). A gate whose verdict depends on a token
and an afternoon gives a different answer than it gave at the ratification.

### D1.1 THE FIFTH ADMISSION KIND, which the measurement forced

The four sites a first draft of this design named (`gitlink`, `pin`, `workflow`,
`root`) are the four ways a repository that ALREADY EXISTS is named. D0.3 found
a fifth case they do not cover and that a gate would refuse on its first day:
`opensoft/LedgerxWallet`, declared by the RATIFIED `create-ledgerxwallet-overlay-boundary`,
whose realization creates it. `admitted_by: change` carries it, the row is marked
PROVISIONAL, and the reverse arm reports a row still admitted only by an ARCHIVED
change, because once the realization has landed, a governed tree CAN name the
repository, and a provisional admission that outlives its change is the same
defect as a row whose evidence has gone.

**THE KIND IS NOT AN ESCAPE HATCH AND THE SHAPE IS WHAT KEEPS IT FROM BEING ONE.**
The evidence is a change id that must resolve under `openspec/changes/`, the
change must be RATIFIED (an author cannot admit a repository by drafting), and the
row expires into a finding at that change's archive.

**AND A KIND THAT EXPIRES OWES A DISCHARGE, WHICH THE FIRST FILING DID NOT
HAVE.** Copilot's review of PR #1101 named the hole exactly: the realization that
creates `opensoft/LedgerxWallet` NESTS it under `ledgerXfactory/LedgerxFactory`
(`tasks.md` § 5.1 of that packet, done 2026-08-28), not under the aggregation, so
with `gitlink` read as the AGGREGATION's `.gitmodules` alone the provisional row
would expire at that change's archive into a finding NO kind could close. A
requirement that mints a finding with no available remedy is the defect this
estate disposes of rather than creates. The fix is the narrowest one that closes
it and it is taken: **`gitlink` is a gitlink in ANY governed estate repository,
and the evidence names the repository that carries it.** The discharge is then
concrete and already measurable — the LedgerxFactory `.gitmodules` entry, live on
2026-09-18 — and rows 28-33 are the six further members that reading admits,
disclosed at D0.2 rather than left for the realization to discover.

*The cost of D1, stated plainly.* A committed file goes stale, and the estate
moves an inventory row every four days (D0.6). The second ADDED requirement
answers that cost rather than ignoring it: **an inventory row that no naming site
names is a FINDING**, so staleness is reported by the same run that judges
declarations.

### D1.2 WHERE THE REVERSE CHECK CAN ACTUALLY LOOK, which the widening forced

The reverse arm's claim is that staleness "is checkable in the tree without a
network call". Copilot's review showed that claim is true of FOUR kinds and false
of the fifth, and widening `gitlink` to the nested case makes the fifth worse
rather than better: `pin`, `workflow` and `change` name files under `contracts/`,
`.github/workflows/` and `openspec/changes/` — all in THIS checkout — and `root`
names no file at all, but a `gitlink` lives in a tree an openxFactory checkout
does not contain, and now in one of SIX such trees (`opensoft/xFactory`,
`MedxSoft/MedxFactory`, `ledgerXfactory/LedgerxFactory`, `opensoft/MedxChart`,
`opensoft/MedxPractice`, `MedxSoft/MedxEHR`) rather than in one.

**THE BOUND IS STATED INSTEAD OF BEING DISCOVERED BY WHOEVER BUILDS § 3.** The
default run re-checks the four in-tree kinds on every run, deterministically and
with no network call, and that is what the house validator and the membership arm
gate. A `gitlink` row is re-checked only in an EXPLICITLY INVOKED mode that takes
the carrying repository's working tree as a PATH INPUT, and a run given no such
path REPORTS those rows as NOT RE-CHECKED, with their count. Silence is never a
pass: a run that has not looked reports neither "named" nor "stale".

*Why not simply fetch the tree.* Because that is the cost D1 refused two
paragraphs above — a required check depending on a token and on read access to a
private repository — and a cost refused at the forward arm may not be readmitted
at the reverse one.

*The alternative, retained.* DROP the reverse check for `gitlink` rows entirely
and name it a successor. *Cost:* the widest kind, carrying 30 of the 33 rows
(every row but the aggregation root and the two `pin`-only members), would then
never be re-checked at all, and the staleness answer to D1's cost
would cover a minority of the file. Declined in favour of the bounded mode, which
costs one path argument and one counted line of output.

## D2. Where the inventory lives: PUT FOR A VETO

**RECOMMENDED: `scripts/estate-repository-inventory.yaml`**, beside
`scripts/code-surface-register.yaml`, read by `scripts/estate_inventory.py` and
by the arm added to `scripts/validate-code-surface.py`. `target_release:
implemented`.

The reason is the register's own, now with a measured rate behind it rather than
an assertion. That file's header states: "a file under `contracts/` is a bundle
surface whose change owes a bundle cut, and an exception register that could not
be edited without cutting a contract release would be edited late or not at all".
D0.6 measures the rate at which this file would need editing: nineteen
inventory-moving acts in seventy-four days.

**ALTERNATIVE: `contracts/policies/estate-repository-inventory.yaml`.** The
strongest argument for it is a real one and it is retained here in full: the
inventory is a CANONICAL STATEMENT ABOUT THE ESTATE, of the same subject matter
as `contracts/policies/repository-identity.yaml` one directory away, and CLAUDE.md
rule 1 has consumers pin the neutral contracts they consume, which only a
`contracts/` surface offers. *Cost:* a new `contracts/` member owes an entry in
`contracts/manifest.yaml` with a recomputed `sha256`, and
`docs/contract-versioning-policy.md` § Change Classes makes "new contracts" an
ADDITIVE (minor) class, so every correction to a fact that moves every four days
spends a bundle minor. `target_release:` would become "next additive contract
bundle (allocated at realization)", the shape `adopt-medxsoft-repository-identity`
carries. *If Brett Heap takes this alternative, `target_release:` moves with it
and the realization owes the manifest entry; nothing else in the packet changes.*

**ALTERNATIVE: no file (D1's derived shape).** Costed at D1.

## D3. `## MODIFIED` over the grammar requirement: PUT FOR A VETO

**RECOMMENDED: one `## MODIFIED` block over *Code-surface declaration grammar is
gated*, restated exactly as canon states it but for ONE paragraph.**

The promoted text is unconditional: "The gate SHALL judge the identifier's SHAPE
and SHALL NOT judge its MEMBERSHIP of any inventory". An ADDED-only delta would
put "membership SHALL be judged" into canon beside it, and canon would then carry
two requirements that cannot both be obeyed. `document-lifecycle` makes
`ideation/brainstorm/` the only place contradiction is legal.

**THE PARAGRAPH IS LIFTED BY REMOVING ITS REASON, WHICH IS THE ONLY HONEST WAY TO
LIFT IT.** The sentence states its own ground, "for the measured reason that
this repository defines no inventory of the estate's repositories to resolve
against", and adds a prediction, that a membership gate "would refuse every
declaration on the day it landed". The ground stops holding at this packet's
realization; the prediction is measured FALSE at D0.3, six of six resolving. The
restated paragraph says both, so a later reader can see what changed and why.

**THE DELETION IS DECLARED AND NOT LEFT TO BE INFERRED.** The three sentences the
replacement supersedes are named as code spans in a reserved
`**Removed from canon by add-estate-repository-inventory (2026-09-18):**` marker
carried inside the block, with the reason after the separator, in the form
`doc-health`'s promoted *Prose tagging marker hygiene* family defines. Without it
the `modified-block-currency` arm reports three carried-body-unit findings against
this block, which is the arm working: it cannot distinguish a deliberate rewording
from a drift and does not claim to. With the marker the arm reports NOTHING new,
measured by running the whole checker at this head and at a clean `origin/main`
checkout in the same clone: 97 findings at both, zero new, zero gone.

**THE SELF-GATE IS CLEAN AND WAS CHECKED RATHER THAN ASSUMED.** No other active
change writes `(release-realization, code-surface declaration grammar is gated)`
— the three code-surface titles have no active writer but this packet, checked by
`grep -rl "Requirement: <title>" openspec/changes/ --include=spec.md`. So this
block is SOLE, no `sequenced_after:` is owed on it, and
`scripts/doc-health.py --single-repo . --family modified-block-currency` reports
no NEW finding against it.

**ALTERNATIVE: ADDED-only, leaving the promoted `SHALL NOT` standing.** *Cost:* a
standing contradiction in canon, and a gate whose authority rests on a reader
preferring the newer requirement. Declined.

## D4. The authority question (who admits, and what a pinned row means): PUT FOR A VETO

#1087 carries the question the predecessor left open: "who admits a repository to
the estate, and what a row means for a repository that is pinned rather than
governed".

**RECOMMENDED, and it is two answers.**

*Who admits.* **NOBODY ADMITS A REPOSITORY BY WRITING A ROW.** A repository joins
the estate when a governed tree NAMES it (a submodule added to the aggregation or
nested under a governed DomainxFactory, an act with its own review; a pin filed
here; a workflow pointed at it; a ratified change whose realization creates it),
and the row RECORDS that act. `admitted_by:` names the site and the kind, so the
row is checkable against the tree rather than asserted, and the reverse arm
reports a row whose evidence has gone, on the bound D1.2 states.

**THE CLOSED SET IS FIVE KINDS — `gitlink`, `pin`, `workflow`, `root`, `change`
— AND IT IS SPELLED HERE EXACTLY AS D0.2, D1.1 AND THE DELTA SPELL IT.** They
are closed because they are exactly the ways this estate has named a repository
(D0.1, D0.2). `change` is the fifth and is not decoration: D1.1 measures the
case that forced it and D0.3 measures the window it covers, and a set of four
stated anywhere in this packet would put the delta and the design at odds over
the very mechanism the packet requires. `gitlink` is the widest of the five and
reaches ANY governed estate repository's `.gitmodules`, the evidence naming the
repository that carries it; read as the aggregation's alone it admits none of
rows 27-33 and leaves the `change` kind with no discharge (D1.1).

*What a pinned row means.* Three governance classes. `governed`, the estate
authors its contents. `pinned`, openxFactory consumes it at a commit and digest
and authors none of it. `external`, pinned and not of this estate at all
(`Fission-AI/OpenSpec`). The distinction is not decoration: a `code_surface:` is
the set of repositories whose runtime artifacts a change CHANGES, and a change
cannot change what the estate does not author, so an `external` head is REFUSED
and the refusal names the class.

**ALTERNATIVE: a flat membership list.** *Cost:* it cannot refuse a surface
declared in `Fission-AI/OpenSpec`, and it cannot tell a reader whether a row means
"we write this" or "we read this at a digest". Declined.

**THE RESOLUTION IS BY ROW AND NEVER BY PROVIDER**, and that is not put for a
veto because it follows from the transfer map's own ratified header: a redirect is
a grace period that stops the moment the former owner reuses the name. A gate
resting on a redirect rests on nobody creating a repository.

## D5. A former address in an active head: PUT FOR A VETO

**RECOMMENDED: REPORT, naming the current address.** The transfer map resolves it,
so the identifier is interpretable and membership is not in doubt; what is owed is
a respelling. The finding names the current address so the author need not look it
up.

**ALTERNATIVE: refuse.** *Cost:* it teaches an author nothing the finding does
not, and it would red a required check on a packet whose declaration everybody can
read. Declined.

**NEITHER DISPOSITION REACHES A GLOSS, AN ARCHIVED PACKET, OR A DIGEST-COVERED
BYTE.** The grammar's own ratified rule stands: the head is judged and the gloss
never is. `adopt-medxsoft-repository-identity` declares the head `openxFactory`
and names both former Medx addresses in its GLOSS, so it is untouched by D5, a
fact checked at D0.3 and not assumed.

## D6. Sequencing, and the sibling search

`sequenced_after: []`. The MODIFIED block takes its pre-text from CANON
(`openspec/specs/release-realization/spec.md`), not from another active change,
and no active change co-writes the requirement key (D3). The two ADDED titles were
checked against `openspec/specs/`, every active delta and the archive and appear
nowhere else.

The sibling search, taken 2026-09-18 before authoring: `ls openspec/changes` and
`ls openspec/changes/archive` for an inventory, estate-enumeration or repository-
membership change (`grep -Ei 'estate|invent|code-surface|repositor'`) returns
`add-xfactory-installer-repository`, `add-repository-lens`,
`add-release-inventory-drift-check`, `refresh-install-repository-enumerations`,
`adopt-codexfactory-repository-identity` and `gate-code-surface-declarations`, all
ARCHIVED and none enumerating the estate; and `adopt-medxsoft-repository-identity`,
ACTIVE and draft, which is a TRANSFER-MAP change and not an enumeration. No active
change proposes an inventory of the estate's repositories. `add-estate-repository-inventory`
collides with no active and no archived change id.

## D7. What is measured and deliberately not taken

Carried to `tasks.md` § 6 with its measurement, not restated here.
