# Tasks: admit-install-repos-to-aggregation

Dependency-ordered. §1 is authored in this change and is complete. §2 is the
aggregation act — it runs in `opensoft/xFactory`, not here, and is left open
for the orchestrator. §3 reads the act back off the landed tree, so it cannot
close before §2. §4 is the bookkeeping this session's org-owner act unblocked,
done during this authoring. §5 is the named work this change deliberately does
NOT do.

**Realization status, 2026-08-21.** The admission RECORD exists and the
bookkeeping is closed; the aggregation ACT has not run. This change declares a
code surface, so it archives only on merged realization with green evidence
(`release-realization`) — which here means the aggregation PR merged and §3's
read-backs green.

Reasoning for every decision is in [design.md](design.md); the authoritative
obligations are the two ratified boundary requirements restated in
[`implement-keycloak-install-repo`](../implement-keycloak-install-repo/specs/repo-boundary-governance/spec.md)
and
[`implement-openxpki-install-repo`](../implement-openxpki-install-repo/specs/repo-boundary-governance/spec.md),
plus the promoted *"Deferred aggregation and web-console integration"* and
*"Neutral installer repository integration"* requirements in the
[promoted spec](../../specs/repo-boundary-governance/spec.md).

## 1. The admission records (this change; design §1-§4)

- [x] 1.1 Record `opensoft/Keycloak-Install` under all eight required field
      labels — **path, remote, visibility, exact validated commit, checkout,
      compatibility, update, rollback**.
      **DONE 2026-08-21** — [design.md](design.md) §1:
      `installs/keycloak-install`,
      `git@github.com:opensoft/Keycloak-Install.git`, private (repo id
      `1342329131`, default branch `main`), exact validated commit
      `1aa184e891d4ba6e641a31260d3f64d2b335f175`, SSH submodule manually
      initialized with no `branch =` key (recursive checkout == plain checkout:
      **no `.gitmodules`**, HTTP 404 read back at `main`), `contract-v1.37`
      pinned at contract commit `c1ffa0fdd358f8db7a86dff4c7c40583e581adff` in
      `config/contracts/identity-brokering/manifest.yaml`, reviewed-PR-only pin
      advance with fast-forward direction verified, revert-the-pin rollback.
- [x] 1.2 Record `opensoft/OpenXPKI-Install` under the same eight labels, with
      **recursive** checkout named explicitly as its requirement demands.
      **DONE 2026-08-21** — [design.md](design.md) §2:
      `installs/openxpki-install`,
      `git@github.com:opensoft/OpenXPKI-Install.git`, private (repo id
      `1342329163`, default branch `main`), exact validated commit
      `05f440444d9091206778e838454ed9b5bb7bff60`, recursive checkout ==
      plain checkout (**no `.gitmodules`**, HTTP 404 read back at `main`; it
      does not vendor `opensoft/Opensoft-Tenant`, so the image-custody split
      survives a recursive checkout), `contract-v1.37` at the same contract
      commit in `config/contracts/trust-anchor/manifest.yaml`, same update and
      rollback discipline plus the ACR-digest gate on any topology-bearing
      advance.
- [x] 1.3 State the shared update/rollback discipline and the deliberate
      exclusions once, rather than leaving them implied by the two tables.
      **DONE 2026-08-21** — [design.md](design.md) §3 (pin-only assembler,
      direction verified not assumed, review-gated `main`) and §4 (no
      deployment, no pin advance beyond the recorded commits, no change to
      either admitted tree, no new requirement, no touch of the two boundary
      requirements, no CI gate, no release digest-inventory fix).
- [x] 1.4 Verify the values rather than transcribing them from the creation
      records.
      **DONE 2026-08-21** — re-read this session with `gh api`: both
      repositories' `visibility` / `private` / `default_branch` / `id`, both
      `commits/main` tips (which equal the two recorded validated commits),
      both `contents/.gitmodules` (404 — genuine absence, since
      `commits/main` succeeded on the same token), and both contract-pin
      manifests' `contract_bundle_tag` / `commit` / `revision_kind` /
      `source_repository` / `digest_source`.
- [x] 1.5 ONE spec delta: `MODIFIED` *"Install repository scope"*, restating
      the requirement entirely — both scenarios verbatim — and extending its
      enumeration with the two admitted repositories. Confirm by grep that no
      other active change is replacing that requirement (design D-enumeration),
      because two concurrent replacements silently drop one admission.
      **DONE 2026-08-21** —
      [specs/repo-boundary-governance/spec.md](specs/repo-boundary-governance/spec.md):
      2 scenarios in, 2 scenarios out, both byte-identical to the promoted
      text. Grep evidence in design D-enumeration: every non-archive hit for
      *"Install repository scope"* is prose, and the four active
      `repo-boundary-governance` deltas name only the two boundary
      requirements (ADDED by the parents, MODIFIED by the `implement-*`
      changes) — none names this one.

