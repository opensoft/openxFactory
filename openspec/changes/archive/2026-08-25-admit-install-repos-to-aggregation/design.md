# Design: admit-install-repos-to-aggregation

This document **is** the admission record. Both ratified boundary requirements
demand that a separate reviewed change record, per repository, *path, remote,
visibility, exact validated commit, checkout, compatibility, update, and
rollback behavior* before the pin is treated as supported. §1 and §2 below
carry those eight fields under those eight labels, one section per repository.
§3 states the update and rollback discipline they share, §4 the deliberate
exclusions, §5 the decisions taken while authoring.

Every value in §1 and §2 is a **read-back**, taken 2026-08-21 from the GitHub
API or from the seeded tree, not an assertion. Where a value could not be
re-read with the token at hand, the source that did read it is named.

Non-normative, like every design document in this family: the authoritative
obligations are the two ratified boundary requirements and the promoted
*"Deferred aggregation and web-console integration"* / *"Neutral installer
repository integration"* requirements. This document records **compliance**
with them; it does not add requirement meaning, and the only spec delta this
change carries is the enumeration refresh (D-enumeration).

## 1. `opensoft/Keycloak-Install`

| Field | Value |
|---|---|
| **Path** | `installs/keycloak-install` |
| **Remote** | `git@github.com:opensoft/Keycloak-Install.git` |
| **Visibility** | `private` — read back `private=true visibility=private`, repository id `1342329131`, default branch `main` |
| **Exact validated commit** | `1aa184e891d4ba6e641a31260d3f64d2b335f175` |
| **Checkout** | SSH submodule in `opensoft/xFactory`, manually initialized like every other `installs/` submodule (`git submodule update --init --recursive`, or `--recurse-submodules` at clone). No `branch =` key: the gitlink is the authority, not a tracked branch. Recursive checkout is identical to plain checkout — the repository carries **no `.gitmodules`** (HTTP 404 on `repos/opensoft/Keycloak-Install/contents/.gitmodules?ref=main`), so there is no nested boundary to reproduce. Private visibility means a checkout needs an SSH key with `opensoft` access, the same condition every existing submodule already imposes. |
| **Compatibility** | The repository pins openxFactory `contract-v1.37` for the neutral `identity-brokering` family, recorded in `config/contracts/identity-brokering/manifest.yaml` as `contract_bundle_tag: contract-v1.37`, `commit: c1ffa0fdd358f8db7a86dff4c7c40583e581adff`, `revision_kind: commit`, `source_repository: opensoft/openxFactory`, plus per-file sha256 for all six schemas (`digest_source: contracts/manifest.yaml`). Read back from `main` this session. **The aggregation pin carries no contract coupling of its own**: `opensoft/xFactory` pins a commit, and that commit pins the contracts. |
| **Update** | The pin advances ONLY via a reviewed aggregation PR on the "Sync submodule pointers" discipline, with fast-forward direction verified against the submodule's `main` before the commit lands (stage the gitlink, verify the direction, commit, read the result back with `git ls-tree`). The submodule's `main` is never force-pushed, which is what makes the fast-forward check meaningful. A pin advance is a new reviewed change, not an extension of this one. |
| **Rollback** | Revert the aggregation pin commit — **the gitlink is the whole coupling**, so reverting it removes the pin (or restores the previous one) with nothing else to unwind. Withdrawing the boundary entirely means removing both the gitlink and the `.gitmodules` entry in a dedicated reviewed change, the discipline the promoted *"Neutral installer repository integration"* requirement already fixed for the installer. The repository's own install/verify/upgrade/backup/restore/disaster-recovery procedures live in its `docs/` per its boundary requirement, and are not duplicated here. |

**Validation state at the recorded commit.** The boundary validator is green
over the whole repository (exit 0, 9 files scanned) and red-proven over its
negative corpus (exit 1, 8 findings over 6 files), with its self-test passing
4 positive and 6 negative cases across all 6 detection classes. Recorded in
[`implement-keycloak-install-repo/evidence/creation-record-2026-08-21.md`](../implement-keycloak-install-repo/evidence/creation-record-2026-08-21.md)
§3.4. That is the evidence the ratified requirement wants a pin to rest on;
this change does not re-derive it, it cites it.

**Effective review gate on the pinned branch.** Repository ruleset "main
review gate", id `21177147`, enforcement `active`, one `pull_request` rule
with `required_approving_review_count: 1`, layered over the two inherited
organization rulesets (whose own count is 0). Read back at creation time and
recorded in the same evidence file's addendum.

## 2. `opensoft/OpenXPKI-Install`

