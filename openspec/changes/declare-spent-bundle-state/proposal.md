---
code_surface: openxFactory (`scripts/doc_health/release_tag_publication.py` — one new pure reader over `contracts/CHANGELOG.md` and the accept/refuse ladder over its result, plus the two new emits; the module already owns its severity and action constants and this adds to them. `tests/doc-health/test_release_tag_publication.py` — the ten new scenarios arrive as new tests over the same real-git fixtures the file already builds, and `test_this_repository_reads_zero_and_the_probe_can_fire` goes GREEN as a consequence rather than by being edited. `contracts/CHANGELOG.md` — ONE reserved declaration line written into the `contract-v2.6` disposition subsection `contract-v3.0`'s entry already carries; it is an EDITORIAL release member, which is what makes it writable between cuts. `docs/doc-health.md` — the family's row and action line gain the third state. NO change to `Finding`, to `report.render`, to the finding or ranked-plan grammars, to `health/dispositions.yaml` or its readers, to the threshold, to the enforcement floor, to `release-inventory-drift`, to `verify_tag`, or to any other family. AND NO CHANGE TO `contracts/manifest.yaml`, `contracts/releases/contract-v2.6.digests.yaml` OR THE `contract-v2.6` CHANGELOG ENTRY — the family's own action text forbids editing the manifest, the changelog entry or the inventory to match an absence, and this change obeys it: nothing is deleted to make a check pass. ONE FILE IS TOUCHED BY THE PROPOSAL PR AND IS NOT PART OF THIS SURFACE, disclosed rather than folded in: `tests/sequenced_after/test_sweep.py` carries the LIVE corpus pin, and authoring an active change that carries a MODIFIED block moves `co_modified` 104 → 105, `active_co_modified` 18 → 19 and `change_ids - 1` 152 → 153. That pin's own protocol is that it "MOVES WITH the corpus … in the SAME COMMIT", with a dated MOVEMENT LOG entry saying which subject moved and why, so it is corpus BOOKKEEPING rather than realization — and the three counts it does NOT move (`sole_modifiers`, `active_sole`, `declaring`) are asserted unchanged, which is what rules out a change adding itself to two populations at once.)
target_release: implemented — the openxFactory main line. This surface cuts no contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed by it, so the archive gate is merge-plus-green in the shape `add-release-tag-publication-check` and `add-family-enumeration-check` both used. ONE PART OF THE INTENT IS DELIBERATELY DEFERRED TO THE NEXT BUNDLE AND IS NOT SMUGGLED IN HERE: the obligation-side statement of the SPENT state belongs in `docs/contract-versioning-policy.md`, which is a NON-EDITORIAL member of `contracts/releases/contract-v3.0.digests.yaml`, so editing it between cuts would raise a `release-inventory-drift` ERROR on `main` — trading the red this change exists to clear for a different red. See OD-6; the policy paragraph rides the next contract cut and the delta is written so that nothing here depends on it having landed.
Status: ratified
Proposed: 2026-09-02
Ratified: 2026-09-02 by Brett Heap (openxFactory repository owner) — in session, in TWO ACTS over the two decisions this proposal declined to take by silence. First, on PR #578: **OD-3 ACCEPTED as proposed** (a correctly declared spent bundle emits an `info` with its own finding key, not silence) and **OD-4 ACCEPTED as proposed** (an unpublished successor is a `warning`; quiet only once the superseding bundle's tag is published; `error` where the named successor was never cut). Then the ratification of the packet on that basis. Record: `review/ratification-2026-09-02.md`. **RATIFICATION AUTHORIZES REALIZATION AND PERFORMS NONE OF IT** — no checker line, no test and no changelog declaration lands in the ratifying commit; that is the next PR, and OD-8 is why.
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
Where all four elements are present and the superseding bundle is itself cut,
itself published, AND STRICTLY LATER (OD-9), the family emits ONE `info` — the
state is recorded, not silent — and the `error` for that bundle goes away. **The
`info`, and every other finding this state raises, lands on that bundle's OWN
release inventory, `contracts/releases/<bundle>.digests.yaml`, and NOT on
`contracts/CHANGELOG.md`** — OD-5 as amended, because a finding's identity is
`(family, repo, path)` and a shared path would let one spent bundle's removal
hide behind another's surviving finding. Where the successor is cut but not yet
published, the supersession is unproven: the family emits ONE `warning` and
SUPPRESSES the superseded `error` for that bundle, this state being PROVISIONAL
rather than refused, and the successor is graded on its own account so the
obligation has moved rather than gone. Where the successor was never cut, where
it is not later than the bundle it supersedes, where an element is missing,
where two declarations name one bundle, where the declaration sits outside its
successor's entry, or where it names the bundle the manifest still declares, the
family `error`s and accepts nothing — and the superseded `error` stands alongside
it, so a bad declaration removes nothing. One finding keeps the changelog path
because it has no bundle inventory to land on: a declaration whose SUBJECT was
never cut disposes nothing and is a `warning` there. **Where there is no
declaration at all, the family behaves exactly as it does today.**

