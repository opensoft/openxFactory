# An upstream issue for `fission-ai/openspec` — FILED 2026-09-05 as https://github.com/Fission-AI/OpenSpec/issues/1793

Status: record
Kind: draft correspondence
Written: 2026-09-05
Author: lane `codexfactory-0d`

> **FILED 2026-09-05 as https://github.com/Fission-AI/OpenSpec/issues/1793, on Brett Heap's word ("file the upstream issue"), by lane codexfactory-0d under Brett's GitHub account.** The paragraph below is kept as the record of the draft's standing before that word; the body was posted as written, with the title corrected to one line after a mangled first post.
>
> Original standing: THIS HAS NOT BEEN POSTED ANYWHERE, AND THIS LANE WILL NOT POST IT.
> It is exit 3 of the three #673's evidence record enumerated. Brett Heap ruled
> **"take exit 2"** on 2026-09-05 — the dispositioned exception, which this
> packet implements. Exit 3 is not excluded by that ruling and the two are not
> exclusive: exit 2 is what this estate does about its own gate, exit 3 is what
> it would ask of the tool. **Filing it is Brett's decision.** If it is filed
> and upstream lands a fix, the two dispositions in
> `contracts/openspec-cli-pin.yaml` go STALE at the next bump and the pin
> REFUSES until they are deleted — which is the mechanism removing them, and the
> outcome everybody wants.
>
> Nothing below has been sent to any tracker, mailing list or maintainer.

---

## Title

`validate --strict`: scenario-currency check has no way to declare a deliberate
scenario rename, so a narrowing reads as an omission

## Body

### Summary

`validate --strict` reports an `ERROR` when a `## MODIFIED Requirements` block
omits a scenario the current spec still carries. The check compares scenario
TITLE SETS, so a deliberate **rename** — the same behaviour, narrowed and
retitled — is indistinguishable from an accidental **drop**, and the only edit
that satisfies the check is to restore the old title. Where the rename was the
point of the change, that means reverting the change.

There is already precedent inside this very check for an author-declared
exclusion: a block whose requirement is renamed away by a
`## RENAMED Requirements` section in the same delta is skipped
(`renamedAway` in `dist/core/validation/validator.js`). **What is missing is the
same affordance one level down, at the scenario.**

### Reproduction (minimal, complete)

`openspec/specs/example-capability/spec.md`

```markdown
## Requirements

### Requirement: Composed views are read-only with a repository jump
A composed view SHALL be read-only, and SHALL offer a jump to the repository.

#### Scenario: Gate verbs hide on a composed view
- **WHEN** a composed view is rendered
- **THEN** the gate verbs are hidden
```

`openspec/changes/rename-a-scenario/specs/example-capability/spec.md`

```markdown
## MODIFIED Requirements

### Requirement: Composed views are read-only with a repository jump
A composed view SHALL be read-only, SHALL offer a jump to the repository, and SHALL admit document creation.

**Merged into `Tile-bound gate verbs hide on a composed view` by rename-a-scenario (2026-09-05):** `Gate verbs hide on a composed view`

#### Scenario: Tile-bound gate verbs hide on a composed view
- **WHEN** a composed view is rendered
- **THEN** the TILE-BOUND gate verbs are hidden
- **AND** document creation stays available
```

Plus a two-line `proposal.md` and `tasks.md`. Then:

```
$ openspec validate --all --strict      # @fission-ai/openspec@1.12.0
✓ spec/example-capability
✗ change/rename-a-scenario
  ✗ [ERROR] example-capability/spec.md: MODIFIED "Composed views are read-only with a repository jump" omits scenario(s) the current spec still has: "Gate verbs hide on a composed view". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
Totals: 1 passed, 1 failed (2 items)

$ openspec validate --all --strict      # @fission-ai/openspec@1.2.0
Totals: 2 passed, 0 failed (2 items)
```

Doing what the message asks — copying `Gate verbs hide on a composed view` back
into the block — reinstates an unconditional statement the change exists to
narrow, beside the narrower successor that contradicts it.

### Why "just keep both scenarios" is not available here

The two titles are not two behaviours. `Tile-bound gate verbs hide on a composed
view` is the SAME behaviour with a narrower scope, because the same change
deliberately admits document creation on a composed view. Carrying both would
put a contradiction in one requirement block.

### What we do today, and why we would rather not

We run the CLI through a content-addressed pin
(`contracts/openspec-cli-pin.yaml`) and reconcile its `--json` findings against
an enumerated, cited, per-finding disposition list, so exactly two findings in
our corpus are accepted with a written citation and everything else fails. It
works, and it is strictly worse than the check being able to read the
declaration: our suppression lives in our pin, so it is invisible to anyone
reading the delta, and it has to be re-derived at every CLI upgrade.

### Asks, in order of preference

1. **Honour a declared scenario rename.** Either a first-class
   `## RENAMED Scenarios` (or a scenario-level entry under the existing
   `## RENAMED Requirements`) that the currency check consults exactly as it
   already consults `renamedAway`; or a recognized in-block marker line naming
   `old title` → `new title`. Our house form, in use since 2026-08 and defined
   by our own promoted spec, is:

   ```
   **Merged into `<new scenario title>` by <change-id> (<date>):** `<old scenario title>`
   ```

   We are not asking for OUR spelling — a canonical one you choose is better.
   What matters is that a DECLARED rename is distinguishable from a silent drop,
   which is the whole distinction the check is trying to make.

2. **Failing that, per-finding suppression the delta can carry** — an
   `openspec/config.yaml` rule list, or a recognized inline directive, keyed by
   check id + item + requirement, so the exception is visible in the repository
   that takes it rather than in a wrapper around the CLI.

3. **Failing both, a severity knob** for this one check, so a corpus that has
   made the judgment once can run `--strict` without either reverting a decision
   or filtering the tool's output. This is the weakest ask and we mention it only
   so the option is on the table.

### Notes for whoever picks this up

- The check is `dist/core/validation/validator.js`, the loop over `modified`
  producing `omits scenario(s) the current spec still has`.
- It already carries one author-declared exclusion (`renamedAway`), so the shape
  of the fix has precedent in the same function.
- `1.2.0` does not carry the check at all; it appears somewhere in `1.3`–`1.12`.
  We upgraded 1.2.0 → 1.12.0 in one step and did not bisect, so we cannot name
  the introducing release.
- Happy to supply the two real deltas from our corpus if a synthetic
  reproduction is not enough, and happy to test a patch — we run this CLI
  digest-pinned in CI, so we can pin a candidate build precisely.
