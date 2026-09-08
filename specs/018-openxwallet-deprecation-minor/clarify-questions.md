# Clarification round — 018-openxwallet-deprecation-minor

**Path**: `/home/brett/projects/xFactory/openxFactory-worktrees/P2.5-deprecation-minor/specs/018-openxwallet-deprecation-minor/clarify-questions.md`

**Session**: 2026-08-27
**Status**: NO OPEN QUESTIONS — nothing is blocked on an answer.

This file exists so the two decisions taken from authority rather than asked are
visible in the feature directory, not only in `spec.md`'s Clarifications section.
Both are already applied. Overturning either is a one-line edit plus a
regenerated inventory; neither changes the shape of the work.

---

## D-1 (decided) — the successor tag in `relocating.tag`

`design.md` D5 and `tasks.md` 5.1 both write the literal
`tag: wallet-v1.0`. **Applied instead: `wallet-v1.1`.**

Why the literal is stale rather than authoritative:

1. `tasks.md`'s own preamble: "`wallet-v1.1` (§4) is one auditable additive-minor
   diff on top and touches none of the eight digested artifacts; **openxFactory's
   pin at P3 records `wallet-v1.1`**."
2. `proposal.md`'s `code_surface` front-matter calls `wallet-v1.1` "**the tag
   openxFactory actually pins**".
3. `wallet-v1.1` is tagged on `opensoft/openXwallet` (`63f5a1ad`) as of
   2026-08-26; D5 was authored before it existed.
4. The marker's whole job is to tell a consumer where to go. Naming `wallet-v1.0`
   would name a tag that is not the migration target, and the byte-identity floor
   D5 protects is proven at `wallet-v1.0` regardless of what this marker says —
   the two facts are independent.

Everything else in D5 is verbatim: the key name `relocating:`, the nested-mapping
form, the three sub-keys `to` / `tag` / `since`, the absence of any removal key on
the row, and `scripts/check-openxfactory-pin.py` as the sole emitter.

**To overturn**: change `tag: wallet-v1.1` to `wallet-v1.0` on the eight rows and
in the changelog paragraph, then regenerate the inventory.

---

## D-2 (decided) — how the removal version is written

`tasks.md` 5.3 asks for "removal at the next MAJOR bundle". **Applied: the
concrete `contract-v2.0`.**

`tasks.md` 5.2 establishes that naming the next MAJOR is permitted precisely
because there is exactly one of them, where naming the next MINOR is forbidden by
`docs/contract-versioning-policy.md:30-31`. All three existing entries under
"Deprecations Currently In Force" write `removal target contract-v2.0`, so the
concrete form is the house precedent and reads better to a migrator.

**To overturn**: replace `contract-v2.0` with "the next major bundle, allocated at
its cut" in the changelog section and the policy-doc list entry.

---

## Not questions, but the two facts a reviewer should re-check at merge

- **The bundle number.** Authored as the next sequential minor after the bundle
  declared on the base branch. Correct only relative to merge order
  (`docs/contract-versioning-policy.md:30-31`). If another bundle lands first,
  this feature is renumbered before merge — the manifest line, the changelog
  heading, the inventory filename, and the eight rows' `since:` all move together.
- **The tag.** Not created here. `contract-v1.44` and `contract-v1.45` are both
  annotated tags cut by `brettheap`; no workflow creates them. Task 5.8 is
  `[OPERATOR]` for that reason.

---

**Path**: `/home/brett/projects/xFactory/openxFactory-worktrees/P2.5-deprecation-minor/specs/018-openxwallet-deprecation-minor/clarify-questions.md`
