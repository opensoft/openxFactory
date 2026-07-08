# Design: Concretize Prose Tagging Syntax

## Decision 1: HTML comments, not visible Markdown markers

The staged fragment's first open question: markers as HTML comments
(`<!-- xspec:... -->`) are invisible in rendered views — feature or hazard?

**Decision: HTML comments.** Rationale:

- The markers are machine contract surface, not reader content. A visible
  marker (e.g. a blockquote badge or bracketed tag line) renders as if it
  were part of the governance prose itself — precisely the
  policy-contamination failure mode the explicit-delta rule exists to
  prevent. Rendered text must never carry tooling directives that a reader
  could mistake for normative content.
- The reviewers who gate lifecycle transitions work in source — commits,
  diffs, PR reviews — where comments are fully visible. Every gate in
  `docs/document-lifecycle.md` is a reviewable source-level step.
- The rendered-invisibility hazard is real but is mitigated structurally:
  the doc-health deterministic pass inventories every marker, so
  rendered-view readers get marker visibility through the health report
  rather than through inline noise. Until the checker lands, `grep -rn
  'xspec:'` is the inventory.
- HTML comments pass through Markdown renderers (GitHub, NotebookLM source
  ingestion) without breaking tables, lists, or headings, and grep
  identically to any visible syntax.
- Precedent: the brainstorm design and the staged fragment already use
  comment fences; no existing material needs re-tagging.

## Decision 2: No nesting, no heading-spanning

The fragment's second open question: may `xspec:candidate` blocks nest or
span headings?

**Decision: neither.**

- **No nesting.** One block selects one coherent passage for one target
  capability. A nested block would make the enclosing block's extraction
  unit ambiguous (does the inner passage belong to both targets?). Prose
  that feeds two capabilities gets two sibling blocks, duplicating the
  lines if necessary — duplication inside comment fences is cheap;
  ambiguous extraction is not.
- **No spanning heading boundaries.** A block MUST open and close with no
  Markdown heading (any level) between its fences. Conversion tooling
  anchors an extracted passage to its enclosing section; a block that
  crosses sections has no single anchor, and checking it would require a
  full Markdown AST. Keeping blocks within a section makes hygiene
  enforceable with a plain line scan — the property that keeps the
  deterministic pass deterministic. A passage covering several sections is
  tagged with one block per section.

## Decision 3: One canonical grammar under the `xspec:` namespace

All markers share the namespace prefix `xspec:` inside an HTML comment,
with space-separated, unquoted `key=value` attributes:

```text
<!-- xspec:candidate target=<capability> -->
...tagged prose...
<!-- /xspec:candidate -->

<!-- xspec:supersedes spec=<capability>/<requirement-slug> change=<change-id> -->
```

- `<capability>` is a spec capability id as it appears under
  `openspec/specs/` (or in an active change's `specs/` while the capability
  is pre-promotion).
- `<requirement-slug>` is the kebab-case of the requirement name, e.g.
  `document-lifecycle/explicit-delta-rule`.
- `change=<change-id>` is included as soon as the OpenSpec change exists.
  A supersedes marker without `change=` is legal at capture time — the
  marker is what makes the delta machine-visible before the proposal is
  written — but the doc-health pass ages it: a marker that never acquires a
  change id is a finding, not a permanent state.
- Grep contract: the literal string `xspec:` appears in governance
  Markdown only inside well-formed markers. The canonical inventory is
  `grep -rn 'xspec:' --include='*.md'`; any hit that does not parse against
  the grammar is a hygiene finding. This is what "one canonical grep-able
  syntax" means operationally.

## Decision 4: Candidacy is block-level only

The doc-health-pipeline brainstorm floated a doc-level
`Status: spec-candidate` header alongside block fences. The staged fragment
already dropped it; this change ratifies the drop.

- The `Status:` taxonomy is a closed eight-value list ratified by
  `add-document-lifecycle-vocabulary`. `spec-candidate` would reopen it and
  conflate lifecycle *state* with conversion-queue *membership* — a
  document can be `draft` and have three tagged passages, or `ratified`
  with none. The two axes stay orthogonal.
- A whole document worth converting is expressed honestly: one or more
  candidate blocks around the passages that actually convert. "Tag the
  whole file" almost always over-selects; forcing block fences forces the
  selection decision.
- Staged fragments (`ideation/staging/<topic>/`) remain the structural
  exception: their headers already carry target capability and delta type,
  so they are machine-queued without inline markers.

## Alternatives considered

- **Visible Markdown badge syntax** (e.g. `> [!XSPEC-CANDIDATE ...]`) —
  rejected per Decision 1: renders as content, and GitHub-style alert
  syntax is renderer-specific.
- **YAML frontmatter tag lists** (file-level index of tagged ranges) —
  rejected: line-range references rot on every edit; fences travel with
  the prose they select.
- **Allowing nesting with target inheritance** — rejected: saves keystrokes
  in a rare case at the cost of AST-grade parsing in the common case.
- **Requiring `change=` on every supersedes marker** — rejected: the marker
  must be placeable the moment prose diverges from promoted policy, which
  is typically before a change id exists; aging covers the gap.
