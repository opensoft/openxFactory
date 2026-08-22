# Tasks: implement-openxpki-install-repo

Dependency-ordered. §1 must complete before §2 (there is no repository to
seed until it exists), §2 before §3 (evidence is read back off the seeded
tree), and §4 is the named work this change deliberately does NOT do.

**Realization status, 2026-08-21.** The repository exists, is seeded, and its
boundary validator is green; the creation record is
[evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md).
**Updated 2026-08-21 (later the same day):** **1.2** landed post-seed
(ruleset id 21177148) and **1.3 / 3.3** are now closed — Brett performed the
org-owner act adding both new repositories to the `openxfactory` App
installation, read back on installation `145372182`. One box remains open:
**3.5** (the parent `add-trust-anchor` has not archived, so this change must
not either). §4 is untouched by design — the topology migration (4.2) is
explicitly not part of this change's realization bar; its
aggregation-admission item (4.1) and enumeration-refresh item (4.6) are
annotated with the change that executed each, and stay unticked because both
are acts of another change.

Reasoning for every decision below is in [design.md](design.md); the
authoritative obligations are the ratified requirement restated in
[specs/repo-boundary-governance/spec.md](specs/repo-boundary-governance/spec.md).
Structurally parallel to the sibling
[`implement-keycloak-install-repo`](../implement-keycloak-install-repo/tasks.md).

## 1. Creation acts (GitHub-side; design D-governance-plumbing)

- [x] 1.1 Create `opensoft/OpenXPKI-Install` — **private**, description
      naming it the deployable OpenXPKI certificate-authority install
      repository for the Opensoft production core, default branch **`main`**.
      Name is exactly `OpenXPKI-Install` (Opensoft-level, unprefixed,
      CloudPC-Install precedent) per the parent's 2026-08-21 Amendment.
      **DONE 2026-08-21** — `opensoft/OpenXPKI-Install`, repository id
      `1342329163`, private, default branch `main`, description as specified.
      Read-back in
      [evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md)
      §3.1-3.2.
- [x] 1.2 DONE 2026-08-21 post-seed — repo-level ruleset "main review gate" (id 21177148, enforcement active, required_approving_review_count: 1) created and read back layered over the two org rulesets. Add a `main` **ruleset requiring 1 approving review**, mirroring
      the family's gate. Do not add a required status check yet — the
      boundary validator's CI job is a follow-up (task 4.5), and a required
      check with no workflow blocks every PR.
      **PENDING — orchestrator, post-seed.** No repository-level ruleset
      exists yet. Two ORGANIZATION-level rulesets are inherited (`Copilot
      Auto-Review All PRs`; `Require Code Owner Review`, whose
      `required_approving_review_count` is **0**), so the inherited pair is
      NOT this gate. Rulesets combine rather than override, so the
      repository-level one will be a third over the same ref.
- [x] 1.3 Add the repository to the **`openxfactory` GitHub App
      installation** (App id `4253636`, installation `145372182`) so the
      content App can author PRs into it.
      **DONE 2026-08-21 — Brett (organization owner) performed the add**
      ("the two repos are added to openXfactory github app"). Read back off
      the installation, not asserted: `GET
      user/installations/145372182/repositories` lists
      `opensoft/OpenXPKI-Install` among **19** repositories on installation
      `145372182` for App `4253636`. Corroborated with the token at hand via
      `GET orgs/opensoft/installations` — installation `145372182`,
      `app_slug: openxfactory`, `repository_selection: selected`; the
      per-repository list itself needs an App-authorized token (a user token
      is refused 403, and `repos/{repo}/installation` needs a JWT), so the
      App-authorized read is the citable one. Recorded in
      [evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md)
      *"Addendum — App installation read-back"*. The earlier HTTP 403
      (*"only an Organization Owner can modify this app"*) is why the seed
      arrived by direct push (see 2.1); that deviation stands as recorded and
      is not retroactively repaired.
- [x] 1.4 Set the repository secrets **`OPENXFACTORY_APP_ID`** and
      **`OPENXFACTORY_APP_PRIVATE_KEY`** for that App. The
      `session-open-pr` workflow's preflight fails closed when either is
      absent, so set both before 1.5 is exercised.
      **DONE 2026-08-21** — both secrets present, read back by NAME only:
      `OPENXFACTORY_APP_ID`, `OPENXFACTORY_APP_PRIVATE_KEY`. Values were never
      read.
