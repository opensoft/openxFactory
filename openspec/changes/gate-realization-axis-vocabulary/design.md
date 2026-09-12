# Design: gate-realization-axis-vocabulary

Status: ratified
Ratified by: gate-realization-axis-vocabulary — 2026-09-12, Brett Heap, D1 "Keep and gate" / D2 "Sweep in this PR" / D3 "Resolve against the registry that exists" (record `review/ratification-2026-09-12.md`)
Kind: design

**EVERY DECISION THIS AUTHORING SESSION TOOK IS HERE, WITH ITS ALTERNATIVE AND
THE ALTERNATIVE'S COST.** Brett Heap's word of 2026-09-11T12:08:24Z — verbatim
**"land each when green, archive both when landed, claim 955 and 956"** —
commissioned the authoring and took none of them.

**D1, D2 AND D3 WERE THE DECLARED VETO POINTS AND ALL THREE ARE NOW RULED.**
Brett Heap ruled on 2026-09-12 at 15:45Z — three independent multiple-choice
rulings, the recommendation presented first in each, recorded on openxFactory PR
[#963](https://github.com/opensoft/openxFactory/pull/963#issuecomment-5646922493)
at 2026-09-12T15:45:19Z; record `review/ratification-2026-09-12.md`. **D1 =
"Keep and gate"**, not *"Admit none"* and not *"Rule none a synonym"*; **D2 =
"Sweep in this PR"**, not *"Each owning lane sweeps"* and not *"Register all
26"*; **D3 = "Resolve against the registry that exists"**, not *"Resolve
literally"* and not *"Accept any release-shaped token"*. Each is the RECOMMENDED
and already-encoded option, so **NOTHING IN THE DELTA, THE VALIDATOR OR THE
REGISTER MOVES**; D0 and D4 through D7 were carried beside them and none was
vetoed. The alternatives below are retained as the record of what was put and
declined, not as work owed. What D2's ruled option REACHED when it was executed
— six carriers at the ratified head, not the five the drafting corpus carried —
is D2a, which is an account of the execution and not a fourth decision.

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

## D1 — RULED: keep the two-value vocabulary exactly as ratified, and gate it

**RULED 2026-09-12 BY BRETT HEAP — "Keep and gate"**, the RECOMMENDED option,
against *"Admit none"* and *"Rule none a synonym"* (recorded on PR #963 at
2026-09-12T15:45:19Z; record `review/ratification-2026-09-12.md`).
**THE RECOMMENDATION WAS TAKEN, SO NOTHING THIS DECISION REACHES MOVES**: the
one `## ADDED Requirements` block stands as authored, there is still no
`## MODIFIED` block and therefore still no `sequenced_after` hold, and the
21-entry register stays CLOSED — which is why the sixth carrier the merge
brought in was SWEPT and could not be registered (D2a). Options 2 and 3 are
retained below as the record of what was put and declined; neither was ever
encoded and neither is work owed.


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

## D2 — RULED: the sweep, in this pull request

**RULED 2026-09-12 BY BRETT HEAP — "Sweep in this PR"**, the RECOMMENDED
option, against *"Each owning lane sweeps"* and *"Register all 26"* (recorded on
PR #963 at 2026-09-12T15:45:19Z; record `review/ratification-2026-09-12.md`).
**THE RECOMMENDATION WAS TAKEN, SO THE SWEEP IS THIS PULL REQUEST'S WORK AND
NOT A LANE-BY-LANE OWED LIST.** Its POPULATION is a fact about a tree and is
measured at the head the sweep lands on, which at ratification is the merge of
`origin/main` `1f068646`: SIX carriers, not the five this section was drafted
against. D2a records the sixth, its different defect class, and why the
correction supplies no judgment. Options 2 and 3 are retained below as the
record of what was put and declined.


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

### D2a — THE SWEEP AS PERFORMED, at the head this packet is ratified on: SIX carriers, not five

**D2 WAS PUT AND RULED AS WRITTEN ABOVE; THIS SUBSECTION RECORDS WHAT THE
RULED OPTION REACHED WHEN IT WAS EXECUTED, AND NOTHING ELSE.** Brett Heap's
word of 2026-09-12T15:45Z takes D2 option 1 under the label **"Sweep in this
PR"** — *the existing non-conforming spellings across the corpus are swept in
this same pull request* — and a sweep's population is a fact about a TREE, so
it is measured at the tree the sweep lands on, not at the tree the option was
drafted against. That is D8e's and D8h's lesson applied before the fact rather
than after it.

Measured on this branch at the merge of `origin/main` `1f068646` (merge commit
`fb55c9e9`), by `python3 scripts/validate-target-release.py .`: **six** active
declarations sit outside the vocabulary and outside the closed register — the
five `none` carriers D2 names, and a SIXTH that `origin/main` acquired after
D2 was drafted, when `amend-kill-switch-to-declared-test-companion` landed
with pull request #959 on 2026-09-11T17:19:09Z.

| change | before | after | class |
| --- | --- | --- | --- |
| add-composed-view-authoring | `none` | `implemented` | `none` carrier |
| add-cpc-clearing-boundary | `none (no contract-bundle involvement — …` | `implemented (no contract-bundle involvement — …` | `none` carrier |
| add-lens-document-selection | `none` | `implemented` | `none` carrier |
| add-substantive-review-lane | `none (no contract-bundle involvement — …` | `implemented (no contract-bundle involvement — …` | `none` carrier |
| register-gate-rules-council-seats | `none — no contract bundle is cut by openxFactory. …` | `implemented — no contract bundle is cut by openxFactory. …` | `none` carrier |
| **amend-kill-switch-to-declared-test-companion** | `a code surface (in codexFactory), so per …` | `implemented — a code surface (in codexFactory), so per …` | **no leading token at all** |

**THE SIXTH IS A DIFFERENT DEFECT FROM THE OTHER FIVE, AND THE CORRECTION IS
THE SAME SIZE.** The other five wrote a token canon does not admit. This one
wrote no token at all: the declaration opens as a running sentence, so the
VALUE TOKEN — the first whitespace-delimited word — is the article `a`, which
is why the gate names `` `a` `` in its refusal. The correction prefixes the
token the author's own gloss already means and preserves every word of that
gloss verbatim after an em dash, exactly as `register-gate-rules-council-seats`
already reads.

**THAT `implemented` IS THE AUTHOR'S OWN MEANING, NOT THIS LANE'S JUDGMENT,
AND THE GLOSS SAYS SO IN ITS OWN WORDS:** *"No contract bundle is cut, nothing
under `contracts/` moves, no `contract_bundle_version` is spent, no
openxFactory CONTRACT digest set moves and NO RELEASE TAG IS OWED."* A packet
that cuts no bundle and is owed no release tag realizes on the affected
repositories' main lines — there, codexFactory's — and that is what
`implemented` MEANS. D2's whole reason for holding that a lane which does not
own a packet may still correct it is that there is no judgment in the
correction; this one meets that bar on the declaration's own sentence. The
custody check is D2's, unchanged: the packet is ACTIVE and `Status: ratified`,
not `record`, so `record-immutability` does not bind it
(`fam_record_immutability` skips any document whose status is not `record`);
*Origin retention at archive* and *Scope retention at archive* reach
`.openspec.yaml`'s `origin:` block and `scope_globs` and neither reaches
`target_release:`; neither file is touched.

**WHAT THE ALTERNATIVE WOULD HAVE BEEN, AND WHY IT IS NOT AVAILABLE.** Leaving
the sixth uncorrected is not a neutral act here: the gate's live-corpus test
`test_corpus_target_release_validates` reds the required `pytest-suite` while
it stands, so the packet could not land. Registering it instead is refused by
the register's own closure (D1: an entry may be REMOVED, never ADDED, because
admitting a value is a canon act and not a validator edit) — the very rule the
same word ratified under **"Keep and gate"**.

**THE POPULATION AFTER THE SWEEP IS ZERO, RE-MEASURED AND NOT ASSERTED**: 41
active proposals, 41 declaring — 17 `implemented`, 3 a named release, 21 named
by the register, **0** outside the vocabulary; exit 0. `tasks.md` § 3.4, § 3.18
and § 4.1 carry the runs.

**THIS IS A LIVE-CORPUS RACE AND IT IS DISCLOSED RATHER THAN CLOSED.** Any
proposal landing on `main` between this measurement and this packet's merge
can add a seventh, and the remedy is the same one-token correction in this
same pull request, re-measured at that head. The gate is what makes the race
visible at all; before it, the divergence landed silently, which is what
openxFactory #956 filed about.

## D3 — RULED: resolve against the registry that exists

**RULED 2026-09-12 BY BRETT HEAP — "Resolve against the registry that exists"**,
the RECOMMENDED option, against *"Resolve literally"* and *"Accept any
release-shaped token"* (recorded on PR #963 at 2026-09-12T15:45:19Z; record
`review/ratification-2026-09-12.md`). **THE RECOMMENDATION WAS TAKEN, SO
`_registry_present`, `RELEASE_ID_RE` AND THE SHAPE-ONLY FALLBACK STAND EXACTLY
AS AUTHORED AND REVIEWED.** The registry the gate resolves against is the one
on the tree it scans: at this ratified head `contracts/releases/` carries 55
digest inventories, two of them (`contract-v3.7`, `contract-v4.0`) arriving with
the same merge — which is the ruled option working as ruled, the gate following
the registry rather than a frozen list. The divergence between that registry and
the promoted sentence's "aggregation repository" is recorded as a successor and
not repaired here (`tasks.md` § 6.2). Options 2 and 3 are retained below as the
record of what was put and declined.


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
`^contract-v[0-9]+(?:\.[0-9]+){1,2}$` (`RELEASE_ID_RE`, TWO or THREE
components — `contract-v1.45` or `contract-v1.2.3` — restating this estate's
own `release-digest-inventory.schema.yaml` `$defs.bundle_tag` pattern, D8c)
is accepted on its own and the run SAYS SO in its output, because refusing
every release name in a tree that cannot define one would make the validator
unusable outside this repository.
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
  `{type: [string, "null"]}` with no enum. So the six corrected values render
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

