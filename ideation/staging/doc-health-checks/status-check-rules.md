# Staged: Status Check Rules For The Doc-Health Pipeline

Status: staged
Kind: reference
Repository context: openxFactory
Target: the codexFactory doc-health implementation proposal (deterministic
pass); staged per task 5.3 of the add-document-lifecycle-vocabulary change.
Proposed by: [add-doc-health-contract](../../../openspec/changes/add-doc-health-contract/proposal.md)
— checks 1–8 below are now carried as the contract's status, succession,
location, immutability, aging, and register check families.

Checks the nightly deterministic pass MUST implement, derived from the
ratified document-lifecycle requirements:

1. Status validity — every governance `*.md` under `docs/`, `templates/`,
   `contracts/`, `examples/`, and `ideation/` carries a `Status:` header
   whose value is in the controlled taxonomy. Missing header = finding;
   free-form value = finding.
2. Standard backing — every `Status: standard` doc names (or resolves to) a
   promoted spec or canonical contract; every prose claim of shared-standard
   authority appears only in a `standard` doc. Unbacked claim = finding.
3. Ratified provenance — every `Status: ratified` doc carries a
   `Ratified by:` line resolving to an existing OpenSpec change (active or
   archived). Dangling reference = finding.
4. Succession integrity — every `Status: superseded` doc names an existing
   successor; every `retired` doc names a reason or decision record.
5. Location conformance — `Status: brainstorm` docs live only under
   `ideation/brainstorm/`; staging fragments only under `ideation/staging/`.
6. Record immutability — `Status: record` docs are not edited after their
   capture commit except for link fixes (flag content diffs).
7. Candidate aging — `staged` items (including register entries) untouched
   for N days are reported as aging (threshold: open question in the
   doc-health brainstorm).
8. Register-lifecycle consistency — candidate register statuses use the
   documented aliases; an `adopted` entry with a surviving domain-local
   near-duplicate = finding (promotion process, adoption section).

Reference implementations of the grep-level checks exist in the
add-document-lifecycle-vocabulary task 5.2 verification commands.