| Field | Value |
|---|---|
| **Path** | `installs/openxpki-install` |
| **Remote** | `git@github.com:opensoft/OpenXPKI-Install.git` |
| **Visibility** | `private` — read back `private=true visibility=private`, repository id `1342329163`, default branch `main` |
| **Exact validated commit** | `05f440444d9091206778e838454ed9b5bb7bff60` |
| **Checkout** | SSH submodule in `opensoft/xFactory`, manually initialized like every other `installs/` submodule. No `branch =` key. This requirement names **recursive** checkout explicitly, and recursive checkout here is identical to plain checkout: the repository carries **no `.gitmodules`** (HTTP 404 on `repos/opensoft/OpenXPKI-Install/contents/.gitmodules?ref=main`), so there is no nested boundary to reproduce. Notably it does **not** vendor `opensoft/Opensoft-Tenant` as a submodule — image custody stays a digest reference, per its boundary requirement, so the custody split survives a recursive checkout instead of being flattened by one. Private visibility means a checkout needs an SSH key with `opensoft` access. |
| **Compatibility** | The repository pins openxFactory `contract-v1.37` for the neutral `trust-anchor` family, recorded in `config/contracts/trust-anchor/manifest.yaml` as `contract_bundle_tag: contract-v1.37`, `commit: c1ffa0fdd358f8db7a86dff4c7c40583e581adff`, `revision_kind: commit`, `source_repository: opensoft/openxFactory`, plus per-file sha256 (`digest_source: contracts/manifest.yaml`). Read back from `main` this session — the same contract commit as the Keycloak half, because both families shipped in the same bundle. **The aggregation pin carries no contract coupling of its own.** |
| **Update** | Identical discipline to §1: reviewed aggregation PR only, "Sync submodule pointers", fast-forward direction verified against the submodule's `main`, submodule `main` never force-pushed, read the landed gitlink back with `git ls-tree`. One additional gate specific to this repository: a pin advance that brings in QA deployment topology must carry the immutable ACR digest that topology consumes, because the topology migration is itself gated on `add-openxpki-qa-image-pipeline` ratifying — a digest read out of an uncommitted tree is not a pin. |
| **Rollback** | Revert the aggregation pin commit; the gitlink is the whole coupling. Full withdrawal removes gitlink and `.gitmodules` entry in a dedicated reviewed change. The repository's own install/verify/upgrade/backup/restore/disaster-recovery procedures live in its `docs/` per its boundary requirement. |

**Validation state at the recorded commit.** Boundary validator green over the
whole repository and red-proven over its negative corpus, self-test passing,
including the DER-structure and image-build-source classes this repository's
boundary adds. Recorded in
[`implement-openxpki-install-repo/evidence/creation-record-2026-08-21.md`](../implement-openxpki-install-repo/evidence/creation-record-2026-08-21.md)
§3.4.

**Effective review gate on the pinned branch.** Repository ruleset "main
review gate", id `21177148`, enforcement `active`, one `pull_request` rule
with `required_approving_review_count: 1`, layered over the two inherited
organization rulesets. Read back at creation time and recorded in the same
evidence file's addendum.

## 3. The shared update and rollback discipline

The two records above state the discipline per repository because the ratified
requirements ask for it per repository. It is one discipline, and it rests on
three facts about the aggregation:

1. **The aggregation is a pin-only workspace assembler.** It owns
   `.gitmodules`, gitlinks, the README topology documentation, and nothing
   else. That is why the rollback field can honestly say "revert the pin
   commit": there is no generated artifact, no lockfile, and no build output
   downstream of a gitlink to reconcile.

2. **Direction is verified, not assumed.** A submodule pin can be moved
   backwards by accident — a `git commit -- <submodule-path>` takes the
   checkout's HEAD and silently overrides a staged pin. So the act is: stage
   the gitlink, verify the direction against the submodule's `main`, commit,
   and read the landed value back with `git ls-tree`. Both pins in this change
   land at a commit that **is** the current tip of the submodule's `main`
   (read back this session: `1aa184e8…` and `05f44044…`), so the
   fast-forward check is trivially satisfied today and non-trivial at the next
   advance.

3. **`main` on the aggregation is review-gated.** The act lands by PR authored
   through the `session-open-pr` route the aggregation already carries, so the
   PR is authored by `openxfactory[bot]` and the only human approver is not
   also its author.

## 4. Deliberate exclusions

- **No deployment.** Admission pins two repositories that hold nothing which
  runs. No broker, no certificate authority, no realm, no organization, no
  persona, no service client, no key, no credential. Neither repository's
  first `runtime-manifest.yaml` exists yet, and this change does not create
  one — the generated-never-hand-edited rule only holds if it holds for the
  first manifest.
- **No pin advance beyond the recorded commits.** A later commit in either
  repository is a later reviewed aggregation PR.
- **No change to either admitted repository's tree.** Not a file, not a
  setting. Admission is an act of the parent.
- **No new requirement.** Recording compliance with a ratified requirement
  does not need a requirement of its own; the only spec delta is the
  enumeration refresh (D-enumeration).
- **No touch of the two boundary requirements.** They are left exactly as
  their creating changes restated them. This change modifies *"Install
  repository scope"* only.
- **No CI gate.** Each repository's boundary validator is committed and green;
  the workflow that runs it on every push and the required status check on its
  `main` ruleset remain the follow-up their creation changes booked (tasks
  4.5 in both). Pinning a repository whose validator is green but unenforced
  is honest as long as it is said out loud, which is what this bullet is for.