- [x] 1.5 Mirror **`.github/workflows/session-open-pr.yml`** — the same file
      `openxFactory` and `OpsxFactory` carry, unchanged. Rationale is in the
      file's own header: an interactive session otherwise authors PRs as the
      operator, and a PR author cannot approve their own PR, which would
      block the only live human approver against the 1.2 ruleset. The route
      fixes authorship ONLY; it never approves and never merges.
      **DONE 2026-08-21** — copied verbatim from
      `OpsxFactory/.github/workflows/session-open-pr.yml` (105 lines,
      byte-identical) in the seed commit. Mirrored, not yet exercised: the
      route cannot mint an App token until 1.3 lands.
- [x] 1.6 Confirm no other GitHub-side surface was created: no environments,
      no deploy keys, no cloud or ACR credentials in Actions secrets, no
      container registry wiring, no packages, no pages. Anything beyond
      1.1-1.5 is out of scope — and registry wiring in particular would be
      image custody arriving through the side door.
      **DONE 2026-08-21** — read back, not asserted: environments
      `total_count: 0`, deploy keys `0`, `has_pages: false`, Actions secrets
      exactly the two App secrets. **No ACR or cloud credential and no
      container-registry wiring of any kind** — the one that mattered most
      here, since registry wiring would be image custody arriving through the
      side door.

## 2. Seed the skeleton (design D-seed, D-openxpki-migration)

- [x] 2.1 Directory skeleton on `main` via the 1.5 authorship route:
      `config/contracts/trust-anchor/`, `config/clients/opensoft/`,
      `deploy/kubernetes/`, `deploy/compose/`, `docs/`, `scripts/`. The
      `deploy/kubernetes` + `deploy/compose` split follows the
      `xFactory-Hermes-Install` layout precedent.
      **DONE 2026-08-21** — all six directories present in seed commit
      `05f440444d9091206778e838454ed9b5bb7bff60`. **Deviation, recorded:** the
      seed landed by **direct push to `main`**, not via the 1.5 authorship
      route, because 1.3 failed 403 and the route therefore cannot author
      anything yet. The repository was empty, so the push created `main` at
      the seed commit.
- [x] 2.2 `README.md` stating the ownership boundary **verbatim** from the
      ratified requirement: the server / client / web deployment-topology
      scope for QA and any later environment; the repository's own install,
      verification, upgrade, backup, restore, and disaster-recovery
      procedures; the per-client `config/clients/<tenant>/runtime-manifest.yaml`
      rule (**generated, never hand-edited**, digest-pinned by its
      consumers); the **consume-ONLY-the-digest-pinned-image** clause with
      its reason (deciding what binary a tenant's certificate authority runs
      is a tenant trust decision); and the MUST-NOT list (no image build
      sources, no pipeline producing that image, no mutable image tag
      reference, no secrets, no credentials, no CA key material). Quote
      rather than paraphrase — `openxFactory` owns `trust-anchor` meaning.
      **DONE 2026-08-21** — `README.md` quotes BOTH paragraphs of the ratified
      requirement verbatim as a blockquote: the server / client / web scope
      for QA and any later environment, the repository's own six procedures,
      the generated-never-hand-edited per-client manifest, the
      consume-ONLY-the-digest-pinned-image clause **with its reason**
      (deciding what binary a tenant's certificate authority runs is a tenant
      trust decision), the full MUST-NOT list, and the three-way ownership
      sentence. It states that the requirement wins on any disagreement.
- [x] 2.3 In the same README, state the **three-way ownership split**
      explicitly — `openxFactory` owns the neutral `trust-anchor` contract,
      OpsxFactory `pki-administration` owns the governed administration
      procedure, `opensoft/Opensoft-Tenant` owns image custody, and this
      repository realizes all three and owns none of them — and name the
      **procedure homes** under `docs/` as owned-but-empty headings: install,
      verify, upgrade, backup, restore, disaster recovery.
      **DONE 2026-08-21** — the three-way split is an explicit table
      (`openxFactory` neutral contract / OpsxFactory `pki-administration`
      governed procedure / `opensoft/Opensoft-Tenant` image custody) with the
      closing claim that this repository *realizes all three and owns none of
      them*, and the image-custody row is flagged as the load-bearing one. The
      six procedure homes are named as an owned-but-empty table in `README.md`
      and repeated as `docs/README.md`'s own index, which adds the CA-specific
      obligation that backup / restore / DR describe restoring key material
      from its declared custody, never a copy kept here.
