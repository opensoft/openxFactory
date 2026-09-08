# Design: fix-pin-value-boundary-and-sentinel-split

Four questions this packet had to answer before it could be written, each
against a measurement rather than a preference. § 1 is how the approved set of
three defects is packaged, which is the one decision that changes what was
approved. § 2 is why one ADDED requirement is enough and where it lands. § 3 is
what the fix to the four regexes actually is, and why it is a boundary rather
than a grammar. § 4 is what the `"unknown"` split does at each of the five
emission sites, including the one the inherited record could not have named and
the one that is already correct.

## 1. The packaging call — two packets, split on the contract-bundle boundary

**This is OD-1, and it is the only decision in the packet that changes what
Brett approved.** The approval selected a SET of three defects. It did not say
how many packets. The authoring session split them, and the argument is
arithmetic rather than taste.

### The measurement that decides it

| defect | surface | bundle inventory member? | realization gate |
| --- | --- | --- | --- |
| 1 — trailing hex boundary | `scripts/doc_health/pin_class.py` | **no** | merge + green |
| 3 — `"unknown"` split | `scripts/ideation_dashboard/snapshot_registry.py`, `experiments/.../avatar_f0/cli.py`, `scripts/doc_health/pin_sentinels.py` | **no** | merge + green |
| 2 — `_blob_object_id` conflation | `scripts/hermes_runtime_validation/release.py` | **YES** — `type: validator`, `digest: sha256:660e55ca…` in `contract-v2.0`, and that digest is exactly what the tree carries today | merge + green **+ an additive contract bundle cut** |

`contracts/releases/contract-v2.0.digests.yaml` was loaded with a YAML parser
and its 192 entries walked. The membership is not close: `scripts/doc_health/*`
contributes ZERO members, and defect 2's single file is in the inventory at the
digest the tree holds, so one byte moved there stops the frozen inventory
reproducing the tree — which `release-surface-integrity` names a defect and
doc-health's release-inventory drift family reports at `error` for any
non-editorial member.

### Why membership decides the packaging rather than merely being noted

Under the release-realization capability a packet with a code surface archives
only on merged plus green realization evidence. Where a bundle rides, the
evidence includes the cut, and the `contract-v1.44` precedent — the *same file*,
cut for the *same cause*, four weeks ago — records exactly how far an authoring
session can take that: its tasks § 4.5 discharged `verify-commit` and
deliberately did NOT discharge `verify-promotion` or the annotated tag, because
`verify-promotion` requires the candidate to be reachable from the remote's
`main`, which by definition it is not before the merge, and because the tag was
ruled not to be that session's act.

So bundling puts two fixes that need nothing but a green suite behind a
human-gated contract tag. The delay is not hypothetical and it is not small:
`contract-v1.44` was cut the same day only because that packet's whole subject
was the cut.

### The rejected alternative, argued rather than dismissed

**One packet for all three** is the shape house practice would reach for first,
and three arguments support it.

* *Multi-capability packets are normal here.* Counted rather than asserted:
  **8 of the 24 active changes predating this pair carry two or more
  capabilities**, `qualify-avatar-live-voice` carrying four.
* *One origin act, one packet* is tidier bookkeeping than one act cited by two
  `.openspec.yaml` files.
* *The theme is real.* All three defects are a component reporting a value it
  did not read: a fabricated pin, an under-claimed sentinel, a flattened
  resolution failure.

Declined, on the archive-gate arithmetic above and on a second measurement: the
two halves share **no file, no capability and no test module**. Defects 1 and 3
are `doc-health` + `ideation-cross-reference` over `scripts/doc_health/`,
`scripts/ideation_dashboard/` and `experiments/`, proved by
`tests/doc-health/`. Defect 2 is `shared-contract-ownership` over
`scripts/hermes_runtime_validation/`, proved by
`tests/hermes_runtime_contracts/`. There is no shared edit to coordinate and no
shared regression to run.

And the constituting precedent cuts this way rather than the other. The sentinel
packet exists as ONE packet because a ruling found its two items were "the same
idea (honest non-pins) and should be one future packet". Read with the same
test: defects 1 and 3 are one idea — what a pin VALUE may be, and what a
sentinel must NAME — and defect 2 is a different idea, what a resolution FAILURE
may be flattened into, on a surface neither of the others touches.

### The cost, stated

Brett said "in order". Two packets re-sequence 1, 2, 3 as {1, 3} then {2}. The
authoring session reads "in order" as governing the set rather than the filing
shape — the instruction was a selection among candidate work, not a filing
instruction — and flags the reading so it can be overruled cheaply. Merging the
two packets back into one is a directory move and one `.openspec.yaml` edit,
and both are cheapest before either packet is reviewed.

## 2. Why one requirement is enough, and where it lands

`doc-health` owns the pin verification: the promoted "Derivation-pin
reachability is verified across a declared artifact class" and both promoted
sentinel requirements are its, and `scripts/doc_health/pin_class.py` is the code
that produces the fabricated pin. There is no second candidate.

**The requirement is ADDED, not MODIFIED, and the seam is precise.** The
promoted classification requirement already governs what happens to a
non-commit value: legal non-pin where declared, defect naming artifact, key and
value where not. What it does not govern is whether the verification may
manufacture a SECOND, shorter reading of the same value and run it down the
commit-shaped path in parallel — which is exactly what happens today, and which
§ 5.5 of the sentinel packet recorded as the interaction to expect. The new
requirement closes that, and touches nothing the promoted one says.

