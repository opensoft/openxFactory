# Design: align-doxbench-contract-pin-to-publisher

## The measurements this rests on

Taken 2026-08-10 from the `change-add-wheel-action-verbs` worktree, so the
proposal argues from readings rather than from reasoning.

| Question | Reading |
| --- | --- |
| What does `validators()` raise? | `ContractPinError: …/change-add-wheel-action-verbs/stack.yaml: no stack.yaml to verify the contract-v1.28 pin against` |
| Where does it raise? | `doxbench_contracts.py:174`, inside `verify_stack_pin` — the first statement of `validators()` |
| What does the route emit? | `500` / `{"ok": false, "error": "catalog_unavailable", "message": "the model catalog could not be assembled safely"}` |
| Does openxFactory have a `stack.yaml`? | No, and never has. `git log -- stack.yaml` is empty; the only tracked matches are two doc-health neutrality fixtures |
| Do the schema bytes verify? | Yes, in BOTH candidate checkouts — sha256 and manifest parity pass for both files |
| Have the bytes moved since v1.28? | No. Identical at v1.28, v1.29, v1.30, v1.31 and HEAD |
| Where does `resolve_root()` land? | `/home/brett/projects/xFactory/openxFactory` — the aggregation's submodule, then at `9fe29a2` on `staging/topology-handoff` |
| Does `OPENXFACTORY_ROOT` fix it? | No. With `OPENXFACTORY_ROOT=$PWD` the released rung ERRORs on the same `ContractPinError`, because `verify_stack_pin` reads `repo_root`/`REPO_ROOT`, a separate axis |

The last row is the one that matters for the ruling: **no configuration of the
current code makes these routes work from this repository.** This is not a
misconfigured plane.

## Decision 1: publisher mode, not a publisher `stack.yaml`

Two ways to satisfy the check were available.

**Add a `stack.yaml` to openxFactory** declaring the release its in-repo runtime
consumes. Rejected. It would have the publisher declare a consumption pin on
itself, inverting working rule 1 at the level of a tracked file, and it creates a
file that must be re-pinned on every release or the runtime breaks again — the
same failure mode, on a timer. It also answers the question dishonestly: the
declaration would be true by construction and could never catch the drift the
check exists to catch.

**Recognize the publisher.** Taken. The check's purpose is stated in its own
docstring — "a consumer can never read one release while the repository declares
another". That risk is real for a domain repo reading a submodule pin, and
structurally absent for tooling reading the release it ships inside. Where there
is no gap between declared and read, there is nothing to verify.

What makes this safe is that the declared-pin check was never the thing proving
the bytes. The fail-closed chain in `_verified_bytes` — sha256 against
`SCHEMA_DIGESTS`, then parity against the checkout's own
`contracts/manifest.yaml` — is untouched, still runs per request, and still
refuses on any drifted byte. Publisher mode drops one vacuous question and keeps
every substantive one. The measurements above confirm the substantive ones pass.

**Detecting the publisher.** Three markers, all present in this repository, all
required together: `contracts/manifest.yaml`, `contracts/schemas/`, and
`scripts/validate-ideation-dashboard-contracts.py`. Requiring all three is what
distinguishes a release checkout from a directory that merely contains a
similarly named file — the same distinction manifest parity already draws for a
single schema, applied to the checkout as a whole. A tree missing any marker is
not a publisher and takes the consumer path, declared pin and all.

**A tighter same-tree rule was considered and rejected.** Raised during design:
publisher mode should apply only when the RESOLVED checkout is the hosting repo,
since `OPENXFACTORY_ROOT` could point at some other release and reopen the
declared-versus-read gap the check exists to close. Implementation showed that
argument is wrong. The declared-pin check never compared `stack.yaml` to the
checkout — it compares `stack.yaml`'s ref to `CONTRACT_REF`, a module literal,
exactly as the digest check compares checkout bytes to `SCHEMA_DIGESTS`, another
module literal. Both anchors are this module's own, so WHICH release gets read is
already fully governed by the digest chain no matter where the checkout sits. The
tighter rule would therefore have added no safety, and it would have broken the
documented `OPENXFACTORY_ROOT=<another released checkout>` integration rung. The
rule keyed on the hosting repository alone is both simpler and correct; the
rejection is recorded in `verify_stack_pin`'s docstring so it is not re-proposed.

## Decision 2: repin to v1.31, digests unchanged

contract-v1.31, target `e5554028e521d57c7501ef9bac206b20415281ef`, annotated tag
object `fc66fa38b999ea15ce74bf00410afe189cc3a5d6`.

The repin is deliberately **digest-neutral**: v1.31's own manifest records the
two digests already hard-pinned, so no verified byte changes and no schema
conformance question reopens. That is the whole reason to do it in this change
rather than defer it — the currency question is settled here at zero risk, and
settling it later would mean doing it against a release whose bytes may have
moved.

The module's comment block above the pin stays true and stays load-bearing: the
release is immutable, these literals name content that already exists, and the
pin moves only through the normal workflow. This change IS that workflow for
this consumer.

Note for whoever repins next: codexFactory's `stack.yaml` declares
contract-v1.30 (`6c03d78`). It no longer hosts this runtime, so the two pins are
independent and the divergence is not a defect — but a future reader comparing
them should know why they differ.

## Decision 3: prefer the running checkout

`VALIDATOR_RELPATH` embeds the `openxFactory/` prefix, which is correct for the
aggregation-relative walk it was written for and wrong for a runtime living
inside openxFactory: it searches one level below where it stands, so from the
publisher it can never resolve to itself and always walks up to the sibling
submodule checkout.

Precedence after this change, highest first:

1. explicit `root=` — a caller that names a checkout means it
2. `OPENXFACTORY_ROOT` — an operator override, unchanged
3. **the hosting repository, when it is itself a publisher checkout** — new
4. the existing walk-up to an aggregation-relative `openxFactory/`
5. `ContractPinError` — absence is never an implicit pass

Only rung 3 is added; nothing above or below it moves. The consumer case reaches
rung 4 exactly as it does today.

This is a correctness fix, not a convenience one. Today a serve launched from a
feature worktree verifies contracts against whatever branch another session left
the aggregation submodule on — the shared-checkout hazard the repo's own working
rules warn about, reached through a code path nobody was watching. It is
currently harmless only by coincidence of those two files not having changed
since v1.28, which is not a property anything guarantees.

## Raised, not decided — outside this change's three items

**The refusal is unobservable to the operator.** Every pin exception is
swallowed to `None` and the route emits a fixed message. That swallowing is
correct on the wire: `ContractPinError` text names checkout paths and digests,
and none of that belongs in a response. But nothing is written anywhere else
either, so a broken pin presents to the operator as an opaque `500` with no
reason — which is why this took a diagnosis session rather than a glance. The
console-token refusal one branch above already writes its reason to stderr
(`serve.py:1174`), so the pattern and the precedent both exist.

Left out because it is a fourth item and not what was asked for. Flagged because
this change removes the symptom that would have prompted it, and the next pin
break — a real digest drift, which publisher mode deliberately still refuses on
— will be exactly as silent as this one was.