- [x] 2.4 `config/contracts/trust-anchor/manifest.yaml` — the contract pin.
      Shape mirrors `xFactory-Hermes-Install`'s `pinned_contract_manifest`
      (`schema_version`, `kind`, `contract_bundle_tag: contract-v1.37`,
      `source_repository: opensoft/openxFactory`, `files:` map of per-file
      sha256) PLUS the `commit` / `revision_kind` fields its
      `config/compatibility-manifest.yaml` carries. Record the exact commit
      the annotated `contract-v1.37` tag resolves to on published
      `origin/main`. Digests are READ from the `trust-anchor-*` rows of
      `contracts/manifest.yaml` — the authoritative published index — for the
      eight schemas (`trust-anchor`, `certificate-record`,
      `issuance-evidence`, `chain-custody-registry`, `dependent-binding`,
      `renewal-record`, `revocation-propagation`,
      `conformance-declaration`) plus
      `trust-anchor-chain-custody.registry.yaml`, never retyped by hand. Do
      **NOT** read them from
      `contracts/releases/contract-v1.37.digests.yaml`: that inventory
      carries 190 entries and none under `contracts/trust-anchor/` (see
      design D-seed and task 4.7). The family README, packaged examples, and
      the canonical validator carry no per-file digest by design and are
      pinned by commit. A tag-only pin is refused.
      **DONE 2026-08-21** — `config/contracts/trust-anchor/manifest.yaml`:
      `pinned_contract_manifest`, `contract_bundle_tag: contract-v1.37`,
      `source_repository: opensoft/openxFactory`, `commit:
      c1ffa0fdd358f8db7a86dff4c7c40583e581adff` (what the annotated tag
      resolves to on published `origin/main`), `revision_kind: commit`,
      `digest_source: contracts/manifest.yaml`, and per-file sha256 for the
      eight schemas plus `trust-anchor-chain-custody.registry.yaml`, read from
      the `trust-anchor-*` rows. All nine were **re-derived from the tag's own
      blobs** (`git cat-file blob contract-v1.37:<path> | sha256sum`) and
      match byte for byte. The release inventory was re-checked: still 190
      entries, none under `contracts/trust-anchor/` — its only `trust-anchor`
      matches are the unrelated
      `contracts/hermes-runtime/installation-trust-anchor*` pair — so 4.7
      stands. README / examples / validator / pytest wiring are listed under
      `pinned_by_commit_only`.
- [x] 2.5 `config/clients/opensoft/README.md` — the placeholder. It documents
      the generation input and where the generated `runtime-manifest.yaml`
      and its generation-evidence file will land (the
      `xFactory-Hermes-Install` `config/clients/opensoft/` pattern), and it
      contains **no `runtime-manifest.yaml`**: hand-writing one would break
      the generated-never-hand-edited rule in the act of illustrating it.
      **DONE 2026-08-21** — `config/clients/opensoft/README.md` documents the
      generation inputs (including the immutable image digest the topology
      consumed, recorded here and decided elsewhere) and both landing files,
      and contains **no** `runtime-manifest.yaml`.
- [x] 2.6 `deploy/kubernetes/README.md` — the topology HOME, **with no
      manifests** (design D-openxpki-migration). It declares the directory
      the governed home of the OpenXPKI server / client / web topology; names
      the amended OpsxFactory `add-openxpki-qa-image-pipeline` **tasks 3.4**
      as the migration path and `opensoft/Opensoft-Tenant` as the
      transitional origin; states the **digest-consumption rule** — deploy
      ONLY the `opensoft/Opensoft-Tenant`-pinned immutable ACR digest in
      `<registry>/<repository>@sha256:<digest>` form, **never a tag**; and
      states the custody rule — this repository consumes the digest and does
      not reproduce the decision that produced it (no build, no pipeline, no
      base-image pin, no harness). Record explicitly that **no digest value
      is present yet and why** (the producing change is an uncommitted draft;
      see 4.2) so a reader does not read the absence as an omission. Do NOT
      author manifests here — a second topology would have to be reconciled
      with the existing one under QA pressure.
      **DONE 2026-08-21** — `deploy/kubernetes/README.md` (89 lines, **no
      manifests**): declares the directory the governed home of the server /
      client / web topology; names `add-openxpki-qa-image-pipeline` **tasks
      3.4** as the migration path and `opensoft/Opensoft-Tenant` as the
      transitional origin (present location transitional, not governed);
      states the digest-consumption rule as a rule — deploy ONLY the
      tenant-pinned immutable ACR digest in
      `<registry>/<repository>@sha256:<digest>` form, **never a tag**; states
      the custody rule (consumes the digest, reproduces neither build,
      pipeline, base-image pin, nor harness); and carries a dedicated section
      saying **no digest value is present yet and why** — the producing change
      is an uncommitted, unratified working-tree draft, and a digest read out
      of another session's uncommitted tree is not a pin. It also explains why
      a second topology is not authored here.