## D8 — the bench's two code findings, TAKEN IN FULL, and the sweep for their classes

The draft pull request's first automated review round opened two threads on
`scripts/target_release.py`. **Both are real defects in this packet's own new
code, both are TAKEN, and neither is a wording quarrel** — each was reproduced
on a built tree before it was fixed, and each fix is pinned by refusal tests
that fail against the code as it stood.

**(a) A VALUE TOKEN REACHED A PATH BEFORE ITS SHAPE WAS CHECKED** (thread
`PRRT_kwDOTAvnrs6heJ1R`, `scripts/target_release.py:172`). `resolves_as_release`
matched `RELEASE_ID_RE` on the NO-REGISTRY branch only; where the registry
exists — which is this repository — the token went straight into
`contracts/releases/<token>.digests.yaml`. The token is author-controlled front
matter, so the boundary the registry is supposed to draw was not holding.
MEASURED, before the fix, on a tree built for it: with
`contracts/elsewhere.digests.yaml` planted one level ABOVE the registry, the
declaration `target_release: ../elsewhere` returned `(True, True)` and the
whole-corpus scan reported **0 findings, 1 a named release** — an off-vocabulary
declaration passing the gate as a release. A planted
`contracts/releases/none.digests.yaml` did the same for the bare word `none`,
which is precisely the value this packet exists to refuse. THE FIX inverts the
order: the shape is the FIRST test, in EVERY branch, and a token that fails it
is refused on its shape and never becomes a path component. On the same tree
the declaration is now a finding naming the file and the token.

**(b) A FIELD THE REQUIREMENT NAMES WAS ENFORCED BY A TEST AND NOT BY THE
LOADER** (thread `PRRT_kwDOTAvnrs6heJ2G`, `scripts/target_release.py:92`,
consumed at `:243`). The ADDED requirement has every standing entry carry "the
value token as it stands, the class of divergence, the reason, a citation, and
the event that retires the entry" — five things — but `_REQUIRED_ENTRY_KEYS`
listed four, omitting `cited_to`, and the citation was asked for only by
`test_every_register_entry_declares_a_known_class_and_a_citation`, which reads
the register THIS repository carries. MEASURED: `load_register` accepted an
entry with no `cited_to:` at all, and `scan` then used it to grandfather a
declaration. A test over one file is not a schema; the loader is. THE FIX makes
`cited_to` a required key, shape-checked as a non-empty list of non-empty
strings, with the refusal naming the entry and, for a bad item, its position.

**THE SWEEP FOR THOSE TWO CLASSES FOUND TWO MORE, AND BOTH ARE FIXED HERE.**
The classes are "author-controlled text that reaches a path" and "a constraint
the requirement states that only a corpus test enforces".
- A register entry's **`change:` is resolved under `openspec/changes/`** by
  every consumer — the corpus test that proves each entry names a live active
  change does exactly that — and nothing checked its shape. `CHANGE_ID_RE` now
  refuses anything that is not one directory segment, at the load, so `../..`
  or `a/b` cannot be written into the register and reach a path.
