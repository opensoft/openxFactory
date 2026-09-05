# corpus-adapter-seam Specification

A NEW capability. It does not exist in `openspec/specs/` and no active change
carries a delta on it, so there is no collision and no basis marker is owed.

**WHY IT IS `openxFactory`'s AND NOT openDox's, which is a real question.**
RULING Q4 (`opensoft/openxFactory` issue #656, 2026-09-04T15:34Z) is that
**openDox DEFINES the corpus-adapter interface and openXdox IMPLEMENTS it**, so
the INTERFACE's own standard — the operation names, their arguments, their return
shapes — belongs to openDox's own OpenSpec instance and is NOT authored here. What
this capability governs is the half `openxFactory` cannot delegate: **the terms on
which a reader that `openxFactory` does not own is permitted to read
`openxFactory`'s corpus, and the direction of the dependency.** Those are
statements about this repository's corpus and this repository's layering, and
they survive whatever openDox names its verbs. The division is the same one
`neutral-product-pin` already makes for the wallet: the product owns its
standard, the consumer owns the terms of consumption.

The interface's SHAPE is nonetheless load-bearing on `openxFactory`, so
`design.md` § D2 carries the four-operation sketch RULING Q4's own words imply —
**list, read, write back, check** — as design rather than as promoted text, and
`tasks.md` § 2 lands the operations before any repository exists.

**RULING DQ-1 (2026-09-04T22:14Z) MAKES THE FOURTH REQUIREMENT BELOW
LOAD-BEARING RATHER THAN PRECAUTIONARY.** It was authored against a world in
which `openxFactory` might keep no adapter at all; Brett has since ruled that it
KEEPS ONE — *"doc-health and OpenSpec stay in openxFactory, and a small adapter
package beside them implements the corpus-adapter seam; `codexDox` becomes a thin
descendant that pins openXdox and reuses that adapter"* — so this repository is
permanently both the owner of a corpus and the author of a reader over it. That
is exactly the position in which a private door gets built, and the fourth
requirement is the rule that forbids one. Read it as the ruling's own safeguard:
without it, DQ-1 collapses into "the reader never really left".

## ADDED Requirements

### Requirement: The corpus reader is an external pinned product and the dependency points one way
`openxFactory` SHALL consume every tool that reads its governed corpus as an
EXTERNAL NEUTRAL PRODUCT pinned under `neutral-product-pin`, and no neutral
product `openxFactory` pins SHALL import `openxFactory`'s own tooling. The
dependency points ONE WAY — a reader depends on the interface it implements, and
never on the corpus's own check families — and where two packages today import
each other, the shared type SHALL be relocated into a module BOTH depend on
before either is extracted. The measured instance this rule is written from:
twelve of `scripts/ideation_dashboard/`'s forty-eight modules carry twenty-three
`scripts/doc_health/` imports, and `scripts/doc_health/` imports back exactly
twice — `derive_possibles.py:857` and `ideation_readiness.py:1351`, each
`from ideation_dashboard.boundary import OutputBoundary` — so the back-edge is
ONE class in ONE module, imported lazily in two places.

#### Scenario: A neutral product imports the corpus's own tooling
- **WHEN** a repository `openxFactory` pins as a neutral product imports `openxFactory`'s check families, validators or corpus readers
- **THEN** the import is refused, because the dependency has reversed and neither repository can be released without the other

#### Scenario: Two packages import each other across the seam
- **WHEN** an extraction would place two mutually importing packages in different repositories
- **THEN** the shared type is relocated into a module both depend on BEFORE either package moves
- **AND** the relocation lands as its own change, because it is correct whether or not the extraction ever happens

#### Scenario: A reader is vendored instead of pinned
- **WHEN** a corpus reader is copied into `openxFactory` rather than pinned as an external product
- **THEN** the copy is refused, because a vendored reader has no version anyone can name and drifts silently from the product it was taken from

### Requirement: A reader over a corpus it does not own fails closed on an unresolvable corpus
A corpus adapter implementation SHALL FAIL CLOSED when the corpus it is pointed at
cannot be resolved: an absent checkout, an unreadable path, a ref that does not
exist, or a corpus whose declared shape the adapter cannot classify SHALL each
produce a REFUSAL naming what it could not resolve, and SHALL NOT degrade to an
empty result, to a partial listing, or to a skip. An empty corpus and an
unreadable corpus SHALL be DISTINCT answers, because a projection built over the
first is correct and a projection built over the second is a lie with a
timestamp.

#### Scenario: The corpus checkout is absent
- **WHEN** an adapter is pointed at a corpus whose checkout is not present
- **THEN** it refuses and names the corpus it could not resolve, rather than returning an empty document list

#### Scenario: A document cannot be classified
- **WHEN** an adapter's classify operation meets a document whose declared shape it does not recognize
- **THEN** it reports the document as unclassifiable and names it, rather than omitting it from the listing

#### Scenario: An empty corpus is served
- **WHEN** an adapter reads a corpus that genuinely holds no documents
- **THEN** it returns an empty result distinguishable from a refusal, so that a consumer can tell "nothing there" from "could not look"

### Requirement: The governed write path is the only write path, and the adapter declares it
An adapter's WRITE-BACK operation over a governed corpus SHALL resolve to that
corpus's declared governed write path and SHALL NOT write the corpus tree
directly. For `openxFactory` that path is the apply lane, per RULING Q1
(2026-09-04T15:24Z): *"Specs, changes, ideation documents and contracts stay in
git, read from repositories and written back only through the apply lane."* An
adapter whose write-back bypasses the declared path SHALL be refused even where it
would produce the identical bytes, because the gate is the act of passing through
the path and not the shape of the result. A corpus that declares NO governed write
path is READ-ONLY to the adapter, and the adapter SHALL say so rather than
failing at the first write.

#### Scenario: An adapter writes the corpus tree directly
- **WHEN** an adapter's write-back operation commits to the corpus checkout instead of dispatching through the declared governed write path
- **THEN** the write is refused, even where the resulting bytes would be identical

#### Scenario: A corpus declares no governed write path
- **WHEN** an adapter is pointed at a corpus with no declared write path
- **THEN** the adapter reports the corpus as read-only at resolution time, rather than accepting a write and failing at dispatch

#### Scenario: The governed write path is unavailable
- **WHEN** the declared write path exists but cannot be reached
- **THEN** the write refuses and names the path, and the document remains unsaved rather than being written by a fallback

### Requirement: openxFactory's own adapter is one implementation and carries no privileged path
An `openxFactory`-authored adapter over its own corpus SHALL be ONE CONFORMANT
IMPLEMENTATION among others and SHALL NOT be reachable by any route the interface
does not define — no privileged
direct call, no bypass of the interface for `openxFactory`'s own corpus, and no
operation available to it that a domain implementation cannot also declare. This
is what makes the seam testable rather than nominal: RULING C2
(2026-09-04T17:47Z) places engineering vocabulary in the engineering descendant
"or … openxFactory as its own adapter over the corpus-adapter interface", and an
adapter with a private door is the same repository it was extracted from, wearing
an interface.

#### Scenario: The home corpus is reached by a privileged route
- **WHEN** a consumer reaches `openxFactory`'s corpus by a call the corpus-adapter interface does not define
- **THEN** the route is refused, because the seam's whole value is that the home corpus is reached the same way every other corpus is

#### Scenario: An operation exists only for the home corpus
- **WHEN** an adapter implementation over `openxFactory`'s corpus offers an operation the interface does not declare
- **THEN** the operation is either promoted into the interface for every implementation or removed, and it is not kept as a local extension
