---
code_surface: openxFactory — TWO PACKERS AND THEIR RECORD, NO CONTRACT SCHEMA EDIT. `scripts/doc_health/semantic.py` gains an input BUDGET over the assembled analysis prompt: one named constant (`DEFAULT_INPUT_BUDGET_BYTES`), a deterministic three-phase first-fit packer (`pack_within_budget`) that packs WHOLE DOCUMENTS ONLY and defers the rest, a reserved share for each of the two populations (`GROUNDING_BUDGET_SHARE`), and five budget fields on the bundle's `meta.json` and on `SweepMeta` (`input_budget_bytes`, `input_bytes`, `docs_included`, `docs_deferred`, `truncated`) plus the named `deferred` list. `scripts/doc_health/runner.py` gains `--semantic-input-budget-bytes`; `scripts/doc_health/report.py` gains one input line plus one line per deferred document. `scripts/doc_health/catalog_dispatch.py` gains `shard_analysis_input` (the cataloger child's own assembly, reproduced so the parent can MEASURE it) and writes the same budget plus per-shard assembled byte counts into the catalog bundle's `meta.json`. Tests at `tests/doc-health/test_semantic_input_budget.py`. The child-side enforcement is the AGGREGATION's surface, not this one: `opensoft/xFactory` `.github/workflows/doc-health-analysis-worker.yml` and `doc-health-cataloger-worker.yml` read `input_budget_bytes` from the bundle and refuse to invoke the model over it. NO CHANGE to the finding families, the finding contract, the job envelope, the worker profile, the dispatch provenance gate, the shard IDENTITY (`build_shards` is untouched, so the catalog's carry-forward is untouched), or any credential path.
target_release: implemented (the affected repositories' main lines — openxFactory for the packers and their record, opensoft/xFactory for the two child workflows). NO CONTRACT-BUNDLE INVOLVEMENT, and that is measured rather than assumed: this packet moves no file under `contracts/`, defines no record kind, adds no schema field, and `contracts/manifest.yaml` carries no doc-health row a byte budget could change. The surface is the doc-health tooling, its report and the two aggregation worker workflows, so there is no cut to allocate a number at and `deferred-allocation` would be declaring a bundle this packet does not owe. The class is ADDITIVE — a new bound and a new record where there was neither; no consumer is made non-conformant and no existing field changes meaning.
Status: draft
Proposed: 2026-09-22, on Brett Heap's word *"brief a writer to add the input-size guard"* (2026-09-22)
Origin: the doc-health nightly's analysis child has failed EVERY night since 2026-08-30 except the two 2026-09-02 runs, silently. Governing issue: opensoft/xFactory#479 (filed with this packet).
---

# Proposal: add-worker-input-budget

## Why

**The bounded workers' input was never bounded.** `semantic.build_analysis_input`
assembled the whole selected corpus plus the whole promoted-spec grounding into
ONE prompt and wrote it to `analysis-input.txt`, with no size check anywhere in
the module, the runner, or the workflow. When that prompt outgrew the model's
context window the child began failing, and it failed INVISIBLY: `claude -p
--output-format json` writes its error to STDOUT, the child redirects stdout into
`worker-result.json`, and the cleanup step deletes the workspace — so the job log
showed `Process completed with exit code 1` against an empty stderr and nothing
else.

### The evidence

Measured from the nightly's own `semantic-sweep-bundle` artifacts, against the
`doc-health-analysis-worker` child's conclusion and its `Run bounded no-tools
analysis` step duration:

| night | `analysis-input.txt` | scope | child | step |
| --- | ---: | --- | --- | ---: |
| 2026-08-30 | 8,430,004 | changed docs | failure | 3 s |
| 2026-08-31 | 3,640,354 | changed docs | failure | 2 s |
| 2026-09-01 | 3,829,890 | changed docs | failure | 2 s |
| 2026-09-02 | 2,524,427 | changed docs (10 of 661) | **success** | **200 s** |
| 2026-09-02 | 1,869,042 | changed docs (0 of 661) | **success** | **56 s** |
| 2026-09-03 | 2,913,875 | changed docs (17 of 666) | failure | 3 s |
| 2026-09-04 | 2,932,442 | changed docs (19 of 669) | failure | 2 s |
| 2026-09-11 | 6,402,585 | changed docs (142 of 713) | failure | 3 s |
| 2026-09-12 | 6,586,271 | changed docs (145 of 716) | failure | 3 s |
| 2026-09-14 | 7,418,276 | changed docs (178 of 726) | failure | 4 s |
| 2026-09-15 | 7,418,276 | changed docs (178 of 726) | failure | 2 s |
| 2026-09-16 | 7,418,276 | changed docs (178 of 726) | failure | 3 s |
| 2026-09-17 | 7,663,396 | changed docs | failure | 3 s |
| 2026-09-18 | 7,706,463 | changed docs | failure | 2 s |
| 2026-09-19 | 7,940,307 | changed docs | failure | 2 s |
| 2026-09-20 | 12,331,149 | full corpus (weekly) | failure | 2 s |
| 2026-09-21 | 7,940,307 | changed docs (188 of 733) | failure | 2 s |

Size separates success from failure with no exception: everything at or under
2,524,427 bytes was accepted, everything at or over 2,913,875 bytes was refused,
and every refusal took two to four seconds — far too little for a model call.

**The control is the sibling lane.** On 2026-09-11, 09-12, 09-14 and 09-15 the
`doc-health-cataloger-worker` child — the SAME runner, the SAME vault-fetched
token, the SAME `claude -p` flag set, the SAME `claude-sonnet-5` — ran 188 s,
324 s, 188 s and 305 s and returned valid structured output, on an assembled
input of 82,712 bytes. On those same four nights the analysis child died in two
to four seconds. Authentication was demonstrably healthy; only the input size
differed.

**Reproduced directly.** Feeding the real 2026-09-21 bundle
(`analysis-input.txt`, 7,940,307 bytes) to `claude -p` with the child's exact
flag set gives exit 1, zero bytes on stderr, and on stdout:

```json
{"is_error": true, "terminal_reason": "blocking_limit",
 "result": "Prompt is too long", "duration_ms": 358}
```

which is the failure the job log could not show.

### Why a budget over the CHANGED DOCS alone would not have been enough

The prompt carries two populations, and the second one is the larger:

| night | promoted-spec grounding | changed docs | total |
| --- | ---: | ---: | ---: |
| 2026-09-02 | 102 specs, 1,866,899 B | 10 docs, 655,400 B | 2,524,427 B |
| 2026-09-21 | 123 specs, 3,051,663 B | 188 docs, 4,886,516 B | 7,940,307 B |

As of 2026-09-21 the promoted-spec grounding is 3,051,663 bytes **on its own** —
already past the ceiling with zero changed documents. A bound that reached only
the changed-docs population would leave the lane dead. The budget therefore
bounds the whole assembled prompt, and reserves a share for each population so
that neither check family is starved: `semantic-normative-prose` needs the
changed documents, `semantic-contradiction` needs the specs to ground against.

## What Changes

1. **A byte budget on the assembled analysis prompt**, defaulting to a single
   named constant and overridable by `--semantic-input-budget-bytes`.
2. **Deterministic packing, whole documents only.** Three phases: the
   changed-docs population packs first fit into its reserved share; the
   promoted-spec grounding packs first fit into its own; whatever either leaves
   unused is re-offered to what the first two phases deferred, corpus first.
   Within each population the order is `(repo, path)` — the same order the
   payload is emitted in. A document that does not fit is deferred ENTIRE and
   the walk continues, so one oversized document defers itself rather than
   starving everything behind it. **Nothing is ever truncated mid-document.**
3. **Every deferral is recorded**, in the bundle's `meta.json` and in the dated
   report, naming each deferred document.
4. **The budget travels with the bundle** so the child can enforce it without a
   duplicated constant, and the child refuses to invoke the model on an input
   over it rather than letting the model refuse silently.
5. **The cataloger's bundle carries the same budget and its own measured
   per-shard input sizes.** `build_shards` bounds a shard by ENTRY COUNT, which
   is not a byte bound: 25 ordinary documents assemble to ~83 KB, 25 large ones
   would not, and nothing measured the difference. Shard identity and selection
   are untouched.

## The budget arithmetic

Every figure is measured, not assumed. Feeding 2,799,448 bytes of this corpus to
the CLI with the child's flag set returns:

> the request is ~1086484 tokens (limit 1000000) but this conversation is only
> ~700164 tokens — the rest is system prompt, tool definitions, and attachment
> content

which resolves both unknowns at once:

```text
context limit                       1,000,000 tokens   (stated by the CLI)
- CLI fixed overhead, MEASURED        386,320 tokens   (1,086,484 - 700,164)
- the model's own answer               64,000 tokens   (max output)
= usable prompt content               549,680 tokens
x bytes per token, MEASURED               3.998 bytes  (2,799,448 / 700,164)
= 2,197,600 bytes
x 0.87 safety margin
= 1,911,912  ->  1,900,000 bytes
```

Forwards: 1,900,000 bytes is ~475,200 content tokens, ~861,520 of the
1,000,000-token request with the fixed overhead, and a full 64,000-token answer
still leaves ~74,000 tokens spare. Against production: the measured ceiling
(~2.45 MB) sits exactly inside the observed bracket of 2,524,427 accepted and
2,913,875 refused, and 1,900,000 is 75% of the former.

## Why this is normative and not an implementation detail

Two ratified requirements are reached, and neither can absorb a budget silently.

**1. Sweep scope is declared to be Hermes-owned policy.** *Hermes-layer sweep
scope resolution* makes scope "Hermes-owned policy resolved deterministically by
orchestration", chosen from the ordered set `incremental | full-weekly |
full-nightly`, and *Sweep sequencing and snapshot consistency*'s first scenario
says the sweep's corpus "is exactly the deterministic pass's inventory for that
run". A byte budget narrows the swept set on a SECOND axis that no Hermes layer
declares and no scope value names, and a budgeted run therefore CONTRADICTS that
scenario as promoted. Shipping it without saying so would make the report's
scope line false. The delta resolves the contradiction rather than living beside
it: the scenario is restated so the corpus is "drawn from exactly the
deterministic pass's inventory for that run and from no other snapshot" — which
is the requirement's real subject, one snapshot shared by both passes — and a
third bullet states that the set SENT may be a subset of that corpus, named as
such, with the shared snapshot unaffected.

**2. A deferred document is not a skipped sweep, and the contested-finding rule
turns on the difference.** *The semantic sweep is unavailable* protects a prior
finding whose sweep "was skipped or unavailable" from reading as resolved. A
partial sweep is neither: the sweep RAN and returned findings, for a corpus that
silently excluded some documents. Without a delta, the first night a document is
deferred its prior semantic findings vanish from the report and the next run
emits "uncited resolution" errors against findings nobody disposed of. The
delta closes that hole explicitly.

## Impact

- **Affected capability:** `doc-health` (two requirements MODIFIED, one ADDED).
- **Affected code:** `scripts/doc_health/{semantic,runner,report,catalog_dispatch}.py`,
  `tests/doc-health/test_semantic_input_budget.py`.
- **Affected repositories:** `openxFactory` (this packet's surface) and
  `opensoft/xFactory` (the two child workflows, landed separately).
- **Not affected:** finding families, finding contract, job envelope, worker
  profile, dispatch provenance gate, shard identity, credential paths.

## Open questions

- **OQ-1 — the grounding share.** The default reserves half the budget for
  promoted specs. At the 2026-09-21 corpus that sends 93 of 311 documents and
  defers 218, of which 71 are promoted specs, so `semantic-contradiction` is
  grounded against roughly half the promoted corpus on any given night. The
  alternative — spending the whole budget on grounding and sweeping almost no
  changed documents — is worse, but the split is a policy choice and is put for
  ruling rather than assumed.
  - **Measured 2026-09-24.** Both nights since the budget went live packed to
    their 1,900,000-byte budget, per their own `semantic-sweep-bundle`
    `meta.json`: 2026-09-23 (opensoft/xFactory run 35810840997) sent 1,899,789
    bytes, 92 documents, and deferred 226 — 152 changed documents and 74
    promoted specs; 2026-09-24 (run 35947804907) sent 1,899,236 bytes, 96
    documents, and deferred 227 — 156 changed documents and 71 promoted specs
    (counted by the `population` the packer records on every deferral; every
    deferred spec is an `openspec/specs/*/spec.md` and no deferred changed
    document is). The split at each share, on the CURRENT inventory with no
    model call: the aggregation's `main` at `c6280584`, assembled by the
    runner's own prepare path (`doc-health.py --repo-root . --previous-inventory
    health/inventory/2026-09-04.json --semantic-prepare`) — 196 changed
    documents costing 5,051,588 bytes and 127 promoted specs costing 2,984,532
    bytes at the packer's `document_cost` — then packed by
    `pack_within_budget` at each share:

    | share | bytes sent | sent / deferred | changed docs sent / deferred | promoted specs sent / deferred | openxFactory sent: changed docs of 109, specs of 66 | codexFactory sent: changed docs of 31, specs of 13 |
    | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
    | 0.3 | 1,899,164 | 90 / 233 | 53 / 143 | 37 / 90 | 1, 0 | 0, 0 |
    | 0.4 | 1,899,413 | 94 / 229 | 50 / 146 | 44 / 83 | 1, 1 | 0, 0 |
    | 0.5 (built) | 1,899,236 | 96 / 227 | 40 / 156 | 56 / 71 | 0, 1 | 1, 7 |
    | 0.6 | 1,899,594 | 96 / 227 | 33 / 163 | 63 / 64 | 1, 3 | 0, 12 |
    | 0.7 | 1,899,953 | 104 / 219 | 29 / 167 | 75 / 52 | 2, 14 | 0, 13 |

    The weekly full sweep over the same inventory (a Sunday `as_of`: 738
    governed documents costing 9,416,787 bytes, the same 127 specs) sends, at
    0.3 / 0.4 / 0.5 / 0.6 / 0.7, 202 / 184 / 183 / 181 / 182 documents — 165 /
    140 / 127 / 118 / 107 governed documents and 37 / 44 / 56 / 63 / 75 specs
    — and of openxFactory's 397 governed documents 0 / 1 / 0 / 0 / 0. The
    method reproduces production: at 0.5 the repack rebuilds each nightly
    bundle's `analysis-input.txt` byte for byte and its `meta.json` budget
    record field for field, and the current inventory's 0.5 prompt is
    byte-identical to the 2026-09-24 night's.
  - **Lane recommendation (not a ruling):** keep 0.5 — each 0.1 of share moves
    about 190,000 bytes, 3 to 12 documents, from one population to the other,
    while what the sweep misses at every share (openxFactory: at most 2 of 109
    changed documents and 14 of 66 specs sent) is set by the `(repo, path)`
    packing order, which no share repairs.
- **OQ-2 — deferral does not carry over, and this packet does not make it.** The
  incremental scope is a content-hash diff against the last committed
  `health/inventory/<date>.json`, which the `finalize` job emits
  UNCONDITIONALLY (`--emit-inventory`, `if: always()`) from the full current
  inventory. There is no per-document sweep cursor anywhere in `doc_health`. A
  document deferred tonight is therefore in tomorrow's baseline, no longer
  "changed", and would not be re-selected. This packet consequently CAPS AND
  RECORDS rather than claiming a carry-over it does not implement; a real
  carry-over needs its own state and its own packet.
  - **Measured 2026-09-24.** The committed baseline has not in fact advanced
    since 2026-09-04: the aggregation's `main` carries `health/inventory/`
    through `2026-09-04.json`, because the nightly's rolling report pull
    request, opensoft/xFactory#396 (`doc-health/nightly`), has been open since
    2026-09-10, and both nights' selections reproduce exactly against that
    file (193 of 736 on 2026-09-23, 196 of 738 on 2026-09-24). A deferred
    document is therefore re-selected today — and deferred again, the packing
    order being deterministic: 219 documents (151 changed, 68 promoted specs)
    were deferred on both nights.
  - **Lane recommendation (not a ruling):** accept cap-and-record for this
    packet, and carry deferrals over in a separate packet staged first as
    `ideation/staging/doc-health-sweep-carry-over/` (not created here). Its
    one design constraint: the cursor is its own committed record beside the
    inventory (for example `health/sweep-cursor/<date>.json`, written from
    the bundle's `meta.json` `deferred` list and delivered in the same report
    commit), never a field of `health/inventory/<date>.json` — `finalize`
    emits that file UNCONDITIONALLY from the full current inventory every
    night, so a cursor folded into it would be erased by the next emit.
- **OQ-3 — RESOLVED 2026-09-23.** Filed as *"a live blocker this packet does
  not address"*: since 2026-09-16 the runner's CLI received HTTP 403 *"Your
  organization has disabled Claude subscription access for Claude Code"* on
  every invocation, which no code change reaches (the 2026-09-22 nightly then
  ran clean and the refusal recurred on 2026-09-23, opensoft/xFactory#491).
  The administrative act was taken on 2026-09-23: Brett Heap reported the
  Console-side remedy #491 names as its option 1 — re-enabling Claude Code
  access via subscription — done, in his words *"the HTTP 403: 'Your
  organization has disabled Claude subscription access for Claude Code.'
  error was fixed. it runs now"* (recorded verbatim on #491 at 16:34:40Z); no
  repository change was made. Verified the same hour: the analysis child
  re-dispatched against nightly parent run 35810840997 — opensoft/xFactory
  Actions run 35889825278, correlation `semantic-35810840997-2` — passed the
  input-size guard at 1,899,789 of 1,900,000 bytes, and the model accepted
  the prompt and returned 4 findings in 2 min 16 s, where that morning's
  02:48Z dispatch of the same bundle (run 35811821401) had been refused 403.
  Issue #491 closed at 16:38:55Z and #479, the governing issue, at 16:38:58Z,
  with both halves of task 4.3 recorded on it. The 2026-09-24 nightly (run
  35947804907, conclusion `success`) is the first full night under the
  restored access: all four model children succeeded with model output —
  analysis 35948587830 (guard passed at 1,899,236 bytes; 5 findings),
  cataloger 35948591376, readiness 35949701420 (12 of 12 clusters, no error
  entry) and derive-possibles 35950836940 (10 of 10). A recurrence can no
  longer pass as a green night: opensoft/xFactory#499 (merge `4feb0db3`,
  2026-09-23T22:52:54Z, for #492) fails the readiness and derive-possibles
  children closed with a degraded artifact on any 401/403 refusal.