**The delta is SCENARIO-COMPLETE and was verified mechanically, not by eye.**
OpenSpec's `MODIFIED` replaces a requirement wholesale, and this requirement
carries eleven promoted scenarios and sixty-seven body lines. The block was
BUILT FROM CANON by splicing at named anchors rather than retyped, and checked
scenario-by-scenario: **11 of 11 canon scenarios present, 10 byte-identical, and
the eleventh — *A bundle was cut, superseded, and never tagged* — differing by
exactly ONE added `AND` bullet and nothing removed**, with all 67 canon body
lines surviving. That is the #331/#329 loss shape, and it is checked rather than
asserted. **Thirteen scenarios are added**, bringing the requirement to
twenty-four — ten as first proposed, and three more for the two Codex P1s
§ Review convergence records.

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

**OD-3 — RULED 2026-09-02: ACCEPTED AS PROPOSED. A CORRECTLY DECLARED SPENT BUNDLE IS AN `info`, NOT SILENCE.** Issue
#575 § 3 put these as the two candidates. `info` is chosen for three reasons.
This family already carries `info` for exactly this purpose — a skip is
*"reported, not dropped"* — so the vocabulary is the family's own. A reader who
finds `contracts/releases/contract-v2.6.digests.yaml` with no matching tag is
owed the answer where they are looking. And **an `info` has a finding key, which
silence does not** — see OD-5, which is the argument that actually decides it.
The cost is honest and is the enforcement floor's own argument turned back:
`info` is a permanent finding nobody can act on. It is accepted because there is
ONE of them in the estate's history and the requirement forbids there being a
second by retrofit. **The veto was available and was not exercised**: Brett
ruled on PR #578, verbatim, that *"a correctly declared spent bundle emits `info`
with its own finding key, not silence"*, because *"the reader who finds
`contracts/releases/contract-v2.6.digests.yaml` with no matching tag is owed the
answer where they are looking, and the key is what makes the one permanent
finding auditable"*. The ruling names the finding key as its reason, which is
OD-5's subject, and OD-5 has since been strengthened on a Codex finding — see
there.

**OD-4 — RULED 2026-09-02: ACCEPTED AS PROPOSED. THE UNPUBLISHED-SUCCESSOR CASE
IS A `warning`: NOT SILENCE, NOT AN ERROR. This is the guard, and it is the
answer to #575 § 4.** A bundle must not
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
**Brett ruled it on PR #578**, verbatim: *"quiet only once the superseding
bundle's tag is published, `warning` while it is cut but untagged, `error` where
the named successor was never cut. The only way to make a bundle quiet is to
publish its successor's tag."*

**AND THE GUARD AS RULED WAS INCOMPLETE, WHICH CODEX FOUND AND THIS PROPOSAL
REPAIRED RATHER THAN FILED — see OD-9.** Cut-and-published does not imply LATER,
and an earlier already-published bundle satisfies it.

**OD-5 — AMENDED ON A CODEX FINDING, 2026-09-02. THE SPENT FINDINGS LAND ON THE
BUNDLE'S OWN RELEASE INVENTORY — `contracts/releases/<bundle>.digests.yaml` —
AND THE `info` IS `contested`.** Every existing finding of this family lands on
`contracts/manifest.yaml`. The spent findings deliberately do not, and the
reason is the finding key: `Finding.match_key()` is `(family, repo, path)` and
ignores the rule text, so a spent `info` on the manifest would be
indistinguishable from every other finding of this family about this repository
and its disappearance would be masked by any surviving sibling.

**AS FIRST PROPOSED THIS DECISION SAID `contracts/CHANGELOG.md`, AND CODEX SHOWED
THAT IS THE SAME DEFECT ONE STEP OVER** (PR #578, P1 on the ratified shape of the
delta): two bundles legitimately declared spent would share THAT path too, so
removing one declaration while the other stood would leave the shared key present
in the current set and `uncited_resolutions()` would raise nothing — exactly the
per-state disappearance detection this decision promises. The repair is the
per-bundle inventory, which is unique to the bundle BY CONSTRUCTION: it is the
artifact whose existence made the bundle enumerable in `cut_bundles` in the first
place, so a path always exists for any bundle this state can reach. Classed
`contested`, its disappearance without a cited change then becomes an
`uncited-resolution` ERROR per bundle, which closes the one abuse a
changelog-read is otherwise open to: **deleting
`contracts/releases/contract-v2.6.digests.yaml` would remove the bundle from
`cut_bundles` and take the whole finding with it**, which is precisely the *"never
edit the manifest, the changelog or the inventory to match the absence"* this
family already prescribes. `promotion_fidelity` lands its findings on the delta
rather than the spec for the same reason, in the same words: the finding belongs
on the document making the claim. **ONE finding of this state has no per-bundle
inventory to land on and stays on the changelog**: a declaration whose SUBJECT is
a bundle this repository never cut disposes nothing, and is reported at `warning`
there — a mistyped subject leaves the real bundle undeclared and still reported,
which is the fail-closed behaviour a typo must not defeat.

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

