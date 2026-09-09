# Quickstart: reproduce every claim this feature makes

**Feature**: `030-realize-codexfactory-repository-identity` | **Date**: 2026-09-08
**Head measured**: `e8021fed`

Every number in [plan.md](./plan.md), [research.md](./research.md) and
[data-model.md](./data-model.md) is reproducible from this page. Run these from
the feature worktree root, never from the shared checkout.

```sh
cd /home/brett/projects/xFactory/openxFactory-worktrees/030-realize-codexfactory-identity
```

## 0. Prerequisites

```sh
python3 --version                # 3.x
gh auth status                   # for the transfer-state check only
git rev-parse HEAD               # the head every count below is taken at
```

## 1. The sweep, and the per-class arithmetic (packet 2.1, 2.2, 2.3)

The recorded command, verbatim from the packet:

```sh
git grep -ic "opensoft/codexfactory" -- .
```

Totals, and the per-class split, with each class's pathspec:

```sh
cls() {
  label="$1"; shift
  git grep -ic "opensoft/codexfactory" -- "$@" \
    | awk -F: -v L="$label" '{s+=$NF; f++} END{printf "%-46s %4d %4d\n", L, s+0, f+0}'
}
cls "contracts (not signed-chain)  RENAME" 'contracts/' ':!contracts/signed-execution-chain/'
cls "tests                         RENAME" 'tests/'
cls ".github                       RENAME" '.github/'
cls "governance                    RENAME" 'governance/'
cls "scripts                       RENAME" 'scripts/'
cls "docs (not decisions)          RENAME" 'docs/' ':!docs/decisions/'
cls "README.md                     RENAME" 'README.md'
cls "signed-execution-chain        FROZEN" 'contracts/signed-execution-chain/'
cls "openspec archive              FROZEN" 'openspec/changes/archive/'
cls "specs                         FROZEN" 'specs/'
cls "docs/decisions                FROZEN" 'docs/decisions/'
cls "active packets            NOT SWEPT" 'openspec/changes/' ':!openspec/changes/archive/'
cls "ideation                  NOT SWEPT" 'ideation/'
cls "ALL                             ---" '.'
```

**Expected at `e8021fed`**: RENAME 124/60, FROZEN 78/54, NOT SWEPT 125/49,
TOTAL 327/163. The drift from the 2026-09-07 baseline of 281/150 is attributed
cause by cause in [data-model.md](./data-model.md) § Path class.

**Caution, and it cost time**: `git grep -Ic` is **not** `git grep -ic`. `-I`
means "skip binary"; the case-insensitive flag is lowercase `-i`. With `-Ic` the
same sweep reports 4 hits, because the literal lowercase `opensoft/codexfactory`
appears only four times.

## 2. The transfer has not happened (the fact the gating rests on)

```sh
gh api repos/codeXfactory/codexFactory --jq '.full_name'      # HTTP 404
gh api repos/opensoft/codexFactory --jq '{full_name,private,visibility}'
# {"full_name":"opensoft/codexFactory","private":true,"visibility":"private"}
gh api orgs/codeXfactory --jq '.plan.name'                    # enterprise (OQ-1, verified)
```

## 3. The denominator's new sorted position, derived not copied (packet 3.1)

```sh
grep -n "repository:" contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml
```

Five entries plus one exclusion row. `c` (0x63) sorts before `o` (0x6F), and
`adopt-medxsoft-repository-identity` has not landed, so the codex entry goes
from position 5 to position **1**. Confirm the sort assertion and the
value-for-value comparison after the move:

```sh
python3 -m pytest tests/hermes_runtime_contracts/test_domain_regression.py -q
```

## 4. The eight inventoried members (packet 7.5, design § 5)

```sh
INV=contracts/releases/contract-v3.4.digests.yaml
grep -c "path:" "$INV"        # 283
for f in \
  contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml \
  contracts/hermes-runtime/fixtures/regression/digest-mismatch.yaml \
  contracts/hermes-runtime/fixtures/regression/duplicate-repository.yaml \
  contracts/hermes-runtime/fixtures/regression/missing-exclusion-reason.yaml \
  contracts/hermes-runtime/README.md \
  docs/contract-versioning-policy.md \
  docs/terminology-and-repo-topology.md \
  docs/xfactory-domain-factory-model.md ; do
  grep -q " $f\$" "$INV" && echo "INVENTORIED  $f" || echo "not-in-inv   $f"
done
```

All eight read `INVENTORIED`. To prove the converse — that **none** of the other
52 renamed files is a member — run the same loop over the RENAME file list minus
these eight; every line reads `not-in-inv`.

## 5. The freeze, proved by diff and not by inspection (packet 6.1, 6.2, 6.3)

Across every pull request this feature opens, these diffs are empty:

```sh
BASE=origin/main
git diff --stat "$BASE"... -- \
  contracts/signed-execution-chain/ \
  openspec/changes/archive/ \
  docs/decisions/ \
  ideation/
# specs/ excluding THIS feature's own directory:
git diff --stat "$BASE"... -- specs/ ':!specs/030-realize-codexfactory-identity/'
# other lanes' active packets, excluding the packet this feature files evidence into:
git diff --stat "$BASE"... -- openspec/changes/ \
  ':!openspec/changes/archive/' \
  ':!openspec/changes/adopt-codexfactory-repository-identity/'
```

