# Design: implement-openxpki-install-repo

Non-normative. The authoritative obligations are the ratified
`repo-boundary-governance` requirement *"OpenXPKI install repository
boundary"* — added by
[`add-trust-anchor`](../add-trust-anchor/specs/repo-boundary-governance/spec.md)
and restated by this change's
[one delta](specs/repo-boundary-governance/spec.md). This document records
the shape of the seed, the creation-time acts, and the four decisions that
were actually decisions.

Structurally parallel to the sibling
[`implement-keycloak-install-repo`](../implement-keycloak-install-repo/design.md)
by intent: same seed shape, same plumbing, same delta reasoning, with
D-openxpki-migration replacing that change's D-keycloak-reference. Where this
repository differs it differs for one reason — **it must never hold the
decision about what binary its certificate authority runs.**

## D-seed — the seed skeleton is a boundary made executable, not a deployment

The temptation with an install repository is to seed it with something that
runs. That is doubly wrong here: a running certificate authority arrives with
a datastore credential, an issuance credential, and CA key material — and the
ratified requirement forbids all three from ever being committed, *with no QA
exemption*, because a QA authority's key is still an authority key. So the
seed is the *boundary*, expressed in four artifacts, and nothing that runs.

**1. `README.md` — the ownership boundary, quoted.** The README states the
boundary VERBATIM from the ratified requirement rather than paraphrasing it,
because a paraphrase of neutral meaning is a restatement and `openxFactory`
remains the canonical owner of `trust-anchor`. Four claims, in the
requirement's own words:

- It owns the **OpenXPKI server, client, and web deployment topology** for QA
  and any later environment, and its own **install, verification, upgrade,
  backup, restore, and disaster-recovery procedures**.
- It owns the **per-client instantiation** at
  `config/clients/<tenant>/runtime-manifest.yaml` — **generated, never
  hand-edited**, digest-pinned by its consumers.
- It **SHALL consume ONLY the digest-pinned container image** whose custody —
  build sources, release / package / configuration / base-image pins, and the
  offline and integration test harness — remains in
  `opensoft/Opensoft-Tenant`, *because deciding what binary a tenant's
  certificate authority runs is a tenant trust decision*. It **MUST NOT**
  contain image build sources, a pipeline producing that image, a mutable
  image tag reference, secrets, credentials, or CA key material.
- The **three-way split**: `openxFactory` owns the neutral `trust-anchor`
  contract, the OpsxFactory `pki-administration` capability owns the governed
  administration procedure, `opensoft/Opensoft-Tenant` owns image custody —
  and this repository *realizes all three and owns none of them*.

The README also names the install / verify / upgrade / backup / restore / DR
procedure homes under `docs/` as empty-but-owned headings, so the first
person to write a DR runbook has a place to put it instead of inventing one.

**2. `config/contracts/trust-anchor/manifest.yaml` — the contract pin.**
Mirrors the `pinned_contract_manifest` shape `xFactory-Hermes-Install`
already uses at `config/contracts/<family>/manifest.yaml` —
`schema_version`, `kind`, `contract_bundle_tag`, `source_repository`, and a
`files:` map of per-file sha256 — with the `commit` / `revision_kind` fields
that install repo's top-level `config/compatibility-manifest.yaml` carries.
The pin is `contract-v1.37`, the bundle that realized the parent's contracts.
Eight schemas are in scope — `trust-anchor`, `certificate-record`,
`issuance-evidence`, `chain-custody-registry`, `dependent-binding`,
`renewal-record`, `revocation-propagation`, `conformance-declaration` — plus
the family's `trust-anchor-chain-custody.registry.yaml`.

