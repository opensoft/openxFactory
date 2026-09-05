# Design: disposition-codexfactory-declared-renames

Status: draft

Four decisions, each recorded because a reader six months from now will ask why
this packet is as small as it is.

---

## 1. Why a DISPOSITION and not a copy-back

The tool's remedy is written into its own message: *"Copy them into the MODIFIED
block (a MODIFIED requirement replaces the whole block, so archive refuses to
drop them)."* Taking that remedy is what this packet refuses, twice, and the
refusal is not a preference.

**Copying the first scenario back reverts a ratified narrowing.**
`add-regular-pr-council-clearance` retitles *"A human-authored pull request is
never auto-approved"* to *"A human-authored pull request is never approved by
tier 1 alone"*. Its own marker line says what the retitle does: the successor
keeps canon's `WHEN` verbatim and narrows the `THEN`, so the tier-1 envelope
still cannot approve a human-authored pull request while tier-2 clearance
carrying a unanimous verdict pinned to the candidate's exact head SHA now may.
That is the BREAKING change the packet declares ("both human-authorship bars
fall"). Restoring the old title puts back the bar the change exists to lower —
and would sit in the same block as its own replacement, so the delta would
declare two incompatible rules at once.

**Copying the second back reverts a ruling.**
`amend-composition-selector-labelling` retitles *"Current aliases do not
masquerade as immutable versions"* on Brett Heap's 2026-08-31 ruling
(`hermes/domain/review-councils/records/2026-08-31-enrolled-roster-model-pin-flip.md`
§5.1/§12.0) that the old title's `THEN` needed a reading to stay true after the
roster model-pin flip. The successor states the rule directly for exact
identifiers and aliases both. Restoring the old title restores the clause the
ruling found unreadable-as-written.

**Canon already holds that these blocks are declared correctly.** Promoted
`doc-health` § *Currency of an active change's MODIFIED requirement blocks*
(`openspec/specs/doc-health/spec.md:1586`) says a block that adds a scenario
title canon does not carry "is a retitle, whatever the marker calls it"
(line 1750) and names `Merged into` as the author's instrument for that shape,
writing the form out at line 1770. codexFactory PR #216 converted the first
block's marker from `Removed from canon` to `Merged into` for exactly that
reason — so what remains is not a corpus defect at all. It is a pinned tool that
cannot read a marker this corpus ratified.

`bump-openspec-cli-pin-to-1.12` already settled what to do about that class:
disposition it, cited, per finding, per repository. Brett Heap ruled the same
exit for codexFactory's pair — *"use recommended name, go on 3 repo shape"* —
after ruling *"take exit 2"* for openxFactory's. This packet writes it down.

---

## 2. Why scope by repository identity, and why out of scope is never stale

One pin file governs the estate, and `scripts/validate-openspec-cli-pin.py` is
invoked with `--repo` against trees that carry none of openxFactory's changes.
Without `repo:`, a change absent because it was never in that tree would be
indistinguishable from a change absent because it archived — and only the second
may refuse.

Identity is read from `git config --get remote.origin.url`, not from the
directory name, because every change in this estate is authored in a worktree
named for its branch; a basename rule would read openxFactory's own corpus as a
repository called `oxf-disp` and quietly place every disposition out of scope.
codexFactory's identity is therefore exactly `codexFactory`.

**The out-of-scope property is a line of code, not a promise.**
`scripts/validate-openspec-cli-pin.py:1145`:

```python
in_scope = [entry for entry in dispositions if entry.get("repo") == identity]
```

`keyed` is built from `in_scope` alone, `applied` is filled only from `keyed`
hits, and `stale` is `[entry for key, entry in keyed.items() if key not in
matched]` — so an entry whose `repo:` differs from the validated tree's identity
is in NEITHER list, by construction. There is no branch in which it could
become stale. That is what makes it safe for this pull request to add two
codexFactory entries to a file openxFactory's own required gate reads on every
pull request, and `evidence/codexfactory-dispositions-2026-09-05.md` measures it
rather than asserting it.

---

## 3. Why the count-pinning test moves 2 → 4, and why that is not a weakening

`test_the_real_pin_declares_exactly_the_two_dispositions_the_bump_carries`
exists to make the list unable to grow unread. Its docstring:

> Asserted against the REAL file because the two entries are the substance of
> the change: a bump that silently grew a third exception would still be a bump
> nobody read.

**So the test is doing its job right now**: this packet cannot add two entries
without touching it, which forces the growth into the diff and into a human's
reading. The correct response to a test that fires for the reason it was written
is to satisfy it deliberately and say so, which is this paragraph.

The test is also STRENGTHENED rather than merely renumbered. It previously
asserted `{entry["repo"] for entry in entries} == {"openxFactory"}` — a set that
a growing fleet would keep loosening. It now asserts the per-repository SPLIT:
which items belong to openxFactory, which to codexFactory, and that the four are
exactly those. A future third repository will fire it again, which is the point.
A companion test asserts the new property directly — the codexFactory pair is
neither applied nor stale on openxFactory's own tree — so the guarantee this
pull request depends on is pinned by a test and not only by a run.

---

## 4. The spec-delta decision, and the criterion it was made by

**Criterion.** This packet writes a spec delta if and only if the rule it
exercises is not already stated. Three properties are needed:

1. a disposition is scoped to one repository by the validated tree's identity;
2. an entry naming another repository is out of scope on this tree and can never
   be stale here;
3. a consumer's entry retires — refuses — when the consumer's own change
   archives.

**Reading.** `openspec/changes/bump-openspec-cli-pin-to-1.12/specs/neutral-product-pin/spec.md`,
the ADDED requirement *"A dispositioned finding is cited, upgrade-coupled, and
refused when stale"*, states all three:

* (1) and (2) in one paragraph — *"A DISPOSITION IS SCOPED TO ONE REPOSITORY.
  Where one pin governs several consuming repositories, a disposition SHALL name
  the repository whose corpus it is about, and a run over any other repository
  SHALL neither apply it nor treat it as stale"* — and again as a scenario,
  *"A consuming repository runs the same pin over its own tree"*, whose THEN is
  *"that disposition is neither applied to nor treated as stale by that run"*
  and whose AND is *"the repository's own findings are judged only against
  dispositions scoped to it"*. That scenario is a description of this packet
  written before this packet existed.
* (3) from the staleness paragraph — *"A DISPOSITION MATCHED BY NO FINDING IN A
  WHOLE-CORPUS SCAN SHALL REFUSE THE RUN"* — read together with the scoping
  rule, which decides WHICH tree's whole-corpus scan is the one that matters;
  and as the scenario *"A dispositioned finding stops occurring"*, whose WHEN is
  *"its change archived"*.

The identity MECHANISM (a git remote URL's basename) is deliberately absent from
the requirement and belongs where it is: in the verifier's docstring and in the
pin's header. A neutral requirement states direction; naming `remote.origin.url`
in canon would pin an implementation.

**Decision: no spec delta, declared rather than omitted.** `.openspec.yaml`
carries `skip_specs: true` — the escape `1.12.0` reads (`dist/core/change-metadata/schema.js`,
`skip_specs: z.boolean().optional()`) and honours in validation
(`dist/commands/validate.js`, `dist/utils/change-metadata.js`), and which
`1.2.0` does not know. The pinned CLI accepting it is measured, not assumed:
`evidence/codexfactory-dispositions-2026-09-05.md` § *The pinned CLI on this
packet*. **This is the first use of `skip_specs` in this corpus**, which is
recorded here because it is the kind of first that should be noticed: it is a
DECLARATION that a change changes no requirement, not a suppression of the
question, and 1.12.0 refuses it as `CHANGE_SKIP_SPECS_CONFLICT` if a `specs/`
file appears beside it.

**The alternative shapes and why each was refused.**

* `## ADDED Requirements` restating the scoping rule — refused. It would put a
  second copy of a ratified requirement into the corpus, free to drift from the
  first, to make a point already made.
* `## MODIFIED Requirements` on that requirement — refused on ORDERING. The
  requirement is not in `openspec/specs/neutral-product-pin/spec.md`: the bump
  is active and has not archived. A MODIFIED block targets promoted text, and
  one targeting text that is not yet canon is the shape `doc-health`'s currency
  rule and the archive gate both refuse.
* Waiting for the bump to archive and then MODIFYing — refused as a sequencing
  cost with no benefit. The bump's archive is not scheduled, codexFactory's step
  3 is blocked until this lands, and the rule needs no modification: it needs
  applying.

---

## 5. What this packet deliberately does not do

* **It does not move `scripts/validate-openspec-cli-pin.py`.** Every property it
  uses — per-repository scope, whole-message matching, the staleness asymmetry,
  `pin-repo-unidentified` — already exists and is already tested. This is the
  first crossing of a repository boundary in production, and it needed no code.
* **It does not move the pin's version, referent or rollback.** Only
  `dispositions:` and the header prose that describes it.
* **It does not wire codexFactory's gate** and does not touch codexFactory at
  all. Step 3 does that, from codexFactory, with the `stack.yaml` re-pin that
  makes this pin file reachable from there.
* **It does not tick task 6.1 of `add-openspec-cli-pin` or 6.3 of the bump.**
  Those describe the wiring, not its precondition, and a tick that ran ahead of
  the act is the thing this estate refuses everywhere else.
* **It does not file exit 3.** Teaching the upstream check to read the reserved
  marker forms remains drafted-and-unfiled in #677's packet
  (`evidence/upstream-issue-draft-merged-into-marker.md`); it is Brett's to
  decide, the two exits are not exclusive, and this packet's four entries are
  the standing cost of not having taken it.
