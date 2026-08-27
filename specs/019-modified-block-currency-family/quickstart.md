# Quickstart: validating F1

**Feature**: `019-modified-block-currency-family`
**Worktree**: the feature's own sibling worktree, named for the branch
(`openxFactory-worktrees/019-modified-block-currency-family` beside the root
checkout — resolve it at runtime, never hard-code the host path).

Every command below runs from that worktree root. Nothing here needs network,
credentials, or the aggregation checkout.

## Prerequisites

```bash
export SPECIFY_FEATURE_DIRECTORY=specs/019-modified-block-currency-family
python3 -c "import yaml" && echo "yaml present (dispositions reader needs it)"
python3 -m pytest tests/doc-health -q | tail -3   # BASELINE count, recorded before any edit
```

**`python3 -m pytest tests` (the whole tree) is NEVER run from a worktree.** It
drives live Postgres containers, and this feature's evidence does not need it:
the count delta is `python3 -m pytest tests/doc-health -q` only. Ruled
2026-08-27 (N12).

`git status -sb` must show branch `019-modified-block-currency-family`. Stage
with explicit pathspecs only; this checkout is shared.

## The RED gate (do this first, every task)

Every behaviour ships behind a test that FAILED first. The proof is mechanical:

```bash
# 1. write the test, run it, capture the failure
python3 -m pytest tests/doc-health/test_modified_block_currency.py -k <name> -q
#    -> must FAIL (ImportError before the module exists, or an assertion after)
# 2. write the behaviour
# 3. re-run -> must PASS, and the whole file must stay green
python3 -m pytest tests/doc-health/test_modified_block_currency.py -q
```

A task whose test passed on first run is not done — it is a test that does not
test anything, and it goes back.

## Running the family by hand

Against a fixture tree:

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "scripts"); sys.path.insert(0, "tests")
sys.path.insert(0, "tests/doc-health")
from conftest import make_ctx
from doc_health.families import FAMILIES
for f in FAMILIES["modified-block-currency"](make_ctx("modified-block-currency")):
    print(f.severity, f.path, "|", f.rule[:160])
PY
```

Against this repository's own tree (the shape F3 will assert; run it here only
to see the movement):

```bash
python3 - <<'PY'
import sys; from pathlib import Path
sys.path.insert(0, "scripts")
from doc_health import modified_block_currency as mbc
class Ctx:
    repo_paths = {"openxFactory": Path(".").resolve()}
    agg_root = None
for f in mbc.fam_modified_block_currency(Ctx()):
    print(f.severity, f.path, "|", f.rule[:160])
PY
```

**For the expected figures, read `plan.md` § Predicted movement and nowhere
else.** That table is the single home for the prediction (ruling B5); this file
deliberately does not restate it, because two copies of a prediction become two
predictions. Asserting it is F3's job; seeing it is how you know F1 landed.

## The sequencing gate (read this before touching the registry)

**Do not register the family until `add-family-enumeration-check` has archived
on `main` and this branch has merged it** (ruling B1). Registering earlier emits
three `family-enumeration` findings against THAT packet's delta path, which
nothing in this change can clear. Reproduce the measurement without touching
anything: monkeypatch `family_enumeration._registry` to return
`list(FAMILIES) + ["modified-block-currency"]`, call
`fe.fam_family_enumeration(Ctx())` with `repo_paths={"openxFactory": <root>}`,
and read the three findings — all on
`openspec/changes/add-family-enumeration-check/specs/doc-health/spec.md`. The
same call with the real registry reads zero.

If the archive is delayed, F1 stops at the end of phase 7 with the module
complete, tested and unregistered — a coherent state — and waits.

## The standing gate this feature must not red

```bash
python3 -m pytest tests/doc-health/test_family_enumeration.py -q
```

`test_the_real_corpus_reads_zero_on_both_halves` is a gate on `main`. It is RED
in any tree where the packet's doc-health delta carries the enumeration
restatement WITHOUT the registration, and GREEN only when both are present —
which is why they are one commit. To see the failure the packet recorded
(§ 6.5), stash nothing: add the block, drop the `FAMILIES` line, run the test,
put the line back.

## The registration checks

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, "scripts")
from doc_health import FAMILY_IDS
from doc_health.families import FAMILIES, FAMILY_RESOLUTION
assert set(FAMILY_IDS) == set(FAMILIES), "FAMILY_IDS must mirror FAMILIES"
assert len(FAMILIES) == 22, len(FAMILIES)
assert "modified-block-currency" not in FAMILY_RESOLUTION, "advisory launch"
print("registered:", len(FAMILIES), "families")
PY
python3 -m pytest tests/doc-health/test_lifecycle_scan_set.py -q
```

