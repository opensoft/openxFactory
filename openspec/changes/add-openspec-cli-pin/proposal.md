---
code_surface: openxFactory — FOUR NEW artifacts, all landing in this pull request, none of them a registered contract row. (1) `contracts/openspec-cli-pin.yaml`, openxFactory's consumption of `@fission-ai/openspec` at version `1.2.0` whose REFERENT is the published tarball's SHA-512 integrity `sha512-2XDmPZcVY0Bs014lP9aoxe3VoEU8hFvqaBFxQaiJO2nhC8vTKCyo6sT/5YpQcOTfR/a64Hht2anTyqLR4eNhlg==` (registry shasum `0fd5333520c8846f0ac51727379b8812e2f13c1b`, tarball `https://registry.npmjs.org/@fission-ai/openspec/-/openspec-1.2.0.tgz`), in the `neutral-product-pin` shape with `kind: pinned_contract_manifest` reused unchanged. (2) `scripts/validate-openspec-cli-pin.py`, standard-library-only and fail-closed, five named refusal codes and one fixed remediation trailer — and it is BOTH the pin's verifier AND the consumer entrypoint through which strict validation runs, which is the design rather than an economy. (3) `.github/workflows/openspec-cli-pin-gate.yml`, which makes this the FIRST repository in the estate whose archive gate actually runs in continuous integration. (4) `tests/openspec_cli_pin/test_openspec_cli_pin.py`, 41 tests over the five checks, the refusal vocabulary, the cache's re-verification property and the gate's freedom from a second copy of the version. NOT THIS CHANGE'S SURFACE, each for a stated reason: the CONSUMING repositories' wiring (OpsxFactory, codexFactory, MedxFactory, LedgerxFactory, AdxFactory) is a successor change per repository and is named in the impact map below; the VERSION BUMP to a later CLI is a separate human-only governed change that must land its target-version evidence with it; the DEPENDENCY CLOSURE of the pinned artifact is a declared shortfall recorded in the pin's own header and named as successor work, not silently implied; and `.github/workflows/pytest-suite.yml`'s literal `@fission-ai/openspec@1.2.0` line is left ALONE in this packet and named as task 5.1, because replacing it touches the repository's most load-bearing required check and deserves its own diff rather than a rider on this one.
target_release: none (no contract-bundle involvement — every artifact this change adds is NEW and none is a registered row: `contracts/openspec-cli-pin.yaml` is a CONSUMPTION pin in the shape of `contracts/openreposhape-pin.yaml` and `contracts/openxwallet-pin.yaml`, and measured on this branch neither of those appears in `contracts/manifest.yaml` nor in any `contracts/releases/*.digests.yaml` inventory; `scripts/validate-openspec-cli-pin.py` is likewise a new unregistered validator, exactly as `scripts/validate-openreposhape-pin.py` is. No digest set moves, no `contract_bundle_version` is spent, and no release tag is owed. The archive gate is therefore `release-realization`'s merged-plus-green realization evidence for a non-empty code surface, and NOT a bundle cut.)
Status: ratified
---

# Proposal: add-openspec-cli-pin

Status: ratified
Ratified: Brett Heap, 2026-09-04 — verbatim "ratify 667", heard first-hand by
session opsxfactory-fb; record at `review/ratification-2026-09-04.md`, which
also records the relay path and the authoring lane's correct refusal to act
on a second-hand word.
Proposed: 2026-09-04
Origin: Operator instruction, Brett Heap, 2026-09-04, verbatim: *"draft the
openxFactory pin change, pinned at 1.2.0"*. The instruction is explicit that
this packet PINS THE CURRENT VERSION and does not bump it; the upgrade is a
later, separate change.

**RATIFICATION HAS NOT HAPPENED AND IS NOT SOUGHT BY THIS PACKET'S LANDING.**
*(True at authoring. RATIFIED 2026-09-04 — see the Ratified line above and
`review/ratification-2026-09-04.md`; the paragraph is kept as the record of
what this packet did and did not seek.)*
Brett Heap authorized the DRAFT. Every judgment the authoring session took is
listed in § Authoring decisions rather than presented as settled.

## Why

**The OpenSpec CLI is unpinned fleet-wide, and it is the tool that decides what
canon is.** `openspec validate --strict` is the gate every spec delta passes
before it may archive; `openspec archive` is the act that writes a ratified
delta into canon. Neither has ever run at a version anybody declared.

**The only pin anywhere in the estate is not a contract.** It is one literal
line — `.github/workflows/pytest-suite.yml:400`,
`npm install -g @fission-ai/openspec@1.2.0` — installed so
`tests/proposal-support/` can drive the real binary. No consuming repository
reads it. Nothing verifies it. Nothing refuses when a different version answers.
And OpenSpec offers no project-level version field to lean on instead:
`openspec/config.yaml` carries only `schema:`, and `openspec config` is
global-scope only. So the version is a property of whoever's machine is running,
and of nothing else.

**The archive gate runs in NO repository's continuous integration.** Measured
2026-09-04 across the estate: openxFactory's `pytest-suite.yml` installs the CLI
but validates nothing with it; OpsxFactory and codexFactory have zero workflows
that mention OpenSpec at all; MedxFactory, LedgerxFactory and AdxFactory have no
workflows at all. `openspec validate --all --strict` — the check every engineer
and agent believes is guarding the corpus — has been running on laptops, at
whatever version was installed there, and its result has been reported by the
person who ran it.

**A version bump is not a small thing, and the numbers say so.** Measured
2026-09-04, the same trees that pass CLEAN at 1.2.0 fail under 1.12.0:

| repository | at 1.2.0 | at 1.12.0 |
| --- | --- | --- |
| openxFactory | 89 passed, 0 failed (89 items) | 48 passed, 41 failed of 89 |
| OpsxFactory | clean | 34 passed, 10 failed of 44 |

**RE-MEASURED ON THIS BRANCH, 2026-09-04, and the re-measurement is worth
recording rather than trusting the first.** With this packet's own delta present
the tree is `49 passed, 41 failed (90 items)` at 1.12.0 and
`90 passed, 0 failed (90 items)` at 1.2.0 — the failure count is UNCHANGED at
41, so THIS PACKET IS CLEAN AT BOTH VERSIONS and adds nothing to the backlog the
upgrade will have to clear. The 89-item figures above are the same measurement
taken before this packet existed.

Every one of those failures is a PRE-EXISTING condition, not a regression
introduced by anybody: placeholder `## Purpose` sections that the `archive`
command itself writes, a duplicate task id, and at least four deltas the newer
`archive` would REFUSE outright — `MODIFIED` blocks written against headers the
main specification does not carry, or against specifications not yet created. So
an unpinned upgrade — which today is one `npm install -g` on one machine away —
turns two repositories red, stalls every archive in the estate, and does it in
the name of whoever happened to upgrade rather than in the name of the conditions
that predate them.

**Therefore: pin at 1.2.0 NOW, where everything is green; make the pin the only
way validation runs; and make the upgrade a separate governed change that must
prove the trees clean at the target before it lands.** Pinning where the estate
is green is what makes the upgrade a decision somebody can make deliberately,
with evidence, instead of an accident somebody discovers.

## What changes

### 1. `contracts/openspec-cli-pin.yaml` — the pin

`kind: pinned_contract_manifest`, reused unchanged, on both sibling pins'
reasoning: only the DISTRIBUTION FORM is new, so reusing the kind keeps
`neutral-product-pin` a statement about direction rather than a new shape.

**The referent is the tarball's SHA-512 integrity. The version string is a
label.** This is `contracts/openreposhape-pin.yaml`'s tag-versus-commit argument
transposed to a registry, and it survives the transposition intact:

* `sha512-2XDmPZ…` is a CONTENT ADDRESS over the published bytes. It cannot be
  moved, because moving it would require different bytes, and different bytes are
  a different address. All 270 files of the package are inside those bytes.
* `1.2.0` is a NAME. That npm declines to republish over a version is a REGISTRY
  POLICY — administered by an operator, with an unpublish window and an operator
  who can act inside it. A policy is not a content address. The version is
  recorded because humans, CI logs and `npm install` all speak in version
  numbers, on exactly the terms a release tag is recorded beside a commit in the
  sibling pin: as a human-readable label, never as the thing being trusted.

The registry's legacy `shasum` is recorded AND CHECKED — not merely recorded —
because a pin field that nothing verifies is a field free to drift into being
wrong unnoticed.

### 2. `scripts/validate-openspec-cli-pin.py` — the verifier and the entrypoint

One file doing both jobs, deliberately. Separating them would put back the exact
defect the pin exists to close: a verifier nobody is obliged to call, standing
beside a bare `openspec` invocation that answers with whatever is on `PATH`.

Five ordered checks, first failure wins: the pin's SHAPE; a SCAN TARGET was
given; the fetched artifact's recomputed SHA-512 and SHA-1 EQUAL the pin; the
resolved binary REPORTS the pinned version; `validate <target> --strict` runs and
its verdict is the tool's.

**It does not trust `npx` to have fetched the right thing.** It fetches the
tarball with `npm pack`, recomputes both digests, and refuses
`pin-integrity-mismatch` before anything is installed and long before anything is
invoked. `neutral-product-pin` requires exactly that ordering — digests verified
BEFORE the pinned reader is invoked, "by running code rather than by a stated
obligation" — and a `npx -y @fission-ai/openspec@1.2.0` that resolved the wrong
bytes would report nothing at all.

**The default mode never reads `PATH`**, which is the property the whole change
turns on: a gate that cannot read `PATH` cannot be made to pass or fail by what
an engineer happens to have installed. `--path-mode` exists for local iteration
and REFUSES `pin-version-mismatch` unless the local binary reports exactly the
pinned version; the gate does not pass it.

**There is no `--verify-only` mode**, and its absence is a requirement rather
than an oversight. A flag that verifies the pin and validates nothing is
precisely the target-less green check `neutral-product-pin` forbids — "a
self-test that opens no governed surface is a green check that verified nothing"
— and offering it would put the hole back behind a convenience.

### 3. `.github/workflows/openspec-cli-pin-gate.yml` — the gate

Mirrors `openreposhape-pin-gate.yml`. On every pull request it verifies the
artifact and runs `validate --all --strict` through it. **This makes openxFactory
the first repository in the estate whose archive gate actually runs in CI.**

The version is NOT written in the workflow. The verifier reads the pin with its
own parser, so there is exactly one place the referent is written — the sibling
gate's "fourth copy of the pin" argument, and
`test_the_gate_workflow_reads_the_pin_and_carries_no_fourth_copy` asserts the
absence against the workflow's own bytes.

Like the sibling, it is **not a required check on landing**: making a check
required is an operator act on an organisation ruleset, and a check is not
selectable until a workflow has reported under it once.

### 4. The spec delta

FOUR ADDED requirements — the CLI is a pinned neutral product and every strict
validation and archive runs at the pin; a consuming repository validates only
through the pinned entrypoint so `PATH` cannot affect a gate; a version bump is
human-only and lands its target-version evidence in the same change; a pin whose
content address cannot be verified refuses with a named remedy.

ONE MODIFIED requirement, and it is **required rather than optional**. The
ratified grammar is COMMIT-ONLY: "that pin SHALL carry the product's COMMIT, its
`revision_kind`, a per-file `sha256` … and `pinned_by_commit_only:` …". An npm
package has no commit this repository consumes and no per-file surface to
enumerate, so writing this pin under the unamended grammar would mean either
inventing a commit or declaring conformance the requirement does not grant. The
MODIFIED block therefore admits a published-artifact referent MINIMALLY — one
added body clause and two added scenarios, **every existing clause and all three
existing scenarios restated unchanged, nothing deleted, and no reserved deletion
marker owed**. It also argues why the two member lists are absent rather than
omitted: one digest over a tarball addresses every byte in it, so the
completeness obligation the lists exist to make checkable is discharged MORE
strongly here, not waived.

## Impact

**This change does not wire any other repository, and that is deliberate.** Each
consuming repository's wiring is a successor change in that repository, because
each has its own CI, its own validator conventions and its own
`stack.yaml` — and because a packet that edited six repositories from here would
be exactly the cross-repository authoring this estate's boundary rules refuse.

| repository | successor work |
| --- | --- |
| `codexFactory` | wire the pinned entrypoint into CI; pin the consumed `openxFactory` version in `stack.yaml` |
| `OpsxFactory` | same; its 44-item corpus is the one measured at 10 failures under 1.12.0, so it is the first place the pin's value is felt |
| `MedxFactory` | same; has no workflows at all today, so this is its first OpenSpec gate |
| `LedgerxFactory` | same |
| `AdxFactory` | same |

Also owed, and named rather than implied:

* **`.github/workflows/pytest-suite.yml:400`** — the literal
  `@fission-ai/openspec@1.2.0` becomes a read of the pin file. Left out of THIS
  packet on purpose: it edits the repository's most load-bearing required check,
  and it deserves its own diff and its own green run rather than a rider on this
  one. Recorded as task 5.1.
* **The dependency closure.** The referent addresses the CLI's own bytes. It does
  NOT address its nine caret-ranged runtime dependencies (`ora ^8.2.0`,
  `zod ^4.0.17`, `yaml ^2.8.2`, `chalk ^5.5.0`, `commander ^14.0.0`,
  `fast-glob ^3.3.3`, `posthog-node ^5.20.0`, `@inquirer/core ^10.2.2`,
  `@inquirer/prompts ^7.8.0`), which npm resolves at install time. This is a
  DECLARED SHORTFALL, written into the pin's own header, mitigated by installing
  with `--ignore-scripts` so an unpinned transitive dependency cannot run a
  lifecycle script inside a gate — a mitigation, not a repair. Closing it needs a
  lockfile the publisher does not ship, and is successor work.
* **The upgrade.** A separate, human-only governed change that re-cuts the pin
  from the real registry bytes and lands `--all --strict` proof at the TARGET
  version in the same change, remedying or declaring each pre-existing failure
  with its owner. **This packet does not bump the version and must not be read as
  approving one.**

## Authoring decisions

Recorded as decisions rather than presented as settled; the reasoning is in
`design.md`.

* **D1 — `kind: pinned_contract_manifest`, unchanged.** Both siblings' argument.
  A `<consumer>_<product>_pin` kind was rejected: that template governs
  DESCENDANTS, and openxFactory is not a descendant of a Node package.
* **D2 — the referent is the tarball integrity, the version is a label.** The
  alternative — treat the npm version as immutable and pin on it — was rejected
  because immutability there is a registry's policy rather than a content
  address, and the whole grammar exists to distinguish those two things.
* **D3 — the verifier and the consumer entrypoint are ONE file.** Rejected:
  separating them, which leaves a verifier nobody must call.
* **D4 — `npm pack`, not a direct HTTPS GET of the `tarball:` URL.** `npm pack`
  goes through the same resolution and the same local cache the rest of the
  estate's npm use does, so the bytes checked are the bytes an ordinary install
  would receive rather than a second, privileged path that could agree with the
  pin while everybody else's npm disagrees.
* **D5 — exit 1 for a validation failure, exit 2 for any refusal.** The siblings
  have no exit 1 by design, because their only question is "may this pull request
  proceed". This tool asks a second question they do not: having established
  which tool adjudicates, what did that tool say? "The pin could not be trusted"
  and "the pin held and your deltas are invalid" have completely different
  remedies. Both non-zero, so no gate is weakened.
* **D6 — no `--verify-only`, and `--strict` is a no-op with no `--no-strict`.**
  A target-less mode is the hole the grammar forbids; a non-strict pass is not the
  act this pin governs.
* **D7 — the install cache is keyed by the verified content address, and the
  ARTIFACT is re-verified on every run.** Only the install is reused. The fetch is
  cheap (npm serves a 200 KB artifact from its own cache) and the install is not,
  so there is no reason to buy speed by trusting a previous run's verdict about
  what the registry served.
* **D8 — the MODIFIED delta is required, and is written minimally.** See § What
  changes 4. The alternative — declaring conformance to a commit-only grammar
  that this pin cannot satisfy — was rejected as a false claim in the pin file.
* **D9 — `pytest-suite.yml`'s literal is left for a successor.** See § Impact.
