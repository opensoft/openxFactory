# Design: add-release-tag-gate

Status: draft
Kind: design
Draft slice of: openspec/changes/add-release-tag-gate/proposal.md

## 0. The convener brief

Brett Heap ruled the SHAPE on 2026-09-04 (lane `openxfactory-max001`, in
session, on issue **#664**), verbatim: *"do your recommendation"* — given
against three options and settling **option 2**. The issue records what that
settles:

1. a `release-tag-gate` workflow on EVERY pull request, short-circuiting when
   the pull request touches neither `contracts/manifest.yaml` nor
   `contracts/releases/**`, otherwise evaluating the merge tree with the
   `release-tag-publication` family;
2. the suite test keeps only its self-test half and drops the zero-findings
   assertion on this repository;
3. nightly doc-health keeps reporting the condition at its current severity;
4. making the check REQUIRED is Brett's console act, recorded as `[OPERATOR]`
   with evidence before archive.

**Not chosen, in the issue's own words:** option 1 (*"keep the suite pin:
collateral to every lane"*) and option 3 (*"PR-scoped suite assertion: same
relief for others, but main's own suite still goes red after the cut and
confuses readers"*).

Everything below is what the ruling did not settle.

## D1 — What the gate may honestly FAIL on, and what it may only RECORD

**THE PROBLEM, STATED WITHOUT SOFTENING IT.** The ruling's item 1 reads *"FAIL
when that tree declares a bundle whose tag is not published on the remote"*. Read
literally and alone, that sentence makes the cutting pull request unpassable: the
tag for a NEW bundle cannot exist before the merge. Measured over every
`contract-v3.x` cut, the annotated tag is created 6–68 seconds AFTER the merge
and points AT THE MERGE COMMIT (the table is in `proposal.md` § Why). A gate
demanding it earlier would be unsatisfiable by construction, and an unsatisfiable
gate is one that gets bypassed, disabled, or worked around — which is the same
failure mode as the pin it replaces, one directory over.

**THE RESOLUTION IS ALREADY IN THE FAMILY, WHICH IS WHY NO NEW JUDGEMENT IS
INVENTED HERE.** The promoted requirement's first scenario is *The declaring
commit is still the published tip*: a bundle whose earliest declaring commit is
the tip emits NO FINDING, "because the cut has only just landed and the owner's
tag act legitimately follows it", and the same scenario adds that this "MUST NOT
[be recorded] as a pass that discharges the obligation, which remains owed".
**On a merge tree the cutting commit IS the tip.** So the family, run unmodified
over the pull request's merge tree, already answers the hard case correctly: the
bundle this pull request cuts is silent, and every OTHER bundle is graded exactly
as it is nightly.

**THE DECISION.** The gate's bar is **exactly the bar the retired pin held —
no `error` and no `warning` from this family — asked of the PULL REQUEST'S MERGE
TREE instead of published `main`, and only of pull requests that touch the
release surface.** Nothing re-implements what "published" means, re-grades a
distance, or invents a severity. This is `#614`'s **ONE CLOCK, NOT TWO** applied
to a family whose clock is already written down, and `#639`'s *one published
tip* read one step further: the family resolves its tip through a single seam
method (`remote_main_sha`), so pointing it at a different tip is a ONE-METHOD
override (`MergeTreeGit`) rather than a fork of the reader.

What the gate consequently FAILS on:

| condition | who says it | pre-merge decidable |
| --- | --- | --- |
| a bundle cut earlier, still untagged, while this pull request touches the release surface | the family (`error`, superseded arm; or `warning`/`error`, distance arm) | yes |
| a tag that peels to a commit not declaring the bundle | the family (MISPLACED, `error`) | yes |
| a lightweight ref where an annotated tag is owed | the family (`error`) | yes |
| the declaration moved onto an already-published number | this gate (D2) | yes |
| the family could not ask its question | this gate, FAIL CLOSED | yes |

What it only RECORDS: **the tag owed by the bundle this pull request itself
cuts.** The check prints `TAG OWED: …` naming the bundle, writes it to the job
summary, and raises it as a `::notice` annotation on the pull request. The
nightly goes on reporting it. And the NEXT pull request that touches the release
surface is refused until it exists — which is the enforcement that the recording
defers to rather than replaces.

**THE VETO POINT.** *A cutting pull request cannot be required to carry its own
tag, so this gate passes it and records the obligation instead.* If the convener
wants the tag REQUIRED at the head before merge, the change is one condition —
refuse when the declared bundle has no published tag peeling to the tree under
judgment — and it is a DIFFERENT PACKET, because it also changes the versioning
policy's realization order (tag before land, not after) and every cut's
choreography with it. The evidence above says the estate does not work that way
today, four times out of four.

## D2 — `gate-version-reuse`: the one addition beyond the ruling's text

**What it is.** Where this pull request MOVES the manifest declaration to a
bundle that ALREADY has a published tag peeling somewhere other than the tree
under judgment, the gate refuses.

**Why it is here.** It is the one release defect a pre-merge gate can catch that
nothing else in the estate catches. The family cannot: at a tip where the
declaration and the tag agree, `_tag_state` reads `ok` and the reuse is
invisible by construction. The policy is explicit — realization order step 1
*"recheck bundle/tag availability and allocate the next available version"*, and
Immutable Tag Correction: a defective release is corrected by a SUPERSEDING one
and a version number *"is never reused"*. The condition is narrow: the
declaration has to MOVE in this pull request, so a pull request editing the
manifest for any other reason never reaches the arm, and a new number never
trips it because a new number has no tag.

**The exception, and why it is not a loophole.** A tag peeling to THE VERY TREE
UNDER JUDGMENT is the obligation met early, not a number cut twice. Two real
situations reach it: a tag published at the head before merge (openXwallet's
`wallet-v1.4` flow), and this gate re-run against a merge commit after the cut
landed. Without the exception the gate would be un-replayable — pointing it at
`807a4f47` would refuse the very cut it should certify — and a check that cannot
be re-run is one nobody can audit.

**Ordering matters and was corrected during authoring.** The arm runs AFTER the
family, not before. A tag that exists and peels to the WRONG commit is both
"reuse" and "misplaced", and the family has ratified words for it; the gate's
own words are reserved for what the family leaves unsaid. (Written the other way
round first, a misplaced-tag fixture came back as `gate-version-reuse` — caught
by `test_a_misplaced_tag_is_refused_in_the_family_s_own_words`.)

**THE VETO POINT.** This arm is NOT in the ruling. Deleting it leaves a gate
that is exactly issue #664's item 1 and nothing more; the deletion is one
`if` block in `scripts/validate-release-tag-gate.py`, two tests, one scenario in
the delta, and one row in D1's table.

## D3 — The obligation is recorded in the check, not in a pull-request comment

The brief for this packet suggested *"a PR comment"* alongside the check
summary. **Declined, and the reason is not tidiness.** A workflow that comments
needs `pull-requests: write`, and on a `pull_request` event that permission is
READ-ONLY for a fork — so the comment would silently fail in exactly the case
where a visible obligation matters most, and the packet would be claiming a
visibility it does not have. A comment would also re-post on every push to the
cutting branch. The `::notice` annotation and the job summary are attached to
the check itself, are visible on the pull request's Checks tab, cannot fail
open, and need no write scope: `permissions: contents: read` is the whole grant.

## D4 — A `warning` refuses too

The family grades an untagged CURRENT declaration by distance: `warning` inside
the threshold, `error` past it. The gate refuses on both.

**Why not `error` only.** Because that is not the bar that was being asserted.
The retired pin asserted *no `error` AND no `warning`*, and this packet's whole
claim is that the assertion MOVED rather than weakened. Failing only on `error`
would quietly relax it under cover of a relocation.

**Why it does not re-create the collateral.** The window the family grants is
for LANDINGS THAT LEAVE THE RELEASE SURFACE ALONE — and those pull requests
never reach the family at all now. The only pull request that meets a `warning`
is one touching `contracts/manifest.yaml` or `contracts/releases/**` while a
declared bundle is unpublished, and such a pull request is asserting the release
surface is in order. **The residue is named rather than hidden:** a pull request
that edits the release surface for an unrelated reason during a legitimate
tagging window will be refused, and its remedy is the same one-act remedy —
publish the tag.

## D5 — The scope test is `contracts/manifest.yaml` + `contracts/releases/**`

Exactly the ruling's two paths, and NOT `contracts/**`. Contract bytes change on
ordinary pull requests; the release SURFACE is the declaration and the
inventories that record a cut. A wider filter would move the collateral this
packet removes one directory down. Asserted directly in
`test_the_short_circuit_names_the_manifest_and_the_inventory_prefix_only`,
including the near misses `contracts/CHANGELOG.md` and `contracts/releases.md`.

`contracts/CHANGELOG.md` is deliberately NOT in the set even though the family
reads it: it is one of the three EDITORIAL members the versioning policy allows
to move between cuts, so treating an edit to it as a release-surface change
would gate the very document a SPENT disposition is recorded in.

## D6 — Fail closed on a family skip, which is where the two moments differ

The family answers a skip where version control cannot answer, and the retired
pin tolerated it explicitly (*"A SKIP IS NOT A DEFECT AND IS NOT ASSERTED
AWAY"*). That was right for the nightly, which reads an environment it does not
control. The gate is now the ENFORCING moment for a tree about to become the
published one, so an unasked question is not a pass. Both readings are stated in
the delta's own scenario so that the divergence is ratified rather than
discovered.

## D7 — Where the code lives, and what it does not touch

One new file under `scripts/`, importable from its hyphenated entrypoint, the
pattern `tests/openreposhape_pin/test_pin_verifier.py` already uses. **Nothing
in `scripts/doc_health/` changes** — the family, its severities, its threshold,
its floor, `Finding`, the report grammar and `FAMILIES` are all untouched, so
the family-enumeration count and the "twenty-three check families" requirement
do not move and no `openspec/specs/` file is added (which would owe a
codexFactory floor advance).

The gate tests live in `tests/doc-health/` rather than a new directory: they
reuse that suite's conftest (which puts `scripts/` on the path and registers the
structural hermeticity guard), and a new top-level test directory would change
the suite's collection shape for no gain.

## Cost, measured

The family consults the published refs once per in-scope cut bundle — 46 of the
52 inventories in `contracts/releases/` today — and each is an `ls-remote` round
trip. Measured end to end against the live repository: **~90s**. The workflow's
timeout is 15 minutes. This is the same cost the nightly already pays, and the
same cost the retired suite pin was paying INSIDE `pytest-suite` on every run:
removing it takes `tests/doc-health/test_release_tag_publication.py` from 110s
to 19s and takes ~46 live network calls out of the required suite, which is a
hermeticity improvement the packet gets for free.

## Replay evidence, and its honest limit

`python3 scripts/validate-release-tag-gate.py . --head 807a4f47` (the
`contract-v3.4` cut) exits **0**, reporting `contract-v3.4` as PRE-PUBLISHED —
its tag now peels to that very commit — and the family clean over the tree.
`--head 16b85614` (PR #636, which touched
`contracts/releases/contract-v3.3.digests.yaml`) also exits 0 **today**, and
that is a limit of replay rather than a result: the family reads LIVE published
refs, and `contract-v3.3`'s tag exists now. At the time that pull request was
open the tag did not, and the gate would have refused it — which is the intended
behaviour and is asserted on synthetic trees instead, where the refs are under
the test's control
(`test_the_window_is_not_a_shield_for_a_release_surface_edit`).

## D8 — The policy-doc edit is made, and the drift it raises is disclosed

`docs/contract-versioning-policy.md` is the document this gate enforces, so the
gate belongs in its § Bundle Realization Order. It is also a DIGESTED MEMBER of
the published `contract-v3.4` bundle, and it is not one of the three EDITORIAL
members (`contracts/CHANGELOG.md`, `contracts/manifest.yaml`,
`contracts/README.md`) that may legitimately move between cuts. Editing it
therefore raises one `release-inventory-drift` `error`.

**The edit is made anyway, and the alternatives were both worse.** Hand-editing
`contracts/releases/contract-v3.4.digests.yaml` to match is forbidden: that
bundle is published, tagged, and immutable provenance, and the family's own
action text forbids editing an inventory to match an absence. Deferring the
sentence to whoever cuts the next bundle would leave the ratified policy silent
about a gate that enforces it, in the window where a reader most needs to be
told. **The finding is the designed transient** —
`release-surface-integrity`'s own scenario says changed members "appear as
non-editorial drift against that previous bundle's inventory, and the condition
is detectable at the commit rather than only at tag-verify time" — and the next
cut clears it by re-digesting the member. The estate does this routinely with
this very document: `95c2cf6a` (PR #622) and `2898b104` both moved it between
cuts.

It is recorded here, in `proposal.md` § Impact with the before/after counts, and
in `tasks.md` § 3.5, so that it is read as a predicted consequence rather than
discovered as a regression.
