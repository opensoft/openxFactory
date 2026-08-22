# Tasks: implement-keycloak-install-repo

Dependency-ordered. §1 must complete before §2 (there is no repository to
seed until it exists), §2 before §3 (evidence is read back off the seeded
tree), and §4 is the named work this change deliberately does NOT do.

**Realization status, 2026-08-21.** The repository exists, is seeded, and its
boundary validator is green; the creation record is
[evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md).
**Updated 2026-08-21 (later the same day):** **1.2** landed post-seed
(ruleset id 21177147) and **1.3 / 3.3** are now closed — Brett performed the
org-owner act adding both new repositories to the `openxfactory` App
installation, read back on installation `145372182`. One box remains open:
**3.5** (the parent `add-identity-brokering` has not archived, so this change
must not either). §4 is untouched by design; its aggregation-admission item
(4.1) and its enumeration-refresh item (4.8) are annotated with the change
that executed each, and stay unticked because both are acts of another
change.

Reasoning for every decision below is in [design.md](design.md); the
authoritative obligations are the ratified requirement restated in
[specs/repo-boundary-governance/spec.md](specs/repo-boundary-governance/spec.md).
Structurally parallel to the sibling
[`implement-openxpki-install-repo`](../implement-openxpki-install-repo/tasks.md).

## 1. Creation acts (GitHub-side; design D-governance-plumbing)

- [x] 1.1 Create `opensoft/Keycloak-Install` — **private**, description
      naming it the deployable identity-broker install repository for the
      Opensoft core, default branch **`main`**. Name is exactly
      `Keycloak-Install` (Opensoft-level, unprefixed, CloudPC-Install
      precedent) per the parent's 2026-08-21 Amendment; it is deliberately
      distinct from the stale public fork `opensoft/keycloak`, which this
      change does not touch (design D-keycloak-reference).
      **DONE 2026-08-21** — `opensoft/Keycloak-Install`, repository id
      `1342329131`, private, default branch `main`, description as specified.
      Read-back in
      [evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md)
      §3.1-3.2. The stale public fork `opensoft/keycloak` was not read,
      written, renamed, or re-pointed.
- [x] 1.2 DONE 2026-08-21 post-seed — repo-level ruleset "main review gate" (id 21177147, enforcement active, required_approving_review_count: 1) created and read back layered over the two org rulesets. Add a `main` **ruleset requiring 1 approving review**, mirroring
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
      `opensoft/Keycloak-Install` among **19** repositories on installation
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
      no deploy keys, no cloud-credential Actions secrets, no packages, no
      pages. Anything beyond 1.1-1.5 is out of scope for this change.
      **DONE 2026-08-21** — read back, not asserted: environments
      `total_count: 0`, deploy keys `0`, `has_pages: false`, Actions secrets
      exactly the two App secrets. No cloud-credential secret, no package, no
      environment, no deploy key.

## 2. Seed the skeleton (design D-seed)

- [x] 2.1 Directory skeleton on `main` via the 1.5 authorship route:
      `config/contracts/identity-brokering/`, `config/clients/opensoft/`,
      `deploy/compose/`, `deploy/kubernetes/`, `docs/`, `scripts/`. The
      `deploy/compose` + `deploy/kubernetes` split follows the
      `xFactory-Hermes-Install` layout precedent.
      **DONE 2026-08-21** — all six directories present in seed commit
      `1aa184e891d4ba6e641a31260d3f64d2b335f175`. **Deviation, recorded:** the
      seed landed by **direct push to `main`**, not via the 1.5 authorship
      route, because 1.3 failed 403 and the route therefore cannot author
      anything yet. The repository was empty, so the push created `main` at
      the seed commit.
- [x] 2.2 `README.md` stating the ownership boundary **verbatim** from the
      ratified requirement — the deployment-topology scope, the per-client
      `config/clients/<tenant>/runtime-manifest.yaml` rule (generated from
      the deployed stack, **never hand-edited**, digest-pinned by its
      consumers), and all three MUST-NOT clauses (no service-client secret /
      upstream IdP credential / datastore credential / admin bootstrap
      credential / key material / credential-bearing configuration or realm
      export; no restatement of neutral `identity-brokering` meaning, which
      `openxFactory` owns; no `keycloak-administration` workflow, which the
      owning DomainxFactory owns). Quote rather than paraphrase — a
      paraphrase is the restatement the requirement's fifth scenario refuses.
      **DONE 2026-08-21** — `README.md` quotes all FOUR paragraphs of the
      ratified requirement verbatim as a blockquote (scope, per-client
      generated-never-hand-edited manifest, the three MUST NOTs, the
      separate-reviewed-act aggregation paragraph), states that the
      requirement wins on any disagreement, and adds a checklist that re-lists
      the MUST NOTs without re-explaining `identity-brokering`.