## 2. The aggregation act (in `opensoft/xFactory`; NOT this repository)

Each box lands in the aggregation repository. Leave them open until the PR
merges — a tick here is a claim about `opensoft/xFactory`'s `main`.

- [x] 2.1 DONE 2026-08-21 — xFactory PR #127 (squash e02d0a8), entries carry url only, no branch key. Add the two `.gitmodules` entries, matching the existing `installs/`
      style and carrying **no `branch =` key** (design D-no-branch-key):
      `[submodule "installs/keycloak-install"]` path
      `installs/keycloak-install`, url
      `git@github.com:opensoft/Keycloak-Install.git`; and
      `[submodule "installs/openxpki-install"]` path
      `installs/openxpki-install`, url
      `git@github.com:opensoft/OpenXPKI-Install.git`.
- [x] 2.2 DONE 2026-08-21 — gitlinks landed at 1aa184e (keycloak-install) and 05f4404 (openxpki-install) exactly. Add the two gitlinks **at the exact validated commits and nowhere
      further**: `installs/keycloak-install` ->
      `1aa184e891d4ba6e641a31260d3f64d2b335f175`,
      `installs/openxpki-install` ->
      `05f440444d9091206778e838454ed9b5bb7bff60`. Stage the gitlink, verify
      the direction against the submodule's `main`, then commit — never
      `git commit -- <submodule-path>`, which takes the checkout's HEAD and
      silently overrides a staged pin.
- [x] 2.3 DONE 2026-08-21 — tree listing + remotes list, same commit. Update the README submodule documentation in the same act, as the
      archived installer precedent's tasks 4.1 did: add both paths to the
      `Repository Layout` tree and both `path -> remote` lines to
      `Current Submodules`. Add exactly those entries — the pre-existing
      staleness of both blocks is not swept in here (design D-readme).
- [x] 2.4 DONE 2026-08-21 — exactly those 4 paths staged (5-file diff incl. the folded openxFactory pointer sync, recorded in the PR body). Stage explicit paths only (`.gitmodules`, the two gitlinks, `README.md`)
      and inspect `git diff --cached --stat` for foreign entries before
      committing. This checkout is shared between sessions; a bare
      `git commit` takes whatever any session has staged.
- [x] 2.5 DONE 2026-08-21 — xFactory PR #127 authored by openxfactory[bot], approved by Brett, auto-merged e02d0a8. Open the PR through the `session-open-pr` route — the aggregation
      carries its own copy of the same
      [workflow](../../../.github/workflows/session-open-pr.yml) openxFactory
      does — so the PR is authored by `openxfactory[bot]` and Brett is free to
      approve it. Do not author it as `brettheap`; do not self-approve; do
      not merge.

## 3. Read-backs (off the landed aggregation tree)

- [x] 3.1 DONE 2026-08-21 — merged-main read-back: 160000 1aa184e keycloak-install, 160000 05f4404 openxpki-install, openxFactory at eeb095d. `git ls-tree HEAD installs/keycloak-install installs/openxpki-install`
      on the merged aggregation `main` — both entries `commit` mode, showing
      exactly `1aa184e891d4ba6e641a31260d3f64d2b335f175` and
      `05f440444d9091206778e838454ed9b5bb7bff60`. Read the landed value back;
      do not infer it from what was staged.
- [x] 3.2 DONE 2026-08-21 — both urls read back exactly (git@github.com:opensoft/Keycloak-Install.git, .../OpenXPKI-Install.git); no branch keys present. Parse `.gitmodules` on the merged `main` — `git config -f .gitmodules
      --get-regexp '^submodule\.installs/(keycloak|openxpki)-install\.'` —
      confirming both `path` and `url` for each and **no `branch` key** on
      either.