- [x] 2.7 `scripts/validate-boundary.py` — refuses committed secrets,
      credentials, CA key material, image build sources, image-producing
      pipelines, and mutable image tag references. Walks file bytes and, for
      YAML/JSON, property names AND values; closed-world at the
      representation level, never a filename denylist. Reuses the established
      detection classes rather than inventing a second definition of
      "secret": from `validate-identity-brokering.py` the secret-shaped
      property-name tokens, the assigned-secret class, the PEM private-key
      armor class, the JWK-carrying-`d` class, the stored password-verifier
      class (bcrypt / apr1 / SHA-crypt / SSHA), and the JWT-shaped bearer
      class; from `validate-trust-anchor.py` the reversible-encoding pass
      (base64, base64url, and hex runs decoded two layers deep) with the
      value classes **and DER private-key STRUCTURE** (SEQUENCE, version
      INTEGER, private-key algorithm OIDs) re-run over the decoded bytes —
      armor is a convention, structure is the thing. Standard library plus
      the YAML parser only; no new dependency.
      **DONE 2026-08-21** — `scripts/validate-boundary.py` (747 lines). Byte
      pass, text pass, and a structural pass over YAML/JSON property names AND
      values; closed-world at the representation level with no filename
      denylist. Borrowed classes: `KEY_MATERIAL` (PEM armor, JWK-with-`d`, raw
      DER structure), `ENCODED_KEY_MATERIAL` (base64 / base64url / hex
      reversed two layers with the value classes **and DER private-key
      STRUCTURE** — SEQUENCE, version INTEGER, private-key algorithm OIDs —
      re-run over the decoded bytes), `ASSIGNED_SECRET`, `STORED_VERIFIER`,
      `BEARER_TOKEN`, `SECRET_PROPERTY`. Standard library plus PyYAML only;
      fails closed (exit 2) without the parser. **References are not values**:
      an entire-value `${ENV}` / `${{ … }}` / `{{ … }}` / `<placeholder>` /
      `scheme://…` / absolute mounted path is accepted, a `${VAR:-fallback}`
      is not.
- [x] 2.8 Add the two classes specific to THIS boundary, which no existing
      validator has: (a) **image build sources and pipelines** — a
      `Dockerfile`, a `Containerfile`, a build context, a `docker build` /
      `buildx` / `podman build` invocation, or a workflow step producing an
      image; (b) **mutable image tag references** — any `image:` value that is
      not `<registry>/<repository>@sha256:<64 hex>`. Rule (b) is a POSITIVE
      shape test, not a blocklist of bad tags: `:latest`, a pinned semver,
      and a bare repository name are all refused by the same rule, because
      the requirement's second scenario is about the decision being
      reproduced here, not about which tag was chosen.
      **DONE 2026-08-21** — both boundary-specific classes added. (a)
      `IMAGE_BUILD`: `Dockerfile` / `Containerfile` / `*.dockerfile` by name,
      a build source by CONTENT (an image base plus a further build
      instruction — so renaming the file is not a way past), a container build
      invocation, the image-producing pipeline tokens, and structurally a
      compose `build` stanza (guarded so a workflow job merely NAMED `build`
      is not a finding) or a build-source key. (b) `MUTABLE_IMAGE_TAG`: a
      POSITIVE shape test over parsed YAML/JSON — an `image`/`images` value
      must be `<registry>/<repository>@sha256:<64 hex>` with the registry a
      real host, so `:latest`, a pinned semver, and a bare repository name all
      fail the same rule; `newTag`/`image_tag` are refused outright, while
      `contract_bundle_tag` deliberately is not. Structural rather than
      textual so prose describing the rule is not a finding; that residue is
      stated in the validator's docstring. **The validator scans itself** —
      which is why the build-tool tokens are assembled from string fragments:
      written verbatim, each would make the validator its own `IMAGE_BUILD`
      finding, and a check that exempts itself has a hole in it.
