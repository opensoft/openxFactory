# Creation record — `opensoft/Keycloak-Install`

Tasks §3 evidence for `implement-keycloak-install-repo`. Read back off the
created repository and the seeded tree, not asserted.

Recorded 2026-08-21 (America/New_York). Two items are **PENDING** and are
named as such below; their tasks stay unticked.

## 3.1 Repository, remote, and seed commit

| Field | Value |
|---|---|
| URL | <https://github.com/opensoft/Keycloak-Install> |
| Remote | `git@github.com:opensoft/Keycloak-Install.git` |
| Repository id | `1342329131` |
| Created (API `created_at`) | `2026-08-22T00:33:42Z` = **2026-08-21 20:33:42 -04:00** |
| Default branch | `main` |
| Seed commit on `main` | `1aa184e891d4ba6e641a31260d3f64d2b335f175` |
| Seed commit subject | `Seed Keycloak-Install: boundary, contract-v1.37 pin, governance plumbing (implement-keycloak-install-repo)` |
| Seed commit author / date | `brettheap <brett.heap@users.noreply.github.com>` / `Fri Aug 21 20:53:13 2026 -0400` |
| Description (API) | `Opensoft-level Keycloak broker install: deployment topology + per-client runtime manifests. Governed by openxFactory repo-boundary-governance (Keycloak install repository boundary); created by implement-keycloak-install-repo.` |

**How the seed arrived, stated plainly.** Tasks 2.1 says "on `main` via the
1.5 authorship route". The seed landed as a **direct push to `main`**, not
through `session-open-pr`, because the route is not yet operable: adding the
repository to the `openxfactory` App installation failed (3.3 below), and
without that installation the workflow's own preflight cannot mint an App
token. The route itself is mirrored and committed (1.5); it is untested end
to end, and 3.3's optional proof is therefore not claimed. Nothing else
about the seed changes: the repository was empty, so the push created `main`
at the seed commit.

### The seeded tree (19 files)

```
.github/workflows/session-open-pr.yml                                                       105 lines
README.md                                                                                   149
config/clients/opensoft/README.md                                                            50
config/contracts/identity-brokering/manifest.yaml                                            55
deploy/compose/README.md                                                                     40
deploy/compose/keycloak.compose.template.yaml                                                70
deploy/kubernetes/README.md                                                                  36
docs/README.md                                                                               28
scripts/boundary-selftest/negative/assigned-secret--compose-inline-datastore-password.yml    13
scripts/boundary-selftest/negative/bearer-token--issued-access-token.yaml                     4
scripts/boundary-selftest/negative/encoded-key-material--base64-wrapped-pem.yaml             10
scripts/boundary-selftest/negative/key-material--broker-signing-private-key.pem               4
scripts/boundary-selftest/negative/secret-property--realm-export-with-client-secret.json     11
scripts/boundary-selftest/negative/stored-verifier--dashboard-htpasswd.txt                    3
scripts/boundary-selftest/positive/actions-expression-references.yaml                        16
scripts/boundary-selftest/positive/compose-credential-references.yaml                        16
scripts/boundary-selftest/positive/credential-contract-references.yaml                       11
scripts/boundary-selftest/positive/kubernetes-secret-references.yaml                         19
scripts/validate-boundary.py                                                                582
                                                                                           -----
                                                                                           1222
```

## 3.2 Settings read-back

`gh api repos/opensoft/Keycloak-Install`:

```json
{"name":"Keycloak-Install","id":1342329131,"private":true,"visibility":"private",
 "default_branch":"main","created_at":"2026-08-22T00:33:42Z","has_pages":false}
```

- visibility **`private`** — confirmed by both `private: true` and
  `visibility: "private"`.
- default branch **`main`** — confirmed.

`gh api repos/opensoft/Keycloak-Install/rulesets` returns **two
ORGANIZATION-level rulesets inherited by this repository, and no
repository-level ruleset**:

| id | name | source | rules |
|---|---|---|---|
| 8981805 | Copilot Auto-Review All PRs | org `opensoft` | `non_fast_forward`, `copilot_code_review` |
| 18834180 | Require Code Owner Review | org `opensoft` | `deletion`, `non_fast_forward`, `pull_request` (`require_code_owner_review: true`, `required_approving_review_count: 0`, `dismiss_stale_reviews_on_push: true`) on `~DEFAULT_BRANCH` |

**The `main` ruleset requiring 1 approving review (task 1.2) does not exist
yet** — it is the orchestrator's post-seed act, and the inherited org
ruleset is not it: its `required_approving_review_count` is `0`. Task 1.2
stays unticked. Recording the inherited pair matters for a second reason:
whoever adds the repository-level ruleset is adding a THIRD ruleset over the
same ref, and rulesets combine rather than override.

