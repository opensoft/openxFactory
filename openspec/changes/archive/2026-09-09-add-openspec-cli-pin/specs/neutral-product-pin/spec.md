# neutral-product-pin Specification

## ADDED Requirements

### Requirement: The OpenSpec CLI is a pinned neutral product, and every strict validation and every archive runs at the pin
The OpenSpec CLI SHALL be declared as a pinned external neutral product in
`contracts/openspec-cli-pin.yaml`, and every `openspec validate … --strict` and
every `openspec archive` performed as a governed act SHALL run at that pin. The
CLI is not an incidental developer convenience: `validate --strict` is the gate a
spec delta passes before it may archive, and `archive` is the act that writes a
ratified delta into canon — so WHICH TOOL ADJUDICATED is a fact about the
governance record itself, and a corpus that cannot say which tool adjudicated
cannot say what its canon was checked against.

The pin SHALL be the ONLY declaration of that version. A version literal written
anywhere else — a workflow's `npm install -g <package>@<version>` line, a
README, a runbook step, an agent instruction — is a SECOND COPY of the pin, and
copies of a pin move separately; such a literal SHALL be replaced by a read of
the pin file rather than kept in step by discipline.

#### Scenario: A governed act runs the CLI
- **WHEN** an engineer or an agent validates a change strictly, or archives a ratified change
- **THEN** the tool that runs is the one the pin names, verified against its recorded content address before it is invoked
- **AND** a run at any other version is refused rather than reported, because strict verdicts differ between versions and a run at the wrong version is a different check rather than a weaker one

#### Scenario: A workflow restates the version
- **WHEN** a workflow, runbook or instruction file carries the pinned version as a literal
- **THEN** that literal is a second copy of the pin and MUST be replaced by a read of the pin file
- **AND** the replacement is owed even where the literal is currently correct, because the defect is that two writings can diverge and not that one of them is wrong today

#### Scenario: The corpus is asked which tool checked it
- **WHEN** a reader asks which CLI adjudicated a green strict validation
- **THEN** the answer is the artifact at the content address the pin records
- **AND** an answer of "whatever was on the runner" is the unpinned state this requirement ends, not a permitted variation of it

### Requirement: A consuming repository runs OpenSpec validation only through the pinned entrypoint, so a PATH binary cannot affect the gate
A repository consuming the pinned OpenSpec CLI SHALL invoke strict validation
ONLY through the entrypoint the pin names in `consumer_entrypoint:`, and that
entrypoint SHALL resolve the CLI from the verified artifact rather than from
`PATH`, so that whatever binary an engineer or a runner happens to have installed
CANNOT determine a gate's verdict. A repository that calls a bare `openspec`
binary is NOT running the pinned tool whatever version answers, because nothing
verified which tool answered; the enforcement claim in such a repository is
UNMET.

Where an entrypoint offers a PATH mode for local iteration, that mode SHALL
REFUSE with a named exit unless the binary on `PATH` reports exactly the pinned
version, and a required check SHALL NOT invoke it. Each consuming repository
SHALL additionally pin the `openxFactory` version it consumes in its
`stack.yaml`, so that WHICH pin file governed a run is as answerable as which
tool ran.

#### Scenario: A gate runs on a machine with a different CLI installed
- **WHEN** a required check runs in an environment whose `PATH` carries an `openspec` at some other version
- **THEN** the gate's verdict is unchanged, the entrypoint having never consulted `PATH`
- **AND** a gate whose verdict COULD be changed by an ambient installation does not satisfy this requirement, whichever way it happened to resolve

#### Scenario: A developer asks for the local binary
- **WHEN** a developer invokes the entrypoint's PATH mode to avoid a registry round trip
- **THEN** the run proceeds only if the local binary reports exactly the pinned version, and otherwise refuses with a named exit and a remedy
- **AND** a required check does not use that mode, the mode existing to check a local install rather than to substitute for the pinned one

