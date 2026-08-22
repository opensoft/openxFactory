# Design: implement-keycloak-install-repo

Non-normative. The authoritative obligations are the ratified
`repo-boundary-governance` requirement *"Keycloak install repository
boundary"* — added by
[`add-identity-brokering`](../add-identity-brokering/specs/repo-boundary-governance/spec.md)
and restated by this change's
[one delta](specs/repo-boundary-governance/spec.md). This document records
the shape of the seed, the creation-time acts, and the four decisions that
were actually decisions.

The whole change is one act with a very small surface, so the design is
short on architecture and long on what is deliberately NOT built.

Structurally parallel to the sibling
[`implement-openxpki-install-repo`](../implement-openxpki-install-repo/design.md)
by intent: same seed shape, same plumbing, same delta reasoning, with
D-keycloak-reference replacing that change's D-openxpki-migration.

## D-seed — the seed skeleton is a boundary made executable, not a deployment

The temptation with an install repository is to seed it with something that
runs. That is the wrong first commit: a running thing arrives with a
datastore password, an admin bootstrap credential, and a realm — and the
ratified requirement forbids all three from ever being committed. So the seed
is the *boundary*, expressed in four artifacts, and nothing that runs.

**1. `README.md` — the ownership boundary, quoted.** The README states the
boundary VERBATIM from the ratified requirement rather than paraphrasing it,
because a paraphrase is a restatement and restatement is exactly what the
requirement's last paragraph and fifth scenario forbid. Three claims, in the
requirement's own words:

- It owns the broker **deployment topology** — manifests, ingress and
  routing, datastore topology, backup, restore, upgrade, verification, and
  disaster recovery.
- It owns the **per-client instantiation** of that topology as
  `config/clients/<tenant>/runtime-manifest.yaml`, on the
  `xFactory-Hermes-Install` precedent: **generated from the deployed stack,
  never hand-edited**, and digest-pinned by its consumers.
- It **MUST NOT** contain a service-client secret, an upstream
  identity-provider credential, a datastore credential, an administrative
  bootstrap credential, key material, or a broker configuration or realm
  export carrying credential values; it MUST NOT restate neutral contract
  meaning (`openxFactory` owns `identity-brokering`); and it MUST NOT carry
  the governed administration workflow (the owning DomainxFactory owns
  `keycloak-administration`).

The README also names the install / verify / upgrade / backup / restore / DR
procedure homes under `docs/` as empty-but-owned headings. Naming the home
before the procedure exists is the point: it is where the first person to
write a DR runbook will put it, instead of inventing a second location.

**2. `config/contracts/identity-brokering/manifest.yaml` — the contract
pin.** Mirrors the `pinned_contract_manifest` shape
`xFactory-Hermes-Install` already uses at
`config/contracts/<family>/manifest.yaml` — `schema_version`, `kind`,
`contract_bundle_tag`, `source_repository`, and a `files:` map of per-file
sha256 — with the `commit` / `revision_kind` fields that install repo's
top-level `config/compatibility-manifest.yaml` carries, because the ratified
requirement demands the bundle tag **plus exact contract commit and digests**
and the family-level manifest alone records only the tag. The pin is
`contract-v1.37`, the bundle that realized the parent's contracts.

**Where the digests come from, and a gap found while deciding that.** The
obvious source is the published release digest inventory
[`contracts/releases/contract-v1.37.digests.yaml`](../../../contracts/releases/contract-v1.37.digests.yaml)
(`digest_source: raw_git_blob`). It cannot be used for this family: that
inventory carries **190 entries, none of them under
`contracts/identity-brokering/`** — the same 190 entries as
`contract-v1.36.digests.yaml`, i.e. the new families were registered in
`contracts/manifest.yaml` without the inventory being regenerated for the
cut. So the authoritative source for this pin is
[`contracts/manifest.yaml`](../../../contracts/manifest.yaml), whose
`identity-brokering-*` rows each carry a `sha256:` over the schema's bytes
plus a `consumption_rule` — and which the `implement-avatar-client-lab`
precedent already calls "the authoritative published index". The six schemas
in scope are `persona-assertion`, `broker-organization`,
`actor-subject-reference`, `identity-link-record`,
`broker-client-declaration`, and `surface-adoption`; the family README,
packaged examples, and the canonical validator are content-addressed by
commit with no per-file digest (the manifest's own comment says so,
following the openxWallet and client-identity-roster precedent), so the pin
records them by commit rather than inventing digests for them.

