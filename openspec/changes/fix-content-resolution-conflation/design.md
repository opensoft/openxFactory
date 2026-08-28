# Design: fix-content-resolution-conflation

Five questions, each answered against a measurement rather than a preference.
§ 1 is how the approved three-defect set is packaged, which is the one decision
that changes what was approved. § 2 is where the requirements land and why they
are all ADDED. § 3 is how the one data condition is told from the fourteen that
are not. § 4 is why the obligation is scoped narrower than the file it fixes.
§ 5 is why a contract bundle rides, and what that costs.

## 1. The packaging call — two packets, split on the contract-bundle boundary

**This is OD-1, and it is the only decision in either packet that changes what
Brett approved.** The selection admitted a SET of three defects. It did not say
how many packets. The argument for splitting is arithmetic.

| defect | surface | inventory member of `contract-v2.0`? | realization gate |
| --- | --- | --- | --- |
| 1 — trailing hex boundary | `scripts/doc_health/pin_class.py` | no | merge + green |
| 3 — `"unknown"` split | `scripts/ideation_dashboard/`, `experiments/`, `scripts/doc_health/pin_sentinels.py` | no | merge + green |
| **2 — this packet** | `scripts/hermes_runtime_validation/release.py` (+ `content.py`) | **YES**, `type: validator`, at the digest the tree holds | merge + green **+ an additive bundle cut** |

The membership was established by loading
`contracts/releases/contract-v2.0.digests.yaml` with a YAML parser and walking
its 192 entries into member paths — not by `grep`, because a `grep` for a
filename is exactly the measurement that would miss a renamed `artifact_id` or a
member listed under a path prefix. `scripts/doc_health/*` contributes **zero**
members; this packet's file is present with `digest:
sha256:660e55ca7e6896ea24106483b926e1919a0cb195ef8b9a700a3522f1f393f6b0`, which
is exactly `sha256sum` of the working tree's copy.

**Why membership decides the packaging rather than merely being noted.** Under
release-realization a packet with a code surface archives only on merged plus
green realization evidence, and where a bundle rides, the cut is part of that
evidence. The `contract-v1.44` precedent — the *same file*, cut for the *same
cause*, two days ago, by the packet whose § 6.3 recorded this defect — records
how far an authoring session can take a cut: its `tasks.md` § 4.5 discharged
`verify-commit` and DELIBERATELY did not discharge `verify-promotion` or the
annotated tag, because `verify-promotion` requires the candidate to be reachable
from the remote's `main`, which by definition it is not before the merge, and
because the tag was ruled not to be that session's act. So a bundled packet's
archive waits on a human-gated tag.

**The rejected alternative — one packet for all three — argued rather than
dismissed.** Three real arguments support it: multi-capability packets are
house-normal (**8 of the 24 active changes predating this pair carry two or more
capabilities**, `qualify-avatar-live-voice` carrying four); one origin act producing one
packet is tidier than one act cited by two `.openspec.yaml` files; and the theme
is genuine — all three defects are a component reporting a value it did not
read. Declined on the gate arithmetic above and on a second measurement: the two
halves share **no file, no capability and no test module**. This packet is
`shared-contract-ownership` over `scripts/hermes_runtime_validation/`, proved by
`tests/hermes_runtime_contracts/`; its sibling is `doc-health` plus
`ideation-cross-reference` over three other trees, proved by
`tests/doc-health/`. And the constituting precedent cuts this way: the sentinel
packet exists as ONE packet because a ruling found its two items were "the same
idea (honest non-pins)". By the same test, defects 1 and 3 are one idea and this
is another.

**The cost, stated.** Brett said "in order"; two packets re-sequence 1, 2, 3 as
{1, 3} then {2}. The authoring session reads "in order" as governing the set
rather than the filing shape, flags the reading, and notes that merging the
packets back is a directory move plus one `.openspec.yaml` edit — cheapest
before either is reviewed.

## 2. Where the requirements land — `shared-contract-ownership`, all ADDED

The capability that owns this surface is `shared-contract-ownership`, and the
binding is not an argument by adjacency. Its `SCO-002` "Contract version
pinning" draws the line: "offline runtime verification SHALL resolve exact
commit/tree/blob objects already present locally." And its scenarios are already
bound to the code in question —
`contracts/hermes-runtime/evidence-register.yaml` binds `SCO-002-S03` to
`test_verify_promotion_rejects_a_drifted_release_surface`, which is the test
over `_surface_drift`, which is the sole caller of the function this packet
fixes. Three more requirements were ADDED there by
`fix-release-reachability-race`, and this family extends them one layer down.

The capability stands at **10** requirements; this makes **12**. No active
change carries a `shared-contract-ownership` delta — enumerated across the
`specs/<capability>/` directories of the 24 active changes predating this pair.
`SCO-002` was under an active `MODIFIED` block when the race packet was written
(`add-hermes-customer-subject-runtime-contract`); that change archived
2026-08-27, so the block is promoted and the ordering hazard it created is gone.
Nothing here restates it either way.

**Two requirements rather than one, copying the sibling family on purpose.** It
separated the mechanics from the proofs and gave its reason: the defect it
closed "was not caught by any test … which means the behaviour was outside
everything the suite exercised". That is this defect's position exactly. It was
found by reading; `tests/hermes_runtime_contracts` passes with the conflation in
place. A requirement about a distinction that carries no proof of the
distinction leaves the next reader unable to tell whether it still holds.

## 3. Telling one condition from fourteen

```
resolve_git_object
├── _repository(path)                    → "Git repository is unavailable"
├── normalize_repository_path(path)      → 5 raises, 4 messages
├── _git(...)                            → "Git content dependency is unavailable"  (OSError, 30s timeout)
│                                        → "exact Git object is unavailable"        (git exited non-zero)
└── the resolution proper                → "revision must be a full Git object ID"
                                         → "Git returned an invalid commit object ID"
                                         → "exact Git path is unavailable"      ←── THE ONE
                                         → "Git tree entry is malformed"
                                         → "Git path resolution was not exact"
                                         → "Git path is not a supported regular file"
                                         → "Git returned an invalid blob object ID"
