# ideation-dashboard

## ADDED Requirements

### Requirement: Project merged view
Selecting a project's all-repositories view SHALL render one composed snapshot spanning the project's member repositories, produced by the existing aggregate composition (per-repo namespaced ids, per-item repository badges, `composed_from` freshness) from an aggregate DERIVED from the project register — one aggregate per register project, members being the project's repositories the serving plane can resolve — with hand-declared aggregates continuing to work and winning any id collision.

#### Scenario: A project offers its all-repos view
- WHEN a project is scoped in the selector
- THEN the roster offers "all repositories in <project>" backed by the project's derived aggregate
- AND selecting it renders the composed snapshot through the existing views

#### Scenario: A commissioned project gains its merged view on fulfilment
- WHEN a create-project commission's fulfilment lands the register edit
- THEN the project's derived aggregate exists on the next index composition with no further authoring

#### Scenario: A member snapshot is unavailable
- WHEN a member repository's snapshot cannot be loaded
- THEN the composed view renders the remaining members and names the missing one, degrading and never refusing

### Requirement: Merged-view cluster union
The wheel and canvas SHALL render a composed snapshot's same-topic clusters as one merged tile whose membership lists each repository's contribution, grouping by the namespaced id's topic tail — while the composition itself SHALL keep its ratified per-repo namespacing, so edges stay uncorrupted and non-composed consumers are unaffected.

#### Scenario: The same topic exists in two member repositories
- WHEN two member repositories carry clusters for the same topic
- THEN the merged wheel renders ONE tile for that topic listing both repositories' contributions
- AND drilling in distinguishes each repository's cluster

#### Scenario: A single-repository snapshot renders unchanged
- WHEN the rendered snapshot is not composed
- THEN clusters render exactly as today through the same view path

### Requirement: Composed views are read-only with a repository jump
On a composed snapshot every gate-bearing affordance SHALL hide — a gate verb binds to one served checkout, and a composed view has none — and the expanded tile SHALL offer one navigation verb, "open in <repo>", which switches the active snapshot to that tile's member repository, where every verb works as on any single-repository view. Per-tile repository binding remains a successor change.

#### Scenario: Gate verbs hide on a composed view
- WHEN the rendered snapshot carries `generation.composed_from`
- THEN no gate-bearing affordance renders anywhere in the view

#### Scenario: A tile jumps to its repository
- WHEN a human invokes "open in <repo>" on a composed tile
- THEN the active snapshot switches to that tile's `(repository, ref)` and the page reloads with every verb available as today
