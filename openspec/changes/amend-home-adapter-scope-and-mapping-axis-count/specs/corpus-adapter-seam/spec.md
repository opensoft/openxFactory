# corpus-adapter-seam Specification

**ONE `## MODIFIED` REQUIREMENT, AND THE BLOCK CARRIES EVERY SCENARIO THE
PROMOTED REQUIREMENT HAS.** A `## MODIFIED` block REPLACES the requirement it
names, so all THREE promoted scenarios are carried below BYTE-IDENTICALLY —
extracted by script rather than retyped, and re-compared at `tasks.md` § 4.2
against the IMMUTABLE BASIS, the promoting delta archived at
`openspec/changes/archive/2026-09-22-split-opendox-two-layer-product/specs/corpus-adapter-seam/spec.md`,
and not against `openspec/specs/corpus-adapter-seam/spec.md`, which this block
rewrites when it archives and which the proof reads only to confirm it still
states that basis or this block — and THREE are added: the home adapter measured against the external-product rule, the home
adapter importing the corpus's own check families, and a second in-repository
reader refused the exception. No active change carries a delta on this capability (checked by
enumerating `openspec/changes/*/specs/` on `main` `4f92d651`), so there is no
collision, no basis marker is owed, and this block is written over canon as
promoted.

**WHAT THE AMENDMENT REACHES AND WHAT IT LEAVES ALONE.** It reaches the SCOPE of
the first requirement's external-product clause and nothing else: the one-way
dependency rule, the relocation rule, the measured back-edge instance and all
three promoted scenarios are carried unedited, and the three requirements below
this one in the promoted spec are untouched by this packet.

## MODIFIED Requirements

### Requirement: The corpus reader is an external pinned product and the dependency points one way
`openxFactory` SHALL consume every tool that reads its governed corpus as an
EXTERNAL NEUTRAL PRODUCT pinned under `neutral-product-pin`, and no neutral
product `openxFactory` pins SHALL import `openxFactory`'s own tooling. THE ONE
EXCEPTION IS `openxFactory`'s OWN ADAPTER OVER ITS OWN CORPUS, which RULING DQ-1
(`opensoft/openxFactory` issue #656, 2026-09-04T22:14Z) keeps in this repository
— *"doc-health and OpenSpec stay in openxFactory, and a small adapter package
beside them implements the corpus-adapter seam"* — and whose obligations the
requirement *openxFactory's own adapter is one implementation and carries no
privileged path* below, together with the promoted capability
`openxfactory-engineering-adapter`, states in this rule's place. THE EXCEPTION IS
ONE NAMED IMPLEMENTATION AND NOT A GENERAL LICENCE: it does not admit a second
in-repository reader, it does not release that adapter from the interface it
implements, and it does not reverse the dependency. It is written here rather
than discharged by pinning the home adapter because pinning it would not resolve
the tension but relocate it — a pinned home adapter would violate this
requirement's SECOND clause the moment it imported `doc_health`, which is
precisely where DQ-1 puts it, so the escape this requirement's first clause
appears to offer is closed by its own second clause and the exception has to be
stated. THE EXCEPTION REACHES THE ONE-WAY SENTENCE BELOW ON THE SAME TERMS, and
saying so is not a second exception but the same one applied where it also
bites: that sentence governs the dependency ACROSS THE SEAM, and a reader inside
the repository whose corpus it reads is not across the seam from it. The home
adapter's dependence on `openxFactory`'s own check families is exactly what
RULING DQ-1 placed it beside them to do — reading the sentence as forbidding it
its neighbours would forbid the one thing that ruling kept it here for — while
what the one-way rule actually protects is untouched and still owed OF IT: it
depends on the pinned interface it implements, and that interface depends on
nothing of this repository's. What the exception does NOT reach is the
relocation rule that follows, which is about EXTRACTION and binds the home
adapter exactly as it binds anything else: if a package here and a package
leaving here import each other, the shared type moves into a module both depend
on before either goes. The dependency points ONE WAY — a reader depends on the interface it
implements, and never on the corpus's own check families — and where two
packages today import each other, the shared type SHALL be relocated into a
module BOTH depend on before either is extracted. The measured instance this
rule is written from: twelve of `scripts/ideation_dashboard/`'s forty-eight
modules carry twenty-three `scripts/doc_health/` imports, and
`scripts/doc_health/` imports back exactly twice — `derive_possibles.py:857` and
`ideation_readiness.py:1351`, each
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

#### Scenario: The home adapter is measured against the external-product rule
- **WHEN** `openxFactory`'s own adapter over its own corpus — the package RULING DQ-1 keeps beside `doc_health`, authored here and named in no pin — is measured against this requirement
- **THEN** it is the one named exception and is NOT refused for being neither external nor pinned, and its obligations are read from "openxFactory's own adapter is one implementation and carries no privileged path" and from `openxfactory-engineering-adapter` instead
- **AND** the exception is not cured by pinning it, because a pinned home adapter importing `doc_health` would then violate this requirement's second clause

#### Scenario: The home adapter imports the corpus's own check families
- **WHEN** `openxFactory`'s own adapter over its own corpus imports `openxFactory`'s check families — the `doc_health` suite it was placed beside in order to run
- **THEN** the import is not refused by the one-way rule, because that rule governs the dependency ACROSS the seam and this reader is inside the repository whose corpus it reads
- **AND** the one-way obligation still owed of it holds and is measurable: it depends on the pinned interface it implements, and that interface depends on nothing of this repository's

#### Scenario: A second in-repository reader claims the exception
- **WHEN** a corpus reader other than the home adapter RULING DQ-1 keeps is authored inside `openxFactory` rather than pinned as an external product
- **THEN** it is refused, because the exception names ONE implementation and a general licence would return this rule to the vendoring its third scenario exists to forbid