- [x] 2.3 In the same README, name the **procedure homes** under `docs/` as
      owned-but-empty headings: install, verify, upgrade, backup, restore,
      disaster recovery. Naming the home before the procedure exists is what
      stops a second location being invented.
      **DONE 2026-08-21** — the six procedure homes are named in `README.md`
      as an owned-but-empty table (install / verify / upgrade / backup /
      restore / disaster-recovery, each `not written`), and `docs/README.md`
      repeats them as the directory's own index with the
      references-never-values and procedure-not-governed-administration rules.
- [x] 2.4 `config/contracts/identity-brokering/manifest.yaml` — the contract
      pin. Shape mirrors `xFactory-Hermes-Install`'s
      `pinned_contract_manifest` (`schema_version`, `kind`,
      `contract_bundle_tag: contract-v1.37`,
      `source_repository: opensoft/openxFactory`, `files:` map of per-file
      sha256) PLUS the `commit` / `revision_kind` fields its
      `config/compatibility-manifest.yaml` carries, because the ratified
      requirement demands bundle tag **plus exact contract commit and
      digests**. Record the exact commit the annotated `contract-v1.37` tag
      resolves to on published `origin/main`. Digests are READ from the
      `identity-brokering-*` rows of `contracts/manifest.yaml` — the
      authoritative published index — for the six schemas
      (`persona-assertion`, `broker-organization`, `actor-subject-reference`,
      `identity-link-record`, `broker-client-declaration`,
      `surface-adoption`), never retyped by hand. Do **NOT** read them from
      `contracts/releases/contract-v1.37.digests.yaml`: that inventory
      carries 190 entries and none under `contracts/identity-brokering/`
      (see design D-seed and task 4.7). The family README, packaged
      examples, and the canonical validator carry no per-file digest by
      design and are pinned by commit. A tag-only pin is refused.
      **DONE 2026-08-21** —
      `config/contracts/identity-brokering/manifest.yaml`:
      `pinned_contract_manifest`, `contract_bundle_tag: contract-v1.37`,
      `source_repository: opensoft/openxFactory`, `commit:
      c1ffa0fdd358f8db7a86dff4c7c40583e581adff` (what the annotated tag
      resolves to on published `origin/main`), `revision_kind: commit`,
      `digest_source: contracts/manifest.yaml`, and per-file sha256 for all
      six schemas read from the `identity-brokering-*` rows. All six were
      **re-derived from the tag's own blobs** (`git cat-file blob
      contract-v1.37:<path> | sha256sum`) and match byte for byte. The release
      inventory was re-checked and still carries 190 entries with none under
      `contracts/identity-brokering/`, so 4.7 stands. README / examples /
      validator are listed under `pinned_by_commit_only`.
- [x] 2.5 `config/clients/opensoft/README.md` — the placeholder. It documents
      the generation input and where the generated `runtime-manifest.yaml`
      and its generation-evidence file will land (the
      `xFactory-Hermes-Install` `config/clients/opensoft/` pattern), and it
      contains **no `runtime-manifest.yaml`**: hand-writing one would break
      the generated-never-hand-edited rule in the act of illustrating it.
      **DONE 2026-08-21** — `config/clients/opensoft/README.md` documents the
      generation inputs and both landing files (`runtime-manifest.yaml` beside
      `runtime-manifest.generation-evidence.json`, on the hermes-install
      precedent) and contains **no** `runtime-manifest.yaml`.
- [x] 2.6 `scripts/validate-boundary.py` — refuses committed secrets, key
      material, and credential-bearing realm or broker configuration
      exports. Walks file bytes and, for YAML/JSON, property names AND
      values; closed-world at the representation level, never a filename
      denylist. Reuses the established detection classes rather than
      inventing a second definition of "secret": from
      `validate-identity-brokering.py` the secret-shaped property-name
      tokens, the assigned-secret class (`client_secret=…`,
      `admin_password: …`, `KEYCLOAK_ADMIN_PASSWORD=…`), the PEM
      private-key armor class, the JWK-carrying-`d` class, the stored
      password-verifier class (bcrypt / apr1 / SHA-crypt / SSHA), and the
      JWT-shaped bearer class; from `validate-trust-anchor.py` the
      reversible-encoding pass (base64, base64url, and hex runs decoded two
      layers deep, with the value classes and DER private-key structure
      re-run over the decoded bytes). Standard library plus the YAML parser
      only — no new dependency.
      **DONE 2026-08-21** — `scripts/validate-boundary.py` (582 lines). Byte
      pass, text pass, and a structural pass over YAML/JSON property names AND
      values; closed-world at the representation level with no filename
      denylist. Six classes, all borrowed rather than re-derived:
      `KEY_MATERIAL` (PEM armor, JWK-with-`d`, raw DER structure),
      `ENCODED_KEY_MATERIAL` (base64 / base64url / hex reversed two layers,
      value classes and DER structure re-run over the decoded bytes),
      `ASSIGNED_SECRET`, `STORED_VERIFIER`, `BEARER_TOKEN`, `SECRET_PROPERTY`.
      Standard library plus PyYAML only; fails closed (exit 2) if the YAML
      parser is absent rather than reporting a partly-read tree as clean.
      **References are not values**: a credential-shaped field whose ENTIRE
      value is `${ENV}` / `${{ … }}` / `{{ … }}` / `<placeholder>` /
      `scheme://…` / an absolute mounted path is accepted; a
      `${VAR:-fallback}` is not, because the fallback is a committed literal.
      **The validator scans itself** — its first run flagged its own
      class-constant line as `ASSIGNED_SECRET`, and the fix was a declaration
      form (tuple + unpack), never an exemption.