- [x] 2.9 The validator's **self-test corpus**: a `positive/` tree that must
      pass and a `negative/` tree that must fail, each negative case labelled
      with the class it exercises. Minimum negative set: a PEM CA private
      key; that same key base64-wrapped; an unarmored PKCS#8 DER blob as
      base64 and again as hex; an inline datastore password; a `Dockerfile`;
      a manifest with `image: …openxpki:latest`; a manifest with a floating
      semver tag. Synthetic values only — the negative corpus is the one
      place secret-SHAPED material legitimately lives, and a real key there
      would be the breach the validator exists to prevent.
      **DONE 2026-08-21** — `scripts/boundary-selftest/{positive,negative}/`,
      4 positive and 12 negative cases, each negative labelled with its class
      in the filename; the self-test FAILS any class with no negative case, so
      all eight are exercised. Minimum set covered: PEM CA private key; the
      same key base64-wrapped; an unarmored PKCS#8 DER prologue as base64
      **and again as hex** (the base64 fixture even carries a "qa only" label,
      one of the five evasions from the trust-anchor adversarial review); an
      inline datastore password; a `Dockerfile` under a name that is not
      `Dockerfile`; a floating `:latest` manifest; and a floating-semver
      manifest. All values synthetic — a real key there would be the exact
      breach the validator exists to prevent.
- [x] 2.10 Confirm the seed contains **nothing that runs and nothing with
      custody**: no CA key, no issuance credential, no datastore password, no
      realm or CA configuration export, no Dockerfile, no build workflow, no
      image tag, no ACR credential. There is **no QA exemption** — the
      ratified `trust-anchor` requirement is explicit that a QA authority's
      key is still an authority key.
      **DONE 2026-08-21** — confirmed by the green whole-tree run plus
      inspection: no CA key, no issuance credential, no datastore password, no
      realm or CA configuration export, no Dockerfile, no build workflow, no
      image tag, no ACR credential; `deploy/` carries READMEs only. No QA
      exemption anywhere in the seeded text — `README.md`, `docs/README.md`,
      `deploy/*/README.md`, and `config/clients/opensoft/README.md` each
      restate it.

## 3. Evidence (the creation record)

- [x] 3.1 Record the repository **URL and remote**
      (`git@github.com:opensoft/OpenXPKI-Install.git`) and the exact seed
      commit on `main`.
      **DONE 2026-08-21** —
      [evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md)
      §3.1: URL, remote, repository id, created stamp, default branch, seed
      commit `05f440444d9091206778e838454ed9b5bb7bff60`, author/date, and the
      24-file/1407-line seeded tree.
- [x] 3.2 DONE 2026-08-21 — read-backs recorded in the creation record and its addendum: visibility private, default branch main, both secret names present, ruleset id 21177148 active with pull_request count 1 (source: Repository). Settings read-back, not assertion: visibility `private`,
      default branch `main`, and the `main` ruleset showing 1 required
      approving review. Capture the read-back output.
      **PARTIAL — the ruleset half waits on 1.2.** Captured and recorded:
      visibility `private` (both `private: true` and `visibility: "private"`),
      default branch `main`, plus the two inherited ORG rulesets verbatim. The
      `main` ruleset showing **1 required approving review does not exist
      yet**, so this task stays open rather than claiming a read-back that has
      nothing to read.
- [x] 3.3 App installation read-back: the repository present on
      installation `145372182` for App `4253636`, and both App secrets
      present (names only, never values). Optionally prove the route end to
      end by opening the seed PR through `session-open-pr` and confirming the
      author is `openxfactory[bot]`.
      **DONE 2026-08-21, after Brett's org-owner act (1.3).**
      `opensoft/OpenXPKI-Install` is present on installation `145372182` for
      App `4253636` — read back via `GET
      user/installations/145372182/repositories`, 19 repositories total. Both
      App secrets remain read back by name only, values never read
      (`OPENXFACTORY_APP_ID`, `OPENXFACTORY_APP_PRIVATE_KEY`). The
      **optional** end-to-end `openxfactory[bot]` authorship proof is still
      **not claimed**: the seed had already landed by direct push, so there is
      no PR left to open for it, and manufacturing one solely to exercise the
      route would be theatre. The first real PR into this repository will be
      the proof; the QA topology migration (4.2) or the CI-wiring follow-up
      (4.5) is its natural occasion. Recorded in
      [evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md)
      *"Addendum — App installation read-back"*.