#### Scenario: A consuming repository wires its own gate
- **WHEN** a domain or install repository adds strict OpenSpec validation to its continuous integration
- **THEN** it invokes the pinned entrypoint from the pinned `openxFactory` checkout rather than copying the entrypoint or installing the CLI itself
- **AND** it names in its `stack.yaml` the `openxFactory` version whose pin it is consuming

### Requirement: A pinned CLI version bump is one human-only act that lands its target-version evidence in the same change
A change that moves a pinned tool's version SHALL be HUMAN-ONLY and SHALL NOT be
clearable by a council or any other automated authority, and it SHALL carry, IN
THE SAME CHANGE, evidence that the governed trees VALIDATE CLEAN at the TARGET
version — `validate --all --strict` reporting zero failures for every repository
the bump reaches. A bump proposed without that evidence SHALL be refused, because
the tool being bumped is the tool that judges whether the bump's own change is
valid, and a candidate that could repoint its own adjudicator could clear itself.

THE EVIDENCE IS OWED BECAUSE THE COST IS MEASURED AND NOT HYPOTHETICAL. Strict
verdicts and archive admissibility differ between CLI versions over trees that
did not change: conditions that pass at one version fail at another on
PRE-EXISTING content, and a newer `archive` may REFUSE deltas an older one
admitted. An unpinned or unevidenced upgrade therefore turns green repositories
red and stalls every archive across the estate, and it does so in the name of
whoever ran the upgrade rather than in the name of the conditions that predate
them. Where the target version's failures are pre-existing conditions, the change
SHALL either remedy them or DECLARE each one with its owner; silence about a
known failure is not evidence of its absence.

#### Scenario: A bump is proposed with no target-version run
- **WHEN** a change moves the pinned version and carries no `--all --strict` result at the target version
- **THEN** the change is refused, the evidence being the whole basis on which a bump can be judged safe
- **AND** the refusal is not satisfied by the CURRENT version's clean run, which says nothing about the target

#### Scenario: An automated authority is asked to clear a bump
- **WHEN** a council or other automated authority is asked to clear a pull request that moves the pin
- **THEN** the request is refused as human-only, because the candidate would otherwise repoint the very tool that judges its own change

#### Scenario: The target version fails on conditions that predate the bump
- **WHEN** the target version's strict run fails over content the change did not author
- **THEN** each failure is remedied in the change or DECLARED with its owner, and the bump does not land silently over it
- **AND** the failures are not attributed to the change that measured them

### Requirement: A pin whose content address cannot be verified refuses, and the refusal names its remedy
A consumer of a pinned tool SHALL FAIL CLOSED where the pinned artifact's
CONTENT ADDRESS cannot be verified: an unreachable registry, an absent package
manager, an artifact whose recomputed digest disagrees with the pin, a binary
that will not report its version, or a pin that records a movable referent SHALL
each produce a REFUSAL with a named exit, and SHALL NOT resolve to an implicit
pass, to a fallback on an ambient installation, or to a skip. Every such refusal
SHALL carry a REMEDIATION STRING naming what to run and where the version policy
lives, so the exit is in the message rather than in tribal memory.

THE DIGEST IS VERIFIED BEFORE THE TOOL IS INSTALLED AND BEFORE IT IS INVOKED, by
running code rather than by a stated obligation. A resolver that merely REQUESTS
a version by name and trusts what it receives has verified nothing: the version
label is a NAME whose stability is a registry's policy, while the artifact's
digest is a CONTENT ADDRESS that nothing can move. A pin that records only a
version, or that records a range, a caret or a dist-tag, SHALL be refused in the
grammar's own words about a tag.

#### Scenario: The registry serves an artifact the pin does not name
- **WHEN** the fetched artifact's recomputed digest differs from the pin's recorded content address
- **THEN** the run refuses, and nothing is installed from those bytes
- **AND** the version label having matched is not a mitigating fact, the label not being the referent

#### Scenario: The pinned artifact cannot be fetched
- **WHEN** the registry is unreachable or the package manager is absent
- **THEN** the run refuses with a named exit rather than falling back to an ambient installation
- **AND** the refusal names what to run, an unanswerable question never being an implicit pass

