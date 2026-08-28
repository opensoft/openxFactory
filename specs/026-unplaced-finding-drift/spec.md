# Feature Specification: The fifth finding class — unplaced-finding drift

**Feature Branch**: `026-unplaced-finding-drift`

**Created**: 2026-08-27

**Status**: Draft

**Realizes**: `openspec/changes/add-unclassified-finding-class` (ratified
2026-08-27 by Brett, in-session commissioning, verbatim "Amend now"; merged as
PR #446, squash `86b7ca3f`). ONE ADDED requirement in the `doc-health`
capability: "A modified-block-currency finding its own class map cannot place
is itself a finding". The packet's `tasks.md` § 2 (2.1–2.15) is this feature's
plan at task grain.

**Input**: Speckit realization of `add-unclassified-finding-class`: the
modified-block-currency family's fifth finding class `unplaced` — when the class
map cannot place a finding's rule text, emit ONE warning per distinct unplaced
rule shape per run, anchored pattern, own severity constant, action line naming
the class-map path, residual row keeps rendering, not contested; plus the seven
F4 pins that move, the unplaced fixture tree with a monkeypatched pass, the F3
fourth probe, the F4 contract amendment, and a numeral sweep.

## Why this exists (one paragraph, from the ratified proposal)

The modified-block-currency family already detects that its own class map has
drifted, and then tells nobody who can act on it. `classify` is fail-closed: a
rule text no pattern matches is not absorbed into a neighbouring class, it falls
to a named residual row in the family's report block. That row is prose. It has
no severity, so no `--fail-on` configuration reaches it; it is not a finding, so
the ranked plan — the workflow this capability builds reports for — never
carries it. The thing it reports is a defect in this capability's own tooling,
and nothing else in the corpus reports it. It reads zero on this tree today,
which is the argument for pinning that state now rather than after it moves.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A steward working a report's ranked plan learns the map drifted (Priority: P1)

A steward reads a doc-health report's ranked plan, which is the list of work the
report produces. Today, if the modified-block-currency family emitted a finding
whose rule text its own class map could not place, the only trace is a prose
residual row inside that family's report block — invisible to the plan, to
`--fail-on`, and to anyone who does not read the block by eye. After this
feature, the drift arrives in the plan as a `warning` naming how many findings
carry the unplaced shape, quoting the first of them verbatim, and stating both
remedies.

**Why this priority**: this is the whole change. Every other story is a
consequence of making the residual reachable as work.

**Independent Test**: run the family over a tree whose class map has drifted
behind its arms (induced by removing one class pattern) and read the rendered
report: a `warning` row for the family appears in the ranked plan, with the
count, the verbatim rule text, the repository, the delta path and the action
line.

**Acceptance Scenarios**:

1. **Given** a run in which the class map places every finding the family
   emitted, **When** the family runs, **Then** no additional finding is emitted
   and the family's rendered class counts still sum to the rows the report
   prints for it.
2. **Given** a run in which one or more findings carry a rule text no pattern of
   the class map matches, **When** the family runs, **Then** exactly one
   additional `warning` finding is emitted for each distinct shape among them,
   naming that shape's count and quoting verbatim the rule text of the first of
   them in the family's own report order.
3. **Given** such an additional finding, **When** the report is rendered,
   **Then** it appears in the ranked plan as a ready-to-stage work item stating
   its severity, repository, path and action, on the same terms as every other
   finding — and the family's residual row still renders in the family's own
   report block.

---

### User Story 2 - The tally still sums, and the new finding is never counted by the residual it reports (Priority: P1)

The family's report block exists so a reader can trust one line without
counting. A finding that reported drift and was itself unplaced would be counted
by the very residual it names: the count would name itself, and the next run
would report a drift the map had just been extended to describe.

**Why this priority**: it is the coherence condition on Story 1. Without it the
feature makes the one line it exists to protect less trustworthy, not more.

**Independent Test**: over a drifted run, read the rendered block and the rows
beneath it — the class counts (including the new class and the residual) sum
exactly to the rows, and the drift finding is counted in the new class rather
than in the residual.

**Acceptance Scenarios**:

1. **Given** a drifted run, **When** the block is rendered, **Then** the drift
   finding is counted in the fifth class and the residual row counts only the
   arms' unplaced findings, and the two counts plus the arms' counts equal the
   number of rows printed.
2. **Given** an unplaced rule text that itself begins with the phrase an arm's
   rule texts begin with, and a drift finding that quotes it, **When** the drift
   finding is classified, **Then** it is placed in the fifth class and not under
   the class its quotation resembles.
3. **Given** a requirement title supplied by the corpus that embeds the fifth
   class's own opening phrase, **When** the resulting arm finding is classified,
   **Then** exactly one class pattern matches it.

---

### User Story 3 - The drift finding disappears when the map is extended, and that is not a contested resolution (Priority: P2)

The remedy for this finding is to extend the class map. A finding designed to
stop being emitted the moment somebody fixes the thing it names must not have
its disappearance reported as an uncited resolution on the next run.

**Why this priority**: it is the launch-safety half. Getting it wrong reds the
nightly on the run that proves the mechanism worked.

**Independent Test**: extend the map with a pattern that places the named rule
text, re-run over the same tree, and observe that the additional finding is gone,
the residual row does not render, and the family is absent from the resolution
registry so no `contested` classification exists to turn the disappearance into
an error.

**Acceptance Scenarios**:

1. **Given** a drifted run that emitted the additional finding, **When** the
   class map gains a pattern that places the rule text the finding named and the
   family runs again over the same tree, **Then** the additional finding is not
   emitted and the residual row does not render.
2. **Given** the family after this feature, **When** the resolution registry is
   read, **Then** the family is still absent from it, so none of its findings is
   classified `contested`.
3. **Given** the reserved flip of the scenario-title arm to `error`, **When**
   that flip is simulated over the module's own source, **Then** the fifth
   class's band is unmoved.

---

### User Story 4 - Two drifted shapes are two findings (Priority: P2)

A drifted class map may be short by more than one pattern. Two genuinely
different unplaced rule shapes are reported apart, so both drifted texts are
quoted; two findings that differ only in a quoted span and a digit run are one
shape and must not be reported twice.

**THE GRAIN IS ONE FINDING PER ARM TEMPLATE — one shape, one map entry, one
remedy.** Two rule texts are one shape where they come from the same template,
whatever their interpolated values: the requirement title, the counts, the
promoted spec's path, the unit-kind list, a change-id list, an unresolved
block's `why` clause.

That is an AMENDMENT to the delta, ruled 2026-08-28 by Brett ("Amend: shape =
arm template, all interpolations masked"). As first ratified the rule masked
quoted spans and digit runs only, leaving every unquoted interpolation
shape-bearing: dropping `carriage-ledger` on this repository left SEVEN unplaced
findings in SIX shapes where one map entry would have placed all seven. This
feature shipped that faithfully, measured it, declined to widen it unilaterally
because the delta's third scenario pinned it, and put the amendment up. All four
measured figures now read ONE — see `plan.md` § OPEN-1, closed.

**Why this priority**: it is the packet's rewritten decision D3, and the half
that decides whether both drifted texts are quoted.

**Independent Test**: construct two unplaced findings whose rule texts are equal
after every quoted span and every digit run is masked, and two whose rule texts
differ outside those; observe one additional finding for the first pair naming
the count two, and two additional findings for the second.

**Acceptance Scenarios**:

1. **Given** two unplaced findings whose rule texts are equal after every
   single-quoted span, every double-quoted span and every run of digits is
   replaced by a fixed placeholder, **When** the family runs, **Then** ONE
   additional finding is emitted for both, naming the count two.
2. **Given** two unplaced findings whose rule texts differ outside their quoted
   spans and digit runs, **When** the family runs, **Then** TWO additional
   findings are emitted.
3. **Given** any drifted run, **When** the additional findings are read,
   **Then** each carries the repository and delta path of the FIRST finding of
   its shape in the family's own report order, and two runs over the same tree
   agree byte for byte.

---

### User Story 5 - The corpus's byte-level contract stays true about the code (Priority: P3)

The report block is described by a byte-level contract that enumerates the four
classes four times over. A fifth class landing without amending it would leave
the corpus carrying a contract that is false about the code it describes — the
exact class of defect the family that gains this class exists to catch.

**Why this priority**: it is documentation-fidelity rather than behaviour, and
it is a hard requirement of the ratified packet.

**Independent Test**: read the contract's four enumeration sites and the module,
and confirm the fifth class appears in each with the bullets, the worked
example, the class-map grammar and the action-line table agreeing with the code.

**Acceptance Scenarios**:

1. **Given** the amended contract, **When** its per-class bullet list, worked
   example, class-map grammar and action-line table are read, **Then** each
   enumerates five classes and the residual bullet is unchanged.
2. **Given** the module and its three test files, **When** every prose numeral
   stating a count of classes, severities, rule shapes or block rows is read,
   **Then** none states a count this feature makes false.

---

### Edge Cases

- **The class map is complete, which is the normal state.** No additional
  finding, no residual row, and the class block gains one row reading `0`. This
  is the predicted state of every run on this tree.
- **A run with no findings at all.** The block still renders with all five
  counts at `0`; nothing about the fifth class changes the quiet-run rendering.
- **A skipped family.** No block renders at all, for either skip shape, and the
  fifth class does not change that.
- **A drift finding whose quoted rule text begins in the shape of an arm's.**
  Placed in the fifth class, never under the class its quotation resembles.
- **A corpus-supplied requirement title that embeds the fifth class's own
  opening phrase.** Exactly one class pattern still matches the resulting arm
  finding — the anchor is what makes this true.
- **No corpus can produce an unplaced rule text while the map is complete.**
  Every rule text the family constructs is one of five fixed prefixes plus a
  Python `repr` of a title, and the title pattern admits every `repr` Python can
  emit. Measured at packet review: 20,065 constructed rule texts over 13
  adversarial and 4000 random titles, 0 unplaceable. The behavioural trigger for
  every test of this feature is therefore the drift itself — one pattern removed
  from the class map — never a crafted fixture title.
- **An aggregation run over many repositories.** The class map is a module
  constant compiled once per process, so one finding names one example per
  shape; a second repository's instance of the same shape is counted but not
  quoted. Named as given up, per the packet's D3.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The family MUST emit ONE additional `warning` finding per run for
  each DISTINCT SHAPE of rule text its own class map does not place. *(delta ¶1;
  packet § 2.4)*
- **FR-002**: Each such finding MUST name how many of that run's findings carry
  that shape. *(delta ¶1)*
- **FR-003**: Each such finding MUST carry, verbatim, the rule text of the first
  finding of that shape in the family's own report order. *(delta ¶1)*
- **FR-004**: Each such finding MUST carry that first finding's repository and
  delta path. *(delta ¶1)*
- **FR-005**: Where the map places every finding the family emits, NO such
  finding MUST be emitted. *(delta ¶1; scenario 1)*
- **FR-006**: Two unplaced findings MUST be treated as ONE SHAPE where their
  rule texts are equal after every single-quoted span, every double-quoted span
  and every run of digits has been replaced by a fixed placeholder. *(delta ¶2;
  packet § 2.4)*
- **FR-007**: The finding's action line MUST be, verbatim, "extend the class map
  in `scripts/doc_health/modified_block_currency.py`, or fix the drifted rule
  text the finding names", and MUST interpolate no path of its own. *(delta ¶3;
  packet § 2.1)*
- **FR-008**: The finding MUST itself be placed by the class map, in a FIFTH
  class of the family's own registry carrying the `warning` band and that action
  line, so that it is never counted by the residual it reports. *(delta ¶4)*
- **FR-009**: The pattern that places that class MUST be anchored at the start
  of the rule text. *(delta ¶5)*
- **FR-010**: The fifth class's band MUST come from its OWN module-level
  severity constant, distinct from the constant the scenario-title arm reads, so
  the reserved flip of that arm cannot drag it. *(packet § 2.1; § 4.1)*
- **FR-011**: The fifth class's id and label MUST NOT contain the substring
  `unclassified`; the id is `unplaced` and the label is `unplaced-finding
  drift`. *(packet § 2.2; proposal D2)*
- **FR-012**: The fifth class MUST be appended LAST in the class registry and
  MUST carry no gloss. *(packet § 2.2)*
- **FR-013**: The family's residual row MUST continue to render whenever its
  count is nonzero, unmoved and unreworded. *(delta ¶6; packet § 2.5)*
- **FR-014**: `classify`, `class_counts` and `class_summary` MUST keep their
  signatures and their no-context discipline. *(packet § 2.5)*
- **FR-015**: The family MUST remain absent from the resolution registry, so
  the finding is never classified `contested`. *(delta ¶7)*
- **FR-016**: The rendered class counts MUST continue to sum to the rows the
  report prints for the family, in every state. *(delta scenarios 1–2)*
- **FR-017**: The class block MUST remain not-a-finding: no line of it may be
  read back by the previous-report parser, reach the ranked plan, or move a
  headline count. *(existing pin; packet § 2.7)*
- **FR-018**: This feature MUST add no deterministic check family and MUST NOT
  restate the "Deterministic check families" enumeration or its numerals.
  *(delta ¶8)*
- **FR-019**: The byte-level report-section contract MUST be amended at all four
  of its class-enumeration sites — the per-class bullets, the worked example,
  the class-map grammar and the action-line table — leaving the residual bullet
  unchanged. *(packet § 2.9)*
- **FR-020**: Every prose numeral in the module and its test files that states a
  count this change makes false MUST be corrected. *(packet § 2.12)*
- **FR-021**: The family's self-gate over the real tree MUST assert the fifth
  class reads zero, with a positive control on the probe string. *(packet
  § 2.10)*
- **FR-022**: The module-surface snapshot MUST cover the new severity constant,
  and the public-callable list MUST be unchanged. *(packet § 2.11)*
- **FR-023**: A fixture tree MUST exist that drives the fifth class through the
  family, the classifier, the summary and the renderer under an induced drift,
  rather than through a constructed `Finding`. *(packet § 2.8)*
- **FR-024**: Nothing outside the named surface may move: no workflow file, no
  `openspec/` edit, no other family, no change to the shared `Finding` grammar,
  the renderer, the ranked-plan or finding grammars, the family-summary
  registry, the resolution registry, the governed corpus, the lifecycle scan set
  or any threshold. *(packet § 2.15; proposal Impact)*

### Key Entities

- **Finding class** — a value in the family's own ordered registry carrying an
  id, a rendered label, a band read from a module severity constant, an action
  line, and an optional gloss. Five after this feature.
- **Class map** — the ordered list of (class id, anchored pattern) pairs the
  classifier reads a finding's rule text against, first match wins, with a
  fail-closed residual.
- **Rule shape** — the identity a run groups unplaced findings by: the rule text
  with every quoted span and every digit run masked to a fixed placeholder.
- **Residual row** — the report block's named line for findings the map does not
  place; rendered only when nonzero; not a finding, and it stays that way.
- **Drift finding** — the new `warning`: one per distinct unplaced rule shape
  per run, placed by the map into the fifth class.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On a run whose class map places every finding, the number of
  findings the family emits is unchanged from before this feature, in every
  severity band. Measured on this repository at the feature's branch point:
  0 `warning`, 7 `info`, class counts 0 / 7 / 0 / 0, residual 0 — before and
  after.
- **SC-002**: On a run with an induced drift, exactly one additional `warning`
  reaches the ranked plan per distinct unplaced rule shape, and zero additional
  findings reach it per repetition of a shape already reported.
- **SC-003**: The rendered class counts equal the rendered rows on every fixture
  tree and on the real tree, in the placed state and in the drifted state.
- **SC-004**: Every one of the delta's six scenarios has at least one named test
  that fails for the stated reason before the module moves.
- **SC-005**: No run configured to fail on `error` or `critical` changes its
  verdict because of this feature: every finding this family emits remains
  `warning` or `info`.
- **SC-006**: A reviewer reading the byte-level report-section contract and the
  module finds five classes enumerated at every one of the contract's four
  enumeration sites, and no prose numeral in the module or its tests stating a
  count the code contradicts.
- **SC-007**: The full doc-health test suite is green, and the count of tests it
  collects moves only by the tests this feature adds.

## Assumptions

- The three orchestrator decisions of the ratified packet — D1 (ADDED-only, no
  MODIFIED block on the currency requirement), D2 (a fifth finding class with an
  anchored pattern rather than an unplaced finding or a severity on the report
  block), D3 (one finding per distinct unplaced rule shape per run) — are
  applied as ratified and are NOT re-decided here. They remain flagged for veto
  in the packet; a veto of D1 re-opens the packet, not this feature.
- The predicted movement on this tree is ZERO in every band, because the class
  map is complete here. The before figure is taken at this feature's own branch
  point rather than copied from the packet, since the arms' population moves as
  active changes land.
- No crafted fixture title can produce an unplaced rule text while the map is
  complete (measured: 20,065 constructed rule texts, 0 unplaceable), so every
  behavioural test of the fifth class induces the drift by removing one pattern
  from the class map — which is precisely the live condition "the map has
  drifted behind the arms".
- The reserved flip of the scenario-title arm to `error` is neither advanced nor
  blocked by this feature. The fifth class's band is deliberately not part of it.
- The packet's `tasks.md` boxes are ticked at its archive act, not by this
  feature; this feature makes no `openspec/` edit.

## Out of Scope

- Any change to another check family, to the shared `Finding` grammar, to the
  renderer, to the ranked-plan or finding grammars, to the family-summary or
  resolution registries, to the governed corpus, to the lifecycle scan set, or
  to any threshold.
- Any workflow file change; any `openspec/` change, including ticking the
  packet's own task boxes or archiving it.
- Extending the residual/class-block mechanism to any other family — no other
  family has a class map, and whether the mechanism should spread is a separate
  question the packet names and does not open.
- Proposing the masked-rule-text shape rule as a general finding-identity rule
  for the package; it is written for this family's rule-text grammar alone.
- Advancing or blocking the reserved severity flip.
