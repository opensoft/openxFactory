# Creation record — `opensoft/OpenXPKI-Install`

Tasks §3 evidence for `implement-openxpki-install-repo`. Read back off the
created repository and the seeded tree, not asserted.

Recorded 2026-08-21 (America/New_York). Two items are **PENDING** and are
named as such below; their tasks stay unticked.

## 3.1 Repository, remote, and seed commit

| Field | Value |
|---|---|
| URL | <https://github.com/opensoft/OpenXPKI-Install> |
| Remote | `git@github.com:opensoft/OpenXPKI-Install.git` |
| Repository id | `1342329163` |
| Created (API `created_at`) | `2026-08-22T00:33:46Z` = **2026-08-21 20:33:46 -04:00** |
| Default branch | `main` |
| Seed commit on `main` | `05f440444d9091206778e838454ed9b5bb7bff60` |
| Seed commit subject | `Seed OpenXPKI-Install: boundary, contract-v1.37 pin, governance plumbing (implement-openxpki-install-repo)` |
| Seed commit author / date | `brettheap <brett.heap@users.noreply.github.com>` / `Fri Aug 21 20:53:17 2026 -0400` |
| Description (API) | `Opensoft-level OpenXPKI install: server/client/web deployment topology + per-client runtime manifests, consuming only the Opensoft-Tenant digest-pinned image. Governed by openxFactory repo-boundary-governance (OpenXPKI install repository boundary); created by implement-openxpki-install-repo.` |

**How the seed arrived, stated plainly.** Tasks 2.1 says "on `main` via the
1.5 authorship route". The seed landed as a **direct push to `main`**, not
through `session-open-pr`, because the route is not yet operable: adding the
repository to the `openxfactory` App installation failed (3.3 below), and
without that installation the workflow's own preflight cannot mint an App
token. The route itself is mirrored and committed (1.5); it is untested end
to end, and 3.3's optional proof is therefore not claimed.

### The seeded tree (24 files)

```
.github/workflows/session-open-pr.yml                                                         105 lines
README.md                                                                                     151
config/clients/opensoft/README.md                                                              52
config/contracts/trust-anchor/manifest.yaml                                                    59
deploy/compose/README.md                                                                       23
deploy/kubernetes/README.md                                                                    89
docs/README.md                                                                                 35
scripts/boundary-selftest/negative/assigned-secret--inline-datastore-password.yaml              6
scripts/boundary-selftest/negative/bearer-token--issued-access-token.yaml                       4
scripts/boundary-selftest/negative/encoded-key-material--base64-wrapped-pem.yaml                9
scripts/boundary-selftest/negative/encoded-key-material--unarmored-pkcs8-der-as-base64.yaml     7
scripts/boundary-selftest/negative/encoded-key-material--unarmored-pkcs8-der-as-hex.yaml        5
scripts/boundary-selftest/negative/image-build--build-and-push-workflow.yaml                   13
scripts/boundary-selftest/negative/image-build--dockerfile                                      5
scripts/boundary-selftest/negative/key-material--ca-issuer-private-key.pem                      4
scripts/boundary-selftest/negative/mutable-image-tag--floating-latest.yaml                     11
scripts/boundary-selftest/negative/mutable-image-tag--pinned-semver.yaml                       13
scripts/boundary-selftest/negative/secret-property--ca-config-with-issuance-credential.json     8
scripts/boundary-selftest/negative/stored-verifier--web-htpasswd.txt                            3
scripts/boundary-selftest/positive/contract-pin-shape.yaml                                     11
scripts/boundary-selftest/positive/credential-contract-references.yaml                         10
scripts/boundary-selftest/positive/digest-pinned-images.yaml                                   16
scripts/boundary-selftest/positive/kubernetes-secret-references.yaml                           21
scripts/validate-boundary.py                                                                  747
                                                                                             -----
                                                                                             1407
```

`deploy/kubernetes/` carries **no manifests** (tasks 2.6): its README is the
topology HOME, the migration path (`add-openxpki-qa-image-pipeline` tasks
3.4, transitional origin `opensoft/Opensoft-Tenant`), the
digest-consumption rule, the custody rule, and an explicit statement that
**no digest value is present yet and why** — the producing change is an
uncommitted working-tree draft, so its digest is not durably recorded
anywhere citable, and a digest read out of another session's uncommitted tree
is not a pin.

## 3.2 Settings read-back

`gh api repos/opensoft/OpenXPKI-Install`:

```json
{"name":"OpenXPKI-Install","id":1342329163,"private":true,"visibility":"private",
 "default_branch":"main","created_at":"2026-08-22T00:33:46Z","has_pages":false}
```