- [x] 2.7 The validator's **self-test corpus**: a `positive/` tree that must
      pass and a `negative/` tree that must fail, each negative case
      labelled with the class it exercises. Minimum negative set: a realm
      export carrying a `client_secret` value; a compose file with an inline
      `POSTGRES_PASSWORD`; a PEM private key; that same key base64-wrapped;
      an htpasswd verifier. Synthetic values only — the negative corpus is
      the one place secret-SHAPED material legitimately lives, and real
      values there would be the breach the validator exists to prevent.
      **DONE 2026-08-21** — `scripts/boundary-selftest/{positive,negative}/`,
      4 positive and 6 negative cases, each negative labelled with its class
      in the filename. Minimum set covered: realm export carrying a
      `client_secret` value (caught structurally — a quoted JSON key defeats
      the text scan), compose file with an inline datastore password, PEM
      private key, the same key base64-wrapped, and an htpasswd verifier; plus
      a JWT-shaped bearer value. The self-test FAILS any class with no
      negative case. All values synthetic.
- [x] 2.8 Confirm the seed contains **nothing that runs**: no realm export,
      no compose or manifest with a resolved credential, no admin bootstrap,
      no datastore password, no key. Mine the local compose workspace at
      `/home/brett/projects/keycloak/` for the compose/Postgres SHAPE only
      (design D-keycloak-reference) — its inline `POSTGRES_PASSWORD`,
      `--db-password`, and `KEYCLOAK_ADMIN_PASSWORD` values and its
      `realms/dartwing/` export are not copied, and 2.6 would reject them if
      they were.
      **DONE 2026-08-21** — confirmed: no realm export, no resolved
      credential, no admin bootstrap value, no datastore password, no key.
      `/home/brett/projects/keycloak/` was mined for the compose/Postgres
      SHAPE only; `deploy/compose/keycloak.compose.template.yaml` carries
      every credential-shaped field as an environment interpolation and
      `deploy/compose/README.md` tabulates the five things that did NOT come
      across (three inline passwords, the realm export, the local image build)
      and why. The reference's realm export was never opened.

## 3. Evidence (the creation record)

