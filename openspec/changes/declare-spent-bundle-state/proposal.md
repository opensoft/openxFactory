---
code_surface: openxFactory (`scripts/doc_health/release_tag_publication.py` — one new pure reader over `contracts/CHANGELOG.md` and the accept/refuse ladder over its result, plus the two new emits; the module already owns its severity and action constants and this adds to them. `tests/doc-health/test_release_tag_publication.py` — the ten new scenarios arrive as new tests over the same real-git fixtures the file already builds, and `test_this_repository_reads_zero_and_the_probe_can_fire` goes GREEN as a consequence rather than by being edited. `contracts/CHANGELOG.md` — ONE reserved declaration line written into the `contract-v2.6` disposition subsection `contract-v3.0`'s entry already carries; it is an EDITORIAL release member, which is what makes it writable between cuts. `docs/doc-health.md` — the family's row and action line gain the third state. NO change to `Finding`, to `report.render`, to the finding or ranked-plan grammars, to `health/dispositions.yaml` or its readers, to the threshold, to the enforcement floor, to `release-inventory-drift`, to `verify_tag`, or to any other family. AND NO CHANGE TO `contracts/manifest.yaml`, `contracts/releases/contract-v2.6.digests.yaml` OR THE `contract-v2.6` CHANGELOG ENTRY — the family's own action text forbids editing the manifest, the changelog entry or the inventory to match an absence, and this change obeys it: nothing is deleted to make a check pass.)
target_release: implemented — the openxFactory main line. This surface cuts no contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed by it, so the archive gate is merge-plus-green in the shape `add-release-tag-publication-check` and `add-family-enumeration-check` both used. ONE PART OF THE INTENT IS DELIBERATELY DEFERRED TO THE NEXT BUNDLE AND IS NOT SMUGGLED IN HERE: the obligation-side statement of the SPENT state belongs in `docs/contract-versioning-policy.md`, which is a NON-EDITORIAL member of `contracts/releases/contract-v3.0.digests.yaml`, so editing it between cuts would raise a `release-inventory-drift` ERROR on `main` — trading the red this change exists to clear for a different red. See OD-6; the policy paragraph rides the next contract cut and the delta is written so that nothing here depends on it having landed.
Status: draft
Proposed: 2026-09-02
Origin: openxFactory issue #575, filed by the `contract-v3.0` cut (#573) at the moment it met the defect, rather than after. Commissioned in session by Brett Heap on 2026-09-02, relayed to the authoring session verbatim as **"Merge now, fix #575 next"** — an authorization to AUTHOR THE FIX, covering nothing below it. Every design decision in § Orchestrator Decisions is the authoring session's and is flagged for veto.
---

# Proposal: declare-spent-bundle-state

## Why

**The family is right, the finding is true, and the state does not exist.**

`scripts/doc_health/release_tag_publication.py` inspects every bundle carrying a
release inventory, not only the declared one — the amendment Codex forced onto
PR #544, and the reason the family catches the recurrence it was built for. It
has exactly two answers for a bundle: *published*, or *owes a tag*. There is no
third.

`contract-v2.6` is the third. It was **declared** at `bbbbeda9` (PR #565) by
three artifacts — the manifest's `contract_bundle_version`, its changelog entry,
and `contracts/releases/contract-v2.6.digests.yaml`. It is **never verifiable**:
`verify-commit --commit bbbbeda9` returns five `HGR-RELEASE-DIGEST-MISMATCH`
findings, because the cut branch forked at `518c670b` and was never rebased over
`a951be76` (#562) and `6856f502` (#564), so the squash landed five release
members the reviewed candidate never saw — three of them a normative schema, the
versioning policy itself and a validator, none of which the between-cuts
editorial allowance reaches. And it is **never publishable**: the targeting rule
is *"the EARLIEST FIRST-PARENT COMMIT on published `main` that DECLARES the
bundle and at which `verify-commit` PASSES"*, exactly one first-parent commit
declares the bundle, and `verify-commit` fails there. A completion commit could
have supplied a digest target and would still not have cured the second defect:
`contract-v2.6` declares change class **ADDITIVE (minor)** over a tree that
refuses three shapes `contract-v2.5` accepted, and no rebuilt inventory moves a
change class.

**The measurement of record is PR #565 comment `5502452624`.** This proposal
cites it and does not re-derive it, because two records of one measurement is how
they drift apart.

**Brett Heap ruled it on 2026-09-02, in session, verbatim as quoted in issue
#575: "Supersede: v3.0 is the completion."** `contract-v3.0` was cut on that
ruling and merged as `ff9ed815` (PR #573), and its tag `59f4f51f` is published
and peels to that commit.

**What the ruling did not say is the reason this packet exists.** It ruled that
`contract-v3.0` supersedes `contract-v2.6`. It did not rule that a checker should
stop objecting to abandoned bundles. So the cut declared the collision in
`contracts/CHANGELOG.md` § *`contract-v2.6` disposition* and filed it as #575
rather than relaxing the check inside a release cut — *"a release cut quietly
relaxing the one check that exists to stop bundles being walked away from is
precisely the failure that check was built for"*. That refusal is what this
change is written to honour rather than to undo.

**The cost of the gap, today, on `main`.** Since `ff9ed815`, `check_repo`
reports `contract-v2.6` at **`error` without grading** — *"cut and SUPERSEDED
without ever being published"* — and
`tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire`
is **RED on `main`**. Measured on this packet's merge base: 18 passed, 1 failed,
the failure being exactly that test and exactly that finding. The prescribed
action — *"publish the annotated tag retrospectively at the commit the versioning
policy's rule identifies"* — is unperformable for this bundle by anyone, and a
finding whose only action cannot be taken is one that teaches its readers to stop
reading the report.

## What changes

**ONE `## MODIFIED Requirements` block over the family's own canon requirement,
`Release-tag publication` in `openspec/specs/doc-health/spec.md`.** No new
requirement, no new family, no new capability. The requirement gains a THIRD
STATE — SPENT — that is entered only by an explicit declaration and refused by
every absence.

The shape, in one paragraph. A superseded, untagged bundle may be declared SPENT
by a reserved single-line declaration in `contracts/CHANGELOG.md`, written inside
the changelog entry of the bundle that superseded it, naming the superseding
bundle, the cause, the ruling that disposed it and the measurement of record.
Where all four elements are present and the superseding bundle is itself cut AND
itself published, the family emits ONE `info` on `contracts/CHANGELOG.md` — the
state is recorded, not silent — and the `error` for that bundle goes away. Where
the successor is cut but not yet published, the supersession is unproven and the
family `warning`s. Where the successor was never cut, where an element is
missing, where two declarations name one bundle, where the declaration sits
outside its successor's entry, or where it names the bundle the manifest still
declares, the family `error`s and accepts nothing. **Where there is no
declaration at all, the family behaves exactly as it does today.**

**The delta is SCENARIO-COMPLETE and was verified mechanically, not by eye.**
OpenSpec's `MODIFIED` replaces a requirement wholesale, and this requirement
carries eleven promoted scenarios and sixty-seven body lines. The block was
BUILT FROM CANON by splicing at named anchors rather than retyped, and checked
scenario-by-scenario: **11 of 11 canon scenarios present, 10 byte-identical, and
the eleventh — *A bundle was cut, superseded, and never tagged* — differing by
exactly ONE added `AND` bullet and nothing removed**, with all 67 canon body
lines surviving. That is the #331/#329 loss shape, and it is checked rather than
asserted. **Ten scenarios are added**, bringing the requirement to twenty-one.

**NO `## MODIFIED` BLOCK IS OPENED OVER `Deterministic check families`**, and
that is a measurement rather than a shortcut — see OQ-1.

## Orchestrator Decisions — flagged for veto

Brett's commissioning covers authoring a fix for #575 and nothing below. All
eight of these are the authoring session's, and each names its alternative.

**OD-1 — THE RECORD IS `contracts/CHANGELOG.md`, NOT `health/dispositions.yaml`.
Mechanical, not preferred.** Issue #575 § 3 raised the dispositions file as a
candidate and raised one objection to it (it lives at the aggregation root, out
of reach of a consumer reading a pinned policy). There are two more, and either
alone is decisive:

* **It cannot name one bundle.** `promotion_fidelity.load_dispositions` keys
  entries by `(family, repo, path)`, and EVERY finding this family raises lands
  on `contracts/manifest.yaml` (`_finding` passes `MANIFEST` for all of them). A
  row disposing `contract-v2.6` would dispose **every finding this family could
  ever raise about openxFactory**, including the next genuinely abandoned bundle.
  A mechanism whose granularity is "the whole family, forever" is not a
  disposition of one bundle; it is the check being switched off with a citation
  attached.
* **It is invisible in the scope that measures this.** That loader's own
  docstring records the caveat: the file lives at the aggregation root and
  *"a `--single-repo` self-gate run has no aggregation root, so no disposition
  applies in that scope"*. The red test is a `--single-repo` self-gate. A
  dispositions row would not clear it, so it would not even be the smaller fix.

The changelog is picked positively as well as by elimination. It is a member of
every release digest inventory, so the record travels with the bundle a consumer
pins. It is one of the **three editorial members** (`contracts/CHANGELOG.md`,
`contracts/manifest.yaml`, `contracts/README.md`) the versioning policy allows to
move between cuts — which, as OD-6 records, is what makes it the *only* release
member a between-cuts disposition can be written to at all. And it is already
where this estate records supersessions twice over: `contract-v2.3`'s disposition
sits in `contract-v2.4`'s entry, and `contract-v2.6`'s already sits in
`contract-v3.0`'s. **Not both mechanisms.** Two places to declare one fact is two
places for them to disagree.

**OD-2 — A RESERVED SINGLE-LINE MARKER INSIDE THE EXISTING SUBSECTION, NOT A
FREE-PROSE READ.** The alternative was to key on the disposition subsection's
existing heading and prose. Rejected: a deterministic family whose behaviour
depends on how a sentence was phrased is a family nobody can predict from its
spec, and its findings would move when an editor rewrote a heading. The form is
`**SPENT BUNDLE:** \`<bundle>\` — SUPERSEDED BY \`<successor>\` — CAUSE: <text> —
RULED BY <author>, <YYYY-MM-DD> — MEASUREMENT: <citation>`, and the opener is
reserved. This follows `document-lifecycle`'s reserved `Modified over` marker
exactly: **a handle on the record, not a second record**, written inside the
human disposition subsection the cut writes anyway.

**OD-3 — A CORRECTLY DECLARED SPENT BUNDLE IS AN `info`, NOT SILENCE.** Issue
#575 § 3 put these as the two candidates. `info` is chosen for three reasons.
This family already carries `info` for exactly this purpose — a skip is
*"reported, not dropped"* — so the vocabulary is the family's own. A reader who
finds `contracts/releases/contract-v2.6.digests.yaml` with no matching tag is
owed the answer where they are looking. And **an `info` has a finding key, which
silence does not** — see OD-5, which is the argument that actually decides it.
The cost is honest and is the enforcement floor's own argument turned back:
`info` is a permanent finding nobody can act on. It is accepted because there is
ONE of them in the estate's history and the requirement forbids there being a
second by retrofit; if Brett prefers silence, the veto is here, and the change is
scenario 1 emitting nothing plus OD-5 losing its subject.

**OD-4 — THE UNPUBLISHED-SUCCESSOR CASE IS A `warning`: NOT SILENCE, NOT AN
ERROR. This is the guard, and it is the answer to #575 § 4.** A bundle must not
become spent by being ignored, and the strongest available guard is not a rule
about who may write a sentence — it is that **the only way to make a bundle
quiet is to publish its successor's tag**, which is the very act this family
exists to compel. A repository that walks away from a bundle by declaring it
spent has moved the obligation onto the successor, where the same check meets it
again. `warning` rather than `error` because the successor's own declare-then-tag
interval is legitimate — the premise of the whole distance grading — and because
the successor is separately graded on its own account, so nothing is lost.
`warning` rather than silence because a declaration whose successor is not
published is a claim not yet evidenced, and this family does not accept claims.

**OD-5 — THE SPENT FINDINGS LAND ON `contracts/CHANGELOG.md`, AND THE `info` IS
`contested`.** Every existing finding of this family lands on
`contracts/manifest.yaml`. The spent findings deliberately do not, and the reason
is the finding key: `Finding.match_key()` is `(family, repo, path)`, so a spent
`info` on the manifest would be indistinguishable from any other finding of this
family about this repository, and its disappearance would be masked by any
sibling finding on the same path. Landed on the document that carries the
declaration, it gets its own key — and classed `contested`, its disappearance
without a cited change becomes an `uncited-resolution` ERROR. That closes the
one abuse a changelog-read is otherwise open to: **deleting
`contracts/releases/contract-v2.6.digests.yaml` would remove the bundle from
`cut_bundles` and take the whole finding with it**, which is precisely the *"never
edit the manifest, the changelog or the inventory to match the absence"* this
family already prescribes. `promotion_fidelity` lands its findings on the delta
rather than the spec for the same reason, in the same words: the finding belongs
on the document making the claim.

**OD-6 — THE POLICY-SIDE STATEMENT RIDES THE NEXT CONTRACT CUT AND IS NOT
LANDED HERE.** This is the one constraint #575 did not anticipate, and it is
worth stating plainly because it cuts against the issue's own preference. Issue
#575 § 3 argues that *"a state readable from the release surface itself is
stronger"*, and it is right — but the release surface is not uniformly writable.
`docs/contract-versioning-policy.md` is artifact `docs-contract-versioning-policy.md`
in `contracts/releases/contract-v3.0.digests.yaml` and is **not** one of the
three editorial members, so editing it between cuts raises a
`release-inventory-drift` **ERROR** (*"member digest differs"*, non-editorial),
while editing `contracts/CHANGELOG.md` raises an **INFO** the family itself
labels *"editorial member — expected between cuts"*. A packet that cleared one
`error` on `main` by creating another would not be a fix. So the obligation-side
paragraph — the versioning policy naming SPENT as a state, beside § *Immutable
Tag Correction* whose *"its version number is never reused"* the disposition
already leans on — is owed at the next bundle, is written into tasks as an owed
item rather than a wish, and **nothing in the delta depends on it having
landed**. The alternative — hold this packet until a cut is due — was rejected:
it leaves `main` red for an unbounded interval to satisfy a sequencing
preference, and the ordering is recoverable while the redness is not.

**OD-7 — ONE MODIFIED BLOCK OVER THE FAMILY'S OWN REQUIREMENT, NOT A NEW
REQUIREMENT AND NOT A NEW FAMILY.** The archived packet's D1 chose a new
requirement over a MODIFIED block on `Release-inventory drift`, on a stated
structural test: *"a tag finding is not resolved by a cut … folding it in would
falsify the sentence that justifies the family's resolution class."* **That same
test answers the other way here.** A spent state IS resolved by the act
`Release-tag publication` already owns — publication, of the successor's tag — so
it belongs inside that requirement and nowhere else. D1's second reason, that a
MODIFIED delta risks the scenarios it restates, is answered by measurement
rather than by avoidance: the restatement is verified 11-of-11 above.

**OD-8 — PROPOSAL ONLY. THE REALIZATION IS A SEPARATE PR, GATED ON
RATIFICATION.** The tempting alternative is #544's shape, which landed this
family's delta, module and tests in ONE commit. **That was a ruling with a
mechanical reason, and the reason does not transfer.** Brett ruled one landing
there because a family ADDITION reddens `family-enumeration`'s self-gate for the
whole interval between delta and registry — *"a family addition is one landing in
this estate"*. This change adds no family and moves no count, so no gate is red
in the interval and no forcing function exists. Three things say to split:

1. **The v3.0 cut said so, in the entry this packet answers**: the shape of this
   vocabulary — *"what record counts as a supersession, who may declare one,
   whether it is `contested` and needs a disposition entry"* — is *"design work
   that owes its own change and its own review"*. All three of those questions
   are OD-1, OD-2/OD-4 and OD-5. Answering them and executing them in one PR is
   the review this sentence asks for not happening.
2. **The family's own precedent for an amendment.** When Codex's P1 changed the
   ratified requirement's text, the packet recorded it *"as an amendment awaiting
   Brett rather than absorbed into the realization, because the ratified baseline
   named a delta and this is not that delta"*. This is the same act, one level
   up: an amendment to PROMOTED CANON.
3. **What is being amended is a fail-closed check.** A session that both designed
   and shipped a relaxation of the one check that stops bundles being walked away
   from would be doing, more slowly, what the cut refused to do quickly.

`main` stays red for one more PR. That redness is **declared, named and
inherited** — #575 exists so that *"a reader meeting the ERROR knows it is
DECLARED rather than undiscovered"* — and one more PR of a declared red is a
smaller harm than an unratified relaxation of the check that declared it.

## Open questions — carried, not decided

**OQ-1 — the `Deterministic check families` document-set sentence is ALREADY
STALE, and this packet does not repair it. Recommendation: leave it to the next
packet that restates that requirement.** Canon says *"The release-tag publication
family reads the DECLARED BUNDLE and the repository's PUBLISHED TAG REFS — a
manifest field and a set of git refs"*. That was true of the family as ratified
and stopped being true at its own accepted amendment: `cut_bundles` reads
`contracts/releases/` through `ls_tree_paths`, and the sentence was never moved.
This change adds a third input (`contracts/CHANGELOG.md`) to a sentence that
already omits the second. **The staleness is inherited, not introduced**, the
sentence's operative conclusion — *"neither the governed corpus nor the lifecycle
scan set … moves no census, word count, canon-share figure, inventory entry, or
catalog record"* — remains exactly true of all three inputs, and no check reads
the input enumeration (`family-enumeration` reads the family NAMES and the three
COUNTS). Opening a second MODIFIED block over an eight-scenario requirement with
four appended historical restatement notes, to repair another change's omission,
is a different change's work and would put those scenarios at risk for a
sentence nothing measures. Named here so it is a disclosure rather than a
discovery, and every packet that adds a family restates that requirement anyway.

**OQ-2 — should the reserved marker be lifted into a schema-backed artifact
later?** Recommendation: no, and revisit only if a second spent bundle ever
exists. A reserved prose marker in an editorial member is writable between cuts;
a schema-backed artifact under `contracts/` is a contract-surface change that
needs a bundle, which is the trap OD-6 describes. One instance does not earn a
schema.

**OQ-3 — does `uncited_resolutions` behave as OD-5 assumes for an `info`?** It
is severity-agnostic as written (`report.py:394-438` iterates
`previous_contested` with no severity test), so the assumption reads sound, but
it has never been exercised by a contested `info`. The realization proves it with
a test rather than inheriting it; if it turns out severity-gated somewhere in
`parse_previous`, OD-5's class choice returns as a question rather than being
quietly dropped.

## What this reports, measured

On the merge base (`ff9ed815`), `pytest tests/doc-health/test_release_tag_publication.py`:
**18 passed, 1 failed** — `test_this_repository_reads_zero_and_the_probe_can_fire`,
on the one `error` naming `contract-v2.6`. That is the inherited red this packet
is about, and this PR does not clear it: OD-8 defers the code.

**What the proposal itself moves while it sits unratified: NOTHING, and that is
measured rather than predicted.** A `--single-repo` run with and without this
packet, same clock, in the shape the family's own packet used:

| | critical | error | warning | info |
|---|---|---|---|---|
| base (`ff9ed815`, a detached worktree) | 6 | 5 | 29 | 12 |
| head (this packet committed) | 6 | 5 | 29 | 12 |

**The two reports are BYTE-IDENTICAL** once the repo-identity string is
normalized — not merely equal in the four counts, but equal line for line, so no
finding moved from one family to another and no census, word count, canon-share
figure or catalog record moved either. Three of those zeroes were checked rather
than assumed:

* **`family-enumeration`: no findings.** This packet adds no family and moves no
  count, which is the whole of OD-8's mechanical argument. This is the difference
  between it and #544, which reddened that gate three times over the same
  interval.
* **`modified-block-currency`: `scenario-title completeness: 0`** — the arm
  carrying that family's gate — and the carriage ledger unchanged at 8. The
  family's own reader agrees with the scenario-by-scenario verification above.
* **The census is unmoved because it should be.** `proposal.md` sits in the
  LIFECYCLE SCAN SET (`corpus.LIFECYCLE_SCAN`), not the governed corpus, and the
  requirement `Deterministic check families` states in terms that no census,
  word count or canon-share figure *"SHALL … move because the lifecycle scan set
  exists"*. `status-validity` reads that set and reports no findings, which is
  the `Status: draft` header being accepted.

The one `error` that does NOT move is the point: `release-tag-publication`
reports `contract-v2.6` at `error` in both runs, in the same words. **This
packet describes the fix and performs none of it.**

**What the realization will move, when it lands**: the one `error` becomes one
`info`, and `contracts/CHANGELOG.md` gains a `release-inventory-drift` `info`
labelled *"editorial member — expected between cuts"* until the next cut
re-baselines the inventory. Net on `main`: **-1 `error`, +2 `info`**, and the
self-gate goes green because the estate stopped having an unanswerable finding,
not because a test was edited.

## Non-goals

* **Publishing or fabricating a tag for `contract-v2.6`.** It has no legal
  target and the number is never reused. This change gives the absence a name;
  it does not fill it.
* **Editing the manifest, the `contract-v2.6` changelog entry, or its digest
  inventory.** They are the record of what was declared and of what was true when
  it was written, and the family's own action text forbids editing them to match
  an absence.
* **Relaxing anything else.** The threshold stays five, the enforcement floor
  stays `contract-v1.7`, the two failure classes keep their different words, and
  the distance grading of the declared bundle is untouched.
* **Retrofitting the five instances** the policy records under § *Untagged
  Bundles After Enforcement Began* (#575 § 5). All five were publishable and all
  five were published; the requirement says so and forbids reading the state
  backwards.
* **Fixing #338**, or building on `verify_tag`. D5 stands unchanged.
* **Touching `health/dispositions.yaml` or its readers** (OD-1).
