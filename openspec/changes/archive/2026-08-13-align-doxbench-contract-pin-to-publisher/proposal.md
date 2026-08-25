---
code_surface: openxFactory (scripts/ideation_dashboard/doxbench_contracts.py — the declared-pin check, the checkout resolution, and the pinned ref; the two doxBench model routes in serve.py recover behavior without changing shape; tests/ideation-dashboard/test_doxbench_contracts.py and the released rung in test_doxbench_routes.py)
target_release: implemented
Status: ratified
Ratified: 2026-08-11 by Brett Heap — in-session, verbatim: "ratify the change". The ruling is publisher mode over adding a `stack.yaml` to openxFactory; the alternative was put and declined (design.md "Decision 1").
Realized: merged to openxFactory main as 5d8e963 (PR #164, 2026-08-11) and green on the implemented target — `tests/ideation-dashboard` 2850 passed / 5 skipped / exit 0, `openspec validate --all --strict` 58/58, doc-health 0 new regressions, contract family validator 26 instances clean. Live-proven in a real browser on the restarted local plane: 127.0.0.1:8765 answers `200 {kind: workbench-model-catalog, models: []}`, having answered `500 catalog_unavailable` from the same request before the restart.
---

# Proposal: align-doxbench-contract-pin-to-publisher

## Why

doxBench's two model routes have been dead since the runtime moved into
openxFactory, and the reason was already written down before they died.

`adopt-neutral-tooling-home` (2026-08-03, `82ae3d8`) relocated the ideation
dashboard runtime from codexFactory into openxFactory. Its own tasks.md,
lines 155-161, recorded the consequence and deferred the fix:

> **OPEN ITEM for Brett/tranche D:** `doxbench_contracts.verify_stack_pin`
> requires the HOSTING repo's `stack.yaml` consumption pin; openxFactory is the
> publisher and has none, so from a publisher checkout serve's two doxbench
> model routes fail CLOSED (fail-closed refusal, server otherwise unaffected)
> until a ruled publisher-side declaration lands.

Tranche D never landed a ruling, so the refusal stands. `GET
/workbench/model-catalog` returns `500 catalog_unavailable` and `POST
/actions/workbench/chat-turn` refuses the same way, on every request, from
every checkout of this repository.

**The check is consumer-shaped and it is now in a producer.** `verify_stack_pin`
demands that the hosting repository's `stack.yaml` declare
`xfactory.contract_ref` equal to the module's hard-pinned ref. Its stated
purpose is that "a consumer can never read one release while the repository
declares another". openxFactory has no `stack.yaml`, has never had one, and
under working rule 1 never should: consumers pin openxFactory, not the reverse.
There is no consumer here to hold honest. The check is not failing — it is
asking a question the publisher cannot be asked.

**The bytes were never the problem.** The two schema files
(`xfactory-workbench-model-catalog.schema.yaml`,
`xfactory-workbench-chat-turn.schema.yaml`) are byte-identical from
contract-v1.28 through contract-v1.31 and HEAD, and both pass sha256 and
manifest parity in every candidate checkout. The digest chain — the part that
actually proves a release was read as released — has been green throughout. Only
the declared-pin question refuses, and it refuses first, before any byte is
read.

**Two adjacent defects have been hidden behind it.** Both are the same
relocation's residue, and both would surface the moment the first is fixed:

- *The pin is three releases stale.* `CONTRACT_REF` names contract-v1.28
  (`ff64e81a`). The repository is at contract-v1.31, and codexFactory — the
  original host, now merely a consumer — has itself moved on to contract-v1.30
  (`6c03d78`). Even back in a consumer repo this check would now refuse on
  drift rather than on absence.
- *The resolution can never find the repository it is running in.*
  `VALIDATOR_RELPATH` is `openxFactory/scripts/validate-ideation-dashboard-contracts.py`,
  so `resolve_root()` looks for a checkout nested one level below where it
  searches. From inside openxFactory it therefore walks past itself every time
  and lands on the aggregation's `openxFactory/` submodule — a sibling checkout
  on whatever branch another session left it. Measured today, that checkout sat
  at `9fe29a2` on `staging/topology-handoff`. A serve running from one worktree
  was verifying its contracts against another session's branch. It is invisible
  only because those two schema files happen not to have changed.

**Why this needs a change rather than a patch.** The publisher-side declaration
is a contract-consumption boundary: it decides what "I read this release as
released" means for tooling that lives inside the release. Neutral tooling now
hosted here is not only doxBench — `adopt-neutral-tooling-home` also moved
doc-health and the NotebookLM sync — so the rule wants stating once, for any of
them, rather than being spelled into one module's control flow.

## What Changes

Three deltas, in the order their dependency runs.

1. **Publisher-mode verification** (`shared-contract-ownership`). State that
   tooling hosted inside the publisher verifies its consumption by the released
   bytes it reads, not by a declared consumption pin. A checkout that carries
   `contracts/manifest.yaml`, `contracts/schemas/`, and the family validator IS
   the release; asking it to declare which release it consumes is vacuous. The
   digest and manifest-parity checks are unchanged and remain the whole
   fail-closed chain. A consumer checkout keeps the declared-pin requirement
   exactly as it stands today — nothing about pinning from a domain repo
   changes.

2. **The pin names the current release.** Move `CONTRACT_REF` /`CONTRACT_TAG`
   from contract-v1.28 (`ff64e81a`) to contract-v1.31
   (`e5554028e521d57c7501ef9bac206b20415281ef`, annotated tag object
   `fc66fa38b999ea15ce74bf00410afe189cc3a5d6`). `SCHEMA_DIGESTS` does not move:
   contract-v1.31's own manifest records exactly the two digests already
   hard-pinned, so this repin is digest-neutral and additive — it re-declares
   which release the runtime reads, and changes no verified byte.

3. **Resolution prefers the checkout the runtime is running in.** When the
   hosting repository is itself a publisher checkout, resolve to it. Only when
   it is not does resolution fall back to the existing walk-up, and the explicit
   `root=` parameter and `OPENXFACTORY_ROOT` override keep their current
   precedence above both. A serve verifies the contracts of the tree it was
   launched from, never a sibling checkout's working state.

## Impact

- **Affected capabilities:** `shared-contract-ownership` (one added
  requirement), `ideation-dashboard` (one added requirement).
- **Affected code:** `scripts/ideation_dashboard/doxbench_contracts.py` only.
  `serve.py` is untouched: `_doxbench_validators` already swallows every pin
  exception to `None` by design, and `_handle_workbench_model_catalog` already
  emits the fixed refusal — they recover because the seam beneath them starts
  succeeding, not because their shape changes.
- **Affected tests:** `test_doxbench_contracts.py` gains publisher-mode and
  resolution-preference coverage. The `@released_only` rung in
  `test_doxbench_routes.py` — four probes skipped unless `OPENXFACTORY_ROOT` is
  set, recorded as environment-conditional in the relocation's own 2.3 gate
  evidence — becomes runnable from a publisher checkout with no env var, which
  is what turns this class of break back into a test failure instead of a
  runtime 500.
- **No contract release.** No schema byte changes; `target_release: none`.
- **Closes** `adopt-neutral-tooling-home` tasks.md 2.1's tranche-D open item.
- **Not in scope:** the provider dispatch arm. No provider is contacted from
  this slice, and the honest empty-catalog posture stays a success — a plane
  with no configured model still gets a conformant empty catalog rather than
  this refusal, which is the whole point of separating the two.