Restating the promoted requirement in a `MODIFIED` block to add one clause was
rejected for a reason this capability has evidence for: a `MODIFIED` block
replaces its counterpart wholesale, three changes in three days truncated the
family-enumeration requirement that way, and this capability now carries a
promoted family specifically to catch it. A packet that can be all-ADDED should
be.

**Collision check, current active set.** Two active changes carry `doc-health`
deltas: `add-nightly-dashboard-refresh` (7 ADDED requirements, all about the
image refresh lane) and `add-unclassified-finding-class` (1 ADDED, about a
modified-block-currency finding its class map cannot place). Both all-ADDED,
neither naming any requirement this packet names. No active change carries an
`ideation-cross-reference` delta at all.

## 3. The fix to the four regexes — a boundary, not a grammar

The module already contains the rule. `LOOSE_SHA_RE` at `:159` is

```python
re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{40}(?![0-9a-fA-F])")
```

with a comment saying that `\b` is insufficient because a hexadecimal digit
boundary inside a longer hexadecimal run is a word boundary, so a sha256 would
yield two spurious pins. Every word of that comment applies to the four
expressions that build sites, and none of them carries the guard.

The fix appends `(?![0-9a-fA-F])` to each value group. Measured against the
committed module and against the patched form, on the same line:

| input under `source_revision` | today | with the boundary |
| --- | --- | --- |
| 64-hex, bare | fabricates a 40-char prefix | **no match** |
| 64-hex, quoted | fabricates a 40-char prefix | **no match** |
| 40-hex, bare / quoted / JSON / sequence item / comment-trailed | site built | **site built, unchanged** |

**Why no backtracking route exists**, which is the part worth writing down
because a reader will reasonably worry about it: `{40}` is exact and cannot
give characters back, and the only way to re-anchor the group one character
later would be for `\s*"?` to consume a hexadecimal character, which it cannot.
So the whole key-plus-value match fails rather than sliding along the value.

**A leading `(?<![0-9a-fA-F])` is deliberately NOT added.** The value group is
already anchored by `\s*"?` immediately after the colon, so a leading guard
could never fire — and an inert guard in a file whose other guard is
load-bearing reads as a live one to the next editor.

**The alternative — widen the value group to the whole scalar and then test its
shape — was rejected on duplication.** That is precisely what `_wide_field_re`
and `_WIDE_VOCAB_RE` already do for the classification path, with a
`_SCALAR_VALUE` grammar and a `_MAPPING_KEY_ANCHOR` that exist because two prose
false positives were measured into them. Reproducing that grammar on the narrow
path would create two scalar readers to keep in agreement, where one boundary
character is sufficient and self-evidently correct.

**What the refused value then does.** Nothing is dropped. The wide path already
extracts the whole scalar, `FULL_SHA_RE` does not match a 64-character string,
`pin_sentinels.declared()` returns `None` for it, so it lands where the promoted
classification requirement puts it: a defect naming the artifact, the key and
the value AS WRITTEN. That is why the delta's first scenario asks for the whole
value in the finding — the fix's whole point is that the reader sees what the
file says.

## 4. The `"unknown"` split, site by site

The promoted vocabulary declares five conditions and one canonical spelling
each. The split assigns each emission site the member matching the condition it
measured.

```
snapshot_registry.index_entry  :283   unestablished-revision   "unknown"              (member unchanged; literal imported)
avatar_f0._git_file_commit     :49    dirty-worktree           "uncommitted-worktree"  ← requires a NEW returncode branch
avatar_f0._git_file_commit     :49'   unreadable-repository    "uncommitted"           ← the other half of that branch
avatar_f0._git_file_commit     :51    unreadable-repository    "uncommitted"
avatar_f0._git_head            :60    unreadable-repository    "uncommitted"
avatar_f0._git_head            :62    unreadable-repository    "uncommitted"
```

**`:49` is the interesting one and it is why this is not a rename.** The call
above it is `subprocess.run(..., capture_output=True, text=True, timeout=10)` —
no `check`, and `out.returncode` is never read — so `out.stdout.strip() or
"unknown"` is reached identically by a *successful* `git log` that found no
commit for the path and by a *failed* `git log` that produced nothing because it
failed. The first is `dirty-worktree`: the repository is readable, the content
is real, and no commit holds it. The second is `unreadable-repository`: nothing
was established. A branch on the return code has to exist before either member
can honestly be written.

**`snapshot_registry:283` keeps `"unknown"`, and that corrects the inherited
record.** § 5.6 of the sentinel packet lists all three of its sites as owing a
split. Measured, the projector's condition IS the weakest member's: the entry
has no recorded revision, the repository is readable, and the emitter cannot say
whether the snapshot's own generation lacked one, could not be fetched, or was
never recorded. Writing a stronger member there would assert a condition nobody
established, which is the same falsification the vocabulary refuses for absent
keys.

**The emitter tuples move with the split.** `pin_sentinels.SENTINELS` declares
`emitters` per member, measured by test rather than believed, precisely so a
phantom emitter cannot hold a stale member alive. After the split
`uncommitted-worktree` and `uncommitted` each gain an avatar site, and `unknown`
keeps `snapshot_registry.index_entry` alone. `unused_sentinels()` therefore
still exempts every member, and no member becomes stale — checked, not assumed,
because a split that quietly stranded a declared member would fail the
declaration's own second direction.

**No committed bytes move.** The class reports seven legal non-pins at this
revision — six `uncommitted-worktree`, one `not-applicable-ad-hoc` — and not one
`"unknown"`. The avatar lane's evidence records are not committed, and the
snapshot index the projector writes is generated. So the split changes future
output only, which is why it owes tests over the emitters rather than a corpus
migration.
