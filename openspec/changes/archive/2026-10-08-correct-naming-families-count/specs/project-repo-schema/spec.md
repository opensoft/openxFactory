# project-repo-schema Specification

**TWO `## MODIFIED` REQUIREMENTS, BOTH WRITTEN OVER CANON AS PROMOTED, AND NO
OTHER BLOCK.** Each restates its requirement as
`openspec/specs/project-repo-schema/spec.md` states it on `main` `16779816`,
extracted by script rather than retyped, and changes only the sentences that
restate a fact about the WHOLE set of naming families the pinned openRepoShape
standard declares. Three units are replaced, each declared by a `Removed from
canon` marker in its own block; one paragraph and one scenario are added; every
other body sentence and every scenario is carried byte-identically (`tasks.md`
§ 3.1). Both titles are unchanged.

**THE READING IS COUNT-FREE.** Canon said "four live naming families" and listed
them. openxFactory's openRepoShape pin has named a naming policy declaring five
families since 2026-09-04 and six since 2026-10-06. The blocks below do not
correct "four" to "six": they stop restating a number and a closed list that the
pinned DATA owns, and they say where both are read (`design.md` D1).

**ORDERING.** The one other active change carrying a delta on this capability,
`prefer-triad-project-shape`, modifies *The project repository schema is
elective and confers nothing* and adds three requirements whose titles canon
does not carry. Neither block here writes any of those four titles, so the two
changes write disjoint requirement keys, neither is sequenced after the other,
and they may archive in either order (`design.md` D5).

## MODIFIED Requirements

### Requirement: A project's repositories are named `<Project>`, `<Project>-spec` and `<Project>-code`
An electing project's repositories SHALL be named `<Project>` for the assembly
root, `<Project>-spec` for the spec leg and `<Project>-code` for the code leg,
where `<Project>` is ONE CamelCase token carrying no hyphen, underscore, dot or
space, and the two suffixes are fixed LOWERCASE and hyphenated. Every repository
of the project SHALL also carry the GitHub topic `xf-project-<id>`, where `<id>`
is the project's lowercase id.

The suffixes are lowercase and hyphenated precisely so they sit in a different
visual class from every family the pinned standard's naming policy spells as a
CamelCase word, and the assembly root is BARE because the thing you clone has no
suffix — the precedent the aggregation root already sets. A name matching no
family at all is REFUSED rather than accepted as a residual, which is the check
that earns its keep: this is a FORWARD rule, and two live repositories
(`xFactory-Installer`, `AgentTower`) fit no suffix rule, so the rule describes
what may be created and never retroactively condemns what exists.

