# Quickstart / validation guide: openxwallet deprecation minor (P2.5)

Every command runs from the feature worktree root
(`../openxFactory-worktrees/P2.5-deprecation-minor`), never from the shared root
checkout. `$WT` below stands for that path.

## Prerequisites

- Python 3 with PyYAML (already required by the repository's validators).
- `git` on PATH.
- `openspec` on PATH for the OpenSpec gate.
- Nothing else. No network access is needed by any check here.

---

## S1 — The eight rows carry the marker, and nothing else moved

```bash
cd "$WT"
# the marker, once per row, with its three sub-keys
grep -c '^    relocating:' contracts/manifest.yaml          # expect: 8
grep -A3 '^    relocating:' contracts/manifest.yaml | grep -c 'to: opensoft/openXwallet'   # expect: 8

# the eight ids that carry it, in manifest order
python3 - <<'PY'
import yaml
m = yaml.safe_load(open("contracts/manifest.yaml"))
print([c["id"] for c in m["contracts"] if "relocating" in c])
PY
```

**Expected**: exactly the eight ids of `data-model.md`, in manifest order, and no
others.

**The floor holds** — this must print nothing at all:

```bash
git diff --name-only origin/main -- \
  contracts/openxwallet/ contracts/openxwallet-agent-profile/ \
  scripts/validate-openxwallet.py scripts/wallet-yaml-syntax-gate.py \
  tests/wallet_yaml_syntax_gate/ .github/workflows/wallet-validation.yml
```

**No row was removed** — this must print `8` before and after:

```bash
git show origin/main:contracts/manifest.yaml | grep -c '  - id: openxwallet'
grep -c '  - id: openxwallet' contracts/manifest.yaml
```

**Digests still verify** (the marker changes no contract file's bytes):

```bash
python3 scripts/validate-manifest-digests.py
```

**Expected**: `OK contracts/manifest.yaml: N per-file digest(s) verify`, exit 0.

---

## S2 — The three bundle names agree, and the inventory is honest

```bash
grep '^contract_bundle_version:' contracts/manifest.yaml     # contract-v1.46
grep -m1 '^## contract-v' contracts/CHANGELOG.md             # ## contract-v1.46 — …
ls contracts/releases/contract-v1.46.digests.yaml
grep '^bundle_tag:' contracts/releases/contract-v1.46.digests.yaml
```

**All four must name `contract-v1.46`** (or whatever the number is after any
merge-order renumber).

The inventory is regenerated, never hand-edited. To prove the committed file is
byte-identical to what the tool emits from the same tree:

```bash
python3 scripts/validate-contract-release.py build \
  --tag contract-v1.46 --output /tmp/regen.digests.yaml
diff contracts/releases/contract-v1.46.digests.yaml /tmp/regen.digests.yaml
```

**Expected**: no diff.

The eight registrations are still on the release surface (FR-017) — and the
containment is TRANSITIVE, through the manifest, because inventory membership is
catalog-driven and has never included the eight artifact files (research R11):

```bash
# the eight files are NOT inventory members, at v1.45 or v1.46 — expect 0 both times
grep -ci openxwallet contracts/releases/contract-v1.45.digests.yaml
grep -ci openxwallet contracts/releases/contract-v1.46.digests.yaml

# what IS checkable: the manifest is a member, and the manifest it digests has 8 rows
grep -A4 'artifact_id: contracts-manifest.yaml' contracts/releases/contract-v1.46.digests.yaml
# NOT `git hash-object` — that is SHA-1 of a blob-with-header. The inventory's
# `digest_source: raw_git_blob` with `digest_algorithm: sha256` means sha256 of
# the raw content bytes:
python3 -c "import hashlib;print('sha256:'+hashlib.sha256(open('contracts/manifest.yaml','rb').read()).hexdigest())"
grep -c '  - id: openxwallet' contracts/manifest.yaml   # expect 8
```

**Expected**: `0` and `0` for the first pair; the recorded manifest digest equal
to that sha256 (verified: `sha256:0750cbdc…`); and `8` rows.

---

## S3 — The release-inventory drift family is clean

```bash
python3 scripts/doc-health.py --single-repo . --family release-inventory-drift
```

**Expected**: `No findings` for `release-inventory-drift` in the Ranked Plan.

**Baseline for comparison** — at base commit `42662b70` this same command
reported THREE findings, one of them error-class:

```
severity=error family=release-inventory-drift path=scripts/validate-hermes-runtime-contracts.py
severity=info  family=release-inventory-drift path=contracts/CHANGELOG.md   (editorial)
severity=info  family=release-inventory-drift path=contracts/manifest.yaml  (editorial)
```

All three are expected to be GONE after this cut, because a new inventory over the
current tree is exactly the "cut a release through the bundle realization order"
that the error's own action text prescribes. Their disappearance is a discharge,
not a suppression.

---

## S4 — The relocation notice, end to end, against a real fixture

This is the evidence `tasks.md` 5.9 asks for: the checker's OUTPUT, not the
manifest rows.

Build a throwaway aggregation checkout whose `openxFactory` gitlink points at the
bundle under test, and a throwaway consumer that pins it:

```bash
set -e
FIX=$(mktemp -d)
PINNED=$(git -C "$WT" rev-parse HEAD)                    # this feature's commit
BASE=$(git -C "$WT" rev-parse origin/main)               # the contract-v1.45 bundle

# an aggregation repo with a .gitmodules naming openxFactory and a real gitlink
mkdir -p "$FIX/agg"
git -C "$FIX/agg" init -q
printf '[submodule "openxFactory"]\n\tpath = openxFactory\n\turl = git@github.com:opensoft/openxFactory.git\n' \
  > "$FIX/agg/.gitmodules"
git -C "$FIX/agg" add .gitmodules
git -C "$WT" worktree add --detach "$FIX/agg/openxFactory" "$PINNED" >/dev/null
git -C "$FIX/agg" update-index --add --cacheinfo 160000,"$PINNED",openxFactory
git -C "$FIX/agg" -c user.email=t@t -c user.name=t commit -qm fixture

# a consumer pinned to THIS bundle
mkdir -p "$FIX/agg/xFactories/Consumer"
printf 'xfactory:\n  contract_ref: %s\n' "$PINNED" > "$FIX/agg/xFactories/Consumer/stack.yaml"
```

**S4a — pinned to this bundle: the WARN appears, exit 0**

```bash
python3 "$WT/scripts/check-openxfactory-pin.py" \
  "$FIX/agg/xFactories/Consumer" --aggregation-root "$FIX/agg"; echo "exit=$?"
```

**Expected**: the pin verdict line, then the multi-line relocation notice naming
all eight artifacts with `-> opensoft/openXwallet @ wallet-v1.1`, then `exit=0`.
See `contracts/pin-check-cli.md` § Worked sample for the exact text.

**S4b — pinned to `contract-v1.45`: no notice at all**

```bash
printf 'xfactory:\n  contract_ref: %s\n' "$BASE" > "$FIX/agg/xFactories/Consumer/stack.yaml"
python3 "$WT/scripts/check-openxfactory-pin.py" \
  "$FIX/agg/xFactories/Consumer" --aggregation-root "$FIX/agg"; echo "exit=$?"
```

**Expected**: the pin verdict line ONLY (a stale-behind WARN, since `$BASE` is an
ancestor of `$PINNED`), no relocation line, `exit=0`.

**Cleanup**

```bash
git -C "$WT" worktree remove --force "$FIX/agg/openxFactory"
rm -rf "$FIX"
```

---

## S5 — The unit and pack-member tests

```bash
cd "$WT"
python3 -m pytest tests/conformance-gate/ -q
```

**Expected**: all pass, including the four pre-existing pin tests unchanged
(`test_pin_equal_passes`, `test_pin_stale_behind_warns_with_refresh_instruction`,
`test_pin_divergent_errors`, `test_pin_skips_outside_aggregation`) and the
`test_pin_hands_git_absolute_directories` argv test.

Then the whole suite, which is what CI's `pytest-suite` collects:

```bash
python3 -m pytest -q
```

---

## S6 — The OpenSpec gate

```bash
cd "$WT"
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

**Expected**: pass. This feature edits only tick-boxes and notes in
`openspec/changes/split-openxwallet-repo/tasks.md`, adding no requirement and no
scenario, so the parser's SHALL/MUST first-line rule is not engaged.

---

## S7 — Whole-repo doc health, measured as a delta

```bash
cd "$WT"
python3 scripts/doc-health.py --single-repo . 2>&1 | tail -40
```

**Expected**: no finding that is not also present at `origin/main`. The
release-inventory-drift trio described in S3 should be **absent** (improved). If
any other family reports something new, it is a defect of this feature.

---

## What is deliberately NOT validated here

- **The annotated tag.** It does not exist yet and must not. `contract-v1.44` and
  `contract-v1.45` are annotated tags cut by the operator; no workflow creates
  them. `validate-contract-release.py verify-tag` / `verify-promotion` are the
  operator's post-merge checks, not this feature's.
- **The LedgerxFactory observation.** P5a.2 bumps its `stack.yaml` to this minor
  and adds the checker invocation to its estate run. S4 proves the checker warns;
  P5a.2 proves the one live consumer sees it.
