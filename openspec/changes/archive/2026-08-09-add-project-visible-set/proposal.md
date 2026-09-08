---
code_surface: openxFactory (dashboard runtime — composed-model visible-set narrowing under union/intersection, selector filter as a visibility control with mode toggle and bulk moves, per-project view state, app wiring, styles; tests)
target_release: none
Status: ratified
Ratified: Brett's 2026-08-07 view-selector ruling (topic `dashboard-project-scoping` D19) — "the 'view' selector would be best as 1. all, 2. the visible union, 3. the visible intersection… we can make this a toggle of union and intersection. Then make a select all or deselect all" — with "otherwise lets implment this idea" as the instruction to realize
---

# Proposal: add-project-visible-set

## Why

Two things are wrong with the project filter as promoted.

**The view is a single choice, not a set.** The popover offers one
repository at a time plus an all-or-nothing "all repositories" line. But
the question a multi-repository project actually raises is comparative —
what do these two factories both carry, what does this one have that the
others do not — and neither affordance can express "these three". The
eyeball on each row is an INDICATOR of a decision made elsewhere rather
than the control it visually promises to be.

**The canon disagrees with the code on queued edits.** The D18 ruling
(edits queue rather than refusing one-in-flight) shipped on 2026-08-07,
but its spec amendment landed in the `add-opendox-project-header` packet
after that change had already archived and promoted its requirements. The
promoted requirement therefore still reads "or while the project carries
an undelivered edit commission", which the code no longer does. A canon
that contradicts shipped behaviour is worse than a canon that omits it —
this change corrects it at the same time, because it is the same
requirement the visibility work rewrites.

## What Changes

- The filter becomes a VISIBILITY CONTROL (D19): each member row's
  eyeball ticks its repository into or out of the view; a single toggle
  chooses UNION (everything the ticked repositories have) or
  INTERSECTION (only identities EVERY ticked repository has); `all` and
  `none` are the two bulk moves, which is why "all" needs no line of its
  own; the member name solos as the one-click shortcut; the filter label
  states the visible count against the total.
- The composed view spans the visible set. Narrowing is applied BEFORE
  the ratified cluster union, so merged tallies count the visible
  contributions, and `composed_from` is trimmed so the freshness header
  names the repositories actually rendered.
- Exactly one visible repository serves that repository's OWN snapshot
  with full capabilities — the pre-D19 single-select outcome, reached
  through the same control. Any other count serves the project's
  composed, read-only aggregate; an empty set renders honestly empty.
- Intersection FILTERS and never merges: each repository's copy stays a
  separately badged, separately openable row, which is what makes
  comparing two factories' takes on one document possible.
- Visible set and mode are viewer state, per project, resolved against
  current membership — a repository that leaves the project drops out; a
  stored set membership has outlived falls back to every member; nothing
  stored means every member under union, the composition's own answer.
- CORRECTION (D18, already shipped): the membership-commission
  requirement states the queueing rule — several undelivered edits may
  stand at once, each validated against the register with the project's
  pending commissions applied oldest-first, a pending creation counting
  as the project existing.

## Impact

No contract growth: no schema, no route, no gate verb changes. The
narrowing is a pure view derivation over data the composition already
carries (`repository` on every item, `composed_from` on the snapshot),
so the served snapshot and every non-composed consumer are untouched.
Where a project cannot be composed the popover degrades to exactly
today's single-select list.

Spec: MODIFIED "The openDox project-first header" and "Project membership
editing is a recorded commission" (both promoted); ADDED "The merged view
spans the visible member set". The composed-view family it extends was
promoted by `add-project-merged-projection`, whose own delta is
unchanged.
