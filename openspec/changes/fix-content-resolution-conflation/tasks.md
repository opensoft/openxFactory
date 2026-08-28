# Tasks: fix-content-resolution-conflation

Every measurement quoted below was taken 2026-08-28 in a fresh worktree off
`origin/main` at `6612d3239cbc99b73eb32cf76a861929aa901276`. A task that cites a
number owes a re-measurement at realization, not a copy of the number.

## 1. Admission

- [ ] 1.1 Land the packet as an ACTIVE change with `Status: ratified`
      (the admission spelling: an approval act exists and is cited, per
      `sanction-ratified-record-spelling`), its
      `.openspec.yaml` recording the 2026-08-28 ad-hoc origin — Brett's verbatim
      selection "lets do all 3 in order" of the orchestrating session's
      recommended "the measured-latents bundle" — with the two voices kept
      apart, and the sibling `fix-pin-value-boundary-and-sentinel-split` named
      in `related:` as citing the same act.
- [ ] 1.2 README "OpenSpec Records" active entry, stating the defect, the two
      ADDED requirements, the two-packet split, and — first, because it is what
      a reader needs to plan around — that a contract bundle cut rides the
      realization.
- [ ] 1.3 `OPENSPEC_TELEMETRY=0 openspec validate fix-content-resolution-conflation --strict`
      and `--all --strict` green. Baseline before the pair: **76 passed, 0
      failed**.
- [ ] 1.4 § Orchestrator decisions OD-1 … OD-6 and § Open Questions Q1 … Q4 are
      open at filing. **OD-1 is the one that changes what was approved**; put it
      to Brett first, because merging the two packets back into one is cheapest
      before either is reviewed.

## 2. Implementation — the distinction

- [ ] 2.1 Re-measure before editing. Confirm the raise-site count in
      `content.py` (**15 sites, 14 distinct messages** at filing), confirm that
      `content.py:125` is still the only one meaning "the tree was read and the
      path was not in it", and re-run the six-condition table from
      `proposal.md` § What was measured 2 against the tree as it then stands. If
      another session has already narrowed the catch, say so and re-scope
      rather than re-applying.
- [ ] 2.2 `content.py:125` gains a declared code naming the absent-path
      condition. Purely additive: swept at filing, **nothing in this repository
      reads `ContentResolutionError.code` and the string
      `HRC-CONTENT-DEPENDENCY` occurs nowhere but its own default**. Re-sweep
      before relying on that.
- [ ] 2.3 `_blob_object_id` (`release.py:312-316`) returns `None` for that code
      alone and fails closed for everything else, with a reason naming the
      condition observed rather than a conclusion about the release. Per Q1's
      recommendation the refusal is `ReleaseDependencyError` wrapping the
      original with `from`; if Brett rules otherwise, record the ruling here.
- [ ] 2.4 `_CommitSource.exists` (`release.py:401-405`) gets the same treatment
      (OD-5). Its four callers — `:519`, `:532`, `:611`, `:621` — decide release
      membership and whether `contracts/manifest.yaml` is present at the commit,
      so a `False` manufactured from an environment failure is a verdict about
      the release.
- [ ] 2.5 `HGR-RELEASE-PATH-UNRESOLVABLE` (`:713-719`) is NOT touched, and the
      requirement is scoped so that leaving it is conforming rather than a
      self-violation (OD-3, `design.md` § 4). Confirm at realization that the
      promoted wording still excludes it; if the wording moved in review, this
      task becomes a scope question rather than a silent inconsistency.
- [ ] 2.6 Nothing about a successful resolution moves. Same return value, same
      comparison at `:796-798`, same finding codes, same severities, same exit
      codes, `_is_ancestor` byte-unchanged as `fix-release-reachability-race`
      § 2.4 protected it.

## 3. Implementation — the proofs

- [ ] 3.1 The absent-path proof: a commit whose tree does not contain a
      release-surface path still reaches the release answer it reaches today,
      unchanged. This is the proof that catches an over-eager refusal, which is
      this fix's real failure mode.
- [ ] 3.2 The unavailable-store proof: a resolution failing for a reason other
      than absence produces a fail-closed refusal whose reason names the
      condition, not the release.