- **No release digest-inventory fix.** `contract-v1.37`'s
  `contracts/releases/contract-v1.37.digests.yaml` still omits both new
  contract families; both pins therefore verify against
  `contracts/manifest.yaml`. That defect is booked as `implement-*` tasks 4.7
  and is not repaired here — editing a released bundle to tidy an admission
  record would be the wrong trade.

## 5. Decisions

### D-enumeration — the *"Install repository scope"* refresh runs here, and the precondition was checked

[`add-trust-anchor` design D8](../add-trust-anchor/design.md) deferred the
enumeration refresh with two conditions: it runs **after both install
repositories exist**, and **only when nothing else is replacing that
requirement** — because a `MODIFIED` delta wholesale-replaces the requirement
it names, so two concurrent replacements would silently drop one repository's
admission.

Both conditions were verified rather than assumed:

- Both repositories exist and are seeded (§1, §2).
- No other active change carries a delta on *"Install repository scope"*.
  Evidence: `grep -rn "Install repository scope" openspec/changes` outside
  `archive/` and outside this change returns **21 hits**, and **every one is
  prose** — `design.md`,
  `tasks.md`, `supporting-docs/`, `proposal.md`, and `evidence/` mentions
  saying the enumeration is deliberately *not* touched. The four active
  `specs/repo-boundary-governance/spec.md` deltas name only four
  requirements: `add-trust-anchor` ADDS *"OpenXPKI install repository
  boundary"*, `add-identity-brokering` ADDS *"Keycloak install repository
  boundary"*, and the two `implement-*` changes MODIFY those same two. None
  names *"Install repository scope"*.

So this change's delta is the only replacement in flight, which is the exact
window tasks 8.1 asked to be run in.

The extension itself is minimal on purpose: the requirement's opening sentence
gains the two repository names, one paragraph records the admission with paths
and remotes and the admitting change, and **both scenarios are restated
verbatim**. The existing `Hermes-Install` / `Omnigent-Install` entries are not
re-labeled with their aggregation paths, even though that would look tidier —
`installs/hermes-install` actually points at `opensoft/xFactory-Hermes-Install`,
and quietly rewriting a ratified requirement's naming of that repository would
smuggle a second decision (and risk the `FarHeap/Hermes-Install` confusion the
aggregation README exists to prevent) into a bookkeeping delta.

### D-index-not-boundary — the enumeration is an index, not a second boundary

Adding two repositories to *"Install repository scope"* could be read as
granting them scope. It does not. Each admitted repository's scope is fixed by
its own ratified boundary requirement, which is narrower and more specific
than the enumeration's "subsystem install, operations, backup, restore,
upgrade, verification, and disaster recovery". The enumeration answers "which
repositories are admitted install repositories?" in one place — that was the
whole point of tasks 8.1 — and the delta says so explicitly so nobody later
cites the enumeration to widen a boundary.

### D-ordering — admission does not wait on the parents archiving

Both boundary requirements are ratified but not yet promoted: their parents
(`add-identity-brokering`, `add-trust-anchor`) have not archived, and the
`implement-*` changes' own tasks 3.5 correctly refuse to archive ahead of
them. That ordering constraint applies to a `MODIFIED` delta, which needs its
target present in the promoted spec. This change's delta targets *"Install
repository scope"*, which **is** promoted today, so it carries no such
dependency and can be authored, reviewed, and archived on its own schedule.

Ratification, not archive, is what authorizes an act in this family: Brett
ratified both boundary requirements on 2026-08-21 and instructed this
admission the same day. Archive is bookkeeping over ratified text — which is
precisely what tasks 8.1 was.

### D-readme — the aggregation README gets two entries, not a bookkeeping sweep

The archived installer precedent's tasks 4.1 updated "the xFactory topology
and current-submodule documentation" in the same act as the pin, so this
change mirrors that: the `Repository Layout` tree and the `Current Submodules`
list both gain `installs/keycloak-install` and `installs/openxpki-install`.

Both of those README blocks are already stale for reasons that predate this
change — `.gitmodules` carries submodules that neither block lists
(`installs/medx-roottruth-install`, `openAvatar`, and several `xFactories/`
entries). Fixing that is a real cleanup and it is **not** done here: silently
adopting another change's bookkeeping inside an admission record makes the
record's diff stop being reviewable, and a reviewer comparing the README
against `.gitmodules` should see exactly the two lines this ratification
authorized. The staleness is named in the proposal's Impact so it is not lost.

### D-no-branch-key — the gitlink is the authority

`installs/xfactory-installer` is the only existing submodule carrying a
`branch = main` key in `.gitmodules`. Neither new entry gets one. A `branch`
key invites `git submodule update --remote`, which advances a pin outside a
reviewed PR — the exact thing the Update field forbids. Matching the majority
of `installs/` entries here is also matching the discipline.