**Where the digests come from, and a gap found while deciding that.** The
obvious source is the published release digest inventory
[`contracts/releases/contract-v1.37.digests.yaml`](../../../contracts/releases/contract-v1.37.digests.yaml).
It cannot be used for this family: that inventory carries **190 entries, none
of them under `contracts/trust-anchor/`** — the same 190 entries as
`contract-v1.36.digests.yaml`, i.e. both new families were registered in
`contracts/manifest.yaml` without the inventory being regenerated for the
cut. So the authoritative source for this pin is
[`contracts/manifest.yaml`](../../../contracts/manifest.yaml), whose
`trust-anchor-*` rows each carry a `sha256:` over the schema's bytes plus a
`consumption_rule` — the index the `implement-avatar-client-lab` precedent
already calls "the authoritative published index". The family README,
packaged examples, and the canonical validator are content-addressed by
commit with no per-file digest (the manifest says so, on the openxWallet and
client-identity-roster precedent), so the pin records them by commit rather
than inventing digests for them. A tag-only pin is refused, on the
`implement-avatar-client-lab` precedent: a tag can be moved, and the pin
exists precisely to prove which bytes of meaning this repository was built
against. The inventory gap is a real openxFactory bookkeeping defect, named
as a follow-up in tasks §4 and left with the bundle's own records — this
change does not edit a released bundle to seed a repository.

**3. The directory skeleton.** `config/clients/opensoft/` exists as a
PLACEHOLDER with a README and deliberately contains no
`runtime-manifest.yaml`: hand-writing one would violate the
generated-never-hand-edited rule in the very act of demonstrating it. The
placeholder documents the generation input and where the generated manifest
and its generation evidence will land, on the pattern
`xFactory-Hermes-Install` proved at `config/clients/opensoft/`
(`runtime-manifest.yaml` beside `runtime-manifest.generation-evidence.json`).
`deploy/` is the topology home following the hermes-install layout precedent
(`deploy/kubernetes` and `deploy/compose` side by side, so a cluster
deployment and a local bring-up do not fight over one directory) — and here
it is seeded as a HOME with its consumption rule and **no manifests**, for
the reason in D-openxpki-migration. `docs/` holds the procedure homes;
`scripts/` holds the validator.

**4. `scripts/validate-boundary.py` — the boundary made enforceable.** The
requirement's first scenario forbids image build sources, secrets,
credentials, and key material at creation; its second says boundary
validation MUST reject a container build, image pinning logic, or a mutable
tag reference and route it to `opensoft/Opensoft-Tenant`. A rule nothing
checks survives until the first bring-up under time pressure, so the seed
carries the check.

Design constraints, in order of importance:

- **Closed-world at the representation level, never a denylist of filenames.**
  The scan walks file BYTES and — for YAML/JSON — property NAMES and VALUES.
  A file named `ca-config-clean.yaml` gets the same treatment as one named
  `secrets.yaml`.
- **Reuse the established detection classes.** The contract-family validators
  in this repository already fought this fight; the validator borrows their
  classes rather than inventing a second definition of "secret". From
  [`scripts/validate-identity-brokering.py`](../../../scripts/validate-identity-brokering.py):
  the secret-shaped property-name token set (`secret`, `password`, `passwd`,
  `htpasswd`, `passphrase`, `private`, `mnemonic`, `api_key`, `apikey`,
  `bearer`, `token`), the **assigned-secret** class (`password: …`,
  `api_key=…` — the shape a configuration export takes), the PEM
  private-key armor class, the JWK-carrying-`d` class, the
  stored-password-verifier class (bcrypt / apr1 / SHA-crypt / SSHA), and the
  JWT-shaped bearer class. From
  [`scripts/validate-trust-anchor.py`](../../../scripts/validate-trust-anchor.py)
  — the more important half for a PKI repository — **reversible encodings**:
  base64, base64url, and hex runs are decoded (two layers, because an
  adversarial review walked five keys past a single-layer scan, including
  unarmored PKCS#8 DER as base64, the same DER as hex, a double-base64
  wrapper, an armor label split across two fields, and a DER blob labelled
  "QA only") and the value classes plus **DER private-key STRUCTURE** — a
  SEQUENCE, a version INTEGER, and the private-key algorithm OIDs — are
  re-run over the decoded bytes. Armor is a convention; structure is the
  thing.
- **Plus the two classes specific to THIS boundary**, which no existing
  validator has: (a) **image build sources and pipelines** — a `Dockerfile`,
  a `Containerfile`, a build context, a `docker build` / `buildx` / `podman
  build` invocation, or a workflow step producing an image; (b) **a mutable
  image tag reference** — an `image:` value that is not
  `<registry>/<repo>@sha256:<64 hex>`. Rule (b) is a positive shape test, not
  a blocklist of bad tags: `:latest`, `:3.31`, and a bare repository name are
  all refused by the same rule, because the requirement's second scenario is
  about the *decision* being reproduced here, not about which tag was chosen.