- [ ] 3.3 **The quiet-direction proof, which is the one that matters.** BOTH
      sides of a `_surface_drift` comparison fail; the verification must refuse,
      not report the surface undrifted. Today two `None`s compare equal and the
      surface reports clean having been read on neither side — assert the
      refusal, and assert that no `HGR-RELEASE-SURFACE-DRIFT` finding is emitted
      either, because the failure has two wrong answers and only one of them is
      loud.
- [ ] 3.4 The safety-refusal proof: a release-surface path that is a directory
      or a nested repository link at one commit is refused, not read as absence.
      Reachable from committed data rather than only from a broken environment,
      which is why it is a proof and not a note.
- [ ] 3.5 Per Q3, the release-surface proofs reuse the `_bare_origin` /
      `_repo_with_committed_inventory` fixture pair already in
      `tests/hermes_runtime_contracts/test_release_inventory.py`, and the
      resolver proofs go in `test_content_resolution.py`, beside the fifteen
      refusals they distinguish.
- [ ] 3.6 Per Q4, the failing conditions are driven by ARGUMENT (a non-canonical
      path, an absent repository) rather than by a real timeout, and each proof
      says so. The requirement is about the distinction, not about any one way
      of failing.
- [ ] 3.7 Mutation-pin at SOURCE level: flatten the distinction back to a single
      value and every refusal proof must fail, while the absent-path proof must
      still pass. A proof that survives the flattening is unpinned and gets
      rewritten rather than accepted — the rule the sibling family's third
      requirement states in its own third scenario.
- [ ] 3.8 If the new scenarios are bound in
      `contracts/hermes-runtime/evidence-register.yaml` alongside the existing
      `SCO-002-S03` binding to
      `test_verify_promotion_rejects_a_drifted_release_surface`, note that the
      register is ITSELF an inventory member (`type: evidence-register`) — so
      the binding rides the same cut, and § 4 must be rebuilt after it, not
      before.

## 4. Realization — the contract bundle

This change cannot land its code without re-cutting the bundle that describes
it. Measured at filing by PARSE:
`contracts/releases/contract-v2.0.digests.yaml`, 192 entries,
`scripts/hermes_runtime_validation/release.py` present as `type: validator`,
`digest: sha256:660e55ca7e6896ea24106483b926e1919a0cb195ef8b9a700a3522f1f393f6b0`,
which is exactly `sha256sum` of the tree's copy; `content.py` present on the
same terms; the editorial set is three files and neither is in it. The
realization order is the one `contract-v1.44` used for this same file, two days
before this filing, and the one recorded in the release finishing recipe.

- [ ] 4.1 **Allocate the bundle number at realization, NOT here.**
      `contract-v2.0` is current; merge order decides the next minor, and the
      `contract-v1.28` renumber sweep is the precedent for why a proposal must
      not reserve one. Collision-check both ways the recipe asks for before
      claiming a number: `git ls-tree origin/main contracts/releases/` and
      `git ls-remote --tags origin 'refs/tags/contract-v2.*'`, plus a scan of
      open pull requests for any that touches a release surface.
- [ ] 4.2 `contracts/manifest.yaml` — advance `contract_bundle_version` (`:3`).
      Expect this to be the only manifest edit: this change touches no schema,
      so no schema row digest moves. The historical prose mentions of earlier
      bundles deeper in the file are consumption-rule text and are left alone.
- [ ] 4.3 `contracts/CHANGELOG.md` — an additive entry stating the class and why
      the cut exists: two validator members' bytes moved, no schema changed,
      `contract_schema_version` unchanged, no instance valid at `contract-v2.0`
      narrowed, consumers pinned there conformant until they upgrade. Name the
      `contract-v1.44` and `contract-v1.10` precedents for this same file.
- [ ] 4.4 `scripts/validate-contract-release.py build --tag contract-v<next>
      --output contracts/releases/contract-v<next>.digests.yaml` — deterministic
      from manifest plus contract index, and RERUN after ANY further edit to an
      inventory member, including the evidence register (§ 3.8). Build twice to
      distinct paths and prove the outputs byte-identical. **Never hand-edit an
      inventory to match a tree**; that is the shortcut `release-surface-integrity`
      forbids by name. Expect `entries=192` unchanged — nothing joins or leaves
      the bundle — and expect the two moved digests to be exactly `sha256sum` of
      the edited files.