- The **CLOSED CLASS SET** lived as a literal inside one corpus test. The
  requirement makes admitting a new class a SPECIFICATION act, so the set is
  now `REGISTER_CLASSES` beside the loader and is enforced for every tree; the
  corpus test reads the module's set rather than keeping a second copy that
  could drift from the thing it is evidence about.

**MEASURED IN THE SWEEP AND DELIBERATELY NOT TAKEN.** The register's own
`schema_version:` and `kind:` headers are not enforced by `load_register`. The
house rule that every YAML carries them is real and this register carries them,
but the ADDED requirement does not name them among what an entry or the file
must carry, and enforcing them would refuse a consuming tree's register — and
every test register built in a tmpdir — for a field the requirement never asks
for. Enforcing what the requirement states is the class of defect being fixed
here; enforcing more than it states would be a different act, and an unruled
one.

### D8b — the bench's second round: four threads, all four TAKEN

A second automated round opened four threads. **None is a wording quarrel and
none is refused.** Two of them are one defect seen from both ends.

**(c) A REPEATED DECLARATION WAS HALF-READ** (`scripts/target_release.py:208`).
`target_release:` is a PROSE header, and the shared strict loader refuses a
repeated STRUCTURED field as the duplicate key it is while JOINING a repeated
prose header into one raw string — a deliberate, documented posture of that
module, not a bug in it. This reader then tokenized the join. MEASURED, against
the code as it stood: a block declaring `target_release: implemented (the main
line)` and then `target_release: none` came back as `'implemented (the main
line)\ntarget_release: none'` and `value_token` returned `implemented`. That is
show-one-authorize-another — a reviewer sees two declarations and the gate
authorizes the first — and it is exactly the class the strict loader exists to
close, arriving here through the one field the loader deliberately leaves prose.
THE FIX refuses the repeat by name in `declaration`, tested on the value the
loader RETURNED (whose own leading header the loader has already stripped, so a
match can only be a repeat). **The shared loader is NOT edited and no second
front-matter parser is written** — both would exceed this packet's code surface,
and the second is the thing the module's docstring promises not to do. The
requirement gains the sentence and the scenario, because a gate that refuses
something canon does not name is a gate nobody can appeal.

**(d) THE CLOSED REGISTER WAS NOT CLOSED** (`scripts/target_release.py:308` and
the requirement text at `specs/release-realization/spec.md:73` — two threads,
one defect, seen from the code and from the canon). The requirement SHALLs a
register that is removable and never addable, and the register file's own header
says "an entry is never ADDED, because admitting a new value to the vocabulary
is a canon act and not a validator edit" — and nothing enforced it. Every new
`(change, token)` pair was accepted, so a later pull request could have appended
an exception and made any off-vocabulary declaration pass with the gate green
and no change to this specification. **A ratchet that only ratchets when nobody
pushes is not a ratchet**, and "a vocabulary stated in prose and checked by
nobody" is the sentence this whole packet opens with; the register had
reproduced the defect it was built to close.

THE FIX records the baseline in the MODULE — `CLOSED_REGISTER`, the 21 pairs the
register carries at this gate's landing — and refuses an entry the baseline does
not carry. Three properties, each chosen and each tested:
- **A baseline may be a strict SUPERSET.** Removal is the one lawful direction
  (`Report.stale` already REFUSES with a distinct status until a matched-nothing
  entry is deleted), so a pair outlives its entry. Ceiling, never floor.
- **It binds the HOUSE register only.** `--register PATH` exists so the tests
  can put a known register in front of a known tree and so a consuming tree can
  name its own; binding those to THIS repository's baseline would refuse every
  register but this one and make the flag useless. A caller may pass its own.
- **It does not pretend to be tamper-proof.** An author who means to add an
  exception can edit both files. What the baseline buys is that they CANNOT do
  it by appending a line to a data file: the addition must be written where the
  refusal is written, in the module, beside the reason, and the diff shows the
  act for what it is. That is what "closed" can mean inside one repository, and
  it is the alternative the bench itself named — an enforced baseline rather
  than a process rule nobody checks.

**(e) TWO COMPLETED TASKS WERE LEFT UNTICKED** (`tasks.md:248`). The README
active row and the sweep-ledger row both landed in `13ff6162` while § 4.11 and
§ 4.9 still read as owed. That is a real defect in a packet whose whole method
is that the task list is the record: a completion ledger that disagrees with the
diff is worth less than no ledger. Both are ticked, each on the output it was
ticked for, and each says which commit did the work.

### D8c — the bench's third round: two threads, both TAKEN, and one of them a regression this packet's own fix introduced

**(f) THE RELEASE-ID SHAPE WAS NARROWER THAN THE ESTATE'S OWN, AND § 3.7 MADE
THAT MATTER** (`scripts/target_release.py:114`). `RELEASE_ID_RE` was
`^contract-v\d+\.\d+$` — two components. The estate DEFINES the shape of a
release tag in `contracts/releases/release-digest-inventory.schema.yaml`
`$defs.bundle_tag`, as `^contract-v[0-9]+(?:\.[0-9]+){1,2}$` — two OR three. So
the gate's idea of a release name was narrower than the inventory contract's,
and a three-component release WITH ITS INVENTORY ON DISK would have been
refused.

**THE HONEST PART: this was latent until the round-1 fix, and the round-1 fix
is what made it live.** Before § 3.7 the shape was consulted only where no
registry exists, and the registry branch resolved a token by looking for its
file — so `contract-v1.2.3.digests.yaml` would have resolved. Making the shape
the FIRST test in EVERY branch closed the traversal and, in the same stroke,
imposed a narrower vocabulary than the estate's own on the branch that
previously had none. That is the cost of a shape-first guard and it is the
reason the guard's shape has to come from the estate rather than from the
author of the guard. Measured 2026-09-11 by counting the files
(`ls contracts/releases/*.digests.yaml | wc -l`): **53** inventories, all
two-component, which is the same 53 D3 counts and the figure this bench line
first got wrong — so nothing in the corpus was refused
and the defect was latent rather than standing — but the next three-component
cut would have met it at the gate, which is the worst possible time.

