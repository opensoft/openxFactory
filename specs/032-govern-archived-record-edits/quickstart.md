# Quickstart: re-running everything this feature claims

**Feature**: `032-govern-archived-record-edits` | **Date**: 2026-09-08

Every claim in this feature is a command. Run them from the repository root of a
checkout on the feature branch. `PIN` is the pinned CLI prefix
(`<scratchpad>/cli-pin-prefix`); PATH's `openspec` is 1.2.0 and is never used.

## 0. Where you are

```bash
git branch --show-current            # 032-govern-archived-record-edits
git log --oneline -1                 # the head every result below is taken at
git diff main...HEAD --stat          # SC-007: the path set, and nothing under archive/
```

## 1. The pinned-CLI gates (task 4.1)

```bash
OPENSPEC_TELEMETRY=0 PATH="$PIN/bin:$PATH" \
  python3 scripts/validate-openspec-cli-pin.py --change govern-archived-record-edits --strict
OPENSPEC_TELEMETRY=0 PATH="$PIN/bin:$PATH" \
  python3 scripts/validate-openspec-cli-pin.py --all --strict
```

Expected: the `--change` run passes; the `--all` run reports ZERO
UNDISPOSITIONED findings (dispositioned exceptions are pre-existing and are
listed in the evidence file with their count at the ratified baseline for
comparison).

## 2. The corpus gates (task 4.3)

```bash
python3 scripts/validate-sequenced-after.py .
python3 scripts/validate-sequenced-after.py . --ledger-diff
python3 scripts/validate-scope-globs.py .
python3 scripts/validate-manifest-digests.py .
```

Expected: all exit 0; `--ledger-diff` reports `per-change sweep ledger consistent
with the corpus`.

## 3. doc-health, diffed against `main` (task 4.4)

**The identity trap first.** doc-health stamps the CHECKOUT'S DIRECTORY BASENAME
into every finding line (`repo=<basename>`), into the `Repo-Identity:` header and
into the "scope limited to single repo <name>" line. A baseline taken in
`../oxf-main` and a branch report taken in `oxf-realize-f3` therefore differ on
EVERY line, and `--previous-report` refuses the pair outright
(`REFUSE previous-report-identity-mismatch`).

```bash
# 1. baseline under an IDENTICAL basename, at a NAMED main sha
mkdir -p "$S/dh-base" && git -C "$S/dh-base" clone -q <this-repo> oxf-realize-f3
git -C "$S/dh-base/oxf-realize-f3" checkout -q <main-sha>

# 2. PROVE the recipe main-vs-main before trusting it: same commit, two dirs
python3 scripts/doc-health.py --single-repo "$S/dh-base/oxf-realize-f3" \
        --fail-on error --report-out /tmp/dh-a.md
python3 scripts/doc-health.py --single-repo <a second checkout of the same sha> \
        --fail-on error --report-out /tmp/dh-b.md
diff /tmp/dh-a.md /tmp/dh-b.md          # expect: ZERO differences

# 3. the real comparison
python3 scripts/doc-health.py --single-repo . --fail-on error \
        --report-out /tmp/dh-branch.md
diff /tmp/dh-main.md /tmp/dh-branch.md
```

If the basenames cannot be made identical, normalize all THREE stamped places
plus the run date before diffing:

```bash
norm() { sed -E 's/repo=[^ ,)]+/repo=X/g; /^Repo-Identity:/d; /scope limited to single repo/d' "$1" \
         | grep -v -E '^(Generated|Run date|As of)'; }
diff <(norm /tmp/dh-main.md) <(norm /tmp/dh-branch.md)
```

Expected: the FINDING SET is identical. Counts that move only because the
document GREW (word totals, canon share) are not findings — state them
separately, never smooth them away. A non-empty finding-set diff is a BLOCKER.

## 3a. The cross-citations against the landed twin (FR-007a, SC-010)

```bash
git clone --filter=blob:none git@github.com:opensoft/OpsxFactory.git "$S/opsx-verify"
git -C "$S/opsx-verify" merge-base --is-ancestor \
    bbbef015cd394e2de31586b9718356586c413884 origin/main && echo "twin on main"
grep -rn 'govern-archived-record-edits' "$S/opsx-verify/openspec/changes" | head
grep -rn 'OpsxFactory' openspec/changes/govern-archived-record-edits | head
```

Every citation each packet makes of the other MUST resolve at the two heads the
evidence file names. One that does not resolve STOPS the branch — it is not a
note.

## 4. The test suite (task 4.5)

```bash
pytest tests/sequenced_after tests/proposal-support tests/scope_globs -q > /tmp/pt.log 2>&1
echo "rc=$?"; tail -3 /tmp/pt.log
```

Capture the return code AND the summary line to a file. `pytest … | tail` proves
nothing: `tail`'s exit status is the pipeline's.

## 5. The MODIFIED-block currency measurement (task 4.2 — measured, NOT ticked)

```bash
python3 - <<'PY'
import re,pathlib
def block(p, head):
    t=pathlib.Path(p).read_text()
    i=t.index(head); j=t.find('\n### Requirement:', i+1)
    return t[i: j if j>0 else len(t)].rstrip('\n')
head='### Requirement: Proposal packets carry the lifecycle header'
canon=block('openspec/specs/document-lifecycle/spec.md', head)
delta=block('openspec/changes/govern-archived-record-edits/specs/document-lifecycle/spec.md', head)
print('canon chars', len(canon), 'delta chars', len(delta))
import difflib
d=[l for l in difflib.unified_diff(canon.splitlines(), delta.splitlines(), lineterm='')]
print('canon lines removed:', sum(1 for l in d if l.startswith('-') and not l.startswith('---')))
PY
```

Expected: canon 5,815 characters, delta 7,186, **0 canon lines removed** — the
1,371-character difference entirely inserted. Box 4.2 stays UNTICKED: the rule
demands currency continuously until archive, and the archive act re-runs this.

## 6. The pinned-target measurement (task 4 note, FR-008)

```bash
grep -rn 'sha256' --include='*.yaml' --include='*.yml' --include='*.json' . \
  | grep -i 'document-lifecycle'          # expect: nothing outside examples/
```

Expected: no IN-REPO `sha256` pin names `docs/document-lifecycle.md`. Recorded at
base `68712924`.

## 7. What this feature deliberately does not do

`openspec archive`, `gh pr create`, any GitHub comment, any merge, any edit under
`openspec/changes/archive/`, any checker, any pin. Those are the lane's or nobody's.