- [x] 3.4 **Boundary validator green on the seeded tree**: `validate-boundary.py`
      exits 0 over the whole repository, AND its self-test passes — every
      `positive/` case accepted and every `negative/` case rejected with the
      expected class, the image-build and mutable-tag classes included. A
      validator that is green only because it finds nothing is not evidence;
      the negative corpus is what makes 3.4 mean something.
      **DONE 2026-08-21** —
      [evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md)
      §3.4, verbatim. Whole-repository scan exit **0** (`BOUNDARY CLEAN — 8
      file(s) scanned`); `--self-test` exit **0** (4 positive accepted, 12
      negative rejected each as the class it names, all 8 classes exercised
      **including `IMAGE_BUILD` and `MUTABLE_IMAGE_TAG`**); and a RED proof —
      the same scanner over the negative corpus as a tree, exit **1**, 13
      findings over 12 files, with the unarmored DER caught in both encodings,
      the build source caught by content under a non-`Dockerfile` name, and
      the pinned semver failing the same rule as `:latest`.
- [ ] 3.5 **Delta ordering check** (design D-delta): confirm
      `add-trust-anchor` has archived — i.e. the requirement *"OpenXPKI
      install repository boundary"* is present in
      `openspec/specs/repo-boundary-governance/spec.md` — BEFORE archiving
      this change. Strict validation does not catch this; verify by hand.
      **NOT SATISFIED YET, and correctly so.** Checked by hand:
      `openspec/specs/repo-boundary-governance/spec.md` carries nine
      requirements and *"OpenXPKI install repository boundary"* is **absent**
      — `add-trust-anchor` has not archived, and it declares a code surface of
      its own, so it archives on its contract realization rather than on this
      change's. This change's MODIFIED delta has nothing to replace yet, so it
      must not archive before its parent. Strict validation does not catch
      this.
- [x] 3.6 **Creation-date correction**: if creation landed after 2026-08-21,
      correct `created 2026-08-21` in the spec delta to the actual creation
      date before archive, so the promoted past-tense sentence is true.
      **DONE 2026-08-21 — no correction needed, reasoning recorded.** API
      `created_at` is `2026-08-22T00:33:46Z`, which in the timezone every
      other record in this family uses (`-04:00`, visible in the org rulesets'
      own stamps) is **2026-08-21 20:33:46**. The delta's `created 2026-08-21`
      is true as written. Flagged because the two readings differ by a
      calendar day: re-check at archive by the LOCAL date.
- [x] 3.7 `OPENSPEC_TELEMETRY=0 openspec validate implement-openxpki-install-repo
      --strict` and `--all --strict` green at archive as well as at
      authoring. This change declares a code surface, so it archives only on
      merged realization with green evidence (`release-realization`), which
      here means the repository created, seeded, and its boundary validator
      green. Note what it does NOT mean: the topology migration is task 4.2
      and is not part of this change's realization bar.
      **DONE 2026-08-21 (authoring + seed bar)** — `openspec validate
      implement-openxpki-install-repo --strict` → *is valid*, exit 0;
      `openspec validate --all --strict` → *Totals: 65 passed, 0 failed (65
      items)*, exit 0, item count unchanged. The archive-time run is not
      claimed: 3.5's gate is not satisfied. And as this task itself notes, the
      topology migration (4.2) is deliberately NOT part of this realization
      bar.

## 4. Named follow-ups — NOT this change

Each is a separate reviewed change. None is authorized by this ratification.

