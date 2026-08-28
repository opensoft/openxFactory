Realizes `add-unclassified-finding-class` — one ADDED requirement in `doc-health`,
"A modified-block-currency finding its own class map cannot place is itself a
finding" — as Speckit feature `026-unplaced-finding-drift`.

## What was wrong

`classify` is fail-closed: a rule text no pattern of the family's class map
matches is not absorbed into a neighbouring class, it falls to a named residual
row in the report block. **That row is prose.** It has no severity, so no
`--fail-on` configuration reaches it; it is not a finding, so `doc-health`'s own
health-report contract — "every finding MUST appear in the ranked plan as an
actionable item" — does not reach it either. A session working a report's ranked
plan never sees it. And the thing it reports is a defect in this capability's
own tooling: the family emits a finding for a MODIFIED block that drifted from
canon by one clause, and stays silent when its own rule text drifts from its own
map.

## What this does

A nonzero residual now emits ONE `warning` per distinct unplaced rule shape per
run — naming that shape's count, quoting the first instance's rule text
verbatim, and carrying its repository and delta path — placed by the map itself
into a FIFTH class, `unplaced-finding drift`, so it is never counted by the
residual it reports. The residual row keeps rendering beside it; the tally still
sums to the rows; the family stays advisory and stays out of `FAMILY_RESOLUTION`.

## The mechanism, in three sentences

Each arm's rule text renders through one registered `_ArmTemplate`, so the
family's fixed prose has exactly one definition and the arm that prints it
cannot drift from the mask that reads it. `_shape` then runs two steps whose
order is load-bearing: mask every `repr`-emitted span with a left-to-right
consumer (a quote opens a span only at the start or after a non-alphanumeric),
then match the registered templates first-match-wins, the shape *being* the
matched template's id. A rule text no template claims falls back to the lexical
mask rather than being merged into a neighbouring template — fail-closed — and
no field was added to `Finding`.

## Precondition, landed

**PR #461 (`6d100e51`) is on `main`** and is this PR's merge base. It amends the
packet's delta on Brett's ruling of 2026-08-28, verbatim *"Amend: shape = arm
template, all interpolations masked"*: shape identity became "equal after EVERY
FIELD THE ARM'S TEMPLATE INTERPOLATES has been replaced by a fixed placeholder …
so that one shape is one template and one remedy", with the family required to
derive that mask from its own arm templates. This feature's `spec.md`,
`data-model.md` and `contracts/` cite the amended text.

## The grain, measured before and after the amendment

A drop of a *different* class pattern exercises a different arm, so each row
names the pattern dropped:

| tree | pattern dropped | unplaced | shapes — was | now |
|---|---|---|---|---|
| this repository | `carriage-ledger` | 7 | **6** | **1** |
| `-two-writers` | `title-resolution` | 9 | 4 | **1** |
| `-markers` | `carriage-ledger` | 3 | 3 | **1** |
| `-unplaced` (this feature's fixture) | `carriage-ledger` | 3 | 1 | **1** |

Under the rule as first ratified, every UNQUOTED interpolation was
shape-bearing — the promoted spec's path, the `[body]`/`[bullet]` unit-kind
list, a change-id list, an unresolved block's `why` clause — so one dropped map
entry reported SIX remedies where ONE was owed. This feature shipped that
faithfully, measured it, declined to widen it unilaterally because the delta's
third scenario pinned it, and put the amendment up.
`test_the_drift_grain_is_one_finding_per_arm_template` holds the real-tree row
against an independently written mask and an independently typed set of
per-template probes.

## Predicted movement: ZERO, and the diff says so

The class map is complete on this tree, so the fifth class reads `0`. Before and
after, both taken as clean `git archive` extractions of the merge base and of
this branch, over a FULL report:

```text
$ diff self-gate-before.txt self-gate-after.txt
126a127
> - unplaced-finding drift: 0 (`warning`)
```

**One line, and it is the new class row reading zero.** The headline is
`0 critical, 0 error, 0 warning, 7 info` on both sides; no other family section,
no ranked-plan row, no census figure moves.

## Gates

| gate | result |
|---|---|
| `python3 -m pytest tests/doc-health -q` | **1270 passed**, 7 warnings |
| CI shape — both sides clean extractions of the same base | 11 failed, **1250 passed**; the failure sets are IDENTICAL by name (all history-dependent), and 1229 → 1250 is exactly this feature's **+21** tests |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | **76 passed, 0 failed** |
| full-report movement diff | **exactly one line** |
| `git diff --stat <merge-base> -- .github/ openspec/` | **empty** |

**Mutation: 16 applied across four rounds, 16 killed, 0 survivors.** Four of them
survived a first attempt and each exposed a real gap — an adversarial title one
clause too short to reach the anchor; a fixture whose emission order and report
order agreed, so "the first of its shape in report order" could not fail; an
adversarial pin built in the wrong direction, passing by luck of the registry
order; and `_ArmTemplate.matches` relying on `re.match` with no `^`, unseeable
because the shipping path never shapes a drift finding. All four are now pinned,
and each pin carries a guard that fails if it ever stops biting.

## Scope

`.github/` and `openspec/` diffs against the merge base are **empty**: no
workflow file, and the packet's own task boxes tick at its archive act, which is
a separate later commit following this merge. Nothing else moves — no other
family, no `report.py`, no `families.py`, no `Finding` field, no registry, no
threshold. `specs/022-modified-block-currency-reporting/contracts/report-section.md`
is amended at all four of its class-enumeration sites and gains a § 5b for the
template registry and the mask, because a fifth class landing without that would
leave the corpus carrying a byte-level contract false about the code it
describes — which is the defect this family exists to catch.

## Reviewing

Start at `specs/026-unplaced-finding-drift/plan.md` § OPEN-1 (RULED AND
IMPLEMENTED) for the mechanism and the measurement, then `evidence/` — the
self-gate pair, `red-log.md` (every behaviour seen to fail before the module
moved), `mutation-round.md` (all four rounds, survivors and what they exposed),
`ci-shape.md` and `scope-diff.md`.

Refs #357

🤖 Generated with [Claude Code](https://claude.com/claude-code)
