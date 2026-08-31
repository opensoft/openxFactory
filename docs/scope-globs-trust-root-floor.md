# The `scope_globs` Scope Surface Is a Never-Clearable Trust-Root Floor

Status: ratified
Ratified by: add-structured-scope-substrate
Kind: reference
Owner: openxFactory (the `release-realization` capability and the
`scope_globs` substrate — `openspec/specs/release-realization/spec.md`,
`scripts/scope_globs.py`, `scripts/validate-scope-globs.py`).
Realizes: CRITICAL #1 (iv) of the 2026-08-28 `gate_rules_council` disposition of
`add-provenance-gated-autonomous-merge` (the "B" change), folded into its "Floor
primacy and per-repository floor instantiation" requirement.

This is **doctrine text realized as a record and an openxFactory-side check**
(add-structured-scope-substrate task 4.2). It states the trust-root property the
`scope_globs` substrate must hold in every repository that enables
provenance-gated autonomous merge. The mechanical ENFORCEMENT of the floor lives
in each enrolled repository's own merge-approval envelope and provenance-tie
verifier (B's downstream realization, tracked in that change's tasks); this
document records the requirement and the assertion openxFactory can make about
its own substrate.

## The requirement

The `openspec/changes/` surface carries the machine-readable path scope
(`scope_globs`) that the provenance-tie verifier reads to decide whether a fully
governed pull request may clear on the provenance axis. That makes it a
**trust-root source**. For the tie it feeds to be trustworthy, the surface must
hold four properties (the four the `release-realization` "Trust-root integrity of
the structured scope declaration" requirement obligates):

1. **Base-read.** The verifier reads `scope_globs` only from the base branch,
   never from a pull-request head. A pull request can therefore never present its
   own widened scope to the check that authorizes it.

2. **Ratification-covered.** The `scope_globs` bytes are part of the ratified
   change artifact and are covered by the change's ratification, so a governed
   pull request can never widen its own scope post-ratification.

3. **Non-author-mutable.** The `openspec/changes/` surface that carries
   `scope_globs` **SHALL be a never-clearable floor member of EVERY repository
   enrolled for provenance-gated autonomous merge**, and **no autonomous
   provenance merge SHALL write to it**. This closes the self-authorization
   recursion in which an earlier autonomous merge could author the scope a later
   tie corroborates against.

4. **Frozen after ratification.** Mutation of `scope_globs` after ratification is
   rejected at the archive gate (the "Scope retention at archive" requirement,
   realized by `scope_globs.scope_retention_at_archive`).

A repository that would floor any trust-root source **outside** its own
tree-validated floor SHALL NOT enable a non-docs provenance-eligible class: a
trust-root source the autonomous path could write breaks property 3.

## The floor overrides the scope at check time

`scope_globs` validation (`openspec validate`-equivalent, in neutral openxFactory)
stays **floor-agnostic**: it never rejects a glob merely because the glob names a
path that lies inside some repository's never-clearable floor, because the floor
is tree-specific and per-repository and openxFactory cannot know it without
coupling to every enrolled repository's tree. The floor is applied at **check
time** by the verifier, which subtracts the enrolled repository's own base-branch
`gate_integrity.never_clearable_paths` from the authorized set. One floor
authority per repository governs; `scope_globs` can never authorize a floor path;
**floor always wins**. A change MAY over-declare scope (even naming a floor path);
the verifier still parks any pull request whose diff touches the floor.

## What openxFactory asserts, and what it does not

openxFactory owns and can assert:

- The **freeze** — `scripts/validate-scope-globs.py --archive-gate` rejects a
  post-ratification `scope_globs` mutation (property 4).
- The **floor-agnostic validator** — `scripts/validate-scope-globs.py` conforms a
  present `scope_globs` to the shared envelope glob dialect without floor
  knowledge.

openxFactory does **not** enforce, and each enrolled repository MUST, in its own
`.github/merge-approval-envelope.yml` and provenance-tie verifier:

- Make `openspec/changes/` (and B's other trust-root sources) a never-clearable
  floor member of the enrolled surface (property 3, enforcement half).
- Base-read `scope_globs` and park any autonomous candidate that would itself
  write a `scope_globs` declaration (properties 1 and 3).
- Apply the floor override at check time (floor wins over declared scope).

These enrolled-repository obligations are B's realization, built against a current
codexFactory checkout and tracked under
`add-provenance-gated-autonomous-merge` — NOT under
`add-structured-scope-substrate`, whose surface is the neutral substrate alone.