- visibility **`private`** — confirmed by both `private: true` and
  `visibility: "private"`.
- default branch **`main`** — confirmed.

`gh api repos/opensoft/OpenXPKI-Install/rulesets` returns **two
ORGANIZATION-level rulesets inherited by this repository, and no
repository-level ruleset**:

| id | name | source | rules |
|---|---|---|---|
| 8981805 | Copilot Auto-Review All PRs | org `opensoft` | `non_fast_forward`, `copilot_code_review` |
| 18834180 | Require Code Owner Review | org `opensoft` | `deletion`, `non_fast_forward`, `pull_request` (`require_code_owner_review: true`, `required_approving_review_count: 0`, `dismiss_stale_reviews_on_push: true`) on `~DEFAULT_BRANCH` |

**The `main` ruleset requiring 1 approving review (task 1.2) does not exist
yet** — it is the orchestrator's post-seed act, and the inherited org
ruleset is not it: its `required_approving_review_count` is `0`. Task 1.2
stays unticked.

Other GitHub-side surface, read back for task 1.6 — which for this
repository is the one that matters most, because registry wiring would be
image custody arriving through the side door:

| Surface | Read-back | Expected |
|---|---|---|
| Environments | `total_count: 0` | none |
| Deploy keys | `0` | none |
| Pages | `has_pages: false` | none |
| Actions secrets | exactly `OPENXFACTORY_APP_ID`, `OPENXFACTORY_APP_PRIVATE_KEY` | those two only |

**No ACR or cloud credential in Actions secrets, and no container-registry
wiring of any kind.** Task 1.6 confirmed.

## 3.3 App installation read-back — **PENDING**

- **Both App secrets present**, names only, values never read:
  `gh api repos/opensoft/OpenXPKI-Install/actions/secrets` →
  `OPENXFACTORY_APP_ID`, `OPENXFACTORY_APP_PRIVATE_KEY`. Task 1.4 done.
- **The repository is NOT yet on installation `145372182` for App
  `4253636`.** The add failed with HTTP 403: *"only an Organization Owner can
  modify this app"*. This needs **Brett** (organization owner) to add both
  new repositories to the `openxfactory` App installation. Task 1.3 stays
  unticked.

Consequence: until 1.3 lands, `session-open-pr` fails closed, the seed could
not be authored by `openxfactory[bot]` (see 3.1), and the optional
end-to-end proof in this task is not claimed.

## 3.4 Boundary validator — green on the seeded tree, and red on the corpus

Runs from the repository root at the seed commit. Python 3.12.3, PyYAML
6.0.1; standard library plus the YAML parser, no other dependency.

**Green over the whole repository** — `python3 scripts/validate-boundary.py`,
exit **0**:

```
BOUNDARY CLEAN — 8 file(s) scanned under <repo> (self-test corpus excluded; run --self-test for that)
```

The scan excludes only `.git/` and `scripts/boundary-selftest/`. **The
validator scans itself**: no source-file exemption, which is why the
build-tool TOKENS are assembled from string fragments — written verbatim,
each would make the validator its own IMAGE_BUILD finding, and a boundary
check that has to exempt itself has a hole in it. (The sibling
Keycloak-Install validator, from which this one is derived, produced exactly
that self-finding on its first run for the ASSIGNED_SECRET class; the fix was
a declaration form, not an exemption.)

**Self-test** — `python3 scripts/validate-boundary.py --self-test`, exit
**0**:

```
-- positive: must be accepted
   ok   contract-pin-shape.yaml
   ok   credential-contract-references.yaml
   ok   digest-pinned-images.yaml
   ok   kubernetes-secret-references.yaml
-- negative: must be rejected, each with the class it names
   ok   assigned-secret--inline-datastore-password.yaml -> ASSIGNED_SECRET
   ok   bearer-token--issued-access-token.yaml -> BEARER_TOKEN
   ok   encoded-key-material--base64-wrapped-pem.yaml -> ENCODED_KEY_MATERIAL
   ok   encoded-key-material--unarmored-pkcs8-der-as-base64.yaml -> ENCODED_KEY_MATERIAL
   ok   encoded-key-material--unarmored-pkcs8-der-as-hex.yaml -> ENCODED_KEY_MATERIAL
   ok   image-build--build-and-push-workflow.yaml -> IMAGE_BUILD
   ok   image-build--dockerfile -> IMAGE_BUILD
   ok   key-material--ca-issuer-private-key.pem -> KEY_MATERIAL
   ok   mutable-image-tag--floating-latest.yaml -> MUTABLE_IMAGE_TAG
   ok   mutable-image-tag--pinned-semver.yaml -> MUTABLE_IMAGE_TAG
   ok   secret-property--ca-config-with-issuance-credential.json -> SECRET_PROPERTY
   ok   stored-verifier--web-htpasswd.txt -> STORED_VERIFIER
-- coverage: every class needs a negative case
   ok   KEY_MATERIAL
   ok   ENCODED_KEY_MATERIAL
   ok   ASSIGNED_SECRET
   ok   STORED_VERIFIER
   ok   BEARER_TOKEN
   ok   SECRET_PROPERTY
   ok   IMAGE_BUILD
   ok   MUTABLE_IMAGE_TAG

SELF-TEST PASSED — 4 positive, 12 negative, 8 classes exercised
```