- [ ] 4.1 **Aggregation admission** — pin `installs/openxpki-install` in the
      top-level xFactory aggregation, recording path, remote, visibility,
      exact validated commit, recursive checkout, compatibility, update, and
      rollback. The ratified requirement is explicit: repository creation
      MUST NOT be treated as aggregation admission.
      **EXECUTED ELSEWHERE 2026-08-21 by
      [`admit-install-repos-to-aggregation`](../admit-install-repos-to-aggregation/proposal.md)**
      (ratified the same day: "do the aggregation admission change"). That
      change carries the eight-field admission record for
      `installs/openxpki-install` at the exact validated commit
      `05f440444d9091206778e838454ed9b5bb7bff60` — including the recursive
      checkout finding that this repository has no `.gitmodules` and does not
      vendor `opensoft/Opensoft-Tenant`, so the image-custody split survives a
      recursive checkout — and the `.gitmodules` + gitlink + README act lands
      by reviewed PR on `opensoft/xFactory`. **Deliberately left unticked**:
      this box is a follow-up that runs elsewhere, and the ratified
      requirement forbids repository creation from being treated as
      aggregation admission — a tick here would claim exactly that.
- [ ] 4.2 **QA topology migration** — the amended OpsxFactory
      `add-openxpki-qa-image-pipeline` **tasks 3.4**: move the QA server /
      client / web deployment manifests of its 3.1-3.3 out of
      `opensoft/Opensoft-Tenant` into `deploy/kubernetes/` here, and record
      the immutable ACR digest they consume. **Gated, not merely deferred**:
      that change is an uncommitted working-tree draft in its owning session,
      implemented through its QA gate but unratified, so the ACR digest it
      produced is not yet durably recorded anywhere citable — a digest read
      out of another session's uncommitted tree is not a pin. Seeding
      proceeds; this waits on that draft committing and ratifying. Image
      source, build, pins, harness, and runbook/evidence templates stay
      tenant-owned.
- [ ] 4.3 **OpsxFactory `pki-administration`** — the governed administration
      workflow as a SIBLING of `exchange-administration`,
      `aks-administration-workflow`, `github-administration-workflow`, and
      `business-central-administration` (not a profile of one of them), with
      the certificate-authority service-subject kind registered in lockstep
      (`customer-kinds` + Hermes template + `stack.yaml`, grant ceilings in
      `credentials/requirements.yaml`). Developed in
      `OpsxFactory:staging:identity-pki-administration`, shared with the
      identity half. The ratified requirement keeps that procedure out of
      this repository. Parent tasks 7.1.
- [ ] 4.4 **The deployment itself** — bring the QA topology up from this
      repository against the recorded digest, with the first GENERATED
      `config/clients/opensoft/runtime-manifest.yaml`. Its credentials — CA
      key material, issuance credentials, datastore — are
      `credential-contracts` records with declared custody, vault-bound,
      referenced by the deployment and never committed here, with no QA
      exemption.
- [ ] 4.5 **CI wiring for the boundary validator** — the workflow that runs
      `validate-boundary.py` on every push and PR, plus adding it as a
      required status check on the `main` ruleset. Seeded here (2.7-2.9),
      gated there.
- [ ] 4.6 **`add-trust-anchor` tasks 8.1 bookkeeping** — with both install
      repositories now existing, one change refreshes the
      `repo-boundary-governance` *"Install repository scope"* requirement so
      the admitted install repos are enumerated in one place, as a MODIFIED
      delta restating all its scenarios, run when nothing else is replacing
      that requirement. Explicitly NOT done here (design D-delta).
      **EXECUTED ELSEWHERE 2026-08-21 by
      [`admit-install-repos-to-aggregation`](../admit-install-repos-to-aggregation/specs/repo-boundary-governance/spec.md)** —
      one MODIFIED delta, both scenarios restated verbatim, enumeration
      extended with both admitted repositories; `add-trust-anchor` tasks 8.1
      is ticked there. Left unticked here for the same reason as 4.1: it is
      another change's act.
- [ ] 4.7 **openxFactory bookkeeping: the `contract-v1.37` release digest
      inventory is missing both new families.**
      `contracts/releases/contract-v1.37.digests.yaml` carries the same 190
      entries as `contract-v1.37`'s predecessor and none under
      `contracts/trust-anchor/` or `contracts/identity-brokering/`, so the
      inventory cannot be used to verify a pin against either family (task
      2.4 reads `contracts/manifest.yaml` instead). Found while deciding the
      pin's digest source; it is a defect in the released bundle's records,
      belongs to openxFactory, and this change deliberately does not edit a
      released bundle to seed a repository.
