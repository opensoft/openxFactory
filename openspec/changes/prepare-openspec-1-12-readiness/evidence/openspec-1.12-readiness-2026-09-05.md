# OpenSpec 1.12.0 readiness — measurement and dispositions, 2026-09-05

Status: record
Kind: report
Measured on: 2026-09-05
Base: openxFactory `main` at `26d0a43d` — the landing of #672, which ARCHIVED
`add-release-tag-gate` (ratified 2026-09-05, realized by #668 `7ee0e73d`).
Branch `change/prepare-openspec-1.12-readiness`, **rebased on `26d0a43d`** and
RE-MEASURED there: the archive moved that change out of the ACTIVE corpus, so
every total below is one item smaller than the same measurement taken on
`9e869acc` before the archive. The 42 findings themselves did not move — the
archived change was never one of them.
Measured by: lane `codexfactory-0d`
Fleet pin at both measurements: `@fission-ai/openspec@1.2.0`
(`contracts/openspec-cli-pin.yaml`, #667). **THIS PACKET DOES NOT BUMP IT.**

Two commands, run from the worktree root, before and after the same diff.

```
python3 scripts/validate-openspec-cli-pin.py --all --strict
OPENSPEC_TELEMETRY=0 npx -y @fission-ai/openspec@1.12.0 validate --all --strict
```

## Totals, verbatim

### The pinned entrypoint — `@fission-ai/openspec@1.2.0`

BEFORE:

```
Totals: 89 passed, 0 failed (89 items)
OK openspec-cli-pin: @fission-ai/openspec@1.2.0 verified against its content address and every target validated --strict clean
```

AFTER:

```
Totals: 90 passed, 0 failed (90 items)
OK openspec-cli-pin: @fission-ai/openspec@1.2.0 verified against its content address and every target validated --strict clean
```

**0 failed, prior count + 1** — the +1 is this packet's own change directory.
The pin held at both measurements; the tool that ran is the tool that is
pinned.

### The successor — `@fission-ai/openspec@1.12.0`

BEFORE:

```
Totals: 47 passed, 42 failed (89 items)
```

AFTER:

```
Totals: 88 passed, 2 failed (90 items)
```

**40 of the 42 are cleared. The 2 that remain are REFUSED, deliberately, and
§ The two refusals says why.**

**A NOTE ON THE EARLIER NUMBERS, because they were published before the
rebase.** This packet was first measured, committed and opened as PR #673 on
`9e869acc`, where the same two commands read **90/0** and **48 passed / 42
failed of 90** BEFORE, and **91/0** and **89 passed / 2 failed of 91** AFTER.
#672 then landed under it, archiving `add-release-tag-gate`. The branch was
rebased on `26d0a43d` and both baselines re-measured there; the figures above
are those re-measurements and are the ones this record certifies. **Only the
denominator moved.** The 42 findings are the same 42, the 40 cleared are the
same 40, and the 2 refused are the same 2.

## The 42, itemized against disposition

| Class | Count | Disposition |
| --- | --- | --- |
| Placeholder `## Purpose` in a main spec (`WARNING`) | 39 | FIXED — written in the main spec directly |
| Task under a group its leading number does not name (`WARNING`, 2 warnings in 1 change) | 1 change | FIXED — the missing `## 4.` header supplied |
| MODIFIED block omits a scenario canon still carries (`ERROR`) | 2 changes | **REFUSED** — see below |
| Archive would refuse this delta (`INFO`) | 4 | RECORDED, not repaired — `[INFO]`, not a failure |
| Requirement text is very long, >500 characters (`INFO`) | many | IGNORED — the house writes long requirements deliberately |

### The 39 Purposes

Every one read `TBD - created by archiving change <X>. Update Purpose after
archive.` Each was replaced by prose derived from that spec's own
`### Requirement` headers and from the CREATING change's `proposal.md` under
`openspec/changes/archive/`. The edit is in the MAIN spec, never a delta, per
the rule the 1.12 message itself states.

`avatar-brokered-call-feasibility`, `avatar-client-lab`, `avatar-client-runtime`,
`avatar-first-ui`, `avatar-lab-evidence`, `avatar-reference-runtime`,
`capability-health`, `chain-anchoring`, `client-identity-roster`,
`client-infrastructure-liaison`, `client-infrastructure-request`,
`consent-instrument`, `crystallization-build`, `crystallization-consent`,
`crystallization-decision`, `crystallization-dispatch`,
`crystallized-capability-registry`, `deployment-handoff-boundary`,
`document-cataloging`, `domain-conformance-checks`,
`domain-descendant-boundary`, `domain-ontology-lifecycle`,
`governed-derived-model`, `ideation-cross-reference`, `ideation-dashboard`,
`ideation-routing`, `layer-vocabulary`, `medxchart-overlay-boundary`,
`medxpractice-overlay-boundary`, `neutral-product-pin`,
`omnigent-domain-overlay`, `omnigent-install-manifest`, `pattern-ledger`,
`release-realization`, `release-surface-integrity`, `signed-execution-chain`,
`subject-establishment`, `workstation-intake`, `xfactory-semantic-kernel`.

Two judgment calls worth recording. `avatar-first-ui`'s Purpose keeps the
spec's own legacy Customer/Client/Domain Hermes spelling rather than the
canonical Subject/Tenant/Domain mapping, because that is the wording the
requirement itself carries and a Purpose must not silently re-layer its spec;
the mapping in `contracts/policies/layer-vocabulary.yaml` is how it is read.
`governed-derived-model`'s Purpose does NOT name MedxFactory's `governed` or
AdxFactory's `calibrated` conformance state, because the spec carries the
tiers and names no conforming domain — asserting it would have been scope the
spec does not carry.

### The task group

`add-doxchat-model-intake/tasks.md` gained `## 4. Still owed — the live
console, and the realization evidence`. **Nothing was renumbered.** Tasks
`4.1` and `4.2` are cited by those numbers in five places already committed —
`proposal.md` twice, task `0.3`, and the Amendment Record twice — and one of
those is a dated amendment, so renumbering to `3.x` would have falsified a
record. A dated note in that packet's own Amendment Record says so.

## The four archive-refusal orderings (INFO — they do not count against 0-failed)

Read rather than assumed, all four are ONE shape, and the manifest's framing of
them as broken pointers to be "read-then-repointed" does not survive the
reading: **nothing needs repointing.** Each is a MODIFIED delta whose target is
ADDED by a change that is ALSO still active.

| MODIFYING change | target | ADDED by | verified how |
| --- | --- | --- | --- |
| `add-wallet-carried-review-authority` | `roles-authority-model` § *Pilot repository and reviewing domain* | `add-substantive-review-lane` | header located at `:149` in that change's `## ADDED Requirements`; the modifying delta's own 2026-08-31 marker states the dependency in words; historical intent read at PR #583, the S5 register act |
| `implement-keycloak-install-repo` | `repo-boundary-governance` § *Keycloak install repository boundary* | `add-identity-brokering` | `grep -rln` over `openspec/` returns exactly two carriers of the title: the ADDING change and the MODIFYING one |
| `implement-openxpki-install-repo` | `repo-boundary-governance` § *OpenXPKI install repository boundary* | `add-trust-anchor` | same, exactly two carriers |
| `add-cpc-clearing-boundary` | the whole `clearing-dispatch-boundary` spec | `add-clearing-dispatch-boundary` | that change's delta is `## ADDED Requirements` over ten requirements creating the spec |

**A.2 and A.3 are one pattern and were dispositioned identically:** an
install-repository boundary requirement promoted by the change that
establishes the product, consumed by the change that builds the repository.
Neither was "reworded after the delta" and neither "was never promoted"; both
are promoted-in-waiting.

**The control that proves A.4's shape** is
`admit-deliberation-clearing-operation`, which targets the SAME non-existent
spec and validates CLEAN, because its block is `## ADDED Requirements`. So the
refusal is about MODIFIED-before-creation and nothing else.

**This shape is already lawful under promoted canon.** `document-lifecycle`
§ *A MODIFIED block over a requirement no promoted specification carries
declares its basis by marker* states it plainly — the successor arriving
before the predecessor archives is legitimate and frequent, and the
DECLARATION is what makes it lawful. Dated ordering notes were added to each
of the four changes' `tasks.md`. Two acts are OWED and deliberately not taken:
a `sequenced_after:` declaration on all four (all four read
`declares: absent` in the ledger), and a basis MARKER on three of the four —
`add-wallet-carried-review-authority` already has one; the other three do not.
Both would mean editing ratified packets from outside, and a basis marker in
particular is a unit inside another packet's MODIFIED block that its own
currency reader counts.

## The two refusals

**These are the two `✗` in the AFTER total, and this packet will not clear
them.**

```
✗ change/add-chain-attestation
  ✗ [ERROR] signed-execution-chain/spec.md: MODIFIED "A gate validates the short chain as a hash-linked chain" omits scenario(s) the current spec still has: "a tranche-two link does not exist yet". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
✗ change/add-composed-view-authoring
  ✗ [ERROR] ideation-dashboard/spec.md: MODIFIED "Composed views are read-only with a repository jump" omits scenario(s) the current spec still has: "Gate verbs hide on a composed view". Copy them into the MODIFIED block (a MODIFIED requirement replaces the whole block, so archive refuses to drop them).
```

**Neither appeared in the readiness manifest this work was commissioned
against.** Both were present in the manifest's own baseline capture and both
were ERROR-level; the manifest's itemization missed them. They are recorded
here so the successor bump does not rediscover them.

**Both omissions are deliberate, and both are DECLARED in the house's reserved
marker form** — ``**Merged into `<destination>` by <change-id> (<date>):**`` —
inside the MODIFIED block itself:

- `add-chain-attestation`: *"canon's scenario is RENAMED AND RE-CONDITIONED
  here, not dropped. Its antecedent … became a PERMISSION for exactly the
  chain this tranche refuses, which is the contradiction the council's LA-A1
  was raised to close"*. The successor is *"a link no ratified tranche has yet
  put in force is absent"*.
- `add-composed-view-authoring`: *"Gate verbs hide on a composed view"* became
  *"Tile-bound gate verbs hide on a composed view"*, because the same change
  deliberately ADMITS document creation on a composed view. The rename was
  declared by its own landed change, #444 — *"Declare
  add-composed-view-authoring's rename with a Merged-into marker: the scenario
  arm's standing population reaches zero"*.

**openxFactory has already ruled on this exact case, and 1.12.0 contradicts
the ruling.** The promoted `doc-health` requirement *"Currency of an active
change's MODIFIED requirement blocks"* defines both marker forms, states that
``a `Merged into` marker names titles only``, and calls `Merged into` *"the
author's instrument for a retitle"*. Its own worked example, written into
canon at `openspec/specs/doc-health/spec.md:1770`, is:

```
**Merged into `Tile-bound gate verbs hide on a composed view` by add-example-change (2026-08-27):** `Gate verbs hide on a composed view`
```

That is, byte for byte, the rename 1.12.0 rejects.

**1.12.0's scenario-currency check is marker-blind.** It compares scenario
title sets and cannot read the declaration this corpus requires, so it
re-reports as an ERROR precisely the two blocks canon holds up as correct. The
only edit that would satisfy it is to restore the old scenario titles — which
in `add-chain-attestation` reinstates the permission council LA-A1 was raised
to close, and in `add-composed-view-authoring` contradicts the sibling
scenario admitting document creation. **Both would revert a ratified decision.
Refused.**

### The house's own reader grades the same two at INFO, and calls them contested

Corroboration, not argument. `scripts/doc-health.py --single-repo .` on this
same tree reports BOTH blocks under its `modified-block-currency` family at
`severity=info`, `class=contested`, with the rule text saying in as many words
that this is *"a divergence this arm CANNOT distinguish from a deliberate
rewording, and does not claim to"* and offering the marker as one of two
remedies. **The same fact, read by the house's reader and by 1.12.0: `info` /
contested here, `ERROR` there.** Five other active changes appear in that same
family at the same severity, so the class is ordinary and long-lived, not a
two-packet anomaly.

### What this means for the bump, stated so nobody discovers it later

While these two changes are ACTIVE, openxFactory cannot read 0 failed under
`1.12.0`, and `openspec archive` at 1.12.0 would REFUSE both. Both findings
vanish on their own when the two changes archive — archived changes are
outside the `--all` corpus. Three honest exits, none taken by this packet
because none is this lane's to take:

1. Sequence the bump AFTER both changes archive.
2. Carry a dispositioned exception for the two.
3. Take it upstream, so the check reads the two reserved marker forms.

## Residual `[INFO]` after the fix, verbatim

Beyond the *"Requirement text is very long (>500 characters)"* class, which
the house writes deliberately and which the manifest names as noise to ignore,
exactly four `[INFO]` lines remain, all four being the orderings above:

```
ℹ [INFO] clearing-dispatch-boundary/spec.md: Archive would refuse this delta: clearing-dispatch-boundary: target spec does not exist; only ADDED requirements are allowed for new specs. MODIFIED and RENAMED operations require an existing spec.
ℹ [INFO] repo-boundary-governance/spec.md: Archive would refuse this delta: repo-boundary-governance MODIFIED failed for header "### Requirement: Keycloak install repository boundary" - not found
ℹ [INFO] repo-boundary-governance/spec.md: Archive would refuse this delta: repo-boundary-governance MODIFIED failed for header "### Requirement: OpenXPKI install repository boundary" - not found
ℹ [INFO] roles-authority-model/spec.md: Archive would refuse this delta: roles-authority-model MODIFIED failed for header "### Requirement: Pilot repository and reviewing domain" - not found
```

## Scope kept

`openspec/changes/add-release-tag-gate/**` and the files #668 owns
(`tests/doc-health/test_release_tag_*.py`, `scripts/validate-release-tag-gate.py`,
`.github/workflows/release-tag-gate.yml`, `docs/contract-versioning-policy.md`)
were not touched. No contract, schema, validator, workflow or test file is in
this diff.