THE FIX makes the pattern the schema's, RESTATED rather than imported, with the
equality asserted by a test that READS the schema
(`test_the_release_id_shape_is_the_estates_own`). Restated, because this module
must judge a consuming tree that carries no `contracts/` at all and a reader
that needed the schema present would refuse such a tree for the wrong reason;
asserted, because a restatement nobody checks is the defect this entire packet
is about. It is the same device `frontmatter_strict` uses for the lifecycle
window it restates from `doc_health`. Four more cases pin the edges: a
three-component release resolving against a registry, its shape accepted where
no registry exists, a FOUR-component name still refused, and a three-component
declaration passing end to end.

**(g) THE README ROW'S TEST FIGURE WAS STALE** (`README.md`). It still read 32
while `proposal.md` and `tasks.md` § 3.5 had been re-measured to 46. Already
corrected in `989c7059`, before the thread was read, and re-measured again with
this round. The lesson is § 3.8's and is now stated as a rule rather than a
habit: the figure moves in ALL THREE places in the same commit, every time,
because a count carried in one document and re-measured in another is the
brief-wording defect this house has already paid for once.

### D8d — the bench's fourth round: five threads, all five TAKEN

**(h) THE SHAPE-ONLY FALLBACK CONTRADICTED THE REQUIREMENT'S OWN MUST** (two
threads: the scenario at `specs/release-realization/spec.md` and the code at
`scripts/target_release.py`). The scenario said *"a release-shaped name the
registry does not carry MUST be refused"*, and `resolves_as_release` accepts
the SHAPE where the scanned tree carries no registry at all — so by the letter
of the scenario, `contract-v999.999` passed in a tree that defines no releases.

The fallback is not an accident. The module has documented it from the first
draft: a gate that refused every release name in a tree that cannot define one
would be unusable in every consuming repository, and `tasks.md` § 6.5 already
names those repositories as unswept by design. **What was missing is that canon
never said it.** A behaviour a reader can only discover by reading the
implementation is the same defect as a vocabulary only prose asserts.

Of the two remedies the bench named, the fallback is **ENCODED** rather than
removed:
- the requirement gains a paragraph — resolution is against the registry THE
  SCANNED TREE defines; where it defines none the shape is the whole test; the
  weaker judgment SHALL NOT be silent; and the shape itself SHALL be the one
  the estate defines rather than one the gate invents (which is D8c (f)'s fix,
  now stated in canon too);
- the existing scenario's MUST is qualified to a tree that HAS a registry;
- a new scenario, *The scanned tree defines no release registry at all*, states
  the fallback and the obligation to say so;
- and the loudness is TESTED, not merely intended: the run prints *"no
  contracts/releases in this tree, so a release name is accepted on its SHAPE
  alone"* with no registry, and must NOT print it with one.

Fail-closed was the alternative and is recorded as refused with its reason: it
would make the gate refuse a lawful declaration in every repository but this
one, and it would do so silently from the consuming repository's point of view
— trading a stated weaker judgment for an unstated stricter one.

**(i) THE REPEAT GUARD WAS OVER-BROAD, AND IT CAUGHT THE PROSE IT WAS WRITTEN
TO PROTECT** (`scripts/target_release.py`). `_REPEATED_HEADER_RE` allowed
leading whitespace. An INDENTED line inside a front-matter block is a
CONTINUATION of the gloss — that is exactly how the loader joins a multi-line
declaration — so a gloss reading `  target_release: the main line` was refused
as a duplicate declaration. Measured: it was. That contradicts the requirement's
own rule to judge the token and never the gloss, and it is a good reminder that
a guard added in one round is new code and gets the next round's scrutiny like
anything else. The pattern is now anchored at column 0, which is the shared
loader's own notion of a header line (`frontmatter_strict._TOP_LEVEL`,
`^([A-Za-z_][A-Za-z0-9_-]*):`), so the guard and the loader agree on what a
declaration IS rather than each having a private idea.

**(j) THE INVENTORIES WERE STALE** (two threads). `proposal.md` still reported
seven scenarios and omitted the two the bench added; the pull-request
description still said 32 tests and seven scenarios. The description had been
rewritten before those threads were read. The proposal's inventory now names
all TEN and marks which THREE the bench added. Same lesson as D8c (g), now
paid for twice: **a count or an inventory moves in ALL of its sites in the SAME
commit.** (A later Copilot pass caught this very sentence overstating the
three as four — `tasks.md` records the correction beside this one.)

### D8e — the bench's fifth round: three threads, all three TAKEN, and one of them a figure this bench invented

**(k) "47 INVENTORIES" WAS A NUMBER NOBODY COUNTED.** D8c's account of the
release-id fix asserted 47 two-component inventories under
`contracts/releases/`. There are **53**, which is what D3 and `tasks.md` § 2
had said all along from an actual count — so the bench's own evidence line
contradicted the packet's own measurement, in the very paragraph arguing that
a restatement nobody checks is a defect. Counted now, and the command is on the
record beside the figure: `ls contracts/releases/*.digests.yaml | wc -l` → 53.
The conclusion the figure supported is unchanged (all 53 are two-component, so
the narrow regex refused nothing standing), which is exactly why the error
survived a read: **a number that does not change the conclusion is the easiest
kind to get wrong and the least likely to be re-derived.** The rule this packet
already states for test counts — re-measure, never carry — applies to every
figure in a record, including the ones written while disposing of a bench.

**(l) THE PROPOSAL'S BEFORE/AFTER TABLE WAS NOT REPRODUCIBLE FROM ITS OWN
COMMAND.** It read `before (this tree, pre-correction) 38 / 9` and `after 38 /
14`, under the command `validate-target-release.py .` — but running that
command HERE gives 39 / 15, because this packet's own `proposal.md` is an
active change declaring `target_release: implemented` and is judged by its own
gate like every other. `tasks.md` § 4.1 and the pull-request description had
both already been re-taken; the proposal had not, so the packet disagreed with
itself in three places on a figure a reader would check first. The rows are now
labelled by TREE (`origin/main` `38c076d1` vs THIS tree), the `+1`/`+1` is
explained as the packet's own proposal, and the table says the two rows are the
same validator pointed at two trees.

**(m) A MISSING NEWLINE HID A TASK.** `- [x] 3.10` ran on from the end of
§ 3.9's paragraph, so Markdown rendered the third bench round as prose inside
the second rather than as its own checklist item — invisible to anyone reading
the completion ledger as a list, which is how it is meant to be read. Split.
Small, and worth recording: in a packet whose method is that the task list IS
the record, a task that does not render as a task is a task that is not in the
record.

### D8f — the bench's sixth round, on the fix round's own head: one thread, TAKEN, and it is the one this packet had already disclosed and declined to take