The inventory gap is a real openxFactory bookkeeping defect, not a reason to
hand-compute digests here. It is named as a follow-up in tasks §4 and left
where it belongs — with the bundle's own records — because this change must
not edit the released bundle to seed a repository.

A tag-only pin is refused, on the `implement-avatar-client-lab` precedent
("record both refs, commit + per-file SHA-256, in one pin; a tag-only pin
fails"): a tag can be moved, and the whole reason the pin exists is that this
repository must be able to prove which bytes of meaning it was built against.

**3. The directory skeleton.** `config/clients/opensoft/` exists as a
PLACEHOLDER with a README, and deliberately contains no
`runtime-manifest.yaml`. Writing one by hand would violate the
generated-never-hand-edited rule in the very act of demonstrating it; the
placeholder instead documents the generation input and where the generated
manifest and its generation evidence will land, on the pattern
`xFactory-Hermes-Install` proved at `config/clients/opensoft/`
(`runtime-manifest.yaml` beside `runtime-manifest.generation-evidence.json`).
`deploy/` is the topology home, following the hermes-install layout
precedent (`deploy/compose` and `deploy/kubernetes` side by side, so a
compose bring-up and a cluster deployment do not fight over one directory).
`docs/` holds the procedure homes. `scripts/` holds the validator.

**4. `scripts/validate-boundary.py` — the boundary made enforceable.** The
requirement's third scenario says repository-boundary validation MUST reject
a committed client secret, identity-provider credential, datastore
credential, key material, or a configuration or realm export containing
credential values. A rule nothing checks is a rule that survives exactly
until the first bring-up under time pressure, so the seed carries the check.

Design constraints, in order of importance:

- **Closed-world at the representation level, never a denylist of filenames.**
  The scan walks file BYTES and — for YAML/JSON — property NAMES and VALUES.
  A file named `realm-export-clean.json` gets the same treatment as one named
  `secrets.yaml`.
- **Reuse the established detection classes.** The contract-family validators
  in this repository already fought this fight; the validator borrows their
  classes rather than inventing a second definition of "secret". From
  [`scripts/validate-identity-brokering.py`](../../../scripts/validate-identity-brokering.py):
  the secret-shaped property-name token set (`secret`, `password`, `passwd`,
  `htpasswd`, `passphrase`, `private`, `mnemonic`, `api_key`, `apikey`,
  `bearer`, `token`), the **assigned-secret** class
  (`client_secret=…`, `admin_password: …`, `KEYCLOAK_ADMIN_PASSWORD=…` — the
  shape a configuration export takes), the PEM private-key armor class, the
  JWK-carrying-`d` class, the stored-password-verifier class
  (bcrypt / apr1 / SHA-crypt / SSHA), and the JWT-shaped bearer class. From
  [`scripts/validate-trust-anchor.py`](../../../scripts/validate-trust-anchor.py):
  **reversible encodings** — base64 and base64url and hex runs are decoded
  (two layers, because an adversarial review walked a key past a single-layer
  scan) and the value classes plus DER private-key structure are re-run over
  the decoded bytes.
- **Small and self-contained.** Standard library plus the YAML parser
  already required to read the pin. No new dependency, because a boundary
  check that cannot run in a bare container is a boundary check that gets
  skipped.
- **A self-test corpus, not a claim.** A `positive/` tree that must pass and
  a `negative/` tree that must fail, each negative case labelled with the
  class it exercises — including at minimum: a Keycloak realm export
  carrying a `client_secret` value, a compose file with an inline
  `POSTGRES_PASSWORD`, a PEM private key, the same key base64-wrapped, and an
  htpasswd verifier. The validator's own exit code over that corpus is the
  evidence in tasks §3, and the negative corpus is the only place in the
  repository where secret-SHAPED material legitimately lives (synthetic
  values, never real ones).
- **Wired to CI later.** The seed lands the script and its self-test; the CI
  job that runs it on every push is the next change's business, together
  with the ruleset status check. Landing the script without the gate is
  honest about what is enforced today; claiming a green gate that does not
  exist is not.

## D-governance-plumbing — the creation-time acts, all of them at creation

Every one of these is cheap on an empty repository and expensive on a
populated one, so they are creation-time acts rather than follow-ups.

- **Private.** The requirement's first sentence and its first scenario both
  say private. A broker's deployment topology names hosts, routes, and
  datastore shapes.
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
Actions with cloud credentials, no packages.

## D-keycloak-reference — the local compose workspace is reference, the fork is out of scope

**`/home/brett/projects/keycloak/` is REFERENCE ONLY.** It is an untracked
local workspace (a `Dockerfile` layering shell tooling onto
`quay.io/keycloak/keycloak:26.1.5`, a `docker-compose.yml` running Keycloak
against `postgres:16`, a `realms/dartwing/` export, and a `themes/` tree). It
is genuinely useful for one thing — the *shape* of a compose bring-up and its
Postgres wiring — and it is mined for that shape and nothing else.

It is **not imported wholesale**, for a reason the repository's own boundary
validator would enforce anyway: its `docker-compose.yml` carries
`POSTGRES_PASSWORD: keycloak`, `--db-password=keycloak`, and
`KEYCLOAK_ADMIN_PASSWORD: admin` as literal inline values — three clean hits
on the assigned-secret class — and a realm export is precisely the artifact
the ratified requirement's third scenario names, because realm exports CAN
embed client secrets even when a given export happens not to. "This
particular export was checked and was clean" is not a boundary; the boundary
is that credential-bearing exports do not live here at all. Values like
`keycloak`/`admin` are also not credentials worth migrating — they are
development defaults that must not survive contact with a governed
deployment.

So: the compose/DB shape informs `deploy/compose/`; the realm export informs
nothing and is not copied; the themes are a later product question, not a
boundary question.

**`opensoft/keycloak` — the stale public fork — is OUT OF SCOPE.** It is an
upstream fork, public, last touched 2025-10, and unrelated to this
repository's purpose. It needs a disposition (archive it, or repurpose it),
and that disposition is worth making deliberately rather than as a side
effect of creating a different repository. It is NAMED here so the decision
is not lost, and it is not touched: nothing in this change reads, writes,
renames, archives, or re-points it. Note in particular that its existence is
a reason the new repository's name is `Keycloak-Install` and not `keycloak`.

## D-delta — one MODIFIED delta on this change's own parent requirement

**A delta is mandatory.** The first thing tested was whether this change
could carry no `specs/` delta at all, on the argument that it executes a
requirement rather than changing one. It cannot:

```
$ OPENSPEC_TELEMETRY=0 openspec validate implement-keycloak-install-repo --strict
Change 'implement-keycloak-install-repo' has issues
✗ [ERROR] file: Change must have at least one delta. No deltas found. …
EXIT=1
```

Given that a delta is required, the only honest one is the smallest true
statement this change makes: the creating act named in the requirement has
now run. So the delta is a `MODIFIED` restatement of
*"Keycloak install repository boundary"* whose only substantive edit is the
creation clause — `created by the …successor change` becomes
`created 2026-08-21 by the …successor change as opensoft/Keycloak-Install`.

Three properties of that choice are load-bearing:

- **Wholesale restatement, never partial.** An archived `MODIFIED` delta
  replaces the named requirement in its entirety, so all four paragraphs and
  all five scenarios are restated verbatim. Restating only the changed
  paragraph would silently delete the four MUST-NOTs and every scenario —
  the exact failure mode the family already has evidence for.
- **The two sibling changes cannot collide.** This change modifies *"Keycloak
  install repository boundary"*; the sibling modifies *"OpenXPKI install
  repository boundary"*. Different requirements, so two `MODIFIED` deltas can
  be in flight at once — which is why the two PARENTS each added their own
  requirement instead of both replacing one shared enumeration.
- **The *"Install repository scope"* enumeration is NOT touched.** Its
  refresh — enumerating both admitted install repos in one place — is already
  booked as [`add-trust-anchor` tasks 8.1](../add-trust-anchor/tasks.md), to
  be run when nothing else is replacing that requirement. Adding a second
  claimant to it here would recreate the collision D8 of both parents was
  written to avoid.

**Two ordering obligations follow, and both are tasks rather than
assumptions.** First, the parent must archive before this change does: the
requirement this delta MODIFIES reaches `openspec/specs/` only when
`add-identity-brokering`'s ADDED delta promotes. Strict validation does NOT
catch this (it validated green with the base requirement still unpromoted),
so it is verified by hand in tasks §3. Second, the asserted creation date
must be the real one: if realization slips past 2026-08-21, the delta's
`created 2026-08-21` is corrected to the actual creation date before archive.
The date is honest at archive time because this change declares a code
surface and therefore archives only on merged realization evidence — the
repository will exist before the past-tense sentence is promoted.