- [ ] 4.5 `verify-commit --commit HEAD` after committing. Then
      `verify-promotion --commit <candidate> --remote origin --tag <tag>` BEFORE
      tagging — which cannot be done before the merge, because it requires the
      candidate to be reachable from the remote's `main`. Per the
      `contract-v1.44` precedent this arm discharges PARTIALLY at the pull
      request and completes post-merge, and the annotated tag is not the
      authoring session's act unless it is explicitly given.
      Note the fortunate property that precedent also records: the cut runs the
      NEW code, so the fix is exercised by the release that carries it.

## 5. Verification

- [ ] 5.1 `set -o pipefail; python3 -m pytest tests/hermes_runtime_contracts -q`
      — exit code READ, never inferred from the tail of the output. This
      repository has merged two pull requests red by inferring it.
- [ ] 5.2 `set -o pipefail; python3 -m pytest tests/doc-health -q` green too:
      the release-inventory-drift family reads the inventory this change
      re-cuts, so a mis-built inventory shows up here as well as in the release
      verifier. Baseline at filing: **1249 passed, 0 failed, exit 0**.
- [ ] 5.3 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
- [ ] 5.4 Re-affirm by PARSE that the rebuilt inventory reproduces the COMMITTED
      tree, not just the working tree — which is what `verify-commit` answers
      and what a `sha256sum` of the working file does not.

## 6. Archive gate

- [ ] 6.1 Merged to `origin/main` with both required checks green, the merge
      commit re-verified an ancestor of `origin/main` and a real two-parent
      merge read out of `git cat-file -p` rather than off the pull request page.
- [ ] 6.2 The cut complete: manifest, changelog, digest inventory and a verified
      annotated tag all agreeing on the new bundle, `verify-tag --remote origin
      --tag contract-v<next>` exit 0, and the aggregation submodule pointer
      synced.
- [ ] 6.3 On the merged tree: both suites green under `set -o pipefail`,
      `openspec validate --all --strict` green, and the release-inventory-drift
      family reporting no `error` for either moved member.
- [ ] 6.4 Every § 7 follow-up carries a disposition rather than a blank box, and
      every OD and Q carries a ruling or an explicit carry-forward.

## 7. Open — deliberately not closed by this change

- [ ] 7.1 **`HGR-RELEASE-PATH-UNRESOLVABLE` (`release.py:713-719`) CONVERTS
      EVERY `ContentResolutionError` FROM `read_member` INTO A FINDING ABOUT THE
      INVENTORY PATH.** Measured here, not inherited. Milder than the two sites
      this packet fixes — it emits a named finding rather than silence — but it
      still turns an environment failure into a verdict about the release. Left
      because changing it changes what a PUBLISHED finding code means to
      consumers reading verifier output, which is a contract question rather
      than a defect fix. The requirement is scoped so that leaving it is
      conforming (OD-3), which is a decision and not an oversight.
- [ ] 7.2 **THE SWEEP OF `scripts/hermes_runtime_validation/` FOR THE SAME
      PATTERN.** `fix-release-reachability-race` § 6.1 opened this for the
      reachability layer and named `consumer_handoff.py` as the obvious next
      candidate; the content layer owes the same sweep. This packet measured
      `release.py` and claims nothing about the rest, on that packet's own rule:
      a sweep asserted without measurement is the same species of unearned
      answer these packets are about.
- [ ] 7.3 **THE ELEVEN-MINUTE EXPOSURE WINDOW**, § 6.2 of the same packet.
      Sharding, or exercising the realization path against a pinned fetch rather
      than the live remote, would shrink it. Both are `pytest-suite.yml`
      questions rather than obligations about the verifier.
- [ ] 7.4 **WHETHER `content.py` SHOULD DECLARE A CODE PER CONDITION RATHER THAN
      ONE.** Q2 recommends one, on the ground that the remaining fourteen are
      all "the question could not be asked" and a vocabulary nothing consumes is
      the drift the sentinel declaration's second direction exists to report. If
      a second caller ever needs to distinguish two of the fourteen, that is the
      evidence a wider vocabulary would need, and this item is where the next
      reader should find that said.