Both boundary-specific classes are exercised, as tasks 3.4 requires.

**Red on planted material** — the same scanner pointed at the negative corpus
as a tree, `python3 scripts/validate-boundary.py
scripts/boundary-selftest/negative`, exit **1**:

```
ASSIGNED_SECRET assigned-secret--inline-datastore-password.yaml:6: a credential-shaped name with a literal assigned value; route it to a credential-contracts record and reference the record
SECRET_PROPERTY assigned-secret--inline-datastore-password.yaml#password: a credential-shaped property holding a literal value; the value belongs in a credential-contracts record with declared custody, and this document should carry a reference to it
BEARER_TOKEN bearer-token--issued-access-token.yaml:4: a bearer-token-shaped value
ENCODED_KEY_MATERIAL encoded-key-material--base64-wrapped-pem.yaml: an armored private key block, reached by reversing base64; armor is a convention, structure is the thing
ENCODED_KEY_MATERIAL encoded-key-material--unarmored-pkcs8-der-as-base64.yaml: a PKCS#8 PrivateKeyInfo for rsaEncryption, reached by reversing base64; armor is a convention, structure is the thing
ENCODED_KEY_MATERIAL encoded-key-material--unarmored-pkcs8-der-as-hex.yaml: a PKCS#8 PrivateKeyInfo for rsaEncryption, reached by reversing hex; armor is a convention, structure is the thing
IMAGE_BUILD image-build--build-and-push-workflow.yaml:11: a pipeline step that produces a container image; image custody — build sources, release / package / configuration / base-image pins, and the test harness — remains in opensoft/Opensoft-Tenant
IMAGE_BUILD image-build--dockerfile:4: is a container build source by content (an image base plus build instructions), whatever the file is called
KEY_MATERIAL key-material--ca-issuer-private-key.pem:1: an armored private key block
MUTABLE_IMAGE_TAG mutable-image-tag--floating-latest.yaml#spec.template.spec.containers[0].image: an image reference that is not <registry>/<repository>@sha256:<64 hex>; consume the immutable digest opensoft/Opensoft-Tenant pinned, never a tag
MUTABLE_IMAGE_TAG mutable-image-tag--pinned-semver.yaml#spec.template.spec.containers[0].image: an image reference that is not <registry>/<repository>@sha256:<64 hex>; consume the immutable digest opensoft/Opensoft-Tenant pinned, never a tag
SECRET_PROPERTY secret-property--ca-config-with-issuance-credential.json#issuance.api_key: a credential-shaped property holding a literal value; the value belongs in a credential-contracts record with declared custody, and this document should carry a reference to it
STORED_VERIFIER stored-verifier--web-htpasswd.txt:3: a stored password verifier

BOUNDARY VIOLATED — 13 finding(s) over 12 file(s) under <repo>/scripts/boundary-selftest/negative
```

Four of those are worth naming.

- **The unarmored PKCS#8 DER blob is caught with no armor label anywhere in
  the file, as base64 AND again as hex** — the same bytes, two encodings, one
  rule. This is the adversarial-review lesson from
  `validate-trust-anchor.py`: armor is a convention, DER STRUCTURE is the
  thing, and a second encoding of the same bytes must not be a second way
  past the scan. (The base64 fixture even carries the label *"qa only,
  honestly"*, because that was one of the five evasions that walked keys past
  an armor-only scan.)
- **The build source is caught by CONTENT, under a filename that is not
  `Dockerfile`** (`image-build--dockerfile`) — renaming the file is not a way
  past the boundary.
- **The pinned semver tag fails the SAME rule as `:latest`.** The rule is a
  positive shape test, not a list of bad tags, because the requirement's
  second scenario is about the decision being reproduced here — not about
  which tag was chosen.
- **The CA configuration export's issuance credential** is caught by the
  structural pass, not the textual one: a quoted JSON key defeats a
  text-level assigned-value scan.