Other GitHub-side surface, read back for task 1.6:

| Surface | Read-back | Expected |
|---|---|---|
| Environments | `total_count: 0` | none |
| Deploy keys | `0` | none |
| Pages | `has_pages: false` | none |
| Actions secrets | exactly `OPENXFACTORY_APP_ID`, `OPENXFACTORY_APP_PRIVATE_KEY` | those two only |

No cloud-credential secret, no package, no environment. Task 1.6 confirmed.

## 3.3 App installation read-back — **PENDING**

- **Both App secrets present**, names only, values never read:
  `gh api repos/opensoft/Keycloak-Install/actions/secrets` →
  `OPENXFACTORY_APP_ID`, `OPENXFACTORY_APP_PRIVATE_KEY`. Task 1.4 done.
- **The repository is NOT yet on installation `145372182` for App
  `4253636`.** The add failed with HTTP 403: *"only an Organization Owner can
  modify this app"*. This needs **Brett** (organization owner) to add both
  new repositories to the `openxfactory` App installation. Task 1.3 stays
  unticked.

Consequence, so it is not discovered later: until 1.3 lands,
`session-open-pr` fails closed at its preflight/token step, the seed could
not be authored by `openxfactory[bot]` (see 3.1), and the optional
end-to-end proof in this task is not claimed.

## 3.4 Boundary validator — green on the seeded tree, and red on the corpus

Runs from the repository root at the seed commit. Python 3.12.3, PyYAML
6.0.1; standard library plus the YAML parser, no other dependency.

**Green over the whole repository** — `python3 scripts/validate-boundary.py`,
exit **0**:

```
BOUNDARY CLEAN — 9 file(s) scanned under <repo> (self-test corpus excluded; run --self-test for that)
```

The scan excludes only `.git/` and `scripts/boundary-selftest/` — whose
negative half exists precisely to fail. **The validator scans itself**: no
source-file exemption. That is not free, and it is evidence in its own
right: the first green run failed on `scripts/validate-boundary.py:88`,
`ASSIGNED_SECRET`, because the line declaring the class constant was itself
a credential-shaped name with a literal on the right of an `=`. The fix was
to declare the class names once in a tuple and unpack them, not to exempt
the file.

**Self-test** — `python3 scripts/validate-boundary.py --self-test`, exit
**0**:

```
-- positive: must be accepted
   ok   actions-expression-references.yaml
   ok   compose-credential-references.yaml
   ok   credential-contract-references.yaml
   ok   kubernetes-secret-references.yaml
-- negative: must be rejected, each with the class it names
   ok   assigned-secret--compose-inline-datastore-password.yml -> ASSIGNED_SECRET
   ok   bearer-token--issued-access-token.yaml -> BEARER_TOKEN
   ok   encoded-key-material--base64-wrapped-pem.yaml -> ENCODED_KEY_MATERIAL
   ok   key-material--broker-signing-private-key.pem -> KEY_MATERIAL
   ok   secret-property--realm-export-with-client-secret.json -> SECRET_PROPERTY
   ok   stored-verifier--dashboard-htpasswd.txt -> STORED_VERIFIER
-- coverage: every class needs a negative case
   ok   KEY_MATERIAL
   ok   ENCODED_KEY_MATERIAL
   ok   ASSIGNED_SECRET
   ok   STORED_VERIFIER
   ok   BEARER_TOKEN
   ok   SECRET_PROPERTY

SELF-TEST PASSED — 4 positive, 6 negative, 6 classes exercised
```

Each negative case names the class it exercises in its filename, and the
self-test FAILS a class that has no negative case — a class with no case is a
claim, not a check.

**Red on planted material** — the same scanner pointed at the negative
corpus as a tree, `python3 scripts/validate-boundary.py
scripts/boundary-selftest/negative`, exit **1**:

```
ASSIGNED_SECRET assigned-secret--compose-inline-datastore-password.yml:9: a credential-shaped name with a literal assigned value; route it to a credential-contracts record and reference the record
ASSIGNED_SECRET assigned-secret--compose-inline-datastore-password.yml:13: a credential-shaped name with a literal assigned value; route it to a credential-contracts record and reference the record
SECRET_PROPERTY assigned-secret--compose-inline-datastore-password.yml#services.broker-db.environment.POSTGRES_PASSWORD: a credential-shaped property holding a literal value; the value belongs in a credential-contracts record with declared custody, and this document should carry a reference to it
BEARER_TOKEN bearer-token--issued-access-token.yaml:4: a bearer-token-shaped value
ENCODED_KEY_MATERIAL encoded-key-material--base64-wrapped-pem.yaml: an armored private key block, reached by reversing base64; armor is a convention, structure is the thing
KEY_MATERIAL key-material--broker-signing-private-key.pem:1: an armored private key block
SECRET_PROPERTY secret-property--realm-export-with-client-secret.json#clients[0].secret: a credential-shaped property holding a literal value; the value belongs in a credential-contracts record with declared custody, and this document should carry a reference to it
STORED_VERIFIER stored-verifier--dashboard-htpasswd.txt:3: a stored password verifier

BOUNDARY VIOLATED — 8 finding(s) over 6 file(s) under <repo>/scripts/boundary-selftest/negative
```

Two of those are worth naming. The **realm export** case is caught by the
STRUCTURAL pass and not the textual one: a quoted JSON key (`"secret": "…"`)
defeats a text-level assigned-value scan, which is exactly why property
NAMES are walked. The **base64-wrapped key** is caught with no armor visible
in the file — the encoding is reversed two layers deep and the value classes
and DER private-key structure are re-run over the decoded bytes.

Every value in the negative corpus is synthetic. That corpus is the only
place in the repository where secret-*shaped* material legitimately lives.

## 3.5 Delta ordering check — **NOT SATISFIED YET** (correctly)

Checked by hand at
`openxFactory/openspec/specs/repo-boundary-governance/spec.md`. The promoted
requirements are: *Canonical workflow authority, Install repository scope,
Copy-first migration, Guarded pilot execution, Install repo scope links,
Neutral installer repository integration, Neutral avatar-client repository
boundary, Avatar-client release evidence, Deferred aggregation and
web-console integration.*

*"Keycloak install repository boundary"* is **absent** — `add-identity-brokering`
has not archived (it is still an active change). This change's `MODIFIED`
delta therefore has nothing to replace yet, so **this change must not archive
before its parent does**. Strict validation does not catch this, which is why
the check is by hand. Task 3.5 stays unticked until the parent archives.

## 3.6 Creation date — no correction needed, with the reasoning recorded

The API stamp is `2026-08-22T00:33:42Z`. In the timezone every other record
in this family uses (`-04:00`, visible in the org rulesets' own
`created_at`), that is **2026-08-21 20:33:42**, so the spec delta's
`created 2026-08-21` is true as written and no correction is made.

Recorded rather than silently accepted because the two readings differ by a
calendar day: anyone re-checking at archive should read the local date, not
the UTC one.

## 3.7 Strict validation

Run from the openxFactory repository root:

```
$ OPENSPEC_TELEMETRY=0 openspec validate implement-keycloak-install-repo --strict
Change 'implement-keycloak-install-repo' is valid
EXIT=0

$ OPENSPEC_TELEMETRY=0 openspec validate --all --strict
…
Totals: 65 passed, 0 failed (65 items)
EXIT=0
```

Green at authoring and green again after this seed's task/evidence edits,
with the item count unchanged at **65**. This is the authoring-and-seed bar;
3.7 also requires a green run at archive, which has not happened (see 3.5).

## What this evidence does NOT establish

- **Not aggregation admission.** The ratified requirement is explicit that
  repository creation SHALL NOT be treated as aggregation admission, and
  that this change MUST NOT be accepted as that record. Nothing here pins
  `installs/keycloak-install`.
- **Not a deployment.** No broker, no realm, no organization, no persona, no
  service client, no credential. The seed contains nothing that runs.
- **Not an enforced gate.** The boundary validator is committed and green;
  the CI workflow that runs it on every push and the required status check
  on the `main` ruleset are a named follow-up (tasks 4.5). Landing the script
  without the gate is honest about what is enforced today.

## Addendum — post-seed ruleset read-back (2026-08-21)

Repo-level ruleset "main review gate" created after the seed push: id 21177147,
target branch `~DEFAULT_BRANCH`, enforcement `active`, one `pull_request`
rule with `required_approving_review_count: 1` (dismiss-stale false,
code-owner false, last-push false, thread-resolution false; merge methods
merge/squash/rebase). Read back via `GET repos/opensoft/Keycloak-Install/rules/branches/main`:
two pull_request rules apply — the org-level rule (count 0) and this
repository rule (count 1, source: Repository). Rulesets combine, so the
effective gate on `main` is one required approving review. The App
installation read-back (tasks 3.3) remains pending on the org-owner act.
