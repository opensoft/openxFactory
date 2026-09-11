# Design: gate-realization-axis-vocabulary

Status: draft
Kind: design

**EVERY DECISION THIS AUTHORING SESSION TOOK IS HERE, WITH ITS ALTERNATIVE AND
THE ALTERNATIVE'S COST.** Brett Heap's word of 2026-09-11T12:08:24Z — verbatim
**"land each when green, archive both when landed, claim 955 and 956"** —
commissioned the authoring and took none of them. **D1, D2 and D3 are the
declared veto points.**

## 0. The brief

openxFactory [#956](https://github.com/opensoft/openxFactory/issues/956):
`target_release: none` is outside `release-realization`'s ratified two-value
vocabulary, the corpus carries it, and **no gate reports it** — *"Whichever is
taken, it wants a GATE, or the next proposal re-introduces the divergence: the
vocabulary is stated in prose and checked by nobody."* The issue names three
options and leaves the choice to a taker.

## D0 — the measurement, taken before the design

**NOTHING BELOW RESTS ON A NUMBER ANYBODY TYPED.** Every figure was re-taken on
a fresh clone at `origin/main` `38c076d1`, by the method the issue names so it
reproduces: a `^target_release:` / `^code_surface:` line at the start of a line
in every `openspec/changes/**/proposal.md`, archived packets included, the
VALUE TOKEN being the first whitespace-delimited word with trailing `.,;:`
stripped.

**THE ISSUE'S TABLE, RE-TAKEN:**

| measure | #956 at filing (`1d20edd4`) | re-measured (`38c076d1`) |
| --- | ---: | ---: |
| `proposal.md` files | 199 | **199** |
| declaring `target_release:` | 181 | **181** |
| declaring `none` | 33 | **32** |
| of those, ACTIVE | 6 | **5** |
| of those, archived | 27 | **27** |
| `code_surface: none` declarers | 20 | **20** — `implemented` 10, `none` 7, `promotion-only` 3 |

The two that moved are one fact: **`state-header-window-budget` archived at PR
#953** between the filing and this authoring, taking one `none` carrier out of
the active set and leaving the archived count where it was — which is itself the
issue's point about archived front matter being frozen record.

**THE MEASUREMENT THE ISSUE DID NOT TAKE, AND THE ONE THAT SHAPED THIS PACKET.**
`none` is not the divergence; it is one fifth of it. Of the **38 ACTIVE**
proposals — every one declares the field — only **12** declare a value the
ratified vocabulary admits:

| | active | changes |
| --- | ---: | --- |
| **inside**: `implemented` | **9** | add-sequenced-after-substrate, add-structured-scope-substrate, add-wallet-carried-review-authority, adopt-configured-notebook-hosting-identity, create-ledgerxwallet-overlay-boundary, disposition-codexfactory-declared-renames, disposition-codexfactory-floor-relocation-retitle, prepare-openspec-1-12-readiness, settle-aging-staging-topics |
| **inside**: a release this estate defines | **3** | add-doxchat-model-intake (`contract-v1.45`), retire-doxbench-chat-turn-v1 (`contract-v3.0`), retire-hermes-flat-keys-and-openworkflow-tokens (`contract-v3.0`) |
| outside: `none` | **5** | add-composed-view-authoring, add-cpc-clearing-boundary, add-lens-document-selection, add-substantive-review-lane, register-gate-rules-council-seats |
| outside: deferred allocation | **12** | add-chain-attestation, add-clearing-dispatch-boundary, add-consent-custody-rederivation-record, add-credential-escrow-checkout, add-requirement-ref-resolution-integrity, add-identity-brokering, add-standing-policy-compliance-contract, add-trust-anchor, add-worker-enrollment-broker, adopt-medxsoft-repository-identity, admit-deliberation-clearing-operation, declare-client-standing-policy-contract |
| outside: realization state | **4** | add-nightly-dashboard-refresh, add-roster-directory-admission-surface, qualify-avatar-live-voice, split-opendox-two-layer-product |
| outside: repository bootstrap | **2** | implement-keycloak-install-repo, implement-openxpki-install-repo |
| outside: answers another question | **3** | admit-review-lane-repin-to-merge-approval-envelope, amend-mirror-floor-regeneration-merge-authority, extend-merge-master-envelope-to-floor-bot-lanes |

**TWELVE OF THE TWENTY-SIX ARE OUTSIDE THE VOCABULARY BECAUSE ANOTHER RATIFIED
RULE PUTS THEM THERE.** `docs/contract-versioning-policy.md` § Bundle
Realization Order, first line: *"Contract-bundle realization is serialized and
allocates versions late"* — step 1 *"allocate the next available version"* at
rebase time, step 5 the tag after the land. Naming a number in a proposal
reserves one the policy allocates at the cut, and those twelve declarations say
so in their own words: *"DELIBERATELY NOT NUMBERED HERE"*, *"NO minor is
reserved here"*. The promoted two-value sentence has no spelling for *a
release, not yet numbered*.

**NO GATE READS THE VALUE, CONFIRMED BY THE COMMAND THE ISSUE NAMES.**
`grep -rn target_release scripts/ tests/ .github/` on `38c076d1` returns, in
`scripts/`, exactly four lines and all four in one module —
`scripts/ideation_dashboard/generator.py:410,416,571,576` (`_release_frontmatter`,
which reads the two headers for the dashboard snapshot) — plus
`scripts/ideation_dashboard/web/views/wheel.js:767-768`, which renders
`"target release: " + change.target_release` as a display line. Nothing else in
`scripts/`, nothing in `.github/`. In `tests/` it is fixture text only, in BOTH
spellings: `tests/ideation-dashboard/test_gate_console.py:381,390,1157` writes
`target_release: none`, while `tests/scope_globs/test_schema.py:50`,
`tests/scope_globs/test_strict_loader.py:54` and
`tests/sequenced_after/test_schema.py:45` write `implemented`; about a hundred
`tests/doc-health/fixtures/**/proposal.md` carry `none`. And
`contracts/schemas/ideation-dashboard-snapshot.schema.yaml:447` types the field
`{type: [string, "null"]}` — free text, no enum. **So the value is displayed,
never judged, and the fixtures disagree with each other.**

**THE ARCHIVE, READ AND NEVER JUDGED:** 161 archived `proposal.md`, **61** of
them carrying a value outside the vocabulary.

## D1 — VETO POINT: what canon does about a value outside its vocabulary

**RECOMMENDED — OPTION 1: KEEP the two-value vocabulary exactly as ratified and
GATE it, by ADDING one requirement.** One `## ADDED Requirements` block,
`### Requirement: Realization axis vocabulary is gated`, whose first line makes
a house validator refuse an off-vocabulary value on an ACTIVE proposal, with the
archive read and never judged and the standing divergence named in a CLOSED
register. **No `## MODIFIED` block, so no collision and no sequencing hold.**

*Why the register rather than a bare refusal.* A bare refusal is not landable:
the measurement says 26 active declarations would red the gate on the day it
lands, twelve of them for obeying the versioning policy. The register is a
RATCHET — every declaration it does not name is judged from day one, and the
named ones are reported and cannot grow, because the register is closed. It is
this estate's own idiom, not an invention: `contracts/openspec-cli-pin.yaml`'s
`dispositions:` block does exactly this for the pinned CLI, down to the
asymmetry this validator copies (an unmatched finding FAILS, an unmatched
exception REFUSES, so the archive is the event that forces re-examination).

*The cost of option 1, stated plainly.* The estate gains a 21-entry exception
file; a reader must consult it to know what the corpus actually declares. Every
one of those 21 entries is archive-coupled: when its packet archives or corrects
its declaration, the gate refuses (exit 2) until the entry is deleted — which
will occasionally red an unrelated lane's archive pull request, remedied by a
one-line deletion in that same pull request. That is the precedent's accepted
cost and it is taken deliberately.

**OPTION 2: AMEND *Realization axis declaration* to ADMIT the divergence** — a
third value, either `none` for an empty code surface (the issue's option 2) or,
on the measurement, a DEFERRED ALLOCATION, which is the larger and better-founded
class. It regularizes rather than corrects.
*Cost, written out:* it is a `## MODIFIED Requirements` block over a title an
ACTIVE ratified change — `add-structured-scope-substrate` — already modifies
(`openspec/changes/add-structured-scope-substrate/specs/release-realization/spec.md:16-42`).
Under *Ordered deltas and branch vocabulary* this packet would then have to
declare `sequenced_after: [add-structured-scope-substrate]`, write its pre-text
from THAT block rather than from canon, and accept the archive-order hold: the
basis change archives first or this one destroys review. It would also close the
question this packet deliberately leaves open — whether a deferred allocation is
canon's business at all — by answering it in the same act that installs the
gate, which is two decisions in one word.

**OPTION 3: RULE the value a synonym** — one canon sentence saying an
off-vocabulary `target_release` on an EMPTY code surface reads as `implemented`
(the issue's option 3, "the cheapest").
*Cost, and a MEASURED objection that is fatal to it as written:* **all five
active `none` carriers declare a NON-EMPTY `code_surface`** — four
`openxFactory`, one `xFactory`. A synonym rule conditioned on an empty code
surface would therefore reach NONE of them, leave every active carrier
off-vocabulary, and settle nothing. Widened to reach them, it stops being a
synonym rule and becomes option 2. And like option 2 it is a MODIFIED block over
the contested title, with the same sequencing hold.

**THE SUCCESSOR OPTION 1 NAMES AND DOES NOT TAKE.** Whether canon should admit a
deferred allocation as a third value is the real question the measurement
exposed, and it is a MODIFIED block with option 2's sequencing cost. It is named
in `tasks.md` § 6 as a successor rather than smuggled in here, and the register's
twelve `deferred-allocation` entries all retire on it.

## D2 — VETO POINT: the sweep

**RECOMMENDED — OPTION 1: this pull request corrects the FIVE active `none`
carriers and nothing else.** One value token per file, `none` → `implemented`,
every prose gloss preserved verbatim; five files, five lines, no behaviour
anywhere.

*Why these five and only these five.* For each of them the declaration's own
gloss says the packet cuts no bundle — *"no contract-bundle involvement"*, *"no
contract bundle is cut by openxFactory"* — and a packet that cuts no bundle
realizes on the affected repositories' main lines, which is what `implemented`
MEANS. The correction preserves each author's stated meaning instead of
supplying one; there is no judgment in it, which is exactly why it can be taken
by a lane that does not own those packets. The other 21 are not like that: a
deferred allocation rewritten to `implemented` would assert a realization on a
main line that is not where the change lands, and a
`repository-bootstrap` rewritten to `implemented` would name a line that does
not exist yet.

The five, with the token before and after:

| change | before | after |
| --- | --- | --- |
| add-composed-view-authoring | `none` | `implemented` |
| add-cpc-clearing-boundary | `none (no contract-bundle involvement — …` | `implemented (no contract-bundle involvement — …` |
| add-lens-document-selection | `none` | `implemented` |
| add-substantive-review-lane | `none (no contract-bundle involvement — …` | `implemented (no contract-bundle involvement — …` |
| register-gate-rules-council-seats | `none — no contract bundle is cut by openxFactory. …` | `implemented — no contract bundle is cut by openxFactory. …` |

*The custody check, taken rather than assumed.* These are ACTIVE ratified
packets, not records. `record-immutability` binds a document whose `Status:` is
`record`; a proposal of an active change carries `Status: ratified`, and
`fam_record_immutability` skips it by construction (`doc.status != "record"` →
`continue`). `release-realization`'s freeze requirements are *Origin retention
at archive* (the `.openspec.yaml` origin declaration) and, from
`add-structured-scope-substrate`, *Scope retention at archive* (`scope_globs`);
neither reaches `target_release:`, and neither file is touched. So no archive
gate of the five is broken by the correction.

**OPTION 2: each owning lane corrects its own, and the gate lands ADVISORY
until the last one is done.**
*Cost:* an advisory gate refuses nothing, which is the state the issue filed
about. It also spreads a five-line correction across five lanes and an unknown
number of days, during which the gate's only effect is a report nobody is
obliged to read.

**OPTION 3: correct nothing and register all 26.**
*Cost:* the register would carry five entries whose retirement is a one-token
edit with no judgment in it — a standing exception for a defect that could be
gone in the same commit — and an exception outlives the packet that needed it
more easily than a correction does.

## D3 — VETO POINT: how the gate resolves "a named release"

**THE MEASUREMENT FORCED THIS ONE OPEN AND IT CANNOT BE DEFERRED, because the
gate has to resolve the phrase in order to run.** Canon says *"a named release
defined in the aggregation repository"*. Measured 2026-09-11: the aggregation
repository `opensoft/xFactory` **defines no releases and carries no tags at all**
— its root holds no `contracts/` tree and `GET /repos/opensoft/xFactory/tags`
returns an empty list. Every release the corpus actually names is defined HERE:
`contracts/releases/contract-v*.digests.yaml` (53 digest inventories plus the
schema), `contracts/manifest.yaml`'s `contract_bundle_version: contract-v3.6`,
and this repository's own annotated tags.

**RECOMMENDED — OPTION 1: resolve a named release against the registry that
exists.** A value token counts as a named release when
`contracts/releases/<token>.digests.yaml` is present in the scanned tree. Where
the scanned tree carries no `contracts/releases/` at all — a consuming
repository that defines no releases of its own — the release-identifier SHAPE
`^contract-v\d+\.\d+$` is accepted on its own and the run SAYS SO in its output,
because refusing every release name in a tree that cannot define one would make
the validator unusable outside this repository.
*Cost:* the gate resolves a phrase against a place the promoted sentence does
not name. That divergence is **recorded as a successor and not repaired here**
(`tasks.md` § 6), because repairing it means editing the promoted sentence —
option 2's MODIFIED block and its sequencing hold, for a wording fix.

**OPTION 2: resolve it literally, against the aggregation repository.**
*Cost:* it admits nothing. `contract-v1.45` and both `contract-v3.0`
declarations would be refused, and the only lawful value in the estate would be
`implemented`. The gate would be wrong about three active packets on day one.

**OPTION 3: accept any release-SHAPED token without resolving it.**
*Cost:* `contract-v<next minor>` and any typo'd or invented version number pass,
and the gate stops distinguishing a release from a wish. The declaration
`declare-client-standing-policy-contract` carries is exactly this shape, and
under option 3 it would pass silently rather than being named in the register as
the deferred allocation it is.

## D4 — the code surface: a sibling validator, reading the shipped loader

**A NEW PAIR OF FILES, NOT AN ARM ON AN EXISTING VALIDATOR, AND THE REASON IS
CUSTODY.** `scripts/frontmatter_strict.py` is the shipped strict loader for the
realization-axis block, produced by `add-sequenced-after-substrate` and
**vendored byte-for-byte into codexFactory** (`scripts/merge_master/frontmatter_strict.py`,
pinned at `stack.yaml`'s `contract_ref`), with its refused set held in lockstep
with that repository's `change_digest.StrictLoader` by an explicit build
obligation. It is not this packet's file to widen, and widening it is not what
this packet needs: `target_release:` is a PROSE HEADER of the block, not one of
its two STRUCTURED fields, so no new strictness is asked for. What this packet
needs is a READER, and it takes one — `scripts/target_release.py` calls
`frontmatter_strict.read_front_matter`, so this gate and the loader refuse the
same documents and no proposal can mean one thing to one reader and another to
the next. A document the loader refuses is reported here as a finding against
that document rather than as a traceback.

**THE SHAPE IS `validate-scope-globs.py`'s, deliberately.** A module with the
rules (`scripts/target_release.py`), a thin CLI
(`scripts/validate-target-release.py [REPO_ROOT]`), and a corpus test that runs
the CLI over the live tree on every pull request
(`tests/target_release/test_target_release_gate.py::test_corpus_target_release_validates`),
which is how the required `pytest-suite` check —
`python3 -m pytest tests/ -q -m "not postgres"`, which runs everything under
`tests/` — comes to gate the corpus with no workflow edit. **Confirmed by
running it**, not by reading the workflow: `python3 -m pytest tests/target_release -q`
collects the new file with no registration anywhere.

**THE SCAN IS TOP-LEVEL AND THAT IS LOAD-BEARING.** It iterates
`REPO_ROOT/openspec/changes/<change>/proposal.md` and the archive one level
down, exactly as `validate-scope-globs.py` does — never `rglob`. About a hundred
`tests/doc-health/fixtures/**/openspec/changes/**/proposal.md` carry
`target_release: none` as fixture text for other families; a recursive scan
would refuse them all and make this gate a tax on every fixture the estate
writes.

**THREE EXIT CODES, AND THE THIRD IS THE PIN FILE'S.** 0 clean; 1 an
off-vocabulary declaration the register does not name (a statement about the
PROPOSAL, remedied by its own packet); 2 a register that cannot be used, or an
entry that matched nothing (a statement about the REGISTER, remedied by deleting
the entry). Where both occur the run prints both and exits 1, the declaration
being the more actionable defect.

**THE REGISTER IS NOT UNDER `contracts/`, AND THAT IS DELIBERATE.** A file under
`contracts/` is a bundle surface whose change owes a bundle cut; an exception
register that could not be edited without cutting a contract release would be
edited late or not at all. It lives beside the validator that reads it, moves
with it, and is shape-checked on every run — a malformed register REFUSES rather
than being ignored, because ignoring it would silently re-fail every declaration
it covers.

## D5 — why an OpenSpec change and not a patch

**BECAUSE CANON GAINS A REQUIREMENT.** The gate is not an implementation detail
of an existing rule: no promoted requirement says the vocabulary is enforced,
which is precisely the defect. `release-realization` today states a vocabulary
and stops. Adding a refusal, a closed exception mechanism, an archive exemption
and a two-status asymmetry in `scripts/` alone would put four governance
decisions in code with no delta behind them — the shape this repository refuses,
and refused in terms on PR #780: *"Rewording the requirement here would edit
ratified text with no word behind it."* The remedy is a requirement plus its
realization in the same pull request, under `release-realization`'s
merged-plus-green rule.

## D6 — sequencing, and the sibling search, pasted

Performed 2026-09-11 before authoring, on the lane-collision protocol's
claim-before-author rule; recorded on #956 at the claim and re-run at the start
of this packet.

```text
$ gh api '/repos/opensoft/openxFactory/pulls?per_page=50' --jq '.[] | "#\(.number) \(.head.ref)"'
#961 record/repository-identity-transferred      #960 change/amend-register-act-5b-projection-proof
#959 change/amend-kill-switch-to-declared-test-companion
#947 change/amend-merged-into-empty-tail-standing
#945 change/honour-grandfather-dispositions-in-ratified-provenance
#940 change/split-opendox-section-5-shed          #888 doc-health/derive-possibles
#594 rescue/worker-fleet-health-monitoring        #518 docs/add-usage-controlled-evidence-chain

$ for n in 940 945 947 959 960 961; do gh api .../pulls/$n/files --jq '.[].filename' \
      | grep -E 'release-realization|target_release|scripts/target'; done
(no output — NO open pull request touches this capability, this field, or these scripts)

$ ls -d openspec/changes/*/specs/release-realization
add-sequenced-after-substrate   add-structured-scope-substrate   gate-realization-axis-vocabulary

$ grep -rln "Realization axis vocabulary is gated" openspec/changes/ | grep -v archive/
openspec/changes/gate-realization-axis-vocabulary/...   (this packet alone — the title is novel)
```

**THE TWO ACTIVE SIBLINGS ON THIS CAPABILITY, BY REQUIREMENT HEADING:**

- **`add-structured-scope-substrate`** — one `## MODIFIED Requirements` block
  over ***Realization axis declaration*** (restating the two-value sentence
  verbatim and adding `scope_globs:`) plus four ADDED requirements
  (*Structured path-scope declaration*, *Structured path-scope validation*,
  *Trust-root integrity of the structured scope declaration*, *Scope retention
  at archive*, *Floor primacy over declared scope at check time*). **This packet
  adds a NOVEL title and modifies nothing, so the two do not collide and no
  `sequenced_after` is owed.** Its header says `code_surface:` and
  `target_release:` are UNCHANGED — the routing `state-header-window-budget`
  made to it does not hold, as #956 records.
- **`add-sequenced-after-substrate`** — ADDED requirements only, among them
  ***Strict loading of the realization-axis front-matter block***. **This packet
  neither realizes nor contradicts it.** That rule reaches "every STRUCTURED
  field" of the block, naming `scope_globs:` and `sequenced_after:`;
  `target_release:` is a prose header and is not in its set. This gate CONSUMES
  the loader that rule produced rather than extending it, so the strictness it
  demands is inherited and not weakened: a document that loader refuses is
  refused here.

`sequenced_after: []` is declared as a ROOT claim, and it is corroborated rather
than asserted: no active change carries a `## MODIFIED` block over any title
this delta writes, the title being new to the capability.

## D7 — what is NOT taken here, measured and deliberately left

- **The deferred-allocation question.** Twelve active packets need a spelling
  canon does not have. Answering it is a MODIFIED block over the title
  `add-structured-scope-substrate` holds, with the sequencing hold that carries
  (D1, option 2). Named as a successor in `tasks.md` § 6; the register's twelve
  `deferred-allocation` entries all retire on it.
- **The "aggregation repository" wording.** Canon resolves a named release
  against a repository that defines none (D3). Repairing the phrase is a
  MODIFIED block for a wording fix; the gate resolves against the registry that
  exists and says so.
- **The 27 archived `none` carriers and the other 34 archived off-vocabulary
  declarations.** 61 in all. Frozen record: read, counted, judged never. A gate
  that demanded an edit nobody may make would be a standing finding with no
  remedy.
- **The ideation dashboard is not changed, and that it need not be is
  MEASURED.** `_release_frontmatter` returns the header string and
  `wheel.js:767-768` renders it; the snapshot schema types the field
  `{type: [string, "null"]}` with no enum. So the five corrected values render
  as themselves and no fixture asserts the old token for a real corpus change —
  `tests/ideation-dashboard`'s `none` fixtures are synthetic trees it builds
  itself, not the live corpus.
- **The other estate repositories are not swept.** codexFactory, OpsxFactory and
  the rest carry their own corpora and their own registers would be their own
  act; this validator takes a `REPO_ROOT` and refuses a tree with no register
  rather than assuming an empty one.
- **`code_surface:` is not gated.** Its vocabulary (`none` or the repositories
  whose runtime artifacts change) is the other half of the same sentence and is
  equally unread. It is a second population, a second register and a second set
  of classes, and folding it in here would widen a ruled remedy into an unruled
  sweep. Named in `tasks.md` § 6.