- **Small and self-contained.** Standard library plus the YAML parser already
  required to read the pin. No new dependency — a boundary check that cannot
  run in a bare container gets skipped.
- **A self-test corpus, not a claim.** A `positive/` tree that must pass and
  a `negative/` tree that must fail, each negative case labelled with the
  class it exercises — at minimum: a PEM CA private key; that same key
  base64-wrapped; an unarmored PKCS#8 DER blob as base64 and again as hex; an
  inline datastore password; a `Dockerfile`; a manifest with
  `image: …openxpki:latest`; and a manifest with a floating semver tag. The
  validator's own exit code over that corpus is the evidence in tasks §3, and
  the negative corpus is the only place in the repository where
  secret-SHAPED material legitimately lives — synthetic values only, never
  real ones, because a real key there would be the exact breach the validator
  exists to prevent.
- **Wired to CI later.** The seed lands the script and its self-test; the CI
  job and the required status check are a follow-up. Landing the script
  without the gate is honest about what is enforced today; claiming a green
  gate that does not exist is not.

## D-governance-plumbing — the creation-time acts, all of them at creation

Every one of these is cheap on an empty repository and expensive on a
populated one, so they are creation-time acts rather than follow-ups. This
list is identical to the sibling's by intent — one route, learned once.

- **Private.** The requirement's first sentence and first scenario both say
  private. A certificate authority's deployment topology names hosts, routes,
  datastore shapes, and issuance endpoints.
- **Default branch `main`**, matching every repository in the family.
- **A `main` ruleset requiring 1 approving review**, mirroring the family's
  gate. This is what makes the next decision necessary rather than nice.
- **Add the repository to the `openxfactory` GitHub App installation**
  (App id `4253636`, installation `145372182`) so the content App can author
  PRs into it.
- **`OPENXFACTORY_APP_ID` and `OPENXFACTORY_APP_PRIVATE_KEY` repository
  secrets**, plus a mirror of
  [`.github/workflows/session-open-pr.yml`](../../../.github/workflows/session-open-pr.yml)
  — the same file `openxFactory` and `OpsxFactory` already carry. Its own
  header states the reason: an interactive session otherwise opens PRs under
  the operator's `gh` auth, which makes the operator the AUTHOR, and GitHub's
  hard rule that a PR author cannot approve their own PR then blocks the only
  live human approver from satisfying the required review. Seeding the route
  on day one means the repository never has a first PR that its only reviewer
  is forbidden to approve. The route fixes authorship only — it never
  approves and never merges.

These are the *sole* GitHub-side acts. No environments, no deploy keys, no
Actions with cloud or ACR credentials, no packages — and specifically no
container registry wiring, which would be image custody arriving through the
side door.

## D-openxpki-migration — seed the HOME, not a second set of manifests

The QA server / client / web topology **already exists**. Another session
built it during the OpenXPKI QA bring-up and authored it inside
`opensoft/Opensoft-Tenant`, and the OpsxFactory change
`add-openxpki-qa-image-pipeline` was amended on 2026-08-21 — before its own
ratification — to record that those manifests' governed home is
`opensoft/OpenXPKI-Install`, adding a **tasks 3.4** obligation to migrate
them when this change creates the repository, and marking their present
location *transitional, not their governed home*. Image source, build, pins,
harness, and runbook/evidence templates stay tenant-owned.

So the decision here is about what NOT to do: **this change does not author
manifests.** Writing a second server/client/web topology would produce two
sets that must be reconciled, and the reconciliation would happen under the
pressure of a QA deployment — which is how a boundary becomes a fork. What
the seed carries instead is the home and the rules that will govern the
manifests when they arrive:

- `deploy/kubernetes/README.md` declaring the directory the governed home of
  the OpenXPKI server / client / web topology, naming
  `add-openxpki-qa-image-pipeline` tasks 3.4 as the migration path and
  `opensoft/Opensoft-Tenant` as the transitional origin.