Every value in the negative corpus is synthetic — a real CA key there would
be the exact breach the validator exists to prevent.

## 3.5 Delta ordering check — **NOT SATISFIED YET** (correctly)

Checked by hand at
`openxFactory/openspec/specs/repo-boundary-governance/spec.md`. The promoted
requirements are: *Canonical workflow authority, Install repository scope,
Copy-first migration, Guarded pilot execution, Install repo scope links,
Neutral installer repository integration, Neutral avatar-client repository
boundary, Avatar-client release evidence, Deferred aggregation and
web-console integration.*

*"OpenXPKI install repository boundary"* is **absent** — `add-trust-anchor`
has not archived (it is still an active change, and it declares a code
surface of its own, so it archives on its contract realization rather than on
this change's). This change's `MODIFIED` delta therefore has nothing to
replace yet, so **this change must not archive before its parent does**.
Strict validation does not catch this, which is why the check is by hand.
Task 3.5 stays unticked until the parent archives.

## 3.6 Creation date — no correction needed, with the reasoning recorded

The API stamp is `2026-08-22T00:33:46Z`. In the timezone every other record
in this family uses (`-04:00`, visible in the org rulesets' own
`created_at`), that is **2026-08-21 20:33:46**, so the spec delta's
`created 2026-08-21` is true as written and no correction is made.

Recorded rather than silently accepted because the two readings differ by a
calendar day: anyone re-checking at archive should read the local date, not
the UTC one.

## 3.7 Strict validation

Run from the openxFactory repository root:

```
$ OPENSPEC_TELEMETRY=0 openspec validate implement-openxpki-install-repo --strict
Change 'implement-openxpki-install-repo' is valid
EXIT=0

$ OPENSPEC_TELEMETRY=0 openspec validate --all --strict
…
Totals: 65 passed, 0 failed (65 items)
EXIT=0
```

Green at authoring and green again after this seed's task/evidence edits,
with the item count unchanged at **65**. This is the authoring-and-seed bar;
3.7 also requires a green run at archive, which has not happened (see 3.5).

## The contract pin, verified rather than transcribed

`config/contracts/trust-anchor/manifest.yaml` pins `contract-v1.37`, commit
`c1ffa0fdd358f8db7a86dff4c7c40583e581adff` (what the annotated tag resolves
to on published `origin/main`), with per-file sha256 read from the
`trust-anchor-*` rows of `contracts/manifest.yaml` for the eight schemas plus
`trust-anchor-chain-custody.registry.yaml`.

All nine digests were **re-derived from the tag's own blobs**
(`git cat-file blob contract-v1.37:<path> | sha256sum`) and match the index
byte for byte. The release inventory
`contracts/releases/contract-v1.37.digests.yaml` was re-checked and still
carries 190 entries with **none** under `contracts/trust-anchor/` — its only
`trust-anchor` matches are the unrelated
`contracts/hermes-runtime/installation-trust-anchor*.schema.yaml` pair — so
tasks 2.4's refusal to use it, and the openxFactory bookkeeping follow-up in
tasks 4.7, both stand.

## What this evidence does NOT establish

- **Not aggregation admission.** The ratified requirement is explicit that
  repository creation MUST NOT be treated as aggregation admission. Nothing
  here pins `installs/openxpki-install`.
- **Not the topology migration.** Tasks 4.2 is gated, not merely deferred:
  `add-openxpki-qa-image-pipeline` is an uncommitted, unratified draft, so no
  ACR digest is recorded here. Creating this repository is what unblocks that
  migration — a migration task naming a repository that does not exist cannot
  close.
- **Not a deployment, and no custody.** No CA key, no issuance credential, no
  datastore credential, no configuration export, no Dockerfile, no build
  workflow, no image tag, no ACR credential. There is no QA exemption.
- **Not an enforced gate.** The boundary validator is committed and green;
  the CI workflow that runs it on every push and the required status check on
  the `main` ruleset are a named follow-up (tasks 4.5).

## Addendum — post-seed ruleset read-back (2026-08-21)

Repo-level ruleset "main review gate" created after the seed push: id 21177148,
target branch `~DEFAULT_BRANCH`, enforcement `active`, one `pull_request`
rule with `required_approving_review_count: 1` (dismiss-stale false,
code-owner false, last-push false, thread-resolution false; merge methods
merge/squash/rebase). Read back via `GET repos/opensoft/OpenXPKI-Install/rules/branches/main`:
two pull_request rules apply — the org-level rule (count 0) and this
repository rule (count 1, source: Repository). Rulesets combine, so the
effective gate on `main` is one required approving review. The App
installation read-back (tasks 3.3) remains pending on the org-owner act.