**Removed from canon by correct-naming-families-count (2026-10-07):** ``The suffixes are lowercase and hyphenated precisely so they sit in a different visual class from every other live family, all of which are CamelCase words, and the assembly root is BARE because the thing you clone has no suffix — the precedent the aggregation root already sets.`` — REPLACED, not dropped: the paragraph above restates it with one clause changed. Its claim that every other family is a CamelCase word has been false at the pin in force since openxFactory's openRepoShape pin moved to `1a9fc537` (openxFactory PR #1260, 2026-10-06), because that commit's naming policy declares the `workspace` form `<user>-wip`, which is lowercase and hyphenated (openRepoShape PR #86). The replacement keeps what the sentence is for, that the leg suffixes are told apart from the CamelCase forms, and states no property of the whole set of families. The removed unit carries no SHALL, and its clause about the bare assembly root is carried word for word.

#### Scenario: A project is scaffolded
- **WHEN** a project named `Atlas` elects the schema
- **THEN** its repositories are `Atlas`, `Atlas-spec` and `Atlas-code`, and each carries the topic `xf-project-atlas`

#### Scenario: A leg name uses the wrong case or separator
- **WHEN** a proposed leg name is `Atlas-SPEC`, `Atlas_spec` or `Atlas-tests`
- **THEN** it is refused before anything is created
- **AND** the refusal names the form that would have been accepted

#### Scenario: An existing repository fits no family
- **WHEN** a repository that predates this rule matches no naming family
- **THEN** it is not thereby non-conformant, this being a forward rule over what may be created

### Requirement: The naming families are governed by the pinned standard, and a descendant form is a claim that needs a declared pin
The naming families SHALL be those the naming policy of the pinned openRepoShape
standard (`contracts/repository-naming.yaml`) declares, governed there as DATA
rather than by prose and restated here by neither their number nor their full
list — among them `open<Product>` neutral products, `<X>-Install` installs,
`<Domainx><Product>` domain descendants, and the project legs above — and a
`<Domainx><Product>`-shaped name SHALL be classified as a domain descendant
ONLY where the project DECLARES a pin on the matching `open<Product>`. Ruled by
Brett Heap, 2026-09-02, choosing from three options presented: *"Descendant only
if it pins open&lt;Product&gt;."* Absent that declared pin the project's DECLARED
ROLE wins, the name is a valid assembly root, and the project manifest SHALL
RECORD that the name ALSO MATCHES the descendant form rather than discarding the
overlap.

A family the pinned policy adds or retires at a later pin owes this capability
no amendment for its count or its listing: how many naming families there are,
and which, is read from the policy at the pin in force and not from this
specification. A count or a closed list restated here would be a second
statement of a fact the pinned data owns, and it would go stale at the first pin
that moved it — which is what this requirement's promoted text did twice, at
openxFactory's openRepoShape pin advances of 2026-09-04 and 2026-10-06.

**Removed from canon by correct-naming-families-count (2026-10-07):** ``The four live naming families SHALL be governed as DATA by the naming policy of the pinned openRepoShape standard (`contracts/repository-naming.yaml`) rather than by prose — `open<Product>` neutral products, `<X>-Install` installs, `<Domainx><Product>` domain descendants, and the project legs above — and a `<Domainx><Product>`-shaped name SHALL be classified as a domain descendant ONLY where the project DECLARES a pin on the matching `open<Product>`.`` — REPLACED, not dropped, and the replacement is this change's whole object. The promoted sentence was true at the pin in force when it was promoted on 2026-09-03, `deacbdc`, whose naming policy declared four families. openxFactory's pin moved to `122d729b` on 2026-09-04 (openxFactory PR #650), whose policy declares five, the `family` holder having been added by openRepoShape PR #16; and to `1a9fc537` on 2026-10-06 (openxFactory PR #1260), whose policy declares six, the `workspace` form `<user>-wip` having been added by openRepoShape PR #86. The paragraph above restates the sentence with its count and its closed list removed and with the four forms it named kept as named members, and carries its descendant clause word for word. Every SHALL the removed unit stated is carried: the families stay governed as DATA by the pinned policy, and a descendant-shaped name is still a descendant only on a declared pin.

The classification SHALL be decided OFFLINE, from facts in the project's own
tree, and SHALL NOT ask any host whether `open<Product>` exists — a rule needing
the network is unrunnable in the fork-and-run case this capability exists for.
`open<Product>` and `<X>-Install` are unambiguous in their own characters and
keep their precedence unchanged; `<Domainx><Product>` is not, its form being a
CLAIM of descent that the characters alone cannot settle, which is why it
carries a referent. This narrows NOTHING in
`domain-descendant-boundary`: a descendant is still a descendant because it pins
the product, which is what that capability already requires.

**Removed from canon by correct-naming-families-count (2026-10-07):** `` `open<Product>` and `<X>-Install` are unambiguous in their own characters and keep their precedence unchanged; `<Domainx><Product>` is the one family whose membership is not decided by the characters alone, which is why it is the one family carrying a referent. `` — REPLACED, not dropped: the paragraph above restates it with its second clause changed. `<Domainx><Product>` stopped being the ONLY family whose membership the characters alone do not decide when openxFactory's pin moved to `122d729b` (openxFactory PR #650, 2026-09-04), because that commit's naming policy declares the `family` holder form DECLARED-ONLY, the characters of a holder's name being those of an assembly root (openRepoShape PR #16). The replacement keeps the sentence's point, that the descendant form is a claim and carries a referent for that reason, and makes no claim about the rest of the set. Its first clause, on `open<Product>` and `<X>-Install`, is carried word for word.

#### Scenario: A descendant-shaped name declares the matching pin
- **WHEN** a repository named `MedxChart` declares a pin on `openChart`
- **THEN** it classifies as a domain descendant, on the strength of the pin rather than the spelling

#### Scenario: A descendant-shaped name declares no matching pin
- **WHEN** a repository named `MedxScribe` is declared as an assembly root and no `openScribe` pin is declared
- **THEN** the declared role wins and the name is a valid assembly root
- **AND** the manifest records that it also matches the descendant form, so a resolved overlap stays visible to the next reader

#### Scenario: The classifier is asked to reach the network
- **WHEN** classification would require asking a host whether a neutral product repository exists
- **THEN** the classification MUST instead be decided from the project's declared pins
- **AND** a rule that reached the network would be unrunnable in an organisation that forked the standard and never speaks upstream

#### Scenario: The pinned policy declares a family no requirement here names
- **WHEN** openxFactory's openRepoShape pin advances to a naming policy that declares a family no requirement of this capability names
- **THEN** that family is a naming family from that pin on, governed as data by the pinned policy
- **AND** no requirement of this capability is amended to restate how many families there are or which, the pinned policy being where both are read
