# Tasks: add-project-merged-projection

## 1. Project-derived aggregates (D11)

- [ ] 1.1 `snapshot_registry`: derive one aggregate per register project at
      index-composition time — id/name from the project, members = the
      project's repositories the registry resolves, default ref; additive
      beside hand-declared aggregates, hand-declared winning an id
      collision.
- [ ] 1.2 The index document advertises derived aggregates exactly like
      declared ones (no schema growth — `aggregates[]` already carries
      them); the composed-snapshot route resolves a derived aggregate id.
- [ ] 1.3 Selector wiring: with a project scoped, the roster offers
      "all repositories in <project>" mapped to the project's aggregate;
      clearing the scope removes it.

## 2. The merged view (D9, D10)

- [ ] 2.1 Wheel/canvas view-side union: composed clusters group by topic
      tail (design D-f) into one merged tile listing per-repo
      contributions; non-composed snapshots render exactly as today through
      the same path.
- [ ] 2.2 Composed-view verb gating: every gate-bearing affordance hides
      when `generation.composed_from` is present; the expanded tile mounts
      the one navigation verb "open in <repo>" (store key + reload — the
      ratified selector posture).
- [ ] 2.3 Composed freshness header: `N repos · composed <date>`, with the
      per-member revisions from `composed_from` reachable on demand.

## 3. Verification

- [ ] 3.1 Registry tests: derived aggregates (membership, ref, collision
      rule, unresolvable member degrade); composed route resolves a project
      aggregate.
- [ ] 3.2 View-model tests: topic-tail union across repos, single-repo
      passthrough, badge content; verb gating on composed vs plain
      snapshots; jump key resolution.
- [ ] 3.3 Live browser check: scope a multi-repo project, select "all
      repositories", the merged wheel renders with union tiles and repo
      badges, gate verbs absent, "open in <repo>" jumps; zero page errors.
- [ ] 3.4 First real merged-view session by Brett (select a project's
      all-repos view, navigate, jump into a member repo).
