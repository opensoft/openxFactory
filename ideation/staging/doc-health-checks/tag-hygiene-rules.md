# Staged: Tag Hygiene Rules For The Doc-Health Pipeline

Status: staged
Kind: reference
Repository context: openxFactory
Target: the codexFactory doc-health implementation proposal (deterministic
pass); companion to [status-check-rules.md](status-check-rules.md); staged
per task 3.1 of the
[concretize-prose-tagging-syntax](../../../openspec/changes/concretize-prose-tagging-syntax/proposal.md)
change, which defines the canonical marker grammar these checks enforce.

## Grep contract

The literal string `xspec:` appears in governance Markdown only inside
well-formed markers. The complete inventory is:

```sh
grep -rn 'xspec:' --include='*.md'
```

Any hit that does not parse against the grammar below is a hygiene finding,
with one exclusion: hits inside fenced code blocks (``` fences) or inline
code spans (backtick-quoted) are documentation examples of the syntax
(e.g. in `docs/document-lifecycle.md`, the prose-tagging staged fragment,
and this file), not live markers — the checker skips them for all rules
below. A marker is live only when the HTML comment is raw line content. No Markdown AST is required: all checks are line-scan plus code-fence
and candidate-fence pairing within heading sections.

## Canonical grammar

```text
<!-- xspec:candidate target=<capability> -->        open fence
<!-- /xspec:candidate -->                           close fence
<!-- xspec:supersedes spec=<capability>/<requirement-slug> change=<change-id> -->
```

Attributes are space-separated, unquoted `key=value`. `<capability>` is a
spec capability id under `openspec/specs/` (or in an active change's
`specs/` while pre-promotion); `<requirement-slug>` is the kebab-case
requirement name. `change=` on a supersedes marker is optional until the
OpenSpec change exists.

## Checks the deterministic pass MUST implement

1. Well-formedness — every `xspec:` occurrence parses as exactly one of the
   three canonical forms with the required attributes (`target=` on
   candidate opens; `spec=` on supersedes). Unknown directive, missing or
   unknown attribute, malformed value = finding.
2. Target resolution — every `target=<capability>` and
   `spec=<capability>/<requirement-slug>` resolves to a capability (and
   requirement) under `openspec/specs/` or in an active change's spec
   deltas; every `change=<change-id>` resolves to an existing change
   (active or archived). Dangling target = finding.
3. Fence structure — candidate fences pair up in document order with no
   nesting, no Markdown heading (any level) between an open fence and its
   close fence, and no unmatched open or close fence. Violation = finding.
4. No doc-level candidacy — no `Status:` header anywhere uses
   `spec-candidate` (candidacy is block-level only). Occurrence = finding.
5. Supersedes aging — an `xspec:supersedes` marker without `change=` older
   than the aging threshold is an aging finding (threshold shared with the
   staged-item aging open question in
   [nightly-run-shape.md](nightly-run-shape.md)).
6. Exclusions — `Status: record` docs are excluded from the conversion
   queue; a candidate block inside one = finding. `ideation/brainstorm/`
   content may carry markers (tagging is legal anywhere), but only hygiene
   is checked there — brainstorm prose is never queued directly.

## Queue derivation

The conversion queue the agentic pass consumes is: every well-formed
candidate block outside `record` docs and `ideation/brainstorm/`, plus
every staged fragment header (`ideation/staging/<topic>/` — target
capability + delta type; no inline markers required).