**AND THE PREDICTION HAS SINCE COME TRUE ON `main`, FROM ANOTHER LANE — measured
after the fact, not claimed in advance.** PR **#577** (merged `2898b104`,
2026-09-02) recorded `contract-v2.6`'s supersession in
`docs/contract-versioning-policy.md` — instance SIX in § *Untagged Bundles After
Enforcement Began* — which is exactly the between-cuts edit to a non-editorial
inventory member this decision declined to make. `release-inventory-drift` now
reports, over `main`: **`[error] docs/contract-versioning-policy.md — bytes
differ from the digest 'contract-v3.0' records`**. The analysis is therefore
vindicated and its arithmetic is overtaken in the same breath: **the drift error
exists already, so the INCREMENTAL cost of adding the SPENT-state paragraph to
that same file is now ZERO, and it clears at the same next cut either way.** This
proposal does not rewrite its own decision retroactively — the decision was
right when taken and its reason is preserved above — but tasks § 3.1 records the
new arithmetic, and the routing of the paragraph is the realization's to take
with that measurement in hand rather than this proposal's to pre-empt. **What
#577 DOES discharge** is the consumer-facing half: a reader of the pinned policy
now learns that `contract-v2.6` is superseded and not dischargeable. What it does
NOT do — and says so itself, deliberately — is DEFINE the state or its
declaration form: *"No sentinel is invented … Building one here would be exactly
the failure that check exists to catch."* That definition is this packet's.

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

**OD-9 — ADDED 2026-09-02 ON A CODEX FINDING, AND IT IS A NARROWING OF THE
GUARD RATHER THAN A NEW DECISION. THE SUPERSEDING BUNDLE MUST BE STRICTLY
LATER.** OD-4 as ruled requires the successor to be CUT and PUBLISHED. Codex
showed on PR #578 that this is satisfiable BACKWARDS: a declaration for
`contract-v2.6` written into `contract-v2.5`'s entry and naming `contract-v2.5`
— a bundle that was cut, is published, and carries a valid annotated tag on a
declaring commit — passes every mechanical check as first written, so an untagged
bundle would go quiet with **no replacement published at all**. The requirement
now demands that the superseding bundle's `(major, minor)` be STRICTLY GREATER
than the spent bundle's, with a scenario and an `error` of its own. **Taken and
repaired here rather than filed as a successor**, because it is not an extension
of the guard, it is the guard: a decision whose stated purpose is *"the only way
to make a bundle quiet is to publish its successor's tag"* is not met by a tag
that already existed. It does NOT reopen OD-4's ruling — the three severities,
the record, and the acceptance ladder are as ruled; a fourth refusal joins them.
The residue is disclosed: version ordering is the CHEAP conjunct and this family
does not prove that the successor actually carries what the spent bundle was to
have carried, that claim living in the declaration's CAUSE and MEASUREMENT, which
are read for presence and not for truth.

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
  the header being accepted — it read `Status: draft` when this was measured,
  and reads `Status: ratified` since 2026-09-02; the measurement stands as
  taken.

The one `error` that does NOT move is the point: `release-tag-publication`
reports `contract-v2.6` at `error` in both runs, in the same words. **This
packet describes the fix and performs none of it.**

**ONE THING DID MOVE, AND IT IS NOT A DOC-HEALTH FINDING — it was found by CI
rather than predicted, and is recorded that way.** `tests/sequenced_after/test_sweep.py::test_the_live_sweep_reproduces_the_AUTHORING_measurement`
went red on the first run: authoring an ACTIVE change that carries a MODIFIED
block raises `co_modified` 104 → 105, `active_co_modified` 18 → 19 and
`change_ids` 153 → 154. That is the pin behaving exactly as designed — its
docstring says *"WHEN THE CORPUS MOVES, THIS PIN MOVES WITH IT — and the move is
RECORDED below rather than silently re-typed"* — so the pin moves in the same
commit with a dated MOVEMENT LOG entry, and the three counts it does NOT move
(`sole_modifiers` 49, `active_sole` 12, `declaring` 1) are asserted unchanged so
that a change adding itself to two populations at once could not hide.
`validate-sequenced-after.py` passes over the corpus with the packet in it (31
active, 1 declaring). **No `sequenced_after:` field is declared**: it is carried
by an ACTIVE, UNPROMOTED change, and adopting an unratified surface is not what
that change's *"declaring must never be worth less than omitting"* doctrine asks
of a packet written before it lands.