- [x] 3.1 Record the repository **URL and remote** (`git@github.com:opensoft/Keycloak-Install.git`)
      and the exact seed commit on `main`.
      **DONE 2026-08-21** —
      [evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md)
      §3.1: URL, remote, repository id, created stamp, default branch, seed
      commit `1aa184e891d4ba6e641a31260d3f64d2b335f175`, author/date, and the
      19-file/1222-line seeded tree.
- [x] 3.2 DONE 2026-08-21 — read-backs recorded in the creation record and its addendum: visibility private, default branch main, both secret names present, ruleset id 21177147 active with pull_request count 1 (source: Repository). Settings read-back, not assertion: visibility `private`,
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
      end by opening the seed PR through `session-open-pr` and confirming
      the author is `openxfactory[bot]`.
      **DONE 2026-08-21, after Brett's org-owner act (1.3).**
      `opensoft/Keycloak-Install` is present on installation `145372182` for
      App `4253636` — read back via `GET
      user/installations/145372182/repositories`, 19 repositories total. Both
      App secrets remain read back by name only, values never read
      (`OPENXFACTORY_APP_ID`, `OPENXFACTORY_APP_PRIVATE_KEY`). The
      **optional** end-to-end `openxfactory[bot]` authorship proof is still
      **not claimed**: the seed had already landed by direct push, so there
      is no PR left to open for it, and manufacturing one solely to exercise
      the route would be theatre. The first real PR into this repository will
      be the proof; the CI-wiring follow-up (4.5) is its natural occasion.
      Recorded in
      [evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md)
      *"Addendum — App installation read-back"*.
- [x] 3.4 **Boundary validator green on the seeded tree**: `validate-boundary.py`
      exits 0 over the whole repository, AND its self-test passes — every
      `positive/` case accepted and every `negative/` case rejected with the
      expected class. A validator that is green only because it finds
      nothing is not evidence; the negative corpus is what makes 3.4 mean
      something.
      **DONE 2026-08-21** —
      [evidence/creation-record-2026-08-21.md](evidence/creation-record-2026-08-21.md)
      §3.4, verbatim. Whole-repository scan exit **0** (`BOUNDARY CLEAN — 9
      file(s) scanned`); `--self-test` exit **0** (4 positive accepted, 6
      negative rejected each as the class it names, all 6 classes exercised);
      and a RED proof — the same scanner over the negative corpus as a tree,
      exit **1**, 8 findings over 6 files.
- [ ] 3.5 **Delta ordering check** (design D-delta): confirm
      `add-identity-brokering` has archived — i.e. the requirement
      *"Keycloak install repository boundary"* is present in
      `openspec/specs/repo-boundary-governance/spec.md` — BEFORE archiving
      this change. Strict validation does not catch this; verify by hand.
      **NOT SATISFIED YET, and correctly so.** Checked by hand:
      `openspec/specs/repo-boundary-governance/spec.md` carries nine
      requirements and *"Keycloak install repository boundary"* is **absent**
      — `add-identity-brokering` has not archived. This change's MODIFIED
      delta has nothing to replace yet, so it must not archive before its
      parent. Strict validation does not catch this.
- [x] 3.6 **Creation-date correction**: if creation landed after 2026-08-21,
      correct `created 2026-08-21` in the spec delta to the actual creation
      date before archive, so the promoted past-tense sentence is true.
      **DONE 2026-08-21 — no correction needed, reasoning recorded.** API
      `created_at` is `2026-08-22T00:33:42Z`, which in the timezone every
      other record in this family uses (`-04:00`, visible in the org rulesets'
      own stamps) is **2026-08-21 20:33:42**. The delta's `created 2026-08-21`
      is true as written. Flagged because the two readings differ by a
      calendar day: re-check at archive by the LOCAL date.
- [x] 3.7 `OPENSPEC_TELEMETRY=0 openspec validate implement-keycloak-install-repo
      --strict` and `--all --strict` green at archive as well as at
      authoring. This change declares a code surface, so it archives only on
      merged realization with green evidence (`release-realization`), which
      here means the repository created, seeded, and its boundary validator
      green.
      **DONE 2026-08-21 (authoring + seed bar)** — `openspec validate
      implement-keycloak-install-repo --strict` → *is valid*, exit 0;
      `openspec validate --all --strict` → *Totals: 65 passed, 0 failed (65
      items)*, exit 0, item count unchanged. The archive-time run is not
      claimed: 3.5's gate is not satisfied.

