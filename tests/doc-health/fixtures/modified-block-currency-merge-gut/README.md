# Fixture: a merge that guts its source

**SYNTHESIZED** — this text is invented and reproduces no historical instance.

## Which rule this exists for

`add-modified-block-currency-check` § 3.3, audit row **A3** — the one row the
F2 audit found with NO test at all.

> **A `Merged into` marker names titles only**, so a bullet a merge makes
> redundant is a declared removal, not a permanent editorial row — but it has to
> be declared as a bullet, one at a time, which is exactly the deliberation the
> class deserves.
> — `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`

## Why not a reconstruction

This corpus carries no instance of the shape — no active change has merged a
scenario away and dropped bullets from underneath it. That is itself the reason
the rule is worth pinning before one arrives: F1's only end-to-end `Merged into`
case has a one-bullet source that the block carries, so it is quiet in both arms
and the rule above was asserted nowhere.

## What the family reports here

- **`A merge that guts its source`** — one `info` naming exactly the TWO
  bullets of the superseded four-bullet scenario that the replacement does not
  carry. The scenario arm is quiet (the marker is valid and names an absent
  title) and no marker defect is emitted.
- **`A merge that declares its redundant bullets`** — **nothing**. The same
  merge, plus a `Removed from canon` marker naming those two bullets one at a
  time. One of them cites `openxFactory`, so its code span carries a LONGER
  FENCE — which makes this requirement carry § 3.7's fence rule too.

Tests: `test_a_merge_marker_does_not_declare_the_bullets_it_makes_redundant`,
`test_the_scenario_arm_is_quiet_because_the_merge_marker_is_valid`,
`test_a_merge_companion_naming_its_redundant_bullets_silences_them`,
`test_the_merge_companion_is_quiet_because_of_its_marker_not_by_carriage`.

The last of those removes the marker and shows the noise return, because silence
proves nothing until the thing causing it is taken away.