- [x] 3.3 DONE 2026-08-21 — both cloned and checked out at exactly the validated commits (submodule status: 1aa184e heads/main, 05f4404); recursive init pulled nothing further (no nested submodules, per the admission record's vendoring check). `git submodule update --init --recursive` over the two new paths
      reproduces both repository boundaries from the recorded commits, with
      nothing nested appearing (neither repository has a `.gitmodules`).
- [x] 3.4 DONE 2026-08-21 — change valid --strict post-merge. `OPENSPEC_TELEMETRY=0 openspec validate
      admit-install-repos-to-aggregation --strict` and `--all --strict` green
      at archive as well as at authoring.
- [ ] 3.5 Archive gate: this change declares a code surface, so it archives
      only on merged realization with green evidence — 2.5's PR merged and
      3.1-3.3 captured. No delta-ordering dependency exists (design
      D-ordering): the delta's target *"Install repository scope"* is already
      promoted, unlike the two boundary requirements.

## 4. Bookkeeping unblocked by the org-owner act (done in this authoring)

- [x] 4.1 Tick [`add-trust-anchor` tasks 8.1](../add-trust-anchor/tasks.md) —
      the deferred *"Install repository scope"* enumeration refresh — with a
      DONE note naming this change.
      **DONE 2026-08-21** — ticked, citing this change's delta and the
      grep that satisfied its "run when nothing else is replacing that
      requirement" condition.
- [x] 4.2 Tick
      [`implement-keycloak-install-repo` tasks 1.3 and 3.3](../implement-keycloak-install-repo/tasks.md)
      with the App-installation read-back facts.
      **DONE 2026-08-21** — installation `145372182` (App `4253636`,
      `openxfactory`) now lists `opensoft/Keycloak-Install`, 19 repositories
      total. Both App secrets were already read back by name.
- [x] 4.3 Tick
      [`implement-openxpki-install-repo` tasks 1.3 and 3.3](../implement-openxpki-install-repo/tasks.md)
      with the same read-back facts for `opensoft/OpenXPKI-Install`.
      **DONE 2026-08-21** — same installation, same read-back, both
      repositories present.
- [x] 4.4 Append a dated App-installation addendum to each creation-record
      evidence file, so the read-back lives with the rest of that change's
      evidence rather than only in a tick.
      **DONE 2026-08-21** — an *"Addendum — App installation read-back"*
      section in
      [the Keycloak record](../implement-keycloak-install-repo/evidence/creation-record-2026-08-21.md)
      and
      [the OpenXPKI record](../implement-openxpki-install-repo/evidence/creation-record-2026-08-21.md).
- [x] 4.5 In each `implement-*` change's §4, annotate the
      aggregation-admission follow-up as executed by this change — **annotate,
      do not tick**. Both items are phrased as follow-ups that run elsewhere
      ("NOT this change… a separate reviewed change"), and their own ratified
      requirements forbid the creation change from being accepted as the
      admission record; a tick there would claim exactly that.
      **DONE 2026-08-21** — `implement-keycloak-install-repo` tasks 4.1 and
      4.8, and `implement-openxpki-install-repo` tasks 4.1 and 4.6, annotated
      with the executing change and left unticked.
- [x] 4.6 Add one entry at the top of README's *"OpenSpec Records"* Active
      changes block, in the neighbours' format.
      **DONE 2026-08-21.**
- [x] 4.7 `OPENSPEC_TELEMETRY=0 openspec validate
      admit-install-repos-to-aggregation --strict` and `--all --strict` green
      at authoring.
      **DONE 2026-08-21** — output recorded in the authoring report; the
      archive-time run is task 3.4.

## 5. Named follow-ups — NOT this change

Each is a separate reviewed change. None is authorized by this ratification.

- [ ] 5.1 **Broker deployment** — the Keycloak topology and the first
      GENERATED `config/clients/opensoft/runtime-manifest.yaml`, its
      credentials being `credential-contracts` records with declared custody.
      `implement-keycloak-install-repo` tasks 4.2.
- [ ] 5.2 **OpenXPKI QA topology migration** — moving the QA server / client /
      web manifests out of `opensoft/Opensoft-Tenant` into
      `deploy/kubernetes/`, with the immutable ACR digest recorded. Gated on
      `add-openxpki-qa-image-pipeline` committing and ratifying.
      `implement-openxpki-install-repo` tasks 4.2.
- [ ] 5.3 **CI wiring for both boundary validators** — the workflow that runs
      `validate-boundary.py` on every push and PR in each repository, plus
      adding it as a required status check on each `main` ruleset.
      `implement-*` tasks 4.5.
- [ ] 5.4 **OpsxFactory `keycloak-administration` and `pki-administration`** —
      the governed administration workflows, with their service-subject kinds
      registered in lockstep (`customer-kinds` + Hermes template +
      `stack.yaml`, grant ceilings in `credentials/requirements.yaml`).
      Developed in `OpsxFactory:staging:identity-pki-administration`.
- [ ] 5.5 **`contract-v1.37` release digest-inventory repair** —
      `contracts/releases/contract-v1.37.digests.yaml` omits both new contract
      families, so neither pin can be verified against it (both verify against
      `contracts/manifest.yaml` instead). `implement-*` tasks 4.7.
- [ ] 5.6 **Aggregation README submodule-documentation cleanup** — both README
      blocks omit already-pinned submodules (`installs/medx-roottruth-install`,
      `openAvatar`, and several `xFactories/` entries). Deliberately not swept
      into this admission act (design D-readme).
- [ ] 5.7 **Any pin advance** for either repository — a new reviewed
      aggregation PR on the recorded update discipline, never an extension of
      this ratification.
