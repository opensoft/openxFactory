# codexFactory's regular-PR-council-clearance archive, dispositioned — the runs, verbatim

Status: record
Kind: report
Measured on: 2026-09-11 (session-local; UTC had rolled to 2026-09-12 — every
timestamp below is UTC and the discrepancy is recorded rather than smoothed)
Base: openxFactory `main` at `323c7adf2d218d050a43d8168ece6d031d025ff8`, in a
FRESH CLONE at branch
`change/disposition-codexfactory-regular-pr-council-clearance-archive`. The
consuming trees measured are codeXfactory/codexFactory at
`87ea247f550b97a9d2cadf844ceb4c48a06996f4` (the head of PR #434,
`archive/add-regular-pr-council-clearance`) and codeXfactory/codexFactory `main`
at `3c31a2e4006e54b3e772076a74ecf93f54ab2952`. ALL READ-ONLY: the codexFactory
clone is local and `--no-checkout`, both trees are DETACHED worktrees of it,
nothing is committed to them and nothing is pushed anywhere; no byte of
codexFactory is written by this packet.
Measured by: lane `provenance-autonomous-merge` (session `codeXfactory-3`), seat
`oxf-disposition`
Ruling on the ORDERING this packet acts under: Brett Heap, 2026-09-11, verbatim
**"This change first"**, codexFactory
`hermes/domain/review-councils/records/2026-09-11-gate-rules-provenance-axis-declaration.md:656-659`, § 8.
Ruling that GRANTS the two entries: Brett Heap, 2026-09-12T03:04:29.167Z,
verbatim **"ratified_by — ratify the entries as encoded"**, recorded on
openxFactory #745 (comment 5643056862).

Every block below is copied from a terminal in this lane. Where a line is elided
it is marked `…`, and nothing is elided from a totals line, a verdict line or an
exit code. Absolute scratch paths are shortened to `<…>`. The pinned CLI is
`@fission-ai/openspec@1.12.0`, resolved by content address on every run, with
its 80-package closure installed through the committed lockfile:

```
openspec-cli-pin: @fission-ai/openspec@1.12.0 from pinned artifact (<…>/node_modules/.bin/openspec); integrity sha512-oFE2Lj7WVSc87nSi… verified
openspec-cli-pin: dependency closure openspec-cli-pin.1.12.0.package-lock.json (80 packages); lockfile_integrity sha512-aw5lIN45tQq2WZll… verified; installed with `npm ci --ignore-scripts`
```

**What is being proved, in five sentences.** That the RETIREMENT is real: the
pin as it stands on `main` REFUSES on #434's tree, naming exactly the entry this
packet deletes (§ 1). That deleting it and stopping there is NOT the fix — the
run then exits 1 with two UNDISPOSITIONED findings, which is how the second half
of this packet was discovered rather than assumed (§ 2). That the two entries
turn those findings into ACCEPTED EXCEPTIONS with the tool's own totals
unchanged (§ 3). That the whole edit is invisible to openxFactory's own gate
(§ 4). And that on codexFactory `main`, where #434 is still open, this pin
REFUSES — which FIXES AN ORDER between the two repositories and is not a defect
in these entries (§ 5).

**The command, in the form the consuming repository's gate issues it**, is the
pinned entrypoint with `--repo` over the tree being measured:

```
cd <openxFactory clone at this branch>
OPENSPEC_TELEMETRY=0 python3 scripts/validate-openspec-cli-pin.py \
    --repo <codexFactory tree> --all --cache-dir <…>
```

---

## 1. BEFORE, on #434's tree: the pin on `main` REFUSES, and it named this day itself