## The full gate set (the PR's own evidence)

```bash
python3 -m pytest tests/doc-health -q | tail -3        # green; count > baseline. THE evidence.
python3 -m pytest tests/doc-health/test_promotion_fidelity.py -q   # 59 tests, byte-green, untouched
python3 -m pytest tests/doc-health/test_duplicate_packet.py -q     # byte-green, untouched
OPENSPEC_TELEMETRY=0 openspec validate --all --strict  # 75 passed on this branch (23 active + 52 specs)
```

Record the pytest counts BEFORE and AFTER so the added tests are visible as a
delta rather than asserted.

## The mutation round (a task, not a nicety)

Each mutation below must make at least one named test FAIL. A surviving mutant
is a missing test, and the fix is the test.

| mutation | must break |
| --- | --- |
| `carried` uses `in` (containment) instead of equality | the widened-bullet test |
| `carried` ignores `kind` | the same-kind test (a body sentence "carried" by a bullet) |
| bullets compared within their own scenario only | the retitle-and-gut test |
| `normalize` also casefolds | the case-sensitivity pin |
| `normalize` strips trailing periods | the trailing-period pin |
| scenario-region prose is dropped instead of becoming a body unit | the O9 prose-unit pin |
| the family reads a basis field from the context | the no-measurement-basis pin |
| marker anchor drops the ISO-date group | the quoted-template test |
| marker anchor drops the change-id group | the quoted-template test |
| `extract_code_spans` uses `` `([^`]*)` `` | the longer-fence test |
| the `Merged into` destination is added to `names` | the destination-not-a-unit test |
| scenario-title suppression applies even with a new title | the § 3.3a combination test |
| `is_dated_bold_note` is tested BEFORE `parse_marker` | every marker test |
| ordering resolved by `created:` date | the no-date-consulted test |
| `_LAUNCH_SEVERITY` set to `ERROR` | the advisory-launch pin |
| the family added to `FAMILY_RESOLUTION` | the advisory-launch pin |
| the ledger emits one finding per UNIT instead of per requirement | the per-requirement granularity pin |
| the ledger's hedge sentence is dropped from the rule text | the no-intent-asserted pin |
| `_RESOLUTION_SEVERITY` set to `ERROR` (a half-flip of an arm section 7.2 does NOT move) | the three-severities pin |
| a canon-side marker paragraph becomes a carriage unit | the promoted-marker-is-not-a-unit pin |
| fenced-block lines are parsed as markers | the fenced-example case at T012 |

## Definition of done for F1

1. Every FR in `spec.md` has a named passing test that failed first.
2. `fam_family_enumeration` reads 0 and the doc-health suite is green in the
   SAME commit that registers the family.
3. `promotion_fidelity.py` and `duplicate_packet.py` are unmodified
   (`git diff --stat` shows neither).
4. `.github/workflows/`, `report.py` and every threshold are unmodified, and
   the REGISTRY is untouched until the sequencing gate opens (ruling B1).
5. The mutation table above has no survivors.
6. The adversarial-review task has run and its findings are dispositioned in
   `plan.md`.