A Copilot pass on `e670cf30` (the ledger-fix commit) suppressed five comments
into its review summary rather than opening threads (*"Comments generated: 0
new"*). One was the scenario-count miscount corrected above the line for it in
`tasks.md` § 3.13. A second was real code, not a count, and this packet's own
fix round DISCLOSED it without taking it, reasoning that a code change with
its own test was outside a round scoped to counts and ledger entries. On the
NEXT push (`378eb3c3`, carrying only that scenario-count correction), the same
finding came back — this time as a formal, unresolved thread
(`PRRT_kwDOTAvnrs6hgEM5`). A finding does not stop being real for having been
named once already; it is taken here.

**(n) A CANDIDATE RELEASE INVENTORY COULD BE A SYMLINK, AND `Path.is_file()`
FOLLOWS THEM.** `resolves_as_release` resolved a release token with
`(registry / f"{token}.digests.yaml").is_file()`. `Path.is_file()` follows
symlinks and reports on the TARGET, so a committed
`contracts/releases/contract-vX.Y.digests.yaml` symlink — including one
pointing outside this tree — would be treated as an estate-defined release:
the gate's own `implemented`-or-named-release vocabulary admits a name whose
"definition" is a link an author planted, not an inventory the estate cut.
This is not a new class this packet invented a defense for; it is the SAME
class `scripts/hermes_runtime_validation/release.py` already defends against,
in `RepoSource.exists` and `list_release_inventories`
(`target.is_file() and not target.is_symlink()`), for the identical reason —
so the fix RESTATES that module's own guard rather than inventing a new one or
importing across a boundary this module does not otherwise cross (it must
judge a tree that carries no `hermes_runtime_validation/` at all, the same
posture D8c and D8d already took for the release-id shape and the loudness
guard). THREE tests pin it: a symlinked inventory does not resolve; one
pointing OUTSIDE the tree (planted in a sibling tmpdir) does not resolve
either, because the defect is not merely a traversal defect; and a REGULAR
inventory beside a symlinked one for a DIFFERENT token still resolves, so the
refusal is per-candidate and not a registry-wide fallback. Measured against
the code as it stood (`git stash` the fix, keep the tests): all three FAIL,
confirming the reproduction; restored, all 65 tests in the file PASS.

### D8g — the bench's seventh round, after a merge of main: one thread, TAKEN, and it is the directory-level twin of D8f

A Copilot pass on the merge of `origin/main` `ac688c40` into this branch
opened one new thread (`PRRT_kwDOTAvnrs6hgYZd`, `scripts/target_release.py:349`):
D8f made the CANDIDATE FILE'S symlink-ness the guard, but never checked the
REGISTRY DIRECTORY itself.

**(o) A COMMITTED `contracts/releases` DIRECTORY SYMLINK LET AN EXTERNAL
INVENTORY PASS, BECAUSE ONLY THE CANDIDATE FILE WAS EVER CHECKED FOR
SYMLINK-NESS.** `resolves_as_release` computed `present = registry.is_dir()`,
and `Path.is_dir()` follows symlinks exactly as `Path.is_file()` does — so a
committed `contracts/releases` DIRECTORY symlink, pointing anywhere outside
this tree, resolved as a PRESENT, trustworthy registry. A REGULAR file
reached only THROUGH that symlinked parent is never itself a symlink, so
D8f's own guard (`candidate.is_file() and not candidate.is_symlink()`) saw
nothing to refuse: the file passed on its own merits while the directory
that made it reachable was never examined at all. This is the SAME class of
defect D8f closed, one level up the path, and the same reason it survived
D8f's own fix: a guard placed at the leaf does not see a compromise at the
root.

**THE FIX IS A SINGLE SHARED CHECK, NOT A SECOND SYMLINK GUARD BOLTED ON
BESIDE THE FIRST.** A new `_registry_present(repo_root)` helper returns
`registry.is_dir() and not registry.is_symlink()`, and BOTH places in this
module that ask "is the registry present" — `resolves_as_release`'s local
`present` and `scan`'s `Report.registry_present` — now call it, where before
each computed the same bare `.is_dir()` independently. This is not merely
tidiness: it is why `Report.registry_present` can no longer say "present"
about a registry `resolves_as_release` itself refused to trust, the exact
kind of report/behaviour split D2's original register-shape fix (D8) closed
for the register file and this closes for the registry directory.

**A SYMLINKED DIRECTORY IS TREATED EXACTLY AS A MISSING ONE, WHICH IS THE
EXISTING, DOCUMENTED FALLBACK AND NOT A NEW RULE INVENTED FOR THIS THREAD.**
Where no registry exists at all (a consuming tree that defines no releases
of its own), the module already trusts a release-shaped TOKEN on its SHAPE
alone and says so out loud (D8d (a), the *shape-only fallback* scenario). A
symlinked `contracts/releases` now falls into that same, already-weaker,
already-loud branch: `registry_present` is False, the run prints the note a
bare tree gets, and — this is the property that closes the finding — an
inventory sitting behind the symlink, present or absent, real or fabricated,
changes NOTHING about the result. The finding described an external
inventory's CONTENT granting elevated trust through a symlinked directory;
after the fix, the directory's contents have no leverage at all, because the
directory itself is never consulted once it is known to be a symlink.

THREE tests pin it, all in the file's `resolves_as_release` unit section
beside D8f's own (never edited): a symlinked registry directory resolves a
release-shaped token on shape alone, with `registry_present` reported False;
an EMPTY symlinked directory and one holding a genuine, matching inventory
resolve IDENTICALLY (proving the external file's presence is inert); and,
end to end through the validator CLI, the gate prints the same "accepted on
its SHAPE alone" note for a symlinked registry directory that it prints for
a tree carrying no `contracts/releases/` at all. Measured against the code
as it stood (`git stash scripts/target_release.py`, keep the tests): all
three FAIL — the symlinked-directory cases returned `(True, True)`, the same
over-trusting result the finding named; restored, `pytest
tests/target_release -q` — **68 passed** (65 → 68, `tests/target_release/
test_target_release_gate.py` 68 `def test_` functions, counted). The
validator re-run: this tree exit 0 (41 active proposals — merging
`origin/main` `ac688c40` added one, `amend-register-act-5b-projection-proof`,
declaring `target_release: implemented` — 17 `implemented`, 3 a named
release, 21 named by the register, 0 outside); the same validator against a
fresh `origin/main ac688c40` clone exit 1, 40 active, 5 outside, naming the
same five carriers D2 already swept here (`add-composed-view-authoring`,
`add-cpc-clearing-boundary`, `add-lens-document-selection`,
`add-substantive-review-lane`, `register-gate-rules-council-seats`) —
unmoved, because main never received this packet's sweep and never will
until this packet lands.

### D8h — the bench's eighth round, on the D8g fix's own push: two threads, both TAKEN, and neither a re-litigation of D1–D3

A Copilot pass on the D8g merge-and-fix push (`08c4f5b9`) opened two more
threads, both stale prose rather than code, and neither reopens which OPTION
D1/D2/D3 recommends — the design is the owner's question and stays exactly as
it stood.

**(p) D3's RECORDED RELEASE-ID SHAPE WAS THE PRE-D8c PATTERN.** D3's own text
still read `^contract-v\d+\.\d+$` — two components only — while `RELEASE_ID_RE`
and the requirement's own scenario have admitted two OR three
(`^contract-v[0-9]+(?:\.[0-9]+){1,2}$`) since D8c (round 3), which fixed the
CODE and left D3's PROSE unfixed beside it. D3 now quotes the current pattern,
names it as `RELEASE_ID_RE`, and cites D8c for why it is two-or-three rather
than the narrower form it first read.

**(q) THE VALIDATOR'S BEFORE/AFTER RECORD IN `tasks.md` § 4.1 (AND ITS TWIN IN
`proposal.md`) HAD STOPPED MOVING.** Both pinned "before" to a frozen
`origin/main` `38c076d1` checkout and "after" to a count taken several rounds
ago (`39 active … 15 implemented`), while the packet's OWN authored
`design.md` D0 and the bench's own later rounds had long since moved past
that sha, and `origin/main` itself has since moved twice more (to `34bb5c71`,
then to `ac688c40`, D8g). Re-measured now, on THIS tree against a FRESH
`origin/main ac688c40` checkout: **41 active / 17 `implemented` / 0 outside**
here, **40 active / 11 `implemented` / 5 outside** there. **The lesson is the
same one D8e (l) already drew and this round re-learns: a before/after table
is a claim about TWO LIVE TREES, and pinning it to a sha is how it goes stale
the next time either tree moves.** Both `tasks.md` § 4.1 and `proposal.md`'s
own table are corrected to the current pair, with the delta now explained in
full: **+1** active is this packet's own `proposal.md` (`implemented`); **+6**
`implemented` is that same `+1` plus **+5** from the sweep (D2) — the five
carriers this pull request corrects are still `none`, and so still counted
`refused`, on `origin/main`, which has not received this packet's sweep and
will not until this packet lands. (This also corrects an inaccuracy in the
PREVIOUS freeze's own prose, carried since D8e: it described the delta
between its two rows as "`+1` active and `+1` `implemented`" while its own
table read 10 → 16 implemented, a `+6` — the same sweep contribution, unnamed.
Not a thread on this round; caught while re-deriving the explanation now
required to be correct.)

Neither thread touches `scripts/target_release.py`, the register, or any
test; `pytest tests/target_release -q` is unaffected (68 passed, unchanged).
Re-validated after both corrections: `openspec validate
gate-realization-axis-vocabulary --strict` exit 0; `validate-sequenced-after.py
. --ledger-diff` exit 0 (202 rows).

### D8i — the bench's ninth round, on the D8h push: two threads, one a real code escalation, one a naming nit, both TAKEN

A Copilot pass on the D8h push (`38cf0ec3`) opened two threads.

**(r) THE LEAF-DIRECTORY GUARD D8g ADDED CLOSED THE ESCAPE AT ONE COMPONENT
AND LEFT EVERY ANCESTOR OPEN.** `_registry_present` checked
`registry.is_symlink()` — the immediate `contracts/releases` component — but a
committed `contracts/` SYMLINK, one level further up, reaches the identical
escape through a `contracts/releases` that is a perfectly ordinary,
unsymlinked path: ordinariness is a property of the ONE component checked and
says nothing about what carried a reader there. The same class D8f closed at
the file and D8g closed at the leaf directory was still open at every
ancestor above the leaf.

**THE FIX REPLACES A PER-COMPONENT CHECK WITH A PER-PATH ONE.**
`_registry_present` no longer asks "is the registry directory itself a
symlink"; it asks whether resolving every symlink between `repo_root` and the
registry lands you back where a symlink-free tree would have put you —
`registry.resolve(strict=True) == repo_root.resolve(strict=True) /
RELEASE_REGISTRY_DIR`. This is not a second guard added beside D8g's; it
REPLACES it, and it SUBSUMES the leaf case D8g pinned (a symlinked `releases`
also fails the equality) rather than needing to be checked separately.
`repo_root` itself is resolved on BOTH sides, so ITS OWN symlink-ness cancels
out rather than being mistaken for an escape — a caller handing this module a
symlinked `repo_root` is trusting that path already, which is not the
vulnerability class the finding named; a test pins this boundary explicitly
so a future reader does not "fix" it into a false positive.

THREE tests: a symlinked `contracts/` (ancestor of the registry, holding a
genuine `releases/` and inventory beneath it) is treated exactly as absent,
the same as D8g's leaf case; `repo_root` itself being reached via a symlink
is NOT the escape and still resolves; and the two prior D8g tests (leaf
symlink absent, external contents grant no extra trust) are unchanged and
still pass, because the new check subsumes rather than replaces their
behaviour. Measured with the fix stashed (tests kept): the ancestor-symlink
test FAILS against the code as it stood (`(True, True)`, the same
over-trusting result D8g's own finding named one level down); the
repo-root-itself test PASSES unchanged either way, confirming it pins a
boundary rather than a regression. Restored: `pytest tests/target_release -q`
— **70 passed** (68 → 70).

**(s) A NEW TEST NAME CARRIED A TYPO.** D8g's
`test_a_symlinked_registry_directorys_contents_grant_no_extra_trust` — a
possessive apostrophe dropped in an identifier, not a word an identifier can
carry — renamed to
`test_a_symlinked_registry_directory_contents_grant_no_extra_trust`. No other
file cited the old name.

Neither thread reopens D1/D2/D3. Re-validated at the fix commit: `openspec
validate gate-realization-axis-vocabulary --strict` exit 0;
`validate-sequenced-after.py . --ledger-diff` exit 0 (202 rows);
`validate-target-release.py .` exit 0 (41 active, 0 outside); the same
validator against a fresh `origin/main ac688c40` clone exit 1 (40 active, 5
outside, the same five carriers).

### D8j — the bench's tenth round, one minute after the freeze and answered on the RATIFIED head: four threads, all four TAKEN

**NONE OF THE FOUR REOPENS D1, D2 OR D3**, and the round is recorded here
rather than folded into the ratification record because it is bench work, not a
decision: the ruling of 2026-09-12T15:45:19Z stands untouched by it.

**TWO WERE ALREADY ANSWERED BY THE RATIFICATION'S OWN RE-MEASUREMENT**, which
is worth saying rather than quietly ticking. (a) `tasks.md` § 4.6 still carried
a `39 active / 9 declaring` capture while § 4.1 read 41; it now reads **41
active / 11 declaring**, re-measured at the ratified head. (b) § 4.9 still said
the ledger held **200** rows while the tree held more; it now says **204**, the
figure `--ledger-diff` prints, with the seed's 200 named as the seed's. Both
are the same defect class D8e and D8h drew the lesson for — a figure that stops
moving when its tree does — and both are now anchored to a named head.

**THE THIRD IS A REAL CODE ESCALATION AND IT IS THE THIRD IN ITS FAMILY.**
`_proposals` found active declarations with a bare `Path.is_file()`, which
FOLLOWS SYMLINKS. So a committed `openspec/changes/<id>/proposal.md` symlink —
or an ordinary `proposal.md` inside a symlinked CHANGE DIRECTORY, or under a
symlinked `openspec/` — was read, judged and counted as the scanned tree's own
declaration, with `declaration()` opening bytes outside `repo_root`; and a
DANGLING link removed a proposal from the corpus the tree is judged on. D8g
closed this escape for the release registry's leaf, D8i closed it at every
ancestor, and **the discovery walk was the same surface all along, left open
because nobody had pointed a validator's reader at it.**

The fix is the D8i test, generalized rather than copied: a new `_unescaped`
helper returns a path only when resolving EVERY symlink between `repo_root` and
it lands where a symlink-free tree would have put it (`repo_root` resolved on
both sides, so a tree reached through a symlinked parent is not mistaken for
the escape), and `_proposals` — active and archived alike — takes every path
through it. `_registry_present` keeps its own body and its own docstring, which
now names the generalization; one helper, two callers, no second idiom.

FIVE tests (74 -> 79). THREE of them measured FAILING with the fix stashed and
passing with it restored: a symlinked active `proposal.md` (the case the bench
named), a regular proposal inside a symlinked change directory, and a symlinked
ARCHIVED proposal — an escape there is a lie about what the archive carries
rather than a false finding, and it is closed by the same call. The other TWO
pass either way and are pinned as BOUNDARIES rather than claimed as fixes: a
dangling link is skipped without crashing, and a `repo_root` that is itself
reached through a symlink still finds its proposals.

**ON THE REAL CORPUS THE FIX CHANGES NOTHING, WHICH IS THE POINT**: 41 active
proposals and 163 archived before and after, `validate-target-release.py .`
exit 0 on both sides of it. A guard that moved the live counts would be a
finding about this repository, not about the guard.

**THE FOURTH IS THE PULL REQUEST'S OWN DESCRIPTION**, which still reported 68
tests and stopped the bench at round 8. It is rebuilt on the ratified head, with
the ruling, the six-carrier sweep, this round, and the re-measured counts —
`refs #956, refs #931` kept and `closingIssuesReferences` re-verified `[]`
after.

### D8k — the bench's twelfth round, on the FREEZE push (16:45Z): one thread, TAKEN

**IT DOES NOT REOPEN D1, D2 OR D3**, and it is bench work recorded here for the
same reason D8g through D8j are: the ruling of 2026-09-12T15:45:19Z stands
untouched.

**A FOURTH MEMBER OF THE SAME SYMLINK-ESCAPE FAMILY, IN A FUNCTION THE FIRST
THREE NEVER TOUCHED.** `load_register` read the register — the default beside
this module, or one named on `--register` for a test tree or a consuming
repository — through a bare `path.is_file()` and `path.read_text()`, neither of
which this module's own established idiom permits any more: both FOLLOW
SYMLINKS, so a committed symlink at the register path would be read instead of
refused, and vary by runner, exactly the escape D8g (`resolves_as_release`'s
leaf), D8i (`_registry_present`'s ancestor walk) and D8j (`_proposals`'s
discovery walk, via `_unescaped`) each closed for a DIFFERENT reader. The
register was the one reader left open.

THE FIX IS A LEAF-LEVEL GUARD, NOT `_unescaped`'S ANCESTOR WALK, AND THAT IS A
DELIBERATE NARROWING, NAMED RATHER THAN LEFT IMPLICIT. `load_register`'s `path`
is not `repo_root`-relative the way a proposal or a release inventory is — it
is named directly, either as `REGISTER_PATH` (itself already resolved through
`Path(__file__).resolve()` at import, which collapses any ancestor symlink
between this module and its own directory) or as an arbitrary path a caller
gives, which may legitimately live anywhere a test tree or a consuming
repository puts it. The one hop neither case resolves is the LEAF itself — the
register file's own name, appended without a further `.resolve()` — so
`path.is_symlink()`, checked before `is_file()` or `read_text()` runs, closes
it; the check is UNCONDITIONAL on `path`, so it is the same guard for the
default argument and for one a caller supplies, and no branch can forget
either.

FIVE tests (79 -> **84**): a symlinked register refuses; one pointing outside
the tree refuses (`tmp_path_factory.mktemp`, D8g's own idiom); a DANGLING
register symlink refuses with the SAME message rather than crashing or
reporting "does not exist"; the DEFAULT argument is proved covered by patching
`load_register.__defaults__` (a function default binds once, at definition
time, so patching the module attribute `REGISTER_PATH` alone would never reach
a bare `load_register()` call); and the CLI surface (`--register PATH`)
reports the documented `exit 2` "register cannot be used" contract rather than
silently reading through the link. ALL FIVE measured FAILING with the fix
stashed and passing restored.

**ON THE REAL CORPUS THE FIX CHANGES NOTHING**: `validate-target-release.py .`
reads the same 42 active / 18 `implemented` / 3 a named release / 21 named by
the register / 0 outside, before and after — the house register is a regular
file, not a symlink, so the new guard has nothing to refuse there. Re-validated
at this fix: `openspec validate gate-realization-axis-vocabulary --strict` exit
0; `pytest tests/target_release -q` **84 passed**; `validate-sequenced-after.py
. --ledger-diff` exit 0 (205 rows); `validate-scope-globs.py .` exit 0;
`doc-health.py --single-repo .` exit 0; `proposal-support.py . verify` exit 0;
`validate-openspec-cli-pin.py --change gate-realization-axis-vocabulary` exit 0
(1 passed, 0 failed); `validate-openspec-cli-pin.py --all --no-cache` exit 0
(102 passed, 2 failed (104), unchanged — the two known
`disposition-codexfactory-*` exceptions); PATH 1.2.0 `--all --strict` 101
passed, 3 failed (104), unchanged; `pytest tests/doc-health -q` **7 failed,
1717 passed, 1 skipped** — the SAME local-only, pre-existing failure set
`tasks.md` § 3.19 measured on `fbe3ffac`, not this packet's and not moved by
it.

### D8l — the bench's thirteenth round, on the D8k push: one thread, TAKEN, and it does not reopen D1, D2 or D3

**THE CODE-SURFACE SUMMARY WAS ONE ROUND BEHIND THE CODE IT DESCRIBES.**
D8k's own fix grew `tests/target_release/test_target_release_gate.py` from
79 to 84 tests, but `proposal.md`'s `code_surface:` line — the thread's own
anchor, Copilot thread `PRRT_kwDOTAvnrs6hyDwH` — still read **79 tests**.
Measured on the flagged head: `grep -c '^def test_'` = 84; `pytest
--collect-only` collects 84.

Two places stated the stale total as a CURRENT figure and are corrected to
84: `proposal.md`'s `code_surface:` line, and the README `## OpenSpec
Records` row's own restatement of the same code surface (`... and 79
tests)`). Left alone, deliberately: `tasks.md` § 3.5, § 3.19 and § 3.20, and
this file's own D8j and D8k narrative, all state a count as a DATED
CHECKPOINT of what a specific round measured (74, then 79, then 84) — each
is true of its own moment and is not a claim about the file's CURRENT total,
so there is nothing to desynchronize there. `review/verification-2026-09-12.md`
is the dated capture `tasks.md` § 3.20 already says is deliberately not
rewritten for a later round.

Fixed, committed `34bc8cad`. `origin/main` moved TWICE while this one-line
round was being answered — `a72f0a76` (#978 `decide-disposition-reading-per-
family`, #998 `repoint-chain-anchoring-medxchain-citation`, #1005 a
`split-opendox` tasks.md amendment) and then, before the first merge's
push had even settled, `177ba819` (#981 `report-stale-grandfather-
dispositions`) — and both were taken as ordinary bookkeeping merges
(`db208513`, then `32e57bd7`), README's `## OpenSpec Records` conflicting
the identical way each time: the newer active row kept FIRST, verbatim,
this packet's row immediately after it, no other row touched and no reflow.

Re-validated at each head: `openspec validate gate-realization-axis-
vocabulary --strict` exit 0 throughout; `pytest tests/target_release -q`
84 passed throughout — this round and both merges are prose- and
bookkeeping-only, so the count does not move; `validate-target-release.py .`
exit 0, growing from 42 active / 18 `implemented` / 0 outside to 45 / 21 / 0
as main's own admitted changes landed; `doc-health.py --single-repo .` exit
0 at each head.

### D8m — the bench's fourteenth round, on the D8l push: two threads, both TAKEN, and neither reopens D1, D2 or D3

**(a) A FIFTH MEMBER OF THE SAME SYMLINK-ESCAPE FAMILY, AND THE FIRST IN THE
ANCESTOR DIMENSION FOR THE REGISTER.** Copilot thread `PRRT_kwDOTAvnrs6hyYeC`,
on `scripts/target_release.py`: D8k's leaf-level `path.is_symlink()` guard
covers only `load_register`'s own name. `linkdir/register.yaml`, where
`linkdir` is a symlink to an external directory, has an entirely ORDINARY
leaf — `register.yaml` itself is a regular file, so `path.is_symlink()` is
False — and the leaf-only guard passed it while `read_text()` still followed
`linkdir` and read bytes from wherever it points.

THE FIX GENERALIZES THE SAME TEST `_unescaped` USES, WITHOUT THE ANCHOR
`_unescaped` HAS. A new `_has_symlinked_ancestor(path)` helper climbs `path`'s
own ancestors one directory at a time, refusing if any is a symlink,
stopping at `/` for an absolute path or at `.` for a relative one — there is
no `repo_root` to check "outside of" the way `_unescaped` checks outside
`repo_root`, because a register named on `--register` is deliberately
allowed to live anywhere a test tree or a consuming repository puts it
(`load_register`'s own docstring says so, and the CLI's `--register` and
`repo_root` positional argument are independent — a register legitimately
outside `repo_root`, reached by an ordinary unsymlinked path, must keep
working). `load_register` now refuses on `path.is_symlink() or
_has_symlinked_ancestor(path)`, before `is_file()` or `read_text()` runs,
unconditional on `path` — the same guard whether `path` is the default
argument or one a caller supplies, matching D8k's own discipline.

TWO tests (84 -> **86**), both measured FAILING with the fix stashed and
passing restored: the direct call (`linkdir` symlinked to a directory
outside `tmp_path`, an ordinary `register.yaml` inside it) and the CLI
(`--register`) surface end to end, `exit 2`. On the real corpus the fix
moves nothing — the house register sits directly beside this module with
no symlinked ancestor anywhere between it and the filesystem root.

**(b) THE PULL REQUEST'S OWN DESCRIPTION, A THIRD TIME.** Copilot thread
`PRRT_kwDOTAvnrs6hybFv`, on `README.md` but naming the PR body directly: the
live description still reported 70 tests in its implementation summary and
79 passed in later verification, both behind the committed 86 — the same
class of defect D8j's item (d) and D8l already closed once each, recurring
because the description is GitHub metadata and not a tracked file a merge or
a grep sweep reaches. Rebuilt on this head with the current figures;
`refs #956` kept, `closingIssuesReferences` re-verified `[]`.

Re-validated: `openspec validate gate-realization-axis-vocabulary --strict`
exit 0; `pytest tests/target_release -q` **86 passed**; `validate-target-
release.py .` exit 0 (45 active, 45 declaring, 21 `implemented`, 3 a named
release, 21 registered, 0 outside, unchanged — an I/O-boundary-only fix);
`validate-sequenced-after.py . --ledger-diff` exit 0 (208 rows);
`validate-scope-globs.py .` exit 0; `doc-health.py --single-repo .` exit 0;
`proposal-support.py . verify` exit 0; `validate-openspec-cli-pin.py
--change gate-realization-axis-vocabulary` exit 0 (1 passed, 0 failed);
`--all --no-cache` exit 0 (102 passed, 2 failed (104), the two known
`disposition-codexfactory-*` exceptions, unchanged).