**What the realization will move, when it lands**: the one `error` becomes one
`info`, and `contracts/CHANGELOG.md` gains a `release-inventory-drift` `info`
labelled *"editorial member — expected between cuts"* until the next cut
re-baselines the inventory. Net on `main`: **-1 `error`, +2 `info`**, and the
self-gate goes green because the estate stopped having an unanswerable finding,
not because a test was edited.

## Review convergence — eight findings over three rounds, seven taken, one refused with a measurement

Recorded here rather than only in the ratification record, because a proposal
whose text moved under review owes a reader the reason where the text is.

**TAKEN — Codex P1, the successor ordering guard.** OD-9, above. The guard as
ruled was satisfiable by an EARLIER already-published bundle. Repaired in the
requirement with a new refusal and a new scenario.

**TAKEN — Codex P1, the shared finding identity.** OD-5, above. Two spent
bundles would have shared one `(family, repo, path)` key on
`contracts/CHANGELOG.md`, defeating the per-state disappearance detection that
decision exists to provide. Repaired to the per-bundle release inventory, with a
scenario pinning that two spent bundles carry DIFFERENT identities.

**TAKEN — Copilot, the reserved form's delimiters.** The marker form was shown
wrapped in double backticks, which a reader can copy as part of the literal. It
is now an indented code block, and the requirement says why in one clause.

**TAKEN — Codex P1, round 3: the PROVISIONAL band was unreachable.** OD-4's
ruled `warning` for a cut-but-unpublished successor was written as a
non-acceptance, and the fallback clause kept the superseded `error` for every
declaration that was not accepted — so a conforming family would have reported
BOTH during the legitimate publication window, contradicting the ruling it was
written to encode. The requirement now names THREE outcomes rather than two —
ACCEPTED, REFUSED, PROVISIONAL — and a PROVISIONAL declaration SUPPRESSES the
superseded `error` and reports one finding. **Nothing is lost by the
suppression, and the requirement says why**: the successor is the bundle the
manifest now declares, so the distance arm grades it on its own account and the
obligation has MOVED rather than been discharged. The band is bounded by that
grading, not by this state's patience.

**TAKEN — Codex P2, round 3: the proposal's own summary still said
`contracts/CHANGELOG.md`.** OD-5 was amended and § *What changes* was not, so a
Spec Kit implementation following the summary would have rebuilt the exact defect
the requirement now avoids. The summary now names
`contracts/releases/<bundle>.digests.yaml` and says why in one clause. **A
proposal whose operative paragraph contradicts its own amended decision is a
defect in the proposal, not a stale sentence**, and it is repaired rather than
noted.

**TAKEN — Copilot, round 3: `recognise` → `recognize`.** Canon spells it with a
`z` five times and with an `s` never; a delta that introduces the other spelling
into a requirement it is restating is introducing drift into text whose whole
value is that it does not drift.

**TAKEN — Copilot, round 3: a misleading pin message.** The `co_modified`
assertion's message said the population is *"unchanged by THIS change"* — true
of the test's OWNING change, `add-sequenced-after-substrate`, whose titles are
ADDED and novel — while the reading it guards had just been raised BY this
packet. The message now names which change raised it and which one does not move
it, because a pin whose failure message points at the wrong subject invites the
wrong repair.

**REFUSED WITH A MEASUREMENT — Copilot, the unquoted `#575` in the front
matter.** The finding says the `Origin:` line's `#575` "will be parsed as a
comment and break metadata consumption". **Nothing parses that block as YAML,
and if anything did the estate would already be broken 150 packets deep.** Three
measurements: `yaml.safe_load` FAILS on the front matter of
`add-release-tag-publication-check`, `add-requirement-ref-resolution-integrity`
AND `add-clearing-dispatch-boundary` — every one of them, on `mapping values are
not allowed here`, because these blocks are markdown headers containing prose
with colons, never YAML documents. The reader that exists is line-wise
(`corpus.STATUS_RE` = `^Status:\s*(.+?)\s*$`, within `STATUS_SCAN_LINES = 15`),
and `sixteen` proposals in this repository already carry an unquoted `#<issue>`
on their `Origin:` line, `add-release-tag-publication-check` — this packet's own
basis — among them. Quoting this one line would make it the lone divergence from
a convention with no YAML reader to serve, so the finding is declined and the
measurement is recorded in its place. **A REAL YAML SURFACE EXISTS AND IS
CORRECT**: `.openspec.yaml` is parsed, and every prose field in it is a folded
`>-` block precisely so that a `#` inside it is literal.

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