```

**15 raise sites, 14 distinct messages, 1 data answer.** "exact Git path is
unavailable" (`content.py:125`) is reached only after `rev-parse` resolved the
commit AND its tree AND `ls-tree` ran — so the tree was read and the path was
not in it. That is a fact about the release. The other fourteen are the
environment or a refusal.

**The mechanism: a declared code, not a matched message.**
`ContentResolutionError.__init__` already accepts `code`, defaulting to
`HRC-CONTENT-DEPENDENCY`, and a sweep of the repository finds **nothing that
reads `.code` on this class and no occurrence of that string outside its own
default**. So giving `:125` a distinct code is purely additive.

Matching the message text was rejected, and the reason is the promoted sentinel
canon applied to the resolver's own vocabulary: "a near-miss spelling is
precisely the condition under which every consumer guarding on the exact string
already fails". A message gets improved; the match then stops firing; a safety
refusal is silently reclassified as release data; and the direction it fails in
produces no output. Probing separately — resolve the commit, then the path —
was also rejected: it doubles git invocations on the ordinary path and still
cannot separate the twelve conditions that are neither.

**Both refusal classes already fail closed.** `ReleaseDependencyError` and
`ContentResolutionError` are both `RuntimeError` with `exit_code = 2`, and
`scripts/validate-contract-release.py:173` catches both. Q1 recommends the
former, wrapping the latter with `from`, so the verifier's refusals stay in one
class while the resolver's own message survives for the reader — but no CLI edit
is needed under either answer.

## 4. Why the obligation is scoped to presence-and-identity reductions

`release.py` has three sites that swallow a `ContentResolutionError`, and they
are not the same kind of thing:

| site | swallows into | this packet |
| --- | --- | --- |
| `_blob_object_id` `:312-316` | `None` (a blob identity) | **fixed** |
| `_CommitSource.exists` `:401-405` | `False` (a presence answer) | **fixed** (OD-5) |
| `read_member` guard `:713-719` | `HGR-RELEASE-PATH-UNRESOLVABLE`, a named finding | **not fixed** |

The first two collapse a resolution into a value a caller then treats as DATA —
a blob identity to compare, a presence to decide membership on. The third emits
a finding, which is at least visible; changing it changes what a published
finding code means to consumers reading verifier output, and that is a
compatibility question rather than a defect fix.

So the requirement is written at the level of the first two: a resolution
*reduced to presence or identity*. **A PACKET MUST NOT SHIP CANON ITS OWN FILE
VIOLATES.** Written as "every content resolution", it would be breached by
`:713-719` on the day it promoted, in the same file, and a requirement whose
first reader finds a live counterexample thirty lines away teaches that canon
here is aspirational. The alternative — broad wording plus a disposition —
converts a scoping decision into paperwork, which is worse.

`exists()` is fixed and `:713` is not, and the line between them is principled
rather than convenient: one turns a failure into silent data, the other turns it
into a visible finding.

## 5. Why a contract bundle rides

`scripts/hermes_runtime_validation/release.py` is a non-editorial member of the
declared bundle's release digest inventory at the digest the tree holds.
`content.py` likewise. The editorial set is exactly three files —
`contracts/CHANGELOG.md`, `contracts/manifest.yaml`, `contracts/README.md`
(`scripts/doc_health/release_inventory.py:62-66`) — and severity turns on that
set: `INFO` for an editorial member's digest moving, `ERROR` for anything else.

Editing either file without cutting leaves the frozen inventory describing bytes
the repository no longer holds, which `release-surface-integrity` names a defect
and doc-health's release-inventory-drift family reports at `error` — a red gate,
not a warning.

**Touching two members owes ONE cut, not two.** The inventory is rebuilt
wholesale from the manifest plus the contract index, so a single
`validate-contract-release.py build` re-baselines every moved member at once.
The same is true of `contracts/hermes-runtime/evidence-register.yaml` if the new
proofs are bound there: it is a member (`type: evidence-register`), and it rides
the same cut.

**The class is additive.** No schema moves, `contract_schema_version` is
unchanged, no instance valid at `contract-v2.0` is narrowed, and consumers
pinned there stay conformant until they upgrade — which is what makes the next
minor the right allocation rather than a major.

**No minor is reserved here** (OD-6). `contract-v2.0` is current; merge order
decides the next; the `contract-v1.28` renumber sweep is the precedent for why a
proposal that reserves one costs somebody a renumber.