#### Scenario: A refusal carries no remediation
- **WHEN** a fail-closed path emits a refusal that does not name a command and the policy it belongs to
- **THEN** the refusal is itself a defect of this capability, because it tells the operator that something is wrong without telling them what to run

## MODIFIED Requirements

### Requirement: An external neutral product is pinned by commit and digest, never by tag
`openxFactory` SHALL declare its consumption of an EXTERNAL neutral product in
`contracts/<product>-pin.yaml`, REUSING `kind: pinned_contract_manifest`
unchanged, and that pin SHALL carry the product's COMMIT, its `revision_kind`, a
per-file `sha256` for every artifact the product's own manifest digests per file,
and `pinned_by_commit_only:` for every artifact the product content-addresses by
commit alone. The pin GRAMMAR is not new — it is the ratified
`pinned_contract_manifest` shape already realized twice under
`repo-boundary-governance`'s per-product requirements
(`installs/keycloak-install/config/contracts/identity-brokering/manifest.yaml:1-20,45-58`
and `installs/openxpki-install/config/contracts/trust-anchor/manifest.yaml:55`);
what is new is only that `openxFactory` is the CONSUMER. A TAG-ONLY pin SHALL be
refused in that shape's own words, "a tag can be moved": a tag MAY be recorded
beside the commit as a human-readable label, never as the thing being trusted,
and a pin SHALL NOT express a version RANGE.

WHERE THE PRODUCT IS DISTRIBUTED AS A PUBLISHED, CONTENT-ADDRESSED ARTIFACT
RATHER THAN AS A SOURCE TREE, the pin SHALL carry that ARTIFACT'S DIGEST as its
referent and SHALL declare `revision_kind` accordingly, and the release NAME —
the version string — is a LABEL recorded beside it on exactly the terms a tag is
recorded beside a commit. The distinction is the same one and it is not weakened
by the change of medium: a digest over the published bytes cannot be moved,
whereas a version name is kept stable by a REGISTRY'S POLICY and an operator who
administers it, and a policy is not a content address.

Such a pin carries NEITHER a per-file `sha256` list NOR a `pinned_by_commit_only:`
list, and their absence is not a permitted omission but a consequence of the
medium. Those two lists exist because a commit is not a digest a consumer can
compare a single file against, so the surface must be ENUMERATED for
completeness to be checkable at all. A published artifact needs no enumeration:
ONE digest addresses EVERY byte inside it, so no member can be undeclared and
none can be added or altered without changing the referent. The completeness
obligation is therefore DISCHARGED MORE STRONGLY here rather than waived, and a
pin of this kind SHALL record every field the consumer's verifier checks —
including any secondary address the registry publishes — so that no declared
field goes unverified.

#### Scenario: A pin declares a tag and no commit
- **WHEN** a pin file names a release tag but no commit
- **THEN** the pin is refused, because a tag can be moved and a commit cannot

#### Scenario: The product digests only part of its release surface
- **WHEN** the product's manifest carries per-file digests for some artifacts and content-addresses the rest by commit
- **THEN** the pin carries per-file `sha256` for the former and `pinned_by_commit_only:` for the latter
- **AND** an artifact that appears in neither list is an undeclared consumption, not a permitted omission

#### Scenario: A pin expresses a range
- **WHEN** a pin expresses a version range or a moving reference
- **THEN** it is refused, because the moment a pin trusts a range the fail-closed property is gone

#### Scenario: The product is published as an artifact rather than as a source tree
- **WHEN** the consumed product is distributed as a published package whose registry publishes a digest over its bytes
- **THEN** the pin records that digest as the referent, declares a `revision_kind` naming it, and records the version string only as a label
- **AND** the pin carries no per-file list, one digest over the artifact addressing every file inside it and leaving nothing undeclared

#### Scenario: A published-artifact pin records only a version
- **WHEN** such a pin names a version, a dist-tag or a range and records no digest over the artifact
- **THEN** it is refused on the same ground a tag-only pin is refused, a name whose stability is a registry's policy not being the thing that is trusted
