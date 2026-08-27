# F1 — the modified-block-currency doc-health family

Realizes `openspec/changes/add-modified-block-currency-check` § 2 (tasks
2.1–2.10), the first of four Speckit features building that change. Ratified
2026-08-27 by Brett, verbatim "Ratify as-is". Feature:
`specs/019-modified-block-currency-family/`.

## What lands

The twenty-second deterministic check family. **A `MODIFIED` requirement block
that restates stale canon passes every gate in this repository and deletes canon
on archive** — it happened four times in one week (#351, #329) and a human
caught it every time. `openspec validate --strict` checks a delta's SHAPE, never
what promotion will do to the requirement being replaced; and
`promotion-fidelity` is structurally blind to it, because after an archive act
canon IS the delta, so a block that dropped seven scenarios and a canon now
missing them agree perfectly. The comparison that can see the loss is between an
ACTIVE delta and the canon it has not yet replaced — read while the change can
still be edited, which is the only moment the remedy is one line.

- `scripts/doc_health/modified_block_currency.py` — the family: the active-delta
  reader, the promoted-requirement reader, the normative unit derivation
  (backtick masking, the sentence split, bullet units, the undivided dated note,
  fenced blocks excluded), same-kind EXACT matching, three arms, the
  reserved-marker parser and its two forms, own-RENAMED-first title resolution,
  ordering BY DECLARATION, and the disposition read.
- `scripts/doc_health/families.py`, `scripts/doc_health/__init__.py` — the two
  registrations. **Absent from `FAMILY_RESOLUTION` deliberately.**
- The owed `## MODIFIED Requirements` block on `doc-health`'s "Deterministic
  check families", in the same commit as the registration.
- `tests/doc-health/test_modified_block_currency.py` — 97 tests.

## Three arms, four finding classes

| class | severity | granularity |
| --- | --- | --- |
| scenario-title completeness | `warning` | one per requirement, naming every omitted title |
| carriage ledger | `info` | AT MOST ONE per requirement, listing every uncarried unit |
| title resolution / ordering | `warning` | one per unresolved block or undecided ordering |
| marker defects | `info` | one per marker naming a unit the block still carries |

The numbers differ on purpose: the arms are three COMPARISONS between two
documents, and the fourth class is a defect in a DECLARATION.

**Findings sort SEVERITY-FIRST**, so the gate-bearing `warning` renders above
the editorial `info` rows. The ledger's population is standing by construction —
every legitimate MODIFIED block edits something — so on any real tree the one
precise signal is outnumbered, and a path-first sort buried it among them, which
is the exact failure the delta split the arms to avoid.

**Advisory at launch, in both halves** — `warning`/`info` severities AND
deliberate absence from `FAMILY_RESOLUTION`. The second half is the one that is
easy to lose: `report.uncited_resolutions` turns a `contested` finding that
vanishes between reports into an `error`, and every finding this family raises
names a block somebody is expected to CORRECT, so a `contested` class would red
the nightly on the first correction. Raising the scenario-completeness arm to
`error` and adding the contested class are ONE later decision by ruling; **no
flip is proposed for the ledger at all.**

## Measured movement

Two real single-repo runs, one with the family and one with
`--skip-family modified-block-currency`:

```text
without: 5 critical, 7 error, 42 warning,  4 info
with:    5 critical, 7 error, 43 warning, 13 info
movement:      0          0        +1        +9
```

**+1 `warning`, +9 `info`, every other family's report section byte-identical.**
The `error` and `critical` bands do not move, so a run configured
`--fail-on error` or `--fail-on critical` is unaffected by construction.

The one `warning` is `add-composed-view-authoring` /
`Composed views are read-only with a repository jump`, omitting canon's
`Gate verbs hide on a composed view`. On inspection it is a deliberate rename —
the case the reserved marker exists for — and **this PR does not claim it is a
defect.**

§ 2.1's block draws exactly ONE ledger finding against this change's own delta,
naming the two body sentences it changes. That is the packet's § 6.6 prediction
realized to the unit; it is expected, advisory, and must not be dispositioned,
because it is the evidence that the family reads its own packet.

## Sequencing: the packet's § 2.1 was unimplementable as written

`fam_family_enumeration` checks EVERY active delta's restatement of
"Deterministic check families" against the LIVE registry, independently. So
registering a twenty-second family while `add-family-enumeration-check` was
active emitted three findings against **that packet's** delta path — measured 0
at 21 registered, 3 at 22 — and no edit inside this change could clear them. The
packet's D5 proved half the problem (a proposal-only tree reds the gate) and
never measured the other half. Ruled: that change archived FIRST (`f027d3b3`),
this branch merged it, and § 2.1's block is written relative to CANON. The
two-writers instance § 2.1 was going to create therefore never existed.

## Evidence

- `python3 -m pytest tests/doc-health -q` — **1077 passed** (baseline 980, +97).
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — **75 passed, 0 failed**.
- `fam_family_enumeration` reads **0** against this tree; per-requirement
  scenario count on the restated requirement **8 → 8**, all eight titles
  identical to canon's, all three dated bold notes carried VERBATIM.
- `promotion_fidelity.py`, `duplicate_packet.py`, `report.py`,
  `.github/workflows/**` and every threshold: **no diff**. Their suites: 90
  passed.
- **Mutation round: 21 mutants, 21 killed**, re-run after every review nit. The
  round found THREE missing tests that twenty-one green tests had not — the
  `FAMILY_RESOLUTION` absence was documented in three places and asserted in
  none; the marker's change-id group was unpinned because the only
  quoted-template case also carried a placeholder date; and the no-basis
  guarantee was asserted on a run OUTCOME rather than on the reader's signature.
  All three are now pinned. The implementation review independently re-killed its
  own 15 mutants and found all 10 of its findings to be true positives.
- **Report ordering verified in a real run**: the family's section opens with the
  `warning`, not with an `info` row.

## What this does NOT close

**#330 stays open.** Its shape 1 — the post-archive safety net, diffing a
promoted spec against its own prior state across the archive commit — is NOT
built here: it needs a third measurement basis inside a family whose promoted
requirement obliges it to declare which of TWO it measured. The pre-archive gate
is the cheaper half and the one #330 itself calls "where it is cheap". Owner and
trigger are recorded in the packet's § 7.1.

Also not here, and not this feature's scope: F2's regression-fixture catalogue,
F3's asserted self-gate, F4's report section and workflow pin. The OpenSpec
change ships ACTIVE and archives only after this merges green.

## Decisions still flagged for veto

Eleven, listed in `specs/019-modified-block-currency-family/plan.md`
§ Decisions taken by the orchestrator. Four supply rules the ratified delta does
not write, and they are the ones a reviewer should read first:

- **O6** — the dated-bold-note predicate (a paragraph opening a bold run that
  carries an ISO date), measured against the notes canon actually holds.
- **O9** — prose under a scenario heading is a body unit; population 2 in this
  corpus. Dropping it would let a block move an obligation into scenario prose
  where neither carriage arm could see it.
- **O11** — carriage is SET-BASED, not multiset. 13 of 513 promoted requirements
  state one normalized unit twice, every instance a repeated scenario-bullet.
  Set semantics cannot lose a DISTINCT obligation; multiset would report a block
  for de-duplicating canon's own repetition.
- **Fenced code blocks are neither units nor markers** — without this the
  delta's OWN written-out marker examples, which promote into canon, parse as two
  real markers on the requirement that defines them.

Two further readings are recorded in the module docstring: a marker is voided
PER NAME rather than wholly, and a marker name matching no canon unit is ignored
fail-closed (the unit the author meant is still reported by whichever arm owns
it).

Refs #357 #329 #330

🤖 Generated with [Claude Code](https://claude.com/claude-code)