## 4. Named follow-ups — NOT this change

Each is a separate reviewed change. None is authorized by this ratification.

- [ ] 4.1 **Aggregation admission** — pin `installs/keycloak-install` in the
      top-level xFactory aggregation, recording path, remote, visibility,
      exact validated commit, checkout, compatibility, update, and rollback.
      The ratified requirement is explicit: repository creation SHALL NOT be
      treated as aggregation admission, and THIS change MUST NOT be accepted
      as that record.
      **EXECUTED ELSEWHERE 2026-08-21 by
      [`admit-install-repos-to-aggregation`](../admit-install-repos-to-aggregation/proposal.md)**
      (ratified the same day: "do the aggregation admission change"). That
      change carries the eight-field admission record for
      `installs/keycloak-install` at the exact validated commit
      `1aa184e891d4ba6e641a31260d3f64d2b335f175`, and the `.gitmodules` +
      gitlink + README act lands by reviewed PR on `opensoft/xFactory`.
      **Deliberately left unticked**: this box is a follow-up that runs
      elsewhere, and the ratified requirement forbids THIS change from being
      accepted as the admission record — a tick here would claim exactly
      that.
- [ ] 4.2 **Broker deployment** — the actual topology (manifests, ingress and
      routing, datastore, backup / restore / upgrade / verification / DR) and
      the first GENERATED `config/clients/opensoft/runtime-manifest.yaml`.
      Its credentials — datastore, admin bootstrap, service-client — are
      `credential-contracts` records with declared custody, referenced by
      the deployment and never committed here.
- [ ] 4.3 **Dashboard oauth2-proxy swap** — oauth2-proxy or nginx
      external-auth in front of the workbench route, pointed at the broker;
      the shared htpasswd secret RETIRES in the same change, and the surface
      records an `authenticated_persona` adoption. Parent tasks 4.3.
- [ ] 4.4 **OpsxFactory `keycloak-administration`** — the governed
      administration workflow, with the service-subject kind registered in
      lockstep (`customer-kinds` + Hermes template + `stack.yaml`, grant
      ceilings in `credentials/requirements.yaml`). Developed in
      `OpsxFactory:staging:identity-pki-administration`. The ratified
      requirement forbids this workflow from living in the install
      repository. Parent tasks 4.1.
- [ ] 4.5 **CI wiring for the boundary validator** — the workflow that runs
      `validate-boundary.py` on every push and PR, plus adding it as a
      required status check on the `main` ruleset. Seeded here (2.6), gated
      there.
- [ ] 4.6 **Disposition of the stale public fork `opensoft/keycloak`**
      (upstream fork, public, last touched 2025-10): archive it or repurpose
      it, decided deliberately. Named so it is not lost; untouched by this
      change.
- [ ] 4.7 **openxFactory bookkeeping: the `contract-v1.37` release digest
      inventory is missing both new families.**
      `contracts/releases/contract-v1.37.digests.yaml` carries the same 190
      entries as `contract-v1.37`'s predecessor and none under
      `contracts/identity-brokering/` or `contracts/trust-anchor/`, so the
      inventory cannot be used to verify a pin against either family (task
      2.4 reads `contracts/manifest.yaml` instead). Found while deciding the
      pin's digest source; it is a defect in the released bundle's records,
      belongs to openxFactory, and this change deliberately does not edit a
      released bundle to seed a repository.
- [ ] 4.8 **`add-trust-anchor` tasks 8.1 bookkeeping** — once BOTH install
      repositories exist, one change refreshes the `repo-boundary-governance`
      *"Install repository scope"* requirement so the admitted install repos
      are enumerated in one place, as a MODIFIED delta restating all its
      scenarios, run when nothing else is replacing that requirement.
      Explicitly NOT done here (design D-delta).
      **EXECUTED ELSEWHERE 2026-08-21 by
      [`admit-install-repos-to-aggregation`](../admit-install-repos-to-aggregation/specs/repo-boundary-governance/spec.md)** —
      one MODIFIED delta, both scenarios restated verbatim, enumeration
      extended with both admitted repositories; `add-trust-anchor` tasks 8.1
      is ticked there. Left unticked here for the same reason as 4.1: it is
      another change's act.