And the validator that would catch a corpus-wide `sed`:

```sh
python3 scripts/validate-signed-execution-chain.py .
```

## 6. No BARE name was edited (packet 6.4)

A transfer moves the OWNER SEGMENT ONLY, so a bare `codexFactory` — a member
name, a wallet/grant id, a change id, a directory or a submodule path — must be
byte-identical before and after.

**Two wrong ways to test this, both tried.** A grep over diff lines
false-positives on every new line of prose that names the repository. Counting
bare occurrences per file and demanding equality false-positives on any
**add-only** diff, because prose about this work names the repository and the
change id `adopt-codexfactory-repository-identity` *contains the bare string
itself*.

The test that actually holds: a file whose diff **removes no line** cannot have
edited anything, whatever its count does; a file whose diff removes lines is
compared on the **multiset of bare occurrences in the removed lines against
those in the added lines** — every bare occurrence that left must come back.

```sh
python3 - origin/main <<'EOF'
import collections, re, subprocess, sys
BASE = sys.argv[1]
OWNED = re.compile(r"(?:opensoft|codeXfactory|codexfactory|MedxSoft)/codexFactory", re.I)
BARE  = re.compile(r"codexfactory", re.I)

def tokens(lines):                      # bare occurrences, with context, as a multiset
    bag = collections.Counter()
    for line in lines:
        masked = OWNED.sub("\x00", line)
        for m in BARE.finditer(masked):
            bag[masked[max(0, m.start() - 24): m.end() + 24]] += 1
    return bag

addonly = compared = 0; bad = []
for row in subprocess.run(["git","diff","--name-status",BASE],
                          capture_output=True, text=True).stdout.split("\n"):
    if not row.strip():
        continue
    path = row.split("\t")[-1]
    if subprocess.run(["git","show",f"{BASE}:{path}"],
                      capture_output=True, text=True).returncode:
        print(f"  new file (edits nothing): {path}"); continue
    diff = subprocess.run(["git","diff","-U0",BASE,"--",path],
                          capture_output=True, text=True).stdout.split("\n")
    removed = [l[1:] for l in diff if l.startswith("-") and not l.startswith("---")]
    added   = [l[1:] for l in diff if l.startswith("+") and not l.startswith("+++")]
    if not removed:
        addonly += 1; continue
    compared += 1
    lost = tokens(removed) - tokens(added)
    if lost:
        bad.append((path, lost))
print(f"add-only diffs (cannot have edited anything): {addonly}")
print(f"diffs with removals, bare multiset compared:  {compared}")
for p, lost in bad:
    for ctx, n in lost.items():
        print(f"!!! {p}: lost {n}x ...{ctx.strip()}...")
sys.exit(1 if bad else 0)
EOF
```

**Results.** On the rename slices (#801, #802, #805, #806) every changed file has
removals and the multiset is preserved. On the mapping-row slice all four changed
pre-existing files are **add-only**, so 6.4 passes there by construction — and
their bare counts DO rise, which is why the equality form had to be replaced.

Filenames are bare names too, so this must also stay empty:

```sh
git diff --name-status --diff-filter=R origin/main || echo "clean: no rename"
```

## 7. The affected validators and suites (packet 7.1)

```sh
python3 -m pytest tests/hermes_runtime_contracts tests/clearing \
                  tests/factory_identity tests/review_lane_pin -q
python3 scripts/validate-hermes-runtime-contracts.py .
python3 scripts/validate-factory-identity.py .
python3 scripts/validate-clearing-dispatch.py .
python3 scripts/validate-signed-execution-chain.py .
python3 scripts/validate-omnigent-contracts.py        # NO argument = self-test; a path argument means REPO mode and fails on this tree
python3 scripts/validate-hermes-domain-overlay.py .
```

## 8. Corpus bookkeeping (packet 8.2, 8.3)

```sh
OPENSPEC_TELEMETRY=0 openspec validate adopt-codexfactory-repository-identity --strict
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
python3 scripts/validate-sequenced-after.py . --ledger-diff
```

**Expected `--all` result: N passed / 1 failed.** The one failure is
`disposition-codexfactory-declared-renames`, a deltaless packet about declared
SCENARIO retitles — unrelated to repository renames, and neither caused nor
repaired by this feature. See [research.md](./research.md) R-11.

## 9. The release-inventory transient (packet 7.5)

Between slice B3 landing and the cut, doc-health reports **eight**
`ERROR`-severity `release-inventory-drift` findings, one per inventoried member.
That is the family working, and it is the reason the cut is sequenced inside the
change:

```sh
python3 -m scripts.doc_health --family release-inventory-drift .   # or as CI invokes it
python3 scripts/validate-contract-release.py verify-commit --commit "$(git rev-parse HEAD)"
```

## 10. What this quickstart deliberately cannot verify

- **The bundle cut.** The minor is allocated after the final integration point,
  which is a merge this lane does not perform ([research.md](./research.md) R-14).
- **The mapping row.** Its target file does not exist (R-5) and its
  `transferred_on` needs the transfer (R-6).
- **The clearing lane end to end** (runbook 10.5) — a sealed request from
  `codeXfactory/codexFactory` cannot be produced before the transfer.
- **`sync-notebooklm-books.py --apply`** — it writes to a live external service
  and is scheduled after the doc changes land.