- The **digest-consumption rule**, stated as a rule rather than as a value:
  *deploy ONLY the `opensoft/Opensoft-Tenant`-pinned immutable ACR digest,
  in `<registry>/<repository>@sha256:<digest>` form; never a tag.* The
  boundary validator enforces the shape (D-seed, rule (b)) so the rule is
  checkable and not merely written down.
- The **custody statement**: this repository consumes the digest and does not
  reproduce the decision that produced it — no build, no pipeline, no
  base-image pin, no harness.

**The honest dependency, stated plainly.** That OpsxFactory change is still
an **uncommitted working-tree draft owned by its authoring session**. It was
found already implemented through its QA gate (tasks 3.x / 4.x checked) and
is **not yet ratified**; the parent's tasks 2.3 is still open for exactly
this reason, on the good branch — the amendment is in the draft text BEFORE
ratification. The consequence for this change is specific: the **immutable
ACR digest** its QA gate produced is **not yet durably recorded** anywhere
this change can cite, and a digest read out of another session's uncommitted
tree is not a pin — it is a rumour with a hash in it.

Therefore: **seeding proceeds; the topology migration waits.** The seed
carries the rule with no digest value in it, and the placeholder says so
explicitly rather than leaving a reader to wonder whether a value was
forgotten. The migration — manifests moved, digest recorded, QA topology
governed here — is a later change, gated on that draft committing and
ratifying. Creating this repository now is what unblocks it: a migration task
naming a repository that does not exist cannot close, and the repository is
the half of the dependency this session can actually discharge.

## D-delta — one MODIFIED delta on this change's own parent requirement

**A delta is mandatory.** The first thing tested was whether this change
could carry no `specs/` delta at all, on the argument that it executes a
requirement rather than changing one. It cannot — validated over the sibling
change, whose structure is identical:

```
$ OPENSPEC_TELEMETRY=0 openspec validate implement-keycloak-install-repo --strict
Change 'implement-keycloak-install-repo' has issues
✗ [ERROR] file: Change must have at least one delta. No deltas found. …
EXIT=1
```

Given that a delta is required, the only honest one is the smallest true
statement this change makes: the creating act named in the requirement has
now run. So the delta is a `MODIFIED` restatement of *"OpenXPKI install
repository boundary"* whose only substantive edit is the creation clause —
`created by the …successor change` becomes `created 2026-08-21 by the
…successor change as opensoft/OpenXPKI-Install`.

Three properties of that choice are load-bearing:

- **Wholesale restatement, never partial.** An archived `MODIFIED` delta
  replaces the named requirement in its entirety, so the image-custody
  sentence, the MUST-NOT list, the three-way ownership paragraph, and all
  three scenarios are restated verbatim. Restating only the changed sentence
  would silently delete the custody split — the single most load-bearing
  clause in the requirement — which is the exact failure mode the family
  already has evidence for.
- **The two sibling changes cannot collide.** This change modifies *"OpenXPKI
  install repository boundary"*; the sibling modifies *"Keycloak install
  repository boundary"*. Different requirements, so two `MODIFIED` deltas can
  be in flight at once — which is why the two PARENTS each added their own
  requirement instead of both replacing one shared enumeration (their D8).
- **The *"Install repository scope"* enumeration is NOT touched.** Its
  refresh — enumerating both admitted install repos in one place — is already
  booked as [`add-trust-anchor` tasks 8.1](../add-trust-anchor/tasks.md), to
  be run after BOTH repositories exist and when nothing else is replacing
  that requirement. Adding a second claimant to it here would recreate the
  collision D8 was written to avoid.

**Two ordering obligations follow, and both are tasks rather than
assumptions.** First, the parent must archive before this change does: the
requirement this delta MODIFIES reaches `openspec/specs/` only when
`add-trust-anchor`'s ADDED delta promotes — and that parent declares a code
surface of its own, so it archives on its contract realization, not on this
change's. Strict validation does NOT catch this (this change validated green
with the base requirement still unpromoted), so it is verified by hand in
tasks §3. Second, the asserted creation date must be the real one: if
realization slips past 2026-08-21, the delta's `created 2026-08-21` is
corrected to the actual creation date before archive. The date is honest at
archive time because this change declares a code surface and therefore
archives only on merged realization evidence — the repository will exist
before the past-tense sentence is promoted.