Tree: codexFactory `87ea247f` (PR #434 head). Pin: openxFactory `main`
`323c7adf`, unedited.

```
$ OPENSPEC_TELEMETRY=0 python3 scripts/validate-openspec-cli-pin.py --repo <cxf@87ea247f> --all
…
Totals: 33 passed, 3 failed (36 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
        …
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
        …
REFUSE pin-disposition-stale: the pin disposes findings this run did not produce:
  • add-regular-pr-council-clearance / merge-master-approval/spec.md (repo codexFactory)

The condition each was granted for no longer occurs — typically because the change archived out of the `--all` corpus, or because the pinned CLI now words the finding differently. A suppression that outlives its condition is a standing exemption nobody re-read, so it is REFUSED rather than tolerated: delete the entry from `dispositions:` in contracts/openspec-cli-pin.yaml, in a change that says the condition is gone
…
exit 2
```

The refusal names **exactly one** entry, and that entry's own `retires_when:`
predicted this run in these words, quoted from the pin as it stood:

> add-regular-pr-council-clearance archives IN codexFactory — and on that day
> codexFactory's own `--all` run REFUSES `pin-disposition-stale` until this
> entry is deleted, which is the mechanism working.

The two ERROR findings the run DOES produce against
`merge-master-approval/spec.md` are already visible in the body of the same run,
one per sibling change, and they are what § 2 isolates:

```
change/extend-merge-master-envelope-to-floor-bot-lanes
  ✗ [ERROR] merge-master-approval/spec.md: MODIFIED "Bounded autonomous surface" omits scenario(s) the current spec still has: "A human-authored pull request is never approved by tier 1 alone", "A gate-integrity path is never approved autonomously". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
…
change/relocate-review-authority-floor
  ✗ [ERROR] merge-master-approval/spec.md: MODIFIED "Bounded autonomous surface" omits scenario(s) the current spec still has: "A human-authored pull request is never approved by tier 1 alone", "A gate-integrity path is never approved autonomously". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
  ✗ [ERROR] repository-gate-floor/spec.md: MODIFIED "An automated floor regeneration only ever proposes" omits scenario(s) the current spec still has: "The human gate is unchanged". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
```

**The canon the check compares against, read directly rather than inferred.**
At `87ea247f`, `openspec/specs/merge-master-approval/spec.md:205` carries three
scenario titles under *Bounded autonomous surface* — *"A human-gated surface is
untouched"*, *"A human-authored pull request is never approved by tier 1
alone"*, *"A gate-integrity path is never approved autonomously"*. At
codexFactory `main` `3c31a2e4` the same requirement carries two — *"A
human-gated surface is untouched"* and *"A human-authored pull request is never
auto-approved"*. **The archive is the whole difference.** Both sibling MODIFIED
blocks, at their own `specs/merge-master-approval/spec.md:5`, carry the OLD
title and NO reserved marker paragraph.

---

## 2. THE DELETION ALONE IS NOT THE FIX — exit 1, two UNDISPOSITIONED

Tree: codexFactory `87ea247f`. Pin: `main`'s, with ONLY the stale entry deleted,
written to `contracts/pin-probe-deleted-only.yaml` for the run and removed
afterwards. (The lockfile resolves relative to the pin file's own directory, so a
probe kept outside `contracts/` refuses `pin-unreadable` before it validates
anything — measured, and recorded here so the next author does not lose the same
ten minutes.)

```
$ … --repo <cxf@87ea247f> --all --pin contracts/pin-probe-deleted-only.yaml
…
Totals: 33 passed, 3 failed (36 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
openspec-cli-pin: the pinned CLI reported 2 failure(s) this pin does not disposition. The PIN held — this is a finding about the deltas, not about which tool ran.
  ✗ extend-merge-master-envelope-to-floor-bot-lanes / merge-master-approval/spec.md: MODIFIED "Bounded autonomous surface" omits scenario(s) the current spec still has: "A human-authored pull request is never approved by tier 1 alone", "A gate-integrity path is never approved autonomously". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
  ✗ relocate-review-authority-floor / merge-master-approval/spec.md: MODIFIED "Bounded autonomous surface" omits scenario(s) the current spec still has: "A human-authored pull request is never approved by tier 1 alone", "A gate-integrity path is never approved autonomously". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
  Remedy for each: FIX IT, or DISPOSITION IT in contracts/openspec-cli-pin.yaml with a canon citation (`cited_to:`, non-empty) and an authority (`ratified_by:`). An undispositioned ERROR is not a tolerated one, and a disposition with no citation is refused rather than read as 'none needed'.
exit 1
```

**This is the discovery, not a confirmation.** The brief this seat was given
named one act — delete the stale entry. The run above is why the packet has a
second half: the archive that retired one exception raised two more in the same
commit, and a pull request carrying only the deletion would have moved
codexFactory's gate from exit 2 to exit 1 and called it fixed.

---

## 3. AFTER, on #434's tree: exit 0, four ACCEPTED EXCEPTIONS, totals unchanged

Tree: codexFactory `87ea247f`. Pin: this branch's
`contracts/openspec-cli-pin.yaml`, one entry deleted and two added.

```
$ … --repo <cxf@87ea247f> --all
…
Totals: 33 passed, 3 failed (36 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (4 applied) — this run is NOT a clean tree:
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
  ✗→D extend-merge-master-envelope-to-floor-bot-lanes / merge-master-approval/spec.md
  ✗→D relocate-review-authority-floor / merge-master-approval/spec.md
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 4 finding(s) are ACCEPTED EXCEPTIONS, named above.
exit 0
```

**`Totals: 33 passed, 3 failed (36 items)` is BYTE-IDENTICAL to § 1's.** The
pinned CLI's own verdict about codexFactory's corpus did not move; what moved is
which of its findings this estate has read and accepted. Three failed ITEMS
carry four findings, because `relocate-review-authority-floor` carries two.

---

## 4. openxFactory's own gate is untouched — the literal CI invocation

Tree: openxFactory, this branch. Command: the exact string
`.github/workflows/openspec-cli-pin-gate.yml:101` runs.

```
$ python3 scripts/validate-openspec-cli-pin.py --all --no-cache
…
Totals: 101 passed, 2 failed (103 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in openxFactory (2 applied) — this run is NOT a clean tree:
  ✗→D add-chain-attestation / signed-execution-chain/spec.md
  ✗→D add-composed-view-authoring / ideation-dashboard/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS, named above.
exit 0
```

All FOUR codexFactory entries are neither applied nor stale here. This is the
property one pin file governing a fleet depends on, and it is measured rather
than assumed on every packet that touches the list. **`Totals: 101 passed, 2
failed (103 items)` is one item more than the same run measured before this
packet existed (`100 passed … 102 items`)** — the extra item is THIS CHANGE,
which the corpus run now validates, and it passes.

**And the packet validates `--strict` on its own**, with `skip_specs: true` and
no `specs/` directory, which is the declaration being CHECKED rather than merely
written:

```
$ … --change disposition-codexfactory-regular-pr-council-clearance-archive
…
change/disposition-codexfactory-regular-pr-council-clearance-archive
  ℹ [INFO] file: skip_specs is set in .openspec.yaml: change declares no spec-level behavior changes, zero deltas accepted
Totals: 1 passed, 0 failed (1 items)
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address and every target validated --strict clean
exit 0
```

---

## 5. ON codexFactory `main` THIS PIN REFUSES — and that FIXES AN ORDER

Tree: codexFactory `main` `3c31a2e4`, where PR #434 is still OPEN. Two runs, the
same tree, two pins.

**Pin as it stands on openxFactory `main` — exit 0:**

```
$ … --repo <cxf@3c31a2e4> --all
…
Totals: 33 passed, 3 failed (36 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (3 applied) — this run is NOT a clean tree:
  ✗→D add-regular-pr-council-clearance / merge-master-approval/spec.md
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
OK openspec-cli-pin: @fission-ai/openspec@1.12.0 verified against its content address; every target validated --strict with 0 UNDISPOSITIONED failures. THIS IS NOT A CLEAN TREE: 3 finding(s) are ACCEPTED EXCEPTIONS, named above.
exit 0
```

**This branch's pin — exit 2:**

```
$ … --repo <cxf@3c31a2e4> --all
…
Totals: 33 passed, 3 failed (36 items)
openspec-cli-pin: DISPOSITIONED FINDINGS in codexFactory (2 applied) — this run is NOT a clean tree:
  ✗→D amend-composition-selector-labelling / domain-hermes-content/spec.md
  ✗→D relocate-review-authority-floor / repository-gate-floor/spec.md
REFUSE pin-disposition-stale: the pin disposes findings this run did not produce:
  • extend-merge-master-envelope-to-floor-bot-lanes / merge-master-approval/spec.md (repo codexFactory)
  • relocate-review-authority-floor / merge-master-approval/spec.md (repo codexFactory)

The condition each was granted for no longer occurs — typically because the change archived out of the `--all` corpus, or because the pinned CLI now words the finding differently. A suppression that outlives its condition is a standing exemption nobody re-read, so it is REFUSED rather than tolerated: delete the entry from `dispositions:` in contracts/openspec-cli-pin.yaml, in a change that says the condition is gone
…
exit 2
```

**Why, stated in the tool's own terms.** On `main` the archive has not landed,
so `openspec/specs/merge-master-approval/spec.md` still carries *"A
human-authored pull request is never auto-approved"* and the pinned CLI words
the finding with THAT title. The `finding:` text is matched WHOLE, so neither
new entry matches anything on that tree, and an entry in scope with no matching
finding is the definition of stale. The deleted entry, meanwhile, still HAS a
matching finding there — so on `main` this packet's pin would leave
`add-regular-pr-council-clearance / merge-master-approval/spec.md`
undispositioned as well; the staleness refusal (exit 2) simply outranks the
undispositioned exit (1) and is what gets printed.

**THE CONSEQUENCE IS AN ORDER, AND IT IS NOT NEGOTIABLE BY PREFERENCE.**
codexFactory's declared openxFactory pin MUST NOT advance to this change's merge
commit before PR #434 merges: an early advance reds codexFactory `main` on two
entries at once. The advance lands together with #434 or after it, never before.
Brett Heap ruled on 2026-09-12T03:04:29.167Z that lane `codeXfactory-1` carries
the advance (*"codeXfactory-1 carries it"*), sequenced after that lane's #435 and
#433.

This is the same shape the precedent measured for codexFactory PR #318 and
recorded in its own `retires_when:`, one requirement further along — and it is
worth naming that the shape has now repeated, because a property that holds
twice for the same reason is a rule this corpus should expect rather than
rediscover.

---

## 6. What was NOT measured, said plainly

* **codexFactory's `validate` job on #434 going green** is a codexFactory
  verdict on a codexFactory tree, and it needs BOTH this change merged AND
  codexFactory's pin advanced to reach it. Nothing here claims it. What is
  claimed and measured is that the `openspec-cli-pin` leg exits 0 once the pin
  file carries this change.
* **The two sibling re-derivations** are not drafted, begun or ticked here.
* **No openxFactory `--all` corpus run beyond the pin gate** is reported in this
  file; the packet's own `openspec validate --strict` and `pytest` runs are
  recorded in `tasks.md`, against this branch's tree.
